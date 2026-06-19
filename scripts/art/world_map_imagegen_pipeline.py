from __future__ import annotations

import argparse
import shutil
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MANIFEST = ROOT / "gd_project" / "Assets" / "ui" / "angus_packaging" / "world_map" / "imagegen_v5" / "world_map_imagegen_manifest.json"
DEFAULT_PROMPT_BUNDLE = ROOT / "docs" / "plans" / "world-map-imagegen-v5" / "prompt-bundle.json"
DEFAULT_REVIEW_DIR = ROOT / "docs" / "screenshots" / "2026-06-12-world-map-imagegen-v5-review"
DEFAULT_CODEX_SOURCE_ROOT = ROOT / "image_gen" / "codex_image2_sources"
OPENROUTER_SCRIPT = ROOT / "skills" / "openrouter-image-gen" / "scripts" / "openrouter_image_gen.py"


class PipelineError(RuntimeError):
    pass


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise PipelineError(f"Missing JSON file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def repo_path(value: str) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = ROOT / path
    return path


def ps_quote(value: str | Path) -> str:
    text = str(value)
    return "'" + text.replace("'", "''") + "'"


def slugify(value: str) -> str:
    lowered = value.strip().lower()
    result = []
    for char in lowered:
        if char.isalnum():
            result.append(char)
        elif char in {"-", "_", ".", " "}:
            result.append("-")
    slug = "".join(result).strip("-")
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug or "world-map-source"


def assert_rect_inside(rect: list[Any], bounds: tuple[int, int], label: str) -> None:
    if len(rect) != 4:
        raise PipelineError(f"{label} must be [x, y, w, h], got {rect!r}")
    x, y, w, h = [int(v) for v in rect]
    if w <= 0 or h <= 0:
        raise PipelineError(f"{label} has non-positive size: {rect!r}")
    bw, bh = bounds
    if x < 0 or y < 0 or x + w > bw or y + h > bh:
        raise PipelineError(f"{label} out of bounds {bounds}: {rect!r}")


def rects_overlap(left: list[Any], right: list[Any]) -> bool:
    lx, ly, lw, lh = [int(v) for v in left]
    rx, ry, rw, rh = [int(v) for v in right]
    return lx < rx + rw and lx + lw > rx and ly < ry + rh and ly + lh > ry


def validate_manifest(path: Path) -> int:
    manifest = load_json(path)
    assets = manifest.get("assets", [])
    if not isinstance(assets, list) or not assets:
        raise PipelineError("Manifest must contain a non-empty assets array.")

    ids: set[str] = set()
    errors: list[str] = []
    warnings: list[str] = []

    for asset in assets:
        asset_id = str(asset.get("id", "")).strip()
        if not asset_id:
            errors.append("Asset missing id.")
            continue
        if asset_id in ids:
            errors.append(f"Duplicate asset id: {asset_id}")
        ids.add(asset_id)

        final_size = asset.get("final_size")
        if not isinstance(final_size, list) or len(final_size) != 2:
            errors.append(f"{asset_id}: final_size must be [w, h].")
            continue
        bounds = (int(final_size[0]), int(final_size[1]))
        if bounds[0] <= 0 or bounds[1] <= 0:
            errors.append(f"{asset_id}: invalid final_size {final_size!r}.")
            continue

        final_path = str(asset.get("final_path", ""))
        if not final_path:
            errors.append(f"{asset_id}: missing final_path.")
        elif "assetized" in final_path.replace("\\", "/").split("/"):
            errors.append(f"{asset_id}: final_path must not target legacy assetized directory.")

        dynamic_zones = asset.get("dynamic_text_rects", [])
        forbidden_zones = asset.get("forbidden_zones", [])

        for zone in dynamic_zones:
            try:
                assert_rect_inside(zone["rect"], bounds, f"{asset_id}.dynamic_text_rects.{zone.get('id', '?')}")
            except Exception as exc:
                errors.append(str(exc))
            if zone.get("noise") != "low":
                warnings.append(f"{asset_id}.{zone.get('id', '?')}: dynamic text zone should declare noise='low'.")

        for zone in forbidden_zones:
            try:
                assert_rect_inside(zone["rect"], bounds, f"{asset_id}.forbidden_zones.{zone.get('id', '?')}")
            except Exception as exc:
                errors.append(str(exc))

        for text_zone in dynamic_zones:
            text_rect = text_zone.get("rect")
            if not isinstance(text_rect, list) or len(text_rect) != 4:
                continue
            for forbidden_zone in forbidden_zones:
                forbidden_rect = forbidden_zone.get("rect")
                if not isinstance(forbidden_rect, list) or len(forbidden_rect) != 4:
                    continue
                if rects_overlap(text_rect, forbidden_rect):
                    errors.append(
                        f"{asset_id}.{text_zone.get('id', '?')}: dynamic text zone overlaps forbidden zone "
                        f"{forbidden_zone.get('id', '?')}."
                    )

        for frame in asset.get("frames", []):
            try:
                assert_rect_inside(frame["rect"], bounds, f"{asset_id}.frames.{frame.get('id', '?')}")
            except Exception as exc:
                errors.append(str(exc))

        if "hot_rect" in asset:
            try:
                assert_rect_inside(asset["hot_rect"], bounds, f"{asset_id}.hot_rect")
            except Exception as exc:
                errors.append(str(exc))

        if "hit_rect" in asset:
            try:
                assert_rect_inside(asset["hit_rect"], bounds, f"{asset_id}.hit_rect")
            except Exception as exc:
                errors.append(str(exc))

        for hit_id, hit_rect in asset.get("hit_rects", {}).items():
            try:
                assert_rect_inside(hit_rect, bounds, f"{asset_id}.hit_rects.{hit_id}")
            except Exception as exc:
                errors.append(str(exc))

        transparent_models = {"codex-image2-chroma-key", "gpt-5-image", "human-art-tool-transparent"}
        if asset.get("background") == "transparent" and asset.get("model") not in transparent_models:
            errors.append(
                f"{asset_id}: transparent assets must use codex-image2-chroma-key, "
                "gpt-5-image, or human-art-tool-transparent."
            )

        if asset.get("background") == "opaque" and asset.get("model") in {"gpt-5-image", "codex-image2-chroma-key"}:
            warnings.append(f"{asset_id}: opaque asset should use codex-image2 or a human art tool source.")

    report = {
        "manifest": str(path),
        "asset_count": len(assets),
        "errors": errors,
        "warnings": warnings,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if errors else 0


def build_openrouter_args(
    job: dict[str, Any],
    shared_negative: list[str],
    approved_artboard: Path | None,
    dry_run: bool,
) -> list[str] | None:
    if not job.get("enabled", True):
        return None
    bundle_id = str(job.get("bundle_id", "world_map_imagegen"))
    args = [
        sys.executable,
        str(OPENROUTER_SCRIPT),
        "generate",
        "--prompt",
        str(job["prompt"]),
        "--user-request",
        f"{bundle_id}::{job['id']}",
        "--asset-type",
        str(job["asset_type"]),
        "--background",
        str(job["background"]),
        "--model",
        str(job["model"]),
        "--count",
        str(job.get("count", 1)),
        "--slug",
        str(job["slug"]),
    ]
    if resolution := job.get("resolution"):
        args.extend(["--resolution", str(resolution)])
    if aspect_ratio := job.get("aspect_ratio"):
        args.extend(["--aspect-ratio", str(aspect_ratio)])
    if image_size := job.get("image_size"):
        args.extend(["--image-size", str(image_size)])

    for negative in shared_negative:
        args.extend(["--negative", negative])

    for ref in job.get("reference_images", []):
        ref_path = str(ref.get("path", ""))
        if ref_path == "APPROVED_ARTBOARD":
            if approved_artboard is None:
                return None
            resolved = approved_artboard
        else:
            resolved = repo_path(ref_path)
        args.extend(["--reference-image", str(resolved)])

    if dry_run:
        args.append("--dry-run")
    return args


def find_job(bundle: dict[str, Any], job_id: str) -> dict[str, Any]:
    for job in bundle.get("jobs", []):
        if str(job.get("id", "")) == job_id:
            return job
    raise PipelineError(f"Prompt bundle does not contain job: {job_id}")


def build_codex_prompt(path: Path, job_id: str, approved_artboard: Path | None) -> int:
    bundle = load_json(path)
    job = find_job(bundle, job_id)
    job["bundle_id"] = str(bundle.get("id", "world_map_imagegen"))
    shared_negative = [str(value) for value in bundle.get("shared_negative", [])]
    reference_images: list[dict[str, str]] = []
    skipped: list[dict[str, str]] = []

    for ref in job.get("reference_images", []):
        ref_path = str(ref.get("path", ""))
        if ref_path == "APPROVED_ARTBOARD":
            if approved_artboard is None:
                skipped.append({"path": ref_path, "reason": "requires --approved-artboard"})
                continue
            resolved = approved_artboard
        else:
            resolved = repo_path(ref_path)
        reference_images.append(
            {
                "path": str(resolved),
                "role": str(ref.get("role", "")),
            }
        )

    prompt_text = (
        f"{job['prompt']}\n\n"
        "Use Codex built-in Image 2 / gpt-image-2 as the image generator. "
        f"Generate a production bitmap source image for the Angus {bundle.get('id', 'world_map_imagegen')} asset pipeline. "
        "The image will later be cropped, resized, padded, and checked by scripts; do not rely on the generator to create final Godot text or state. "
        f"Avoid: {'; '.join(shared_negative)}."
    )
    result = {
        "job_id": job_id,
        "stage": job.get("stage"),
        "primary_provider": "codex_builtin_image2",
        "prompt_text": prompt_text,
        "reference_images": reference_images,
        "skipped_reference_images": skipped,
        "after_generation": [
            "Save or copy the selected Codex Image 2 output into a stable local path.",
            "Run stage-source to copy it into image_gen/codex_image2_sources/YYYY-MM-DD/ with metadata.",
            "Use the staged source path in a postprocess mapping file.",
            "Run postprocess, validate-final-assets, and review-overlays before any Godot wiring.",
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def stage_source(
    manifest_path: Path,
    prompt_bundle_path: Path,
    asset_id: str,
    source_path: Path,
    provider: str,
    job_id: str | None,
    slug: str | None,
    out_root: Path,
) -> int:
    manifest = load_json(manifest_path)
    asset = next((item for item in manifest.get("assets", []) if item.get("id") == asset_id), None)
    if asset is None:
        raise PipelineError(f"Manifest does not contain asset id: {asset_id}")
    if not source_path.exists():
        raise PipelineError(f"Source image not found: {source_path}")
    if source_path.suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp"}:
        raise PipelineError(f"Unsupported source image suffix: {source_path.suffix}")

    prompt_info: dict[str, Any] | None = None
    if job_id:
        bundle = load_json(prompt_bundle_path)
        job = find_job(bundle, job_id)
        prompt_info = {
            "job_id": job_id,
            "stage": job.get("stage"),
            "prompt": job.get("prompt"),
            "shared_negative": bundle.get("shared_negative", []),
        }

    date_dir = out_root / datetime.now().strftime("%Y-%m-%d")
    date_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    safe_slug = slugify(slug or asset_id)
    target = date_dir / f"{timestamp}_{safe_slug}{source_path.suffix.lower()}"
    metadata = target.with_suffix(".json")
    shutil.copy2(source_path, target)

    metadata.write_text(
        json.dumps(
            {
                "provider": provider,
                "asset_id": asset_id,
                "source_original": str(source_path),
                "staged_source": str(target),
                "manifest": str(manifest_path),
                "manifest_final_path": asset.get("final_path"),
                "manifest_final_size": asset.get("final_size"),
                "prompt_info": prompt_info,
                "postprocess_mapping_snippet": {
                    asset_id: {
                        "source": str(target.relative_to(ROOT)).replace("\\", "/") if target.is_relative_to(ROOT) else str(target),
                        "mode": "cover" if asset.get("background") == "opaque" else "contain",
                        "crop": None,
                    }
                },
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "staged_source": str(target),
                "metadata": str(metadata),
                "mapping_snippet": {
                    asset_id: {
                        "source": str(target.relative_to(ROOT)).replace("\\", "/") if target.is_relative_to(ROOT) else str(target),
                        "mode": "cover" if asset.get("background") == "opaque" else "contain",
                        "crop": None,
                    }
                },
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def emit_commands(path: Path, stage: str | None, approved_artboard: Path | None, dry_run: bool) -> int:
    bundle = load_json(path)
    shared_negative = [str(value) for value in bundle.get("shared_negative", [])]
    commands: list[str] = []
    skipped: list[str] = []

    for job in bundle.get("jobs", []):
        if stage and job.get("stage") != stage and job.get("id") != stage:
            continue
        if job.get("requires_approved_artboard") and approved_artboard is None:
            skipped.append(str(job["id"]))
            continue
        job["bundle_id"] = str(bundle.get("id", "world_map_imagegen"))
        args = build_openrouter_args(job, shared_negative, approved_artboard, dry_run)
        if args is None:
            skipped.append(str(job["id"]))
            continue
        commands.append("& " + " ".join(ps_quote(arg) for arg in args))

    result = {
        "prompt_bundle": str(path),
        "dry_run": dry_run,
        "stage_filter": stage,
        "approved_artboard": str(approved_artboard) if approved_artboard else None,
        "commands": commands,
        "skipped_requires_approved_artboard": skipped,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def run_job(path: Path, job_id: str, approved_artboard: Path | None, dry_run: bool) -> int:
    bundle = load_json(path)
    job = find_job(bundle, job_id)
    job["bundle_id"] = str(bundle.get("id", "world_map_imagegen"))
    if job.get("requires_approved_artboard") and approved_artboard is None:
        raise PipelineError(f"{job_id} requires --approved-artboard.")
    args = build_openrouter_args(job, [str(value) for value in bundle.get("shared_negative", [])], approved_artboard, dry_run)
    if args is None:
        raise PipelineError(f"{job_id} is disabled or cannot be built.")
    print("Running image generation job:")
    print(" ".join(ps_quote(arg) for arg in args))
    completed = subprocess.run(args, cwd=ROOT)
    return int(completed.returncode)


def crop_resize(source: Path, target: Path, final_size: tuple[int, int], crop: list[int] | None, mode: str) -> None:
    try:
        from PIL import Image
    except ImportError as exc:
        raise PipelineError("Pillow is required for postprocess/review commands.") from exc

    image = Image.open(source).convert("RGBA")
    if crop:
        x, y, w, h = [int(v) for v in crop]
        image = image.crop((x, y, x + w, y + h))

    target_w, target_h = final_size
    if mode == "stretch":
        output = image.resize(final_size, Image.Resampling.LANCZOS)
    else:
        scale = max(target_w / image.width, target_h / image.height) if mode == "cover" else min(target_w / image.width, target_h / image.height)
        new_size = (max(1, round(image.width * scale)), max(1, round(image.height * scale)))
        resized = image.resize(new_size, Image.Resampling.LANCZOS)
        output = Image.new("RGBA", final_size, (0, 0, 0, 0))
        left = (target_w - resized.width) // 2
        top = (target_h - resized.height) // 2
        output.alpha_composite(resized, (left, top))

    target.parent.mkdir(parents=True, exist_ok=True)
    output.save(target)


def postprocess(manifest_path: Path, mapping_path: Path) -> int:
    manifest = load_json(manifest_path)
    mapping = load_json(mapping_path)
    by_id = {asset["id"]: asset for asset in manifest.get("assets", [])}
    processed: list[dict[str, str]] = []
    errors: list[str] = []

    for asset_id, spec in mapping.get("assets", {}).items():
        asset = by_id.get(asset_id)
        if asset is None:
            errors.append(f"Unknown asset in mapping: {asset_id}")
            continue
        source = repo_path(str(spec.get("source", "")))
        if not source.exists():
            errors.append(f"{asset_id}: source image not found: {source}")
            continue
        final_size = (int(asset["final_size"][0]), int(asset["final_size"][1]))
        target = repo_path(str(asset["final_path"]))
        mode = str(spec.get("mode", "cover"))
        crop = spec.get("crop")
        if mode not in {"cover", "contain", "stretch"}:
            errors.append(f"{asset_id}: mode must be cover, contain, or stretch.")
            continue
        crop_resize(source, target, final_size, crop, mode)
        processed.append({"asset_id": asset_id, "source": str(source), "target": str(target)})

    result = {"processed": processed, "errors": errors}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if errors else 0


def validate_final_assets(manifest_path: Path) -> int:
    try:
        from PIL import Image
    except ImportError as exc:
        raise PipelineError("Pillow is required for final asset validation.") from exc

    manifest = load_json(manifest_path)
    checked: list[dict[str, Any]] = []
    missing: list[str] = []
    errors: list[str] = []
    warnings: list[str] = []

    for asset in manifest.get("assets", []):
        asset_id = str(asset.get("id", ""))
        final_path = repo_path(str(asset.get("final_path", "")))
        expected_size = tuple(int(value) for value in asset.get("final_size", [0, 0]))
        if not final_path.exists():
            missing.append(str(final_path))
            continue
        with Image.open(final_path) as image:
            actual_size = image.size
            has_alpha = image.mode in {"RGBA", "LA"} or ("transparency" in image.info)
            if actual_size != expected_size:
                errors.append(f"{asset_id}: expected {expected_size}, got {actual_size}")
            if asset.get("background") == "transparent" and not has_alpha:
                errors.append(f"{asset_id}: expected transparent asset with alpha channel.")
            if asset.get("background") == "opaque" and has_alpha:
                alpha = image.convert("RGBA").getchannel("A")
                if alpha.getextrema() != (255, 255):
                    warnings.append(f"{asset_id}: opaque asset contains non-opaque alpha pixels.")
            checked.append(
                {
                    "asset_id": asset_id,
                    "path": str(final_path),
                    "expected_size": list(expected_size),
                    "actual_size": list(actual_size),
                    "has_alpha": has_alpha,
                }
            )

    result = {
        "manifest": str(manifest_path),
        "checked": checked,
        "missing": missing,
        "errors": errors,
        "warnings": warnings,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if errors else 0


def make_review_overlays(manifest_path: Path, out_dir: Path) -> int:
    try:
        from PIL import Image, ImageDraw
    except ImportError as exc:
        raise PipelineError("Pillow is required for review overlays.") from exc

    manifest = load_json(manifest_path)
    out_dir.mkdir(parents=True, exist_ok=True)
    generated: list[str] = []
    missing: list[str] = []

    for asset in manifest.get("assets", []):
        final_path = repo_path(str(asset.get("final_path", "")))
        if not final_path.exists():
            missing.append(str(final_path))
            continue
        image = Image.open(final_path).convert("RGBA")
        overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        for zone in asset.get("dynamic_text_rects", []):
            x, y, w, h = [int(v) for v in zone["rect"]]
            draw.rectangle((x, y, x + w, y + h), outline=(60, 255, 120, 230), width=3)
        for zone in asset.get("forbidden_zones", []):
            x, y, w, h = [int(v) for v in zone["rect"]]
            draw.rectangle((x, y, x + w, y + h), outline=(255, 60, 60, 230), width=3)
        for frame in asset.get("frames", []):
            x, y, w, h = [int(v) for v in frame["rect"]]
            draw.rectangle((x, y, x + w, y + h), outline=(60, 210, 255, 230), width=2)
        if "hot_rect" in asset:
            x, y, w, h = [int(v) for v in asset["hot_rect"]]
            draw.rectangle((x, y, x + w, y + h), outline=(255, 210, 60, 230), width=3)
        if "hit_rect" in asset:
            x, y, w, h = [int(v) for v in asset["hit_rect"]]
            draw.rectangle((x, y, x + w, y + h), outline=(255, 210, 60, 230), width=3)
        for hit_rect in asset.get("hit_rects", {}).values():
            x, y, w, h = [int(v) for v in hit_rect]
            draw.rectangle((x, y, x + w, y + h), outline=(255, 210, 60, 230), width=3)

        reviewed = Image.alpha_composite(image, overlay)
        out_path = out_dir / f"{asset['id']}-zones.png"
        reviewed.save(out_path)
        generated.append(str(out_path))

    result = {"generated": generated, "missing_final_assets": missing}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def parse_hex_color(value: str) -> tuple[int, int, int]:
    text = value.strip()
    if text.startswith("#"):
        text = text[1:]
    if len(text) != 6:
        raise PipelineError(f"Color must be #RRGGBB, got {value!r}.")
    try:
        return tuple(int(text[index:index + 2], 16) for index in (0, 2, 4))  # type: ignore[return-value]
    except ValueError as exc:
        raise PipelineError(f"Color must be #RRGGBB, got {value!r}.") from exc


def is_near_color(pixel: tuple[int, int, int, int], key: tuple[int, int, int], tolerance: int) -> bool:
    red, green, blue, _alpha = pixel
    return (
        abs(red - key[0]) <= tolerance
        and abs(green - key[1]) <= tolerance
        and abs(blue - key[2]) <= tolerance
    )


def extract_chromakey_atlas(
    manifest_path: Path,
    asset_id: str,
    source_path: Path,
    key_color: str,
    tolerance: int,
    expected_frames: int,
    max_frame_fill: int,
    min_column_pixels: int,
    group_gap: int,
) -> int:
    try:
        from PIL import Image
    except ImportError as exc:
        raise PipelineError("Pillow is required for chroma-key atlas extraction.") from exc

    manifest = load_json(manifest_path)
    asset = next((item for item in manifest.get("assets", []) if item.get("id") == asset_id), None)
    if asset is None:
        raise PipelineError(f"Manifest does not contain asset id: {asset_id}")
    if asset.get("background") != "transparent":
        raise PipelineError(f"{asset_id}: extract-chromakey-atlas requires a transparent manifest asset.")
    if not source_path.exists():
        raise PipelineError(f"Source image not found: {source_path}")

    final_size = tuple(int(value) for value in asset.get("final_size", [0, 0]))
    frame_size = tuple(int(value) for value in asset.get("frame_size", [0, 0]))
    if len(final_size) != 2 or len(frame_size) != 2 or final_size[0] <= 0 or final_size[1] <= 0:
        raise PipelineError(f"{asset_id}: final_size and frame_size must be positive [w, h].")
    frame_w, frame_h = frame_size
    if final_size[0] < frame_w * expected_frames or final_size[1] < frame_h:
        raise PipelineError(f"{asset_id}: final_size cannot contain {expected_frames} frames of {frame_size}.")

    key = parse_hex_color(key_color)
    source = Image.open(source_path).convert("RGBA")
    column_hits: list[int] = []
    for x in range(source.width):
        count = 0
        for y in range(source.height):
            if not is_near_color(source.getpixel((x, y)), key, tolerance):
                count += 1
        if count >= min_column_pixels:
            column_hits.append(x)

    groups: list[list[int]] = []
    for x in column_hits:
        if not groups or x - groups[-1][1] > group_gap:
            groups.append([x, x])
        else:
            groups[-1][1] = x

    if len(groups) != expected_frames:
        raise PipelineError(f"{asset_id}: expected {expected_frames} icon groups, got {len(groups)}: {groups!r}")

    atlas = Image.new("RGBA", final_size, (0, 0, 0, 0))
    frames: list[dict[str, Any]] = []
    for index, (x0, x1) in enumerate(groups):
        x0 = max(0, x0 - 12)
        x1 = min(source.width, x1 + 13)
        ys: list[int] = []
        for y in range(source.height):
            for x in range(x0, x1):
                if not is_near_color(source.getpixel((x, y)), key, tolerance):
                    ys.append(y)
                    break
        if not ys:
            raise PipelineError(f"{asset_id}: no pixels found for frame {index}.")
        y0 = max(0, min(ys) - 12)
        y1 = min(source.height, max(ys) + 13)
        crop = source.crop((x0, y0, x1, y1))
        pixels = crop.load()
        for y in range(crop.height):
            for x in range(crop.width):
                red, green, blue, alpha = pixels[x, y]
                if is_near_color((red, green, blue, alpha), key, tolerance):
                    pixels[x, y] = (red, green, blue, 0)
        bbox = crop.getchannel("A").getbbox()
        if bbox:
            crop = crop.crop(bbox)
        crop.thumbnail((max_frame_fill, max_frame_fill), Image.Resampling.LANCZOS)
        frame = Image.new("RGBA", frame_size, (0, 0, 0, 0))
        frame.alpha_composite(crop, ((frame_w - crop.width) // 2, (frame_h - crop.height) // 2))
        atlas.alpha_composite(frame, (index * frame_w, 0))
        frames.append({"index": index, "source_crop": [x0, y0, x1 - x0, y1 - y0]})

    target = repo_path(str(asset["final_path"]))
    target.parent.mkdir(parents=True, exist_ok=True)
    atlas.save(target)

    result = {"asset_id": asset_id, "source": str(source_path), "target": str(target), "frames": frames}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Plan, validate, and postprocess Angus world-map image-generation UI assets.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate = subparsers.add_parser("validate-manifest")
    validate.add_argument("--manifest", default=str(DEFAULT_MANIFEST))

    codex = subparsers.add_parser("codex-prompt")
    codex.add_argument("--prompt-bundle", default=str(DEFAULT_PROMPT_BUNDLE))
    codex.add_argument("--job", required=True, help="Prompt bundle job id to prepare for built-in Codex Image 2.")
    codex.add_argument("--approved-artboard", default=None, help="Approved artboard path for component prompt references.")

    stage = subparsers.add_parser("stage-source")
    stage.add_argument("--manifest", default=str(DEFAULT_MANIFEST))
    stage.add_argument("--prompt-bundle", default=str(DEFAULT_PROMPT_BUNDLE))
    stage.add_argument("--asset", required=True, help="Manifest asset id this source image belongs to.")
    stage.add_argument("--source", required=True, help="Codex Image 2 / art tool output image path.")
    stage.add_argument("--provider", default="codex-image2", help="Source generator label for metadata.")
    stage.add_argument("--job", default=None, help="Prompt bundle job id that produced the image.")
    stage.add_argument("--slug", default=None, help="Optional staged filename slug.")
    stage.add_argument("--out-root", default=str(DEFAULT_CODEX_SOURCE_ROOT))

    emit = subparsers.add_parser("emit-commands")
    emit.add_argument("--prompt-bundle", default=str(DEFAULT_PROMPT_BUNDLE))
    emit.add_argument("--stage", default=None, help="Filter by stage or job id.")
    emit.add_argument("--approved-artboard", default=None, help="Approved artboard path for component jobs.")
    emit.add_argument("--dry-run", action="store_true")

    run = subparsers.add_parser("run-job")
    run.add_argument("--prompt-bundle", default=str(DEFAULT_PROMPT_BUNDLE))
    run.add_argument("--job", required=True, help="Prompt bundle job id to execute.")
    run.add_argument("--approved-artboard", default=None, help="Approved artboard path for component jobs.")
    run.add_argument("--dry-run", action="store_true")

    pack = subparsers.add_parser("postprocess")
    pack.add_argument("--manifest", default=str(DEFAULT_MANIFEST))
    pack.add_argument("--mapping", required=True, help="JSON mapping from asset id to generated source/crop/mode.")

    final = subparsers.add_parser("validate-final-assets")
    final.add_argument("--manifest", default=str(DEFAULT_MANIFEST))

    review = subparsers.add_parser("review-overlays")
    review.add_argument("--manifest", default=str(DEFAULT_MANIFEST))
    review.add_argument("--out-dir", default=str(DEFAULT_REVIEW_DIR))

    chroma = subparsers.add_parser("extract-chromakey-atlas")
    chroma.add_argument("--manifest", default=str(DEFAULT_MANIFEST))
    chroma.add_argument("--asset", required=True, help="Transparent atlas asset id in the manifest.")
    chroma.add_argument("--source", required=True, help="Chroma-key source image from Codex Image 2 / art tool.")
    chroma.add_argument("--key-color", default="#ff00ff", help="Flat background color to remove.")
    chroma.add_argument("--tolerance", type=int, default=90, help="Per-channel tolerance for chroma-key removal.")
    chroma.add_argument("--expected-frames", type=int, default=8, help="Expected number of horizontal icon groups.")
    chroma.add_argument("--max-frame-fill", type=int, default=58, help="Max icon size inside each frame.")
    chroma.add_argument("--min-column-pixels", type=int, default=5, help="Minimum non-key pixels for a source column to be considered occupied.")
    chroma.add_argument("--group-gap", type=int, default=1, help="Horizontal gap allowed inside one icon group.")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        if args.command == "validate-manifest":
            return validate_manifest(repo_path(args.manifest))
        if args.command == "codex-prompt":
            approved = repo_path(args.approved_artboard) if args.approved_artboard else None
            return build_codex_prompt(repo_path(args.prompt_bundle), args.job, approved)
        if args.command == "stage-source":
            return stage_source(
                manifest_path=repo_path(args.manifest),
                prompt_bundle_path=repo_path(args.prompt_bundle),
                asset_id=args.asset,
                source_path=repo_path(args.source),
                provider=args.provider,
                job_id=args.job,
                slug=args.slug,
                out_root=repo_path(args.out_root),
            )
        if args.command == "emit-commands":
            approved = repo_path(args.approved_artboard) if args.approved_artboard else None
            return emit_commands(repo_path(args.prompt_bundle), args.stage, approved, args.dry_run)
        if args.command == "run-job":
            approved = repo_path(args.approved_artboard) if args.approved_artboard else None
            return run_job(repo_path(args.prompt_bundle), args.job, approved, args.dry_run)
        if args.command == "postprocess":
            return postprocess(repo_path(args.manifest), repo_path(args.mapping))
        if args.command == "validate-final-assets":
            return validate_final_assets(repo_path(args.manifest))
        if args.command == "review-overlays":
            return make_review_overlays(repo_path(args.manifest), repo_path(args.out_dir))
        if args.command == "extract-chromakey-atlas":
            return extract_chromakey_atlas(
                manifest_path=repo_path(args.manifest),
                asset_id=args.asset,
                source_path=repo_path(args.source),
                key_color=args.key_color,
                tolerance=args.tolerance,
                expected_frames=args.expected_frames,
                max_frame_fill=args.max_frame_fill,
                min_column_pixels=args.min_column_pixels,
                group_gap=args.group_gap,
            )
    except PipelineError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
