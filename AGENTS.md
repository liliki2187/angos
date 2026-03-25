## Skills

Project-local skills for Angus live in `./skills`.
Prefer these workspace copies over duplicated installs under `$CODEX_HOME/skills`.

### Available skills

- `art-reference-picker`: Review local art-reference images for the Angus project, compare them against project docs, and select the most relevant images with concrete fit reasons. Use when the user asks to analyze downloaded screenshots, pick the best references for current UI or art needs, explain project relevance, archive selected images, or send chosen images with reasons to a Feishu group. (file: `./skills/art-reference-picker/SKILL.md`)
- `claude-to-im`: Bridge this Codex or Claude Code session to Telegram, Discord, Feishu/Lark, or QQ so the user can chat with the agent from their phone. Use for setup, start, stop, restart, status, logs, reconfigure, and diagnosis of the claude-to-im bridge daemon. Do not use for standalone bot development or direct IM platform SDK work. (file: `./skills/claude-to-im/SKILL.md`)
- `feishu-send`: Send a one-off message from this Codex session to a Feishu/Lark chat. Use when the user wants to post plain text to a Feishu group, or send a local image with a short explanation to a Feishu chat. Do not use for bridge setup, inbound routing, or general Feishu app configuration. (file: `./skills/feishu-send/SKILL.md`)

### How to use skills

- If the user names one of these skills, open its `SKILL.md` and follow it.
- Resolve relative paths from the skill directory first.
- Shared bridge config, logs, and state for this workspace live in `./skills/.claude-to-im` unless `CTI_HOME` overrides it.

## 对话续用与换新会话（主动提醒）

When this chat thread is long or context is strained, **proactively suggest** the user start a **new Cursor chat** if any of the following apply:

- The user switches to a **largely unrelated** task and carrying full thread history adds noise.
- You **repeatedly misunderstand** recent decisions, file paths, or constraints that were already settled earlier in the thread.
- The user mentions **high context usage** (e.g. the corner indicator is full) or asks for a “clean slate”.
- The work ahead is a **natural milestone** (e.g. large feature merged, doc handoff) and `docs/Cursor对话交接指引_研发无缝衔接.md` would onboard a new session faster than scrolling the thread.

**How to remind (keep brief):** One short paragraph: why a new chat may help, and point to `docs/Cursor对话交接指引_研发无缝衔接.md` (and current `git` state) for handoff. Do not nag every reply—at most **once per distinct situation**, unless the user asks again.
