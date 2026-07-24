# 发刊编辑正式黑白结构稿 v4：筛选 / 排序交付清单

## 结论

本轮已把用户采纳的“无名称搜索、按报道类型筛选、按等级或获得时间排序”落入 `formal_ui_structure_wireframe_v4`。自动审计全部通过；它仍是功能、交互和布局结构稿，不是最终视觉包装或 Godot 正式界面。

## 交付物

- 可运行页面：`docs/prototypes/weekly-editorial-formal-black-structure-v4/index.html`
- 使用说明：`docs/prototypes/weekly-editorial-formal-black-structure-v4/README.md`
- 默认获得时间新到旧：`docs/screenshots/2026-07-20-weekly-editorial-formal-black-structure-v4-filter-sort/01-default-acquired-new-to-old.png`
- 类型多选筛选：`docs/screenshots/2026-07-20-weekly-editorial-formal-black-structure-v4-filter-sort/02-filter-deep-and-breaking.png`
- 等级高到低排序：`docs/screenshots/2026-07-20-weekly-editorial-formal-black-structure-v4-filter-sort/03-sort-quality-high-to-low.png`
- 真实点击动态演示：`docs/screenshots/2026-07-20-weekly-editorial-formal-black-structure-v4-filter-sort/04-filter-sort-interaction-demo.webp`
- 机器审计：`docs/screenshots/2026-07-20-weekly-editorial-formal-black-structure-v4-filter-sort/audit.json`

## 本轮证明范围

- 名称搜索入口、输入态与检索逻辑均不存在；左栏只保留一个筛选入口和一个排序入口。
- 筛选提供全部、抢先快讯、深度报道、个人专栏、爆炸性新闻；具体类型可多选，空结果可一键恢复全部。
- 排序提供等级高到低 / 低到高、获得时间新到旧 / 旧到新；获得时间由 `acquired_order` 提供真值，不借稿件 ID 或数组下标冒充。
- 8 条候选全部完整可见；12 条候选只在左栏滚动，中间双页与右栏几何不变。
- 筛选隐藏当前已选稿时保留来源与 6 个合法目标，并提供“显示并定位”；再次修改筛选后结束临时显示。
- 筛选 / 排序不触发推演重算；执行真实替换后选中、合法目标、悬停和换稿按钮归零，进入正在重算，两个左栏工具与送印 CTA 锁定。
- 确认状态仍保留两张完整报纸、固定签发区和唯一“确认送印”按钮。
- 浏览器控制台错误 / 警告为 `0`。

## 自动审计结果

- 共 `18` 项检查，`18/18` 通过。
- 三张静态证据均为 `1920×1080`。
- 动态演示为 `1280×720` animated WebP，共 `11` 帧；画面全部来自真实页面点击状态，程序只负责缩放与封装。

## 不能声称

- 不能称为最终 UI、最终美术包装或生产视觉真源。
- 不能称为 Godot 已接入；`acquired_order` 尚未进入正式候选稿生成与存档链。
- 不能据此提前升版 `candidate_card` 或 `signoff_panel` 组件合同。
- 不能据此裁决“版面不完整是否硬阻断”的 GDD 歧义。

## 用户需要裁决

- 是否冻结 v4 左栏的功能结构：无搜索、两个 `44×44` 工具入口、五项类型筛选、四项排序和已选稿隐藏保护。
- 若冻结，下一阶段才进入正式视觉包装；Godot 与组件合同仍需单独授权。
