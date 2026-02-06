# 05. 나이스(NEIS) API 연동 가이드

## 개요

교육부 나이스 교육정보 개방 포털에서 제공하는 공공 API를 사용하여 학사일정 데이터를 자동 수집한다.

## 1단계: API 키 발급

### 발급 절차

1. **나이스 교육정보 개방 포털** 접속: `https://open.neis.go.kr`
2. 회원가입 (간편인증 또는 이메일)
3. 로그인 → "인증키 신청" 메뉴
4. 인증키 신청:
   - 활용 용도: "기타" 또는 "교육/학습"
   - 서비스 URL: `http://localhost` (로컬 전용이므로)
5. 즉시 발급됨 → `.env` 파일에 저장

### API 키 관리

```env
# .env
NEIS_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

- 일 호출 제한: **1,000건/일** (무료 기준, 충분함)
- 키 노출 주의: `.gitignore`에 `.env` 반드시 포함

---

## 2단계: 사용할 API 엔드포인트

### 2-1. 학교 검색 API

학교를 추가할 때 학교명으로 검색하여 학교코드를 찾는다.

**엔드포인트**: `GET /hub/schoolInfo`

```
https://open.neis.go.kr/hub/schoolInfo?KEY={API_KEY}&Type=json&SCHUL_NM={학교명}
```

**요청 파라미터**:
| 파라미터 | 필수 | 설명 | 예시 |
|----------|------|------|------|
| KEY | O | 인증키 | |
| Type | O | 응답 형식 | `json` |
| SCHUL_NM | O | 학교명 (부분 검색 가능) | `대치고` |
| pIndex | X | 페이지 번호 | `1` |
| pSize | X | 페이지 크기 | `10` |

**응답 예시**:
```json
{
  "schoolInfo": [
    {
      "head": [{"list_total_count": 1}, {"RESULT": {"CODE": "INFO-000", "MESSAGE": "정상 처리"}}]
    },
    {
      "row": [
        {
          "ATPT_OFCDC_SC_CODE": "B10",
          "ATPT_OFCDC_SC_NM": "서울특별시교육청",
          "SD_SCHUL_CODE": "7010057",
          "SCHUL_NM": "대치고등학교",
          "ENG_SCHUL_NM": "Daechi High School",
          "SCHUL_KND_SC_NM": "고등학교",
          "LCTN_SC_NM": "서울특별시",
          "JU_ORG_NM": "서울특별시강남서초교육지원청",
          "FOND_SC_NM": "사립",
          "ORG_RDNMA": "서울특별시 강남구 역삼로 ...",
          "ORG_TELNO": "02-XXX-XXXX",
          "HMPG_ADRES": "http://daechi.sen.hs.kr",
          "COEDU_SC_NM": "남여공학",
          "ORG_FAXNO": "02-XXX-XXXX",
          "FOND_YMD": "19840301"
        }
      ]
    }
  ]
}
```

**추출할 필드**:
- `ATPT_OFCDC_SC_CODE` → `atptCode` (교육청 코드)
- `SD_SCHUL_CODE` → `sdCode` (학교 코드)
- `SCHUL_NM` → `name`
- `SCHUL_KND_SC_NM` → `schoolType` 매핑 ("고등학교" → "high")

### 2-2. 학사일정 API (핵심)

**엔드포인트**: `GET /hub/SchoolSchedule`

```
https://open.neis.go.kr/hub/SchoolSchedule?KEY={API_KEY}&Type=json&ATPT_OFCDC_SC_CODE={교육청코드}&SD_SCHUL_CODE={학교코드}&AA_YMD={날짜}
```

**요청 파라미터**:
| 파라미터 | 필수 | 설명 | 예시 |
|----------|------|------|------|
| KEY | O | 인증키 | |
| Type | O | 응답 형식 | `json` |
| ATPT_OFCDC_SC_CODE | O | 교육청 코드 | `B10` |
| SD_SCHUL_CODE | O | 학교 코드 | `7010057` |
| AA_FROM_YMD | X | 기간 시작일 | `20260301` |
| AA_TO_YMD | X | 기간 종료일 | `20260331` |
| AA_YMD | X | 특정 날짜 | `20260315` |
| pIndex | X | 페이지 번호 | `1` |
| pSize | X | 페이지 크기 | `100` |

> `AA_FROM_YMD` + `AA_TO_YMD`로 기간 조회하는 것이 효율적.
> 한 달 단위 (월초~월말) 또는 학기 단위로 조회 권장.

**응답 예시**:
```json
{
  "SchoolSchedule": [
    {
      "head": [{"list_total_count": 5}, {"RESULT": {"CODE": "INFO-000", "MESSAGE": "정상"}}]
    },
    {
      "row": [
        {
          "ATPT_OFCDC_SC_CODE": "B10",
          "SD_SCHUL_CODE": "7010057",
          "AA_YMD": "20260302",
          "AA_NM": "삼일절",
          "EVENT_NM": "삼일절",
          "EVENT_CNTNT": "공휴일",
          "ONE_GRADE_EVENT_YN": "Y",
          "TW_GRADE_EVENT_YN": "Y",
          "THREE_GRADE_EVENT_YN": "Y",
          "FR_GRADE_EVENT_YN": "*",
          "FIV_GRADE_EVENT_YN": "*",
          "SIX_GRADE_EVENT_YN": "*",
          "SBTR_DD_SC_NM": "공휴일",
          "LOAD_DTM": "20260115"
        },
        {
          "AA_YMD": "20260420",
          "EVENT_NM": "1학기 중간고사",
          "EVENT_CNTNT": "1학기 중간고사(1,2학년)",
          "SBTR_DD_SC_NM": ""
        }
      ]
    }
  ]
}
```

**추출할 필드**:
- `AA_YMD` → `date` (형식 변환: "20260302" → "2026-03-02")
- `EVENT_NM` → `title`
- `EVENT_CNTNT` → 상세 내용 (raw에 저장)
- `SBTR_DD_SC_NM` → 수업일수 구분 ("공휴일", "휴업일" 등)

---

## 3단계: Python 백엔드 구현

### neis_client.py 핵심 로직

```python
import httpx
from datetime import datetime, date

