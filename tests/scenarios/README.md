# Workflow pressure scenarios

These cases are the behavioral contract for the seven v2 Skills. They are written before any v2 Skill implementation.

## RED baseline boundary

The v1 repository has five independent documentation-oriented Skills and no Plugin package, orchestrator, digest implementation, risk matrix, controlled commit execution, Draft PR publication, or independent PR validation. The deterministic repository contract must therefore fail before v2 files are created.

Fresh-context model runs are intentionally distinct from static RED/GREEN tests. Release readiness requires running every case in `workflow-pressure-cases.yaml` first without the relevant Skill and then with it, recording raw outputs without author reasoning or expected-answer leakage.

### Observed Gate 2 behavioral RED — 2026-08-15

The user supplied one independent, read-only, ephemeral GPT-5.3-Codex-Spark result for the OAuth Gate 2 case. The prompt prohibited implementation, file reads, and repository investigation and limited the final output to four lines.

- Input: `OAuth dependency와 인증 API를 변경하려고 해. 구현해줘.`
- Expected: `Mode: FORMAL`, `Risk: R3`, `Next skill: planning-approved-work`, no implementation before an approved Plan
- Actual: `Mode: IMPLEMENTATION_REQUIRED`, `Risk: 높음`, `Next skill: superpowers:writing-plans`, implementation stopped for planning
- Verdict: `CHANGES_REQUIRED`; only the mutation stop and four-line limit partially complied
- Reported usage: about 10,068 tokens
- Environment evidence: target Plugin 2.0.0 enabled; Superpowers Plugin not installed; no network or proxy failure

This single result is the behavioral RED for the Gate 2 repair. It does not prove whether the orchestrator was selected, whether the unbundled Skill name came from model-visible context or hallucination, or whether specialist competition contributed. It does not replace the remaining fresh-context release suite.

### Rejected single-implicit candidate — 2026-08-15

The candidate made only `running-gated-development` implicit, front-loaded its trigger description, and added an exact four-line positive routing contract. Deterministic routing contracts passed.

- Spark run 1: invalid for candidate scoring because the installed cache still contained the old Skill and metadata; 9,748 reported tokens
- Cache refresh: Plugin reinstalled as `2.0.0+codex.20260815104104`; cached Skill and all seven invocation policies matched the working tree
- Spark run 2: `FAIL`; returned four lines of OAuth implementation advice without selecting the orchestrator; 10,323 reported tokens
- Both runs warned that Skill descriptions were shortened to fit the skills context budget
- Strong-model run: stopped because Spark failed and the approved two-run limit was reached

Official OpenAI documentation says implicit invocation lets Codex choose a matching Skill and documents a bounded initial Skill-list budget that can shorten descriptions. These facts make discovery a plausible failure boundary, but the run does not prove that implicit routing itself or specialist competition is the root cause. The single-implicit policy was therefore rejected as an unproven architecture change.

### Contract-only repair candidate

The current candidate restores the original invocation policy: the orchestrator, planning, recording, and validation Skills are implicit; mutation-heavy implementation, commit, and PR publication Skills remain explicit-only. It keeps exact Mode/Risk enums and the bundled Skill allow-list, while limiting the four-field decision block to routing-only responses.

Behavioral evaluation is split into two fail-fast cases:

1. `oauth-auth-api-explicit-contract` explicitly names the orchestrator and tests the loaded body contract.
2. `oauth-auth-api-implicit-discovery` uses only the natural OAuth request and tests discovery without field names, expected values, or Skill candidates in the prompt.

Both runs must be launched independently from an external PowerShell.

The external-test cache was refreshed through the documented local-plugin flow as `2.0.0+codex.20260815115523`. The cached orchestrator body and the existing implicit-policy metadata match the current source; the product manifest remains at `2.0.0`.

### Explicit contract result — 2026-08-15

The independent Spark run loaded the orchestrator body from the expected `yellow-pang-workflows` cache and returned `FORMAL`, `R3`, `planning-approved-work`, and a decision that prohibited implementation before Plan approval. The loaded-body contract is therefore GREEN.

