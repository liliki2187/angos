# WMW `right_dossier_page` v0.8.5 无字 clean-sprite brief

> **历史版本**：动作栈几何已由 A196 / v0.8.6 取代；当前生产入口见 `2026-07-14-world-map-wmw-right-dossier-clean-sprite-brief-v0-8-6.md`。本文件仅保留 v0.8.5 的结构评审记录，不得继续作为现行合同输入。

> 日期：2026-07-14
> 产物类型：`production brief / structure board / not production art / not atlas / not Godot runtime`
> `structure_gate`：`pass`
> `brief_landing`：`conditional_pass`
> `imagegen_execution`：`hold_for_primary_cta_color_decision`

## 1. 本轮范围

本轮只把 A189 方案 B 转为可执行的无字素材结构，不调用 imagegen、不生产 atlas、不改 Godot、不修改三份 v0.8.5 合同的任何 frozen 字段，也不启动其它 class。

只覆盖：

- `right_dossier_page`：一个正交 parent hollow-shell 母版；
- `right_mission_intel_button`：一个独立次级按钮母版；
- `right_action_lane`：一个独立主 CTA 母版。

核心禁令：**不得生成“一张已经烘焙两个按钮的完整 dossier 成品”**。parent 与两个 child 必须分别生产、分别验收、按合同装配。

## 2. 真源与证据

- 合同：`design/ui-contracts/world-map/right_dossier_page.json` v0.8.5。
- 合同：`design/ui-contracts/world-map/right_mission_intel_button.json` v0.8.5。
- 合同：`design/ui-contracts/world-map/right_action_lane.json` v0.8.5。
- A189 与 raster bbox 复核：`2026-07-13-world-map-wmw-right-dossier-a184-capacity-review.md`。
- 当前文字证据：567-570；563-566 的文字位置证据已作废，不得引用。
- 风格真值：`benchmark-board-01.png`、`benchmark-board-02.png`、clean-lowpoly-weekly 支线规范与纸张材质合同。
- `05-right-dossier-base-v0-4.png` 只作外形、照片窗和纸件层次参考；旧三行动条、亮白纸、锈红常态 CTA 不是生产真源。

结构板：`571-world-map-wmw-v0-8-5-right-dossier-clean-sprite-brief-board.png`。
manifest：`572-world-map-wmw-v0-8-5-right-dossier-clean-sprite-brief-manifest.json`。

## 3. 精确几何与像素所有权

所有生产素材使用 `export_scale=2`。

| 元素 | reference rect | 2x 尺寸 | 像素所有者 |
| --- | --- | --- | --- |
| parent export | `320x520` | `640x1040` | `right_dossier_page` |
| `header_icon` | `[24,38,36,36]` | `72x72` | parent 中性安装位 + 独立 runtime 图标 |
| `title_slot` | `[82,42,160,34]` | `320x68` | parent 可见 carrier + runtime 文字 |
| `status_stamp` | `[246,34,58,58]` | `116x116` | parent 中性底盘 + runtime 文字 / 图标 |
| `photo_slot` | `[22,98,276,176]` | `552x352` | runtime 普通矩形照片 + parent 镂空窗口边界 |
| `region_body` | `[22,288,276,54]` | `552x108` | parent 只读 carrier + runtime 两行文字 |
| `decision_facts` | `[22,346,276,32]` | `552x64` | parent 只读 carrier + runtime 单行事实 |
| `mission_intel_button` | `[22,390,276,44]` | `552x88` | child 完整独占 |
| `primary_enter_cta` | `[16,444,284,50]` | `568x100` | child 完整独占 |

### Parent 独占

- 外轮廓、正面纸张、背后叠纸、侧签与单层硬阴影；
- 照片窗口四边及照片与纸面的遮挡；
- 标题、状态章、正文、事实区的无字可见 carrier；
- default / warning / locked 的页面级状态 accent mask；
- 两个 child rect 下方连续、无描边的页面底纸。

### Child 独占

每个 child 在自己的 export 内完整拥有：外框、纸边、内板、`left_icon_zone` 中性底盘、`label_plate`、`right_action_badge` 中性底盘、局部阴影与交互皮肤。

