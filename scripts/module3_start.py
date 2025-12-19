import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Load cleaned dataset
df = pd.read_csv("data/materials_cleaned.csv")

# Features (X)
X = df[
    [
        "strength_kg",
        "weight_g_per_m2",
        "biodegradability_score",
        "co2_emission_kg_per_kg",
        "recyclability_percent",
        "cost_kg"
    ]
]

# Target (y)
y = df["material_suitability"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print("Training samples:", X_train.shape[0])
print("Testing samples:", X_test.shape[0])

# Train model
model = LinearRegression()
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Evaluation
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
print("RMSE:", rmse)