# WMW v2.2.3 整屏结构恢复施工基线

> **产物类型**：`screen_structure_target` 的运行装配映射，不是美术资产、runtime pass 或组件合同升版。
> **双参考权限**：`30-v2-2-3-clean-right-function.png` 只定义功能布局、空间职责和信息层级；`575-world-map-wmw-v0-8-6-right-dossier-full-screen-reinsert.png` 只定义组件造型、色彩、材质和整体美术气质。
> **反例**：30 的白色浮雕地图、旧左右组件和外置 CTA 不采用；575 的底票据跨栏、symbol strip、顶部 QA 条和错误父子关系不采用；639-643 为 `invalidated_wrong_host`。

## 1. 结论

保留 B2.12 左卡和 A5.1 右 dossier 的内部 frozen 几何，按 30 的三栏职责重新建立独立 WMW 宿主，并用 575 的造型、色彩、材质与深色低多边形方向映射组件。右栏是当前地区决策区，底部辅助区只属于中央栏；右下 symbol inventory 不进入运行界面。A5.1 内部橄榄 CTA 是右栏唯一跨层动作，A5.1 下方允许留白。

## 2. 1280×720 宿主边界

| 区域 | 宿主矩形 | 职责 |
| --- | --- | --- |
| 左栏 | `[24,16,228,688]` | B2.12 四状态地区卡栈，只负责地区选择与状态 |
| 中央栏 | `[268,16,648,688]` | 全局轻状态、世界地图、动态 pin / 路线 / 选中层、底部辅助区 |
| 右栏 | `[932,16,320,688]` | A5.1 当前地区描述、任务披露、两条只读任务预览、唯一 CTA |
| 栏间隔离 | `16px` | 任何可见模块、投影和命中区都不得跨栏 |
| 中央辅助区最右界 | `x=916` | 票据、日程、状态和投影均不得进入右栏投影 |

建议中央栏内部先按以下宿主 rect 装配，具体 map panel 合同完成后再冻结：

- `top_status_strip = [268,16,648,32]`，低密度全局事实，不使用 CTA 色语法；
- `map_stage = [268,56,648,480]`，底图与动态 pin / 路线 / selected layer 分层；
- `auxiliary_band = [268,552,648,152]`，只接入通过功能审计的全局日程与辅助信息。

## 3. 当前组件映射

- B2.12 继续使用 `left_region_card.json` 0.8.5 的 `204×160` 与四个既有位置，不恢复 meta 小条，不在左卡承载推荐人数、任务数、风险或进入成本。
- A5.1 继续使用 `right_dossier_page` 的 `320×520 @ [932,30]`；右栏责任区仍从 `[932,16]` 开始，因此册页顶部留 14px、底部留 154px。任务情报保持透明摘要 disclosure，展开只显示两条只读任务；内部 `进入地区任务台` CTA 保持唯一显性按钮。
- `selected_region_id` 是唯一选区真源，同时驱动左卡 selected、地图选中 pin、A5.1 payload、披露内容与 CTA 目标。任何组件内示例默认地区不得进入正式宿主。
- 世界地图的美术方向取自 575 的深色低多边形世界轮廓，不采用 30 的白色浮雕地图。正式 `map_panel` 仍必须是干净底板；禁止从 30、575 或其它整屏参考图裁出带 pin / 路线 / 标签的压平地图冒充正式资产。本轮若只具备结构占位层，必须显式标记 `structure_only`。

## 4. 底部与符号处理

- 575 的右下 globe / eye / check / hand 是符号配料库存，不是功能；当前 runtime 全部不挂载。
- 旧 `bottom_receipt_card` 为 `246×138`，第三位置 `[826,558]` 会进入右栏投影。不得原样接回，也不得直接缩放为 208px 来绕过 frozen 字段。
- 后续只有两条合法路线：功能审计后新建 `bottom_aux_ticket_compact` 类并显式立合同；或按真实功能减为一至两项。裁决前 `auxiliary_band` 只预留空间，不以伪控件填空。
- 全局日程若保留，必须位于中央辅助区并降低权重，不与进入地区 CTA 共用橄榄实体按钮或红色行动语法。

## 5. 首张运行图硬门槛

首张正确宿主截图必须同时与 30、575 并排：30 对照结构，575 对照美术。并逐项证明：

1. B2.12 四态卡栈、中央地图、A5.1 三栏同时完整可见；
2. 同一地区在左卡、地图 pin、右册标题和 CTA 目标四端一致；
3. A5.1 展开态只有两条只读任务，橄榄 CTA 是唯一跨层动作；
4. `x>916` 范围内没有底票据、日程、辅助入口或其投影；
5. 右栏下部没有 icon strip、第二 CTA 或为填空增加的装饰控件；
6. 不出现 `GLOBAL CHANNEL`、旧装订索引、旧频道回条和 QA 说明层。
7. 视觉气质来自 575 的深色低多边形地图、橄榄 / 青 / 金 / 灰状态和干净纸质组件，但没有继承其错误宏观结构。

任一项失败即 `screen_identity = fail`，不得继续跑局部组件通过口径。

## 6. 实施顺序

1. 隔离旧 `WeeklyRunGame / GLOBAL CHANNEL` 上的 A5.1 错挂载；
2. 新建独立 WMW assembly host，只先装 B2.12、中央 map stage 占位层和 A5.1；
3. 接通单一 `selected_region_id` 并做四端同步测试；
4. 取得干净 map panel 后替换占位层，pin / 路线 / selected 继续运行时绘制；
5. 底部辅助模块完成逐项功能审计和新合同后再进入宿主；
6. windowed Godot 截取 collapsed / expanded / locked 与结构 QA，最后才允许写整屏通过。

## 7. 本轮落地结果

- 正式世界地图视图已切换到独立 `WeeklyRunWorldMapAssembly.tscn`，旧 `GLOBAL CHANNEL` 宿主只保留未启用的历史回退结构。
- 左栏采用 B2.12 frozen 几何，地区照片按地区固定，避免照片随 selected / warning / locked 状态漂移；照片内容仍为临时构图资产。
- 中央建立 `MapBaseLayer / RouteLayer / SelectedRegionLayer / PinLayer / LabelLayer`，底图标记为 `structure_only`；没有从 30 或 575 裁取压平地图。
- A5.1 保持 frozen `[932,30,320,520]`，只有 `MissionSummaryButton` 与 `PrimaryEnterButton` 两个交互按钮。
- 644-650 覆盖双参考板、collapsed、expanded、locked、几何 QA、GIF 与 integration manifest。
- UX 老哥与 UI Designer 最终均判 `P0=0 / P1=0`；遗留 P2 为折叠符号语义、`2/4` 余项解释、锁定空照片槽识别和右栏留白保护。
- 结论只允许写“整屏宿主结构与状态接线通过”；正式 `map_panel`、最终地区照片与锁定文案仍未完成生产放行。
