import sqlite3
import pandas as pd
import os

# Database connection parameters (sqlite path)
def get_db_path():
    # We are in app/db_helper.py
    # app/ is current dir
    # Module_5... is parent
    # Milestone_3 is grand parent
    # infosys is great grand parent
    
    # Actually, let's use relative path handling robustly
    # This file is typically at: .../Milestone_3/Module_5_Flask_Backend_API/app/db_helper.py
    
    current_dir = os.path.dirname(os.path.abspath(__file__)) # app
    parent_dir = os.path.dirname(current_dir) # Module_5_Flask_Backend_API
    m3_dir = os.path.dirname(parent_dir) # Milestone_3
    base_dir = os.path.dirname(m3_dir) # infosys root
    
    db_path = os.path.join(base_dir, 'Milestone_1', 'Module_1_Data_Collection', 'ecopackai.db')
    return db_path

def load_data_from_db():
    """Establishes connection to the database and loads materials data. Falls back to CSV."""
    conn = None
    try:
        db_path = get_db_path()
        if os.path.exists(db_path):
             conn = sqlite3.connect(db_path)
             query = "SELECT * FROM materials_data"
             df = pd.read_sql_query(query, conn)
             print(f"Data loaded successfully from Database. Shape: {df.shape}")
             return df
        else:
             print(f"DB not found at {db_path}")
             raise FileNotFoundError("Database file not found")
             
    except Exception as e:
        print(f"Error loading data from DB: {e}")
        print("Attempting to load from local CSV...")
        
        # Fallback to csv location
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            parent_dir = os.path.dirname(current_dir)
            m3_dir = os.path.dirname(parent_dir)
            base_dir = os.path.dirname(m3_dir)
            
            csv_path = os.path.join(base_dir, 'Milestone_1', 'Module_1_Data_Collection', 'data', 'materials.csv')
            
            print(f"Looking for CSV at: {csv_path}")
            if os.path.exists(csv_path):
                df = pd.read_csv(csv_path)
                print(f"Data loaded successfully from CSV. Shape: {df.shape}")
                return df
            else:
                print(f"CSV file not found at {csv_path}. Data loading failed.")
                return None
        except Exception as csv_e:
            print(f"CSV Check Error: {csv_e}")
            return None
    finally:
        if conn:
            conn.close()
