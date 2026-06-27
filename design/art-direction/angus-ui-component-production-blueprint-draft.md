# Angus UI 组件风格转译生产草案

> 状态：工作草案，供 UI 出稿、生图提示词、切图验收和运行时 UI 落地使用。  
> 关系：不替代 `design/art-direction/angus-visual-style-guide.md` 与 `design/gdd/`。若本草案被正式采纳，应再同步到对应视觉真源或 UI 生产文档。  
> 核心原则：美术标杆不是再做一张相似风格板，而是把 Angus 的真实界面组件转译成“现代异常周刊编辑部”的可生产物件。

## 0. 标杆相似度硬闸门

组件落地不能以牺牲标杆 DNA 为代价。若一张图只是更像“干净的可玩 UI”，但第一眼不像用户给出的标杆，它仍然失败。

生成或评审任何“标杆转 UI”的图前，必须逐项对照：

| 标杆 DNA | 必须保留 | 常见跑偏 |
| --- | --- | --- |
| 画面组织 | 高密度编辑部资产板、纸件叠层、照片 / 贴纸 / 文件夹 / 图标共同组织 | 单一地图 + 单一侧栏的普通策略 UI |
| 主物件尺度 | 大周刊封面、大 dossier、大照片、大文件夹能成为视觉锚点 | 所有东西缩成面板和小卡片 |
| 材质比例 | 深色底板 + 干净米白纸 + 橄榄绿 / 芥末黄文件夹 + 少量蓝绿信号 | 过度灰蓝、过度黑、过度红橙 |
| 低多边形语言 | 快照、场景、怪异物件、图标边缘都带块面感 | 只在地图上低多边形，其他元素写实或扁平 |
| 周刊品牌感 | 大胆标题块、刊号、条码、裁切线、色票、图标系统作为图形语言 | 为了禁文字而完全丢掉版式冲击 |
| 物件密度 | 回形针、夹子、便签、贴纸、文件夹、CD / 照片等形成可触摸的桌面资产感 | 只剩纸面、边框和 UI 线条 |
| 纸张气质 | 干净现代纸件，轻微印刷感 | 泛黄旧档案、复古报纸、温馨木桌 |

如果目标是可玩 UI 底稿，应采用“标杆资产板的局部被玩家操作化”的思路，而不是把标杆抽象成普通 `left list / center map / right panel`。  
UI 安全区可以通过空白纸面、遮盖条、贴纸边缘和未印刷区域解决；不能为了安全区把画面做成低密度表单。

## 0.5 大块低多边形与微细节闸门

2026-06-24 世界地图组件母版复审确认：新的标杆威力来自**大块概括的低多边形 / 手绘裁纸感 / 形状经济**，不是来自密集三角网、孔洞、条码、微线和摄影噪声。

追加纠偏：标杆并不依赖“重质感”。纸张、照片、山体、文件夹和图标的质感主要由**低多边形色块的深浅关系**、硬边阴影、冷暖色块和压层关系产生，而不是纸纹、脏点、刮痕、细孔、微线或高清摄影颗粒。后续 prompt 和验收应先追问：去掉纹理噪声后，物件是否仍靠大块色面成立。

后续生成或评审世界地图、地区卡、dossier 快照、票条、ticker、图标 atlas 时，必须先过以下检查：

