# Subagent 协作与能力沉淀规则

> **用途**：规定父级 Codex 如何和 `game_producer`、`game_sys_architect`、`game_numerical`、`game_logic_check`、`ux_laoge`、`ui_designer`、`angus_art_director`、`angus_character_pixel_director`、`steam_indie_appraiser` 等项目级 subagent 协作，并把实战经验沉淀成可复用知识，而不是把核心文档越写越臃肿。
> **定位**：这是项目级协作规则，不是某个 subagent 的自身 prompt。
> **最后更新**：2026-07-13（新增 clean low-poly weekly 支线的美术指导临时路由例外）

---

## 1. 分层原则

subagent 成长只允许按层沉淀，不把普通案例直接塞进核心规则。

- **项目级硬规则**：写入 `AGENTS.md` 或 `docs/onboarding/*`。例如 Angus 不做移动版、截图交付规则、何时必须调用哪个 subagent。
- **subagent 自身流程**：写入对应 `skills/<skill-name>/SKILL.md`。例如 UX 老哥的 P0/P1/P2 流程、SIA 的 Steam 首屏 / ROI 模式。
- **普通实战案例**：写入对应 `skills/<skill-name>/references/casebook/`，不写进 `SKILL.md` 主体。
- **重复出现的模式**：先在 casebook 里累计，至少 3 次以上稳定出现，再提炼成 `references/patterns.md` 或对应方法论文档。
- **用户明确采纳 / 撤回 / 待定**：先写入 `docs/设计采纳记录.md` 总索引，再按索引路由写入 `docs/design-decisions/` 对应分册。该文档记录用户决策，不替代规格文档；跨领域意见必须补 cross-read tags，避免后续只读单一分册而漏掉 UI / 机制 / 美术 / 流程上下文。
- **Codex Desktop 注册壳**：`.codex/agents/*.toml` 只保留短启动壳，不承载完整中文规程、案例库或 references 清单。
- **沉淀去重律（2026-07-08 起）**：同一条经验只允许一个主承载位（全文），其他位置只准短引用 + 链接；写入前先 `rg` 查重，命中就更新原条目而不是新开日期补丁或在别处重写全文。完整规则见 `docs/workflows/angus-workflow-harness.md` §7.1。

## 2. 父级 Codex 的角色

父级 Codex 是总编，不是两个 subagent 的转发器。

- 先判断当前问题应该由谁提供判断：制作人看立项、范围、里程碑、greenlight / kill 和生产风险；系统架构看核心循环映射、系统注册、边界接口、依赖/耦合和资源流；数值策划看 Angus 主干数值、公式、概率、配表和验证方案；逻辑审查看已成形规则、状态机、配表、剧情时间线和跨系统依赖的漏洞；SIA 看吸引力、商业可读性和功能 ROI；`@像素艺术` / 美术指导看 Angus 全局视觉风格、美术资源、界面视觉包装、像素 / 半调 / 印刷材质、参考图转译和 prompt 跑偏；像素美术专科看四人标杆图一致性、角色高清微像素、角色表情真值源和角色 prompt；UX 老哥看操作链、信息层级、遮挡、状态与误读。
- UI Designer 看从 brief 到元素表、桌面 16:9 wireframe / mock、控件清单和设计交接；它不替代 UX 老哥做现有界面诊断。
- 给 subagent 的任务必须窄，明确“不看什么”。例如“只看桌面 16:9 首屏遮挡，不做移动版建议”。
- subagent 默认只读诊断或规划，不直接改代码、不直接生成图片，除非用户另行明确要求。
- 父级负责合并意见、识别冲突、做取舍，并把最终落地范围讲清楚。
- 如果 Game Producer、Game System Architect、Game Numerical、Game Logic Check、UI Designer、Angus Art Director、Angus Character Pixel Director、UX 老哥或 SIA 意见冲突，父级不能把多方建议都堆进系统、界面、数据、美术或计划；必须说明冲突、取舍成本和推荐方案。

## 3. 协作顺序

常用顺序如下：

