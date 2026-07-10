# 世界地图 WMW 资产化路线状态页

> **用途**：本资产线的唯一进度真源。每轮交付必须更新本页（这是交付定义的一部分，见 `docs/onboarding/assetized-ui-production-chain.md` §9）。新对话 / 新 AI 接手时先读本页，不需要考古全部评审文件。
> **最后更新**：2026-07-10（B2.8 / v0.9.14 已降级为 `visual_fail_exposed_harmonic_inpaint`：状态徽章位置、完整字形和地球 / 照片分源已修正，但用户在 509 明确指出四状态徽章右侧均有纵向涂抹。探针确认旧 badge 足迹经 700 轮 harmonic inpaint 后，右侧有 `399px` 修补像素未被新底盘覆盖而直接暴露。不得冻结、不得批量生产其它 class）

## 一、当前一句话状态

四个主组件类合同（左卡 / 右 dossier / CTA 条 / 底部票据）已锁定为候选并通过脚本校验；v0.9 已交付**合并 clean-sprite brief**。用户已裁决接受 `left_region_card` 候选 B 方向，并认可 B1（v0.9.2）的地区照片素材方向（金字塔 / 天线阵 / 遗迹 / 林间人影），但判定 397/403 合成质量存在明显叠化。B1.1（v0.9.3，406-414）修复双地球、warning 双三角、照片槽上缘越界、饱和绿残留，但用户复审指出四状态右侧边缘仍有竖向接缝 / 暗带 / 源裁片边缘残留，411 已降级为 `composite_cleanliness = fail`。B1.2（v0.9.4，415-425）尝试程序修边，但把右侧壳带擦成透明洞；复核确认为 x390..408、y40..300 卡体轮廓内透明像素 selected 3820、available 3859、warning 3802、locked 3835，421 已降级并新增 `card_body_opacity_probe = fail`。B1.3（v0.9.5，426-435）继续不重生图、不改合同，把 `x390..408` 透明洞补成不透明并跑完几何 QA、atlas、Python 回填、manifest、Godot windowed 单组件截图；但用户复审判定该区域是状态色程序填充带，不是重建壳体纹理，视觉上仍像照片右边多了一条“镶边”。431 已降级为 `art_shell_texture_integrity = fail`、`composite_cleanliness = fail`，并新增 `photo_window_vs_photo_slot_conflict = needs_decision`。

本轮按用户采纳的“配料化拼装：生图管风格，几何靠构造”方向做 B2（v0.9.6，436-446）试点：登记 A167 设计采纳后，脚本从 B 壳提取 frame / plate / globe / badge 材料，从 B1 复用四张地区照片，按 `left_region_card.json` v0.8.2 构造 atlas；中途否决 x408 / x400 照片窗口变体，因为 Godot 真实图显示 photo 层会压住右框并产生外探感；最终 B2 保持照片层在合同 `photo_slot` `[42,48,390,176]` 内，把 x390..408 重建为 B 壳 bitmap 右框唇。442 manifest 记录 `geometry_ratio_1_275`、`photo_layer_contract_slot_mask`、`card_body_opacity_probe`、`chroma_residue_full_frame_all_states`、`right_band_texture_variation`、`godot_windowed_capture` 均 pass；合同 frozen 字段未改、`design/ui-contracts/world-map/` 无 diff。

2026-07-09 用户基于 445 Godot 截图复审 B2，明确指出以第二张“欧洲灰域”为例：照片左上没有贴合地球圆弧，下方露出底板图片，右侧仍有不自然遮挡 / 接缝。这证明 B2 的失败不只是 x390..408 右框问题，而是照片层一开始就缺少真实窗口形状 mask 与独立 frame overlay，矩形 photo 层、地球圆弧、底框和右框之间的遮挡关系没有被正确建模。B2 因此降级为 `visual_fail_shape_mask_and_frame_overlay_missing`；不得继续做坐标级补丁，不得宣称 B2 视觉通过，不得批量生产其它 class。

