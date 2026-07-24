# 发刊编辑界面标杆落地状态

更新时间：2026-07-22（v6 继续作为功能结构与交互位置真值；中央双版编辑结构稿 v2 已完成 UI / UX 双 PASS，待用户结构裁决；不是 Godot 生产界面）

## 当前结论

A238 已冻结 `formal_ui_structure_wireframe_v4`：桌面 `1920×1080`、固定 `320 / 1040 / 360` 三栏、双页完整常显、8 卡无滚动、12 卡仅左栏滚动、定向替换、重算阻断、右栏固定阻断与唯一 CTA。用户本轮又明确采用“无名称搜索、类型筛选与等级/获得时间排序并存”的左栏方案。

当前最新冻结的功能 / 布局候选仍为 `weekly-editorial-formal-visual-packaging-v4`；v6 继续作为信息架构、功能区责任与交互位置真值。用户未整套选择 A / B / C，而是明确锁定 B 的明亮杂志纸面，同时要求外围底板与组件恢复 benchmark 的深海军蓝和钴蓝 / 青绿 / 橄榄中间调；v2 只保留为程序换肤失败样本。

**当前截图仍不是最终界面或 Godot 生产证据。** v4 没有重新生成正式方形母图或横向扩图，A01–A06 旧素材只用于图片窗与裁切压力预览，A07–A13 仍是占位；组件合同、Godot、GDD 规则真源均未修改。

发刊规则仍有一项待裁决：公式侧要求必填槽位完整，边界侧允许头条为空时尝试发刊。本视觉候选沿用现有硬阻断展示，但在裁决前不得把该口径冻结进 GDD 或组件合同。

## 已完成

