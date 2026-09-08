# 世界地图 Dossier 无字母版：透明通道与生成式几何误判 Loop Log

日期：2026-09-01  
关联：A339、世界地图 Dossier 第一条 vertical slice

## 发生了什么

在装配合同通过后，父级尝试让内置生图一次生成完整的 Dossier 无字透明母版，并期望它可以直接进入切件。视觉方向经过多轮定向返修后基本成立，但机器审计发现：

- 文件为 RGB，没有真实 alpha；
- 所谓透明背景只是烘焙棋盘格；
- 再次执行背景提取仍得到 RGB；
- 目标比例和内部槽位只能视觉近似；
- 黑夹尺寸侵入既定 no-text 禁入区。

因此该产物已降级为 `vertical_slice_visual_candidate`，没有升格为生产母版。

## 错在哪里

错误不是生图风格不好，而是把三个不同问题错误地交给同一张完整生图解决：

1. 美术质感与物件关系；
2. 像素级功能槽位；
3. 真实透明切件。

图像生成适合提供第 1 项的材质和形态候选，但不能被默认视为第 2、3 项的确定性证据。提示词中的“透明”和“468×1032 比例”也不能替代文件通道与像素审计。

## 为什么及时阻断

如果直接切件：

- 棋盘格会进入游戏；
- 缩放或裁切会让 photo / Disclosure / expanded / CTA 与冻结 rect 错位；
- 过大的夹子会再次压住动态文字；
- 之后所有 Godot 对齐问题都会被误判为实现问题，而根因其实在资产源。

## 修正后的流程

1. 完整生图只负责视觉候选，不直接成为装配源。
2. FrontCarrier 改为“真实生图矩形材质源＋合同坐标装配”。
3. BackDecor 的夹子、胶带和纸层露边必须来自真正透明来源，并独立审计 alpha bbox。
4. 程序只负责裁切、缩放、排版、文字与 QA，不生成美术质感。
5. 每个 PNG 在登记 manifest 前必须检查：
   - `mode` / alpha 通道；
   - source/runtime ratio；
   - content_rect / no_text_rect；
   - protrusion bbox；
   - 是否含伪文字和烘焙棋盘格。
6. 无真实 alpha 时保持 blocked，不用颜色键或脚本抠图默默绕过。

## 本轮证据

- 视觉候选：`image_gen/2026-09-01/world-map-dossier-vertical-slice-v1/01-dossier-no-text-master-candidate.png`
- 合同叠框：`image_gen/2026-09-01/world-map-dossier-vertical-slice-v1/02-dossier-candidate-contract-overlay.png`
- 审计：`image_gen/2026-09-01/world-map-dossier-vertical-slice-v1/03-dossier-candidate-audit.json`

## Gate

当前：`VISUAL_DIRECTION_PASS / PRODUCTION_CUT_BLOCKED`。

解锁条件：获得真正带 alpha 的独立 BackDecor 来源，并用合同坐标重新装配 FrontCarrier；在此之前不得进入 atlas、最终 manifest、Godot 或 WeeklyRunGame。

