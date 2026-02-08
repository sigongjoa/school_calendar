import sqlite3
import json
from datetime import date, timedelta

DB_PATH = "backend/data/school_calendar.db"

def seed_data():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # 1. Clear existing schools and events (for fresh test)
    # cursor.execute("DELETE FROM events")
    # cursor.execute("DELETE FROM schools")

    # 2. Add schools
    schools = [
        ("시지중학교", "R10", "8311025", "middle", "#f97316"), # Orange
        ("시지고등학교", "R10", "8311026", "high", "#3b82f6"),  # Blue
        ("노변중학교", "R10", "8311068", "middle", "#22c55e"), # Green
        ("고산중학교", "R10", "8311082", "middle", "#ef4444")  # Red
    ]

    # Update ID 1 (대치고) if exists
    cursor.execute("UPDATE schools SET color = '#6366f1' WHERE id = 1")

    inserted_schools = []
    for name, atpt, sd, stype, color in schools:
        cursor.execute("""
            INSERT OR IGNORE INTO schools (name, atpt_code, sd_code, school_type, color, enabled)
            VALUES (?, ?, ?, ?, ?, 1)
        """, (name, atpt, sd, stype, color))
        
        # Ensure color is updated if already exists
        cursor.execute("UPDATE schools SET color = ? WHERE sd_code = ?", (color, sd))
        
        row = cursor.execute("SELECT id FROM schools WHERE sd_code = ?", (sd,)).fetchone()
        inserted_schools.append(dict(row))

    # 3. Add events for Feb and March 2026
    events = [
        # 대치고
        (1, "2026-03-02", "개학식", "event", "neis"),
        
        # 시지중
        (inserted_schools[0]['id'], "2026-02-13", "졸업식", "event", "neis"),
        (inserted_schools[0]['id'], "2026-03-02", "입학식", "event", "neis"),
        (inserted_schools[0]['id'], "2026-03-20", "학부모총회", "event", "neis"),
        
        # 시지고
        (inserted_schools[1]['id'], "2026-02-10", "종업식", "event", "neis"),
        (inserted_schools[1]['id'], "2026-03-02", "개학식", "event", "neis"),
        (inserted_schools[1]['id'], "2026-03-12", "3월 학력평가", "exam", "neis"),
        
        # 노변중
        (inserted_schools[2]['id'], "2026-03-02", "입학식", "event", "neis"),
        (inserted_schools[2]['id'], "2026-03-25", "봉사활동", "event", "neis"),
        
        # 고산중
        (inserted_schools[3]['id'], "2026-03-02", "시업식", "event", "neis"),
        (inserted_schools[3]['id'], "2026-03-05", "동아리 조직", "event", "neis"),
    ]

    for sid, dt, title, cat, src in events:
        cursor.execute("""
            INSERT OR IGNORE INTO events (school_id, date, title, category, source)
            VALUES (?, ?, ?, ?, ?)
        """, (sid, dt, title, cat, src))

    conn.commit()
    conn.close()
    print("Database seeded with school data.")

if __name__ == "__main__":
    seed_data()
