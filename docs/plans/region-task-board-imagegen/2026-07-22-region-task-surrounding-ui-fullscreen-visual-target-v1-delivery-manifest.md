# 区域任务台外围一体化整屏视觉目标 v1 Delivery Manifest

## 当前状态

`surrounding_ui_fullscreen_visual_target_v1 / structure_no_go_after_user_layer_stacking_feedback`

这是一张带真实中文的 `1920×1080` selected-ready 整屏视觉目标，不是组件 atlas、生产切图或 Godot 运行候选。中央地图与 pin v7 保持冻结；event card 继续冻结。

## 本轮回答的问题

- 顶部、左索引、右 dossier 与底部行动带能否读成同一期《世界怪闻周刊》，而不是旧 Panel / Button / Label 的换皮。
- 真实中文标题、摘要、字段值、风险等级、依据、建议与 CTA 能否自然落在纸件 carrier 中。
- 用户决策链能否保持为“左侧选任务 → 地图确认 → 右侧判断风险 / 依据 / 建议 → 送至签批台”。
- 左下“推进一天”能否明确低于右下任务 CTA。

## 制作边界

- 真实生图负责外围纸材、色块、切角、折面、印刷颗粒和各区 carrier。
- 程序只负责把生成图中的完整区域裁切重排到固定坐标、回填既有地图 / pin、叠加既有 kind icon 与真实中文；没有程序绘制 carrier、边框、切角、按钮或装饰。
- 生成模型未严格遵守精确坐标，因此没有直接切图落地；本轮只将生成结果重排成视觉目标。
- 未修改 Godot、manifest、UI contract 或冻结中的 event card。

## 交付证据

- 整屏：`design/art-direction/region-task-board/surrounding-ui-fullscreen-visual-target-v1/review/01-region-task-surrounding-ui-fullscreen-visual-target-v1.png`
- 左索引与底部行动票：`design/art-direction/region-task-board/surrounding-ui-fullscreen-visual-target-v1/review/02-left-index-and-bottom-action-detail-v1.png`
- 右 dossier 风险 / 建议：`design/art-direction/region-task-board/surrounding-ui-fullscreen-visual-target-v1/review/03-right-dossier-risk-advice-detail-v1.png`
- 25% 整屏：`design/art-direction/region-task-board/surrounding-ui-fullscreen-visual-target-v1/review/04-fullscreen-25-percent-readability-v1.png`
- 几何 QA：`design/art-direction/region-task-board/surrounding-ui-fullscreen-visual-target-v1/review/05-geometry-qa-overlay-v1.png`
- 无字生图源：`design/art-direction/region-task-board/surrounding-ui-fullscreen-visual-target-v1/source/region-task-surrounding-ui-imagegen-source-v1.png`
- 可复现合成脚本：`scripts/art/build_region_task_surrounding_ui_visual_target_v1.py`

## 验证

- 输出尺寸：`1920×1080`。
- 冻结地图矩形：`x=420, y=96, w=1040, h=804`。
- 与既有运行截图的地图区域逐像素对比：完全一致。
- UI Designer：`P0=0 / P1=0 / P2=1 / GO`；唯一 P2 为 25% 下部分纸件叠边略密。
- UX：`P0=0 / P1=0 / P2=0 / GO`。
- 美术指导：`P0=0 / P1=0 / P2=0 / GO`。

以上是用户指出组件堆叠问题前的窄范围回归结论，不能继续作为整屏结构放行结论。2026-07-22 用户复核后重新打开结构 Gate：

- UI Designer：`P0=0 / P1=1 / NO-GO`。
- UX：`P0=0 / P1=2 / P2=1 / NO-GO`。
- 美术指导：`P0=0 / P1=3 / P2=0 / NO-GO`。
- 直接原因：合成脚本先贴完整大区，再重复贴入内部 carrier，形成双层檐口、重复底边和 CTA 托板。
- 当前图只保留色彩、纸材、文字层级与大区构图参考，不再是纸层结构或资产拆分真源。

## 待用户判断

当前不再请求冻结。用户若要求继续，只需确认是否按同一配色、文字和大区构图做一次定向减层；不重开风格路线。

减层图通过用户审核后，才允许反推宏观 shell、文字 carrier、CTA 权重和最小伸缩规则，并先做一个运行时竖切验证。
