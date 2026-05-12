import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="Shaukat AI Pro Bot", layout="wide")

# Sidebar for Market Info
st.sidebar.header("📊 Shaukat Trading Control")
symbol = st.sidebar.selectbox("Select Asset", ["^NSEI", "^NSEBANK", "RELIANCE.NS", "HDFCBANK.NS"])
timeframe = st.sidebar.selectbox("Timeframe", ["5m", "15m", "1h", "1d"])

st.title("🛡️ Shaukat AI: Professional Trading Terminal")

# Tabs for different Analysis
tab1, tab2 = st.tabs(["📈 Live Chart & Signals", "🏦 FII / DII Activity"])

with tab1:
    try:
        data = yf.download(symbol, period="5d", interval=timeframe)
        if not data.empty:
            # Technical Analysis Indicators
            data['EMA_20'] = ta.ema(data['Close'], length=20)
            data['EMA_200'] = ta.ema(data['Close'], length=200)
            data['RSI'] = ta.rsi(data['Close'], length=14)
            
            # Metric Row
            l_price = data['Close'].iloc[-1]
            change = l_price - data['Open'].iloc[-1]
            st.metric(f"{symbol} Price", f"₹{round(l_price, 2)}", f"{round(change, 2)}")

            # Candlestick Chart
            fig = go.Figure(data=[go.Candlestick(x=data.index, open=data['Open'], 
                            high=data['High'], low=data['Low'], close=data['Close'], name="Price")])
            
            # Adding EMA Lines
            fig.add_trace(go.Scatter(x=data.index, y=data['EMA_20'], name="EMA 20", line=dict(color='orange')))
            fig.add_trace(go.Scatter(x=data.index, y=data['EMA_200'], name="EMA 200", line=dict(color='blue')))
            
            fig.update_layout(template="plotly_dark", height=600, xaxis_rangeslider_visible=False)
            st.plotly_chart(fig, use_container_width=True)
            
            # RSI Indicator
            st.subheader("🔭 RSI Analysis (Strength)")
            st.line_chart(data['RSI'])
            
    except Exception as e:
        st.error(f"Error: {e}")

with tab2:
    st.subheader("🏦 Smart Money Flow (Estimated)")
    st.info("FII/DII data is updated after market hours. Current view: Sentiment Tracker")
    # Placeholder for FII/DII - Professional apps use paid APIs, we show a manual daily tracker
    st.table(pd.DataFrame({
        "Category": ["FII Net", "DII Net"],
        "Action": ["Monitoring...", "Monitoring..."],
        "Sentiment": ["Bullish", "Neutral"]
    }))

st.sidebar.write(f"Last Sync: {datetime.now().strftime('%H:%M:%S')}")
