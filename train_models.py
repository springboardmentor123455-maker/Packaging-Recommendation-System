from ml_preparation import load_data_from_db, prepare_data
from ml_models import CostPredictor, CO2Predictor
import joblib
import os

MODEL_DIR = "models"
if not os.path.exists(MODEL_DIR):
    os.makedirs(MODEL_DIR)

def run_training():
    df = load_data_from_db()
    if df is None:
        print("Failed to load data. Exiting.")
        return

    # Train Cost Predictor
    print("\n=== Training Cost Predictor (Random Forest) ===")
    X_train_cost, X_test_cost, y_train_cost, y_test_cost, preproc_cost = prepare_data(df, target_col='cost_per_kg')
    
    # We must fit the preprocessor on training data and transform both train and test
    X_train_cost_processed = preproc_cost.fit_transform(X_train_cost)
    X_test_cost_processed = preproc_cost.transform(X_test_cost)
    
    cost_model = CostPredictor()
    cost_model.model.fit(X_train_cost_processed, y_train_cost) # Accessing underlying sklearn model directly for now to use preprocessed data
    # Actually, the BasePredictor.train takes X_train, y_train. Let's use that.
    # But wait, BasePredictor.train calls model.fit.
    # I should update BasePredictor to maybe handle pipelines, but for now passing processed data is fine.
    
    # Better yet, let's include the preprocessor in the final saved object or save it separately.
    # Standard practice: Save the preprocessor separately or make a Pipeline.
    # Since ml_models classes wrap the regressor, let's just save the preprocessor separately.
    
    joblib.dump(preproc_cost, os.path.join(MODEL_DIR, "cost_preprocessor.pkl"))
    print("Cost preprocessor saved.")

    cost_model.train(X_train_cost_processed, y_train_cost)
    cost_model.evaluate(X_test_cost_processed, y_test_cost)
    cost_model.save_model(os.path.join(MODEL_DIR, "cost_model.pkl"))

    # Train CO2 Predictor
    print("\n=== Training CO2 Predictor (XGBoost) ===")
    X_train_co2, X_test_co2, y_train_co2, y_test_co2, preproc_co2 = prepare_data(df, target_col='co2_emission_score')
    
    X_train_co2_processed = preproc_co2.fit_transform(X_train_co2)
    X_test_co2_processed = preproc_co2.transform(X_test_co2)
    
    joblib.dump(preproc_co2, os.path.join(MODEL_DIR, "co2_preprocessor.pkl"))
    print("CO2 preprocessor saved.")

    co2_model = CO2Predictor()
    co2_model.train(X_train_co2_processed, y_train_co2)
    co2_model.evaluate(X_test_co2_processed, y_test_co2)
    co2_model.save_model(os.path.join(MODEL_DIR, "co2_model.pkl"))

if __name__ == "__main__":
    run_training()
