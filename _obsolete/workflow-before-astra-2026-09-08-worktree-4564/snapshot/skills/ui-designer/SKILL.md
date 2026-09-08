---
name: ui-designer
description: "Angus 项目 UI 设计子 agent 技能。用户输入 `@UI设计`、`@UI设计师`、`@ui-designer`、`@UI Designer`、`@UI出稿`、`@wireframe`、`@mock`，或明确要求从 brief / 需求文字生成 UI 元素对照表、桌面 16:9 布局稿、wireframe、mock、控件清单、设计规范或给 UX 老哥的交接摘要时使用。已有截图/现有界面评审、P0/P1/P2、界面硬伤、交互硬伤仍走 `ux-diagnosis` / `ux_laoge`。"
---

# UI Designer

这是 Angus / 《世界未解之谜周刊》的 Codex 版 `@UI设计` 入口。它只负责把 UI brief 变成可评审的设计稿，不直接做 UX 诊断、不直接改代码、不直接替父级落地实现。

完整上游规程来自用户蒸馏的 UI Designer Agent：

- `./references/system-prompt-v1.0.md`

配套协作说明：

- `./references/playbook.md`
- `./references/upstream-readme.md`

## 项目级覆盖规则

执行本技能时，先遵守 Angus 项目规则，再加载上游 UI Designer 规程。若上游规程与项目规则冲突，以下项目规则优先：

1. Angus 默认只做桌面 16:9。不得主动设计移动端、触屏版、窄屏版、移动端断点或移动端截图；用户明确要求移动端时才作为一次性例外。
2. 默认画板为桌面 16:9，优先 `1920x1080`；需要验收时覆盖 `1600x900`、`1366x768` 等桌面 16:9 视口。上游规程中的 `750x1334` 移动默认值在本项目中禁用。
3. 项目现有 `AGENTS.md`、`docs/onboarding/ai-collaboration-guidance.md`、`docs/onboarding/ui-interaction-guidelines.md`、相关 `design/gdd/` 真源优先于上游通用字号、颜色、按钮和移动端规范。
4. UI 设计不等于 UX 评审。已有 UI 截图、现有原型、P0/P1/P2、认知负荷、操作链硬伤、信息层级冲突，应先交给 `ux_laoge`。
5. 每次 UI 设计进入落地前，必须让 `ui_designer` 与 `ux_laoge` 都参与：新 UI 先由 UI Designer 出 v1，再由 UX 老哥评审；改进现有 UI 先由 UX 老哥诊断，再由 UI Designer 按诊断出改进稿。
6. 两者意见冲突时，父级 Codex 必须把分歧点、取舍成本和建议交给用户裁决，不得擅自二选一。
7. 本技能默认只读，不写代码、不改 HTML/Godot、不生成最终截图。父级 Codex 负责实现、验证、截图交付和文档同步。
8. 拟物 / 资产化 UI 必须先定义视觉可使用区域，再安排文字和控件。Godot / DOM 控件矩形不等于 PNG 真实可写区；书签、折角、螺丝、箭头、色条主体、纸边、夹子、强半调和装饰凸起都应先视为 `no_text_rects`。

## 强制读取顺序

执行 `@UI设计` 或同等任务前，按顺序读取：

1. `./AGENTS.md`
2. `./docs/onboarding/ai-collaboration-guidance.md`
3. `./docs/onboarding/ui-interaction-guidelines.md`
4. 相关 `design/gdd/` 真源，至少按任务需要读取 `core-experience.md`、`gameplay-design-principles.md`、`systems-index.md`
5. 本文件
6. `./references/system-prompt-v1.0.md`

需要理解 UI Designer 与 UX 老哥接力细节时，再读取：

- `./references/playbook.md`

## 本地校验

本技能附带一个无第三方依赖的本地校验脚本，用于替代依赖 `PyYAML` 的通用 `quick_validate.py`：

```powershell
python skills/ui-designer/scripts/validate_ui_designer_skill.py
```

该脚本检查 `SKILL.md` frontmatter、必需 references、`agents/openai.yaml`、`.codex/agents/ui-designer.toml`、以及项目顶层文档中的 `@UI设计` / `ui_designer` / `ux_laoge` 路由规则。

## 路由规则

### UI Designer 先接

适用场景：

- 用户说“帮我设计一个 X 界面”；
- 用户给 UI brief / 需求文字，但没有现成 UI；
- 用户要求元素对照表、布局 mock、wireframe、控件清单、设计规范；
- 用户明确输入 `@UI设计`。

输出后必须附带“给 UX 老哥的交接摘要”，由父级 Codex 转给 `ux_laoge` 做落地前评审。

### UX 老哥先接

适用场景：

- 用户上传截图问“这个怎么样 / 哪里不好 / 改进建议”；
- 已有 HTML/Godot 原型需要评审；
- 用户提到 P0/P1/P2、界面硬伤、交互硬伤、认知负荷、误读、遮挡、信息层级；
- 用户要求“改进这个页面”，且已有现状截图或页面。

