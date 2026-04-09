from __future__ import annotations

import argparse
import base64
import hashlib
import json
import mimetypes
import os
import re
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib import error, parse, request


SKILL_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = SKILL_DIR.parents[1]
CONFIG_PATH = SKILL_DIR / "config.env"
CONFIG_EXAMPLE_PATH = SKILL_DIR / "config.env.example"
OUTPUT_ROOT = REPO_ROOT / "image_gen"

SUPPORTED_IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp", ".gif"}
SUPPORTED_GEMINI_RESOLUTIONS = {
    "1024x1024": "1:1",
    "832x1248": "2:3",
    "1248x832": "3:2",
    "864x1184": "3:4",
    "1184x864": "4:3",
    "896x1152": "4:5",
    "1152x896": "5:4",
    "768x1344": "9:16",
    "1344x768": "16:9",
    "1536x672": "21:9",
}
STANDARD_GEMINI_ASPECT_RATIOS = {
    "1:1",
    "2:3",
    "3:2",
    "3:4",
    "4:3",
    "4:5",
    "5:4",
    "9:16",
    "16:9",
    "21:9",
}
EXTENDED_NANO_BANANA_2_ASPECT_RATIOS = {"1:4", "4:1", "1:8", "8:1"}
GPT_IMAGE_RESOLUTIONS = {"1024x1024", "1536x1024", "1024x1536", "auto"}
GPT_IMAGE_BACKGROUND = {"transparent", "opaque", "auto"}
NANO_BANANA_IMAGE_SIZES = {"1K", "2K", "4K"}
NANO_BANANA_2_IMAGE_SIZES = {"0.5K", "1K", "2K", "4K"}
SUPPORTED_COUNT_RANGE = range(1, 9)
MAX_REFERENCE_IMAGES = 4

MODEL_ALIASES = {
    "auto": "auto",
    "gpt-5-image": "openai/gpt-5-image",
    "openai/gpt-5-image": "openai/gpt-5-image",
    "nano-banana": "google/gemini-2.5-flash-image",
    "google/gemini-2.5-flash-image": "google/gemini-2.5-flash-image",
    "nano-banana-2": "google/gemini-3.1-flash-image-preview",
    "google/gemini-3.1-flash-image-preview": "google/gemini-3.1-flash-image-preview",
}

TRANSPARENT_FIRST_ASSET_TYPES = {
    "icon",
    "item",
    "prop",
    "sprite",
    "vfx",
    "decal",
    "logo-mark",
    "isometric-asset",
}

ASSET_TYPE_SUFFIXES = {
    "icon": "game icon, centered composition, readable silhouette, clean cutout, production-ready asset",
    "item": "isolated game item, clean contour, production-ready asset, readable at small size",
    "prop": "isolated game prop, clear shape language, clean cutout, production-ready asset",
    "sprite": "2D game sprite, clean outline, animation-friendly silhouette, readable at gameplay scale",
    "vfx": "game VFX asset, emissive effect shape, clean alpha edges, production-ready effect sheet look",
    "decal": "game decal graphic, flat readable graphic language, edge-safe cutout",
    "texture": "game texture study, material-first read, even detail distribution, production-ready material source",
    "tileable-texture": "seamless tileable game texture, edge continuity, even coverage, material-first read",
    "portrait": "portrait concept art, clear face read, costume readability, production-ready character render",
    "character-concept": "character concept art, costume readability, silhouette clarity, production-ready game character design",
    "creature-concept": "creature concept art, anatomy clarity, threat readability, production-ready creature design",
    "environment-concept": "environment concept art, layered depth, strong lighting story, production-ready world-building image",
    "background": "game background art, gameplay-safe composition, horizon clarity, production-ready background plate",
    "key-art": "game key art, hero composition, strong focal hierarchy, premium marketing illustration",
    "poster": "game poster illustration, graphic hierarchy, premium marketing composition, clear focal design",
    "ui-screen": "full game UI screen mockup, readable panel hierarchy, production-ready interface concept, interaction-first composition",
    "ui-banner": "game UI banner art, controlled empty space for overlays, strong focal hierarchy",
    "logo-mark": "game logo mark, clean shape design, bold read, minimal clutter",
    "card-art": "game card illustration, focal composition, frame-aware subject placement",
    "isometric-asset": "isometric game asset, consistent angle, clean volume read, production-ready asset",
}

