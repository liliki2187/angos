# Cursor 新对话 · 研发无缝衔接指引

> 用途：在 Cursor 新开对话时，把本文整体粘贴给 AI，或让 AI 先读本文件再继续开发。  
> 工作区路径（本机）：`d:\angos`  
> 最后更新：以仓库 `git log -1` 为准。

---

## 1. 项目是什么

《世界未解之谜周刊》相关原型与文档：**网页全链条 Demo** + **Godot 4.3 原型** 已合并到同一仓库。

- **可玩网页（全链条）**：根目录 `world-mysteries-full-chain.html`（由 `world-mysteries-full-chain-head.htm` + `world-mysteries-full-chain.js` 合并生成）。
- **功能实验索引**：`labs/index.html`（合成台拖拽、骰子动画、报刊演示入口、探索骰子独立页等）。
- **故事合成台实验页**：`labs/synth-workbench-lab.html`（与主干合成规则须保持同步，见 **§6**）。
- **独立骰子动画实验页**：`labs/dice-animation-lab.html`（调参验证用，与主干逻辑解耦）。根目录 `dice-animation-lab.html` 为重定向。
- **报刊结算独立原型**：`index.html`。
- **Godot**：`project.godot`、`scenes/`、`scripts/` 等（来自 `daydreamerguan/angus` 历史合并）。

---

## 2. Git：双远程必须一致（必读，避免误解）

**协作约定（现行）**：`origin` 与 `daydreamer` 两个仓库的 **`main` 分支应始终保持同一提交**（内容一致且为最新）。推送时 **不要只推一边**。

| 远程名 | URL | 说明 |
|--------|-----|------|
| **`origin`** | `https://github.com/liliki2187/angos.git` | 主展示仓名 **angos** |
| **`daydreamer`** | `https://github.com/daydreamerguan/angus.git` | 同名历史仓 **angus**，与上表 **同一套 `main` 历史** |

**推荐操作**（在仓库根目录）：

1. 开发在 **`main`** 上；`commit` 后先 `git pull origin main`（或 `--rebase`，团队统一一种即可），解决冲突再推送。  
2. **连续推两次**，或运行脚本一次搞定：  
   - `git push origin main`  
   - `git push daydreamer main`  
   - 或：`.\sync-both-remotes.ps1`（默认推 `main` 到上述两个远程）

若本地缺少 `daydreamer`：`git remote add daydreamer https://github.com/daydreamerguan/angus.git`

**给 AI / 新同事的一句话**：本仓库 **不是**「只维护 angos」；**任何合并进 `main` 的改动都应同步到 `origin` 与 `daydreamer`**，除非负责人明确说临时只推一侧（并记得补推）。

**若 `git push origin` 被 GitHub 拒绝（Push Protection / Secret Scanning）**

- 常见原因：历史提交里含疑似 **Personal Access Token**（例如曾出现在 `scripts/github_push.py` 等路径）。
- 处理方向：从历史中剔除或替换密钥后重写可见历史，或按 GitHub 提示走一次性放行（不推荐长期依赖）。具体以报错与团队安全规范为准。

---

## 3. 近期关键提交（理解进度用）

| 提交 | 说明 |
|------|------|
| `600c04c` | 故事合成台、回合事件、地图 UI、骰子动画等与全链条相关的大量功能 |
| `47d4925` | 交接文档文件名规范化 |
| `094c125` | 与 `daydreamer/main` 合并（无共同历史，已 `--allow-unrelated-histories`） |
| `4fab604` / `67bea62` | 与双远程相关的历史脚本提交 |
| （最新） | 现行约定：**`main` 同时推 `origin` + `daydreamer`**，见本节上文 |

---

## 4. 文档索引（新对话优先读这些）

| 路径 | 内容 |
|------|------|
| `docs/AI说明_最新版.md` | 给 AI 的仓库级交接摘要 |
| `docs/世界未解之谜周刊_全链条版设计文档汇总.md` | 全链条总览与索引 |
| `docs/故事合成与报道编写系统设计文档.md` | 故事合成正式设计 |
| `docs/报刊结算出版玩法设计文档.md` | 组版与结算公式（与 `index.html` / 全链条编辑部对齐） |
| `docs/骰子判定玩法_最终版.md` | 二项 / split 检定数学 |
| `docs/世界未解之谜周刊_探索部分设计文档.md` | 探索侧（注意与全链条 split 实现的差异说明在汇总里） |
| `docs/GIT上传与分享说明.md` | 合并 HTML 的 PowerShell 命令 |

