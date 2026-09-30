import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'student-analytics-secret-key-2026')
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'starlight123')  # Ensure this is correct
    MYSQL_DB = os.environ.get('MYSQL_DB', 'student_analytics')