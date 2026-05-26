import streamlit as st

from frontend.api_client import APIClient, MODEL_GUIDANCE, MODEL_OPTIONS
from frontend.components.ui import glass_card, hero1_glow_background
from frontend.pages.history import render_history


def _title(eyebrow: str, title: str, subtitle: str, accent: str = "#5eb3ff") -> str:
    return (
        '<p style="font-family:\'Space Grotesk\',sans-serif;font-size:0.72rem;letter-spacing:0.2em;text-transform:uppercase;color:{};margin-bottom:0.25rem;">{}</p>'
        '<h1 style="font-family:Outfit,sans-serif;font-size:clamp(1.5rem,3vw,2rem);font-weight:700;letter-spacing:-0.02em;line-height:1.15;margin:0 0 0.5rem;background:linear-gradient(135deg,#fff,{});-webkit-background-clip:text;-webkit-text-fill-color:transparent;">{}</h1>'
        '<p style="font-size:1rem;color:#7a9bb8;max-width:48ch;margin:0 0 1.5rem;">{}</p>'
    ).format(accent, eyebrow, accent, title, subtitle)


def render_upload_study(api: APIClient) -> None:

    if st.session_state.get("show_doc_result") and st.session_state.get("doc_result"):
        from frontend.components.animations import result_reveal_banner
        from frontend.components.charts import malignancy_chart, subtype_chart
        from frontend.components.ui import metric_grid
        result = st.session_state["doc_result"]
        cm = result.get("confidence_metrics", {})
        st.markdown(
            '<div style="position:fixed;inset:0;pointer-events:none;overflow:hidden;z-index:0;">'
            + hero1_glow_background()
            + "</div>",
            unsafe_allow_html=True,
        )
        st.markdown(result_reveal_banner(result.get("classification", ""), result.get("study_id", ""), result.get("molecular_subtype", "")), unsafe_allow_html=True)
        st.markdown(metric_grid([("Confidence", f"{cm.get('primary_confidence', 0)*100:.0f}%"), ("Benign", f"{cm.get('benign_probability', 0)*100:.0f}%"), ("Malignant", f"{cm.get('malignancy_probability', 0)*100:.0f}%"), ("Urgency", st.session_state.get("urgency", "Routine"))]), unsafe_allow_html=True)
        if st.button("← Upload new study", key="doc_back_to_upload"):
            for k in ("doc_result", "doc_filename", "show_doc_result", "urgency"):
                st.session_state.pop(k, None)
            st.rerun()
        return

    st.markdown(
        '<div style="position:fixed;inset:0;pointer-events:none;overflow:hidden;z-index:0;">'
        + hero1_glow_background()
        + "</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        _title("Diagnostics", "Upload Imaging Study", "Upload patient imaging and provide clinical context for AI-powered analysis."),
        unsafe_allow_html=True,
    )

    col_upload, col_context = st.columns([1.2, 0.8], gap="large")

    with col_upload:
        st.markdown(
            '<div class="upload-aura" style="padding:2.5rem;border-radius:20px;text-align:center;">'
            '<div style="font-size:3rem;margin-bottom:1rem;">🩻</div>'
            '<p style="color:white;font-weight:600;font-size:1.05rem;margin:0 0 0.5rem;">Drop patient imaging here</p>'
            '<p style="color:#7a9bb8;font-size:0.85rem;margin:0 0 1.5rem;">DICOM · CT · MRI · X-Ray · PET</p>'
            "</div>",
            unsafe_allow_html=True,
        )
        uploaded = st.file_uploader(
            "Select imaging file",
            type=["png", "jpg", "jpeg", "tiff", "tif", "bmp", "dcm"],
            key="doc_study_upload",
            label_visibility="collapsed",
        )

        if uploaded:
            st.markdown(
                glass_card(
                    '<div style="display:flex;align-items:center;gap:0.75rem;">'
                    '<span style="font-size:1.5rem;">📄</span>'
                    '<div><strong style="color:white;font-size:0.9rem;">{}</strong>'
                    '<p style="color:#7a9bb8;font-size:0.8rem;margin:0.15rem 0 0;">{} · Ready for diagnostic pipeline</p></div>'
                    "</div>".format(uploaded.name, uploaded.type or "Unknown format")
                ),
                unsafe_allow_html=True,
            )

    with col_context:
        st.markdown(
            glass_card(
                '<p style="font-family:\'Space Grotesk\',sans-serif;font-size:0.72rem;letter-spacing:0.2em;text-transform:uppercase;color:#5eb3ff;margin-bottom:0.75rem;">Clinical intake</p>'
                '<h4 style="font-family:Outfit,sans-serif;color:white;margin:0 0 0.5rem;">Attending notes</h4>'
                '<p style="color:#7a9bb8;font-size:0.82rem;margin:0 0 1rem;">Enter clinical observations, suspected diagnosis, and relevant history.</p>'
            ),
            unsafe_allow_html=True,
        )

        description = st.text_area(
            "Clinical notes",
            height=100,
            key="doc_study_desc",
            placeholder="E.g., 65yo male, history of smoking, CT shows 2cm nodule in upper left lobe. Suspected adenocarcinoma. Patient reports persistent cough and weight loss.",
            label_visibility="collapsed",
        )

        model_name = st.selectbox(
            "AI Model",
            options=list(MODEL_OPTIONS.keys()),
            key="doc_model_select",
            help="Select the cancer-type model that matches the imaging study.",
        )
        st.caption(MODEL_GUIDANCE.get(model_name, ""))
        api.selected_model = model_name

        col_p1, col_p2 = st.columns(2)
        with col_p1:
            modality = st.selectbox("Modality", ["CT Scan", "MRI", "X-Ray", "Ultrasound", "Mammogram", "PET", "DICOM"], key="doc_modality")
        with col_p2:
            urgency = st.selectbox("Urgency", ["Routine", "Priority", "STAT"], key="doc_urgency")

        if st.button("🚀 Run Diagnostic Pipeline", key="upload_study_go", type="primary", disabled=uploaded is None, use_container_width=True):
            st.session_state["urgency"] = urgency
            with st.spinner("Running diagnostic pipeline..."):
                try:
                    result = api.predict(uploaded.name, uploaded.getvalue(), uploaded.type or "application/octet-stream")
                    st.session_state["doc_result"] = result
                    st.session_state["doc_filename"] = uploaded.name
                    st.session_state["show_doc_result"] = True
                    st.rerun()
                except Exception as exc:
                    st.error(f"Diagnostic pipeline failed: {exc}")


