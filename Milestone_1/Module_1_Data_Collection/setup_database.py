"""
EcoPackAI - Database Setup Script
Sets up SQLite database and imports CSV data
"""

import sqlite3
import pandas as pd
import os
from pathlib import Path

DATABASE_NAME = 'ecopackai.db'

def get_connection():
    """Get database connection"""
    return sqlite3.connect(DATABASE_NAME)


def create_database():
    """Create the EcoPackAI database (SQLite creates it on connection)"""
    try:
        conn = get_connection()
        print(f"✓ Database '{DATABASE_NAME}' ready")
        conn.close()
        return True
    except Exception as e:
        print(f"✗ Error creating database: {e}")
        return False


def create_schema():
    """Execute SQL schema file to create tables"""
    try:
        # Connect to the ecopackai database
        conn = get_connection()
        cursor = conn.cursor()
        
        # Read and execute schema file
        with open('database_schema.sql', 'r', encoding='utf-8') as f:
            schema_sql = f.read()
            
        cursor.executescript(schema_sql)
        conn.commit()
        
        print("✓ Database schema created successfully")
        print("  - materials_data table")
        print("  - product_categories table")
        print("  - packaging_recommendations table")
        print("  - Indexes and views created")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"✗ Error creating schema: {e}")
        return False

def import_csv_data():
    """Import CSV data into SQLite tables"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Import materials data
        materials_file = 'data/materials.csv'
        if os.path.exists(materials_file):
            materials_df = pd.read_csv(materials_file)
            
            insert_query = """
            INSERT INTO materials_data (
                material_id, material_name, material_type, strength, 
                weight_capacity, biodegradability_score, co2_emission_score,
                recyclability_percent, cost_per_kg, thickness_mm, 
                water_resistance, temperature_tolerance
            ) VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            )
            """
            
            for _, row in materials_df.iterrows():
                cursor.execute(insert_query, tuple(row))
            
            conn.commit()
            print(f"✓ Imported {len(materials_df)} materials records")
        
        # Import product categories data
        categories_file = 'data/product_categories.csv'
        if os.path.exists(categories_file):
            categories_df = pd.read_csv(categories_file)
            
            insert_query = """
            INSERT INTO product_categories (
                category_id, category_name, fragility_level, required_strength,
                moisture_sensitivity, temperature_sensitivity, typical_weight_min,
                typical_weight_max, recommended_materials
            ) VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?
            )
            """
            
            for _, row in categories_df.iterrows():
                cursor.execute(insert_query, tuple(row))
            
            conn.commit()
            print(f"✓ Imported {len(categories_df)} product categories")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"✗ Error importing data: {e}")
        return False

def validate_data():
    """Validate imported data"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Count records
        cursor.execute("SELECT COUNT(*) FROM materials_data")
        materials_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM product_categories")
        categories_count = cursor.fetchone()[0]
        
        print("\nDatabase Validation:")
        print(f"  - Materials: {materials_count} records")
        print(f"  - Categories: {categories_count} records")
        
        # Sample query
        cursor.execute("""
            SELECT material_type, COUNT(*) as count, 
                   AVG(biodegradability_score) as avg_bio,
                   AVG(co2_emission_score) as avg_co2
            FROM materials_data 
            GROUP BY material_type 
            ORDER BY avg_bio DESC 
            LIMIT 5
        """)
        
        print("\nTop 5 Material Types by Biodegradability:")
        for row in cursor.fetchall():
            print(f"  - {row[0]}: {row[1]} items, Avg Bio: {row[2]:.2f}, Avg CO₂: {row[3]:.3f}")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"✗ Error validating data: {e}")
        return False

def main():
    """Main setup function"""
    print("=" * 70)
    print("EcoPackAI Database Setup (SQLite)")
    print("=" * 70)
    
    # Step 1: Create database
    print("\n[Step 1] Creating database...")
    if not create_database():
        print("Setup failed at database creation")
        return
    
    # Step 2: Create schema
    print("\n[Step 2] Creating schema...")
    if not create_schema():
        print("Setup failed at schema creation")
        return
    
    # Step 3: Import CSV data
    print("\n[Step 3] Importing CSV data...")
    if not import_csv_data():
        print("Setup failed at data import")
        return
    
    # Step 4: Validate data
    print("\n[Step 4] Validating data...")
    if not validate_data():
        print("Warning: Data validation had issues")
    
    print("\n" + "=" * 70)
    print("✓ Database setup complete!")
    print(f"  Database File: {os.path.abspath(DATABASE_NAME)}")
    print("=" * 70)

if __name__ == "__main__":
    main()
