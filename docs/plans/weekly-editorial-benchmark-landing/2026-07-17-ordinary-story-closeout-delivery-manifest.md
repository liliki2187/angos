# 普通报道图资产序列阶段交付清单

## 决策条

- **结论**：1003–1006 普通报道图资产已获用户确认并通过当前结构宿主中的映射 / 交互 / 容量验证；整屏发刊编辑界面仍是未包装的程序化结构稿，不是最终效果。
- **影响**：manifest v7 只能记录“报道图资产在结构宿主中通过”，不能记录“编辑器侧收口、整屏包装完成、最终 UI 或生产候选”。
- **下一步**：暂停自动扩产其它 B / C 级资产；先对现有整屏做 UX 诊断与桌面 16:9 UI 包装方案，再由用户确认是否进入资产化落地。

## 交付清单

- **交付对象**：`article_id=1003 / 1004 / 1005 / 1006` 普通报道图序列及其在当前程序化结构宿主中的运行状态。
- **产物类型**：`runtime_state_preview`。
- **宿主阶段**：`unpackaged_programmatic_structure_host`；顶部状态、候选池、工作区外壳、发刊复核、按钮与大部分文字 / 边框仍为程序化控件。
- **它能证明**：用户已通过 A225 确认 1006；四张普通报道图的 `article_id + role` 映射通过 `25/25` 定向审计；当前结构宿主交互通过 `42/42`；`0/6、3/6、5/6、6/6` 四态的双版几何稳定、候选数 / 已填数互补、默认换稿按钮为 `0`。
- **它不能证明**：整屏视觉包装、最终信息层级、候选池 / 签批区物件化、图文功能融合、生产 UI、完整 weekly smoke、后续 B / C 级资产或整屏生产真源已经通过。
- **截图汇总**：`docs/screenshots/2026-07-17-weekly-editorial-ordinary-story-closeout/00-capacity-closeout-contact-sheet.png`，由四张真实 `1920×1080` Godot 窗口截图排版组成。
- **单态截图**：同目录下 `01-godot-capacity-0-of-6.png`、`02-godot-capacity-3-of-6.png`、`03-godot-capacity-5-of-6.png`、`04-godot-capacity-6-of-6.png`。
- **容量审计**：`docs/screenshots/2026-07-17-weekly-editorial-ordinary-story-closeout/capacity-audit.json`，四态全部通过。
- **交互审计**：`docs/screenshots/2026-07-15-weekly-editorial-same-paper-local-replace/interaction-audit.json`，`42/42` 通过。
- **资产审计**：`docs/screenshots/2026-07-16-weekly-editorial-blue-phone-booth-b-slice/standard-story-asset-audit.json`，`25/25` 通过。

## Gate 结果

| Gate | 结果 | 说明 |
| --- | --- | --- |
| 用户视觉确认 | PASS | A225 已记录 1006 单图与六版位全填充预览确认 |
| 普通报道图定向审计 | PASS | `25/25` |
| 发刊编辑器交互回归 | PASS | `42/42` |
| 四容量态运行截图 / 审计 | PASS | `0/6、3/6、5/6、6/6` 全通过 |
| 整屏视觉包装 | NOT STARTED | 当前仍是程序化结构宿主，仅局部报刊资产接入 |
| `test_phase_flow.gd` | PASS | 本轮重新运行 |
| `test_settlement_result.gd` | PASS | 本轮重新运行 |
| `test_weekly_run_layout.gd` | FAIL / TEST DRIFT | 22 项全部指向已隐藏 / 已替换的 legacy 节点；现行替代结构测试 `86/86` 通过，正式 smoke 尚待同步 |

## 边界与异常记录

- 首次调用周流程脚本被 Windows 执行策略阻止；随后只对本次进程使用 `-ExecutionPolicy Bypass` 运行，没有修改系统策略。
- 首次容量态临时截图脚本因两个局部变量缺少显式 `bool` 类型而解析失败；修正后重新运行成功，失败轮没有生成或混入交付截图，临时脚本已删除。
- 最终复跑 42 项交互审计时，受限沙箱内的 Godot 连续两次在输出测试结果前发生原生 `signal 11`；改用同一可执行文件、同一项目和同一测试脚本在沙箱外复跑后退出码为 `0`，审计文件仍为 `42/42` 通过。该异常按运行环境稳定性记录，不抹除，也不改写为功能失败。
- 22 项布局失败已完成只读归因：它们来自 legacy WorldView / RegionView / StatsPanel 测试漂移，不是本轮报道图或现行 WMW / 地区任务板的视觉回归；正式 smoke 未同步前仍不能写“完整 weekly smoke 通过”。
- 用户在 2026-07-17 进一步指出当前整屏只是粗糙程序结构上加入报刊资产；复核截图与 `WeeklyRunEditorialPhase.gd` 后确认判断正确。先前“编辑器侧收口”标签属于验证等级冒充，现已降级。
- 本轮没有改玩法规则、常量或系统边界，不修改 GDD；STATUS、A225 与 manifest 状态已同步。
- 本轮没有新增 UI / 新布局，也没有新增或编辑图片资产，因此不触发 UI / UX 双 agent 或真实生图链。

## 放行边界

- **已放行**：普通报道图资产序列及其在当前结构宿主中的运行证据。
- **未放行**：整屏视觉包装、最终 UI、生产候选、完整 weekly smoke、全局回归冻结、后续 B / C 级资产与整屏真源升格。
- **允许下一步**：按改进现有 UI 的双 agent 顺序，先由 UX 诊断当前整屏，再由 UI Designer 输出桌面 16:9 包装稿、元素表和资产化边界；测试漂移可作为独立工程清理。
- **禁止跳到**：自动扩产、自动选择下一资产类别、把局部图片与运行验证 PASS 汇总成界面包装或最终 UI PASS。