---

## 5. 网页全链条：开发与合并命令

修改逻辑时改 **`world-mysteries-full-chain-head.htm`** 与 **`world-mysteries-full-chain.js`**，再合并生成 **`world-mysteries-full-chain.html`**（UTF-8 带 BOM 为宜，见 `docs/GIT上传与分享说明.md`）。

---

## 6. 实验页与主干同步（固定规则）

凡改动 **`world-mysteries-full-chain-head.htm`** / **`world-mysteries-full-chain.js`** 中与**故事合成**相关的内容（配方类型、情报与素材规则、槽位逻辑、一览表文案、消耗/计数规则等），**若存在对口的实验页，须同步修改该实验页**，避免实验与全链条行为不一致。

| 主干变更范围 | 须同步的实验页 | 说明 |
|--------------|----------------|------|
| 合成台配方、公开合成、一览表等 | **`labs/synth-workbench-lab.html`** | 与主干对齐；必要时同步 **`labs/index.html`** 中该实验的简介一句。 |
| 骰子动画参数/流程 | **`labs/dice-animation-lab.html`**（及根目录重定向页若仅链路） | 仅当主干骰子表现或可调参数变更时。 |
| 报刊填充演示等 | **`labs/newspaper-fill-lab.html`** 等 | 仅当对应该实验的能力变更时。 |

**无对应实验页的功能**不必强行往实验页搬运逻辑。

---

## 7. 当前玩法流程（主干网页）

`world-mysteries-full-chain.html` 内大致顺序：

1. 探索（地图点位、区域节点地图、split 检定）  
2. **故事合成台**（现象/情报/认知/工具、各定型配方；情报领域影响成稿走向）  
3. 报刊组版与结算  
4. 下一周  

回合开始有 **条件随机事件**（无选项 / 多选项）；探索结算在 **骰子模式** 下会先切到结果页再播动画（六面轮播：`✓` 绿、`×` 红、`?` 蓝、三空白为真空白）。

---

## 8. 本地未提交项（新对话注意）

- `bootstrap-angus.ps1` 可能显示为已修改（多为行尾/未暂存），**提交前请 `git diff` 确认是否应纳入**。

---

## 9. 给新对话 AI 的一键开场模板（复制即用）

```text
请接手《世界未解之谜周刊》/ Angus 合并仓库。

工作区：d:\angos（或 clone 后打开同结构仓库）

请先读：
1) docs/Cursor对话交接指引_研发无缝衔接.md
2) docs/AI说明_最新版.md
3) docs/世界未解之谜周刊_全链条版设计文档汇总.md

Git：
- 日常只推本人仓库：origin = https://github.com/liliki2187/angos.git
- 不再要求双远程同步；若 push 被 Secret Scanning 拦截，需按报错处理历史密钥等问题

主入口网页：world-mysteries-full-chain.html
骰子实验页：labs/dice-animation-lab.html

当前 HEAD 以 git log -1 为准。请在我说明的具体任务上继续，不要擅自大范围重构。
```

---

## 10. 建议的下一步（可选，按产品优先级）

- 若 `origin` 推送仍受 Secret Scanning 影响：清理历史中的密钥或按规范处理，保证日常 `push` 顺畅。  
- 将 `labs/dice-animation-lab.html` 中的可调参数（面权重、间隔）以最小方式暴露到主干设置里。  
- 故事合成与 Godot 全链条计划的文档对齐（见 `design/`、`docs/plans/`）。

---

## 11. 本指引文件的更新约定（固定规则）

1. **重大规则**：AI 或协作者若拟在本文件中**新增或改写「大条」约定**（例如：影响多文件协作流程、Git 策略、实验页同步范围、默认工作方式等），应先在对话中向负责人**汇总要点（简明列表即可）**，经负责人**明确同意**后再写入本文。
2. **小修**：修正错字、更新路径示例、与已实现代码对齐的细表述等，可在完成任务时直接修改，无需逐项报批。

---

**全文完。**
