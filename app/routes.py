from flask import render_template, jsonify, request
from app import app
from app.database import get_all_categories
import sys
import os

# Ensure parent directory is in path for imports if not already
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

# Import RecommendationEngine from the parent directory
# We need to be careful about where we run the app from.
# Assuming we run from 'infosys' directory.
try:
    from recommendation_engine import RecommendationEngine
    engine = RecommendationEngine()
except ImportError as e:
    print(f"Error importing RecommendationEngine: {e}")
    engine = None
except Exception as e:
    print(f"Error initializing RecommendationEngine: {e}")
    engine = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/categories', methods=['GET'])
def get_categories():
    categories = get_all_categories()
    return jsonify(categories)

@app.route('/api/recommend', methods=['POST'])
def recommend():
    if not engine:
        return jsonify({'error': 'Recommendation Engine not initialized'}), 500
        
    data = request.json
    
    
    # Extract parameters
    try:
        print(f"DEBUG: Incoming request data: {data}")
        required_strength = float(data.get('strength', 0))
        max_cost = data.get('max_cost')
        max_co2 = data.get('max_co2')
        valid_max_cost = float(max_cost) if max_cost and max_cost != '' else None
        valid_max_co2 = float(max_co2) if max_co2 and max_co2 != '' else None
        
        print(f"DEBUG: Parsed params - Strength: {required_strength}, MaxCost: {valid_max_cost}, MaxCO2: {valid_max_co2}")

        # Get recommendations
        # Note: recommend_materials returns a DataFrame
        recommendations_df = engine.recommend_materials(
            required_strength=required_strength,
            max_cost=valid_max_cost,
            max_co2=valid_max_co2
        )
        
        if recommendations_df.empty:
             print("DEBUG: No recommendations found.")
             return jsonify({'message': 'No recommendations found matching criteria', 'results': []})
        
        # Convert to dictionary
        results = recommendations_df.to_dict(orient='records')
        
        # Clean NaN values which break JSON serialization
        import pandas as pd
        import numpy as np
        results = [{k: (None if isinstance(v, float) and np.isnan(v) else v) for k, v in record.items()} for record in results]
        
        print(f"DEBUG: Found {len(results)} recommendations. Top result: {results[0] if results else 'None'}")
        return jsonify({'message': 'Success', 'results': results})
        
    except ValueError:
        return jsonify({'error': 'Invalid input parameters'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
