# World Map WMW Single-State Refill v0.91 Review

Date: 2026-07-02

## Artifact Type

`filled-state text mock / single-state refill candidate`

This is a generated visual target for review. It is not a no-text production asset, not an atlas, not a runtime screenshot, and not a final world-map replacement.

## Source Rules

- Accepted component carrier contract: `docs/screenshots/2026-06-24-world-map-benchmark-landing/223-world-map-wmw-component-carrier-contract-v10-v0-89.png`
- Accepted carrier manifest: `docs/screenshots/2026-06-24-world-map-benchmark-landing/224-world-map-wmw-component-carrier-contract-v10-v0-89.json`
- No-text / palette reference: `docs/screenshots/2026-06-24-world-map-benchmark-landing/140-world-map-wmw-paper-atlas-v3-refill-v0-66-info-gray.png`
- WMW branch visual reference: `docs/screenshots/2026-06-24-world-map-benchmark-landing/95-world-map-imagegen-color-recorrected-v0-51.png`

## Output Files

- v0.90 first pass: `docs/screenshots/2026-06-24-world-map-benchmark-landing/229-world-map-wmw-single-state-refill-v0-90-imagegen.png`
- v0.90 crops / QA: `230` through `235`
- v0.91 focused fix: `docs/screenshots/2026-06-24-world-map-benchmark-landing/236-world-map-wmw-single-state-refill-v0-91-imagegen.png`
- v0.91 crops / QA:
  - `237-world-map-wmw-v0-91-left-cards-crop.png`
  - `238-world-map-wmw-v0-91-right-dossier-crop.png`
  - `239-world-map-wmw-v0-91-cta-crop.png`
  - `240-world-map-wmw-v0-91-bottom-receipts-crop.png`
  - `241-world-map-wmw-v0-91-center-map-crop.png`
  - `242-world-map-wmw-v0-91-crop-contact-sheet.png`

## Real State Filled

- Selected region: `北美禁区带`
- State: `红线升温`
- Risk stamp: `高危 / 推荐 2`
- Primary CTA: `进入北美禁区 · 消耗1天`
- Secondary CTA: `查看任务情报 · 线报3`
- Deadline CTA / warning: `红线截止 · 4天`
- Bottom receipts: `本周行动 / 余 6 天`, `情报余量 / 线报 3`, `红线台账 / 4天后升温`

## v0.90 Local QA

v0.90 established the overall direction, but it failed the receipt carrier rule:

- Bottom receipt text became large paper-card headings.
- It did not read as text inside the dark `receipt_field_lane`.
- It was superseded by v0.91 and should remain only as an iteration record.

## v0.91 Local QA

Status update on 2026-07-03: **failed / downgraded**.

The original 2026-07-02 note incorrectly said v0.91 could enter user review. That was a false pass. The user pointed out that the CTA rows were still visibly tilted. A follow-up geometry QA crop confirms this:

- `docs/screenshots/2026-06-24-world-map-benchmark-landing/243-world-map-wmw-v0-91-cta-tilt-fail-qa.png`

Approximate row-edge checks on the CTA crop show about `0.7 deg` to `1.4 deg` tilt, exceeding the `0.5 deg` hard gate. Therefore v0.91 must not be used as a pass candidate, production candidate, or downstream source.

What v0.91 still improved:

- CTA text sits inside the button label plates better than v0.90, but the rows themselves are not orthogonal and therefore fail.
- Right dossier title has a visible gray title lane, with status lane below.
- Bottom receipt text now sits in dark printed lanes, preserving the v0.89 `receipt_field_lane` rule.
- Left cards keep selected / available / warning / locked states readable.
- The central map preserves the selected North America state and low-poly block language.
- Color/material direction stays close to the WMW branch: deep navy background, muted olive, teal, rust red, warm gray paper.

Failed gates:

- CTA functional rows are still tilted; functional front faces are not axis-aligned.
- The review used crop + subjective visual judgment but did not run the required `ui_geometry_gate` before saying it could enter user review.
- The assistant treated "better than v0.90" as enough for user review, which violated the hard rule: functional component geometry fails first, then style is irrelevant.

Watch items before any future production-like claim:

- Generated image size is `1672x941`, not the target `1920x1080`; this is acceptable for review only.
- Chinese text is baked into the generated mock. Production must still rebuild dynamic text in runtime or generate no-text assets.
- This candidate is a filled-state visual target, not a cuttable source. Do not cut UI components from it.
- If accepted by user, next step is to produce a no-text / dynamic-text asset brief and a runtime placement manifest derived from v0.89, not from the baked text pixels in v0.91.

## Next Gate

Do not ask the user to approve v0.91.

Next valid revision must:

1. Start from the accepted v0.89 carrier contract.
2. Make the CTA/front-facing functional rows exactly axis-aligned.
3. Run geometry QA before any user-facing pass claim.
4. Attach a CTA crop with true horizontal guide lines and measured edges.
5. Only then ask the user to review the next single-state refill candidate.

If rejected:

1. Identify whether the failure is color/material, carrier alignment, typography, component style, or full-screen layout.
2. Fix only that class of issue.
3. Re-run 100% crops before producing a new full-screen claim.

## Loop Log: v0.91 Tilt False Pass

- **触发来源**：2026-07-03 用户指出 v0.91 CTA 区域“还是斜的”，并追问为什么硬规则和 Loop 没有校验出来。
- **原始问题**：v0.91 的右侧 CTA 功能行仍有可见倾斜。由于 CTA 承载动态文字、点击、状态和行动语义，按 A124 与 `ui_geometry_gate` 必须一票否决。
- **失败归因**：父级 Codex 把 `100% crop + 肉眼粗判` 当成了几何 QA；没有画贴住真实边缘的水平参考线，没有量化角度，也没有把 `axis_aligned == true` 当作用户评审前置条件。文档规则存在，但没有绑定到放行动作，因此 Loop 记录没有真正拦截产物。
- **本轮处理**：生成 `243-world-map-wmw-v0-91-cta-tilt-fail-qa.png`，用水平参考线和近似边缘角度标出 CTA 行 `0.7 deg` 到 `1.4 deg` 的倾斜，并将 v0.91 从“待用户把关候选”降级为失败样本。
- **复发保护**：后续所有资产化 UI 生图 / mock，只要声称可进入用户把关、生产候选、资源候选或落地候选，必须先附 `ui_geometry_gate` 证据；没有角度 QA，只能说“几何未验证”，不得说“基本正交”“可进入把关”。
- **是否沉淀**：已沉淀到本 review、`docs/onboarding/assetized-ui-production-chain.md`、`docs/onboarding/ui-interaction-guidelines.md` 与 `docs/onboarding/ai-collaboration-guidance.md`。规则已从“生产候选前触发”前移到“用户正向把关前也必须触发”。
