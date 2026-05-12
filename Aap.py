import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Shaukat AI Pro", layout="wide")
st.title("🛡️ Shaukat AI: Live Trading Terminal")

# Sidebar
symbol = st.sidebar.selectbox("Select Asset", ["BTC-USD", "^NSEI", "^NSEBANK", "RELIANCE.NS"])
timeframe = st.sidebar.selectbox("Timeframe", ["5m", "15m", "1h", "1d"])

try:
    # डेटा मंगाने का सबसे स्टेबल तरीका
    ticker = yf.Ticker(symbol)
    data = ticker.history(period="2d", interval=timeframe)
    
    if not data.empty:
        # Price Metric
        last_price = data['Close'].iloc[-1]
        st.metric(f"{symbol} Price", f"₹{round(float(last_price), 2)}")

        # Candlestick Chart
        fig = go.Figure(data=[go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close']
        )])
        
        fig.update_layout(template="plotly_dark", height=600, xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)
        st.success("Live Update Active! 🚀")
    else:
        # अगर निफ्टी काम नहीं कर रहा, तो बिटकॉइन चेक करें
        st.warning("Nifty data abhi nahi mil raha. Sidebar se 'BTC-USD' select karke dekhein agar chart aa raha hai.")

except Exception as e:
    st.error(f"Error: {e}")
