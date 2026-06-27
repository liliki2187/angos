# 任务派遣 / 签批外勤界面：V9 主编外勤案卷桌母题验证稿

状态：`rejected_counterexample / old-skeleton-reskin`。这是旧四栏骨架换皮反例，不是高保真真实内容风格稿、no-text 生产母版、atlas 来源或 Godot 落地稿，也不再作为后续布局基准。

> 2026-06-23 复盘结论：用户指出本稿与 V8.2 没有本质区别，仍沿用 `左任务 + 中央已选卡 + 右票据 + 底候选` 的旧配置器骨架。UX 老哥、UI Designer 与 SIA 复审后，V9 降级为“母题命名正确但信息架构未重构”的反例。后续应转向 V10 `编辑桌俯视牌桌` 骨架，而不是继续在 V9 上小修小补。

## 目标

本稿用于验证 SIA 复盘后的核心方向：

> 玩家应读到“主编在外勤案卷桌上，把记者、器材和本周时间押进一份未解案卷，盖章派出去，赌他们带回可写进周刊的素材”。

因此，本版不再继续围绕“删除重复复核信息后如何填空”做局部补丁，而是先重建页面主语。

## 截图

- 整屏默认稿：`docs/screenshots/2026-06-23-dispatch-signoff-v9-field-dossier-motif/01-dispatch-signoff-v9-field-dossier-motif-default.png`
- 批注稿：`docs/screenshots/2026-06-23-dispatch-signoff-v9-field-dossier-motif/02-dispatch-signoff-v9-field-dossier-motif-overlay.png`
- 中央裁切：`docs/screenshots/2026-06-23-dispatch-signoff-v9-field-dossier-motif/03-dispatch-signoff-v9-field-dossier-motif-central-crop.png`

## 本版结构

1. **左侧任务卷宗**：只回答为什么派人和本周行动代价，不承载队伍复核。
2. **中央主编外勤案卷桌**：当前任务是一份展开案卷，已选员工证卡直接压入案卷，随队器材写回案卷。
3. **中央留白**：只保留纸层、无字底稿、半调和装饰纹理，不用状态块、路线图、覆盖表或伪说明填满。
4. **底部候选抽屉**：已选员工从候选池移出；候选员工和器材是供应层，不是主舞台。
5. **右侧签批回执**：完整复核和 CTA 只在右侧，中央不重复 `可签 / 待盖章 / 压力 +2` 等同义状态块。

## 待确认

- 本稿已不再待确认；保留用于提醒后续链路：只改物件名、纸张和局部包装，不能算底层重构。
- 可继承的只有“外勤案卷 / 主编盖章”的职业母题；不可继承旧四栏空间骨架。
