# 世界地图 WMW 资产化路线状态页

> **用途**：本资产线的唯一进度真源。每轮交付必须更新本页（这是交付定义的一部分，见 `docs/onboarding/assetized-ui-production-chain.md` §9）。新对话 / 新 AI 接手时先读本页，不需要考古全部评审文件。
> **最后更新**：2026-07-24（独立世界地图风格板 v2 的非旅行语义、总体构图、综合色彩和三段阅读链获方向性保留，但组件画法未通过：UFO 贴纸矢量化、站台 / 时钟与无线电塔写实化、底部符号工具栏化、日程器拟物过重。当前状态 `direction_retained_component_render_language_rework_required`；只允许局部组件重画，未改 Godot、runtime、正式合同、atlas、compact A5.1、B2.12 或 GDD。）

## 一、当前一句话状态

2026-07-24 独立风格板旁路线：v2 已解决旅行目的地首读，但尚未通过对象—画法 Gate。下一轮冻结整板构图、综合色盘、中央地图与 `02` 同源落位，只重画新闻图像、UFO 贴纸、符号试条、待核实批注与日程器表面；详见 A273 与对应 Loop Log。

用户已选择方案 1「无涂布独立周刊」，材料方向继续有效。v0.1 与 v0.2 保留为假通过 / 裁切失败证据；当前唯一主审图为 `wmw-a263-uncoated-fullscreen-default-v0-3.png`，流程对照为 `wmw-a263-uncoated-fullscreen-state-pair-v0-3.png`，全流程证据为 `wmw-a263-uncoated-fullscreen-third-card-mapping-qa-v0-3.png`。v0.3 状态 `dual_reviewed_pending_user_visual_confirmation`；不重开三栏、图片、地图或配色，也不代表 runtime 已实现。

五个当前组件合同（左卡 / 右 dossier / 底部主 CTA / 任务情报按钮 / 底部票据）已锁定为候选并通过脚本校验；v0.9 已交付**合并 clean-sprite brief**。用户已裁决接受 `left_region_card` 候选 B 方向，并认可 B1（v0.9.2）的地区照片素材方向（金字塔 / 天线阵 / 遗迹 / 林间人影），但判定 397/403 合成质量存在明显叠化。B1.1（v0.9.3，406-414）修复双地球、warning 双三角、照片槽上缘越界、饱和绿残留，但用户复审指出四状态右侧边缘仍有竖向接缝 / 暗带 / 源裁片边缘残留，411 已降级为 `composite_cleanliness = fail`。B1.2（v0.9.4，415-425）尝试程序修边，但把右侧壳带擦成透明洞；复核确认为 x390..408、y40..300 卡体轮廓内透明像素 selected 3820、available 3859、warning 3802、locked 3835，421 已降级并新增 `card_body_opacity_probe = fail`。B1.3（v0.9.5，426-435）继续不重生图、不改合同，把 `x390..408` 透明洞补成不透明并跑完几何 QA、atlas、Python 回填、manifest、Godot windowed 单组件截图；但用户复审判定该区域是状态色程序填充带，不是重建壳体纹理，视觉上仍像照片右边多了一条“镶边”。431 已降级为 `art_shell_texture_integrity = fail`、`composite_cleanliness = fail`，并新增 `photo_window_vs_photo_slot_conflict = needs_decision`。

2026-07-16（已作废的错宿主接线）曾把 A5.1 接入 `WeeklyRunGame` 的旧 `GLOBAL CHANNEL` 世界地图。局部组件、数据、尺寸与交互断言均通过，但这些证据没有核验整屏身份；用户看到 639 后指出页面已回退到旧界面。639-643 与对应“双终审通过”口径全部撤回，状态改为 `invalidated_wrong_host`。本段只保留事故审计价值，不再代表当前路线进度；详见 `2026-07-16-world-map-wmw-a51-wrong-host-integration-loop-log.md`。

同日二次复核确认第一次纠偏仍选错了参考图类型：575 的用途是验证 v0.8.6 右侧两条功能条同宽、组件尺度与同屏回填，不是整页信息架构。页面结构必须以 v2.2.3 的 30 号图为准：左卡选择、中部地图定位、右栏地区决策三者分区；底部日程和辅助入口不得进入右栏；无明确用途、状态和去向的 icon strip 不得作为运行时功能出现。该裁决登记为 A221，并已扩展 `screen_identity_gate` 的参考图产物类型检查。

用户随后把两张参考图的权限进一步拆开并登记为 A223：30 只回答“东西放在哪里、各自负责什么”，575 只回答“东西长什么样”。因此正确整屏既不能复制 30 的白色浮雕地图、旧左卡 / 文件夹右栏和外置 CTA，也不能继承 575 的底票据跨栏、symbol strip 与 QA 条；左侧继续使用 B2.12，右侧继续使用 A5.1，中央地图只继承 575 的深色低多边形美术方向。首张运行图必须同时与 30、575 并排，分别检查结构和美术映射。

同日已完成正确整屏接线：`WeeklyRunWorldMapAssembly.tscn` 独立承载左 `[24,16,228,688]`、中 `[268,16,648,688]`、右 `[932,16,320,688]` 三个责任区；A5.1 保持 frozen `[932,30,320,520]`。`selected_region_id` 原子驱动左卡、地图 pin、右册与 CTA；locked 状态不泄漏任务，进入地区任务台 0 天。644-650 由 Godot 4.6.2 windowed OpenGL3 生成并通过全黑 / 颜色多样性 / 几何 / 局部 disclosure diff gate。首轮把 A5.1 错放到 y=16 的偏差已在交付前自检发现、写入 Loop Log、恢复 frozen 位置并全量重跑。中央 `map_panel` 仍为 `structure_only`，不得宣称生产地图美术通过。

2026-07-17 用户进一步否决上述截图作为“正确的大致拼接效果”：左侧三张卡后和 A5.1 下方都出现明显断口，中下大框的信息密度也不足以形成底部承重。此前 UI / UX 对“技术留白可接受”的判断只能证明没有伪控件或误操作，不能替代整屏构图闭合。A226 已登记；644–650 自此只保留结构接线审计价值。下一张概念图必须先通过四角闭合 Gate，再讨论正式 `map_panel` 或 runtime 落地。

同日用户继续否决功能密度 v2：左下压缩日程器后仍余 64px，右侧浅袋口后仍余 169px，无框背景只是把空白从组件内部搬到组件外部。A229 已登记，v2 Router / Review / Manifest 已标作废。当前 v3 黑白稿让左栏以完整日程器落底，右栏以 A5.1-H 的既有四任务展开区与固定 CTA 落底；中央大地图和紧凑双回执保留。该稿仍是 `structure_wireframe_ready_pending_user_visual_review`，不是正式合同、运行时或美术资产。