| 检查项 | 通过标准 | 失败表现 |
| --- | --- | --- |
| 低多边形块面 | 主图形优先用少量大面表达；场景 / 地图 / 快照在缩小后仍能读出 8-20 个主要块面 | 大陆和照片被切成密集三角网，读成 GIS / 雷达终端纹理 |
| 色块塑形 | 质感由大色块明度、冷暖分区、硬边阴影和压层产生；一个物体先有大剪影，再用 3-8 个明暗面塑造 | 用纸纹、雾气、噪点、刮痕、摄影颗粒和细线补“高级感” |
| 手绘概括感 | 轮廓和切面可以轻微不规则，像被概括过的纸面 / 插图 | 写实海岸线、小岛、雷达细节、摄影雾气和高清纹理主导 |
| 微细节预算 | 小孔、条码、短刻度、点阵、刮痕、微线同一组件最多保留一种，且服务结构或状态 | 票据孔洞、条码、半调点、纸边、阴影、短线同时竞争 |
| 半调方式 | 半调应成片、成块、成方向地出现，用于阴影、危险区、扫描区 | 芝麻点、纸脏点、随机噪声、摄影颗粒 |
| 文字安全区 | 可写区干净，不能有孔洞、斜纹、强半调或纹理穿过 | 文本槽被装饰线、孔洞、点阵、强纸纹压住 |

Prompt 正向必须倾向：

```text
large simplified low-poly planes, bold blocky polygon shapes, editorial cut-paper graphic design, slightly hand-drawn imperfect polygon edges, halftone as large structured patches, minimal micro-detail, strong negative space
texture through polygon value blocks, large flat shaded planes, graphic hand-drawn abstraction
```

Prompt 负向必须写死：

```text
no dense triangulation mesh, no tiny polygon web, no small holes, no barcode clutter, no scattered speckle noise, no photographic grain, no GIS terminal map detail, no overly detailed coastlines, no decorative micro-lines, no texture covering text areas
no texture-heavy rendering, no paper grain as detail, no surface scratches, no many tiny UI marks
```

验收口径：缩到 25% 预览时，应先看到大块地图 / 文件 / 票据剪影，而不是细线、孔洞、点和条码；100% 局部看时，半调必须是块状结构，文字区必须干净。

## 1. 转译公式

每个 UI 组件必须同时回答五件事：

| 维度 | 必须明确 |
| --- | --- |
| 玩法职责 | 玩家在这里判断什么、点击什么、承担什么后果 |
| 物件隐喻 | 它在编辑部世界里是什么物件，而不是抽象 UI 框 |
| 动态承载 | 哪些文字、数字、状态、按钮文案由运行时 UI 渲染 |
| 美术承载 | 哪些纸张、照片、贴纸、夹子、半调、低多边形图像可以做成 bitmap / atlas |
| 禁止烘死 | 哪些中文、数值、按钮、长标题、可点击状态绝不能被生图写死 |

标杆提供的是视觉语言：深蓝黑主场、低多边形异常快照、现代周刊图形设计、档案夹和桌面物件、干净纸面、少量绿蓝扫描信号、红橙危险 / 主 CTA。  
Angus 的界面仍必须先服务信息层级、可读性和决策路径。

## 2. 高频组件词表

