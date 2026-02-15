import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import yfinance as yf
import time

# Page configuration
st.set_page_config(
    page_title="NBFC Dashboard - Poonawalla",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Error tracking
if 'errors' not in st.session_state:
    st.session_state.errors = []

# Enhanced Poonawalla bluish theme
st.markdown("""
    <style>
    /* Main background */
    .main {
        background-color: #f8fafc;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #e0f2fe;
        padding: 10px;
        border-radius: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border-radius: 6px;
        color: #0369a1;
        font-weight: 600;
        padding: 10px 20px;
        transition: all 0.3s ease;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #bae6fd;
    }
    .stTabs [aria-selected="true"] {
        background-color: #0284c7;
        color: white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Headers */
    h1 {
        color: #0c4a6e;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    h2, h3 {
        color: #0c4a6e;
        font-weight: 600;
    }
    
    /* Metric cards */
    [data-testid="stMetricValue"] {
        font-size: 1.8rem;
        font-weight: 700;
        color: #0c4a6e;
    }
    
    /* Data tables */
    .dataframe {
        border: none !important;
    }
    
    /* Loading spinner */
    .stSpinner > div {
        border-color: #0284c7 !important;
    }
    
    /* Info boxes */
    .element-container div[data-testid="stMarkdownContainer"] p {
        color: #334155;
    }
    
    /* Success/Error messages */
    .stSuccess {
        background-color: #dcfce7;
        border-left: 4px solid #16a34a;
    }
    .stError {
        background-color: #fee2e2;
        border-left: 4px solid #dc2626;
    }
    .stWarning {
        background-color: #fef3c7;
        border-left: 4px solid #f59e0b;
    }
    .stInfo {
        background-color: #dbeafe;
        border-left: 4px solid #0284c7;
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

@st.cache_data(ttl=3600)
def fetch_stock_data(symbol, period='1y'):
    """Fetch stock data using yfinance"""
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period=period)
        return data
    except Exception as e:
        st.error(f"Error fetching data for {symbol}: {str(e)}")
        return None

@st.cache_data(ttl=3600)
def get_current_prices():
    """Get current price data for all NBFCs with robust error handling"""
    data = []
    failed_nbfcs = []
    
    for name, symbol in NBFCS.items():
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period='5d')
            
            if len(hist) > 0:
                current_price = hist['Close'].iloc[-1]
                prev_close = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
                change = current_price - prev_close
                change_pct = (change / prev_close) * 100
                
                # Try to get market cap from info, with fallback
                try:
                    info = ticker.info
                    market_cap = info.get('marketCap', 0) / 10000000  # Convert to Crores
                except:
                    # Fallback calculation: shares outstanding * current price
                    market_cap = 0  # Will show as 0 if can't fetch
                
                data.append({
                    'NBFC': name,
                    'Symbol': symbol,
                    'Current Price': current_price,
                    'Change': change,
                    'Change %': change_pct,
                    'Market Cap (Cr)': market_cap,
                    'Volume': hist['Volume'].iloc[-1],
                    'Status': 'success'
                })
            else:
                failed_nbfcs.append(name)
                st.session_state.errors.append(f"No recent data available for {name}")
                
        except Exception as e:
            failed_nbfcs.append(name)
            st.session_state.errors.append(f"Failed to fetch data for {name}: {str(e)}")
    
    # Store failed NBFCs for display
    if failed_nbfcs:
        st.session_state.failed_nbfcs = failed_nbfcs
    
    return pd.DataFrame(data) if data else pd.DataFrame()

def format_currency(value):
    """Format currency in Indian style"""
    if value >= 100000:
        return f"₹{value/100000:.2f}L Cr"
    elif value >= 1000:
        return f"₹{value/1000:.2f}K Cr"
    else:
        return f"₹{value:.2f} Cr"

def create_price_comparison_chart(df):
    """Create bar chart for current prices"""
    fig = go.Figure()
    
    colors = ['#0284c7' if x >= 0 else '#ef4444' for x in df['Change %']]
    
    fig.add_trace(go.Bar(
        x=df['NBFC'],
        y=df['Current Price'],
        marker_color=colors,
        text=df['Current Price'].apply(lambda x: f'₹{x:.2f}'),
        textposition='outside',
    ))
    
    fig.update_layout(
        title='Current Stock Prices',
        xaxis_title='NBFC',
        yaxis_title='Price (₹)',
        template='plotly_white',
        height=400,
        showlegend=False,
        font=dict(color='#0c4a6e')
    )
    
    return fig

def create_market_cap_chart(df):
    """Create market cap comparison"""
    fig = px.bar(
        df.sort_values('Market Cap (Cr)', ascending=False),
        x='NBFC',
        y='Market Cap (Cr)',
        text='Market Cap (Cr)',
        color='Market Cap (Cr)',
        color_continuous_scale=['#bae6fd', '#0284c7', '#0c4a6e']
    )
    
    fig.update_traces(texttemplate='₹%{text:.2f}L Cr', textposition='outside')
    fig.update_layout(
        title='Market Capitalization Comparison',
        xaxis_title='NBFC',
        yaxis_title='Market Cap (₹ Lakh Crores)',
        template='plotly_white',
        height=400,
        showlegend=False,
        font=dict(color='#0c4a6e')
    )
    
    return fig

# Main App
st.title("📊 NBFC Dashboard")
st.markdown(f"*Last Updated: {datetime.now().strftime('%B %d, %Y %I:%M %p')}*")

# Create tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📈 Market Overview",
    "💼 Financial Performance", 
    "💰 Valuation Metrics",
    "📊 Historical Trends",
    "🔍 Deep Dive",
    "🏆 Rankings"
])

# TAB 1: Market Overview
with tab1:
    st.header("📈 Market Overview")
    st.caption(f"Live stock data for all 9 NBFCs")
    
    # Fetch data with loading indicator
    with st.spinner("🔄 Fetching latest stock data from market..."):
        price_df = get_current_prices()
    
    # Check if we have data
    if price_df.empty:
        st.error("❌ Unable to fetch stock data. Please check your internet connection or try again later.")
        st.info("💡 **Troubleshooting:** This usually happens when Yahoo Finance API is temporarily unavailable. The data will refresh automatically in a few minutes.")
        
        # Show which NBFCs failed
        if hasattr(st.session_state, 'failed_nbfcs'):
            st.warning(f"Failed to fetch data for: {', '.join(st.session_state.failed_nbfcs)}")
    else:
        # Show warnings if some NBFCs failed
        if hasattr(st.session_state, 'failed_nbfcs') and st.session_state.failed_nbfcs:
            st.warning(f"⚠️ Partial data: Could not fetch data for {len(st.session_state.failed_nbfcs)} NBFC(s): {', '.join(st.session_state.failed_nbfcs)}")
        
        # Summary metrics in columns
        st.subheader("Key Market Indicators")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            avg_change = price_df['Change %'].mean()
            st.metric(
                "Average Change", 
                f"{avg_change:.2f}%",
                delta=f"{avg_change:.2f}%",
                help="Average percentage change across all NBFCs today"
            )
        
        with col2:
            gainers = len(price_df[price_df['Change %'] > 0])
            st.metric(
                "Gainers", 
                gainers,
                delta=f"{gainers} of {len(price_df)}",
                help="Number of NBFCs trading in positive territory"
            )
        
        with col3:
            losers = len(price_df[price_df['Change %'] < 0])
            st.metric(
                "Losers", 
                losers,
                delta=f"-{losers} of {len(price_df)}", 
                delta_color="inverse",
                help="Number of NBFCs trading in negative territory"
            )
        
        with col4:
            total_mcap = price_df['Market Cap (Cr)'].sum()
            st.metric(
                "Total Market Cap", 
                format_currency(total_mcap),
                help="Combined market capitalization of all 9 NBFCs"
            )
        
        st.markdown("---")
        
        # Price comparison charts
        st.subheader("Price Performance")
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(create_price_comparison_chart(price_df), use_container_width=True)
        
        with col2:
            st.plotly_chart(create_market_cap_chart(price_df), use_container_width=True)
        
        st.markdown("---")
        
        # Detailed table
        st.subheader("Detailed Stock Data")
        st.caption("Click on column headers to sort")
        
        # Format the dataframe for display
        display_df = price_df.copy()
        display_df['Current Price'] = display_df['Current Price'].apply(lambda x: f"₹{x:.2f}")
        display_df['Change'] = display_df.apply(
            lambda row: f"₹{row['Change']:.2f}" if row['Change'] >= 0 else f"-₹{abs(row['Change']):.2f}",
            axis=1
        )
        display_df['Change %'] = display_df['Change %'].apply(
            lambda x: f"+{x:.2f}%" if x >= 0 else f"{x:.2f}%"
        )
        display_df['Market Cap (Cr)'] = display_df['Market Cap (Cr)'].apply(
            lambda x: f"₹{x:,.0f} Cr" if x > 0 else "N/A"
        )
        display_df['Volume'] = display_df['Volume'].apply(lambda x: f"{x:,.0f}")
        
        # Remove status column before display
        if 'Status' in display_df.columns:
            display_df = display_df.drop('Status', axis=1)
        
        st.dataframe(
            display_df,
            hide_index=True,
            use_container_width=True,
            column_config={
                "NBFC": st.column_config.TextColumn("NBFC", width="medium", help="NBFC Name"),
                "Symbol": st.column_config.TextColumn("Symbol", width="small", help="Stock Symbol"),
                "Current Price": st.column_config.TextColumn("Price", width="small", help="Latest traded price"),
                "Change": st.column_config.TextColumn("Change (₹)", width="small", help="Absolute price change"),
                "Change %": st.column_config.TextColumn("Change %", width="small", help="Percentage change"),
                "Market Cap (Cr)": st.column_config.TextColumn("Market Cap", width="medium", help="Market Capitalization in Crores"),
                "Volume": st.column_config.TextColumn("Volume", width="medium", help="Trading volume"),
            }
        )
        
        # Data freshness indicator
        st.caption(f"💡 Data refreshes every hour. Last updated: {datetime.now().strftime('%I:%M %p')}")

# TAB 2: Financial Performance (Placeholder)
with tab2:
    st.header("Financial Performance")
    st.info("📊 Financial metrics will be updated as quarterly results are announced")
    
    st.markdown("""
    ### Key Metrics Tracked:
    - **AUM** (Assets Under Management)
    - **ROA** (Return on Assets)
    - **PAT** (Profit After Tax)
    - **GNPA** (Gross Non-Performing Assets %)
    - **NNPA** (Net Non-Performing Assets %)
    - **NIM** (Net Interest Margin)
    
    *Data will be updated automatically when NBFCs announce their quarterly results*
    """)

# TAB 3: Valuation Metrics (Placeholder)
with tab3:
    st.header("Valuation Metrics")
    st.info("💰 Valuation ratios calculated from latest financials and current prices")
    
    st.markdown("""
    ### Metrics Available:
    - Price-to-Earnings (P/E) Ratio
    - Price-to-Book (P/B) Ratio
    - Price-to-AUM Ratio
    - Dividend Yield
    """)

# TAB 4: Historical Trends
with tab4:
    st.header("Historical Trends & Analysis")
    
    # Date picker
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input(
            "Start Date",
            value=datetime.now() - timedelta(days=365),
            max_value=datetime.now()
        )
    with col2:
        end_date = st.date_input(
            "End Date",
            value=datetime.now(),
            max_value=datetime.now()
        )
    
    # NBFC selector
    selected_nbfcs = st.multiselect(
        "Select NBFCs to compare",
        options=list(NBFCS.keys()),
        default=list(NBFCS.keys())
    )
    
    # Index to 100 toggle
    index_to_100 = st.checkbox("Index to 100 (Relative Performance)", value=True)
    show_bank_nifty = st.checkbox("Show Bank Nifty Benchmark", value=True)
    
    if selected_nbfcs:
        with st.spinner("Loading historical data..."):
            # Fetch data for selected NBFCs
            historical_data = {}
            for name in selected_nbfcs:
                symbol = NBFCS[name]
                data = fetch_stock_data(symbol, period='1y')
                if data is not None and not data.empty:
                    # Filter by date range
                    data = data.loc[start_date:end_date]
                    historical_data[name] = data
            
            # Fetch Bank Nifty if selected
            if show_bank_nifty:
                bn_data = fetch_stock_data(BANK_NIFTY, period='1y')
                if bn_data is not None:
                    bn_data = bn_data.loc[start_date:end_date]
                    historical_data['Bank Nifty'] = bn_data
            
            if historical_data:
                # Create the chart
                fig = go.Figure()
                
                for name, data in historical_data.items():
                    if index_to_100:
                        # Normalize to 100
                        indexed = (data['Close'] / data['Close'].iloc[0]) * 100
                        final_value = indexed.iloc[-1]
                        pct_change = final_value - 100
                        
                        # Add trace with percentage label at end
                        fig.add_trace(go.Scatter(
                            x=data.index,
                            y=indexed,
                            mode='lines',
                            name=f"{name} ({pct_change:+.1f}%)",
                            line=dict(width=2.5 if name != 'Bank Nifty' else 2),
                            opacity=0.5 if name == 'Bank Nifty' else 1
                        ))
                    else:
                        fig.add_trace(go.Scatter(
                            x=data.index,
                            y=data['Close'],
                            mode='lines',
                            name=name,
                            line=dict(width=2.5 if name != 'Bank Nifty' else 2),
                            opacity=0.5 if name == 'Bank Nifty' else 1
                        ))
                
                fig.update_layout(
                    title='Stock Price Performance',
                    xaxis_title='Date',
                    yaxis_title='Indexed Value (Base = 100)' if index_to_100 else 'Price (₹)',
                    template='plotly_white',
                    height=600,
                    hovermode='x unified',
                    legend=dict(
                        orientation="v",
                        yanchor="top",
                        y=1,
                        xanchor="left",
                        x=1.02
                    ),
                    font=dict(color='#0c4a6e')
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Summary statistics
                st.subheader("Period Performance Summary")
                summary_data = []
                for name, data in historical_data.items():
                    if name != 'Bank Nifty':
                        start_price = data['Close'].iloc[0]
                        end_price = data['Close'].iloc[-1]
                        change_pct = ((end_price - start_price) / start_price) * 100
                        
                        summary_data.append({
                            'NBFC': name,
                            'Start Price': f"₹{start_price:.2f}",
                            'End Price': f"₹{end_price:.2f}",
                            'Change': f"{change_pct:+.2f}%"
                        })
                
                st.dataframe(
                    pd.DataFrame(summary_data).sort_values('Change', ascending=False, key=lambda x: x.str.rstrip('%').astype(float)),
                    hide_index=True,
                    use_container_width=True
                )

# TAB 5: Deep Dive (Placeholder)
with tab5:
    st.header("Individual NBFC Deep Dive")
    
    selected_nbfc = st.selectbox("Select NBFC", list(NBFCS.keys()))
    
    st.info(f"Detailed analysis for {selected_nbfc} will be displayed here")

# TAB 6: Rankings (Placeholder)
with tab6:
    st.header("Rankings & Benchmarking")
    st.info("🏆 Comprehensive rankings across all metrics coming soon")

# Sidebar
with st.sidebar:
    # Logo placeholder (using colored box since we can't embed actual logo)
    st.markdown("""
        <div style='background: linear-gradient(135deg, #0284c7 0%, #0c4a6e 100%); 
                    padding: 30px; 
                    border-radius: 10px; 
                    text-align: center; 
                    margin-bottom: 20px;'>
            <h2 style='color: white; margin: 0; font-size: 24px;'>📊</h2>
            <p style='color: #bae6fd; margin: 5px 0 0 0; font-size: 14px;'>NBFC Dashboard</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Dashboard Info")
    st.markdown(f"""
    - **NBFCs Tracked:** 9
    - **Benchmark:** Bank Nifty
    - **Data Source:** Yahoo Finance
    - **Update Frequency:** Hourly
    - **Last Refresh:** {datetime.now().strftime('%I:%M %p')}
    """)
    
    st.markdown("---")
    
    st.markdown("### 📊 Data Freshness")
    
    # Stock data status
    st.markdown("**Stock Prices:**")
    if hasattr(st.session_state, 'failed_nbfcs') and st.session_state.failed_nbfcs:
        st.warning(f"⚠️ Partial ({9 - len(st.session_state.failed_nbfcs)}/9 NBFCs)")
    else:
        st.success("✅ Live Data")
    
    # Financial data status
    st.markdown("**Financial Metrics:**")
    st.info("⏳ Updates on result announcements")
    
    st.markdown("---")
    
    st.markdown("### 🏢 Tracked NBFCs")
    for i, (name, symbol) in enumerate(NBFCS.items(), 1):
        st.caption(f"{i}. {name}")
    
    st.markdown("---")
    
    st.markdown("### 📞 Support")
    st.caption("For questions or issues:")
    st.caption("📧 vibhorjain27@gmail.com")
    
    st.markdown("---")
    st.caption("*Built for Poonawalla Fincorp*")
    st.caption(f"*v1.0 | {datetime.now().year}*")
