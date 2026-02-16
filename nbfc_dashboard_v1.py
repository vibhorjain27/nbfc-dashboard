import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import pytz
import yfinance as yf

# Page config
st.set_page_config(
    page_title="NBFC Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Professional Financial Theme - Bloomberg inspired
st.markdown("""
    <style>
    /* Professional background - subtle blue-grey */
    .main {
        background: linear-gradient(135deg, #f8f9fb 0%, #e8edf3 100%);
    }
    
    .block-container {
        padding: 2rem 3rem;
        max-width: 1400px;
    }
    
    /* Headers - dark blue, professional */
    h1 {
        color: #0a2540;
        font-weight: 700;
        font-size: 2rem;
        margin-bottom: 0.5rem;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }
    
    h2, h3 {
        color: #1a3a52;
        font-weight: 600;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }
    
    /* Remove Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Stock cards */
    .stock-card {
        background: white;
        border-radius: 8px;
        padding: 16px 20px;
        margin-bottom: 12px;
        border-left: 4px solid #0284c7;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    }
    
    .stock-name {
        font-size: 16px;
        font-weight: 600;
        color: #0a2540;
        margin-bottom: 8px;
    }
    
    .stock-price-row {
        display: flex;
        align-items: baseline;
        gap: 8px;
        margin-bottom: 8px;
    }
    
    .stock-price {
        font-size: 24px;
        font-weight: 700;
        color: #1a3a52;
        font-family: 'Monaco', 'Courier New', monospace;
    }
    
    .stock-change-positive {
        color: #16a34a;
        font-weight: 600;
        font-size: 15px;
    }
    
    .stock-change-negative {
        color: #dc2626;
        font-weight: 600;
        font-size: 15px;
    }
    
    .stock-volume {
        font-size: 13px;
        color: #64748b;
        font-weight: 500;
    }
    
    /* Buttons - small, clean style for time periods */
    .stButton button {
        background: white;
        color: #475569;
        border: 1.5px solid #cbd5e1;
        border-radius: 6px;
        padding: 6px 16px;
        font-weight: 600;
        font-size: 13px;
        transition: all 0.2s;
        min-height: 32px;
    }
    
    .stButton button:hover {
        border-color: #0284c7;
        color: #0284c7;
    }
    
    .stButton button:active {
        background: #0284c7;
        color: white;
        border-color: #0284c7;
    }
    
    /* Checkbox styling */
    .stCheckbox {
        font-size: 14px;
    }
    
    /* Caption text */
    .caption-text {
        color: #64748b;
        font-size: 14px;
        margin-top: 4px;
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

# Default comparison stocks
DEFAULT_COMPARISON = ['Poonawalla Fincorp', 'Bajaj Finance', 'L&T Finance', 'Shriram Finance']

# Colors - professional palette
COLORS = {
    'Poonawalla Fincorp': '#0284c7',  # Blue
    'Bajaj Finance': '#dc2626',        # Red
    'L&T Finance': '#16a34a',          # Green
    'Shriram Finance': '#ea580c',      # Orange
    'Cholamandalam Finance': '#9333ea', # Purple
    'Aditya Birla Capital': '#0891b2',  # Cyan
    'Piramal Finance': '#be123c',       # Rose
    'Muthoot Finance': '#65a30d',       # Lime
    'Mahindra Finance': '#7c3aed'       # Violet
}

# Session state
if 'time_period' not in st.session_state:
    st.session_state.time_period = '6M'
if 'comparison_stocks' not in st.session_state:
    st.session_state.comparison_stocks = DEFAULT_COMPARISON.copy()

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
    """Get current prices for stock cards"""
    data = []
    for name, symbol in NBFCS.items():
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period='5d')
            if len(hist) > 0:
                current = hist['Close'].iloc[-1]
                prev = hist['Close'].iloc[-2] if len(hist) > 1 else current
                change = current - prev
                change_pct = (change / prev) * 100
                
                # Get volume (today's volume)
                volume = hist['Volume'].iloc[-1]
                
                # Get sparkline data (last 30 days)
                spark_data = ticker.history(period='1mo')['Close'].tolist()
                
                data.append({
                    'name': name,
                    'price': current,
                    'change': change,
                    'change_pct': change_pct,
                    'volume': volume,
                    'sparkline': spark_data
                })
        except:
            continue
    return data

def get_period_days(period):
    """Convert period to days"""
    return {'1D': 1, '1W': 7, '1M': 30, '3M': 90, '6M': 180, '1Y': 365}.get(period, 180)

def create_comparison_chart(time_period, selected_stocks):
    """Create indexed comparison chart with end labels"""
    fig = go.Figure()
    
    days = get_period_days(time_period)
    yf_period = '5d' if days <= 7 else '1mo' if days <= 30 else '3mo' if days <= 90 else '1y'
    
    # Store performance data for sorting
    performance_data = []
    
    for name in selected_stocks:
        symbol = NBFCS[name]
        try:
            data = fetch_stock_data(symbol, period=yf_period)
            if data is None or data.empty:
                continue
            
            # Filter to period
            end_date = data.index[-1]
            start_date = end_date - timedelta(days=days)
            filtered = data[(data.index >= start_date)]
            
            if filtered.empty or len(filtered) < 2:
                continue
            
            # Index to 100
            prices = filtered['Close']
            indexed = (prices / prices.iloc[0]) * 100
            
            # Calculate performance
            performance = indexed.iloc[-1] - 100
            
            # Store for sorting
            performance_data.append({
                'name': name,
                'performance': performance,
                'dates': filtered.index,
                'values': indexed,
                'color': COLORS[name]
            })
        except:
            continue
    
    # Sort by performance (best to worst)
    performance_data.sort(key=lambda x: x['performance'], reverse=True)
    
    # Add traces in performance order
    for item in performance_data:
        # Create label with performance
        label = f"{item['name']} ({item['performance']:+.1f}%)"
        
        fig.add_trace(go.Scatter(
            x=item['dates'],
            y=item['values'],
            name=label,
            line=dict(color=item['color'], width=3),
            mode='lines',
            hovertemplate=f"<b>{item['name']}</b><br>Date: %{{x|%d %b %Y}}<br>Index: %{{y:.2f}}<extra></extra>"
        ))
        
        # Add end label
        fig.add_annotation(
            x=item['dates'][-1],
            y=item['values'].iloc[-1],
            text=f"{item['name']}<br>{item['performance']:+.1f}%",
            showarrow=False,
            xanchor='left',
            xshift=10,
            font=dict(size=11, color=item['color'], weight='bold'),
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor=item['color'],
            borderwidth=1,
            borderpad=4
        )
    
    # Layout
    fig.update_layout(
        title=dict(
            text=f'<b>Stock Performance Comparison - {time_period}</b>',
            font=dict(size=20, color='#0a2540'),
            x=0
        ),
        xaxis_title='Date',
        yaxis_title='Indexed Value (Base = 100)',
        template='plotly_white',
        height=500,
        hovermode='x unified',
        showlegend=False,  # We have end labels instead
        plot_bgcolor='white',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=60, r=150, t=60, b=60),
        font=dict(family='Arial, sans-serif', color='#1a3a52')
    )
    
    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='#f1f5f9',
        showline=True,
        linewidth=1,
        linecolor='#cbd5e1'
    )
    
    fig.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='#f1f5f9',
        showline=True,
        linewidth=1,
        linecolor='#cbd5e1'
    )
    
    return fig

# Main App
ist = pytz.timezone('Asia/Kolkata')
current_time = datetime.now(ist)

st.title("NBFC Dashboard")
st.caption(f"Last updated: {current_time.strftime('%d %B %Y, %I:%M %p IST')}")
st.markdown("---")

# Stock List (Cards) - 3x3 Grid
st.subheader("Current Stock Prices")

with st.spinner("Loading stock data..."):
    stocks = get_current_prices()

if not stocks:
    st.error("Unable to fetch stock data")
else:
    # Display in 3x3 grid
    for row_idx in range(3):
        cols = st.columns(3)
        for col_idx in range(3):
            stock_idx = row_idx * 3 + col_idx
            if stock_idx < len(stocks):
                stock = stocks[stock_idx]
                arrow = "↑" if stock['change_pct'] >= 0 else "↓"
                change_class = "stock-change-positive" if stock['change_pct'] >= 0 else "stock-change-negative"
                sign = "+" if stock['change'] >= 0 else ""
                
                # Format volume (convert to M/K)
                vol = stock['volume']
                if vol >= 1_000_000:
                    vol_str = f"{vol/1_000_000:.2f}M"
                elif vol >= 1_000:
                    vol_str = f"{vol/1_000:.2f}K"
                else:
                    vol_str = f"{vol:.0f}"
                
                with cols[col_idx]:
                    st.markdown(f"""
                        <div class="stock-card">
                            <div class="stock-name">{stock['name']}</div>
                            <div class="stock-price-row">
                                <span class="stock-price">₹{stock['price']:,.2f}</span>
                                <span class="{change_class}">{arrow} ({sign}₹{abs(stock['change']):.2f}) ({sign}{abs(stock['change_pct']):.2f}%)</span>
                            </div>
                            <div class="stock-volume">Volume: {vol_str}</div>
                        </div>
                    """, unsafe_allow_html=True)

st.markdown("---")

# Performance Comparison Section
st.subheader("Performance Comparison")

# Stock selection for comparison
st.markdown("#### Select stocks to compare")
col1, col2, col3 = st.columns(3)

# Poonawalla always shown (no checkbox)
with col1:
    st.markdown("**Poonawalla Fincorp** (always shown)")

# Other stocks - checkboxes
other_stocks = [name for name in NBFCS.keys() if name not in ['Poonawalla Fincorp']]
selected_others = []

for i, name in enumerate(other_stocks):
    col_idx = i % 3
    with [col1, col2, col3][col_idx]:
        is_default = name in DEFAULT_COMPARISON
        if st.checkbox(name, value=is_default, key=f"check_{name}"):
            selected_others.append(name)

# Final comparison list
comparison_stocks = ['Poonawalla Fincorp'] + selected_others

st.markdown("<br>", unsafe_allow_html=True)

# Time Period Selector - Small buttons close to chart
st.caption("Indexed to 100 (default)")

# Create inline style for small period buttons
period_buttons_html = f"""
<div style="margin-bottom: 20px;">
    <style>
        .period-btn {{
            display: inline-block;
            padding: 6px 16px;
            margin: 0 4px;
            background: white;
            border: 1.5px solid #cbd5e1;
            border-radius: 6px;
            cursor: pointer;
            font-size: 13px;
            font-weight: 600;
            color: #475569;
            transition: all 0.2s;
        }}
        .period-btn:hover {{
            border-color: #0284c7;
            color: #0284c7;
        }}
        .period-btn-active {{
            background: #0284c7;
            color: white;
            border-color: #0284c7;
        }}
    </style>
</div>
"""
st.markdown(period_buttons_html, unsafe_allow_html=True)

# Use Streamlit buttons in compact layout
period_cols = st.columns([1, 1, 1, 1, 1, 1, 10])
periods = ['1D', '1W', '1M', '3M', '6M', '1Y']

for i, period in enumerate(periods):
    with period_cols[i]:
        if st.button(period, key=f"btn_{period}", use_container_width=True):
            st.session_state.time_period = period
            st.rerun()

# Comparison Chart
with st.spinner("Loading comparison chart..."):
    try:
        chart = create_comparison_chart(st.session_state.time_period, comparison_stocks)
        st.plotly_chart(chart, use_container_width=True, config={'displayModeBar': False})
    except Exception as e:
        st.error(f"Unable to load chart: {str(e)}")
