Feature: 학사일정 동기화
  등록된 학교의 학사일정을 NEIS API에서 가져와 동기화한다.

  Scenario: 단일 학교 일정 동기화
    Given 등록된 학교가 있다
    When 해당 학교의 일정을 동기화한다
    Then 동기화 결과에 synced_count가 0보다 크다
    And 학교의 last_sync_at이 업데이트된다

  Scenario: 동기화 후 일정 조회
    Given 일정이 동기화된 학교가 있다
    When 해당 학교의 일정 목록을 조회한다
    Then 일정 목록에 이벤트가 포함된다
    And 각 이벤트에 date, title, category가 포함된다

  Scenario: 캘린더 뷰 데이터 조회
    Given 일정이 동기화된 학교가 있다
    When 특정 년월의 캘린더 데이터를 조회한다
    Then 해당 월의 이벤트 목록이 반환된다
    And exam_periods 정보가 포함된다

  Scenario: 카테고리별 일정 필터링
    Given 일정이 동기화된 학교가 있다
    When "holiday" 카테고리로 일정을 필터링한다
    Then 반환된 모든 일정의 카테고리가 "holiday"이다

  Scenario: 존재하지 않는 학교 동기화 시도
    When 존재하지 않는 학교 ID로 동기화를 시도한다
    Then 404 에러가 반환된다
