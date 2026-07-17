# 地区任务台资产化返工生产规格

> **2026-07-16 当前支线覆盖**：本文件 2026-06-15 / 06-17 的旧像素、重半调、红青 atlas 与整屏 `rt_artboard_full` 路线仅保留为历史 fallback。当前以两张标杆和 `clean low-poly weekly` 支线为真源；执行前先读取 [`2026-07-16-region-task-board-component-cutout-preflight-v2.md`](./region-task-board-imagegen/2026-07-16-region-task-board-component-cutout-preflight-v2.md) 与 [`component_cutout_inventory_v1.json`](../../design/ui-contracts/region-task-board/component_cutout_inventory_v1.json)。E2 只作组合气质参考，从 E2 直接裁切的正式组件数为 0；与本文件旧资产名、固定五热点、整屏图优先级、逐状态生图或宽泛“约 8 类外壳”口径冲突时，以 2026-07-16 的 18-class inventory 为准。

> **状态**：2026-06-15 返工规格；2026-06-17 追加 v3 视觉锁定口径。`region-task-board-clean-pixel-v2.png` 只能作为已认可地图质感的风格源和失败链路样本；当前 v3 以 `gd_project/Assets/ui/angus_packaging/region_task/artboard_v3/rt-artboard-full.png` 作为用户认可整屏视觉锁定源和高保真恢复底图。  
> **目标**：冻结用户认可的深蓝低多边形纸质地图质感、整体配色和视觉语言，只用资产化 UI 链路解决 HUD 挤压、文字出框、框体不配套、地图标签烘焙和按钮无状态等功能落地问题。  
> **依据**：`docs/onboarding/assetized-ui-production-chain.md`、`docs/onboarding/ui-interaction-guidelines.md`、`docs/设计采纳记录.md` A51-A57、A67-A69、A82。
> **生图约束包**：`docs/plans/region-task-board-imagegen/prompt-bundle.json`

---

## 1. 当前问题定性

当前地区任务台的问题不是“坐标没调好”，而是生产链断裂：

1. **整屏图承担了太多功能**：左任务栏、右详情栏、地图标签、按钮语义被画进同一张图，后续只能靠 Godot 文字和控件硬贴。
2. **可交互对象没有拆层**：按钮、地图 pin、任务卡、筛选签没有独立状态贴图，无法稳定表达 hover / pressed / selected / disabled。
3. **动态文字没有真实安全区**：左/右纸面上的框体、书签、半调、斜边与动态文本没有共同设计。
4. **顶部 HUD 压缩主舞台**：全局信息占据过多高度，导致用户认可的地图底图比例被压扁。
5. **地图底图混入动态对象**：白色任务签、黄色提示、pin 和标签被烘焙或混层，无法按任务数量和状态复用。

结论：下一轮不继续修当前 PNG 的局部排版；应重建资产包和 manifest。

---

## 2. 视觉冻结约束

上一套图的风格、视觉、配色没有方向性问题，尤其是中间地图已经成立。返工目标不是重新设计视觉，而是把已成立的视觉拆成可交互、可复用、可维护的生产资产。

2026-06-17 v3 修订：用户已经明确认可最新整屏图的整体美术效果。地区任务台 v3 首轮落地允许把该整屏图作为 `visual_lock_backdrop` 接入 Godot，以先恢复视觉锚点和中央地图质感；但它只承担不可变背景 / 高保真恢复目标职责，不能重新把动态文字、按钮状态和可点击反馈烘焙进图。中央地图因本页功能简单，可以先保留为底图；若后续需要 pin、路线或短签的真实 hover / selected / locked / completed / urgent 状态，再叠加独立状态层或 atlas。

必须保留：

- 深海军蓝工程底板 / 编辑部地图墙气质。
- 中央地图的低多边形纸质分面、纸膜感、红青路线、半调点、裁切标记和像素颗粒密度。
- 暖白 / 浅象牙的新鲜印刷纸方向，不能回到旧档案、旧报纸、羊皮纸、茶渍或泛黄 sepia。
- 红橙用于异常 / 截稿 / 高风险，青色用于追踪 / 信号，金色只做选中 / 签批重点。
- 当前已经被认可的整体冷静、现代、杂志社工作台质感。

