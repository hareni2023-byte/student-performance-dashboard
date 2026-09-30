import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import mysql.connector
from config import Config

def init_database():
    try:
        conn = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD
        )
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {Config.MYSQL_DB}")
        cursor.execute(f"USE {Config.MYSQL_DB}")
        
        create_table_query = """
        CREATE TABLE IF NOT EXISTS predictions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            student_name VARCHAR(100) NOT NULL,
            attendance FLOAT NOT NULL,
            study_hours FLOAT NOT NULL,
            assignment_score FLOAT NOT NULL,
            internal_score FLOAT NOT NULL,
            previous_gpa FLOAT NOT NULL,
            participation_score FLOAT NOT NULL,
            assignments_completed INT NOT NULL,
            prediction VARCHAR(50) NOT NULL,
            model_used VARCHAR(50) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        cursor.execute(create_table_query)
        print("Database & table initialized successfully!")
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print(f"Error initializing DB: {err}")

if __name__ == '__main__':
    init_database()