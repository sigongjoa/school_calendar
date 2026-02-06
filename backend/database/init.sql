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
