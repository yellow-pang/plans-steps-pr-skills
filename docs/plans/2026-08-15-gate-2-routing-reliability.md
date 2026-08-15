---
workflow_id: gdw-20260815-gate2-routing-reliability
mode: FORMAL
state: APPROVED
completion_target: IMPLEMENTATION
risk: R2
plan_digest: "sha256:f23af0f9008e1ba9bd0e743c07f15106b1fcb9842ba43ce99e2f4ea502b3e384"
approved_digest: "sha256:f23af0f9008e1ba9bd0e743c07f15106b1fcb9842ba43ce99e2f4ea502b3e384"
approved_by: "user"
approved_at: "2026-08-15T22:21:12.0076653+09:00"
approval_evidence: "user-message: sha256:f23af0f9008e1ba9bd0e743c07f15106b1fcb9842ba43ce99e2f4ea502b3e384 승인"
previous_approved_digest: "sha256:c3c2583d5b5e8d7bb685bd26bf04c01ddf31923784734d2617fd65c03826b482"
previous_approved_by: "user"
previous_approved_at: "2026-08-15T19:32:47.6977400+09:00"
previous_approval_evidence: "user-message: sha256:c3c2583d5b5e8d7bb685bd26bf04c01ddf31923784734d2617fd65c03826b482 승인."
previous_approved_digest_2: "sha256:569346396b7d67ab6d3e500c27f2aaf08206c4854cdaf2a1033dd2ee897c1dce"
previous_approved_by_2: "user"
previous_approved_at_2: "2026-08-15T20:47:31.6152942+09:00"
previous_approval_evidence_2: "user-message: sha256:569346396b7d67ab6d3e500c27f2aaf08206c4854cdaf2a1033dd2ee897c1dce 승인"
previous_approved_digest_3: "sha256:54d81167e1d9164b3cff7a3c7728bc48cbdafbfbfe8c08f8d4a7cbdfe4a22eb2"
previous_approved_by_3: "user"
previous_approved_at_3: "2026-08-15T21:32:25.7669391+09:00"
previous_approval_evidence_3: "user-message: 파일 읽기 제약 완화 및 implicit Spark 1회(추가 예상 20k~30k토큰) 승인"
---

# 구현 계획: Gate 2 discovery 평가 분리와 비용 상한

## 1. 목표와 현재 문제

자연스러운 개발 요청에서 총괄 Skill이 발견되는지와, 총괄 Skill이 선택된 뒤 정확한 라우팅 계약을 따르는지를 독립적으로 검증한다. 다음 단계의 구현 목표는 Skill을 다시 수정하는 것이 아니라, 작은 fixture와 검증된 실행 profile로 Gate 2B를 저비용으로 한 번 재현할 수 있는 평가 환경을 만드는 것이다.

기존 GPT-5.3-Codex-Spark RED는 “OAuth dependency와 인증 API를 변경하려고 해. 구현해줘.”에 `Mode: IMPLEMENTATION_REQUIRED`, `Risk: 높음`, `Next skill: superpowers:writing-plans`를 반환했다. 기대값은 `FORMAL`, `R3`, `planning-approved-work`다. 이 실행은 안전하게 구현을 중단한 부분만 맞았으며 다음 두 실패 중 어느 것이 발생했는지는 원본 activation trace가 없어 확정할 수 없다.

1. **Discovery:** `running-gated-development`를 선택하지 못했다.
2. **Contract:** Skill을 선택했지만 Mode, Risk, bundled Skill 식별자 계약을 따르지 못했다.

기존 실제 실패를 behavioral RED로 인정한다. 현재 결과는 다음처럼 고정한다.

```text
Explicit body contract  → GREEN
Implicit discovery      → 현재 profile에서 RED
Plugin 자체 결함         → 아직 판정 불가
모델 영향                → 미분리
Skill 경쟁 영향          → 미분리
AGENTS 연계 효과         → 미검증
```

수정 전 RED를 얻기 위한 모델 실행은 반복하지 않는다.

## 2. 조사 근거

