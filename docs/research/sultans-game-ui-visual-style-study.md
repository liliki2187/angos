# 《苏丹的游戏》界面视觉风格研究

> **状态**：外部参考研究 / 视觉风格拆解  
> **创建时间**：2026-06-17  
> **用途**：总结《Sultan's Game / 苏丹的游戏》的界面视觉语言，供后续 AI 生成风格稿、UI 资源、卡牌、面板、图标和装饰件时参考。  
> **边界**：本文不是 Angus GDD 真源，不是 Angus 正式美术方向采纳记录，也不授权复制《苏丹的游戏》的 IP、角色、卡名、UI 框体、构图或具体文本。

配套风格稿图：[`docs/research/sultans-game-ui-style-board/01-sultans-game-ui-style-board.png`](./sultans-game-ui-style-board/01-sultans-game-ui-style-board.png)

---

## 0. 证据来源

本地 Steam 截图样本：

- `D:\angos\docs\research\steam-first-eye-assets\batch-02\screenshots\3117820-0.jpg`
- `D:\angos\docs\research\steam-first-eye-assets\batch-02\screenshots\3117820-1.jpg`
- `D:\angos\docs\research\steam-first-eye-assets\batch-02\screenshots\3117820-2.jpg`
- `D:\angos\docs\research\steam-first-eye-assets\batch-02\screenshots\3117820-3.jpg`

网页公开参考：

- Steam 商店页：<https://store.steampowered.com/app/3117820/_/>
- Steam 公共截图和商店简介。
- 巴哈姆特、PC Gamer、Keymailer 等公开截图，用于补充宫廷事件面板、地图、角色卡、难度选择等界面观察。

核心判断：它值得学的不是“中东花纹贴皮”，而是**所有 UI 层都像同一个桌面游戏世界里的实体物件**。地图是织锦毯，卡牌是手牌，事件是黑色羊皮纸/宫廷告示，按钮是黄铜仪式盘，资源是徽章/钱币/吊坠。

---

## 1. 一句话风格公式

**黑暗宫廷桌游 + 红色织锦地图 + 旧金铜丝花边 + 手绘塔罗卡牌 + 黑羊皮纸文本面板 + 机械仪式圆盘。**

玩家看到的不是抽象面板，而是一张危险宫廷游戏铺在桌上：手里有牌，桌上有地图，右下有推进时间的黄铜仪器，弹出的说明像宫廷告示或仪式文书。

---

## 2. 屏幕大结构

大多数玩法截图有稳定构图：

- **顶部压力条**：处刑日 / 当前天数 / 资源徽章，细、长、带装饰，负责压迫感。
- **中央舞台**：红色织锦地图、宫廷内景、浴场、事件场景或角色详情。
- **底部手牌**：横向一排卡牌，是最主要的可操作资源池。
- **右下主动作**：巨大的圆形 `End Day / Next / 下一天` 物件，视觉权重大于普通按钮。
- **浮动详情面板**：黑绿底、旧金框、羊皮纸/告示板质感，承载长文本和决策。
- **左侧边缘物件**：骷髅助手牌、竖向工具/提示栈，让屏幕更像一张桌面边缘，而不是全屏后台。

它的高密度不乱，是因为锚点非常少且稳定：顶部管压力，底部管手牌，右下管推进，中央管当前对象，文本永远落在黑金面板上。

---

## 3. 用色系统

### 3.1 主色表

以下是近似工作色，不是精确取样：

| 角色 | 色值 | 用途 |
| --- | --- | --- |
| 深织锦红 | `#5A1713` / `#741E16` | 地图底、宫廷压迫、危险氛围 |
| 黑绿近黑 | `#07100D` / `#101610` | 长文本底、阴影、按钮凹槽 |
| 旧金 / 黄铜 | `#A77A2A` / `#C7A64D` | 边框、徽章、金币、标题牌 |
| 旧象牙白 | `#D8C99A` / `#E6D9B0` | 卡纸、羊皮纸高光、标签文字 |
| 脏橄榄阴影 | `#3B3A20` | 做旧、金属锈色、纸面污痕 |
| 去饱和孔雀绿 | `#1E5D57` / `#2D7770` | 孔雀、灯具、水面、宫廷点缀 |
| 暗青金石蓝 | `#263D66` / `#344D83` | 宫殿瓷砖、冷色卡牌、夜色对比 |
| 毒性旧绿 | `#6C8B45` | 秘密、荒野、异术、诡异卡牌 |
| 骨白 | `#C8C4A9` | 骷髅、线稿、旧纸文字 |

