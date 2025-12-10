EcoPackAI – Packaging Recommendation System

This project recommends sustainable packaging materials based on strength, cost, recyclability, and sustainability parameters.


---
Objective

To build a system that:

collects packaging material data

cleans & preprocesses it

applies feature engineering

stores in database

recommends best eco-friendly material



---

Week-1 (Data Collection + SQL)

✔ Imported 2 datasets

materials.csv

products.csv


✔ Data imported into PostgreSQL

Commands used:

\c ecopackai
\dt
select * from materials;
select * from products;
select count(*) from materials;

✔ Validations

checked table counts

verified schema

previewed records



---
 Week-2 (Data Cleaning + Feature Engineering)

All cleaning done in VS Code using Python.


---

 Data Cleaning Steps

1️⃣ Remove non-numeric values

df[col] = pd.to_numeric(df[col], errors="coerce")

2️⃣ Handle missing values (Median)

df.fillna(df.median(), inplace=True)

✔ Median is used because numeric data can have outliers and mean is affected by outliers.

3️⃣ Normalization using Min-Max

from sklearn.preprocessing import MinMaxScaler

Why Min-Max?

all numeric values scale 0 to 1

easy comparison



---

 Feature Engineering

df["cost_efficiency_index"] = df["strength_kg"]/(df["unit_cost"]+0.0001)

df["sustainability_score"] = df["biodegradability_score"]*0.6 + df["recyclability_percent"]*0.4

df["material_suitability"] = df["sustainability_score"]*0.6 + df["cost_efficiency_index"]*0.4


---

Validation / Outlier Check

df.describe()

Why?

mean, std, min, max gives extreme values

helps identify outliers



---

 Folder Structure

data/
    materials.csv
    products.csv
scripts/
    clean_materials.py
backend/
    recommend.py


---
 Final Output

Cleaned file generated

Stored as data/materials_cleaned.csv

Used for recommendation engine