2026-07-09 用户进一步裁决采用 B2.1（v0.9.7，447-457）三层 z 序结构：底层为普通矩形地区照片，cover 铺满照片窗口外接矩形，不做任何形状 / 圆弧 / mask 裁切；上层为从 B 壳四状态提取的镂空框体，保留框、地球徽章、纸签底板与 action badge，旧夜空照片像素置透明，所有地球圆弧、右缘、下缘和卡体边界都由框体 alpha 定义；运行时继续只放中文 title / meta Label。A168 设计采纳已登记，评审记录为 `docs/plans/world-map-benchmark-landing/2026-07-09-world-map-wmw-left-card-b2-1-hollow-shell-review.md`。455 manifest 记录旧照片签名扫描四状态 0、卡体轮廓内透明像素 0、比例 1.275、禁止照片形状裁切、镂空壳 z-order、200% 圆弧 / 右缘 / 下缘目检与 Godot windowed 截图均通过；456/457 已用正式 windowed opengl3 runner 生成并通过非黑 / 颜色多样性校验。B2.1 当前是纵向切片通过、等待用户观感裁决的候选，不是冻结生产资源。

2026-07-09 按用户最新“WMW 左卡镂空框规程 v1.1”修正 B2.2（v0.9.8）量测方法：脚本 `scripts/ui-contracts/wmw/wmw_v098_left_card_b22_hollow_shell_geometry_pipeline.py` 已改为逐帧自适应样本集，照片样本来自合同槽中心区网格，壳体样本来自顶部框带与底板行；地球圆盘改为 available 全量实测，其它三帧在 available bbox 外扩 12px 范围内局部搜索；GateE 改为宽/高互差 ≤10px、位置互差 ≤10px，并新增 458 overlay 目检闸。458 已生成并目检：红色逐帧实测矩形均落在照片区域，cyan 公共矩形位于照片内，但 GateE 仍失败。实测窗口为 selected `(32,56,370,169)`、available `(38,56,366,184)`、warning `(40,58,371,191)`、locked `(33,57,369,191)`；宽度互差 10px 达标，中心 x 互差 4.5px 达标，但高度互差 21px、中心 y 互差 12px 超标。按 R4/R6，未继续挖窗合成，未生成正式 atlas / Godot 截图 / pass manifest；不得把 B2.2 写成通过。当前需用户裁决：是接受这四帧真实窗口存在纵向差异并指定公共窗口真源，还是继续修订量测 / GateE 定义。

2026-07-09 用户进一步裁决撤销“逐帧窗口真源”，改为 B2.3（v0.9.9，459-468）“一类一母版”：以候选 B 原始 atlas 的 `available` 帧作为唯一母版，按 v1.1 自适应方法实测窗口 `[38,56,366,184]` 与地球圆盘 `center=[57,45], r=26`，纯几何挖窗一次；selected / warning / locked 全部由母版程序派生状态色、原帧 `action_badge` 槽位小图与 selected 绿光晕。照片复用 B1.3 四张地区图，只按母版窗口矩形 cover 铺底，不做任何形状 / 圆弧 / mask 裁切。脚本 `scripts/ui-contracts/wmw/wmw_v099_left_card_b23_single_master_pipeline.py` 已生成 459 派生对比板、465 地球弧 / 右缘 / 下缘 300% 目检板、461 atlas、463/464 Python 回填、466 manifest；Godot capture 已切换到 B2.3 atlas 并用 windowed opengl3 runner 生成 467/468，非黑与颜色多样性校验通过。466 manifest 状态为 `b2_3_single_master_pass_pending_user_review`，GateA 旧图残留、GateB 边框完整、GateC 窗口 alpha、GateD 非 selected 绿残留、GateE 同窗口 diff=0、GateF 1.275 几何比例、300% 目检、派生美术质量和 Godot windowed 截图均为 pass；合同 frozen 字段未改、未调用 imagegen、未批量生产其它 class。B2.3 当前是完整纵向切片通过的候选，等待用户裁决观感是否接受，不是冻结生产资源。