| Angus 组件 | 风格包装 | 生产重点 | 不要做成 |
| --- | --- | --- | --- |
| 全局背景 / 主舞台 | 夜间编辑部品牌黑板、印刷定位板 | 保留深蓝黑负空间，给面板留清晰边界 | 纯科幻终端、旧档案黄纸墙 |
| 顶部 HUD | 本期周刊刊号 + 编辑部状态条 | 周数、天数、资源、压力是 UI 文本 | 大标题海报、装饰性 logo 区 |
| 世界地图 | 全球异常频道板 / 低多边形地图桌 | 地区、pin、红线、可进入状态分层 | 只是一张漂亮地图 |
| 地区索引卡 | 文件夹标签 / 地区短签 | selected / warning / locked 明确 | 普通网页列表 |
| 地图 pin | 图钉、频道锚点、贴纸 | normal / hover / selected / locked / warning atlas | 发光手游图标 |
| 右侧地区详情 | 当前案件 dossier 首页 | 先做 content rect，再做纸面纹理 | 旧档案页、满屏手写字 |
| 地区快照 | 低多边形异常照片 / CRT 截帧 | 只承载图像，不承载 UI 文案 | 带文字说明的生成图 |
| 任务卡 | story pitch 文件夹 / 短案件条 | 标题、时长、风险、奖励动态排版 | 卡牌游戏式稀有度卡 |
| 任务详情 | 周刊选题 brief / dossier front page | 目标、骰面、需求、后果分区 | 视觉小说对话框 |
| 主 CTA | 红橙签批票条 / 盖章动作 / 印刷按钮 | hover、pressed、disabled 必须有差异 | 泛用圆角按钮、霓虹按钮 |
| 推进一天 | 日历撕页 / 编辑部排期机 | 与进入地区 CTA 分级，不能抢主线 | 另一个同级红按钮 |
| 角色卡 | 记者证 / field pass / 编辑胸牌 | 高清微像素角色头像，文本清爽 | 低清 8-bit 头像 |
| 候选抽屉 | 桌面卡片抽屉 / dossier tray | 可拖拽、可筛选、可比较 | 卡牌牌库皮肤 |
| 派遣主舞台 | 任务 dossier 桌面签批场 | 空槽、已放入角色、装备格清楚 | 只有漂亮桌面没有操作层 |
| 右侧签批单 | 主编签字纸 / 出勤回执 | 覆盖率、风险、预计结果动态文本 | 装饰报纸 |
| 骰子 / 检定 | 印刷校验票 / field feedback ticket | 成功率、黑骰、反噬要读得快 | 玄学符号动画遮挡数字 |
| 报道 / 发刊 | 打开的厚周刊 / 版位台 | 稿件排版、版位优先级、发刊动作 | 纯报纸编辑器模拟 |
| 势力压力 | 来函、禁令、赞助商贴纸、威胁印章 | 来源、期限、影响范围明确 | 无法区分来源的红戳 |
| 宏观属性 | 周刊立场仪表 / 读者反馈条 | 变化趋势比装饰更重要 | SaaS 仪表盘 |
| 日志 / ticker | 新闻走字条 / 编辑部回执 | 最新事件可扫读 | 纯氛围字幕 |
| 弹窗 / 确认 | 主编签批纸 / 最后校样 | 后果、取消、确认清楚 | 遮挡一切的美术纸张 |

## 3. 第一优先竖切：世界地图右侧地区详情

目标：验证“标杆风格能服务真实 UI”，而不是验证整屏好不好看。  
建议先只做一个地区：北美禁区，红线升温，可进入。

### 3.1 物件隐喻

右侧详情不是普通信息面板，而是一张夹在世界地图旁的“当前地区 dossier 首页”。  
它由干净纸面、顶部夹子、地区低多边形快照、状态贴纸、短标签和底部红橙行动票条组成。

### 3.2 动态字段

| 字段 | 示例 | 运行时属性 |
| --- | --- | --- |
| `region_name` | 北美禁区 | 文本，不烘死 |
| `region_status` | 红线升温 | 文本 + 状态色 |
| `cycle_label` | 探索周 01 / 剩余 5 天 | 文本 |
| `visible_task_count` | 可见任务 3 | 文本 / 数字 |
| `entry_cost` | 消耗 1 天 | 文本 / 数字 |
| `reward_window` | 收益窗口 3 天 | 文本 / 数字 |
| `risk_tags` | 失真、封锁、监听 | 动态标签 |
| `cta_label` | 进入地区 | 按钮文案，不烘死 |

### 3.3 区域合同

以下坐标为 16:9 桌面布局下的相对约束，供生图和 UI 出稿使用，不是最终像素值。

| 区域 | 建议范围 | 说明 |
| --- | --- | --- |
| `title_rect` | 右侧面板上方 8%-18% | 地区名 + 状态贴纸，背景必须干净 |
| `snapshot_rect` | 右侧面板 20%-45% | 低多边形地区快照，不放文字数字 |
| `meta_rect` | 右侧面板 48%-60% | 周期、收益窗口、进入消耗 |
| `task_summary_rect` | 右侧面板 62%-75% | 可见任务、风险标签、短描述 |
| `cta_rect` | 右侧面板 80%-91% | 红橙主 CTA，文字由 UI 渲染 |
| `no_text_rects` | 夹子、折角、快照主体、贴纸边缘、条码、半调重区 | 禁止放正文 |
| `hit_rects` | CTA、地区卡、地图 pin、底部入口 | 视觉边界和点击边界必须一致 |

