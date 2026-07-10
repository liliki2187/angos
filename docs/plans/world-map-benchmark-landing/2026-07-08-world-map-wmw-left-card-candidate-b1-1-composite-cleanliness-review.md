# WMW left_region_card 候选 B1.1 v0.9.3 合成清理复审

日期：2026-07-08  
范围：仅修 `left_region_card` 候选 B1 的程序合成叠化；不重新生图、不改合同、不扩展其它 class。  
合同：`design/ui-contracts/world-map/left_region_card.json`（frozen 字段未改）

## 结论（已被用户复审修订）

B1.1 不是视觉通过版本。406 合成源、407 几何 QA、408 atlas、409/410 Python 回填、412/413 Godot windowed 截图均已生成，非黑 / 比例 / greenish 等机器口径通过；但用户在 414 对比板右侧明确圈出四状态右侧边缘仍有竖向接缝 / 暗带 / 源裁片边缘残留。因此 411 manifest 已降级为 `composite_cleanliness = fail`。

B1.1 仍是失败候选，不是冻结生产资源；确认前不得批量生产其它 class。

## 输入与修法

| 项 | 路径 / 编号 | 说明 |
| --- | --- | --- |
| B 壳 | `383-world-map-wmw-v0-9-1-left-card-imagegen-candidate-b.png` | 保留卡壳、地球徽章、四状态 badge 与 204x160 合同比例 |
| B1 照片源 | `396-world-map-wmw-v0-9-2-left-card-imagegen-candidate-b1-r4-wide-failed.png` | 仅裁地区感照片内容；避开源图地球徽章和源卡边框 |
| B1 缺陷对照 | `397` / `403` | 双地球、warning 双三角、欧洲照片越界、locked 绿条 |
| 合成脚本 | `scripts/ui-contracts/wmw/wmw_v093_left_card_b11_vertical_slice.py` | 逐卡正规化到 408x320，photo_slot 硬掩膜，B 壳图标单轨制 |
| Godot capture | `gd_project/tests/capture_world_map_wmw_left_card_runtime_v09.gd` | 切到 B1.1 atlas 与 412/413 输出；保留 `RenderingServer.frame_post_draw` 与全黑帧拒绝 |

## 四项缺陷修复记录

| 缺陷 | B1 问题 | B1.1 修法 | 证据 |
| --- | --- | --- | --- |
| 双地球 | 照片裁片带入 396 的羊皮纸地球，叠在 383 白线地球下 | 照片裁窗左侧内收，贴图后只用圆形遮罩恢复 383 的 B 壳地球 | 406、412、414 |
| warning 红三角双层 | 运行时叠了额外红三角，与素材 baked 三角错位 | 删除运行时叠罩路线；只对 baked badge 三角亮笔画做素材层修色 | 406、412、414 |
| 欧洲灰域照片越界 | 裁片带源卡白边并顶出 photo_slot 上边界 | 每张照片先 fit 到 2x photo_slot `[42,48,348,128]`，只在槽内 alpha-composite | 407、410、413 |
| locked 绿条 / greenish 口径 | 旧统计只看 32px 外缘，漏掉可见残边 | 非 selected 全帧 artifact-green 清理；manifest 改为全 408x320 帧统计 | 411、414 |
| 右缘竖带 / 暗色接缝 | B1.1 四状态右侧仍有竖向边缘带，用户复审圈出 | 未修复；这是本轮目检漏判 | 用户标注图、414 |

## Gate 结果

| gate | 结果 | 口径 |
| --- | --- | --- |
| geometry_ratio_1_275 | PASS | 四状态 atlas 帧均为 408x320，比例 1.275 |
| photo_slot_mask | PASS | 2x 槽位 `[42,48,390,176]`，照片槽外不写像素 |
| single_icon_track | PASS | 地球和四状态 badge 均来自 B 壳；无运行时 warning 叠罩 |
| greenish_full_frame_nonselected | PASS | available / warning / locked 全帧 artifact-green = 0 |
| composite_cleanliness | FAIL | 用户复审发现四状态右缘竖向接缝 / 暗带；先前“无接缝、无源图残留”判断撤回 |
| Godot windowed capture | PASS | 412/413 使用 windowed opengl3；非黑与颜色多样性通过 |

## 复盘摘要

这次失败不是 Godot 截图失败，也不是 `greenish` 统计失败，而是验收对象错了：我把“右侧绿色残留”缩窄成饱和 greenish 像素问题，修掉了能被阈值抓到的颜色，却没有把低饱和竖向接缝 / 源裁片边缘作为独立否决项。414 对比板又把卡片缩小，导致我把右缘竖带误读为卡壳阴影或可接受边框。

后续修 B1.2 前，`composite_cleanliness` 必须新增右缘 close-up：四状态各裁右侧 32px-48px，100% / 200% 并排检查，逐张确认无竖向色带、无源裁片边缘、无旧照片内容残留后才能写通过。

## 输出索引

| 编号 | 文件 | 用途 |
| --- | --- | --- |
| 406 | `world-map-wmw-v0-9-3-left-card-candidate-b1-1-composite-clean.png` | B1.1 四状态合成源检查板 |
| 407 | `world-map-wmw-v0-9-3-left-card-candidate-b1-1-geometry-qa.png` | 几何 / slot / action QA |
| 408 | `world-map-wmw-v0-9-3-left-card-candidate-b1-1-atlas-2x.png` | 2x atlas |
| 409/410 | Python runtime fill / QA | title/meta token 回填与槽位 overlay |
| 411 | `world-map-wmw-v0-9-3-left-card-candidate-b1-1-manifest.json` | B1.1 manifest，含 `composite_cleanliness` |
| 412/413 | Godot single-component / QA | 真实 windowed 运行截图 |
| 414 | `world-map-wmw-v0-9-3-left-card-b1-vs-b1-1-composite-fix-board.png` | B1 vs B1.1 四缺陷对比板 |

## 流程沉淀

- `docs/onboarding/ai-collaboration-guidance.md` 已补“几何 / 统计 gate 不能替代内容目检”的程序合成叠化错题。
- `docs/onboarding/assetized-ui-production-chain.md` 已补 `composite_cleanliness` 到 manifest、截图验收、失败模式和交付前检查表。
