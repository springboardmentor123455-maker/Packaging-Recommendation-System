

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

def load_cleaned_data():
    """Load cleaned materials data"""
    print("Loading cleaned data...")
    df = pd.read_csv('data/materials_cleaned.csv')
    print(f"✓ Loaded {len(df)} cleaned records")
    return df

def create_co2_impact_index(df):
    
    print("\nCreating CO₂ Impact Index...")
    
    df['co2_impact_index'] = (
        (df['co2_emission_score'] * 0.6) + 
        ((100 - df['recyclability_percent']) * 0.4)
    )
    
    # Normalize to 0-100 scale
    df['co2_impact_index'] = (
        (df['co2_impact_index'] - df['co2_impact_index'].min()) / 
        (df['co2_impact_index'].max() - df['co2_impact_index'].min()) * 100
    )
    
    print(f"✓ CO₂ Impact Index created")
    print(f"  Range: {df['co2_impact_index'].min():.2f} - {df['co2_impact_index'].max():.2f}")
    print(f"  Mean: {df['co2_impact_index'].mean():.2f}")
    
    return df

def create_cost_efficiency_index(df):
    """
    Create Cost Efficiency Index
    Higher score = better value for money
    Formula: (Strength / Cost) × (Weight_Capacity / Cost)
    """
    print("\nCreating Cost Efficiency Index...")
    
    df['cost_efficiency_index'] = (
        (df['strength'] / df['cost_per_kg']) * 
        (df['weight_capacity'] / df['cost_per_kg'])
    )
    
    # Normalize to 0-100 scale
    df['cost_efficiency_index'] = (
        (df['cost_efficiency_index'] - df['cost_efficiency_index'].min()) / 
        (df['cost_efficiency_index'].max() - df['cost_efficiency_index'].min()) * 100
    )
    
    print(f"✓ Cost Efficiency Index created")
    print(f"  Range: {df['cost_efficiency_index'].min():.2f} - {df['cost_efficiency_index'].max():.2f}")
    print(f"  Mean: {df['cost_efficiency_index'].mean():.2f}")
    
    return df

def create_material_suitability_score(df):
    """
    Create Material Suitability Score
    Composite score considering multiple factors
    Formula: (Biodegradability × 0.3) + (Recyclability × 0.25) + 
             ((100 - CO₂_Impact_Index) × 0.25) + (Strength_Normalized × 0.2)
    """
    print("\nCreating Material Suitability Score...")
    
    # Normalize strength to 0-100 scale
    strength_normalized = (
        (df['strength'] - df['strength'].min()) / 
        (df['strength'].max() - df['strength'].min()) * 100
    )
    
    df['material_suitability_score'] = (
        (df['biodegradability_score'] * 0.3) +
        (df['recyclability_percent'] * 0.25) +
        ((100 - df['co2_impact_index']) * 0.25) +
        (strength_normalized * 0.2)
    )
    
    print(f"✓ Material Suitability Score created")
    print(f"  Range: {df['material_suitability_score'].min():.2f} - {df['material_suitability_score'].max():.2f}")
    print(f"  Mean: {df['material_suitability_score'].mean():.2f}")
    
    return df

def create_sustainability_rating(df):
    """
    Create Sustainability Rating (1-5 stars)
    Based on combined environmental metrics
    """
    print("\nCreating Sustainability Rating...")
    
    # Calculate eco score
    df['eco_score'] = (
        (df['biodegradability_score'] * 0.35) +
        (df['recyclability_percent'] * 0.35) +
        ((10 - df['co2_emission_score']) * 5 * 0.3)  # Inverse CO₂ (lower is better)
    )
    
    # Convert to 1-5 star rating
    df['sustainability_rating'] = pd.cut(
        df['eco_score'],
        bins=[0, 20, 40, 60, 80, 100],
        labels=[1, 2, 3, 4, 5],
        include_lowest=True
    ).astype(int)
    
    print(f"✓ Sustainability Rating created")
    print(f"  Rating distribution:")
    print(df['sustainability_rating'].value_counts().sort_index())
    
    return df

