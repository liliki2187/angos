# 世界地图「夜班剪版台」内部变体 v1 交付清单

> 日期：2026-08-18  
> 当前产物类型：`visual_style_reference / filled_state_text_mock / internal_direction_demo`  
> 状态：`three_variants_generated / user_abstraction_feedback_received / overresolved_component_language_diagnostic_only`  
> 禁止升级：本轮不是 `no_text_asset_master`、`production_candidate`、atlas、manifest 资产接线或 Godot runtime 证据。

## 1. 本轮只验证什么

在用户已经淘汰「折页特刊」与「蓝光校片灯箱」、保留「夜班剪版台」之后，本轮只比较同一宏观母方向内部的三种组件语言：

1. 地图先行·初剪底稿；
2. 分色校样·套印拼版；
3. 图片编辑·单张样剪版。

冻结三栏职责、左侧三条地区选题、中央世界地图、右侧当前地区稿、左下 Schedule 与底部 CTA；不进入 Godot，不制作正式壳体，不修改现行功能合同。

## 2. 真实生图产物

所有美术图均使用 Codex 内置 ImageGen 生成或编辑。程序仅负责把内置工具输出的 `1672×941` 无裁切等比规格化为 `1920×1080`，并把三张成图排成对比板；程序没有代替生图生成美术内容。

| 编号 | 名称 | 项目内主审图 | 用途 |
| --- | --- | --- | --- |
| 01 | 地图先行·初剪底稿 | `image_gen/2026-08-18/world-map-pasteup-internal-variants-v1/01-map-first-rough-pasteup-1920x1080.png` | 完整整屏基线；验证地图主语、左栏综合色和右栏深青承载 |
| 02 | 分色校样·套印拼版 | `image_gen/2026-08-18/world-map-pasteup-internal-variants-v1/02-color-separation-proof-1920x1080.png` | 验证宽色版、套印偏移、综合色稿夹 |
| 03 | 图片编辑·单张样剪版 | `image_gen/2026-08-18/world-map-pasteup-internal-variants-v1/03-photo-editing-sample-1920x1080.png` | 验证唯一一张 selected `69:44` 校样载体与图片编辑氛围 |
| 04 | 三方案对比板 | `image_gen/2026-08-18/world-map-pasteup-internal-variants-v1/04-three-internal-variants-comparison-board-1920x430.png` | 同骨架缩略对照 |

同时保留三张 ImageGen 原始输出：

- `01-map-first-rough-pasteup-source.png`
- `02-color-separation-proof-source.png`
- `03-photo-editing-sample-source.png`

## 3. 生成锚点与不可变项

参考锚点：

- 既有 B「夜班剪版台」：`image_gen/2026-08-17/world-map-alternative-macro-style-demos-v1/02-night-newsroom-paste-up-desk-1920x1080.png`
- A291：`image_gen/2026-08-06/world-map-art-gap-demos-v1/04-final-a-c-b10-visual-target.png`
- `design/art-direction/references/clean-lowpoly-weekly-branch/benchmark-board-01.png`
- `design/art-direction/references/clean-lowpoly-weekly-branch/benchmark-board-02.png`

视觉 brief 中冻结：

- 桌面 `1920×1080`、三栏职责不重开；
- 左侧三条地区选题保持同一几何家族、同尺寸图窗；
- 中央地图至少约占中央工作区 `60%`；selected 照片不超过约 `22%`；
- 同一洗衣店图片在左卡、中央样张与右栏中只按 `69:44` 外观比例展示，不主动裁切或拉伸；
- 功能承载面保持 `0°`，独立 BackDecor 才允许轻微倾斜；
- 不新增按钮、玩法字段、热区或状态；
- 禁止杂志折页、SCP 档案、军事雷达、科幻灯箱、霓虹 HUD、红线证据网、泛黄旧档案和细碎伪写实多边形。

注意：02、03 虽以 01 为编辑母图并在 prompt 中声明只改中央＋右栏，但内置 ImageGen 会重新采样整图。本轮只把它们称为「受控视觉变体」，没有取得像素级 `scope_invariant` 通行证，也不能据此声明左栏、顶部或 Schedule 可直接复用为正式资产。

## 4. 最终提示词

### 4.1 01 地图先行·初剪底稿

```text
Use case: ui-mockup
Asset type: full-screen 1920×1080 desktop game UI visual target, filled state
Primary request: redesign the existing night newsroom paste-up desk into a much bolder map-first rough proof interface for World Mystery Weekly. Keep the exact desktop three-column responsibility structure, three equal-height region pitch items at left, a dominant world map in center, selected-region dossier and one CTA at right, and Schedule at lower left. Keep functional carriers orthogonal.
Major transformation: central world map occupies at least 60%; remove enclosed software-panel/GIS grid and giant headline strip; use broad cobalt, cold cyan, olive and mustard low-poly print regions with controlled misregistration; place exactly one small 69:44 selected laundromat proof in North America; replace identical white left cards with cobalt/olive/mustard editorial pitch strips while keeping one geometry and independent state tabs; replace the full-height white right form with a deep-teal review board holding a smaller warm-white proof; make Schedule a mustard/olive print ticket; lock header as WMW globe + masthead + ISSUE 001/WEEK 01.
Style: polished clean low-poly weekly, modern editorial paste-up, midnight slate blue, warm off-white paper, olive, mustard and restrained rust red. Use believable overlap and contact; one dry UFO/question-mark editor joke only.
Avoid: magazine/gatefold, SCP dossier, military radar, sci-fi light table, neon HUD, red-string evidence board, aged archive, travel postcard, photorealism, tiny noisy polygons, extra controls and watermark.
```

