import pandas as pd

class Backtester:
    def __init__(self, initial_capital=10000):
        self.initial_capital = initial_capital
        self.balance = initial_capital
        self.position = 0  # Number of units held
        self.trades = 0

    def run(self, df):
        """Simulates trading based on the 'Signal' column"""
        # We start tracking from the first row where we have indicators
        df = df.dropna().copy()
        
        for index, row in df.iterrows():
            # BUY Logic: If signal is 1 and we are not already in a position
            if row['Signal'] == 1 and self.position == 0:
                self.position = self.balance / row['Close']
                self.balance = 0
                self.trades += 1
                # print(f"BUY at {row['Close']:.2f} on {index}")

            # SELL Logic: If signal is -1 and we hold a position
            elif row['Signal'] == -1 and self.position > 0:
                self.balance = self.position * row['Close']
                self.position = 0
                self.trades += 1
                # print(f"SELL at {row['Close']:.2f} on {index}")

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