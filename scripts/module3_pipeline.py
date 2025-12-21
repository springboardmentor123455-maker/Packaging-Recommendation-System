import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# -----------------------------
# 1. Load cleaned dataset
# -----------------------------
df = pd.read_csv("data/materials_cleaned.csv")

# -----------------------------
# 2. Feature selection (X)
# -----------------------------
X = df[
    [
        "strength_kg",
        "weight_g_per_m2",
        "biodegradability_score",
        "co2_emission_kg_per_kg",
        "recyclability_percent"
    ]
]

# -----------------------------
# 3. Target variable (y)
# Cost prediction
# -----------------------------
y = df["cost_kg"]

# -----------------------------
# 4. Train–Test Split
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print("Training samples:", X_train.shape[0])
print("Testing samples:", X_test.shape[0])

# -----------------------------
# 5. ML Pipeline (Scaling + Model)
# -----------------------------
pipeline = Pipeline(
    steps=[
        ("scaler", StandardScaler()),
        ("model", LinearRegression())
    ]
)

# -----------------------------
# 6. Train model
# -----------------------------
pipeline.fit(X_train, y_train)

# -----------------------------
# 7. Predictions
# -----------------------------
y_pred = pipeline.predict(X_test)

# -----------------------------
# 8. Evaluation (RMSE)
# -----------------------------
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
print("RMSE:", rmse)