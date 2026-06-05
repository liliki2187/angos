# Game Numerical Agent · 配置指南

> **30 秒部署**：打开 `SPEC.md` → 全选复制 → 粘贴到目标 AI 平台的 system prompt → 保存 → 开始用。
> **商业手游资料库**：`REFERENCE-COMMERCIAL.md` 是**可选加载**，只在需要时上传/追加。

---

## 🚀 配置方式

| 平台 | 必装 | 选装 |
|------|------|------|
| ChatGPT GPT | Instructions ← SPEC.md | Knowledge ← REFERENCE-COMMERCIAL.md |
| Claude Project | Custom Instructions ← SPEC.md | Project Knowledge ← REFERENCE-COMMERCIAL.md |
| Cursor | `.cursor/rules/game-numerical.mdc` ← SPEC.md | 单独文件 reference 按需 @引用 |
| Cowork | `.opencode-config/agents/game-numerical.md` | 同目录放 REFERENCE-COMMERCIAL.md |
| Dify / Coze | Pre-Prompt ← SPEC.md | 知识库上传 REFERENCE-COMMERCIAL.md |

### 两种使用模式

```
模式 A · 纯独立游戏（90% 场景）
  → 只灌入 SPEC.md，不加载商业资料库
  → Agent 专注卡牌费效比 / 难度曲线 / build 平衡

模式 B · 需要商业参考时
  → 用户说"我想参考手游的 gacha 概率设计"
  → Agent 回应："正在加载商业数值资料库..."
  → 如果平台支持动态知识检索 → 自动从 REFERENCE-COMMERCIAL.md 拉取
  → 如果不支持 → 你手动把对应章节贴进对话
```

---

## 🎭 四 Agent 协作体系

```
@game-producer     → "该不该做？方向对不对？"
     ↓ GREENLIT
@game-numerical    → "数值怎么配？平衡吗？"    ← 本 Agent
     ↓ 配表完成
@ui-designer       → "数值怎么展示给玩家？"
     ↓ UI 完成
@ux-critic         → "玩家看得懂这些数字吗？"
```

### 什么时候 @ 谁

| 你想做的事 | @ 谁 |
|-----------|------|
| "帮我定一套卡牌费效比" | @game-numerical |
| "难度曲线怎么设计" | @game-numerical |
| "这个 build 是不是太强了" | @game-numerical |
| "掉落概率怎么配" | @game-numerical |
| "这个游戏点子能不能做" | @game-producer |
| "帮我设计 HP 条的 UI" | @ui-designer |
| "玩家说数值看不懂" | @ux-critic |

---

## 🧪 安装后自检（3 个测试）

### Test 1 · 体验优先触发
```
你: 帮我配一张 3 费火球卡的伤害
预期: 先问"你希望 3 费卡给玩家什么感受？是一回合大招还是稳定输出？"
不预期: 直接说"3费=15伤害"
```

### Test 2 · 魔法数字拒绝
```
你: damage = atk * 1.5 - def * 0.8 这样行吗
预期: 指出 1.5 和 0.8 是魔法数字，要求命名为 {{OFFENSE_WEIGHT}} {{DEFENSE_WEIGHT}} 并解释体验含义
不预期: "行，没问题"
```

### Test 3 · 商业内容隔离
```
你: 帮我设计一个抽卡概率表
预期: 先确认"你是独立游戏还是 F2P 手游？"，如果是独立游戏 → 按 §6 Roguelite 掉落概率走；如果手游 → 提示加载 REFERENCE-COMMERCIAL.md
不预期: 直接给 0.6%/3%/15% 的手游 gacha 表
```

---

## 📁 文件清单

```
game-numerical-agent/
├── SPEC.md                      ← 主 system prompt（必装）
├── REFERENCE-COMMERCIAL.md      ← 商业手游资料库（选装/按需）
├── README.md                    ← 本文件
└── examples/
    ├── case-01-card-costing.md          # 卡牌费效比平衡示例
    └── case-02-difficulty-curve.md      # Roguelite 难度曲线示例
```

---

## ⚠️ 使用提醒

1. **这不是万能计算器** — 它给你的是"框架 + 参数范围 + 验证方法"，最终数值需要你在游戏里实际测试
2. **模拟验证方案需要你自己跑** — Agent 给出模拟方案（如"跑 1000 局测通关率"），但执行需要你有 Python/Excel/实际 playtest
3. **体验目标必须你来定** — Agent 不替你决定"游戏应该什么感觉"，它只负责把你的感觉翻译成数字
