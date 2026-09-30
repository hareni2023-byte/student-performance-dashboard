# Student Performance Dashboard

An ML-based web application for analyzing and predicting student performance using academic, attendance, and engagement-related data.

## 📌 Project Overview

The Student Performance Dashboard integrates Machine Learning, Flask, MySQL, and a web-based dashboard to provide student performance analysis and prediction.

The system processes student information, applies feature engineering and preprocessing, and uses multiple machine learning classification algorithms to predict student performance.

## 🚀 Key Features

- Student performance prediction
- Student data management
- Performance analytics
- Student comparison
- Interactive dashboard
- MySQL database integration
- Multiple machine learning models
- Model performance evaluation
- Feature engineering and preprocessing

## 🤖 Machine Learning Algorithms

The project uses and compares three classification algorithms:

- Random Forest Classifier
- Gradient Boosting Classifier
- Logistic Regression

### Model Optimization

The models are optimized using:

- GridSearchCV
- 3-Fold Stratified Cross-Validation
- Hyperparameter tuning
- Class balancing

The best-performing tuned model is selected as the final prediction model.

## 📊 Evaluation Metrics

The models are evaluated using:

- Accuracy
- Precision
- Recall
- F1-Score

## 🗄️ Database

MySQL is used for storing and managing student-related application data.

Database components include:

- Database connection
- Database initialization
- Data seeding
- Student data management

## 🛠️ Technologies Used

### Backend
- Python
- Flask

### Database
- MySQL

### Machine Learning
- Scikit-learn
- Pandas
- NumPy
- Joblib

### Frontend
- HTML
- CSS
- JavaScript

## 📁 Project Structure

```text
student_dashboard/
│
├── models/
│   ├── model.pkl
│   ├── rf_model.pkl
│   ├── gb_model.pkl
│   ├── lr_model.pkl
│   └── scaler.pkl
│
├── data/
│   └── student_data.csv
│
├── src/
│   ├── __init__.py
│   ├── db.py
│   ├── init_db.py
│   ├── preprocess.py
│   ├── seed_db.py
│   ├── train_models.py
│   └── utils.py
│
├── static/
│   ├── main.js
│   └── style.css
│
├── templates/
│   ├── analytics.html
│   ├── base.html
│   ├── comparison.html
│   ├── index.html
│   └── predict.html
│
├── app.py
├── check_accuracy.py
├── config.py
├── evaluate_models.py
├── generate_data.py
└── requirements.txt
