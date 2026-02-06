# 04. 데이터 모델

## TypeScript 타입 정의

`src/renderer/types/index.ts`에 정의할 타입들:

### School (학교)

```typescript
export interface School {
  id: string;                // UUID 또는 자동 증가 ID
  name: string;              // "대치고등학교"
  neisAtptCode: string;      // 교육청 코드 (예: "B10" = 서울)
  neisSdCode: string;        // 학교 코드 (예: "7010057")
  schoolType: SchoolType;    // 학교 유형
  color: string;             // 캘린더 표시 색상 (hex)
  enabled: boolean;          // 토글 on/off 상태
  lastSyncAt: string | null; // 마지막 동기화 시각 (ISO 8601)
  createdAt: string;         // 생성일
}

export type SchoolType = 'elementary' | 'middle' | 'high' | 'special';

export const SCHOOL_TYPE_LABELS: Record<SchoolType, string> = {
  elementary: '초등학교',
  middle: '중학교',
  high: '고등학교',
  special: '특수/영재학교',
};
```

### SchoolEvent (학사일정 이벤트)

```typescript
export interface SchoolEvent {
  id: string;
  schoolId: string;          // FK → School.id
  date: string;              // "2026-03-02" (시작일)
  endDate: string | null;    // "2026-03-06" (종료일, 기간 이벤트)
  title: string;             // "1학기 중간고사"
  category: EventCategory;   // 이벤트 구분
  source: 'neis' | 'manual'; // 데이터 출처
  raw: string | null;        // 나이스 API 원본 데이터 (JSON string)
}

export type EventCategory =
  | 'exam'       // 시험 (중간고사, 기말고사, 모의고사)
  | 'holiday'    // 공휴일 (설날, 추석 등)
  | 'school_holiday' // 학교 자체 휴일 (개교기념일, 재량휴업 등)
  | 'vacation'   // 방학 (여름방학, 겨울방학)
  | 'event'      // 학교행사 (입학식, 졸업식, 체육대회 등)
  | 'other';     // 기타

export const CATEGORY_CONFIG: Record<EventCategory, { label: string; bgColor: string; textColor: string; borderColor: string }> = {
  exam:           { label: '시험',     bgColor: 'bg-red-100',    textColor: 'text-red-700',    borderColor: 'border-red-400' },
  holiday:        { label: '공휴일',   bgColor: 'bg-green-100',  textColor: 'text-green-700',  borderColor: 'border-green-400' },
  school_holiday: { label: '학교휴일', bgColor: 'bg-blue-100',   textColor: 'text-blue-700',   borderColor: 'border-blue-400' },
  vacation:       { label: '방학',     bgColor: 'bg-purple-100', textColor: 'text-purple-700', borderColor: 'border-purple-400' },
  event:          { label: '학교행사', bgColor: 'bg-orange-100', textColor: 'text-orange-700', borderColor: 'border-orange-400' },
  other:          { label: '기타',     bgColor: 'bg-gray-100',   textColor: 'text-gray-700',   borderColor: 'border-gray-400' },
};
```

### CalendarDay (캘린더 셀 데이터)

```typescript
export interface CalendarDay {
  date: string;             // "2026-03-15"
  dayOfMonth: number;       // 15
  isCurrentMonth: boolean;  // 이번 달 날짜인지
  isToday: boolean;
  isWeekend: boolean;
  isSunday: boolean;
  isSaturday: boolean;
  events: CalendarEvent[];  // 이 날짜의 이벤트 목록
  examBars: ExamBar[];      // 시험 기간 바 (상단 표시)
}

export interface CalendarEvent {
  event: SchoolEvent;
  school: School;           // 어느 학교의 이벤트인지
}

export interface ExamBar {
  schoolId: string;
  schoolName: string;
  color: string;            // 학교 색상
  title: string;            // "대치고 중간고사"
  isStart: boolean;         // 이 날짜가 시험 시작일인지
  isEnd: boolean;           // 이 날짜가 시험 종료일인지
  isMid: boolean;           // 중간 날짜인지
}
```

### API 요청/응답 타입

