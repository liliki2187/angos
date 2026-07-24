# WMW「成年怪新闻周刊」v0.2 交付清单

## 状态

`art_direction_candidates_dual_reviewed_pending_user_choice`

## 用户审阅入口

| 文件 | 用途 |
| --- | --- |
| `wmw-adult-weird-weekly-v0-2-comparison-board.png` | 唯一首屏审阅入口；A / B / C 三套完整整屏同板对照 |
| `wmw-adult-weird-weekly-01-news-frontpage-v0-2.png` | A 怪新闻头版，1920×1080 |
| `wmw-adult-weird-weekly-02-editorial-pitch-desk-v0-2.png` | B 编辑部选题桌，1920×1080，推荐方向 |
| `wmw-adult-weird-weekly-03-world-oddities-special-v0-2.png` | C 世界奇闻特刊，1920×1080 |

以上图片均位于 `docs/prototypes/world-map-wmw-fullscreen-visual-style-default/`。

## 生成与审计证据

| 文件 | 用途 |
| --- | --- |
| `wmw-adult-weird-weekly-01-news-frontpage-v0-2-imagegen.png` | A 的真实 built-in imagegen 定向编辑源 |
| `wmw-adult-weird-weekly-02-editorial-pitch-desk-v0-2-imagegen.png` | B 的真实 built-in imagegen 定向编辑源 |
| `wmw-adult-weird-weekly-03-world-oddities-special-v0-2-imagegen.png` | C 的真实 built-in imagegen 定向编辑源 |
| `compose_wmw_adult_weird_weekly_v0_2.py` | 只做裁切、尺寸归一化、宏观三栏回位、拼版与审计 |
| `wmw-adult-weird-weekly-v0-2-audit.json` | 尺寸、来源、目标区域、裁切框与双审结果 |

## 文档

| 文件 | 用途 |
| --- | --- |
| `2026-07-21-world-map-wmw-adult-weird-weekly-v0-2-production-brief.md` | 用户意图、输入权限、三方向、故事钩子与 prompt set |
| `2026-07-21-world-map-wmw-adult-weird-weekly-v0-2-review.md` | UX / UI 双审与父级结论 |
| `2026-07-21-world-map-wmw-adult-weird-weekly-v0-2-delivery-manifest.md` | 本交付清单 |

## 明确未做

- 未改 Godot 或 runtime；
- 未改正式组件合同、frozen compact A5.1、B2.12 或 GDD；
- 未回填真实中文；
- 未拆件、未做 atlas、未 stage、commit 或 push；
- 未把任一方案宣称为正式整屏母本。