用户随后追问中央两条紧凑回执的用途，并授权尝试删除或重新判断。代码与 GDD 核对确认：红线属于推进日后果和限时任务，深链属于具体任务类型；两者在左下、右侧和中央重复，七格还误导为按日同步推进。A232 已登记，v3 中栏被部分取代。v4 默认态删除双条、地图扩为 924×936；条件态只示意未来真实差量回执。当前运行时没有满足条件的事件模型，因此 default 可作为结构候选，conditional 不能宣称已实现。

2026-07-20 继续复核右侧 A5.1-H 顶部“红线升温”。职责矩阵确认：左卡回答“看哪个地区”，左下日程器回答“当前日 / 剩余天数”，任务情报 `限时 1` 回答“有没有 / 有几条”，具体任务行回答“哪一条 / 第几天截止”；当前状态章只做第三次、最模糊的存在性重复。代码复核另发现 `_build_region_warning_text()` 与地区卡状态把 `run_state.remaining_days` 当限时窗口，而内容真源 `temp_ufo.deadline_day=4`，形成“7 天内处理”与“第 4 天截止”的 P0 时间冲突。用户已采纳 A233 / B：A5.1-H warning 派生态撤下可见章并把标题扩至 `[1521,87,333,51]`，保留 compact A5.1 与 locked / chain 状态能力；正文删除错误 7 天句。B 已升为 v5 默认黑白结构候选；A“最早截止 / 第4天”仅在未来同源 `earliest_deadline_day` 成立时重新评估。任务情报、四任务、CTA、三栏、Godot 与合同不动。

同日继续做 v5 整页基础功能终审。UX 老哥按原始 1920×1080 图、GDD 与代码数据逐项核对，判定三栏、A233 / B 和右侧行动链均保留，但 v5 不能原样冻结：左下“红线 / 深链推进”把只在任务成功后变化的深链伪装成自然日后果，“第 0 天进入结算”也应改为天数归零后进入编辑部；当前 runtime 尚无独立 `advance_day`，结构稿必须标 `TARGET_ONLY`。初始 `reputation=45`，东亚需 `>=55` 或 `roswell_dossier`，故默认卡和 pin 应锁定。任务摘要 / 行标签 / 内容类型需统一真源；地图闭环虚线只是按数组顺序连线，没有 edge 数据；`地区说明只回答为什么去` 属于设计注释。UI Designer 已提供保持全部几何的 v5.1 default / confirming 文案、locked pin、任务四行、路径 mask 与允许差异区。当前下一步是生成两张 v5.1 黑白图和审计后做 UX 回归，不进入有色、runtime 或合同。

同日已完成 v5.1 生成与回归。真实产物为 `black-white-full-map-v5-1-default.png`、`black-white-full-map-v5-1-schedule-confirming.png` 和 `black-white-full-map-v5-1-audit.json`；脚本 `render_full_map_functional_truth_v5_1.py` 可复现。三栏、地图、右栏、任务盒体与 CTA 保持，路线使用精确 path mask 删除；默认 / 确认相对 v5 的允许区外像素均为 0，两态差异只在日程器。UX 老哥回归判定 PASS（TARGET_ONLY），P0=0、P1=0；其 P2 `当前到期：无任务到期` 已压缩为 `当前：无任务到期`，栏目轴名 P2 暂不扩文案。用户随后确认整体没有问题并授权推进，A237 已将两态、`常驻 2 · 限时 1 · 深链 1` 与地区正文第二行冻结为当前整屏黑白布局真源。下一阶段先做资产化 / 有色映射 brief，不直接生成有色整屏，不进入 runtime 或正式合同。

同日继续完成 v5.1 资产化 / 有色映射 bridge。UI Designer 将左卡、日程器、地图、pin、A5.1-H、任务行、照片与 CTA 分为既有资产条件复用、新无字资产、运行时层和禁烘焙四类；父级直接对照两张 clean-low-poly benchmark board、支线规范、纸张与色彩合同。UX 首轮发现日程状态不全、0 天缺口、B2.12 状态 / 照片耦合、锁区 CTA 与审计层隔离等 P1，均已修订；第二轮的 disclosure 内部矛盾按 A211 / A229 统一为 `collapsed_summary / expanded` 等高、单一回调、CTA 不移动，UX 最终确认 PASS。bridge 已冻结为下一阶段输入；第一切片为 `schedule_gate`，但只允许先做派生候选规格和单组件无字资产，不生成有色整屏，不进入 Godot 或正式合同。

2026-07-21 完成 `schedule_gate v0.1` 派生候选规格、可复现黑白合同板和 audit。UI Designer 固定 runtime-local `[36,810,342,246]`、future export `[456,328] @ 0.75` 记录、文字安全区、状态矩阵与最后一天专用文案。UX 首轮 `P1=3/P2=1` 推动拆分 `input_capture_rect=[0,0,342,246]` 与 `activation_hit_rect=[12,74,318,100]`、补 0/1/N 动态摘要及 `idle_error`；第二轮剩余的前缀重复 / 最终整行压力与 `idle_error` hover 缺口也已关闭。最终终审 `P0=0/P1=0/P2=0 PASS`。audit 记录 48 条状态文字和 20 条最终装配压力文案均无 safe-area 违规，default / confirming 与 v5.1 crop exact。当前仅待用户接受候选；接受前不制作无字有色母版，不升正式合同，不接 runtime。

同日用户以 A240 接受上述候选并授权单组件有色纵切。built-in imagegen 只生成 warm / olive / ivory / ink 四块无字材质配料，程序按 runtime×4 坐标完成 1368×984 装配，再输出唯一 456×328 RGBA 母版、342×246 回放与 7 个运行时状态。用户随后指出“只给几张图无法判断”，A241 因此要求每次资产交付展示来源、拆分、装配到最终回填的完整流程，并逐图说明用途、为什么现在看和需要判断什么。本轮已新增完整拆图流水线板，状态板保留 7 态 1:1；材料 / 几何板降为用户无需裁决的技术 QA 附录。UI / UX 最终均 PASS，当前只待用户判断纸材、状态辨识与小尺寸可读性；Godot、正式合同和整屏仍冻结。

用户进一步指出，上述完整拆图仍是孤立小组件，不能回答其与三张 B2.12、中央地图和 A5.1-H 同屏后是否属于美术标杆；当前也不存在一张已获用户认可、同时结合 v5.1 正确结构与 benchmark 视觉基因的完整有色整屏。A242 已把 `schedule_gate` 有色结果降级为技术管线证据，撤回其用户美术裁决与下一组件风格母本身份。组件扩产、atlas 与 Godot 接入暂停；下一张有效美术产物必须是 1920×1080 默认态整屏真实内容风格稿，整屏通过后再以同底图补 confirming 回归。

