from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class ImageFeatures:
    vector: np.ndarray
    evidence: dict[str, float]


class CellFeatureExtractor:
    """Small, inspectable feature extractor for microscopy-style images."""

    def extract(self, image: np.ndarray) -> ImageFeatures:
        red = image[:, :, 0]
        green = image[:, :, 1]
        blue = image[:, :, 2]
        gray = image.mean(axis=2)

        darkness = 1.0 - float(gray.mean())
        contrast = float(gray.std())
        blue_purple_index = float(np.clip((blue.mean() + red.mean()) / 2.0 - green.mean(), 0.0, 1.0))
        red_dominance = float(np.clip(red.mean() - (green.mean() + blue.mean()) / 2.0, 0.0, 1.0))
        pigmentation = float(np.clip((red.std() + green.std() + blue.std()) / 3.0, 0.0, 1.0))

        high_density_mask = gray < np.quantile(gray, 0.35)
        dense_cell_fraction = float(high_density_mask.mean())

        edge_strength = self._edge_strength(gray)
        color_entropy = self._entropy(gray)

        evidence = {
            "dark_cell_density": dense_cell_fraction,
            "nuclear_darkness": darkness,
            "stain_contrast": contrast,
            "blue_purple_stain": blue_purple_index,
            "red_dominance": red_dominance,
            "pigmentation_variation": pigmentation,
            "edge_complexity": edge_strength,
            "texture_entropy": color_entropy,
        }
        vector = np.array(list(evidence.values()), dtype=np.float32)
        return ImageFeatures(vector=vector, evidence=evidence)

    @staticmethod
    def _edge_strength(gray: np.ndarray) -> float:
        dx = np.diff(gray, axis=1)
        dy = np.diff(gray, axis=0)
        return float(np.clip((np.abs(dx).mean() + np.abs(dy).mean()) * 2.0, 0.0, 1.0))

    @staticmethod
    def _entropy(gray: np.ndarray) -> float:
        histogram, _ = np.histogram(gray, bins=32, range=(0.0, 1.0), density=False)
        probabilities = histogram / max(1, histogram.sum())
        probabilities = probabilities[probabilities > 0]
        entropy = -np.sum(probabilities * np.log2(probabilities))
        return float(entropy / 5.0)

