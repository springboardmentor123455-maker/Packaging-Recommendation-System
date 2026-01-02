import pandas as pd
import numpy as np
from sqlalchemy import create_engine


DB_USER = "postgres"
DB_PASS = "0816"  
DB_NAME = "ecopack_db"
DB_HOST = "localhost"

def generate_data():
    print("--- Step 1: Loading Seed Data ---")
    engine = create_engine(f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}')
    
    df_seed = pd.read_sql("SELECT * FROM processed_materials", engine)
    
    synthetic_rows = []
    
    print(f"--- Step 2:Generating Synthetic Variations (Target: 1000 rows) ---")

    for _ in range(50): 
        for index, row in df_seed.iterrows():
            
            noise_factor = np.random.uniform(0.9, 1.1) 
            
            new_row = row.copy()
            new_row['tensile_strength'] = row['tensile_strength'] * noise_factor
            new_row['weight_capacity'] = row['weight_capacity'] * np.random.uniform(0.9, 1.1)
            new_row['price_inr_per_unit'] = row['price_inr_per_unit'] * np.random.uniform(0.95, 1.05)
            new_row['co2_emission_score'] = row['co2_emission_score'] * np.random.uniform(0.98, 1.02)
            
            synthetic_rows.append(new_row)
            
    df_large = pd.DataFrame(synthetic_rows)
    
    df_large = df_large.sample(frac=1).reset_index(drop=True)
    
    print(f"Generated {len(df_large)} rows of synthetic data.")
    
    df_large.to_csv("data_pipeline/ml_training_dataset.csv", index=False)
    print("Saved to 'data_pipeline/ml_training_dataset.csv'")

if __name__ == "__main__":
    generate_data()