### 3.2 用色规则

- 红色是**世界表面**，不是单纯警示色；它承担地图、织物、宫廷压迫。
- 金色是**边缘和仪式金属**，不要大面积铺满；主要用于边框、徽章、硬币、圆盘。
- 黑色是**阅读底**，长文本、事件说明、决策文字都要落在平静黑绿底上。
- 蓝、绿、紫只做卡牌类别、宫廷内景和小面积宝石/瓷砖点缀。
- 白色必须是旧象牙或骨白，不用干净 SaaS 白。

---

## 4. 线条与形状

### 4.1 线条

- 主轮廓像手绘墨线，线宽不完全均匀，有轻微抖动、飞白、套印感。
- 金属边线通常是双层/三层：外金边、内暗槽、小珠点或小缺口。
- 地图路径用点线、虚线、珠链、脚印/沙路，不用干净折线。
- 卡牌边缘和属性图标有细小尖角、缺口、花边、锯齿和卷草。
- 装饰线不追求几何精确，而追求“被印刷/雕刻/磨损过”的手感。

### 4.2 形状

优先使用：

- 尖拱、宫廷拱、贝壳形/花瓣形拱顶；
- 悬挂徽章、圆形印玺、钟表/星盘/罗盘；
- 竖向塔罗卡轮廓；
- 卷轴杆、细竹竿式边框；
- 地毯边、织锦条、蕾丝角花；
- 黑色药丸按钮嵌在旧金花边里。

避免一眼能读成普通矩形面板。程序布局可以是矩形，但可见视觉对象应读成卡、毯、告示、铭牌、器械或羊皮纸。

---

## 5. 材质系统

主要材质：

- **织锦 / 地毯**：深红底、几何/花纹暗纹、织线颗粒、较暗边带。
- **黑羊皮纸 / 烟熏告示板**：黑绿底，轻微云状污痕，足够安静可放长文。
- **旧黄铜 / 旧金**：边缘磨亮、暗处有锈、局部浮雕，不像新金属。
- **旧卡纸**：象牙、灰蓝、毒绿、脏红、黑纸，边角磨损、油墨脏边。
- **珐琅 / 宝石点缀**：孔雀绿、青金石蓝、暗红小珠，少量发亮。
- **暗木桌面**：几乎黑棕，只作为边缘环境，不抢主体。
- **骨 / 骷髅**：骨白图标或助手，提供黑色幽默和死亡压力。

材质密度分配：

- 地毯、宫殿、边框可以密。
- 文字承载面必须相对安静。
- 卡牌可以旧、脏、有纹理，但标题条、数值章和图标位必须清楚。
- 禁止把高频织锦花纹直接压在小字下面。

---

## 6. 组件拆解

### 6.1 地图板

地图不是羊皮纸地图，而是**红色织锦毯上的路线图**。

需要：

- 深红织物底；
- 地毯边框；
- 地点像织上去/画上去的小建筑、小剪影；
- 路线像沙路、珠链或刺绣线；
- 地点标签是小黑金铭牌，像钉在毯子上的牌子。

避免：干净奇幻羊皮纸、卫星地图、现代 pin、Google Map 标签、霓虹路线。

### 6.2 卡牌

卡牌是最重要的可复用资产。

需要：

- 竖向塔罗比例；
- 厚装饰边框；
- 顶部小标题牌；
- 中央手绘人物/物品插画；
- 底部费用、阶级或资源章；
- 金、绿、蓝灰、象牙、脏红、黑等类别纸；
- 旧角、脏边、印刷颗粒；
- 小图标槽和戳印数值。

卡牌插画要能在小尺寸读清轮廓；可以神秘、危险、宫廷化，但不能变成高清摄影或手游抽卡立绘。

### 6.3 事件 / 详情面板

事件面板像一个**黑色阅读神龛**。

需要：

- 黑绿烟熏内底；
- 旧金/象牙复杂边框；
- 标题牌嵌在上框；
- 侧边竖向小图标列；
- 底部黑金决策按钮；
- 宫廷拱门、帘幕或告示板轮廓。

它不能像网页 modal。它应像宫廷告示、雕刻铭板、黑羊皮纸或仪式说明牌。

### 6.4 主按钮

右下 `End Day / Next / 下一天` 是**时间仪式器械**，不是普通 CTA。

需要：

