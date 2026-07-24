# 区域任务短签选中背板风格版 v1 生图提示

> 日期：2026-07-21  
> 模式：参考图驱动的新图生成  
> 用途：`visual_style_reference_candidate`

## 目标

生成一张桌面 16:9 的 4×2 大比例风格版，只验证四类任务在“默认 → 选中”时的颜色继承关系。四行依次为常驻、限时、连续、隐藏；左列默认，右列选中。选中背板的形状、面积和层级完全一致，仅继承该行任务类型色。

## 类型色

- 常驻：橄榄绿 `#7F8A47`
- 限时：赭黄 `#886A40`
- 连续：青绿 `#34767A`
- 隐藏：蓝灰 `#445967`

## 生成约束

- 沿用当前 C 混合短签轮廓、暖灰米纸、深蓝墨线、薄象牙切边和 clean-lowpoly-weekly 的现代周刊纸品感。
- 默认态只在单侧纸脊 / 端帽与图钉尖端保留约 `4%–7%` 类型色。
- 选中态保留默认短签，在图钉与短签接合处后方增加约 `14%–20%` 的同形背板；颜色为本行类型色的低饱和浅化版本。
- 四行背板轮廓必须一致；不得使用圆形选择环。
- 四类图标依次使用文档、沙漏、链环、隐藏眼；左右两列同一行的图标、位置和尺寸一致。
- 深海军蓝展示底，预留空标题栏、空列标题牌和空行标题牌，供后续精确中文排字。
- 禁止任何文字、伪文字、水印；禁止 hover、urgent、assigned、locked、disabled、focus、红色警告签、完整彩色纸身、旧档案泛黄、软件面板感和移动端布局。

## 参考图

- `design/art-direction/region-task-board/2026-07-20-region-task-tag-state-style-board-v1.png`
- `image_gen/2026-07-16/20260716_region-task-color-mood-E2-local-calibration-v1.png`
- `design/art-direction/references/clean-lowpoly-weekly-branch/benchmark-board-01.png`
- `design/art-direction/references/clean-lowpoly-weekly-branch/benchmark-board-02.png`
- `docs/screenshots/2026-06-24-world-map-benchmark-landing/13-ticket-symbol-atlas-v0-7-benchmark-palette.png`

生图模型负责全部纸件、图钉、图标和背板美术；`scripts/art/annotate_region_task_selected_backplate_style_board.ps1` 只在空白牌内加入精确中文，不参与美术绘制。
