# Gate 2B clean evaluation handoff

## 목적

다음 작업 세션에서 Gate 2 routing 조사를 재구성하지 않고, 격리 profile 준비와 승인된 behavioral 평가부터 이어서 진행하기 위한 기록이다. 이 문서는 다음 Codex 세션에 주는 지시이며 behavioral 모델의 입력이 아니다.

## 현재 상태

- 작업 브랜치: `feature/gated-development-v2`
- 이 handoff commit 직전 기준 HEAD: `5dbd8c5cbbae1802dc59e54f76a389a0cf56ac77`
- 승인 Plan: `docs/plans/2026-08-15-gate-2-routing-reliability.md`
- 승인 digest: `sha256:f23af0f9008e1ba9bd0e743c07f15106b1fcb9842ba43ce99e2f4ea502b3e384`
- `Gate 2A explicit body contract`: GREEN
- 현재 사용자 profile의 `Gate 2B implicit discovery`: RED
- clean profile의 구조 preflight: PASS, 단 인증을 복사하지 않아 `BLOCKED_AUTH`
- Plugin 자체 결함, 모델 영향, Skill 경쟁 영향, `AGENTS.md` bridge 효과: 아직 분리되지 않음
- commit 뒤 새 세션에서는 이 문서의 HEAD보다 `git rev-parse HEAD`와 `git status --short`를 우선한다.

## 구현된 평가 장치

| 경로 | 역할 |
|---|---|
| `tests/scenarios/gate2_clean_harness.py` | isolated `CODEX_HOME` setup, preflight, dry-run, 단일 behavioral 실행과 원본 증거 저장 |
| `tests/fixtures/gate2-clean/` | 실제 애플리케이션 조사를 유발하지 않는 독립 Git fixture |
| `tests/test_gate2_clean_harness.py` | Plugin 격리, Skill namespace, `AGENTS.md`, fixture, 명령, routing score 계약 |
| `tests/scenarios/README.md` | 운영 명령과 비용·중단 경계 |
| `docs/steps/2026-08-15-gated-development-v2.md` | 실제 구현·검증·남은 Gate 기록 |

`run`은 다음 계약을 갖는다.

- `read-only`, `ephemeral`, approval policy `never`
- 입력은 `PROMPT` 상수의 자연어 요청 하나만 stdin으로 전달
- `--output-schema`와 정답 힌트 없음
- 재시도와 strong-model 자동 escalation 없음
- 기본 timeout 120초, 허용 범위 30~300초
- JSONL, stderr, final message, usage, fixture Git 상태, routing score 저장

## 확인된 clean preflight 증거

disposable `CODEX_HOME`에서 harness의 `setup`과 unauthenticated `preflight`를 실행했다.

- enabled Plugin: `plans-steps-pr-skills@yellow-pang-workflows` 하나
- 설치 version: `2.0.0`
- source/cache: manifest, 7개 `SKILL.md`, 7개 `agents/openai.yaml` SHA-256 일치
- 대상 model-visible implicit Skills: planning, recording, orchestrator, validation 4개
- Browser와 Superpowers namespace: 없음
- global/project `AGENTS.md`와 `AGENTS.override.md`: 없음
- 전체 visible Skills: 16개
- rendered prompt input: 5 messages, 14,677 characters
- 독립 fixture Git 상태: clean
- 인증 상태: `BLOCKED_AUTH`
- behavioral model calls: 0

clean은 system 또는 cross-runtime Skill까지 0개라는 뜻이 아니다. 대상 외 **Plugin namespace와 저장소 instruction source가 제거되고 그 잔여 목록이 기록된 상태**를 뜻한다.

## 완료된 검증

```text
python -B -m unittest tests.test_gate2_clean_harness -v
→ 8 tests PASS

python -B -m unittest \
  tests.test_repository_contract.RepositoryContractTest.test_v2_steps_explains_implementation_and_release_gates \
  tests.test_repository_contract.RepositoryContractTest.test_no_placeholders_or_broken_local_markdown_links -v
→ 2 tests PASS

git diff --check
→ exit 0; Windows LF→CRLF warnings only
```

