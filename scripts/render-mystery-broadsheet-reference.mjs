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
const sourceFile = path.join(referenceDir, "mystery-broadsheet-reference.html");
const outputDir = path.join(referenceDir, "output");
const outputFile = path.join(outputDir, "06-mystery-broadsheet-reference.png");
const tempFile = path.join(outputDir, "_06-mystery-broadsheet-reference.png");
const execFileAsync = promisify(execFile);
const outputWidth = 1240;
const outputHeight = 2520;
const windowWidth = 1260;
const windowHeight = 2600;

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

async function cropScreenshot(inputPath, finalPath) {
  const cropScript = [
    "from PIL import Image",
    "import sys",
    "src, dst = sys.argv[1], sys.argv[2]",
    "img = Image.open(src)",
    `img.crop((0, 0, ${outputWidth}, ${outputHeight})).save(dst)`,
    "img.close()"
  ].join("; ");

  await execFileAsync("python", ["-c", cropScript, inputPath, finalPath], {
    windowsHide: true,
    maxBuffer: 1024 * 1024
  });
}

async function render() {
  await fs.mkdir(outputDir, { recursive: true });
  const edgePath = await findEdgePath();

  await execFileAsync(
    edgePath,
    [
      "--headless=new",
      "--disable-gpu",
      "--hide-scrollbars",
      "--run-all-compositor-stages-before-draw",
      "--virtual-time-budget=4000",
      `--window-size=${windowWidth},${windowHeight}`,
      `--screenshot=${tempFile}`,
      toFileUrl(sourceFile)
    ],
    { windowsHide: true, maxBuffer: 1024 * 1024 }
  );

  await cropScreenshot(tempFile, outputFile);
  await fs.rm(tempFile, { force: true });
  console.log(`rendered ${outputFile}`);
}

render().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
