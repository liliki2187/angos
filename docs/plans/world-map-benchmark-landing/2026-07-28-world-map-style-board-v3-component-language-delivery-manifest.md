# 世界地图风格板 v3 组件语言返工交付清单

## 决策条

- **结论**：部分通过。可审阅新闻图像、塔、站台、待核批注与符号试条是否进入同一视觉语言；不得称为生产标杆。
- **影响**：25% 缩略阅读成立，三处 `02` 塔已有同母版视觉；UFO 和 `DAY 1` 仍有残余偏差，严格 `scope_invariant` 缺少 mask / ROI 外像素差分证据。
- **下一步**：先由用户审阅本版。若继续返工，不做第三次整板重采样，改为孤立组件生图、局部合成和像素差分验收。

## 产物身份

- `artifact_type = visual_style_reference`
- `state = component_render_language_revision`
- `status = visual_component_language_candidate_partial_pass_pending_user_review`
- `production_candidate = false`
- `runtime_implemented = false`
- `component_render_language_lock = partial_pass`
- `scope_invariant = unverified`

这是一张桌面 16:9 世界地图界面的美术风格证明板，目标是验证同一界面内部的对象—画法统一，不是可切 atlas 的生产资产，不是 Godot runtime 截图，也不代表区域地图与报刊界面可据此扩产。

## 用户审阅入口

- 完整风格板：`image_gen/2026-07-28/world-map-interface-style-board-v3-component-language/01-world-map-interface-style-board-v3-component-language.png`
- 25% 缩略证据：`image_gen/2026-07-28/world-map-interface-style-board-v3-component-language/02-world-map-interface-style-board-v3-25pct.png`
- 100% 组件裁切证据：`image_gen/2026-07-28/world-map-interface-style-board-v3-component-language/03-world-map-interface-style-board-v3-component-qa.png`
- 说明：`image_gen/` 当前被仓库 `.gitignore` 忽略；以上文件已落在工作区，但未进入 Git 追踪。

## 输入与生成链

- 原始 v2：`image_gen/2026-07-24/world-map-interface-style-board-v2/01-world-map-interface-style-board-v2.png`
- 直接艺术标杆：
  - `design/art-direction/references/clean-lowpoly-weekly-branch/benchmark-board-01.png`
  - `design/art-direction/references/clean-lowpoly-weekly-branch/benchmark-board-02.png`
- 贴纸局部参考：
  - `design/art-direction/references/clean-lowpoly-weekly-branch/sticker-reference-crop.png`
  - `design/art-direction/references/clean-lowpoly-weekly-branch/premium-sticker-reference-crop.png`
- 规范输入：
  - `design/art-direction/clean-lowpoly-weekly-branch-style-guide.md`
  - `design/art-direction/clean-lowpoly-weekly-paper-and-color-contract.md`
- 生图方式：Codex 内置 `imagegen` 的真实位图编辑；程序只用于 25% 缩放与 100% QA 裁切，没有替代生图。
- 第一轮原始输出：`C:\Users\gzfangyue\.codex\generated_images\019f8963-8f75-7e91-92e0-515d05adc6c9\call_1dWOvChsyOlzmRwTADZbeR2W.png`
- 第二轮原始输出：`C:\Users\gzfangyue\.codex\generated_images\019f8963-8f75-7e91-92e0-515d05adc6c9\call_9wP4gsPn1bE3GBhUvUJFURfW.png`
- 最终图片尺寸：`1672×941`，RGB。
- 最终图片 SHA-256：`b10290628e7979e4d161b2b077d3b229bbdc0f8996bc3e71acb4fe0a4c18374a`
- 25% 证据 SHA-256：`5ffef2cdcfec5c4f641c3880bdafaeb405d60c6bc0054ee94d6b05103d75c7a5`
- 100% QA 拼版 SHA-256：`c7e943b745e8920611cb98d2cddd3b49e78195013a753c99e611ee44ca7ad100`

## 冻结范围与返工范围

冻结不变：

- 整板总体构图、组件位置、尺寸、阅读顺序和纸堆关系。
- 左索引→中央地图→右 `NEWS LEAD` 的三段阅读链。
- 中央地图拓扑、网格、海陆色块、白圈、蓝色连线与黄色便签。
- 深海军蓝、钴蓝、青绿、橄榄与暖纸的综合色彩面积。
- `01/02/03`、`DEFAULT/SELECTED/LOCKED`、`WMW`、期号、条码和机构印刷图形的身份。

本轮只要求改变：

- 新闻现场图由细桁架、逐窗和摄影细节改成强剪影、粗颗粒大色面。
- 三处 `02` 塔在视觉上使用同一母版语言。
- UFO 增加偏心、线重变化、断口 / 重描、不等宽纸边等手工印刷证据。
- 底部五枚符号由等权工具栏改成职责不同的印刷试条。
- 两处虚线问号由开发占位符改成编辑部待核批注。
- `DAY 1` 保留时间硬件身份，同时压低镜面高光、深 bevel 和厚投影。

