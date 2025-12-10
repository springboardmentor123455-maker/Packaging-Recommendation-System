import pandas as pd
from sqlalchemy import create_engine


DB_USER = "postgres"        
DB_PASS = "XXXX"  
DB_NAME = "ecopack_db"
DB_HOST = "localhost"
CSV_FILE = "materials_final.csv"

def upload_data():
    print("--- Starting Data Upload ---")
    
    
    try:
        engine = create_engine(f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}')
        print(" Connected to Database.")
    except Exception as e:
        print(f" Connection Failed: {e}")
        return

    # 2. Read CSV
    try:
        df = pd.read_csv(CSV_FILE)
        print(f" CSV Read Successfully: Found {len(df)} materials.")
    except FileNotFoundError:
        print(" Error: 'materials_final.csv' not found. Check the file name.")
        return

    
    df = df.rename(columns={
        "tensile_strength_mpa": "tensile_strength",
        "weight_capacity_kg": "weight_capacity"
        
    })

  
    try:
        
        df.to_sql('packaging_materials', engine, if_exists='replace', index=False)
        print(" Success! Data uploaded to 'packaging_materials' table.")
    except Exception as e:
        print(f" Upload Failed: {e}")

if __name__ == "__main__":
    upload_data()