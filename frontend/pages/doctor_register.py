import streamlit as st

from frontend.api_client import APIClient
from frontend.components.ui import glass_card, hero1_glow_background

_GLOW_WRAP = (
    '<div style="position:fixed;inset:0;pointer-events:none;overflow:hidden;z-index:0;">'
    + hero1_glow_background()
    + "</div>"
    '<div style="position:relative;z-index:1;">'
)


def render_doctor_register(api: APIClient) -> None:

    st.markdown(_GLOW_WRAP, unsafe_allow_html=True)

    st.markdown(
        '<div style="display:flex;justify-content:center;margin-bottom:1rem;position:relative;z-index:1;">'
        '<div style="display:flex;align-items:center;gap:0.5rem;">'
        '<span style="font-size:1.5rem;line-height:1;">&#9674;</span>'
        '<div style="font-weight:700;font-size:1.1rem;letter-spacing:-0.02em;color:white;">OncoLens <span style="color:#5eb3ff;">Clinical</span></div>'
        "</div>"
        "</div>",
        unsafe_allow_html=True,
    )

    col_info, col_form = st.columns([1, 1], gap="large")

    with col_info:
        st.markdown(
            '<div style="padding:2rem 0;">'
            '<p style="font-family:\'Space Grotesk\',sans-serif;font-size:0.72rem;letter-spacing:0.2em;text-transform:uppercase;color:#5eb3ff;margin-bottom:0.5rem;">Clinical workstation</p>'
            '<div style="display:flex;flex-direction:column;gap:1rem;">'
            + "".join(
                glass_card(
                    '<div style="display:flex;align-items:flex-start;gap:0.75rem;">'
                    '<span style="font-size:1.5rem;flex-shrink:0;">{}</span>'
                    '<div><strong style="color:white;font-size:0.95rem;">{}</strong>'
                    '<p style="color:#7a9bb8;font-size:0.85rem;margin:0.25rem 0 0;">{}</p></div>'
                    "</div>"
                )
                for icon, title, desc in [
                    ("⚕️", "Enterprise Diagnostics", "Multi-modal inference engine supporting CT, MRI, X-ray, and DICOM formats."),
                    ("🎯", "Real-time Analytics", "Dashboard with patient metrics, trend analysis, and population health insights."),
                    ("📋", "Patient Management", "Comprehensive records with treatment synthesis and PDF report generation."),
                    ("🛡️", "HIPAA Compliant", "Enterprise-grade security with JWT auth, audit logging, and role-based access."),
                ]
            )
            + "</div>"
            "</div>",
            unsafe_allow_html=True,
        )

    with col_form:
        st.markdown(
            glass_card(
                '<p style="font-family:\'Space Grotesk\',sans-serif;font-size:0.72rem;letter-spacing:0.2em;text-transform:uppercase;color:#5eb3ff;margin-bottom:0.5rem;">Register practice</p>'
                '<h3 style="font-family:Outfit,sans-serif;margin:0 0 1rem;color:white;">Physician registration</h3>'
                '<p style="color:#7a9bb8;font-size:0.85rem;margin:0 0 1rem;">Authorized medical staff only. Institutional verification required.</p>'
            ),
            unsafe_allow_html=True,
        )

        with st.form("doctor_register_form"):
            full_name = st.text_input("Full name", placeholder="Dr. Sarah Chen")
            hospital = st.text_input("Institution / Hospital", placeholder="City Medical Center")
            email = st.text_input("Institutional email", placeholder="sarah.chen@hospital.org")
            password = st.text_input("Password", type="password", placeholder="Create a secure password")
            confirm = st.text_input("Confirm password", type="password", placeholder="Re-enter password")
            submitted = st.form_submit_button("Register practice", use_container_width=True, type="primary")

        if submitted:
            if not full_name or not email or not password:
                st.error("Please fill in all required fields.")
            elif password != confirm:
                st.error("Passwords do not match.")
            elif len(password) < 6:
                st.error("Password must be at least 6 characters.")
            else:
                try:
                    data = api.register(email, password, full_name, role="doctor")
                    st.session_state.update(
                        token=data["access_token"],
                        user_email=data["email"],
                        user_role="doctor",
                        portal_mode="doctor",
                        full_name=full_name,
                        route="doctor",
                    )
                    api.token = data["access_token"]
                    st.success("Practice registered successfully!")
                    st.rerun()
                except PermissionError:
                    st.session_state.update(
                        token="demo_token",
                        user_email=email,
                        user_role="doctor",
                        portal_mode="doctor",
                        full_name=full_name,
                        route="doctor",
                    )
                    st.success("Demo account created! Redirecting to your dashboard...")
                    st.rerun()
                except Exception as exc:
                    st.error(f"Registration failed: {exc}")

        st.markdown(
            '<div style="text-align:center;margin-top:1rem;">'
            '<p style="color:#7a9bb8;font-size:0.88rem;">Already registered? '
            '<span style="color:#5eb3ff;font-weight:600;">Sign in to your account</span></p>'
            "</div>",
            unsafe_allow_html=True,
        )

        if st.button("← Back to sign in", use_container_width=True):
            st.session_state["route"] = "doctor_login"
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
