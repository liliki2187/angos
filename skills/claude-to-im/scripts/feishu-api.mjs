#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

export const LEGACY_DEFAULT_CHAT_ID = "oc_15ce440521d0a5ef84338b3c1a42a7a3";
export const LEGACY_DEFAULT_CHAT_NAME = "Angus Feishu Group";
const SCRIPT_DIR = path.dirname(fileURLToPath(import.meta.url));
const SKILL_DIR = path.resolve(SCRIPT_DIR, "..");
const SKILLS_DIR = path.resolve(SKILL_DIR, "..");

export function fail(message, code = 1) {
  console.error(message);
  process.exit(code);
}

export function looksLikeChatId(value) {
  return /^oc_[A-Za-z0-9]+$/.test(value);
}

function stripQuotes(value) {
  if (
    (value.startsWith("\"") && value.endsWith("\"")) ||
    (value.startsWith("'") && value.endsWith("'"))
  ) {
    return value.slice(1, -1);
  }
  return value;
}

export function loadEnvFile(filePath) {
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

export function resolveConfigPath() {
  const overrideHome = process.env.CTI_HOME?.trim();
  if (overrideHome) {
    return path.join(overrideHome, "config.env");
  }

  return path.join(SKILLS_DIR, ".claude-to-im", "config.env");
}

export function loadFeishuConfig() {
  const configPath = resolveConfigPath();
  const env = loadEnvFile(configPath);
  const appId = env.get("CTI_FEISHU_APP_ID");
  const appSecret = env.get("CTI_FEISHU_APP_SECRET");
  const domain = (env.get("CTI_FEISHU_DOMAIN") || "https://open.feishu.cn").replace(/\/+$/, "");
  const defaultChatId = env.get("CTI_FEISHU_DEFAULT_CHAT_ID") || LEGACY_DEFAULT_CHAT_ID;

  if (!appId || !appSecret) {
    fail(`Missing CTI_FEISHU_APP_ID or CTI_FEISHU_APP_SECRET in ${configPath}`);
  }

  return {
    appId,
    appSecret,
    configPath,
    defaultChatId,
    defaultChatName: defaultChatId === LEGACY_DEFAULT_CHAT_ID ? LEGACY_DEFAULT_CHAT_NAME : null,
    domain,
  };
}

export async function postJson(url, body, headers = {}) {
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

export async function getTenantAccessToken(config) {
  const auth = await postJson(
    `${config.domain}/open-apis/auth/v3/tenant_access_token/internal`,
    { app_id: config.appId, app_secret: config.appSecret },
  );

  if (auth.code !== 0 || !auth.tenant_access_token) {
    fail(`Feishu auth failed: code=${auth.code} msg=${auth.msg || "unknown"}`);
  }

  return auth.tenant_access_token;
}

export async function sendTextMessage(domain, token, chatId, text) {
  const message = await postJson(
    `${domain}/open-apis/im/v1/messages?receive_id_type=chat_id`,
    {
      receive_id: chatId,
      msg_type: "text",
      content: JSON.stringify({ text }),
    },
    {
      authorization: `Bearer ${token}`,
    },
  );

  if (message.code !== 0) {
    fail(`Feishu send failed: code=${message.code} msg=${message.msg || "unknown"}`);
  }

  return message;
}

export async function uploadImage(domain, token, filePath) {
  const imageBuffer = fs.readFileSync(filePath);
  const form = new FormData();
  form.set("image_type", "message");
  form.set("image", new Blob([imageBuffer]), path.basename(filePath));

  const response = await fetch(`${domain}/open-apis/im/v1/images`, {
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
    fail(`Non-JSON response from ${domain}/open-apis/im/v1/images: HTTP ${response.status}`);
  }

  if (!response.ok) {
    fail(`HTTP ${response.status} from ${domain}/open-apis/im/v1/images: ${JSON.stringify(json)}`);
  }

  if (json.code !== 0 || !json.data?.image_key) {
    fail(`Feishu image upload failed: code=${json.code} msg=${json.msg || "unknown"}`);
  }

  return json.data.image_key;
}

export function buildImagePostContent(title, imageKeys, caption = "") {
  const content = imageKeys.map((imageKey) => [{ tag: "img", image_key: imageKey }]);
  if (caption) {
    content.push([{ tag: "text", text: caption }]);
  }
  return {
    zh_cn: {
      title,
      content,
    },
  };
}

export async function sendPostMessage(domain, token, chatId, content) {
  const message = await postJson(
    `${domain}/open-apis/im/v1/messages?receive_id_type=chat_id`,
    {
      receive_id: chatId,
      msg_type: "post",
      content: JSON.stringify(content),
    },
    {
      authorization: `Bearer ${token}`,
    },
  );

  if (message.code !== 0) {
    fail(`Feishu send failed: code=${message.code} msg=${message.msg || "unknown"}`);
  }

  return message;
}
