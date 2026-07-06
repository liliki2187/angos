# Godot Debug Skill v0

> 人话说明：这是 Angus 的 Godot 报错错题本，给 Codex 用。
> 它不是 Godot 教程，而是把常见报错翻译成“哪里坏了、为什么坏、怎么小修、怎么验证”。

## 什么时候用

遇到这些情况，先看这份文件：

- Godot smoke test 失败。
- 修改了 `.gd`、`.tscn`、节点名字、场景层级、autoload、preload 路径。
- 修改了周循环、世界地图、地区任务、派遣、报道、阶段切换。
- 用户说“Godot 报错了”。
- 同一种 Godot 错误第二次出现，应该沉淀成可复用卡片。

不要误用：这份文件只能证明“怎么修 Godot 报错”。它不能证明 UI 好看、截图达标、玩法平衡或资产化 UI 可进生产。

## 默认验证命令

正常情况下，修完 Godot 问题后跑这一条：

```powershell
powershell.exe -ExecutionPolicy Bypass -File "D:\angos\scripts\run_godot_agent_smoke.ps1" -GdaOffline -PythonPath "C:\Python314\python.exe"
```

看到这一句，才算通过：

```text
Godot agent smoke passed.
```

如果第一次运行需要下载 `gda`，可能要去掉 `-GdaOffline`。只有确认允许联网时才这么做。

## Codex 使用顺序

1. 先把当前报错对到下面最像的一张卡。
2. 如果用户在问“什么意思”，先用卡片的人话解释说明。
3. 只修根因，不顺手大改。
4. 跑默认验证命令。
5. 如果是新型、可复发的错误，把它追加成新卡。

## 错误卡片

### 001. GDScript 语法或编译错误

**报错长什么样**

```text
Parse Error
Expected ":" after function declaration
gda script validate failed for scenes/...
valid: false
```

**人话解释**

Godot 连脚本都没读懂。可以理解成代码这句话标点错了，游戏还没进入运行阶段，就卡在“读代码”这一步。

**常见原因**

- 函数结尾少了 `:`。
- 缩进坏了。
- 括号、引号、逗号少了一个。
- 写了当前 Godot 版本不认识的类型或函数写法。

**怎么修**

- 先打开 `gda` 指到的那一个脚本。
- 先修报错行，不要顺手重构旁边代码。
- 如果这次改的脚本不在默认检查列表里，验证时加 `-ExtraValidateScript`。

**怎么验证**

```powershell
powershell.exe -ExecutionPolicy Bypass -File "D:\angos\scripts\run_godot_agent_smoke.ps1" -GdaOffline -PythonPath "C:\Python314\python.exe" -ExtraValidateScript "scenes/gameplay/weekly_run/path/to/changed_script.gd"
```

**通过标准**

这个脚本返回 `valid: true`，并且完整 smoke 最后出现 `Godot agent smoke passed.`

### 002. 节点路径找不到

**报错长什么样**

```text
Node not found
missing node: RootMargin/RootVBox/PhaseHost
Cannot get node "..."
```

**人话解释**

代码在场景树里找一个 UI 物件，但那个物件不在原来的位置了。你可以把它想成：清单写着“去 A 柜第 3 个抽屉拿文件”，但抽屉被改名或搬走了。

**常见原因**

- `.tscn` 里的节点被改名。
- 面板被移动到另一个父节点下面。
- 复制出来的场景层级和原场景不一样。
- 代码写了很长的固定路径，场景一改就断。

**怎么修**

- 打开对应 `.tscn` 或脚本，确认真实节点名字和路径。
- 如果这是必需节点，修路径或修场景结构，不要悄悄忽略。
- 如果这是可选节点，用 `get_node_or_null()`，并明确处理“没有这个节点”的状态。
- 如果这个节点以后必须保护，把它加进 `gd_project/tests/gda_angus_weekly_run_smoke.gd`。

**怎么验证**

跑默认验证命令。输出里不应再出现 `missing node`。

**通过标准**

真实场景能加载，关键节点存在，weekly-run 最小路径能走到派遣。

