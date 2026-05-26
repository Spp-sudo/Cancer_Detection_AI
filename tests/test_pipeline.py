from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import numpy as np
from PIL import Image

from src.cancer_detector.inference import CancerDetectionPipeline


class PipelineTest(unittest.TestCase):
    def test_pipeline_returns_prediction(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            image_path = Path(directory) / "sample.png"
            image = Image.fromarray(np.full((64, 64, 3), 180, dtype=np.uint8))
            image.save(image_path)

            result = CancerDetectionPipeline.from_model_path().predict(image_path)

        self.assertIn(result.predicted_label, {"cancer", "no_cancer"})
        self.assertGreaterEqual(result.confidence, 0.0)
        self.assertLessEqual(result.confidence, 1.0)
        self.assertGreaterEqual(result.cancer_cell_likelihood, 0.0)
        self.assertLessEqual(result.cancer_cell_likelihood, 1.0)
        self.assertTrue(result.evidence)


if __name__ == "__main__":
    unittest.main()

