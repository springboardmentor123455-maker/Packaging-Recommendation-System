from flask import Flask, jsonify, request
from flask_cors import CORS
from config import Config
from db import db
from models import Material, Product, Recommendation
from flask import render_template
import pandas as pd
from flask import send_file
import os

from flask import Flask

app = Flask(__name__, template_folder="templates")





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

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")




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

    )

    db.session.add(product)
    db.session.commit()

    # 2) Use same logic of recommend
    category = (data.get("category") or "").lower()
    fragile = data.get("fragile", False)
    weight_kg = float(data.get("weight_kg", 1.0))


    materials = Material.query.all()

    results = []
    for m in materials:
        strength_score = (m.strength or 50) / 100

        estimated_cost = round((m.cost_per_kg or 0) * weight_kg, 3)



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

from sqlalchemy import func

@app.route("/api/dashboard/summary", methods=["GET"])
def dashboard_summary():
    # Total products created
    total_products = db.session.query(func.count(Product.id)).scalar() or 0

    # Total recommendations saved
    total_recommendations = db.session.query(func.count(Recommendation.id)).scalar() or 0

    # Material usage trends (Top materials)
    material_usage = (
        db.session.query(Recommendation.material_name, func.count(Recommendation.id).label("count"))
        .group_by(Recommendation.material_name)
        .order_by(func.count(Recommendation.id).desc())
        .limit(5)
        .all()
    )

    top_materials = [{"material_name": m, "count": c} for m, c in material_usage]

    # ✅ Baseline assumptions (you can change later)
    # baseline_cost = weight_kg * 10
    # baseline_co2 = weight_kg * 2
    baseline_cost_per_kg = 10
    baseline_co2_per_kg = 2

    # Get all products
    products = Product.query.all()

    total_baseline_cost = 0
    total_baseline_co2 = 0
    total_recommended_cost = 0
    total_recommended_co2 = 0

    for p in products:
        weight = p.weight_kg or 1

        # baseline
        total_baseline_cost += weight * baseline_cost_per_kg
        total_baseline_co2 += weight * baseline_co2_per_kg

        # best recommendation for this product (lowest co2)
        best_rec = (
            Recommendation.query.filter_by(product_id=p.id)
            .order_by(Recommendation.estimated_co2.asc())
            .first()
        )

        if best_rec:
            total_recommended_cost += best_rec.estimated_cost or 0
            total_recommended_co2 += best_rec.estimated_co2 or 0

    # savings
    cost_saved = total_baseline_cost - total_recommended_cost
    co2_saved = total_baseline_co2 - total_recommended_co2

    # % reduction
    cost_saving_percent = 0
    co2_reduction_percent = 0

    if total_baseline_cost > 0:
        cost_saving_percent = (cost_saved / total_baseline_cost) * 100

    if total_baseline_co2 > 0:
        co2_reduction_percent = (co2_saved / total_baseline_co2) * 100

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


from sqlalchemy import func

@app.route("/api/dashboard/savings", methods=["GET"])
def dashboard_savings():

    # ✅ baseline assumptions (you can change later)
    BASELINE_COST_PER_KG = 10
    BASELINE_CO2_PER_KG = 2

    # ✅ total baseline from all saved products
    products = Product.query.all()

    baseline_total_cost = 0
    baseline_total_co2 = 0

    for p in products:
        w = p.weight_kg or 1
        baseline_total_cost += BASELINE_COST_PER_KG * w
        baseline_total_co2 += BASELINE_CO2_PER_KG * w

    # ✅ total recommended from DB (from recommendations table)
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


@app.route("/api/dashboard/export-excel", methods=["GET"])
def export_excel():
    recs = Recommendation.query.order_by(Recommendation.created_at.desc()).limit(200).all()

    rows = []
    for r in recs:
        rows.append({
            "Product ID": r.product_id,
            "Material": r.material_name,
            "Final Score": r.final_score,
            "Estimated Cost": r.estimated_cost,
            "Estimated CO2": r.estimated_co2,
            "Created At": r.created_at
        })

    df = pd.DataFrame(rows)

    file_path = "sustainability_report.xlsx"
    df.to_excel(file_path, index=False)

    return send_file(file_path, as_attachment=True)


import pandas as pd
from flask import send_file
import io

@app.route("/api/dashboard/export/excel", methods=["GET"])
def export_dashboard_excel():
    products = Product.query.all()
    recs = Recommendation.query.all()

    # Products Data
    products_data = [{
        "id": p.id,
        "product_name": p.product_name,
        "category": p.category,
        "weight_kg": p.weight_kg,
        "fragile": p.fragile,
        "created_at": p.created_at
    } for p in products]

    # Recommendations Data
    recs_data = [{
        "id": r.id,
        "product_id": r.product_id,
        "material_name": r.material_name,
        "final_score": r.final_score,
        "estimated_cost": r.estimated_cost,
        "estimated_co2": r.estimated_co2,
        "created_at": r.created_at
    } for r in recs]

    df_products = pd.DataFrame(products_data)
    df_recs = pd.DataFrame(recs_data)

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df_products.to_excel(writer, sheet_name="Products", index=False)
        df_recs.to_excel(writer, sheet_name="Recommendations", index=False)

    output.seek(0)

    return send_file(
        output,
        as_attachment=True,
        download_name="sustainability_report.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )





import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

