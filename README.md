# angos / 世界未解之谜周刊 Demo

单机网页 Demo（探索 → 骰子检定 → 报刊组版 → 结算），无后端依赖。

## 快速体验

- 用浏览器打开项目根目录下的 **`world-mysteries-full-chain.html`**（建议 Chrome / Edge）。
- 设计文档见 **`docs/`**，总览见 **`docs/世界未解之谜周刊_全链条版设计文档汇总.md`**。

## 其它文件

- `world-mysteries-full-chain-head.htm` + `world-mysteries-full-chain.js`：合并生成完整 HTML 的源码片段（见 `docs/GIT上传与分享说明.md` 中的合并命令）。
- `index.html`：报刊结算独立原型（与全链条不同入口）。

## Git：两个 GitHub 仓库要保持一致

本仓库约定 **`main` 同时推送到两个远程**，避免只更新一侧：

| 远程 | 仓库 |
|------|------|
| `origin` | [liliki2187/angos](https://github.com/liliki2187/angos) |
| `daydreamer` | [daydreamerguan/angus](https://github.com/daydreamerguan/angus) |

推送示例：`git push origin main` 后执行 `git push daydreamer main`，或在根目录运行 **`sync-both-remotes.ps1`**。详情见 **`docs/Cursor对话交接指引_研发无缝衔接.md`** 第 2 节。

## 编码说明

合并 HTML 时请使用 **UTF-8**；Windows 下建议输出 **UTF-8 带 BOM** 的 `world-mysteries-full-chain.html`，避免中文乱码。
