import pandas as pd
import matplotlib.pyplot as plt

# Load cleaned materials data
df = pd.read_csv("data/materials_cleaned.csv")

# Print column names (for safety)
print(df.columns)

# Numerical columns for histograms
numeric_cols = [
    "strength_kg",
    "weight_g_per_m2",
    "biodegradability_score",
    "co2_emission_kg_per_kg",
    "recyclability_percent",
    "cost_kg"
]

# Plot histograms
for col in numeric_cols:
    plt.figure()
    plt.hist(df[col], bins=10)
    plt.title(f"Histogram of {col}")
    plt.xlabel(col)
    plt.ylabel("Frequency")
    plt.show()