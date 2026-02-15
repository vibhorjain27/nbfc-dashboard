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
    initial_sidebar_state="expanded"
)

# Professional Financial Dashboard Theme
st.markdown("""
    <style>
    /* Import professional fonts */
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=JetBrains+Mono:wght@400;600&display=swap');
    
    /* Main background */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #f0f4f8 100%);
        font-family: 'DM Sans', sans-serif;
    }
    
    /* Headers */
    h1, h2, h3 {
        font-family: 'DM Sans', sans-serif;
        color: #0c4a6e;
        font-weight: 700;
    }
    
    /* Tab styling - Financial platform style */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background-color: white;
        padding: 8px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border-radius: 8px;
        color: #64748b;
        font-weight: 600;
        padding: 12px 24px;
        font-size: 14px;
        transition: all 0.2s ease;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #f1f5f9;
        color: #0284c7;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
        color: white;
        box-shadow: 0 2px 6px rgba(2, 132, 199, 0.3);
    }
    
    /* Data table styling */
    .dataframe {
        font-family: 'JetBrains Mono', monospace;
        font-size: 13px;
    }
    
    /* Metric values */
    [data-testid="stMetricValue"] {
        font-size: 28px;
        font-weight: 700;
        font-family: 'JetBrains Mono', monospace;
    }
    
    /* Buttons - Time period selector */
    .stButton > button {
        background-color: white;
        color: #475569;
        border: 2px solid #e2e8f0;
        border-radius: 8px;
        padding: 8px 20px;
        font-weight: 600;
        font-size: 13px;
        transition: all 0.2s ease;
        font-family: 'DM Sans', sans-serif;
    }
    .stButton > button:hover {
        border-color: #0284c7;
        color: #0284c7;
        background-color: #f0f9ff;
    }
    
    /* Cards */
    div[data-testid="stVerticalBlock"] > div {
        background-color: white;
        border-radius: 12px;
        padding: 0px;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #f1f5f9;
    }
    ::-webkit-scrollbar-thumb {
        background: #cbd5e1;
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #94a3b8;
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

# Color palette for NBFCs - Vibrant and distinct
NBFC_COLORS = {
    'Poonawalla Fincorp': '#0284c7',  # Blue
    'Bajaj Finance': '#dc2626',       # Red
    'L&T Finance': '#16a34a',         # Green
    'Shriram Finance': '#ea580c',     # Orange
    'Cholamandalam Finance': '#9333ea', # Purple
    'Aditya Birla Capital': '#0891b2', # Cyan
    'Piramal Finance': '#be123c',     # Rose
    'Muthoot Finance': '#65a30d',     # Lime
    'Mahindra Finance': '#7c3aed'     # Violet
}

# Session state initialization
if 'time_period' not in st.session_state:
    st.session_state.time_period = '1Y'
if 'index_to_100' not in st.session_state:
    st.session_state.index_to_100 = False
if 'selected_nbfcs' not in st.session_state:
    st.session_state.selected_nbfcs = list(NBFCS.keys())

@st.cache_data(ttl=3600)
def fetch_stock_data(symbol, period='1y'):
    """Fetch stock data using yfinance with error handling"""
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
                
                # Get market cap
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
                    'Market Cap': market_cap,
                    'Color': NBFC_COLORS[name]
                })
        except Exception as e:
            continue
            
    return pd.DataFrame(data)

def get_period_days(period):
    """Convert period string to days"""
    period_map = {
        '1D': 1,
        '1W': 7,
        '1M': 30,
        '3M': 90,
        '6M': 180,
        '1Y': 365
    }
    return period_map.get(period, 365)

def create_stock_price_chart(time_period, index_to_100=False, selected_nbfcs=None):
    """Create interactive multi-line stock price chart"""
    if selected_nbfcs is None:
        selected_nbfcs = list(NBFCS.keys())
    
    fig = go.Figure()
    
    # Determine yfinance period
    days = get_period_days(time_period)
    if days <= 7:
        yf_period = '5d'
        interval = '15m' if days == 1 else '1h'
    elif days <= 30:
        yf_period = '1mo'
        interval = '1d'
    elif days <= 90:
        yf_period = '3mo'
        interval = '1d'
    else:
        yf_period = '1y'
        interval = '1d'
    
    # Fetch data for each NBFC
    for name in selected_nbfcs:
        symbol = NBFCS[name]
        try:
            data = fetch_stock_data(symbol, period=yf_period)
            if data is not None and not data.empty:
                # Filter to exact period
                end_date = data.index[-1]
                start_date = end_date - timedelta(days=days)
                mask = (data.index >= start_date)
                filtered_data = data[mask]
                
                if not filtered_data.empty:
                    prices = filtered_data['Close']
                    
                    if index_to_100:
                        # Normalize to 100
                        prices = (prices / prices.iloc[0]) * 100
                        yaxis_title = 'Indexed Value (Base = 100)'
                        
                        # Calculate percentage change for label
                        pct_change = prices.iloc[-1] - 100
                        line_name = f"{name} ({pct_change:+.1f}%)"
                    else:
                        yaxis_title = 'Price (₹)'
                        line_name = name
                    
                    fig.add_trace(go.Scatter(
                        x=filtered_data.index,
                        y=prices,
                        name=line_name,
                        line=dict(color=NBFC_COLORS[name], width=2.5),
                        mode='lines',
                        hovertemplate=f'<b>{name}</b><br>' +
                                    'Date: %{x|%d %b %Y}<br>' +
                                    'Value: ₹%{y:,.2f}<br>' +
                                    '<extra></extra>'
                    ))
        except Exception as e:
            continue
    
    # Update layout
    fig.update_layout(
        title=dict(
            text=f'<b>Stock Price Performance - {time_period}</b>',
            font=dict(size=20, family='DM Sans', color='#0c4a6e')
        ),
        xaxis_title='Date',
        yaxis_title=yaxis_title,
        template='plotly_white',
        height=500,
        hovermode='x unified',
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.02,
            font=dict(size=11, family='DM Sans')
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='DM Sans', color='#334155'),
        margin=dict(l=60, r=180, t=60, b=60)
    )
    
    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='#f1f5f9',
        showline=True,
        linewidth=1,
        linecolor='#e2e8f0'
    )
    
    fig.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='#f1f5f9',
        showline=True,
        linewidth=1,
        linecolor='#e2e8f0'
    )
    
    return fig

def create_market_cap_chart(time_period, selected_nbfcs=None):
    """Create market cap trend chart"""
    if selected_nbfcs is None:
        selected_nbfcs = list(NBFCS.keys())
    
    fig = go.Figure()
    
    days = get_period_days(time_period)
    if days <= 7:
        yf_period = '5d'
    elif days <= 30:
        yf_period = '1mo'
    elif days <= 90:
        yf_period = '3mo'
    else:
        yf_period = '1y'
    
    for name in selected_nbfcs:
        symbol = NBFCS[name]
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=yf_period)
            
            if not hist.empty:
                # Filter to period
                end_date = hist.index[-1]
                start_date = end_date - timedelta(days=days)
                mask = (hist.index >= start_date)
                filtered_hist = hist[mask]
                
                if not filtered_hist.empty:
                    # Get shares outstanding
                    try:
                        info = ticker.info
                        shares = info.get('sharesOutstanding', 0)
                        if shares > 0:
                            market_cap = (filtered_hist['Close'] * shares) / 10000000  # In Crores
                            
                            fig.add_trace(go.Scatter(
                                x=filtered_hist.index,
                                y=market_cap,
                                name=name,
                                line=dict(color=NBFC_COLORS[name], width=2.5),
                                mode='lines',
                                hovertemplate=f'<b>{name}</b><br>' +
                                            'Date: %{x|%d %b %Y}<br>' +
                                            'Market Cap: ₹%{y:,.0f} Cr<br>' +
                                            '<extra></extra>'
                            ))
                    except:
                        continue
        except:
            continue
    
    fig.update_layout(
        title=dict(
            text=f'<b>Market Capitalization Trends - {time_period}</b>',
            font=dict(size=20, family='DM Sans', color='#0c4a6e')
        ),
        xaxis_title='Date',
        yaxis_title='Market Cap (₹ Crores)',
        template='plotly_white',
        height=500,
        hovermode='x unified',
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.02,
            font=dict(size=11, family='DM Sans')
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='DM Sans', color='#334155'),
        margin=dict(l=60, r=180, t=60, b=60)
    )
    
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#f1f5f9')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#f1f5f9')
    
    return fig

# Main App
st.title("📊 NBFC Dashboard")
st.caption(f"*Live market data • Last updated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}*")

# Create tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📈 Market Overview",
    "💼 Financial Performance", 
    "💰 Valuation Metrics",
    "📊 Historical Analysis",
    "🔍 Deep Dive",
    "🏆 Rankings"
])

# TAB 1: Market Overview
with tab1:
    # Fetch current prices
    with st.spinner("🔄 Fetching latest market data..."):
        price_df = get_current_prices()
    
    if price_df.empty:
        st.error("❌ Unable to fetch stock data. Please try again later.")
    else:
        # CURRENT PRICES TABLE (TOP)
        st.markdown("### 💹 Current Stock Prices")
        
        # Format the dataframe with colors
        styled_data = []
        for _, row in price_df.iterrows():
            change_color = '#16a34a' if row['Change %'] >= 0 else '#dc2626'
            arrow = '↑' if row['Change %'] >= 0 else '↓'
            
            styled_data.append({
                'Company': row['Company'],
                'Symbol': row['Symbol'],
                'Price (₹)': f"₹{row['Price']:,.2f}",
                'Change (₹)': f"{arrow} ₹{abs(row['Change']):,.2f}",
                'Change (%)': f"{arrow} {abs(row['Change %']):.2f}%",
                'Market Cap (Cr)': f"₹{row['Market Cap']:,.0f}" if row['Market Cap'] > 0 else 'N/A'
            })
        
        display_df = pd.DataFrame(styled_data)
        
        # Display table with custom CSS for colors
        st.dataframe(
            display_df,
            hide_index=True,
            use_container_width=True,
            height=400,
            column_config={
                "Company": st.column_config.TextColumn("Company", width="medium"),
                "Symbol": st.column_config.TextColumn("Symbol", width="small"),
                "Price (₹)": st.column_config.TextColumn("Price", width="small"),
                "Change (₹)": st.column_config.TextColumn("Change", width="small"),
                "Change (%)": st.column_config.TextColumn("Change %", width="small"),
                "Market Cap (Cr)": st.column_config.TextColumn("Market Cap", width="medium"),
            }
        )
        
        st.markdown("---")
        
        # TIME PERIOD SELECTOR
        st.markdown("### 📅 Select Time Period")
        col1, col2, col3, col4, col5, col6, col7 = st.columns([1, 1, 1, 1, 1, 1, 2])
        
        with col1:
            if st.button("1D", use_container_width=True):
                st.session_state.time_period = '1D'
        with col2:
            if st.button("1W", use_container_width=True):
                st.session_state.time_period = '1W'
        with col3:
            if st.button("1M", use_container_width=True):
                st.session_state.time_period = '1M'
        with col4:
            if st.button("3M", use_container_width=True):
                st.session_state.time_period = '3M'
        with col5:
            if st.button("6M", use_container_width=True):
                st.session_state.time_period = '6M'
        with col6:
            if st.button("1Y", use_container_width=True):
                st.session_state.time_period = '1Y'
        
        # Index to 100 toggle
        st.session_state.index_to_100 = st.checkbox(
            "📊 Show Relative Performance (Index to 100)",
            value=st.session_state.index_to_100,
            help="Normalize all stocks to start at 100 for easy comparison"
        )
        
        st.markdown("---")
        
        # STOCK PRICE CHART
        with st.spinner(f"📈 Loading {st.session_state.time_period} stock price data..."):
            price_chart = create_stock_price_chart(
                st.session_state.time_period,
                st.session_state.index_to_100,
                st.session_state.selected_nbfcs
            )
            st.plotly_chart(price_chart, use_container_width=True)
        
        st.markdown("---")
        
        # MARKET CAP CHART
        with st.spinner(f"💰 Loading {st.session_state.time_period} market cap data..."):
            mcap_chart = create_market_cap_chart(
                st.session_state.time_period,
                st.session_state.selected_nbfcs
            )
            st.plotly_chart(mcap_chart, use_container_width=True)

# TAB 2-6: Placeholders
with tab2:
    st.header("💼 Financial Performance")
    st.info("📊 Quarterly financial metrics will be displayed here")
    
with tab3:
    st.header("💰 Valuation Metrics")
    st.info("💹 Valuation ratios and metrics coming soon")
    
with tab4:
    st.header("📊 Historical Analysis")
    st.info("📈 Detailed historical analysis tools coming soon")
    
with tab5:
    st.header("🔍 Deep Dive")
    st.info("🔎 Individual NBFC analysis coming soon")
    
with tab6:
    st.header("🏆 Rankings & Benchmarking")
    st.info("📊 Comprehensive rankings coming soon")

# Sidebar
with st.sidebar:
    st.markdown("""
        <div style='background: linear-gradient(135deg, #0284c7 0%, #0c4a6e 100%); 
                    padding: 30px; 
                    border-radius: 12px; 
                    text-align: center; 
                    margin-bottom: 20px;'>
            <h2 style='color: white; margin: 0; font-size: 24px;'>📊</h2>
            <p style='color: #bae6fd; margin: 5px 0 0 0; font-size: 14px; font-weight: 600;'>NBFC Dashboard</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Dashboard Info")
    st.markdown(f"""
    - **NBFCs Tracked:** 9
    - **Benchmark:** Bank Nifty
    - **Data Source:** Yahoo Finance
    - **Update Frequency:** Hourly
    - **Selected Period:** {st.session_state.time_period}
    """)
    
    st.markdown("---")
    
    st.markdown("### 📊 Data Status")
    st.success("✅ Stock Data: Live")
    st.info("⏳ Financial Data: Quarterly")
    
    st.markdown("---")
    
    st.markdown("### 🏢 NBFCs")
    for i, name in enumerate(NBFCS.keys(), 1):
        color = NBFC_COLORS[name]
        st.markdown(f"<span style='color: {color}; font-weight: 600;'>●</span> {name}", unsafe_allow_html=True)
    
    st.markdown("---")
    st.caption("*Built for Poonawalla Fincorp*")
    st.caption(f"*v2.0 Professional | {datetime.now().year}*")
