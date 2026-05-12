import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Shaukat Scalper Pro", layout="wide")
st.title("⚡ Shaukat AI: Professional Scalper")

symbol = st.sidebar.selectbox("Select Asset", ["BTC-USD", "^NSEI", "^NSEBANK"])
timeframe = st.sidebar.selectbox("Timeframe", ["1m", "5m", "15m"])

try:
    # Data Fetching
    data = yf.download(symbol, period="1d", interval=timeframe)
    
    if not data.empty:
        # Technicals
        data['EMA_9'] = data['Close'].ewm(span=9, adjust=False).mean()
        data['EMA_21'] = data['Close'].ewm(span=21, adjust=False).mean()
        
        # Price Display (Fixed the Error)
        last_price = float(data['Close'].iloc[-1])
        st.metric(f"Live {symbol}", f"₹{round(last_price, 2)}")

        # Professional Scalping Chart
        fig = go.Figure()
        fig.add_trace(go.Candlestick(x=data.index, open=data['Open'], high=data['High'], 
                                   low=data['Low'], close=data['Close'], name="Price"))
        
        # Signals Logic (Arrows)
        buy_cond = (data['EMA_9'] > data['EMA_21']) & (data['EMA_9'].shift(1) <= data['EMA_21'].shift(1))
        sell_cond = (data['EMA_9'] < data['EMA_21']) & (data['EMA_9'].shift(1) >= data['EMA_21'].shift(1))
        
        fig.add_trace(go.Scatter(x=data.index[buy_cond], y=data['Low'][buy_cond]*0.999, mode='markers', 
                                 marker=dict(color='lime', size=15, symbol='triangle-up'), name="BUY"))
        fig.add_trace(go.Scatter(x=data.index[sell_cond], y=data['High'][sell_cond]*1.001, mode='markers', 
                                 marker=dict(color='red', size=15, symbol='triangle-down'), name="SELL"))

        fig.update_layout(template="plotly_dark", height=600, xaxis_rangeslider_visible=False,
                          dragmode=False, yaxis=dict(fixedrange=True), xaxis=dict(fixedrange=True))
        
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        st.success("Scalping signals fixed! Try now. 🚀")
    else:
        st.warning("Fetching data...")
except Exception as e:
    st.error("System Refreshing... Please click 'Get Live Update'")

if st.button('🔄 Get Live Update'):
    st.rerun()
