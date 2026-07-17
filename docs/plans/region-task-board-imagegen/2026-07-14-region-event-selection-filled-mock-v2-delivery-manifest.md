# 区域事件选择界面风格稿 v2：交付清单

> 日期：2026-07-14
> 产物类型：`filled_state_visual_mock`
> 风险等级：`risky`
> 状态：用户复核发现中央地图板存在 P1 无归属空带；当前已降级，待版式修正。不是运行时截图、组件图集或生产真源。

## Router Card

- **本轮交付物**：桌面 `1920×1080` 区域事件选择界面代表性有内容状态风格稿。
- **被路由对象**：区域任务台的视觉骨架、事件 pin 语言、左侧索引与右侧选题夹关系。
- **目标载体**：世界地图下一层的区域任务台，不是派遣签批台。
- **必读真源**：`design/gdd/exploration-and-node-dispatch.md`、两份 UI 协作文档、clean low-poly weekly 两张标杆、纸张材质合同、已选第三张地图。
- **必调角色**：`ui_designer` 先出结构，`ux_laoge` 再评审；clean low-poly weekly 临时例外下不调用旧像素坐标系的 `angus_art_director`。
- **本轮只验证**：地图是否仍是第一视觉主语；左索引 / 地图 pin / 右 dossier / CTA 是否形成同一选择链；整体是否接近标杆的现代周刊纸品与低多边形语言。
- **本轮不验证**：运行时 `0–N` 节点生成、碰撞聚合、hover / pressed / disabled、中文容量、响应式桌面回归、Godot 接入。

## 合并后的关键裁决

1. 区域地图使用事件坐标；不存在固定五热点，也不存在一地块一个入口。
2. `0` 个事件不选中；`1` 个可见事件自动选中；`2+` 个事件等待玩家点击。
3. Hover 只显示局部短签，不切换右侧 dossier；click 才固定 selected。
4. 聚合触发依据是 pin、标签、头像、阴影与展开范围的完整视觉安全区碰撞，不只看节点数量或中心距。
5. 已派遣事件退出派遣主操作流；右侧 CTA 槽改为非交互执行中回条，不保留 disabled 派遣按钮。
6. 点击地图空白只收起 cluster / chain 临时展开，不清除当前 selected。
7. 深度链第一次点击只展开，第二次选择当前环；真正进入派遣仍通过右侧唯一 CTA。

## 生成与后处理

- 整屏外壳和代表性纸品组件由内置真实生图工具生成。
- 动态 pin 组件由内置真实生图工具单独生成，并通过洋红色键控移除背景。
- 程序后处理只负责：
  - 把整屏规范化到 `1920×1080`；
  - 用已选地图原图精确回填 `960×742` 地图槽，纠正生图模型造成的横向压缩；
  - 合成真实生图得到的透明 pin；
  - 输出单独的几何 QA 图。
- 程序没有绘制或替代周刊纸品、地图、图钉和 dossier 美术。

## 交付文件

- 主图：`image_gen/2026-07-14/20260714-wmw-region-event-selection-filled-mock-map-locked-v2.png`
- QA 图：`image_gen/2026-07-14/20260714-wmw-region-event-selection-filled-mock-map-locked-v2-qa.png`
- 机器清单：`image_gen/2026-07-14/20260714-wmw-region-event-selection-filled-mock-map-locked-v2.json`
- 生图原稿：`image_gen/2026-07-14/20260714-wmw-region-event-selection-filled-mock-source-v1.png`
- pin 生图源：`image_gen/2026-07-14/20260714-wmw-region-event-marker-sheet-chroma-v1.png`
- pin 透明稿：`image_gen/2026-07-14/20260714-wmw-region-event-marker-sheet-alpha-v1.png`

## 它能证明什么

- 地图、索引、dossier 与 CTA 的横向关系可以继续保留；整屏纵向权重尚未通过，中央地图板底部存在无职责空带。
- 同一区域可出现多个事件标记，视觉上不再是一地块一个固定按钮。
- 标杆的专业文书、克制纸张、独立贴纸符号与大块低多边形地图可以在同一屏共存。
- 已选地图以正确 `960×742` 比例回填；除生成 pin 覆盖范围外，地图像素保持原图。

## 它不能证明什么

- 静态图不能证明节点碰撞、聚合扇出、标签避让和深度链展开真的可用。
- 当前英文短文案只检查视觉气质，不是最终中文 UI。
- 代表性有内容状态不能替代 `0 / 1 / 多点 / 密集 / locked / dispatched / chain-expanded` 的运行时状态验收。
- 右侧专业文书的动态文字安全区仍需后续组件合同与真实中文回填验证。

## Gate 结果

- `ui_designer`：通过结构方向，建议“地图主板 + 左窄索引 + 右悬挂 dossier”。
- `ux_laoge`：P0 为 0；四个 P1 已在本清单中冻结。
- 地图比例：通过，主图地图槽为 `960×742`。
- 产物诚实：通过，标为 `filled_state_visual_mock`，未声称运行时或生产候选。
- 视觉反向读法：当前不再像固定分区热点，但用户复核确认中央地图会被读成塞进高容器的一张插图，底部深蓝空带会被读成漏掉的 footer / 状态栏；此项不通过。
- 文档 / 实现 drift：已知旧 `region_task_asset_manifest.json` 仍有固定五热点；本轮不改实现，后续运行时合同必须改为动态事件节点。

## 允许与禁止的下一步

- **允许**：用户先评审整体风格、地图权重、纸张 / 文书气质与 pin 符号语言；确认后再做无字组件合同和运行时状态原型。
- **禁止**：本图直接切 atlas、替换 Godot runtime、升格为生产标杆或以静态图宣称动态聚合已完成。

## 2026-07-14 用户复核：中央地图板余高

- **问题等级**：P1。
- **现象**：锁定地图以 `960×742` 放入更高的中央舞台后，下方留下约百像素无标题、无边界转换、无功能的深蓝空带；上方短留边与下方宽空带也不构成有意装裱。
- **旧稿处理**：旧区域任务台让地图填满地图框，并由独立底部全局日程条接管剩余高度；详见 `docs/screenshots/2026-06-18-region-task-v3-6-separated-advance/01-region-task-v3-6-separated-advance.png`。
- **修正边界**：保留第三张地图比例、地形、象牙边框和事件 pin；下一版只重排中央地图板与底部真实日程条，不拉伸、不裁切、不生成式补绘地图，不重生左右两栏。
- **Loop Log**：`docs/plans/region-task-board-imagegen/2026-07-14-region-map-stage-unassigned-vertical-space-loop-log.md`。
