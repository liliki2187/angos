# Game System Architect Agent · 配置指南

> **30 秒部署**：打开 `SPEC.md` → 全选复制 → 粘贴到目标 AI 平台的 system prompt → 保存 → 开始用。

---

## 🚀 配置方式

| 平台 | 粘贴位置 |
|------|---------|
| ChatGPT GPT | Configure → Instructions |
| Claude Project | Custom Instructions |
| Cursor | `.cursor/rules/game-sys-architect.mdc` |
| Cowork | `.opencode-config/agents/game-sys-architect.md` |
| Dify / Coze | Pre-Prompt |

---

## 🎭 在 Agent 体系中的位置

```
@game-producer     → "做不做？" (GREENLIT)
        ↓
@game-sys-architect → "系统怎么拆？怎么连？"  ← 本 Agent
        ↓
@game-sys-design   → "每个系统的具体规则"
@game-numerical    → "数值怎么填"
        ↓
@game-logic-check  → "有没有漏洞"
```

### 什么时候用

| 场景 | 做什么 |
|------|--------|
| "项目刚立项，需要搭架构" | Phase 1-5 完整走一遍 |
| "我想加一个新系统" | 系统注册守门（4 问审批） |
| "两个系统打架了" | 耦合度审查 + 拆分建议 |
| "感觉资源不平衡" | 资源流转图审查 |
| "项目越做越大控制不住" | 健康度 Checklist + 砍建议 |

---

## 🧪 安装后自检（2 个测试）

### Test 1 · 守门触发
```
你: 我想加一个成就系统
预期: 立即问"它服务核心循环哪一环？去掉它核心体验会消失吗？"
不预期: "好的，成就系统包含以下功能..."（直接开始设计）
```

### Test 2 · 自上而下
```
你: 帮我搭系统架构
预期: 先问"核心循环是什么？"，从循环出发拆模块
不预期: 直接列一堆系统（装备/背包/商店/公会...）
```

---

## 📁 文件清单

```
game-sys-architect-agent/
├── SPEC.md             ← 主 system prompt（必装）
├── README.md           ← 本文件
└── examples/
    └── case-01-weekly-architecture.md   ← 周刊项目架构样本
```

---

## ⚠️ 关键区分

```
它是策划架构师（关心玩家体验、系统循环、资源流转）
不是程序架构师（不关心代码结构、API、数据库）

它的产出 = 给策划和制作人看的"系统蓝图"
不是给程序员看的"技术方案"
```
