# Git 上传与分享说明

> 这份文档只用于“新建一个外部仓库或镜像并首次上传”的场景。
> 日常协作、推送规则、双远程镜像约定请只看 `docs/onboarding/git-collaboration.md`。

## 适用场景

- 你要新建一个全新的 GitHub 仓库来承载当前内容
- 你要额外建一个只读镜像或临时分享仓

## 首次推送模板

在仓库根目录执行，并把仓库地址替换成你的目标地址：

```powershell
git init
git add .
git commit -m "chore: initial import"
git branch -M main
git remote add origin https://github.com/<your-account>/<your-repo>.git
git push -u origin main
```

## 分享给别人时发什么

- 只读浏览：仓库主页 HTTPS 地址
- 本地继续开发：`.git` 结尾的 clone 地址

## 重要提醒

- 如果你是在 Angus 现有协作仓上继续工作，不要只参考这份文档决定推送方式。
- 先运行 `git remote -v`，再对照 `docs/onboarding/git-collaboration.md`。
