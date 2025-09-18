# Stock_Bro 📈

A smart AI that guides your investments with real-time insights, trend analysis, and personalized advice.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.85.0+-green.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🚀 Features

- **📊 Real-time Stock Data**: Fetch current and historical stock prices using yfinance
- **🔍 Technical Analysis**: Calculate SMA, EMA, RSI, MACD, Bollinger Bands, and more
- **🤖 AI Predictions**: Machine learning-based price predictions using Random Forest
- **🌐 REST API**: Comprehensive FastAPI-based REST API
- **📈 Trend Analysis**: Identify market trends and momentum
- **🎯 Support/Resistance**: Automatic detection of key price levels
- **📱 Easy Integration**: Simple Python package with clear API

## 🏗️ Project Structure

```
Stock_Bro/
├── src/stock_bro/           # Main application code
│   ├── api/                 # FastAPI routes and server
│   ├── data/                # Data fetching and management
│   ├── analysis/            # Technical analysis tools
│   ├── ai/                  # Machine learning models
│   ├── config/              # Configuration management
│   └── utils/               # Utility functions
├── tests/                   # Test suite
│   ├── unit/                # Unit tests
│   └── integration/         # Integration tests
├── docs/                    # Documentation
├── config/                  # Configuration files
├── data/                    # Data storage
│   ├── samples/             # Sample data
│   └── cache/               # Cached data
├── scripts/                 # Utility scripts
└── models/                  # ML model storage
```

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Quick Start

```bash
# Clone the repository
git clone https://github.com/PericoLedesma/Stock_Bro.git
cd Stock_Bro

# Install the package
pip install -e .

# Set up development environment (optional)
python scripts/setup_dev.py

# Copy environment configuration
cp .env.example .env
# Edit .env with your API keys (optional for basic functionality)

# Run the application
python -m stock_bro.main
```

The API will be available at `http://localhost:8000` with interactive documentation at `http://localhost:8000/docs`.

## 📖 Quick Usage Examples

### Python API

```python
from stock_bro.data.fetcher import StockDataFetcher
from stock_bro.analysis.technical import TechnicalAnalyzer
from stock_bro.ai.predictor import StockPredictor

# Fetch stock data
fetcher = StockDataFetcher()
data = fetcher.get_stock_data("AAPL", period="1y")

# Perform technical analysis
analyzer = TechnicalAnalyzer()
sma = analyzer.calculate_sma(data, window=20)
rsi = analyzer.calculate_rsi(data)
trend = analyzer.analyze_trend(data)

# Make AI predictions
predictor = StockPredictor()
predictor.train(data)
prediction = predictor.predict(data)
```

### REST API

```bash
# Get stock data
curl "http://localhost:8000/api/v1/stocks/AAPL?period=1y"

# Get technical analysis
curl "http://localhost:8000/api/v1/stocks/AAPL/analysis"

# Get AI prediction
curl -X POST "http://localhost:8000/api/v1/stocks/predict" \
     -H "Content-Type: application/json" \
     -d '{"symbol": "AAPL", "days_ahead": 1}'

# Get multiple stocks
curl "http://localhost:8000/api/v1/stocks/batch/AAPL,GOOGL,MSFT"
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=src/stock_bro --cov-report=html

# Run specific test categories
pytest tests/unit/
pytest tests/integration/

# Quick functionality test
python scripts/test_basic.py
```

## 🔧 Configuration

The application uses environment variables for configuration. Copy `.env.example` to `.env` and customize:

```env
# API Keys (optional, enhances functionality)
STOCK_BRO_ALPHA_VANTAGE_API_KEY=your_key_here
STOCK_BRO_FINNHUB_API_KEY=your_key_here

# Server settings
STOCK_BRO_HOST=0.0.0.0
STOCK_BRO_PORT=8000
STOCK_BRO_DEBUG=false

# Data settings
STOCK_BRO_DATA_CACHE_DIR=./data/cache
STOCK_BRO_DATABASE_URL=sqlite:///./data/stock_bro.db
```

## 📚 API Documentation

Once the server is running, visit:
- **Interactive API Docs**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **Health Check**: `http://localhost:8000/health`

### Main Endpoints

- `GET /api/v1/stocks/{symbol}` - Get stock data
- `GET /api/v1/stocks/{symbol}/info` - Get company information
- `GET /api/v1/stocks/{symbol}/analysis` - Get technical analysis
- `POST /api/v1/stocks/predict` - Get AI price prediction
- `GET /api/v1/stocks/batch/{symbols}` - Get multiple stocks data

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and add tests
4. Run tests: `pytest`
5. Format code: `black src/ tests/`
6. Lint code: `flake8 src/ tests/`
7. Commit changes: `git commit -am 'Add feature'`
8. Push to branch: `git push origin feature-name`
9. Submit a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This application is for educational and research purposes only. The predictions and analysis provided should not be considered as financial advice. Always consult with qualified financial advisors before making investment decisions.

## 🔗 Useful Resources

- [Getting Alpha Vantage API Key](https://www.alphavantage.co/support/#api-key)
- [Getting Finnhub API Key](https://finnhub.io/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [yfinance Documentation](https://pypi.org/project/yfinance/)

## 📞 Support

If you have any questions or run into issues, please [open an issue](https://github.com/PericoLedesma/Stock_Bro/issues) on GitHub.