def create_derived_features(df):
    """Create additional derived features"""
    print("\nCreating derived features...")
    
    # Strength-to-Weight Ratio
    df['strength_weight_ratio'] = df['strength'] / (df['weight_capacity'] + 0.1)  # Avoid division by zero
    
    # Value-for-Money Score
    df['value_for_money'] = (
        (df['strength'] / df['cost_per_kg']) * 0.4 +
        (df['weight_capacity'] / df['cost_per_kg']) * 0.3 +
        (df['biodegradability_score'] / df['cost_per_kg']) * 0.3
    )
    
    # Environmental Impact Score (lower is better)
    df['environmental_impact'] = (
        (df['co2_emission_score'] * 0.5) +
        ((100 - df['biodegradability_score']) * 0.05) +
        ((100 - df['recyclability_percent']) * 0.025)
    )
    
    # Durability Index
    df['durability_index'] = (
        (df['strength'] * 0.4) +
        (df['water_resistance'] * 100 * 0.3) +
        (df['thickness_mm'] * 10 * 0.3)
    )
    
    # Normalize durability index to 0-100
    df['durability_index'] = (
        (df['durability_index'] - df['durability_index'].min()) / 
        (df['durability_index'].max() - df['durability_index'].min()) * 100
    )
    
    print(f"✓ Created 4 derived features:")
    print(f"  - Strength-to-Weight Ratio")
    print(f"  - Value-for-Money Score")
    print(f"  - Environmental Impact Score")
    print(f"  - Durability Index")
    
    return df

def save_engineered_data(df):
    """Save engineered dataset"""
    output_file = 'data/materials_engineered.csv'
    df.to_csv(output_file, index=False)
    print(f"\n✓ Engineered data saved to: {output_file}")
    return output_file

def generate_feature_summary(df):
    """Generate summary of engineered features"""
    print("\n" + "="*70)
    print("ENGINEERED FEATURES SUMMARY")
    print("="*70)
    
    engineered_features = [
        'co2_impact_index',
        'cost_efficiency_index',
        'material_suitability_score',
        'sustainability_rating',
        'eco_score',
        'strength_weight_ratio',
        'value_for_money',
        'environmental_impact',
        'durability_index'
    ]
    
    print("\nEngineered Features Statistics:")
    print(df[engineered_features].describe())
    
    print("\nTop 10 Materials by Suitability Score:")
    top_materials = df.nlargest(10, 'material_suitability_score')[
        ['material_name', 'material_type', 'material_suitability_score', 
         'sustainability_rating', 'cost_per_kg']
    ]
    print(top_materials.to_string(index=False))
    
    print("\nMaterial Type Performance:")
    type_performance = df.groupby('material_type').agg({
        'material_suitability_score': 'mean',
        'sustainability_rating': 'mean',
        'cost_efficiency_index': 'mean',
        'environmental_impact': 'mean'
    }).round(2).sort_values('material_suitability_score', ascending=False)
    print(type_performance)
    
    return df

def main():
    """Main feature engineering pipeline"""
    print("="*70)
    print("EcoPackAI Feature Engineering Pipeline")
    print("="*70)
    
    # Load cleaned data
    df = load_cleaned_data()
    
    # Create engineered features
    df = create_co2_impact_index(df)
    df = create_cost_efficiency_index(df)
    df = create_material_suitability_score(df)
    df = create_sustainability_rating(df)
    df = create_derived_features(df)
    
    # Generate summary
    df = generate_feature_summary(df)
    
    # Save engineered data
    save_engineered_data(df)
    
    print("\n" + "="*70)
    print("✓ Feature engineering completed successfully!")
    print(f"  Total features: {df.shape[1]}")
    print(f"  Ready for ML model training")
    print("="*70)

if __name__ == "__main__":
    main()
