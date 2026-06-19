# 派遣签批台 review sheet base v1

> 日期：2026-06-16  
> 状态：`ds_review_sheet_base` 工程验证候选；可用于检查裁切、挂载、文字槽和 CTA 拆分，不可称为最终美术生产标杆。

## 产物

| 文件 | 用途 | 状态 |
| --- | --- | --- |
| `gd_project/Assets/ui/angus_packaging/dispatch_signoff/assetized/ds-review-sheet-base.png` | 右侧复核纸 base 候选，`454x860` | 工程验证候选 |
| `docs/screenshots/2026-06-16-dispatch-signoff-full-style-v3/11-ds-review-sheet-base-preview.png` | 空 base 预览 | 检查是否仍烘焙旧 CTA |
| `docs/screenshots/2026-06-16-dispatch-signoff-full-style-v3/12-ds-review-sheet-base-safe-zone-overlay.png` | 安全区 overlay | 检查 `content_rects / no_text_rects / cta_mount` |
| `docs/screenshots/2026-06-16-dispatch-signoff-full-style-v3/13-ds-review-sheet-recompose-with-cta.png` | 真实装配回拼 | 先清掉旧 v3b 右栏，再挂 base + CTA atlas |
| `docs/screenshots/2026-06-16-dispatch-signoff-full-style-v3/14-ds-review-sheet-filled-text-fit-test.png` | 中文填字测试 | 检查 `time_cost / action_scope / blocking_reason` 不进入 CTA |
| `docs/screenshots/2026-06-16-dispatch-signoff-full-style-v3/11-ds-review-sheet-base-report.json` | 构建报告 | 记录裁切、清理区、挂载区和不变量 |
| `tmp/ui-screens/build-dispatch-review-sheet-base.py` | 本地构建脚本 | 工具脚本，不是运行时代码 |
| `gd_project/Assets/ui/angus_packaging/dispatch_signoff/assetized/ds-review-sheet-base-v2-art-pass.png` | v2 美术生成候选，`454x860` | 视觉更自然，但需要重新映射 content rect |
| `docs/screenshots/2026-06-16-dispatch-signoff-full-style-v3/18-ds-review-sheet-base-v2-art-pass-manifest-overlay.png` | v2 美术候选叠当前 manifest | 证明不能直接替换 v1 工程候选 |

## 通过点

- 裁切框已从错误的右侧中段改为整张复核纸：`component_rect = [1260, 130, 454, 860]`。
- 旧 v3b 烘焙红色 CTA 区已从 base 中清掉；真实装配回拼时只剩 `ds_cta_signoff_atlas` 一个动作主体。
- `time_cost` 已从 `action_scope` 中拆成显式事实槽，避免后续按分类检索时漏掉耗时 / 剩余天数。
- CTA 只承载动作标签和按钮状态；`blocking_reason`、`time_cost`、`action_scope` 均归右侧复核纸。

## 未通过 / 风险

- 底部清理区仍偏程序化，纸纹和顶部原生 v3b 纸面存在密度差异。
- 该版本适合作为坐标、装配和文字安全验证，不适合作为美术最终资产。
- 下一轮正式图像生成或修图必须以这个 manifest 坐标为约束，重新生成更自然的空 `cta_mount`：压痕 / 纸层 / 套印裁切标可以保留，但不得出现红色实心按钮、旋钮、按钮文案或假中文。

## v2 美术候选

v2 美术生成图解决了 v1 的程序化纸面问题：纸张比例正好为 `454x860`，左侧图标列、右上红角、底部空压痕 mount 和无文字约束都更自然，也没有烘焙红色 CTA。

但它不能直接替换当前 `ds_review_sheet_base`：

- 当前 manifest 的 `content_rects` 是按 v1 工程裁切重映射的，叠到 v2 上会压到图标列和纸边。
- v2 的字段列更靠右，正式接入前必须重新标定 `summary / probability / risk / time_cost / action_scope / blocking_reason / failure / cta_mount`。
- 在 remap 和 `content_rects` 交叉检查通过前，v2 只能作为美术方向候选，不能作为运行时 final path。

## 复审结论

- `ux_laoge`：P0 风险是双层 CTA 破坏不可逆动作归属；`time_cost / action_scope / blocking_reason` 必须稳定存在。
- `angus_art_director`：P0 风险是红橙主行动色被底图占用；`review_sheet_base` 应是“可签批的空复核纸”，不是“没有文字的红按钮底图”。
