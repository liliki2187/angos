# 世界地图 Dossier 正交组件校正板 v1｜交付清单

## 结论

本轮完成一张 `1920×1080` 的“美术 + 合同混合校正板”，用于回答：右侧 Dossier 视觉上由多张编辑纸件构成时，运行时是否必须拆成大量组件。

答案是：不需要。当前推荐结构为：

```text
BackDecor（NO-HIT，可轻倾）
+ BaseFrontCarrierSkin（静态无字壳，视觉纸件合批）
+ 69:44 Photo（独立内容）
+ DynamicText（独立）
+ optional ExpandedPreviewSkin（展开态覆盖，NO-HIT）
+ Disclosure Control（HIT 1）
+ CTA Control（HIT 2）
```

UX 老哥与 UI Designer 均判 `CONDITIONAL PASS / 可直接交用户解释落地复杂度`。本板不是切图母版、atlas、manifest、Godot 或 runtime 证据。

## Router Card

- 任务类型：资产化 UI 前的组件解释 / 美术与合同混合校正板。
- 风险等级：`risky / experimental`。
- 当前产物类型：`interaction_fix_sketch + visual_style_reference + problem_overlay`。
- 本轮只验证：视觉多纸件能否收束为少量运行时层；collapsed / expanded 状态、69:44、0°、hit 与合同冲突能否同板说明。
- 本轮不验证：真实切片、透明 clean sprite、atlas、manifest、Godot 节点、真实字体、runtime screenshot。
- 必调链：现有 UI 改进先由 `ux_laoge` 定合同边界，再由 `ui_designer` 出板面规格；生成后按同一顺序复审。
- 美术例外：clean-low-poly weekly 支线不调用旧像素 / 半调坐标系美术指导。

## 输入真值

- 正向美术标杆：
  - `design/art-direction/references/clean-lowpoly-weekly-branch/benchmark-board-01.png`
  - `design/art-direction/references/clean-lowpoly-weekly-branch/benchmark-board-02.png`
- 开放编辑材料融合参考：
  - `image_gen/2026-08-19/world-map-open-editorial-material-fusion-v1/02-open-editorial-material-fusion-imagegen-native.png`
- frozen 合同：
  - `design/ui-contracts/world-map/right_dossier_page.json`
  - `design/ui-contracts/world-map/right_mission_intel_button.json`

## 交付物

### 主审板

- `image_gen/2026-08-19/world-map-dossier-orthogonal-component-board-v1/05-dossier-orthogonal-component-correction-board-1920x1080.png`
- 分辨率：`1920×1080`
- SHA256：`0238FFBE285EB790265B8DEEC6DB28B4B1BC5E70D07DA37E2CA18177C6AA7E9A`

### 生图来源

- 原始混合板：
  - `02-imagegen-native-art-board.png`
  - `1672×941`
  - SHA256：`6158BD7F6B2603425F056BEB6A99EFBAB4786BDD10BD6D38DDB4A2C4E524313A`
- 两行连续索引纸修订：
  - `03-imagegen-continuous-two-row-art-board.png`
  - `1672×941`
  - SHA256：`1C455EC66DB77EB2035CCCD5CEFF15A2A5885134EB3146E7345B045E33F7E370`
- prompt：
  - `01-imagegen-prompt.md`
- 生成方式：Codex 内置真实 ImageGen；不是 SVG / Canvas / HTML / Pillow 生图。

### 精确标注层

- `04-annotate-component-board.py`
- 只负责：中文 mock、P3 分层说明、P4 exact slot / hit overlay、69:44 映射、0°意图标记、合同冲突与阶段边界。
- 不负责生成纸张、文件夹、照片、材质或接触阴影。

### 被拒绝的局部编辑

- `06-rejected-targeted-edit-lost-headline-body.png`
- SHA256：`6711314091296ACAA9F3EF7826080E9D82ADC9E569920F799052231B32D44244`
- 目标是把 CTA 收回 parent 并修正 Disclosure / preview 顺序；结果同时删除 headline / body 承载面，超出允许 ROI，按 `scope_invariant` 拒绝，不覆盖主审板。

## 板上冻结表达

- parent：`468×1032`；export scale `2`。
- source photo：`1104×704 = 69:44`。
- runtime photo：`414×264 = 69:44`。
- export photo：`828×528 = 69:44`。
- collapsed：无任务预览，Disclosure 使用 `＋`。
- expanded：只显示两条只读预览，显示 `已显示 2 / 共 4 条` 与 `－`。
- 只有 Disclosure 和 CTA 有 hit。
- FrontCarrier 全部为 `0°`；只允许 NO-HIT BackDecor 轻倾。
- 北美故事便签不进入通用 BaseSkin。

## 公开边界

### P1 / P2 美术预览

只用于证明：

- 开放钴蓝编辑稿夹身份；
- 多纸件视觉可以保留；
- collapsed / expanded 的状态差异；
- CTA 是唯一强动作。

它们不用于证明 exact slot。P1 / P2 中 CTA 视觉外置、expanded 的压缩顺序不能作为切片或接线依据。

### P4 几何真值

板上已经醒目标注：

> P1 / P2 只验证美术与状态关系；exact 顺序、父子关系、切片与接线一律以 P4 为准。

P4 表达当前 frozen slot、唯一两个 hit、69:44、FrontCarrier 0° 与 contract-note conflict。

## 合同冲突

`right_dossier_page` 对 expanded 两条预览的主承载位存在两种说明：`region_body inner` 与 `expanded_body_capacity`。本板临时采用当前 slot 更明确的：

`expanded_body_capacity = [27,640,414,248]`

并只显示两条只读预览。这不是永久修改；正式无字资产化前必须由合同 owner 裁决并同步真源。

## 双审结果

### UX 老哥

- 总判定：`CONDITIONAL PASS`。
- 可以回答“视觉分体、运行时合批”和落地复杂度。
- P4 / 底部合同层基本准确；P1 / P2 只应视为美术关系。
- P0：`0`。
- 剩余 P1：P1/P2 与 exact 顺序不一致；CTA 预览中外置；合同 owner 冲突未解。
- 剩余 P2：两条任务行端部短杠略有假交互；P3 比例为示意；P4 未打印完整 rect 数值表。

### UI Designer

- 总判定：`CONDITIONAL PASS`。
- 代码结构复杂度低至中，美术切片复杂度中，状态和交互复杂度低。
- 标杆氛围 Gate：`PASS`。
- 板上醒目标出 `P4 = GEOMETRY TRUTH` 后，足以交用户判断分层逻辑。
- 进入切图前仍须按 P4 重建正交无字资产，不能直接从 P1 / P2 截图。

## 当前状态

`dossier_component_layering_explanation_ready_pending_user_direction`

## 下一步

先由用户判断是否接受：

> 视觉上保留多张编辑材料；运行时收束为一个静态 BaseSkin、一个 optional ExpandedPreviewSkin、独立照片 / 文字和两个交互控件。

用户确认后，仍先裁决 `region_body / expanded_body_capacity` 合同冲突，再决定是否制作真正的正交无字 asset master。不得从本板直接进入 atlas、manifest、Godot 或 `WeeklyRunGame`。