ASSET_TYPE_NEGATIVES = {
    "shared": [
        "watermark",
        "signature",
        "artist name",
        "copyright stamp",
        "frame border",
        "presentation mockup",
        "ui chrome",
        "drop shadow",
        "cropped subject",
        "cut off limbs",
        "duplicate objects",
        "extra fingers",
        "broken anatomy",
        "unreadable text",
        "muddy details",
        "jpeg artifacts",
        "oversaturated colors",
        "noisy background",
        "inconsistent lighting",
    ],
    "transparent": [
        "background scene",
        "floor shadow",
        "environmental clutter",
        "vignette",
    ],
    "texture": [
        "visible seams",
        "hard lighting hotspots",
        "perspective scene elements",
    ],
    "tileable-texture": [
        "visible seams",
        "hard lighting hotspots",
        "perspective scene elements",
    ],
    "poster": [
        "accidental logos",
        "misspelled typography",
        "random stickers",
    ],
    "ui-banner": [
        "accidental logos",
        "misspelled typography",
        "random stickers",
    ],
    "ui-screen": [
        "accidental logos",
        "misspelled typography",
        "floating panels without structure",
        "illegible ui labels",
    ],
    "portrait": [
        "asymmetrical eyes",
        "malformed hands",
        "fused accessories",
    ],
    "character-concept": [
        "asymmetrical eyes",
        "malformed hands",
        "fused accessories",
    ],
    "creature-concept": [
        "merged limbs",
        "broken anatomy",
    ],
}

DEFAULT_GEMINI_ASPECT_RATIOS = {
    "icon": "1:1",
    "item": "1:1",
    "prop": "1:1",
    "sprite": "1:1",
    "vfx": "1:1",
    "decal": "1:1",
    "texture": "1:1",
    "tileable-texture": "1:1",
    "portrait": "3:4",
    "character-concept": "3:4",
    "creature-concept": "2:3",
    "environment-concept": "16:9",
    "background": "16:9",
    "key-art": "3:4",
    "poster": "3:4",
    "ui-screen": "16:9",
    "ui-banner": "16:9",
    "logo-mark": "1:1",
    "card-art": "3:4",
    "isometric-asset": "1:1",
}

DEFAULT_GEMINI_IMAGE_SIZES = {
    "icon": "1K",
    "item": "1K",
    "prop": "1K",
    "sprite": "1K",
    "vfx": "1K",
    "decal": "1K",
    "texture": "2K",
    "tileable-texture": "2K",
    "portrait": "1K",
    "character-concept": "2K",
    "creature-concept": "2K",
    "environment-concept": "2K",
    "background": "2K",
    "key-art": "2K",
    "poster": "2K",
    "ui-screen": "2K",
    "ui-banner": "2K",
    "logo-mark": "1K",
    "card-art": "2K",
    "isometric-asset": "1K",
}


class ValidationError(RuntimeError):
    pass


@dataclass
class PlannedRequest:
    original_prompt: str
    compiled_prompt: str
    asset_type: str
    background: str
    model: str
    model_reason: str
    count: int
    slug: str
    resolution: str | None
    aspect_ratio: str | None
    image_size: str | None
    quality: str
    output_format: str
    output_compression: int | None
    seed: int | None
    reference_images: list[Path]
    negative_constraints: list[str]
    inference_notes: list[str]
    provider_object: dict[str, Any]