NEIS_BASE_URL = "https://open.neis.go.kr/hub"

class NeisClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = httpx.AsyncClient(timeout=30.0)

    async def search_school(self, keyword: str) -> list[dict]:
        """학교명으로 검색"""
        params = {
            "KEY": self.api_key,
            "Type": "json",
            "SCHUL_NM": keyword,
            "pSize": 20,
        }
        resp = await self.client.get(f"{NEIS_BASE_URL}/schoolInfo", params=params)
        data = resp.json()

        # 결과 파싱
        try:
            rows = data["schoolInfo"][1]["row"]
        except (KeyError, IndexError):
            return []

        return [
            {
                "atpt_code": r["ATPT_OFCDC_SC_CODE"],
                "sd_code": r["SD_SCHUL_CODE"],
                "name": r["SCHUL_NM"],
                "school_type": self._map_school_type(r["SCHUL_KND_SC_NM"]),
                "address": r.get("ORG_RDNMA", ""),
            }
            for r in rows
        ]

    async def fetch_schedule(
        self,
        atpt_code: str,
        sd_code: str,
        from_date: date,
        to_date: date,
    ) -> list[dict]:
        """기간별 학사일정 조회"""
        params = {
            "KEY": self.api_key,
            "Type": "json",
            "ATPT_OFCDC_SC_CODE": atpt_code,
            "SD_SCHUL_CODE": sd_code,
            "AA_FROM_YMD": from_date.strftime("%Y%m%d"),
            "AA_TO_YMD": to_date.strftime("%Y%m%d"),
            "pSize": 500,
        }
        resp = await self.client.get(
            f"{NEIS_BASE_URL}/SchoolSchedule", params=params
        )
        data = resp.json()

        try:
            rows = data["SchoolSchedule"][1]["row"]
        except (KeyError, IndexError):
            return []

        return [
            {
                "date": self._parse_date(r["AA_YMD"]),
                "title": r["EVENT_NM"],
                "content": r.get("EVENT_CNTNT", ""),
                "category": self._classify(r["EVENT_NM"], r.get("SBTR_DD_SC_NM", "")),
                "raw": r,
            }
            for r in rows
        ]

    def _parse_date(self, ymd: str) -> str:
        """'20260302' → '2026-03-02'"""
        return f"{ymd[:4]}-{ymd[4:6]}-{ymd[6:8]}"

    def _map_school_type(self, kind: str) -> str:
        mapping = {"초등학교": "elementary", "중학교": "middle", "고등학교": "high"}
        return mapping.get(kind, "special")

    def _classify(self, event_name: str, sbtr: str) -> str:
        """이벤트명 → 카테고리 자동 분류"""
        import re
        if re.search(r"중간고사|기말고사|모의고사|학력평가|시험", event_name):
            return "exam"
        if re.search(r"방학|개학", event_name):
            return "vacation"
        if sbtr == "공휴일" or re.search(r"설날|추석|어린이날|광복절|한글날|개천절|삼일절|현충일|성탄", event_name):
            return "holiday"
        if re.search(r"개교기념|재량휴업|대체휴", event_name):
            return "school_holiday"
        if re.search(r"입학|졸업|체육|수학여행|현장학습|학예|수련", event_name):
            return "event"
        return "other"
