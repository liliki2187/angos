# 发刊中央双版区域母件 v1 交付清单

## 结论

中央双版区域母件 v1 已完成真实生图、合同几何回正、六篇真实报道回填和未来态整屏合成，但用户复审判定文字与图版配合很差、没有报刊感且不如程序版。此前 UI Designer / UX PASS 已撤回；v1 降级为几何与材质证据，不得冻结或反向拆层。这不是 Godot 正式界面。

## 用户审阅图

1. `01-central-spread-master-v1-native.png`：`1040×920` 无字区域母件；只审纸张、书脊、六个照片框与钴蓝语言。
2. `02-central-spread-master-v1-filled.png`：`1040×920` 六篇真实报道组合；只审主 / 副 / 普通三级层级、图文密度和双页阅读节奏。
3. `03-weekly-editorial-future-state-v1.png`：`1920×1080` 中央完成区＋左右 / 顶栏目标风格代理；只审中央是否仍为第一视觉锚点和综合色彩是否成立。

证据目录：`docs/screenshots/2026-07-22-weekly-editorial-central-spread-master-v1/`。

## 内部修正记录

- 初版真实生图母件的六个照片槽没有遵守冻结版位内部顺序，UI Designer 判 FAIL。
- 改用真实生图空白双版纸面作为底层，把真实生图照片凹槽和蓝色折角按冻结合同矩形重新排回；程序没有绘制纸张、书脊、折角或框体美术。
- 第二轮左下页边 L 形角标侵入专题 1 meta，UI Designer 判 PASS WITH CHANGES；通过真实生图定向编辑移除四个外侧角标后，最终 UI 与 UX 均 PASS。

## 几何与层级

- 中央区域：整屏 `[420,96,1040,920]`。
- 六组 `headline / photo / meta` 均写入 `audit.json`；主标题 `28px`、副标题 `22px`、普通标题 `14px`。
- 主、副头版均使用横图；四个普通位使用方形 / 近方形图片框。
- 照片折角位于照片矩形内，不侵入 headline；页边角标已移除。

## 生图与程序边界

- 初始双版母件：`image_gen/2026-07-22/20260722-weekly-editorial-central-spread-master-v1-source.png`。
- 清空动态文字安全区母件：`image_gen/2026-07-22/20260722-weekly-editorial-central-spread-master-v1-clean-source.png`。
- 空白纸面：`image_gen/2026-07-22/20260722-weekly-editorial-central-spread-master-v1-blank-base-v2.png`。
- 程序入口：`scripts/art/build_weekly_editorial_central_spread_master_v1_preview.py`。
- 程序操作只包含缩放、真实生图配料裁切 / 重排、真实内容回填、动态文字覆盖与整屏粘贴；`program_drawn_visible_art=false`。

## 冻结边界

- 用户通过中央区域前，不反向拆层，不制作四态，不扩产左栏候选报道抽屉。
- 未修改正式 Godot、组件合同、GDD 和正式资产 manifest。
- 用户通过后，下一生产单位是从该区域母件反向拆出中央纸面与六个版位，再做重组差分；下一审阅区域才是左侧候选报道抽屉。
