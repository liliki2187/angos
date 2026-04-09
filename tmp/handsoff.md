# 当前交接状态

更新时间：2026-04-09

## 本轮已完成

- 周循环正式运行时继续收口到 `gd_project/scenes/gameplay/weekly_run/`，并保留 `briefing -> explore -> editorial -> summary` 四阶段正式链路。
- `material_inventory` 已从 `WeeklyRunState` 中抽出，独立为：
  - `gd_project/scenes/gameplay/weekly_run/materials/WeeklyMaterialInventory.gd`
- 旧 `full_chain/` 已收成显式兼容 shim：
  - `gd_project/scenes/gameplay/full_chain/FullChainGame.gd`
  - 旧路径仍可打开，但正式逻辑只继续落在 `weekly_run/`
- `weekly_run` 的 UI 已从 demo 式混合大页面重构为“固定壳层 + 阶段场景 + 复用组件”：
  - 壳层：
    - `gd_project/scenes/gameplay/weekly_run/WeeklyRunGame.tscn`
    - `gd_project/scenes/gameplay/weekly_run/WeeklyRunGame.gd`
  - 阶段场景：
    - `phases/WeeklyRunBriefingPhase.tscn`
    - `phases/WeeklyRunExplorePhase.tscn`
    - `phases/WeeklyRunEditorialPhase.tscn`
    - `phases/WeeklyRunSummaryPhase.tscn`
  - 复用组件：
    - `components/WeeklyRunActionItem.tscn`
    - `components/WeeklyRunInfoCard.tscn`
    - `components/WeeklyRunMetricCard.tscn`
    - `components/WeeklyRunScrollableText.tscn`
- 项目 UI 设计基线已切到 `1920x1080`，并把“非浮动模态优先相对布局”的规则写入：
  - `gd_project/project.godot`
  - `docs/technical-preferences.md`
- 修掉了新 `weekly_run` 界面被上下顶开的结构性问题：
  - 不再让 `briefing` 借住 `explore` 页面
  - 新周进入 `briefing` 时不会再因为上周日志 / 文本撑高整页
- 修掉了 `本周简报 / 派遣简报 / 结算预估` 内容挤到左边窄列的问题：
  - 统一改成 `WeeklyRunScrollableText`
  - 内容宽度跟随滚动区同步，不再退化成 `1px`
- 为排查“外采后切换探索节点卡顿”补了结构化日志与耗时：
  - `WeeklyRunGame.gd`
  - `phases/WeeklyRunExplorePhase.gd`
  - `phases/WeeklyRunEditorialPhase.gd`

## 当前真实来源

- 正式周循环运行时：
  - `gd_project/scenes/gameplay/weekly_run/`
- 周状态真源：
  - `design/gdd/weekly-run-loop.md`
- 迁移边界与 UI 约束：
  - `docs/architecture/adr-0002-godot-ui-scene-first-and-binding-driven.md`
  - `docs/architecture/adr-0003-demo-weekly-schema-migration-boundary.md`
- 本地工具链工作流：
  - `docs/tools/godot-local-engine-workflow.md`

## 已验证

- smoke test 已通过：
  - `tests/godot/weekly_run/test_phase_flow.gd`
  - `tests/godot/weekly_run/test_settlement_result.gd`
  - `tests/godot/weekly_run/test_weekly_run_layout.gd`
- 验证命令：

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run_weekly_run_smoke_tests.ps1
```

- `full_chain` 兼容 shim 已做过 headless 加载检查，能正确挂到新的 `weekly_run`
- repo-local Godot 4.6.2 与 export templates 已就位：
  - `tools/godot/4.6.2-stable/`
- 已重新导出可测包：
  - `gd_project/build/debug/Angus.exe`
  - `gd_project/build/debug/Angus.console.exe`
  - `gd_project/build/release/Angus.exe`

## 关键技术结论

- 当前“外采后切换探索节点会卡一下”已经定位到主因，不是公式，不是合法派遣枚举：
  - `_refresh_all()` 平均约 `60ms`
  - `_on_node_pressed()` 触发后平均约 `62ms`
  - `ExplorePhase.render()` 本身约 `62ms`
- 目前最重的是 `ExplorePhase` 的整块重建：
  - `StaffGrid` 重建约 `29ms`
  - `NodeList` 重建约 `17ms`
  - `RegionList` 重建约 `8ms`
- `build_explore_payload()` 本身很轻，问题不在 payload 计算，而在“切节点时整页删节点再实例化”

## 目前还没闭环的点

1. 探索页切换节点仍是“整页 refresh -> 整页 render -> 列表重建”。
原因：
当前 `WeeklyRunGame._on_node_pressed()` 仍直接调 `_refresh_all()`，还没改成局部刷新。

2. `gd_project/project.godot` 里的 `config/features` 仍显示 `4.3`。
原因：
还没有做一次正式的编辑器保存迁移。

3. Windows 导出虽然成功，但 Godot 退出时仍有：
   - `ObjectDB instances leaked at exit`
   - `resources still in use at exit`
这不是当前阻塞，但后续值得排查。

## 下个会话建议起点

1. 把 `ExplorePhase` 改成“局部刷新”，至少做到切换节点时不再重建区域 / 节点 / 职员 / 素材 / 日志整页
2. 如果继续收口正式切片，再把 `briefing/explore/editorial/summary` 中仍用代码实例化的列表项继续替换成更稳定的 item scene 池或复用更新策略
3. 视情况用 4.6.2 编辑器正式打开并保存 `gd_project/project.godot`，把版本戳迁掉
4. 后续再看 `ObjectDB` / `resources still in use at exit` 的退出警告

## 备注

- 仓库根的 `.godot/` 是本轮探针和导出产生的缓存，已补进 `.gitignore`
- `tools/godot/4.6.2-stable/` 下实际二进制仍按仓库规则不纳入 Git
