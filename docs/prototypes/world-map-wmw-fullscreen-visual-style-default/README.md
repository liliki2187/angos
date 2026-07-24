# WMW v5.1 默认态完整整屏美术风格稿

本目录对应 A242 后的整屏前置 Gate。

- `wmw-fullscreen-default-imagegen-source-v0-1.png`：built-in imagegen 生成的完整无字整屏视觉提案源，只提供整屏色重、材质与低多边形气质，不是几何真源，也不直接交用户裁决。
- `render_wmw_fullscreen_default_style_v0_1.py`：按 v5.1 三栏基础恢复整屏，并应用 A244 左栏共轴修正；当前输出 v0.3。
- `wmw-fullscreen-default-filled-style-v0-1.png` / audit：左栏双 carrier 失败证据，不再是审阅入口。
- `wmw-fullscreen-default-filled-style-v0-2.png` / audit：清除双 carrier 后仍存在左栏外壳不共轴，保留为失败证据。
- `wmw-fullscreen-default-filled-style-v0-3.png`：功能与几何验证稿；日程器与三卡同为 `x=66,w=306`，但按钮 / 纸面仍为程序粗装，不再是美术审阅入口。
- `wmw-fullscreen-default-filled-style-v0-3-audit.json`：几何、文字、占位权限、共轴硬 Gate 与 v0.2 区外回归。
- `wmw-fullscreen-default-filled-style-v0-3-alignment-qa.png`：内部 200% 共轴检查图，不作为用户交付图。

v0.3 的功能、内容与几何复核通过，但用户已否决其美术完成度并指出左栏整体仍偏内缩。下一有效审阅入口必须是按 `2026-07-21-world-map-wmw-fullscreen-art-pass-v0-4-production-brief.md` 生成的完整整屏 art pass。

v0.4 用户裁决：版面没有问题，但美术效果与 benchmark-board-01/02 相去甚远。上一轮 UI / UX 美术 PASS 已撤回；v0.4 只保留为布局、内容、阅读链和美术错译证据，不再是用户审阅入口或视觉基准候选。

当前证据：

- `wmw-fullscreen-default-art-pass-filled-v0-4.png`：1920×1080 布局 / 内容证据与美术偏差案例；状态 `rejected_by_user_art_identity_mismatch_layout_retained`。
- `wmw-fullscreen-default-art-pass-filled-v0-4-audit.json`：几何、44 条文字安全区、左右共轴、路线为 0、组件数量与评审边界审计。
- `wmw-fullscreen-default-art-pass-imagegen-source-v0-4.png`：内置 imagegen 生成的完整无字整屏源，只是技术输入，不是另一张需要用户审阅的图。
- `render_wmw_fullscreen_art_pass_v0_4.py`：从完整 art pass 源恢复精确 1920×1080 几何并后置真实中文；美术表面不由纯色矩形替换。

v0.5 已按 A248 保留 v0.4 的版面与内容容量，完全重建美术身份，并完成 UI Designer 与 UX 老哥双终检：

- `wmw-fullscreen-default-benchmark-art-pass-filled-v0-5.png`：当前三图同屏比较候选；完整 1920×1080 默认态玩家视图，状态 `parent_three_up_benchmark_identity_iterate_pending_user_decision`。功能 / UX Gate 通过，但艺术身份 Gate 已由父级同屏复核重新打开。
- `wmw-fullscreen-default-benchmark-art-pass-filled-v0-5-audit.json`：几何、文字安全区、内容数量、禁路线 / 禁红线章、生成边界和内部双审记录。
- `wmw-fullscreen-default-art-pass-imagegen-source-v0-5.png`：内置 imagegen 生成源，只是技术输入，不单独交用户审阅。
- `render_wmw_fullscreen_benchmark_art_pass_v0_5.py`：使用同一生成源恢复精确 1920×1080 几何、真实中文与运行时语义；不以程序纯色面板替代生成材质。

v0.5 的艺术身份 Gate 已在三图同屏后重新打开并进入 v0.6 返修；它不再是 confirming、完整拆图 / atlas、Godot 接入或正式合同的前置候选。

