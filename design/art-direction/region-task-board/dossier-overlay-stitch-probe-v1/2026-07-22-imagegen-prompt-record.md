# 区域任务 dossier 同源叠印拆分试验｜生图记录

> 日期：2026-07-22  
> 状态：`probe_only / pending_user_visual_freeze`

## 目标

在既有 `824×1920` dossier 外壳几何不变的前提下，生成一张无字视觉母件，把执行条件与风险决策表现为同一张暖纸上的青色 / 锈色印刷，而不是独立卡片、程序色块或多层 NinePatch。

本轮只验证“同源母件能否拆成透明叠印层并在 Godot 1× 无缝重组”。不修改正式 `dossier_contract.json`、component inventory、manifest 或生产实现。

## 输入参考

1. 精确外壳：`gd_project/Assets/ui/angus_packaging/region_task/v2/dossier_assetization_v1/rt-dossier-shell-v1-2x.png`
2. 分区目标：`design/art-direction/region-task-board/void-print-dossier-partition-local-board-v1/review/03-left-dual-state-right-dossier-partition-v1-1-1920x1080.png`
3. clean-lowpoly weekly 标杆：`tmp/region-task-surrounding-ui-target-v1-refs/benchmark-board-01.jpg`
4. clean-lowpoly weekly 标杆：`tmp/region-task-surrounding-ui-target-v1-refs/benchmark-board-02.jpg`

## 生成约束

- 外壳、切角、橄榄背板和纸面轮廓继承第一参考；不加入文字、数字、图标、印章或 CTA。
- 摘要区只保留一条深青编辑竖线。
- metadata 使用低饱和青色满宽印刷和低对比多边形折面，无边框、阴影和第二层纸边。
- risk 使用浅锈色印刷与左侧锈红签条，无警告图标、边框或阴影。
- CTA 槽保持空白，继续使用既有独立 CTA 资源。
- 颜色过渡可以是干净的印刷硬边，但不得出现组件间缝隙、悬浮厚度或嵌套卡片。

## 输出与归一

- 生图原件：`source/01-imagegen-no-text-dossier-master-v1.png`，模型输出 `822×1914`。
- 归一母件：`source/02-imagegen-no-text-dossier-master-normalized-v1.png`，归一为 `824×1920`，alpha 使用既有精确外壳遮罩。
- 生图工具把透明棋盘格烘进原始输出，因此运行时不直接使用整张母件；只抽取纸面内部美术色区，并再次由既有暖纸 mask 裁切。

## 程序处理边界

`scripts/art/build_region_task_dossier_overlay_probe_v1.py` 只负责：

- 尺寸归一；
- 裁切与透明遮罩；
- 把母件自然色区缩放到合同文字槽对应的 2× 美术区；
- 拼接既有 CTA；
- 生成爆炸图、重组预览和像素审计。

程序没有绘制纸纹、色区纹理、多边形折面或正式装饰。risk 叠印在文字安全区上方向上出血运行时 `10px`，只为吃掉 metadata / risk 之间的中性纸缝；文字 rect 与 CTA 锚点均未改变。

