import yfinance as yf
import pandas as pd

class DataLoader:  # <--- Make sure this name is exactly like this
    def __init__(self, ticker, interval="1d"):
        self.ticker = ticker
        self.interval = interval

    def fetch_data(self, period="1y"):
        print(f"Fetching data for {self.ticker}...")
        data = yf.download(
            tickers=self.ticker,
            period=period,
            interval=self.interval,
            progress=False
        )
        data.dropna(inplace=True)
        return data