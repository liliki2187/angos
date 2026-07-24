# 区域任务短签一体接合 v3 生图提示词

> 工具：Codex 内置 `image_gen`  
> 用途：只锁定 pin / label 的一体压合美术关系，不直接作为 Godot 正式 atlas  
> 输出：`runtime-preflight-v3/01-integrated-pin-label-source-v3-chroma.png`

## 输入图职责

1. `runtime-preflight-v2/01-pin-macro-components-source-v2-alpha.png`：pin 材质、轮廓、纸纹、橄榄色与 default / selected 参考。
2. `runtime-preflight-v2/02-label-macro-components-source-v2e-alpha.png`：横条纸面、切角、安静文字区与远端类型帽参考。
3. 用户提供的旧连接效果局部：pin 压住横条、两者读作同一纸件的构图参考。

## 最终提示词

```text
Use case: stylized-concept
Asset type: production-oriented game UI compound background source sheet for Angus region-task pins
Input images: Image 1 is the exact pin material, silhouette, paper texture, olive accent, default/selected style reference; Image 2 is the exact horizontal label paper, cut corners, quiet empty content face and far-end accent reference; Image 3 is the required connection/composition reference showing that the pin presses over and physically overlaps the horizontal label so both read as one object.
Primary request: create one focused corrected source sheet containing exactly four isolated, text-free compound tag backgrounds in a clean 2x2 grid: top-left default right-hanging label, top-right default left-hanging label, bottom-left selected right-hanging label, bottom-right selected left-hanging label. In every component the horizontal paper label must continue underneath the pin shoulder and overlap behind the pin; the pin foreground visibly clamps the label. There must be no background-colored gap between pin and label, no floating separation, and no extra connector patch. The inner end of the label is a simple flat paper neck hidden under the pin, while the colored type cap remains only at the far outer end. Selected differs only by the larger muted olive paper backplate behind the pin.
Style/medium: match the references exactly: clean low-poly weekly UI, warm off-white paper, restrained geometric cut corners, subtle paper fibers and faint angular watermark texture, thin dark ink outline, muted olive accents, crisp game-UI asset edges.
Composition/framing: four components at identical scale, generous separation and padding, long blank label areas suitable for later dynamic text, pin icon aperture left empty with no symbol.
Scene/backdrop: perfectly flat solid #ff00ff chroma-key background for local removal. The background must be one uniform color with no shadows, gradients, texture, reflections or lighting variation.
Constraints: preserve the existing pin and label proportions and visual language; connection overlap is the only design change; pin must be on top of label; no text, no letters, no numbers, no icons, no state badges, no arrows, no labels, no annotations, no watermark; do not use #ff00ff anywhere in the UI components; keep all four components fully inside the canvas with crisp separated silhouettes.
Avoid: navy gaps at the joint, double outlines at the joint, third-piece connector blocks, glossy rendering, thick shadows, ornate decoration, old newspaper distress, yellowed dirty paper, photorealistic noise.
```

## 后处理

- 使用 imagegen 技能自带 `remove_chroma_key.py` 将平面洋红背景转为 alpha。
- 程序只做透明化、裁切、九宫格延展中央空白纸面与 1×回填；没有绘制连接色块或重新设计接合肩。
