# Ticket / Sticker Color Contract v0.1

> 状态：临时色彩检查，用于纠正 v0.6 过亮问题。  
> 基准图：`design/art-direction/references/clean-lowpoly-weekly-branch/premium-sticker-reference-crop.png`，辅以 `benchmark-board-01.png` / `benchmark-board-02.png`。  
> 候选边界：v0.5 = 太土暗泥；v0.6 = 太亮太白。  
> 说明：本轮使用自动 mask / 聚类抽样，不是最终固定 ROI，因此只能作为 v0.7 prompt 色彩合同草案；生产候选仍需固定 ROI 复采样。

## 1. 关键结论

- v0.6 的纸边 / 高亮纸面明显过白：标杆约 `#C2BAAC`，v0.6 为 `#F3E8D9`，luma 高约 `+46.6`。
- v0.6 的橄榄绿过亮、偏黄：标杆约 `#4E623D`，v0.6 为 `#747945`。
- v0.6 的警示红橙过鲜：标杆锈色区间约 `#6D462D`，v0.6 为 `#BD4F26`。
- v0.6 不能整体压暗：青蓝 token 反而比标杆更暗，标杆约 `#384946`，v0.6 为 `#24313C`。下一轮必须分 token 调色。

## 2. Token 对比

| token | 标杆参考 | v0.5 边界 | v0.6 边界 | v0.6 相对标杆 | 判断 |
| --- | --- | --- | --- | ---: | --- |
| `paper_high` | `#C2BAAC` | `#D1C0A9` | `#F3E8D9` | luma `+46.6` | 明显过白、过亮 |
| `paper_mid` | `#B2AB9B` | `#C9B8A0` | `#AAA992` | luma `-3.8` | 接近，可作为内纸低值参考 |
| `warm_ivory` | `#BCB4A5` | `#D0C0A8` | `#CAC7B8` | luma `+17.9` | 偏亮 |
| `olive_mid` | `#4E623D` | `#5E5F31` | `#747945` | luma `+25.1` | 过亮、偏黄 |
| `olive_dark` | `#435737` | `#484C25` | `#596133` | luma `+11.5` | 偏亮 |
| `teal_blue` | `#384946` | `#2F4647` | `#24313C` | luma `-22.1` | 偏暗，不能继续整体压暗 |
| `warning_rust` | `#6D462D` | `#882C14` | `#BD4F26` | luma `+22.9` | 过鲜、过亮 |
| `ink_dark` | `#272A2B` | `#080F19` | `#1E2C39` | luma `+0.5` | 明度接近，但偏蓝 |
| `bg_dark` | `#191C1E` | `#080F19` | `#17212D` | luma `+4.2` | 略亮、偏蓝 |

## 3. v0.7 调色目标

优先目标：

- `paper_high` 回到 `#C2BAAC` 附近，允许区间约 `#BEB5A6` - `#C9C0B0`；禁止 `#E8DCCB` 以上的亮白纸边。
- `paper_mid` 使用 `#B2AB9B` - `#BCB4A5`，不要把可写区推成 `#F2E6D7`。
- `olive_mid` 回到 `#4E623D` - `#5B6A37`；禁止 `#747945` 这种黄亮橄榄。
- `olive_dark` 回到 `#3F4C2D` - `#435737`。
- `warning_rust` 使用低饱和锈红 / 红棕，目标约 `#6D462D` - `#8A4E32`；禁止鲜红橙 `#BD4F26`。
- `teal_blue` 不要继续压黑，目标约 `#384946` / `#293C41`。
- `ink_dark` 使用 `#191E1F` - `#272A2B`，避免 v0.5 的死黑 `#080F19`。

负面边界：

- 不要全局提亮。
- 不要全局压暗。
- 不要惨白纸边、奶油白、米黄纸板、棕黄旧档案、鲜艳警示橙、死黑投影。
- 纸面亮度、橄榄绿和红橙必须分别匹配标杆；不能用“整体看着高级”覆盖 token 偏差。

## 4. v0.7 Prompt 色彩约束

```text
Match the sampled benchmark palette exactly: warm off-white sticker edges around #C2BAAC, mid paper around #B2AB9B to #BCB4A5, olive green around #4E623D and dark olive around #435737, muted rust warning color around #6D462D to #8A4E32, teal-blue dark accents around #384946, ink dark around #272A2B, deep board dark around #191C1E. Preserve sampled palette; do not globally retone the image. Avoid bright white paper (#F3E8D9), yellow-bright olive (#747945), saturated orange-red (#BD4F26), dead black shadows (#080F19), muddy brown paper, craft-paper look, and vintage archive yellowing.
```

## 5. v0.7 / v0.8 复采样记录

生成样本：

