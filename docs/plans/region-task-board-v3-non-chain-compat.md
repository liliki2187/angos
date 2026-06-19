# 地区任务台 v3.4 非深链兼容态

日期：2026-06-18

目的：验证地区任务台在“当前选中任务不是深度链”的情况下，仍能使用同一套左卡、地图、右详情、底部事件结构。

## 核心规则

- 非深链任务不出现链线、`1/4`、`2/4`、`下一环 ?`、`当前环`、`未揭示` 等深链语法。
- 地图仍是任务点选与空间定位区，但非深链只显示 `pin + selected 短签`。
- 左侧任务卡恢复为普通任务索引：点击左卡或地图 pin 都选中同一任务。
- 右侧原“深度调查槽”泛化为“任务特殊状态槽”，但普通任务不显示该槽。
- 普通任务的默认规则并入右侧大文本框，删除信息后必须回收空间。
- 红色截稿、线索调查、深度链等特殊状态只使用短票据，不再做大卡抢正文空间。
- 底部中段继续显示地区事件 / 全局 buff-debuff，不改成当前任务说明。
- `推进一天` 是全局日程动作，使用独立底部按钮语法，不和 `进入派遣签批` 共用红色任务 CTA 语法。
- `推进一天` 不得出现在右侧任务 CTA 的正下方或相邻热区内；所有任务类型都必须保持任务签批和全局日程推进的空间分离。

## 类型兼容

| 类型 | 左卡 | 地图 | 右侧特殊状态槽 | CTA |
| --- | --- | --- | --- | --- |
| 普通白色调查 | 普通任务卡，选中金框 | 单 pin + `51区 / 可点任务` | 无；规则并入主文本框 | `进入派遣签批` |
| 红色截稿 | 红条 + `截稿`章 + 剩余天数 | 红色急件 pin + `截稿 / 可点任务` | 短票据：`红色截稿 · 剩4天；过期关闭` | `抢占截稿窗口` |
| 线索调查 | 青蓝线索卡 | 青蓝 pin + `线索 / 可点任务` | 短票据：`线索调查；成功后生成新任务` | `派遣线索调查` |
| 已派遣执行中 | 降权只读卡，显示执行中/到期 | pin 叠执行中状态或头像 | `执行状态：已派遣、到期、可查看/撤回` | `查看派遣单` 或 disabled `等待结算` |

## 验证产物

- 普通白色调查：`docs/screenshots/2026-06-18-region-task-v3-4-compact-status/normal-task-compat-fill.png`
- 红色截稿：`docs/screenshots/2026-06-18-region-task-v3-4-compact-status/deadline-task-compat-fill.png`
- 线索调查：`docs/screenshots/2026-06-18-region-task-v3-4-compact-status/lead-task-compat-fill.png`
- 生成脚本：`scripts/art/build_region_task_v3_non_chain_compat.py`

## 后续落地

- `task_special_state_slot` 应支持 `deadline / clue / chain / running` 四类特殊态；`normal` 不生成槽位。
- 非深链地图组件只需要 pin、selected ring、hover short label；深链地图组件才需要 current ring card、future `?`、chain line。
- 截稿倒计时的主承载位在左卡和右侧特殊状态槽；底部事件只显示地区/全局影响，不再给第二套倒计时。
- 线索调查成功后生成新任务 pin，但生成前不显示成深链下一环。
- 底部 `advance_day_button` 应拥有独立素材 / 状态：default、hover、pressed、disabled、confirming；不应借用任务 CTA 贴图。`confirming` 态文案建议为 `确认推进？ / 再次点击执行`，用于防止玩家误触全局时间推进。
- `task_dispatch_cta.hit_rect` 与 `advance_day_button.hit_rect` 必须是两套互不相邻的热区；装饰底板、斜纹、红色托盘和底部票据不得扩大为隐藏点击区。
