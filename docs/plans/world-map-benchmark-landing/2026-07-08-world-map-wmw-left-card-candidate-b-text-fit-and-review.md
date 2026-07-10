# WMW left_region_card 候选 B 文字适配与复审记录

> 日期：2026-07-08  
> 状态：候选 B 复审材料已产出，等待用户裁决“是否够接近标杆”。  
> 约束：不改 `design/ui-contracts/world-map/` frozen 字段；不批量生产其它 class；不压缩 / 裁切素材凑比例。

## 1. 本轮产物

| 编号 | 文件 | 用途 |
| --- | --- | --- |
| 391 | `docs/screenshots/2026-06-24-world-map-benchmark-landing/391-world-map-wmw-v0-9-1-left-card-candidate-b-text-pressure.png` | 候选 B 文字压力检查板 |
| 392 | `docs/screenshots/2026-06-24-world-map-benchmark-landing/392-world-map-wmw-v0-9-1-left-card-candidate-b-review-board.png` | 候选 B 四状态 vs 标杆对应左栏复审板 |
| 393 | `docs/screenshots/2026-06-24-world-map-benchmark-landing/393-world-map-wmw-v0-9-1-light-contract-merge-board.png` | `map_panel` / `top_status_strip` / `icon_badge` 轻合同合并板 |

生成脚本：`scripts/ui-contracts/wmw/wmw_v091_left_card_candidate_b_review.py`。  
内容校验：三张图均为 1920x1080，非黑像素与颜色数量正常。

## 2. 文字压力检查

合同槽位基准：`left_region_card.json` v0.8.2，`label_plate [22,104,114,32]`，`meta_line [22,138,96,10]`，`export_scale = 2`。本轮只跑槽位与字体 / 文案压力，不修改合同。

| 测试项 | 文案 | 测量结果 | 结论 |
| --- | --- | --- | --- |
| 当前最长地区名 | `北美禁区带` | title 190x37 / inner 196x64；meta 144x20 / inner 176x20 | 通过 |
| 当前最长 meta | `异常升温  高危` | title 190x37 / inner 196x64；meta 132x19 / inner 176x20 | 通过 |
| 压力地区名 | `北美禁区警戒带` | title 266x37 / inner 196x64；meta 156x20 / inner 176x20 | 不扩槽；需缩短文案或降到约 30px |
| 压力 meta | `锁定  需12线报` | title 190x37 / inner 196x64；meta 136x21 / inner 176x20 | 不扩槽；需改短 token 或降到约 19px |

结论：

- 当前 389/390 使用的短地区名和短 meta 可以落入合同槽，文字压力检查判为“当前文案通过”。
- `meta_line` 的 10px 参考高度仍是主风险：当前能塞下，但远景读感偏贴边。
- 压力文案不触发合同修改；优先改成短 token，例如 `缺3线报`、`高危`、`荐2`，或等最终字体 token 确定后重跑。

## 3. 候选 B vs 标杆差异点

候选 B 优点：

- 383 无字壳目检未发现烘焙假字；384 比例 / 几何 gate 通过；389 Godot 运行时回填非黑帧且四状态可见。
- 四状态共用同一 `left_region_card` 壳和合同槽，纵向切片链路已跑通。

仍需用户裁决的观感差异：

- 卡片厚度：B 的外框更厚、更像独立 UI 卡；标杆更薄、更贴近整屏地图板。
- label 纸签：B 更干净、方正、可写安全；标杆纸签更融入纸张 / 油墨，但运行时可写安全性更难。
- 图片槽气质：B 是通用低多边形风景，安全但地区识别弱；标杆有更强的场景 / 物件暗示。
- 状态独占性：B 四状态同构成立，但非 selected 也有绿色残边，selected 独占性偏弱。

本轮不把 B 冻结为生产资源。若用户接受 B 的方向，下一步应做局部美术微调后重跑 atlas / Godot；若不接受，应回 brief 再生 / 手修，继续沿用 382 wireframe anchor 与 v0.8.2 合同槽。

## 4. UX 老哥复审摘要

UX 老哥判定：没有 P0；候选 B 卡在“图文融合与视觉可写区质量”，不是 Godot 链路问题。

P1：

- `meta_line` 可读性不足，锁定 / 高危 / 推荐数等关键副信息太贴边。
- selected 状态不够独占，非 selected 卡也有绿色边缘 / 亮线。
- 图文融合仍偏“Label 贴上去”，需要 `label_title` 与 `meta_status` 字体 / 墨色 token。

P2：

- `区域 / 禁区带` 术语混用，若不是业务差异应统一。
- globe badge 与照片槽抢角落注意力。
- warning 状态整卡偏黄，警告三角本身不够红。

只属于 provisional / token 的建议：字号、字重、行高、墨色、文案缩写、meta 信息优先级、selected 发光强弱、状态色皮肤、非 selected 绿边清理。扩大或移动 `label_plate` / `meta_line` / `action_badge` 属于 frozen 合同变更，需升版本并重跑整屏回填。

## 5. 388 manifest 修正

已把 388 manifest 及 Godot 资产目录副本中的三个遗留标签从候选 A 改为候选 B 真实核验记录：

- `no_fake_text`: `manual_check_pass_on_candidate_b_383`
- `functional_faces_orthogonal`: `manual_check_pass_on_candidate_b_384_389`
- `same_state_layout`: `manual_check_pass_on_candidate_b_383_384_389`

同时同步 Godot manifest 中关于 389/390 的输出路径与 windowed opengl3 通过状态。JSON 校验通过，旧字符串扫描无残留。

## 6. 轻合同合并板

本轮只产出一张合并板，不开逐个评审轮，不阻塞候选 B 裁决。

- `map_panel`：烘焙到底图的是深色地图板、低多边形陆块、网格 / 海线、静态纸张边框、无文字地域底纹；pin、路线、选中环、hover、locked / heat overlay、tooltip、文字与点击热区全部运行时。
- `top_status_strip`：低密度草案，参考高度 44-48px，运行时 66-72px；只放 3-5 个状态项，每项 icon 24-32px + 一行短数字，不承载长说明。
- `icon_badge`：基础格 32x32 ref / 64x64 atlas，图标内芯 22-24px ref；不得烘焙文字、数字、地区名，状态色走 token。

## 7. 当前 gate 结论

- 文字压力：当前文案通过；压力地区名 / 压力 meta 记录为字体与短文案 token 待办。
- 视觉复审：候选 B 可进入用户观感裁决；不冻结。
- manifest：遗留候选 A 标签已修正为 B；JSON 校验通过。
- 轻合同：合并板已产出；不写 frozen，不触发批量生产。
