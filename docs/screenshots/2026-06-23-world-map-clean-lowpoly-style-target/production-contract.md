# B7 世界地图 · 新标杆风格生产合同

> 本目录用于把用户确认的图3/图4“干净低多边形周刊风格标杆”转译到 B7 世界地图界面。  
> 当前产物是 **屏幕级风格目标 + 安全区 overlay**，不是 runtime UI，也不是最终切图母版。

## 当前产物

- `01-no-text-fullscreen-style-target.png`：无字整屏风格目标图。
- `02-content-rects-overlay.png`：基于目标图标注的动态文字区 / 禁写区。
- `03-v2-no-text-fullscreen-style-target.png`：v2 无字整屏风格目标图，目标是补强图3/图4的品牌符号层、结构化半调和红橙纸品 CTA，同时保持具体 B7 世界地图界面职责。
- `04-v2-content-rects-overlay.png`：v2 动态文字区 / 禁写区 overlay。
- `05-v2-filled-state-text-mock.png`：v2 真实中文填充验证稿，使用“北美禁区 selected + 红线升温 + 可进入”单状态检查文本承载。
- `06-v2-filled-right-dossier-crop.png` 至 `10-v2-filled-bottom-tools-crop.png`：v2 关键局部裁切。
- `11-v2-1-filled-state-text-mock.png`：吸收 UI Designer / UX 老哥复审后的 v2.1 填充验证稿。
- `12-v2-1-filled-right-dossier-crop.png` 至 `17-v2-1-filled-schedule-crop.png`：v2.1 关键局部裁切。
- `30-v2-2-3-clean-right-function.png`：按用户反馈移除右下无功能小按钮组后的 v2.2.3 填充验证稿；释放空间归还给右侧当前地区功能。
- `31-v2-2-3-clean-right-function-crop.png`：v2.2.3 右侧地区 dossier 裁切。
- `32-v2-2-3-clean-right-action-crop.png`：v2.2.3 右下行动确认 / 进入地区 CTA 裁切。
- `33-v2-2-3-full-bottom-crop.png`：v2.2.3 底部整体裁切，用于检查左下日程、底部入口和右侧行动确认不互抢。

## v2 生成边界

2026-06-24 的两张中间失败图暴露出一个明确边界：提示词里如果过度强调 `brand system / visual direction / style guide`，模型会把目标做成风格板、参考板或品牌手册，而不是具体可玩界面。后续 prompt 必须把主语锁定为 **一张可玩的 B7 世界地图无字界面底稿**。

后续生成禁止：

- style guide sheet。
- art reference board。
- mood board。
- visual direction poster。
- brand manual。
- sample grid / thumbnail studies。
- 巨大标题字、章节标题和可读说明文字。

允许的品牌符号只能作为界面内部的小型图形层出现，例如地球符号、WMW 风格 monogram、眼睛、警示三角、裁切标、伪条码、低多边形快照编号和不可读刊号块。它们不能抢走地图、地区列表、右侧 dossier 和 CTA 的界面职责。

v2 仍不是生产标杆；它是进入 `filled-state text mock` 前的候选基准。若 v2 复审通过，下一步才填真实中文状态；若复审指出 CTA、纸面比例或品牌符号层仍不达标，应先重出 v2.1 无字稿。

## v2 / v2.1 复审结论

`@像素艺术` 复审结论：v2 **有条件通过**，可以进入 filled-state text mock，不需要继续空图微调；但不能称为生产标杆。原因是像素 / 半调结构、CTA 动作层和真实文字安全区仍需填字验证。

UI Designer 复审结论：v2 filled mock **可以进入组件拆解，但不能直接 runtime 替换**；优先做右侧 dossier vertical slice。中央 pin、右侧 CTA、推进一天模块仍需要安全区重定义或重出资产。

UX 老哥复审结论：无严格 P0，但有三个 P1：

1. 左侧“北美禁区”、中央 `B7` pin、右侧“北美禁区”三端对象对应不够硬。
2. 左下 `推进一天` 与右侧 `进入北美禁区` 都在底部形成强动作，需要降权和作用域区分。
3. CTA、左侧卡顶部 chip 和 pin 仍有“控件盒通过但视觉安全区风险”。

v2.1 已做的修正：

- 页面标题从 `B7 世界地图` 改为 `世界地图`，避免 `B7` 同时像地图编号和地区编号。
- 全局 chips 移到顶部全局 strip，不再压入左侧选中地区卡。
- 中央选中 pin 改为 `B7 北美`，建立左卡 / 地图 / 右栏三端对应。
- 右侧 CTA 只保留主动作 `进入北美禁区`，不再叠加说明文字。
- 左下 `推进一天` 降权为全局日程控件，并用低权重 `+1` 仪表块覆盖底图中原有强箭头。

v2.2.3 已做的修正：

- 删除右下角无确认功能的小按钮 / icon strip，不再为了填空加入候选工具。
- 右侧 dossier 向下获得更多空间，新增 `当前地区任务` 预览区，用于承载选中地区的可见任务和收益 / 消耗摘要。
- `进入北美禁区` 保留为右侧唯一主 CTA，放入独立 `行动确认` 票据中；右下不再出现第二组小工具或装饰按钮。
- v2.2 / v2.2.1 / v2.2.2 是过程文件：v2.2 有 CTA 残影，v2.2.1 有编码导致的中文问号，v2.2.2 有底部小字裁切；对外引用以 v2.2.3 为准。

仍需在组件拆解中处理：

