function createMetric([label, value]) {
  const box = document.createElement("div");
  box.className = "metric";
  box.innerHTML = `<div class="metric-label">${label}</div><div class="metric-value">${value}</div>`;
  return box;
}

function createTruthBar([left, value, right, legend]) {
  const wrap = document.createElement("div");
  wrap.className = "truth-bar";
  wrap.innerHTML = `
    <div class="bar-top"><span>${left}</span><span>${legend}</span><span>${right}</span></div>
    <div class="bar-track"><div class="bar-fill" style="width:${value}%"></div></div>
  `;
  return wrap;
}

function createStoryCard(entry) {
  const row = document.createElement("div");
  row.className = "story-card";
  row.innerHTML = `
    <div class="story-thumb"></div>
    <div>
      <div class="story-meta">
        <span class="tag ${entry.tag}">${entry.tag === "science" ? "科学" : entry.tag === "mystery" ? "玄学" : "世俗"}</span>
        <span class="story-level">${entry.level}</span>
      </div>
      <div class="story-title">${entry.title}</div>
      <div class="story-desc">${entry.desc}</div>
    </div>
  `;
  return row;
}

function createSlot([label, name, quality, effect, note]) {
  const row = document.createElement("div");
  row.className = "slot-card";
  row.innerHTML = `
    <div class="slot-label">${label}</div>
    <div class="slot-name">${name}</div>
    <div class="slot-foot"><span>${quality}</span><span>${effect}</span></div>
    ${note ? `<div class="slot-note">${note}</div>` : ""}
  `;
  return row;
}

function createDeltaBlock(entry) {
  const row = document.createElement("div");
  row.className = "insight-card";
  row.innerHTML = `
    <div class="insight-kicker">${entry.title}</div>
    <div class="insight-text">${entry.text}</div>
  `;
  return row;
}

function createInsight([title, text]) {
  const row = document.createElement("div");
  row.className = "insight-card";
  row.innerHTML = `
    <div class="insight-kicker">${title}</div>
    <div class="insight-text">${text}</div>
  `;
  return row;
}

function createScoreRow([label, value, tone]) {
  const row = document.createElement("div");
  row.className = "delta-row";
  row.innerHTML = `
    <span class="delta-label">${label}</span>
    <span class="delta-value ${tone}">${value}</span>
  `;
  return row;
}

function createAttribute([name, value, delta, fillClass, tone]) {
  const row = document.createElement("div");
  row.className = "attribute-row";
  row.innerHTML = `
    <span class="attribute-name">${name}</span>
    <div class="attribute-track"><div class="attribute-fill ${fillClass}" style="width:${value}%"></div></div>
    <span class="attribute-delta ${tone}">${delta}</span>
  `;
  return row;
}

function createFaction([name, status, detail]) {
  const row = document.createElement("div");
  row.className = "faction-card";
  row.innerHTML = `
    <div class="faction-head">
      <div class="faction-name">${name}</div>
      <div class="faction-status">${status}</div>
    </div>
    <div class="faction-detail">${detail}</div>
  `;
  return row;
}

function createUnlock([title, detail]) {
  const row = document.createElement("div");
  row.className = "unlock-card";
  row.innerHTML = `
    <div class="faction-name" style="font-size:17px;margin-bottom:6px">${title}</div>
    <div class="unlock-detail">${detail}</div>
  `;
  return row;
}

function renderVariant(data) {
  const artboard = document.getElementById("artboard");
  artboard.classList.add(data.cssClass);

  document.getElementById("variantTitle").textContent = data.title;
  document.getElementById("variantCode").textContent = data.code;
  document.getElementById("variantSubtitle").textContent = data.subtitle;
  document.getElementById("ambientStampA").textContent = data.ambientStampA;
  document.getElementById("ambientStampB").textContent = data.ambientStampB;
  document.getElementById("ambientGlyph").textContent = data.ambientGlyph;
  document.getElementById("coverChip").textContent = data.coverChip;
  document.getElementById("coverMark").textContent = data.coverMark;
  document.getElementById("coverLabel").textContent = data.coverLabel;
  document.getElementById("coverHeadline").textContent = data.coverHeadline;
  document.getElementById("coverDeck").textContent = data.coverDeck;
  document.getElementById("centerChip").textContent = data.centerChip;
  document.getElementById("scoreChip").textContent = data.scoreChip;
  document.getElementById("readerText").textContent = data.readerText;
  document.getElementById("nextIssueText").textContent = data.nextIssueText;
  document.getElementById("sealText").textContent = data.sealText;

  data.headerMetrics.forEach((entry) => document.getElementById("headerMetrics").appendChild(createMetric(entry)));
  data.truthBars.forEach((entry) => document.getElementById("truthBars").appendChild(createTruthBar(entry)));
  data.storyCards.forEach((entry) => document.getElementById("storyStrip").appendChild(createStoryCard(entry)));
  data.slots.forEach((entry) => document.getElementById("slotColumn").appendChild(createSlot(entry)));
  data.deltaBlocks.forEach((entry) => document.getElementById("deltaColumn").appendChild(createDeltaBlock(entry)));
  data.insights.forEach((entry) => document.getElementById("insightCluster").appendChild(createInsight(entry)));
  data.scoreRows.forEach((entry) => document.getElementById("scoreRows").appendChild(createScoreRow(entry)));
  data.attributes.forEach((entry) => document.getElementById("attributeGrid").appendChild(createAttribute(entry)));
  data.factions.forEach((entry) => document.getElementById("factionList").appendChild(createFaction(entry)));
  data.unlocks.forEach((entry) => document.getElementById("unlockList").appendChild(createUnlock(entry)));
}

const variant = new URLSearchParams(window.location.search).get("variant") || "cover_desk";
renderVariant(window.SETTLEMENT_REFERENCE_VARIANTS[variant] || window.SETTLEMENT_REFERENCE_VARIANTS.cover_desk);
window.__renderReady = true;