def load_env_file(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def load_config() -> dict[str, str]:
    config = load_env_file(CONFIG_PATH)
    for key, value in os.environ.items():
        if key.startswith("OPENROUTER_"):
            config[key] = value
    return config


def require_api_key(config: dict[str, str]) -> str:
    api_key = config.get("OPENROUTER_API_KEY", "").strip()
    if not api_key:
        raise ValidationError(
            f"Missing OPENROUTER_API_KEY. Copy {CONFIG_EXAMPLE_PATH} to {CONFIG_PATH} and fill it before generating."
        )
    return api_key


def slugify(text: str) -> str:
    lowered = text.strip().lower()
    lowered = re.sub(r"[^a-z0-9]+", "-", lowered)
    lowered = lowered.strip("-")
    return lowered[:80] or "image"


def infer_background(background: str, asset_type: str, notes: list[str]) -> str:
    if background != "auto":
        return background
    if asset_type in TRANSPARENT_FIRST_ASSET_TYPES:
        notes.append(f"Inferred transparent background from asset_type={asset_type}.")
        return "transparent"
    notes.append(f"Inferred opaque background from asset_type={asset_type}.")
    return "opaque"


def normalize_model(model: str) -> str:
    normalized = MODEL_ALIASES.get(model.strip().lower())
    if not normalized:
        allowed = ", ".join(sorted(MODEL_ALIASES))
        raise ValidationError(f"Unsupported model alias '{model}'. Allowed values: {allowed}")
    return normalized


def choose_model(
    asset_type: str,
    background: str,
    requested_model: str,
    references: list[Path],
    prompt: str,
    aspect_ratio: str | None,
    image_size: str | None,
    notes: list[str],
) -> tuple[str, str]:
    normalized_model = normalize_model(requested_model)
    if background == "transparent":
        if normalized_model not in {"auto", "openai/gpt-5-image"}:
            raise ValidationError("Transparent background requests must use GPT-5 Image in this skill.")
        return "openai/gpt-5-image", "Transparent background requested; GPT-5 Image is the only supported transparent model in this skill."

    if normalized_model == "google/gemini-2.5-flash-image":
        return normalized_model, "User explicitly selected Nano Banana."
    if normalized_model == "google/gemini-3.1-flash-image-preview":
        return normalized_model, "User explicitly selected Nano Banana 2."
    if normalized_model == "openai/gpt-5-image":
        raise ValidationError("Opaque requests in this skill must route to Nano Banana or Nano Banana 2, not GPT-5 Image.")

    lower_prompt = prompt.lower()
    score = 0
    if asset_type in {"key-art", "poster", "ui-banner", "environment-concept"}:
        score += 2
    if len(references) > 1:
        score += 2
    if aspect_ratio in EXTENDED_NANO_BANANA_2_ASPECT_RATIOS:
        score += 3
    if image_size == "4K":
        score += 1
    for marker in (
        "poster",
        "key art",
        "marketing",
        "banner",
        "title treatment",
        "multi character",
        "multi-character",
        "crowd",
        "complex",
        "intricate",
        "layout",
        "typography",
        "logo",
        "story scene",
        "cinematic",
    ):
        if marker in lower_prompt:
            score += 2
            break
    if score >= 3:
        notes.append("Selected Nano Banana 2 because the request is composition-heavy or reference-heavy.")
        return "google/gemini-3.1-flash-image-preview", "Complex opaque request: multi-element or higher-control composition."
    notes.append("Selected Nano Banana because the request is a simpler opaque generation task.")
    return "google/gemini-2.5-flash-image", "Simpler opaque request: faster image generation is sufficient."


def validate_count(count: int) -> None:
    if count not in SUPPORTED_COUNT_RANGE:
        raise ValidationError(f"count must be between 1 and 8. Received: {count}")


def validate_references(reference_images: list[Path]) -> None:
    if len(reference_images) > MAX_REFERENCE_IMAGES:
        raise ValidationError(f"This skill supports up to {MAX_REFERENCE_IMAGES} reference images per request. Received: {len(reference_images)}")
    for image_path in reference_images:
        if not image_path.exists():
            raise ValidationError(f"Reference image does not exist: {image_path}")
        if image_path.suffix.lower() not in SUPPORTED_IMAGE_SUFFIXES:
            allowed = ", ".join(sorted(SUPPORTED_IMAGE_SUFFIXES))
            raise ValidationError(f"Unsupported reference image format: {image_path.name}. Allowed suffixes: {allowed}")


def normalize_resolution(value: str | None) -> str | None:
    if value is None:
        return None
    text = value.strip().lower()
    if text == "auto":
        return "auto"
    if not re.fullmatch(r"\d+x\d+", text):
        raise ValidationError(f"resolution must look like WIDTHxHEIGHT or auto. Received: {value}")
    return text


def map_gpt_image_resolution(asset_type: str, aspect_ratio: str | None) -> str:
    if aspect_ratio == "1:1" or asset_type in {"icon", "item", "prop", "sprite", "vfx", "decal", "logo-mark", "texture", "tileable-texture", "isometric-asset"}:
        return "1024x1024"
    if aspect_ratio in {"2:3", "3:4", "4:5", "9:16"} or asset_type in {"portrait", "character-concept", "creature-concept", "card-art", "poster"}:
        return "1024x1536"
    return "1536x1024"


def validate_transparent_request(
    resolution: str | None,
    aspect_ratio: str | None,
    background: str,
    output_format: str,
    quality: str,
) -> tuple[str, str]:
    if background not in GPT_IMAGE_BACKGROUND:
        allowed = ", ".join(sorted(GPT_IMAGE_BACKGROUND))
        raise ValidationError(f"Unsupported GPT Image background value: {background}. Allowed: {allowed}")
    if resolution and resolution not in GPT_IMAGE_RESOLUTIONS:
        allowed = ", ".join(sorted(GPT_IMAGE_RESOLUTIONS))
        raise ValidationError(f"Unsupported transparent resolution: {resolution}. Allowed: {allowed}")
    if aspect_ratio and aspect_ratio not in {"1:1", "2:3", "3:2", "3:4", "4:3", "4:5", "5:4", "9:16", "16:9"}:
        raise ValidationError(
            "Transparent GPT-5 Image requests only accept square, portrait, or landscape ratios that can map to 1024x1024, 1024x1536, or 1536x1024."
        )
    if quality not in {"low", "medium", "high", "auto"}:
        raise ValidationError("quality must be one of low, medium, high, auto")

    resolved_format = output_format
    if background == "transparent":
        if output_format == "jpeg":
            raise ValidationError("Transparent GPT-5 Image output only supports png or webp.")
        if output_format == "auto":
            resolved_format = "png"
    elif output_format == "auto":
        resolved_format = "png"
    return resolution or "auto", resolved_format


def validate_gemini_request(model: str, resolution: str | None, aspect_ratio: str | None, image_size: str | None) -> tuple[str, str]:
    if resolution:
        if resolution == "auto":
            raise ValidationError("Gemini requests in this skill do not accept resolution=auto. Use an allowed literal Gemini resolution or aspect_ratio + image_size.")
        mapped_aspect_ratio = SUPPORTED_GEMINI_RESOLUTIONS.get(resolution)
        if not mapped_aspect_ratio:
            allowed = ", ".join(sorted(SUPPORTED_GEMINI_RESOLUTIONS))
            raise ValidationError(
                f"Unsupported literal Gemini resolution: {resolution}. Allowed literal resolutions: {allowed}. Otherwise use --aspect-ratio plus --image-size."
            )
        if aspect_ratio and aspect_ratio != mapped_aspect_ratio:
            raise ValidationError(f"resolution={resolution} maps to aspect_ratio={mapped_aspect_ratio}, which conflicts with explicit aspect_ratio={aspect_ratio}.")
        aspect_ratio = mapped_aspect_ratio
        image_size = image_size or "1K"

    if not aspect_ratio:
        aspect_ratio = "1:1"
    allowed_aspects = set(STANDARD_GEMINI_ASPECT_RATIOS)
    if model == "google/gemini-3.1-flash-image-preview":
        allowed_aspects |= EXTENDED_NANO_BANANA_2_ASPECT_RATIOS
    if aspect_ratio not in allowed_aspects:
        allowed = ", ".join(sorted(allowed_aspects))
        raise ValidationError(f"Unsupported aspect_ratio={aspect_ratio} for model={model}. Allowed: {allowed}")

    if not image_size:
        image_size = "1K"
    allowed_sizes = NANO_BANANA_IMAGE_SIZES if model == "google/gemini-2.5-flash-image" else NANO_BANANA_2_IMAGE_SIZES
    if image_size not in allowed_sizes:
        allowed = ", ".join(sorted(allowed_sizes))
        raise ValidationError(f"Unsupported image_size={image_size} for model={model}. Allowed: {allowed}")
    return aspect_ratio, image_size


def default_gemini_aspect_ratio(asset_type: str) -> str:
    return DEFAULT_GEMINI_ASPECT_RATIOS.get(asset_type, "1:1")


def default_gemini_image_size(asset_type: str, model: str) -> str:
    preferred = DEFAULT_GEMINI_IMAGE_SIZES.get(asset_type, "1K")
    if preferred == "0.5K" and model != "google/gemini-3.1-flash-image-preview":
        return "1K"
    if preferred == "4K" and model == "google/gemini-2.5-flash-image":
        return "4K"
    return preferred


def build_negative_constraints(asset_type: str, background: str, user_negatives: list[str]) -> list[str]:
    negatives = list(ASSET_TYPE_NEGATIVES["shared"])
    if background == "transparent":
        negatives.extend(ASSET_TYPE_NEGATIVES["transparent"])
    negatives.extend(ASSET_TYPE_NEGATIVES.get(asset_type, []))
    negatives.extend(item.strip() for item in user_negatives if item.strip())
    seen: set[str] = set()
    deduped: list[str] = []
    for item in negatives:
        lowered = item.lower()
        if lowered not in seen:
            seen.add(lowered)
            deduped.append(item)
    return deduped


def build_prompt(prompt: str, asset_type: str, background: str, negatives: list[str], reference_images: list[Path]) -> str:
    suffix = ASSET_TYPE_SUFFIXES.get(asset_type, "")
    background_clause = "transparent background, clean alpha edges" if background == "transparent" else "opaque background, resolved scene context"
    reference_clause = ""
    if reference_images:
        reference_clause = "Use the provided reference images as guidance for composition, material, palette, or editing intent while keeping the result production-ready."
    negative_clause = "; ".join(negatives)
    parts = [
        prompt.strip(),
        suffix,
        background_clause,
        reference_clause,
        f"Avoid: {negative_clause}.",
    ]
    return ". ".join(part for part in parts if part)


def read_reference_as_data_url(path: Path) -> str:
    mime_type, _ = mimetypes.guess_type(str(path))
    if mime_type not in {"image/png", "image/jpeg", "image/webp", "image/gif"}:
        raise ValidationError(f"Unsupported reference image MIME type for {path}")
    raw = path.read_bytes()
    encoded = base64.b64encode(raw).decode("ascii")
    return f"data:{mime_type};base64,{encoded}"


def sha256_for_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def request_json(url: str, payload: dict[str, Any] | None, headers: dict[str, str], timeout_seconds: int) -> dict[str, Any]:
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    req = request.Request(url, data=data, headers=headers, method="GET" if payload is None else "POST")
    try:
        with request.urlopen(req, timeout=timeout_seconds) as response:
            body = response.read().decode("utf-8")
            return json.loads(body)
    except error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code} from OpenRouter: {body}") from exc
    except error.URLError as exc:
        raise RuntimeError(f"OpenRouter request failed: {exc}") from exc