2026-07-09 用户复审 B2.3 后指出 466 manifest 写“300% 目检 pass”但 465 QA 板仍清晰可见三处缺陷，因此 B2.3 降级为 `manual_visual_check_false_pass`：地球下方旧照片淡蓝层被圆盘保护区保留；窗口底边 y184..190 残留旧照片带；badge 从源帧坐标贴完整槽位导致八角环 / 靶心重影。B2.4（v0.9.10，469-478）已按结构修正：窗口矩形整块挖穿，地球徽章提取为独立顶层贴片；新增 `window_edge_residue_scan`，母版窗口从 `[38,56,366,184]` 扩展为 `[37,56,367,192]`，四边旧照片签名最终均为 0；badge 保留母版外环，用奶油色连通块分类区分外环与状态字形，并清除 available 靶心字形及其 3px 抗锯齿 / 阴影残留后贴入 selected / warning / locked 字形。脚本 `scripts/ui-contracts/wmw/wmw_v0910_left_card_b24_layer_fix_pipeline.py` 已生成 469 对比板、475 四状态 × 四检查点 16 点目检板、471 atlas、473/474 Python 回填、476 manifest；Godot capture 已切换到 B2.4 atlas 并用 windowed opengl3 runner 生成 477/478，非黑与颜色多样性校验通过。476 manifest 状态为 `b2_4_overlay_fix_pass_pending_user_review`，GateA-F、`old_content_leftover_scan`、`window_edge_residue_scan`、16 点目检、派生美术质量和 Godot windowed 截图均为 pass；合同 frozen 字段未改、未调用 imagegen、未批量生产其它 class。B2.4 当前是完整纵向切片通过的候选，等待用户裁决观感是否接受，不是冻结生产资源。

2026-07-09 按 B2.5（v0.9.11，479-488）修正 badge 层与派生换色：badge 底盘内芯纳入框色家族换色，新增 `badge_state_color_consistency` 多像素 hue / 明度 gate；状态字形贴换改为奶油色字形的形状 alpha 掩膜并做 1px 收边，矩形裁片带背景直接失败。本轮只动 badge 层与派生换色，地球贴片、边缘扫描、照片层、母版窗口和合同 frozen 字段均不动，未调用 imagegen，未批量生产其它 class。脚本 `scripts/ui-contracts/wmw/wmw_v0911_left_card_b25_badge_fix_pipeline.py` 已生成 479 派生对比板、485 四状态 × 四检查点 16 点证据板、481 atlas、483/484 Python 回填、486 manifest；Godot capture 已切换到 B2.5 atlas 并用 windowed opengl3 runner 生成 487/488，非黑与颜色多样性校验通过。第一次 B2.5 生成中发现 badge 内芯采样范围过小，导致八角 badge 右侧 / 下侧仍有 available 母版青色残片；已将 `badge_core` predicate 扩为整个 action badge 内的非奶油色 / 非语义绿像素后重跑。486 manifest 状态为 `b2_5_badge_fix_evidence_ready_pending_review`：程序 gate 全部通过，16 点目检和派生美术质量仅为 `evidence_ready`，最终视觉 PASS/FAIL 等待复核方 / 用户裁决。

2026-07-09 按 B2.6（v0.9.12，489-498）执行 A172 止损裁决：badge 状态语义图标不再烘焙进 atlas，也不再做源帧字形贴换；母版 badge 底盘一次性清空靶心字形及抗锯齿 / 阴影影响区，干净底盘随状态框色家族换色；勾 / 靶心 / 警示三角 / 锁提取为透明 runtime icon 配料，和中文 title / meta 同属运行时层。脚本 `scripts/ui-contracts/wmw/wmw_v0912_left_card_b26_runtime_badge_pipeline.py` 已生成 489 派生对比板、490 配料纯度 + 400% 证据板、491 atlas、493/494 Python 回填、495 四状态 × 四检查点 16 点证据板、496 manifest；Godot capture 已切换到 B2.6 atlas 与 runtime icon 配料，并用 windowed opengl3 runner 生成 497/498，非黑与颜色多样性校验通过。用户复核 497 后指出 selected 右下 badge 明显多层错乱；拆层探针确认 runtime icon PNG 自身干净，但 atlas clean badge base 中仍保留旧 available 靶心的暗色圆弧 / 阴影 / 内芯残影。B2.6 降级为 `visual_fail_badge_clean_base_semantic_residue`：原 496 程序 gate 只能作为局部机器证据，不得作为视觉通过依据；下一轮必须先新增并满足 `badge_clean_base_no_semantic_residue`，再叠 runtime icon。

