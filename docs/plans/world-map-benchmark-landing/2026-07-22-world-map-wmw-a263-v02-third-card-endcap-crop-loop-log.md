# WMW A263 v0.2 第三卡状态签端帽裁切 Loop Log

## 结论

v0.2 原 `dual_reviewed_pending_user_visual_confirmation` 与 UX/UI PASS 全部撤回，当前降级为 `user_visual_review_failed_third_card_endcap_crop_rework_required`。第三卡整体和日程器均未因空间不足被裁；失败发生在局部 ingredient 到 footer 的 source-to-target 映射阶段。

## 触发来源与原始问题

- **触发来源**：用户最终整屏截图复审。
- **原始问题**：“这个按钮不完整，是否是因为空间问题，第三个地区已经显示不全”。
- **事实结论**：第三卡下沿到日程器仍有约 9px，footer 右边也在卡体内。只有第三卡灰靛“锁定”状态签右端帽、右侧轮廓和纸面余量不完整。

## 根因证据

- source crop：`[100,430,2050,650]`，尺寸 `1950×220`，宽高比 `8.863636`。
- target footer：`[49,744,367,52]`，宽高比 `7.057692`。
- 使用方式：`ImageOps.fit(center, cover)`。
- 实际有效源窗口：`[298.65,430,1851.35,650]`。
- 状态签 protected bbox：`[1576,523,2133,623]`。
- 右侧裁切损失：`281.65px`；像素保留率：`0.4943`。
- 最终可见映射 bbox：`[350.92,765.98,416,789.62]`；右边距 `0px`，右端帽缺失。

完整证据已写入 `wmw-a263-uncoated-fullscreen-v0-2-audit.json -> protected_object_mapping_audit.third_card_state_tag`。

## 为什么原复核没有发现

1. 父级、UX 与 UI Designer 检查了“文字是否位于作者声明的 carrier”“旧接缝是否消失”“footer 是否为单层”，没有检查实际图形对象是否完整。
2. audit 使用名义状态槽 `[314,744,102,52]` 计算文字中心，未检测最终灰靛色域 bbox；文字相对错误矩形居中产生假阳性。
3. QA 只展示最终局部，没有并列展示完整 ingredient、source crop、`fit` 有效窗口和端帽放大图。
4. 视觉复核将贴住 footer 右缘的意外直切边误读为有意的切角收口。

## 失败归因与复发判定

- **失败归因**：证据 / 实现 / 可读性联合失败。实现阶段未声明 protected object；审计阶段只检查名义 bbox；人工阶段未做源图到最终图的对象完整性反查。
- **复发判定**：归入 F1“验证等级冒充”第 26 次以上复发。此次是 `declared carrier + text center PASS` 冒充 `visible protected object 完整`，不是全新错误家族。
- **本轮处理**：降级 + 撤回原双审结论 + 更新现有 `text_carrier_capacity` gate + 在 v0.2 可复现脚本中加入 protected-object mapping audit。由于 F1 已在脚本层仍复发，不能只补文字规则。

## 当前范围裁决

- 日程日期 / 动作 9px 分组：继续有效。
- 右栏正文 / 任务标题 / 首任务 10px / 10px 章节间距：继续有效。
- 第三卡单层 footer 与旧 x=314 接缝消失：只保留为局部事实，不代表状态签完整。
- 下一轮只重开第三卡 footer `[49,744,367,52]`；不改三栏、卡片尺寸、日程尺寸、右栏、图片、地图、配色、Godot、runtime、atlas、正式合同或 frozen compact A5.1。

## 下一版修正门槛

- 重新生成或定向编辑接近 footer `7.058:1` 的局部 ingredient；不得用简单右移旧 crop 勉强救回过宽状态签。
- 任何含 protected object 的 `fit/crop/cover` 必须先输出有效源窗口。
- protected bbox 必须完整落在有效窗口内，四向裁切损失均为 0，像素保留率至少 `0.99`。
- 最终状态签左右端帽完整，右侧距 footer 边缘至少 `8px`，上下至少 `4px`；标题到状态签视觉间距至少 `16px`。
- `锁定`文字按最终实际灰靛色域中心复核，每轴误差建议不超过 `4px`。
- QA 必须并列展示完整 ingredient、source crop、有效窗口 / protected bbox、最终 100% / 200% 第三卡和两个端帽放大图。
- 修复后的用户审阅入口必须包含完整 1920×1080 默认态和默认 / 确认流程对照，并说明每张图的用途与需要判断的内容。

## Agent 复核结论

- UX 老哥：`ITERATE / P0=0 / P1=1 / P2=0`。空间足够；唯一 P1 是第三卡状态签真实可见对象不完整。此前漏检因为只核对文字和名义 carrier，没有核对端帽 / 闭合轮廓 / 源到目标映射。
- UI Designer：`ITERATE / P0=0 / P1=1 / P2=1`。状态签只保留约 49.4%；不建议简单右移旧 crop，应在冻结 footer 几何内重做紧凑闭合签体。P2 仍是右栏 12px 摘要未来 runtime 清晰度验证。

## 沉淀位置

- 决策状态：A263 总索引与 `art-direction-decisions.md`。
- 进度真源：`STATUS.md`。
- 复发防线：`workflow-gates.yml -> text_carrier_capacity`。
- 可执行证据：v0.2 渲染脚本与 audit 的 `protected_object_mapping_audit`。

## 关闭记录（A263 v0.3）

v0.3 已按本日志的结构性替代路线关闭缺陷，而非右移旧 crop：built-in imagegen 定向生成紧凑闭合状态签；source crop 改为 `848×120`，通过 `direct_resize` 映入 `367×52`，不再使用 cover 居中裁切。protected 保留率 `100%`、四向裁切损失均为 `0`，最终右 / 上 / 下边距为 `8.22 / 8.67 / 5.2px`，左右端帽完整，文字相对实际色域中心误差 `(0.49,2.77px)`。v0.3 相对 v0.2 只改变第三卡 footer ROI，UX 与 UI Designer 均终审 `PASS / P0=0 / P1=0 / P2=0`。日志状态由“待返工”改为“已由 v0.3 关闭”；防复发 gate 与 v0.2 失败证据继续保留。
