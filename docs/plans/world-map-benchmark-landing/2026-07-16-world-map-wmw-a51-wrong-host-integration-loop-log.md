# WMW A5.1 错宿主接线 Loop Log

> **结论**：639-643 接入的是旧 `GLOBAL CHANNEL / WeeklyRunGame` 世界地图；随后又把 575 组件回填 / 资产盘点板误认成页面结构真源。两层宿主判断均作废，当前结构真源回到 `30-v2-2-3-clean-right-function.png` 与同目录 `production-contract.md`。
> **影响**：A5.1 组件级方向与 629-638 仍有效，但“正式整屏接线通过”撤回。
> **下一步**：先锁定新 WMW 整屏宿主身份，再做接线；不得在旧场景继续补丁。

## 1. 触发

2026-07-16 用户看到 639 后指出：右 dossier 被放回很久以前的旧界面。第一次对照确认 639 含 `GLOBAL CHANNEL` 顶栏、旧左侧装订索引与旧底部频道回条，但纠偏时又错误地把 575 当作当前整屏结构。用户继续指出：575 的右 dossier 与下方票据形成错误堆叠，右下只有一组符号资产而没有正经功能。复核 `docs/screenshots/2026-06-23-world-map-clean-lowpoly-style-target/production-contract.md` 后确认，575 只是组件尺寸、对齐和同屏回填证据；真正结构真源是 `30-v2-2-3-clean-right-function.png`。

## 2. 原问题与影响

- `WeeklyRunWorldMapRightDossierA51` 的局部尺寸、折叠 / 展开和生产数据绑定可以成立；
- 但它被挂到错误整屏，639-643 只能证明“组件能在旧页面运行”，不能证明“当前 WMW 页面已经落地”；
- 575 只能证明 B2.12、地图、A5.1、底票据和符号资产可以被放在一张盘点板中，不能证明这些对象具有正确父子关系、功能必要性或页面分区；
- 575 的第三张底票进入右栏水平投影，右下等距符号组又具备工具栏外观，导致“右侧地区决策区”被读成 dossier、票据和伪功能图标的混合堆栈；
- 24 项组件测试、15 项下游测试、非黑帧与局部 diff 都没有检查页面身份，因此在错误问题上给出了正确答案；
- UX / UI 终审的输入提示也把“正式 WeeklyRunGame”写成既定前提，导致评审只检查右栏局部，没有反向审查宿主是否正确。

## 3. 失败原因

1. 把用户的“继续落地”解释为“接入仓库里现成的生产场景”，没有重新确认当前整屏真源。
2. 因 `WeeklyRunGame` 已有 `WorldDetailPanel` 和 production payload，按工程便利性选择宿主，错误地替代了视觉路线判断。
3. `STATUS.md` 很长，且对话经历多次上下文压缩；压缩摘要保留了“正式运行接线”动作，却弱化了“WMW 新整屏仍在资产化组装阶段”。这是诱因，但不是免责理由。
4. 缺少 `screen_identity_gate`。现有 gate 检查了组件、数据、alpha、尺寸与差分，却没有检查整屏的身份锚点。
5. 新增的 `screen_identity_gate` 只要求“有一张整屏参考”，却没有先验证参考图本身的产物类型，因而允许组件回填 / 资产盘点板冒充页面结构真源。这是同一 F1 错误家族的第二层复发。

## 4. 复发判定

命中 `ai-collaboration-guidance.md` 的 F1“验证等级冒充”：局部组件在错误宿主中运行，被写成目标整屏正式落地。F1 计数更新；本轮新增机器可读 `screen_identity_gate`，不再只补文字提醒。

## 5. 当前处理

- 639 / 640 / 641 / 642 / 643 统一标记为 `invalidated_wrong_host`，不得再引用为正式 WMW 整屏通过证据；
- 575 继续保留 v0.8.6 组件同宽、同中心与同屏尺度审计价值，但降级为 `component_reinsert_review_board`，不得再引用为页面结构、功能必要性或 runtime 宿主证据；
- A211 对 A5.1 原位展开结构的用户采纳继续有效；629-638 继续是组件级评审证据；
- 旧 `WeeklyRunGame` 接线代码暂不继续扩写，也不据此生产其它 class；清理与正确接线需在整屏宿主确认后做定向修改；
- `STATUS.md`、A211、A5.1 复审文档同步撤回“正式接线完成”口径。

## 6. 防复发门槛

运行时整页接线前必须先提交 `screen_identity_gate`：

- 明确目标场景 / 页面文件与一张当前整屏真源截图；
- 先声明真源截图的产物类型；只有 `screen_structure_target` / 已批准的运行整屏可以定义页面结构，组件回填板、contact sheet、QA 板和资产盘点板一律不能；
- 写出至少四个身份锚点与禁止锚点；
- WMW 当前正向锚点为：左侧四状态卡栈、中央低多边形世界地图、右侧独占的 A5.1 地区决策栏、只在左 / 中栏下方出现的全局日程与辅助入口、右侧唯一进入地区 CTA；
- 禁止锚点包括 `GLOBAL CHANNEL` 顶栏、旧装订索引、旧频道回条、跨入右栏的底票据、右下无功能 icon strip、与进入 CTA 同级的第二功能条；任一出现即整屏失败；
- 首张接线截图必须和目标整屏并排，不得只看组件局部；
- 子 agent 的 prompt 必须要求先判断“是否为正确页面”，再评局部 UI。

## 7. 沉淀

- `docs/workflows/workflow-gates.yml`：新增 `screen_identity` hard gate；
- `docs/onboarding/assetized-ui-production-chain.md`：阶段 9 增加整屏身份通行证；
- `docs/onboarding/ai-collaboration-guidance.md`：F1 更新本次复发与门槛。
- 本次二次纠正进一步把 `target_reference_artifact_type` 纳入 hard gate：先判参考图是不是结构真源，再比较运行截图是否匹配，禁止“拿错参考图但比对通过”。
