# 任务派遣 / 签批外勤界面：V12 中间主舞台三方向结构稿

状态：`multi-direction-structure-wireframes`。本稿只比较中间主舞台，不推翻左侧任务卷宗、右侧签批票据和底部候选抽屉；不是高保真真实内容风格稿、no-text 生产母版、atlas 来源或 Godot 落地稿。

## 参考来源

- `Sultan's Game`：每周抽卡、限期内完成要求、部署 allies / tools / secrets。转译为“当前任务吞入人手和器材”，不学宫廷题材或新增卡组系统。
- `Papers, Please`：文件审查台与盖章权力。转译为“主编签批前的文件台”，不学边检放行/拒绝分支。
- `Strange Horticulture`：对象触感、柜台物件和故事影响。转译为“员工证、器材、案卷都是可触对象”，不学植物识别或地点探索。
- `News Tower`：报社、记者岗位、每周截稿与选题。转译为“周刊编辑部派人取材”，不学塔楼经营。
- `Death and Taxes`、`BOOK OF HOURS`、`The Operator`：只作为办公文书、对象整理和支援外勤的辅助参考。

## 截图

- 对照总览：`docs/screenshots/2026-06-23-dispatch-signoff-v12-middle-directions/00-dispatch-signoff-v12-middle-directions-contact-sheet.png`
- A 案卷插槽台：`docs/screenshots/2026-06-23-dispatch-signoff-v12-middle-directions/01-dispatch-signoff-v12a-dossier-slot-stage.png`
- B 报社派工版面台：`docs/screenshots/2026-06-23-dispatch-signoff-v12-middle-directions/02-dispatch-signoff-v12b-newsroom-layout-stage.png`
- C 外勤包检查台：`docs/screenshots/2026-06-23-dispatch-signoff-v12-middle-directions/03-dispatch-signoff-v12c-field-kit-stage.png`

## 方案 A：案卷插槽台

母题：员工证被插进当前 M330 外勤案卷，像一份等待右侧盖章的派遣文件。

优势：
- 最接近 UX / SIA 推荐的“本周外勤案卷承载台”。
- 与 V11 的实现距离最近，但比 V11 更有“压入案卷”的物理关系。
- 能清楚表达 4 名员工、1 个备用派遣夹、1 件附件袋器材。

风险：
- 若美术后续只画成横排卡片，会退回 V11 的普通感。
- 需要把卡底部压条、插槽阴影和纸层做足。

## 方案 B：报社派工版面台

母题：把外勤派遣转译成 `WMW 本周外勤取材版`，角色像被贴到本周取材版上的派工条。

优势：
- 最有 Angus / 周刊编辑部职业特色。
- 能把 News Tower 的“报社、记者、截稿”母题转译到派遣页。
- 与右侧签批票据形成“左中是派工版，右侧是签批回执”的关系。

风险：
- 容易滑回报纸排版或后台表格，必须控制字段密度。
- 不能提前引入发刊排版系统；这里只能是派工隐喻。

## 方案 C：外勤包检查台

母题：出发前检查一只外勤包，里面装员工证件、备用证件袋和随队器材袋。

优势：
- 对象触感最强，最像 Strange Horticulture / The Operator 里的桌面物件工作流。
- 器材归属感强，不像独立库存横条。
- 空槽天然是“备用证件袋”，不会强迫玩家补满。

风险：
- 若托盘/包裹感太强，可能弱化“签批台”与“主编盖章”的权力感。
- 需要美术上避免普通工具箱或证物箱既视感。

## 推荐判断

- 结构安全优先：先选 A。
- 产品特色优先：继续打磨 B。
- 对象触感优先：试 C 的局部语法，把器材袋和备用证件袋迁回 A。

父级初步建议：用 A 作为下一张主线结构稿；吸收 C 的“附件袋 / 备用证件袋”物件触感；从 B 借 `WMW 本周外勤取材版` 的报社身份标题，但不把中间做成完整报纸版面。
