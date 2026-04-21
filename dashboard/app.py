from __future__ import annotations

import sys
from pathlib import Path

import joblib
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.inference.service import IDSInferenceService  # noqa: E402
from src.utils.config import load_config  # noqa: E402

st.set_page_config(
    page_title="Intrusion Detection Platform",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

config = load_config(PROJECT_ROOT / "configs" / "default.yaml")
artifact_path = PROJECT_ROOT / config["paths"]["artifacts_dir"] / "model_bundle.joblib"
service = IDSInferenceService(
    artifact_path=artifact_path,
    drift_threshold=config["monitoring"]["drift_threshold"],
)
artifacts = joblib.load(artifact_path) if artifact_path.exists() else None

PALETTE = {
    "bg": "#07111f",
    "panel": "#0f1b2d",
    "panel_alt": "#12233a",
    "border": "rgba(123, 170, 255, 0.14)",
    "text": "#ecf3ff",
    "muted": "#8fa4c4",
    "accent": "#00c2a8",
    "warning": "#ffb84d",
    "danger": "#ff6b6b",
    "normal": "#3aa0ff",
    "attack": "#ff6b6b",
}

st.markdown(
    f"""
    <style>
    .stApp {{
        background:
            radial-gradient(circle at top left, rgba(0,194,168,0.12), transparent 28%),
            radial-gradient(circle at top right, rgba(58,160,255,0.12), transparent 24%),
            linear-gradient(180deg, #050b15 0%, {PALETTE["bg"]} 100%);
        color: {PALETTE["text"]};
    }}
    .block-container {{
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1350px;
    }}
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #091321 0%, #0c1628 100%);
        border-right: 1px solid {PALETTE["border"]};
    }}
    [data-testid="stMetricValue"] {{
        color: {PALETTE["text"]};
    }}
    .hero {{
        padding: 1.75rem 1.75rem 1.25rem 1.75rem;
        border-radius: 24px;
        border: 1px solid {PALETTE["border"]};
        background:
            linear-gradient(135deg, rgba(15,27,45,0.96), rgba(10,18,32,0.92)),
            linear-gradient(180deg, rgba(255,255,255,0.04), rgba(255,255,255,0.00));
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.25);
        margin-bottom: 1.25rem;
    }}
    .hero-kicker {{
        color: {PALETTE["accent"]};
        font-size: 0.8rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.18em;
        margin-bottom: 0.7rem;
    }}
    .hero-title {{
        font-size: 2.4rem;
        font-weight: 800;
        line-height: 1.05;
        margin: 0 0 0.55rem 0;
        color: {PALETTE["text"]};
    }}
    .hero-copy {{
        color: #b6c6df;
        font-size: 1rem;
        max-width: 850px;
        margin-bottom: 0;
    }}
    .section-label {{
        color: {PALETTE["muted"]};
        text-transform: uppercase;
        letter-spacing: 0.12em;
        font-size: 0.76rem;
        font-weight: 700;
        margin: 0.2rem 0 0.75rem 0;
    }}
    .panel {{
        background: linear-gradient(180deg, {PALETTE["panel"]} 0%, {PALETTE["panel_alt"]} 100%);
        border: 1px solid {PALETTE["border"]};
        border-radius: 22px;
        padding: 1rem 1rem 0.75rem 1rem;
        box-shadow: 0 14px 44px rgba(0, 0, 0, 0.16);
    }}
    .metric-card {{
        padding: 1rem 1rem 0.85rem 1rem;
        border-radius: 18px;
        background: linear-gradient(180deg, rgba(255,255,255,0.04), rgba(255,255,255,0.015));
        border: 1px solid {PALETTE["border"]};
        min-height: 118px;
    }}
    .metric-label {{
        color: {PALETTE["muted"]};
        font-size: 0.82rem;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        margin-bottom: 0.6rem;
    }}
    .metric-value {{
        color: {PALETTE["text"]};
        font-size: 2rem;
        font-weight: 800;
        line-height: 1;
        margin-bottom: 0.5rem;
    }}
    .metric-note {{
        color: #b6c6df;
        font-size: 0.88rem;
    }}
    .pill {{
        display: inline-block;
        padding: 0.25rem 0.65rem;
        border-radius: 999px;
        font-size: 0.78rem;
        font-weight: 700;
        margin-right: 0.45rem;
    }}
    .pill-normal {{
        color: #caecff;
        background: rgba(58,160,255,0.18);
    }}
    .pill-attack {{
        color: #ffd3d3;
        background: rgba(255,107,107,0.18);
    }}
    .pill-warning {{
        color: #ffe8be;
        background: rgba(255,184,77,0.18);
    }}
    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div,
    .stFileUploader > div > div {{
        background: rgba(255,255,255,0.02);
        border-color: {PALETTE["border"]};
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


def render_metric_card(label: str, value: str, note: str) -> None:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def style_plotly(fig: go.Figure) -> go.Figure:
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=PALETTE["text"]),
        margin=dict(l=18, r=18, t=56, b=18),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor="rgba(0,0,0,0)",
        ),
    )
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(gridcolor="rgba(255,255,255,0.08)", zeroline=False)
    return fig


def render_empty_state() -> None:
    st.markdown('<div class="section-label">Operator Workflow</div>', unsafe_allow_html=True)
    st.info(
        "Upload a CSV with KDD-style network traffic fields to score records, visualize attack volume, "
        "and inspect confidence and drift in a single view."
    )

    if artifacts is None:
        st.warning("No trained model bundle found yet. Run the training pipeline to unlock leaderboard and SHAP insights.")


def get_results_frame(uploaded_file) -> pd.DataFrame | None:
    if uploaded_file is None:
        return None
    source_df = pd.read_csv(uploaded_file)
    predictions = service.predict_records(source_df.to_dict("records"))
    results = pd.concat([source_df.reset_index(drop=True), pd.DataFrame(predictions)], axis=1)
    results["risk_band"] = pd.cut(
        results["probability"],
        bins=[-0.01, 0.4, 0.7, 1.0],
        labels=["Low", "Elevated", "Critical"],
    )
    return results


with st.sidebar:
    st.markdown("## Console Controls")
    st.caption("Analyst-facing controls for triage and dashboard density.")
    uploaded_file = st.file_uploader("Traffic CSV", type=["csv"], help="Upload a batch of network telemetry records.")
    confidence_threshold = st.slider("Highlight threshold", 0.0, 1.0, 0.7, 0.05)
    show_only_attacks = st.toggle("Show attacks only", value=False)
    compact_table = st.toggle("Compact result table", value=True)

    st.markdown("---")
    st.markdown("### Platform Status")
    st.markdown(
        """
        <span class="pill pill-normal">API Ready</span>
        <span class="pill pill-warning">Drift Watch</span>
        """,
        unsafe_allow_html=True,
    )
    st.caption(
        "The dashboard uses the shared inference layer, so API and UI stay aligned on thresholds, labels, and drift logic."
    )


st.markdown(
    """
    <div class="hero">
        <div class="hero-kicker">Security Operations Dashboard</div>
        <h1 class="hero-title">Intrusion Detection Command Center</h1>
        <p class="hero-copy">
            Review suspicious traffic, compare model behavior, and surface attack signals with a cleaner operational view.
            The dashboard is optimized for batch triage today and can grow into a real-time SOC display tomorrow.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

results_df = get_results_frame(uploaded_file)
display_df = results_df.copy() if results_df is not None else None
if display_df is not None and show_only_attacks:
    display_df = display_df[display_df["prediction"] == "attack"].reset_index(drop=True)

summary_cols = st.columns(4)
with summary_cols[0]:
    render_metric_card(
        "Traffic Records",
        str(len(display_df)) if display_df is not None else "0",
        "Records currently in the analyst view",
    )
with summary_cols[1]:
    attack_count = int((display_df["prediction"] == "attack").sum()) if display_df is not None else 0
    render_metric_card(
        "Attack Alerts",
        str(attack_count),
        "Predictions flagged as malicious",
    )
with summary_cols[2]:
    avg_conf = float(display_df["probability"].mean()) if display_df is not None and not display_df.empty else 0.0
    render_metric_card(
        "Avg Confidence",
        f"{avg_conf:.2%}",
        "Average confidence across visible records",
    )
with summary_cols[3]:
    drift_score = float(display_df["drift_score"].iloc[0]) if display_df is not None and not display_df.empty else 0.0
    drift_flag = "Investigate distribution shift" if drift_score >= config["monitoring"]["drift_threshold"] else "Within baseline tolerance"
    render_metric_card(
        "Drift Score",
        f"{drift_score:.2f}",
        drift_flag,
    )

overview_col, model_col = st.columns([1.45, 1], gap="large")

with overview_col:
    st.markdown('<div class="section-label">Triage Overview</div>', unsafe_allow_html=True)
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    if display_df is None or display_df.empty:
        render_empty_state()
    else:
        attack_counts = (
            display_df["prediction"]
            .value_counts()
            .rename_axis("prediction")
            .reset_index(name="count")
        )
        attack_fig = px.bar(
            attack_counts,
            x="prediction",
            y="count",
            color="prediction",
            color_discrete_map={"normal": PALETTE["normal"], "attack": PALETTE["attack"]},
            title="Traffic Classification Mix",
        )
        st.plotly_chart(style_plotly(attack_fig), use_container_width=True)

        left_chart, right_chart = st.columns(2)
        with left_chart:
            confidence_fig = px.histogram(
                display_df,
                x="probability",
                color="prediction",
                nbins=24,
                title="Confidence Distribution",
                color_discrete_map={"normal": PALETTE["normal"], "attack": PALETTE["attack"]},
            )
            confidence_fig.add_vline(
                x=confidence_threshold,
                line_dash="dash",
                line_color=PALETTE["warning"],
                annotation_text="Highlight threshold",
            )
            st.plotly_chart(style_plotly(confidence_fig), use_container_width=True)

        with right_chart:
            risk_counts = (
                display_df["risk_band"]
                .astype(str)
                .value_counts()
                .rename_axis("risk_band")
                .reset_index(name="count")
            )
            risk_fig = px.pie(
                risk_counts,
                names="risk_band",
                values="count",
                hole=0.62,
                title="Risk Band Breakdown",
                color="risk_band",
                color_discrete_map={
                    "Low": PALETTE["normal"],
                    "Elevated": PALETTE["warning"],
                    "Critical": PALETTE["attack"],
                },
            )
            risk_fig.update_traces(textposition="inside", textinfo="percent+label")
            st.plotly_chart(style_plotly(risk_fig), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with model_col:
    st.markdown('<div class="section-label">Model Intelligence</div>', unsafe_allow_html=True)
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    if artifacts is None:
        st.info("Train the model bundle to unlock leaderboard rankings and explainability highlights.")
    else:
        leaderboard_df = pd.DataFrame(artifacts["model_report"]).sort_values("roc_auc", ascending=False)
        st.dataframe(
            leaderboard_df[["model", "cv_roc_auc", "roc_auc"]],
            use_container_width=True,
            hide_index=True,
        )
        st.markdown("#### Top Explainability Signals")
        shap_df = pd.DataFrame(artifacts["shap_importance"]).head(8).sort_values("importance")
        shap_fig = px.bar(
            shap_df,
            x="importance",
            y="feature",
            orientation="h",
            color="importance",
            color_continuous_scale=["#1d4e89", "#00c2a8"],
            title="Most Influential Features",
        )
        shap_fig.update_layout(coloraxis_showscale=False)
        st.plotly_chart(style_plotly(shap_fig), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

if display_df is not None and not display_df.empty:
    st.markdown('<div class="section-label">Analyst Review</div>', unsafe_allow_html=True)
    review_tab, queue_tab, feature_tab = st.tabs(["Results", "Priority Queue", "Feature Snapshot"])

    with review_tab:
        table_df = display_df.sort_values("probability", ascending=False).reset_index(drop=True)
        if compact_table:
            preferred_columns = [
                "prediction",
                "probability",
                "risk_band",
                "drift_score",
                "protocol_type",
                "service",
                "flag",
                "src_bytes",
                "dst_bytes",
                "count",
            ]
            available_columns = [column for column in preferred_columns if column in table_df.columns]
            table_df = table_df[available_columns]
        st.dataframe(
            table_df.style.format({"probability": "{:.2%}", "drift_score": "{:.2f}"}),
            use_container_width=True,
            hide_index=True,
        )

    with queue_tab:
        queue_df = display_df[display_df["probability"] >= confidence_threshold].copy()
        queue_df = queue_df.sort_values("probability", ascending=False).reset_index(drop=True)
        high_priority = int((queue_df["prediction"] == "attack").sum())
        st.markdown(
            f"""
            <span class="pill pill-attack">Priority records: {len(queue_df)}</span>
            <span class="pill pill-warning">Attack-heavy queue: {high_priority}</span>
            """,
            unsafe_allow_html=True,
        )
        if queue_df.empty:
            st.success("No records currently exceed the analyst highlight threshold.")
        else:
            queue_columns = [
                column
                for column in ["prediction", "probability", "protocol_type", "service", "flag", "src_bytes", "dst_bytes"]
                if column in queue_df.columns
            ]
            st.dataframe(
                queue_df[queue_columns].style.format({"probability": "{:.2%}"}),
                use_container_width=True,
                hide_index=True,
            )

    with feature_tab:
        numeric_candidates = [
            column for column in ["src_bytes", "dst_bytes", "count", "srv_count", "dst_host_count"] if column in display_df.columns
        ]
        if len(numeric_candidates) >= 2:
            scatter_fig = px.scatter(
                display_df,
                x=numeric_candidates[0],
                y=numeric_candidates[1],
                color="prediction",
                size="probability",
                title="Traffic Pattern Cluster",
                color_discrete_map={"normal": PALETTE["normal"], "attack": PALETTE["attack"]},
                hover_data=["service", "flag"] if {"service", "flag"}.issubset(display_df.columns) else None,
            )
            st.plotly_chart(style_plotly(scatter_fig), use_container_width=True)
        else:
            st.info("The uploaded file does not include enough numeric fields for the feature scatter view.")
else:
    st.markdown('<div class="section-label">Analyst Review</div>', unsafe_allow_html=True)
    st.info("Upload traffic data from the sidebar to activate the detailed triage views.")
