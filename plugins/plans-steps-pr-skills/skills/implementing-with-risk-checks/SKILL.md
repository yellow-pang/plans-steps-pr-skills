---
name: implementing-with-risk-checks
description: Use when implementing an explicitly approved FORMAL Plan or a clearly bounded QUICK R0/R1 change that needs proportionate tests and regression evidence.
---

# Implementing With Risk Checks

## Core principle

Implement only the verified contract and produce current evidence at the lowest safe cost. Read [references/verification-policy.md](references/verification-policy.md) before selecting checks.

## Preflight gate

1. Read repository instructions, Git status, relevant source, test configuration, CI, and user-owned changes.
2. For FORMAL work, require a user approval message, `state: APPROVED`, and equal `plan_digest` and `approved_digest`. Stop otherwise.
3. For QUICK work, confirm the request is both R0/R1 and bounded. Escalate dependency, public contract, runtime/build, persistence, cross-module, security, auth, migration, or data-loss work to FORMAL.
4. Restate included scope, excluded scope, completion target, Risk, and the first affected check.

## Execution loop

1. Identify one observable behavior or document/metadata contract.
2. For new behavior or a reproducible bug, write the smallest test that fails for the intended reason before implementation. For non-code files, first run the relevant schema, link, render, or contract check and observe RED.
3. Make the minimum change that satisfies the contract. Preserve unrelated work and existing architecture unless the approved Plan changes it.
4. Run the failed check, then directly affected checks. Record each command and result in the **verification ledger**.
5. If a relevant failure appears, determine whether the change caused it. Do not hide, weaken, delete, or rewrite a correct test merely to obtain GREEN.
6. Reinspect the diff and approval boundary. Stop with `REAPPROVAL_REQUIRED` before any material change.
7. Repeat by behavior. Do not commit, push, publish a PR, or write success-only documentation from this Skill.

## Completion evidence

Report the purpose, actual change, ledger entries, skipped checks and reasons, existing failures, unknown failures, and remaining risk. A test file or CI configuration proves only that a check exists, not that it passed.

## Red flags

- “It is one line” used to downgrade R2
- a test that never failed before production behavior changed
- repeated slow full regression without invalidated evidence
- unknown failure origin reported as an existing failure
- scope expansion described as cleanup
- success claimed from stale output or a different HEAD

Stop and restore the correct gate when any red flag appears.
