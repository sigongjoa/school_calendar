# node15_school_calendar

학원용 학사일정 통합 캘린더 모듈

나이스(NEIS) API를 통해 여러 학교의 학사일정을 자동 수집하고, 하나의 캘린더에서 통합 조회할 수 있는 Electron 데스크톱 앱.

## 기능

- 나이스 API 연동으로 학교별 학사일정 자동 수집
- 통합 캘린더: 여러 학교 일정을 토글로 켜고/끄며 한눈에 확인
- 학교별 일정 관리: 테이블 형태로 상세 조회
- 시험 기간, 공휴일, 방학 등 카테고리별 시각화

## 기술 스택

- **프론트**: React 19 + TypeScript + Vite + Electron + Zustand + Tailwind CSS
- **백엔드**: Python (FastAPI) + SQLite
- **API**: 나이스 교육정보 개방 포털 (open.neis.go.kr)

## 개발 문서

`docs/` 폴더에 전체 개발 가이드가 있습니다. [문서 인덱스](./docs/00_INDEX.md) 참조.

## 빠른 시작

```bash
# 1. 나이스 API 키 설정
cp .env.example .env
# .env 파일에 NEIS_API_KEY 입력

# 2. 백엔드
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python main.py

# 3. 프론트엔드
pnpm install
pnpm dev
```

## 통합 대상

wawa_smart_erp 모노레포 (`apps/desktop/src/modules/school-calendar/`)
