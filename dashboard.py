"""
Root-level entry point for the OncoLens frontend.

Usage:
    streamlit run dashboard.py

This file sets up sys.path and then runs frontend/dashboard.py so that
both `frontend.*` and `src.*` imports resolve from the project root.
"""
import sys
from pathlib import Path

_root = Path(__file__).resolve().parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

# Streamlit re-executes this file on every interaction, so exec() is safe here.
exec(compile(open(_root / "frontend" / "dashboard.py").read(), "frontend/dashboard.py", "exec"))  # noqa: S102
