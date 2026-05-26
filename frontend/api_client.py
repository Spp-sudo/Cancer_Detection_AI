"""
OncoLens API client with local-inference fallback.

When the remote API is reachable, all calls go to it.
When it is offline (or the token is the demo sentinel), the client
falls back to the local CancerDetectionPipeline so the UI works
without a running server.
"""
from __future__ import annotations

import io
import json
import os
import sys
import threading
import time
import uuid
from pathlib import Path
from typing import Any, Callable

import requests

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

API_BASE = os.getenv("ONCOLENS_API_URL", "http://127.0.0.1:8000").rstrip("/")

# ---------------------------------------------------------------------------
# Model registry — mirrors app.py MODEL_OPTIONS
# ---------------------------------------------------------------------------
MODEL_OPTIONS: dict[str, Path] = {
    "Brain cancer model":      _PROJECT_ROOT / "models" / "Brain.joblib",
    "Breast cancer model":     _PROJECT_ROOT / "models" / "Breast.joblib",
    "Lung cancer model":       _PROJECT_ROOT / "models" / "Lung.joblib",
    "Pancreatic cancer model": _PROJECT_ROOT / "models" / "pan.joblib",
    "Prostate cancer model":   _PROJECT_ROOT / "models" / "pro.joblib",
}

MODEL_GUIDANCE: dict[str, str] = {
    "Brain cancer model":      "Upload brain MRI or similar grayscale brain scan images.",
    "Breast cancer model":     "Upload breast MRI, PET, mammography, or pathology-style medical images.",
    "Lung cancer model":       "Upload lung CT or PET scan images. Natural photos are rejected.",
    "Pancreatic cancer model": "Upload pancreatic CT, MRI, or histopathology medical images.",
    "Prostate cancer model":   "Upload prostate MRI or prostate histopathology images.",
}

_DEMO_TOKEN = "demo_token"
_MIN_CONFIDENCE = 0.65
_MIN_MARGIN = 0.20


# ---------------------------------------------------------------------------
# Local inference helpers
# ---------------------------------------------------------------------------

def _load_local_pipeline(model_name: str):
    """Return a CancerDetectionPipeline for the given model name."""
    from src.cancer_detector.inference import CancerDetectionPipeline  # type: ignore
    model_path = MODEL_OPTIONS.get(model_name)
    if model_path is None or not model_path.exists():
        # Try any available model
        for p in MODEL_OPTIONS.values():
            if p.exists():
                model_path = p
                break
    return CancerDetectionPipeline.from_model_path(model_path)


def _result_to_dict(result, model_name: str, filename: str, elapsed_ms: float) -> dict[str, Any]:
    """Map CancerDetectionResult → frontend result dict schema."""
    is_cancer = result.cancer_cell_likelihood >= 0.5
    classification = "Malignant" if is_cancer else "Benign"

    # chart_data
    chart_data = {
        "malignancy_vector": {
            "timepoints_weeks": [0],
            "malignancy_index": [result.cancer_cell_likelihood],
            "confidence_band_upper": [min(1.0, result.cancer_cell_likelihood + 0.05)],
            "confidence_band_lower": [max(0.0, result.cancer_cell_likelihood - 0.05)],
        },
        "subtype_accuracy": {
            "subtypes": [p.label.replace("_", " ").title() for p in result.predictions[:5]],
            "accuracy_pct": [p.probability * 100 for p in result.predictions[:5]],
        },
    }

    # disease_breakdown from top predictions
    disease_breakdown = {
        p.label: p.probability
        for p in result.predictions[:5]
    }

    return {
        "study_id": str(uuid.uuid4())[:8].upper(),
        "filename": filename,
        "modality": "Medical Image",
        "model_name": model_name,
        "classification": classification,
        "molecular_subtype": result.display_name,
        "confidence_metrics": {
            "primary_confidence": result.confidence,
            "benign_probability": 1.0 - result.cancer_cell_likelihood,
            "malignancy_probability": result.cancer_cell_likelihood,
        },
        "processing_time_ms": elapsed_ms,
        "grad_cam_image_b64": None,
        "chart_data": chart_data,
        "disease_breakdown": disease_breakdown,
        "treatment_protocol": _build_treatment(classification, result.recommendation),
        "recommendation": result.recommendation,
        "evidence": result.evidence,
        "predictions": [{"label": p.label, "probability": p.probability} for p in result.predictions],
    }


def _build_treatment(classification: str, recommendation: str) -> list[dict]:
    if classification != "Malignant":
        return [{"medicine": "Routine follow-up", "dosage": "—", "route": "—", "cycle": "—", "purpose": recommendation}]
    return [
        {"medicine": "Oncology referral", "dosage": "—", "route": "—", "cycle": "Immediate", "purpose": recommendation},
        {"medicine": "Biopsy / Pathology", "dosage": "—", "route": "Tissue", "cycle": "STAT", "purpose": "Histological confirmation"},
    ]


def _local_predict(filename: str, content: bytes, model_name: str) -> dict[str, Any]:
    from src.cancer_detector.preprocessing import load_image  # type: ignore
    pipeline = _load_local_pipeline(model_name)
    t0 = time.perf_counter()
    result = pipeline.predict(io.BytesIO(content))
    elapsed_ms = (time.perf_counter() - t0) * 1000
    return _result_to_dict(result, model_name, filename, elapsed_ms)