同日完成默认态整屏 v0.1，但用户复核发现左栏把 imagegen 源中的占位横条 / 状态块与程序真实标题 / 状态 / 日程层再次叠加，形成双 carrier、meta 残影和日程占位残片；此前 UI / UX PASS 撤回，v0.1 只保留为失败证据。v0.2 清除占位叠层后，用户继续发现三卡与日程器外壳不同轴；v0.2 PASS 再次撤回。v0.3 关闭了共轴错误，但用户继续指出其按钮 / 纸面粗糙、左栏整组仍过度内缩。v0.3 现只证明功能 / 几何，不再等待美术采纳；下一张有效视觉产物改为完整 imagegen art pass，左栏候选 `[30,y,348,h]`，中央 / 右栏职责和真实内容不变。

同日完成 v0.4 默认态完整整屏 Art Pass。内置 imagegen 负责卡框、按钮、纸面、切角、阴影与整屏材质，程序只恢复精确 rect、真实照片和真实中文；最终图为 1920×1080，左卡 `[30,36/294/552,348,240]`、日程器 `[30,810,348,246]`、地图 `[426,96,924,936]`、右档案 `[1398,24,480,1032]`。44/44 文字安全区、左栏共轴 / 间距、路线为 0、三 pin / 四任务 / 单 CTA 与红线章删除均通过审计。UI Designer 与 UX 老哥终审均 `PASS，P0/P1/P2=0`；当前状态为 `ui_ux_pass_pending_user_art_direction_decision`，只提交一张完整玩家视图，不展示技术源图。用户采纳前不生成 confirming、atlas、拆件，不改 Godot 或正式合同。

用户随后完成裁决：版面没有问题，但美术效果与两张 benchmark 相去甚远。上述 UI / UX PASS 只覆盖功能可读、几何与拼装卫生，被错误扩大为美术身份通过，现已撤回；两 agent 修订为 `FAIL，P0=1，P1=4`。v0.4 状态改为 `rejected_by_user_art_identity_mismatch_layout_retained`。根因是制作 brief 把 benchmark 降为第三顺位 visual DNA，并在 hard negatives 中连同假功能一起删除了编辑拼贴、品牌图形、层叠纸件和附着物，最后只剩深蓝 / 米纸 / 橄榄 / 低多边形的灰暗策略 HUD。A248 已登记；下一轮保留全部版面 rect，不从旧 Prompt 微调，先以 benchmark 为艺术第一真值建立五秒同族 Gate。

同日完成 v0.5 默认态 benchmark Art Pass。内置 imagegen 以两张 benchmark 为艺术身份第一真值、v0.4 仅作 geometry / content mask，重建裁切卡纸、装裱照片、强刊头、globe seal、编辑夹具、橄榄 / teal / slate 色块与整屏纸件层次；程序仅恢复精确 rect、真实中文和运行时语义。终检中四条任务状态由凸起牌体改为平面只读文字，删除日程伪复选框与任务标题滑块式圆点，并下移“全局日程”。43/43 文字安全区、左栏共轴和 18px 间距、路线 0、三 pin / 四任务 / 单 CTA、红线章删除及无程序平面覆盖均通过；两次复渲染 SHA-256 一致。UI Designer 与 UX 老哥原终审均 `PASS，P0/P1/P2=0`。随后三图同屏复核发现艺术身份仍有关键差距：大字号出版图形、强色块节奏、非对称拼贴与品牌符号能量不足；父级把艺术身份 Gate 修订为 `ITERATE，P0=1`，UX 功能 / 交互 PASS 继续有效，用户美术裁决仍为 `pending`。

同日完成 v0.6 默认态 benchmark Art Pass。两张 benchmark 继续作为艺术身份真值，v0.5 只提供固定 rect、功能层级与文字安全区。内置 imagegen 把大刊头、北美 olive、日程动作带、右任务头、CTA、受控跨层纸件和四个统一品牌节点提升为整屏构图骨架；程序恢复真实中文和精确内容。首轮装配中的放大地图背景、绿色补片残影、任务占位线叠字和北美 pin 重影已在交付前清除。UI Designer 初审 `ITERATE，P1=2` 后关闭锁卡环球超量与右档案叠页，最终 `PASS，P0/P1/P2=0`；UX 终审同样全 0 PASS。v0.6 当前为唯一用户审阅入口；用户接受前仍不生成 confirming、atlas、拆件或 runtime 接入。

用户随后把 `wmw-colorway-base-user-selected-v0-1.png` 指定为本轮唯一版式 / 设计真源，要求只改配色与质感，并且方案差异不能只是细微换色。A254 已登记。UX 老哥先锁定地图 / 右档案 / CTA / locked / deadline 的共同语义，UI Designer 再给出 A 核心橄榄、B 芥末黄 × 钴蓝、C 极地青、D 黑墨 × 酸绿四套合同。built-in imagegen 逐套生成，B 定向恢复第三任务左右两处危险色，D 定向强化灰白 / 近黑 / chartreuse 对比；程序只把模型原生 `1672×941` 归一化为 `1920×1080` 并制作 2×2 完整整屏板。全局边缘最佳位移均为 `[0,0]`，六个语义采样区两两 RGB RMS 距离均不低于 `21.80`。当前只待用户选择色系；正式有字稿、confirming、拆件、atlas、Godot 与合同继续冻结。

用户对四套完成复核后否决“继续选色”这条路径：四套虽然在色彩上足够不同，但都继续读成严肃的政治 / 国安游戏，缺少 benchmark 中神秘、丰富、带成年冷面趣味的邀请感。A256 与专项 Loop Log 已登记。UX 将正确情绪链定义为 `异样 → 好奇 → 比较故事 → 选择追查`，而非 `警报 → 风险判断 → 处置`；UI Designer 进一步确认，下一轮必须在保留功能布局的同时解冻照片异常主体、每区故事差异、地图的选题世界解释、组件物件隐喻、出版图形和内部拼贴节奏。A–D 统一降级为诊断证据，本轮停止继续生图。

同日用户确认三栏大模块组合可以保留，但指出上一张概念图仍然在功能、位置和尺寸上明显错误，并明确要求左下日期组件承担“推进到下一天”。A227 已登记并修订 A226 的“只读周程”：进入地区任务台仍是当前选区唯一主 CTA 且进入不耗天；推进日是独立全局危险动作，首次点击只进入确认态并预览剩余天数、红线截止与到期任务变化。父级对照 A99 / A110 后确认这是既有已采纳规则被上一轮漏读，不是本轮临时新增。黑白结构稿与审计文件位于 `docs/prototypes/world-map-wmw-black-white-structure/`；当前运行代码没有独立推进日命令，故本轮只交付目标交互结构与 `filled_state_text_mock`，不声称 runtime 功能落地。

用户随后对 A227 结构稿生成结果继续做密度纠偏：整体大致正确，但两张世界回执只是标题、短状态与七日刻度，不应各占 369×207 大纸；A5.1 主 CTA 下方零信息、零命中的 231px 档案尾也不应读成第二功能区。A228 已登记。新版 structure wireframe 保留三栏、B2.12、A5.1、地图、推进日日程器与双回执语义，新增 450×90 `bottom_receipt_strip` 候选，把地图扩至 924×822；A5.1 下只留 480×62 浅袋口，其后为无框背景。旧 frozen `bottom_receipt_card v0.8.5` 未拉扁，正式新类合同与 runtime 均未创建。

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