| 근거 | 확인 내용 | 계획에 미치는 영향 |
|---|---|---|
| Git 상태 | `feature/gated-development-v2`, HEAD `5dbd8c5`; 기존 Gate 2 변경 8개 tracked 파일과 이 Plan이 미커밋 상태다. | 사용자 변경을 보존하고 이번 후속 범위를 별도로 유지한다. |
| 최초 외부 Spark 결과 | 잘못된 enum과 설치되지 않은 Skill 이름을 반환했다. activation trace는 없다. | discovery와 contract를 별도 가설로 둔다. |
| 후보 Spark 결과 | stale-cache 실행은 무효였고, cache 갱신 후 중첩 실행도 총괄을 사용한 증거 없이 실패했다. | 외부 PowerShell에서 후보를 대조하기 전 환경 원인과 구조 원인을 확정하지 않는다. |
| Skill authoring 계약 | description은 discovery에 사용되고 본문은 선택된 뒤 로드된다. | 본문 contract 수정과 metadata discovery 수정을 같은 효과로 취급하지 않는다. |
| invocation 정책 | 총괄, planning, recording, validating은 implicit이고 나머지 세 mutation specialist는 explicit-only인 원래 정책으로 복원되어 있다. | specialist explicit-only 전체 전환이나 총괄-only implicit을 정답으로 고정하지 않는다. |
| specialist chaining | 총괄이 explicit-only specialist 본문을 동적으로 로드한다는 host 보장은 확인되지 않았다. | single-entry 구조와 Skill-to-Skill chaining에 의존하지 않는다. |
| deterministic test | contract와 원래 invocation policy를 독립 검사하는 targeted 테스트는 GREEN이다. | 기존 GREEN을 재사용하고 clean harness 자체의 새 deterministic RED/GREEN만 추가한다. |
| 모델 입력 제약 | 정답 구조를 프롬프트에 제공하면 Skill을 읽지 않고도 정답 형태를 모방할 수 있다. | behavioral prompt에는 기대 enum, 필드명, Skill 이름을 넣지 않는다. |
| explicit contract 결과 | 독립 Spark가 올바른 총괄 Skill을 읽고 `FORMAL`, `R3`, `planning-approved-work`, 승인 전 구현 중단을 반환했지만 Git·Plan 확인 과정에서 저장소를 읽고 24,602토큰을 사용했다. | loaded-body contract는 GREEN으로 인정하고, 읽기 전용 상태 확인은 허용하되 쓰기·구현 금지와 비용을 별도 판정한다. |
| implicit discovery 결과 | 자연어 입력만 받은 Spark가 repository 조사와 patch 시도까지 진행했고 read-only sandbox가 쓰기를 차단했다. 최종 응답은 routing contract가 아니었으며 61,758토큰을 사용했다. | 현재 profile의 implicit discovery는 RED다. 실패 후 실제 개발 조사까지 이어진 구조를 평가 비용과 제품 failure mode로 함께 기록한다. |
| 현재 Plugin 목록 | 외부 CLI에는 대상 Plugin이 enabled이고 Superpowers는 not installed다. documents, pdf, template-creator, browser, sites, visualize 등 다른 기본 Plugin은 활성화되어 있다. | 현재 실행을 Superpowers 공존 실패나 clean 실행으로 부르지 않는다. |
| CLI profile 경계 | `--profile`은 `$CODEX_HOME/<name>.config.toml`을 기본 설정 위에 겹치고, `--ignore-user-config`는 인증을 제외한 사용자 설정을 무시한다. | 별도 profile이나 `CODEX_HOME`이 Plugin 설치·cache·인증까지 격리한다고 가정하지 않고 Gate 2.0에서 실제 목록과 경로를 검증한다. |

## 3. 추천 방향과 보류 대안

추천안은 **현재 contract-only 후보를 유지하고 clean Gate 2B 평가 환경만 먼저 구현**하는 것이다.

### 유지할 현재 후보

