# WMW v5.1 资产化 / 有色映射 Bridge Brief

> 状态：UI Designer 草案已按两轮 UX 回归修订，可作为下一阶段输入。  
> 范围：A237 冻结的 1920×1080 v5.1 默认 / 日程确认两态。  
> 产物类型：`assetization_bridge_brief`，不是有色稿、生产素材、Godot 实现或正式合同。

## 1. 总结

A237 的几何与文案全部保持。下一阶段先制作“全局日程器”纵向切片，验证无字资产、运行时文字 / 图标、默认 / 二次确认两态和纸张材质；本轮不生成有色整屏。

## 2. 分区资产映射

| 区块与冻结位置 | 可复用既有资产 | 需新增无字资产 | 运行时层 | 禁止烘焙 |
| --- | --- | --- | --- | --- |
| 左侧三张地区卡 `[66,36/294/552,306,240]` | 条件复用 B2.12 的 `left_region_card_b212_hollow_shell_<state>.png`、`lower_substrate_<state>.png`、地球贴片与独立 runtime badge 图标；`left_region_card_b212_meta_retired_atlas_2x.png` 只作证据 / 装配参考，不整帧直挂 | 各地区正式照片必须按 `region_id` 独立提供；状态变化不得替换照片 | 地区名、按 `region_id` 绑定的照片、选中 / 锁定图标、hover / focus、整卡热区 | 地区名、锁定原因、任务数、天数；禁止把状态帧内的示例照片当地区身份 |
| 左下日程器 `[36,810,342,246]` | 纸张材质 atlas 只作材质源；`gd_project/Assets/ui/angus_packaging/region_task/assetized/rt-advance-day-atlas.png` 只参考日历 / 箭头语义，不直接复用外框 | 新建一张无字日程器母版：外纸、日期栏、动作栏、图标井、两条后果栏 | 栏目名、当前日、剩余日、主副文案、箭头 / 叹号、后果、到期提示、完整热区 | 具体天数、任务名、“推进 / 确认”文案、状态图标 |
| 中央标题区 | 不复用旧全屏文字图层 | 不需要独立背景；沿用全局深色板 | `WORLD MYSTERIES WEEKLY`、`WEEK 01` | 周数与可变标题 |
| 地图 `[426,96,924,936]` | `gd_project/Assets/ui/angus_packaging/world_map/imagegen_v6/final/components/wm-map-board-v6g-component.png` 仅可提取大陆轮廓遮罩和坐标参考 | 新建无路线、无 pin、无文字的深色低多边形地图底板 | pin、地区名、选中环、锁、hover / focus、热区 | 路线、地区名、锁状态、选中态、装饰性事件点 |
| 地图 pin | 旧 `wm-pin-icon-v6g-atlas.png` 有明显旧像素 / 描边语言，不直接复用 | 新建 clean-low-poly 无字 pin 状态 atlas：默认、选中、锁定 | 锚点保持 `(620,365)`、`(1164,371)`、`(1160,710)`；状态与地区标签运行时绑定 | 坐标、地区名、锁符号烘进地图 |
| 地图审计层 | 无 | 无 | 仅开发 / 验收开关：列宽、安全边距、TARGET_ONLY、组件 bbox | 审计文字、虚线框、尺寸说明不得进入发行资产 |
| 右侧全高档案 `[1398,24,480,1032]` | `right_dossier_candidate_a5_parent_2x.png` 只参考纸张语言和层次，禁止拉伸；compact A5.1 能力不变 | 先建立独立 `right_dossier_tall / A5.1-H` 派生候选规格，再新建专属无字全高 parent shell | 地区标题、正文、任务摘要；A237 默认态显示四任务展开，`collapsed_summary / expanded` 继续使用单一 disclosure 回调且两态等高 | “红线升温”、地区名、任务统计、正文；收起态不得压缩档案或让 CTA 上移 |
| 地区照片 `[1431,171,414,264]` | `gd_project/Assets/ui/angus_packaging/world_map/wmw_v091_right_dossier_candidate_a1/ingredients/right_dossier_north_america_photo_552x352.png` 的 69:44 比例可用于构图占位 | 北美及其他地区的正式身份照片后续按同规格分别生产 | 按当前 `region_id` 换图 | 标题、图注、状态文字；现有北美图不得升格为正式地区身份资产 |
| 地区正文 `[1431,456,414,135]` | 复用全高 shell 的纸面语言 | 正文 carrier 纳入新 parent shell | 两行地区说明 | 具体正文 |
| 任务情报头 `[1425,609,426,66]` | 沿用 compact A5.1 的单一透明 disclosure 热区 / 回调语义；不复用旧满宽青色按钮皮肤 | 新 shell 内提供低权重分组边界 / 分隔线 | `任务情报`、任务摘要或 `已展开 4/4`、`＋/－` 状态指示；expanded 显示四行，collapsed 用同高摘要替换四行区域 | 统计数、任务类型文字；不得拆成多个按钮，不得因收起改变 CTA 位置 |
| 四条任务 `[1431,681,414,248]` | 无可直接复用的同规格行 | 新建统一无字任务行母版；常驻 / 限时 / 深链只使用无字语义色条或 tag 底 | 序号、任务名、内容类型、耗时、截止日、类型标签 | 任务名、耗时、截止日、类型文字 |
| 底部 CTA `[1425,957,426,75]` | `right_action_lane_candidate_a3_primary_olive_2x.png` 可复用为可进入地区的 default 色皮；284×50 对应 1920 下 426×75 | 若现有资源包没有同几何 `locked_disabled` 皮肤，必须按 `right_action_lane` 既有合同补齐，不能用 opacity 临时代替 | `进入地区任务台 / 暂不可进入`、箭头、hover / pressed / focus、enabled / disabled 热区 | CTA 文案、地区名、天数；锁定地区不得继续显示橄榄进入邀请态 |

