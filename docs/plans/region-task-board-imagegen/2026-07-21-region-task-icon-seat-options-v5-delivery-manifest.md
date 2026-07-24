# 区域任务 pin 图标座 v5 交付清单

> 状态：`visual_options_pending_user_selection`  
> 范围：常驻任务右挂 pin 头图标座三案；未接入生产，未同步三态 compound。

## 结论

用户指出的问题成立：无内框没有破坏点击功能，但使小图标漂在大块空白纸面上，缺少“图标容器”与第二层纸件结构。旧 v4 的错误不是“有框”，而是细闭合线在原生 1×下断续。v5 因此改为比较三种能够真实缩放的美术图标座。

## 三案

| 方案 | 原生 1×结果 | 当前判断 |
| --- | --- | --- |
| A 下开口切角框 | 上、左、右连续托住图标，底部朝 pin 尖端开口 | 唯一推荐；有框但不形成闭合双框 |
| B 闭合八边纸槽 | 框最完整、最醒目 | 过重；与外 pin 轮廓形成徽章 / 盾牌套娃 |
| C 微差色切角纸窗 | 纸件语言最克制 | 回到 1×后边界偏弱，未完全关闭用户指出的空心感 |

三案是不同设计方案，不是 idle / hover / selected 三种状态。用户选定后，同一图标座才会同步进入三态美术帧。

## 产物

- 生图记录：`design/art-direction/region-task-board/2026-07-21-region-task-icon-seat-options-v5-imagegen-prompt.md`
- 候选资源：`design/art-direction/region-task-board/icon-seat-options-v5/`
- 构建脚本：`scripts/art/build_region_task_icon_seat_options_v5.py`
- Godot 夹具：`gd_project/tests/fixtures/region_task_icon_seat_options_v5/`
- Godot 捕获脚本：`gd_project/tests/capture_region_task_icon_seat_options_v5.gd`
- 1× / 4×标注 QA：`docs/screenshots/2026-07-21-region-task-icon-seat-options-v5/01-icon-seat-options-imagegen-1x-qa.png`
- 1920×1080 Godot 真实地图：`docs/screenshots/2026-07-21-region-task-icon-seat-options-v5/02-godot-icon-seat-options-1x.png`

## 冻结项

- pin `64×80`
- runtime icon `[18,14,28,28]`
- hit `72×80`
- anchor `[36,76]`
- compound `278×80`
- selected 类型色后纸及 `3–4px` 露边
- title / meta / caption rect
- idle → hover → selected 状态时序
- dense、cluster、clamp 和 event card

## 当前推荐

推荐 A。它在树林和低多边形折面上仍能立即形成图标承托，底部开口又避免复制外 pin 的闭合轮廓。若用户选择 A，下一步只把 A 同步到 default pin-only、hover compound 和 selected compound，再输出原生 1×三态静态图与 hover → selected 动图；B / C 不继续生产化。

美术指导、UI Designer 与 UX 老哥对真实生图板和 Godot 原生 1×地图分别复核后，均把 A 判为唯一 GO，且均要求 A 在三态中逐像素保持位置、尺寸、线宽和颜色不变。B 因闭合双框 / 内层按钮感判 NO-GO；C 因 1×过弱、未关闭空心感判 NO-GO。三方最终均为 `P0=0 / P1=0 / P2=0`（针对 A）。

## 本次请用户判断

1. A 是否已经达到“图标周围有框、画面不空”，同时没有 B 的套娃感。
2. 若不选 A，是更偏好 B 的完整框，还是 C 的纸窗层次。