2026-07-10 B2.9（v0.9.15，519-528）按 A176 修复 B2.8 的可见涂抹，不再退役 / 重建整个徽章。实测候选 B approved 外环 bbox `[288,201,376,291]`、中心 `(332,246)`、1x 右视觉留白 `16px`；脚本 `scripts/ui-contracts/wmw/wmw_v0915_left_card_b29_no_inpaint_badge_pipeline.py` 仅替换与外环像素交集为 `0` 的语义内芯 `CORE_MASK=[302,216,362,277]`，状态换色也只进入内芯。管线不调用 harmonic inpaint、模糊、扩散或色带；`retired_footprint_texture_continuity` 记录 approved 外环保留 `1983/1983px`、内芯外变化 `0px`、右侧走廊变化 `0px`、外露修补像素 `0px`。519/520 配料依赖板先通过目检后才生成 521 atlas、522 几何 QA、523/524 Python 回填、525 16 点证据板与 526 manifest；526 JSON 解析和 `check_delivery_manifest.py` 均 PASS。527/528 由锁定的 Godot 4.6.2 windowed OpenGL3 生成，未用 headless，QA 相对 normal 的 baseline 缺失采样为 `0`。随后用户复核 519 发现新建内芯的低多边形 X 形分界明显歪斜；代码确认 `neutral_core_texture()` 的 top / right / bottom / left 四块色面没有使用镜像矩形四边，而是错用了八角轮廓上的不成对锚点。B2.9 因此降级为 `visual_fail_badge_core_facet_asymmetry`；无涂抹局部 gate 仍有效，但不能替代整体视觉通过。

2026-07-13 B2.10（v0.9.16，529-538）按 A178 只修 B2.9 共同内芯分面对称性。脚本 `scripts/ui-contracts/wmw/wmw_v0916_left_card_b210_symmetric_core_pipeline.py` 以 `CORE_MASK=[302,216,362,277]` 与中心 `(332,246)` 参数化生成四块镜像分面；首次直接裁入历史 `CORE_MASK` 时，gate 主动检出掩膜自身单像素不对称导致左右面积 `921/876px`、镜像 IoU `0.95114`，未放宽判据。最终结构分面使用 `CORE_MASK ∩ horizontal_mirror(CORE_MASK)`，完整 `CORE_MASK` 继续清除旧语义，交集外边缘只铺状态基色。536 manifest 记录端点误差 `0px`、中心误差 `0px`、左右面积 `876/876px`、面积差 `0`、镜像 IoU `1.0`，明度 top `+3` / left-right `0` / bottom `-3`，共享稀疏颗粒覆盖率 `0.082106`；approved 外环 `1983/1983px` 保留、内芯外与右侧走廊变化均为 `0px`，未调用 inpaint / 模糊 / 扩散。529/530 已由美术指导与 UI 设计师只读复核为 PASS；531 atlas、532 几何 QA、533/534 Python 回填、535 16 点证据板、536 manifest 已生成。537/538 由锁定的 Godot 4.6.2 windowed OpenGL3 生成，未用 headless，非黑、颜色多样性与 baseline 缺失采样 `0` 均通过；UX 老哥终审 537 的 P0/P1/P2 均为 0，未见图标重影或外环 / 右框回退。当前只写 `evidence_ready_pending_user_visual_review`，等待用户最终裁决，不是冻结生产资源。

2026-07-13 B2.11（v0.9.17，539-548）按 A179 修复底部 meta 纸条过窄和文字拥挤。用户采纳正式扩槽路线后，`left_region_card` 合同显式升为 0.8.4，仅把 `meta_line=[22,138,96,10]` 修订为 `[22,138,112,14]`；卡片、照片、标题纸签、状态徽章、hit rect 与 B2.10 其它层均不动。脚本 `scripts/ui-contracts/wmw/wmw_v0917_left_card_b211_meta_carrier_pipeline.py` 以旧纸条四角 / 边框和标题纸签安静纸面配料重建新 carrier，禁止拉伸、模糊、inpaint 与纯色带；第一版重复纸纹分隔线被证据板拦下，改用安静中心材质后重跑。546 manifest 记录四状态目标区 alpha 洞 `0`、目标区外变化 `0px`、纸面覆盖率 `1.0`，最长压力串右侧仍余 `57px`；Godot runtime 使用 15px 字号、9px 左内边距、垂直居中和单个中点分隔。539/540 经 UI 设计师与美术指导复核 PASS；541 atlas、542 几何 QA、543/544 Python 回填、545 回归板、546 manifest 已生成并通过 JSON / delivery manifest 校验。547/548 由锁定的 Godot 4.6.2 windowed OpenGL3 生成，未用 headless；normal 颜色数 `61912`、非黑像素 `2073127`，QA baseline 缺失采样 `0`。UX 老哥终审判定 runtime visual PASS，P0/P1/P2 均为 0。当前仍等待用户最终观感裁决，不是冻结生产资源。

2026-07-13 用户复核 B2.11 后认为扩宽纸条的整体效果仍不好，提出“符号 + 数字”或完全删除两条路线；UX 老哥与 UI 设计师均推荐完全删除，用户采纳为 A184。B2.12（v0.9.18，549-558）因此显式撤回 A179 的生产候选路线：`left_region_card` 合同升至 0.8.5 并删除 `meta_line`，不留零尺寸死槽；Python / Godot 同步删除 meta Label，本轮不实现符号数字后备方案。脚本 `scripts/ui-contracts/wmw/wmw_v0918_left_card_b212_meta_retirement_pipeline.py` 不做局部遮盖，而是以 available 为唯一母版重建完整下层面板，再派生四状态；旧纸条、边框和阴影均不作为纹理源，禁止 inpaint、模糊、扩散、镜像硬拼与平色带。556 manifest 记录四状态旧纸张像素 `0`、alpha 洞 `0`、重建区外 / title / badge 变化 `0/0/0`，退役足迹跨 `4` 个分面、最大单分面占比 `0.4286`、非周期颗粒 `0.0802`，旧边界均值梯度 `0.0508-0.0805`；合同校验与 JSON 解析通过。557/558 由锁定 Godot 4.6.2 windowed OpenGL3 生成，颜色数 `59897/58000`、非黑像素 `2072509/2073600`、baseline 缺失采样 `0`，未用 headless。美术指导基于真实 549/550/557 复审 PASS，P0/P1/P2 均为 0，未见旧纸条矩形、第二阴影、涂抹带或周期接缝。用户随后回复“好的，下一步是什么”，确认接受 B2.12；左卡当前视觉基线自此冻结。

