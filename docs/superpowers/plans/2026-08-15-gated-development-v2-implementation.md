# Gated Development Workflow v2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. This session executes inline because the active policy does not authorize subagent dispatch.

**Goal:** Package seven standalone Agent Skills as a repo-local Codex Plugin that enforces explicit approval, risk-scaled verification, evidence-based documentation, controlled commits, Draft PR publication, and independent PR validation.

**Architecture:** Keep one canonical copy of every Skill under `plugins/plans-steps-pr-skills/skills`. The repository root owns marketplace metadata, tests, design records, CI, and portfolio documentation. Put deterministic operations such as Plan digest updates in tested Python scripts and keep judgment rules in concise Skill instructions and reusable templates.

**Tech Stack:** Markdown Agent Skills, YAML `agents/openai.yaml`, JSON Codex Plugin metadata, Python 3 standard library, `unittest`, GitHub Actions.

## Global Constraints

- Modify only the local clone under `work/plans-steps-pr-skills`; do not push or mutate GitHub.
- Preserve the existing MIT license and `Copyright (c) 2026 yellow-pang`.
- Do not copy Superpowers wording, templates, or code into the v2 runtime skills.
- Keep `Mode` and `Risk` independent; QUICK is limited to R0/R1.
- Require explicit user approval and matching Plan body digest before FORMAL implementation.
- Treat new dependencies, public contracts, schema, security boundaries, scope expansion, completion-target changes, and verification reductions as material changes.
- Do not repeat a slow full regression on the same HEAD and environment without a concrete reason.
- Never auto-approve or auto-merge a PR.
- Treat official OpenAI documentation and installed validators as the packaging source of truth.
- Do not claim behavioral release readiness until fresh-context pressure scenarios have run.

---

### Task 1: Establish RED contracts for v1

**Files:**
- Create: `tests/test_repository_contract.py`
- Create: `tests/scenarios/workflow-pressure-cases.yaml`
- Create: `tests/scenarios/README.md`

**Interfaces:**
- Consumes: existing v1 repository layout and five Skill files.
- Produces: `python -m unittest discover -s tests -p "test_*.py"` as the fast local contract command.

- [x] **Step 1: Write failing repository tests**

  Assert that the repo marketplace, nested Plugin manifest, seven canonical Skill folders, required `agents/openai.yaml`, templates, notice, and CI workflow exist. Assert the core policy phrases and exact skill names through parsed frontmatter instead of prose snapshots.

- [x] **Step 2: Run tests and verify RED**

  Run: `python -m unittest discover -s tests -p "test_*.py" -v`

  Expected: failures report missing `.agents/plugins/marketplace.json`, Plugin manifest, and v2 skills.

- [x] **Step 3: Record pressure scenarios before Skill edits**

  Define inputs and observable pass conditions for DISCUSS mutation, QUICK-to-FORMAL escalation, approval evidence, material dependency change, repeated regression, unknown failure provenance, unrelated staging, unauthorized PR, R3 fresh review, and merge prohibition.

- [x] **Step 4: Preserve the RED output**

  Save the command and summarized expected failures in `tests/scenarios/README.md`. Do not claim agent-behavior RED because fresh subagents are unavailable in this session.

### Task 2: Scaffold and validate the repo-local Plugin

**Files:**
- Create: `.agents/plugins/marketplace.json`
- Create: `plugins/plans-steps-pr-skills/.codex-plugin/plugin.json`
- Create: `plugins/plans-steps-pr-skills/skills/`

**Interfaces:**
- Consumes: installed `plugin-creator` scaffold and validator.
- Produces: a Plugin whose manifest name and folder name are both `plans-steps-pr-skills`.

- [x] **Step 1: Run the official scaffold**

  Run `create_basic_plugin.py` with repo-local `plugins` and `.agents/plugins/marketplace.json` destinations, `--with-skills`, and `--with-marketplace`.

- [x] **Step 2: Replace only validated metadata**

  Set semver `2.0.0`, repository URLs, MIT license, Coding/Productivity presentation fields accepted by the current validator, and `skills: "./skills/"`. Do not add MCP, app, hook, icon, privacy, or terms fields without matching resources.

