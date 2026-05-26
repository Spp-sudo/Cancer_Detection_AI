from __future__ import annotations

import argparse
import os
from pathlib import Path

import numpy as np
import streamlit as st

from src.cancer_detector.inference import CancerDetectionPipeline
from src.cancer_detector.preprocessing import load_image


DEFAULT_MODEL_PATH = Path("models/cancer_classifier.joblib")
MIN_RECOGNITION_CONFIDENCE = 0.65
MIN_RECOGNITION_MARGIN = 0.2
MODEL_OPTIONS = {
    "Brain cancer model": Path("models/Brain.joblib"),
    "Breast cancer model": Path("models/Breast.joblib"),
    "Lung cancer model": Path("models/Lung.joblib"),
    "Pancreatic cancer model": Path("models/pan.joblib"),
    "Prostate cancer model": Path("models/pro.joblib"),
}
MODEL_GUIDANCE = {
    "Brain cancer model": "Upload brain MRI or similar grayscale brain scan images.",
    "Breast cancer model": "Upload breast MRI, PET, mammography, or pathology-style medical images.",
    "Lung cancer model": "Upload lung CT or PET scan images. Natural photos are rejected.",
    "Pancreatic cancer model": "Upload pancreatic CT, MRI, or histopathology medical images.",
    "Prostate cancer model": "Upload prostate MRI or prostate histopathology images.",
}
EVIDENCE_LABELS = {
    "dark_cell_density": "Dark region density",
    "nuclear_darkness": "Overall darkness",
    "stain_contrast": "Image contrast",
    "blue_purple_stain": "Blue/purple stain signal",
    "red_dominance": "Red tissue signal",
    "pigmentation_variation": "Color variation",
    "edge_complexity": "Texture complexity",
    "texture_entropy": "Texture variation",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--model", type=Path, default=None)
    args, _ = parser.parse_known_args()
    return args


def main() -> None:
    st.set_page_config(page_title="Cancer Cell Detection AI", layout="wide")
    initialize_history()

    st.title("Cancer Cell Detection AI")
    st.caption("Research prototype only. Not for clinical diagnosis.")
    history_container = st.sidebar.container()

    args = parse_args()
    selected_model_name = st.selectbox(
        "Select image/model type",
        options=list(MODEL_OPTIONS),
        index=0,
    )
    st.info(MODEL_GUIDANCE[selected_model_name])
    selected_model_path = MODEL_OPTIONS[selected_model_name]
    model_path = resolve_model_path(args.model, selected_model_path)

    try:
        pipeline = CancerDetectionPipeline.from_model_path(model_path)
    except Exception as error:
        st.error(f"Could not load model: {error}")
        st.info(f"Check that {selected_model_path} exists on the deployed server.")
        st.stop()

    if model_path is None:
        st.warning("No trained model found. Using fallback demo logic, so predictions may not match local results.")

    uploaded_file = st.file_uploader(
        "Upload an MRI, CT, PET, microscopy, or pathology image",
        type=["png", "jpg", "jpeg", "tif", "tiff", "bmp", "dcm", "dicom"],
    )

    if uploaded_file is None:
        st.info("Upload an image to run analysis.")
        build_prediction_history(history_container)
        return

    try:
        uploaded_file.seek(0)
        preview_image = load_image(uploaded_file)
    except Exception as error:
        st.error("This image could not be analyzed.")
        st.info(f"Upload a valid medical image file for the selected model. Details: {error}")
        build_prediction_history(history_container)
        return

    image_col, result_col = st.columns([1, 1])
    with image_col:
        st.image(preview_image, caption="Uploaded image", use_container_width=True)

    with result_col:
        quality_reasons = image_quality_rejection_reasons(preview_image, selected_model_name)
        if quality_reasons:
            build_random_image_screen(selected_model_name, quality_reasons)
            add_history_entry(uploaded_file.name, selected_model_name, "Rejected", "Unsupported image")
            build_prediction_history(history_container)
            return

        try:
            uploaded_file.seek(0)
            result = pipeline.predict(uploaded_file)
        except Exception as error:
            st.error("This image could not be analyzed.")
            st.info(f"Upload a valid medical image file for the selected model. Details: {error}")
            build_prediction_history(history_container)
            return

        if is_unrecognized_result(result):
            build_unrecognized_screen(selected_model_name, result)
            add_history_entry(uploaded_file.name, selected_model_name, "Rejected", "Low confidence")
            build_prediction_history(history_container)
            return

        build_polished_summary(selected_model_name, result)
        add_history_entry(
            uploaded_file.name,
            selected_model_name,
            result.display_name,
            f"{result.confidence:.1%}",
        )
        build_prediction_history(history_container)


def resolve_model_path(argument_path: Path | None, selected_model_path: Path) -> Path | None:
    if argument_path is not None:
        return argument_path

    environment_path = os.getenv("MODEL_PATH")
    if environment_path:
        return Path(environment_path)

    if selected_model_path.exists():
        return selected_model_path

    if DEFAULT_MODEL_PATH.exists():
        return DEFAULT_MODEL_PATH

    return None


def is_unrecognized_result(result) -> bool:
    second_probability = result.predictions[1].probability if len(result.predictions) > 1 else 0.0
    confidence_margin = result.confidence - second_probability
    return (
        result.confidence < MIN_RECOGNITION_CONFIDENCE
        or confidence_margin < MIN_RECOGNITION_MARGIN
    )


def image_quality_rejection_reasons(image, selected_model_name: str) -> list[str]:
    width, height = image.size
    array = np.asarray(image.convert("RGB"), dtype=np.float32) / 255.0
    red = array[:, :, 0]
    green = array[:, :, 1]
    blue = array[:, :, 2]
    gray = array.mean(axis=2)

    color_range = array.max(axis=2) - array.min(axis=2)
    mean_color_range = float(color_range.mean())
    colorful_pixel_fraction = float((color_range > 0.18).mean())
    grayscale_similarity = float(np.mean(np.abs(red - green) + np.abs(green - blue) + np.abs(red - blue)))
    brightness = float(gray.mean())
    contrast = float(gray.std())

    reasons: list[str] = []
    if width < 96 or height < 96:
        reasons.append("Image resolution is too small for reliable analysis.")
    if brightness < 0.02 or brightness > 0.98 or contrast < 0.015:
        reasons.append("Image is too blank, too dark, too bright, or too low contrast.")

    scan_models = ("Brain", "Lung", "Breast")
    if any(model_name in selected_model_name for model_name in scan_models):
        if mean_color_range > 0.12 or colorful_pixel_fraction > 0.25 or grayscale_similarity > 0.18:
            reasons.append("Image appears too colorful for the selected scan-style model.")
    elif mean_color_range > 0.35 and colorful_pixel_fraction > 0.55:
        reasons.append("Image appears more like a natural photo than a medical image.")

    return reasons


def build_unrecognized_screen(selected_model_name: str, result) -> None:
    st.error("Image not recognized by the selected model.")
    st.write(
        "The uploaded image does not look reliable enough for this model to classify. "
        "Please upload the correct medical image type for the selected model."
    )

    metric_col_1, metric_col_2 = st.columns(2)
    metric_col_1.metric("Top confidence", f"{result.confidence:.1%}")
    metric_col_2.metric("Selected model", selected_model_name)

    st.info(
        "Try another image, choose a different model, or retrain with more examples "
        "that match this image style."
    )


def build_random_image_screen(selected_model_name: str, reasons: list[str]) -> None:
    st.error("Unsupported image type.")
    st.write(
        "This image does not appear to match the medical image style expected by "
        f"{selected_model_name}."
    )
    st.write("Why it was rejected")
    for reason in reasons:
        st.warning(reason)
    st.info("Please upload a valid scan, pathology, or clinical medical image for the selected model.")


def build_polished_summary(selected_model_name: str, result) -> None:
    st.subheader(result.display_name)
    st.write(result.description)

    confidence_label = confidence_badge(result.confidence)
    metric_col_1, metric_col_2, metric_col_3 = st.columns(3)
    metric_col_1.metric("Confidence", f"{result.confidence:.1%}")
    metric_col_2.metric("Cancer-cell likelihood", f"{result.cancer_cell_likelihood:.1%}")
    metric_col_3.metric("Reliability", confidence_label)

    st.warning(result.recommendation)

    st.write("Top class probabilities")
    st.bar_chart({
        prediction.label: prediction.probability
        for prediction in result.predictions[:5]
    })

    st.write("Image evidence")
    st.dataframe(
        [
            {
                "feature": EVIDENCE_LABELS.get(name, name.replace("_", " ").title()),
                "score": round(value, 4),
            }
            for name, value in result.evidence.items()
        ],
        use_container_width=True,
        hide_index=True,
    )

    st.download_button(
        "Download report",
        data=build_text_report(selected_model_name, result),
        file_name="cancer_detection_report.txt",
        mime="text/plain",
    )


def confidence_badge(confidence: float) -> str:
    if confidence >= 0.85:
        return "High"
    if confidence >= 0.7:
        return "Medium"
    return "Low"


def build_text_report(selected_model_name: str, result) -> str:
    top_classes = "\n".join(
        f"- {prediction.label}: {prediction.probability:.1%}"
        for prediction in result.predictions[:5]
    )
    evidence = "\n".join(
        f"- {EVIDENCE_LABELS.get(name, name.replace('_', ' ').title())}: {value:.4f}"
        for name, value in result.evidence.items()
    )
    return (
        "Cancer Cell Detection AI Report\n"
        "Educational prototype only. Not for clinical diagnosis.\n\n"
        f"Selected model: {selected_model_name}\n"
        f"Prediction: {result.display_name}\n"
        f"Confidence: {result.confidence:.1%}\n"
        f"Cancer-cell likelihood: {result.cancer_cell_likelihood:.1%}\n"
        f"Reliability: {confidence_badge(result.confidence)}\n"
        f"Recommendation: {result.recommendation}\n\n"
        "Top classes:\n"
        f"{top_classes}\n\n"
        "Image evidence:\n"
        f"{evidence}\n"
    )


def initialize_history() -> None:
    if "prediction_history" not in st.session_state:
        st.session_state.prediction_history = []
    if "last_history_key" not in st.session_state:
        st.session_state.last_history_key = None


def add_history_entry(file_name: str, model_name: str, outcome: str, detail: str) -> None:
    history_key = (file_name, model_name, outcome, detail)
    if st.session_state.last_history_key == history_key:
        return

    st.session_state.prediction_history.insert(
        0,
        {
            "file": file_name,
            "model": model_name,
            "outcome": outcome,
            "detail": detail,
        },
    )
    st.session_state.prediction_history = st.session_state.prediction_history[:5]
    st.session_state.last_history_key = history_key


def build_prediction_history(container) -> None:
    with container:
        st.subheader("Recent results")
        if not st.session_state.prediction_history:
            st.caption("No predictions yet.")
            return

        for item in st.session_state.prediction_history:
            st.write(f"**{item['outcome']}**")
            st.caption(f"{item['model']} | {item['detail']} | {item['file']}")


if __name__ == "__main__":
    main()