### 防双框硬规则

- parent 禁止在 child rect 内或周围绘制按钮托盘、凹槽框、label plate、图标井、箭头区或预烘焙按钮阴影；
- child 主轮廓不得依赖 parent 补边；局部阴影必须收在 child 导出画布内；
- 合成后每个按钮四边只能找到一套框、一套内板和一套阴影；
- parent、`region_body`、`decision_facts` 忽略鼠标，整页最终只有两个交互热区。

## 4. 固定 z 序

```text
z10  背后叠纸 / 侧签 / parent 单层阴影
z20  地区照片内容：普通矩形 cover，不做异形或圆弧裁切
z30  parent hollow shell：照片窗挖穿，窗口边界全部归 shell
z40  mission child + primary CTA child
z50  所有动态文字、数字、header/status/button 图标
z60  focus / hover / pressed / disabled 运行时反馈
```

照片只负责内容，不负责任何窗口边界。禁止从叠过框、文字或图标的 atlas / 截图回采照片。

## 5. Carrier 可见形态

### `region_body`

读作正式 dossier 上的两行正文印刷区：直接建立在 parent 主纸面上，可有 2-3 个极低对比宽面明度块及一条短左索引线，但不得出现闭合高对比框、独立阴影、角切、图标井、箭头、badge 或 hover。

### `decision_facts`

读作嵌入纸面的窄事实行：比主纸面深半档，可有上下细印刷规则线，左右保持开放；不得出现闭合按钮边、阴影、抬升、icon zone、右动作 badge 或箭头。

无字 affordance 直接失败条件：隐藏全部文字和图标后，评审仍把 `region_body` / `decision_facts` 认成可点击按钮，或无法区分上方次级按钮与底部主 CTA。

## 6. 三母版与状态派生

### `right_dossier_page_master`

- 一个正交 hollow shell；照片窗只挖一次；
- default / warning / locked 只通过批准的 accent mask 派生；
- 三状态 alpha、外边缘、carrier 与 frozen 槽位逐像素全等；
- warning 只允许 status stamp、窄侧签或局部边线进入 `warning_rust`，禁止整页染红；
- locked 不允许整页灰罩，正文和缺口必须保持可读。

### `right_mission_intel_button_master`

- 一个无字、无图标的 secondary 母版；
- rest / hover / pressed 从同一结构派生；
- locked 页面必须命名为 `locked_context_enabled`，保留可点击抬升、边界及 hover 邀请，不得误做 disabled；
- 相比主 CTA 使用更浅阴影、更克制边框与更低 badge 权重。

### `right_action_lane_master`

- 一个无字、无图标的 primary 母版；
- 主次不能只靠 50px 与 44px 的尺寸差；主 CTA 必须有更明确的抬升层、底边纸厚和内板对比；
- hover 只强化内板与窄边高光；pressed 只让视觉内板下压 1px、阴影收短；外框、hit rect 和布局不动；
- `locked_disabled` 去主邀请感，无 hover 抬升、无 pressed、低饱和并弱化边框。

构造断言：同 class 状态 alpha silhouette diff = 0，frozen slot diff = 0；禁止让 imagegen 分别生成多个状态成品作为生产输入。

## 7. 无字与运行时边界

素材禁止烘焙：

- 中文、英文、数字、条码内容、假文案、假数据；
- 警告三角、锁、箭头、靶心、勾等状态语义图标；
- title、status、正文、事实、任务数、缺口、按钮 label；
- 旧三 action lane、假 tooltip、假 pin 或任意同义重复符号。

运行时独占：所有文字 / 数字、header/status/button 图标、focus、hover、pressed、disabled 与 warning 确认行为。目标字体进入 Godot 后必须引用 570 的 raster alpha bbox 机制重新跑三状态 `8/8 fit`，当前最小运行时字号下限为 18px。

## 8. 风格与提示要求

