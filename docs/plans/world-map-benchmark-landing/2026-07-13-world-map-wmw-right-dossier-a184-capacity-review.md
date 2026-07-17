# WMW `right_dossier_page` A184 容量与信息架构复核

日期：2026-07-13（2026-07-14 完成文字 bbox 证据纠正）
状态：`contract_v0_8_5_raster_bbox_pass_ready_for_clean_sprite_brief`
产物类型：`component_contract / text_capacity_stress / full_screen_reinsert / structure_review / not production art / not atlas / not Godot runtime`

## 1. 本轮范围

本轮只回答一个问题：A184 从左卡下沉的风险原因、推荐人数、可见目标数、解锁缺口、进入代价和主 CTA，能否与 A75 的地区理解正文一起放进现有右侧合同。复核同时发现术语冲突：现行探索规则规定进入区域不消耗天数，只有具体任务的派遣签批才消耗天数，因此本板不再把天数绑在“进入地区”CTA 上，而以“地区任务预计耗时”做容量 fixture，等待用户确认 A184 的“进入代价”究竟指什么。

559-562 预检阶段没有修改 `design/ui-contracts/world-map/`：

- `right_dossier_page` 仍为 v0.8.4，`320x520`；
- `right_action_lane` 仍为 v0.8.4，`284x50 x3`；
- 没有调用 imagegen；
- 没有生产 atlas、Godot 组件或其它 class；
- 559-561 是合同预检板，不是最终美术或运行时截图。

用户随后明确选择方案 B，并登记为 A189。获批后已按提议几何升版合同：

- `right_dossier_page` 升为 v0.8.5，上半部与 `320x520` 外形不动，下半部替换为四个新槽位；
- `right_action_lane` 升为 v0.8.5，旧三实例结构退役，class id 仅保留为底部唯一主 CTA；
- 新增 `right_mission_intel_button` v0.8.5，作为唯一任务情报 / 条件次级入口；
- 563-565 曾作为升版后的正式合同、三状态压力和整屏回填证据，但其文字 QA 框丢弃了字体 bearing，文字位置证据已降级；合同几何本身不受影响。
- 567-569 以实际光栅 alpha 字形 bbox 重出合同板、三状态压力板和整屏回填，替代 563-565；仍不是生产美术、atlas 或 Godot runtime。

## 2. 证据

- 559：`docs/screenshots/2026-06-24-world-map-benchmark-landing/559-world-map-wmw-right-dossier-a184-contract-decision-board.png`
- 560：`docs/screenshots/2026-06-24-world-map-benchmark-landing/560-world-map-wmw-right-dossier-a184-proposed-state-stress.png`
- 561：`docs/screenshots/2026-06-24-world-map-benchmark-landing/561-world-map-wmw-right-dossier-a184-proposed-reinsert.png`
- 562 manifest：`docs/screenshots/2026-06-24-world-map-benchmark-landing/562-world-map-wmw-right-dossier-a184-capacity-manifest.json`
- 生成脚本：`scripts/ui-contracts/wmw/wmw_right_dossier_a184_capacity_review.py`
- 563：`docs/screenshots/2026-06-24-world-map-benchmark-landing/563-world-map-wmw-v0-8-5-right-dossier-b-contract-board.png`
- 564：`docs/screenshots/2026-06-24-world-map-benchmark-landing/564-world-map-wmw-v0-8-5-right-dossier-b-state-stress.png`
- 565：`docs/screenshots/2026-06-24-world-map-benchmark-landing/565-world-map-wmw-v0-8-5-right-dossier-b-reinsert.png`
- 566 manifest（文字 bbox 证据已作废，仅保留审计）：`docs/screenshots/2026-06-24-world-map-benchmark-landing/566-world-map-wmw-v0-8-5-right-dossier-b-contract-manifest.json`
- 567：`docs/screenshots/2026-06-24-world-map-benchmark-landing/567-world-map-wmw-v0-8-5-right-dossier-b-raster-bbox-contract-board.png`
- 568：`docs/screenshots/2026-06-24-world-map-benchmark-landing/568-world-map-wmw-v0-8-5-right-dossier-b-raster-bbox-state-stress.png`
- 569：`docs/screenshots/2026-06-24-world-map-benchmark-landing/569-world-map-wmw-v0-8-5-right-dossier-b-raster-bbox-reinsert.png`
- 570 manifest：`docs/screenshots/2026-06-24-world-map-benchmark-landing/570-world-map-wmw-v0-8-5-right-dossier-b-raster-bbox-manifest.json`
- bbox 独立校验器：`scripts/ui-contracts/validate_text_bbox_evidence.py`
- 纠错 Loop Log：`docs/plans/world-map-benchmark-landing/2026-07-14-world-map-wmw-right-dossier-raster-glyph-bbox-loop-log.md`
- 正式合同脚本：`scripts/ui-contracts/wmw/wmw_v085_right_dossier_b_contract.py`

