# 发刊编辑界面标杆落地 Delivery Manifest

产物类型：`vertical_slice_proof + runtime_state_preview`（A214 同纸色双版与局部换稿已形成新证据，待用户视觉复核）

## 当前交付范围

| 交付项 | 路径 | 状态 | 用途 |
| --- | --- | --- | --- |
| 当前运行时基线截图 | `docs/screenshots/2026-07-14-weekly-editorial-benchmark-landing/01-editorial-current-runtime.png` | 已完成 | 只验证现状实现与信息缺口，不作为视觉真源 |
| 路由卡 | `docs/plans/weekly-editorial-benchmark-landing/ROUTER-CARD.md` | 已完成 | 约束 risky 工作流和本轮停点 |
| 颜色合同 v1 | `docs/plans/weekly-editorial-benchmark-landing/COLOR-CONTRACT-v1.md` | 基准侧已完成 | `benchmark-board-02.png` 为唯一颜色真值；候选回采待生图后执行 |
| 已填稿风格稿 Brief | `docs/plans/weekly-editorial-benchmark-landing/FILLED-MOCK-BRIEF-v1.md` | 已完成 | 锁定真实中文容量、结构、安全区与生图提示词 |
| 已填稿整屏风格稿 | `image_gen/2026-07-14/20260714-110214_weekly_editorial_filled_style_01.png` | `rejected_by_user` | 只作“功能全显吞噬包装”的偏差案例；严禁作为正向参考、runtime 底图或切图源 |
| 生图 sidecar | `image_gen/2026-07-14/20260714-110214_weekly_editorial_filled_style_01.json` | 已完成 | 保存路由、提示词、参考图角色与警告 |
| 生图 QA | `docs/plans/weekly-editorial-benchmark-landing/IMAGEGEN-QA-v1.md` | 已完成 | 标杆、颜色、几何、文字真实性与升格边界复核 |
| 拒收 Loop Log | `docs/plans/weekly-editorial-benchmark-landing/2026-07-14-weekly-editorial-packaging-text-dominance-loop-log.md` | 已完成 | 记录错误根因、量化反证、撤回项与防复发 Gate |
| UX 二次诊断 | `docs/plans/weekly-editorial-benchmark-landing/UX-REVIEW-v2-REJECTION.md` | 已完成 | 默认信息删减、渐进披露与氛围优先约束 |
| UI 二次校正 | `docs/plans/weekly-editorial-benchmark-landing/UI-REVIEW-v2-REJECTION.md` | 已完成 | 新构图面积预算、色彩物件转译与硬禁项 |
| 氛围优先 Brief v2 | `docs/plans/weekly-editorial-benchmark-landing/FILLED-MOCK-BRIEF-v2-ATMOSPHERE.md` | 已完成 | 依据拒收结论重写默认信息、面积预算与标杆转译 |
| 氛围优先整屏候选 v2 | `image_gen/2026-07-14/20260714-114433_weekly_editorial_atmosphere_v2_01.png` | `rejected_by_user` | 只作“写实漂移 + 功能骨架消失”偏差案例；不得作为 UI 母版或正向参考 |
| v2 生图 sidecar | `image_gen/2026-07-14/20260714-114433_weekly_editorial_atmosphere_v2_01.json` | 已完成 | 记录路由、参考图角色、输出与拒收原因 |
| v2 复发 Loop Log | `docs/plans/weekly-editorial-benchmark-landing/2026-07-14-weekly-editorial-realism-and-function-collapse-loop-log.md` | 已完成 | 升级记录同错误家族复发与下一轮 Hard Gate |
| v2 功能崩塌 UX 诊断 | `docs/plans/weekly-editorial-benchmark-landing/UX-REVIEW-v3-FUNCTION-COLLAPSE.md` | 已完成 | 核对候选、六版位、退换、复核与送印链路 |
| v2 方法纠偏 UI 复核 | `docs/plans/weekly-editorial-benchmark-landing/UI-REVIEW-v3-METHOD-CORRECTION.md` | 已完成 | 区分整屏生图、组件生图与确定性装配职责 |
| 无美术功能骨架 v0.2 | `docs/prototypes/weekly-editorial-functional-skeleton/index.html` | 历史实验 | 曾验证双版总览、单版聚焦与共享状态；已被当前“双版常显”修订取代 |
| 功能骨架说明 | `docs/prototypes/weekly-editorial-functional-skeleton/README.md` | 已完成 | 记录验证边界、演示数据与 GDD / 实现不确定项 |
| v0.1 功能骨架证据 | `docs/screenshots/2026-07-14-weekly-editorial-functional-skeleton/` | 已被 v0.2 替代 | 保留首轮单尺度六槽验证记录，不作为当前交付图 |
| v0.2 功能骨架真实截图 | `docs/screenshots/2026-07-14-weekly-editorial-dual-page-focus-skeleton/01-dual-page-overview-held.png` 等 | 已完成 | 展示双版总览、右页单版聚焦和双页签批确认三态 |
| v0.2 功能骨架动态演示 | `docs/screenshots/2026-07-14-weekly-editorial-dual-page-focus-skeleton/04-dual-page-focus-flow.webp` | 已完成 | 由真实点击后的三态截图组成，验证总览—聚焦—整期确认的状态变化 |
| v0.2 自动交互审计 | `docs/screenshots/2026-07-14-weekly-editorial-dual-page-focus-skeleton/interaction-audit.json` | 已通过 | 验证共享状态、跨页互换、返回总览、双页确认、主头版演示阻断和页面无报错 |
| 组件比例分类 v1 | `docs/plans/weekly-editorial-benchmark-landing/COMPONENT-ASPECT-TAXONOMY-v1.md` | 已锁候选 | 定义 S/A/B/C 资源档位与主要 class 比例 |
| 整页合同板 v1 | `docs/plans/weekly-editorial-benchmark-landing/PAGE-CONTRACT-BOARD-v1.md` | 已锁候选 | 冻结总览、聚焦、书序、持稿条、确认和主副版位几何 |
| 类合同 JSON | `design/ui-contracts/weekly-editorial/`、`design/ui-contracts/weekly-editorial-focus/` | 已通过校验 | 12 份 class contract，目录级几何 / 重叠检查通过 |
| 主头版无文字纸壳 | `gd_project/Assets/ui/angus_packaging/weekly_editorial/assetized/editorial-main-head-slot-base-v1.png` | vertical slice candidate | 真实生图；运行时文字 / 状态 / 操作独立 |
| M330 S 级报道图 | `gd_project/Assets/ui/angus_packaging/weekly_editorial/assetized/editorial-story-m330-last-train-v1.png` | vertical slice candidate | 真实生图；低多边形异常站台报道图 |
| 发刊资产 manifest | `gd_project/Assets/ui/angus_packaging/weekly_editorial/weekly_editorial_asset_manifest.json` | 已接入 | 记录来源、合同、尺寸、安全区、runtime rect 与动态层职责 |
| Godot 双版 / 聚焦运行时 | `gd_project/scenes/gameplay/weekly_run/phases/WeeklyRunEditorialPhase.gd` | 已完成首切片 | 替换开发期三列列表，接入真实交互与确认层 |
| Godot 真实截图与动态 WebP | `docs/screenshots/2026-07-14-weekly-editorial-assetized-vertical-slice/` | 已完成 | 双版总览、聚焦主版、整期确认与真实 0.28s 过渡 |
| Godot 交互审计 | `docs/screenshots/2026-07-14-weekly-editorial-assetized-vertical-slice/interaction-audit.json` | 13/13 通过 | 持稿连续、书序、跨页投放、替换、回总览签批和共享快照 |
| 双版常显 Loop Log | `docs/plans/weekly-editorial-benchmark-landing/2026-07-14-weekly-editorial-persistent-instruction-and-focus-scope-loop-log.md` | 已完成 | 记录常驻教学吞噬主舞台与聚焦范围超前，并把防复发升级为自动审计 |
| 双版常显合同板 v2 | `docs/plans/weekly-editorial-benchmark-landing/PAGE-CONTRACT-BOARD-v2-DUAL-PAGE.md` | 历史合同 | 保留固定持稿条的上一版口径，不再驱动当前实现 |
| 静态刊头合同板 v3 | `docs/plans/weekly-editorial-benchmark-landing/PAGE-CONTRACT-BOARD-v3-MASTHEAD.md` | 历史合同 | 静态刊头继续有效；旧来源 / 目标文本反馈已由 v5 修订 |
| Godot 双版常显运行时 | `gd_project/scenes/gameplay/weekly_run/phases/WeeklyRunEditorialPhase.gd` | 当前实现 | 删除 focus、footer、固定持稿条、全局状态徽记与常驻退回箭头；保留双版、局部换稿、拖拽、复核与确认 |
| 静态刊头真实截图 | `docs/screenshots/2026-07-15-weekly-editorial-masthead/` | 已完成 | 5/6 持稿、6/6 与双版确认三态，附布局与 25 项交互审计 |
| 双版常显交互审计 | `gd_project/tests/test_weekly_editorial_dual_page_assetized.gd` | 25/25 通过 | 自动拒绝固定持稿条与可交互刊头，并覆盖同卡 / Esc 取消、来源 / 目标反馈和跨页替换 |
| 副头版无字钴蓝壳 | `gd_project/Assets/ui/angus_packaging/weekly_editorial/assetized/editorial-secondary-head-slot-base-v1.png` | rejected by user | 真实生图与分层可追溯，但独立钴蓝页色破坏同一期杂志统一感；仅保留偏差证据 |
| A02 副头版报道图 | `gd_project/Assets/ui/angus_packaging/weekly_editorial/assetized/editorial-story-area51-breathing-sign-v1.png` | retained for revision | clean-lowpoly 货车与会呼吸路牌获保留；后续回填到同纸色副头版壳 |
| 副头版生图来源与 sidecar | `image_gen/2026-07-15/20260715-weekly-editorial-secondary-head-shell-v1-original.*`、`20260715-weekly-editorial-area51-story-v1-original.*` | 已完成 | 记录 built-in imagegen 路由、完整 prompt、参考图角色、裁切缩放与 QA |
| 副头版合同板 v4 | `docs/plans/weekly-editorial-benchmark-landing/PAGE-CONTRACT-BOARD-v4-SECONDARY-ASSETIZED.md` | 当前真源 | 冻结分层、rect、fallback、右下动作位和报道图全亮规则 |
| 副头版真实截图与动态 WebP | `docs/screenshots/2026-07-15-weekly-editorial-secondary-head-assetized/` | deviation evidence | 证明当前代码行为；双页面底色和全局替换徽记均被用户否决，不得作为正向交互参考 |
| 副头版 QA 与交互审计 | `asset-qa.json`、`interaction-audit.json` | 35/35 通过 | 标杆直对照、资产尺寸 / hash、合同 rect、fallback 互斥、状态误触与双版冻结 |
| 副头版纸色 / 替换控件 Loop Log | `docs/plans/weekly-editorial-benchmark-landing/2026-07-15-secondary-page-color-and-replace-affordance-loop-log.md` | 已记录 | 解释层级映射与全局动作控件误判，冻结 A214 返工边界与新审计断言 |
| 同纸色副头版无字壳 v2 | `gd_project/Assets/ui/angus_packaging/weekly_editorial/assetized/editorial-secondary-head-slot-base-v2.png` | evidence ready | 真实生图；对齐主头版暖纸材质，沿用副头版几何与安全区 |
| v2 生图原图与 sidecar | `image_gen/2026-07-15/20260715-weekly-editorial-secondary-head-same-paper-v2-original.png`、`docs/screenshots/2026-07-15-weekly-editorial-same-paper-local-replace/secondary-head-v2-imagegen-manifest.json` | 已完成 | 保留原始生成结果、完整 prompt、参考图角色、裁切缩放和旧资产偏差关系 |
| 同纸色 / 局部换稿合同板 v5 | `docs/plans/weekly-editorial-benchmark-landing/PAGE-CONTRACT-BOARD-v5-SAME-PAPER-LOCAL-REPLACE.md` | 当前真源 | 冻结统一纸面、按钮数量状态机、拖拽边线与原子 transfer 结果 |
| 拖拽运行时组件 | `gd_project/scenes/gameplay/weekly_run/components/WeeklyRunEditorialDragButton.gd`、`WeeklyRunEditorialCandidateDropZone.gd` | 已接入 | 候选 / 版位真实拖拽源、版位 / 候选池落点与运行时拖拽预览 |
| A214 真实截图与动态 | `docs/screenshots/2026-07-15-weekly-editorial-same-paper-local-replace/` | evidence ready | 默认同纸色、单槽唯一换稿、拖拽 hover 三态；附 10 帧 animated WebP |
| A214 自动交互审计 | `gd_project/tests/test_weekly_editorial_dual_page_assetized.gd` | 42/42 通过 | 覆盖按钮 `0/1/0/<=1`、候选不重复、替换退稿、移动、原子交换、退回候选、no-op、唯一性与确认冻结 |
| A214 同纸色资产 QA | `docs/screenshots/2026-07-15-weekly-editorial-same-paper-local-replace/asset-qa.json` | 通过 | 暖纸平均色 `DeltaE00 0.504`、`dL 0.0113`；副头版尺寸 `884×684` |

