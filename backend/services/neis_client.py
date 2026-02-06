import httpx
import os
import re
import datetime
from typing import List, Dict, Optional

NEIS_BASE_URL = "https://open.neis.go.kr/hub"

class NeisApiError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message

class NeisClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("NEIS_API_KEY")
        self.client = httpx.AsyncClient(timeout=30.0)

    async def search_school(self, keyword: str) -> List[Dict]:
        """학교명으로 검색"""
        if not self.api_key:
             # For development without key, we might want to return mock or error, 
             # but for now let's try assuming the user put it in .env
             pass

        params = {
            "KEY": self.api_key,
            "Type": "json",
            "SCHUL_NM": keyword,
            "pSize": 20,
        }
        
        try:
            resp = await self.client.get(f"{NEIS_BASE_URL}/schoolInfo", params=params)
            resp.raise_for_status()
            data = resp.json()
        except httpx.HTTPError as e:
            print(f"NEIS API Error: {e}")
            return []
        except Exception as e:
            print(f"Error parsing NEIS response: {e}")
            return []

        # 결과 파싱
        try:
            if "schoolInfo" not in data:
                return []
            
            head = data["schoolInfo"][0]["head"]
            # Check for INFO-200 (No data) which is structured differently sometimes or just check row
            # Actually standard NEIS response has head in list[0] and row in list[1] usually
            
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
        from_date: datetime.date,
        to_date: datetime.date,
    ) -> List[Dict]:
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
        
        try:
            resp = await self.client.get(
                f"{NEIS_BASE_URL}/SchoolSchedule", params=params
            )
            data = resp.json()
        except Exception:
            return []

        try:
            # Check for error or empty
            if "SchoolSchedule" not in data:
                 return []
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
        # Substring matching might be safer if kind has extra spaces or chars
        for k, v in mapping.items():
            if k in kind:
                return v
        return "special"

    def _classify(self, event_name: str, sbtr: str) -> str:
        """이벤트명 → 카테고리 자동 분류"""
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