- [x] **Step 3: Validate the Plugin**

  Run the installed `validate_plugin.py` against `plugins/plans-steps-pr-skills` and fix schema failures before Skill work.

### Task 3: Implement `planning-approved-work` with digest TDD

**Files:**
- Create: `plugins/plans-steps-pr-skills/skills/planning-approved-work/SKILL.md`
- Create: `plugins/plans-steps-pr-skills/skills/planning-approved-work/agents/openai.yaml`
- Create: `plugins/plans-steps-pr-skills/skills/planning-approved-work/assets/plan-template.md`
- Create: `plugins/plans-steps-pr-skills/skills/planning-approved-work/scripts/plan_digest.py`
- Create: `tests/test_plan_digest.py`

**Interfaces:**
- Consumes: a Markdown Plan containing one YAML frontmatter block.
- Produces: `compute_body_digest(text) -> str`, `refresh_plan(text) -> str`, and `approve_plan(text, expected_digest, approved_by, approved_at, approval_evidence) -> str`.

- [x] **Step 1: Write failing digest tests**

  Cover LF/CRLF equivalence, frontmatter exclusion, body-change detection, refresh to `AWAITING_APPROVAL`, expected-digest mismatch rejection, and approval metadata written only after matching digest.

- [x] **Step 2: Verify RED**

  Run: `python -m unittest tests.test_plan_digest -v`

  Expected: import failure because `plan_digest.py` does not exist.

- [x] **Step 3: Initialize the Skill with `init_skill.py`**

  Generate only `scripts` and `assets`, plus `agents/openai.yaml` containing explicit display name, 25–64 character short description, and a `$planning-approved-work` default prompt.

- [x] **Step 4: Implement the minimal digest script and Plan template**

  Use only Python standard library. Reject missing/unterminated frontmatter, duplicate approval, digest mismatch, and invalid approval evidence. Never infer a user approval from file metadata alone.

- [x] **Step 5: Write the minimal Skill rules**

  Require read-only project investigation, Plan-only writes before approval, clear decision questions, material-change boundaries, and the four-step approval evidence order.

- [x] **Step 6: Verify GREEN and Skill metadata**

  Run the digest tests and `quick_validate.py` for this Skill.

### Task 4: Implement the orchestrator

**Files:**
- Create: `plugins/plans-steps-pr-skills/skills/running-gated-development/SKILL.md`
- Create: `plugins/plans-steps-pr-skills/skills/running-gated-development/agents/openai.yaml`

**Interfaces:**
- Consumes: user request, repo state, Plan state, approval evidence, requested completion target.
- Produces: one mode, one risk, current state, next specialist, and stop reason when a gate is unmet.

- [x] **Step 1: Add failing contract assertions**

  Require `Mode != Risk`, R2/R3 escalation, DISCUSS read-only behavior, explicit approval, and named specialist transitions.

- [x] **Step 2: Verify RED for this Skill**

  Run the targeted repository contract test and confirm the missing Skill is the cause.

- [x] **Step 3: Initialize and write the Skill**

  Keep it concise: classify, inspect state, verify gate, invoke one specialist, reassess. Do not duplicate templates or implementation rules.

- [x] **Step 4: Validate GREEN**

  Run targeted contract and `quick_validate.py`.

### Task 5: Implement risk-scaled execution

**Files:**
- Create: `plugins/plans-steps-pr-skills/skills/implementing-with-risk-checks/SKILL.md`
- Create: `plugins/plans-steps-pr-skills/skills/implementing-with-risk-checks/agents/openai.yaml`
- Create: `plugins/plans-steps-pr-skills/skills/implementing-with-risk-checks/references/verification-policy.md`

**Interfaces:**
- Consumes: approved Plan or QUICK contract, affected code, repository test configuration.
- Produces: scoped implementation and a verification ledger with command, outcome, HEAD, environment, and timestamp.

