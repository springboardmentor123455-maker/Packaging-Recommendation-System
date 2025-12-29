# EcoPackAI - Sustainable Packaging Recommendation System

## Project Overview

An AI-powered platform for recommending eco-friendly packaging materials based on product attributes and sustainability parameters.

## Implementation Status

**Milestone 1 (Week 1-2): Complete**
- Data collection and management
- Data cleaning and preprocessing
- Feature engineering
- Validation and quality assurance

**Milestone 2 (Week 3-4): Complete**
- Machine Learning Dataset Preparation
- Train Cost & CO2 Prediction Models (Random Forest, XGBoost)
- Recommendation Engine Development
- Verification & Testing

**Milestone 3 (Week 5-6): Complete**
- Flask Backend API Implementation
- Frontend UI Development (Glassmorphism Design)
- Dynamic Recommendation Interface
- Database Integration

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

### Web Application
- **Modern UI**: Dark-themed, glassmorphism design with responsive layout.
- **Parametrization**: Input product category, strength, and constraints.
- **AI Ranking**: Real-time scoring and ranking of materials using ML models.
- **Visuals**: Progress bars for suitability scores and badges for top ranks.

## Project Structure

```
infosys/
├── app/
│   ├── templates/
│   │   └── index.html               # Main frontend interface
│   ├── static/
│   │   ├── css/style.css            # Custom styling
│   │   └── js/script.js             # Frontend logic
│   ├── __init__.py                  # Flask app factory
│   ├── app.py                       # App entry point (circular dep fixed in run.py)
│   ├── routes.py                    # API Routes
│   └── database.py                  # Database connection logic
│
├── data/
│   ├── materials.csv                # Raw materials data (1200 records)
│   ├── product_categories.csv       # Product categories (12 types)
│   ├── materials_cleaned.csv        # Preprocessed dataset
│   ├── materials_engineered.csv     # Feature-engineered dataset
│   └── ...
│
├── run.py                           # Application startup script
├── ml_models.py                     # ML Model Definitions
├── train_models.py                  # Model Training Script
├── recommendation_engine.py         # Recommendation Logic
├── setup_database.py                # PostgreSQL setup script
├── database_schema.sql              # Database schema definition
└── requirements.txt                 # Dependencies
```

## Setup and Execution

### Dependencies
```bash
pip install pandas numpy scikit-learn matplotlib seaborn psycopg2-binary faker scipy xgboost flask
```

### Running the Pipeline
```bash
# 1. Setup Database
python setup_database.py

# 2. Train ML Models (Required for app)
python train_models.py

# 3. Run Web Application
python run.py
```

Access the application at: **http://127.0.0.1:5001/**

## Results

### Top Sustainable Materials (by Suitability Score)
1. Recycled Paper Grade Standard - 79.11 (5 stars)
2. Recycled Paper Grade Economy - 78.73 (5 stars)
3. Hemp Packaging Grade Economy - 78.40 (4 stars)
4. Recycled Paper Grade C - 77.73 (4 stars)
5. Recycled Paper Grade A - 77.64 (4 stars)

## Database Schema

PostgreSQL database ready for deployment with:
- `materials_data` table - All material attributes
- `product_categories` table - Category specifications
- `packaging_recommendations` table - ML prediction storage
- Indexed columns for performance optimization
