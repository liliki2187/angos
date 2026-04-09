#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";

import {
  buildImagePostContent,
  fail,
  getTenantAccessToken,
  loadFeishuConfig,
  looksLikeChatId,
  sendPostMessage,
  uploadImage,
} from "./feishu-api.mjs";

const IMAGE_EXTENSIONS = new Set([".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp"]);
const MAX_IMAGES_PER_POST = 9;

function printHelp() {
  console.log("Usage: node send-feishu-images-post.mjs [chat_id] [options] <path_or_dir> [more_paths_or_dirs...]");
  console.log("Options:");
  console.log("  --chat, -c <chat_id>     Override CTI_FEISHU_DEFAULT_CHAT_ID");
  console.log("  --title, -t <title>      Post title");
  console.log("  --caption <caption>      Post caption");
  console.log("  --match, -m <substring>  Keep only files whose basename contains the substring");
  console.log("  --limit <n>              Send at most n images after filtering");
  console.log("  --recursive, -r          Walk directories recursively");
  console.log("  --separate, -s           Send one post per image");
}

function parsePositiveInt(value, flagName) {
  const parsed = Number.parseInt(value, 10);
  if (!Number.isFinite(parsed) || parsed <= 0) {
    fail(`Invalid value for ${flagName}: ${value}`);
  }
  return parsed;
}

function isImageFile(filePath) {
  return IMAGE_EXTENSIONS.has(path.extname(filePath).toLowerCase());
}

function normalizeSubstring(value) {
  return value.trim().toLowerCase();
}

function collectFilesFromDirectory(dirPath, recursive, collected) {
  const entries = fs.readdirSync(dirPath, { withFileTypes: true })
    .sort((left, right) => left.name.localeCompare(right.name));
  for (const entry of entries) {
    const fullPath = path.join(dirPath, entry.name);
    if (entry.isDirectory()) {
      if (recursive) {
        collectFilesFromDirectory(fullPath, true, collected);
      }
      continue;
    }
    if (entry.isFile() && isImageFile(fullPath)) {
      collected.push(fullPath);
    }
  }
}

function collectImagePaths(inputs, options) {
  const collected = [];

  for (const rawInput of inputs) {
    const resolved = path.resolve(rawInput);
    if (!fs.existsSync(resolved)) {
      fail(`Path not found: ${resolved}`);
    }

    const stat = fs.statSync(resolved);
    if (stat.isDirectory()) {
      collectFilesFromDirectory(resolved, options.recursive, collected);
      continue;
    }

    if (!stat.isFile()) {
      fail(`Unsupported path type: ${resolved}`);
    }

    if (!isImageFile(resolved)) {
      fail(`Not a supported image file: ${resolved}`);
    }
    collected.push(resolved);
  }

  const unique = [...new Set(collected.map((filePath) => path.normalize(filePath)))];
  const filtered = options.matches.length === 0
    ? unique
    : unique.filter((filePath) => {
        const baseName = path.basename(filePath).toLowerCase();
        return options.matches.every((pattern) => baseName.includes(pattern));
      });

  const limited = typeof options.limit === "number" ? filtered.slice(0, options.limit) : filtered;
  if (limited.length === 0) {
    fail("No matching image files found.");
  }

  return limited;
}

function chunkItems(items, size) {
  const chunks = [];
  for (let index = 0; index < items.length; index += size) {
    chunks.push(items.slice(index, index + size));
  }
  return chunks;
}

function buildChunkTitle(baseTitle, chunkIndex, totalChunks, fallbackTitle) {
  const title = baseTitle || fallbackTitle;
  if (totalChunks === 1) {
    return title;
  }
  return `${title} (${chunkIndex + 1}/${totalChunks})`;
}

