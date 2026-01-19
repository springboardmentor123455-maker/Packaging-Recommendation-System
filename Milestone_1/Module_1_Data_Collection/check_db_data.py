import psycopg2
from psycopg2.extras import RealDictCursor

DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'user': 'postgres', 
    'password': 'postgres',
    'dbname': 'ecopackai_db'
}

def check_categories():
    try:
        import os
        database_url = os.environ.get('DATABASE_URL')
        if database_url:
            conn = psycopg2.connect(database_url)
        else:
            conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM product_categories")
        count = cur.fetchone()[0]
        print(f"Total categories in DB: {count}")
        
        if count > 0:
            cur.execute("SELECT category_name FROM product_categories LIMIT 5")
            print("Sample categories:", [r[0] for r in cur.fetchall()])
            
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error checking DB: {e}")

if __name__ == "__main__":
    check_categories()