## UI Designer 等价 brief

UI Designer 子 agent 在读取阶段异常卡住并被中断，没有产出可用正文。父级读取同一 `skills/ui-designer/SKILL.md` 与必需规范后，按等价流程执行以下交接：

| 对象 | 保留身份 | 新画法 | 禁止项 |
| --- | --- | --- | --- |
| 默认建筑 | 现场报道图 | `3–8` 个结构块、粗大色面、少量窗带 | 逐窗、摄影景深、工业渲染 |
| 三处 `02` 塔 | 同一事件母图 | 同一塔头、塔身节点和基座剪影 | 分别生成近似版本、细桁架 |
| 锁定站台 | 低多边形现场图 | 大钟面、大体块、低细节暗场 | 刻度、微型字、玻璃反射 |
| 待核批注 | 世界内未知线索 | 偏移便签、未确认剪影、圈注 | 虚线控件框、居中 placeholder |
| UFO | 黑色幽默态度贴 | 手工墨线、轻微偏心、模切纸边 | 完美镜像、统一矢量描边 |
| 符号试条 | 品牌符号样本 | 不同载体、尺寸和印刷重量 | 等尺寸、等线宽、机械等距 |
| `DAY 1` | 编辑部时间硬件 | 哑光、浅 relief、少量硬影 | 镀铬、深 bevel、产品摄影 |

桌面线框、模块位置与交互职责全部沿用 v2，不新增按钮、图例、路线、CTA 或玩法。可见差异只能发生在上述对象内部画法。

## UX 老哥诊断与本轮映射

UX 老哥原始结论：`局部返工 GO，但整板仍不得升格生产候选。P0=0，P1=4，P2=1。`

| 原诊断 | v3 结果 | 证据 |
| --- | --- | --- |
| P1 新闻图像语言分裂 | 通过 | 默认建筑、站台与三处塔均改为粗块面；100% 拼版可对照 |
| P1 UFO 商品矢量贴 | 部分通过 | 纸边与墨线有改善，但主体仍略平滑、偏对称 |
| P1 符号试条伪装工具栏 | 基本通过 | 五枚符号已使用不同载体与印刷重量，但仍共用黑色承载带 |
| P1 待核信息变开发占位符 | 通过 | 虚线方框已删除，改为偏移便签与未确认剪影 |
| P2 日程器产品感过重 | 部分通过 | 高光下降，但外壳厚度与机械 bevel 仍偏强 |

UX 冻结意见继续生效：保持 `1672×941` 画布、全部位置与遮挡、三段阅读链、地图拓扑、综合色彩、`02` 同源事件关系、右侧纸堆与机构印刷图形；不得由本风格板直接扩展地区地图、报刊页、atlas 或 Godot。

## Gate 结果

| Gate | 结果 | 说明 |
| --- | --- | --- |
| 直接标杆对照 | `partial_pass` | 非旅行语义、编辑部氛围、粗颗粒图像与纸面品牌化成立；UFO / DAY 1 仍未完全命中 |
| 25% 缩略可读 | `pass` | 中央地图与 `NEWS LEAD` 仍为主焦点；三处塔一眼同源；底部对象没有反抢主层级 |
| 100% 组件语言 | `partial_pass` | 塔、站台、待核批注通过；UFO、DAY 1 部分通过 |
| 同母版视觉 | `pass_visual_only` | 三处塔的塔头、塔身、基座结构一致；底层资产是否同一文件仍未验证 |
| `scope_invariant` | `unverified` | 当前内置 imagegen 没有 mask / 局部像素锁定；全图虽视觉上保持构图，但不能证明 ROI 外像素未重采样 |
| `composite_cleanliness` | `not_run` | 本轮没有局部程序合成；若下一轮采用孤立组件合成，必须补跑 |
| UI 双 agent | `exception_recorded` | UX 老哥完成；UI Designer 子 agent 卡住，父级按同一技能执行等价流程 |
| 生产标杆 / 真源候选 | `blocked` | 用户未审阅，且 UFO、DAY 1 与 `scope_invariant` 未全通过 |

## Stop-loss 与禁止跳步

- 已连续做两轮针对性真实生图编辑，同类偏差仍残留；本轮不进行第三次整板重采样。
- 若用户继续要求修正，先生成孤立 UFO 与 `DAY 1` 组件候选，再按明确 ROI 合成，并证明 ROI 外像素不变。
- 用户确认前，不把 v3 写入正式美术真源，不更新合同版本，不切 atlas，不接 Godot，不扩展区域地图和报刊界面。
- 本轮未修改 GDD、runtime、正式 UI 合同或设计采纳记录；没有新增用户已采纳结论。
