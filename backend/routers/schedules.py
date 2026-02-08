from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from datetime import date, datetime
from database.connection import get_db_connection
from models.schemas import EventResponse, CalendarResponse, SyncResult, ExamPeriod
from services.neis_client import NeisClient
import json

router = APIRouter()

@router.get("", response_model=List[EventResponse])
def get_schedules(
    school_id: Optional[int] = None,
    school_ids: Optional[str] = None,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
    category: Optional[str] = None
):
    conn = get_db_connection()
    try:
        clauses = []
        params = []
        
        if school_id:
            clauses.append("e.school_id = ?")
            params.append(school_id)
        
        if school_ids:
            # Safe integer parsing
            ids = [int(x) for x in school_ids.split(",") if x.isdigit()]
            if ids:
                placeholders = ",".join("?" * len(ids))
                clauses.append(f"e.school_id IN ({placeholders})")
                params.extend(ids)
                
        if from_date:
            clauses.append("e.date >= ?")
            params.append(from_date)
            
        if to_date:
            clauses.append("e.date <= ?")
            params.append(to_date)
            
        if category:
            clauses.append("e.category = ?")
            params.append(category)
            
        where = "WHERE " + " AND ".join(clauses) if clauses else ""
        
        query = f"""
            SELECT e.*, s.name as school_name, s.color as school_color
            FROM events e
            JOIN schools s ON e.school_id = s.id
            {where}
            ORDER BY e.date
        """
        
        rows = conn.execute(query, params).fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()

@router.get("/calendar", response_model=CalendarResponse)
def get_calendar_events(year: int, month: int):
    # Calculate start/end of month
    # Actually, for calendar view we usually need leading/trailing days from prev/next month
    # But specification says year/month param. Let's return events for that month.
    # We might want to handle padded days if frontend requests, but strict month filter for now.
    
    start_date = f"{year}-{month:02d}-01"
    # End date calculation is a bit tricky without calendar lib, let's just grab enough
    if month == 12:
        end_date = f"{year+1}-01-01" # Exclusive usually better for range, but we use string compare
        # Let's say <= end of month. 
        # Easier: e.date LIKE 'year-month-%'
    else:
        end_date = f"{year}-{month+1:02d}-01"

    # We can use strftime
    month_str = f"{year}-{month:02d}"

    conn = get_db_connection()
    try:
        # Activate schools only
        query = """
            SELECT e.*, s.name as school_name, s.color as school_color
            FROM events e
            JOIN schools s ON e.school_id = s.id
            WHERE s.enabled = 1 AND strftime('%Y-%m', e.date) = ?
            ORDER BY e.date
        """
        rows = conn.execute(query, (month_str,)).fetchall()
        events = [dict(row) for row in rows]
        
        # Exam periods: merge continuous exam events
        # This implementation is simplified. 
        # Group by school + title, then find min start/max end.
        
        # Fetch all exams for this month
        exams = [e for e in events if e['category'] == 'exam']
        
        # We need a robust logic, but for now simple aggregation:
        # Group by (school_id, title)
        grouped = {}
        for ex in exams:
            key = (ex['school_id'], ex['title'])
            if key not in grouped:
                grouped[key] = []
            grouped[key].append(ex)
            
        exam_periods = []
        for (sid, title), group in grouped.items():
            # Simply take min/max date.
            # Warning: if "Midterms" are split by a weekend, is it one period? Yes usually.
            dates = sorted([e['date'] for e in group])
            school_color = group[0]['school_color']
            school_name = group[0]['school_name']
            
            exam_periods.append({
                "school_id": sid,
                "school_name": school_name,
                "school_color": school_color,
                "title": title,
                "start_date": dates[0],
                "end_date": dates[-1]
            })

        return {
            "year": year,
            "month": month,
            "events": events,
            "exam_periods": exam_periods
        }
    finally:
        conn.close()

@router.post("/sync/{school_id}", response_model=SyncResult)
async def sync_school_schedule(school_id: int):
    conn = get_db_connection()
    try:
        school = conn.execute("SELECT * FROM schools WHERE id = ?", (school_id,)).fetchone()
        if not school:
            raise HTTPException(status_code=404, detail="School not found")
        
        # Calculate academic year (March to next Feb)
        today = date.today()
        year = today.year if today.month >= 3 else today.year - 1
        from_date = date(year, 3, 1)
        to_date = date(year + 1, 2, 28)
        
        client = NeisClient()
        events_data = await client.fetch_schedule(
            school["atpt_code"], 
            school["sd_code"], 
            from_date, 
            to_date
        )
        
        # DB Upsert/Replace strategy
        # Spec says: "Delete existing neis source events and re-insert"
        # This is safer to remove deleted events.
        
        cursor = conn.cursor()
        
        # 1. Delete existing neis events for this school in range
        cursor.execute(
            """
            DELETE FROM events 
            WHERE school_id = ? 
            AND source = 'neis' 
            AND date BETWEEN ? AND ?
            """,
            (school_id, from_date.isoformat(), to_date.isoformat())
        )
        
        # 2. Insert new
        new_count = 0
        for ev in events_data:
            cursor.execute(
                """
                INSERT INTO events (school_id, date, title, category, source, raw)
                VALUES (?, ?, ?, ?, 'neis', ?)
                """,
                (school_id, ev['date'], ev['title'], ev['category'], json.dumps(ev['raw']))
            )
            new_count += 1
            
        # Update last_sync_at
        now_iso = datetime.now().isoformat()
        cursor.execute("UPDATE schools SET last_sync_at = ? WHERE id = ?", (now_iso, school_id))
        
        conn.commit()
        
        return {
            "school_id": school_id,
            "synced_count": len(events_data),
            "new_count": new_count, # Simplified: all inserted are counted as new in this logic
            "updated_count": 0,
            "synced_at": now_iso
        }
        
    finally:
        conn.close()

@router.post("/sync-all")
async def sync_all_schools():
    try:
        # Helper to iterate all schools and calling logic similar to above.
        conn = get_db_connection()
        schools = conn.execute("SELECT id FROM schools").fetchall()
        conn.close()
        
        results = []
        total = 0
        now_iso = datetime.now().isoformat()

        for row in schools:
            res = await sync_school_schedule(row['id'])
            results.append(res)
            total += res["synced_count"]
            
        return {
            "results": results,
            "total_synced": total,
            "synced_at": now_iso
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