## 3. z-order 与安全区

| 层级 | 内容 |
| --- | --- |
| `Z0` | `dark_board` 全局深色底 |
| `Z10` | 大区块无字 parent shell、地图底板 |
| `Z20` | 地区照片及嵌入式内容图 |
| `Z30` | 纸边、窗口框、裁切 mask、分隔线 |
| `Z40` | 运行时文字和独立信息图标 |
| `Z50` | pin、锁定、选中、hover、focus |
| `Z60` | 二次确认和 pressed 状态反馈 |
| `Z90` | 仅开发环境启用的几何审计层 |

硬规则：

- 标题栏、日期栏、任务行、CTA 和所有文字 carrier 必须保持 `0°` 正交。
- 倾斜只允许在不承载文字的背页、贴纸边或阴影中，且不得越过组件矩形。
- 地图、档案、日程器不得侵入 24px 外围安全区和三栏 gutter。
- 地区照片固定 69:44，不拉伸、不透视。
- 必须先识别 `visible_color_module_rect`，再派生 `content_rect / inner_safe / glyph_bbox / hit_rect`；不得凭浅色区域猜文字载体。
- 小中型文字预留约 8–14px 内边距，CTA 预留 12–18px。
- pin 周围保持低细节，标签方向避免高对比碎分面；不增加标签底牌或地图图例。

## 4. 材质与色彩边界

- 全局底使用 `dark_board`，接近 `#16191C / #191C1E`。
- 新纸面按角色使用 `warm_paper / paper_mid / ivory_edge`，禁止全屏统一重染。
- 主 CTA 延续已采纳的 olive。
- teal 只用于信息层，不形成第二主按钮。
- warning rust 只服务真实截止或二次确认，不作常驻装饰。
- B2.12 保持已批准配色，不重新校色。
- 禁止奶油白、泛黄档案纸、污渍、折痕、旧报纸颗粒、密集三角网、GIS 网格和装饰路线。

## 5. 日程状态矩阵

v5.1 冻结截图仍只展示 default / confirming，两态只允许在 `[36,810,342,246]` 内改变：

| 字段 | 默认态 | 确认态 |
| --- | --- | --- |
| 图标 | `→` | `!` |
| 主文案 | `推进到下一天` | `确认推进到第 2 天` |
| 副文案 | `点击后查看推进影响` | `再次点击执行 · 后果见下方` |
| 后果行 | `当前：无任务到期` | `确认后：剩余 6 天 · 无任务到期` |
| 底行 | `日程归零：进入编辑部阶段` | `限时任务：雷达异常仍开放至第 4 天` |

实现原则：一张无字母版 + 运行时文字 / 图标 / 局部状态层。不制作两张完整日程器，不交换整屏资产。当前日和剩余日在进入确认态时保持不变；二次确认沿用原位热区，不弹模态框。

生产候选必须补齐以下状态，不能只做两张静态皮肤：

