# WMW A263 v0.3 第三卡 footer 交付清单

## 用户审阅入口

本轮不是让用户审孤立按钮。请按以下顺序看完整界面，再用流程板确认状态关系；技术拆图只负责解释为什么这次不会再裁断。

1. `wmw-a263-uncoated-fullscreen-default-v0-3.png`
   - **这是什么**：完整 1920×1080 默认态，是本轮主审图。
   - **为什么现在看**：确认修好的第三卡放回整页后是否自然，是否仍属于已选择的方案 1。
   - **需要判断**：整屏观感是否接受；第三卡“锁定”是否像完整只读状态签，而不是被截断按钮。
   - SHA-256：`78c1098d4010c4733d1b1c96c734b665185d3ab2d35c0867e34be93b06374ddc`
2. `wmw-a263-uncoated-fullscreen-state-pair-v0-3.png`
   - **这是什么**：默认态与推进二次确认态的完整并排流程板。
   - **为什么现在看**：保证第三卡修复没有破坏日程二次确认，且两态仍只在日程区变化。
   - **需要判断**：确认态是否仍清楚、整页是否没有跳动或意外改色。
   - SHA-256：`0a1ff9374fd0c4c42fa3594cecfe6bf5c411bad241e9b3c5a4be753e3be75250`
3. `wmw-a263-uncoated-fullscreen-third-card-mapping-qa-v0-3.png`
   - **这是什么**：完整 ingredient → source crop → 最终 100% / 200% → 端帽 400% 的全流程证据板。
   - **为什么现在看**：解释本次素材如何落入整屏，以及 v0.2 裁切错误为何已被结构性消除。
   - **需要判断**：一般无需做美术裁决；如需核验，只看左右端帽是否完整、右边是否留白。
   - SHA-256：`ca1396495efe96b09137279a0e5855fb14f665cefd1ea0bc954fc67d05db72c5`

## 完整产物

- `wmw-a263-v03-third-card-footer-imagegen.png`：built-in imagegen 项目内最终 ingredient，SHA-256 `d76b360933926af2c6f43bf788c0443854e330b45d47ebcdcca8efee83986c26`；
- `wmw-a263-uncoated-fullscreen-default-v0-3.png`；
- `wmw-a263-uncoated-fullscreen-schedule-confirming-v0-3.png`，SHA-256 `1871ca00707fda640d5783559bfac3f0e64a4c6b706fa63bce7fe9df82124c2a`；
- `wmw-a263-uncoated-fullscreen-state-pair-v0-3.png`；
- `wmw-a263-uncoated-fullscreen-local-qa-v0-3.png`；
- `wmw-a263-uncoated-fullscreen-qa-third-card-v0-3.png`；
- `wmw-a263-uncoated-fullscreen-qa-schedule-v0-3.png`；
- `wmw-a263-uncoated-fullscreen-qa-dossier-v0-3.png`；
- `wmw-a263-uncoated-fullscreen-third-card-mapping-qa-v0-3.png`；
- `wmw-a263-uncoated-fullscreen-v0-3-audit.json`，SHA-256 `6e4727f3c35f6d274044363bb974a63a13eee1cea0106ba4090989c75ffa4ca7`；
- `render_wmw_a263_uncoated_fullscreen_text_landing_v0_3.py` 与共享 v0.2 装配脚本。

## 状态与边界

`dual_reviewed_pending_user_visual_confirmation`。UX/UI 均 `PASS / P0=0 / P1=0 / P2=0`。未修改 Godot、runtime、atlas、正式合同、frozen compact A5.1、B2.12 或 GDD；本轮未 stage、commit 或 push。

