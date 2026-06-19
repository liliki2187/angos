# World Map v7 Difficulty / Recommendation + Task Intel Popover Prompt

> Status: 2026-06-17 A77 filled-state target prompt. Superseded by A79 for the next right-dossier target.  
> Output: `docs/screenshots/2026-06-17-world-map-v7-fusion-b-refined-ux/03-world-map-v7-difficulty-rating-task-intel-popover.png`  
> Rule: this is a target screenshot / visual-density reference only. It must not be used as a production PNG, cut-up UI asset, manifest source, or runtime background.
> Current prompt: `docs/plans/world-map-imagegen-v7/right-prose-task-count-button-prompt.md`.

## Purpose

Generate a desktop 16:9 filled-state target screenshot that tests the latest v7 information architecture:

- left region cards show region-level difficulty and recommendation;
- task-pool information is removed from the left cards;
- the selected-region dossier repeats difficulty / recommendation as confirmation;
- the cyan secondary ticket sits directly below the red / state ticket, shows the task count, and opens a read-only task-intel popover;
- the large region-description paper contains only region prose, not task summaries;
- the page still only chooses and enters a region, not a concrete task.

This target is allowed to contain baked Chinese text because it is only a visual target. Production assets must be no-text component PNGs with runtime text.

## Required State

```text
Selected region: 北美禁区带
Region state: 红线升温 + 可进入
Difficulty: 中等
Recommendation: ★★★★
Reason: 首区主线 / 红线升温 / 素材价值高
Remaining days: 7 天
Primary action: 进入选定地区
Task intel popover: open
Task count on ticket: 3条
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
- compact game UI composition, not a landing page or poster.

Important:
- This is NOT production asset art. It is a filled-state target screenshot for judging information density, typography, and art/text fit.
- Text can be baked only for this mock. Later production PNGs must be no-text components.
- Keep the structure close to the accepted fusion-B layout, but remove redundant task counters from the left cards and from the large right body paper.

Top status strip:
- Left weekly tickets: 探索周 01, 剩余 7 天.
- Right world-state rail: 世界状态, 公信 42, 诡名 18, 声望 31, 守序 26, 狂性 11.
- Week/day tickets and world-state rail must use different visual grammar. The world-state rail should look like a low-weight signal / badge meter, not another white paper ticket.

Left region index:
- Four visible region cards.
- Card 1 selected: 北美禁区带. Show 红线升温 / 可进入, 难度：中等, 推荐 ★★★★, short reason such as 首区主线 or 红线升温.
- Card 2 locked: 东亚神秘地带. Show 锁定, 难度：高, 推荐 ★★, short blocker such as 声望 31/40 or 缺青线 1.
- Card 3 enterable: 太平洋失航带. Show 可进入, 难度：低, 推荐 ★★★.
- Card 4 locked / sealed: 南美红线档. Show 封存, 难度：异常, 推荐 ★, short blocker.
- Do NOT show 目标 / 限时 / 线索 / 深链 counters on the left cards.

Central map:
- North America is selected with a clear pin, selected ring, and route emphasis.
- Other pins are muted. Locked pins look sealed / ghosted.
- Do not place long text labels on the map.

Right selected-region dossier:
- Fixed label: 选定地区 or 区域档案.
- Title: 北美禁区带.
- Next to or below title: compact badges for 难度：中等 and 推荐 ★★★★.
- Keep a visible region image / identity panel near the top, showing a dark city / anomaly signal image in the approved pixel-print style.
- Red / state ticket: 红线升温 / 可进入 / 本周取材区已打开.
- Directly below the red / state ticket, place the cyan secondary task-intel ticket. Its face must include the task count in the standard format: 任务情报 · 3. It is a secondary control, not the primary CTA.
- The large paper body below these tickets must contain only region prose. Use sections such as 地区特征, 本周异变, 可带回素材, 地区预警 / 编辑价值.
- Do not put task summaries, task counters, task names, or task preview rows in the large right body paper.

Task intel popover:
- Show the popover open, anchored near the cyan 任务情报 · 3 ticket under the red / state ticket and expanding leftward without covering the primary CTA.
- Title: 任务情报预览.
- 2-3 compact read-only task preview rows only. Each row can show a rough task type / task name and small tags such as 成本, 条件, 风险, 素材.
- It must not look selectable. No dispatch button, no staff slots, no dice, no success rate, no full task cards, no active row highlight.
- Footer note may say: 进入地区后再选择具体线报.

Primary CTA:
- Large fixed action plate: 进入选定地区.
- Do not include the selected region name in the CTA.
- CTA should be visually primary; 任务情报 · 3 is secondary.

Bottom ticker:
- Three low-weight feedback lanes: 地区情报, 档案更新 / 最新记录, 地区预警.
- They must not become a second task summary, tutorial prompt, filter bar, or progress bar.

Typography:
- Use sharp, legible modern Chinese UI type.
- Keep text inside clean content-safe areas with comfortable padding from tabs, screws, halftone dots, crop marks, stripes, and paper edges.
- Avoid tiny unreadable text, broken Chinese, gibberish, extra English headings, or random pseudo labels.
```

## Negative Checks

- No left-card `目标 / 限时 / 线索 / 深链`.
- No task summary inside the large right body paper; that paper is only 地区特征 / 本周异变 / 可带回素材 / 地区预警 prose.
- No task selection or dispatch controls in the popover.
- No staff, dice, success rate, next-day button, or long action log.
- No production PNG may bake the text from this prompt.
