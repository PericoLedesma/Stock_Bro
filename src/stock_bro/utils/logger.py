"""
Logging configuration and utilities.
"""

import sys
from loguru import logger
from stock_bro.config.settings import get_settings


def setup_logging():
    """Setup application logging."""
    settings = get_settings()
    
    # Remove default logger
    logger.remove()
    
    # Console logging
    logger.add(
        sys.stderr,
        level=settings.log_level,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
               "<level>{level: <8}</level> | "
               "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
               "<level>{message}</level>",
        colorize=True
    )
    
    # File logging (if configured)
    if settings.log_file:
        logger.add(
            settings.log_file,
            level=settings.log_level,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
            rotation="10 MB",
            retention="30 days",
            compression="gz"
        )
    
    return logger