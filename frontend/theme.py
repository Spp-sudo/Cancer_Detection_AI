"""OncoLens design system — CSS content and HTML helpers."""

FONT_IMPORTS = """
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700&family=Outfit:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
"""

BASE_CSS = """
:root {
  --ol-bg-deep: #0c0414;
  --ol-bg-mid: #0a1628;
  --ol-glass: rgba(12, 28, 48, 0.55);
  --ol-glass-border: rgba(120, 200, 255, 0.18);
  --ol-text: #e8f4fc;
  --ol-muted: #7a9bb8;
  --ol-radius: 16px;
  --ol-shadow: 0 8px 32px rgba(0, 0, 0, 0.35);
  --ol-transition: 0.35s cubic-bezier(0.4, 0, 0.2, 1);
}

html, body, [data-testid="stAppViewContainer"] {
  background: var(--ol-bg-deep) !important;
  color: var(--ol-text) !important;
  font-family: 'DM Sans', sans-serif !important;
}

[data-testid="stHeader"], [data-testid="stToolbar"] { background: transparent !important; }
.block-container {
  padding-top: 1rem !important;
  padding-bottom: 2rem !important;
  max-width: 1320px !important;
  animation: ol-fade-in 0.5s ease;
}

@keyframes ol-fade-in {
  from { opacity: 0; transform: translateY(8px); }
  to { opacity: 1; transform: translateY(0); }
}

.ol-mesh-bg {
  position: fixed; inset: 0; z-index: 0; pointer-events: none; overflow: hidden;
}
.ol-mesh-bg::before, .ol-mesh-bg::after {
  content: ''; position: absolute; border-radius: 50%; filter: blur(80px);
  animation: ol-drift 18s ease-in-out infinite alternate;
}
.ol-mesh-bg::before {
  width: 55vw; height: 55vw; top: -15%; left: -10%;
  background: radial-gradient(circle, rgba(0, 180, 255, 0.12), transparent 70%);
}
.ol-mesh-bg::after {
  width: 45vw; height: 45vw; bottom: -10%; right: -5%;
  background: radial-gradient(circle, rgba(100, 80, 255, 0.1), transparent 70%);
  animation-delay: -6s;
}
@keyframes ol-drift {
  0% { transform: translate(0, 0) scale(1); }
  100% { transform: translate(3%, 4%) scale(1.08); }
}

.glass-card {
  background: var(--ol-glass);
  backdrop-filter: blur(20px) saturate(160%);
  -webkit-backdrop-filter: blur(20px) saturate(160%);
  border: 1px solid var(--ol-glass-border);
  border-radius: var(--ol-radius);
  box-shadow: var(--ol-shadow), inset 0 1px 0 rgba(255,255,255,0.06);
  padding: 1.25rem 1.5rem;
  margin-bottom: 1rem;
  transition: transform var(--ol-transition), box-shadow var(--ol-transition), border-color var(--ol-transition);
  transform-style: preserve-3d;
  perspective: 800px;
}
.glass-card:hover {
  transform: translateY(-3px) rotateX(1deg);
  box-shadow: 0 16px 48px rgba(0, 120, 200, 0.15), inset 0 1px 0 rgba(255,255,255,0.08);
  border-color: rgba(0, 212, 255, 0.35);
}

.glass-card-float { animation: ol-float 6s ease-in-out infinite; }
@keyframes ol-float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-6px); }
}

.ol-display {
  font-family: 'Outfit', sans-serif;
  font-weight: 700;
  font-size: clamp(1.75rem, 4vw, 2.75rem);
  letter-spacing: -0.02em;
  line-height: 1.15;
  margin: 0 0 0.5rem 0;
  background: linear-gradient(135deg, #fff 0%, var(--ol-accent, #5ee7ff) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.ol-subtitle {
  font-size: 1.05rem;
  color: var(--ol-muted);
  line-height: 1.55;
  max-width: 52ch;
  margin-bottom: 1.5rem;
}
.ol-eyebrow {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 0.72rem;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--ol-accent, #00d4ff);
  margin-bottom: 0.5rem;
}

.metric-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
  gap: 12px;
  margin: 1rem 0;
}
.metric-tile {
  background: rgba(0, 0, 0, 0.25);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 12px;
  padding: 14px;
  text-align: center;
  transition: transform 0.25s ease;
}
.metric-tile:hover { transform: scale(1.03); }
.metric-tile .m-label { font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.08em; color: var(--ol-muted); }
.metric-tile .m-value {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 1.4rem;
  font-weight: 600;
  color: var(--ol-accent, #00e6c3);
  margin-top: 4px;
}

.portal-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
  margin: 2rem 0;
}
.portal-tile {
  position: relative;
  padding: 2rem 1.75rem;
  border-radius: 20px;
  cursor: default;
  overflow: hidden;
  min-height: 280px;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
}
.portal-tile::before {
  content: '';
  position: absolute; inset: 0;
  background: linear-gradient(160deg, rgba(255,255,255,0.08), transparent 50%);
  opacity: 0;
  transition: opacity 0.4s ease;
}
.portal-tile:hover::before { opacity: 1; }
.portal-icon { font-size: 2.5rem; margin-bottom: 1rem; filter: drop-shadow(0 0 20px var(--tile-glow)); }

.upload-aura {
  border: 2px dashed rgba(0, 200, 255, 0.35);
  border-radius: 20px;
  padding: 2rem;
  text-align: center;
  background: rgba(0, 40, 70, 0.2);
  position: relative;
  overflow: hidden;
}
.upload-aura::after {
  content: '';
  position: absolute;
  inset: -50%;
  background: conic-gradient(from 0deg, transparent, rgba(0,212,255,0.08), transparent 30%);
  animation: ol-spin-slow 8s linear infinite;
}
@keyframes ol-spin-slow { to { transform: rotate(360deg); } }

.ai-orbit {
  width: 88px; height: 88px; margin: 0 auto 1.25rem;
  border-radius: 50%;
  border: 2px solid rgba(0, 212, 255, 0.15);
  border-top-color: var(--ol-accent, #00d4ff);
  animation: ol-spin 1s linear infinite;
  box-shadow: 0 0 40px rgba(0, 180, 255, 0.25);
}
@keyframes ol-spin { to { transform: rotate(360deg); } }

.result-reveal {
  animation: ol-reveal 0.7s cubic-bezier(0.2, 0.9, 0.3, 1) forwards;
}
@keyframes ol-reveal {
  from { opacity: 0; transform: translateY(24px) scale(0.98); filter: blur(6px); }
  to { opacity: 1; transform: translateY(0) scale(1); filter: blur(0); }
}

.step-row { display: flex; gap: 12px; align-items: flex-start; margin: 12px 0; }
.step-num {
  flex-shrink: 0; width: 28px; height: 28px; border-radius: 50%;
  background: var(--ol-accent-soft, rgba(0,212,255,0.2));
  color: var(--ol-accent, #00d4ff);
  font-weight: 700; font-size: 0.8rem;
  display: flex; align-items: center; justify-content: center;
}

[data-testid="stSidebar"] {
  background: rgba(6, 14, 28, 0.85) !important;
  backdrop-filter: blur(16px) !important;
  border-right: 1px solid var(--ol-glass-border) !important;
}
[data-testid="stSidebar"] * { color: var(--ol-text) !important; }
[data-testid="stFileUploader"] {
  background: rgba(0, 30, 50, 0.35) !important;
  border-radius: 14px !important;
  border: 1px dashed rgba(0, 200, 255, 0.3) !important;
}
.stButton > button {
  border-radius: 12px !important;
  font-family: 'Space Grotesk', sans-serif !important;
  font-weight: 600 !important;
  transition: all 0.25s ease !important;
}
.stButton > button:hover {
  transform: translateY(-1px);
  box-shadow: 0 8px 24px rgba(0, 150, 255, 0.25) !important;
}
div[data-testid="stMetric"] {
  background: rgba(0,0,0,0.2);
  border-radius: 12px;
  padding: 12px;
  border: 1px solid rgba(255,255,255,0.06);
}

.ol-hide-sidebar [data-testid="stSidebar"] { display: none !important; }
.ol-hide-sidebar .block-container { max-width: 100% !important; }

.scan-frame-3d {
  border-radius: 14px;
  padding: 4px;
  background: linear-gradient(135deg, rgba(0,212,255,0.4), rgba(100,80,255,0.2));
  box-shadow: 0 12px 40px rgba(0, 100, 180, 0.2);
  transform: perspective(600px) rotateY(-2deg);
  transition: transform 0.4s ease;
}
.scan-frame-3d:hover { transform: perspective(600px) rotateY(0deg) scale(1.01); }

.treatment-row {
  display: grid; gap: 6px; padding: 12px 14px; margin: 6px 0;
  background: rgba(0,0,0,0.2); border-radius: 10px;
  border-left: 3px solid var(--ol-accent, #00d4ff);
  font-size: 0.9rem;
}
@media (min-width: 900px) {
  .treatment-row { grid-template-columns: 1.1fr 0.8fr 0.7fr 1.5fr; }
}
@media (max-width: 768px) {
  .block-container { padding-left: 1rem !important; padding-right: 1rem !important; }
  .portal-grid { grid-template-columns: 1fr; }
  .metric-grid { grid-template-columns: repeat(2, 1fr); }
}
"""

