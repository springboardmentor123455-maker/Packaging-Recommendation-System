import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

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
# -----------------------------
y = df["cost_kg"]

# -----------------------------
# 4. Train-test split
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print("Training samples:", X_train.shape[0])
print("Testing samples:", X_test.shape[0])

# -----------------------------
# 5. Random Forest Model
# -----------------------------
rf_model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

rf_model.fit(X_train, y_train)

# -----------------------------
# 6. Predictions
# -----------------------------
y_pred = rf_model.predict(X_test)

# -----------------------------
# 7. Evaluation Metrics
# -----------------------------
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("Random Forest Results:")
print("RMSE:", rmse)
print("MAE:", mae)
print("R2 Score:", r2)