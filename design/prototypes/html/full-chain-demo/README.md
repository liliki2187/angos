# Full-Chain Demo Reference

这里保存的是从 `upstream-angos` 同步进来的网页参考原型，作为当前 Angus 主仓库的补充设计资产。
这一目录现在也是仓库内全链条网页 Demo 的唯一源码位置；打包脚本与 Pages 工作流都从这里取源。

## 文件说明

- `world-mysteries-full-chain.html`
  - 可直接打开的完整单文件 Demo，串联探索、骰子判定、组版与结算。
- `world-mysteries-full-chain-head.htm`
  - 全链条 Demo 的静态 HTML 外壳。
- `world-mysteries-full-chain.js`
  - 全链条 Demo 的逻辑脚本源码。
- `world-mysteries-explore-dice.html`
  - 独立的探索 + 骰子判定 Demo。

## 使用原则

- 这些文件是“参考实现”，不是当前 Godot 原型的主入口。
- 当前仓库默认网页入口仍是 `../prototype-hub.html`。
- `Assets/` 子目录只服务于这套网页原型，不再占用 Godot 运行时 `Assets/`。
- `source/avatars/` 保存头像裁图源图；导出的网页头像在 `Assets/avatars/`。
- 如果后续要吸收其中某一段交互或公式，优先把规则沉淀回 `design/gdd/`；更细的分析或模板再落到 `design/systems/`，而不是直接让多个原型分叉演进。
