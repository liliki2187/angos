#!/usr/bin/env python3
"""Validate the Angus Game Numerical skill without third-party dependencies."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python < 3.11 fallback.
    tomllib = None


REQUIRED_FILES = [
    "skills/game-numerical/SKILL.md",
    "skills/game-numerical/agents/openai.yaml",
    "skills/game-numerical/references/system-prompt-v1.0.md",
    "skills/game-numerical/references/commercial-mmo-f2p.md",
    "skills/game-numerical/references/upstream-readme.md",
    "skills/game-numerical/references/casebook/case-01-card-costing.md",
    "skills/game-numerical/references/casebook/case-02-difficulty-curve.md",
    ".codex/agents/game-numerical.toml",
]

DOC_REQUIRED_PHRASES_BY_FILE = {
    "AGENTS.md": ["game_numerical", "@数值策划", "Angus 主干数值"],
    "docs/onboarding/ai-collaboration-guidance.md": ["game_numerical", "@数值策划", "Angus 主干数值"],
    "docs/onboarding/subagent-collaboration-improvement.md": ["game_numerical", "@数值策划", "Angus 主干数值"],
}

SKILL_REQUIRED_PHRASES = [
    "@数值策划",
    "Angus 主干数值",
    "不默认加载",
    "commercial-mmo-f2p.md",
    "event-check-resolution.md",
    "experience_note",
]


class Validator:
    def __init__(self, repo: Path) -> None:
        self.repo = repo
        self.failures: list[str] = []
        self.warnings: list[str] = []
        self.passes: list[str] = []

    def ok(self, message: str) -> None:
        self.passes.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)

    def fail(self, message: str) -> None:
        self.failures.append(message)

    def path(self, rel: str) -> Path:
        return self.repo / rel

    def read_text(self, rel: str) -> str | None:
        path = self.path(rel)
        try:
            text = path.read_text(encoding="utf-8")
        except FileNotFoundError:
            self.fail(f"missing file: {rel}")
            return None
        except UnicodeDecodeError as exc:
            self.fail(f"not valid UTF-8: {rel} ({exc})")
            return None
        if "\ufffd" in text:
            self.fail(f"replacement character found, possible mojibake: {rel}")
        return text

    def validate_required_files(self) -> None:
        missing = [rel for rel in REQUIRED_FILES if not self.path(rel).exists()]
        if missing:
            for rel in missing:
                self.fail(f"missing required file: {rel}")
            return
        self.ok("required files exist")

    def parse_frontmatter(self, text: str) -> dict[str, str] | None:
        lines = text.splitlines()
        if not lines or lines[0] != "---":
            self.fail("SKILL.md frontmatter must start with ---")
            return None
        try:
            end = lines[1:].index("---") + 1
        except ValueError:
            self.fail("SKILL.md frontmatter must end with ---")
            return None
        data: dict[str, str] = {}
        for line in lines[1:end]:
            if not line.strip():
                continue
            if ":" not in line:
                self.fail(f"invalid frontmatter line: {line}")
                continue
            key, value = line.split(":", 1)
            data[key.strip()] = value.strip().strip('"')
        return data

    def validate_skill_md(self) -> None:
        rel = "skills/game-numerical/SKILL.md"
        text = self.read_text(rel)
        if text is None:
            return
        frontmatter = self.parse_frontmatter(text)
        if frontmatter is None:
            return
        if frontmatter.get("name") != "game-numerical":
            self.fail("SKILL.md frontmatter name must be game-numerical")
        elif not frontmatter.get("description"):
            self.fail("SKILL.md frontmatter description is empty")
        else:
            self.ok("SKILL.md frontmatter looks valid")
        for phrase in SKILL_REQUIRED_PHRASES:
            if phrase not in text:
                self.fail(f"SKILL.md missing required phrase: {phrase}")
        self.ok("SKILL.md required routing phrases present")

    def load_toml(self, rel: str) -> dict[str, object] | None:
        text = self.read_text(rel)
        if text is None:
            return None
        if tomllib is not None:
            try:
                return tomllib.loads(text)
            except tomllib.TOMLDecodeError as exc:
                self.fail(f"invalid TOML: {rel} ({exc})")
                return None
        self.warn("tomllib unavailable; using limited TOML fallback parser")
        data: dict[str, object] = {}
        for raw in text.splitlines():
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip()
            if value.startswith('"') and value.endswith('"'):
                data[key] = value[1:-1]
            elif value.startswith("[") and value.endswith("]"):
                items = value[1:-1].split(",")
                data[key] = [item.strip().strip('"') for item in items if item.strip()]
        return data

    def validate_agent_toml(self) -> None:
        rel = ".codex/agents/game-numerical.toml"
        data = self.load_toml(rel)
        if data is None:
            return
        expected = {
            "name": "game_numerical",
            "sandbox_mode": "read-only",
            "model_reasoning_effort": "high",
        }
        for key, value in expected.items():
            if data.get(key) != value:
                self.fail(f"{rel} {key} must be {value!r}")
        instructions = str(data.get("developer_instructions", ""))
        for phrase in [
            "skills/game-numerical/SKILL.md",
            "Angus mainline systems",
            "Do not apply Roguelite",
            "Do not load commercial MMO/F2P",
        ]:
            if phrase not in instructions:
                self.fail(f"{rel} developer_instructions missing: {phrase}")
        self.ok("game-numerical.toml basic fields parse")

    def validate_openai_yaml(self) -> None:
        rel = "skills/game-numerical/agents/openai.yaml"
        text = self.read_text(rel)
        if text is None:
            return
        for phrase in ["display_name", "short_description", "default_prompt", "Game Numerical"]:
            if phrase not in text:
                self.fail(f"{rel} missing metadata phrase: {phrase}")
        self.ok("openai.yaml metadata present and UTF-8")

    def validate_project_docs(self) -> None:
        for rel, phrases in DOC_REQUIRED_PHRASES_BY_FILE.items():
            text = self.read_text(rel)
            if text is None:
                continue
            for phrase in phrases:
                if phrase not in text:
                    self.fail(f"{rel} missing project routing phrase: {phrase}")
        self.ok("project routing docs contain expected Numerical routing references")

    def validate_references(self) -> None:
        for rel in [
            "skills/game-numerical/references/system-prompt-v1.0.md",
            "skills/game-numerical/references/commercial-mmo-f2p.md",
            "skills/game-numerical/references/upstream-readme.md",
            "skills/game-numerical/references/casebook/case-01-card-costing.md",
            "skills/game-numerical/references/casebook/case-02-difficulty-curve.md",
        ]:
            text = self.read_text(rel)
            if text is not None and len(text.strip()) < 200:
                self.fail(f"reference file unexpectedly short: {rel}")
        self.ok("reference files are readable")

    def run(self) -> int:
        self.validate_required_files()
        self.validate_skill_md()
        self.validate_agent_toml()
        self.validate_openai_yaml()
        self.validate_project_docs()
        self.validate_references()
        for message in self.passes:
            print(f"[OK] {message}")
        for message in self.warnings:
            print(f"[WARN] {message}")
        for message in self.failures:
            print(f"[FAIL] {message}")
        if self.failures:
            print(f"\nValidation failed: {len(self.failures)} issue(s).")
            return 1
        print("\nValidation passed.")
        return 0


def default_repo() -> Path:
    return Path(__file__).resolve().parents[3]


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Validate Angus Game Numerical skill without dependencies.")
    parser.add_argument("--repo", type=Path, default=default_repo(), help="Repository root. Defaults to this script's repo.")
    args = parser.parse_args(argv)
    repo = args.repo.resolve()
    if not (repo / "AGENTS.md").exists():
        print(f"[FAIL] repo root does not contain AGENTS.md: {repo}")
        return 1
    return Validator(repo).run()


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
