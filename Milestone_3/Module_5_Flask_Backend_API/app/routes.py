from flask import render_template, jsonify, request
from app import app
from app.database import get_all_categories
import sys
import os

# Ensure parent directory is in path for imports if not already
# We need to reach 'infosys' root to find other Milestones
current_dir = os.path.dirname(os.path.abspath(__file__)) # app
backend_api_dir = os.path.dirname(current_dir) # Module_5_Flask_Backend_API
milestone_3_dir = os.path.dirname(backend_api_dir) # Milestone_3
root_dir = os.path.dirname(milestone_3_dir) # infosys

# Add Module 4 (Recommendation Engine) to path
rec_model_dir = os.path.join(root_dir, 'Milestone_2', 'Module_4_AI_Recommendation_Model')
if rec_model_dir not in sys.path:
    sys.path.append(rec_model_dir)

# Add Module 3 (ML Preparation) to path for reporting
ml_prep_dir = os.path.join(root_dir, 'Milestone_2', 'Module_3_ML_Dataset_Preparation')
if ml_prep_dir not in sys.path:
    sys.path.append(ml_prep_dir)

# RecommendationEngine initialization moved to inside recommend() route for memory efficiency

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/categories', methods=['GET'])
def get_categories():
    categories = get_all_categories()
    return jsonify(categories)

@app.route('/api/recommend', methods=['POST'])
def recommend():
    recommendations_df = None
    engine = None
    
    # Try to initialize AI Engine (Lazy Load)
    # RENDER FIX: DISABLED AI ENGINE TO PREVENT MEMORY CRASHES ON FREE TIER
    # try:
    #     from recommendation_engine import RecommendationEngine
    #     # Lazy initialization
    #     models_dir = os.path.join(rec_model_dir, 'models')
    #     engine = RecommendationEngine(model_dir=models_dir)
    #     print("✓ Recommendation Engine initialized successfully (Lazy Load)")
    # except Exception as e:
    #      print(f"⚠️ Warning: Failed to initialize AI Engine: {e}. Switching to Simple/Rule-Based Fallback.")
    #      engine = None

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

        if engine:
            try:
                # Get recommendations from AI
                recommendations_df = engine.recommend_materials(
                    required_strength=required_strength,
                    max_cost=valid_max_cost,
                    max_co2=valid_max_co2
                )
                # Cleanup AI memory immediately
                del engine
                import gc
                gc.collect()
            except Exception as e:
                print(f"⚠️ AI Engine Runtime Error: {e}. Fallback to Simple Logic.")
                recommendations_df = None
        
        # FALLBACK: If AI failed or wasn't loaded
        if recommendations_df is None:
            print("ℹ️ Using Simple Rule-Based Filtering (Fallback)...")
            from ml_preparation import load_data_from_db
            df = load_data_from_db()
            
            # Filter Logic
            filtered_df = df.copy()
            if required_strength > 0:
                filtered_df = filtered_df[filtered_df['strength'] >= required_strength]
            if valid_max_cost is not None:
                filtered_df = filtered_df[filtered_df['cost_per_kg'] <= valid_max_cost]
            if valid_max_co2 is not None:
                filtered_df = filtered_df[filtered_df['co2_emission_score'] <= valid_max_co2]
            
            # Sort by sustainable score descending
            # Calculate a simple score if not present
            if 'sustainable_score' not in filtered_df.columns:
                 # Normalize and combine (Simple heuristic)
                 filtered_df['sustainable_score'] = (
                     (filtered_df['biodegradability_score'] / 100) * 0.4 + 
                     (1 - (filtered_df['co2_emission_score'] / filtered_df['co2_emission_score'].max())) * 0.4 +
                     (filtered_df['recyclability_score'] / 10) * 0.2
                 ) * 100
            
            recommendations_df = filtered_df.sort_values(by='sustainable_score', ascending=False).head(5)

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

