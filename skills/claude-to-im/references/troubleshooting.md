# Troubleshooting

## Bridge won't start

**Symptoms**: `/claude-to-im start` fails or daemon exits immediately.

**Steps**:

1. Run `/claude-to-im doctor` to identify the issue
2. Try a clean restart: `/claude-to-im restart`
3. Check that Node.js >= 20 is installed: `node --version`
4. Check that Claude Code CLI is available: `claude --version`
5. Verify config exists: `ls -la skills/.claude-to-im/config.env`
6. Check logs for startup errors: `/claude-to-im logs`

**Common causes**:
- Missing or invalid config.env -- run `/claude-to-im setup`
- Node.js not found or wrong version -- install Node.js >= 20
- Port or resource conflict -- check if another instance is running with `/claude-to-im status`

## Messages not received

**Symptoms**: Bot is online but doesn't respond to messages.

**Steps**:

1. Verify the bot token is valid: `/claude-to-im doctor`
2. Restart the bridge to clear stale websocket state: `/claude-to-im restart`
3. Check allowed user IDs in config -- if set, only listed users can interact
4. For Telegram: ensure you've sent `/start` to the bot first
5. For Discord: verify the bot has been invited to the server with message read permissions
6. For Feishu: confirm the app has been approved and event subscriptions are configured
7. Check logs for incoming message events: `/claude-to-im logs 200`

## Permission timeout

**Symptoms**: Claude Code session starts but times out waiting for tool approval.

**Steps**:

1. The bridge runs Claude Code in non-interactive mode; ensure your Claude Code configuration allows the necessary tools
2. Consider using `--allowedTools` in your configuration to pre-approve common tools
3. Check network connectivity if the timeout occurs during API calls

## High memory usage

**Symptoms**: The daemon process consumes increasing memory over time.

**Steps**:

1. Check current memory usage: `/claude-to-im status`
2. Restart the daemon to reset memory: `/claude-to-im restart`
3. If the issue persists, check how many concurrent sessions are active -- each Claude Code session consumes memory
4. Review logs for error loops that may cause memory leaks

## Quick recovery

**Symptoms**: The bridge is running but appears stuck, silent, or disconnected.

**Fast path**:

1. Run `/claude-to-im restart`
2. Run `/claude-to-im status`
3. If it still fails, run `/claude-to-im logs 100`
4. If the logs show startup/build/auth errors, run `/claude-to-im doctor`

## Stale PID file

**Symptoms**: Status shows "running" but the process doesn't exist, or start refuses because it thinks a daemon is already running.

The daemon management script (`daemon.sh`) handles stale PID files automatically. If you still encounter issues:

1. Run `/claude-to-im stop` -- it will clean up the stale PID file
2. If stop also fails, manually remove the PID file:
   ```bash
   rm skills/.claude-to-im/runtime/bridge.pid
   ```
3. Run `/claude-to-im start` to launch a fresh instance
