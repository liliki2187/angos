# WMW A258 三方向完整整屏交付清单

## 状态

`dual_reviewed_pending_user_selection`

## 用户审阅入口

| 文件 | 用途 |
| --- | --- |
| `wmw-a258-v0-1-comparison-board.png` | 唯一首屏入口；三套完整 1920×1080 同板比较 |
| `wmw-a258-01-light-indigo-sage-v0-1.png` | 方案 1：浅靛鼠尾草 · 轻奇闻特刊 |
| `wmw-a258-02-warm-coral-frontpage-v0-1.png` | 方案 2：暖纸柔珊瑚 · 怪新闻头版 |
| `wmw-a258-03-dusk-terracotta-midnight-v0-1.png` | 方案 3：暮蓝陶土 · 午夜增刊 |

以上图片均位于 `docs/prototypes/world-map-wmw-fullscreen-visual-style-default/`。

## 生成源与 QA

| 文件 | 用途 |
| --- | --- |
| 三份 `*-imagegen.png` | built-in imagegen 真实输出，1672×941 |
| `compose_wmw_a258_variants_v0_1.py` | 只做尺寸归一化、拼版、哈希与审计 |
| `wmw-a258-v0-1-audit.json` | 生成模式、尺寸、hash、共同资产合同与 UX / UI 复核 |

## 文档

- `2026-07-22-world-map-wmw-a258-three-direction-production-brief.md`
- `2026-07-22-world-map-wmw-a258-three-direction-review.md`
- `2026-07-22-world-map-wmw-a258-three-direction-delivery-manifest.md`

## 明确未做

- 未回填真实中文或最终锁图标；
- 未制作 confirming、hover、pressed、atlas 或拆图；
- 未改 Godot、runtime、正式组件合同、GDD 或 frozen 组件；
- 未 stage、commit 或 push；
- 未把任一方案称为正式运行时母本。
