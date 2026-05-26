from __future__ import annotations

import argparse
from pathlib import Path

from src.cancer_detector.inference import CancerDetectionPipeline
from src.cancer_detector.reporting import format_text_report


def main() -> None:
    parser = argparse.ArgumentParser(description="Run cancer cell image analysis.")
    parser.add_argument("image", type=Path, help="Path to the image to analyze.")
    parser.add_argument("--model", type=Path, default=None, help="Optional trained joblib model.")
    args = parser.parse_args()

    pipeline = CancerDetectionPipeline.from_model_path(args.model)
    result = pipeline.predict(args.image)
    print(format_text_report(result))


if __name__ == "__main__":
    main()

