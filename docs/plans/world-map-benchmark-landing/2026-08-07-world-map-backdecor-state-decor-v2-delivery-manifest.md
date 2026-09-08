# 世界地图 BackDecor / StateDecor v2 交付清单

> 日期：2026-08-07  
> 状态：`visual_dual_review_pass_pending_user_visual_gate`  
> 下一门：用户认可后进入 Godot 节点集成与真实运行时验证；当前不得宣称 runtime / production 放行。

## 结论

本轮将 A291 的约 `10%` 纸层厚度、编辑桌接触感、手绘状态语言和黑色幽默证物重新映射到已冻结的正交功能件。Dossier、Schedule、CTA、Disclosure、真实中文、`69:44` 图片和 hit rect 均未移动；新增资产只属于 `BackDecor / StateDecor / StoryDecor`，不消费输入。

UI Designer 与 UX 老哥最终均判视觉层 `PASS / P0=0 / P1=0`；UX 进一步确认 `P2=0`。该结论只放行用户视觉裁决与下一阶段 Godot 集成，不替代真实节点树、输入树、状态切换和 windowed capture 证据。

## 真实美术来源

新增四类源件均由 Codex 内置 ImageGen 生成在 `1:1` 品红色键画布：

- Dossier 冷蓝灰窄长后页；
- Schedule 暖灰白横向后页；
- 哑光低多边形长尾夹；
- 冷蓝证物底托。

复用的真实 ImageGen 资源：

- UFO 无字涂鸦便签：源 PNG 不含中文；`不是飞碟。／大概。` 由 `RuntimeText` 绘制，归 `StoryDecor`。
- Eye 源接触表：拆为 `EyeBase / SelectedUnderlay / WarningNotch / LockedEye`，不再使用带 selected 的 warning 整态。
- 北美 canonical 新闻图：复用 `north_america_story_1104x704.png`，证物簇显示为 `207×132`，严格 `69:44`、完整 UV、无裁切。

程序只负责色键转透明、alpha 裁切、合同等比下采样、状态源拆层、BackDecor 轻旋转、接触阴影、排版和 QA；没有程序重画纸材、夹子、UFO、Eye 或新闻图。

## 迭代记录

1. 首张夹子因连续金属高光与产品摄影体积感被拦截。
2. 第二张夹子因过扁、手柄过高和矢量图标感被拦截。
3. 第三张以紧凑比例、5–8 个哑光块面与离散明度阶进入候选。
4. v1 双审指出中央证物簇仍像漂浮小物件，且 warning/selected 未独立；整批判 `ITERATE`。
5. v2 加入冷白＋冷蓝双底托，三窗条退出最终簇并换为同一 canonical 新闻图；Eye 完成独立组合层，UFO 明确为 `StoryDecor + RuntimeText`。
6. 标签保护区 `[714,322,170,70]` 在独立证物层中透明切断，保留原运行时标签与手绘圈断口。

## 机器 Gate

`10-backdecor-state-decor-validation.json`：`all_pass=true`。

- 四张主板均为 `1920×1080`；
- 四类新增源件透明角通过；
- 可见品红残边 `0`；
- 所有运行时归一化只下采样，上采样 `0`；
- Dossier `468×1032`、Schedule `372×246` 与 frozen 资产精确匹配；
- 新 hit rect `0`；
- `warning_unselected=[EyeBase, WarningNotch]`，selected / warning 独立；
- UFO 源无文字、文案由 RuntimeText 承担；
- 北美 canonical 图以 `207×132` 严格复用；
- 四个 Eye 组合层尺寸和 WarningNotch 非空通过。

## 用户主审入口

- `image_gen/2026-08-07/world-map-backdecor-state-decor-v1/06-real-ui-backdecor-reinsert-preview.png`：真实内容整屏回填预览。
- `image_gen/2026-08-07/world-map-backdecor-state-decor-v1/07-a291-vs-real-ui-comparison.png`：A291 并排与 Dossier / Schedule 局部。
- `image_gen/2026-08-07/world-map-backdecor-state-decor-v1/05-independent-asset-board.png`：独立透明资产与层级合同。
- `image_gen/2026-08-07/world-map-backdecor-state-decor-v1/08-layer-safety-qa.png`：冻结矩形、装饰包络和标签保护区。

## 附件

- 生图提示词：`00-imagegen-prompts.md`
- 审计：`09-backdecor-state-decor-audit.json`
- 校验：`10-backdecor-state-decor-validation.json`
- 可复现脚本：`scripts/ui-contracts/wmw/build_world_map_backdecor_state_decor_v1.py`
- 夹具偏差 Loop Log：`2026-08-07-world-map-backdecor-clip-render-language-loop-log.md`
- 首轮双审前产物：同目录 `iteration1-*`，只作迭代审计。

## 下一阶段边界

用户视觉认可后只允许：

1. 在 Godot 中建立 `BackDecor / FrontCarrier / RuntimeImage / StateDecor / RuntimeText / HitRect` 节点层级；
2. 将所有装饰节点设为 `MOUSE_FILTER_IGNORE / FOCUS_NONE`；
3. 复验 selected / warning / locked 独立组合、canonical 资源引用、完整 UV 和零新增热区；
4. 输出真实 `1920×1080` windowed 截图与交互 GIF。

本轮不放行地区卡、ISSUE、atlas、manifest 或正式生产冻结。地区卡 `2:1` 与旧 `86:41` 冲突、ISSUE exact rect 未冻结的问题仍需单独关闭。

