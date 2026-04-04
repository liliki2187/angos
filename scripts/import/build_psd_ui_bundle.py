from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

from psd_support import PROJECT_ROOT, forward_slash
from psd_support import repo_relative

SCRIPT_ROOT = Path(__file__).resolve().parent


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Build a project-ready Godot UI bundle from a PSD."
    )
    parser.add_argument("input_psd", type=Path, help="Path to the source PSD file.")
    parser.add_argument(
        "--mode",
        choices=("reusable", "preview"),
        default="reusable",
        help="Choose reusable for project asset output, or preview for validation-only output.",
    )
    parser.add_argument(
        "--slug",
        help="Override the bundle slug. Defaults to the PSD filename.",
    )
    parser.add_argument(
        "--skip-configure-editor",
        action="store_true",
        help="Do not update Godot Editor Settings for Importality.",
    )
    return parser


def slugify(value: str) -> str:
    chars: list[str] = []
    last_was_dash = False
    for char in value.lower():
        if char.isalnum():
            chars.append(char)
            last_was_dash = False
            continue
        if not last_was_dash:
            chars.append("-")
            last_was_dash = True
    text = "".join(chars).strip("-")
    return text or "psd-ui"


def pascal_case(slug: str) -> str:
    return "".join(part.capitalize() for part in slug.split("-") if part) or "PsdUi"


def resolve_output_paths(slug: str, mode: str, source_name: str) -> tuple[Path, Path, Path, str]:
    pascal = pascal_case(slug)
    if mode == "preview":
        asset_root = PROJECT_ROOT / "Assets" / "ui" / "psd_samples" / slug
        scene_path = PROJECT_ROOT / "scenes" / "dev" / f"{pascal}ImportedPreview.tscn"
        root_name = f"{pascal}ImportedPreview"
    else:
        asset_root = PROJECT_ROOT / "Assets" / "ui" / "imported" / slug
        scene_path = PROJECT_ROOT / "scenes" / "ui" / "imported" / f"{pascal}Ui.tscn"
        root_name = f"{pascal}Ui"

    source_path = asset_root / "source" / source_name
    generated_dir = asset_root / "generated"
    return source_path, generated_dir, scene_path, root_name


def run_python_script(script_name: str, args: list[str]) -> None:
    script_path = SCRIPT_ROOT / script_name
    subprocess.run(
        [sys.executable, str(script_path), *args],
        cwd=PROJECT_ROOT,
        check=True,
    )


def main() -> int:
    args = build_parser().parse_args()

    input_psd = args.input_psd.resolve()
    if not input_psd.exists():
        raise SystemExit(f"PSD file not found: {input_psd}")

    slug = slugify(args.slug or input_psd.stem)
    source_path, generated_dir, scene_path, root_name = resolve_output_paths(
        slug,
        args.mode,
        input_psd.name,
    )

    source_path.parent.mkdir(parents=True, exist_ok=True)
    if input_psd != source_path:
        shutil.copy2(input_psd, source_path)

    if not args.skip_configure_editor:
        run_python_script("configure_importality_psd.py", [])

    run_python_script(
        "psd_to_godot_ui.py",
        [
            str(source_path),
            "--output-dir",
            str(generated_dir),
            "--scene",
            str(scene_path),
            "--root-name",
            root_name,
        ],
    )

    summary = {
        "mode": args.mode,
        "slug": slug,
        "source_psd": repo_relative(source_path),
        "generated_dir": repo_relative(generated_dir),
        "scene_path": repo_relative(scene_path),
        "root_name": root_name,
        "preview_png": repo_relative(generated_dir / "preview" / f"{source_path.stem}_flat.png"),
        "manifest_path": repo_relative(generated_dir / "manifest.json"),
    }
    generated_dir.mkdir(parents=True, exist_ok=True)
    summary_path = generated_dir / "bundle.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
