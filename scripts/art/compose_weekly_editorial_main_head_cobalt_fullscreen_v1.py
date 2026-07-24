#!/usr/bin/env python3
"""把 Godot 主头版切片按合同坐标放回 v6 整屏，生成位置审阅证据。"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image, ImageChops


TARGET = (459, 276, 442, 374)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--screen", type=Path, required=True)
    parser.add_argument("--component", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--audit", type=Path, required=True)
    args = parser.parse_args()

    with Image.open(args.screen) as opened:
        screen = opened.convert("RGB")
    with Image.open(args.component) as opened:
        component = opened.convert("RGBA")
    if screen.size != (1920, 1080):
        raise ValueError(f"screen must be 1920x1080, got {screen.size}")
    if component.size != (TARGET[2], TARGET[3]):
        component = component.resize((TARGET[2], TARGET[3]), Image.Resampling.LANCZOS)

    result = screen.convert("RGBA")
    result.alpha_composite(component, (TARGET[0], TARGET[1]))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    result.convert("RGB").save(args.output, optimize=True)

    diff = ImageChops.difference(screen, result.convert("RGB"))
    bbox = diff.getbbox()
    allowed = (TARGET[0], TARGET[1], TARGET[0] + TARGET[2], TARGET[1] + TARGET[3])
    passed = bbox is not None and bbox[0] >= allowed[0] and bbox[1] >= allowed[1] and bbox[2] <= allowed[2] and bbox[3] <= allowed[3]
    audit = {
        "artifact": "weekly_editorial_main_head_cobalt_fullscreen_placement_preview_v1",
        "screen": args.screen.as_posix(),
        "component": args.component.as_posix(),
        "output": args.output.as_posix(),
        "canvas": list(screen.size),
        "contract_rect": list(TARGET),
        "changed_pixel_bbox": list(bbox) if bbox else None,
        "changes_outside_contract_rect": not passed,
        "passed": passed,
        "boundary": "整屏位置合成预览；未修改正式 Godot 发刊界面。",
    }
    args.audit.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(audit, ensure_ascii=False))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
