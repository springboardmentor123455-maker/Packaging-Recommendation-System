from flask import Flask, request, jsonify
from flask_cors import CORS
import model

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return jsonify({"status": "Packaging Recommendation API Running"})

# 🔹 API used by frontend
@app.route("/api/recommend", methods=["POST"])
def recommend():
    product_data = request.json
    recommendations = model.recommend_material(product_data)

    return jsonify({
        "success": True,
        "recommendations": recommendations
    })

# 🔹 API for testing in browser
@app.route("/api/recommend-test")
def recommend_test():
    recommendations = model.recommend_material({})
    return jsonify({
        "success": True,
        "recommendations": recommendations
    })

if __name__ == "__main__":
    app.run(debug=True)
