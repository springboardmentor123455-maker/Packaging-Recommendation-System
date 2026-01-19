import pandas as pd
import numpy as np
import joblib
import os
from ml_preparation import load_data_from_db

MODEL_DIR = "models"

class RecommendationEngine:
    def __init__(self, model_dir=None):
        self.model_dir = model_dir if model_dir else MODEL_DIR
        self.cost_model = None
        self.co2_model = None
        self.cost_preprocessor = None
        self.co2_preprocessor = None
        self.load_artifacts()

    def load_artifacts(self):
        try:
            self.cost_model = joblib.load(os.path.join(self.model_dir, "cost_model.pkl"))
            self.co2_model = joblib.load(os.path.join(self.model_dir, "co2_model.pkl"))
            self.cost_preprocessor = joblib.load(os.path.join(self.model_dir, "cost_preprocessor.pkl"))
            self.co2_preprocessor = joblib.load(os.path.join(self.model_dir, "co2_preprocessor.pkl"))
            print(f"All models and preprocessors loaded successfully from {self.model_dir}.")
        except FileNotFoundError as e:
            print(f"Error loading artifacts from {self.model_dir}: {e}. Please run train_models.py first.")

    def predict_material_metrics(self, material_data):
        """
        Predicts Cost and CO2 for a list of material dictionaries.
        """
        if not self.cost_model or not self.co2_model:
            return None

        # Convert to DataFrame
        df = pd.DataFrame(material_data)
        
        # Preprocess features (ensure columns match what was used in training)
        # Note: input data must have same schema as DB training data minus target columns
        
        # Transform for Cost Model
        try:
            X_cost = self.cost_preprocessor.transform(df)
            predicted_cost = self.cost_model.predict(X_cost)
        except Exception as e:
            print(f"Prediction error (Cost): {e}")
            return None

        # Transform for CO2 Model
        try:
            X_co2 = self.co2_preprocessor.transform(df)
            predicted_co2 = self.co2_model.predict(X_co2)
        except Exception as e:
             print(f"Prediction error (CO2): {e}")
             return None

        return predicted_cost, predicted_co2

    def recommend_materials(self, required_strength, max_cost=None, max_co2=None):
        """
        Recommends materials from the database that meet criteria, ranked by a composite score.
        """
        df = load_data_from_db()
        if df is None:
            print("DEBUG: load_data_from_db returned None")
            return []
        
        print(f"DEBUG: Loaded DataFrame with shape: {df.shape}")
        # print(f"DEBUG: Columns: {df.columns.tolist()}")

        # Filter by hard constraints first
        print(f"DEBUG: Filtering for strength >= {required_strength}")
        candidates = df[df['strength'] >= required_strength].copy()
        
        print(f"DEBUG: Candidates after filter: {len(candidates)}")
        
        if candidates.empty:
            print("No materials meet the strength requirement.")
            return []

        try:
            X_cost_candidates = self.cost_preprocessor.transform(candidates)
            candidates['predicted_cost'] = self.cost_model.predict(X_cost_candidates)
            
            X_co2_candidates = self.co2_preprocessor.transform(candidates)
            candidates['predicted_co2'] = self.co2_model.predict(X_co2_candidates)
            
        except Exception as e:
            print(f"Error during prediction for recommendation: {e}")
            import traceback
            traceback.print_exc()
            return []

        # Ranking Logic
        # Normalize to 0-1 scale for combination
        # Lower cost and lower CO2 is better.
        
        # Handle min=max case to avoid division by zero
        cost_range = candidates['predicted_cost'].max() - candidates['predicted_cost'].min()
        co2_range = candidates['predicted_co2'].max() - candidates['predicted_co2'].min()
        
        if cost_range == 0: cost_range = 1
        if co2_range == 0: co2_range = 1

        candidates['norm_cost'] = (candidates['predicted_cost'] - candidates['predicted_cost'].min()) / cost_range
        candidates['norm_co2'] = (candidates['predicted_co2'] - candidates['predicted_co2'].min()) / co2_range
        
        # Composite Score: Weight Cost (40%) and CO2 (60%) - user can adjust
        # We want to MINIMIZE this score (since lower cost/co2 is better)
        candidates['rank_score'] = (0.4 * candidates['norm_cost']) + (0.6 * candidates['norm_co2'])
        
        # Create recommendation list
        recommendations = candidates.sort_values('rank_score', ascending=True)
        
        # Apply optional filters
        if max_cost:
            recommendations = recommendations[recommendations['predicted_cost'] <= max_cost]
        if max_co2:
            recommendations = recommendations[recommendations['predicted_co2'] <= max_co2]
            
        return recommendations[['material_name', 'material_type', 'strength', 'predicted_cost', 'predicted_co2', 'rank_score', 
                                'biodegradability_score', 'recyclability_percent', 'water_resistance', 'temperature_tolerance', 
                                'weight_capacity', 'thickness_mm']]

if __name__ == "__main__":
    engine = RecommendationEngine()
    print("\n--- Testing Recommendation Engine ---")
    recs = engine.recommend_materials(required_strength=50.0)
    if not recs.empty:
        print("\nTop 5 Recommendations for Strength >= 50kg/cm²:")
        print(recs.head())
    else:
        print("No recommendations found.")
