import pandas as pd

df = pd.read_csv("data/processed_materials.csv")

X = df[
    [
        'material_suitability_score',
        'biodegradability_score',
        'recyclability_percent',
        'strength_Low',
        'strength_Medium',
        'weight_capacity_Low',
        'weight_capacity_Medium'
    ]
]

X.to_csv("ml/features.csv", index=False)

print("✅ Feature selection completed")
