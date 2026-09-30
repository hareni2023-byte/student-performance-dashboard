import mysql.connector
from config import Config

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DB
        )
        return conn
    except mysql.connector.Error as err:
        print(f"[DB ERROR] Connection failed: {err}")
        return None

def save_prediction(data):
    conn = get_db_connection()
    if conn is None:
        print("[DB ERROR] Save failed: No database connection.")
        return None
    try:
        cursor = conn.cursor()
        query = """
        INSERT INTO predictions 
        (student_name, attendance, study_hours, assignment_score, internal_score, previous_gpa, participation_score, assignments_completed, prediction, model_used)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            data.get('student_name', 'Anonymous'),
            data['attendance'],
            data['study_hours'],
            data['assignment_score'],
            data['internal_score'],
            data['previous_gpa'],
            data['participation_score'],
            data['assignments_completed'],
            data['prediction'],
            data['model_used']
        ))
        conn.commit()
        
        # Retrieve primary key ID of newly created row
        inserted_id = cursor.lastrowid
        print(f"[DB SUCCESS] Recorded prediction for: {data.get('student_name', 'Anonymous')} (ID: {inserted_id})")
        
        cursor.close()
        conn.close()
        return inserted_id
    except mysql.connector.Error as err:
        print(f"[DB ERROR] Failed to insert prediction: {err}")
        return None

def fetch_recent_predictions(limit=10):
    conn = get_db_connection()
    if conn is None:
        return []
    try:
        cursor = conn.cursor(dictionary=True)
        query = """
        SELECT id, student_name, attendance, study_hours, assignment_score, 
               internal_score, previous_gpa, prediction, model_used, created_at 
        FROM predictions 
        ORDER BY created_at DESC 
        LIMIT %s
        """
        cursor.execute(query, (limit,))
        records = cursor.fetchall()
        cursor.close()
        conn.close()
        return records
    except mysql.connector.Error as err:
        print(f"[DB ERROR] Failed to fetch predictions: {err}")
        return []

def delete_prediction(record_id):
    conn = get_db_connection()
    if conn is None:
        print("[DB ERROR] Delete failed: No database connection.")
        return False
    try:
        cursor = conn.cursor()
        query = "DELETE FROM predictions WHERE id = %s"
        cursor.execute(query, (record_id,))
        conn.commit()
        print(f"[DB SUCCESS] Successfully deleted prediction record ID: {record_id}")
        cursor.close()
        conn.close()
        return True
    except mysql.connector.Error as err:
        print(f"[DB ERROR] Failed to delete record ID {record_id}: {err}")
        return False