def build_payload(plan: PlannedRequest) -> dict[str, Any]:
    content: list[dict[str, Any]] = [{"type": "text", "text": plan.compiled_prompt}]
    for image_path in plan.reference_images:
        content.append({"type": "image_url", "image_url": {"url": read_reference_as_data_url(image_path)}})

    payload: dict[str, Any] = {
        "model": plan.model,
        "messages": [{"role": "user", "content": content}],
        "modalities": ["image", "text"],
        "stream": False,
        "provider": plan.provider_object,
    }

    if plan.seed is not None:
        payload["seed"] = plan.seed

    if plan.model.startswith("google/"):
        payload["image_config"] = {
            "aspect_ratio": plan.aspect_ratio,
            "image_size": plan.image_size,
        }
    else:
        payload["background"] = plan.background
        payload["size"] = plan.resolution
        payload["quality"] = plan.quality
        payload["output_format"] = plan.output_format
        if plan.output_compression is not None:
            payload["output_compression"] = plan.output_compression
    return payload


def parse_image_url_entry(entry: dict[str, Any]) -> tuple[str, bytes]:
    image_url = entry.get("image_url") or entry.get("imageUrl") or {}
    data_url = image_url.get("url")
    if not isinstance(data_url, str) or not data_url.startswith("data:"):
        raise RuntimeError("Expected a base64 data URL in response image payload.")
    match = re.match(r"data:(image/[a-zA-Z0-9.+-]+);base64,(.+)", data_url, re.DOTALL)
    if not match:
        raise RuntimeError("Unable to parse returned image data URL.")
    mime_type = match.group(1).lower()
    raw = base64.b64decode(match.group(2))
    return mime_type, raw


