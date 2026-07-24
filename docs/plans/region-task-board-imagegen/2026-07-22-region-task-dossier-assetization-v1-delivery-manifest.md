# 区域任务 dossier 资产化 v1 Delivery Manifest

## 当前状态

`dossier_assetization_v1 / rejected_by_user_fullscreen_visual_system_gap_technical_evidence_only`

短签 compound v7 已冻结；event card 继续冻结。本轮只资产化右侧 dossier 的外壳、信息附页和主 CTA。

## 已落地

- `rt_dossier_shell`：`824×1920` 固定透明外壳，运行尺寸 `412×960`。
- `rt_dossier_section_plate`：`728×288` 中性 NinePatch，同一母件用于 metadata 与 risk。
- `rt_dispatch_cta_mother`：`712×224` 空白橄榄 CTA，文字与状态由 Godot 提供。
- dossier 五区采用固定坐标；empty / selected / disabled / ready 不换壳、不跳位。
- 选中后同时显示风险等级、截稿 / 连续追踪依据和一条可执行建议。
- summary 内部滚动已关闭；7 / 8 / 9 行合同回归通过。

## 真实证据

- `docs/screenshots/2026-07-22-region-task-dossier-assetization-v1/01-selected-ready-full-v1.png`
- `docs/screenshots/2026-07-22-region-task-dossier-assetization-v1/02-selected-ready-dossier-v1.png`
- `docs/screenshots/2026-07-22-region-task-dossier-assetization-v1/03-empty-disabled-dossier-v1.png`
- `docs/screenshots/2026-07-22-region-task-dossier-assetization-v1/04-empty-selected-focus-runtime-v1.gif`
- `docs/screenshots/2026-07-22-region-task-dossier-assetization-v1/05-two-line-title-pressure-v1.png`

## 验证

- Godot 4.6.3 `test_region_task_board_v2.gd`：通过。
- Godot 4.6.3 `test_region_task_manifest_v2.gd`：通过。
- Godot 4.6.3 `test_region_task_board_v2_integration.gd`：通过。
- capture：通过。
- UI / UX / 美术最终复核：`P0=0 / P1=0 / P2=0 / GO`。

## 冻结边界

2026-07-22 用户已完成整屏判断并否决冻结。局部资产保留为技术证据，但不能继续作为整屏视觉真源。用户指出：

1. 除地图外，左栏、右栏与下栏都明显粗糙，仍像程序生成界面；
2. 文字只是放入控件安全区，没有成为纸件和编辑版式的一部分；
3. 当前不应继续单件修 dossier，而应先建立整屏外围视觉与文字真值。

后续在用户授权前不继续生图或修改实现。下一验证应是一张 `1920×1080` 单方向、真实中文的整屏 selected-ready visual target；通过后再决定哪些内部 rect 继续冻结、哪些合同需要正式升版。
