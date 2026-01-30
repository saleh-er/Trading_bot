from src.data_loader import DataLoader
from src.strategy import TradingStrategy
import os

def main():
    # --- 1. SETTINGS ---
    symbol = "BTC-USD"  # You can change this to "AAPL" or "ETH-USD"
    interval = "1d"
    period = "1y"

    print(f"--- Starting Trading Bot Analysis for {symbol} ---")

    # --- 2. FETCH DATA ---
    # We initialize our DataLoader module
    loader = DataLoader(symbol, interval=interval)
    df = loader.fetch_data(period=period)

    if df.empty:
        print("❌ Error: No data found. Check your ticker symbol.")
        return

    # --- 3. APPLY STRATEGY ---
    # We initialize our Strategy module
    strategy = TradingStrategy(rsi_period=14, sma_fast=20, sma_slow=50)
    
    # Add indicators (RSI, SMA)
    df = strategy.add_indicators(df)
    
    # Generate signals (Buy/Sell)
    df = strategy.generate_signals(df)

    # --- 4. SHOW RESULTS ---
    # Display the last 10 rows of relevant data
    print("\nRecent Market Data & Signals:")
    cols_to_show = ['Close', 'RSI', 'SMA_Fast', 'SMA_Slow', 'Signal']
    print(df[cols_to_show].tail(10))

    # Identify the current action
    current_signal = df['Signal'].iloc[-1]
    
    print("\n" + "="*30)
    if current_signal == 1:
        print("🚀 CURRENT STATUS: BUY SIGNAL")
    elif current_signal == -1:
        print("🔻 CURRENT STATUS: SELL SIGNAL")
    else:
        print("😴 CURRENT STATUS: NEUTRAL (WAITING)")
    print("="*30)

if __name__ == "__main__":
    main()