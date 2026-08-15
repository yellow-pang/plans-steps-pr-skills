---
name: running-gated-development
description: Use when a user asks to change, implement, plan, verify, commit, publish, or review software.
---

# Running Gated Development

## Core principle

Select one Mode, one Risk, and one bundled specialist. **Mode is not Risk**.

## Output contract

For a routing-only response, return this four-line decision block:

```text
Mode: <DISCUSS | QUICK | FORMAL>
Risk: <R0 | R1 | R2 | R3>
Next skill: <none | planning-approved-work | implementing-with-risk-checks | recording-implementation | committing-verified-work | publishing-pull-request | validating-pull-request>
Decision: <one sentence describing the allowed next action>
```

## Classify

| Mode | Condition |
|---|---|
| `DISCUSS` | No change requested |
| `QUICK` | Contained R0/R1 change |
| `FORMAL` | Any R2/R3 or PR target |

| Risk | Boundary |
|---|---|
| `R0` | Documentation or behavior-neutral metadata |
| `R1` | Isolated behavior or reproducible bug |
| `R2` | dependency, public API, runtime/build, persistence, multiple modules |
| `R3` | authentication, authorization, payment, migration, concurrency, security, data loss |

Use the highest Risk. R2/R3 always means FORMAL, even when called QUICK.

## Route

1. Inspect the request, Git state, Plan digest, authority, and completion target.
2. DISCUSS is read-only with `Next skill: none`; QUICK uses `$implementing-with-risk-checks`.
3. FORMAL without an **explicit approval** message and matching `approved_digest` uses `$planning-approved-work` and does not implement. APPROVED metadata alone is insufficient.
4. Approved FORMAL uses `$implementing-with-risk-checks`; verified FORMAL uses `$recording-implementation`.
5. Use `$committing-verified-work`, `$publishing-pull-request`, or `$validating-pull-request` only when state and authority require it. Reinspect state afterward.

Use `REAPPROVAL_REQUIRED` for material scope or digest changes, `BLOCKED` for missing authority or tooling, `CHANGES_REQUIRED` for defects, and `REVIEW_REQUIRED` for missing evidence. Never convert uncertainty into success. **Never merge**.

Supporting test, debug, or review techniques do not own these gates.
