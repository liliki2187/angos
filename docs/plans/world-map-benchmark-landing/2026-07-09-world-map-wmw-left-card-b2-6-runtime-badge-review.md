# WMW 左卡 B2.6 运行时 badge 图标层复审记录

> 轮次：B2.6 / v0.9.12  
> 日期：2026-07-09  
> 状态：用户复核后降级为视觉失败；程序 gate 只能作为局部证据，不能代表 badge clean base 通过。  
> 禁止宣称：本轮不是冻结生产资源，不得批量生产其它 class。

## 零、复核降级

用户复核 497 Godot 截图后指出 selected 右下 badge 明显存在不同层的叠加错乱。拆层探针确认：

- runtime selected icon PNG 自身只有奶油色勾，透明背景；
- atlas 的“干净 badge 底盘”并不干净，仍保留旧 available 靶心的暗色圆弧 / 阴影 / 内芯残影；
- 勾图标叠上去后形成旧靶心残影 + 新勾的多层混杂。

因此 B2.6 当前结论改为 `visual_fail_badge_clean_base_semantic_residue`。下文程序 gate 保留为“当时机器证据”，但不再支持视觉通过判断。

## 一、任务范围

本轮执行 A172 裁决：badge 状态字形不再烘焙进 atlas，也不再从源帧贴换到壳层。

- 壳侧：母版 badge 底盘清空靶心字形及其抗锯齿 / 阴影影响区，得到干净底盘；底盘内芯继续参与状态换色。
- 图标侧：勾 / 靶心 / 警示三角 / 锁提取为独立透明 PNG 配料，逐个过 `ingredient_purity`。
- 运行时侧：Python 回填与 Godot capture 在 `action_badge` 槽绘制对应图标，和中文 Label 同属运行时层。
- 地球贴片：保持独立覆盖配料，并补 `ingredient_purity` 与 400% 证据。
- 本轮零 imagegen，不改合同 frozen 字段，不批量生产其它 class。

## 二、产物

| 编号 | 产物 | 路径 |
| --- | --- | --- |
| 489 | B2.6 派生对比板 | `docs/screenshots/2026-06-24-world-map-benchmark-landing/489-world-map-wmw-v0-9-12-left-card-b2-6-runtime-badge-compare.png` |
| 490 | 配料纯度 + 400% 证据板 | `docs/screenshots/2026-06-24-world-map-benchmark-landing/490-world-map-wmw-v0-9-12-left-card-b2-6-ingredients-purity-qa.png` |
| 491 | B2.6 atlas 2x | `docs/screenshots/2026-06-24-world-map-benchmark-landing/491-world-map-wmw-v0-9-12-left-card-b2-6-atlas-2x.png` |
| 493 | Python 运行时回填预览 | `docs/screenshots/2026-06-24-world-map-benchmark-landing/493-world-map-wmw-v0-9-12-left-card-b2-6-runtime-fill.png` |
| 495 | 四状态 × 四检查点 16 点证据板 | `docs/screenshots/2026-06-24-world-map-benchmark-landing/495-world-map-wmw-v0-9-12-left-card-b2-6-16point-visual-qa.png` |
| 496 | manifest | `docs/screenshots/2026-06-24-world-map-benchmark-landing/496-world-map-wmw-v0-9-12-left-card-b2-6-manifest.json` |
| 497 | Godot 单组件截图 | `docs/screenshots/2026-06-24-world-map-benchmark-landing/497-world-map-wmw-v0-9-12-left-card-b2-6-godot-single-component.png` |
| 498 | Godot QA 截图 | `docs/screenshots/2026-06-24-world-map-benchmark-landing/498-world-map-wmw-v0-9-12-left-card-b2-6-godot-single-component-qa.png` |

Godot 资产副本：

- `gd_project/Assets/ui/angus_packaging/world_map/wmw_v09_left_card_slice/left_region_card_b26_runtime_badge_atlas_2x.png`
- `gd_project/Assets/ui/angus_packaging/world_map/wmw_v09_left_card_slice/left_region_card_b26_runtime_badge_manifest.json`
- `gd_project/Assets/ui/angus_packaging/world_map/wmw_v09_left_card_slice/ingredients/left_region_card_b26_runtime_icon_selected.png`
- `gd_project/Assets/ui/angus_packaging/world_map/wmw_v09_left_card_slice/ingredients/left_region_card_b26_runtime_icon_available.png`
- `gd_project/Assets/ui/angus_packaging/world_map/wmw_v09_left_card_slice/ingredients/left_region_card_b26_runtime_icon_warning.png`
- `gd_project/Assets/ui/angus_packaging/world_map/wmw_v09_left_card_slice/ingredients/left_region_card_b26_runtime_icon_locked.png`
- `gd_project/Assets/ui/angus_packaging/world_map/wmw_v09_left_card_slice/ingredients/left_region_card_b26_independent_globe_patch.png`

