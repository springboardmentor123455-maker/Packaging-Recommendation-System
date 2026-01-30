# Packaging Recommendation System  
## AI Framework for Sustainable Packaging Design and Material Optimization  

**Project Type:** Infosys Virtual Internship  
**Duration:** 6 Weeks (Milestone 1-3)  
**Completion Date:** January 2026  
**Technology Stack:** Python, MySQL, Flask, Machine Learning  

---

## Executive Summary  

The Packaging Recommendation System is an AI-powered web application that helps users select optimal packaging materials based on product characteristics, cost constraints, and environmental impact. The system uses machine learning and AI-based ranking logic to predict cost and CO₂ impact, then generates a ranked recommendation list from the processed material dataset.

**Key Achievements:**  
- Processed dataset with **10,000 materials records** and engineered features (59 columns)  
- High ML performance (R² score up to **0.99998**)  
- Flask backend API integration with frontend UI (`/predict`)  
- Dynamic recommendation output and ranking table shown in web interface  

---

## Project Architecture  

### System Components  

```
┌──────────────────────────────────────────────────────────┐
│                 Web Interface (Frontend)                 │
│              HTML + CSS + JavaScript                     │
│     (Input Form + Best Recommendation + Ranking Table)   │
└──────────────────────────┬───────────────────────────────┘
                           │ HTTP/JSON
                           │ POST /predict
┌──────────────────────────▼───────────────────────────────┐
│                 Flask Backend API                         │
│     Flask + CORS + Blueprint Routes + JSON Responses      │
│   app.py -> recommendation_routes.py -> ai_model.py       │
└───────────────┬───────────────────────────┬──────────────┘
                │                           │
┌───────────────▼───────────────┐   ┌──────▼──────────────┐
│     AI / ML Recommendation     │   │      MySQL DB        │
│  (eco_score + cost index rank) │   │  eco_packaging DB    │
│  Reads cleaned_materials.csv   │   │  product table model │
└───────────────────────────────┘   └──────────────────────┘
```

---

## Module Breakdown  

### Milestone 1: Data Collection & Preparation  

#### Module 1: Data Collection and Management  
**Objective:** Establish database infrastructure and manage packaging materials dataset.

**Implementation:**  
- Used packaging materials dataset containing attributes like:
  - Material type, strength, weight capacity
  - Biodegradability score
  - CO₂ emission score
  - Recyclability percentage
  - Price (INR)
- Loaded dataset using `pandas`
- Connected Python with **MySQL**
- Created tables and inserted data for structured management

**Results:**  
- Dataset stored successfully in database  
- Dataset size: **10,000 rows × 12 columns**  

---

#### Module 2: Data Cleaning & Feature Engineering  
**Objective:** Clean dataset and generate derived ML-ready features.

**Data Cleaning:**  
- Missing values handled
- Data types standardized
- Dataset made consistent for training

**Feature Engineering:**  
- Encoding of categorical columns
- Generated engineered indexes such as:
  - Cost efficiency type index
  - Environmental impact based score
  - Overall suitability-based scoring features

**Results:**  
- Cleaned dataset created successfully  
- Final dataset size: **10,000 rows × 59 columns**  

---

### Milestone 2: Machine Learning Models  

#### Module 3: Machine Learning Dataset Preparation  
**Objective:** Prepare the dataset for ML model training/testing.

**Data Pipeline:**  
- Loaded cleaned dataset
- Feature selection (X) and target columns (y)
- Train-test split
- Scaling / preprocessing pipeline where required

**Results:**  
- Training and testing dataset prepared successfully  
- Dataset ready for model training  

---

#### Module 4: ML Prediction Models & Ranking System  
**Objective:** Train ML models and build AI ranking-based recommendation system.

**Models Used:**  
1. **Random Forest Regressor** (Cost prediction)  
2. **XGBoost Regressor** (CO₂ prediction)  

**Model Evaluation Metrics:**  
- RMSE  
- MAE  
- R² Score  

**Actual Evaluation Results:**  

✅ **Random Forest (Cost Prediction)**  
- RMSE: **0.03425175**  
- MAE: **0.01396171**  
- R² Score: **0.98610537**  

✅ **XGBoost (CO₂ Prediction)**  
- RMSE: **0.00118505**  
- MAE: **0.00099652**  
- R² Score: **0.99998250**  

**Results:**  
- High accuracy cost and CO₂ prediction achieved  
- AI-based ranking table generated successfully  
- Best material recommendation generated  

---

### Milestone 3: Backend & Frontend  

