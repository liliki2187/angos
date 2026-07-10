# WMW 左卡 B2.7 合同对齐 badge 复审材料

> 版本：B2.7 / v0.9.13  
> 日期：2026-07-10  
> 当前状态：`evidence_ready_pending_user_visual_review`，不是冻结生产资源。  
> 本轮范围：只重建 badge 底盘与运行时图标锚点；照片、地球、框体、纸签、文字 token 与冻结合同均未改。

## 一、修复目标

B2.6 的 selected badge 同时显示旧靶心圆弧和 runtime 勾号，并且旧八角环与合同图标中心错位。本轮不再扩大清理半径或调整图标遮住残影，而是：

1. 整区退役旧 badge 足迹；
2. 按冻结 `action_badge` 重建无语义底盘；
3. 状态字形只由 runtime icon 层绘制；
4. 空底盘先验收，再允许叠图标。

## 二、关键实现

- 脚本：`scripts/ui-contracts/wmw/wmw_v0913_left_card_b27_contract_badge_pipeline.py`。
- 旧 badge 足迹用纯几何多边形整体重建，未使用颜色连通组件保留旧环。
- 新外环 bbox：`[318,214,390,286]`；中性内芯 bbox：`[331,227,377,273]`；合同中心：`(354,250)`。
- 中性内芯由四块低对比多边形材质构成，不含靶心、圆弧、三角、锁或勾的可识别语义。
- 四状态从 available 单母版换色；状态字形全部从 atlas 移出。
- 四个 runtime icon 等比收进 42×42 设计盒，Python / Godot 共用合同中心。

## 三、证据

| 编号 | 内容 | 判读口径 |
| --- | --- | --- |
| 499 | 四状态无图标空底盘 400% 板 | 先看底盘本体是否有旧语义残影 |
| 500 | B2.6 失败底盘 vs B2.7 合同对齐底盘 | 红框为冻结 action badge，青十字为合同中心 |
| 501 | B2.7 2x atlas | atlas 中无状态字形 |
| 502 | 冻结槽位几何 QA | 外环 / 内芯与 action badge 同心 |
| 503/504 | Python 运行时回填 / QA | 每帧只叠一个 runtime icon |
| 505 | 四状态 × 四检查点证据板 | 执行方只写 evidence_ready |
| 506 | manifest | 程序 gate 与禁止项真源 |
| 507/508 | Godot windowed 运行截图 / QA | 真实 4.6.2 + OpenGL3，禁 headless |

## 四、程序 Gate 结果

| Gate | 结果 | 依据 |
| --- | --- | --- |
| `badge_clean_base_no_semantic_residue` | PASS | 旧足迹原样像素 0；内芯奶油语义像素 0；源字形复制 0 |
| `badge_geometry_contract_alignment` | PASS | 外环 / 内芯 bbox 精确；中心误差 0.5px |
| runtime icon purity + bounds | PASS | 四状态非目标像素 0；bbox 全在内芯；中心误差 ≤0.5px |
| Gate A-F / edge residue / green residue | PASS | 照片与镂空壳既有链未回退；比例 1.275 |
| Godot windowed capture | PASS | 507/508 均为 1920×1080；颜色数 54844 / 54733；非黑像素 2072502 / 2073600 |
| 16 点视觉检查 | `evidence_ready` | 505 已生成，最终 PASS/FAIL 归用户 |

## 五、执行方目检说明

- 499 空底盘：四状态均未见旧靶心浅色线、暗色圆弧、双环或矩形贴片边。
- 503 Python：四个图标均只出现一次，和新八角环同心。
- 507 Godot：selected 勾号不再叠旧靶心；available / warning / locked 同样未见双层符号。
- 以上只表示证据已准备并完成执行方自检，不替代用户视觉裁决。

## 六、双 agent 与美术守门意见

### UX 老哥诊断原文

- P0：0。
- P1：状态语义曾由 atlas 残影与 runtime icon 双重承载；clean-base gate 只查浅色字形造成假干净；证据顺序把最终合成放在空底盘之前；`evidence_ready` 文案仍有过度宣称风险。
- 固定验证顺序：源 → 空底盘 → 换色底盘 → runtime 图标配料 → 合成 → Godot。
- 必须新增 `badge_clean_base_no_semantic_residue`，`ingredient_purity` 只证明图标，颜色 gate 只证明色相；空底盘应单独验收后才能叠图标。

### 美术指导诊断原文

- 放弃在旧靶心底盘上的减法清理。
- 用显式几何八角奶油环重建外环，不允许依赖连通组件保护；内芯使用 4-6 个低对比色面、左上略亮右下略暗并保留轻微印刷颗粒，禁止纯色矩形补丁。
- 状态语义只由 runtime icon 承载；本轮只动 action badge，照片、地球、纸签和其它壳体层保持不动。
- 先出无图标 400% 底盘板，再看运行时叠层。

### UI Designer 交接原文

- 冻结槽 `[316,212,392,288]`，中心 `(354,250)`。
- 外环 bbox `[318,214,390,286]`，72×72，14px 切角；内切 bbox `[328,224,380,276]`；中性内芯 bbox `[331,227,377,273]`。
- runtime icon 设计盒最大 42×42，必须完全位于中性内芯，且与外环共用中心；Python / Godot 中心差 ≤1px。
- 旧视觉中心不在合同槽时应重建到底盘合同几何，不得继续迁就旧中心。

## 七、等待用户裁决

请重点看 499 的空底盘和 507 的真实 Godot 叠层：若右下 badge 已不再呈现旧圆弧、双环或不同心叠层，可接受 B2.7 作为下一轮冻结候选；否则继续停在左卡，不开启其它 class。