- v0.7：`docs/screenshots/2026-06-24-world-map-benchmark-landing/13-ticket-symbol-atlas-v0-7-benchmark-palette.png`
- v0.8：`docs/screenshots/2026-06-24-world-map-benchmark-landing/14-ticket-symbol-atlas-v0-8-color-corrected.png`

自动 mask 复采样结果：

| token | 标杆 | v0.6 | v0.7 | v0.8 | v0.8 判断 |
| --- | --- | --- | --- | --- | --- |
| `paper_high` | `#C2BAAC` | `#F3E8D9` | `#C9B79F` | `#CBB9A1` | 基本收回，不再亮白 |
| `paper_mid` | `#B2AB9B` | `#AAA992` | `#C4B198` | `#C9B79F` | 仍偏亮，需在真实中文填充时看可读性 |
| `olive_mid` | `#4E623D` | `#747945` | `#53582F` | `#4F532C` | 不再黄亮，但略暗、偏土，需保留低多边形层次 |
| `teal_blue` | `#384946` | `#24313C` | `#233E41` | `#1E3234` | 仍偏暗，后续不能继续压暗 |
| `red_orange` | `#6D462D` - `#8A4E32` | `#BD4F26` | `#792B13` | `#783214` | 已从鲜红橙收回，仍需防止棕黑化 |
| `ink_dark` | `#272A2B` | `#1E2C39` | `#081118` | `#0C1114` | 仍偏死黑，后续应把图形墨色抬回深灰墨 |
| `background_dark` | `#191C1E` | `#17212D` | `#071018` | `#0C1114` | 仍偏黑，界面整合时需看与主背景关系 |

阶段结论：

- v0.8 是目前最接近的小组件候选：它解决了 v0.6 的亮白和 v0.5 的泥厚问题。
- v0.8 仍不是生产 atlas：深墨、背景、青蓝偏暗；纸面可写区略亮且还有纸纹，需要真实中文填充检查。
- 下一步应把 v0.8 放进右侧 dossier / 左侧地区卡的小范围真实 UI 里验证，而不是继续单独无限修 atlas。

## 6. 用户复核：v0.8 并未与标杆同色

2026-06-24 用户追问“确定目前色号一样吗”。使用用户重新贴出的标杆裁图
`C:/Users/GZFANG~1/AppData/Local/Temp/codex-clipboard-44fd6e17-d601-4e88-9126-957d411d089b.png`
与 v0.8 做同一套自动 mask 复采样，结论是：**没有同色，只是部分 token 比 v0.6 更接近**。

| token | 标杆 | v0.8 | RGB 距离 | 亮度差 | 结论 |
| --- | --- | --- | ---: | ---: | --- |
| `paper_high` | `#C2BAAC` | `#CBB9A1` | `14.2` | `+0.4` | 亮度接近，但 RGB 未同色 |
| `paper_mid` | `#B2AB9B` | `#C9B79F` | `26.2` | `+13.8` | 偏亮 |
| `warm_ivory` | `#BCB4A5` | `#CBBAA1` | `16.6` | `+7.2` | 略偏亮 |
| `olive_mid` | `#4E623D` | `#4F532C` | `22.7` | `-11.8` | 偏暗、偏土 |
| `olive_dark` | `#435737` | `#454B25` | `21.7` | `-9.4` | 偏暗 |
| `teal_blue` | `#384946` | `#1E3234` | `39.1` | `-23.3` | 明显偏暗 |
| `red_orange` | `#45382F` | `#783214` | `58.0` | `+4.6` | 色相 / 饱和度不同 |
| `ink_dark` | `#272A2B` | `#0C1114` | `43.4` | `-25.2` | 明显死黑 |
| `background_dark` | `#191C1E` | `#0C1114` | `19.7` | `-11.3` | 偏黑 |

后续约束：

- 不得再说 v0.8 “色号一样”或“颜色通过”。
- v0.8 只能作为当前视觉方向候选，不是色彩通过样本。
- 若要追求同色，必须建立固定 ROI / 吸管采样表，并对生成图做复采样；单靠 imagegen prompt 不能保证 exact hex。

## 7. v0.9 调色复采样

样本：

- `docs/screenshots/2026-06-24-world-map-benchmark-landing/15-ticket-symbol-atlas-v0-9-palette-match.png`

v0.9 相比 v0.8 明显改善，但仍不能称为完全同色。

