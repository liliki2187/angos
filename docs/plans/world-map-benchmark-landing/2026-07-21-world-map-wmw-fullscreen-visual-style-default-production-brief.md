# WMW v5.1 默认态整屏美术风格稿 Production Brief

## 判定

- `artifact_type = filled_state_fullscreen_visual_style_mock`
- `canvas = 1920x1080`
- `state = default`
- `status = v0_3_left_axis_corrected_ui_ux_pass_pending_user_style_decision`
- `target_only = true`
- `not_runtime = true`
- `not_formal_contract = true`
- `not_atlas = true`

进入本轮时为 `P0=0 / P1=2 / P2=0`；两个 P1 均为阶段问题：孤立 `schedule_gate` 无法证明整屏符合 WMW 标杆，且当时没有一张经用户认可的 1920×1080 完整正式美术风格稿。v0.1 因左栏双 carrier 被用户否决；v0.2 清除双 carrier 后又因日程器与三卡不同轴被用户否决。v0.3 已按 A244 将四个左栏外壳统一为 `x=66,w=306,right=372,center=219`，UI / UX 复核均为 `P0=0 / P1=0 / P2=0`；是否成为正式整屏视觉基准仍等待用户裁决。组件扩产继续暂停。

## 输入权限

### 唯一布局与容量真源

`docs/prototypes/world-map-wmw-black-white-structure/black-white-full-map-v5-1-default.png`

它独占决定三栏职责、全部 rect、内容容量、默认态文案、地图无路线、左下日程器与 A5.1-H 四任务 / 底锚 CTA。

### 视觉基因真源

- `design/art-direction/references/clean-lowpoly-weekly-branch/benchmark-board-01.png`
- `design/art-direction/references/clean-lowpoly-weekly-branch/benchmark-board-02.png`

两张 benchmark 只提供：现代 clean low-poly weekly、深色负空间、哑光彩色块面、薄而干净的纸、概括低多边形插画、克制 olive / teal / warm paper / rust、正交平视编辑拼贴。

不得复制 benchmark 的版式、英文标题、文件夹堆、回形针、CD、贴纸墙、办公桌或其他不存在于 v5.1 的物件。

### 局部形式输入

- B2.12：只继承照片、标题 plate、selected / locked 状态身份与卡内语法。
- compact A5.1：只继承照片、正文、原位 disclosure 与唯一 CTA 的局部语法。
- A5.1-H：按 v5.1 显示连续全高纸页、四任务与底锚 CTA，不反向修改 compact A5.1。
- `schedule_gate v0.1`：只保留为低权重材料 / 分层技术实验，不决定整屏纸色、边框粗细或正式美术方向，也不得直接整块嵌入。
- 旧 575：只可参考局部配色与深色地图倾向，不得恢复跨栏底票据、符号库存或旧宿主结构。

## 冻结几何

| 模块 | 1920×1080 rect |
| --- | --- |
| 左栏责任区 | `[36,24,342,1032]` |
| 北美卡 | `[66,36,306,240]` |
| 东亚卡 | `[66,294,306,240]` |
| 太平洋卡 | `[66,552,306,240]` |
| 日程器 | `[66,810,306,246]`（A244 修订） |
| 中栏责任区 | `[402,24,972,1032]` |
| 中栏标题区 | `[426,24,924,72]` |
| 地图主场 | `[426,96,924,936]` |
| 右侧 A5.1-H | `[1398,24,480,1032]` |
| 右栏标题 plate | `[1521,87,333,51]` |
| 69:44 地区照片 | `[1431,171,414,264]` |
| 地区正文 | `[1431,456,414,135]` |
| 任务情报头 | `[1425,609,426,66]` |
| 四任务区域 | `[1431,681,414,248]` |
| 任务行 01–04 | `x=1431,w=414,h=56,y=681/745/809/873` |
| 唯一地区 CTA | `[1425,957,426,75]` |

不得改变列宽、间距、模块顺序、任务容量、照片比例、地图高度、CTA 坐标或日程器高度。不得新增地图图例、筛选器、世界新闻、第三回执、快捷按钮、袋口、后页或右下无框空白。

## 默认态真实内容

### 全局

- `WORLD MYSTERIES WEEKLY`
- `WEEK 01`
- 同一 `selected_region_id = north_america` 驱动左卡、地图与右栏。

### 左栏

- 北美禁区带：选中。
- 东亚神秘地带：锁定。
- 太平洋失航带：锁定。
- 日程：当前第 1 天、剩余 7 天、推进到下一天、当前无任务到期、日程归零进入编辑部。
- 只展示默认态，不展示 confirming rust。

### 中央地图

- 北美 pin：选中。
- 东亚 pin：锁定。
- 太平洋 pin：锁定。
- 无路线、无图例、无筛选器、无假事件点、无雷达圈。

### 右栏

