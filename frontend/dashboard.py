"""
OncoLens AI — Premium dual-portal Streamlit application.
"""
import sys
from pathlib import Path

# Ensure the project root (parent of this file's directory) is on sys.path
# so that both `frontend.*` and `src.*` imports resolve correctly regardless
# of which directory Streamlit is launched from.
_project_root = Path(__file__).resolve().parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

import streamlit as st

from frontend.api_client import APIClient
from frontend.components.layout import render_doctor_sidebar, render_user_sidebar
from frontend.pages.doctor_login import render_doctor_login
from frontend.pages.doctor_register import render_doctor_register
from frontend.pages.doctor_workspace import render_doctor_app
from frontend.pages.portal import render_portal
from frontend.pages.user_home import render_user_app
from frontend.pages.user_login import render_user_login
from frontend.pages.user_register import render_user_register
from frontend.theme import get_css_content, mesh_background_html, portal_shell_html

# ---------------------------------------------------------------------------
# Global stylesheet — single valid <style> block (never inject CSS as raw text)
# ---------------------------------------------------------------------------
custom_css_string = f"""<style>
{get_css_content()}
</style>
"""

st.set_page_config(
    page_title="OncoLens AI",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="auto",
)

st.markdown(custom_css_string, unsafe_allow_html=True)


def _render_portal_shell(portal: str | None) -> None:
    """Decorative layers only; styles are applied via custom_css_string above."""
    st.markdown(mesh_background_html(), unsafe_allow_html=True)
    st.markdown(portal_shell_html(portal), unsafe_allow_html=True)


# Session defaults
for key, default in (
    ("api", None),
    ("route", "portal"),
    ("portal_mode", None),
    ("token", None),
):
    if key not in st.session_state:
        st.session_state[key] = default

if st.session_state.api is None:
    st.session_state.api = APIClient()
api: APIClient = st.session_state.api
if st.session_state.get("token"):
    api.token = st.session_state["token"]

route = st.session_state.get("route", "portal")

# Routes without sidebar
if route == "portal":
    _render_portal_shell("portal")
    render_portal()
    st.stop()

if route == "user_login":
    _render_portal_shell("user_login")
    render_user_login(api)
    st.stop()

if route == "user_register":
    _render_portal_shell("user_register")
    render_user_register(api)
    st.stop()

if route == "doctor_register":
    _render_portal_shell("doctor_register")
    render_doctor_register(api)
    st.stop()

if route == "doctor_login":
    _render_portal_shell("doctor_login")
    render_doctor_login(api)
    st.stop()

# Authenticated app routes
if not st.session_state.get("token"):
    st.session_state["route"] = "portal"
    st.rerun()

portal_mode = st.session_state.get("portal_mode", "doctor")
_render_portal_shell(portal_mode)

with st.sidebar:
    if portal_mode == "user":
        page = render_user_sidebar(api)
    else:
        page = render_doctor_sidebar(api)

    if st.button("⇄ Switch portal", use_container_width=True):
        for k in ("token", "user_email", "user_role", "portal_mode", "result", "filename", "image_bytes"):
            st.session_state.pop(k, None)
        api.token = None
        st.session_state["route"] = "portal"
        st.rerun()

if portal_mode == "user":
    render_user_app(api, page)
else:
    render_doctor_app(api, page)