2026-07-13 完成 `right_dossier_page` A184 容量与信息架构预检（559-562）。旧 364/367 的 `8/8 fit` 只证明旧字段未越框；UX 老哥复核为 P0 承载链断裂、P1 CTA 终点倒置 / 状态按钮化 / 计数口径串线，UI Designer 同样判定现 `meta_slot=196x22 + 3x full-hit lane` 无法同时满足 A75 地区理解正文与 A184 下沉信息。559 对比现合同保底 A 与推荐升版 B；560 以 1.5x 运行时尺度验证 B 的 default / warning / locked 均 `8/8 fit`，最小运行时字号 18px；561 为 1280x720 整屏位置回填。推荐 B 保持外框、title、stamp、photo 不动，只提议 `region_body=[22,288,276,54]`、`decision_facts=[22,346,276,32]`、`mission_intel_button=[22,390,276,44]`、`primary_enter_cta=[16,444,284,50]`。复核另发现 A184“进入代价”与现行探索规则“进入区域不扣天数、派遣签批才扣天数”冲突；559-562 已撤掉 CTA 天数，改以“地区任务预计耗时”做容量 fixture，等待用户确认术语。562 状态为 `evidence_ready_pending_user_contract_decision`；本轮没有修改合同、没有 imagegen、没有 atlas / Godot runtime 产物，用户批准前禁止进入素材生产。

2026-07-13 用户明确选择方案 B，登记为 A189 并完成正式合同升版（563-566）。`right_dossier_page` v0.8.5 保持 `320x520 @ (932,30)`、title/stamp/photo 原位，退役 `meta_slot + action_stack`，下半部改为 `region_body=[22,288,276,54]`、`decision_facts=[22,346,276,32]`、`mission_intel_button=[22,390,276,44]`、`primary_enter_cta=[16,444,284,50]`；`right_action_lane` v0.8.5 收敛为底部唯一主 CTA 单实例，新增 `right_mission_intel_button` v0.8.5。563 合同板断言上半部不变、下半部互相交叠 0、子组件绝对位置一致；564 default / warning / locked 均 `8/8 fit`、最小运行时字号 18px；565 整屏回填未压到底票据或越出右侧。566 状态为 `contract_v0_8_5_pass_ready_for_clean_sprite_brief`。locked 次级入口、warning 二次确认和“进入代价”术语仍为 provisional；本轮零 imagegen、零生产 atlas、零 Godot runtime。

2026-07-14 用户复核 563 后指出粉色框与“北美禁区警戒带”“高危”“推荐12”等真实墨迹错位。像素 / 字体探针确认旧实现丢弃 `textbbox` 的 left/top bearing：三组示例 top 偏移分别为 8px、6px、5px；旧框实际是 `draw_origin + width/height` 的 synthetic bbox，旧 `8/8 fit` 又只比较宽高，未验证绝对位置。因此 566 已降级为 `invalidated_text_bbox_overlay_false_pass_superseded_by_570`，但 A189 信息架构与 v0.8.5 槽位几何不撤回。新增共用模块 `wmw_text_layout_metrics.py`、独立校验器 `validate_text_bbox_evidence.py` 和 bearing / descender / 三种对齐单测；567-570 以实际 raster alpha bbox 重出合同板、三状态压力、整屏回填和 manifest，排版、粉框与记录共享同一 bbox，绝对包含关系重新通过，三状态仍为 `8/8 fit`、最小运行时字号 18px。本轮仍是合同 / 代理字体证据，不是生产美术、atlas 或 Godot runtime。

2026-07-14 完成 `right_dossier_page` v0.8.5 无字 clean-sprite brief（571-572）。brief 只覆盖 `right_dossier_page`、`right_mission_intel_button`、`right_action_lane` 三类：一个 parent hollow-shell 母版负责纸张、照片窗边界及 title / status / body / facts carrier；两个 child button 各自独占完整边框、底盘、局部阴影和交互皮肤；文字、数字、状态语义图标与 hover / pressed 反馈均归运行时层。default / warning / locked 只从各自唯一母版派生，禁止按状态独立生成；locked 次级入口统一命名为 `locked_context_enabled`，只有底部主 CTA 为 `locked_disabled`。双 agent 复核为 P0=0；P1 是主 CTA 色族待裁决、主次按钮需要明确视觉权重差、locked 语义不得误写为 disabled；P2 要求父子接缝 gate、100-200ms 运行时反馈和“线索3 / 任务12项”非等量压力 fixture。571 已目检为结构说明板，不是生产美术；572 JSON 与三份合同断言通过。当前状态为 `structure_gate=pass`、`brief_landing=conditional_pass`、`imagegen_execution=hold_for_primary_cta_color_decision`；本轮零 imagegen、零生产素材、零 atlas、零 Godot runtime，合同 frozen 字段无改动。

2026-07-14 用户复核 571 后指出两条功能条左右边缘未对齐。实测 v0.8.5 的任务情报条中心 `160`、左右 `22/22px`，主 CTA 中心 `158`、左右 `16/20px`，既非共中心也非有意单边对齐。UX 老哥与 UI Designer 均推荐同宽、同中心、双边齐，用户明确回复“可以，推进”，登记为 A196。三份合同显式升至 v0.8.6：父页两槽统一为 `[18,390,284,44]` / `[18,444,284,50]`；mission child 为 `284x44 @ (950,420)`，primary child 为 `284x50 @ (950,474)`。573 对比旧误差与新规则并冻结 `visible_body_bbox` 排除 `shadow_bbox` 的口径；574 三状态实际 raster alpha glyph bbox 均 `8/8 fit`、最小运行时字号 18px；575 整屏回填显示双边共线；576 更新三母版结构板；577 manifest 记录 `left_edge_diff=0`、`right_edge_diff=0`、`center_x_diff=0`、`width_diff=0`，40 份 bbox 全部通过。五合同与页面重叠校验、bbox validator、四组 bearing / 对齐断言、JSON 与 delivery manifest 均通过。v0.8.5 两份历史脚本已加版本锁，禁止读取当前合同后覆盖旧编号。当前仍为合同 / brief 证据，零 imagegen、零生产素材、零 atlas、零 Godot runtime；主 CTA 色族仍待裁决。

2026-07-14 用户明确选择橄榄绿，登记为 A199，并完成右 dossier 候选 A（v0.9.0，578-588）单 class 纵向切片。578 为三母版 anchor；579-581 分别是真实 imagegen 的 parent、青蓝 secondary、橄榄绿 primary 源。脚本 `scripts/ui-contracts/wmw/wmw_v090_right_dossier_candidate_a_pipeline.py` 采用分块合同映射构造 582 无字母版与三母版 atlas，不做整图压缩；parent 导出 `640x1040`、照片窗透明 `194304/194304`、边框结构破损 `0`，两个 child 导出 `568x88/568x100`，可见主体 bbox 左右 / 宽度差均为 `0`，阴影另量。583/584 Python 回填的 8 个实际 raster glyph bbox 全在槽内；复核发现 Python / Godot 临时图标漂移后已改为两端共用 globe / document / arrow / check PNG 配料。585/586 由锁定 Godot 4.6.2 windowed OpenGL3 runner 生成，颜色采样 `3789/3856`、非黑采样均 `32400`。UX 老哥与 UI Designer 均判 P0=0、P1=0，可交用户视觉裁决；仍保留“推荐12”正式单位与整条按钮统一 hover / pressed 反馈两个 P2。588 状态为 `evidence_ready_user_visual_review_pending`，候选未冻结，未批量生产其它 class。

