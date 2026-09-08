# 世界地图 Integrated UI 功能骨架交付清单

> 状态修订：本文记录的 v2“地图＋右下横向 dossier”已被 v3 不对称三责任区取代。当前交付证据见 `2026-08-03-world-map-asymmetric-three-zone-v3-delivery-manifest.md`；v2 截图仅作布局对照。

**结论**：通过本轮可见检查点，可交用户判断 integrated UI 的结构方向；当前产物是 `runtime_skeleton / runtime_state_preview`，不是视觉成品或生产候选。

**影响**：已经能够验证世界地图不再沿用旧三栏换皮，也不是把风格板物件硬贴到功能稿上；但仍不能据此开始正式 atlas、纹理精修或覆盖正式世界地图场景。

**下一步**：由用户先判断整体构图、氛围和功能融合是否成立；通过后再进入组件美术壳、完整状态矩阵与正式场景纵切片。

## 本轮产物

- 类型：`runtime_skeleton` + 少量真实状态的 `runtime_state_preview`。
- 目标载体：Godot 4.6.3，桌面 1920×1080。
- 场景：隔离原型，不覆盖 `WeeklyRunGame` 正式世界地图。
- 视觉来源：只继承世界地图 A 的夜班石板蓝、暖纸、低多边形地图、橄榄 / 锈红 / 克制蓝和编辑部黑色幽默；不复制 A 的固定物件与完成构图。

## 已实现

1. 全屏深夜石板蓝地图成为主舞台，不再被三列等宽面板切碎。
2. 左侧 `RegionIndex` 是唯一地区选择边界；三张卡各自只有一个整卡命中区。
3. 卡片与地图 beacon 共享同一 `region_id`，当前北美在卡、节点、档案三处同帧同步。
4. `selected` 使用克制蓝整卡框 / 双环；`warning` 使用锈红折角 / 弧段 / 状态章；`locked` 独立使用灰橄榄与锁。
5. 锁定地区点击只给阻断和解锁条件反馈，不替换当前北美和右侧档案。
6. 右下 dossier 由标题、状态、主图、摘要、任务 disclosure、耗时和唯一 CTA 的真实槽位组成；展开任务情报时外框、主图和 CTA 不跳位。
7. `DAY 01 · DAYS LEFT 07 · 本屏操作 0 天` 为纯只读信息，没有伪按钮。
8. 原生中文和按钮状态均由 Godot Control 渲染；没有把真实文字烘焙进位图。

## 它能证明什么

- “真实行为组件 + 新布局合同 + A 视觉语法”这条路线能够形成可运行界面，而不是拼贴效果图。
- RegionIndex、beacon、dossier、disclosure、CTA 和只读时间条的职责、热区和状态关系可成立。
- 北美 `selected + warning`、东亚锁定反馈、任务折叠 / 展开三种首批状态能在同一结构中承载。
- 页面第一主语仍是世界地图与异常地区，不会误读成旅行社地图或后台管理三栏。

## 它不能证明什么

- 不能证明最终纸张材质、贴纸 / 标志系统、低多边形配图细节和字体美术已达到生产质量。
- 不能证明所有地区、长文案、键盘 / 手柄、完整 focus、全部 hover / pressed / disabled 状态已经覆盖。
- 不能把本原型直接升为 atlas、manifest、production candidate 或正式世界地图替换。
- 本轮未改玩法数据、正式周循环导航和资产合同。

## UX 复核

- Gate 1 `RegionIndex 唯一边界`：PASS。
- Gate 2 `selected 蓝 / warning 锈红分离`：PASS。
- Gate 3 `dossier 动态结构`：PASS。
- 分级：P0=0，P1=0，P2=1；P2 仅询问锁定地区是否允许切换查看。现有已采纳合同明确“锁定点击不改变 selected / dossier，只显示已有解锁条件”，因此本轮按既定规则关闭该疑问。
- 最终门禁：PASS，可交用户看 `runtime_skeleton / runtime_state_preview`；本轮无需追加资产化精修。

## 运行与测试证据

- `gda script validate`：`WorldMapIntegratedPrototype.gd`、测试脚本与截图脚本通过。
- 正式 Godot agent smoke：`Godot agent smoke passed.`
- 窗口化 OpenGL 状态断言：`test_world_map_integrated_prototype.gd OK`。
- 真实渲染：`capture_world_map_integrated_prototype.gd OK`。
- 原型自身的 Windows headless 独立 runner 在 Dummy 显示路径会等待，未用它冒充通过；本轮视觉与状态证据来自同版本 Godot 4.6.3 的窗口化 OpenGL 路径。正式周循环 headless smoke 不受影响。

## 截图证据

- `docs/screenshots/2026-08-03-world-map-integrated-functional-skeleton/05-clean-selected-warning-v2.png`：北美选中＋预警首帧。
- `docs/screenshots/2026-08-03-world-map-integrated-functional-skeleton/06-hit-rect-review-v2.png`：卡片、beacon、disclosure、CTA 与只读条热区证据。
- `docs/screenshots/2026-08-03-world-map-integrated-functional-skeleton/07-locked-feedback-v2.png`：锁定地区阻断反馈，北美与 dossier 保持不变。
- `docs/screenshots/2026-08-03-world-map-integrated-functional-skeleton/08-mission-expanded-v2.png`：任务情报原位展开。
- `docs/screenshots/2026-08-03-world-map-integrated-functional-skeleton/09-interaction-state-sequence-v2.gif`：五态短序列。

## Gate 与阶段边界

- 已过：结构职责、唯一地区选择边界、状态同步、selected / warning / locked 分语法、dossier 动态容量、真实热区、主流程 smoke、真实截图、UX 三项复核。
- 未过：用户整屏观感裁决、正式组件美术、最长文案、全状态矩阵、正式场景接入、资产合同与生产复审。
- 允许下一步：用户评审；随后只对被指出的 integrated UI 问题做增量修订。
- 禁止跳到：整屏生图替换、正式 atlas / manifest、覆盖 `WeeklyRunGame`、宣称视觉标杆或生产候选。

## 反向读法检查

- 若把它看成旅行地图：页面没有目的地照片、行程推荐、交通路线或观光 CTA；地图线表达异常证据关联，地区状态以封锁 / 红线 / 解锁条件为主，因此该误读不成立。
- 若把它看成旧三栏后台：右上没有独立第三列，dossier 嵌入地图下半部，地图仍占据上半屏与中心负空间，因此该误读不成立。
- 若把它看成风格板拼贴：卡片、beacon、dossier、disclosure 和 CTA 均有真实命中区、信号和共享状态，装饰文字全部 mouse-ignore，因此该误读不成立。
