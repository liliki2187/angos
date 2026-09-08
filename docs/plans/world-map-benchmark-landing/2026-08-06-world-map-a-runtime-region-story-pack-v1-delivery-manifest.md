# 世界地图 A 风格地区新闻母图包 v1 交付清单

## 结论

东亚与太平洋两张旧 SVG 占位图已替换为真实 ImageGen 新闻母图，并保持与北美一致的 `69:44` 同资源复用合同。当前仍是 `runtime_state_preview_region_story_pack_pass_pending_user_visual_gate`；自动测试与 UI / UX 双审均通过，等待用户审阅实际整屏观感。

## 资产矩阵

| 地区 | 单一异常关系 | 生成来源 | Runtime 资源 |
| --- | --- | --- | --- |
| 东亚神秘地带 | 宽阔阶梯式现代观测建筑穿过骨白圆月中心 | Codex 内置 ImageGen，参考 A 风格稿与北美母图 | `east_asia_story_1104x704.png` |
| 太平洋失航带 | 倾斜民用海洋监听碟内部装着绝对水平海面 | Codex 内置 ImageGen，参考 A 风格稿与北美母图 | `pacific_story_1104x704.png` |

来源、提示目标与哈希见：`image_gen/2026-08-06/world-map-region-story-pack-v1/`。

## 运行规格

- 三个地区均使用唯一 `1104×704`、`69:44` PNG。
- 左侧列表完整等比显示 `138×88`，`STRETCH_KEEP_ASPECT_CENTERED`。
- 右侧档案完整等比显示 `414×264`；当前北美卡与档案已断言同一资源路径，东亚 / 太平洋解锁后沿用同一组件和同一映射表。
- 图片不烘焙文字、边框、锁定、警告、选中圈或按钮暗示；所有状态均由 Godot runtime 负责。
- `WorldMapIntegratedAbstractImage.gd` 已移除东亚 / 太平洋旧 SVG preload，改用本包 PNG。

## 自动 Gate

- Godot 4.6.2：`test_world_map_integrated_prototype.gd OK`。
- 东亚、太平洋 source size：`1104×704`。
- 东亚、太平洋 card display：`138×88`。
- 三地区 stretch：`STRETCH_KEEP_ASPECT_CENTERED`。
- 三地区 resource path 均指向 `a_style_v2_runtime/*_story_1104x704.png`。
- 交互节点仍恰好 8 个；locked 点击不替换 selected 或 dossier；disclosure 展开不移动 CTA。

## 真实证据

目录：`docs/screenshots/2026-08-06-world-map-a-runtime-region-story-pack-v1/`

- `01-selected-collapsed.png`
- `02-locked-feedback.png`
- `03-selected-expanded.png`
- `04-hit-rect-review.png`
- `05-interaction-state-sequence.gif`

截图由 Godot 4.6.2 windowed OpenGL3 真实渲染；headless 只用于自动断言，不作为 UI 截图来源。

## 双终审

- UI Designer：`PASS / P0=0 / P1=0`。东亚与太平洋在锁定调光后的 `138×88` 中均一秒可辨，与 V2 和北美属于同族。
- UX 老哥：`PASS / P0=0 / P1=0`。锁定态无状态误导；点击锁定地区后北美选区、dossier、展开容量与 CTA 均保持。
- 非阻塞 P2：东亚未来可强化“穿透”而非“遮挡”；太平洋未来可删除左上小月亮并合并碟腔局部碎面。

## 阶段边界

- 本轮不升格为 `production_frozen`。
- 本轮不声称用户已经接受两张新图的最终观感。
- 用户确认前不接正式 `WeeklyRunGame`；若用户否决，只重生被点名的地区母图，不重开 A282 布局、北美母图或符号包。
