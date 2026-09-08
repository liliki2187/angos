"""检查本轮使用的简单技能头字段及配置引用；不是通用 YAML 解析器。"""
import ast
import json
import re
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
NAMES = [
    "ui-designer", "ux-diagnosis", "angus-art-director",
    "angus-character-pixel-director", "steam-indie-appraiser",
    "ux-kb-risks", "ux-kb-cross-page", "ux-kb-symptoms",
    "ux-kb-principles", "ux-kb-templates", "openrouter-image-gen",
    "art-reference-picker", "psd-to-godot-ui",
]


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    for name in NAMES:
        source = (ROOT / "skills" / name / "SKILL.md").read_text(encoding="utf-8-sig")
        match = re.match(r"^---\n(.*?)\n---(?:\n|$)", source, re.S)
        assert match, name
        fields = {}
        for line in match.group(1).splitlines():
            key, raw = line.split(":", 1)
            assert key not in fields, (name, key)
            value = raw.strip()
            fields[key] = json.loads(value) if value.startswith('"') else value
        assert set(fields) == {"name", "description"}, name
        assert fields["name"] == name and re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name), name
        assert isinstance(fields["description"], str) and 0 < len(fields["description"]) <= 1024, name
        assert not any(c in fields["description"] for c in "<>"), name
        assert "[TODO:" not in source, name
    print(f"技能头字段检查：{len(NAMES)} 份通过")

    for path in (ROOT / ".codex/agents").glob("*.toml"):
        tomllib.loads(path.read_text(encoding="utf-8-sig"))
    print("项目角色 TOML 语法：通过")
    for name in ("risks", "cross-page", "symptoms", "principles", "templates"):
        data = json.loads((ROOT / f"skills/ux-kb-{name}/skill_meta.json").read_text(encoding="utf-8"))
        assert re.fullmatch(r"\d+\.\d+\.\d+", data["version"])
        assert data["name"] == f"ux-kb-{name}"
        assert (ROOT / "skills" / data["name"] / data["source"]).is_file()
        assert not re.search(r"\d+\s*(个|条|类)", data["display_name"])
    print("KB JSON / 版本字段：通过")

    for relative in (
        "scripts/check_delivery_manifest.py",
        "skills/ui-designer/scripts/validate_ui_designer_skill.py",
        "skills/openrouter-image-gen/scripts/openrouter_image_gen.py",
        "scripts/tests/test_astra_ui_workflow.py",
    ):
        ast.parse((ROOT / relative).read_text(encoding="utf-8-sig"))
    print("修改的 Python AST：通过")

    gates = (ROOT / "docs/workflows/workflow-gates.yml").read_text(encoding="utf-8")
    block = gates.split("artifact_types:\n", 1)[1].split("\nstage_transitions:", 1)[0]
    ids = re.findall(r"^  (\w+):$", block, re.M)
    assert ids and len(ids) == len(set(ids))
    transitions = gates.split("stage_transitions:\n", 1)[1].split("\nhard_gates:", 1)[0]
    for raw in re.findall(r"allowed: \[([^\]]+)\]", transitions):
        assert all(value.strip() in ids for value in raw.split(","))
    risk_block = gates.split("risk_levels:\n", 1)[1].split("\nfeedback_contract:", 1)[0]
    production = risk_block.split("  production:\n", 1)[1]
    raw = re.search(r"checks:\s*\[([^\]]+)\]", production).group(1)
    checks = {value.strip() for value in raw.split(",")}
    assert {"contract", "runtime", "affected_states", "visual_review", "recovery"} <= checks
    print(f"证据目录：{len(ids)} 个身份唯一；引用及必要生产证据匹配（不固定数量和序列化顺序）")
    print("说明：仅检查本轮简单字段与引用；未使用通用 YAML 解析器，不代替运行或视觉验收。")


if __name__ == "__main__":
    main()
