import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="venky5678",   # 🔴 change this
        database="eco_pack_db"
    )
