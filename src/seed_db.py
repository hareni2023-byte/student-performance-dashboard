import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import mysql.connector
from config import Config

def seed_data():
    try:
        conn = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DB
        )
        cursor = conn.cursor()

        sample_students = [
            ('Alex Smith', 88.5, 4.5, 82.0, 78.0, 8.2, 85.0, 9, 'Good', 'RandomForestClassifier'),
            ('Emma Watson', 95.0, 6.0, 91.0, 89.0, 9.4, 92.0, 10, 'Excellent', 'RandomForestClassifier'),
            ('John Doe', 52.0, 1.5, 45.0, 48.0, 5.5, 40.0, 4, 'At Risk', 'DecisionTreeClassifier'),
            ('Sarah Connor', 74.0, 3.2, 68.0, 70.0, 7.1, 75.0, 7, 'Average', 'LogisticRegression')
        ]

        query = """
        INSERT INTO predictions 
        (student_name, attendance, study_hours, assignment_score, internal_score, previous_gpa, participation_score, assignments_completed, prediction, model_used)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        cursor.executemany(query, sample_students)
        conn.commit()
        print(f"Successfully inserted {cursor.rowcount} sample records into MySQL database!")

        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print(f"Error seeding database: {err}")

if __name__ == '__main__':
    seed_data()