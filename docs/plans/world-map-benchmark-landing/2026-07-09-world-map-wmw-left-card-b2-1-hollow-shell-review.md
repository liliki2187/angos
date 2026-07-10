# WMW left_region_card B2.1 镂空框体分层评审

> 资产线：world-map-benchmark-landing / WMW `left_region_card`  
> 版本：B2.1（v0.9.7）  
> 状态：纵向切片通过，等待用户观感裁决；不是冻结生产资源。

## 1. 本轮结构裁决

用户已裁决并采纳含图片槽资产的三层结构：

1. 底层：地区照片，普通矩形内容层，cover 铺满窗口外接矩形，不做形状、圆弧或窗口 mask 裁切。
2. 上层：镂空框体，包含框、地球徽章、纸签底板、action badge 和状态皮肤；照片窗口区域为透明，所有右缘、下缘、地球圆弧边界由框体 alpha 定义。
3. 运行时：中文 title / meta Label，不烘进素材。

本轮先烘焙合成 atlas 验证视觉与 gate；未来 Godot 正式结构也应按同一模型拆节点：照片为地区内容节点，框体为状态皮肤节点，文字为运行时 Label 节点。

设计采纳已登记为 A168：`docs/设计采纳记录.md` 与 `docs/design-decisions/ui-ux-decisions.md`。

## 2. 与 B2 失败的区别

B2（v0.9.6）把照片按合同矩形槽放入卡内，再尝试重建右侧框唇。用户复审 445 后确认失败根因不是单一右缘坐标，而是照片窗口本身不规则：左上被地球徽章啃出圆弧，右 / 下缘都需要由上层框体遮挡。

B2.1 不再让照片负责边界，不再裁照片成窗口形状。程序只从 B 壳中挖掉旧夜空照片，生成永久复用的镂空框体配料，然后把 B1 地区照片作为矩形下层铺入。

## 3. 输出证据

| 编号 | 文件 | 说明 |
| --- | --- | --- |
| 447 | `docs/screenshots/2026-06-24-world-map-benchmark-landing/447-world-map-wmw-v0-9-7-left-card-b2-1-hollow-shell-ingredients.png` | 四状态镂空框体配料板 |
| 448 | `docs/screenshots/2026-06-24-world-map-benchmark-landing/448-world-map-wmw-v0-9-7-left-card-b2-1-window-cutout-qa.png` | 窗口挖空与旧图签名 QA |
| 451 | `docs/screenshots/2026-06-24-world-map-benchmark-landing/451-world-map-wmw-v0-9-7-left-card-b2-1-atlas-2x.png` | 2x atlas，408x320 x4 |
| 452 | `docs/screenshots/2026-06-24-world-map-benchmark-landing/452-world-map-wmw-v0-9-7-left-card-b2-1-runtime-fill.png` | Python 回填预览 |
| 454 | `docs/screenshots/2026-06-24-world-map-benchmark-landing/454-world-map-wmw-v0-9-7-left-card-b2-1-arc-edge-fit-qa.png` | 200% 地球圆弧 / 下缘 / 右缘目检板 |
| 455 | `docs/screenshots/2026-06-24-world-map-benchmark-landing/455-world-map-wmw-v0-9-7-left-card-b2-1-manifest.json` | B2.1 manifest |
| 456 | `docs/screenshots/2026-06-24-world-map-benchmark-landing/456-world-map-wmw-v0-9-7-left-card-b2-1-godot-single-component.png` | Godot windowed 单组件截图 |
| 457 | `docs/screenshots/2026-06-24-world-map-benchmark-landing/457-world-map-wmw-v0-9-7-left-card-b2-1-godot-single-component-qa.png` | Godot windowed QA 叠线截图 |

Godot 资产副本：

- `gd_project/Assets/ui/angus_packaging/world_map/wmw_v09_left_card_slice/left_region_card_b21_hollow_shell_atlas_2x.png`
- `gd_project/Assets/ui/angus_packaging/world_map/wmw_v09_left_card_slice/left_region_card_b21_hollow_shell_manifest.json`
- `gd_project/Assets/ui/angus_packaging/world_map/wmw_v09_left_card_slice/ingredients/left_region_card_b21_hollow_shell_*.png`

## 4. Gate 结果

| Gate | 结果 | 证据 |
| --- | --- | --- |
| 镂空框旧图签名扫描 | PASS | selected / available / warning / locked 均为 0 |
| 卡体轮廓内 alpha 100% | PASS | 四状态 `transparent_pixels_inside_card_body = 0` |
| 几何比例 1.275 | PASS | 四状态 ratio 均为 1.275，delta 0 |
| 禁止照片形状裁切 | PASS | manifest 记录 photo underlay 为矩形 cover，`photo_shape_clipping = forbidden_not_used` |
| 200% 圆弧 / 右缘 / 下缘目检 | PASS | 454 + 456/457：无旧图带、无色带、无缝隙、无重影 |
| Godot windowed 截图 | PASS | 456 / 457 由 windowed opengl3 生成，未使用 headless |

Godot 内容校验：

- 456：1920x1080，`nonblack_pixels = 2072049`，`unique_colors = 68479`。
- 457：1920x1080，`nonblack_pixels = 2073600`，`unique_colors = 65946`。

## 5. 注意事项

- 本轮没有调用 imagegen，地区照片复用 B1 素材。
- 未修改 `design/ui-contracts/world-map/` frozen 字段。
- 未批量生产其它 class。
- 源 B 壳中存在压缩后的绿色色键背景细线，本轮在挖壳与卡体 alpha 探针中将其作为背景残留排除和清理；探针口径写入 455 manifest。
- B2.1 是结构切片通过，是否作为视觉方向继续推进仍需用户裁决。
