import os
import joblib
import numpy as np
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for
from config import Config
from src.db import save_prediction, fetch_recent_predictions, delete_prediction
from src.utils import generate_analytics_charts

app = Flask(__name__)
app.config.from_object(Config)

# 1. Load Preprocessing Artifacts
scaler = joblib.load('models/scaler.pkl')
encoder = joblib.load('models/encoder.pkl')
metrics = joblib.load('models/metrics.pkl')

# 2. Load Individual Models for Dynamic Routing
gb_model = joblib.load('models/gb_model.pkl')
rf_model = joblib.load('models/rf_model.pkl')
lr_model = joblib.load('models/lr_model.pkl')

@app.route('/')
def index():
    df = pd.read_csv('data/student_data.csv')
    stats = {
        'total_students': len(df),
        'avg_attendance': round(df['attendance'].mean(), 1),
        'avg_study_hours': round(df['study_hours'].mean(), 1),
        'at_risk_count': len(df[df['performance'] == 'At Risk'])
    }
    recent = fetch_recent_predictions(10)
    return render_template('index.html', stats=stats, recent=recent)

@app.route('/delete/<int:record_id>', methods=['POST'])
def delete_record(record_id):
    delete_prediction(record_id)
    return redirect(request.referrer or url_for('index'))

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        student_name = request.form.get('student_name', 'Anonymous').strip()
        attendance = float(request.form.get('attendance', 0))
        study_hours = float(request.form.get('study_hours', 0))
        assignment_score = float(request.form.get('assignment_score', 0))
        internal_score = float(request.form.get('internal_score', 0))
        previous_gpa = float(request.form.get('previous_gpa', 0))
        participation_score = float(request.form.get('participation_score', 0))
        assignments_completed = float(request.form.get('assignments_completed', 0))

        # 1. Compute 4 Engineered Features
        total_academic_score = (assignment_score * 0.4) + (internal_score * 0.6)
        effort_score = (study_hours * 10) + attendance
        overall_weighted_index = (total_academic_score * 0.5) + (effort_score * 0.3) + (previous_gpa * 10 * 0.2)
        completion_ratio = assignments_completed / (study_hours + 1e-5)

        raw_features = pd.DataFrame([[
            attendance, study_hours, assignment_score, internal_score,
            previous_gpa, participation_score, assignments_completed,
            total_academic_score, effort_score, overall_weighted_index, completion_ratio
        ]], columns=[
            'attendance', 'study_hours', 'assignment_score', 'internal_score',
            'previous_gpa', 'participation_score', 'assignments_completed',
            'total_academic_score', 'effort_score', 'overall_weighted_index', 'completion_ratio'
        ], dtype=np.float64)

        scaled_input = scaler.transform(raw_features).astype(np.float64)

        # 2. Dynamic Ensemble Routing Logic
        if overall_weighted_index >= 75.0 or total_academic_score >= 80.0:
            selected_model = gb_model
            model_name = "Gradient Boosting (High-Performance Specialist)"
        elif 50.0 <= overall_weighted_index < 75.0:
            selected_model = rf_model
            model_name = "Random Forest (Mid-Tier Specialist)"
        else:
            selected_model = lr_model
            model_name = "Logistic Regression (At-Risk Specialist)"

        # 3. Predict & Decode Target
        prediction_idx = selected_model.predict(scaled_input)[0]
        prediction_label = encoder.inverse_transform([prediction_idx])[0]

        # 4. Save to Database
        record = {
            'student_name': student_name if student_name else 'Anonymous',
            'attendance': attendance,
            'study_hours': study_hours,
            'assignment_score': assignment_score,
            'internal_score': internal_score,
            'previous_gpa': previous_gpa,
            'participation_score': participation_score,
            'assignments_completed': assignments_completed,
            'prediction': prediction_label,
            'model_used': model_name
        }
        
        record_id = save_prediction(record)

        return render_template(
            'predict.html', 
            result=prediction_label, 
            student_name=student_name,
            record_id=record_id,
            model_used=model_name
        )

    return render_template('predict.html', result=None)

@app.route('/analytics')
def analytics():
    c1, c2, c3 = generate_analytics_charts()
    return render_template('analytics.html', chart1=c1, chart2=c2, chart3=c3)

@app.route('/comparison')
def comparison():
    return render_template('comparison.html', metrics=metrics)

if __name__ == '__main__':
    app.run(debug=True, port=5000)