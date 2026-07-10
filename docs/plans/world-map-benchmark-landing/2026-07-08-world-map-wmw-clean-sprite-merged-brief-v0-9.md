# 世界地图 WMW 合并 clean-sprite brief v0.9

> 状态：生产 brief + 左卡纵向切片输入。不是新合同轮。  
> 日期：2026-07-08  
> 参考分辨率：1280x720  
> 运行分辨率：1920x1080  
> 素材倍率：2x  
> 当前路线：四个主 class 已有 locked_candidate 合同；剩余轻合同只做并行捎带，不阻塞左卡纵向切片。

## 1. 本轮目标

本轮只做两件事：

1. 把已锁候选合同合并成一份无字素材生产 brief。
2. 用 `left_region_card` 跑一条纵向切片：生图候选 → 几何 QA → atlas 候选 → 运行时文字回填 → Godot 单组件截图。

本轮明确不做：

- 不再逐个组件开合同评审轮。
- 不批量生产所有素材。
- 不替换世界地图正式界面。
- 不把不服从合同的生图素材硬压缩、裁切或反向改合同。

## 2. 合同真源

所有生产尺寸与槽位以 `design/ui-contracts/world-map/` 为准：

| class_id | 合同版本 | 生产尺寸（参考分辨率） | 2x 生产尺寸 | 用途 |
| --- | --- | --- | --- | --- |
| `left_region_card` | 0.8.2 | 204x160 | 408x320 | 左侧地区摘要卡，四状态纵向切片对象 |
| `right_dossier_page` | 0.8.4 | 320x520 | 640x1040 | 右侧选中地区详情纸 |
| `right_action_lane` | 0.8.4 | 284x50 | 568x100 | 右侧行动条，父级为 dossier |
| `bottom_receipt_card` | 0.8.5 | 246x138 | 492x276 | 底部票据卡 |

统一规则：

- `reference_resolution = 1280x720`。
- `runtime_resolution = 1920x1080`。
- `export_scale = 2`，运行时缩小，禁止 1.5x 位图放大。
- 状态只能换颜色皮肤、图标、低多边形块面，不得改外框、槽位、热区。
- 最终字体确定后，所有贴上限的文字槽必须重跑压力测试。

## 3. 生图 / 美术生产要求

对所有主 class：

- 输出无字 clean sprite，不能烘焙真实中文、英文、数字、假标签、假条码、假 UI 文案。
- 功能面必须正交，承载文字或点击的面不得倾斜、透视、梯形化。
- 文字槽必须是安静底面：不能有折痕、裂痕、撕边、强半调、低多边形尖角、阴影或贴纸边穿过。
- 低多边形质感用大块色面深浅表达，不做密集小点、细孔、细划痕、旧档案脏污。
- 纸面是现代印刷纸，不是泛黄旧案、旧报纸或怀旧办公室。
- 如果素材外观不服从合同，判素材失败，回 brief / 生图 / 美术修正；不得静默迁就素材。

## 4. 左卡纵向切片 brief

`left_region_card` 固定合同：

- 外框：204x160，2x 生产为 408x320。
- 参考分辨率位置：`[44,24] / [44,196] / [44,368] / [44,540]`。
- `photo_slot = [21,24,174,64]`。
- `label_plate = [22,104,114,32]`。
- `meta_line = [22,138,96,10]`。
- `icon_badge = [8,8,32,32]`。
- `action_badge = [158,106,38,38]`。

四状态：

| state | 色彩 / 语义 | 图标 |
| --- | --- | --- |
| `selected` | 橄榄绿，当前选中 | check |
| `available` | 青蓝，可派遣 / 可进入 | target |
| `warning` | 赭黄 / 红橙警示 | warning triangle |
| `locked` | 中性灰，锁定 | lock |

左卡验收点：

- 四张卡必须同尺寸、同槽位、同热区。
- 不能出现某张状态高/宽不同、上缘空间被压扁、图片槽裁切失控。
- 图片槽不得被横向压扁；如果美术图比例不合，回素材，不压缩图片。
- `label_plate` 是短纸签，不是整卡大白框。
- `meta_line` 只能轻量承载副信息；若字太挤，优先调整文案或后续字体 token，不改卡尺寸。

## 5. 轻合同并行捎带

这三类不进入本轮主裁决，只作为后续 atlas 前补齐项：