允许改变：

- 顶部 HUD 的高度、信息密度和布局权重。
- 左侧任务卡、右侧详情纸的结构、槽位和安全区。
- 地图 pin、短签、tooltip、按钮、筛选签的拆层方式和状态矩阵。
- 任务名、地点名、按钮文案、状态章等动态信息的承载位置。
- 为去除烘焙标签而重出“干净版地图底图”，但必须继承原地图的材质、配色、构图和颗粒语言。

禁止改变：

- 把界面换成另一套视觉主题、另一种色彩体系或另一种材质方向。
- 为了功能清晰把界面降级成普通后台面板、SaaS 卡片或通用网页按钮。
- 把中间地图重画成写实地图、旧地图、简洁扁平矢量图、低清 8-bit 图或高噪声摄影纹理。
- 因为需要拆 pin / 标签，就顺手更换地图底图的主体风格、比例、颜色和质感。
- 用“更清爽”为理由删除用户已经认可的地图质感和红青印刷关系。

验收时先问：**截图第一眼是否仍然是上一套图的视觉方向，只是功能层更干净、更可用？** 如果答案是否，即使功能拆层正确，也判定返工方向偏了。

---

## 3. 页面功能合约

地区任务台只负责一件事：

```text
在当前地区里选择一个可派遣任务，并送往派遣签批台。
```

本页显示：

- 当前地区地图。
- 当前地区可选任务 / 线索列表。
- 当前选中任务摘要；它是右侧详情纸的主要叙事正文区，默认承载 7–8 行介绍，以 9 行中文做容量压力验收。
- 任务类型、耗时、风险、截稿 / 深度链等关键状态。
- 主操作：进入派遣签批。
- 当前地区的全局日程推进：`推进一天`，但必须作为底部日程条里的全局动作，不得贴近任务主 CTA。

本页不显示：

- 候选员工列表。
- 已选员工槽。
- 完整骰池。
- 达标率拆解。
- 真正消耗天数的执行按钮。
- 结束探索周 / 进入编辑部等跨阶段按钮。

`推进一天` 是例外的日程动作：它可以出现在地区任务台，但不属于当前任务详情，也不进入右侧签批纸。它必须在底部全局日程条中显示当前派遣数、到期摘要和二次确认态，避免被误读为“当前任务确认”。

---

## 4. 桌面 16:9 布局合约

默认按 `1920x1080` 设计和验收。

```text
┌────────────────────────────────────────────────────────────┐
│ 64-72 顶部低权重频道条：刊名 / 当前周 / 剩余天数 / 五维摘要 / 返回 │
├──────────────┬────────────────────────────┬───────────────┤
│ 左 380-420    │ 中 960-1040                 │ 右 400-460      │
│ 任务档案索引   │ 地区地图底图 + pin 状态层      │ 选中任务签批摘要 │
│              │                            │               │
│ 任务卡 1      │                            │ 标题           │
│ 任务卡 2      │                            │ 摘要           │
│ 任务卡 3      │                            │ 耗时 / 风险     │
│ 任务卡 4      │                            │ 截稿 / 链条     │
│              │                            │ 主 CTA         │
└──────────────┴────────────────────────────┴───────────────┘
```

硬规则：

- 顶部 HUD 不得超过 72px；不能再做两行厚仪表盘。
- 中央地图是主视觉，比例不得因 HUD 或侧栏挤压而变形。
- 左右栏承载动态文字的纸张正面、内框、标题槽、正文槽、状态槽和按钮文字槽必须是正交矩形，边线与画布水平 / 垂直对齐。外层可以有厚度、叠页和背后斜纸，但这些只能出现在边缘或背景；不得让整张可写纸面再次倾斜。
- 地图默认态不显示常驻白牌和长标签；hover / selected 才显示短签。

### 4.1 正交纸面一票否决

地区任务台已经多次验证：斜纸面会让动态文字、按钮热区、状态槽和后续拆图全部受限。因此后续任何声称为 `filled-state text mock / 真实内容风格稿`、`no-text asset master` 或 `production_candidate` 的图，必须满足：