- A238 已记录 v4 功能结构冻结，v4 作为正式视觉包装的结构真源。
- 用户在正式视觉包装候选 v1 上重新打开了报道图片框合同：每篇报道以一张方形核心构图为真源，除主头版外全部使用方图，主头版横图只能由方图左右扩图获得。
- 两规格图片合同黑白结构审阅板 v1 已完成 UX 诊断 → UI 设计 → 父级合并；当前推荐 `1024×1024` 方形母图、`189×189` 普通位、`210×210` 副头版方图与 `15:8` 主头版扩图，P0 为 0。
- 用户已确认上述精确参数；正式视觉包装候选 v2 已完成独立 HTML 落地与 `1920×1080` 回归。
- v2 默认定向、真实换稿重算、确认送印与 12 条候选左栏滚动均通过；三张静态证据、animated WebP 与机器审计已生成。
- 用户随后依据 v2 实图撤回副头版 `210×210` 方图方案，指出其造成大片无法填充的无职责空白。
- UX 复诊判定 v2 `FAIL`、副头版横图方向 `PASS WITH CHANGES`；UI Designer 与父级统一采用 `375×200`，不采用与主头版等权的 `410×219`。
- 正式视觉包装候选 v3 已完成默认、最长标题、真实换稿重算、确认送印与 12 条候选回归；三张静态证据、7 帧 animated WebP 与机器审计已生成。
- 用户已确认并冻结 v3 副头版横图结构；随后提出主头版标题需更大以形成头版感。
- v4 已完成 UX 诊断 → UI 设计 → 父级合并；主标题改为真实字宽驱动的 `28px` 单行 / `24px` 双行，A01 与最长 A12 均无溢出，主图和 meta 未移动。
- 用户查看 v4 完整三栏双版截图后确认标题大小，A247 主头版标题层级正式冻结。
- v5 已完成 UX 诊断 → UI 设计 → 父级合并；普通编辑、定向替换、重算、确认冻结与实际清空后的空版状态均已回归，清空入口只在可执行状态显示并进入键盘焦点链。
- 用户指出 v5 的“选择可替换版位”无法直接理解；v6 已按 UX 复核 → UI 设计 → 父级合并改为不可点击的明确下一步提示，其余状态未改变。
- 用户明确要求在当前 v6 UI 布局基础上，按两张美术标杆生成完整风格稿；首稿因三栏几何漂移内部退回。v2 虽锁回 `320 / 1040 / 360` 三栏并曾通过 UI / UX 复审，但用户指出它仍是程序框体换肤，现已正式否决；原 PASS 无效。
- 左栏已落地无名称搜索的类型多选筛选，以及等级/获得时间四向排序。
- 正式视觉包装候选 v1 已完成 UI Designer → UX 老哥 → 父级合并；UX 结论 `PASS WITH CHANGES`、P0 为 0。
- UX 必须修中的排序状态常显、11px候选元信息、合法目标角标、明确返回修改、项目内清空确认与锈红语义收敛已完成。
- 已生成五张 `1920×1080` 状态截图、审阅总览板、6帧 animated WebP 与机器审计。
- 删除常驻教学 footer、固定持稿功能条、可交互页眉、单版聚焦和上下文缩略分支。
- 双版保持 `490×800` 常显，并共享唯一 `slot_assignment`。
- 刊头只承担《世界未解之谜周刊》身份装饰，不承载选择或取消功能。
- 主 / 副页面统一 `#AA916B` 基础纸色与 `#D3B37C` 纸边。
- 新增真实生图 `editorial-secondary-head-slot-base-v2.png`；旧冷钴蓝 v1 保留为偏差证据但不再加载。
- A02 报道图、fallback 互斥、文章 ID 映射与报道图全亮规则继续保留。
- `StatusBadge` 与 `ReturnToCandidates` 已退出当前实现。
- 已上版报道不在候选池重复显示；槽内稿直接从真实版位拖动。
- 点击路径支持候选优先与版位优先换稿；拖拽支持投放、替换、移动、交换和退回候选。
- 打开发刊确认时清除全部临时状态并冻结编辑入口。
- A218 首张普通报道图《港口广播连续七晚播报明天的潮汐》已真实生图并接入；同一母图覆盖 compact / tall 四个普通版位，按 `article_id=1003` 跟随文章移动，无映射报道继续显示 fallback。
- 新报道图片层忽略鼠标输入，不改变 A214 的默认 `0`、点击 `1`、拖拽 `0` 换稿按钮合同。
- A220 已把 `article_id=1001 / 1002 / 1003` 三张报道图统一重绘为粗颗粒低多边形编辑插画；保留原运行时文件名、尺寸、槽位与文章绑定，不修改 UI、交互或 manifest。
- 三张新图已由 Godot 重新导入，并在 `1920×1080` 默认双版状态中同时成功显示；本轮只做单状态运行预览，未重复完整交互 / smoke 链。
- `article_id=1004`《罗斯威尔档案第十四页拒绝被复印》已按单图纵向切片完成真实生图、确定性居中裁切与 `756×696 RGB` 运行资产输出；在 `189×170` 普通版位中首先读出“复印机＋拒绝被复制的纸”。
- A222 已记录用户对 1004 单图与默认双版落位的明确确认，并据此只继续 1005；该确认不扩张为整屏或 1006 预先通过。
- `article_id=1005`《市政厅新增了一个不存在的影子部门》已完成内置真实生图、确定性居中裁切与 `756×696 RGB` 运行资产输出；在默认 `189×174` 右页普通版位中先读“实体市政楼＋建筑不存在的影子侧翼和第二道门”。
- A224 已记录用户对 1005 单图与默认双版落位的明确确认，并据此只继续 1006；该确认不扩张为整屏或其他 B / C 级资源预先通过。
- `article_id=1006`《街区猫群一致拒绝经过蓝色电话亭》已完成内置真实生图、确定性居中裁切与 `756×696 RGB` 运行资产输出；在默认 `189×174` 右页普通版位中先读“钴蓝电话亭＋停在同一侧的三只成年猫”。
- 普通版位图片按 `article_id + role` 查询 manifest；1003 / 1004 / 1005 / 1006 均可跟随文章移动到 compact / tall，切换到真实存在但未映射的文章时会清空旧纹理并显示原 fallback。
- manifest 已升至 v7，新增 `editorial_story_cats_refuse_blue_phone_booth`；未修改 UI、布局、标题、交互、签批或既有报道资产的运行尺寸与文章绑定。
- A225 已记录用户对 1006 单图与六版位全填充双版预览的明确确认；1003–1006 普通报道图单图切片序列据此结束，但不扩张为整屏或其他 B / C 级资源预先通过。
- `0/6、3/6、5/6、6/6` 四个容量态已在真实 `1920×1080` Godot 窗口中完成截图；四态均保持双版几何稳定、已填版位数与候选数互补、默认换稿按钮为 `0`。
- 上述完成项全部属于“报道图资产 + 当前程序化结构宿主”的运行验证；整屏界面包装不在已完成范围内。

