#!/usr/bin/env python3
"""校验运行时复审图中的可见字段是否来自正式数据，而非压力 fixture。"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
FIELD_REQUIRED = {
    "field_id",
    "component",
    "visible",
    "player_question",
    "decision_value",
    "owner_scope",
    "source_kind",
    "data_source",
    "fixture_key",
    "screenshot_value",
    "decision",
}
COMPONENT_REQUIRED = {
    "component_id",
    "visible",
    "player_question",
    "necessity",
    "data_source",
    "interactive",
    "decision",
}
ALLOWED_SOURCE_KINDS = {"live_runtime", "state_derived", "content_mapping", "static_semantic"}
ALLOWED_VISIBLE_DECISIONS = {"keep", "change"}


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _resolve_repo_path(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else ROOT / path


def _resolve_key(data: Any, dotted_key: str) -> Any:
    current = data
    for part in dotted_key.split("."):
        if not isinstance(current, dict) or part not in current:
            raise KeyError(dotted_key)
        current = current[part]
    return current


def validate(path: Path) -> list[str]:
    manifest = _load(path)
    errors: list[str] = []

    fixture_path_value = manifest.get("runtime_fixture_path")
    if not isinstance(fixture_path_value, str) or not fixture_path_value:
        return ["缺少 runtime_fixture_path"]
    fixture_path = _resolve_repo_path(fixture_path_value)
    if not fixture_path.is_file():
        return [f"runtime fixture 不存在: {fixture_path}"]
    fixture = _load(fixture_path)
    if fixture.get("provenance") != "production_runtime_export":
        errors.append("runtime fixture provenance 必须为 production_runtime_export")
    if fixture.get("generated_from_production_data") is not True:
        errors.append("runtime fixture 未声明 generated_from_production_data=true")

    fields = manifest.get("visible_field_semantics")
    if not isinstance(fields, list) or not fields:
        errors.append("visible_field_semantics 必须是非空数组")
    else:
        seen_fields: set[str] = set()
        for index, field in enumerate(fields):
            if not isinstance(field, dict):
                errors.append(f"visible_field_semantics[{index}] 不是对象")
                continue
            missing = sorted(FIELD_REQUIRED - set(field))
            if missing:
                errors.append(f"visible_field_semantics[{index}] 缺少字段 {missing}")
                continue
            field_id = str(field["field_id"])
            if field_id in seen_fields:
                errors.append(f"重复 field_id: {field_id}")
            seen_fields.add(field_id)
            if field["visible"] is not True:
                errors.append(f"{field_id}: visible_field_semantics 只能登记当前可见字段")
            if field["decision"] not in ALLOWED_VISIBLE_DECISIONS:
                errors.append(f"{field_id}: 可见字段 decision={field['decision']!r}")
            if field["source_kind"] not in ALLOWED_SOURCE_KINDS:
                errors.append(f"{field_id}: source_kind={field['source_kind']!r} 不允许进入复审图")
            for key in ("player_question", "decision_value", "owner_scope", "data_source"):
                if not str(field[key]).strip():
                    errors.append(f"{field_id}: {key} 为空")
            try:
                fixture_value = _resolve_key(fixture, str(field["fixture_key"]))
            except KeyError:
                errors.append(f"{field_id}: fixture_key 不存在: {field['fixture_key']}")
                continue
            if field["screenshot_value"] != fixture_value:
                errors.append(
                    f"{field_id}: screenshot_value={field['screenshot_value']!r} "
                    f"与 production fixture={fixture_value!r} 不一致"
                )

    components = manifest.get("visible_component_audit")
    expected_ids = manifest.get("visible_component_expected_ids")
    if not isinstance(expected_ids, list) or not expected_ids:
        errors.append("缺少 visible_component_expected_ids")
    if not isinstance(components, list) or not components:
        errors.append("visible_component_audit 必须是非空数组")
    else:
        actual_ids: list[str] = []
        for index, component in enumerate(components):
            if not isinstance(component, dict):
                errors.append(f"visible_component_audit[{index}] 不是对象")
                continue
            missing = sorted(COMPONENT_REQUIRED - set(component))
            if missing:
                errors.append(f"visible_component_audit[{index}] 缺少字段 {missing}")
                continue
            component_id = str(component["component_id"])
            actual_ids.append(component_id)
            if component["visible"] is not True:
                errors.append(f"{component_id}: 当前组件审计项必须 visible=true")
            if component["decision"] not in ALLOWED_VISIBLE_DECISIONS:
                errors.append(f"{component_id}: decision={component['decision']!r}")
            for key in ("player_question", "necessity", "data_source"):
                if not str(component[key]).strip():
                    errors.append(f"{component_id}: {key} 为空")
        if isinstance(expected_ids, list) and actual_ids != expected_ids:
            errors.append(f"组件审计覆盖不完整或顺序漂移: expected={expected_ids}, actual={actual_ids}")

    removed = manifest.get("removed_fixture_fields")
    if not isinstance(removed, list) or not removed:
        errors.append("必须登记 removed_fixture_fields，证明压力字段已显式退役")
    else:
        for index, item in enumerate(removed):
            if not isinstance(item, dict) or not {
                "field_id",
                "prior_value",
                "reason",
                "visible_after",
            }.issubset(item):
                errors.append(f"removed_fixture_fields[{index}] 记录不完整")
                continue
            if item["visible_after"] is not False:
                errors.append(f"{item['field_id']}: 已退役 fixture 仍标记为可见")

    return errors


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("用法: python scripts/ui-contracts/validate_visible_field_semantics.py <manifest.json> [...]")
        return 2
    failed = False
    for argument in argv[1:]:
        path = Path(argument)
        errors = validate(path)
        if errors:
            failed = True
            print(f"FAIL {path}")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"PASS {path}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
