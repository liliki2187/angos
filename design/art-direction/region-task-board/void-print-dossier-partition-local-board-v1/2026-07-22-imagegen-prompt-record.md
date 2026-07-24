# 区域任务台底板显隐与 dossier 分区局部板 v1｜生图记录

> 日期：2026-07-22  
> 产物类型：`filled_state_text_mock / local_dual_state_board`  
> 用途：同时验证左栏底板印刷的遮盖逻辑，以及右 dossier 在不重新套卡的前提下建立语义分区。

## 参考图角色

- 用户截图 `codex-clipboard-9d7de178-9936-42a6-9132-c942506d3d90.png`：左栏深青底板与条目遮盖关系参考。
- `text-integrated-fullscreen-style-draft-v1/review/03-right-text-art-integration-v1.png`：真实中文容量与字阶参考；其平整、弱分区问题不得继承。
- `benchmark-board-01.jpg`、`benchmark-board-02.jpg`：clean-lowpoly weekly 的纸色、低多边形折面、深海军蓝、橄榄、青绿、锈红与成年怪新闻周刊气质真值。

## 生成要求摘要

- 单张 1920×1080 深海军蓝审阅板，只包含三个样本：`左栏 · 条目不足`、`左栏 · 条目充足`、`右侧档案 · 已选任务`。
- 左 A 显示两张任务纸条，下面露出深青底板低对比 `ISSUE INDEX / 02 / NORTH SHORE DESK` 印刷；该印刷没有白底、边框、图标或独立热区语法。
- 左 B 使用同一底板与 header / footer，四张任务纸条自然覆盖印刷；页眉和回条计数与四张条目一致。
- 右侧保持一张连续暖白主纸，使用页眉 / 摘要、青色 metadata 全宽带、锈红风险决策区和独立橄榄 CTA 四段结构；风险内部按等级、依据、建议分组。
- 所有核心中文直接由生图模型生成，不使用程序覆字；程序不重绘纸件、色带、折线或按钮。

## 生成轮次

1. `source/01-imagegen-local-board-v1.png`：首轮完整局部板。
2. 首轮发现 B 态有四张任务但页眉 / 回条仍写 `2`，属于提示内容错误。
3. `source/02-imagegen-count-correction-source-v1-1.png`：只用生图模型把 B 页眉改为 `4 条可选 · 已选 1`、回条改为 `已选 1 · 可处理 4 · 执行中 0`；未修改其他结构。

## 最终审核图

- `review/02-left-dual-state-right-dossier-partition-v1-1.png`：模型原生 `1672×941` 输出。
- `review/03-left-dual-state-right-dossier-partition-v1-1-1920x1080.png`：仅使用高质量双三次插值归一为 `1920×1080` 的审核拷贝；没有重绘、修字、裁切或改变内容。

原始 v1 保留为计数错误证据，不覆盖或删除。
