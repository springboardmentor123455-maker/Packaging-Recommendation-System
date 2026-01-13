from flask import Flask
from flask_cors import CORS
from routes.recommendation_routes import recommendation_bp

app = Flask(__name__)
CORS(app)

# Register blueprint
app.register_blueprint(recommendation_bp)

@app.route("/")
def home():
    return {"status": "Backend is running"}

if __name__ == "__main__":
    app.run(debug=True)
