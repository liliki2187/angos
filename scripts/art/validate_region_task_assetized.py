from __future__ import annotations

import json
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
ASSET_ROOT = ROOT / "gd_project" / "Assets" / "ui" / "angus_packaging" / "region_task"
MANIFEST = ASSET_ROOT / "region_task_asset_manifest.json"


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    errors: list[str] = []
    rows: list[str] = []

    for asset in manifest["assets"]:
        asset_id = asset["id"]
        raw_path = asset.get("path") or asset.get("final_path")
        raw_size = asset.get("target_size") or asset.get("final_size")
        if raw_path is None:
            errors.append(f"PATH_FIELD {asset_id}: expected path or final_path")
            continue
        if raw_size is None:
            errors.append(f"SIZE_FIELD {asset_id}: expected target_size or final_size")
            continue

        path = ROOT / raw_path
        if not path.exists():
            errors.append(f"MISSING {asset_id}: {path.relative_to(ROOT)}")
            continue

        with Image.open(path) as image:
            size = image.size

        expected_size = tuple(raw_size)
        if size != expected_size:
            errors.append(f"SIZE {asset_id}: got {size}, expected {expected_size}")

        if "frame_size" in asset:
            frame_w, frame_h = asset["frame_size"]
            if size[0] % frame_w or size[1] % frame_h:
                errors.append(
                    f"FRAME_GRID {asset_id}: size {size} not divisible by {(frame_w, frame_h)}"
                )

            capacity = (size[0] // frame_w) * (size[1] // frame_h)
            frame_count = len(asset.get("frames", []))
            if capacity < frame_count:
                errors.append(
                    f"FRAME_CAPACITY {asset_id}: capacity {capacity}, frames {frame_count}"
                )

            rows.append(
                f"{asset_id}: {size}, frame={frame_w}x{frame_h}, frames={frame_count}, capacity={capacity}"
            )
        else:
            rows.append(f"{asset_id}: {size}")

    print("\n".join(rows))
    if errors:
        print("\nRESULT: FAIL")
        print("\n".join(errors))
        return 1

    print("\nRESULT: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
