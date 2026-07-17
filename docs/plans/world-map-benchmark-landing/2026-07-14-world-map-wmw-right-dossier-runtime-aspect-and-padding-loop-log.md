# Loop Log：右 dossier 候选 A 的 Python / Godot 装配漂移

> **产物类型**：错题复盘 / workflow loop log。
> **触发**：用户在 585 局部截图中指出 header 不齐、正文贴左、照片拉伸。

## 错误结论

588 曾写双 agent 复核 P0/P1=0、可进入用户视觉裁决；但该结论只结合了 Python bbox、非黑 / 颜色多样性和整屏目检，没有验证 Godot 照片的实际缩放矩阵，也没有把 header 实际 ink 共轴与正文真实颜色模块内边距列为 gate。

## 事故链

1. Python 使用 `cover_image()`，Godot 通用 `_add_texture()` 使用 `STRETCH_SCALE`，两套 runtime 规则不一致。
2. `348x128` 左卡横幅被复用为 `276x176` 右 dossier 照片，素材用途和比例从源头不匹配。
3. manifest 只检查照片窗 alpha、色键残留和截图非黑，没有 `image_aspect_pass`，因此 73.4% 相对纵向变形仍能通过。
4. Python 正文有约 7px 参考尺度内缩，Godot 直接使用完整 `region_body`；588 的 Python 字形 bbox 无法证明 Godot 真实位置。
5. header 三槽分别独立居中，未定义共同光学轴；“各自在框内”被误当成“组成一行”。

## 已有规则为何没有生效

`docs/workflows/ui-geometry-and-text-safety-gates.md` §4 已明确禁止非等比拉伸，§5 已要求 `visible_color_module_rect -> carrier_rect -> inner_rect -> glyph_bbox`。本次不是缺规则，而是 manifest 和 capture 没把规则变成可执行断言，双 agent 又没有索取 source/target 尺寸与变换证据。

## 修正律

- 同一视觉证据的 Python / Godot 必须加载同一份精确比例 ingredient；不得各自临时适配源图。
- 图片 manifest 必须记录 raw source、production source、ingredient、runtime slot、crop rect、统一缩放系数与 hash，并断言 `scale_x == scale_y`。
- Godot capture 在创建照片节点前先比较 texture 与 slot 比例；偏差超过 `0.5%` 直接退出 1，禁止视觉兜底。
- 文字 pass 必须来自目标引擎真实 inner rect；Python 证据只能作为同构预检。
- 混合尺寸 header 必须声明共同 optical axis，并以实际 ink bbox 验收。

## 停止条件

候选 A 原 588 降级。只有新照片按已落盘规格真实生成、Python / Godot 同构、三项 P1 均有局部截图证据后，才可重新进入用户视觉裁决；不得把非黑截图或 bbox containment 单独写成视觉通过。
