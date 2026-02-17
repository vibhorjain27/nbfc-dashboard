import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import yfinance as yf
import pytz

# Page configuration
st.set_page_config(
    page_title="NBFC Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Professional Bloomberg-inspired theme
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

    /* Background */
    .main {
        background: linear-gradient(135deg, #f8f9fb 0%, #e8edf3 100%);
        font-family: 'DM Sans', sans-serif;
    }

    .block-container {
        padding: 2rem 3rem;
        max-width: 1400px;
    }

    /* Headers */
    h1 { color: #0a2540; font-weight: 700; font-size: 2rem; }
    h2, h3 { color: #1a3a52; font-weight: 600; }

    /* Section title — dark blue pill used across tabs */
    .section-title {
        background: linear-gradient(135deg, #0a2540 0%, #1e3a5f 100%);
        color: white;
        padding: 14px 22px;
        border-radius: 10px;
        font-size: 1.15rem;
        font-weight: 700;
        margin-bottom: 18px;
        display: block;
    }
    .section-subtitle {
        color: #94a3b8;
        font-size: 12px;
        margin-top: 4px;
        display: block;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: white;
        padding: 8px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 8px;
        color: #64748b;
        font-weight: 600;
        padding: 12px 24px;
        font-size: 14px;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%) !important;
        color: white !important;
    }

    /* Stock cards */
    .stock-card {
        background: white;
        border-radius: 10px;
        padding: 16px 20px;
        border-left: 4px solid #0284c7;
        box-shadow: 0 1px 4px rgba(0,0,0,0.08);
        margin-bottom: 4px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        min-height: 100px;
    }
    .stock-left { display: flex; flex-direction: column; justify-content: center; }
    .stock-right { display: flex; flex-direction: column; align-items: flex-end; justify-content: center; }
    .stock-name { font-size: 17px; font-weight: 700; color: #0a2540; margin-bottom: 3px; }
    .stock-symbol { font-size: 11px; color: #94a3b8; letter-spacing: 0.04em; margin-bottom: 6px; }
    .stock-volume { font-size: 11px; color: #64748b; margin-top: 4px; }
    .stock-price { font-size: 24px; font-weight: 700; color: #1a3a52; font-family: 'JetBrains Mono', monospace; margin-bottom: 4px; }
    .stock-change-pos { color: #16a34a; font-weight: 700; font-size: 14px; }
    .stock-change-neg { color: #dc2626; font-weight: 700; font-size: 14px; }

    /* Period buttons */
    .stButton button {
        background: white;
        color: #475569;
        border: 1.5px solid #cbd5e1;
        border-radius: 6px;
        padding: 5px 14px;
        font-weight: 600;
        font-size: 12px;
        transition: all 0.2s;
        width: 100%;
    }
    .stButton button:hover {
        border-color: #0284c7;
        color: #0284c7;
    }

    /* Checkboxes */
    .stCheckbox { font-size: 13px; }

    /* Hide Streamlit chrome */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    .stDeployButton { display: none; }
    [data-testid="stSidebar"] { display: none; }
    </style>
""", unsafe_allow_html=True)

# ─── CONFIG ───────────────────────────────────────────────────────────────────

NBFCS = {
    'Poonawalla Fincorp': 'POONAWALLA.NS',
    'Bajaj Finance':      'BAJFINANCE.NS',
    'L&T Finance':        'LTF.NS',
    'Shriram Finance':    'SHRIRAMFIN.NS',
    'Cholamandalam Finance': 'CHOLAFIN.NS',
    'Aditya Birla Capital':  'ABCAPITAL.NS',
    'Piramal Finance':    'PIRAMALFIN.NS',
    'Muthoot Finance':    'MUTHOOTFIN.NS',
    'Mahindra Finance':   'M&MFIN.NS',
}

DEFAULT_COMPARISON = ['Poonawalla Fincorp', 'Bajaj Finance', 'L&T Finance', 'Shriram Finance']

COLORS = {
    'Poonawalla Fincorp':    '#0284c7',
    'Bajaj Finance':         '#f97316',
    'L&T Finance':           '#8b5cf6',
    'Shriram Finance':       '#10b981',
    'Cholamandalam Finance': '#ef4444',
    'Aditya Birla Capital':  '#0891b2',
    'Piramal Finance':       '#be123c',
    'Muthoot Finance':       '#65a30d',
    'Mahindra Finance':      '#7c3aed',
}

# Tab 2 financial data (4 quarters, 4 NBFCs)
QUARTERS = ['Q4 FY25', 'Q1 FY26', 'Q2 FY26', 'Q3 FY26']

AUM = {
    # ── Confirmed from official investor presentations / press releases ──
    'Poonawalla Fincorp':   [31900,  36636,  47709,   55017],
    'Bajaj Finance':        [341001, 363000, 412000,  485883],
    'Shriram Finance':      [249005, 262000, 281309,  291709],
    'L&T Finance':          [96000,  103000, 108000,  114285],
    'Cholamandalam Finance':[189141, 199159, 214906,  227770],  # ✅ official
    'Piramal Finance':      [80689,  86000,  91447,   96690],   # ✅ official (Q1 est)
    'Muthoot Finance':      [122181, 130000, 147674,  164720],  # ✅ official (Q1 est)
    # ── Partially estimated ──
    'Aditya Birla Capital': [157404, 168000, 179000,  190386],  # NBFC+HFC; Q4 & Q3 official
    'Mahindra Finance':     [103000, 107000, 112000,  118000],  # ⚠️ estimated (~17% YoY growth)
}
NIM = {
    'Poonawalla Fincorp':   [7.80,  8.10,  8.40,  8.62],
    'Bajaj Finance':        [9.90,  10.10, 10.10, 10.20],
    'Shriram Finance':      [8.20,  8.25,  8.29,  8.40],
    'L&T Finance':          [9.80,  10.00, 10.20, 10.41],
    'Cholamandalam Finance':[8.00,  7.50,  7.90,  8.00],        # ✅ official
    'Piramal Finance':      [5.50,  5.80,  6.10,  6.30],        # ✅ official
    'Muthoot Finance':      [11.50, 11.60, 11.80, 11.85],       # ✅ gold loan spread (not NIM)
    'Aditya Birla Capital': [8.50,  8.60,  8.70,  8.80],        # ⚠️ estimated
    'Mahindra Finance':     [7.50,  7.60,  7.70,  7.60],        # ⚠️ estimated
}
GNPA = {
    'Poonawalla Fincorp':   [1.84, 1.72, 1.59, 1.51],
    'Bajaj Finance':        [0.96, 1.11, 1.24, 1.21],
    'Shriram Finance':      [4.55, 4.80, 4.57, 5.01],
    'L&T Finance':          [3.29, 3.10, 2.90, 2.70],
    'Cholamandalam Finance':[3.97, 4.29, 4.57, 4.63],           # ✅ official RBI norms
    'Piramal Finance':      [2.80, 2.80, 2.60, 2.40],           # ✅ official
    'Muthoot Finance':      [2.58, 2.50, 2.25, 1.60],           # ✅ official
    'Aditya Birla Capital': [2.80, 2.70, 2.60, 2.50],           # ⚠️ growth biz GNPA; partial
    'Mahindra Finance':     [4.80, 4.60, 4.50, 4.20],           # ⚠️ est from Stage-3 (3.7%)
}
NNPA = {
    'Poonawalla Fincorp':   [0.85, 0.83, 0.81, 0.80],
    'Bajaj Finance':        [0.44, 0.54, 0.60, 0.47],
    'Shriram Finance':      [2.64, 2.55, 2.49, 2.60],
    'L&T Finance':          [0.97, 0.90, 0.82, 0.75],
    'Cholamandalam Finance':[2.63, 2.86, 3.07, 2.80],           # ✅ official RBI norms
    'Piramal Finance':      [1.90, 2.00, 1.80, 1.60],           # ✅ official
    'Muthoot Finance':      [2.10, 2.10, 1.86, 1.20],           # ✅ official
    'Aditya Birla Capital': [1.50, 1.40, 1.30, 1.20],           # ⚠️ estimated
    'Mahindra Finance':     [2.50, 2.40, 2.30, 2.10],           # ⚠️ estimated
}
ROA = {
    'Poonawalla Fincorp':   [0.60, 0.80, 1.00, 1.20],
    'Bajaj Finance':        [4.40, 4.50, 4.55, 4.60],
    'Shriram Finance':      [2.70, 2.85, 2.95, 3.09],
    'L&T Finance':          [2.40, 2.50, 2.60, 2.70],
    'Cholamandalam Finance':[2.10, 2.10, 2.20, 2.30],           # ⚠️ PAT-ROA; derived from PBT-ROA 3%
    'Piramal Finance':      [1.40, 1.50, 1.60, 1.90],           # ✅ Growth biz RoAUM
    'Muthoot Finance':      [4.20, 4.50, 5.80, 6.50],           # ⚠️ est; gold loans = high ROA
    'Aditya Birla Capital': [2.25, 2.20, 2.30, 2.40],           # ✅ Q4 FY25; rest estimated
    'Mahindra Finance':     [2.20, 2.10, 2.00, 1.80],           # ⚠️ est; Q3 PAT fell 10% YoY
}

FIN_COLORS = {
    'Poonawalla Fincorp':   '#0284c7',
    'Bajaj Finance':        '#f97316',
    'Shriram Finance':      '#10b981',
    'L&T Finance':          '#8b5cf6',
    'Cholamandalam Finance':'#ef4444',
    'Aditya Birla Capital': '#0891b2',
    'Piramal Finance':      '#be123c',
    'Muthoot Finance':      '#65a30d',
    'Mahindra Finance':     '#7c3aed',
}

# Default 4 shown; others toggleable
FIN_DEFAULT = ['Poonawalla Fincorp', 'Bajaj Finance', 'Shriram Finance', 'L&T Finance']
FIN_OPTIONAL = ['Cholamandalam Finance', 'Aditya Birla Capital', 'Piramal Finance',
                'Muthoot Finance', 'Mahindra Finance']

# ─── SESSION STATE ─────────────────────────────────────────────────────────────

if 'time_period' not in st.session_state:
    st.session_state.time_period = '6M'

# ─── DATA FUNCTIONS ────────────────────────────────────────────────────────────

@st.cache_data(ttl=3600)
def fetch_stock_data(symbol, period='1y'):
    try:
        return yf.Ticker(symbol).history(period=period)
    except:
        return None

@st.cache_data(ttl=300)  # Refresh every 5 min for live volume
def get_current_prices():
    data = []
    for name, symbol in NBFCS.items():
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period='5d')
            if len(hist) > 0:
                current = hist['Close'].iloc[-1]
                prev = hist['Close'].iloc[-2] if len(hist) > 1 else current
                change_abs = current - prev
                change_pct = (change_abs / prev) * 100
                # Volume: today's traded volume
                volume = int(hist['Volume'].iloc[-1]) if 'Volume' in hist.columns else 0
                data.append({
                    'name': name,
                    'symbol': symbol.replace('.NS', ''),
                    'price': current,
                    'change_abs': change_abs,
                    'change_pct': change_pct,
                    'volume': volume,
                })
        except:
            continue
    return data

def get_period_days(period):
    return {'1D': 1, '1W': 7, '1M': 30, '3M': 90, '6M': 180, '1Y': 365}.get(period, 180)

def create_comparison_chart(time_period, selected_stocks):
    fig = go.Figure()
    days = get_period_days(time_period)
    yf_period = '5d' if days <= 7 else '1mo' if days <= 30 else '3mo' if days <= 90 else '1y'

    performance_data = []
    actual_start_date = None
    actual_end_date = None

    for name in selected_stocks:
        symbol = NBFCS[name]
        try:
            data = fetch_stock_data(symbol, period=yf_period)
            if data is None or data.empty:
                continue
            end_date = data.index[-1]
            start_date = end_date - timedelta(days=days)
            filtered = data[data.index >= start_date]
            if filtered.empty or len(filtered) < 2:
                continue
            prices = filtered['Close']
            indexed = (prices / prices.iloc[0]) * 100
            # Track actual date range across all stocks
            if actual_start_date is None or filtered.index[0] < actual_start_date:
                actual_start_date = filtered.index[0]
            if actual_end_date is None or filtered.index[-1] > actual_end_date:
                actual_end_date = filtered.index[-1]
            performance_data.append({
                'name': name,
                'performance': indexed.iloc[-1] - 100,
                'dates': filtered.index,
                'values': indexed,
                'color': COLORS[name],
                'end_y': float(indexed.iloc[-1]),
            })
        except:
            continue

    # Sort best to worst
    performance_data.sort(key=lambda x: x['performance'], reverse=True)

    # ── Anti-collision: DYNAMIC gap based on actual data range ─────────────────
    # Compute y-range across ALL data points
    if performance_data:
        all_vals = [v for item in performance_data for v in item['values']]
        y_range = max(all_vals) - min(all_vals)
        # Gap = 15% of data range, floor of 0.5, ceiling of 4.0
        # This auto-scales: 1D (range ~2) → gap ~0.3; 3M (range ~35) → gap ~5
        MIN_GAP = max(0.5, min(4.0, y_range * 0.15))
    else:
        MIN_GAP = 2.0

    label_positions = [item['end_y'] for item in performance_data]

    # Pass 1: push DOWN if too close to label above
    for i in range(1, len(label_positions)):
        if label_positions[i - 1] - label_positions[i] < MIN_GAP:
            label_positions[i] = label_positions[i - 1] - MIN_GAP

    # Pass 2: push UP from bottom if pass 1 overcorrected
    for i in range(len(label_positions) - 2, -1, -1):
        if label_positions[i] - label_positions[i + 1] < MIN_GAP:
            label_positions[i] = label_positions[i + 1] + MIN_GAP

    # Add traces + annotations with corrected positions
    for i, item in enumerate(performance_data):
        fig.add_trace(go.Scatter(
            x=item['dates'],
            y=item['values'],
            name=item['name'],
            line=dict(color=item['color'], width=2.5),
            mode='lines',
            hovertemplate=f"<b>{item['name']}</b><br>%{{x|%d %b %Y}}<br>%{{y:.1f}}<extra></extra>"
        ))

        # Small dot at line end to connect label to line
        fig.add_trace(go.Scatter(
            x=[item['dates'][-1]],
            y=[item['end_y']],
            mode='markers',
            marker=dict(size=7, color=item['color']),
            showlegend=False,
            hoverinfo='skip',
        ))

        pct_str = f"{item['performance']:+.1f}%"
        fig.add_annotation(
            x=item['dates'][-1],
            y=label_positions[i],
            text=f"<b>{item['name']}</b>  {pct_str}",
            showarrow=False,
            xanchor='left',
            xshift=12,
            font=dict(size=11, color=item['color']),
            bgcolor='rgba(255,255,255,0.9)',
            bordercolor=item['color'],
            borderwidth=1,
            borderpad=4,
        )

    fig.update_layout(
        title=dict(
            text=f'<span style="color:#0a2540;font-weight:700;font-size:17px">'
                 f'Performance Comparison — {time_period} (Indexed to 100)</span>',
            font=dict(family='DM Sans, sans-serif'), x=0),
        xaxis_title='Date',
        yaxis_title='Indexed Value (Base = 100)',
        template='plotly_white',
        height=520,
        hovermode='x unified',
        showlegend=False,
        plot_bgcolor='white',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=60, r=200, t=60, b=50),
        font=dict(family='DM Sans, sans-serif', color='#1a3a52'),
    )
    fig.update_xaxes(showgrid=True, gridcolor='#f1f5f9', showline=True, linecolor='#cbd5e1')
    fig.update_yaxes(showgrid=True, gridcolor='#f1f5f9', showline=True, linecolor='#cbd5e1')
    return fig, actual_start_date, actual_end_date

def make_fin_chart(metric_data, selected, title, ylabel, fmt='pct', note=None):
    """
    Full-width chart with:
    • Traces sorted by average value → hover tooltip order matches chart top-to-bottom order
      across all quarters (Plotly shows hover items in trace-addition order)
    • End-of-line labels with anti-collision spacing
    • Dark blue bold chart title, note in muted grey below
    """
    fig = go.Figure()

    # ── Sort series by mean value descending so hover order ≈ visual order ──
    series = []
    for name in selected:
        if name not in metric_data:
            continue
        vals = metric_data[name]
        series.append({'name': name, 'values': vals,
                       'avg': sum(vals) / len(vals), 'last': vals[-1],
                       'color': FIN_COLORS[name]})
    series.sort(key=lambda x: x['avg'], reverse=True)

    # ── Add traces in sorted order (determines hover tooltip order) ──────────
    for s in series:
        val_fmt = '%{y:.2f}%' if fmt == 'pct' else '₹%{y:,.0f} Cr'
        fig.add_trace(go.Scatter(
            x=QUARTERS,
            y=s['values'],
            name=s['name'],
            mode='lines+markers',
            line=dict(color=s['color'], width=2.5),
            marker=dict(size=8, color=s['color']),
            hovertemplate=f"<b>{s['name']}</b>  {val_fmt}<extra></extra>",
        ))

    # ── Anti-collision end-of-line labels ────────────────────────────────────
    label_y = [s['last'] for s in series]
    all_vals = [v for s in series for v in s['values']]
    y_range  = max(all_vals) - min(all_vals) if all_vals else 1
    MIN_GAP  = max(y_range * 0.12, 0.25)

    # Push down pass
    for i in range(1, len(label_y)):
        if label_y[i - 1] - label_y[i] < MIN_GAP:
            label_y[i] = label_y[i - 1] - MIN_GAP
    # Push up pass
    for i in range(len(label_y) - 2, -1, -1):
        if label_y[i] - label_y[i + 1] < MIN_GAP:
            label_y[i] = label_y[i + 1] + MIN_GAP

    for i, s in enumerate(series):
        val_str = f"{s['last']:.2f}%" if fmt == 'pct' else f"₹{s['last']:,.0f} Cr"
        # Connector line from actual value to label
        if abs(s['last'] - label_y[i]) > MIN_GAP * 0.3:
            fig.add_shape(type='line',
                x0=QUARTERS[-1], x1=QUARTERS[-1],
                y0=s['last'], y1=label_y[i],
                line=dict(color=s['color'], width=1, dash='dot'),
                xref='x', yref='y')
        fig.add_annotation(
            x=QUARTERS[-1], y=label_y[i],
            text=f"<b style='color:{s['color']}'>{s['name']}</b>  {val_str}",
            showarrow=False,
            xanchor='left', xshift=14,
            font=dict(size=11, color=s['color']),
            bgcolor='rgba(255,255,255,0.95)',
            bordercolor=s['color'],
            borderwidth=1,
            borderpad=4,
        )

    # ── Title: dark blue bold + muted note line ──────────────────────────────
    title_html = (
        f'<span style="color:#0a2540;font-weight:700;font-size:16px">{title}</span>'
    )
    if note:
        title_html += (
            f'<br><span style="color:#94a3b8;font-size:11px;font-weight:400">{note}</span>'
        )

    fig.update_layout(
        title=dict(text=title_html, font=dict(family='DM Sans, sans-serif'), x=0, xref='paper'),
        yaxis_title=ylabel,
        template='plotly_white',
        height=420,
        hovermode='x unified',
        showlegend=False,
        plot_bgcolor='white',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=60, r=240, t=70, b=50),
        font=dict(family='DM Sans, sans-serif', color='#1a3a52'),
        hoverlabel=dict(bgcolor='white', bordercolor='#cbd5e1',
                        font=dict(family='DM Sans, sans-serif', size=12)),
    )
    fig.update_xaxes(showgrid=True, gridcolor='#f1f5f9', showline=True, linecolor='#cbd5e1',
                     tickfont=dict(size=12, color='#475569'))
    fig.update_yaxes(showgrid=True, gridcolor='#f1f5f9', showline=True, linecolor='#cbd5e1',
                     tickfont=dict(size=12, color='#475569'))
    return fig

# ─── HEADER ────────────────────────────────────────────────────────────────────

ist = pytz.timezone('Asia/Kolkata')
current_time = datetime.now(ist)

st.title("NBFC Dashboard")
st.caption(f"Live market data  •  Last updated: {current_time.strftime('%B %d, %Y at %I:%M %p IST')}")

# ─── TABS ──────────────────────────────────────────────────────────────────────

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📈 Market Overview",
    "💼 Financial Performance",
    "💰 Valuation Metrics",
    "📊 Historical Analysis",
    "🔍 Deep Dive",
    "🏆 Rankings",
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — MARKET OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════

with tab1:
    st.markdown('<div class="section-title">Current Stock Prices<span class="section-subtitle">Live NSE prices • Updates every 5 minutes</span></div>', unsafe_allow_html=True)

    with st.spinner("Fetching live prices..."):
        stocks = get_current_prices()

    if not stocks:
        st.error("Unable to fetch stock data. Please try again.")
    else:
        # 3×3 grid
        for row_start in range(0, len(stocks), 3):
            cols = st.columns(3)
            for col_idx, stock in enumerate(stocks[row_start:row_start + 3]):
                arrow = "▲" if stock['change_pct'] >= 0 else "▼"
                chg_class = "stock-change-pos" if stock['change_pct'] >= 0 else "stock-change-neg"
                border_color = "#16a34a" if stock['change_pct'] >= 0 else "#dc2626"
                # Format absolute change
                abs_sign = "+" if stock['change_abs'] >= 0 else ""
                abs_str = f"{abs_sign}₹{stock['change_abs']:.2f}"
                pct_str = f"({abs_sign}{stock['change_pct']:.2f}%)"
                # Format volume
                vol = stock['volume']
                if vol >= 10_000_000:
                    vol_str = f"{vol/10_000_000:.1f}Cr"
                elif vol >= 100_000:
                    vol_str = f"{vol/100_000:.1f}L"
                elif vol >= 1000:
                    vol_str = f"{vol/1000:.0f}K"
                else:
                    vol_str = str(vol) if vol > 0 else "—"

                with cols[col_idx]:
                    st.markdown(f"""
                        <div class="stock-card" style="border-left-color: {border_color}">
                            <div class="stock-left">
                                <div class="stock-name">{stock['name']}</div>
                                <div class="stock-symbol">{stock['symbol']}</div>
                                <div class="stock-volume">Vol: {vol_str}</div>
                            </div>
                            <div class="stock-right">
                                <div class="stock-price">₹{stock['price']:,.2f}</div>
                                <div class="{chg_class}">{arrow} {abs_str} {pct_str}</div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

    st.markdown("---")

    # ── Comparison Chart Section ──
    st.markdown('<div class="section-title">Performance Comparison<span class="section-subtitle">Indexed to 100 • Select stocks and time period below</span></div>', unsafe_allow_html=True)

    # Stock selector checkboxes
    st.caption("Select stocks to include in comparison chart:")
    other_stocks = [n for n in NBFCS if n != 'Poonawalla Fincorp']
    col1, col2, col3 = st.columns(3)
    cols_map = [col1, col2, col3]

    selected_others = []
    with col1:
        st.markdown("**Poonawalla Fincorp** *(always shown)*")
    for i, name in enumerate(other_stocks):
        with cols_map[i % 3]:
            is_default = name in DEFAULT_COMPARISON
            if st.checkbox(name, value=is_default, key=f"chk_{name}"):
                selected_others.append(name)

    comparison_stocks = ['Poonawalla Fincorp'] + selected_others

    # Period selector — real st.buttons + JS to style the active one after render
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    periods = ['1D', '1W', '1M', '3M', '6M', '1Y']
    active = st.session_state.time_period

    btn_cols = st.columns(6)
    for i, p in enumerate(periods):
        with btn_cols[i]:
            if st.button(p, key=f"pb_{p}", use_container_width=True):
                st.session_state.time_period = p
                st.rerun()

    # JS: find the button whose text matches the active period and colour it blue.
    # Runs inside an iframe (st.components) but reaches parent DOM via window.parent.
    # Three attempts with delays to catch Streamlit's async render.
    components.html(f"""
        <script>
            function applyStyle() {{
                var active = "{active}";
                var btns = window.parent.document.querySelectorAll("button");
                btns.forEach(function(b) {{
                    var txt = b.innerText.trim();
                    if (txt === active) {{
                        b.style.setProperty("background", "#0284c7", "important");
                        b.style.setProperty("color", "white", "important");
                        b.style.setProperty("border-color", "#0284c7", "important");
                        b.style.setProperty("font-weight", "700", "important");
                    }} else if (["1D","1W","1M","3M","6M","1Y"].indexOf(txt) !== -1) {{
                        b.style.removeProperty("background");
                        b.style.removeProperty("color");
                        b.style.removeProperty("border-color");
                        b.style.removeProperty("font-weight");
                    }}
                }});
            }}
            applyStyle();
            setTimeout(applyStyle, 150);
            setTimeout(applyStyle, 400);
        </script>
    """, height=0)

    # Date range label
    ist_tz = pytz.timezone('Asia/Kolkata')
    today = datetime.now(ist_tz)
    days_map = {'1D': 1, '1W': 7, '1M': 30, '3M': 90, '6M': 180, '1Y': 365}
    range_start = today - timedelta(days=days_map.get(active, 180))

    def fmt_date(dt):
        return dt.strftime("%-d %b'%y")

    st.caption(f"**{active}** &nbsp;|&nbsp; {fmt_date(range_start)} – {fmt_date(today)} &nbsp;|&nbsp; Indexed to 100")

    with st.spinner("Loading chart..."):
        try:
            chart, chart_start, chart_end = create_comparison_chart(st.session_state.time_period, comparison_stocks)
            st.plotly_chart(chart, use_container_width=True, config={'displayModeBar': False})
        except Exception as e:
            st.error(f"Chart error: {str(e)}")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — FINANCIAL PERFORMANCE
# ══════════════════════════════════════════════════════════════════════════════

with tab2:
    st.markdown("""
        <div style="background: linear-gradient(135deg, #0a2540 0%, #1e3a5f 100%);
                    padding: 20px 28px; border-radius: 12px; margin-bottom: 20px;">
            <h2 style="color: white; margin: 0; font-size: 1.4rem;">Financial Performance — Quarterly Metrics</h2>
            <p style="color: #94a3b8; margin: 6px 0 0 0; font-size: 13px;">
                Consolidated results  •  Q4 FY25 – Q3 FY26  •  Q3 FY26 = Oct–Dec 2025
            </p>
        </div>
    """, unsafe_allow_html=True)

    # ── NBFC selector ──────────────────────────────────────────────────────
    st.markdown("**Select NBFCs to compare:**")

    # Poonawalla — greyed out disabled checkbox, always shown
    st.markdown("""
        <div style="display:inline-flex;align-items:center;gap:8px;
                    margin-bottom:10px;opacity:0.4;cursor:not-allowed;">
            <input type="checkbox" checked disabled
                   style="width:16px;height:16px;accent-color:#0284c7;">
            <span style="font-size:14px;font-weight:600;color:#0a2540;">
                Poonawalla Fincorp
                <span style="font-size:11px;font-weight:400;color:#64748b;"> — always shown</span>
            </span>
        </div>
    """, unsafe_allow_html=True)

    # Remaining 8 NBFCs — Bajaj/Shriram/L&T on by default
    TOGGLEABLE = {
        "Bajaj Finance":         True,
        "Shriram Finance":       True,
        "L&T Finance":           True,
        "Cholamandalam Finance": False,
        "Aditya Birla Capital":  False,
        "Piramal Finance":       False,
        "Muthoot Finance":       False,
        "Mahindra Finance":      False,
    }
    tcols = st.columns(4)
    selected_fin = ["Poonawalla Fincorp"]
    for i, (name, default) in enumerate(TOGGLEABLE.items()):
        with tcols[i % 4]:
            if st.checkbox(name, value=default, key=f"fin_{name}"):
                selected_fin.append(name)

    # Quality warnings
    _estimated = {"Aditya Birla Capital", "Mahindra Finance"}
    _partial   = {"Cholamandalam Finance", "Piramal Finance", "Muthoot Finance"}
    _show_est  = [n for n in selected_fin if n in _estimated]
    _show_par  = [n for n in selected_fin if n in _partial]
    if _show_est:
        st.markdown(
            f'<div style="background:#fef2f2;border-left:3px solid #dc2626;padding:8px 14px;'
            f'border-radius:6px;margin:10px 0 4px 0;font-size:12px;color:#7f1d1d;">'
            f'⚠️ <b>Partially estimated:</b> {", ".join(_show_est)} — confirm before MD presentation.</div>',
            unsafe_allow_html=True)
    if _show_par:
        st.markdown(
            f'<div style="background:#fffbeb;border-left:3px solid #f59e0b;padding:8px 14px;'
            f'border-radius:6px;margin:4px 0 4px 0;font-size:12px;color:#92400e;">'
            f'📋 <b>Note:</b> {", ".join(_show_par)} — mostly official; see source footnote below.</div>',
            unsafe_allow_html=True)

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    # ── All charts full-width stacked ──────────────────────────────────────
    for _data, _title, _ylabel, _fmt, _note in [
        (AUM,  "Assets Under Management (AUM)", "₹ Crore", "num", None),
        (NIM,  "Net Interest Margin (NIM)",      "NIM (%)", "pct",
         "⚠️ Muthoot = gold loan spread — not directly comparable to other NBFCs"),
        (GNPA, "Gross NPA",                      "GNPA (%)", "pct", None),
        (NNPA, "Net NPA",                        "NNPA (%)", "pct", None),
        (ROA,  "Return on Assets (ROA)",         "ROA (%)",  "pct",
         "⚠️ Piramal = Growth business RoAUM • Muthoot ROA estimated"),
    ]:
        st.plotly_chart(
            make_fin_chart(_data, selected_fin, _title, _ylabel, fmt=_fmt, note=_note),
            use_container_width=True, config={"displayModeBar": False}
        )

    st.markdown("""
        <div style="background:#f8fafc;border-radius:8px;padding:12px 18px;
                    margin-top:8px;border-left:3px solid #0284c7;font-size:12px;color:#64748b;">
            <b>Sources:</b> Investor presentations, BSE/NSE filings, ICICI Direct & Axis Direct analyst reports.
            Bajaj Finance consolidated (incl. BHFL). Cholamandalam GNPA per RBI norms.
            Muthoot NIM = gold loan spread. Aditya Birla AUM = NBFC + HFC lending portfolio.
            <b>⚠️ Aditya Birla Capital & Mahindra Finance values partially estimated — confirm before use.</b>
        </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TABS 3–6 — PLACEHOLDERS
# ══════════════════════════════════════════════════════════════════════════════

with tab3:
    st.header("Valuation Metrics")
    st.info("Coming soon — P/B, P/E, ROE comparison across NBFCs.")

with tab4:
    st.header("Historical Analysis")
    st.info("Coming soon — multi-year trend analysis.")

with tab5:
    st.header("Deep Dive")
    st.info("Coming soon — individual NBFC deep-dive profiles.")

with tab6:
    st.header("Rankings")
    st.info("Coming soon — scorecard rankings across all metrics.")
