# 世界地图正交功能承载面校正板 01 交付清单

## 本轮结论

《正交功能承载面校正板 01》已完成，并通过 UI Designer 与 UX 老哥双审：`component_correction_sheet = PASS / P0=0 / P1=0 / P2=2`。当前只放行下一阶段的五类独立 `2×` 无字 FrontCarrier；atlas、manifest、Godot、动态文字、状态矩阵和真实 hit rect 仍未放行。

## 目标与范围

- 关闭斜功能纸面、错误比例和整屏回裁的生产风险。
- 本轮只处理 dossier 正面、地区卡正面、Schedule 正面、ISSUE 票签与主 CTA 五类功能壳。
- 不处理背页、夹子、胶带、阴影、状态签、文字、图片、atlas 或 Godot。

## 制作方法

1. 真实 ImageGen 第一轮得到正交但比例错误的接触板。
2. 第二轮只修 dossier 与地区卡比例，仍失败；按止损规则停止 prompt-only 微调。
3. 保留第二轮真实 ImageGen 的纸材、颜色和低多边形纹理；程序只执行合同比例矩形遮罩、接触板拼版和 QA 标注，不生成美术纹理。
4. 独立校验器重新读取最终 bitmap，扫描真实前景边缘并计算 bbox、比例和边角。

## 主要证据

- 玩家查看主板：`image_gen/2026-08-07/world-map-orthogonal-functional-carriers-v1/03-contract-assembled-sheet.png`
- Safe rect QA：`image_gen/2026-08-07/world-map-orthogonal-functional-carriers-v1/04-geometry-qa-overlay.png`
- 构造审计：`image_gen/2026-08-07/world-map-orthogonal-functional-carriers-v1/05-geometry-audit.json`
- 独立位图验证：`image_gen/2026-08-07/world-map-orthogonal-functional-carriers-v1/06-independent-geometry-validation.json`
- 真实边缘 QA：`image_gen/2026-08-07/world-map-orthogonal-functional-carriers-v1/07-detected-edge-qa.png`
- 可复现构建：`scripts/ui-contracts/wmw/build_world_map_orthogonal_carrier_sheet_v1.py`
- 独立验证：`scripts/ui-contracts/wmw/validate_world_map_orthogonal_carrier_sheet_v1.py`

## Gate 结果

- 五项真实 bitmap bbox 与合同 rect 偏差：`0px`。
- 五项真实边缘最大偏角：`0°`，阈值 `≤1°`。
- 五项比例误差：均低于 `0.5%` 门槛。
- `text_geometry_pass=true`。
- `art_shell_geometry_pass=true`。
- `all_pass=true`。

## 双审摘要

- UI Designer：作为校正板 PASS，当前克制扁平是正确阶段结果；最终组件仍须分别输出独立 `2×` 壳体，纸色差、纤维尺度和 1–2px 机构线留到下一阶段，斜纸 / 夹子 / 阴影留到 BackDecor。
- UX 老哥：本阶段 PASS，可进入独立 `2×` FrontCarrier；当前 PNG 不能证明 hit rect、MouseFilter、状态矩阵或最长文案，暂不可进入 atlas / Godot。

## P2 与下一门

1. ISSUE 与 CTA 同为橄榄色，正式组装时要拉开元信息标签与主操作的明度 / 反馈身份。
2. 当前只有组件级 safe rect；下一门必须用最长中文、两位数、照片槽、Disclosure 展开态和 CTA 状态做内部插槽压力板。

当前状态：`component_correction_sheet_dual_review_pass_pending_user_confirmation`。