def extension_for_mime(mime_type: str) -> str:
    return {
        "image/png": ".png",
        "image/jpeg": ".jpg",
        "image/webp": ".webp",
        "image/gif": ".gif",
    }.get(mime_type, ".bin")


def plan_request(args: argparse.Namespace) -> PlannedRequest:
    validate_count(args.count)
    reference_images = [Path(value).resolve() for value in args.reference_image]
    validate_references(reference_images)

    asset_type = args.asset_type
    inference_notes: list[str] = []
    background = infer_background(args.background, asset_type, inference_notes)

    resolution = normalize_resolution(args.resolution)
    aspect_ratio = args.aspect_ratio
    image_size = args.image_size

    model, model_reason = choose_model(
        asset_type=asset_type,
        background=background,
        requested_model=args.model,
        references=reference_images,
        prompt=args.prompt,
        aspect_ratio=aspect_ratio,
        image_size=image_size,
        notes=inference_notes,
    )

    if model == "openai/gpt-5-image":
        if args.image_size is not None:
            raise ValidationError("GPT-5 Image requests in this skill do not support --image-size. Use --resolution instead.")
        resolution, output_format = validate_transparent_request(
            resolution=resolution or map_gpt_image_resolution(asset_type, aspect_ratio),
            aspect_ratio=aspect_ratio,
            background=background,
            output_format=args.output_format,
            quality="medium" if args.quality == "auto" else args.quality,
        )
        aspect_ratio = None
        image_size = None
        output_compression = args.output_compression
        quality = "medium" if args.quality == "auto" else args.quality
        if output_format == "png":
            output_compression = None
    else:
        if args.output_format not in {"auto", "png"}:
            raise ValidationError("Opaque Nano Banana workflows in this skill only save PNG outputs.")
        if not aspect_ratio and not resolution:
            aspect_ratio = default_gemini_aspect_ratio(asset_type)
        if not image_size:
            image_size = default_gemini_image_size(asset_type, model)
        aspect_ratio, image_size = validate_gemini_request(
            model=model,
            resolution=resolution,
            aspect_ratio=aspect_ratio,
            image_size=image_size,
        )
        resolution = None
        output_format = "png"
        output_compression = None
        quality = args.quality

    negatives = build_negative_constraints(asset_type, background, args.negative)
    compiled_prompt = build_prompt(
        prompt=args.prompt,
        asset_type=asset_type,
        background=background,
        negatives=negatives,
        reference_images=reference_images,
    )

    provider_object: dict[str, Any] = {"require_parameters": True, "allow_fallbacks": True}

    return PlannedRequest(
        original_prompt=args.prompt,
        compiled_prompt=compiled_prompt,
        asset_type=asset_type,
        background=background,
        model=model,
        model_reason=model_reason,
        count=args.count,
        slug=slugify(args.slug or f"{asset_type}-{args.prompt[:48]}"),
        resolution=resolution,
        aspect_ratio=aspect_ratio,
        image_size=image_size,
        quality=quality,
        output_format=output_format,
        output_compression=output_compression,
        seed=args.seed,
        reference_images=reference_images,
        negative_constraints=negatives,
        inference_notes=inference_notes,
        provider_object=provider_object,
    )