```typescript
// 학교 검색 (나이스 API)
export interface SchoolSearchRequest {
  keyword: string;          // 학교명 검색어
}

export interface SchoolSearchResult {
  atptCode: string;         // 교육청 코드
  sdCode: string;           // 학교 코드
  name: string;             // 학교명
  address: string;          // 주소
  schoolType: SchoolType;   // 학교 유형
}

// 일정 동기화 응답
export interface SyncResult {
  schoolId: string;
  syncedCount: number;      // 동기화된 이벤트 수
  newCount: number;         // 새로 추가된 이벤트 수
  updatedCount: number;     // 업데이트된 이벤트 수
  syncedAt: string;
}

// 캘린더 뷰 타입
export type CalendarViewType = 'day' | 'week' | 'month';
```

---

## SQLite 스키마

`backend/database/init.sql`:

```sql
-- 학교 테이블
CREATE TABLE IF NOT EXISTS schools (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL,                          -- "대치고등학교"
    atpt_code   TEXT NOT NULL,                          -- 교육청 코드 "B10"
    sd_code     TEXT NOT NULL,                          -- 학교 코드 "7010057"
    school_type TEXT NOT NULL DEFAULT 'high',           -- elementary/middle/high/special
    color       TEXT NOT NULL DEFAULT '#f97316',        -- hex 색상
    enabled     INTEGER NOT NULL DEFAULT 1,             -- 0 or 1
    last_sync_at TEXT,                                  -- ISO 8601
    created_at  TEXT NOT NULL DEFAULT (datetime('now')),

    UNIQUE(atpt_code, sd_code)                          -- 같은 학교 중복 방지
);

-- 학사일정 이벤트 테이블
CREATE TABLE IF NOT EXISTS events (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    school_id   INTEGER NOT NULL REFERENCES schools(id) ON DELETE CASCADE,
    date        TEXT NOT NULL,                          -- "2026-03-02"
    end_date    TEXT,                                   -- "2026-03-06" (기간형)
    title       TEXT NOT NULL,                          -- "1학기 중간고사"
    category    TEXT NOT NULL DEFAULT 'other',          -- exam/holiday/...
    source      TEXT NOT NULL DEFAULT 'neis',           -- neis/manual
    raw         TEXT,                                   -- 나이스 원본 JSON
    created_at  TEXT NOT NULL DEFAULT (datetime('now')),

    UNIQUE(school_id, date, title)                      -- 같은 날짜+제목 중복 방지
);

-- 인덱스
CREATE INDEX IF NOT EXISTS idx_events_school_id ON events(school_id);
CREATE INDEX IF NOT EXISTS idx_events_date ON events(date);
CREATE INDEX IF NOT EXISTS idx_events_date_range ON events(date, end_date);
```

## 학교 색상 프리셋

학교 추가 시 순서대로 배정:

```typescript
export const SCHOOL_COLOR_PRESETS = [
  '#f97316', // orange
  '#3b82f6', // blue
  '#22c55e', // green
  '#ef4444', // red
  '#a855f7', // purple
  '#ec4899', // pink
  '#14b8a6', // teal
  '#f59e0b', // amber
  '#6366f1', // indigo
  '#84cc16', // lime
  '#06b6d4', // cyan
  '#e11d48', // rose
];
```

## 나이스 API → EventCategory 매핑

나이스 API 응답의 이벤트명을 기반으로 카테고리를 자동 분류:

```typescript
export function classifyEvent(eventName: string): EventCategory {
  // 시험 키워드
  if (/중간고사|기말고사|모의고사|학력평가|수능|시험/.test(eventName)) return 'exam';
  // 방학 키워드
  if (/방학|개학/.test(eventName)) return 'vacation';
  // 공휴일 키워드
  if (/설날|추석|어린이날|광복절|한글날|개천절|삼일절|석가탄신|성탄|현충일|대통령|선거/.test(eventName)) return 'holiday';
  // 학교 자체 휴일
  if (/개교기념|재량휴업|대체휴일/.test(eventName)) return 'school_holiday';
  // 학교 행사
  if (/입학|졸업|체육대회|수학여행|현장학습|학예회|수련|봉사/.test(eventName)) return 'event';
  // 기타
  return 'other';
}
```
