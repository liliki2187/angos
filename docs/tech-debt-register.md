## 技术债登记
最后更新：2026-04-09
总条目：0

| ID | 类别 | 描述 | 文件 | Effort | Impact | Priority | Added | Sprint | 接受原因 |
|----|------|------|------|--------|--------|----------|-------|--------|----------|

## 本轮已解决

- `TD-001`：`gd_project/scenes/gameplay/full_chain/` 已收成显式兼容 shim，正式逻辑只保留在 `weekly_run/`。
- `TD-002`：素材库存真源已独立到 `gd_project/scenes/gameplay/weekly_run/materials/WeeklyMaterialInventory.gd`，`WeeklyRunState` 只保留 `new_material_ids` 等周内引用。
- `TD-003`：仓库内 `tools/godot/4.6.2-stable/` 已补齐并安装 export templates，`scripts/run_weekly_run_smoke_tests.ps1` 已在本机跑通。
