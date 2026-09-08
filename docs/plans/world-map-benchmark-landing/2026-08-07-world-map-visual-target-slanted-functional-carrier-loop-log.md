# 世界地图视觉目标斜功能承载面误放行 Loop Log

结论：A＋C＋B10% 整屏继续保留为视觉目标，但“可直接进入真实 Godot 落地”的扩大表述撤回；从整屏直接裁切功能组件的路径立即阻断。

影响：右 dossier、地区卡、Schedule、票签、CTA 与证物簇混合了倾斜纸面、动态文字、状态、图片、阴影和疑似热区。若直接切入运行时，会破坏动态文案安全区、状态同构、图片比例和轴对齐 hit rect，也无法稳定做本地化与 disclosure 展开态。

下一步：停止整屏重生，先交《正交功能承载面校正板 01》，只验证五类无字、零旋转、真实比例的独立前壳；正交 Gate 通过后再做 BackDecor 拆层和单组件 Godot 回填。

## 触发与归因

- **触发来源**：用户反馈。
- **原始问题**：用户指出当前有些资源是斜的，显然无法正式使用，并要求从实用角度分析全部元素，避免生成不可用组件。
- **失败归因**：产物类型与证据放行错误。整屏 ImageGen 的视觉、氛围与操作层级通过，被错误扩大成“可以进入真实 Godot 落地”；父级与双 agent 未在该表述前执行 `ui_geometry_gate` 的三处核心面裁切、真实美术边缘测量和 `text_geometry_pass + art_shell_geometry_pass`。
- **复发判定**：命中 `docs/onboarding/ai-collaboration-guidance.md` §7.0 的 F2“功能面倾斜 / 正交”，为该家族至少第 6 次复发。现有规则与脚本并非缺失，问题是没有绑定到本次“可进 Godot”的放行动作。
- **本轮处理**：视觉方向继续；直接裁切生产降级为 `BLOCK`；不修改 Godot，不进入 atlas / manifest。

## 当前产物重新分类

| 对象 | 修订后身份 | 允许证明 | 禁止声称 |
| --- | --- | --- | --- |
| `04-final-a-c-b10-visual-target.png` | `visual_target / style_and_composition_truth` | A＋C＋B10% 的构图、色彩、纸层剂量、氛围与操作层级 | 可直接裁切、正交通过、无字资产母版、生产候选 |
| 右 dossier / 左卡 / Schedule / CTA 等压平局部 | `visual_reference_only` | 造型、材质与层次参考 | 可承载动态文字、状态或 hit rect |
| 下一张组件板 | `component_correction_sheet` | 正交壳、真实比例、安全区与拆层路线 | 整屏视觉完成、runtime 已接入 |

## 复发保护

1. 任何整屏视觉目标只要被表述为“可拆资产、可进 manifest、可进 Godot”，自动触发 `ui_geometry_gate`；缺少至少三处核心面真实边缘裁切与双通行证时，只能写“几何未验证”。
2. 生成功能前壳的 prompt 必须包含：`front writable paper faces are square-on and axis-aligned; no tilted/skewed/perspective writable document faces; angled sheets are background decoration only`。
3. 功能壳必须按真实宽高比独立生成；方形只属于 icon / badge，不得把 dossier、地区卡、Schedule、ISSUE 票签或 CTA 先做成 `1:1` 再拉伸。
4. 节点固定为 `FunctionalRoot(0°) / BackDecor / FrontCarrier(0°) / RuntimeImage / RuntimeText / StateDecor / ButtonHitRect(0°)`；只有 `BackDecor` 可倾斜，所有装饰层 `MOUSE_FILTER_IGNORE`。
5. 视觉目标禁止回裁图片源；三张新闻图继续引用原始 `1104×704 / 69:44` 母图。

## 沉淀判断

- 用户裁决与当前产物降级登记为 A292，并更新世界地图资产线 `STATUS.md`。
- 既有正交规则已经完整存在于 `docs/workflows/ui-geometry-and-text-safety-gates.md` 与 `docs/onboarding/ui-interaction-guidelines.md` §13.2–13.5，本轮不重复新建第三套规则。
- 更新 F2 家族复发次数与最后日期；后续失败应修正放行动作绑定，而不是继续追加同义 prompt 文档。

## 修复结果（2026-08-07）

- 真实 ImageGen 第一轮正交但 dossier / 地区卡比例失败；第二轮定向修正仍失败，因此 prompt-only 路线按止损规则停止。
- 第二轮只保留为真实纸材、颜色和低多边形纹理来源；程序只按合同比例做矩形遮罩、拼板与 QA，不生成美术纹理或界面内容。
- 独立校验器读取最终 bitmap 后确认五项 bbox 与合同偏差 `0px`、边缘偏角 `0°`、比例全部通过；UI Designer 与 UX 老哥双审均 `PASS / P0=0 / P1=0`。
- 当前只关闭 `component_correction_sheet` Gate；等待用户确认后才进入五类独立 `2×` 无字 FrontCarrier。atlas、manifest、Godot、动态文字与状态矩阵仍未放行。
- 用户要求继续后，真实运行合同回查只放行 Dossier、Schedule、CTA 三项独立 `2×` FrontCarrier；地区卡因 `340×170=2:1` 与 `86:41` 冲突、ISSUE 因缺 exact rect，只保留材质参考。三项最终位图与运行时落位独立验证 `all_released_pass=true`，并修正了 Dossier / Schedule 整根热区误标与 Schedule safe rect 顶部漏 8px。当前进入 internal slot pressure board，atlas / manifest / Godot 继续阻断。
- internal slot pressure board 已以真实内容与容量 fixture 闭环：81 处真实栅格字形、完整 `耗时99天｜限时第99天`、`1104×704 → 414×264` 全幅图源、collapsed / expanded 冻结插槽和真实输入合同全部通过。首轮视觉 / UX 复审发现 CTA 三态辨识不足、Schedule 禁用箭头像按钮、Preview 压力文案被简写，均只改 StateDecor / fixture 后关闭；双审终审 `PASS / P0=0 / P1=0`。该结果证明正交壳可承载真实内容，但不撤销对整屏目标回裁、地区卡比例冲突和 ISSUE exact rect 的阻断；下一门为 BackDecor / StateDecor 合成。