## 3. 复核结论

### 方案 A：现 frozen 合同内做最小兼容

三条 full-hit lane 从上到下改为：

1. `查看风险 / 解锁说明`；
2. `查看任务情报 · N项`；
3. `进入选定地区` / `暂不可进入`。

这能让主 CTA 回到底部，也能用短 token 装下 A184 的部分信息。559 warning 压力态全部文字未越框，但方案 A 仍没有可见的完整事实区，只能把任务耗时等信息藏进“查看风险 / 条件”详情。

但方案 A 仍失败于 A75：现合同只有 `meta_slot=196x22`，没有连续的地区正文 carrier。把风险、缺口和正文继续塞进行动条，还会把只读信息伪装成按钮。因此 A 只能作为临时兼容，不应进入正式素材生产。

### 方案 B：推荐的合同升版结构

保留现有真实上半部，不移动：

- `export_size=[320,520]`
- `title_slot=[82,42,160,34]`
- `status_stamp=[246,34,58,58]`
- `photo_slot=[22,98,276,176]`

只重构照片下方的真实剩余空间：

| 新槽位 | 提议 rect | 职责 | 交互 |
| --- | --- | --- | --- |
| `region_body` | `[22,288,276,54]` | 两行地区特征 / 本周异变；warning/locked 可把第二行用于风险或阻断原因 | 只读、忽略鼠标 |
| `decision_facts` | `[22,346,276,32]` | 限时、线索、深链、地区任务预计耗时；locked 改为明确缺口 | 只读、忽略鼠标 |
| `mission_intel_button` | `[22,390,276,44]` | `查看任务情报 · N项`；locked 可切换为 `查看解锁条件` | 次级动作 |
| `primary_enter_cta` | `[16,444,284,50]` | `进入选定地区` / `暂不可进入` | 底部唯一主 CTA |

这组 rect 以当前 v0.8.4 的真实 `photo_slot` 下界 `y=274` 为前提。UI Designer 最初给出的 `[18,262,...]` 下半部草案会与现有照片重叠，因此父级没有照抄；在不动上半部的约束下，地区任务预计耗时放入 `decision_facts`，CTA 保持固定动作文案和现有 50px 高度。

方案 B 明确触碰 frozen：替换 `meta_slot` 与 `action_stack`，退役三条同形 `right_action_lane` 实例，新增两个只读 carrier、一个次级按钮和一个底部 CTA。用户已明确批准该变更，A189 和合同 v0.8.5 保留完整授权链；这份授权不延伸到其它 class 或未决运行时语义。

## 4. 三状态压力结果

568 按 1.5 倍运行时尺度重新渲染 default / warning / locked，使用最长地区名、两位数任务数、两位数缺口和最长任务耗时预览：

| 状态 | 结果 | 最小运行时字号 | 关键压力串 |
| --- | --- | ---: | --- |
| default | `8/8 fit` | `18px` | `限时1 · 线索3 · 深链1 · 任务耗时1-2天` |
| warning | `8/8 fit` | `18px` | `北美禁区警戒带`、`查看任务情报 · 12项`、`任务耗时2-3天` |
| locked | `8/8 fit` | `18px` | `声望31/55 · 还差24 · 需档案残页` |

这里的 PASS 来自每组文案实际光栅化后的 alpha `glyph_bbox`：排版、粉色框与 570 manifest 共用同一 bbox，并检查其绝对坐标完整位于 inner rect。它仍只证明脚本代理字体，不证明最终纸面纹理、按钮美术或 Godot 字体已经通过；目标字体接入后必须按相同 gate 重跑。

### 4.1 2026-07-14 文字 bbox 纠正

