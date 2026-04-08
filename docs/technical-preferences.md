# 技术偏好

<!-- Angus 项目的技术默认约束。 -->
<!-- 当团队有意识地调整编码规范、测试策略或引擎级限制时，更新本文件。 -->

## 引擎与语言

- **引擎**：Godot 4.6.2 stable
- **主要运行时语言**：GDScript
- **辅助工具语言**：PowerShell、Python，以及少量仅用于工具链的 C# 或 Node.js
- **本地锁定引擎目录**：`tools/godot/4.6.2-stable/`
- **渲染**：以 2D / UI 为主的 Godot 项目，使用项目设置中的 `mobile` 渲染方式
- **物理**：极少使用。本项目主要由 UI、状态切换和公式驱动，而不是物理模拟。

## 命名规范

- **类 / 场景脚本**：当脚本与场景或功能成对出现时使用 PascalCase，例如 `MainMenu.gd`、`EventCheck.gd`、`FullChainGame.gd`
- **变量**：使用 snake_case，例如 `selected_region_id`、`editorial_profile`
- **函数**：使用 snake_case，例如 `_refresh_all()`、`_calculate_node_probabilities()`
- **信号 / 事件**：使用 snake_case 的动作名或过去式名称，例如 `closed`
- **场景**：使用与场景用途匹配的 PascalCase `.tscn`，例如 `MainMenu.tscn`、`MysteryBroadsheetModal.tscn`
- **常量**：使用 UPPER_SNAKE_CASE，例如 `DIFFICULTY_P`、`MACRO_LABELS`、`PSD_UI_PREVIEW_SIZE`
- **脚本文件**：
  - 运行时场景脚本遵循现有的 PascalCase 配对模式
  - `scripts/` 下的工具和管线脚本可以使用 snake_case 或动词导向命名

## 目录规范

- **正式 Godot 项目根目录**：`gd_project/`
- **运行时场景**：`gd_project/scenes/`
- **正式 UI 场景与组件**：`gd_project/scenes/ui/`
- **运行时资产**：`gd_project/Assets/`
- **UI 设计稿、规范与高保真布局**：`design/ui/`
- **编辑器插件 / addons**：`gd_project/addons/`
- **面向引擎的工具**：`scripts/`
- **非引擎自动化 / 打包脚本**：`scripts/`
- **HTML 原型与参考实验室**：`design/prototypes/html/`
- **正式玩法设计文档**：`design/gdd/`
- **系统分析与补充设计说明**：`design/systems/`
- **架构决策**：`docs/architecture/`
- **生产追踪与协作**：`production/`
- **HTML 原型与参考实验**：仅作参考，不是运行时真实来源

## 真实来源规则

- **Godot 是当前 MVP 唯一规范运行时**。
- **`gd_project/` 是日常游戏开发唯一正式运行时根目录**。
- **`design/gdd/` 是当前玩法行为的正式设计层**。
- **HTML 原型仅是参考材料**。如果 `design/prototypes/html/` 中某条规则要提升进游戏，必须先同步到 `design/gdd/`，之后才能视为规范。
- **`Globals` 必须保持轻量**，只用于启动、场景路径、调试日志和少量共享辅助，不得成为玩法状态的永久归宿。

## 文档与落盘语言

- 默认使用简体中文编写并更新仓库内文档。
- 适用范围包括 `README`、GDD、ADR、计划、规格、交接、报告、清单及其他 `*.md` / `*.txt` 文档文件。
- 代码、路径、命令、配置键、API 字段、类名、文件名、外部官方名称和许可证文本可以保留英文。
- 如果模板或历史文档是英文，更新时应优先整体译为中文，而不是继续追加英文内容。

## 架构偏好

- 优先把 **内容数据**、**周状态 / 规则** 与 **场景表现** 分离。
- 当一块新内容可以被干净抽离时，不要继续扩张单体场景脚本。
- 新玩法改动应能追溯到某份 GDD、spec 或 ADR。
- 当引入具有长期影响的新技术边界或工作流时，在 `docs/architecture/` 中留下记录。

