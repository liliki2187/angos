# 区域任务短签选中背板风格版 v1 交付清单

> 日期：2026-07-21  
> 产物类型：`visual_style_reference_candidate`  
> 当前 Gate：`pending_user_visual_review`

**结论**：4×2 背板风格版已经把“选中背板继承任务类型色”做成可直接审核的美术图；它不是多路线选型，也不是生产 atlas。  
**影响**：本轮没有修改 Godot、运行时合同或 event card；原 v3 继续处于待视觉修正状态。  
**下一步**：用户确认四类颜色、同形换色逻辑与背板厚度后，决定冻结风格语义或只做一轮定向减薄。

## 实物证据

- 首选审核图：`design/art-direction/region-task-board/2026-07-21-region-task-selected-backplate-style-board-v1-annotated-cn.png`
- 无字底稿：`design/art-direction/region-task-board/2026-07-21-region-task-selected-backplate-style-board-v1.png`
- 像素尺寸：`1672 × 941`
- 生成提示：`design/art-direction/region-task-board/2026-07-21-region-task-selected-backplate-style-board-v1-prompt.md`
- 精确标注脚本：`scripts/art/annotate_region_task_selected_backplate_style_board.ps1`

无字底稿由真实生图模型完成；标注脚本只在预留空白牌内加入标题、列名、任务类型和颜色名，没有重画短签、图钉、图标或选中背板。

## 4×2 映射

| 行 | 左：默认 | 右：选中 |
| --- | --- | --- |
| 常驻任务 | 中性纸身 + 小面积橄榄绿 | 同形背板继承橄榄绿 |
| 限时任务 | 中性纸身 + 小面积赭黄 | 同形背板继承赭黄 |
| 连续任务 | 中性纸身 + 小面积青绿 | 同形背板继承青绿 |
| 隐藏任务 | 中性纸身 + 小面积蓝灰 | 同形背板继承蓝灰 |

## 已通过的方向项

- 四个选中背板轮廓一致，只改变类型色。
- 默认态仍以中性纸身为主，没有变成整块彩色按钮。
- 选中反馈位于图钉 / 短签接合处，未使用通用绿色矩形或圆形选择环。
- 文档、沙漏、链环、隐藏眼在左右两列保持同类图标。
- 整体已从程序现场拼出的底框，转向可切片的美术纸件层。

## 待用户判断

1. 常驻橄榄绿、限时赭黄、连续青绿、隐藏蓝灰是否符合类型认知。
2. 选中态是否就按“同一背板形状，只继承类型色”冻结语义。
3. 当前背板的双层纸厚是否过重；若过重，下一轮只减薄，不改颜色职责与主体结构。

## 保留边界

- 本图不证明透明裁切、像素级锚点或运行时动画，不能直接替代 v3 资源。
- 不修改已通过的尺寸、alpha、锚点、文字容量、密集避让、cluster 与 clamp 合同。
- 流程状态色与任务类型色保持独立；event card 继续冻结。
