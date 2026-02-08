Feature: 학교 관리
  학부모/학생이 자녀 학교를 등록하고 관리할 수 있다.

  Scenario: NEIS에서 학교 검색
    Given NEIS API 키가 설정되어 있다
    When "서울" 키워드로 학교를 검색한다
    Then 검색 결과에 학교 목록이 반환된다
    And 각 학교에 atpt_code, sd_code, name, school_type, address가 포함된다

  Scenario: 학교 등록
    Given NEIS API 키가 설정되어 있다
    When 학교 정보를 입력하여 등록한다
    Then 학교가 정상적으로 생성된다
    And 생성된 학교에 고유 ID가 부여된다

  Scenario: 중복 학교 등록 방지
    Given 이미 등록된 학교가 있다
    When 같은 atpt_code와 sd_code로 학교를 등록한다
    Then 409 Conflict 에러가 반환된다

  Scenario: 학교 목록 조회
    Given 등록된 학교가 1개 이상 있다
    When 학교 목록을 조회한다
    Then 등록된 모든 학교 정보가 반환된다
    And 각 학교에 event_count가 포함된다

  Scenario: 학교 정보 수정
    Given 등록된 학교가 있다
    When 학교의 색상을 변경한다
    Then 학교 정보가 정상적으로 업데이트된다

  Scenario: 학교 삭제
    Given 등록된 학교가 있다
    When 해당 학교를 삭제한다
    Then 204 상태코드가 반환된다
    And 학교 목록에서 해당 학교가 제거된다
