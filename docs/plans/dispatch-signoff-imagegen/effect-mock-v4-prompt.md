# Dispatch Signoff Filled Effect Mock v4 Prompt

> Date: 2026-06-17  
> Output: `docs/screenshots/2026-06-17-dispatch-signoff-effect-mock-v4/01-dispatch-signoff-filled-effect-mock-v4.png`  
> Label: target effect mock / filled-state text mock  
> Tool path: built-in image generation. OpenRouter was not used because uploading local project reference images to a third-party route was blocked by policy.

## Purpose

Generate a high-fidelity filled-state text mock for the Angus dispatch signoff screen. This image is for visual review of layout, functional partitions, text/avatar integration, and target screenshot feel. It is not a production cut asset and must not enter the manifest or runtime as a background.

## Prompt

```text
Generate a high-fidelity filled-state text mock for an Angus / World Mystery Weekly dispatch signoff screen. This is the screen after choosing a task, where the player assigns 1-3 reporters to execute it.

1920x1080 desktop 16:9 full screen game UI. Orthographic front view. No mobile layout. Dark deep navy editorial desk/workbench frame with modern graphic UI edges. Four-zone structure: top low-weight global status strip; left task signoff file; center dice-pool workbench with staff cards; right signoff review paper; bottom dispatch receipt and CTA state strip.

Functional content must be visibly filled. Top strip: 世界未解之谜周刊 / 第 1 周 / 本周 7 日 / 纽约市 / 线索调查 / 危险 / 可派 6/8 / 压力 22.

Left task file: 线索调查：纽约市. Tags 非正式记录. Meta 危险 · 耗时 2 天 · 截稿 3 天. Brief: 地下电报码在午夜重复播出，邻近街区的收音机同时接到一段无人署名的求救信号. Requirements 人脉 2 / 洞察 2. Target 潜在有效点 8. Failure 任务关闭，压力 +2. Return button 返回纽约市任务台.

Center workbench: header 本次骰池 3/3. Three selected staff cards with high-definition micro-pixel chibi reporter avatars and names 主角, 娜娜, 末日时钟. Each card has dice pips / attribute bars and a small 移出 button. Teal support card: 支援已投入 / 匿名热线录音 / 不占人位 · 可撤回. Candidate row: 伪人 disabled with red stamp 人数已满 / 先移出一人; 艾灵 and 印第安纳 available with dice summaries.

Right review paper: 签批复核. Red state banner: 不可签批 · 本次骰池已满. Review rows: 当前：潜在有效点 13 / 目标 8; 阻断原因：本任务最多派遣 3 人; 处理：先移出一名已选队员; 签批后：本周 7→5 · 截稿 3→1; 将派出：主角、娜娜、末日时钟. Disabled CTA: 先调整队伍. Add a blue round signoff stamp motif as non-clickable decoration.

Bottom strip: six CTA state sample plates: 默认 签批外勤, 悬停 签批外勤, 按下 签批外勤, 签批中..., 不可用 先调整队伍, 已盖章 已签批.

Angus visual style: modern graphic design + high-end micro-pixel texture + fresh printed paper material + deep navy and red-orange contrast. Paper should be clean warm ivory / off-white, not yellow, dirty, torn, or decayed. Slight paper grain and printed halftone are allowed only as controlled structure, never as stains. Use 2-4px pixel clusters, blocky halftone, red/cyan overprint misregistration, crisp cut marks and pixel edge accents. Avoid photorealistic paper details, old archive, sepia, brown office, worn newspaper, grunge stains, cracked corners, mold, dust, tea stains, and realistic photographic noise.

Character style: high-definition micro-pixel chibi reporters, low-energy black humor expressions, deep navy night mood, crisp outlines, not realistic portraits and not 8-bit retro.

Chinese text should look like printed UI text integrated into paper fields. Keep it crisp, aligned, and placed inside clean content rectangles. Do not let paper texture or halftone cross through text. Use strong Chinese headings, smaller paper-ink body text, red for blockers, cyan for support/available signals.

Avoid watermark, signature, artist name, copyright stamp, random logos, browser chrome, mobile frame, presentation mockup, dirty old paper, photorealistic desk clutter, generic fantasy RPG cards, glass SaaS panels, neon cyberpunk terminal, malformed faces, extra limbs, duplicate characters, oversaturated colors, muddy details, old newspaper nostalgia.
```

## Follow-Up Constraints

- If used for production, derive a separate no-text component prompt. Do not reuse this filled-state prompt as a cut-asset prompt.
- If promoted to a resource benchmark, run `@像素艺术` generation-after review first.
- Godot / HTML still owns task names, staff names, avatars, dice summaries, blocker reasons, CTA labels, and all runtime states.
