# Delivery Manifest：区域任务台图钉与短签纵向切片

> 日期：2026-07-16
> 当前 Gate（2026-07-17 修订）：技术、裁切、运行时与 UI / UX 功能通过；用户美术质量复核未通过，不得作为美术 production candidate。

## 资产

- `rt-task-pin-shell-v2-3x.png`：192×240 透明图钉壳，运行时缩放至 64×80，装入 72×80 命中框。
- `rt-task-pin-label-v2-2x.png`：400×144 透明无字短签，运行时固定 200×72；不启用 NinePatch。
- 两者均不含运行文字、事件 icon、状态色、外投影或地图背景。
- 运行时内容安全区：短签 `[14, 8, 166, 56]`；图钉 anchor `[36, 76]`（命中框坐标）。

## 真实运行接入

- `WeeklyRunRegionEventPin.gd` 以 TextureRect 装入两张透明资产。
- 中文标题与 meta、事件符号、双状态环、禁用线和 assigned / urgent / locked 角标由 Godot 叠加。
- 短签 `mouse_filter = IGNORE`，不会形成覆盖图钉的第二命中区。
- selected 标签持久；hover 标签临时；右边缘使用左挂点。
- 5 个同点事件使用 164px 内运行时避让；8 个同密集 cell 使用程序聚合标记并可展开。

## 验证

| 项目 | 结果 |
| --- | --- |
| alpha 可见污染 | PASS，magenta-like visible pixels = 0 |
| pin 3x → 64×80 | PASS |
| label 2x → 200×72 | PASS，固定尺寸 |
| 组件裁切 inventory | PASS，18 class；`10 / 5 / 2 / 1` |
| manifest 资产加载 | PASS，Godot 4.6.3 |
| 0 / 1 / N / 五点密集 | PASS |
| selected 短签与相邻 pin 8px 视觉净距 | PASS，P1 复核修正 |
| 8 点 cluster 收拢 / 展开 | PASS |
| selected 唯一持久短签 | PASS |
| 右边缘 label clamp | PASS |
| 7 / 8 / 9 行 dossier 压力 | PASS |
| 主流程进入区域任务台与派遣 | PASS |
| 1920×1080 / 1600×900 截图 | PASS |
| hover → selected 动态证据 | PASS，真实 Godot 帧 GIF |

## 证据入口

- 截图说明页：`docs/screenshots/2026-07-16-region-task-pin-slice-v2/index.html`
- 状态矩阵：`docs/screenshots/2026-07-16-region-task-pin-slice-v2/05-runtime-state-matrix.png`
- 动态演示：`docs/screenshots/2026-07-16-region-task-pin-slice-v2/06-hover-select-runtime-demo.gif`

## 已知环境差异

- Godot 4.6.2 在本机编辑器导入阶段持续触发引擎级 `signal 11`。
- 同一项目改用已安装的 Godot 4.6.3 后，manifest、board、主流程测试与窗口捕获全部通过；未把 4.6.2 崩溃误记为功能通过。

## 下一 Gate

本清单证明 pin + label 的技术生产路线可行。2026-07-17 用户指出当前组件美术不如效果稿，`rt_event_card_mother` 解锁暂时撤回；先返工并重新取得用户视觉确认。不因此解锁 dossier、CTA、整屏挖图或批量生成。

## 双复核结论

- `ui_designer`：最终 GO，P0 = 0、P1 = 0；允许解锁 event card。
- `ux_laoge`：最终 GO，P0 = 0、P1 = 0；允许解锁 event card。
- 首轮共同 P1 为“五点密集时 selected 短签遮挡相邻 pin”。运行时现将 selected label rect 以 8px clearance 加入其它 pin 的 displacement，复核图 `07-five-dense-selected-label-clearance.png` 已确认关闭。
- **范围修订（2026-07-17）**：上述 GO 只覆盖 UI / UX 功能和落地可行性，不能替代 benchmark 视觉复审。当前资产状态为 `production_feasible / visual_quality_reopened_by_user`。
