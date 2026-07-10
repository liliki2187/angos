# 设计采纳记录分册

此目录承载从 `docs/设计采纳记录.md` 拆出的完整条目。`docs/设计采纳记录.md` 仍是唯一稳定入口，用来做总索引、跨分类检索保护和新增条目的路由。

## 防漏检规则

1. 不要只按文件名判断该读哪个分册；先看总索引的 cross-read tags 和“跨分类检索保护”。
2. 任务同时包含玩法、UI、视觉、流程时，必须读取所有相关分册。分类用于减少噪音，不用于截断上下文。
3. 做 UI / 原型 / 截图任务时，默认先读 `ui-ux-decisions.md`；如果包含骰子、派遣、达标率、黑骰、任务类型或资源流，补读 `core-mechanics.md`；如果涉及 PNG、生图、像素、半调、纸质、地图底图或视觉包装，补读 `art-direction-decisions.md`。
4. 做机制 / 数值 / 规则任务时，默认先读 `core-mechanics.md`；如果玩家会在界面上操作或理解该机制，补读 `ui-ux-decisions.md`；如果机制需要视觉隐喻或资产表达，补读 `art-direction-decisions.md`。
5. 不确定分类时，用 `rg` 同时搜总索引与分册，例如：`rg -n "骰|dice|派遣|dispatch|美术|视觉|assetized-ui" docs/设计采纳记录.md docs/design-decisions`。

## 分册

| 分册 | 主要内容 |
|------|----------|
| `core-mechanics.md` | 核心机制、任务规则、角色骰、黑骰、探索与报道解释 |
| `ui-ux-decisions.md` | UI/UX、地图、派遣、骰子界面、报道板、资产化 UI |
| `art-direction-decisions.md` | 美术方向、像素 / 半调 / 印刷材质、角色风格与美术守门 |
| `process-and-research-decisions.md` | 流程、研究、subagent、采纳记录维护与跨分类检索规则 |
| `backlog-and-deferred.md` | 待定、进阶、备查机制库 |
| `_obsolete/design-decisions-archive/archive-raw-adoption-log.md` | 2026-06-15 拆分前全文归档（2026-07-08 挪入 `_obsolete/`），仅历史考证用，不作为新增写入口 |