USER_THEME = """
:root, [data-portal="user"] {
  --ol-accent: #4dffc9;
  --ol-accent-soft: rgba(77, 255, 201, 0.15);
  --ol-accent-warm: #ffb86b;
  --tile-user-bg: linear-gradient(145deg, rgba(20, 60, 55, 0.6), rgba(10, 30, 45, 0.8));
  --tile-glow: rgba(77, 255, 201, 0.4);
}
.portal-tile-user {
  background: var(--tile-user-bg);
  border: 1px solid rgba(77, 255, 201, 0.25);
}
.feature-pill {
  display: inline-block; padding: 6px 14px; margin: 4px 6px 4px 0;
  border-radius: 999px; font-size: 0.82rem;
  background: rgba(77, 255, 201, 0.12);
  border: 1px solid rgba(77, 255, 201, 0.25);
  color: #b8ffe8;
}
"""

DOCTOR_THEME = """
:root, [data-portal="doctor"] {
  --ol-accent: #5eb3ff;
  --ol-accent-soft: rgba(94, 179, 255, 0.12);
  --ol-accent-secondary: #8b9dc3;
  --tile-doc-bg: linear-gradient(145deg, rgba(15, 35, 65, 0.75), rgba(8, 18, 35, 0.9));
  --tile-glow: rgba(94, 179, 255, 0.35);
}
.portal-tile-doctor {
  background: var(--tile-doc-bg);
  border: 1px solid rgba(94, 179, 255, 0.22);
}
.doc-stat-bar {
  height: 4px; border-radius: 4px; background: rgba(255,255,255,0.08); overflow: hidden;
}
.doc-stat-bar > span {
  display: block; height: 100%;
  background: linear-gradient(90deg, #5eb3ff, #00d4ff);
  border-radius: 4px;
  animation: ol-bar-grow 1s ease forwards;
}
@keyframes ol-bar-grow { from { width: 0; } }
"""


def get_css_content() -> str:
    """Raw CSS only (no HTML wrappers)."""
    return FONT_IMPORTS + BASE_CSS + USER_THEME + DOCTOR_THEME


def mesh_background_html() -> str:
    return '<div class="ol-mesh-bg" aria-hidden="true"></div>'


def portal_shell_html(portal: str | None = "doctor") -> str:
    """Non-style HTML shell for portal attribute and sidebar visibility."""
    hide = "ol-hide-sidebar" if portal in (None, "portal", "user_login", "doctor_login") else ""
    portal_attr = portal or "doctor"
    return f'<div data-portal="{portal_attr}" class="ol-portal-root {hide}"></div>'
