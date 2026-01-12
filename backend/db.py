import psycopg2

def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="packaging_db",
        user="postgres",
        password="your_password"
    )
    return conn
