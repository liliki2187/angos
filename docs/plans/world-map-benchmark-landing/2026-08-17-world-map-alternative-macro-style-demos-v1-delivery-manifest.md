# 世界地图三套宏观风格演示 v1 交付清单

## 结论

已使用 Codex 内置 ImageGen 从空白画布分别生成三张配对的 `1920×1080` filled-state 宏观风格演示：

- A：本期折页特刊；
- B：夜班剪版台；
- C：蓝光校片灯箱。

三张冻结相同三栏职责、真实地区内容、新闻图、Disclosure、CTA 与 Schedule 事实，只改变主媒介、组件家族、材料与灯光。当前状态为 `three_macro_style_demos_ready / pending_user_selection`，不是 exact rect、功能合同、生产资产或 Godot 通过证据。

2026-08-17 用户已完成方向裁决：A 折页特刊因杂志成品不应成为本界面主媒介而淘汰；C 蓝光校片灯箱因过于科幻而淘汰；B 夜班剪版台保留并进入内部路线深化。当前状态修订为 `night_newsroom_pasteup_selected / A_and_C_rejected`。

## 交付物

- `image_gen/2026-08-17/world-map-alternative-macro-style-demos-v1/01-gatefold-weekly-1920x1080.png`
- `image_gen/2026-08-17/world-map-alternative-macro-style-demos-v1/02-night-newsroom-paste-up-desk-1920x1080.png`
- `image_gen/2026-08-17/world-map-alternative-macro-style-demos-v1/03-acetate-light-table-1920x1080.png`
- `image_gen/2026-08-17/world-map-alternative-macro-style-demos-v1/04-three-direction-comparison-board-1920x500.png`

三张模型原始结果均为 `1672×941`；程序只做高质量无裁切规格化为 `1920×1080`。三联板只做等比排版和标题，不替代生图。

## 共享生成约束

```text
同一 1920×1080 桌面三栏责任区；左侧三张同规格 RegionCard 与只读 Schedule；中央世界地图和三个地区锚点；右侧北美主稿、69:44 新闻图、Disclosure、现场记录和唯一 CTA。三张左图槽同规格，北美左图与右图保持同一构图。功能正面 0°，不新增控件或热区。

clean low-poly weekly；深夜海军蓝、钴蓝、冷青、橄榄、芥末、暖白与少量锈红；现代纸品和宽块面；禁止 SCP、军情雷达、CASE FILE、Eye、锁、靶标、旅行明信片、泛黄旧档案、写实摄影、像素和半调。
```

## 三套核心提示词

### A｜本期折页特刊

```text
整屏必须是一份横向展开的 World Mystery Weekly 特刊。左卡是折页内的蓝 / 橄榄 / 芥末栏目封签；中央地图是一张连续跨页；右侧主稿是夹入右折页的独立插页；Schedule 是刊尾抽出的截稿回条。遮掉文字后仍先读成一本打开的怪新闻特刊，不得读成文件夹围绕地图。禁止旅行杂志、地图册、文件袋和档案案卷。
```

### B｜夜班剪版台

```text
整屏必须是编辑正在制作本周版面的现代剪版台。左卡是同规格选题稿条；中央是大地图底稿＋一张主照片＋粗标题条＋来源条；右侧是模块化送印拼版；Schedule 是送版票。所有松散稿件服从清楚的列网和基线。禁止证据墙、红线、图钉网络、随机拼贴和数字控制台。
```

### C｜蓝光校片灯箱

```text
整屏必须是一张实体磨砂冷青校片灯箱。左卡是综合色透明校片框＋不透明文字 / 图片条；中央地图由两到三层透明分色套片构成；右栏是完全不透明的钴蓝主编板；Schedule 是压住灯箱边缘的芥末实体截稿卡。透明度只属于无字地图套片，所有功能文字与图片必须在不透明载体上。禁止实验室、X 光室、情报灯箱、HUD、扫描线和玻璃 UI。
```

## 双审结果

### 共识

- 三条路线确实改变了主媒介，不是换色或增加批注。
- A 折页特刊排名第一：周刊品牌最强、左中右职责最完整、与 SCP 距离最大。
- 三张都不能直接升格；02 / 03 locked-but-previewable 语义、Schedule 分层、精确 `69:44` 和动态安全区仍需后续证明。

### UI Designer

- 排序：A > C > B。
- A 的连续刊物轮廓、综合色章节和主稿插页最值得保留。
- B 中央大照片＋大标题很有效，但硬框、网格和三角地图仍偏数字工作站。
- C 的透明套片与冷暖灯光最独特，但必须降低实验室、金属器材和机构剪贴板感。

### UX 老哥

- 排序：A > B > C。
- A 是唯一遮字后仍能凭大载体直接读成“周刊”的路线。
- B 有明确编辑动作，但中央地图职责被大照片和标题削弱。
- C 首读更像法证 / 情报分析灯箱，三栏边界也因共用灯箱而变弱。

## 当前边界

- 用户本轮只需选择整体方向或指定混合关系。
- 不从三张图回裁生产组件。
- 不进入透明化、atlas、manifest、Godot 或 `WeeklyRunGame`。
