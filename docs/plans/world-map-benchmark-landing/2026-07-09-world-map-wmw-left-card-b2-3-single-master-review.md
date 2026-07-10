# WMW 左侧地区卡 B2.3 单母版派生评审记录

> 版本：v0.9.9 / B2.3  
> 日期：2026-07-09  
> 结论：完整纵向切片已重跑通过，当前为“待用户观感裁决”的候选切片，不是冻结生产资源。

## 一、本轮裁决

用户撤销 B2.2 的“逐帧窗口真源”，改为“一类一母版”：

- 以候选 B 原始 atlas 的 `available` 帧作为唯一母版。
- 只对母版实测照片窗口与地球圆盘，纯几何挖窗一次。
- 其它状态从母版派生：框色家族换色、badge 槽位小图贴换、selected 绿光晕叠加。
- 四状态照片均使用同一个母版窗口矩形，GateE 改为 diff = 0 断言。

设计采纳已登记：

- `docs/设计采纳记录.md`：A169
- `docs/design-decisions/process-and-research-decisions.md`：A169
- 专用规程：`docs/workflows/wmw-hollow-shell-photo-pipeline.md`

## 二、输入与脚本

输入：

- 候选 B 原始 atlas：`gd_project/Assets/ui/angus_packaging/world_map/wmw_v09_left_card_slice/left_region_card_candidate_b_atlas_2x.png`
- B1.3 地区照片 atlas：`docs/screenshots/2026-06-24-world-map-benchmark-landing/428-world-map-wmw-v0-9-5-left-card-candidate-b1-3-atlas-2x.png`

脚本：

- `scripts/ui-contracts/wmw/wmw_v099_left_card_b23_single_master_pipeline.py`
- `gd_project/tests/capture_world_map_wmw_left_card_runtime_v09.gd`
- `scripts/run_wmw_godot_capture_v09.ps1`

