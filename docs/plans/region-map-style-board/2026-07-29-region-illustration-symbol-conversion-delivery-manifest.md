# 区域任务配图抽象符号转换 V6 交付清单

## 决策条

- **结论**：V6 已关闭微缩模型问题，但用户回填整屏复核后判定其又过于极简；当前降级为 `ICON` 层下限诊断，不再是待采纳对象—画法参考。
- **影响**：V6 能证明“过写实端已经离开”，不能证明命中标杆。任务母图应重新定位到 `PHOTO & SNAPSHOT` 的简化端。
- **下一步**：停止整屏回填，先生成四联 PHOTO 母图＋真实左卡 `1×`＋整屏 `25%` 三尺度证据。

## 产物身份

- `artifact_type = visual_style_reference`
- `state = region_task_illustration_symbol_conversion_v6`
- `status = user_rejected_over_minimal_icon_layer_diagnostic`
- `production_candidate = false`
- `runtime_implemented = false`
- `scope_invariant = standalone_style_board_no_screen_geometry_claim`

## 当前交付

- V6 四联板：`image_gen/2026-07-28/region-map-map-variants-v1/35-region-illustration-symbol-conversion-v6-review.png`
- 源失败样本 / V6 对照：`image_gen/2026-07-28/region-map-map-variants-v1/36-region-illustration-source-vs-conversion-v6.png`
- V6 25%：`image_gen/2026-07-28/region-map-map-variants-v1/37-region-illustration-conversion-v6-25pct.png`
- V6 独立暖纸卡：`image_gen/2026-07-28/region-map-map-variants-v1/38-region-illustration-conversion-v6-cards.png`

## 诊断过程

- V1：`21-region-illustration-symbol-conversion-v1.png`
- V2：`25-region-illustration-symbol-conversion-v2.png`
- V3：`29-region-illustration-symbol-conversion-v3.png`
- V4：`30-region-illustration-symbol-conversion-v4-paper-balanced.png`
- V5：`34-region-illustration-symbol-conversion-v5-factory-shadow.png`

`image_gen/` 被 `.gitignore` 忽略；图片已落入工作区，但不进入 Git 追踪。

## Gate

| Gate | 结果 | 说明 |
| --- | --- | --- |
| 真实生图 | `pass` | 六轮均由内置 `imagegen` 生成 / 编辑 |
| 微缩模型退役 | `pass_visual` | 无等距地台、AO、接触阴影和建筑零件清单 |
| 四种主剪影 | `pass_visual` | 大碟、竖楔、横块、低锯齿带互不混淆 |
| 低多边形颗粒 | `pass_visual` | 采用少量宽大硬边面，没有碎三角滤镜 |
| 四个异常关系 | `pass_visual` | 背向信号、高空鱼、投影假烟囱和低头接收均成立 |
| 25% 无标题阅读 | `pass_visual` | 四对象可辨，异常没有塌缩为写实零件 |
| 独立暖纸单卡 | `pass_visual` | 不再像可拿起摆放的建筑模型 |
| 防通用按钮化 | `pass_after_revision` | V2 厂房 / 天线城失败，V6 已补回非正常因果 |
| 暖纸合同 | `pass_after_revision` | V2 / V3 压花偏黄，V4–V6 收回暖灰无涂布区间 |
| UI Designer | `pass` | `P0=0 / P1=0 / P2=2` |
| UX 老哥 | `pass` | `P0=0 / P1=0 / P2=1` |
| 标杆图像层级 | `fail_after_user_review` | V6 落到 `ICON / GRAPHIC ELEMENTS`，缺少 PHOTO 层的现场与环境信息 |
| 三尺度验收 | `missing` | 未同时提交四联母图、真实左卡 `1×` 与整屏 `25%` |
| 整屏回填 | `blocked` | 待用户裁决，尚未生成同源缩略图与状态回填 |
| 生产候选 | `blocked` | 未冻结资产尺寸、透明通道、同源裁切、atlas 或 runtime |

## P2 观察项

- 厂房锈橙假烟囱在 25% 下视觉权重稍强，可能短暂读成独立标记。
- 低头天线末端略像吊钩；回填到真实任务卡最终尺寸时必须再次复核。

