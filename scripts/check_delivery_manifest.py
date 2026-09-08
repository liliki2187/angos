# -*- coding: utf-8 -*-
"""交付记录的结构检查；不证明视觉、运行行为或用户认可。

仅对需要记录的复杂交接/生产候选主动调用，不作为所有回复的前置条件。
退出码：0 记录结构完整；1 记录缺项；2 参数/文件错误。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
GATES_YML = REPO_ROOT / "docs/workflows/workflow-gates.yml"
RUNTIME_TYPES = {"runtime_state_preview", "runtime_skeleton", "vertical_slice_proof", "production_candidate", "godot_agent_smoke", "isolated_technical_probe"}


def load_artifact_types():
    """读取保留的类型目录，不加载或执行全套门槛。"""
    types = []
    in_block = False
    for line in GATES_YML.read_text(encoding="utf-8-sig").splitlines():
        if line == "artifact_types:":
            in_block = True
        elif in_block:
            if re.match(r"^\S", line):
                break
            match = re.match(r"^  (\w+):\s*$", line)
            if match:
                types.append(match.group(1))
    return types


def field(text, name):
    """支持普通与 Markdown 加粗字段，要求字段有实际值。"""
    plain = text.replace("**", "")
    match = re.search(rf"^[ \t-]*{re.escape(name)}[ \t]*[：:][ \t]*([^\r\n]*)", plain, re.M)
    return match.group(1).strip().strip("`") if match else ""


def check_file(path, artifact_types):
    text = path.read_text(encoding="utf-8-sig")
    results = []
    for name in ("产物类型", "变更范围", "验证证据", "未验证边界"):
        value = field(text, name)
        results.append(("PASS" if value else "FAIL", name, "字段已填写（未核实内容正确性）" if value else "缺少非空字段"))

    kind = field(text, "产物类型").split()[0] if field(text, "产物类型") else ""
    if kind and kind not in artifact_types:
        results.append(("FAIL", "类型目录", f"未知产物类型：{kind}"))
    if kind in RUNTIME_TYPES:
        evidence = field(text, "验证证据")
        if evidence in {"无", "未验证", "待补", "暂无", "N/A", ""}:
            results.append(("FAIL", "运行证据", "运行类交付需要指向实际证据，不能填写未验证"))
        else:
            results.append(("PASS", "运行证据", "存在证据说明；仍需独立检查其文件、执行结果与覆盖范围"))
    results.append(("INFO", "声明边界", "本工具只做记录 lint，不代表几何、美术、交互通过；不要求 STATUS 或特定角色名称"))
    return results, any(level == "FAIL" for level, _, _ in results)


def main(argv):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass
    if len(argv) < 2:
        print("用法：python scripts/check_delivery_manifest.py <交付记录.md> [...]")
        return 2
    try:
        types = load_artifact_types()
        if not types:
            raise ValueError("产物类型目录为空")
        failed = False
        for arg in argv[1:]:
            path = Path(arg)
            results, has_fail = check_file(path, types)
            failed |= has_fail
            print(path)
            for level, name, detail in results:
                print(f"[{level}] {name}：{detail}")
        print("仅完成记录结构检查，未执行运行或视觉验收。")
        return 1 if failed else 0
    except (OSError, UnicodeError, ValueError) as exc:
        print(f"检查错误：{exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
