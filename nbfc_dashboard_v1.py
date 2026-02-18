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
        border: 1.5px solid #cbd5e1;
        color: #475569;
        border-radius: 8px;
        padding: 8px 18px;
        font-weight: 600;
        font-size: 13px;
        transition: all 0.15s;
    }
    .stButton button:hover {
        border-color: #0284c7;
        background: #f0f9ff;
        color: #0284c7;
    }
    </style>
""", unsafe_allow_html=True)

# ─── NBFC CONSTANTS ────────────────────────────────────────────────────────────

NBFCS = {
    'Poonawalla Fincorp':   'POONAWALLA.NS',
    'Bajaj Finance':        'BAJFINANCE.NS',
    'Shriram Finance':      'SHRIRAMFIN.NS',
    'L&T Finance':          'L&TFH.NS',
    'Cholamandalam Finance':'CHOLAFIN.NS',
    'Aditya Birla Capital': 'ABCAPITAL.NS',
    'Piramal Finance':      'PEL.NS',
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
            hist = ticker.history(period='5d')
            if len(hist) > 0:
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

# ─── TAB 3: VALUATION FUNCTIONS ───────────────────────────────────────────────

@st.cache_data(ttl=3600)
def get_current_pb_ratios(selected_stocks):
    """Get current P/B ratios for selected stocks - more reliable than historical"""
    data = []
    for name in selected_stocks:
        symbol = NBFCS[name]
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            # Get current price
            hist = ticker.history(period='5d')
            if hist.empty:
                continue
            current_price = hist['Close'].iloc[-1]
            
            # Get book value - try multiple fields
            book_value = (
                info.get('bookValue') or 
                info.get('priceToBook') and current_price / info.get('priceToBook') or
                None
            )
            
            if book_value and book_value > 0:
                pb_ratio = current_price / book_value
                data.append({
                    'name': name,
                    'price': float(current_price),
                    'book_value': float(book_value),
                    'pb_ratio': float(pb_ratio),
                    'color': COLORS[name]
                })
        except Exception as e:
            print(f"Error fetching P/B for {name}: {e}")
            continue
    
    return data

def create_pb_chart(selected_stocks):
    """Create current P/B ratio comparison bar chart"""
    data = get_current_pb_ratios(selected_stocks)
    
    if not data:
        return None
    
    # Sort by P/B ratio descending
    data.sort(key=lambda x: x['pb_ratio'], reverse=True)
    
    fig = go.Figure()
    
    # Add bars
    fig.add_trace(go.Bar(
        y=[item['name'] for item in data],
        x=[item['pb_ratio'] for item in data],
        orientation='h',
        marker=dict(
            color=[item['color'] for item in data],
            line=dict(color='white', width=1)
        ),
        customdata=[[item['price'], item['book_value']] for item in data],
        hovertemplate=(
            "<b>%{y}</b><br>"
            "P/B Ratio: %{x:.2f}x<br>"
            "Price: ₹%{customdata[0]:.2f}<br>"
            "Book Value: ₹%{customdata[1]:.2f}"
            "<extra></extra>"
        ),
        text=[f"{item['pb_ratio']:.2f}x" for item in data],
        textposition='outside',
        textfont=dict(size=12, color='#1a3a52', family='JetBrains Mono', weight=600),
    ))
    
    fig.update_layout(
        title=dict(
            text=(
                '<span style="color:#0a2540;font-weight:700;font-size:16px">'
                'Current Price-to-Book Ratios</span><br>'
                '<span style="color:#94a3b8;font-size:11px;font-weight:400">'
                'Live data from Yahoo Finance • Hover for details</span>'
            ),
            font=dict(family='DM Sans, sans-serif'),
            x=0,
            xref='paper'
        ),
        xaxis_title='P/B Ratio (x)',
        yaxis_title='',
        template='plotly_white',
        height=max(400, len(data) * 60),
        showlegend=False,
        plot_bgcolor='white',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=200, r=100, t=70, b=50),
        font=dict(family='DM Sans, sans-serif', color='#1a3a52'),
        hoverlabel=dict(
            bgcolor='white',
            bordercolor='#cbd5e1',
            font=dict(family='DM Sans, sans-serif', size=12)
        ),
    )
    fig.update_xaxes(
        showgrid=True,
        gridcolor='#f1f5f9',
        showline=True,
        linecolor='#cbd5e1',
        tickfont=dict(size=12, color='#475569')
    )
    fig.update_yaxes(
        showgrid=False,
        showline=True,
        linecolor='#cbd5e1',
        tickfont=dict(size=13, color='#1a3a52', family='DM Sans', weight=600)
    )
    
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
        for row_start in range(0, len(stocks), 3):
            cols = st.columns(3)
            for col_idx, stock in enumerate(stocks[row_start:row_start + 3]):
                arrow = "▲" if stock['change_pct'] >= 0 else "▼"
                chg_class = "stock-change-pos" if stock['change_pct'] >= 0 else "stock-change-neg"
                border_color = "#16a34a" if stock['change_pct'] >= 0 else "#dc2626"
                abs_sign = "+" if stock['change_abs'] >= 0 else ""
                abs_str = f"{abs_sign}₹{stock['change_abs']:.2f}"
                pct_str = f"({abs_sign}{stock['change_pct']:.2f}%)"
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

    st.markdown('<div class="section-title">Performance Comparison<span class="section-subtitle">Indexed to 100 • Select stocks and time period below</span></div>', unsafe_allow_html=True)

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

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
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
                Consolidated results  •  Q3 FY25 – Q3 FY26  •  5 quarters for YoY comparison
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div style="background:#fefce8; border:1px solid #fbbf24; border-radius:8px;
                    padding:12px 16px; margin-bottom:18px; font-size:13px; color:#92400e;">
            <b>⚠️ Data collection in progress.</b>
            Charts show only numbers confirmed directly from official company investor
            presentation PDFs. Gaps indicate quarters where data has not yet been verified
            from source. No estimates or analyst-cited numbers are used.
        </div>
    """, unsafe_allow_html=True)

    st.markdown("**Select NBFCs to compare:**")

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

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

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
        <div style="background:#f8fafc;border-radius:8px;padding:12px 18px;
                    margin-top:8px;border-left:3px solid #0284c7;font-size:12px;color:#64748b;">
            <b>Data sourced directly from:</b> Official company investor presentation PDFs and IR pages.
            Gaps in charts = data pending PDF verification.
            Poonawalla: poonawallafincorp.com &nbsp;|&nbsp;
            Bajaj Finance: cms-assets.bajajfinserv.in &nbsp;|&nbsp;
            Piramal: piramalfinance.com &nbsp;|&nbsp;
            Aditya Birla Capital: adityabirlacapital.com &nbsp;|&nbsp;
            Remaining NBFCs: collection in progress.
        </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — VALUATION METRICS
