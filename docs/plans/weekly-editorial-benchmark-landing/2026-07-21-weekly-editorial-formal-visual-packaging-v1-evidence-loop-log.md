# 发刊编辑正式视觉包装候选 v1 证据纠偏 Loop Log

## 触发

本轮内部审计发现两处会污染交付证据的问题：

1. 初版 `04-recalculating-after-replace.png` 通过 `?state=recalculating` 直接进入重算预览，却使用了“真实换稿后”的文件名。该状态保留了替换前的版面事实，不能证明 A04 / A03 已完成交易。
2. UX 必须修中新增的排序短状态在 `MutationObserver` 回调里无条件重写 `textContent`，会再次触发 `childList` 观察，形成无报错的重复回调并拖慢浏览器审计。

## 根因

- 把“状态覆盖预览”和“真实操作链证据”混成同一种 capture method。
- 视觉装饰函数没有保持幂等；对被观察节点写入相同文本也可能继续产生 DOM mutation。

## 修正

- 删除初版错误证据并使用真实点击“换稿”重捕同路径。更新后中央副头版为 A04、左栏返回 A03，选中 / 合法目标 / 悬停 / 换稿按钮全部归零，右栏进入“正在重算”。
- `audit.json` 为换稿与确认分别记录 `capture_method=real_click / real_click_from_ready`；README 明确 query 状态只能作预览。
- 排序短状态改为仅在文本实际变化时写入，恢复装饰函数幂等。

## 防复发规则

- 文件名含 `after-click / after-replace / after-confirm` 时，必须由真实点击链生成；查询参数直达图只能命名为 `state-preview`。
- 交易态截图必须同时核对来源、目标、退回候选、右栏交易记录和临时交互状态，不能只看状态标题。
- 所有 MutationObserver 装饰器必须满足“重复调用不产生新 mutation”；写文本、追加节点或改变结构前先比较当前值 / 存在性。
- 交付清单必须同时写 capture method，避免把可视状态覆盖误当交互回归。

## 结果

问题均在交付用户审核前修正，没有进入 Godot、组件合同或 GDD 真源。最终审计中的换稿事实与视觉状态一致。
