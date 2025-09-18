"""Tests for technical analysis functionality."""

import pytest
import pandas as pd
import numpy as np
from stock_bro.analysis.technical import TechnicalAnalyzer


class TestTechnicalAnalyzer:
    """Test cases for TechnicalAnalyzer."""
    
    def setup_method(self):
        """Setup for each test."""
        self.analyzer = TechnicalAnalyzer()
    
    def test_init(self):
        """Test analyzer initialization."""
        assert self.analyzer is not None
        assert hasattr(self.analyzer, 'logger')
    
    def test_calculate_sma(self, sample_stock_data):
        """Test Simple Moving Average calculation."""
        sma = self.analyzer.calculate_sma(sample_stock_data, window=20)
        
        assert isinstance(sma, pd.Series)
        assert len(sma) == len(sample_stock_data)
        # First 19 values should be NaN
        assert sma.iloc[:19].isna().all()
        # Values after window should not be NaN
        assert not sma.iloc[19:].isna().any()
    
    def test_calculate_ema(self, sample_stock_data):
        """Test Exponential Moving Average calculation."""
        ema = self.analyzer.calculate_ema(sample_stock_data, window=20)
        
        assert isinstance(ema, pd.Series)
        assert len(ema) == len(sample_stock_data)
        # EMA should not have NaN values (except possibly the first)
        assert not ema.iloc[1:].isna().any()
    
    def test_calculate_rsi(self, sample_stock_data):
        """Test RSI calculation."""
        rsi = self.analyzer.calculate_rsi(sample_stock_data, window=14)
        
        assert isinstance(rsi, pd.Series)
        assert len(rsi) == len(sample_stock_data)
        # RSI should be between 0 and 100
        valid_rsi = rsi.dropna()
        assert (valid_rsi >= 0).all()
        assert (valid_rsi <= 100).all()
    
    def test_calculate_macd(self, sample_stock_data):
        """Test MACD calculation."""
        macd_result = self.analyzer.calculate_macd(sample_stock_data)
        
        assert isinstance(macd_result, dict)
        assert 'macd' in macd_result
        assert 'signal' in macd_result
        assert 'histogram' in macd_result
        
        for key, series in macd_result.items():
            assert isinstance(series, pd.Series)
            assert len(series) == len(sample_stock_data)
    
    def test_calculate_bollinger_bands(self, sample_stock_data):
        """Test Bollinger Bands calculation."""
        bands = self.analyzer.calculate_bollinger_bands(sample_stock_data)
        
        assert isinstance(bands, dict)
        assert 'upper' in bands
        assert 'middle' in bands
        assert 'lower' in bands
        
        # Upper band should be above middle, middle above lower
        valid_data = sample_stock_data.iloc[20:]  # Skip first 20 for window
        upper = bands['upper'].iloc[20:]
        middle = bands['middle'].iloc[20:]
        lower = bands['lower'].iloc[20:]
        
        assert (upper >= middle).all()
        assert (middle >= lower).all()
    
    def test_get_support_resistance_levels(self, sample_stock_data):
        """Test support and resistance level detection."""
        levels = self.analyzer.get_support_resistance_levels(sample_stock_data)
        
        assert isinstance(levels, dict)
        assert 'support' in levels
        assert 'resistance' in levels
        assert 'current_price' in levels
        
        # Support should be below current price, resistance above
        assert levels['support'] < levels['current_price']
        assert levels['resistance'] > levels['current_price']
    
    def test_analyze_trend(self, sample_stock_data):
        """Test trend analysis."""
        trend = self.analyzer.analyze_trend(sample_stock_data)
        
        assert isinstance(trend, dict)
        assert 'trend' in trend
        assert 'strength' in trend
        assert 'price_change_pct' in trend
        assert 'sma_short' in trend
        assert 'sma_long' in trend
        
        # Trend should be one of the expected values
        assert trend['trend'] in ['bullish', 'bearish', 'neutral']
        
        # Strength should be non-negative
        assert trend['strength'] >= 0