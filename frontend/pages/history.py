import pandas as pd
import streamlit as st

from frontend.api_client import APIClient
from frontend.components.charts import malignancy_chart, subtype_chart
from frontend.components.ui import empty_state, glass_card, skeleton_loader


def render_history(api: APIClient, portal: str = "doctor") -> None:
    is_user = portal == "user"
    title = "My Health Timeline" if is_user else "Patient Records & Analytics"
    accent = "#4dffc9" if is_user else "#5eb3ff"
    eyebrow = "Your history" if is_user else "Records"
    st.markdown(
        '<p style="font-family:\'Space Grotesk\',sans-serif;font-size:0.72rem;letter-spacing:0.2em;text-transform:uppercase;color:{};margin-bottom:0.25rem;">{}</p>'
        '<h2 style="font-family:Outfit,sans-serif;font-size:clamp(1.25rem,2.5vw,1.5rem);font-weight:700;letter-spacing:-0.02em;line-height:1.15;margin:0 0 0.5rem;background:linear-gradient(135deg,#fff,{});-webkit-background-clip:text;-webkit-text-fill-color:transparent;">{}</h2>'.format(accent, eyebrow, accent, title),
        unsafe_allow_html=True,
    )

    placeholder = st.empty()
    placeholder.markdown(skeleton_loader(4), unsafe_allow_html=True)

    try:
        rows = api.history()
    except Exception as exc:
        placeholder.empty()
        st.error(f"Could not load records: {exc}")
        return

    placeholder.empty()

    if not rows:
        st.markdown(
            empty_state(
                "📋",
                "No scans yet" if is_user else "No patient records",
                "Run an analysis to build your timeline." if is_user else "Diagnostic runs will appear here.",
            ),
            unsafe_allow_html=True,
        )
        return

    df = pd.DataFrame(rows)

    if not is_user:
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Studies", len(df))
        m2.metric("Malignant", int((df["classification"] == "Malignant").sum()))
        m3.metric("Benign", int((df["classification"] == "Benign").sum()))
        m4.metric("Avg Latency", f"{df['processing_time_ms'].mean():.0f} ms")

    st.markdown(
        glass_card(
            f'<p style="margin:0 0 0.5rem;color:var(--ol-muted);font-size:0.85rem">'
            f'{"Showing your saved analyses" if is_user else f"{len(df)} studies in database"}</p>'
        ),
        unsafe_allow_html=True,
    )

    display_cols = [
        "study_id",
        "filename",
        "modality",
        "classification",
        "malignancy_probability",
        "benign_probability",
        "created_at",
    ]
    if not is_user:
        display_cols.insert(-1, "model_name")

    st.dataframe(
        df[display_cols],
        use_container_width=True,
        hide_index=True,
        column_config={
            "malignancy_probability": st.column_config.ProgressColumn(
                "Malignancy", min_value=0, max_value=1, format="%.0%%"
            ),
            "benign_probability": st.column_config.ProgressColumn(
                "Benign", min_value=0, max_value=1, format="%.0%%"
            ),
        },
    )

    if not is_user and len(df) >= 2:
        st.markdown("#### Aggregate trends")
        c1, c2 = st.columns(2)
        mock_chart = {
            "malignancy_vector": {
                "timepoints_weeks": list(range(len(df))),
                "malignancy_index": df["malignancy_probability"].tolist(),
                "confidence_band_upper": (df["malignancy_probability"] + 0.05).clip(0, 1).tolist(),
                "confidence_band_lower": (df["malignancy_probability"] - 0.05).clip(0, 1).tolist(),
            },
            "subtype_accuracy": {
                "subtypes": df["modality"].unique().tolist()[:5] or ["CT"],
                "accuracy_pct": [92.0] * min(5, len(df["modality"].unique()) or 1),
            },
        }
        with c1:
            st.plotly_chart(malignancy_chart(mock_chart, portal), use_container_width=True)
        with c2:
            st.plotly_chart(subtype_chart(mock_chart, portal), use_container_width=True)
