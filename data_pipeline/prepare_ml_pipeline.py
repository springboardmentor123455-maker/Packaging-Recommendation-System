import pandas as pd
import numpy as np
import joblib  # Used to save the Scalers for later use
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def prepare_pipeline():
    print("--- Module 3: ML Dataset Preparation ---")
    
    # 1. Load the Large Dataset
    try:
        df = pd.read_csv("ml_training_dataset.csv") # Reads from current folder
    except FileNotFoundError:
        print("❌ Error: Run 'generate_synthetic_data.py' first!")
        return

    # 2. Select Features (X) and Targets (y)
    # Features: What we use to predict (Physical properties + Material Type)
    # Note: We must use the numeric columns, not the text names
    feature_cols = [
        'tensile_strength', 
        'weight_capacity', 
        'biodegradability_score', 
        'recyclability_percent',
        'material_type_encoded' # Ensure this column exists from Module 2
    ]
    
    # Targets: What we want to predict (Cost and CO2)
    target_cost = 'price_inr_per_unit'
    target_co2 = 'co2_emission_score'

    X = df[feature_cols]
    y_cost = df[target_cost]
    y_co2 = df[target_co2]

    print(f"✅ Selected {len(feature_cols)} Features and 2 Targets.")

    # 3. Split Data (Train 80% / Test 20%)
    # We do this TWICE: once for Cost prediction, once for CO2 prediction
    X_train, X_test, y_cost_train, y_cost_test = train_test_split(X, y_cost, test_size=0.2, random_state=42)
    _, _, y_co2_train, y_co2_test = train_test_split(X, y_co2, test_size=0.2, random_state=42)

    # 4. Scaling (Normalization)
    # Standardize features by removing the mean and scaling to unit variance
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    print("✅ Data Split: 80% Training, 20% Testing.")
    print("✅ Features Scaled using StandardScaler.")

    # 5. Save the Processed Data & Scaler
    # We save these so the next module (Model Training) can just load them
    save_data = {
        'X_train': X_train_scaled,
        'X_test': X_test_scaled,
        'y_cost_train': y_cost_train,
        'y_cost_test': y_cost_test,
        'y_co2_train': y_co2_train,
        'y_co2_test': y_co2_test,
        'feature_names': feature_cols
    }
    
    # Save Data
    joblib.dump(save_data, 'ml_ready_data.pkl')
    # Save Scaler (Vital: We need this to scale new user inputs later)
    joblib.dump(scaler, 'feature_scaler.pkl')
    
    print("✅ Pipeline Saved: 'ml_ready_data.pkl' and 'feature_scaler.pkl'")

if __name__ == "__main__":
    prepare_pipeline()