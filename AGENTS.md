## Skills

Project-local skills for Angus live in `./skills`.
Prefer these workspace copies over duplicated installs under `$CODEX_HOME/skills`.

### Available skills

- `art-reference-picker`: Review local art-reference images for the Angus project, compare them against project docs, and select the most relevant images with concrete fit reasons. Use when the user asks to analyze downloaded screenshots, pick the best references for current UI or art needs, explain project relevance, archive selected images, or send chosen images with reasons to a Feishu group. (file: `./skills/art-reference-picker/SKILL.md`)
- `claude-to-im`: Bridge this Codex or Claude Code session to Telegram, Discord, Feishu/Lark, or QQ so the user can chat with the agent from their phone, and use its bundled Feishu send scripts for one-off text or image posts. Aliases/triggers: `claude to im`, `claude_to_im`, `bridge`, `start bridge`, `restart bridge`, `bridge status`, `bridge logs`, `send to feishu`, `post to feishu`. Use for setup, start, stop, restart, status, logs, reconfigure, diagnosis of the claude-to-im bridge daemon, and one-off Feishu sending from repo files. Do not use for standalone bot development or direct IM platform SDK work. (file: `./skills/claude-to-im/SKILL.md`)
- `openrouter-image-gen`: Generate, edit, or plan game-ready images through OpenRouter image models, including GPT-5 Image transparent PNG/WebP workflows and Nano Banana / Nano Banana 2 opaque workflows. Aliases/triggers: `openrouter image gen`, `openrouter 生图`, `nano banana`, `nano banana 2`, `gpt-5 image transparent`, `参考图生图`, `openrouter image`, `or image gen`. Use when the user asks for OpenRouter-based image generation, transparent asset cutouts, reference-image image editing, icons, props, textures, sprites, posters, key art, UI banners, portraits, environments, or similar visual asset generation tasks. (file: `./skills/openrouter-image-gen/SKILL.md`)
- `psd-to-godot-ui`: Convert a Photoshop PSD into a reusable Godot UI bundle for this project: copied source PSD, generated layer PNGs, flattened preview, manifest, and a `Control`-rooted `.tscn` scene that can later be instanced into gameplay scenes. Use when the user wants to import a PSD mockup, validate the PSD-to-Godot UI path, regenerate a UI scene after PSD changes, or prepare UI art for later integration. (file: `./skills/psd-to-godot-ui/SKILL.md`)
- Imported Claude Code Game Studios workflows now live as project-local Codex skills under `./skills/<skill-name>/SKILL.md`. Use them when the user names one directly or asks for the matching game-production workflow.
- Reviews and analysis: `asset-audit`, `balance-check`, `code-review`, `design-review`, `gate-check`, `perf-profile`, `project-stage-detect`, `scope-check`, `tech-debt`.
- Planning, documentation, and release: `architecture-decision`, `bug-report`, `changelog`, `estimate`, `hotfix`, `launch-checklist`, `milestone-review`, `onboard`, `patch-notes`, `release-checklist`, `retrospective`, `reverse-document`, `setup-engine`, `sprint-plan`, `start`.
- Design and preproduction: `brainstorm`, `design-system`, `localize`, `map-systems`, `playtest-report`, `prototype`.
- Team orchestration: `team-audio`, `team-combat`, `team-level`, `team-narrative`, `team-polish`, `team-release`, `team-ui`.
- Image and asset helpers: `openrouter-image-gen`, `reply-image-context`, `svg-to-png`.

### How to use skills

- If the user names one of these skills, open its `SKILL.md` and follow it.
- Treat obvious alias forms as naming the skill directly. For `claude-to-im`, this includes `claude to im`, `claude_to_im`, `bridge`, `start bridge`, `restart bridge`, `bridge status`, `bridge logs`, and similar bridge-management requests.
- Treat obvious alias forms as naming the skill directly. For `openrouter-image-gen`, this includes `openrouter image gen`, `openrouter 生图`, `openrouter image`, `or image gen`, `nano banana`, `nano banana 2`, `gpt-5 image transparent`, `透明背景生图`, `参考图生图`, and similar OpenRouter image-generation requests.
- Treat obvious alias forms as naming the skill directly. For `psd-to-godot-ui`, this includes `psd to godot ui`, `import psd`, `psd ui`, `photoshop ui import`, and similar PSD-to-Godot UI conversion requests.
- Resolve relative paths from the skill directory first.
- Imported game-studio skills use shared templates under `./skills/_game-studio-shared/templates`.
- Shared bridge config, logs, and state for this workspace live in `./skills/.claude-to-im` unless `CTI_HOME` overrides it.