### 4.2 02 分色校样·套印拼版

```text
Use case: precise-object-edit
Image 1 is the edit target and composition master. Change only the central map working area and the inner content of the right review board; preserve the header, entire left column, Schedule, three-column geometry and outer carriers.
Create a color-separation proof variant: the map remains at least 60% and uses 3–4 broad overlapping cobalt/cold-cyan/olive/mustard print plates, with controlled 2–4 mm visual misregistration only at selected coastlines and a few registration crosses. Keep exactly one small 69:44 selected laundromat photo. On the right, preserve the deep-teal carrier but use a smaller warm-white lead proof on a muted cyan/blue under-sheet, with mustard and olive registration tabs and the existing olive CTA.
Avoid RGB/neon glow, CMYK software UI, vertical toolbars, acetate, contact sheets, full-page white forms, SCP, radar, red strings, yellowed archive paper, tiny polygons, new controls and watermark.
```

### 4.3 03 图片编辑·单张样剪版

```text
Use case: precise-object-edit
Image 1 is the edit target and composition master. Change only the central map working area and the inner content of the right review board; preserve the header, entire left column, Schedule, three-column geometry and outer carriers.
Create a photo-editing sample variant while the map remains the first subject: keep the broad low-poly map visible across at least 60%; use exactly one selected 69:44 laundromat proof no larger than 22%, with a cobalt proof mount, warm-white photo border, one paperclip, a narrow mustard caption slug and one rust-red grease-pencil mark. Connect it to North America with one short locator arc, not an evidence network. On the right, retain the deep-teal carrier and use an upper 69:44 photo proof on cobalt plus a lower compact warm-white caption/evidence strip and the existing olive CTA.
Avoid contact sheets, multiple crops, different image ratios, full-page white forms, viewfinder/eye controls, SCP, radar, sci-fi light table, neon HUD, red strings, aged archive paper, tiny polygons, new controls and watermark.
```

## 5. 双审结论与冲突合并

### UX 老哥

- 01 最不容易误导交互，`P0=0 / 可见 P1=0`；
- 02 的右侧竖向分色轨像合同外工具栏，记 `P1=1`；
- 03 最有编辑部趣味，但 Eye 图标是假按钮，且右栏内部槽位疑似重排，记 `P1=2`；
- 推荐用 01 做冻结结构底座，吸收 03 的图片校样氛围；02 只贡献综合色和套印材料。

### UI Designer

- 02 的综合色已成为左、中、右和 Schedule 的结构节拍，最接近 clean-low-poly weekly；
- 01 应作为地图占比、照片尺寸和职责主次真源；
- 03 只提供唯一一张 selected `69:44` 校样载体，不宜把图片编辑语言放大成整屏取证台；
- 推荐 `01 宏观主次 + 02 宽色版/综合色稿夹 + 03 单张校样组件`。

### 父级合并

下一张完整候选若获用户授权，应只走一条混合路线：

> 01 的地图比例与冻结 FrontCarrier  
> ＋ 02 的宽色版、克制套印和右栏综合色背页  
> ＋ 03 的唯一一张 `69:44` selected 校样载体。

必须删除 / 禁止叠加：

- 02 的竖向分色工具条；
- 03 的 Eye、取景框和右栏槽位重排；
- 顶部准星、条码等机构化身份符号；
- 01 手绘圆弧、02 定位十字、03 Eye 同时出现；
- 第二张中央照片、contact sheet、红线网络或巨型标题压图。

## 6. 当前裁决口径

三张均可用于内部风格比较；没有一张可直接进入资产化。01 是功能结构基线，02 是主风格材料证据，03 是 selected 图片组件证据。等待用户确认是否按上述混合配方生成下一张完整 `1920×1080` filled-state visual target。

## 7. 2026-08-18 用户复审修订

用户对照两张正式 benchmark 的文件夹 / 文书裁切后指出，02 的组件比标杆更完整、更精密、细节更多，综合色也缺少共同灰底。该判断覆盖本清单此前“02 最接近 clean-low-poly weekly”的扩大表述：02 只保留宽色版和跨栏综合色的诊断价值，不再作为下一张完整候选的直接主风格。下一轮必须先按 A311 削减纸层、五金、边框、校准符和微型信息，并用 benchmark 同类裁切校准综合色灰度；当前停止继续生图。