- specialist implicit 정책을 원래 상태로 복원한다.
- 총괄 description은 짧고 구체적인 trigger 중심으로 유지한다.
- 정확한 Mode/Risk enum, bundled specialist allow-list, auth/dependency 경계를 유지한다.
- 4개 필드는 route-only 판정의 positive contract로 사용하되 모든 개발 응답을 항상 정확히 네 줄로 끝내도록 강제하지 않는다.
- explicit body contract의 기존 GREEN과 현재-profile implicit RED를 재사용한다.

### 다음 최소 구현

- 조사할 내용이 거의 없는 작은 fixture repository를 만든다.
- 모델 호출 없이 effective `CODEX_HOME`, config, marketplace, Plugin 목록, cache 경로와 hash, 적용되는 `AGENTS.md` 출처를 기록하는 preflight를 만든다.
- clean은 "시스템 Skill이 전혀 없음"이 아니라 "대상 optional Plugin 외 활성 구성과 기본 Skill 집합이 확인되고 고정됨"으로 정의한다.
- 자연어 OAuth 입력만 전달하고 enum, 필드명, 기대값, Skill 후보를 prompt에 넣지 않는다.
- `read-only`, `ephemeral`, 단일 task, 재시도 없음과 외부 process timeout을 harness 계약으로 둔다.
- JSONL을 원본 증거로 보존하되, 실제 Skill activation event가 노출되는지는 preflight에서 확인하기 전까지 가정하지 않는다.

### 보류 대안

1. **총괄-only implicit:** specialist 경쟁을 줄일 수 있지만 원인 증거와 Skill chaining 보장이 부족하다.
2. **repo-level instruction:** 특정 저장소에서는 강한 진입 경계를 줄 수 있지만 배포형 Plugin의 일반 동작을 증명하지 않는다.
3. **단일 Skill로 병합:** chaining 의존을 제거하지만 범위와 본문 크기가 크게 바뀐다.

보류 대안과 Gate 2C/2D는 clean Gate 2B 결과를 검토한 뒤 별도 Plan과 승인을 받아 검토한다.

## 4. 사용자 결정 사항

- 사용자는 2026-08-15에 discovery와 contract를 분리하고 specialist explicit-only를 미확정 상태로 되돌리는 방향을 승인했다.
- 사용자는 explicit 결과 확인 후 파일 읽기 금지를 완화해 Skill, Git 상태, Plan의 읽기 전용 확인을 허용하고, 구현·파일 수정 금지는 유지하기로 승인했다.
- 사용자는 implicit Spark 1회에 추가 20k~30k reported tokens를 승인했다.
- 승인된 implicit 실행은 61,758토큰을 사용해 실패했으며, 이 결과로 기존 실행 승인은 소진됐다.
- 사용자는 피드백 검토 후 Gate 2.0→2A 재사용→2B clean 저비용 1회→실패 시 strong 1회의 escalation 방향을 Plan에 반영하도록 요청했다.
- 이 승인은 Plan 재작성 방향에 대한 승인이다. 새 body digest의 구현 승인을 대신하지 않는다.
- completion target은 `IMPLEMENTATION`이다.
- commit, push, Draft PR, GitHub 변경은 포함하지 않는다.
- 다른 에이전트와 subagent를 사용하지 않는다.

## 5. 포함 범위와 제외 범위

이번 후속 범위에 포함:

- Gate 2.0 deterministic preflight
- 작은 fixture repository와 비용 제한 harness
- 기존 explicit GREEN 및 implicit RED의 재사용
- clean Gate 2B 저비용 모델 1회와, 실패한 경우에만 동일 조건 strong model 1회
- 원본 prompt, 환경 목록, JSONL 또는 가용한 실행 trace, 최종 응답, reported tokens 기록

제외:

- `running-gated-development` 본문 또는 metadata 추가 수정
- OAuth 키워드 추가
- specialist implicit 정책 변경
- specialist 본문의 재설계 또는 Skill 병합
- single-implicit 정책 확정
- Skill-to-Skill chaining을 지원된 기능으로 가정하는 변경
- repo-level `AGENTS.md` 추가
- Gate 2C 공존 평가와 Superpowers 설치
- Gate 2D `AGENTS.md` bridge 평가
- 전체 pressure suite와 release-ready 판정
- commit, push, PR 생성, merge

