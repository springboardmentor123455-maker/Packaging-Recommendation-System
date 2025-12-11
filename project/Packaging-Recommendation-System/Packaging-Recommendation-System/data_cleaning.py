import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler


# 1. LOAD DATA
print("\n LOAD DATA")
df = pd.read_csv("data/sustainable_materials.csv")
print("Loaded rows:", len(df))
print("Initial Shape:", df.shape)
print("Columns:", len(df.columns))
print(df.head())

# 2. MISSING VALUE SUMMARY
print("\n MISSING VALUE SUMMARY")

missing_count = df.isnull().sum()
print(df.isnull().sum())
missing_percent = (df.isnull().mean() * 100).round(2)

summary_table = pd.DataFrame({
    "Missing Count": missing_count,
    "Missing %": missing_percent
})

print(summary_table)


# 3. HANDLE MISSING VALUES

# Numeric columns
numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns

# Categorical columns
cat_cols = df.select_dtypes(include=['object']).columns

# Fill numeric → median
df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())

# Fill categorical → mode
df[cat_cols] = df[cat_cols].fillna(df[cat_cols].mode().iloc[0])

# Remove duplicates
df = df.drop_duplicates()
print("After Removing Duplicates:", df.shape)


# 4. DROP RULES
# Drop fully empty rows
before = len(df)
df.dropna(how="all", inplace=True)
after = len(df)
print(f"Dropped fully-empty rows: {before - after}")

# Drop columns with > 80% missing
cols_to_drop = df.columns[df.isnull().mean() > 0.80]

if len(cols_to_drop) > 0:
    print("Dropped columns (>80% missing):", list(cols_to_drop))
    df.drop(columns=cols_to_drop, inplace=True)
else:
    print("No columns dropped (>80% missing)")


# 5. NUMERIC COLUMN HANDLING (Rules)
print("\n NUMERIC COLUMN FIXING")

numeric_fixed = False

for col in numeric_cols:
    if col not in df.columns:
        continue

    miss_pct = df[col].isnull().mean()

    if miss_pct == 0:
        continue

    numeric_fixed = True
    print(f"Fixing numeric column: {col} ({round(miss_pct*100, 2)}% missing)")

    if miss_pct < 0.05:
        df[col].fillna(df[col].median(), inplace=True)
    elif miss_pct < 0.30:
        df[col].fillna(df[col].mean(), inplace=True)
    elif miss_pct < 0.60:
        df[col] = df[col].interpolate(method='linear', limit_direction='forward')
    else:
        df[col].fillna(-1, inplace=True)

if not numeric_fixed:
    print("✔ No numeric columns needed fixing.")


# 6. CATEGORICAL COLUMN HANDLING (Rules)
print("\n CATEGORICAL COLUMN FIXING")

categorical_fixed = False

for col in cat_cols:
    if col not in df.columns:
        continue

    miss_pct = df[col].isnull().mean()

    if miss_pct == 0:
        continue

    categorical_fixed = True
    print(f"Fixing categorical column: {col} ({round(miss_pct*100,2)}% missing)")

    if miss_pct < 0.05:
        df[col].fillna(df[col].mode()[0], inplace=True)
    elif miss_pct < 0.30:
        df[col].fillna("Unknown", inplace=True)
    else:
        df[col].fillna("Not Provided", inplace=True)

if not categorical_fixed:
    print("✔ No categorical columns needed fixing.")


# 7. OUTLIER TREATMENT (IQR → median)
print("\n  OUTLIER TREATMENT (IQR)")

numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
outlier_found = False

for col in numeric_cols:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1

    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    outliers = df[(df[col] < lower) | (df[col] > upper)]

    if len(outliers) > 0:
        outlier_found = True
        print(f"Outliers in {col}: {len(outliers)} → replaced with median")
        df.loc[(df[col] < lower) | (df[col] > upper), col] = df[col].median()

if not outlier_found:
    print("✔ No outliers detected in any numeric column.")


# 8. NORMALIZATION (MinMax Scaling)
print("\n NORMALIZATION ")

scaler = MinMaxScaler()

df_scaled = df.copy()
df_scaled[numeric_cols] = scaler.fit_transform(df[numeric_cols])

print("Normalized numerical columns:")
print(df_scaled[numeric_cols].head())


# 9. SAVE CLEANED DATASETS
df.to_csv("cleaned_materials.csv", index=False)
df_scaled.to_csv("cleaned_materials_normalized.csv", index=False)

print("\n✔ Cleaned dataset saved as: cleaned_materials.csv")
print("✔ Cleaned + Normalized dataset saved as: cleaned_materials_normalized.csv")

