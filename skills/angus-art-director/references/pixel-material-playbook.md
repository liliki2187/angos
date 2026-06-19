# 像素 / 半调 / 印刷材质方法库

> 用途：供 `angus-art-director` 在分析像素风参考、指导视觉 prompt、拆解可迁移美术手法时使用。

## 1. 高级像素风判断

高级不等于精细。高级是像素在执行明确设计意图，并与整个视觉系统保持一致。

5 个判断维度：

1. 摄影感：构图、焦点、影调、负空间是否成立。
2. 版式感：文字层级、排版和信息结构是否自信。
3. 物件叙事：每个物件是否有存在理由。
4. 品牌系统：跨界面的视觉语言是否统一。
5. 克制留白：删掉 20% 是否更好。

## 2. 像素可扮演的角色

| 角色 | 可借鉴项目 | Angus 用法 |
| --- | --- | --- |
| 氛围材质 | `NORCO`、`Animal Well` | 城市远景、天际线、异常粒子、信号噪点 |
| 信息载体 | `Papers, Please`、`Golden Idol` | 文件、证据、报道版面自身成为玩法承载 |
| 物件叙事工具 | `Eastward`、`Backbone` | 桌面物件、纸件、印章、剪报承担状态和故事 |
| 品牌视觉身份 | `SIGNALIS`、`Katana ZERO` | 高对比配色、警示色、工业 / 编辑字体系统 |
| 印刷 / 信号隐喻 | `Animal Well`、Angus | 半调网点、套印错位、扫描线、像素遮罩 |

## 3. 标杆拆解

- `NORCO`：日常空间加一度异常；学习氛围材质和地方感，不学习灰土慢节奏。
- `The Drifter`：粗颗粒仍有电影镜头；学习镜头感，不把粗糙当复古。
- `Golden Idol`：画面即证据板；学习视觉服务功能。
- `SIGNALIS`：像素、低多边形、警告色、工业字体统一；学习品牌系统。
- `Animal Well`：限色和动态光照产生层次；学习少量颜色制造丰富变化。
- `REPLACED`：像素、3D、景深、电影光；学习混合媒介的高级感。
- `Eastward`：像素与光照混合；学习高密度小触感。
- `Papers, Please` / `Republia Times`：工作台即玩法；学习文件即操作对象。
- `Pentiment`：字体即身份；学习编辑设计思维进入游戏规则。

## 4. Angus 可用的 7 种像素材质

1. **像素城市剪影**：放在底边、窗外或地图远景，作为氛围层。
2. **像素粒子扩散**：从实体边缘有方向地脱落，表达信息传播、现实解体或异常污染。
3. **半调网点纹理**：用于报道图、周刊插图、纸面主图，表达印刷感。
4. **扫描线 / 干扰条**：偶尔闪过，表达信号异常；不能常驻到干扰阅读。
5. **色差偏移**：红蓝通道微偏 1-2px，表达印刷对版错误；只用于少量焦点元素。
6. **像素化遮罩**：大像素块遮蔽未解锁信息或异常污染区域。
7. **裁切标记**：四角十字、套印标记、刊号、报价，表达印刷品身份。

## 5. 高级感来源

- 高纯度主色对撞，而不是随机深蓝配红。
- 重要物件尺度戏剧化，例如报纸、签批夹或印刷按钮成为画面主物件。
- 粒子和纹理有方向性，不是随机噪点；像素颗粒应读作有意的 2-4px 方块簇、块状半调、套印错位和图形边缘，而不是高清摄影噪声或细碎旧纸脏污。
- 排版自信，标题敢占空间，负空间有意图。
- 混合精度成立：高清角色 / 图形设计与像素材质都做得精，不互相降级。
- 印刷隐喻贯穿：半调、裁切、错印、刊号、报价、纸边服务同一品牌。

## 6. 常见 prompt 坑

- 只写 `pixel art`：模型容易跑成 8-bit、FC、Pico-8 或全界面低清像素。角色 prompt 必须写清“高清微像素 Q 版角色，并以四人标杆图为像素密度锚”。
- 只写 `flat`：模型容易变廉价扁平色块。
- 写 `desk / workspace`：模型容易生成暖光木桌和温馨办公室。
- 写 `newspaper archive`：模型容易生成旧档案、灰褐纸和历史案件。
- 写 `cyberpunk UI`：模型容易生成霓虹全息和玻璃面板。

## 7. 稳定 prompt 片段

可按任务组合使用：

- `cinematic game UI mockup, bold modern editorial graphic design`
- `deep navy #0F1A2E and vivid red-orange #E84B2C extreme contrast`
- `high-definition micro-pixel chibi characters matching the four-character benchmark image`
- `pixel art texture for city silhouettes, particles, halftone texture and signal noise`
- `fresh supernatural weekly magazine, not vintage archive, not cozy desk`
- `same visual density as surrounding elements`
- `printed matter materiality, halftone dots, crop marks, subtle misregistration`

负面约束必须具体写出：

- `no warm wooden desk`
- `no yellowed old paper archive`
- `no low-resolution 8-bit or voxel characters`
- `no 3D metallic gradient`
- `no generic mobile game buttons`
- `no neon holographic cyberpunk panel`
