# 世界地图 Dossier 袋口凸起侵入文字区 Loop Log

## 结论

用户反馈成立。North expanded 初版虽然当前两条短文案没有被完全遮住，但左右钴蓝袋角从纸张底部向上侵入约 `51–59px`，占 expanded 内容高度约 `21%–24%`，已经破坏动态文字安全区。此前只按当前字形检查“有没有压字”，没有检查载体是否仍能承载其他地区长标题与 meta，视觉通过口径不完整。

该初版 expanded 降为 `folder_protrusion_intrusion_diagnostic`，不得作为后续地区复用来源。

## 用户反馈

2026-08-21，用户将当前 expanded 与此前正交组件板并排后指出：

> “目前这两块的文件夹凸起，有点影响功能性，因为挡住文字部分了。之前你给的图里，好像没有这么严重？”

## 根因

- ImageGen 定点编辑为强调“纸插在袋中”，生成了左右对称的大斜角，物件关系表达超过功能承载需要。
- 注册审查只检测当前 North 标题和 meta 的 glyph bbox，没有把整个 `visual_write_rect` 作为零遮挡区。
- 父级用“当前字还能读”替代“任何合法动态内容都能使用相同字号与行位”。

## 修正

- 冻结 expanded slot `[27,640,414,248]` 不动。
- 文字安全区至少保持 `x=43–425, y=652–876`；其中不允许任何实心蓝色袋口、斜边或折角。
- 真实 ImageGen 定点编辑删除左右高凸起，将任务纸恢复为连续矩形，并以底部低矮钴蓝挡边表达夹持。
- expanded 仍只新增连续索引纸；不移动文字、不缩字号、不压行距、不为 North 做特例。
- 修正版：`image_gen/2026-08-21/world-map-dossier-north-text-registration-v1/10-north-dossier-expanded-runtime-468x1032.png`。

## 防复发 Gate

- 美术遮挡验收必须针对完整 `visual_write_rect`，不能只针对当前 fixture 的 glyph bbox。
- 文件夹、袋口、夹片、折边只允许侵入明确的 no-text gutter；不得靠文案避让成立。
- collapsed / expanded 复用同一袋体语义；expanded 只增加纸件，不新增独有高凸起。
- 低挡边可保留极轻微压痕与接触阴影，但不得重新抬高或演变为装甲 / 机械卡槽。
- East / Pacific 内容替换时，字号、基线和任务间距必须与 North 完全一致。

## 复审

- UX 老哥：原 expanded `FAIL / P1=2`；要求改轮廓而非挪字，并把高凸起降低 `75%–85%`。
- UI Designer：修正版 `PASS / P0=0 / P1=0`；蓝色实体已退出文字安全区，两条任务容量恢复，同壳关系成立。

## 当前状态

`pocket_lip_intrusion_closed / north_single_dossier_pending_user_confirmation`

