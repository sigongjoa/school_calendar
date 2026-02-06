# 08. 컴포넌트 설계

## 컴포넌트 트리

```
App
├── Header
│   ├── Logo + 앱명
│   ├── Nav Links (캘린더 | 학교관리)
│   └── SearchInput (선택)
│
├── CalendarPage (/)
│   ├── SchoolToggleList (사이드바)
│   │   └── SchoolToggleItem × N
│   ├── CalendarNav
│   ├── CalendarGrid
│   │   ├── CalendarHeader (요일)
│   │   └── CalendarCell × 35~42
│   │       ├── ExamPeriodBar × 0~N
│   │       └── EventBadge × 0~N
│   └── Legend
│
├── SchoolSchedulePage (/schools)
│   ├── SchoolListSidebar
│   │   └── SchoolListItem × N
│   ├── ScheduleTable
│   │   ├── ScheduleRow × N
│   │   │   └── CategoryBadge
│   │   └── LoadMoreButton
│   └── StatsCards (× 3)
│
└── SchoolAddModal (공통)
    ├── SearchInput
    ├── SearchResultList
    └── ColorPicker
```

---

## 컴포넌트 상세

### Header

```typescript
// components/layout/Header.tsx
interface HeaderProps {
  currentPath: string;  // react-router의 현재 경로
}

// 네비게이션 링크:
// - "/" → "일정 캘린더" (CalendarPage)
// - "/schools" → "학교 관리" (SchoolSchedulePage)
// 현재 페이지는 text-primary font-bold, 나머지는 기본
```

**구현 포인트**:
- `useLocation()` 으로 현재 경로 파악
- `<Link>` 컴포넌트로 페이지 전환
- 반응형 불필요 (데스크톱 전용)

---

### SchoolToggleList (캘린더 사이드바)

```typescript
// components/school/SchoolToggleList.tsx

// Props 없음 - Zustand 스토어에서 직접 읽음

// 내부 로직:
// const { schools, toggleSchool } = useSchoolStore();
// schools.map(school => <SchoolToggleItem ... />)
```

### SchoolToggleItem

```typescript
interface SchoolToggleItemProps {
  school: School;
  onToggle: (id: string) => void;
}

// 렌더링:
// <label>
//   <input type="checkbox" checked={school.enabled} onChange={...} />
//   <span>{school.name}</span>
//   <div className="w-2 h-2 rounded-full" style={{background: school.color}} />
// </label>
```

**Tailwind 클래스** (디자인 시안 기반):
```
label: "flex items-center gap-3 px-3 py-2 rounded-lg bg-gray-50 cursor-pointer
        border border-transparent hover:border-primary/30 transition-all"
checkbox: "rounded border-gray-300 text-primary focus:ring-primary"
name: "text-sm font-medium"
dot: "ml-auto w-2 h-2 rounded-full"
```

---

### CalendarNav

```typescript
// components/calendar/CalendarNav.tsx

// Zustand에서 읽음:
// const { currentYear, currentMonth, viewType, goToPrev, goToNext, goToToday, setViewType } = useCalendarStore();

// 렌더링:
// 1. 페이지 제목 + "2026년 3월"
// 2. 뷰 토글 라디오 (일간/주간/월간) - MVP에서는 월간만 active
// 3. ◀ [오늘] ▶ 버튼
```

**뷰 토글 Tailwind** (디자인 시안 기반):
```
wrapper: "flex h-10 w-64 items-center justify-center rounded-lg bg-[#f0f2f4] p-1"
label:   "flex cursor-pointer h-full grow items-center justify-center rounded-lg px-2
          has-[:checked]:bg-white has-[:checked]:shadow-sm
          has-[:checked]:text-[#111318] text-[#616f89] text-sm font-medium"
```

---

### CalendarGrid

```typescript
// components/calendar/CalendarGrid.tsx

interface CalendarGridProps {
  days: CalendarDay[];     // 35~42일 (6주 고정 권장)
  examPeriods: ExamBar[];
}

// 렌더링:
// <div className="grid grid-cols-7">
//   <CalendarHeader />
//   {days.map(day => <CalendarCell key={day.date} day={day} />)}
// </div>
```

**날짜 계산 로직** (`utils/calendar.ts`):

```typescript
import { startOfMonth, endOfMonth, startOfWeek, endOfWeek, eachDayOfInterval, format, isToday, isSameMonth, isSaturday, isSunday } from 'date-fns';

export function getCalendarDays(year: number, month: number): CalendarDay[] {
  const monthStart = startOfMonth(new Date(year, month - 1));
  const monthEnd = endOfMonth(monthStart);
  const calStart = startOfWeek(monthStart, { weekStartsOn: 0 }); // 일요일 시작
  const calEnd = endOfWeek(monthEnd, { weekStartsOn: 0 });

  return eachDayOfInterval({ start: calStart, end: calEnd }).map(date => ({
    date: format(date, 'yyyy-MM-dd'),
    dayOfMonth: date.getDate(),
    isCurrentMonth: isSameMonth(date, monthStart),
    isToday: isToday(date),
    isWeekend: isSaturday(date) || isSunday(date),
    isSunday: isSunday(date),
    isSaturday: isSaturday(date),
    events: [],      // 나중에 채움
    examBars: [],    // 나중에 채움
  }));
}
```

