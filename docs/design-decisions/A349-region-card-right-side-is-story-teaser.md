# A349：RegionCard 右侧为动态故事钩子文字区

- 日期：2026-09-04
- 状态：已裁决，字段细节待合同化
- 分类：UI / UX / 内容绑定
- cross-read tags：`world-map`、`RegionCard`、`dynamic-text`、`content-bundle`、`story-teaser`

## 用户反馈

RegionCard 右侧需要放文字，因此 V3 的宽块面背景过花，不能继续按纯装饰留白处理。

## 裁决

1. 右侧 `[168,56,156,90]` 从装饰静区改为动态故事钩子文字区。
2. 文字背后至少 80% 保持连续、安静的暖白纸面；任何色块边缘不得穿过字形区域。
3. 右侧只承载事件 headline 与最多一行次级来源/稿件类型，不重复 warning、locked、任务数或解锁条件。
4. 顶部 `status_slot` 继续唯一承载风险与访问权限；Dossier 继续承载完整正文、任务与解锁缺口。
5. 右侧不新增边框、输入框、按钮、加号或独立 hit；整张 RegionCard 仍是唯一交互面。
6. 现有 `retired_meta_safe_rect` 的“不得放动态文字”解释失效；正式资产化前必须升级合同并重命名为 `story_teaser_slot` 或等价字段。

## 暂定容量

- headline：最多两行，不自动缩小字体。
- source/type：最多一行。
- 总计最多三行；超长由内容侧短写或截断，不使用滚动和跑马灯。

## 保持冻结

`340×170`、photo/title/status 几何、`69:44` 母图复用、FrontCarrier 0°、整卡 root hit 与状态语义保持不变。

