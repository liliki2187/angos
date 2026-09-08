# A339 世界地图资产化前规划 Delivery Manifest v2

日期：2026-09-01  
替代：同日初版 Delivery Manifest（初版记录了验证前状态）

## 交付物

| 交付物 | 路径 | 身份 |
| --- | --- | --- |
| 页面装配规格 | `docs/plans/world-map-benchmark-landing/2026-09-01-world-map-a339-asset-assembly-spec.md` | 人类可读规格候选 |
| 页面机器合同 | `design/ui-contracts/world-map/world_map_page_assembly.json` | `0.9.0 implementation_planning_candidate` |
| UI / UX 交接 | `docs/plans/world-map-benchmark-landing/2026-09-01-world-map-a339-ui-ux-handoff.md` | 父级合并裁决 |
| 合同审计 | `docs/plans/world-map-benchmark-landing/2026-09-01-world-map-a339-assembly-audit.json` | 关键不变量机器审计 |
| 分层结构板 | `C:/Users/gzfangyue/.codex/visualizations/2026/08/10/019fe9bb-6bca-71b3-822b-69174b4f780a/world-map-asset-layers.html` | 对话内说明图，不是游戏资产 |
| Router Card | `docs/plans/world-map-benchmark-landing/2026-09-01-world-map-a339-asset-assembly-router-card.md` | 工作流路由记录 |

## 已取得证据

- JSON 成功解析；
- `reference_resolution = 1920×1080`；
- `interactive_node_count = 8`；
- `canonical_image_ratio = 69:44`；
- Schedule 与 Dossier 关键冻结 rect 通过；
- 规格文档与分层结构板文件存在；
- 关键不变量审计 `all_pass = true`。

## 证据边界

本次审计只证明合同形状和关键不变量，不证明：

- 生产美术质量；
- 浏览器结构板实际渲染截图；
- 运行时字体清晰度；
- 三枚 Beacon 精确 rect；
- Godot 装配；
- atlas 或最终 manifest 就绪。

结构板的自动浏览器渲染检查因本地 sandbox helper 异常未完成；不影响合同 JSON 的只读解析结果，但在结构板被升格为正式 QA 证据前必须补跑。

## Gate

当前状态：`CONTRACT_DRAFTED / KEY_INVARIANTS_PASS / ASSET_PRODUCTION_AWAITING_DIRECTION_CONFIRMATION`。

允许的下一动作：确认本装配方向后，只启动 `right_dossier_page` 第一条 vertical slice 的无字母版生成、切件和安全区测量；仍不进入整页 Godot 或 WeeklyRunGame。

