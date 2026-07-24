# 区域任务台外围整屏视觉目标 v1.1 定向减层 Delivery Manifest

## 当前状态

`surrounding_ui_fullscreen_visual_target_v1_1_delayered / pending_user_arbitration`

本轮只修正用户指出的组件堆叠，不重开风格路线，不覆盖 v1 失败证据，不修改 Godot、manifest、UI contract 或冻结中的地图 / pin / event card。

## 实际减层

- 左栏：只贴一次完整 folder；不再先贴 folder 后重复贴 header、任务卡和 footer。
- 底栏：删除完整 outer band，只保留一个禁用动作票与一个双栏长回条，二者是同级 sibling tickets。
- 右栏：只保留一个橄榄 backing、一张连续暖纸和一个 CTA；metadata、risk、建议直接排版在同一主纸上。
- 顶栏：三个同级 carrier 各贴一次。
- 地图：继续从既有运行截图原像素回填。

## 证据

- 整屏：`design/art-direction/region-task-board/surrounding-ui-fullscreen-visual-target-v1-1-delayered/review/01-fullscreen-delayered-v1-1.png`
- 左栏 100%：`design/art-direction/region-task-board/surrounding-ui-fullscreen-visual-target-v1-1-delayered/review/02-left-folder-delayered-v1-1.png`
- 底栏 100%：`design/art-direction/region-task-board/surrounding-ui-fullscreen-visual-target-v1-1-delayered/review/03-bottom-tickets-delayered-v1-1.png`
- 右栏 100%：`design/art-direction/region-task-board/surrounding-ui-fullscreen-visual-target-v1-1-delayered/review/04-right-dossier-delayered-v1-1.png`
- 25%：`design/art-direction/region-task-board/surrounding-ui-fullscreen-visual-target-v1-1-delayered/review/05-fullscreen-25-percent-delayered-v1-1.png`
- 可复现脚本：`scripts/art/build_region_task_surrounding_ui_visual_target_v1_1_delayered.py`

## 技术校验

- 输出尺寸：`1920×1080`。
- 地图矩形：`x=420, y=96, w=1040, h=804`。
- 地图与既有运行截图逐像素对比：完全一致。
- `git diff --check`：通过。

## 复核分歧

- UX：`P0=0 / P1=0 / P2=0 / GO`。认为左栏、底栏与右栏的重复容器均已关闭，只读区不再与按钮同构。
- 美术指导：`P0=0 / P1=0 / P2=0 / GO`。认为现有纸边是单张纸的材质边与接触阴影，不构成三重容器。
- UI Designer：`P0=0 / P1=3 / P2=0 / NO-GO`。认为 header、slip、footer、长回条与 CTA 内仍能读到烘焙后纸，当前可见物理层数仍高于最小值。

父级裁决：直接重复合成已经关闭，但“单张纸的材质边是否仍显得像第二组件”属于用户需要亲眼判断的视觉问题。当前不得冻结，也不得用二比一多数意见代替用户确认。

## 用户只需判断

v1.1 在 100% 下是否仍然显得组件堆叠。若接受，冻结减层结构并进入单例资产反推；若仍显得厚，下一步改为定向重生真正单层的 header / slip / receipt / CTA 美术源，不再继续程序裁切重排。
