# backend/clean_materials.py
import pandas as pd

# 1) read
df = pd.read_csv("data/materials.csv", dtype=str)   # read as strings first to inspect

# 2) strip spaces from column names and values
df.columns = [c.strip() for c in df.columns]
df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

# 3) fix any obvious header typos (example)
# rename map if needed (adjust to your actual header)
rename_map = {
    'material id':'material_id',
    'material id':'material_id',
    # add other mapping if you spotted typos
}
df = df.rename(columns=rename_map)

# 4) convert numeric columns (add the actual numeric columns you have)
num_cols = ['material_id','strength_kg','weight_g_per_m2','biodegradability_score',
            'co2_emission_kg_per_kg','recyclability_percent','cost_per_unit']
for col in num_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')   # invalid -> NaN

# 5) drop rows with no material_name
df = df[df['material_name'].notna()]

# 6) fill or remove NaNs (example: drop rows where material_id or material_name missing)
df = df.dropna(subset=['material_id','material_name'])

# 7) optional: remove duplicate material_name (keep first)
df = df.drop_duplicates(subset=['material_name'], keep='first')

# 8) reorder columns if you like
cols = ['material_id','material_name','material_type','strength_kg','weight_g_per_m2',
        'biodegradability_score','co2_emission_kg_per_kg','recyclability_percent','cost_per_unit']
cols = [c for c in cols if c in df.columns]
df = df[cols]

# 9) save cleaned CSV
df.to_csv("data/materials_cleaned.csv", index=False)
print("Saved data/materials_cleaned.csv with", len(df), "rows")
