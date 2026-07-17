const fs = require("node:fs");
const path = require("node:path");
const { chromium } = require("playwright");

const prototypeDir = __dirname;
const repoRoot = path.resolve(prototypeDir, "..", "..", "..");
const outputDir = path.join(repoRoot, "docs", "screenshots", "2026-07-17-weekly-editorial-packaging-mock-v1");
const outputPath = path.join(outputDir, "01-weekly-editorial-packaging-mock-v1.png");
const auditPath = path.join(outputDir, "packaging-mock-audit.json");

function fileUrl(filePath) {
  return `file:///${filePath.replace(/\\/g, "/").replace(/ /g, "%20")}`;
}

function chromeExecutable() {
  const candidates = [
    process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE,
    "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
    path.join(process.env.LOCALAPPDATA || "", "Google", "Chrome", "Application", "chrome.exe"),
    "C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe",
    "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
  ].filter(Boolean);
  return candidates.find((candidate) => fs.existsSync(candidate));
}

(async () => {
  fs.mkdirSync(outputDir, { recursive: true });
  const executablePath = chromeExecutable();
  const browser = await chromium.launch({
    headless: true,
    ...(executablePath ? { executablePath } : {}),
  });
  const page = await browser.newPage({
    viewport: { width: 1920, height: 1080 },
    deviceScaleFactor: 1,
  });
  const failedRequests = [];
  page.on("requestfailed", (request) => {
    failedRequests.push({ url: request.url(), error: request.failure()?.errorText || "unknown" });
  });
  await page.goto(fileUrl(path.join(prototypeDir, "index.html")), { waitUntil: "networkidle" });
  const audit = await page.evaluate(() => {
    const rect = (selector) => {
      const node = document.querySelector(selector);
      if (!node) return null;
      const value = node.getBoundingClientRect();
      return {
        x: Math.round(value.x),
        y: Math.round(value.y),
        width: Math.round(value.width),
        height: Math.round(value.height),
        right: Math.round(value.right),
        bottom: Math.round(value.bottom),
      };
    };
    const backgroundLoaded = (selector) => {
      const node = document.querySelector(selector);
      return !!node && getComputedStyle(node).backgroundImage !== "none";
    };
    return {
      viewport: { width: innerWidth, height: innerHeight },
      app: rect(".app"),
      workspace: rect(".workspace"),
      candidateCase: rect(".candidate-case"),
      editionBoard: rect(".edition-board"),
      signoffCase: rect(".signoff-case"),
      heldCandidate: rect(".candidate-card"),
      dropTarget: rect(".drop-target"),
      previewDisabled: document.querySelector(".preview-action")?.disabled ?? null,
      sendDisabled: document.querySelector(".send-action")?.disabled ?? null,
      unknownCount: document.querySelectorAll(".check-row.unknown").length,
      riskCount: document.querySelectorAll(".check-row.risk").length,
      storyBackgroundsPresent: [
        ".candidate-image",
        ".head-slot.main .head-image",
        ".head-slot.secondary .head-image",
        ".story-card.harbor .story-thumb",
        ".story-card.roswell .story-thumb",
        ".story-card.city .story-thumb",
      ].every(backgroundLoaded),
      scroll: {
        bodyWidth: document.body.scrollWidth,
        bodyHeight: document.body.scrollHeight,
        documentWidth: document.documentElement.scrollWidth,
        documentHeight: document.documentElement.scrollHeight,
      },
    };
  });
  audit.failedRequests = failedRequests;
  audit.passed =
    audit.viewport.width === 1920 &&
    audit.viewport.height === 1080 &&
    audit.app?.width === 1920 &&
    audit.app?.height === 1080 &&
    audit.workspace?.x === 80 &&
    audit.workspace?.y === 96 &&
    audit.workspace?.width === 1760 &&
    audit.workspace?.height === 920 &&
    audit.candidateCase?.width === 320 &&
    audit.editionBoard?.width === 1040 &&
    audit.signoffCase?.width === 360 &&
    audit.dropTarget?.right <= 1920 &&
    audit.dropTarget?.bottom <= 1080 &&
    audit.previewDisabled === false &&
    audit.sendDisabled === true &&
    audit.unknownCount === 2 &&
    audit.riskCount === 1 &&
    audit.storyBackgroundsPresent === true &&
    audit.failedRequests.length === 0;
  fs.writeFileSync(auditPath, `${JSON.stringify(audit, null, 2)}\n`, "utf8");
  await page.screenshot({ path: outputPath, fullPage: false });
  console.log(outputPath);
  console.log(auditPath);
  console.log(`passed=${audit.passed}`);
  await browser.close();
  if (!audit.passed) process.exitCode = 1;
})();