### 003. 运行时空对象或方法不存在

**报错长什么样**

```text
Invalid call
Attempt to call method ... on a null instance
Nonexistent function ... in base Nil
missing method: _on_open_dispatch_requested
not initialized: explore_phase
```

**人话解释**

游戏已经开始跑了，但它拿到的某个对象是空的。可以理解成：系统准备给某人打电话，结果电话本里这个人的号码是空白。

**常见原因**

- 子场景没有初始化成功。
- `_ready()` 里本来该赋值的变量没有赋上。
- 节点路径改了，变量变成 `null`。
- 方法改名了，但按钮、信号或 smoke test 还在调用旧名字。
- 场景创建顺序变了，代码太早运行。

**怎么修**

- 先找日志里第一个 `null` 或 `missing method`，优先修第一个；后面的错误可能只是连锁反应。
- 如果这个对象是流程必需的，smoke test 应该明确失败，不要隐藏。
- 如果这个对象是可选的，写清楚空状态分支。
- 被按钮、信号、测试调用的方法名尽量保持稳定；要改名就同步所有调用点。

**怎么验证**

跑默认验证命令。如果错误发生在更后面的交互，就在 `gda_angus_weekly_run_smoke.gd` 里补一个最小调用，让下次能抓到。

**通过标准**

smoke 能进入探索、选择地区、打开派遣、切换一名员工，中途没有 null 或方法缺失错误。

### 004. `class_name` 或单文件校验假阳性

**报错长什么样**

```text
Class "WeeklyRunActionItem" hides a global script class.
gda script validate failed for a class_name helper script
```

**人话解释**

有些 Godot 脚本会用 `class_name` 注册成全局类。单独检查这一个文件时，工具可能误以为它和项目里已经注册的类冲突。这个不一定代表项目真的坏了，但也不能无脑忽略。

**常见原因**

- 一次性把所有 `.gd` 文件都拿去单文件校验。
- 某个 `class_name` 脚本脱离完整项目加载路径后，被工具误判。
- 项目已经认识这个类，单文件检查又重新注册了一遍。

**怎么修**

- 默认 smoke 不要全量单文件校验所有 `.gd`。
- 默认只校验入口脚本和 smoke runner。
- 对刚改过、适合单文件检查的脚本，才加 `-ExtraValidateScript`。
- `class_name` 相关问题主要靠完整 Godot headless 场景运行覆盖。
- 如果完整项目运行也报同类冲突，那就当真问题修。

**怎么验证**

默认验证应只检查这些入口：

```text
scenes/gameplay/weekly_run/WeeklyRunGame.gd
tests/gda_angus_weekly_run_smoke.gd
```

然后完整 headless 场景必须通过。

**通过标准**

入口脚本没有 `valid: false`，完整 Godot headless 运行也没有类名冲突。

### 005. Godot 版本、PowerShell 或 `gda` 环境失败

**报错长什么样**

```text
running scripts is disabled on this system
Godot executable not found
Using Godot executable: ...4.3...
gda was not found on PATH
uvx was not found
No package found in offline mode
```

**人话解释**

这时游戏本身可能没坏，而是“检查工具没跑起来”。像体温计没开机一样，不能据此说病人没事，也不能说病人有事。

**常见原因**

- Windows 禁止直接运行 `.ps1`。
- 脚本找到了旧版 Godot，而不是项目需要的版本。
- 没全局安装 `gda`，`uvx` 也不能下载。
- 第一次运行就用了离线模式，缓存里还没有包。
- Python 路径不存在或指错了。

**怎么修**

- 用本文档里的 `powershell.exe -ExecutionPolicy Bypass -File ...` 命令。
- 看输出里的 `Using Godot executable:`，确认它优先用 repo 里的新版 Godot，通常应是 4.6 系列。
- 如果 `gda` 第一次需要下载，只在确认允许联网时去掉 `-GdaOffline`。
- 需要指定 Godot 时，传 `-GodotPath`。
- 需要指定 Python 时，传 `-PythonPath`。

**怎么验证**

