# 世界地图怪新闻周刊品牌语义目标稿 v1 交付清单

## 结论

`02-full-screen-filled-state-brand-shift-clean-1920x1080.png` 曾通过只读语义与静态功能回归，但 2026-08-17 用户指出其视觉差异主要仍是小批注装饰，未改变组件样式与整屏氛围。UX 老哥与 UI Designer 随即撤回“品牌方向通过”结论：本图降级为 `semantic_copy_and_annotation_proof / macro_style_fail`，不得再作为方向确认稿。

本图只证明“怪新闻周刊编辑部”品牌身份、综合色彩、板块内容与静态功能语义方向；不证明 exact rect、真实资源路径、动态文字安全区、运行时状态切换、热区、透明拆件或 Godot 接线。

## 交付物

- `image_gen/2026-08-17/world-map-weekly-brand-semantic-target-v1/01-full-screen-filled-state-brand-shift-target-1920x1080.png`
  - 第一轮品牌转向成图。
  - 因回流 `剩余 7 天`、selected / warning 混色、Schedule 伪按钮与右栏伪正文，只保留为修订前诊断稿。
- `image_gen/2026-08-17/world-map-weekly-brand-semantic-target-v1/02-full-screen-filled-state-brand-shift-clean-1920x1080.png`
  - 只保留为周刊文案、批注语气与静态状态分离证明；宏观风格 Gate 失败。
  - Codex 内置 ImageGen 生成；模型原始结果为 `1672×941`，程序只做高质量无裁切规格化到 `1920×1080`，未重绘组件、图像或文字。

## 输入真源与权限

- A291：整体平衡、WMW 刊头锁组、地图与编辑材料同场、约 10% 纸层厚度。
- `benchmark-board-01.png / benchmark-board-02.png`：clean low-poly、现代纸品、色板、夹具与完成度；其中 `TOP SECRET / CASE FILE / radar / archive` 不作为叙事身份真值。
- A305 / A306：三栏、RegionCard 统一规格、`69:44` 图片槽、locked 可预览、Disclosure、CTA 与输入合同。
- A296：删除 `最早截止：第4天`、`截稿倒计时7天` 与 `剩余7天`；只保留正式任务摘要中的 `限时 1`。

## 主要视觉转译

1. 左栏从权限目录改为三份不同来源的地区线报，出版编号与故事钩子取代 Eye、锁章和 `REGION FILE`。
2. 中央从异常监控地图改为地图定位底板＋本周选题编辑簇；01 独占照片、候选标题、来源纸与批注，02 / 03 退为简短来源签。
3. 右栏从 `CASE FILE` 权威案卷改为 `NEWS LEAD / 本期主稿候选`，并以可读现场记录关闭伪正文。
4. selected 改由钴蓝背页、蓝勾与蓝色引线承担；warning 继续由锈红 `红线升温` 独立承担。
5. Schedule 只保留当前日与阶段说明，日历图标降为只读印刷图示。

## 最终提示词（结构化记录）

### 主生成

```text
生成完整 1920×1080 桌面三栏 World Mystery Weekly filled-state UI。
以当前真实 UI 冻结三栏、RegionCard / Map / Dossier / Schedule、Disclosure、CTA、统一 69:44 图片槽；以 A291 决定平衡、刊头和纸层；以两张 clean-low-poly weekly benchmark 决定现代纸品、宽块低多边形、深夜海军蓝＋冷青＋暖白＋橄榄＋芥末＋锈红及完成度。

把第一视觉主语从“异常管理机构”改为“成年人认真编辑怪新闻的周刊”：顶部为 WMW 刊头；左栏为三份地区线报；中央为地图定位底板与北美选题编辑簇；右栏为 NEWS LEAD / 本期主稿候选；Schedule 为只读截稿附件。用候选标题、来源纸、主编批注、校样意见形成克制黑色幽默。

禁止 CASE FILE、TOP SECRET、CONFIDENTIAL、Eye 跨栏重复、大锁、雷达、围捕红圈、监控网格、军事 / SCP / 国安身份、泛黄旧档案、摄影写实、像素 / 半调、细碎伪写实三角面、移动端和新增热区。
```

### 定点清稿

```text
保持首图整屏构图与美术不动，只关闭功能语义问题：
1. 删除“剩余7天 / 第4天 / 倒计时”，Schedule 只保留当前第1天与选题会尚未开始；日历改为无按钮暗示的印刷图示。
2. selected 使用钴蓝 / 冷青，warning 仅使用锈红；三卡与 69:44 图片槽零位移。
3. 02 / 03 降低照片对比，以“线索不足”编辑搁置签表达可预览但未就绪，不使用锁、Eye 或权限章。
4. 中央 02 / 03 改为短小记者来源签；01 继续独占照片、候选标题与批注簇。
5. 右栏模糊伪正文改为可读“现场记录”：00:40 三台滚筒同时停转；02:15 潮线仍保持水平；店主坚持昨夜没有下雨。Disclosure 与 CTA 不动。
```

## 双审结果

### UX 老哥

- 五秒身份 Gate 通过；自然首读为“本周选题墙 / 怪新闻编辑桌 / 主稿候选版面”。
- 时间字段回流、Schedule 伪按钮、selected / warning 混色、locked 过软和伪正文五项 P1 均已关闭。
- `P0=0 / P1=0 / P2=2`：Schedule 方形日历仍有极轻控件感；中央来源签不重复 locked 状态，需在未来交互中验证预览后 CTA disabled 的理解。

### UI Designer

- 左栏、中央、右栏均已重做板块本体，不是对旧 SCP 界面增加纸件装饰。
- 品牌趣味、现代综合色彩、纸物接触、clean low-poly 与功能承载面均通过方向 Gate。
- 无阻断 P1；P2 为 `现场记录` 可后续改成更出版化的 `取材记录`、中央虚线仍略像流程线、地图块面仍略碎及三卡回形针重复。

## 继续阻断

- 不从本整屏回裁生产组件。
- 不进入透明化、exact rect 量测、atlas、manifest、Godot 或 `WeeklyRunGame`。
- 用户确认方向后，下一步应先做无字 / 可拆层组件定义与严格状态矩阵，而不是继续堆叠整屏装饰。