- v2 底图里的非选中 pin 白色纸签已经烙在无字图里，filled mock 不能真正删除；正式资产需要重出 `wm-pin-clean-atlas`，常态只显示 pin + 短 code，选中 / hover 才展开纸签。
- `wm-global-schedule-clean` 需要重出无强箭头版本，避免与右侧 CTA 共用“下一步”语法。
- `wm-cta-enter-region-clean` 需要独立拆出文字槽、箭头、准星、斜纹、螺丝和底壳；箭头与装饰必须列为 `no_text_rects`。

## 定位

这张目标图解决的是：“B7 世界地图如果接上图3/图4新标杆，整体应该长什么样。”

它不解决：

- 组件状态矩阵。
- 真实中文文案排版。
- Godot / HTML 运行时布局。
- 低多边形地图、右侧 snapshot、按钮等组件的最终切图细节。

## 生产顺序

### 1. 屏幕级风格稿

先确认整屏气质是否成立，再拆组件。验收点：

- 深蓝主场是否成立。
- 低多边形是否成为统一图形语言，而不只是地图特效。
- 纸张、文件夹、贴纸、照片和按钮是否更干净，少旧档案脏噪。
- 红橙是否收束到危险 / 主 CTA，不再全屏泛滥。
- 绿色 / 蓝绿色是否承担神秘信号和扫描语义。

### 2. 安全区合同

所有后续组件必须同时输出：

- `content_rects`：动态文字、数值、按钮文案可放区域。
- `no_text_rects`：图片、夹子、折角、色签主体、贴纸、强半调、纸边、装饰边。
- `hit_rects`：可点击区域，和视觉按钮必须一致。
- `state_matrix`：default / hover / selected / disabled / warning 等状态。

### 3. 组件拆解

从整屏目标稿中拆组件，不凭空另起风格。

| 组件 | 用途 | 需要状态 | 优先级 |
| --- | --- | --- | --- |
| `wm-map-board-clean-lowpoly` | 中央世界地图主舞台 | default / selected-region / hover-pin / locked-pin | P0 |
| `wm-right-dossier-clean` | 右侧选中地区详情纸夹 | default / locked-region / warning-region | P0 |
| `wm-region-snapshot-lowpoly` | 右侧地区图样 | per-region variants, image-only | P0 |
| `wm-cta-enter-region-clean` | 进入地区主 CTA | default / hover / pressed / disabled | P0 |
| `wm-left-region-card-clean` | 左侧地区索引卡 | normal / selected / locked / warning | P0 |
| `wm-pin-clean-atlas` | 地图 pin | normal / selected / locked / warning / hover | P1 |
| `wm-bottom-folder-tab-clean` | 底部辅助入口 | normal / warning / info / disabled | P1 |
| `wm-global-schedule-clean` | 左下推进一天 | default / confirm / disabled | P1 |
| `wm-status-sticker-clean` | 红线、可进入、锁定、推荐等小标签 | red / cyan / olive / gold / disabled | P2 |

### 3.1 右下无功能按钮规则

右下角不得为了填空加入未确认的小按钮、icon strip、装饰工具栏或候选工具入口。只有当对应地图功能已经进入真实系统范围，并具备明确用途、状态矩阵、tooltip / 文案、hit rect 和冲突评审时，才允许出现小工具按钮。

在当前世界地图分支中，右下空间优先归还给右侧选中地区功能：地区任务预览、收益 / 消耗摘要、行动确认和 `进入地区` 主 CTA。若需要地图图层、定位、筛选、情报视图等工具，必须另开功能设计，不得作为空白填充物塞回右下。

### 4. 真实内容填充稿

用真实 B7 状态填充：

- 选中：北美禁区。
- 状态：红线升温。
- 收益窗口：3天。
- 进入消耗：1天。
- 可见任务：3。
- 周期：探索周 01，剩余 5 天。
- 左侧还需覆盖欧洲裂隙、东亚镜像城、南美遗迹等不同状态。

验收点：

- 中文最长态不压边。
- CTA 仍是视线终点。
- `推进一天` 与 `进入地区` 不同级、不相邻、不共用红色语法。
- 底部三个入口不抢主 CTA。

### 5. 运行时落地

只有在 filled-state text mock 通过后，才进入 HTML / Godot。

运行层只负责：

- 动态文字。
- 状态切换。
- 点击和 hover。
- 布局适配桌面 16:9。

视觉质感来自前面拆好的 bitmap / atlas / component assets。

## 下一步建议

不要立即重做整屏运行 UI。下一步建议先做 **右侧地区详情 vertical slice**：

1. 右侧 dossier 空白底板。
2. 北美禁区低多边形 snapshot。
3. 主 CTA 默认 / hover / disabled 三态。
4. 对应 `content_rects / no_text_rects` overlay。
5. 一张真实中文填充预览。

原因：右侧详情决定“当前选中地区 -> 进入地区”的主链，也最能验证图3/图4风格能否服务真实 UI，而不是停留在美术板。

## 右侧 snapshot 方向

北美禁区图样建议：

- 深蓝 / 蓝绿低多边形夜景。
- 一个高识别异常主物件，例如广播塔、金字塔状山体、信号柱或低多边形城市设施。
- 一束橄榄绿 / 蓝绿色扫描光。
- 少量剪影人群或封锁线，但不做细节叙事。
- 不出现文字、数字、UI、章、按钮或地图标签。
- 外框可为 Polaroid / snapshot，但框内只承载图像。

## CTA 方向

主 CTA 建议：

- 红橙印刷票条 / 文件夹 action tab。
- 干净矩形文字槽。
- 右侧固定箭头禁写区。
- 轻纸层厚度和短投影。
- hover 可增加 1-2px 亮边或纸层抬升。
- pressed 做轻微下压，不做金属发光。
- disabled 改为灰橄榄 / 去饱和红，不保留强红。
