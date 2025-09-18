"""Test configuration and fixtures."""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


@pytest.fixture
def sample_stock_data():
    """Create sample stock data for testing."""
    dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
    np.random.seed(42)
    
    # Generate realistic stock data
    base_price = 100
    prices = [base_price]
    volumes = []
    
    for i in range(1, len(dates)):
        # Random walk with slight upward bias
        change = np.random.normal(0.001, 0.02)
        new_price = prices[-1] * (1 + change)
        prices.append(max(new_price, 1))  # Ensure positive prices
        
        # Volume correlated with price changes
        volume = int(np.random.normal(1000000, 200000))
        volumes.append(max(volume, 100000))
    
    volumes.append(volumes[-1])  # Add one more for the last date
    
    data = pd.DataFrame({
        'Open': [p * np.random.uniform(0.98, 1.02) for p in prices],
        'High': [p * np.random.uniform(1.00, 1.05) for p in prices],
        'Low': [p * np.random.uniform(0.95, 1.00) for p in prices],
        'Close': prices,
        'Volume': volumes
    }, index=dates)
    
    return data