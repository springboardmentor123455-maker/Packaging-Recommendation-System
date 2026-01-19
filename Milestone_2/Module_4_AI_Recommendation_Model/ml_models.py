import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import joblib
import os

class BasePredictor:
    def __init__(self, model_name):
        self.model = None
        self.model_name = model_name

    def train(self, X_train, y_train):
        print(f"Training {self.model_name}...")
        self.model.fit(X_train, y_train)
        print("Training complete.")

    def evaluate(self, X_test, y_test):
        if not self.model:
            raise Exception("Model not trained yet.")
        
        predictions = self.model.predict(X_test)
        mse = mean_squared_error(y_test, predictions)
        rmse = np.sqrt(mse)
        mae = mean_absolute_error(y_test, predictions)
        r2 = r2_score(y_test, predictions)
        
        metrics = {
            "RMSE": rmse,
            "MAE": mae,
            "R2": r2
        }
        
        print(f"--- {self.model_name} Evaluation ---")
        for k, v in metrics.items():
            print(f"{k}: {v:.4f}")
        return metrics, predictions

    def save_model(self, filepath):
        joblib.dump(self.model, filepath)
        print(f"Model saved to {filepath}")

    def load_model(self, filepath):
        if os.path.exists(filepath):
            self.model = joblib.load(filepath)
            print(f"Model loaded from {filepath}")
        else:
            print(f"Model file {filepath} not found.")

class CostPredictor(BasePredictor):
    def __init__(self):
        super().__init__("Cost Predictor (Random Forest)")
        # Random Forest: Robust to outliers, handles non-linearities well
        self.model = RandomForestRegressor(
            n_estimators=100,
            max_depth=15,
            random_state=42,
            n_jobs=-1
        )

class CO2Predictor(BasePredictor):
    def __init__(self):
        super().__init__("CO2 Predictor (XGBoost)")
        # XGBoost: High performance, regularization for generalization
        self.model = XGBRegressor(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=6,
            random_state=42,
            n_jobs=-1,
            # Suppress warnings
            verbosity=1
        )
