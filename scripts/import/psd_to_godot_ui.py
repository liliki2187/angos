from __future__ import annotations

import argparse
from pathlib import Path

from psd_support import (
    LayerNode,
    PROJECT_ROOT,
    export_composite_png,
    export_layer_tree,
    forward_slash,
    quote_tres_string,
    write_manifest,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Export visible PSD layers to PNG files and generate a Godot UI scene."
    )
    parser.add_argument("input_psd", type=Path)
    parser.add_argument(
        "--output-dir",
        type=Path,
        required=True,
        help="Directory where generated PNG files and the manifest will be written.",
    )
    parser.add_argument(
        "--scene",
        type=Path,
        required=True,
        help="Output .tscn path, relative to the project root or absolute.",
    )
    parser.add_argument(
        "--root-name",
        default="ImportedPsdUi",
        help="Root Control node name for the generated scene.",
    )
    parser.add_argument(
        "--include-hidden",
        action="store_true",
        help="Export hidden layers too.",
    )
    return parser


def to_project_relative(path: Path) -> str:
    resolved = path.resolve()
    try:
        rel_path = resolved.relative_to(PROJECT_ROOT)
    except ValueError as exc:
        raise SystemExit(f"Path must be inside the project: {resolved}") from exc
    return "res://" + forward_slash(rel_path)


def scene_path(parent_path: str, node_name: str) -> str:
    if parent_path == ".":
        return node_name
    return f"{parent_path}/{node_name}"


def iter_leaf_nodes(nodes: list[LayerNode]) -> list[LayerNode]:
    output: list[LayerNode] = []
    for node in nodes:
        if node.is_group:
            output.extend(iter_leaf_nodes(node.children))
        else:
            output.append(node)
    return output


def assign_ext_resource_ids(nodes: list[LayerNode]) -> list[LayerNode]:
    leaves = iter_leaf_nodes(nodes)
    for index, node in enumerate(leaves, start=1):
        node.ext_resource_id = f"{index}_layer"
    return leaves


def build_scene_text(
    *,
    root_name: str,
    psd_size: tuple[int, int],
    nodes: list[LayerNode],
    output_dir: Path,
) -> str:
    leaf_nodes = assign_ext_resource_ids(nodes)
    lines: list[str] = [
        f"[gd_scene load_steps={len(leaf_nodes) + 1} format=3]",
        "",
    ]

    for node in leaf_nodes:
        assert node.image_rel_path is not None
        resource_path = to_project_relative(output_dir / node.image_rel_path)
        lines.append(
            f"[ext_resource type=\"Texture2D\" path={quote_tres_string(resource_path)} id={quote_tres_string(node.ext_resource_id or '')}]"
        )
    if leaf_nodes:
        lines.append("")

    width, height = psd_size
    lines.extend(
        [
            f"[node name={quote_tres_string(root_name)} type=\"Control\"]",
            "layout_mode = 0",
            f"offset_right = {float(width):.1f}",
            f"offset_bottom = {float(height):.1f}",
            "mouse_filter = 2",
            "",
        ]
    )

    def emit_group(node: LayerNode, parent_path: str, parent_left: int, parent_top: int) -> None:
        path = scene_path(parent_path, node.node_name)
        offset_left = float(node.left - parent_left)
        offset_top = float(node.top - parent_top)
        offset_right = float(node.right - parent_left)
        offset_bottom = float(node.bottom - parent_top)

        if node.is_group:
            lines.extend(
                [
                    f"[node name={quote_tres_string(node.node_name)} type=\"Control\" parent={quote_tres_string(parent_path)}]",
                    "layout_mode = 0",
                    f"offset_left = {offset_left:.1f}",
                    f"offset_top = {offset_top:.1f}",
                    f"offset_right = {offset_right:.1f}",
                    f"offset_bottom = {offset_bottom:.1f}",
                    "mouse_filter = 2",
                    "",
                ]
            )
            for child in node.children:
                emit_group(child, path, node.left, node.top)
            return

        lines.extend(
            [
                f"[node name={quote_tres_string(node.node_name)} type=\"TextureRect\" parent={quote_tres_string(parent_path)}]",
                "layout_mode = 0",
                f"offset_left = {offset_left:.1f}",
                f"offset_top = {offset_top:.1f}",
                f"offset_right = {offset_right:.1f}",
                f"offset_bottom = {offset_bottom:.1f}",
                "mouse_filter = 2",
                f"texture = ExtResource({quote_tres_string(node.ext_resource_id or '')})",
                "",
            ]
        )

    for node in nodes:
        emit_group(node, ".", 0, 0)

    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    args = build_parser().parse_args()

    input_psd = args.input_psd.resolve()
    output_dir = args.output_dir.resolve()
    scene_path_abs = args.scene.resolve() if args.scene.is_absolute() else (PROJECT_ROOT / args.scene).resolve()

    psd, nodes = export_layer_tree(
        input_psd,
        output_dir,
        include_hidden=args.include_hidden,
    )
    export_composite_png(input_psd, output_dir / "preview" / f"{input_psd.stem}_flat.png")
    write_manifest(
        psd_path=input_psd,
        psd_size=psd.size,
        nodes=nodes,
        manifest_path=output_dir / "manifest.json",
    )

    scene_text = build_scene_text(
        root_name=args.root_name,
        psd_size=psd.size,
        nodes=nodes,
        output_dir=output_dir,
    )
    scene_path_abs.parent.mkdir(parents=True, exist_ok=True)
    scene_path_abs.write_text(scene_text, encoding="utf-8")

    print(f"Generated scene: {scene_path_abs}")
    print(f"Generated assets: {output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