2026-07-10 B2.7（v0.9.13，499-508）完成根因复盘与结构重建。探针确认 B2.6 清理器和 `atlas_baked_state_glyph_pixels` 共用同一个奶油色连通组件分类器；旧靶心圆弧与八角环连通后被两边同时误认为“应保留外环”。同时旧 B badge 视觉中心约 `(331,246)`，冻结 `action_badge=[316,212,392,288]` / runtime 中心为 `(354,250)`，即使清干净也天然不同心。本轮脚本 `scripts/ui-contracts/wmw/wmw_v0913_left_card_b27_contract_badge_pipeline.py` 不再做减法清理：以纯几何多边形整区退役旧 badge 足迹，在合同槽内重建外环 bbox `[318,214,390,286]`、中性内芯 bbox `[331,227,377,273]`，四状态从 available 单母版换色；runtime icon 等比收进 42×42 设计盒，Python / Godot 共用 `(354,250)`。脚本先阻塞在 499/500 空底盘证据，确认旧足迹原样像素 0、内芯奶油语义像素 0、中心误差 0.5px 后才生成 501 atlas、502 几何 QA、503/504 Python 回填、505 16 点证据板与 506 manifest。Godot 4.6.2 windowed OpenGL3 已生成 507/508，颜色数 54844 / 54733、非黑像素 2072502 / 2073600；程序 gate 全部 PASS，执行方目检未见旧圆弧 / 双环 / 不同心叠层，但最终视觉结论只写 `evidence_ready_pending_user_visual_review`，等待用户裁决，禁止批量生产其它 class。

2026-07-10 用户复核 507 后进一步指出 B2.7 仍有三项清晰缺陷：状态徽章比候选 B 标杆更贴右框、欧洲灰域靶心字形被截断、左上地球下方仍有旧圆章月牙层。拆层探针确认旧冻结 `action_badge` 把视觉中心推到 1x `(177,125)`，比候选 B 标杆约 `(166,123)` 向右偏 11px；四个 runtime 字形的源 bbox 左边都恰好等于旧合同 `x=316`，进入运行时前已被裁断；照片又从 428 压平 atlas 回采，夹带旧地球下缘。B2.7 因此降级为 `visual_fail_contract_style_mismatch_clipped_source_and_flattened_ingredient`。用户采纳 A174 后执行 B2.8（v0.9.14，509-518）：合同显式升为 0.8.3，仅把 `action_badge` 修订为 `[144,101,44,44]`；B2.8 外环 2x bbox `[290,204,374,288]`、中心约 `(331.65,245.43)`、1x 右视觉留白 `17px`；四个完整字形先从候选 B 宽搜索区提取，再装入 44×44 透明画布，最小 padding 4px、border touch 0；照片从 396 实测纯场景绝对矩形裁取，禁止 428 回流；地球仅保留独立暖色线稿。第一次 510 配料板主动拦下三张照片右侧源框线，改为逐张绝对内容矩形并新增边缘长直框线扫描后才进入正式合成。516 manifest 记录既有程序 gate 全部 PASS；517/518 已由 Godot 4.6.2 windowed OpenGL3 生成且 baseline 缺失采样为 0。随后用户在 509 指出四状态徽章右侧均有程序涂抹；代码与像素探针确认 `harmonic_inpaint()` 把旧足迹 `(284..382,196..295)` 扩散填充，而左移后的新底盘只覆盖其中一部分。在探针区 `x374..382,y196..295`，旧 mask `576px`、新底盘覆盖 `177px`、裸露 inpaint `399px`。B2.8 因此降级为 `visual_fail_exposed_harmonic_inpaint`；原 gate 只能证明旧语义像素消失，不能证明底板纹理连续。禁止继续用 inpaint / 色带补丁，下一轮必须从显式底板与右框配料重建。

