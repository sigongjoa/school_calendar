# 10. 스타일 가이드

## 디자인 토큰 (Tailwind 설정)

디자인 시안에서 추출한 색상/크기 시스템.

### 색상

```javascript
// tailwind.config.js (또는 CSS 변수)
colors: {
  primary: '#135bec',            // 메인 브랜드 색상
  'background-light': '#f6f6f8', // 라이트모드 배경
  'background-dark': '#101622',  // 다크모드 배경 (선택)
}
```

### 텍스트 색상

| 용도 | 클래스 | Hex |
|------|--------|-----|
| 기본 텍스트 | `text-[#111318]` | #111318 |
| 보조 텍스트 | `text-[#616f89]` | #616f89 |
| 비활성 텍스트 | `text-[#d1d5db]` | #d1d5db |
| 일요일 | `text-red-500` | - |
| 토요일 | `text-blue-500` | - |
| 강조/링크 | `text-primary` | #135bec |

### 보더/배경

| 용도 | 클래스 |
|------|--------|
| 카드/테이블 보더 | `border-[#f0f2f4]` |
| 입력필드/버튼 배경 | `bg-[#f0f2f4]` |
| 카드 배경 | `bg-white` |
| 페이지 배경 | `bg-background-light` |
| 호버 배경 | `hover:bg-gray-50` |

### 학교 색상 (캘린더 표시용)

| 순서 | 색상 | Hex | Tailwind 근사 |
|------|------|-----|---------------|
| 1 | 오렌지 | #f97316 | orange-400 |
| 2 | 블루 | #3b82f6 | blue-500 |
| 3 | 그린 | #22c55e | green-500 |
| 4 | 레드 | #ef4444 | red-500 |
| 5 | 퍼플 | #a855f7 | purple-500 |
| 6 | 핑크 | #ec4899 | pink-500 |
| 7 | 틸 | #14b8a6 | teal-500 |
| 8 | 앰버 | #f59e0b | amber-500 |

### 이벤트 카테고리 색상

| 카테고리 | 배경 | 텍스트 | 보더 |
|----------|------|--------|------|
| 시험 | `bg-red-100` | `text-red-700` | `border-red-400` |
| 공휴일 | `bg-green-100` | `text-green-700` | `border-green-400` |
| 학교휴일 | `bg-blue-100` | `text-blue-700` | `border-blue-400` |
| 방학 | `bg-purple-100` | `text-purple-700` | `border-purple-400` |
| 학교행사 | `bg-orange-100` | `text-orange-700` | `border-orange-400` |
| 기타 | `bg-gray-100` | `text-gray-700` | `border-gray-400` |

---

## 폰트

```css
font-family: 'Lexend', 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, sans-serif;
```

- **Lexend**: Google Fonts (영문+숫자, 가독성 우수)
- **Pretendard**: 한글 폰트 (없으면 시스템 폰트 폴백)

### 폰트 로드

Electron 앱이므로 로컬 폰트 파일 사용 권장. 또는 Google Fonts CDN:

```html
<link href="https://fonts.googleapis.com/css2?family=Lexend:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet" />
```

---

## 공통 컴포넌트 스타일 패턴

### 카드

```html
<div class="bg-white rounded-xl shadow-sm border border-[#f0f2f4] p-6">
  ...
</div>
```

### 버튼 - Primary

```html
<button class="flex items-center justify-center gap-2 rounded-lg h-10 px-4 bg-primary text-white text-sm font-bold">
  텍스트
</button>
```

### 버튼 - Secondary

```html
<button class="flex items-center justify-center rounded-lg h-10 px-4 bg-white border border-[#f0f2f4] text-[#111318] text-sm font-bold hover:bg-gray-50">
  텍스트
</button>
```

### 버튼 - Icon Only

```html
<button class="flex items-center justify-center rounded-lg h-10 w-10 bg-[#f0f2f4] hover:bg-gray-200">
  <span class="material-symbols-outlined text-xl">icon_name</span>
</button>
```

### 입력 필드

```html
<div class="flex w-full items-stretch rounded-lg bg-[#f0f2f4]">
  <div class="text-[#616f89] flex items-center justify-center pl-4">
    <span class="material-symbols-outlined text-lg">search</span>
  </div>
  <input class="form-input flex w-full border-none bg-transparent focus:outline-0 focus:ring-0 text-base placeholder:text-[#616f89]"
         placeholder="검색..." />
</div>
```

### 뱃지 (이벤트)

```html
<!-- 캘린더 셀 내 이벤트 뱃지 -->
<div class="px-2 py-0.5 text-[10px] font-bold rounded bg-orange-50 text-orange-600">
  대치고: 중간고사
</div>

<!-- 테이블 내 카테고리 뱃지 -->
<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-bold bg-red-100 text-red-700">
  시험
</span>
```

### 사이드바 아이템

```html
<!-- 선택됨 -->
<div class="flex items-center gap-3 px-3 py-3 rounded-lg bg-primary/10 border-l-4 border-primary">
  <span class="material-symbols-outlined text-primary">school</span>
  <p class="text-primary text-sm font-bold">학교명</p>
</div>

<!-- 미선택 -->
<div class="flex items-center gap-3 px-3 py-3 rounded-lg hover:bg-gray-100 cursor-pointer">
  <span class="material-symbols-outlined text-gray-400">school</span>
  <p class="text-[#111318] text-sm font-medium">학교명</p>
</div>
```

---

## 아이콘

Google Material Symbols (Outlined):

```html
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet" />
```

**사용할 아이콘 목록**:

| 아이콘 | 용도 |
|--------|------|
| `school` | 학교 아이콘 |
| `search` | 검색 |
| `chevron_left` / `chevron_right` | 캘린더 이전/다음 |
| `add` / `add_circle` | 추가 |
| `edit` | 수정 |
| `delete` | 삭제 |
| `sync` | 동기화 |
| `cloud_download` | 외부 데이터 가져오기 |
| `campaign` | 학교 공지 |
| `celebration` | 기념일 |
| `notifications` | 알림 |
| `settings` | 설정 |
| `history` | 변경 이력 |
| `upload_file` | 내보내기 |
| `print` | 인쇄 |
| `trending_up` | 증가 트렌드 |
| `keyboard_arrow_down` | 더보기 |
| `close` | 모달 닫기 |

---

## 반응형 (불필요)

Electron 데스크톱 앱이므로 모바일 반응형은 불필요.
최소 창 크기: **1200 × 800px** 기준으로 개발.
