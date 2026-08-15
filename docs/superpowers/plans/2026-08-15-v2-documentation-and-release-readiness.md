# v2 구현 기록 및 Release Readiness Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** v2가 무엇을 해결하고 어떻게 구현됐는지 한 문서에서 이해할 수 있게 만들고, 남은 다섯 Release Gate를 재현 가능한 증거와 함께 순서대로 검증한다.

**Architecture:** 일반 독자를 위한 설명과 유지보수자를 위한 기술 상세를 하나의 Steps 문서에 계층적으로 배치한다. Release 검증은 저장소 내부 deterministic 검사, 설치된 Plugin 동작, fresh-context 행동, standalone 설치, GitHub CI 순서로 진행하며 외부 권한이나 호스트 기능이 없으면 성공으로 바꾸지 않고 환경 차단 증거를 남긴다.

**Tech Stack:** Markdown, Mermaid, JSON, YAML, Python 3 standard library, `unittest`, Agent Skills validators, Codex Plugin host, GitHub Actions.

## Global Constraints

- 작업 대상은 `C:\Dev\plans-steps-pr-skills`의 `feature/gated-development-v2` 브랜치다.
- 사용자의 명시적 요청 없이 commit, push, Draft PR 생성, GitHub APPROVE, merge를 수행하지 않는다.
- 기존 개인 Codex 설정과 설치된 Plugin을 덮어쓰지 않는다. 사용자가 로컬 Plugin 설치를 명시적으로 요청한 경우 공식 CLI 명령으로 repo marketplace와 해당 Plugin만 추가한다.
- Microsoft Store package 내부 CLI의 `Access is denied` 이력은 보존하되, 이후 설치된 npm 기반 `codex-cli 0.147.0`을 현재 실행 경로로 사용한다.
- 공식 OpenAI 문서가 명령이나 호스트 동작과 충돌하면 공식 문서와 현재 설치된 validator를 우선하고 차이를 문서화한다.
- fresh-context 결과는 static 계약 테스트와 구분하며, 원본 입력·출력·호스트·시각을 보존한다.
- 다섯 Gate가 실제 증거로 통과하기 전에는 `release-ready`로 표현하지 않는다.

---

### Task 1: 구현 기록 문서 계약 만들기

**Files:**
- Modify: `tests/test_repository_contract.py`
- Create: `docs/steps/2026-08-15-gated-development-v2.md`
- Modify: `README.md`

**Interfaces:**
- Consumes: v2 설계서, 구현 계획서, 7개 `SKILL.md`, assets, references, scripts, 실제 검증 출력.
- Produces: README에서 발견할 수 있고 정적 계약으로 보호되는 통합형 구현 기록 문서.

- [x] **Step 1: 구현 기록 링크와 핵심 섹션 계약을 실패 테스트로 추가**

  `test_repository_docs_and_ci_contract`에 README의 `docs/steps/2026-08-15-gated-development-v2.md` 링크를 요구하고, 새 테스트 `test_v2_steps_explains_implementation_and_release_gates`에서 다음 제목과 문자열을 요구한다.

  ```python
  required = [
      "한눈에 보기",
      "전체 흐름",
      "7개 Skill",
      "Plan digest",
      "패키지 구조",
      "완료된 검증",
      "미완료 Release Gate",
      "권장 다음 단계",
      "BLOCKED_ENVIRONMENT",
  ]
  ```

- [x] **Step 2: 대상 테스트가 문서 부재로 RED인지 확인**

  Run: `python -B -m unittest tests.test_repository_contract.RepositoryContractTest.test_v2_steps_explains_implementation_and_release_gates -v`

  Expected: `docs/steps/2026-08-15-gated-development-v2.md`가 없어 FAIL 또는 ERROR.

- [x] **Step 3: 통합형 Steps 문서 작성**

  앞부분은 문제, 해결 방식, 전체 흐름, Mode·Risk, 실제 사용 예를 쉬운 한국어로 설명한다. 뒷부분은 7개 Skill 경계, 승인 digest, 검증 ledger, 패키지 파일 지도, 테스트, CI, 완료 증거, 다섯 Gate의 실행법·통과 조건·증거·권한을 다룬다. 세 개 이상의 상태 전이가 있는 전체 흐름과 승인 흐름에만 Mermaid를 사용한다.

- [x] **Step 4: README에서 구현 기록 문서 연결**

  `개발과 검증` 절에 “처음 읽는 사람과 유지보수자를 위한 v2 구현 기록” 한 줄을 추가하고 상대 링크를 연결한다. README 본문에 Steps 내용을 중복 복사하지 않는다.

- [x] **Step 5: 문서 계약 GREEN 확인**

  Run: `python -B -m unittest tests.test_repository_contract -v`

  Expected: 모든 repository contract 테스트 PASS.

### Task 2: 현재 로컬 구현 증거 갱신

**Files:**
- Modify: `docs/steps/2026-08-15-gated-development-v2.md`
- Modify: `docs/superpowers/plans/2026-08-15-v2-documentation-and-release-readiness.md`

