import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Shaukat Scalping Pro", layout="wide")

# Sidebar for Scalping Tools
st.sidebar.header("⚡ Scalper Controls")
symbol = st.sidebar.selectbox("Asset", ["BTC-USD", "^NSEI", "^NSEBANK", "RELIANCE.NS"])
# स्कल्पिंग के लिए 1m या 5m बेस्ट होता है
timeframe = st.sidebar.selectbox("Timeframe", ["1m", "5m", "15m"])

st.title("🚀 Shaukat AI: Live Scalping Terminal")

try:
    # कम डेटा ताकि लोड जल्दी हो (Scalping के लिए बेस्ट)
    data = yf.download(symbol, period="1d", interval=timeframe)
    
    if not data.empty:
        # Indicators for Scalping
        data['EMA_9'] = data['Close'].ewm(span=9, adjust=False).mean()
        data['EMA_21'] = data['Close'].ewm(span=21, adjust=False).mean()
        
        # Dashboard
        l_price = data['Close'].iloc[-1]
        change = l_price - data['Open'].iloc[-1]
        st.metric("Live Price", f"₹{round(l_price, 2)}", f"{round(change, 2)}")

        # Scalping Chart
        fig = go.Figure()
        fig.add_trace(go.Candlestick(x=data.index, open=data['Open'], high=data['High'], 
                                   low=data['Low'], close=data['Close'], name="Price"))
        
        # EMA Lines for Trend
        fig.add_trace(go.Scatter(x=data.index, y=data['EMA_9'], name="Fast EMA (9)", line=dict(color='yellow', width=1)))
        fig.add_trace(go.Scatter(x=data.index, y=data['EMA_21'], name="Slow EMA (21)", line=dict(color='cyan', width=1)))

        # Buy/Sell Logic for Scalping
        # जब EMA 9, EMA 21 को ऊपर काटे (Golden Cross)
        data['Signal'] = 0
        data.loc[data['EMA_9'] > data['EMA_21'], 'Signal'] = 1
        data.loc[data['EMA_9'] < data['EMA_21'], 'Signal'] = -1
        
        fig.update_layout(template="plotly_dark", height=600, xaxis_rangeslider_visible=False,
                          dragmode=False, yaxis=dict(fixedrange=True), xaxis=dict(fixedrange=True))
        
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        
        st.success("Scalping Mode Active! ⚡")
        
    else:
        st.warning("Data fetch ho raha hai... Wait karein.")

except Exception as e:
    st.error(f"Error: {e}")

# Auto-refresh logic (Sahi wala)
if st.button('🔄 Refresh Manual'):
    st.rerun()
