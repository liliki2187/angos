# 世界地图 Dossier 文字注册错位与强行拼贴 Loop Log

## 结论

用户否决成立。`04-real-content-filled-state-style-target-1920x1080.png` 虽证明了三地区同壳、`69:44` 图片复用和状态数据边界，但没有证明文字真正属于可见组件。程序把 frozen slot 坐标直接压到一张内部纸件位置不同的 ImageGen 母壳上，并额外覆盖纸块、边框和纹理条；文字对齐的是程序矩形，不是玩家看到的标题纸、照片孔、正文纸、Disclosure、preview 纸和 CTA 票条。

当前图降级为：

`programmatic content-overlay mismatch diagnostic / rejected filled-state target`

不得继续称为真实内容风格目标、容量通过证明或资产化来源，不进入 Godot。

## 触发

2026-08-21，用户审阅主审图后明确指出：

> “感觉目前的拼贴很强行啊，文字内容都没有对准界面组件，文字在组件里的大小等都有问题。”

该反馈推翻父级、UX 老哥与 UI Designer 上一轮的视觉通过判断。此前通过只保留为数据、图片规格、状态语义和同壳复用的技术证据，不再代表玩家可见排版成立。

## 影响

- 标题、状态、headline、正文、Disclosure、任务预览和 CTA 的数学坐标大致在合同槽内，但没有注册到母壳真实可写纸面。
- 母壳原纸边与程序新增纸块同时存在，产生双框、接缝、盖住阴影和“后贴文本框”感。
- 三个 `468×1032` Dossier 被缩成约 `390×860` 后再与 proof rail 同屏，正文和 metadata 被迫降成工程注释级字号。
- `fit_text` 让各地区和各字段按“是否塞得下”自由缩字，破坏统一的排版系统。
- 同一张图同时承担 beauty target、三地区 content swap、三状态、标题压力和工程 QA，产物类型混杂。

## 失败信号

1. 顶部标题纸、夹子和 status 没有共同基线；程序状态框又与母壳锈红圆章竞争。
2. `69:44` 图片虽然比例正确，但贴入的是程序硬框，不是母壳真实照片开窗和纸垫。
3. headline 被挤成后台标签条，正文小字悬在大纸左上角。
4. Disclosure 被画成封闭实底按钮，违背冻结的透明背景、轻分隔线与标题 / facts / symbol 三区。
5. 两条 preview 字号过小、行间死空，未形成稳定编辑索引关系。
6. locked 下区是程序覆盖的大蓝矩形，像未加载占位而不是空档案袋。
7. CTA 文字数学居中，却没有落在 ImageGen 票条真实内框。
8. 外部 FORMAL / FIXTURE / PENDING 和 proof rail 进一步把画面推向设计审核板，而非游戏 filled-state。

## 根因

### 1. 把无字美术方向误升格为 content-ready carrier

用户接受的是上一张 component board 的版面 / 物件语言方向，不是其中每张纸已经与 frozen dynamic slot 完成几何注册。父级把“无字壳看起来对”扩大为“可以直接填真实文字”。

### 2. 缺失 `visual_write_rect` 审计

生成后没有先标出真实可写纸面、折痕、夹子、阴影、破口和露边禁区，而是直接使用 frozen rect。正确安全区应为：

`frozen slot ∩ visible writable paper − no_text_rect`

交集不足时应重做母壳，而不是加一张程序纸或继续缩字。

### 3. 程序越权补美术载体

程序不只排字，还重画标题纸、图片框、headline 条、正文纸、Disclosure、expanded 纸和 CTA，实质把 ImageGen 母壳降成背景纹理。美术接触关系被矩形覆盖，产生强行拼贴。

### 4. 用 QA 标注替代 100% 玩家视图证据

上一轮审查过度关注 `69:44`、正式任务名、状态 pending、共 4 显 2 等可枚举事实，却没有先用 100% 原图检查真实字形、基线、纸面内边距和光学轴。板上写着“同壳”“8 字通过”不等于玩家视觉已经通过。

## 立即止损

- 停止修改当前三联板；不在其上继续移动 3–5px 或缩字。
- 删除其 `filled-state style/capacity target` 身份。
- 02b 只保留为钴蓝开放稿夹美术语言 donor，不是可直接填字资产。
- 三张 canonical 地区图、North 正式内容、East/Pacific fixture 矩阵和状态覆盖思路可以保留。

## 下一版流程

1. 只做一张 North America `468×1032` 原生 1:1 Dossier，不先做三联板。
2. 在母壳原尺寸建立三层叠加：
   - frozen slot；
   - `visual_write_rect`；
   - clip / fold / shadow / exposed-edge `no_text_rect`。
3. 若可写交集不足，依据 frozen slots 重生母壳；不新增程序纸块，不升合同版本。
4. 冻结统一 type tokens，再填内容；禁止逐文案自由 `fit_text`，只允许合同声明的单级 fallback。
5. 分别输出 North collapsed 与 expanded 的 100% 玩家视图，先验 title、photo、headline、body、Disclosure、两条 preview 和 CTA。
6. North 通过后，使用完全相同的字号、行高和坐标替换 East / Pacific。
7. 玩家视觉目标只展示一个真实 Dossier；三地区 / 多状态容量与工程说明另做独立 QA 板。

## 防复发 Gate

- 动态文字不得压住夹子、折边、阴影、袋面、纸边或露边。
- 不存在为了装文字而额外绘制的不透明纸矩形。
- title、photo、headline、body、Disclosure、preview、CTA 形成稳定光学左轴。
- Disclosure 保持透明轻量，不读成整条按钮。
- 任意地区切换不改变字号、行高、组件尺寸与图片槽。
- 八字标题不靠异常缩字通过。
- 100% 玩家视图先通过，才允许做缩小展示板。
- beauty target 不再夹带 proof rail、fixture badge 或工程说明。

## 保留冻结

- 桌面 1920×1080 与三栏结构。
- `right_dossier_page` v1.0.0 动态槽和状态语义。
- `right_mission_intel_button` v1.0.0 hit、透明 Disclosure 与 title / facts / symbol 三区。
- expanded 仅两条只读 preview，无新 hit / hover / button。
- CTA 独立且唯一；FrontCarrier `0°`。
- 三张 `1104×704 / 69:44` 母图只等比缩放、完整画幅。
- 暂不进入 atlas、manifest、Godot 或 `WeeklyRunGame`。

## 修复结果

已完成 North America 单卡文字注册候选：

- `09-north-dossier-collapsed-runtime-468x1032.png`
- `10-north-dossier-expanded-runtime-468x1032.png`
- `11-north-dossier-registration-qa-1920x1080.png`

可见壳体与 expanded 连续索引纸均来自真实 ImageGen；程序仅执行既有美术模块的几何注册、`69:44` canonical 图片回填、固定字号文字与 QA 排版，没有补画纸块、按钮底板或任务卡。刊头 kicker 已避开中央夹子禁区；正文、Disclosure、两条任务与 CTA 均按真实纸边 / 袋角建立写入区；expanded 第二条任务移至真实分隔线下方，重复统计已删除。

UX 复审先给出 `CONDITIONAL PASS`，要求加深正文与 Disclosure、增强 `＋/－` 并删除重复统计；上述三项关闭后，UI Designer 终审为 `PASS / P0=0 / P1=0`。该结果只证明 North 单卡的文字注册方法成立，仍待用户视觉确认；不证明三栏整屏、East / Pacific 复用、Godot 字体、hit rect、atlas 或生产资产。

## 当前状态

`north_single_dossier_text_registration_pass_pending_user_visual_confirmation`
