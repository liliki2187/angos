# WMW `schedule_gate v0.1` 有色纵切复核

## 结论

`schedule_gate v0.1` 已完成 A240 授权范围内的完整纵向切片：真实 imagegen 材料源、四角色拆片、材质归一化、1368×984 确定性装配、456×328 无字母版、342×246 runtime 回放、局部状态叠加与 7 个最终状态全部产出。UI Designer 与 UX 老哥最终均为 `PASS · P0=0 / P1=0 / P2=1`。

组件技术状态曾达到 `UI/UX PASS`，但用户随后以 A242 指出：孤立小组件无法证明其符合整屏美术标杆，且 WMW 尚无获用户认可的完整正式美术风格稿。本产物自此降级为 `technical_pipeline_evidence_only_not_visual_candidate_a242`。唯一 P2 是日期 carrier 下采样实测高度 49px、目标 48px，符合预先批准的 `≤1px` 容差。

## 历史审阅入口（A242 后撤回）

1. `wmw-schedule-gate-colored-v0-1-full-pipeline-walkthrough-1920x1080.png`
   - 用途：把完整拆图生产链串成 8 个连续阶段。
   - 为什么现在看：本轮已经走到授权范围的 runtime 回填末端，没有停留在材料或母版中间阶段。
   - 用户判断：纸材方向是否符合 WMW；是否理解这是一母多态的组件链；是否允许继续下一单组件。
2. `wmw-schedule-gate-colored-v0-1-runtime-states-review-1920x1080.png`
   - 用途：以真实 342×246、1:1 尺寸比较 7 个最终可见状态。
   - 为什么现在看：几何与材料已由自动审计关闭，当前只剩观感、状态辨识与文案可读性需要人看。
   - 用户判断：危险确认、执行中、禁用是否一眼分开；idle / error / 最后一天 / 0 天是否误读；小尺寸文字是否可读。

上述两张图与 `material-geometry-review` 现在全部属于技术证据，不再要求用户判断 WMW 美术方向，也不解锁下一组件。下一次有效美术裁决必须发生在完整 1920×1080 整屏真实内容风格稿上。

## 生产链

1. built-in imagegen 按两张 clean-low-poly weekly benchmark board 与黑白日程器的“材质角色”生成四块无字材料源。
2. 脚本从源图提取 warm / olive / ivory / ink 四类配料。
3. 配料对照 branch paper token 做角色级归一化；保留 imagegen 的宽面 low-poly 价值块，不做完整 UI 生图。
4. runtime-local 整数坐标乘四，在 1368×984 工作画布确定性装配外纸、日期、动作、图标井和两条信息区。
5. 工作画布 3:1 下采样为唯一 456×328 RGBA 无字母版；外部阴影、文字、数字、图标、锈红和执行青灰均不进入母版。
6. 母版按 0.75 回放为 342×246；同一母版覆盖所有状态。
7. runtime 层仅在动作区叠加 confirming / error 锈红、executing 青灰与 disabled 灰，并回填文案 / glyph。
8. 输出 idle、confirming、executing、runtime unavailable、idle_error、confirming last day、zero days 七态。

## 自动审计

- 母版：真实 `456×328 RGBA`，可见 alpha bbox `[0,0,456,328]`，无额外透明 padding，alpha 为 0 的隐藏 RGB 值为 0。
- 回放：真实 `342×246`；date / action / icon / info carrier 与 runtime 真值差异均 `≤1px`。
- 文案：7×8 共 56 条状态文字全部进入原 safe rect。
- 压力：0 / 1 / 99 / 99+、两位截止日、最长 short title、idle_error 等 20 条最终整行全部通过 bbox。
- 颜色：基础母版中 warning rust 和 executing teal 近色像素均为 0；状态颜色只属于 runtime overlay。
- 分层：全部状态复用同一个 master hash；没有烘焙文字、数字、箭头、叹号、进度符号或勾号。
- 证据：三张板均为真实 1920×1080 PNG；其中两张是用户审阅入口，一张是技术 QA 附录。

完整数值、hash、文字 bbox 与覆盖层参数见 `wmw-schedule-gate-colored-v0-1-audit.json`。

## UI Designer 最终意见

- `PASS，可交 UX；P0=0 / P1=0 / P2=1`。
- imagegen 仅作材料配料、一母多态、runtime-local 几何、现代暖灰纸感、confirming / error 锈红、executing 青灰、disabled 灰与 56+20 条文字审计均通过。
- 完整流水线板覆盖 8 个必要阶段；第 8 阶段缩略图只证明七态齐全，真正的 1:1 判断由状态板承担。
- 唯一 P2 是 date 高度 +1px，仍在批准 Gate 内，不建议为此重出母版。

## UX 老哥最终意见

- `PASS；P0=0 / P1=0 / P2=1`。
- 普通用户可以顺序读出 imagegen 原料、拆片、归一化、工作装配、母版、runtime 回放、状态叠加和七态输出。
- 用户最终只需看流水线板与 1:1 状态板，只判断纸材、状态辨识和小尺寸文案可读性。
- 材料 / 几何板作为技术附录，不再把 alpha、hash 和像素坐标转嫁给用户。
- 静态图明确不证明 committed 180–300ms、executing 全区输入锁或 Esc / 点外 / context change 退出。

## 用户反馈闭环

首轮证据按“材料板 / 状态板”技术类型分组，虽然数据完整，但没有把全流程和用户判断任务讲清楚。用户指出不能只给若干图让其自行反推后，已登记 A241，并新增完整流水线板、逐图用途 / 当前出示原因 / 判断点和证据身份分级。复盘见 `2026-07-21-world-map-wmw-schedule-gate-evidence-context-loop-log.md`。

用户随后进一步指出，即使补齐拆图流程，孤立组件仍无法承担整屏美术判断；当前也不存在获其认可的完整正式 WMW 风格稿。A242 因此把本切片降级为技术管线证据并暂停组件扩产，路线退回整屏 `filled-state visual style mock`。阶段误判复盘见 `2026-07-21-world-map-wmw-component-before-fullscreen-style-loop-log.md`。

## 边界

- 没有修改 Godot、`design/ui-contracts/`、compact A5.1、B2.12、地图或三栏结构。
- 没有生成有色整屏。
- 当前 runtime 仍无独立 `advance_day`；真实构建只能显示 unavailable。
- 静态回填不能替代将来的动态时序与输入行为证据。
- 本轮没有执行 Git stage、commit 或 push。
