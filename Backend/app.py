from flask import Flask, jsonify, request
from flask_cors import CORS
from config import Config
from db import db
from models import Material, Product, Recommendation
from flask import render_template



app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
CORS(app)

with app.app_context():
    db.create_all()
    print("✅ Tables created successfully!")


@app.route("/")
def home():
    return jsonify({"success": True, "message": "Packaging Backend Running ✅"})

@app.route("/ui")
def ui():
    return render_template("index.html")



@app.route("/api/material", methods=["POST"])
def add_material():
    data = request.get_json()

    material = Material(
        material_name=data.get("material_name"),
        material_type=data.get("material_type"),
        recyclable=data.get("recyclable", False),
        biodegradable=data.get("biodegradable", False),
        density=data.get("density"),
        strength=data.get("strength"),
        cost_per_kg=data.get("cost_per_kg"),
        co2_per_kg=data.get("co2_per_kg"),
    )

    db.session.add(material)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Material added successfully",
        "material_id": material.id
    }), 201


@app.route("/api/product", methods=["POST"])
def add_product():
    data = request.get_json()

    product = Product(
        product_name=data.get("product_name"),
        category=data.get("category"),
        weight_kg=data.get("weight_kg"),
        fragile=data.get("fragile", False),
        shipping_distance_km=data.get("shipping_distance_km"),
    )

    db.session.add(product)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Product added successfully",
        "product_id": product.id
    }), 201


@app.route("/api/materials", methods=["GET"])
def get_materials():
    materials = Material.query.all()

    result = []
    for m in materials:
        result.append({
            "id": m.id,
            "material_name": m.material_name,
            "material_type": m.material_type,
            "recyclable": m.recyclable,
            "biodegradable": m.biodegradable,
            "density": m.density,
            "strength": m.strength,
            "cost_per_kg": m.cost_per_kg,
            "co2_per_kg": m.co2_per_kg,
        })

    return jsonify({
        "success": True,
        "total": len(result),
        "data": result
    })

@app.route("/api/recommend", methods=["POST"])
def recommend_material():
    data = request.get_json()
    show_debug = request.args.get("debug", "false").lower() == "true"

    if not data:
        return jsonify({"success": False, "message": "JSON body required"}), 400

    category = data.get("category", "").lower()
    fragile = data.get("fragile", False)
    weight_kg = float(data.get("weight_kg", 1.0))
    shipping_distance_km = float(data.get("shipping_distance_km", 100.0))

    materials = Material.query.all()

    results = []
    for m in materials:
        strength_score = (m.strength or 50) / 100
        cost_score = 1 / (1 + (m.cost_per_kg or 50))
        co2_score = 1 / (1 + (m.co2_per_kg or 1))

        recyclable_bonus = 0.10 if m.recyclable else 0
        fragile_bonus = 0.10 if fragile and (m.strength or 0) >= 70 else 0

        # ✅ ADD THIS (Category bonus)
        category_bonus = 0

        if category in ["food", "grocery"]:
            if m.biodegradable:
                category_bonus += 0.12
            if m.recyclable:
                category_bonus += 0.05

        elif category in ["electronics"]:
            if (m.strength or 0) >= 75:
                category_bonus += 0.12
            if m.recyclable:
                category_bonus += 0.08

        elif category in ["furniture"]:
            if (m.strength or 0) >= 80:
                category_bonus += 0.15

        elif category in ["cosmetics", "glass"]:
            if (m.strength or 0) >= 70:
                category_bonus += 0.12

        # ✅ UPDATE final_score (add category_bonus)
        final_score = (
                              0.35 * strength_score +
                              0.35 * co2_score +
                              0.20 * cost_score +
                              recyclable_bonus +
                              fragile_bonus +
                              category_bonus
                      ) * 100

        estimated_cost = (m.cost_per_kg or 0) * weight_kg
        estimated_co2 = (m.co2_per_kg or 0) * weight_kg

        item = {
            "material_name": m.material_name,
            "material_type": m.material_type,
            "recyclable": m.recyclable,
            "cost_per_kg": m.cost_per_kg,
            "co2_per_kg": m.co2_per_kg,
            "strength": m.strength,
            "final_score": round(final_score, 2),
            "estimated_cost": round(estimated_cost, 2),
            "estimated_co2": round(estimated_co2, 2)
        }

        # ✅ ADD category_bonus in debug also
        if show_debug:
            item["debug"] = {
                "strength_score": round(strength_score, 3),
                "co2_score": round(co2_score, 3),
                "cost_score": round(cost_score, 3),
                "recyclable_bonus": recyclable_bonus,
                "fragile_bonus": fragile_bonus,
                "category_bonus": category_bonus
            }

        results.append(item)

    results.sort(key=lambda x: x["final_score"], reverse=True)

    return jsonify({
        "success": True,
        "product_input": {
            "category": category,
            "fragile": fragile,
            "weight_kg": weight_kg,
            "shipping_distance_km": shipping_distance_km
        },
        "top_recommendations": results[:5]
    })


