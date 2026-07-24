# WMW `schedule_gate v0.1` 无字有色母版 Production Brief

## 身份

- `artifact_type = derived_no_text_component_candidate`
- `status = target_only_not_formal_contract`
- 最终母版：`456×328`。
- runtime 显示：`342×246 @ 0.75`。
- imagegen 只生产材质配料；完整组件由程序按 runtime-local 整数真值装配。
- 一张母版覆盖所有状态；外部阴影由未来 runtime host 持有。

## Imagegen 输入角色

- `benchmark-board-01.png`：现代 clean low-poly weekly 风格参考。
- `benchmark-board-02.png`：olive、warm paper、平面裁纸与编辑拼贴参考。
- `black-white-schedule-gate-v0-1-contract-board.png`：仅说明材质角色，不复制文字、数字、图标、状态或审计标记。

## 最终使用的 built-in imagegen prompt

```text
Use case: stylized-concept
Asset type: material ingredient board for a deterministic desktop game UI component pipeline

Input images:
- Image 1: style reference only. Use its modern clean low-poly weekly editorial material language.
- Image 2: style reference only. Use its restrained olive, warm paper, matte cut-paper planes, and clean orthographic presentation.
- Image 3: geometry-role reference only. It explains which material roles exist in the schedule component. Do not reproduce its layout, text, numbers, icons, state labels, arrows, punctuation, audit marks, or grayscale appearance.

Primary request:
Create one opaque material ingredient board, not a complete assembled UI component. The ingredients will later be masked and assembled by code into an exact 456×328 no-text schedule gate.

Produce four large, clearly separated, unlabeled material fields:
1. warm gray-beige modern weekly paper for the date and information areas;
2. muted olive matte action-panel material;
3. quiet ivory paper-edge and inset-rim material;
4. dark charcoal ink/divider material.

Style/medium:
Clean low-poly weekly editorial UI material, broad matte color-value planes, flat cut-paper construction, sophisticated modern weekly publication feel. Use only 3–5 broad low-contrast value planes per material field and extremely subtle print tooth. Keep writable surfaces calm and low-detail.

Composition:
Strict front-facing orthographic 2D material sheet. Every material field is flat, axis-aligned, and seen straight-on. Large usable uninterrupted sample areas, clear gutters between fields, no overlapping objects.

Color palette:
Warm paper centered near #B7A488, quiet ivory edge near #C0B9B3, muted olive action material within #4E623D–#5B6A37 with darker planes near #3F4C2D, charcoal ink near #191E1F–#272A2B.
Do not include warning rust in this source; warning rust belongs only to future runtime state overlays.
Do not introduce intentional teal, bright orange, white, or dead black.

Lighting/material:
Even flat studio-neutral illumination with no directional cast shadow. Paper depth comes only from subtle value planes and restrained surface tooth, not stains, wrinkles, folds, tears, or damage.

Text:
No text of any kind.

Constraints:
This is a material source sheet only, not a button, card, screen, wireframe, mockup, interface, atlas, or assembled component.
No typography, letters, numbers, symbols, punctuation, arrows, exclamation marks, check marks, progress marks, calendar icons, logos, stamps, labels, watermark, or UI indicators.
No perspective, no tilt, no isometric view, no camera angle, no foreshortening, no floating object, no environment, no desk, no wall, no hand, no clip, no tape.
No old newspaper, no yellowed archive, no sepia, no cardboard, no grime, no stains, no cloudy paper noise, no scratches, no folds, no torn edges, no heavy halftone, no pixel-art treatment, no dense triangulation, no GIS grid.
```

## 坐标与装配策略

1. runtime-local 坐标是权威。
2. 在 `1368×984` 工作画布按 runtime 坐标 `×4` 装配，所有边界均为整数。
3. 工作画布以 3:1 下采样到 `456×328`。
4. 母版以 0.75 显示到 `342×246`，与 runtime 真值对照。

程序负责外框、模块 mask、分隔线、alpha 和安全区；imagegen 像素只被采样 / 平铺进角色 mask，不能决定矩形边界。

## 材质角色

- 外层主体：benchmark-derived `warm_paper` 归一化后的 imagegen 配料。
- 日期栏 / 信息栏：安静 warm paper，safe rect 内无高对比断层。
- 动作栏：muted olive；warning rust 不进入母版。
- 图标井 / 窄边：quiet ivory。
- 边框 / 分隔线：charcoal ink。
- 外部投影：母版内 0 像素。

## Gate

- 原始配料板无文字、符号、完整组件结构、warning rust、旧报纸、泛黄、污渍或折痕。
- 456×328 母版无烘焙文字 / 图标，RGBA alpha 由程序几何产生。
- 342×246 回放结构边缘相对 runtime truth 偏差不超过 1px。
- 同一母版 hash 服务全部状态。
- default / confirming / executing / unavailable / idle_error / last-day / zero-days 的 glyph bbox 全部落在既有 safe rect。
- 输出真实 1920×1080 复核板与 geometry / alpha / color / text audit。
- 不修改 Godot、`design/ui-contracts`、compact A5.1 或有色整屏。

