# 区域任务台组件裁切准入评估 v2

> 日期：2026-07-16
> 评估对象：`image_gen/2026-07-16/20260716_region-task-color-mood-E2-local-calibration-v1.png`
> 组件合同：`design/ui-contracts/region-task-board/component_cutout_inventory_v1.json`
> 本文件覆盖 2026-07-15 评估报告中的“组件身份、裁切分类和生产次序”；冻结页面几何、运行数据合同和既有测试证据仍以原报告及 `design/ui-contracts/region-task-board/` 为准。

## 决策

- **结论**：E2 继续作为 `filled-state text mock / 组合气质参考`，从 E2 直接裁成正式资产的组件数量为 **0**。
- **影响**：全页现登记 18 个组件 class；其中 9 类独立透明母版、6 类矩形 NinePatch、2 类不透明底图 / tile、1 类程序组件。未登记 class 不得进入生图或裁切。
- **下一步**：只允许先做 `rt_task_pin_shell_mother + rt_task_pin_label_mother` 单点纵向切片；通过透明边缘、缩小、anchor、状态与回插验收后再做事件卡。

## 1. 为什么当前整屏不能裁

E2 是 `1672×941 RGB` 压平稿，不是目标 `1920×1080` 分层源，也没有 alpha。它把真实文字、选中颜色、任务图标、图钉、短签、状态章、风险框、CTA 勾选、`OFFLINE`、纸张外投影和相邻组件遮挡画在同一层。任何从 E2 直接挖出的组件都会至少命中一项问题：

1. 缺失被相邻纸张或阴影遮住的完整轮廓；
2. alpha 边缘带深蓝地图 / 工作台底色；
3. 固定文字、图标或状态无法随真实数据变化；
4. hover / pressed / disabled 需要重新生成，造成同 class 几何漂移；
5. 1672×941 像素不能反向定义 1920×1080 合同坐标；
6. 外投影焊死后，运行时抬升和按压会产生双影。

所以本轮的“裁切”不是从整屏抠图，而是：**先独立生成单件无字母版，要求源文件自带干净 alpha，再按合同检查和导出。** 若模型没有给出可用 alpha，该结果直接退回，不靠复杂手抠抢救。

## 2. 完整 class 分类

| 类别 | 数量 | class_id | 是否复杂裁切 |
| --- | ---: | --- | --- |
| 独立透明母版 | 9 | `rt_event_index_shell`、`rt_event_card_mother`、`rt_event_type_icon_atlas`、`rt_task_pin_shell_mother`、`rt_task_pin_icon_atlas`、`rt_dossier_shell`、`rt_status_badge_atlas`、`rt_dispatch_cta_mother`、`rt_advance_day_gate_mother` | 源图必须直接提供干净 alpha；不允许人工从整屏抠 |
| 矩形 NinePatch | 6 | `rt_hud_strip`、`rt_hud_back_button_mother`、`rt_running_receipt_mother`、`rt_task_pin_label_mother`、`rt_dossier_section_plate`、`rt_schedule_info_plate` | 规则矩形画布，只检查透明角和拉伸区 |
| 不透明底图 / tile | 2 | `rt_board_surface_tile`、`rt_region_map_base_clean` | 不裁轮廓 |
| 程序组件 | 1 | `rt_cluster_marker_mother` | 不生图、不裁切 |

正式逐项字段、frame roster、尺寸、倍率、padding、阴影所有权、允许 / 禁止烘焙内容与状态派生方式已冻结在 [`component_cutout_inventory_v1.json`](../../../design/ui-contracts/region-task-board/component_cutout_inventory_v1.json)。JSON 是后续 prompt、文件名、manifest 与 QA 的机器真源；本报告只提供人工可读摘要。

## 3. 9 类独立透明母版

| asset_id | 运行尺寸 | 倍率 | 允许进入位图 | 必须留给程序 | 裁切准入 |
| --- | --- | ---: | --- | --- | --- |
| `rt_event_index_shell` | `380×804` | 2x | 文件夹外轮廓、内部纸边、禁字区内孔环 | 标题、任务卡、计数、滚动、当前书签、外投影 | 单件闭合轮廓；四周 12px alpha padding |
| `rt_event_card_mother` | `336×104` | 2x | 暖白正交票据轮廓、低权重无语义色块 | 标题、meta、icon、选中 / 紧急 / 已派遣状态、外投影 | 只出 1 枚母版；6px alpha padding；所有状态几何全等 |
| `rt_event_type_icon_atlas` | 单格 `44×44` | 3x | `sci / pop / occult` 三类粗线手绘 glyph | 纸底、贴纸边、文字、状态色 | 每格独立、不接触；四周 16% 空白 |
| `rt_task_pin_shell_mother` | 视觉 `64×80`，hit `72×80` | 3x | 中性纸质 pin 壳、内部纸边 | icon、ring、颜色、外发光、投影、地图 | stem 完整；asset anchor `[32,76]`；装入 hit control 时 x 偏移 4px |
| `rt_task_pin_icon_atlas` | 单格 `28×28` | 3x | `sci / pop / occult` 三类加粗小 glyph | pin 壳、纸色方块、发光 | 每格四周 18% 空白，缩小后线条不断裂 |
| `rt_dossier_shell` | `412×960` | 2x | 正交文书、橄榄夹板、禁字区内夹子 / 胶带、内部纸边 | 标题、摘要、`APPROVED`、风险红框、状态章、CTA、外投影 | 四周 10px alpha padding；摘要区必须完全安静 |
| `rt_status_badge_atlas` | 单格 `72×72` | 3x | `urgent / chain / hidden_locked / assigned / completed` 无字符号章 | `APPROVED`、任务 ID、风险板底色 | 每格闭合、无纸张背景；真实状态由数据选择 frame |
| `rt_dispatch_cta_mother` | `356×112` | 2x | 中性橄榄纸品轮廓、内部纸边 | 文案、勾、loading、disabled 原因、pressed 阴影 | 8px alpha padding；程序负责 hover / pressed / disabled / focus |
| `rt_advance_day_gate_mother` | `318×100` | 2x | 中性灰白时间票据轮廓、内部纸边 | 文案、`OFFLINE`、日历 / 沙漏、确认态、强右箭头、外投影 | 8px alpha padding；玩法命令接入前只允许 disabled，暂不授权正式生产 |

