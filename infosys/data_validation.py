"""
EcoPackAI - Data Validation and Quality Report Generator
Generates comprehensive data quality reports with visualizations
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Set visualization style
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (12, 6)

def load_data():
    """Load all datasets for validation"""
    print("Loading datasets for validation...")
    
    materials_raw = pd.read_csv('data/materials.csv')
    materials_cleaned = pd.read_csv('data/materials_cleaned.csv')
    materials_engineered = pd.read_csv('data/materials_engineered.csv')
    product_categories = pd.read_csv('data/product_categories.csv')
    
    print(f"✓ Raw materials: {len(materials_raw)} records")
    print(f"✓ Cleaned materials: {len(materials_cleaned)} records")
    print(f"✓ Engineered materials: {len(materials_engineered)} records")
    print(f"✓ Product categories: {len(product_categories)} records")
    
    return materials_raw, materials_cleaned, materials_engineered, product_categories

def validate_completeness(df, dataset_name):
    """Validate data completeness"""
    print(f"\nValidating completeness for {dataset_name}...")
    
    total_cells = df.shape[0] * df.shape[1]
    missing_cells = df.isnull().sum().sum()
    completeness = ((total_cells - missing_cells) / total_cells) * 100
    
    print(f"  Completeness: {completeness:.2f}%")
    print(f"  Missing cells: {missing_cells} / {total_cells}")
    
    if missing_cells > 0:
        print("  Missing values by column:")
        missing_by_col = df.isnull().sum()
        for col, count in missing_by_col[missing_by_col > 0].items():
            print(f"    - {col}: {count} ({count/len(df)*100:.2f}%)")
    
    return completeness

def validate_consistency(df):
    """Validate data consistency"""
    print("\nValidating data consistency...")
    
    issues = []
    
    # Check if scores are within valid ranges
    if 'biodegradability_score' in df.columns:
        invalid_bio = df[(df['biodegradability_score'] < 0) | (df['biodegradability_score'] > 100)]
        if len(invalid_bio) > 0:
            issues.append(f"Biodegradability scores out of range: {len(invalid_bio)}")
    
    if 'recyclability_percent' in df.columns:
        invalid_rec = df[(df['recyclability_percent'] < 0) | (df['recyclability_percent'] > 100)]
        if len(invalid_rec) > 0:
            issues.append(f"Recyclability percentages out of range: {len(invalid_rec)}")
    
    # Check for negative values in physical properties
    numeric_cols = ['strength', 'weight_capacity', 'cost_per_kg']
    for col in numeric_cols:
        if col in df.columns:
            negative = df[df[col] < 0]
            if len(negative) > 0:
                issues.append(f"Negative values in {col}: {len(negative)}")
    
    if len(issues) == 0:
        print("  ✓ No consistency issues found")
    else:
        print("  Consistency issues found:")
        for issue in issues:
            print(f"    - {issue}")
    
    return len(issues) == 0

def validate_accuracy(df):
    """Validate data accuracy through statistical analysis"""
    print("\nValidating data accuracy...")
    
    # Check for unrealistic outliers
    numeric_cols = ['strength', 'weight_capacity', 'cost_per_kg', 'co2_emission_score']
    
    outlier_summary = {}
    for col in numeric_cols:
        if col in df.columns:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            outliers = df[(df[col] < (Q1 - 1.5 * IQR)) | (df[col] > (Q3 + 1.5 * IQR))]
            outlier_summary[col] = len(outliers)
    
    print("  Outlier detection (IQR method):")
    for col, count in outlier_summary.items():
        print(f"    - {col}: {count} outliers ({count/len(df)*100:.2f}%)")
    
    return outlier_summary

def create_distribution_plots(df):
    """Create distribution plots for key metrics"""
    print("\nGenerating distribution plots...")
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    fig.suptitle('EcoPackAI - Key Metrics Distribution', fontsize=16, fontweight='bold')
    
    metrics = [
        ('biodegradability_score', 'Biodegradability Score'),
        ('recyclability_percent', 'Recyclability %'),
        ('co2_emission_score', 'CO₂ Emission Score'),
        ('strength', 'Strength (kg/cm²)'),
        ('cost_per_kg', 'Cost per kg ($)'),
        ('weight_capacity', 'Weight Capacity (kg)')
    ]
    
    for idx, (col, title) in enumerate(metrics):
        row = idx // 3
        col_idx = idx % 3
        
        if col in df.columns:
            axes[row, col_idx].hist(df[col].dropna(), bins=30, color='steelblue', edgecolor='black', alpha=0.7)
            axes[row, col_idx].set_title(title, fontweight='bold')
            axes[row, col_idx].set_xlabel(title)
            axes[row, col_idx].set_ylabel('Frequency')
            axes[row, col_idx].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('data/distribution_plots.png', dpi=300, bbox_inches='tight')
    print("  ✓ Distribution plots saved to data/distribution_plots.png")
    plt.close()

def create_correlation_heatmap(df):
    """Create correlation heatmap for numerical features"""
    print("\nGenerating correlation heatmap...")
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    correlation_matrix = df[numeric_cols].corr()
    
    plt.figure(figsize=(14, 12))
    sns.heatmap(correlation_matrix, annot=True, fmt='.2f', cmap='coolwarm', 
                center=0, square=True, linewidths=1, cbar_kws={"shrink": 0.8})
    plt.title('Feature Correlation Heatmap', fontsize=16, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig('data/correlation_heatmap.png', dpi=300, bbox_inches='tight')
    print("  ✓ Correlation heatmap saved to data/correlation_heatmap.png")
    plt.close()

def create_material_comparison_plot(df):
    """Create material type comparison plot"""
    print("\nGenerating material type comparison...")
    
    if 'material_type' in df.columns:
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Material Type Performance Comparison', fontsize=16, fontweight='bold')
        
        # Average biodegradability by material type
        bio_avg = df.groupby('material_type')['biodegradability_score'].mean().sort_values(ascending=False)
        axes[0, 0].barh(bio_avg.index, bio_avg.values, color='green', alpha=0.7)
        axes[0, 0].set_xlabel('Average Biodegradability Score')
        axes[0, 0].set_title('Biodegradability by Material Type')
        axes[0, 0].grid(True, alpha=0.3)
        
        # Average CO₂ emission by material type
        co2_avg = df.groupby('material_type')['co2_emission_score'].mean().sort_values()
        axes[0, 1].barh(co2_avg.index, co2_avg.values, color='red', alpha=0.7)
        axes[0, 1].set_xlabel('Average CO₂ Emission Score')
        axes[0, 1].set_title('CO₂ Emissions by Material Type')
        axes[0, 1].grid(True, alpha=0.3)
        
        # Average recyclability by material type
        rec_avg = df.groupby('material_type')['recyclability_percent'].mean().sort_values(ascending=False)
        axes[1, 0].barh(rec_avg.index, rec_avg.values, color='blue', alpha=0.7)
        axes[1, 0].set_xlabel('Average Recyclability %')
        axes[1, 0].set_title('Recyclability by Material Type')
        axes[1, 0].grid(True, alpha=0.3)
        
        # Average cost by material type
        cost_avg = df.groupby('material_type')['cost_per_kg'].mean().sort_values()
        axes[1, 1].barh(cost_avg.index, cost_avg.values, color='orange', alpha=0.7)
        axes[1, 1].set_xlabel('Average Cost per kg ($)')
        axes[1, 1].set_title('Cost by Material Type')
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('data/material_comparison.png', dpi=300, bbox_inches='tight')
        print("  ✓ Material comparison plots saved to data/material_comparison.png")
        plt.close()

def generate_quality_report(materials_raw, materials_cleaned, materials_engineered, product_categories):
    """Generate comprehensive data quality report"""
    print("\n" + "="*70)
    print("DATA QUALITY REPORT")
    print("="*70)
    
    report = []
    report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("=" * 70)
    
    # Dataset overview
    report.append("\n1. DATASET OVERVIEW")
    report.append(f"   Raw Materials: {len(materials_raw)} records, {materials_raw.shape[1]} columns")
    report.append(f"   Cleaned Materials: {len(materials_cleaned)} records, {materials_cleaned.shape[1]} columns")
    report.append(f"   Engineered Materials: {len(materials_engineered)} records, {materials_engineered.shape[1]} columns")
    report.append(f"   Product Categories: {len(product_categories)} records, {product_categories.shape[1]} columns")
    
    # Completeness
    report.append("\n2. DATA COMPLETENESS")
    complete_raw = validate_completeness(materials_raw, "Raw Materials")
    complete_cleaned = validate_completeness(materials_cleaned, "Cleaned Materials")
    complete_engineered = validate_completeness(materials_engineered, "Engineered Materials")
    complete_categories = validate_completeness(product_categories, "Product Categories")
    
    report.append(f"   Raw: {complete_raw:.2f}%")
    report.append(f"   Cleaned: {complete_cleaned:.2f}%")
    report.append(f"   Engineered: {complete_engineered:.2f}%")
    report.append(f"   Categories: {complete_categories:.2f}%")
    
    # Consistency
    report.append("\n3. DATA CONSISTENCY")
    validate_consistency(materials_cleaned)
    
    # Accuracy
    report.append("\n4. DATA ACCURACY")
    validate_accuracy(materials_cleaned)
    
    # Feature summary
    report.append("\n5. ENGINEERED FEATURES SUMMARY")
    engineered_features = [col for col in materials_engineered.columns 
                          if col not in materials_raw.columns]
    report.append(f"   New features created: {len(engineered_features)}")
    report.append(f"   Features: {', '.join(engineered_features[:10])}")
    
    # Save report
    report_text = '\n'.join(report)
    with open('data/data_quality_report.txt', 'w') as f:
        f.write(report_text)
    
    print("\n✓ Quality report saved to data/data_quality_report.txt")
    print(report_text)

def main():
    """Main validation function"""
    print("="*70)
    print("EcoPackAI Data Validation & Quality Report Generator")
    print("="*70)
    
    # Load all datasets
    materials_raw, materials_cleaned, materials_engineered, product_categories = load_data()
    
    # Create visualizations
    create_distribution_plots(materials_cleaned)
    create_correlation_heatmap(materials_cleaned)
    create_material_comparison_plot(materials_cleaned)
    
    # Generate quality report
    generate_quality_report(materials_raw, materials_cleaned, materials_engineered, product_categories)
    
    print("\n" + "="*70)
    print("✓ Data validation completed successfully!")
    print("  Generated outputs:")
    print("    - data/distribution_plots.png")
    print("    - data/correlation_heatmap.png")
    print("    - data/material_comparison.png")
    print("    - data/data_quality_report.txt")
    print("="*70)

if __name__ == "__main__":
    main()