**Interfaces:**
- Consumes: 현재 working tree와 fresh validator 출력.
- Produces: 실행 명령, 결과, 범위, 환경 차단을 구분한 최신 검증 표.

- [x] **Step 1: deterministic 전체 계약 실행**

  Run: `python -B -m unittest discover -s tests -p "test_*.py" -v`

  Expected: 실패 0개.

- [x] **Step 2: 7개 Skill과 Plugin 공식 validator 실행**

  설치된 `quick_validate.py`를 각 `plugins/plans-steps-pr-skills/skills/<skill-name>`에 실행하고 `validate_plugin.py`를 `plugins/plans-steps-pr-skills`에 실행한다.

  Expected: Skill 7개와 Plugin 1개 모두 valid.

- [x] **Step 3: Plan digest와 Git 범위 검사**

  Run: `python -B plugins/plans-steps-pr-skills/skills/planning-approved-work/scripts/plan_digest.py digest plugins/plans-steps-pr-skills/skills/planning-approved-work/assets/plan-template.md`

  Run: `git diff --check`

  Expected: digest는 `sha256:` 문자열을 출력하고 Git whitespace 오류는 0개.

- [x] **Step 4: Steps 문서의 완료 증거 갱신**

  실제 출력에서 테스트 수, validator 수, digest 결과, 실행 환경을 기록한다. 실행하지 않은 host 행동은 완료 표에 넣지 않는다.

### Task 3: Plugin 설치 및 7개 Skill 노출 Gate

**Files:**
- Create: `tests/scenarios/results/2026-08-15/plugin-install.md`
- Modify: `docs/steps/2026-08-15-gated-development-v2.md`

**Interfaces:**
- Consumes: repo marketplace, Plugin manifest, 공식 Plugin 테스트 지침, 접근 가능한 Codex host.
- Produces: 설치 경로, Plugin 표시, 7개 Skill 노출 여부를 담은 설치 smoke 증거.

- [x] **Step 1: 공식 host 경로 확인**

  공식 OpenAI Plugin 문서의 “local marketplace에 추가 → Plugins Directory에서 설치 → 새 대화에서 활성화” 순서를 기준으로 현재 Codex Desktop에서 지원되는 설치 표면을 확인한다. CLI를 사용할 수 있으면 `codex plugin marketplace add .`와 `codex plugin add plans-steps-pr-skills@yellow-pang-workflows`의 실제 도움말을 먼저 확인한다.

- [x] **Step 2: 사용자 개인 설치와 격리 경계 확인**

  별도 profile, test directory, disposable app context처럼 기존 설치를 건드리지 않는 경로가 확인되면 그 경로만 사용한다. 격리 경로가 없으면 설치를 수행하지 않고 WindowsApps 실행 차단과 지원 표면 부재를 `BLOCKED_ENVIRONMENT`로 기록한다.

- [x] **Step 3: 설치 후 새 작업에서 Plugin과 Skill 목록 확인**

  `plans-steps-pr-skills` Plugin이 설치됨으로 표시되고 아래 7개 Skill이 모두 보이는지 확인한다.

  ```text
  running-gated-development
  planning-approved-work
  implementing-with-risk-checks
  recording-implementation
  committing-verified-work
  publishing-pull-request
  validating-pull-request
  ```

  Evidence: `codex plugin list`에서 version `2.0.0`이 `installed, enabled`로 표시됐고 설치 캐시에 7개 Skill 디렉터리가 모두 존재했다. 별도 `read-only`·`ephemeral` 작업에서 `$running-gated-development`를 직접 호출해 설치 캐시의 Skill 로드, `DISCUSS` 판정, 실행 전후 Git 상태 일치를 확인했다.

- [x] **Step 4: 설치 증거 기록**

  host·버전, 설치 표면, 설치 위치, 표시된 Skill, 누락 항목, 원복 방법을 `plugin-install.md`에 기록한다. 계정 식별자와 개인 설정 값은 기록하지 않는다.

### Task 4: 호출 정책과 fresh-context pressure scenario Gate

**Files:**
- Modify: `tests/scenarios/workflow-pressure-cases.yaml`
- Create: `tests/scenarios/results/2026-08-15/behavioral-summary.md`
- Create: `tests/scenarios/results/2026-08-15/raw/README.md`
- Modify: `docs/steps/2026-08-15-gated-development-v2.md`

**Interfaces:**
- Consumes: 설치된 Plugin, 10개 pressure scenario, `agents/openai.yaml` 호출 정책.
- Produces: Skill 없음/있음 비교와 총괄→전문 Skill 라우팅의 행동 증거.

- [ ] **Step 1: scenario 실행 메타데이터 확정**

  `workflow-pressure-cases.yaml`의 `behavioral_run`을 실행 전에는 `in-progress`로 두고 host, model, 실행 시각, fresh-context 정의를 기록한다. 결과가 없는데 `passed`로 바꾸지 않는다.

- [ ] **Step 2: 각 scenario를 Skill 없이 fresh context에서 실행**

  10개 입력을 서로 상태를 공유하지 않는 새 작업에서 실행한다. 원본 prompt와 응답을 `raw/`에 scenario id별 Markdown으로 보존하고 baseline의 실제 위반과 통과를 평가한다.