## 生产证据

- v4 结构真源：`docs/prototypes/weekly-editorial-formal-black-structure-v4/`。
- 正式视觉包装候选 v1：`docs/prototypes/weekly-editorial-formal-visual-packaging-v1/`。
- 正式视觉包装候选 v2：`docs/prototypes/weekly-editorial-formal-visual-packaging-v2/`。
- v2 状态截图、换稿动态与机器审计：`docs/screenshots/2026-07-21-weekly-editorial-formal-visual-packaging-v2/`。
- v2 交付清单：`2026-07-21-weekly-editorial-formal-visual-packaging-v2-delivery-manifest.md`。
- 正式视觉包装候选 v3：`docs/prototypes/weekly-editorial-formal-visual-packaging-v3/`。
- v3 状态截图、换稿动态与机器审计：`docs/screenshots/2026-07-21-weekly-editorial-formal-visual-packaging-v3/`。
- v3 交付清单：`2026-07-21-weekly-editorial-formal-visual-packaging-v3-delivery-manifest.md`。
- 正式视觉包装候选 v4：`docs/prototypes/weekly-editorial-formal-visual-packaging-v4/`。
- v4 主状态、最长标题压力截图与审计：`docs/screenshots/2026-07-21-weekly-editorial-formal-visual-packaging-v4/`。
- v4 交付清单：`2026-07-21-weekly-editorial-formal-visual-packaging-v4-delivery-manifest.md`。
- 正式视觉包装候选 v5：`docs/prototypes/weekly-editorial-formal-visual-packaging-v5/`。
- v5 普通编辑 / 定向替换整页截图与机器审计：`docs/screenshots/2026-07-21-weekly-editorial-formal-visual-packaging-v5/`。
- v5 交付清单：`2026-07-21-weekly-editorial-formal-visual-packaging-v5-delivery-manifest.md`。
- 正式视觉包装候选 v6：`docs/prototypes/weekly-editorial-formal-visual-packaging-v6/`。
- v6 定向提示整页截图与机器审计：`docs/screenshots/2026-07-21-weekly-editorial-formal-visual-packaging-v6/`。
- v6 交付清单：`2026-07-21-weekly-editorial-formal-visual-packaging-v6-delivery-manifest.md`。
- 完整风格稿 v2 失败样本：`image_gen/2026-07-21/20260721-174656_weekly-editorial-style-draft-v2.png`（用户已否决，不得作为美术候选）。
- 完整风格稿 v2 交付清单：`2026-07-21-weekly-editorial-full-style-draft-v2-delivery-manifest.md`。
- 物件化完整风格稿 v3.1：`image_gen/2026-07-21/20260721-183300_weekly-editorial-objectified-style-draft-v3-1.png`。
- v3.1 交付清单：`2026-07-21-weekly-editorial-objectified-style-draft-v3-1-delivery-manifest.md`。
- A 夜班印务室：`image_gen/2026-07-21/20260721-190000_weekly-editorial-style-option-a-night-print-room.png`。
- B 现场回传编辑桌：`image_gen/2026-07-21/20260721-190500_weekly-editorial-style-option-b-field-transmission.png`。
- C 截稿校样台：`image_gen/2026-07-21/20260721-191000_weekly-editorial-style-option-c-deadline-proofing.png`。
- A / B / C 交付清单：`2026-07-21-weekly-editorial-style-options-abc-delivery-manifest.md`。
- 当前审阅总览：`docs/screenshots/2026-07-21-weekly-editorial-formal-visual-packaging-v1/00-review-contact-sheet.png`。
- 当前状态证据与审计：`docs/screenshots/2026-07-21-weekly-editorial-formal-visual-packaging-v1/`；产物类型为 `formal_visual_packaging_candidate`，不得称为 Godot 生产界面。
- 当前交付清单：`2026-07-21-weekly-editorial-formal-visual-packaging-v1-delivery-manifest.md`。
- 两规格图片合同审阅板：`docs/prototypes/weekly-editorial-two-spec-image-contract-review-v1/`；主审阅图与审计位于 `docs/screenshots/2026-07-21-weekly-editorial-two-spec-image-contract-review-v1/`。
- 两规格图片合同交付清单：`2026-07-21-weekly-editorial-two-spec-image-contract-review-v1-delivery-manifest.md`。
- 当前合同板：`PAGE-CONTRACT-BOARD-v5-SAME-PAPER-LOCAL-REPLACE.md`
- 类合同真源：`design/ui-contracts/weekly-editorial/`
- 资产 manifest：`gd_project/Assets/ui/angus_packaging/weekly_editorial/weekly_editorial_asset_manifest.json`（v7）
- 当前真实截图与动态：`docs/screenshots/2026-07-15-weekly-editorial-same-paper-local-replace/`
- 普通版位 B 级切片截图：`docs/screenshots/2026-07-15-weekly-editorial-standard-story-b-slice/`
- 三张报道图重绘后的默认双版截图：`docs/screenshots/2026-07-16-weekly-editorial-story-art-restyle/01-godot-three-restyled-story-images-default.png`
- 1004 接入后的默认双版截图：`docs/screenshots/2026-07-16-weekly-editorial-roswell-b-slice/01-godot-two-standard-story-images-default.png`
- 1005 接入后的默认双版截图：`docs/screenshots/2026-07-16-weekly-editorial-shadow-department-b-slice/01-godot-three-standard-story-images-default.png`
- 1006 接入后的六版位全填充默认双版截图：`docs/screenshots/2026-07-16-weekly-editorial-blue-phone-booth-b-slice/01-godot-four-standard-story-images-default.png`
- 四容量态汇总板：`docs/screenshots/2026-07-17-weekly-editorial-ordinary-story-closeout/00-capacity-closeout-contact-sheet.png`
- 四容量态机器审计：`docs/screenshots/2026-07-17-weekly-editorial-ordinary-story-closeout/capacity-audit.json`，`0/6、3/6、5/6、6/6` 全部通过。
- 当前截图产物类型：`runtime_state_preview / unpackaged_programmatic_structure_host`；禁止称为最终 UI、整屏包装稿或生产界面。
- 功能黑色结构稿：`docs/screenshots/2026-07-17-weekly-editorial-functional-black-structure-v1/01-weekly-editorial-functional-black-structure-v1.png`；产物类型为 `structure_wireframe`。
- 功能黑色结构审计：`docs/screenshots/2026-07-17-weekly-editorial-functional-black-structure-v1/audit.json`，`passed: true`；六张完整候选卡、隐藏第七卡、3/6 槽位、唯一合法目标和单一禁用 CTA 均通过。
- 可运行 HTML 结构页：`docs/prototypes/weekly-editorial-functional-black-structure-v1/index.html`；点击 / 拖放语义已实现，但本轮未完成本地浏览器运行验证，因此不把交互回归标记为 PASS。
- 正式界面黑白结构候选：`docs/screenshots/2026-07-17-weekly-editorial-formal-black-structure-v2/01-weekly-editorial-formal-black-structure-v2.png`；已删除全部结构注释、开发态英文与像素尺寸，默认八张候选卡完整可见。
- 正式界面黑白结构审计：`docs/screenshots/2026-07-17-weekly-editorial-formal-black-structure-v2/audit.json`，`passed: true`；八卡无滚动条、普通卡无冗余状态槽、3/6 版面、唯一合法目标、正式中文复核字段和单一禁用 CTA 均通过。
- 第七 / 八张候选卡属于 `candidate_card v1.3.0` 合同升版提议；当前生产合同仍为 v1.2.0，用户确认结构前不改真源。
- 自动交互审计：`42/42` 通过。
- 普通报道资产增量审计：`25/25` 通过；标题自适应回归的最近证据：`8/8` 通过。
- 同纸色资产 QA：`DeltaE00 0.504`、`dL 0.0113`，通过。
- Godot 周循环 smoke：`test_phase_flow.gd` 通过，`test_settlement_result.gd` 通过，`test_weekly_run_layout.gd` 失败 `22` 项。后续只读诊断确认 22 项全部来自旧布局断言：20 项重复检查已隐藏的 legacy 世界地图安全区，1 项检查已隐藏的旧 WorldMapPanel 尺寸，1 项检查已由 `RegionTaskBoardV2` 接管的旧 RegionView；随后还有未计入 22 的旧 StatsPanel 空路径错误。现行 WMW / 地区任务板对应测试共 `86/86` 通过，但正式 weekly layout smoke 尚未同步。
- 动态证据：`960×540`、10 帧 animated WebP。