## 用户复核后的状态修订

- 回填诊断稿：
  - `image_gen/2026-07-28/region-map-map-variants-v1/39-region-map-a2-5-v6-symbols-preview-v1.png`
  - `image_gen/2026-07-28/region-map-map-variants-v1/40-region-map-a2-5-v6-symbols-preview-v2-r55-restored.png`
- 两图都只作过极简证据，不继续局部修补。
- 当前颗粒度真值板：`image_gen/2026-07-28/region-map-map-variants-v1/41-region-illustration-granularity-truth-board.png`。
- 正确目标不是给 V6 加噪点，而是补回 `2–4` 块平面环境、主体 `6–9` 个有意义结构块和一组异常关系。

## PHOTO & SNAPSHOT 再校准交付

- 当前最近邻母图：`image_gen/2026-07-28/region-map-map-variants-v1/43-region-photo-snapshot-mothers-v2-broad-planes.png`
- 三尺度 QA：`image_gen/2026-07-28/region-map-map-variants-v1/44-region-photo-snapshot-v2-three-scale-qa.png`
- 整屏诊断回填：`image_gen/2026-07-28/region-map-map-variants-v1/45-region-map-a2-5-photo-snapshot-preview-v1.png`
- 聚焦标杆裁切：`image_gen/2026-07-28/region-map-map-variants-v1/47-region-photo-snapshot-focused-benchmark-reference.png`
- 过简诊断：`46-region-photo-snapshot-mothers-v3-over-minimal-diagnostic.png`、`48-region-photo-snapshot-mothers-v4-targeted-subtraction-diagnostic.png`
- 过密 / 纪念碑化诊断：`49-region-photo-snapshot-mothers-v5-over-detailed-diagnostic.png`、`50-region-photo-snapshot-satellite-anchor-over-monumental-diagnostic.png`

当前状态修订：

- `state = region_task_illustration_photo_snapshot_recalibration`
- `status = v2_nearest_three_scale_diagnostic_user_review_pending`
- `production_candidate = false`
- `three_scale_evidence = produced_but_visual_gate_iterate`
- `fullscreen_preview = diagnostic_only_not_runtime`

| 新增 Gate | 结果 | 说明 |
| --- | --- | --- |
| 四联母图 | `iterate` | V2 最近，但卫星 / 灯塔底座与厂房投影仍为 P1 |
| 真实左卡 `1×` | `evidence_ready` | 四对象与异常均可检查；不等于美术通过 |
| 整屏 `25%` | `evidence_ready` | 证明 PHOTO 层比 V6 更合适，同时暴露局部误读 |
| 双 Agent | `iterate` | `P0=0`；共同要求局部修三图后复测 |
| 生产候选 | `blocked` | 用户未裁决颗粒度，且 P1 未关闭 |

## 原始生图输出

- V1：`C:\Users\gzfangyue\.codex\generated_images\019f8963-8f75-7e91-92e0-515d05adc6c9\call_bE8HXHsaHoyib3U72KQfjkSG.png`
- V2：`C:\Users\gzfangyue\.codex\generated_images\019f8963-8f75-7e91-92e0-515d05adc6c9\call_9Ro2MbHyXgWYdwDYol5clfD7.png`
- V3：`C:\Users\gzfangyue\.codex\generated_images\019f8963-8f75-7e91-92e0-515d05adc6c9\call_8VZF0qp2BlFnFnSRXUEBbgmm.png`
- V4：`C:\Users\gzfangyue\.codex\generated_images\019f8963-8f75-7e91-92e0-515d05adc6c9\call_yjnPxVdKJjP5ZunV3SEMLQAA.png`
- V5：`C:\Users\gzfangyue\.codex\generated_images\019f8963-8f75-7e91-92e0-515d05adc6c9\call_dSS0lUOiJHO9Nyzu2bpWOsdE.png`
- V6：`C:\Users\gzfangyue\.codex\generated_images\019f8963-8f75-7e91-92e0-515d05adc6c9\call_P25LqrPUh0fZGmghm2GxAkEz.png`
