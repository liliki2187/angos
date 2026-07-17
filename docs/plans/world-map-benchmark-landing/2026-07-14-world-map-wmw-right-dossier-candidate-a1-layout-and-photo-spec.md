# WMW 右 dossier 候选 A1 布局与照片规格（v0.9.1）

> **产物类型**：生产输入规格 / 修正 brief delta，不是生产美术。
> **设计采纳**：A201。
> **约束**：三份 v0.8.6 frozen 几何不动；完成本规格和 589 规格板后才允许真实 imagegen。

## 1. 失败输入

候选 A 的旧 runtime 使用左卡照片 `348x128` 填入 `414x264` 照片槽。Godot `STRETCH_SCALE` 的横纵缩放分别约为 `1.1897` 与 `2.0625`，相对纵向变形约 `73.4%`。Python 虽使用等比 cover，但会裁掉约 `42.3%` 总宽度并把低分辨率源放大 `2.75x`；两条路径都不得成为正式方案。

候选 A 的 header 三个 frozen 槽中心为 `56/59/63px`；正文 Godot Label 又直接占满 `region_body`，没有避开左侧青色索引线。原 588 因未检查 runtime 图片变换、真实 ink 光学轴和可见模块内边距而形成视觉 false pass。

## 2. Header 光学轴

frozen carrier 不动，只修运行时 ink：

| 项目 | 参考分辨率 | 2x 证据 | 1.5x Godot |
| --- | ---: | ---: | ---: |
| `header_optical_axis_y` | `59px` | `118px` | `88.5px`（叠加 dossier 原点） |
| icon ink offset | `+3px` | `+6px` | `+4.5px` |
| title ink offset | `0px` | `0px` | `0px` |
| status ink group offset | `-4px` | `-8px` | `-6px` |

验收读取图标与真实 glyph alpha bbox；三个 ink bbox 中心距光学轴均 `<=1px`。节点 rect、carrier 框或彩色 QA overlay 不能替代墨迹证据。

## 3. 正文安全区

| 层级 | 矩形（参考分辨率） |
| --- | --- |
| visible module / carrier | `[22,288,276,54]` |
| 青色索引线禁入区 | `[22,288,4,54]` |
| runtime inner rect | `[34,290,252,50]` |

两行实际 glyph 左缘必须 `>=x34`、彼此差 `<=1px`，与索引线右缘至少相隔 `8px`，右缘不得超过 `x286`。default / warning / locked 最长两行均按同一 inner rect 验收；禁止逐句手调偏移或继续缩字。

## 4. 照片三层规格

| 层级 | 固定尺寸 | 比例 | 操作 |
| --- | ---: | ---: | --- |
| production source | `1104x704` | `69:44` | 生图原始工作输出先等比 cover 到本规格；裁切总量每轴 `<=10%` |
| 2x ingredient | `552x352` | `69:44` | source 精确 `0.5x` 等比缩小，不裁切、不上采样 |
| runtime slot | `414x264` | `69:44` | Godot `KEEP_ASPECT_COVERED`，精确 `0.75x`，禁止 `STRETCH_SCALE` |

硬 Gate：

- 三层宽高比偏差 `<=0.5%`；
- 记录 raw imagegen、source、ingredient 的尺寸、统一缩放系数、crop rect、focal point 与文件 hash；
- ingredient 到 runtime 的 `scale_x == scale_y`；
- 任一上采样、非等比缩放、裁切超过 10% 或关键主体越出安全区，素材失败并重新生图。

## 5. 生图构图合同

- 用途：`right_dossier_page.photo_slot` 的独立纯场景配料；无边框、无纸框、无文字、无假字、无地球、无状态章、无 UI。
- 风格：clean low-poly weekly；中粗大块面、编辑插画式概括，不是照片加细密三角滤镜。
- 硬安全区：归一化 `[0.05,0.05]-[0.95,0.95]`；正式 source 约 `[55,35,994,669]`。
- 主焦点：雷达碟面中心约 `(0.74,0.46)`；雷达位于右侧 `64%-88%`，朝画面内。
- 次焦点：金字塔位于左侧 `10%-38%`，尖顶完整。
- 三级线索：天线塔位于 `46%-56%`，降低对比并保持细长，不得成为中央分割线。
- 主次固定为 `雷达 > 金字塔 > 天线塔`，三者不得等权；外围 5% 不放关键轮廓。

## 6. 本轮边界

本轮只修候选 A 的 default 静态装配：header ink、正文 inner rect、独立照片 source/ingredient/runtime。parent、两个 child、动作栈、照片槽、正文外框、状态章与 hit rect 均不改；hover / pressed / warning / locked 动态状态另轮验收，不生产其它 class。
