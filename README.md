# plans-steps-pr-skills

개발 작업을 분석, 계획, 검토, 구현, 기록하고 Git 작업을 준비하거나 요청된 범위에서 실행하는 독립 Agent Skills 7개입니다. 각 Skill은 따로 사용할 수 있습니다. 작은 수정에 전체 순서를 강제하지 않습니다.

| Skill | 사용 시점 |
|---|---|
| [analyzing-work](skills/analyzing-work/SKILL.md) | 구조·원인·lifecycle·영향 조사, 긴 작업의 Context 인계 |
| [task-planning](skills/task-planning/SKILL.md) | 앞으로 할 변경·대안·완료·검증 계획 |
| [reviewing-development-work](skills/reviewing-development-work/SKILL.md) | 분석·Plan·실제 구현의 근거 기반 검토 |
| [implementation-workflow](skills/implementation-workflow/SKILL.md) | 명확한 요청이나 Plan의 실제 구현·필요 검증 |
| [steps-documentation](skills/steps-documentation/SKILL.md) | 실제 변경 이유·전후 흐름·검증·제한 기록 |
| [commit-workflow](skills/commit-workflow/SKILL.md) | Commit/Push 준비 또는 명시된 실행 |
| [pr-workflow](skills/pr-workflow/SKILL.md) | PR 설명 준비 또는 명시된 생성·갱신 |

`preparing-commit`은 `commit-workflow`, `pr-documentation`은 `pr-workflow`로 개편했습니다. 옛 이름의 Skill은 함께 제공하지 않습니다. 메시지·설명만 요청하면 준비 자료만 만들며 Git/PR 상태를 바꾸지 않습니다. Commit·Push·PR 실행은 각각 명시된 요청 범위에서 수행합니다.

배경과 설계는 [기존 Skill 분석](docs/README.md)과 [v3 구체 설계](docs/04-v3-upgrade-considerations.md)에, 초기 행동 평가 명세는 [B01~B07](tests/behavior/cases.md)에 있습니다. 분석 문서의 과거 main 원문 링크는 고정 SHA를 가리킵니다.

첫 구현 `e8e9328`과 이후 설명 품질·메시지 처리 보완의 차이는 [재검토와 전후 비교](docs/steps/2026-09-27-v3-skill-review.md)에서 확인할 수 있습니다. 정적 검사와 실제 모델 행동 평가의 결과는 구분해 기록합니다.

현재 사용자 지정 행동 평가 대상은 GPT-6 Sol Medium입니다. [실제 행동 평가](tests/behavior/runs/2026-09-27-gpt-6-sol-medium.md)에서 B01–B07 대표 사례와 v3 Skill 7개의 격리 자연어 선택을 실행했고, B04 보완과 실제 플러그인·실서비스의 미검증 범위를 함께 기록했습니다.