- 地区：`北美禁区带`
- 正文一：`都市传说与军事封锁交叠。`
- 正文二：`军方巡逻、档案残页与异常雷达同时露头。`
- 摘要：`常驻 2 · 限时 1 · 深链 1`
- 展开状态：`已展开 4 / 4`

四条任务：

1. `51 区外围公路` / `科学纪实 · 耗时 2 天` / `常驻`
2. `罗斯威尔档案残页` / `科学纪实 · 耗时 1 天` / `常驻`
3. `突发：雷达异常光点` / `大众热度 · 耗时 2 天` / `限时至第 4 天`
4. `M330 末班车空白段` / `神秘玄学 · 耗时 2 天` / `深链`

唯一 CTA：`进入地区任务台 →`

不得恢复“红线升温”。

## 整屏视觉权重

第一眼顺序：

1. 中央世界地图与北美选中点。
2. 右栏北美照片、地区身份和任务情报。
3. 右下唯一地区 CTA。
4. 左侧三张地区索引卡。
5. 左下低权重日程器。

注意力目标：中央地图约 55%–60%，右侧档案约 25%–30%，左侧索引与日程约 15%–20%。日程动作区不得比右下 CTA 更亮、更饱和或更厚重。

## 色材系统

| 角色 | 建议范围 | 用途 |
| --- | --- | --- |
| `dark_board` | `#16191C`–`#191C1E` | 全局底与地图主场 |
| `ink_dark` | `#191E1F`–`#272A2B` | 文字、细边、分隔 |
| `warm_paper` | 以 `#B7A488` 为中心 | 档案、日程与信息纸面 |
| `paper_mid` | `#B2AB9B`–`#BCB4A5` | 次级卡面与正文 carrier |
| `ivory_edge` | 接近 `#C0B9B3` | 照片边、薄纸边、图标井 |
| `olive_mid` | `#4E623D`–`#5B6A37` | 选中、主 CTA、少量重点 |
| `olive_dark` | `#3F4C2D`–`#435737` | 日程次级动作、暗分面 |
| `teal_dark` | `#293C41`–`#384946` | 地图冷色面与信息辅助 |
| `warning_rust` | `#6D462D`–`#8A4E32` | 真实限时短标识 |
| `disabled_gray` | 接近 `#686554` | 锁定状态 |

禁止纯白、死黑、饱和橙、亮黄绿、泛黄档案、sepia、奶油纸、污渍、折痕、破损、高清摄影噪声、重半调、旧报纸颗粒、密集小三角、GIS 网格、雷达 HUD、平均铺满强调色和无功能办公装饰。

## 地图主场

- `[426,96,924,936]` 是整屏视觉核心。
- 底色使用深 navy-charcoal，不使用白纸地图。
- 大陆保持 v5.1 位置与比例，每块主要区域仅 3–5 个宽面 low-poly 明度层。
- 非选中陆地使用 slate / teal-gray；北美只做克制 olive wash。
- 北美 pin 使用最清晰的 ivory / olive 对比；东亚和太平洋使用灰阶锁定。
- 地区名、pin、锁与选中环后置。
- 地图底边只做非交互版面收束；不画路线、图例、刻度、假事件点或雷达圈。
- 如需辅助线，只允许 4–6 条极低对比编辑注册线，不得读成 GIS 网格。

## 左右栏规则

### 左栏

- 三张卡统一纸边和阴影方向；selected 用 olive，locked 用低饱和灰。
- 地区照片身份固定，不随状态换图。
- 日程器使用更暗、更低饱和的 olive；纸面安静；不抢右侧 CTA。

### 右栏

- 一张连续全高档案纸，无袋口、后页或文件夹叠层。
- 69:44 照片为右栏第一视觉锚点。
- 正文、任务头和四任务连续向下，CTA 固定到底部。
- 任务行是信息行，不做成四个同权重按钮。
- 限时只在第三行小 tag / 短边条使用 rust；深链只用克制暗色标识。
- 右下 CTA 使用整屏最明确的 olive 和最高文字对比。

## 纸张、阴影与边框

- 全部功能面保持 0° 正交平视。
- 纸面低多边形只做宽面明度变化，文字安全区无强分界。
- 大纸允许一个下右偏移阴影，建议 `[6,8]`、alpha 25%–30%；小卡 `[4,5]` 同向。
- 禁止多重阴影、柔光、霓虹、厚浮雕、玻璃质感。
- 1920 下以 1–2px ink 边为主，不把 schedule 实验的粗黑框扩成全屏语言。
- 允许轻微切角，但不得侵入任何内容 carrier。
- 图片只用薄 ivory rim，不做倾斜 Polaroid 墙。

## Imagegen 与程序职责

### Imagegen

生成一张完整无字整屏视觉提案源，用于解决：全屏深浅、地图与纸面色重、地图 / 地区照片 / 档案纸的共同语言、三栏属于同一个 WMW 世界的感觉。不得含可识别文字、数字或 UI 图标。输出不是几何真源。

### 程序装配

