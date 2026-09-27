# v3 스킬 업그레이드 중간 인계

기록 기준: 아래 본문은 2026-09-27의 설계 완료 시점 인계 스냅샷이다. **현재는 v3 첫 구현 `e8e9328`과 재검토 보완 `24205fe`를 커밋한 단계다.** 현재 상태는 실제 Git 상태와 [재검토·전후 비교](../steps/2026-09-27-v3-skill-review.md)가 우선한다. 재개 시 이 문서 아래의 “구현 전” 작업 목록을 다시 실행하지 않는다. 평가 대상은 사용자 요청으로 GPT-6 Sol Medium으로 바뀌었다. CLI 업데이트 후 [실제 행동 평가](../../tests/behavior/runs/2026-09-27-gpt-6-sol-medium.md)에서 B01·B02·B06을 실행했고 나머지는 아직 미검증이다.

## 1. 현재 요청과 완료 지점

기존 5개 Skill 분석·문서화와 최초 인계는 커밋 완료됐다. 이후 실제 개발 workflow 요구를 문서에 반영했고, 준비도가 충분하다는 검토를 거쳐 이번에는 **역할·입출력·진입/종료·인계·공통 원칙·Context·Git 실행·평가·첫 구현 범위**를 구체화했다.

이번에 추가로 확정된 사용자 결정은 **Commit·Push·PR의 PREPARE/EXECUTE 지원**이다. 메시지/설명 요청과 실제 실행 요청을 구분한다. 설계자가 합리적으로 정할 구조·이름·파일 배치를 더 이상 전부 사용자 미결정으로 남기지 말라는 요청도 반영했다.

원본 요구는 2026-09-27의 두 첨부문이다. 최초 workflow는 `da4cdaa9-807c-46e4-a843-d26f83d4e8a6`, 후속 구체 설계는 `a351945f-d3e2-4aba-9575-a7291730b687` 아래의 `붙여넣은 텍스트.txt`다. 전체 로컬 경로와 상세 내용은 [04 구체 설계](../04-v3-upgrade-considerations.md)에 기록했다.

현재 범위:

- 실제 `SKILL.md`·Plugin·캐시를 변경하지 않는다. 현재 존재하는 Skill은 여전히 main의 5개다.
- 기존 branch/worktree와 기존 미커밋 문서 변경을 유지한다. 새 branch/worktree·commit·push·PR을 만들지 않는다.
- 기존 main/v2 사실 분석을 보존하고, 사용자 확정 요구와 추천 설계를 구별한다.
- 새 설계 문서를 늘리지 않고 04에 상세 설계를 통합한다. 이 문서는 재개에 필요한 결정과 근거만 남긴다.

## 2. Git 스냅샷과 이력

| 항목 | 이번 구체 설계 시작 시 확인값 |
|---|---|
| 경로·셸 | `C:/Dev/plans-steps-pr-skills`, PowerShell |
| 작업 branch | `feat/skill-v3-upgrade` |
| HEAD / 최초 인계 커밋 | `53da0de4951d990895b3eb2eebea4e9786be77b3` |
| 기존 분석 커밋 | `44f58614f3387ac328c78c052e8ca8421f083148` |
| main / 원문 기준 | `d7c0887e8d8fe2a4ca847c821a46f85bfba88e7a` |
| 보존할 v2 | `feature/gated-development-v2` / `eb70e3f72dcbe23bc76245e3b8ad12f841279154` |
| 로컬 origin/feat/skill-v3-upgrade | `44f58614f3387ac328c78c052e8ca8421f083148`, HEAD가 1커밋 앞섬 |
| 시작 working tree | 이전 요구 반영의 문서 4개가 이미 수정됨: 04·docs README·handoff·구현 Skill 분석 |
| 이번 문서 범위 | 위 4개를 이어서 갱신하고 02의 향후 평가 절에 현재 카탈로그 방침을 연결 |

로컬 참조만 조회했고 fetch·원격 조회는 하지 않았다. 이전 요구 반영 시작 때 clean이었다는 기록과 현재 시작 상태를 혼동하지 않는다. 최초 인계 작성 시 HEAD `44f5861`·ahead/behind 0/0, 이후 사용자 요청으로 인계가 `53da0de`에 커밋됐다. 이번 두 문서 갱신 단계는 커밋하지 않았다.

