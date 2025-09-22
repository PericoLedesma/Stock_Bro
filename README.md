# Stock_Bro
**Stock_Bro** will be a multi-agent system with specialized agents collaborating to deliver investment guidance.




## 📦 Application features

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

## Basic Folder Structure
Stock Bro App
├── Frontend
│   ├── public/                   # Static files (index.html, favicon, images)
│   └── src/
│       ├── components/           # Reusable UI components
│       │   ├── Portfolio.js
│       │   ├── AddStockForm.js
│       │   └── MarketAnalysis.js
│       │
│       ├── pages/                # Full pages for routing
│       │   ├── HomePage.js
│       │   ├── PortfolioPage.js
│       │   ├── AddStockPage.js
│       │   └── MarketAnalysisPage.js
│       │
│       ├── services/             # API calls and backend integration
│       │   └── api.js
│       │
│       ├── hooks/                # Custom React hooks
│       │   └── usePortfolio.js
│       │
│       ├── context/              # Context API or global state
│       │   └── PortfolioContext.js
│       │
│       ├── styles/               # CSS / Tailwind config
│       │   └── index.css
│       │
│       ├── App.js                # Main layout and routing
│       └── index.js              # Entry point
│
└── Backend
    ├── app/
    │   ├── main.py               # FastAPI app entry point
    │   ├── models/               # Database models
    │   │   └── stock.py
    │   ├── routes/               # API endpoints
    │   │   ├── portfolio.py
    │   │   ├── market.py
    │   │   └── stocks.py
    │   ├── services/             # Business logic / calculations
    │   │   └── portfolio_service.py
    │   ├── database.py           # DB connection & session
    │   └── config.py             # Config variables (DB URL, API keys)
    │
    └── requirements.txt          # Python dependencies