### 3.4 状态矩阵

| 状态 | 美术差异 | UI 差异 |
| --- | --- | --- |
| default | 干净纸面，弱投影，绿色 / 蓝绿信号少量出现 | 可读基础信息 |
| hover CTA | 票条轻微抬起，边缘亮 1-2px | 鼠标提示进入 |
| pressed CTA | 票条轻微下压，投影变短 | 触发进入 |
| selected region | dossier 与地图 pin 有同色扫描线关联 | 地区名和 pin 同步高亮 |
| warning | 红橙贴纸 / 斜纹 / 危险章增强 | 风险信息前置 |
| locked | 纸面去饱和，CTA 变灰橄榄 | 明确锁定原因 |
| disabled CTA | 去红色，文字仍清晰 | 不可点击且说明原因 |

### 3.5 生图提示词骨架

不要再写“style guide / reference board / visual direction poster”。主语必须是具体可玩 UI 底稿。

```text
A playable desktop 16:9 game UI background for the Angus world map right-region dossier component, no readable text, no labels, no numbers. 
The right side is a clean modern dossier front page pinned beside a dark navy low-poly world map board. 
Reserve blank content rectangles for dynamic UI text: title at top, meta rows in the middle, task summary below, and a large bottom red-orange action ticket button with no baked text. 
Include a low-poly anomalous regional snapshot frame, paper tabs, small stickers, barcode-like unreadable marks, crop marks, subtle halftone, blue-green scanning signal, and one red-orange CTA asset. 
Modern weekly magazine editorial design, clean paper surfaces, deep navy black background, olive/blue-green signal accents, warm off-white paper, restrained red-orange danger accent.
Avoid mood board, style guide sheet, poster labels, readable typography, old yellow archive paper, cozy wood desk, generic sci-fi terminal, mobile UI, ornate decoration, horror gore, and any baked Chinese or English UI text.
```

## 4. 第二优先竖切：地区任务卡 + 任务详情

目标：把“任务选择”变成周刊编辑部的选题选择，而不是普通任务列表。

### 4.1 任务卡

| 项目 | 设计 |
| --- | --- |
| 物件隐喻 | story pitch 文件夹、短案件条、被夹住的照片索引 |
| 动态字段 | 任务标题、地点、耗时、需求角色、风险、奖励、截止状态 |
| 美术资产 | 文件夹底、索引标签、低多边形小缩略图框、风险贴纸、回形针 |
| 禁止烘死 | 标题、数字、奖励、需求、CTA |

状态：default / hover / selected / locked / expired / urgent / completed。  
`urgent` 才允许红橙占比升高；普通任务卡不要都做红。

### 4.2 任务详情

任务详情应像“选题 brief / dossier front page”，左侧为任务快照和标题层级，右侧为派遣条件、角色需求、收益风险、进入派遣 CTA。  
低多边形图像只负责情绪和识别，不负责讲完全部任务文本。

推荐区域：

| 区域 | 说明 |
| --- | --- |
| `brief_title_rect` | 大标题，2 行以内 |
| `image_rect` | 低多边形任务快照，无文字 |
| `requirements_rect` | 角色、技能、装备、耗时 |
| `risk_reward_rect` | 奖励和反噬并列 |
| `dispatch_cta_rect` | 进入派遣，主 CTA |

## 5. 第三优先竖切：派遣签批主舞台

目标：让玩家一眼知道“我正在把记者和装备签批到某个任务里”，并能看懂成功率、覆盖率和风险变化。

### 5.1 组件结构

