"""Called by the Next.js API route. Writes JSON to stdout."""
from __future__ import annotations

import argparse
import json
import sys
import time
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from src.cancer_detector.inference import CancerDetectionPipeline

MODEL_MAP = {
    "Brain cancer model":      "models/Brain.joblib",
    "Breast cancer model":     "models/Breast.joblib",
    "Lung cancer model":       "models/Lung.joblib",
    "Pancreatic cancer model": "models/pan.joblib",
    "Prostate cancer model":   "models/pro.joblib",
}

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("image", type=Path)
    parser.add_argument("--model-name", default="Brain cancer model")
    args = parser.parse_args()

    model_path = Path(MODEL_MAP.get(args.model_name, "models/Brain.joblib"))
    if not model_path.exists():
        for p in MODEL_MAP.values():
            if Path(p).exists():
                model_path = Path(p)
                break

    t0 = time.perf_counter()
    pipeline = CancerDetectionPipeline.from_model_path(model_path)
    result = pipeline.predict(args.image)
    elapsed = (time.perf_counter() - t0) * 1000

    is_cancer = result.cancer_cell_likelihood >= 0.5
    print(json.dumps({
        "study_id": str(uuid.uuid4())[:8].upper(),
        "classification": "Malignant" if is_cancer else "Benign",
        "molecular_subtype": result.display_name,
        "confidence_metrics": {
            "primary_confidence": result.confidence,
            "benign_probability": 1.0 - result.cancer_cell_likelihood,
            "malignancy_probability": result.cancer_cell_likelihood,
        },
        "processing_time_ms": elapsed,
        "recommendation": result.recommendation,
        "predictions": [{"label": p.label, "probability": p.probability} for p in result.predictions[:5]],
        "evidence": result.evidence,
    }))

if __name__ == "__main__":
    main()
