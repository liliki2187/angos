# 区域地图界面风格板 v1 Router Card

## 路由结论

- **本轮交付物**：区域地图组件美术风格板与首轮视觉评审。
- **被路由对象**：`visual_style_reference`，不是完整界面、运行截图或生产资产。
- **任务类型**：主流程 UI 美术生图。
- **风险等级**：`risky`。
- **当前阶段**：世界地图 A「夜班石板蓝」已被用户选为同族界面当前配色锚点；区域地图尚无获用户确认的独立风格板。
- **目标载体**：桌面 16:9 位图风格板。

## 用户明示需求

- 继续为下一个界面建立风格板。
- 区域地图与世界地图虽然都以地图为核心，但必须在原型、氛围和元素上明显区分。
- 同时保持两张直接标杆、A 配色和同一 WMW 品牌家族。

## 本轮必要补全

- 将区域地图从世界地图的 `region-centric` 语法切换为 `event-centric` 的 `0–N` 事件坐标。
- 先生成元素风格板，验证“本地外勤案卷作业图”原型，不直接生成完整有字界面。
- 在生图前完成 UI Designer brief，并在生图前由 UX 老哥检查跨界面误读风险。
- 生图后执行 25% 缩略图、Mapness、低多边形颗粒、纸张材质、色彩面积与反向读法检查。

## 可以延期

- 按黑白功能稿生成完整区域地图界面。
- 动态中文、最长文案、安全区、状态 atlas、Godot 接入与运行截图。
- 正式 palette token、纸张 atlas、生产 manifest 与美术真源升格。

## 必读真源

- `design/art-direction/references/clean-lowpoly-weekly-branch/benchmark-board-01.png`
- `design/art-direction/references/clean-lowpoly-weekly-branch/benchmark-board-02.png`
- `design/art-direction/clean-lowpoly-weekly-branch-style-guide.md`
- `design/art-direction/clean-lowpoly-weekly-paper-material-contract.md`
- `design/gdd/exploration-and-node-dispatch.md`
- `docs/onboarding/ui-interaction-guidelines.md`
- `docs/workflows/angus-workflow-harness.md`
- 世界地图 A：`image_gen/2026-07-28/world-map-colorways-v1/01-a-night-slate-blue.png`

## Agent 路由

- `ui_designer`：定义风格板分区、资产清单、色彩比例和对象—画法映射。
- `ux_laoge`：检查世界地图二级缩放误读、地图主语、事件选择链和 25% 风险。
- `angus_art_director`：按 clean low-poly weekly 临时例外不自动调用。

## 本轮只验证

- 区域地图是否一眼读成“本地外勤案卷作业图”，而不是世界地图放大版。
- 地图是否保持事件型空间主语，并能承载同区 `0–N` 个事件坐标。
- 是否继承 A 配色、现代周刊拼贴、大块低多边形、轻纸品和黑色幽默品牌 DNA。
- 是否避免旅行社、军事 HUD、GIS、写实摄影、暗色软件后台和泛黄侦探档案。

## 本轮明确不做

- 不生成完整 runtime UI，不烘焙真实中文，不修改现有功能稿。
- 不切 atlas、不接 Godot、不声明生产标杆或正式真源。
- 不让世界地图候选的大陆、地球、全球网格和完整构图下沉到区域地图。
