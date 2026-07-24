# WMW `schedule_gate` 无字有色母版纵切片 Router Card

## 决策条

- **结论**：A240 已接受 `schedule_gate v0.1`，单张无字有色母版生产解锁。
- **影响**：imagegen 只生成材质配料；程序按 A240 几何装配 456×328 母版并生成 342×246 多状态回填证据。
- **下一步**：完成材质源、母版、回填板和审计后交 UX 老哥复审；不进入 Godot 或正式合同。

## 路由

- **任务类型**：真实位图资产 / 单组件资产化纵切片。
- **风险等级**：normal。
- **上游真源**：A240、`schedule-gate-v0-1-candidate-spec.json`、两张 clean-low-poly benchmark board、支线风格规范、纸张材质合同与 v3 material atlas。
- **技能**：built-in `imagegen`；真实生成源必须落入工作区，程序只做几何装配、材质归一化和 QA。
- **Agent 顺序**：`ui_designer → imagegen / 父级装配 → ux_laoge`。
- **美术路由**：clean-low-poly weekly 临时例外，不自动调用旧像素 / 半调 `angus_art_director`。
- **禁止**：有色整屏、Godot、正式合同、compact A5.1、B2.12、地图和三栏重排。

## Gate

1. 原始生成结果必须是四块无字材质配料，不是完整组件。
2. 所有最终几何由 1368×984 工作画布上的 runtime×4 mask 决定。
3. 纸面按 benchmark material atlas 分角色归一化，不做全图 recolor。
4. warning rust、teal、文字、数字、状态图标和外部阴影不得进入母版。
5. 456×328 母版与 342×246 runtime crop 必须有 alpha / 几何 / 颜色审计。
6. 多状态回填必须共用同一母版 hash，文字 bbox 和输入职责保持 A240。

## 执行结果

- built-in imagegen 已生成并保留一张四角色无字材料源；没有用程序绘图冒充生图。
- 确定性脚本已完成 1368×984 工作装配、456×328 RGBA 无字母版、342×246 回放和 7 个状态输出。
- 56 条状态文字、20 条动态压力文案、alpha、颜色与几何审计通过；日期栏下采样高度 +1px，在预定 `≤1px` Gate 内。
- 按 A241 新增完整拆图流水线讲解板；用户审阅只保留流水线板与 1:1 状态板，材料 / 几何板降为技术 QA 附录。
- UI Designer 与 UX 老哥对组件技术证据均为 `PASS · P0=0 / P1=0 / P2=1`；但用户随后以 A242 撤回该组件作为美术裁决入口。当前只保留技术管线证据，暂停下一组件，路线退回完整 1920×1080 整屏真实内容风格稿。
