# node15_school_calendar - 개발 문서 인덱스

> 학원용 학사일정 통합 캘린더 모듈

이 `docs/` 폴더만으로 전체 개발이 가능합니다.

## 문서 목록

| # | 파일 | 내용 | 읽는 순서 |
|---|------|------|-----------|
| 01 | [PROJECT_OVERVIEW.md](./01_PROJECT_OVERVIEW.md) | 프로젝트 개요, 목표, 범위 | 필수 (처음) |
| 02 | [TECH_STACK.md](./02_TECH_STACK.md) | 기술 스택, 버전, 설치 방법 | 필수 |
| 03 | [PROJECT_STRUCTURE.md](./03_PROJECT_STRUCTURE.md) | 디렉토리 구조, 파일별 역할 | 필수 |
| 04 | [DATA_MODEL.md](./04_DATA_MODEL.md) | 데이터 모델, TypeScript 타입, DB 스키마 | 필수 |
| 05 | [NEIS_API.md](./05_NEIS_API.md) | 나이스 API 연동 가이드 (키 발급~호출) | 필수 |
| 06 | [BACKEND_SPEC.md](./06_BACKEND_SPEC.md) | Python 백엔드 API 명세 | 필수 |
| 07 | [FRONTEND_PAGES.md](./07_FRONTEND_PAGES.md) | 페이지별 상세 구현 명세 | 필수 |
| 08 | [COMPONENTS.md](./08_COMPONENTS.md) | 컴포넌트 설계 (props, 상태, 이벤트) | 필수 |
| 09 | [STATE_MANAGEMENT.md](./09_STATE_MANAGEMENT.md) | Zustand 스토어 설계 | 필수 |
| 10 | [STYLE_GUIDE.md](./10_STYLE_GUIDE.md) | Tailwind 디자인 토큰, 컬러 시스템 | 참고 |
| 11 | [INTEGRATION_GUIDE.md](./11_INTEGRATION_GUIDE.md) | wawa_smart_erp 모노레포 통합 가이드 | 나중에 |
| 12 | [DEV_WORKFLOW.md](./12_DEV_WORKFLOW.md) | 개발 순서, 마일스톤, 체크리스트 | 필수 |

## 빠른 시작

```bash
# 1. 프로젝트 세팅
cd node15_school_calendar
pnpm install

# 2. 나이스 API 키 설정
cp .env.example .env
# .env에 NEIS_API_KEY 입력

# 3. 백엔드 실행
cd backend && pip install -r requirements.txt && python main.py

# 4. 프론트엔드 실행
pnpm dev
```
