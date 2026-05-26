import streamlit as st

from frontend.components.ui import hero1_html, portal_tile


def render_portal() -> None:

    st.markdown(hero1_html(), unsafe_allow_html=True)

    st.markdown(
        '<div style="max-width:56rem;margin:0 auto;position:relative;z-index:1;padding:0 1rem;">',
        unsafe_allow_html=True,
    )
    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown(
            portal_tile(
                "🌿",
                "Patient Portal",
                "Upload scans, track health insights, and receive AI-guided reports in plain language.",
                "user",
            ),
            unsafe_allow_html=True,
        )
        if st.button("Enter Patient Portal →", key="go_user", use_container_width=True, type="primary"):
            st.session_state["route"] = "user_login"
            st.rerun()
    with c2:
        st.markdown(
            portal_tile(
                "⚕️",
                "Clinical Portal",
                "Enterprise diagnostics, patient records, analytics, and AI-assisted decision support.",
                "doctor",
            ),
            unsafe_allow_html=True,
        )
        if st.button("Enter Clinical Portal →", key="go_doc", use_container_width=True):
            st.session_state["route"] = "doctor_login"
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        '<p style="text-align:center;color:var(--ol-muted);font-size:0.82rem;margin-top:2rem">'
        "HIPAA-aware architecture · Grad-CAM explainability · Secure JWT authentication</p>",
        unsafe_allow_html=True,
    )
