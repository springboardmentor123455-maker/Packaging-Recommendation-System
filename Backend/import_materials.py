import pandas as pd
from app import app
from db import db
from models import Material

CSV_PATH = r"C:\Users\ayush\OneDrive\Desktop\Infosys Project\materials_500.csv"  # update if file is in different location


def to_bool(x):
    if pd.isna(x):
        return False
    if isinstance(x, bool):
        return x
    x = str(x).strip().lower()
    return x in ["1", "true", "yes", "y"]


with app.app_context():
    df = pd.read_csv(CSV_PATH)

    print("✅ CSV Loaded. Rows:", len(df))
    print("✅ Columns:", list(df.columns))

    inserted = 0
    skipped = 0

    for _, row in df.iterrows():
        name = str(row.get("material_name", "")).strip()
        if not name:
            skipped += 1
            continue

        existing = Material.query.filter_by(material_name=name).first()
        if existing:
            skipped += 1
            continue

        m = Material(
            material_name=name,
            material_type=row.get("material_type"),
            recyclable=to_bool(row.get("recyclable")),
            biodegradable=to_bool(row.get("biodegradable")),
            density=row.get("density"),
            strength=row.get("strength"),
            cost_per_kg=row.get("cost_per_kg"),
            co2_per_kg=row.get("co2_per_kg"),
        )

        db.session.add(m)
        inserted += 1

    db.session.commit()
    print(f"✅ Inserted: {inserted}, Skipped: {skipped}")
