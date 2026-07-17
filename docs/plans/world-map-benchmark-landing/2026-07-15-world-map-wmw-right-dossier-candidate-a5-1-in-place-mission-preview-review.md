# WMW 右 dossier 候选 A5.1 原位任务预览复审

> **版本**：candidate A5.1 / v0.9.6
> **产物类型**：`runtime_state_preview`
> **设计采纳**：A211 原位展开最终裁决
> **状态**：用户已确认 A5.1 组件视觉方向；639–643 因接入旧 `GLOBAL CHANNEL / WeeklyRunGame` 错误宿主而作废，当前 WMW 新整屏尚未接线
> **范围**：撤回 A5 左锚抽屉，在纸面既有信息区原位显示两条只读任务；不改照片、静态美术、主 CTA 或纸面总高，不调用 imagegen，不生产其它 class

## 1. 用户裁决与实现

用户确认采用“摘要行固定、两条任务向上原位展开”的方案。A5.1 因此只改变运行时内容模式：

- collapsed：`region_body` 显示地区描述，摘要行显示 `限时 1 · 线索 2 · 深链 1` 与 `＋`；
- expanded：同一 `region_body inner=[34,292,252,82]` 切成两条 `41px` 只读任务行，摘要行改为 `已显示 2 / 共 4 条` 与 `－`；
- 两条任务显示任务名及一行 `类型 · 耗时N天` meta，不设独立 hit rect、焦点、hover、按钮底色或端部箭头；
- 完整列表继续只由底部橄榄 `进入地区任务台` 进入；照片、摘要行、CTA 和纸面总高在前后状态中不移动。

两份合同升至 `0.8.8`，只登记 provisional 状态内容分配；所有 frozen 矩形保持 A5 数值不变。

## 2. 运行数据

A5.1 使用新的 production-derived fixture，但不重造内容：原三条任务数组与总数 `4` 继续来自 `WeeklyRunContent / WeeklyRunSystems / WeeklyRunState`。fixture 新增展示派生字段，并在 Python 与 Godot 加载阶段反向断言它们必须等于生产任务前两项：

- `51 区外围公路` / `线索 · 耗时2天`；
- `罗斯威尔档案残页` / `线索 · 耗时1天`；
- `已显示 2 / 共 4 条`。

`validate_visible_field_semantics.py` 已通过，运行图不使用压力 fixture 或写死的无来源字段。

## 3. 程序 gate

| gate | 结果 | 依据 |
| --- | --- | --- |
| frozen 几何 | PASS | dossier / disclosure 合同只升行为版本，外部槽与内部四槽数值不变 |
| 原位变更边界 | PASS | collapsed / expanded 在 `region_body + mission_intel_button` 联合区外像素差 `0` |
| 照片稳定 | PASS | photo_slot 前后像素差 `0` |
| 主 CTA 稳定 | PASS | primary_enter_cta 前后像素差 `0` |
| 外部覆盖层 | PASS | `external_overlay_pixels=0`，Godot 不创建 drawer / popover 节点 |
| 任务数量 | PASS | source `3` 条，按冻结的 `preview_limit=2` 精确渲染 `2` 条 |
| 任务交互 | PASS | 两条任务 `hit_rects=0`；整页仍只有摘要 disclosure 与主 CTA 两个交互热区 |
| 文字容量 | PASS | Python 实际 raster alpha bbox `25/25` 全部落在对应槽内；原始报告写入 manifest，并由独立重放器逐条复核通过 |
| 图片比例 | PASS | 继续使用 `552×352 = 69:44`，Godot `KEEP_ASPECT_COVERED`，无拉伸 |
| 生图调用 | PASS | `0`；本轮只改运行时装配 |

## 4. Godot 证据

633 / 634 / 635 由锁定的 Godot `4.6.2-stable`、windowed OpenGL3 生成，未用 headless 截 UI；capture 保留双 `RenderingServer.frame_post_draw` 与全黑帧拒绝。

| 编号 | 内容 | 颜色数 | 非黑像素 | 结论 |
| --- | --- | ---: | ---: | --- |
| 633 | collapsed | 46637 | 2072991 | 描述与摘要正常 |
| 634 | expanded | 46857 | 2072991 | 两条任务原位显示，无卡外层 |
| 635 | expanded QA | 50567 | 2073600 | 同源矩形与任务行证据就绪 |

第二次捕获曾因 QA 标注层把 Variant 字典键直接用于字符串判断而发生 GDScript 类型推断错误；该次没有生成新证据，也没有修改产品节点。修正为显式 `String` 后完整重跑通过。QA 任务区随后去掉重叠标签，只保留青色行框、粉色文字框和独立图例；产品态未改。

## 5. 目检

- **633 collapsed**：PASS。原地区描述、摘要统计、照片和主 CTA 与 A5 collapsed 保持一致。
- **634 expanded**：PASS（父级证据就绪）。两条任务能顺序扫读，没有实体底板、箭头或 hover 暗示；摘要行仍在原位，计数明确说明只展示两条；卡外抽屉完全消失。
- **635 QA**：PASS。两条任务行分别占固定 `41px`；文字槽在行内，青 / 粉证据框不改变产品像素。
- **637 对比板**：A5 被否决的左锚抽屉与 A5.1 两态同板展示，照片、摘要行与橄榄 CTA 的位置保持一致。

## 6. 产物

