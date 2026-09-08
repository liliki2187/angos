# A339 世界地图资产化前规划 Router Card

- 任务：把已接受的 filled-state 视觉方向转换为可装配页面合同，不继续追生图小字，也不进入 Godot。
- 产物类型：`component_class_contract / assembly planning`。
- 风险级别：`risky`。原因是本轮定义后续生产资产、动态文字和 8 个交互节点的所有权边界。
- 真源：A282、A294、A305、A306、A338、A339；`design/ui-contracts/world-map/` 现行 v1.0.0 类合同；A339 1920×1080 视觉参考。
- 必需协作：现有 UI 改进先由 `ux_laoge` 诊断，再由 `ui_designer` 转成规格；clean-low-poly weekly 临时例外，不调用旧像素/半调美术指导。
- 本轮允许：页面 assembly contract、分层结构板、字体/容量矩阵、未冻结项清单、第一条 vertical slice 选择。
- 本轮禁止：atlas、最终 manifest、Godot、WeeklyRunGame、ISSUE 票签资产化，以及从整屏参考或旧 `86:41` 历史壳直接裁切生产资产。Dossier 与 RegionCard 的 vertical slice 可使用真实 ImageGen 材质源＋合同坐标装配。
- 通过条件：五区几何与 8 节点录入；状态真值唯一；no-hit 分层明确；Dossier 最大内容与 CTA 固定；全部 provisional 项显式列出。

