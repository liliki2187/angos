# UI Designer Agent · 一键复制配置指南

> **本文件目的**：教你把这个 agent 装到任何 AI 平台上跑起来。
> **核心原则**：所有平台都靠一招—— **把 `SPEC.md` 整篇粘贴进对应字段**。差别只在于"粘贴到哪个字段"。

---

## 🚀 30 秒一键复制（所有平台通用）

```
1. 打开 SPEC.md
2. 全选所有内容（Ctrl+A）
3. 复制（Ctrl+C）
4. 在你的目标 AI 平台找到 system prompt / instructions / rules 字段
5. 粘贴（Ctrl+V）
6. 保存
7. 开始对话："帮我设计 XXX"
```

完事。**不需要任何额外工具、API、插件、控件库**。

---

## 📋 各平台具体配置方式

### 1. ChatGPT 自定义 GPT

```
1. 进入 https://chatgpt.com/gpts/editor
2. 配置 → Instructions 字段
3. 粘贴 SPEC.md 全部内容
4. Name: "UI Designer"
5. Description: "从 brief 出 UI 设计方案 (与 UX Critic 配合使用)"
6. 推荐勾选 capabilities：
   - ✅ Web Browsing（让它能搜参考资料）
   - ✅ DALL·E Image Generation（出风格概念稿）
   - ✅ Code Interpreter（生成 SVG 文件）
7. 保存
```

> 💡 **配套**：建议同时用 `Magic UX Agent` 那份蒸馏 spec 创建一个 "UX Critic" GPT，两个 GPT 在 ChatGPT 顶部切换使用。

---

### 2. Claude Project（推荐用法）

```
1. 进入 https://claude.ai → Projects → 新建 Project
2. Project Name: "Game UI Workshop"
3. Custom Instructions 字段 → 粘贴 SPEC.md 全部
4. Project Knowledge → 上传 PLAYBOOK.md（可选，给协作工作流参考）
5. 保存
```

> 💡 Claude Project 支持把 PLAYBOOK.md 一并上传，agent 在需要协作时会自动检索。

---

### 3. Cursor（开发场景用）

```
1. 在你的项目根目录创建：.cursor/rules/ui-designer.mdc
2. 文件开头加：
   ---
   description: UI Designer Agent for game/app UI design from brief
   globs: ["*"]
   alwaysApply: false
   ---
3. 粘贴 SPEC.md 内容
4. 用法：在 Cursor 对话中 @ui-designer
```

---

### 4. Cowork / Brainmaker（你当前的环境）

```
1. 在 .opencode-config/agents/ 下创建：cowork-ui-designer.md
2. 文件顶部加 frontmatter：
   ---
   description: UI Designer Agent - 从 brief 出 UI 设计方案
   mode: subagent
   color: "#9C27B0"
   ---
3. 粘贴 SPEC.md 内容（去掉文件头的版本声明那一段）
4. 重启 Cowork
5. 用 @cowork-ui-designer 调用
```

---

### 5. LangChain / LangGraph

```python
from langchain_core.messages import SystemMessage

# 读取 SPEC.md
with open('SPEC.md', 'r', encoding='utf-8') as f:
    system_prompt = f.read()

# 创建 agent
ui_designer = ChatAnthropic(
    model="claude-sonnet-4",
    system=system_prompt
)
```

---

### 6. 任何 LLM API（OpenAI / Anthropic / Gemini / DeepSeek）

```python
# 通用模板（任何支持 system role 的 API 都能用）
import requests

with open('SPEC.md', 'r', encoding='utf-8') as f:
    system_prompt = f.read()

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": "帮我设计一个登录页"}
]

# 然后调你的目标 LLM API
```

---

### 7. Dify / Coze / FastGPT（国产 AI 平台）

```
1. 创建新应用 / Bot
2. 类型：智能助手 / Agent
3. Prompt / Pre-Prompt 字段 → 粘贴 SPEC.md
4. 模型选择：建议 Claude Sonnet / GPT-4o / DeepSeek-V3 等强模型
5. 保存发布
```

---

### 8. 本地部署（Ollama / LM Studio）

```bash
# Ollama
cat SPEC.md | ollama create ui-designer-agent -f -

# 或直接用 Modelfile：
echo 'FROM llama3.1:70b
SYSTEM """' > Modelfile
cat SPEC.md >> Modelfile
echo '"""' >> Modelfile

ollama create ui-designer-agent -f Modelfile
ollama run ui-designer-agent
```

---

## 🔧 模型推荐 & 适配建议

| 模型 | 适配度 | 说明 |
|---|---|---|
| **Claude Sonnet 4 / Opus 4** | 🟢 最佳 | spec 就是为它写的，结构化指令理解最好 |
| **GPT-4o / GPT-4 Turbo** | 🟢 优秀 | 直接灌入即可，可能需要轻微 prompt tuning |
| **Gemini 2.5 Pro** | 🟢 优秀 | 视觉理解 + 长上下文优势 |
| **DeepSeek V3** | 🟡 良好 | 国产中表现最好，建议在 §3 Hard Rules 重复 2 次 |
| **Qwen 3 / Kimi K2** | 🟡 良好 | 同上，建议加 1-2 个 few-shot 示例 |
| **GLM 4 / 文心一言** | 🟡 凑合 | 建议把 SPEC 拆成多段 system + user 引导 |
| **小模型（< 70B）** | 🔴 不推荐 | 复杂 Confidence Gate 决策可能失控 |

---

## 🎁 配套伙伴 Agent 配置

### UX Critic Agent（强烈建议同时配）

