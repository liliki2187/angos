# 区域任务台图文一体整屏风格稿 v1｜生图记录

> 日期：2026-07-22  
> 产物类型：`filled_state_text_mock`  
> 用途：验证真实中文内容、纸件美术、留白和信息层级能否形成一个整体；不作为 Godot 运行截图、可拆生产资产或逐字文本真源。

## 输入参考

- 编辑底稿：`surrounding-ui-fullscreen-visual-target-v1-1-delayered/review/01-fullscreen-delayered-v1-1.png`
- 风格参考：`tmp/region-task-surrounding-ui-target-v1-refs/benchmark-board-01.jpg`
- 风格参考：`tmp/region-task-surrounding-ui-target-v1-refs/benchmark-board-02.jpg`
- 冻结地图回填真源：`docs/screenshots/2026-07-22-region-task-dossier-assetization-v1/01-selected-ready-full-v1.png`

## 核心提示要求

生成一张 1920×1080、桌面 16:9 的 Angus“北岸调查区 · 区域任务台”完整有字界面美术风格稿。保留中央地图与任务短签的布局，外围采用 clean-lowpoly weekly：深海军蓝底、暖白哑光纸、橄榄与青绿、少量锈红风险色、克制的大块裁纸折面与印刷颗粒。所有中文必须作为画面中的真实排版直接生成，不使用伪字、乱码或占位符；全文限制在四级字阶内。

结构限制：左侧只允许一个索引载体、标题区、两张任务纸条和回条；右侧只允许橄榄 backing、一张连续档案主纸和一个 CTA，摘要、元数据、风险与建议靠开放色条、规则线和留白组织；底部是禁用推进票与日程回执两个同级物件；禁止卡片套卡片、双重托板、厚重 GUI 描边、发光和摄影噪声。

真实内容覆盖：返回、区域标题、期数/周数/剩余天数、两条事件标题及元信息、已选状态、七行事件摘要、地点/耗时/需求、风险等级/截稿依据/连续追踪、两行建议、任务 CTA、推进一天禁用原因以及底部日程/推进预览。

## 生成与后处理边界

1. 首次生图建立完整有字整屏。
2. 第二次仅删除两张左侧任务纸条上误生的相机图标；不要求改变布局或重做文字。
3. 本地脚本只做 1920×1080 尺寸归一、冻结地图像素回填和审核裁图；没有覆盖、重排或程序修正任何文字。
4. 生图把摘要中的“线路图”生成成近似“线圈图/线圉图”的错误字形。该错误保留为模型能力证据，不用程序修字，因此本稿不得作为逐字生产真源。

## 输出

- `source/01-imagegen-text-integrated-source-v1.png`：首次生图原图。
- `source/02-imagegen-camera-cleanup-source-v1.png`：定点删除误生相机图标后的原图。
- `review/01-text-integrated-fullscreen-style-draft-v1.png`：1920×1080 审核整屏，中央地图使用冻结运行证据回填。
- `review/02-left-text-art-integration-v1.png`：左侧 100% 局部。
- `review/03-right-text-art-integration-v1.png`：右侧 100% 局部。
- `review/04-bottom-text-art-integration-v1.png`：底部 100% 局部。
- `review/05-fullscreen-25-percent-v1.png`：25% 层级复核图。
