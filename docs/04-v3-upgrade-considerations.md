# v3 업그레이드 구체 설계

설계 기준: 2026-09-27. **사용자 요구를 구현 가능한 추천 설계로 구체화한 당시 기록이다.** 이후 같은 브랜치에 v3 `SKILL.md` 7개와 행동 평가 명세를 작성했다. 아래의 “아직 구현하지 않았다”는 표현은 설계 시점의 상태를 뜻한다. 현재 구현·검증 상태는 [Steps](steps/2026-09-27-v3-skill-implementation.md)를 본다.

## 1. 근거와 상태의 구분

| 구분 | 이 문서에서의 의미 |
|---|---|
| 기존 원문 사실 | main `d7c0887e8d8fe2a4ca847c821a46f85bfba88e7a`의 5개 Skill, v2 `eb70e3f72dcbe23bc76245e3b8ad12f841279154`의 실제 파일에서 확인한 내용 |
| 기존 분석의 문제 | 선택 경계·승인 재사용·완료 지점 등의 정적 평가. [Q01~Q24](02-enforcement-and-request-evaluation.md)는 실측 결과가 아님 |
| 새 사용자 요구 | 이번 첨부문에 적힌 실제 경험·원하는 방향. 과거 main/v2의 동작 증거로 소급하지 않음 |
| 추천 설계 | 사용자 요구로부터 도출한 구체 구조·책임·파일 배치. 다음 구현의 기준안이며 사용자가 모든 세부를 직접 선택했다는 뜻은 아님 |
| 남은 사용자 결정 | 핵심 설계에 반드시 필요한 미결정은 없음. 실행 당시 대상·권한 확인과 미확인 ponytail은 별도로 구분 |

사용자 요구는 2026-09-27의 두 첨부문에 근거한다. 최초 workflow 요구는 `C:/Users/bigbros/.codex/attachments/da4cdaa9-807c-46e4-a843-d26f83d4e8a6/붙여넣은 텍스트.txt`, 이번 구체 설계 요청은 `C:/Users/bigbros/.codex/attachments/a351945f-d3e2-4aba-9575-a7291730b687/붙여넣은 텍스트.txt`다. 첨부 없이도 이어갈 수 있도록 주요 결정과 구현 범위를 아래에 남긴다.

### 원문을 다시 대조한 결과

| 주제 | 기존 main/v2에서 확인된 사실 | 기존 분석 또는 이번 대조에서 도출한 문제 |
|---|---|---|
| 최소 수정과 영향 | main 구현 원문 24·30행에 최소 변경/최소 수정이 있고, 28행에 producer·consumer·타입·오류 처리·문서·테스트 확인이 이미 있음 | lifecycle 고려가 없었던 것이 아님. 분석 범위를 넓힐 조건과 영향이 닫혔음을 판단하는 기준은 명시되지 않음 |
| Plan과 복잡도 | main Plan은 진입점·계약 조사, 유지보수성·호환성·검증 가능성 등의 대안 비교와 검증 계획을 요구 | abstraction의 가치, 계층별 중복 validation/test, 관측되지 않은 외부 값의 계약화를 검토하는 기준은 부족 |
| 진행 중 기록 | Plan은 앞으로 할 일, Steps는 완료 사실·결과·근거 중심이며 시간순 재현과 Plan 반복을 지양 | Plan 이전부터 유지하는 작업 context의 책임과 갱신 기준은 5개 Skill에 없음 |
| 테스트·mock | main 5개 Skill에 TDD·mock·fixture 강제나 기존 테스트 무조건 보존 규칙은 없음 | 사용자 경험을 main이 과잉 테스트를 강제했다는 증거로 사용할 수 없음. 외부 관측과 테스트 유효성의 판단 기준을 새로 설계할 필요 |
| v2 테스트 | v2 구현은 새 동작/재현 버그에 구현 전 실패 테스트를 요구하고 비코드에도 먼저 RED 확인을 요구. 올바른 테스트를 GREEN만 얻으려고 약화·삭제하지 못하게 함 | 모든 기존 테스트가 올바르다고 선언한 규칙은 아님. 오래된 테스트·잘못된 fixture 등을 판별하는 기준은 별도로 보완할 후보 |
| v2 lifecycle | v2 PR 검토에도 producer/consumer·오류·데이터/상태 전이·호환성·롤백 추적이 있음 | lifecycle 관점 자체가 새로 생기는 것은 아님. 구현 이전 분석·Plan 검토와 조사 종료 근거를 구체화할 후보 |
| 검증 재사용 | main은 각 단계의 관련 검증과 실제 기록 확인을 요구하며 commit 뒤/PR 전 전체 재실행을 강제하지 않음. v2는 same HEAD·관련 환경·동등한 입력의 근거 재사용과 무효화 조건을 이미 명시 | v2가 무조건 반복을 요구했다고 쓰면 부정확. commit 전후 관련 코드가 동일한 경우와 변경된 환경·위험의 판단을 정교화할 후보 |
| Git 책임 | main은 메시지 준비·PR 설명 중심, v2에는 실행 전문 Skill이 있음 | 최초 workflow 설명만으로는 실행 책임이 미정이었으나, 이번 후속 요청에서 PREPARE/EXECUTE 두 경로 지원이 확정됨 |

