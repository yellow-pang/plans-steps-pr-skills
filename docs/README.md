# 기존 스킬 분석과 v3 검토 자료

현재 v3를 설치하거나 이전 main에서 교체하려면 [설치·교체와 사용 안내](installation.md)를 먼저 읽는다. 아래 문서는 설계의 배경과 단계별 검증 이력을 보존한다.

v3 첫 구현은 `e8e9328`, 이후 문서·커밋 처리 기준의 보완은 `24205fe`에 커밋했다. 검토의 발견, 보완 전후와 실제 검증은 [v3 재검토 문서](steps/2026-09-27-v3-skill-review.md)에 있다. 아래의 과거 main 분석과 현재 v3 구현을 구별한다.

컨텍스트 압축 후 재개할 때는 [v3 중간 인계 문서](handoffs/2026-09-27-v3-analysis-handoff.md)를 먼저 읽는다. 최초 분석 절의 검증 수치는 당시 기록이며, 이후 커밋 상태와 다음 작업은 인계 문서와 실제 Git 상태에서 확인한다. 이번 요구 반영의 검증은 문서 끝에 별도로 기록한다.

2026-09-27에 사용자 개발 workflow와 개선 요구를 확인한 뒤 [04 구체 설계](04-v3-upgrade-considerations.md)를 완성했다. 이후 같은 브랜치에서 v3 Skill 7개와 [초기 행동 평가 명세](../tests/behavior/cases.md)를 작성했다. 이 문서의 아래 비교·평가는 **과거 main 5개**를 대상으로 한다. 현재 v3 구현은 [루트 README](../README.md)를 본다. 설계 당시 평가 대상은 GPT-5.6 Sol Medium이었고, 현재 사용자 지정 대상은 GPT-6 Sol Medium이다. CLI 업데이트 후 [B01–B07 실제 행동 평가](../tests/behavior/runs/2026-09-27-gpt-6-sol-medium.md)를 진행했다.

기존 스킬은 **계획·구현·커밋 메시지 준비·완료 기록·PR 설명을 각각 맡는 5개의 독립 스킬**이다. 모든 작업을 Plan → 구현 → Steps → Commit → PR로 강제하는 구조는 아니다. 범위가 명확한 수정은 계획 없이 진행할 수 있고, 관련 문서가 없어도 각 작업을 수행할 수 있다.

강점은 사실·diff·실제 검증 근거 중심의 작성과 불필요한 후속 산출물 억제다. 최초 분석의 개선 대상은 **계획과 직접 구현의 선택 경계, 간접 요청의 해석, 기존 승인 재사용, 작은 작업의 출력 분량, 복합 요청의 완료 지점**이다. 새 사용자 요구로 **lifecycle 영향 분석, 중간 context, 외부 관측, 테스트 유효성·증거 재사용, Plan 단계의 복잡도·중복 검토**를 추가했다.

## 읽는 순서

| 문서 | 확인할 내용 |
|---|---|
| [01. 구성과 실행 흐름](01-structure-and-flow.md) | 파일 구조, Mermaid 흐름도, 입출력, 공통 규칙, 책임 범위 |
| [02. 강제성과 요청 처리 평가](02-enforcement-and-request-evaluation.md) | 강제 수준, 스킬별 비교, 정적 시나리오 24개와 평가 한계; v3에서는 카탈로그로 사용 |
| [03. v2 비교 맥락](03-v2-context.md) | 5개 독립 스킬과 7개 플러그인 스킬의 차이, 기존 테스트 기록, 미확정 원인 |
| [04. v3 업그레이드 구체 설계](04-v3-upgrade-considerations.md) | 원문 대조·U01~U13, 7개 역할·인계·main 변경 매핑, 공통 원칙·Context·Git·평가·첫 구현 범위 |

빠르게 파악하려면 이 문서와 01·02를 읽으면 된다. 개별 규칙을 고칠 때는 아래 스킬별 분석과 원문을 함께 확인한다.

## 스킬별 분석

각 문서는 선택 조건, 입력·산출물, 절차, 필수·조건부·재량 규칙, 짧은 요청 사례, 스킬 간 경계와 개선 후보를 다룬다.

