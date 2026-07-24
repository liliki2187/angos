# 区域任务短签单例 compound v4 交付清单

> 状态：`v4b_runtime_candidate_pending_user_visual_review / art_ui_ux_go`  
> 范围：只验证常驻任务右挂的 `idle / hover / selected` 状态链；未接入生产。

## 白话摘要

本轮没有再拿结构示意图代替成品，也没有把旧 pin 和横条硬叠。先用真实生图制作完整 selected compound，再从它定向派生无后衬的 default compound；由于旧生产 pin-only 与 v4 头部不一致，另从 default compound 派生了匹配头部的 idle pin-only。用户复核 v4 后指出 selected 偏弱、pin 内圈若隐若现；v4b 已定向增强 selected 左头美术后纸并删除三态闭合内圈。三态已放入真实 Godot 1×地图，并由 58 张 Godot 实帧生成动图；结构、接合、锚点、文字、时序及状态辨识均通过三方复核，现等待用户最终冻结裁决。

## 本轮产物

- 生图记录：`design/art-direction/region-task-board/2026-07-21-region-task-single-compound-probe-v4-imagegen-prompt.md`
- 色键源：`design/art-direction/region-task-board/runtime-preflight-v4-single-probe/01-permanent-selected-right-compound-source-v4-chroma.png`
- 透明原始源：`design/art-direction/region-task-board/runtime-preflight-v4-single-probe/01-permanent-selected-right-compound-source-v4-alpha.png`
- 3×运行候选：`design/art-direction/region-task-board/runtime-preflight-v4-single-probe/rt-task-compound-permanent-selected-right-v4-3x.png`
- 1×读回：`design/art-direction/region-task-board/runtime-preflight-v4-single-probe/rt-task-compound-permanent-selected-right-v4-1x.png`
- default compound：`design/art-direction/region-task-board/runtime-preflight-v4-single-probe/rt-task-compound-permanent-default-right-v4-3x.png`
- idle pin-only：`design/art-direction/region-task-board/runtime-preflight-v4-single-probe/rt-task-pin-permanent-default-v4-3x.png`
- 技术元数据：`design/art-direction/region-task-board/runtime-preflight-v4-single-probe/single-compound-probe-v4.json`
- Godot 测试夹具：`gd_project/tests/fixtures/region_task_compound_probe_v4/rt-task-compound-permanent-selected-right-v4-3x.png`
- 测试专用捕获：`gd_project/tests/capture_region_task_single_compound_probe_v4.gd`
- 透明 / 接合 QA：`docs/screenshots/2026-07-21-region-task-single-compound-probe-v4/01-transparent-compound-and-joint-v4.png`
- Godot 真实 1×全屏：`docs/screenshots/2026-07-21-region-task-single-compound-probe-v4/02-godot-1x-map-placement-v4.png`
- Godot 真实 1×局部放大：`docs/screenshots/2026-07-21-region-task-single-compound-probe-v4/03-godot-1x-pin-detail-v4.png`
- default / selected 透明对照：`docs/screenshots/2026-07-21-region-task-single-compound-probe-v4/04-default-selected-transparent-qa-v4.png`
- idle / hover / selected 资产板：`docs/screenshots/2026-07-21-region-task-single-compound-probe-v4/05-default-hover-selected-asset-qa-v4.png`
- Godot 真实三态全屏：`docs/screenshots/2026-07-21-region-task-single-compound-probe-v4/06-godot-three-state-1x-v4.png`
- 58 帧 Godot 动图：`docs/screenshots/2026-07-21-region-task-single-compound-probe-v4/07-hover-selected-runtime-demo-v4.gif`
- 状态链测试捕获：`gd_project/tests/capture_region_task_compound_state_chain_v4.gd`

## 拆分与拼接方式

三态使用真实美术资源切换，不由程序绘制绿色底框：idle 使用匹配 v4 头部的 `64×80` pin-only；hover 使用无后衬的 `278×80` default compound；selected 在同位 default 前纸下淡入 selected compound，使其美术后衬显露。现有类型图标、标题和 meta 保持同坐标；状态小签仍预留为独立上层。

中央长度归一采用横向三切片：左侧 pin 头、共享肩和右端类型帽固定，只延展安静无字纸面。1× / 3× alpha 均为单一连通体；针尖中心分别为 `35.5 / 107.5px`，目标锚点为 `36 / 108px`。

## 保持不变的合同

- compound：`278×80`
- pin hit：`72×80`
- anchor：`[36,76]`
- 右 caption rect：`[78,4,200,72]`
- 文字区：`[14,12,158,48]`
- 动态标题：`15px`
- 动态 meta：`12px`
- dense、cluster、clamp 与点击合同：未修改

