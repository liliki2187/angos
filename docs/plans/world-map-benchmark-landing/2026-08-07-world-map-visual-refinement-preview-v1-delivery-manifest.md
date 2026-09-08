# 世界地图视觉返修局部预演 v1 交付清单

## 结论

本轮只完成视觉预演，不进入 atlas、manifest、Godot 或 `WeeklyRunGame` 接线。北美选中证据簇与 Dossier / Schedule 纸层接触已完成局部改前 / 改后合成；UI Designer 与 UX 老哥最终均判定视觉预演阶段 `PASS`，P0=0、P1=0。

当前状态：`diagnostic_local_refinement_insufficient_rejected_as_next_visual_target`。

## 用户视觉 Gate 修订

2026-08-07 用户审阅后明确指出本轮改动幅度过小，需要结合 A291 风格稿重新判断。此前 UI / UX 的 `PASS` 仅保留为局部工艺与功能安全证据，不再代表整屏视觉方向通过。本目录全部产物降级为诊断样本，不得进入资产化或运行时落地。

## 本轮修改范围

- 北美证据簇：照片保持 `207×132 / 69:44` 完整 UV；照片、黄色便签、Eye、地区标签重新分层；删除地图内重复的红色风险文字。
- 地区标签：统一 `no_decor_text_safe_rect=[714,328,156,62]`；连接线在 `x=704` 后断开、`x=880` 再起，安全区内无机构线。
- 红线状态：Dossier 顶部完整文字为主承载，Eye `WarningNotch` 为地图无文字回声，左卡红字为辅助。
- Dossier：FrontCarrier 不动；两张后页使用不同冷暖、错位与接触阴影；夹子区分 `clip_bbox=[1624,4,52,48]` 与 `contact_rect=[1626,24,48,12]`。
- Schedule：FrontCarrier 不动；两张薄后页仅用轻微色差、错位与接触阴影表达厚度，不增加夹具、箭头或第三页。

## 冻结边界

- Dossier `[1416,24,468,1032]`
- Schedule `[36,810,372,246]`
- Hero `[1443,174,414,264]`
- Disclosure `[1443,596,414,56]`
- CTA `[1443,956,414,76]`
- canonical 新闻图、Eye 状态族、既有文字槽与 hit rect 全部不动
- 新控件 `0`，新热区 `0`

## 交付物

- 完整整屏预演：`image_gen/2026-08-07/world-map-visual-refinement-preview-v1/01-full-screen-refined-preview.png`
- 局部改前 / 改后对比：`image_gen/2026-08-07/world-map-visual-refinement-preview-v1/02-before-after-local-comparison.png`
- 机器审计：`image_gen/2026-08-07/world-map-visual-refinement-preview-v1/03-visual-refinement-audit.json`
- 可重复生成脚本：`scripts/ui-contracts/wmw/build_world_map_visual_refinement_preview_v1.py`

## 审查结果

- UI Designer：`PASS`。证据簇层级、纸层主次与 clean low-poly weekly 同族关系成立；剩余仅照片框明度与轻接触影等非阻塞 P2。
- UX 老哥：最终 `PASS / P0=0 / P1=0 / P2=1`。唯一 P2 为 Schedule 原有禁用说明块仍略带控件轮廓，但文案与无输入合同足以避免假操作。
- 机器审计：`connector_vs_text_safe_rect_intersection=false`、`canonical_ratio_pass=true`、`clip.top_clearance_pass=true`、`new_controls=0`、`new_hit_rects=0`。

## 尚未证明

- 本轮 PNG 不能证明 `mouse_filter`、焦点、hover / pressed / disabled、状态切换残留或缩放采样。
- 用户确认视觉方向前，不得把本轮预演称为生产冻结，也不得进入 runtime 落地。
