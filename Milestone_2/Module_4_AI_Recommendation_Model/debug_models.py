import joblib
import os
import sys

MODEL_DIR = "models"

def check_models():
    print("Checking models in", os.path.abspath(MODEL_DIR))
    files = ["cost_model.pkl", "co2_model.pkl", "cost_preprocessor.pkl", "co2_preprocessor.pkl"]
    for f in files:
        path = os.path.join(MODEL_DIR, f)
        if not os.path.exists(path):
            print(f"MISSING: {path}")
            continue
            
        print(f"Loading {f}...")
        try:
            obj = joblib.load(path)
            print(f"  SUCCESS: Loaded {type(obj)}")
        except Exception as e:
            print(f"  FAIL: {e}")

if __name__ == '__main__':
    check_models()
