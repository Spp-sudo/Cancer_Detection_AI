from __future__ import annotations

from src.cancer_detector.inference import CancerDetectionResult


def format_text_report(result: CancerDetectionResult) -> str:
    alternatives = "\n".join(
        f"  - {prediction.label}: {prediction.probability:.1%}"
        for prediction in result.predictions[:5]
    )
    evidence = "\n".join(
        f"  - {name}: {value:.3f}"
        for name, value in result.evidence.items()
    )
    return (
        "Cancer Cell Detection Report\n"
        f"Prediction: {result.display_name}\n"
        f"Confidence: {result.confidence:.1%}\n"
        f"Cancer-cell likelihood: {result.cancer_cell_likelihood:.1%}\n"
        f"Model note: {result.description}\n"
        f"Recommendation: {result.recommendation}\n\n"
        "Top classes:\n"
        f"{alternatives}\n\n"
        "Image evidence:\n"
        f"{evidence}"
    )


def build_streamlit_summary(result: CancerDetectionResult) -> None:
    import streamlit as st

    st.subheader(result.display_name)
    st.write(result.description)

    metric_col_1, metric_col_2 = st.columns(2)
    metric_col_1.metric("Confidence", f"{result.confidence:.1%}")
    metric_col_2.metric("Cancer-cell likelihood", f"{result.cancer_cell_likelihood:.1%}")

    st.warning(result.recommendation)

    st.write("Top class probabilities")
    st.bar_chart({
        prediction.label: prediction.probability
        for prediction in result.predictions[:5]
    })

    st.write("Extracted image evidence")
    st.dataframe(
        [{"feature": name, "value": round(value, 4)} for name, value in result.evidence.items()],
        use_container_width=True,
        hide_index=True,
    )

