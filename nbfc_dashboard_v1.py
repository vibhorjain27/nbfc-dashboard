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

# Executive terminal theme
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

    /* Base */
    .main { background: #eef0f4; font-family: 'Inter', sans-serif; }
    .block-container { padding: 0.6rem 1.6rem !important; max-width: 1600px; }

    /* Reduce Streamlit's default vertical gap between elements */
    div[data-testid="stVerticalBlock"] > div { gap: 0 !important; }

    /* Section label — subtle left-bar uppercase tag */
    .section-label {
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: #64748b;
        border-left: 2px solid #0284c7;
        padding-left: 7px;
        margin: 12px 0 8px 0;
        display: block;
    }
    .section-label-sub {
        font-size: 9px;
        font-weight: 400;
        letter-spacing: 0.04em;
        color: #94a3b8;
        margin-left: 6px;
        text-transform: none;
    }

    /* Tabs — clean underline style, no filled pills */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background: white;
        padding: 0 8px;
        border-radius: 0;
        border-bottom: 1px solid #e2e8f0;
        box-shadow: 0 1px 4px rgba(0,0,0,0.05);
        margin-bottom: 14px;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 0;
        color: #64748b;
        font-weight: 500;
        padding: 10px 18px;
        font-size: 12.5px;
        border-bottom: 2px solid transparent;
        margin-bottom: -1px;
        letter-spacing: 0.01em;
    }
    .stTabs [aria-selected="true"] {
        background: transparent !important;
        color: #0284c7 !important;
        border-bottom: 2px solid #0284c7 !important;
        font-weight: 600 !important;
    }

    /* Ticker cards */
    .ticker-card {
        background: white;
        border-radius: 5px;
        padding: 10px 13px 8px 13px;
        border-top: 3px solid #0284c7;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        height: 98px;
        box-sizing: border-box;
    }
    .ticker-name-sm {
        font-size: 14px;
        font-weight: 600;
        color: #0a2540;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .ticker-sym {
        font-family: 'JetBrains Mono', monospace;
        font-size: 10px;
        font-weight: 400;
        color: #94a3b8;
        letter-spacing: 0.05em;
        margin-top: 2px;
    }
    .ticker-price {
        font-family: 'JetBrains Mono', monospace;
        font-size: 18px;
        font-weight: 700;
        color: #0a2540;
        line-height: 1.1;
    }
    .ticker-pos { color: #16a34a; font-size: 11px; font-weight: 600; }
    .ticker-neg { color: #dc2626; font-size: 11px; font-weight: 600; }
    .ticker-meta {
        font-size: 10px;
        color: #94a3b8;
        margin-top: 5px;
        border-top: 1px solid #f1f5f9;
        padding-top: 4px;
        font-family: 'JetBrains Mono', monospace;
    }

    /* Period buttons */
    .stButton button {
        background: white;
        border: 1px solid #e2e8f0;
        color: #64748b;
        border-radius: 4px;
        padding: 3px 10px;
        font-weight: 500;
        font-size: 11.5px;
        transition: all 0.1s;
        height: 28px !important;
        line-height: 1 !important;
    }
    .stButton button:hover {
        border-color: #0284c7;
        color: #0284c7;
        background: #f0f9ff;
    }

    /* Tighten checkbox rows */
    .stCheckbox { margin-bottom: -2px; }
    .stCheckbox label { font-size: 12.5px; color: #475569; }

    /* Tighten caption */
    .stCaption p { font-size: 10.5px !important; color: #94a3b8 !important; margin: 0 !important; }

    /* Thin divider */
    hr { margin: 8px 0; border-color: #e2e8f0; }

    /* Warning / info banners — tighter */
    .stAlert { padding: 8px 12px !important; font-size: 12px; border-radius: 5px; }
    </style>
""", unsafe_allow_html=True)

# ─── NBFC CONSTANTS ────────────────────────────────────────────────────────────

NBFCS = {
    'Poonawalla Fincorp':   'POONAWALLA.NS',
    'Bajaj Finance':        'BAJFINANCE.NS',
    'Shriram Finance':      'SHRIRAMFIN.NS',
    'L&T Finance':          'LTF.NS',
    'Cholamandalam Finance':'CHOLAFIN.NS',
    'Aditya Birla Capital': 'ABCAPITAL.NS',
    'Piramal Finance':      'PIRAMALFIN.NS',
    'Muthoot Finance':      'MUTHOOTFIN.NS',
    'Mahindra Finance':     'M&MFIN.NS',
}

COLORS = {
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

DEFAULT_COMPARISON = ['Bajaj Finance', 'Shriram Finance', 'L&T Finance']

# ─── FINANCIAL DATA (QUARTERLY) ───────────────────────────────────────────────

QUARTERS = ['Q3 FY25', 'Q4 FY25', 'Q1 FY26', 'Q2 FY26', 'Q3 FY26']

AUM = {
    # [Q3 FY25, Q4 FY25, Q1 FY26, Q2 FY26, Q3 FY26]  — ₹ Crore
    'Poonawalla Fincorp':   [30984,  35631,  None,  None,  55017 ],
    'Bajaj Finance':        [None,   None,   None,  None,  None  ],
    'Shriram Finance':      [None,   None,   None,  None,  None  ],
    'L&T Finance':          [None,   None,   None,  None,  None  ],
    'Cholamandalam Finance':[None,   None,   None,  None,  None  ],
    'Aditya Birla Capital': [None,   None,   None,  None,  None  ],
    'Piramal Finance':      [None,   None,   None,  None,  None  ],
    'Muthoot Finance':      [None,   None,   None,  None,  None  ],
    'Mahindra Finance':     [None,   None,   None,  None,  None  ],
}

NIM = {
    # [Q3 FY25, Q4 FY25, Q1 FY26, Q2 FY26, Q3 FY26]  — % (Net Interest Margin)
    'Poonawalla Fincorp':   [None,  None,  None,  None,  None ],
    'Bajaj Finance':        [None,  None,  None,  None,  None ],
    'Shriram Finance':      [None,  None,  None,  None,  None ],
    'L&T Finance':          [None,  None,  None,  None,  None ],
    'Cholamandalam Finance':[None,  None,  None,  None,  None ],
    'Aditya Birla Capital': [None,  None,  None,  None,  None ],
    'Piramal Finance':      [None,  None,  None,  None,  None ],
    'Muthoot Finance':      [None,  None,  None,  None,  None ],
    'Mahindra Finance':     [None,  None,  None,  None,  None ],
}

GNPA = {
    # [Q3 FY25, Q4 FY25, Q1 FY26, Q2 FY26, Q3 FY26]  — % per RBI norms
    'Poonawalla Fincorp':   [1.85,  1.84,  None,  None,  1.51 ],
    'Bajaj Finance':        [None,  None,  1.03,  1.24,  None ],
    'Shriram Finance':      [None,  None,  None,  None,  None ],
    'L&T Finance':          [None,  None,  None,  None,  None ],
    'Cholamandalam Finance':[None,  None,  None,  None,  None ],
    'Piramal Finance':      [None,  2.80,  2.80,  2.60,  None ],
    'Muthoot Finance':      [None,  None,  None,  None,  None ],
    'Aditya Birla Capital': [None,  None,  None,  None,  None ],
    'Mahindra Finance':     [None,  None,  None,  None,  None ],
}

NNPA = {
    # [Q3 FY25, Q4 FY25, Q1 FY26, Q2 FY26, Q3 FY26]  — % per RBI norms
    'Poonawalla Fincorp':   [0.81,  0.85,  None,  None,  0.80 ],
    'Bajaj Finance':        [None,  None,  0.50,  0.60,  None ],
    'Shriram Finance':      [None,  None,  None,  None,  None ],
    'L&T Finance':          [None,  None,  None,  None,  None ],
    'Cholamandalam Finance':[None,  None,  None,  None,  None ],
    'Piramal Finance':      [None,  1.90,  2.00,  1.80,  None ],
    'Muthoot Finance':      [None,  None,  None,  None,  None ],
    'Aditya Birla Capital': [None,  None,  None,  None,  None ],
    'Mahindra Finance':     [None,  None,  None,  None,  None ],
}

ROA = {
    # [Q3 FY25, Q4 FY25, Q1 FY26, Q2 FY26, Q3 FY26]  — % annualised PAT/avg assets
    'Poonawalla Fincorp':   [None,  None,  None,  None,  1.20 ],
    'Bajaj Finance':        [None,  None,  4.5,   None,  None ],
    'Shriram Finance':      [None,  None,  None,  None,  None ],
    'L&T Finance':          [None,  None,  None,  None,  None ],
    'Cholamandalam Finance':[None,  None,  None,  None,  None ],
    'Piramal Finance':      [None,  None,  None,  None,  None ],
    'Muthoot Finance':      [None,  None,  None,  None,  None ],
    'Aditya Birla Capital': [None,  2.25,  None,  None,  None ],
    'Mahindra Finance':     [None,  None,  None,  None,  None ],
}

FIN_COLORS = COLORS
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

@st.cache_data(ttl=300)
def get_current_prices():
    data = []
    for name, symbol in NBFCS.items():
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period='1mo')
            if hist.empty:
                print(f"⚠️  No data for {name} ({symbol})")
                continue
            current = hist['Close'].iloc[-1]
            prev = hist['Close'].iloc[-2] if len(hist) > 1 else current
            change_abs = current - prev
            change_pct = (change_abs / prev) * 100
            volume = int(hist['Volume'].iloc[-1]) if 'Volume' in hist.columns else 0
            data.append({
                'name': name,
                'symbol': symbol.replace('.NS', ''),
                'price': current,
                'change_abs': change_abs,
                'change_pct': change_pct,
                'volume': volume,
            })
        except Exception as e:
            print(f"❌ Error fetching {name} ({symbol}): {e}")
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
                print(f"⚠️  No data for {name} in period {yf_period}")
                continue
            end_date = data.index[-1]
            start_date = end_date - timedelta(days=days)
            filtered = data[data.index >= start_date]
            if filtered.empty or len(filtered) < 2:
                print(f"⚠️  Insufficient data for {name} in selected period")
                continue
            prices = filtered['Close']
            indexed = (prices / prices.iloc[0]) * 100
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
        except Exception as e:
            print(f"❌ Error processing {name}: {e}")
            continue

    performance_data.sort(key=lambda x: x['performance'], reverse=True)

    if performance_data:
        all_vals = [v for item in performance_data for v in item['values']]
        y_range = max(all_vals) - min(all_vals)
        MIN_GAP = max(0.5, min(4.0, y_range * 0.15))
    else:
        MIN_GAP = 2.0

    label_positions = [item['end_y'] for item in performance_data]

    for i in range(1, len(label_positions)):
        if label_positions[i - 1] - label_positions[i] < MIN_GAP:
            label_positions[i] = label_positions[i - 1] - MIN_GAP

    for i in range(len(label_positions) - 2, -1, -1):
        if label_positions[i] - label_positions[i + 1] < MIN_GAP:
            label_positions[i] = label_positions[i + 1] + MIN_GAP

    for i, item in enumerate(performance_data):
        fig.add_trace(go.Scatter(
            x=item['dates'],
            y=item['values'],
            name=item['name'],
            line=dict(color=item['color'], width=2.5),
            mode='lines',
            hovertemplate=f"<b>{item['name']}</b><br>%{{x|%d %b %Y}}<br>%{{y:.1f}}<extra></extra>"
        ))

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
            font=dict(family='Inter, sans-serif'), x=0),
        xaxis_title='Date',
        yaxis_title='Indexed Value (Base = 100)',
        template='plotly_white',
        height=520,
        hovermode='x unified',
        showlegend=False,
        plot_bgcolor='white',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=60, r=200, t=60, b=50),
        font=dict(family='Inter, sans-serif', color='#1a3a52'),
    )
    fig.update_xaxes(showgrid=True, gridcolor='#f1f5f9', showline=True, linecolor='#cbd5e1')
    fig.update_yaxes(showgrid=True, gridcolor='#f1f5f9', showline=True, linecolor='#cbd5e1')
    return fig, actual_start_date, actual_end_date

def make_fin_chart(metric_data, selected, title, ylabel, fmt='pct', note=None):
    fig = go.Figure()

    series = []
    for name in selected:
        if name not in metric_data:
            continue
        vals = metric_data[name]
        confirmed = [v for v in vals if v is not None]
        if not confirmed:
            continue
        last_confirmed = confirmed[-1]
        last_idx = max(i for i, v in enumerate(vals) if v is not None)
        series.append({
            'name': name,
            'values': vals,
            'avg': sum(confirmed) / len(confirmed),
            'last': last_confirmed,
            'last_idx': last_idx,
            'color': FIN_COLORS[name],
        })
    series.sort(key=lambda x: x['avg'], reverse=True)

    for s in series:
        val_fmt = '%{y:.2f}%' if fmt == 'pct' else '₹%{y:,.0f} Cr'
        fig.add_trace(go.Scatter(
            x=QUARTERS,
            y=s['values'],
            name=s['name'],
            mode='lines+markers',
            connectgaps=False,
            line=dict(color=s['color'], width=2.5),
            marker=dict(size=8, color=s['color']),
            hovertemplate=f"<b>{s['name']}</b>  {val_fmt}<extra></extra>",
        ))

    label_y = [s['last'] for s in series]
    all_vals = [v for s in series for v in s['values'] if v is not None]
    y_range  = max(all_vals) - min(all_vals) if len(all_vals) > 1 else 1
    MIN_GAP  = max(y_range * 0.12, 0.25)

    for i in range(1, len(label_y)):
        if label_y[i - 1] - label_y[i] < MIN_GAP:
            label_y[i] = label_y[i - 1] - MIN_GAP
    for i in range(len(label_y) - 2, -1, -1):
        if label_y[i] - label_y[i + 1] < MIN_GAP:
            label_y[i] = label_y[i + 1] + MIN_GAP

    for i, s in enumerate(series):
        val_str = f"{s['last']:.2f}%" if fmt == 'pct' else f"₹{s['last']:,.0f} Cr"
        x_anchor = QUARTERS[s['last_idx']]
        if abs(s['last'] - label_y[i]) > MIN_GAP * 0.3:
            fig.add_shape(type='line',
                x0=x_anchor, x1=x_anchor,
                y0=s['last'], y1=label_y[i],
                line=dict(color=s['color'], width=1, dash='dot'),
                xref='x', yref='y')
        fig.add_annotation(
            x=x_anchor, y=label_y[i],
            text=f"<b style='color:{s['color']}'>{s['name']}</b>  {val_str}",
            showarrow=False,
            xanchor='left', xshift=14,
            font=dict(size=11, color=s['color']),
            bgcolor='rgba(255,255,255,0.95)',
            bordercolor=s['color'],
            borderwidth=1,
            borderpad=4,
        )

    title_html = (
        f'<span style="color:#0a2540;font-weight:700;font-size:16px">{title}</span>'
    )
    if note:
        title_html += (
            f'<br><span style="color:#94a3b8;font-size:11px;font-weight:400">{note}</span>'
        )

    fig.update_layout(
        title=dict(text=title_html, font=dict(family='Inter, sans-serif'), x=0, xref='paper'),
        yaxis_title=ylabel,
        template='plotly_white',
        height=420,
        hovermode='x unified',
        showlegend=False,
        plot_bgcolor='white',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=60, r=240, t=70, b=50),
        font=dict(family='Inter, sans-serif', color='#1a3a52'),
        hoverlabel=dict(bgcolor='white', bordercolor='#cbd5e1',
                        font=dict(family='Inter, sans-serif', size=12)),
    )
    fig.update_xaxes(showgrid=True, gridcolor='#f1f5f9', showline=True, linecolor='#cbd5e1',
                     tickfont=dict(size=12, color='#475569'))
    fig.update_yaxes(showgrid=True, gridcolor='#f1f5f9', showline=True, linecolor='#cbd5e1',
                     tickfont=dict(size=12, color='#475569'))
    return fig

# ─── TAB 3: VALUATION FUNCTIONS ─────────────────────────────────────────────
# (placeholder — being rebuilt from scratch after data source analysis)

# ─── HEADER ────────────────────────────────────────────────────────────────────

ist = pytz.timezone('Asia/Kolkata')
current_time = datetime.now(ist)

st.markdown(f"""
    <div style="display:flex; justify-content:space-between; align-items:center;
                padding:8px 0 10px 0; border-bottom:1px solid #dde1e8; margin-bottom:0;">
        <div style="display:flex; align-items:baseline; gap:10px;">
            <span style="font-size:16px; font-weight:700; color:#0a2540; letter-spacing:-0.01em; font-family:'Inter',sans-serif;">
                NBFC Dashboard
            </span>
            <span style="font-size:9.5px; color:#94a3b8; font-family:'JetBrains Mono',monospace;
                         background:#e8edf3; padding:2px 7px; border-radius:3px; letter-spacing:0.06em;">
                NSE &nbsp;·&nbsp; INDIA
            </span>
        </div>
        <div style="font-family:'JetBrains Mono',monospace; font-size:10.5px; color:#64748b; text-align:right; line-height:1.6;">
            {current_time.strftime('%d %b %Y')}
            <span style="color:#94a3b8; margin-left:6px;">{current_time.strftime('%H:%M IST')}</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# ─── TABS ──────────────────────────────────────────────────────────────────────

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Market",
    "Financials",
    "Valuation",
    "Historical",
    "Deep Dive",
    "Rankings",
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — MARKET OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════

with tab1:
    st.markdown('<span class="section-label">Stock Prices <span class="section-label-sub">Live NSE · refreshes every 5 min</span></span>', unsafe_allow_html=True)

    with st.spinner("Fetching live prices..."):
        stocks = get_current_prices()

    if not stocks:
        st.error("Unable to fetch stock data. Please try again.")
    else:
        for row_start in range(0, len(stocks), 3):
            cols = st.columns(3, gap="small")
            for col_idx, stock in enumerate(stocks[row_start:row_start + 3]):
                arrow = "▲" if stock['change_pct'] >= 0 else "▼"
                chg_class = "ticker-pos" if stock['change_pct'] >= 0 else "ticker-neg"
                abs_sign = "+" if stock['change_abs'] >= 0 else ""
                abs_str = f"{abs_sign}₹{stock['change_abs']:.2f}"
                pct_str = f"{abs_sign}{stock['change_pct']:.2f}%"
                vol = stock['volume']
                if vol >= 10_000_000:
                    vol_str = f"{vol/10_000_000:.1f}Cr"
                elif vol >= 100_000:
                    vol_str = f"{vol/100_000:.1f}L"
                elif vol >= 1000:
                    vol_str = f"{vol/1000:.0f}K"
                else:
                    vol_str = str(vol) if vol > 0 else "—"

                border_color = "#16a34a" if stock['change_pct'] >= 0 else "#dc2626"

                with cols[col_idx]:
                    st.markdown(f"""
                        <div class="ticker-card" style="border-top-color:{border_color};">
                            <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                                <div>
                                    <div class="ticker-name-sm">{stock['name']}</div>
                                    <div class="ticker-sym">{stock['symbol']}</div>
                                </div>
                                <div style="text-align:right;">
                                    <div class="ticker-price">₹{stock['price']:,.0f}</div>
                                    <div class="{chg_class}">{arrow} {pct_str}</div>
                                </div>
                            </div>
                            <div class="ticker-meta">{abs_str} &nbsp;·&nbsp; Vol {vol_str}</div>
                        </div>
                    """, unsafe_allow_html=True)
            st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
    st.markdown('<span class="section-label">Performance Comparison <span class="section-label-sub">Indexed to 100 · select stocks and period below</span></span>', unsafe_allow_html=True)

    other_stocks = [n for n in NBFCS if n != 'Poonawalla Fincorp']
    col1, col2, col3 = st.columns(3)
    cols_map = [col1, col2, col3]

    selected_others = []
    with col1:
        st.markdown("<span style='font-size:12px;font-weight:600;color:#334155;'>Poonawalla Fincorp <span style='font-weight:400;color:#94a3b8;font-size:11px;'>always shown</span></span>", unsafe_allow_html=True)
    for i, name in enumerate(other_stocks):
        with cols_map[i % 3]:
            is_default = name in DEFAULT_COMPARISON
            if st.checkbox(name, value=is_default, key=f"chk_{name}"):
                selected_others.append(name)

    comparison_stocks = ['Poonawalla Fincorp'] + selected_others

    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
    periods = ['1D', '1W', '1M', '3M', '6M', '1Y']
    active = st.session_state.time_period

    btn_cols = st.columns(6)
    for i, p in enumerate(periods):
        with btn_cols[i]:
            if st.button(p, key=f"pb_{p}", use_container_width=True):
                st.session_state.time_period = p
                st.rerun()

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

    ist_tz = pytz.timezone('Asia/Kolkata')
    today = datetime.now(ist_tz)
    days_map = {'1D': 1, '1W': 7, '1M': 30, '3M': 90, '6M': 180, '1Y': 365}
    range_start = today - timedelta(days=days_map.get(active, 180))

    def fmt_date(dt):
        return dt.strftime("%-d %b'%y")

    st.caption(f"**{active}** · {fmt_date(range_start)} – {fmt_date(today)} · Indexed to 100")

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
        <div style="display:flex; justify-content:space-between; align-items:center;
                    padding:10px 14px; background:white; border-radius:5px;
                    border-left:3px solid #0284c7; margin-bottom:10px;
                    box-shadow:0 1px 2px rgba(0,0,0,0.05);">
            <div>
                <span style="font-size:13px; font-weight:700; color:#0a2540;">Financial Performance — Quarterly Metrics</span>
                <span style="font-size:10.5px; color:#94a3b8; margin-left:12px;">Q3 FY25 – Q3 FY26 &nbsp;·&nbsp; 5 quarters</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div style="background:#fffbeb; border:1px solid #fbbf24; border-radius:4px;
                    padding:8px 12px; margin-bottom:10px; font-size:11.5px; color:#92400e;">
            <b>⚠ Data collection in progress.</b>
            Charts show only numbers confirmed from official investor presentation PDFs.
            Gaps = quarters not yet verified. No estimates used.
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<span class="section-label">Select NBFCs to compare</span>', unsafe_allow_html=True)

    st.markdown("""
        <div style="display:inline-flex;align-items:center;gap:8px;
                    margin-bottom:6px;opacity:0.4;cursor:not-allowed;">
            <input type="checkbox" checked disabled
                   style="width:14px;height:14px;accent-color:#0284c7;">
            <span style="font-size:12.5px;font-weight:600;color:#0a2540;">
                Poonawalla Fincorp
                <span style="font-size:10.5px;font-weight:400;color:#64748b;"> — always shown</span>
            </span>
        </div>
    """, unsafe_allow_html=True)

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

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    for _data, _title, _ylabel, _fmt, _note in [
        (AUM,  "Assets Under Management (AUM)", "₹ Crore",  "num", None),
        (NIM,  "Net Interest Margin (NIM)",      "NIM (%)",  "pct",
         "Data collection in progress — NIM pending PDF verification for all NBFCs"),
        (GNPA, "Gross NPA",                      "GNPA (%)", "pct", None),
        (NNPA, "Net NPA",                        "NNPA (%)", "pct", None),
        (ROA,  "Return on Assets (ROA)",         "ROA (%)",  "pct",
         "Note: Bajaj Finance ROA = annualised PAT / avg AUF (their standard methodology)"),
    ]:
        st.plotly_chart(
            make_fin_chart(_data, selected_fin, _title, _ylabel, fmt=_fmt, note=_note),
            use_container_width=True, config={"displayModeBar": False}
        )

    st.markdown("""
        <div style="background:#f8fafc;border-radius:4px;padding:8px 14px;
                    margin-top:4px;border-left:2px solid #0284c7;font-size:11px;color:#64748b;">
            <b>Data sourced from:</b> Official investor presentation PDFs and IR pages.
            Gaps = pending verification. &nbsp;
            Poonawalla: poonawallafincorp.com &nbsp;·&nbsp;
            Bajaj Finance: cms-assets.bajajfinserv.in &nbsp;·&nbsp;
            Piramal: piramalfinance.com &nbsp;·&nbsp;
            Aditya Birla Capital: adityabirlacapital.com
        </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — VALUATION METRICS
# ══════════════════════════════════════════════════════════════════════════════

with tab3:
    st.info("Valuation Metrics — rebuilding with reliable data sources. Coming soon.")

# ══════════════════════════════════════════════════════════════════════════════
# TABS 4–6 — PLACEHOLDERS
# ══════════════════════════════════════════════════════════════════════════════

with tab4:
    st.markdown('<span class="section-label">Historical Analysis</span>', unsafe_allow_html=True)
    st.info("Coming soon — multi-year trend analysis.")

with tab5:
    st.markdown('<span class="section-label">Deep Dive</span>', unsafe_allow_html=True)
    st.info("Coming soon — individual NBFC deep-dive profiles.")

with tab6:
    st.markdown('<span class="section-label">Rankings</span>', unsafe_allow_html=True)
    st.info("Coming soon — scorecard rankings across all metrics.")

st.markdown("""
    <div style="font-size:10px; color:#94a3b8; font-family:'JetBrains Mono',monospace;
                border-top:1px solid #e2e8f0; padding-top:8px; margin-top:12px;">
        Yahoo Finance &nbsp;·&nbsp; NSE &nbsp;·&nbsp; BSE &nbsp;·&nbsp; Updates every 5 min
    </div>
""", unsafe_allow_html=True)
