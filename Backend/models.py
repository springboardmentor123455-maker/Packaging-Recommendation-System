from datetime import datetime
from db import db


class Material(db.Model):
    __tablename__ = "materials"

    id = db.Column(db.Integer, primary_key=True)
    material_name = db.Column(db.String(100), nullable=False, unique=True)

    material_type = db.Column(db.String(50), nullable=True)
    recyclable = db.Column(db.Boolean, default=False)
    biodegradable = db.Column(db.Boolean, default=False)

    density = db.Column(db.Float, nullable=True)
    strength = db.Column(db.Float, nullable=True)

    cost_per_kg = db.Column(db.Float, nullable=True)
    co2_per_kg = db.Column(db.Float, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(50), nullable=False)

    weight_kg = db.Column(db.Float, nullable=True)
    fragile = db.Column(db.Boolean, default=False)
    shipping_distance_km = db.Column(db.Float, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Recommendation(db.Model):
        __tablename__ = "recommendations"

        id = db.Column(db.Integer, primary_key=True)

        product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)

        material_name = db.Column(db.String(100), nullable=False)

        final_score = db.Column(db.Float, nullable=False)
        estimated_cost = db.Column(db.Float, nullable=True)
        estimated_co2 = db.Column(db.Float, nullable=True)

        created_at = db.Column(db.DateTime, default=datetime.utcnow)

