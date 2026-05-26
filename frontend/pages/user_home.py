import streamlit as st

from frontend.api_client import APIClient, MODEL_GUIDANCE, MODEL_OPTIONS
from frontend.components.ui import glass_card, hero1_glow_background
from frontend.pages.analysis import render_analysis
from frontend.pages.history import render_history


def _title(eyebrow: str, title: str, subtitle: str, accent: str = "#4dffc9") -> str:
    return (
        '<p style="font-family:\'Space Grotesk\',sans-serif;font-size:0.72rem;letter-spacing:0.2em;text-transform:uppercase;color:{};margin-bottom:0.25rem;">{}</p>'
        '<h1 style="font-family:Outfit,sans-serif;font-size:clamp(1.5rem,3vw,2rem);font-weight:700;letter-spacing:-0.02em;line-height:1.15;margin:0 0 0.5rem;background:linear-gradient(135deg,#fff,{});-webkit-background-clip:text;-webkit-text-fill-color:transparent;">{}</h1>'
        '<p style="font-size:1rem;color:#7a9bb8;max-width:48ch;margin:0 0 1.5rem;">{}</p>'
    ).format(accent, eyebrow, accent, title, subtitle)


def render_upload_scan(api: APIClient) -> None:

    st.markdown(
        '<div style="position:fixed;inset:0;pointer-events:none;overflow:hidden;z-index:0;">'
        + hero1_glow_background()
        + "</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        _title("Step 1 · Upload", "Share your scan", "Upload your medical imaging study and provide clinical context for AI analysis."),
        unsafe_allow_html=True,
    )

    col_upload, col_context = st.columns([1.2, 0.8], gap="large")

    with col_upload:
        st.markdown(
            '<div class="upload-aura" style="padding:2.5rem;border-radius:20px;text-align:center;">'
            '<div style="font-size:3rem;margin-bottom:1rem;">🫁</div>'
            '<p style="color:white;font-weight:600;font-size:1.05rem;margin:0 0 0.5rem;">Drop your scan here</p>'
            '<p style="color:#7a9bb8;font-size:0.85rem;margin:0 0 1.5rem;">PNG, JPEG, TIFF, BMP, DICOM (.dcm)</p>'
            "</div>",
            unsafe_allow_html=True,
        )
        uploaded = st.file_uploader(
            "Select imaging file",
            type=["png", "jpg", "jpeg", "tiff", "tif", "bmp", "dcm"],
            key="user_scan_upload",
            label_visibility="collapsed",
        )

        if uploaded:
            st.markdown(
                glass_card(
                    '<div style="display:flex;align-items:center;gap:0.75rem;">'
                    '<span style="font-size:1.5rem;">📄</span>'
                    '<div><strong style="color:white;font-size:0.9rem;">{}</strong>'
                    '<p style="color:#7a9bb8;font-size:0.8rem;margin:0.15rem 0 0;">{} · Ready for analysis</p></div>'
                    "</div>".format(uploaded.name, uploaded.type or "Unknown format")
                ),
                unsafe_allow_html=True,
            )

    with col_context:
        st.markdown(
            glass_card(
                '<p style="font-family:\'Space Grotesk\',sans-serif;font-size:0.72rem;letter-spacing:0.2em;text-transform:uppercase;color:#4dffc9;margin-bottom:0.75rem;">Clinical context</p>'
                '<h4 style="font-family:Outfit,sans-serif;color:white;margin:0 0 0.5rem;">Describe your concern</h4>'
                '<p style="color:#7a9bb8;font-size:0.82rem;margin:0 0 1rem;">Provide relevant medical history or symptoms to help the AI deliver more accurate insights.</p>'
            ),
            unsafe_allow_html=True,
        )

        description = st.text_area(
            "Description",
            height=120,
            key="user_scan_desc",
            placeholder="E.g., Patient presents with persistent cough and history of smoking. Suspected nodules in upper left lobe...",
            label_visibility="collapsed",
        )

        model_name = st.selectbox(
            "Cancer model",
            options=list(MODEL_OPTIONS.keys()),
            key="user_model_select",
            help="Choose the model that matches your scan type.",
        )
        st.caption(MODEL_GUIDANCE.get(model_name, ""))
        api.selected_model = model_name

        study_type = st.selectbox(
            "Study type",
            ["CT Scan", "MRI", "X-Ray", "Ultrasound", "Mammogram", "DICOM"],
            key="user_study_type",
            label_visibility="visible",
        )

        if st.button("✨ Start AI Health Analysis", key="upload_scan_go", type="primary", disabled=uploaded is None, use_container_width=True):
            st.session_state["upload_description"] = description
            st.session_state["study_type"] = study_type
            with st.spinner("Analyzing your scan with AI..."):
                try:
                    result = api.predict(uploaded.name, uploaded.getvalue(), uploaded.type or "application/octet-stream")
                    st.session_state["result"] = result
                    st.session_state["filename"] = uploaded.name
                    st.session_state["image_bytes"] = uploaded.getvalue()
                    st.session_state["clinician_note"] = description
                    st.session_state["show_result"] = True
                    st.rerun()
                except Exception as exc:
                    st.error(f"Analysis failed: {exc}")

    if st.session_state.get("show_result") and st.session_state.get("result"):
        st.divider()
        from frontend.components.animations import result_reveal_banner
        from frontend.components.ui import metric_grid
        result = st.session_state["result"]
        cm = result.get("confidence_metrics", {})
        st.markdown(result_reveal_banner(result.get("classification", ""), result.get("study_id", ""), result.get("molecular_subtype", "")), unsafe_allow_html=True)
        st.markdown(metric_grid([("Confidence", f"{cm.get('primary_confidence', 0)*100:.0f}%"), ("Benign", f"{cm.get('benign_probability', 0)*100:.0f}%"), ("Malignant", f"{cm.get('malignancy_probability', 0)*100:.0f}%"), ("Speed", f"{result.get('processing_time_ms', 0):.0f}ms")]), unsafe_allow_html=True)
        if st.button("← Upload another scan", key="back_to_upload"):
            for k in ("result", "filename", "image_bytes", "clinician_note", "show_result"):
                st.session_state.pop(k, None)
            st.rerun()


