from __future__ import annotations

from pathlib import Path
from typing import BinaryIO

import numpy as np
from PIL import Image, ImageOps

from src.cancer_detector.config import IMAGE_SIZE


ImageSource = str | Path | BinaryIO
DICOM_EXTENSIONS = {".dcm", ".dicom"}


def load_image(source: ImageSource) -> Image.Image:
    if source_suffix(source) in DICOM_EXTENSIONS:
        return load_dicom_image(source)

    image = Image.open(source)
    image = ImageOps.exif_transpose(image)
    return image.convert("RGB")


def preprocess_image(source: ImageSource, image_size: tuple[int, int] = IMAGE_SIZE) -> np.ndarray:
    image = load_image(source)
    image = ImageOps.fit(image, image_size, method=Image.Resampling.LANCZOS)
    array = np.asarray(image, dtype=np.float32) / 255.0
    return array


def source_suffix(source: ImageSource) -> str:
    if isinstance(source, str | Path):
        return Path(source).suffix.lower()
    return Path(str(getattr(source, "name", ""))).suffix.lower()


def load_dicom_image(source: ImageSource) -> Image.Image:
    try:
        import pydicom
    except ImportError as error:
        raise RuntimeError("DICOM files require pydicom. Install it with: pip install pydicom") from error

    dataset = pydicom.dcmread(source)
    pixels = dataset.pixel_array.astype(np.float32)

    slope = float(getattr(dataset, "RescaleSlope", 1.0))
    intercept = float(getattr(dataset, "RescaleIntercept", 0.0))
    pixels = pixels * slope + intercept

    if pixels.ndim == 3 and pixels.shape[-1] not in (3, 4):
        pixels = pixels[0]

    if pixels.ndim == 3 and pixels.shape[-1] in (3, 4):
        normalized = normalize_array(pixels[:, :, :3])
        return Image.fromarray(normalized, mode="RGB")

    if str(getattr(dataset, "PhotometricInterpretation", "")).upper() == "MONOCHROME1":
        pixels = pixels.max() - pixels

    normalized = normalize_array(pixels)
    return Image.fromarray(normalized, mode="L").convert("RGB")


def normalize_array(array: np.ndarray) -> np.ndarray:
    low, high = np.percentile(array, [1, 99])
    if high <= low:
        low = float(array.min())
        high = float(array.max())
    if high <= low:
        return np.zeros(array.shape, dtype=np.uint8)

    normalized = np.clip((array - low) / (high - low), 0.0, 1.0)
    return (normalized * 255).astype(np.uint8)