# ---------------------------------------------------------------------------
# APIClient
# ---------------------------------------------------------------------------

class APIClient:
    def __init__(self) -> None:
        self.token: str | None = None
        self.selected_model: str = "Brain cancer model"

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _headers(self) -> dict[str, str]:
        h = {"Accept": "application/json"}
        if self.token:
            h["Authorization"] = f"Bearer {self.token}"
        return h

    def _is_demo(self) -> bool:
        return self.token == _DEMO_TOKEN

    def _api_online(self) -> bool:
        try:
            requests.get(f"{API_BASE}/health", timeout=3)
            return True
        except Exception:
            return False

    # ------------------------------------------------------------------
    # Auth
    # ------------------------------------------------------------------

    def login(self, email: str, password: str) -> dict[str, Any]:
        if not self._api_online():
            # Offline demo login — accept any credentials
            self.token = _DEMO_TOKEN
            return {
                "access_token": _DEMO_TOKEN,
                "email": email,
                "role": "doctor" if "doctor" in email or "admin" in email else "user",
            }
        r = requests.post(
            f"{API_BASE}/api/v1/auth/login",
            json={"email": email, "password": password},
            timeout=15,
        )
        r.raise_for_status()
        data = r.json()
        self.token = data["access_token"]
        return data

    def register(self, email: str, password: str, full_name: str, role: str = "doctor") -> dict[str, Any]:
        if not self._api_online():
            self.token = _DEMO_TOKEN
            return {"access_token": _DEMO_TOKEN, "email": email, "role": role}
        r = requests.post(
            f"{API_BASE}/api/v1/auth/register?full_name={full_name}&role={role}",
            json={"email": email, "password": password},
            headers=self._headers(),
            timeout=15,
        )
        if r.status_code == 401:
            raise PermissionError("Registration requires admin privileges. Contact your administrator.")
        r.raise_for_status()
        data = r.json()
        self.token = data["access_token"]
        return data

    # ------------------------------------------------------------------
    # Health
    # ------------------------------------------------------------------

    def health(self) -> dict[str, Any]:
        if self._is_demo() or not self._api_online():
            available = [name for name, p in MODEL_OPTIONS.items() if p.exists()]
            return {
                "status": "local",
                "version": "local",
                "model_name": self.selected_model,
                "model_loaded": bool(available),
                "database": "local",
                "available_models": available,
            }
        r = requests.get(f"{API_BASE}/health", timeout=5)
        r.raise_for_status()
        return r.json()

    # ------------------------------------------------------------------
    # Prediction
    # ------------------------------------------------------------------

    def create_job(self) -> str:
        if self._is_demo() or not self._api_online():
            return str(uuid.uuid4())
        r = requests.post(f"{API_BASE}/api/v1/predict/jobs", headers=self._headers(), timeout=10)
        r.raise_for_status()
        return r.json()["job_id"]

    def predict(
        self,
        filename: str,
        content: bytes,
        content_type: str,
        job_id: str | None = None,
        on_progress: Callable[[dict], None] | None = None,
        model_name: str | None = None,
    ) -> dict[str, Any]:
        effective_model = model_name or self.selected_model

        # Always use local inference when demo token or API offline
        if self._is_demo() or not self._api_online():
            if on_progress:
                for pct, stage in ((20, "Loading model"), (60, "Extracting features"), (90, "Classifying")):
                    on_progress({"percent": pct, "stage": stage, "message": ""})
            return _local_predict(filename, content, effective_model)

        if job_id is None:
            job_id = self.create_job()

        if on_progress:
            ws_thread = threading.Thread(
                target=self._consume_ws, args=(job_id, on_progress), daemon=True
            )
            ws_thread.start()

        files = {"image": (filename, content, content_type)}
        data = {"job_id": job_id}
        r = requests.post(
            f"{API_BASE}/api/v1/predict",
            headers=self._headers(),
            files=files,
            data=data,
            timeout=180,
        )
        r.raise_for_status()
        return r.json()

    def _consume_ws(self, job_id: str, callback: Callable[[dict], None]) -> None:
        try:
            import websocket  # type: ignore
            ws_url = API_BASE.replace("http://", "ws://").replace("https://", "wss://")
            ws = websocket.create_connection(f"{ws_url}/api/v1/ws/progress/{job_id}", timeout=120)
            while True:
                raw = ws.recv()
                if not raw:
                    break
                msg = json.loads(raw)
                callback(msg)
                if msg.get("percent", 0) >= 100:
                    break
            ws.close()
        except Exception:
            pass

    # ------------------------------------------------------------------
    # History
    # ------------------------------------------------------------------

    def history(self, limit: int = 50) -> list[dict]:
        if self._is_demo() or not self._api_online():
            return []
        r = requests.get(
            f"{API_BASE}/api/v1/history/scans",
            headers=self._headers(),
            params={"limit": limit},
            timeout=15,
        )
        r.raise_for_status()
        return r.json()

    # ------------------------------------------------------------------
    # Reports
    # ------------------------------------------------------------------

    def download_pdf(self, study_id: str, note: str = "") -> bytes:
        if self._is_demo() or not self._api_online():
            raise RuntimeError("PDF export requires a live API connection.")
        r = requests.get(
            f"{API_BASE}/api/v1/reports/{study_id}/pdf",
            headers=self._headers(),
            params={"clinician_note": note},
            timeout=60,
        )
        r.raise_for_status()
        return r.content
