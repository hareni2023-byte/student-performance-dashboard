# Student Performance Dashboard

An ML-based web dashboard for analyzing and predicting student performance using academic and engagement-related features.

## 🚧 Project Status

This project is currently under development.

The core machine learning pipeline, database integration, and dashboard structure have been developed. Additional testing, improvements, and final integration are still in progress.

## 📌 Project Overview

The Student Performance Dashboard combines:

- Machine Learning
- Flask Web Application
- MySQL Database
- Data Preprocessing
- Student Performance Analytics
- Performance Prediction

The system uses student academic and engagement information to predict student performance and provide analytical insights through a web dashboard.

## 🤖 Machine Learning Algorithms

Three classification algorithms are trained and compared:

1. Random Forest Classifier
2. Gradient Boosting Classifier
3. Logistic Regression

The models are optimized using:

- GridSearchCV
- 3-Fold Stratified Cross-Validation

The best-performing tuned model is selected as the final model.

## 📊 Evaluation Metrics

The models are evaluated using:

- Accuracy
- Precision
- Recall
- F1-Score

## 🗄️ Database

MySQL is used to store and manage student-related application data.

Database-related components include:

- Database connection
- Database initialization
- Data seeding
- Student data management

## 🛠️ Technologies Used

- Python
- Flask
- MySQL
- Pandas
- NumPy
- Scikit-learn
- Joblib
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
