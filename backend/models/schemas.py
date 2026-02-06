from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class SchoolCreate(BaseModel):
    name: str
    atpt_code: str
    sd_code: str
    school_type: str = "high"
    color: str = "#f97316"

class SchoolUpdate(BaseModel):
    name: Optional[str] = None
    color: Optional[str] = None
    enabled: Optional[bool] = None

class SchoolResponse(BaseModel):
    id: int
    name: str
    atpt_code: str
    sd_code: str
    school_type: str
    color: str
    enabled: bool
    last_sync_at: Optional[str]
    created_at: str
    event_count: Optional[int] = 0

class EventResponse(BaseModel):
    id: int
    school_id: int
    school_name: str
    school_color: str
    date: str
    end_date: Optional[str]
    title: str
    category: str
    source: str

class ExamPeriod(BaseModel):
    school_id: int
    school_name: str
    school_color: str
    title: str
    start_date: str
    end_date: str

class CalendarResponse(BaseModel):
    year: int
    month: int
    events: List[EventResponse]
    exam_periods: List[ExamPeriod]

class SyncResult(BaseModel):
    school_id: int
    synced_count: int
    new_count: int
    updated_count: int
    synced_at: str

class SchoolSearchResult(BaseModel):
    atpt_code: str
    sd_code: str
    name: str
    school_type: str
    address: str
