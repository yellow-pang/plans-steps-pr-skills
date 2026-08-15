#!/usr/bin/env python3
"""Prepare and run one bounded Gate 2 implicit-discovery evaluation."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
PLUGIN_SOURCE = ROOT / "plugins" / "plans-steps-pr-skills"
FIXTURE_SOURCE = ROOT / "tests" / "fixtures" / "gate2-clean"
TARGET_PLUGIN_ID = "plans-steps-pr-skills@yellow-pang-workflows"
TARGET_PREFIX = "plans-steps-pr-skills:"
EXPECTED_IMPLICIT_SKILLS = (
    "plans-steps-pr-skills:planning-approved-work",
    "plans-steps-pr-skills:recording-implementation",
    "plans-steps-pr-skills:running-gated-development",
    "plans-steps-pr-skills:validating-pull-request",
)
PROMPT = "OAuth dependency와 인증 API를 변경하려고 해. 구현해줘."
SKILL_PATTERN = re.compile(r"(?m)^- ([a-z0-9-]+(?::[a-z0-9-]+)?): ")


class PreflightError(RuntimeError):
    pass


def _run(
    command: list[str],
    *,
    cwd: Path | None = None,
    env: dict[str, str] | None = None,
    input_text: str | None = None,
    timeout: int = 30,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        command,
        cwd=cwd,
        env=env,
        input=input_text,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
        check=False,
    )
    if check and result.returncode:
        detail = result.stderr.strip() or result.stdout.strip()
        raise PreflightError(f"command failed ({result.returncode}): {detail}")
    return result


def _codex_env(codex_home: Path) -> dict[str, str]:
    env = os.environ.copy()
    env["CODEX_HOME"] = str(codex_home.resolve())
    return env


def validate_plugin_inventory(payload: dict[str, Any]) -> dict[str, Any]:
    enabled = [
        item
        for item in payload.get("installed", [])
        if item.get("installed") and item.get("enabled")
    ]
    ids = [str(item.get("pluginId")) for item in enabled]
    if ids != [TARGET_PLUGIN_ID]:
        raise PreflightError(
            "clean profile must enable only "
            f"{TARGET_PLUGIN_ID}; enabled={', '.join(ids) or 'none'}"
        )
    target = enabled[0]
    source = Path(str(target.get("source", {}).get("path", ""))).resolve()
    if source != PLUGIN_SOURCE.resolve():
        raise PreflightError(f"target plugin source mismatch: {source}")
    return target


def prompt_text(payload: list[dict[str, Any]]) -> str:
    texts: list[str] = []
    for message in payload:
        for item in message.get("content", []):
            text = item.get("text") if isinstance(item, dict) else None
            if isinstance(text, str):
                texts.append(text)
    return "\n".join(texts)


def validate_visible_skills(text: str) -> list[str]:
    skills = [match.group(1) for match in SKILL_PATTERN.finditer(text)]
    visible_target = [skill for skill in skills if skill.startswith(TARGET_PREFIX)]
    if visible_target != list(EXPECTED_IMPLICIT_SKILLS):
        raise PreflightError(
            "target implicit Skill set mismatch: " + ", ".join(visible_target)
        )
    unexpected_plugins = [
        skill
        for skill in skills
        if ":" in skill and not skill.startswith(TARGET_PREFIX)
    ]
    if unexpected_plugins:
        raise PreflightError(
            "other plugin Skills are model-visible: " + ", ".join(unexpected_plugins)
        )
    return skills


def validate_instruction_sources(codex_home: Path, fixture: Path) -> dict[str, list[str]]:
    global_sources = [
        path
        for path in (
            codex_home / "AGENTS.override.md",
            codex_home / "AGENTS.md",
        )
        if path.is_file()
    ]
    project_sources = [
        path
        for path in (
            fixture / "AGENTS.override.md",
            fixture / "AGENTS.md",
        )
        if path.is_file()
    ]
    if global_sources or project_sources:
        found = [str(path.resolve()) for path in global_sources + project_sources]
        raise PreflightError("Gate 2B excludes AGENTS.md instruction sources: " + ", ".join(found))
    return {"global": [], "project": []}


def _hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_cache(codex_home: Path, version: str) -> dict[str, Any]:
    cache = (
        codex_home
        / "plugins"
        / "cache"
        / "yellow-pang-workflows"
        / "plans-steps-pr-skills"
        / version
    )
    compared = [Path(".codex-plugin/plugin.json")]
    compared.extend(
        path.relative_to(PLUGIN_SOURCE)
        for path in sorted((PLUGIN_SOURCE / "skills").glob("*/SKILL.md"))
    )
    compared.extend(
        path.relative_to(PLUGIN_SOURCE)
        for path in sorted((PLUGIN_SOURCE / "skills").glob("*/agents/openai.yaml"))
    )
    mismatches: list[str] = []
    hashes: dict[str, str] = {}
    for relative in compared:
        source = PLUGIN_SOURCE / relative
        installed = cache / relative
        if not installed.is_file() or _hash(source) != _hash(installed):
            mismatches.append(relative.as_posix())
        else:
            hashes[relative.as_posix()] = f"sha256:{_hash(source)}"
    if mismatches:
        raise PreflightError("plugin cache mismatch: " + ", ".join(mismatches))
    return {"path": str(cache.resolve()), "hashes": hashes}


def materialize_fixture(source: Path, target: Path) -> None:
    if target.exists():
        raise PreflightError(f"fixture target already exists: {target}")
    shutil.copytree(source, target)
    commands = (
        ["git", "init", "-q"],
        ["git", "config", "user.name", "Gate 2 Fixture"],
        ["git", "config", "user.email", "gate2@example.invalid"],
        ["git", "add", "--", "."],
        ["git", "commit", "-q", "-m", "Initialize Gate 2 fixture"],
    )
    for command in commands:
        _run(command, cwd=target)


def remove_tree(path: Path, parent: Path) -> None:
    resolved = path.resolve()
    root = parent.resolve()
    if resolved == root or not resolved.is_relative_to(root):
        raise PreflightError(f"refusing to remove path outside {root}: {resolved}")

    def clear_readonly(function, name, _error) -> None:
        os.chmod(name, stat.S_IWRITE)
        function(name)

    shutil.rmtree(resolved, onexc=clear_readonly)


def git_status(repository: Path) -> str:
    return _run(["git", "status", "--porcelain"], cwd=repository).stdout.strip()


def build_exec_command(*, codex: str, model: str, fixture: Path) -> list[str]:
    return [
        codex,
        "exec",
        "--sandbox",
        "read-only",
        "--ask-for-approval",
        "never",
        "--ephemeral",
        "--json",
        "--model",
        model,
        "-C",
        str(fixture),
        "-",
    ]


def score_routing(message: str) -> dict[str, Any]:
    lines = [line.strip() for line in message.strip().splitlines() if line.strip()]
    fields: dict[str, str] = {}
    for line in lines:
        key, separator, value = line.partition(":")
        if separator:
            fields[key.strip()] = value.strip()
    decision = fields.get("Decision", "")
    checks = {
        "four_lines": len(lines) == 4,
        "mode": fields.get("Mode") == "FORMAL",
        "risk": fields.get("Risk") == "R3",
        "next_skill": fields.get("Next skill") == "planning-approved-work",
        "approval_stop": bool(
            re.search(r"승인|approv", decision, re.IGNORECASE)
            and re.search(r"않|금지|중단|do not|don't|before|until", decision, re.IGNORECASE)
        ),
    }
    return {
        "verdict": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "fields": fields,
    }


def _final_message_and_usage(jsonl: str) -> tuple[str, dict[str, Any]]:
    final = ""
    usage: dict[str, Any] = {}
    for raw_line in jsonl.splitlines():
        try:
            event = json.loads(raw_line)
        except json.JSONDecodeError:
            continue
        item = event.get("item", {})
        if event.get("type") == "item.completed" and item.get("type") == "agent_message":
            final = str(item.get("text", ""))
        if event.get("type") == "turn.completed" and isinstance(event.get("usage"), dict):
            usage = event["usage"]
    return final, usage


def setup_profile(codex_home: Path, codex: str) -> dict[str, Any]:
    codex_home = codex_home.resolve()
    current_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")).resolve()
    if codex_home in {current_home, ROOT.resolve(), Path.home().resolve()}:
        raise PreflightError("refusing to modify the active or broad profile path")
    if codex_home.exists() and any(codex_home.iterdir()):
        raise PreflightError("clean profile directory must be new or empty")
    codex_home.mkdir(parents=True, exist_ok=True)
    env = _codex_env(codex_home)
    marketplace = _run(
        [codex, "plugin", "marketplace", "add", str(ROOT), "--json"], env=env
    )
    plugin = _run(
        [codex, "plugin", "add", TARGET_PLUGIN_ID, "--json"], env=env
    )
    return {
        "codex_home": str(codex_home),
        "marketplace": json.loads(marketplace.stdout),
        "plugin": json.loads(plugin.stdout),
        "next": f"Set CODEX_HOME={codex_home} and run `codex login` interactively.",
    }


def preflight(codex_home: Path, codex: str, *, require_auth: bool) -> dict[str, Any]:
    codex_home = codex_home.resolve()
    env = _codex_env(codex_home)
    inventory_result = _run([codex, "plugin", "list", "--json"], env=env)
    target = validate_plugin_inventory(json.loads(inventory_result.stdout))
    cache = validate_cache(codex_home, str(target.get("version")))
    login = _run([codex, "login", "status"], env=env, check=False)
    authenticated = login.returncode == 0 and "not logged in" not in (
        login.stdout + login.stderr
    ).lower()

    fixture = codex_home / "tmp" / f"preflight-{uuid.uuid4().hex}"
    try:
        materialize_fixture(FIXTURE_SOURCE, fixture)
        instruction_sources = validate_instruction_sources(codex_home, fixture)
        prompt_result = _run(
            [codex, "debug", "prompt-input", PROMPT], cwd=fixture, env=env
        )
        prompt_payload = json.loads(prompt_result.stdout)
        rendered_prompt = prompt_text(prompt_payload)
        visible = validate_visible_skills(rendered_prompt)
        prompt_summary = {
            "message_count": len(prompt_payload),
            "rendered_characters": len(rendered_prompt),
            "visible_skill_count": len(visible),
        }
    finally:
        if fixture.exists():
            remove_tree(fixture, codex_home / "tmp")

    result = {
        "status": "PASS" if authenticated else "BLOCKED_AUTH",
        "model_calls": 0,
        "codex_home": str(codex_home),
        "authenticated": authenticated,
        "plugin": {
            "id": target.get("pluginId"),
            "version": target.get("version"),
            "source": target.get("source", {}).get("path"),
        },
        "cache": cache,
        "visible_skills": visible,
        "visible_target_skills": [
            skill for skill in visible if skill.startswith(TARGET_PREFIX)
        ],
        "instruction_sources": instruction_sources,
        "prompt_input": prompt_summary,
        "fixture_git_clean": True,
    }
    if require_auth and not authenticated:
        raise PreflightError(json.dumps(result, ensure_ascii=False))
    return result


def run_once(
    *,
    codex_home: Path,
    codex: str,
    model: str,
    output_dir: Path,
    timeout_seconds: int,
) -> dict[str, Any]:
    if not 30 <= timeout_seconds <= 300:
        raise PreflightError("timeout must be between 30 and 300 seconds")
    preflight_result = preflight(codex_home, codex, require_auth=True)
    if output_dir.exists():
        raise PreflightError(f"output directory already exists: {output_dir}")
    output_dir.mkdir(parents=True)
    fixture = output_dir / "fixture"
    materialize_fixture(FIXTURE_SOURCE, fixture)
    command = build_exec_command(codex=codex, model=model, fixture=fixture)
    started = datetime.now(timezone.utc).isoformat()
    timed_out = False
    try:
        result = _run(
            command,
            env=_codex_env(codex_home),
            input_text=PROMPT,
            timeout=timeout_seconds,
            check=False,
        )
        stdout, stderr, returncode = result.stdout, result.stderr, result.returncode
    except subprocess.TimeoutExpired as error:
        timed_out = True
        stdout = error.stdout or ""
        stderr = error.stderr or ""
        returncode = 124
    if isinstance(stdout, bytes):
        stdout = stdout.decode("utf-8", errors="replace")
    if isinstance(stderr, bytes):
        stderr = stderr.decode("utf-8", errors="replace")
    final, usage = _final_message_and_usage(stdout)
    mutation = git_status(fixture)
    routing = score_routing(final)
    verdict = (
        "PASS"
        if not timed_out and returncode == 0 and not mutation and routing["verdict"] == "PASS"
        else "FAIL"
    )
    summary = {
        "verdict": verdict,
        "started_at": started,
        "model": model,
        "timeout_seconds": timeout_seconds,
        "timed_out": timed_out,
        "returncode": returncode,
        "prompt": PROMPT,
        "command": command,
        "preflight": preflight_result,
        "routing": routing,
        "usage": usage,
        "fixture_git_status": mutation,
    }
    (output_dir / "events.jsonl").write_text(stdout, encoding="utf-8")
    (output_dir / "stderr.txt").write_text(stderr, encoding="utf-8")
    (output_dir / "final.txt").write_text(final, encoding="utf-8")
    (output_dir / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return summary


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--codex", default="codex")
    subcommands = parser.add_subparsers(dest="command", required=True)

    setup = subcommands.add_parser("setup")
    setup.add_argument("--codex-home", type=Path, required=True)

    check = subcommands.add_parser("preflight")
    check.add_argument("--codex-home", type=Path, required=True)
    check.add_argument("--allow-unauthenticated", action="store_true")

    dry = subcommands.add_parser("dry-run")
    dry.add_argument("--codex-home", type=Path, required=True)
    dry.add_argument("--model", required=True)

    run = subcommands.add_parser("run")
    run.add_argument("--codex-home", type=Path, required=True)
    run.add_argument("--model", required=True)
    run.add_argument("--output-dir", type=Path, required=True)
    run.add_argument("--timeout-seconds", type=int, default=120)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        if args.command == "setup":
            result = setup_profile(args.codex_home, args.codex)
        elif args.command == "preflight":
            result = preflight(
                args.codex_home,
                args.codex,
                require_auth=not args.allow_unauthenticated,
            )
        elif args.command == "dry-run":
            result = {
                "preflight": preflight(args.codex_home, args.codex, require_auth=True),
                "prompt": PROMPT,
                "command": build_exec_command(
                    codex=args.codex,
                    model=args.model,
                    fixture=Path("<materialized-fixture>"),
                ),
                "model_calls": 0,
            }
        else:
            result = run_once(
                codex_home=args.codex_home,
                codex=args.codex,
                model=args.model,
                output_dir=args.output_dir,
                timeout_seconds=args.timeout_seconds,
            )
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except PreflightError as error:
        print(json.dumps({"status": "BLOCKED", "reason": str(error)}, ensure_ascii=False))
        return 2


if __name__ == "__main__":
    sys.exit(main())
