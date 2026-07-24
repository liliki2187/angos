# WMW 1920×1080 完整整屏 Art Pass v0.4 Production Brief

## 判定

- `artifact_type = fullscreen_art_pass_filled_state_mock`
- `canvas = 1920x1080`
- `state = default`
- `status = executed_rejected_by_user_art_identity_mismatch_layout_retained`
- `functional_input = wmw-fullscreen-default-filled-style-v0-3.png`
- `v0_3_role = filled-state functional assembly / geometry and real-content evidence`
- `not_runtime = true`
- `not_formal_contract = true`
- `not_atlas = true`

v0.3 不再承担美术风格候选。它只证明三栏职责、真实内容容量、文字安全区、无路线、左栏共轴和状态语义。v0.4 必须以完整整屏 imagegen art pass 解决卡框、按钮、纸面、阴影、切角和整屏材质统一，不能继续用程序纯色矩形冒充完成度。

## 布局候选

左栏外壳从 v0.3 的 `x=66,w=306` 重新打开；v0.4 候选采用：

| 模块 | Rect |
| --- | --- |
| 卡 1 | `[30,36,348,240]` |
| 卡 2 | `[30,294,348,240]` |
| 卡 3 | `[30,552,348,240]` |
| 日程器 | `[30,810,348,246]` |

四外壳统一 `left=30 / right=378 / center=204`，三段垂直间距均为 18px。

对称关系：

- 左栏右缘到中心责任区 `[402,...]`：24px。
- 中心责任区右缘 `[1374,...]` 到右栏 `[1398,...]`：24px。
- 左栏右缘到地图主场 `[426,...]`：48px。
- 地图主场右缘 `[1350,...]` 到右栏：48px。

中央地图 `[426,96,924,936]` 与右档案 `[1398,24,480,1032]` 的职责、rect 和容量保持不变。

## 左卡内部

以每张卡 y 为基准：

- Photo：`[42,y+12,324,144]`
- Footer：`[42,y+156,324,72]`
- Title safe：`[48,y+166,224,48]`
- Status：`[284,y+166,80,48]`

## 日程内部

- Label：`[42,812,116,14]`
- Date：`[46,826,316,48]`
- Current：`[58,836,132,28]`
- Remaining：`[218,836,132,28]`
- Action：`[42,884,324,100]`
- Icon well：`[56,899,70,70]`
- Title：`[144,898,210,34]`
- Subtitle：`[144,942,210,24]`
- Info 1：`[46,992,316,24]`
- Info 2：`[46,1020,316,24]`

## Art Pass 职责

- 真实生成一张完整无字 1920×1080 整屏视觉源，不生成孤立组件。
- 生成卡框切角、照片窗 rim、单层阴影、暖纸 Footer、状态块、日期纸、推进按钮、图标井、后果纸面、右侧档案与地图的共同材质语言。
- 纸面使用克制的宽面 low-poly 明度变化，不能是纯色矩形，也不能出现污渍、旧报纸颗粒、placeholder、假字或办公物件。
- selected 使用 olive，locked 使用灰橄榄；日程动作、任务 tag 与右下 CTA 属于同一材质系统，但 CTA 继续是唯一最强动作。
- 中央地图保持第一视觉中心，右档案第二，左栏不再过度内缩。

## 程序职责

- 恢复全部候选 rect、裁切 mask 与真实地区照片。
- 后置真实中文、数字、箭头、锁、pin、任务 tag 和状态。
- 清除假字、占位横条、假按钮与生成越界。
- 不得用纯色矩形覆盖 art pass 已生成的卡框、按钮和纸面材质；文字安静区使用同源无字 clean layer / mask，亮度差控制为 `ΔL≤4`。
- 继续执行文字 bbox、同栏共轴、child containment、路线为 0、中央 / 右栏职责和 CTA 唯一性审计。

## 用户审阅入口

第一轮只展示一张带真实中文的完整 1920×1080 玩家视图。用户只判断：

1. 左栏是否不再内缩，整屏左右重量是否均衡；
2. 卡框、按钮、纸面和状态块是否摆脱程序矩形的粗糙感；
3. 是否达到 clean-low-poly weekly 标杆的完整美术气质；
4. 地图是否仍为第一中心、右档案第二、右下 CTA 唯一最强；
5. 是否愿意把它升格为后续资产化视觉基准。

不展示孤立组件、imagegen 原图、局部 QA 或拆图流程，除非用户明确要求技术复核。

## 边界

- 不改三栏职责、真实内容、任务容量或推进日语义。
- 不改 Godot、正式组件合同、compact A5.1 或 B2.12。
- 不生成 confirming、atlas 或批量组件；默认态 art pass 获用户认可后再继续。