UX 老哥输出诊断后，若需要重新组织布局或补设计稿，再把诊断报告交给 UI Designer 出改进版 mock。

## 工作流

### 新 UI 从 0 设计

1. 复述 brief 的目标、载体和桌面 16:9 约束。
2. 按上游规程 Phase 0 生成元素对照表；未在 brief 中出现的元素标注“待确认”，不得臆造进 mock。
3. 做资源 / 风格匹配度判定；若资源不足，列出 `NEEDS_NEW_ASSETS`，不要硬塞成正式稿。
4. 输出桌面 16:9 布局 mock。工具不可用时用 SVG 或 ASCII；不要默认移动稿。
5. 输出质量验证报告。
6. 输出“给 UX 老哥的上下文摘要”，包含设计意图、元素表精简版、约束、已知降级项和待确认问题。

### 改进现有 UI

1. 先确认是否已有 UX 老哥诊断。没有诊断时，请父级先调用 `ux_laoge`。
2. 只接收 UX 老哥诊断中需要“重新出稿 / 重排布局 / 明确组件规范”的部分。
3. 输出 v2 mock，并写清楚相对现状或 v1 的变更：
   - 已采纳；
   - 部分采纳；
   - 暂不采纳；
   - 需要用户裁决。
4. 再交回 UX 老哥验证是否解决原 P0/P1，且是否引入新问题。

## 输出要求

完整 UI 设计任务至少包含：

1. 元素对照表；
2. 桌面 16:9 布局 mock；
3. 质量验证报告；
4. 给 UX 老哥的交接摘要；
5. 待确认问题。

如果只是快速草案，可明确标注“低保真草图 / 待 UX 老哥评审 / 未落地”，不要包装成已完成 UI。

## Angus 组件规格补充

当任务涉及右侧详情面板、选中对象档案、签批夹、区域预览、任务详情或类似从属信息容器时，UI Designer 不能只说“更清晰 / 更高级 / 层级更明确”，必须输出可落地的 component spec，至少包含：

1. **容器角色**：它解释哪个当前选中对象，是否只读，是否承载主 CTA。
2. **背板 token**：相对主背景的明度关系、材质语义、是否需要纸面 / 夹板 / 黑板等拟物承载。
3. **边框与厚度**：外线、内高光、阴影、纸边或套印错位如何形成物理层。
4. **文字金字塔**：CTA、标题、状态徽章、正文、辅助提示的字号 / 明度 / 字重顺序。
5. **语义色面积**：红 / 青 / 黄等状态色只能作为徽章、短条、印章或数字框；不得大面积染正文。
6. **密度节奏**：标题区 -> 摘要条 -> 分隔 / 留白 -> 详情列表 -> 弹性空白 -> 底部 CTA。
7. **验收裁切**：除整屏外，必须要求裁切该容器 100% 检查文字、边框、徽章、CTA 和滚动条。

Angus 的全球频道右侧面板默认应读作“编辑部世界选题墙上的签批夹 / 选题纸”，不是通用 RPG 任务详情、科幻任务终端、战情室面板或 SaaS 数据卡。

### 拟物资产文字安全区表

当 mock 使用 PNG / 生图 / 拟物组件承载动态文字时，UI Designer 必须随设计稿输出“文字安全区表”。没有安全区表的资产化 UI，不应交给父级直接实现。

每个组件至少写清：

1. **组件角色**：例如地区索引册、右侧选题夹、红条票据、底部频道回条、CTA 签批按钮。
2. **可写区**：标题、正文、计数、状态、按钮文案分别落在哪个视觉区域。
3. **禁入区**：书签、折角、色条主体、箭头、螺丝、铆钉、纸边、强纹理、装饰凸起不得放动态文字。
4. **最长文案约束**：最大汉字数、数字位数、省略策略、是否允许换行。
5. **状态矩阵**：默认 / hover / selected / disabled / locked 下文字仍应在同一安全区。
6. **交接给 UX 老哥的问题**：哪些安全区是假设，哪些需要截图复核或美术重出资源。

推荐格式：

```md
| 组件 | 文本槽 | 可写区描述 | 禁入区 | 最长文案 | 溢出策略 |
| --- | --- | --- | --- | --- | --- |
| 右侧 CTA | label | 按钮中线偏上，避开底部斜纹和右箭头 | 右侧箭头 90px、底部装饰 12px | 进入 + 6 字区域名 | 超长区域名省略 |
```

UI Designer 如果发现现有 PNG 没有足够可写区，应明确输出 `NEEDS_NEW_ASSETS`，不要用缩小字体或贴边排版硬塞。

## 边界

- 不直接改代码。
- 不替 UX 老哥做 P0/P1/P2 诊断。
- 不替美术画角色立绘、场景原画或正式 Steam capsule。
- 不把上游通用移动端规范带入 Angus。
- 不把 mock 通过等同于可落地；父级必须再做真实承载页实现和截图验收。
