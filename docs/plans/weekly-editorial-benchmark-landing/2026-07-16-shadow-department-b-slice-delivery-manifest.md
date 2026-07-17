# 市政厅影子部门 1005 B 级报道图纵向切片交付清单

## 决策条

- **结论**：1005 单图、manifest 映射和默认双版运行预览已经通过增量工程检查，当前等待用户视觉确认。
- **影响**：右页左下普通版位不再显示橄榄占位块；1003 / 1004 / 1005 都能在普通版位间跟稿显示，1006 继续保持 fallback。
- **下一步**：用户先看默认双版截图中的影子侧翼语义、亮度和同刊一致性；通过后再单独推进 1006。

## 详情

- **一句话结论**：`article_id=1005` 已成为第三张可动态映射的 B 级普通报道图，但不据此声称整套普通报道资产完成。
- **实际完成**：内置真实生图、确定性中心裁切到 `756×696 RGB`、manifest v6、21 项定向测试、Godot 导入与一张真实窗口截图；既有通用运行时映射无需再改代码。
- **当前没有工程阻断**：资源能加载，默认 inner-1 显示 1005；compact / tall 切换、未映射 fallback 和旧纹理清理均通过。
- **仍需用户裁决**：1005 与 1003 / 1004 并排时是否足够像同一期刊，实体楼与额外影子侧翼在小图中是否一眼成立，亮度是否仍低于主 / 副头版。
- **本轮不做**：不跑完整 UI / weekly smoke，不触发换稿、拖拽或确认全链，不生成 1006，不升格整屏生产真源。

## 交付清单

- **交付对象**：`editorial_story_city_hall_shadow_department`，`article_id=1005`。
- **产物类型**：`runtime_state_preview`。
- **它能证明**：1005 在默认 `189×174` 普通版位中可显示；1003 / 1004 / 1005 可按 `article_id + role` 解析并移动到 compact / tall；1006 无映射时继续 fallback；纹理切换无旧图残留；图片层不消费鼠标输入。
- **它不能证明**：用户已采纳 1005；1006 的风格方向；完整交互链、weekly smoke 或整套生产真源已经通过。
- **原始生图**：`image_gen/2026-07-16/20260716-weekly-editorial-city-hall-shadow-department-coarse-editorial-v1-original.png`，`1313×1198 RGB`。
- **运行资产**：`gd_project/Assets/ui/angus_packaging/weekly_editorial/assetized/editorial-story-city-hall-shadow-department-v1.png`，`756×696 RGB`。
- **运行截图**：`docs/screenshots/2026-07-16-weekly-editorial-shadow-department-b-slice/01-godot-three-standard-story-images-default.png`，`1920×1080 RGBA`。
- **定向审计**：`docs/screenshots/2026-07-16-weekly-editorial-shadow-department-b-slice/standard-story-asset-audit.json`，`21/21` 通过。
- **已过 gate**：Godot 新 PNG 导入成功；三张普通报道图的 compact / tall 跟稿、1006 fallback、旧纹理清理、冻结 rect 与鼠标穿透均通过；真实窗口截图已肉眼复核。
- **未过 / 待确认 gate**：用户视觉确认；完整 UI / smoke / 42 项交互回归；1006 扩产。
- **反向读法检查**：重点排除了写实市政厅、古典柱廊、阴谋办公室、黑色电影、3D 低多边形与复古政府海报；运行小图先读实体楼和多出的深蓝影子侧翼，第二道门与影子内小文件柜未被裁掉。
- **agent 例外**：本轮不是新 UI / 新布局，不重复 UI / UX 双 agent 链；按 clean-lowpoly-weekly 临时例外不自动调用旧像素坐标系美术守门。
- **文档 / 实现 drift**：STATUS 与 manifest v6 已同步；A222 已记录 1004 的明确采纳；本轮未改玩法规则或常量，因此不修改 GDD。
- **允许下一步**：用户确认后只做 1006，或只返修 1005。
- **禁止跳到**：自动批量扩产、整套生产标杆 / 真源升格。

## 后续状态

- 2026-07-16 用户在审阅 1005 单图和默认双版截图后回复“继续”，已按 A224 记录为 1005 获确认并授权只进入 1006；本清单中“等待用户确认”的描述保留为交付当时状态。
