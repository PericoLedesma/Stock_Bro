"""
Technical indicators and market analysis tools.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, Optional
from loguru import logger


class TechnicalAnalyzer:
    """Provides technical analysis indicators and tools."""
    
    def __init__(self):
        self.logger = logger
    
    def calculate_sma(self, data: pd.DataFrame, window: int = 20, column: str = 'Close') -> pd.Series:
        """
        Calculate Simple Moving Average.
        
        Args:
            data: Stock data DataFrame
            window: Moving average window
            column: Column to calculate SMA for
            
        Returns:
            Series with SMA values
        """
        return data[column].rolling(window=window).mean()
    
    def calculate_ema(self, data: pd.DataFrame, window: int = 20, column: str = 'Close') -> pd.Series:
        """
        Calculate Exponential Moving Average.
        
        Args:
            data: Stock data DataFrame
            window: Moving average window
            column: Column to calculate EMA for
            
        Returns:
            Series with EMA values
        """
        return data[column].ewm(span=window).mean()
    
    def calculate_rsi(self, data: pd.DataFrame, window: int = 14, column: str = 'Close') -> pd.Series:
        """
        Calculate Relative Strength Index.
        
        Args:
            data: Stock data DataFrame
            window: RSI window
            column: Column to calculate RSI for
            
        Returns:
            Series with RSI values
        """
        delta = data[column].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
    
    def calculate_macd(
        self, 
        data: pd.DataFrame, 
        fast: int = 12, 
        slow: int = 26, 
        signal: int = 9,
        column: str = 'Close'
    ) -> Dict[str, pd.Series]:
        """
        Calculate MACD (Moving Average Convergence Divergence).
        
        Args:
            data: Stock data DataFrame
            fast: Fast EMA period
            slow: Slow EMA period
            signal: Signal line EMA period
            column: Column to calculate MACD for
            
        Returns:
            Dictionary with MACD, signal, and histogram
        """
        ema_fast = data[column].ewm(span=fast).mean()
        ema_slow = data[column].ewm(span=slow).mean()
        
        macd = ema_fast - ema_slow
        signal_line = macd.ewm(span=signal).mean()
        histogram = macd - signal_line
        
        return {
            'macd': macd,
            'signal': signal_line,
            'histogram': histogram
        }
    
    def calculate_bollinger_bands(
        self, 
        data: pd.DataFrame, 
        window: int = 20, 
        num_std: float = 2,
        column: str = 'Close'
    ) -> Dict[str, pd.Series]:
        """
        Calculate Bollinger Bands.
        
        Args:
            data: Stock data DataFrame
            window: Moving average window
            num_std: Number of standard deviations
            column: Column to calculate bands for
            
        Returns:
            Dictionary with upper, middle, and lower bands
        """
        sma = self.calculate_sma(data, window, column)
        std = data[column].rolling(window=window).std()
        
        upper_band = sma + (std * num_std)
        lower_band = sma - (std * num_std)
        
        return {
            'upper': upper_band,
            'middle': sma,
            'lower': lower_band
        }
    
    def get_support_resistance_levels(
        self, 
        data: pd.DataFrame, 
        window: int = 20
    ) -> Dict[str, float]:
        """
        Identify support and resistance levels.
        
        Args:
            data: Stock data DataFrame
            window: Window for local extrema detection
            
        Returns:
            Dictionary with support and resistance levels
        """
        highs = data['High'].rolling(window=window, center=True).max()
        lows = data['Low'].rolling(window=window, center=True).min()
        
        resistance_levels = data[data['High'] == highs]['High'].unique()
        support_levels = data[data['Low'] == lows]['Low'].unique()
        
        # Get most recent levels
        current_price = data['Close'].iloc[-1]
        
        resistance = min([r for r in resistance_levels if r > current_price], default=current_price * 1.1)
        support = max([s for s in support_levels if s < current_price], default=current_price * 0.9)
        
        return {
            'support': support,
            'resistance': resistance,
            'current_price': current_price
        }
    
    def analyze_trend(self, data: pd.DataFrame, window: int = 20) -> Dict[str, Any]:
        """
        Analyze overall trend direction.
        
        Args:
            data: Stock data DataFrame
            window: Window for trend analysis
            
        Returns:
            Dictionary with trend analysis
        """
        sma_short = self.calculate_sma(data, window // 2)
        sma_long = self.calculate_sma(data, window)
        
        current_short = sma_short.iloc[-1]
        current_long = sma_long.iloc[-1]
        
        if current_short > current_long:
            trend = "bullish"
        elif current_short < current_long:
            trend = "bearish"
        else:
            trend = "neutral"
        
        # Calculate trend strength
        price_change = (data['Close'].iloc[-1] - data['Close'].iloc[-window]) / data['Close'].iloc[-window]
        
        return {
            'trend': trend,
            'strength': abs(price_change),
            'price_change_pct': price_change * 100,
            'sma_short': current_short,
            'sma_long': current_long
        }