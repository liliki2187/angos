# WMW A261 材质与情绪三方案交付清单

## 状态

`dual_reviewed_pending_user_material_selection`

## 用户审阅入口

全部图片位于 `docs/prototypes/world-map-wmw-fullscreen-visual-style-default/`。

| 文件 | 用途 |
| --- | --- |
| `wmw-a259-v0-1-comparison-board.png` | 首屏总览；三张完整整屏同板比较 |
| `wmw-a259-01-uncoated-independent-weekly-v0-1.png` | 方案 1：无涂布独立周刊，1920×1080 |
| `wmw-a259-02-cloth-spine-special-v0-1.png` | 方案 2：当代布脊专题册，1920×1080 |
| `wmw-a259-03-fine-mesh-silkscreen-v0-1.png` | 方案 3：细网丝印增刊，1920×1080 |

## 生成源与 QA

| 文件 | 用途 |
| --- | --- |
| 三份 `wmw-a259-*-imagegen.png` | built-in imagegen 真实输出 |
| `compose_wmw_a259_material_variants_v0_1.py` | 只做 1920×1080 归一化、拼版、hash 与审计 |
| `wmw-a259-v0-1-audit.json` | 尺寸、来源、hash、共同边界与父级 / UX / UI 复核 |

## 文档

- `2026-07-22-world-map-wmw-a261-material-variants-production-brief.md`
- `2026-07-22-world-map-wmw-a261-material-variants-review.md`
- `2026-07-22-world-map-wmw-a261-material-variants-delivery-manifest.md`

## 明确未做

- 未回填真实中文、最终锁图标或 runtime 状态；
- 未制作 confirming、hover、pressed、拆图或 atlas；
- 未改 Godot、runtime、正式组件合同、GDD 或 frozen 组件；
- 未 stage、commit 或 push；
- 未把任一方案称为正式生产母本。
