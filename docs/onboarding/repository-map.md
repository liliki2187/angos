# 仓库地图

这份文档用于最快识别哪些内容是规范来源、哪些只是参考、哪些是可重建产物。

## 规范层

- `gd_project/`：Godot 运行时项目根目录
- `gd_project/scenes/`：Godot 运行时场景与场景所属脚本
- `gd_project/Assets/`：属于游戏运行时的资产与导入源文件
- `gd_project/addons/`：运行时所需的项目本地 Godot 插件
- `docs/`：项目文档、技术指导、入门材料与日志
- `design/gdd/`：正式玩法设计
- `docs/architecture/`：架构决策与技术边界
- `production/`：执行状态、冲刺上下文与交接信息
- `scripts/`：自动化、导入、渲染与打包脚本
- `specs/`：未来的功能规格包与验收驱动工作

## 仅参考层

- `design/prototypes/html/`：HTML 原型、实验室和旧网页 Demo
- `design/systems/`：补充系统分析与较旧的设计拆解
- `docs/archive/`：历史设计或延期设计材料

## 默认忽略层

- `_obsolete/`：已失效、被替代或仅供审计的材料，只为历史查询或恢复保留，不能作为真实来源

## 生成或可重建层

- `prototype/fullchain_demo/`：生成的分发包目录
- `prototype/*.zip`：生成的打包导出物
- `scripts/__pycache__/`：Python 字节码缓存

## 关于历史材料的说明

- 原型 HTML 入口现在位于 `design/prototypes/html/`；仓库根目录已移除旧入口。
- 自包含的全链条网页 Demo 源码现在位于 `design/prototypes/html/full-chain-demo/`。
- `design/generated-settlement-reference/` 仍是参考资产区域；其中部分结果仍服务于当前 Godot UI 预览流程。
- `design/original-art-reference/` 仍保留为当前原画参考归档路径，因为项目技能已依赖该位置。
- 头像裁图规则现在位于 `docs/tools/avatar-cropping.md`。
- `_obsolete/` 专门用于保存“需要保留但默认应忽略”的材料。
