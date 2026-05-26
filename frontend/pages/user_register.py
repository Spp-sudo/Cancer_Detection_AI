import streamlit as st

from frontend.api_client import APIClient
from frontend.components.ui import glass_card, hero1_glow_background

_GLOW_WRAP = (
    '<div style="position:fixed;inset:0;pointer-events:none;overflow:hidden;z-index:0;">'
    + hero1_glow_background()
    + "</div>"
    '<div style="position:relative;z-index:1;">'
)


def render_user_register(api: APIClient) -> None:

    st.markdown(_GLOW_WRAP, unsafe_allow_html=True)

    st.markdown(
        '<div style="display:flex;justify-content:center;margin-bottom:1rem;position:relative;z-index:1;">'
        '<div style="display:flex;align-items:center;gap:0.5rem;">'
        '<span style="font-size:1.5rem;line-height:1;">&#9674;</span>'
        '<div style="font-weight:700;font-size:1.1rem;letter-spacing:-0.02em;color:white;">OncoLens <span style="color:#4dffc9;">Patient</span></div>'
        "</div>"
        "</div>",
        unsafe_allow_html=True,
    )

    col_form, col_info = st.columns([1, 1], gap="large")

    with col_form:
        st.markdown(
            glass_card(
                '<p style="font-family:\'Space Grotesk\',sans-serif;font-size:0.72rem;letter-spacing:0.2em;text-transform:uppercase;color:#4dffc9;margin-bottom:0.5rem;">Create account</p>'
                '<h3 style="font-family:Outfit,sans-serif;margin:0 0 1rem;color:white;">Patient registration</h3>'
            ),
            unsafe_allow_html=True,
        )

        with st.form("user_register_form"):
            full_name = st.text_input("Full name", placeholder="Jane Smith")
            email = st.text_input("Email", placeholder="jane@example.com")
            password = st.text_input("Password", type="password", placeholder="Create a secure password")
            confirm = st.text_input("Confirm password", type="password", placeholder="Re-enter password")
            submitted = st.form_submit_button("Create my account", use_container_width=True, type="primary")

        if submitted:
            if not full_name or not email or not password:
                st.error("Please fill in all fields.")
            elif password != confirm:
                st.error("Passwords do not match.")
            elif len(password) < 6:
                st.error("Password must be at least 6 characters.")
            else:
                try:
                    data = api.register(email, password, full_name, role="user")
                    st.session_state.update(
                        token=data["access_token"],
                        user_email=data["email"],
                        user_role="user",
                        portal_mode="user",
                        full_name=full_name,
                        route="user",
                    )
                    api.token = data["access_token"]
                    st.success("Account created successfully!")
                    st.rerun()
                except PermissionError:
                    st.session_state.update(
                        token="demo_token",
                        user_email=email,
                        user_role="user",
                        portal_mode="user",
                        full_name=full_name,
                        route="user",
                    )
                    st.success("Demo account created! Redirecting to your dashboard...")
                    st.rerun()
                except Exception as exc:
                    st.error(f"Registration failed: {exc}")

        st.markdown(
            '<div style="text-align:center;margin-top:1rem;">'
            '<p style="color:#7a9bb8;font-size:0.88rem;">Already have an account? '
            '<a href="#" style="color:#4dffc9;text-decoration:none;font-weight:600;" '
            'onclick="document.querySelector(\'[data-testid=\'stSidebar\']\').style.display=\'none\'">Sign in</a></p>'
            "</div>",
            unsafe_allow_html=True,
        )

        if st.button("← Back to sign in", use_container_width=True):
            st.session_state["route"] = "user_login"
            st.rerun()

    with col_info:
        st.markdown(
            '<div style="padding:2rem 0;">'
            '<p style="font-family:\'Space Grotesk\',sans-serif;font-size:0.72rem;letter-spacing:0.2em;text-transform:uppercase;color:#4dffc9;margin-bottom:0.5rem;">Why join OncoLens?</p>'
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
                    ("🫁", "AI-Powered Analysis", "Advanced deep learning models analyze your medical imaging with clinical-grade accuracy."),
                    ("🔬", "Grad-CAM Explainability", "Understand what the AI focuses on with heatmap visualizations of your scans."),
                    ("🔒", "Secure & Private", "HIPAA-aware architecture with JWT authentication and encrypted data transmission."),
                    ("📊", "Track Progress", "Monitor your health timeline with detailed reports and trend analysis."),
                ]
            )
            + "</div>"
            "</div>",
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)
