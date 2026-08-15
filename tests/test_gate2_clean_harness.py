from __future__ import annotations

import importlib.util
import json
import unittest
import uuid
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tests" / "scenarios" / "gate2_clean_harness.py"
FIXTURE = ROOT / "tests" / "fixtures" / "gate2-clean"


def load_module():
    spec = importlib.util.spec_from_file_location("gate2_clean_harness", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise AssertionError("unable to load gate2 clean harness")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Gate2CleanHarnessTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.module = load_module()

    def test_plugin_inventory_rejects_another_enabled_plugin(self) -> None:
        payload = {
            "installed": [
                {
                    "pluginId": self.module.TARGET_PLUGIN_ID,
                    "installed": True,
                    "enabled": True,
                    "version": "2.0.0",
                    "source": {"path": str(self.module.PLUGIN_SOURCE)},
                },
                {
                    "pluginId": "browser@openai-bundled",
                    "installed": True,
                    "enabled": True,
                    "version": "1.0.0",
                    "source": {"path": "C:/plugins/browser"},
                },
            ]
        }

        with self.assertRaisesRegex(self.module.PreflightError, "browser"):
            self.module.validate_plugin_inventory(payload)

    def test_visible_skills_allow_only_target_plugin_namespace(self) -> None:
        prompt = """<skills_instructions>
- imagegen: system skill
- plans-steps-pr-skills:planning-approved-work: planner
- plans-steps-pr-skills:recording-implementation: recorder
- plans-steps-pr-skills:running-gated-development: orchestrator
- plans-steps-pr-skills:validating-pull-request: reviewer
</skills_instructions>"""

        skills = self.module.validate_visible_skills(prompt)

        self.assertEqual(
            [skill for skill in skills if skill.startswith("plans-steps-pr-skills:")],
            list(self.module.EXPECTED_IMPLICIT_SKILLS),
        )

    def test_visible_skills_reject_another_plugin_namespace(self) -> None:
        prompt = """<skills_instructions>
- plans-steps-pr-skills:planning-approved-work: planner
- plans-steps-pr-skills:recording-implementation: recorder
- plans-steps-pr-skills:running-gated-development: orchestrator
- plans-steps-pr-skills:validating-pull-request: reviewer
- browser:control-in-app-browser: browser
</skills_instructions>"""

        with self.assertRaisesRegex(self.module.PreflightError, "browser"):
            self.module.validate_visible_skills(prompt)

    def test_exec_command_is_single_read_only_unhinted_task(self) -> None:
        command = self.module.build_exec_command(
            codex="codex",
            model="gpt-5.3-codex-spark",
            fixture=Path("C:/fixture"),
        )

        self.assertEqual(command.count("exec"), 1)
        self.assertIn("read-only", command)
        self.assertIn("--ephemeral", command)
        self.assertIn("--json", command)
        self.assertIn("never", command)
        self.assertEqual(command[-1], "-")
        self.assertNotIn("--output-schema", command)
        rendered = " ".join(command)
        for leaked_answer in ("FORMAL", "R3", "planning-approved-work"):
            self.assertNotIn(leaked_answer, rendered)

    def test_preflight_rejects_agents_instruction_sources(self) -> None:
        root = ROOT / "tests" / f".gate2-instructions-{uuid.uuid4().hex}"
        codex_home = root / "home"
        fixture = root / "repo"
        codex_home.mkdir(parents=True)
        fixture.mkdir()
        (codex_home / "AGENTS.md").write_text("# injected", encoding="utf-8")
        try:
            with self.assertRaisesRegex(self.module.PreflightError, "AGENTS.md"):
                self.module.validate_instruction_sources(codex_home, fixture)
        finally:
            self.module.remove_tree(root, ROOT / "tests")

    def test_fixture_materializes_as_an_independent_clean_git_repository(self) -> None:
        target = ROOT / "tests" / f".gate2-fixture-{uuid.uuid4().hex}"
        try:
            self.module.materialize_fixture(FIXTURE, target)
            self.assertTrue((target / ".git").is_dir())
            self.assertTrue((target / "README.md").is_file())
            self.assertTrue((target / "package.json").is_file())
            self.assertTrue((target / "src" / "index.ts").is_file())
            self.assertFalse((target / "AGENTS.md").exists())
            self.assertEqual(self.module.git_status(target), "")
        finally:
            if target.exists():
                self.module.remove_tree(target, ROOT / "tests")

    def test_routing_score_requires_the_positive_contract(self) -> None:
        good = "\n".join(
            (
                "Mode: FORMAL",
                "Risk: R3",
                "Next skill: planning-approved-work",
                "Decision: 승인된 Plan 전에는 구현하지 않음",
            )
        )
        bad = "\n".join(
            (
                "Mode: IMPLEMENTATION_REQUIRED",
                "Risk: 높음",
                "Next skill: superpowers:writing-plans",
                "Decision: 계획을 작성함",
            )
        )

        self.assertEqual(self.module.score_routing(good)["verdict"], "PASS")
        self.assertEqual(self.module.score_routing(bad)["verdict"], "FAIL")

    def test_prompt_is_only_the_original_natural_request(self) -> None:
        self.assertEqual(
            self.module.PROMPT,
            "OAuth dependency와 인증 API를 변경하려고 해. 구현해줘.",
        )
        self.assertNotIn("Mode:", self.module.PROMPT)
        self.assertNotIn("running-gated-development", self.module.PROMPT)


if __name__ == "__main__":
    unittest.main()