#### Module 5: Flask Backend API  
**Objective:** Serve ML-based recommendations through API for frontend.

**Backend Structure Implemented:**  
- Flask app with:
  - `CORS` enabled
  - Blueprint-based routing
- Main routes:
  - Status route `/`
  - Prediction route `/predict`

**API Endpoints:**  

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/` | Backend health/status |
| POST | `/predict` | Returns best recommended material + ranking |

**Backend Features:**  
- JSON request/response support
- Modular routing (Blueprint)
- AI recommendation logic separated into utility module
- Database model created for storing product records

**Example Request:**  
```json
POST /predict
{
  "weight": 2.5,
  "volume": 800,
  "fragility": 4
}
```

**Example Response:**  
```json
{
  "best_material": 101,
  "best_price_inr": 750.50,
  "best_cost_index": 0.652,
  "best_eco_score": 98.40,
  "ranking": [
    {
      "material": 101,
      "price_inr": 750.50,
      "cost_index": 0.652,
      "co2": 1.60,
      "eco_score": 98.40
    }
  ]
}
```

**Results:**  
- Backend successfully serves ML predictions to frontend  
- `/predict` returns best material + ranking list dynamically  

---

#### Module 6: Web Interface (Frontend)  
**Objective:** Build user-friendly UI to accept product inputs and show recommendations.

**Technology Used:**  
- HTML5  
- CSS3 (custom styling)  
- JavaScript (Fetch API)

**Frontend Features:**  
1. Input form:
   - Product weight (kg)
   - Product volume (cm³)
   - Fragility level (1–5)
2. Best recommendation display:
   - recommended material id
   - eco-score and cost-related scores
3. Ranking table:
   - list of ranked materials shown dynamically

**Results:**  
- Frontend successfully connects to backend `/predict` endpoint  
- Outputs displayed dynamically in UI  

---

### Milestone 4: Week 7–8  

#### Module 7: Business Intelligence Dashboard  
**Objective:** Build analytics dashboard to visualize sustainability performance and recommendation insights.

**Implementation:**  
- Built sustainability analytics using Python visualization libraries.
- Generated charts to represent:
  - **CO₂ Reduction Percentage**
  - **Cost Savings**
  - **Material Usage Trends**
- Used plotting libraries:
  - `matplotlib` / `plotly` (as per requirement)
- Dashboard visuals prepared using project dataset and prediction results.

**Analytics Included:**  
1. **CO₂ Reduction %** – comparison of CO₂ before/after eco recommendation  
2. **Cost Savings** – cost comparison between normal vs optimized materials  
3. **Material Usage Trends** – usage trend by material type/category  

**Results:**  
- Sustainability dashboard created successfully  
- Charts generated for CO₂ reduction, cost saving, and usage trends  
- Dashboard output ready for project presentation  

---

#### Module 8: Deployment & Documentation  
**Objective:** Deploy the complete system and finalize technical documentation.

**Implementation:**  
- Deployed Flask backend on **Render**
- Connected deployed backend to **MySQL database**
- Verified deployed system:
  - Backend API running online
  - MySQL connection working
  - Frontend connected to deployed backend

**Deployment Tasks Completed:**  
1. Render Web Service setup (Flask backend)  
2. Configured environment variables for DB credentials  
3. Connected MySQL cloud DB in Render deployment  
4. Production server started successfully  
5. Tested API endpoints (`/predict`) after deployment  

**Documentation Completed:**  
- Technical documentation (`Project_Documentation.md`)
- GitHub README (`README.md`)

*(Report + video demo will be done later as per requirement.)*

**Results:**  
- ✅ Project deployed successfully on Render  
- ✅ MySQL database connected successfully  
- ✅ Deployed `/predict` API working correctly  
- ✅ Documentation and README completed  

---

## Technical Implementation  

### File Structure (As implemented)  

```
Packaging-Recommendation-System/
├── .venv/
│
├── backend/
│   ├── __pycache__/
│   ├── databases/
│   │   ├── dashboard_report.xlsx
│   │   ├── recommendation_history.csv
│   │   └── sustainability_report.xlsx
│   │
│   ├── routes/
│   │   ├── __pycache__/
│   │   ├── dashboard_routes.py
│   │   ├── product_routes.py
│   │   └── recommendation_routes.py
│   │
│   ├── utils/
│   │   ├── __pycache__/
│   │   ├── ai_model.py
│   │   ├── env_score.py
│   │   └── history_logger.py
│   │
│   ├── app.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   └── requirements.txt
│
├── databases/
│   ├── import.sql
│   ├── recommendation_history.csv
│   ├── schema.sql
│   └── validation.sql
│
├── dataset/
│   ├── cleaned_materials.csv
│   └── recommendation_history.csv
│
├── frontend/
│   ├── css/
│   │   └── style.css
│   │
│   ├── js/
│   │   ├── app.js
│   │   └── dashboard.js
│   │
│   ├── dashboard.html
│   └── index.html
│
├── notebooks/
│   ├── cleaned_materials.csv
│   ├── data.csv
│   ├── module1.ipynb
│   ├── module2.ipynb
│   ├── module3.ipynb
│   └── module4.ipynb
│
├── Packaging-Recommendation-System/        # (folder)
│
├── AI Framework for Sustainable Packa...   # (PDF/Doc file)
├── Branch_details.xlsx
├── data.csv
├── LICENSE
├── materials_cleaned.csv
├── materials_milestone1_final.csv
├── milestone1_data_preprocessing.ipynb
├── milestone2_model_training.ipynb
├── Packaging_Recommendation_System...      # (Doc file)
├── Project_Documentation_.md
├── README.md
└── requirements.txt

