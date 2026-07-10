# WMW left_region_card B1.2 右边框断裂 Loop Log

日期：2026-07-08  
对象：`left_region_card` 候选 B1.2（v0.9.4）  
相关产物：419 Python runtime fill、421 manifest、422 right-edge close-up、425 对比板

## 三行结论

结论：B1.2 失败，不是可放行修复；右侧边框被修边逻辑擦成透明洞，深色背景把洞渲染成暗缝。  
影响：B1.1 / B1.2 都只能作为失败证据归档，不能进入 Godot 放行或批量生产其它 class。  
下一步：继续修之前必须先重建分层合成口径：照片只在 `photo_slot` 内，卡壳 / 边框作为独立 top mask 覆盖在照片之上，再做四状态边缘 close-up 与 `card_body_opacity_probe`。

## 用户指出的问题

用户在 419 Python runtime fill 截图中指出：

- warning 卡右侧边框被图片或透明带隔断，原本连续的卡壳竖边不再成立；
- 照片下方还能看到另一段被遮盖的图片，说明洞后方的深色背景 / 底层图像参与了最终读图；
- 这不是“右缘残留少量像素”的问题，而是卡体轮廓内出现透明孔洞。

像素探针复现：`x390..408, y40..300, alpha < 250`。四状态右侧壳带透明像素分别为 selected 3820、available 3859、warning 3802、locked 3835；卡体控制区域 `x42..390, y40..300` 均为 0。

## 直接原因

B1.2 的 `scrub_right_outer_bleed()` 把 `x=393..408, y=24..288` 的右侧带状区域直接置透明。这个区域被误判为“残边 / bleed”，但它实际包含合法的右侧卡壳、边框和斜切结构。

因此 B1.2 做到了“看起来没有竖向源图残带”，但代价是在卡体轮廓内打出透明洞。透明洞铺到深色背景上会读成暗缝，视觉上就是边框被切断、照片下方露出另一层。

源头错位是 B 壳烘焙照片窗口和合同 `photo_slot` 不一致：B 壳可见照片窗口向右延伸到 x≈408，而合同槽右边界是 x390。B1.1 只按合同贴新照片，所以 x390..408 露出旧照片残带；B1.2 没有重建这段壳体底板，而是把它擦成透明。

正确层级应该是：

1. 地区照片：严格裁在 `photo_slot [21,24,174,64]` 内；
2. 卡壳 / 边框 / bevel：独立 top mask 覆盖照片边缘；
3. badge / globe：同一语义只保留素材层单轨；
4. label / meta：运行时文字 token。

B1.2 实际是在 383 / 397 这种扁平图上做像素擦除和局部回填，没有可靠的“卡壳在照片上方”的保护层。

## 为什么会犯

- 把“去掉右缘竖带”当成唯一目标，忽略了“右边框必须连续”这个更上层的不变量；
- 把绿像素统计、垂直亮度跳变当成视觉 clean 的替代证据；真正该跑的“卡体轮廓内 alpha 必须不透明”没有进入 gate；
- 422 close-up gate 的框选范围和判据只覆盖了 strip 是否消失，没有强制检查边框连续、卡壳厚度、下方是否露出旧照片；
- 在扁平图像上做修边时，没有先把素材分成照片层、卡壳 top mask、badge 层，因此修一个区域会破坏另一个视觉职责；
- 复审时把“问题像素被消掉”误读成“合成干净”，没有对四状态逐张做内容语义目检；
- QA 口径被问题牵着走：从“不能有残带”滑向“深色背景看起来干净”，等于让透明洞恰好通过了错误口径。

## 已执行纠偏

- 421 manifest 已降级为 `candidate_b1_2_failed_user_review_right_frame_interrupted_and_layer_leakage`；
- `composite_cleanliness` 改为 fail；
- 新增并标记失败 gate：`right_frame_continuity`、`layer_order_integrity`；
- 新增并标记失败 gate：`card_body_opacity_probe`，探针范围 `x390..408, y40..300`；
- `right_edge_closeup` 虽然保留机器统计，但整体改为 fail，原因是 gate 目标不完整；
- `scripts/ui-contracts/wmw/wmw_v094_left_card_b12_right_edge_fix.py` 标注该修法只用于再生失败证据，不是生产修复路径。

## 下一次修复前置条件

- 不再擦除整条右侧带状区域；先明确哪些像素属于合法卡壳，哪些属于照片槽或源图残留；
- 必须先重建 B 壳照片窗口：清空旧照片窗口，用周围底板纹理补回 x390..408，让可见窗口等于合同 `photo_slot`；
- 必须建立或提取 shell / frame top mask，让卡壳边框始终压在照片层上；
- 每状态都要输出右侧边缘 100% / 200% close-up，检查 `right_frame_continuity`；
- 每状态都要检查照片槽下沿和右沿是否有隐藏 underlay / 旧照片泄漏；
- 每状态都要跑 `card_body_opacity_probe`：卡体可见轮廓内 alpha 必须为不透明，任何透明洞直接 fail；
- QA 判据如需修改，必须先在 manifest 写明原因和新旧口径差异，禁止改到能过为止。