- 左侧四张任务卡的可写正面必须水平，不得随档案夹透视倾斜。
- 右侧详情纸的标题框、正文框、状态票据和 CTA 挂点必须水平，不得整体向左 / 右倾。
- 底部日程条和 `推进一天` 文案槽必须水平，不得跟随桌面透视倾斜。
- 可以保留背后纸叠、夹板、页脚、侧边标签、阴影和透视外框，但它们必须在 `no_text_rects` 或装饰层，不承载动态文字。
- 生图结果只要出现“可写纸面倾斜”，即使美术质感好，也必须标记为失败样本或灵感图，不能继续填字、写 manifest 或进入拆分落地。

Prompt 中不得只写 “text area orthographic”。必须显式写 “front writable paper faces must be square-on, axis-aligned, not tilted, not skewed, not in perspective; only background backing sheets may be angled”。

---

## 5. 元素归属表

| 元素 | 玩家问题 | 动态 | 交互 | 归属 | 生产要求 |
| --- | --- | --- | --- | --- | --- |
| 地区地图底图 | 当前地区空间关系是什么 | 否 | 否 | 烘焙底图 | 保留深蓝低多边形纸质质感；无 pin、无标签、无任务牌、无文字 |
| 地图路线底层 | 哪些点有关联 | 可选 | 否 / 弱交互 | 独立层 | 默认低权重；高亮路线由运行时状态层控制 |
| 地图 pin | 哪些任务可选 | 是 | 是 | 独立组件 | 统一 anchor；normal / hover / selected / locked / completed / urgent |
| 地图短签 | 当前 hover / 选中任务是什么 | 是 | 弱交互 | 独立组件 + 动态文字 | 只显示短名和状态，不显示完整说明 |
| 左任务卡 | 候选任务如何比较 | 是 | 是 | 独立组件 + 动态文字 | 卡片底、色签、状态章、文字槽分离 |
| 左筛选签 | 当前筛选是什么 | 是 | 是 | 独立组件 | default / hover / selected / disabled |
| 返回地图 | 回到上一级 | 是 | 是 | 独立组件 | 低于主 CTA，但点击面积稳定 |
| 右详情纸 | 当前任务详情是什么 | 是 | 否 | 独立组件 + 动态文字 | 正交内容区；标题、摘要、meta、特殊状态分槽 |
| 主 CTA | 下一步做什么 | 是 | 是 | 独立组件 + 动态文字 | default / hover / pressed / disabled / focus / loading |
| 日程推进按钮 | 是否推进全局天数 | 是 | 是 | 独立组件 + 动态文字 | 属于底部全局日程条；default / hover / pressed / disabled / focus / confirming；不得贴近主 CTA |
| 顶部频道条 | 当前周与全局摘要 | 是 | 少量 | 独立组件 + 动态文字 | 一行低权重，不压主舞台 |

---

## 6. 资产包清单

目标目录：

```text
gd_project/Assets/ui/angus_packaging/region_task/assetized/
```

### P0 必需资产

| asset_id | 文件建议 | 类型 | 说明 |
| --- | --- | --- | --- |
| `rt_board_shell` | `rt-board-shell.png` | 不透明底图 | 深蓝工作台 / 边框 / 裁切标记；不含功能框、文字、按钮 |
| `rt_map_base_clean` | `rt-map-base-clean.png` | 不透明或透明 | 用户认可风格的干净地区地图；无 pin、无标签、无白牌 |
| `rt_map_route_layer` | `rt-map-route-layer.png` | 透明 | 低权重路线和信号线；高亮另出状态层 |
| `rt_pin_atlas` | `rt-pin-atlas.png` | 透明 atlas | normal / hover / selected / locked / completed / urgent |
| `rt_pin_label_atlas` | `rt-pin-label-atlas.png` | 透明 atlas | hover / selected / disabled 短签底板 |
| `rt_task_card_atlas` | `rt-task-card-atlas.png` | 透明 atlas / 九宫格 | normal / hover / selected / unavailable / assigned / deadline |
| `rt_filter_tab_atlas` | `rt-filter-tab-atlas.png` | 透明 atlas | default / hover / selected / disabled |
| `rt_detail_sheet_base` | `rt-detail-sheet-base.png` | 透明或不透明 | 右侧正交签批纸，内容区干净 |
| `rt_cta_dispatch_atlas` | `rt-cta-dispatch-atlas.png` | 透明 atlas | default / hover / pressed / disabled / focus / loading |
| `rt_advance_day_atlas` | `rt-advance-day-atlas.png` | 透明 atlas | 底部全局日程推进按钮；default / hover / pressed / disabled / focus / confirming |
| `rt_hud_strip` | `rt-hud-strip.png` | 九宫格 | 顶部一行频道条 / 微仪表底 |