- 629：collapsed / expanded / QA 三态结构板；
- 630 / 631 / 632：Python collapsed / expanded / QA；
- 633 / 634 / 635：Godot collapsed / expanded / QA；
- 636：collapsed → expanded → collapsed 动态 GIF；
- 637：A5 左抽屉与 A5.1 原位方案对比板；
- 638：delivery manifest。

## 7. 双 agent 复核

- `ui_designer`：**PASS，无阻断项**。原文结论：“meta 明确表达耗时；‘＋/－’准确表达展开与收起。”
- `ux_laoge`：**P0 0 / P1 0 / P2 0，无阻断项**。原文结论：“‘耗时’消除了剩余时间/任务成本歧义；‘＋/－’清楚表达展开与收起，不再存在空间方向误导。”

两项抛光均已进入 633–637 最终证据。双 agent 结论只代表专业复核通过，最终候选是否冻结仍由用户裁决。

## 8. 待用户裁决

历史裁决点为 634 / 636 / 637：两条任务密度、`已显示 2 / 共 4 条` 清晰度，以及任务预览是否像只读情报。用户已于 2026-07-15 确认继续落地，A5.1 因此升为组件接线基线；2026-07-16 进一步明确，这不等于自动选定现成 `WeeklyRunGame` 为整屏宿主，也不等于冻结 locked disclosure 或把北美构图图例升格为正式地区照片。

## 9. 错宿主运行接线（639–643，已作废）

> 2026-07-16 用户纠正：本节截图属于很久以前的旧 `GLOBAL CHANNEL` 页面，不是当前 WMW 新整屏。下列局部测试数据只保留审计价值，不能再用于“正式整屏接线通过”的结论。

A5.1 已作为独立组件挂入正式 `WeeklyRunExplorePhase/WorldDetailPanel`，旧 `WorldDetailVBox` 隐藏；左索引、世界地图、底部回条、地区任务台与派遣流程均未改。`WeeklyRunGame` 生成窄化 dossier view model：地区标题 / 状态 / 描述、未受筛选器影响的生产可见任务、计数与 CTA 共同绑定 `selected_region_id`。

| 编号 | 内容 | 关键结果 |
| --- | --- | --- |
| 639 | 正式整屏 collapsed | 两行地区描述；摘要为 `限时 1 · 线索 2 · 深链 1`；`＋` 与 CTA 正常 |
| 640 | 正式整屏 expanded | 原位两条只读任务；`已显示 2 / 共 4 条`；`－`；照片 / CTA / 纸页不动 |
| 641 | 正式整屏合同 QA | header、photo、两任务行、summary、CTA 全部落在运行时槽位 |
| 642 | 正式折叠 / 展开 GIF | 只改变右栏正文联合区，无抽屉、popover 或任务行点击态 |
| 643 | live integration manifest | 生产绑定、交互数量、锁定态、整帧与局部差分证据 |

新增构造性 gate：

- `WorldDetailPanel` 正式矩形为 `[1480,120,414,843]`，A5.1 纸页居中，旧整屏壳的烘焙右页由宿主 backdrop 完整隔离；
- `TextureRect` 必须先设 `EXPAND_IGNORE_SIZE` 再挂 2x texture；节点最终尺寸断言为 parent `320×520`、photo `276×176`、CTA `284×50`；
- 整页只有 `MissionSummaryButton / PrimaryEnterButton` 两个 Button，任务行 hit rect 为 `0`；
- collapsed → expanded 的真实像素 diff bbox 为 `[1524,591,1850,751]`，`x<1400` 差异为 `0`；
- 三张截图均为 `1920×1080`、alpha `255/255`，四区完整性、颜色多样性和双 `frame_post_draw` 通过；
- 锁定东亚时任务数组为空、摘要 / CTA 均真实 disabled，北美占位图不跨地区复用；
- 资产缺失会显式报错，禁止静默回退旧 dossier；摘要与 CTA 均补可见 focus ring。

## 10. 仍未冻结

- 当前北美图片只证明 `69:44` 规格与构图，不是正式地区身份图；正式地区与内容冻结后逐区专门生图。
- locked disclosure 继续使用保守占位口径 `解锁后可查看`，是否改为显示解锁条件仍待产品裁决。
- 本轮没有生产其它 class，也没有修改 `design/ui-contracts/world-map/` 的 frozen 字段。

## 11. 错误前提下的双 agent 局部终审（已失效）

`ux_laoge` 基于 639 / 640 / 641 与 643 的终审原文：

> **P0：0 / P1：0 / P2：0。问题：无。** 折叠/展开仅原位替换正文区；任务行无热区、不误像按钮；CTA 清楚；641 几何对位正常；643 证明旧壳隐藏、无整屏叠层或区外位移。locked disclosure 与北美照片虽为 provisional，但不阻断当前操作链。总裁决：终审 PASS，可作为正式 WeeklyRunGame 右 dossier 接线基线。

`ui_designer` 在 UX 终审后复核同一批正式运行证据，原文：

> **P0：0 / P1：0 / P2：0。问题：无。** 纸页、照片、摘要、任务双行与 CTA 槽位对齐稳定；折叠/展开密度合理；未见旧层叠加或尺寸错位。总裁决：A5.1 通过最终 UI 终审，可作为当前正式运行版本。

两份 agent prompt 都把“正式 WeeklyRunGame”当成已确认前提，因此只检查了右栏局部，没有检查整屏身份。它们对组件局部的判断仍可参考，但整屏 PASS 结论随 639-643 一并撤回。
