# 区域任务台底板显隐与 dossier 分区局部板 v1｜交付清单

> 日期：2026-07-22  
> 当前状态：`local_dual_state_board_v1_1_go_pending_user_visual_review`  
> 交付性质：真实生图的局部双态风格实验；不是 Godot 截图、可拆生产资产或合同升版。

## 本轮验证

1. 左栏期号印刷是否只在条目不足时作为深青底板露出，条目充足时能否自然被任务纸条覆盖。
2. 右 dossier 是否能在保持一张连续主纸、不重新卡片套娃的前提下，清楚区分摘要、执行条件、风险决策与 CTA。
3. 风险等级、两条依据和建议是否形成可扫读次序，而不是一个混合段落。

## 主证据

- `design/art-direction/region-task-board/void-print-dossier-partition-local-board-v1/review/03-left-dual-state-right-dossier-partition-v1-1-1920x1080.png`：用户主审图，只做尺寸归一。
- `design/art-direction/region-task-board/void-print-dossier-partition-local-board-v1/review/02-left-dual-state-right-dossier-partition-v1-1.png`：模型原生尺寸证据。
- 生图记录：`design/art-direction/region-task-board/void-print-dossier-partition-local-board-v1/2026-07-22-imagegen-prompt-record.md`
- 复盘：`docs/plans/region-task-board-imagegen/2026-07-22-region-task-void-print-dossier-partition-collapse-loop-log.md`

## 结果

- 左 A：两条任务后露出低对比底板印刷，没有白底、独立边框、图标或状态语法，不读成第三条内容。
- 左 B：四张任务纸条完整覆盖底板印刷；`4 条可选`、四张任务、`可处理 4` 数值一致。
- 右侧：页眉 / 摘要保持连续暖纸；执行条件使用低饱和青色全宽带；风险使用锈红侧签和浅锈底面；CTA 使用独立橄榄签批票。
- 风险顺序明确为 `风险等级 → 依据 → 建议`；主 CTA 仍是唯一高权重动作。

## 复核

- UI Designer：`GO / P0=0 / P1=0 / P2=1`。双态遮盖、计数和右侧分区成立；风险区浅锈面积略大，资产拆分时可降低饱和度或收窄面积。
- UX 老哥：`GO / P0=0 / P1=0 / P2=1`。底板不会误读成第三条内容，A/B 数据一致，四段决策链完整；同样建议轻量收窄风险色面积，把最高权重留给 CTA。
- clean-lowpoly weekly 直接标杆复核：暖白纸、深海军蓝、橄榄、青绿、锈红、低多边形折面与低对比印刷均在 benchmark 坐标系内，没有滑向泛黄旧档案、军情终端或泛 SaaS。

## 父级裁决

本稿可作为下一步资产拆分的视觉依据，但尚未获得用户视觉冻结。当前只冻结候选规则，不修改正式实现：

- 左栏底板印刷必须位于任务纸条下层，并随条目数量自然显隐。
- 右侧必须保留 `页眉/摘要 → 执行条件 → 风险等级/依据/建议 → CTA` 的四段顺序。
- 资产拆分时不得把三个只读分区压成同一张中性 NinePatch，也不得把整张 dossier 烘焙为不可回填的大图。
- 浅锈风险底色作为非阻断 P2，在拆分前收窄或降饱和，不为此重生整张审核板。

## 当前需要用户判断

只判断这套左侧显隐逻辑和右侧四分区视觉是否可以冻结为后续资产拆分依据。用户确认前，不修改 `dossier_contract.json`、component inventory、Godot、manifest 或 event card。
