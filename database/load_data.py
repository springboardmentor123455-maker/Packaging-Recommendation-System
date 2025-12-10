import psycopg2
import pandas as pd
import getpass
import os

# ======================
# CONNECT TO DATABASE
# ======================
db_password = getpass.getpass("Enter PostgreSQL password for 'postgres': ")

conn = psycopg2.connect(
    host="localhost",
    database="eco_packaging",
    user="postgres",
    password=db_password
)
cur = conn.cursor()
print("✅ Connected to PostgreSQL")

# ======================
# LOAD CSV FILES
# ======================
materials = pd.read_csv(
    r"D:\codingvscode\Python vscode\infosysintern\Packaging-Recommendation-System\data\materials_.csv"
)
products = pd.read_csv(
    r"D:\codingvscode\Python vscode\infosysintern\Packaging-Recommendation-System\data\products_.csv"
)

print(f"📄 Loaded CSVs: {materials.shape} materials, {products.shape} products")

# ======================
# DROP ID COLUMNS IF EXISTS
# ======================
materials = materials.drop(columns=[c for c in materials.columns if c.lower() == "material_id"], errors="ignore")
products  = products.drop(columns=[c for c in products.columns  if c.lower() == "product_id"], errors="ignore")

# ======================
# INSERT MATERIALS
# ======================
materials_inserted = 0
materials_failed = 0

for _, row in materials.iterrows():
    try:
        cur.execute("SAVEPOINT sp;")

        cur.execute("""
            INSERT INTO materials
            (material_name, material_type, durability_score, cushioning_score,
             water_resistance_score, biodegradability_score, recyclability_score,
             co2_emission_per_kg, cost_per_kg, weight_capacity_kg)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (material_name) DO NOTHING;
        """, tuple(row.values))

        if cur.rowcount:
            materials_inserted += 1

    except Exception as e:
        materials_failed += 1
        print("❌ Material insert failed:", e)
        cur.execute("ROLLBACK TO SAVEPOINT sp;")

print(f"✔️ Materials inserted: {materials_inserted}")
print(f"⚠️ Materials failed: {materials_failed}")

# ======================
# INSERT PRODUCTS
# ======================
products_inserted = 0
products_failed = 0

for _, row in products.iterrows():
    try:
        cur.execute("SAVEPOINT sp;")

        cur.execute("""
            INSERT INTO products
            (product_name, industry, weight_kg, volume_cm3, fragility_level,
             moisture_sensitivity, temperature_sensitivity, price_usd)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (product_name) DO NOTHING;
        """, tuple(row.values))

        if cur.rowcount:
            products_inserted += 1

    except Exception as e:
        products_failed += 1
        print("❌ Product insert failed:", e)
        cur.execute("ROLLBACK TO SAVEPOINT sp;")

print(f"✔️ Products inserted: {products_inserted}")
print(f"⚠️ Products failed: {products_failed}")

# ======================
# COMMIT & CLOSE
# ======================
conn.commit()
cur.close()
conn.close()
print("\n🎉 Raw CSV data loaded into PostgreSQL successfully!")