@app.route('/api/dashboard_stats', methods=['GET'])
def get_dashboard_metrics():
    try:
        from app.database import get_dashboard_stats
        stats = get_dashboard_stats()
        
        if not stats:
            return jsonify({'error': 'Failed to fetch stats'}), 500

        # Process data
        overall_co2 = stats.get('overall', {}).get('avg_co2') or 1
        susp_co2 = stats.get('sustainable_avg', {}).get('avg_co2') or 1
        # Prevent division by zero if averages are None (empty DB)
        overall_co2 = float(overall_co2) if overall_co2 else 1.0
        susp_co2 = float(susp_co2) if susp_co2 else 1.0

        co2_reduction = ((overall_co2 - susp_co2) / overall_co2) * 100
        
        overall_cost = stats.get('overall', {}).get('avg_cost') or 1
        susp_cost = stats.get('sustainable_avg', {}).get('avg_cost') or 1
        overall_cost = float(overall_cost) if overall_cost else 1.0
        susp_cost = float(susp_cost) if susp_cost else 1.0
        susp_bio = float(stats.get('sustainable_avg', {}).get('avg_bio') or 0)

        cost_savings = ((overall_cost - susp_cost) / overall_cost) * 100
        
        return jsonify({
            'metrics': {
                'co2_reduction_pct': round(co2_reduction, 1),
                'cost_savings_pct': round(cost_savings, 1),
                'avg_sustainable_co2': round(susp_co2, 3),
                'avg_sustainable_cost': round(susp_cost, 2),
                'avg_sustainable_bio': round(susp_bio, 1)
            },
            'trends': stats.get('trends', []),
            'savings_comparison': stats.get('savings_comparison', [])
        })
    except Exception as e:
        print(f"Stats Error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/export_report', methods=['GET'])
def export_report():
    try:
        export_format = request.args.get('format', 'xlsx')
        
        # 1. Fetch Data
        from ml_preparation import load_data_from_db
        df = load_data_from_db()
        from app.database import get_all_categories
        cats = get_all_categories()
        
        if export_format == 'pdf':
            return generate_pdf_report(df, cats)
        else:
            return generate_excel_report(df, cats)
            
    except Exception as e:
        print(f"Export Error: {e}")
        return jsonify({'error': str(e)}), 500

def generate_excel_report(df, cats):
    try:
        import pandas as pd
        from io import BytesIO
        from flask import send_file
        
        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        
        if df is not None:
            df.to_excel(writer, sheet_name='All Materials', index=False)
        else:
            pd.DataFrame({'Info': ['No materials data available']}).to_excel(writer, sheet_name='All Materials', index=False)
            
        if cats:
            pd.DataFrame(cats).to_excel(writer, sheet_name='Categories', index=False)
        else:
            pd.DataFrame({'Info': ['No categories available']}).to_excel(writer, sheet_name='Categories', index=False)
            
        writer.close()
        output.seek(0)
        
        return send_file(output, download_name="Sustainability_Report.xlsx", as_attachment=True)
    except Exception as e:
        raise e

def generate_pdf_report(df, cats):
    try:
        from fpdf import FPDF
        from io import BytesIO
        from flask import send_file, make_response
        
        class PDF(FPDF):
            def header(self):
                self.set_font('Arial', 'B', 15)
                self.cell(0, 10, 'EcoPackAI - Sustainability Report', 0, 1, 'C')
                self.ln(5)
                
            def footer(self):
                self.set_y(-15)
                self.set_font('Arial', 'I', 8)
                self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

        pdf = PDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        # Summary Section
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "Executive Summary", 0, 1)
        pdf.set_font("Arial", size=11)
        
        total_materials = len(df) if df is not None else 0
        avg_co2 = df['co2_emission_score'].mean() if df is not None else 0
        
        pdf.cell(0, 8, f"Total Materials Analyzed: {total_materials}", 0, 1)
        pdf.cell(0, 8, f"Average Portfolio CO2 Score: {avg_co2:.3f}", 0, 1)
        pdf.ln(10)
        
        # Top Sustainable Materials
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "Top 5 Sustainable Materials", 0, 1)
        pdf.set_font("Arial", size=10)
        
        # Table Header
        col_width = 38
        pdf.set_fill_color(200, 220, 255)
        headers = ['Name', 'Type', 'CO2 Score', 'Cost ($)', 'Bio %']
        for col in headers:
            pdf.cell(col_width, 10, col, 1, 0, 'C', 1)
        pdf.ln()
        
        if df is not None:
            # Sort by CO2
            top_df = df.sort_values('co2_emission_score').head(5)
            
            for _, row in top_df.iterrows():
                pdf.cell(col_width, 10, str(row['material_name'])[:20], 1)
                pdf.cell(col_width, 10, str(row['material_type'])[:20], 1)
                pdf.cell(col_width, 10, f"{row['co2_emission_score']:.3f}", 1)
                pdf.cell(col_width, 10, f"{row['cost_per_kg']:.2f}", 1)
                pdf.cell(col_width, 10, f"{row.get('biodegradability_score', 'N/A')}", 1)
                pdf.ln()
        
        pdf.ln(10)
        
        # Matplotlib Chart
        try:
            import matplotlib
            matplotlib.use('Agg')
            import matplotlib.pyplot as plt
            import tempfile
            import os

            if df is not None:
                top_df = df.sort_values('co2_emission_score').head(5)
                
                plt.figure(figsize=(10, 6))
                colors = ['#198754', '#20c997', '#0dcaf0', '#ffc107', '#fd7e14']
                bars = plt.bar(top_df['material_name'], top_df['co2_emission_score'], color=colors[:len(top_df)])
                
                plt.title('Top 5 Sustainable Materials (CO2 Score)', fontsize=14)
                plt.xlabel('Material Name', fontsize=12)
                plt.ylabel('CO2 Emission Score (Lower is Better)', fontsize=12)
                plt.xticks(rotation=45, ha='right')
                plt.tight_layout()
                
                # Save to temp file
                with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_img:
                    plt.savefig(tmp_img.name, dpi=100)
                    tmp_img_path = tmp_img.name
                
                plt.close()
                
                # Add to PDF
                pdf.ln(5)
                pdf.cell(0, 10, "Visualization: CO2 Impact Comparison", 0, 1)
                # Calculate X to center image (A4 width ~210mm)
                # Image width 150mm
                x_centered = (210 - 150) / 2
                pdf.image(tmp_img_path, x=x_centered, w=150)
                pdf.ln(5)
                
                # Clean up
                try:
                    os.unlink(tmp_img_path)
                except:
                    pass

        except Exception as e:
            print(f"Chart Generation Error: {e}")
            pdf.cell(0, 10, "Chart could not be generated.", 0, 1)
        
        pdf.ln(10)
        
        # Category Breakdown
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "Category Overview", 0, 1)
        pdf.set_font("Arial", size=10)
        
        if cats:
            for cat in cats:
                pdf.cell(0, 8, f"- {cat['category_name']} (Strength Req: {cat['required_strength']})", 0, 1)
                
        # Output
        # FPDF output() returns string in older versions, bytes in newer.
        # We use a temp file strategy or byte string if possible.
        # safe way: output to string then encode
        
        # In FPDF < 2.0, output(dest='S') returns string.
        try:
             pdf_output = pdf.output(dest='S').encode('latin-1')
        except:
             # FPDF 2.0+
             pdf_output = pdf.output(dest='S') # returns bytes
             if isinstance(pdf_output, str):
                 pdf_output = pdf_output.encode('latin-1')

        response = make_response(pdf_output)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'attachment; filename=Sustainability_Report.pdf'
        
        return response
        
    except Exception as e:
        print(f"PDF Gen Error: {e}")
        raise e