- 圆形印玺、钟表、罗盘、星盘或黄铜盘；
- 厚金边；
- 中央黑色或雕刻凹槽；
- 文字居中，强对比；
- 周边有小环、珠链、金属脚、孔雀/藤蔓装饰；
- 永远处在视觉流程终点。

次级按钮可以是小黑金药丸，但推进回合的主动作必须是一个实体器物。

### 6.5 属性图标

属性图标像宫廷小印章：

- 方形/圆角小框；
- 中央剪影图标；
- 旧金或象牙边；
- 背后是低饱和类别色；
- 数字像戳印或铭刻。

避免通用 RPG 图标包、明亮手游品质框、干净线性 icon。

---

## 7. 装饰母题

高价值母题：

- 红色波斯 / 中亚地毯边；
- 宫廷尖拱、花瓣拱、贝壳拱；
- 镂空窗格、格栅；
- 吊灯、油灯、烛台；
- 孔雀；
- 钱币、珠串、吊坠、徽章；
- 星盘、罗盘、钟表、齿轮圆盘；
- 卷草花边、蕾丝角花；
- 卷轴杆、悬挂布帘；
- 骷髅助手牌；
- 棕榈、沙漠动物、商队路线；
- 旧书、卷轴、契约纸；
- 小黑金地名牌。

这些母题必须有功能：做地图边、面板框、按钮器械、卡牌类别或状态锚点。不要只铺成背景墙纸。

---

## 8. 角色与插画

角色风格：

- 手绘故事书 / 塔罗插画感；
- 暗色粗轮廓；
- 身形略拉长，姿态有戏剧性；
- 五官表达清楚但不过度写实；
- 服装靠图案、平涂阴影和边线表现；
- 解剖不是重点，轮廓和身份更重要；
- 色彩旧、低饱和，偶尔用宝石色点亮。

卡牌插画：

- 像印在卡纸上的微型画，不像概念设定图；
- 背景简化，保证小尺寸轮廓；
- 质感来自纸和油墨，不靠高清笔刷噪点；
- 卡牌类别色、数值章和图标位不能被插画抢掉。

避免：二游抽卡精修、干净矢量吉祥物、写实摄影、3D 渲染、过甜童话插画、血腥恐怖细节。

---

## 9. 字体与文本面

字体气质：

- 英文标题偏装饰 serif / fantasy display；
- 中文可转译为装饰宋、刻印感宋体、略书法但可读的标题字；
- 正文用紧凑高可读宋体/印刷字体；
- 数字像铭刻或戳印，不像电子 LED；
- 小标签写在黑金铭牌或旧纸条上。

生成可复用 bitmap 资产时：

- 不要烘焙真实 UI 文本；
- 留出平整、低噪、横平竖直的黑底或旧纸内容区；
- 花边、织锦纹、角花必须退出未来文本安全区；
- 标题牌可以留空，交给引擎后续渲染。

---

## 10. AI 生成提示词

### 10.1 大风格稿 prompt

```text
Create a 16:9 visual style board for an original dark court tabletop card RPG interface. Use the visual language of a dangerous palace game laid on a red brocade carpet: deep crimson woven map board, tarnished brass filigree, blackened parchment reading panels, hand-painted tarot-like cards, court medallion icons, scalloped palace arches, hanging lamps, peacock accents, dotted caravan map paths, and a large circular ritual time button.

The board should include: a red textile map board sample, 6 vertical card templates with worn paper and ornate borders, a black parchment event panel with gold frame and blank text-safe zones, a circular End Day / Next style button as a brass clock or astrolabe, small attribute seal icons, location label plaques, rug border samples, palace arch frame samples, and material swatches for brocade, black parchment, tarnished gold, old ivory card paper, teal enamel, lapis tile, poison green card paper, and bone-white ink.

Linework: uneven hand-inked contours, printed miniature illustration, tarnished metallic edges, small ornamental beads, scallops, notches, and filigree corners. Dense decoration on borders and textiles, calm flat dark surfaces for long text.

Mood: opulent, oppressive, strategic, ritualized, dark fantasy court intrigue, tabletop resource management, dangerous but elegant. It should feel like a physical game board and card set, not a modern software dashboard.

No readable text, no existing game names, no copied characters, no copied card names, no exact Sultan's Game UI layout, no logos, no watermark.
```

### 10.2 组件资源 prompt