## 验证

- 透明资源：1× / 3× alpha 连通分量均为 `1`。
- Godot 4.6.3：测试脚本在 OpenGL 兼容窗口模式成功输出 1920×1080 截图。
- 同一轮无头渲染后端两次触发 `signal 11`；未用程序合成图冒充运行截图，改由 4.6.3 可见 OpenGL 后端取得真实证据。
- 右 dossier 的实际截图已显示 `风险等级：低` 和明确的 `建议` 文案。
- Godot 4.6.3：状态链脚本成功输出三态 1920×1080 截图与 58 张原生 1×逐帧；GIF 只做裁切和整数倍放大。
- idle → hover：没有双头、锚点跳位或一帧空白；pin-only 右闭合边由 compound 自然覆盖。
- hover → selected：标签、图标、标题和 meta 不重排；selected 后衬只在前纸外侧出现。
- v4 美术终审：`P0=0 / P1=0 / P2=1 / GO`，认为 selected 后衬达到最低冻结线但不得再减弱。
- v4 UI 终审：`P0=0 / P1=1 / NO-GO for freeze`；真实 1× 下 hover / selected 差异不足。
- v4 UX 终审：`P0=0 / P1=1 / NO-GO`；点击后的任务标记本体缺少即时选中确认，不能依赖鼠标移出后持续显示或远端面板更新来反推。
- v4 父级裁决：compound 视觉母结构继续 GO；完整三态状态链不冻结。该阻断已由下方 v4b 定向修正关闭。

## 仍冻结

- 左挂方向
- 限时 / 连续 / 隐藏三种类型
- 16 帧 atlas
- 生产 `WeeklyRunRegionEventPin.gd`
- 正式 contract / manifest
- event card

## v4 阶段的用户判断（已由 v4b 定向修正关闭）

1. idle → hover 的头部同位、无双头和无跳位是否可以确认通过。
2. 当前 selected 橄榄后衬是否确实太弱，不能与 hover 第一眼区分。
3. 用户已通过指出具体问题并要求继续，授权只把 selected 后衬定向增强到约 `3–4px` 连续露边；compound、文字、端帽、锚点和动画保持不动。

## v4b 定向修正与真实运行结果

用户随后明确指出两个问题：selected 第一眼不够明显；pin 头的闭合黑色内圈在原生 1× 下若隐若现。v4b 没有重开造型，只做两项资源级修正：

1. idle pin-only、hover default compound、selected compound 三态统一删除闭合黑色内圈；不以淡线、粗线、C 形线、角标或程序描边替代。
2. selected 只加强左上、左侧、左下的常驻橄榄后纸，使其在原生 1× 下连续露出约 `3–4px`；接合肩、横条、右端帽保持无背板。

新增产物：

- v4b 色键 / 透明 / 1× / 3×资源：`design/art-direction/region-task-board/runtime-preflight-v4b-single-probe/`
- v4 / v4b 资源 QA：`docs/screenshots/2026-07-21-region-task-state-chain-v4b/01-v4-v4b-selected-and-inner-line-qa.png`
- Godot 真实三态全屏：`docs/screenshots/2026-07-21-region-task-state-chain-v4b/02-godot-three-state-1x-v4b.png`
- 58 帧 Godot 动图：`docs/screenshots/2026-07-21-region-task-state-chain-v4b/03-hover-selected-runtime-demo-v4b.gif`
- 技术元数据：`design/art-direction/region-task-board/runtime-preflight-v4b-single-probe/state-chain-v4b.json`
- 构建脚本：`scripts/art/build_region_task_state_chain_v4b.py`

Godot 4.6.3 可见 OpenGL 运行成功；idle → hover → selected → hover → idle 全程没有双头、残线、空白帧、文字重排、icon / anchor 跳动。美术指导、UI Designer、UX 老哥最终复核均为 `P0=0 / P1=0 / P2=0 / GO`，一致建议冻结当前“常驻任务｜右挂”状态链。父级尚未替用户执行最终冻结；生产实现、正式合同、左挂、其他类型、atlas 与 event card 继续冻结。

## v4b 本次请用户判断

1. selected 的橄榄后纸强度现在是否足够清楚且不过量。
2. 删除闭合黑色内圈后，pin 是否更干净且仍保持完整识别。
3. 若两点确认，是否正式冻结“常驻任务｜右挂｜idle / hover / selected”母状态链并进入下一资产化范围。
