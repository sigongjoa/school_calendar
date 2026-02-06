import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "school_calendar.db")
SQL_PATH = os.path.join(os.path.dirname(__file__), "init.sql")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    with open(SQL_PATH, "r", encoding="utf-8") as f:
        schema = f.read()
        
    conn = get_db_connection()
    try:
        conn.executescript(schema)
        conn.commit()
        print(f"Database initialized at {DB_PATH}")
    finally:
        conn.close()
