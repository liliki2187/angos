# World Map B7 Branch Filled-State Text Mock Brief

> Date: 2026-06-22  
> Purpose: generate or polish one true `filled-state text mock` after B7 color/style lock and capacity validation.  
> Must read with: `filled-content-contract-b7-2026-06-22.md`, `docs/onboarding/imagegen-color-contract-gate.md`, and `docs/screenshots/2026-06-22-world-map-branch-pixel-grain-experiment/color-contract-v1-b7-strict-pass.md`.

## 1. Artifact Type

Target artifact:

```text
filled-state text mock
```

Allowed use:

- judge real content, typography, hierarchy, state grammar, and art/text fusion
- compare against B7 color-locked style direction
- decide whether this branch deserves another production pass

Forbidden use:

- component slicing
- atlas source
- manifest source
- runtime background
- production benchmark / truth source

## 2. Reference Inputs

| Reference | Path | Role |
| --- | --- | --- |
| B7 strict color pass | `docs/screenshots/2026-06-22-world-map-branch-pixel-grain-experiment/15-variant-b7-strict-color-match-pass.png` | palette, material, pixel grain, main visual direction |
| Capacity validation preview | `docs/screenshots/2026-06-22-world-map-branch-pixel-grain-experiment/17-b7-filled-content-capacity-validation.png` | content placement, exposed capacity risks, required structural corrections |
| Color contract | `docs/screenshots/2026-06-22-world-map-branch-pixel-grain-experiment/color-contract-v1-b7-strict-pass.md` | required palette gate after generation |
| Functional contract | `docs/plans/world-map-branch-pixel-grain/filled-content-contract-b7-2026-06-22.md` | real content and acceptance rules |

## 3. Model Route

If using `openrouter-image-gen`:

| Field | Value |
| --- | --- |
| asset_type | `ui-screen` |
| background | `opaque` |
| model | `nano-banana-2` / `google/gemini-3.1-flash-image-preview` |
| reason | complex UI composition, multiple reference images, heavy layout control, in-image text demands |
| count | `1` |
| aspect_ratio | `16:9` |
| image_size | `2K` |
| slug | `world-map-b7-filled-state-text-mock` |

Do not use a transparent-output route. This is a full opaque UI-screen mock.

## 4. Positive Prompt Draft

