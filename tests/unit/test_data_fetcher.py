"""Tests for data fetching functionality."""

import pytest
from unittest.mock import Mock, patch
import pandas as pd
from stock_bro.data.fetcher import StockDataFetcher


class TestStockDataFetcher:
    """Test cases for StockDataFetcher."""
    
    def setup_method(self):
        """Setup for each test."""
        self.fetcher = StockDataFetcher()
    
    def test_init(self):
        """Test fetcher initialization."""
        assert self.fetcher is not None
        assert hasattr(self.fetcher, 'logger')
    
    @patch('stock_bro.data.fetcher.yf.Ticker')
    def test_get_stock_data_success(self, mock_ticker, sample_stock_data):
        """Test successful stock data fetching."""
        # Mock yfinance ticker
        mock_ticker_instance = Mock()
        mock_ticker_instance.history.return_value = sample_stock_data
        mock_ticker.return_value = mock_ticker_instance
        
        result = self.fetcher.get_stock_data("AAPL", "1y", "1d")
        
        assert result is not None
        assert isinstance(result, pd.DataFrame)
        assert len(result) > 0
        mock_ticker.assert_called_once_with("AAPL")
        mock_ticker_instance.history.assert_called_once_with(period="1y", interval="1d")
    
    @patch('stock_bro.data.fetcher.yf.Ticker')
    def test_get_stock_data_empty_response(self, mock_ticker):
        """Test handling of empty data response."""
        # Mock empty dataframe
        mock_ticker_instance = Mock()
        mock_ticker_instance.history.return_value = pd.DataFrame()
        mock_ticker.return_value = mock_ticker_instance
        
        result = self.fetcher.get_stock_data("INVALID", "1y", "1d")
        
        assert result is None
    
    @patch('stock_bro.data.fetcher.yf.Ticker')
    def test_get_stock_data_exception(self, mock_ticker):
        """Test handling of exceptions during data fetching."""
        # Mock exception
        mock_ticker.side_effect = Exception("API Error")
        
        result = self.fetcher.get_stock_data("AAPL", "1y", "1d")
        
        assert result is None
    
    @patch('stock_bro.data.fetcher.yf.Ticker')
    def test_get_stock_info_success(self, mock_ticker):
        """Test successful stock info fetching."""
        # Mock stock info
        mock_info = {
            "longName": "Apple Inc.",
            "sector": "Technology",
            "marketCap": 2000000000000
        }
        mock_ticker_instance = Mock()
        mock_ticker_instance.info = mock_info
        mock_ticker.return_value = mock_ticker_instance
        
        result = self.fetcher.get_stock_info("AAPL")
        
        assert result is not None
        assert result == mock_info
        mock_ticker.assert_called_once_with("AAPL")
    
    def test_get_multiple_stocks(self, sample_stock_data):
        """Test fetching data for multiple stocks."""
        with patch.object(self.fetcher, 'get_stock_data') as mock_get_data:
            mock_get_data.return_value = sample_stock_data
            
            symbols = ["AAPL", "GOOGL", "MSFT"]
            results = self.fetcher.get_multiple_stocks(symbols, "1y", "1d")
            
            assert len(results) == 3
            assert all(symbol in results for symbol in symbols)
            assert mock_get_data.call_count == 3