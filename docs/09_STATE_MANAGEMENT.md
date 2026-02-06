# 09. 상태 관리 (Zustand)

## 스토어 구조

3개의 독립 스토어로 관심사 분리:

| 스토어 | 역할 | 주요 상태 |
|--------|------|-----------|
| `useSchoolStore` | 학교 목록, 토글 | schools, selectedSchoolId |
| `useCalendarStore` | 캘린더 네비게이션 | year, month, viewType |
| `useScheduleStore` | 학사일정 데이터 | events, examPeriods, loading |

---

## useSchoolStore

```typescript
// stores/useSchoolStore.ts
import { create } from 'zustand';
import { School } from '../types';
import { schoolApi } from '../services/schoolApi';

interface SchoolState {
  // 상태
  schools: School[];
  selectedSchoolId: string | null;  // SchoolSchedulePage에서 선택된 학교
  isAddModalOpen: boolean;
  loading: boolean;
  error: string | null;

  // 액션
  fetchSchools: () => Promise<void>;
  toggleSchool: (id: string) => void;
  selectSchool: (id: string) => void;
  addSchool: (data: SchoolCreate) => Promise<School>;
  updateSchool: (id: string, data: Partial<School>) => Promise<void>;
  deleteSchool: (id: string) => Promise<void>;
  setAddModalOpen: (open: boolean) => void;

  // 파생 (getter)
  getEnabledSchools: () => School[];
  getEnabledSchoolIds: () => string[];
}

export const useSchoolStore = create<SchoolState>((set, get) => ({
  schools: [],
  selectedSchoolId: null,
  isAddModalOpen: false,
  loading: false,
  error: null,

  fetchSchools: async () => {
    set({ loading: true, error: null });
    try {
      const schools = await schoolApi.getAll();
      set({ schools, loading: false });
      // 첫 번째 학교를 기본 선택
      if (schools.length > 0 && !get().selectedSchoolId) {
        set({ selectedSchoolId: String(schools[0].id) });
      }
    } catch (e) {
      set({ error: '학교 목록을 불러오지 못했습니다.', loading: false });
    }
  },

  toggleSchool: (id) => {
    set((state) => ({
      schools: state.schools.map((s) =>
        String(s.id) === id ? { ...s, enabled: !s.enabled } : s
      ),
    }));
    // 백엔드에도 반영 (fire-and-forget)
    const school = get().schools.find((s) => String(s.id) === id);
    if (school) {
      schoolApi.update(id, { enabled: school.enabled });
    }
  },

  selectSchool: (id) => set({ selectedSchoolId: id }),

  addSchool: async (data) => {
    const school = await schoolApi.create(data);
    set((state) => ({ schools: [...state.schools, school] }));
    return school;
  },

  updateSchool: async (id, data) => {
    await schoolApi.update(id, data);
    set((state) => ({
      schools: state.schools.map((s) =>
        String(s.id) === id ? { ...s, ...data } : s
      ),
    }));
  },

  deleteSchool: async (id) => {
    await schoolApi.delete(id);
    set((state) => ({
      schools: state.schools.filter((s) => String(s.id) !== id),
      selectedSchoolId:
        state.selectedSchoolId === id ? null : state.selectedSchoolId,
    }));
  },

  setAddModalOpen: (open) => set({ isAddModalOpen: open }),

  getEnabledSchools: () => get().schools.filter((s) => s.enabled),
  getEnabledSchoolIds: () =>
    get()
      .schools.filter((s) => s.enabled)
      .map((s) => String(s.id)),
}));
```

---

## useCalendarStore

```typescript
// stores/useCalendarStore.ts
import { create } from 'zustand';
import { CalendarViewType } from '../types';

interface CalendarState {
  // 상태
  currentYear: number;
  currentMonth: number;   // 1-12
  viewType: CalendarViewType;

  // 액션
  goToPrev: () => void;
  goToNext: () => void;
  goToToday: () => void;
  setViewType: (type: CalendarViewType) => void;
  setYearMonth: (year: number, month: number) => void;
}

export const useCalendarStore = create<CalendarState>((set) => {
  const now = new Date();
  return {
    currentYear: now.getFullYear(),
    currentMonth: now.getMonth() + 1,
    viewType: 'month',

    goToPrev: () =>
      set((state) => {
        if (state.currentMonth === 1) {
          return { currentYear: state.currentYear - 1, currentMonth: 12 };
        }
        return { currentMonth: state.currentMonth - 1 };
      }),

    goToNext: () =>
      set((state) => {
        if (state.currentMonth === 12) {
          return { currentYear: state.currentYear + 1, currentMonth: 1 };
        }
        return { currentMonth: state.currentMonth + 1 };
      }),

    goToToday: () => {
      const now = new Date();
      set({ currentYear: now.getFullYear(), currentMonth: now.getMonth() + 1 });
    },

    setViewType: (type) => set({ viewType: type }),
    setYearMonth: (year, month) => set({ currentYear: year, currentMonth: month }),
  };
});
```

