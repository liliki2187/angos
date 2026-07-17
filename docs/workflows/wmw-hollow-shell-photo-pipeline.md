# WMW 含图片槽镂空框照片产线

> 适用范围：世界地图 WMW 左侧地区卡，以及后续所有“图片内容 + 状态框体 + 运行时文字”的组件类。
> 当前版本：2026-07-13 · B2.12 meta carrier 退役版：继承 B2.10 对称内芯与全部分层资产，按 A184 同步删除可见纸条、合同 `meta_line` 与运行时 meta 节点；原足迹重建为连续状态底板。

## 一、核心结论

WMW 含图片槽组件不再从压平成品图里裁照片、补边或擦边。正式结构为：

```text
底层：地区照片，普通矩形，cover 铺满窗口外接矩形
上层：镂空框体，负责右缘、下缘、badge 外环、纸签和卡体边界
覆盖元素：地球徽章等压在照片上的元素必须独立贴片，位于镂空框体之上
运行时：中文 title Label + 状态语义图标
```

照片不负责任何不规则边界；所有边界只由上层镂空框体 alpha 定义。

## 二、一类一母版

- 每个组件 class 只选一个几何最干净的母版。本轮 `left_region_card` 选 `available` 帧。
- 只对母版实测照片窗口与地球圆盘，并做一次纯几何挖窗。
- `selected / warning / locked` 不再各自挖窗，全部从母版派生。
- 状态与实例变体只允许通过程序派生：框色家族换色、badge 内芯随框色家族换色、selected 绿光晕叠加；状态语义图标不进入 atlas，由运行时层绘制。
- 风格稿允许同类尺寸差异；生产链第一步必须重建母版到合同几何，此后母版是唯一几何真源。

## 三、施工步骤

1. 读取候选 B 原始 atlas。
2. 以 `available` 帧作为母版，按自适应样本分类实测窗口矩形与地球圆盘。
3. 对母版做边缘残留扫描：沿窗口四边外侧扫描旧照片签名，最多外扩 8px；最终四边残留必须为 0。
4. 对母版做纯几何挖窗：最终窗口矩形整块置透明，禁止地球保护区或条件挖窗。
5. 从母版提取地球徽章暖色线条贴片，作为独立覆盖元素置于最上层，不保留旧照片像素。
6. 从 396 原始四场景的实测纯内容矩形裁四张普通地区照片；裁源必须完全位于源照片内部、位于源地球 bbox 右侧、止于源框内侧，并过 `photo_ingredient_overlay_contamination`。禁止从 B1.3 / 428 等压平 atlas 回采；按母版窗口矩形 cover 铺底，不做形状裁切。
7. 从母版派生四状态：
   - `available` 使用母版；
   - `selected / warning / locked` 对框色家族像素做色相 / 明度映射；
   - 先把 badge 拆成“合格结构外框”和“可替换语义内芯”。候选 B approved 外环 bbox 为 `[288,201,376,291]`、中心 `(332,246)`、1x 右 gutter `16px`，必须逐像素保留；仅重建与外环交集为 `0` 的 `CORE_MASK=[302,216,362,277]`；
   - A174 已显式把合同 `action_badge` 修订为 `[144,101,44,44]`。合同、候选 B 外环与运行时图标共享中心 `(332,246)`；合同与标杆冲突时必须停下裁决，不得盲从旧槽或自行改合同；
   - A176 禁止在退役足迹或外露底板上使用 inpaint、模糊、扩散或程序色带。程序重建掩膜不得触碰 approved 外环、阴影或相邻右框；`retired_footprint_texture_continuity` 必须证明内芯外变化 `0px`、右侧走廊变化 `0px`、外露修补像素 `0px`；
   - A178 要求中性内芯的低多边形分面从 `CORE_MASK.getbbox()` 与共享中心参数化生成：上 / 右 / 下 / 左依次使用 bbox 四边完整端点汇聚中心，左右同明度、上 `+3 RGB`、下 `-3 RGB`；禁止独立手写端点和逐像素周期噪点；
   - badge 底盘内芯属于框色家族，必须进入状态色映射与 `badge_state_color_consistency` gate；atlas 内禁止任何状态字形、暗色圆弧、靶心阴影或其它旧状态语义残影；
   - 空 badge 底盘必须先单独出放大证据并通过 `badge_clean_base_no_semantic_residue`，才允许叠 runtime icon；
   - 勾 / 靶心 / 警示三角 / 锁在候选 B 的宽搜索区先提取完整源形状，再等比装入 `44x44` 透明 PNG；最小 padding `4px`、border touch `0`，过 `runtime_icon_shape_completeness`、`ingredient_purity` 与 400% 证据后冻结，由 Python / Godot 运行时绘制进 `action_badge` 槽；
   - selected 从原 B selected 帧提取绿光晕，只给 selected 叠加；
   - 非 selected 执行全帧绿残留清理。
