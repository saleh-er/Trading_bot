import streamlit as st
import pandas as pd
from src.data_loader import DataLoader
from src.strategy import TradingStrategy
from src.visualizer import Visualizer  # Updated for Plotly
from backtests.backtest import Backtester

# Page Config
st.set_page_config(page_title="Pro Algo-Trading Dashboard", layout="wide", page_icon="📈")

def main():
    st.title("🛡️ Institutional Trading Scanner")
    st.sidebar.header("Configuration")

    # 1. Sidebar Settings
    watchlist = st.sidebar.multiselect(
        "Select Watchlist", 
        ["BTC-USD", "ETH-USD", "SOL-USD", "^GSPC", "^IXIC", "AAPL", "NVDA", "TSLA"],
        default=["BTC-USD", "^GSPC", "NVDA"]
    )
    period = st.sidebar.selectbox("Period", ["6mo", "1y", "2y"], index=1)
    capital = st.sidebar.number_input("Initial Capital ($)", value=1000)

    if not watchlist:
        st.info("Please select at least one ticker from the sidebar.")
        return

    # 2. Processing Data
    strategy = TradingStrategy()
    
    # Create Tabs for different views
    tab1, tab2 = st.tabs(["🔍 Market Scanner", "📊 Deep Analysis"])

    with tab1:
        st.subheader("Live Market Signals")
        cols = st.columns(len(watchlist))
        
        for i, symbol in enumerate(watchlist):
            loader = DataLoader(symbol)
            df = loader.fetch_data(period=period)
            df = strategy.add_indicators(df)
            df = strategy.generate_signals(df)
            
            last_row = df.iloc[-1]
            signal = last_row['Signal'].item()
            price = last_row['Close'].item()

            # Display "Metric" Cards
            with cols[i]:
                if signal == 1:
                    st.success(f"**{symbol}**\n\n🚀 BUY\n\n${price:,.2f}")
                elif signal == -1:
                    st.error(f"**{symbol}**\n\n🔻 SELL\n\n${price:,.2f}")
                else:
                    st.metric(label=symbol, value=f"${price:,.2f}", delta="Neutral")

    with tab2:
        selected_stock = st.selectbox("Select Asset for Detailed View", watchlist)
        # Fetch data for selected stock
        loader = DataLoader(selected_stock)
        df = loader.fetch_data(period=period)
        df = strategy.add_indicators(df)
        df = strategy.generate_signals(df)

        # Backtest
        bt = Backtester(initial_capital=capital)
        final_val, ret, trades = bt.run(df)

        # Display Stats
        col1, col2, col3 = st.columns(3)
        col1.metric("Final Value", f"${final_val:,.2f}")
        col2.metric("Total Return", f"{ret:.2f}%")
        col3.metric("Trades Executed", trades)

        # Interactive Plotly Chart
        fig = Visualizer.plot_professional(df, selected_stock)
        st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()