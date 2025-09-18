"""
API routes for stock operations.
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List, Dict, Any
from pydantic import BaseModel

from stock_bro.data.fetcher import StockDataFetcher
from stock_bro.analysis.technical import TechnicalAnalyzer
from stock_bro.ai.predictor import StockPredictor

stock_router = APIRouter()

# Initialize services
data_fetcher = StockDataFetcher()
tech_analyzer = TechnicalAnalyzer()
predictor = StockPredictor()


class StockRequest(BaseModel):
    """Stock request model."""
    symbol: str
    period: str = "1y"
    interval: str = "1d"


class PredictionRequest(BaseModel):
    """Prediction request model."""
    symbol: str
    days_ahead: int = 1


@stock_router.get("/stocks/{symbol}")
async def get_stock_data(
    symbol: str,
    period: str = Query("1y", description="Data period"),
    interval: str = Query("1d", description="Data interval")
):
    """Get stock data for a symbol."""
    try:
        data = data_fetcher.get_stock_data(symbol.upper(), period, interval)
        
        if data is None:
            raise HTTPException(status_code=404, detail=f"No data found for symbol {symbol}")
        
        # Convert to JSON-serializable format
        result = {
            "symbol": symbol.upper(),
            "period": period,
            "interval": interval,
            "data_points": len(data),
            "latest_price": float(data['Close'].iloc[-1]),
            "latest_volume": int(data['Volume'].iloc[-1]),
            "data": [
                {
                    "date": str(date),
                    "open": float(row['Open']),
                    "high": float(row['High']),
                    "low": float(row['Low']),
                    "close": float(row['Close']),
                    "volume": int(row['Volume'])
                }
                for date, row in data.tail(100).iterrows()  # Limit to last 100 points for API response
            ]
        }
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@stock_router.get("/stocks/{symbol}/info")
async def get_stock_info(symbol: str):
    """Get basic information about a stock."""
    try:
        info = data_fetcher.get_stock_info(symbol.upper())
        
        if info is None:
            raise HTTPException(status_code=404, detail=f"No info found for symbol {symbol}")
        
        # Extract key information
        result = {
            "symbol": symbol.upper(),
            "company_name": info.get("longName", "N/A"),
            "sector": info.get("sector", "N/A"),
            "industry": info.get("industry", "N/A"),
            "market_cap": info.get("marketCap", 0),
            "pe_ratio": info.get("trailingPE", 0),
            "dividend_yield": info.get("dividendYield", 0),
            "52_week_high": info.get("fiftyTwoWeekHigh", 0),
            "52_week_low": info.get("fiftyTwoWeekLow", 0),
            "description": info.get("longBusinessSummary", "N/A")[:500] + "..." if info.get("longBusinessSummary", "") else "N/A"
        }
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@stock_router.get("/stocks/{symbol}/analysis")
async def get_technical_analysis(symbol: str, period: str = Query("1y", description="Data period")):
    """Get technical analysis for a stock."""
    try:
        data = data_fetcher.get_stock_data(symbol.upper(), period)
        
        if data is None:
            raise HTTPException(status_code=404, detail=f"No data found for symbol {symbol}")
        
        # Calculate technical indicators
        sma_20 = tech_analyzer.calculate_sma(data, 20)
        ema_12 = tech_analyzer.calculate_ema(data, 12)
        rsi = tech_analyzer.calculate_rsi(data)
        macd = tech_analyzer.calculate_macd(data)
        bollinger = tech_analyzer.calculate_bollinger_bands(data)
        support_resistance = tech_analyzer.get_support_resistance_levels(data)
        trend_analysis = tech_analyzer.analyze_trend(data)
        
        result = {
            "symbol": symbol.upper(),
            "analysis_date": str(data.index[-1].date()),
            "current_price": float(data['Close'].iloc[-1]),
            "sma_20": float(sma_20.iloc[-1]) if not sma_20.isna().iloc[-1] else None,
            "ema_12": float(ema_12.iloc[-1]) if not ema_12.isna().iloc[-1] else None,
            "rsi": float(rsi.iloc[-1]) if not rsi.isna().iloc[-1] else None,
            "macd": {
                "macd": float(macd['macd'].iloc[-1]) if not macd['macd'].isna().iloc[-1] else None,
                "signal": float(macd['signal'].iloc[-1]) if not macd['signal'].isna().iloc[-1] else None,
                "histogram": float(macd['histogram'].iloc[-1]) if not macd['histogram'].isna().iloc[-1] else None
            },
            "bollinger_bands": {
                "upper": float(bollinger['upper'].iloc[-1]) if not bollinger['upper'].isna().iloc[-1] else None,
                "middle": float(bollinger['middle'].iloc[-1]) if not bollinger['middle'].isna().iloc[-1] else None,
                "lower": float(bollinger['lower'].iloc[-1]) if not bollinger['lower'].isna().iloc[-1] else None
            },
            "support_resistance": support_resistance,
            "trend_analysis": trend_analysis
        }
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@stock_router.post("/stocks/predict")
async def predict_stock_price(request: PredictionRequest):
    """Predict future stock price."""
    try:
        # Get historical data for training
        data = data_fetcher.get_stock_data(request.symbol.upper(), "2y", "1d")
        
        if data is None or len(data) < 100:
            raise HTTPException(
                status_code=400, 
                detail=f"Insufficient data for prediction. Need at least 100 data points, got {len(data) if data is not None else 0}"
            )
        
        # Train model
        training_metrics = predictor.train(data)
        
        # Make prediction
        prediction = predictor.predict(data, request.days_ahead)
        
        result = {
            "symbol": request.symbol.upper(),
            "prediction": prediction,
            "training_metrics": training_metrics,
            "disclaimer": "This is a prediction based on historical data and should not be considered as financial advice."
        }
        
        return result
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@stock_router.get("/stocks/batch/{symbols}")
async def get_multiple_stocks(symbols: str, period: str = Query("1y", description="Data period")):
    """Get data for multiple stocks."""
    try:
        symbol_list = [s.strip().upper() for s in symbols.split(",")]
        
        if len(symbol_list) > 10:
            raise HTTPException(status_code=400, detail="Maximum 10 symbols allowed")
        
        results = {}
        for symbol in symbol_list:
            data = data_fetcher.get_stock_data(symbol, period)
            if data is not None:
                results[symbol] = {
                    "latest_price": float(data['Close'].iloc[-1]),
                    "price_change": float((data['Close'].iloc[-1] - data['Close'].iloc[-2]) / data['Close'].iloc[-2] * 100),
                    "volume": int(data['Volume'].iloc[-1])
                }
            else:
                results[symbol] = {"error": "No data available"}
        
        return {"symbols": results}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))