## 当前工作流位置

- 当前级别：`central_spread_editorial_structure_v2_right_inner_gutter_fix_applied_pending_render_review`。
- v4 功能结构、v3 副头版横图与 v4 主头版标题层级已经冻结；早期 `weekly-editorial-packaging-mock-v1` 与 v2 副头版方图方案只作历史证据。
- 用户明确指出：A / C 整体过暗影响阅读；B 的杂志亮度值得采用，但浅帆布底板和浅色组件偏离美术标杆。
- 方案 1 钴蓝配色偏好继续有效，但主头版资产化预演 v1 已被用户否决：固定装饰侵入眉题区，真实生图在拆分时被程序重画的线框与色条取代，导致成品重新接近程序 UI。几何审计只保留为坐标证据，不再构成美术放行。
- 修正后的 v3 已完成完整 2× `visual master`、真实动态文字 / 报道图回填和整屏预览：纸面、照片压角与印务信号来自真实生图，程序只做裁切、蒙版、内容回填与位置合成。因其余区域仍为程序皮肤，v3 当前只记为组件级局部暂准；整屏图只证明位置兼容，不再要求用户据此批准美术或放行拆层。
- 中央双版区域母件 v1 的合同几何、暖纸 / 书脊和报道图材质可保留，但用户判定文字与图版配合很差、没有报刊感且不如程序版；此前 UI / UX PASS 已撤回，v1 不得反向拆层。
- 返工只保留中央区域 / 页壳 / 书脊 / 六个版位外矩形与命中区；六组内部 headline / photo / meta 排列、主副头版构图、版头 / 栏网 / 图注带和印务信号全部解冻。下一轮仍是中央双版，不启动左栏。
- 中央双版编辑结构稿 v2 的右页普通报道空轨修正已写入 HTML：图片保持 `160×160`，由 `x=53` 移至 `x=26`，全高竖线改为 `32px` folio 短规则，标题与 meta 不动。原 UI Designer / UX 全区域 PASS 仍保持撤回；本轮预览环境拒绝直接打开本机 `file://` 页面，待补真实整版截图后再决定是否冻结。
- 已正式采用 `局部暂准 → 区域通过 → 整屏冻结 → 运行态生产冻结` 审阅分级；未美术化区域使用目标风格代理，不显示旧程序皮肤作为审美背景。
- `candidate_card` 扩产继续暂停，不进入正式 Godot 发刊场景、组件合同升版或 GDD 修改。

## 后续仍未完成

- A07–A13 七张正式语义报道图与全部报道图的大图 / 窄槽 / 64px 缩略图裁切安全区。
- 正式视觉包装的最长中文标题、不同质量标签和多槽位裁切压力图。
- 键盘 / 手柄焦点链，以及不依赖 hover 的合法目标换稿路径（若正式范围要求）。
- `candidate_card`、`signoff_panel` 合同升版与 Godot 正式落地。
- 裁决“不完整版面属于严重风险还是硬阻断”，随后再同步 GDD 真源。
- 将 `test_weekly_run_layout.gd` 从 legacy WorldView / RegionView / StatsPanel 断言同步到现行 WMW assembly、`RegionTaskBoardV2` 与 `EditorialRoot`；这是测试清理，不是视觉包装完成证据。
- `pre_publish_check`、公开取向、同题疲劳的完整玩家可见链路；本轮只保留现有结算预览，不冒充已接通。
