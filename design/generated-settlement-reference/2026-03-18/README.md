# 2026-03-18 杂志结算页参考图

本目录产出 5 张基于项目文档生成的“杂志成刊 + 发行结算”参考图。

## 设计依据

- `README.md`
- `design/systems/editing.md`
- `design/systems/attributes.md`
- `design/systems/factions.md`
- `design/prototypes/html/ui-prototype.html`

## 5 个方向

- `01-cover-desk-settlement-reference.png`
  - 深夜编辑桌视角，强调“选稿入刊”到“发行结算”的连续体验。
- `02-sealed-briefing-settlement-reference.png`
  - 审查简报视角，强调政府禁令、守序、公信与过审反馈。
- `03-faction-pressure-settlement-reference.png`
  - 三方势力拉扯视角，强调强制任务、连携、对冲与缓冲版面。
- `04-astral-bleed-settlement-reference.png`
  - 高狂性污染视角，强调灵视、隐藏探索点与失控真相。
- `05-cartography-echo-settlement-reference.png`
  - 世界地图与针图墙视角，强调探索点解锁、区域追踪与结算后下一轮远征规划。

## 源文件

- `magazine-settlement-reference.html`
  - 单文件模板，通过 `?variant=` 切换方案。
- `scripts/render/magazine-settlement-references.mjs`
  - 使用 Playwright 批量导出 PNG。

## 导出命令

```powershell
node scripts/render/magazine-settlement-references.mjs
```