def save_outputs(plan: PlannedRequest, response_json: dict[str, Any], timestamp_prefix: str, image_index_start: int, user_request: str | None) -> list[dict[str, Any]]:
    date_dir = OUTPUT_ROOT / datetime.now().strftime("%Y-%m-%d")
    date_dir.mkdir(parents=True, exist_ok=True)

    choices = response_json.get("choices") or []
    if not choices:
        raise RuntimeError("OpenRouter response did not contain any choices.")
    message = choices[0].get("message") or {}
    images = message.get("images") or []
    if not images:
        raise RuntimeError("OpenRouter response did not include any images.")

    saved: list[dict[str, Any]] = []
    for offset, entry in enumerate(images, start=image_index_start):
        mime_type, raw_bytes = parse_image_url_entry(entry)
        extension = extension_for_mime(mime_type)
        stem = f"{timestamp_prefix}_{plan.slug}_{offset:02d}"
        image_path = date_dir / f"{stem}{extension}"
        metadata_path = date_dir / f"{stem}.json"
        image_path.write_bytes(raw_bytes)

        metadata = {
            "timestamp": timestamp_prefix,
            "user_request": user_request,
            "original_prompt": plan.original_prompt,
            "compiled_prompt": plan.compiled_prompt,
            "asset_type": plan.asset_type,
            "background": plan.background,
            "model": plan.model,
            "model_reason": plan.model_reason,
            "resolution": plan.resolution,
            "aspect_ratio": plan.aspect_ratio,
            "image_size": plan.image_size,
            "count_requested": plan.count,
            "image_index": offset,
            "quality": plan.quality,
            "output_format": plan.output_format,
            "output_compression": plan.output_compression,
            "negative_constraints": plan.negative_constraints,
            "reference_images": [str(path) for path in plan.reference_images],
            "inference_notes": plan.inference_notes,
            "provider_object": plan.provider_object,
            "openrouter": {
                "id": response_json.get("id"),
                "model": response_json.get("model"),
                "created": response_json.get("created"),
                "usage": response_json.get("usage"),
                "assistant_text": message.get("content"),
            },
            "files": {
                "image": str(image_path),
                "metadata": str(metadata_path),
                "mime_type": mime_type,
                "bytes": len(raw_bytes),
                "sha256": sha256_for_file(image_path),
            },
        }
        metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
        saved.append({"image": str(image_path), "metadata": str(metadata_path)})
    return saved