2026-07-14 用户继续复核 585 后指出三项实际缺陷，候选 A 因此被 588 降级为 `visual_fail_runtime_alignment_padding_and_image_aspect`：header icon / title / status 只按各自 carrier 居中，视觉轴不齐；`region_body` 文字直接使用冻结外槽，贴住左侧青色索引条；照片源为左卡 `348x128`，Godot `STRETCH_SCALE` 到 `414x264`，造成约 73.4% 的相对纵向变形。用户采纳 A201 后完成候选 A1（v0.9.1，589-597）：589 先锁页眉光学轴、正文 inner/no-text 与照片 `69:44` 三层规格，590 再真实 imagegen 纯场景；脚本 `scripts/ui-contracts/wmw/wmw_v091_right_dossier_candidate_a1_pipeline.py` 生成 `1104x704` source、`552x352` ingredient、591 配料 QA、592/593 Python 回填、三母版 atlas 与 597 manifest。raw→source 只裁横向 `0.27%`、无上采样，source→ingredient 为严格 `0.5x/0.5x`；页眉实际 ink bbox 中心为 `118.5/117.5/118.5@2x`，目标轴 `118`；正文两行 bbox 左缘均为 `68@2x`，距禁字区右缘 `16px@2x`。Godot capture 改为照片专用 `STRETCH_KEEP_ASPECT_COVERED`，尺寸或比例不符时截图前直接失败；594/595 已由锁定 4.6.2 windowed OpenGL3 生成，596 为 A/A1 对比板。UX 老哥与 UI Designer 终审均为 P0=0、P1=0、P2=2；遗留仅“推荐12”正式语义 / 单位与未来整条按钮动态反馈。A1 当前为 `evidence_ready_user_visual_review_pending`，未冻结、未生产动态状态或其它 class。

2026-07-14 用户继续追问“推荐12是什么功能”，并明确要求以后由 AI 主动审计基本功能和组件，不应等用户逐项发现。父级对照现行玩法与 production runtime 后登记 A205：世界地图只选地区，推荐人数只在具体任务 / 派遣签批成立，因此地区级推荐人数退役；进一步确认 A1 的标题、状态、正文、facts 与任务数也混入压力 / 演示 fixture。597 已降级为 `visual_fail_fixture_semantic_leak_superseded_by_604`。候选 A2（v0.9.2，598-604）复用 A1 无字 parent / child、69:44 照片与共享图标，不调用 imagegen、不改三份 v0.8.6 frozen、不生产其它 class；Godot 逻辑导出 production fixture，Python / Godot 同读该 JSON。598 覆盖 8 个功能组件 + 2 组图标配置；599/600 实际字形 bbox `7/7`、语义与 bbox 两个独立 validator 均 PASS；601/602 由锁定 4.6.2 windowed OpenGL3 生成，颜色采样 `3799/3905`，非黑与相对基线完整性通过；603 为 A1/A2 对照。终审后又将 facts 修为 `任务构成 · 限时1 · 线索2 · 深链1`，正文修为 `本周剩余7天，红线稿应优先处理`。UX 老哥最终 `P0=0/P1=3/P2=1`，UI Designer 判可交用户视觉裁决；三个 P1 裁决点为北美与金字塔照片的地区身份、action row 三段式观感、secondary / primary 默认权重。604 状态为 `evidence_ready_user_visual_review_pending`，A2 未冻结、未生产动态状态。

2026-07-14 用户完成 A2 三项组件视觉裁决并登记 A206。照片方面，当前北美与金字塔 / 雷达 / 荒漠组合只认作照片槽与构图图例，不承担正式地区身份；地区名单与内容冻结后按精确 `69:44` 规格逐区专门生图。动作方面，青色 `mission_intel_button` 只在当前 dossier 展开少量只读摘要，不切页、不选任务、不派遣、不扣天数；橄榄绿 `primary_enter_cta` 才进入地区任务台，切页但不扣天数，耗时发生在后续派遣签批。两行各只有一个整行 `hit_rect`；左右圆标与中央 label 没有三个独立功能。双 agent 复核确认 A196 的同宽共轴可以保留，但当前同模板端部圆槽、共同右箭头与近似重量造成“伪三控件 + 动作伪并列”。A2 两份 action child 因此降级为 `visual_fail_action_scope_and_affordance`；production fixture、parent 上半部、正文、状态与照片比例证据继续可复用。本轮只更新决策、交互规则与 Loop Log，不改三份 v0.8.6 frozen，不生产新素材。`查看任务情报 · 4项` 的总数与 popover 仅显示 2–3 条摘要仍需下一版收敛。

2026-07-14 按 A207 完成候选 A3（v0.9.3，605-611）默认态结构轮。两份 action child 不再修补 A2 源，而是以连续多边形空底重建：旧左右圆托、中央纸签和主 CTA 左侧重复地球全部退役；任务总数回到 `decision_facts`。`WeeklyRunContent.WORLD_MAP_UI_COPY` 成为 `展开任务情报 / 收起任务情报 / 进入地区任务台 / 暂不可进入` 的生产文案真源，fixture 由 Godot 逻辑导出。605 记录两空底尺寸 `568x88/568x100`、alpha 连通组件 `1/1`、核心透明洞 `0/0`、旧圆环 / 纸签槽内像素 `0/0`；606/607 文字 bbox `7/7`；608/609 由固定 4.6.2 windowed OpenGL3 生成。第一次 609 因新建第二 SubViewport 丢失右侧说明区却被旧全图统计假放行，已作废并触发 F1 Loop Log；重截改为同场景追加 QA，独立右侧亮像素探针 `2349/2349`、保留率 `1.00`。610 为 A2/A3 对比板，611 通过合同与可见字段校验。UX 老哥和 UI Designer 均判 `P0=0/P1=0/P2=1`，无必须先修项；唯一 P2 是青色 disclosure 的满宽实底仍略像次级按钮。A3 当前为 `evidence_ready_user_visual_review_pending`，等待用户决定是否接受该权重；用户确认前不得冻结或生产 hover / pressed / locked。

