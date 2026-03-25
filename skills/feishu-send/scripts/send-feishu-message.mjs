#!/usr/bin/env node

import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

const DEFAULT_CHAT_ID = "oc_15ce440521d0a5ef84338b3c1a42a7a3";
const DEFAULT_CHAT_NAME = "Angus Feishu Group";
const SCRIPT_DIR = path.dirname(fileURLToPath(import.meta.url));
const SKILLS_DIR = path.resolve(SCRIPT_DIR, "..", "..");

function fail(message, code = 1) {
  console.error(message);
  process.exit(code);
}

function looksLikeChatId(value) {
  return /^oc_[A-Za-z0-9]+$/.test(value);
}

function stripQuotes(value) {
  if (
    (value.startsWith('"') && value.endsWith('"')) ||
    (value.startsWith("'") && value.endsWith("'"))
  ) {
    return value.slice(1, -1);
  }
  return value;
}

function loadEnvFile(filePath) {
  if (!fs.existsSync(filePath)) {
    fail(`Config file not found: ${filePath}`);
  }

  const out = new Map();
  const text = fs.readFileSync(filePath, "utf8");
  for (const rawLine of text.split(/\r?\n/)) {
    const line = rawLine.trim();
    if (!line || line.startsWith("#")) continue;
    const idx = line.indexOf("=");
    if (idx === -1) continue;
    const key = line.slice(0, idx).trim();
    const value = stripQuotes(line.slice(idx + 1).trim());
    out.set(key, value);
  }
  return out;
}

function resolveConfigPath() {
  const overrideHome = process.env.CTI_HOME?.trim();
  if (overrideHome) {
    return path.join(overrideHome, "config.env");
  }

  const workspaceConfig = path.join(SKILLS_DIR, ".claude-to-im", "config.env");
  if (fs.existsSync(workspaceConfig)) {
    return workspaceConfig;
  }

  return path.join(os.homedir(), ".claude-to-im", "config.env");
}

async function postJson(url, body, headers = {}) {
  const response = await fetch(url, {
    method: "POST",
    headers: {
      "content-type": "application/json",
      ...headers,
    },
    body: JSON.stringify(body),
  });

  let json;
  try {
    json = await response.json();
  } catch {
    fail(`Non-JSON response from ${url}: HTTP ${response.status}`);
  }

  if (!response.ok) {
    fail(`HTTP ${response.status} from ${url}: ${JSON.stringify(json)}`);
  }

  return json;
}

async function main() {
  const args = process.argv.slice(2);
  if (args.length === 0) {
    fail("Usage: node send-feishu-message.mjs [chatid] <text>");
  }

  let chatId = DEFAULT_CHAT_ID;
  let textParts = args;

  if (looksLikeChatId(args[0])) {
    chatId = args[0];
    textParts = args.slice(1);
  }

  const text = textParts.join(" ").trim();
  if (!text) {
    fail("Usage: node send-feishu-message.mjs [chatid] <text>");
  }

  const configPath = resolveConfigPath();
  const config = loadEnvFile(configPath);

  const appId = config.get("CTI_FEISHU_APP_ID");
  const appSecret = config.get("CTI_FEISHU_APP_SECRET");
  const domain = (config.get("CTI_FEISHU_DOMAIN") || "https://open.feishu.cn").replace(/\/+$/, "");

  if (!appId || !appSecret) {
    fail(`Missing CTI_FEISHU_APP_ID or CTI_FEISHU_APP_SECRET in ${configPath}`);
  }

  const auth = await postJson(
    `${domain}/open-apis/auth/v3/tenant_access_token/internal`,
    { app_id: appId, app_secret: appSecret },
  );

  if (auth.code !== 0 || !auth.tenant_access_token) {
    fail(`Feishu auth failed: code=${auth.code} msg=${auth.msg || "unknown"}`);
  }

  const message = await postJson(
    `${domain}/open-apis/im/v1/messages?receive_id_type=chat_id`,
    {
      receive_id: chatId,
      msg_type: "text",
      content: JSON.stringify({ text }),
    },
    {
      authorization: `Bearer ${auth.tenant_access_token}`,
    },
  );

  if (message.code !== 0) {
    fail(`Feishu send failed: code=${message.code} msg=${message.msg || "unknown"}`);
  }

  const messageId = message?.data?.message_id || null;
  console.log(JSON.stringify({
    ok: true,
    chat_id: chatId,
    default_chat_name: chatId === DEFAULT_CHAT_ID ? DEFAULT_CHAT_NAME : null,
    message_id: messageId,
  }, null, 2));
}

main().catch((error) => {
  fail(error instanceof Error ? error.message : String(error));
});