- 按冻结 rect 恢复最终 1920×1080 canvas 与全部 carrier。
- 从生成源提取 / 采样材质、地图色面与照片气质。
- 把 imagery 裁入精确照片和地图 mask。
- 重画正交边框、纸边、分隔线与阴影。
- 清除假字、假图标、假按钮和假路线。
- 后置全部真实中文、数字、pin、锁、badge 与 CTA。
- 检查文字 bbox 与 safe rect，另行输出 audit；玩家视图不得出现 QA 信息。

## 最终 imagegen prompt

```text
Use case: ui-mockup
Asset type: no-text 1920×1080 desktop game UI visual-style proposal

Input images:
- Image 1 is the only geometry and information-capacity reference. Preserve its three-column hierarchy, world-map dominance, left card stack with bottom schedule, and right full-height dossier with four visible mission rows and bottom CTA. Do not copy any visible text, numbers, icons, audit labels, grid labels, or grayscale styling.
- Images 2 and 3 are visual-DNA references only. Use their modern clean low-poly weekly editorial language, dark navy board, muted warm paper, olive/teal restraint, broad matte value planes, and crisp orthographic paper construction. Do not copy their composition, English wording, folders, CDs, office supplies, clips, sticky notes, desks, or decorative object collections.

Primary request:
Create one cohesive full-screen World Mysteries Weekly visual-style proposal for a 1920×1080 desktop game screen. It must read as one mature investigation-weekly interface, not as three unrelated component experiments.

Composition:
Strictly front-facing orthographic 2D interface.
Left narrow region index with three stacked photo cards and a compact schedule panel at the bottom.
Large central dark world-map stage as the dominant visual field.
Right full-height single dossier sheet with one 69:44 region photo, region description area, one mission-intelligence header, four expanded mission rows, and one bottom primary CTA.
Keep broad negative space in the central map.
No route lines.

Visual hierarchy:
The central dark map is the first focal area.
The right dossier photo and mission content are second.
The bottom-right CTA is the strongest action.
The left cards and schedule are lower visual weight.
The schedule action must not compete with the bottom-right CTA.

Style:
Modern clean low-poly weekly editorial UI.
Deep navy-charcoal board, restrained warm gray-beige paper, muted olive primary accents, dark teal/slate map planes, tiny rust accents only where a real deadline would exist.
Use 3–5 broad low-poly planes per major object or landmass.
Writable paper and text-carrier areas must remain calm and low-detail.
Thin paper edges, crisp restrained offset shadows, matte materials.

Map:
Dark navy map board with broad simplified continent silhouettes and large low-poly value planes.
North America visually selected with restrained olive emphasis.
East Asia and Pacific remain muted and locked.
No route lines, radar circles, event networks, GIS overlays, legends, filters, or decorative markers.

Constraints:
No readable text, letters, numbers, punctuation, icons, arrows, lock symbols, button labels, watermarks, audit marks, TARGET_ONLY labels, bounding boxes, or QA annotations.
No perspective, tilt, isometric view, desk scene, wall scene, office environment, folders piled outside the defined panels, clips, tapes, CDs, sticky notes, stamps, hands, stationery, or physical-object collage.
No yellowed archive paper, sepia, old newspaper, dirt, stains, folds, tears, scratches, heavy halftone, pixel art, dense triangulation, glossy sci-fi HUD, neon, glass, GIS map, or fake route lines.
Do not add any UI element absent from the geometry reference.
```

## 用户只看一张图、判断五项

第一轮只展示一张无 QA 标记、真实中文内容填充的 1920×1080 默认态完整玩家视图。不同时展示材料板、atlas、geometry overlay、多候选、局部 schedule 大图、imagegen 原图或中间图。

用户只判断：

1. 整体是否像 benchmark 指向的 WMW，而不是通用 dashboard、旧报纸或档案软件。
2. 中央地图是否是真正主场，左右栏是否完整但不抢地图。
3. warm paper / dark board / olive / teal / 少量 rust 是否统一且现代。
4. 北美选中、两个锁区、日程、四任务和唯一 CTA 是否一眼分清职责。
5. 是否愿意把此图作为后续组件资产化与有色回填的整屏风格基准。

## 默认态通过后的 confirming 回归

- 复用同一完整无字底图和相同 master hash。
- 左卡、地图、右栏、照片、任务和 CTA 全部不变。
- 只在日程器 `[36,810,342,246]` 内切换文字、`!` 与局部 rust 状态层。
- 默认 / confirming 的整屏差异区外像素必须为 0。
- 不重新调用 imagegen；confirming 只作为状态回归，不是新风格方案。

## 当前边界

- built-in imagegen 已按本 brief 的最终 prompt 生成完整无字视觉提案源；程序只负责按 v5.1 rect 装配、后置真实文字 / pin / 任务 / CTA 与几何审计。
- clean-low-poly weekly 临时例外继续生效，不调用旧像素 / 半调 `angus_art_director`。
- 不制作单组件 atlas，不修改 Godot，不升级正式合同，不批量生产其他组件。
