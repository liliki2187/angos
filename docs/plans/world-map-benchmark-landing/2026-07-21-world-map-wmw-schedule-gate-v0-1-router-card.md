# WMW `schedule_gate` v0.1 派生候选 Router Card

## 决策条

- **结论**：A237 已冻结的左下日程器进入首条组件纵向切片；本轮只建立派生候选规格和黑白合同板。
- **影响**：固定 342×246 几何、文字安全区、完整热区、状态矩阵和最后一天边界，为后续无字母版提供可审输入。
- **下一步**：UI Designer 精确化后交 UX 老哥复审；通过后由用户决定是否接受该候选并进入无字有色母版。

## 路由

- **任务类型**：资产化 UI / 派生组件候选。
- **风险等级**：normal。
- **上游真源**：A237、v5.1 default / schedule-confirming、v5.1 audit、资产化 bridge brief / review / manifest。
- **旧资料边界**：`region_task_schedule_v2` 与 `rt-advance-day-atlas.png` 只作交互原则和语义参考；不继承横向几何、旧皮肤、atlas 切片或 asset id。
- **本轮允许**：在 `docs/prototypes/` 建立候选 JSON、程序化黑白合同板、几何 / 文字审计和说明文档。
- **本轮禁止**：修改 `design/ui-contracts/`、Godot、compact A5.1；生成有色资产或有色整屏；宣称 `advance_day` 已实现。
- **Agent 顺序**：`ui_designer → ux_laoge → 父级合并`。
- **美术路由**：属于 `clean low-poly weekly` 临时例外，不自动调用旧像素 / 半调坐标系的 `angus_art_director`。

## Gate

1. runtime-local 整数坐标是本候选唯一权威：`[36,810,342,246]`。
2. default / confirming 必须逐像素回放 v5.1 对应 crop。
3. 所有稳定状态共享同一壳体、热区与分隔线；不得交换整组件或整屏。
4. `remaining_days == 1` 的确认明确进入编辑部；计算钳制到 0，不产生负数。
5. `executing` 锁定完整热区；`committed` 只作瞬时语义节点。
6. 当前 runtime 没有独立 `advance_day`，真实构建只能显示 `disabled_runtime_unavailable`。
7. 所有候选文字必须通过实际字体 bbox 安全区审计。
8. 本轮产物持续标记 `TARGET_ONLY / 非正式合同 / 非 runtime 实现`。
