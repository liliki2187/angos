# A339 世界地图资产化前规划 Delivery Manifest

日期：2026-09-01

## 交付物

| 交付物 | 路径 | 身份 |
| --- | --- | --- |
| 页面装配规格 | `docs/plans/world-map-benchmark-landing/2026-09-01-world-map-a339-asset-assembly-spec.md` | 人类可读真源候选 |
| 页面机器合同 | `design/ui-contracts/world-map/world_map_page_assembly.json` | `0.9.0 implementation_planning_candidate` |
| 分层结构板 | `C:/Users/gzfangyue/.codex/visualizations/2026/08/10/019fe9bb-6bca-71b3-822b-69174b4f780a/world-map-asset-layers.html` | 对话内说明图，不是游戏资产 |
| Router Card | `docs/plans/world-map-benchmark-landing/2026-09-01-world-map-a339-asset-assembly-router-card.md` | 工作流路由记录 |

## 证据范围

- 已录入 1920×1080 五个冻结区域。
- 已录入三张 RegionCard、三枚 Map Beacon、Disclosure、CTA 共 8 个交互节点。
- 已录入 69:44 母图完整等比复用合同。
- 已录入页面层级、唯一选择真值、`selected+locked` 合法、Disclosure 展开 CTA 不移动。
- 已录入运行时功能字号下限与 Dossier 最大内容容量。
- 已把 A339 合成图标记为 `reference only / do not crop as runtime asset`。

## 尚未取得的证据

- 终端 helper 当前异常，JSON 解析、矩形审计和仓库 diff 尚需在本轮结束前补跑；未补跑时不得声称机器验证通过。
- 三枚 Beacon 的精确 rect 未冻结。
- ISSUE 票签 exact rect 未冻结。
- Schedule 无字母版的 content/no_text rect 未测量。
- RegionCard 依 A305 与 `left_region_card.json v1.0.0` 正式采用 `340×170`；旧 `86:41` 已退役为历史 evidence，不再构成阻断。
- 没有生成无字生产资产、atlas、最终 manifest、Godot 场景或 runtime 截图。

## Gate

当前状态：`CONTRACT_SYNCED / DOSSIER_VISUAL_SLICE_COMPLETE / REGION_CARD_SLICE_READY / RUNTIME_BLOCKED`。

允许的下一动作：在 Dossier 视觉切片后启动 `left_region_card` 第二条 vertical slice；只做单一共享无字母壳、状态矩阵、canonical 图片回填与 QA，不进入 atlas、最终 manifest 或 Godot。

