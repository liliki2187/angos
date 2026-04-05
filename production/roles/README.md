# 目录归属

这是日常工作使用的实际归属地图。

- 设计：`design/gdd/`、`design/systems/`、`specs/`
- 运行时开发：`gd_project/scenes/`、`gd_project/Assets/`、`docs/architecture/`、`docs/`
- 引擎工具链：`scripts/`、`.github/workflows/`
- UI 与导入管线：`design/ui/`（如存在）、`gd_project/Assets/ui/`、`gd_project/scenes/ui/`、`docs/tools/psd-ui-import.md`
- 生产协同：`production/`
- 仅参考原型：`design/prototypes/html/`、`prototype/`

## 规则

- 不要把参考原型视为运行时权威来源。
- 不要在仓库根目录增加新的长期源码文件，除非它们确实是根层项目文件。
- 新的实现工作应回链到相应 GDD、spec 或 ADR。
