# 派遣签批台中央主物件实验记录

> 日期：2026-06-22  
> 状态：结构方向实验 / not production benchmark  
> 起因：用户指出按新参考图生成的真实内容风格稿与参考图视觉差异过大；经 `angus_art_director` 与 `ux_laoge` 复核，问题不是材质不够，而是缺少参考图的“中央强主物件”构图。

## 1. 实验产物

| 文件 | 目的 | 结论 |
| --- | --- | --- |
| `docs/screenshots/2026-06-22-dispatch-signoff-central-object-experiment/01-central-object-dispatch-board-experiment-a.png` | 第一次把中央区改成外勤地图签批板 | 主物件感明显增强，但太旧、太机械、铆钉和磨损过重。 |
| `docs/screenshots/2026-06-22-dispatch-signoff-central-object-experiment/02-central-object-dispatch-board-experiment-b-clean.png` | 清理 A 的旧机械感 | 更干净、更接近参考图，但仍有一些卡片面板感。 |
| `docs/screenshots/2026-06-22-dispatch-signoff-central-object-experiment/03-central-object-dispatch-board-experiment-c-short-stamps.png` | 压缩判断尺、压低底部列表感、强化红青线路 | 当前优选实验方向；不回退，但仍不是生产标杆。 |

## 2. 当前判断

C 相比 V17.2 面板式稿，已找回参考图的关键视觉逻辑：

- 中央是一张外勤地图签批板，而不是多块并列面板。
- 选中员工、空槽、随队器材、判断章都贴附在主板上。
- `78% / 13>8 / 无缺口` 被压成短判断章，降低数据仪表盘感。
- 红青线路开始承担“任务 -> 队伍 -> 器材 -> 签批票据”的结构语言。
- 右侧签批票据仍保留最终结论和 CTA。

仍需修正：

- 底部资源抽屉仍有列表感，需要更像从主板下方抽出的纸件 / 票据带。
- 左侧任务卷宗纸件偏多，深蓝负空间仍可再增加。
- 候选员工与器材入口还可以更像 pinned dossier slips / printed tags，减少通用按钮感。
- 角色头像风格后续仍需 `angus_character_pixel_director` 专审。

## 3. 下一步建议

继续沿 C 方向做一轮“资产合同化”而不是继续大范围抽卡：

1. 反推 C 的 `content_rects / no_text_rects / hit_rects` 草案。
2. 把中央主板拆成：深蓝主板、折纸地图基底、队伍 slip 槽、器材 slip、三枚判断章、红青路线层。
3. 把底部抽屉默认态压成推荐 4 人 + 器材短槽 + 更多候选；hover 再展开。
4. 将按钮语义改为贴签 / 压章 / 夹条 / 机械按点。
5. 仅在上述合同成立后，再继续高保真单组件或 Godot 回拼。
