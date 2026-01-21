import sqlite3
import pandas as pd
import os
import numpy as np

# Database configuration
# In production/docker, use absolute path or env var. For now relative to app root or consistent location.
# We placed the DB in Milestone_1/Module_1_Data_Collection/ecopackai.db
# We need to find it relative to this file: Milestone_3/Module_5_Flask_Backend_API/app/database.py

def get_db_path():
    # Go up 3 levels to scratch/infosys
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    db_path = os.path.join(base_dir, 'Milestone_1', 'Module_1_Data_Collection', 'ecopackai.db')
    return db_path

def get_db_connection():
    try:
        db_path = get_db_path()
        print(f"DEBUG: Calculated DB Path: {db_path}")
        if not os.path.exists(db_path):
             print(f"ERROR: Database not found at: {db_path}")
             print(f"DEBUG: Current working directory: {os.getcwd()}")
             print(f"DEBUG: Listing directories at root...")
             try:
                 # valid for render structure
                 print(os.listdir(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))))
             except:
                 pass
             return None
             
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row # Access columns by name
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

def get_all_categories():
    conn = get_db_connection()
    if conn is None:
        print("DB Connection failed. Attempting CSV fallback...")
        return get_categories_from_csv()
    
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM product_categories ORDER BY category_name")
        # specific conversion to dict because sqlite3.Row object behaves like dict but isn't exactly one for JSON serialization sometimes
        categories = [dict(row) for row in cur.fetchall()]
        cur.close()
        conn.close()
        return categories
    except Exception as e:
        print(f"Error fetching categories from DB: {e}")
        if conn:
            conn.close()
        return get_categories_from_csv()

def get_categories_from_csv():
    try:
        # Navigate from app/database.py to data/product_categories.csv
        # Path: scratch/infosys/Milestone_1/Module_1_Data_Collection/data/product_categories.csv
        # Start at app/database.py
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        csv_path = os.path.join(base_dir, 'Milestone_1', 'Module_1_Data_Collection', 'data', 'product_categories.csv')
        
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            # Handle NaN values if any, replace with None or empty string for JSON compatibility if needed
            df = df.replace({np.nan: None})
            return df.to_dict('records')
        else:
            print(f"CSV not found at {csv_path}")
            return []
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return []

def get_dashboard_stats():
    conn = get_db_connection()
    
    if conn:
        try:
            cur = conn.cursor()
            
            # Get Material Trends (Count per type)
            cur.execute("SELECT material_type, count, avg_co2, avg_cost, avg_strength FROM material_statistics")
            trends = [dict(row) for row in cur.fetchall()]
            
            # Calculate Overalls for "Savings" calculation
            cur.execute("SELECT AVG(co2_emission_score) as avg_co2, AVG(cost_per_kg) as avg_cost FROM materials_data")
            overall = dict(cur.fetchone())
            
            # Calculate "Sustainable" averages (e.g. materials with bio > 70)
            cur.execute("SELECT AVG(co2_emission_score) as avg_co2, AVG(cost_per_kg) as avg_cost, AVG(biodegradability_score) as avg_bio FROM materials_data WHERE biodegradability_score > 70")
            susp_avg = dict(cur.fetchone())
            
            # Additional: Savings Comparison per Type for Bar Chart
            # We want Avg CO2 for each type, compared to Avg CO2 of "Sustainable" items of that type (if any)
            cur.execute("""
                SELECT 
                    material_type,
                    AVG(co2_emission_score) as market_avg_co2,
                    AVG(CASE WHEN biodegradability_score > 70 THEN co2_emission_score ELSE NULL END) as susp_avg_co2
                FROM 
                    materials_data
                GROUP BY 
                    material_type
            """)
            savings_comparison = [dict(row) for row in cur.fetchall()]

            cur.close()
            conn.close()
            
            return {
                'trends': trends,
                'overall': overall,
                'sustainable_avg': susp_avg,
                'savings_comparison': savings_comparison
            }
        except Exception as e:
            print(f"Error fetching dashboard stats from DB: {e}")
            if conn: conn.close()
            # If DB error, fall through to CSV
    
    # Fallback to CSV calculation
    print("Calculating dashboard stats from CSV fallback...")
    try:
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        # Prefer cleaned or engineered if available
        # Check explicit paths
        csv_path = os.path.join(base_dir, 'Milestone_1', 'Module_2_Data_Cleaning', 'data', 'materials_cleaned.csv') # Assuming this is where it might be if processed
        if not os.path.exists(csv_path):
             csv_path = os.path.join(base_dir, 'Milestone_1', 'Module_1_Data_Collection', 'data', 'materials.csv')
            
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            
            # Ensure columns exist before accessing
            req_cols = ['material_type', 'co2_emission_score', 'cost_per_kg', 'strength', 'biodegradability_score']
            if not all(col in df.columns for col in req_cols):
                 print(f"Missing columns in CSV for stats. Available: {df.columns}")
                 # Try to map if names are different or return empty
                 if 'CO2 Emission' in df.columns: # Example mapping if needed
                     pass 
                 else:
                     return {}

            # 1. Trends
            trends_df = df.groupby('material_type').agg(
                count=('material_type', 'size'),
                avg_co2=('co2_emission_score', 'mean'),
                avg_cost=('cost_per_kg', 'mean'),
                avg_strength=('strength', 'mean')
            ).reset_index()
            
            trends = trends_df.to_dict('records')
            
            # 2. Overall
            overall = {
                'avg_co2': df['co2_emission_score'].mean(),
                'avg_cost': df['cost_per_kg'].mean()
            }
            
            # 3. Sustainable (bio > 70)
            susp_df = df[df['biodegradability_score'] > 70]
            if not susp_df.empty:
                susp_avg = {
                    'avg_co2': susp_df['co2_emission_score'].mean(),
                    'avg_cost': susp_df['cost_per_kg'].mean(),
                    'avg_bio': susp_df['biodegradability_score'].mean()
                }
            else:
                susp_avg = {'avg_co2': 0, 'avg_cost': 0, 'avg_bio': 0}
            
            # 4. Savings Comparison (Market vs Sustainable per type)
            # Create a helper for sustainable CO2 avg
            def calc_susp_co2(x):
                susp = x[x['biodegradability_score'] > 70]
                return susp['co2_emission_score'].mean() if not susp.empty else None

            savings_df = df.groupby('material_type').agg(
                market_avg_co2=('co2_emission_score', 'mean'),
                susp_avg_co2=('co2_emission_score', lambda x: x[df.loc[x.index, 'biodegradability_score'] > 70].mean())
            ).reset_index()

            # Handle NaN from lambda if no sustainable items
            savings_df['susp_avg_co2'] = savings_df['susp_avg_co2'].fillna(savings_df['market_avg_co2']) 

            savings_comparison = savings_df.to_dict('records')
            
            # Convert numpy types
            trends = [{k: (float(v) if isinstance(v, (np.float32, np.float64)) else int(v) if isinstance(v, (np.int64, np.int32)) else v) for k, v in t.items()} for t in trends]
            overall = {k: float(v) for k, v in overall.items()}
            susp_avg = {k: float(v) for k, v in susp_avg.items()}
            savings_comparison = [{k: (float(v) if isinstance(v, (np.float32, np.float64)) else v) for k, v in t.items()} for t in savings_comparison]

            return {
                'trends': trends,
                'overall': overall,
                'sustainable_avg': susp_avg,
                'savings_comparison': savings_comparison
            }
            
        else:
            print(f"No materials CSV found at {csv_path} for dashboard fallback.")
            return {}
            
    except Exception as e:
        print(f"Error calculating stats from CSV: {e}")
        return {}
