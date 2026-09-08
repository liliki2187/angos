# 世界地图 A 版真实界面落地 Router Card

> 状态修订（2026-08-03）：本文的 `filled_state_visual_target_before_component_contract` 路线已被用户否决并由 A280 取代。当前路线为隔离 Godot `runtime_skeleton / runtime_state_preview`，先验证 integrated UI 的组件边界、状态同步和动态容量；证据见 `2026-08-03-world-map-integrated-functional-skeleton-delivery-manifest.md`。本文不再授权继续生成整屏目标图或按旧三栏换皮。

## 结论

- 目标：把世界地图 A「夜班石板蓝」从 `visual_style_reference` 转译为可交互 Godot 纵切片。
- 当前阶段：`filled_state_visual_target_before_component_contract`。
- 实施路线：保留动态数据、交互职责与信号，允许重构旧三栏的精确几何；以 A 的深蓝地图墙、错层剪报、新闻纸堆和编辑桌物件关系作为视觉母体，不把 A 降格成旧 runtime 的材质皮肤。
- 当前首交付：一张 `1920×1080` 真实内容有字目标界面；用户确认后，第一轮运行状态再进入 `北美禁区带 selected / 红线升温 / 可进入 / 任务情报 collapsed→expanded / 进入地区 0 天`。

## 输入真源

- 视觉锚点：`image_gen/2026-07-28/world-map-colorways-v1/01-a-night-slate-blue.png`
- 直接标杆：
  - `design/art-direction/references/clean-lowpoly-weekly-branch/benchmark-board-01.png`
  - `design/art-direction/references/clean-lowpoly-weekly-branch/benchmark-board-02.png`
- 功能稿：`design/art-direction/references/clean-lowpoly-weekly-branch/interface-inputs/world-map-functional-wireframe.png`
- 当前运行证据：`docs/screenshots/2026-07-29-godot-visual-feedback-smoke/01-world-map-region-ready.png`
- 运行实现：
  - `gd_project/scenes/gameplay/weekly_run/components/WeeklyRunWorldMapAssembly.gd`
  - `gd_project/scenes/gameplay/weekly_run/components/WeeklyRunWorldMapLeftRegionCardB212.gd`
  - `gd_project/scenes/gameplay/weekly_run/components/WeeklyRunWorldMapRightDossierA51.gd`
  - `gd_project/scenes/gameplay/weekly_run/phases/WeeklyRunExplorePhase.gd`
- 组件合同：`design/ui-contracts/world-map/`

## 路由与分工

- `ui_designer`：拆解功能—视觉映射、尺寸、切图 / 原生 Control 边界与安全区。
- `ux_laoge`：复核地区选择链、锁定权限、任务预览边界、CTA 与伪控件风险。
- 父级 Codex：合并方案、制作资产、实现 Godot、运行测试并交付真实截图 / 动态证据。
- clean-lowpoly 临时例外继续生效：不自动调用旧像素 / 半调美术指导。

## 首轮范围

### 阶段 0：用户先审的真实内容目标图

1. 使用正式 payload 回填 A 母体整屏，不使用假字与占位信息；黑白稿只做功能遗漏检查，不规定模块必须组成规整三栏。
2. 直接展示最终信息密度、视觉层级、状态距离和唯一 CTA。
3. 当前产物只是 `filled_state_visual_target`，不拆组件、不接 Godot。
4. 首张“旧骨架＋A 色材”目标稿已被用户否决并归档为偏差案例；必须先通过新版 A 母体目标稿。
4. 用户通过后再进入下方组件与运行纵切片。

### 做

1. 左侧三张真实地区卡的 selected / locked 基础状态。
2. 中央无字夜班石板蓝地图底板，以及动态 pin、标签、选中圈的联动。
3. 右侧无字 dossier、真实中文回填、任务情报原位展开和唯一进入 CTA。
4. 保留中央地区回条与“选择 / 进入地区任务台不耗天数”说明。
5. 验证左卡 / pin / dossier / CTA 共享同一 `selected_region_id`。

### 不做

1. 不把完整 A 图作为全屏背景。
2. 不新增世界地图推进一天功能；A 图里的 `DAY 1` 机器首轮不进入交互层。
3. 不启用尚未装配的三张 `bottom_receipt_card`。
4. 不在世界层选择具体任务、配置队伍或展示骰池。
5. 不修改玩法常量与进入地区 0 天规则。

## Gate

- 真实运行：必须在正式 `WeeklyRunGame` 世界模式中可点击。
- 状态一致：左卡、pin、dossier、CTA 四端点一致。
- 权限一致：锁定地区可查看缺口，但 CTA 不可进入。
- 分层：动态中文、数字、任务摘要和交互状态不得烘焙进位图。
- 安全区：文字、hit rect 不得压夹子、纸边、折角、照片边框和装饰签。
- 视觉：直接并排 A 与两张标杆，检查大块低多边形、夜班石板蓝、暖纸、克制幽默与非旅行语义。
- 证据：完整 1920×1080 collapsed / expanded 截图、关键局部、debug overlay；CTA 状态提供 GIF / WebM。
