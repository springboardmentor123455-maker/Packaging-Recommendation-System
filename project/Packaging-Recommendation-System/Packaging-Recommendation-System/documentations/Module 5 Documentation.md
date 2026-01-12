EcoPackAI – Module 5
Flask Backend API

Module 5 implements the backend REST API for EcoPackAI, providing secure, scalable services for product management, material ingestion, AI-driven material recommendations, and environmental score computation using Flask + PostgreSQL + ML models.

🚀 Features

RESTful APIs for:

Product management

Material candidate ingestion

AI-based material recommendation

Environmental score calculation

Secure endpoints using API Key authentication

PostgreSQL database integration via SQLAlchemy

Automatic table creation and auto-add missing columns

Machine Learning model integration:

Random Forest → Cost prediction

XGBoost → CO₂ emission prediction

Consistent JSON response structure

CORS enabled for frontend integration

🛠 Tech Stack

Backend Framework: Flask

Database: PostgreSQL

ORM: SQLAlchemy

ML Models: scikit-learn (Random Forest), XGBoost

Data Processing: Pandas

Security: API Key-based authentication

📂 Project Structure
module5_api.py
rf_cost_model.pkl
xgb_co2_model.pkl
README.md

⚙️ Configuration

Environment variables (optional):

Variable	Description	Default
API_KEY	API authentication key	super
DATABASE_URL	PostgreSQL connection URL	postgresql://postgres:pass@localhost:5432/postgres
RF_COST_MODEL_PATH	Cost prediction model	rf_cost_model.pkl
XGB_CO2_MODEL_PATH	CO₂ prediction model	xgb_co2_model.pkl
COST_WEIGHT	Ranking weight for cost	0.5
CO2_WEIGHT	Ranking weight for CO₂	0.5
PORT	Flask port	5000
🧪 Database Tables

products

material_candidates

recommendation_records

environmental_scores

Tables and missing columns are automatically created/updated at startup.

🔐 Authentication

All protected endpoints require an API key in headers:

X-API-Key: super

📌 API Endpoints
Health Check

GET /api/health

Products
Create Product

POST /api/products

{
  "name": "Food Container",
  "description": "Eco-friendly packaging",
  "max_cost_per_kg_usd": 3.5,
  "max_co2_emission_kgCO2_per_kg": 1.2
}

List Products

GET /api/products

Materials
Add Material Candidates

POST /api/materials

{
  "materials": [
    {
      "name": "PLA",
      "material_type": "Bioplastic",
      "material_subtype": "PLA",
      "strength_MPa": 60,
      "weight_capacity_kg": 10,
      "density_g_per_cm3": 1.25,
      "biodegradability_score": 8,
      "recyclability_percentage": 70,
      "material_suitability_score": 9
    }
  ]
}

List Materials

GET /api/materials

AI Material Recommendation

POST /api/recommendations/materials

{
  "product_id": 1,
  "weights": {
    "cost": 0.6,
    "co2": 0.4
  }
}


Response includes:

Predicted cost

Predicted CO₂

Ranking score (lower = better)

Environmental Score

POST /api/score/environmental

{
  "material_name": "PLA",
  "co2_kgCO2_per_kg": 1.2,
  "recyclability_percentage": 70,
  "biodegradability_score": 8
}


Scoring Logic

CO₂ impact (60%)

Recyclability (30%)

Biodegradability (10%)

Score range: 0–100

▶️ Running the Server
python module5_api.py


Server will start at:

http://localhost:5000
