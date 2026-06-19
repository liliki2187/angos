# 派遣签批台 CTA atlas v1

> 日期：2026-06-16  
> 状态：`ds_cta_signoff_atlas` 透明 PNG 候选；用于验证第一批组件化资产，不代表整套派遣签批台已经生产完成。  
> 生成方式：内置 `image_gen` 生成绿幕源图，本地 chroma-key 抠除，再按 alpha 自动分 6 帧规范到 manifest 尺寸。

## 产物

| 文件 | 用途 | 状态 |
| --- | --- | --- |
| `docs/screenshots/2026-06-16-dispatch-signoff-full-style-v3/05-ds-cta-signoff-atlas-source-chromakey.png` | 绿幕源图 | 仅作来源留档 |
| `docs/screenshots/2026-06-16-dispatch-signoff-full-style-v3/06-ds-cta-signoff-atlas-source-alpha.png` | 抠除绿幕后透明源 | 中间产物 |
| `gd_project/Assets/ui/angus_packaging/dispatch_signoff/assetized/ds-cta-signoff-atlas.png` | 正式候选 atlas，`1044x92`，6 帧 | 当前 CTA atlas 候选 |
| `docs/screenshots/2026-06-16-dispatch-signoff-full-style-v3/07-ds-cta-signoff-atlas-preview.png` | 深蓝底预览图 | 用于肉眼检查状态差异 |
| `docs/screenshots/2026-06-16-dispatch-signoff-full-style-v3/07-ds-cta-signoff-atlas-report.json` | 自动分帧报告 | 记录源 bbox 和放置 rect |
| `docs/screenshots/2026-06-16-dispatch-signoff-full-style-v3/08-ds-cta-signoff-atlas-label-test.png` | 中文标签测试图 | 检查 `签批外勤` 是否适配 `label` 安全区 |
| `docs/screenshots/2026-06-16-dispatch-signoff-full-style-v3/09-ds-cta-signoff-atlas-recompose-default.png` | default 态整屏回拼 | 检查 CTA 放回 v3b 后的全局融合 |
| `docs/screenshots/2026-06-16-dispatch-signoff-full-style-v3/10-ds-cta-signoff-atlas-recompose-states.png` | 六状态右下局部回拼 | 检查状态差异、跳变和文字安全区 |
| `tmp/ui-screens/build-dispatch-cta-atlas.py` | 绿幕源转 atlas 脚本 | 工具脚本，不是运行时代码 |
| `tmp/ui-screens/render-dispatch-cta-atlas-label-test.ps1` | CTA 中文标签测试脚本 | 工具脚本，不是运行时代码 |
| `tmp/ui-screens/render-dispatch-cta-recompose-test.py` | CTA 回拼测试脚本 | 工具脚本，不是运行时代码 |

## 帧顺序

`default / hover / pressed / disabled / focus / loading`

每帧大小：`174x92`。  
整图大小：`1044x92`。

## 通过点

- 六帧状态视觉区别清楚，且同属于 v3c 的红橙签批压板语言。
- 没有文字、数字、按钮文案或假标签；中央保留运行时 CTA label 安全区。
- 已从绿幕源图转成透明 PNG，能进入 Godot `TextureButton` atlas 验证。
- 尺寸与 `dispatch_signoff_asset_manifest.json` 中 `ds_cta_signoff_atlas.final_size` / `frame_size` 一致。
- 中文标签测试后，CTA 只保留主动作 `签批外勤`；`消耗 2 天` 不再放入 CTA，改由右侧复核纸 `time_cost / action_scope` 承载。
- 回拼后六状态差异可见，`default / hover / pressed / disabled / focus / loading` 均能识别为同一物件的状态变化。

## 待验收点

- 需要在 Godot / 回拼预览里验证：default、hover、pressed、disabled、focus、loading 六态是否都像同一物件，而不是换图跳变。
- 需要在 Godot 中确认中文 `签批外勤` 能落在 `label` rect 内，不压装饰边。
- `loading` 帧目前更像 stamped / overprint 态，若后续需要明确旋转或进度反馈，应另做局部动画层，而不是在 CTA 中烘焙通用 spinner。
- 这只是第一批组件资产，不证明任务纸、员工卡、复核纸等组件已经可落地。

## 回拼发现

CTA atlas 本体可以继续作为候选资产，但 v3b 整屏底图当前已经烘焙了一个大红签批按钮。把透明 CTA 回拼到 v3b 上时会出现“双层 CTA”观感。这不是 CTA atlas 自身的问题，而是提醒下一步生产 `ds_review_sheet_base` 时必须重出或清理右侧复核纸：复核纸只能提供空 `cta_mount` 和纸面装饰，真实按钮必须只来自 `ds_cta_signoff_atlas`。
