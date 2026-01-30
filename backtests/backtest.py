import pandas as pd

class Backtester:
    def __init__(self, initial_capital=10000):
        self.initial_capital = initial_capital
        self.balance = initial_capital
        self.position = 0  # Number of units held
        self.trades = 0

    def run(self, df):
        """Simulates trading based on the 'Signal' column"""
        df = df.dropna().copy()
        
        for index, row in df.iterrows():
            # Extract the actual value from the signal column
            # We use .item() to turn a single-element Series into a scalar
            try:
                # If row['Signal'] is a Series, .item() gets the value. 
                # If it's already a scalar, it works too.
                signal = row['Signal'].item() if hasattr(row['Signal'], 'item') else row['Signal']
                price = row['Close'].item() if hasattr(row['Close'], 'item') else row['Close']
            except ValueError:
                # Fallback if there are multiple values for some reason
                signal = row['Signal'].iloc[0] if hasattr(row['Signal'], 'iloc') else row['Signal']
                price = row['Close'].iloc[0] if hasattr(row['Close'], 'iloc') else row['Close']

            # BUY Logic
            if signal == 1 and self.position == 0:
                self.position = self.balance / price
                self.balance = 0
                self.trades += 1

            # SELL Logic
            elif signal == -1 and self.position > 0:
                self.balance = self.position * price
                self.position = 0
                self.trades += 1

        # Final evaluation: If we are still holding, sell at the last price
        final_price = df['Close'].iloc[-1]
        if self.position > 0:
            self.balance = self.position * final_price
            self.position = 0

        # Performance Metrics
        total_return = ((self.balance - self.initial_capital) / self.initial_capital) * 100
        return self.balance, total_return, self.trades

if __name__ == "__main__":
    print("Backtester module ready.")