旧 563-566 用绘制原点加 `width/height` 合成粉色框，忽略 `textbbox` 返回的 left/top bearing；标题、状态和推荐人数分别出现约 8px、6px、5px 的可见错位。旧 `8/8 fit` 只比较宽高，没有证明真实墨迹在绝对位置上位于槽内，因此已撤销。566 保留为审计记录并显式标记无效，后续合同与 brief 只能引用 570。

## 5. 字段唯一归属

| 信息 | 唯一主承载位 |
| --- | --- |
| 当前状态 | `status_stamp` 主行 |
| 推荐人数 | `status_stamp` 副行 |
| 地区理解 / 风险原因 | `region_body` |
| 可见目标数 | `mission_intel_button` 的 `N项`，不得再称“线报N” |
| 限时 / 线索 / 深链 / 地区任务预计耗时 | `decision_facts` |
| locked 解锁缺口 | `region_body` 阻断行 + `decision_facts` 明确数值 |
| 任务预览 | `mission_intel_button` 打开只读 popover，不进入任务选择或派遣 |
| 进入地区 | `primary_enter_cta`，固定底部且唯一最高权重 |

“任务数”与“线报缺口”必须使用不同术语和数据源；旧 364/367 用同一个 `12` 同时表达任务数量和资源缺口，不能继续作为正式 fixture。

## 6. 双评审共识

UX 老哥将现合同判为 P0 承载链断裂、P1 CTA 终点倒置、P1 状态伪装成动作、P1 计数口径串线。核心结论是：旧 `8/8 fit` 只证明旧字段没越框，不能证明 A184/A75 已有承载位；正式结构应只保留任务情报与主 CTA 两个动作。

UI Designer 同样推荐方案 B：只读正文与事实不能继承 full hit rect；次级任务情报与底部主 CTA 必须拆开。其草案中的上半部坐标仅为假设，最终合并严格服从现合同真实 title/stamp/photo 几何。

## 7. 用户裁决与未决语义

用户已明确选择 **B：保持 `320x520` 外框与上半部不动，只升版重构下半部**。该结构裁决与 v0.8.5 几何保持有效。567 的合同断言、568 的实际光栅字形三状态压力与 569 的整屏位置回填已完成；570 记录全部三份合同为 v0.8.5、下半部槽位互相交叠为 0、两个子组件绝对位置与父槽位换算一致，并确认只有任务情报与底部主 CTA 两个交互热区。563-566 的文字位置证据不得再引用。

本次选择没有自动采纳以下语义，继续留在 provisional：

1. locked 地区的次级入口采用 `查看解锁条件`，还是允许 `查看已知任务情报`；当前 560 先演示 `查看解锁条件`。
2. warning 状态点击进入是否需要二次确认；本轮只验证静态层级，未决定交互。
3. A184 的“进入代价”是否正式改名为“地区任务预计耗时”。当前合同 fixture 先用该安全口径；按现行 GDD，点击 `进入选定地区` 本身不扣天数，真正扣天数发生在下游派遣签批。

两行地区正文容量已随方案 B 的几何采纳：约 30-36 个汉字，更长内容进入任务情报 / 地区页，不继续缩字。当前代理字体的 raster bbox 合同 gate 已通过，下一步是为 v0.8.5 新下半部写无字 clean-sprite brief，再做单类纵向切片；当前仍不得直接批量生产，Godot 目标字体仍需独立复核。

## 8. A205 语义追认：容量 fixture 不得进入运行复审图

2026-07-14 用户追问“推荐12”的实际功能后，正式玩法真源确认世界地图只选择地区，具体任务与派遣人数在进入地区后才成立。由此撤销本评审 §5 中“推荐人数由 `status_stamp` 副行承载”的字段归属：地区级推荐人数退役，`status_stamp` 只允许显示一个由正式运行状态推导的地区状态。

568 中的最长地区名、两位数任务数、两位数缺口、最长耗时与 `推荐12` 仍可作为**离线容量压力串**，但只能证明槽位承载能力。它们不得出现在玩家运行截图、Godot 复审图或生产候选 manifest 的 `screenshot_value` 中；运行候选必须从正式 region payload 导出独立 fixture，并以 `visible_field_semantic_necessity` 校验。A1 违反了这条边界，已由 A2 / 604 取代。
