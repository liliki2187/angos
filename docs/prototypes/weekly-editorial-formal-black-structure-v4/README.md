# 发刊编辑正式界面黑白结构稿 v4

## 本轮变化

- 左栏删除名称搜索，不要求玩家输入报道标题。
- 栏头在原 `288×48` 高度内加入两个 `44×44` 入口：`筛` 与 `序`，候选列表仍从 `y=80` 开始。
- 类型筛选只消费 `recipe_type`：全部、抢先快讯、深度报道、个人专栏、爆炸性新闻；具体类型可多选。
- 排序消费真实字段：`quality` 对应等级，`acquired_order` 对应本周候选池内的获得先后。
- 默认按获得时间新到旧排列；也可选择获得时间旧到新、等级高到低、等级低到高。
- 筛选与排序都只改变左栏可见集合，不触发推演重算，也不取消已选来源。
- 若筛选隐藏当前已选稿，栏头改为“已选报道被隐藏 / 显示并定位”；玩家修改筛选后会结束临时显示。

## 仍然冻结的结构

- 桌面 `1920×1080`、固定三栏。
- 中间双页始终同时完整可见。
- 8 张候选卡在 1080p 内完整可见；12 张时只滚动左栏。
- 定向替换、替换后重算、右栏固定阻断与唯一主 CTA、确认送印冻结双页等 v3 规则不变。
- 本稿仍是功能、交互和布局候选，不是最终视觉包装；尚未进入 Godot，也未升版组件合同。

## 可复现预览参数

- `?candidates=12`：显示 12 条候选稿。
- `&filter=r2,r4`：按类型筛选，可用 `r1` 至 `r4`，逗号分隔。
- `&sort=quality_desc`：可选 `quality_desc`、`quality_asc`、`acquired_desc`、`acquired_asc`。
- `&candidateMenu=filter` 或 `candidateMenu=sort`：打开对应浮层。
- `&showSelected=1`：临时显示被筛选隐藏的已选稿。

页面提供 `window.editorialWireframe` 调试接口和 `getAuditState()` 自动审计状态。

## 验证证据

- 默认获得时间新到旧：`docs/screenshots/2026-07-20-weekly-editorial-formal-black-structure-v4-filter-sort/01-default-acquired-new-to-old.png`
- 深度报道 + 爆炸性新闻多选：`docs/screenshots/2026-07-20-weekly-editorial-formal-black-structure-v4-filter-sort/02-filter-deep-and-breaking.png`
- 等级高到低：`docs/screenshots/2026-07-20-weekly-editorial-formal-black-structure-v4-filter-sort/03-sort-quality-high-to-low.png`
- 真实点击动态演示：`docs/screenshots/2026-07-20-weekly-editorial-formal-black-structure-v4-filter-sort/04-filter-sort-interaction-demo.webp`
- 自动审计：`docs/screenshots/2026-07-20-weekly-editorial-formal-black-structure-v4-filter-sort/audit.json`
