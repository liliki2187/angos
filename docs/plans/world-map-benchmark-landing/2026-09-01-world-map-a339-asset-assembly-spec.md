# 世界地图 A339 资产分层与装配规格

日期：2026-09-01  
阶段：`component_class_contract / implementation_planning`  
视觉参考：[01-filled-state-visual-target-1920x1080.png](../../../image_gen/2026-09-01/world-map-filled-state-legibility-v2/01-filled-state-visual-target-1920x1080.png)  
机器合同：[world_map_page_assembly.json](../../../design/ui-contracts/world-map/world_map_page_assembly.json)

## 1. 本轮交付身份

A339 已允许停止继续追逐生图合成稿里的小字清晰度，转入资产化前规划。当前视觉稿只负责确认方向、材质家族、色彩节拍、内容密度和整屏关系；它不是无字生产母版，也不能被直接切图用于运行时。

本轮只冻结以下内容：

- 1920×1080 三栏页面总几何；
- 已存在组件的职责、层级、输入边界和状态真值；
- 运行时动态文字的字号下限、容量上限和溢出策略；
- 无字美术层、动态内容层、状态层、交互反馈层的装配关系；
- 第一条垂直切片的选择和进入条件。

本轮不做：

- 不生成或裁切生产美术资产；
- 不制作 atlas，不冻结最终 manifest；
- 不进入 Godot，不改 WeeklyRunGame；
- 不从旧 `86:41` 历史壳或整屏视觉参考裁切 RegionCard；RegionCard 依 A305 与 `left_region_card.json v1.0.0` 的 `340×170` 正式合同进入第二条垂直切片；
- 不把 exact rect 未冻结的 ISSUE 票签资产化。

## 2. 页面唯一职责

世界地图页负责回答四个问题：

1. 本周有哪些地区候选；
2. 当前选择的是哪个地区、它是否可进入；
3. 该地区为什么值得调查、已经知道哪些任务线索；
4. 玩家下一步能否进入地区任务台。

它不承担任务详情表、来源档案表、结算、选题会操作或复杂筛选。视觉上可以像夜间编辑部工作台，但功能事实必须由动态文字和状态节点承载，不能藏在烘焙批注里。

## 3. 冻结页面几何

| 区域 | 全局 rect | 职责 | 输入 |
| --- | --- | --- | --- |
| Masthead | `[36,24,1356,106]` | 刊名、WMW 地球章、期号、工作台语境 | 无 |
| RegionIndex | `[36,154,372,640]` | 三个地区候选与状态比较 | 仅三张 RegionCard |
| Schedule | `[36,810,372,246]` | 当前日与选题会阶段说明 | 无，`mouse_filter=IGNORE` |
| MapField | `[432,154,960,902]` | 空间定位、选中地区证据和氛围 | 仅三枚 Beacon |
| Dossier | `[1416,24,468,1032]` | 当前地区稿件详情、任务摘要、主行动 | 仅 Disclosure 与 CTA |

冻结子组件：

- RegionCards：`[52,226] / [52,408] / [52,590]`，统一 `340×170`；
- RegionCard 图片：统一 `138×88`；
- Dossier 图片：`414×264`；
- Disclosure：`[1443,596,414,56]`；
- CTA：`[1443,956,414,76]`。

三张新闻图继续来自 `1104×704 / 69:44` 母图，只允许完整等比缩放，禁止裁切、拉伸和另做缩略图。

## 4. 装配层级

| z | 层 | 所有者 | 可以包含 | 禁止包含 |
| ---: | --- | --- | --- | --- |
| 0 | Backdrop | 美术 | 深夜石板蓝整体底 | 功能文字、输入 |
| 10 | BackDecor | 美术 | 独立夹子、胶带、露边、照片背衬、猫 | hit rect、状态事实、功能正文 |
| 20 | FrontCarrier | UI 资产 | 正交纸壳、文件夹壳、图槽框、功能条 | 烘焙动态文字；超过 0° 倾斜 |
| 30 | CanonicalImages | 内容 | 69:44 母图完整 fit | 裁切、状态换规格 |
| 40 | StateDecor | UI 状态 | selected、locked、warning、expanded 的非文字形态 | 改变组件几何、吞输入 |
| 50 | DynamicText | 运行时 | 所有功能文字、数字、状态词 | 倾斜、被纸纹烘焙 |
| 60 | InteractionFeedback | 运行时 | hover、pressed、focus、blocked 反馈 | 改变 hit rect 或挤动文字 |
| 70 | HitRects | 运行时 | 8 个既有交互节点 | 新增任务行点击区、Schedule 点击区 |

FrontCarrier 是稳定承载面；只有独立 BackDecor 可以轻微倾斜。文字、图片与按钮均保持 0° 正交。

## 5. 八个交互节点

交互节点总数固定为 8：

