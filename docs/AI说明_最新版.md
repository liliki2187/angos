# 《世界未解之谜周刊》项目交接说明（给另一端 AI）

> 更新时间：2026-03-23  
> 目标：让另一端 AI 快速接手最新原型与文档，不重复摸索。

---

## 1) 可直接访问链接

- 可玩网页（GitHub Pages）：`https://liliki2187.github.io/angos/`
- 代码仓库（GitHub）：`https://github.com/liliki2187/angos`
- **同步仓（须与上者 `main` 一致）**：`https://github.com/daydreamerguan/angus` — 远程名一般为 `daydreamer`；推送时请 **`git push origin main` 与 `git push daydreamer main` 都做**，或运行根目录 `sync-both-remotes.ps1`。详见 `docs/Cursor对话交接指引_研发无缝衔接.md` 第 2 节。

---

## 2) 当前原型主入口（本地）

- `world-mysteries-full-chain.html`（最终可玩单文件，已合并）
- 源码拆分：
  - `world-mysteries-full-chain-head.htm`（HTML + CSS + DOM骨架）
  - `world-mysteries-full-chain.js`（全部逻辑）

说明：

- 开发时优先改 `head.htm` / `js`，然后再合并生成 `html`。
- 当前流程为：**探索 -> 故事合成台 -> 报刊组版 -> 结算 -> 下一周**。

---

## 3) 本次新增的关键内容

## 3.1 新增文档（重点）

- `docs/故事合成与报道编写系统设计文档.md`

文档内容包括：

- 现象牌 / 情报牌 / 认知牌 / 工具牌 / 报道牌体系
- 认知牌等级（假说/理论/法则/元理论）与升级链
- 四类合成公式（类型1-4）
- 报道四维属性（轰动性、可信度、神秘度、诡视度）
- 风险、污染、信誉回补机制
- 与报刊结算系统的字段映射与兼容方案

## 3.2 总览索引已更新

- `docs/世界未解之谜周刊_全链条版设计文档汇总.md`
  - 已新增“故事合成与报道编写”分册入口。

## 3.3 代码层新增玩法

在 `world-mysteries-full-chain.js` + `world-mysteries-full-chain-head.htm` 中新增：

- `phase-synthesis`（故事合成台）
- 素材仓与分类标签页
- 配方类型切换（r1~r4）
- 研究现象 -> 认知
- 执行合成（含成功率、消耗、失败、污染）
- 本周合成报道列表
- “进入组版”后优先导入合成结果到故事库

---

## 4) 主要设计文档清单（建议阅读顺序）

1. `docs/世界未解之谜周刊_全链条版设计文档汇总.md`（先看总览）
2. `docs/世界未解之谜周刊_探索部分设计文档.md`
3. `docs/骰子判定玩法_最终版.md`
4. `docs/故事合成与报道编写系统设计文档.md`（本次核心）
5. `docs/报刊结算出版玩法设计文档.md`

---

## 5) 运行与验证

## 本地体验

1. 直接打开 `world-mysteries-full-chain.html`
2. 完整试玩一轮：
   - 探索获得线索
   - 进入故事合成台合成报道
   - 进入组版
   - 结算并进入下一周

## 合并命令（PowerShell）

```powershell
$utf8bom = New-Object System.Text.UTF8Encoding $true
$utf8 = [System.Text.UTF8Encoding]::new($false)
$head = [System.IO.File]::ReadAllText('d:\angos\world-mysteries-full-chain-head.htm', $utf8)
$js = [System.IO.File]::ReadAllText('d:\angos\world-mysteries-full-chain.js', $utf8)
$out = $head + $js + "`r`n</script>`r`n</body>`r`n</html>`r`n"
[System.IO.File]::WriteAllText('d:\angos\world-mysteries-full-chain.html', $out, $utf8bom)
```

---

## 6) 当前可继续深化的方向（建议）

- 把认知等级链从“轻量数值”升级为“严格配方树”
- 将四维属性更深接入结算（不仅映射 quality/tags/negatives）
- 增加合成失败的可视化反馈与恢复机制（降低挫败）
- 增加“诡视度 -> 高层注视事件”的跨周事件联动

---

## 7) 给下一端 AI 的任务指令模板（可直接复制）

```text
请接手 d:\angos 的最新《世界未解之谜周刊》全链条原型。
先阅读：
1) docs/世界未解之谜周刊_全链条版设计文档汇总.md
2) docs/故事合成与报道编写系统设计文档.md
3) world-mysteries-full-chain-head.htm
4) world-mysteries-full-chain.js

当前已实现流程：探索 -> 故事合成台 -> 组版 -> 结算。
请在不破坏现有流程的前提下继续迭代（优先做：认知等级严格升级链 + 合成配方树可视化）。
修改后请重新合并生成 world-mysteries-full-chain.html 并给出体验说明。
```

