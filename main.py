from src.data_loader import DataLoader
from src.strategy import TradingStrategy
from backtests.backtest import Backtester
from src.visualizer import Visualizer 
import os
import pandas as pd

def main():
    watchlist = ["BTC-USD", "ETH-USD", "^GSPC", "^IXIC", "NVDA", "AAPL"]
    all_data = {}
    strategy = TradingStrategy()

    for symbol in watchlist:
        loader = DataLoader(symbol)
        df = loader.fetch_data(period="6mo")
        
        if not df.empty:
            df = strategy.add_indicators(df)
            df = strategy.generate_signals(df)
            all_data[symbol] = df
            print(f"✅ Processed {symbol}")

    # Generate the multi-asset chart
    if all_data:
        Visualizer.plot_multi_assets(all_data)

if __name__ == "__main__":
    main()