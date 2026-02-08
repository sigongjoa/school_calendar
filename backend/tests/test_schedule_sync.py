"""BDD tests for Schedule Sync - 학사일정 동기화"""
import asyncio
import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from httpx import AsyncClient, ASGITransport
from main import app

scenarios("features/schedule_sync.feature")


def run_async(coro):
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


async def _request(method, url, **kwargs):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        return await getattr(ac, method)(url, **kwargs)


@pytest.fixture
def context():
    return {}


# -- Given Steps --

@given("등록된 학교가 있다", target_fixture="context")
def registered_school(clean_db):
    clean_db.execute(
        "INSERT INTO schools (name, atpt_code, sd_code, school_type, color) VALUES (?, ?, ?, ?, ?)",
        ("대치중학교", "B10", "7091427", "middle", "#3b82f6")
    )
    clean_db.commit()
    row = clean_db.execute("SELECT id FROM schools WHERE sd_code = '7091427'").fetchone()
    return {"school_id": row["id"]}


@given("일정이 동기화된 학교가 있다", target_fixture="context")
def synced_school(clean_db):
    clean_db.execute(
        "INSERT INTO schools (name, atpt_code, sd_code, school_type, color) VALUES (?, ?, ?, ?, ?)",
        ("대치중학교", "B10", "7091427", "middle", "#3b82f6")
    )
    clean_db.commit()
    row = clean_db.execute("SELECT id FROM schools WHERE sd_code = '7091427'").fetchone()
    school_id = row["id"]

    resp = run_async(_request("post", f"/api/schedules/sync/{school_id}"))
    assert resp.status_code == 200

    return {"school_id": school_id}


# -- When Steps --

@when("해당 학교의 일정을 동기화한다", target_fixture="response")
def sync_school(context):
    return run_async(_request("post", f"/api/schedules/sync/{context['school_id']}"))


@when("해당 학교의 일정 목록을 조회한다", target_fixture="response")
def get_school_schedules(context):
    return run_async(_request("get", f"/api/schedules?school_id={context['school_id']}"))


@when("특정 년월의 캘린더 데이터를 조회한다", target_fixture="response")
def get_calendar_data(context):
    return run_async(_request("get", "/api/schedules/calendar?year=2025&month=3"))


@when(parsers.parse('"{category}" 카테고리로 일정을 필터링한다'), target_fixture="response")
def filter_by_category(context, category):
    return run_async(_request("get", f"/api/schedules?school_id={context['school_id']}&category={category}"))


@when("존재하지 않는 학교 ID로 동기화를 시도한다", target_fixture="response")
def sync_nonexistent():
    return run_async(_request("post", "/api/schedules/sync/99999"))


# -- Then Steps --

@then("동기화 결과에 synced_count가 0보다 크다")
def check_synced_count(response):
    assert response.status_code == 200
    data = response.json()
    assert data["synced_count"] > 0


@then("학교의 last_sync_at이 업데이트된다")
def check_last_sync(response):
    data = response.json()
    assert data["synced_at"] is not None


@then("일정 목록에 이벤트가 포함된다")
def check_events_exist(response):
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0


@then("각 이벤트에 date, title, category가 포함된다")
def check_event_fields(response):
    data = response.json()
    for ev in data:
        assert "date" in ev
        assert "title" in ev
        assert "category" in ev


@then("해당 월의 이벤트 목록이 반환된다")
def check_calendar_events(response):
    assert response.status_code == 200
    data = response.json()
    assert "events" in data
    assert len(data["events"]) > 0


@then("exam_periods 정보가 포함된다")
def check_exam_periods(response):
    data = response.json()
    assert "exam_periods" in data


@then(parsers.parse('반환된 모든 일정의 카테고리가 "{expected}"이다'))
def check_all_categories(response, expected):
    assert response.status_code == 200
    data = response.json()
    for ev in data:
        assert ev["category"] == expected


@then("404 에러가 반환된다")
def check_not_found(response):
    assert response.status_code == 404
