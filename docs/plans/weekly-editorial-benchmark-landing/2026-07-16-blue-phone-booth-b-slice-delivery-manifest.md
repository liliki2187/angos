# 蓝色电话亭猫群 1006 B 级报道图纵向切片交付清单

## 后续状态（2026-07-17）

- 用户已明确确认 1006 单图及六版位全填充双版预览，采纳记录为 A225；下文“等待用户视觉确认”保留为 2026-07-16 交付当时的历史状态。
- 后续收口中，普通报道图定向审计 `25/25`、发刊编辑器交互回归 `42/42`、`0/6、3/6、5/6、6/6` 四容量态全部通过。
- 全局周循环并未完整通过：`test_phase_flow.gd` 与 `test_settlement_result.gd` 通过，`test_weekly_run_layout.gd` 仍失败 22 项。因此本清单不能反向解读为“完整 UI / weekly smoke 已通过”。
- 最新收口边界与证据见 `2026-07-17-ordinary-story-closeout-delivery-manifest.md`。

## 决策条

- **结论**：1006 单图、manifest 映射和六版位全填充双版运行预览已经通过增量工程检查，当前等待用户视觉确认。
- **影响**：1003 / 1004 / 1005 / 1006 四张普通报道图都能在四个普通版位间跟稿显示；六个版位已有完整报道图预览。
- **下一步**：用户先看右页右下小图的猫群停步语义、钴蓝强度和同刊一致性；通过后结束普通报道图单图序列。

## 详情

- **一句话结论**：`article_id=1006` 已成为第四张可动态映射的 B 级普通报道图，但不据此声称整屏或后续 B / C 级资产已经完成。
- **实际完成**：内置真实生图、确定性中心裁切到 `756×696 RGB`、manifest v7、25 项定向测试、Godot 导入与一张六版位全填充真实窗口截图；既有通用运行时映射无需再改代码。
- **当前没有工程阻断**：资源能加载，inner-2 可显示 1006；四图 compact / tall 切换、空槽隐藏、未映射 fallback 和旧纹理清理均通过。
- **仍需用户裁决**：1006 与 1003–1005 并排时是否足够像同一期刊；三只猫集体停在电话亭同一侧是否足够表达“拒绝经过”而不只是围观；钴蓝是否仍服从普通版位层级。
- **本轮不做**：不跑完整 UI / weekly smoke，不触发换稿、拖拽或确认全链，不生产其他 B / C 级资产，不升格整屏生产真源。

## 交付清单

- **交付对象**：`editorial_story_cats_refuse_blue_phone_booth`，`article_id=1006`。
- **产物类型**：`runtime_state_preview`。
- **它能证明**：1006 在默认 `189×174` 普通版位中可显示；1003–1006 均可按 `article_id + role` 解析并移动到 compact / tall；空槽保持隐藏，真实存在但未映射的文章继续 fallback；纹理切换无旧图残留；图片层不消费鼠标输入。
- **它不能证明**：用户已采纳 1006；完整交互链、weekly smoke、其他 B / C 级资源或整套生产真源已经通过。
- **原始生图**：`image_gen/2026-07-16/20260716-weekly-editorial-cats-refuse-blue-phone-booth-coarse-editorial-v1-original.png`，`1327×1185 RGB`。
- **运行资产**：`gd_project/Assets/ui/angus_packaging/weekly_editorial/assetized/editorial-story-cats-refuse-blue-phone-booth-v1.png`，`756×696 RGB`。
- **运行截图**：`docs/screenshots/2026-07-16-weekly-editorial-blue-phone-booth-b-slice/01-godot-four-standard-story-images-default.png`，`1920×1080 RGBA`。
- **定向审计**：`docs/screenshots/2026-07-16-weekly-editorial-blue-phone-booth-b-slice/standard-story-asset-audit.json`，`25/25` 通过。
- **已过 gate**：Godot 新 PNG 导入成功；四张普通报道图的 compact / tall 跟稿、空槽、未映射 fallback、旧纹理清理、冻结 rect 与鼠标穿透均通过；真实窗口截图已肉眼复核。
- **未过 / 待确认 gate**：用户视觉确认；完整 UI / smoke / 42 项交互回归；后续资产范围。
- **反向读法检查**：排除了 TARDIS / 英式警亭、写实街景、恐怖传送门、发光眼、萌宠插画与猫贴纸包；运行小图先读钴蓝电话亭和三只成年猫的大剪影，猫群全部停在电话亭同一侧且没有穿过。
- **agent 例外**：本轮不是新 UI / 新布局，不重复 UI / UX 双 agent 链；按 clean-lowpoly-weekly 临时例外不自动调用旧像素坐标系美术守门。
- **文档 / 实现 drift**：STATUS 与 manifest v7 已同步；A224 已记录 1005 的明确采纳；本轮未改玩法规则或常量，因此不修改 GDD。
- **允许下一步**：用户确认后结束普通报道图单图序列，或只返修 1006。
- **禁止跳到**：自动进入其他资产类别、批量扩产、整套生产标杆 / 真源升格。