| token | 标杆 | v0.8 | v0.9 | v0.9 RGB 距离 | v0.9 亮度差 | 结论 |
| --- | --- | --- | --- | ---: | ---: | --- |
| `paper_high` | `#C2BAAC` | `#CBB9A1` | `#C1B6A2` | `10.8` | `-3.8` | 接近 |
| `paper_mid` | `#B2AB9B` | `#C9B79F` | `#B5AB96` | `5.8` | `+0.3` | 接近 |
| `warm_ivory` | `#BCB4A5` | `#CBBAA1` | `#B7AC98` | `16.1` | `-7.7` | 改善但未同色 |
| `olive_mid` | `#4E623D` | `#4F532C` | `#515A36` | `11.0` | `-5.6` | 接近但略暗 |
| `olive_dark` | `#435737` | `#454B25` | `#474F30` | `11.4` | `-5.3` | 接近但略暗 |
| `teal_blue` | `#384946` | `#1E3234` | `#2F403E` | `15.0` | `-9.0` | 改善但仍偏暗 |
| `red_orange` | `#45382F` | `#783214` | `#6D331D` | `44.1` | `+3.6` | 色相 / 饱和度仍不同 |
| `ink_dark` | `#272A2B` | `#0C1114` | `#131719` | `32.9` | `-19.1` | 仍偏黑 |
| `background_dark` | `#191C1E` | `#0C1114` | `#131719` | `9.3` | `-5.2` | 接近但略暗 |

阶段结论：

- v0.9 是目前色彩最接近标杆的小组件候选。
- 纸面与橄榄基本可进入真实 UI 验证。
- 若继续追色，下一版只应处理 `ink_dark`、`teal_blue`、`red_orange` 三个 token；不要再动纸色和橄榄。
- 由于 imagegen 无法保证 exact hex，若目标是“色号完全一致”，应转为固定 ROI + 后期调色 / LUT / 分层资源流程，而不是继续纯 prompt 生图。

## 8. v0.10-v0.16 三 token 修色记录

样本：

- v0.10：`docs/screenshots/2026-06-24-world-map-benchmark-landing/16-ticket-symbol-atlas-v0-10-three-token-fix.png`
- v0.11：`docs/screenshots/2026-06-24-world-map-benchmark-landing/17-ticket-symbol-atlas-v0-11-ink-teal-red-fix.png`
- v0.12：`docs/screenshots/2026-06-24-world-map-benchmark-landing/18-ticket-symbol-atlas-v0-12-ink-lift.png`
- v0.13：`docs/screenshots/2026-06-24-world-map-benchmark-landing/19-ticket-symbol-atlas-v0-13-local-color-corrected.png`
- v0.14：`docs/screenshots/2026-06-24-world-map-benchmark-landing/20-ticket-symbol-atlas-v0-14-smooth-color-match.png`
- v0.15：`docs/screenshots/2026-06-24-world-map-benchmark-landing/21-ticket-symbol-atlas-v0-15-smooth-graphite.png`
- v0.16：`docs/screenshots/2026-06-24-world-map-benchmark-landing/22-ticket-symbol-atlas-v0-16-minimal-clean-color.png`

关键复核：

| token | 标杆 | v0.10 | v0.15 | v0.16 | v0.16 判断 |
| --- | --- | --- | --- | --- | --- |
| `paper_high` | `#C2BAAC` | `#C1B5A2` | `#C1B5A2` | `#C1B5A2` | 稳定，接近 |
| `paper_mid` | `#B2AB9B` | `#B6AA96` | `#B6AA96` | `#B6AA96` | 稳定，接近 |
| `olive_mid` | `#4E623D` | `#4D5131` | `#4E5231` | `#4D5131` | 稍暗，但未回到 v0.6 黄亮 |
| `teal_blue` | `#384946` | `#2F3E3F` | `#354543` | `#324241` | 明显改善，v0.15 数值更近但有斑点 |
| `red_orange` | `#45382F` | `#683821` | `#673D27` | `#693C24` | 仍不同；标杆裁图缺少可比红色 ROI，不能按 exact red 判定 |
| `ink_dark` | `#272A2B` | `#15191B` | `#191C1E` | `#181B1D` | 仍偏暗；全图 mask 被背景占比污染 |
| `background_dark` | `#191C1E` | `#15191B` | `#191C1E` | `#181B1D` | 接近 |

版本取舍：

- v0.11 / v0.12：没有有效抬起墨色，且部分色块变暗；不升级。
- v0.13 / v0.14：数据改善，但暗按钮和红按钮出现局部斑点；只能作为 LUT 实验，不适合作为视觉候选。
- v0.15：背景和青蓝数据最好，但斑点最明显；不采用。
- v0.16：数据不是最极限，但视觉最干净，是当前小组件色彩候选。

后续约束：

- 若继续追 `ink_dark`，必须改用固定 ROI 吸管点，例如单独框选 `WWW` 黑色笔触、三角眼图标笔触、手掌暗形、背景空场。全图自动 mask 已经不能区分背景和墨线。
- 若目标是生产可控色号，应使用“生图底稿 + 分层/局部 LUT 校色”流程；纯 imagegen 只用于生成形状与低多边形手绘感。
