import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import yfinance as yf
import pytz
from nbfc_data_cache import NBFC_TIMESERIES, QUARTERS as CACHE_QUARTERS, METRIC_LABELS
from nbfc_ai_data import NBFC_AI_INITIATIVES, FUNCTION_TAXONOMY

# ─── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NBFC Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── GLOBAL STYLES ─────────────────────────────────────────────────────────────
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

    .main { background: #eef0f4; font-family: 'Inter', sans-serif; }
    .block-container { padding: 2.8rem 1.6rem 0.6rem 1.6rem !important; max-width: 1600px; }
    div[data-testid="stVerticalBlock"] > div { gap: 0 !important; }

    .section-label {
        font-size: 12px; font-weight: 700; letter-spacing: 0.08em;
        text-transform: uppercase; color: #64748b;
        border-left: 2px solid #0284c7; padding-left: 7px;
        margin: 12px 0 8px 0; display: block;
    }
    .section-label-sub {
        font-size: 10.5px; font-weight: 400; letter-spacing: 0.03em;
        color: #94a3b8; margin-left: 6px; text-transform: none;
    }
    .tab-intro {
        background: white; border-left: 4px solid #0284c7;
        padding: 12px 18px; border-radius: 5px; margin-bottom: 12px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.07);
    }
    .tab-intro-title { font-size: 17px; font-weight: 700; color: #0a2540; display: block; }
    .tab-intro-sub   { font-size: 12.5px; color: #94a3b8; display: block; margin-top: 3px; }

    .metric-note {
        background: #f8fafc; border-radius: 4px; padding: 6px 12px;
        border-left: 2px solid #cbd5e1; font-size: 10.5px; color: #64748b;
        margin-top: 2px; margin-bottom: 8px;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0; background: white; padding: 0 8px; border-radius: 0;
        border-bottom: 1px solid #e2e8f0;
        box-shadow: 0 1px 4px rgba(0,0,0,0.05); margin-bottom: 14px;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent; border-radius: 0; color: #64748b;
        font-weight: 500; padding: 10px 18px; font-size: 13.5px;
        border-bottom: 2px solid transparent; margin-bottom: -1px;
    }
    .stTabs [aria-selected="true"] {
        background: transparent !important; color: #0284c7 !important;
        border-bottom: 2px solid #0284c7 !important; font-weight: 600 !important;
    }

    /* Stock cards */
    .ticker-card {
        background: white; border-radius: 5px; padding: 12px 14px 10px 14px;
        border-top: 3px solid #0284c7; box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        height: 112px; box-sizing: border-box;
    }
    .ticker-name-sm {
        font-size: 17px; font-weight: 600; color: #0a2540;
        white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
    }
    .ticker-sym {
        font-family: 'JetBrains Mono', monospace; font-size: 10px;
        font-weight: 400; color: #94a3b8; letter-spacing: 0.05em; margin-top: 2px;
    }
    .ticker-price {
        font-family: 'JetBrains Mono', monospace; font-size: 24px;
        font-weight: 700; color: #0a2540; line-height: 1.1;
    }
    .ticker-pos { color: #16a34a; font-size: 14px; font-weight: 600; }
    .ticker-neg { color: #dc2626; font-size: 14px; font-weight: 600; }
    .ticker-meta {
        font-size: 10px; color: #94a3b8; margin-top: 5px;
        border-top: 1px solid #f1f5f9; padding-top: 4px;
        font-family: 'JetBrains Mono', monospace;
    }

    /* Period buttons */
    .stButton button {
        background: white; border: 1px solid #e2e8f0; color: #64748b;
        border-radius: 4px; padding: 3px 10px; font-weight: 500;
        font-size: 11.5px; height: 28px !important; line-height: 1 !important;
    }
    .stButton button:hover { border-color: #0284c7; color: #0284c7; background: #f0f9ff; }

    .stCheckbox { margin-bottom: -2px; }
    .stCheckbox label { font-size: 13.5px; color: #475569; }
    .stCaption p { font-size: 10.5px !important; color: #94a3b8 !important; margin: 0 !important; }
    hr { margin: 8px 0; border-color: #e2e8f0; }
    .stAlert { padding: 8px 12px !important; font-size: 12px; border-radius: 5px; }

    /* Rankings table */
    .rank-table { border-collapse: collapse; width: 100%; font-size: 12px; font-family: 'Inter', sans-serif; }
    .rank-table th {
        background: #0a2540; color: white; padding: 8px 10px;
        text-align: right; font-size: 10.5px; font-weight: 600;
        letter-spacing: 0.04em; white-space: nowrap;
    }
    .rank-table th:first-child { text-align: left; }
    .rank-table td { padding: 7px 10px; border-bottom: 1px solid #f1f5f9; text-align: right; }
    .rank-table td:first-child { text-align: left; font-weight: 600; color: #0a2540; }
    .rank-table tr:hover td { background: #f8fafc; }

    /* AI Bulletin */
    .ai-nbfc-header {
        background: white; border-left: 4px solid var(--nbfc-color, #0284c7);
        padding: 10px 16px; border-radius: 5px; margin: 18px 0 6px 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.07);
        display: flex; align-items: center; justify-content: space-between;
    }
    .ai-nbfc-name {
        font-size: 15px; font-weight: 700; color: #0a2540;
    }
    .ai-nbfc-count {
        font-size: 11px; font-weight: 600; color: white;
        background: var(--nbfc-color, #0284c7);
        border-radius: 12px; padding: 2px 10px; letter-spacing: 0.03em;
    }
    .ai-impact {
        font-size: 12px; color: #0a2540; font-weight: 500;
        background: #f0f9ff; border-left: 3px solid #0284c7;
        padding: 7px 12px; border-radius: 3px; margin: 8px 0;
    }
    .ai-desc {
        font-size: 12.5px; color: #374151; line-height: 1.65;
        margin: 8px 0;
    }
    .ai-func-tag {
        display: inline-block; font-size: 10px; font-weight: 600;
        letter-spacing: 0.04em; color: #0284c7;
        background: #e0f2fe; border-radius: 10px;
        padding: 2px 9px; margin: 2px 3px 2px 0;
    }
    .ai-meta-row {
        display: flex; align-items: center; gap: 10px;
        margin-top: 10px; padding-top: 8px; border-top: 1px solid #f1f5f9;
        font-size: 11px; color: #64748b; flex-wrap: wrap;
    }
    .ai-date-badge {
        font-family: 'JetBrains Mono', monospace; font-size: 10.5px;
        color: #64748b; background: #f1f5f9; padding: 2px 8px; border-radius: 3px;
    }
    .ai-source-link {
        font-size: 11px; color: #0284c7; text-decoration: none;
    }
    .ai-nbfc-badge {
        display: inline-block; font-size: 10.5px; font-weight: 700;
        color: white; border-radius: 4px; padding: 2px 9px;
        letter-spacing: 0.02em;
    }
    .ai-stat-card {
        background: white; border-radius: 5px; padding: 14px 18px;
        border-top: 3px solid #0284c7; box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        text-align: center;
    }
    .ai-stat-num {
        font-size: 28px; font-weight: 700; color: #0a2540;
        font-family: 'JetBrains Mono', monospace;
    }
    .ai-stat-label {
        font-size: 10.5px; font-weight: 600; color: #94a3b8;
        text-transform: uppercase; letter-spacing: 0.07em; margin-top: 3px;
    }
    .ai-timeline-dot {
        width: 10px; height: 10px; border-radius: 50%;
        display: inline-block; margin-right: 6px; vertical-align: middle;
    }
    </style>
""", unsafe_allow_html=True)

# ─── NBFC REGISTRY ─────────────────────────────────────────────────────────────

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

# Map display name → cache key (only Chola differs)
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
Q_LABELS = CACHE_QUARTERS  # ["Q4FY24", ..., "Q3FY26"]

# ─── DATA HELPERS ──────────────────────────────────────────────────────────────

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

# ─── CHART FACTORY ─────────────────────────────────────────────────────────────

def make_trend_chart(
    metric: str,
    selected: list,
    title: str,
    ylabel: str,
    fmt: str = 'pct',       # 'pct' | 'cr' | 'ratio' | 'inr'
    note: str = None,
    height: int = 420,
    lower_is_better: bool = False,
):
    """Line-chart for a single metric across selected NBFCs over 8 quarters."""
    data = get_series(metric)
    fig = go.Figure()

    series = []
    for name in selected:
        vals = data.get(name, [None] * 8)
        confirmed = [v for v in vals if v is not None]
        if not confirmed:
            continue
        last_v, last_i = latest_val(vals)
        series.append({
            'name': name, 'values': vals,
            'last': last_v, 'last_i': last_i,
            'color': COLORS[name],
        })

    # Sort descending by last value so label positions match visual top→bottom order
    series.sort(key=lambda x: x['last'] if x['last'] is not None else 0,
                reverse=True)

    if fmt == 'cr':
        hover_tmpl = lambda n: f"<b>{n}</b>  ₹%{{y:,.0f}} Cr<extra></extra>"
        val_str_fn = lambda v: f"₹{v:,.0f} Cr"
    elif fmt == 'inr':
        hover_tmpl = lambda n: f"<b>{n}</b>  ₹%{{y:,.1f}}<extra></extra>"
        val_str_fn = lambda v: f"₹{v:,.1f}"
    elif fmt == 'ratio':
        hover_tmpl = lambda n: f"<b>{n}</b>  %{{y:.2f}}x<extra></extra>"
        val_str_fn = lambda v: f"{v:.2f}x"
    else:
        hover_tmpl = lambda n: f"<b>{n}</b>  %{{y:.2f}}%<extra></extra>"
        val_str_fn = lambda v: f"{v:.2f}%"

    for s in series:
        fig.add_trace(go.Scatter(
            x=Q_LABELS, y=s['values'],
            name=s['name'],
            mode='lines+markers',
            connectgaps=False,
            line=dict(color=s['color'], width=2.5),
            marker=dict(size=7, color=s['color']),
            hovertemplate=hover_tmpl(s['name']),
        ))

    # Right-side labels (staggered)
    label_y = [s['last'] for s in series]
    all_vals = [v for s in series for v in s['values'] if v is not None]
    y_range  = (max(all_vals) - min(all_vals)) if len(all_vals) > 1 else 1
    GAP      = max(y_range * 0.11, 0.2)

    for i in range(1, len(label_y)):
        if label_y[i - 1] - label_y[i] < GAP:
            label_y[i] = label_y[i - 1] - GAP
    for i in range(len(label_y) - 2, -1, -1):
        if label_y[i] - label_y[i + 1] < GAP:
            label_y[i] = label_y[i + 1] + GAP

    for i, s in enumerate(series):
        x_anchor = Q_LABELS[s['last_i']]
        if abs(s['last'] - label_y[i]) > GAP * 0.3:
            fig.add_shape(type='line',
                x0=x_anchor, x1=x_anchor,
                y0=s['last'], y1=label_y[i],
                line=dict(color=s['color'], width=1, dash='dot'),
                xref='x', yref='y')
        fig.add_annotation(
            x=x_anchor, y=label_y[i],
            text=f"<b>{s['name']}</b>  {val_str_fn(s['last'])}",
            showarrow=False, xanchor='left', xshift=12,
            font=dict(size=10.5, color=s['color']),
            bgcolor='rgba(255,255,255,0.95)',
            bordercolor=s['color'], borderwidth=1, borderpad=3,
        )

    title_html = f'<span style="color:#0a2540;font-weight:700;font-size:15px">{title}</span>'
    if note:
        title_html += f'<br><span style="color:#94a3b8;font-size:10px">{note}</span>'

    fig.update_layout(
        title=dict(text=title_html, font=dict(family='Inter'), x=0, xref='paper'),
        yaxis_title=ylabel,
        template='plotly_white', height=height,
        hovermode='x unified', showlegend=False,
        plot_bgcolor='white', paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=55, r=230, t=55, b=45),
        font=dict(family='Inter', color='#1a3a52'),
        hoverlabel=dict(bgcolor='white', bordercolor='#cbd5e1',
                        font=dict(family='Inter', size=12)),
    )
    fig.update_xaxes(showgrid=True, gridcolor='#f1f5f9', showline=True,
                     linecolor='#cbd5e1', tickfont=dict(size=11, color='#475569'))
    fig.update_yaxes(showgrid=True, gridcolor='#f1f5f9', showline=True,
                     linecolor='#cbd5e1', tickfont=dict(size=11, color='#475569'))
    return fig


def make_bar_chart(
    metric: str,
    selected: list,
    title: str,
    ylabel: str,
    fmt: str = 'cr',
    height: int = 380,
):
    """Grouped bar chart for absolute value metrics (AUM, PAT)."""
    data = get_series(metric)
    fig = go.Figure()
    for name in selected:
        vals = data.get(name, [None] * 8)
        fig.add_trace(go.Bar(
            x=Q_LABELS, y=vals,
            name=name,
            marker_color=COLORS[name],
            opacity=0.85,
            hovertemplate=(
                f"<b>{name}</b><br>%{{x}}<br>"
                + ("₹%{y:,.0f} Cr" if fmt == 'cr' else "%{y:.2f}")
                + "<extra></extra>"
            ),
        ))

    fig.update_layout(
        title=dict(
            text=f'<span style="color:#0a2540;font-weight:700;font-size:15px">{title}</span>',
            font=dict(family='Inter'), x=0, xref='paper'),
        yaxis_title=ylabel,
        barmode='group',
        template='plotly_white', height=height,
        hovermode='x unified', showlegend=True,
        plot_bgcolor='white', paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=55, r=20, t=55, b=90),
        font=dict(family='Inter', color='#1a3a52'),
        legend=dict(orientation='h', yanchor='top', y=-0.18,
                    xanchor='center', x=0.5, font=dict(size=10.5)),
    )
    fig.update_xaxes(showgrid=False, showline=True, linecolor='#cbd5e1',
                     tickfont=dict(size=11, color='#475569'),
                     range=[-0.5, len(Q_LABELS) - 0.5])   # remove trailing whitespace
    fig.update_yaxes(showgrid=True, gridcolor='#f1f5f9', showline=True,
                     linecolor='#cbd5e1', tickfont=dict(size=11, color='#475569'))
    return fig


def make_yoy_chart(
    metric: str,
    selected: list,
    title: str,
    height: int = 310,
):
    """Line chart showing YoY growth for the last 4 quarters.

    Pairs: Q4FY25/Q4FY24 · Q1FY26/Q1FY25 · Q2FY26/Q2FY25 · Q3FY26/Q3FY25
    Growth is set to None when the base-year value is zero or negative
    (e.g. loss quarters) to avoid meaningless / inverted percentages.
    """
    data = get_series(metric)

    YOY_LABELS = ["Q4FY25", "Q1FY26", "Q2FY26", "Q3FY26"]
    YOY_PAIRS  = [(4, 0), (5, 1), (6, 2), (7, 3)]   # (current_idx, prior_year_idx)

    series = []
    for name in selected:
        vals = data.get(name, [None] * 8)
        growth = []
        for cur_i, py_i in YOY_PAIRS:
            cur = vals[cur_i]
            py  = vals[py_i]
            if cur is not None and py is not None and py > 0:
                growth.append(round((cur - py) / py * 100, 1))
            elif cur is None or py is None:
                growth.append(None)   # data missing → keep gap
            else:
                growth.append(0)      # base ≤ 0 → 0% for line continuity
        confirmed = [g for g in growth if g is not None]
        if not confirmed:
            continue
        last_g = next((g for g in reversed(growth) if g is not None), None)
        series.append({
            'name': name, 'growth': growth,
            'last': last_g, 'color': COLORS[name],
        })

    # Sort descending so label order matches visual top→bottom
    series.sort(key=lambda x: x['last'] if x['last'] is not None else -9999, reverse=True)

    fig = go.Figure()
    for s in series:
        fig.add_trace(go.Scatter(
            x=YOY_LABELS, y=s['growth'],
            name=s['name'],
            mode='lines+markers',
            connectgaps=False,
            line=dict(color=s['color'], width=2.5),
            marker=dict(size=8, color=s['color']),
            hovertemplate=f"<b>{s['name']}</b><br>%{{x}}<br>YoY: %{{y:+.1f}}%<extra></extra>",
        ))

    # Staggered right-side labels
    label_y = [s['last'] for s in series]
    all_vals = [g for s in series for g in s['growth'] if g is not None]
    if all_vals:
        y_range = max(all_vals) - min(all_vals) if len(all_vals) > 1 else 10
        GAP = max(y_range * 0.14, 2.0)
        for i in range(1, len(label_y)):
            if label_y[i - 1] is not None and label_y[i] is not None:
                if label_y[i - 1] - label_y[i] < GAP:
                    label_y[i] = label_y[i - 1] - GAP
        for i in range(len(label_y) - 2, -1, -1):
            if label_y[i] is not None and label_y[i + 1] is not None:
                if label_y[i] - label_y[i + 1] < GAP:
                    label_y[i] = label_y[i + 1] + GAP
        for i, s in enumerate(series):
            if s['last'] is None or label_y[i] is None:
                continue
            sign = '+' if s['last'] >= 0 else ''
            fig.add_annotation(
                x=YOY_LABELS[-1], y=label_y[i],
                text=f"<b>{s['name']}</b>  {sign}{s['last']:.1f}%",
                showarrow=False, xanchor='left', xshift=12,
                font=dict(size=10.5, color=s['color']),
                bgcolor='rgba(255,255,255,0.95)',
                bordercolor=s['color'], borderwidth=1, borderpad=3,
            )

    # y = 0 reference line
    fig.add_hline(y=0, line_dash='dot', line_color='#94a3b8', line_width=1)

    fig.update_layout(
        title=dict(
            text=f'<span style="color:#0a2540;font-weight:700;font-size:15px">{title}</span>',
            font=dict(family='Inter'), x=0, xref='paper'),
        yaxis_title='YoY Growth (%)',
        template='plotly_white', height=height,
        hovermode='x unified', showlegend=False,
        plot_bgcolor='white', paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=55, r=155, t=55, b=45),
        font=dict(family='Inter', color='#1a3a52'),
        hoverlabel=dict(bgcolor='white', bordercolor='#cbd5e1',
                        font=dict(family='Inter', size=12)),
    )
    fig.update_xaxes(showgrid=True, gridcolor='#f1f5f9', showline=True,
                     linecolor='#cbd5e1', tickfont=dict(size=11, color='#475569'))
    fig.update_yaxes(showgrid=True, gridcolor='#f1f5f9', showline=True,
                     linecolor='#cbd5e1', tickfont=dict(size=11, color='#475569'),
                     ticksuffix='%')
    return fig


def make_qoq_chart(
    metric: str,
    selected: list,
    title: str,
    height: int = 310,
):
    """Line chart showing QoQ growth for Q1FY25 through Q3FY26 (7 data points).

    Growth set to None when the base quarter is zero or negative.
    """
    data = get_series(metric)

    QOQ_LABELS = ["Q1FY25", "Q2FY25", "Q3FY25", "Q4FY25", "Q1FY26", "Q2FY26", "Q3FY26"]
    QOQ_PAIRS  = [(1,0),(2,1),(3,2),(4,3),(5,4),(6,5),(7,6)]

    series = []
    for name in selected:
        vals = data.get(name, [None] * 8)
        growth = []
        for cur_i, pr_i in QOQ_PAIRS:
            cur = vals[cur_i]
            pr  = vals[pr_i]
            if cur is not None and pr is not None and pr > 0:
                growth.append(round((cur - pr) / pr * 100, 1))
            elif cur is None or pr is None:
                growth.append(None)   # data missing → keep gap
            else:
                growth.append(0)      # base ≤ 0 → 0% for line continuity
        confirmed = [g for g in growth if g is not None]
        if not confirmed:
            continue
        last_g = next((g for g in reversed(growth) if g is not None), None)
        series.append({
            'name': name, 'growth': growth,
            'last': last_g, 'color': COLORS[name],
        })

    series.sort(key=lambda x: x['last'] if x['last'] is not None else -9999, reverse=True)

    fig = go.Figure()
    for s in series:
        fig.add_trace(go.Scatter(
            x=QOQ_LABELS, y=s['growth'],
            name=s['name'],
            mode='lines+markers',
            connectgaps=False,
            line=dict(color=s['color'], width=2.5),
            marker=dict(size=7, color=s['color']),
            hovertemplate=f"<b>{s['name']}</b><br>%{{x}}<br>QoQ: %{{y:+.1f}}%<extra></extra>",
        ))

    # Staggered right-side labels
    label_y = [s['last'] for s in series]
    all_vals = [g for s in series for g in s['growth'] if g is not None]
    if all_vals:
        y_range = max(all_vals) - min(all_vals) if len(all_vals) > 1 else 10
        GAP = max(y_range * 0.14, 1.5)
        for i in range(1, len(label_y)):
            if label_y[i - 1] is not None and label_y[i] is not None:
                if label_y[i - 1] - label_y[i] < GAP:
                    label_y[i] = label_y[i - 1] - GAP
        for i in range(len(label_y) - 2, -1, -1):
            if label_y[i] is not None and label_y[i + 1] is not None:
                if label_y[i] - label_y[i + 1] < GAP:
                    label_y[i] = label_y[i + 1] + GAP
        for i, s in enumerate(series):
            if s['last'] is None or label_y[i] is None:
                continue
            sign = '+' if s['last'] >= 0 else ''
            fig.add_annotation(
                x=QOQ_LABELS[-1], y=label_y[i],
                text=f"<b>{s['name']}</b>  {sign}{s['last']:.1f}%",
                showarrow=False, xanchor='left', xshift=12,
                font=dict(size=10.5, color=s['color']),
                bgcolor='rgba(255,255,255,0.95)',
                bordercolor=s['color'], borderwidth=1, borderpad=3,
            )

    fig.add_hline(y=0, line_dash='dot', line_color='#94a3b8', line_width=1)

    fig.update_layout(
        title=dict(
            text=f'<span style="color:#0a2540;font-weight:700;font-size:15px">{title}</span>',
            font=dict(family='Inter'), x=0, xref='paper'),
        yaxis_title='QoQ Growth (%)',
        template='plotly_white', height=height,
        hovermode='x unified', showlegend=False,
        plot_bgcolor='white', paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=55, r=155, t=55, b=45),
        font=dict(family='Inter', color='#1a3a52'),
        hoverlabel=dict(bgcolor='white', bordercolor='#cbd5e1',
                        font=dict(family='Inter', size=12)),
    )
    fig.update_xaxes(showgrid=True, gridcolor='#f1f5f9', showline=True,
                     linecolor='#cbd5e1', tickfont=dict(size=11, color='#475569'))
    fig.update_yaxes(showgrid=True, gridcolor='#f1f5f9', showline=True,
                     linecolor='#cbd5e1', tickfont=dict(size=11, color='#475569'),
                     ticksuffix='%')
    return fig


def make_pb_chart(selected: list, height: int = 520):
    """Daily P/B ratio chart: 2-year daily price ÷ most recent quarterly BVPS.

    Quarter-end → BVPS index mapping:
      Q4FY24=0  Q1FY25=1  Q2FY25=2  Q3FY25=3
      Q4FY25=4  Q1FY26=5  Q2FY26=6  Q3FY26=7

    BVPS steps up at each quarter-end date and stays flat until the next one.
    """
    bvps_data = get_series('bvps_inr')

    # (quarter-end date, BVPS index) — sorted ascending so we can binary-search
    QUARTER_ENDS = [
        (pd.Timestamp('2024-03-31').date(), 0),
        (pd.Timestamp('2024-06-30').date(), 1),
        (pd.Timestamp('2024-09-30').date(), 2),
        (pd.Timestamp('2024-12-31').date(), 3),
        (pd.Timestamp('2025-03-31').date(), 4),
        (pd.Timestamp('2025-06-30').date(), 5),
        (pd.Timestamp('2025-09-30').date(), 6),
        (pd.Timestamp('2025-12-31').date(), 7),
    ]

    fig = go.Figure()
    series = []

    for name in selected:
        bvps_vals = bvps_data.get(name, [None] * 8)
        symbol = NBFCS[name]

        try:
            hist = fetch_stock_data(symbol, period='2y')
            if hist is None or hist.empty:
                continue

            dates, pb_vals, prices_list, bvps_list = [], [], [], []
            for dt, row in hist.iterrows():
                try:
                    price = float(row['Close'])
                    if price <= 0:
                        continue
                    date_only = pd.Timestamp(dt).date()

                    # Find the most recent quarter-end that has passed
                    bvps = None
                    for qend, idx in reversed(QUARTER_ENDS):
                        if date_only >= qend:
                            bv = bvps_vals[idx]
                            if bv is not None and bv > 0:
                                bvps = bv
                            break

                    if bvps is None:
                        continue

                    dates.append(pd.Timestamp(dt))
                    pb_vals.append(round(price / bvps, 2))
                    prices_list.append(price)
                    bvps_list.append(bvps)
                except Exception:
                    continue

            if not dates:
                continue

            last_pb = pb_vals[-1]
            series.append({
                'name': name, 'dates': dates, 'pb': pb_vals,
                'prices': prices_list, 'bvps_vals': bvps_list,
                'last': last_pb, 'color': COLORS[name],
            })
        except Exception:
            continue

    # Sort descending by latest P/B so labels match visual top→bottom
    series.sort(key=lambda x: x['last'] if x['last'] is not None else 0, reverse=True)

    for s in series:
        import numpy as _np
        _cd = _np.column_stack([s['prices'], s['bvps_vals']])
        fig.add_trace(go.Scatter(
            x=s['dates'], y=s['pb'],
            name=s['name'],
            mode='lines',
            line=dict(color=s['color'], width=2),
            customdata=_cd,
            hovertemplate=(
                f"<b>{s['name']}</b><br>"
                "%{x|%d %b %Y}<br>"
                "P/B: %{y:.2f}x &nbsp;·&nbsp; "
                "Price: ₹%{customdata[0]:,.0f} &nbsp;·&nbsp; "
                "BVPS: ₹%{customdata[1]:,.0f}"
                "<extra></extra>"
            ),
        ))

    # Staggered right-side labels
    if series:
        label_y = [s['last'] for s in series]
        all_vals = [v for s in series for v in s['pb'] if v is not None]
        if all_vals:
            y_range = max(all_vals) - min(all_vals) if len(all_vals) > 1 else 1
            GAP = max(y_range * 0.08, 0.12)
            for i in range(1, len(label_y)):
                if label_y[i - 1] - label_y[i] < GAP:
                    label_y[i] = label_y[i - 1] - GAP
            for i in range(len(label_y) - 2, -1, -1):
                if label_y[i] - label_y[i + 1] < GAP:
                    label_y[i] = label_y[i + 1] + GAP
            for i, s in enumerate(series):
                fig.add_annotation(
                    x=s['dates'][-1], y=label_y[i],
                    text=f"<b>{s['name']}</b>  {s['last']:.2f}x",
                    showarrow=False, xanchor='left', xshift=12,
                    font=dict(size=10.5, color=s['color']),
                    bgcolor='rgba(255,255,255,0.95)',
                    bordercolor=s['color'], borderwidth=1, borderpad=3,
                )

    # P/B = 1 reference line
    fig.add_hline(y=1, line_dash='dot', line_color='#94a3b8', line_width=1)

    fig.update_layout(
        title=dict(
            text='<span style="color:#0a2540;font-weight:700;font-size:15px">'
                 'Price-to-Book (P/B) Ratio — 2Y Daily</span>',
            font=dict(family='Inter'), x=0, xref='paper'),
        yaxis_title='P/B Ratio (×)',
        template='plotly_white', height=height,
        hovermode='x unified', showlegend=False,
        plot_bgcolor='white', paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=55, r=200, t=55, b=45),
        font=dict(family='Inter', color='#1a3a52'),
        hoverlabel=dict(bgcolor='white', bordercolor='#cbd5e1',
                        font=dict(family='Inter', size=12)),
    )
    fig.update_xaxes(showgrid=True, gridcolor='#f1f5f9', showline=True,
                     linecolor='#cbd5e1', tickfont=dict(size=11, color='#475569'))
    fig.update_yaxes(showgrid=True, gridcolor='#f1f5f9', showline=True,
                     linecolor='#cbd5e1', tickfont=dict(size=11, color='#475569'),
                     ticksuffix='x')
    return fig


# ─── MARKET DATA ───────────────────────────────────────────────────────────────

@st.cache_data(ttl=3600)
def fetch_stock_data(symbol, period='1y'):
    try:
        return yf.Ticker(symbol).history(period=period)
    except:
        return None


@st.cache_data(ttl=3600)
def fetch_stock_data_range(symbol, start_str, end_str):
    """Fetch daily OHLCV between start_str and end_str ('YYYY-MM-DD')."""
    try:
        return yf.Ticker(symbol).history(start=start_str, end=end_str)
    except Exception:
        return None


@st.cache_data(ttl=3600)
def fetch_shares_outstanding():
    """Returns {symbol: shares_outstanding} for all NBFCs, cached 1 hr."""
    result = {}
    for name, symbol in NBFCS.items():
        try:
            shares = yf.Ticker(symbol).fast_info.shares
            if shares and shares > 0:
                result[symbol] = int(shares)
        except Exception:
            pass
    return result


def make_mktcap_trend_chart(selected: list, height: int = 440):
    """1-year daily market cap trend in ₹ Lakh Crore (price × shares outstanding)."""
    shares_map = fetch_shares_outstanding()
    fig = go.Figure()
    series = []

    for name in selected:
        symbol = NBFCS[name]
        shares = shares_map.get(symbol)
        if not shares:
            continue
        try:
            hist = fetch_stock_data(symbol, period='1y')
            if hist is None or hist.empty:
                continue
            mktcap = (hist['Close'] * shares) / 1e12  # ₹ Lakh Crore (1 L.Cr = 1e12 INR)
            series.append({
                'name': name, 'dates': hist.index,
                'values': mktcap.values, 'color': COLORS[name],
                'last': float(mktcap.iloc[-1]),
            })
        except Exception:
            continue

    series.sort(key=lambda x: x['last'], reverse=True)

    for s in series:
        fig.add_trace(go.Scatter(
            x=s['dates'], y=s['values'], name=s['name'],
            mode='lines', line=dict(color=s['color'], width=2.5),
            hovertemplate=(
                f"<b>{s['name']}</b><br>"
                "%{x|%d %b %Y}<br>"
                "MCap: ₹%{y:.2f} L.Cr<extra></extra>"
            ),
        ))

    # Staggered right-side labels
    if series:
        label_y = [s['last'] for s in series]
        all_vals = [float(v) for s in series for v in s['values'] if not pd.isna(float(v))]
        if all_vals:
            y_range = max(all_vals) - min(all_vals) if len(all_vals) > 1 else 1
            GAP = max(y_range * 0.06, 0.05)
            for i in range(1, len(label_y)):
                if label_y[i - 1] - label_y[i] < GAP:
                    label_y[i] = label_y[i - 1] - GAP
            for i in range(len(label_y) - 2, -1, -1):
                if label_y[i] - label_y[i + 1] < GAP:
                    label_y[i] = label_y[i + 1] + GAP
        for i, s in enumerate(series):
            fig.add_trace(go.Scatter(
                x=[s['dates'][-1]], y=[s['last']],
                mode='markers', marker=dict(size=7, color=s['color']),
                showlegend=False, hoverinfo='skip',
            ))
            fig.add_annotation(
                x=s['dates'][-1], y=label_y[i],
                text=f"<b>{s['name']}</b>  ₹{s['last']:.2f} L.Cr",
                showarrow=False, xanchor='left', xshift=12,
                font=dict(size=11, color=s['color']),
                bgcolor='rgba(255,255,255,0.9)',
                bordercolor=s['color'], borderwidth=1, borderpad=4,
            )

    fig.update_layout(
        height=height,
        margin=dict(l=60, r=230, t=55, b=40),
        plot_bgcolor='white', paper_bgcolor='white',
        showlegend=False,
        font=dict(family='Inter', color='#1a3a52'),
        hoverlabel=dict(bgcolor='white', bordercolor='#cbd5e1',
                        font=dict(family='Inter', size=12)),
        xaxis=dict(showgrid=True, gridcolor='#f1f5f9', showline=True,
                   linecolor='#cbd5e1', tickfont=dict(size=11, color='#475569')),
        yaxis=dict(showgrid=True, gridcolor='#f1f5f9', showline=True,
                   linecolor='#cbd5e1', tickfont=dict(size=11, color='#475569'),
                   ticksuffix=' L.Cr',
                   title=dict(text='₹ Lakh Crore', font=dict(size=11, color='#64748b'))),
    )
    return fig


def _fetch_all_prices():
    """Batch-download all 9 tickers in one request; retry missing ones individually."""
    symbols  = list(NBFCS.values())
    name_map = {v: k for k, v in NBFCS.items()}
    rows = {}

    # --- 1. Single batch download (avoids per-ticker rate-limiting) ---
    try:
        raw = yf.download(
            symbols, period='1mo', group_by='ticker',
            auto_adjust=True, progress=False, threads=False,
        )
        if raw is not None and not raw.empty:
            for symbol in symbols:
                try:
                    df = raw[symbol] if len(symbols) > 1 else raw
                    df = df.dropna(subset=['Close'])
                    if len(df) < 2:
                        continue
                    cur  = float(df['Close'].iloc[-1])
                    prev = float(df['Close'].iloc[-2])
                    chg  = cur - prev
                    rows[symbol] = {
                        'name': name_map[symbol],
                        'symbol': symbol.replace('.NS', ''),
                        'price': cur, 'change_abs': chg,
                        'change_pct': (chg / prev) * 100,
                        'volume': int(df['Volume'].iloc[-1]) if 'Volume' in df.columns else 0,
                    }
                except Exception:
                    continue
    except Exception:
        pass

    # --- 2. Individually retry any ticker that the batch missed ---
    for symbol in [s for s in symbols if s not in rows]:
        try:
            hist = yf.Ticker(symbol).history(period='1mo')
            hist = hist.dropna(subset=['Close'])
            if len(hist) < 2:
                continue
            cur  = float(hist['Close'].iloc[-1])
            prev = float(hist['Close'].iloc[-2])
            chg  = cur - prev
            rows[symbol] = {
                'name': name_map[symbol],
                'symbol': symbol.replace('.NS', ''),
                'price': cur, 'change_abs': chg,
                'change_pct': (chg / prev) * 100,
                'volume': int(hist['Volume'].iloc[-1]) if 'Volume' in hist.columns else 0,
            }
        except Exception:
            continue

    # Enrich with current market cap from fast_info
    for symbol in list(rows.keys()):
        try:
            mc = yf.Ticker(symbol).fast_info.market_cap
            rows[symbol]['market_cap'] = int(mc) if mc and mc > 0 else None
        except Exception:
            rows[symbol]['market_cap'] = None

    # Return in NBFCS display order
    return [rows[s] for s in symbols if s in rows]


def get_current_prices():
    """Smart cache: 5 min when all 9 stocks loaded; 30 sec when partial so it retries fast."""
    import time
    now   = time.time()
    cache = st.session_state.get('_prices_cache', [])
    ts    = st.session_state.get('_prices_ts', 0)
    ttl   = 300 if len(cache) == len(NBFCS) else 30

    if cache and (now - ts) < ttl:
        return cache

    result = _fetch_all_prices()
    if result:
        st.session_state['_prices_cache'] = result
        st.session_state['_prices_ts']    = now
    return result

def create_comparison_chart(time_period, selected_stocks, start_date=None, end_date=None):
    """Indexed-to-100 performance chart.

    Pass start_date / end_date (date objects) to use a custom range;
    otherwise time_period string drives the window.
    """
    fig = go.Figure()
    use_custom = start_date is not None and end_date is not None

    DAYS_MAP = {'1W': 7, '1M': 30, '3M': 90, '6M': 180,
                '1Y': 365, '3Y': 3 * 365, '5Y': 5 * 365}

    if not use_custom:
        days = DAYS_MAP.get(time_period, 180)
        yf_period = ('5d'  if days <= 7   else
                     '1mo' if days <= 30  else
                     '3mo' if days <= 90  else
                     '1y'  if days <= 365 else '5y')

    perf = []
    for name in selected_stocks:
        try:
            if use_custom:
                df = fetch_stock_data_range(
                    NBFCS[name], str(start_date), str(end_date)
                )
            else:
                df = fetch_stock_data(NBFCS[name], period=yf_period)
                if df is not None and not df.empty:
                    end = df.index[-1]
                    df = df[df.index >= end - timedelta(days=days)]

            if df is None or df.empty or len(df) < 2:
                continue

            prices  = df['Close']
            indexed = (prices / prices.iloc[0]) * 100
            perf.append({
                'name':        name,
                'performance': float(indexed.iloc[-1]) - 100,
                'dates':       df.index,
                'values':      indexed,
                'raw_prices':  prices.values,       # actual ₹ prices for hover
                'start_price': float(prices.iloc[0]),
                'end_price':   float(prices.iloc[-1]),
                'color':       COLORS[name],
                'end_y':       float(indexed.iloc[-1]),
            })
        except Exception:
            continue

    perf.sort(key=lambda x: x['performance'], reverse=True)
    if not perf:
        return fig, None, None

    all_vals = [v for item in perf for v in item['values']]
    y_range  = (max(all_vals) - min(all_vals)) if len(all_vals) > 1 else 20
    # GAP must be a meaningful fraction of the actual y-range.
    # The old min(4.0, ...) cap caused labels to pile up on indexed charts
    # (where values run 100–450) while being fine on pct charts (0–100).
    GAP = max(4.0, y_range * 0.13)

    label_pos = [item['end_y'] for item in perf]
    for i in range(1, len(label_pos)):
        if label_pos[i - 1] - label_pos[i] < GAP:
            label_pos[i] = label_pos[i - 1] - GAP
    for i in range(len(label_pos) - 2, -1, -1):
        if label_pos[i] - label_pos[i + 1] < GAP:
            label_pos[i] = label_pos[i + 1] + GAP

    for i, item in enumerate(perf):
        fig.add_trace(go.Scatter(
            x=item['dates'], y=item['values'],
            name=item['name'],
            line=dict(color=item['color'], width=2.5), mode='lines',
            customdata=item['raw_prices'],
            hovertemplate=(
                f"<b>{item['name']}</b><br>"
                "%{x|%d %b %Y}<br>"
                "Index: %{y:.1f} &nbsp;·&nbsp; ₹%{customdata:,.0f}"
                "<extra></extra>"
            ),
        ))
        fig.add_trace(go.Scatter(
            x=[item['dates'][-1]], y=[item['end_y']],
            mode='markers', marker=dict(size=7, color=item['color']),
            showlegend=False, hoverinfo='skip',
        ))
        fig.add_annotation(
            x=item['dates'][-1], y=label_pos[i],
            text=(
                f"<b>{item['name']}</b>  {item['performance']:+.1f}%<br>"
                f"₹{item['start_price']:,.0f} → ₹{item['end_price']:,.0f}"
            ),
            showarrow=False, xanchor='left', xshift=12,
            font=dict(size=10.5, color=item['color']),
            bgcolor='rgba(255,255,255,0.92)',
            bordercolor=item['color'], borderwidth=1, borderpad=4,
        )

    period_label = 'Custom Range' if use_custom else time_period
    fig.update_layout(
        title=dict(
            text=f'<span style="color:#0a2540;font-weight:700;font-size:17px">'
                 f'Performance Comparison — {period_label} (Indexed to 100)</span>',
            font=dict(family='Inter'), x=0),
        template='plotly_white', height=520, hovermode='x unified', showlegend=False,
        plot_bgcolor='white', paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=60, r=220, t=60, b=50), font=dict(family='Inter', color='#1a3a52'),
        hoverlabel=dict(bgcolor='white', bordercolor='#cbd5e1',
                        font=dict(family='Inter', size=12)),
    )
    # Expand y-axis so labels pushed outside the data range remain visible
    pad     = y_range * 0.06
    y_lo    = min(min(all_vals), min(label_pos)) - pad
    y_hi    = max(max(all_vals), max(label_pos)) + pad

    fig.update_xaxes(showgrid=True, gridcolor='#f1f5f9', showline=True, linecolor='#cbd5e1')
    fig.update_yaxes(range=[y_lo, y_hi],
                     showgrid=True, gridcolor='#f1f5f9', showline=True, linecolor='#cbd5e1')
    return fig, perf[0]['dates'][0], perf[0]['dates'][-1]

# ─── RANKINGS TABLE ────────────────────────────────────────────────────────────

def build_rankings_table():
    """Returns a Plotly table with all 9 NBFCs at Q3FY26 (last available quarter)."""
    METRICS = [
        ('aum_cr',                'AUM (₹ Cr)',   'cr',    False),
        ('pat_cr',                'PAT (₹ Cr)',   'cr',    False),
        ('gnpa_pct',              'GNPA %',       'pct',   True ),
        ('nnpa_pct',              'NNPA %',       'pct',   True ),
        ('nim_pct',               'NIM %',        'pct',   False),
        ('roa_pct',               'ROA %',        'pct',   False),
        ('roe_pct',               'ROE %',        'pct',   False),
        ('cost_of_borrowing_pct', 'CoB %',        'pct',   True ),
        ('d_e_ratio',             'D/E',          'ratio', True ),
        ('car_pct',               'CAR %',        'pct',   False),
        ('bvps_inr',              'BVPS (₹)',     'bvps',  False),
    ]

    Q_IDX = 7  # Q3FY26 index
    data = {}
    for metric, _, _, _ in METRICS:
        data[metric] = get_series(metric)

    rows = []
    for disp_name in DISPLAY_NAMES:
        row = {'NBFC': disp_name}
        for metric, col_label, fmt, _ in METRICS:
            v = data[metric][disp_name][Q_IDX]
            if v is None:
                row[col_label] = '—'
            elif fmt == 'cr':
                row[col_label] = f"₹{v:,.0f}"
            elif fmt == 'bvps':
                row[col_label] = f"₹{v:,.0f}"
            elif fmt == 'ratio':
                row[col_label] = f"{v:.2f}x"
            else:
                row[col_label] = f"{v:.2f}%"
        rows.append(row)

    df = pd.DataFrame(rows)

    # Color cells: green = good, red = bad, grey = missing
    def color_col(values_raw, lower_is_better, fmt):
        numeric = []
        for v in values_raw:
            if v == '—':
                numeric.append(None)
            else:
                try:
                    numeric.append(float(v.replace('₹','').replace(',','').replace('%','').replace('x','')))
                except:
                    numeric.append(None)
        filled = [v for v in numeric if v is not None]
        if len(filled) < 2:
            return ['rgba(248,250,252,0.7)'] * len(values_raw)
        mn, mx = min(filled), max(filled)
        colors = []
        for v in numeric:
            if v is None:
                colors.append('rgba(241,245,249,0.5)')
                continue
            if mx == mn:
                colors.append('rgba(248,250,252,0.7)')
                continue
            t = (v - mn) / (mx - mn)  # 0=min, 1=max
            if lower_is_better:
                t = 1 - t  # invert: low = good = green
            # Piecewise red(0) → yellow(0.5) → green(1)
            if t <= 0.5:
                s = t * 2
                r = int(220 + s * (255 - 220))   # 220 → 255
                g = int(60  + s * (215 - 60))    # 60  → 215
                b = int(60  + s * (50  - 60))    # 60  → 50
            else:
                s = (t - 0.5) * 2
                r = int(255 + s * (60  - 255))   # 255 → 60
                g = int(215 + s * (190 - 215))   # 215 → 190
                b = int(50  + s * (80  - 50))    # 50  → 80
            colors.append(f'rgba({r},{g},{b},0.35)')
        return colors

    col_labels = ['NBFC'] + [m[1] for m in METRICS]
    cell_values = [df[c].tolist() for c in col_labels]

    fill_colors = [['rgba(240,249,255,0.6)'] * len(DISPLAY_NAMES)]  # NBFC col
    for metric, col_label, fmt, lib in METRICS:
        raw = df[col_label].tolist()
        fill_colors.append(color_col(raw, lib, fmt))

    header_vals = [f'<b>{h}</b>' for h in col_labels]

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
            values=cell_values,
            fill_color=fill_colors,
            font=dict(color='#1a3a52', family='Inter', size=11.5),
            align=['left'] + ['right'] * len(METRICS),
            height=30,
        ),
    )])
    fig.update_layout(
        margin=dict(l=0, r=0, t=10, b=0),
        height=380,
        paper_bgcolor='rgba(0,0,0,0)',
    )
    return fig

# ─── DEEP DIVE MINI CHARTS ─────────────────────────────────────────────────────

def make_deep_dive(nbfc_disp: str):
    """4×3 grid of mini line charts for all 12 metrics for one NBFC."""
    cache = CACHE_KEY[nbfc_disp]
    metrics_grid = [
        ('aum_cr',                'AUM (₹ Cr)',          'cr'   ),
        ('pat_cr',                'PAT (₹ Cr)',          'cr'   ),
        ('gnpa_pct',              'GNPA %',              'pct'  ),
        ('nnpa_pct',              'NNPA %',              'pct'  ),
        ('pcr_pct',               'PCR %',               'pct'  ),
        ('nim_pct',               'NIM %',               'pct'  ),
        ('roa_pct',               'ROA %',               'pct'  ),
        ('roe_pct',               'ROE %',               'pct'  ),
        ('cost_of_borrowing_pct', 'Cost of Borrowing %', 'pct'  ),
        ('d_e_ratio',             'D/E Ratio',           'ratio'),
        ('car_pct',               'CAR %',               'pct'  ),
        ('bvps_inr',              'BVPS (₹)',            'bvps' ),
    ]
    fig = make_subplots(
        rows=4, cols=3,
        subplot_titles=[m[1] for m in metrics_grid],
        vertical_spacing=0.12, horizontal_spacing=0.07,
    )
    color = COLORS[nbfc_disp]

    def _fmt(v, fmt):
        """Format a single value for the end-of-line label."""
        if v is None:
            return ''
        if fmt == 'cr':
            if v >= 1_00_000:
                return f'₹{v / 1_00_000:.1f}L Cr'
            elif v >= 1_000:
                return f'₹{v / 1_000:.0f}K Cr'
            else:
                return f'₹{v:.0f} Cr'
        if fmt == 'pct':
            return f'{v:.1f}%'
        if fmt == 'ratio':
            return f'{v:.2f}x'
        if fmt == 'bvps':
            return f'₹{v:,.0f}'
        return f'{v:.1f}'

    # Collect data-legend annotations to add after subplot-title font update
    pending_annotations = []

    for idx, (metric, label, fmt) in enumerate(metrics_grid):
        row = idx // 3 + 1
        col = idx %  3 + 1
        vals = NBFC_TIMESERIES[cache][metric]
        has_data = any(v is not None for v in vals)

        if has_data:
            # Index of the last non-None point → that gets the callout legend
            last_idx = next(
                (i for i in range(len(vals) - 1, -1, -1) if vals[i] is not None),
                None,
            )
            # Larger marker at the last data point to anchor the callout
            marker_sizes = [8 if i == last_idx else 5 for i in range(len(vals))]
            fig.add_trace(go.Scatter(
                x=Q_LABELS, y=vals,
                mode='lines+markers',
                connectgaps=False,
                line=dict(color=color, width=2),
                marker=dict(size=marker_sizes, color=color),
                showlegend=False,
                hovertemplate=f"<b>{label}</b><br>%{{x}}<br>%{{y}}<extra></extra>",
            ), row=row, col=col)

            # Build xref/yref for this subplot's axes
            axis_num = idx + 1
            xref = 'x' if axis_num == 1 else f'x{axis_num}'
            yref = 'y' if axis_num == 1 else f'y{axis_num}'

            pending_annotations.append(dict(
                x=Q_LABELS[last_idx],
                y=vals[last_idx],
                text=f"<b>{_fmt(vals[last_idx], fmt)}</b>",
                showarrow=True,
                arrowhead=0,
                arrowcolor=color,
                arrowwidth=1,
                ax=0,
                ay=-24,
                xref=xref,
                yref=yref,
                font=dict(size=9, color=color, family='Inter'),
                bgcolor='rgba(255,255,255,0.95)',
                bordercolor=color,
                borderwidth=1,
                borderpad=3,
            ))
        else:
            fig.add_trace(go.Scatter(
                x=Q_LABELS, y=[None] * 8,
                mode='lines', showlegend=False,
                line=dict(color='#e2e8f0'),
            ), row=row, col=col)

    fig.update_layout(
        height=820,
        title=dict(
            text=f'<span style="color:#0a2540;font-weight:700;font-size:16px">'
                 f'{nbfc_disp} — All Metrics Q4FY24 → Q3FY26</span>',
            font=dict(family='Inter'), x=0,
        ),
        template='plotly_white',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='white',
        margin=dict(l=50, r=30, t=70, b=40),
        font=dict(family='Inter', size=11, color='#475569'),
    )
    # Update subplot title font (these are the first 12 annotations)
    fig.update_annotations(font_size=11.5)
    fig.update_xaxes(showgrid=True, gridcolor='#f1f5f9', tickfont=dict(size=9),
                     tickangle=45)
    fig.update_yaxes(showgrid=True, gridcolor='#f1f5f9', tickfont=dict(size=9))

    # Add data-legend callouts after title-font update so they keep size=9
    for ann in pending_annotations:
        fig.add_annotation(**ann)

    return fig

# ─── NBFC SELECTOR WIDGET ─────────────────────────────────────────────────────

def nbfc_selector(tab_key: str, default_on=None) -> list:
    """Renders a compact NBFC checkbox row, returns selected display names."""
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

# ─── SESSION STATE ─────────────────────────────────────────────────────────────
if 'time_period' not in st.session_state:
    st.session_state.time_period = '6M'
if 'use_custom_date' not in st.session_state:
    st.session_state.use_custom_date = False

# ─── HEADER ────────────────────────────────────────────────────────────────────
ist = pytz.timezone('Asia/Kolkata')
now = datetime.now(ist)

st.markdown(f"""
    <div style="display:flex; justify-content:space-between; align-items:center;
                padding:8px 0 10px 0; border-bottom:1px solid #dde1e8; margin-bottom:0;">
        <div style="display:flex; align-items:baseline; gap:10px;">
            <span style="font-size:16px;font-weight:700;color:#0a2540;
                         letter-spacing:-0.01em;font-family:'Inter',sans-serif;">
                NBFC Dashboard
            </span>
            <span style="font-size:9.5px;color:#94a3b8;font-family:'JetBrains Mono',monospace;
                         background:#e8edf3;padding:2px 7px;border-radius:3px;letter-spacing:0.06em;">
                NSE &nbsp;·&nbsp; INDIA
            </span>
        </div>
        <div style="font-family:'JetBrains Mono',monospace;font-size:10.5px;
                    color:#64748b;text-align:right;line-height:1.6;">
            {now.strftime('%d %b %Y')}
            <span style="color:#94a3b8;margin-left:6px;">{now.strftime('%H:%M IST')}</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# ─── TABS ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
    "Market", "Financials", "Asset Quality", "Capital & Leverage",
    "Profitability Ratios", "Valuation Metrics", "Deep Dive", "Rankings",
    "AI Bulletin",
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — MARKET
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown('<span class="section-label">Stock Prices <span class="section-label-sub">Live NSE · refreshes every 5 min</span></span>', unsafe_allow_html=True)

    with st.spinner("Fetching live prices..."):
        stocks = get_current_prices()

    if not stocks:
        st.warning("Unable to fetch live prices. Check network or NSE data availability.")
    else:
        for row_start in range(0, len(stocks), 3):
            cols = st.columns(3, gap="small")
            for ci, stock in enumerate(stocks[row_start:row_start + 3]):
                arrow = "▲" if stock['change_pct'] >= 0 else "▼"
                cls   = "ticker-pos" if stock['change_pct'] >= 0 else "ticker-neg"
                sign  = "+" if stock['change_abs'] >= 0 else ""
                vol   = stock['volume']
                vol_s = (f"{vol/1e7:.1f}Cr" if vol >= 1e7
                         else f"{vol/1e5:.1f}L" if vol >= 1e5
                         else f"{vol/1e3:.0f}K" if vol >= 1e3
                         else str(vol) if vol > 0 else "—")
                bc = "#16a34a" if stock['change_pct'] >= 0 else "#dc2626"
                mc = stock.get('market_cap')
                if mc and mc > 0:
                    cr = mc / 1e7
                    mktcap_s = (f"₹{cr/1e5:.2f} L.Cr" if cr >= 1e5
                                else f"₹{cr/1e3:.1f}K Cr" if cr >= 1000
                                else f"₹{cr:.0f} Cr")
                else:
                    mktcap_s = "—"
                with cols[ci]:
                    st.markdown(f"""
                        <div class="ticker-card" style="border-top-color:{bc};">
                            <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                                <div>
                                    <div class="ticker-name-sm">{stock['name']}</div>
                                    <div class="ticker-sym">{stock['symbol']}</div>
                                </div>
                                <div style="text-align:right;">
                                    <div class="ticker-price">₹{stock['price']:,.0f}</div>
                                    <div class="{cls}">{arrow} {sign}{stock['change_pct']:.2f}%</div>
                                </div>
                            </div>
                            <div class="ticker-meta">{sign}₹{stock['change_abs']:.2f} &nbsp;·&nbsp; Vol {vol_s}</div>
                            <div class="ticker-meta" style="margin-top:3px;color:#0a2540;font-weight:600;">MCap {mktcap_s}</div>
                        </div>
                    """, unsafe_allow_html=True)
            st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
    st.markdown('<span class="section-label">Performance Comparison <span class="section-label-sub">Indexed to 100 · select stocks and period below</span></span>', unsafe_allow_html=True)

    others = [n for n in NBFCS if n != 'Poonawalla Fincorp']
    cmap = st.columns(5)
    cmap[0].checkbox("Poonawalla Fincorp", value=True, disabled=True, key="mkt_poonawalla_fixed")
    sel_mkt = ['Poonawalla Fincorp']
    for i, name in enumerate(others):
        with cmap[(i + 1) % 5]:
            if st.checkbox(name, value=(name in DEFAULT_COMPARISON), key=f"mkt_{name}"):
                sel_mkt.append(name)

    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

    # ── Period buttons ────────────────────────────────────────────────────────
    from datetime import date as _date
    PERIODS      = ['1W', '1M', '3M', '6M', '1Y', '3Y', '5Y']
    use_custom   = st.session_state.use_custom_date
    active       = st.session_state.time_period
    active_label = 'CUSTOM' if use_custom else active   # 'CUSTOM' means no button highlighted

    btn_cols = st.columns([0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 3.5])
    for i, p in enumerate(PERIODS):
        with btn_cols[i]:
            if st.button(p, key=f"pb_{p}", use_container_width=True):
                st.session_state.time_period    = p
                st.session_state.use_custom_date = False
                st.rerun()

    components.html(f"""<script>
        function applyStyle() {{
            var active = "{active_label}";
            document.querySelectorAll('button').forEach(function(b) {{
                var t = b.innerText.trim();
                if (t === active) {{
                    b.style.setProperty('background','#0284c7','important');
                    b.style.setProperty('color','white','important');
                    b.style.setProperty('border-color','#0284c7','important');
                    b.style.setProperty('font-weight','700','important');
                }} else if (['1W','1M','3M','6M','1Y','3Y','5Y'].includes(t)) {{
                    b.style.removeProperty('background');
                    b.style.removeProperty('color');
                    b.style.removeProperty('border-color');
                    b.style.removeProperty('font-weight');
                }}
            }});
        }}
        applyStyle(); setTimeout(applyStyle,150); setTimeout(applyStyle,400);
    </script>""", height=0)

    # ── Custom date picker ────────────────────────────────────────────────────
    _today_date = _date.today()
    _min_date   = _date(2021, 1, 1)
    _default_start = _date(2024, 1, 1)

    dc1, dc2, dc3, _ = st.columns([1.4, 1.4, 0.8, 4.4])
    with dc1:
        cd_start = st.date_input(
            "From", value=_default_start,
            min_value=_min_date, max_value=_today_date,
            key="cd_start", label_visibility="visible",
        )
    with dc2:
        cd_end = st.date_input(
            "To", value=_today_date,
            min_value=_min_date, max_value=_today_date,
            key="cd_end", label_visibility="visible",
        )
    with dc3:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        if st.button("Apply", key="apply_custom", use_container_width=True):
            if cd_start < cd_end:
                st.session_state.use_custom_date = True
                st.rerun()

    # ── Render chart ─────────────────────────────────────────────────────────
    today    = datetime.now(pytz.timezone('Asia/Kolkata'))
    DAYS_MAP = {'1W': 7, '1M': 30, '3M': 90, '6M': 180,
                '1Y': 365, '3Y': 3 * 365, '5Y': 5 * 365}

    if use_custom:
        fmt_from = cd_start.strftime("%-d %b'%y")
        fmt_to   = cd_end.strftime("%-d %b'%y")
    else:
        days_back  = DAYS_MAP.get(active, 180)
        range_from = today - timedelta(days=days_back)
        fmt_from   = range_from.strftime("%-d %b'%y")
        fmt_to     = today.strftime("%-d %b'%y")

    with st.spinner("Loading chart..."):
        try:
            if use_custom:
                ch, _, _ = create_comparison_chart(
                    'Custom', sel_mkt,
                    start_date=cd_start, end_date=cd_end,
                )
            else:
                ch, _, _ = create_comparison_chart(active, sel_mkt)

            period_display = f"Custom Range" if use_custom else active
            ch.update_layout(title_text=(
                f'<span style="color:#0a2540;font-weight:700;font-size:17px">'
                f'Performance Comparison — {period_display} (Indexed to 100)</span>'
                f'<span style="color:#94a3b8;font-size:13px;font-weight:400;">'
                f' &nbsp;·&nbsp; {fmt_from} – {fmt_to}</span>'
            ))
            st.plotly_chart(ch, use_container_width=True, config={'displayModeBar': False}, key="mkt_comparison")
        except Exception as e:
            st.error(f"Chart error: {e}")

    # ── Market Capitalisation Trend ──────────────────────────────────────────
    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    st.markdown('<span class="section-label">Market Capitalisation Trend <span class="section-label-sub">1-year daily · ₹ Lakh Crore · price × shares outstanding</span></span>', unsafe_allow_html=True)

    others_mc = [n for n in NBFCS if n != 'Poonawalla Fincorp']
    mc_cols = st.columns(5)
    mc_cols[0].checkbox("Poonawalla Fincorp", value=True, disabled=True, key="mc_poonawalla_fixed")
    sel_mc = ['Poonawalla Fincorp']
    for i, name in enumerate(others_mc):
        with mc_cols[(i + 1) % 5]:
            if st.checkbox(name, value=(name in DEFAULT_COMPARISON), key=f"mc_{name}"):
                sel_mc.append(name)

    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
    with st.spinner("Fetching 1-year price history for market cap trend..."):
        try:
            mc_fig = make_mktcap_trend_chart(sel_mc, height=440)
            mc_fig.update_layout(title_text=(
                '<span style="color:#0a2540;font-weight:700;font-size:17px">'
                'Market Capitalisation — 1 Year</span>'
                '<span style="color:#94a3b8;font-size:13px;font-weight:400;">'
                ' &nbsp;·&nbsp; Daily NSE price × current shares outstanding</span>'
            ))
            st.plotly_chart(mc_fig, use_container_width=True, config={'displayModeBar': False}, key="mkt_mcap")
        except Exception as e:
            st.error(f"Market cap chart error: {e}")
    st.markdown('<div class="metric-note">Market cap = daily NSE closing price × current shares outstanding (sourced from yfinance). Values in ₹ Lakh Crore (1 L.Cr = ₹1 Trillion). Use the MCap row on each price card above for the current total market capitalisation.</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — FINANCIALS  (Growth & Profitability)
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("""
        <div class="tab-intro">
            <span class="tab-intro-title">Growth & Scale</span>
            <span class="tab-intro-sub">Q4FY24 – Q3FY26 &nbsp;·&nbsp; AUM · PAT · NIM &nbsp;·&nbsp; 8 quarters &nbsp;·&nbsp; 9 NBFCs</span>
        </div>
    """, unsafe_allow_html=True)

    sel2 = nbfc_selector('fin')
    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    # — AUM: full-width bar, then QoQ + YoY side-by-side below
    st.markdown('<span class="section-label">Scale</span>', unsafe_allow_html=True)
    st.plotly_chart(make_bar_chart('aum_cr', sel2, 'Assets Under Management (AUM)', '₹ Crore'),
                    use_container_width=True, config={'displayModeBar': False}, key="fin_aum_bar")
    ca1, ca2 = st.columns(2)
    with ca1:
        st.plotly_chart(make_qoq_chart('aum_cr', sel2, 'AUM — QoQ Growth'),
                        use_container_width=True, config={'displayModeBar': False}, key="fin_aum_qoq")
    with ca2:
        st.plotly_chart(make_yoy_chart('aum_cr', sel2, 'AUM — YoY Growth'),
                        use_container_width=True, config={'displayModeBar': False}, key="fin_aum_yoy")

    # — PAT: full-width bar, then QoQ + YoY side-by-side below
    st.plotly_chart(make_bar_chart('pat_cr', sel2, 'Profit After Tax (PAT)', '₹ Crore'),
                    use_container_width=True, config={'displayModeBar': False}, key="fin_pat_bar")
    cp1, cp2 = st.columns(2)
    with cp1:
        st.plotly_chart(make_qoq_chart('pat_cr', sel2, 'PAT — QoQ Growth'),
                        use_container_width=True, config={'displayModeBar': False}, key="fin_pat_qoq")
    with cp2:
        st.plotly_chart(make_yoy_chart('pat_cr', sel2, 'PAT — YoY Growth'),
                        use_container_width=True, config={'displayModeBar': False}, key="fin_pat_yoy")

    # — NIM (full-width)
    st.markdown('<span class="section-label">Yield</span>', unsafe_allow_html=True)
    st.plotly_chart(make_trend_chart('nim_pct', sel2, 'Net Interest Margin (NIM)', 'NIM (%)'),
                     use_container_width=True, config={'displayModeBar': False}, key="fin_nim")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — ASSET QUALITY
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("""
        <div class="tab-intro">
            <span class="tab-intro-title">Asset Quality</span>
            <span class="tab-intro-sub">Q4FY24 – Q3FY26 &nbsp;·&nbsp; GNPA · NNPA · PCR</span>
        </div>
    """, unsafe_allow_html=True)

    sel3 = nbfc_selector('aq')
    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    # GNPA + NNPA full-width
    st.plotly_chart(make_trend_chart('gnpa_pct', sel3, 'Gross NPA (GNPA)', 'GNPA (%)',
                     lower_is_better=True),
                     use_container_width=True, config={'displayModeBar': False}, key="aq_gnpa")
    st.plotly_chart(make_trend_chart('nnpa_pct', sel3, 'Net NPA (NNPA)', 'NNPA (%)',
                     lower_is_better=True),
                     use_container_width=True, config={'displayModeBar': False}, key="aq_nnpa")

    # PCR full width
    st.plotly_chart(make_trend_chart('pcr_pct', sel3, 'Provision Coverage Ratio (PCR)',
                     'PCR (%)', height=380),
                     use_container_width=True, config={'displayModeBar': False}, key="aq_pcr")

    st.markdown('<div class="metric-note">Lower GNPA/NNPA = better credit quality. Higher PCR = more conservative provisioning.</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — CAPITAL & LEVERAGE
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown("""
        <div class="tab-intro">
            <span class="tab-intro-title">Capital Structure & Leverage</span>
            <span class="tab-intro-sub">Q4FY24 – Q3FY26 &nbsp;·&nbsp; CoB · D/E · CAR · BVPS</span>
        </div>
    """, unsafe_allow_html=True)

    sel4 = nbfc_selector('cap')
    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    st.plotly_chart(make_trend_chart('cost_of_borrowing_pct', sel4, 'Cost of Borrowing', 'CoB (%)',
                     lower_is_better=True),
                     use_container_width=True, config={'displayModeBar': False}, key="cap_cob")

    st.plotly_chart(make_trend_chart('d_e_ratio', sel4, 'Debt / Equity Ratio', 'D/E (×)',
                     fmt='ratio', lower_is_better=True),
                     use_container_width=True, config={'displayModeBar': False}, key="cap_de")
    st.plotly_chart(make_trend_chart('car_pct', sel4, 'Capital Adequacy Ratio (CAR / CRAR)',
                     'CAR (%)'),
                     use_container_width=True, config={'displayModeBar': False}, key="cap_car")

    st.markdown('<div class="metric-note">D/E (Debt-to-Equity): lower = less levered. CAR: higher = better capitalized (RBI minimum = 15%).</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — PROFITABILITY RATIOS
# ══════════════════════════════════════════════════════════════════════════════
with tab5:
    st.markdown("""
        <div class="tab-intro">
            <span class="tab-intro-title">Profitability Ratios</span>
            <span class="tab-intro-sub">Q4FY24 – Q3FY26 &nbsp;·&nbsp; ROA · ROE &nbsp;·&nbsp; 8 quarters &nbsp;·&nbsp; 9 NBFCs</span>
        </div>
    """, unsafe_allow_html=True)

    sel5 = nbfc_selector('prof')
    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    st.plotly_chart(make_trend_chart('roa_pct', sel5, 'Return on Assets (ROA)', 'ROA (%)'),
                     use_container_width=True, config={'displayModeBar': False}, key="prof_roa")
    st.plotly_chart(make_trend_chart('roe_pct', sel5, 'Return on Equity (ROE)', 'ROE (%)'),
                     use_container_width=True, config={'displayModeBar': False}, key="prof_roe")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 6 — VALUATION METRICS
# ══════════════════════════════════════════════════════════════════════════════
with tab6:
    st.markdown("""
        <div class="tab-intro">
            <span class="tab-intro-title">Valuation Metrics</span>
            <span class="tab-intro-sub">Q4FY24 – Q3FY26 &nbsp;·&nbsp; BVPS · P/B Ratio &nbsp;·&nbsp; Daily prices over quarterly book value</span>
        </div>
    """, unsafe_allow_html=True)

    sel6 = nbfc_selector('val')
    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    st.markdown('<span class="section-label">Price-to-Book Ratio <span class="section-label-sub">Daily NSE closing price ÷ latest quarterly BVPS</span></span>', unsafe_allow_html=True)
    with st.spinner("Fetching 2-year price history for P/B calculation..."):
        st.plotly_chart(make_pb_chart(sel6, height=520),
                        use_container_width=True, config={'displayModeBar': False}, key="val_pb")

    st.markdown('<span class="section-label">Book Value Per Share (BVPS) <span class="section-label-sub">₹ per share · quarterly — absolute reference</span></span>', unsafe_allow_html=True)
    st.plotly_chart(make_trend_chart('bvps_inr', sel6, 'Book Value Per Share (BVPS)',
                     'BVPS (₹)', fmt='inr', height=380),
                     use_container_width=True, config={'displayModeBar': False}, key="val_bvps")

    st.markdown('<div class="metric-note">P/B = Daily NSE closing price ÷ most recently reported quarterly BVPS. BVPS steps up at each quarter-end (Q4FY24–Q3FY26). Dotted line at P/B = 1 (book value floor). Lower P/B may indicate undervaluation relative to peers. BVPS chart below shows the absolute book values underpinning each P/B reading.</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 7 — DEEP DIVE (Per-NBFC full profile)
# ══════════════════════════════════════════════════════════════════════════════
with tab7:
    st.markdown("""
        <div class="tab-intro">
            <span class="tab-intro-title">Company Deep Dive</span>
            <span class="tab-intro-sub">Select an NBFC to view all 12 metrics across 8 quarters</span>
        </div>
    """, unsafe_allow_html=True)

    chosen = st.selectbox(
        "Select NBFC",
        DISPLAY_NAMES,
        index=0,
        key="deep_dive_nbfc",
        label_visibility="collapsed",
    )
    with st.spinner(f"Rendering {chosen} profile..."):
        st.plotly_chart(make_deep_dive(chosen),
                        use_container_width=True, config={'displayModeBar': False}, key="dd_main")

    st.markdown('<div class="metric-note">Gaps in charts = metric not disclosed for that quarter. Refer to individual company investor presentations for full notes.</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 8 — RANKINGS (Q3FY26 scorecard)
# ══════════════════════════════════════════════════════════════════════════════
with tab8:
    st.markdown("""
        <div class="tab-intro">
            <span class="tab-intro-title">Peer Scorecard — Q3 FY26</span>
            <span class="tab-intro-sub">All 9 NBFCs · 11 metrics · Red → Yellow → Green spectrum within each column</span>
        </div>
    """, unsafe_allow_html=True)

    st.plotly_chart(build_rankings_table(),
                    use_container_width=True, config={'displayModeBar': False}, key="rank_table")

    st.markdown("""
        <div class="metric-note">
            <b>Color coding:</b> Within each column, green = best-in-class, yellow = mid-range, red = weakest (continuous spectrum).
            For GNPA/NNPA/CoB/D/E lower is better; for AUM/PAT/NIM/ROA/ROE/CAR higher is better. &nbsp;·&nbsp;
            <b>—</b> = not disclosed or not yet available.
        </div>
    """, unsafe_allow_html=True)

    # Quick summary stats
    st.markdown('<span class="section-label">Quick Highlights — Q3 FY26</span>', unsafe_allow_html=True)
    hi_cols = st.columns(4)
    Q_IDX = 7
    aum_s = get_series('aum_cr')
    pat_s = get_series('pat_cr')
    roa_s = get_series('roa_pct')
    gnpa_s = get_series('gnpa_pct')

    best_aum   = max(DISPLAY_NAMES, key=lambda n: aum_s[n][Q_IDX] or 0)
    best_pat   = max(DISPLAY_NAMES, key=lambda n: pat_s[n][Q_IDX] or 0)
    best_roa   = max(DISPLAY_NAMES, key=lambda n: roa_s[n][Q_IDX] or 0)
    best_gnpa  = min(DISPLAY_NAMES, key=lambda n: gnpa_s[n][Q_IDX] or 99)

    def highlight_card(label, value, note, color):
        return f"""
        <div style="background:white;border-radius:5px;padding:12px 14px;
                    border-top:3px solid {color};box-shadow:0 1px 2px rgba(0,0,0,0.05);">
            <div style="font-size:10px;font-weight:700;letter-spacing:0.06em;
                        text-transform:uppercase;color:#94a3b8;">{label}</div>
            <div style="font-size:15px;font-weight:700;color:#0a2540;margin:4px 0 2px;">{value}</div>
            <div style="font-size:10.5px;color:#64748b;">{note}</div>
        </div>"""

    with hi_cols[0]:
        v = aum_s[best_aum][Q_IDX]
        st.markdown(highlight_card("Largest AUM", best_aum, f"₹{v:,.0f} Cr", "#0284c7"), unsafe_allow_html=True)
    with hi_cols[1]:
        v = pat_s[best_pat][Q_IDX]
        st.markdown(highlight_card("Highest PAT", best_pat, f"₹{v:,.0f} Cr", "#10b981"), unsafe_allow_html=True)
    with hi_cols[2]:
        v = roa_s[best_roa][Q_IDX]
        st.markdown(highlight_card("Best ROA", best_roa, f"{v:.2f}%", "#f97316"), unsafe_allow_html=True)
    with hi_cols[3]:
        v = gnpa_s[best_gnpa][Q_IDX]
        st.markdown(highlight_card("Cleanest Book", best_gnpa, f"GNPA {v:.2f}%", "#8b5cf6"), unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 9 — AI BULLETIN
# ══════════════════════════════════════════════════════════════════════════════
from datetime import datetime as _dt

def _parse_ai_date(d: str):
    """Parse 'DD Mon YYYY' → datetime for sorting. Falls back to epoch on error."""
    try:
        return _dt.strptime(d.strip(), "%d %b %Y")
    except Exception:
        return _dt(1970, 1, 1)

def _render_initiative_card(nbfc: str, init: dict, show_nbfc_badge: bool = False):
    """Render one initiative as a Streamlit expander with styled internals."""
    label_prefix = f"[{nbfc}]  " if show_nbfc_badge else ""
    with st.expander(f"{label_prefix}{init['title']}"):
        # NBFC badge (only in cross-NBFC views)
        if show_nbfc_badge:
            color = COLORS.get(nbfc, '#0284c7')
            st.markdown(
                f'<span class="ai-nbfc-badge" style="background:{color};">{nbfc}</span>',
                unsafe_allow_html=True,
            )

        # Impact line
        st.markdown(
            f'<div class="ai-impact">⚡ {init["impact"]}</div>',
            unsafe_allow_html=True,
        )

        # Full description
        st.markdown(
            f'<div class="ai-desc">{init["description"]}</div>',
            unsafe_allow_html=True,
        )

        # Function tags
        tags_html = "".join(
            f'<span class="ai-func-tag">{fn}</span>'
            for fn in init.get("functions", [])
        )
        if tags_html:
            st.markdown(tags_html, unsafe_allow_html=True)

        # Meta row: date + source
        src_name = init.get("source_name", "")
        src_url  = init.get("source_url", "")
        src_html = (
            f'<a class="ai-source-link" href="{src_url}" target="_blank">↗ {src_name}</a>'
            if src_url else src_name
        )
        st.markdown(
            f'<div class="ai-meta-row">'
            f'<span class="ai-date-badge">{init["date"]}</span>'
            f'{src_html}'
            f'</div>',
            unsafe_allow_html=True,
        )


with tab9:
    st.markdown("""
        <div class="tab-intro">
            <span class="tab-intro-title">AI Bulletin</span>
            <span class="tab-intro-sub">51 AI initiatives · 9 NBFCs · Jan 2021 – Feb 2026 &nbsp;·&nbsp; Research compiled 23 Feb 2026</span>
        </div>
    """, unsafe_allow_html=True)

    # ── Top stats banner ────────────────────────────────────────────────────
    total_initiatives = sum(len(v) for v in NBFC_AI_INITIATIVES.values())
    all_flat = [(nbfc, i) for nbfc, inits in NBFC_AI_INITIATIVES.items() for i in inits]
    all_sorted_dates = sorted(all_flat, key=lambda x: _parse_ai_date(x[1]['date']))
    earliest = all_sorted_dates[0][1]['date'] if all_sorted_dates else "—"
    latest   = all_sorted_dates[-1][1]['date'] if all_sorted_dates else "—"
    func_count = len(FUNCTION_TAXONOMY)

    sc1, sc2, sc3, sc4 = st.columns(4)
    for col, num, lbl, clr in [
        (sc1, str(total_initiatives), "Total Initiatives", "#0284c7"),
        (sc2, str(len(NBFC_AI_INITIATIVES)), "NBFCs Covered", "#10b981"),
        (sc3, str(func_count), "Business Functions", "#8b5cf6"),
        (sc4, "Jan '21 – Feb '26", "Date Range", "#f97316"),
    ]:
        with col:
            st.markdown(
                f'<div class="ai-stat-card" style="border-top-color:{clr};">'
                f'<div class="ai-stat-num" style="color:{clr};">{num}</div>'
                f'<div class="ai-stat-label">{lbl}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

    # ── Three sub-tabs ──────────────────────────────────────────────────────
    ai_sub1, ai_sub2, ai_sub3 = st.tabs(["By NBFC", "By Function", "Timeline"])

    # ── SUB-TAB 1: BY NBFC ─────────────────────────────────────────────────
    with ai_sub1:
        st.markdown(
            '<div class="metric-note">All 51 initiatives grouped by NBFC · '
            'Click any row to expand the full description, impact, and source.</div>',
            unsafe_allow_html=True,
        )
        for nbfc, initiatives in NBFC_AI_INITIATIVES.items():
            color = COLORS.get(nbfc, '#0284c7')
            st.markdown(
                f'<div class="ai-nbfc-header" style="--nbfc-color:{color};">'
                f'<span class="ai-nbfc-name">{nbfc}</span>'
                f'<span class="ai-nbfc-count">{len(initiatives)} initiative{"s" if len(initiatives) != 1 else ""}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )
            for init in initiatives:
                _render_initiative_card(nbfc, init, show_nbfc_badge=False)

    # ── SUB-TAB 2: BY FUNCTION ─────────────────────────────────────────────
    with ai_sub2:
        # Count initiatives per function for the selector label
        func_counts = {
            fn: sum(1 for _, inits in NBFC_AI_INITIATIVES.items() for i in inits if fn in i.get('functions', []))
            for fn in FUNCTION_TAXONOMY
        }
        func_options = [f"{fn}  ({func_counts[fn]})" for fn in FUNCTION_TAXONOMY]

        selected_func_label = st.selectbox(
            "Select a business function to filter all NBFC initiatives:",
            options=func_options,
            index=0,
            key="ai_func_select",
        )
        selected_func = FUNCTION_TAXONOMY[func_options.index(selected_func_label)]

        filtered = [
            (nbfc, init)
            for nbfc, inits in NBFC_AI_INITIATIVES.items()
            for init in inits
            if selected_func in init.get('functions', [])
        ]

        n = len(filtered)
        nbfcs_in_view = sorted(set(nbfc for nbfc, _ in filtered))
        st.markdown(
            f'<div class="metric-note">'
            f'<b>{n} initiative{"s" if n != 1 else ""}</b> tagged '
            f'<b>{selected_func}</b> across '
            f'<b>{len(nbfcs_in_view)} NBFC{"s" if len(nbfcs_in_view) != 1 else ""}</b>: '
            f'{", ".join(nbfcs_in_view)}'
            f'</div>',
            unsafe_allow_html=True,
        )

        if not filtered:
            st.info("No initiatives found for this function.")
        else:
            for nbfc, init in filtered:
                _render_initiative_card(nbfc, init, show_nbfc_badge=True)

    # ── SUB-TAB 3: TIMELINE ────────────────────────────────────────────────
    with ai_sub3:
        st.markdown(
            '<div class="metric-note">All 51 initiatives sorted newest → oldest · '
            'NBFC badge colour-coded · reveals the pace of AI adoption across the sector.</div>',
            unsafe_allow_html=True,
        )

        timeline_items = sorted(
            [(nbfc, init) for nbfc, inits in NBFC_AI_INITIATIVES.items() for init in inits],
            key=lambda x: _parse_ai_date(x[1]['date']),
            reverse=True,
        )

        current_year = None
        for nbfc, init in timeline_items:
            year = _parse_ai_date(init['date']).year
            if year != current_year:
                current_year = year
                st.markdown(
                    f'<span class="section-label">{year}</span>',
                    unsafe_allow_html=True,
                )
            _render_initiative_card(nbfc, init, show_nbfc_badge=True)

    st.markdown(
        '<div class="metric-note" style="margin-top:14px;">'
        'Sources: company websites, annual reports, BSE filings, earnings call transcripts, '
        'Business Standard, Medianama, Microsoft News, Analytics India Magazine, and vendor case studies. '
        'Compiled 23 Feb 2026.'
        '</div>',
        unsafe_allow_html=True,
    )


# ─── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("""
    <div style="font-size:10px;color:#94a3b8;font-family:'JetBrains Mono',monospace;
                border-top:1px solid #e2e8f0;padding-top:8px;margin-top:14px;">
        Data: Screener.in investor presentations · Yahoo Finance (market prices) ·
        Q4FY24–Q3FY26 (8 quarters) · 9 NBFCs · Last refreshed: Feb 2026
    </div>
""", unsafe_allow_html=True)
