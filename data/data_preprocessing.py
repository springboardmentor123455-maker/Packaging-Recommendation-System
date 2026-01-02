import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sklearn.preprocessing import MinMaxScaler, LabelEncoder

DB_USER = "postgres"
DB_PASS = "XXXX"  
DB_NAME = "ecopack_db"
DB_HOST = "localhost"

def process_data():

    engine = create_engine(f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}')
    df = pd.read_sql("SELECT * FROM packaging_materials", engine)
    print(f" Loaded {len(df)} rows from database.")

    numeric_cols = ['tensile_strength', 'weight_capacity', 'co2_emission_score', 'price_inr_per_unit']
    for col in numeric_cols:
        if df[col].isnull().sum() > 0:
            print(f" Fixing missing values in {col}...")
            df[col].fillna(df[col].median(), inplace=True)

    le = LabelEncoder()
    if 'material_type' in df.columns:
        df['material_type_encoded'] = le.fit_transform(df['material_type'])
        print("Categorical 'materials_type' encoded.")

   
    scaler = MinMaxScaler()
    
   
    norm_price = scaler.fit_transform(df[['price_inr_per_unit']])
    df['cost_efficiency_index'] = 1 - norm_price

    
    norm_co2 = scaler.fit_transform(df[['co2_emission_score']])
    df['co2_impact_index'] = 1 - norm_co2
    
   
    df['durability_index'] = scaler.fit_transform(df[['tensile_strength']])


    df['base_suitability_score'] = (
        (df['co2_impact_index'] * 0.4) + 
        (df['cost_efficiency_index'] * 0.3) + 
        (df['durability_index'] * 0.3)
    )

   
    print("\n--- Data Validation (Summary Stats) ---")
    print(df[['cost_efficiency_index', 'co2_impact_index', 'base_suitability_score']].describe().round(3))
    

    print("\n--- Saving Processed Data ---")
    try:
        
        df.to_sql('processed_materials', engine, if_exists='replace', index=False)
        print(" Success! Processed data saved to table: 'processed_materials'")
    except Exception as e:
        print(f" Error saving to DB: {e}")


    
    
    print("\n Module 2 Complete: Features engineered and indices created.")
    
   
    return df

if __name__ == "__main__":
    df_result = process_data()
    
    
    print("\n--- Top 3 Recommended Materials (Base Score) ---")
    print(df_result[['material_name', 'base_suitability_score']].sort_values(by='base_suitability_score', ascending=False).head(3))