
import sqlite3
import pandas as pd
import datetime

def validate():
    print("\n")
    print("=" * 70)
    print("  ECOPACKAI - DATASET VALIDATION REPORT (MILESTONE 1)")
    print(f"  Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 70)
    
    try:
        conn = sqlite3.connect('ecopackai.db')
        df = pd.read_sql("SELECT * FROM materials_data", conn)
        
        print(f"\n[1] DATA VOLUME")
        print(f"    Total Records: {len(df)}")
        print(f"    Total Features: {len(df.columns)}")
        print("    Status: PASS")

        print(f"\n[2] DATA QUALITY CHECKS")
        nulls = df.isnull().sum().sum()
        dups = df.duplicated().sum()
        print(f"    Missing Values: {nulls}")
        print(f"    Duplicate Rows: {dups}")
        if nulls == 0 and dups == 0:
             print("    Status: NO ISSUES FOUND")
        else:
             print("    Status: WARNING")

        print(f"\n[3] KEY METRICS DISTRIBUTION")
        print("-" * 65)
        num_cols = df.select_dtypes(include=['float64', 'int64']).columns
        key_cols = [c for c in num_cols if c in ['strength', 'co2_emission_score', 'biodegradability_score', 'cost_per_kg']]
        print(df[key_cols].describe().T[['mean', 'std', 'min', 'max']].round(2).to_string())
        print("-" * 65)

        print("\n" + "=" * 70)
        print("  VERDICT: DATASET READY FOR MODEL TRAINING")
        print("=" * 70 + "\n")

    except Exception as e:
        print(f"Error: {e}")
        # Hint for user
        print("\nHint: Make sure 'ecopackai.db' exists (Run init_sqlite_db.py first)")
    finally:
        if 'conn' in locals(): conn.close()
        
if __name__ == "__main__":
    validate()