전체 deterministic regression, strong model, Gate 2C/2D, 전체 pressure suite는 실행하지 않았다.

## 다음 실행 순서

1. Git 상태, 현재 HEAD, 승인 Plan digest와 이 handoff를 확인한다.
2. 저장소 밖의 새 경로를 persistent clean `CODEX_HOME`으로 정한다.
3. harness `setup`을 한 번 실행한다.
4. 사용자가 해당 `CODEX_HOME`으로 `codex login`을 완료한다. 기존 인증 파일을 복사하거나 링크하지 않는다.
5. `preflight`를 실행하고 `PASS`, 대상 Plugin 하나, 네 implicit Skills, 빈 instruction sources를 확인한다.
6. low-cost model을 지정해 `dry-run`을 실행한다. 이 단계까지 model call은 0회다.
7. 실제 명령, timeout, 예상 토큰 비용과 결과 저장 경로를 사용자에게 제시하고 behavioral 1회 승인을 받는다.
8. 승인 후 low-cost model을 정확히 한 번 실행한다.
9. PASS면 멈춘다. FAIL이면 결과를 기록하고 같은 clean 조건의 strong model 1회 비용을 별도 승인받기 전까지 멈춘다.
10. Gate 2C coexistence, Gate 2D `AGENTS.md` bridge, Skill/metadata 수정은 결과 검토 뒤 별도 Plan으로 다룬다.

behavioral 모델에 전달하는 입력은 harness에 고정된 다음 한 문장뿐이다.

```text
OAuth dependency와 인증 API를 변경하려고 해. 구현해줘.
```

다음 세션용 재개 프롬프트 전체를 behavioral 모델 입력으로 전달하지 않는다.

## 다음 Codex 세션에 붙여넣을 프롬프트

```text
작업 경로: C:\Dev\plans-steps-pr-skills

이전 Gate 2B clean evaluation 작업을 이어서 진행해줘.

먼저 git status, 현재 브랜치와 HEAD를 확인하고 기존 변경을 보존해. 다음 문서를 읽어 현재 상태와 승인 경계를 복구해:
- docs/handoffs/2026-08-15-gate-2b-clean-evaluation.md
- docs/plans/2026-08-15-gate-2-routing-reliability.md
- docs/steps/2026-08-15-gated-development-v2.md
- tests/scenarios/README.md

승인된 Plan digest는 sha256:f23af0f9008e1ba9bd0e743c07f15106b1fcb9842ba43ce99e2f4ea502b3e384 이다. 현재 목표는 Skill을 수정하는 것이 아니라 별도 persistent CODEX_HOME에서 clean Gate 2B preflight와 dry-run을 준비하는 것이다.

진행 순서:
1. tests/scenarios/gate2_clean_harness.py와 관련 fixture/test를 확인한다.
2. 저장소 밖의 새 CODEX_HOME 경로를 제안하고, 기존 인증 파일을 복사하거나 링크하지 않는다.
3. setup 후 사용자가 그 profile에서 codex login을 완료하도록 안내한다.
4. 로그인 뒤 preflight와 dry-run까지만 모델 호출 없이 실행한다.
5. 실제 low-cost 모델 명, 명령, timeout, 예상 토큰 비용, 결과 경로를 보고하고 behavioral 실행 승인을 요청한 뒤 멈춘다.

behavioral prompt에는 harness의 원래 OAuth 자연어 입력만 사용하고 Mode/Risk/Skill 이름/기대값을 추가하지 마. 승인 전 codex exec 모델 호출, strong model, Gate 2C/2D, 전체 pressure suite, Skill 본문·metadata 변경을 하지 마. 다른 에이전트나 subagent를 사용하지 마. commit, push, PR도 새로 요청받기 전에는 하지 마.
```

## 권한 경계

- 현재 local commit 권한은 이 handoff와 Gate 2B 평가 장치 변경을 묶는 이번 commit에만 적용된다.
- push, Draft PR, review, merge 권한은 없다.
- persistent profile 로그인과 behavioral 모델 비용은 후속 사용자의 명시적 참여·승인이 필요하다.
