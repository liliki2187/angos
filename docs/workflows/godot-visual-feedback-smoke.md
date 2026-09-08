# Godot 视觉反馈 Smoke

这是针对现有探索/派遣路径的图像采集与基本有效性检查；需要这条路径的证据时使用，不是任意 Godot 改动的固定后续步骤。

一句话：`godot-agent-smoke` 证明场景能跑，这个脚本证明同一条真实路径能产出可看的运行截图。

## 它解决什么问题

Godot 改动常有两类假通过：

1. 代码没报错，节点也存在，但画面是黑的、空的、脏帧或关键区域没渲染出来。
2. 只跑了 headless / 逻辑 smoke，就声称 UI 没问题，但玩家看到的真实窗口没有证据。

这个 smoke 不判断美术好坏；父级仍需查看实际图像并说明判断依据，角色协作按当前任务选择。它只挡住最基础的视觉假阳性：截图文件必须真实生成、分辨率正确、非黑帧、颜色多样性正常、主要屏幕区域有可见内容。

## 命令

```powershell
powershell.exe -ExecutionPolicy Bypass -File .\scripts\run_godot_visual_feedback_smoke.ps1
```

默认使用仓库里已验证可做 windowed 截图的 Godot 4.6.2 console。不要把 headless smoke 自动选到的版本，直接等同于 windowed 视觉截图也可用；本机已观察到 4.6.3 的 windowed 截图路径可能超时。

```text
tools/godot/4.6.2-stable/Godot_v4.6.2-stable_win64_console.exe
```

如果要指定 Godot：

```powershell
powershell.exe -ExecutionPolicy Bypass -File .\scripts\run_godot_visual_feedback_smoke.ps1 -GodotPath "D:\angos\tools\godot\4.6.2-stable\Godot_v4.6.2-stable_win64_console.exe"
```

## 它会产出什么

截图目录：

```text
docs/screenshots/2026-07-29-godot-visual-feedback-smoke/
```

当前最小路径会保存四张图：

1. `01-world-map-region-ready.png`：进入探索后的世界地图 / 地区选择。
2. `02-region-task-m330-selected.png`：进入北美首区并选中 `m330` 任务。
3. `03-dispatch-m330-no-staff.png`：打开派遣界面但未选人。
4. `04-dispatch-m330-staff-selected.png`：选中 `ivy` 和 `mora` 后的派遣界面。

同时生成：

```text
capture-manifest.json
```

里面记录每张截图的尺寸、采样颜色数、黑色采样比例、透明采样数和通过状态。

## 此脚本的通过条件

下列阈值只对这条既有采集路径有效，不作为新页面的通用亮度、配色或尺寸限制。此脚本要求：

- 尺寸为 `1920x1080`。
- 透明采样数为 `0`。
- 采样颜色数不少于 `240`。
- 黑色采样比例不高于 `35%`。
- header、left、center、right 四个关键区域都有足够可见信号。
- 四张 PNG 和 `capture-manifest.json` 都存在。

## 什么时候调用

改动影响本文四个状态、对应阶段切换或共享渲染层，且需要确认实际窗口图像时调用。其他界面或单个局部可以使用已有专项采集，按 [截图指引](../onboarding/功能改动截图指引.md) 覆盖受影响内容。运行接线仍有疑问时选 [运行检查](godot-agent-smoke.md)，不强制先后顺序或重复已有证据。

## 它不能证明什么

它不能证明：

- UI 已经好看；
- 文字安全区已经通过；
- 资产化 UI 能进入生产；
- 所有状态都覆盖；
- 动效节奏正确；
- Godot GUI 编辑器不会崩。

如果用户看到的是 Windows 原生 Godot 崩溃弹窗，仍应跑：

```powershell
powershell.exe -ExecutionPolicy Bypass -File .\scripts\run_godot_gui_startup_check.ps1
```

## 对 agent 的使用规则

当 agent 修 Godot 后，最终回复里必须分清：

- `godot-agent-smoke passed`：代码 / 节点 / 最小运行路径通过。
- `godot-visual-feedback-smoke passed`：真实运行截图可用。
- `visual quality approved`：必须说明由谁、基于哪张图、对什么范围作出判断；内部审查不能冒称用户认可，角色名不自动证明质量。

不要把第二项冒充第三项。
