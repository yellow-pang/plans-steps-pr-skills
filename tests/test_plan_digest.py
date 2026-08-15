from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = (
    ROOT
    / "plugins"
    / "plans-steps-pr-skills"
    / "skills"
    / "planning-approved-work"
    / "scripts"
    / "plan_digest.py"
)


def load_module():
    spec = importlib.util.spec_from_file_location("plan_digest", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise AssertionError("unable to load plan_digest module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def plan(body: str, *, state: str = "AWAITING_APPROVAL", approved: str = "null") -> str:
    return (
        "---\n"
        "workflow_id: gdw-20260815-example\n"
        "mode: FORMAL\n"
        f"state: {state}\n"
        "completion_target: IMPLEMENTATION\n"
        "risk: R2\n"
        'plan_digest: "sha256:stale"\n'
        f"approved_digest: {approved}\n"
        "approved_by: null\n"
        "approved_at: null\n"
        "approval_evidence: null\n"
        "---\n"
        f"{body}"
    )


class PlanDigestTest(unittest.TestCase):
    def setUp(self) -> None:
        self.module = load_module()

    def test_digest_ignores_frontmatter(self) -> None:
        first = plan("# 목표\n\n본문\n")
        second = first.replace("risk: R2", "risk: R3")
        self.assertEqual(
            self.module.compute_body_digest(first),
            self.module.compute_body_digest(second),
        )

    def test_digest_normalizes_line_endings(self) -> None:
        lf = plan("# 목표\n\n본문\n")
        crlf = lf.replace("\n", "\r\n")
        self.assertEqual(
            self.module.compute_body_digest(lf),
            self.module.compute_body_digest(crlf),
        )

    def test_digest_changes_when_body_changes(self) -> None:
        first = plan("# 목표\n\n첫 본문\n")
        second = plan("# 목표\n\n다른 본문\n")
        self.assertNotEqual(
            self.module.compute_body_digest(first),
            self.module.compute_body_digest(second),
        )

    def test_refresh_unapproved_plan_clears_stale_approval_fields(self) -> None:
        source = plan("# 목표\n")
        refreshed = self.module.refresh_plan(source)
        digest = self.module.compute_body_digest(source)
        self.assertIn("state: AWAITING_APPROVAL", refreshed)
        self.assertIn(f'plan_digest: "{digest}"', refreshed)
        self.assertIn("approved_digest: null", refreshed)
        self.assertIn("approval_evidence: null", refreshed)

    def test_refresh_changed_approved_plan_requires_reapproval(self) -> None:
        source = plan(
            "# 변경된 목표\n",
            state="APPROVED",
            approved='"sha256:previous"',
        )
        refreshed = self.module.refresh_plan(source)
        self.assertIn("state: REAPPROVAL_REQUIRED", refreshed)
        self.assertIn('approved_digest: "sha256:previous"', refreshed)

    def test_approval_rejects_missing_user_message_evidence(self) -> None:
        source = self.module.refresh_plan(plan("# 목표\n"))
        digest = self.module.compute_body_digest(source)
        with self.assertRaisesRegex(ValueError, "approval evidence"):
            self.module.approve_plan(
                source,
                expected_digest=digest,
                approved_by="user",
                approved_at="2026-08-15T12:00:00+09:00",
                approval_evidence="",
            )

    def test_approval_rejects_digest_mismatch_without_writing_metadata(self) -> None:
        source = self.module.refresh_plan(plan("# 목표\n"))
        with self.assertRaisesRegex(ValueError, "digest mismatch"):
            self.module.approve_plan(
                source,
                expected_digest="sha256:not-current",
                approved_by="user",
                approved_at="2026-08-15T12:00:00+09:00",
                approval_evidence="chat-message:2026-08-15T11:59:00+09:00",
            )
        self.assertNotIn("state: APPROVED", source)

    def test_approval_records_metadata_only_after_evidence_and_match(self) -> None:
        source = self.module.refresh_plan(plan("# 목표\n"))
        digest = self.module.compute_body_digest(source)
        approved = self.module.approve_plan(
            source,
            expected_digest=digest,
            approved_by="user",
            approved_at="2026-08-15T12:00:00+09:00",
            approval_evidence="chat-message:2026-08-15T11:59:00+09:00",
        )
        self.assertIn("state: APPROVED", approved)
        self.assertIn(f'approved_digest: "{digest}"', approved)
        self.assertIn('approved_by: "user"', approved)
        self.assertIn('approved_at: "2026-08-15T12:00:00+09:00"', approved)
        self.assertIn(
            'approval_evidence: "chat-message:2026-08-15T11:59:00+09:00"',
            approved,
        )

    def test_approval_rejects_overwriting_existing_approval(self) -> None:
        source = self.module.refresh_plan(plan("# 목표\n"))
        digest = self.module.compute_body_digest(source)
        approved = self.module.approve_plan(
            source,
            expected_digest=digest,
            approved_by="user",
            approved_at="2026-08-15T12:00:00+09:00",
            approval_evidence="chat-message:2026-08-15T11:59:00+09:00",
        )
        with self.assertRaisesRegex(ValueError, "already approved"):
            self.module.approve_plan(
                approved,
                expected_digest=digest,
                approved_by="user",
                approved_at="2026-08-15T12:01:00+09:00",
                approval_evidence="chat-message:2026-08-15T12:00:30+09:00",
            )

    def test_missing_frontmatter_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "frontmatter"):
            self.module.compute_body_digest("# 목표\n")


if __name__ == "__main__":
    unittest.main()