@app.route("/api/save-recommendation", methods=["POST"])
def save_recommendation():
    data = request.get_json()

    if not data:
        return jsonify({"success": False, "message": "JSON body required"}), 400

    product_id = data.get("product_id")
    recommendations = data.get("recommendations")  # list

    if not product_id or not recommendations:
        return jsonify({"success": False, "message": "product_id and recommendations required"}), 400

    saved = 0
    for r in recommendations:
        rec = Recommendation(
            product_id=product_id,
            material_name=r.get("material_name"),
            final_score=r.get("final_score"),
            estimated_cost=r.get("estimated_cost"),
            estimated_co2=r.get("estimated_co2"),
        )
        db.session.add(rec)
        saved += 1

    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Recommendations saved successfully",
        "saved_count": saved
    }), 201

@app.route("/api/product-recommend", methods=["POST"])
def product_recommend():
    data = request.get_json()

    if not data:
        return jsonify({"success": False, "message": "JSON body required"}), 400

    # 1) Save product in DB
    product = Product(
        product_name=data.get("product_name"),
        category=data.get("category"),
        weight_kg=data.get("weight_kg"),
        fragile=data.get("fragile", False),
        shipping_distance_km=data.get("shipping_distance_km"),
    )

    db.session.add(product)
    db.session.commit()

    # 2) Use same logic of recommend
    category = (data.get("category") or "").lower()
    fragile = data.get("fragile", False)
    weight_kg = float(data.get("weight_kg", 1.0))
    shipping_distance_km = float(data.get("shipping_distance_km", 100.0))

    materials = Material.query.all()

    results = []
    for m in materials:
        strength_score = (m.strength or 50) / 100

        estimated_cost = round((m.cost_per_kg or 0) * weight_kg, 3)
        estimated_co2 = round((m.co2_per_kg or 0) * weight_kg * (shipping_distance_km / 100), 3)

        cost_score = 1 / (1 + (m.cost_per_kg or 50))
        co2_score = 1 / (1 + (m.co2_per_kg or 1))

        recyclable_bonus = 0.10 if m.recyclable else 0
        fragile_bonus = 0.10 if fragile and (m.strength or 0) >= 70 else 0

        category_bonus = 0

        if category in ["food", "grocery"]:
            if m.biodegradable:
                category_bonus += 0.12
            if m.recyclable:
                category_bonus += 0.05

        elif category in ["electronics"]:
            if (m.strength or 0) >= 75:
                category_bonus += 0.12
            if m.recyclable:
                category_bonus += 0.08

        elif category in ["furniture"]:
            if (m.strength or 0) >= 80:
                category_bonus += 0.15

        elif category in ["cosmetics", "glass"]:
            if (m.strength or 0) >= 70:
                category_bonus += 0.12

        final_score = (
                              0.35 * strength_score +
                              0.35 * co2_score +
                              0.20 * cost_score +
                              recyclable_bonus +
                              fragile_bonus +
                              category_bonus
                      ) * 100

        results.append({
            "material_name": m.material_name,
            "material_type": m.material_type,
            "recyclable": m.recyclable,
            "cost_per_kg": m.cost_per_kg,
            "co2_per_kg": m.co2_per_kg,
            "strength": m.strength,
            "final_score": round(final_score, 2),
            "estimated_cost": estimated_cost,
            "estimated_co2": estimated_co2
        })

    results.sort(key=lambda x: x["final_score"], reverse=True)

    top5 = results[:5]

    # ✅ Save top5 recommendations into DB
    for r in top5:
        rec = Recommendation(
            product_id=product.id,
            material_name=r["material_name"],
            final_score=r["final_score"],
            estimated_cost=r.get("estimated_cost"),
            estimated_co2=r.get("estimated_co2"),
        )
        db.session.add(rec)

    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Product saved and recommendation generated ✅",
        "product_id": product.id,
        "product_input": {
            "product_name": product.product_name,
            "category": product.category,
            "weight_kg": product.weight_kg,
            "fragile": product.fragile,
            "shipping_distance_km": product.shipping_distance_km
        },
        "top_recommendations": top5
    }), 201







if __name__ == "__main__":
    app.run(debug=True)