P0 资产的生产契约补充：

- `prompt-bundle.json` 必须逐项覆盖上表所有 P0 资产，不能漏掉 `rt_board_shell` 或 `rt_map_route_layer`。
- 所有 atlas prompt 必须写死 `target_size`、`frame_size`、`frame_order`，并与 manifest 一致。
- 所有文字承载组件必须同步写出 `content_rects`、`no_text_rects` 和 `overflow_policy`。
- 所有可点击组件必须同步写出 `hit_rect`、`hover_rect`、状态帧和 `feedback_spec`。
- 同一决策事实只能有一个主承载位：主 CTA 的 label 和按钮状态只归 `rt_cta_dispatch_atlas`；右详情纸只保留 CTA 挂点和阻断原因槽。
- 地图路线主承载位必须明确：干净地图底图只能保留低权重不可交互纹理，正式路线高亮和状态路线归 `rt_map_route_layer` 或 Godot runtime layer。

### P1 可选资产

| asset_id | 说明 |
| --- | --- |
| `rt_deadline_stamp_atlas` | 截稿 / 突发任务状态章 |
| `rt_chain_badge_atlas` | 深度链 / 追踪状态章 |
| `rt_risk_badge_atlas` | 风险 / 凶险 / 锁定标识 |
| `rt_empty_state_note` | 未选中任务时的空白批注纸 |
| `rt_selection_thread` | 左任务卡与地图 pin 的选中连线或归属线 |

---

## 7. 交互状态矩阵

| 组件 | default / normal | hover | pressed | selected | disabled / locked | loading / active |
| --- | --- | --- | --- | --- | --- | --- |
| 主 CTA | 可进入签批 | 亮边 / 轻抬 | 下沉 2px / 印章压下 | 不适用 | 灰纸 / 禁用原因 | 短暂签批中 |
| 返回地图 | 低权重可点 | 边框增强 | 下沉或暗化 | 不适用 | 不可用时隐藏或灰化 | 不适用 |
| 任务卡 | 可选任务 | 纸张抬起 / 侧签亮 | 轻压 | 金色或青色选中归属 | 灰纸 / 锁 / 已派遣 | 执行中下沉到次级队列 |
| 地图 pin | 小图钉 / 锚点 | 放大或发光 | 轻压 | pin + 短签展开 | 灰 pin / 锁态 | 可选，显示执行中 |
| 地图短签 | 默认隐藏 | hover 出现 | 不单独 pressed | selected 常驻 | disabled 只解释原因 | 不适用 |
| 筛选签 | 可点 | 轻亮 | 下沉 | 选中底板 | 禁用灰化 | 不适用 |
| 日程推进按钮 | 全局日程动作 | 亮金边 / 日历高亮 | 下沉 2px | 不适用 | 灰化并说明不可推进 | confirming 显示 `确认推进？`，再次点击才执行 |

状态验收要求：

- 每个状态文字仍在同一 `content_rect`。
- pressed 必须有可见反馈，不只触发代码事件。
- disabled 必须一眼不像可点击对象。
- selected 必须同时在左任务卡、地图 pin、右详情形成一致反馈。

---

## 8. Manifest 最低规格

建议文件：

```text
gd_project/Assets/ui/angus_packaging/region_task/region_task_asset_manifest.json
```

每个组件至少声明：

