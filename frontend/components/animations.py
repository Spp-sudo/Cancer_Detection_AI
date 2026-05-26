"""Animated UI blocks (HTML/CSS only for Streamlit performance)."""


def ai_processing_loader(stage: str = "Analyzing", message: str = "Neural engine active", pct: int = 0) -> str:
    return f"""
    <div class="glass-card" style="text-align:center;padding:2rem 1.5rem;">
      <div class="ai-orbit"></div>
      <p class="ol-eyebrow" style="margin-bottom:0.35rem">AI PROCESSING</p>
      <p style="font-family:Outfit,sans-serif;font-size:1.1rem;color:var(--ol-text);margin:0 0 0.5rem">{stage}</p>
      <p style="color:var(--ol-muted);font-size:0.88rem;margin:0 0 1rem">{message}</p>
      <div style="height:6px;background:rgba(0,0,0,0.3);border-radius:6px;overflow:hidden;max-width:320px;margin:0 auto;">
        <div style="height:100%;width:{pct}%;background:linear-gradient(90deg,var(--ol-accent),#00d4ff);
             border-radius:6px;transition:width 0.4s ease;box-shadow:0 0 12px var(--ol-accent-soft);"></div>
      </div>
      <p style="font-size:0.75rem;color:var(--ol-muted);margin-top:0.5rem">{pct}%</p>
    </div>
    """


def scan_upload_animation() -> str:
    return """
    <div class="upload-aura glass-card" style="margin-bottom:1.25rem;position:relative;z-index:1;">
      <div style="position:relative;z-index:2;">
        <div style="font-size:2.5rem;margin-bottom:0.5rem">🧬</div>
        <p style="font-family:Outfit,sans-serif;font-size:1.05rem;margin:0 0 0.35rem;color:var(--ol-text)">
          Drop your medical scan here
        </p>
        <p style="color:var(--ol-muted);font-size:0.85rem;margin:0">
          CT · MRI · X-Ray · DICOM — encrypted & secure
        </p>
      </div>
    </div>
    """


def result_reveal_banner(classification: str, study_id: str, subtitle: str) -> str:
    is_mal = classification.lower() == "malignant"
    accent = "#ff6b8a" if is_mal else "#4dffc9"
    return f"""
    <div class="glass-card result-reveal" style="border-color:{accent}44;">
      <p class="ol-eyebrow">Analysis Complete</p>
      <h2 style="font-family:Outfit,sans-serif;font-size:1.75rem;margin:0;color:{accent};
          text-shadow:0 0 30px {accent}55">{classification}</h2>
      <p style="color:var(--ol-muted);margin:0.35rem 0 0">{study_id} · {subtitle}</p>
    </div>
    """


def onboarding_steps_user() -> str:
    from frontend.components.ui import feature_step

    steps = [
        (1, "Upload your scan", "Drag & drop imaging files — we support hospital formats."),
        (2, "AI analyzes securely", "Deep learning reviews patterns in seconds."),
        (3, "Understand your results", "Clear explanations, not confusing medical jargon."),
        (4, "Download your report", "EHR-ready PDF summaries for your doctor."),
    ]
    return "".join(feature_step(n, t, b) for n, t, b in steps)
