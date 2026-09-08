#!/usr/bin/env python3
"""检查 UI Designer 的真实入口、只读配置与本地链接；不绑定规范措辞。"""
from __future__ import annotations
import argparse
import re
import sys
import tomllib
from pathlib import Path
from urllib.parse import unquote


def validate(repo: Path) -> list[str]:
    errors: list[str] = []
    entry = repo / "skills/ui-designer/SKILL.md"
    shell = repo / ".codex/agents/ui-designer.toml"
    sources = [repo / "AGENTS.md", entry,
               repo / "docs/onboarding/ai-collaboration-guidance.md",
               repo / "docs/onboarding/ui-interaction-guidelines.md",
               repo / "docs/onboarding/subagent-collaboration-improvement.md"]
    try:
        text = entry.read_text(encoding="utf-8-sig")
        match = re.match(r"^---\n(.*?)\n---(?:\n|$)", text, re.S)
        if not match:
            errors.append("技能缺少头字段")
        else:
            fields = dict(re.findall(r"^(name|description):\s*(.+)$", match.group(1), re.M))
            if fields.get("name", "").strip('"') != "ui-designer":
                errors.append("技能 name 与目录不符")
            if not fields.get("description", "").strip('" '):
                errors.append("技能 description 为空")
        config = tomllib.loads(shell.read_text(encoding="utf-8-sig"))
        if config.get("name") != "ui_designer" or config.get("sandbox_mode") != "read-only":
            errors.append("角色身份或只读边界不正确")
        if "model" in config or "model_reasoning_effort" in config:
            errors.append("UI 角色应继承父级模型与推理档位")
        skill_refs = re.findall(r"skills/[a-z0-9-]+/SKILL\.md", str(config.get("developer_instructions", "")))
        if "skills/ui-designer/SKILL.md" not in skill_refs:
            errors.append("启动壳未指向 UI Designer 技能")
        for ref in skill_refs:
            if not (repo / ref).is_file():
                errors.append(f"启动来源不存在：{ref}")
        metadata = (repo / "skills/ui-designer/agents/openai.yaml").read_text(encoding="utf-8-sig")
        # 此处仅检查当前单行元数据字段，不冒充通用 YAML 解析器。
        for key in ("display_name", "short_description", "default_prompt"):
            match = re.search(rf"^\s+{key}:\s*(.+)$", metadata, re.M)
            if not match or not match.group(1).strip('" '):
                errors.append(f"技能展示元数据缺少 {key}")
        for path in sources:
            source = path.read_text(encoding="utf-8-sig")
            if "\ufffd" in source:
                errors.append(f"可能存在编码损坏：{path.relative_to(repo)}")
            for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", source):
                if re.match(r"(?:[a-z]+:|#)", target, re.I):
                    continue
                target = unquote(target.split("#", 1)[0]).strip("<>")
                if target and not (path.parent / target).exists():
                    errors.append(f"本地链接失效：{path.relative_to(repo)} -> {target}")
        for name in ("system-prompt-v1.0.md", "playbook.md", "upstream-readme.md"):
            path = repo / "skills/ui-designer/references" / name
            source = path.read_text(encoding="utf-8-sig")
            if "SKILL.md" not in source:
                errors.append(f"旧入口没有指回当前技能：{name}")
    except (OSError, UnicodeError, tomllib.TOMLDecodeError) as exc:
        errors.append(str(exc))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[3])
    args = parser.parse_args()
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    errors = validate(args.repo.resolve())
    for error in errors:
        print(f"[FAIL] {error}")
    if errors:
        return 1
    print("通过：角色身份、权限、继承、技能元数据、启动来源和当前入口链接。未验证模型行为或美术质量。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
