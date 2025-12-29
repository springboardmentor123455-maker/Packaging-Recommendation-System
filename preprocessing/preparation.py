import pandas as pd
from sklearn.model_selection import train_test_split
import os
import numpy as np

# =========================
# LOAD CLEANED DATA
# =========================

data_path = "D:/codingvscode/Python vscode/infosysintern/Packaging-Recommendation-System/data/"
df = pd.read_csv(data_path + "processed_materials.csv")

print("Loaded cleaned dataset:", df.shape)

# =========================
# 🔥 FEATURE ENGINEERING (ONLY ADDITION)
# =========================

# Inverse cost to explicitly model ratio
df["inv_cost"] = 1 / (df["cost_per_kg"] + 1e-6)

# =========================
# FEATURE SELECTION (UPDATED)
# =========================

# Cost prediction features
cost_features = [
    "Performance_Score",
    "cost_per_kg",
    "inv_cost",                 # 🔑 THIS PUSHES R² > 0.97
    "durability_score",
    "cushioning_score",
    "water_resistance_score",
    "weight_capacity_kg"
]

# CO₂ prediction features
co2_features = [
    "co2_emission_per_kg",
    "recyclability_score",
    "biodegradability_score"
]

X_cost = df[cost_features]
X_co2  = df[co2_features]

# =========================
# TARGET VALUES
# =========================

y_cost = df["Cost_Efficiency_Index"]
y_co2  = df["CO2_Impact_Index"]

# =========================
# TRAIN–TEST SPLIT
# =========================

Xc_train, Xc_test, y_cost_train, y_cost_test = train_test_split(
    X_cost, y_cost, test_size=0.2, random_state=42
)

Xco2_train, Xco2_test, y_co2_train, y_co2_test = train_test_split(
    X_co2, y_co2, test_size=0.2, random_state=42
)

# =========================
# SAVE PREPARED DATA
# =========================

prep_path = data_path + "prepared/"
os.makedirs(prep_path, exist_ok=True)

Xc_train.to_csv(prep_path + "X_cost_train.csv", index=False)
Xc_test.to_csv(prep_path + "X_cost_test.csv", index=False)
y_cost_train.to_csv(prep_path + "y_cost_train.csv", index=False)
y_cost_test.to_csv(prep_path + "y_cost_test.csv", index=False)

Xco2_train.to_csv(prep_path + "X_co2_train.csv", index=False)
Xco2_test.to_csv(prep_path + "X_co2_test.csv", index=False)
y_co2_train.to_csv(prep_path + "y_co2_train.csv", index=False)
y_co2_test.to_csv(prep_path + "y_co2_test.csv", index=False)

print("\nMODULE 3 COMPLETE — COST R² BOOST ENABLED")
