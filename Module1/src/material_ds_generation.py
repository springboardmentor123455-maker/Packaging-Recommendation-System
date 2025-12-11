import pandas as pd
import numpy as np
import random
import os

# Seed for reproducibility
np.random.seed(42)
random.seed(42)

# Number of rows
num_rows = 1500

# Material types
material_types = ['Aluminum', 'Plastic', 'Glass', 'Paper', 'Steel', 'Wood', 'Bamboo', 'Cotton']

# Generate synthetic data
data = {
    'Material_ID': [f'M-{i:04d}' for i in range(1, num_rows+1)],
    'Material_Type': np.random.choice(material_types, num_rows),
    'Strength': np.round(np.random.uniform(50, 500, num_rows), 2),
    'Weight_Capacity': np.round(np.random.uniform(5, 100, num_rows), 2),
    'Biodegradability_Score': np.round(np.random.uniform(0, 1, num_rows), 2),
    'CO2_Emission_Score': np.round(np.random.uniform(1, 50, num_rows), 2),
    'Recyclability_Percent': np.round(np.random.uniform(0, 100, num_rows), 2)
}

df = pd.DataFrame(data)

# Introduce missing values (~5%)
for col in ['Material_Type', 'Strength', 'Weight_Capacity', 'Biodegradability_Score', 'CO2_Emission_Score', 'Recyclability_Percent']:
    df.loc[df.sample(frac=0.05).index, col] = np.nan

# Introduce duplicates (~5%)
duplicates = df.sample(frac=0.05)
df = pd.concat([df, duplicates], ignore_index=True)

# Shuffle rows
df = df.sample(frac=1).reset_index(drop=True)

# Save CSV to Desktop
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "synthetic_materials_dataset_1500.csv")
df.to_csv(desktop_path, index=False)

print(f"Synthetic dataset created! You can find it here: {desktop_path}")
