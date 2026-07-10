#!/usr/bin/env python3
"""资产化 UI 组件类合同校验器。

校验 design/ui-contracts/<页面>/ 下的 class 合同 JSON：

1. 必填字段：reference_resolution / runtime_resolution / export_scale /
   frozen.export_size / frozen.positions / frozen.hit_rect。
2. 倍率声明：参考分辨率与运行分辨率非整数倍时，export_scale 必须 >= 2。
3. 槽位包含：frozen.slots 与 frozen.no_text_rects 中的矩形必须完整落在
   export_size 内；hit_rect 不得超出 export_size。
4. 整屏回填边界：所有实例位置放置后必须落在 reference_resolution 内。
5. 页面级重叠：不同实例的矩形两两不得相交；声明了 parent_class 的组件
   与其父组件的重叠豁免（父子关系，例如 CTA 条在 dossier 内）。
6. 状态几何一致：若合同提供 per_state_overrides，则各状态的 export_size
   与槽位必须与 frozen 逐项一致（component_class_uniformity_gate）。

用法：
    python scripts/ui-contracts/validate_class_contract.py design/ui-contracts/world-map
    python scripts/ui-contracts/validate_class_contract.py design/ui-contracts/world-map/left_region_card.json

退出码：0 全部通过；1 存在失败项。
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

Rect = tuple[float, float, float, float]  # x, y, w, h


def rect_inside(inner: Rect, outer_w: float, outer_h: float) -> bool:
    x, y, w, h = inner
    return x >= 0 and y >= 0 and x + w <= outer_w and y + h <= outer_h


def rects_intersect(a: Rect, b: Rect) -> bool:
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    return ax < bx + bw and bx < ax + aw and ay < by + bh and by < ay + ah


def as_rect(value) -> Rect | None:
    if isinstance(value, (list, tuple)) and len(value) == 4:
        try:
            return tuple(float(v) for v in value)  # type: ignore[return-value]
        except (TypeError, ValueError):
            return None
    return None


def load_contracts(target: Path) -> list[tuple[Path, dict]]:
    if target.is_file():
        return [(target, json.loads(target.read_text(encoding="utf-8")))]
    contracts = []
    for path in sorted(target.glob("*.json")):
        contracts.append((path, json.loads(path.read_text(encoding="utf-8"))))
    return contracts


def validate_contract(path: Path, data: dict) -> list[str]:
    errors: list[str] = []
    cid = data.get("class_id", path.stem)

    ref = data.get("reference_resolution")
    runtime = data.get("runtime_resolution")
    scale = data.get("export_scale")
    if not (isinstance(ref, list) and len(ref) == 2):
        errors.append(f"[{cid}] 缺少或非法 reference_resolution")
        ref = None
    if not (isinstance(runtime, list) and len(runtime) == 2):
        errors.append(f"[{cid}] 缺少或非法 runtime_resolution")
        runtime = None
    if not isinstance(scale, (int, float)):
        errors.append(f"[{cid}] 缺少或非法 export_scale")
        scale = None

    if ref and runtime and scale is not None:
        ratio_w = runtime[0] / ref[0]
        ratio_h = runtime[1] / ref[1]
        non_integer = abs(ratio_w - round(ratio_w)) > 1e-6 or abs(ratio_h - round(ratio_h)) > 1e-6
        if non_integer and scale < 2:
            errors.append(
                f"[{cid}] 参考分辨率与运行分辨率为非整数倍关系（{ratio_w:.2f}x），export_scale 必须 >= 2，当前为 {scale}"
            )

    frozen = data.get("frozen")
    if not isinstance(frozen, dict):
        errors.append(f"[{cid}] 缺少 frozen 字段块")
        return errors

    export_size = frozen.get("export_size")
    if not (isinstance(export_size, list) and len(export_size) == 2):
        errors.append(f"[{cid}] 缺少或非法 frozen.export_size")
        return errors
    ew, eh = float(export_size[0]), float(export_size[1])

    hit_rect = as_rect(frozen.get("hit_rect"))
    if hit_rect is None:
        errors.append(f"[{cid}] 缺少或非法 frozen.hit_rect")
    elif not rect_inside(hit_rect, ew, eh):
        errors.append(f"[{cid}] hit_rect {hit_rect} 超出 export_size {export_size}")

    for group_name in ("slots", "no_text_rects"):
        group = frozen.get(group_name, {})
        if not isinstance(group, dict):
            errors.append(f"[{cid}] frozen.{group_name} 必须是对象")
            continue
        for slot_name, value in group.items():
            rect = as_rect(value)
            if rect is None:
                errors.append(f"[{cid}] {group_name}.{slot_name} 不是 [x,y,w,h] 矩形")
                continue
            if not rect_inside(rect, ew, eh):
                errors.append(
                    f"[{cid}] {group_name}.{slot_name} {list(rect)} 超出 export_size {export_size}"
                )

    positions = frozen.get("positions")
    if not (isinstance(positions, list) and positions and all(isinstance(p, list) and len(p) == 2 for p in positions)):
        errors.append(f"[{cid}] 缺少或非法 frozen.positions")
    elif ref:
        for pos in positions:
            inst = (float(pos[0]), float(pos[1]), ew, eh)
            if not rect_inside(inst, float(ref[0]), float(ref[1])):
                errors.append(
                    f"[{cid}] 实例 {pos} + export_size {export_size} 超出参考分辨率 {ref}"
                )

    overrides = data.get("per_state_overrides")
    if isinstance(overrides, dict):
        for state, override in overrides.items():
            o_size = override.get("export_size")
            if o_size is not None and o_size != export_size:
                errors.append(
                    f"[{cid}] 状态 {state} 的 export_size {o_size} 与 frozen {export_size} 不一致（类一致 gate 失败）"
                )
            o_slots = override.get("slots")
            if isinstance(o_slots, dict):
                base_slots = frozen.get("slots", {})
                for slot_name, value in o_slots.items():
                    if slot_name in base_slots and value != base_slots[slot_name]:
                        errors.append(
                            f"[{cid}] 状态 {state} 的槽位 {slot_name} {value} 与 frozen {base_slots[slot_name]} 不一致（类一致 gate 失败）"
                        )

    return errors


def validate_page_overlaps(contracts: list[tuple[Path, dict]]) -> list[str]:
    errors: list[str] = []
    instances: list[tuple[str, str | None, Rect]] = []
    for path, data in contracts:
        cid = data.get("class_id", path.stem)
        parent = data.get("parent_class")
        frozen = data.get("frozen", {})
        export_size = frozen.get("export_size")
        positions = frozen.get("positions")
        if not (isinstance(export_size, list) and isinstance(positions, list)):
            continue
        for pos in positions:
            if isinstance(pos, list) and len(pos) == 2:
                instances.append(
                    (cid, parent, (float(pos[0]), float(pos[1]), float(export_size[0]), float(export_size[1])))
                )

    for i in range(len(instances)):
        for j in range(i + 1, len(instances)):
            cid_a, parent_a, rect_a = instances[i]
            cid_b, parent_b, rect_b = instances[j]
            if parent_a == cid_b or parent_b == cid_a:
                continue  # 父子关系豁免
            if rects_intersect(rect_a, rect_b):
                errors.append(
                    f"[页面重叠] {cid_a} {list(rect_a)} 与 {cid_b} {list(rect_b)} 相交，且未声明父子关系"
                )
    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 1
    target = Path(sys.argv[1])
    if not target.exists():
        print(f"路径不存在: {target}")
        return 1

    contracts = load_contracts(target)
    if not contracts:
        print(f"未找到合同 JSON: {target}")
        return 1

    all_errors: list[str] = []
    for path, data in contracts:
        errs = validate_contract(path, data)
        all_errors.extend(errs)
        status = "PASS" if not errs else "FAIL"
        print(f"{status}  {path.name}  (class_id={data.get('class_id', path.stem)}, version={data.get('contract_version', '?')})")

    if target.is_dir():
        overlap_errors = validate_page_overlaps(contracts)
        all_errors.extend(overlap_errors)
        print(f"{'PASS' if not overlap_errors else 'FAIL'}  页面级重叠检查（{len(contracts)} 份合同）")

    if all_errors:
        print("\n失败项：")
        for err in all_errors:
            print(f"  - {err}")
        return 1
    print("\n全部通过。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
