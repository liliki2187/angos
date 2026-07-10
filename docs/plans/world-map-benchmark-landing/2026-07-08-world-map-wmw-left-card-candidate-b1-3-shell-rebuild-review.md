# WMW left_region_card 候选 B1.3 壳重建评审记录

日期：2026-07-08  
版本：v0.9.5  
范围：仅 `left_region_card`，不重生图、不改合同、不批量生产其它 class。

## 结论

B1.3 按“壳重建”路线修复 B1.1 右缘残带和 B1.2 透明洞：先把 B 壳过宽照片窗口的 `x390..408` 区域补成不透明区域，再把地区照片严格贴入合同 `photo_slot [42,48,390,176]`。  

用户复审判定：B1.3 **视觉失败**。透明窟窿确实补上了，`x390..408,y40..300` 四状态透明像素为 0；但补上的不是重建壳体纹理，而是一条按状态色调出来的程序色带。视觉结果是照片右侧多出一条“镶边”，照片没有像 B 版那样贴到内框，仍然不是干净合成。

因此 B1.3 从“待用户视觉裁决”降级为 `candidate_b1_3_failed_user_review_program_color_band_not_shell_texture`，不得进入冻结或批量生产。

## 产物

| 编号 | 文件 | 说明 |
| --- | --- | --- |
| 426 | `docs/screenshots/2026-06-24-world-map-benchmark-landing/426-world-map-wmw-v0-9-5-left-card-candidate-b1-3-shell-rebuild.png` | B1.3 四状态合成源 |
| 427 | `docs/screenshots/2026-06-24-world-map-benchmark-landing/427-world-map-wmw-v0-9-5-left-card-candidate-b1-3-geometry-qa.png` | 几何 QA |
| 428 | `docs/screenshots/2026-06-24-world-map-benchmark-landing/428-world-map-wmw-v0-9-5-left-card-candidate-b1-3-atlas-2x.png` | 2x atlas |
| 429 / 430 | `docs/screenshots/2026-06-24-world-map-benchmark-landing/429-world-map-wmw-v0-9-5-left-card-candidate-b1-3-runtime-fill.png` / `430-world-map-wmw-v0-9-5-left-card-candidate-b1-3-runtime-fill-qa.png` | Python 运行时回填预览 |
| 431 | `docs/screenshots/2026-06-24-world-map-benchmark-landing/431-world-map-wmw-v0-9-5-left-card-candidate-b1-3-manifest.json` | manifest，已降级 |
| 432 | `docs/screenshots/2026-06-24-world-map-benchmark-landing/432-world-map-wmw-v0-9-5-left-card-candidate-b1-3-right-edge-alpha-qa.png` | 右缘 400% + alpha probe |
| 433 | `docs/screenshots/2026-06-24-world-map-benchmark-landing/433-world-map-wmw-v0-9-5-left-card-b1-2-vs-b1-3-alpha-hole-fix-board.png` | B1.2 vs B1.3 透明洞修复对比板 |
| 434 / 435 | `docs/screenshots/2026-06-24-world-map-benchmark-landing/434-world-map-wmw-v0-9-5-left-card-candidate-b1-3-godot-single-component.png` / `435-world-map-wmw-v0-9-5-left-card-candidate-b1-3-godot-single-component-qa.png` | Godot windowed 单组件截图 |

## Gate 结果

| gate | 结果 | 证据 |
| --- | --- | --- |
| 合同冻结字段 | pass | 未修改 `design/ui-contracts/world-map/left_region_card.json`；`validate_class_contract.py` PASS |
| 几何比例 | pass | 408x320，ratio 1.275 |
| photo_slot mask | pass | 照片只贴入 `[42,48,390,176]` |
| `card_body_opacity_probe` | pass | `x390..408,y40..300` 四状态透明像素均为 0，控制区域也为 0 |
| 非 selected 绿色残留 | pass | `greenish_full_frame_nonselected = pass` |
| `art_shell_texture_integrity` | fail | `x390..408` 是状态色程序填充带，不是 B 壳纹理，也不是照片窗口自然延伸 |
| `right_frame_continuity` | fail | 右边框不再透明，但被程序色带视觉割裂 |
| `layer_order_integrity` | fail | 照片按合同停在 x390，B 壳可见照片窗口约到 x408，18px 冲突区仍未解决 |
| `photo_window_vs_photo_slot_conflict` | needs_decision | 当前规则要求照片槽外 0px 溢出，但 B 壳视觉窗口本身比槽宽约 18px |
| composite_cleanliness | fail | 透明洞已修，但合成仍肉眼可见补丁痕迹 |
| Godot windowed capture | pass | 434/435 由 `scripts/run_wmw_godot_capture_v09.ps1 -SkipRepro` 生成，非黑 / 颜色多样性写入 431 |

## 复盘

这轮不是“透明洞没测出来”，而是把 gate 当成目标本身：上一轮新增 `card_body_opacity_probe` 后，B1.3 只满足了“卡体轮廓内不透明”，没有满足“壳体像一块完整美术”。机器口径从透明洞失败推进到了 alpha pass，但内容目检失败。

根因仍是 **B 壳烘焙的可见照片窗口比合同 `photo_slot` 宽约 18px**。严格要求照片只进 `photo_slot`，同时又要求视觉像 B 版贴到内框，这两条在当前素材上互相冲突。继续局部擦、盖、填只会产生旧照片残带、透明洞、程序色带这一类变体。

## 下一轮只能先裁决 A/B

| 方案 | 做法 | 代价 | 结论 |
| --- | --- | --- | --- |
| A：照片填满可见窗口 | 允许照片美术层贴到 B 壳实际可见窗口约 x408；合同 `photo_slot` 保留为运行时文字 / hit / safe 语义 | 需要显式记录合同语义解释，不改 frozen 几何字段 | 最接近 B 版观感，消灭 18px 缝隙类问题 |
| B：窗口收窄到槽 | 真正重建 18px 壳体纹理，让可见窗口等于 `photo_slot` | 纹理接缝难，仍有美术风险 | 逻辑最纯，但成本和失败概率更高 |

在 A/B 未裁决前，不应继续产出 B1.4 局部补丁，也不应把任何新 gate 改到让色带通过。