## 本轮通过条件

- 5 秒内能读出“正在排一期周刊、头版是谁、还有一个空版、右侧可以送印”。
- 中央双页周刊是最大主物件，六版位由面积与位置而不是倍率数字区分。
- 报道、版位、后果和 CTA 形成连续视线链。
- 视觉语言直接继承两张 clean-lowpoly-weekly 标杆，不滑向旧档案、旧报纸、摄影噪声、终端霓虹或 SaaS 后台。
- 正式动态文字承载面 0° 正交，不压书脊、纸边、夹子、折角、贴签或图像窗。
- 风格稿即使通过，也只升格为目标图，不升格为生产资产。

## 用户确认后的固定后续

1. 冻结 `class / aspect / role / state / safe zone` 组件分类。
2. 制作整页合同板，确认可裁切大区和不可裁切物件。
3. 只选一个高风险版位类做 vertical slice；通过后再扩全套无字资产。
4. 生成 atlas 与 manifest，绑定 Godot 独立文字层和真实交互状态。
5. 覆盖空态、1/3、5/6、满版、选稿、投放目标、冲突、阻断、确认送印等状态。
6. 提供 1920×1080 等桌面 16:9 真实截图，以及落位、签批、送印节奏的真实 GIF / 视频。

## 当前阻断与不确定项

- GDD 要求 `pre_publish_check`、`required_slots_filled`、公开立场、同题疲劳与硬阻断；当前运行时没有完整可见字段或阻断链。
- 空版是否允许送印及其真实代价尚未由实现字段确认。
- 风格稿可以展示这些信息的目标承载位，但不得声称对应机制已经接通。
- 在用户确认整屏视觉方向前，不进入无字资产批量生成和运行时集成。
- 当前功能骨架采用“主头版缺失硬阻断、副头版或其他空版带风险送印”的临时交互假设；现行 GDD 仍允许头版空缺时尝试发刊。正式落地前必须择一修正文档或实现，不能把骨架演示值当作既定规则。
