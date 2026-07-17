# WMW 左卡 B2.10 对称内芯复审材料

> 版本：B2.10 / v0.9.16
> 日期：2026-07-13
> 当前状态：`evidence_ready_pending_user_visual_review`，不是冻结生产资源。
> 本轮范围：只修 B2.9 状态徽章中性内芯的低多边形 X 分面对称性；候选 B approved 外环、右框、照片、地球、运行时状态图标、文字 token、卡体尺寸和合同 frozen 字段均未改。

## 一、B2.9 为什么会歪

B2.9 已经结构性移除了 B2.8 的 harmonic inpaint 涂抹，但 `neutral_core_texture()` 又手写了四组互不关联的外围锚点。top / right / bottom / left 没有共享同一矩形四边，导致四块色面虽然都汇聚到 `(332,246)`，外围端点却不成镜像，最终形成肉眼可见的歪 X。

此前 gate 只证明 approved 外环和右框未被修改，没有检查本轮新生成内芯的分面关系。执行方又把目检注意力锁在“右侧涂抹是否消失”，因此对新可见区域产生了人工假阴性。

## 二、B2.10 结构修复

1. 保留 B2.9 已验证层：approved 外环、右框、照片、地球、运行时图标和文字层全部复用。
2. 从 `CORE_MASK=[302,216,362,277]` 与共享中心 `(332,246)` 参数化生成上 / 右 / 下 / 左四个三角分面，禁止独立手写端点。
3. 首次直接以原 `CORE_MASK` 裁分面时，程序 gate 主动报出左右面积 `921/876px`、面积差 `4.886%`、镜像 IoU `0.95114`。根因是历史 `CORE_MASK` 自身含单像素不对称边缘，不是分面端点再次歪斜。
4. 最终以 `CORE_MASK ∩ horizontal_mirror(CORE_MASK)` 承载结构分面；完整 `CORE_MASK` 仍负责清除旧语义，交集外的单像素边缘只铺状态基色，不生成额外分界线。
5. 分面明度固定为上 `+3 RGB`、左 / 右 `0`、下 `-3 RGB`；四面共用同一稀疏颗粒场，禁止逐像素周期噪点、渐变、模糊和 inpaint。

## 三、关键 Gate

| Gate | 结果 | 可核验依据 |
| --- | --- | --- |
| `badge_core_facet_symmetry` | PASS | 端点镜像误差 `0px`；中心误差 `0px`；左右面积 `876/876px`；面积差 `0`；结构镜像 IoU `1.0` |
| 分面明度 / 颗粒 | PASS | top `+3`、left/right `0`、bottom `-3`；共享颗粒覆盖率 `0.082106`，振幅 `±1 RGB`，未使用周期逐像素噪点 |
| `retired_footprint_texture_continuity` | PASS | approved 外环 `1983/1983px` 保留；内芯外变化 `0px`；右侧走廊变化 `0px`；外露修补像素 `0px` |
| `runtime_icon_shape_completeness` | PASS | 四状态图标透明配料保持完整，padding `>=4px`，border touch `0`；atlas 不烘焙状态字形 |
| Gate A-F / edge residue / alpha / green residue | PASS | 窗口旧图签名与边缘残留为 `0`、窗口 alpha 无洞、非 selected 绿残留 `0`、四状态窗口 diff `0`、比例 `1.275` |
| Godot windowed capture | PASS | Godot `4.6.2-stable` + windowed OpenGL3；537/538 非黑；QA 相对 normal 丢失采样 `0` |
| 16 点视觉复核 | `evidence_ready` | 535 展示四状态 × 地球弧下 / 窗口右缘 / 窗口下缘 / badge；最终视觉裁决归用户 |

## 四、只读复核结论

- UX 老哥：537 终审 P0 / P1 / P2 均为 0；四状态 X 视觉居中，勾 / 靶心 / 警示 / 锁无双描边、底图泄漏或重影，外环 / 右框无可见回退，结论为内部 `evidence_ready` PASS。
- UI 设计师：529 / 530 复核 PASS；四状态交点落在同一 guide 中心，中心到四向边界笔直，无单侧塌陷。
- 美术指导：529 / 530 复核 PASS；X 分面镜像居中，`±3` 明度可辨但不抢成独立符号，共享颗粒没有形成棋盘纹或四块程序色带，approved 外环与右框无视觉回退。

上述结论构成内部证据就绪，不替代用户最终视觉裁决。

## 五、证据索引

- 529：候选 B / 失败 B2.9 / B2.10 四状态对照。
- 530：400% 空底盘、中心 guide、分面与配料证据。
- 531：B2.10 2x atlas。
- 532：几何 QA。
- 533/534：Python 运行时回填 / QA。
- 535：四状态 × 四检查点 16 点证据板。
- 536：B2.10 manifest。
- 537/538：Godot 4.6.2 windowed 单组件截图 / QA。

## 六、边界与宣称

- 本轮未调用 imagegen，未修改 `design/ui-contracts/world-map/` 任何 frozen 字段，未生产其它 class。
- B2.10 已完成程序 gate、Python 回填、Godot 真实运行截图与内部只读复核；当前只可写 `evidence_ready_pending_user_visual_review`。
- 用户确认 B2.10 观感前，不得冻结 `left_region_card`，不得批量生产 `right_dossier_page` 等其它 class。
