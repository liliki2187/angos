# 世界地图 benchmark 三方向风格探索 v1 交付清单

## 交付结论

已按两张 clean-low-poly weekly 正式标杆，以完全相同的真实内容与三栏职责，从空白画布生成三套完整 `1920×1080` 美术方向：

- A：连续桌面·巨幅地图母版。
- B：扁平纸雕·综合色周刊拼贴。
- C：夜班桌景·综合色灯光静物。

当前状态：`three_benchmark_style_variants_pending_user_choice`。

三张都只用于比较主物件、综合色、纸物关系、拼贴节奏和场景氛围。它们不是功能合同稿、生产组件或 Godot 输入。

## 交付文件

| 文件 | 用途 | SHA-256 |
| --- | --- | --- |
| `02-a-giant-map-master-1920x1080.png` | A 完整方向 | `EFAC4D74DBE75627DDB94947E84261815C9E1C4FE60C8EF9833BC5F02578AC6B` |
| `04-b-flat-cut-paper-collage-1920x1080.png` | B 完整方向 | `7FC90618269515B50F03A68C199E22F1636674AAD4601173FB6F8F078ED1CFE4` |
| `06-c-night-desk-light-islands-1920x1080.png` | C 完整方向 | `4387BBE0D47932F23EDD3C2959EE8B9C00A1B0DB08FAF526781BDA16FF97DC79` |
| `07-three-benchmark-style-variants-comparison-1920x520.png` | 三方向同尺寸并排板 | `008A75A4A10EEDF342511F00D9C6EE4E8CFD8561E50DEFC7B350A5799950B44C` |
| `08-generation-prompt-set.md` | 三次最终 ImageGen prompt set | — |

输出目录：`image_gen/2026-08-18/world-map-benchmark-style-variants-v1/`。

## 制作方法

- 使用 Codex 内置 ImageGen，一方向一次独立调用，均从空白画布生成。
- 两张 benchmark 是唯一正向美术真值。
- 上一张被否决候选只提供功能、真实文案和负面三栏轮廓参考。
- canonical 内容板只锁定北美洗衣店、东亚天文台、太平洋射电望远镜三张 `1104×704 / 69:44` 母图。
- 程序只负责把模型原始 `1672×941` 结果无裁切规格化为 `1920×1080`，并排版对比板；没有重画三张方向稿的纸材、组件、地图或灯光。

## 三方向差异

| 方向 | 第一眼主物件 | 主要优势 | 当前风险 |
| --- | --- | --- | --- |
| A | 一张横跨三栏的灰蓝地图母版 | 功能与美术最平衡；三卡同构基本稳定 | 地图纸偏制图稿 / GIS，灰度略旧 |
| B | 无硬框的综合色剪纸世界与大型出版图形 | 最接近 benchmark，最远离 SCP / 后台 UI | 01 卡放大、图窗漂移、Schedule 箭头假交互 |
| C | 三处工作光组织的夜班桌景 | 接触关系和场景氛围最完整 | 中央完整暗面板与左托盘回流旧三栏 |

## 双审结论

- UI Designer 排序：`B > A > C`。三张宏观差异足够，可交用户做纯风格比较；B 的三卡与 Schedule 漂移必须在选中后回填。
- UX 老哥美术排序：`B > A > C`；功能安全排序：`A > C > B`。建议在 A 的物理地图母版与 B 的大胆纸雕拼贴之间优先裁决。

## 用户本轮只需判断

1. 更喜欢 A 的“巨大物理地图底稿”，还是 B 的“大胆扁平纸雕周刊拼贴”？
2. C 的夜班灯光是否足以改变旧三栏感，还是仍然太像上一版？

不要以当前卡片 exact rect、图窗尺寸或 Schedule 外形选择 B；这些是已标注的合同漂移，不是推荐交互。

## 阶段边界

- 用户选中前不修 exact rect、不生成共享卡壳、不拆组件。
- 用户若选 B，下一轮只做统一 RegionCard、严格 `69:44`、passive Schedule 与大陆减面，不混入 A 的灰地图纸或 C 的暗矩形底稿。
- 用户若选 A，下一轮只降低制图学细节与旧化，不改巨幅地图母版的主轮廓。
- C 只有在用户明确选择保守氛围路线时才继续。
- 三条路线均不进入 atlas、manifest、Godot 或 `WeeklyRunGame`。