- `map_panel`：只需明确底图烘焙边界。地图底板、低多边形大陆、暗蓝网格可烘焙；pin、路线、选中光圈、hover、点击热区全部运行时。
- `top_status_strip`：低密度状态条，记录尺寸、图标/色块网格、禁入区即可。
- `icon_badge`：只做图标清单和尺寸网格；方形仅用于 icon / sticker / badge，不反套到主组件。

## 6. v0.9 左卡切片输出

本轮输出路径：

- 线框生图锚点：`docs/screenshots/2026-06-24-world-map-benchmark-landing/373-world-map-wmw-v0-9-left-card-wireframe-prompt-anchor.png`
- 生图候选 A：`docs/screenshots/2026-06-24-world-map-benchmark-landing/374-world-map-wmw-v0-9-left-card-imagegen-candidate-a.png`
- 几何 QA：`docs/screenshots/2026-06-24-world-map-benchmark-landing/375-world-map-wmw-v0-9-left-card-imagegen-candidate-a-geometry-qa.png`
- atlas 候选：`docs/screenshots/2026-06-24-world-map-benchmark-landing/376-world-map-wmw-v0-9-left-card-candidate-atlas-2x.png`
- 运行时回填预览：`docs/screenshots/2026-06-24-world-map-benchmark-landing/377-world-map-wmw-v0-9-left-card-vertical-slice-runtime-fill.png`
- 运行时 QA：`docs/screenshots/2026-06-24-world-map-benchmark-landing/378-world-map-wmw-v0-9-left-card-vertical-slice-runtime-fill-qa.png`
- manifest：`docs/screenshots/2026-06-24-world-map-benchmark-landing/379-world-map-wmw-v0-9-left-card-vertical-slice-manifest.json`
- Godot 单组件截图：`380-world-map-wmw-v0-9-left-card-godot-single-component.png`、`381-world-map-wmw-v0-9-left-card-godot-single-component-qa.png`（windowed opengl3；仅对应候选 A）
- 候选 B 输出：`382` 无字几何锚点、`383` 生图候选、`384` 几何 QA、`385` atlas 候选、`386/387` Python 回填、`388` manifest、`389/390` Godot 单组件截图（windowed opengl3，已验证非黑帧）。

## 7. 本轮判断口径

如果 v0.9 生图候选有轻微风格偏差，但几何服从，可以继续进入左卡美术微调。

如果 v0.9 生图候选无字、正交、同构，但比例仍偏宽，结论不是“合同错了”，而是：

> 生图素材没有完全服从合同；下一步应使用 wireframe anchor + 局部编辑 / 美术手修，让资产回到 204x160，而不是压缩图片或修改运行时槽位。

本轮候选 A 的实际结果：

- 无字：通过人工目检。
- 功能面正交：通过人工目检。
- 四状态同构：通过人工目检。
- 合同比例：未通过，检测比例约 `1.34-1.37`，目标为 `1.275`。
- 运行时回填：已生成 Python 回填预览，能暴露文字槽与生成图短标签仍不完全贴合。
- Godot 单组件：已在 windowed opengl3 下通过；`--headless` 不支持 UI texture capture，不是脚本逻辑错误。注意：380/381 只可作为候选 A 的运行证据。

本轮候选 B 的实际结果（2026-07-08 追加）：

- 无字几何锚点：`382-world-map-wmw-v0-9-1-left-card-no-text-wireframe-anchor.png`。
- 生图候选：`383-world-map-wmw-v0-9-1-left-card-imagegen-candidate-b.png`。
- 几何 QA：`384-world-map-wmw-v0-9-1-left-card-imagegen-candidate-b-geometry-qa.png`。
- 合同比例：通过，检测比例约 `1.25-1.29`，目标为 `1.275`。
- atlas 候选：`385-world-map-wmw-v0-9-1-left-card-candidate-b-atlas-2x.png`。
- Python 运行时回填：`386/387` 已生成，可用于文字贴合与局部美术复审。
- Godot 单组件：`389/390` 已用候选 B atlas 生成并通过非黑帧校验（runner：`scripts/run_wmw_godot_capture_v09.ps1`）。早先“signal 11”未在常规本地 shell 复现；另曾出现全黑帧问题，已通过在 capture 脚本中等待 `RenderingServer.frame_post_draw` 并拒绝全黑帧修复。

只有当左卡切片在以下四项同时通过后，才允许批量生产其余 class：

1. 生图 / 美术素材几何通过。
2. atlas / manifest 与合同一致。
3. Godot 单组件动态文字回填通过。
4. 整屏 100% 局部截图看起来像正式游戏 UI，而不是贴字验证稿。
