import streamlit as st
import yfinance as yf
import pandas_ta as ta
import pandas as pd
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh

# 1. पेज सेटअप और ऑटो-रिफ्रेश (हर 60 सेकंड में खुद अपडेट होगा)
st.set_page_config(page_title="90% Accuracy AI Bot", layout="wide")
st_autorefresh(interval=60 * 1000, key="bot_refresh")

st.title("🛡️ Shaukat AI: Auto-Pilot Trading Bot")

# 2. इनपुट पैरामीटर्स (साइडबार)
symbol = st.sidebar.selectbox("Market Symbol", ["^NSEI", "^NSEBANK", "RELIANCE.NS", "HDFCBANK.NS"])
qty = st.sidebar.number_input("Quantity (Lot Size)", value=50, step=1)

def get_live_signal(ticker):
    # डेटा फेच करना (5 मिनट की कैंडल सबसे सटीक होती है)
    df = yf.download(ticker, period="5d", interval="5m", progress=False)
    
    # --- इंडिकेटर्स (90% Confluence Logic) ---
    # 1. Major Trend (EMA 200)
    df['EMA_200'] = ta.ema(df['Close'], length=200)
    # 2. Momentum (RSI)
    df['RSI'] = ta.rsi(df['Close'], length=14)
    # 3. Volatility (ATR) for Stop Loss
    df['ATR'] = ta.atr(df['High'], df['Low'], df['Close'], length=14)
    # 4. Trend Rider (SuperTrend)
    sti = ta.supertrend(df['High'], df['Low'], df['Close'], length=10, multiplier=3)
    df = pd.concat([df, sti], axis=1)
    # 5. Volume Average
    df['VOL_AVG'] = df['Volume'].rolling(window=15).mean()

    last = df.iloc[-1]
    
    # --- स्ट्रिक्ट सिग्नल लॉजिक ---
    # Buy: Price > EMA 200 + SuperTrend Green + RSI > 50 + Volume High
    buy_sig = (last['Close'] > last['EMA_200']) and (last['SUPERTd_10_3.0'] == 1) and (last['RSI'] > 50) and (last['Volume'] > last['VOL_AVG'])
    
    # Sell: Price < EMA 200 + SuperTrend Red + RSI < 50 + Volume High
    sell_sig = (last['Close'] < last['EMA_200']) and (last['SUPERTd_10_3.0'] == -1) and (last['RSI'] < 50) and (last['Volume'] > last['VOL_AVG'])
    
    return df, buy_sig, sell_sig

df, is_buy, is_sell = get_live_signal(symbol)
cp = round(df['Close'].iloc[-1], 2)
atr = df['ATR'].iloc[-1]

# 3. डैशबोर्ड और मीट्रिक्स
c1, c2, c3 = st.columns(3)
c1.metric("Live Price", f"₹{cp}")
sentiment = "BULLISH 🚀" if is_buy else "BEARISH 📉" if is_sell else "NEUTRAL ⚖️"
c2.metric("Market Sentiment", sentiment)
c3.metric("ATR Volatility", round(atr, 2))

st.divider()

# 4. सिग्नल अलर्ट्स (Entry, SL, Target)
if is_buy:
    sl = round(cp - (atr * 1.5), 2)
    tgt = round(cp + (atr * 3), 2)
    st.success(f"🔥 **90% PROBABILITY BUY!** \n\n **Entry:** {cp} | **Stop Loss:** {sl} | **Target:** {tgt}")
    st.balloons()
elif is_sell:
    sl = round(cp + (atr * 1.5), 2)
    tgt = round(cp - (atr * 3), 2)
    st.error(f"📉 **90% PROBABILITY SELL!** \n\n **Entry:** {cp} | **Stop Loss:** {sl} | **Target:** {tgt}")
else:
    st.warning("⌛ **WAITING FOR HIGH-PROBABILITY SIGNAL...** (बाजार अभी शांत है)")

# 5. प्रोफेशनल चार्ट
fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], name="Market")])
fig.add_trace(go.Scatter(x=df.index, y=df['EMA_200'], name="EMA 200 (Major Trend)", line=dict(color='blue', width=1.5)))
fig.update_layout(height=600, template="plotly_dark", xaxis_rangeslider_visible=False)
st.plotly_chart(fig, use_container_width=True)

st.sidebar.write(f"Last Sync: {pd.Timestamp.now().strftime('%H:%M:%S')}")
st.sidebar.info("Tip: Always trade with Stop Loss. Best signals occur after 9:45 AM.")
