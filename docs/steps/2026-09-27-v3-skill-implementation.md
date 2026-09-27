# v3 Skill 구현 결과

기준: 2026-09-27, `feat/skill-v3-upgrade` 작업 트리. 이 문서는 실제 구현과 정적 확인 결과를 기록한다. Commit·Push·PR과 실서비스 Provider 실행은 하지 않았다.

## 배경과 변경 전 문제

main의 5개 독립 Skill은 Plan·구현·Steps·커밋 메시지·PR 설명을 맡았다. 명확한 직접 구현과 실제 diff 중심 검증은 이미 지원했지만, 긴 분석의 Context 인계, lifecycle 영향 종료 판단, 외부 관측과 오래된 fixture의 충돌 처리, 검증 재사용의 적용 조건, 실제 Commit/Push/PR 실행 역할은 부족했다. v2 Plugin 실험의 실패 원인은 확정되지 않았으므로 이 구현은 v2 상태 머신이나 승인 digest를 가져오지 않았다. 자세한 원문 비교는 [설계](../04-v3-upgrade-considerations.md)를 따른다.

## 실제 구성과 흐름

| main 역할 | v3 결과 | 주요 변화 |
|---|---|---|
| 없음 | `analyzing-work` 신설 | 구조·원인·lifecycle·영향 종료, 필요 시 Context 인계 |
| `task-planning` | 개편 | 현재 사실과 앞으로 할 변경을 분리하고 실제 대안·완료·검증을 설계 |
| 없음 | `reviewing-development-work` 신설 | 요청된 분석·Plan·구현 검토. 모든 작업의 Router는 아님 |
| `implementation-workflow` | 개편 | 넓은 영향 조사 후 필요한 범위 수정, 관측·테스트 유효성·증거 재사용 |
| `steps-documentation` | 개편 | 실제 배경·이유·전후 흐름·검증·제한 설명 |
| `preparing-commit` | `commit-workflow`로 이동·개편 | 메시지/단위 준비와 명시된 Commit·Push 실행 구분 |
| `pr-documentation` | `pr-workflow`로 이동·개편 | 전체 PR diff 기반 설명과 명시된 생성·갱신 실행 구분 |

각 Skill은 독립 선택·사용을 전제로 한다. Analysis는 현재 참인 것, Plan은 앞으로 할 것, Steps는 실제로 달라진 것을 다룬다. 긴 작업의 Context는 명령 일지가 아니라 중요한 요구·구조·결정·미확정의 인계 기록이며 작은 작업에 강제하지 않는다. Review는 검토 의도나 구체 위험이 있을 때만 적용한다.

구현 Skill은 데이터·상태·API·DB·worker·async·Browser/provider·UI 경계를 넘는 변경에서 producer/consumer와 상태 전이를 확인하고 영향 종료 근거를 찾는다. 조회 가능한 외부 동작은 관측 후 계약화한다. 기존 테스트는 유효한 동작을 보호하는지 판단하며, 새 테스트는 가능한 한 고유 failure mode를 겨냥한다. 기존 검증의 관련 내용·환경·근거가 유효하면 재사용하고 달라진 부분만 다시 확인한다.

Git 두 Skill은 PREPARE에서 index·HEAD·remote·PR을 변경하지 않는다. EXECUTE는 사용자가 명시한 완료 지점까지만 다룬다. Commit은 자동 Push/PR이 아니고, PR 생성도 미커밋 변경의 자동 Commit이 아니다. 응답 유실 시 상태 조회로 중복 실행을 피하도록 작성했다. 특정 Provider의 미확인 API 형식은 내장하지 않았다.

## 파일과 평가 명세

7개 `skills/*/SKILL.md`와 역할별 reference 5개를 작성했다. 옛 `preparing-commit`, `pr-documentation` 경로는 제거했다. 루트 README에 역할과 이름 대응을 추가했고, 과거 main 분석 문서의 원문 링크는 고정 SHA URL로 바꿔 현행 Skill과 구별했다. [B01~B07 평가 명세](../../tests/behavior/cases.md)는 작은 변경, lifecycle·인계·Steps, 외부 관측, Plan 검토, 검증 재사용, PREPARE, EXECUTE·응답 유실의 고유 실패를 다룬다. 기존 자동 테스트를 수정·삭제하지 않았고, Skill 파일별 문구 검사는 추가하지 않았다.

## 검증과 한계

`skill-creator`의 `quick_validate.py`는 현재 Python 환경에 `yaml` 모듈이 없어 시작되지 못했다. 별도 읽기 전용 검사로 Skill 7개 이름·frontmatter 필수 필드, role-local reference와 Markdown 상대 링크를 확인했다. `git diff --check`로 추적 파일의 공백 오류를 확인했다.

| 검사 | 결과 |
|---|---|
| `quick_validate.py` | 실패: 시작 시 `ModuleNotFoundError: yaml` |
| 자체 구조·링크 검사 | 통과: 7개 Skill frontmatter, 자체 reference, Markdown 상대 링크 52개 |
| `git diff --check` | 통과: 추적 파일의 공백 오류 없음 |
| B01~B07 실제 모델 행동 | 미실행. 격리된 GPT-5.6 Sol Medium 평가 환경이 현재 없음 |
| 실제 GitHub/Gitea Provider 통합 | 미실행. 이번 작업 범위에 실제 Push/PR 없음 |

현재 변경은 Skill 소스와 문서에 한정된다. 실제 자동 선택률과 EXECUTE 복구 품질은 명세만으로 입증되지 않는다. 사용자 검토 후 별도 격리 환경에서 관련 행동 사례를 실행하고 관측된 실패만 좁게 수정하는 것이 다음 단계다.