2026-07-15 用户明确否决 A3 青色满宽实底，并登记 A209：`mission_intel_button` 继续保留 284×44 frozen 热区与单一回调，但可见层改为透明内联 disclosure header；文案从命令式 `展开 / 收起任务情报` 收敛为静态章节名 `任务情报`，状态只由小 chevron 与邻近内容表达。A4（v0.9.4，612-618）不生成新 PNG 背板、不调用 imagegen：文档位于 frozen `left_icon_zone`，章节名和 chevron 位于 frozen `label_plate`，`right_action_badge` 几何保留但墨迹为 0，底部仅保留 `[16,42,252,1]` 的 28% alpha 分隔线；橄榄主 CTA 直接复用 A3 资产与 hash。612 / 613 / 614 记录有色面积 `5.23%`、满宽实底行 0、封闭轮廓 0、bevel / shadow 0、文字 bbox 7/7；615 / 616 由固定 4.6.2 windowed OpenGL3 生成，右侧亮像素 `2196/2196`、保留率 `1.00`；617 为 A3/A4 对比板。合同目录校验、可见字段语义校验和周循环三项 smoke 均通过。UX 老哥与 UI Designer 输出复审同判 `P0=0/P1=0/P2=1`：静态伪并列已消除，frozen 适配未产生新问题；唯一 P2 为动态状态尚无证据。618 当前为 `evidence_ready_user_visual_review_pending`，用户确认前不冻结、不生产 hover / focus / pressed / expanded / locked。

本轮复审记录：`docs/plans/world-map-benchmark-landing/2026-07-14-world-map-wmw-right-dossier-candidate-a2-semantic-audit-review.md`；事故复盘：`docs/plans/world-map-benchmark-landing/2026-07-14-world-map-wmw-right-dossier-fixture-semantic-leak-loop-log.md`；执行 brief：`docs/plans/world-map-benchmark-landing/2026-07-14-world-map-wmw-right-dossier-clean-sprite-brief-v0-8-6.md`。
动作作用域与视觉控件数量 Loop Log：`docs/plans/world-map-benchmark-landing/2026-07-14-world-map-wmw-right-dossier-action-affordance-audit-gap-loop-log.md`。
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
B2.9 无涂抹状态徽章复审：`docs/plans/world-map-benchmark-landing/2026-07-10-world-map-wmw-left-card-b2-9-no-inpaint-badge-review.md`。
B2.9 内芯分面对称性 Loop Log：`docs/plans/world-map-benchmark-landing/2026-07-10-world-map-wmw-left-card-b2-9-core-facet-symmetry-loop-log.md`。
B2.10 对称内芯复审：`docs/plans/world-map-benchmark-landing/2026-07-13-world-map-wmw-left-card-b2-10-symmetric-core-review.md`。
B2.11 meta 纸条扩槽复审：`docs/plans/world-map-benchmark-landing/2026-07-13-world-map-wmw-left-card-b2-11-meta-carrier-review.md`。
B2.12 meta 载体退役复审：`docs/plans/world-map-benchmark-landing/2026-07-13-world-map-wmw-left-card-b2-12-meta-retirement-review.md`。
右 dossier A184 容量与合同决策复审：`docs/plans/world-map-benchmark-landing/2026-07-13-world-map-wmw-right-dossier-a184-capacity-review.md`。
右 dossier 文字 bbox 错位 Loop Log：`docs/plans/world-map-benchmark-landing/2026-07-14-world-map-wmw-right-dossier-raster-glyph-bbox-loop-log.md`。
右 dossier v0.8.5 无字 clean-sprite brief：`docs/plans/world-map-benchmark-landing/2026-07-14-world-map-wmw-right-dossier-clean-sprite-brief-v0-8-5.md`。
右 dossier v0.8.6 同宽动作栈 clean-sprite brief：`docs/plans/world-map-benchmark-landing/2026-07-14-world-map-wmw-right-dossier-clean-sprite-brief-v0-8-6.md`。
右 dossier A1 布局与照片规格：`docs/plans/world-map-benchmark-landing/2026-07-14-world-map-wmw-right-dossier-candidate-a1-layout-and-photo-spec.md`。
右 dossier A1 复审：`docs/plans/world-map-benchmark-landing/2026-07-14-world-map-wmw-right-dossier-candidate-a1-layout-photo-review.md`。
右 dossier运行时比例 / 内边距 Loop Log：`docs/plans/world-map-benchmark-landing/2026-07-14-world-map-wmw-right-dossier-runtime-aspect-and-padding-loop-log.md`。
右 dossier A3 动作层级复审：`docs/plans/world-map-benchmark-landing/2026-07-14-world-map-wmw-right-dossier-candidate-a3-action-hierarchy-review.md`。
右 dossier A3 QA 基线丢失 Loop Log：`docs/plans/world-map-benchmark-landing/2026-07-14-world-map-wmw-right-dossier-a3-qa-baseline-loss-loop-log.md`。
右 dossier A4 内联 disclosure 复审：`docs/plans/world-map-benchmark-landing/2026-07-15-world-map-wmw-right-dossier-candidate-a4-inline-disclosure-review.md`。
右 dossier A5.1 原位任务预览复审：`docs/plans/world-map-benchmark-landing/2026-07-15-world-map-wmw-right-dossier-candidate-a5-1-in-place-mission-preview-review.md`。

## 1.1 Godot 截图最小复现结论（2026-07-08）

| 模式 | 结果 | 说明 |
| --- | --- | --- |
| `--headless` + `root.get_texture()` | 失败 | dummy renderer 返回 null；本轮最小复现 headless 分支出现 signal 11，仍按“不可用于 UI 截图”记录，不判环境坏 |
| `--headless` + `SubViewport` | 失败 | 同上，不是 v0.9 / v0.9.2 脚本独有问题 |
| windowed + `--rendering-driver opengl3` | 截图技术链通过 | 左卡 380/381（候选 A）至 557/558（B2.12）已生成；右 dossier 585/586 至 633-635 为有效组件证据，639-641 虽生成成功但因错宿主作废 |
| 错误 Godot 版本（如误选 4.6.3） | 不稳定 | runner 现固定优先 `tools/godot/4.6.2-stable/` |
| 只等 `process_frame` 就取图 | 可能全黑 | 曾出现 389/390 全黑帧；capture 脚本已改为等 `RenderingServer.frame_post_draw` 并拒绝全黑帧 |

复现脚本：`gd_project/tests/godot_capture_minimal_repro.gd`  
推荐 runner：`scripts/run_wmw_godot_capture_v09.ps1`

## 二、路线环状态

