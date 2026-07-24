# 区域任务 pin 图标座 v5 生图记录

> 日期：2026-07-21  
> 模式：Codex 内置 `imagegen` 定向编辑；程序只负责色键转透明、尺寸归一、放入既有 kind icon、QA 排版和 Godot 测试夹具。

## 用户反馈与范围

用户复核 v4b 无内框 pin 后明确指出：图标周围没有线框会显得过空，设计不成立，要求提供多个优化方案。本轮只比较常驻任务右挂 pin 头的图标座；外轮廓、图标 bbox、anchor、hit、compound、selected 后纸、文字和动效全部冻结。

唯一编辑真源：

`runtime-preflight-v4b-single-probe/03-permanent-default-pin-only-source-v4b-chroma.png`

## 三个有效候选

### A｜下开口切角框

要求只增加上、左、右三边连续的切角纸框，底部朝 pin 尖端主动开口；原生 `64×80` 下保持约 `2px` 连续实色带，颜色弱于图标，不形成闭合双框。首张输出因框带过厚降级为内部偏差样本；第二次只减薄并收紧图标座后进入候选。

- 最终内置生图原件：`C:/Users/gzfangyue/.codex/generated_images/019f7e72-fe5d-7d51-aee7-4b441aa89cc9/exec-44b3b8bd-79ae-4d3d-afd9-7522a3ffaadb.png`
- 仓库色键源：`icon-seat-options-v5/01-option-a-open-bottom-frame-chroma.png`

### B｜闭合八边纸槽

要求使用连续、实心、低对比暖灰纸槽带，原生 1× 最细处不低于 `2px`；不复制 pin 的尖底轮廓，不使用纯黑、细发丝线或断续边。

- 内置生图原件：`C:/Users/gzfangyue/.codex/generated_images/019f7e72-fe5d-7d51-aee7-4b441aa89cc9/exec-eead2fc0-668d-4560-b5ba-dd5903331097.png`
- 仓库色键源：`icon-seat-options-v5/02-option-b-closed-octagon-groove-chroma.png`

### C｜微差色切角纸窗

要求以比主纸面仅深约 `8–12%` 的实面切角纸片承托图标，不依赖细描边；只允许轻微纸面分层，不做按钮浮雕、内阴影或状态色。

- 内置生图原件：`C:/Users/gzfangyue/.codex/generated_images/019f7e72-fe5d-7d51-aee7-4b441aa89cc9/exec-19a9454c-1117-41eb-a9d5-bc78fd6566b5.png`
- 仓库色键源：`icon-seat-options-v5/03-option-c-tonal-paper-window-chroma.png`

## 共同硬约束

- 中心保持空白，文档 icon 继续由运行时 atlas 提供。
- 图标座在 idle / hover / selected 三态中必须是同一结构常量，不参与状态渐变。
- 不使用 selected 橄榄后纸承担图标座，不增加发光、黑框、污渍、复古印章或程序描边。
- 原生 1×先于放大图验收；4×图只使用最近邻放大，不作为精度替代。

## 输出

- 候选源与运行尺寸：`design/art-direction/region-task-board/icon-seat-options-v5/`
- 构建脚本：`scripts/art/build_region_task_icon_seat_options_v5.py`
- Godot 测试脚本：`gd_project/tests/capture_region_task_icon_seat_options_v5.gd`
- 透明 / 1× QA：`docs/screenshots/2026-07-21-region-task-icon-seat-options-v5/01-icon-seat-options-imagegen-1x-qa.png`
- Godot 真实地图回填：`docs/screenshots/2026-07-21-region-task-icon-seat-options-v5/02-godot-icon-seat-options-1x.png`

本轮没有替换生产资源，也没有把候选同步到 hover / selected compound。用户选定后才进入同一图标座的三态同步复验。

## 用户选择 B 后的 compound 同步

用户明确选择 B，并指出 A 的开口框像少了下半截、只有三边，第一观感未完成。B pin-only 保持原候选；新增一次 `precise-object-edit`，以 v4b default compound 为唯一编辑目标、B pin-only 为图标座视觉真值，只把闭合八边纸槽转移到 compound 左头。

核心调用约束：

```text
Change only the left pin-shaped head of the default compound by transferring the CLOSED CUT-CORNER OCTAGONAL PAPER-GROOVE FRAME from the user-selected B pin-only reference into the exact corresponding position. Preserve the compound canvas, #FF00FF chroma background, entire warm-ivory silhouette, shared shoulder, long writable paper body, right olive cap, paper facets, texture, proportions and placement. Keep the frame center blank for the runtime icon. The frame is state-neutral and must not add selected backing, hover glow, focus marks, text or icons. Do not redesign B into an open frame and do not remove its bottom side.
```

- 内置生图原件：`C:/Users/gzfangyue/.codex/generated_images/019f7e72-fe5d-7d51-aee7-4b441aa89cc9/exec-67a86c6e-a959-4faa-a952-c6f1cff2d188.png`
- 仓库色键源：`runtime-preflight-v5b-selected-icon-seat/01-permanent-default-right-compound-source-v5b-chroma.png`

selected 不另生成第二套 B 框：运行时保持 B default compound 在前层，selected underlay 只在后层提供橄榄纸背，从结构上保证三态 B 框逐像素一致。
