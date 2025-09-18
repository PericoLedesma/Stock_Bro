"""
Stock price prediction using machine learning models.
"""

import numpy as np
import pandas as pd
from typing import Tuple, Optional, Dict, Any
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.preprocessing import StandardScaler
from loguru import logger


class StockPredictor:
    """Machine learning-based stock price predictor."""
    
    def __init__(self):
        self.logger = logger
        self.model = None
        self.scaler = StandardScaler()
        self.feature_columns = []
    
    def prepare_features(self, data: pd.DataFrame, lookback_days: int = 30) -> Tuple[np.ndarray, np.ndarray]:
        """
        Prepare features and targets for training.
        
        Args:
            data: Stock data DataFrame
            lookback_days: Number of days to look back for features
            
        Returns:
            Tuple of (features, targets)
        """
        features = []
        targets = []
        
        # Calculate technical indicators as features
        data['sma_5'] = data['Close'].rolling(5).mean()
        data['sma_10'] = data['Close'].rolling(10).mean()
        data['sma_20'] = data['Close'].rolling(20).mean()
        data['ema_12'] = data['Close'].ewm(span=12).mean()
        data['ema_26'] = data['Close'].ewm(span=26).mean()
        
        # RSI
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rs = gain / loss
        data['rsi'] = 100 - (100 / (1 + rs))
        
        # Volume indicators
        data['volume_sma'] = data['Volume'].rolling(20).mean()
        data['volume_ratio'] = data['Volume'] / data['volume_sma']
        
        # Price momentum
        data['price_change'] = data['Close'].pct_change()
        data['volatility'] = data['Close'].rolling(20).std()
        
        self.feature_columns = [
            'sma_5', 'sma_10', 'sma_20', 'ema_12', 'ema_26',
            'rsi', 'volume_ratio', 'price_change', 'volatility'
        ]
        
        # Create sequences
        for i in range(lookback_days, len(data) - 1):
            # Features: technical indicators for the past lookback_days
            feature_row = []
            for col in self.feature_columns:
                if col in data.columns:
                    values = data[col].iloc[i-lookback_days:i].values
                    feature_row.extend([
                        np.mean(values),
                        np.std(values),
                        values[-1]  # Latest value
                    ])
            
            features.append(feature_row)
            
            # Target: next day's price change
            current_price = data['Close'].iloc[i]
            next_price = data['Close'].iloc[i + 1]
            price_change = (next_price - current_price) / current_price
            targets.append(price_change)
        
        return np.array(features), np.array(targets)
    
    def train(self, data: pd.DataFrame, test_size: float = 0.2) -> Dict[str, float]:
        """
        Train the prediction model.
        
        Args:
            data: Stock data DataFrame
            test_size: Fraction of data to use for testing
            
        Returns:
            Dictionary with training metrics
        """
        self.logger.info("Preparing features for training...")
        X, y = self.prepare_features(data)
        
        if len(X) < 50:
            raise ValueError("Not enough data for training. Need at least 50 samples.")
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, shuffle=False
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train model
        self.logger.info("Training Random Forest model...")
        self.model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        )
        
        self.model.fit(X_train_scaled, y_train)
        
        # Evaluate
        train_pred = self.model.predict(X_train_scaled)
        test_pred = self.model.predict(X_test_scaled)
        
        metrics = {
            'train_mse': mean_squared_error(y_train, train_pred),
            'test_mse': mean_squared_error(y_test, test_pred),
            'train_mae': mean_absolute_error(y_train, train_pred),
            'test_mae': mean_absolute_error(y_test, test_pred),
            'train_samples': len(X_train),
            'test_samples': len(X_test)
        }
        
        self.logger.info(f"Training completed. Test MAE: {metrics['test_mae']:.4f}")
        return metrics
    
    def predict(self, data: pd.DataFrame, days_ahead: int = 1) -> Dict[str, Any]:
        """
        Make price predictions.
        
        Args:
            data: Recent stock data
            days_ahead: Number of days to predict ahead
            
        Returns:
            Dictionary with predictions and confidence
        """
        if self.model is None:
            raise ValueError("Model not trained. Call train() first.")
        
        # Prepare features for latest data
        X, _ = self.prepare_features(data)
        
        if len(X) == 0:
            raise ValueError("Not enough data for prediction.")
        
        # Use the most recent features
        latest_features = X[-1:].reshape(1, -1)
        latest_features_scaled = self.scaler.transform(latest_features)
        
        # Make prediction
        prediction = self.model.predict(latest_features_scaled)[0]
        
        # Calculate confidence based on model's feature importance
        feature_importance = self.model.feature_importances_
        confidence = np.mean(feature_importance) * 100
        
        current_price = data['Close'].iloc[-1]
        predicted_price = current_price * (1 + prediction)
        
        return {
            'current_price': current_price,
            'predicted_change_pct': prediction * 100,
            'predicted_price': predicted_price,
            'confidence': min(confidence, 95),  # Cap at 95%
            'direction': 'up' if prediction > 0 else 'down'
        }
    
    def get_feature_importance(self) -> Optional[Dict[str, float]]:
        """Get feature importance from trained model."""
        if self.model is None:
            return None
        
        # Create feature names (3 values per technical indicator)
        feature_names = []
        for col in self.feature_columns:
            feature_names.extend([f"{col}_mean", f"{col}_std", f"{col}_current"])
        
        importance_dict = {}
        for name, importance in zip(feature_names, self.model.feature_importances_):
            importance_dict[name] = importance
        
        return dict(sorted(importance_dict.items(), key=lambda x: x[1], reverse=True))