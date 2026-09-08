# 世界地图内部插槽压力板 v1 交付清单

> 日期：2026-08-07  
> 阶段：`independent_2x_front_carrier -> internal_slot_pressure_board`  
> 当前状态：机器验证与 UI / UX 迭代终审全部通过  
> 不包含：地区卡 / ISSUE 壳体、BackDecor、Atlas、manifest、Godot 正式回填

## 交付目的

在不重生纸材、不改变 A282 固定矩形的前提下，证明 Dossier、Schedule 与主 CTA 的正交 `FrontCarrier` 能承载真实中文、极限中文、完整地区图、collapsed / expanded 和输入状态；把“看起来像组件”推进为“能装入运行内容的候选壳”。

## 产物

评审目录：`image_gen/2026-08-07/world-map-internal-slot-pressure-v1/`

- `01-internal-slot-pressure-clean-real.png`：真实内容视觉板。
- `02-internal-slot-pressure-qa-overlay.png`：插槽 / 图片 / 热区叠加板。
- `03-internal-slot-pressure-capacity.png`：最长字段、两位数、`99+`、零日边界压力板。
- `04–10`：四张 Dossier 与三张 Schedule 原生运行时切片。
- `11-internal-slot-pressure-audit.json`：构建侧审计。
- `12-independent-slot-pressure-validation.json`：独立位图验证。
- `13-detected-glyph-safe-qa.png`：独立验证可视证据。

可复现脚本：

- `scripts/ui-contracts/wmw/build_world_map_internal_slot_pressure_board_v1.py`
- `scripts/ui-contracts/wmw/validate_world_map_internal_slot_pressure_board_v1.py`

## 固定合同

### Dossier

- 根：`468×1032`。
- Kicker `[27,24,414,24]`；标题 `[27,58,286,76]`；状态 `[325,60,116,42]`。
- 图片 `[27,150,414,264]`；标题 `[27,426,414,40]`；摘要 `[27,472,414,84]`。
- Disclosure `[27,572,414,56]`；Preview `[27,640,414,248]`；Cost `[27,898,414,22]`；CTA `[27,932,414,76]`。
- collapsed / expanded 只允许 Disclosure 与 Preview 内容变化；其它插槽逐像素不动。
- 仅 Disclosure 与 CTA 为真实热区；Preview 任务行只读。

### 图片

- 正式源：`gd_project/Assets/prototypes/world_map_integrated/a_style_v2_runtime/north_america_story_1104x704.png`。
- 运行时：`414×264`；与源图同为 `69:44`。
- `full_uv=true / crop=false / upsample=false`；没有从风格稿或目标截图回裁。

### Schedule

- 根：`372×246`；safe `[16,8,356,230]`。
- 真实禁用态、`当前第99天 / 剩余99天` 与零日边界均完成容量测试。
- 整根及所有后代 `MOUSE_FILTER_IGNORE / FOCUS_NONE`；无热区、无 hover / pressed / focus。

### CTA

- 五态均为 `414×76`：default / hover / pressed / focus / disabled。
- default / hover / pressed / focus 文案 bbox 与 hit rect 零位移。
- disabled 使用“暂不可进入”，无 hit rect、无焦点、无指针输入。

## 真实内容与容量 fixture

- 真实内容沿用北美：`北美禁区带`、`红线升温`、`洗衣店里出现了一片海`、四条现有任务、`本次进入：0 天`、`进入地区任务台 →`。
- 容量内容严格标为 `capacity_fixture_only`：八字标题 `北境深层雷达异常`、状态 `暂不可进入`、`99+`、`第 99 天` 与四行完整 `耗时99天｜限时第99天`。
- 容量 fixture 只证明插槽上限，不进入真实运行内容。

## 机器验证

`12-independent-slot-pressure-validation.json` 当前结果：

- `all_pass=true`。
- 真实栅格字形 `81` 处：越界 `0`，对比度失败 `0`。
- 图片同源、比例、完整 UV、无裁切、无上采样全部通过。
- collapsed / expanded 冻结插槽零位移通过。
- Dossier、Schedule 与 CTA 输入合同通过。
- 所有三张板为 `1920×1080`，所有运行时切片尺寸匹配。

## 双审与分歧处理

- UI Designer 与 UX 老哥首轮均确认排版、图片、零位移和 QA 身份成立，但分别发现 CTA 三态差异过弱、Schedule 禁用箭头像可点击，以及 Preview 未使用完整两位截止日格式。
- 已只改状态层和 fixture：CTA hover 提亮并加轻内线、pressed 压暗并加内压线；Schedule 右箭头改为低对比静态短横；四条容量任务改为完整 `耗时99天｜限时第99天`。纸材、尺寸、文字位置和热区均不变，独立验证仍为 `all_pass=true`。
- 完整 locked Dossier 的意见分歧已按当前 runtime 边界处理：当前锁定卡不会替换右侧 Dossier，因此本阶段不伪造该页，只保留 disabled CTA 测试。若未来改变交互，必须新开语义门。

## 当前 Gate

- `internal_slot_pressure_board`：`PASS`；UI Designer `PASS / P0=0 / P1=0`，UX 老哥 `PASS / P0=0 / P1=0 / P2=0`。
- `independent_2x_front_carrier`：继续保持通过。
- `atlas / manifest / Godot`：继续阻断。
- `BackDecor / StateDecor composition`：下一门已放行；不得改变已通过的 FrontCarrier、slot、图片和输入合同。
