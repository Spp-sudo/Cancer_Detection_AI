from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

import joblib
import numpy as np

from src.cancer_detector.config import CANCER_CLASSES


@dataclass(frozen=True)
class ClassPrediction:
    label: str
    probability: float


class CancerImageModel(Protocol):
    def predict_proba(self, features: np.ndarray) -> list[ClassPrediction]:
        ...


class HeuristicCancerModel:
    """Small binary fallback for demos before a real trained model exists."""

    classes = CANCER_CLASSES

    def predict_proba(self, features: np.ndarray) -> list[ClassPrediction]:
        dark_density, nuclear_darkness, contrast, _, _, pigmentation, edge_complexity, entropy = features

        cancer_likelihood = np.clip(
            0.28 * dark_density
            + 0.22 * nuclear_darkness
            + 0.18 * contrast
            + 0.17 * edge_complexity
            + 0.15 * entropy,
            0.0,
            1.0,
        )

        scores = {
            "cancer": cancer_likelihood + 0.08 * pigmentation,
            "no_cancer": 1.0 - cancer_likelihood,
        }

        return _softmax_predictions(scores)


class SklearnCancerModel:
    def __init__(self, model_path: Path) -> None:
        bundle = joblib.load(model_path)
        self.estimator = bundle["estimator"]
        self.classes = tuple(bundle["classes"])

    def predict_proba(self, features: np.ndarray) -> list[ClassPrediction]:
        probabilities = self.estimator.predict_proba([features])[0]
        predictions = [
            ClassPrediction(label=str(label), probability=float(probability))
            for label, probability in zip(self.classes, probabilities, strict=True)
        ]
        return sorted(predictions, key=lambda item: item.probability, reverse=True)


def load_model(model_path: Path | None) -> CancerImageModel:
    if model_path is None:
        return HeuristicCancerModel()
    return SklearnCancerModel(model_path)


def _softmax_predictions(scores: dict[str, float]) -> list[ClassPrediction]:
    labels = list(scores)
    values = np.array([scores[label] for label in labels], dtype=np.float32)
    values = values - values.max()
    probabilities = np.exp(values) / np.exp(values).sum()
    predictions = [
        ClassPrediction(label=label, probability=float(probability))
        for label, probability in zip(labels, probabilities, strict=True)
    ]
    return sorted(predictions, key=lambda item: item.probability, reverse=True)
