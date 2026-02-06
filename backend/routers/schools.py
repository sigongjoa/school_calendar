from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List
from database.connection import get_db_connection
from models.schemas import SchoolCreate, SchoolUpdate, SchoolResponse, SchoolSearchResult
from services.neis_client import NeisClient
import sqlite3

router = APIRouter()

@router.get("", response_model=List[SchoolResponse])
def get_schools():
    conn = get_db_connection()
    try:
        # Join with event count
        query = """
            SELECT s.*, COUNT(e.id) as event_count
            FROM schools s
            LEFT JOIN events e ON s.id = e.school_id
            GROUP BY s.id
        """
        rows = conn.execute(query).fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()

@router.post("", response_model=SchoolResponse, status_code=201)
def create_school(school: SchoolCreate):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO schools (name, atpt_code, sd_code, school_type, color)
            VALUES (?, ?, ?, ?, ?)
            """,
            (school.name, school.atpt_code, school.sd_code, school.school_type, school.color)
        )
        school_id = cursor.lastrowid
        conn.commit()
        
        # Fetch created
        row = conn.execute("SELECT *, 0 as event_count FROM schools WHERE id = ?", (school_id,)).fetchone()
        return dict(row)
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=409, detail="이미 등록된 학교입니다.")
    finally:
        conn.close()

@router.patch("/{school_id}", response_model=SchoolResponse)
def update_school(school_id: int, school: SchoolUpdate):
    conn = get_db_connection()
    try:
        updates = []
        values = []
        if school.name is not None:
            updates.append("name = ?")
            values.append(school.name)
        if school.color is not None:
            updates.append("color = ?")
            values.append(school.color)
        if school.enabled is not None:
            updates.append("enabled = ?")
            values.append(1 if school.enabled else 0) # SQLite boolean handling
            
        if not updates:
            row = conn.execute("""
                SELECT s.*, COUNT(e.id) as event_count
                FROM schools s
                LEFT JOIN events e ON s.id = e.school_id
                WHERE s.id = ?
                GROUP BY s.id
            """, (school_id,)).fetchone()
            if not row:
                raise HTTPException(status_code=404, detail="School not found")
            return dict(row)
            
        values.append(school_id)
        conn.execute(f"UPDATE schools SET {', '.join(updates)} WHERE id = ?", values)
        conn.commit()
        
        row = conn.execute("""
            SELECT s.*, COUNT(e.id) as event_count
            FROM schools s
            LEFT JOIN events e ON s.id = e.school_id
            WHERE s.id = ?
            GROUP BY s.id
        """, (school_id,)).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="School not found")
        return dict(row)
    finally:
        conn.close()

@router.delete("/{school_id}", status_code=204)
def delete_school(school_id: int):
    conn = get_db_connection()
    try:
        # Check existence
        row = conn.execute("SELECT id FROM schools WHERE id = ?", (school_id,)).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="School not found")
            
        conn.execute("DELETE FROM schools WHERE id = ?", (school_id,))
        conn.commit()
    finally:
        conn.close()

@router.get("/search", response_model=List[SchoolSearchResult])
async def search_schools(keyword: str = Query(..., min_length=2)):
    client = NeisClient()
    results = await client.search_school(keyword)
    return results
