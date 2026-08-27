import os
import pandas as pd
from db import db
from models import Material


def to_bool(x):
    if pd.isna(x):
        return False
    if isinstance(x, bool):
        return x
    x = str(x).strip().lower()
    return x in ["1", "true", "yes", "y"]


def import_materials():
    """Import materials from CSV safely. Must be called within an app context."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        os.path.join(base_dir, "materials_500.csv"),
        os.path.join(base_dir, "..", "materials_500.csv"),
        os.path.join(base_dir, "materials_cleaned.csv"),
        os.path.join(base_dir, "..", "materials_cleaned.csv"),
        os.path.join(base_dir, "..", "materials_milestone1_final.csv"),
    ]

    csv_path = None
    for p in candidates:
        if os.path.exists(p):
            csv_path = p
            break

    if not csv_path:
        print("[WARNING] No materials CSV file found for initialization. Skipping import.")
        return

    try:
        df = pd.read_csv(csv_path)
        print(f"[INFO] CSV Loaded from {csv_path}. Rows: {len(df)}")
    except Exception as e:
        print(f"[ERROR] Reading CSV {csv_path}: {e}")
        return

    inserted = 0
    skipped = 0

    for _, row in df.iterrows():
        name = str(row.get("material_name") or row.get("material") or "").strip()
        if not name:
            skipped += 1
            continue

        existing = Material.query.filter_by(material_name=name).first()
        if existing:
            skipped += 1
            continue

        cost = row.get("cost_per_kg") if "cost_per_kg" in row else row.get("cost")
        co2 = row.get("co2_per_kg") if "co2_per_kg" in row else row.get("co2_emission")
        strength = row.get("strength") if "strength" in row else row.get("durability")
        if strength is not None and pd.notna(strength):
            try:
                strength = float(strength)
                if strength <= 10:
                    strength = strength * 10
            except ValueError:
                strength = 50.0

        m = Material(
            material_name=name,
            material_type=row.get("material_type", "Standard"),
            recyclable=to_bool(row.get("recyclable")),
            biodegradable=to_bool(row.get("biodegradable")),
            density=row.get("density"),
            strength=strength,
            cost_per_kg=cost,
            co2_per_kg=co2,
        )

        db.session.add(m)
        inserted += 1

    db.session.commit()
    print(f"[SUCCESS] Inserted: {inserted}, Skipped: {skipped}")


if __name__ == "__main__":
    from app import app
    with app.app_context():
        import_materials()