- 三张 RegionCard；
- 三枚 Map Beacon；
- 一个 Disclosure；
- 一个 CTA。

Schedule、Dossier 纸页本身、两条任务摘要、地图照片和所有装饰都必须 `mouse_filter=IGNORE / focus_mode=NONE`。

三张 RegionCard 的 hit rect 等于整个 `340×170` 卡体。三枚 Beacon 的核心注册框统一 `72×72`，但最终 hit rect、标签框与 wrapper rect 尚需从当前实现测量后冻结，当前合同不得编造坐标。

## 6. 状态真值与原子更新

唯一选择真值为 `selected_region_id`。访问状态、紧急状态和展开状态是独立维度：

- `region_access_state = available | locked`；
- `region_urgency_state = normal | warning`；
- `disclosure_expanded = false | true`。

`selected + locked` 是合法组合。点击锁定地区仍然完成选择和预览；它必须在同一帧原子更新：

- RegionCard；
- Map Beacon；
- Map Label；
- Map Evidence；
- Dossier；
- CTA。

锁定态 CTA 保持原 rect，切换为 `locked_disabled`，不得消失或换位置。Disclosure 展开只切换符号和现有容量区内容，不移动 CTA，也不给任务行新增 hit rect。

## 7. 文字规格与容量

### 7.1 全局字体阶梯

| token | 字号/行高 | 用途 | 规则 |
| --- | ---: | --- | --- |
| `functional_min` | `14/20` | 最小功能说明、地区标签 | 冻结下限，不得再缩 |
| `meta` | `15/22` | 状态、计数、任务元数据 | 低对比但不能低透明度吞字 |
| `body` | `16/26` | Dossier 导语、说明正文 | 默认 2 行 |
| `component_title` | `18/26` | 地区名、任务标题、Schedule 阶段 | 最长内容优先缩写或省略 |
| `news_title` | `22/30` | 新闻标题 | 1 行优先，最多 2 行 |
| `primary_action` | `22/30` | CTA | 唯一主行动 |
| `dossier_title` | `36/44` | 当前地区标题 | 1 行 |

9–12px 只允许用于不承载任何玩法事实的烘焙 microtype。状态、计数、耗时、锁定原因、可进入性和任务类型不得落入该级。

### 7.2 RegionCard

| 槽 | 局部 rect | 默认 | 最大容量 |
| --- | --- | ---: | --- |
| 序号 | `[42,10,34,32]` | `16/22` | 固定 2 位 |
| 地区名 | `[80,8,160,38]` | `18/24` | 默认 9 字；10–12 字可降至 `16/22`；再长省略 |
| 状态 | `[244,10,80,30]` | `15/22` | 5 字 |
| 图片 | `[16,56,138,88]` | — | 69:44 完整 fit |
| 右侧安静区 | `[168,56,156,90]` | — | 不恢复旧 meta 表、坐标、任务数 |

状态不能改变卡体、图片或文字槽几何。锁定卡仍须保持标题、图片和状态可读，不能通过整体降透明度暗示“不可选”。

### 7.3 Schedule

| 内容 | 字号/行高 | 容量 |
| --- | ---: | --- |
| `GLOBAL SCHEDULE / 全局日程` | `14/18` | 1 行 |
| `当前第 1 天` | `24/30` | 1 行 |
| `选题会尚未开始` | `18/26` | 10 字 |
| `当前版本不可操作` | `15/22` | 1 行 |

Schedule 的空白属于层级停顿，不补表格、进度格、重复日期或装饰说明。其内部精确 content/no_text rect 需要最终无字母版出来后测量，本轮只冻结外框和 no-hit 语义。

### 7.4 MapField

- 地区标签：至少 `15/22`；
- 锁定原因：至少 `14/20`；
- 北美照片签：`15/22`；
- 夜班传真时刻：`14/20`；
- 黄色便签为 BackDecor 氛围文字，不覆盖 Beacon、标签或图片安全区；
- 中央证据卡 `207×132 / NO-HIT` 仍为 provisional。

地图标签必须短写，不能用缩小到 10–12px 的方式制造“资料很多”。

### 7.5 Dossier

既有局部槽位继续沿用 `right_dossier_page.json`：

| 槽 | 局部 rect | 字号/行高 | 最大容量 |
| --- | --- | ---: | --- |
| Kicker | `[27,24,414,24]` | `14/20` | 1 行，避开夹子禁入区 |
| 地区标题 | `[27,58,286,76]` | `36/44` | 8 字，1 行 |
| 状态章 | `[325,60,116,42]` | `15/22` | 5 字 |
| 主图 | `[27,150,414,264]` | — | 69:44 完整 fit |
| 新闻标题 | `[27,426,414,40]` | `22/30` | 15 字；超出最多 2 行 |
| 导语 | `[27,472,414,84]` | `16/26` | 2 行，总计约 44 字 |
| Disclosure | `[27,572,414,56]` | `15/22` | 标题 6 字、摘要 18 字符 |
| 任务容量 | `[27,640,414,248]` | 标题 `18/26`；元数据 `15/22` | 最多 2 条只读任务 |
| CTA | `[27,932,414,76]` | `22/30` | 12 字 |