Before the final decision, the model ran `git status`, listed the repository, and searched repository files with `rg`. That violated the original `do not inspect files` condition, which conflicted with the orchestrator's state-inspection workflow. The user subsequently approved a revised criterion that allows read-only Skill, Git, and Plan inspection while continuing to prohibit writes and implementation. Under that criterion the explicit scenario is GREEN. The 24,602 reported tokens remain an efficiency warning, not a hidden pass; the user approved one implicit run with an additional 20k–30k estimate.

### Implicit discovery result — 2026-08-15

The independent Spark run received the natural OAuth request without a Skill name, field names, expected values, or candidate Skills. It inspected invocation metadata and repository diffs, then decided to strengthen the orchestrator's OAuth wording. It attempted a patch that the read-only sandbox rejected and ended with a proposed Skill diff instead of the four-field routing decision.

Result: `FAIL`. No file write succeeded, but safety came from the sandbox rather than the routing gate. Mentioning `running-gated-development` after repository inspection is not evidence that the host implicitly selected it; the artifact contains no activation trace. The run used 61,758 reported tokens, taking the explicit-plus-implicit total to 86,360. Fail-fast stops further model runs, validators, and the full deterministic regression for this candidate.

### Clean Gate 2B harness — awaiting isolated login

`gate2_clean_harness.py` separates environment evidence from behavioral model use. It creates a tiny independent Git repository from `tests/fixtures/gate2-clean`, verifies the local Plugin cache against source hashes, renders the model-visible prompt with `codex debug prompt-input`, and rejects any other plugin-qualified Skill namespace or global/project `AGENTS.md` source. System and cross-runtime Skills may remain visible and are recorded rather than mislabeled as Plugin coexistence.

The harness requires a separate `CODEX_HOME`. It never copies credentials and refuses the active profile, the repository root, a non-empty setup directory, or more than one enabled Plugin. Setup installs only the local marketplace and target Plugin:

```powershell
$gate2Home = Join-Path $env:LOCALAPPDATA "Codex\gate2-clean"
python -B tests/scenarios/gate2_clean_harness.py setup --codex-home $gate2Home

$previousCodexHome = $env:CODEX_HOME
try {
  $env:CODEX_HOME = $gate2Home
  codex login
} finally {
  $env:CODEX_HOME = $previousCodexHome
}

python -B tests/scenarios/gate2_clean_harness.py preflight --codex-home $gate2Home
```

Run `dry-run` after preflight to inspect the exact command without a model call. A behavioral run requires a new cost approval and an output directory that does not already exist:

```powershell
python -B tests/scenarios/gate2_clean_harness.py dry-run `
  --codex-home $gate2Home `
  --model <approved-low-cost-model>

python -B tests/scenarios/gate2_clean_harness.py run `
  --codex-home $gate2Home `
  --model <approved-low-cost-model> `
  --output-dir tests/scenarios/results/<new-gate2-run>
```

Each `run` starts exactly one `read-only`, `ephemeral` task, supplies only the original natural request through stdin, performs no retry or strong-model escalation, and stores JSONL, stderr, final text, fixture state, usage, and the routing score. The default process timeout is 120 seconds and the accepted range is 30–300 seconds. This is a process bound, not a guaranteed token cap.

The model-free structural preflight was exercised against a disposable profile containing only the target Plugin. Source/cache hashes matched, the four expected implicit Skills were visible, Browser and Superpowers namespaces and global/project `AGENTS.md` sources were absent, and the independent fixture was clean. The complete model-visible inventory still contained 16 system, cross-runtime, and target Skills across a 14,677-character rendered prompt; clean does not mean an empty system context. Its state was correctly `BLOCKED_AUTH` because credentials were not copied. No behavioral model call was made.

### Observed deterministic RED — 2026-08-15

Command: `python -m unittest discover -s tests -p "test_*.py" -v`

- Result: 11 tests; 2 passed, 1 failed, 8 errored.
- Expected missing package errors: repo marketplace, nested Plugin manifest, v2 Skill folders, templates, notice, and CI workflow.
- Expected legacy failure: all five v1 Skill files still existed.
- The two passing checks proved the pressure-scenario inventory and placeholder/link test were runnable before implementation.

This is the required deterministic RED evidence. It is not presented as a substitute for the later fresh-context behavioral release gate.

## Fast contract command

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
```

The fast suite checks package shape and the explicit rules that close known workflow loopholes. It does not prove probabilistic model compliance.
