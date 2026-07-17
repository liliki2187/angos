from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
INVENTORY = ROOT / "design/ui-contracts/region-task-board/component_cutout_inventory_v1.json"
MANIFEST = ROOT / "gd_project/Assets/ui/angus_packaging/region_task/region_task_asset_manifest_v2.json"


def no_duplicate_keys(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"重复 JSON key：{key}")
        result[key] = value
    return result


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    data = json.loads(INVENTORY.read_text(encoding="utf-8"), object_pairs_hook=no_duplicate_keys)
    classes = data["component_classes"]
    ids = [item["asset_id"] for item in classes]
    routes = Counter(item["route"] for item in classes)
    expected_routes = {
        "isolated_alpha_master": 10,
        "rectangular_nine_patch": 5,
        "opaque_base_or_tile": 2,
        "program_only": 1,
    }

    require(len(classes) == 18, "正式组件 class 必须正好为 18")
    require(len(ids) == len(set(ids)), "asset_id 必须唯一")
    require(routes == expected_routes, f"生产路线计数不符：{routes}")
    require(
        data["classification_counts"]["direct_crops_from_visual_reference"] == 0,
        "整屏视觉稿直接裁切数必须为 0",
    )

    required_common = {
        "asset_id",
        "role",
        "route",
        "implementation",
        "master_count",
        "geometry_status",
        "needs_new_generation",
        "requires_manual_cutout",
        "crop_difficulty",
    }
    for item in classes:
        missing = required_common - item.keys()
        require(not missing, f"{item.get('asset_id', '<unknown>')} 缺字段：{sorted(missing)}")
        require(item["requires_manual_cutout"] is False, f"{item['asset_id']} 不得把复杂手抠当正常流程")
        require(
            "runtime_size" in item
            or "runtime_sizes" in item
            or "runtime_rect" in item
            or "runtime_frame_size" in item
            or "runtime_visual_size" in item,
            f"{item['asset_id']} 缺运行尺寸",
        )
        if item["route"] == "isolated_alpha_master":
            require(item.get("export_scale") in (2, 3), f"{item['asset_id']} 缺 2x / 3x 导出倍率")
            require(item.get("allowed_baked_content"), f"{item['asset_id']} 缺允许烘焙清单")
            require(item.get("forbidden_baked_content"), f"{item['asset_id']} 缺禁止烘焙清单")
        if item["route"] == "program_only":
            require(item["master_count"] == 0, f"{item['asset_id']} 程序组件不得声明位图母版")

    slice_ids = data["first_vertical_slice"]["asset_ids"]
    require(all(asset_id in ids for asset_id in slice_ids), "纵向切片必须引用已登记 asset_id")
    require(slice_ids == ["rt_task_pin_shell_mother", "rt_task_pin_label_mother"], "首条切片必须是 pin + 短签")

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"), object_pairs_hook=no_duplicate_keys)
    require([1366, 768] in manifest["runtime_resolutions"], "manifest 必须登记 1366×768 回归")
    contract_paths = [manifest["page_contract"], *manifest["component_contracts"].values()]
    for relative_path in contract_paths:
        require((ROOT / relative_path).is_file(), f"manifest 合同不存在：{relative_path}")
    require(
        manifest["component_contracts"].get("component_cutout_inventory")
        == "design/ui-contracts/region-task-board/component_cutout_inventory_v1.json",
        "manifest 必须引用裁切 inventory",
    )

    print("OK component_cutout_inventory_v1")
    print(f"classes={len(classes)} routes={dict(routes)} direct_crops=0 manifest_paths={len(contract_paths)}")


if __name__ == "__main__":
    main()