| 区块 | 风格包装 | 关键要求 |
| --- | --- | --- |
| 中央任务 dossier | 桌面上的任务签批文件 | 任务名、目标、需求槽位清晰 |
| 角色槽 | 记者证插槽 / 胸牌位 | 空槽、已放入、不可用、推荐态清楚 |
| 装备槽 | 小证物袋 / 工具票夹 | 与角色槽视觉区分 |
| 候选列表 | 卡片抽屉 / field pass tray | 可比较，不抢中央 |
| 右侧签批单 | 主编回执 / 覆盖率票据 | 成功率、风险、预计后果最醒目 |
| 底部 CTA | 红橙签批票条 / 盖章按钮 | 确认派遣是唯一主动作 |

### 5.2 状态矩阵

| 状态 | 视觉规则 |
| --- | --- |
| empty slot | 干净虚线框 + 弱图标，不用强红 |
| valid drag-over | 蓝绿色扫描边 |
| invalid drag-over | 红橙短警示边 + 原因提示 |
| assigned | 角色证件压入槽内，有轻投影 |
| recommended | 小号橄榄 / 蓝绿贴纸，不替代数值判断 |
| risk rising | 右侧签批单出现红橙印章和斜纹 |
| ready | 底部确认票条升为主视觉 |
| blocked | 确认票条去饱和，并显示缺失条件 |

### 5.3 美术边界

角色头像使用角色真源的高清微像素 Q 版风格；界面纸张、插槽、票据仍保持现代图形设计。  
不要把整个派遣界面做成像素游戏，也不要把成功率、角色能力和风险数字做进贴图。

## 6. 报道 / 发刊页方向

这一页适合更强地使用“周刊成品”的视觉隐喻，但仍然不是旧报纸模拟器。

| 组件 | 风格包装 | 动态重点 |
| --- | --- | --- |
| 版位 | 打开的厚周刊版面网格 | 稿件优先级、可拖放、空位 |
| 稿件 | 文章文件夹 / 小样纸条 | 标题、影响、风险、主题 |
| 发刊 CTA | 印刷机开关 / 最终盖章 | 不可逆动作要醒目 |
| 发行反馈 | 读者反馈条 / 销量回执 / 势力回函 | 变化原因可追溯 |

发刊页可以有更强的纸面、半调和套印，但正文区域仍必须干净，中文标题不能被纹理压坏。

## 7. 横向材质规则

| 材质 | 应该出现在哪里 | 不应该出现在哪里 |
| --- | --- | --- |
| 低多边形 | 地区快照、任务照片、封面图、异常物件、地图大形 | 长正文区、按钮文字底下、所有小图标 |
| 半调 / 套印 | 插图边缘、周刊图片、状态章、纸张局部 | 正文、数值、CTA 文案下方 |
| 像素颗粒 | 角色、远景城市、异常粒子、图标边缘、信号损伤 | 全 UI、所有字体、按钮主体 |
| 纸张 | dossier、任务卡、签批单、回执、文件夹 | 整屏泛黄背景 |
| 红橙 | 主 CTA、危险、不可逆、红线升温 | 普通装饰、所有选中态 |
| 绿 / 蓝绿 | 扫描、信号、神秘线索、可连接关系 | 普通成功按钮大面积铺色 |

## 8. 交付检查表

每个组件或生图结果交付时，至少要附上：

1. `bitmap_assets`：哪些是固定图层、底图、纸面、照片、贴纸、按钮底。
2. `runtime_ui`：哪些文字、数字、按钮文案、状态图标由 UI 渲染。
3. `content_rects`：动态文本和数字可放的位置。
4. `no_text_rects`：美术强纹理、图像、折角、夹子、半调禁写区域。
5. `hit_rects`：点击 / hover / drag 的真实交互范围。
6. `state_matrix`：default、hover、selected、warning、disabled 等状态差异。
7. `rejection_risks`：是否滑向旧档案、泛黄旧报纸、纯科幻终端、泛桌面拼贴、全像素游戏或装饰过量。

如果一个图只有气氛，没有这些合同，它只能作为灵感草稿，不能作为生产标杆。

## 9. 界面替换生产链

