# WMW 右 dossier 候选 A1 布局与照片复审

> **日期**：2026-07-14
> **版本**：candidate A1 / v0.9.1
> **产物类型**：`runtime_state_preview`
> **裁决状态**：A205 已判运行语义失败；几何、照片和文字容器证据可复用，但 A1 不再是玩家视觉候选，由 A2 / 604 取代。

## 本轮修正

用户指出候选 A（585）存在三项问题：页眉图标、标题、状态章的视觉中心不齐；地区正文过于靠左；照片被非等比拉伸。A201 采纳以下修法，三份 v0.8.6 合同的 frozen 字段均未改动：

1. 页眉以参考分辨率 `y=59` 为真实墨迹光学轴，运行时偏移为 icon `+3px`、title `0px`、status 两行组 `-4px`。
2. `region_body` 外槽仍为 `[22,288,276,54]`，正文统一进入 `[34,290,252,50]`；`[22,288,4,54]` 为青色索引条禁字区。
3. 正式照片先锁精确 `69:44`：`1104x704` source → `552x352` 2x ingredient → `414x264` Godot runtime。只允许等比缩放，Godot 禁止 `STRETCH_SCALE`。

## 证据

- 589：布局与照片输入规格板。
  `docs/screenshots/2026-06-24-world-map-benchmark-landing/589-world-map-wmw-v0-9-1-right-dossier-candidate-a1-layout-photo-spec.png`
- 590：按规格真实 imagegen 的纯场景原图，无 UI、文字或假字。
  `docs/screenshots/2026-06-24-world-map-benchmark-landing/590-world-map-wmw-v0-9-1-right-dossier-photo-imagegen-raw.png`
- 591：raw / source / ingredient 与三母版 QA。
  `docs/screenshots/2026-06-24-world-map-benchmark-landing/591-world-map-wmw-v0-9-1-right-dossier-candidate-a1-photo-and-master-qa.png`
- 592/593：Python 回填与实际 raster glyph bbox、参考轴、正文 inner/no-text 参考线 QA。
- 594/595：Godot 4.6.2 windowed OpenGL3 真实运行与 QA；截图脚本保留 `frame_post_draw` 等待、全黑拒绝与相对基线完整性检查。
- 596：同一 Godot 链的 A / A1 整体与页眉、照片、正文裁切对照。
  `docs/screenshots/2026-06-24-world-map-benchmark-landing/596-world-map-wmw-v0-9-1-right-dossier-candidate-a1-review-board.png`
- 597：完整 manifest。
  `docs/screenshots/2026-06-24-world-map-benchmark-landing/597-world-map-wmw-v0-9-1-right-dossier-candidate-a1-manifest.json`

## Gate 结果

| Gate | 结果 | 可核验数据 |
| --- | --- | --- |
| 页眉真实墨迹共轴 | PASS | icon `118.5`、title `117.5`、status group `118.5`，目标 `y=118@2x`，最大偏差 `0.5px@2x` |
| 正文可读内区 | PASS | 两行 glyph 左缘均为 `x=68@2x`；距 no-text 右缘 `16px@2x`；两行左缘差 `0` |
| 照片比例 | PASS | raw `1573x1000` 等比缩至 `1107x704` 后只裁横向 `0.27%`；source / ingredient 比例误差 `0`，无上采样 |
| Godot 运行时照片 | PASS | 输入断言 `552x352`；`STRETCH_KEEP_ASPECT_COVERED`；运行槽 `414x264` |
| 实际光栅字形证据 | PASS | 8/8 字段的 `bbox`、粉框和 `raster_glyph_bbox` 同源；独立重放校验通过 |
| 原 A196 动作栈对齐 | PASS | 两 child 可见主体左 / 右 / 宽度差仍为 `0/0/0` |
| Godot 内容有效性 | PASS | 594/595 均为 `1920x1080`，采样颜色 `3749/3845`，非黑采样有效 |
| 可见字段语义必要性 | **FAIL** | `推荐12`、压力标题 / 计数与虚构正文来自容量 fixture，并非正式 region payload；A205 后由 604 取代 |

## 双 Agent 复核

### UX 老哥

结论为 `P0=0 / P1=0 / P2=2`，静态 default 状态可交用户视觉裁决。三项旧 P1 均已修复，未发现新增 P0/P1：页眉最大墨迹轴偏差 `0.5px@2x`；正文两行左缘一致并与禁字区相隔 `16px@2x`；照片全链精确 `69:44`，缩小后仍为雷达 > 金字塔 > 天线三级层级。

保留两个 P2：`推荐12` 的正式语义 / 单位仍未闭合，并可能与按钮的 `12项` 串读；后续 hover / pressed / disabled 必须用动态证据证明整条动作带作为单一 hit rect 统一响应。

### UI Designer

结论同样为 `P0=0 / P1=0 / P2=2`，未发现新增美术或层级问题。页眉已从三个独立居中的 carrier 读成同一视觉行；正文在索引条后形成稳定呼吸空间，未因右移产生拥挤；新照片延续 clean low-poly weekly，未滑向写实摄影或密集三角网，雷达、金字塔与天线在小槽内仍有明确主次。

## 当前结论

### A205 追认修订（2026-07-14）

用户追问“推荐12是什么功能”后，父级对照现行玩法真源确认：世界地图只选择地区，具体任务与 1-3 人派遣发生在进入地区之后，因此不存在稳定的地区级推荐人数。进一步全页审计又确认，A1 的 `北美禁区警戒带 / 高危 / 推荐12 / 限时2周 / 线索缺口3 / 12项` 以及两行正文均是压力或演示 fixture，而不是正式首周 region payload。

因此，A1 只能继续作为 A201 的页眉光学轴、正文安全内区、照片 `69:44` 与无字母版证据；其玩家可见运行语义已失败，不得再称“可交用户视觉裁决”。A2 以同一无字美术复用这些有效证据，同时把所有可见字段改为 production export，并由 604 的 `visible_field_semantic_necessity` gate 接管。
