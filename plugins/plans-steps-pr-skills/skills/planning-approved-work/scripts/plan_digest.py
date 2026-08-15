#!/usr/bin/env python3
"""Compute and record approval-bound SHA-256 digests for Markdown Plans."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


REQUIRED_APPROVAL_FIELDS = (
    "approved_digest",
    "approved_by",
    "approved_at",
    "approval_evidence",
)


def _normalize(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def _parse_scalar(value: str) -> Any:
    stripped = value.strip()
    if stripped == "null":
        return None
    if stripped in {"true", "false"}:
        return stripped == "true"
    if stripped.startswith('"'):
        try:
            return json.loads(stripped)
        except json.JSONDecodeError as error:
            raise ValueError("frontmatter contains an invalid quoted value") from error
    return stripped


def _dump_scalar(key: str, value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if key in {"workflow_id", "mode", "state", "completion_target", "risk"}:
        return str(value)
    return json.dumps(str(value), ensure_ascii=False)


def _split_plan(text: str) -> tuple[dict[str, Any], str]:
    normalized = _normalize(text)
    if not normalized.startswith("---\n"):
        raise ValueError("Plan must start with YAML frontmatter")
    closing = normalized.find("\n---\n", 4)
    if closing == -1:
        raise ValueError("Plan frontmatter is not closed")

    metadata: dict[str, Any] = {}
    for line in normalized[4:closing].split("\n"):
        if not line.strip():
            continue
        key, separator, value = line.partition(":")
        if not separator or not key.strip():
            raise ValueError(f"invalid frontmatter line: {line}")
        metadata[key.strip()] = _parse_scalar(value)
    return metadata, normalized[closing + len("\n---\n") :]


def _render_plan(metadata: dict[str, Any], body: str) -> str:
    lines = ["---"]
    lines.extend(
        f"{key}: {_dump_scalar(key, value)}" for key, value in metadata.items()
    )
    lines.append("---")
    return "\n".join(lines) + "\n" + body


def compute_body_digest(text: str) -> str:
    """Return the SHA-256 digest of the LF-normalized body, excluding frontmatter."""
    _, body = _split_plan(text)
    digest = hashlib.sha256(body.encode("utf-8")).hexdigest()
    return f"sha256:{digest}"


def refresh_plan(text: str) -> str:
    """Refresh the body digest and derive approval state without inventing approval."""
    metadata, body = _split_plan(text)
    digest = f"sha256:{hashlib.sha256(body.encode('utf-8')).hexdigest()}"
    approved_digest = metadata.get("approved_digest")

    metadata["plan_digest"] = digest
    if approved_digest:
        metadata["state"] = (
            "APPROVED" if approved_digest == digest else "REAPPROVAL_REQUIRED"
        )
    else:
        metadata["state"] = "AWAITING_APPROVAL"
        for field in REQUIRED_APPROVAL_FIELDS:
            metadata[field] = None
    return _render_plan(metadata, body)


def approve_plan(
    text: str,
    *,
    expected_digest: str,
    approved_by: str,
    approved_at: str,
    approval_evidence: str,
) -> str:
    """Record approval only after explicit evidence and an exact current digest match."""
    metadata, body = _split_plan(text)
    if metadata.get("state") == "APPROVED" or metadata.get("approved_digest"):
        raise ValueError("Plan is already approved; do not overwrite approval evidence")
    if not approval_evidence.strip():
        raise ValueError("explicit user approval evidence is required")
    if not approved_by.strip() or not approved_at.strip():
        raise ValueError("approved_by and approved_at are required")

    current_digest = f"sha256:{hashlib.sha256(body.encode('utf-8')).hexdigest()}"
    if current_digest != expected_digest:
        raise ValueError(
            f"digest mismatch: expected {expected_digest}, current {current_digest}"
        )

    metadata["state"] = "APPROVED"
    metadata["plan_digest"] = current_digest
    metadata["approved_digest"] = current_digest
    metadata["approved_by"] = approved_by
    metadata["approved_at"] = approved_at
    metadata["approval_evidence"] = approval_evidence
    return _render_plan(metadata, body)


def _write_lf(path: Path, content: str) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as stream:
        stream.write(content)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)

    for name in ("digest", "refresh"):
        command = commands.add_parser(name)
        command.add_argument("plan", type=Path)

    approve = commands.add_parser("approve")
    approve.add_argument("plan", type=Path)
    approve.add_argument("--expected-digest", required=True)
    approve.add_argument("--approved-by", required=True)
    approve.add_argument("--approved-at", required=True)
    approve.add_argument("--approval-evidence", required=True)
    return parser


def main() -> None:
    args = _parser().parse_args()
    source = args.plan.read_text(encoding="utf-8")
    if args.command == "digest":
        print(compute_body_digest(source))
        return
    if args.command == "refresh":
        _write_lf(args.plan, refresh_plan(source))
        print(compute_body_digest(args.plan.read_text(encoding="utf-8")))
        return

    updated = approve_plan(
        source,
        expected_digest=args.expected_digest,
        approved_by=args.approved_by,
        approved_at=args.approved_at,
        approval_evidence=args.approval_evidence,
    )
    _write_lf(args.plan, updated)
    print(args.expected_digest)


if __name__ == "__main__":
    main()
