(() => {
  const imageByCode = {
    A01: "editorial-story-m330-last-train-v1.png",
    A02: "editorial-story-area51-breathing-sign-v1.png",
    A03: "editorial-story-harbor-tomorrow-tide-v1.png",
    A04: "editorial-story-roswell-copy-refusal-v1.png",
    A05: "editorial-story-city-hall-shadow-department-v1.png",
    A06: "editorial-story-cats-refuse-blue-phone-booth-v1.png"
  };

  const recipeByLabel = {
    "深度": "deep",
    "爆炸": "breaking",
    "快讯": "brief",
    "专栏": "column"
  };

  const sortState = {
    quality_desc: ["高", "当前按等级高到低排序"],
    quality_asc: ["低", "当前按等级低到高排序"],
    acquired_desc: ["新", "当前按获得时间新到旧排序"],
    acquired_asc: ["旧", "当前按获得时间旧到新排序"]
  };

  function assetUrl(fileName) {
    return new URL(
      `../../../gd_project/Assets/ui/angus_packaging/weekly_editorial/assetized/${fileName}`,
      location.href
    ).href;
  }

  function imageFormatFor(node) {
    return node.classList.contains("main-slot") || node.classList.contains("secondary-slot")
      ? "headliner_landscape_15_8"
      : "square";
  }

  function decorateArticleNode(node) {
    const code = node.querySelector(".candidate-id, .slot__article-id")?.textContent?.trim();
    if (!code) return;

    node.dataset.articleCode = code;
    node.dataset.imageFormat = imageFormatFor(node);
    const metaNode = node.querySelector(".candidate-meta, .slot__meta");
    const meta = metaNode?.textContent?.trim() || "";
    const recipe = Object.entries(recipeByLabel).find(([label]) => meta.startsWith(label))?.[1] || "unknown";
    node.dataset.recipe = recipe;

    if (meta.includes("金级")) node.dataset.quality = "gold";
    else if (meta.includes("银级")) node.dataset.quality = "silver";
    else if (meta.includes("铜级")) node.dataset.quality = "bronze";

    if (node.classList.contains("candidate-card") && metaNode && !metaNode.dataset.fieldLabeled) {
      metaNode.textContent = meta.replace(/\s*·\s*(\d+)$/, " · 基值 $1");
      metaNode.dataset.fieldLabeled = "true";
    }

    const imageName = imageByCode[code];
    if (imageName) {
      node.classList.add("has-story-art");
      node.dataset.assetState = "legacy-art-layout-preview";
      node.querySelector(".candidate-thumb")?.removeAttribute("title");
      node.style.setProperty("--story-image", `url("${assetUrl(imageName)}")`);
    } else {
      node.classList.remove("has-story-art");
      node.dataset.assetState = "placeholder";
      node.querySelector(".candidate-thumb")?.setAttribute("title", "占位缩略图：正式方形母图待补");
      node.style.removeProperty("--story-image");
    }
  }

  function ensureVisualWidgets() {
    const workspace = document.querySelector(".workspace");
    if (!workspace) return false;

    const filterButton = document.getElementById("candidate-filter-button");
    const sortButton = document.getElementById("candidate-sort-button");
    filterButton.title = "按报道类型筛选";
    sortButton.title = "按等级或获得时间排序";

    if (!sortButton.querySelector(".candidate-sort-state")) {
      const badge = document.createElement("span");
      badge.className = "candidate-sort-state";
      badge.setAttribute("aria-hidden", "true");
      sortButton.appendChild(badge);
    }

    const centerHeading = document.querySelector(".center-panel .panel-heading");
    if (centerHeading && !centerHeading.querySelector(".targeting-guidance")) {
      const guidance = document.createElement("span");
      guidance.className = "targeting-guidance";
      guidance.textContent = "选择角标版位替换";
      guidance.hidden = true;
      centerHeading.insertBefore(guidance, document.getElementById("clear-layout"));
    }

    if (!document.getElementById("clear-layout-confirmation")) {
      const layer = document.createElement("section");
      layer.id = "clear-layout-confirmation";
      layer.className = "clear-confirm-layer";
      layer.hidden = true;
      layer.setAttribute("role", "dialog");
      layer.setAttribute("aria-modal", "true");
      layer.setAttribute("aria-labelledby", "clear-confirm-title");
      layer.innerHTML = `
        <div class="clear-confirm-card">
          <div class="clear-confirm-kicker">破坏性操作</div>
          <h2 id="clear-confirm-title">确认清空双版？</h2>
          <p>所有已上版报道将返回候选栏，当前推演结果立即失效。</p>
          <div class="clear-confirm-actions">
            <button class="clear-confirm-cancel" type="button">继续编辑</button>
            <button class="clear-confirm-submit" type="button">确认清空</button>
          </div>
        </div>`;
      document.querySelector(".stage").appendChild(layer);

      const nativeConfirm = window.confirm.bind(window);
      const visualConfirm = (message) => {
        if (!String(message).includes("清空本期双版")) return nativeConfirm(message);
        layer.hidden = false;
        layer.querySelector(".clear-confirm-cancel").focus();
        return false;
      };
      window.confirm = visualConfirm;

      layer.querySelector(".clear-confirm-cancel").addEventListener("click", () => {
        layer.hidden = true;
        document.getElementById("clear-layout").focus();
      });
      layer.querySelector(".clear-confirm-submit").addEventListener("click", () => {
        layer.hidden = true;
        window.confirm = () => true;
        document.getElementById("clear-layout").click();
        window.confirm = visualConfirm;
      });
      document.addEventListener("keydown", (event) => {
        if (event.key === "Escape" && !layer.hidden) {
          event.preventDefault();
          layer.querySelector(".clear-confirm-cancel").click();
        }
      });
    }

    document.querySelectorAll("[data-sort-mode]").forEach((button) => {
      if (button.dataset.visualListener) return;
      button.dataset.visualListener = "true";
      button.addEventListener("click", () => queueMicrotask(decorate));
    });
    return true;
  }

  function decorate() {
    document.querySelectorAll(".candidate-card, .slot.is-occupied").forEach(decorateArticleNode);
    document.querySelectorAll(".slot:not(.is-occupied)").forEach((slot) => {
      slot.classList.remove("has-story-art");
      slot.dataset.imageFormat = slot.classList.contains("main-slot") || slot.classList.contains("secondary-slot")
        ? "headliner_landscape_15_8"
        : "square";
      slot.style.removeProperty("--story-image");
    });

    const activeSort = document.querySelector("[data-sort-mode][aria-checked='true']")?.dataset.sortMode || "acquired_desc";
    const [shortSort, sortLabel] = sortState[activeSort];
    const sortButton = document.getElementById("candidate-sort-button");
    const sortBadge = sortButton?.querySelector(".candidate-sort-state");
    if (sortBadge && sortBadge.textContent !== shortSort) sortBadge.textContent = shortSort;
    if (sortButton) sortButton.setAttribute("aria-label", `候选报道排序，${sortLabel}`);

    const selectedVisible = Boolean(document.querySelector(".candidate-card.is-selected"));
    const selectedHidden = !document.getElementById("candidate-reveal-selected")?.hidden;
    const guidance = document.querySelector(".targeting-guidance");
    if (guidance) guidance.hidden = !(selectedVisible || selectedHidden);
  }

  document.title = "发刊编辑界面｜正式视觉包装候选 v4";
  const stage = document.querySelector(".stage");
  if (stage) stage.dataset.artifact = "formal_visual_packaging_candidate_v3";

  if (!ensureVisualWidgets()) return;
  decorate();

  const workspace = document.querySelector(".workspace");
  const observer = new MutationObserver(decorate);
  observer.observe(workspace, { childList: true, subtree: true });

  window.editorialVisual = {
    getAuditState: () => window.editorialWireframe?.getAuditState(),
    showState: (name) => window.editorialWireframe?.showState(name),
    setCandidateCount: (count) => window.editorialWireframe?.setCandidateCount(count),
    clearFilters: () => window.editorialWireframe?.clearFilters(),
    get inner() { return window.editorialWireframe; }
  };
})();