def run_generate(args: argparse.Namespace) -> int:
    config = load_config()
    api_key = require_api_key(config)
    plan = plan_request(args)

    timeout_seconds = int(config.get("OPENROUTER_TIMEOUT_SECONDS", "180"))
    base_url = config.get("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1").rstrip("/")
    if allowed := config.get("OPENROUTER_ALLOWED_PROVIDERS", "").strip():
        provider_list = [item.strip() for item in allowed.split(",") if item.strip()]
        if provider_list:
            plan.provider_object["only"] = provider_list

    payload = build_payload(plan)
    request_headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    if referer := config.get("OPENROUTER_HTTP_REFERER", "").strip():
        request_headers["HTTP-Referer"] = referer
    if app_name := config.get("OPENROUTER_APP_NAME", "").strip():
        request_headers["X-Title"] = app_name

    preview = {
        "plan": {
            "asset_type": plan.asset_type,
            "background": plan.background,
            "model": plan.model,
            "model_reason": plan.model_reason,
            "resolution": plan.resolution,
            "aspect_ratio": plan.aspect_ratio,
            "image_size": plan.image_size,
            "count": plan.count,
            "slug": plan.slug,
            "quality": plan.quality,
            "output_format": plan.output_format,
            "reference_images": [str(path) for path in plan.reference_images],
            "inference_notes": plan.inference_notes,
        },
        "payload": payload,
    }
    if args.dry_run:
        print(json.dumps(preview, ensure_ascii=False, indent=2))
        return 0

    timestamp_prefix = datetime.now().strftime("%Y%m%d-%H%M%S")
    all_saved: list[dict[str, Any]] = []
    for index in range(plan.count):
        if plan.seed is not None:
            payload["seed"] = plan.seed + index
        response_json = request_json(
            url=f"{base_url}/chat/completions",
            payload=payload,
            headers=request_headers,
            timeout_seconds=timeout_seconds,
        )
        saved = save_outputs(
            plan=plan,
            response_json=response_json,
            timestamp_prefix=timestamp_prefix,
            image_index_start=len(all_saved) + 1,
            user_request=args.user_request,
        )
        all_saved.extend(saved)

    result = {
        "saved": all_saved,
        "output_root": str((OUTPUT_ROOT / datetime.now().strftime("%Y-%m-%d")).resolve()),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def run_doctor(_: argparse.Namespace) -> int:
    config = load_config()
    api_key = require_api_key(config)
    timeout_seconds = int(config.get("OPENROUTER_TIMEOUT_SECONDS", "60"))
    base_url = config.get("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1").rstrip("/")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    result = request_json(
        url=f"{base_url}/models?{parse.urlencode({'output_modalities': 'image'})}",
        payload=None,
        headers=headers,
        timeout_seconds=timeout_seconds,
    )
    data = result.get("data") or []
    model_ids = {item.get("id") for item in data if isinstance(item, dict)}
    report = {
        "config_path": str(CONFIG_PATH),
        "api_key_present": True,
        "api_key_masked": f"{api_key[:6]}...{api_key[-4:]}" if len(api_key) >= 10 else "***",
        "base_url": base_url,
        "image_model_count": len(data),
        "required_models_present": {
            "openai/gpt-5-image": "openai/gpt-5-image" in model_ids,
            "google/gemini-2.5-flash-image": "google/gemini-2.5-flash-image" in model_ids,
            "google/gemini-3.1-flash-image-preview": "google/gemini-3.1-flash-image-preview" in model_ids,
        },
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate game-ready images through OpenRouter.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    doctor = subparsers.add_parser("doctor", help="Validate config and query OpenRouter image models.")
    doctor.set_defaults(func=run_doctor)

    generate = subparsers.add_parser("generate", help="Generate one or more images and save them under image_gen/YYYY-MM-DD.")
    generate.add_argument("--prompt", required=True, help="Core generation prompt or edit instruction.")
    generate.add_argument("--user-request", default=None, help="Original user phrasing to record in metadata.")
    generate.add_argument("--asset-type", required=True, choices=sorted(ASSET_TYPE_SUFFIXES), help="Normalized asset category used for prompt defaults and validation.")
    generate.add_argument("--background", default="auto", choices=["auto", "transparent", "opaque"], help="Use transparent only for GPT-5 Image workflows.")
    generate.add_argument("--model", default="auto", choices=sorted(MODEL_ALIASES), help="Model alias. Use auto to let the skill route between GPT-5 Image, Nano Banana, and Nano Banana 2.")
    generate.add_argument("--count", type=int, default=1, help="How many images to generate. Supported range: 1-8.")
    generate.add_argument("--resolution", default=None, help="Literal output resolution, for example 1024x1024.")
    generate.add_argument("--aspect-ratio", default=None, help="Gemini image_config.aspect_ratio, such as 16:9 or 3:4.")
    generate.add_argument("--image-size", default=None, help="Gemini image_config.image_size, such as 1K, 2K, 4K.")
    generate.add_argument("--quality", default="auto", choices=["auto", "low", "medium", "high"], help="Requested quality.")
    generate.add_argument("--output-format", default="auto", choices=["auto", "png", "jpeg", "webp"], help="Output format.")
    generate.add_argument("--output-compression", type=int, default=None, help="JPEG/WebP compression percentage (0-100).")
    generate.add_argument("--seed", type=int, default=None, help="Base seed. If count>1 the script increments per request.")
    generate.add_argument("--slug", default=None, help="Filename slug. If omitted, the script derives one from the prompt.")
    generate.add_argument("--negative", action="append", default=[], help="Additional negative constraint. Repeat as needed.")
    generate.add_argument("--reference-image", action="append", default=[], help="Local reference image path. Repeat up to 4 times.")
    generate.add_argument("--dry-run", action="store_true", help="Plan and validate without calling OpenRouter.")
    generate.set_defaults(func=run_generate)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        output_compression = getattr(args, "output_compression", None)
        if output_compression is not None and not 0 <= output_compression <= 100:
            raise ValidationError("output-compression must be between 0 and 100.")
        return args.func(args)
    except ValidationError as exc:
        print(f"ValidationError: {exc}", file=sys.stderr)
        return 2
    except RuntimeError as exc:
        print(f"RuntimeError: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
