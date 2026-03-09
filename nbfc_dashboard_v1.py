# ── NBFC Dashboard v1 ─────────────────────────────────────────────────────────
# Streamlit dashboard for 9 Indian NBFCs
# Run: streamlit run nbfc_dashboard_v1.py

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta, date as _date
from datetime import datetime as _dt
from concurrent.futures import ThreadPoolExecutor
import numpy as _np
import yfinance as yf
import pytz

from nbfc_data_cache import NBFC_TIMESERIES, QUARTERS as CACHE_QUARTERS, METRIC_LABELS
from nbfc_ai_data import NBFC_AI_INITIATIVES, FUNCTION_TAXONOMY
from shareholding_data import SHAREHOLDING, SH_QUARTERS, CATEGORY_COLORS, ENTITY_CATEGORY_COLORS, ENTITY_BADGE_TEXT_COLORS

st.set_page_config(
    page_title="NBFC Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── GLOBAL CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600;700&display=swap" rel="stylesheet">
<style>
* { font-family: 'Inter', sans-serif; }
.main { background: #eef0f4; }
.block-container { padding: 2.8rem 1.6rem 0.6rem 1.6rem !important; max-width: 1600px !important; }
.section-label { font-size: 12px; font-weight: 700; text-transform: uppercase; color: #64748b; border-left: 2px solid #0284c7; padding-left: 7px; margin-bottom: 4px; }
.section-label-sub { font-size: 10.5px; font-weight: 400; color: #94a3b8; }
.tab-intro { background: white; border-left: 4px solid #0284c7; padding: 12px 18px; border-radius: 5px; margin-bottom: 16px; }
.tab-intro-title { font-size: 17px; font-weight: 700; color: #0a2540; }
.tab-intro-sub { font-size: 12.5px; color: #94a3b8; }
.metric-note { background: #f8fafc; border-radius: 4px; padding: 6px 12px; border-left: 2px solid #cbd5e1; font-size: 10.5px; color: #64748b; margin-top: 8px; }
.stTabs [data-baseweb="tab-list"] { background: white; border-bottom: 1px solid #e2e8f0; gap: 0; }
.stTabs [data-baseweb="tab"] { color: #64748b; font-size: 13px; font-weight: 500; padding: 10px 18px; border-bottom: 2px solid transparent; }
.stTabs [aria-selected="true"] { color: #0284c7 !important; border-bottom: 2px solid #0284c7 !important; font-weight: 600; }
.ticker-card { background: white; border-radius: 5px; padding: 12px 14px 10px 14px; border-top: 3px solid #0284c7; box-shadow: 0 1px 3px rgba(0,0,0,0.07); height: 112px; }
.ticker-name-sm { font-size: 17px; font-weight: 600; color: #0a2540; line-height: 1.2; }
.ticker-sym { font-family: 'JetBrains Mono', monospace; font-size: 10px; color: #94a3b8; }
.ticker-price { font-family: 'JetBrains Mono', monospace; font-size: 24px; font-weight: 700; color: #0a2540; }
.ticker-pos { color: #16a34a; font-size: 14px; font-weight: 600; }
.ticker-neg { color: #dc2626; font-size: 14px; font-weight: 600; }
.ticker-meta { font-family: 'JetBrains Mono', monospace; font-size: 10px; color: #94a3b8; }
.stButton button { background: white !important; border: 1px solid #e2e8f0 !important; color: #64748b !important; border-radius: 4px !important; padding: 3px 10px !important; height: 28px !important; font-size: 11.5px !important; }
.rank-table { border-collapse: collapse; width: 100%; font-size: 12px; }
.rank-table th { background: #0a2540; color: white; padding: 8px 10px; text-align: right; font-size: 10.5px; }
.rank-table th:first-child { text-align: left; }
.rank-table td { padding: 7px 10px; border-bottom: 1px solid #f1f5f9; text-align: right; }
.rank-table td:first-child { text-align: left; font-weight: 600; color: #0a2540; }
.ai-row-card { background: white; border-radius: 6px; padding: 14px 18px; margin-bottom: 10px; border-left: 4px solid var(--nbfc-color); }
.ai-row-title { font-size: 14px; font-weight: 700; color: #0a2540; margin-bottom: 6px; }
.ai-row-desc { font-size: 12px; color: #374151; line-height: 1.65; margin-top: 6px; }
.ai-impact { font-size: 12px; color: #0a2540; font-weight: 500; background: #f0f9ff; border-left: 3px solid #0284c7; padding: 7px 12px; margin-bottom: 6px; }
.ai-func-tag { display: inline-block; font-size: 10px; font-weight: 600; color: #0284c7; background: #e0f2fe; border-radius: 10px; padding: 2px 9px; }
.ai-nbfc-badge { display: inline-block; font-size: 10.5px; font-weight: 700; color: white; border-radius: 4px; padding: 2px 9px; }
.ai-date-badge { font-family: 'JetBrains Mono', monospace; font-size: 10.5px; color: #64748b; background: #f1f5f9; padding: 2px 8px; border-radius: 3px; }
.ai-source-link { font-size: 11px; color: #0284c7; text-decoration: none; }
.sh-table { border-collapse: collapse; width: 100%; font-size: 12px; }
.sh-table th { background: #0a2540; color: white; padding: 7px 10px; font-size: 10.5px; }
.sh-table td { padding: 6px 10px; border-bottom: 1px solid #f1f5f9; font-family: 'JetBrains Mono', monospace; font-size: 11.5px; }
.sh-td-name { text-align: left; font-family: 'Inter', sans-serif !important; font-size: 12px; font-weight: 600; color: #0a2540; max-width: 200px; }
.sh-cat-badge { display: inline-block; font-size: 10px; font-weight: 700; border-radius: 10px; padding: 2px 9px; }
.sh-cell-up { color: #16a34a; }
.sh-cell-dn { color: #dc2626; }
.sh-cell-flat { color: #64748b; }
.sh-cell-nil { color: #cbd5e1; }
.sh-entry-dot { color: #16a34a; font-size: 9px; vertical-align: super; }
.sh-exit-dot { color: #dc2626; font-size: 9px; vertical-align: super; }
.sh-summary-card { background: white; border-radius: 5px; padding: 14px 18px; border-top: 3px solid #0284c7; }
.sh-summary-num { font-family: 'JetBrains Mono', monospace; font-size: 24px; font-weight: 700; color: #0a2540; }
.sh-summary-label { font-size: 10px; font-weight: 600; color: #94a3b8; text-transform: uppercase; }
.sh-summary-delta { font-size: 11px; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# ── NBFC REGISTRY ──────────────────────────────────────────────────────────────
NBFCS = {
    'Poonawalla Fincorp':    'POONAWALLA.NS',
    'Bajaj Finance':         'BAJFINANCE.NS',
    'Shriram Finance':       'SHRIRAMFIN.NS',
    'L&T Finance':           'LTF.NS',
    'Cholamandalam Finance': 'CHOLAFIN.NS',
    'Aditya Birla Capital':  'ABCAPITAL.NS',
    'Piramal Finance':       'PIRAMALFIN.NS',
    'Muthoot Finance':       'MUTHOOTFIN.NS',
    'Mahindra Finance':      'M&MFIN.NS',
}

CACHE_KEY = {
    'Poonawalla Fincorp':    'Poonawalla Fincorp',
    'Bajaj Finance':         'Bajaj Finance',
    'Shriram Finance':       'Shriram Finance',
    'L&T Finance':           'L&T Finance',
    'Cholamandalam Finance': 'Chola Finance',
    'Aditya Birla Capital':  'Aditya Birla Capital',
    'Piramal Finance':       'Piramal Finance',
    'Muthoot Finance':       'Muthoot Finance',
    'Mahindra Finance':      'Mahindra Finance',
}

COLORS = {
    'Poonawalla Fincorp':    '#0284c7',
    'Bajaj Finance':         '#f97316',
    'Shriram Finance':       '#10b981',
    'L&T Finance':           '#8b5cf6',
    'Cholamandalam Finance': '#ef4444',
    'Aditya Birla Capital':  '#0891b2',
    'Piramal Finance':       '#be123c',
    'Muthoot Finance':       '#65a30d',
    'Mahindra Finance':      '#7c3aed',
}

DISPLAY_NAMES = list(NBFCS.keys())
DEFAULT_COMPARISON = ['Bajaj Finance', 'Shriram Finance', 'L&T Finance']
Q_LABELS = CACHE_QUARTERS  # ["Q4FY24", "Q1FY25", ..., "Q3FY26"]

# ── DATA HELPERS ───────────────────────────────────────────────────────────────
def get_series(metric: str) -> dict:
    """Returns {display_name: [8 values aligned to Q_LABELS]}."""
    out = {}
    for disp in DISPLAY_NAMES:
        cache = CACHE_KEY[disp]
        out[disp] = NBFC_TIMESERIES[cache][metric]
    return out

def latest_val(series_list):
    """Return last non-None value and its index."""
    for i in range(len(series_list) - 1, -1, -1):
        if series_list[i] is not None:
            return series_list[i], i
    return None, -1


# ── CHART FACTORIES ────────────────────────────────────────────────────────────

def _fmt_val(v, fmt):
    """Format a value according to fmt string."""
    if v is None:
        return "—"
    if fmt == 'pct':
        return f"{v:.2f}%"
    elif fmt == 'cr':
        return f"₹{v:,.0f} Cr"
    elif fmt == 'ratio':
        return f"{v:.2f}x"
    elif fmt == 'inr':
        return f"₹{v:.1f}"
    elif fmt == 'bvps':
        return f"₹{v:,.0f}"
    return str(v)


def make_trend_chart(metric, selected, title, ylabel, fmt='pct', note=None, height=420, lower_is_better=False):
    """Line chart for a single metric across selected NBFCs over 8 quarters."""
    data = get_series(metric)

    # Collect series and sort by last value descending
    series_info = []
    for name in selected:
        vals = data[name]
        lv, li = latest_val(vals)
        if lv is not None:
            series_info.append((name, vals, lv, li))
        else:
            series_info.append((name, vals, -1e9, -1))

    if lower_is_better:
        series_info.sort(key=lambda x: x[2])
    else:
        series_info.sort(key=lambda x: -x[2])

    fig = go.Figure()

    for name, vals, lv, li in series_info:
        color = COLORS[name]
        x_vals = list(range(len(Q_LABELS)))
        y_vals = vals
        hover_text = []
        for i, v in enumerate(y_vals):
            if v is not None:
                hover_text.append(_fmt_val(v, fmt))
            else:
                hover_text.append("—")

        fig.add_trace(go.Scatter(
            x=x_vals,
            y=y_vals,
            name=name,
            mode='lines+markers',
            line=dict(color=color, width=2),
            marker=dict(color=color, size=6),
            connectgaps=False,
            hovertemplate=f"<b>{name}</b><br>%{{x}}<br>{ylabel}: %{{customdata}}<extra></extra>",
            customdata=hover_text,
        ))

    # Collect annotation points
    ann_points = []
    for name, vals, lv, li in series_info:
        if lv is not None and lv != -1e9:
            ann_points.append((name, li, lv))

    # Stagger annotations
    if ann_points:
        all_y = [v for _, vals, _, _ in series_info for v in vals if v is not None]
        if all_y:
            y_min, y_max = min(all_y), max(all_y)
            y_range = y_max - y_min if y_max != y_min else 1.0
        else:
            y_range = 1.0
        GAP = max(y_range * 0.11, 0.2)

        ann_points_sorted = sorted(ann_points, key=lambda x: -x[2])
        label_positions = []
        for name, xi, yv in ann_points_sorted:
            pos = yv
            for prev_pos in label_positions:
                if abs(pos - prev_pos) < GAP:
                    pos = prev_pos - GAP
            label_positions.append(pos)

        for idx, (name, xi, yv) in enumerate(ann_points_sorted):
            label_y = label_positions[idx]
            color = COLORS[name]
            label_text = f"<b>{name}</b>  {_fmt_val(yv, fmt)}"
            fig.add_annotation(
                x=len(Q_LABELS) - 1,
                y=label_y,
                text=label_text,
                showarrow=False,
                xanchor='left',
                xshift=12,
                font=dict(size=10.5, color='#0a2540'),
                bgcolor='white',
                bordercolor=color,
                borderwidth=1,
                borderpad=3,
            )
            if abs(label_y - yv) > GAP * 0.3:
                fig.add_shape(
                    type='line',
                    x0=len(Q_LABELS) - 1,
                    x1=len(Q_LABELS) - 1,
                    y0=yv,
                    y1=label_y,
                    line=dict(color=color, width=0.8, dash='dot'),
                )

    title_html = f'<b style="color:#0a2540;font-size:15px;">{title}</b>'
    if note:
        title_html += f'<br><span style="color:#94a3b8;font-size:10px;">{note}</span>'

    fig.update_layout(
        template='plotly_white',
        height=height,
        hovermode='x unified',
        showlegend=False,
        margin=dict(l=55, r=230, t=55, b=45),
        title=dict(text=title_html, x=0, xref='paper', font=dict(family='Inter')),
        xaxis=dict(
            tickmode='array',
            tickvals=list(range(len(Q_LABELS))),
            ticktext=Q_LABELS,
            showgrid=True,
            gridcolor='#f1f5f9',
            showline=True,
            linecolor='#cbd5e1',
            tickangle=0,
        ),
        yaxis=dict(
            title=dict(text=ylabel, font=dict(size=11, color='#64748b')),
            showgrid=True,
            gridcolor='#f1f5f9',
            showline=True,
            linecolor='#cbd5e1',
        ),
        font=dict(family='Inter'),
    )

    return fig


def make_bar_chart(metric, selected, title, ylabel, fmt='cr', height=380):
    """Grouped bar chart for AUM and PAT."""
    data = get_series(metric)
    fig = go.Figure()

    for name in selected:
        vals = data[name]
        color = COLORS[name]
        x_vals = list(range(len(Q_LABELS)))
        fig.add_trace(go.Bar(
            x=x_vals,
            y=vals,
            name=name,
            marker_color=color,
            opacity=0.85,
            hovertemplate=f"<b>{name}</b><br>%{{x}}<br>{ylabel}: %{{y:,.0f}}<extra></extra>",
        ))

    title_html = f'<b style="color:#0a2540;font-size:15px;">{title}</b>'

    fig.update_layout(
        template='plotly_white',
        height=height,
        barmode='group',
        showlegend=True,
        legend=dict(orientation='h', y=-0.18, x=0.5, xanchor='center', font=dict(size=10)),
        margin=dict(l=55, r=20, t=55, b=90),
        title=dict(text=title_html, x=0, xref='paper', font=dict(family='Inter')),
        xaxis=dict(
            tickmode='array',
            tickvals=list(range(len(Q_LABELS))),
            ticktext=Q_LABELS,
            range=[-0.5, len(Q_LABELS) - 0.5],
            showgrid=True,
            gridcolor='#f1f5f9',
            showline=True,
            linecolor='#cbd5e1',
        ),
        yaxis=dict(
            title=dict(text=ylabel, font=dict(size=11, color='#64748b')),
            showgrid=True,
            gridcolor='#f1f5f9',
            showline=True,
            linecolor='#cbd5e1',
        ),
        font=dict(family='Inter'),
    )

    return fig


def make_yoy_chart(metric, selected, title, height=310):
    """YoY growth line chart for last 4 quarters."""
    data = get_series(metric)
    YOY_LABELS = ["Q4FY25", "Q1FY26", "Q2FY26", "Q3FY26"]
    YOY_PAIRS = [(4, 0), (5, 1), (6, 2), (7, 3)]

    series_info = []
    for name in selected:
        vals = data[name]
        growth = []
        for cur_idx, py_idx in YOY_PAIRS:
            cur = vals[cur_idx] if cur_idx < len(vals) else None
            py = vals[py_idx] if py_idx < len(vals) else None
            if cur is None or py is None:
                growth.append(None)
            elif py <= 0:
                growth.append(0.0)
            else:
                growth.append((cur - py) / py * 100)
        last_g = None
        for g in reversed(growth):
            if g is not None:
                last_g = g
                break
        series_info.append((name, growth, last_g if last_g is not None else -1e9))

    series_info.sort(key=lambda x: -x[2])

    fig = go.Figure()
    for name, growth, _ in series_info:
        color = COLORS[name]
        x_vals = list(range(len(YOY_LABELS)))
        fig.add_trace(go.Scatter(
            x=x_vals,
            y=growth,
            name=name,
            mode='lines+markers',
            line=dict(color=color, width=2),
            marker=dict(color=color, size=6),
            connectgaps=False,
            hovertemplate=f"<b>{name}</b><br>YoY: %{{y:.1f}}%<extra></extra>",
        ))

    all_g = [g for _, glist, _ in series_info for g in glist if g is not None]
    if all_g:
        y_min, y_max = min(all_g), max(all_g)
        y_range = y_max - y_min if y_max != y_min else 1.0
    else:
        y_range = 1.0
    GAP = max(y_range * 0.14, 2.0)

    ann_points = []
    for name, growth, _ in series_info:
        last_g = None
        for g in reversed(growth):
            if g is not None:
                last_g = g
                break
        if last_g is not None:
            ann_points.append((name, last_g))

    ann_points_sorted = sorted(ann_points, key=lambda x: -x[1])
    label_positions = []
    for name, yv in ann_points_sorted:
        pos = yv
        for prev_pos in label_positions:
            if abs(pos - prev_pos) < GAP:
                pos = prev_pos - GAP
        label_positions.append(pos)

    for idx, (name, yv) in enumerate(ann_points_sorted):
        label_y = label_positions[idx]
        color = COLORS[name]
        fig.add_annotation(
            x=len(YOY_LABELS) - 1,
            y=label_y,
            text=f"<b>{name}</b>  {yv:.1f}%",
            showarrow=False,
            xanchor='left',
            xshift=10,
            font=dict(size=9.5, color='#0a2540'),
            bgcolor='white',
            bordercolor=color,
            borderwidth=1,
            borderpad=2,
        )
        if abs(label_y - yv) > GAP * 0.3:
            fig.add_shape(
                type='line',
                x0=len(YOY_LABELS) - 1,
                x1=len(YOY_LABELS) - 1,
                y0=yv,
                y1=label_y,
                line=dict(color=color, width=0.8, dash='dot'),
            )

    fig.add_hline(y=0, line=dict(color='#94a3b8', width=1, dash='dot'))

    title_html = f'<b style="color:#0a2540;font-size:13px;">YoY Growth — {title}</b>'
    fig.update_layout(
        template='plotly_white',
        height=height,
        hovermode='x unified',
        showlegend=False,
        margin=dict(l=55, r=155, t=55, b=45),
        title=dict(text=title_html, x=0, xref='paper', font=dict(family='Inter')),
        xaxis=dict(
            tickmode='array',
            tickvals=list(range(len(YOY_LABELS))),
            ticktext=YOY_LABELS,
            showgrid=True,
            gridcolor='#f1f5f9',
            showline=True,
            linecolor='#cbd5e1',
        ),
        yaxis=dict(
            ticksuffix='%',
            showgrid=True,
            gridcolor='#f1f5f9',
            showline=True,
            linecolor='#cbd5e1',
        ),
        font=dict(family='Inter'),
    )
    return fig


def make_qoq_chart(metric, selected, title, height=310):
    """QoQ growth line chart for Q1FY25 through Q3FY26."""
    data = get_series(metric)
    QOQ_LABELS = ["Q1FY25", "Q2FY25", "Q3FY25", "Q4FY25", "Q1FY26", "Q2FY26", "Q3FY26"]
    QOQ_PAIRS = [(1, 0), (2, 1), (3, 2), (4, 3), (5, 4), (6, 5), (7, 6)]

    series_info = []
    for name in selected:
        vals = data[name]
        growth = []
        for cur_idx, prev_idx in QOQ_PAIRS:
            cur = vals[cur_idx] if cur_idx < len(vals) else None
            prev = vals[prev_idx] if prev_idx < len(vals) else None
            if cur is None or prev is None:
                growth.append(None)
            elif prev <= 0:
                growth.append(0.0)
            else:
                growth.append((cur - prev) / prev * 100)
        last_g = None
        for g in reversed(growth):
            if g is not None:
                last_g = g
                break
        series_info.append((name, growth, last_g if last_g is not None else -1e9))

    series_info.sort(key=lambda x: -x[2])

    fig = go.Figure()
    for name, growth, _ in series_info:
        color = COLORS[name]
        x_vals = list(range(len(QOQ_LABELS)))
        fig.add_trace(go.Scatter(
            x=x_vals,
            y=growth,
            name=name,
            mode='lines+markers',
            line=dict(color=color, width=2),
            marker=dict(color=color, size=6),
            connectgaps=False,
            hovertemplate=f"<b>{name}</b><br>QoQ: %{{y:.1f}}%<extra></extra>",
        ))

    all_g = [g for _, glist, _ in series_info for g in glist if g is not None]
    if all_g:
        y_min, y_max = min(all_g), max(all_g)
        y_range = y_max - y_min if y_max != y_min else 1.0
    else:
        y_range = 1.0
    GAP = max(y_range * 0.14, 1.5)

    ann_points = []
    for name, growth, _ in series_info:
        last_g = None
        for g in reversed(growth):
            if g is not None:
                last_g = g
                break
        if last_g is not None:
            ann_points.append((name, last_g))

    ann_points_sorted = sorted(ann_points, key=lambda x: -x[1])
    label_positions = []
    for name, yv in ann_points_sorted:
        pos = yv
        for prev_pos in label_positions:
            if abs(pos - prev_pos) < GAP:
                pos = prev_pos - GAP
        label_positions.append(pos)

    for idx, (name, yv) in enumerate(ann_points_sorted):
        label_y = label_positions[idx]
        color = COLORS[name]
        fig.add_annotation(
            x=len(QOQ_LABELS) - 1,
            y=label_y,
            text=f"<b>{name}</b>  {yv:.1f}%",
            showarrow=False,
            xanchor='left',
            xshift=10,
            font=dict(size=9.5, color='#0a2540'),
            bgcolor='white',
            bordercolor=color,
            borderwidth=1,
            borderpad=2,
        )
        if abs(label_y - yv) > GAP * 0.3:
            fig.add_shape(
                type='line',
                x0=len(QOQ_LABELS) - 1,
                x1=len(QOQ_LABELS) - 1,
                y0=yv,
                y1=label_y,
                line=dict(color=color, width=0.8, dash='dot'),
            )

    fig.add_hline(y=0, line=dict(color='#94a3b8', width=1, dash='dot'))

    title_html = f'<b style="color:#0a2540;font-size:13px;">QoQ Growth — {title}</b>'
    fig.update_layout(
        template='plotly_white',
        height=height,
        hovermode='x unified',
        showlegend=False,
        margin=dict(l=55, r=155, t=55, b=45),
        title=dict(text=title_html, x=0, xref='paper', font=dict(family='Inter')),
        xaxis=dict(
            tickmode='array',
            tickvals=list(range(len(QOQ_LABELS))),
            ticktext=QOQ_LABELS,
            showgrid=True,
            gridcolor='#f1f5f9',
            showline=True,
            linecolor='#cbd5e1',
        ),
        yaxis=dict(
            ticksuffix='%',
            showgrid=True,
            gridcolor='#f1f5f9',
            showline=True,
            linecolor='#cbd5e1',
        ),
        font=dict(family='Inter'),
    )
    return fig


def make_pb_chart(selected, height=520):
    """Daily P/B ratio chart over 2 years."""
    QUARTER_ENDS = [
        (_date(2024, 3, 31), 0),
        (_date(2024, 6, 30), 1),
        (_date(2024, 9, 30), 2),
        (_date(2024, 12, 31), 3),
        (_date(2025, 3, 31), 4),
        (_date(2025, 6, 30), 5),
        (_date(2025, 9, 30), 6),
        (_date(2025, 12, 31), 7),
    ]

    fig = go.Figure()
    series_info = []

    for name in selected:
        symbol = NBFCS[name]
        cache_name = CACHE_KEY[name]
        bvps_series = NBFC_TIMESERIES[cache_name].get('bvps_inr', [None] * 8)
        hist = fetch_stock_data(symbol, period='2y')
        if hist is None or len(hist) == 0:
            continue

        hist = hist.copy()
        hist.index = hist.index.tz_localize(None) if hist.index.tzinfo is not None else hist.index

        dates = []
        pb_vals = []
        prices = []
        bvps_vals = []

        for dt_idx, row in hist.iterrows():
            dt_date = dt_idx.date() if hasattr(dt_idx, 'date') else dt_idx
            # Find most recent quarter end <= date
            best_q_idx = None
            for qe_date, q_idx in QUARTER_ENDS:
                if qe_date <= dt_date:
                    best_q_idx = q_idx
                else:
                    break
            if best_q_idx is None:
                continue
            bvps = bvps_series[best_q_idx] if best_q_idx < len(bvps_series) else None
            if bvps is None or bvps <= 0:
                continue
            price = float(row['Close'])
            pb = price / bvps
            dates.append(dt_idx)
            pb_vals.append(pb)
            prices.append(price)
            bvps_vals.append(bvps)

        if not dates:
            continue

        custom_data = _np.column_stack([prices, bvps_vals])

        color = COLORS[name]
        lv = pb_vals[-1]
        series_info.append((name, lv))

        fig.add_trace(go.Scatter(
            x=dates,
            y=pb_vals,
            name=name,
            mode='lines',
            line=dict(color=color, width=2),
            customdata=custom_data,
            hovertemplate=(
                f"<b>{name}</b><br>"
                "%{x|%d %b %Y}<br>"
                "P/B: %{y:.2f}x · Price: ₹%{customdata[0]:,.0f} · BVPS: ₹%{customdata[1]:,.0f}"
                "<extra></extra>"
            ),
        ))

    if series_info:
        all_pb = []
        for trace in fig.data:
            all_pb.extend([v for v in trace.y if v is not None])
        if all_pb:
            y_min, y_max = min(all_pb), max(all_pb)
            y_range = y_max - y_min if y_max != y_min else 1.0
        else:
            y_range = 1.0
        GAP = max(y_range * 0.08, 0.12)

        series_info_sorted = sorted(series_info, key=lambda x: -x[1])
        label_positions = []
        for name, yv in series_info_sorted:
            pos = yv
            for prev_pos in label_positions:
                if abs(pos - prev_pos) < GAP:
                    pos = prev_pos - GAP
            label_positions.append(pos)

        for idx, (name, yv) in enumerate(series_info_sorted):
            label_y = label_positions[idx]
            color = COLORS[name]
            fig.add_annotation(
                x=1.0,
                y=label_y,
                xref='paper',
                yref='y',
                text=f"<b>{name}</b>  {yv:.2f}x",
                showarrow=False,
                xanchor='left',
                xshift=8,
                font=dict(size=10, color='#0a2540'),
                bgcolor='white',
                bordercolor=color,
                borderwidth=1,
                borderpad=3,
            )
            if abs(label_y - yv) > GAP * 0.3:
                fig.add_shape(
                    type='line',
                    x0=1.0,
                    x1=1.0,
                    y0=yv,
                    y1=label_y,
                    xref='paper',
                    yref='y',
                    line=dict(color=color, width=0.8, dash='dot'),
                )

    fig.add_hline(y=1, line=dict(color='#94a3b8', width=1, dash='dot'))

    fig.update_layout(
        template='plotly_white',
        height=height,
        hovermode='x unified',
        showlegend=False,
        margin=dict(l=55, r=200, t=55, b=45),
        title=dict(
            text='<b style="color:#0a2540;font-size:15px;">Price-to-Book (P/B) Ratio — 2Y Daily</b>',
            x=0, xref='paper', font=dict(family='Inter')
        ),
        xaxis=dict(
            showgrid=True,
            gridcolor='#f1f5f9',
            showline=True,
            linecolor='#cbd5e1',
        ),
        yaxis=dict(
            ticksuffix='x',
            showgrid=True,
            gridcolor='#f1f5f9',
            showline=True,
            linecolor='#cbd5e1',
        ),
        font=dict(family='Inter'),
    )
    return fig


def make_mktcap_trend_chart(selected, height=440):
    """1-year daily market cap trend."""
    shares_dict = fetch_shares_outstanding()
    fig = go.Figure()
    series_info = []

    for name in selected:
        symbol = NBFCS[name]
        shares = shares_dict.get(symbol)
        if not shares:
            continue
        hist = fetch_stock_data(symbol, period='1y')
        if hist is None or len(hist) == 0:
            continue

        hist = hist.copy()
        hist.index = hist.index.tz_localize(None) if hist.index.tzinfo is not None else hist.index

        mktcap = hist['Close'] * shares / 1e12  # ₹ Lakh Crore (1 L.Cr = 1 Trillion)

        color = COLORS[name]
        lv = float(mktcap.iloc[-1]) if len(mktcap) > 0 else 0
        series_info.append((name, lv))

        fig.add_trace(go.Scatter(
            x=mktcap.index,
            y=mktcap.values,
            name=name,
            mode='lines',
            line=dict(color=color, width=2),
            hovertemplate=f"<b>{name}</b><br>%{{x|%d %b %Y}}<br>MCap: ₹%{{y:.2f}} L.Cr<extra></extra>",
        ))

        # Endpoint dot
        fig.add_trace(go.Scatter(
            x=[mktcap.index[-1]],
            y=[lv],
            mode='markers',
            marker=dict(color=color, size=7),
            showlegend=False,
            hoverinfo='skip',
        ))

    if series_info:
        all_mc = []
        for trace in fig.data:
            if trace.mode and 'lines' in trace.mode:
                all_mc.extend([v for v in trace.y if v is not None])
        if all_mc:
            y_min, y_max = min(all_mc), max(all_mc)
            y_range = y_max - y_min if y_max != y_min else 1.0
        else:
            y_range = 1.0
        GAP = max(y_range * 0.08, 0.02)

        series_info_sorted = sorted(series_info, key=lambda x: -x[1])
        label_positions = []
        for name, yv in series_info_sorted:
            pos = yv
            for prev_pos in label_positions:
                if abs(pos - prev_pos) < GAP:
                    pos = prev_pos - GAP
            label_positions.append(pos)

        for idx, (name, yv) in enumerate(series_info_sorted):
            label_y = label_positions[idx]
            color = COLORS[name]
            fig.add_annotation(
                x=1.0,
                y=label_y,
                xref='paper',
                yref='y',
                text=f"<b>{name}</b>  ₹{yv:.2f} L.Cr",
                showarrow=False,
                xanchor='left',
                xshift=8,
                font=dict(size=10, color='#0a2540'),
                bgcolor='white',
                bordercolor=color,
                borderwidth=1,
                borderpad=3,
            )

    fig.update_layout(
        template='plotly_white',
        height=height,
        hovermode='x unified',
        showlegend=False,
        margin=dict(l=60, r=230, t=55, b=40),
        title=dict(
            text='<b style="color:#0a2540;font-size:15px;">Market Capitalisation — 1 Year · Daily NSE price × current shares outstanding</b>',
            x=0, xref='paper', font=dict(family='Inter')
        ),
        xaxis=dict(
            showgrid=True,
            gridcolor='#f1f5f9',
            showline=True,
            linecolor='#cbd5e1',
        ),
        yaxis=dict(
            title=dict(text='₹ Lakh Crore', font=dict(size=11, color='#64748b')),
            ticksuffix=' L.Cr',
            showgrid=True,
            gridcolor='#f1f5f9',
            showline=True,
            linecolor='#cbd5e1',
        ),
        paper_bgcolor='white',
        font=dict(family='Inter'),
    )
    return fig


def build_rankings_table():
    """Plotly Table for Tab 8."""
    METRICS = [
        ('aum_cr', 'AUM (₹ Cr)', 'cr', False),
        ('pat_cr', 'PAT (₹ Cr)', 'cr', False),
        ('gnpa_pct', 'GNPA %', 'pct', True),
        ('nnpa_pct', 'NNPA %', 'pct', True),
        ('nim_pct', 'NIM %', 'pct', False),
        ('roa_pct', 'ROA %', 'pct', False),
        ('roe_pct', 'ROE %', 'pct', False),
        ('cost_of_borrowing_pct', 'CoB %', 'pct', True),
        ('d_e_ratio', 'D/E', 'ratio', True),
        ('car_pct', 'CAR %', 'pct', False),
        ('bvps_inr', 'BVPS (₹)', 'bvps', False),
    ]
    Q_IDX = 7

    def _fmt_cell(v, fmt):
        if v is None:
            return "—"
        if fmt == 'cr':
            return f"₹{int(v):,}"
        elif fmt == 'pct':
            return f"{v:.2f}%"
        elif fmt == 'ratio':
            return f"{v:.2f}x"
        elif fmt == 'bvps':
            return f"₹{int(v):,}"
        return str(v)

    def _parse_num(s):
        if s == "—":
            return None
        try:
            return float(s.replace('₹', '').replace(',', '').replace('%', '').replace('x', ''))
        except:
            return None

    def color_col(col_values, lower_is_better):
        nums = [_parse_num(v) for v in col_values]
        valid = [n for n in nums if n is not None]
        if not valid:
            return ['rgba(241,245,249,0.5)'] * len(col_values)
        mn, mx = min(valid), max(valid)
        colors = []
        for n in nums:
            if n is None:
                colors.append('rgba(241,245,249,0.5)')
                continue
            if mx == mn:
                colors.append('rgba(248,250,252,0.7)')
                continue
            t = (n - mn) / (mx - mn)
            if lower_is_better:
                t = 1.0 - t
            if t <= 0.5:
                s = t * 2
                r = int(220 + s * (255 - 220))
                g = int(60 + s * (215 - 60))
                b = int(60 + s * (50 - 60))
            else:
                s = (t - 0.5) * 2
                r = int(255 + s * (60 - 255))
                g = int(215 + s * (190 - 215))
                b = int(50 + s * (80 - 50))
            colors.append(f'rgba({r},{g},{b},0.35)')
        return colors

    # Build table data
    nbfc_names = DISPLAY_NAMES
    header_vals = ['NBFC'] + [m[1] for m in METRICS]

    rows = {}
    for name in nbfc_names:
        cache = CACHE_KEY[name]
        row = []
        for metric, label, fmt, lib in METRICS:
            vals = NBFC_TIMESERIES[cache].get(metric, [None] * 8)
            v = vals[Q_IDX] if Q_IDX < len(vals) else None
            row.append(_fmt_cell(v, fmt))
        rows[name] = row

    cell_vals = [nbfc_names]
    cell_colors = [['rgba(240,249,255,0.6)'] * len(nbfc_names)]

    for i, (metric, label, fmt, lib) in enumerate(METRICS):
        col = [rows[name][i] for name in nbfc_names]
        cell_vals.append(col)
        cell_colors.append(color_col(col, lib))

    fig = go.Figure(data=[go.Table(
        columnwidth=[160] + [80] * len(METRICS),
        header=dict(
            values=header_vals,
            fill_color='#0a2540',
            font=dict(color='white', family='Inter', size=11),
            align=['left'] + ['right'] * len(METRICS),
            height=34,
        ),
        cells=dict(
            values=cell_vals,
            fill_color=cell_colors,
            font=dict(color='#1a3a52', family='Inter', size=11.5),
            align=['left'] + ['right'] * len(METRICS),
            height=30,
        ),
    )])

    fig.update_layout(
        margin=dict(l=0, r=0, t=10, b=0),
        height=380,
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter'),
    )
    return fig


def make_deep_dive(nbfc_disp):
    """5×3 subplot grid for one NBFC (14 metrics)."""
    metrics_grid = [
        ('aum_cr', 'AUM (₹ Cr)', 'cr'),
        ('pat_cr', 'PAT (₹ Cr)', 'cr'),
        ('gnpa_pct', 'GNPA %', 'pct'),
        ('nnpa_pct', 'NNPA %', 'pct'),
        ('pcr_pct', 'PCR %', 'pct'),
        ('nim_pct', 'NIM %', 'pct'),
        ('roa_pct', 'ROA %', 'pct'),
        ('roe_pct', 'ROE %', 'pct'),
        ('cost_of_borrowing_pct', 'Cost of Borrowing %', 'pct'),
        ('d_e_ratio', 'D/E Ratio', 'ratio'),
        ('car_pct', 'CAR %', 'pct'),
        ('bvps_inr', 'BVPS (₹)', 'bvps'),
        ('t1_pct', 'Tier 1 Capital %', 'pct'),
        ('t2_pct', 'Tier 2 Capital %', 'pct'),
    ]

    def _fmt(v, fmt):
        if v is None:
            return "—"
        if fmt == 'cr':
            if abs(v) >= 1e5:
                return f"₹{v/1e5:.1f}L Cr"
            elif abs(v) >= 1e3:
                return f"₹{v/1e3:.0f}K Cr"
            else:
                return f"₹{v:.0f} Cr"
        elif fmt == 'pct':
            return f"{v:.1f}%"
        elif fmt == 'ratio':
            return f"{v:.2f}x"
        elif fmt == 'bvps':
            return f"₹{v:,.0f}"
        return str(v)

    subplot_titles = [m[1] for m in metrics_grid] + ['', '']

    fig = make_subplots(
        rows=5, cols=3,
        subplot_titles=subplot_titles,
        vertical_spacing=0.10,
        horizontal_spacing=0.07,
    )

    cache_name = CACHE_KEY[nbfc_disp]
    color = COLORS[nbfc_disp]
    x_vals = list(range(len(Q_LABELS)))

    callout_annotations = []

    for idx, (metric, label, fmt) in enumerate(metrics_grid):
        row = idx // 3 + 1
        col = idx % 3 + 1
        axis_num = idx + 1
        xref = 'x' if axis_num == 1 else f'x{axis_num}'
        yref = 'y' if axis_num == 1 else f'y{axis_num}'

        vals = NBFC_TIMESERIES[cache_name].get(metric, [None] * 8)
        has_data = any(v is not None for v in vals)

        if has_data:
            fig.add_trace(
                go.Scatter(
                    x=x_vals,
                    y=vals,
                    mode='lines+markers',
                    line=dict(color=color, width=2),
                    marker=dict(color=color, size=5),
                    connectgaps=False,
                    hovertemplate=f"<b>{label}</b><br>%{{x}}<br>{_fmt(None, fmt).replace('—', '')}%{{y}}<extra></extra>",
                    showlegend=False,
                ),
                row=row, col=col,
            )

            lv, li = latest_val(vals)
            if lv is not None:
                # Larger marker at last data point
                fig.add_trace(
                    go.Scatter(
                        x=[li],
                        y=[lv],
                        mode='markers',
                        marker=dict(color=color, size=8),
                        showlegend=False,
                        hoverinfo='skip',
                    ),
                    row=row, col=col,
                )
                # Callout annotation
                callout_annotations.append(dict(
                    x=li,
                    y=lv,
                    xref=xref,
                    yref=yref,
                    text=_fmt(lv, fmt),
                    showarrow=True,
                    ax=0,
                    ay=-24,
                    font=dict(size=9),
                    bgcolor='white',
                    bordercolor=color,
                    borderwidth=1,
                    borderpad=2,
                    arrowcolor=color,
                    arrowsize=0.7,
                ))
        else:
            # Flat grey line
            flat_y = [0] * len(Q_LABELS)
            fig.add_trace(
                go.Scatter(
                    x=x_vals,
                    y=flat_y,
                    mode='lines',
                    line=dict(color='#e2e8f0', width=1.5),
                    showlegend=False,
                    hoverinfo='skip',
                ),
                row=row, col=col,
            )

    # Update subplot title fonts first
    fig.update_annotations(font_size=11.5)

    # Add callout annotations separately
    for ann in callout_annotations:
        fig.add_annotation(**ann)

    # Update x-axis ticks for all subplots
    for i in range(1, 16):
        xaxis_key = f'xaxis{i}' if i > 1 else 'xaxis'
        fig.update_layout(**{
            xaxis_key: dict(
                tickmode='array',
                tickvals=list(range(len(Q_LABELS))),
                ticktext=Q_LABELS,
                tickangle=45,
                tickfont=dict(size=8),
                showgrid=True,
                gridcolor='#f1f5f9',
            )
        })

    title_text = f'<b style="color:#0a2540;font-size:16px;">{nbfc_disp} — All Metrics Q4FY24 → Q3FY26</b>'
    fig.update_layout(
        height=1020,
        showlegend=False,
        title=dict(text=title_text, x=0, xref='paper', font=dict(family='Inter')),
        font=dict(family='Inter'),
        paper_bgcolor='white',
        plot_bgcolor='#fafafa',
    )

    return fig


# ── MARKET DATA FUNCTIONS ──────────────────────────────────────────────────────

@st.cache_data(ttl=3600, persist="disk")
def fetch_stock_data(symbol, period='1y'):
    try:
        return yf.Ticker(symbol).history(period=period)
    except:
        return None


@st.cache_data(ttl=3600, persist="disk")
def fetch_stock_data_range(symbol, start_str, end_str):
    try:
        return yf.Ticker(symbol).history(start=start_str, end=end_str)
    except Exception:
        return None


@st.cache_data(ttl=3600, persist="disk")
def fetch_shares_outstanding():
    def _fetch_one(args):
        name, symbol = args
        try:
            shares = yf.Ticker(symbol).fast_info.shares
            return symbol, int(shares) if shares and shares > 0 else None
        except Exception:
            return symbol, None
    result = {}
    with ThreadPoolExecutor(max_workers=len(NBFCS)) as ex:
        for symbol, shares in ex.map(_fetch_one, NBFCS.items()):
            if shares:
                result[symbol] = shares
    return result


def _fetch_all_prices():
    """Batch download all 9 tickers and return price data list."""
    symbols = list(NBFCS.values())
    names = list(NBFCS.keys())
    result = []

    try:
        raw = yf.download(
            symbols,
            period='1mo',
            group_by='ticker',
            auto_adjust=True,
            progress=False,
            threads=False,
        )
    except Exception:
        raw = None

    price_map = {}
    if raw is not None and not raw.empty:
        for sym in symbols:
            try:
                if len(symbols) == 1:
                    hist = raw
                else:
                    hist = raw[sym] if sym in raw.columns.get_level_values(0) else None
                if hist is not None and not hist.empty and 'Close' in hist.columns:
                    closes = hist['Close'].dropna()
                    if len(closes) >= 2:
                        cur = float(closes.iloc[-1])
                        prev = float(closes.iloc[-2])
                        vol = float(hist['Volume'].iloc[-1]) if 'Volume' in hist.columns else 0
                        price_map[sym] = {'cur': cur, 'prev': prev, 'vol': vol}
            except Exception:
                pass

    # Retry missing individually
    for sym in symbols:
        if sym not in price_map:
            try:
                hist = yf.Ticker(sym).history(period='1mo')
                if hist is not None and not hist.empty:
                    closes = hist['Close'].dropna()
                    if len(closes) >= 2:
                        cur = float(closes.iloc[-1])
                        prev = float(closes.iloc[-2])
                        vol = float(hist['Volume'].iloc[-1]) if 'Volume' in hist.columns else 0
                        price_map[sym] = {'cur': cur, 'prev': prev, 'vol': vol}
            except Exception:
                pass

    # Parallel fetch market caps
    mc_map = {}
    def _fetch_mc(sym):
        try:
            mc = yf.Ticker(sym).fast_info.market_cap
            return sym, mc if mc else None
        except Exception:
            return sym, None

    with ThreadPoolExecutor(max_workers=len(symbols)) as ex:
        for sym, mc in ex.map(_fetch_mc, symbols):
            mc_map[sym] = mc

    # Build result in NBFCS display order
    for name in DISPLAY_NAMES:
        sym = NBFCS[name]
        pd_map = price_map.get(sym, {})
        cur = pd_map.get('cur')
        prev = pd_map.get('prev')
        vol = pd_map.get('vol', 0)
        mc = mc_map.get(sym)

        if cur is not None and prev is not None:
            change_abs = cur - prev
            change_pct = (change_abs / prev * 100) if prev != 0 else 0
        else:
            change_abs = None
            change_pct = None

        result.append({
            'name': name,
            'symbol': sym,
            'price': cur,
            'prev': prev,
            'change_abs': change_abs,
            'change_pct': change_pct,
            'volume': vol,
            'market_cap': mc,
        })

    return result


def get_current_prices():
    """Smart cache in session state: TTL=300s if all 9 loaded, 30s otherwise."""
    now = datetime.now().timestamp()
    cache_data = st.session_state.get('_prices_cache', None)
    cache_ts = st.session_state.get('_prices_ts', 0)

    if cache_data is not None:
        loaded = sum(1 for p in cache_data if p.get('price') is not None)
        ttl = 300 if loaded == len(NBFCS) else 30
        if now - cache_ts < ttl:
            return cache_data

    data = _fetch_all_prices()
    st.session_state['_prices_cache'] = data
    st.session_state['_prices_ts'] = now
    return data


def create_comparison_chart(time_period, selected_stocks, start_date=None, end_date=None):
    """Returns (fig, start_date, end_date)."""
    DAYS_MAP = {'1W': 7, '1M': 30, '3M': 90, '6M': 180, '1Y': 365, '3Y': 1095, '5Y': 1825}

    if start_date is None or end_date is None:
        days = DAYS_MAP.get(time_period, 180)
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days)

    start_str = start_date.strftime('%Y-%m-%d')
    end_str = end_date.strftime('%Y-%m-%d')

    fig = go.Figure()
    series_info = []

    all_indexed = {}
    first_prices = {}
    last_prices = {}

    for name in selected_stocks:
        symbol = NBFCS[name]
        hist = fetch_stock_data_range(symbol, start_str, end_str)
        if hist is None or len(hist) < 2:
            # Fall back to period-based fetch
            days = DAYS_MAP.get(time_period, 180)
            if days <= 7:
                period = '5d'
            elif days <= 30:
                period = '1mo'
            elif days <= 90:
                period = '3mo'
            elif days <= 180:
                period = '6mo'
            elif days <= 365:
                period = '1y'
            elif days <= 1095:
                period = '3y'
            else:
                period = '5y'
            hist = fetch_stock_data(symbol, period=period)

        if hist is None or len(hist) < 2:
            continue

        hist = hist.copy()
        hist.index = hist.index.tz_localize(None) if hist.index.tzinfo is not None else hist.index
        closes = hist['Close'].dropna()
        if len(closes) < 2:
            continue

        indexed = (closes / closes.iloc[0]) * 100
        all_indexed[name] = indexed
        first_prices[name] = float(closes.iloc[0])
        last_prices[name] = float(closes.iloc[-1])
        lv = float(indexed.iloc[-1])
        series_info.append((name, lv))

    for name in selected_stocks:
        if name not in all_indexed:
            continue
        indexed = all_indexed[name]
        raw_prices = list(last_prices.get(name, 0) * indexed / 100) if name in all_indexed else []
        color = COLORS[name]

        fig.add_trace(go.Scatter(
            x=indexed.index,
            y=indexed.values,
            name=name,
            mode='lines',
            line=dict(color=color, width=2),
            customdata=[[p] for p in (indexed.values * first_prices.get(name, 1) / 100)],
            hovertemplate=(
                f"<b>{name}</b><br>"
                "%{x|%d %b %Y}<br>"
                "Index: %{y:.1f} · ₹%{customdata[0]:,.0f}"
                "<extra></extra>"
            ),
        ))

        # Endpoint dot
        if len(indexed) > 0:
            fig.add_trace(go.Scatter(
                x=[indexed.index[-1]],
                y=[float(indexed.iloc[-1])],
                mode='markers',
                marker=dict(color=color, size=7),
                showlegend=False,
                hoverinfo='skip',
            ))

    if series_info:
        all_ys = []
        for trace in fig.data:
            if trace.y is not None:
                all_ys.extend([v for v in trace.y if v is not None])
        if all_ys:
            y_min, y_max = min(all_ys), max(all_ys)
            y_range = y_max - y_min if y_max != y_min else 1.0
        else:
            y_range = 1.0
        GAP = max(4.0, y_range * 0.13)

        series_info_sorted = sorted(series_info, key=lambda x: -x[1])
        label_positions = []
        for name, yv in series_info_sorted:
            pos = yv
            for prev_pos in label_positions:
                if abs(pos - prev_pos) < GAP:
                    pos = prev_pos - GAP
            label_positions.append(pos)

        # Expand y bounds to include label positions
        if label_positions:
            y_min_new = min(all_ys + label_positions) - GAP * 0.5
            y_max_new = max(all_ys + label_positions) + GAP * 0.5
            fig.update_yaxes(range=[y_min_new, y_max_new])

        for idx, (name, yv) in enumerate(series_info_sorted):
            label_y = label_positions[idx]
            color = COLORS[name]
            fp = first_prices.get(name, 0)
            lp = last_prices.get(name, 0)
            change_pct = (yv - 100)
            sign = '+' if change_pct >= 0 else ''
            ann_text = f"<b>{name}</b>  {sign}{change_pct:.1f}%<br>₹{fp:,.0f} → ₹{lp:,.0f}"
            fig.add_annotation(
                x=1.0,
                y=label_y,
                xref='paper',
                yref='y',
                text=ann_text,
                showarrow=False,
                xanchor='left',
                xshift=8,
                font=dict(size=9.5, color='#0a2540'),
                bgcolor='white',
                bordercolor=color,
                borderwidth=1,
                borderpad=3,
                align='left',
            )

    period_label = time_period if not (start_date and end_date) else 'CUSTOM'
    title_text = f'<b style="color:#0a2540;font-size:17px;">Performance Comparison — {period_label} (Indexed to 100)</b>'

    fig.update_layout(
        template='plotly_white',
        hovermode='x unified',
        showlegend=False,
        margin=dict(l=60, r=220, t=60, b=50),
        title=dict(text=title_text, x=0, xref='paper', font=dict(family='Inter')),
        xaxis=dict(
            showgrid=True,
            gridcolor='#f1f5f9',
            showline=True,
            linecolor='#cbd5e1',
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='#f1f5f9',
            showline=True,
            linecolor='#cbd5e1',
        ),
        font=dict(family='Inter'),
    )

    return fig, start_date, end_date


# ── NBFC SELECTOR WIDGET ───────────────────────────────────────────────────────

def nbfc_selector(tab_key: str, default_on=None) -> list:
    if default_on is None:
        default_on = ['Bajaj Finance', 'Shriram Finance', 'L&T Finance']
    cols = st.columns(5)
    selected = ['Poonawalla Fincorp']
    others = [n for n in DISPLAY_NAMES if n != 'Poonawalla Fincorp']
    cols[0].checkbox("Poonawalla Fincorp", value=True, disabled=True, key=f"{tab_key}_poonawalla_fixed")
    for i, name in enumerate(others):
        with cols[(i + 1) % 5]:
            if st.checkbox(name, value=(name in default_on), key=f"{tab_key}_{name}"):
                selected.append(name)
    return selected


# ── AUTO-REFRESH JS ────────────────────────────────────────────────────────────
components.html("""
<script>
(function() {
    const IDLE_TIMEOUT = 5 * 60 * 1000;  // 5 minutes

    function touchActivity() {
        try {
            window.parent.localStorage.setItem('nbfc_last_active', Date.now().toString());
        } catch(e) {}
    }

    function checkAndReload() {
        try {
            var last = parseInt(window.parent.localStorage.getItem('nbfc_last_active') || '0');
            if (last === 0) {
                touchActivity();
                return;
            }
            if (Date.now() - last > IDLE_TIMEOUT) {
                touchActivity();
                window.parent.location.reload();
            }
        } catch(e) {}
    }

    ['mousemove', 'click', 'keydown', 'scroll', 'touchstart'].forEach(function(evt) {
        window.parent.addEventListener(evt, touchActivity, { passive: true });
    });

    document.addEventListener('visibilitychange', function() {
        if (!document.hidden) checkAndReload();
    });

    window.addEventListener('focus', checkAndReload);

    touchActivity();
})();
</script>
""", height=0)


# ── SESSION STATE INIT ─────────────────────────────────────────────────────────
if 'time_period' not in st.session_state:
    st.session_state.time_period = '6M'
if 'use_custom_date' not in st.session_state:
    st.session_state.use_custom_date = False


# ── HEADER ─────────────────────────────────────────────────────────────────────
ist = pytz.timezone('Asia/Kolkata')
now_ist = datetime.now(ist)
date_str = now_ist.strftime('%-d %b %Y')
time_str = now_ist.strftime('%H:%M')

st.markdown(f"""
<div style="display:flex;align-items:baseline;justify-content:space-between;
            border-bottom:1px solid #dde1e8;padding-bottom:10px;margin-bottom:16px;">
  <div style="display:flex;align-items:baseline;gap:14px;">
    <span style="font-family:'Inter',sans-serif;font-size:26px;font-weight:800;color:#0a2540;">
      NBFC Dashboard
    </span>
    <span style="font-family:'JetBrains Mono',monospace;font-size:11px;font-weight:600;
                 color:#0284c7;background:#e0f2fe;padding:3px 9px;border-radius:4px;">
      NSE · INDIA
    </span>
  </div>
  <span style="font-family:'JetBrains Mono',monospace;font-size:12px;color:#94a3b8;">
    {date_str} · {time_str} IST
  </span>
</div>
""", unsafe_allow_html=True)


# ── TABS ───────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10 = st.tabs([
    "Market", "Financials", "Asset Quality", "Capital & Leverage",
    "Profitability Ratios", "Valuation Metrics", "Deep Dive", "Rankings",
    "AI Bulletin", "Shareholding",
])


# ── TAB 1 — MARKET ─────────────────────────────────────────────────────────────
with tab1:
    st.markdown("""
    <div class="section-label">Stock Prices
      <span class="section-label-sub" style="margin-left:8px;">Live NSE · auto-refreshes after 5 min idle</span>
    </div>
    """, unsafe_allow_html=True)

    with st.spinner("Fetching live prices…"):
        prices_data = get_current_prices()

    if not prices_data:
        st.warning("Unable to fetch prices. Check your internet connection.")
    else:
        def _fmt_vol(v):
            if v is None or v == 0:
                return "—"
            if v >= 1e7:
                return f"{v/1e7:.1f}Cr"
            elif v >= 1e5:
                return f"{v/1e5:.1f}L"
            elif v >= 1e3:
                return f"{v/1e3:.1f}K"
            return str(int(v))

        def _fmt_mc(mc):
            if mc is None:
                return "—"
            mc_lc = mc / 1e12
            if mc_lc >= 1:
                return f"₹{mc_lc:.2f} L.Cr"
            mc_k = mc / 1e9
            if mc_k >= 1:
                return f"₹{mc_k:.1f}K Cr"
            mc_cr = mc / 1e7
            return f"₹{mc_cr:.0f} Cr"

        rows_of_3 = [prices_data[i:i+3] for i in range(0, len(prices_data), 3)]
        for row_items in rows_of_3:
            cols = st.columns(3)
            for ci, item in enumerate(row_items):
                name = item['name']
                sym = NBFCS[name].replace('.NS', '')
                price = item['price']
                chg_abs = item['change_abs']
                chg_pct = item['change_pct']
                vol = item['volume']
                mc = item['market_cap']

                is_pos = (chg_pct is not None and chg_pct >= 0)
                border_color = '#16a34a' if is_pos else '#dc2626'
                chg_cls = 'ticker-pos' if is_pos else 'ticker-neg'
                arrow = '▲' if is_pos else '▼'

                if price is not None:
                    price_str = f"₹{price:,.2f}"
                    chg_str = f"{arrow} {abs(chg_pct):.2f}%" if chg_pct is not None else "—"
                    meta1 = f"±₹{abs(chg_abs):.2f} · Vol {_fmt_vol(vol)}" if chg_abs is not None else f"Vol {_fmt_vol(vol)}"
                else:
                    price_str = "—"
                    chg_str = "—"
                    meta1 = "—"

                meta2 = f"MCap {_fmt_mc(mc)}"

                with cols[ci]:
                    st.markdown(f"""
                    <div class="ticker-card" style="border-top-color:{border_color};">
                      <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                        <div>
                          <div class="ticker-name-sm">{name}</div>
                          <div class="ticker-sym">{sym}</div>
                        </div>
                        <div style="text-align:right;">
                          <div class="ticker-price">{price_str}</div>
                          <div class="{chg_cls}">{chg_str}</div>
                        </div>
                      </div>
                      <div style="margin-top:6px;">
                        <span class="ticker-meta">{meta1}</span><br>
                        <span class="ticker-meta">{meta2}</span>
                      </div>
                    </div>
                    """, unsafe_allow_html=True)

            st.markdown('<div style="height:4px;"></div>', unsafe_allow_html=True)

        # Fetch timestamp
        cache_ts = st.session_state.get('_prices_ts', 0)
        if cache_ts > 0:
            mins_ago = int((datetime.now().timestamp() - cache_ts) / 60)
            st.markdown(
                f'<div style="text-align:right;font-size:10px;color:#94a3b8;font-family:\'JetBrains Mono\',monospace;">↻ fetched {mins_ago} min ago</div>',
                unsafe_allow_html=True
            )

    st.markdown('<div style="height:6px;"></div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="section-label">Performance Comparison
      <span class="section-label-sub" style="margin-left:8px;">Indexed to 100 · select stocks and period below</span>
    </div>
    """, unsafe_allow_html=True)

    sel_cmp = nbfc_selector('mkt', default_on=DEFAULT_COMPARISON)

    st.markdown('<div style="height:6px;"></div>', unsafe_allow_html=True)

    # Period buttons
    periods = ['1W', '1M', '3M', '6M', '1Y', '3Y', '5Y']
    btn_cols = st.columns([0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 3.5])
    for i, p in enumerate(periods):
        with btn_cols[i]:
            if st.button(p, key=f"period_{p}"):
                st.session_state.time_period = p
                st.session_state.use_custom_date = False
                st.rerun()

    active_label = 'CUSTOM' if st.session_state.use_custom_date else st.session_state.time_period

    # Highlight active period button
    js_highlight = f"""
    <script>
    (function() {{
        var active = "{active_label}";
        var buttons = window.parent.document.querySelectorAll('button[kind="secondary"]');
        buttons.forEach(function(btn) {{
            if (btn.innerText.trim() === active) {{
                btn.style.background = '#0284c7';
                btn.style.color = 'white';
                btn.style.fontWeight = '700';
                btn.style.borderColor = '#0284c7';
            }}
        }});
    }})();
    </script>
    """
    components.html(js_highlight, height=0)

    # Custom date picker
    c1, c2, c3, c4 = st.columns([1.4, 1.4, 0.8, 4.4])
    today = _date.today()
    with c1:
        custom_from = st.date_input("From", value=today - timedelta(days=180), key="cust_from", label_visibility="visible")
    with c2:
        custom_to = st.date_input("To", value=today, key="cust_to", label_visibility="visible")
    with c3:
        st.markdown('<div style="height:28px;"></div>', unsafe_allow_html=True)
        if st.button("Apply", key="apply_custom"):
            st.session_state.use_custom_date = True
            st.rerun()

    if st.session_state.use_custom_date:
        s_date = custom_from
        e_date = custom_to
    else:
        days = {'1W': 7, '1M': 30, '3M': 90, '6M': 180, '1Y': 365, '3Y': 1095, '5Y': 1825}.get(st.session_state.time_period, 180)
        e_date = today
        s_date = e_date - timedelta(days=days)

    fmt_from = s_date.strftime('%-d %b\'%y')
    fmt_to = e_date.strftime('%-d %b\'%y')

    with st.spinner("Loading comparison chart…"):
        cmp_fig, _, _ = create_comparison_chart(
            st.session_state.time_period,
            sel_cmp,
            start_date=s_date if st.session_state.use_custom_date else None,
            end_date=e_date if st.session_state.use_custom_date else None,
        )
        # Update title with date range
        date_label = f"{fmt_from} – {fmt_to}"
        period_label = 'CUSTOM' if st.session_state.use_custom_date else st.session_state.time_period
        cmp_fig.update_layout(
            title_text=f'<b style="color:#0a2540;font-size:17px;">Performance Comparison — {period_label} · {date_label} (Indexed to 100)</b>'
        )
        st.plotly_chart(cmp_fig, use_container_width=True, key="mkt_comparison")

    st.markdown('<div style="height:10px;"></div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="section-label">Market Capitalisation Trend
      <span class="section-label-sub" style="margin-left:8px;">1-year daily · ₹ Lakh Crore · price × shares outstanding</span>
    </div>
    """, unsafe_allow_html=True)

    sel_mc = nbfc_selector('mc_', default_on=DEFAULT_COMPARISON)

    st.markdown('<div style="height:6px;"></div>', unsafe_allow_html=True)

    with st.spinner("Loading market cap chart…"):
        mc_fig = make_mktcap_trend_chart(sel_mc, height=440)
        st.plotly_chart(mc_fig, use_container_width=True, key="mkt_mcap")

    st.markdown("""
    <div class="metric-note">
      Market cap = daily NSE closing price × current shares outstanding (sourced from yfinance).
      Values in ₹ Lakh Crore (1 L.Cr = ₹1 Trillion).
    </div>
    """, unsafe_allow_html=True)


# ── TAB 2 — FINANCIALS ─────────────────────────────────────────────────────────
with tab2:
    st.markdown("""
    <div class="tab-intro">
      <div class="tab-intro-title">Growth &amp; Scale</div>
      <div class="tab-intro-sub">Q4FY24 – Q3FY26 · AUM · PAT · NIM · 8 quarters · 9 NBFCs</div>
    </div>
    """, unsafe_allow_html=True)

    sel2 = nbfc_selector('fin')
    st.markdown('<div style="height:10px;"></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-label">Scale</div>', unsafe_allow_html=True)

    aum_bar = make_bar_chart('aum_cr', sel2, 'Assets Under Management (AUM)', '₹ Crore')
    st.plotly_chart(aum_bar, use_container_width=True, key="fin_aum_bar")

    col_a, col_b = st.columns(2)
    with col_a:
        qoq_aum = make_qoq_chart('aum_cr', sel2, 'AUM')
        st.plotly_chart(qoq_aum, use_container_width=True, key="fin_aum_qoq")
    with col_b:
        yoy_aum = make_yoy_chart('aum_cr', sel2, 'AUM')
        st.plotly_chart(yoy_aum, use_container_width=True, key="fin_aum_yoy")

    pat_bar = make_bar_chart('pat_cr', sel2, 'Profit After Tax (PAT)', '₹ Crore')
    st.plotly_chart(pat_bar, use_container_width=True, key="fin_pat_bar")

    col_c, col_d = st.columns(2)
    with col_c:
        qoq_pat = make_qoq_chart('pat_cr', sel2, 'PAT')
        st.plotly_chart(qoq_pat, use_container_width=True, key="fin_pat_qoq")
    with col_d:
        yoy_pat = make_yoy_chart('pat_cr', sel2, 'PAT')
        st.plotly_chart(yoy_pat, use_container_width=True, key="fin_pat_yoy")

    st.markdown('<div class="section-label">Yield</div>', unsafe_allow_html=True)

    nim_chart = make_trend_chart('nim_pct', sel2, 'Net Interest Margin (NIM)', 'NIM (%)')
    st.plotly_chart(nim_chart, use_container_width=True, key="fin_nim")


# ── TAB 3 — ASSET QUALITY ──────────────────────────────────────────────────────
with tab3:
    st.markdown("""
    <div class="tab-intro">
      <div class="tab-intro-title">Asset Quality</div>
      <div class="tab-intro-sub">Q4FY24 – Q3FY26 · GNPA · NNPA · PCR</div>
    </div>
    """, unsafe_allow_html=True)

    sel3 = nbfc_selector('aq')
    st.markdown('<div style="height:10px;"></div>', unsafe_allow_html=True)

    gnpa_chart = make_trend_chart('gnpa_pct', sel3, 'Gross NPA (GNPA %)', 'GNPA (%)', lower_is_better=True)
    st.plotly_chart(gnpa_chart, use_container_width=True, key="aq_gnpa")

    nnpa_chart = make_trend_chart('nnpa_pct', sel3, 'Net NPA (NNPA %)', 'NNPA (%)', lower_is_better=True)
    st.plotly_chart(nnpa_chart, use_container_width=True, key="aq_nnpa")

    pcr_chart = make_trend_chart('pcr_pct', sel3, 'Provision Coverage Ratio (PCR %)', 'PCR (%)', height=380)
    st.plotly_chart(pcr_chart, use_container_width=True, key="aq_pcr")

    st.markdown("""
    <div class="metric-note">
      Lower GNPA/NNPA = better credit quality. Higher PCR = more conservative provisioning.
    </div>
    """, unsafe_allow_html=True)


# ── TAB 4 — CAPITAL & LEVERAGE ─────────────────────────────────────────────────
with tab4:
    st.markdown("""
    <div class="tab-intro">
      <div class="tab-intro-title">Capital Structure &amp; Leverage</div>
      <div class="tab-intro-sub">Q4FY24 – Q3FY26 · CoB · D/E · CAR · Tier 1 · Tier 2</div>
    </div>
    """, unsafe_allow_html=True)

    sel4 = nbfc_selector('cap')
    st.markdown('<div style="height:10px;"></div>', unsafe_allow_html=True)

    cob_chart = make_trend_chart('cost_of_borrowing_pct', sel4, 'Cost of Borrowing (%)', 'CoB (%)', lower_is_better=True)
    st.plotly_chart(cob_chart, use_container_width=True, key="cap_cob")

    de_chart = make_trend_chart('d_e_ratio', sel4, 'Debt-to-Equity Ratio (D/E)', 'D/E Ratio', fmt='ratio', lower_is_better=True)
    st.plotly_chart(de_chart, use_container_width=True, key="cap_de")

    car_chart = make_trend_chart('car_pct', sel4, 'Capital Adequacy Ratio (CAR/CRAR %)', 'CAR (%)')
    st.plotly_chart(car_chart, use_container_width=True, key="cap_car")

    t1_note = 'Chola · AB Capital · L&T Finance only — others not disclosed separately'
    t1_chart = make_trend_chart('t1_pct', sel4, 'Tier 1 Capital (%)', 'Tier 1 (%)', note=t1_note)
    st.plotly_chart(t1_chart, use_container_width=True, key="cap_t1")

    t2_note = 'Chola · AB Capital · L&T Finance only — others not disclosed separately'
    t2_chart = make_trend_chart('t2_pct', sel4, 'Tier 2 Capital (%)', 'Tier 2 (%)', note=t2_note)
    st.plotly_chart(t2_chart, use_container_width=True, key="cap_t2")

    st.markdown("""
    <div class="metric-note">
      D/E: lower = less levered. CAR: higher = better capitalised (RBI minimum 15%).
      Tier 1 = core equity capital; Tier 2 = supplementary capital.
      T1/T2 available for Chola, AB Capital, and L&T Finance only.
    </div>
    """, unsafe_allow_html=True)


# ── TAB 5 — PROFITABILITY RATIOS ───────────────────────────────────────────────
with tab5:
    st.markdown("""
    <div class="tab-intro">
      <div class="tab-intro-title">Profitability Ratios</div>
      <div class="tab-intro-sub">Q4FY24 – Q3FY26 · ROA · ROE · 8 quarters · 9 NBFCs</div>
    </div>
    """, unsafe_allow_html=True)

    sel5 = nbfc_selector('prof')
    st.markdown('<div style="height:10px;"></div>', unsafe_allow_html=True)

    roa_chart = make_trend_chart('roa_pct', sel5, 'Return on Assets (ROA)', 'ROA (%)')
    st.plotly_chart(roa_chart, use_container_width=True, key="prof_roa")

    roe_chart = make_trend_chart('roe_pct', sel5, 'Return on Equity (ROE)', 'ROE (%)')
    st.plotly_chart(roe_chart, use_container_width=True, key="prof_roe")


# ── TAB 6 — VALUATION METRICS ─────────────────────────────────────────────────
with tab6:
    st.markdown("""
    <div class="tab-intro">
      <div class="tab-intro-title">Valuation Metrics</div>
      <div class="tab-intro-sub">Q4FY24 – Q3FY26 · BVPS · P/B Ratio · Daily prices over quarterly book value</div>
    </div>
    """, unsafe_allow_html=True)

    sel6 = nbfc_selector('val')
    st.markdown('<div style="height:10px;"></div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="section-label">Price-to-Book Ratio
      <span class="section-label-sub" style="margin-left:8px;">Daily NSE closing price ÷ latest quarterly BVPS</span>
    </div>
    """, unsafe_allow_html=True)

    with st.spinner("Loading P/B chart…"):
        pb_chart = make_pb_chart(sel6, height=520)
        st.plotly_chart(pb_chart, use_container_width=True, key="val_pb")

    st.markdown("""
    <div class="section-label">Book Value Per Share (BVPS)
      <span class="section-label-sub" style="margin-left:8px;">₹ per share · quarterly — absolute reference</span>
    </div>
    """, unsafe_allow_html=True)

    bvps_chart = make_trend_chart('bvps_inr', sel6, 'Book Value Per Share (BVPS)', 'BVPS (₹)', fmt='inr', height=380)
    st.plotly_chart(bvps_chart, use_container_width=True, key="val_bvps")

    st.markdown("""
    <div class="metric-note">
      P/B = Daily NSE closing price ÷ most recently reported quarterly BVPS.
      BVPS steps up at each quarter-end (Q4FY24–Q3FY26). Dotted line at P/B = 1 (book value floor).
      Lower P/B may indicate undervaluation relative to peers.
    </div>
    """, unsafe_allow_html=True)


# ── TAB 7 — DEEP DIVE ──────────────────────────────────────────────────────────
with tab7:
    st.markdown("""
    <div class="tab-intro">
      <div class="tab-intro-title">Company Deep Dive</div>
      <div class="tab-intro-sub">Select an NBFC to view all 14 metrics across 8 quarters · Tier 1 &amp; Tier 2 where disclosed</div>
    </div>
    """, unsafe_allow_html=True)

    chosen = st.selectbox(
        "Select NBFC",
        DISPLAY_NAMES,
        index=0,
        key="deep_dive_nbfc",
        label_visibility="collapsed"
    )

    with st.spinner(f"Loading deep dive for {chosen}…"):
        dd_fig = make_deep_dive(chosen)
        st.plotly_chart(dd_fig, use_container_width=True, key="deep_dive_chart")

    st.markdown("""
    <div class="metric-note">
      Gaps in charts = metric not disclosed for that quarter.
    </div>
    """, unsafe_allow_html=True)


# ── TAB 8 — RANKINGS ───────────────────────────────────────────────────────────
with tab8:
    st.markdown("""
    <div class="tab-intro">
      <div class="tab-intro-title">Peer Scorecard — Q3 FY26</div>
      <div class="tab-intro-sub">All 9 NBFCs · 11 metrics · Red → Yellow → Green spectrum within each column</div>
    </div>
    """, unsafe_allow_html=True)

    rank_fig = build_rankings_table()
    st.plotly_chart(rank_fig, use_container_width=True, key="rank_table")

    st.markdown("""
    <div class="metric-note">
      Color coding: green = best-in-class, yellow = mid-range, red = weakest.
      For GNPA/NNPA/CoB/D/E lower is better; for AUM/PAT/NIM/ROA/ROE/CAR higher is better.
      — = not disclosed.
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-label">Quick Highlights — Q3 FY26</div>', unsafe_allow_html=True)

    # Compute highlights
    Q_IDX = 7

    def _get_q3(metric):
        best_name, best_val = None, None
        for name in DISPLAY_NAMES:
            cache = CACHE_KEY[name]
            vals = NBFC_TIMESERIES[cache].get(metric, [None] * 8)
            v = vals[Q_IDX] if Q_IDX < len(vals) else None
            if v is not None:
                if best_val is None or v > best_val:
                    best_val = v
                    best_name = name
        return best_name, best_val

    def _get_q3_min(metric):
        best_name, best_val = None, None
        for name in DISPLAY_NAMES:
            cache = CACHE_KEY[name]
            vals = NBFC_TIMESERIES[cache].get(metric, [None] * 8)
            v = vals[Q_IDX] if Q_IDX < len(vals) else None
            if v is not None:
                if best_val is None or v < best_val:
                    best_val = v
                    best_name = name
        return best_name, best_val

    aum_name, aum_val = _get_q3('aum_cr')
    pat_name, pat_val = _get_q3('pat_cr')
    roa_name, roa_val = _get_q3('roa_pct')
    gnpa_name, gnpa_val = _get_q3_min('gnpa_pct')

    hl_cols = st.columns(4)
    highlights = [
        ("Largest AUM", aum_name, f"₹{int(aum_val):,} Cr" if aum_val else "—", "AUM Q3FY26", '#0284c7'),
        ("Highest PAT", pat_name, f"₹{int(pat_val):,} Cr" if pat_val else "—", "PAT Q3FY26", '#10b981'),
        ("Best ROA", roa_name, f"{roa_val:.2f}%" if roa_val else "—", "ROA Q3FY26", '#f97316'),
        ("Cleanest Book", gnpa_name, f"GNPA {gnpa_val:.2f}%" if gnpa_val else "—", "GNPA Q3FY26", '#8b5cf6'),
    ]

    for i, (label, name, value, note_txt, color) in enumerate(highlights):
        with hl_cols[i]:
            st.markdown(f"""
            <div style="background:white;border-radius:5px;padding:12px 14px;border-top:3px solid {color};box-shadow:0 1px 2px rgba(0,0,0,0.05);">
              <div style="font-size:10px;font-weight:700;letter-spacing:0.06em;text-transform:uppercase;color:#94a3b8;">{label}</div>
              <div style="font-size:15px;font-weight:700;color:#0a2540;margin:4px 0 2px;">{name or '—'}</div>
              <div style="font-size:12px;font-weight:600;color:{color};">{value}</div>
              <div style="font-size:10.5px;color:#64748b;">{note_txt}</div>
            </div>
            """, unsafe_allow_html=True)


# ── TAB 9 — AI BULLETIN ────────────────────────────────────────────────────────
with tab9:
    st.markdown("""
    <div class="tab-intro">
      <div class="tab-intro-title">AI Bulletin</div>
      <div class="tab-intro-sub">51 AI initiatives across 9 NBFCs · Jan 2021 – Feb 2026 · Research compiled 23 Feb 2026</div>
    </div>
    """, unsafe_allow_html=True)

    def _parse_ai_date(d):
        try:
            return _dt.strptime(d.strip(), "%d %b %Y")
        except Exception:
            return _dt(1970, 1, 1)

    # Filter row
    ai_col1, ai_col2, ai_col3 = st.columns([2, 2, 1])
    with ai_col1:
        ai_nbfc_filter = st.selectbox(
            "Filter by NBFC",
            ["All NBFCs"] + list(NBFC_AI_INITIATIVES.keys()),
            key="ai_nbfc_filter",
        )
    with ai_col2:
        ai_func_filter = st.selectbox(
            "Filter by Function",
            ["All Functions"] + FUNCTION_TAXONOMY,
            key="ai_func_filter",
        )
    with ai_col3:
        ai_sort = st.selectbox(
            "Sort by",
            ["Newest first", "Oldest first", "NBFC", "Title"],
            key="ai_sort",
        )

    # Build items list
    tbl_items = []
    for nbfc, initiatives in NBFC_AI_INITIATIVES.items():
        if ai_nbfc_filter != "All NBFCs" and nbfc != ai_nbfc_filter:
            continue
        for init in initiatives:
            if ai_func_filter != "All Functions":
                if ai_func_filter not in init.get('functions', []):
                    continue
            tbl_items.append((nbfc, init))

    # Sort
    if ai_sort == "Newest first":
        tbl_items.sort(key=lambda x: _parse_ai_date(x[1].get('date', '')), reverse=True)
    elif ai_sort == "Oldest first":
        tbl_items.sort(key=lambda x: _parse_ai_date(x[1].get('date', '')))
    elif ai_sort == "NBFC":
        tbl_items.sort(key=lambda x: x[0])
    elif ai_sort == "Title":
        tbl_items.sort(key=lambda x: x[1].get('title', ''))

    # Render cards
    for nbfc, init in tbl_items:
        color = COLORS.get(nbfc, '#0284c7')
        tags_html = ''.join(
            f'<span class="ai-func-tag">{fn}</span> '
            for fn in init.get('functions', [])
        )
        src_url = init.get('source_url', '')
        src_name = init.get('source_name', '')
        if src_url:
            src_html = f'<a class="ai-source-link" href="{src_url}" target="_blank" rel="noopener">↗ {src_name}</a>'
        else:
            src_html = f'<span style="font-size:11px;color:#94a3b8;">{src_name}</span>'

        st.markdown(f"""
        <div class="ai-row-card" style="--nbfc-color:{color};">
          <div class="ai-row-header" style="display:flex;align-items:center;justify-content:space-between;margin-bottom:7px;">
            <span class="ai-nbfc-badge" style="background:{color};">{nbfc}</span>
            <span class="ai-date-badge">{init.get('date', '')}</span>
          </div>
          <div class="ai-row-title">{init.get('title', '')}</div>
          <div class="ai-impact">⚡ {init.get('impact', '')}</div>
          <div class="ai-row-desc">{init.get('description', '')}</div>
          <div class="ai-row-footer" style="display:flex;align-items:flex-start;justify-content:space-between;flex-wrap:wrap;gap:6px;border-top:1px solid #f1f5f9;padding-top:8px;margin-top:4px;">
            <div style="display:flex;flex-wrap:wrap;gap:4px;">{tags_html}</div>
            {src_html}
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="metric-note">
      Sources: company websites, annual reports, BSE filings, earnings call transcripts,
      Business Standard, Medianama, Microsoft News, Analytics India Magazine, and vendor case studies.
      Compiled 23 Feb 2026.
    </div>
    """, unsafe_allow_html=True)


# ── TAB 10 — SHAREHOLDING PATTERN ─────────────────────────────────────────────
with tab10:
    st.markdown("""
    <div class="tab-intro">
      <div class="tab-intro-title">Shareholding Pattern</div>
      <div class="tab-intro-sub">BSE quarterly filings · Q4FY24 – Q3FY26 (8 quarters) · Named shareholders ≥1%</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Helper functions ──────────────────────────────────────────────────────
    def sh_latest(lst):
        for v in reversed(lst):
            if v is not None: return v
        return None

    def sh_first(lst):
        for v in lst:
            if v is not None: return v
        return None

    def sh_delta_str(lst):
        f, l = sh_first(lst), sh_latest(lst)
        if f is None or l is None: return 0, ""
        d = l - f
        if abs(d) < 0.05:
            return d, '<span style="color:#64748b;font-size:11px;">→ flat</span>'
        arrow = "▲" if d > 0 else "▼"
        col = "#16a34a" if d > 0 else "#dc2626"
        return d, f'<span style="color:{col};font-size:11px;">{arrow} {abs(d):.2f}%</span>'

    def _cell_html(val, prev_val, is_first_app, is_last_app):
        if val is None:
            return '<td class="sh-cell-nil">—</td>'
        v_str = f"{val:.2f}%"
        marker = ""
        if is_first_app:
            marker = '<span class="sh-entry-dot">●</span>'
        elif is_last_app:
            marker = '<span class="sh-exit-dot">○</span>'
        if prev_val is None:
            cls = "sh-cell-flat"
        elif val > prev_val + 0.04:
            cls = "sh-cell-up"
        elif val < prev_val - 0.04:
            cls = "sh-cell-dn"
        else:
            cls = "sh-cell-flat"
        return f'<td class="{cls}">{v_str}{marker}</td>'

    def _total_row(label, vals_list, bg):
        cells, prev = "", None
        for val in vals_list:
            if val is None:
                cells += f'<td class="sh-cell-nil" style="font-weight:700;">—</td>'
            else:
                if prev is None:
                    cls = "sh-cell-flat"
                elif val > prev + 0.04:
                    cls = "sh-cell-up"
                elif val < prev - 0.04:
                    cls = "sh-cell-dn"
                else:
                    cls = "sh-cell-flat"
                cells += f'<td class="{cls}" style="font-weight:700;background:{bg};">{val:.2f}%</td>'
                prev = val
        fv, lv = sh_first(vals_list), sh_latest(vals_list)
        if fv is not None and lv is not None:
            d = lv - fv
            if d > 0.04:
                trend = f'<span class="sh-cell-up">▲ {abs(d):.2f}%</span>'
            elif d < -0.04:
                trend = f'<span class="sh-cell-dn">▼ {abs(d):.2f}%</span>'
            else:
                trend = '<span class="sh-cell-flat">→ flat</span>'
        else:
            trend = "—"
        return (
            f'<tr style="background:{bg};">'
            f'<td class="sh-td-name" style="font-weight:700;color:#0a2540;">{label}</td>'
            f'<td></td>{cells}'
            f'<td style="font-size:10.5px;">{trend}</td>'
            f'</tr>'
        )

    TOTAL_BG = {
        "Promoter": "#d1fae5",
        "FII":      "#e0f2fe",
        "DII":      "#ffedd5",
        "Public":   "#f1f5f9",
    }

    def _group_hdr(label, n_cols):
        empty_cells = ''.join(['<td></td>'] * (n_cols - 1))
        return (
            f'<tr style="background:#f1f5f9;">'
            f'<td colspan="1" style="font-size:10px;font-weight:700;text-transform:uppercase;'
            f'color:#64748b;letter-spacing:0.06em;padding:5px 10px;">{label}</td>'
            f'{empty_cells}'
            f'</tr>'
        )

    def _entity_rows(cat, rows_list, n_q):
        rows_list_sorted = sorted(
            rows_list,
            key=lambda r: (sh_latest(r['pct']) or 0),
            reverse=True,
        )
        html = ""
        for ent in rows_list_sorted:
            pct_vals = ent['pct']
            n = len(pct_vals)
            first_app_i = next((i for i, v in enumerate(pct_vals) if v is not None), None)
            last_app_i = next((i for i, v in enumerate(reversed(pct_vals)) if v is not None), None)
            if last_app_i is not None:
                last_app_i = n - 1 - last_app_i
            is_exited = (last_app_i is not None and last_app_i < n - 1)

            cells = ""
            for qi in range(n_q):
                val = pct_vals[qi] if qi < n else None
                prev_val = pct_vals[qi - 1] if qi > 0 and (qi - 1) < n else None
                is_first = (qi == first_app_i)
                is_last_exit = (qi == last_app_i and is_exited)
                cells += _cell_html(val, prev_val, is_first, is_last_exit)

            # Trend
            fv, lv = sh_first(pct_vals), sh_latest(pct_vals)
            if is_exited and fv is not None and lv is not None:
                d = lv - fv
                trend = f'<span class="sh-cell-dn">▼ {abs(d):.2f}% → exited</span>'
            elif fv is not None and lv is not None:
                d = lv - fv
                if d > 0.04:
                    trend = f'<span class="sh-cell-up">▲ {abs(d):.2f}%</span>'
                elif d < -0.04:
                    trend = f'<span class="sh-cell-dn">▼ {abs(d):.2f}%</span>'
                else:
                    trend = '<span class="sh-cell-flat">→ flat</span>'
            else:
                trend = "—"

            badge_bg = ENTITY_CATEGORY_COLORS.get(cat, '#94a3b8')
            badge_fg = ENTITY_BADGE_TEXT_COLORS.get(cat, 'white')
            badge = f'<span class="sh-cat-badge" style="background:{badge_bg};color:{badge_fg};">{cat}</span>'

            html += (
                f'<tr>'
                f'<td class="sh-td-name">{ent["name"]}</td>'
                f'<td style="padding:6px 10px;">{badge}</td>'
                f'{cells}'
                f'<td style="font-size:10.5px;">{trend}</td>'
                f'</tr>'
            )
        return html

    DII_CATS = ["DII – MF", "DII – Insurance", "DII – Pension", "DII – Other"]

    # ── Section 1 — Q3FY26 Cross-NBFC Snapshot ───────────────────────────────
    st.markdown("""
    <div class="section-label">Q3FY26 Snapshot — All NBFCs
      <span class="section-label-sub" style="margin-left:8px;">Current quarter shareholding · % of paid-up capital</span>
    </div>
    """, unsafe_allow_html=True)

    available_sh = [n for n in DISPLAY_NAMES if n in SHAREHOLDING]
    Q3_IDX = len(SH_QUARTERS) - 1

    snapshot_rows = []
    for name in available_sh:
        sh_data = SHAREHOLDING[name]
        cat_pct = sh_data.get('category_pct', {})
        row = {'name': name}
        for cat in ['Promoter', 'FII', 'DII', 'Public']:
            vals = cat_pct.get(cat, [None] * 8)
            row[cat] = vals[Q3_IDX] if Q3_IDX < len(vals) else None
        snapshot_rows.append(row)

    snapshot_rows.sort(key=lambda r: (r['Promoter'] or 0), reverse=True)

    # Per-column min/max for shading
    col_stats = {}
    for cat in ['Promoter', 'FII', 'DII', 'Public']:
        vals = [r[cat] for r in snapshot_rows if r[cat] is not None]
        if vals:
            col_stats[cat] = (min(vals), max(vals))
        else:
            col_stats[cat] = (0, 1)

    cat_header_colors = {
        'Promoter': '#059669',
        'FII': '#0284c7',
        'DII': '#ea580c',
        'Public': '#64748b',
    }

    snap_html = '<table style="border-collapse:collapse;width:100%;font-size:12px;">'
    snap_html += '<thead><tr>'
    snap_html += '<th style="background:#0a2540;color:white;padding:8px 12px;text-align:left;font-size:11px;">NBFC</th>'
    for cat in ['Promoter', 'FII', 'DII', 'Public']:
        hc = cat_header_colors[cat]
        snap_html += f'<th style="background:{hc};color:white;padding:8px 12px;text-align:right;font-size:11px;">{cat}</th>'
    snap_html += '</tr></thead><tbody>'

    for row in snapshot_rows:
        nbfc_color = COLORS.get(row['name'], '#0284c7')
        name_cell = (
            f'<td style="padding:8px 12px;font-weight:600;color:#0a2540;">'
            f'<span style="display:inline-block;width:8px;height:8px;border-radius:50%;'
            f'background:{nbfc_color};margin-right:6px;"></span>'
            f'{row["name"]}</td>'
        )
        snap_html += f'<tr>{name_cell}'
        for cat in ['Promoter', 'FII', 'DII', 'Public']:
            v = row[cat]
            mn, mx = col_stats[cat]
            if v is not None and mx > mn:
                intensity = (v - mn) / (mx - mn)
            else:
                intensity = 0
            hc = cat_header_colors[cat]
            # Parse r,g,b from hex
            hx = hc.lstrip('#')
            r0, g0, b0 = int(hx[0:2], 16), int(hx[2:4], 16), int(hx[4:6], 16)
            bg_alpha = 0.07 + intensity * 0.23
            fw = '700' if intensity > 0.65 else '400'
            cell_bg = f'rgba({r0},{g0},{b0},{bg_alpha:.2f})'
            v_str = f"{v:.2f}%" if v is not None else "—"
            snap_html += f'<td style="padding:8px 12px;text-align:right;background:{cell_bg};font-weight:{fw};font-family:JetBrains Mono,monospace;font-size:11.5px;">{v_str}</td>'
        snap_html += '</tr>'

    snap_html += '</tbody></table>'
    st.markdown(snap_html, unsafe_allow_html=True)

    st.markdown('<div style="height:12px;"></div>', unsafe_allow_html=True)

    # ── Section 2 — Per-NBFC Selector ─────────────────────────────────────────
    st.markdown("""
    <div class="section-label">Select NBFC
      <span class="section-label-sub" style="margin-left:8px;">Detailed 8-quarter view below</span>
    </div>
    """, unsafe_allow_html=True)

    sh_sel = st.radio(
        "NBFC",
        available_sh,
        horizontal=True,
        key="sh_nbfc_sel",
        label_visibility="collapsed",
    )

    if sh_sel and sh_sel in SHAREHOLDING:
        sh_data = SHAREHOLDING[sh_sel]
        cat_pct = sh_data.get('category_pct', {})
        named_ents = sh_data.get('named_entities', [])

        # ── Section 3 — Summary Cards ──────────────────────────────────────────
        sum_cols = st.columns(4)
        for ci, cat in enumerate(['Promoter', 'FII', 'DII', 'Public']):
            vals = cat_pct.get(cat, [None] * 8)
            lv = sh_latest(vals)
            _, delta_html = sh_delta_str(vals)
            cat_color = CATEGORY_COLORS.get(cat, '#94a3b8')
            lv_str = f"{lv:.2f}%" if lv is not None else "—"
            with sum_cols[ci]:
                st.markdown(f"""
                <div class="sh-summary-card" style="border-top-color:{cat_color};">
                  <div class="sh-summary-label">{cat}</div>
                  <div class="sh-summary-num">{lv_str}</div>
                  <div class="sh-summary-delta">{delta_html}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown('<div style="height:12px;"></div>', unsafe_allow_html=True)

        # ── Section 4 — ≥1% Shareholders Table ────────────────────────────────
        n_q = len(SH_QUARTERS)
        st.markdown(f"""
        <div class="section-label">≥1% Shareholders
          <span class="section-label-sub" style="margin-left:8px;">
            {sh_sel} · Q4FY24 – Q3FY26 · green = building · red = reducing ·
            ● = new entry · ○ = exited · shaded rows = category totals
          </span>
        </div>
        """, unsafe_allow_html=True)

        # Build full-width table
        n_total_cols = 2 + n_q + 1  # name + category + quarters + trend

        header_html = '<thead><tr>'
        header_html += '<th style="background:#0a2540;color:white;padding:7px 10px;text-align:left;font-size:10.5px;min-width:180px;">Shareholder</th>'
        header_html += '<th style="background:#0a2540;color:white;padding:7px 10px;text-align:left;font-size:10.5px;">Category</th>'
        for q in SH_QUARTERS:
            header_html += f'<th style="background:#0a2540;color:white;padding:7px 10px;text-align:right;font-size:10.5px;">{q}</th>'
        header_html += '<th style="background:#0a2540;color:white;padding:7px 10px;text-align:left;font-size:10.5px;">Trend</th>'
        header_html += '</tr></thead>'

        # Group entities
        prom_ents = [e for e in named_ents if e.get('category') == 'Promoter']
        fii_ents  = [e for e in named_ents if e.get('category') == 'FII']
        dii_mf_ents  = [e for e in named_ents if e.get('category') == 'DII – MF']
        dii_ins_ents = [e for e in named_ents if e.get('category') == 'DII – Insurance']
        dii_pen_ents = [e for e in named_ents if e.get('category') == 'DII – Pension']
        dii_oth_ents = [e for e in named_ents if e.get('category') == 'DII – Other']
        pub_ents  = [e for e in named_ents if e.get('category') == 'Public']

        body_html = '<tbody>'

        def _group_hdr_full(label):
            return (
                f'<tr style="background:#f1f5f9;">'
                f'<td style="font-size:10px;font-weight:700;text-transform:uppercase;color:#64748b;'
                f'letter-spacing:0.06em;padding:5px 10px;" colspan="{n_total_cols}">{label}</td>'
                f'</tr>'
            )

        # Promoter section
        if prom_ents:
            body_html += _group_hdr_full("Promoter")
            body_html += _entity_rows("Promoter", prom_ents, n_q)
        prom_totals = cat_pct.get('Promoter', [None] * n_q)
        body_html += _total_row("Promoter Total", prom_totals, TOTAL_BG["Promoter"])

        # FII section
        if fii_ents:
            body_html += _group_hdr_full("FII / FPI")
            body_html += _entity_rows("FII", fii_ents, n_q)
        fii_totals = cat_pct.get('FII', [None] * n_q)
        body_html += _total_row("FII Total", fii_totals, TOTAL_BG["FII"])

        # DII sub-categories
        for dii_cat_label, dii_ents_list in [
            ("DII – MF", dii_mf_ents),
            ("DII – Insurance", dii_ins_ents),
            ("DII – Pension", dii_pen_ents),
            ("DII – Other", dii_oth_ents),
        ]:
            if dii_ents_list:
                body_html += _group_hdr_full(dii_cat_label)
                body_html += _entity_rows(dii_cat_label, dii_ents_list, n_q)
        dii_totals = cat_pct.get('DII', [None] * n_q)
        body_html += _total_row("DII Total", dii_totals, TOTAL_BG["DII"])

        # Public section
        if pub_ents:
            body_html += _group_hdr_full("Public")
            body_html += _entity_rows("Public", pub_ents, n_q)
        pub_totals = cat_pct.get('Public', [None] * n_q)
        body_html += _total_row("Public Total", pub_totals, TOTAL_BG["Public"])

        body_html += '</tbody>'

        table_html = f'<table class="sh-table">{header_html}{body_html}</table>'
        st.markdown(table_html, unsafe_allow_html=True)

        st.markdown("""
        <div class="metric-note">
          ● = new entry this window · ○ = position exited after this quarter ·
          Cell colour = direction vs prior quarter ·
          Shaded total rows include all holders (named + sub-1%)
        </div>
        """, unsafe_allow_html=True)


# ── FOOTER ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="font-size:10px;color:#94a3b8;font-family:'JetBrains Mono',monospace;
            border-top:1px solid #e2e8f0;padding-top:8px;margin-top:14px;">
    Data: Screener.in investor presentations · Yahoo Finance (market prices) ·
    Q4FY24–Q3FY26 (8 quarters) · 9 NBFCs · Last refreshed: Feb 2026
</div>
""", unsafe_allow_html=True)