后续替换真实界面时，不建议从“整屏重做”开始。整屏 prompt 会天然把标杆稀释成普通 UI 布局，尤其容易变成 `left list / center board / right panel`。  
推荐按下面六步走：

### 9.1 先冻结功能骨架

先截当前可玩页面，只做功能标注，不讨论风格：

| 标注 | 内容 |
| --- | --- |
| `primary_decision` | 玩家这一屏主要决定什么 |
| `primary_action` | 唯一主按钮是什么 |
| `secondary_actions` | 次级动作有哪些 |
| `must_read_fields` | 3 秒内必须读到的文字 / 数字 |
| `optional_fields` | 可以弱化或折叠的信息 |
| `interaction_rects` | 真实点击、hover、拖拽区域 |

这一步的目标是保护玩法职责，避免为了贴近标杆新增不存在的功能。

### 9.2 再做标杆母版，不做运行时 UI

第二步只做“标杆组件母版板”，类似 `angus-ui-component-style-guide-v2-imagegen.png`。  
母版里放真实组件样本：地区 dossier、任务卡、角色证、签批单、骰子校验票、发刊文件夹、CTA 状态、icon atlas、色票材质。

母版必须先过标杆相似度硬闸门：

- 第一眼像用户给的标杆，而不是干净后台 UI。
- 资产板密度、纸件叠层、文件夹色系、贴纸 / 夹子 / 快照 / 色票都在。
- 大组件能看出 Angus 功能身份，不只是泛参考物件。
- 没有被模型写死的重要中文、数字和按钮文案。

### 9.3 从母版抽单组件，而不是从整屏裁

通过母版后，每次只抽一个组件做生产切片：

| 优先级 | 组件切片 | 原因 |
| --- | --- | --- |
| P0 | 右侧地区 dossier | 最能验证地区选择到进入地区的主链 |
| P0 | 任务 pitch card | 高频出现，直接影响任务选择 |
| P0 | 主 CTA / 状态票条 atlas | 决定整个游戏的行动语法 |
| P1 | 角色 field pass | 连接角色真源与 UI 包装 |
| P1 | 派遣签批 slip | 验证复杂数字与拟物纸件能否共存 |
| P1 | icon / sticker atlas | 统一小状态和导航语言 |
| P2 | 发刊 folder / report layout | 影响阶段高潮，但可以稍后 |

不要先切全屏背景。全屏背景最后做，因为它会掩盖组件是否真的成立。

### 9.4 每个组件先做三张图

每个组件都按三张图交付：

1. **无字 bitmap 底图**：只有纸张、照片、贴纸、夹子、按钮底，不含真实文案。
2. **安全区 overlay**：标出 `content_rects / no_text_rects / hit_rects`。
3. **真实中文填充预览**：用当前游戏真实字段填进去，验证最长中文、数字和状态。

这三张都过了，才允许进入 atlas / Godot / HTML 替换。

### 9.5 运行时替换只替组件皮肤

工程侧第一次替换时，尽量只换组件皮肤，不改信息结构：

- 保留原页面的数据流、按钮逻辑、状态机。
- 用新 bitmap / atlas 替换底板、卡片、贴纸、按钮底。
- 文本、数字、按钮 label 仍由运行时 UI 渲染。
- hover / selected / disabled / warning 用状态贴图或 shader 叠层实现。
- 不在第一轮同时重排所有页面。

这样可以判断问题到底来自美术资源、文字安全区，还是原本 UX 结构。

### 9.6 最后再做整屏融合

当 3-5 个核心组件稳定后，再做整屏融合：

- 背景主舞台统一成深蓝黑编辑部底板。
- 文件夹、纸件、贴纸和快照的尺度统一。
- 全局 HUD、ticker、弹窗、CTA 共享同一套 atlas 语言。
- 删除临时面板和重复边框。
- 用真实桌面 16:9 截图验收，而不是只看生图。

## 10. 页面替换顺序

### 10.1 世界地图页

先替：

