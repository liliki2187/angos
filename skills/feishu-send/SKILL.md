---
name: feishu-send
description: |
  Send a one-off message from this Codex session to a Feishu/Lark chat.
  Use when the user wants to post plain text to a Feishu group, or send a
  local image with a short explanation to a Feishu chat.
  Typical triggers: "feishu-send ...", "send this to Feishu",
  "post this to a Feishu group".
  Do not use for bridge setup, inbound routing, or general Feishu app
  configuration.
---

# Feishu Send

Use this skill for direct outbound Feishu delivery. The default target is:

- Group name: `安格斯的活灵魂`
- Default `chat_id`: `oc_15ce440521d0a5ef84338b3c1a42a7a3`

## Workflow

Choose the lightest path that matches the request.

### Plain text

1. If the first token looks like a Feishu `chat_id` such as `oc_xxx`, use it as the destination and treat the remaining text as the message body.
2. Otherwise, send to the default group and treat the entire argument string as the message body.
3. If the message body is missing, ask the user for it concisely.
4. Run:

```bash
node "SKILL_DIR/scripts/send-feishu-message.mjs" [chat_id] "<text>"
```

### Local image with caption

Use this path when the user wants a local image posted with a short reason.

1. Resolve the image path to an absolute local file.
2. Prepare a short title and caption in Chinese unless the user asked for another language.
3. Run:

```bash
node "SKILL_DIR/scripts/send-feishu-image-post.mjs" [chat_id] "<image_path>" "<title>" "<caption>"
```

The script uploads the image first, then sends a Feishu `post` message with the image and caption.

## Reporting

Report only the high-signal result:

- success or failure
- target `chat_id`
- returned `message_id` if present

Never print app secrets or access tokens.

## Credential Source

The bundled scripts read Feishu credentials from `CTI_HOME/config.env`.
When `CTI_HOME` is not set, this workspace first checks `../.claude-to-im/config.env` relative to the skills directory, then falls back to `~/.claude-to-im/config.env`.

Expected keys:

- `CTI_FEISHU_APP_ID`
- `CTI_FEISHU_APP_SECRET`
- `CTI_FEISHU_DOMAIN` (optional)

If the config file is missing or incomplete, tell the user to configure the Feishu bridge first.