| 状态 | 进入条件 | 交互与退出 | 可见要求 |
| --- | --- | --- | --- |
| `idle_enabled` | `advance_day` 能力存在且 `remaining_days > 0` | 首次点击进入 `confirming` | 对应 v5.1 default |
| `confirming` | 首次点击 | 再次点击进入 `executing`；`Esc`、点击日程器外、切换地区或关键上下文变化均撤回 `idle_enabled` | 对应 v5.1 confirming；日期栏仍显示提交前的当前日 / 剩余日 |
| `executing` | 第二次点击已提交命令 | 锁定完整热区，拒绝重复提交；成功后进入 `committed`，失败后回到可操作态并显示真实错误 | 主动作区显示局部执行反馈，不移动组件、不弹第三层确认 |
| `committed` | 命令成功 | 原子刷新当前日、剩余日和到期结果；若剩余日归零则进入编辑部阶段，否则回到 `idle_enabled` | 不保留旧确认文案，不出现跨区域残影 |
| `disabled_runtime_unavailable` | runtime 尚无独立 `advance_day` 能力 | 热区禁用 | 真实运行构建不得把 target-only 默认态伪装成可点击；资产演示须显式标注 mock |
| `disabled_zero_days` | `remaining_days == 0` 且尚未完成页面切换 | 热区禁用；不得再进入 confirming | 不显示“推进到下一天”，不出现负天数；若页面仍短暂停留，显示本周日程已结束 / 正在进入编辑部 |
| `hover / focus / pressed` | 对应 enabled 状态的指针 / 键盘 / 按压反馈 | 不改变状态语义 | 只加强边线、明度或局部层，不移动文字和热区 |

最后一天边界：当 `remaining_days == 1` 时，确认态必须明确 `确认后：剩余 0 天 · 进入编辑部阶段`；执行后不得进入“下一天”空状态或显示负数。

## 6. 第一条纵向切片

优先选择“全局日程器”：

- 它是 v5.1 新增且没有同规格现成资产的独立组件。
- 默认 / 确认两张真源已有严格像素差异边界。
- 一次可验证纸张材质、文字 carrier、图标分层、状态切换和热区。
- 不触碰 compact A5.1 frozen，也不被地图和全高档案的资产规模拖慢。
- 当前 runtime 没有独立 `advance_day`；本切片只能称为资产与装配候选，不能宣称功能已实现。
- 切片前先形成 `schedule_gate` 派生候选规格，登记可见模块、文字安全区、完整热区和以上状态矩阵；该规格不是对现有正式合同的修改。

## 7. 后续生产顺序

1. `schedule_gate` 派生候选规格 → 日程器无字母版 → 运行时填充规范 → default / confirming / disabled / executing 100% crop。
2. `right_dossier_tall / A5.1-H` 派生候选规格 → 全高 parent shell 与统一任务行母版；北美现有照片只作占位，橄榄 CTA 仅用于可进入态并补 `locked_disabled`；同时验证 `collapsed_summary / expanded` 两态等高、CTA 不移动。
3. 无路线地图底板；旧 v6g 仅作轮廓遮罩来源。
4. 新 clean-low-poly pin 状态 atlas。
5. 与冻结 B2.12 合并，生成无字整屏装配检查。
6. 填入真实中文运行时文字和图标，输出 1920×1080 两态与几何审计。
7. 与两张 benchmark board 直接并排复核；通过后再由用户决定是否进入正式合同或 runtime。

## 8. 支线复审规则

本支线继续执行 `clean low-poly weekly` 临时例外：不调用旧像素 / 半调坐标系的 `angus_art_director`。复审链为：

```text
benchmark 原图
→ clean-low-poly 支线规范
→ 纸张 / 色彩合同
→ UI Designer
→ UX 老哥
→ 父级逐项对照
```

未完成上述直接标杆复审的资产不得称为生产标杆或正式美术真源。

## 9. 发行审计隔离 Gate

- `Z90` 必须是独立开发资源 / 节点，默认关闭，不得进入任何 atlas、parent shell 或发行位图。
- 发行构建中 `LOW-FIDELITY / TARGET_ONLY / LEFT 342 / CENTER 924 / RIGHT 480 / safe margin / bbox` 等审计字形和虚线像素必须为 0。
- 发行节点树中审计 overlay 节点数量必须为 0；仅隐藏但仍打包的节点不能算通过。
- 结构验证图继续保留 `TARGET_ONLY`；正式资产截图则通过旁注和 Delivery Manifest 声明边界，不把审计文字烘进界面。
