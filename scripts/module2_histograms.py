import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler

# Load cleaned data
df = pd.read_csv("data/materials_cleaned.csv")

# Select numeric columns
numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns

print("Numeric columns used:")
print(numeric_cols)

# -------------------------
# 1. NORMALIZATION
# -------------------------
scaler = StandardScaler()
scaled_data = scaler.fit_transform(df[numeric_cols])
scaled_df = pd.DataFrame(scaled_data, columns=numeric_cols)

# -------------------------
# 2. HISTOGRAMS
# -------------------------
for col in numeric_cols:
    plt.figure(figsize=(6,4))
    sns.histplot(scaled_df[col], kde=True)
    plt.title(f"Histogram of {col}")
    plt.xlabel(col)
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.show()

# -------------------------
# 3. OUTLIER CHECK (BOXPLOT)
# -------------------------
plt.figure(figsize=(12,6))
sns.boxplot(data=scaled_df)
plt.xticks(rotation=45)
plt.title("Outlier Detection using Boxplot")
plt.tight_layout()
plt.show()