1. 右侧地区 dossier。
2. 地区索引卡。
3. 地图 pin / sticker atlas。
4. 主 CTA 票条。

后替：

1. 地图大底图。
2. 全局 HUD。
3. 底部日程 / ticker。

原因：世界地图页的标杆味主要来自“地图旁的 dossier 和文件夹物件”，不是地图本身。

### 10.2 地区任务页

先替：

1. 任务 pitch card。
2. 任务详情 brief。
3. 风险 / 奖励 / 截止贴纸。
4. 进入派遣 CTA。

后替：

1. 地区背景。
2. 次级筛选和排序。

原因：任务选择是高频扫读页面，任务卡必须先证明可读。

### 10.3 派遣签批页

先替：

1. 角色 field pass。
2. 空槽 / 已放入槽。
3. 右侧签批 slip。
4. 主确认 CTA。

后替：

1. 中央桌面 / dossier 主舞台。
2. 候选抽屉底板。
3. 复杂动效。

原因：派遣页信息复杂，不能先上大氛围图；必须先保证角色、槽位和签批数字可读。

### 10.4 报道 / 发刊页

先替：

1. 稿件 card / 小样纸条。
2. 版位 grid。
3. 发刊 CTA。
4. 发行反馈 slip。

后替：

1. 大周刊封面。
2. 印刷机 / 出刊动效。

原因：发刊页最容易做成旧报纸；先用现代周刊版位和红橙印刷动作锁住方向。

## 11. 组件替换合同模板

每次替换一个组件，按这个格式写清楚：

```md
组件名：
所在页面：
当前功能职责：
标杆物件身份：

必须保留的标杆 DNA：
- 纸件 / 文件夹 / 快照 / 贴纸 / 夹子 / 色票 / 图标中哪些必须出现
- 主色比例
- 半调 / 低多边形 / 像素颗粒出现位置

bitmap_assets：
- 固定底图：
- 状态贴图：
- icon / sticker：

runtime_ui：
- 标题：
- 数字：
- 状态：
- 按钮 label：

content_rects：
- ...

no_text_rects：
- ...

hit_rects：
- ...

state_matrix：
- default：
- hover：
- selected：
- warning：
- disabled：

验收：
- 第一眼是否像标杆：
- 中文最长态是否可读：
- 红橙是否只用于主行动 / 危险：
- 是否滑向普通面板：
```

## 12. Prompt 写法

### 12.1 推荐写法

主语必须是“标杆组件母版”或“某个真实组件”，不要写泛泛的 UI。

```text
Generate an Angus UI component production board, in the same visual-density family as the benchmark: dark navy editorial board, layered paper dossiers, olive and mustard folders, low-poly snapshots, stickers, paper clips, barcode marks, icon atlas, color swatches, and bold modern weekly-magazine graphic design.

The board must show real Angus game UI component specimens: region dossier, task pitch card, character field pass, dispatch signoff slip, dice verification ticket, report publishing folder, CTA state atlas, and map pin / sticker icon atlas.

Keep important dynamic text areas blank or represented by abstract placeholder bars. Do not create a clean playable map screen, dashboard, SaaS panel, or ordinary strategy UI.
```

### 12.2 禁止写法

这些写法会稀释标杆：

- `make the current UI in this style`
- `clean game UI with dossier panel`
- `world map with left list and right info panel`
- `dark mystery dashboard`
- `paper archive interface`
- `cyberpunk investigation terminal`
- `minimal modern UI`

### 12.3 修正方向

如果生成结果不像标杆，不要先说“更像 Angus / 更高级”。要明确加回：

- 高密度资产板。
- 大纸件和文件夹叠层。
- 橄榄绿、芥末黄、米白、蓝文件套。
- 贴纸、夹子、色票、CD、条码、图标 atlas。
- 低多边形快照分布在多个组件里。
- 粗体周刊版式和图形符号系统。

如果结果可读性差，再通过 `content_rects` 和组件切片解决，不要直接把画面降成普通面板。