## 三、配料纯度证据

`ingredient_purity` 的容差为 0：非目标色族像素必须为 0。400% 证据见 490。

| 配料 | opaque | non-target | 结果 |
| --- | ---: | ---: | --- |
| runtime icon selected | 642 | 0 | pass |
| runtime icon available | 1059 | 0 | pass |
| runtime icon warning | 637 | 0 | pass |
| runtime icon locked | 1336 | 0 | pass |
| independent globe patch | 1017 | 0 | pass |

图标提取口径：只保留奶油色字形像素，透明背景；矩形裁片与背景像素均未进入配料。

## 四、badge 底盘与运行时图标

`badge_state_color_consistency` 采用多像素采样，不使用单点取色。atlas 内状态字形残留像素均为 0，状态语义只由 Python / Godot 运行时图标绘制。

| 状态 | 模式 | 框色 hue | badge 内芯 hue | delta | atlas 烘焙字形像素 |
| --- | --- | ---: | ---: | ---: | ---: |
| selected | hue_compare | 69.5° | 69.1° | 0.0013 | 0 |
| available | hue_compare | 182.1° | 182.1° | 0.0000 | 0 |
| warning | hue_compare | 38.9° | 38.8° | 0.0003 | 0 |
| locked | low_saturation_lightness_compare | 64.6° | 65.0° | 0.0009 | 0 |

## 五、程序 gate 汇总（降级解读）

| gate | 结果 | 依据 |
| --- | --- | --- |
| GateA 旧图残留核心区 | pass | 挖窗核心区不透明像素 0 |
| old_content_leftover_scan | pass | 壳层 + 地球贴片完整窗口旧图签名 0；扫描发生在状态换色前 |
| window_edge_residue_scan | pass | top / right / bottom / left 最终旧图签名 0 |
| GateB 边框完整 | pass | 窗口外 3px 环带破损像素 0 |
| GateC 窗口 alpha | pass | 合成后窗口内 alpha 非 255 像素 0 |
| GateD 非 selected 绿残留 | pass | selected 语义豁免；其余状态全帧绿签名 0 |
| badge_state_color_consistency | 局部 pass | badge 内芯随状态框色家族换色，atlas 烘焙浅色字形像素 0；但未覆盖暗色语义残影，已被用户复核判漏检 |
| ingredient_purity | pass | 四个 runtime icon + 地球贴片 non-target 均为 0 |
| GateE 同类窗口 | pass | 四状态同一母版窗口，diff=0 |
| GateF 几何比例 | pass | 四帧 408x320，比例 1.275 |
| Godot windowed capture | pass | 497/498 由 windowed opengl3 runner 生成 |

## 六、目检口径

495 已生成四状态 × 四检查点证据板：地球弧下、窗口右缘、窗口下缘、badge 区域。按照 `ui-geometry-and-text-safety-gates.md` §5.2，本轮执行自检只写 `evidence_ready`；用户已基于 497 裁决 badge 区域失败。

新增缺失检查点：`badge_clean_base_no_semantic_residue`。该项要求在未叠 runtime icon 的 atlas / shell 中，badge 内芯不得出现任何可被识别为旧状态符号的暗色圆弧、靶心、三角、锁、勾影子；`atlas_baked_state_glyph_pixels = 0` 不能替代本项。

## 七、验证命令

```powershell
& "C:\Users\gzfangyue\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" scripts/ui-contracts/wmw/wmw_v0912_left_card_b26_runtime_badge_pipeline.py
powershell -ExecutionPolicy Bypass -File scripts/run_wmw_godot_capture_v09.ps1 -SkipRepro
& "C:\Users\gzfangyue\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -m json.tool docs/screenshots/2026-06-24-world-map-benchmark-landing/496-world-map-wmw-v0-9-12-left-card-b2-6-manifest.json
```

Godot 截图继续禁止 headless；本轮实际使用 `tools/godot/4.6.2-stable/Godot_v4.6.2-stable_win64_console.exe`、windowed、opengl3，并保留 `RenderingServer.frame_post_draw` 与全黑帧拒绝。
