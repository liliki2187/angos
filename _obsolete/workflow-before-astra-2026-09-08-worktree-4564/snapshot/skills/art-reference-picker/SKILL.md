---
name: art-reference-picker
description: Review local art-reference images for the Angus project, compare them against project docs, and select the most relevant images with concrete fit reasons. Use when the user asks to analyze downloaded screenshots, pick the best references for current UI or art needs, explain project relevance, archive selected images, or send chosen images with reasons to a Feishu group.
---

# Art Reference Picker

Read only the project docs and image files needed for the current request. Prefer:

- `README.md`
- `docs/plans/art-development-plan.md`
- `docs/plans/ui-design-plan.md`
- the relevant files under `design/references/original-art/`

Use `view_image` for any candidate image you are going to judge. Do not guess from filenames alone.

## Workflow

### 1. Build project fit criteria

Before ranking any image, reduce the current Angus need to concrete criteria from the docs. Typical criteria:

- `复古报刊感`
- `黑色幽默 + 克苏鲁/怪谈气质`
- `高信息密度 UI / 卡牌化界面`
- `探索、线索、编辑部、档案感`
- `适合当前阶段的参考价值`

Current stage usually favors UI layout, style direction, and card/editor motifs over final-key-art polish.

### 2. Inspect images and score them

For each candidate image, judge at least:

- motif match to Angus
- direct use for current UI or art tasks
- uniqueness versus other references in the same batch
- risk of sending noise or over-specific inspiration

Keep the selection bar high. It is better to send 1 strong reference than 5 weak ones.

### 3. Write reasons in this format

Use concise Chinese by default:

```text
这张我保留，理由：
1. 它最贴合……
2. 对我们当前的……阶段直接有帮助
3. 可转译成项目里的……
```

Do not use generic praise. Tie each reason to an Angus system, screen, or art task.

### 4. Sending to Feishu

When the user asks to send selected images to Feishu:

1. Use `claude-to-im/scripts/send-feishu-images-post.mjs`.
2. Prefer `--separate` so each selected image is its own message.
3. Use a short title, usually one line naming the motif.
4. Put the relevance reason in the caption, not as a separate dump.
5. If one image was previously sent with bad text, resend that image cleanly instead of referencing the broken message.

### 5. Archiving

If the task includes organizing references in the repo:

- store originals under `design/references/original-art/<date-or-range>/raw/...`
- keep generated contact sheets or crops under `analysis/`
- add a short README only if it helps future retrieval

## Resource

Use `scripts/rank_art_references.mjs` to produce a quick filename list from a directory when the batch is large. The script is only for inventory. Final judgment still requires visual inspection.
