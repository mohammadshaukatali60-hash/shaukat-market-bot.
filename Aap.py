import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Shaukat AI Pro", layout="wide")
st.title("🛡️ Shaukat AI: Professional Terminal")

# Sidebar
symbol = st.sidebar.selectbox("Select Asset", ["^NSEI", "^NSEBANK", "RELIANCE.NS", "BTC-USD"])
timeframe = st.sidebar.selectbox("Timeframe", ["5m", "15m", "1h", "1d"])

try:
    ticker = yf.Ticker(symbol)
    data = ticker.history(period="2d", interval=timeframe)
    
    if not data.empty:
        # EMA Calculation
        data['EMA_20'] = data['Close'].ewm(span=20, adjust=False).mean()
        
        # RSI Calculation (Manual)
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        data['RSI'] = 100 - (100 / (1 + rs))
        
        # Price Metric
        last_price = data['Close'].iloc[-1]
        st.metric(f"{symbol} Current Price", f"₹{round(float(last_price), 2)}")

        # Main Chart
        fig = go.Figure(data=[go.Candlestick(x=data.index, open=data['Open'], 
                        high=data['High'], low=data['Low'], close=data['Close'], name="Price")])
        fig.add_trace(go.Scatter(x=data.index, y=data['EMA_20'], name="EMA 20", line=dict(color='orange')))
        fig.update_layout(template="plotly_dark", height=500, xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)

        # RSI Chart
        st.subheader("🔭 RSI (Strength Indicator)")
        fig_rsi = go.Figure()
        fig_rsi.add_trace(go.Scatter(x=data.index, y=data['RSI'], name="RSI", line=dict(color='yellow')))
        fig_rsi.add_shape(type="line", x0=data.index[0], y0=70, x1=data.index[-1], y1=70, line=dict(color="red", dash="dash"))
        fig_rsi.add_shape(type="line", x0=data.index[0], y0=30, x1=data.index[-1], y1=30, line=dict(color="green", dash="dash"))
        fig_rsi.update_layout(template="plotly_dark", height=200)
        st.plotly_chart(fig_rsi, use_container_width=True)
        
    else:
        st.warning("Market is closed. Try BTC-USD for testing.")
except Exception as e:
    st.error(f"Error: {e}")
