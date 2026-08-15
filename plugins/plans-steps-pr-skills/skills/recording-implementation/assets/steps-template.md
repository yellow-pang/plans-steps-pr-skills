<!-- R2 compact: keep only sections that explain the result, flow, evidence, and risk. -->
<!-- R3 full: keep every evidence-bearing section below. -->
<!-- Do not repeat empty sections or write `해당 없음`; remove them. -->

# 구현 기록: 작업 이름

## 1. 한눈에 보는 결과

사용자 또는 시스템 관점에서 달라진 결과를 먼저 설명한다.

## 2. 변경 전과 변경 후

| 구분 | 변경 전 | 변경 후 |
|---|---|---|
| 핵심 동작 | 확인된 이전 상태 | 실제 구현된 상태 |

## 3. 핵심 구현 흐름

세 개 이상의 구성 요소, 분기 또는 상태 전이가 있을 때만 Mermaid로 표현한다. 그보다 단순하면 짧은 순서 설명을 사용한다.

## 4. 주요 파일과 역할

| 파일 | 역할 | 중요한 변경 |
|---|---|---|
| 실제 경로 | 현재 책임 | diff로 확인한 내용 |

## 5. 계약·데이터·상태 변화

입력, 출력, 오류, 저장 형식, 상태 전이와 호환성 영향을 설명한다.

## 6. Plan과 달라진 내용

승인 범위 안의 실제 차이와 이유만 기록한다. material change가 있었다면 정상 완료로 덮지 말고 재승인 증거를 연결한다.

## 7. Verification ledger

| Command | Result | HEAD / environment | Scope | Executed at |
|---|---|---|---|---|
| 실제 실행 명령 | exit status와 결과 | 실행 기준 | 검증 범위 | ISO-8601 |

## 8. 실행하지 못한 검증

실행하지 못한 검사, 구체적 이유, 대체 증거, 남은 위험을 적는다.

## 9. 알려진 제한과 후속 작업

현재 결과의 제한과 별도 승인·작업이 필요한 후속 범위를 구분한다.
