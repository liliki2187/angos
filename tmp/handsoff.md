# 当前交接状态

更新时间：2026-04-09

## 本轮已完成

- 已按系统目录建立正式周循环运行时骨架：
  - `gd_project/scenes/gameplay/weekly_run/`
  - `WeeklyRunGame.gd`
  - `state/WeeklyRunState.gd`
  - `systems/WeeklyRunSystems.gd`
  - `content/WeeklyRunContent.gd`
- 顶层阶段已切到正式链路：
  - `briefing -> explore -> editorial -> summary`
- 菜单入口已改到 `weekly_run/`，旧 `full_chain` 当前只作为过渡入口别名保留。
- 已补文档：
  - `docs/architecture/adr-0003-demo-weekly-schema-migration-boundary.md`
  - `production/sprints/2026-04-09-weekly-schema-migration-slice-1.md`
  - `docs/engine-reference/godot/`
  - `docs/tools/godot-local-engine-workflow.md`
  - `docs/tech-debt-register.md`

## 引擎与工具链状态

- 项目现在锁定使用 `Godot 4.6.2 stable`。
- 仓库内标准引擎目录：
  - `tools/godot/4.6.2-stable/`
- 已下载到仓库内的文件：
  - `Godot_v4.6.2-stable_win64.exe`
  - `Godot_v4.6.2-stable_win64_console.exe`
  - `export_templates/templates/`
- 已补脚本：
  - `scripts/run_weekly_run_smoke_tests.ps1`
  - `scripts/install_repo_local_godot_templates.ps1`
- 以后默认不要再用外部目录 `E:\angus\tools\godot-4.3` 作为真源。

## 已验证结果

- 用仓库内 Godot 运行 smoke test 已通过：
  - `tests/godot/weekly_run/test_phase_flow.gd`
  - `tests/godot/weekly_run/test_settlement_result.gd`
- 验证命令：

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run_weekly_run_smoke_tests.ps1
```

- 已安装 repo-local export templates 到用户目录：

```powershell
powershell -ExecutionPolicy Bypass -File scripts/install_repo_local_godot_templates.ps1
```

- 已用仓库内 `4.6.2` 做过一次 Windows debug 导出，产物存在：
  - `gd_project/build/debug/Angus.exe`

## 关键技术结论

- 官方最新稳定版仍然**不支持**嵌套 typed collections。
- `Array[Array[String]]` 不是 4.3 的局限，而是最新稳定文档下仍不成立。
- 当前代码里相关组合枚举已改成非嵌套 typed collections 方案。

## 本轮顺手修掉的问题

- `MysteryBroadsheetModal.gd` 之前错误地 `preload()` 了 `design/` 下的参考图，导致导出时报错。
- 现在已经把正式运行时资源放到：
  - `gd_project/Assets/ui/mystery_broadsheet/06-mystery-broadsheet-reference.png`
- 对应脚本已改为引用项目内资产：
  - `gd_project/scenes/ui/modals/MysteryBroadsheetModal.gd`

## 目前还没闭环的点

1. `gd_project/project.godot` 里的 `config/features` 仍显示 `4.3`。
原因：
还没有做一次正式的编辑器保存迁移。

2. 第一次用 4.6.2 打开/导出项目后生成了很多新的 `.uid` 文件。
原因：
这是 4.4+ UID 工作流落地后的正常副作用，但是否全部纳入版本库需要人工决定。

3. Windows 导出虽然成功，但 Godot 退出时仍有：
   - `ObjectDB instances leaked at exit`
   - `resources still in use at exit`
这不是当前阻塞，但后续值得排查。

4. 周循环结构债仍在：
   - 旧 `full_chain/` 目录尚未彻底归档或清理
   - `material_inventory` 仍暂住在 `WeeklyRunState`

## 下个会话建议起点

优先顺序建议：

1. 决定是否接受本次 Godot 4.6.2 迁移生成的 `.uid` 文件
2. 用 4.6.2 编辑器正式打开并保存 `gd_project/project.godot`，确认版本戳迁移
3. 继续 weekly run 的系统拆分，优先把 `material_inventory` 从 `WeeklyRunState` 中抽走
4. 视情况清理 `full_chain/` 旧入口

## 当前未提交状态提醒

- 工作区里已经有较多未提交改动，包含：
  - weekly run 新目录
  - engine reference 文档
  - 本地工具链脚本
  - 4.6.2 首次运行生成的 `.uid` 文件
- 本次没有做 commit。
