#!/usr/bin/env node

import {
  fail,
  getTenantAccessToken,
  loadFeishuConfig,
  looksLikeChatId,
  sendTextMessage,
} from "./feishu-api.mjs";

function printHelp() {
  console.log("Usage: node send-feishu-message.mjs [chat_id] <text>");
  console.log("   or: node send-feishu-message.mjs --chat <chat_id> <text>");
}

async function main() {
  const args = process.argv.slice(2);
  if (args.length === 0 || args.includes("--help") || args.includes("-h")) {
    printHelp();
    process.exit(args.length === 0 ? 1 : 0);
  }

  let chatId;
  let textParts = [];

  if (args[0] === "--chat" || args[0] === "-c") {
    chatId = args[1];
    textParts = args.slice(2);
  } else if (looksLikeChatId(args[0])) {
    chatId = args[0];
    textParts = args.slice(1);
  } else {
    textParts = args;
  }

  const text = textParts.join(" ").trim();
  if (!text) {
    fail("Usage: node send-feishu-message.mjs [chat_id] <text>");
  }

  const config = loadFeishuConfig();
  const targetChatId = chatId || config.defaultChatId;
  const token = await getTenantAccessToken(config);
  const message = await sendTextMessage(config.domain, token, targetChatId, text);

  console.log(JSON.stringify({
    ok: true,
    chat_id: targetChatId,
    default_chat_name: targetChatId === config.defaultChatId ? config.defaultChatName : null,
    message_id: message?.data?.message_id || null,
  }, null, 2));
}

main().catch((error) => {
  fail(error instanceof Error ? error.message : String(error));
});
