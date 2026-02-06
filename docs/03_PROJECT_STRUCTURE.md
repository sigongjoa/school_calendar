# 03. 프로젝트 구조

## 전체 디렉토리 트리

```
node15_school_calendar/
├── docs/                           # 개발 문서 (이 폴더)
│   ├── 00_INDEX.md
│   ├── 01_PROJECT_OVERVIEW.md
│   ├── ...
│   └── designs/                    # HTML 디자인 시안 보관
│       ├── calendar_page.html
│       └── school_schedule_page.html
│
├── backend/                        # Python 백엔드
│   ├── main.py                     # FastAPI 앱 엔트리포인트
│   ├── routers/
│   │   ├── schools.py              # 학교 CRUD API
│   │   └── schedules.py            # 학사일정 API (나이스 연동)
│   ├── services/
│   │   └── neis_client.py          # 나이스 API 클라이언트
│   ├── models/
│   │   └── schemas.py              # Pydantic 모델
│   ├── database/
│   │   ├── connection.py           # SQLite 연결
│   │   └── init.sql                # 테이블 생성 DDL
│   ├── data/
│   │   └── school_calendar.db      # SQLite DB 파일 (gitignore)
│   ├── requirements.txt
│   └── venv/                       # 가상환경 (gitignore)
│
├── src/                            # Electron + React 프론트엔드
│   ├── main/                       # Electron 메인 프로세스
│   │   └── index.ts                # Electron 앱 시작점
│   │
│   ├── preload/                    # Electron 프리로드
│   │   └── index.ts                # IPC 브릿지
│   │
│   └── renderer/                   # React 앱 (브라우저 프로세스)
│       ├── App.tsx                  # 루트 컴포넌트 + 라우터
│       ├── main.tsx                 # React 엔트리포인트
│       ├── index.html              # HTML 템플릿
│       │
│       ├── pages/                  # 페이지 컴포넌트
│       │   ├── CalendarPage.tsx        # 페이지1: 통합 캘린더
│       │   └── SchoolSchedulePage.tsx  # 페이지2: 학교별 일정 관리
│       │
│       ├── components/             # 재사용 컴포넌트
│       │   ├── layout/
│       │   │   ├── Header.tsx          # 상단 네비게이션
│       │   │   └── Sidebar.tsx         # 좌측 사이드바 (공통 쉘)
│       │   │
│       │   ├── calendar/
│       │   │   ├── CalendarGrid.tsx     # 월간 캘린더 그리드
│       │   │   ├── CalendarCell.tsx     # 개별 날짜 셀
│       │   │   ├── CalendarHeader.tsx   # 요일 헤더 (일~토)
│       │   │   ├── CalendarNav.tsx      # 이전/오늘/다음 + 뷰 토글
│       │   │   ├── EventBadge.tsx       # 일정 뱃지 (각 이벤트)
│       │   │   └── ExamPeriodBar.tsx    # 시험 기간 상단 바
│       │   │
│       │   ├── school/
│       │   │   ├── SchoolToggleList.tsx # 학교 토글 체크박스 목록
│       │   │   ├── SchoolListSidebar.tsx# 학교 목록 사이드바 (페이지2)
│       │   │   └── SchoolAddModal.tsx   # 학교 추가 모달
│       │   │
│       │   └── schedule/
│       │       ├── ScheduleTable.tsx    # 학사일정 테이블
│       │       ├── ScheduleRow.tsx      # 테이블 행
│       │       ├── CategoryBadge.tsx    # 구분 뱃지 (시험/공휴일 등)
│       │       └── StatsCards.tsx       # 하단 통계 카드 3개
│       │
│       ├── stores/                 # Zustand 상태 관리
│       │   ├── useSchoolStore.ts       # 학교 목록 + 토글 상태
│       │   ├── useCalendarStore.ts     # 캘린더 네비게이션 상태
│       │   └── useScheduleStore.ts     # 학사일정 데이터
│       │
│       ├── services/               # API 호출 레이어
│       │   ├── api.ts                  # axios/fetch 인스턴스
│       │   ├── schoolApi.ts            # 학교 관련 API
│       │   └── scheduleApi.ts          # 일정 관련 API
│       │
│       ├── types/                  # TypeScript 타입 정의
│       │   └── index.ts                # 모든 타입 (School, Event 등)
│       │
│       ├── utils/                  # 유틸리티 함수
│       │   ├── calendar.ts             # 캘린더 날짜 계산
│       │   └── color.ts                # 학교 색상 매핑
│       │
│       └── assets/
│           └── main.css                # Tailwind 진입점 + 커스텀 스타일
│
├── package.json
├── electron.vite.config.ts
├── electron-builder.yml
├── tailwind.config.js
├── tsconfig.json
├── tsconfig.node.json
├── tsconfig.web.json
├── .env.example
├── .gitignore
└── README.md
```

## 파일별 역할 상세

### backend/

| 파일 | 역할 |
|------|------|
| `main.py` | FastAPI 앱 생성, 라우터 등록, CORS 설정, uvicorn 실행 |
| `routers/schools.py` | `GET/POST/DELETE /api/schools` - 학교 CRUD |
| `routers/schedules.py` | `GET /api/schedules`, `POST /api/schedules/sync` - 일정 조회/동기화 |
| `services/neis_client.py` | 나이스 API 호출 래퍼 (학사일정 조회, 학교 검색) |
| `models/schemas.py` | Pydantic 요청/응답 모델 |
| `database/connection.py` | SQLite 연결 관리, 초기화 |
| `database/init.sql` | 테이블 DDL (schools, events) |

### src/renderer/ (React)

| 파일 | 역할 |
|------|------|
| `App.tsx` | react-router 설정, 두 페이지 라우팅 |
| `pages/CalendarPage.tsx` | 학교 토글 사이드바 + 캘린더 그리드 조합 |
| `pages/SchoolSchedulePage.tsx` | 학교 리스트 사이드바 + 일정 테이블 조합 |
| `stores/*.ts` | Zustand 스토어 3개 (학교, 캘린더, 일정) |
| `services/*.ts` | 백엔드 API 호출 함수들 |
| `types/index.ts` | 공유 TypeScript 인터페이스 |

## 데이터 흐름

```
[나이스 API] ──httpx──> [Python 백엔드] ──SQLite──> [로컬 DB]
                              │
                         FastAPI REST
                              │
                              ▼
                    [React 프론트엔드]
                    ├── Zustand Store (상태)
                    ├── Pages (페이지)
                    └── Components (UI)
```
