# 世界地图功能—标杆元素转译概念稿 v1 交付清单

## 结论

`CONDITIONAL PASS / P0=0 / P1=2`。

本稿已证明两张正式 benchmark 的视觉语言可以覆盖“左选地区—中定位证据—右确认主案—唯一 CTA”的粗功能链，且上一稿的灰土问题已实质关闭。它仍是 `functional-style translation concept`，不证明组件合同、图片像素同源或运行时状态。

## 输入与权限

- 正向美术真值：
  - `design/art-direction/references/clean-lowpoly-weekly-branch/benchmark-board-01.png`
  - `design/art-direction/references/clean-lowpoly-weekly-branch/benchmark-board-02.png`
- 功能职责参考：
  - `design/art-direction/references/clean-lowpoly-weekly-branch/interface-inputs/world-map-functional-wireframe.png`
- 上一纯风格稿只参与人工对比与色彩量化，没有作为本次 ImageGen 正向输入。
- clean-low-poly weekly 临时例外继续有效，没有调用旧像素 / 半调坐标系的美术指导。

## 产物

| 文件 | 用途 |
| --- | --- |
| `image_gen/2026-08-19/world-map-functional-style-translation-v1/01-functional-style-translation-imagegen-native-v0.png` | 首轮真实 ImageGen；综合色与结构成立，但三张地区卡错误重复洗衣店图，保留作诊断样本 |
| `image_gen/2026-08-19/world-map-functional-style-translation-v1/02-generation-prompt.md` | 首轮生成提示词、参考图权限与第二轮定点修正规则 |
| `image_gen/2026-08-19/world-map-functional-style-translation-v1/03-functional-style-translation-imagegen-native.png` | 当前用户审阅稿；北美 / 东亚 / 太平洋分别为洗衣店 / 天文台 / 射电望远镜 |

最终图为 Codex 内置 ImageGen 原生 `1672×941 / RGB / 16:9`，未程序重绘、拼接、裁切、拉伸或重采样；SHA-256：`88F8C2AD3C55F3F08A82C6185048EB939E7E4836A109A3F5BC01BF6F2A2F7F4F`。

## 色彩对比

| 图 | 可见内容 V_mean | 可见内容 L_mean | 判断 |
| --- | ---: | ---: | --- |
| benchmark 01 | 0.461 | 0.184 | 正向真值 |
| benchmark 02 | 0.471 | 0.183 | 正向真值 |
| 上一纯风格稿 | 0.363 | 0.103 | 中间调过暗，综合色泥化 |
| 本次转译稿 | 0.491 | 0.205 | 接近且略高于标杆；灰土关闭，纸面接近亮度上限 |

本次不是全局增艳，而是把棕褐重新拆成冷灰米纸、芥末、橄榄、钴蓝与冷青，并把地图从最大灰团改成综合色宽块。下一轮不得继续扩大暖白纸面积；如需修色，只把右侧 Dossier 主纸局部压暗约 5%。

## 功能—标杆元素映射

| 功能区 | 转译物件 |
| --- | --- |
| 刊头 | 大字周刊锁定＋粗线 WMW 地球章＋ NO-HIT ISSUE 小票 |
| RegionCards | 三张同构正交简报纸＋蓝 / 芥末 / 橄榄 BackDecor 稿夹 |
| 地图 | 综合色宽块世界地图母纸，淡网格，无 GIS |
| Beacon | 粗断续锈红蜡笔圈与短批注 |
| selected evidence | 地点附近被夹住的 `69:44` 同源概念校样，NO-HIT |
| Dossier | 钴蓝背夹＋暖灰正交周刊主稿纸 |
| Disclosure | 主稿纸内部折入信息条，`＋/－` 原位切换 |
| CTA | 全屏唯一橄榄进入签 |
| Schedule | 左下被动 WEEK / DAY 回执 |

## 双 agent 终审

- UX 老哥：`CONDITIONAL PASS / P0=0 / P1=2`。灰土、地图 GIS、主照片电影化与粗功能链均已大幅关闭；右栏机构表格化及 `DISCLOSURE ＋` 与已显示内容的状态矛盾为两个 P1。
- UI Designer：`CONDITIONAL PASS`。品牌、三卡同构、三地区不同图、综合色地图、地点证据、Dossier 外壳、唯一 CTA、Schedule passive 与正交功能面均通过；右栏内容语言仍须在升格前转成周刊编辑记录。
- 两者都不建议交付前整屏重生；当前图已足够让用户判断综合色与物件映射，下一轮应只定点修改右栏。

## 已知边界

1. 三处洗衣店图只证明 `same-story / same-source concept`；ImageGen 不能证明同一 `1104×704 / 69:44` canonical 位图逐像素复用。
2. `DISCLOSURE ＋` 下方同时显示四行记录，折叠符号与内容状态矛盾。
3. `STATUS ACTIVE / FIELD REPORT / WITNESS NOTE / ANALYST MEMO / 日期 / Desk` 仍会让右栏局部回流机构档案。
4. `DAY 1 / 7 DAYS LEFT` 仅为风格稿 fixture，不冻结正式运行值。
5. ISSUE exact rect、动态文字容量、hit rect、状态矩阵与所有 BackDecor 的 NO-HIT 均未由本稿证明。

## 下一步

等待用户先裁决综合色与功能物件映射。若接受，只在右侧 Dossier 下半部进行定点真实 ImageGen：

- 选择 collapsed：只保留 `任务情报 ＋`，不显示条目；或 expanded：改为 `－`，只显示两条短情报；
- 删除四行日期 / Desk / FIELD 机构表；
- 改成两条不等长周刊编辑情报纸签；
- 保持整屏构图、地图、综合色、三卡、主图与 CTA 不动。

仍禁止组件拆分、atlas、manifest、Godot 与 `WeeklyRunGame`。
