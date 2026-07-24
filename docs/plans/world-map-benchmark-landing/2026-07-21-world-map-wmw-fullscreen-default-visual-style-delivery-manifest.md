# WMW v5.1 默认态完整整屏视觉风格稿交付清单

## 交付目的

给用户一张可以直接判断整体美术方向的完整 1920×1080 默认态玩家视图，不再以孤立小组件承担整屏风格审批。

## v0.1 撤回

- `docs/prototypes/world-map-wmw-fullscreen-visual-style-default/wmw-fullscreen-default-filled-style-v0-1.png` 已被用户判定左栏视觉混乱，状态改为失败证据，不再作为有效审阅入口。

修正版必须使用 v0.2 文件名，并继续只展示完整玩家视图。

## v0.2 再次撤回

v0.2 虽清除了双 carrier，但日程器仍为 `[36,810,342,246]`，与三卡 `[66,y,306,240]` 不共轴；用户判定为明显基础错误，v0.2 不再是有效候选。

## 当前唯一用户审阅入口

- `docs/prototypes/world-map-wmw-fullscreen-visual-style-default/wmw-fullscreen-default-filled-style-v0-3.png`

v0.3 只重排日程器外框与内部槽位；三张卡、中央与右栏相对 v0.2 的差异像素均为 0。用户判断左栏四外壳是否已明显同轴统一，以及完整整屏是否可接受。

## 技术附件

- `wmw-fullscreen-default-filled-style-v0-1-audit.json`：v0.1 失败状态与原始审计。
- `wmw-fullscreen-default-filled-style-v0-2-audit.json`：v0.2 几何、文字、源层权限与左栏区外回归。
- `wmw-fullscreen-default-filled-style-v0-3-audit.json`：v0.3 共轴硬 Gate、文字安全区与 v0.2 区外回归。
- `wmw-fullscreen-default-filled-style-v0-3-alignment-qa.png`：内部 200% 对齐检查，不交用户审阅。
- `render_wmw_fullscreen_default_style_v0_1.py`：可复现装配脚本。
- `wmw-fullscreen-default-imagegen-source-v0-1.png`：built-in imagegen 无字源，只是技术输入，不作为用户独立审阅图。
- `2026-07-21-world-map-wmw-fullscreen-visual-style-default-production-brief.md`：输入权限、冻结 rect、真实内容、色材与最终 imagegen prompt。
- `2026-07-21-world-map-wmw-fullscreen-default-visual-style-review.md`：UI / UX 复核与父级裁决。

## Gate

| 检查 | 结果 |
| --- | --- |
| 1920×1080 完整玩家视图 | PASS |
| v5.1 rect 与三栏容量 | PASS |
| 真实中文内容与 44 条安全区 | PASS |
| 中央地图第一、右档案第二、CTA 唯一主动作 | PASS |
| 3 pin / 4 任务 / 1 CTA / 0 路线 | PASS |
| 红线状态章已删除 | PASS |
| UI Designer | PASS，P0=0 / P1=0 / P2=0 |
| UX 老哥 | PASS；父级核实后 P0=0 / P1=0 / P2=1 |
| 左栏占位载体复用 | 0，PASS |
| v0.2 中央与右栏回归 | 0 diff pixels，PASS |
| v0.2 用户复核 | FAIL：左栏外壳不共轴 |
| v0.3 左栏共轴 | PASS，0px 容差 |
| v0.3 UI Designer | PASS，P0=0 / P1=0 / P2=0 |
| v0.3 UX 老哥 | PASS，P0=0 / P1=0 / P2=0 |
| 用户风格采纳 | V0.1 / V0.2 REJECTED；V0.3 降级为功能几何证据；V0.4 未生成 |

## 后续修订

用户已继续否决 v0.3 的美术完成度：v0.3 只保留为功能与几何证据，不再是 `PENDING` 美术候选。下一有效交付必须按 `2026-07-21-world-map-wmw-fullscreen-art-pass-v0-4-production-brief.md` 制作完整整屏 art pass；v0.4 尚未生成。
| Godot / 正式合同 / atlas / confirming | NOT STARTED BY DESIGN |

## 下一步限制

只有用户接受默认态整屏方向后，才可复用同一底图制作仅日程区域变化的 confirming 回归；该回归通过后再讨论组件拆分与资产化顺序。当前不得宣称风格已冻结。