# ══════════════════════════════════════════════════════════════════════════════

with tab3:
    st.markdown(
        '<div class="section-title">Valuation Metrics'
        '<span class="section-subtitle">Price-to-Book and Price-to-Earnings analysis</span></div>',
        unsafe_allow_html=True
    )
    
    st.markdown("#### Select NBFCs to Compare")
    col1, col2 = st.columns([3, 1])
    
    with col1:
        selected_fin = FIN_DEFAULT.copy()
        
        optional_selected = st.multiselect(
            "Add more NBFCs:",
            FIN_OPTIONAL,
            default=[],
            key='tab3_selector'
        )
        selected_fin.extend(optional_selected)
    
    st.markdown("### 📊 Price-to-Book Ratio")
    
    with st.spinner("Fetching current P/B ratios..."):
        pb_chart = create_pb_chart(selected_fin)
    
    if pb_chart:
        st.plotly_chart(pb_chart, use_container_width=True, config={'displayModeBar': False})
    else:
        st.warning("⚠️ Unable to fetch P/B data from Yahoo Finance. This may be due to API limitations. Please try again later or check with fewer stocks selected.")
    
    st.markdown("### 📊 Price-to-Earnings Ratio")
    st.info("⏳ P/E chart coming next...")

# ══════════════════════════════════════════════════════════════════════════════
# TABS 4–6 — PLACEHOLDERS
# ══════════════════════════════════════════════════════════════════════════════

with tab4:
    st.header("Historical Analysis")
    st.info("Coming soon — multi-year trend analysis.")

with tab5:
    st.header("Deep Dive")
    st.info("Coming soon — individual NBFC deep-dive profiles.")

with tab6:
    st.header("Rankings")
    st.info("Coming soon — scorecard rankings across all metrics.")

st.markdown("---")
st.caption("Data sources: Yahoo Finance • NSE • BSE  •  Dashboard updates every 5 minutes")
