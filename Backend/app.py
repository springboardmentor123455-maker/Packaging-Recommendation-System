from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from config import Config
from db import db
from models import Material, Product, Recommendation
from sqlalchemy import func
import os


app = Flask(__name__, template_folder="templates")
app.config.from_object(Config)

db.init_app(app)
CORS(app)


@app.route("/")
def home():
    return jsonify({"success": True, "message": "Packaging Backend Running ✅"})


@app.route("/ui")
def ui():
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


# ✅ Run this ONCE after deploy to create tables
@app.route("/init-db")
def init_db():
    with app.app_context():
        db.create_all()
    return jsonify({"success": True, "message": "✅ Tables created successfully!"})


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
    recommendations = data.get("recommendations")

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

    product = Product(
        product_name=data.get("product_name"),
        category=data.get("category"),
        weight_kg=data.get("weight_kg"),
        fragile=data.get("fragile", False),
    )

    db.session.add(product)
    db.session.commit()

    category = (data.get("category") or "").lower()
    fragile = data.get("fragile", False)
    weight_kg = float(data.get("weight_kg", 1.0))

    materials = Material.query.all()

    results = []
    for m in materials:
        strength_score = (m.strength or 50) / 100
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

        estimated_cost = round((m.cost_per_kg or 0) * weight_kg, 2)
        estimated_co2 = round((m.co2_per_kg or 0) * weight_kg, 2)

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
        "top_recommendations": top5
    }), 201


@app.route("/api/dashboard/summary", methods=["GET"])
def dashboard_summary():
    total_products = db.session.query(func.count(Product.id)).scalar() or 0
    total_recommendations = db.session.query(func.count(Recommendation.id)).scalar() or 0

    material_usage = (
        db.session.query(Recommendation.material_name, func.count(Recommendation.id).label("count"))
        .group_by(Recommendation.material_name)
        .order_by(func.count(Recommendation.id).desc())
        .limit(5)
        .all()
    )
    top_materials = [{"material_name": m, "count": c} for m, c in material_usage]

    baseline_cost_per_kg = 10
    baseline_co2_per_kg = 2

    products = Product.query.all()

    total_baseline_cost = 0
    total_baseline_co2 = 0
    total_recommended_cost = 0
    total_recommended_co2 = 0

    for p in products:
        weight = p.weight_kg or 1

        total_baseline_cost += weight * baseline_cost_per_kg
        total_baseline_co2 += weight * baseline_co2_per_kg

        best_rec = (
            Recommendation.query.filter_by(product_id=p.id)
            .order_by(Recommendation.estimated_co2.asc())
            .first()
        )

        if best_rec:
            total_recommended_cost += best_rec.estimated_cost or 0
            total_recommended_co2 += best_rec.estimated_co2 or 0

    cost_saved = total_baseline_cost - total_recommended_cost
    co2_saved = total_baseline_co2 - total_recommended_co2

    cost_saving_percent = (cost_saved / total_baseline_cost * 100) if total_baseline_cost > 0 else 0
    co2_reduction_percent = (co2_saved / total_baseline_co2 * 100) if total_baseline_co2 > 0 else 0

    return jsonify({
        "success": True,
        "summary": {
            "total_products": total_products,
            "total_recommendations": total_recommendations,
            "total_baseline_cost": round(total_baseline_cost, 2),
            "total_recommended_cost": round(total_recommended_cost, 2),
            "cost_saved": round(cost_saved, 2),
            "cost_saving_percent": round(cost_saving_percent, 2),
            "total_baseline_co2": round(total_baseline_co2, 2),
            "total_recommended_co2": round(total_recommended_co2, 2),
            "co2_saved": round(co2_saved, 2),
            "co2_reduction_percent": round(co2_reduction_percent, 2),
        },
        "top_materials": top_materials
    })


@app.route("/api/dashboard/material-trends", methods=["GET"])
def material_trends():
    rows = (
        db.session.query(Recommendation.material_name, func.count(Recommendation.id))
        .group_by(Recommendation.material_name)
        .order_by(func.count(Recommendation.id).desc())
        .limit(5)
        .all()
    )

    data = [{"material_name": name, "count": count} for name, count in rows]
    return jsonify({"success": True, "data": data})


@app.route("/api/dashboard/savings", methods=["GET"])
def dashboard_savings():
    BASELINE_COST_PER_KG = 10
    BASELINE_CO2_PER_KG = 2

    products = Product.query.all()

    baseline_total_cost = 0
    baseline_total_co2 = 0

    for p in products:
        w = p.weight_kg or 1
        baseline_total_cost += BASELINE_COST_PER_KG * w
        baseline_total_co2 += BASELINE_CO2_PER_KG * w

    recommended_total_cost = db.session.query(func.sum(Recommendation.estimated_cost)).scalar() or 0
    recommended_total_co2 = db.session.query(func.sum(Recommendation.estimated_co2)).scalar() or 0

    cost_savings = baseline_total_cost - recommended_total_cost
    co2_savings = baseline_total_co2 - recommended_total_co2

    cost_savings_percent = (cost_savings / baseline_total_cost * 100) if baseline_total_cost > 0 else 0
    co2_reduction_percent = (co2_savings / baseline_total_co2 * 100) if baseline_total_co2 > 0 else 0

    return jsonify({
        "success": True,
        "baseline_total_cost": round(baseline_total_cost, 2),
        "baseline_total_co2": round(baseline_total_co2, 2),
        "recommended_total_cost": round(recommended_total_cost, 2),
        "recommended_total_co2": round(recommended_total_co2, 2),
        "cost_savings": round(cost_savings, 2),
        "cost_savings_percent": round(cost_savings_percent, 2),
        "co2_savings": round(co2_savings, 2),
        "co2_reduction_percent": round(co2_reduction_percent, 2),
        "total_products": len(products)
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

