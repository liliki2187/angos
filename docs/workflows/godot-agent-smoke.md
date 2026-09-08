# Godot 运行健康检查

按受影响行为选检查，不因改了任意 `.gd` 或 `.tscn` 就固定运行整套工具。修改脚本要检查解析，修改运行实现要验证相应真实路径；入口、autoload、阶段切换或共享依赖影响 weekly-run 时扩大到主流程。

本文的组合脚本适用于需要核验 weekly-run 启动、节点接线和基础探索/派遣路径的任务。局部显示修改已有覆盖该消费者的专用运行验证时，不重复跑无关流程。文档和纯设计讨论不调用本脚本。

## 已有组合工具

```powershell
.\scripts\run_godot_agent_smoke.ps1
```

若执行策略阻止项目脚本，可用：

```powershell
powershell.exe -ExecutionPolicy Bypass -File .\scripts\run_godot_agent_smoke.ps1
```

脚本组合 `gda script validate` 与 Godot headless smoke。没有全局 gda 时会用 `uvx --from gda gda`，首次获取可能需要网络权限。已有缓存时可使用 `-GdaOffline`，`-PythonPath` 指向本机实际可用 Python，不复制他人机器路径。

默认验证 WeeklyRunGame.gd 和 gda_angus_weekly_run_smoke.gd；其他受影响脚本可传：

```powershell
.\scripts\run_godot_agent_smoke.ps1 -ExtraValidateScript scenes/gameplay/weekly_run/phases/SomeChangedScript.gd
```

随后运行 `res://tests/gda_angus_weekly_run_smoke.gd`，加载真实 WeeklyRunGame.tscn、检查关键节点、进入探索、选择初始北美地区、打开派遣节点并切换一名人员。超出这条路径的改动需选择对应验证，不能用此通过覆盖未测页面。

## 正确解读结果

- 使用 gda 时读取 JSON 的 `valid` 字段；进程退出码为 0 仍可能返回 `valid: false`。
- 使用 headless 时检查退出码及相关运行错误。脚本解析正确仍可能有节点改名、null 调用或 autoload 加载失败。
- 个别 class_name 脚本脱离项目单独解析可能误报全局类冲突；根据项目实际加载环境复核，不批量忽略真实错误。

失败时按 [Godot 错误笔记](godot-debug-skill-v0.md) 定位原因、修复并复验。组合脚本内部两层均成功才称该脚本通过；采用其他针对性方法时如实写所用方法，不冒称运行了组合工具。

## 视觉与原生窗口边界

这只证明所覆盖运行路径，不证明美术、所有状态、所有玩法或动态节奏。可见改动按 [截图指引](../onboarding/功能改动截图指引.md) 交付；[视觉 smoke](godot-visual-feedback-smoke.md) 是针对其既有路径的可选采集工具。

Windows 的应用程序错误或内存读取弹窗属于原生 GUI/进程问题；headless 正常不证明精确 GUI EXE 正常。按错误笔记卡 006 单独核验出错可执行文件：

```powershell
powershell.exe -ExecutionPolicy Bypass -File .\scripts\run_godot_gui_startup_check.ps1 -GodotPath "<实际出错的 Godot EXE 绝对路径>"
```
