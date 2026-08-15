# Verification policy

Use the highest applicable Risk. Risk measures failure impact; Mode measures workflow cost.

## Risk matrix

| Risk | Examples | Development checks | Final boundary |
|---:|---|---|---|
| R0 | documentation, comments, static copy, behavior-neutral metadata | schema, syntax, links, render, or exact affected contract | affected check only |
| R1 | isolated feature, UI behavior, ordinary reproducible bug | behavior RED→GREEN and affected module checks | affected module suite once |
| R2 | public API, dependency, multiple modules, persistence boundary, runtime/build configuration | targeted unit/integration, type, and build checks | slow full validation normally once in final CI |
| R3 | authentication, authorization, payment, security, migration, concurrency, data loss | boundary, error, regression, and relevant integration checks | repository full regression, CI, and independent review |

Never downgrade because the diff is short. A one-line dependency or permission change keeps its real Risk.

## TDD boundary

- Test an observable behavior, regression, contract, or failure mode; do not require one test per private function.
- Use format validation rather than artificial code tests for documentation and metadata.
- If automation is not practical, state the manual or analytical substitute and the residual risk in the approved Plan and final ledger.
- Do not add generic abstractions, extension points, or unrelated refactors for hypothetical tests.

## Regression evidence reuse

Reuse a passing command only when it ran on the **same HEAD**, same relevant environment, and equivalent inputs. Invalidate it when source, dependency lock, generated output, configuration, environment, or test selection affecting that command changes.

During a fix loop, rerun the failed and directly affected checks. Do not repeat a slow full suite after every small edit. Run it at the final boundary required by Risk, repository policy, CI, or a concrete local-reproduction need.

## Failure provenance

Classify a failure as caused by the change, proven pre-existing, environmental/external, or **unknown provenance**. Evidence is required for the first three. Unknown provenance is not success and keeps the work in VERIFYING or BLOCKED.

## Verification ledger

Record one row per meaningful execution.

| Field | Required content |
|---|---|
| command | exact command or deterministic operation |
| result | exit status and pass/fail/blocked summary |
| HEAD | Git SHA, or `working-tree` with diff identity when no commit exists |
| environment | local/CI and relevant runtime or platform |
| executed_at | ISO-8601 timestamp |
| scope | behavior, module, or suite covered |
| provenance | current change, pre-existing, environment, or unknown |

Do not copy a command into the ledger unless it actually ran.
