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

async function uploadImage(url, token, filePath) {
  const imageBuffer = fs.readFileSync(filePath);
  const form = new FormData();
  form.set("image_type", "message");
  form.set("image", new Blob([imageBuffer]), path.basename(filePath));

  const response = await fetch(url, {
    method: "POST",
    headers: {
      authorization: `Bearer ${token}`,
    },
    body: form,
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

  if (json.code !== 0 || !json.data?.image_key) {
    fail(`Feishu image upload failed: code=${json.code} msg=${json.msg || "unknown"}`);
  }

  return json.data.image_key;
}

async function main() {
  const args = process.argv.slice(2);
  if (args.length < 3) {
    fail("Usage: node send-feishu-image-post.mjs [chatid] <image_path> <title> <caption>");
  }

  let chatId = DEFAULT_CHAT_ID;
  let cursor = 0;
  if (looksLikeChatId(args[0])) {
    chatId = args[0];
    cursor = 1;
  }

  const imagePath = path.resolve(args[cursor] || "");
  const title = (args[cursor + 1] || "").trim();
  const caption = args.slice(cursor + 2).join(" ").trim();

  if (!imagePath || !title || !caption) {
    fail("Usage: node send-feishu-image-post.mjs [chatid] <image_path> <title> <caption>");
  }

  if (!fs.existsSync(imagePath)) {
    fail(`Image file not found: ${imagePath}`);
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

  const imageKey = await uploadImage(
    `${domain}/open-apis/im/v1/images`,
    auth.tenant_access_token,
    imagePath,
  );

  const content = {
    zh_cn: {
      title,
      content: [
        [{ tag: "img", image_key: imageKey }],
        [{ tag: "text", text: caption }],
      ],
    },
  };

  const message = await postJson(
    `${domain}/open-apis/im/v1/messages?receive_id_type=chat_id`,
    {
      receive_id: chatId,
      msg_type: "post",
      content: JSON.stringify(content),
    },
    {
      authorization: `Bearer ${auth.tenant_access_token}`,
    },
  );

  if (message.code !== 0) {
    fail(`Feishu send failed: code=${message.code} msg=${message.msg || "unknown"}`);
  }

  console.log(JSON.stringify({
    ok: true,
    chat_id: chatId,
    default_chat_name: chatId === DEFAULT_CHAT_ID ? DEFAULT_CHAT_NAME : null,
    image_path: imagePath,
    image_key: imageKey,
    message_id: message?.data?.message_id || null,
  }, null, 2));
}

main().catch((error) => {
  fail(error instanceof Error ? error.message : String(error));
});