v0.6 针对 v0.5 三图同屏暴露的四项艺术身份差距完成整屏重建：大字号出版图形、强色块节奏、受控非对称拼贴、统一品牌符号系统。当前证据：

- `wmw-fullscreen-default-benchmark-art-pass-filled-v0-6.png`：当前唯一用户审阅入口；完整 1920×1080 默认态玩家视图，状态 `benchmark_ui_ux_pass_pending_user_art_direction_decision`。
- `wmw-fullscreen-default-benchmark-art-pass-filled-v0-6-audit.json`：几何、43 条文字安全区、内容数量、禁路线 / 禁红线章、生成边界与内部三方终审记录。
- `wmw-fullscreen-default-benchmark-art-pass-imagegen-source-v0-6.png`：内置 imagegen 生成源，只是技术输入，不单独交用户审阅。
- `render_wmw_fullscreen_benchmark_art_pass_v0_6.py`：使用同一生成源恢复精确 1920×1080 几何、真实中文与运行时语义。

父级三图同屏、UI Designer 与 UX 老哥均 `PASS，P0/P1/P2=0`；用户美术裁决仍为 `pending`。用户认可 v0.6 后才进入同源 confirming 和完整拆图 / atlas 流程演示。

## 用户指定整屏配色探索 v0.1

用户随后指定 `wmw-colorway-base-user-selected-v0-1.png` 为唯一版式 / 设计真源，只允许调整配色与既有表面质感，并要求方案差异不能只是细微换色。当前审阅入口为：

- `wmw-colorway-v0-1-comparison-board.png`：3840×2280 的 2×2 完整整屏对照板；四格均包含完整 1920×1080 画面，无裁切。
- `wmw-colorway-01-core-olive-v0-1.png`：A 核心橄榄周刊。
- `wmw-colorway-02-mustard-cobalt-v0-1.png`：B 芥末黄 × 钴蓝周刊。
- `wmw-colorway-03-arctic-teal-v0-1.png`：C 极地青档案。
- `wmw-colorway-04-ink-acid-v0-1.png`：D 黑墨 × 酸绿印刷。
- `wmw-colorway-v0-1-audit.json`：尺寸、边缘相关、语义采样与方案差异数据。
- `compose_wmw_colorway_board_v0_1.py`：只做 imagegen 输出的 1920×1080 归一化、拼版与 QA，不做程序化调色或重绘。

用户复核后指出四套仍然过于严肃、像政治游戏，没有继承 benchmark 在神秘基础上的趣味和丰富。A–D 现统一降级为 `rejected_by_user_serious_political_tone_diagnostic_only`，只证明“配色与质感不能单独改变当前全球异常管控台的体验承诺”，不再等待用户选色，也不作为正式有字稿、confirming、拆件或 atlas 的母本。纠偏见 A256 与 `2026-07-21-world-map-wmw-colorway-serious-political-tone-loop-log.md`。

## 「成年怪新闻周刊」整屏方向 v0.2

A256 纠偏后，使用 built-in imagegen 生成并定向编辑三套完整无字整屏，再由程序只做裁切、1920×1080 归一化、宏观三栏回位和拼版：

- `wmw-adult-weird-weekly-v0-2-comparison-board.png`：当前唯一用户审阅入口；A / B / C 完整整屏对照。
- `wmw-adult-weird-weekly-01-news-frontpage-v0-2.png`：A 怪新闻头版。
- `wmw-adult-weird-weekly-02-editorial-pitch-desk-v0-2.png`：B 编辑部选题桌，UX / UI 共同推荐方向。
- `wmw-adult-weird-weekly-03-world-oddities-special-v0-2.png`：C 世界奇闻特刊。
- `wmw-adult-weird-weekly-v0-2-audit.json`：来源、尺寸、目标区域、裁切框与双审结论。
- `compose_wmw_adult_weird_weekly_v0_2.py`：只负责裁切、归位、拼版与审计，不重绘、不调色、不新增 UI。

三套均无明显裁切拉伸，并已恢复完整日程、四条任务和选中故事连续性。当前状态为 `art_direction_candidates_dual_reviewed_pending_user_choice`：只供用户裁决玩家身份感，尚不是正式整屏母本。共同排序为 `B > C > A`；若用户选择 B，下一轮只在 B 内统一子槽和回填真实文字，不再继续三套整屏互跑。