8. 合成顺序固定为：透明底 -> 矩形照片 -> 派生镂空框体 -> selected 光晕 -> 独立地球贴片。
9. A184 起左卡退役 meta carrier：合同中不得保留 `meta_line` 或零尺寸死槽，atlas 不得保留空纸条，Python / Godot 不得创建 meta Label。以单一 `available` 母版重建完整下层面板，再派生四状态；旧纸条及其边缘、阴影都不得作为纹理源，也不得用局部矩形覆盖、inpaint、模糊、扩散或纯色带隐藏。
10. 拼 2x atlas，跑 Python 回填、Godot windowed 截图与 manifest；运行时只绘制地区标题 Label 与状态图标。风险、目标、推荐、解锁缺口、进入代价和主 CTA 统一由右侧 dossier 承载。

当前脚本：

- `scripts/ui-contracts/wmw/wmw_v0918_left_card_b212_meta_retirement_pipeline.py`
- `gd_project/tests/capture_world_map_wmw_left_card_runtime_v09.gd`
- `scripts/run_wmw_godot_capture_v09.ps1`

## 四、冻结 Gate

本规程的 gate 判据执行中不得放宽。

| Gate | 判据 |
| --- | --- |
| GateA 旧图残留 | 镂空母版挖窗核心区不透明像素 = 0 |
| old_content_leftover_scan | 壳层与覆盖元素贴片在完整窗口范围内旧照片签名 = 0 |
| window_edge_residue_scan | 窗口四边旧照片签名扫描，外扩后 top / right / bottom / left 均 = 0 |
| GateB 边框完整 | 窗口外 3px 环带内，母版原本不透明的像素仍不透明 |
| GateC 窗口 alpha | 合成后母版窗口矩形内 alpha 全部为 255 |
| GateD 绿残留 | 非 selected 全帧绿签名像素 = 0；selected 免检 |
| badge_state_color_consistency | badge 内芯与框色家族用多像素 hue / 明度采样比较；atlas 烘焙状态字形像素必须为 0 |
| state_badge_contract_and_style_alignment | 1x 合同 `[144,101,44,44]` / 2x `[288,202,376,290]`；approved 候选 B 外环 bbox `[288,201,376,291]`、语义内芯 bbox `[302,216,362,277]`；标杆 / 合同中心 `(332,246)`；到真实右框视觉 gutter `>=16px`，Python / Godot 复用同一中心 |
| retired_footprint_texture_continuity | `harmonic_inpaint=false`、`blur_or_diffusion=false`；approved 外环保留 `100%`；语义内芯外变化、右侧走廊变化、最终外露修补像素均为 `0`。禁止把“旧像素已消失”当成纹理连续性通过 |
| badge_core_facet_symmetry | 内芯分面由同一 bbox / 中心生成；端点镜像误差 `<=1px@2x`、中心误差 `<=0.5px`、左右面积差 `<=1%`、结构镜像 IoU `>=0.985`；结构与颗粒分开验，空底盘与运行态分别贴 400% / 真实截图 |
| text_carrier_capacity | 仅适用于仍保留的文字载体：可见 carrier 完整包住合同槽；正常与最长文案无换行 / 裁切 / 自动压缩，class 四边留白阈值通过；扩槽纹理无拉伸、硬缝、涂抹或纯色色带；目标引擎真实字体与缩放截图通过 |
| retired_carrier_absence | 载体退役必须同步删除合同槽、运行时节点和可见 carrier；原足迹纸张像素与 alpha 洞均为 0，完整底板至少跨 3 个显式低多边形分面，最大单分面占比 `<=45%`，非周期颗粒覆盖率 `>=7.5%`，旧矩形边界无接缝；重建区外、标题和 badge 保护像素变化均为 0 |
| badge_clean_base_no_semantic_residue | 旧 badge 足迹原样像素复用 = 0、内芯奶油语义像素 = 0、源状态字形复制 = 0；未叠 runtime icon 的四状态空底盘另出 400% 证据，不能由最终合成图或 `atlas_baked_state_glyph_pixels=0` 替代 |
| ingredient_purity | 地球贴片与 runtime badge icon 配料的非目标色族像素必须为 0，并附 400% 证据 |
| runtime_icon_shape_completeness | 完整源 bbox 从宽搜索区提取；目标画布 `44x44`，四边 padding `>=4px`，border touch `0`；禁止按 action_badge 源坐标裁取 |
| photo_ingredient_overlay_contamination | 照片来自 396 实测纯场景矩形；bbox 在源照片内且位于源地球右侧；边缘浅色长直框线 `<=24px`、色键绿 `0`；压平 atlas 来源直接失败 |
| GateE 同类窗口 | 四状态均使用同一母版窗口，diff = 0 |
| GateF 几何比例 | 四帧均为 408x320，比例 1.275 不回退 |
| 人工目检 | 四状态 × 地球弧下 / 窗口右缘 / 窗口下缘 / badge 区域，逐点记录；执行自检只能写 `evidence_ready`，最终 PASS/FAIL 归复核方 / 用户 |
| Godot 截图 | windowed/opengl3 真实截图非黑，颜色多样性正常，运行时文字正常 |

