# 将本仓库上传到 Git 并分享链接

> 本机需已安装 **Git**（[Git for Windows](https://git-scm.com/download/win)）。若未安装，请先安装并重启终端。

---

## 1. 在 GitHub 上新建空仓库（网页操作）

1. 登录 [GitHub](https://github.com)，右上角 **+** → **New repository**。  
2. **Repository name** 填例如：`angos`（可自定）。  
3. 选 **Public**（方便分享链接）。  
4. **不要**勾选「Add a README」等（本地已有文件时避免冲突）。  
5. 点 **Create repository**。

创建完成后，页面会显示仓库地址，形如：

- **HTTPS（推荐）**：`https://github.com/你的用户名/angos.git`  
- **网页浏览**（可分享给他人或另一段对话）：`https://github.com/你的用户名/angos`

把 **你的用户名** 和 **仓库名** 换成实际值即可。

---

## 2. 在本机首次推送（PowerShell）

在 **`d:\angos`** 目录下执行（按顺序替换 `你的用户名` 与仓库名）：

```powershell
cd d:\angos
git init
git add .
git commit -m "chore: initial commit — 世界未解之谜周刊全链条 Demo 与文档"
git branch -M main
git remote add origin https://github.com/你的用户名/angos.git
git push -u origin main
```

首次 `git push` 时 GitHub 会要求登录：可用 **Personal Access Token**（HTTPS）或 **SSH 密钥**（若已配置 `git@github.com:...`）。

---

## 3. 可分享给「另一对话」的内容

复制下面两类信息即可（把占位符改成你的真实地址）：

| 用途 | 示例 |
|------|------|
| **给人看的仓库主页** | `https://github.com/你的用户名/angos` |
| **给 Cursor / 克隆用** | `https://github.com/你的用户名/angos.git` |

在 Cursor 新对话里可以写：

> 请打开仓库 `https://github.com/你的用户名/angos`（或克隆到本地后打开文件夹），继续改 `world-mysteries-full-chain.html` / `docs/` 下的文档。

若对方只需只读浏览，发 **仓库主页 HTTPS 链接** 即可；若要在本地继续开发，发 **`.git` 结尾的 clone 地址** 或 **GitHub 主页上的绿色 Code 按钮** 里的链接。

---

## 4. 以后更新代码

```powershell
cd d:\angos
git add .
git commit -m "描述本次修改"
git push
```

---

## 5. 无法用命令行时（可选）

在 GitHub 仓库页使用 **Upload files** 可上传少量文件，但不适合长期维护；仍建议安装 Git 后使用命令行推送。
