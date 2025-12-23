import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import psycopg2
from psycopg2.extras import RealDictCursor
import os

# Database connection parameters (should match setup_database.py)
DB_PARAMS = {
    "dbname": "eco_pack_db",
    "user": "postgres",
    "password": "password",
    "host": "localhost",
    "port": "5432"
}

def load_data_from_db():
    """Establishes connection to the database and loads materials data. Falls back to CSV."""
    conn = None
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        query = "SELECT * FROM materials_data"
        df = pd.read_sql_query(query, conn)
        print(f"Data loaded successfully from Database. Shape: {df.shape}")
        return df
    except Exception as e:
        print(f"Error loading data from DB: {e}")
        print("Attempting to load from local CSV...")
        csv_path = 'data/materials.csv'
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            print(f"Data loaded successfully from CSV. Shape: {df.shape}")
            return df
        else:
            print(f"CSV file not found at {csv_path}. Data loading failed.")
            return None
    finally:
        if conn:
            conn.close()

def prepare_data(df, target_col='cost_per_kg'):
    """
    Prepares data for ML models.
    
    Args:
        df: Input DataFrame.
        target_col: The target variable to predict ('cost_per_kg' or 'co2_emission_score').
        
    Returns:
        X_train, X_test, y_train, y_test, preprocessor
    """
    if df is None:
        return None, None, None, None, None

    # Separate features and target
    # Dropping ID, name, date columns, and targets
    drop_cols = ['material_id', 'material_name', 'created_at', 'cost_per_kg', 'co2_emission_score']
    
    # Only drop columns that exist
    existing_drop_cols = [col for col in drop_cols if col in df.columns]
    X = df.drop(columns=existing_drop_cols)
    y = df[target_col]

    # Identify numerical and categorical columns
    # Note: 'biodegradability_score', 'recyclability_percent' are numerical
    numeric_features = ['strength', 'weight_capacity', 'biodegradability_score', 
                        'recyclability_percent', 'thickness_mm', 
                        'water_resistance', 'temperature_tolerance']
    
    categorical_features = ['material_type']

    # Create preprocessing steps
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ])

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print(f"Data split completed. Train size: {X_train.shape[0]}, Test size: {X_test.shape[0]}")
    
    return X_train, X_test, y_train, y_test, preprocessor

if __name__ == "__main__":
    df = load_data_from_db()
    if df is not None:
        print("\n--- Preparing Data for Cost Prediction ---")
        X_train_cost, X_test_cost, y_train_cost, y_test_cost, preproc_cost = prepare_data(df, target_col='cost_per_kg')
        
        print("\n--- Preparing Data for CO2 Prediction ---")
        X_train_co2, X_test_co2, y_train_co2, y_test_co2, preproc_co2 = prepare_data(df, target_col='co2_emission_score')
