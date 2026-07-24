# WMW 整屏功能真值 v5.1 Delivery Manifest

## 决策条

- **结论**：v5.1 黑白两态通过几何、UX 回归与用户视觉裁决，已冻结为当前整屏黑白布局真源；仍为 `TARGET_ONLY`。
- **影响**：A233 / B、三栏和底部 CTA 保留；v5 中时间、锁区、路线和任务分类 drift 已在结构稿中止血。
- **下一步**：进入资产化 / 有色映射 brief，先定义黑白结构到既有 WMW 视觉资产的逐区映射；不得直接跳到有色整屏或 runtime。

## 交付清单

| 文件 | 字节 | SHA-256 |
| --- | ---: | --- |
| `black-white-full-map-v5-1-default.png` | 137374 | `C7534894BA44432535122E5AA056D4E45D1D57CE9168B46A00DA25B9F3ACEBFD` |
| `black-white-full-map-v5-1-schedule-confirming.png` | 142090 | `9128F143E30DC3D8812064EE30CD454B5143FD65E17796C815496EBB7FBF5C98` |
| `black-white-full-map-v5-1-audit.json` | 4700 | `A85EF6DAB6F7E7109965A47101F0B629A08F55844F495F9B9C272D399182FB88` |
| `render_full_map_functional_truth_v5_1.py` | 14681 | `18C480F8B93A70C0125424B19919A99662372C22EC6C05A3162DB1A43B219021` |

> 哈希对应 2026-07-20 本轮最终重跑结果；后续修改脚本或图片必须重新计算。

## Manifest

- **交付对象**：WMW 1920×1080 整屏黑白功能结构 v5.1 默认态 / 日程确认态。
- **产物类型**：`structure_wireframe_state_pair`。
- **风险等级**：normal。
- **它能证明**：A233 / B 删除“红线升温”无独立信息缺口；静态结构中的时间、锁区、任务分类、路线和两态差量已对齐现有真值；允许区外像素变化为 0。
- **它不能证明**：独立推进日已实现、A5.1-H 已接入、截止日在 runtime 会刷新、锁定地区点击反馈成立、正式美术通过。
- **真值 fixture**：`week=1`、`current_day=1`、`remaining_days=7`、`reputation=45`、`roswell_dossier=false`、东亚/太平洋锁定。
- **主要几何**：左 342、中 924、右 480；地图 `[426,96,924,936]`；日程 `[36,810,342,246]`；右栏 `[1398,24,480,1032]`；CTA `[1425,957,426,75]`。
- **几何审计**：默认 / 确认相对 v5 的 `outside_allowed_pixels=0`；两态差异只在日程器，`outside_schedule_pixels=0`。
- **父级目检**：两张原始 1920×1080 PNG 已检查；路线清除后大陆 / 网格连续，锁定 pin、右栏标题、任务列表和 CTA 无新断口。
- **agent 链路**：先由 `ux_laoge` 完成功能终审，再由 `ui_designer` 给出精确 v5.1 结构，生成后由 `ux_laoge` 回归；最终 `P0=0 / P1=0 / P2=2`，其中重复文案 P2 已执行。
- **用户裁决**：已接受 `常驻 2 · 限时 1 · 深链 1`、正文第二行及两态整体视觉；登记为 A237。
- **未调用 agent**：冷备 `game_logic_check` 未获用户解冻确认；runtime 前仍建议解冻。
- **未改范围**：Godot、正式合同、compact A5.1 frozen、有色稿、生产美术、三栏大结构。
- **反向读法检查**：不得把 `TARGET_ONLY` 图称为游戏运行截图；不得把静态确认态称为 advance_day 已实现；A237 冻结的是整屏黑白布局与文案，不是 compact A5.1 或 Godot 正式合同。

## Gate

- 1920×1080：PASS。
- A233 / B：PASS。
- 三栏与 CTA 几何：PASS。
- 初始锁区真值：PASS。
- 日程默认 / confirming：PASS（静态结构）。
- 任务数量与内容类型：PASS。
- 无 edge 路线删除：PASS。
- 允许区外像素：PASS，0。
- UX 回归：PASS，P0=0 / P1=0。
- 用户视觉裁决：PASS，A237。
- runtime / Godot / 正式合同 / 有色稿：NOT STARTED，本轮禁止误报。
