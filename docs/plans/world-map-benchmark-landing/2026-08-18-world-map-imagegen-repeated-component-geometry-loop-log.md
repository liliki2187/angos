# 世界地图整屏生图重复组件几何误判 Loop Log

## 结论

本轮最初错误地把“整屏 ImageGen 能理解三张卡属于同一 class”扩大为“它能稳定输出三张像素同构的 RegionCard”。连续三次结果都自动把 selected 的 01 卡画大，并把三张图窗改成不同横幅比例。该路径已经止损；最终采用“一张真实 ImageGen 共享无字卡壳＋确定性同构复制＋canonical 内容回填”。

## 影响

- 若继续把整屏生图近似当成 exact contract，会重现用户已经否决的“状态改变卡体和图片规格”。
- 直接程序绘制三张卡虽然能修几何，却会重新造成粗糙后台组件，违背用户对生图质感的要求。
- 正确分工必须同时满足：美术表面来自真实 ImageGen；重复实例、图片槽、状态槽、文字安全区由确定性排版保证。

## 失败证据

1. `02-filled-state-rough-abstraction-1920x1080.png`：美术减法成立，但 01 明显高于 02/03，图窗规格不一。
2. `04-left-contract-edit-1920x1080.png`：selected / warning 语义分轨成立，但 01 仍是大卡。
3. `07-geometry-guided-edit-1920x1080.png`：加入正确合同整屏作 geometry-only 参考后，模型仍把 01 画大；说明问题不是 prompt 缺一句尺寸，而是整屏生成模式不适合证明同 class exact repetition。
4. `05-region-card-blank-master-imagegen.png`：单组件母版能稳定提供真实纸材，但内部预制表头、双栏和 footer 造成后台表格感，只能作为诊断母版。

## 根因

1. 生图模型会主动用尺寸、图窗和信息容量表达 selected 权重；这与冻结的“状态零布局位移”合同冲突。
2. 任务同时要求高质感美术与同 class 精确重复，却没有在第一轮就把两种职责拆开。
3. 首张共享母版为了预留所有槽位，把占位结构画得过完整；精确不等于必须预制成表格。

## 修正路线

1. 使用 benchmark 真值重新生成 `09-region-card-simple-paper-master-imagegen.png`：只保留一张连续暖灰简报纸和一层露边综合色背纸，删除表头、图窗占位、右单元格、footer 条、网格和多重边线。
2. 程序仅承担：连通背景转透明、母版等比缩放、三次同构复制、三张 `1104×704` 母图等比缩至 `207×132`、真实中文、状态文字和 footer 安全区。
3. warning 不再画闭合框，改为短锈红竖条＋裸文字；selected / locked 使用同位状态签。
4. 地图、顶部、右稿、Disclosure、CTA、Schedule 和背景不参与程序重画。

## 防复发规则

- 同一屏内多个同 class 组件需要 exact repetition 时，默认禁止用整屏 ImageGen 分别画实例来证明合同。
- 必须先生成一张共享无字材质母版，再确定性复制并回填内容。
- 共享母版不得预制成完整后台表格；槽位可以由排版坐标存在，不必全部由美术框线可见。
- 合成后同时过两类 Gate：几何 / 同源复用 Gate 与“是否重新读成程序后台组件”的美术 Gate。

## 当前状态

最终图 `10-final-filled-state-visual-target-1920x1080.png` 已由 UX 老哥与 UI Designer 双审：`P0=0 / P1=0 / PASS`，可作为 filled-state 视觉方向候选提交用户；仍不是 Godot、atlas、manifest 或生产资产。
