# WMW 左卡 B2.6 运行时 badge 图标层误判 Loop Log

> 日期：2026-07-09  
> 触发：用户复核 497 Godot 截图，指出右下角 selected badge 符号明显多层叠加错乱。  
> 结论：B2.6 降级为视觉失败；此前 `evidence_ready` 判读遗漏了 atlas clean badge base 内的旧靶心暗色残影。

## 一、实际问题

用户框出的 selected badge 不是单纯“运行时勾图标偏大”，而是：

- runtime icon PNG 自身只有奶油色勾，透明背景；
- atlas 里的所谓“干净 badge 底盘”仍保留旧 available 靶心的暗色圆弧 / 阴影 / 内芯残影；
- 勾图标叠到这个残影上，形成不同语义层的叠加错乱。

因此 B2.6 的核心裁决“壳侧 badge 底盘清空状态字形及抗锯齿 / 阴影残留”没有真正满足。

## 二、为什么会漏判

1. **gate 只查奶油色字形像素，没有查暗色语义残影**  
   `atlas_baked_state_glyph_pixels = 0` 只说明奶油色线条被清掉，不说明旧靶心的暗色底影被清掉。B2.6 的旧靶心残影正好不属于奶油色，因此骗过了该 gate。

2. **`ingredient_purity` 只证明图标配料干净，不能证明底盘干净**  
   四个 runtime icon 的 non-target=0 是真结论，但它只覆盖独立 PNG 配料；底盘层仍可能夹带旧语义图形。

3. **目检对象错位**  
   490 展示了空 badge 底盘，但执行自检没有把“空底盘是否仍有旧靶心暗色残影”列为独立检查点；495 / 497 看到的是“底盘 + runtime icon”合成结果，我把它误读成图标叠层成立，而没有回头拆层看底盘。

4. **上一轮教训没有被完整程序化**  
   B2.5 的问题是“形状贴片未清旧字形导致叠影”；B2.6 只把“字形”理解成浅色线条，未把阴影 / 内芯残影纳入同一缺陷家族。

## 三、当前降级

- 496 manifest 中的程序 gate 仍可作为机器证据，但视觉状态必须降级：`manual_16point_visual_check = fail`，`derived_art_quality_check = fail`。
- B2.6 不是生产候选，不得冻结，不得批量生产其它 class。
- 下一轮不得继续以“调图标尺寸 / 锚点”作为主修法；先重建 badge clean base，再谈运行时图标。

## 四、必须补的新 gate / 目检项

新增目检项：`badge_clean_base_no_semantic_residue`。

判据：

- 在未叠 runtime icon 的 atlas / shell 中，badge 内芯不得出现任何可被识别为旧状态符号的暗色圆弧、靶心、三角、锁、勾影子；
- 该项必须在叠运行时图标前单独截图；
- `atlas_baked_state_glyph_pixels = 0` 不能替代本项。

可程序化方向：

- clean badge base 应使用无状态语义的底盘重建，不再从带靶心的 available 原帧直接清浅色线条；
- 若继续用程序补底，必须对 badge 内芯做结构性平滑 / 纹理一致性 probe，而非只测奶油色像素。

## 五、下一轮建议

B2.7 应先解决壳层：

1. 从 available 母版里完整清空 badge 内芯的旧状态符号影响区，包含浅色线条、暗色阴影、圆弧和内芯残影。
2. 用同一 badge 底盘纹理重建内芯，保留外八角环与整体材质。
3. 先产出“空 badge 底盘四状态”对比板，过 `badge_clean_base_no_semantic_residue` 后，才允许叠 runtime icon。
4. runtime icon 的尺寸 / 锚点作为第二步调，不得用它掩盖底盘残影。
