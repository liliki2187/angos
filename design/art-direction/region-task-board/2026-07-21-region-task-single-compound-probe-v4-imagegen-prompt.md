# 区域任务短签单例 compound v4 生图记录

> 日期：2026-07-21  
> 模式：Codex 内置 `imagegen` 真实生图 / 定向编辑；程序仅负责色键转透明、中央空白纸面三切片延展、尺寸归一、逐帧录制与 QA 排版。

## 本轮范围

先生成一个 `常驻任务｜selected｜右挂` 的无字完整底图；用户要求继续厘清选中 / 非选中后，再从同一真值定向派生 `default compound` 与匹配 v4 头部的 `idle pin-only`。范围仍只有常驻右挂，不是 16 帧批量生产。

## 参考图角色

1. `runtime-preflight-v2/01-pin-macro-components-source-v2-alpha.png`：只参考纸张材质、pin 头比例、针尖与内部印刷线语言；不继承连接侧完整外框。
2. `runtime-preflight-v2/02-label-macro-components-source-v2e-alpha.png`：只参考安静纸面、远端类型帽与文字安全区；不继承内端端盖。
3. 用户旧一体式参考图：正例，只参考“一张横向纸签的左端长成 pin 头”的物件读法和尺度关系。
4. 用户红框否决图：纯负例，禁止复制其双外框、上下凹口、绿色竖块和 overlap 接头。

## 实际调用主提示词

```text
Create ONE single manufactured die-cut front-paper silhouette for the Angus clean low-poly weekly UI: a permanent-task, selected-state, right-facing horizontal map task ticket. It is not a separate map pin attached to a separate label. The long ticket body and the pin-shaped enlarged left end are the same continuous warm-ivory sheet of paper.

The front compound has exactly ONE continuous outer contour and ONE continuous ivory cut rim, with no internal boundary at the head-to-strip junction. At the connector side, the upper and lower contour of the pin-shaped head flow directly into the horizontal top and bottom edges of the long ticket through short clean shared-shoulder transitions. The paper base color, broad low-poly value planes and subtle print tooth continue uninterrupted across the shoulder; at least one broad low-contrast paper facet crosses the former junction.

The pin-shaped left end has a downward locator tip. Its central face may retain one thin printed inset keyline for a future icon socket, but it must not have a second cut rim, raised paper edge or cast shadow. Keep the icon socket blank. Keep the long central writable face calm and blank for future dynamic Chinese title and meta. Preserve a small muted-olive permanent-task cap at the far right end.

Behind the front compound is ONE continuous muted-olive selected backing sheet. It is a rear offset paper silhouette, never a connector block. Only a narrow edge is visible around the outer left head; on the right side it continues briefly underneath the long front-paper body and its return edge is completely occluded by the front sheet. The backing is hard-edged paper and has no visible vertical terminal, tongue, spine or bridge.

Preserve the referenced warm paper and muted-olive palette; do not globally retone the asset. Clean low-poly weekly paper UI, broad geometric paper facets, restrained print tooth, crisp readable shape at small runtime scale.

One isolated asset only, centered with generous gutters, on a perfectly flat uniform #FF00FF chroma-key background. No grid, captions, comparison board, decorative frame or cast shadow on the chroma background.

Do not average the references. Use each reference only for its declared role. The red-box image is a rejection example, never a positive geometry reference.

No two separate closed silhouettes, no complete pin outline on the connector side, no left end-cap on the label body, no internal vertical seam, no double ivory rim, no double keyline, no double cast shadow, no top or bottom concave notch, no dark background wedge at the shoulder, no olive connector block, no green vertical rectangle, no colored bridge, tongue, spine or patch, no modular joint cap, no paper-on-paper overlap line between head and strip, no soft gradient blend, no text, no letters, no numbers, no pseudo-text, no icon, no state badge, no urgent marker, no watermark, no old-paper stains, no antique archive texture, no glossy UI and no metallic bevel.
```

## 输出

