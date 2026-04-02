## Skills

Project-local skills for Angus live in `./skills`.
Prefer these workspace copies over duplicated installs under `$CODEX_HOME/skills`.

### Available skills

- `art-reference-picker`: Review local art-reference images for the Angus project, compare them against project docs, and select the most relevant images with concrete fit reasons. Use when the user asks to analyze downloaded screenshots, pick the best references for current UI or art needs, explain project relevance, archive selected images, or send chosen images with reasons to a Feishu group. (file: `./skills/art-reference-picker/SKILL.md`)
- `claude-to-im`: Bridge this Codex or Claude Code session to Telegram, Discord, Feishu/Lark, or QQ so the user can chat with the agent from their phone, and use its bundled Feishu send scripts for one-off text or image posts. Aliases/triggers: `claude to im`, `claude_to_im`, `bridge`, `start bridge`, `restart bridge`, `bridge status`, `bridge logs`, `send to feishu`, `post to feishu`. Use for setup, start, stop, restart, status, logs, reconfigure, diagnosis of the claude-to-im bridge daemon, and one-off Feishu sending from repo files. Do not use for standalone bot development or direct IM platform SDK work. (file: `./skills/claude-to-im/SKILL.md`)
- Imported Claude Code Game Studios workflows now live as project-local Codex skills under `./skills/<skill-name>/SKILL.md`. Use them when the user names one directly or asks for the matching game-production workflow.
- Reviews and analysis: `asset-audit`, `balance-check`, `code-review`, `design-review`, `gate-check`, `perf-profile`, `project-stage-detect`, `scope-check`, `tech-debt`.
- Planning, documentation, and release: `architecture-decision`, `bug-report`, `changelog`, `estimate`, `hotfix`, `launch-checklist`, `milestone-review`, `onboard`, `patch-notes`, `release-checklist`, `retrospective`, `reverse-document`, `setup-engine`, `sprint-plan`, `start`.
- Design and preproduction: `brainstorm`, `design-system`, `localize`, `map-systems`, `playtest-report`, `prototype`.
- Team orchestration: `team-audio`, `team-combat`, `team-level`, `team-narrative`, `team-polish`, `team-release`, `team-ui`.
- Image and asset helpers: `reply-image-context`, `svg-to-png`.

### How to use skills

- If the user names one of these skills, open its `SKILL.md` and follow it.
- Treat obvious alias forms as naming the skill directly. For `claude-to-im`, this includes `claude to im`, `claude_to_im`, `bridge`, `start bridge`, `restart bridge`, `bridge status`, `bridge logs`, and similar bridge-management requests.
- Resolve relative paths from the skill directory first.
- Imported game-studio skills use shared templates under `./skills/_game-studio-shared/templates`.
- Shared bridge config, logs, and state for this workspace live in `./skills/.claude-to-im` unless `CTI_HOME` overrides it.

## 对话续用与换新会话（主动提醒）

When this chat thread is long or context is strained, **proactively suggest** the user start a **new Cursor chat** if any of the following apply:

- The user switches to a **largely unrelated** task and carrying full thread history adds noise.
- You **repeatedly misunderstand** recent decisions, file paths, or constraints that were already settled earlier in the thread.
- The user mentions **high context usage** (e.g. the corner indicator is full) or asks for a “clean slate”.
- The work ahead is a **natural milestone** (e.g. large feature merged, doc handoff) and `docs/Cursor对话交接指引_研发无缝衔接.md` would onboard a new session faster than scrolling the thread.

**How to remind (keep brief):** One short paragraph: why a new chat may help, and point to `docs/Cursor对话交接指引_研发无缝衔接.md` (and current `git` state) for handoff. Do not nag every reply—at most **once per distinct situation**, unless the user asks again.
