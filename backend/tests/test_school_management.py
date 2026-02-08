"""BDD tests for School Management - 학교 CRUD 관리"""
import asyncio
import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from httpx import AsyncClient, ASGITransport
from main import app

scenarios("features/school_management.feature")


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

@given("NEIS API 키가 설정되어 있다")
def api_key_set():
    import os
    assert os.getenv("NEIS_API_KEY") is not None


@given("이미 등록된 학교가 있다", target_fixture="context")
def existing_school(clean_db):
    clean_db.execute(
        "INSERT INTO schools (name, atpt_code, sd_code, school_type, color) VALUES (?, ?, ?, ?, ?)",
        ("테스트중학교", "T10", "8888888", "middle", "#3b82f6")
    )
    clean_db.commit()
    row = clean_db.execute("SELECT id FROM schools WHERE sd_code = '8888888'").fetchone()
    return {"school_id": row["id"]}


@given("등록된 학교가 1개 이상 있다", target_fixture="context")
def at_least_one_school(clean_db):
    clean_db.execute(
        "INSERT INTO schools (name, atpt_code, sd_code, school_type, color) VALUES (?, ?, ?, ?, ?)",
        ("목록테스트학교", "T11", "7777777", "high", "#22c55e")
    )
    clean_db.commit()
    row = clean_db.execute("SELECT id FROM schools WHERE sd_code = '7777777'").fetchone()
    return {"school_id": row["id"]}


@given("등록된 학교가 있다", target_fixture="context")
def registered_school(clean_db):
    clean_db.execute(
        "INSERT INTO schools (name, atpt_code, sd_code, school_type, color) VALUES (?, ?, ?, ?, ?)",
        ("수정테스트학교", "T12", "6666666", "high", "#ef4444")
    )
    clean_db.commit()
    row = clean_db.execute("SELECT id FROM schools WHERE sd_code = '6666666'").fetchone()
    return {"school_id": row["id"]}


# -- When Steps --

@when(parsers.parse('"{keyword}" 키워드로 학교를 검색한다'), target_fixture="response")
def search_schools(keyword):
    return run_async(_request("get", f"/api/schools/search?keyword={keyword}"))


@when("학교 정보를 입력하여 등록한다", target_fixture="response")
def create_school(clean_db):
    return run_async(_request("post", "/api/schools", json={
        "name": "신규테스트학교",
        "atpt_code": "N01",
        "sd_code": "1111111",
        "school_type": "high",
        "color": "#a855f7"
    }))


@when("같은 atpt_code와 sd_code로 학교를 등록한다", target_fixture="response")
def create_duplicate_school(context):
    return run_async(_request("post", "/api/schools", json={
        "name": "중복학교",
        "atpt_code": "T10",
        "sd_code": "8888888",
        "school_type": "middle",
        "color": "#3b82f6"
    }))


@when("학교 목록을 조회한다", target_fixture="response")
def get_school_list():
    return run_async(_request("get", "/api/schools"))


@when("학교의 색상을 변경한다", target_fixture="response")
def update_school_color(context):
    return run_async(_request("patch", f"/api/schools/{context['school_id']}", json={
        "color": "#000000"
    }))


@when("해당 학교를 삭제한다", target_fixture="response")
def delete_school(context):
    resp = run_async(_request("delete", f"/api/schools/{context['school_id']}"))
    return {"delete_response": resp, "school_id": context["school_id"]}


# -- Then Steps --

@then("검색 결과에 학교 목록이 반환된다")
def check_search_results(response):
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@then("각 학교에 atpt_code, sd_code, name, school_type, address가 포함된다")
def check_search_result_fields(response):
    data = response.json()
    if len(data) > 0:
        for school in data:
            assert "atpt_code" in school
            assert "sd_code" in school
            assert "name" in school
            assert "school_type" in school
            assert "address" in school


@then("학교가 정상적으로 생성된다")
def check_school_created(response):
    assert response.status_code == 201


@then("생성된 학교에 고유 ID가 부여된다")
def check_school_has_id(response):
    data = response.json()
    assert "id" in data
    assert isinstance(data["id"], int)


@then("409 Conflict 에러가 반환된다")
def check_conflict(response):
    assert response.status_code == 409


@then("등록된 모든 학교 정보가 반환된다")
def check_all_schools(response):
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1


@then("각 학교에 event_count가 포함된다")
def check_event_count_field(response):
    data = response.json()
    for school in data:
        assert "event_count" in school


@then("학교 정보가 정상적으로 업데이트된다")
def check_school_updated(response):
    assert response.status_code == 200
    data = response.json()
    assert data["color"] == "#000000"


@then("204 상태코드가 반환된다")
def check_delete_status(response):
    assert response["delete_response"].status_code == 204


@then("학교 목록에서 해당 학교가 제거된다")
def check_school_removed(response):
    resp = run_async(_request("get", "/api/schools"))
    schools = resp.json()
    ids = [s["id"] for s in schools]
    assert response["school_id"] not in ids
