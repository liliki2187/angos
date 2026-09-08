# 世界地图深色地图＋分散亮岛校色交付清单

## 结论

当前用户判断候选为 v4：`CONDITIONAL PASS / P0=0`。

它已关闭“白地图”与“全屏关灯”两个相反误判：中央保持深石板地图，钴蓝、冷青、橄榄与芥末在中暗区共享灰桥；刊头、三卡、selected evidence、Dossier、Schedule 和 CTA 文字重新形成亮岛。当前纸件高亮仍比 benchmark 多约一档，因此只供母关系裁决，不是最终校色稿。

## 版本轨迹

| 版本 | 主要结果 | 裁决 |
| --- | --- | --- |
| v1 功能转译 | 地图改成大面积浅纸 | 功能映射保留，色彩拒绝 |
| v2 深色地图 | 地图身份正确，但高亮为 0% | 像关灯，诊断样本 |
| v3 分区恢复 | 高亮仍 0.1%，更暗 | 拒绝 |
| v4 分散亮岛 | 地图 `dark 57.7% / light 2.7%`；全屏 `dark 45.8% / light 21.4%` | 当前 `CONDITIONAL PASS` 候选 |
| v5 纸面收束 | 高亮重新降至 2.0% | 过度压暗，拒绝 |

## 当前候选

- 图片：`image_gen/2026-08-19/world-map-functional-style-translation-v4-lit-islands/02-functional-style-translation-lit-islands-imagegen-native.png`
- 提示词：`image_gen/2026-08-19/world-map-functional-style-translation-v4-lit-islands/01-local-highlight-recovery-prompt.md`
- 原生规格：`1672×941 / RGB / 16:9`
- SHA-256：`CC253CE54ED714F0DC9A0E6EBFAAB00DDDFCB7FC19EF4133413072B67AB207FD`
- 生成方式：Codex 内置 ImageGen 精确编辑；程序只做色彩量化、哈希与文件复制，没有重绘图像。

## 与 benchmark 的关系

| 图 | V_mean | L_mean | 暗部 | 高亮 |
| --- | ---: | ---: | ---: | ---: |
| benchmark 01 | 0.290 | 0.098 | 49.7% | 12.9% |
| benchmark 02 | 0.276 | 0.087 | 54.6% | 13.0% |
| v4 全屏 | 0.310 | 0.123 | 45.8% | 21.4% |
| v4 地图裁切 | 0.215 | 0.044 | 57.7% | 2.7% |

v4 地图层级已经命中；偏差集中在左卡、Dossier 与 Schedule 的大纸面过亮。综合色与纸张色温本身未滑向棕褐旧档案。

## 双审

- UX 老哥：地图深色身份与关灯问题均通过；纸面亮岛连片为 P1，建议后续只压大纸面基础值，不动地图与局部高光。
- UI Designer：地图、综合色、功能不变量通过；左卡 / Dossier / Schedule 形成两片亮纸墙，v4 只能 `CONDITIONAL PASS`。
- v5 已证明继续用整屏 ImageGen追半档纸值会过度压暗，因此本轮止损，以 v4 交用户判断母关系。

## 已知 P1

1. 纸面高亮 `21.4%` 高于 benchmark 约 `13%`；后续需 role-based paper token / 分区遮罩校准，而不是整屏重生。
2. `DISCLOSURE ＋` 与已显示四行内容仍有状态矛盾。
3. 右侧四行日期 / Desk / FIELD 记录仍偏机构业务表格。

## 阶段边界

- 本稿不证明 canonical `1104×704 / 69:44` 图片逐像素同源。
- 不证明 exact rect、动态文字容量、状态矩阵、hit rect 或 NO-HIT 资产分层。
- 不进入组件拆分、atlas、manifest、Godot 或 `WeeklyRunGame`。
