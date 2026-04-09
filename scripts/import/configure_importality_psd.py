from __future__ import annotations

import argparse
import re
import shutil
from datetime import datetime
from pathlib import Path

from psd_support import PROJECT_ROOT, REPO_ROOT, forward_slash, quote_tres_string


TEMP_DIR_KEY = "importality/temporary_files_directory_path"
RULES_KEY = "importality/command_building_rules_for_custom_image_loader"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Configure Godot editor settings for PSD conversion through Importality."
    )
    default_settings_path = Path.home() / "AppData" / "Roaming" / "Godot" / "editor_settings-4.3.tres"
    parser.add_argument(
        "--settings-file",
        type=Path,
        default=default_settings_path,
        help="Path to Godot editor_settings-4.3.tres.",
    )
    return parser


def parse_packed_string_array(line: str) -> list[str]:
    return [
        bytes(match, "utf-8").decode("unicode_escape")
        for match in re.findall(r'"((?:[^"\\]|\\.)*)"', line)
    ]


def encode_packed_string_array(values: list[str]) -> str:
    encoded_items = ", ".join(quote_tres_string(value) for value in values)
    return f"PackedStringArray({encoded_items})"


def upsert_assignment(lines: list[str], key: str, value: str) -> list[str]:
    prefix = f"{key} = "
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = prefix + value
            return lines

    try:
        resource_index = lines.index("[resource]")
    except ValueError:
        lines.extend(["", "[resource]"])
        resource_index = len(lines) - 1
    insert_at = resource_index + 1
    lines.insert(insert_at, prefix + value)
    return lines


def main() -> int:
    args = build_parser().parse_args()
    settings_path = args.settings_file.expanduser().resolve()
    if not settings_path.exists():
        raise SystemExit(f"Editor settings file not found: {settings_path}")

    temp_dir = (PROJECT_ROOT / ".godot" / "importality-temp").resolve()
    temp_dir.mkdir(parents=True, exist_ok=True)

    python_path = forward_slash(Path(__import__("sys").executable).resolve())
    converter_path = forward_slash((REPO_ROOT / "scripts" / "import" / "psd_to_png.py").resolve())
    psd_rule = f"psd: {python_path} {converter_path} {{in_path}} {{out_path}}"

    original_text = settings_path.read_text(encoding="utf-8")
    lines = original_text.splitlines()

    existing_rules: list[str] = []
    for line in lines:
        if line.startswith(f"{RULES_KEY} = "):
            existing_rules = parse_packed_string_array(line)
            break

    updated_rules: list[str] = []
    replaced = False
    for rule in existing_rules:
        if rule.split(":", 1)[0].strip().lower() == "psd":
            updated_rules.append(psd_rule)
            replaced = True
        else:
            updated_rules.append(rule)
    if not replaced:
        updated_rules.append(psd_rule)

    upsert_assignment(lines, TEMP_DIR_KEY, quote_tres_string(forward_slash(temp_dir)))
    upsert_assignment(lines, RULES_KEY, encode_packed_string_array(updated_rules))

    updated_text = "\n".join(lines).rstrip() + "\n"
    if updated_text == original_text:
        print(f"Importality PSD settings already configured in {settings_path}")
        return 0

    backup_path = settings_path.with_suffix(settings_path.suffix + "." + datetime.now().strftime("%Y%m%d%H%M%S") + ".bak")
    shutil.copy2(settings_path, backup_path)
    settings_path.write_text(updated_text, encoding="utf-8")

    print(f"Updated {settings_path}")
    print(f"Backup: {backup_path}")
    print(f"PSD rule: {psd_rule}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
