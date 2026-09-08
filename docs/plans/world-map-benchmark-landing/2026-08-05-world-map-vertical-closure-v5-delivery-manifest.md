# 世界地图纵向闭合合并版 v5 交付清单

## 结论

v5 已把 V5.1 的纵向容量与 v4 的交互组件合并到同一张真实运行界面：左侧完整日程器、中央纵向地图与右侧全高档案共同收口到 `y=1056`；69:44 一图两用、任务折叠和唯一 CTA 保持不变。

## 产物身份

- `runtime_skeleton / runtime_state_preview`
- 可以证明：三责任区闭合、禁用日程状态、地区选择 / 锁定反馈、任务折叠、CTA 与同源图合同在 Godot 中成立。
- 不能证明：正式地区美术已完成、独立 `advance_day` 已接入、整屏已达到生产美术标杆、完整 `WeeklyRunGame` 数据接线完成。

## 几何合同

- `RegionIndex=[36,154,372,640]`
- `ScheduleGate=[36,810,372,246]`
- `MapField=[432,154,960,902]`
- `SelectedRegionDossier=[1416,24,468,1032]`
- 三个主要责任区底线：`y=1056`
- `MissionDisclosure=[1443,596,414,56]`
- `PrimaryCTA=[1443,956,414,76]`

## 资源与状态合同

- canonical source：`1104×704 / 69:44`
- 左卡：`138×88`
- 右档案：`414×264`
- 宽高严格 `3×`，完整 UV、无裁切、无非等比拉伸、同一 `resource_path`
- `ScheduleGate=disabled_runtime_unavailable`，不冒充未实现的推进命令
- collapsed / expanded 使用同一 `414×248` 容量，CTA 不移动

## 运行证据

- 隔离 Godot 用户缓存后的 headless 状态测试：`test_world_map_integrated_prototype.gd OK`
- 固定 Godot 4.6.2、窗口化 OpenGL 截图脚本：`capture_world_map_integrated_prototype.gd OK`
- 初次未隔离缓存的 headless 调用发生项目已知原生 signal 11；隔离缓存后同版本测试通过，未出现 GDScript 断言失败。

## 截图证据

目录：`docs/screenshots/2026-08-03-world-map-integrated-functional-skeleton/`

- `31-vertical-closure-shared-image-v5.png`：默认折叠态与三责任区闭合
- `32-hit-rect-review-v5.png`：地图、地区卡、beacon、披露、CTA 与禁用日程区
- `33-locked-feedback-v5.png`：锁定地区反馈不替换当前档案
- `34-mission-expanded-v5.png`：四任务容量展开且 CTA 不移动
- `35-interaction-state-sequence-v5.gif`：真实运行状态序列

## 下一 Gate

用户先判断 v5 的宏观结构、地图纵深、完整日程器和全高档案是否比 v4 更合理。通过前不把当前程序化 SVG 地区图称为正式美术，也不把禁用日程控件接成伪功能。

## 双审收口

- 首轮：UI / UX 均指出“技术禁用、视觉像按钮”的日程状态不能放行；同时标记 collapsed 假列表框、锁定术语和对称南极填空带。
- 修订：日程器彻底移除 Button 与动作热区，改为静态低对比 Panel；collapsed 取消全高边框；锁定状态与访问结果分工；南极洲改为低明度不规则轮廓，地图网格同步降权。
- 最终：UI Designer `PASS / P0=0 / P1=0 / P2=0`；UX 老哥 `PASS / P0=0 / P1=0 / P2=0`。
