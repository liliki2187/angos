# 区域任务右 dossier 资产化 Router Card

## 任务范围

在已冻结短签 v7、event card 继续冻结的前提下，把右侧 `412×960` dossier 从程序矩形面板推进为可信的编辑档案纸件。第一轮只做一个无字单例与真实 Godot 回插，不批量生产全状态。

## 风险级别

`risky`。该组件同时承载长摘要、任务 meta、风险等级、风险依据、建议和唯一主 CTA；美术层一旦侵入文字区或把 CTA 烘焙进 shell，会直接破坏运行信息与交互。

## 冻结输入

- `design/ui-contracts/region-task-board/dossier_contract.json`
- 运行尺寸 `412×960`
- header、summary、metadata、risk、primary CTA 五区
- 标题最多两行；summary 7–8 行、压力态 9 行，不允许内部滚动
- selected 后必须同时显示风险等级与一条可执行建议
- CTA 固定底部；empty / selected / disabled / ready 不允许布局跳动
- 所有文字、风险色、CTA 文案 / icon / 状态归 Godot
- clean-lowpoly benchmark 与 E2 右 dossier 只提供纸件、色彩、材质和层次参考，不是裁图源

## 当前路线

1. UX 先诊断当前程序骨架与交互合同；
2. 父级关闭 `summary_scroll` 合同冲突并运行回归测试；
3. UI Designer 输出 exact 1× 元素 / 所有权表、文字安全区与唯一单例 brief；
4. Angus 美术指导审 prompt 与拆分策略；
5. built-in imagegen 生成大尺寸、无字、可色键分离的单例美术源；
6. 程序仅做色键透明、尺寸归一、切片 / 组合 QA 与动态文字回插；
7. Godot 4.6.3 输出 1920×1080 真实截图，完成 UX / UI / 美术终审。

## 禁止项

- 不直接裁 E2 整屏右栏；
- 不烘焙任务标题、摘要、meta、风险文字、建议、CTA 文案或 icon；
- 不烘焙红色风险框、APPROVED 章、问号或固定任务 ID；
- 不把 shell、section plate、status badge 与 CTA mother 焊成一张最终生产资源；
- 不移动 CTA、不缩小文字安全区、不新增滚动条；
- 不解锁 event card、完整摘要层或移动端。

## 交付 Gate

- 无字时仍可读出一件完整 dossier，而非四个程序矩形；
- 拆分后重新组合仍保持纸层连续、共享边与材质一致；
- 1× 下文字对比、边角、纸层和轻微 low-poly 面差成立；
- 7 / 8 / 9 行摘要、风险等级 + 两条依据 + 建议、CTA disabled / ready 均不遮挡；
- 没有高可见程序临时装饰冒充美术资源。
