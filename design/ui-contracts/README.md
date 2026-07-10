# UI 组件类合同真源

> **用途**：存放资产化 UI 的组件类（component class）几何合同 JSON。这是合同的唯一真源；评审文档、clean-sprite brief、manifest 和 Godot loader 只引用本目录，不得另行复制几何数值。
> **上游流程**：`docs/onboarding/assetized-ui-production-chain.md` 阶段 4（整页合同板）。
> **校验器**：`scripts/ui-contracts/validate_class_contract.py`，进 manifest 前必须通过。

## 目录结构

```text
design/ui-contracts/
  README.md
  <页面>/                  例如 world-map/
    <class_id>.json        每个组件类一个合同文件
```

## 合同 JSON 约定

| 字段 | 说明 |
| --- | --- |
| `schema_version` | 合同结构版本，当前为 1 |
| `contract_version` | 合同内容版本；修改 `frozen` 字段必须升版本并重跑整屏回填 |
| `status` | `candidate`（候选）/ `locked_candidate`（已锁候选，等美术轮验证）/ `production`（生产合同） |
| `reference_resolution` | 合同坐标所在参考分辨率，缺失不得进 clean-sprite brief |
| `runtime_resolution` | 运行与截图验收目标分辨率（项目默认 1920x1080） |
| `export_scale` | 素材制作倍率；参考与运行分辨率非整数倍时必须 ≥2，禁止位图放大上屏 |
| `frozen` | 几何骨架：`export_size`、`positions`、槽位矩形、`hit_rect`、间距。静默改动即违规 |
| `provisional` | 弹性位：贴容量上限的槽、依赖最终字体的假设；排版 / 美术复审可回改，不算打破合同 |
| `states` | 状态皮肤清单；全部状态共享 `frozen` 几何（component_class_uniformity_gate） |
| `parent_class` | 若组件实例位于另一组件内部（如 CTA 条在 dossier 内），声明父 class，校验器跳过父子重叠检查 |
| `evidence` | 评审文档、量测 manifest、生成脚本路径；脚本必须位于 `scripts/`，不得引用 `tmp/` |

矩形一律 `[x, y, w, h]`；槽位坐标相对组件左上角；`positions` 为组件在参考分辨率页面上的实例位置。

## 修改规则

- 改 `frozen` 字段：升 `contract_version`，重跑 `validate_class_contract.py` 与整屏回填，更新对应页面 STATUS.md。
- 改 `provisional` 字段：在字段内注明修订原因与日期即可。
- 素材不服从合同时判素材失败，回 brief 重生成；不得反向静默迁就素材。
