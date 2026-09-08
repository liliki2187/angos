# 两种分析方式的共同题目与证据

2026-09-08。用户认为功能差不多了，但截图中的任务区文字、图片与界面资源配合不好，显得质量不高；要求先由父级独立分析，再按传统 subagent 路径另做一份，比较分析和处理方式。本轮只分析、记录与比较，不修改界面或生成新图。

## 共同边界

- 桌面 16:9、1920×1080，当前真实 Godot 世界地图；保留已认可的墨青、矿物青、暖白、蜜黄与宽块面、手绘编辑部气氛。
- 左侧选区与只读日程，中央地图与地点证据，右侧新闻、任务预览、进入地区。原始标杆是形体与气氛依据，不照搬其中旧纸或灰土配色。
- 任务取真实游戏数据，默认最多预览两条并显示总数；类型、风险／追踪说明、剩余天数已接入。折叠保留分类和提醒。任务行只读，具体任务进入地区后选择；锁定可预览但不能进入，开放空态与锁定分开。
- 左、中、右新闻图片为每地区同一 Texture2D，完整等比显示。可提布局或资源修改方案，不假称本轮已获实施／生图授权。
- 本次比较针对分析依据、原因解释、处理的具体程度、功能保护和预期实施代价。只有文字分析，没有 A/B 成品或用户测试，不能声称已证明某流程普遍更好。

## 证据路径

- 用户局部图：`C:/Users/GZFANG~1/AppData/Local/Temp/codex-clipboard-9c93756a-0b45-4f32-96e6-5c72c9ddfb3a.png`。
- 当前整屏：`D:/angos/docs/screenshots/2026-09-08-world-map-task-readability/01-live-default.png`。
- 长内容样本：同目录 `13-long-content-layout-fixture.png`；折叠：`10-task-collapsed.png`；锁定：`02-live-locked.png`；空态：`03-live-open-empty.png`。
- 用户选定的三栏视觉候选：`D:/angos/image_gen/2026-09-07/world-map-a-soft-three-columns-v1/02-filled-soft-three-column-candidate.png`。
- 原标杆：`D:/angos/design/art-direction/references/clean-lowpoly-weekly-branch/benchmark-board-01.png`、`benchmark-board-02.png`。
- 等比查看副本：`C:/Users/gzfangyue/.codex/worktrees/4564/angos/tmp/world-map-task-analysis/benchmark-board-01-view.png`、`benchmark-board-02-view.png`；仅为解决查看工具解码失败，未改标杆。
- 当前实现：`D:/angos/gd_project/scenes/gameplay/weekly_run/components/WeeklyRunWorldMapSoftColumns.gd`。
- 当前纸件：`D:/angos/gd_project/Assets/ui/angus_packaging/world_map/soft_columns_v1/region-tag.png`、`action-paper.png`。

## 执行隔离

父级独立稿先保存并计算 SHA256，之后不回改。传统路径使用新上下文的 UX 老哥 → UI Designer → UX 定向复核；不读取父级独立稿或其摘要，不要求赞同父级。父级最后比较两份分析。该隔离减少本次互相迎合，不消除父级作为此前作者的历史偏见。

## 输入补齐记录

UI 初稿返回后，父级发现上述简报虽说明真实功能与配色，却没有显式写入上一轮用户原话：“另外任务的显示不能只和上方纯信息的显示一样，这样容易漏掉任务。”这条约束仍有效，已经原样补充给 UI Designer，让其自行判断是否修订；没有提供父级独立方案。最终比较以补齐后的方案为准，不把不完整 brief 下的初稿作为角色能力优劣证据。父级自身知道历史要求，故本实验不宣称严格相同输入或严格盲测。
