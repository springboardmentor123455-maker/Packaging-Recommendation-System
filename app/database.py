import psycopg2
from psycopg2.extras import RealDictCursor

# Database configuration (matching setup_database.py)
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'user': 'postgres', 
    'password': 'postgres',
    'dbname': 'ecopackai_db'
}

def get_db_connection():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
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
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * FROM product_categories ORDER BY category_name")
        categories = cur.fetchall()
        cur.close()
        conn.close()
        return categories
    except Exception as e:
        print(f"Error fetching categories from DB: {e}")
        if conn:
            conn.close()
        return get_categories_from_csv()

def get_categories_from_csv():
    import pandas as pd
    import os
    try:
         # Navigate from app/database.py to data/product_categories.csv
        csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'product_categories.csv')
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            return df.to_dict('records')
        else:
            print(f"CSV not found at {csv_path}")
            return []
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return []
