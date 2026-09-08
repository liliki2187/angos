# 世界地图精确 Filled-State v1 交付清单

## 结论

用户确认 A336 的纸材、配色、明亮度和编辑部氛围后，本轮以三个真实 ImageGen 无字母壳和冻结 UI 合同装配出完整 `1920×1080` 最大内容态候选。程序只负责裁配、文字、坐标、状态和 QA，不生成纸纹或美术表面。

当前身份：`precise_filled_state_visual_target_candidate / pending_user_visual_gate`。机器合同通过不等于用户视觉通过，不进入 atlas、manifest、Godot 或 `WeeklyRunGame`。

## 主产物

- `image_gen/2026-09-01/world-map-filled-state-precision-v1/01-filled-state-visual-target-1920x1080.png`
- `image_gen/2026-09-01/world-map-filled-state-precision-v1/02-a291-vs-filled-state-side-by-side-3840x1080.png`
- `image_gen/2026-09-01/world-map-filled-state-precision-v1/02b-a291-vs-filled-state-side-by-side-1920x540.png`
- `image_gen/2026-09-01/world-map-filled-state-precision-v1/03-left-column-100pct-review.png`
- `image_gen/2026-09-01/world-map-filled-state-precision-v1/04-map-field-100pct-review.png`
- `image_gen/2026-09-01/world-map-filled-state-precision-v1/05-dossier-100pct-review.png`
- `image_gen/2026-09-01/world-map-filled-state-precision-v1/06-contract-qa-overlay-1920x1080.png`
- `image_gen/2026-09-01/world-map-filled-state-precision-v1/07-filled-state-audit.json`

## 美术来源

- `sources/01-imagegen-region-card-master-source.png`：统一 RegionCard 暖白纸与墨蓝 folio 母壳。
- `sources/02-imagegen-schedule-master-source.png`：同纸族 Schedule 母壳。
- `sources/03-imagegen-dossier-master-source.png`：同纸族 Dossier、夹子、背页与橄榄 CTA 母壳。
- A336 整屏：刊头、中央地图、证据照片、便签、猫与综合色彩母语。
- 三张正式 `1104×704 / 69:44` 新闻母图：只做完整等比缩放，不裁切、不拉伸、不另做缩略图。

## 冻结合同

| 项目 | 矩形或规格 |
| --- | --- |
| RegionIndex | `[36,154,372,640]` |
| Schedule | `[36,810,372,246]` |
| MapField | `[432,154,960,902]` |
| Dossier | `[1416,24,468,1032]` |
| RegionCard | `3 × 340×170`，位置 `[52,226] / [52,408] / [52,590]` |
| 左卡图片 | `3 × 138×88`，完整 `69:44` |
| Dossier 图片 | `414×264`，完整 `69:44` |
| Disclosure | `[1443,596,414,56]` |
| CTA | `[1443,956,414,76]` |

## 最大内容态

- 北美：`selected + warning`；东亚 / 太平洋：`locked + previewable`。
- Dossier 为 expanded，只读显示两条任务预览；任务行无独立 hit rect、无按钮底色。
- Disclosure 显示“已显示 2 / 共 4 条”与 `－`；CTA 原位，仍是唯一主行动。
- 删除截止日、剩余日、坐标、来源表、档案编号、伪表格与第二按钮。

## QA

- `canvas_pass=true`：严格 `1920×1080`。
- 三张 canonical source 均为 `1104×704`。
- 三张左卡 `138×88` 图槽与对应母图直接缩放结果逐像素一致。
- 右 Dossier `414×264` 图槽与北美母图直接缩放结果逐像素一致。
- `07-filled-state-audit.json`：`all_pass=true`，并记录全部源图 SHA-256 与冻结矩形。
- 首轮 QA 曾发现图片最外侧 `1px` 被边框覆盖；边框已移至图槽外侧后关闭，未改美术或布局。

## 双审

- UX 老哥：生成前冻结阅读链、P0/P1、删除字段与五秒主行动 Gate。
- UI Designer：生成前冻结元素表、真实文字密度、装饰白名单和精确矩形。
- 生成后子 agent 仍受 Windows `view_image helper_unknown_error` 阻断，因此没有伪造视觉 PASS；最终视觉方向等待用户目视裁决。

## 实现边界

- 生成脚本：`tmp/ui-screens/build_world_map_filled_state_precision_v1.py`。
- ISSUE 票签 exact rect 仍未资产化，本轮只作为刊头视觉层。
- 本轮不创建 atlas、asset manifest、Godot 节点或 `WeeklyRunGame` 接线。
