# WMW 左卡 B2.9 无涂抹状态徽章复审材料

> 版本：B2.9 / v0.9.15
> 日期：2026-07-10
> 当前状态：`visual_fail_badge_core_facet_asymmetry`，不是冻结生产资源。B2.9 已修复右侧涂抹，但用户复核确认新建内芯的低多边形 X 形分界明显歪斜。
> 本轮范围：只修 B2.8 状态徽章右侧暴露的程序涂抹；照片、地球、文字 token、卡体尺寸和合同 frozen 字段均未改。

## 一、B2.8 为什么会出现涂抹

B2.8 先对旧 badge 足迹 `(284..382,196..295)` 执行 700 轮 `harmonic_inpaint()`，再把左移后的新底盘盖上去。新底盘没有覆盖旧足迹最右侧，导致扩散生成的像素直接成为最终可见纹理。探针区 `x374..382,y196..295` 内，旧足迹 `576px`、新底盘覆盖 `177px`、裸露 inpaint `399px`。程序只检查“旧语义像素是否消失”，没有检查“替代纹理是否来自真实底板 / 外框”，因此形成假阴性。

## 二、B2.9 结构修复

1. 重新量测候选 B 原始外环。approved 外环 bbox 为 `[288,201,376,291]`，中心 `(332,246)`，1x 右视觉留白 `16px`；该外环与右框本来就是合格美术，不再退役或重画。
2. 仅重建外环包围的语义内芯 `CORE_MASK`，bbox `[302,216,362,277]`。该掩膜与 approved 外环像素交集为 `0`，完整覆盖旧靶心环与中心点。
3. 内芯使用显式低多边形状态色纹理；四状态只对内芯做框色家族映射。勾 / 靶心 / 警示三角 / 锁继续作为独立运行时透明 PNG。
4. 管线中不调用 inpaint、模糊、扩散或色带生成。内芯以外的像素不得变化，右侧走廊也不得变化。

这次不是把涂抹“盖住”，而是删除产生涂抹的操作：候选 B 合格外观逐像素保留，程序只拥有语义内芯。

## 三、关键 Gate

| Gate | 结果 | 可核验依据 |
| --- | --- | --- |
| `retired_footprint_texture_continuity` | PASS | `harmonic_inpaint=false`、`blur_or_diffusion=false`、内芯外变化 `0px`、右侧走廊变化 `0px`、外露 inpaint `0px` |
| approved 外环保留 | PASS | `1983/1983px` 与候选 B 源像素一致；bbox `[288,201,376,291]`；1x 右留白 `16px` |
| 旧状态语义清理 | PASS | 内芯奶油语义像素 `0`；旧靶心原样像素 `0` |
| `runtime_icon_shape_completeness` | PASS | 四状态 padding `>=4px`，border touch `0`，非目标像素 `0` |
| `badge_state_color_consistency` | PASS | selected / available / warning hue 差分别 `0.0001 / 0.0024 / 0.0002`；locked 低饱和明度差 `0.0705` |
| Gate A-F / edge residue / alpha / green residue | PASS | 四边旧图签名 `0`、窗口 alpha 无洞、非 selected 绿残留 `0`、四状态窗口 diff `0`、比例 `1.275` |
| Godot windowed capture | PASS | Godot `4.6.2-stable` + windowed OpenGL3；527/528 非黑；QA 相对 normal 丢失采样 `0` |
| 16 点视觉复核 | `evidence_ready` | 525 已逐帧展示地球弧下、窗口右缘、窗口下缘、状态徽章；最终视觉裁决归用户 |

## 四、执行方目检记录

| 状态 | 地球弧下 | 窗口右缘 | 窗口下缘 | 状态徽章 |
| --- | --- | --- | --- | --- |
| selected | 未见旧月牙或缝隙 | 原框纹连续；selected 绿光仅在外缘 | 未见旧图带 | 用户复核 FAIL：共同内芯分面 X 歪斜；运行时勾本身完整 |
| available | 未见旧月牙或缝隙 | 原框纹连续，无青色色带 | 未见旧图带 | 用户复核 FAIL：519 空底盘清楚显示分面 X 歪斜；靶心本身未截断 |
| warning | 未见旧月牙或缝隙 | 原框纹连续，无纵向涂抹 | 未见旧图带 | 用户复核 FAIL：共同内芯分面 X 歪斜；三角本身完整 |
| locked | 未见旧月牙或缝隙 | 原框纹连续，无灰色扩散带 | 未见旧图带 | 用户复核 FAIL：共同内芯分面 X 歪斜；锁本身完整 |

以上原执行方判断只构成局部证据；用户对状态徽章内芯的最终结论为 FAIL，优先级高于执行方自检。

## 五、用户复核后的降级结论

用户指出的歪 X 来自 `neutral_core_texture()` 的四块程序色面，不是旧图层残留。B2.9 右侧无涂抹、approved 外环保留和运行时图标完整等局部结论仍有效，但整体视觉已降级为 `visual_fail_badge_core_facet_asymmetry`。详细根因与下一轮冻结修法见：

`docs/plans/world-map-benchmark-landing/2026-07-10-world-map-wmw-left-card-b2-9-core-facet-symmetry-loop-log.md`

## 六、证据索引

- 519：候选 B / 失败 B2.8 / B2.9 放大对照，直接显示涂抹移除与外环保留。
- 520：纯照片、完整运行时图标、地球线稿与四状态空底盘配料板。
- 521：B2.9 2x atlas。
- 522：几何 QA。
- 523/524：Python 运行时回填 / QA。
- 525：四状态 × 四检查点 16 点视觉证据板。
- 526：B2.9 manifest。
- 527/528：Godot 4.6.2 windowed 单组件截图 / QA。

## 七、流程沉淀

- 设计采纳 A176：资产退役区域禁止以 inpaint / 模糊 / 扩散 / 色带作为最终可见纹理；保留合格外框时只重建其语义内芯。
- `retired_footprint_texture_continuity` 成为冻结 gate：程序必须证明外露修补像素为 `0`，不能只证明旧像素消失。
- 后续遇到“外框合格、内芯语义需替换”的组件，先把外框与内芯的所有权分开；外框不进入重建掩膜，运行时语义不回烘 atlas。
- 本轮未调用 imagegen，未修改 `design/ui-contracts/world-map/` frozen 字段，未生产其它 class。
