import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sklearn.preprocessing import MinMaxScaler, LabelEncoder

# --- CONFIGURATION ---
DB_USER = "postgres"
DB_PASS = "0816"  # <--- Update this
DB_NAME = "ecopack_db"
DB_HOST = "localhost"

def process_data():
    print("--- Module 2: Data Cleaning & Feature Engineering ---")

    # 1. CONNECT & LOAD DATA
    engine = create_engine(f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}')
    df = pd.read_sql("SELECT * FROM packaging_materials", engine)
    print(f"✅ Loaded {len(df)} rows from database.")

    # 2. HANDLE MISSING VALUES
    # Strategy: Fill missing numeric values with the Median (safer than Mean)
    numeric_cols = ['tensile_strength', 'weight_capacity', 'co2_emission_score', 'price_inr_per_unit']
    for col in numeric_cols:
        if df[col].isnull().sum() > 0:
            print(f"   ⚠️ Fixing missing values in {col}...")
            df[col].fillna(df[col].median(), inplace=True)
            
    # 3. ENCODE CATEGORICAL DATA
    # We turn text like "Bioplastic" into numbers (0, 1, 2) for ML analysis
    le = LabelEncoder()
    if 'material_type' in df.columns:
        df['material_type_encoded'] = le.fit_transform(df['material_type'])
        print("✅ Categorical 'material_type' encoded.")

    # 4. NORMALIZE NUMERICAL FEATURES (Scale 0 to 1)
    # We use MinMaxScaler so all values are fair game for the algorithm
    scaler = MinMaxScaler()
    
    # 5. FEATURE ENGINEERING: CREATING INDICES
    
    # A. Cost Efficiency Index
    # Logic: Lower Price is BETTER. 
    # Formula: 1 - Normalized(Price)
    # Result: 1.0 = Cheapest (Best), 0.0 = Most Expensive (Worst)
    norm_price = scaler.fit_transform(df[['price_inr_per_unit']])
    df['cost_efficiency_index'] = 1 - norm_price

    # B. CO2 Impact Index
    # Logic: Lower CO2 is BETTER.
    # Formula: 1 - Normalized(CO2)
    # Result: 1.0 = Eco-Friendly, 0.0 = Polluting
    norm_co2 = scaler.fit_transform(df[['co2_emission_score']])
    df['co2_impact_index'] = 1 - norm_co2
    
    # C. Durability Index (Helper for Suitability)
    # Logic: Higher Strength is BETTER.
    df['durability_index'] = scaler.fit_transform(df[['tensile_strength']])

    # D. Material Suitability Score (Base Calculation)
    # Assumption: For a general score, we give equal weight to Eco (40%), Cost (30%), Strength (30%)
    # NOTE: The User Interface will allow dynamic weights later, but this is a static baseline.
    df['base_suitability_score'] = (
        (df['co2_impact_index'] * 0.4) + 
        (df['cost_efficiency_index'] * 0.3) + 
        (df['durability_index'] * 0.3)
    )

    # 6. VALIDATE DATA QUALITY (Summary Statistics)
    print("\n--- Data Validation (Summary Stats) ---")
    print(df[['cost_efficiency_index', 'co2_impact_index', 'base_suitability_score']].describe().round(3))
    # 6. SAVE TO DATABASE (The New Step)
    print("\n--- Saving Processed Data ---")
    try:
        # We create a NEW table called 'processed_materials'
        # 'if_exists="replace"' will drop the old one and create a fresh one every time you run this.
        df.to_sql('processed_materials', engine, if_exists='replace', index=False)
        print("✅ Success! Processed data saved to table: 'processed_materials'")
    except Exception as e:
        print(f"❌ Error saving to DB: {e}")


    # Optional: Save processed data back to DB or CSV for inspection
    # df.to_csv("processed_materials.csv", index=False)
    print("\n✅ Module 2 Complete: Features engineered and indices created.")
    
    # Return df for viewing if running in notebook
    return df

if __name__ == "__main__":
    df_result = process_data()
    
    # Show the top 3 "Best" materials based on our new Suitability Score
    print("\n--- Top 3 Recommended Materials (Base Score) ---")
    print(df_result[['material_name', 'base_suitability_score']].sort_values(by='base_suitability_score', ascending=False).head(3))