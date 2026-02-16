import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import yfinance as yf

# Page config with LIGHT theme
st.set_page_config(
    page_title="NBFC Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Minimal CSS - only what's necessary
st.markdown("""
    <style>
    /* Force light theme */
    [data-testid="stAppViewContainer"] {
        background-color: #ffffff;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #0c4a6e !important;
    }
    
    /* Remove Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
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

# Colors
COLORS = ['#0284c7', '#dc2626', '#16a34a', '#ea580c', '#9333ea', 
          '#0891b2', '#be123c', '#65a30d', '#7c3aed']

# Session state
if 'time_period' not in st.session_state:
    st.session_state.time_period = '1Y'
if 'index_to_100' not in st.session_state:
    st.session_state.index_to_100 = False

@st.cache_data(ttl=3600)
def fetch_stock_data(symbol, period='1y'):
    """Fetch stock data"""
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period=period)
        return data
    except:
        return None

@st.cache_data(ttl=3600)
def get_current_prices():
    """Get current prices"""
    data = []
    for name, symbol in NBFCS.items():
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period='5d')
            if len(hist) > 0:
                current = hist['Close'].iloc[-1]
                prev = hist['Close'].iloc[-2] if len(hist) > 1 else current
                change_pct = ((current - prev) / prev) * 100
                
                # Get market cap
                try:
                    info = ticker.info
                    mcap = info.get('marketCap', 0) / 10000000
                except:
                    mcap = 0
                
                data.append({
                    'Company': name,
                    'Symbol': symbol.replace('.NS', ''),
                    'Price (₹)': f"₹{current:,.2f}",
                    'Change (%)': f"{'↑' if change_pct >= 0 else '↓'} {abs(change_pct):.2f}%",
                    'Market Cap (Cr)': f"₹{mcap:,.0f}" if mcap > 0 else 'N/A'
                })
        except:
            continue
    return pd.DataFrame(data)

def get_period_days(period):
    """Convert period to days"""
    return {'1D': 1, '1W': 7, '1M': 30, '3M': 90, '6M': 180, '1Y': 365}.get(period, 365)

def create_chart(time_period, chart_type='price', index_to_100=False):
    """Create price or market cap chart"""
    fig = go.Figure()
    
    days = get_period_days(time_period)
    yf_period = '5d' if days <= 7 else '1mo' if days <= 30 else '3mo' if days <= 90 else '1y'
    
    for idx, (name, symbol) in enumerate(NBFCS.items()):
        try:
            data = fetch_stock_data(symbol, period=yf_period)
            if data is None or data.empty:
                continue
                
            # Filter to period
            end_date = data.index[-1]
            start_date = end_date - timedelta(days=days)
            filtered = data[(data.index >= start_date)]
            
            if filtered.empty:
                continue
            
            if chart_type == 'price':
                values = filtered['Close']
                if index_to_100:
                    values = (values / values.iloc[0]) * 100
                    pct = values.iloc[-1] - 100
                    label = f"{name} ({pct:+.1f}%)"
                    yaxis_title = 'Index (Base=100)'
                else:
                    label = name
                    yaxis_title = 'Price (₹)'
            else:  # market cap
                # Simplified market cap - just use price as proxy
                values = filtered['Close'] / 10  # Simplified
                label = name
                yaxis_title = 'Relative Market Cap'
            
            fig.add_trace(go.Scatter(
                x=filtered.index,
                y=values,
                name=label,
                line=dict(color=COLORS[idx % len(COLORS)], width=2.5),
                mode='lines'
            ))
        except:
            continue
    
    # Mobile-optimized layout
    fig.update_layout(
        title=f'{"Stock Prices" if chart_type == "price" else "Market Cap"} - {time_period}',
        xaxis_title='Date',
        yaxis_title=yaxis_title,
        template='plotly_white',
        height=400,  # Shorter for mobile
        hovermode='x unified',
        showlegend=True,
        legend=dict(
            orientation="h",  # Horizontal legend for mobile
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            font=dict(size=9)
        ),
        margin=dict(l=40, r=20, t=60, b=40),
        font=dict(size=11)
    )
    
    # Simplified axes for mobile
    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='#f1f5f9',
        tickangle=0  # Horizontal tick labels
    )
    fig.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='#f1f5f9'
    )
    
    return fig

# Main App
st.title("📊 NBFC Dashboard")
st.caption(f"*Updated: {datetime.now().strftime('%d %b %Y, %I:%M %p')}*")

# Tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📈 Market",
    "💼 Financial",
    "💰 Valuation",
    "📊 History",
    "🔍 Deep Dive",
    "🏆 Rankings"
])

with tab1:
    # Current Prices
    st.subheader("💹 Current Prices")
    
    with st.spinner("Loading..."):
        df = get_current_prices()
    
    if df.empty:
        st.error("Unable to fetch data")
    else:
        st.dataframe(df, hide_index=True, use_container_width=True, height=350)
        
        st.markdown("---")
        
        # Time Period Buttons
        st.subheader("📅 Time Period")
        cols = st.columns(6)
        periods = ['1D', '1W', '1M', '3M', '6M', '1Y']
        
        for i, period in enumerate(periods):
            with cols[i]:
                if st.button(period, key=f"btn_{period}", use_container_width=True):
                    st.session_state.time_period = period
                    st.rerun()
        
        st.caption(f"*Selected: {st.session_state.time_period}*")
        
        # Index to 100
        st.session_state.index_to_100 = st.checkbox(
            "📊 Show Relative Performance (Index to 100)",
            value=st.session_state.index_to_100
        )
        
        st.markdown("---")
        
        # Stock Price Chart
        st.subheader("📈 Stock Prices")
        with st.spinner("Loading chart..."):
            try:
                chart = create_chart(
                    st.session_state.time_period,
                    'price',
                    st.session_state.index_to_100
                )
                st.plotly_chart(chart, use_container_width=True, config={'displayModeBar': False})
            except Exception as e:
                st.error(f"Chart error: {str(e)}")
        
        st.markdown("---")
        
        # Market Cap Chart
        st.subheader("💰 Market Capitalization")
        with st.spinner("Loading chart..."):
            try:
                mcap_chart = create_chart(st.session_state.time_period, 'mcap')
                st.plotly_chart(mcap_chart, use_container_width=True, config={'displayModeBar': False})
            except Exception as e:
                st.error(f"Chart error: {str(e)}")

# Other tabs
with tab2:
    st.info("Financial Performance - Coming Soon")
with tab3:
    st.info("Valuation Metrics - Coming Soon")
with tab4:
    st.info("Historical Analysis - Coming Soon")
with tab5:
    st.info("Deep Dive - Coming Soon")
with tab6:
    st.info("Rankings - Coming Soon")

# Sidebar
with st.sidebar:
    st.markdown("### 📊 Info")
    st.markdown(f"""
    - **NBFCs:** 9
    - **Period:** {st.session_state.time_period}
    - **Source:** Yahoo Finance
    """)
    st.markdown("---")
    st.caption("*Built for Poonawalla Fincorp*")
