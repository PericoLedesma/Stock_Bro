# Stock_Bro
**Stock_Bro** will be a multi-agent system with specialized agents collaborating to deliver investment guidance.


## 🚀 Features

- [ ] **📊 Real-time Stock Data**: Fetch current and historical prices using `yfinance`.
- [ ] **🔍 Technical Analysis**: Compute SMA, EMA, RSI, MACD, Bollinger Bands, and more.
- [ ] **🤖 AI Predictions**: Random Forest-based price prediction experiments.
- [ ] **🌐 REST API**: FastAPI-powered REST API for data and model access.
- [ ] **📈 Trend Analysis**: Identify market trends and momentum.
- [ ] **🎯 Support/Resistance**: Automatic detection of key price levels.


## 📦 Application Modules

### Portfolio
- Create and maintain a database of the current portfolio.
- Accept user inputs: stock ticker, purchase date, and purchase price.
- Track gains/losses and price performance; compute profitability by time period.
- Provide a brief portfolio analysis:
  - Risks
  - News
  - Sell or hold recommendation

### Search for New Opportunities
- Identify investment trends and momentum.
- Suggest where to invest (e.g., sectors, tickers, ETFs).
- Provide a market overview (breadth, volatility, macro context).


## 🧠 Project Architecture Overview

stock_bro/
backend/
    ├── app/
    │   ├── main.py
    │   ├── models/
    │   ├── services/
    │   ├── agents/
    │   └── utils/
    ├── tests/
    ├── Dockerfile
    ├── requirements.txt
    ├── README.md
    ├── .env
    └── .gitignore
frontend/
    ├── public/
    ├── src/
    ├── package.json
    ├── Dockerfile
    └── README.md

