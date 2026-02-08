Feature: NEIS API 클라이언트
  NEIS 교육정보 개방포털 API와 직접 통신하는 클라이언트 검증

  Scenario: 학교명 검색 성공
    Given NEIS API 클라이언트가 생성되어 있다
    When "대치"로 학교를 검색한다
    Then 검색 결과가 1개 이상 반환된다
    And 각 결과에 atpt_code, sd_code, name 필드가 있다

  Scenario: 짧은 키워드 검색
    Given NEIS API 클라이언트가 생성되어 있다
    When "가"로 학교를 검색한다
    Then 검색 결과가 반환된다

  Scenario: 존재하지 않는 학교 검색
    Given NEIS API 클라이언트가 생성되어 있다
    When "XYZNONEXISTENT999"로 학교를 검색한다
    Then 빈 검색 결과가 반환된다

  Scenario: 학사일정 조회 성공
    Given NEIS API 클라이언트가 생성되어 있다
    When 대치중학교의 2025년 3월 일정을 조회한다
    Then 일정 데이터가 1개 이상 반환된다
    And 각 일정에 date, title, category 필드가 있다

  Scenario: 이벤트 카테고리 자동 분류
    Given NEIS API 클라이언트가 생성되어 있다
    When 이벤트명 "1학기 중간고사"를 분류한다
    Then 카테고리가 "exam"으로 분류된다

  Scenario: 날짜 포맷 변환
    Given NEIS API 클라이언트가 생성되어 있다
    When NEIS 날짜 "20260302"를 변환한다
    Then "2026-03-02" 형식으로 변환된다
