

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

def load_data():
    
    print("Loading data...")
    df = pd.read_csv('data/materials.csv')
    print(f"✓ Loaded {len(df)} records with {df.shape[1]} columns")
    return df

def handle_missing_values(df):
    """Handle missing values in the dataset"""
    print("\nHandling missing values...")
    
    
    missing_before = df.isnull().sum()
    print(f"Missing values before cleaning:\n{missing_before[missing_before > 0]}")
    
    # Impute numerical features
    numerical_cols = ['thickness_mm', 'water_resistance', 'temperature_tolerance']
    
    for col in numerical_cols:
        if df[col].isnull().any():
            # Use median for imputation
            median_value = df[col].median()
            df[col].fillna(median_value, inplace=True)
            print(f"  ✓ Imputed {col} with median: {median_value:.2f}")
    
    # Verify no missing values remain
    missing_after = df.isnull().sum().sum()
    print(f"✓ Missing values after cleaning: {missing_after}")
    
    return df

def remove_duplicates(df):
    """Remove duplicate material entries"""
    print("\nRemoving duplicates...")
    
    initial_count = len(df)
    df = df.drop_duplicates(subset=['material_name', 'material_type'], keep='first')
    removed = initial_count - len(df)
    
    print(f"✓ Removed {removed} duplicate records")
    print(f"  Remaining records: {len(df)}")
    
    return df

def detect_outliers(df):
    """Detect and handle outliers using Z-score and IQR methods"""
    print("\nDetecting outliers...")
    
    numerical_features = ['strength', 'weight_capacity', 'biodegradability_score', 
                         'co2_emission_score', 'recyclability_percent', 'cost_per_kg']
    
    outlier_counts = {}
    
    for col in numerical_features:
        # Z-score method
        z_scores = np.abs(stats.zscore(df[col]))
        outliers_z = (z_scores > 3).sum()
        
        # IQR method
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        outliers_iqr = ((df[col] < (Q1 - 1.5 * IQR)) | (df[col] > (Q3 + 1.5 * IQR))).sum()
        
        outlier_counts[col] = {'z_score': outliers_z, 'iqr': outliers_iqr}
    
    print("Outlier detection results:")
    for col, counts in outlier_counts.items():
        print(f"  {col}: Z-score={counts['z_score']}, IQR={counts['iqr']}")
    
    print("✓ Outliers detected (not removed - keeping for material diversity)")
    
    return df

def normalize_features(df):
    """Normalize numerical features"""
    print("\nNormalizing features...")
    
    # Create copy for normalized features
    df_normalized = df.copy()
    
    # Standard scaling for strength, weight_capacity, cost
    standard_scaler = StandardScaler()
    standard_cols = ['strength', 'weight_capacity', 'cost_per_kg']
    
    df_normalized[['strength_scaled', 'weight_capacity_scaled', 'cost_scaled']] = \
        standard_scaler.fit_transform(df[standard_cols])
    
    print(f"✓ StandardScaler applied to: {', '.join(standard_cols)}")
    
    # MinMax scaling for scores (0-100 range)
    minmax_scaler = MinMaxScaler()
    score_cols = ['biodegradability_score', 'recyclability_percent']
    
    df_normalized[['biodegradability_normalized', 'recyclability_normalized']] = \
        minmax_scaler.fit_transform(df[score_cols])
    
    print(f"✓ MinMaxScaler applied to: {', '.join(score_cols)}")
    
    # CO2 emission inverse normalization (lower is better)
    co2_scaler = MinMaxScaler()
    df_normalized['co2_normalized'] = 1 - co2_scaler.fit_transform(df[['co2_emission_score']])
    
    print("✓ Inverse normalization applied to CO₂ emission score")
    
    return df_normalized

def encode_categorical(df):
    """Encode categorical variables"""
    print("\nEncoding categorical variables...")
    
    # Label encoding for material_type
    label_encoder = LabelEncoder()
    df['material_type_encoded'] = label_encoder.fit_transform(df['material_type'])
    
    print(f"✓ Label encoding applied to material_type")
    print(f"  Material types: {len(label_encoder.classes_)}")
    
    # Store mapping for reference
    material_mapping = dict(enumerate(label_encoder.classes_))
    print("  Encoding mapping:")
    for code, material in material_mapping.items():
        print(f"    {code}: {material}")
    
    return df

def save_cleaned_data(df):
    """Save cleaned dataset"""
    output_file = 'data/materials_cleaned.csv'
    df.to_csv(output_file, index=False)
    print(f"\n✓ Cleaned data saved to: {output_file}")
    return output_file

def generate_summary_statistics(df):
    """Generate summary statistics"""
    print("\n" + "="*70)
    print("CLEANED DATA SUMMARY STATISTICS")
    print("="*70)
    
    print("\nNumerical Features Summary:")
    print(df[['strength', 'weight_capacity', 'biodegradability_score', 
              'co2_emission_score', 'recyclability_percent', 'cost_per_kg']].describe())
    
    print("\nMaterial Type Distribution:")
    print(df['material_type'].value_counts())
    
    print("\nData Quality Metrics:")
    print(f"  Total records: {len(df)}")
    print(f"  Total features: {df.shape[1]}")
    print(f"  Missing values: {df.isnull().sum().sum()}")
    print(f"  Duplicate rows: {df.duplicated().sum()}")
    
    return df

def main():
    """Main data cleaning pipeline"""
    print("="*70)
    print("EcoPackAI Data Cleaning Pipeline")
    print("="*70)
    
    # Load data
    df = load_data()
    
    # Data cleaning steps
    df = handle_missing_values(df)
    df = remove_duplicates(df)
    df = detect_outliers(df)
    df = normalize_features(df)
    df = encode_categorical(df)
    
    # Generate summary statistics
    df = generate_summary_statistics(df)
    
    # Save cleaned data
    save_cleaned_data(df)
    
    print("\n" + "="*70)
    print("✓ Data cleaning pipeline completed successfully!")
    print("="*70)

if __name__ == "__main__":
    main()
