import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def prepare_pipeline():
    print("--- Module 3: ML Dataset Preparation ---")

    try:
        df = pd.read_csv("ml_training_dataset.csv") 
    except FileNotFoundError:
        print("Error : Run 'generate_synthetic_data.py' first!")
        return

    feature_cols = [
        'tensile_strength', 
        'weight_capacity', 
        'biodegradability_score', 
        'recyclability_percent',
        'material_type_encoded' 
    ]
    
    
    target_cost = 'price_inr_per_unit'
    target_co2 = 'co2_emission_score'

    X = df[feature_cols]
    y_cost = df[target_cost]
    y_co2 = df[target_co2]

    print(f"Selected {len(feature_cols)} Features and 2 Targets.")

    
    X_train, X_test, y_cost_train, y_cost_test = train_test_split(X, y_cost, test_size=0.2, random_state=42)
    _, _, y_co2_train, y_co2_test = train_test_split(X, y_co2, test_size=0.2, random_state=42)

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    print("Data Split: 80% Training, 20% Testing.")
    print("Features Scaled using StandardScaler.")

    save_data = {
        'X_train': X_train_scaled,
        'X_test': X_test_scaled,
        'y_cost_train': y_cost_train,
        'y_cost_test': y_cost_test,
        'y_co2_train': y_co2_train,
        'y_co2_test': y_co2_test,
        'feature_names': feature_cols
    }
    
   
    joblib.dump(save_data, 'ml_ready_data.pkl')
  
    joblib.dump(scaler, 'feature_scaler.pkl')
    
    print("Pipeline Saved: 'ml_ready_data.pkl' and 'feature_scaler.pkl'")

if __name__ == "__main__":
    prepare_pipeline()