## 五、失败处理

- 若母版量测失败：停止，上报量测截图，不改 gate。
- 若派生状态色或材质明显劣于原 B 帧：停止，贴对比板等待用户裁决。
- 若出现新缺陷类型：当轮写入 gate 或人工目检清单，不允许继续补丁绕过。
- 覆盖元素不得用保护区豁免挖窗；必须贴片化并接受旧图签名扫描。
- badge 不得按源帧坐标贴矩形槽位；状态语义图标不得烘焙或贴换进 atlas，只能作为运行时透明 PNG 配料绘制。
- 源 badge 含状态语义时，必须先判断结构外框是否已通过标杆复核。外框合格则逐像素保留，只重建与外框零交集的语义内芯；外框不合格才整区退役。禁止用 inpaint、模糊、扩散、色带、扩大覆盖或移动新组件去遮退役足迹。B2.6 证明减法清理会自证错误，B2.7 证明合同内部对齐也可能违背标杆，B2.8 证明“旧像素消失”不等于替代纹理合格。
- badge 内芯采样范围必须覆盖整个 action badge 内的非奶油色 / 非语义绿像素；不得只采中央小块导致边缘内底漏换色。
- `old_content_leftover_scan` 等颜色签名扫描必须在状态换色前执行；换色后只能用结构性对比与配料纯度 gate。
- 禁止调用 imagegen、禁止执行方擅自修改 `design/ui-contracts/world-map/` frozen 字段、禁止批量生产其它 class、禁止对照片做形状 / 圆弧 / mask 裁切。用户明确裁决的合同修订必须登记设计采纳、升合同版本并重跑全链。

## 六、B2.12 当前证据与历史失败对照

> B2.12 程序链、合同校验与 Godot windowed 截图已完成；当前只写 `evidence_ready_pending_user_visual_review`，不是冻结生产资源。

- B2.11 / B2.12 四状态与载体退役对照：`docs/screenshots/2026-06-24-world-map-benchmark-landing/549-world-map-wmw-v0-9-18-left-card-b2-12-meta-retirement-compare.png`
- 单母版干净底板与退役足迹近照：`docs/screenshots/2026-06-24-world-map-benchmark-landing/550-world-map-wmw-v0-9-18-left-card-b2-12-clean-substrate-qa.png`
- 四状态 × 退役足迹 / 标题接缝 / badge / 整卡证据板：`docs/screenshots/2026-06-24-world-map-benchmark-landing/555-world-map-wmw-v0-9-18-left-card-b2-12-16point-visual-qa.png`
- manifest：`docs/screenshots/2026-06-24-world-map-benchmark-landing/556-world-map-wmw-v0-9-18-left-card-b2-12-manifest.json`
- Godot 截图：`docs/screenshots/2026-06-24-world-map-benchmark-landing/557-world-map-wmw-v0-9-18-left-card-b2-12-godot-single-component.png`

### B2.11 历史基线

> A179 / B2.11 已验证“载体与槽位同步扩展”的技术链，但用户视觉复核否决了小条这一信息架构。其证据保留为已完成但未采纳的实验，不再作为当前生产候选。

- carrier 对照：`docs/screenshots/2026-06-24-world-map-benchmark-landing/539-world-map-wmw-v0-9-17-left-card-b2-11-meta-carrier-compare.png`
- manifest：`docs/screenshots/2026-06-24-world-map-benchmark-landing/546-world-map-wmw-v0-9-17-left-card-b2-11-manifest.json`
- Godot 截图：`docs/screenshots/2026-06-24-world-map-benchmark-landing/547-world-map-wmw-v0-9-17-left-card-b2-11-godot-single-component.png`

