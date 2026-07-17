# 发刊编辑界面标杆落地状态

更新时间：2026-07-17（功能结构纠偏：包装 Mock v1 因候选容量与双 CTA 被否决；当前黑色结构稿已通过几何与双 agent 回验，等待用户审核，不是最终发刊编辑界面）

## 当前结论

当前 Godot 发刊编辑台保持唯一“双版常显”，不提供单版放大。主版与副版已统一为同一期杂志的暖米色纸面、纸边和油墨体系；副头版继续沿用 A02“会呼吸路牌”题材的重绘报道图，但不再使用整块冷钴蓝页壳。主 / 副层级改由头版高度、标题字号、图片构图、栏线和留白承担。

**当前截图不是最终界面效果。** 现阶段只在程序化结构稿上接入了主 / 副版纸面壳与六张报道图等局部报刊资产。顶部状态条、左侧候选池、中央工作区外壳、右侧发刊复核、按钮、文字层级与大部分边框仍由 `PanelContainer + StyleBoxFlat` 等程序化控件生成，尚未完成整屏视觉包装、物件化、图文融合或最终 UI 验收。

2026-07-17 的 `weekly-editorial-packaging-mock-v1` 已因功能容量错误降级：单张约 `280×264` 大候选卡无法承载多篇报道的比较与滚动，且双 CTA 与当前 `signoff_panel` 单一 `primary_cta` 合同冲突。它只保留为包装探索 / 偏差证据，不再作为结构真源。本轮已退回黑色结构阶段，以 `8` 篇候选、`6` 张 `288×92` 常显、`2` 张滚动访问、`3/6` 版位和单一禁用签批 CTA 重新建立功能候选。

普通版位现已接入四张 B 级报道图：`article_id=1003` 港口广播、`article_id=1004` 罗斯威尔拒绝复印、`article_id=1005` 市政厅影子部门与 `article_id=1006` 蓝色电话亭猫群。compact / tall 版位会按当前文章 ID 从 manifest 动态解析对应图片；未来真实存在但未建立映射的文章继续使用既有纯色 fallback。

A225 已记录用户对 1006 单图及六版位全填充双版预览的明确确认。1003–1006 普通报道图**资产切片**的定向审计、42 项结构宿主交互回归和 `0/6、3/6、5/6、6/6` 容量态均通过；这些证据只说明报道图能在当前结构宿主中运行，不说明发刊编辑界面已经完成包装。全局 `test_weekly_run_layout.gd` 的 22 项失败已诊断为仍指向隐藏 legacy WorldView / RegionView 与已移除 StatsPanel 路径的测试漂移，正式 smoke 文件尚待同步。

交互已从“六版位动作地毯”收敛为：默认 `0` 枚换稿按钮；点击一个占用版位后只显示该版位右下 `1` 枚“换稿”；拖拽态与确认态为 `0`。候选投放、覆盖退稿、槽间移动、占用槽原子交换和拖回候选均走同一个原子事务。

## 已完成

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

- 当前级别：`formal_ui_structure_wireframe_v2_ready_for_user_review`。
- 1003–1006 四张普通报道图单图切片的用户确认继续有效；`weekly-editorial-packaging-mock-v1` 已因候选容量与 CTA 合同冲突而否决 / 降级，不得据此称为整屏包装开始或结构通过。
- UX 老哥与 UI Designer 已完成正式字段、八卡容量与右栏复核结构收束；父级已输出确定性 `1920×1080` 正式界面黑白结构候选。放行范围仍只到功能结构，不包含 Godot 运行时、最终美术、10 / 12 篇动态滚动回归或生产 UI。
- 下一步等待用户审核 v2 正式黑白结构；用户确认后，才升 `candidate_card` 位置合同并以它为布局真源进入整屏视觉包装。用户确认前不改 Godot，也不继续扩产 B / C 级资源。

## 后续仍未完成

- B 级专题 / 内页图，及 C 级地图、波形、证据模块。
- 整屏视觉包装：顶部状态条、候选报道池、中央杂志工作台外壳、发刊复核 / 签批区、CTA、空态 / 中间态 / 满态的统一物件语法与图文融合。
- 完整长标题压力截图。
- 将 `test_weekly_run_layout.gd` 从 legacy WorldView / RegionView / StatsPanel 断言同步到现行 WMW assembly、`RegionTaskBoardV2` 与 `EditorialRoot`；这是测试清理，不是视觉包装完成证据。
- `pre_publish_check`、公开取向、同题疲劳的完整玩家可见链路；本轮只保留现有结算预览，不冒充已接通。
