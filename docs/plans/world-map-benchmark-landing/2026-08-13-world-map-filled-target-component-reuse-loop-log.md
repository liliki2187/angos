# 世界地图氛围方向稿误带不可复用组件 Loop Log

## 三行结论

- **结论**：`world-map-lightweight-editorial-props-v2` 的编辑部氛围与轻量叙事物方向可保留，但其 RegionCard、新闻图槽、beacon 状态族与动态内容布局不能作为组件母稿；产物降级为 `visual_atmosphere_reference / component_runtime_blocked`。
- **影响**：若直接按图拆件，会破坏一地区一张 `1104×704 / 69:44` canonical 新闻图、三卡状态切换零位移、固定 hit rect、同源数据同步与装饰层 `NO-HIT` 等已冻结合同，且可能把已删除的旧截止文案重新带回运行时。
- **下一步**：停止从整屏方向图裁组件；先用 A282 exact rect 制作统一 RegionCard 槽位、`69:44` 三尺度图槽、组合状态与输入层合同板。`340×170=2:1` 与 `86:41` 冲突关闭前，RegionCard FrontCarrier 继续阻断生产。

## Loop 记录

- **触发来源**：用户反馈。用户指出三张地区图的尺寸规格不一致，导致图片不能复用，并要求继续扫描其它功能不合理组件。
- **原始问题**：前一轮只审了轻量叙事物是否增加编辑部气氛，没有重新执行整屏组件类一致性、图片槽合同、状态切换零位移、输入层和真实数据源审计。
- **失败归因**：主命中 F1“验证等级冒充”——把保留功能内容的 ImageGen `filled_state visual target` 误当成可以继续承载组件方向的稿件；次命中 F4“只修点名局部不扫同类”——只检查新增的三处叙事物，没有回扫整屏同类组件与既有 A282 合同。
- **复发判定**：F1 已知家族再次复发，更新为 `≥33 次（2026-05-13 至 2026-08-13）`；F4 本轮作为伴随命中记录，不新增错误家族。
- **本轮处理**：当前图仅保留刊头、冷白纸 / 钴蓝背页、证据照片＋批注、轻量送稿签等媒介与氛围参考。RegionCard 三卡、左卡 / 地图证据 / Dossier 图槽、beacon 状态族、Dossier 动态槽和输入层全部不得从图中直接裁切或反推尺寸。
- **复发保护**：后续任何整屏 `filled_state visual target` 在被称为“组件方向稿、可拆母稿或下一步资产来源”前，必须逐项核对 `same_class_geometry`、`canonical_media_reuse`、`state_zero_layout_shift`、`dynamic_slot_capacity`、`input_layer_ownership` 与 `contract_source_of_truth`；任一缺证据即自动降级为氛围参考。
- **沉淀判断**：更新 A303 与 F1 复发计数；不新增 gate。现有 `component_class_contract`、`assetized_ui` blockers 和 `component_render_language_lock` 已覆盖，本轮失败在于没有执行既有放行检查。

## 审计摘要

1. **RegionCard 家族断裂**：三卡的外框、照片窗口、标题 / 状态 / 条件槽和 selected 体量不同，无法共享同一 class，状态切换会跳版并侵入相邻 hit rect。
2. **canonical 新闻图复用失败**：方向图中的左卡、地图证据照片和右 Dossier 使用不同宽高比与重新生成画面；“看起来是同一洗衣店”不等于引用同一 `resource_path`。
3. **beacon 状态族断裂**：selected 使用大 Eye 章，locked 使用另一套小锁图标；没有证明同一 `72×72` registration 和状态切图。
4. **地图证据 overlay 只覆盖北美**：尚未证明东亚 / 太平洋切换时使用同尺寸组件、预定义安全位置且不遮挡其它锚点。
5. **输入层未证明解耦**：卡片露边、夹子、背页、便签、照片和来源回条越出内容矩形；必须全部 `MOUSE_FILTER_IGNORE / FOCUS_NONE`，只有三张卡、三个 beacon、Disclosure 与 CTA 保留输入。
6. **合同真源漂移**：A282 runtime 使用 RegionCard `340×170`、Schedule `372×246`、Dossier `468×1032`，而现有旧合同 JSON 仍记录 `left_region_card 204×160 @1280`、`right_dossier_page 320×520 @1280`；RegionCard 另有 `2:1` 与 `86:41` 冲突，ISSUE 票签 exact rect 仍未冻结。
7. **旧 fixture 回流风险**：`WorldMapIntegratedDossier.gd` 仍含“最早截止：第4天”，`WorldMapIntegratedPrototype.gd` 仍含“截稿倒计时7天”，与 A296 的删除裁决不一致；本轮不修改 Godot，但后续接线前必须择一修正文档或实现。

