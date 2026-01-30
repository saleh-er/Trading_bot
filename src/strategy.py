import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import SMAIndicator

class TradingStrategy:
    def __init__(self, rsi_period=14, sma_fast=20, sma_slow=50):
        self.rsi_period = rsi_period
        self.sma_fast = sma_fast
        self.sma_slow = sma_slow

    def add_indicators(self, df):
        """Adds technical indicators using the 'ta' library"""
        # Close prices must be a Series
        close_prices = df['Close']
        
        # Add RSI
        df['RSI'] = RSIIndicator(close=close_prices, window=self.rsi_period).rsi()
        
        # Add SMAs
        df['SMA_Fast'] = SMAIndicator(close=close_prices, window=self.sma_fast).sma_indicator()
        df['SMA_Slow'] = SMAIndicator(close=close_prices, window=self.sma_slow).sma_indicator()
        
        return df

    def generate_signals(self, df):
        """Signal logic remains the same"""
        df['Signal'] = 0
        
        # Buy Signal (RSI < 30 and Fast SMA > Slow SMA)
        df.loc[(df['RSI'] < 30) & (df['SMA_Fast'] > df['SMA_Slow']), 'Signal'] = 1
        
        # Sell Signal (RSI > 70)
        df.loc[(df['RSI'] > 70), 'Signal'] = -1
        
        return df