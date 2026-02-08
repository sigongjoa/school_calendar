export type SchoolType = 'elementary' | 'middle' | 'high' | 'special';

export const SCHOOL_TYPE_LABELS: Record<SchoolType, string> = {
    elementary: '초등학교',
    middle: '중학교',
    high: '고등학교',
    special: '특수/영재학교',
};

export interface School {
    id: number;                // Backend uses integer ID
    name: string;              // "대치고등학교"
    atpt_code: string;         // "B10" - Snake case from backend
    sd_code: string;           // "7010057"
    school_type: SchoolType;
    color: string;             // hex
    enabled: boolean;
    last_sync_at: string | null; // ISO 8601
    created_at: string;
    event_count: number;
}

export type EventCategory =
    | 'exam'
    | 'holiday'
    | 'school_holiday'
    | 'vacation'
    | 'event'
    | 'other';

export const CATEGORY_CONFIG: Record<EventCategory, { label: string; bgColor: string; textColor: string; borderColor: string }> = {
    exam: { label: '시험', bgColor: 'bg-red-100', textColor: 'text-red-700', borderColor: 'border-red-400' },
    holiday: { label: '공휴일', bgColor: 'bg-green-100', textColor: 'text-green-700', borderColor: 'border-green-400' },
    school_holiday: { label: '학교휴일', bgColor: 'bg-blue-100', textColor: 'text-blue-700', borderColor: 'border-blue-400' },
    vacation: { label: '방학', bgColor: 'bg-purple-100', textColor: 'text-purple-700', borderColor: 'border-purple-400' },
    event: { label: '학교행사', bgColor: 'bg-orange-100', textColor: 'text-orange-700', borderColor: 'border-orange-400' },
    other: { label: '기타', bgColor: 'bg-gray-100', textColor: 'text-gray-700', borderColor: 'border-gray-400' },
};

export interface SchoolEvent {
    id: number;
    school_id: number;
    school_name: string;
    school_color: string;
    date: string;              // "2026-03-02"
    end_date: string | null;
    title: string;
    category: EventCategory;
    source: 'neis' | 'manual';
}

export interface ExamPeriod {
    school_id: number;
    school_name: string;
    school_color: string;
    title: string;
    start_date: string;
    end_date: string;
}

export interface CalendarDay {
    date: string;             // "2026-03-15"
    dayOfMonth: number;
    isCurrentMonth: boolean;
    isToday: boolean;
    isWeekend: boolean;
    isSunday: boolean;
    isSaturday: boolean;
    events: CalendarEvent[];
    examBars: ExamBar[];
}

export interface CalendarEvent {
    event: SchoolEvent;
    // School info is already inside event response from backend (joined)
}

export interface ExamBar {
    schoolId: number;
    schoolName: string;
    color: string;
    title: string;
    isStart: boolean;
    isEnd: boolean;
    isMid: boolean;
    row: number;              // To handle overlapping bars
}

export interface SchoolSearchRequest {
    keyword: string;
}

export interface SchoolSearchResult {
    atpt_code: string;
    sd_code: string;
    name: string;
    address: string;
    school_type: SchoolType;
}

export interface SyncResult {
    school_id: number;
    synced_count: number;
    new_count: number;
    updated_count: number;
    synced_at: string;
}

export interface SchoolCreate {
    name: string;
    atpt_code: string;
    sd_code: string;
    school_type: SchoolType;
    color?: string;
}

export interface SchoolUpdate {
    name?: string;
    atpt_code?: string;
    sd_code?: string;
    school_type?: SchoolType;
    color?: string;
    enabled?: boolean;
}

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

export interface CalendarResponse {
    events: SchoolEvent[];
    exam_periods: ExamPeriod[];
}