本轮复审记录：`docs/plans/world-map-benchmark-landing/2026-07-08-world-map-wmw-left-card-candidate-b1-1-composite-cleanliness-review.md`。  
本轮 Loop Log：`docs/plans/world-map-benchmark-landing/2026-07-08-world-map-wmw-left-card-b1-1-right-edge-loop-log.md`。
B1.2 Loop Log：`docs/plans/world-map-benchmark-landing/2026-07-08-world-map-wmw-left-card-b1-2-frame-break-loop-log.md`。
B1.3 评审记录：`docs/plans/world-map-benchmark-landing/2026-07-08-world-map-wmw-left-card-candidate-b1-3-shell-rebuild-review.md`。
B1.3 Loop Log：`docs/plans/world-map-benchmark-landing/2026-07-08-world-map-wmw-left-card-b1-3-color-band-loop-log.md`。
B2 试点评审：`docs/plans/world-map-benchmark-landing/2026-07-08-world-map-wmw-left-card-b2-constructed-pipeline-trial-review.md`。
B2 Loop Log：`docs/plans/world-map-benchmark-landing/2026-07-08-world-map-wmw-left-card-b2-constructed-pipeline-loop-log.md`。
B2.1 镂空框体评审：`docs/plans/world-map-benchmark-landing/2026-07-09-world-map-wmw-left-card-b2-1-hollow-shell-review.md`。
B2.2 停止点：`scripts/ui-contracts/wmw/wmw_v098_left_card_b22_hollow_shell_geometry_pipeline.py`（v1.1 GateE 失败，458 overlay 已生成，未产出通过 manifest）。
B2.3 单母版评审：`docs/plans/world-map-benchmark-landing/2026-07-09-world-map-wmw-left-card-b2-3-single-master-review.md`。
B2.4 叠层修正评审：`docs/plans/world-map-benchmark-landing/2026-07-09-world-map-wmw-left-card-b2-4-overlay-fix-review.md`。
B2.5 badge 修正评审：`docs/plans/world-map-benchmark-landing/2026-07-09-world-map-wmw-left-card-b2-5-badge-fix-review.md`。
B2.6 运行时 badge 图标层评审：`docs/plans/world-map-benchmark-landing/2026-07-09-world-map-wmw-left-card-b2-6-runtime-badge-review.md`。
B2.6 badge 误判 Loop Log：`docs/plans/world-map-benchmark-landing/2026-07-09-world-map-wmw-left-card-b2-6-runtime-badge-loop-log.md`。
B2.7 合同对齐 badge 复审：`docs/plans/world-map-benchmark-landing/2026-07-10-world-map-wmw-left-card-b2-7-contract-aligned-badge-review.md`。
B2.7 重复拼接问题 Loop Log：`docs/plans/world-map-benchmark-landing/2026-07-10-world-map-wmw-left-card-b2-7-badge-reassembly-loop-log.md`。
B2.8 状态徽章与地球分层复审：`docs/plans/world-map-benchmark-landing/2026-07-10-world-map-wmw-left-card-b2-8-state-badge-and-globe-review.md`。
B2.8 合同 / 风格 / 配料来源 Loop Log：`docs/plans/world-map-benchmark-landing/2026-07-10-world-map-wmw-left-card-b2-8-contract-style-and-ingredient-loop-log.md`。

## 1.1 Godot 截图最小复现结论（2026-07-08）

