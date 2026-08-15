---
name: recording-implementation
description: Use when verified development work needs a readable Steps report that explains actual changes, flow, evidence, Plan differences, limitations, and follow-up work.
---

# Recording Implementation

## Core principle

Record verified results, not remembered effort. A reader should understand what changed and how it works without reading every line of code.

## Evidence order

Use evidence in this order: actual diff; current code and configuration; test output and verification ledger; Git or CI records; approved Plan. Never turn a planned action into a completed fact.

## Workflow

1. Read repository document conventions and identify the exact task diff. Separate unrelated user changes.
2. Gather the approved Plan when present, current interfaces and flow, actual verification ledger, skipped checks, and known limitations.
3. Choose the report depth:
   - QUICK: write Steps only when requested or when the result has durable tracking value.
   - R1 FORMAL exception: use result, before/after, main files, verification, and limitations.
   - R2: use the compact relevant sections from [assets/steps-template.md](assets/steps-template.md).
   - R3: use the full contract from the template.
4. Explain purpose and result first. Use a table for repeated file/contract mappings.
5. Add Mermaid only when three or more components, branches, or state transitions become materially clearer as a diagram.
6. Compare with the Plan only where execution differed. Classify a material difference as requiring reapproval rather than normalizing it in documentation.
7. Follow repository conventions; otherwise save to `docs/steps/YYYY-MM-DD-<task-slug>.md`.

## Truth rules

- Quote commands only when they actually ran; include outcome and scope.
- Label inferences and unverified claims explicitly.
- Distinguish new failures, proven existing failures, environment blocks, and unknown provenance.
- Do not repeat the Plan, narrate every edit chronologically, or expand the report merely to fill a template.
- Do not stage, commit, push, publish, review, or merge from this Skill.

## Quality check

Confirm that the summary matches the diff, every claimed check has evidence, important contracts and flow are visible, empty sections are removed, diagrams pass the complexity threshold, and remaining risk is easy to find.