async function main() {
  const args = process.argv.slice(2);
  if (args.length === 0 || args.includes("--help") || args.includes("-h")) {
    printHelp();
    process.exit(args.length === 0 ? 1 : 0);
  }

  const options = {
    caption: "",
    chatId: "",
    limit: undefined,
    matches: [],
    recursive: false,
    separate: false,
    title: "",
  };
  const inputs = [];

  for (let index = 0; index < args.length; index += 1) {
    const value = args[index];

    if (index === 0 && looksLikeChatId(value) && !options.chatId) {
      options.chatId = value;
      continue;
    }

    if (value === "--chat" || value === "-c") {
      options.chatId = args[index + 1] || "";
      if (!options.chatId) fail(`Missing value for ${value}`);
      index += 1;
      continue;
    }

    if (value === "--title" || value === "-t") {
      options.title = args[index + 1] || "";
      if (!options.title) fail(`Missing value for ${value}`);
      index += 1;
      continue;
    }

    if (value === "--caption") {
      options.caption = args[index + 1] || "";
      if (!options.caption) fail(`Missing value for ${value}`);
      index += 1;
      continue;
    }

    if (value === "--match" || value === "-m") {
      const pattern = normalizeSubstring(args[index + 1] || "");
      if (!pattern) fail(`Missing value for ${value}`);
      options.matches.push(pattern);
      index += 1;
      continue;
    }

    if (value === "--limit") {
      options.limit = parsePositiveInt(args[index + 1] || "", value);
      index += 1;
      continue;
    }

    if (value === "--recursive" || value === "-r") {
      options.recursive = true;
      continue;
    }

    if (value === "--separate" || value === "-s") {
      options.separate = true;
      continue;
    }

    if (value.startsWith("-")) {
      fail(`Unknown option: ${value}`);
    }

    inputs.push(value);
  }

  if (inputs.length === 0) {
    fail("Usage: node send-feishu-images-post.mjs [chat_id] [options] <path_or_dir> [more_paths_or_dirs...]");
  }

  const imagePaths = collectImagePaths(inputs, options);
  const config = loadFeishuConfig();
  const targetChatId = options.chatId || config.defaultChatId;
  const token = await getTenantAccessToken(config);
  const uploaded = [];

  for (const filePath of imagePaths) {
    const imageKey = await uploadImage(config.domain, token, filePath);
    uploaded.push({ filePath, imageKey });
  }

  const messages = [];

  if (options.separate) {
    for (const item of uploaded) {
      const title = options.title || path.basename(item.filePath);
      const content = buildImagePostContent(title, [item.imageKey], options.caption);
      const message = await sendPostMessage(config.domain, token, targetChatId, content);
      messages.push({
        image_path: item.filePath,
        message_id: message?.data?.message_id || null,
        title,
      });
    }
  } else {
    const chunks = chunkItems(uploaded, MAX_IMAGES_PER_POST);
    const fallbackTitle = uploaded.length === 1
      ? path.basename(uploaded[0].filePath)
      : "Image batch";

    for (const [chunkIndex, chunk] of chunks.entries()) {
      const title = buildChunkTitle(options.title, chunkIndex, chunks.length, fallbackTitle);
      const caption = chunkIndex === 0 ? options.caption : "";
      const content = buildImagePostContent(
        title,
        chunk.map((item) => item.imageKey),
        caption,
      );
      const message = await sendPostMessage(config.domain, token, targetChatId, content);
      messages.push({
        image_paths: chunk.map((item) => item.filePath),
        message_id: message?.data?.message_id || null,
        title,
      });
    }
  }

  console.log(JSON.stringify({
    ok: true,
    chat_id: targetChatId,
    default_chat_name: targetChatId === config.defaultChatId ? config.defaultChatName : null,
    image_count: uploaded.length,
    images: uploaded.map((item) => ({
      image_key: item.imageKey,
      image_path: item.filePath,
    })),
    message_count: messages.length,
    messages,
  }, null, 2));
}

main().catch((error) => {
  fail(error instanceof Error ? error.message : String(error));
});