```json
{
  "id": "rt_cta_dispatch",
  "role": "primary_cta",
  "asset_paths_by_state": {
    "default": "assetized/rt-cta-dispatch-default.png",
    "hover": "assetized/rt-cta-dispatch-hover.png",
    "pressed": "assetized/rt-cta-dispatch-pressed.png",
    "disabled": "assetized/rt-cta-dispatch-disabled.png",
    "focus": "assetized/rt-cta-dispatch-focus.png",
    "loading": "assetized/rt-cta-dispatch-loading.png"
  },
  "base_size": [320, 64],
  "nine_slice": [20, 20, 16, 20],
  "content_rects": {
    "label": [44, 12, 214, 38]
  },
  "no_text_rects": {
    "arrow": [268, 10, 34, 42],
    "bottom_stripe": [0, 54, 320, 10]
  },
  "hit_rect": [0, 0, 320, 64],
  "hover_rect": [-6, -6, 332, 76],
  "anchor_points": {
    "tooltip": [160, -8]
  },
  "states": ["default", "hover", "pressed", "disabled", "focus", "loading"],
  "feedback_spec": {
    "pressed_offset": [0, 2],
    "pressed_duration_ms": 90,
    "sound": "stamp_soft"
  },
  "overflow_policy": {
    "label": "ellipsis"
  },
  "qa_cases": ["long_label", "disabled_reason", "pressed_frame"]
}
```

地图 pin 还需声明：

```json
{
  "anchor_point": [24, 52],
  "hit_rect": [-18, -54, 36, 58],
  "label_anchor": [18, -46],
  "collision_radius": 72
}
```

任务卡还需声明：

```json
{
  "content_rects": {
    "title": [72, 16, 260, 28],
    "meta": [72, 48, 270, 42],
    "status": [294, 14, 54, 28]
  },
  "no_text_rects": {
    "left_tab": [0, 0, 54, 116],
    "bookmark": [326, 0, 34, 46],
    "halftone_corner": [286, 76, 70, 34]
  }
}
```

---

## 9. 生图 Prompt 硬约束

### 9.1 地图底图

必须：

- 以当前用户认可的中间地图为视觉锚点，保留深海军蓝、低多边形、纸质分面、红青路线、半调和高清微像素颗粒。
- 只做功能清洁版：去掉烘焙 pin、白牌、黄色提示和动态标签，不能换地图风格。
- 地图无文字、无地点名、无任务牌、无 pin、无黄色 tooltip、无空白白签。
- 路线和氛围信号只低权重存在，不像可点击节点；正式路线高亮另交给 `rt_map_route_layer` 或运行时层。
- prompt 固定使用 “derive / retouch from approved map / same composition / same land silhouette / same camera/proportion”，避免模型理解成重画新地图。
- `rt_map_base_clean` 不得由程序化多边形、PIL / Canvas / SVG 白盒绘图、简化矢量大陆或调试网格图替代；本地脚本只能做裁切、尺寸校验、打包、透明路线层或白盒对照，不能重画正式地图主体。

禁止：

- 写实旧地图、旧档案、泛黄纸、羊皮纸、旧报纸、茶渍。
- 新配色、新地图构图、新 UI 主题或明显不同于上一套图的材质。
- 程序化低保真地图、白盒占位地图或调试网格图写入正式 `assetized` 目录。
- 假任务标签、假按钮、假可点击框。
- 把地图点、白牌和任务名烘焙进去。

### 9.2 左任务卡 / 右详情纸 / CTA

必须：

- 使用干净暖白 / 浅象牙的新鲜印刷纸。
- 内容区正交、水平、低噪声。
- 每个动态文字槽有至少 32px 视觉安全边距，或按组件尺寸等比例给出稳定边距。
- 装饰只在 `no_text_rects` 中。
- CTA 文案只允许出现在独立 CTA 组件的 `content_rects.label`；右详情纸不得再定义 `cta_label`，只能定义 `cta_mount` 和 `blocking_reason`。
- 禁用原因不得挤进按钮 label；放到右详情阻断原因槽或 tooltip。
- 右详情纸优先把任务标题与 CTA 之间的弹性高度分配给摘要正文；默认不显示框内滚动条、不缩字。地点 / 耗时、风险 / 链条保持为独立短事实块并稳定可见，摘要超过 9 行时另走 `展开全文` 阅读层。

禁止：

- 大角度斜透视正文面。
- 内框线、半调点、折角穿过未来正文。
- 把标题、任务名、按钮文案画进图。
- 通用 SaaS / 网页按钮质感。

---

## 10. Godot 接入要求

