import pandas as pd
from sklearn.preprocessing import MinMaxScaler, LabelEncoder

print("\n LOAD DATA")
df = pd.read_csv("cleaned_materials.csv")
print("Loaded rows:", len(df))
print("Columns:", len(df.columns))


# 1. MISSING VALUE CHECK
print("\n MISSING VALUE CHECK")
print(df.isnull().sum())


# 2. REMOVE DUPLICATES
print("\n DUPLICATE REMOVAL ")
duplicates = df.duplicated().sum()
print("Duplicate rows found:", duplicates)

df.drop_duplicates(inplace=True)
print("After removal, rows:", len(df))



# 3. OUTLIER TREATMENT (IQR)
print("\n OUTLIER TREATMENT (IQR)")

numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns

for col in numeric_cols:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - (1.5 * IQR)
    upper = Q3 + (1.5 * IQR)

    outliers = df[(df[col] < lower) | (df[col] > upper)]

    if len(outliers) > 0:
        print(f"{col}: {len(outliers)} outliers → replaced with median")
        df.loc[(df[col] < lower) | (df[col] > upper), col] = df[col].median()
    else:
        print(f"{col}: No outliers found")


# 4. NUMERIC COLUMN SCALING (Min-Max)
print("\n NUMERIC SCALING")

scaler = MinMaxScaler()
df_scaled = df.copy()
df_scaled[numeric_cols] = scaler.fit_transform(df[numeric_cols])

print("Scaled numeric columns:", list(numeric_cols))



# 5. CATEGORICAL ENCODING (Label Encoding)
print("\n CATEGORICAL ENCODING")

string_cols = df.select_dtypes(include=['object']).columns
df_cleaned = df_scaled.copy()

encoders = {}
for col in string_cols:
    encoder = LabelEncoder()
    df_cleaned[col] = encoder.fit_transform(df_cleaned[col])
    encoders[col] = encoder
    print(f"Encoded column: {col}")


# 6. CORRELATION REPORT
print("\n CORRELATION MATRIX ")
print(df_cleaned.corr())


# 7. EXPORT CLEANED DATASET
df_cleaned.to_csv("fully_cleaned_materials.csv", index=False)

print("\n✔ Cleaned dataset saved as: fully_cleaned_materials.csv")

