import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
import joblib

def preprocess():
    df = pd.read_csv('data/student_data.csv')
    
    # 1. Advanced Feature Engineering (Matches train_models.py & app.py)
    df['total_academic_score'] = (df['assignment_score'] * 0.4) + (df['internal_score'] * 0.6)
    df['effort_score'] = (df['study_hours'] * 10) + df['attendance']
    df['overall_weighted_index'] = (df['total_academic_score'] * 0.5) + (df['effort_score'] * 0.3) + (df['previous_gpa'] * 10 * 0.2)
    df['completion_ratio'] = df['assignments_completed'] / (df['study_hours'] + 1e-5)
    
    # 2. Separate features (X) and target (y)
    X = df.drop(columns=['student_id', 'performance'], errors='ignore')
    y = df['performance']
    
    # 3. Cast features to uniform float64
    X = X.astype(np.float64)
    
    # 4. Scale features & fit scaler on all 11 columns
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X).astype(np.float64)
    
    # 5. Encode target string labels into numeric classes
    encoder = LabelEncoder()
    y_encoded = encoder.fit_transform(y)
    
    # 6. Save preprocessed artifacts
    joblib.dump(scaler, 'models/scaler.pkl')
    joblib.dump(encoder, 'models/encoder.pkl')
    
    print("[SUCCESS] Enhanced Preprocessing Completed! 'scaler.pkl' and 'encoder.pkl' updated with 11 features.")

if __name__ == '__main__':
    preprocess()