# WMW 右 dossier A5.1 正式接线 Loop Log

> **触发时间**：2026-07-15
> **触发原因**：父级在正式整屏肉眼复核中发现 A5.1 标题 / 图片 / 正文 / CTA 明显错位；随后又把批量查看器的差分预览误读为黑帧。
> **结论**：两类错误均已机制化修正；639–643 最终证据重出后方恢复通过口径。

## 1. 事故一：2x 纹理把合同尺寸顶回原生尺寸

首版 `WeeklyRunWorldMapRightDossierA51._make_texture()` 的顺序是：先赋 `texture`、再写合同 `size`、最后设 `EXPAND_IGNORE_SIZE`。Godot 在前两步已经把 `TextureRect` 最小尺寸钳到原生 2x 图尺寸，后补 `expand_mode` 不会自动把现有节点缩回合同值。因此：

- parent 本应为 `320×520`，实际沿用 `640×1040`；
- photo 本应为 `276×176`，实际沿用 `552×352`；
- 图片、纸页与 CTA 共同溢出，视觉上表现为标题槽空、正文压图和旧页残层。

旧测试只断言了 payload、按钮数量与交互状态，没有读取实际 `TextureRect.size`，因此逻辑全绿但视觉失败。

## 2. 事故二：宿主旧皮肤回灌

初版挂载发生在 `_apply_world_imagegen_v5_candidate_style()` 之前。后者又把旧 right dossier panel 皮肤和 `450px` 最小宽写回宿主，形成双壳风险。修正后：

- A5.1 在旧样式流程完成后挂载；
- 宿主恢复 `414px` 正式宽度与空 panel style；
- 不接收输入的深色 backdrop 完整隔离整屏旧壳烘焙的右页；
- 旧 VBox 不再因资产缺失静默复活，缺失时显式报错。

## 3. 事故三：把查看器差分预览误判成文件黑帧

一次批量 `view_image` 中，第二、第三张同尺寸图以“相对上一张的变化区”呈现，未变化区显示为黑色。父级最初把该预览误判为 SubViewport 脏帧。后续直接回读原 PNG 证明：

- 三张 alpha 均为 `255/255`；
- 页眉、左索引、地图、右 dossier 固定锚点均存在；
- 639 → 640 真实 diff 只在 `[1524,589,1850,751]`，`x<1400` 为零差异。

因此查看器预览不能替代文件像素证据。最终目检改用单张查看与折叠 / 展开右栏并排裁片。

## 4. 已落下的防线

1. `TextureRect` 构造顺序固定为 `expand_mode → texture → position/size`。
2. 固定画布启用 `clip_contents`；父级缩放时字体 token 反算，避免字号二次放大。
3. 集成测试新增 parent `320×520`、photo `276×176`、CTA `284×50` 节点尺寸断言。
4. 截图 gate 新增整帧 alpha、四区内容信号、区外状态差异与宿主 global rect。
5. 批量查看差分预览必须由 RGBA 探针 + 单图或并排板复核。
6. 规则同步到 `assetized-ui-production-chain.md` 与 `功能改动截图指引.md`。

## 5. 最终状态

- 正式集成测试与既有地区任务台 / 周循环回归通过；
- 639 collapsed、640 expanded、641 QA、642 GIF、643 manifest 已重出；
- locked disclosure 与正式地区照片仍 provisional，不借本轮事故修复偷冻结。
