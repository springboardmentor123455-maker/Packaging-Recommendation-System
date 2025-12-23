# EcoPackAI - Sustainable Packaging Recommendation System

## Project Overview

An AI-powered platform for recommending eco-friendly packaging materials based on product attributes and sustainability parameters.

## Implementation Status

**Milestone 1 (Week 1-2): Complete**
- Data collection and management
- Data cleaning and preprocessing
- Feature engineering
- Validation and quality assurance

## Dataset Summary

### Materials Dataset
- **Total Records**: 1200
- **Material Types**: 15 eco-friendly packaging types
- **Parameters**: 11 core attributes per material

### Product Categories
- **Total Categories**: 12
- **Coverage**: Electronics, Food, Cosmetics, Pharmaceuticals, etc.

## Key Features

### Engineered Metrics
1. **CO₂ Impact Index** - Environmental impact score (0-100)
2. **Cost Efficiency Index** - Value for money metric (0-100)
3. **Material Suitability Score** - Composite sustainability rating (0-100)
4. **Sustainability Rating** - 1-5 star environmental grade

### Data Quality
- Completeness: 100%
- Missing values: Handled via median imputation
- Normalization: StandardScaler and MinMaxScaler applied
- Total features: 28 (11 original + 17 engineered)

## Project Structure

```
infosys/
├── data/
│   ├── materials.csv                    # Raw materials data (1200 records)
│   ├── product_categories.csv           # Product categories (12 types)
│   ├── materials_cleaned.csv            # Preprocessed dataset
│   ├── materials_engineered.csv         # Feature-engineered dataset
│   ├── distribution_plots.png           # Data visualizations
│   ├── correlation_heatmap.png          # Feature correlation analysis
│   └── material_comparison.png          # Material type comparisons
│
├── generate_materials_data.py           # Data generation script
├── generate_product_categories.py       # Category generation script
├── data_cleaning.py                     # Data preprocessing pipeline
├── feature_engineering.py               # Feature creation pipeline
├── data_validation.py                   # Quality validation script
├── setup_database.py                    # PostgreSQL setup script
├── database_schema.sql                  # Database schema definition
├── validate_week1_2.py                  # Automated validation
└── requirements.txt                     # Dependencies
```

## Setup and Execution

### Dependencies
```bash
pip install pandas numpy scikit-learn matplotlib seaborn psycopg2-binary faker scipy
```

### Running the Pipeline
```bash
# Generate datasets
python generate_materials_data.py
python generate_product_categories.py

# Process and engineer features
python data_cleaning.py
python feature_engineering.py

# Validate results
python data_validation.py
python validate_week1_2.py
```

## Results

### Top Sustainable Materials (by Suitability Score)
1. Recycled Paper Grade Standard - 79.11 (5 stars)
2. Recycled Paper Grade Economy - 78.73 (5 stars)
3. Hemp Packaging Grade Economy - 78.40 (4 stars)
4. Recycled Paper Grade C - 77.73 (4 stars)
5. Recycled Paper Grade A - 77.64 (4 stars)

### Material Type Distribution
All 15 material types contain 80 records each for balanced representation:
- Cardboard, Kraft Paper, Biodegradable Plastic
- Mushroom Packaging, Cornstarch Packaging
- Recycled Paper, Bamboo Fiber, Hemp Packaging
- Seaweed Packaging, Glass, Aluminum
- Recycled Plastic, Wood Fiber, Cotton Packaging, Jute Packaging

## Technical Implementation

### Data Cleaning
- Missing value imputation using median strategy
- Outlier detection via Z-score and IQR methods
- Feature normalization and standardization
- Categorical encoding (Label Encoding for material types)

### Feature Engineering Formulas

**CO₂ Impact Index:**
```
= (CO₂_Emission × 0.6) + ((100 - Recyclability) × 0.4)
Normalized to 0-100 scale (lower is better)
```

**Cost Efficiency Index:**
```
= (Strength / Cost) × (Weight_Capacity / Cost)
Normalized to 0-100 scale (higher is better)
```

**Material Suitability Score:**
```
= (Biodegradability × 0.3) + (Recyclability × 0.25) + 
  ((100 - CO₂_Impact) × 0.25) + (Strength_Normalized × 0.2)
```

## Database Schema

PostgreSQL database ready for deployment with:
- `materials_data` table - All material attributes
- `product_categories` table - Category specifications
- `packaging_recommendations` table - ML prediction storage
- Indexed columns for performance optimization

