"""BDD tests for NEIS API Client - 나이스 교육정보 개방포털 클라이언트 검증"""
import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from services.neis_client import NeisClient
from datetime import date

scenarios("features/neis_client.feature")

# -- Fixtures --

@pytest.fixture
def neis_client():
    return NeisClient()


@pytest.fixture
def search_results():
    return {}


@pytest.fixture
def schedule_results():
    return {}


@pytest.fixture
def classify_result():
    return {}


@pytest.fixture
def date_result():
    return {}


# -- Given Steps --

@given("NEIS API 클라이언트가 생성되어 있다")
def neis_client_created(neis_client):
    assert neis_client is not None
    assert neis_client.api_key is not None


# -- When Steps --

@when(parsers.parse('"{keyword}"로 학교를 검색한다'), target_fixture="search_results")
def search_school(neis_client, keyword):
    import asyncio
    results = asyncio.get_event_loop().run_until_complete(
        neis_client.search_school(keyword)
    )
    return results


@when("대치중학교의 2025년 3월 일정을 조회한다", target_fixture="schedule_results")
def fetch_schedule_march(neis_client):
    import asyncio
    results = asyncio.get_event_loop().run_until_complete(
        neis_client.fetch_schedule("B10", "7091427", date(2025, 3, 1), date(2025, 3, 31))
    )
    return results


@when(parsers.parse('이벤트명 "{event_name}"를 분류한다'), target_fixture="classify_result")
def classify_event(neis_client, event_name):
    category = neis_client._classify(event_name, "")
    return {"category": category}


@when(parsers.parse('NEIS 날짜 "{ymd}"를 변환한다'), target_fixture="date_result")
def parse_date(neis_client, ymd):
    result = neis_client._parse_date(ymd)
    return {"date": result}


# -- Then Steps --

@then("검색 결과가 1개 이상 반환된다")
def check_results_not_empty(search_results):
    assert len(search_results) >= 1


@then("각 결과에 atpt_code, sd_code, name 필드가 있다")
def check_result_fields(search_results):
    for r in search_results:
        assert "atpt_code" in r
        assert "sd_code" in r
        assert "name" in r


@then("검색 결과가 반환된다")
def check_results_returned(search_results):
    assert isinstance(search_results, list)


@then("빈 검색 결과가 반환된다")
def check_empty_results(search_results):
    assert len(search_results) == 0


@then("일정 데이터가 1개 이상 반환된다")
def check_schedule_not_empty(schedule_results):
    assert len(schedule_results) >= 1


@then("각 일정에 date, title, category 필드가 있다")
def check_schedule_fields(schedule_results):
    for ev in schedule_results:
        assert "date" in ev
        assert "title" in ev
        assert "category" in ev


@then(parsers.parse('카테고리가 "{expected}"으로 분류된다'))
def check_category(classify_result, expected):
    assert classify_result["category"] == expected


@then(parsers.parse('"{expected}" 형식으로 변환된다'))
def check_date_format(date_result, expected):
    assert date_result["date"] == expected
