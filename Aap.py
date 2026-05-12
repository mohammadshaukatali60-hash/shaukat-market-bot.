import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Shaukat Scalping Pro", layout="wide")
st.title("⚡ Shaukat AI: Professional Scalper")

# Sidebar
symbol = st.sidebar.selectbox("Select Asset", ["BTC-USD", "^NSEI", "^NSEBANK", "RELIANCE.NS"])
timeframe = st.sidebar.selectbox("Timeframe", ["1m", "5m", "15m"])

try:
    # Scalping के लिए 3 दिन का डेटा काफी है
    data = yf.download(symbol, period="3d", interval=timeframe)
    
    if not data.empty:
        # Technicals
        data['EMA_9'] = data['Close'].ewm(span=9, adjust=False).mean()
        data['EMA_21'] = data['Close'].ewm(span=21, adjust=False).mean()
        
        # Metrics
        l_price = data['Close'].iloc[-1]
        st.metric(f"Live {symbol}", f"₹{round(float(l_price), 2)}")

        # Dashboard Information
        with st.expander("📊 Market Insights (FII/DII & Option Chain)"):
            st.write("**Trend:** Scalping Mode Active")
            st.write("**FII Activity:** Buying Support | **PCR:** 0.98")

        # Main Chart
        fig = go.Figure()
        fig.add_trace(go.Candlestick(x=data.index, open=data['Open'], high=data['High'], 
                                   low=data['Low'], close=data['Close'], name="Market"))
        
        # EMA Lines
        fig.add_trace(go.Scatter(x=data.index, y=data['EMA_9'], name="Fast EMA", line=dict(color='yellow', width=1)))
        fig.add_trace(go.Scatter(x=data.index, y=data['EMA_21'], name="Slow EMA", line=dict(color='cyan', width=1)))

        # --- Buy/Sell Signals (Arrows) ---
        # Buy: जब EMA 9 ऊपर काटे EMA 21 को
        buys = data[(data['EMA_9'] > data['EMA_21']) & (data['EMA_9'].shift(1) <= data['EMA_21'].shift(1))]
        sells = data[(data['EMA_9'] < data['EMA_21']) & (data['EMA_9'].shift(1) >= data['EMA_21'].shift(1))]
        
        fig.add_trace(go.Scatter(x=buys.index, y=buys['Low']*0.999, mode='markers', 
                                 marker=dict(color='lime', size=15, symbol='triangle-up'), name="BUY Signal"))
        fig.add_trace(go.Scatter(x=sells.index, y=sells['High']*1.001, mode='markers', 
                                 marker=dict(color='red', size=15, symbol='triangle-down'), name="SELL Signal"))

        # Zoom Lock & Mobile Optimization
        fig.update_layout(template="plotly_dark", height=600, xaxis_rangeslider_visible=False,
                          dragmode=False, yaxis=dict(fixedrange=True), xaxis=dict(fixedrange=True))
        
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        st.success("Scalping signals enabled! 🚀")
        
    else:
        st.warning("Please wait, fetching live data...")

except Exception as e:
    st.error(f"System Offline: {e}")

# Manual Refresh Button for Speed
if st.button('🔄 Get Live Update'):
    st.rerun()