当前代码状态：

- `WeeklyRunExplorePhase.gd` 通过 `load_region_task_texture("region-task-board-clean-pixel-v2.png")` 加载单张整屏背景。
- `RegionMapCanvas` 在启用该图时被隐藏，地图信息依赖背景图。
- pin、CTA、任务卡部分仍用 `StyleBoxFlat` 临时样式。
- 左右栏通过现有 `PanelContainer` 和文本控件硬贴到背景区域。

返工后应改为：

1. 新增 `region_task_asset_manifest.json`。
2. 新增类似 `WeeklyRunWorldMapAssetManifest.gd` 的 `WeeklyRunRegionTaskAssetManifest.gd`。
3. `WeeklyRunUiStyle.gd` 增加 region task assetized 读取入口，按 manifest 加载 atlas frame。
4. `WeeklyRunExplorePhase.tscn` / `WeeklyRunExplorePhase.gd` 不再把整屏 PNG 作为功能底图；改成：
   - 底层 `rt_board_shell`；
   - 中央 `rt_map_base_clean`；
   - 独立 `NodePinLayer`；
   - 左侧 task card 组件列表；
   - 右侧 detail sheet 组件；
   - 独立 CTA TextureButton / Button texture style；
   - 底部全局日程条与独立 `rt_advance_day_atlas` TextureButton；
   - 顶部 HUD strip。
5. 所有动态文字由 Label / RichTextLabel 渲染，但位置必须来自 manifest `content_rects`。
6. 所有可点击对象使用 manifest `hit_rect`，不可用状态不能保留手型 cursor。
7. 点击、hover、pressed、selected、disabled 状态必须来自状态贴图或运行时状态层，不再靠一张图 modulate 硬改。
8. 旧的 `region_task_v2` StyleBoxFlat 临时样式只能作为 fallback，不作为最终生产路径。

---

## 11. 验收计划

### 11.1 自动校验

需要新增或扩展脚本，至少检查：

- manifest JSON 结构有效。
- 每个必需 asset_id 和 state frame 都存在。
- prompt bundle 逐项覆盖 P0 资产，且 atlas 的 `target_size`、`frame_size`、`frame_order` 与 manifest 一致。
- PNG 尺寸符合 manifest。
- `content_rects` 不与 `no_text_rects` 相交。
- `hit_rect` 覆盖视觉对象主体，但不覆盖相邻对象。
- 主承载唯一：右详情纸无 `cta_label`，CTA label 只在 `rt_cta_dispatch_atlas`。
- 动作分离：`rt_cta_dispatch_atlas` 与 `rt_advance_day_atlas` 均存在，且 `advance_day_button` 的默认 runtime rect 不在右侧详情纸内；二者 hit rect 不相交、不相邻、不共享红色签批语法。
- 地图对象分离：`rt_map_base_clean` 禁止 baked pins / labels / tooltip，pin atlas 声明 `anchor_point`、`label_anchor`、`collision_radius`。
- QA case 覆盖长标题、两位数截稿、disabled CTA、hover/pressed、空态和满态。
- 任务卡长标题、两行 meta、截稿状态、已派遣状态不会超过可写区。

### 11.2 截图验收

必须覆盖桌面 16:9：

- `1920x1080` 主验收。
- `1600x900` 和 `1366x768` 回归验收。

状态截图：

0. 视觉冻结对照：新版默认态与上一套图并排检查，中间地图、配色、纸质、红青关系必须明显同源。
1. 默认未选中：地图无白牌噪音，左任务卡可读，右侧为空态。
2. hover 地图 pin：短签就近出现，不遮挡路线和邻近 pin。
3. 选中普通任务：左卡、地图 pin、右详情同步选中。
4. 选中截稿 / 突发任务：红色状态章进入专属槽，不挤压 meta。
5. 选中深度链任务：青色追踪状态进入专属槽，不与截稿混用。
6. CTA disabled：按钮不像可点，显示短阻断原因。
7. CTA pressed：按钮有下沉 / 压章 / 明暗变化。
8. 推进一天确认态：按钮位于底部全局日程条，第一击进入确认态，不和右侧任务 CTA 构成连续点击区。
9. 长标题压力测试：标题省略但不贴边、不压书签、不穿半调。