```text
Create original UI asset components for a dark court tabletop card RPG. Components: blank event panel, card frames, location label plaques, attribute seal icons, circular day-advance button, small black-gold decision buttons, red brocade map border strips, palace arch frame, and material swatches.

All components must share one material grammar: deep crimson woven textile, blackened parchment, tarnished brass filigree, old ivory paper, muted teal enamel, lapis tile, poison green paper, bone-white ink. Use uneven hand-inked outlines, worn printed texture, rubbed gold edges, and clear blank text-safe rectangles. Avoid clean vector UI, modern glass panels, neon, mobile game rarity frames, generic fantasy parchment, exact IP copying, and baked readable text.
```

### 10.3 卡牌模板 prompt

```text
Design a set of original vertical tarot-like resource cards for a dark palace intrigue tabletop RPG. Each card has a worn paper face, tarnished brass or ink border, top title plaque left blank, central hand-painted miniature illustration area, bottom cost/rank seal, tiny attribute icon slots, dirty corners, and aged print texture. Use category papers: gold coin paper, green secret paper, blue-gray court paper, ivory character paper, black curse paper, muted red danger paper. Keep silhouettes readable at small card size. No readable text, no copied game symbols, no glossy gacha finish.
```

### 10.4 面板模板 prompt

```text
Create a blank ornate event panel for a dark court tabletop RPG. The panel is blackened parchment with smoky green-black texture, tarnished brass filigree frame, scalloped palace arch top, small blank title plaque, side column for three small seal icons, and bottom row for three black-gold decision buttons. Leave a large quiet text-safe rectangle in the middle. Dense ornament only on frame and corners. No readable text, no logos, no watermark.
```

---

## 11. 负面约束

生成时避免：

- 现代 SaaS 卡片、玻璃面板、霓虹描边、全息 HUD；
- 干净扁平矢量 UI；
- 普通奇幻羊皮纸地图；
- 亮闪手游品质框；
- 二游抽卡质感；
- 3D 金币 / 3D 按钮；
- 写实宫殿摄影；
- 只有棕黄旧纸，没有红织锦和黑金仪式物件；
- 过量米黄 / 棕黄导致泛旧档案化；
- 复制《苏丹的游戏》的地图、角色、卡牌、卡名、苏丹卡符号、按钮布局或具体文本；
- 动态文本底下有密集花纹；
- 花边侵入内容安全区；
- 生成图里烘焙伪中文、伪英文；
- 血腥、湿润恐怖、生理解剖、真实暴力细节。

---

## 12. 对 Angus 可迁移的部分

不要把中东宫廷主题直接搬到 Angus。可学的是界面方法：

- UI 先像真实工作台/物件系统，再像面板；
- 主动作要有强实体锚点；
- 卡牌要像压在桌上的义务/资源，而不是装饰标签；
- 长文本必须落在安静高对比材质上；
- 装饰丰富度放在边、角、承载物和器械上；
- 固定屏幕语法：顶部压力、中央工作对象、底部库存、右侧主动作；
- 少量材质规则重复使用，使高密度界面仍然统一。

可转译方向：

- 红织锦地图 -> 现代印刷杂志 / 全球频道地图板；
- 宫廷卡牌 -> 报道卡、任务卡、证据卡；
- 黑羊皮纸面板 -> 编辑部档案 / 暗色播报通知；
- 旧金仪式圆盘 -> 送印 / 发刊 / 频道切入器械；
- 宫廷徽章 -> 周刊印章、频道章、信号徽章；
- 商队点线路径 -> 调查路线 / 媒体传播轨迹。

不可迁移：

- 一千零一夜 / 苏丹 / 处刑题材；
- 情欲、暴力、宫廷猎奇内容；
- 精确卡框造型；
- 精确右下圆形 `End Day` 器械；
- 把红地毯设为 Angus 默认大背景。

---

## 13. 通过标准

生成结果“对味”的信号：

- 2 秒内读成实体桌游 / 宫廷物件系统；
- 红织锦、黑羊皮纸、旧金三角成立；
- 卡、面板、图标、按钮共享同一套材质语法；
- 主动作是强实体器械，不是普通按钮；
- 文本安全区安静、宽裕；
- 装饰母题都有功能，不是墙纸；
- 卡面插画像印刷微型画，不像二游精修；
- 整体气质华丽、压迫、策略化、仪式化。

失败信号：

- 看起来像普通奇幻 RPG HUD；
- 只是羊皮纸加金边；
- 变成后台仪表盘；
- 复制原游戏具体 UI 或命名内容；
- 烘焙了大量假文本；
- 没有给真实 UI 文本预留可读区域。
