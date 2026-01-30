# 🛡️ Institutional Multi-Asset Scanner & Trading Bot

An advanced algorithmic trading dashboard built with **Python**, **Streamlit**, and **Plotly**. This tool provides real-time market scanning, technical deep dives, and automated sentiment analysis.

## 🚀 Live Features
- **Global Scanner**: Real-time monitoring of multiple assets (Crypto & Indices).
- **Triple Confirmation Strategy**: Buy/Sell signals based on RSI, Bollinger Bands, and MACD alignment.
- **Sentiment Analysis**: Live news processing using Natural Language Processing (NLP).
- **Risk Management**: Dynamic position sizing based on custom risk parameters.

---

## 📸 Dashboard Showcase

### 🔍 Global Market Scanner
Monitor your entire watchlist at a glance with real-time RSI indicators and signal status.

<p align="center">
  <img src="assets/pi1.png" width="90%" alt="Global Scanner View">
</p>

### 📊 Individual Deep Dive
Deep analysis for specific assets including interactive Plotly charts and strategy backtesting.

<p align="center">
  <img src="assets/pi3.png" width="90%" alt="Deep Dive Analysis">
</p>

---

## 🛠️ Technical Stack
- **Frontend**: Streamlit (Custom CSS for Bloomberg-style Dark Mode)
- **Data**: Yahoo Finance API (via `yfinance`)
- **Visuals**: Plotly Interactive Charts (4-tier layout)
- **Indicators**: `ta` library (RSI, Bollinger Bands, MACD, SMA)
- **Alerts**: Telegram Bot API integration

## ⚠️ Disclaimer
This project is for **educational purposes only**. Trading involves significant risk. Never trade with money you cannot afford to lose. The author is not responsible for any financial losses incurred using this software.