## 执行记录

- 生图模式：Codex 内置 `imagegen`，任务类型 `ui-mockup`。
- 生图源：`wmw-fullscreen-default-art-pass-imagegen-source-v0-4.png`，原始输出 1672×941；它是完整无字整屏视觉源，仅作为技术输入，不单独交用户裁决。
- 最终整屏：`wmw-fullscreen-default-art-pass-filled-v0-4.png`，真实 1920×1080，有真实中文与确定几何。
- 程序只负责精确 rect、照片、文字语义与裁切；卡框、按钮、纸面、阴影和切角来自生图，不使用纯色矩形替换美术表面。

## 结果修订

用户确认 v0.4 版面没有问题，但否决其美术效果，认为与 benchmark-board-01/02 相去甚远。上一轮 UI / UX 美术 PASS 已撤回。该 Prompt 只保留为失败审计：它把 benchmark 降为第三顺位“visual DNA”，又在 hard negatives 中同时删除 `icons / office objects / folders / floating components`，实质上切掉了编辑拼贴、品牌图形、层叠纸件与附着物等关键身份载体；剩余的深色底、暖纸、橄榄与低多边形不足以单独构成 WMW。

后续不得从本 Prompt 微调重试。下一轮必须以 benchmark 艺术身份为第一视觉真值、v0.4 只提供 geometry / content mask，并新增五秒同族识别 Gate。

本轮最终执行 Prompt：

```text
Use case: ui-mockup.

Create one complete no-text 1920x1080 desktop game UI art pass for WORLD MYSTERIES WEEKLY, shown as a full player-facing screen, not isolated components and not an asset sheet.

Reference authority:
- Image 1 is the functional skeleton only: preserve its three-column responsibilities, real content capacity, map-first hierarchy, and default-state layout. Do not imitate its rough programmatic rectangles.
- Image 2 is the immediate art-direction source: inherit its dark blue-black cartographic stage, olive selected land, warm ivory dossier paper, low-poly facets, thin dark outlines, restrained shadows, and clean cut-corner construction.
- Images 3 and 4 provide visual DNA only: clean low-poly weekly editorial graphics, broad faceted surfaces, controlled olive / ivory / charcoal palette, precise modern geometry. Do not copy their placeholder bars or alter the functional layout.

Exact full-screen composition:
- Canvas 1920x1080, desktop 16:9.
- Left column has four aligned outer shells, all x approximately 30, right edge approximately 378, width approximately 348. Three region cards at y approximately 36, 294, 552, each height approximately 240. A full schedule / advance-day module at y approximately 810, height approximately 246. Vertical gaps are approximately 18. The left group must feel deliberately close to the left edge, not over-inset.
- Central dark map responsibility area occupies approximately x 402 to 1374, with the actual map stage approximately x 426, y 96, width 924, height 936. It is the first visual center. Use large faceted landmasses, one olive selected region, quiet dark sea, and a faceted bottom ice / world silhouette. No route lines.
- Right region dossier is one continuous warm-paper object at approximately x 1398, y 24, width 480, height 1032. It contains one title zone, one large photo window, one description area, one mission-intelligence header, four stacked mission rows, and one bottom primary CTA. The dossier is the second visual center; the bottom CTA is the only strongest action.

Art direction:
- Polished clean-low-poly weekly interface, premium indie strategy game, precise editorial geometry.
- Refine every card frame, photo-window rim, cut corner, paper footer, status block, schedule date strip, advance-day action, consequence strips, dossier sections, task tags, and CTA with coherent generated material language.
- Broad calm low-poly tonal variation instead of flat program rectangles. Warm ivory paper, dark navy-charcoal map field, muted olive selection and CTA, restrained rust only for the timed task accent.
- Keep shadows single-layered and controlled. Maintain clear hierarchy and generous readable surfaces for later real text overlay.

Hard negatives:
- Absolutely no text, pseudo-text, letters, numbers, placeholder bars, lorem ipsum, labels, icons, arrows, locks, padlocks, marker symbols, route lines, decorative buttons, filters, news ticker, legend, office objects, folders, desk, clipboard, stains, yellowed newspaper, grunge, photographic noise, excessive sepia, mobile layout, perspective view, isometric view, cropped screen, floating components, duplicated frames, double carriers, or extra UI modules.
- Do not put a redline-warning badge at the top of the right dossier.
- Do not create a second CTA or any clickable-looking control below the dossier.

The result must read as a finished, coherent full-screen art-direction proposal while leaving calm blank surfaces for exact Chinese text and runtime semantics to be composited afterward.
```
