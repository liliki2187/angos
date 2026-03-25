# Cursor 新对话 · 研发无缝衔接指引

> 用途：在 Cursor 新开对话时，把本文整体粘贴给 AI，或让 AI 先读本文件再继续开发。  
> 工作区路径（本机）：`d:\angos`  
> 最后更新：以仓库 `git log -1` 为准。

---

## 1. 项目是什么

《世界未解之谜周刊》相关原型与文档：**网页全链条 Demo** + **Godot 4.3 原型** 已合并到同一仓库。

- **可玩网页（全链条）**：根目录 `world-mysteries-full-chain.html`（由 `world-mysteries-full-chain-head.htm` + `world-mysteries-full-chain.js` 合并生成）。
- **独立骰子动画实验页**：`dice-animation-lab.html`（调参验证用，与主干逻辑解耦）。
- **报刊结算独立原型**：`index.html`。
- **Godot**：`project.godot`、`scenes/`、`scripts/` 等（来自 `daydreamerguan/angus` 历史合并）。

---

## 2. Git：日常只需本人仓库（必读）

**协作约定（现行）**：每日研发成果 **只提交并推送到本人主仓** 即可，**不再做双远程双同步**。

| 项目 | 说明 |
|------|------|
| **规范远程** | `origin` → `https://github.com/liliki2187/angos.git`（本人 angos 仓库） |
| **日常操作** | 本地 `commit` 后 `git push origin <分支>`（一般为 `main`） |
| **克隆/拉取** | 以 `origin` 对应 URL 为准即可 |

**历史说明**：仓库曾合并 `daydreamerguan/angus` 历史，本地 `git remote` 里可能仍留有 `daydreamer` 等名称；**日常开发不必再向这些远程推送**。根目录下的 `sync-both-remotes.ps1` 为历史脚本，**非当前工作流必需**，需要时自行判断是否删除或仅作存档。

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
| `4fab604` / `67bea62` | 曾用于双远程推送的脚本（**现行流程已不再要求双推**） |

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

## 6. 当前玩法流程（主干网页）

`world-mysteries-full-chain.html` 内大致顺序：

1. 探索（地图点位、区域节点地图、split 检定）  
2. **故事合成台**（现象/情报/认知/工具、四类配方）  
3. 报刊组版与结算  
4. 下一周  

回合开始有 **条件随机事件**（无选项 / 多选项）；探索结算在 **骰子模式** 下会先切到结果页再播动画（六面轮播：`✓` 绿、`×` 红、`?` 蓝、三空白为真空白）。

---

## 7. 本地未提交项（新对话注意）

- `bootstrap-angus.ps1` 可能显示为已修改（多为行尾/未暂存），**提交前请 `git diff` 确认是否应纳入**。

---

## 8. 给新对话 AI 的一键开场模板（复制即用）

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
骰子实验页：dice-animation-lab.html

当前 HEAD 以 git log -1 为准。请在我说明的具体任务上继续，不要擅自大范围重构。
```

---

## 9. 建议的下一步（可选，按产品优先级）

- 若 `origin` 推送仍受 Secret Scanning 影响：清理历史中的密钥或按规范处理，保证日常 `push` 顺畅。  
- 将 `dice-animation-lab.html` 中的可调参数（面权重、间隔）以最小方式暴露到主干设置里。  
- 故事合成与 Godot 全链条计划的文档对齐（见 `design/`、`docs/plans/`）。

---

**全文完。**
