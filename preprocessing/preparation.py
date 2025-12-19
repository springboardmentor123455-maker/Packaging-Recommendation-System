import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline



# LOAD DATA


# Processed features (already cleaned & engineered)
materials_processed = pd.read_csv(
    "D:/codingvscode/Python vscode/infosysintern/Packaging-Recommendation-System/data/processed_materials.csv"
)

# Raw data (for true target values)
materials_raw = pd.read_csv(
    "D:/codingvscode/Python vscode/infosysintern/Packaging-Recommendation-System/data/materials_.csv"
)

print("Processed data shape:", materials_processed.shape)
print("Raw data shape      :", materials_raw.shape)



# FEATURE SELECTION



# Material strength
strength_features = [
    "durability_score",
    "cushioning_score",
    "water_resistance_score",
    "weight_capacity_kg"
]

# Material safety / sustainability
safety_features = [
    "recyclability_score",
    "biodegradability_score"
]

# Shipping category (proxy via physical properties)
shipping_proxy_features = [
    "cushioning_score",
    "water_resistance_score",
    "weight_capacity_kg"
]

# Final feature set (unique)
feature_columns = list(set(
    strength_features +
    safety_features +
    shipping_proxy_features
))

X = materials_processed[feature_columns]



# TARGET VALUE GENERATION


# Cost prediction target
y_cost = materials_raw["cost_per_kg"]

# CO₂ impact prediction target
y_co2 = materials_raw["co2_emission_per_kg"]



# TRAIN–TEST SPLIT


X_train, X_test, y_cost_train, y_cost_test = train_test_split(
    X,
    y_cost,
    test_size=0.20,
    random_state=42
)

_, _, y_co2_train, y_co2_test = train_test_split(
    X,
    y_co2,
    test_size=0.20,
    random_state=42
)



# DATA PIPELINE & SCALING


scaling_pipeline = Pipeline(
    steps=[
        ("scaler", StandardScaler())
    ]
)

X_train_scaled = scaling_pipeline.fit_transform(X_train)
X_test_scaled = scaling_pipeline.transform(X_test)



# VERIFICATION OUTPUT


print("\n=== DATA PREPARATION SUMMARY ===")

print("Selected features:", feature_columns)

print("\nTraining set shapes:")
print("X_train:", X_train_scaled.shape)
print("y_cost_train:", y_cost_train.shape)
print("y_co2_train :", y_co2_train.shape)

print("\nTesting set shapes:")
print("X_test :", X_test_scaled.shape)
print("y_cost_test:", y_cost_test.shape)
print("y_co2_test :", y_co2_test.shape)

print("\nML DATA PREPARATION COMPLETE")
