from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from src.cancer_detector.config import CANCER_CLASS_INFO
from src.cancer_detector.feature_extractor import CellFeatureExtractor
from src.cancer_detector.models import ClassPrediction, load_model
from src.cancer_detector.preprocessing import ImageSource, preprocess_image


NON_CANCER_LABELS = {"benign", "healthy", "negative", "no_cancer", "normal"}
CANCER_LABELS = {
    "breast_cancer",
    "brain_cancer",
    "bladder_cancer",
    "cancer",
    "cancer_cells",
    "colon_cancer",
    "colorectal_cancer",
    "kidney_cancer",
    "leukemia",
    "liver_cancer",
    "lung_cancer",
    "lymphoma",
    "malignant",
    "pancreatic_cancer",
    "positive",
    "prostate_cancer",
    "skin_melanoma",
    "soft_tissue_sarcoma",
}


@dataclass(frozen=True)
class CancerDetectionResult:
    predicted_label: str
    display_name: str
    description: str
    confidence: float
    cancer_cell_likelihood: float
    predictions: list[ClassPrediction]
    evidence: dict[str, float]
    recommendation: str


class CancerDetectionPipeline:
    def __init__(self, model, feature_extractor: CellFeatureExtractor | None = None) -> None:
        self.model = model
        self.feature_extractor = feature_extractor or CellFeatureExtractor()

    @classmethod
    def from_model_path(cls, model_path: Path | None = None) -> "CancerDetectionPipeline":
        return cls(model=load_model(model_path))

    def predict(self, source: ImageSource) -> CancerDetectionResult:
        image = preprocess_image(source)
        features = self.feature_extractor.extract(image)
        predictions = self.model.predict_proba(features.vector)
        best = predictions[0]
        class_info = CANCER_CLASS_INFO.get(best.label)

        malignant_probability = self._cancer_cell_likelihood(predictions)

        recommendation = self._recommend(best.probability, malignant_probability)

        return CancerDetectionResult(
            predicted_label=best.label,
            display_name=class_info.display_name if class_info else best.label.replace("_", " ").title(),
            description=class_info.description if class_info else "Custom trained class.",
            confidence=best.probability,
            cancer_cell_likelihood=malignant_probability,
            predictions=predictions,
            evidence=features.evidence,
            recommendation=recommendation,
        )

    @staticmethod
    def _cancer_cell_likelihood(predictions: list[ClassPrediction]) -> float:
        non_cancer_probability = sum(
            item.probability
            for item in predictions
            if item.label.lower() in NON_CANCER_LABELS
        )
        if non_cancer_probability > 0.0:
            return max(0.0, min(1.0, 1.0 - non_cancer_probability))

        cancer_probability = sum(
            item.probability
            for item in predictions
            if item.label.lower() in CANCER_LABELS
        )
        if cancer_probability > 0.0:
            return max(0.0, min(1.0, cancer_probability))

        return 1.0

    @staticmethod
    def _recommend(confidence: float, malignant_probability: float) -> str:
        if malignant_probability >= 0.7 and confidence >= 0.45:
            return "High-risk pattern detected. Send for expert pathology review."
        if malignant_probability >= 0.45:
            return "Suspicious pattern detected. Review with a trained clinician or pathologist."
        return "Low-risk output from this model. Do not treat this as a clinical rule-out."
