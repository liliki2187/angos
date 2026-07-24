# 区域任务 selected 类型色内框 v6 局部实验交付清单

> 状态：`runtime_candidate_pending_user_visual_review`  
> 范围：常驻任务右挂单例；未接入生产，未扩到其他类型 / 左挂，event card 继续冻结

## 用户裁决与本轮目标

用户明确要求按推荐方案做局部实验。推荐方案已从待选转为本轮唯一方向：selected 时，B 闭合八边纸槽由中性纸灰切换为常驻任务橄榄类型色 `#7F8A47`；既有 `3–4px` 橄榄 selected 后纸继续保留。

本轮只验证两个问题：选中强度是否足够，以及内外两层橄榄是否能在 1×真实地图与动效中清楚共存。没有重开 A/B/C，也没有借机修改图标、文字、右端帽、compound 结构或右侧档案布局。

## 资产与实现

- 生图记录：`design/art-direction/region-task-board/2026-07-21-region-task-selected-type-frame-v6-imagegen-prompt.md`
- 源与运行尺寸：`design/art-direction/region-task-board/runtime-preflight-v6-selected-type-frame/`
- 构建脚本：`scripts/art/build_region_task_selected_type_frame_v6.py`
- Godot 局部捕获：`gd_project/tests/capture_region_task_selected_type_frame_v6.gd`
- Godot 夹具：`gd_project/tests/fixtures/region_task_selected_type_frame_v6/`
- 元数据：`design/art-direction/region-task-board/runtime-preflight-v6-selected-type-frame/selected-type-frame-v6.json`

## 运行时分层

- idle：B pin-only；不显示横条。
- hover：B 中性闭合框 compound。
- selected：既有橄榄 selected underlay 在后，类型色闭合框 compound 在前。
- hover → selected：目标 `96ms` ease-out；中性前层 alpha=`1-t`，类型色前层 alpha=`t`，underlay alpha=`t`。GIF 以 20ms 步长量化为 `100ms`，不是新合同。
- selected → hover：约 `80ms` ease-out，执行反向互补淡变。
- 图标、标题、meta 始终固定坐标，不参与缩放或位移。

互补 alpha 的目的不是做两层叠加高亮，而是保证任意过渡帧中两张同几何前层的权重之和为 1，避免框线变粗、双线和残灰。

## 可见证据

1. `docs/screenshots/2026-07-21-region-task-selected-type-frame-v6/01-selected-type-frame-asset-layer-qa-v6.png`  
   验证同一短签在 hover 与 selected 下的资源差异、1×可读性和前后图层职责。
2. `docs/screenshots/2026-07-21-region-task-selected-type-frame-v6/02-godot-three-state-1x-v6.png`  
   验证 Godot 4.6.3 的真实桌面 1920×1080 三态、地图复杂背景、右侧风险等级与建议。
3. `docs/screenshots/2026-07-21-region-task-selected-type-frame-v6/03-hover-selected-type-frame-runtime-v6.gif`  
   验证 idle → hover → selected、指针移出保持、取消 selected 与回收 idle。GIF 以 20ms 源步长编码；目标 `96ms` 的选中反馈在证据中量化为 `100ms`，取消为 `80ms`。

## 合同结果

- default 与 selected 前层 alpha：逐像素一致。
- compound：`278×80`。
- pin：`64×80`。
- hit：`72×80`。
- anchor：`36/76`。
- caption rect：`78,4,200,72`。
- 图标、标题、meta、共享肩、右端帽和三段拉伸规则：不变。
- 生产 `WeeklyRunRegionEventPin.gd`、`WeeklyRunRegionTaskBoardV2.gd`、正式合同与资产 manifest：未修改。

## 当前 Gate

等待用户只判断两点：

1. selected 的强度现在是否足够，不再与 hover 混淆；
2. 内层类型色闭合框与外层 selected 后纸是否形成清楚的一体关系，而不是粘成一块或显得过度描边。

通过后只冻结“B 闭合框 + selected 类型色内框 + 既有外后纸”这一母结构；后续再按既定色表派生另外三类。未通过则只围绕用户指出的问题做一次定向修正。

## 三方复核与父级裁决

- UX：`P0=0 / P1=0 / P2=0 / GO`。hover 中性框与 selected 双通道不看标签也能分辨；类型色没有替代风险语义，右侧风险等级与建议继续承担决策信息。
- UI：`P0=0 / P1=0 / P2=0 / GO`。原生 1×约 2px 主宽稳定，互补交叉淡变无双线、增粗、残影，图标、文字、右帽、共享肩和锚点无回归。
- 美术初审：发现生成框中位色约 `[145,154,65]`，相对 `#7F8A47` 偏亮、偏黄，记为 P1；几何、alpha、纸张、线宽与内外分层通过。
- 美术校色复验：中位色校准为 `[127,138,71]` 后，原 P1 关闭；永久任务局部美术母结构为 GO。美术另保留一个动效合同 P2，建议取消 selected 也统一为 96ms。

父级不把该 P2 判为当前合同缺陷：本轮进入实验前的 UI / UX 推荐一直是 hover → selected 目标 `96ms ease-out`、取消 selected `80ms`；当前 Godot 两向都使用 cubic ease-out，元数据已补齐 easing，GIF 仅把 96ms 量化为 100ms。保留 80ms 的更快取消有利于减少粘滞感，也没有产生视觉残影。该分歧作为后续手感微调项保留，不阻断本轮局部视觉判断。
