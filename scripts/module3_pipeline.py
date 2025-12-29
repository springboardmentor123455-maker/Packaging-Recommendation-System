import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler

# STEP 1: Load cleaned dataset
df = pd.read_csv("data/materials_cleaned.csv")

print("\n🔹 Dataset Loaded")
print("Shape:", df.shape)

# STEP 2: Feature Selection (X)
features = [
    "strength_kg",
    "weight_g_per_m2",
    "recyclability_percent",
    "water_resistance_score"
]

X = df[features]

# STEP 3: Target Variables (y)
y_cost = df["cost_kg"]                       # Cost Prediction
y_co2 = df["co2_emission_kg_per_kg"]         # CO₂ Prediction

print("\n Selected Features (X):")
print(X.head())

print("\n Target: Cost (y_cost) sample:")
print(y_cost.head())

print("\n Target: CO₂ (y_co2) sample:")
print(y_co2.head())

# STEP 4: Train-Test Split
X_train, X_test, y_cost_train, y_cost_test, y_co2_train, y_co2_test = train_test_split(
    X, y_cost, y_co2, test_size=0.2, random_state=42
)

print("\n Train-Test Split Completed")
print("X_train:", X_train.shape)
print("X_test :", X_test.shape)

# STEP 5: Data Pipeline (Scaling)
scaling_pipeline = Pipeline([
    ("scaler", MinMaxScaler())
])

X_train_scaled = scaling_pipeline.fit_transform(X_train)
X_test_scaled = scaling_pipeline.transform(X_test)

print("\n Data Pipeline & Scaling Prepared")

# Save prepared data for Module 4
pd.DataFrame(X_train_scaled, columns=features).to_csv("data/X_train.csv", index=False)
pd.DataFrame(X_test_scaled, columns=features).to_csv("data/X_test.csv", index=False)

y_cost_train.to_csv("data/y_cost_train.csv", index=False)
y_cost_test.to_csv("data/y_cost_test.csv", index=False)

y_co2_train.to_csv("data/y_co2_train.csv", index=False)
y_co2_test.to_csv("data/y_co2_test.csv", index=False)

print("\n Module 3 Dataset Preparation Completed")