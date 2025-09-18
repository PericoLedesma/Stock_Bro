# Stock Bro Documentation

## Overview

Stock Bro is an AI-powered investment guidance application that provides real-time insights, trend analysis, and personalized investment advice.

## Features

- **Real-time Stock Data**: Fetch current and historical stock prices
- **Technical Analysis**: Calculate various technical indicators (SMA, EMA, RSI, MACD, Bollinger Bands)
- **AI Predictions**: Machine learning-based price predictions
- **REST API**: Comprehensive API for integration
- **Support/Resistance**: Automatic detection of key price levels
- **Trend Analysis**: Identify market trends and strength

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/PericoLedesma/Stock_Bro.git
cd Stock_Bro

# Install dependencies
pip install -e .

# Copy environment configuration
cp .env.example .env

# Edit .env file with your API keys
```

### Running the Application

```bash
# Start the development server
python -m stock_bro.main

# Or use the installed command
stock-bro
```

The API will be available at `http://localhost:8000` with documentation at `http://localhost:8000/docs`.

### API Examples

#### Get Stock Data
```bash
curl "http://localhost:8000/api/v1/stocks/AAPL?period=1y&interval=1d"
```

#### Get Technical Analysis
```bash
curl "http://localhost:8000/api/v1/stocks/AAPL/analysis"
```

#### Get Price Prediction
```bash
curl -X POST "http://localhost:8000/api/v1/stocks/predict" \
     -H "Content-Type: application/json" \
     -d '{"symbol": "AAPL", "days_ahead": 1}'
```

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/stock_bro --cov-report=html

# Run specific test file
pytest tests/unit/test_data_fetcher.py
```

## Development

### Code Style
- Use Black for formatting: `black src/ tests/`
- Use Flake8 for linting: `flake8 src/ tests/`

### Adding New Features
1. Create feature branch
2. Add tests
3. Implement feature
4. Update documentation
5. Submit pull request

## Configuration

See `.env.example` for all available configuration options.

## License

MIT License