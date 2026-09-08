# 世界地图 v3 不对称三责任区交付清单

**结论**：已由 v4 取代。v3 解决了地图面积超过真实内容、横向 dossier 侵入地图和 clean 状态混入调试文案的问题，但 2026-08-04 用户复核发现左索引与 DAY 之间仍有 `106px` 无职责夹层，且左右地区图只是同算法不同比例复绘；原 `P0/P1/P2=0` 终审结论撤回。当前真值见 `2026-08-04-world-map-shared-image-and-gap-v4-delivery-manifest.md`。

**影响**：页面重新建立了“左选地区—中看位置—右看档案并进入”的稳定链路，同时没有退回旧等宽三栏；但仍不能据此升为正式美术或生产候选。

**下一步**：用户先裁决 v3 相比 v2 的空间与内容匹配度；通过后再制作正式组件美术壳与正式世界地图纵切片。

## v3 区域合同

- 左地区索引：`[36,174,372,650]`。
- 中央地图交互净区：`[432,154,960,700]`，无可见面板外框，不被详情遮挡。
- 右纵向 dossier：`[1416,174,468,842]`。
- 左只读 DAY：`[36,930,372,86]`。
- 水平职责闭合：`36 + 372 + 24 + 960 + 24 + 468 + 36 = 1920`。

## 相比 v2 的关键变化

1. 地图从约 1400px 的泛化全屏交互区收束为 960×700 的真实净区。
2. dossier 从右下横向浮窗改成右侧纵向固定输出区，不再遮挡地图。
3. 地图只保留三个地区、短状态与低权重关系线；没有添加任务、派遣、骰池或假事件填空。
4. 左卡命中区从 380×170 收束为 340×170，三卡仍位于唯一 RegionIndex 边界内。
5. dossier 的主图、摘要、disclosure、三行展开容量、成本与 CTA 改成稳定纵向内容流。
6. `DAYS LEFT 07` 只在顶栏出现一次；clean 状态删除“当前锚点 / 来源 / 状态已同步”。
7. selected 蓝、warning 锈红、locked 灰橄榄与卡—beacon—dossier 同步逻辑保持不变。

## UX 终审

- 地图净区：PASS。
- 5 秒操作链：PASS。
- 状态同步：PASS。
- 世界层内容边界：PASS。
- 展开态：PASS。
- P0=0，P1=0，P2=0。
- 结论：v3 明显比 v2 匹配当前真实内容密度，可交用户查看；本轮不追加美术精修。

## 运行证据

- `gda script validate`：主原型与最终修改组件通过。
- 正式 Godot agent smoke：`Godot agent smoke passed.`
- 窗口化 OpenGL 状态断言：`test_world_map_integrated_prototype.gd OK`。
- 真实截图：`capture_world_map_integrated_prototype.gd OK`。
- 原型独立 headless runner 的 Windows Dummy 显示路径仍不作为本轮状态证据；正式项目 headless smoke 不受影响。

## 截图

- `15-clean-asymmetric-three-zone-v3-final.png`：v3 clean 首帧。
- `16-hit-rect-review-v3-final.png`：地图净区、卡片、beacon、disclosure、CTA 与只读条证据。
- `17-locked-feedback-v3-final.png`：东亚阻断反馈，北美 selected / dossier 不变。
- `18-mission-expanded-v3-final.png`：三行只读任务预览原位展开，CTA 不移动。
- `19-interaction-state-sequence-v3-final.gif`：状态短序列。
- `20-v2-v3-layout-comparison.png`：v2 / v3 并排对比。

证据目录：`docs/screenshots/2026-08-03-world-map-integrated-functional-skeleton/`。

## 阶段边界

- 能证明：三责任区的空间合同、真实状态同步、世界层内容边界与少量运行状态成立。
- 不能证明：最终纸材、符号与字体美术、完整状态矩阵、正式场景接入和生产复审已经通过。
- 允许：用户评审；对用户指出的结构问题做增量调整。
- 禁止：直接制作正式 atlas / manifest、覆盖 `WeeklyRunGame`、宣称视觉标杆或生产候选。

## 反向读法

- 它不是旧三栏后台：中央地图没有面板壳或纵向分割线，左右纸面组件也不等高、不等材质。
- 它不是地图壁纸：地图拥有独立 960×700 真实命中净区，三组 beacon 均可操作并同步右档案。
- 它不是靠假内容填满：世界层只存在地区选择和关系，具体任务仅在 dossier 的只读展开区出现。
