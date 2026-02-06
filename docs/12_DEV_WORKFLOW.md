# 12. 개발 워크플로우

## 마일스톤

### M1: 프로젝트 세팅 + 백엔드 기반 (1일)

- [ ] electron-vite + React + TypeScript 프로젝트 초기화
- [ ] Tailwind CSS 설정
- [ ] 라우터 설정 (2페이지)
- [ ] Python 백엔드 초기화 (FastAPI + SQLite)
- [ ] DB 테이블 생성
- [ ] 나이스 API 키 발급 및 테스트

**완료 기준**: `pnpm dev`로 빈 Electron 앱 실행, `python main.py`로 백엔드 실행, `/docs` 자동 생성 확인

### M2: 나이스 API 연동 (1일)

- [ ] `neis_client.py` 구현 (학교 검색 + 학사일정 조회)
- [ ] `routers/schools.py` 구현 (학교 CRUD + 나이스 검색 프록시)
- [ ] `routers/schedules.py` 구현 (일정 조회 + 동기화)
- [ ] API 테스트 (curl 또는 FastAPI /docs)

**완료 기준**: `curl localhost:8015/api/schools/search?keyword=대치고` 로 검색 결과 반환, 학교 등록 후 동기화하면 학사일정 DB 저장

### M3: 프론트엔드 기본 구조 (1일)

- [ ] Zustand 스토어 3개 구현
- [ ] API 서비스 레이어 구현
- [ ] Header 컴포넌트
- [ ] 타입 정의

**완료 기준**: 앱 실행 시 학교 목록 API 호출 성공, 콘솔에서 데이터 확인

### M4: 캘린더 페이지 (2-3일)

- [ ] CalendarNav 구현 (뷰 토글 + 네비게이션)
- [ ] CalendarGrid 구현 (7×6 그리드)
- [ ] CalendarCell 구현 (날짜 + 스타일)
- [ ] CalendarHeader 구현 (요일 헤더)
- [ ] EventBadge 구현 (카테고리별 색상)
- [ ] ExamPeriodBar 구현 (시험 기간 바)
- [ ] SchoolToggleList 사이드바 구현
- [ ] 학교 토글 → 이벤트 필터링 연동
- [ ] 이전달/다음달 네비게이션 동작

**완료 기준**: 학교 2-3개 등록, 토글로 켜고 끌 때 캘린더에 이벤트 표시/숨김 동작

### M5: 학교 관리 페이지 (1-2일)

- [ ] SchoolListSidebar 구현
- [ ] ScheduleTable 구현
- [ ] CategoryBadge 구현
- [ ] StatsCards 구현
- [ ] 학교 선택 → 테이블 데이터 전환
- [ ] 동기화 버튼 동작

**완료 기준**: 학교 선택 시 해당 학교 학사일정 테이블 표시, 동기화 버튼으로 최신 데이터 갱신

### M6: 학교 추가 모달 + 마무리 (1일)

- [ ] SchoolAddModal 구현 (검색 → 선택 → 색상 → 추가)
- [ ] 학교 추가 후 자동 초기 동기화
- [ ] 에러 처리 / 로딩 상태
- [ ] 범례 (Legend) 추가
- [ ] 전체 플로우 테스트

**완료 기준**: 학교 검색 → 추가 → 동기화 → 캘린더 표시 → 토글 → 학교관리 페이지 조회 전체 플로우 동작

---

## 개발 순서 (파일 생성 순서)

### Step 1: 프로젝트 초기화

```bash
# 1-1. electron-vite 프로젝트 생성
cd /mnt/d/progress/mathesis/node15_school_calendar
pnpm create @quick-start/electron . --template react-ts

# 1-2. 추가 패키지 설치
pnpm add zustand react-router-dom date-fns
pnpm add -D tailwindcss @tailwindcss/vite

# 1-3. Tailwind 설정
# electron.vite.config.ts에 tailwindcss 플러그인 추가
# src/renderer/assets/main.css에 @import "tailwindcss" 추가
```

### Step 2: 백엔드 구축

```bash
# 2-1. Python 환경
cd backend
python -m venv venv
source venv/bin/activate
pip install fastapi uvicorn httpx
pip freeze > requirements.txt
```

파일 생성 순서:
1. `backend/database/init.sql` - DDL
2. `backend/database/connection.py` - DB 연결
3. `backend/models/schemas.py` - Pydantic 모델
4. `backend/services/neis_client.py` - 나이스 API 클라이언트
5. `backend/routers/schools.py` - 학교 API
6. `backend/routers/schedules.py` - 일정 API
7. `backend/main.py` - 엔트리포인트

### Step 3: 프론트엔드 타입 + 서비스