최종 조회에서는 로컬 `origin/feat/skill-v3-upgrade`도 `53da0de`로 바뀌어 ahead/behind가 `0 / 0`이었다. 위 표의 시작값과 구분한다. 이 작업에서는 push/fetch를 실행하지 않았으며 참조가 바뀐 경위는 추정하지 않는다.

원래 분석 커밋은 `docs/` 10개·996줄 추가, 인계 커밋은 handoff와 목차 연결이다. 현재 `skills/` 5개와 루트 README·LICENSE가 main과 동일함을 다시 확인했다.

## 3. 다음 구현에 사용할 추천 구조

추천안은 **독립 Skill 7개**다. 새 역할 두 개는 반복되는 독립 분석·검토 요청에서 도출했다. 개수 자체가 사용자 지정은 아니며 아래 구조가 이번 설계 결과다.

| 추천 Skill | 핵심 책임·종료 지점 | 현재 소스와의 관계 |
|---|---|---|
| analyzing-work | 요구·구조·lifecycle·영향 조사, 필요 시 Context. 근거 있는 결론/미확정과 인계에서 종료 | 신규 |
| task-planning | 앞으로 할 변경·대안·완료·검증 계획. Plan-only면 종료, 이미 구현까지 요청됐으면 해당 범위 진행 | 기존 개편 |
| reviewing-development-work | 분석·Plan·실제 구현 세 대상의 근거 기반 검토. 문제·영향·필요 조치·한계 보고 | 신규; Plan Review만 따로 분리하지 않음 |
| implementation-workflow | 명확한 요청/Plan의 실제 수정·필요 검증·완료 보고 | 기존 개편; 자체 조사와 직접 구현 유지 |
| steps-documentation | 실제 배경·문제·변경 이유·전후 구조/흐름·검증·제한 설명 | 책임 유지·보강 |
| commit-workflow | Commit/Push PREPARE 또는 요청된 EXECUTE의 실제 결과 확인 | preparing-commit에서 이동·확대 |
| pr-workflow | PR 제목/본문 PREPARE 또는 생성/갱신 EXECUTE | pr-documentation에서 이동·확대 |

