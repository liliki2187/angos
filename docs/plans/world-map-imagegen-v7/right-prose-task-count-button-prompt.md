# World Map v7 A79 Right Prose + Task Count Button Prompt

> Status: 2026-06-17 A79 filled-state target prompt.  
> Output target: next Image 2 filled-state mock after `03-world-map-v7-difficulty-rating-task-intel-popover.png`.  
> Rule: target screenshot / visual-density reference only. Do not use as production PNG, cut-up source, manifest source, or runtime background.

## Purpose

This prompt updates the A77 direction with the user's latest right-dossier correction:

- left region cards still show region-level difficulty / recommendation;
- the right large body paper contains only region prose;
- task information sits in a secondary task-count button directly below the red / state ticket;
- the task button displays the count and an action verb, preferably `查看任务情报 · N`;
- clicking the task button opens a read-only popover, not a task selection UI.

Generation note:

- If the model places `任务情报` below the large prose paper, treat that output as failed. The cyan task-count ticket belongs between the red / state ticket and the prose paper, because the prose paper is only for region copy.
- If the task-count ticket is full-width and visually attached to the prose paper, treat that output as failed. The ticket must look like an independent clickable ticket / drawer tab, not the title bar of the prose paper.

## Required State

```text
Selected region: 北美禁区带
Region state: 红线升温 + 可进入
Difficulty: 中等
Recommendation: ★★★★
Task count: 3 current known previewable tasks
Task button: 查看任务情报 · 3
Task popover: open
Primary action: 进入选定地区
```

## Prompt

```text
Create a 1920x1080 desktop filled-state target mock for the Angus world-map UI.

Visual language:
- high-end pixel-print editorial board;
- deep navy control table;
- bright modern ivory paper, not yellow archive paper;
- low-poly faceted paper world map in the center;
- strong but controlled pixel grain, crisp pixel edges, printed halftone clusters;
- red-orange urgency marks and restrained cyan signal marks;
- compact game UI composition, not a poster or landing page.

Important:
- This is NOT production asset art. It is a filled-state target screenshot for judging information density, typography, and art/text fit.
- Text can be baked only for this mock. Later production PNGs must be no-text components.
- Keep the accepted v7 / fusion-B composition, but correct the right-dossier information hierarchy.

Top status strip:
- Left weekly tickets: 探索周 01, 剩余 7 天.
- Right world-state rail: 世界状态, 公信 42, 诡名 18, 声望 31, 守序 26, 狂性 11.
- Week/day tickets and world-state rail must use different visual grammar.

Left region index:
- Four visible region cards.
- Card 1 selected: 北美禁区带, 红线升温 / 可进入, 难度：中等, 推荐 ★★★★, short reason such as 首区主线 or 红线升温.
- Card 2 locked: 东亚神秘地带, 锁定, 难度：高, 推荐 ★★, blocker such as 声望 31/40 or 缺青线 1.
- Card 3 enterable: 太平洋失航带, 可进入, 难度：低, 推荐 ★★★.
- Card 4 locked / sealed: 南美红线档, 封存, 难度：异常, 推荐 ★.
- Do NOT show 目标 / 限时 / 线索 / 深链 counters on the left cards.

Central map:
- North America is selected with a clear pin, selected ring, and route emphasis.
- Other pins are muted. Locked pins look sealed / ghosted.
- Do not place long text labels on the map.

Right selected-region dossier, strict top-to-bottom order:
1. Fixed label: 选定地区 or 区域档案.
2. Title: 北美禁区带.
3. Compact badges near title: 难度：中等 and 推荐 ★★★★.
4. Region image / identity panel, showing a dark city / anomaly signal image in the approved pixel-print style.
5. Red / state ticket directly under the image: 红线升温 / 可进入 / 7 天内提升狂性风险.
6. Cyan secondary task-count button directly under the red / state ticket: 查看任务情报 · 3. It is a secondary preview button, not the primary CTA.
   It must be an independent, inset ticket: narrower than the prose paper, with 12-20px side inset, slight raised shadow / offset, right-side arrow or `查看` action chip, and hover / pressed / open affordance. It must not share the exact width or top edge of the prose paper below.
7. Large region prose paper below the task-count button with a clear 12-16px air gap. This paper contains only region description sections: 地区特征, 本周异变, 可带回素材, 地区预警 / 编辑价值.
8. Primary CTA plate below the dossier: 进入选定地区.

Hard placement rule:
- The cyan 查看任务情报 · 3 ticket must never sit below the large prose paper.
- The large prose paper must never sit directly under the red / state ticket when the task-intel ticket exists.
- The task-intel ticket must show its count on the button face; do not render it as only 任务情报.
- The task-intel ticket must not be full-width like a section title bar. It must read as a clickable control, with an action verb or right-side action cue.

Hard boundary for the large region prose paper:
- It must not contain task count, task list, task name, task summary, task preview rows, dispatch controls, staff, dice, success rate, filters, sorting, or tutorial text.
- It should read like a region dossier: what this place is, what changed this week, what kind of materials may be found, and what warning / editor value it carries.
- Keep paragraphs short and legible, with comfortable margins from folds, screws, halftone dots, and paper edges.

Task intel popover:
- Show the popover open, anchored near the cyan 查看任务情报 · 3 button and expanding leftward without covering the primary CTA.
- Title: 本区可追踪任务 3.
- 2-3 compact read-only task preview rows only. Each row can show a rough task type / task name and small tags such as 成本, 条件, 风险, 素材.
- It must not look selectable. No dispatch button, no staff slots, no dice, no success rate, no full task cards, no active row highlight.
- Footer note may say: 进入地区后再选择具体线报.

Primary CTA:
- Large fixed action plate: 进入选定地区.
- Do not include the selected region name in the CTA.
- CTA should be visually primary; 查看任务情报 · 3 is secondary.

Bottom ticker:
- Three low-weight feedback lanes: 地区情报, 档案更新 / 最新记录, 地区预警.
- They must not become a second task summary, tutorial prompt, filter bar, or progress bar.

Typography:
- Use sharp, legible modern Chinese UI type.
- Keep text inside clean content-safe areas.
- Avoid tiny unreadable text, broken Chinese, gibberish, extra English headings, or random pseudo labels.
```

## Negative Checks

- No left-card `目标 / 限时 / 线索 / 深链`.
- No task summary inside the large right body paper.
- No full-width cyan title bar attached to the prose paper.
- No task selection or dispatch controls in the popover.
- No staff, dice, success rate, next-day button, or long action log.
- No production PNG may bake the text from this prompt.