### 11.3 人工复审

交付前按顺序复审：

1. 当前 `clean low-poly weekly` 支线按 A180 临时例外，直接用两张标杆、支线风格规范、纸面 / 色彩合同和失败样本逐项复审；不自动调用旧像素坐标系的 `angus_art_director`。其他 Angus 像素 / 半调支线以及用户显式点名不受影响。
2. `ui_designer`：布局和组件清单是否能承载 1920x1080 桌面 UI。
3. `ux_laoge`：玩家是否能理解任务选择、选中反馈、返回层级和进入派遣主操作。

---

## 12. 返工执行顺序

建议分三步，不再一次性做整屏大图：

### Step 0：落地前全组件评估与纵向切片准入（2026-07-15 新增）

在任何新一轮裁切、批量生图或 Godot 全量接入前，必须先完成：

1. 以冻结的 1920×1080 黑白功能框为几何真源，不从完整风格稿反推坐标。
2. 为 HUD、左任务索引、地图图钉、dossier、派遣 CTA、推进一天和日程条分别登记功能、状态、visual / layout / clip / hit rect 与文本安全区。
3. 将每个组件归入“复用原图 / Godot 原生构造 / 生图无字母版 / 退役旧资产”四类，不允许把整屏风格稿直接挖成 atlas。
4. 建立 `region_task_asset_manifest_v2.json` 与 `design/ui-contracts/region-task-board/`；旧固定五热点 manifest 不得沿用。
5. 先跑“地图 + 0–N 事件图钉 + dossier 真实摘要 + 固定底部 CTA”纵向切片。切片未通过，不得批量生成任务卡、按钮状态或同类实例。

完整坐标、组件清单、生产难度与放行证据见 2026-07-15 落地前评估报告。

### Step 1：资产规格与干净地图

- 产出 `rt_board_shell`。
- 产出 `rt_map_base_clean`。
- 产出 `rt_map_route_layer`，明确它是正式路线和路线高亮的承载位。
- 以当前中间地图为强参考，只清除烘焙标签和交互对象，不改配色、质感和主体构图。
- 产出 `rt_pin_atlas` 和 `rt_pin_label_atlas`。
- 接入 map + pin 状态层。
- 验收地图不再有烘焙标签和奇怪方块。

### Step 2：左右栏组件化

- 产出 `rt_task_card_atlas`。
- 产出 `rt_detail_sheet_base`。
- 接入任务卡、右详情安全区。
- 验收长标题、meta、截稿、深度链。

### Step 3：HUD 和主 CTA 状态化

- 压缩顶部 HUD 到 64-72px。
- 产出 `rt_cta_dispatch_atlas` 和 `rt_hud_strip`。
- 接入 hover / pressed / disabled / loading。
- 验收主舞台比例、按钮反馈和三状态截图。

每一步都要真实截图，不等全部完成后再验收。

---

## 13. 通过标准

本轮彻底解决问题的标准：

- 新版第一眼仍继承上一套图的视觉、配色和中间地图质感，没有换方向。
- 地图底图仍保留用户认可的风格和比例。
- 地图底图不含任何任务标签、pin、白牌、tooltip 或动态信息。
- 地图、左任务索引、右详情纸、底部回执 / 装饰各自有明确 visual rect、layout rect、clip rect 和 hit rect；地图不得堆叠、压住或穿入右栏、底部纸条和 CTA。
- 顶部 HUD 不再压缩主舞台。
- 左侧任务卡和右侧详情的文字只落在 manifest 安全区。
- 右侧正文区正交，不再受斜纸限制。
- 主 CTA 是独立动作组件，视觉底板、label、hit rect、hover / pressed / disabled / loading 反馈属于同一个组件，不得由底图装饰、白条和浮字拼成。
- `推进一天` 是独立全局日程组件，拥有自己的 atlas、hit rect、hover / pressed / disabled / confirming 状态，不得放在主 CTA 下方或共用红色签批托盘。
- 主 CTA、返回、筛选、任务卡、地图 pin 全部有可验证状态。
- pressed / disabled / selected 能被截图看出来。
- Godot 控件通过、视觉安全区通过、交互状态通过三者同时满足。

