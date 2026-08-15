---
name: publishing-pull-request
description: Use when verified committed work has explicit push and Draft PR authority and needs a consistent reviewer-facing pull request created or updated from the full branch diff.
---

# Publishing Pull Request

## Core principle

Publish the verified branch as a Draft PR and prove what happened. Push authority and PR authority are separate external-write gates.

## Preflight

1. Confirm explicit authority for both push and Draft PR publication from the approved completion target or a current user message.
2. Resolve repository, branch, remote, base branch, upstream, and merge-base. Stop on detached HEAD or ambiguous base.
3. Inspect status. Separate uncommitted staged, unstaged, and untracked files from the committed PR diff; never imply they are in the PR.
4. Compare `merge-base..HEAD` and read the commits, Plan, Steps, and actual verification evidence.
5. Check whether the branch already has a PR. Update it rather than creating a duplicate.
6. Stop for material Plan drift, missing FORMAL Steps, unresolved verification failure, secrets, or unrelated committed work.

## Publish

1. Create the body from [assets/pr-template.md](assets/pr-template.md). Lead with observable results and keep every verification claim tied to a command or CI record.
2. Prefer a connected GitHub capability for structured PR operations. Use authenticated `gh` and local Git only for coverage gaps. If neither is available, produce the exact title, body, and manual commands without claiming success.
3. Push only the authorized branch. Do not force-push unless separately and explicitly authorized after explaining impact.
4. Create a **Draft** PR or update the existing Draft. Preserve human edits that remain correct.
5. Read back the PR URL, number, base, head, Draft state, and displayed body. Report those values as evidence.

## Boundary

Do not request fake success, dismiss failing CI, use GitHub APPROVE, enable auto-merge, or merge. Publication ends in `PR_OPEN` or `BLOCKED`, followed by independent validation.

## Red flags

- treating local commit permission as push permission
- describing working-tree changes as committed PR content
- creating a second PR for the same branch
- using stale test output in the body
- reporting a URL that was never read back
- publishing a ready-for-review PR when only Draft was authorized
