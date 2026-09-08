# 世界地图 North Dossier 文字注册 v1 交付清单

## 结论

North America 单卡已完成 `468×1032` collapsed / expanded 文字注册视觉候选。上一张三联稿的“文字对齐程序矩形、程序补纸、自由缩字”问题已关闭。本轮只证明一张 Dossier 的真实纸面与动态内容可以共同成立，状态为：

`north_single_dossier_text_registration_visual_target / pending_user_confirmation`

## 用户主审图

1. `image_gen/2026-08-21/world-map-dossier-north-text-registration-v1/09-north-dossier-collapsed-runtime-468x1032.png`
   - SHA-256：`49BCE30EF889B998E570B339ED9B3115C0D7571824E314335E4805BB80C45191`
2. `image_gen/2026-08-21/world-map-dossier-north-text-registration-v1/10-north-dossier-expanded-runtime-468x1032.png`
   - SHA-256：`CD552B3453570E0DB52A9F61AB97C7AF25B113D03E45282BD8A314A28B5A1097`

## QA 证据

- `image_gen/2026-08-21/world-map-dossier-north-text-registration-v1/11-north-dossier-registration-qa-1920x1080.png`
  - SHA-256：`BD965D08F82A4BB09630F9A4C40CB049CF10F4FEE5752E90D1080A143E02BB2E`
  - 用途：说明 BaseSkin 同源、ExpandedPreviewSkin 唯一增量、Photo 规格、Disclosure / CTA hit 边界和固定 type token；不作为玩家视觉目标。

## 美术来源

- 无字 BaseSkin：`04-imagegen-registered-base-shell.png`
  - 真实 ImageGen 生成；SHA-256：`185BEB8523244A8759F5625EAA610053B5207A0DECB621E6C970DA06B2128C0B`
- expanded 连续索引纸修正版：`12-imagegen-expanded-low-lip-shell.png`
  - 真实 ImageGen 定点编辑；将左右高凸起改为底部低挡边；SHA-256：`66BA8E713F3812CAB0A484620A2D8E319A15D84E4DAE0FFF6A7D8136D2D54400`
  - 最终 prompt：`13-imagegen-low-lip-edit-prompt.md`
- 照片：`gd_project/Assets/prototypes/world_map_integrated/a_style_v2_runtime/north_america_story_1104x704.png`
  - 以 `414×264 / 69:44` 完整等比回填，不裁切、不拉伸、不生成缩略图。

程序脚本 `06-compose-north-registered-runtime.py` 只负责既有 ImageGen 美术模块的带状注册、canonical 图片回填、固定字号文字与 QA 排版；没有绘制纸张、边框、按钮底板、任务卡或状态章。

## 关闭的问题

- kicker 不再穿过中央夹子禁区；
- title / status / photo / headline / body / Disclosure / preview / CTA 均对齐实际可见载体；
- 禁止逐字段 `fit_text`，所有字段使用固定字号与基线；
- expanded 两条任务位于同一张连续索引纸，第二条位于真实分隔线下方；
- 正文、Disclosure 和任务 meta 的可读对比已提高；
- `＋/－` 状态反馈强度已统一；
- “已显示 2 / 共 4 条”只在 Disclosure 承载一次；
- 左右高袋角已退出完整动态写入区，低挡边只压住无字纸边，不再要求第二条任务避让；
- 玩家主审图没有 proof rail、fixture badge 或程序补纸。

## 双审结果

- UX 老哥：初审 `CONDITIONAL PASS`；三项条件关闭后无 P0，用户所指“强行拼贴 / 文字未长在组件里”已实质关闭。
- UI Designer：终审 `PASS / P0=0 / P1=0`，可作为 North 单卡文字注册视觉目标。
- 用户指出袋口侵入后，UX 补充诊断原 expanded 为 `FAIL / P1=2`；真实 ImageGen 轮廓修正后，UI Designer 再审 `PASS / P0=0 / P1=0`。复盘见 `2026-08-21-world-map-dossier-pocket-lip-text-intrusion-loop-log.md`。

## 继续冻结

- 当前不是整屏 filled-state、生产资产、atlas、manifest 或 Godot runtime 截图；
- 不证明 East / Pacific 内容替换与完整状态矩阵；
- 不证明实际引擎字体、hover、row hit 或 CTA / Disclosure 接线；
- `红线升温` 仍为 `PENDING / CAPACITY ONLY`；
- 用户确认 North 前，不复制另外两地区，不进入 Godot 或 `WeeklyRunGame`。
