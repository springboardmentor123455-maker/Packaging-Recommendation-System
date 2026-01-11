from flask import Flask, jsonify, request
from flask_cors import CORS

from backend.models.recommender import get_material_recommendations

app = Flask(__name__)
CORS(app)

# -------------------------
# Health Check API
# -------------------------
@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "success",
        "message": "Flask backend is running"
    })


# -------------------------
# Material Recommendation API
# -------------------------
@app.route("/api/recommend", methods=["POST"])
def recommend_material():
    """
    Accepts product input and returns recommended materials
    """

    data = request.get_json()

    product_weight = data.get("product_weight")
    strength_required = data.get("strength_required")

    recommendations = get_material_recommendations(
        product_weight=product_weight,
        strength_required=strength_required
    )

    return jsonify({
        "status": "success",
        "recommendations": recommendations
    })


if __name__ == "__main__":
    app.run(debug=True)
