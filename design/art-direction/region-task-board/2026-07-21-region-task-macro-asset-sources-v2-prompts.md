# 区域任务短签宏观组合件 v2 生图提示

> 日期：2026-07-21  
> 用途：生产切片可行性预检，不直接进入 Godot  
> 方法：美术模型生成纸件与内部压合关系；程序只负责色键转透明、裁切、尺寸归一和动态文字回填

## 共同真源

- `2026-07-21-region-task-selected-backplate-style-board-v1.png`：默认 / 选中纸件语言与四色关系。
- `2026-07-20-region-task-tag-state-style-board-v1.png`：状态小纸签、贴体弧和组合状态语言。
- `docs/screenshots/2026-07-17-region-task-pin-slice-v3/05-runtime-state-matrix.png`：只参考现有运行比例，不继承程序绘制的粗糙造型。

## A. 图钉组合件源板

```text
Use case: stylized-concept
Asset type: production-oriented 2D game UI component source sheet
Primary request: Create one clean 4-row by 2-column source sheet of eight isolated REGION TASK MAP PIN macro-components. The four rows are permanent, temporary, chain, hidden. The left column is default and the right column is selected. Do not draw row or column labels.
Input images: Image 1 is the approved paper style and selected-backplate reference; Image 2 is the state-language reference; Image 3 is runtime proportion reference only.
Scene/backdrop: perfectly flat solid #FF00FF chroma-key background, one uniform color, no grid, no border, no texture, no lighting variation.
Subject: Eight large paper map-pin components in exact aligned cells, each with the same 64:80 silhouette ratio and the same bottom anchor. Default is one baked macro-piece containing the warm ivory front paper shell, inset keyline, paper edge, connector shoulder and the small type-colored tip. Selected is one baked macro-piece containing the complete offset colored paper backplate, side folds, connector neck, front shell and type-colored tip. The selected backplate must feel like a paper layer behind the pin, not a centered octagonal frame. Leave the central 28×28 icon socket blank and clean; no symbols.
Style/medium: Angus clean-lowpoly-weekly editorial paper UI, warm gray-ivory stock, dark navy ink keyline, controlled low-poly paper facets, thin ivory cut edge, subtle misregistration, crisp flat 2D cutout.
Color palette: permanent muted olive #7F8A47; temporary ochre #886A40; chain teal #34767A; hidden slate blue-gray #445967. Type color is restrained and baked into the tip; selected additionally uses a lightened version on the rear paper plate.
Composition/framing: identical component scale, generous gutters, nothing touching. Internal contact shadows and paper overlaps may be baked inside each macro-component. No external cast shadow on the chroma background.
Constraints: front-shell geometry must be identical across all rows; selected geometry identical across all rows except color. Preserve large readable facets at final 64×80. No detached micro-pieces. No text, letters, numbers, icons, labels, watermark or pseudo-text.
Avoid: concentric selection ring, centered badge frame, metallic bevel, glossy button, thick dark shadow, antique yellowed archive paper, photoreal paper noise, tiny filigree, one-pixel decorations, software dashboard styling.
```

## B. 左右短签组合件源板

```text
Use case: stylized-concept
Asset type: production-oriented 2D game UI label-shell source sheet
Primary request: Create one clean 4-row by 2-column source sheet of eight isolated blank REGION TASK LABEL macro-components. Rows are permanent, temporary, chain, hidden. Left column is RIGHT-HANGING: the map pin attaches at the label's left side and the colored end-cap is at the far right. Right column is LEFT-HANGING: the map pin attaches at the label's right side and the colored end-cap is at the far left. Do not draw labels explaining the grid.
Input images: Image 1 is the approved type-color and selected paper reference; Image 2 is the full state-language reference.
Scene/backdrop: perfectly flat solid #FF00FF chroma-key background, no grid, no border, no texture, no lighting variation.
Subject: Eight long warm-ivory paper label shells with identical 200:72 outer ratio. Each is one baked macro-piece containing the full paper face, inset keyline, shallow connector cut/neck at the pin side, layered paper edge, and the type-colored outer end-cap. The left- and right-hanging versions are intentionally redrawn structural counterparts, not a mechanically mirrored texture. Keep the center blank and quiet for dynamic title and meta text. Reserve a visibly generous rectangular safe area equivalent to 158×48 inside a final 200×72 label, starting about 14px from the inner left/top edge and ending before the outer cap.
Style/medium: same Angus clean-lowpoly-weekly editorial paper UI as Image 1, thin ivory edge, dark navy keyline, restrained low-poly facets, crisp cut corners, subtle internal paper overlap.
Color palette: permanent muted olive #7F8A47; temporary ochre #886A40; chain teal #34767A; hidden slate blue-gray #445967. Only the far outer cap and a very small paper seam use type color.
Composition/framing: identical scale and baseline, generous gutters, nothing touching. Internal paper-contact shading may be baked. No external shadow on the chroma background.
Constraints: no pin, no icon, no text, no letters, no numbers, no watermark, no pseudo-text. The blank text face must remain low contrast and free of folds, cap color or dark keylines.
Avoid: narrow decorative spine floating on top, type color crossing the text area, deep embossing, glossy UI, antique stains, thick frames, tiny ornamental cuts that vanish at 1×.
```

## C. 流程状态小纸签源板

```text
Use case: stylized-concept
Asset type: production-oriented 2D game UI status-badge source sheet
Primary request: Create three isolated complete paper status tickets in one horizontal row: assigned, urgent, locked. Do not draw captions.
Input images: Image 1 is the approved full state-language reference; Image 2 is the approved paper and type-color reference.
Scene/backdrop: perfectly flat solid #FF00FF chroma-key background, no grid, no border, no texture, no lighting variation.
Subject: Three compact shoulder-mounted paper tickets designed to overlap the upper-right shoulder of a 64×80 map pin. Each ticket is one complete baked component with paper base, cut corners, thin ivory edge, small internal contact shadow and a bold readable icon. Assigned uses a quiet blue-gray person/document mark; urgent uses a restrained rust-red deadline/clock mark; locked uses a charcoal-gray padlock mark. All three share the same bounding box and attachment geometry.
Style/medium: Angus clean-lowpoly-weekly editorial paper UI, crisp flat cutout, warm ivory paper, dark navy ink, subtle facets, readable at roughly 18×18 runtime.
Composition/framing: large centered badges with wide equal gutters. Internal layer shading only; no cast shadow on the background.
Constraints: no text, no letters, no numbers, no watermark, no pseudo-text. One bold symbol per ticket, no detached strokes.
Avoid: plain program polygon, naked unicode glyph, circular app badge, glossy icon, metallic emblem, tiny detail, thick shadow, antique archive paper.
```