- [x] **Step 1: Add failing assertions for risk and regression budget**

  Require dependency/API changes as R2, auth/migration as R3, same-HEAD regression reuse, and unknown failure provenance as non-success.

- [x] **Step 2: Verify RED**

  Run the targeted contract test.

- [x] **Step 3: Initialize and implement**

  Put the short execution loop in SKILL.md and the R0–R3 matrix, TDD boundary, invalidation rules, and ledger schema in `references/verification-policy.md`.

- [x] **Step 4: Validate GREEN**

  Run targeted contract, reference-link checks, and `quick_validate.py`.

### Task 6: Implement implementation records

**Files:**
- Create: `plugins/plans-steps-pr-skills/skills/recording-implementation/SKILL.md`
- Create: `plugins/plans-steps-pr-skills/skills/recording-implementation/agents/openai.yaml`
- Create: `plugins/plans-steps-pr-skills/skills/recording-implementation/assets/steps-template.md`

**Interfaces:**
- Consumes: actual diff, code/config, verification ledger, Git/CI evidence, approved Plan.
- Produces: `docs/steps/YYYY-MM-DD-<slug>.md` with R2 compact or R3 full sections.

- [x] **Step 1: Add failing template assertions**

  Require evidence order, R2 omission rules, R3 full contract, and Mermaid only for three or more components/branches/states.

- [x] **Step 2: Verify RED**

  Run the targeted template test.

- [x] **Step 3: Initialize and implement**

  Keep authoring rules in SKILL.md and the reusable report shape in the asset. Do not repeat empty sections with `해당 없음`.

- [x] **Step 4: Validate GREEN**

  Run targeted contract and `quick_validate.py`.

### Task 7: Implement controlled local commits

**Files:**
- Create: `plugins/plans-steps-pr-skills/skills/committing-verified-work/SKILL.md`
- Create: `plugins/plans-steps-pr-skills/skills/committing-verified-work/agents/openai.yaml`
- Create: `plugins/plans-steps-pr-skills/skills/committing-verified-work/assets/commit-template.md`

**Interfaces:**
- Consumes: approved completion target, verified diff, staged/unstaged/untracked state.
- Produces: one or more intentional local commits and an evidence-based message.

- [x] **Step 1: Add failing safety assertions**

  Require explicit commit authority, secret-safe inspection, explicit paths for staging, unrelated-file exclusion, and split commits for independently reversible purposes.

- [x] **Step 2: Verify RED**

  Run the targeted contract test.

- [x] **Step 3: Initialize and implement**

  Preserve Conventional Commit plus Korean details as a default, while following an existing repository convention when present. Prohibit push and PR.

- [x] **Step 4: Validate GREEN**

  Run targeted contract and `quick_validate.py`.

### Task 8: Implement Draft PR publication

**Files:**
- Create: `plugins/plans-steps-pr-skills/skills/publishing-pull-request/SKILL.md`
- Create: `plugins/plans-steps-pr-skills/skills/publishing-pull-request/agents/openai.yaml`
- Create: `plugins/plans-steps-pr-skills/skills/publishing-pull-request/assets/pr-template.md`
- Create: `.github/PULL_REQUEST_TEMPLATE.md`

**Interfaces:**
- Consumes: committed branch diff, Plan, Steps, verification evidence, explicit push/PR authority.
- Produces: an updated or new Draft PR, or a truthful manual handoff if tooling/authority is absent.

- [x] **Step 1: Add failing authority and shape assertions**

  Require base merge-base diff, uncommitted-change separation, existing-PR detection, Draft status, fixed sections, and no merge.

- [x] **Step 2: Verify RED**

  Run the targeted contract test.

- [x] **Step 3: Initialize and implement**

  Define connector, `gh`, and manual fallback order without hard MCP dependencies. Treat push and PR as distinct external writes.

- [x] **Step 4: Validate GREEN**

  Run targeted contract and `quick_validate.py`.

### Task 9: Implement independent PR validation

**Files:**
- Create: `plugins/plans-steps-pr-skills/skills/validating-pull-request/SKILL.md`
- Create: `plugins/plans-steps-pr-skills/skills/validating-pull-request/agents/openai.yaml`

