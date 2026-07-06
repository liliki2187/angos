# World Map WMW Single-State Refill v0.92 Review

Date: 2026-07-03

## Artifact Type

`filled-state text mock / failed geometry sample`

This is not a pass candidate, not a production candidate, not a no-text asset source, and not a runtime placement source.

## Output Files

- Full generated image: `docs/screenshots/2026-06-24-world-map-benchmark-landing/244-world-map-wmw-single-state-refill-v0-92-imagegen.png`
- Failure crop: `docs/screenshots/2026-06-24-world-map-benchmark-landing/245-world-map-wmw-v0-92-right-cta-visible-slant-fail.png`

## Result

**Failed / downgraded.**

The right CTA functional rows still visibly slant inside the text-bearing frame. This violates the WMW hard rule: any component carrying dynamic text, button semantics, hit rect, status, hover, pressed, disabled, or selected state must be 0-degree orthogonal.

v0.92 improved some visual polish over v0.91, but this is irrelevant for pass judgment. Text UI cannot slant.

## Loop Log: v0.92 Text-Bearing Frame Still Slants

- **触发来源**：2026-07-03 用户圈出 v0.92 右侧 CTA 区域，指出“框体内仍是斜的，文字界面绝对不能斜，这是铁律”。
- **原始问题**：v0.92 的右侧三条 CTA 行虽然比 v0.91 更接近正面，但按钮框体与文字承载槽仍有可见倾斜。该区域承载按钮文案、点击语义和状态语义，必须直接失败。
- **失败归因**：父级 Codex 继续使用“整屏有字生图”试图让模型同时解决风格、纸张、低多边形、中文文字和正交功能面。这个路径本身不稳定：模型会把纸张拟物、边缘阴影和轻微透视带进功能行。更严重的是，内置生图工具会先把原始生成图展示给用户，导致未过几何闸门的图先进入用户视野。
- **本轮处理**：将 v0.92 降级为失败样本，新增失败裁切 `245-world-map-wmw-v0-92-right-cta-visible-slant-fail.png`。不再把 v0.92 当作候选继续推进。
- **复发保护**：后续 WMW 资产 UI 化不再用“整屏有字生图”作为正向候选路径。生图只负责无字材质、外轮廓、装饰层、低多边形缩略图和贴纸语言；凡承载文字 / 点击 / 状态的功能面，必须进入可校正的正交资产层或运行时 UI 层，并在展示候选前通过几何 QA。
- **是否沉淀**：已沉淀到本 review、`docs/onboarding/ui-interaction-guidelines.md`、`docs/onboarding/assetized-ui-production-chain.md` 与 `docs/onboarding/ai-collaboration-guidance.md`。文字界面不斜已升级为铁律；若 prompt-only 生图再次产生倾斜，必须停止继续 prompt 微调，转入分层资产 / 正交运行时 UI 工作流。