## 6. Gate 분리

| Gate | 확인 대상 | 현재 상태 |
|---|---|---|
| `2.0` | 설치, metadata, cache, effective profile 같은 기계적 계약 | clean profile preflight 미구현 |
| `2A` | 선택된 Skill의 loaded-body routing contract | 기존 Spark 결과로 GREEN |
| `2B` | 대상 Plugin의 implicit discovery | 현재 profile RED; clean 조건 미실행 |
| `2C` | 다른 Skill과 공존할 때의 discovery | 후속 승인 전 미실행 |
| `2D` | 선택적 `AGENTS.md` bridge를 포함한 repository integration | 후속 승인 전 미실행 |

Gate 2B는 제품의 자연어 진입 UX를 시험하는 유효한 통합 테스트다. 다만 clean 조건 1회만으로 전체 Plugin 품질을 확정하지 않으며, activation trace가 없으면 "host가 Skill을 선택했다"가 아니라 "선택 결과와 행동적으로 일치한다"고만 판정한다.

## 7. 실행 escalation

```text
Gate 2.0: 모델 호출 없는 clean preflight
        ↓ PASS
Gate 2A: 기존 explicit GREEN 재사용
        ↓
Gate 2B clean / 저비용 모델 1회
        ├─ PASS → STOP, 결과 검토
        └─ FAIL → 동일 clean / strong model 1회
                          ↓
                     STOP, 결과 판정
```

다음 단계의 behavioral model 실행은 최대 2회다. 저비용 모델이 통과하면 strong model은 실행하지 않는다. 두 모델 결과가 나온 뒤에도 같은 단계에서 metadata 수정, 재시도, Gate 2C, Gate 2D 또는 전체 회귀로 자동 진행하지 않는다.

결과 해석은 다음으로 제한한다.

| 결과 | 판정 |
|---|---|
| clean 저비용 PASS | 대상 Plugin의 기본 implicit UX가 해당 조건에서 동작함; 공존 평가는 별도 단계 |
| clean 저비용 FAIL / strong PASS | discovery가 model-sensitive한 후보 |
| clean 두 모델 FAIL | 모델만의 문제로 보기 어려움; metadata/profile/discovery 가설을 한 변수씩 재계획 |
| 향후 clean PASS / coexistence FAIL | Skill-set interaction 후보; 그때 Gate 2C 착수 |

## 8. 예상 파일과 계약

| 파일 또는 영역 | 책임 | 계획된 변화 |
|---|---|---|
| `docs/plans/2026-08-15-gate-2-routing-reliability.md` | 승인 경계 | Gate 구조, 비용 상한, escalation과 중단 조건을 고정한다. |
| `tests/fixtures/gate2-clean/` | 작은 작업 대상 | 읽을 코드와 Git diff를 최소화한 비운영 fixture를 둔다. |
| `tests/scenarios/` 아래 단일 harness | preflight와 실행 | profile/plugin/cache 확인, 단일 `codex exec`, timeout, 원본 증거 저장을 담당한다. 정확한 파일명은 구현 전에 기존 테스트 관례와 PowerShell 이식성을 확인해 정한다. |
| `tests/scenarios/README.md` | 운영 절차 | clean의 정의, 오염 방지, 실행·중단·판정 방법을 기록한다. |
| `docs/steps/2026-08-15-gated-development-v2.md` | 결과 기록 | 구현된 harness와 실제 실행 결과만 추가한다. |

Skill, `agents/openai.yaml`, manifest, 기존 behavioral 기대값은 이번 후속 구현에서 수정하지 않는다.

## 9. 단계별 구현

