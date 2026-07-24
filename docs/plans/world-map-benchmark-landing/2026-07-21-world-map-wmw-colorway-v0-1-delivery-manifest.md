# WMW 整屏配色方案 v0.1 交付清单

## 状态

`rejected_by_user_serious_political_tone_diagnostic_only`

用户复核确认四套虽有明确配色差异，但整体仍过于严肃、像政治游戏。下列产物只保留为“换色不足以改变体验承诺”的诊断证据，不再是待选色系。

## 唯一输入

- 版式 / 设计真源：`docs/prototypes/world-map-wmw-fullscreen-visual-style-default/wmw-colorway-base-user-selected-v0-1.png`
- 风格参考：`design/art-direction/references/clean-lowpoly-weekly-branch/benchmark-board-01.png`
- 风格参考：`design/art-direction/references/clean-lowpoly-weekly-branch/benchmark-board-02.png`

## 用户审阅入口

- `docs/prototypes/world-map-wmw-fullscreen-visual-style-default/wmw-colorway-v0-1-comparison-board.png`

## 四张完整 1920×1080 候选

| 方案 | 文件 | SHA-256 |
| --- | --- | --- |
| A 核心橄榄周刊 | `wmw-colorway-01-core-olive-v0-1.png` | `6615BF1C0E673577AB74F9A0DA6709C17A6FDED841841D2D02F44BAB8F01F9DE` |
| B 芥末黄 × 钴蓝周刊 | `wmw-colorway-02-mustard-cobalt-v0-1.png` | `F3C61612444E93CC7E29C0F633C968E70486C7497E2B7D47D742270C7FB23259` |
| C 极地青档案 | `wmw-colorway-03-arctic-teal-v0-1.png` | `C948F2692321A36FE5BCDDE3C347AF44CB2A1BC7585B749F961D307DF4195062` |
| D 黑墨 × 酸绿印刷 | `wmw-colorway-04-ink-acid-v0-1.png` | `A164EBA03FAA5A0297CE4658ED9518F384B5F7374735389FB540F0A9BDCE986F` |

## 生成源与工具证据

- 四个 `*-imagegen.png`：built-in imagegen 原生 `1672×941` 编辑输出。
- `compose_wmw_colorway_board_v0_1.py`：只做 1920×1080 尺寸归一化、标签拼版与 QA，不做调色或重绘。
- `wmw-colorway-v0-1-audit.json`：画布、边缘相关、语义采样与方案差异数据。
- `wmw-colorway-v0-1-comparison-board.png`：SHA-256 `A9AA0662084E7580B350F1E0E9B681DB32A2F514FCE607A5D608D704FFD67C07`。

## 完成项

- [x] UX 老哥先锁定语义边界。
- [x] UI Designer 再输出四套色板、材质合同与提示词。
- [x] 四套均使用真实图像生成工具独立生成。
- [x] B 修复第三任务右胶囊危险色丢失。
- [x] D 提升酸绿与灰白对比，避免与 A 只有细微差异。
- [x] 四张归一化为真实 `1920×1080`。
- [x] 2×2 对照板包含四张完整整屏，无裁切。
- [x] 全局位移审计均为 `[0,0]`。

## 未授权项

- [ ] 有文字正式稿与 confirming。
- [ ] 拆件、atlas、状态扩产。
- [ ] Godot、runtime、正式组件合同、GDD 或 frozen compact A5.1 修改。
- [ ] Git stage、commit、push。