| 环 | 阶段 | 状态 | 说明 |
| --- | --- | --- | --- |
| 1 | 风格标杆理解 | 可用 | WMW 标杆方向已认可（低多边形、大块色面、档案纸张、贴纸、深色地图板） |
| 2 | 页面结构 / 职责 | **三栏职责与 v0.4 rect 获用户确认** | v0.4 `x=30,w=348`、18px 间距、地图与右档案 rect 作为下一 art pass 布局真值；不重开版面 |
| 3 | 真实内容有字 mock | 按分层路线重定义 | 整屏有字生图多次倾斜失败，已切分层路线；图文融合改由“无字素材 + 运行时回填预览”验证（环 7 之后） |
| 4 | 组件比例分类 | **通过** | v0.8：主组件为长方形家族，方形只属于 icon / sticker / badge |
| 5 | 组件类几何合同 | **左卡已冻结；右 dossier v0.8.8 通过** | A211 原位展开已登记为 provisional 状态内容；正文、摘要行与主 CTA frozen 几何未改，目录合同校验通过 |
| 6 | 无字 clean-sprite brief | **旧 schedule_gate v0.1 降为技术证据** | A244 已修订其整屏宽度 / 位置；旧 342×246 母版不再作为当前视觉几何输入，仍不是正式合同 |
| 7 | 生图 / 素材生产 | **v0.6 整屏默认态内部三方终审通过，待用户美术裁决** | benchmark 为艺术真值；只交完整 1920×1080 玩家视图，不扩产孤立组件 |
| 8 | atlas / manifest | **右 dossier A5.1 gate 通过** | 638 已生成；区外 / 照片 / CTA / 外部覆盖层差异均 0，任务行 hit rect 0，25/25 字形 bbox 原始证据独立重放 PASS |
| 9 | Godot 运行装配 | **正确整屏结构接线通过** | 644-650 来自独立 WMW assembly；旧 `GLOBAL CHANNEL` 与旧 A5.1 mount 已隔离，四端同步和 0 天进入通过 |
| 10 | 多状态截图验收 | **v0.6 默认态 PASS；confirming 未开始** | 等用户裁决 v0.6；接受后做同源 confirming 与完整拆图流程，否决则目标化返修整屏 |

## 三、已锁合同清单

合同真源：`design/ui-contracts/world-map/`；校验器：`scripts/ui-contracts/validate_class_contract.py`（2026-07-08 全部 PASS）。

| class_id | 版本 | 关键几何 | 弹性位（provisional） |
| --- | --- | --- | --- |
| `left_region_card` | 0.8.5 | 204x160，四张 y=24/196/368/540，photo_slot 174x64，label_plate 114x32，action_badge 44x44 @ (144,101)；A184 已删除 meta_line | 最终 UI 字体变化后仅需重跑地区标题压力 |
| `right_dossier_page` | 0.8.8 | 320x520 @ (932,30)，上半部不动；下半部为连续正文 276x90、合并摘要 284x44、主 CTA 284x50；独立 facts 槽已删除 | 原位 collapsed / expanded 内容模式已采纳；locked 摘要与最终动画 easing 仍 provisional |
| `right_action_lane` | 0.8.6 | 284x50 单实例 @ (950,474)，仅作为底部 `primary_enter_cta` | 主文案固定，不拼地区名、不绑定天数；候选需实测 visible / shadow bbox |
| `right_mission_intel_button` | 0.8.8 | 284x44 单实例 @ (950,420)；内部为 document / title / facts / state indicator 四槽，一个 hit rect | expanded 计数与 `＋/－` 已进入候选；locked 文案仍 provisional |
| `bottom_receipt_card` | 0.8.5 | 246x138，x=288/557/826 y=558 | value_slot 贴上限；抢眼问题调字体层级不改尺寸 |

统一声明：`reference_resolution = 1280x720`，`runtime_resolution = 1920x1080`，`export_scale = 2`（素材按 2x 制作，运行时缩放；禁止 1.5x 位图放大）。压力测试基于脚本字体和实际 raster alpha glyph bbox；最终字体确定后必须按同一 bbox gate 重跑。

## 四、下一步（按新工作流）

0. **等待用户选择 A258 三套完整整屏之一**：
   - 方案 1：最轻、selected / locked / deadline / CTA 语义最稳；选中后只需简化地图块面并轻暖右纸面；
   - 方案 2：最完整命中“成年怪新闻”；选中后只需拉开 selected 与 deadline、压低纸面高光并简化地图块面；
   - 方案 3：只在用户明确希望更暗、更悬疑时选择；必须抬高纸面 / 照片中间调并避免 locked 像 disabled；
   - 用户选定后才回填真实中文、锁状态和三条异常钩子，并仍交完整 1920×1080 filled-state；不提前拆孤立组件、atlas 或接 Godot。该里程碑仍命中冷备 `game_producer` 的熔断价值窗口；若不解冻，继续由完整整屏 art-pass Gate 承担替代把关。
1. **冻结 B2.12 左卡基线**（已完成）：
   - 用户已基于 549/550/557 确认；当前基线为合同 0.8.5、551 atlas、获批前技术 manifest 556 与 557/558 Godot 证据，最终用户确认以本 STATUS 和 B2.12 评审记录为准；
   - 后续不再做局部补丁，只有新裁决或整屏回归失败才重开左卡。
2. **锁定当前 WMW 整屏宿主并撤销错接线**（本轮已完成）：
   - 正确整屏身份以 `30-v2-2-3-clean-right-function.png` 与其 `production-contract.md` 为基线：左卡栈、中央低多边形世界地图、右侧独占 A5.1 地区决策栏；全局日程与辅助入口只在左 / 中栏下方，右下只保留进入地区唯一 CTA；
   - 575 只作 `component_reinsert_review_board`：不得继承其跨入右栏的第三张底票，也不得把右下 globe / eye / check / hand 等符号资产表现为工具栏或正经功能；
   - 不得出现 `GLOBAL CHANNEL` 顶栏、旧装订索引、旧频道回条、右栏下方票据堆叠或无功能 icon strip；
   - 先定向清理 `WeeklyRunGame` 错误挂载，再为新 WMW 整屏建立独立 assembly scene / 正确宿主，禁止继续在旧场景补丁；
   - 施工边界与首图 gate 已落到 `2026-07-16-world-map-wmw-v223-screen-structure-recovery.md`；底部旧三票合同不原样接回，待功能审计后新建 compact class 或减项；
   - 644 双参考板与 645-650 运行证据已通过 `screen_identity_gate`；A5.1 frozen 位置漂移也已修正并加入断言。
3. **A5.1 组件证据**（组件级与整屏结构级已完成）：
   - 629-638 继续证明 A5.1 的原位展开结构；639-643 只作错宿主失败样本；
   - 644-650 已重新编号生成 collapsed / expanded / locked / QA / GIF / manifest；639-643 不复用。
4. **剩余轻合同并行补完**（不阻塞右 dossier 容量复核，不批量生产）：
   - `393` 已产出合并板：`map_panel` 只定烘焙分界（底图烘什么；pin / 路线 / 选中层全部运行时）；
   - `top_status_strip` 已记录低密度轻合同；
   - `icon_badge` 集已记录清单 + 尺寸网格，atlas 打包前再升为正式合同或图集清单。
5. 素材不服从当前有效合同默认判素材失败；若量测证明合同与已采纳标杆冲突，必须停下交用户裁决，获批后显式升版本并重跑校验器、整屏回填与 Godot 全链，禁止执行方私改。
6. **本资产线收尾时执行 Workflow Lab 首跑 + gate 合并审查**（2026-07-08 挂入，来源：错题本复盘 A165）：
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
