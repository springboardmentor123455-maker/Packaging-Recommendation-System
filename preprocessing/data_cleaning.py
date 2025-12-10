
import psycopg2
import pandas as pd
from sklearn.impute import SimpleImputer
import getpass
import os
import numpy as np
from sqlalchemy import create_engine


db_password = getpass.getpass("Enter PostgreSQL password for 'postgres': ")

engine = create_engine(
    f"postgresql://postgres:{db_password}@localhost/eco_packaging"
)

conn = psycopg2.connect(
    host="localhost",
    database="eco_packaging",
    user="postgres",
    password=db_password
)

print("\n🔗 Connected to PostgreSQL!")



def iqr_clip(df, col):
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    df[col] = df[col].clip(Q1 - 1.5 * IQR, Q3 + 1.5 * IQR)




mean_imputer = SimpleImputer(strategy="mean")
median_imputer = SimpleImputer(strategy="median")

def preprocess(df):

    # Drop ID columns
    id_cols = [c for c in df.columns if c.lower().endswith("_id")]
    df = df.drop(columns=id_cols, errors="ignore")

    # Identify numeric columns
    numeric = df.select_dtypes(include=['float64', 'int64']).columns

    # Split numeric -> scores vs others
    bounded_scores = [c for c in numeric if "score" in c.lower()]
    other_numeric = [c for c in numeric if c not in bounded_scores]

    # Impute missing values
    if bounded_scores:
        df[bounded_scores] = mean_imputer.fit_transform(df[bounded_scores])

    if other_numeric:
        df[other_numeric] = median_imputer.fit_transform(df[other_numeric])

    # Outlier clipping
    for col in numeric:
        iqr_clip(df, col)

    return df



materials = pd.read_sql("SELECT * FROM materials;", engine)
products = pd.read_sql("SELECT * FROM products;", engine)

print("\nDATA LOADED")
print(materials.shape, products.shape)



materials_processed = preprocess(materials)
products_processed = preprocess(products)

print("\nPREPROCESSING COMPLETE")



save_path = r"D:/codingvscode/Python vscode/infosysintern/Packaging-Recommendation-System/data/"
os.makedirs(save_path, exist_ok=True)

materials_processed.to_csv(save_path + "processed_materials.csv", index=False)
products_processed.to_csv(save_path + "processed_products.csv", index=False)

print("\n💾 CSVs saved")



materials_processed.to_sql("materials_processed", engine, if_exists="append", index=False, method="multi")
products_processed.to_sql("products_processed", engine, if_exists="append", index=False, method="multi")

print("\n📦 Inserted into DB")



print("\nVALIDATION")
print("\nShapes:", materials_processed.shape, products_processed.shape)

print("\nMissing values:")
print(materials_processed.isna().sum())
print(products_processed.isna().sum())

print("\nDuplicates:")
print(materials_processed.duplicated().sum(), products_processed.duplicated().sum())

print("\nSummary Stats:")
print(materials_processed.describe().T)
print(products_processed.describe().T)



conn.close()
print("\n🔒 DB Closed")
print("\n🎯 DONE")
