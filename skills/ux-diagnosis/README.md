# UX 诊断技能部署说明

本目录是 Angus 项目的 `@UX老哥` Codex 入口，不直接采用新版 portable 包的 `adapters/codex/AGENTS.md`。

## 当前结构

- `SKILL.md`：Codex 技能入口，负责触发词、读取顺序、项目真源和输出边界。
- `system-prompt-v2.2.md`：完整 UX 诊断主 spec，来源于 portable 包的 `core/system-prompt.md`。
- `../../.codex/agents/ux-laoge.toml`：Codex Desktop custom subagent 壳，负责让父级 Codex 能通过 `spawn_agent(agent_type="ux_laoge")` 调用。

## 为什么不用 adapters/codex/AGENTS.md 覆盖项目根

新版 portable 包的 `adapters/codex/AGENTS.md` 适合独立 Codex CLI 项目；Angus 项目根 `AGENTS.md` 还承载 GDD 真源、截图交付、本地技能优先级、文档落盘语言等项目规则。直接覆盖会让 UX 诊断规则压过项目协作规则。

本项目采用的方案是：

1. 使用 portable 包的 `core/system-prompt.md` 作为平台无关主 spec。
2. 保留 `.codex/agents/ux-laoge.toml` 作为 Codex Desktop subagent 执行壳。
3. 保留 `../ux-kb-*` 的 `SKILL.md` 结构，确保项目本地技能仍能被发现和读取。

## 家里 Codex 验证对白

在另一台电脑拉取仓库后，进入仓库根目录并新开 Codex 会话，先发这句：

```text
@ux老哥 自检一下：不要做诊断，只确认你是否是 ux_laoge 子 agent，能否读取 skills/ux-diagnosis/system-prompt-v2.2.md 和 skills/ux-kb-*/SKILL.md。请说明是否为无缝子 agent 模式。
```

判断结果：

- 如果出现 `subagent_notification`，或回复明确说自己是 `ux_laoge`，并能读取 `system-prompt-v2.2.md` 与 `ux-kb-*`，就是无缝接入。
- 如果没有子 agent 通知，但能按 `skills/ux-diagnosis/SKILL.md` 在当前线程执行，就是 fallback 模式：能力可用，但不是独立 UX 老哥子 agent。
- 如果文件不存在，说明仓库没有拉全或提交没有包含相关文件。

如果不能无缝接入，让家里 Codex 执行这段指引：

```text
请检查当前仓库是否存在 .codex/agents/ux-laoge.toml、skills/ux-diagnosis/system-prompt-v2.2.md 和 skills/ux-kb-*/SKILL.md。
如果文件齐全但 @ux老哥 没有触发子 agent，请重新从仓库根目录打开一个新 Codex 会话，确认 Codex 环境支持项目级 .codex/agents custom subagent。
如果当前环境不支持 custom subagent，请按 AGENTS.md 的 fallback 规则读取 skills/ux-diagnosis/SKILL.md，并在当前线程执行同等 UX 诊断。
```
