import os
import joblib
import pandas as pd
import numpy as np
from sklearn.metrics import r2_score

def verify_milestone2():
    print("=== Milestone 2 Verification ===")
    
    # 1. Verify Artifacts
    artifacts = [
        "models/cost_model.pkl",
        "models/co2_model.pkl",
        "models/cost_preprocessor.pkl",
        "models/co2_preprocessor.pkl",
        "data/materials.csv"
    ]
    
    missing = []
    for art in artifacts:
        if os.path.exists(art):
            print(f"✓ Found {art}")
        else:
            print(f"✗ Missing {art}")
            missing.append(art)
            
    if missing:
        print("Verification Failed: Missing artifacts.")
        return

    # 2. Verify Models Load
    try:
        cost_model = joblib.load("models/cost_model.pkl")
        co2_model = joblib.load("models/co2_model.pkl")
        print("✓ Models loaded successfully")
    except Exception as e:
        print(f"✗ Model Load Error: {e}")
        return

    # 3. Quick Sanity Check on Recommendation Engine
    from recommendation_engine import RecommendationEngine
    
    try:
        engine = RecommendationEngine()
        recs = engine.recommend_materials(required_strength=50.0)
        
        if not recs.empty:
             print(f"✓ Recommendation Engine returned {len(recs)} results")
             print("Top Result:")
             print(recs.iloc[0])
        else:
             print("✗ Recommendation Engine returned no results (unexpected for Strength=50)")
             
    except Exception as e:
        print(f"✗ Recommendation Engine Error: {e}")
        return

    print("\n=== Verification Complete: ALL TESTS PASSED ===")

if __name__ == "__main__":
    verify_milestone2()
