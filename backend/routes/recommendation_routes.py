from flask import Blueprint, request, jsonify
from utils.ai_model import recommend_material

recommendation_bp = Blueprint("recommendation", __name__)

@recommendation_bp.route("/predict", methods=["POST"])
def predict():
    data = request.json

    weight = float(data.get("weight"))
    volume = float(data.get("volume"))
    fragility = int(data.get("fragility"))

    result = recommend_material(weight, volume, fragility)

    return jsonify(result)
