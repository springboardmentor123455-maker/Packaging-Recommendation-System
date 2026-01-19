
import sqlite3
import pandas as pd
import os

# Configuration
DB_NAME = "ecopackai.db"
MATERIALS_CSV = "data/materials.csv"
CATEGORIES_CSV = "data/product_categories.csv"

def init_db():
    print("=" * 60)
    print("EcoPackAI - Local Database Setup (SQLite)")
    print("=" * 60)

    # 1. Connect/Create DB
    print(f"\n[Step 1] Initializing {DB_NAME}...")
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        print("✓ Database file created/connected successfully.")
    except Exception as e:
        print(f"✗ Error: {e}")
        return

    # 2. Create Tables
    print("\n[Step 2] Creating Schema...")
    try:
        # Materials Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS materials_data (
                material_id TEXT PRIMARY KEY,
                material_name TEXT,
                material_type TEXT,
                strength REAL,
                weight_capacity REAL,
                biodegradability_score REAL,
                co2_emission_score REAL,
                recyclability_percent REAL,
                cost_per_kg REAL,
                thickness_mm REAL,
                water_resistance TEXT,
                temperature_tolerance REAL
            )
        """)
        
        # Categories Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS product_categories (
                category_id TEXT PRIMARY KEY,
                category_name TEXT,
                fragility_level TEXT,
                required_strength REAL,
                moisture_sensitivity TEXT,
                temperature_sensitivity TEXT,
                typical_weight_min REAL,
                typical_weight_max REAL,
                recommended_materials TEXT
            )
        """)
        
        # Recommendations Table
        cursor.execute("""
             CREATE TABLE IF NOT EXISTS packaging_recommendations (
                recommendation_id INTEGER PRIMARY KEY AUTOINCREMENT,
                request_data TEXT,
                recommended_material_id TEXT,
                score REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✓ Tables created successfully.")
    except Exception as e:
        print(f"✗ Schema Error: {e}")
        conn.close()
        return

    # 3. Import Data
    print("\n[Step 3] Importing Data from CSV...")
    try:
        # Materials
        if os.path.exists(MATERIALS_CSV):
            df_mat = pd.read_csv(MATERIALS_CSV)
            df_mat.to_sql('materials_data', conn, if_exists='replace', index=False)
            print(f"✓ Imported {len(df_mat)} material records.")
        else:
            print(f"⚠ Warning: {MATERIALS_CSV} not found.")

        # Categories
        if os.path.exists(CATEGORIES_CSV):
            df_cat = pd.read_csv(CATEGORIES_CSV)
            df_cat.to_sql('product_categories', conn, if_exists='replace', index=False)
            print(f"✓ Imported {len(df_cat)} category records.")
        else:
            print(f"⚠ Warning: {CATEGORIES_CSV} not found.")
            
    except Exception as e:
        print(f"✗ Import Error: {e}")

    # 4. Validation
    print("\n[Step 4] Final Validation...")
    cursor.execute("SELECT Count(*) FROM materials_data")
    count = cursor.fetchone()[0]
    print(f"✓ Verification: {count} total records available in DB.")

    conn.commit()
    conn.close()
    
    print("\n" + "=" * 60)
    print("SUCCESS: Milestone 1 Setup Complete")
    print("=" * 60)

if __name__ == "__main__":
    init_db()
