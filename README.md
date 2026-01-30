# Algorithmic Trading Bot Project (WIP)

## 📌 Project Overview
This is a personal project focused on building a modular **Algorithmic Trading Bot** using Python. The goal is to develop a system capable of automated market analysis, backtesting strategies, and eventually executing trades via API.

> **Status: 🚧 Under Development**
> Currently setting up the core architecture and data ingestion modules.

## 🏗️ Architecture
The project follows a modular design to ensure scalability and ease of testing:
- **Data Loader**: Fetching historical and real-time data from various sources (Yahoo Finance, Crypto Exchanges).
- **Strategy Engine**: Implementation of technical indicators and signal logic.
- **Risk Management**: Position sizing, Stop-Loss, and Take-Profit logic.
- **Executor**: API integration for order execution (Planned).

## 🛠️ Tech Stack
- **Language:** Python 3.x
- **Libraries:** Pandas, Pandas-TA, YFinance, CCXT
- **Environment:** VS Code / Virtualenv

## 🚀 Current Roadmap
- [x] Project structure and environment setup
- [ ] Implement historical data fetching (`data_loader.py`)
- [ ] Develop basic SMA/RSI strategy logic (`strategy.py`)
- [ ] Create a backtesting engine
- [ ] Live data integration via WebSockets

## ⚠️ Disclaimer
This project is for **educational purposes only**. Trading involves significant risk. Never trade with money you cannot afford to lose. The author is not responsible for any financial losses incurred using this software.