from __future__ import annotations

import argparse
from pathlib import Path

from src.cancer_detector.training import extract_zip_dataset, format_image_counts, train_from_directory


def main() -> None:
    parser = argparse.ArgumentParser(description="Train a cancer image classifier.")
    parser.add_argument("--data", type=Path, default=Path("dataset"), help="Folder containing cancer/ and no_cancer/.")
    parser.add_argument("--zip-data", type=Path, default=None, help="Optional dataset .zip to extract before training.")
    parser.add_argument("--extract-to", type=Path, default=Path("colab_dataset"), help="Folder used for extracted zip data.")
    parser.add_argument("--output", type=Path, default=Path("models/cancer_classifier.joblib"))
    parser.add_argument("--test-size", type=float, default=0.2)
    args = parser.parse_args()

    try:
        dataset_dir = args.data
        if args.zip_data is not None:
            dataset_dir = extract_zip_dataset(args.zip_data, args.extract_to)
            print(f"Using extracted dataset: {dataset_dir}")

        metrics = train_from_directory(
            dataset_dir=dataset_dir,
            output_path=args.output,
            test_size=args.test_size,
        )
    except ValueError as error:
        parser.exit(2, f"Training data error: {error}\n")

    print(f"Saved model: {args.output}")
    print(f"Accuracy: {metrics.accuracy:.3f}")
    print("Classes:", ", ".join(metrics.classes))
    print("Images:", format_image_counts(metrics.image_counts))
    print("\nValidation report:")
    print(metrics.report)


if __name__ == "__main__":
    main()
