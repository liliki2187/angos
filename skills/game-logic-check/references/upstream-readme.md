# Game Logic Check Agent · 配置指南

> **30 秒部署**：打开 `SPEC.md` → 全选复制 → 粘贴到目标 AI 平台的 system prompt → 保存 → 开始用。

---

## 🚀 配置方式

| 平台 | 粘贴位置 |
|------|---------|
| ChatGPT GPT | Configure → Instructions |
| Claude Project | Custom Instructions |
| Cursor | `.cursor/rules/game-logic-check.mdc` |
| Cowork | `.opencode-config/agents/game-logic-check.md` |
| Dify / Coze | Pre-Prompt |

---

## 🎭 在 Agent 体系中的位置

```
@game-producer     → 立项验证
@game-numerical    → 数值配表        ──┐
@game-narrative    → 剧情/对白       ──┤── 提交审查
@game-sys-design   → 系统规则        ──┘
                                       ↓
                          @game-logic-check    ← 本 Agent
                                       ↓
                            PASS / FAIL 报告
                                       ↓
                          FATAL → 打回原作者
```

### 什么时候用

```
✅ 用：写完一套系统规则/数值表/剧情时间线后，提交给它"体检"
✅ 用：两个系统互锁时，检查有没有冲突
✅ 用：写了 10+ 期叙事内容后，检查有没有前后矛盾
❌ 不用：设计阶段（先设计完再审）
❌ 不用：创意验证（那是 producer 的事）
```

---

## 🧪 安装后自检（2 个测试）

### Test 1 · 黑客思维触发
```
你: 我有一个签到系统，每日首次登录给 100 金币
预期: 立即追问"服务端是否验证时间戳？并发请求怎么处理？跨天零点瞬间呢？"
不预期: "好的，这个设计没问题"
```

### Test 2 · 精准报告格式
```
你: 检查这个规则："好感度 < -5 触发禁令"
预期: 输出标准 YAML 验证报告（含 ID/严重度/维度/位置/描述/影响/修复方向）
不预期: 只说"这个可能有边界问题"
```

---

## 📁 文件清单

```
game-logic-check-agent/
├── SPEC.md             ← 主 system prompt（必装）
├── README.md           ← 本文件
└── examples/
    └── case-01-faction-system.md   ← 势力系统审查样本
```

---

## ⚠️ 使用提醒

1. **它不会帮你设计** — 只审查，给修复方向但不替你改
2. **FATAL = 不可上线** — 它说 FATAL 就真的要停下来修
3. **叙事矛盾它也管** — "前后剧情矛盾"在它眼里跟"刷钱漏洞"一样是 bug
4. **等内容够了再用** — 刚开始设计时不需要，写了 10+ 条规则/期内容后再提交审查
