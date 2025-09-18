#!/usr/bin/env python3
"""
Setup script for Stock Bro development environment.
"""

import os
import sys
from pathlib import Path


def create_directories():
    """Create necessary directories."""
    directories = [
        "logs",
        "data/cache",
        "models",
        "temp"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"Created directory: {directory}")


def setup_environment():
    """Setup environment file."""
    env_example = Path(".env.example")
    env_file = Path(".env")
    
    if env_example.exists() and not env_file.exists():
        env_file.write_text(env_example.read_text())
        print("Created .env file from .env.example")
        print("Please edit .env file with your API keys")
    elif env_file.exists():
        print(".env file already exists")
    else:
        print("Warning: .env.example file not found")


def install_dependencies():
    """Install development dependencies."""
    try:
        import subprocess
        print("Installing development dependencies...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-e", ".[dev]"], check=True)
        print("Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")


def main():
    """Main setup function."""
    print("Setting up Stock Bro development environment...")
    
    # Change to script directory
    os.chdir(Path(__file__).parent.parent)
    
    create_directories()
    setup_environment()
    
    # Ask user if they want to install dependencies
    response = input("Install development dependencies? (y/n): ").lower().strip()
    if response in ['y', 'yes']:
        install_dependencies()
    
    print("\nSetup complete!")
    print("Next steps:")
    print("1. Edit .env file with your API keys")
    print("2. Run 'python -m stock_bro.main' to start the application")
    print("3. Visit http://localhost:8000/docs for API documentation")


if __name__ == "__main__":
    main()