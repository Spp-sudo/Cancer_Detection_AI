import streamlit as st

from frontend.api_client import APIClient
from frontend.components.ui import glass_card, hero1_glow_background, metric_grid

_GLOW_WRAP = (
    '<div style="position:fixed;inset:0;pointer-events:none;overflow:hidden;z-index:0;">'
    + hero1_glow_background()
    + "</div>"
    '<div style="position:relative;z-index:1;">'
)


def render_doctor_login(api: APIClient) -> bool:

    st.markdown(_GLOW_WRAP, unsafe_allow_html=True)

    st.markdown(
        '<div style="display:flex;justify-content:center;margin-bottom:1.5rem;position:relative;z-index:1;">'
        '<div style="display:flex;align-items:center;gap:0.5rem;">'
        '<span style="font-size:1.5rem;line-height:1;">&#9674;</span>'
        '<div style="font-weight:700;font-size:1.1rem;letter-spacing:-0.02em;color:white;">OncoLens <span style="color:#5eb3ff;">Clinical</span></div>'
        "</div>"
        "</div>",
        unsafe_allow_html=True,
    )

    left, right = st.columns([1, 1], gap="large")

    with left:
        st.markdown(
            '<p style="font-family:\'Space Grotesk\',sans-serif;font-size:0.72rem;letter-spacing:0.2em;text-transform:uppercase;color:#5eb3ff;margin-bottom:0.5rem;">Clinical intelligence workstation</p>'
            '<h1 style="font-family:Outfit,sans-serif;font-size:clamp(1.75rem,3vw,2.5rem);font-weight:700;letter-spacing:-0.02em;line-height:1.15;margin:0 0 0.5rem;background:linear-gradient(135deg,#fff,#5eb3ff);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">OncoLens Pro</h1>'
            '<p style="font-size:1.05rem;color:#7a9bb8;line-height:1.55;max-width:48ch;margin-bottom:1.5rem;">Enterprise-grade AI diagnostics, patient records, and real-time analytics.</p>',
            unsafe_allow_html=True,
        )
        st.markdown(
            metric_grid(
                [
                    ("Inference", "< 2s"),
                    ("Models", "EffNet"),
                    ("Explain", "Grad-CAM"),
                    ("Auth", "JWT"),
                ]
            ),
            unsafe_allow_html=True,
        )
        st.markdown(
            glass_card(
                """<p style="margin:0 0 0.75rem;font-size:0.88rem;color:var(--ol-muted)">System modules</p>
                <div class="doc-stat-bar"><span style="width:94%"></span></div>
                <p style="margin:0.35rem 0 0.75rem;font-size:0.82rem">Diagnostics pipeline</p>
                <div class="doc-stat-bar"><span style="width:88%"></span></div>
                <p style="margin:0.35rem 0 0.75rem;font-size:0.82rem">Patient records DB</p>
                <div class="doc-stat-bar"><span style="width:96%"></span></div>
                <p style="margin:0.35rem 0;font-size:0.82rem">Report generation</p>""",
                extra_class="glass-card-float",
            ),
            unsafe_allow_html=True,
        )

    with right:
        st.markdown(
            glass_card(
                '<p style="font-family:\'Space Grotesk\',sans-serif;font-size:0.72rem;letter-spacing:0.2em;text-transform:uppercase;color:#5eb3ff;margin-bottom:0.5rem;">Physician access</p>'
                '<h3 style="font-family:Outfit,sans-serif;margin:0 0 0.25rem;color:white;">Clinical sign in</h3>'
                '<p style="color:var(--ol-muted);font-size:0.88rem;margin:0 0 1rem">'
                "Authorized medical staff only</p>",
            ),
            unsafe_allow_html=True,
        )
        with st.form("doc_login_form"):
            email = st.text_input("Institutional email", value="doctor@oncolens.ai")
            password = st.text_input("Password", type="password", value="doctor123")
            submitted = st.form_submit_button("Authenticate", use_container_width=True, type="primary")

        st.caption("Admin: admin@oncolens.ai / admin123")

        if submitted:
            try:
                data = api.login(email, password)
                st.session_state.update(
                    token=data["access_token"],
                    user_email=data["email"],
                    user_role=data["role"],
                    portal_mode="doctor",
                    route="doctor",
                )
                api.token = data["access_token"]
                st.rerun()
            except Exception as exc:
                st.error(f"Authentication failed: {exc}")

        if st.button("← Back to portal"):
            st.session_state["route"] = "portal"
            st.rerun()

        st.markdown(
            '<div style="text-align:center;margin-top:1.5rem;padding-top:1.5rem;border-top:1px solid rgba(255,255,255,0.06);">'
            '<p style="color:#7a9bb8;font-size:0.88rem;">New to OncoLens Clinical?</p>'
            "</div>",
            unsafe_allow_html=True,
        )
        if st.button("Register your practice →", key="go_doc_register", use_container_width=True):
            st.session_state["route"] = "doctor_register"
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    return bool(st.session_state.get("token") and st.session_state.get("portal_mode") == "doctor")
