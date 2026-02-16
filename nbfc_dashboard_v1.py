import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import yfinance as yf

# Page configuration
st.set_page_config(
    page_title="NBFC Dashboard - Poonawalla",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Professional Mobile-Responsive Theme
st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Main container */
    .main {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        padding: 1rem;
    }
    
    /* Remove default Streamlit padding on mobile */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 100%;
    }
    
    /* Headers */
    h1 {
        color: #0c4a6e;
        font-size: 1.75rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    h2, h3 {
        color: #0c4a6e;
        font-weight: 600;
    }
    
    /* Mobile responsive headers */
    @media (max-width: 768px) {
        h1 {
            font-size: 1.5rem;
        }
        h2 {
            font-size: 1.25rem;
        }
        h3 {
            font-size: 1.1rem;
        }
    }
    
    /* Tabs - Mobile Friendly */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: white;
        padding: 8px;
        border-radius: 12px;
        overflow-x: auto;
        flex-wrap: nowrap;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 8px;
        color: #64748b;
        font-weight: 600;
        padding: 10px 16px;
        font-size: 13px;
        white-space: nowrap;
        min-width: fit-content;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: #f1f5f9;
        color: #0284c7;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
        color: white !important;
    }
    
    /* Table Styling - CRITICAL FIX FOR MOBILE */
    .stDataFrame {
        width: 100%;
    }
    
    /* Force light background on table */
    .stDataFrame, .stDataFrame > div, .stDataFrame table {
        background-color: white !important;
        color: #1e293b !important;
    }
    
    .stDataFrame th {
        background-color: #f8fafc !important;
        color: #0c4a6e !important;
        font-weight: 600 !important;
        padding: 12px 8px !important;
        font-size: 12px !important;
    }
    
    .stDataFrame td {
        background-color: white !important;
        color: #334155 !important;
        padding: 12px 8px !important;
        font-size: 13px !important;
    }
    
    /* Alternating row colors */
    .stDataFrame tr:nth-child(even) td {
        background-color: #f9fafb !important;
    }
    
    /* Mobile table adjustments */
    @media (max-width: 768px) {
        .stDataFrame {
            font-size: 11px !important;
        }
        .stDataFrame th, .stDataFrame td {
            padding: 8px 4px !important;
        }
    }
    
    /* Buttons - Mobile Optimized */
    .stButton button {
        background: white;
        color: #475569;
        border: 2px solid #e2e8f0;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
        font-size: 14px;
        width: 100%;
        transition: all 0.2s;
    }
    
    .stButton button:hover {
        border-color: #0284c7;
        color: #0284c7;
        background: #f0f9ff;
    }
    
    /* Active button state */
    .stButton button:active {
        background: #0284c7;
        color: white;
        border-color: #0284c7;
    }
    
    /* Mobile button sizing */
    @media (max-width: 768px) {
        .stButton button {
            padding: 12px 16px;
            font-size: 13px;
        }
    }
    
    /* Checkbox styling */
    .stCheckbox {
        background: white;
        padding: 12px;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
    }
    
    /* Plotly charts mobile responsive */
    .js-plotly-plot {
        width: 100% !important;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Caption styling */
    .caption {
        color: #64748b;
        font-size: 0.875rem;
    }
    
    /* Spinner color */
    .stSpinner > div {
        border-top-color: #0284c7 !important;
    }
    
    /* Mobile spacing */
    @media (max-width: 768px) {
        .main {
            padding: 0.5rem;
        }
        .block-container {
            padding: 1rem;
        }
    }
    </style>
""", unsafe_allow_html=True)

# NBFC Configuration
NBFCS = {
    'Poonawalla Fincorp': 'POONAWALLA.NS',
    'Bajaj Finance': 'BAJFINANCE.NS',
    'L&T Finance': 'LTF.NS',
    'Shriram Finance': 'SHRIRAMFIN.NS',
    'Cholamandalam Finance': 'CHOLAFIN.NS',
    'Aditya Birla Capital': 'ABCAPITAL.NS',
    'Piramal Finance': 'PIRAMALFIN.NS',
    'Muthoot Finance': 'MUTHOOTFIN.NS',
    'Mahindra Finance': 'M&MFIN.NS'
}

BANK_NIFTY = '^NSEBANK'

# Vibrant color palette for charts
NBFC_COLORS = {
    'Poonawalla Fincorp': '#0284c7',
    'Bajaj Finance': '#dc2626',
    'L&T Finance': '#16a34a',
    'Shriram Finance': '#ea580c',
    'Cholamandalam Finance': '#9333ea',
    'Aditya Birla Capital': '#0891b2',
    'Piramal Finance': '#be123c',
    'Muthoot Finance': '#65a30d',
    'Mahindra Finance': '#7c3aed'
}

# Session state
if 'time_period' not in st.session_state:
    st.session_state.time_period = '1Y'
if 'index_to_100' not in st.session_state:
    st.session_state.index_to_100 = False

@st.cache_data(ttl=3600)
def fetch_stock_data(symbol, period='1y'):
    """Fetch stock data with error handling"""
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period=period)
        return data
    except Exception as e:
        return None

@st.cache_data(ttl=3600)
def get_current_prices():
    """Get current price data for all NBFCs"""
    data = []
    
    for name, symbol in NBFCS.items():
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period='5d')
            
            if len(hist) > 0:
                current_price = hist['Close'].iloc[-1]
                prev_close = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
                change = current_price - prev_close
                change_pct = (change / prev_close) * 100
                
                try:
                    info = ticker.info
                    market_cap = info.get('marketCap', 0) / 10000000
                except:
                    market_cap = 0
                
                data.append({
                    'Company': name,
                    'Symbol': symbol.replace('.NS', ''),
                    'Price': current_price,
                    'Change': change,
                    'Change %': change_pct,
                    'Market Cap': market_cap
                })
        except:
            continue
            
    return pd.DataFrame(data)

def get_period_days(period):
    """Convert period to days"""
    return {'1D': 1, '1W': 7, '1M': 30, '3M': 90, '6M': 180, '1Y': 365}.get(period, 365)

def create_stock_chart(time_period, index_to_100=False):
    """Create multi-line stock chart"""
    fig = go.Figure()
    
    days = get_period_days(time_period)
    yf_period = '5d' if days <= 7 else '1mo' if days <= 30 else '3mo' if days <= 90 else '1y'
    
    for name, symbol in NBFCS.items():
        try:
            data = fetch_stock_data(symbol, period=yf_period)
            if data is not None and not data.empty:
                end_date = data.index[-1]
                start_date = end_date - timedelta(days=days)
                mask = (data.index >= start_date)
                filtered = data[mask]
                
                if not filtered.empty:
                    prices = filtered['Close']
                    
                    if index_to_100:
                        prices = (prices / prices.iloc[0]) * 100
                        pct_change = prices.iloc[-1] - 100
                        label = f"{name} ({pct_change:+.1f}%)"
                        yaxis = 'Indexed Value (Base = 100)'
                    else:
                        label = name
                        yaxis = 'Price (₹)'
                    
                    fig.add_trace(go.Scatter(
                        x=filtered.index,
                        y=prices,
                        name=label,
                        line=dict(color=NBFC_COLORS[name], width=2.5),
                        mode='lines',
                        hovertemplate=f'<b>{name}</b><br>Date: %{{x|%d %b %Y}}<br>Value: ₹%{{y:,.2f}}<extra></extra>'
                    ))
        except:
            continue
    
    fig.update_layout(
        title=dict(text=f'<b>Stock Price Performance - {time_period}</b>', font=dict(size=18, color='#0c4a6e')),
        xaxis_title='Date',
        yaxis_title=yaxis if index_to_100 else 'Price (₹)',
        template='plotly_white',
        height=450,
        hovermode='x unified',
        legend=dict(orientation="v", yanchor="top", y=1, xanchor="left", x=1.01, font=dict(size=10)),
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=50, r=120, t=50, b=50),
        font=dict(color='#334155')
    )
    
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#f1f5f9')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#f1f5f9')
    
    return fig

def create_mcap_chart(time_period):
    """Create market cap chart"""
    fig = go.Figure()
    
    days = get_period_days(time_period)
    yf_period = '5d' if days <= 7 else '1mo' if days <= 30 else '3mo' if days <= 90 else '1y'
    
    for name, symbol in NBFCS.items():
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=yf_period)
            
            if not hist.empty:
                end_date = hist.index[-1]
                start_date = end_date - timedelta(days=days)
                mask = (hist.index >= start_date)
                filtered = hist[mask]
                
                if not filtered.empty:
                    try:
                        info = ticker.info
                        shares = info.get('sharesOutstanding', 0)
                        if shares > 0:
                            mcap = (filtered['Close'] * shares) / 10000000
                            
                            fig.add_trace(go.Scatter(
                                x=filtered.index,
                                y=mcap,
                                name=name,
                                line=dict(color=NBFC_COLORS[name], width=2.5),
                                mode='lines',
                                hovertemplate=f'<b>{name}</b><br>Date: %{{x|%d %b %Y}}<br>Market Cap: ₹%{{y:,.0f}} Cr<extra></extra>'
                            ))
                    except:
                        continue
        except:
            continue
    
    fig.update_layout(
        title=dict(text=f'<b>Market Capitalization - {time_period}</b>', font=dict(size=18, color='#0c4a6e')),
        xaxis_title='Date',
        yaxis_title='Market Cap (₹ Crores)',
        template='plotly_white',
        height=450,
        hovermode='x unified',
        legend=dict(orientation="v", yanchor="top", y=1, xanchor="left", x=1.01, font=dict(size=10)),
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=50, r=120, t=50, b=50),
        font=dict(color='#334155')
    )
    
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#f1f5f9')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#f1f5f9')
    
    return fig

# Main App
st.title("📊 NBFC Dashboard")
st.caption(f"Live market data • Updated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")

# Tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📈 Market",
    "💼 Financial", 
    "💰 Valuation",
    "📊 History",
    "🔍 Deep Dive",
    "🏆 Rankings"
])

# TAB 1: Market Overview
with tab1:
    with st.spinner("🔄 Fetching latest data..."):
        price_df = get_current_prices()
    
    if price_df.empty:
        st.error("❌ Unable to fetch stock data")
    else:
        # Current Prices Table
        st.markdown("### 💹 Current Prices")
        
        # Format display data with colors
        display_data = []
        for _, row in price_df.iterrows():
            arrow = '↑' if row['Change %'] >= 0 else '↓'
            display_data.append({
                'Company': row['Company'],
                'Symbol': row['Symbol'],
                'Price': f"₹{row['Price']:,.2f}",
                'Change': f"{arrow} {abs(row['Change %']):.2f}%",
                'Market Cap': f"₹{row['Market Cap']:,.0f} Cr" if row['Market Cap'] > 0 else 'N/A'
            })
        
        display_df = pd.DataFrame(display_data)
        
        st.dataframe(
            display_df,
            hide_index=True,
            use_container_width=True,
            height=400
        )
        
        st.markdown("---")
        
        # Time Period Buttons
        st.markdown("### 📅 Time Period")
        
        cols = st.columns(6)
        periods = ['1D', '1W', '1M', '3M', '6M', '1Y']
        
        for i, period in enumerate(periods):
            with cols[i]:
                if st.button(period, key=f"btn_{period}", use_container_width=True):
                    st.session_state.time_period = period
                    st.rerun()
        
        st.caption(f"*Selected: {st.session_state.time_period}*")
        
        # Index to 100 toggle
        st.session_state.index_to_100 = st.checkbox(
            "📊 Show Relative Performance (Index to 100)",
            value=st.session_state.index_to_100
        )
        
        st.markdown("---")
        
        # Charts
        with st.spinner(f"📈 Loading {st.session_state.time_period} data..."):
            st.plotly_chart(
                create_stock_chart(st.session_state.time_period, st.session_state.index_to_100),
                use_container_width=True,
                config={'displayModeBar': False}
            )
        
        st.markdown("---")
        
        with st.spinner(f"💰 Loading market cap data..."):
            st.plotly_chart(
                create_mcap_chart(st.session_state.time_period),
                use_container_width=True,
                config={'displayModeBar': False}
            )

# Other tabs - placeholders
with tab2:
    st.header("💼 Financial Performance")
    st.info("Quarterly metrics coming soon")
    
with tab3:
    st.header("💰 Valuation Metrics")
    st.info("Valuation ratios coming soon")
    
with tab4:
    st.header("📊 Historical Analysis")
    st.info("Historical analysis coming soon")
    
with tab5:
    st.header("🔍 Deep Dive")
    st.info("Individual NBFC analysis coming soon")
    
with tab6:
    st.header("🏆 Rankings")
    st.info("Rankings coming soon")

# Sidebar
with st.sidebar:
    st.markdown("### 📊 Dashboard Info")
    st.markdown(f"""
    - **NBFCs:** 9 tracked
    - **Period:** {st.session_state.time_period}
    - **Source:** Yahoo Finance
    - **Refresh:** Hourly
    """)
    
    st.markdown("---")
    st.markdown("### 🏢 Companies")
    for name in NBFCS.keys():
        st.caption(f"• {name}")
    
    st.markdown("---")
    st.caption("*Built for Poonawalla Fincorp*")
    st.caption(f"*v2.1 Mobile | {datetime.now().year}*")
