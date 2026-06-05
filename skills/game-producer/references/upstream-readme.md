# Game Producer Agent · 一键复制配置指南

> **30 秒部署**：打开 `SPEC.md` → 全选复制 → 粘贴到目标 AI 平台的 system prompt 字段 → 保存 → 开始用。

---

## 🚀 各平台配置方式

| 平台 | 粘贴位置 | 备注 |
|------|---------|------|
| ChatGPT GPT | Configure → Instructions | 建议开启 Web Browsing（让它搜竞品数据） |
| Claude Project | Custom Instructions | 推荐：把 examples/ 一起上传到 Knowledge |
| Cursor | `.cursor/rules/game-producer.mdc` | 加 frontmatter `alwaysApply: false` |
| Cowork | `.opencode-config/agents/game-producer.md` | 加 frontmatter（见下方） |
| Dify / Coze | Pre-Prompt | 模型选 Claude/GPT-4o |
| LangChain API | system message | 直接读文件内容 |

### Cowork frontmatter 模板

```yaml
---
description: >-
  极其严苛的游戏项目把关人，负责立项评估、创意验证、商业化设计和风险分析
mode: subagent
color: "#DC2626"
---
```

---

## 🎭 三 Agent 协作体系

本 agent 是你独立游戏工作流中的**最上游决策者**。完整体系：

```
@game-producer     → 立项评估 / 创意验证 / 竞品分析 / 风险扫描
     ↓ GREENLIT
@ui-designer       → 从 brief 出 UI 设计方案 / wireframe / mock
     ↓
@ux-critic         → 评审已有 UI / 认知负荷 / 可用性诊断
```

### 什么时候 @ 谁

| 你想做的事 | @ 谁 |
|-----------|------|
| "我有个游戏点子想验证" | @game-producer |
| "分析一下竞品 X" | @game-producer |
| "这个方向做不做得起来" | @game-producer |
| "帮我设计登录页 / 商店页" | @ui-designer |
| "这个界面好不好用" | @ux-critic |
| "做了 3 个月了方向对不对" | @game-producer |

### 协作禁令

- ❌ 不让 game-producer 做具体 UI 设计（那是 ui-designer 的事）
- ❌ 不让 game-producer 评审界面可用性（那是 ux-critic 的事）
- ❌ 不在 game-producer 过关前就进入 ui-designer 阶段（先验证再设计）
- ✅ 唯一例外：竞品分析中涉及的 UI 层面观察，game-producer 可以评论（但深入评审请转 ux-critic）

---

## 🧪 安装后自检（3 个测试）

### Test 1 · 魔鬼代言人触发
```
你: 我想做一个开放世界生存游戏
预期: 立即攻击 — 质疑差异化 + 给出竞品数据 + 提 2 个方向
不预期: "好主意！加油！"
```

### Test 2 · 快速失败触发
```
你: 我一个人想做 3A 开放世界 MMORPG
预期: 立即触发 🛑 熔断 — 成本不可控 + 建议缩小范围
不预期: 默默开始帮你规划里程碑
```

### Test 3 · 完整性熔断
```
你: 帮我设计装备强化系统
预期: 拒绝 — "核心循环都没定，先补全核心文档"
不预期: 直接开始设计强化系统
```

通过 3/3 = 装对了。

---

## 💡 使用技巧

### 1. 喂竞品时给名字就行
```
"分析一下 Slay the Spire 和 Balatro"
→ Producer 会自己搜索信息（如有搜索工具）或基于知识库分析
```

### 2. 被骂了别急着反驳，先想想
Producer 的致命质疑 90% 是对的。如果你能用证据反驳 → 说明你想清楚了；如果反驳不了 → 说明确实有问题。

### 3. 定期拉回来做"里程碑回顾"
每做 1 个月拉 Producer 回来问一次："我的 scope 膨胀了没？核心循环还在吗？"

### 4. 配合搜索工具效果翻倍
如果你的 LLM 平台支持 Web Browsing / Google Search → 强烈建议开启。Producer 的"市场佐证"环节**需要真实数据**，有搜索工具时准确度提升 50%+。

---

## 📁 文件清单

```
game-producer-agent/
├── SPEC.md             ← 主 system prompt（一键复制，必装）
├── README.md           ← 本文件
└── examples/
    └── case-01-greenlight.md   ← 完整立项评估样本
```

---

## ⚠️ 诚实提醒

本 agent 的核心能力是**判断和评估**，不是创造。它能告诉你"该不该做"和"风险在哪"，但不能替你做游戏。

如果你只是想要鼓励和肯定 → 任何普通 ChatGPT 对话都能给你。
如果你想要真相 → 用这个。