```

---

## 4단계: 동기화 전략

### 초기 동기화

학교 추가 시 **해당 학년도 전체** (3월~다음해 2월) 일정을 한번에 가져옴:

```python
# 학년도 기준: 3월 시작
async def initial_sync(school_id: int, atpt_code: str, sd_code: str):
    today = date.today()
    # 현재 학년도 계산
    year = today.year if today.month >= 3 else today.year - 1
    from_date = date(year, 3, 1)
    to_date = date(year + 1, 2, 28)

    events = await neis.fetch_schedule(atpt_code, sd_code, from_date, to_date)
    # DB에 upsert
    ...
```

### 정기 동기화

- 앱 실행 시 마지막 동기화가 24시간 이상 지난 학교들 자동 동기화
- 수동 "동기화" 버튼으로 즉시 동기화 가능
- 동기화 시 기존 neis 소스 이벤트를 삭제 후 재삽입 (upsert)

### 시험 기간 자동 감지

시험 이벤트가 연속 날짜에 있으면 기간으로 묶음:

```python
def merge_exam_periods(events: list[dict]) -> list[dict]:
    """연속된 시험 이벤트를 기간형으로 병합"""
    exam_events = [e for e in events if e["category"] == "exam"]
    # 날짜순 정렬 후 연속 날짜 병합
    # start_date, end_date 설정
    ...
```

---

## 5단계: 에러 처리

### 나이스 API 에러 코드

| 코드 | 의미 | 대응 |
|------|------|------|
| `INFO-000` | 정상 | - |
| `INFO-200` | 해당하는 데이터가 없습니다 | 빈 배열 반환 (에러 아님) |
| `ERROR-300` | 필수 값이 누락 | 파라미터 검증 |
| `ERROR-290` | 인증키가 유효하지 않습니다 | API 키 확인 안내 |
| `ERROR-337` | 일일 트래픽 제한 초과 | 캐시 활용, 내일 재시도 |

### 구현

```python
class NeisApiError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message

def parse_response(data: dict, endpoint_key: str) -> list[dict]:
    """나이스 API 응답 공통 파서"""
    if endpoint_key not in data:
        # 에러 응답 확인
        result = data.get("RESULT", {})
        code = result.get("CODE", "UNKNOWN")
        if code == "INFO-200":
            return []  # 데이터 없음은 정상
        raise NeisApiError(code, result.get("MESSAGE", "알 수 없는 에러"))

    return data[endpoint_key][1]["row"]
```

---

## 교육청 코드 참조표

| 코드 | 교육청 |
|------|--------|
| B10 | 서울특별시교육청 |
| C10 | 부산광역시교육청 |
| D10 | 대구광역시교육청 |
| E10 | 인천광역시교육청 |
| F10 | 광주광역시교육청 |
| G10 | 대전광역시교육청 |
| H10 | 울산광역시교육청 |
| I10 | 세종특별자치시교육청 |
| J10 | 경기도교육청 |
| K10 | 강원특별자치도교육청 |
| M10 | 충청북도교육청 |
| N10 | 충청남도교육청 |
| P10 | 전북특별자치도교육청 |
| Q10 | 전라남도교육청 |
| R10 | 경상북도교육청 |
| S10 | 경상남도교육청 |
| T10 | 제주특별자치도교육청 |
