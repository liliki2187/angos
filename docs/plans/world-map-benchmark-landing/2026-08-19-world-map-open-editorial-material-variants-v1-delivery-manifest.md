# 世界地图开放编辑材料式三方向风格稿 v1 Delivery Manifest

## 结论

三张均由 Codex 内置 ImageGen 使用两张正式 benchmark 作为唯一正向美术真值、v4 只作为冻结功能构图参考分别生成。当前只供用户比较组件身份，不是生产视觉目标。

双审排序：`B > C > A`。

推荐吸收关系：`B 的开放钴蓝稿夹母构图＋A 的主照片校样权重＋C 的单张故事便签`。若下一张表现 Disclosure 展开态，四条任务必须落在一张连续索引纸上，不得沿用 C 的四张独立任务纸。

## 交付物

| 方向 | 文件 | 原生尺寸 | SHA256 | 当前裁决 |
| --- | --- | --- | --- | --- |
| A 照片校样主导 | `image_gen/2026-08-19/world-map-open-editorial-material-variants-v1/01-variant-a-photo-proof-led-imagegen-native.png` | `1672×941` | `48A17D6B2941CE25F083798957657668454173CB63BFE8817E74376A51607C06` | donor only；主照片关系可吸收，Disclosure 状态和报告清单感失败 |
| B 标题剪版主导 | `image_gen/2026-08-19/world-map-open-editorial-material-variants-v1/02-variant-b-headline-pasteup-led-imagegen-native.png` | `1672×941` | `EF4B111CE4BC931FEEDF5429BD04800780FB9481DDB21265B477EE3F1D626111` | `CONDITIONAL PASS`；推荐母构图 |
| C 媒介混编主导 | `image_gen/2026-08-19/world-map-open-editorial-material-variants-v1/03-variant-c-mixed-media-field-packet-imagegen-native.png` | `1672×941` | `3AFC8DDC2FC8EC5BC4553A8E4F2926CE7089BCA45CB5640ACEF19C3AB7288BE0` | donor only；便签与展开态可吸收，左卡同构和任务假交互失败 |
| Prompt set | `image_gen/2026-08-19/world-map-open-editorial-material-variants-v1/00-prompt-set.md` | 文档 | — | 记录共同约束与三方向差异 |

## UX / UI 双审摘要

### A

- 已离开纯公司报表，但中下段仍像完成的报告清单。
- `任务情报·4 [+]` 与可见四条冲突。
- 右上化学结构纸回流科研机构联想。
- 左侧三卡统一和主照片叙事权重可保留。

### B

- 遮字后仍能分辨母夹、标题纸、照片校样、资料索引和行动签，最符合 A316。
- collapsed `＋` 与隐藏条目自洽。
- 左卡同构、地图关系和唯一 CTA 均成立。
- 下一步须把照片、标题、摘要、Disclosure 和 CTA 全部严格锁回 `0°`，并降低标题 / 摘要纸条的按钮感。

### C

- 一张洗衣机故事便签显著增加编辑者存在与低剂量黑色幽默。
- expanded `－` 与四条内容自洽。
- selected 01 图片槽明显大于 02 / 03，违反同构。
- 四张任务纸与综合色标签像四个独立入口；若任务只读，必须改成一张连续索引纸。

## 下一张建议

若用户选择继续，建议只生成一张明确 expanded filled-state：

- 使用 B 的整屏和 Dossier 母结构；
- 使用 A 的主照片面积与权重；
- 使用 C 的一张缩小芥末故事便签，限制在 Dossier 外矩形内并标记 NO-HIT；
- Disclosure 使用 `－`；
- 四条任务印在一张连续索引纸上，等行高但无单元格、无独立卡阴影、无强 action chip；
- 所有功能面 `0°`；
- 左侧三张 RegionCard 图槽完全同构；
- CTA 面积和字号不得超过主照片权重。

## 未证明与冻结边界

- 生图只能证明概念级同源内容，不能证明同一 `1104×704 / 69:44` 位图逐像素复用。
- exact rect、动态文字容量、FrontCarrier、Disclosure / CTA hit rect、状态 atlas 和真实字体尚未验证。
- ISSUE exact rect 与地区卡 `2:1 / 86:41` 冲突继续未冻结。
- 不进入组件拆分、透明化、atlas、资产 manifest、Godot 或 `WeeklyRunGame`。
