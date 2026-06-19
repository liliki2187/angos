# World Map v7 Filled-State Text Mock v3 Review

> Draft: `docs/screenshots/2026-06-16-world-map-v7-functional-style-draft/04-world-map-v7-filled-state-text-mock-v3.png`  
> Prompt: `docs/plans/world-map-imagegen-v7/filled-state-text-mock-prompt.md`  
> Status: revised target screenshot / visual-density reference only. Not a production asset.

## User Feedback Addressed

- Removed the top-strip `阶段：取材` slot.
- Expanded the macro-attribute area so all five values render in one row and the last chip (`狂性 11`) is not cropped.
- Replaced the third bottom lane from a tutorial-like `进入提示` with a system-relevant `地区预警` lane.

## v3 Field Contract

Top strip:

```text
探索周 01 | 剩余 7 天 | 公信 42 | 诡名 18 | 声望 31 | 守序 26 | 狂性 11
```

Bottom receipts:

```text
地区情报：城市频道持续升温
任务小结：红线 1 / 青线 1
地区预警：进入暂无惩罚
```

`地区预警` is the stable third-lane role. It can show no penalty in the current selected state, but the same slot may later show region-level entry impact such as fatigue, reputation loss, lock risk, abnormal contamination, pursuit pressure, or other debuffs.

## Visual Check

- The top status strip no longer spends width on the phase label.
- The five macro attributes are complete and readable in the generated target screenshot.
- The bottom third lane now reads as a region warning / entry impact receipt, not as a tutorial prompt or second CTA.
- The overall six-zone layout remains unchanged from v2, so this is a field-contract refinement rather than a visual reset.

## Remaining Rule

This v3 image is still a text mock. Production components must remain no-text assets with Godot / HTML rendering the exact macro values, region warning text, ticker content, region name, CTA label, and state text dynamically.
