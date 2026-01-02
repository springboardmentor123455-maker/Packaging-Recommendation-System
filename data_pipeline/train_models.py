import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor  # <--- New Model
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error

def train_and_evaluate():
    print("--- Module 4: Advanced Model Training (RF & XGBoost) ---")
    
    # 1. Load Data
    try:
        data = joblib.load('ml_ready_data.pkl')
        X_train = data['X_train']
        X_test = data['X_test']
        y_cost_train = data['y_cost_train']
        y_cost_test = data['y_cost_test']
        y_co2_train = data['y_co2_train']
        y_co2_test = data['y_co2_test']
        print("✅ Data Loaded Successfully.")
    except FileNotFoundError:
        print("❌ Error: 'ml_ready_data.pkl' not found. Run Module 3 first!")
        return

    # --- MODEL 1: COST PREDICTION (Random Forest) ---
    print("\nTRAINING MODEL 1: Cost Predictor (Random Forest)...")
    cost_model = RandomForestRegressor(n_estimators=100, random_state=42)
    cost_model.fit(X_train, y_cost_train)
    
    # Evaluate Cost
    cost_preds = cost_model.predict(X_test)
    cost_r2 = r2_score(y_cost_test, cost_preds)
    cost_mae = mean_absolute_error(y_cost_test, cost_preds)
    cost_rmse = np.sqrt(mean_squared_error(y_cost_test, cost_preds)) # RMSE Calculation
    
    print(f"   > R² Score: {cost_r2:.4f}")
    print(f"   > MAE (Avg Error): ₹{cost_mae:.2f}")
    print(f"   > RMSE: ₹{cost_rmse:.2f}")

    # --- MODEL 2: CO2 FOOTPRINT PREDICTION (XGBoost) ---
    print("\nTRAINING MODEL 2: CO2 Predictor (XGBoost)...")
    # XGBoost requires no special changes to inputs, it handles scaling well
    co2_model = XGBRegressor(n_estimators=100, learning_rate=0.1, random_state=42)
    co2_model.fit(X_train, y_co2_train)
    
    # Evaluate CO2
    co2_preds = co2_model.predict(X_test)
    co2_r2 = r2_score(y_co2_test, co2_preds)
    co2_mae = mean_absolute_error(y_co2_test, co2_preds)
    co2_rmse = np.sqrt(mean_squared_error(y_co2_test, co2_preds))
    
    print(f"   > R² Score: {co2_r2:.4f}")
    print(f"   > MAE (Avg Error): {co2_mae:.2f} kg")
    print(f"   > RMSE: {co2_rmse:.2f}")

    # 3. Save the Models
    print("\n--- Saving Models ---")
    joblib.dump(cost_model, 'model_cost_rf.pkl')   # Renamed to indicate RF
    joblib.dump(co2_model, 'model_co2_xgb.pkl')    # Renamed to indicate XGB
    print("✅ Models saved: 'model_cost_rf.pkl' & 'model_co2_xgb.pkl'")

if __name__ == "__main__":
    train_and_evaluate()