def render_doctor_profile() -> None:
    st.markdown(
        _title("Account", "Your Profile", "Manage your clinical practice settings and credentials."),
        unsafe_allow_html=True,
    )

    name = st.session_state.get("full_name", st.session_state.get("user_email", "").split("@")[0].title())
    email = st.session_state.get("user_email", "—")

    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.markdown(
            glass_card(
                '<div style="text-align:center;">'
                '<div style="width:80px;height:80px;border-radius:50%;background:linear-gradient(135deg,#5eb3ff,#0c0414);margin:0 auto 1rem;display:flex;align-items:center;justify-content:center;font-size:2.2rem;font-weight:700;">{}</div>'
                '<h3 style="font-family:Outfit,sans-serif;color:white;margin:0 0 0.25rem;">{}</h3>'
                '<p style="color:#7a9bb8;font-size:0.88rem;margin:0 0 1.5rem;">{} · Clinical Provider</p>'
                '<div style="display:flex;justify-content:center;gap:2rem;padding-top:1rem;border-top:1px solid rgba(255,255,255,0.06);">'
                '<div><p style="color:#7a9bb8;font-size:0.72rem;text-transform:uppercase;margin:0;">Studies</p><p style="color:white;font-weight:700;font-size:1.1rem;margin:0.15rem 0 0;">—</p></div>'
                '<div><p style="color:#7a9bb8;font-size:0.72rem;text-transform:uppercase;margin:0;">Role</p><p style="color:#5eb3ff;font-weight:600;font-size:1.1rem;margin:0.15rem 0 0;">Physician</p></div>'
                '<div><p style="color:#7a9bb8;font-size:0.72rem;text-transform:uppercase;margin:0;">Since</p><p style="color:white;font-weight:700;font-size:1.1rem;margin:0.15rem 0 0;">2025</p></div>'
                "</div>"
                "</div>".format(name[0].upper(), name, email)
            ),
            unsafe_allow_html=True,
        )


def render_doctor_system(api: APIClient) -> None:
    st.markdown(
        _title("Infrastructure", "System Status", "Real-time platform health and model registry."),
        unsafe_allow_html=True,
    )
    try:
        h = api.health()
        st.markdown(
            glass_card(
                f"""<div class="metric-grid">
                <div class="metric-tile"><div class="m-label">Status</div><div class="m-value">{h.get('status','—')}</div></div>
                <div class="metric-tile"><div class="m-label">Version</div><div class="m-value">{h.get('version','—')}</div></div>
                <div class="metric-tile"><div class="m-label">Model</div><div class="m-value" style="font-size:0.9rem">{h.get('model_name','—')}</div></div>
                <div class="metric-tile"><div class="m-label">DB</div><div class="m-value">{h.get('database','—')}</div></div>
                </div>"""
            ),
            unsafe_allow_html=True,
        )
        gpu = h.get("gpu", {})
        st.json({"gpu": gpu, "model_loaded": h.get("model_loaded")})
    except Exception as exc:
        st.error(str(exc))


def render_doctor_app(api: APIClient, page: str) -> None:
    if page == "Upload Study":
        render_upload_study(api)
    elif page == "Patient Records":
        render_history(api, portal="doctor")
    elif page == "System":
        render_doctor_system(api)
    elif page == "Profile":
        render_doctor_profile()