1. **Steam 产品吸引力未定 / Steam 首屏 / 功能 ROI / 竞品借鉴**：先调用 `steam_indie_appraiser`。
2. **立项 / 重大功能 / 范围失控 / 里程碑 / 熔断判断**：用户输入 `@制作人` 或明确要求制作人视角时，调用 `game_producer`。它可以使用 SIA 的市场证据，但不替代 SIA 做 Steam 首屏、头图、宣传片或垂直切片吸引力诊断。
3. **系统结构 / 新系统注册 / 资源流 / 耦合审查 / 更新系统索引前置判断**：用户输入 `@系统架构` 或明确要求系统架构时，调用 `game_sys_architect`。它位于制作人下游、系统设计/数值/逻辑审查上游，只读输出蓝图、注册表、依赖图、资源流和健康检查；已确认结构若要写入 `systems-index.md`，再由父级 Codex 或 `map-systems` 落盘。
4. **Angus 主干数值 / 达标率 / 概率 / 配表 / 平衡验证**：用户输入 `@数值策划` 或明确要求数值策划时，调用 `game_numerical`。它只在系统结构和体验目标基本明确后接入，负责公式、变量、参数区间、配表和验证方案；Roguelite、卡牌、塔防、回合 RPG、MMO/F2P、商业手游等只作为按需资料库，不干扰 Angus 数值设计主干。
5. **已成形规则 / 状态机 / 配表 / 剧情时间线 / 跨系统依赖审查**：用户输入 `@逻辑审查` 或明确要求逻辑检查时，调用 `game_logic_check`。它只读，不设计、不修改；适合在规则、数值、剧情或实现片段准备落地前找 exploit、因果断链、边界条件、跨系统矛盾和叙事一致性问题。
6. **新 UI / 新布局从 brief 出稿**：先调用 `ui_designer`，输出元素对照表、桌面 16:9 mock、质量报告和给 UX 老哥的交接摘要。
7. **已有 UI / 截图 / 原型改进**：先调用 `ux_laoge`，确认操作链、信息层级、遮挡、状态噪音和玩家误读。
8. **UI 方案落地前**：让 `ui_designer` 与 `ux_laoge` 接力校验；新稿先 UI 后 UX，现有页先 UX 后 UI。拟物 / 资产化 UI 必须在接力中交接视觉可使用区域：UI Designer 给出文字安全区表和 `content_rects / no_text_rects` 假设，UX 老哥检查控件盒通过但视觉安全区失败的情况，父级落地时把关键安全区变成截图裁切或测试断言。若 UI 任务的主要问题是视觉风格、像素 / 半调 / 印刷材质、参考转译或 prompt 跑偏，再让 `angus_art_director` 做风格守门；它不替代 UI 布局和 UX 可读性。`game_producer` 不插入每次 UI 设计，除非该 UI 背后代表重大功能扩张、项目方向变化或里程碑风险；`game_sys_architect` 只在 UI 背后代表系统边界、资源流或状态接口变化时提供结构输入；`game_numerical` 只在数字呈现依赖明确阈值、概率或参数区间时提供输入；`game_logic_check` 只在 UI 承载状态机或规则流程时检查逻辑，不审布局。
    - 资产化 UI 的阶段判断必须先于下一步建议：如果当前产物只是 `visual_style_reference` / `color-locked style draft` / 无字风格方向稿，且尚无通过复审的 `filled-state text mock`，父级不得把组件拆分、atlas、manifest 或切图说成当前下一步。此时必须先组织轻量内容合同，再做真实内容填充预览稿，并交给 UI / UX / 像素艺术复审。
    - **`clean low-poly weekly` 临时例外（2026-07-13）**：当任务明确以 `design/art-direction/references/clean-lowpoly-weekly-branch/benchmark-board-01.png` 与 `benchmark-board-02.png` 为视觉真值时，不自动调用 `angus_art_director`，也不把它的像素颗粒、重半调或套印结构判断作为放行条件。该 agent 的启动壳和技能仍以旧像素 / 半调坐标系为默认，容易把“大块低多边形明度面 + 干净现代周刊 + 轻纸品”拉回旧方向。支线临时改由父级直接执行标杆对照，强制读取 `clean-lowpoly-weekly-branch-style-guide.md`、纸张材质合同与 Color Contract；`ui_designer`、`ux_laoge` 继续负责布局、容量、可读性和交互。用户显式点名 `@像素艺术` 时仍可调用，但其意见仅作非阻断对照。恢复自动路由前，必须先完成该 agent 的支线专用真值源 / 失败样本校准，并由用户确认重新接入。
