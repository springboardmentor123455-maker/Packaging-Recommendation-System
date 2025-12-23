import pandas as pd
import numpy as np
import joblib
import os
from ml_preparation import load_data_from_db

MODEL_DIR = "models"

class RecommendationEngine:
    def __init__(self):
        self.cost_model = None
        self.co2_model = None
        self.cost_preprocessor = None
        self.co2_preprocessor = None
        self.load_artifacts()

    def load_artifacts(self):
        try:
            self.cost_model = joblib.load(os.path.join(MODEL_DIR, "cost_model.pkl"))
            self.co2_model = joblib.load(os.path.join(MODEL_DIR, "co2_model.pkl"))
            self.cost_preprocessor = joblib.load(os.path.join(MODEL_DIR, "cost_preprocessor.pkl"))
            self.co2_preprocessor = joblib.load(os.path.join(MODEL_DIR, "co2_preprocessor.pkl"))
            print("All models and preprocessors loaded successfully.")
        except FileNotFoundError as e:
            print(f"Error loading artifacts: {e}. Please run train_models.py first.")

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
            return []

        # Filter by hard constraints first
        candidates = df[df['strength'] >= required_strength].copy()
        
        if candidates.empty:
            print("No materials meet the strength requirement.")
            return []

        # In a real scenario, we might want to predict values for *hypothetical* materials or 
        # just use the actual values in the DB. 
        # Since the task is "AI Recommendation", we often use the model to predict/verify 
        # or to rank materials where we might have missing data (imputed) or if we are generating new material concepts.
        # BUT, for this specific milestone, let's use the models to "score" the candidates 
        # (or assume we are simulating a scenario where we don't know the exact cost/co2 yet, 
        # e.g., for a new batch, but here we do have them in DB).
        
        # Let's use the PREDICTED values for ranking to demonstrate the ML capability.
        # This simulates "what would the model think this material costs/pollutes?" 
        # (Useful if the DB values were old or estimates).
        
        # Prepare data for prediction (drop targets as we are predicting them)
        # The preprocessor expects columns present in training.
        # Training had: 'strength', 'weight_capacity', 'biodegradability_score'..., 'material_type'
        # And checks dropped 'cost_per_kg', 'co2_emission_score'.
        
        # So we pass the candidates dataframe. The preprocessor will handle it.
        # Wait, prepare_data drops target columns. The preprocessor.transform expects the dataframe *without* drops?
        # No, preprocessor (ColumnTransformer) selects columns by name. 
        # As long as the DF has the feature columns, it's fine.
        
        try:
            X_cost_candidates = self.cost_preprocessor.transform(candidates)
            candidates['predicted_cost'] = self.cost_model.predict(X_cost_candidates)
            
            X_co2_candidates = self.co2_preprocessor.transform(candidates)
            candidates['predicted_co2'] = self.co2_model.predict(X_co2_candidates)
            
        except Exception as e:
            print(f"Error during prediction for recommendation: {e}")
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
            
        return recommendations[['material_name', 'material_type', 'strength', 'predicted_cost', 'predicted_co2', 'rank_score']]

if __name__ == "__main__":
    engine = RecommendationEngine()
    print("\n--- Testing Recommendation Engine ---")
    recs = engine.recommend_materials(required_strength=50.0)
    if not recs.empty:
        print("\nTop 5 Recommendations for Strength >= 50kg/cm²:")
        print(recs.head())
    else:
        print("No recommendations found.")
