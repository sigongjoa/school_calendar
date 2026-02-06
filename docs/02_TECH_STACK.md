# 02. 기술 스택

## 호환성 기준

wawa_smart_erp 모노레포(node14 기준)와 호환되는 스택을 사용한다.

## 프론트엔드

| 기술 | 버전 | 용도 |
|------|------|------|
| React | ^19.2.1 | UI 프레임워크 |
| React DOM | ^19.2.1 | DOM 렌더링 |
| TypeScript | ^5.9.3 | 타입 안전성 |
| Vite | ^7.2.6 | 빌드 도구 |
| electron-vite | ^5.0.0 | Electron + Vite 통합 |
| Electron | ^39.2.6 | 데스크톱 앱 (로컬 실행) |
| Zustand | ^5.0.0 | 상태 관리 |
| react-router-dom | ^7.0.0 | 라우팅 (페이지 전환) |
| Tailwind CSS | ^4.0.0 | 스타일링 |
| date-fns | ^4.1.0 | 날짜 유틸리티 |

## 백엔드

| 기술 | 버전 | 용도 |
|------|------|------|
| Python | ^3.11 | 백엔드 런타임 |
| FastAPI | ^0.115.0 | REST API 서버 |
| uvicorn | ^0.34.0 | ASGI 서버 |
| httpx | ^0.28.0 | 나이스 API HTTP 클라이언트 |
| sqlite3 | 내장 | 로컬 데이터 저장 |

## 개발 도구

| 기술 | 용도 |
|------|------|
| pnpm | 패키지 매니저 (모노레포 호환) |
| ESLint | 코드 린팅 |
| Prettier | 코드 포매팅 |
| electron-builder | 데스크톱 앱 빌드 |

## 설치 명령어

### 프론트엔드 초기 세팅

```bash
cd node15_school_calendar

# pnpm 초기화 (electron-vite 템플릿 기반)
pnpm create @quick-start/electron . --template react-ts

# 추가 의존성
pnpm add zustand react-router-dom date-fns
pnpm add -D tailwindcss @tailwindcss/vite
```

### 백엔드 초기 세팅

```bash
cd backend

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install fastapi uvicorn httpx
pip freeze > requirements.txt
```

## Tailwind CSS 설정

`src/renderer/assets/main.css` 최상단:
```css
@import "tailwindcss";
```

`electron.vite.config.ts`에 Tailwind 플러그인 추가:
```typescript
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  renderer: {
    plugins: [react(), tailwindcss()],
  }
})
```

## 환경 변수

`.env` 파일 (루트):
```env
# 나이스 API
NEIS_API_KEY=your_api_key_here

# 백엔드
BACKEND_PORT=8015
BACKEND_HOST=127.0.0.1

# 프론트엔드
VITE_BACKEND_URL=http://127.0.0.1:8015
```

## 포트 규칙

모노레포 내 다른 모듈과 충돌 방지:
- 프론트엔드 dev 서버: `5173` (Vite 기본)
- 백엔드 API 서버: `8015` (node15이므로 8015)