1. `src/renderer/types/index.ts`
2. `src/renderer/services/api.ts`
3. `src/renderer/services/schoolApi.ts`
4. `src/renderer/services/scheduleApi.ts`

### Step 4: Zustand 스토어

1. `src/renderer/stores/useSchoolStore.ts`
2. `src/renderer/stores/useCalendarStore.ts`
3. `src/renderer/stores/useScheduleStore.ts`

### Step 5: 레이아웃 컴포넌트

1. `src/renderer/components/layout/Header.tsx`
2. `src/renderer/App.tsx` (라우터 + 레이아웃)

### Step 6: 캘린더 페이지

1. `src/renderer/utils/calendar.ts` (날짜 계산)
2. `src/renderer/components/calendar/CalendarHeader.tsx`
3. `src/renderer/components/calendar/CalendarNav.tsx`
4. `src/renderer/components/calendar/EventBadge.tsx`
5. `src/renderer/components/calendar/ExamPeriodBar.tsx`
6. `src/renderer/components/calendar/CalendarCell.tsx`
7. `src/renderer/components/calendar/CalendarGrid.tsx`
8. `src/renderer/components/school/SchoolToggleList.tsx`
9. `src/renderer/pages/CalendarPage.tsx`

### Step 7: 학교 관리 페이지

1. `src/renderer/components/schedule/CategoryBadge.tsx`
2. `src/renderer/components/schedule/ScheduleRow.tsx`
3. `src/renderer/components/schedule/ScheduleTable.tsx`
4. `src/renderer/components/schedule/StatsCards.tsx`
5. `src/renderer/components/school/SchoolListSidebar.tsx`
6. `src/renderer/pages/SchoolSchedulePage.tsx`

### Step 8: 학교 추가 모달

1. `src/renderer/utils/color.ts`
2. `src/renderer/components/school/SchoolAddModal.tsx`

---

## 개발 실행 방법

### 터미널 1: 백엔드

```bash
cd /mnt/d/progress/mathesis/node15_school_calendar/backend
source venv/bin/activate   # Windows: venv\Scripts\activate
python main.py
# → http://127.0.0.1:8015
# → Swagger: http://127.0.0.1:8015/docs
```

### 터미널 2: 프론트엔드 (Electron)

```bash
cd /mnt/d/progress/mathesis/node15_school_calendar
pnpm dev
# → Electron 앱 실행 (내부적으로 Vite dev server + Electron)
```

### 브라우저 개발 (Electron 없이)

Electron 없이 브라우저에서 먼저 개발하고 싶다면:

```bash
# electron.vite.config.ts의 renderer 설정만 별도 Vite로 실행
pnpm vite src/renderer
# → http://localhost:5173
```

---

## 테스트 시나리오

### 1. 학교 추가 플로우

1. "학교 추가" 버튼 클릭
2. "대치" 검색 → 대치고등학교 표시
3. 대치고등학교 선택 → 오렌지 색상 선택
4. "추가" → 학교 목록에 표시
5. 자동 동기화 → 학사일정 로드

### 2. 캘린더 조회 플로우

1. 학교 3개 등록 + 동기화 완료
2. 캘린더 페이지 → 3개 학교 일정 모두 표시
3. 학교 1개 토글 off → 해당 학교 일정 사라짐
4. 다음달 이동 → 해당 월 일정 표시
5. 시험 기간이 있는 달 → 상단 바 표시

### 3. 학교 관리 플로우

1. "학교 관리" 페이지 이동
2. 사이드바에서 학교 선택 → 해당 학교 일정 테이블
3. "외부 일정 가져오기" → 동기화 실행 → 테이블 갱신
4. 다른 학교 선택 → 테이블 전환

---

## 트러블슈팅 가이드

### 나이스 API 관련

| 문제 | 원인 | 해결 |
|------|------|------|
| 검색 결과 없음 | 학교명 불일치 | 정확한 학교명 또는 짧은 키워드 사용 |
| INFO-200 응답 | 해당 기간 데이터 없음 | 학년도 범위 확인 (3월~2월) |
| ERROR-290 | API 키 만료/오류 | 키 재발급 |
| ERROR-337 | 일 호출 제한 초과 | 캐시 활용, 불필요한 호출 줄이기 |
| 타임아웃 | 네트워크 문제 | 재시도, timeout 늘리기 |

### 프론트엔드 관련

| 문제 | 원인 | 해결 |
|------|------|------|
| CORS 에러 | 백엔드 CORS 미설정 | main.py CORS 미들웨어 확인 |
| 캘린더 날짜 오류 | month가 0-indexed | date-fns는 0-indexed, 주의 |
| Tailwind 미적용 | 설정 누락 | @tailwindcss/vite 플러그인 + CSS import 확인 |
| 이벤트 안 보임 | enabled 필터 | 학교 토글 상태 확인 |
