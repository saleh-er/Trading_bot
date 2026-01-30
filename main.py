import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from src.data_loader import DataLoader
from src.strategy import TradingStrategy
from src.visualizer import Visualizer 
from backtests.backtest import Backtester
from src.sentiment_analyzer import SentimentAnalyzer
from src.notifier import TelegramNotifier

# Page Config
st.set_page_config(page_title="Institutional Trading Dashboard", layout="wide", page_icon="📈")

# Apply custom CSS
st.markdown("""
    <style>
    .stMetric { background-color: #1e2130; padding: 15px; border-radius: 10px; border: 1px solid #2d2e32; }
    [data-testid="stMetricValue"] { font-size: 24px; }
    </style>
    """, unsafe_allow_html=True)

def main():
    st.title("🛡️ Institutional Multi-Asset Scanner")
    st.sidebar.header("🕹️ Control Panel")

    # 1. Sidebar Config
    watchlist = st.sidebar.multiselect(
        "Watchlist Symbols", 
        ["BTC-USD", "ETH-USD", "SOL-USD", "^GSPC", "^IXIC", "AAPL", "NVDA", "TSLA", "MSFT", "GOOGL"],
        default=["BTC-USD", "ETH-USD", "^GSPC"]
    )
    period = st.sidebar.selectbox("Analysis Period", ["6mo", "1y", "2y", "5y"], index=1)
    capital = st.sidebar.number_input("Simulator Capital ($)", value=10000)

    # Risk Management Sidebar Controls
    st.sidebar.divider()
    st.sidebar.subheader("🛡️ Risk Parameters")
    risk_pct = st.sidebar.slider("Risk Per Trade (%)", 0.1, 5.0, 1.0)
    stop_loss_pct = st.sidebar.slider("Stop Loss (%)", 1.0, 10.0, 3.0)

    # NEW: Telegram Notification Sidebar
    st.sidebar.divider()
    st.sidebar.subheader("📱 Alerts")
    enable_alerts = st.sidebar.checkbox("Enable Telegram Notifications")
    tele_token = st.sidebar.text_input("Bot Token", type="password")
    tele_chat_id = st.sidebar.text_input("Chat ID")

    if not watchlist:
        st.warning("👈 Please select symbols in the sidebar to begin analysis.")
        return

    strategy = TradingStrategy()
    
    tab1, tab2, tab3 = st.tabs(["🔍 GLOBAL SCANNER", "📊 INDIVIDUAL DEEP DIVE", "🧬 CORRELATION"])

    with tab1:
        st.subheader("Real-Time Signals Dashboard")
        grid_cols = st.columns(3) 
        progress_bar = st.progress(0)
        
        for i, symbol in enumerate(watchlist):
            progress_bar.progress((i + 1) / len(watchlist))
            loader = DataLoader(symbol)
            df = loader.fetch_data(period=period)
            
            if df.empty: continue
                
            df = strategy.add_indicators(df)
            df = strategy.generate_signals(df)
            
            last_row = df.iloc[-1]
            price = last_row['Close'].item() if hasattr(last_row['Close'], 'item') else last_row['Close']
            signal = last_row['Signal'].item() if hasattr(last_row['Signal'], 'item') else last_row['Signal']
            rsi = last_row['RSI'].item() if hasattr(last_row['RSI'], 'item') else last_row['RSI']

            # Trigger Telegram Alerts
            if enable_alerts and tele_token and tele_chat_id:
                notifier = TelegramNotifier(tele_token, tele_chat_id)
                if signal == 1:
                    notifier.send_alert(f"🚀 *BUY ALERT*: {symbol}\nPrice: ${price:,.2f}\nRSI: {rsi:.1f}")
                elif signal == -1:
                    notifier.send_alert(f"🔻 *SELL ALERT*: {symbol}\nPrice: ${price:,.2f}\nRSI: {rsi:.1f}")

            with grid_cols[i % 3]:
                with st.container():
                    if signal == 1:
                        st.success(f"**{symbol}** | 🚀 BUY SIGNAL")
                    elif signal == -1:
                        st.error(f"**{symbol}** | 🔻 SELL SIGNAL")
                    else:
                        st.info(f"**{symbol}** | 😴 NEUTRAL")
                    st.metric("Price", f"${price:,.2f}", delta=f"RSI: {rsi:.1f}")
                    st.divider()
        progress_bar.empty()

    with tab2:
        st.subheader("Technical & Sentiment Deep Dive")
        selected_stock = st.selectbox("Select Asset to Inspect", watchlist)
        
        loader = DataLoader(selected_stock)
        df_detailed = loader.fetch_data(period=period)
        df_detailed = strategy.add_indicators(df_detailed)
        df_detailed = strategy.generate_signals(df_detailed)

        mood_score = SentimentAnalyzer.get_sentiment(selected_stock)
        
        c1, c2 = st.columns([1, 3])
        with c1:
            st.write("### Market Mood")
            if mood_score > 0.05:
                st.write(f"## 😊 Bullish ({mood_score:.2f})")
            elif mood_score < -0.05:
                st.write(f"## 😨 Bearish ({mood_score:.2f})")
            else:
                st.write(f"## 😐 Neutral ({mood_score:.2f})")
        
        with c2:
            risk_amount = capital * (risk_pct / 100)
            pos_size = risk_amount / (stop_loss_pct / 100)
            st.write("### Risk Strategy")
            st.info(f"💡 Based on your settings, risk **${risk_amount:,.2f}** to buy **${pos_size:,.2f}** of {selected_stock}.")

        st.divider()

        bt = Backtester(initial_capital=capital)
        final_val, ret, trades = bt.run(df_detailed)

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Final Portfolio", f"${final_val:,.2f}")
        m2.metric("Net ROI", f"{ret:.2f}%")
        m3.metric("Total Trades", trades)
        
        first_p = df_detailed['Close'].iloc[0].item()
        last_p = df_detailed['Close'].iloc[-1].item()
        bh_ret = ((last_p - first_p) / first_p) * 100
        m4.metric("Buy & Hold ROI", f"{bh_ret:.2f}%")

        fig = Visualizer.plot_professional(df_detailed, selected_stock)
        st.plotly_chart(fig, use_container_width=True, theme=None)

    with tab3:
        st.subheader("Asset Correlation Matrix")
        st.write("Understand how assets move relative to each other.")

        if len(watchlist) > 1:
            corr_data = {}
            for symbol in watchlist:
                loader = DataLoader(symbol)
                df_corr = loader.fetch_data(period=period)
                if not df_corr.empty:
                    corr_data[symbol] = df_corr['Close']
            
            corr_df = pd.DataFrame(corr_data).corr()
            
            fig_corr, ax = plt.subplots(figsize=(10, 8))
            sns.heatmap(corr_df, annot=True, cmap='RdYlGn', center=0, ax=ax)
            ax.set_title("Portfolio Correlation Heatmap")
            st.pyplot(fig_corr)
            
            high_corr = corr_df[corr_df > 0.8].stack().reset_index()
            high_corr = high_corr[high_corr['level_0'] != high_corr['level_1']]
            if not high_corr.empty:
                st.warning("⚠️ High Correlation Detected! Diversification is limited.")
        else:
            st.info("Add more assets to your watchlist to see correlations.")

if __name__ == "__main__":
    main()