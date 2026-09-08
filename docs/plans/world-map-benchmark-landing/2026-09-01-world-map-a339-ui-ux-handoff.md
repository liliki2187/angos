# A339 世界地图资产化前 UI / UX 交接结论

日期：2026-09-01

## 共同结论

UX 老哥与 UI Designer 一致认为：A339 当前只允许进入 `component_class_contract / assembly planning`，不能直接进入生图切件、atlas、最终 manifest、Godot 或 WeeklyRunGame。

两者共同确认：

- 页面以 `selected_region_id` 为唯一选择真值；
- selection、access、urgency、disclosure 四个维度正交；
- `selected + locked` 合法；
- 交互节点严格保持 8 个；
- Schedule、装饰、动态文字、图片和任务阅读行全部 no-hit；
- Disclosure 展开不能移动 CTA；
- A339 整屏图只能作为视觉参考，不能作为切图源；
- 第一条 vertical slice 应选择 Dossier。

## 父级合并裁决

### 采纳

1. 锁定地区仍可以被选择并完整预览。
2. 锁定只限制“进入地区”，不把整个 Dossier 降灰。
3. locked Dossier 仍允许展开只读 Disclosure，作为当前规划默认；CTA 单独进入 `locked_disabled`。
4. 键盘焦点采用两个 roving group 的实现候选：
   - Tab 进入 RegionCard 组，方向键在三卡间移动；
   - 下一次 Tab 进入 Beacon 组，方向键在三枚 Beacon 间移动；
   - 再依次进入 Disclosure 与 CTA；
   - focus 不自动改变选择，Enter/Space 才提交选择。
5. `bottom_receipt_card.json` 从当前 A339 页面装配与后续 manifest 排除，只保留历史审计身份。
6. Dossier 是第一条 vertical slice；RegionCard 为第二条重复类验证。

### 保持既有更严格约束

UI Designer 在新审查中提出 Dossier 标题最多 2 行、正文最多 3 行。父级不采纳这一放宽，继续沿用 A338 已获接受的紧凑容量：

- Dossier 地区标题：1 行，建议上限 8 个汉字；
- 新闻标题：1 行优先，极限最多 2 行；
- 导语：`16/26`，2 行，总量约 44 个汉字；
- expanded：最多 2 条只读任务；
- CTA 前保留完整呼吸区。

理由：当前视觉方向的层级已经通过；本阶段目标是装配稳定性，不应借“最大内容”重新把 Dossier 变成高密度后台表单。超限优先由内容编辑缩写和省略处理，而不是放宽层数或缩小字号。

### A305 关闭旧 RegionCard 比例阻断

A305 与 `left_region_card.json v1.0.0 / frozen` 已正式采用 RegionCard `340×170`、统一图槽与交互合同，并明确把旧 `86:41`、`204×160` 壳退役为历史 evidence。A294 并未重新打开该比例裁决；A339 早先将其继续列作阻断属于下游规划文案未同步。

- 运行时与 FrontCarrier 几何均按 `340×170`；
- 左右 `8px` transparent bleed 与独立 BackDecor 只能在该导出画布内表达，不改变 `340×170` hit rect；
- 若未来要恢复超出 2:1 的可见突出外轮廓，必须由用户明确重开并升 `left_region_card` 合同版本；当前不重开。

### 暂不冻结

- ISSUE 票签 exact rect；
- Schedule 四个文字槽与夹子 protrusion 的精确 rect；
- 三枚 Beacon 的 local position、hit wrapper、label safe rect；
- 中央 Evidence `207×132` 是否进入首批生产；当前继续 provisional / NO-HIT；
- Dossier photo frame outer rect、right bleed、lower protrusion；
- empty data 时地区是否仍可选择；
- locked CTA 是否保留 focus、如何显示锁定原因；
- 运行时中文字体与 fallback。

## 第一条 vertical slice 的目标

Dossier 只在以下五类 Gate 同时通过后，才允许复制方法到其他组件：

1. 几何：所有 frozen rect、0° FrontCarrier、no-text 区无冲突；
2. 文字：最大内容不小于 14px、不遮挡、不靠生图文字；
3. 状态：available / warning / locked / collapsed / expanded 可组合；
4. 输入：整页 no-hit，仅 Disclosure 与 CTA 可点；
5. 图片：1104×704 母图以 69:44 完整 fit 到 414×264。

通过后也只能称为 `vertical_slice_candidate`，不能称整页 runtime 通过。

## 2026-09-02 第二条 vertical slice 同步

Dossier 已完成无字 FrontCarrier、状态矩阵与最大内容视觉候选；运行时字体与 Godot 仍待后续 Gate。下一条切片转为 RegionCard：单一 `680×340` 2×无字母壳、三实例同构、`276×176` 2×图片槽、selected / warning / locked 独立 StateDecor、整卡唯一 hit rect。旧 `86:41` 不再阻断。

