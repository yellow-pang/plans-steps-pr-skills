from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "plans-steps-pr-skills"
SKILLS = PLUGIN / "skills"

EXPECTED_SKILLS = {
    "running-gated-development": True,
    "planning-approved-work": True,
    "implementing-with-risk-checks": False,
    "recording-implementation": True,
    "committing-verified-work": False,
    "publishing-pull-request": False,
    "validating-pull-request": True,
}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def frontmatter(markdown: str) -> dict[str, str]:
    lines = markdown.splitlines()
    if not lines or lines[0] != "---":
        raise AssertionError("SKILL.md must start with YAML frontmatter")
    try:
        end = lines.index("---", 1)
    except ValueError as error:
        raise AssertionError("SKILL.md frontmatter is not closed") from error

    result: dict[str, str] = {}
    for line in lines[1:end]:
        if not line.strip():
            continue
        key, separator, value = line.partition(":")
        if not separator:
            raise AssertionError(f"invalid frontmatter line: {line}")
        result[key.strip()] = value.strip().strip('"').strip("'")
    return result


class RepositoryContractTest(unittest.TestCase):
    def test_repo_marketplace_points_to_nested_plugin(self) -> None:
        path = ROOT / ".agents" / "plugins" / "marketplace.json"
        data = json.loads(read(path))
        self.assertEqual(data["name"], "yellow-pang-workflows")
        entry = data["plugins"][0]
        self.assertEqual(entry["name"], "plans-steps-pr-skills")
        self.assertEqual(entry["source"], {
            "source": "local",
            "path": "./plugins/plans-steps-pr-skills",
        })
        self.assertEqual(entry["policy"], {
            "installation": "AVAILABLE",
            "authentication": "ON_INSTALL",
        })

    def test_plugin_manifest_is_skill_only(self) -> None:
        path = PLUGIN / ".codex-plugin" / "plugin.json"
        data = json.loads(read(path))
        self.assertEqual(data["name"], PLUGIN.name)
        self.assertEqual(data["version"], "2.0.0")
        self.assertEqual(data["skills"], "./skills/")
        self.assertEqual(data["license"], "MIT")
        for unsupported in ("hooks", "mcpServers", "apps"):
            self.assertNotIn(unsupported, data)

    def test_exact_skill_set_and_metadata(self) -> None:
        actual = {path.name for path in SKILLS.iterdir() if path.is_dir()}
        self.assertEqual(actual, set(EXPECTED_SKILLS))
        self.assertEqual(
            [name for name, implicit in EXPECTED_SKILLS.items() if implicit],
            [
                "running-gated-development",
                "planning-approved-work",
                "recording-implementation",
                "validating-pull-request",
            ],
        )

        for name, implicit in EXPECTED_SKILLS.items():
            with self.subTest(skill=name):
                skill_dir = SKILLS / name
                metadata = frontmatter(read(skill_dir / "SKILL.md"))
                self.assertEqual(metadata, {
                    "name": name,
                    "description": metadata.get("description", ""),
                })
                self.assertTrue(metadata["description"].startswith("Use when"))
                self.assertLessEqual(len(metadata["description"]), 500)

                openai_yaml = read(skill_dir / "agents" / "openai.yaml")
                self.assertIn(f"$%s" % name, openai_yaml)
                self.assertIn(
                    f"allow_implicit_invocation: {str(implicit).lower()}",
                    openai_yaml,
                )
                short_match = re.search(r'short_description:\s*"([^"]+)"', openai_yaml)
                self.assertIsNotNone(short_match)
                self.assertGreaterEqual(len(short_match.group(1)), 25)
                self.assertLessEqual(len(short_match.group(1)), 64)

    def test_orchestrator_gate_contract(self) -> None:
        text = read(SKILLS / "running-gated-development" / "SKILL.md")
        for phrase in (
            "Mode is not Risk",
            "DISCUSS",
            "QUICK",
            "FORMAL",
            "R2",
            "R3",
            "explicit approval",
            "REAPPROVAL_REQUIRED",
            "Never merge",
        ):
            self.assertIn(phrase, text)

    def test_orchestrator_has_compact_route_only_contract(self) -> None:
        text = read(SKILLS / "running-gated-development" / "SKILL.md")
        metadata = frontmatter(text)
        self.assertEqual(
            metadata["description"],
            "Use when a user asks to change, implement, plan, verify, commit, publish, "
            "or review software.",
        )
        expected_lines = (
            "Mode: <DISCUSS | QUICK | FORMAL>",
            "Risk: <R0 | R1 | R2 | R3>",
            "Next skill: <none | planning-approved-work | implementing-with-risk-checks | "
            "recording-implementation | committing-verified-work | publishing-pull-request | "
            "validating-pull-request>",
            "Decision: <one sentence describing the allowed next action>",
        )
        for line in expected_lines:
            self.assertIn(line, text)

        self.assertIn(
            "For a routing-only response, return this four-line decision block:",
            text,
        )
        self.assertNotIn("Return exactly four lines", text)
        self.assertLess(text.index("## Output contract"), text.index("## Route"))
        self.assertLessEqual(len(text.split()), 300)

        referenced_skills = set(re.findall(r"\$([a-z0-9-]+)", text))
        self.assertLessEqual(referenced_skills, set(EXPECTED_SKILLS))

        for phrase in (
            "| `R0` |",
            "| `R1` |",
            "| `R2` |",
            "| `R3` |",
            "dependency, public API",
            "authentication, authorization",
        ):
            self.assertIn(phrase, text)

    def test_planning_approval_contract(self) -> None:
        text = read(SKILLS / "planning-approved-work" / "SKILL.md")
        for phrase in (
            "user approval message",
            "current digest",
            "approved_digest",
            "approved_by",
            "approved_at",
            "material change",
            "Plan-only write boundary",
        ):
            self.assertIn(phrase, text)

    def test_implementation_verification_contract(self) -> None:
        text = read(SKILLS / "implementing-with-risk-checks" / "SKILL.md")
        policy = read(
            SKILLS
            / "implementing-with-risk-checks"
            / "references"
            / "verification-policy.md"
        )
        self.assertIn("verification ledger", text)
        for phrase in (
            "same HEAD",
            "dependency",
            "unknown provenance",
            "R0",
            "R1",
            "R2",
            "R3",
        ):
            self.assertIn(phrase, policy)

    def test_document_and_delivery_contracts(self) -> None:
        steps = read(
            SKILLS / "recording-implementation" / "assets" / "steps-template.md"
        )
        commit = read(
            SKILLS / "committing-verified-work" / "assets" / "commit-template.md"
        )
        pr = read(SKILLS / "publishing-pull-request" / "assets" / "pr-template.md")
        reviewer = read(SKILLS / "validating-pull-request" / "SKILL.md")

        self.assertIn("R2 compact", steps)
        self.assertIn("R3 full", steps)
        self.assertIn("Verification ledger", steps)
        self.assertIn("Do not repeat empty sections", steps)
        self.assertIn("Explicitly staged paths", commit)
        self.assertIn("Verification", commit)
        for heading in (
            "Summary",
            "Background",
            "Main changes",
            "Flow",
            "Impact",
            "Verification",
            "Review focus",
            "Risk and rollback",
            "Plan and Steps",
        ):
            self.assertIn(heading, pr)
        self.assertIn("R3 requires fresh context", reviewer)
        self.assertIn("Do not use GitHub APPROVE", reviewer)
        self.assertIn("Never merge", reviewer)

    def test_recording_template_contract(self) -> None:
        steps = read(
            SKILLS / "recording-implementation" / "assets" / "steps-template.md"
        )
        self.assertIn("R2 compact", steps)
        self.assertIn("R3 full", steps)
        self.assertIn("Verification ledger", steps)
        self.assertIn("Do not repeat empty sections", steps)

    def test_commit_template_contract(self) -> None:
        commit = read(
            SKILLS / "committing-verified-work" / "assets" / "commit-template.md"
        )
        self.assertIn("Explicitly staged paths", commit)
        self.assertIn("Verification", commit)

    def test_pull_request_template_contract(self) -> None:
        pr = read(SKILLS / "publishing-pull-request" / "assets" / "pr-template.md")
        for heading in (
            "Summary",
            "Background",
            "Main changes",
            "Flow",
            "Impact",
            "Verification",
            "Review focus",
            "Risk and rollback",
            "Plan and Steps",
        ):
            self.assertIn(heading, pr)

    def test_pressure_scenarios_cover_high_risk_loopholes(self) -> None:
        text = read(ROOT / "tests" / "scenarios" / "workflow-pressure-cases.yaml")
        for scenario_id in (
            "discuss-does-not-mutate",
            "quick-r2-escalates",
            "oauth-auth-api-explicit-contract",
            "oauth-auth-api-implicit-discovery",
            "approval-message-before-metadata",
            "dependency-needs-reapproval",
            "same-head-regression-not-repeated",
            "unknown-failure-is-not-success",
            "unrelated-files-not-staged",
            "unauthorized-pr-is-not-claimed",
            "r3-requires-fresh-review",
            "never-auto-merge",
        ):
            self.assertIn(f"id: {scenario_id}", text)

    def test_repository_docs_and_ci_contract(self) -> None:
        readme = read(ROOT / "README.md")
        notice = read(ROOT / "THIRD_PARTY_NOTICES.md")
        workflow = read(ROOT / ".github" / "workflows" / "validate-plugin.yml")

        for phrase in (
            "DISCUSS",
            "QUICK",
            "FORMAL",
            "R0",
            "R3",
            "codex plugin marketplace add",
            "$skill-installer",
            "docs/steps/2026-08-15-gated-development-v2.md",
            "pull_request_target",
            "not affiliated with the Superpowers project",
        ):
            self.assertIn(phrase, readme)
        self.assertIn("obra/superpowers", notice)
        self.assertIn("MIT License", notice)
        self.assertIn("python -m unittest", workflow)

    def test_v2_steps_explains_implementation_and_release_gates(self) -> None:
        path = ROOT / "docs" / "steps" / "2026-08-15-gated-development-v2.md"
        self.assertTrue(path.is_file(), "v2 implementation record is missing")
        text = read(path)
        for phrase in (
            "한눈에 보기",
            "전체 흐름",
            "7개 Skill",
            "Plan digest",
            "패키지 구조",
            "완료된 검증",
            "미완료 Release Gate",
            "권장 다음 단계",
            "BLOCKED_ENVIRONMENT",
        ):
            self.assertIn(phrase, text)

    def test_v1_skills_are_removed(self) -> None:
        for name in (
            "task-planning",
            "implementation-workflow",
            "steps-documentation",
            "preparing-commit",
            "pr-documentation",
        ):
            self.assertFalse((ROOT / "skills" / name / "SKILL.md").exists())

    def test_no_placeholders_or_broken_local_markdown_links(self) -> None:
        tracked_roots = [PLUGIN, ROOT / "README.md", ROOT / "THIRD_PARTY_NOTICES.md"]
        markdown_files: list[Path] = []
        for target in tracked_roots:
            if target.is_file():
                markdown_files.append(target)
            elif target.exists():
                markdown_files.extend(target.rglob("*.md"))

        placeholder = re.compile(r"\b(?:TBD|TODO)\b|\[TODO:", re.IGNORECASE)
        link_pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
        for path in markdown_files:
            with self.subTest(file=str(path.relative_to(ROOT))):
                text = read(path)
                self.assertIsNone(placeholder.search(text))
                for raw_target in link_pattern.findall(text):
                    target = raw_target.split("#", 1)[0]
                    if not target or "://" in target or target.startswith("mailto:"):
                        continue
                    self.assertTrue(
                        (path.parent / target).resolve().exists(),
                        f"broken local link {raw_target!r}",
                    )


if __name__ == "__main__":
    unittest.main()