| 模式 | 结果 | 说明 |
| --- | --- | --- |
| `--headless` + `root.get_texture()` | 失败 | dummy renderer 返回 null；本轮最小复现 headless 分支出现 signal 11，仍按“不可用于 UI 截图”记录，不判环境坏 |
| `--headless` + `SubViewport` | 失败 | 同上，不是 v0.9 / v0.9.2 脚本独有问题 |
| windowed + `--rendering-driver opengl3` | 通过 | 380/381（候选 A）、389/390（候选 B）、403/404（候选 B1）、412/413（候选 B1.1）、445/446（B2 失败证据）、456/457（B2.1）、467/468（B2.3）、477/478（B2.4）、487/488（B2.5）、497/498（B2.6）、507/508（B2.7）、517/518（B2.8）已生成 |
| 错误 Godot 版本（如误选 4.6.3） | 不稳定 | runner 现固定优先 `tools/godot/4.6.2-stable/` |
| 只等 `process_frame` 就取图 | 可能全黑 | 曾出现 389/390 全黑帧；capture 脚本已改为等 `RenderingServer.frame_post_draw` 并拒绝全黑帧 |

复现脚本：`gd_project/tests/godot_capture_minimal_repro.gd`  
推荐 runner：`scripts/run_wmw_godot_capture_v09.ps1`

## 二、路线环状态

| 环 | 阶段 | 状态 | 说明 |
| --- | --- | --- | --- |
| 1 | 风格标杆理解 | 可用 | WMW 标杆方向已认可（低多边形、大块色面、档案纸张、贴纸、深色地图板） |
| 2 | 页面结构 / 职责 | 基本可用 | 左列表 / 中地图 / 右 dossier / 底票据分区已随合同板实际冻结 |
| 3 | 真实内容有字 mock | 按分层路线重定义 | 整屏有字生图多次倾斜失败，已切分层路线；图文融合改由“无字素材 + 运行时回填预览”验证（环 7 之后） |
| 4 | 组件比例分类 | **通过** | v0.8：主组件为长方形家族，方形只属于 icon / sticker / badge |
| 5 | 组件类几何合同 | **四类已锁候选** | 见下方合同清单；剩余三类走轻合同并行补完 |
| 6 | 无字 clean-sprite brief | **初版已完成** | v0.9 合并 brief 已写；四个已锁 class 合并生产要求，轻合同只并行捎带 |
| 7 | 生图 / 素材生产 | **B2.8 视觉失败** | 照片 / 地球 / 字形配料已分源，但旧 badge 足迹仍以 harmonic inpaint 退役，右侧修补纹理裸露 |
| 8 | atlas / manifest | **516 既有 gate 假阴性，需补新 gate** | 511 atlas 与 516 manifest 仅作失败证据；新增 `retired_footprint_texture_continuity` 后必须重跑 |
| 9 | Godot 运行装配 | **B2.8 通过** | capture 脚本与 runner 已切到 B2.8 atlas / runtime icon 配料 / 517 / 518；windowed OpenGL3 跑通，baseline 局部残帧探针为 0，未使用 headless |
| 10 | 多状态截图验收 | **FAIL** | 509 与 515 已清楚显示四状态徽章右侧涂抹；用户复核判定失败 |

## 三、已锁合同清单

合同真源：`design/ui-contracts/world-map/`；校验器：`scripts/ui-contracts/validate_class_contract.py`（2026-07-08 全部 PASS）。

| class_id | 版本 | 关键几何 | 弹性位（provisional） |
| --- | --- | --- | --- |
| `left_region_card` | 0.8.3 | 204x160，四张 y=24/196/368/540，photo_slot 174x64，action_badge 44x44 @ (144,101) | meta_line 纵向分配 |
| `right_dossier_page` | 0.8.4 | 320x520 @ (932,30)，photo_slot 276x176 | title_slot 贴上限、meta_slot 接近上限 |
| `right_action_lane` | 0.8.4 | 284x50 x3（dossier 内），label_plate 170x32 | CTA1 最紧，label plate 必须保持安静底面 |
| `bottom_receipt_card` | 0.8.5 | 246x138，x=288/557/826 y=558 | value_slot 贴上限；抢眼问题调字体层级不改尺寸 |