- 生图色键源：`runtime-preflight-v4-single-probe/01-permanent-selected-right-compound-source-v4-chroma.png`
- 透明原始源：`runtime-preflight-v4-single-probe/01-permanent-selected-right-compound-source-v4-alpha.png`
- 运行候选：`runtime-preflight-v4-single-probe/rt-task-compound-permanent-selected-right-v4-3x.png`
- 1×读回：`runtime-preflight-v4-single-probe/rt-task-compound-permanent-selected-right-v4-1x.png`

## default compound 定向编辑提示词

唯一输入为已通过的 selected v4 色键源。实际调用要求只删除 selected 后衬，不重新设计前纸：

```text
Use case: precise-object-edit
Asset type: Angus clean low-poly weekly game UI compound background, default/non-selected companion frame
Input images: Image 1 is the ONLY positive source of truth and the exact edit target.
Primary request: Create a subtraction-only derivative of Image 1. Remove ONLY the rear muted-olive selected backing paper visible around the outer left/pin-shaped head and beneath its short shoulder. Replace those removed backing pixels with the same perfectly flat uniform #FF00FF chroma-key background. This is not a redesign.
Critical invariants: preserve the entire warm-ivory front compound exactly: same canvas and placement, same single alpha/front-paper silhouette, same shared upper and lower shoulder turns, same pin tip, same thin printed inner octagonal keyline, same long top and bottom edges, same calm writable face, same broad low-poly paper facets and print tooth, same right-end bevel, and exactly the same far-right permanent-task muted-olive end-cap. Preserve every visible front-paper edge, rim and proportion. Preserve the empty icon socket and blank text area.
State distinction: the output is the default/non-selected compound. It has no rear selected backing anywhere. It has no hover highlight; hover is runtime behavior and must not be baked into this asset.
Scene/backdrop: perfectly flat uniform #FF00FF chroma-key background, with no shadow, gradient, texture, floor plane, halo or color spill.
Constraints: change only the rear selected backing; keep all other pixels and geometry as visually identical to Image 1 as possible. One isolated asset only. No text, letters, numbers, pseudo-text, icons, badges or watermark.
Avoid: do not remove or recolor the far-right olive permanent end-cap; do not remove any olive accent at the far-right end; no new outline, no connector seam, no closed pin edge on the connector side, no label inner end-cap, no double border, no green connector block, no notch, no extra paper layer, no new cast shadow, no simplification, no flattening, no restyling.
```

输出：

- 色键源：`runtime-preflight-v4-single-probe/02-permanent-default-right-compound-source-v4-chroma.png`
- 透明源：`runtime-preflight-v4-single-probe/02-permanent-default-right-compound-source-v4-alpha.png`
- 3×运行候选：`runtime-preflight-v4-single-probe/rt-task-compound-permanent-default-right-v4-3x.png`
- 1×读回：`runtime-preflight-v4-single-probe/rt-task-compound-permanent-default-right-v4-1x.png`

## idle pin-only 定向编辑提示词

复核发现旧生产 pin-only 与 v4 头部比例不同，会在 idle → hover 时形成双头。唯一输入改为 default compound，并只删除横条、补最短右闭合边：

```text
Use case: precise-object-edit
Asset type: Angus clean low-poly weekly game UI idle pin-only companion
Input images: Image 1 is the approved default compound and the ONLY edit target. Treat it as a locked raster production source, not a loose style reference.
Primary request: Create a subtraction-and-minimal-closure derivative, not a redesign. Preserve the pin-shaped head exactly in its existing pixel position. Remove ONLY the long horizontal ticket extension to the right of the existing upper and lower shared-shoulder roots, including the long paper body and far-right olive end-cap. Then close the newly exposed right side of the pin head with the shortest possible single warm-ivory paper edge connecting the existing upper and lower shoulder roots.
Critical invariants: preserve the left, top, lower and pointed-tip outer contour of the pin-shaped head; preserve the exact head width, height, anchor, tip slopes, shoulder-root coordinates, thin printed inner octagonal keyline, warm paper color, ivory cut rim, ink-line weight, broad low-poly paper facets and print tooth. Do not redraw, rescale, recenter, rotate, symmetrize or reinterpret the head. Do not alter the icon socket.
Closure: the new right closure is one quiet straight/slightly faceted paper edge, using exactly the same warm paper fill, ivory cut rim and fine ink outline. It must remain inside the area that was covered by the removed horizontal ticket body, so the default compound can cover it during idle-to-hover transition. No connector cap, no colored tip and no extra layer.
State constraints: no selected olive backing, no horizontal label, no far-right end-cap, no hover highlight, no icon, no text, no state badge.
Scene/backdrop: perfectly flat uniform #FF00FF chroma-key background with generous empty space; no shadow, gradient, texture, floor plane, halo or color spill.
Constraints: change only the removed horizontal extension and the minimal new closure. One isolated blank pin-only asset. No letters, numbers, pseudo-text, icon, badge or watermark.
Avoid: no old production pin reference, no new map-pin redesign, no wider or narrower head, no longer or shorter tip, no new type-colored accent, no connector block, no second paper silhouette, no double border, no glow, no hover arc, no cast shadow, no glossy or metallic treatment.
```

