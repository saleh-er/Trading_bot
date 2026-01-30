import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import SMAIndicator, MACD
from ta.volatility import BollingerBands

class TradingStrategy:
    def __init__(self, rsi_period=14, sma_fast=20, sma_slow=50, bb_period=20, bb_std=2):
        self.rsi_period = rsi_period
        self.sma_fast = sma_fast
        self.sma_slow = sma_slow
        self.bb_period = bb_period
        self.bb_std = bb_std

    def add_indicators(self, df):
        """Adds triple-confirmation indicators using the 'ta' library"""
        close_prices = df['Close'].squeeze()
        
        # 1. RSI (Momentum Oscillator)
        df['RSI'] = RSIIndicator(close=close_prices, window=self.rsi_period).rsi()
        
        # 2. Moving Averages (Trend)
        df['SMA_Fast'] = SMAIndicator(close=close_prices, window=self.sma_fast).sma_indicator()
        df['SMA_Slow'] = SMAIndicator(close=close_prices, window=self.sma_slow).sma_indicator()
        
        # 3. MACD (Momentum Trend)
        macd_indicator = MACD(close=close_prices)
        df['MACD'] = macd_indicator.macd()
        df['MACD_Signal'] = macd_indicator.macd_signal()
        df['MACD_Diff'] = macd_indicator.macd_diff() # Histogram
        
        # 4. Bollinger Bands (Volatility)
        bb_indicator = BollingerBands(close=close_prices, window=self.bb_period, window_dev=self.bb_std)
        df['BB_High'] = bb_indicator.bollinger_hband()
        df['BB_Low'] = bb_indicator.bollinger_lband()
        df['BB_Mid'] = bb_indicator.bollinger_mavg()
        
        return df

    def generate_signals(self, df):
        """
        Triple Confirmation Logic:
        - BUY: RSI < 35 (Oversold), Price < BB_Low (Volatility limit), MACD turning Bullish
        - SELL: RSI > 65 (Overbought), Price > BB_High (Volatility limit), MACD turning Bearish
        """
        # Initialize the signal column
        df['Signal'] = 0

        # Extract underlying values to avoid index alignment issues
        # This converts Pandas columns into raw Numpy arrays for high-speed comparison
        close = df['Close'].values.flatten()
        rsi = df['RSI'].values.flatten()
        bb_low = df['BB_Low'].values.flatten()
        bb_high = df['BB_High'].values.flatten()
        macd_diff = df['MACD_Diff'].values.flatten()

        # --- BUY SIGNAL (Triple Confirmation) ---
        # Logic: RSI Oversold + Price at BB Floor + MACD turning up
        buy_mask = (rsi < 35) & (close <= bb_low) & (macd_diff > 0)
        
        # Now this will work because buy_mask is strictly 1D
        df.loc[buy_mask, 'Signal'] = 1
        
        # --- SELL SIGNAL (Triple Confirmation) ---
        # Logic: RSI Overbought + Price at BB Ceiling + MACD turning down
        sell_mask = (rsi > 65) & (close >= bb_high) & (macd_diff < 0)
        df.loc[sell_mask, 'Signal'] = -1
        
        return df