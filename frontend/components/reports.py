import json
from datetime import datetime, timezone


def ehr_text(result: dict, filename: str, note: str) -> str:
    cm = result.get("confidence_metrics", {})
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    lines = [
        f"  - {a.get('medicine')}: {a.get('dosage')} — {a.get('purpose')}"
        for a in result.get("treatment_protocol", [])
    ]
    return f"""ONCOLENS AI — EHR CLINICAL REPORT
Study ID: {result.get('study_id')} | Generated: {ts}
File: {filename} | Modality: {result.get('modality')} | Model: {result.get('model_name')}
Classification: {result.get('classification')} | Subtype: {result.get('molecular_subtype')}

Confidence: primary {cm.get('primary_confidence', 0)*100:.1f}% | benign {cm.get('benign_probability', 0)*100:.1f}% | malignant {cm.get('malignancy_probability', 0)*100:.1f}%
Processing: {result.get('processing_time_ms', 0):.0f} ms

Treatment:
{chr(10).join(lines)}

Breakdown: {json.dumps(result.get('disease_breakdown', {}))}
Notes: {note or 'N/A'}

Disclaimer: AI decision-support only. Physician review required.
"""


def treatment_card_html(protocol: list[dict], breakdown: dict[str, float]) -> str:
    cells = "".join(
        f'<div class="metric-cell"><div class="label">{k.replace("_"," ")}</div>'
        f'<div class="value">{v*100:.0f}%</div></div>'
        for k, v in breakdown.items()
    )
    rows = "".join(
        f'<div class="treatment-row"><strong>{a.get("medicine")}</strong>'
        f'<span>{a.get("dosage")}</span><span>{a.get("route")} · {a.get("cycle")}</span>'
        f'<span>{a.get("purpose")}</span></div>'
        for a in protocol
    )
    return (
        f'<div class="glass-card"><h4 style="font-family:Outfit,sans-serif;color:var(--ol-accent)">'
        f"Disease Breakdown</h4><div class=\"metric-grid\">{cells}</div>"
        f'<h4 style="margin-top:1rem;font-family:Outfit,sans-serif;color:var(--ol-accent)">'
        f"Medicine Regimen</h4>{rows}</div>"
    )
