# 发刊编辑界面正式黑白结构稿 v3

> 产物类型：`formal_ui_structure_wireframe`
>
> 本稿验证功能结构、交互状态和容量，不代表最终视觉包装或 Godot 生产界面。

## 本版目标

- 保留桌面 `1920×1080`、`320 / 1040 / 360` 三栏、两张 `490×800` 同屏双版和六版位冻结几何。
- 左栏使用 `288×92` 紧凑横卡，8篇完整常显，10/12篇启用真实滚动并保持位置。
- 主图呈现事务提交前的 `targeting / replace_pending`：唯一来源、全部合法目标、当前 hover 目标与唯一 `44×44` 局部“换稿”。
- 第二态呈现事务提交后的 `recalculating`：临时选择、目标边线和换稿按钮全部清除，旧结果失效，送印 CTA 禁用。
- 右栏升级为“上部连续签批证据链 + 下部固定硬阻断 + 唯一 CTA”，确认态只替换右栏并冻结双版。

## 运行方式

直接用桌面浏览器打开 `index.html`，或从仓库根目录启动静态服务器后访问：

```text
http://127.0.0.1:<port>/docs/prototypes/weekly-editorial-formal-black-structure-v3/
```

页面默认展示 targeting 主状态。点击副头版或局部“换稿”后进入 recalculating 第二态。

页面还暴露了结构验收接口：

```js
editorialWireframe.showState("targeting")
editorialWireframe.showState("recalculating")
editorialWireframe.showState("ready")
editorialWireframe.showState("confirmation")
editorialWireframe.setCandidateCount(12)
editorialWireframe.getAuditState()
```

## 合同边界

- `candidate_card v1.2.0 → v1.3.0`：卡片尺寸和命中区不变，新增第7/8张位置、8px间距和10/12篇滚动合同。
- `signoff_panel v1.1.0 → v1.2.0`：由固定卡堆改成连续证据链滚动区、固定阻断区和固定 CTA。
- 三栏、双页、六版位、同纸双版、唯一 CTA 及 `44×44` 局部换稿命中区保持不变。