### B2.10 历史基线

> B2.10 的对称内芯、approved 外环与运行时图标继续作为 B2.12 的已验证输入；其 meta 纸条已由 A184 / B2.12 显式退役。

- 对称内芯对照：`docs/screenshots/2026-06-24-world-map-benchmark-landing/529-world-map-wmw-v0-9-16-left-card-b2-10-symmetric-core-compare.png`
- manifest：`docs/screenshots/2026-06-24-world-map-benchmark-landing/536-world-map-wmw-v0-9-16-left-card-b2-10-manifest.json`

### B2.9 失败对照

> B2.9 的无涂抹结构 gate 仍有效，但中性内芯四块色面使用不成对端点，形成明显歪 X；以下产物只作失败证据。

- 无涂抹对照：`docs/screenshots/2026-06-24-world-map-benchmark-landing/519-world-map-wmw-v0-9-15-left-card-b2-9-no-inpaint-compare.png`
- manifest：`docs/screenshots/2026-06-24-world-map-benchmark-landing/526-world-map-wmw-v0-9-15-left-card-b2-9-manifest.json`
- Loop Log：`docs/plans/world-map-benchmark-landing/2026-07-10-world-map-wmw-left-card-b2-9-core-facet-symmetry-loop-log.md`

### B2.8 失败对照

> B2.8 因旧 badge 足迹的 harmonic inpaint 有 `399px` 在新底盘右侧裸露而降级；以下产物只作失败证据。

- 标杆 / B2.7 / B2.8 状态徽章位置对照：`docs/screenshots/2026-06-24-world-map-benchmark-landing/509-world-map-wmw-v0-9-14-left-card-b2-8-style-position-compare.png`
- 纯照片 / 完整字形 / 地球线稿 / 空底盘配料证据：`docs/screenshots/2026-06-24-world-map-benchmark-landing/510-world-map-wmw-v0-9-14-left-card-b2-8-clean-ingredients-qa.png`
- 16 点证据板：`docs/screenshots/2026-06-24-world-map-benchmark-landing/515-world-map-wmw-v0-9-14-left-card-b2-8-16point-visual-qa.png`
- manifest：`docs/screenshots/2026-06-24-world-map-benchmark-landing/516-world-map-wmw-v0-9-14-left-card-b2-8-manifest.json`
- Godot 截图：`docs/screenshots/2026-06-24-world-map-benchmark-landing/517-world-map-wmw-v0-9-14-left-card-b2-8-godot-single-component.png`

### B2.7 失败对照

> B2.7 因状态徽章比标杆向右偏约 11px、源字形被旧合同边界截断、照片从 428 压平 atlas 回采旧地球月牙而降级；其程序 gate 只作历史证据。

- 合同对齐评审：`docs/plans/world-map-benchmark-landing/2026-07-10-world-map-wmw-left-card-b2-7-contract-aligned-badge-review.md`
- Godot 截图：`docs/screenshots/2026-06-24-world-map-benchmark-landing/507-world-map-wmw-v0-9-13-left-card-b2-7-godot-single-component.png`

### B2.6 失败对照

> 复核结论：B2.6 已因 selected badge 底盘旧靶心暗色残影降级为失败；以下产物只作为错误案例与下一轮对照，不是生产候选。

- 派生对比板：`docs/screenshots/2026-06-24-world-map-benchmark-landing/489-world-map-wmw-v0-9-12-left-card-b2-6-runtime-badge-compare.png`
- 配料纯度证据板：`docs/screenshots/2026-06-24-world-map-benchmark-landing/490-world-map-wmw-v0-9-12-left-card-b2-6-ingredients-purity-qa.png`
- 16 点目检证据板：`docs/screenshots/2026-06-24-world-map-benchmark-landing/495-world-map-wmw-v0-9-12-left-card-b2-6-16point-visual-qa.png`
- manifest：`docs/screenshots/2026-06-24-world-map-benchmark-landing/496-world-map-wmw-v0-9-12-left-card-b2-6-manifest.json`
- Godot 截图：`docs/screenshots/2026-06-24-world-map-benchmark-landing/497-world-map-wmw-v0-9-12-left-card-b2-6-godot-single-component.png`
- Godot QA：`docs/screenshots/2026-06-24-world-map-benchmark-landing/498-world-map-wmw-v0-9-12-left-card-b2-6-godot-single-component-qa.png`