未满足以上标准时，只能称为临时止血版或风格草图，不能称为生产级地区任务台。

---

## 14. 2026-07-15 clean low-poly 支线生产覆盖

### 14.1 资产路线

- 地图：复用 2026-07-14 已选“地标节奏”原图，不重新生成简化地图，也不从整屏 mock 裁切。
- HUD、动态文字、数字、路线、分隔线、日程摘要与命中反馈：Godot 原生构造。
- 左栏壳、任务卡、图钉、短签、dossier 壳、状态章、派遣 CTA、推进一天和日程信息板：只生产无字母版；一类一母版，状态由运行时派生。
- 当前完整风格稿：只作为组合气质与默认选中态参考，不是生产位图或几何真源。
- 旧 `assetized/` 红青像素 / 半调资源与 prompt bundle v1：保留审计，不作为本支线生产输入。

### 14.2 运行时阻断

- `WeeklyRunExplorePhase.gd` 当前优先应用 `rt_artboard_full` 并提前返回；接入纵向切片时必须移除这条对新资产链的遮蔽。
- `WeeklyRunUiStyle.gd` 当前按旧多状态 atlas 与旧 asset_id 读取；manifest v2 必须支持单母版、运行时状态层与动态 0–N 图钉。
- 旧 manifest 的五个固定 `hotspots` 与 A204 冲突，不能只改坐标继续使用。
- `assetized/.gdignore` 对当前 `Image.load_from_file` 自定义加载器不是直接阻断；只有迁移到 Godot 导入资源 / Texture2D / tscn 路线时才同步处理。

### 14.3 放行边界

在 2026-07-15 评估报告列出的 manifest v2、`task_id` 一致性、7 / 8 / 9 行文本压力、0 / 1 / N / 密集图钉、CTA 底部锚定和状态矩阵证据完成前，结论一律保持“允许纵向切片，不允许批量生产”。

---

## 15. 2026-07-15 v2 运行纵向切片落地结果

### 15.1 已落地

- 新增 `region_task_asset_manifest_v2.json` 与 `design/ui-contracts/region-task-board/`，旧五热点表不再参与新切片。
- 地图直接复用已选 clean-lowpoly 原图，只承担地区地貌与静态地标；任务卡、图钉、短签、摘要与 CTA 全部由 `payload.nodes` / 当前任务 payload 动态生成。
- 左侧任务卡与地图图钉共享 `task_id`；已通过 0 / 1 / N、同坐标密集五点避让和“只保留一个常驻选中标签”测试。
- 右侧摘要使用独立可滚动正文区，已通过 7 / 8 / 9 行文本压力；地点 / 耗时、风险 / 链条与底部派遣 CTA 不被正文挤占。
- 右侧 CTA 已接回现有派遣流程；未选中时禁用，选中后可进入原派遣页。
- 1920×1080 与 1600×900 已完成真实 Godot 运行截图；几何叠线证明五大区与冻结合同一致。

### 15.2 有意未接入

- `推进一天` 仍停留在左下冻结位置并保持禁用。原因不是 UI 未做，而是当前玩法层没有独立“推进一天”命令；不得用结束探索或无效果按钮冒充。启用前必须先补玩法语义、确认态、后果预览与 GDD 同步。
- 当前任务卡、图钉、dossier 和 CTA 是 Godot 原生运行骨架，用于验证数据、位置和交互，不是最终无字美术母版，也不是 production candidate。
- `1366×768`、键盘全链、最终 hover / pressed 动效、最终一类一母版与 atlas 仍在下一阶段验收范围。

### 15.3 当前放行判断

- 原 Step 0 阻断项中的 manifest v2、动态 `task_id`、0 / 1 / N / 密集点位、7 / 8 / 9 行摘要、CTA 底边锚定与旧 `rt_artboard_full` 遮蔽已解除。
- 放行“按组件制作无字母版并逐类替换运行骨架”，仍不放行整屏裁切、同类批量生图、全量 atlas 或生产候选命名。
- 运行纵向切片的 Router Card 与 Delivery Manifest 位于 `docs/plans/region-task-board-imagegen/`；真实截图位于 `docs/screenshots/2026-07-15-region-task-board-runtime-v2/`。
