# WMW A263 v0.2 局部载体返工交付清单

## 用户审阅入口

> **撤回说明（2026-07-22）**：以下三图不再是等待确认的 PASS 候选，只作为 v0.2 失败证据。用户在完整整屏中发现第三卡状态签右端帽被裁掉；日程和右栏两项修复仍有效。下一次用户主审必须是修复后的完整 1920×1080 整屏与流程对照，不以本清单中的失败图继续请求确认。

1. `wmw-a263-uncoated-fullscreen-default-v0-2.png`
   - 用途：完整 `1920×1080` 默认态主审图。
   - 失败用途：定位第三卡状态签裁切；不再请求用户判断是否通过。
   - SHA-256：`70ff5805ad33b4412d287930bb9a7e19d7b94db43d2b12c9518748ef0018acca`
2. `wmw-a263-uncoated-fullscreen-state-pair-v0-2.png`
   - 用途：完整默认态/推进确认态流程对照。
   - 保留证据：确认态仍只改变日程，最长确认文案空间有效；不代表第三卡通过。
   - SHA-256：`8221af41924ccf95a239a3895fc57527a3204b74b2410d08de964eb928e278b4`
3. `wmw-a263-uncoated-fullscreen-local-qa-v0-2.png`
   - 用途：三个问题区域的 200% 内部 QA 证据，不替代整屏主审图。
   - 失败用途：证明既有 QA 板没有展示 ingredient / 有效窗口 / 端帽比较，因而产生假通过。
   - SHA-256：`4e2501729339b04b4ff4bbe5ef785e5c6b747b5f99972ec44fad7910501dec7e`

## 完整产物

- `wmw-a263-uncoated-fullscreen-default-v0-2.png`
- `wmw-a263-uncoated-fullscreen-schedule-confirming-v0-2.png`
  - SHA-256：`021a332bdadeab1ae214d43042f801b40173752709614de275063619d058c5f1`
- `wmw-a263-uncoated-fullscreen-state-pair-v0-2.png`
- `wmw-a263-uncoated-fullscreen-qa-third-card-v0-2.png`
- `wmw-a263-uncoated-fullscreen-qa-schedule-v0-2.png`
- `wmw-a263-uncoated-fullscreen-qa-dossier-v0-2.png`
- `wmw-a263-uncoated-fullscreen-local-qa-v0-2.png`
- `wmw-a263-uncoated-fullscreen-v0-2-audit.json`
- `render_wmw_a263_uncoated_fullscreen_text_landing_v0_2.py`
- `wmw-a263-v02-third-card-footer-imagegen.png`
- `wmw-a263-v02-schedule-carriers-imagegen.png`

## 状态

`user_visual_review_failed_third_card_endcap_crop_rework_required`。原 UX/UI PASS 已撤回；当前 `P0=0/P1=1`，UI 另保留未来 runtime 清晰度 `P2=1`。本轮未 stage、commit 或 push。