任务标题上限 17 字，元数据上限 24 字。内容超限按以下顺序处理：

1. 编辑缩写；
2. 使用已登记短称；
3. 尾部省略；
4. 只有 RegionCard 10–12 字地区名允许降到 16px。

禁止压缩字距、侵占邻槽、缩到 14px 以下或让美术装饰覆盖文字。

## 8. 无字资产计划

后续每个资产文件只承载一种职责：

| 资产类 | 预期内容 | 是否含文字 | 状态 |
| --- | --- | --- | --- |
| `wmw_backdrop` | 深夜石板蓝底与低频材质 | 否 | 待生成 |
| `region_index_folio` | 左栏蓝色 folio 背板与露边 | 否 | 待生成 |
| `region_card_carrier` | 统一正交暖白纸壳、图框、状态章槽 | 否 | 第二条垂直切片；按 `340×170` 正式合同制作 |
| `schedule_carrier` | 正交日程纸壳 | 否 | 待无字母版后测量 |
| `map_back_decor` | 地图背板、照片背衬、胶带、便签、猫 | 可含纯氛围手写，不含功能事实 | 待生成 |
| `dossier_folio` | 右侧蓝色厚 folio 和露边 | 否 | 第一条垂直切片 |
| `dossier_page_carrier` | 暖白主稿纸、图框、Disclosure/CTA 承载面 | 否 | 第一条垂直切片 |
| `state_decor_set` | selected/locked/warning/expanded 装饰 | 否 | 待状态板 |

无字资产必须来自真实生图/美术流程；程序只负责裁切、缩放、文字排版和 QA，不能程序绘制替代质感资产。

## 9. 第一条垂直切片

首个垂直切片选择 `right_dossier_page`，不是因为它最显眼，而是因为它一次覆盖当前风险最高的合同组合：

- 蓝 folio、暖白纸页和夹子的真实接触；
- 414×264 同源母图完整 fit；
- Kicker 与夹子 no-text 禁入区；
- 标题、导语、状态、Disclosure、两条最大内容任务和 CTA；
- collapsed / expanded / locked_disabled；
- 仅 Disclosure 与 CTA 可点；
- 文字层与美术壳的双通道装配。

通过这条垂直切片后，把同一纸张/文件夹家族扩展到 Schedule 与 RegionCard。Dossier 视觉切片完成后，RegionCard 按 A305 的 `340×170` 冻结合同成为第二条切片；旧 `86:41` 只保留为历史 evidence，不再构成阻断。

## 10. 第一条垂直切片进入条件

全部满足才允许开始生成 Dossier 无字母版：

1. 用户确认本规格中的层级、字体阶梯和 Dossier 优先级；
2. ISSUE 票签继续留在整屏参考层，不进入切片；
3. Dossier `binder_clip_zone=[186,0,96,30]` 与全部动态文字槽完成相交检查；
4. 明确 `selected+locked` 合法，锁定预览文案容量已列入样例；
5. 明确展开态只显示最多两条只读任务，CTA 零移动；
6. 生成资产无烘焙功能文字、无错误字符、无裁切功能区；
7. 运行时字体测试保留为 Godot 隔离装配硬 Gate，不再用生图小字作为清晰度证据。

## 11. 待冻结项

- ISSUE 票签 exact rect；
- 三枚 Beacon 的 hit / wrapper / label 精确 rect；
- Schedule 最终无字纸壳的 content/no_text rect；
- MapField 中心证据卡最终位置和容量；
- Godot 中文字体、字重、fallback 与 glyph bbox。

这些项目在完成前必须显式显示为 `provisional`，不能用“视觉上差不多”代替合同冻结。

## 12. 本阶段 PASS Gate

- 页面五区与冻结 rect 全部录入机器合同；
- 八个交互节点名单唯一，Schedule 和任务行明确 no-hit；
- `selected+locked`、Disclosure 展开与 CTA 同位规则无矛盾；
- FrontCarrier、BackDecor、StateDecor、DynamicText、InteractionFeedback 所有权分离；
- 三张 RegionCard 图槽和 Dossier 图槽统一引用 69:44 母图完整 fit；
- 功能文字下限 14px；Dossier 最大内容容量明确；
- 所有尚未测量项显式标为 provisional；
- 当前视觉稿只标记为 reference，不进入切图链；
- 未创建 atlas、最终 manifest、Godot 场景或 WeeklyRunGame 改动。