9. **美术资源 / 界面视觉风格 / 参考图 / prompt 审查**：用户输入 `@像素艺术`、`@美术指导`，或明确要求 Angus 美术资源、界面视觉风格、美术风格守门时，调用 `angus_art_director`。它根据 `design/art-direction/angus-visual-style-guide.md` 判断是否像 Angus，输出风格风险、可转译手法、负面约束和交接对象。
10. **像素美术 / 四人标杆图一致性 / 角色 prompt**：用户输入 `@像素美术`、`@像素角色`、`@角色美术`、`@角色风格守门`、`@角色设计风格`，或任务对象是眼镜记者、末日时钟、伪人、外星少女、新角色、角色头像/立绘/群像/表情时，调用 `angus_character_pixel_director`。它根据 `角色设计风格规范-AI包` 和四人标杆图判断角色是否过线，输出真值源、参考图角色、负面约束、prompt 和验收清单。
11. **视觉资产生成前**：如果目标是 Steam 首屏、头图、宣传片或 demo 吸引力，SIA 先确认第一眼吸引力和可截图产物，再由 `angus_art_director` 审风格和 prompt；如果目标是普通 UI 贴片、材质、场景概念或全局视觉实验，由 `angus_art_director` 写 / 审 prompt；如果目标是角色头像、角色立绘、角色群像或新角色，先由 `angus_character_pixel_director` 写 / 审 prompt；最后再交 `openrouter-image-gen` 或父级执行生成。`clean low-poly weekly` 两标杆支线按第 8 条临时例外执行，不经过 `angus_art_director`。
    - 若生成前或返工要求涉及色彩调整、去黄、提亮、压暗、冷暖、纸色或“更接近参考图”，父级和 `angus_art_director` 必须先按 `docs/onboarding/imagegen-color-contract-gate.md` 建立 `Color Contract v1`：唯一参考图、固定 ROI、`hex / RGB / Lab`、逐 token 阈值、整图均亮度、纸面 / 暗部比例和失败边界；没有合同不得继续写调色 prompt。候选图生成后必须同 ROI 复采样，颜色硬闸门未过时，`angus_art_director` 不得继续给“风格通过 / 生产标杆候选”的判断。
12. **视觉资产生成后复审**：除 `clean low-poly weekly` 两标杆支线临时例外外，生成出的 UI 风格稿、美术资源包、界面元素风格稿或生图结果，只有经过 `@像素艺术` 复审后，才能称为生产标杆、资源标杆或真源候选。复审必须显式检查像素颗粒度、颗粒密度、半调 / 套印是否成为结构语言、是否继承当前标杆图、动态文字安全区是否可落地，以及是否滑向旧报纸、旧档案、泛黄纸噪点或高清摄影噪声。`clean low-poly weekly` 支线由父级对两张标杆做逐项对照，并联合 UI / UX、Color Contract、纸张材质合同和真实内容回填证据放行；缺任一项仍只能归档为风格草稿或偏差案例。
13. **交付前**：父级用真实桌面截图复核，并说明采纳、未采纳或待确认项。

## 4. 实战案例记录格式

casebook 每条只记录可迁移的短经验，禁止写成长篇复盘。推荐结构：

```md
## YYYY-MM-DD · 案例名

- **场景**：这次处理的对象。
- **调用**：用了哪个 subagent / skill。
- **判断**：关键诊断是什么。
- **用户反馈**：用户采纳、修正、撤回或补充了什么。
- **可迁移规则**：一句话，说明未来遇到相似情况怎么判断。
- **不升级原因**：为什么它暂时不进 `SKILL.md` / `AGENTS.md`。
```

## 5. 升级门槛

只有满足以下条件之一，普通案例才允许升级：

