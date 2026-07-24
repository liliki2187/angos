# 区域任务 selected 类型色内框 v6 生图记录

> 日期：2026-07-21  
> 模式：内置 `imagegen`，`precise-object-edit`  
> 范围：常驻任务、右挂、B 闭合八边纸槽单例；不是四类型批量生产

## 编辑目标

- 编辑目标：`runtime-preflight-v5b-selected-icon-seat/01-permanent-default-right-compound-source-v5b-chroma.png`
- 唯一视觉修改：把图标座周围的中性闭合八边纸槽切换为常驻任务橄榄色 `#7F8A47`。
- 不变项：短签外轮廓、纸面、共享肩、指针尖端、右端类型帽、画布、图标、文字、selected 外后纸、尺寸、锚点与 alpha 边界。

## 首轮提示词

```text
Use case: precise-object-edit
Asset type: Angus desktop 16:9 game UI, selected-state compound task pin source asset
Input images: Image 1 is the exact edit target and geometry truth.
Primary request: Change only the closed octagonal recessed frame line surrounding the icon seat from its current neutral taupe-gray color to the permanent-task olive color #7F8A47. Preserve the exact same closed eight-sided geometry, exact line thickness, exact position, exact bevel, exact alpha edge, and exact paper-grain integration.
Scene/backdrop: Preserve the perfectly flat solid #FF00FF chroma-key background exactly; no gradient, shadow, texture, spill, or lighting variation on the background.
Style/medium: Identical stylized printed-paper game UI asset; subtle physical paper, restrained print texture, production-ready.
Composition/framing: Preserve the exact canvas dimensions, framing, compound silhouette, pointer tip, label strip, right cap, and all margins from Image 1.
Color palette: Only the recessed octagonal frame becomes #7F8A47 olive; keep all cream paper, neutral edges, and the existing olive right cap unchanged.
Constraints: Change only the octagonal frame color. Keep every other pixel-level design feature visually unchanged: silhouette, proportions, join geometry, paper texture, bevels, highlights, shadows, label body, right cap, pointer tip, and chroma background. No icon, no text, no new decoration, no extra ring, no glow, no scaling, no line growth, no inner-face tint, no selected backing plate, no watermark.
Avoid: geometry drift, thicker frame, double frame, incomplete frame, dark outline, green-tinted paper, recolored right label body, added seams, added shadows.
```

首轮视觉方向成立，但模型把 `1816×866` 画布漂移为 `1818×865`，不得直接拆图或进入 Godot。

## 单点纠偏提示词

```text
Use case: precise-object-edit
Asset type: Angus game UI exact replacement source asset
Input images: Image 1 is the edit target and absolute pixel-geometry truth.
Primary request: Repeat the selected-state edit, changing ONLY the closed octagonal recessed frame line around the icon seat from neutral taupe-gray to permanent-task olive #7F8A47.
Critical correction: Output must preserve the exact original canvas size of 1816 × 866 pixels. Do not add, crop, expand, shrink, rescale, shift, or reframe even one pixel. The compound silhouette, closed octagon vertices, line thickness, bevel, pointer tip, join shoulder, long paper strip, right cap, and all margins must align exactly with Image 1.
Scene/backdrop: Preserve the perfectly flat solid #FF00FF chroma-key background, uniform and unchanged.
Style/medium: identical stylized printed-paper game UI asset with restrained paper texture.
Color palette: only the existing neutral octagonal groove/frame changes to #7F8A47 olive; all other colors and materials stay unchanged.
Constraints: exact 1816x866 canvas; change only frame color; no icon; no text; no backing plate; no extra ring; no glow; no green paper tint; no geometry drift; no thickness change; no shadow change; no texture change outside the frame; no watermark.
```

纠偏稿仍为 `1815×866`。按照局部资产合同，它只作为橄榄油墨与纸面材质源；构建脚本用已通过的 B 中性框像素覆盖范围约束生成内容，使最终 selected 前层恢复 `1816×866`，并保证 default / selected alpha 逐像素一致。生成稿原始框色中位数约为 `[145,154,65]`，美术复核判为偏亮、偏黄；构建阶段只在原 B 框遮罩内做色号校准，最终中位数精确为 `[127,138,71]`（`#7F8A47`）。程序只负责高保真遮罩、色号校准、裁切和状态合成，不重新设计框型。

## 归档

- 原始生成稿：`runtime-preflight-v6-selected-type-frame/02-permanent-selected-type-frame-source-v6-imagegen-raw.png`
- 合同约束后的色键源：`runtime-preflight-v6-selected-type-frame/02-permanent-selected-type-frame-source-v6-chroma.png`
- 覆盖范围：`runtime-preflight-v6-selected-type-frame/02-permanent-selected-type-frame-source-v6-mask.png`
- 元数据：`runtime-preflight-v6-selected-type-frame/selected-type-frame-v6.json`
