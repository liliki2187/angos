# Clean Low-Poly Weekly 纸张材质合同

创建于 2026-07-01；2026-09-07 将材质样本与旧页面装配日志分离。

## 适用范围

本文件保留已登记纸材的样本与复用依据，只用于明确选择这些样本的既有资产/生产批次。它不是新风格探索、配色变体或所有未来 UI 的前置 gate，也不规定世界地图的结构、字体、按钮颜色或旧版本下一步。

同一纸材的消费者应保持一致；更换材质或 token 时明确影响范围并同步实际消费者。下面样本数值未因流程重构改变，原有图片/JSON 与页面几何合同也未修改。

## 原始参考与历史样本

- 原始标杆：`design/art-direction/references/clean-lowpoly-weekly-branch/benchmark-board-01.png`、`benchmark-board-02.png`。
- 材质依据：`docs/screenshots/2026-07-01-wmw-component-correction/13-wmw-paper-material-truth-board-v0-3.png`、`14-wmw-paper-material-truth-samples-v0-3.json`（同目录）。
- 测试纸材 atlas：`docs/screenshots/2026-07-01-wmw-component-correction/31-wmw-clean-paper-material-atlas-v3-recommended.png`、`32-wmw-clean-paper-material-atlas-v3-manifest.json`（同目录）。

atlas 是当时的支线测试底材，不自动等于当前正式生产美术。原图与当前用户选定方向优先于旧实验的阶段状态。

## 保留的 token 样本

| token | 样本 | 原用途 |
| --- | --- | --- |
| warm_paper | #B7A488 | 暖灰米纸 |
| case_paper | #967E5E | 较深档案纸 |
| ivory_edge | #C0B9B3 | 照片、贴纸浅边 |
| gray_board | #686554 | 灰绿背板，非默认可写面 |
| note_paper | #B3A456 | 克制的黄色便签 |
| dark_board | #16191C | 炭色深底 |

这些不是所有新方案必须回到的统一色值，也不能从一次失败生图平均出新的“标杆 token”。

## 材质与装配

纸面使用平面大明度块和轻微印刷触感，避免污渍、旧化、褶皱穿过内容区。纸边、背纸、阴影与夹具负责接触关系，不在动态文字区域堆质感。

生产时可根据风险选择直接生图、共享纸材、分层复用或局部校色；不强制先形状后材质、角色 atlas 覆盖或 Lab 色迁移。程序归一化若抹掉宽块面、制造涂抹或接缝，不因数值接近就放行。纸材调整不能洗掉地图、照片和强调色，也不应把整张画面统一压暗。

检查同类纸面的色温/明度/纹理尺度，实际可写区与图文组合；需要精确匹配才按可比样本测量，阈值由该批次确定。样本测试和风格审查可以相互反馈，不设置“纸材量化未通过就不能看整屏”的通用禁令。

## 已隔离的历史结论

2026-07-02 的 v0.66–v0.89 装配过程、文字占高/边距阈值、深条文字承载识别、特定 CTA 配色和 contract sheet 下一步均保存在本次重构快照。它们适用于当时特定素材/画布，不是新页面默认布局。

当年的 v0.89 用户确认只证明该局部图文承载合同，不是整屏生产批准。需维护旧实现时读取相应 `design/ui-contracts/world-map/` 与原始证据；不要重新采用历史失败稿。当前通用检查见 `docs/workflows/ui-geometry-and-text-safety-gates.md`，整体方向见支线风格指南。
