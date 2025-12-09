import psycopg2
import pandas as pd
import getpass
import os

# --------------------------------------------------
# 1. Ask for PostgreSQL password
# --------------------------------------------------
db_password = getpass.getpass("Enter PostgreSQL password for user 'postgres': ")

# --------------------------------------------------
# 2. Connect to PostgreSQL
# --------------------------------------------------
conn = psycopg2.connect(
    host="localhost",
    database="eco_packaging",
    user="postgres",
    password=db_password
)
cur = conn.cursor()
print("Connected to PostgreSQL")

# --------------------------------------------------
# 3. Load CSV files
# --------------------------------------------------
materials_path = os.path.join("data", "materials_.csv")
products_path = os.path.join("data", "products_.csv")

materials = pd.read_csv(materials_path)
products = pd.read_csv(products_path)

# --------------------------------------------------
# 4. Insert MATERIALS data
# --------------------------------------------------
print("Inserting materials...")

for _, row in materials.iterrows():
    cur.execute("""
        INSERT INTO materials
        (material_name, material_type, durability_score, cushioning_score,
         water_resistance_score, biodegradability_score, recyclability_score,
         co2_emission_per_kg, cost_per_kg, weight_capacity_kg)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        row["material_name"],
        row["material_type"],
        row["durability_score"],
        row["cushioning_score"],
        row["water_resistance_score"],
        row["biodegradability_score"],
        row["recyclability_score"],
        row["co2_emission_per_kg"],
        row["cost_per_kg"],
        row["weight_capacity_kg"]
    ))

print("Materials inserted successfully.")

# --------------------------------------------------
# 5. Insert PRODUCTS data
# --------------------------------------------------
print("Inserting products...")

for _, row in products.iterrows():
    cur.execute("""
        INSERT INTO products
        (product_name, industry, weight_kg, volume_cm3, fragility_level,
         moisture_sensitivity, temperature_sensitivity, price_usd)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        row["product_name"],
        row["industry"],
        row["weight_kg"],
        row["volume_cm3"],
        row["fragility_level"],
        row["moisture_sensitivity"],
        row["temperature_sensitivity"],
        row["price_usd"]
    ))

print("Products inserted successfully.")

# --------------------------------------------------
# 6. Commit & close
# --------------------------------------------------
conn.commit()
cur.close()
conn.close()

print("🎉 All CSV data loaded into PostgreSQL successfully!")
