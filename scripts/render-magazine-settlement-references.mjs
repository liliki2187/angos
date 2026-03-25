import fs from "node:fs/promises";
import path from "node:path";
import { execFile } from "node:child_process";
import { promisify } from "node:util";

const repoRoot = process.cwd();
const referenceDir = path.join(
  repoRoot,
  "design",
  "generated-settlement-reference",
  "2026-03-18"
);
const sourceFile = path.join(referenceDir, "magazine-settlement-reference.html");
const outputDir = path.join(referenceDir, "output");
const execFileAsync = promisify(execFile);

const variants = [
  { key: "cover_desk", file: "01-cover-desk-settlement-reference.png" },
  { key: "sealed_briefing", file: "02-sealed-briefing-settlement-reference.png" },
  { key: "faction_pressure", file: "03-faction-pressure-settlement-reference.png" },
  { key: "astral_bleed", file: "04-astral-bleed-settlement-reference.png" },
  { key: "cartography_echo", file: "05-cartography-echo-settlement-reference.png" }
];

function toFileUrl(filePath) {
  const normalized = filePath.replace(/\\/g, "/");
  return `file:///${normalized}`;
}

async function findEdgePath() {
  const candidates = [
    "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
    "C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe"
  ];

  for (const candidate of candidates) {
    try {
      await fs.access(candidate);
      return candidate;
    } catch {
      // Try next path.
    }
  }

  throw new Error("Microsoft Edge executable was not found.");
}

async function cropScreenshot(inputPath, outputPath) {
  const cropScript = [
    "from PIL import Image",
    "import sys",
    "src, dst = sys.argv[1], sys.argv[2]",
    "img = Image.open(src)",
    "img.crop((0, 0, 1600, 1000)).save(dst)",
    "img.close()"
  ].join("; ");

  await execFileAsync("python", ["-c", cropScript, inputPath, outputPath], {
    windowsHide: true,
    maxBuffer: 1024 * 1024
  });
}

async function renderAll() {
  await fs.mkdir(outputDir, { recursive: true });
  const edgePath = await findEdgePath();

  for (const variant of variants) {
    const url = `${toFileUrl(sourceFile)}?variant=${variant.key}`;
    const tempPath = path.join(outputDir, `_${variant.file}`);
    const finalPath = path.join(outputDir, variant.file);
    await execFileAsync(
      edgePath,
      [
        "--headless=new",
        "--disable-gpu",
        "--hide-scrollbars",
        "--run-all-compositor-stages-before-draw",
        "--virtual-time-budget=4000",
        "--window-size=1624,1092",
        `--screenshot=${tempPath}`,
        url
      ],
      { windowsHide: true, maxBuffer: 1024 * 1024 }
    );
    await cropScreenshot(tempPath, finalPath);
    await fs.rm(tempPath, { force: true });
    console.log(`rendered ${variant.file}`);
  }
}

renderAll().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
