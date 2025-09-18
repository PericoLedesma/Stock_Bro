"""
Main application entry point for Stock Bro.
"""

import asyncio
import logging
from typing import Optional

from stock_bro.config.settings import get_settings
from stock_bro.api.server import create_app
from stock_bro.utils.logger import setup_logging


class StockBroApp:
    """Main application class for Stock Bro."""
    
    def __init__(self):
        self.settings = get_settings()
        self.logger = setup_logging()
        self.app = None
    
    async def initialize(self):
        """Initialize the application."""
        self.logger.info("Initializing Stock Bro application...")
        self.app = create_app()
        self.logger.info("Stock Bro application initialized successfully!")
    
    async def run(self):
        """Run the application."""
        if not self.app:
            await self.initialize()
        
        import uvicorn
        self.logger.info(f"Starting Stock Bro server on {self.settings.host}:{self.settings.port}")
        
        config = uvicorn.Config(
            self.app,
            host=self.settings.host,
            port=self.settings.port,
            log_level=self.settings.log_level.lower()
        )
        server = uvicorn.Server(config)
        await server.serve()


def main():
    """Main entry point."""
    app = StockBroApp()
    asyncio.run(app.run())


if __name__ == "__main__":
    main()