正向：现代图形周刊拼贴、平面裁纸式低多边形、正面正交；`warm_paper` 暖灰米纸、窄 `ivory_edge`、一层清脆错位阴影；主纸面 4-6 个宽阔低对比明度面；深海军蓝负空间、干净橄榄、深青蓝和少量锈红；文字槽安静连续。

总约束句：

```text
front-facing orthogonal modern editorial dossier, matte warm gray-beige paper,
broad flat low-poly value planes, thin clean ivory edge, one crisp offset shadow,
transparent hollow photo window, calm writable carriers, separate secondary and
primary button sprites, no baked content
```

负向：无倾斜功能面、透视或梯形文字板；无双底板、双框、双阴影；无厚纸板、塑料 bevel、手游按钮或 SaaS 表单；无泛黄档案、污渍、折痕、撕裂或云状纸纹；无细密三角网；无整页 warning 红染或 locked 灰蒙层；不得复刻 v0.4 旧三按钮结构。

## 9. QA 与放行 gate

生产候选必须依次提供：

1. 三份合同 frozen geometry overlay；
2. photo / parent / two children / runtime 的分层板；
3. parent / child 伪色像素所有权板；
4. 照片窗四边与四角 200%-300% alpha close-up；
5. 隐去文字后的只读 / 次级 / 主 CTA affordance 板；
6. default / warning / locked 与 diff mask 的一母版派生板；
7. 两个按钮 rest / hover / pressed / disabled 交互板；
8. 无烘焙文字、数字、假字与状态图标扫描；
9. 纸张 / edge / secondary / primary / warning 的颜色 ROI 板；
10. 25% / 100% / 200% 目检；
11. Python 真实内容中间回填；
12. 1920x1080 Godot 4.6.2 windowed OpenGL3 三状态与交互截图。

硬 gate：`parent_child_absolute_position_match`、`parent_button_decoration_absence`、`readonly_carrier_no_hit_rect`、`single_master_geometry_identity`、`alpha_silhouette_identity`、`photo_window_alpha_clear`、`no_baked_text_digits_or_state_glyphs`、`paper_token_match`、`composite_cleanliness`、`card_body_opacity_probe`、`runtime_glyph_bbox_inside_inner`、`manual_200_percent_seam_review`、`godot_windowed_capture`。

整屏压力 fixture 必须故意使用不同计数，例如“线索3 / 任务情报12项”，禁止继续用相同的 12 冒充数据源已解耦。

## 10. 双评审结论

UI Designer 原结论：

> 不要生成“一张带两个按钮的完整详情页”。应生产三个独立母版：一个 parent hollow shell，加两个 child button clean sprite。

UX 老哥原结论：

> 结构 Gate 条件通过。允许把 brief 作为“结构已定、颜色待裁决”的版本落盘，但不得标记为 `ready_for_imagegen`。生图前唯一必须交用户裁决的是主 CTA 常态色族。冻结 rect 无需改变，也不需要升合同版本。

UX finding：P0=0；P1 为主 CTA 色义分叉、两个无字按钮同级风险、`locked` 名称污染仍可点击次级入口；P2 为父子接缝 gate、hover/pressed 时序验证和不同数值 fixture。上述 P1/P2 已写入本 brief，唯有主 CTA 色族仍需用户裁决。

## 11. 生图前唯一阻断

主 CTA 常态色存在三套历史口径：

| 选项 | 来源 | 风险 |
| --- | --- | --- |
| 橄榄绿 | 纸张合同的 primary 角色 | 与青蓝次级、锈红 warning、中性灰 disabled 最易保持语义独占；双评审推荐 |
| 锈红 | v0.4 旧参考 | 会与 warning 危险色冲突 |
| 芥末金 | 569 合同回填示意 | 尚无生产色真源，会新增第四套语义色 |

在用户裁决前，571 结构板只显示 `PRIMARY COLOR HOLD`，不得把任一颜色偷渡为生产决定。结构 brief 可以落盘，但不得启动 imagegen、状态 atlas 或正式颜色派生。

以下事项不阻塞无字结构，但在最终 runtime 前仍需确认：locked 次级入口文案 / 回调、warning 进入二次确认、“进入代价”是否统一为“地区任务预计耗时”。