- 用户明确说这是长期规则或顶层硬规则。
- 同类案例至少出现 3 次，且用户反馈都指向同一判断。
- 某条经验会影响后续所有任务的安全性、截图交付、调用方式或项目范围。
- 某条经验已经从单一案例变成可操作模板，例如固定的 ROI 分层、固定的截图验收清单或固定的 UI 安全区规则。

反过来，以下内容不得升级到核心：

- 单张图片的局部调色、局部遮罩、局部按钮位置。
- 某次实验页里的临时折中。
- subagent 对一个具体素材的主观偏好。
- 父级为了赶进度做出的临时实现选择。

## 6. 当前固定分工

### Game Producer

适合：

- `@制作人` 触发的制作人视角判断；
- 立项评估、greenlight / kill、熔断判断；
- 重大功能范围把关、P0/P1/P2、人月和 80% 替代方案；
- 项目里程碑复盘、scope 膨胀检查；
- 制作人视角竞品分析：可复制 / 不可复制、ROI、团队成本、下一阶段验证。

不适合：

- Steam 头图、商店页、宣传片、demo 吸引力诊断；
- 每次 UI 设计默认参与；
- 具体 UI / 系统 / 数值 / 叙事设计；
- 直接改代码或生图；
- 在没有来源时声称“最新市场数据”。

### Game System Architect

适合：

- `@系统架构` 触发的只读玩法系统架构判断；
- 核心循环到 L1/L2/L3 的系统树拆解；
- 新系统注册、系统放置、合并 / 降级 / 暂缓建议；
- 系统依赖图、资源流转图、Source / Pool / Converter / Sink / Trader；
- 边界接口、扇出节点、耦合度和架构健康检查；
- 更新 `design/gdd/systems-index.md` 前的架构蓝图或审查。

不适合：

- 判断功能是否值得做或是否超范围；
- Steam 头图、商店页、宣传片或垂直切片产品相；
- 具体 if-then 规则、状态机细节、任务规则或剧情条件；
- 数值、概率、阈值、公式或配表；
- 已成形规则漏洞审查；
- UI/UX 可读性或布局；
- 技术架构、API、数据库、工程目录或代码质量；
- 直接替代 `map-systems` 更新 `systems-index.md`。

### Game Numerical

适合：

- `@数值策划` 触发的数值策划判断；
- Angus 主干数值：角色骰、达标率、任务目标值、需求总量、黑骰反噬、周压力、发刊结算、势力/宏观属性、资源消耗；
- 概率校准、难度曲线、参数区间、配表和验证方案；
- 把“可搏 / 稳妥 / 压迫 / 稀缺 / 失控 / 成长”等体验目标翻译成公式和变量；
- 既有原型太难、太稳、太随机、太无感时，定位数值原因。

不适合：

- 判断功能是否值得做或是否超范围；
- 判断 Steam 吸引力、头图、宣传片或垂直切片产品相；
- 设计系统结构本身；
- 判断玩家是否看懂界面数字；
- 直接设计 UI；
- 默认套用 Roguelite、卡牌、塔防、回合 RPG、MMO/F2P、商业手游数值模板；
- 默认读取商业/MMO/F2P 资料库。

### Game Logic Check

适合：

- `@逻辑审查` 触发的只读规则审查；
- 已成形规则、GDD、配表、状态机、剧情时间线或实现片段；
- exploit、重复结算、资源刷取、因果闭环、边界条件、跨系统矛盾、MDA 体验逻辑和叙事一致性；
- 周循环、派遣/角色骰、黑骰、深度链、发刊结算、势力任务、宏观属性、资源流的上线前规则防爆；
- 大改系统后，检查是否有状态不可达、不可退出、后果不可观测或永久锁死。

不适合：

- 早期头脑风暴或创意验证；
- 判断功能是否值得做或是否超范围；
- 做系统设计或改规则；
- 做数值调优或配表设计；
- 判断 Steam 吸引力；
- 判断玩家是否看懂界面；
- 直接改代码、GDD、配表或剧情稿；
- 替代 `design-review` 的文档完整性检查或 `code-review` 的代码质量检查。

### Angus Art Director

适合：

