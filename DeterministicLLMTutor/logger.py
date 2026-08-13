import sqlite3
import datetime
import os

DB_PATH = "database_v2.db"

def init_db():
    """Initializes SQLite database table if it doesn't already exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            student_question TEXT NOT NULL,
            detected_topic TEXT NOT NULL,
            detected_objective TEXT NOT NULL,
            response_time_ms REAL NOT NULL,
            response_returned TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def log_interaction(
    student_question: str,
    detected_topic: str,
    detected_objective: str,
    response_time_ms: float,
    response_returned: str
):
    """Logs every tutoring interaction to the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    cursor.execute("""
        INSERT INTO audit_logs (
            timestamp, student_question, detected_topic, 
            detected_objective, response_time_ms, response_returned
        ) VALUES (?, ?, ?, ?, ?, ?)
    """, (
        timestamp, student_question, detected_topic,
        detected_objective, response_time_ms, response_returned
    ))
    conn.commit()
    conn.close()

def fetch_logs(limit: int = 50):
    """Retrieves the recent interaction history from SQLite."""
    if not os.path.exists(DB_PATH):
        init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Selecting exactly 6 columns to match app.py
    cursor.execute("""
        SELECT timestamp, student_question, detected_topic, detected_objective, 
               response_time_ms, response_returned
        FROM audit_logs
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()
    return rows