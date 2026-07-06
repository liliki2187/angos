# Angus AI Radar Memory

> 状态：2026-07-02 起作为 AI 日报 / 次报线程的上下文侧车。
> 目标：把用户强反馈、日报规则、错题本、eval case 和上次报告状态对象化，避免上下文压缩或换线程后丢失。

## 使用场景

当用户说“发日报”“发次报”“继续日报”“复盘日报”“这条进错题本”“转成 eval case”时，先读本文件，再读 `ai-radar-loop-cases.md`。

本文件不替代联网检索。它只回答“Angus 需要怎样筛选、解释和交付 AI 情报”；具体新闻、论文、工具版本、来源和发布日期仍必须当次联网验证。

## 核心原则

1. **从聊天流变成对象**：重要反馈不能只留在对话里，要沉淀成可检索对象。
2. **先区分对象类型**：强反馈、错题本、eval case、已采纳规则、上次报告状态分别记录，不混成一段总结。
3. **不把推演冒充事实**：工具实际能力、论文评测任务、Angus 可能用法、制作人判断必须分层。
4. **不重复旧报**：除非有新版本、新官方说明、新可复现结果、新安全事件或 Angus 跟进行动，否则不要复用上次重点条目。
5. **图文不降密度**：图形化是帮助理解，不是减少信息。中文密集解释优先用 HTML / SVG / Markdown / Mermaid 等可控版式；若用生图，必须先写清文字版。

## 上下文对象类型

### 1. 用户强反馈

记录用户明确纠错、不满意、要求复盘或要求防复发的原始问题。

字段：

```md
ID:
日期:
范围: AI日报 / 自动化 / 图文页 / 工具解释 / 周报
用户反馈:
当时产物:
本质问题:
影响:
本轮处理:
```

### 2. 错题本 / Loop Case

把强反馈转成下次交付前必须检查的规则。错题本不一定都能自动测试，但必须能指导人工检查。

字段：

```md
ID:
触发来源:
错误模式:
防复发规则:
交付前检查:
适用范围:
状态: active / superseded
```

### 3. Eval Case

当错题能被相对稳定地判定，就升级为 eval case。eval 可以先是自然语言 checklist，后续再脚本化。

字段：

```md
ID:
输入样本:
应通过条件:
应失败条件:
人工判定口径:
脚本化可能性: low / medium / high
```

### 4. 已采纳规则

只有用户明确同意后，才写成已采纳规则。已采纳规则应进入本文件、`ai-radar-loop-cases.md` 或更上游的 workflow / design-decisions。

字段：

```md
ID:
采纳日期:
规则:
适用范围:
已同步位置:
```

### 5. 上次报告状态

每次正式日报 / 次报后更新，用来避免重复旧内容。

字段：

```md
报告标题:
产出日期:
覆盖窗口:
重点条目:
弱信号:
下次报告禁止重复:
允许追踪条件:
```

## 日报 / 次报交付结构

### 标题层

不要把陌生论文名或工具名直接当大标题。先用人话标题说明“这是什么变化”，再给正式名称。

推荐：

```md
### 1. 给 Agent 加长期记忆的训练方法
- 名称：AutoMem
```

避免：

```md
### 1. AutoMem
```

### 重点条目

每条重点必须包含：

- **名称**：工具 / 论文 / 平台 / 版本名。
- **类型**：workflow / benchmark / image / video / game production / security / platform / weak signal。
- **新在哪里**：今天或本报告窗口内为什么值得看。
- **它是什么**：一句话解释，不用术语堆叠。
- **它实际能做什么**：只写已发布、论文明确展示或官方说明的能力。
- **典型例子**：给一个具体场景，帮助快速想象。
- **制作人判断**：Angus 是否吸收、怎么吸收、先做什么小实验。
- **风险 / 不要误读**：论文不是产品、demo 不是可用工具、benchmark 不是能力本身等。
- **来源**：优先官方、论文、GitHub、Hugging Face、产品 changelog。

### 弱信号

弱信号可以更短，但仍要说明“为什么对 Angus 有一点价值”。不收录纯大厂融资、泛泛模型榜单、与生产关系不清的营销新闻。

### Angus 行动

最后给 1-3 个可执行动作。动作必须具体，例如：

- 建一个 `memory-sidecar.md` 模板。
- 给 Codex eval 加 3 个 perturbation case。
- 把某类工具列入“观察，不落地”。

## 分类规则

### 通用 AI 工作流突破

收录会改变 Angus 制作方式的 agent、harness、loop、MCP、上下文管理、长期记忆、工具调用、代码代理、自动化评测、协作工作流。

筛选问题：

- 它能不能减少我们长任务中“忘规则 / 乱跳步 / 没复盘”的问题？
- 它能不能变成 Angus 的 Codex eval、workflow harness 或制作流水线？
- 它是新能力，还是只是包装现有 prompt？

### 生成工具突破

收录图像、视频、音频、角色一致性、局部编辑、分镜、UI 草图、VFX 等工具。

筛选问题：

- 它实际能产出什么资产或中间稿？
- 是否支持局部编辑、风格一致性、角色一致性、可控镜头、批量迭代？
- Angus 该把它用于灵感、风格稿、真实内容 mock，还是生产候选？

### 游戏制作垂直工具

收录动画、动作生成、像素 / Spine / Aseprite / Blender / Godot / Unity、AI playtest、关卡生成、任务生成、QA、特效、UI 生产链工具。

筛选问题：

