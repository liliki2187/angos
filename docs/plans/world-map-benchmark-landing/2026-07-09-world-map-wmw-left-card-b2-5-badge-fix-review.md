# WMW 左卡 B2.5 badge 修正复审记录

> 轮次：B2.5 / v0.9.11  
> 日期：2026-07-09  
> 状态：程序 gate 全部通过；16 点目检证据就绪，最终视觉 PASS/FAIL 由复核方 / 用户裁决。  
> 禁止宣称：本轮不是冻结生产资源，不得批量生产其它 class。

## 一、任务范围

本轮只重做 badge 层与派生换色：

- badge 底盘内芯纳入框色家族换色。
- 状态字形贴换改为形状 alpha 掩膜，只保留奶油色字形像素，并做 1px 收边。
- 地球贴片、边缘残留扫描、照片层、母版窗口和合同 frozen 字段均不动。
- 本轮零 imagegen。

## 二、产物

| 编号 | 产物 | 路径 |
| --- | --- | --- |
| 479 | B2.5 派生对比板 | `docs/screenshots/2026-06-24-world-map-benchmark-landing/479-world-map-wmw-v0-9-11-left-card-b2-5-badge-fix-compare.png` |
| 481 | B2.5 atlas 2x | `docs/screenshots/2026-06-24-world-map-benchmark-landing/481-world-map-wmw-v0-9-11-left-card-b2-5-atlas-2x.png` |
| 485 | 四状态 × 四检查点 16 点证据板 | `docs/screenshots/2026-06-24-world-map-benchmark-landing/485-world-map-wmw-v0-9-11-left-card-b2-5-16point-visual-qa.png` |
| 486 | manifest | `docs/screenshots/2026-06-24-world-map-benchmark-landing/486-world-map-wmw-v0-9-11-left-card-b2-5-manifest.json` |
| 487 | Godot 单组件截图 | `docs/screenshots/2026-06-24-world-map-benchmark-landing/487-world-map-wmw-v0-9-11-left-card-b2-5-godot-single-component.png` |
| 488 | Godot QA 截图 | `docs/screenshots/2026-06-24-world-map-benchmark-landing/488-world-map-wmw-v0-9-11-left-card-b2-5-godot-single-component-qa.png` |

Godot 资产副本：

- `gd_project/Assets/ui/angus_packaging/world_map/wmw_v09_left_card_slice/left_region_card_b25_badge_fix_atlas_2x.png`
- `gd_project/Assets/ui/angus_packaging/world_map/wmw_v09_left_card_slice/left_region_card_b25_badge_fix_manifest.json`

## 三、新增 badge gate 证据

`badge_state_color_consistency` 采用多像素采样，不使用单点取色：

| 状态 | 模式 | 框色 hue | badge 内芯 hue | delta | 字形依据 |
| --- | --- | ---: | ---: | ---: | --- |
| selected | hue_compare | 69.4° | 68.2° | 0.0033 | alpha 像素 450，矩形贴片 false |
| available | hue_compare | 182.1° | 179.1° | 0.0082 | 母版靶心保留，矩形贴片 false |
| warning | hue_compare | 38.9° | 38.8° | 0.0004 | alpha 像素 242，矩形贴片 false |
| locked | low_saturation_lightness_compare | 64.6° | 65.2° | 0.0018 | alpha 像素 996，矩形贴片 false |

阈值：普通色相比较 `hue_delta <= 0.08`；低饱和状态使用明度比较，`lightness_delta <= 0.18`。

## 四、中途发现并修掉的自检盲区

第一次 B2.5 生成时，badge 中央已经随状态换色，但八角 badge 内部右侧 / 下侧仍残留 available 母版的青色内底。原因是脚本把 `badge_core` 采样区收得太小，只覆盖中间区域，导致边缘内底既没有参与状态换色，也没有进入 `badge_state_color_consistency` gate。

修正方式：`_is_badge_core_pixel` 改为覆盖整个 `ACTION_RECT_2X` 内的非奶油色、非 selected 绿语义像素；同一 predicate 同时用于换色 mask 和 gate 采样。重跑后 479 / 485 中 selected、warning、locked 的 badge 内芯不再残留青色带。

## 五、程序 gate 汇总

| gate | 结果 | 依据 |
| --- | --- | --- |
| GateA 旧图残留核心区 | pass | 挖窗核心区不透明像素 0 |
| old_content_leftover_scan | pass | 壳层 + 地球贴片完整窗口旧图签名 0 |
| window_edge_residue_scan | pass | top / right / bottom / left 最终旧图签名 0 |
| GateB 边框完整 | pass | 窗口外 3px 环带破损像素 0 |
| GateC 窗口 alpha | pass | 合成后窗口内 alpha 非 255 像素 0 |
| GateD 非 selected 绿残留 | pass | selected 语义豁免；其余状态全帧绿签名 0 |
| badge_state_color_consistency | pass | 见上表，多像素色相 / 明度证据 |
| GateE 同类窗口 | pass | 四状态同一母版窗口，diff=0 |
| GateF 几何比例 | pass | 四帧 408x320，比例 1.275 |
| Godot windowed capture | pass | 487/488 由 windowed opengl3 runner 生成 |

## 六、目检口径

485 已生成四状态 × 四检查点证据板：地球弧下、窗口右缘、窗口下缘、badge 区域。按照 `ui-geometry-and-text-safety-gates.md` §5.2，本轮执行自检只写 `evidence_ready`；最终 PASS/FAIL 必须由复核方 / 用户基于 485、487、488 裁决。

## 七、验证命令

```powershell
& "C:\Users\gzfangyue\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" scripts/ui-contracts/wmw/wmw_v0911_left_card_b25_badge_fix_pipeline.py
powershell -ExecutionPolicy Bypass -File scripts/run_wmw_godot_capture_v09.ps1 -SkipRepro
& "C:\Users\gzfangyue\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -m json.tool docs/screenshots/2026-06-24-world-map-benchmark-landing/486-world-map-wmw-v0-9-11-left-card-b2-5-manifest.json
```

Godot 截图继续禁止 headless；本轮实际使用 `tools/godot/4.6.2-stable/Godot_v4.6.2-stable_win64_console.exe`、windowed、opengl3，并保留 `RenderingServer.frame_post_draw` 与全黑帧拒绝。
