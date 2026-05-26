from __future__ import annotations

import math
import shutil
import zipfile
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from src.cancer_detector.feature_extractor import CellFeatureExtractor
from src.cancer_detector.preprocessing import preprocess_image


SUPPORTED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp", ".dcm", ".dicom"}


@dataclass(frozen=True)
class TrainingMetrics:
    accuracy: float
    classes: tuple[str, ...]
    report: str
    image_counts: dict[str, int]


def train_from_directory(dataset_dir: Path, output_path: Path, test_size: float = 0.2) -> TrainingMetrics:
    features, labels = load_dataset_features(dataset_dir)
    image_counts = dict(sorted(Counter(labels).items()))
    validate_labels_for_training(image_counts)

    test_count = max(len(image_counts), math.ceil(len(labels) * test_size))

    x_train, x_test, y_train, y_test = train_test_split(
        features,
        labels,
        test_size=test_count,
        random_state=42,
        stratify=labels,
    )

    estimator = Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            ("classifier", RandomForestClassifier(n_estimators=250, random_state=42, class_weight="balanced")),
        ]
    )
    estimator.fit(x_train, y_train)

    predictions = estimator.predict(x_test)
    accuracy = float(accuracy_score(y_test, predictions))
    report = classification_report(y_test, predictions, zero_division=0)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(
        {
            "estimator": estimator,
            "classes": tuple(estimator.classes_),
            "feature_names": tuple(CellFeatureExtractor().extract(np.zeros((224, 224, 3), dtype=np.float32)).evidence),
            "report": report,
        },
        output_path,
    )

    return TrainingMetrics(
        accuracy=accuracy,
        classes=tuple(estimator.classes_),
        report=report,
        image_counts=image_counts,
    )


def extract_zip_dataset(zip_path: Path, extract_to: Path) -> Path:
    if not zip_path.exists():
        raise ValueError(f"Dataset zip does not exist: {zip_path}")
    if zip_path.suffix.lower() != ".zip":
        raise ValueError(f"Expected a .zip file, got: {zip_path}")

    extract_root = extract_to / zip_path.stem
    if extract_root.exists():
        shutil.rmtree(extract_root)
    extract_root.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(zip_path) as archive:
        archive.extractall(extract_root)

    return find_dataset_dir(extract_root)


def find_dataset_dir(search_root: Path) -> Path:
    candidates = [search_root, *[path for path in search_root.rglob("*") if path.is_dir()]]
    for candidate in candidates:
        class_dirs = [path for path in candidate.iterdir() if path.is_dir()]
        populated_class_dirs = [
            class_dir
            for class_dir in class_dirs
            if any(path.suffix.lower() in SUPPORTED_EXTENSIONS for path in class_dir.rglob("*"))
        ]
        if len(populated_class_dirs) >= 2:
            return candidate
    raise ValueError(
        "Could not find a dataset folder with at least two populated class folders "
        f"inside {search_root}."
    )


def load_dataset_features(dataset_dir: Path) -> tuple[np.ndarray, list[str]]:
    if not dataset_dir.exists():
        raise ValueError(f"Dataset folder does not exist: {dataset_dir}")

    extractor = CellFeatureExtractor()
    rows: list[np.ndarray] = []
    labels: list[str] = []

    for class_dir in sorted(path for path in dataset_dir.iterdir() if path.is_dir()):
        for image_path in sorted(class_dir.rglob("*")):
            if image_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
                continue
            image = preprocess_image(image_path)
            rows.append(extractor.extract(image).vector)
            labels.append(class_dir.name)

    if not rows:
        raise ValueError(
            f"No supported images found in {dataset_dir}. "
            "Put images inside class folders such as dataset/no_cancer/image1.png "
            "and dataset/leukemia/image1.png."
        )

    return np.vstack(rows), labels


def validate_labels_for_training(image_counts: dict[str, int]) -> None:
    if len(image_counts) < 2:
        raise ValueError(
            "Training requires at least two class folders with images. "
            f"Current image counts: {format_image_counts(image_counts)}"
        )

    too_small = {label: count for label, count in image_counts.items() if count < 2}
    if too_small:
        raise ValueError(
            "Each class needs at least 2 images so train/test splitting can be stratified. "
            f"Too small: {format_image_counts(too_small)}"
        )


def format_image_counts(image_counts: dict[str, int]) -> str:
    if not image_counts:
        return "none"
    return ", ".join(f"{label}={count}" for label, count in sorted(image_counts.items()))