- [ ] **Step 3: 각 scenario를 설치된 Plugin과 함께 fresh context에서 실행**

  동일한 10개 입력을 새 작업에서 Plugin을 활성화해 실행한다. 기대 답을 prompt에 넣지 않고, 각 expected 항목이 출력과 실제 mutation 경계에서 관찰됐는지 기록한다.

- [ ] **Step 4: 명시 호출과 암묵 호출 경계 확인**

  총괄 Skill이 mutation 전문 Skill을 명시적으로 선택하는지 확인한다. `allow_implicit_invocation: false`인 구현·commit·PR Skill이 일반 요청에서 단독 암묵 호출되지 않고, `$skill-name` 직접 호출에서는 발견되는지 기록한다.

- [ ] **Step 5: 행동 verdict 기록**

  20회 원본 실행을 기준으로 scenario별 `PASS`, `FAIL`, `BLOCKED_ENVIRONMENT` 중 하나를 기록한다. 하나라도 FAIL 또는 BLOCKED이면 `behavioral_run`을 `passed`로 바꾸지 않는다.

### Task 5: standalone Skill 설치 Gate

**Files:**
- Create: `tests/scenarios/results/2026-08-15/standalone-install.md`
- Modify: `docs/steps/2026-08-15-gated-development-v2.md`

**Interfaces:**
- Consumes: 저장소 하위 Skill 경로와 `$skill-installer`.
- Produces: Plugin 없이 선택한 Skill을 설치·발견·호출한 증거.

- [ ] **Step 1: 격리된 설치 대상 확인**

  `$skill-installer`가 사용자 기본 Skill 디렉터리를 건드리지 않고 별도 대상에 설치할 수 있는지 도움말과 Skill 지침으로 확인한다. 별도 대상이 없으면 사용자 전역 설치를 수행하지 않고 Gate를 `BLOCKED_ENVIRONMENT`로 둔다.

- [ ] **Step 2: 대표 Skill 두 개 설치**

  격리 대상이 있으면 `planning-approved-work`와 `validating-pull-request`를 저장소 하위 경로에서 설치한다. 하나는 작성 흐름, 하나는 읽기 중심 검토 흐름을 대표한다.

- [ ] **Step 3: 새 작업에서 직접 호출 확인**

  `$planning-approved-work`와 `$validating-pull-request`가 Plugin 없이 발견되고 각 Skill의 mutation 경계를 지키는지 확인한다.

- [ ] **Step 4: 설치·호출·정리 증거 기록**

  설치 명령 또는 UI 단계, 대상 경로, 발견 결과, 호출 결과, 정리 결과를 기록한다. 원래 사용자 Skill은 제거하거나 덮어쓰지 않는다.

### Task 6: 실제 GitHub Actions와 release-ready 판정

**Files:**
- Create: `tests/scenarios/results/2026-08-15/github-actions.md`
- Modify: `docs/steps/2026-08-15-gated-development-v2.md`
- Modify: `README.md`
- Modify: `docs/superpowers/plans/2026-08-15-gated-development-v2-implementation.md`
- Modify: `docs/superpowers/plans/2026-08-15-v2-documentation-and-release-readiness.md`

**Interfaces:**
- Consumes: 사용자의 별도 commit·push·Draft PR 권한, 실제 Actions 결과, 앞선 네 Gate 증거.
- Produces: release-ready 또는 명시적 미완료 verdict.

- [ ] **Step 1: 외부 쓰기 승인 확인**

  local commit, push, Draft PR 각각에 대해 현재 사용자 메시지 또는 승인된 completion target이 있는지 확인한다. 하나라도 없으면 GitHub 변경을 수행하지 않는다.

- [ ] **Step 2: 승인된 경우 branch diff를 commit하고 Draft PR 게시**

  관련 파일만 명시적으로 stage하고 검증된 목적 단위로 local commit한다. push와 Draft PR이 각각 승인된 경우에만 현재 feature branch를 push하고 Draft PR을 만든다. merge와 GitHub APPROVE는 금지한다.

- [ ] **Step 3: 실제 Actions 결과 확인**

  `.github/workflows/validate-plugin.yml`의 run URL, commit SHA, 각 job 결과를 읽어 기록한다. 취소, 미실행, 권한 실패, dependency 실패를 PASS로 처리하지 않는다.

- [ ] **Step 4: release verdict 갱신**

  Plugin 설치, 7개 Skill 노출, 호출 정책, 10개 pressure scenario, standalone 설치, GitHub Actions가 모두 실제 증거로 통과한 경우에만 README의 사전-release 경고를 release-ready 표현으로 변경한다. 그 외에는 미완료 Gate와 다음 행동을 그대로 유지한다.

- [ ] **Step 5: 최종 검증**

  Run: `python -B -m unittest discover -s tests -p "test_*.py" -v`

  Run: `git diff --check`

  Expected: 테스트 실패 0개, whitespace 오류 0개, 결과 문서와 실제 Gate verdict 일치.
