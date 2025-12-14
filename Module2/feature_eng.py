import pandas as pd
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder

materials = pd.read_csv("synthetic_materials_dataset.csv")
products = pd.read_csv("synthetic_products_dataset.csv")

# Handle missing
for df in [materials, products]:
    for col in df.select_dtypes(include='number').columns:
        df[col] = df[col].fillna(df[col].median())
    for col in df.select_dtypes(exclude='number').columns:
        df[col] = df[col].fillna(df[col].mode()[0])

# Encode categorical in materials
enc = OneHotEncoder(sparse=False, handle_unknown='ignore')
mat_type_encoded = enc.fit_transform(materials[['Material_Type']])
enc_cols = [f"Material_Type_{c}" for c in enc.categories_[0]]
materials[enc_cols] = mat_type_encoded

# Normalize numeric features
scaler = MinMaxScaler()
num_cols_mat = materials.select_dtypes(include='number').columns
materials[num_cols_mat] = scaler.fit_transform(materials[num_cols_mat])

num_cols_prod = products.select_dtypes(include='number').columns
products[num_cols_prod] = scaler.fit_transform(products[num_cols_prod])

# Feature engineering
materials['CO2_Impact_Index'] = materials['CO2_Emission_Score'] * (1 - materials['Recyclability_Percent'])
materials['Cost_Efficiency_Index'] = materials['Strength'] / (materials['Weight_Capacity'] + 1e-6)
materials['Material_Suitability_Score'] = (
    0.4*materials['Strength'] +
    0.3*materials['Biodegradability_Score'] +
    0.3*materials['Recyclability_Percent']
)

# Save CSVs
mat_out = "processed_materials.csv"
prod_out = "processed_products.csv"
materials.to_csv(mat_out, index=False)
products.to_csv(prod_out, index=False)


