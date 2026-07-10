# WMW left_region_card B2 配料化拼装试点评审（v0.9.6）

> 日期：2026-07-08  
> 产物范围：仅 `left_region_card`，不扩展其它 class。  
> 结论：B2 纵向切片已跑通，机器 gate 与 Godot windowed 截图通过；但 2026-07-09 用户基于 445 复审后视觉拒收。B2 不是生产资源，失败原因升级为缺少真实照片窗口形状 mask 与独立 frame overlay。

## 1. 试点目标

B1.1 / B1.2 / B1.3 的共同问题不是照片内容，而是把压平成品当源图切补后，右缘 18px 冲突反复变成残带、透明洞、程序色带。B2 改为配料化拼装：

- B 壳提供 frame / plate / globe / state badge 材料；
- B1 提供四张地区照片内容；
- Python 按 `left_region_card.json` v0.8.2 构造 2x atlas；
- title / meta 继续由 Python/Godot 运行时回填；
- 不修改 `design/ui-contracts/world-map/` frozen 字段。

## 2. 本轮产物

| 编号 | 文件 | 说明 |
| --- | --- | --- |
| 436 | `docs/screenshots/2026-06-24-world-map-benchmark-landing/436-world-map-wmw-v0-9-6-left-card-b2-constructed-ingredients.png` | 配料拆解板 |
| 437 | `docs/screenshots/2026-06-24-world-map-benchmark-landing/437-world-map-wmw-v0-9-6-left-card-b2-constructed-composite.png` | B2 四状态拼装源 |
| 438 | `docs/screenshots/2026-06-24-world-map-benchmark-landing/438-world-map-wmw-v0-9-6-left-card-b2-geometry-qa.png` | 几何 QA |
| 439 | `docs/screenshots/2026-06-24-world-map-benchmark-landing/439-world-map-wmw-v0-9-6-left-card-b2-atlas-2x.png` | 2x atlas |
| 440 / 441 | `docs/screenshots/2026-06-24-world-map-benchmark-landing/440-world-map-wmw-v0-9-6-left-card-b2-runtime-fill.png` / `441-world-map-wmw-v0-9-6-left-card-b2-runtime-fill-qa.png` | Python runtime fill |
| 442 | `docs/screenshots/2026-06-24-world-map-benchmark-landing/442-world-map-wmw-v0-9-6-left-card-b2-manifest.json` | B2 manifest |
| 443 | `docs/screenshots/2026-06-24-world-map-benchmark-landing/443-world-map-wmw-v0-9-6-left-card-b2-edge-and-texture-qa.png` | 右缘近景 QA |
| 444 | `docs/screenshots/2026-06-24-world-map-benchmark-landing/444-world-map-wmw-v0-9-6-left-card-b1-3-vs-b2-constructed-board.png` | B1.3 vs B2 对比板 |
| 445 / 446 | `docs/screenshots/2026-06-24-world-map-benchmark-landing/445-world-map-wmw-v0-9-6-left-card-b2-godot-single-component.png` / `446-world-map-wmw-v0-9-6-left-card-b2-godot-single-component-qa.png` | Godot windowed 真实截图 |

Godot asset copy：

- `gd_project/Assets/ui/angus_packaging/world_map/wmw_v09_left_card_slice/left_region_card_b2_constructed_atlas_2x.png`
- `gd_project/Assets/ui/angus_packaging/world_map/wmw_v09_left_card_slice/left_region_card_b2_constructed_manifest.json`

## 3. Gate 结果

| gate | 状态 | 证据 |
| --- | --- | --- |
| 合同校验 | pass | `validate_class_contract.py left_region_card.json` 通过 |
| frozen 字段 | pass | `design/ui-contracts/world-map/` 无 diff |
| geometry_ratio_1_275 | pass | 438 / 442 |
| photo_layer_contract_slot_mask | pass | 照片层只贴入合同 `photo_slot` `[42,48,390,176]` |
| card_body_opacity_probe | pass | x390..408 / y40..300 透明洞为 0 |
| chroma_residue_full_frame_all_states | pass | 四状态全帧色键绿残留为 0 |
| right_band_texture_variation | pass | x390..408 为 B 壳 bitmap 右唇材料，不是纯色程序带 |
| Godot windowed capture | pass | 445 / 446，非黑与颜色多样性写入 442 |

## 4. 视觉结论

B2 修掉了 B1.1 到 B1.3 的三类硬缺陷：旧照片残带、透明洞、纯状态色填充带。当前右侧不再是照片层外溢，也不是直接透明或程序纯色，而是用 B 壳 bitmap 材料镜像重建的右框唇。

但用户复审指出，以第二张“欧洲灰域”为例：

- 照片左上没有贴合地球徽章下方的圆弧 cutout；
- 照片下方露出底板 / 另一层图片，说明下缘遮挡关系错误；
- 右侧仍有不自然遮挡 / 接缝。

这证明 B2 失败不只是右侧 18px，而是 photo 层缺少真实窗口形状 mask，frame / globe / bottom lip / right lip 没有作为 overlay 明确压在 photo 之上。机器 gate 只能证明没有透明洞、色键残留和纯色带，不能证明形状和遮挡贴合。

B2 视觉结论：fail，状态记为 `visual_fail_shape_mask_and_frame_overlay_missing`。

## 5. 中途否决记录

- 严格 `photo_slot` 初稿：机器过，但右侧 18px 仍像轨道，原因是右唇覆盖不完整。
- x408 照片窗口变体：照片会压住右框并在 Godot 中显得探出卡体，否决。
- x400 照片窗口变体：照片外探缓解但仍压框，否决。
- 最终 B2：照片回到合同槽，x390..408 作为完整右框唇重建，保留为当前可审版本。

## 6. 后续建议

不要再修单点坐标。下一轮若继续左卡，必须先做独立 frame overlay 配料与 shaped photo mask：

- `body / plate`；
- `photo clipped by shaped mask`；
- `frame overlay / globe / badge`；
- `runtime text`。

没有 shaped mask 与 frame overlay 前，不得继续试 x390 / x400 / x408 坐标，也不得把机器 gate 通过写成视觉通过。
