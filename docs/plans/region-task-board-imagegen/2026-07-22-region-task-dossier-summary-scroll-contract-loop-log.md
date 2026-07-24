# 区域任务 dossier 摘要滚动合同冲突 Loop Log

## 结论

UX 在 dossier 资产化预检中发现：正式合同规定 `summary_scroll=false`，当前 Godot 实现却设置 `_dossier_summary.scroll_active=true`。该 P1 已在美术生产前关闭，避免后续母版围绕错误交互建立。

## 原因

- 现有运行骨架早期为了容纳长摘要临时启用了 RichTextLabel 内滚动；
- 后续 dossier 合同已明确改为固定 7–8 行、压力态最多 9 行，超出时走完整摘要层；
- 实现没有随合同更新，既有测试只检查正文与 CTA 不重叠，没有断言滚动属性。

## 修正

- `_dossier_summary.scroll_active` 改为 `false`；
- 增加 `is_dossier_summary_scroll_enabled()` 测试接口；
- `test_region_task_board_v2.gd` 新增无内滚断言；
- Godot 4.6.3 可见 OpenGL 回归通过，既有 7 / 8 / 9 行摘要与 CTA 合同继续通过。

## 防错 Gate

资产化 UI 开始生图前，必须先比较正式合同与当前运行属性；发现状态、滚动、溢出、命中或布局所有权不一致时，先统一实现再生成美术，不允许用美术母版掩盖交互冲突。