- 能不能直接减少 Angus 的角色、UI、任务、动画、测试或工具链成本？
- 是否和当前 Godot / HTML / assetized UI 链路兼容？
- 是否需要大量工程接入，还是可以先做离线实验？

### 个人向弱信号

收录小但可能改变工作习惯的 skill、repo、个人 workflow、prompt pattern、独立开发者管线。

筛选问题：

- 是否能转成一个 Angus 小实验？
- 是否解决了我们刚暴露过的错题？
- 是否只是热闹，和 Angus 没有真实连接？

### 平台 / 法务 / 成本 / 生态

收录 Steam AI 披露、模型价格、开源许可、版权风险、本地化、平台规则、工具弃用、API 改动、安全事件等。

筛选问题：

- 会不会影响 Angus 上架、宣发、素材来源、生产成本或工具选择？
- 是强制变化，还是观察即可？

## 报告窗口

- 用户说“发日报”：默认覆盖上次正式报告后到当前时间的 AI 情报；若没有上次记录，则覆盖最近 24 小时并说明。
- 用户说“发次报”：覆盖上次正式日报 / 次报之后到当前时间，不按自然日强行切分。
- 间隔 1 天：偏日报。
- 间隔 2-4 天：偏次报，重点看新增和进展。
- 间隔 5-7 天以上：加一个 mini-weekly 趋势判断。

## 交付前检查

每次发报告前检查：

- 是否联网验证了“最新 / 今日 / 本窗口”。
- 是否列明覆盖时间。
- 是否避开上次已经报道过且无新进展的条目。
- 每个重点条目是否有人话标题。
- 每个重点条目是否有“新在哪里”。
- 是否解释“它实际能做什么”和“典型例子”。
- Angus 判断是否放在事实解释之后。
- benchmark / dataset / survey 是否没有被写成工具能力。
- video / image / edit / generator / platform 名称是否没有被误命名。
- “雷达”是否只作为报告栏目名，不作为单个工具标题，除非官方名称如此。
- 来源是否优先官方 / 论文 / GitHub / changelog。

## 当前报告状态

### 上次正式次报

- **报告标题**：Angus AI 次报 - 2026-07-02 扩源版
- **覆盖窗口**：从 `Angus AI 日报 - 2026-07-02 重制版` 之后到本次检索时点；同时按用户新增要求，补扫近 7-30 天内未进入前报的游戏制作小工具、GitHub 工作流、MCP 目录、itch 工具页、游戏行业 AI 披露与创作者实践。
- **重点条目**：Godot AI Agent CLI / gda、Aseprite MCP Pro、itch.io AI tools / AI assets 矿源、MCP Server Architecture Patterns、GameDevBench v2、Steam AI 披露与 AI Warning for Steam、MUSE 3D scene authoring。
- **弱信号**：Unity MCP Server、UnrealClaude、AI Game DevTools、AI-driven graphical asset heuristics、Claude Code + Godot 个人实验。
- **下次报告禁止重复**：上述条目不得作为新重点重复，除非出现新版本、官方更新、开源代码变更、真实 Angus 小实验、安全后续或平台规则变化。
- **允许追踪条件**：`gda` 若 Windows headless / live 支持、Godot 4.6 兼容或 Codex skill 接入有进展可追踪；Aseprite MCP 若 Windows 稳定性、免费替代或 Godot 导出链有可靠验证可追踪；Steam AI 披露若 Valve / Epic / 浏览器插件 / 数据研究出现新变化可追踪；GameDevBench 若发布代码、任务集或 Angus 可复用 eval case 可追踪。

### 上次正式日报

- **报告标题**：Angus AI 日报 - 2026-07-02 重制版
- **覆盖窗口**：2026-07-02 当日重制；按新规则补抓论文、GitHub / 产品 changelog、开源工作流、游戏制作生态与安全边界。包含少量 2026-06-11 到 2026-07-01 的重要补收项，已标注不是今日新发。
- **重点条目**：Copilot Browser Tools GA、Copilot Vision GA、GitHub Agentic Workflows、Awesome Agent Skills、Godot AI-authored contribution policy、0din / Claude Code clean-repo malware path、Theoria、Making Failure Safe、Performance-Optimization Benchmark Audit、SPIRE slide personalization。
- **弱信号**：Lightroom Generate Video、Claude creative connectors、Copilot C++ language-server skill、Copilot CLI auto model selection。
- **下次报告禁止重复**：上述条目不得作为新重点重复，除非出现新版本、官方实现、开源代码、可复现实验、重大安全后续或 Angus 已执行 follow-up。
- **允许追踪条件**：Copilot browser / vision 若用于 Angus 截图验收可追踪；Godot AI policy 若官方原文或贡献指南更新可追踪；Theoria / Making Failure Safe 若有代码或复现实验可追踪；Awesome Agent Skills 若出现高价值新 skill / repo 可追踪。

### 历史正式次报

- **报告标题**：Angus AI 次报 - 2026-07-02
- **覆盖窗口**：从 2026-07-01 正式报告之后到 2026-07-02 当次检索时点。
- **重点条目**：AutoMem、Self-GC、AI Native Games survey、OpenAgent、Mnemosyne。
- **弱信号**：Performance-Optimization Benchmarks、Coachable gameplay agents、ABot-M0.5、Valdi、BioInsight。
- **重复保护**：除非出现新版本、官方实现、GitHub 开源、复现实验、安全事件或 Angus 已执行 follow-up，否则不再把以上条目当新重点。
