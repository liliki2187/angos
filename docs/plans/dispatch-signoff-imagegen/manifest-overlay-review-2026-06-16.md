# 派遣签批台 P0 Manifest / 安全区 Overlay 复审

> 日期：2026-06-16  
> 对象：`dispatch_signoff_asset_manifest.json`、`06-dispatch-signoff-manifest-safety-overlay.png`  
> 状态：草案通过结构检查；可进入 prompt bundle 与 P0 资产生产准备，但不能称为生产标杆。

## 产物

| 文件 | 说明 |
| --- | --- |
| `gd_project/Assets/ui/angus_packaging/dispatch_signoff/dispatch_signoff_asset_manifest.json` | P0 资产契约，含 16 个资产、15 条决策事实、17 个 QA case |
| `docs/screenshots/2026-06-15-dispatch-signoff-style-draft/06-dispatch-signoff-manifest-safety-overlay.png` | 基于填充态图生成的安全区 overlay |
| `tmp/ui-screens/render-dispatch-manifest-overlay.ps1` | overlay 生成脚本 |

## 本轮合并的关键修正

- 补 `coordinate_space / viewport_base / scale_policy`，防止 16:9 回归时安全区漂移。
- 给文字槽补 `text_slots`：`font_token / color_token / max_chars / align / overflow_policy / min_gap_to_no_text`。
- 把 UX 指出的 `dispatch_eligibility / time_anchors / staff_pool_availability / selected_staff_capacity / support_item_contract / temporary_staff_contract` 写入 `DecisionFactMatrix`。
- 候选区从单一 `candidate_grid` 改为 6 个显式候选卡 mount。
- 右复核纸拆出 `mutually_exclusive_text_slots`，阻断原因与失败后果同槽互斥；CTA 和签批章作为 child mount。
- `ds_approval_stamp_atlas` 标记为 `interactive=false`，防止“可签批”章被当成按钮。

## Overlay 发现并修正的问题

- 顶部左 / 右半调禁字区原本过大，压到标题和员工池文字；已缩小并拆出 `pressure_summary`。
- 中央托盘原本把整个外框标成禁字区，导致所有子组件都被红区覆盖；已改为上下左右边缘禁字区。
- 左侧失败后果槽原本压到底部折角；已缩窄 `failure_short` 并降低最大字数。
- 支援槽与 CTA 的外缘禁字区原本覆盖正文；已改成边缘 / 底部压痕禁字区。

## 仍需后续验证

- 生成真实 P0 PNG 后，必须重新跑 overlay；当前 overlay 只验证草案坐标与填充态观感图的关系。
- 必须补 100% 局部截图：已选槽、候选卡、复核纸、CTA、阻断原因。
- 必须补状态截图：未选人、1 人低达标、2 人变化、3 人满员、天数不足、潜在点不足、道具不可用、临时线人、CTA pressed / confirm_pending / loading / stamped。
- 美术资源生成后必须再交 `angus_art_director` 复审；当前 manifest 不是美术生产标杆。
