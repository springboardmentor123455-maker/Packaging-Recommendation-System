

import pandas as pd
import numpy as np
from faker import Faker
import random

fake = Faker()
Faker.seed(42)
np.random.seed(42)
random.seed(42)

# Define material types with realistic characteristics
MATERIAL_TYPES = {
    'Cardboard': {
        'strength_range': (200, 800),
        'weight_capacity_range': (5, 30),
        'biodegradability_range': (85, 95),
        'co2_range': (0.8, 1.5),
        'recyclability_range': (85, 100),
        'cost_range': (0.8, 2.5),
        'thickness_range': (2, 8),
        'water_resistance': (2, 4),
        'temp_tolerance_range': (-10, 80)
    },
    'Kraft Paper': {
        'strength_range': (150, 600),
        'weight_capacity_range': (2, 15),
        'biodegradability_range': (90, 100),
        'co2_range': (0.5, 1.2),
        'recyclability_range': (90, 100),
        'cost_range': (0.6, 2.0),
        'thickness_range': (0.5, 3),
        'water_resistance': (1, 3),
        'temp_tolerance_range': (-20, 70)
    },
    'Biodegradable Plastic': {
        'strength_range': (300, 1200),
        'weight_capacity_range': (3, 25),
        'biodegradability_range': (70, 85),
        'co2_range': (1.5, 3.0),
        'recyclability_range': (60, 80),
        'cost_range': (2.5, 6.0),
        'thickness_range': (1, 5),
        'water_resistance': (7, 9),
        'temp_tolerance_range': (-30, 100)
    },
    'Mushroom Packaging': {
        'strength_range': (250, 700),
        'weight_capacity_range': (4, 20),
        'biodegradability_range': (95, 100),
        'co2_range': (0.2, 0.6),
        'recyclability_range': (0, 20),
        'cost_range': (3.0, 8.0),
        'thickness_range': (3, 10),
        'water_resistance': (3, 5),
        'temp_tolerance_range': (-5, 60)
    },
    'Cornstarch Packaging': {
        'strength_range': (200, 800),
        'weight_capacity_range': (2, 18),
        'biodegradability_range': (90, 100),
        'co2_range': (0.4, 1.0),
        'recyclability_range': (10, 30),
        'cost_range': (2.0, 5.5),
        'thickness_range': (1, 4),
        'water_resistance': (5, 7),
        'temp_tolerance_range': (-20, 90)
    },
    'Recycled Paper': {
        'strength_range': (180, 650),
        'weight_capacity_range': (3, 20),
        'biodegradability_range': (85, 95),
        'co2_range': (0.6, 1.3),
        'recyclability_range': (95, 100),
        'cost_range': (0.5, 1.8),
        'thickness_range': (1, 6),
        'water_resistance': (2, 4),
        'temp_tolerance_range': (-15, 75)
    },
    'Bamboo Fiber': {
        'strength_range': (400, 1500),
        'weight_capacity_range': (5, 35),
        'biodegradability_range': (80, 90),
        'co2_range': (0.3, 0.8),
        'recyclability_range': (70, 85),
        'cost_range': (2.5, 7.0),
        'thickness_range': (2, 8),
        'water_resistance': (4, 6),
        'temp_tolerance_range': (-10, 100)
    },
    'Hemp Packaging': {
        'strength_range': (350, 1300),
        'weight_capacity_range': (4, 28),
        'biodegradability_range': (85, 95),
        'co2_range': (0.4, 0.9),
        'recyclability_range': (75, 90),
        'cost_range': (2.8, 7.5),
        'thickness_range': (2, 7),
        'water_resistance': (3, 5),
        'temp_tolerance_range': (-15, 95)
    },
    'Seaweed Packaging': {
        'strength_range': (150, 500),
        'weight_capacity_range': (1, 10),
        'biodegradability_range': (95, 100),
        'co2_range': (0.1, 0.4),
        'recyclability_range': (5, 25),
        'cost_range': (4.0, 10.0),
        'thickness_range': (0.5, 3),
        'water_resistance': (6, 8),
        'temp_tolerance_range': (-10, 70)
    },
    'Glass': {
        'strength_range': (800, 2500),
        'weight_capacity_range': (10, 50),
        'biodegradability_range': (0, 5),
        'co2_range': (0.8, 2.0),
        'recyclability_range': (95, 100),
        'cost_range': (1.5, 5.0),
        'thickness_range': (2, 10),
        'water_resistance': (10, 10),
        'temp_tolerance_range': (-40, 200)
    },
    'Aluminum': {
        'strength_range': (1000, 3500),
        'weight_capacity_range': (15, 80),
        'biodegradability_range': (0, 5),
        'co2_range': (8.0, 15.0),
        'recyclability_range': (90, 100),
        'cost_range': (3.0, 9.0),
        'thickness_range': (0.5, 5),
        'water_resistance': (10, 10),
        'temp_tolerance_range': (-50, 150)
    },
    'Recycled Plastic': {
        'strength_range': (500, 2000),
        'weight_capacity_range': (5, 40),
        'biodegradability_range': (5, 15),
        'co2_range': (2.0, 5.0),
        'recyclability_range': (80, 95),
        'cost_range': (1.5, 4.5),
        'thickness_range': (1, 6),
        'water_resistance': (8, 10),
        'temp_tolerance_range': (-40, 120)
    },
    'Wood Fiber': {
        'strength_range': (300, 1100),
        'weight_capacity_range': (4, 30),
        'biodegradability_range': (75, 90),
        'co2_range': (0.5, 1.1),
        'recyclability_range': (70, 85),
        'cost_range': (1.8, 5.0),
        'thickness_range': (2, 9),
        'water_resistance': (3, 5),
        'temp_tolerance_range': (-20, 90)
    },
    'Cotton Packaging': {
        'strength_range': (250, 900),
        'weight_capacity_range': (2, 15),
        'biodegradability_range': (80, 95),
        'co2_range': (0.6, 1.4),
        'recyclability_range': (65, 80),
        'cost_range': (3.5, 9.0),
        'thickness_range': (1, 5),
        'water_resistance': (2, 4),
        'temp_tolerance_range': (-10, 85)
    },
    'Jute Packaging': {
        'strength_range': (280, 1000),
        'weight_capacity_range': (3, 20),
        'biodegradability_range': (85, 95),
        'co2_range': (0.4, 1.0),
        'recyclability_range': (70, 85),
        'cost_range': (2.0, 6.0),
        'thickness_range': (1, 6),
        'water_resistance': (3, 5),
        'temp_tolerance_range': (-15, 80)
    }
}