检查器本身要打印出这些关键行：

```text
Using Godot executable: ...
Using gda command: ...
PASS gda validate: ...
Running Godot headless smoke: res://tests/gda_angus_weekly_run_smoke.gd
Godot agent smoke passed.
```

**通过标准**

只有检查器真的跑完，并且最后 smoke 通过，才能说测试通过。不能因为脚本存在就说通过。

### 006. Godot 原生程序崩溃或 Windows 应用程序错误

**报错长什么样**

```text
Godot_v4.6.2-stable_win64.exe - 应用程序错误
0x... 指令引用了 0x0000000000000058 内存。该内存不能为 read。
要终止程序，请单击“确定”。
```

**人话解释**

这通常不是普通 GDScript 报错，而是 Godot 程序本身崩了。可以理解成：不是游戏规则里某张表写错，而是打开游戏引擎的那个程序先摔了。现有 `gda + headless smoke` 主要检查脚本和真实场景最小路径，不能自动覆盖所有 GUI 启动、编辑器、显卡渲染、导入缓存或不同 Godot exe 的原生崩溃。

**常见原因**

- 用户或脚本打开的是 `Godot_v4.6.2-stable_win64.exe` GUI 版，而 smoke 默认使用 repo 里匹配项目的 console / headless 版，例如 4.6.3。
- Godot 编辑器 / GUI 渲染路径崩溃，但 headless 路径仍然通过。
- 显卡驱动、渲染后端、窗口初始化、编辑器缓存、`.godot` 导入缓存或用户目录缓存有问题。
- 项目启动时加载了某个资源或插件，导致 Godot 原生层崩溃，来不及输出正常 GDScript 错误。
- 直接双击 Godot 或打开编辑器，不会自动触发 Angus smoke gate。

**怎么修**

- 先确认这次崩溃用的是哪个 exe。截图标题里的版本和文件名必须记录下来。
- 立刻跑一次默认 smoke，判断项目脚本 / 场景最小路径是否仍健康。
- 如果 smoke 通过，把问题归类为“GUI / 原生进程崩溃”，不要误判为 GDScript 已坏。
- 尝试用 repo 当前推荐的 Godot console/headless 版本验证；不要混用旧版 4.6.2 GUI 和新版 4.6.3 headless 结论。
- 如果必须打开 GUI，下一步再做专门的 GUI 启动测试、渲染后端切换、缓存隔离或最小复现项目。不要把 headless smoke 当成 GUI 崩溃保险。

**怎么验证**

先跑默认 smoke：

```powershell
powershell.exe -ExecutionPolicy Bypass -File "D:\angos\scripts\run_godot_agent_smoke.ps1" -GdaOffline -PythonPath "C:\Python314\python.exe"
```

如果 smoke 通过，再单独验证 GUI / 具体 exe：

```powershell
powershell.exe -ExecutionPolicy Bypass -File "D:\angos\scripts\run_godot_gui_startup_check.ps1" -GodotPath "D:\angos\tools\godot\4.6.2-stable\Godot_v4.6.2-stable_win64.exe"
```

记录：

```text
使用的 Godot exe:
是否 GUI:
是否 console/headless:
是否同一版本:
是否仍弹 Windows 应用程序错误:
```

**通过标准**

分两层判断：

- `Godot agent smoke passed.` 只能说明 Angus 最小 headless 场景路径健康。
- GUI / 编辑器崩溃必须用同一个 GUI exe 再打开成功，或有明确的原生崩溃原因与规避方案，才算该问题通过。

## 新卡模板

当新的可复发 Godot 错误出现时，用这个格式追加：

````md
### 00X. 短错误名

**报错长什么样**

```text
贴稳定、可识别的报错片段。
```

**人话解释**

用不懂引擎的人也能理解的方式解释哪里坏了。

**常见原因**

- ...

**怎么修**

- ...

**怎么验证**

先跑最小相关命令；如果影响真实 Godot 项目路径，再跑完整 Godot agent smoke。

**通过标准**

写清楚哪一句输出、退出码、截图或场景行为能证明修好了。
````
