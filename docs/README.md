# 기존 스킬 분석과 v3 검토 자료

기존 스킬은 **계획·구현·커밋 메시지 준비·완료 기록·PR 설명을 각각 맡는 5개의 독립 스킬**이다. 모든 작업을 Plan → 구현 → Steps → Commit → PR로 강제하는 구조는 아니다. 범위가 명확한 수정은 계획 없이 진행할 수 있고, 관련 문서가 없어도 각 작업을 수행할 수 있다.

강점은 사실·diff·실제 검증 근거 중심의 작성과 불필요한 후속 산출물 억제다. 주된 개선 대상은 **계획과 직접 구현의 선택 경계, 간접 요청의 해석, 기존 승인 재사용, 작은 작업의 출력 분량, 복합 요청의 완료 지점**이다. 이번 문서는 그 근거와 v3 검토 후보를 정리한다.

## 읽는 순서

| 문서 | 확인할 내용 |
|---|---|
| [01. 구성과 실행 흐름](01-structure-and-flow.md) | 파일 구조, Mermaid 흐름도, 입출력, 공통 규칙, 책임 범위 |
| [02. 강제성과 요청 처리 평가](02-enforcement-and-request-evaluation.md) | 강제 수준, 스킬별 비교, 짧은 요청·경계 사례 24개, 평가 한계 |
| [03. v2 비교 맥락](03-v2-context.md) | 5개 독립 스킬과 7개 플러그인 스킬의 차이, 기존 테스트 기록, 미확정 원인 |
| [04. v3 업그레이드 검토 사항](04-v3-upgrade-considerations.md) | 유지할 원칙, 개선 우선순위, 아직 정하지 않은 사용자 작업 방식 |

빠르게 파악하려면 이 문서와 01·02를 읽으면 된다. 개별 규칙을 고칠 때는 아래 스킬별 분석과 원문을 함께 확인한다.

## 스킬별 분석

각 문서는 선택 조건, 입력·산출물, 절차, 필수·조건부·재량 규칙, 짧은 요청 사례, 스킬 간 경계와 개선 후보를 다룬다.

| 스킬 | 상세 분석 | 원문 |
|---|---|---|
| task-planning | [계획 스킬 분석](skills/task-planning.md) | [SKILL.md](../skills/task-planning/SKILL.md) |
| implementation-workflow | [구현 스킬 분석](skills/implementation-workflow.md) | [SKILL.md](../skills/implementation-workflow/SKILL.md) |
| preparing-commit | [커밋 준비 스킬 분석](skills/preparing-commit.md) | [SKILL.md](../skills/preparing-commit/SKILL.md) |
| steps-documentation | [완료 기록 스킬 분석](skills/steps-documentation.md) | [SKILL.md](../skills/steps-documentation/SKILL.md) |
| pr-documentation | [PR 설명 스킬 분석](skills/pr-documentation.md) | [SKILL.md](../skills/pr-documentation/SKILL.md) |

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

## 분석 기준과 작업 범위

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
- **개선 후보:** 분석에 근거한 제안. 사용자의 현재 작업 방식이나 v3 요구사항으로 확정하지 않았다.
- **공식 설명:** description과 본문 역할 등 일반 구조만 OpenAI 공식 문서로 보강했다. 저장소 자체의 성공 여부를 외부 문서로 입증하지 않는다.

## 검증 범위

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

v3 설계에서는 [미확정 작업 방식](04-v3-upgrade-considerations.md#4-아직-확정되지-않은-사용자-작업-방식)을 실제 사용 사례와 대응시키는 일이 남아 있다. 이번 분석은 그 결정을 위한 기준 자료다.
