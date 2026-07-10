# WMW 左侧地区卡 B2.4 叠层修正评审记录

> 版本：v0.9.10 / B2.4  
> 日期：2026-07-09  
> 结论：三处叠层缺陷已按结构修正，完整纵向切片已重跑通过；当前为“待用户观感裁决”的候选切片，不是冻结生产资源。

## 一、本轮问题

用户复审 B2.3 时指出：466 manifest 写了 300% 目检通过，但 465 QA 板上仍可见缺陷。本轮先修正目检口径，再修素材。

缺陷清单：

- 地球下方叠着旧图层：B2.3 把地球圆盘当保护区不挖，旧照片淡蓝山体跟着保留下来。
- 照片底边旧图残留带：窗口下界实测到 y=184，但旧照片实际延伸到约 y=190。
- badge 图标双环重影：从源帧按槽位矩形贴完整 badge，源帧与母版几何不齐，环形错位。
- 目检口径错误：不得再写整批 pass，必须逐状态、逐检查点记录。

## 二、结构修法

- 地球贴片化：从 available 母版提取暖色奶油线条地球贴片，窗口矩形整块挖穿，不再保留地球保护区。
- z 序更新：矩形照片 -> 镂空壳 -> selected 绿光晕 -> 独立地球贴片 -> 运行时文字。
- 边缘残留扫描：母版窗口从 `[38,56,366,184]` 扩展为 `[37,56,367,192]`，四边旧照片签名最终均为 0。
- badge 字形贴换：保留母版 badge 外八角环；用奶油色连通块区分外环与状态字形，清除母版 available 靶心字形及其 3px 抗锯齿 / 阴影区，再居中贴入 selected / warning / locked 字形。
- 目检口径：475 中每帧四点，地球弧下 / 窗口右缘 / 窗口下缘 / badge 区域，共 16 个独立结论，全部写入 manifest。

## 三、输入与脚本

输入：

- 候选 B 原始 atlas：`gd_project/Assets/ui/angus_packaging/world_map/wmw_v09_left_card_slice/left_region_card_candidate_b_atlas_2x.png`
- B1.3 地区照片 atlas：`docs/screenshots/2026-06-24-world-map-benchmark-landing/428-world-map-wmw-v0-9-5-left-card-candidate-b1-3-atlas-2x.png`

脚本：

- `scripts/ui-contracts/wmw/wmw_v0910_left_card_b24_layer_fix_pipeline.py`
- `gd_project/tests/capture_world_map_wmw_left_card_runtime_v09.gd`
- `scripts/run_wmw_godot_capture_v09.ps1`

