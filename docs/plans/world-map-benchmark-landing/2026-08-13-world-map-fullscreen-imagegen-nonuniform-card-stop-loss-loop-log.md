# 世界地图整屏生图无法稳定保持 RegionCard 同壳 Loop Log

## 三行结论

- **结论**：`world-map-filled-state-contract-v1` 连续两轮真实 ImageGen 均未保持三张 `340×170` RegionCard 同壳；01 选中卡持续被模型放大，02 / 03 图片窗亦未严格同尺寸。两图只能保留为 `full_screen_atmosphere_candidate / direct_component_crop_blocked`，不得升格为 filled-state 视觉目标或组件来源。
- **影响**：整体刊头、地图证据现场、Dossier 内部重构、综合色彩与轻量黑色幽默明显接近正式 clean-low-poly 标杆，但若继续用整屏 prompt 修卡，会重复破坏刚冻结的 `same_class_geometry / 69:44 / state_zero_layout_shift` 合同，也会把“视觉目标可看”误报为“组件可落地”。
- **下一步**：触发止损，停止第三轮整屏 prompt 修补。转为“真实生图负责整屏氛围与无字视觉配料；精确合成只负责按冻结矩形回填同一 RegionCard 母壳、canonical 新闻图与动态文字”的分层路线；先交单独左栏精确回填证明，再合成完整目标图。

## Loop 记录

- **触发来源**：父级交付前自检。第一张整屏图 `01-fullscreen-imagegen-contract-miss.png` 中 01 选中卡明显高于另外两卡；第二轮只编辑左栏的 `02-left-card-edit-still-nonuniform.png` 仍保留相同结构错误。
- **原始目标**：在 A305 已冻结 `340×170` RegionCard、锁区可选中预览和单母图复用后，生成一张达到两张 clean-low-poly 正式标杆氛围的完整 `1920×1080` filled-state visual target。
- **根因**：整屏生成模型会把“selected / current”理解为扩大载体、增加内容密度和图像面积；自然图像生成无法可靠遵守三个像素级同类组件矩形，也无法证明同一 `resource_path`。这不是继续加强提示词即可稳定解决的局部措辞问题，而是生成任务分解错误。
- **已试方案**：
  1. 首轮在完整 prompt 中明确三张 `340×170`、同 `138×88` 图槽、selected 只换皮肤——失败，01 卡仍显著放大；
  2. 第二轮以首图为编辑目标，要求只修左栏且其它区域不变——仍失败，01 卡继续更高，三图窗未完全统一。
- **结构性替代**：
  1. 真实 ImageGen 继续提供整屏色彩、纸材、地图、Dossier 与卡壳视觉配料；
  2. 三张 RegionCard 必须“一类一母版”：只生成 / 选取一个无字同壳母版，selected / locked 以 BackDecor / StateDecor 派生；
  3. 用程序只做精确 mask、裁切、等比缩放、文字排版和分层合成，不程序绘制美术内容；同地区左卡 / Dossier 照片读取同一 canonical 源；
  4. 先做左栏 `3×340×170` 单独证明和 100% 局部截图，三卡同壳与 `69:44` 通过后，再回填整屏。
- **待裁决问题**：无新增产品规则；A305 已关闭功能合同。当前只需 UI / UX 对上述分层路线互审，父级据此继续执行；若互审认为会破坏第二张图整体氛围，再停下交用户选择。
- **复发判定**：命中 F1“验证等级冒充”与 F4“只修点名局部不扫同类”，也是 `assetized-ui-production-chain` 已登记的“一类一母版”规则再次未在生图前转换为执行方式。连续两轮同类缺陷已按 harness §6.2 触发止损；不新增第三条提示词补丁。
- **本轮处理**：两张图保留为氛围候选与分层配料参考，不称正式目标；第三轮整屏 ImageGen 停止。
- **复发保护**：凡整屏生图包含两个以上同类可复用功能组件，prompt 声明只能算风格意图，不能承担 same-class geometry 证明。正式 filled-state target 必须从单一无字母壳按合同复制实例，或以运行时 / 精确合成层覆盖；未经 100% 局部同壳证据不得升格。
- **沉淀判断**：更新本资产线 Loop Log，不新增 onboarding 规则或 workflow gate；现有 §5.3 一类一母版、`component_class_uniformity_gate` 与 F1 保护已覆盖，问题在于本轮开工方式未执行既有规则。

## 证据

- `image_gen/2026-08-13/world-map-filled-state-contract-v1/01-fullscreen-imagegen-contract-miss.png`
- `image_gen/2026-08-13/world-map-filled-state-contract-v1/02-left-card-edit-still-nonuniform.png`
- `design/ui-contracts/world-map/left_region_card.json` v1.0.0
- `design/ui-contracts/world-map/right_dossier_page.json` v1.0.0

## 结构替代路线执行结果（2026-08-13）

