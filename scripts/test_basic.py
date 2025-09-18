#!/usr/bin/env python3
"""
Quick test script to verify Stock Bro functionality.
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from stock_bro.data.fetcher import StockDataFetcher
from stock_bro.analysis.technical import TechnicalAnalyzer


async def test_basic_functionality():
    """Test basic functionality without API keys."""
    print("Testing Stock Bro basic functionality...")
    
    # Test data fetcher
    print("\n1. Testing data fetcher...")
    fetcher = StockDataFetcher()
    
    # Try to fetch data for a common stock
    try:
        data = fetcher.get_stock_data("AAPL", "1mo", "1d")
        if data is not None:
            print(f"✓ Successfully fetched {len(data)} data points for AAPL")
            print(f"  Latest price: ${data['Close'].iloc[-1]:.2f}")
        else:
            print("✗ No data returned (this may be expected without API keys)")
    except Exception as e:
        print(f"✗ Error fetching data: {e}")
    
    # Test technical analyzer
    print("\n2. Testing technical analyzer...")
    if data is not None and len(data) > 20:
        analyzer = TechnicalAnalyzer()
        
        try:
            sma = analyzer.calculate_sma(data, 20)
            rsi = analyzer.calculate_rsi(data)
            trend = analyzer.analyze_trend(data)
            
            print(f"✓ SMA(20): ${sma.iloc[-1]:.2f}")
            print(f"✓ RSI: {rsi.iloc[-1]:.2f}")
            print(f"✓ Trend: {trend['trend']} (strength: {trend['strength']:.3f})")
        except Exception as e:
            print(f"✗ Error in technical analysis: {e}")
    else:
        print("⚠ Skipping technical analysis (insufficient data)")
    
    print("\n3. Testing configuration...")
    try:
        from stock_bro.config.settings import get_settings
        settings = get_settings()
        print(f"✓ App name: {settings.app_name}")
        print(f"✓ Version: {settings.version}")
        print(f"✓ Host: {settings.host}:{settings.port}")
    except Exception as e:
        print(f"✗ Error loading settings: {e}")
    
    print("\nBasic functionality test complete!")


if __name__ == "__main__":
    asyncio.run(test_basic_functionality())