Godot 截图跑法：

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run_wmw_godot_capture_v09.ps1 -SkipRepro
```

## 四、产物

| 编号 | 文件 | 说明 |
| --- | --- | --- |
| 469 | `docs/screenshots/2026-06-24-world-map-benchmark-landing/469-world-map-wmw-v0-9-10-left-card-b2-4-layer-fix-compare.png` | 原 B vs B2.4 派生对比板 |
| 470 | `docs/screenshots/2026-06-24-world-map-benchmark-landing/470-world-map-wmw-v0-9-10-left-card-b2-4-ingredients.png` | 镂空壳 / 地球贴片 / 清理 mask 配料板 |
| 471 | `docs/screenshots/2026-06-24-world-map-benchmark-landing/471-world-map-wmw-v0-9-10-left-card-b2-4-atlas-2x.png` | 2x atlas |
| 472 | `docs/screenshots/2026-06-24-world-map-benchmark-landing/472-world-map-wmw-v0-9-10-left-card-b2-4-geometry-qa.png` | 几何 QA |
| 473 | `docs/screenshots/2026-06-24-world-map-benchmark-landing/473-world-map-wmw-v0-9-10-left-card-b2-4-runtime-fill.png` | Python 回填 |
| 474 | `docs/screenshots/2026-06-24-world-map-benchmark-landing/474-world-map-wmw-v0-9-10-left-card-b2-4-runtime-fill-qa.png` | Python 回填 QA |
| 475 | `docs/screenshots/2026-06-24-world-map-benchmark-landing/475-world-map-wmw-v0-9-10-left-card-b2-4-16point-visual-qa.png` | 16 点 200% 目检板 |
| 476 | `docs/screenshots/2026-06-24-world-map-benchmark-landing/476-world-map-wmw-v0-9-10-left-card-b2-4-manifest.json` | manifest |
| 477 | `docs/screenshots/2026-06-24-world-map-benchmark-landing/477-world-map-wmw-v0-9-10-left-card-b2-4-godot-single-component.png` | Godot windowed 单组件截图 |
| 478 | `docs/screenshots/2026-06-24-world-map-benchmark-landing/478-world-map-wmw-v0-9-10-left-card-b2-4-godot-single-component-qa.png` | Godot windowed QA 截图 |

Godot 资产副本：

- `gd_project/Assets/ui/angus_packaging/world_map/wmw_v09_left_card_slice/left_region_card_b24_overlay_fix_atlas_2x.png`
- `gd_project/Assets/ui/angus_packaging/world_map/wmw_v09_left_card_slice/left_region_card_b24_overlay_fix_manifest.json`
- `gd_project/Assets/ui/angus_packaging/world_map/wmw_v09_left_card_slice/ingredients/`

## 五、Gate 结果

manifest 状态：

```text
b2_4_overlay_fix_pass_pending_user_review
```

| Gate | 结果 | 证据 |
| --- | --- | --- |
| GateA 旧图残留核心区 | pass | 四状态 `opaque_pixels_in_cutout_core = 0` |
| old_content_leftover_scan | pass | 壳层 + 地球贴片全窗口旧照片签名 = 0 |
| window_edge_residue_scan | pass | 扩展后 top / right / bottom / left 旧照片签名均 = 0 |
| GateB 边框完整环带 | pass | 四状态 `broken_opaque_pixels = 0` |
| GateC 窗口 alpha | pass | 四状态 `transparent_or_nonopaque_pixels_in_window = 0` |
| GateD 非 selected 绿残留 | pass | available / warning / locked 全帧绿签名 = 0；selected 语义免检 |
| GateE 同状态窗口 | pass | 母版派生 diff = 0 |
| GateF 几何比例 | pass | 四帧 408x320，比例 1.275 |
| 16 点目检 | pass | 475，四状态 × 四检查点均独立记录 pass |
| Godot windowed 截图 | pass | 477/478，非黑、颜色多样性正常 |

JSON 校验：

- `python -m json.tool docs/screenshots/2026-06-24-world-map-benchmark-landing/476-world-map-wmw-v0-9-10-left-card-b2-4-manifest.json` 通过
- `python -m json.tool gd_project/Assets/ui/angus_packaging/world_map/wmw_v09_left_card_slice/left_region_card_b24_overlay_fix_manifest.json` 通过

## 六、目检备注

- 地球弧下：四状态地球徽章改为独立顶层贴片，未再保留旧照片淡蓝山体。
- 窗口右缘：照片由母版框体遮挡，无旧图带、透明洞或状态色色带。
- 窗口下缘：窗口向下扩展到 y=192，底边旧图残留带清零。
- badge 区域：外八角环保留，状态字形用连通块方式贴换；selected / warning / locked 未再出现 available 靶心虚线或双环重影。
- 运行时文字：Python 与 Godot 均使用 `label_title / meta_status` token；未烘进素材。

## 七、禁止与状态

已遵守：

- 未调用 imagegen。
- 未改 `design/ui-contracts/world-map/` frozen 字段。
- 未批量生产其它 class。
- 未对照片做形状 / 圆弧 / mask 裁切。
- 未使用 headless 跑 UI 截图。
- 未修改 gate 判据来迁就缺陷。

当前状态：

```text
B2.4 是完整纵向切片通过的候选，等待用户对观感与 B2.4 修正路线裁决。
```
