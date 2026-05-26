import os
from datetime import datetime, timezone

import streamlit as st

from frontend.api_client import APIClient
from frontend.components.ui import metric_grid


def render_user_sidebar(api: APIClient) -> str:
    st.markdown(
        '<div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.5rem;">'
        '<span style="font-size:1.2rem;line-height:1;">&#9674;</span>'
        '<span style="font-weight:700;font-size:0.95rem;letter-spacing:-0.02em;color:white;">OncoLens <span style="color:#4dffc9;">Patient</span></span>'
        "</div>",
        unsafe_allow_html=True,
    )
    st.divider()
    page = st.radio(
        "Navigate",
        ["Upload Scan", "My Results", "Profile", "Help"],
        label_visibility="collapsed",
        format_func=lambda x: {
            "Upload Scan": "📤 Upload Scan",
            "My Results": "📊 My Results",
            "Profile": "👤 Profile",
            "Help": "💬 Help",
        }.get(x, x),
    )
    _sidebar_footer(api, warm=True)
    return page


def render_doctor_sidebar(api: APIClient) -> str:
    st.markdown(
        '<div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.5rem;">'
        '<span style="font-size:1.2rem;line-height:1;">&#9674;</span>'
        '<span style="font-weight:700;font-size:0.95rem;letter-spacing:-0.02em;color:white;">OncoLens <span style="color:#5eb3ff;">Clinical</span></span>'
        "</div>",
        unsafe_allow_html=True,
    )
    st.divider()
    page = st.radio(
        "Navigate",
        ["Upload Study", "Patient Records", "System", "Profile"],
        label_visibility="collapsed",
        format_func=lambda x: {
            "Upload Study": "📤 Upload Study",
            "Patient Records": "📋 Patient Records",
            "System": "⚙️ System",
            "Profile": "👤 Profile",
        }.get(x, x),
    )
    _sidebar_footer(api, warm=False)
    return page


def _sidebar_footer(api: APIClient, warm: bool) -> None:
    if st.session_state.get("token"):
        st.caption(f"Signed in · {st.session_state.get('user_email', '')}")
        if st.button("Sign out", use_container_width=True, key=f"logout_{warm}"):
            for k in list(st.session_state.keys()):
                if k not in ("api",):
                    st.session_state.pop(k, None)
            api.token = None
            st.session_state["route"] = "portal"
            st.rerun()
    st.divider()
    try:
        h = api.health()
        st.markdown(
            metric_grid(
                [
                    ("API", h.get("status", "—")[:4].upper()),
                    ("Model", (h.get("model_name") or "—")[:10]),
                    ("ML", "OK" if h.get("model_loaded") else "—"),
                ]
            ),
            unsafe_allow_html=True,
        )
    except Exception:
        st.caption("⚠ API offline")
    st.caption(f"UTC {datetime.now(timezone.utc).strftime('%H:%M')}")
    st.caption(os.getenv("ONCOLENS_API_URL", "http://127.0.0.1:8000"))
