# 派遣签批台整屏风格稿 v2

> 日期：2026-06-16  
> 状态：给用户评审整体效果的整屏风格预览；不作为生产切图或 Godot 底图。  
> 生成方式：内置 `image_gen` 生成无运行时文字美术底稿，再用本地脚本叠加可控中文与数值。

## 产物

| 文件 | 用途 | 状态 |
| --- | --- | --- |
| `docs/screenshots/2026-06-16-dispatch-signoff-full-style-v2/01-dispatch-signoff-full-style-v2-artboard-no-runtime-text.png` | 无运行时文字整屏美术底稿 | 可作为视觉锚点候选；含少量抽象占位条，不可直接切图 |
| `docs/screenshots/2026-06-16-dispatch-signoff-full-style-v2/02-dispatch-signoff-full-style-v2-filled-preview.png` | 本地叠字后的完整填充态预览 | 当前给用户看的主图 |
| `tmp/ui-screens/render-dispatch-v2-filled-overlay.ps1` | 将中文、数值、骰面、CTA 文案叠到美术底稿上的本地脚本 | 工具脚本，不是运行时资源 |

## 本轮目标

这张图只回答一个问题：派遣签批台如果按资产化 UI 方向继续走，整屏观感是否成立。

它继承的结构：

- 左侧：当前任务档案纸。
- 中央：本次骰池、3 个已选队员槽、1 个支援槽、6 张候选员卡。
- 右侧：签批复核纸、达标率、风险、签批后果、非交互状态章、主 CTA。

## Prompt 摘要

- `1920x1080` 桌面 16:9 游戏 UI 风格稿。
- “主编外勤签批台”，不是 SaaS dashboard。
- 深海军蓝工作台、暖白新印刷纸、红橙截稿 / 签批、青色支援 / 追踪。
- 现代图形设计、半调网点、套印错位、2-4px 高清微像素颗粒。
- 不烘焙真实中文、英文、数字、任务名、员工名、概率、按钮文案。
- 生成底稿只留干净安全区；动态文字由本地叠层 / Godot 渲染。

## 初步判断

优点：

- 比 `05` 更像正式美术风格稿，员工卡、头像、支援槽、右侧红色签批按钮的物件感更强。
- 三栏结构更自然，第一眼更容易读成“签批台”而不是普通后台表单。
- 适合反推下一步 P0 资产 prompt bundle，尤其是任务纸、员工卡、复核纸和 CTA。

风险：

- 底稿仍有抽象黑色占位条，不能直接作为最终 UI 或生产切图。
- 左侧纸面略有旧档案感，后续 P0 资产应继续压回“新鲜暖白印刷纸”。
- 右侧复核纸的图形装饰密度偏高，生产拆件时必须保证 `content_rects` 不被图章、线条、图标穿过。
- 候选卡头像风格是剪影占位，不代表最终角色头像方向；角色头像仍需遵守高清微像素 Q 版角色真源。

## 美术指导复审

结论：有条件通过。

可作为后续 P0 资产 prompt bundle 的视觉锚点，原因是它已经具备 Angus 的主要读法：深海军蓝工作台、暖白新印刷纸、红橙签批 CTA、青色支援卡、异常眼符号、纸夹 / 签批单 / 中控托盘等编辑部工作物件。

不得直接升级为生产标杆或切图母版，必须在 P0 资产 prompt 中修正：

- 纸张和边缘脏污略偏旧档案：保留暖白新印刷纸，压低泛黄、灰褐脏边和随机旧污，改成干净印刷压痕、套印错位和轻微纸纤维。
- 噪声有摄影贴图感：桌面刮痕、金属夹和红按钮磨损要转为 2-4px 像素颗粒、块状半调、红青套印偏移和清晰图形边缘。
- 填充态文字覆盖层有 SaaS 化风险：米白文字盒、顶部标题胶囊、达标率卡片只作为预览手段；正式资产中动态文字必须落在纸签、压章、标签 plate、按钮铭牌和签批纸字段里。
- 红 CTA 需要更像签批动作入口：强化印章压下、机械送印开关、红色签批盖板语义，避免普通大按钮。
- 安全区必须进入资产要求：纸夹、折角、书签、眼符号、红牌、强半调、按钮边框全部作为 `no_text_rects`，任务标题、数值、状态、CTA 文案必须有干净正交可写区。

## 二次复审

> 2026-06-16 用户对局部纸张、整体写实度和功能分区提出明确反馈后，SIA 与 `@像素艺术` 再次复审。

结论：v2 的三栏构图可作为参考，但不得作为生产标杆、资源标杆或直接切图母版。下一版不应继续润色当前图，而应基于功能分区重新生成无运行时文字底稿。

必须修正：

- 纸张允许有质感，但必须从偏黄旧档案改为干净象牙白 / 暖白新印刷纸；禁止脏污、破边、撕裂、茶渍、灰褐脏边、旧报纸、羊皮纸和 sepia。
- 整体质感必须从摄影级旧物件转为 Angus 像素印刷语言：2-4px 方块颗粒、块状半调、红青套印错位、裁切线、清晰图形边缘和低权重印刷压痕。
- 功能分区必须先于生图：顶部全局状态条、左任务简报纸、中派遣配置台、右签批复核纸各自承担明确决策事实；不可先生成装饰桌面再后贴文字。
- Steam 缩略图必须能读出“派人 + 支援 + 达标率 / 风险 + 消耗 + 签批执行”的因果链；中央已选队伍和支援应视觉流向右侧结果预览。
- 动态文字安全区必须是干净正交矩形；折角、夹子、红签、印章、半调块、强像素颗粒和纸边全部列为 `no_text_rects`。

下一版正向 prompt 核心：

```text
16:9 desktop game UI artboard, no readable text, no baked UI labels.
Modern supernatural weekly magazine dispatch signoff desk, three clear functional work objects:
left clean ivory task briefing clipboard, center dark navy assignment tray with staff card slots and support slot, right clean ivory signoff sheet with a large red-orange stamp/approval button.
Angus visual style: bold modern editorial graphic design, deep navy #0F1A2E, vivid red-orange #E84B2C, clean warm ivory paper #F5EDD8 / #F8F2E4.
Printed matter materiality, crisp paper edges, subtle halftone fields, 2-4px pixel grain clusters, slight red-cyan misregistration, crop marks, clean graphic shadows.
Keep large blank content rectangles for runtime text, flat readable surfaces, controlled texture outside text zones.
Cool, confident, urgent, black humor, fresh supernatural weekly magazine, not vintage archive.
```

下一版负面 prompt 必须包含：

```text
no yellowed old archive paper, no dirty stains, no broken torn paper, no coffee marks,
no dusty old newspaper, no decayed folder, no warm wooden desk, no cozy office,
no photorealistic scratches, no corroded metal, no chipped paint, no random paper noise,
no generic SaaS panels, no mobile game capsule buttons, no neon cyberpunk hologram,
no baked readable text, no fake paragraphs inside content areas.
```

## 下一步建议

下一步不继续修整 v2 整屏图，而是按 A65 进入功能分区版 v3 和 P0 asset prompt bundle：

1. `ds_task_brief_sheet`
2. `ds_selected_slot_atlas`
3. `ds_staff_card_atlas`
4. `ds_support_slot_atlas`
5. `ds_review_sheet_base`
6. `ds_cta_signoff_atlas`

每个组件都必须继承当前 v2 的物件感，但重新生成为无文字、可切图、带状态帧和安全区的正式 P0 资产。
