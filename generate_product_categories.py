"""
EcoPackAI - Product Categories Data Generator
Generates product categories with specific packaging requirements
"""

import pandas as pd
import numpy as np

# Define product categories with specific packaging requirements
PRODUCT_CATEGORIES = [
    {
        'category_id': 1,
        'category_name': 'Electronics',
        'fragility_level': 9,
        'required_strength': 800,
        'moisture_sensitivity': 9,
        'temperature_sensitivity': 7,
        'typical_weight_min': 0.5,
        'typical_weight_max': 25.0,
        'recommended_materials': 'Cardboard, Biodegradable Plastic, Recycled Plastic, Wood Fiber'
    },
    {
        'category_id': 2,
        'category_name': 'Food & Beverages',
        'fragility_level': 5,
        'required_strength': 400,
        'moisture_sensitivity': 8,
        'temperature_sensitivity': 9,
        'typical_weight_min': 0.1,
        'typical_weight_max': 10.0,
        'recommended_materials': 'Kraft Paper, Cornstarch Packaging, Seaweed Packaging, Glass, Aluminum'
    },
    {
        'category_id': 3,
        'category_name': 'Cosmetics & Personal Care',
        'fragility_level': 6,
        'required_strength': 300,
        'moisture_sensitivity': 7,
        'temperature_sensitivity': 6,
        'typical_weight_min': 0.05,
        'typical_weight_max': 2.0,
        'recommended_materials': 'Recycled Paper, Biodegradable Plastic, Glass, Bamboo Fiber'
    },
    {
        'category_id': 4,
        'category_name': 'Pharmaceuticals',
        'fragility_level': 8,
        'required_strength': 500,
        'moisture_sensitivity': 10,
        'temperature_sensitivity': 10,
        'typical_weight_min': 0.01,
        'typical_weight_max': 5.0,
        'recommended_materials': 'Glass, Aluminum, Biodegradable Plastic, Recycled Plastic'
    },
    {
        'category_id': 5,
        'category_name': 'Books & Media',
        'fragility_level': 3,
        'required_strength': 250,
        'moisture_sensitivity': 6,
        'temperature_sensitivity': 4,
        'typical_weight_min': 0.2,
        'typical_weight_max': 15.0,
        'recommended_materials': 'Cardboard, Kraft Paper, Recycled Paper, Hemp Packaging'
    },
    {
        'category_id': 6,
        'category_name': 'Clothing & Textiles',
        'fragility_level': 2,
        'required_strength': 200,
        'moisture_sensitivity': 5,
        'temperature_sensitivity': 3,
        'typical_weight_min': 0.1,
        'typical_weight_max': 8.0,
        'recommended_materials': 'Cotton Packaging, Jute Packaging, Kraft Paper, Recycled Paper'
    },
    {
        'category_id': 7,
        'category_name': 'Toys & Games',
        'fragility_level': 5,
        'required_strength': 400,
        'moisture_sensitivity': 4,
        'temperature_sensitivity': 4,
        'typical_weight_min': 0.1,
        'typical_weight_max': 10.0,
        'recommended_materials': 'Cardboard, Recycled Plastic, Biodegradable Plastic, Wood Fiber'
    },
    {
        'category_id': 8,
        'category_name': 'Home Appliances',
        'fragility_level': 7,
        'required_strength': 1000,
        'moisture_sensitivity': 6,
        'temperature_sensitivity': 5,
        'typical_weight_min': 2.0,
        'typical_weight_max': 50.0,
        'recommended_materials': 'Cardboard, Wood Fiber, Recycled Plastic, Mushroom Packaging'
    },
    {
        'category_id': 9,
        'category_name': 'Industrial Equipment',
        'fragility_level': 6,
        'required_strength': 1500,
        'moisture_sensitivity': 7,
        'temperature_sensitivity': 6,
        'typical_weight_min': 5.0,
        'typical_weight_max': 100.0,
        'recommended_materials': 'Wood Fiber, Bamboo Fiber, Aluminum, Recycled Plastic'
    },
    {
        'category_id': 10,
        'category_name': 'Fragile Items',
        'fragility_level': 10,
        'required_strength': 600,
        'moisture_sensitivity': 8,
        'temperature_sensitivity': 7,
        'typical_weight_min': 0.1,
        'typical_weight_max': 15.0,
        'recommended_materials': 'Mushroom Packaging, Cornstarch Packaging, Biodegradable Plastic, Cardboard'
    },
    {
        'category_id': 11,
        'category_name': 'Frozen Foods',
        'fragility_level': 4,
        'required_strength': 350,
        'moisture_sensitivity': 10,
        'temperature_sensitivity': 10,
        'typical_weight_min': 0.2,
        'typical_weight_max': 12.0,
        'recommended_materials': 'Biodegradable Plastic, Recycled Plastic, Aluminum, Cornstarch Packaging'
    },
    {
        'category_id': 12,
        'category_name': 'Glassware & Ceramics',
        'fragility_level': 10,
        'required_strength': 700,
        'moisture_sensitivity': 5,
        'temperature_sensitivity': 6,
        'typical_weight_min': 0.3,
        'typical_weight_max': 20.0,
        'recommended_materials': 'Mushroom Packaging, Cardboard, Wood Fiber, Biodegradable Plastic'
    }
]

def generate_product_categories():
    """Generate product categories dataset"""
    
    df = pd.DataFrame(PRODUCT_CATEGORIES)
    return df

if __name__ == "__main__":
    print("Generating EcoPackAI Product Categories Dataset...")
    print("-" * 60)
    
    # Generate data
    categories_df = generate_product_categories()
    
    # Save to CSV
    output_file = 'data/product_categories.csv'
    categories_df.to_csv(output_file, index=False)
    
    print(f"✓ Generated {len(categories_df)} product categories")
    print(f"✓ Saved to: {output_file}")
    print("\nCategories Overview:")
    print(categories_df[['category_name', 'fragility_level', 'required_strength']])
    print("\n" + "=" * 60)
    print("Product categories dataset generation complete!")
