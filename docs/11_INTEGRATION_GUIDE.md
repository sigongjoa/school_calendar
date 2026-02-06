# 11. 모노레포 통합 가이드

> 이 문서는 독립 모듈 개발 완료 후, wawa_smart_erp 모노레포에 통합할 때 참고.

## 통합 대상 구조

```
wawa_smart_erp/
├── apps/desktop/
│   ├── src/
│   │   ├── modules/
│   │   │   └── school-calendar/     ← 여기에 통합
│   │   │       ├── pages/
│   │   │       ├── components/
│   │   │       ├── stores/
│   │   │       ├── services/
│   │   │       ├── types/
│   │   │       └── utils/
│   │   ├── App.tsx                  ← 라우트 추가
│   │   └── ...
│   ├── backend/
│   │   ├── routers/
│   │   │   └── neis_schedules.py    ← 백엔드 라우터 추가
│   │   └── ...
```

## 통합 체크리스트

### 1. 프론트엔드 이관

- [ ] `src/renderer/` 하위 파일들을 `apps/desktop/src/modules/school-calendar/`로 복사
- [ ] import 경로 조정 (상대경로 → 모듈 기준)
- [ ] `App.tsx` 라우터에 `/calendar`, `/schools` 경로 추가
- [ ] 사이드바 네비게이션에 "학사일정" 메뉴 추가

### 2. 공유 타입 이관

- [ ] `types/index.ts`의 타입을 `packages/shared-types/`로 이동 (필요 시)
- [ ] 또는 모듈 내부에 유지 (독립성 선호 시)

### 3. 백엔드 이관

- [ ] `backend/routers/schedules.py` → `apps/desktop/backend/routers/neis_schedules.py`
- [ ] `backend/services/neis_client.py` → `apps/desktop/backend/engine/neis_client.py`
- [ ] `main.py`에 라우터 등록: `app.include_router(neis_schedules.router)`

### 4. DB 통합

- [ ] 별도 SQLite 파일 유지 (school_calendar.db) 또는
- [ ] 기존 DB에 테이블 추가

### 5. 의존성

- [ ] `zustand`, `date-fns`가 이미 wawa에 있는지 확인
- [ ] 없으면 `pnpm add zustand date-fns --filter @wawa/desktop`
- [ ] Python: `httpx`가 requirements.txt에 있는지 확인

### 6. UI 컴포넌트

- [ ] `packages/ui-components/`에 공통 컴포넌트 있으면 재활용
- [ ] Header, Sidebar 등은 기존 wawa 레이아웃에 맞게 조정

## 네비게이션 통합

wawa_smart_erp의 기존 메뉴 구조에 "학사일정" 추가:

```
대시보드 | 시간표 | 채점 | 보고서 | 학사일정(NEW)
                                    ├── 통합 캘린더
                                    └── 학교 관리
```

## 주의사항

- wawa_smart_erp는 Electron 기반이므로, 백엔드는 Electron의 child_process로 Python 서버를 자동 시작하는 방식
- 기존 `backend/main.py`에 라우터만 추가하면 됨
- CORS는 Electron에서는 불필요 (같은 origin)
- 포트는 기존 백엔드와 동일 포트 사용
