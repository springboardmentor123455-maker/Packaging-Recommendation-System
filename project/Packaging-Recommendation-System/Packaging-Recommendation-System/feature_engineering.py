# FULL DATA CLEANING + FEATURE ENGINEERING

import pandas as pd
from sklearn.preprocessing import MinMaxScaler, LabelEncoder

# 1. LOAD RAW DATA
df = pd.read_csv("cleaned_materials.csv")
print("Loaded rows:", len(df))
print("Columns available:", df.columns.tolist())


# 2. MISSING VALUE CHECK
print(df.isnull().sum())


# 3. REMOVE DUPLICATES
duplicates = df.duplicated().sum()
print("Duplicate rows found:", duplicates)
df.drop_duplicates(inplace=True)
print("After removal, rows:", len(df))


# 4. OUTLIER TREATMENT (IQR)
numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns

for col in numeric_cols:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    outliers = df[(df[col] < lower) | (df[col] > upper)]
    if len(outliers) > 0:
        print(f"{col}: {len(outliers)} outliers → replaced with median")
        df.loc[(df[col] < lower) | (df[col] > upper), col] = df[col].median()
    else:
        print(f"{col}: No outliers found")


# 5. NUMERIC COLUMN SCALING (Min-Max)
scaler = MinMaxScaler()
df_scaled = df.copy()
df_scaled[numeric_cols] = scaler.fit_transform(df[numeric_cols])
print("Scaled numeric columns:", list(numeric_cols))


# 6. CATEGORICAL ENCODING (Label Encoding)
string_cols = df.select_dtypes(include=['object']).columns
df_cleaned = df_scaled.copy()
encoders = {}
for col in string_cols:
    encoder = LabelEncoder()
    df_cleaned[col] = encoder.fit_transform(df_cleaned[col])
    encoders[col] = encoder
    print(f"Encoded column: {col}")


# 7. FEATURE ENGINEERING

# 7a. CO2 Impact Index (lower CO2 → higher score)
df_cleaned['co2_impact_index'] = 1 - scaler.fit_transform(df_cleaned[['co2_emission_kgCO2_per_kg']])
df_cleaned['co2_impact_index'] = df_cleaned['co2_impact_index'].round(2)

# 7b. Cost Efficiency Index (lower cost → higher score)
df_cleaned['cost_efficiency_index'] = 1 - scaler.fit_transform(df_cleaned[['cost_per_kg_usd']])
df_cleaned['cost_efficiency_index'] = df_cleaned['cost_efficiency_index'].round(2)

# 7c. Normalize other features for Material Suitability Score
df_cleaned['strength_norm'] = scaler.fit_transform(df_cleaned[['strength_MPa']])
df_cleaned['weight_capacity_norm'] = scaler.fit_transform(df_cleaned[['weight_capacity_kg']])
df_cleaned['density_norm'] = scaler.fit_transform(df_cleaned[['density_g_per_cm3']])
df_cleaned['biodegradability_norm'] = scaler.fit_transform(df_cleaned[['biodegradability_score']])
df_cleaned['recyclability_norm'] = scaler.fit_transform(df_cleaned[['recyclability_percentage']])

# 7d. Material Suitability Score (weighted sum)
df_cleaned['material_suitability_score'] = (
    0.25 * df_cleaned['co2_impact_index'] +
    0.25 * df_cleaned['cost_efficiency_index'] +
    0.15 * df_cleaned['strength_norm'] +
    0.10 * df_cleaned['weight_capacity_norm'] +
    0.10 * df_cleaned['density_norm'] +
    0.10 * df_cleaned['biodegradability_norm'] +
    0.05 * df_cleaned['recyclability_norm']
)
df_cleaned['material_suitability_score'] = df_cleaned['material_suitability_score'].clip(0,1).round(2)


# 8. EXPORT FINAL DATASET
df_cleaned.to_csv("fully_featured_materials.csv", index=False)
print("\n✔ Fully featured dataset saved as: fully_featured_materials.csv")


# 9. SAMPLE OUTPUT
print("\nSample of computed indices:")
print(df_cleaned[['material_id', 'material_type', 'co2_impact_index', 
                  'cost_efficiency_index', 'material_suitability_score']].head())
