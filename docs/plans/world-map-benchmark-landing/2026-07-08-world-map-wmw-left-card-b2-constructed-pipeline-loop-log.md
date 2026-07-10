# Loop Log：B2 配料化拼装试点中的右缘误判

> 日期：2026-07-08  
> 范围：WMW `left_region_card` B2 / v0.9.6

## 触发

执行中发现严格合同槽版 B2 虽然机器 gate 通过，但右侧仍可能被看成“轨道”；随后尝试照片窗口扩到 x408 / x400，Godot 真实截图显示照片层压住右框并产生外探感。

2026-07-09 用户继续基于 445 截图指出第二张“欧洲灰域”的更根本问题：照片左上未贴合地球圆弧，照片下方露出底板 / 另一层图片，右侧仍有不自然接缝。这证明 B2 的失败不只是右缘 18px，而是整个照片窗口形状、位置和遮挡关系没有正确建模。

## 错因

配料化拼装方向是对的，但第一次心智模型仍漏了一个层：

`plate -> photo -> icon/text` 不够，必须是：

`plate/body -> photo clipped by shaped mask -> frame overlay / globe / badge -> runtime text`

压平成品图里，frame overlay 与 photo 的遮挡关系是隐含的；一旦改成分层拼装，这个遮挡关系必须显式建模。否则 photo 窗口扩宽时会压住右框，严格 slot 时又会露出右侧轨道。

更准确地说，B2 只做了矩形 photo_slot，没有做真实窗口 mask：左上地球徽章的圆弧 cutout、底部 lip、右框唇、卡体 silhouette 都没有作为同一个 mask / overlay 系统处理。因此即使 alpha / green / texture gate 全 pass，视觉仍然错。

## 本轮处理

- 否决 x408 变体：照片压到 atlas 右侧，Godot 中显得探出卡体。
- 否决 x400 变体：外探减弱但仍压框。
- 回到合同 `photo_slot`，把 x390..408 定义为右框唇，用 B 壳左侧 bitmap 材料镜像重建完整 18px，避免旧照片残带 / 透明洞 / 程序纯色带。
- manifest 状态原保留为 `pending_user_visual_review`；用户复审后改判为 `visual_fail_shape_mask_and_frame_overlay_missing`，不宣称生产冻结。

## 下一轮防线

1. 分层拼装必须显式声明每个像素层的 z-order：body / photo clipped by shaped mask / frame overlay / icon / runtime text。
2. 任何扩宽 photo 的方案，都必须先有独立 frame overlay mask；没有 overlay 就不得让 photo 超出合同槽。
3. shaped photo mask 是硬前置：必须覆盖地球圆弧 cutout、底边遮挡、右框唇和卡体 silhouette。
4. machine gate 只能证明“没有洞、没有纯色带、没有色键残留”，不能证明形状贴合和遮挡正确。
5. 下一轮直接做 frame overlay + shaped mask 配料，不再尝试坐标级补丁。
