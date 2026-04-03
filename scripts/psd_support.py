from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable


PROJECT_ROOT = Path(__file__).resolve().parents[1]
LOCAL_PYTHON_DIR = PROJECT_ROOT / ".local" / "python"
if LOCAL_PYTHON_DIR.exists():
    sys.path.insert(0, str(LOCAL_PYTHON_DIR))

try:
    from psd_tools import PSDImage
except ImportError as exc:  # pragma: no cover - runtime guard
    raise SystemExit(
        "psd-tools is not available. Run `python -m pip install --target .local/python psd-tools==1.14.2`."
    ) from exc


@dataclass
class LayerNode:
    original_name: str
    node_name: str
    bbox: tuple[int, int, int, int]
    is_group: bool
    visible: bool
    children: list["LayerNode"] = field(default_factory=list)
    image_rel_path: str | None = None
    ext_resource_id: str | None = None

    @property
    def left(self) -> int:
        return self.bbox[0]

    @property
    def top(self) -> int:
        return self.bbox[1]

    @property
    def right(self) -> int:
        return self.bbox[2]

    @property
    def bottom(self) -> int:
        return self.bbox[3]

    @property
    def width(self) -> int:
        return max(0, self.right - self.left)

    @property
    def height(self) -> int:
        return max(0, self.bottom - self.top)

    def to_manifest_dict(self) -> dict:
        return {
            "original_name": self.original_name,
            "node_name": self.node_name,
            "bbox": list(self.bbox),
            "is_group": self.is_group,
            "visible": self.visible,
            "image_rel_path": self.image_rel_path,
            "children": [child.to_manifest_dict() for child in self.children],
        }


_NON_ALNUM_RE = re.compile(r"[^0-9A-Za-z]+")


def slugify(value: str, fallback: str) -> str:
    text = _NON_ALNUM_RE.sub("_", value.strip()).strip("_").lower()
    return text or fallback


def forward_slash(path: Path | str) -> str:
    return str(path).replace("\\", "/")


def quote_tres_string(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def ensure_parent_dir(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def load_psd(psd_path: Path) -> PSDImage:
    return PSDImage.open(psd_path)


def export_composite_png(psd_path: Path, output_path: Path) -> None:
    psd = load_psd(psd_path)
    image = psd.composite()
    if image is None:
        raise SystemExit(f"Failed to composite PSD: {psd_path}")
    ensure_parent_dir(output_path)
    image.save(output_path)


def _layer_is_group(layer: object) -> bool:
    checker = getattr(layer, "is_group", None)
    return bool(checker()) if callable(checker) else False


def _valid_bbox(bbox: object) -> bool:
    if not bbox:
        return False
    left, top, right, bottom = bbox
    return right > left and bottom > top


def _build_layer_tree(
    layer: object,
    *,
    include_hidden: bool,
    output_dir: Path,
    sibling_name_counts: dict[str, int],
    path_segments: list[str],
) -> LayerNode | None:
    if not include_hidden and not getattr(layer, "visible", True):
        return None

    bbox = getattr(layer, "bbox", None)
    if not _valid_bbox(bbox):
        return None

    base_name = slugify(getattr(layer, "name", ""), "layer")
    sibling_count = sibling_name_counts.get(base_name, 0) + 1
    sibling_name_counts[base_name] = sibling_count
    unique_name = base_name if sibling_count == 1 else f"{base_name}_{sibling_count}"

    node = LayerNode(
        original_name=getattr(layer, "name", "") or unique_name,
        node_name=unique_name,
        bbox=tuple(int(part) for part in bbox),
        is_group=_layer_is_group(layer),
        visible=bool(getattr(layer, "visible", True)),
    )

    next_path_segments = [*path_segments, unique_name]
    if node.is_group:
        child_name_counts: dict[str, int] = {}
        for child in layer:
            child_node = _build_layer_tree(
                child,
                include_hidden=include_hidden,
                output_dir=output_dir,
                sibling_name_counts=child_name_counts,
                path_segments=next_path_segments,
            )
            if child_node is not None:
                node.children.append(child_node)
        if not node.children:
            return None
        return node

    image = layer.composite()
    if image is None:
        return None

    rel_path = Path("layers").joinpath(*next_path_segments).with_suffix(".png")
    abs_path = output_dir / rel_path
    ensure_parent_dir(abs_path)
    image.save(abs_path)
    node.image_rel_path = forward_slash(rel_path)
    return node


def export_layer_tree(
    psd_path: Path,
    output_dir: Path,
    *,
    include_hidden: bool = False,
) -> tuple[PSDImage, list[LayerNode]]:
    psd = load_psd(psd_path)
    output_dir.mkdir(parents=True, exist_ok=True)

    top_level_nodes: list[LayerNode] = []
    sibling_name_counts: dict[str, int] = {}
    for layer in psd:
        node = _build_layer_tree(
            layer,
            include_hidden=include_hidden,
            output_dir=output_dir,
            sibling_name_counts=sibling_name_counts,
            path_segments=[],
        )
        if node is not None:
            top_level_nodes.append(node)

    return psd, top_level_nodes


def write_manifest(
    *,
    psd_path: Path,
    psd_size: tuple[int, int],
    nodes: Iterable[LayerNode],
    manifest_path: Path,
) -> None:
    payload = {
        "source_psd": forward_slash(psd_path),
        "size": list(psd_size),
        "layers": [node.to_manifest_dict() for node in nodes],
    }
    ensure_parent_dir(manifest_path)
    manifest_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
