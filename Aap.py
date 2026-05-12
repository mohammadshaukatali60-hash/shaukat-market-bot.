import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# Page Configuration
st.set_page_config(page_title="Shaukat AI Bot", layout="wide")
st.title("🛡️ Shaukat AI: Live Trading Terminal")

# Sidebar
symbol = st.sidebar.selectbox("Select Asset", ["^NSEI", "^NSEBANK", "RELIANCE.NS"])
timeframe = st.sidebar.selectbox("Timeframe", ["5m", "15m", "1h", "1d"])

try:
    # Fetch Data
    data = yf.download(symbol, period="5d", interval=timeframe)
    
    if not data.empty:
        # EMA Calculations (Manual Math - No extra library needed)
        data['EMA_20'] = data['Close'].ewm(span=20, adjust=False).mean()
        data['EMA_200'] = data['Close'].ewm(span=200, adjust=False).mean()
        
        # Price Metric
        l_price = data['Close'].iloc[-1]
        st.metric(f"{symbol} Live Price", f"₹{round(float(l_price), 2)}")

        # Candlestick Chart
        fig = go.Figure(data=[go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            name="Candlesticks"
        )])
        
        # Add EMA Lines
        fig.add_trace(go.Scatter(x=data.index, y=data['EMA_20'], name="EMA 20", line=dict(color='orange', width=1.5)))
        fig.add_trace(go.Scatter(x=data.index, y=data['EMA_200'], name="EMA 200", line=dict(color='blue', width=1.5)))
        
        fig.update_layout(template="plotly_dark", height=600, xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)
        
        st.success("Bot is Running Smoothly! 🚀")
    else:
        st.warning("Waiting for Market Data...")
except Exception as e:
    st.error("Error: Please check your Internet or Market Status.")
