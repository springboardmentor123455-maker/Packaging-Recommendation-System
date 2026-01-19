from flask import request, jsonify
from functools import wraps

API_KEY = "ECO2025"

def require_key(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        key = request.headers.get("x-api-key")
        if key != API_KEY:
            return jsonify({"error": "Unauthorized"}), 403
        return func(*args, **kwargs)
    return wrapper