输出：

- 色键源：`runtime-preflight-v4-single-probe/03-permanent-default-pin-only-source-v4-chroma.png`
- 透明源：`runtime-preflight-v4-single-probe/03-permanent-default-pin-only-source-v4-alpha.png`
- 3×运行候选：`runtime-preflight-v4-single-probe/rt-task-pin-permanent-default-v4-3x.png`
- 1×读回：`runtime-preflight-v4-single-probe/rt-task-pin-permanent-default-v4-1x.png`

pin-only 生图的色键背景存在轻微色差，通用 soft matte 会误伤纸面纹理，因此最终透明化使用“仅从画布边缘连通的高饱和品红区域”洪泛遮罩；程序没有重画纸面或闭合边。

## v4b：selected 强度与闭合内圈定向修正

用户在原生 1×局部中指出 selected 不够明显，且闭合黑色内圈缩放后若隐若现。v4b 保持三态结构、画布、前纸、共享肩、右端类型帽和动态层合同，只做以下美术编辑：

- default compound 与 idle pin-only：删除闭合黑色内圈，其他造型保持。
- selected compound：删除同一内圈，并把左头后方橄榄纸层加强；第一次编辑缩到 1×后仍只有约 `1–2px`，未进入交付，随后只重做 selected。
- 最终 selected 追加调用原文：

```text
Edit the provided Angus UI compound task-tag raster asset. Preserve the canvas size, magenta chroma-key background, transparent-cutout-ready isolation, exact cream foreground silhouette, right-side olive type cap, paper texture, bevel language, and all outer geometry. This is the SELECTED state only.

Make exactly one targeted visual correction: enlarge the olive-green rear paper layer behind the left pin/head so that after the asset is downscaled to 80 px total height it remains a crisp, clearly visible 3–4 px reveal. At this 1818×866 source size, the rear olive layer should extend about 30–38 source pixels beyond the cream foreground along the upper-left bevel, straight left side, and lower-left diagonal/shoulder. It must read as a single offset rear sheet of paper tucked behind the cream pin head, with hard faceted paper edges and subtle shadow separation. It must NOT continue behind the connector/neck, horizontal label body, bottom edge of the label, or the right cap. Do not create a full green ring, green plaque, halo, glow, thick stroke, or rectangular block.

The closed dark inner octagonal keyline around the left pin head must remain completely absent. Do not add any replacement line, dotted line, groove, corner ticks, C-shape, embossed outline, or black border. Leave the center blank for the runtime icon; add no icon and no text. Keep the cream front face exactly in front of the olive rear sheet.
```

最终生图原件：`C:/Users/gzfangyue/.codex/generated_images/019f7e72-fe5d-7d51-aee7-4b441aa89cc9/exec-a7e8d2c8-c9ad-4953-8808-ffdf48f3b849.png`。仓库色键源、透明源和运行尺寸候选统一归档到 `runtime-preflight-v4b-single-probe/`；程序只做边缘连通色键去除、尺寸归一、透明 QA 和动图排版，没有绘制 selected 背板或替换美术边线。
