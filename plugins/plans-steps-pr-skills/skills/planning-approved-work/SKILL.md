---
name: planning-approved-work
description: Use when a development change needs a written implementation plan, unresolved decisions, explicit approval, or a safe boundary before multi-file, R2, or R3 work.
---

# Planning Approved Work

## Core principle

Turn a requested direction into an inspectable Plan contract. Preserve a **Plan-only write boundary** until a user approval message exists and the approved body digest matches the current body.

## Workflow

1. Read repository instructions, Git state, relevant code, contracts, tests, build configuration, CI, and existing document conventions.
2. Separate known facts, assumptions, user decisions, included scope, excluded scope, and the requested completion target.
3. Compare viable approaches only when a real choice exists. Recommend one with impact, risk, compatibility, maintenance, and verification evidence.
4. Classify Risk independently from workflow Mode. Treat dependency, public API, runtime/build, cross-module, and persistence-boundary changes as at least R2. Treat auth, permission, payment, migration, concurrency, and data-loss boundaries as R3.
5. Create the Plan from [assets/plan-template.md](assets/plan-template.md). Follow repository conventions; otherwise use `docs/plans/YYYY-MM-DD-<task-slug>.md`.
6. Run `python scripts/plan_digest.py refresh <plan>` to record the current body digest and enter `AWAITING_APPROVAL`.
7. Present the Plan, decisions, digest, and completion target. Stop without editing source, configuration, tests, Git history, or external systems.

## Approval contract

Accept approval only in this order:

1. Find an explicit **user approval message** that identifies the Plan or its current digest.
2. Recompute the **current digest** from the Plan body.
3. Match it to the digest the user approved.
4. Only then record `approved_digest`, `approved_by`, `approved_at`, and `approval_evidence` and enter `APPROVED`.

Use `python scripts/plan_digest.py approve <plan> --expected-digest <digest> --approved-by user --approved-at <ISO-8601> --approval-evidence <message-reference>` for the deterministic update. File metadata alone never proves approval.

## Material change boundary

Enter `REAPPROVAL_REQUIRED` before making a **material change**:

- public API, storage format, database, or schema change;
- new dependency or external service;
- new module, file area, user impact, security, auth, or permission boundary;
- completion-target change, higher Risk, or reduced verification.

Record internal naming, fixture placement, small implementation details, planned internal refactors, and document wording differences in Steps when they preserve the approved behavior and scope.

## Output contract

Write for a reader who should understand the direction without reading code deeply. Include evidence, decisions, files and interfaces, execution/data flow, ordered implementation, risk, rollback, verification, completion target, and one explicit approval request. Do not invent repository facts or hide uncertainty.

## Red flags

- `state: APPROVED` without a matching user message
- implementation edits while the Plan is awaiting approval
- calling a dependency “one line” to keep QUICK mode
- changing the Plan body after approval and reusing the old digest
- treating unresolved scope as an implementation detail

Any red flag means stop and restore the approval boundary.
