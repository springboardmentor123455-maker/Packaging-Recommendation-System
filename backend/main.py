import os
import joblib
import pandas as pd
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine

# # --- CONFIGURATION ---
# DB_USER = "postgres"
# DB_PASS = "0816"   # <--- Your Password
# DB_NAME = "ecopack_db"
# DB_HOST = "localhost"
DATABASE_URL = os.getenv("postgresql://neondb_owner:npg_wLV9zEcHyZ8h@ep-little-sun-ah1ijpio-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require")

# Ensure the engine uses this new URL
engine = create_engine(DATABASE_URL)
# --- LOAD ML MODELS (The "Brains") ---
# We load them once at startup so we don't waste time reloading for every request
# --- LOAD ML MODELS ---
try:
    cost_model = joblib.load('model_cost_rf.pkl')  # Updated Name
    co2_model = joblib.load('model_co2_xgb.pkl')   # Updated Name
    scaler = joblib.load('feature_scaler.pkl')
    print("✅ ML Models (RF & XGBoost) loaded successfully.")
except Exception as e:
    print(f"⚠️ Warning: Could not load ML models. {e}")

# Initialize App
app = FastAPI(title="EcoPackAI API", description="AI-Powered Packaging Recommender & Predictor")

# Database Connection
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}"
engine = create_engine(DATABASE_URL)

# --- INPUT MODELS ---

# 1. For Recommendations (User Priorities)
class RecommendationRequest(BaseModel):
    industry: str
    priority_eco: float
    priority_cost: float
    priority_strength: float

# 2. For Prediction (Raw Material Specs)
class PredictionRequest(BaseModel):
    tensile_strength: float
    weight_capacity: float
    biodegradability_score: int
    recyclability_percent: int
    material_type_encoded: int  # User sends 0, 1, 2 (Front-end will handle the mapping)

# --- API ENDPOINTS ---

@app.get("/")
def home():
    return {"message": "EcoPackAI is running!"}

@app.post("/recommend")
def get_recommendations(request: RecommendationRequest):
    """ Returns ranked materials from the Database based on priorities. """
    try:
        query = "SELECT * FROM processed_materials"
        df = pd.read_sql(query, engine)
        
        mask = df['suitable_industries'].str.contains(request.industry, case=False, na=False)
        df_filtered = df[mask].copy()
        
        if df_filtered.empty:
            return {"status": "error", "message": f"No materials found for industry: {request.industry}"}

        df_filtered['final_score'] = (
            (request.priority_eco * df_filtered['co2_impact_index']) + 
            (request.priority_cost * df_filtered['cost_efficiency_index']) + 
            (request.priority_strength * df_filtered['durability_index'])
        )

        recommendations = df_filtered.sort_values(by='final_score', ascending=False).head(5)
        
        return {
            "industry_requested": request.industry,
            "top_recommendations": recommendations[['material_name', 'final_score', 'price_inr_per_unit', 'co2_emission_score']].to_dict(orient='records')
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict_impact")
def predict_impact(request: PredictionRequest):
    """ 
    Uses Random Forest & XGBoost Models to predict Cost and CO2.
    """
    if not cost_model or not scaler:
        raise HTTPException(status_code=500, detail="ML Models are not loaded on the server.")

    try:
        # 1. Prepare Input Array
        input_data = np.array([[
            request.tensile_strength,
            request.weight_capacity,
            request.biodegradability_score,
            request.recyclability_percent,
            request.material_type_encoded
        ]])

        # 2. Scale the Input
        input_scaled = scaler.transform(input_data)

        # 3. Predict
        # ERROR FIX: Convert numpy result to standard Python float using float()
        predicted_cost = float(cost_model.predict(input_scaled)[0])
        predicted_co2 = float(co2_model.predict(input_scaled)[0])

        return {
            "status": "success",
            "input_summary": {
                "strength": request.tensile_strength,
                "recyclability": f"{request.recyclability_percent}%"
            },
            "predictions": {
                "estimated_cost_inr": round(predicted_cost, 2),
                "estimated_co2_emission": round(predicted_co2, 2)
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction Error: {str(e)}")
    
