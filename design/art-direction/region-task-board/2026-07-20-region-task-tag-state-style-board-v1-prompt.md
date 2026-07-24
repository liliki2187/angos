# 区域任务短签全类型 / 全状态美术母板 v1 生成提示

## 产物定位

`visual_style_reference / component correction sheet`。只用于确认短签 / 图钉的类型与状态美术语言，不是 atlas，不直接进入 Godot。

## 正向提示

生成一张严格 4×4 的 16:9 大比例组件美术母板。深海军蓝工作台背景，十六个无字的“短签 + 图钉”组合，全部采用同一个 clean low-poly weekly 纸件家族、相同主轮廓、相同尺寸关系和相同空白文字安全区；元素约为最终运行尺寸的 2.5 倍，方便审阅。

第一排只定义四类任务：permanent 使用文件 / 记录符号，temp 使用沙漏 / 截止符号，chain 使用相扣链环，hidden 使用遮蔽眼 / 隐匿符号。四枚符号均位于图钉中心固定槽。

第二排只定义交互态：available 为中性基线；hover 使用贴体、克制的局部印刷弧；selected 使用图钉后方的橄榄灰纸背板，不能扩大短签文字面；focus 使用深墨错位短线 / 局部弧，与 hover 和 selected 明显不同。

第三排只定义流程态：assigned 在右上固定槽使用安静的灰蓝人员 / 头像托架；urgent 使用锈红截止票角；locked 使用深墨锁扣；disabled 为整件低饱和、低对比的不可用处理。

第四排是四个组合压力样例：temp+urgent、chain+assigned、hidden+selected、左右镜像 / 贴近屏幕边缘的翻签样例。组合时类型图标、流程签和交互外缘必须各守固定位置，不堆叠成徽章墙。

纸张为灰米暖纸、象牙亮边、很浅的低多边形分面与受控印刷错位；轮廓清楚、平面、现代编辑拼贴，保留大块面与轻微手工偏心。短签内部必须完全无文字、无数字、无乱码。状态信息只进入固定 overlay 槽，不改变 200×72 文字安全区。

## 负向提示

不要旧报纸、泛黄档案、棕色怀旧、污渍、折痕、写实纸纹、金属浮雕、厚阴影、玻璃发光、按钮高光、同心圆、多层厚框、软件 dashboard、手机 UI、文字、数字、字母、乱码、每格不同纸壳、32 格全排列墙、巨大红色多边形、程序感实心几何补丁。

## 参考图

- `design/art-direction/benchmarks/clean-lowpoly-weekly/benchmark-board-01.png`
- `design/art-direction/benchmarks/clean-lowpoly-weekly/benchmark-board-02.png`
- 区域任务台 E2 效果稿
- `pin_slice_c_hybrid_v3` 当前 C 混合母版
- clean-lowpoly weekly 纸张材质真值板