## Godot UI 实现规范

- 正式 UI 优先使用 `.tscn` 场景和可复用组件场景完成布局、层级和基础控件结构。
- UI 脚本默认只负责节点引用、信号连接、数据绑定、显隐切换和状态刷新，不负责手工拼装固定布局。
- 对于数量可变的列表、卡片、日志、槽位等内容，优先实例化预制的 item scene，而不是直接 `new` 原始 `Control` / `Button` / `Label` / `Container` 树。
- UI 不拥有玩法真状态，只读取状态并通过信号或明确接口发出动作请求。
- `dev`、`debug`、纯原型、特效型界面可以受控例外，但必须在对应 spec、注释或 ADR 中注明，不得作为正式 UI 模板扩散。

## 性能预算

- **目标帧率**：60 FPS
- **单帧预算**：16.6 ms
- **主要风险区域**：UI 刷新抖动与全流程单体场景逻辑
- **Draw Calls**：`[待配置]`
- **内存上限**：`[待配置]`
- **加载时间预算**：`[待配置]`

## 测试

- **推荐框架**：GdUnit4 或 GUT
- **本地 smoke test 入口**：`scripts/run_weekly_run_smoke_tests.ps1`，默认优先使用 `tools/godot/` 下的仓库内引擎
- **最低覆盖策略**：在追求广覆盖前，优先覆盖关键公式与阶段 / 状态切换
- **必须关注的回归覆盖区域**：
  - 事件检定概率与结果层级
  - 周循环阶段切换
  - 结算公式与订阅更新
  - 解锁规则与隐藏节点可见性
  - 内容 / 配置解析（待配置管线落地后）

## 禁止模式

- 不要把 HTML 原型视作与运行时同级的实现目标。
- 不要把新的长期玩法状态塞进 `Globals`。
- 不要在没有明确理由的情况下，把内容数据、状态所有权、公式和 UI 刷新重新混进新的单体脚本。
- 不要在 GDScript 中继续写 `Array[Array[T]]`、`Array[Dictionary[String, T]]` 这类嵌套 typed collections；稳定版文档仍不支持，改用 `Array[Array]`、typed dictionaries、显式校验函数或独立状态类。
- 不要在正式 UI 中继续使用 `Button.new()`、`Label.new()`、`HBoxContainer.new()` 之类的方式拼装固定布局。
- 不要把“允许实例化预制组件场景”误用成“允许继续现场手搓原始控件树”。
- 不要在未更新相关 GDD 或 ADR 的前提下硬编码新的核心玩法规则。
- 不要把本应放在 `design/`、`_obsolete/` 或 `scripts/` 下的实验内容，新增为仓库根层入口文件。
- 不要把新的 Godot 运行时内容放到 `gd_project/` 之外。
- 不要把本该在 `scripts/` 下的引擎辅助脚本重新塞回运行时目录。
- 不要让 AI 在仓库中新增英文说明文档，除非用户明确要求或该文件属于上游/第三方原文。

## 允许的库 / Addon

- `nklbdev.importality`，用于 PSD 导入工作流
- `scripts/` 下的项目本地引擎辅助脚本
- `.github/workflows/` 下的 GitHub Actions 工作流
- 其他第三方 addon 只有在被明确接受并文档化后才能加入

## 构建 / 导出默认约定

- Godot 导出预设保存在 `gd_project/export_presets.cfg`
- CI 构建与导出自动化视为仓库自有工具链
- 优先使用可复现的打包脚本，而不是手工复制粘贴式发布流程

## 架构决策记录

- `ADR-0001`：Godot 周循环状态与数据边界
- `ADR-0002`：Godot UI 场景优先与绑定式脚本规范
- `ADR-0003`：Demo 周状态字段向正式 Weekly Schema 的迁移边界
