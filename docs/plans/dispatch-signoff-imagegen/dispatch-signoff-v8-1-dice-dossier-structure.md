# 任务派遣 / 签批外勤界面：V8.1 本次骰池案卷结构稿

日期：2026-06-23

定位：V8.1 是对 V8 “路线纸 / 去哪里”拟物越界的机制回正。用户指出路线纸虽然有趣，但游戏内没有路线规划或站点选择功能，因此中央下方改为真实游戏机制承载物：`本次骰池预备纸`。

## 截图

- 默认结构：`docs/screenshots/2026-06-23-dispatch-signoff-v8-1-dice-dossier/01-dispatch-signoff-v8-1-dice-dossier-default.png`
- 职责标注：`docs/screenshots/2026-06-23-dispatch-signoff-v8-1-dice-dossier/02-dispatch-signoff-v8-1-dice-dossier-overlay.png`
- 中央裁切：`docs/screenshots/2026-06-23-dispatch-signoff-v8-1-dice-dossier/03-dispatch-signoff-v8-1-dice-dossier-central-crop.png`

## 与 V8 的区别

- 删除高权重 `路线纸 / 北美禁区 → 夜间站台` 功能物件。
- 中央下方改为 `本次骰池预备纸`，展示 4 个员工骰 + 1 个器材骰的组成。
- `随队器材` 在中央改口为 `辅助骰位 1/1`，说明 `匿名热线录音` 是一次性道具骰、不占人员槽。
- 任务短条从 `去哪里` 改为 `深度调查 · 外勤2天 · 签批后判定`。
- 右侧签批票据仍是唯一完整复核位，中央骰池纸只展示组成，不承接最终可签批结论。

## 保留的 V8 主语

V8.1 仍保留“编辑部外勤案卷桌面”的代入感：人员证件卡被放入案卷桌面，辅助骰位托盘写回本次队伍，右侧签批回执等待盖章。区别是：代入感不再来自路线规划，而来自玩家真实会操作和判断的 `本次骰池`。

## 进入真实内容风格稿前 Gate

1. 中央不能暗示玩家要规划路线、选择站点或分派地点。
2. 中央必须能读出 `谁去 / 带什么 / 本次骰池由哪些骰组成`。
3. `本次骰池预备纸` 不得膨胀为完整复核表；需求覆盖、达标率、缺口、风险和耗时的完整结论仍在右侧票据。
4. 路线、地图、图钉如保留，只能进入 no-text 背景层或低权重装饰层。
5. 后续高保真生图 prompt 应使用 `dice pool preparation sheet / character dice / item dice` 作为中央机制关键词，不再使用 `route planning map / route selection / waypoint planning`。
