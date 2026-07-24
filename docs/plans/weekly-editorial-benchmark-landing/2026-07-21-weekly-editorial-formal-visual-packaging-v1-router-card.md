# 发刊编辑正式视觉包装候选 v1 Router Card

## 任务路由

- 任务类型：现有 UI 结构冻结后的正式视觉包装候选。
- 风险级别：`risky`。原因是可见主流程 UI、筛选/排序新增反馈、破坏性清空确认与送印确认同时存在。
- 目标载体：桌面 `1920×1080` HTML 有字视觉 Mock。
- 明确排除：Godot 正式落地、组件合同升版、GDD 规则裁决、A07–A13 正式生图。

## 输入真源

- 结构真源：`weekly-editorial-formal-black-structure-v4`。
- 视觉真源：`clean-lowpoly-weekly-branch-style-guide.md`、纸张材质合同、颜色合同与两张 branch benchmark board。
- 交互真源：A238 结构冻结裁决、v4 审计、发刊编辑相关 GDD。
- 用户本轮裁决：去掉名称搜索；类型筛选与等级/获得时间排序同时保留；按此方向落地并继续视觉包装。

## Agent 路由

1. `ui_designer`：先给正式视觉包装方案、元素表、1920×1080 几何、状态和资产缺口。
2. `ux_laoge`：再基于真实截图做 P0/P1/P2、历史回归、操作链和安全审计。
3. 父级：合并方案并消费 UX 必须修，生成真实静态/动态证据。

本支线命中 `clean low-poly weekly` 临时例外，因此没有自动调用 `angus_art_director`；改由 branch benchmark、支线风格规范、纸张/颜色合同、UI/UX 与父级逐项对照放行。

## Gate

- 结构守门：PASS。三栏、双页、8卡、唯一局部按钮、唯一 CTA 未改变。
- UI 方案守门：PASS。
- UX 守门：`PASS WITH CHANGES`，P0 为 0。
- 必须修消费：排序状态常显、11px 候选元信息、合法目标角标、明确返回修改、项目内清空确认、锈红语义收敛已完成。
- 资产守门：HOLD。A07–A13 仍为明确占位，未补正式报道图与裁切安全区。
- 生产守门：HOLD。尚未进入 Godot，也未升组件合同。

## 交付判定

当前只可称为 `formal_visual_packaging_candidate_v1`，可交用户做视觉冻结前审阅；不能称为 Godot 生产候选或最终 UI。
