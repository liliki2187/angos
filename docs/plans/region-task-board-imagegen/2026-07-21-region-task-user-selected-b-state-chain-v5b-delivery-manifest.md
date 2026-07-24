# 区域任务用户选择 B 三态 v5b 交付清单

> 状态：`runtime_candidate_pending_user_visual_review`  
> 范围：常驻任务右挂的 idle / hover / selected；未接入生产。

## 用户裁决

用户在 A / B / C 图标座中明确选择 B，并指出 A 的方框下半截缺失、只有三边，第一观感像未完成。该裁决覆盖此前美术 / UI / UX 对 A 的推荐；后续不再继续优化 A，也不重新比较三案。

## v5b 实现

- idle：使用带 B 闭合八边纸槽的 `64×80` pin-only。
- hover：使用带同一 B 纸槽的 `278×80` default compound。
- selected：B default compound 保持前层不变，v4b 橄榄 selected underlay 仅从后层淡入。
- runtime kind icon、标题、meta、hit、anchor、caption rect 与状态时序不变。

因此 B 框是三态结构常量，不承担 hover / selected 状态；选中反馈仍只由橄榄后纸承担。

## 产物

- B hover compound 生图色键源：`design/art-direction/region-task-board/runtime-preflight-v5b-selected-icon-seat/01-permanent-default-right-compound-source-v5b-chroma.png`
- selected underlay：`design/art-direction/region-task-board/runtime-preflight-v5b-selected-icon-seat/02-permanent-selected-backing-underlay-source-v5b-chroma.png`
- B idle pin-only：`design/art-direction/region-task-board/runtime-preflight-v5b-selected-icon-seat/03-permanent-default-pin-only-source-v5b-chroma.png`
- 运行尺寸与元数据：`design/art-direction/region-task-board/runtime-preflight-v5b-selected-icon-seat/`
- 构建脚本：`scripts/art/build_region_task_state_chain_v5b.py`
- Godot 夹具：`gd_project/tests/fixtures/region_task_compound_probe_v5b/`
- 资产层 QA：`docs/screenshots/2026-07-21-region-task-state-chain-v5b/01-user-selected-b-three-state-assets-qa.png`
- Godot 真实三态全屏：`docs/screenshots/2026-07-21-region-task-state-chain-v5b/02-godot-three-state-1x-v5b.png`
- 58 帧 Godot 动图：`docs/screenshots/2026-07-21-region-task-state-chain-v5b/03-hover-selected-runtime-demo-v5b.gif`

## 运行验证

- Godot 4.6.3 可见 OpenGL 模式成功输出 `1920×1080` 三态截图和 58 张原生逐帧。
- idle / hover / selected 中 B 框保持相同位置、颜色、比例与闭合拓扑。
- idle → hover 无双头、空白帧或图标跳动。
- hover → selected 只增加橄榄后纸；B 框、图标、标题与 meta 不重排。
- selected 指针移出后持续，取消后正确返回 hover 再收回 idle。
- 生产组件、正式 contract / manifest、其他任务类型、左挂与 event card 均未修改。

## 三方回归复核

- 美术指导：`P0=0 / P1=0 / P2=0 / GO`。闭合框全程连续，无断角、残影、叠框或图标粘连；compound 共享肩与 selected 后纸未被破坏。
- UI Designer：`P0=0 / P1=0 / P2=0 / GO`。原生 1×图标居中、净距充分；三态框线几何一致，标题、meta、锚点、标签宽度和端帽无回归。
- UX 老哥：`P0=0 / P1=0 / P2=1 / GO`。idle / hover / selected、移出保持与取消链均成立；唯一 P2 是闭合内槽初见时可能略像内层按钮，但用户已明确选择完整框，不建议继续削弱。

父级裁决：无新增 P0 / P1，可直接交用户做 v5b 冻结审核；不再重开 A / C。

## 本次请用户判断

1. B 的完整闭合框是否解决了 A“像未完成”的问题。
2. B 在展开横条后是否仍与 compound 读成同一纸件，而不是独立按钮。
3. selected 橄榄后纸是否仍足够清楚，没有被 B 框抢走状态辨识。

## 用户视觉复核：selected 强度 P1 重开

用户确认 B 的完整框方向后，进一步指出当前 selected 仍差一点，并提出“选中后多边形线框也变色”或提供其他方案。此前三态实现和动效回归继续有效，但完整状态链冻结 Gate 重新打开，状态改为 `selected_reinforcement_options_pending_user_choice`。

当前三案：

1. selected 时 B 闭合框从中性纸灰切换为任务类型色，外背保持 `3–4px`；UX、UI、美术一致首推。
2. B 框保持中性，外部类型色后纸扩大到 `5–6px`；轮廓增重风险高。
3. B 框保持中性，框内纸面以类型色低饱和轻染约 `14%`；按钮 / 徽章填充与图标对比风险较高。

下一步只建议验证方案 1 的 permanent `#7F8A47` 单例真图和 Godot `96ms` 状态动图；用户选择前不生成资源。

## 2026-07-21 后续裁决

用户已采用方案 1 做常驻任务局部实验。v5b 继续作为中性 hover、B 几何与既有 selected underlay 的来源，不再是最终 selected 强度候选；后续证据与 Gate 转移到 `2026-07-21-region-task-selected-type-frame-v6-delivery-manifest.md`。
