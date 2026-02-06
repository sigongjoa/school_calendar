# 06. 백엔드 API 명세

## 서버 설정

- 프레임워크: FastAPI
- 포트: `8015`
- DB: SQLite (`backend/data/school_calendar.db`)
- CORS: `http://localhost:5173` 허용 (Vite dev server)

## 엔트리포인트

`backend/main.py`:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import schools, schedules
from database.connection import init_db

app = FastAPI(title="School Calendar API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(schools.router, prefix="/api/schools", tags=["schools"])
app.include_router(schedules.router, prefix="/api/schedules", tags=["schedules"])

@app.on_event("startup")
async def startup():
    init_db()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8015)
```

---

## API 엔드포인트 목록

### 학교 관리

| Method | Path | 설명 |
|--------|------|------|
| GET | `/api/schools` | 등록된 학교 목록 조회 |
| POST | `/api/schools` | 학교 등록 |
| PATCH | `/api/schools/{id}` | 학교 정보 수정 (색상, 활성화 등) |
| DELETE | `/api/schools/{id}` | 학교 삭제 |
| GET | `/api/schools/search?keyword=` | 나이스 API 학교 검색 |

### 학사일정

| Method | Path | 설명 |
|--------|------|------|
| GET | `/api/schedules` | 일정 조회 (필터: 학교, 기간, 카테고리) |
| GET | `/api/schedules/calendar?year=&month=` | 캘린더 뷰용 월별 일정 |
| POST | `/api/schedules/sync/{school_id}` | 특정 학교 일정 동기화 |
| POST | `/api/schedules/sync-all` | 전체 학교 일정 동기화 |

---

## 상세 API 명세

### GET /api/schools

등록된 모든 학교 목록 반환.

**응답 200**:
```json
[
  {
    "id": 1,
    "name": "대치고등학교",
    "atpt_code": "B10",
    "sd_code": "7010057",
    "school_type": "high",
    "color": "#f97316",
    "enabled": true,
    "last_sync_at": "2026-02-06T14:32:00",
    "created_at": "2026-02-01T10:00:00",
    "event_count": 45
  }
]
```

> `event_count`는 JOIN으로 해당 학교의 이벤트 수를 포함.

---

### POST /api/schools

학교 등록 (나이스 검색 결과에서 선택한 학교).

**요청**:
```json
{
  "name": "대치고등학교",
  "atpt_code": "B10",
  "sd_code": "7010057",
  "school_type": "high",
  "color": "#f97316"
}
```

**응답 201**:
```json
{
  "id": 1,
  "name": "대치고등학교",
  "atpt_code": "B10",
  "sd_code": "7010057",
  "school_type": "high",
  "color": "#f97316",
  "enabled": true,
  "last_sync_at": null,
  "created_at": "2026-02-06T10:00:00"
}
```

**에러 409** (이미 등록된 학교):
```json
{ "detail": "이미 등록된 학교입니다." }
```

---

### PATCH /api/schools/{id}

학교 정보 부분 수정.

**요청** (변경할 필드만):
```json
{
  "color": "#3b82f6",
  "enabled": false
}
```

**응답 200**: 수정된 학교 객체 전체.

---

### DELETE /api/schools/{id}

학교 및 관련 이벤트 모두 삭제 (CASCADE).

**응답 204**: No Content

---

### GET /api/schools/search?keyword={학교명}

나이스 API를 통해 학교 검색. DB에 저장하지 않음 (프록시).

**응답 200**:
```json
[
  {
    "atpt_code": "B10",
    "sd_code": "7010057",
    "name": "대치고등학교",
    "school_type": "high",
    "address": "서울특별시 강남구 역삼로 ..."
  },
  {
    "atpt_code": "B10",
    "sd_code": "7010058",
    "name": "대치중학교",
    "school_type": "middle",
    "address": "서울특별시 강남구 ..."
  }
]
```

---

### GET /api/schedules

일정 조회. 쿼리 파라미터로 필터링.

**쿼리 파라미터**:
| 파라미터 | 타입 | 필수 | 설명 |
|----------|------|------|------|
| school_id | int | X | 특정 학교만 필터 |
| school_ids | string | X | 콤마 구분 학교 ID들 "1,2,3" |
| from_date | string | X | 시작일 "2026-03-01" |
| to_date | string | X | 종료일 "2026-03-31" |
| category | string | X | 카테고리 필터 "exam,holiday" |

**응답 200**:
```json
[
  {
    "id": 1,
    "school_id": 1,
    "school_name": "대치고등학교",
    "school_color": "#f97316",
    "date": "2026-04-18",
    "end_date": "2026-04-22",
    "title": "1학기 중간고사",
    "category": "exam",
    "source": "neis"
  }
]
```

---

### GET /api/schedules/calendar?year=2026&month=3

캘린더 뷰에 최적화된 월별 일정. 활성화된 학교의 일정만 반환.

**쿼리 파라미터**:
| 파라미터 | 타입 | 필수 | 기본값 |
|----------|------|------|--------|
| year | int | O | - |
| month | int | O | - |

**응답 200**:
```json
{
  "year": 2026,
  "month": 3,
  "events": [
    {
      "id": 1,
      "school_id": 1,
      "school_name": "대치고등학교",
      "school_color": "#f97316",
      "date": "2026-03-01",
      "end_date": null,
      "title": "삼일절",
      "category": "holiday"
    }
  ],
  "exam_periods": [
    {
      "school_id": 1,
      "school_name": "대치고등학교",
      "school_color": "#f97316",
      "title": "1학기 중간고사",
      "start_date": "2026-04-18",
      "end_date": "2026-04-22"
    }
  ]
}
```

> `exam_periods`는 연속된 시험 이벤트를 병합한 결과. 캘린더 상단 바 표시에 사용.

---

### POST /api/schedules/sync/{school_id}

특정 학교의 학사일정을 나이스 API에서 가져와 DB에 동기화.

**요청**: Body 없음 (현재 학년도 전체를 동기화)

**응답 200**:
```json
{
  "school_id": 1,
  "synced_count": 45,
  "new_count": 3,
  "updated_count": 0,
  "synced_at": "2026-02-06T14:32:00"
}
```

---

### POST /api/schedules/sync-all

등록된 모든 학교의 일정을 동기화.

**응답 200**:
```json
{
  "results": [
    { "school_id": 1, "synced_count": 45, "new_count": 3 },
    { "school_id": 2, "synced_count": 38, "new_count": 0 }
  ],
  "total_synced": 83,
  "synced_at": "2026-02-06T14:32:00"
}
```

---

## Pydantic 모델

`backend/models/schemas.py`:

```python
from pydantic import BaseModel
from typing import Optional
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
    events: list[EventResponse]
    exam_periods: list[ExamPeriod]

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
```
