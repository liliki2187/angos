# 区域任务短签全类型 / 全状态美术母板 Router Card

> 日期：2026-07-20  
> 风险：`risky / assetized-ui / imagegen`  
> 当前阶段：`runtime_candidate_user_rejected_state_overlay_quality -> visual_style_reference`

**结论**：当前 v3 暂不冻结；先用一张大尺寸美术母板重新定义短签的类型与状态资源语言。  
**影响**：本轮只验证美术资源分层和状态家族，不切 atlas、不替换 Godot、不解锁 event card。  
**下一步**：母板经用户确认后，再拆透明资源并做一次定向运行时回插。

## 范围

- **用户明示需求**：短签及其全部类型、状态先由真实生图生成大尺寸风格稿；解决当前程序多边形底板、尾块、弧线和状态签显得粗糙的问题。
- **必要补全**：区分“任务类型”与“交互 / 流程状态”两条视觉轴；加入组合压力样例，避免单态好看但叠加后重新变成程序补丁。
- **可以延期**：透明抠图、atlas、manifest / 合同升版、Godot 替换、全状态运行截图、event card 与右侧 dossier 实现。
- **后续保留项**：右侧 dossier 在选中任务后显示风险等级、风险依据与推荐 / 建议；本轮只记录信息职责，不把它塞进短签生图。

## 被路由对象

- 当前对象：`pin_slice_c_hybrid_v3 / runtime_candidate_pending_user_visual_review`
- 本轮产物：`visual_style_reference / component correction sheet`
- 允许下一步：用户确认后进入 `no_text_asset_master` 拆分与单次 runtime 回插。
- 禁止跳到：`atlas / manifest replacement / production_candidate / event card batch`。

## 母板覆盖

- 类型轴：`permanent / chain / hidden / temp`。
- 状态轴：`available / hover / selected / disabled / assigned / urgent / locked / focus`。
- 组合压力：覆盖 `temp + urgent`、`chain + assigned`、`hidden + selected` 与左右翻签 / clamp 极端态；不制作难以审阅的 `4 × 8 = 32` 全排列墙。
- 动态任务名、天数和中文状态词不烘焙进生产面；母板可使用非生产注释区说明矩阵。

## 冻结合同

- 图钉运行时视觉 `64×80`、命中区 `72×80`、锚点 `[36, 76]`。
- 短签固定 `200×72`，内容安全区 `[14, 8, 166, 56]`，不使用 NinePatch。
- 标签左右挂点、8px 净空、0–N、cluster、clamp、共享 `task_id` 和文字分层不变。
- 程序继续负责状态判断、显隐、文字、锚点、避让与时序；美术资源负责可见纸壳、状态背板 / 端帽 / 色脊 / 印刷笔触的形状与材质。

## 真值与复审

- 视觉真值：`benchmark-board-01.png`、`benchmark-board-02.png`、E2、支线风格规范与纸张材质合同。
- 协作顺序：现有 UI 先由 `ux_laoge` 诊断，再由 `ui_designer` 整理母板矩阵，父级调用真实 `imagegen`。
- clean-lowpoly-weekly 临时例外继续生效：不自动调用旧像素 / 半调坐标系的 `angus_art_director`。
