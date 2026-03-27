import sqlite3
import pandas as pd
import tkinter as tk
from tkinter import filedialog

# Hide the root Tkinter window
root = tk.Tk()
root.withdraw()

# ===========================
# Prompt user to select CSVs
# ===========================
print("Select your Materials CSV file:")
materials_csv = filedialog.askopenfilename(title="Select Materials CSV", filetypes=[("CSV files", "*.csv")])

print("Select your Products CSV file:")
products_csv = filedialog.askopenfilename(title="Select Products CSV", filetypes=[("CSV files", "*.csv")])

# ===========================
# Create/connect to SQLite database
# ===========================
conn = sqlite3.connect("ecopack_ai.db")
print("SQLite database created/connected: ecopack_ai.db")

# ===========================
# Load CSVs into pandas DataFrames
# ===========================
materials_df = pd.read_csv(materials_csv)
products_df = pd.read_csv(products_csv)

# ===========================
# Create tables in SQLite
# ===========================
materials_df.to_sql("Materials", conn, if_exists="replace", index=False)
products_df.to_sql("Products", conn, if_exists="replace", index=False)

print("Tables created and CSVs imported successfully!")

# ===========================
# Preview first 5 rows
# ===========================
print("\nMaterials Table Preview:")
print(pd.read_sql("SELECT * FROM Materials LIMIT 5;", conn))

print("\nProducts Table Preview:")
print(pd.read_sql("SELECT * FROM Products LIMIT 5;", conn))

# ===========================
# Validate table row counts
# ===========================
materials_count = pd.read_sql("SELECT COUNT(*) as count FROM Materials;", conn)
products_count = pd.read_sql("SELECT COUNT(*) as count FROM Products;", conn)
print(f"\nTotal rows in Materials: {materials_count['count'][0]}")
print(f"Total rows in Products: {products_count['count'][0]}")

# ===========================
# Close connection
# ===========================
conn.close()
print("\nSQLite connection closed.")