main 근거: [구현](https://github.com/yellow-pang/plans-steps-pr-skills/blob/d7c0887e8d8fe2a4ca847c821a46f85bfba88e7a/skills/implementation-workflow/SKILL.md#구현), [Plan](https://github.com/yellow-pang/plans-steps-pr-skills/blob/d7c0887e8d8fe2a4ca847c821a46f85bfba88e7a/skills/task-planning/SKILL.md), [Steps](https://github.com/yellow-pang/plans-steps-pr-skills/blob/d7c0887e8d8fe2a4ca847c821a46f85bfba88e7a/skills/steps-documentation/SKILL.md), [커밋 준비](https://github.com/yellow-pang/plans-steps-pr-skills/blob/d7c0887e8d8fe2a4ca847c821a46f85bfba88e7a/skills/preparing-commit/SKILL.md), [PR 설명](https://github.com/yellow-pang/plans-steps-pr-skills/blob/d7c0887e8d8fe2a4ca847c821a46f85bfba88e7a/skills/pr-documentation/SKILL.md). v2 근거: [구현 원문][v2-implementation], [검증 정책][v2-verification], [PR 검토 원문][v2-review]. main 상대 링크는 작업 트리를 가리키므로 향후 변경 시 위 기준 SHA의 원문과 구분한다.

## 2. 사용자 확정 요구와 채택한 설계 방향

실제 workflow는 요구사항 → Branch → 코드·문서 조사 → Agent 분석 → GPT 분석 검토 → 필요 시 추가 분석 → Plan → GPT Plan 검토 → 새 세션 구현·검증 → Steps → GPT의 요구·기존 서비스 영향·lifecycle 검수 → Commit 단위·메시지 확인 → Commit → 필요한 PR 검증·설명 → 직접/Agent PR이다. **이 순서는 선택 가능한 책임의 연결이며 모든 작업의 필수 순서가 아니다.**

- Superpowers는 실제 v3 workflow에서 사용하지 않는다. Superpowers·Spec Kit·BMAD는 참고 자료이며 기준 방법론이 아니다.
- 주 실행 환경은 사용자가 지정한 **GPT-5.6 Sol + Medium reasoning**이다. 모델의 실제 준수 능력을 검증했다는 의미는 아니다.
- 분석은 확인된 영향이 이어지는 범위까지 넓히고, 수정은 그 영향을 해결하는 만큼 수행한다.
- 관측·테스트 유효성·검증 재사용·고유 실패 보호·abstraction의 가치로 판단한다. 고정 위험 등급, 승인 digest, 상태 머신, 긴 체크리스트를 기본 구조로 만들지 않는다.
- **Commit·Push·PR은 PREPARE/EXECUTE 두 경로를 지원한다.** 메시지/설명 요청은 준비에서 끝나고, 명시 실행 요청과 유효한 권한이 있을 때만 해당 실행을 한다. 이 지원 결정이 현재 설계 작업에서의 Git 실행 허가는 아니다.
- Steps는 배경·문제·변경·이유·전후 구조/흐름·검증·제한을 설명한다. 작은 작업의 분량은 줄이되 확인되지 않은 이유를 만들지 않는다.
- 첫 구현은 **독립 Skill 7개**로 구성한다. 새 분석/context 역할과 통합 검토 역할을 추가하고 Git 두 역할은 개명·확대한다. Plugin 패키징은 첫 구현에서 제외한다.
- Context만을 위한 Skill, Plan Review만을 위한 Skill, 총괄 router는 두지 않는다. 반복되는 독립 분석과 검토 요청만 별도 진입점으로 만든다.

H(Hard invariant): 사실·가정·미실행을 구분하고, 사용자 변경과 권한을 보존하며, PREPARE에서 Git/PR을 실행하지 않는다.
D(Decision rule): 조사 깊이·종료, 테스트 유효성·수준·재사용, Browser 관측, 수정 범위·abstraction을 근거로 판단한다.
P(Preference / workflow aid): Context·Plan·Steps·독립 검토·메시지 사전 확인은 요청과 작업 필요에 따라 선택한다. 선택된 작업의 책임은 수행하지만 다른 모든 작업의 선행 조건으로 승격하지 않는다.

## 3. 사용자 요구와 구체 설계 매핑

이전 U01~U13의 요구 식별자를 유지한다. 아래 역할 배치는 사용자 경험을 main/v2의 과거 실패 원인으로 소급한 것이 아니다.

| ID·문제 | 원하는 행동 | 분류 | 담당 설계 | 이번 결정 |
|---|---|---|---|---|
| U01 downstream·상태 전이 누락 | 영향 추적 후 필요한 만큼 수정 | D | 분석·Plan·구현, 4.1절 | 최소 diff 표현을 영향 해결 기준으로 대체 |
| U02 긴 작업의 context 손실 | 중요한 지식·결정을 지속 기록 | P, 사실성 H | 분석 역할 + 현재 작업자, 8절 | 별도 Context Skill 없이 선택적 문서 관리 |
| U03 미관측 값의 계약화 | 관측·안정성 판단 후 반영 | H/D | 분석·구현·검토, 4.3절 | 미관측 부분만 가정/한계로 남기고 독립 작업은 진행 |
| U04 오래된 테스트에 구현 맞춤 | 유효한 요구·runtime·계약과 비교 | D/H | 구현·검토 | 수정·삭제 근거와 남는 보호 범위 설명 |
| U05 추측 mock/fixture | 확인된 boundary 또는 명시적 시뮬레이션 | D/H | 구현, verification reference | 실제 관측과 합성 자료를 구분 |
| U06 반복 검증 | 유효한 증거 재사용·필요한 무효화 | D/H | 구현·검토·Git, 4.4절 | 같은 SHA 여부보다 관련 내용·환경·위험 확인 |
| U07 중복 테스트 | 고유 실패 범위 검토 | D | Plan·검토·구현 | 동일 값 중첩과 다른 경계의 보호를 구분 |
| U08 불필요한 abstraction·validation | 실제 가치·복잡도·확장성 판단 | D | Plan·검토·구현, 4.5절 | 관련 있는 비용만 확인, 파일/class 수 기준 배제 |
| U09 늦은 방향 오류 발견 | 분석·Plan·구현 결과 독립 검토 | D/P | reviewing-development-work | 하나의 검토 Skill에서 대상별 관점 선택 |
| U10 ponytail 중복 | 실물 근거로 통합 판단 | D | 이번 핵심 설계에서 제외 | 미확인 유지; 전체 구현의 선행 조건 아님 |
| U11 규칙·gate 과잉 | H/D/P 분리 | H/D/P | 각 Skill 핵심 + 역할별 참조, 7절 | 공통 router·상태 머신 없이 독립 동작 |
| U12 요청 완료 지점 누락 | PREPARE/EXECUTE와 실행 종류 구분 | H/D/P | commit-workflow·pr-workflow, 9절 | 명시 실행까지 지원; 이미 받은 권한 재질문 안 함 |
| U13 작은 작업의 과한 절차 | 필요한 조사·수정·확인으로 종료 | D/P | 직접 구현 경로, 5절 | Plan/context/Steps/후속 Skill 기본 비강제 |

## 4. 구현에 적용할 판단 기준

### 4.1 분석 범위와 수정 범위

main의 `최소 변경/최소 수정` 표현은 다음 기준으로 대체한다. 관련 없는 정리를 배제하는 목적은 유지한다.

> 요청과 관련된 영향이 어디까지 이어지는지 먼저 확인한다. 수정은 요구사항과 확인된 영향을 해결하는 데 필요한 만큼 수행하고, 무관한 변경은 섞지 않는다.

진입 조건은 데이터 shape·상태 전이·API·DB persistence·async worker/job·Browser/Provider·event/message·downstream·UI 등 관련 경계의 의미가 바뀌는 경우다. producer → transformation → persistence → worker/service → consumer → UI는 조사할 수 있는 경로의 예시다. 모든 저장소에서 이 순서를 강제하거나 없는 계층을 만들지 않는다. 데이터·상태·API·DB·Browser·provider·async 경계를 바꾸면 앞뒤 IO, 소비자의 가정, 관련 오류·재시도·상태 전이를 살핀다. 실제 영향이 없는 재시도나 정리 단계까지 항상 조사하는 규칙은 두지 않는다.

조사 종료는 파일 수보다 근거로 판단한다. 예를 들어 직접 소비자를 확인했고 인터페이스·상태 의미가 유지되며 추가 경계에 영향이 없다는 근거가 있으면 멈출 수 있다. 반대로 영향이 남아 있는데 diff가 작다는 이유로 멈추지 않는다. 영향 분석으로 발견한 관련 작업과 원래 요청 밖의 제품 변경을 구분하고, 후자에 필요한 사용자 선택을 임의로 대신하지 않는다.

### 4.2 지속 가능한 context와 Plan·Steps의 역할

| 자료 | 목적 | 남길 정보 | 반복하지 않을 내용 |
|---|---|---|---|
| Context | 분석 초기부터 다음 판단·세션의 연속성 유지 | 원래 요구, 현재 구조·lifecycle, 코드/runtime 관측 근거와 조건, 영향 가능 영역, 결정, 미확정, 폐기 대안의 중요한 이유, Plan·구현 주의점 | 시각별 명령/파일 열람 일지, 긴 로그, 기존 문서 전체 복사 |
| Plan | 앞으로 수행할 변경과 완료 조건·검증을 구체화 | 채택 방향·근거, 범위·계약, 단계·선후관계, 위험·검증 | 분석 기록 전체, 아직 하지 않은 일을 완료 사실로 기재 |
| Steps | 실제 완료 결과와 검증·Plan 차이를 설명 | 실제 변경·이유·영향·결과·제한·후속 | Plan 복사, 확인 못한 결정·순서를 사후 창작 |

사용자가 제안한 **실제 코드/runtime/관측 → 현재 context → Plan/Steps**는 현재 상태를 확인하는 근거 순서로 적용한다. 문서가 낡았으면 실제 상태를 확인하고 차이를 정정한다. 코드·runtime·관측끼리도 버전·환경이 다를 수 있으므로 충돌 시 재확인한다.

원하는 동작을 정하는 최신 사용자 요구·합의된 계약과, 지금 무엇이 동작하는지를 입증하는 관측은 역할이 다르다. 기존 코드의 버그가 새 요구보다 우선하거나 낡은 context가 최신 Plan 결정을 덮어쓰도록 만들지 않는다. 문서 종류만으로 최신성을 보장하지 않고 근거·조건을 확인한다.

Context는 독립 선택 문서로 두고 분석 역할이 기본 생성 책임을 맡는다. 이후 중요한 사실을 바꾼 현재 역할이 갱신한다. 정확한 생성·종료·인계 조건은 8절에 정한다. 작은 작업에 파일 생성을 의무화하지 않는다.

### 4.3 외부 관측·mock·기존 테스트

`Observe before encode`는 **실제 값 관측 → 의미와 안정성 판단 → 필요한 동작을 테스트/계약에 반영**하는 원칙이다. DOM·URL·network·metadata·provider/API의 관측 경로, 버전·환경, 관측 조건을 필요한 만큼 남긴다. 한 번 본 값이 보편 계약이라는 결론으로 바로 넘어가지 않는다.

접근할 수 없으면 모르는 형태를 사실처럼 고정하지 않고 가정과 한계를 표시한다. 알려진 내부 계약의 독립 작업은 진행할 수 있고, 외부 형태가 없으면 정답을 결정할 수 없는 부분만 보류한다. fixture 전체나 민감한 외부 응답을 기록해야 한다는 뜻도 아니다.

mock/fixture는 통제하는 안정적 boundary, 명확한 IO, 관측으로 확인한 계약, 의도한 오류·edge case 재현에 유효할 수 있다. 합성한 오류 케이스는 시뮬레이션으로 표시하고 provider가 실제 반환한 오류처럼 취급하지 않는다. 미확인 예상 payload·DOM·오류 구조는 검증된 현실로 승격하지 않는다. 순수 내부 로직·이미 확인된 안정적 계약은 테스트 우선 접근이 가능하다.

`Tests protect valid behavior, not historical implementation.`를 다음 판단으로 적용한다.

| 실패 원인 후보 | 확인할 근거 | 가능한 대응 |
|---|---|---|
| 실제 회귀 | 현재 유효한 요구·계약, 변경 전후 관측 | 구현 수정과 관련 회귀 검증 |
| 오래된 테스트·요구 변경 | 최신 요구·합의된 변경과 테스트 기대값 차이 | 계약과 기대값을 함께 갱신하고 변경 이유 기록 |
| 잘못된 mock/fixture·외부 변화 | 실제 관측·외부 계약과 테스트 입력 차이 | fixture·adapter·계약 중 잘못된 부분 수정 |
| 구현 세부 결합·중복 검증 | 보호해야 할 동작과 각 테스트의 고유 실패 범위 | 동작 중심으로 개선, 보호 공백이 없으면 통합·제거 검토 |
| 원인 미확인 | 아직 근거가 부족함 | 미확인으로 남기고 완료에 필요한 부분 추가 조사 |

불편하거나 GREEN이 필요하다는 이유만으로 유효한 계약을 제거하지 않는다. 테스트를 바꿀 때도 현재 요구와 관측에 맞는지, 보호하던 실패를 잃는지 설명할 수 있어야 한다. 모든 테스트 변경마다 새 승인 절차를 붙이자는 제안은 아니다.

### 4.4 검증 근거 재사용과 고유 실패 범위

검증 선택은 단계 이름이나 횟수보다 현재 완료 판단에 필요한 증거로 정한다.

| 상황 | 검토할 증거 후보 |
|---|---|
| 실제 외부 동작·DOM/API 의미를 새로 판단 | 관련 Browser·외부 환경의 실제 관측 |
| 확인된 실제 fixture에 대한 순수 parser 변경 | 해당 edge case와 회귀를 확인하는 unit test로 충분할 수 있음 |
| Browser → 처리 → DB 등 연결 영향 | 계약 연결을 확인하는 integration·smoke·E2E 중 필요한 검증 |
| 같은 관련 코드·환경·입력의 유효한 이전 결과 | 기존 근거 재사용, 단계가 바뀌었다는 이유만으로 재실행하지 않음 |
| 코드·lock·생성물·설정·환경·입력/선택·요구 또는 위험 변화 | 그 변화로 무효화된 증거와 새 위험을 대상으로 재검증 |

결과 재사용 시 무엇을 검사했는지, 어떤 코드 상태·환경·입력에서 실제 실행됐는지 식별할 근거가 필요하다. 고정 ledger나 모든 명령의 timestamp 기록은 요구하지 않는다. 의미 있는 검증의 명령/관측, 결과, 대상 코드 상태, 관련 환경·입력, 확인한 위험을 응답 또는 기존 Context/Steps에 남기면 충분하다. HEAD가 같아도 working tree·환경이 다르면 충분하지 않다. 반대로 commit으로 SHA만 바뀌고 관련 내용이 같다는 근거가 있으면 재사용할 수 있다. commit hook 등이 내용을 바꿨다면 다시 비교한다. 저장소가 요구하는 CI 또는 새 외부 상태 확인을 과거 로컬 결과로 대신하지 않는다.

Plan에서 테스트를 여러 계층에 추가한다면 각 테스트가 어떤 다른 실패를 잡는지 본다. parser edge case, DB 저장 계약, 실제 Browser에서 저장까지의 연결 실패는 별개의 가치가 있다. 같은 값이 여러 테스트에 등장하는 것만으로 중복이라고 단정하지 않는다. 독립된 경계·설정·통합 실패를 잡는 중첩은 남기고, 고유 실패 보호가 없는 반복을 줄이는 방향이다.

### 4.5 Plan 검토와 복잡도

Plan 검토는 요구 해결 여부, 분석된 lifecycle·producer/consumer·계약, 관측 없는 가정, 기존 테스트의 유효성, abstraction·validation·테스트 중복, 더 단순한 대안, 유지보수성·합리적 확장, 위험에 맞는 검증을 살피는 별도 책임이며, 5절의 통합 검토 Skill에서 담당한다. 항목 전부를 매번 출력하는 양식으로 만들지 않는다.

abstraction은 파일·class 개수가 아니라 **현재 문제, 근거 있는 예상 변경, 중복 제거, 명확한 책임 분리**에 주는 가치로 판단한다. 새 state·metadata와 coupling, provider 추가 시 바뀔 지점도 실제 변경 가능성에 맞춰 본다. 이름이 Factory/Manager/Coordinator/Registry/Strategy라는 이유만으로 금지하지 않고, 존재 이유를 설명할 수 없는 계층을 과설계 후보로 본다.

성능·규모와 관련될 때만 시간·공간 복잡도, DB query·network 호출 수, Browser context/tab 수, concurrency 비용을 확인한다. 작은 변경에 형식적인 Big-O를 요구하지 않는다. 독립 GPT 검토는 현재 사용자 방식이다. 검토 자료를 넘길 수 있게 작성하되 별도 모델 호출·새 세션·재승인을 매 Plan의 필수 gate로 만들지 않는다.

### 4.6 ponytail 확인 범위와 한계

이전 요구 반영 단계의 문서 편집 전 worktree의 숨김·ignore 포함 파일명과 본문(`.git` 제외), tracked/untracked/ignored 목록, main·v2·HEAD의 파일 경로와 추적 본문을 조사했다. `ponytail` 관련 파일·설정·호출 관계를 찾지 못했다. 당시 untracked/ignored 파일 목록도 비어 있었다. 전역 설치 영역이나 다른 프로젝트에서 사용한 구현은 조사 범위가 아니다.

사용자가 과설계·중복 테스트 방지 목적으로 사용한다고 설명한 것은 **사용 목적**으로 기록할 수 있지만, 실제 기능·실행 방식·중복 범위의 증거는 아니다. 현재 역할, 독립 유지 가치, Plan 검토와의 중복, 흡수·제거 손실은 모두 **확인 불가**다. 추후 실제 파일·설정·호출 자료가 확보되면 이 부분만 비교한다. 이번 핵심 설계와 첫 구현에서 제외하며 다른 역할의 구현을 막지 않는다.

## 5. 제안하는 v3 Skill 구조와 인계

새 분석 책임은 Plan 이전의 독립 조사·인계 요청을, 새 검토 책임은 작성자와 다른 관점에서 분석·Plan·실제 구현을 검토하는 요청을 담당한다. Plan·구현에 필요한 작은 자체 조사·자기 점검은 그대로 남긴다. 독립 분석/검토 Skill을 반드시 먼저 호출하게 하지 않는다.

| 역할·추천 Skill 이름 | 책임·진입 조건 | 주요 입력 | 주요 산출물 |
|---|---|---|---|
| 분석·Context / `analyzing-work` | 구조·원인·영향 분석 또는 긴 작업 인계/재개 요청. 단순 함수 설명은 필요한 답변으로 끝낼 수 있음 | 요구·현재 코드/설정/runtime·관련 문서·기존 Context | 근거 있는 분석, 영향 종료 근거·미확정 사항, 필요 시 Context |
| Plan / `task-planning` | Plan 요청 또는 서로 다른 제품 결과·계약·접근 중 의미 있는 선택이 필요한 작업 | 요구·현재 상태·분석/Context(있을 때)·검증 수단 | 변경 범위·대안/추천·구현 단계·완료 조건·검증 계획 |
| 검토 / `reviewing-development-work` | 분석, Plan, 구현 결과의 검토 요청 또는 구체 위험 때문에 별도 점검이 필요한 경우 | 원래 요구 + 검토 대상 + 관련 코드·관측·diff·검증 근거 | 근거 있는 문제·영향·필요 수정·검토 한계, 문제가 없으면 그 범위 설명 |
| 구현 / `implementation-workflow` | 명확한 수정 요청 또는 현재 요청 범위의 Plan 구현 | 요청/Plan·현재 코드·기존 사용자 변경·Context/실측/테스트 | 실제 수정·필요한 검증·차이·남은 위험 |
| Steps / `steps-documentation` | 결과 기록 요청 또는 지속 기록 필요성. 파일은 요청/작업에 포함된 기록 범위에서 작성 | 실제 diff·관측·검증, 관련 Plan/Context | 배경·문제·변경 이유·전후 구조/흐름·검증·제한을 설명하는 Steps |
| Commit·Push / `commit-workflow` | 메시지/단위 준비 또는 실제 commit/push 요청 | status·staged/unstaged/untracked·현재 요청·검증 근거·remote/ref | PREPARE 자료 또는 실제 commit SHA / push 결과 |
| PR / `pr-workflow` | PR 설명 준비 또는 실제 생성/갱신 요청 | base/head·전체 branch diff·검증 근거·provider 도구·요청된 대상 | PR 제목/본문 또는 확인된 PR 식별자·URL·head/base·실행 결과 |

역할별 H는 2절의 공통 불변조건에 더해 아래 책임 경계를 뜻한다. 문서 내용이 실행 사실이나 권한을 대신하지 않는다.

| 역할 | 종료 조건 | 다음 역할과의 관계 | Hard invariant | 모델 판단 영역 |
|---|---|---|---|---|
| 분석·Context | 관련 계약·상태·소비자 영향과 종료 근거를 설명하거나, 남은 핵심 미확정과 해결 방법을 특정 | 요청된 경우 분석 검토·Plan·구현에 근거/미확정 전달 | 미확인을 사실로 확정하지 않음; 분석만 요청받고 코드를 수정하지 않음 | 조사 깊이·실측·Context 필요성 |
| Plan | 구현 방향·범위·단계·완료·검증과 사용자 선택이 필요한 부분이 구체적임 | Plan-only면 종료. 검토 요청이면 검토. 이미 구현까지 요청됐다면 해결된 범위부터 구현 | 계획을 완료 사실로 쓰지 않음; 미해결 제품 선택을 대신 확정하지 않음 | 대안·분할·분량·검증 설계 |
| 검토 | 중요 발견·근거·필요한 대응과 확인 한계 전달 | 발견별로 분석/Plan/구현에 반환; 검토만 요청이면 응답에서 종료 | 문서만으로 실제 정합성을 확정하지 않음; 검토 자체가 수정/실행 승인 아님 | 대상에 맞는 관점·추가 조사·검증 충분성 |
| 구현 | 요청 동작과 확인된 영향의 수정·필요 검증을 완료, 미확인 부분을 구분해 보고 | 기본은 완료 응답. Steps·검토·Git은 요청 범위에 있을 때만 연결 | 사용자 변경 보존·허위 성공 금지 | 영향 해결에 필요한 수정·테스트 유효성/재사용·복잡도 |
| Steps | 독자가 무엇이 왜 어떻게 달라졌고 무엇을 검증했는지 이해 가능 | 구현 검토의 보조 자료; 자동 Git 실행/새 모델 호출 없음 | 근거 없는 이유·수행 결과를 사후 창작하지 않음 | 분량·표·Mermaid·전후 비교 |
| Commit·Push | 메시지, commit, push 중 요청된 완료 지점과 실제 상태 확인 | PR은 요청된 경우만. PR의 필요 push는 같은 실행 경계를 적용 | PREPARE 무실행, 무관 변경 혼입·권한 확대 금지 | commit 단위·선택 staging·추가 검증 필요성 |
| PR | 준비 응답 또는 요청한 생성/갱신 상태 확인 | 코드 수정·추가 commit은 별도 요청 범위. merge를 포함하지 않음 | 실제 전체 diff 근거·PREPARE 무실행·중복 PR 방지 | provider 도구·필요 push·설명 분량·미확인 범위 |

### 진입·종료의 운영 기준

- 파일 수나 diff 길이만으로 Plan을 강제하지 않는다. 목표·유효 계약·수정 범위가 충분히 명확하면 구현에서 필요한 조사 후 진행한다. 불확실성이 조사로 해결되면 별도 사용자 선택이나 Plan 파일을 만들 이유가 되지 않는다.
- “계획만”, “분석만”, “검토만”은 해당 산출물에서 종료한다. “계획부터 구현까지”는 이미 받은 구현 요청을 유지한다. 새로운 제품 의미·범위·외부 영향에 실제 선택이 필요한 부분만 확인하며 전체를 반복 승인으로 묶지 않는다.
- 분석 종료는 관련 producer/consumer·상태 전이·경계의 영향이 확인되고 추가 전파가 없다는 근거가 있을 때다. 자료가 없어 영향 종료를 입증하지 못하면 그 부분을 미확인으로 보고한다. 조사 응답 종료와 구현 완료는 다른 판단이다.
- 단순 수정 후 기본 산출물은 짧은 완료 응답이다. Context·Plan·Steps의 파일을 항상 생성하지 않는다. 문서 위치는 사용자 지정 → 저장소 지침/관례 → 해당 역할의 기본 경로, 언어는 사용자 요청 → 저장소 관례 → 현재 대화 언어로 정한다.
- 인계는 필요한 요구·결정·현재 범위·근거·미확정·요청 완료 지점만 전달한다. 원문과 변경 상태를 재확인하되 조사 전체를 반복하거나 모든 Skill을 읽지 않는다.
- 선택은 각 description이 맡고 총괄 router를 추가하지 않는다. 분석/Plan/구현/기록/메시지/실행 의도를 구분하는 예시를 본문에 짧게 둔다. 일반 자동 선택을 유지하며 EXECUTE는 선택 여부와 별도로 명시 요청·유효 권한을 확인한다.
- 일반 작업 요청 자체가 branch/worktree 생성 지시는 아니다. 사용자가 선택한 현재 작업 위치를 유지하고 별도 branch 생성이 필요한 요청은 그 요청 범위에서 처리한다.

### 검토 대상과 독립성

`reviewing-development-work`는 분석·Plan·구현 결과 세 대상을 하나의 책임으로 다룬다. 분석 검토는 사실/가정과 누락 영향, Plan 검토는 4.5절의 설계·검증 방향, 구현 검토는 원래 요구·실제 diff/runtime·기존 서비스 영향·lifecycle·검증을 본다. Steps는 탐색용 입력이며 실제 구현 대신 믿지 않는다.

기본 검토는 읽기와 필요한 근거 확인, 발견 보고까지다. “검토하고 고쳐줘”는 검토 결과를 기존 구현 요청에 인계해 수정할 수 있다. 별도 세션/다른 GPT에 사용자가 전달하거나 가능한 독립 검토자를 활용할 수 있지만, 다른 모델·특정 도구·새 세션을 일괄 필수화하지 않는다. 같은 작성자가 자기 점검했으면 독립 검증이라고 보고하지 않는다. 리뷰 통과 문자열·상태값·digest로 실행을 막는 gate를 두지 않는다.

## 6. 현재 main의 5개 Skill 변경 매핑

원문 기준은 `d7c0887`이며 지금 파일을 변경한 결과가 아니다.

| 현재 Skill | 분류·v3 경로 | 유지하는 실제 책임 | 변경 내용과 원문 근거 |
|---|---|---|---|
| task-planning | 내용 변경 / 동일 경로 | 조사 후 구현 가능한 Plan, 관련 문서 부재 허용 | 원문 10·16·45행의 조사/Plan 유지. 독립 분석·별도 검토는 신규 역할로 분리하되 자체 조사 삭제 안 함. 49행 일괄 승인 대기를 요청 완료 지점·기존 권한 기준으로 조정 |
| implementation-workflow | 내용 변경 / 동일 경로 | 10행의 직접 구현, 28행 producer/consumer 확인, 사용자 변경 보존 | 24·30행 최소 수정 표현을 4.1절로 대체. 27행 Plan 밖 변경은 기존 요청 안의 구현 상세 조정과 새 사용자 선택을 구분. 관측·유효 테스트·재사용 추가 |
| steps-documentation | 책임 유지·내용 보강 / 동일 경로 | 35~44행에 이미 목적·문제·이유·흐름·검증·제한 포함 | 짧은 로그를 새 보고서로 바꾸는 것이 아님. 기존 설명 책임에 전후 구조·필요한 시각 자료·Context와의 역할 차이 보강 |
| preparing-commit | 개명·역할 확대 / commit-workflow | staged 우선·diff별 범위·관련 untracked 선별·메시지 PREPARE | 10행 메시지 전용·58행 실행 금지를 요청별 EXECUTE로 확대. 무관 변경 혼입 금지는 유지하고 목적별 분리·사전 메시지 확인은 판단/선호로 조정 |
| pr-documentation | 개명·역할 확대 / pr-workflow | 15행 전체 PR diff·문서 없는 작성, 제목/본문 PREPARE | 10·49행 생성 금지를 명시 요청의 생성/갱신으로 확대. provider 공통 책임과 실제 도구 선택을 분리 |

기존 역할을 제거하지 않는다. 개명하는 두 옛 경로만 첫 구현에서 새 경로로 이동한다. 별도 alias Skill을 동시에 설치하지 않고 README에 이름 대응을 안내한다. 역사 분석의 원문 상대 링크는 실제 이동 시 위 main 고정 SHA로 교체해 근거가 끊기지 않게 한다. 내용 분석을 v3 동작으로 소급 변경하지 않는다.

## 7. 공통 원칙 배치와 최초 파일 구성

**독립 설치·독립 호출이 가능한 구조**로 정한다. 각 `SKILL.md`에는 역할 수행에 필요한 짧은 핵심을 직접 두고, 긴 조건별 판단은 그 Skill 안의 reference로 분리한다. 다른 Skill 폴더나 저장소 루트의 정책 파일을 반드시 읽어야 동작하는 구조는 만들지 않는다.

| 원칙 | 배치안 | 중복을 줄이는 방식 |
|---|---|---|
| 사실성·변경 보존·요청/권한 | 관련 각 SKILL의 짧은 H | 독립 동작에 필요한 짧은 중복만 허용; 정책 설명 전체 복제 금지 |
| lifecycle·분석 종료·관측 | analyzing-work 본문에 조사 기준; 구현 본문에 계약 영향 확인 | Plan은 조사 지침 재서술 대신 영향에 맞는 변경·검증을 결정, Review는 누락을 확인 |
| Context lifecycle | analyzing-work/references/context-lifecycle.md | 다른 역할에는 필요 시 생성 조건·최소 내용·기본 경로와 중요한 사실/결정의 갱신 기준만 짧게 포함. 상세 lifecycle은 분석 역할에 둠 |
| test validity·mock·verification reuse | implementation-workflow/references/verification.md | Plan에는 고유 실패·검증 선택, Review에는 근거 검수, Git에는 관련 변화와 증거 적용성만 기재 |
| Plan/분석/실제 구현 검토·복잡도 | reviewing-development-work/references/review-lenses.md | 대상별 필요한 절만 읽음. Plan은 대안의 실제 가치 판단만 핵심에 포함 |
| staging·실행·실패 복구 | commit-workflow/references/execution.md | PREPARE는 실행 상세를 불필요하게 로드하지 않음 |
| provider의 PR 실행 | pr-workflow/references/provider-operations.md | 공통 입력·권한은 본문, 실제 도구 조회/생성/갱신/결과 확인은 조건부 참조 |

이 문서가 설계의 공통 근거다. 실행 시 반드시 읽는 공통 정책 Skill이나 repository-global reference는 첫 구현에 두지 않는다. 짧은 원칙의 의미 일치는 리뷰와 행동 평가로 확인하며 문구 동기화 생성기·규칙 문자열 테스트를 추가하지 않는다.

첫 구현의 소스 구성:

```text
skills/
  analyzing-work/SKILL.md                         신규
    references/context-lifecycle.md
  task-planning/SKILL.md                          기존 개편
  reviewing-development-work/SKILL.md             신규
    references/review-lenses.md
  implementation-workflow/SKILL.md                기존 개편
    references/verification.md
  steps-documentation/SKILL.md                    기존 개편
  commit-workflow/SKILL.md                        preparing-commit에서 이동·개편
    references/execution.md
  pr-workflow/SKILL.md                            pr-documentation에서 이동·개편
    references/provider-operations.md
tests/behavior/cases.md                           10절의 실행 가능한 평가 명세
```

위는 앞으로 만들 파일 목록이며 현재 생성된 파일이 아니다. reference는 본문에 읽을 조건과 링크를 둔다. 첫 구현에 실행 script, provider SDK/registry, Plugin manifest/marketplace, 정책 상태 파일은 추가하지 않는다. UI metadata는 실제 표시 필요가 있을 때 별도로 다루며 자동 선택을 끄는 기본 정책은 넣지 않는다.

## 8. Context lifecycle과 Plan·Steps 연결

| 항목 | 채택한 동작 |
|---|---|
| 생성 조건 | 사용자가 인계/지속 기록을 요청했거나, 긴 조사·다수 경계·여러 세션 작업에서 잃으면 판단이 바뀔 정보가 누적될 때 생성. 작은 수정·간단 설명에는 생략 |
| 생성 주체 | 독립 분석 중에는 analyzing-work. Plan/구현에서 처음 필요해지면 현재 역할이 같은 최소 목적의 Context를 직접 생성할 수 있음. 별도 Skill 호출을 의무화하지 않음 |
| 위치·이름 | 사용자/저장소 관례 우선, 없으면 `docs/context/<task-slug>.md`. 같은 작업의 Context가 있으면 갱신하고 중복 파일을 만들지 않음 |
| 내용 | 요구·현재 구조·lifecycle·중요 관측과 근거/조건·영향 가능 영역·결정·미확정·폐기 대안의 중요한 이유·Plan/구현 인계 사항·관련 문서/코드 상태 |
| 제외 | 모든 명령·열람 파일 목록·사소한 조사 과정·긴 로그·쉽게 다시 읽는 코드 복사. 코드 참조는 판단 근거를 찾는 데 필요한 경우만 |
| 갱신 조건·책임 | 중요한 사실/결정이 바뀌거나 무효화됐을 때 현재 작업자가 해당 부분 갱신. 도구 호출마다 갱신하지 않음. 리뷰-only는 발견을 보고하고 문서를 자동 수정하지 않음 |
| Plan 연결 | Context는 왜 그렇게 판단했는지의 현재 지식, Plan은 앞으로 할 일. Plan 작성 시 필요한 근거를 참조하고 전체 내용을 복사하지 않음 |
| Steps 연결 | Steps는 실제 결과·전후·검증·제한을 설명. Context/Plan에만 있는 일을 완료로 승격하지 않음 |
| 종료 조건 | 작업 완료·취소 시 필요한 지속 결정은 Steps 또는 관련 기존 문서에 연결하고 Context는 완료/취소와 재개 조건을 짧게 남겨 동결. 자동 삭제하지 않음. 후속 작업에 중요한 미확정은 보존 |
| 새 세션 사용 | Context에서 요구·결정·다음 작업을 먼저 복구한 뒤 저장소/branch·관련 코드 변화·관측 환경·증거 유효성을 재확인. 달라진 부분만 조사·수정하고 전체 분석을 반복하지 않음 |

파일 수정이 금지된 읽기 전용 요청/환경이면 같은 정보를 응답으로 전달한다. Context의 유용성만으로 금지된 파일 쓰기를 수행하지 않는다. 문서가 없다는 이유로 Plan·구현·Steps·Git을 일괄 중단하지 않는다.

## 9. PREPARE / EXECUTE와 provider 경계

PREPARE/EXECUTE는 **Git 역할 내부의 요청 구분**이며 전체 workflow의 Mode/Risk 또는 영구 상태값이 아니다. 출력마다 mode block을 강제하지 않는다.

| 사용자 요청 | 담당·경로 | 수행 범위·완료 지점 | 포함되지 않는 실행 |
|---|---|---|---|
| 메시지/제목/본문, commit 준비 | commit-workflow / PREPARE | 각 diff·관련 파일 확인, 단위·메시지·미포함 변경 제공 | staging·commit·push·PR |
| 현재 작업 commit | commit-workflow / EXECUTE | 확정 범위의 필요한 staging → commit → 포함 범위/SHA 확인 | push·PR |
| 현재 branch push | commit-workflow / EXECUTE | 확인한 remote/ref에 기존 commit 일반 push → 결과 확인 | 미커밋 변경 commit·PR |
| PR 설명/준비 | pr-workflow / PREPARE | 실제 base/head 차이·검증 근거 기반 제목/본문과 한계 제공 | staging·commit·push·PR 생성 |
| PR 생성 | pr-workflow / EXECUTE | 확정된 committed head의 필요한 일반 push → 조회/생성 → URL·head/base·상태 확인 | 미커밋 변경 자동 commit·무관 commit 공개·merge |
| 지정 PR 설명 갱신 | pr-workflow / EXECUTE | 해당 PR의 요청된 제목/본문 갱신·확인 | 코드 수정·새 commit·push·reviewer 지정·merge |
| commit·push·PR을 함께 요청 | 두 역할의 EXECUTE | 이미 요청된 각 완료 지점을 연결하고 실제 결과 확인 | 같은 권한 반복 질문, 요청 밖 history 변경 |

PR 생성에 필요한 push는 사용자가 금지하지 않았고 대상·공개할 commit 범위가 확실한 일반 push에 한정한다. 필요한 절차를 알리고 진행하되 같은 PR 실행 의사를 다시 묻지 않는다. 별도 push Skill을 반드시 호출할 필요는 없다. Git 공통 동작을 같은 원칙으로 적용한다. remote/base·공개 범위가 모호하거나 필요한 push가 금지된 경우 해당 실행만 보류하고 준비 자료는 완성한다.

### 변경 범위와 권한

- PREPARE는 index·HEAD·remote·PR을 변경하지 않는다. 요청한 메시지/문서 파일 작성은 허용하지만 Git 실행으로 확대하지 않는다. 기존 검증을 읽고 필요한 추가 검증을 제안하며, 검증까지 요청/작업 범위에 있는 경우 그 부분만 수행한다.
- EXECUTE는 현재 요청과 이전의 유효한 범위 지정을 재사용한다. “커밋해줘”가 자동으로 push·PR까지 허용하지 않는다. 요청의 의미가 명확하면 메시지 사전 확인을 추가 gate로 만들지 않는다.
- staged가 있으면 기본 commit 대상은 staged다. 사용자가 다른 포함 범위를 명시했으면 그 범위를 따른다. 같은 파일의 제외할 unstaged를 전체 파일 staging으로 끌어들이지 않는다.
- staged가 없으면 요청과 작업 근거로 관련 수정·안전하게 확인한 새 파일만 선택 staging한다. 기존 사용자 파일이라는 이유만으로 명시 포함된 변경을 배제하지 않는다.
- 무관 staged가 섞이면 index를 임의로 지우거나 재구성하지 않는다. 기존 index와 제외 hunk를 보존하는 선택 commit을 확실하게 할 수 있을 때만 진행하고, 분리가 불명확하면 구체 후보를 제시해 해당 범위만 확인한다.
- commit 분리는 목적·되돌리기·검증 가능성으로 추천한다. 하나의 목적의 코드·테스트·문서는 함께 묶을 수 있다. 사용자가 정확한 범위를 하나의 commit으로 지정했다면 형식 때문에 거부하지 않는다.
- 실행 직전 diff/index·대상 ref를 재확인한다. 변경 없는 검증은 재사용하며 hook 등이 관련 내용을 바꾸면 필요한 검사만 재판단한다. commit 요청만으로 모든 테스트 GREEN을 일괄 선행 조건으로 만들지 않으며 미검증·실패를 성공으로 표현하지 않는다.
- force push·reset·history rewrite·merge·무관 branch 공개는 일반 EXECUTE 권한에 포함하지 않는다. 그런 별도 요청은 그 범위·위험을 따로 판단한다. 이번 설계/첫 구현의 Git 기본 경로에 자동 파괴 동작을 두지 않는다.

### Provider별 실행과 실패 후 인계

공통 입력은 repository·remote·head/base·title/body·대상 PR·실행 범위, 공통 결과는 실제 commit/ref 또는 PR 식별자·URL·head/base·관측된 상태다. 첫 구현의 provider reference는 사용 가능한 인증된 CLI/API/connector의 **조회·생성·갱신·결과 확인 기능을 실제로 확인해서 선택**하도록 안내한다. 특정 GitHub/Gitea payload나 명령 옵션을 추측해 내장하지 않는다. 구체 provider 지원을 추가할 때 해당 설치 도구/공식 계약을 확인한다.

Draft 여부는 사용자 지정 → 저장소 관례 → 도구 기본 동작을 따르고 실제 상태를 보고한다. 자동 Draft·reviewer·label 정책은 넣지 않는다. 도구/권한이 없으면 제목·본문·대상·미완료 실행을 제공하되 실행 성공으로 보고하지 않는다. 다음 단계의 직접 PR 진행에 사용할 수 있어야 한다.

commit은 포함 범위와 SHA, push는 대상 remote ref, PR은 실제 조회 결과로 완료를 확인한다. timeout·응답 유실 시 mutation을 재전송하기 전에 이미 성공했는지 확인한다. 기존 동일 head/base PR은 재사용할 수 있는지 확인하며 사용자 요청 없는 본문 덮어쓰기를 하지 않는다. 성공 여부가 불명확한 동안 중복 commit/PR을 만들지 않는다. 실제 실패가 확인되고 같은 범위에서 해결 가능하면 해결·재시도하되 원인·권한이 바뀌는 경우 그 부분만 멈춘다.

중간 실패는 완료된 동작, 실패/미확인 동작, 보존된 변경, 다음 필요한 조치를 보고한다. 별도 ledger·승인 토큰·상태 전이 파일을 생성하지 않는다.

## 10. 테스트와 검증 계획

제품 개발의 검증 정책은 4.3~4.5절을 따른다. 아래는 **v3 Skill 자체의 초기 행동 평가 설계**다. Q01~Q24는 시나리오 카탈로그이고 전체를 상시 regression으로 만들지 않는다. 기존 02 문서의 반복 평가 제안은 이 선택적 평가 방안으로 구체화한다.

| ID | 재현 입력·초기 상태 | 기대 행동·실패 판정 | 고유 failure mode·필요성 | 기존 사례와 관계 / 종류 |
|---|---|---|---|---|
| B01 작은 변경 | 경계가 바뀌지 않는 UI 문구 1개 수정 요청 | 관련 수정·필요 확인 후 종료. 불필요한 Plan/Context·전체 조사·신규 테스트 의무화면 실패 | 작은 작업의 절차 과잉 | Q02·Q03을 한 사례로 대표 / behavior |
| B02 lifecycle·새 세션·Steps | 통제된 소형 저장소의 producer 상태가 DB·worker·UI에 전달됨. 분석·인계 후 새 세션에서 승인된 범위 구현·Steps 요청 | 실제 downstream과 상태 의미를 찾아 종료 근거 기록. 새 세션은 주요 결정·미확정 복구와 현재 상태 대조. 직접 파일만 수정·낡은 Context 고정·Steps 이유 창작이면 실패 | 경계 누락과 세션 간 의미 손실. Steps는 같은 변경의 설명 정확성을 검증 | Q08·Q11·Q14와 부분 중첩, lifecycle·인계는 신규 / 두 세션 behavior |
| B03 외부 관측·오래된 fixture | 조회 가능한 Browser/API 동작과 불일치하는 기존 fixture, 별도의 유효한 회귀 테스트 제공. 조회 전에는 실제 payload 미제공 | 관측·안정성 근거로 fixture/구현 중 잘못된 부분 판별. 실제값 추측 고정·오래된 기대값에 구현 맞춤·유효 회귀 삭제면 실패 | 외부 현실과 테스트가 충돌할 때의 판단 | Q04 확장; 관측·fixture 계약 판별은 신규 / behavior |
| B04 Plan Review | 같은 parser 실패를 여러 계층에서 반복하는 검사, 고유 DB 저장 검사, 근거 없는 abstraction과 가치 있는 경계 분리가 함께 있는 Plan | 중복만 줄이고 고유 검증·설계 가치는 보존. 테스트 수·파일 수만으로 삭제/추가하거나 검토를 자동 승인 gate로 만들면 실패 | Plan 단계의 중복 검증·과설계 판별 | 기존 Q에 없는 신규 관점 / behavior |
| B05 증거 재사용·무효화 | 실제 실행 근거와 동일 관련 코드/환경, commit으로 SHA만 달라진 상태. 이어 관련 설정이 변경된 상태 제공 | 처음은 관련 내용 동일성 확인 후 재사용, 다음은 영향받는 검증 재판단. 무조건 전체 재실행·무조건 재사용·허위 성공이면 실패 | 단계/SHA와 증거 유효성 혼동 | 신규 / 대비 조건 behavior |
| B06 PREPARE | 같은 파일 staged/unstaged와 무관 파일이 있는 저장소. commit 메시지와 PR 설명만 요청 | staged 대상과 전체 PR diff를 구분해 산출물 제공. index/HEAD/remote/PR mutation이면 실패 | 준비 요청의 실행 확대·변경 혼입 | Q15·Q16·Q20·Q22 대표 / behavior |
| B07 EXECUTE·응답 유실 | 확정 staged와 제외 unstaged. “commit” 후 별도 “PR 생성” 요청. 통제된 PR 도구가 생성 후 응답 유실 재현 | 첫 요청은 commit만. 다음은 필요한 일반 push·PR 생성/조회로 완료. 반복 승인·unstaged 혼입·먼저 push·중복 PR·성공 오보고면 실패 | 실행 권한 연결·부분 상태·중복 mutation | Q19·Q21 대표 / behavior + 로컬 Git integration |

9종 사용자 평가 후보를 7개 사례로 묶었다. B02의 downstream·인계, B03의 미관측 값·기존 fixture 충돌은 같은 원인 흐름을 공유한다. 단계별 관측과 실패 판정을 나누어 원인을 구분한다. **7개 사례가 7번의 모델 호출이라는 의미는 아니다.** B02는 새 세션, B05/B07은 대비 상태·후속 요청이 필요하다.

실행 방법과 한계:

- 첫 구현에서 `tests/behavior/cases.md`에 입력 저장소의 최소 내용·초기 Git 상태·사용자 요청·허용 도구·관측 항목·실패 판정을 재현 가능하게 작성한다. 위 fixture는 통제된 평가 자료이며 실제 Browser/provider 계약의 증거라고 주장하지 않는다.
- B02의 앱은 알려진 내부 계약을 가진 소형 평가 저장소다. B03은 실제 조회 가능한 로컬 Browser/API 환경을 관측하게 하고 초기 가짜 fixture는 의도적으로 잘못된 입력으로 명시한다. B07은 격리 로컬 Git/로컬 bare remote와 명시된 테스트 계약의 가짜 PR 도구를 사용한다. 실제 서비스에 push/PR하지 않는다.
- 평가는 요청된 GPT-5.6 Sol Medium, 평가 대상 v3 Skill과 필요한 도구만 노출한 환경에서 자연어 요청으로 시작한다. 실제 노출 경로/버전·모델·조건을 기록한다. v2 캐시를 섞지 않는다. 첫 대표 실행 뒤 실패·관련 변경이 있을 때 해당 사례만 다시 실행한다.
- 선택한 Skill과 선택 후 행동을 구분해 기록한다. 자연어 선택 실패를 본문 결함으로 단정하지 않고 필요한 경우만 명시 호출로 원인을 분리한다. 여러 모델 반복 실행을 기본으로 하지 않는다.
- 판정은 파일 diff·도구 호출·실제 Git/provider 상태·근거·요청 종료 지점이다. 정확한 출력 문구·Markdown heading·체크리스트 길이·질문 횟수 자체를 정답으로 고정하지 않는다.
- 순수 Markdown Skill에 1:1 Unit 테스트를 만들지 않는다. 기본 frontmatter·내부 참조·깨진 경로는 정적 검사로 확인한다. 실행 script를 나중에 추가할 때만 그 실제 로직에 필요한 Unit/integration을 검토한다.
- B07은 실제 GitHub/Gitea 통합 성공의 증거가 아니다. provider 실행 수단을 새로 도입·변경할 때 필요한 연결 검증을 선택한다. 일반 실행에서는 사용자가 요청한 실제 동작과 결과 확인을 증거로 삼고 별도 테스트 push/PR을 기본으로 생성하지 않는다. 추가 smoke가 필요하면 그 서비스 범위·권한을 해당 작업에서 확인한다.
- push-only, PR 갱신, 무관 staged 혼합, 외부 접근 불가 등 변형은 관련 동작 변경·실패가 있을 때 선택한다. 이 작은 세트가 모든 Git 경계·실패 분류를 검증했다고 주장하지 않는다.
- v2 pressure suite 전체 복원, 매번 전체 regression, 기능 없는 문구 검사, 같은 계약의 계층별 중복은 초기 계획에 포함하지 않는다.

현재 이 행동 평가를 실행하지 않았다. 문서 링크 검사와 설계 리뷰는 실제 Skill 동작 검증을 대신하지 않는다.

## 11. 첫 구현 범위와 남은 사용자 결정

**핵심 설계를 완성하기 위해 지금 반드시 필요한 추가 사용자 선택은 없다.** 7개 구성·이름·참조 배치·기본 문서 경로·독립 Skill 형태를 추천안으로 정했다. PREPARE/EXECUTE는 사용자 결정으로 확정됐다. ponytail 실물과 실제 provider/인증 정보는 이번 핵심 설계에서 제외하거나 실행 시 확인하는 항목이며 미결정 설계 목록으로 다시 넘기지 않는다.

다음 구현 범위는 다음과 같다.

1. 7절의 7개 Skill 본문과 역할별 reference를 작성한다. 독립 선택 경계·입출력·종료·H/D/P를 먼저 반영하고, 상세 사례는 필요할 때 읽게 한다.
2. task-planning·implementation-workflow·steps-documentation을 개편하고, preparing-commit→commit-workflow 및 pr-documentation→pr-workflow를 이동·확대한다. 분석·통합 검토 두 역할을 추가한다.
3. 루트 README의 역할·이름·사용 예를 갱신하고, 과거 분석의 원문 링크를 main 고정 SHA에 연결해 보존한다. 구/신 Skill 동시 노출을 기본 설치 방식으로 만들지 않는다. Plugin/캐시/marketplace는 이 단계에서 변경하지 않는다.
4. 평가 명세를 작성하고 frontmatter·참조/경로·변경 범위를 정적으로 확인한다. 실행 가능한 격리 환경에서 10절의 관련 핵심 행동 사례를 수행한다. 환경이 없으면 그 평가만 미실행으로 보고하고 성공을 가정하지 않는다.
5. 결과에 따라 관측된 실패를 좁게 수정하고 실제 변경·검증·제한을 보고한다. 변경된 Skill/사례와 무관한 전면 재실행은 하지 않는다.

이번 문서 작업의 종료점은 **구현할 책임·파일·정책·평가가 정의된 설계**다. 실제 Skill 작성은 다음 구현 작업에서 시작한다. 이 문서는 미래 Git 기능의 지원 계획이며 현재 branch/worktree 변경·commit·push·PR·플러그인 설치를 허가하지 않는다.

[v2-implementation]: https://github.com/yellow-pang/plans-steps-pr-skills/blob/eb70e3f72dcbe23bc76245e3b8ad12f841279154/plugins/plans-steps-pr-skills/skills/implementing-with-risk-checks/SKILL.md
[v2-verification]: https://github.com/yellow-pang/plans-steps-pr-skills/blob/eb70e3f72dcbe23bc76245e3b8ad12f841279154/plugins/plans-steps-pr-skills/skills/implementing-with-risk-checks/references/verification-policy.md
[v2-review]: https://github.com/yellow-pang/plans-steps-pr-skills/blob/eb70e3f72dcbe23bc76245e3b8ad12f841279154/plugins/plans-steps-pr-skills/skills/validating-pull-request/SKILL.md
