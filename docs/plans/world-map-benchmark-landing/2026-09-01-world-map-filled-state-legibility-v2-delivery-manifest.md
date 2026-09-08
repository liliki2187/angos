# 世界地图 Filled-state 可读性 v2 交付清单

## 结论

A337 的整体美术方向保留；本轮完成整屏功能文字与留白复检，并在不改变冻结矩形、图片规格、功能合同和 ImageGen 纸材的前提下完成槽内重排。当前为 filled_state_legibility_v2 / pending user visual gate，不是 Godot 落地件。

## 主产物

- 整屏视觉目标：image_gen/2026-09-01/world-map-filled-state-legibility-v2/01-filled-state-visual-target-1920x1080.png
- A291 并排板：02-a291-vs-filled-state-side-by-side-3840x1080.png
- 对话预览板：02b-a291-vs-filled-state-side-by-side-1920x540.png
- 左栏 100% 审查图：03-left-column-100pct-review.png
- 地图 100% 审查图：04-map-field-100pct-review.png
- Dossier 100% 审查图：05-dossier-100pct-review.png
- 功能合同叠层：06-contract-qa-overlay-1920x1080.png
- 审计：07-filled-state-audit.json

## 本轮修订

- 删除 Dossier 右下“需更多目击记录”装饰簇。
- Dossier 导语：14px → 16px。
- Disclosure 统计：13px → 15px。
- 任务标题：16px → 18px；元数据：12px → 15px；编号：12px → 14px。
- 两条任务在既有 expanded capacity 内扩为约 104px 只读阅读行；CTA、Disclosure 与 hit rect 零位移。
- RegionCard 状态与说明提高至 15px，删除 9px 伪元数据。
- Schedule 栏目头提高至 14px，禁用说明提高至 15px 并增强字重。
- 左栏计数提高至 14px 并增强对比。
- 当前阶段统一使用“候选稿”，不再同时出现“本期主稿”。

## 验证

- 画布：1920×1080。
- RegionIndex、Schedule、MapField、Dossier、Disclosure、CTA 全部保持冻结矩形。
- 三张 RegionCard 图槽均保持 138×88。
- Dossier 图槽保持 414×264。
- 北美、东亚、太平洋三张 canonical 母图仍为 1104×704 / 69:44。
- 三处卡片图槽和一处 Dossier 图槽均与直接 LANCZOS 等比缩放逐像素一致。
- 07-filled-state-audit.json：all_pass=true。

## 尚未放行

- 用户尚未完成 v2 视觉 Gate。
- MapField 底部橄榄插袋若未来与南美/南太平洋节点冲突，须另过容量 Gate。
- ISSUE 票签 exact rect 仍未冻结。
- 不进入 atlas、asset manifest、Godot 或 WeeklyRunGame。
