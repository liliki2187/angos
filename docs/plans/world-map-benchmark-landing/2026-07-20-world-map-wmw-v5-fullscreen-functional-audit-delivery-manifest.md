# WMW v5 整页基础功能终审 Delivery Manifest

## 决策条

- **结论**：v5 原图局部不通过；后续 v5.1 已完成修正并通过 TARGET_ONLY 回归，三栏与 A233 / B 保留。
- **影响**：v5 不冻结；v5.1 可交用户视觉裁决，但仍阻断有色稿、runtime 与正式合同。
- **下一步**：用户裁决 v5.1 的任务摘要与正文第二行候选。

## 详情

- **一句话结论**：v5 的失败来自真值与文案，不来自布局；后续已生成 v5.1 两态与审计，未修改 runtime。
- **我实际做了什么**：完成整页组件清单、代码/GDD核对、UX 诊断与 UI Designer 最小规格。
- **现在卡在哪里**：P0/P1 已在 v5.1 可见结构稿中清零，等待用户裁决两处候选文案。
- **为什么不能跳过**：不可逆时间操作和地区解锁状态必须真实。
- **下一步怎么验证**：v5.1 两态、路径 mask、允许差异区、外漂移 0 与 UX 回归均完成；下一步是用户目检。
- **本轮不要做**：有色稿、Godot、正式合同、整页重排。

## 术语版 / Manifest

- **交付对象**：`black-white-full-map-v5-default.png` 整页基础功能终审
- **产物类型**：problem_overlay 等价的只读设计审计（无新图片）
- **风险等级**：normal
- **它能证明**：三栏几何可保留；B 正确；当前可见语义尚未达到冻结条件；v5.1 的最小修改范围已确定。
- **它不能证明**：advance_day 已实现、A5.1-H 已接入 runtime、正式视觉通过。
- **对照真源 / 标杆**：v5 default / audit / review、A229/A232/A233、`exploration-and-node-dispatch.md`、Weekly Run code/data。
- **截图 / 文件路径**：`docs/prototypes/world-map-wmw-black-white-structure/black-white-full-map-v5-default.png`（本轮只读对象）。
- **几何 / 正交检查**：未触发新图；既有 1920×1080 图按原始像素审计。
- **已过 gate**：三栏职责、B 状态章删除、右栏闭合、进入地区 CTA。
- **未过 / 待确认 gate**：v5.1 用户视觉裁决、runtime、正式合同与有色视觉；静态日程真值、东亚锁定、任务分类、路线删除、审计层分离和两态证据已通过。
- **反向读法检查**：不得把 v5 / v5.1 当 runtime 已实现；不得把局部 FAIL 读成三栏否决。
- **已调用 agent / 复审**：`ux_laoge` → `ui_designer`。
- **未调用 agent 与原因**：冷备 `game_logic_check` 未获解冻确认；runtime 前建议解冻。
- **文档 / 实现 drift 检查**：发现结构稿与 GDD / state / content / systems 的时间、解锁与分类 drift。
- **下一步允许做**：v5.1 黑白局部修正、审计与 UX 回归。
- **下一步禁止跳到**：有色整屏、Godot、compact A5.1 合同修改、生产候选。
