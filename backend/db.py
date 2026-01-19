import psycopg2
import getpass

# ---------------------------------
# DATABASE CONNECTION
# ---------------------------------

print("Enter PostgreSQL password for user 'postgres':")
db_password = getpass.getpass()

try:
    conn = psycopg2.connect(
        host="localhost",
        database="eco_packaging",
        user="postgres",
        password=db_password
    )
    print("PostgreSQL connected successfully")
except Exception as e:
    print("PostgreSQL connection failed:", e)
    raise


# ---------------------------------
# BASIC LOOKUP FUNCTIONS
# ---------------------------------

def get_materials():
    
    cur = conn.cursor()
    cur.execute("SELECT material_name FROM materials")
    return [row[0] for row in cur.fetchall()]


def get_products():
    
    cur = conn.cursor()
    cur.execute("SELECT product_name FROM products")
    return [row[0] for row in cur.fetchall()] 