本 agent 与 **UX Critic Agent** 互补不重叠（UX Critic = 你之前蒸馏的 Magic UX Agent v2.2.1+）。

**配置方法**（任何平台同样适用）：
```
1. 在同一平台再创建一个 agent
2. system prompt = 你蒸馏的 magic-ux 那份 spec
3. 命名为 "UX Critic" 或 "@ux-critic"
4. 这样你就有了：
   @ui-designer  → 从 0 设计
   @ux-critic    → 评审 + 改进建议
```

详见 `PLAYBOOK.md` 的协作工作流。

---

## 🧪 安装后的 5 分钟自检

在新装的 agent 上跑这 5 个测试，确认装对了：

### Test 1 · 基本响应
```
你: 你是谁？你能做什么？
预期: agent 自我介绍为 "UI Designer Agent"，明确说自己做"从 brief 出 UI 设计方案"，
     并主动说明自己不做评审（评审找 UX Critic）。
```

### Test 2 · 反臆造测试
```
你: 帮我设计一个登录页
预期: agent 主动询问澄清问题（平台桌面/移动？登录方式？品牌色？等），
     而不是直接出一个标准登录页 mock。
     如果它直接出 mock 不询问 → SPEC 没装对。
```

### Test 3 · 风格不匹配测试（Confidence Gate C1）
```
你: 我要做一个赛博朋克风的游戏 UI，但我手头只有 Material Design 的控件库
预期: agent 触发 AUTO-DECIDE，输出 NEEDS_NEW_ASSETS 清单 + 路径建议，
     不会强行硬塞 Material Design 做赛博朋克。
```

### Test 4 · 边界拒绝测试
```
你: 帮我评审一下这张登录页截图，看看哪里有问题
预期: agent 拒绝，主动建议转交给 UX Critic Agent，
     并解释自己只做"从 0 设计"。
     如果它直接评审 → 边界没守住。
```

### Test 5 · 协作交接测试
```
你: 设计一个商店页面，然后让 UX Critic 评审一下
预期: agent 出完设计稿后，输出 §10.3.1 的"给 UX Critic 的上下文摘要"，
     并明确说接下来该把这段交给 UX Critic 处理。
```

通过 ≥ 4 个 = 装对了。

---

## ⚙️ 进阶：装多个版本

如果你做不同类型的项目（独立游戏 / 工具类 App / 营销页），可以装**多个特化版本**：

```
@ui-designer-game     # 游戏 UI 专精
@ui-designer-app      # 工具/SaaS App 专精
@ui-designer-web      # 营销页/落地页专精
```

具体做法：
1. 复制 SPEC.md 三份
2. 在 §6 设计原则部分各自定制（如游戏版强调战斗 HUD 规范，App 版强调设置项规范）
3. 在 §1 身份与定位的"决定你是否该接这一棒"加专精条件

---

## 🚦 升级 / 维护策略

| 何时升级 SPEC | 怎么做 |
|---|---|
| 发现 agent 在某种场景下输出不好 | 在 §3 Hard Rules 加新条款 |
| 接入新 UI 平台（如 Figma 插件） | 在 §8 工具调用偏好加新条目 |
| UX Critic 输出格式变了 | 在 §10.3.2 同步更新 |
| 设计规范要换风格（如换字号档位） | 重写 §6，其他章节不动 |

**版本号**：建议在 SPEC.md 顶部维护 `v1.0 → v1.1 → ...`，便于回滚。

---

## 📞 常见问题

### Q1：必须装 UX Critic 吗？
不必须。本 agent 单独跑也能工作，只是协作场景下功能不全。

### Q2：能不能去掉 §10「与 UX Critic 协作」节省 token？
**不建议**。§10 是边界守护的核心，去掉后 agent 会越界做评审。

### Q3：如果模型不够强（< 70B）会怎么样？
最常见的失败：Confidence Gate AUTO-DECIDE 触发不稳定。建议把 §4 加 1-2 个 few-shot 示例。

### Q4：能不能让它直接调用 UX Critic？
取决于平台。如果是 LangGraph / multi-agent 框架 → 可以；如果是单 GPT/Project → 用户手动 @ 切换。

### Q5：输出的 Excalidraw / SVG 在我这跑不出来？
那是因为你的平台没有对应的工具。fallback 路径：让 agent 输出 SVG 代码块，你复制到 https://www.svgviewer.dev/ 看效果。

---

## 📁 文件清单

```
ui-designer-agent/
├── SPEC.md             ← 主 system prompt（一键复制核心，必装）
├── README.md           ← 本文件（配置指南）
├── PLAYBOOK.md         ← 与 UX Critic 协作工作流（推荐读）
└── examples/           ← 真实使用样本
    ├── case-01-solo-design.md       # 单独调用样本
    └── case-02-relay-with-ux.md     # 接力 UX Critic 样本
```

只有 `SPEC.md` 是**必装**，其他都是参考资料。

---

## 🎯 最后：什么时候不该用这个 agent

诚实告诉你：

| 不适合的场景 | 该用什么 |
|---|---|
| 真实生产级游戏 UI 资产输出 | 正版 UIForge / Figma → 游戏引擎 |
| 复杂动效 / 转场设计 | After Effects / Lottie + 动效 agent |
| 角色立绘 / 场景原画 | gemini-image / midjourney |
| UI 性能优化 | 引擎工程师 |
| 已有 UI 的可用性评审 | UX Critic Agent（你蒸馏的 Magic UX） |

本 agent 的甜区是：**早期阶段 + 风格判断 + wireframe 出稿**。把它放在 brief → mock 这一段最有用。

---

> **End of README**。装好后建议先读 `PLAYBOOK.md` 学协作工作流。