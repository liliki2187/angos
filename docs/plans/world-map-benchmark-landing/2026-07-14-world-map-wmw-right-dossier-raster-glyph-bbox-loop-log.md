# WMW 右侧 dossier 文字框错位 Loop Log

> 日期：2026-07-14
> 产物类型：`loop_log / qa_correction / not production art / not Godot runtime`
> 触发来源：用户在 563 合同板截图中指出，粉色框与“北美禁区警戒带”“高危”“推荐12”等文字位置明显不对应。
> 结论：563-566 的文字位置证据是假阳性，必须降级；v0.8.5 合同槽位几何本身不受影响。
> 影响：旧 `8/8 fit` 不再可引用，改由 567-570 的实际光栅字形 bbox 证据替代。
> 下一步：clean-sprite brief 只能引用 570；进入 Godot 后还要用目标字体按同一口径重跑。

## 一、原始问题

旧脚本先用 Pillow 的 `textbbox((0, 0), text, font)` 得到字形宽高，再丢弃返回值中的 `left/top` bearing；随后以绘制原点 `(x, y)` 和 `width/height` 合成 `[x, y, x+w, y+h]`，同时用这个假 bbox 画粉色框并判定 fit。

实际探针显示：

| 文案 | 字号 | `textbbox((0,0))` | 被丢弃的 top bearing |
| --- | ---: | --- | ---: |
| `北美禁区警戒带` | 32px | `(0,8,224,40)` | 8px |
| `高危` | 26px | `(0,6,52,32)` | 6px |
| `推荐12` | 19px | `(0,5,62,25)` | 5px |

因此旧粉框从绘制原点开始，而真实墨迹要到下方 5-8px 才出现。用户看到的错位不是截图缩放误差，也不是合同槽移动，而是 QA 工具绘制了一个不存在的字形盒。

## 二、为什么反复出现

1. 排版、overlay 和 manifest 没有共享一份可验证的实际字形结果，各自相信“宽高足够”等同于“位置正确”。
2. 旧 gate 只比较字形宽高是否小于 inner rect，未检查实际绝对 bbox 是否完整位于 inner rect。
3. 同一个错误 bbox 同时负责修复和验收，形成自证闭环；粉框看似提供了证据，实际上只是把错误算法可视化。
4. 旧脚本未覆盖中文字体 bearing、拉丁下伸部、不同水平对齐方式等回归用例。
5. 563-566 因此复发 F1“验证等级冒充”：工具生成成功被误写成视觉 `8/8 fit`。

## 三、机制修复

- 新增 `scripts/ui-contracts/wmw/wmw_text_layout_metrics.py`：先把每组 `字体 + 字号 + 文案` 真正光栅化，从 alpha 非透明像素提取 bbox；排版时反向补偿 left/top bearing。
- 排版结果、粉色 QA 框和 manifest 只消费同一个 `raster_glyph_bbox`，不再允许 `draw_origin + size` 的 synthetic bbox。
- 新增 `scripts/ui-contracts/validate_text_bbox_evidence.py`：不调用生产侧 bbox helper，而是根据 manifest 中的字体文件、字号、文案和 draw origin 独立重光栅；再检查 overlay bbox 等于重放结果、实际字形位于 inner rect、bbox 来源为 `raster_alpha_bbox`、没有手调 y 偏移。
- 新增 `scripts/ui-contracts/wmw/test_wmw_text_layout_metrics.py`：覆盖中文标题、状态、混合数字、拉丁下伸部，以及 left/center/right 三种对齐。
- 同步收紧 `text_carrier_capacity`，把实际字形绝对包含关系和校验器列为必需证据。

## 四、证据替换

- 563-566：保留审计，但文字 bbox 与 `8/8 fit` 结论作废；566 已标记 `invalidated_text_bbox_overlay_false_pass_superseded_by_570`。
- 567：以实际 raster alpha bbox 重画正式合同板。
- 568：default / warning / locked 三状态压力板，粉框逐项贴合真实墨迹；三状态仍为 `8/8 fit`，最小运行时字号仍为 18px。
- 569：1280x720 整屏位置回填；不改变已采纳的 v0.8.5 几何。
- 570：记录逐字段 `draw_origin / font_metric_bbox / raster_glyph_bbox / inner_rect / margins` 与校验结果。

## 五、宣称边界

- A189 采纳的右侧下半部信息架构和 v0.8.5 rect 不撤回，本轮没有修改 frozen 几何。
- 567-570 是脚本字体的合同与容量证据，不是生产美术、atlas 或 Godot runtime。
- clean-sprite brief 可以继续，但最终字体进入 Godot 后必须重新生成实际字形 bbox；代理字体通过不能替代目标引擎字体通过。
