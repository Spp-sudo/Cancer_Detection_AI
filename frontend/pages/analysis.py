import base64
import io
from datetime import datetime, timezone

import streamlit as st
import streamlit.components.v1 as components
from PIL import Image

from frontend.api_client import APIClient
from frontend.components.animations import ai_processing_loader, result_reveal_banner, scan_upload_animation
from frontend.components.charts import malignancy_chart, subtype_chart
from frontend.components.reports import ehr_text, treatment_card_html
from frontend.components.ui import glass_card, metric_grid


def _friendly_summary(result: dict) -> str:
    cls = result.get("classification", "")
    cm = result.get("confidence_metrics", {})
    if cls == "Benign":
        return (
            "Our AI did not detect strong signs of malignancy in this scan. "
            f"Confidence: {cm.get('primary_confidence', 0)*100:.0f}%. "
            "Please discuss with your doctor before making any decisions."
        )
    return (
        "Our AI detected patterns that may need further clinical review. "
        f"Confidence: {cm.get('primary_confidence', 0)*100:.0f}%. "
        "Please consult your oncology team promptly."
    )


def render_analysis(api: APIClient, portal: str = "doctor") -> None:
    is_user = portal == "user"

    if is_user:
        st.markdown(
            '<p style="font-family:\'Space Grotesk\',sans-serif;font-size:0.72rem;letter-spacing:0.2em;text-transform:uppercase;color:#4dffc9;margin-bottom:0.25rem;">Step 1 · Upload</p>'
            '<h2 style="font-family:Outfit,sans-serif;font-size:clamp(1.25rem,2.5vw,1.6rem);font-weight:700;letter-spacing:-0.02em;line-height:1.15;margin:0 0 0.5rem;background:linear-gradient(135deg,#fff,#4dffc9);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">Share your scan</h2>',
            unsafe_allow_html=True,
        )
        st.markdown(scan_upload_animation(), unsafe_allow_html=True)

    uploaded = st.file_uploader(
        "Select imaging study" if not is_user else "Your scan file",
        type=["png", "jpg", "jpeg", "tiff", "tif", "bmp", "dcm"],
        label_visibility="collapsed",
    )

    note_label = "Notes for your doctor (optional)" if is_user else "Clinician attestation"
    note = st.text_area(note_label, height=64, placeholder="Add context for the medical record…", label_visibility="visible")

    btn_label = "✨ Start AI Health Analysis" if is_user else "Run Diagnostic Pipeline"
    btn_key = "analysis_run_user" if is_user else "analysis_run_doc"
    if st.button(btn_label, key=btn_key, type="primary", disabled=uploaded is None, use_container_width=True):
        if uploaded is None:
            return
        progress_box = st.empty()
        state = {"pct": 0, "stage": "Initializing", "msg": "Preparing secure pipeline"}

        def on_progress(msg: dict) -> None:
            state.update(
                pct=msg.get("percent", 0),
                stage=msg.get("stage", "Processing").title(),
                msg=msg.get("message", ""),
            )

        try:
            progress_box.markdown(
                ai_processing_loader(state["stage"], state["msg"], state["pct"]),
                unsafe_allow_html=True,
            )
            result = api.predict(
                uploaded.name,
                uploaded.getvalue(),
                uploaded.type or "application/octet-stream",
                on_progress=on_progress,
            )
            st.session_state["result"] = result
            st.session_state["filename"] = uploaded.name
            st.session_state["image_bytes"] = uploaded.getvalue()
            st.session_state["clinician_note"] = note
            progress_box.empty()
        except Exception as exc:
            progress_box.empty()
            st.error(f"Analysis failed: {exc}")
            return

    if "result" not in st.session_state:
        if is_user:
            st.markdown(
                glass_card(
                    "<p style='margin:0;color:var(--ol-muted)'>No results yet. "
                    "Upload a scan above to begin your AI-assisted review.</p>"
                ),
                unsafe_allow_html=True,
            )
        return

    result = st.session_state["result"]
    filename = st.session_state.get("filename", "study")
    image_bytes = st.session_state.get("image_bytes")
    note = st.session_state.get("clinician_note", "")
    cm = result.get("confidence_metrics", {})

    st.markdown(
        result_reveal_banner(
            result.get("classification", ""),
            result.get("study_id", ""),
            result.get("molecular_subtype", ""),
        ),
        unsafe_allow_html=True,
    )

    if is_user:
        st.markdown(glass_card(f"<p style='margin:0;line-height:1.6'>{_friendly_summary(result)}</p>"), unsafe_allow_html=True)

    st.markdown(
        metric_grid(
            [
                ("Confidence", f"{cm.get('primary_confidence', 0)*100:.0f}%"),
                ("Benign", f"{cm.get('benign_probability', 0)*100:.0f}%"),
                ("Malignant", f"{cm.get('malignancy_probability', 0)*100:.0f}%"),
                ("Speed", f"{result.get('processing_time_ms', 0):.0f}ms"),
            ]
        ),
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2, gap="medium")
    with col1:
        st.markdown('<div class="scan-frame-3d">', unsafe_allow_html=True)
        if image_bytes:
            try:
                st.image(Image.open(io.BytesIO(image_bytes)), use_container_width=True)
            except Exception:
                st.warning("Preview unavailable")
        st.markdown("</div>", unsafe_allow_html=True)
        st.caption(filename)
    with col2:
        st.markdown("**AI Focus Map (Grad-CAM)**" if not is_user else "**What the AI focused on**")
        b64 = result.get("grad_cam_image_b64")
        if b64:
            st.image(
                Image.open(io.BytesIO(base64.b64decode(b64))),
                use_container_width=True,
                caption="Highlighted regions influenced the prediction",
            )
        else:
            st.info("Explainability map unavailable.")

    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(malignancy_chart(result.get("chart_data", {}), portal), use_container_width=True)
    with c2:
        st.plotly_chart(subtype_chart(result.get("chart_data", {}), portal), use_container_width=True)

    if not is_user:
        components.html(
            treatment_card_html(result.get("treatment_protocol", []), result.get("disease_breakdown", {})),
            height=360,
            scrolling=True,
        )
    else:
        with st.expander("View detailed treatment information (for your physician)", expanded=False):
            components.html(
                treatment_card_html(result.get("treatment_protocol", []), result.get("disease_breakdown", {})),
                height=300,
                scrolling=True,
            )

    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    study_id = result.get("study_id", "report")
    d1, d2 = st.columns(2)
    with d1:
        st.download_button(
            "📄 Download Summary (TXT)" if is_user else "Export TXT",
            ehr_text(result, filename, note),
            f"oncolens_{stamp}.txt",
            "text/plain",
            use_container_width=True,
        )
    with d2:
        try:
            pdf = api.download_pdf(study_id, note)
            st.download_button(
                "📑 Download Medical Report (PDF)" if is_user else "Export PDF",
                pdf,
                f"oncolens_{stamp}.pdf",
                "application/pdf",
                use_container_width=True,
            )
        except Exception as exc:
            st.caption(f"PDF unavailable: {exc}")
