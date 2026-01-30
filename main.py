import streamlit as st
import pandas as pd
from src.data_loader import DataLoader
from src.strategy import TradingStrategy
from src.visualizer import Visualizer 
from backtests.backtest import Backtester

# Page Config - Sets the Bloomberg-style wide layout
st.set_page_config(page_title="Institutional Trading Dashboard", layout="wide", page_icon="📈")

# Apply custom CSS for a cleaner "Dark Mode" look
st.markdown("""
    <style>
    .stMetric { background-color: #1e2130; padding: 15px; border-radius: 10px; border: 1px solid #2d2e32; }
    [data-testid="stMetricValue"] { font-size: 24px; }
    </style>
    """, unsafe_allow_index=True)

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

    if not watchlist:
        st.warning("👈 Please select symbols in the sidebar to begin analysis.")
        return

    strategy = TradingStrategy()
    
    # Create Navigation Tabs
    tab1, tab2 = st.tabs(["🔍 GLOBAL SCANNER", "📊 INDIVIDUAL DEEP DIVE"])

    with tab1:
        st.subheader("Real-Time Signals Dashboard")
        
        # Grid layout for signals
        # We use a loop with columns to prevent the UI from becoming too vertically long
        grid_cols = st.columns(3) 
        
        progress_bar = st.progress(0)
        for i, symbol in enumerate(watchlist):
            # Update progress
            progress_bar.progress((i + 1) / len(watchlist))
            
            # Fetch and process
            loader = DataLoader(symbol)
            df = loader.fetch_data(period=period)
            
            if df.empty:
                continue
                
            df = strategy.add_indicators(df)
            df = strategy.generate_signals(df)
            
            last_row = df.iloc[-1]
            # Handle potential Series/Scalar issue from earlier
            price = last_row['Close'].item() if hasattr(last_row['Close'], 'item') else last_row['Close']
            signal = last_row['Signal'].item() if hasattr(last_row['Signal'], 'item') else last_row['Signal']
            rsi = last_row['RSI'].item() if hasattr(last_row['RSI'], 'item') else last_row['RSI']

            # Place card in the grid
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
        st.subheader("Technical Performance Analysis")
        selected_stock = st.selectbox("Select Asset to Inspect", watchlist)
        
        # Load data for selected specific asset
        loader = DataLoader(selected_stock)
        df_detailed = loader.fetch_data(period=period)
        df_detailed = strategy.add_indicators(df_detailed)
        df_detailed = strategy.generate_signals(df_detailed)

        # 1. Backtest Analytics
        bt = Backtester(initial_capital=capital)
        final_val, ret, trades = bt.run(df_detailed)

        # Performance Metrics Header
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Final Portfolio", f"${final_val:,.2f}")
        m2.metric("Net ROI", f"{ret:.2f}%", delta=f"{ret:.2f}%")
        m3.metric("Total Trades", trades)
        
        # Benchmarking
        first_p = df_detailed['Close'].iloc[0].item() if hasattr(df_detailed['Close'].iloc[0], 'item') else df_detailed['Close'].iloc[0]
        last_p = df_detailed['Close'].iloc[-1].item() if hasattr(df_detailed['Close'].iloc[-1], 'item') else df_detailed['Close'].iloc[-1]
        bh_ret = ((last_p - first_p) / first_p) * 100
        m4.metric("Buy & Hold ROI", f"{bh_ret:.2f}%")

        # 2. The Professional Plotly Chart
        st.markdown("---")
        fig = Visualizer.plot_professional(df_detailed, selected_stock)
        st.plotly_chart(fig, use_container_width=True, theme=None) # theme=None keeps your custom dark colors

if __name__ == "__main__":
    main()