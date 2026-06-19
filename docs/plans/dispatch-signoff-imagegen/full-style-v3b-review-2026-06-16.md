# 派遣签批台整屏风格稿 v3b

> 日期：2026-06-16  
> 状态：功能分区优先的整屏风格稿候选；可作为下一步 P0 资产拆分和安全区讨论基准，不作为最终生产标杆。  
> 生成方式：内置 `image_gen` 生成无运行时文字美术底稿，再用本地脚本叠加可控中文与安全区 overlay。

## 产物

| 文件 | 用途 | 状态 |
| --- | --- | --- |
| `docs/screenshots/2026-06-16-dispatch-signoff-full-style-v3/01-dispatch-signoff-full-style-v3b-artboard-no-runtime-text.png` | v3b 无运行时文字整屏美术底稿 | 作为功能分区和风格修正候选；仍有少量假字横条风险 |
| `docs/screenshots/2026-06-16-dispatch-signoff-full-style-v3/02-dispatch-signoff-full-style-v3b-filled-preview.png` | 本地叠字后的完整填充态预览 | 给用户评审整体界面观感和信息层级 |
| `docs/screenshots/2026-06-16-dispatch-signoff-full-style-v3/03-dispatch-signoff-full-style-v3b-safe-zone-overlay.png` | `content_rects / no_text_rects / hit_rects` 安全区 overlay | 用于下一步 manifest 和组件拆分讨论 |
| `tmp/ui-screens/render-dispatch-v3b-filled-overlay.ps1` | 中文填充预览脚本 | 工具脚本，不是运行时资源 |
| `tmp/ui-screens/render-dispatch-v3b-safe-zone-overlay.ps1` | 安全区 overlay 脚本 | 工具脚本，不是运行时资源 |

## 为什么选择 v3b

v3b 解决了 v2 的三个核心偏差：

- 纸张从偏黄旧档案转为更干净的暖白 / 浅象牙纸，破败感明显降低。
- 中央已选队员、支援槽、右侧复核纸之间有明确红 / 青线路，能读出“派人 + 支援 -> 达标率 / 风险 / 耗时 -> 签批”的因果链。
- 四区职责更接近真实功能：顶部低权重状态条、左任务简报、中派遣配置台、右签批复核纸。

## 仍未通过生产标杆的点

- 底稿里仍残留少量黑色横条 / 假字式占位，尤其是队员卡头像下方和局部字段附近；进入生产 P0 资产时必须清空。
- 顶部状态条仍有图标化倾向，正式版本应保留抽象状态槽，不烘焙功能结论。
- 左下纸角和右侧纸叠仍有轻微旧物件感；下一步组件生成时纸面必须继续压向新鲜象牙白印刷纸。
- 当前仍是整屏母稿，不是组件 atlas。CTA、队员卡、支援槽、签批纸、状态章都必须拆成独立资产并声明状态矩阵。

## 下一步拆分建议

优先从 v3b 反推 P0 资产：

1. `ds_desk_base_v3b`：只保留深海军蓝桌面、不可交互装饰和低权重半调。
2. `ds_task_brief_sheet_v3b`：左任务简报纸，清空所有假字横条，保留大面积正交安全区。
3. `ds_assignment_tray_v3b`：中央托盘和因果导轨；导轨属于 `no_text_rects`。
4. `ds_selected_slot_atlas_v3b`：3 个已选槽，含 empty / occupied / hover / blocked_full。
5. `ds_staff_card_atlas_v3b`：候选卡，首屏尽量保留完整 dice net。
6. `ds_support_slot_atlas_v3b`：支援道具槽，不占员工位。
7. `ds_review_sheet_base_v3b`：右侧复核纸，承载达标率、风险、耗时、后果和阻断原因。
8. `ds_cta_signoff_atlas_v3b`：签批 CTA，含 default / hover / pressed / disabled / loading / stamped。

## 结论

v3b 可以继续作为“下一轮拆资产和 manifest 的视觉基准候选”。在正式称为生产标杆前，还需要：

- 基于 overlay 收紧真实 `dispatch_signoff_asset_manifest.json` 坐标。
- 对 `ds_*` 组件逐项重生成无假字透明 PNG / atlas。
- 经 `@像素艺术` 复审，重点检查纸张是否仍脏旧、像素颗粒是否成为结构语言、动态文字安全区是否可落地。
- 再做 Godot 接入截图：空队、1 人、2 人、3 人、人数满、天数不足、阻断、pressed / loading / stamped。

## 像素艺术复审

结论：**有条件通过为“下一步拆资产基准候选”，不能称为“生产标杆”。**

已解决：

- 旧档案 / 脏旧 / 过写实问题大部分已解决。v3b 已明显回到深蓝桌面、红橙行动色、干净象牙纸和现代编辑部工作台。
- 三栏签批台的职业物件叙事成立，中央派遣盘与右侧复核纸能支撑派遣签批读法。

剩余 P0 风险：

- 假字横条必须从所有动态文字区移除，尤其是队员卡头像下方和字段附近。
- 顶部 HUD 图标偏通用资源栏，需要改成周刊印刷系统里的短条、压章、裁切标、信号条。
- 纸面折角 / 纸叠可以保留少量层次，但不能脏、破、卷、黄，折角必须退到 `no_text_rects`。
- 右侧盖章按钮偏写实 3D / 旧机器，应转成更扁平的红橙印章压板 / 签批动作入口。
- 金属夹与文具不能抢主视觉，也不能走掉漆旧物件写实路线。

组件化 prompt 修正清单：

```text
clean fresh ivory printed paper, not yellowed archive, no stains, no tea marks, no torn dirty paper
no baked text, no fake glyph bars, no placeholder micro text inside content_rects
empty clean content rectangles for runtime Chinese UI text
2-4px intentional pixel clusters, blocky halftone, subtle red-cyan misregistration, crop marks outside text zones
modern supernatural weekly magazine UI, bold editorial graphic design, deep navy #0F1A2E, vivid red-orange #E84B2C, warm ivory #F5EDD8
flat graphic stamp press CTA, printed approval plate, no glossy 3D knob, no generic mobile game button
printed pictogram icon system, stamp-like HUD marks, not SaaS icons, not mobile resource bars
minimal clean paper stacks, no archive scrapbook, no realistic rusty metal, no sepia paper
```

组件化验收重点：

- 先拆左任务纸、中央派遣托盘、候选卡、右签批纸、CTA、顶部 HUD 六类资产。
- 每类都要有 `content_rects / no_text_rects`，并用中文填充预览做 100% 局部裁切检查。
- 必查假字是否清零、纸纹是否穿过正文、CTA 是否像签批动作、图标是否像 Angus 印刷系统、折角和夹具是否全部退到文字禁入区。
