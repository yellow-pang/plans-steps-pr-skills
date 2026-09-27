# pr-documentation 분석

> 분석 기준: `main`과 동일한 `d7c0887`의 원문. 실제 모델 실행 시험이 아닌 정적 분석이다.
> 이 문서의 “강제”는 프롬프트에 적힌 요구·금지를 뜻한다. 이를 집행하는 스크립트나 자동 gate는 없다.
> 아래 금지는 이 스킬의 기본 역할 계약이며, 상위 지침이나 명시적 사용자 지시보다 우선하는 권한 장벽이라는 뜻은 아니다.

## 1. 역할과 구성

`pr-documentation`은 현재 변경을 리뷰할 수 있도록 배경, 영향, 검증, 리뷰 포인트를 설명하는 스킬이다.
실제 Pull Request 생성·게시·병합을 수행하는 스킬은 아니다.
구성 파일은 [`SKILL.md`](https://github.com/yellow-pang/plans-steps-pr-skills/blob/d7c0887e8d8fe2a4ca847c821a46f85bfba88e7a/skills/pr-documentation/SKILL.md) 하나이며 별도 템플릿, 스크립트, 에이전트 설정은 없다.

| 구간 | 내용 | 기능 |
| --- | --- | --- |
| Frontmatter | 명시적인 PR 문서·설명 작성 요청 | 자동 후속 선택 범위를 제한 |
| 핵심 원칙 | 실제 변경 우선, Plan·Steps 없이 진행 | 리뷰 설명의 근거와 독립성 확보 |
| 사전 확인 | PR 전체 diff와 working tree 구분 | 커밋된 변경 누락과 미포함 변경 혼입 방지 |
| 문서 위치와 언어 | 저장소 관례, 파일 작성 요청 | 응답과 저장소 문서의 분기 |
| 문서 내용 | 배경, 영향, 흐름, 검증, 리뷰 포인트 | 리뷰어 관점의 정보 구성 |
| 금지 사항 | 허위 검증, 무관한 변경, Git·PR 조작 금지 | 설명 작성 책임으로 범위 제한 |

## 2. 선택 조건과 간단 요청 감지

[description](https://github.com/yellow-pang/plans-steps-pr-skills/blob/d7c0887e8d8fe2a4ca847c821a46f85bfba88e7a/skills/pr-documentation/SKILL.md)은 PR 문서나 설명 작성을 “명시적으로 요청”해야 한다고 정한다.
`preparing-commit`의 “유용한 경우”, `steps-documentation`의 “장기 기록 필요” 같은 선제 선택 조건은 없다.
“PR 설명 써줘”는 짧아도 목적이 분명하고, 일반적인 “정리해줘”는 이 스킬의 직접 단서가 약하다.

이는 불필요한 PR 문서 자동 생성을 억제하는 방향이다.
다만 “PR 만들어줘”는 설명 작성과 실제 PR 생성의 구분이 없어 선택 단계에서 해석 문제가 생길 수 있다.
본문은 실제 PR 생성을 기본 역할에서 제외하며, 실행 요청의 담당자나 인계 절차는 정의하지 않는다.

## 3. 입력·산출물·절차

입력은 현재 변경의 실제 코드·설정·검증 결과, Git diff, 기준 브랜치, 기존 PR 형식이다.
Plan·Steps는 있으면 대조하지만 필수 선행 자료는 아니다.
산출물은 응답으로 제공하는 PR 설명 또는 사용자가 파일 작성을 요청한 경우의 저장소 문서다.

1. 저장소 지침과 기존 PR 형식을 확인한다.
2. 기준 브랜치와 비교 가능하면 커밋된 변경을 포함한 전체 PR diff를 확인한다.
3. staged, unstaged, untracked 변경은 PR diff와 별도로 구분한다.
4. 변경 파일, 계약, 설정, 테스트, 알려진 제한을 확인한다.
5. 관련 Plan·Steps가 있으면 실제 변경과 대조한다.
6. 변경 배경, 주요 영향, 검증, 리뷰 포인트와 제한을 작성한다.
7. 기준이나 범위가 불명확하면 확인 가능한 범위의 초안과 그 한계를 명시한다.

파일 위치는 저장소 지침 → 기존 문서 관례 → `docs/pr/` 순으로 결정한다.
언어는 사용자 요청이 우선이며 없으면 기존 PR 또는 문서 언어를 따른다.
PR 설명만 요청했으면 응답으로 제공하고, 파일 작성 요청이 있을 때만 저장소에 쓴다.
근거: [사전 확인](https://github.com/yellow-pang/plans-steps-pr-skills/blob/d7c0887e8d8fe2a4ca847c821a46f85bfba88e7a/skills/pr-documentation/SKILL.md#사전-확인), [문서 위치와 언어](https://github.com/yellow-pang/plans-steps-pr-skills/blob/d7c0887e8d8fe2a4ca847c821a46f85bfba88e7a/skills/pr-documentation/SKILL.md#문서-위치와-언어).

## 4. 강제성 평가

| 수준 | 원문 요구 | 평가 |
| --- | --- | --- |
| 필수 | 실제 코드·설정·결과·diff 기준 | 문서보다 구현을 우선한다. |
| 조건부 필수 | 기준과 비교 가능하면 전체 PR diff 확인 | working tree만 보고 커밋된 변경을 놓치는 문제를 줄인다. |
| 필수 | working tree 상태 별도 구분 | 아직 PR에 들어가지 않은 변경의 혼입을 억제한다. |
| 조건부 필수 | 범위 불명확 시 제한을 밝힌 초안 | 정보 부족을 무조건 중단 사유로 삼지 않는다. |
| 조건부 필수 | 파일 작성 요청 시에만 파일 수정 | 응답 생성과 저장소 변경 권한을 구분한다. |
| 필수 금지 | 미실행 검증 성공, 근거 없는 효과·성능 개선 주장 | 리뷰어에게 잘못된 확신을 주는 설명을 제한한다. |
| 필수 금지 | add, commit, push, PR 생성, reviewer 지정, merge | 외부 게시와 Git 조작을 명확히 제외한다. |
| 판단 영역 | PR 범위, 알려진 제한, 리뷰 집중점, 항목 분량 | 선택 기준·축약 예시가 없어 작성 편차가 남는다. |

“영향받지 않는 범위”도 근거가 있을 때만 쓰도록 하여 무영향 주장의 부담을 분명히 한다.
검증 실행 자체나 새 테스트 작성은 의무화하지 않으며, 실행 기록으로 확인한 결과를 문서화한다.
Steps와 달리 “작업 규모에 맞게”라는 분량 조정 문구가 없어 작은 변경에도 항목을 전부 펼칠 위험이 있다.
근거: [문서 내용](https://github.com/yellow-pang/plans-steps-pr-skills/blob/d7c0887e8d8fe2a4ca847c821a46f85bfba88e7a/skills/pr-documentation/SKILL.md#문서-내용), [금지 사항](https://github.com/yellow-pang/plans-steps-pr-skills/blob/d7c0887e8d8fe2a4ca847c821a46f85bfba88e7a/skills/pr-documentation/SKILL.md#금지-사항).

## 5. 짧은 요청 시나리오 평가

다음은 문구와 절차로 예상한 경로이며, 재현 시험 결과나 성공률이 아니다.

| 요청과 상태 | 예상 경로 | 판단·한계 |
| --- | --- | --- |
| “PR 설명 써줘.” / 기준 브랜치 확인 가능 | 전체 PR diff를 읽고 응답으로 설명 | 명시 단서가 강하며 파일을 만들 이유는 없다. |
| “docs/pr/login.md로 PR 문서 만들어줘.” | 범위·근거 확인 후 지정 파일 작성 | 파일 요청과 경로가 명확하다. |
| “오타 수정 PR 설명 두 줄만.” | 실제 변경에 맞춰 짧은 설명 작성 가능 | 요청은 명확하지만 고정 항목 목록과 축약 기준이 긴장한다. |
| “PR 만들어줘.” | 설명 작성인지 실제 생성인지 해석 필요 | 기본 역할은 생성 제외이며, 실행 요청에 대한 인계 절차가 없다. |
| “PR 설명 정리해줘.” / 기준 브랜치 불명확 | 확인 가능한 범위의 초안과 제한 작성 | 정보가 부족해도 진행하는 분기가 명시되어 있다. |

명시적인 설명 작성 요청에는 잘 대응할 것으로 예상된다.
그러나 짧은 실행형 표현과 작은 변경의 분량 요구에는 추가적인 경계 예시가 유용하다.

## 6. 다른 스킬과의 경계

[`steps-documentation`](https://github.com/yellow-pang/plans-steps-pr-skills/blob/d7c0887e8d8fe2a4ca847c821a46f85bfba88e7a/skills/steps-documentation/SKILL.md)은 완료 결과의 장기 기록이고, 이 스킬은 리뷰어를 위한 변경 설명이다.
목적·변경·검증이 겹치지만 PR에는 리뷰 집중점과 배포 고려사항이 추가된다.
Steps가 있더라도 그대로 신뢰하는 대신 실제 변경과 대조하고, 없어도 작성한다.

[`task-planning`](https://github.com/yellow-pang/plans-steps-pr-skills/blob/d7c0887e8d8fe2a4ca847c821a46f85bfba88e7a/skills/task-planning/SKILL.md)의 계획은 선택적 비교 자료다.
[`preparing-commit`](https://github.com/yellow-pang/plans-steps-pr-skills/blob/d7c0887e8d8fe2a4ca847c821a46f85bfba88e7a/skills/preparing-commit/SKILL.md)은 현재 커밋 후보를 다루며, PR 설명은 기준 브랜치 대비 전체 변경을 다룬다.
따라서 커밋 메시지를 PR 설명으로 대체하거나 staged diff만으로 PR 전체를 설명해서는 안 된다.
[`implementation-workflow`](https://github.com/yellow-pang/plans-steps-pr-skills/blob/d7c0887e8d8fe2a4ca847c821a46f85bfba88e7a/skills/implementation-workflow/SKILL.md#금지-사항)는 후속 스킬을 강제하지 않으므로 구현 완료가 자동 PR 설명 작성으로 이어지지 않는다.

명시 PR 문서 요청이라는 선택 조건과 파일 작성 요청이라는 저장 조건은 별개의 안전장치다.
두 조건을 하나로 취급하면 단순 설명 요청에 불필요한 파일이 생길 수 있다.

## 7. 유지 가치와 v3 개선 후보

**유지할 가치가 큰 부분**은 전체 PR 범위 확인, working tree 분리, 근거 없는 영향·성능 주장 금지다.
기준이 불명확해도 한계를 명시한 초안을 제공하는 분기는 간단한 요청의 진행성을 높인다.

| 개선 후보 | 이유 | 확인할 수용 기준 |
| --- | --- | --- |
| “PR 설명”과 “PR 생성” 선택 예시 | 짧은 생성형 표현의 의미 차이를 줄인다. | 실제 게시 요청을 설명 작성만으로 완료 처리하지 않는다. |
| 소규모 PR용 최소 형식 | 단순 변경에 과한 보고서를 만들지 않는다. | 한두 문장 배경·결과와 필요한 검증으로 충분히 작성한다. |
| 기준 브랜치·비교 범위 판단 절차 | 서로 다른 diff 해석으로 범위가 달라지는 문제를 줄인다. | 사용한 기준과 포함 범위를 확인할 수 있다. |
| 미커밋 변경 처리 예시 | 현재 작업과 실제 PR 포함 범위의 혼동을 줄인다. | 포함 예정과 이미 포함된 변경을 명확히 구분한다. |
| 응답·파일·게시 산출물 구분 | 문서 작성 조건과 실행 권한을 분리한다. | 설명 요청에 파일 또는 PR을 임의 생성하지 않는다. |

종합하면 명시 요청 감지와 근거 중심 설명은 탄탄하며 파일 쓰기·게시 경계도 분명하다.
v3에서는 작은 PR의 분량 조정과 “만들어줘” 같은 표현의 분기를 먼저 보완할 가치가 있다.
