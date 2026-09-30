import pandas as pd
import numpy as np
import joblib
import warnings
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

warnings.filterwarnings('ignore')

def train():
    df = pd.read_csv('data/student_data.csv')
    scaler = joblib.load('models/scaler.pkl')
    encoder = joblib.load('models/encoder.pkl')
    
    # Feature Engineering matching preprocess.py and app.py
    df['total_academic_score'] = (df['assignment_score'] * 0.4) + (df['internal_score'] * 0.6)
    df['effort_score'] = (df['study_hours'] * 10) + df['attendance']
    df['overall_weighted_index'] = (df['total_academic_score'] * 0.5) + (df['effort_score'] * 0.3) + (df['previous_gpa'] * 10 * 0.2)
    df['completion_ratio'] = df['assignments_completed'] / (df['study_hours'] + 1e-5)

    X = df.drop(columns=['student_id', 'performance'], errors='ignore').astype(np.float64)
    y = encoder.transform(df['performance'])
    
    X_scaled = scaler.transform(X).astype(np.float64)
    
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.15, random_state=42, stratify=y
    )
    
    # 3-fold Stratified CV strategy
    cv_strategy = StratifiedKFold(n_splits=3, shuffle=True, random_state=42)

    param_grids = {
        'RandomForestClassifier': (
            # Added class_weight='balanced' to prevent majority bias
            RandomForestClassifier(random_state=42, class_weight='balanced'),
            {
                'n_estimators': [100, 200],
                'max_depth': [8, 12, None],
                'min_samples_split': [2, 5],
                'criterion': ['gini', 'entropy']
            },
            'models/rf_model.pkl'
        ),
        'GradientBoostingClassifier': (
            GradientBoostingClassifier(random_state=42),
            {
                'n_estimators': [100, 150],
                'learning_rate': [0.01, 0.05, 0.1],
                'max_depth': [3, 4],
                'subsample': [0.8, 1.0]
            },
            'models/gb_model.pkl'
        ),
        'LogisticRegression': (
            # Added class_weight='balanced'
            LogisticRegression(max_iter=1000, random_state=42, class_weight='balanced'),
            {
                'C': [0.1, 1.0, 5.0, 10.0],
                'solver': ['lbfgs'],
                'penalty': ['l2']
            },
            'models/lr_model.pkl'
        )
    }
    
    metrics = {}
    best_model = None
    best_score = 0

    print("=" * 60)
    print("       HYPERPARAMETER TUNING VIA GRIDSEARCHCV (3-FOLD)       ")
    print("=" * 60)

    for name, (base_model, grid, save_path) in param_grids.items():
        print(f"\n[TUNING] Running 3-Fold Stratified CV for {name}...")
        grid_search = GridSearchCV(
            estimator=base_model,
            param_grid=grid,
            cv=cv_strategy,
            scoring='accuracy',
            n_jobs=-1
        )
        grid_search.fit(X_train, y_train)
        
        # Extract tuned model
        tuned_model = grid_search.best_estimator_
        
        # Save individual model file for tier-based routing
        joblib.dump(tuned_model, save_path)
        print(f"  • Saved model instance to: {save_path}")
        
        preds = tuned_model.predict(X_test)
        
        acc = round(accuracy_score(y_test, preds) * 100, 2)
        prec = round(precision_score(y_test, preds, average='weighted', zero_division=0) * 100, 2)
        rec = round(recall_score(y_test, preds, average='weighted', zero_division=0) * 100, 2)
        f1 = round(f1_score(y_test, preds, average='weighted', zero_division=0) * 100, 2)
        
        metrics[name] = {
            'accuracy': acc,
            'precision': prec,
            'recall': rec,
            'f1_score': f1,
            'best_params': grid_search.best_params_
        }
        
        print(f"  • Best Parameters: {grid_search.best_params_}")
        print(f"  • Test Accuracy  : {acc}%")
        
        if acc > best_score:
            best_score = acc
            best_model = tuned_model

    # Save globally top-performing model and metrics map
    joblib.dump(best_model, 'models/model.pkl')
    joblib.dump(metrics, 'models/metrics.pkl')
    
    print("\n" + "=" * 60)
    print(f" OPTIMAL MODEL SAVED: {type(best_model).__name__} ({best_score}% Accuracy)")
    print("=" * 60)

if __name__ == '__main__':
    train()