## A258「A 规格 × C 情绪」三方向 v0.1

用户将资源规格与情绪目标拆开后，built-in imagegen 按同一 A 骨架分别生成三套完整整屏：

- `wmw-a258-v0-1-comparison-board.png`：当前唯一用户审阅入口。
- `wmw-a258-01-light-indigo-sage-v0-1.png`：方案 1，浅靛鼠尾草 · 轻奇闻特刊。
- `wmw-a258-02-warm-coral-frontpage-v0-1.png`：方案 2，暖纸柔珊瑚 · 怪新闻头版。
- `wmw-a258-03-dusk-terracotta-midnight-v0-1.png`：方案 3，暮蓝陶土 · 午夜增刊。
- 三份对应 `*-imagegen.png`：真实生成源。
- `compose_wmw_a258_variants_v0_1.py`：只做 1920×1080 归一化、拼版、hash 和审计。
- `wmw-a258-v0-1-audit.json`：共同资产合同、尺寸、来源与双审结果。

三套均为同一三栏、恰好 8 个规则矩形图片槽、完整日程、四任务和唯一 CTA；无多图拼贴、异形图、标题压图或假文字。当前状态 `dual_reviewed_pending_user_selection`。UX 推荐 `1 > 2 > 3`，UI 推荐 `2 > 1 > 3`；方案 1 / 2 为正式候选，方案 3 为深色边界样本。

## A261 图 1 配色下的材质 / 情绪三方案 v0.1

用户选定 A258 方案 1 的浅靛鼠尾草配色后，built-in imagegen 在同一 A 规格、同一 8 个矩形图位与同一资源容量下生成三张完整整屏：

- `wmw-a259-v0-1-comparison-board.png`：当前唯一用户首屏审阅入口；
- `wmw-a259-01-uncoated-independent-weekly-v0-1.png`：无涂布独立周刊；
- `wmw-a259-02-cloth-spine-special-v0-1.png`：当代布脊专题册；
- `wmw-a259-03-fine-mesh-silkscreen-v0-1.png`：细网丝印增刊；
- 三份对应 `*-imagegen.png`：真实生图源；
- `compose_wmw_a259_material_variants_v0_1.py`：只做尺寸归一化、拼版、hash 与审计；
- `wmw-a259-v0-1-audit.json`：来源、尺寸、共同边界与父级 / UX / UI 复核。

共同排序为 `1 > 2 > 3`。方案 1 是长期生产基线首选；方案 2 / 3 分别作为温暖收藏感和实验丝印感的完整对照。当前状态 `dual_reviewed_pending_user_material_selection`，用户选择前不回填真实中文、不拆件、不制作 atlas、不接 Godot。

## A263 方案 1 真实中文整屏 v0.1

用户已选择方案 1「无涂布独立周刊」。本轮保持其三栏、八个矩形图槽、图片、地图、配色与材料，只从同一生图源取安静纸面补片，回填真实中文和默认 / 日程确认语义：

- `wmw-a263-uncoated-fullscreen-default-v0-1.png`：完整 `1920×1080` 默认态主审图；
- `wmw-a263-uncoated-fullscreen-schedule-confirming-v0-1.png`：完整日程二次确认态；
- `wmw-a263-uncoated-fullscreen-state-pair-v0-1.png`：默认态与确认态完整并排流程板；
- `wmw-a263-uncoated-fullscreen-v0-1-audit.json`：来源、文字安全区、来源差分、双态差分与终审结论；
- `render_wmw_a263_uncoated_fullscreen_text_landing_v0_1.py`：可复现的同源补纸、文字回填、拼版与审计脚本。

默认态和确认态各检查 38 条文字且作者定义的 safe rect 违规为 0；两态差异仅位于日程允许区。但用户在 100% 局部截图中发现第三卡状态签错层、日程状态/动作粘连和右栏章节拥挤，证明这些工程断言不能代表视觉通过。UX 与 UI Designer 已撤回原 `PASS`，当前状态为 `user_visual_review_failed_rework_required`。v0.1 只保留为材料、内容、受控差分和假通过审计证据，不再作为用户主审图；详见 `2026-07-22-world-map-wmw-a263-text-carrier-and-spacing-false-pass-loop-log.md`。

