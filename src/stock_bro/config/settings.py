"""
Application settings and configuration.
"""

import os
from typing import Optional
from pydantic import BaseModel


class Settings(BaseModel):
    """Application settings."""
    
    # Application settings
    app_name: str = "Stock Bro"
    version: str = "0.1.0"
    debug: bool = False
    
    # Server settings
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Logging
    log_level: str = "INFO"
    log_file: Optional[str] = None
    
    # API Keys (loaded from environment)
    alpha_vantage_api_key: Optional[str] = None
    finnhub_api_key: Optional[str] = None
    
    # Database
    database_url: str = "sqlite:///./stock_bro.db"
    
    # Data settings
    data_cache_dir: str = "./data/cache"
    data_retention_days: int = 30
    
    # AI/ML settings
    model_cache_dir: str = "./models"
    prediction_horizon_days: int = 30
    
    def __init__(self, **kwargs):
        """Initialize settings with environment variables."""
        # Load from environment with prefix
        env_vars = {}
        prefix = "STOCK_BRO_"
        
        for key, value in os.environ.items():
            if key.startswith(prefix):
                setting_name = key[len(prefix):].lower()
                env_vars[setting_name] = value
        
        # Override with any provided kwargs
        env_vars.update(kwargs)
        
        super().__init__(**env_vars)


# Global settings instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Get application settings."""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings