#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";

const IMAGE_EXTENSIONS = new Set([".png", ".jpg", ".jpeg", ".webp"]);

function fail(message, code = 1) {
  console.error(message);
  process.exit(code);
}

function walk(dir, out) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      walk(fullPath, out);
      continue;
    }
    if (!entry.isFile()) continue;
    if (!IMAGE_EXTENSIONS.has(path.extname(entry.name).toLowerCase())) continue;
    const stat = fs.statSync(fullPath);
    out.push({
      path: fullPath,
      name: entry.name,
      bytes: stat.size,
      modified_at: stat.mtime.toISOString(),
    });
  }
}

function main() {
  const targetDir = path.resolve(process.argv[2] || "");
  if (!targetDir) {
    fail("Usage: node rank_art_references.mjs <directory>");
  }
  if (!fs.existsSync(targetDir) || !fs.statSync(targetDir).isDirectory()) {
    fail(`Directory not found: ${targetDir}`);
  }

  const images = [];
  walk(targetDir, images);
  images.sort((a, b) => a.name.localeCompare(b.name, "en"));
  console.log(JSON.stringify({
    directory: targetDir,
    image_count: images.length,
    images,
  }, null, 2));
}

main();