정확한 책임·진입·입출력·종료·인계·H/D/P는 [04의 5절](../04-v3-upgrade-considerations.md#5-제안하는-v3-skill-구조와-인계), 원문 대비 근거는 [6절](../04-v3-upgrade-considerations.md#6-현재-main의-5개-skill-변경-매핑)에 있다.

공통 router·상태 머신·Plan digest·별도 Context Skill을 추가하지 않는다. 각 Skill의 짧은 핵심과 **자기 폴더 안 reference**로 독립 설치를 보존한다. sibling Skill·저장소 루트 정책 파일 의존이나 원칙 복제 생성기를 도입하지 않는다. 파일 목록은 [7절](../04-v3-upgrade-considerations.md#7-공통-원칙-배치와-최초-파일-구성)에 있다.

## 4. 반드시 이어받을 동작 결정

- **Superpowers 비사용**, Superpowers·Spec Kit·BMAD는 참고 자료. 주 환경은 **GPT-5.6 Sol Medium**이며 실제 성능은 아직 검증하지 않았다.
- 분석은 관련 데이터·상태·API·DB·async·Browser/provider·event·consumer·UI 경계를 추적하고, 관련 producer/consumer·상태 전이·추가 영향이 닫혔다는 근거에서 멈춘다. 항상 저장소 전체를 조사하지 않는다.
- `최소 변경/최소 수정` 문구는 “영향을 먼저 확인하고, 요구와 확인된 영향을 해결할 만큼 수정하며 무관 변경은 배제”로 대체한다.
- 현재 상태는 코드/runtime/관측으로 확인한다. 최신 사용자 요구·합의된 계약은 원하는 동작을 정의한다. 기존 버그나 낡은 Context를 최신 요구보다 우선하지 않는다.
- Observe before encode: 관측 → 의미/안정성 판단 → 필요한 구현/계약화. 미관측은 가정, 합성 오류는 시뮬레이션으로 구분한다. 내부 로직·확인된 계약의 mock/TDD는 허용한다.
- 테스트는 유효한 동작을 보호한다. 기존 기대값을 수정/제거하려면 요구·runtime·유효 계약과의 불일치 및 남는 보호 범위를 설명한다. GREEN 목적만으로 유효 검증을 없애지 않는다.
- 새 테스트는 고유 실패 보호로 판단한다. 다른 경계를 보호하는 중첩은 허용한다. 파일/class 수나 테스트 수로 품질을 판정하지 않는다.
- 검증은 관련 내용·dependency/config·환경·입력·위험·실행 근거가 유효하면 재사용한다. HEAD만 같다고 충분하지 않고 commit으로 SHA만 달라져도 관련 내용이 같으면 재사용할 수 있다.
- Plan/검토에서 abstraction·validation/state/metadata·coupling·유지보수·합리적 확장을 본다. 규모와 관련될 때만 시간·공간·IO·Browser·concurrency 비용을 본다.
- H는 사실성·권한·변경 보존, D는 상황 판단, P는 편의 절차다. 문서·독립 검토·메시지 사전 확인을 모든 작업의 선행 gate로 만들지 않는다.
- “분석만/계획만/검토만”은 그 산출물에서 끝난다. 이미 구현까지 요청됐으면 같은 승인 재질문 없이 이어간다. 새 제품 의미·범위·외부 영향의 실제 선택만 확인한다.

### Context와 Steps

Context는 긴 조사·여러 경계/세션 또는 명시 인계 요청에서 필요한 지식이 누적될 때 선택적으로 만든다. 기본 생성 책임은 분석 역할, 이후 갱신은 중요한 사실/결정을 바꾼 현재 역할이다. 기본 경로는 사용자/저장소 관례가 없을 때 `docs/context/<task-slug>.md`다.

명령 일지와 파일 열람 목록을 남기지 않는다. 완료·취소 시 중요한 지속 결정은 Steps/기존 문서와 연결하고 Context를 동결하며 자동 삭제하지 않는다. 새 세션은 Context에서 복구한 뒤 실제 코드·환경·증거를 확인하고 바뀐 부분만 조사한다. 읽기 전용이면 응답 인계로 대체한다. 자세한 lifecycle은 [8절](../04-v3-upgrade-considerations.md#8-context-lifecycle과-plansteps-연결)에 있다.

Plan은 앞으로 할 일, Steps는 실제로 달라진 결과다. Steps의 배경·문제·이유·흐름·검증 설명은 main에도 이미 있는 책임이며 v3에서 전후 비교·필요한 표/Mermaid를 보강한다. 짧은 로그를 새 보고서로 전환했다고 과거 역할을 왜곡하지 않는다.

### PREPARE / EXECUTE

PREPARE는 산출물만 준비하고 index·HEAD·remote·PR을 바꾸지 않는다. EXECUTE는 명시 요청·현재 권한·확정 범위에서만 수행한다.

- Commit 요청: 필요한 선택 staging과 commit까지. Push/PR은 자동 포함하지 않는다.
- Push 요청: 기존 commit의 확인된 remote/ref push까지. 미커밋 변경 commit은 포함하지 않는다.
- PR 생성 요청: 확정된 committed head의 필요한 일반 push와 PR 생성/조회. 미커밋 변경·무관 commit을 임의 포함하지 않는다.
- 지정 PR 설명 갱신: 요청된 title/body 갱신까지. reviewer·merge 등을 추가하지 않는다.
- 이미 전체 실행을 요청했다면 단계마다 같은 권한을 다시 묻지 않는다.
- staged/unstaged/untracked와 같은 파일의 hunk를 구분해 기존 index·제외 변경을 보존한다.
- timeout 후 실제 상태를 먼저 확인하고 중복 commit/PR을 만들지 않는다. 부분 실패는 완료·실패/미확인·보존 상태·다음 조치를 보고한다.

GitHub/Gitea에 구조를 고정하지 않는다. 실제 사용 가능한 CLI/API/connector 기능을 확인해 선택하고 첫 구현에 SDK/adapter registry를 만들지 않는다. 지원 도구가 없으면 완성한 준비 자료와 미완료 실행을 남긴다. 상세 권한·실행 계약은 [9절](../04-v3-upgrade-considerations.md#9-prepare--execute와-provider-경계)에 있다.

## 5. 원문 사실과 미확인 자료

main은 독립 Skill 5개이고 강제 전체 파이프라인이 아니다. Plan 없는 명확한 구현, 실제 diff·실행 근거, 사용자 변경 보존, staged/unstaged/untracked 구별, 파일 요청/응답 구별이 기존 강점이다.

main 구현 원문 24·30행에 최소 수정, 28행에 producer/consumer 확인이 함께 있다. main에 TDD/mock/fixture 강제나 commit/PR마다 전체 검증 반복 규칙은 없다. v2는 선행 RED와 correct test 보호뿐 아니라 같은 HEAD·환경·입력의 근거 재사용을 이미 지원하며, PR 검토에서 lifecycle도 확인한다. 이번 요구를 그 규칙이 과거 문제를 실제 유발했다는 원인 증거로 바꾸지 않는다.

**ponytail은 미확인으로 이번 핵심 설계/첫 구현에서 제외한다.** 이전 단계에서 worktree의 숨김·ignore 포함 파일/본문(.git 제외), tracked/untracked/ignored, main·v2·HEAD에서 실물을 발견하지 못했다. 전역 설치·다른 프로젝트는 조사하지 않았다. 지금 검색되는 설계 문서의 이름 언급은 구현 발견이 아니다.

현재 설치 v2 계열 위치는 다음과 같으며 main 소스와 별개다.

```text
C:/Users/bigbros/.codex/plugins/cache/yellow-pang-workflows/plans-steps-pr-skills/2.0.0/skills
```

v2의 과거 explicit GREEN / implicit RED / clean profile BLOCKED_AUTH(행동 호출 0) 기록은 [03 문서](../03-v2-context.md)를 따른다. 실패 원인은 Plugin·모델·Skill 경쟁·환경으로 분리되지 않았고 현재 캐시/v2 전체 해시 일치도 확인하지 않았다. v2 재실험·복구·병합·재설치는 현재 요청이 아니다.

## 6. 남은 사용자 결정과 다음 구현 작업

**현재 핵심 설계에 반드시 필요한 추가 사용자 선택은 없다.** 파일 위치·이름·7개 구성·Plan/Review 분리·공통 원칙 배치는 추천안으로 정했고 PREPARE/EXECUTE는 사용자가 확정했다. 실제 구현 요청을 받으면 이 기준으로 진행할 수 있다. 현재 설계 요청을 구현 허가로 바꾸지 않는다.

다음 구현 시 필요한 순서:

1. 현재 Git 상태와 미커밋 문서를 확인하고 보존한다. 04의 5~11절과 수정할 main 원문만 읽는다.
2. 신규 분석/검토, 기존 Plan/구현/Steps 개편, Git 두 Skill 이동·확대를 수행한다. 각 본문의 핵심과 7절 reference를 작성한다.
3. 루트 README의 역할·이름 안내와 역사 분석의 고정 SHA 원문 링크를 갱신한다. 구/신 이름의 이중 Skill alias를 만들지 않는다.
4. `tests/behavior/cases.md`로 초기 행동 사례를 재현 가능한 입력·기대 행동·실패 판정까지 구체화하고 정적 검사를 한다.
5. 격리된 대상 환경에서 관련 행동 사례를 실행해 실제 결과만 보고한다. Plugin 설치·provider 실서비스 실행·commit/push/PR은 그 시점 사용자 요청과 환경 권한에 따라 별도로 판단한다.

먼저 읽을 원문은 [Plan](https://github.com/yellow-pang/plans-steps-pr-skills/blob/d7c0887e8d8fe2a4ca847c821a46f85bfba88e7a/skills/task-planning/SKILL.md), [구현](https://github.com/yellow-pang/plans-steps-pr-skills/blob/d7c0887e8d8fe2a4ca847c821a46f85bfba88e7a/skills/implementation-workflow/SKILL.md), [Steps](https://github.com/yellow-pang/plans-steps-pr-skills/blob/d7c0887e8d8fe2a4ca847c821a46f85bfba88e7a/skills/steps-documentation/SKILL.md), [커밋 준비](https://github.com/yellow-pang/plans-steps-pr-skills/blob/d7c0887e8d8fe2a4ca847c821a46f85bfba88e7a/skills/preparing-commit/SKILL.md), [PR 설명](https://github.com/yellow-pang/plans-steps-pr-skills/blob/d7c0887e8d8fe2a4ca847c821a46f85bfba88e7a/skills/pr-documentation/SKILL.md)이다. 적용 가능한 저장소 지침을 다시 확인한다. 이번에는 상위·루트·하위에서 AGENTS.md가 발견되지 않았다.

## 7. 검증 계획과 실제 검증 이력

초기 행동 평가는 B01 작은 변경, B02 lifecycle·새 세션·Steps, B03 외부 관측·잘못된 fixture, B04 Plan 중복/복잡도 검토, B05 증거 재사용/무효화, B06 PREPARE, B07 EXECUTE·응답 유실의 7개다. 입력·고유 실패·기존 Q와의 관계·종류는 [10절](../04-v3-upgrade-considerations.md#10-테스트와-검증-계획)에 있다. Q01~Q24는 카탈로그이며 전체 상시 regression이 아니다.

자연어 선택과 선택 후 행동을 구분한다. 대상은 GPT-5.6 Sol Medium, 실제 노출된 v3 버전·경로를 확인하고 v2를 섞지 않는다. 7개 사례는 호출 7회를 뜻하지 않는다. 새 세션·후속 요청이 필요한 사례는 해당 의미를 평가한다. 통제된 fixture/provider 도구 결과를 실서비스 계약·통합 성공으로 보고하지 않는다.

과거 검증 이력:

- 최초 분석: 문서 10개, 내부 링크·앵커 105개, 고정 SHA 경로 23개 확인.
- 최초 handoff 추가: 로컬 링크 31개 확인, 문서 커밋 전후 diff 형식 검사 통과.
- 앞선 사용자 요구 반영: 문서 11개, 내부 링크·앵커 119개, 중복 제외 고정 SHA 18경로 확인, 문서 4개 변경·원본 보존 확인.

이는 당시 결과이며 이번 구체 설계의 검사 수치가 아니다. 이번 문서 검증 결과는 [docs README](../README.md#구체-설계-검증)에 별도로 남긴다. 실제 Skill 행동 평가·Mermaid 렌더링·Browser/PR 실행은 아직 하지 않았다.

```powershell
Set-Location 'C:/Dev/plans-steps-pr-skills'
git status --short --branch
git log -3 --oneline
git rev-parse HEAD main feature/gated-development-v2
git diff --stat
git diff d7c0887 -- skills README.md LICENSE
```

## 8. 다음 세션 재개 문장

```text
C:/Dev/plans-steps-pr-skills의 v3 작업을 이어가자.
docs/handoffs/2026-09-27-v3-analysis-handoff.md와 현재 Git 상태를 먼저 확인해줘.
현재는 구현 가능한 추천 설계까지 완료됐고 실제 Skill 구현은 아직 시작하지 않았어.
docs/04-v3-upgrade-considerations.md의 7개 독립 Skill 구조와 첫 구현 범위를 기준으로 봐줘.
PREPARE/EXECUTE는 확정 요구이고, Context와 통합 검토 책임·파일 배치도 추천안이 정해졌어.
Superpowers 비사용, GPT-5.6 Sol Medium 대상, ponytail 미확인 제외를 유지해줘.
미커밋 문서 변경과 main/v2의 과거 사실을 보존하고 내가 이번 세션에 요청한 범위에서 진행해줘.
```

진행 단계가 바뀌면 현재 상태·Git 스냅샷·실제 완료 범위·검증 근거부터 갱신한다. 추천 설계, 사용자 확정 요구, 구현 결과와 실측 증거를 구분한다.