def generate_materials_data(num_records=1200):
    """Generate comprehensive materials dataset"""
    
    materials = []
    material_id = 1
    
    # Calculate records per material type
    material_types = list(MATERIAL_TYPES.keys())
    records_per_type = num_records // len(material_types)
    extra_records = num_records % len(material_types)
    
    for idx, material_type in enumerate(material_types):
        # Add extra record to first few types to reach exact count
        count = records_per_type + (1 if idx < extra_records else 0)
        specs = MATERIAL_TYPES[material_type]
        
        for _ in range(count):
            # Generate realistic variations within material type
            material = {
                'material_id': material_id,
                'material_name': f"{material_type} Grade {fake.random_element(['A', 'B', 'C', 'Premium', 'Standard', 'Economy'])}",
                'material_type': material_type,
                'strength': round(np.random.uniform(*specs['strength_range']), 2),
                'weight_capacity': round(np.random.uniform(*specs['weight_capacity_range']), 2),
                'biodegradability_score': round(np.random.uniform(*specs['biodegradability_range']), 2),
                'co2_emission_score': round(np.random.uniform(*specs['co2_range']), 3),
                'recyclability_percent': round(np.random.uniform(*specs['recyclability_range']), 2),
                'cost_per_kg': round(np.random.uniform(*specs['cost_range']), 2),
                'thickness_mm': round(np.random.uniform(*specs['thickness_range']), 2),
                'water_resistance': np.random.randint(specs['water_resistance'][0], specs['water_resistance'][1] + 1),
                'temperature_tolerance': np.random.randint(*specs['temp_tolerance_range'])
            }
            materials.append(material)
            material_id += 1
    
    # Create DataFrame
    df = pd.DataFrame(materials)
    
    # Introduce some realistic missing values (5% of data)
    missing_rate = 0.05
    for col in ['thickness_mm', 'water_resistance', 'temperature_tolerance']:
        mask = np.random.random(len(df)) < missing_rate
        df.loc[mask, col] = np.nan
    
    return df

if __name__ == "__main__":
    print("Generating EcoPackAI Materials Dataset...")
    print("-" * 60)
    
    # Generate data
    materials_df = generate_materials_data(1200)
    
    # Save to CSV
    output_file = 'data/materials.csv'
    materials_df.to_csv(output_file, index=False)
    
    print(f"✓ Generated {len(materials_df)} material records")
    print(f"✓ Material types: {materials_df['material_type'].nunique()}")
    print(f"✓ Saved to: {output_file}")
    print("\nDataset Summary:")
    print(materials_df.describe())
    print("\nMaterial Type Distribution:")
    print(materials_df['material_type'].value_counts())
    print("\n" + "=" * 60)
    print("Materials dataset generation complete!")
