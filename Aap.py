import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

st.set_page_config(page_title="Shaukat Market Bot", layout="wide")
st.title("🛡️ Shaukat AI: Live Trading Chart")

# Market Symbol Select
symbol = st.sidebar.selectbox("Market Symbol", ["^NSEI", "^NSEBANK", "RELIANCE.NS"])

try:
    # Fetch Data
    df = yf.download(symbol, period="1d", interval="5m")
    
    if not df.empty:
        last_price = round(df['Close'].iloc[-1], 2)
        st.metric(f"{symbol} Live Price", f"₹{last_price}")
        
        # Simple Candlestick Chart
        fig = go.Figure(data=[go.Candlestick(
            x=df.index, open=df['Open'], high=df['High'], 
            low=df['Low'], close=df['Close']
        )])
        fig.update_layout(template="plotly_dark", height=600)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Market ka data abhi fetch ho raha hai... Thoda intezar karein.")
except:
    st.error("Market close hai ya internet check karein.")