- 已停止第三轮整屏 prompt 修补，转为真实 ImageGen 单母壳与精确装配：`03-region-card-front-carrier-clean-source.png` 是无字纸张材料，`03-region-card-front-carrier-clean-680x340.png` 是按合同裁切的 2× 母壳。
- `05-region-card-assembly-board-1920x1080.png` 已证明三实例共用同一 `340×170` FrontCarrier、同一 `138×88 / 69:44` photo slot、同一槽位与零状态位移；三张新闻图继续来自各自唯一 `1104×704` canonical 母图。
- `05a-region-card-selected-locked-proof-1920x560.png` 补齐 A305 的 `selected + locked` 静态证明：锁定地区可选中预览条件，Card bbox 与槽位零位移，进入权限仍由右侧 `locked_disabled` CTA 决定。
- `06-filled-state-visual-target-contract-composite-1920x1080.png` 将真实生图气氛、A291 品牌物件与单母壳材料回填至 `1920×1080` 冻结坐标；已删除旧截止日 / 剩余日 / 进入耗时 fixture，Dossier 只保留一行 Disclosure 与一个主 CTA。
- UI Designer 与 UX 老哥互审均确认 RegionCard 分层方法、exact rect、同源图与整屏操作层级成立；互审提出的 Disclosure 重复、锁区术语与未证实时间字段已在最终图中闭合。中央北美证据簇相对偏重仅保留为待用户视觉裁决的 P2，不构成功能阻断。
- 当前结论仍是 `direction_confirmation_candidate`，不自动升为生产标杆；Godot、atlas、manifest 与 `WeeklyRunGame` 继续冻结。

## 用户复核后的再发保护（A306）

- 用户再次点名 `exec-3c9a4662-543f-47c8-b80b-803d968a12b7.png` 中 01 selected 与 02 / 03 locked 使用不同图片规格，明确裁决该做法错误。该图的左栏继续降级为 `visual_atmosphere_reference_only`，不得因整体气氛较强而恢复其大图卡 / 横幅卡结构。
- 本轮将大胆感从组件几何迁移到真实 ImageGen 共享稿夹材料、钴蓝 / 橄榄 BackDecor、锈红脊线、状态章与纸层接触；`08-left-region-index-bold-rack-proof-1920x1080.png` 和 `09-filled-state-uniform-regioncard-bold-rack-1920x1080.png` 均复用同一 `340×170` FrontCarrier 与 `138×88` photo slot。
- UX 老哥最终复审为 `P0=0 / P1=0 / P2=0`，确认三卡同壳同槽、selected 仅高一档、locked 可预览、共享 BackDecor 无伪入口；UI Designer 同样确认同族同级与大胆包装迁移通过。
- UI Designer 复审中“锁区预览仍待裁决”的意见与 A305 已冻结结论冲突，因此不采纳；继续以 locked 可选中、Dossier 预览条件、CTA `locked_disabled` 为真源。
- 后续生成或实现若再次把 selected 解释为更大图片 / 更高卡体，直接触发生产阻断，不再进入综合色彩、阴影或纸层微调。

## selected + locked 完整伴随态闭环（2026-08-13）

- `10-selected-locked-east-asia-companion-1920x1080.png` 将 A305 的 `selected + locked` 从单卡证明扩为完整屏幕状态：北美恢复 `unselected + warning + available`，东亚进入 `selected + locked`，太平洋保持 `unselected + locked`；三张卡仍为同一 `340×170` FrontCarrier 与 `138×88` photo slot。
- 中央地图改用无状态的 `world_map_board_960x902.png` 重新装配，彻底移除上一态的北美照片、红圈与英雄证据簇；东亚成为唯一拥有 selected Eye、锁定徽记、同源新闻照片和解锁条件便签的主动证据焦点。
- 东亚左卡、中央证据和右侧 Dossier 均读取同一 `east_asia_story_1104x704.png`，使用完整画幅 contain；Dossier 保留完整二选一语义“声望≥55，或先拿到罗斯威尔档案残页证据”，不使用运行时代码里的含混斜杠缩写。
- Dossier、Disclosure 和 CTA 几何继续冻结；CTA 仍位于 `[1443,956] / 414×76`，只切换为 `locked_disabled / 暂不可进入`，没有因地区被选中恢复进入邀请感。
- `11-default-vs-selected-locked-atomic-state-board-1920x1080.png` 用整屏前后态并排证明：选择、访问、证据与 CTA 原子切换，而 RegionCard、photo slot、三栏与 action rect 零位移。
- UI Designer 成图复核最初指出北美红框 / 红引线仍继承旧 selected 语汇；已改为中性蓝灰边框与短引线，仅保留“红线升温”小字为锈红风险语义。该问题在最终图中闭合。
- 本伴随态仍属于方向确认 / 视觉目标证据，不授权进入 Godot、atlas、manifest 或 `WeeklyRunGame`。