1. 모델 호출 없이 현재 CLI의 `--profile`, `--ignore-user-config`, `CODEX_HOME`, plugin marketplace와 auth 경계를 확인한다.
2. 사용자 인증정보를 복사하지 않는 방식으로 clean profile을 만들 수 있는지 preflight로 검증한다. 불가능하면 모델을 실행하지 않고 `BLOCKED`로 멈춘다.
3. fixture와 harness의 deterministic RED를 작성한다. preflight가 대상 Plugin 외 optional Plugin, 예상 cache, 알려진 instruction source를 구분하지 못하면 실패해야 한다.
4. fixture와 harness를 최소 구현하고 targeted deterministic 테스트만 실행한다.
5. Plan에 정한 profile과 비용 경계가 실제 명령에 반영되는지 dry-run 또는 명령 출력으로 검증한다. 이 단계까지 모델 호출은 0회다.
6. 변경 내역과 실행 명령을 사용자에게 제시하고 behavioral 실행 비용을 다시 승인받는다.
7. 승인 후 clean 저비용 모델을 1회 실행한다. PASS면 즉시 멈춘다.
8. FAIL이면 같은 prompt, fixture, profile, sandbox 조건을 유지한 strong model 1회를 별도 승인 범위 안에서 실행하고 멈춘다.
9. 결과를 기록하고 다음 가설을 제안한다. 이번 단계에서 Skill 변경이나 Gate 2C/2D로 넘어가지 않는다.

## 10. 위험, 배포, 롤백

Risk는 R2다. 외부 `codex exec`를 시작하고 profile·Plugin 상태를 판정하는 평가 harness를 추가하기 때문이다. Skill의 공개 workflow contract는 이번 후속 범위에서 변경하지 않는다.

주요 위험:

- 별도 profile이 config만 겹치고 Plugin 설치·cache·auth를 완전히 격리하지 않을 수 있다.
- read-only sandbox는 파일 쓰기를 막지만 조사와 토큰 소비를 막지 못한다.
- process timeout은 비용을 제한하지만 activation 판정 전에 실행을 종료할 수 있다.
- 작은 fixture가 실제 repository의 instruction chain이나 Skill 경쟁을 대표하지 않는다.

롤백은 새 fixture, harness와 관련 문서로 제한한다. 사용자 기본 config, 인증정보, 기존 Plugin cache를 덮어쓰거나 제거하지 않는다.

## 11. RED→GREEN 검증과 완료 지점

| 단계 | 검증 | 실행 횟수와 중단 조건 |
|---|---|---|
| 기존 RED | 사용자가 제공한 외부 Spark 실패 | 기존 1회를 인정; 신규 RED 실행 없음 |
| Gate 2.0 RED | 아직 clean 여부를 기계적으로 증명할 preflight가 없음 | 모델 호출 0회 |
| Gate 2.0 GREEN | preflight와 작은 fixture/harness targeted test | 구현 중 관련 deterministic test만 실행; 실패 시 모델 실행 금지 |
| Gate 2A | 완료된 explicit Spark 결과 재사용 | 신규 실행 0회 |
| Gate 2B low-cost | clean profile, 자연어 implicit 입력 | 승인 후 최대 1회; PASS면 중단 |
| Gate 2B strong escalation | low-cost가 FAIL인 경우 동일 조건 | 승인 범위 안에서 최대 1회; 결과와 무관하게 중단 |
| 전체 deterministic 회귀 | 저장소 전체 unittest | behavioral 결과로 후보 수정이 안정된 마지막 Gate에서 정확히 1회; 이번 clean 환경 구축 단계에서는 실행하지 않음 |
| Gate 2C/2D | coexistence 및 `AGENTS.md` integration | 이번 Plan에서 0회 |

새 `codex exec`는 최대 2회다. 그러나 clean 환경 구현과 deterministic 검증이 끝난 뒤 예상 비용과 timeout을 다시 제시하고 별도 승인을 받기 전에는 실행하지 않는다. 첫 저비용 실행이 PASS면 실제 실행 수는 1회다.

이번 후속 구현의 완료 지점은 모델 호출 없이 Gate 2B clean 실행 환경, preflight, 작은 fixture와 비용 제한 harness가 준비되고 targeted deterministic 검증이 통과한 상태다. local commit, push, Draft PR은 수행하지 않는다.