---

### CalendarCell

```typescript
// components/calendar/CalendarCell.tsx

interface CalendarCellProps {
  day: CalendarDay;
}

// 렌더링 구조:
// <div className={셀 스타일}>
//   {day.examBars.map(bar => <ExamPeriodBar ... />)}
//   <span className={날짜 스타일}>{day.dayOfMonth}</span>
//   {day.events.slice(0, 3).map(ev => <EventBadge ... />)}
//   {day.events.length > 3 && <span>+{day.events.length - 3} 더보기</span>}
// </div>
```

**셀 스타일 로직**:
```typescript
const cellClass = clsx(
  'border-r border-b border-[#f0f2f4] p-2 flex flex-col gap-1 min-h-[140px] relative',
  {
    'bg-gray-50 text-[#d1d5db]': !day.isCurrentMonth,
    'bg-primary/5 border-primary/30': day.isToday,
  }
);

const dateClass = clsx('text-sm font-bold', {
  'text-red-500': day.isSunday,
  'text-blue-500': day.isSaturday,
  'text-primary': day.isToday,
  'text-[#d1d5db]': !day.isCurrentMonth,
});
```

---

### ExamPeriodBar

```typescript
// components/calendar/ExamPeriodBar.tsx

interface ExamPeriodBarProps {
  color: string;       // 학교 색상
  title: string;       // 호버 시 표시
}

// 렌더링:
// <div
//   className="absolute top-0 left-0 right-0 h-1 z-10"
//   style={{ backgroundColor: color }}
//   title={title}
// />
```

---

### EventBadge

```typescript
// components/calendar/EventBadge.tsx

interface EventBadgeProps {
  event: SchoolEvent;
  school: School;
}

// 렌더링: 카테고리별 스타일
// <div className={카테고리 스타일}>
//   {school.name.slice(0, 3)}: {event.title}
// </div>
```

**카테고리별 Tailwind** (디자인 시안 기반):
```typescript
const styles: Record<EventCategory, string> = {
  exam:           'bg-red-50 text-red-600 border-l-2 border-red-400',
  holiday:        'bg-green-50 text-green-600',
  school_holiday: 'bg-blue-50 text-blue-600',
  vacation:       'bg-purple-50 text-purple-600',
  event:          'bg-orange-50 text-orange-600',
  other:          'bg-gray-50 text-gray-600',
};
// 공통: "px-2 py-0.5 text-[10px] font-bold rounded"
```

---

### SchoolListSidebar (학교관리 페이지)

```typescript
// components/school/SchoolListSidebar.tsx

// Props 없음 - Zustand에서 읽음

// const { schools } = useSchoolStore();
// const [selectedId, setSelectedId] = useState(schools[0]?.id);

// 선택된 학교: bg-primary/10 border-l-4 border-primary text-primary font-bold
// 미선택:      hover:bg-gray-100 cursor-pointer
```

---

### ScheduleTable

```typescript
// components/schedule/ScheduleTable.tsx

interface ScheduleTableProps {
  events: SchoolEvent[];
  schoolName: string;
}

// 테이블 컬럼: 날짜 | 구분 | 이벤트명 | 상태 | 관리
// <table> 기반, 디자인 시안의 스타일 재활용
```

### CategoryBadge

```typescript
// components/schedule/CategoryBadge.tsx

interface CategoryBadgeProps {
  category: EventCategory;
}

// CATEGORY_CONFIG에서 스타일 가져옴
// "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-bold"
// + bgColor + textColor
```

### StatsCards

```typescript
// components/schedule/StatsCards.tsx

interface StatsCardsProps {
  monthEventCount: number;
  remainingHolidays: number;
  totalHolidays: number;
  lastSyncAt: string | null;
}

// 3열 그리드: grid grid-cols-1 md:grid-cols-3 gap-6
// 카드 스타일: bg-white p-6 rounded-xl border border-gray-100 shadow-sm
```

---

### SchoolAddModal

```typescript
// components/school/SchoolAddModal.tsx

interface SchoolAddModalProps {
  isOpen: boolean;
  onClose: () => void;
  onAdded: (school: School) => void;
}

// 내부 상태:
// - keyword: string (검색어)
// - results: SchoolSearchResult[] (검색 결과)
// - selected: SchoolSearchResult | null (선택된 학교)
// - selectedColor: string (선택된 색상)
// - loading: boolean
// - step: 'search' | 'confirm'

// 플로우:
// 1. 검색어 입력 → 검색 → 결과 목록
// 2. 학교 선택 → 색상 선택
// 3. "추가" → API 호출 → onAdded 콜백 → 모달 닫기
```
