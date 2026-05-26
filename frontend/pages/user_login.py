import streamlit as st

from frontend.api_client import APIClient
from frontend.components.ui import glass_card, hero1_glow_background

_GLOW_WRAP = (
    '<div style="position:fixed;inset:0;pointer-events:none;overflow:hidden;z-index:0;">'
    + hero1_glow_background()
    + "</div>"
    '<div style="position:relative;z-index:1;">'
)


def render_user_login(api: APIClient) -> bool:

    st.markdown(_GLOW_WRAP, unsafe_allow_html=True)

    st.markdown(
        '<div style="display:flex;justify-content:center;margin-bottom:1.5rem;position:relative;z-index:1;">'
        '<div style="display:flex;align-items:center;gap:0.5rem;">'
        '<span style="font-size:1.5rem;line-height:1;">&#9674;</span>'
        '<div style="font-weight:700;font-size:1.1rem;letter-spacing:-0.02em;color:white;">OncoLens <span style="color:#4dffc9;">Patient</span></div>'
        "</div>"
        "</div>",
        unsafe_allow_html=True,
    )

    col_story, col_form = st.columns([1.1, 0.9], gap="large")

    with col_story:
        st.markdown(
            '<p style="font-family:\'Space Grotesk\',sans-serif;font-size:0.72rem;letter-spacing:0.2em;text-transform:uppercase;color:#4dffc9;margin-bottom:0.5rem;">Your health companion</p>'
            '<h1 style="font-family:Outfit,sans-serif;font-size:clamp(1.75rem,3vw,2.5rem);font-weight:700;letter-spacing:-0.02em;line-height:1.15;margin:0 0 0.5rem;background:linear-gradient(135deg,#fff,#4dffc9);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">Welcome to OncoLens</h1>'
            '<p style="font-size:1.05rem;color:#7a9bb8;line-height:1.55;max-width:48ch;margin-bottom:1.5rem;">We help you understand medical imaging with AI — calmly, clearly, and securely.</p>',
            unsafe_allow_html=True,
        )
        st.markdown(
            glass_card(
                '<span class="feature-pill">📤 Upload your scan</span>'
                '<span class="feature-pill">📈 Track your health</span>'
                '<span class="feature-pill">🤖 AI-powered analysis</span>'
                '<span class="feature-pill">🔒 Secure medical reports</span>',
                floating=True,
            ),
            unsafe_allow_html=True,
        )
        st.markdown("#### How it works")
        st.markdown(
            glass_card(
                "<p style='margin:0;color:var(--ol-muted);font-size:0.9rem'>"
                "💬 <strong style='color:#4dffc9'>AI Assistant:</strong> "
                "Think of OncoLens as a translator between complex scans and what they mean for you. "
                "Always share results with your physician.</p>"
            ),
            unsafe_allow_html=True,
        )

    with col_form:
        st.markdown(
            glass_card(
                '<p style="font-family:\'Space Grotesk\',sans-serif;font-size:0.72rem;letter-spacing:0.2em;text-transform:uppercase;color:#4dffc9;margin-bottom:0.5rem;">Patient sign in</p>'
                '<h3 style="font-family:Outfit,sans-serif;margin:0 0 1rem;color:white;">Access your dashboard</h3>',
            ),
            unsafe_allow_html=True,
        )
        with st.form("user_login_form"):
            email = st.text_input("Email", value="doctor@oncolens.ai", help="Demo uses clinical API account")
            password = st.text_input("Password", type="password", value="doctor123")
            submitted = st.form_submit_button("Continue to my dashboard", use_container_width=True, type="primary")

        if st.button("🚀 Quick demo (no typing)", use_container_width=True):
            try:
                data = api.login("doctor@oncolens.ai", "doctor123")
                st.session_state.update(
                    token=data["access_token"],
                    user_email=data["email"],
                    user_role=data["role"],
                    portal_mode="user",
                    route="user",
                )
                api.token = data["access_token"]
                st.rerun()
            except Exception as exc:
                st.error(f"Demo login failed: {exc}")

        if submitted:
            try:
                data = api.login(email, password)
                st.session_state.update(
                    token=data["access_token"],
                    user_email=data["email"],
                    user_role=data["role"],
                    portal_mode="user",
                    route="user",
                )
                api.token = data["access_token"]
                st.rerun()
            except Exception as exc:
                st.error(f"Could not sign in: {exc}")

        if st.button("← Back to portal selection"):
            st.session_state["route"] = "portal"
            st.rerun()

        st.markdown(
            '<div style="text-align:center;margin-top:1.5rem;padding-top:1.5rem;border-top:1px solid rgba(255,255,255,0.06);">'
            '<p style="color:#7a9bb8;font-size:0.88rem;">Don\'t have an account?</p>'
            "</div>",
            unsafe_allow_html=True,
        )
        if st.button("Create patient account →", key="go_user_register", use_container_width=True):
            st.session_state["route"] = "user_register"
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    return bool(st.session_state.get("token") and st.session_state.get("portal_mode") == "user")
