## 技术债登记
最后更新：2026-04-09
总条目：3

| ID | 类别 | 描述 | 文件 | Effort | Impact | Priority | Added | Sprint | 接受原因 |
|----|------|------|------|--------|--------|----------|-------|--------|----------|
| TD-001 | Architecture Debt | `gd_project/scenes/gameplay/full_chain/` 仍保留旧 demo 入口实现，尚未收成显式 shim 或归档。 | `gd_project/scenes/gameplay/full_chain/` | M | High | 8 | 2026-04-09 | 周循环正式 Schema 迁移（切片 1） | 本轮先把正式入口切到 `weekly_run/`，避免在迁移中同时处理所有旧目录善后。 |
| TD-002 | Architecture Debt | `material_inventory` 目前仍暂住在 `WeeklyRunState`，还没有独立成真正的素材库存系统。 | `gd_project/scenes/gameplay/weekly_run/state/WeeklyRunState.gd` | M | High | 7 | 2026-04-09 | 周循环正式 Schema 迁移（切片 1） | 本轮优先把顶层阶段流、状态命名和正式入口落地，先接受单体状态容器中的过渡存放。 |
| TD-003 | Test Debt | 已补 Godot headless smoke tests，但当前环境缺少可直接调用的 Godot 可执行文件，尚未跑通自动化。 | `tests/godot/weekly_run/`、`scripts/run_weekly_run_smoke_tests.ps1` | S | Medium | 6 | 2026-04-09 | 周循环正式 Schema 迁移（切片 1） | 先把可执行测试脚本和运行入口落盘，等待本机或 CI 提供 Godot 路径后再完成实际执行。 |