---

## useScheduleStore

```typescript
// stores/useScheduleStore.ts
import { create } from 'zustand';
import { SchoolEvent, ExamPeriod } from '../types';
import { scheduleApi } from '../services/scheduleApi';

interface ScheduleState {
  // 상태 - 캘린더 뷰용
  calendarEvents: SchoolEvent[];
  examPeriods: ExamPeriod[];
  calendarLoading: boolean;

  // 상태 - 학교별 테이블용
  schoolEvents: SchoolEvent[];
  schoolEventsLoading: boolean;

  // 동기화 상태
  syncLoading: Record<string, boolean>;  // schoolId → loading

  // 액션
  fetchCalendar: (year: number, month: number) => Promise<void>;
  fetchSchoolEvents: (schoolId: string) => Promise<void>;
  syncSchool: (schoolId: string) => Promise<void>;
  syncAll: () => Promise<void>;
}

export const useScheduleStore = create<ScheduleState>((set, get) => ({
  calendarEvents: [],
  examPeriods: [],
  calendarLoading: false,

  schoolEvents: [],
  schoolEventsLoading: false,

  syncLoading: {},

  fetchCalendar: async (year, month) => {
    set({ calendarLoading: true });
    try {
      const data = await scheduleApi.getCalendar(year, month);
      set({
        calendarEvents: data.events,
        examPeriods: data.exam_periods,
        calendarLoading: false,
      });
    } catch {
      set({ calendarLoading: false });
    }
  },

  fetchSchoolEvents: async (schoolId) => {
    set({ schoolEventsLoading: true });
    try {
      const events = await scheduleApi.getBySchool(schoolId);
      set({ schoolEvents: events, schoolEventsLoading: false });
    } catch {
      set({ schoolEventsLoading: false });
    }
  },

  syncSchool: async (schoolId) => {
    set((s) => ({ syncLoading: { ...s.syncLoading, [schoolId]: true } }));
    try {
      await scheduleApi.sync(schoolId);
      // 동기화 후 데이터 새로고침
      await get().fetchSchoolEvents(schoolId);
    } finally {
      set((s) => ({ syncLoading: { ...s.syncLoading, [schoolId]: false } }));
    }
  },

  syncAll: async () => {
    await scheduleApi.syncAll();
    // 전체 새로고침은 현재 보고 있는 뷰에 따라
  },
}));
```

---

## 스토어 간 관계

```
useSchoolStore                useCalendarStore
  │ schools                     │ year, month
  │ enabledSchoolIds            │
  └──────────┬──────────────────┘
             │
             ▼
      useScheduleStore
        │ fetchCalendar(year, month)
        │ → 백엔드가 enabled 학교만 반환
        │
        │ fetchSchoolEvents(schoolId)
        │ → 특정 학교의 전체 일정
        ▼
      [React 컴포넌트에서 필터링]
      calendarEvents.filter(e => enabledSchoolIds.includes(e.schoolId))
```

## 앱 초기화 순서

```typescript
// App.tsx 또는 최상위 컴포넌트
function App() {
  const fetchSchools = useSchoolStore((s) => s.fetchSchools);
  const fetchCalendar = useScheduleStore((s) => s.fetchCalendar);
  const { currentYear, currentMonth } = useCalendarStore();

  useEffect(() => {
    // 1. 학교 목록 로드
    fetchSchools();
  }, []);

  useEffect(() => {
    // 2. 캘린더 데이터 로드 (년/월 변경 시마다)
    fetchCalendar(currentYear, currentMonth);
  }, [currentYear, currentMonth]);

  return <RouterProvider ... />;
}
```