Godot 截图跑法：

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run_wmw_godot_capture_v09.ps1 -SkipRepro
```

## 三、母版量测

母版状态：`available`

实测窗口矩形（2x 帧内坐标）：

```json
[38, 56, 366, 184]
```

实测地球圆盘：

```json
{
  "center": [57.0, 45.0],
  "radius": 26.0,
  "cream_bbox": [34, 21, 81, 70],
  "cream_pixels": 910
}
```

GateE：

```text
pass，四状态均由母版派生，窗口几何 diff = 0
```

## 四、过程修正

首版脚本只把各状态 badge 的奶油色线条贴回母版，导致 warning / locked 的 action badge 内部残留 available 靶心底色，视觉明显劣于原帧。该问题属于“badge 小图贴换范围过窄”的实现错误，不涉及照片几何或 gate 放宽。

修正后改为从原 B 帧贴换完整 `action_badge` 槽位小图，重新生成 459 / 465 / 463 / 467 / 468。修正后 badge 质感回到各状态原图标表现，未改变母版窗口与照片层逻辑。

## 五、产物

| 编号 | 文件 | 说明 |
| --- | --- | --- |
| 459 | `docs/screenshots/2026-06-24-world-map-benchmark-landing/459-world-map-wmw-v0-9-9-left-card-b2-3-single-master-derive-compare.png` | 原 B vs B2.3 派生对比板 |
| 460 | `docs/screenshots/2026-06-24-world-map-benchmark-landing/460-world-map-wmw-v0-9-9-left-card-b2-3-single-master-ingredients.png` | 母版配料板 |
| 461 | `docs/screenshots/2026-06-24-world-map-benchmark-landing/461-world-map-wmw-v0-9-9-left-card-b2-3-atlas-2x.png` | 2x atlas |
| 462 | `docs/screenshots/2026-06-24-world-map-benchmark-landing/462-world-map-wmw-v0-9-9-left-card-b2-3-geometry-qa.png` | 几何 QA |
| 463 | `docs/screenshots/2026-06-24-world-map-benchmark-landing/463-world-map-wmw-v0-9-9-left-card-b2-3-runtime-fill.png` | Python 回填 |
| 464 | `docs/screenshots/2026-06-24-world-map-benchmark-landing/464-world-map-wmw-v0-9-9-left-card-b2-3-runtime-fill-qa.png` | Python 回填 QA |
| 465 | `docs/screenshots/2026-06-24-world-map-benchmark-landing/465-world-map-wmw-v0-9-9-left-card-b2-3-300pct-fit-qa.png` | 地球弧 / 右缘 / 下缘 300% 目检板 |
| 466 | `docs/screenshots/2026-06-24-world-map-benchmark-landing/466-world-map-wmw-v0-9-9-left-card-b2-3-manifest.json` | manifest |
| 467 | `docs/screenshots/2026-06-24-world-map-benchmark-landing/467-world-map-wmw-v0-9-9-left-card-b2-3-godot-single-component.png` | Godot windowed 单组件截图 |
| 468 | `docs/screenshots/2026-06-24-world-map-benchmark-landing/468-world-map-wmw-v0-9-9-left-card-b2-3-godot-single-component-qa.png` | Godot windowed QA 截图 |

Godot 资产副本：

- `gd_project/Assets/ui/angus_packaging/world_map/wmw_v09_left_card_slice/left_region_card_b23_single_master_atlas_2x.png`
- `gd_project/Assets/ui/angus_packaging/world_map/wmw_v09_left_card_slice/left_region_card_b23_single_master_manifest.json`
- `gd_project/Assets/ui/angus_packaging/world_map/wmw_v09_left_card_slice/ingredients/`

## 六、Gate 结果

manifest 状态：

```text
b2_3_single_master_pass_pending_user_review
```

| Gate | 结果 | 证据 |
| --- | --- | --- |
| GateA 旧图残留核心区 | pass | 四状态 `opaque_pixels_in_cutout_core = 0` |
| GateB 边框完整环带 | pass | 四状态 `broken_opaque_pixels = 0` |
| GateC 窗口 alpha | pass | 四状态 `transparent_or_nonopaque_pixels_in_window = 0` |
| GateD 非 selected 绿残留 | pass | available / warning / locked 全帧绿签名 = 0；selected 语义免检 |
| GateE 同状态窗口 | pass | 母版派生 diff = 0 |
| GateF 几何比例 | pass | 四帧 408x320，比例 1.275 |
| 300% 目检 | pass | 465，地球弧 / 右缘 / 下缘未见旧图带、色带、透明洞、底层照片泄漏 |
| 派生美术质量 | pass_pending_user_review | 459，父级目检认为不明显劣于原 B，但最终观感由用户裁决 |
| Godot windowed 截图 | pass | 467/468，非黑、颜色多样性正常 |

JSON 校验：

- `python -m json.tool docs/screenshots/2026-06-24-world-map-benchmark-landing/466-world-map-wmw-v0-9-9-left-card-b2-3-manifest.json` 通过
- `python -m json.tool gd_project/Assets/ui/angus_packaging/world_map/wmw_v09_left_card_slice/left_region_card_b23_single_master_manifest.json` 通过

## 七、目检备注

- 地球圆弧：四状态照片均在地球徽章下方被上层框体遮盖，未再出现“左上弧线不贴合”。
- 右缘：四状态照片不再切断右框，也没有 x390..408 透明洞或程序色带。
- 下缘：照片贴到母版窗口底边，下方由框体遮盖；465 中可见的暗色接触线是窗口内照片与框体阴影交界，不是另一张图泄漏。
- 运行时文字：Python 与 Godot 均使用 `label_title / meta_status` token；未烘进素材。

## 八、禁止与状态

已遵守：

- 未调用 imagegen。
- 未改 `design/ui-contracts/world-map/` frozen 字段。
- 未批量生产其它 class。
- 未对照片做形状 / 圆弧 / mask 裁切。
- UI 截图未使用 headless。

当前状态：

```text
B2.3 是完整纵向切片通过的候选，等待用户对观感与单母版派生路线裁决。
```