统一声明：`reference_resolution = 1280x720`，`runtime_resolution = 1920x1080`，`export_scale = 2`（素材按 2x 制作，运行时缩放；禁止 1.5x 位图放大）。压力测试基于脚本字体，最终字体确定后需重跑。

## 四、下一步（按新工作流）

1. **B2.8 已失败，下一轮只重建旧 badge 足迹底板**（主线，不开新合同轮）：
   - 禁止继续使用 harmonic inpaint、模糊、色带或扩大新 badge 覆盖范围遮丑；
   - 从显式底板纹理与右框唇配料构造旧足迹未覆盖区，状态换色后四态同构；
   - 新增 `retired_footprint_texture_continuity`，要求最终暴露修补像素为 0，并单独出 400% 纹理连续性证据；
   - B2.8 修好的位置、完整字形与地球 / 照片分源可以复用；不得批量生产 `right_dossier_page` 等其它 class。
2. **Godot B2.8 截图**（已完成）：
   - 517/518 已生成并通过非黑帧 / 颜色多样性校验，走 `powershell -ExecutionPolicy Bypass -File scripts/run_wmw_godot_capture_v09.ps1 -SkipRepro`；
   - 本轮记录：UI 截图继续禁止 headless；windowed OpenGL3 正式 517/518 通过；
   - capture 脚本继续保留 `RenderingServer.frame_post_draw` 等待与全黑帧拒绝；`.ps1` 执行策略问题用 `powershell -ExecutionPolicy Bypass -File ...` 绕过即可。
3. **剩余轻合同并行补完**（不阻塞左卡裁决，不批量生产）：
   - `393` 已产出合并板：`map_panel` 只定烘焙分界（底图烘什么；pin / 路线 / 选中层全部运行时）；
   - `top_status_strip` 已记录低密度轻合同；
   - `icon_badge` 集已记录清单 + 尺寸网格，atlas 打包前再升为正式合同或图集清单。
4. 素材不服从当前有效合同默认判素材失败；若量测证明合同与已采纳标杆冲突，必须停下交用户裁决，获批后显式升版本并重跑校验器、整屏回填与 Godot 全链，禁止执行方私改。
5. **本资产线收尾时执行 Workflow Lab 首跑 + gate 合并审查**（2026-07-08 挂入，来源：错题本复盘 A165）：
   - 按 harness Level 3 跑一次产物类型判定实验：抽本线 10 张近期图，判定产物类型并核对当时交付声明是否一致；
   - 按 harness §6.1 做第一次 gate 合并审查：合并重复 gate、标注被取代项、收窄过宽触发、退役没拦到问题的 gate，并评估 `check_delivery_manifest.py`（trial）是否转正；
   - 结果更新到错误家族索引（`ai-collaboration-guidance.md` §7.0）的防线层级列。

## 五、禁止跳到

- 未过纵向切片不得批量生产素材；
- 未过素材几何 gate 不得进 atlas / manifest；
- 未有运行截图与目标稿对照不得宣称视觉验收通过；
- 本页未更新不得宣称本轮交付完成。

## 六、历史包袱与版本线说明

- 本文件夹存在两条历史版本线：`v0.9x` 系列（2026-07-02/03 单状态回填与分层实验）与重启的 `v0.x` 系列（2026-07-03 起，资源功能适配 → 正交壳 → 组件修正 → 合同板）。以 `v0.8.x` 系列为当前有效线；`v0.6.8 / v0.6.9` 的 clean-sprite brief 与 class 合同因上游比例分类错误作废，只保留“同 class 状态共享几何”这一条结论。
- 评审引用的生成脚本已从 `tmp/` 升格到 `scripts/ui-contracts/wmw/`；历史评审文档中的 `tmp/` 路径不再保证有效。
- 依据工作区落盘语言规则，后续评审与状态文档一律中文落盘（v0.8.x 系列历史评审为英文，属于违规遗留，不再补翻，但不作为新文档范式）。