- `@像素艺术`、`@美术指导`、`@美术总监`、`@ArtDirector`、`@像素风美术`、`@视觉风格`、`@风格守门`、`@美术鉴赏师` 触发的只读美术风格判断；
- Angus 全局视觉风格守门：深蓝 / 红橙 / 米白、现代异常周刊、印刷品物质感、黑色幽默、角色高清微像素与 UI/印刷材质比例；
- 像素 / 半调 / 信号噪点 / 套印错位 / 印刷材质的可用手法和禁区判断；
- 外部参考图转译：哪些手法可迁移，哪些只是通用像素风或 Angus 不适用；
- 视觉 prompt 审查、负面约束、生成后验收清单；
- 生图或截图结果的风格跑偏诊断：旧报纸、暖木、全像素、通用赛博、手游素材包、灰土档案等。

不适合：

- 直接生成图片或调用图像模型；
- 替代 `ui_designer` 做布局、元素对照表、wireframe 或 mock；
- 替代 `ux_laoge` 做 P0/P1/P2、可读性、遮挡、操作链和状态误读；
- 替代 `steam_indie_appraiser` 判断 Steam 第一眼吸引力、商店页、头图、宣传片或 demo 卖相；
- 替代 `game_producer` 判断美术资产范围、人月、里程碑或外包风险；
- 替代 `art-reference-picker` 做本地图库清点、归档和发送；
- 自行修改 `design/art-direction/angus-visual-style-guide.md` 或其它真源。需要改风格定义时必须交给父级和用户确认。

### Angus Character Pixel Director

适合：

- `@像素美术`、`@像素角色`、`@角色美术`、`@角色风格守门`、`@角色设计风格` 触发的只读像素美术 / 角色美术判断；
- 眼镜记者、末日时钟、伪人、外星少女、新角色、角色头像、角色立绘、角色群像和角色表情；
- 根据 `角色设计风格规范-AI包` 与四人标杆图判断角色高清微像素、Q 版比例、深蓝夜色、像素密度、低能量表情是否一致；
- 伪人灰肤、红瞳、嘴型等级 3，以及末日时钟低头闭嘴放空表情的真值源验收；
- 新角色 DNA：异常类型、超自然关系、服装语言、情绪基线、识别色和群像兼容性；
- 给 `openrouter-image-gen` 输出角色 prompt、参考图清单、负面约束和生成后 checklist。

不适合：

- 替代 `angus_art_director` 判断全项目视觉方向、UI 包装、Steam 头图或印刷材质系统；
- 替代 `openrouter-image-gen` 实际生图；
- 替代 `ui_designer` / `ux_laoge` 做 UI 布局和可读性；
- 替代 `steam_indie_appraiser` 判断 Steam 第一眼吸引力；
- 替代 `game_producer` 判断角色资产量、人月、外包和里程碑风险；
- 自行改写 `角色设计风格规范-AI包`、`design/art-direction/angus-visual-style-guide.md` 或其它真源。

### UI Designer

适合：

- 从 UI brief / 需求文字生成元素对照表；
- 桌面 16:9 wireframe / mock；
- 控件清单、布局分区、低保真视觉方案；
- 输出给 UX 老哥的设计意图和约束摘要。

不适合：

- 评审现有界面截图；
- P0/P1/P2、认知负荷、操作链硬伤诊断；
- 直接改 HTML / Godot 代码；
- 默认设计移动端或触屏版。

### UX 老哥

适合：

- UI / 交互硬伤；
- P0/P1/P2；
- 遮挡、空间安全区、状态噪音；
- 操作链和玩家误读；
- 桌面 16:9 截图验收。

不适合：

- 判断 Steam 小爆款潜力；
- 研究竞品销量和商店页；
- 直接生成美术图；
- 直接改代码，除非用户明确要求。

### Steam 独立游戏鉴赏师

适合：

- Steam 第一眼吸引力；
- 小爆款感、职业幻想、可截图产物、动作钩子；
- 功能 ROI；
- 内容包 / 垂直切片 / Steam 首屏；
- 竞品样本和近期待借鉴游戏。

不适合：

- 逐像素 UI 遮挡审计；
- 直接决定最终交互布局；
- 直接改代码或生图；
- 在没有来源时声称“最新 Steam 情况”。

