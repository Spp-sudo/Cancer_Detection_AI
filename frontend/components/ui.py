"""Reusable HTML UI primitives for Streamlit."""


def glass_card(content: str, extra_class: str = "", floating: bool = False) -> str:
    fc = " glass-card-float" if floating else ""
    return f'<div class="glass-card{fc} {extra_class}">{content}</div>'


def hero(eyebrow: str, title: str, subtitle: str) -> str:
    return f"""
    <p class="ol-eyebrow">{eyebrow}</p>
    <h1 class="ol-display">{title}</h1>
    <p class="ol-subtitle">{subtitle}</p>
    """


def hero1_glow_background() -> str:
    """Gradient glow decoration layers matching Hero1 design."""
    glow_data = [
        ("-40rem", "-30rem", "20rem", "20rem", "20rem"),
        ("-50rem", "-50rem", "20rem", "20rem", "20rem"),
        ("-60rem", "-60rem", "30rem", "30rem", "30rem"),
    ]
    gradients = ""
    for t, r, h1, h2, h3 in glow_data:
        gradients += (
            '<div class="hero-glow-layer" style="display:flex;gap:10rem;'
            'position:absolute;top:{};right:{};z-index:0;'
            'filter:blur(4rem);transform:rotate(-20deg) skew(-40deg);opacity:.5;">'
            '<div style="width:10rem;height:{};background:linear-gradient(90deg,#fff,#93c5fd);"></div>'
            '<div style="width:10rem;height:{};background:linear-gradient(90deg,#fff,#93c5fd);"></div>'
            '<div style="width:10rem;height:{};background:linear-gradient(90deg,#fff,#93c5fd);"></div>'
            "</div>"
        ).format(t, r, h1, h2, h3)
    return gradients


def hero1_html() -> str:
    """OncoLens AI landing hero – Hero1 design language, medical context."""
    feature_pills = "".join(
        '<span style="background:#1c1528;border-radius:999px;padding:0.5rem 1rem;font-size:0.875rem;border:none;color:white;">{}</span>'.format(label)
        for label in [
            "Grad-CAM Explainability",
            "DICOM / Multi-modal",
            "JWT Secure",
            "Treatment Synthesis",
            "Real-time Analytics",
        ]
    )

    return (
        '<div style="min-height:85vh;background:#0c0414;color:white;display:flex;flex-direction:column;position:relative;overflow-x:hidden;font-family:system-ui,-apple-system,sans-serif;">'
        + hero1_glow_background()
        + '<header style="display:flex;justify-content:space-between;align-items:center;padding:1.5rem;position:relative;z-index:1;">'
        '<div style="display:flex;align-items:center;gap:0.5rem;">'
        '<span style="font-size:1.5rem;line-height:1;">&#9674;</span>'
        '<div style="font-weight:700;font-size:1.1rem;letter-spacing:-0.02em;">OncoLens <span style="color:#5eb3ff;">AI</span></div>'
        "</div>"
        "</header>"
        '<main style="flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:0 1rem;text-align:center;position:relative;z-index:1;">'
        '<div style="max-width:56rem;width:100%;margin:0 auto;display:flex;flex-direction:column;gap:1.5rem;">'
        '<div style="display:flex;justify-content:center;">'
        '<div style="background:#1c1528;border-radius:999px;padding:0.5rem 1rem;display:flex;align-items:center;gap:0.5rem;width:fit-content;">'
        '<span style="font-size:0.75rem;display:flex;align-items:center;gap:0.5rem;">'
        '<span style="background:#5eb3ff;padding:0.25rem 0.5rem;border-radius:999px;font-size:0.65rem;font-weight:600;color:black;">AI</span>'
        "Powered Oncology Intelligence"
        "</span>"
        "</div>"
        "</div>"
        '<h1 style="font-size:clamp(2rem,5vw,3.5rem);font-weight:700;line-height:1.1;margin:0;letter-spacing:-0.03em;">Next-generation cancer care<br/>intelligence</h1>'
        '<p style="font-size:1.05rem;margin:0 auto;opacity:.8;max-width:48ch;line-height:1.6;">Deep learning for oncology imaging — Grad-CAM explainability, DICOM support, and clinical-grade inference in a HIPAA-aware architecture.</p>'
        '<div style="display:flex;flex-wrap:wrap;justify-content:center;gap:0.5rem;max-width:42rem;margin:1.5rem auto 0;">'
        + feature_pills
        + "</div>"
        "</div>"
        "</main>"
        "</div>"
    )


def metric_grid(items: list[tuple[str, str]]) -> str:
    cells = "".join(
        f'<div class="metric-tile"><div class="m-label">{label}</div><div class="m-value">{val}</div></div>'
        for label, val in items
    )
    return f'<div class="metric-grid">{cells}</div>'


def feature_step(num: int, title: str, body: str) -> str:
    return f"""
    <div class="step-row">
      <div class="step-num">{num}</div>
      <div><strong style="color:var(--ol-text)">{title}</strong><br/>
      <span style="color:var(--ol-muted);font-size:0.92rem">{body}</span></div>
    </div>
    """


def empty_state(icon: str, title: str, message: str) -> str:
    return glass_card(
        f'<div style="text-align:center;padding:2rem 1rem;">'
        f'<div style="font-size:3rem;margin-bottom:0.75rem;opacity:0.9">{icon}</div>'
        f'<h3 style="margin:0 0 0.5rem;font-family:Outfit,sans-serif">{title}</h3>'
        f'<p style="color:var(--ol-muted);margin:0">{message}</p></div>',
        floating=True,
    )


def skeleton_loader(rows: int = 3) -> str:
    bars = "".join(
        '<div style="height:14px;background:rgba(255,255,255,0.06);border-radius:8px;'
        'margin:10px 0;animation:ol-pulse 1.2s ease infinite;"></div>'
        for _ in range(rows)
    )
    return f"""<style>@keyframes ol-pulse {{ 0%,100%{{opacity:0.4}} 50%{{opacity:0.8}} }}</style>
    <div class="glass-card">{bars}</div>"""


def portal_tile(icon: str, title: str, desc: str, variant: str) -> str:
    return f"""
    <div class="glass-card portal-tile portal-tile-{variant}">
      <div class="portal-icon">{icon}</div>
      <h3 style="font-family:Outfit,sans-serif;margin:0 0 0.5rem;font-size:1.35rem">{title}</h3>
      <p style="color:var(--ol-muted);margin:0;font-size:0.95rem;line-height:1.5">{desc}</p>
    </div>
    """