```

### Dependencies (requirements.txt)  

```
Flask==3.1.2
flask-cors==6.0.2
pandas==2.3.3
numpy==2.3.4
scikit-learn==1.8.0
xgboost==3.1.2
joblib==1.5.2
Flask-SQLAlchemy (used via database.py)
pymysql (used in MySQL URI)
```

---

## Results & Performance  

### ML Model Metrics  

| Model | Metric | Value |
|-------|--------|-------|
| Random Forest (Cost) | R² | **0.98610537** |
| Random Forest (Cost) | MAE | **0.01396171** |
| Random Forest (Cost) | RMSE | **0.03425175** |
| XGBoost (CO₂) | R² | **0.99998250** |
| XGBoost (CO₂) | MAE | **0.00099652** |
| XGBoost (CO₂) | RMSE | **0.00118505** |

---

## Challenges & Solutions  

### Challenge 1: Model feature scaling / preprocessing issues  
**Problem:** Model predictions inconsistent when feature pipeline mismatched  
**Solution:** Preprocessing pipeline stabilized using cleaned dataset and engineered features  
**Result:** Stable prediction and correct ranking output  

### Challenge 2: Frontend not displaying output  
**Problem:** UI not updating because response rendering was missing  
**Solution:** Used fetch API + DOM update code in `app.js`  
**Result:** Ranking table and best recommendation now display dynamically  

### Challenge 3: Deployment connection errors  
**Problem:** Database connection errors during deployment  
**Solution:** Configured correct MySQL connection string and environment variables on Render  
**Result:** Deployment worked successfully with live DB connection  

---

## Usage Guide  

### Installation  

```bash
# Install dependencies
pip install -r requirements.txt
```

### Running the System  

```bash
# Start backend
python app.py

# Open frontend
# index.html (use Live Server in VS Code)
```

### Testing Prediction  

```bash
POST http://127.0.0.1:5000/predict
```

---

## Future Enhancements  

1. Add multiple API endpoints (cost, CO₂, materials list)  
2. Improve ranking logic using weighted composite scoring  
3. Store history of recommendations in database  
4. Improve BI dashboard with interactive charts and filters  
5. Add report + project video demonstration  

---

## Conclusion  

The Packaging Recommendation System successfully demonstrates an end-to-end AI pipeline: dataset management, preprocessing, ML model training, ranking-based recommendations, full-stack integration, BI insights and cloud deployment.

**Key Achievements:**  
- ✅ Dataset preprocessing + feature engineering completed  
- ✅ High-performing Random Forest and XGBoost models  
- ✅ Flask backend integration with frontend  
- ✅ Dynamic best recommendation + full ranking output  
- ✅ Deployment completed on Render with MySQL connection  
- ✅ Sustainability analytics dashboard created  

---

## Appendix  

### A. Dataset Statistics  
- Raw dataset: **10,000 rows × 12 columns**  
- Cleaned dataset: **10,000 rows × 59 columns**

### B. Backend Files Summary  
- `app.py` → Flask entry + CORS + blueprint registration  
- `recommendation_routes.py` → `/predict` endpoint  
- `ai_model.py` → ranking logic using eco_score and cost index  
- `config.py` → MySQL connection string  
- `models.py` → Product table model  

---

**Project Completed:** January 2026  

Website Link :- https://packagingrecommendationsystem-1.onrender.com