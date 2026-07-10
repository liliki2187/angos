# WMW left_region_card 候选 B1 v0.9.2 局部微调复审
> 日期：2026-07-08  
> 状态：B1 完整纵向切片已跑通，等待用户裁决是否进入后续 class 扩展。  
> 约束：未修改 `design/ui-contracts/world-map/` frozen 字段；未批量生产其它 class；未压缩 / 裁切素材凑比例。

## 1. 本轮前置裁决登记

已按用户裁决登记设计采纳：

- 总索引：`docs/设计采纳记录.md` A170（原误编 A164，2026-07-09 改号）。
- 分册：`docs/design-decisions/ui-ux-decisions.md` A170。
- 结论：采纳 `left_region_card` 候选 B 的方向，进入 B1 局部美术微调；不回 brief 重摇，不冻结生产资源。
- cross-read tags：`art, assetized-ui, gate, imagegen, typography, ui, ux, world-map`。

## 2. 产物清单

| 编号 | 文件 | 用途 |
| --- | --- | --- |
| 394 | `docs/screenshots/2026-06-24-world-map-benchmark-landing/394-world-map-wmw-v0-9-2-left-card-imagegen-candidate-b1-r1.png` | 真实 imagegen 尝试 R1，动作章跑位，未采用 |
| 395 | `docs/screenshots/2026-06-24-world-map-benchmark-landing/395-world-map-wmw-v0-9-2-left-card-imagegen-candidate-b1-r2.png` | 真实 imagegen 尝试 R2，整体变宽，未采用 |
| 396 | `docs/screenshots/2026-06-24-world-map-benchmark-landing/396-world-map-wmw-v0-9-2-left-card-imagegen-candidate-b1-r4-wide-failed.png` | 真实 imagegen 尝试 R4，几何变宽；仅作为 photo / warning 局部美术源 |
| 397 | `docs/screenshots/2026-06-24-world-map-benchmark-landing/397-world-map-wmw-v0-9-2-left-card-candidate-b1-composited-polish.png` | B1 几何保真局部合成候选 |
| 398 | `docs/screenshots/2026-06-24-world-map-benchmark-landing/398-world-map-wmw-v0-9-2-left-card-candidate-b1-geometry-qa.png` | B1 几何比例 QA |
| 399 | `docs/screenshots/2026-06-24-world-map-benchmark-landing/399-world-map-wmw-v0-9-2-left-card-candidate-b1-atlas-2x.png` | B1 2x atlas |
| 400 | `docs/screenshots/2026-06-24-world-map-benchmark-landing/400-world-map-wmw-v0-9-2-left-card-candidate-b1-runtime-fill.png` | Python 回填预览 |
| 401 | `docs/screenshots/2026-06-24-world-map-benchmark-landing/401-world-map-wmw-v0-9-2-left-card-candidate-b1-runtime-fill-qa.png` | Python 回填 QA |
| 402 | `docs/screenshots/2026-06-24-world-map-benchmark-landing/402-world-map-wmw-v0-9-2-left-card-candidate-b1-manifest.json` | B1 manifest |
| 403 | `docs/screenshots/2026-06-24-world-map-benchmark-landing/403-world-map-wmw-v0-9-2-left-card-candidate-b1-godot-single-component.png` | Godot 单组件运行截图 |
| 404 | `docs/screenshots/2026-06-24-world-map-benchmark-landing/404-world-map-wmw-v0-9-2-left-card-candidate-b1-godot-single-component-qa.png` | Godot 单组件 QA 截图 |
| 405 | `docs/screenshots/2026-06-24-world-map-benchmark-landing/405-world-map-wmw-v0-9-2-left-card-b-vs-b1-comparison-board.png` | B vs B1 复审对比板 |

生成 / 拼板脚本：

- `scripts/ui-contracts/wmw/wmw_v092_left_card_b1_vertical_slice.py`
- `scripts/ui-contracts/wmw/wmw_v092_left_card_b1_compare.py`

## 3. 生图与合成边界

B1 使用了真实 imagegen 工具，但三次完整卡片编辑都会带来几何漂移：

- R1：地区感和 warning 红色有改善，但 action badge 跑到右上，合同槽失败。
- R2 / R4：photo_slot 地区感较好，但卡体变成宽 banner，比例失败。

因此最终 B1 不是“纯模型一次性输出”。它采用：

- `383` 候选 B 作为几何与合同槽位来源。
- `396` 真实 imagegen R4 作为 photo_slot 地区物件和 warning 红三角的局部美术来源。
- 程序只做局部合成、chroma / 绿边清理、atlas 排版、文字 token 回填和 QA，不冒充生图。

这个路线可以保合同、保尺寸、保同构，但是否允许进入后续 class 扩展，需要用户裁决。

## 4. 四项微调结果

| 微调项 | B1 结果 | 结论 |
| --- | --- | --- |
| 减薄卡片外框 | non-selected 外缘绿色 glow 和暗绿底边已清理，外框观感比 B 更薄；主 bevel 仍保留 B 的卡体语言 | 局部通过，仍需用户按标杆裁决厚度 |
| 清理非 selected 绿色残边 | atlas 统计：32px 外缘 greenish 像素 selected=1324，available=0，warning=0，locked=0 | 通过 |
| photo_slot 地区感 | selected 加金字塔 / 天线；available 加天线阵；warning 加遗迹；locked 加森林人影剪影 | 通过 |
| warning 三角更红 | 保留原槽位，叠入 R4 红三角来源，不整块盖 badge | 通过 |

## 5. 文字 token

素材层不烘文字；回填和 Godot capture 使用运行时 token：

- `label_title`：Python 19px / Godot 25px，墨色 `#121612`。
- `meta_status`：Python 11px / Godot 14px，墨色 `#421c14`。

403 的运行截图里，meta 比 389 更深、更可读；压力长文案仍按上一轮记录为文案 / 字体 token 待办，不改合同槽位。

## 6. QA 记录

- 几何比例 gate：398 通过，四状态均在 1.275 目标比例阈值内。
- no fake text：397 / 399 / 403 目检未发现烘焙文字或可读假字；中文为运行时 Label。
- functional faces orthogonal：photo / label / meta / action 仍与 `left_region_card.json` 槽位正交。
- same state layout：四状态共用同一 204x160 合同卡形与相同槽位。
- Godot capture：使用 `powershell -ExecutionPolicy Bypass -File scripts/run_wmw_godot_capture_v09.ps1 -SkipRepro`，Godot 4.6.2 stable，windowed opengl3。
- 非黑校验：403 为 1920x1080、unique colors 70888、non-black 2073219；404 为 1920x1080、unique colors 66635、non-black 2073600。
- 最小复现记录：headless 分支 signal 11，不用于 UI 截图；windowed opengl3 最小复现 root texture / SubViewport capture 通过。
- JSON 校验：402 与 Godot 资产目录 manifest 均解析通过。

## 7. 待用户裁决

B1 已完成完整切片链，但仍是候选：

1. 是否接受“383 几何 + 真实 imagegen 局部美术源 + 程序合成”的路线作为后续 class 的生产方法。
2. 是否认为 B1 的卡片厚度、label 纸签和图片槽气质已经足够接近标杆。
3. 若不接受，下一轮应继续只微调 `left_region_card`，而不是批量生产其它 class。
