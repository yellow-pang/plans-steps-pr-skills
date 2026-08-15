---
name: committing-verified-work
description: Use when a user explicitly requests local commits or an approved FORMAL completion target includes COMMIT, PUSH, or DRAFT_PR after implementation verification.
---

# Committing Verified Work

## Core principle

Create an intentional local commit from verified task changes only. Uncommitted files do not imply commit authority.

## Authority and evidence gate

1. Confirm a current user message or approved completion target authorizes a local commit.
2. Require successful affected verification for the exact current diff, plus Steps for FORMAL work.
3. Read repository commit conventions. Use Conventional Commit with concise Korean details only when no stronger convention exists.
4. Stop if the diff contains unresolved failures, unknown provenance, material scope drift, conflict markers, or unclear ownership.

## Select the commit

1. Inspect `git status --short` and separate staged, unstaged, and untracked changes.
2. Screen paths for credentials, tokens, keys, certificates, environment files, dumps, and generated secrets before showing content. Report risky paths without exposing values.
3. Inspect staged and unstaged diffs separately. Inspect an untracked file only when its path, type, size, and task relationship make that safe and necessary.
4. Group changes by one purpose that can be reviewed and reverted independently. Split implementation, refactor, docs, test, build, and CI purposes when they are independently reversible.
5. Stage exact task paths with `git add -- <path>`. Never use a broad catch-all when unrelated changes exist. For a partially related file, stage only the intended hunk or ask for direction.
6. Reinspect `git diff --cached`, status, secret risk, and the verification evidence invalidated by the final staged content.

## Commit and report

Use [assets/commit-template.md](assets/commit-template.md) for the message shape. Commit only after the staged diff matches one message. Report commit SHA, subject, explicit paths, verification evidence, and remaining unstaged/untracked work.

Do not push, publish a PR, alter unrelated staging, amend an existing commit, or rewrite history unless separately authorized. A failed commit remains uncommitted; never claim success from the message text alone.

## Red flags

- “Commit everything” inferred from a completion report
- broad staging in a dirty worktree
- secret values printed for inspection
- one message forced over unrelated staged purposes
- verification copied from a different diff
- push treated as part of local commit authority
