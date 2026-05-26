import plotly.graph_objects as go

_CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(6, 14, 28, 0.85)",
    font=dict(color="#a8c8e0", family="DM Sans", size=11),
    margin=dict(l=44, r=16, t=48, b=40),
    height=300,
)


def _accent(portal: str) -> str:
    return "#4dffc9" if portal == "user" else "#5eb3ff"


def malignancy_chart(chart_data: dict, portal: str = "doctor") -> go.Figure:
    accent = _accent(portal)
    vec = chart_data.get("malignancy_vector", {})
    weeks = vec.get("timepoints_weeks", [])
    idx = vec.get("malignancy_index", [])
    upper = vec.get("confidence_band_upper", [])
    lower = vec.get("confidence_band_lower", [])
    fig = go.Figure()
    if upper and lower:
        fig.add_trace(
            go.Scatter(
                x=weeks + weeks[::-1],
                y=upper + lower[::-1],
                fill="toself",
                fillcolor=f"rgba({77 if portal=='user' else 94}, {255 if portal=='user' else 179}, {201 if portal=='user' else 255}, 0.08)",
                line=dict(color="rgba(0,0,0,0)"),
                hoverinfo="skip",
            )
        )
    fig.add_trace(
        go.Scatter(
            x=weeks,
            y=idx,
            mode="lines+markers",
            line=dict(color=accent, width=2.5, shape="spline"),
            marker=dict(size=7, color="#fff", line=dict(width=1.5, color=accent)),
            name="Risk trajectory",
        )
    )
    title = "Your Health Trend" if portal == "user" else "Malignancy Vector — Temporal"
    fig.update_layout(
        title=dict(text=title, font=dict(size=13, color=accent)),
        xaxis=dict(title="Weeks", gridcolor="rgba(255,255,255,0.06)", zeroline=False),
        yaxis=dict(title="Index", gridcolor="rgba(255,255,255,0.06)", range=[0, 1]),
        showlegend=False,
        **_CHART_LAYOUT,
    )
    return fig


def subtype_chart(chart_data: dict, portal: str = "doctor") -> go.Figure:
    accent = _accent(portal)
    sub = chart_data.get("subtype_accuracy", {})
    labels = sub.get("subtypes", [])
    values = sub.get("accuracy_pct", [])
    fig = go.Figure(
        go.Bar(
            x=labels,
            y=values,
            marker=dict(
                color=values,
                colorscale=[[0, "#0a1a2e"], [0.5, accent], [1, "#00ffcc" if portal == "user" else "#5eb3ff"]],
                line=dict(color=accent, width=0.5),
            ),
            text=[f"{v:.0f}%" for v in values],
            textposition="outside",
            textfont=dict(size=9, color="#c8e0f0"),
        )
    )
    title = "AI Confidence by Type" if portal == "user" else "Accuracy by Molecular Subtype"
    fig.update_layout(
        title=dict(text=title, font=dict(size=13, color=accent)),
        xaxis=dict(tickangle=-22, gridcolor="rgba(255,255,255,0.04)"),
        yaxis=dict(range=[80, 100], title="Accuracy %", gridcolor="rgba(255,255,255,0.06)"),
        **_CHART_LAYOUT,
    )
    return fig
