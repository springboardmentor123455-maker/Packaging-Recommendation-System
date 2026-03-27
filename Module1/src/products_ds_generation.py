import pandas as pd
import numpy as np
import random
import os

# Seed for reproducibility
np.random.seed(42)
random.seed(42)

# Number of products
num_rows = 200

# Product categories
categories = ['Electronics', 'Food', 'Cosmetics', 'Books', 'Glassware', 'Toys', 'Apparel', 'Furniture']

# Distribute categories evenly across products
category_list = (categories * (num_rows // len(categories) + 1))[:num_rows]
random.shuffle(category_list)

# Generate synthetic products
data = {
    'Product_ID': [i for i in range(1, num_rows+1)],
    'Product_Name': [f'Product_{i:03d}' for i in range(1, num_rows+1)],
    'Category': category_list,
    'Avg_Weight_g': np.round(np.random.uniform(50, 1500, num_rows), 2),
    'Fragility_Score': np.round(np.random.uniform(0, 1, num_rows), 2),
    'Dimension_L_cm': np.round(np.random.uniform(5, 50, num_rows), 2),
    'Dimension_W_cm': np.round(np.random.uniform(5, 50, num_rows), 2),
    'Dimension_H_cm': np.round(np.random.uniform(2, 30, num_rows), 2)
}

df_products = pd.DataFrame(data)

# Shuffle rows to mix categories
df_products = df_products.sample(frac=1).reset_index(drop=True)

# Save CSV to Desktop
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "synthetic_products_dataset_final_200.csv")
df_products.to_csv(desktop_path, index=False)

print(f"Final synthetic products dataset created! You can find it here: {desktop_path}")
print(df_products.head(10))