```text
Create one desktop 16:9 game UI filled-state text mock for Angus / The World Mystery Weekly world map screen.

Asset identity and game use:
This is a high-fidelity filled-state text mock, not a production asset sheet. It validates a real world-map selection state with real Simplified Chinese UI content, typography, paper slots, status ribbons, CTA, and bottom ticker integrated into the same visual language.

Reference roles:
Use the B7 strict color pass reference as the palette, material, pixel grain, paper relief world map, deep navy editorial board, red-orange and cyan signal accents, left region card stack, right dossier sheet, and bottom receipt-card visual direction. Use the capacity validation preview only as content placement guidance and as a warning list: improve the top status rail, tighten bottom ticker capacity, reserve a cleaner right prose body, and avoid persistent map label clutter.

Scene / layout:
Keep the B7 overall composition: left vertical region index, large central tactile paper-relief world map board, right selected-region dossier, and bottom ticker receipts. If this mock includes `下一天 / 推进一天`, it must reuse the current region task board's bottom global schedule grammar: a dark cyan-black base, gold schedule edge, calendar / arrow signal, independent hit area, and a first-click `确认推进？` confirming state. 2026-06-23 layout target: place this schedule action as a left-bottom independent global schedule dock below the region index, not as part of the region card stack; extend the right selected-region dossier downward into the former lower-right console area to provide more region prose. The lower-right mechanical console must be removed or fully absorbed into the right dossier; it must not read as a `next day`, `advance`, or `end week` machine button. Add a deliberate top status rail on or above the central board for `探索周 01`, `剩余 5天`, and a grouped world-state rail with `公信 42`, `诡名 18`, `声望 12`, `守序 34`, `狂性 16`. The top rail must feel like part of the editorial board, not tiny technical marks.

Filled state:
North America quarantine zone is selected, red-line heating, enterable. The selected state must be consistent across the left card, map pin / selected cue, right dossier, CTA, and ticker.

Real Chinese UI content to render legibly:
Left region index:
- `北美禁区` / `已选` / `难度 高` / `推荐 ★★★★★` / `红线升温`
- `欧洲裂隙` / `可进入` / `难度 中` / `推荐 ★★★` / `线索稳定`
- `东亚镜像城` / `锁定` / `难度 异常` / `公信 42/60`
- `南美遗迹` / `可进入` / `难度 高` / `推荐 ★★★★` / `截稿临近`
- optional if space allows: `非洲夜航线`, `南极静默区`; if six cards make the screen cramped, reduce to four cards but keep one locked region.

Right dossier:
Fixed label `选定地区`.
Title `北美禁区`.
Badges `难度 高` and `推荐 ★★★★★`.
Red ribbon `红线升温 · 3天内进入收益最高`.
Cyan secondary ticket `查看任务情报 · 3`, clearly independent from the prose paper, with a small right-side action cue.
One continuous intro paragraph only: `废弃广播塔复述不存在的晨间新闻。封锁线外出现同步采访记录，三名目击者都听见尚未出生的播报员。`
Footer line: `进入消耗 1 天，解锁区域任务台。`
Primary CTA: `进入选定地区`.

Bottom ticker:
Three low-weight clickable detail entrances:
- `地区情报` / `封锁线重复采访`
- `档案更新` / `镜像缺口更新`
- `地区预警` / `失败损失公信`

Left-bottom global schedule dock:
- `推进一天`
- supporting status: `Day 1 / 剩余 5天`
- nearby schedule summary: `当前派遣 0 / 5`, `预计返报 1天后`
- confirming state target: `确认推进？`

Map labels:
Do not label every pin persistently. Show a compact selected label for `北美禁区`; optionally show one hover-style label or one locked marker. Keep the central map mostly visual and readable.

Materials and style:
Preserve the exact B7 color family and brightness: warm ivory paper, deep navy board, red-orange alert, restrained cyan signal, dark ink. Preserve the strict B7 color contract as much as the model allows. Maintain intentional pixel-print / halftone material: 2-4px and 5-8px block clusters, crisp printed edges, red-cyan misregistration, low-poly faceted paper map, tactile paper layers. Keep the paper clean and modern, not yellowed, not sepia, not old archive.

Typography:
Chinese UI text must be legible, aligned, and integrated like printed ink / field labels on paper, not default web labels pasted on top. Text should have enough quiet paper behind it; no paper grain, folds, halftone, arrows, clips, screws, tabs, or stripes should cross through important text.
```

## 5. Negative Constraints

```text
Do not include watermark, signature, artist name, copyright stamp, presentation mockup, random stickers, accidental logos, misspelled typography, unreadable Chinese text, garbled characters, pseudo-Chinese, extra task cards, staff cards, dice, success rate, dispatch controls, standalone lower-right day-advance button, next-day lever, end-week button, full action log, tutorial copy, task selection controls, fake production annotations, over-yellowed paper, sepia, old newspaper, old archive, dirty stains, coffee paper, warm wood desk, rusty metal console, generic sci-fi dashboard, SaaS panels, glassmorphism, oversaturated colors, muddy details, jpeg artifacts, noisy photographic paper grain, persistent labels on every map pin, text crossing folds or halftone, CTA with region name inside the button.
```

## 6. Post-Generation Gate

The result may only be called a candidate `filled-state text mock` if:

1. It is not full of garbled / unreadable Chinese. If text is mangled, stop and downgrade to visual inspiration.
2. It still passes the B7 Color Contract Gate or is clearly marked as color-failed.
3. The top status rail is deliberate and readable, not tiny filler.
4. `北美禁区` is selected consistently across left card, map, right dossier, CTA, and ticker.
5. The CTA says fixed `进入选定地区`, not `进入北美禁区`.
6. The right dossier body is one intro paragraph only; no task list or task operation appears there.
7. `查看任务情报 · 3` reads as an independent secondary ticket, not a prose-paper title.
8. Bottom ticker lanes are low-weight detail entrances, not task cards.
9. Locked region state is visually distinct from enterable state.
10. If `推进一天` appears, it is in the bottom global schedule strip with a confirming state and does not compete with the primary CTA; any separate lower-right device does not read as a time-advance / next-day control.
11. Pixel / halftone / paper material remains structural, and the image does not slide into old paper, old archive, or high-definition photography noise.

If any of these fail, the image remains a failure sample or inspiration draft. Do not proceed to asset grouping.
