---
name: claude-to-im
description: |
  Bridge this Codex or Claude Code session to Telegram, Discord, Feishu/Lark,
  or QQ so the user can chat with the agent from their phone.
  Use for setup, start, stop, restart, status, logs, reconfigure, and
  diagnosis of the claude-to-im bridge daemon.
  Do not use for standalone bot development or direct IM platform SDK work.
argument-hint: "setup | start | stop | restart | status | logs [N] | reconfigure | doctor"
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - AskUserQuestion
  - Grep
  - Glob
---

# Claude-to-IM Bridge Skill

You are managing the claude-to-im bridge.
Project-local runtime data lives in `../.claude-to-im/` relative to this skill by default.
If `CTI_HOME` is set, use that directory instead.

Resolve `SKILL_DIR` from this file location first. If needed, fall back to `**/skills/**/claude-to-im/SKILL.md`.

## Command parsing

Map the user request to one of these subcommands:

| User intent | Subcommand |
| --- | --- |
| setup, configure, connect a channel | `setup` |
| start bridge, launch daemon | `start` |
| stop bridge | `stop` |
| restart bridge, bot is stuck, bot is not responding | `restart` |
| show status, check if running | `status` |
| show logs, tail logs | `logs` |
| change config, switch token, switch runtime | `reconfigure` |
| diagnose, broken, not receiving messages, failing | `doctor` |

Prefer `doctor` over `status` when the user reports a symptom.
Extract the optional numeric argument for `logs` and default to `50`.

Before asking the user for any platform credential, read `references/setup-guides.md` internally and only surface the exact next step they need.

## Runtime detection

- If `AskUserQuestion` is available, interactive setup is allowed.
- If `AskUserQuestion` is not available, stay non-interactive and point the user to `config.env.example`.

## Config check

Before `start`, `stop`, `restart`, `status`, `logs`, `reconfigure`, or `doctor`, verify that `CTI_HOME/config.env` exists.

- If missing in Codex, tell the user to create it from `SKILL_DIR/config.env.example` and stop.
- Do not start the daemon without config; that creates stale PID problems.

## Subcommands

### `setup`

If interactive questions are available, collect:

1. Enabled channels
2. Channel credentials
3. Runtime, working directory, model, and mode
4. Confirmation before writing config

Then:

1. Create `CTI_HOME/{data,logs,runtime,data/messages}`
2. Write `CTI_HOME/config.env`
3. Validate credentials using `references/token-validation.md`

If interactive questions are not available, show `SKILL_DIR/config.env.example` and explain the required fields briefly.

### `start`

Run the platform daemon entrypoint:

- Windows: `powershell -File "SKILL_DIR/scripts/daemon.ps1" start`
- Other platforms: `bash "SKILL_DIR/scripts/daemon.sh" start`

Show the result. If it fails, tell the user to run `doctor` or inspect logs.

### `stop`

Run:

- Windows: `powershell -File "SKILL_DIR/scripts/daemon.ps1" stop`
- Other platforms: `bash "SKILL_DIR/scripts/daemon.sh" stop`

### `restart`

Use this when the bridge is stuck, silent, or disconnected.

Run:

- Windows: `powershell -File "SKILL_DIR/scripts/daemon.ps1" restart`
- Other platforms: `bash "SKILL_DIR/scripts/daemon.sh" restart`

After restarting, also run:

1. `status`
2. `logs 50`

Report:

- whether restart succeeded
- the new PID if present
- any immediate startup error from recent logs

### `status`

Run:

- Windows: `powershell -File "SKILL_DIR/scripts/daemon.ps1" status`
- Other platforms: `bash "SKILL_DIR/scripts/daemon.sh" status`

### `logs`

Run:

- Windows: `powershell -File "SKILL_DIR/scripts/daemon.ps1" logs N`
- Other platforms: `bash "SKILL_DIR/scripts/daemon.sh" logs N`

### `reconfigure`

1. Read current config from `CTI_HOME/config.env`
2. Show current values with secrets masked
3. Ask what should change
4. Update config atomically
5. Re-validate changed credentials
6. Remind the user to restart the bridge

### `doctor`

Run:

- `bash "SKILL_DIR/scripts/doctor.sh"`

Then summarize findings and point to `references/troubleshooting.md` for next actions.

Common fixes:

- `npm install` if dependencies are missing
- `npm run build` if `dist/daemon.mjs` is stale
- `restart` if the process is stuck but still running
- `setup` if config is missing

## Notes

- Always mask secrets in user-visible output.
- Always prefer the scripted daemon entrypoints over ad hoc `node dist/daemon.mjs`.
- On Windows, the bridge may run either as a service or a background process; let `daemon.ps1` decide.
- Config persists in `CTI_HOME/config.env`.