| 과거 main 스킬 | 상세 분석 | 고정 SHA 원문 |
|---|---|---|
| task-planning | [계획 스킬 분석](skills/task-planning.md) | [SKILL.md](https://github.com/yellow-pang/plans-steps-pr-skills/blob/d7c0887e8d8fe2a4ca847c821a46f85bfba88e7a/skills/task-planning/SKILL.md) |
| implementation-workflow | [구현 스킬 분석](skills/implementation-workflow.md) | [SKILL.md](https://github.com/yellow-pang/plans-steps-pr-skills/blob/d7c0887e8d8fe2a4ca847c821a46f85bfba88e7a/skills/implementation-workflow/SKILL.md) |
| preparing-commit | [커밋 준비 스킬 분석](skills/preparing-commit.md) | [SKILL.md](https://github.com/yellow-pang/plans-steps-pr-skills/blob/d7c0887e8d8fe2a4ca847c821a46f85bfba88e7a/skills/preparing-commit/SKILL.md) |
| steps-documentation | [완료 기록 스킬 분석](skills/steps-documentation.md) | [SKILL.md](https://github.com/yellow-pang/plans-steps-pr-skills/blob/d7c0887e8d8fe2a4ca847c821a46f85bfba88e7a/skills/steps-documentation/SKILL.md) |
| pr-documentation | [PR 설명 스킬 분석](skills/pr-documentation.md) | [SKILL.md](https://github.com/yellow-pang/plans-steps-pr-skills/blob/d7c0887e8d8fe2a4ca847c821a46f85bfba88e7a/skills/pr-documentation/SKILL.md) |

## 평가 요약

| 관점 | 결론 | 핵심 근거 |
|---|---|---|
| 구성 | 짧은 단일 파일 5개, 선택적으로 조합 | 별도 라우터·실행 스크립트·플러그인 설정 없음 |
| 명시 요청 인식 | 계획·메시지·Steps·PR 설명처럼 목적을 말하면 선택 근거가 명확함 | 각 description에 해당 산출물 명시 |
| 간접 요청 인식 | “개선해줘”, “정리해줘” 같은 표현은 판단 편차 가능 | “결정 필요”, “유용”, “장기 기록 필요”의 경계 미정 |
| 작은 수정 | 직접 구현을 지원하는 기반이 있음 | Plan 부재 허용, 후속 문서·스킬 비강제 |
| 강제성 | 본문상의 금지·조건은 강하나 프로그램에 의한 실행 차단은 없음 | Markdown 지침만 존재 |
| 승인 | 계획 승인 전 대기·범위 밖 변경 승인은 명시됨 | 기존 승인 유효 범위와 복합 요청 인계는 상세 규칙 부족 |
| Git 완료 범위 | 메시지 준비·PR 설명까지 지원 | 실제 commit·push·PR 발행 담당은 main에 없음 |
| 검증 사실성 | 강점 | 미실행 검증 성공 주장, 계획을 완료 사실로 기록하는 행위 금지 |
| v2의 교훈 | 설치·명시 호출·자동 선택 성공을 분리해야 함 | 기존 기록에서 explicit GREEN과 implicit RED가 공존 |

인식률을 수치로 측정한 결과는 아니다. 높고 낮음에 대한 판단은 원문 기준의 정적 평가이며, 실제 성공률은 별도 환경을 고정한 행동 평가가 필요하다.

## 최초 분석 기준과 작업 범위

| 항목 | 기준 |
|---|---|
| 분석일 | 2026-09-27 |
| 작업 브랜치 | 이미 존재한 `feat/skill-v3-upgrade` 사용 |
| 시작 상태 | working tree clean; HEAD·main·로컬 origin/main·로컬 origin/feat/skill-v3-upgrade 동일 |
| 주 분석 원본 | `d7c0887e8d8fe2a4ca847c821a46f85bfba88e7a`의 `skills/` 5개 |
| 비교 원본 | `feature/gated-development-v2`의 `eb70e3f72dcbe23bc76245e3b8ad12f841279154` |
| 이번 산출물 | `docs/` 아래 분석 문서 10개 |
| 범위 | 원문·브랜치·기존 평가 기록 조사, 구조·규칙 평가와 문서화 |
| 후속 범위 | v3 스킬 구현, 플러그인 재설치, 행동 평가 재실행은 이번 산출물에 포함되지 않음 |

Git 상태는 로컬 참조 기준이다. 원격 최신 상태 확인을 위한 fetch는 하지 않았다. 작업 브랜치가 이미 main과 같은 커밋이어서 새 브랜치를 중복 생성하지 않았다. v2 checkout·merge, 기존 스킬 수정, 설치 캐시 변경, staging·commit·push는 수행하지 않았다.

향후 v3에서 원문이 바뀌어도 이번 분석을 재현할 수 있도록 [main 기준 원본](https://github.com/yellow-pang/plans-steps-pr-skills/tree/d7c0887e8d8fe2a4ca847c821a46f85bfba88e7a/skills)을 고정했다. 문서 내부의 상대 링크는 작업 트리의 파일을 가리키므로 이후에는 원본 SHA도 함께 확인해야 한다.

```powershell
git show d7c0887e8d8fe2a4ca847c821a46f85bfba88e7a:skills/task-planning/SKILL.md
git show eb70e3f72dcbe23bc76245e3b8ad12f841279154:tests/scenarios/README.md
```

## 근거를 읽는 방법

- **원문 사실:** main의 `SKILL.md`에 직접 적힌 규칙과 Git 파일 목록. 각 문서에서 원문 구간으로 연결한다.
- **기존 기록:** v2 브랜치에 남은 2026-08-15의 결과. 이번 세션에서 다시 실행한 성공·실패가 아니다.
- **정적 평가:** 규칙 간 경계와 요청별 예상 동작. 실제 모델 동작과 다를 수 있다.
- **사용자 요구:** 이번 첨부문에서 확인된 실제 경험과 원하는 개발 방향. main/v2가 그 문제를 유발했다는 원인 증거와는 구분한다.
- **개선 후보:** 원문 분석과 사용자 요구를 실현하기 위한 제안. Skill 구조·실행 정책으로 확정된 것은 아니다.
- **공식 설명:** description과 본문 역할 등 일반 구조만 OpenAI 공식 문서로 보강했다. 저장소 자체의 성공 여부를 외부 문서로 입증하지 않는다.

## 최초 분석의 검증 범위

문서 완성 후 Python 일회성 읽기 검사와 Git 조회로 다음을 확인했다. 신규 문서는 untracked 상태이므로 `git diff --check`만으로 검사했다고 주장하지 않고 파일을 직접 읽어 검사했다.

| 확인 항목 | 실제 결과 |
|---|---|
| 문서 파일 수 | 10개 |
| 내부 상대 링크·앵커 | 105개 확인, 오류 0개 |
| 고정 SHA 저장소 참조 경로 | 23개 확인, Git 객체 내 누락 0개; 외부 HTTP 접근 검사는 아님 |
| 후행 공백·코드 블록 짝 | 오류 0개 |
| 기존 추적 파일 | 7개 모두 기준 커밋과 동일; CRLF/LF 차이는 정규화 후 비교 |
| 브랜치 커밋 | HEAD·main·v2 모두 분석 시작 값 유지 |
| Git diff·상태 | `git diff --check` exit 0; 신규 `docs/` 문서 10개만 표시 |

또한 별도 검토자가 전체 흐름·24개 시나리오·개선 후보를 원문과 대조했다. 승인 후 재요청으로 읽힐 표현, PR diff 확인의 조건, 언어 규칙의 근거 링크를 보완했다. Mermaid 도식의 실제 렌더링과 새 모델 세션의 요청 처리 실험은 실행하지 않았다. 검증은 문서의 연결·형식·근거 범위를 확인한 것이며 스킬의 실제 인식률을 검증하는 테스트가 아니다.

## 사용자 요구와 구체 설계로 갱신한 문서

최초 요구 반영에서는 기존 4개 문서를 갱신했고 이번 구체 설계에서는 그 변경을 이어서 수정했다. 02의 향후 평가 절에도 카탈로그 방침을 연결해 현재 미커밋 변경은 기존 문서 5개다. 새 문서는 만들지 않았다. 01·03과 각 Skill의 역사적 원문 분석·Q01~Q24 평가는 보존했다.

| 문서 | 수정 이유와 내용 | 기존 사실 분석 변경 여부 |
|---|---|---|
| [04 구체 설계](04-v3-upgrade-considerations.md) | 요구·원문 대조를 보존하고 7개 역할·책임·인계, PREPARE/EXECUTE, 원칙 배치, Context lifecycle, 7개 평가 사례, 첫 구현 범위를 결정 | 과거 동작을 변경하지 않음. 사용자 확정 사항과 추천 설계 구분 |
| [구현 Skill 분석](skills/implementation-workflow.md) | 최소 수정의 재검토를 영향 해결 기준의 구체 추천안으로 갱신 | 원문·처리 흐름·강제성 분석 유지; v3 제안 부분만 수정 |
| [중간 인계](handoffs/2026-09-27-v3-analysis-handoff.md) | 설계 완료 상태, 확정 요구·추천안, 기존 미커밋 변경, 실제 다음 구현 작업과 평가 한계 기록 | 과거 이력 보존; 낡은 현재 상태 설명 갱신 |
| [02 정적 평가](02-enforcement-and-request-evaluation.md) | 향후 평가 절에 Q01~Q24 카탈로그·선택 실행 방침과 구체 설계 연결 | 기존 평가·사실 변경 없음; 후속 설계 안내만 추가 |
| 이 목차 | 새 요구와 역사적 분석의 구분, 읽는 순서·링크·갱신 범위 정리 | 최초 분석·검증 수치는 과거 기록으로 유지 |

핵심 설계에 반드시 필요한 추가 사용자 선택은 없다. 다음 구현 요청에서는 [첫 구현 범위](04-v3-upgrade-considerations.md#11-첫-구현-범위와-남은-사용자-결정)를 기준으로 진행할 수 있다. ponytail은 실물이 없어 핵심 설계에서 제외했고 Plugin 패키징·설치 캐시 변경은 첫 구현 범위에 넣지 않았다.

## 요구사항 반영 검증

앞선 요구사항 반영 단계에서 2026-09-27에 Python 일회성 읽기 검사와 Git 조회로 다음을 확인했다. 아래는 이번 구체 설계 갱신 이전의 검증 이력이다.

| 확인 항목 | 실제 결과 |
|---|---|
| 검사 문서 | 기존 분석·인계 Markdown 11개 |
| 내부 상대 링크·앵커 | 119개 확인, 오류 0개 |
| 고정 SHA 참조 | 중복을 제외한 18개 경로가 로컬 Git 객체에 존재; 외부 HTTP 확인은 아님 |
| 문서 형식 | 후행 공백·코드 블록 짝 오류 0개, `git diff --check` 통과 |
| 변경 범위 | 위 기존 문서 4개만 수정, staged·untracked 변경 없음 |
| 원본·브랜치 | `skills/` 5개·루트 README·LICENSE는 main과 동일, HEAD·main·v2 SHA와 작업 브랜치 유지 |
| 독립 원문 대조 | 첨부 요구 및 main/v2 원문과 변경 문서를 읽기 전용 검토; 중대한 누락·사실 왜곡 발견 없음 |

Skill 구현·Plugin 변경·새 branch/worktree·commit·push·PR은 수행하지 않았다. 모델 행동 평가·Mermaid 렌더링·Browser 실행은 하지 않았으며 문서 검사를 해당 기능의 성공 증거로 해석하지 않는다.

## 구체 설계 검증

2026-09-27에 Python 일회성 읽기 검사와 Git 조회로 문서·참조 연결·변경 범위를 확인했다.

| 확인 항목 | 실제 결과 |
|---|---|
| 문서·내부 참조 | Markdown 11개, 내부 상대 링크·앵커 122개, 오류 0개 |
| 고정 원문 참조 | 중복 제외 18개 SHA 경로가 로컬 Git 객체에 존재 |
| 문서 형식 | 후행 공백·코드 블록 짝 오류 0개, `git diff --check` 통과 |
| 변경·보존 범위 | 기존 문서 5개만 수정, staged·untracked 없음. main의 Skill 5개·루트 README·LICENSE 및 HEAD/main/v2·작업 브랜치 유지 |
| 독립 설계 검토 | 역할/Context/공통 참조와 Git/행동 평가를 별도로 읽기 검토. Context 생성 책임과 provider smoke 조건의 표현을 정정 |

이는 구현 가능한 설계와 문서의 검사 결과다. 실제 Skill의 행동 평가, GPT-5.6 Sol Medium 준수 여부, Git/provider 실행은 아직 검증하지 않았다. 실제 `SKILL.md`·Plugin·캐시·worktree·branch·commit·push·PR 변경은 하지 않았다.
