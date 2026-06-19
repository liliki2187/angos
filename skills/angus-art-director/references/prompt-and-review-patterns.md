# 评审与 Prompt 模板

> 用途：供 `angus-art-director` 输出稳定、可交接的风格评审、参考转译和生图 prompt。

## 1. 快速风格审查模板

```md
美术指导判断｜<对象名>

结论：通过 / 有条件通过 / 跑偏 / 与真源冲突

证据：
- <截图或 prompt 中的具体观察>
- <与 Angus 风格真源的对应关系>

Angus 三关：
- 色彩：通过 / 风险 / 不通过，原因……
- 情绪：通过 / 风险 / 不通过，原因……
- 混合比例：通过 / 风险 / 不通过，原因……

5 维评审：
- 摄影感：...
- 版式感：...
- 物件叙事：...
- 品牌系统：...
- 克制留白：...

优先改法：
1. ...
2. ...
3. ...

不要做：
- ...

交接：
- 给 UI Designer：...
- 给 UX 老哥：...
- 给 SIA / 制作人 / 生图工具：...
```

## 2. 参考图转译模板

```md
参考转译｜<参考名>

可学习的不是：
- <表层风格或 Angus 禁区>

真正可迁移的是：
1. <具体手法> -> Angus 中用于 <对象 / 页面 / 资产>
2. <具体手法> -> Angus 中用于 <对象 / 页面 / 资产>

Angus 不适用部分：
- <原因必须对应色彩、情绪或混合比例>

推荐实验：
- 低成本验证：...
- 需要用户确认：...
```

## 3. 生图 Prompt Bundle 模板

```md
用途：<key-art / ui-screen / card-art / prop / texture / icon>
画幅：<16:9 / 3:4 / 1:1 / 透明 PNG>
主物件：<只保留 1-2 个视觉主语>
场景 / 构图：<镜头、焦点、负空间>
风格：cinematic game UI mockup, bold modern editorial graphic design
色彩：deep navy #0F1A2E, vivid red-orange #E84B2C, warm paper #F5EDD8
材质：printed matter, halftone, crop marks, subtle misregistration, pixel particles
像素范围：角色为高清微像素 Q 版；城市剪影 / 粒子 / 半调 / 信号噪点作为环境与材质层
角色范围：high-definition micro-pixel chibi characters matching `角色设计风格规范-AI包/reference/01-原始基准图.png`
情绪：cool, confident, urgent, black humor, supernatural weekly magazine
负面约束：no warm wooden desk, no yellowed archive, no low-resolution 8-bit pixel art, no voxel characters, no 3D metallic gradient, no generic mobile game buttons, no neon cyberpunk hologram
验收：<小尺寸 / 局部裁切 / 文案安全区 / 可读性>
```

## 4. 生成后验收清单

### 整体

- 是否第一眼像《世界未解之谜周刊》，而不是普通探案、旧报纸、视觉小说、纯恐怖或普通报社经营？
- 是否有一个明确主物件，不是碎纸、印章、符号、蓝光互相抢注意？
- 缩小时是否仍能读出主物件和品牌色？

### 风格

- 主色是否仍是深蓝 + 红橙 + 米白，而不是灰褐旧纸？
- 角色是否符合四人标杆图的高清微像素密度、Q 版比例和低能量怪谈表情？
- UI、字体和正文是否仍保持现代图形设计，而不是低清复古像素界面？
- 是否保留现代图形设计的排版自信？
- 像素颗粒是否是有意的 2-4px 方块簇、块状半调、套印错位和清晰图形边缘，而不是高清摄影噪点、细碎纸脏或随机旧化纹理？
- 半调 / 像素 / 套印是否已经成为界面结构语言，而不是只贴在角落里的装饰样本？

### 标杆资格

- 若用户希望将结果作为生产标杆、资源标杆或真源候选：是否已经生成后复审，而不是只审过 prompt？
- 是否能明确说出它继承了哪个项目标杆图的配色、颗粒、线条、负空间和功能承载方式？
- 未通过标杆资格时，必须标注为“元素词汇草稿 / 偏差案例 / 灵感图”，不得称为资源生产标准。

### 世界地图 / 全球频道专项

- 默认对照 `docs/screenshots/2026-06-07-global-channel-style-board/05-global-channel-style-board-reference-clean-modern-pixel.png` 和 `docs/screenshots/2026-06-07-global-channel-style-board/07-global-channel-full-interface-style-draft-flat-magazine-ui.png`。
- 地图应是低细节、现代、图形化的世界频道 / 世界选题墙，不是写实旧地图、旧档案墙、泛黄纸堆或高密度地理细节。
- `docs/screenshots/2026-06-11-world-map-ui-style-sheet/01-world-map-ui-style-sheet.png` 只能作为元素词汇草稿与偏差案例：组件类型可参考，但像素颗粒度、旧纸噪点、旧档案倾向不通过生产标杆。

### UI / 文字

- 动态文字是否应由 DOM / Godot UI 渲染，而不是被生图烙死？
- 纸纹、折线、半调颗粒是否穿过正文？
- CTA 是否像场景动作或印刷动作，而不是通用圆角按钮？

### 禁区

- 暖木桌、台灯、泛黄历史纸张。
- 灰银金属和 3D 渐变按钮。
- 全息霓虹、玻璃面板、赛博终端。
- 手游素材包按钮和胶囊 chip。
- 写实厚重旧档案。

## 5. 与其它 agent 的交接句

### 给 UI Designer

说明视觉主语、材质 token、色彩预算、不要动的风格边界，让 UI Designer 转成布局和组件 spec。

### 给 UX 老哥

说明哪些风格元素可能影响可读性、点击判断、文字安全区或状态误读，让 UX 老哥做玩家视角验收。

### 给 SIA

说明风格是否符合 Angus，但不判断 Steam 卖相；请 SIA 继续判断第一眼吸引力、类型误读和竞品旁排。

### 给 OpenRouter Image Gen

传入 prompt bundle、负面约束、参考图路径、输出用途和验收清单。不要让生图工具自由扩写成旧档案或全像素。
