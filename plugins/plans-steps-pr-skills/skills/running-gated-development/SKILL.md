---
name: running-gated-development
description: Use when a request spans planning, implementation, verification, implementation records, commits, Draft PR publication, or PR validation and needs one controlled workflow.
---

# Running Gated Development

## Core principle

Select one workflow state and one specialist at a time. **Mode is not Risk**: Mode controls workflow cost; Risk controls safety evidence.

## Classify the request

| Mode | Observable condition | Mutation boundary |
|---|---|---|
| `DISCUSS` | The user asks how, why, what exists, or which direction without requesting a change | Read-only investigation and answer |
| `QUICK` | A clear, contained R0/R1 change with no public, dependency, runtime, persistence, security, or cross-module boundary | Implement and run affected checks; Plan and Steps are optional |
| `FORMAL` | R2/R3, multiple modules, design choice, dependency, public contract, runtime/build, database, auth, migration, or PR target | Require an approved Plan and Steps |

Honor an explicit Mode only when it does not weaken safety. Escalate any R2/R3 QUICK request to FORMAL and explain the trigger.

## Route by verified state

1. Inspect the user request, repository state, applicable instructions, Plan metadata, current digest, Git state, and requested completion target.
2. For planning or an unmet FORMAL gate, explicitly use `$planning-approved-work`.
3. Enter FORMAL implementation only after an **explicit approval** user message and matching `approved_digest`. A file that merely says APPROVED is insufficient.
4. For implementation, explicitly use `$implementing-with-risk-checks` and stop at the approved scope.
5. After FORMAL verification, explicitly use `$recording-implementation` before commit.
6. Use `$committing-verified-work` only when the completion target or a new user message authorizes local commit.
7. Use `$publishing-pull-request` only when push and Draft PR are authorized.
8. Use `$validating-pull-request` for evidence-first review. Preserve reviewer independence.
9. Reinspect state after every specialist; do not assume its outcome.

## Stop states

- Use `REAPPROVAL_REQUIRED` when the body digest changes or a material change is needed.
- Use `BLOCKED` when authority, tooling, environment, or external state prevents the next approved action.
- Use `CHANGES_REQUIRED` when verification or review finds a relevant defect.
- Use `REVIEW_REQUIRED` while required independent evidence is absent.

Never convert uncertainty into success. Never claim a commit, push, PR, CI result, review, or merge without current evidence. **Never merge**, even after reporting `MERGEABLE`.

## Guard against competing workflows

Do not run another end-to-end development orchestrator on the same change. Individual testing, debugging, or review techniques may support a specialist, but this Skill owns mode, approval, completion target, and state transitions.

## Quick reference

| Current condition | Next action |
|---|---|
| Question only | DISCUSS and answer read-only |
| QUICK R0/R1 | Implement, affected verification, report |
| FORMAL without approval | Plan and wait |
| Approved digest matches | Implement with risk checks |
| Material change | Stop for reapproval |
| Verified FORMAL work | Record Steps |
| Commit authorized | Commit verified paths only |
| Draft PR authorized | Push and publish Draft PR |
| R3 without fresh reviewer | Keep REVIEW_REQUIRED |