def render_user_profile() -> None:
    st.markdown(
        _title("Account", "Your Profile", "Manage your personal information and preferences."),
        unsafe_allow_html=True,
    )

    name = st.session_state.get("full_name", st.session_state.get("user_email", "").split("@")[0].title())
    email = st.session_state.get("user_email", "—")

    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.markdown(
            glass_card(
                '<div style="text-align:center;">'
                '<div style="width:80px;height:80px;border-radius:50%;background:linear-gradient(135deg,#4dffc9,#0c0414);margin:0 auto 1rem;display:flex;align-items:center;justify-content:center;font-size:2.2rem;font-weight:700;">{}</div>'
                '<h3 style="font-family:Outfit,sans-serif;color:white;margin:0 0 0.25rem;">{}</h3>'
                '<p style="color:#7a9bb8;font-size:0.88rem;margin:0 0 1.5rem;">{}</p>'
                '<div style="display:flex;justify-content:center;gap:2rem;padding-top:1rem;border-top:1px solid rgba(255,255,255,0.06);">'
                '<div><p style="color:#7a9bb8;font-size:0.72rem;text-transform:uppercase;margin:0;">Studies</p><p style="color:white;font-weight:700;font-size:1.1rem;margin:0.15rem 0 0;">—</p></div>'
                '<div><p style="color:#7a9bb8;font-size:0.72rem;text-transform:uppercase;margin:0;">Role</p><p style="color:#4dffc9;font-weight:600;font-size:1.1rem;margin:0.15rem 0 0;">Patient</p></div>'
                '<div><p style="color:#7a9bb8;font-size:0.72rem;text-transform:uppercase;margin:0;">Since</p><p style="color:white;font-weight:700;font-size:1.1rem;margin:0.15rem 0 0;">2025</p></div>'
                "</div>"
                "</div>".format(name[0].upper(), name, email)
            ),
            unsafe_allow_html=True,
        )


def render_user_help() -> None:
    st.markdown(
        _title("Support", "We're here to help", "Simple answers about your OncoLens experience."),
        unsafe_allow_html=True,
    )
    faqs = [
        ("Is my data safe?", "Yes. Scans are transmitted over secure APIs with authentication. Never share passwords."),
        ("What file types work?", "PNG, JPEG, TIFF, BMP, and DICOM (.dcm) from CT, MRI, or X-ray."),
        ("Can this diagnose me?", "No. OncoLens supports your care team — always follow your doctor's guidance."),
        ("What is the heatmap?", "It shows where the AI focused — like highlighting important areas on your scan."),
    ]
    for q, a in faqs:
        st.markdown(glass_card(f"<strong>{q}</strong><p style='margin:0.35rem 0 0;color:var(--ol-muted)'>{a}</p>"), unsafe_allow_html=True)


def render_user_app(api: APIClient, page: str) -> None:
    if page == "Upload Scan":
        render_upload_scan(api)
    elif page == "My Results":
        render_history(api, portal="user")
    elif page == "Profile":
        render_user_profile()
    elif page == "Help":
        render_user_help()
