# 区域任务 dossier 生图几何偏差 Loop Log

## 结论

首轮三件关联生图中，附页错误继承了外壳的橄榄背板；CTA 两次出现明显长宽比漂移。两类输出都在进入 Godot 前被拦截，没有用程序拉伸冒充正确美术。

## 发现的问题

1. 首张 section plate 变成“奶油纸 + 橄榄背板”的小号 dossier，违背中性单层 NinePatch 合同，实装后会形成套娃式层级。
2. 首张 CTA 可见轮廓约为 2.3:1，第二张又漂到约 6:1；目标合同为 `712×224`，即约 3.18:1。

## 修正

- section plate 改用“单层中性纸片、禁止 olive backing”的定向 prompt 重生。
- CTA 不采用程序非等比压缩；用真实图像编辑调用只修正轮廓比例，再进行标准的等比裁切与尺寸归一。
- 被否决源图保留在 `image_gen/2026-07-22/region-task-dossier-assetization-v1/source/`，文件名带 `rejected`，供后续审计。

## 防错 Gate

关联生图不等于允许复制母件的全部层级。每件输出进入去底前必须先核对：单层 / 双层所有权、目标轮廓比例、中心拉伸安全区和禁止颜色。比例不符时优先重生或真实图像编辑，不用程序非等比变形掩盖问题。

## 运行完整性追加

首轮真实截图中，CTA 资源虽然已加载，但 `_render_dossier()` 末尾再次调用 `_style_button()`，把 `_style_dossier_asset_button()` 安装的 `StyleBoxTexture` 覆盖成了程序平面样式。UX 将其判为 P1；现已删除覆盖调用，并把 `are_dossier_candidate_assets_loaded()` 的断言升级为检查 normal style 必须是带纹理的 `StyleBoxTexture`。后续“资源已加载”不得再等同于“资源已成为最终可见载体”。