## A263 v0.2 三个局部载体返工

v0.2 只修 v0.1 的三个 P1，不改整页其它部分：

- `wmw-a263-v02-third-card-footer-imagegen.png`：built-in imagegen 生成的无字 footer / 状态签局部素材；完整素材本身存在，但 v0.2 的 source crop / `ImageOps.fit` 映射只保留约 49.4% 状态签，右端帽被裁掉；
- `wmw-a263-v02-schedule-carriers-imagegen.png`：built-in imagegen 生成的日期 / 动作双 carrier 局部素材；
- `wmw-a263-uncoated-fullscreen-default-v0-2.png`：完整默认态主审图；
- `wmw-a263-uncoated-fullscreen-schedule-confirming-v0-2.png`：完整推进确认态；
- `wmw-a263-uncoated-fullscreen-state-pair-v0-2.png`：完整双态流程板；
- `wmw-a263-uncoated-fullscreen-local-qa-v0-2.png`：三个问题区域的 200% QA 板；
- 三张 `qa-*-v0-2.png`：复核者从最终 PNG 独立裁出的 100% 局部；
- `wmw-a263-uncoated-fullscreen-v0-2-audit.json`：owner carrier、语义间距、scope invariant、双态差分与双审结论；
- `render_wmw_a263_uncoated_fullscreen_text_landing_v0_2.py`：可复现装配和审计脚本。

有效结果：日期/动作间距 9px；正文/任务标题 10px；任务标题/首任务 10px；三个批准 ROI 外变化为 0。失效结果：第三卡状态中心误差 `(0,2.5px)` 只相对名义 carrier 成立，不能证明实际签体完整。用户最终整屏复审发现状态签右端帽被裁掉；source crop `1950×220` 经 `ImageOps.fit` 映入 `367×52` 后，有效窗口裁掉 protected tag 右侧 `281.65px`，保留率仅 `49.43%`。UX/UI 已撤回 PASS，当前状态 `user_visual_review_failed_third_card_endcap_crop_rework_required`；v0.2 只保留为失败证据。

## A263 v0.3 第三卡状态签闭合修复

v0.3 只重开第三卡 footer `[49,744,367,52]`，不改日程、右栏、地图、照片、三栏、配色或其它文字：

- `wmw-a263-v03-third-card-footer-imagegen.png`：built-in imagegen 定向编辑的完整无字 ingredient，状态签改为紧凑闭合双端帽；
- `wmw-a263-uncoated-fullscreen-default-v0-3.png`：完整 1920×1080 默认态主审图；
- `wmw-a263-uncoated-fullscreen-schedule-confirming-v0-3.png`：完整推进二次确认态；
- `wmw-a263-uncoated-fullscreen-state-pair-v0-3.png`：默认 / 确认完整流程对照；
- `wmw-a263-uncoated-fullscreen-third-card-mapping-qa-v0-3.png`：完整 ingredient → source crop → 最终 100% / 200% → 端帽 400% 的全流程证据；
- `wmw-a263-uncoated-fullscreen-v0-3-audit.json`：protected-object 映射、真实色域文字中心、v0.2 区外回归和双审结论；
- `render_wmw_a263_uncoated_fullscreen_text_landing_v0_3.py`：v0.3 可复现入口，复用 v0.2 脚本的共享装配逻辑。

source crop `848×120` 与目标 `367×52` 的比例误差 `0.13%`，非均匀缩放误差 `0.127%`；protected 保留率 `100%`，四向 crop loss 全为 `0`，右 / 上 / 下边距 `8.22 / 8.67 / 5.2px`，文字对实际色域中心误差 `(0.49,2.77px)`。v0.3 相对 v0.2 只改变第三卡 footer；UX 与 UI Designer 均 `PASS / P0=0 / P1=0 / P2=0`。当前状态 `dual_reviewed_pending_user_visual_confirmation`。
