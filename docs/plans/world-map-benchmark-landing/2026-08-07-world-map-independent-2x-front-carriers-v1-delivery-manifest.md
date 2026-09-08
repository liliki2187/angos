# 世界地图独立 2× FrontCarrier v1 交付清单

## 本轮结论

用户在《正交功能承载面校正板 01》后要求继续，本轮已完成真实运行合同复核、五份独立 ImageGen 材质源、三项独立 `2×` FrontCarrier、运行时尺寸预览板和独立位图验证。

最终放行：

- Dossier `936×2064 → 468×1032`，`39:86`。
- Schedule `744×492 → 372×246`，`62:41`。
- 主 CTA `828×152 → 414×76`，`207:38`。

继续阻断：

- 地区卡：A282 / 当前原型是 `340×170 = 2:1`，A292 校正板是 `86:41`；未获用户裁决前不生成壳体。
- ISSUE：没有冻结 exact runtime rect、safe rect 和交互属性；只保留材质参考。

当前状态为 `independent_2x_front_carrier_dual_review_pass_ready_for_internal_slot_pressure_board`。Atlas、manifest 与 Godot 正式回填继续阻断。

## 制作方法与来源

- 生成模式：Codex 内置 ImageGen。
- 风格参考：`image_gen/2026-08-06/world-map-art-gap-demos-v1/04-final-a-c-b10-visual-target.png`，只参考 A＋C＋B10% 的纸材、综合色彩、低多边形与氛围，不复制斜纸或界面结构。
- ImageGen 职责：五份独立纸材、色彩与低多边形纹理。
- 程序职责：精确尺寸中心裁切 / 镜像铺展、2–3px 源图机构登记线、运行时尺寸拼板和 QA；不生成美术纹理，不从整屏目标回裁。
- 完整提示词：`image_gen/2026-08-07/world-map-front-carriers-v1/14-imagegen-prompts.md`。
- 可复现构建：`scripts/ui-contracts/wmw/build_world_map_front_carriers_v1.py`。
- 独立验证：`scripts/ui-contracts/wmw/validate_world_map_front_carriers_v1.py`。

## 可见交付

- 生产预览：`image_gen/2026-08-07/world-map-front-carriers-v1/09-runtime-scale-review-board.png`。
- Safe rect QA：`image_gen/2026-08-07/world-map-front-carriers-v1/10-geometry-safe-rect-qa.png`。
- 独立落位 QA：`image_gen/2026-08-07/world-map-front-carriers-v1/13-detected-placement-qa.png`。
- 三项独立位图：`06-front-carrier-dossier-2x.png`、`07-front-carrier-schedule-2x.png`、`08-front-carrier-cta-default-2x.png`。
- 构造审计：`11-front-carrier-audit.json`。
- 独立位图验证：`12-independent-front-carrier-validation.json`。

## 几何与交互结果

三项均满足：

- 源图尺寸是运行时 exact rect 的严格 `2×`。
- 比例误差 `0`；根节点 `0°`；四条机构线轴向偏角 `0°`。
- 没有非等比拉伸和位图上采样。
- 运行时拼板与源图缩放结果逐像素一致；`all_released_pass=true`。

交互映射不是“整张纸都能点”：

- Dossier 根页为 `pass_not_full_button`；只列 Disclosure `[27,572,414,56]` 与 CTA child `[27,932,414,76]`。
- Schedule 为 `MOUSE_FILTER_IGNORE / FOCUS_NONE`，无热区。
- CTA 自身 hit rect 为 `[0,0,414,76]`。

Safe rect：

- Dossier `2× [54,48,882,2016]`，运行时 `[27,24,441,1008]`。
- Schedule `2× [32,16,712,460]`，运行时 `[16,8,356,230]`，已覆盖顶部 Kicker。
- CTA `2× [48,20,780,132]`，运行时 `[24,10,390,66]`。

## UI / UX 双审

- UI Designer：三个 FrontCarrier 视觉 `PASS`。Dossier 温米灰、Schedule 略冷灰、CTA 深低饱和橄榄均与 A291 同族；纤维与大块低多边形在运行时不会滑向写实纸毛、SaaS 面板或军事档案。ISSUE 材质仅作参考，正式小票应选更安静区域，防止迷彩感。
- UX 老哥：首轮发现 Dossier / Schedule 整根热区误标和 Schedule safe rect 顶部漏 8px，修正后复核 `PASS / P0=0 / P1=0 / P2=0`；放行 internal slot pressure board，Atlas / manifest / Godot 继续阻断。

## 下一门

制作内部插槽压力板，但只针对三项已放行壳体：

1. Dossier：真实 `414×264` 图片、最长地区名 / 状态 / 标题 / 正文、collapsed / expanded 同高与两条真实交互区。
2. Schedule：顶部 Kicker、两位数天数、剩余天数和禁用文案；保持完全不可交互。
3. CTA：最长正式文案及 normal / hover / pressed / disabled / warning 的独立状态层；不得把状态烘进 FrontCarrier。

地区卡与 ISSUE 不进入正式壳体或 hit 压力，直到用户裁决比例 / exact rect。