**Interfaces:**
- Consumes: Plan, Steps, PR diff, test evidence; excludes author reasoning.
- Produces: `MERGEABLE`, `CHANGES_REQUIRED`, or `REVIEW_REQUIRED` with evidence.

- [x] **Step 1: Add failing reviewer assertions**

  Require R2 fresh context as recommended, R3 fresh context as mandatory, evidence-first review, and prohibition of GitHub APPROVE and merge.

- [x] **Step 2: Verify RED**

  Run the targeted contract test.

- [x] **Step 3: Initialize and implement**

  Distinguish CI absence, failed checks, missing evidence, Plan mismatch, and reviewer unavailability. Never convert uncertainty into MERGEABLE.

- [x] **Step 4: Validate GREEN**

  Run targeted contract and `quick_validate.py`.

### Task 10: Complete documentation, attribution, and CI

**Files:**
- Modify: `README.md`
- Create: `THIRD_PARTY_NOTICES.md`
- Create: `.github/workflows/validate-plugin.yml`
- Delete: `skills/task-planning/SKILL.md`
- Delete: `skills/implementation-workflow/SKILL.md`
- Delete: `skills/steps-documentation/SKILL.md`
- Delete: `skills/preparing-commit/SKILL.md`
- Delete: `skills/pr-documentation/SKILL.md`

**Interfaces:**
- Consumes: completed Plugin and Skill layout.
- Produces: installable, understandable repository with no competing v1 triggers.

- [x] **Step 1: Write failing docs and workflow assertions**

  Require local and GitHub marketplace commands, standalone `$skill-installer` paths, mode/risk examples, security warning, development command, independence statement, and third-party notice.

- [x] **Step 2: Verify RED**

  Run the repository contract tests.

- [x] **Step 3: Rewrite README and add notices**

  Explain the real problem, design trade-off, installation surfaces, example prompts, outputs, validation budget, GitHub gates, and Superpowers relationship. Preserve MIT and include Superpowers MIT attribution without claiming copied runtime content.

- [x] **Step 4: Add fast CI**

  Run Python unit/contract tests plus per-Skill `quick_validate.py` or an equivalent vendored-free schema check. Do not run paid model scenarios on every push.

- [x] **Step 5: Remove v1 Skill files**

  Remove the old five trigger definitions after all v2 replacements pass, preventing duplicate workflows.

- [x] **Step 6: Verify GREEN**

  Run the full unittest suite, all Skill validators, and Plugin validator.

### Task 11: Final local verification and handoff

**Files:**
- Modify: `docs/superpowers/plans/2026-08-15-gated-development-v2-implementation.md`

**Interfaces:**
- Consumes: complete local changes and fresh command output.
- Produces: verified working tree and explicit remaining release gates.

- [x] **Step 1: Run fresh full verification**

  Run the unit/contract suite, Plugin validator, per-Skill validator, JSON parsing, YAML metadata checks, placeholder scan, and broken relative-path scan.

- [x] **Step 2: Inspect scope**

  Run `git status --short`, `git diff --stat`, and `git diff --check`. Confirm no secret, cache, temporary output, unrelated file, or remote mutation.

- [x] **Step 3: Update checklist truthfully**

  Mark only actually completed plan steps. Keep local Plugin installation and fresh-context behavioral tests unchecked if they were not executed.

- [x] **Step 4: Hand off without remote write**

  Report the local path, verified commands, remaining smoke/behavior tests, and that no push or GitHub PR was performed.

## Release gates not executed in this local implementation turn

- [ ] Run every pressure scenario without and with the relevant Skill in fresh contexts and preserve raw outputs.
- [ ] Install the repo marketplace in a disposable Codex environment and confirm all seven Skills appear in a new task.
- [ ] Verify orchestrator-to-specialist explicit activation and `allow_implicit_invocation` behavior in the installed host.
- [ ] Install selected standalone Skills through `$skill-installer` in a disposable environment.
- [ ] Observe the GitHub Actions workflow on an actual branch or pull request.