## 7. 本轮已形成的案例库入口

- UX：`skills/ux-diagnosis/references/casebook/`
- SIA：`skills/steam-indie-appraiser/references/casebook/`
- Game Producer：`skills/game-producer/references/casebook/`
- Game System Architect：`skills/game-sys-architect/references/casebook/`
- Game Numerical：`skills/game-numerical/references/casebook/`
- Game Logic Check：`skills/game-logic-check/references/casebook/`
- Angus Art Director：`skills/angus-art-director/references/casebook/`
- Angus Character Pixel Director：`skills/angus-character-pixel-director/references/casebook/`

后续每次有值得复用的实战判断，优先补一条 casebook。只有达到升级门槛，再改 `SKILL.md`、方法论文档或 `AGENTS.md`。

## 8. 冷备冻结与解冻提醒（2026-07-08 起）

### 冻结状态表

2026-07-08 的 agent 体系评审确认：以下四个 subagent 自导入（2026-06-05）以来在 onboarding 路由文档之外没有真实使用记录，转入冷备冻结。

| Agent | 状态 | 冻结日期 | 解冻日期 |
| --- | --- | --- | --- |
| `game_producer` | 冷备冻结 | 2026-07-08 | — |
| `game_sys_architect` | 冷备冻结 | 2026-07-08 | — |
| `game_numerical` | 冷备冻结 | 2026-07-08 | — |
| `game_logic_check` | 冷备冻结 | 2026-07-08 | — |

### 冻结含义

- 保留 `.codex/agents/*.toml` 注册壳与 `skills/` 技能目录，随时可用。
- 用户显式触发词（`@制作人`、`@系统架构`、`@数值策划`、`@逻辑审查`）调用时仍正常执行，不需要先走解冻流程；但 AI 应在执行时顺带提醒该 agent 处于冷备，并询问是否正式解冻。
- 冻结期间不再为这四个 agent 投入维护：不新增规则、不扩写 SKILL.md、不补 references / casebook、不做能力校准。
- AI 不主动 spawn 它们参与常规任务链路（UI 双 agent 链、美术守门链等不受影响）。

### 解冻提醒义务（硬规则）

用户明确表示自己无法判断解冻时机，且可能忘记冻结这件事。因此 AI（父级 Codex / 任何后续会话）在任务中识别到下列价值窗口时，**必须当场主动提醒用户**，不得默默替代该 agent 职责而不提醒，也不得等用户自己想起：

| 冷备 agent | 解冻触发条件（命中任一即提醒） |
| --- | --- |
| `game_producer` | 用户讨论要不要做某个大功能、立项 / 砍范围 / 里程碑 / 熔断、项目方向变化；或 AI 自检发现范围膨胀、工期风险、系统增殖失控迹象 |
| `game_sys_architect` | 要新增玩法系统或长期玩法层、准备更新 `design/gdd/systems-index.md`、多系统耦合冲突、资源流产消不清 |
| `game_numerical` | 玩法数值调校启动：达标率、概率校准、任务目标值、黑骰反噬、周压力、发刊结算数值、势力 / 宏观属性参数、配表或平衡验证 |
| `game_logic_check` | 规则 / 状态机 / 配表 / 剧情时间线成形并准备实现前；或原型出现重复结算、流程卡死、exploit、状态永久锁死类问题 |

提醒格式：一句话说明命中了哪个触发条件 + 建议解冻哪个 agent + 不解冻时的替代方案（通常是父级在当前线程按对应 `SKILL.md` 执行同等流程，但不做能力沉淀）。是否解冻由用户决定；用户未回应时按替代方案继续当前任务，不算解冻。

### 解冻流程

1. 用户明确同意解冻后，更新本节冻结状态表（填解冻日期）。
2. 同步修订 `AGENTS.md` 的「冷备 subagent 冻结与解冻提醒顶层规则」条目，把该 agent 从冷备名单移除。
3. 恢复该 agent 的正常维护投入；首次实战使用后按 §4 格式补一条 casebook，再按 §5 门槛决定是否校准 SKILL.md。
