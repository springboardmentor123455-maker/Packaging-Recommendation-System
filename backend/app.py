from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

# Base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Path to final recommendations CSV
DATA_PATH = os.path.join(BASE_DIR, "data", "final_recommendations.csv")


@app.route("/")
def home():
    return jsonify({
        "status": "EcoPackAI Backend is running",
        "message": "Use /api/recommendations to get results"
    })


@app.route("/api/recommendations", methods=["GET"])
def get_recommendations():
    try:
        if not os.path.exists(DATA_PATH):
            return jsonify({"error": "final_recommendations.csv not found"}), 404

        df = pd.read_csv(DATA_PATH)

        # Convert dataframe to JSON
        data = df.to_dict(orient="records")

        return jsonify({
            "count": len(data),
            "recommendations": data
        })

    except Exception as e:
        return jsonify({
            "error": "Failed to load recommendations",
            "details": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)