这里的 `requires_manual_cutout = false` 不是“不需要透明层”，而是更严格：**正式源必须已是独立透明 PNG，不允许把复杂手抠当作正常生产步骤。**

## 4. 6 类规则矩形 NinePatch

| asset_id | 运行尺寸 | 生产方式 | 不得烘焙 |
| --- | --- | --- | --- |
| `rt_hud_strip` | `1920×72` | 原生条带 + 平铺微纹理，必要时一枚 NinePatch | 刊名、地区名、期号、周次、剩余天数、语义状态点 |
| `rt_hud_back_button_mother` | `238×44` | Button + NinePatch StyleBox | 箭头、按钮文字、hover / pressed |
| `rt_running_receipt_mother` | 暂定 `336×96` | 无字回条 NinePatch；高度进入合同板复核 | 执行中 / 可处理 / 已选计数与趋势图 |
| `rt_task_pin_label_mother` | `200×72` | 一枚 NinePatch，hover / selected 共用 | 事件名、耗时、状态、selected 色、外投影 |
| `rt_dossier_section_plate` | `364×144` | 中性分区 NinePatch | 风险红框、链条青框、警告三角、字段文字 |
| `rt_schedule_info_plate` | `480×100`、`530×100` | 一枚横向可拉伸母版复用两处 | 栏目标题、计数、剩余天数、胶带遮挡文字 |

NinePatch 不需要复杂轮廓裁切，但仍必须从独立无字规则画布生产，不能裁 E2 中已经承载文字的矩形。

## 5. 不生图的部分

- `rt_board_surface_tile`：`ColorRect + 256×256` 可平铺微纹理；尺寸仍为暂定，路线已冻结。
- `rt_region_map_base_clean`：复用 2026-07-14 获选地图源；只包含地貌、岸线、静态道路和不可点击地标。
- `rt_cluster_marker_mother`：Godot 原生圆章 / 菱形 + 动态数字；不生产固定 `2/3/4/5` 位图。
- 所有文字、数字、ID、本地化、路线、分隔线、focus / hover / selected ring、状态颜色、pressed 位移、loading、tooltip、命中区、anchor、clamp、collision 和 cluster 逻辑都由 Godot 承担。

## 6. 功能与交互复核

E2 的五秒操作链成立：`左卡或地图 pin 选任务 → 三处同步选中 → 阅读右 dossier → 送至签批台`。但进入生产前有以下阻断：

1. `APPROVED` 与“送至签批台”语义冲突，且占用 7–9 行摘要安全区，必须从无字壳删除；真实批准状态只能是运行时状态。
2. 风险红框不能焊进 dossier 或 section plate；普通 / 风险 / 链条 / 禁用由运行时状态层表达。
3. 任务卡与 pin 的状态合同补齐 `assigned / urgent / locked / focus`；cluster 为程序态，不生产固定数字图。
4. dossier 摘要执行 A210：默认完整显示 7–8 行，以 9 行压力验收；默认不滚动，超出后进入独立“展开全文”阅读层。
5. `推进一天` 仍缺玩法命令，只能保持 disabled；不能因已画出按钮壳就宣称功能可用。
6. E2 中所有 pin、短签、任务图标、CTA 勾、沙漏、状态章都只是组合示意，不进入正式底图。

## 7. 首个纵向切片

UI 复核倾向先做 pin，因为它最能暴露小尺寸 alpha、尖轮廓、anchor、状态环和 0–N 避让问题；UX 复核认为事件卡 / dossier 也适合用来验证文字容量和状态。父级取舍为：

1. **先做 `rt_task_pin_shell_mother + rt_task_pin_label_mother`**：只替换一个 selected 事件点；要求 normal / hover / selected / urgent / disabled / focus、0 / 1 / N / 五点密集、标签 clamp 与 cluster 证据。
2. **第二个做 `rt_event_card_mother`**：验证两行最长标题、一行 meta、图标分层和 8 态共用同一轮廓。
3. pin 和事件卡都通过后，才做大尺寸 `rt_dossier_shell`；大壳不应承担首轮试错成本。

## 8. 放行与否

| 动作 | 当前结论 |
| --- | --- |
| 使用 E2 对照色调、材质和默认选中链 | GO |
| 从 E2 裁任意正式组件 | NO-GO |
| 依据 inventory 生成单个 pin / label 无字母版 | GO |
| 一次生成 4 张任务卡或整套状态 atlas | NO-GO |
| 把固定 `APPROVED`、风险红框或 pin 留在生产底图 | NO-GO |
| pin 纵向切片通过后逐类替换运行骨架 | 条件 GO |

批量生产只在以下证据全部存在后放行：原始独立透明图、alpha probe、关键边缘 300% 近照、2x / 3x 缩小对照、真实 Godot 回插截图、最长文案、完整状态矩阵、1920×1080 / 1600×900 / 1366×768 回归，以及相同 class 的几何全等检查。
