# 发刊报道图片两规格合同黑白结构审阅板 v1｜交付清单

## 结论

已完成可审阅的两规格图片合同候选。UX 与 UI Designer 均为 `PASS WITH CHANGES`、P0 为 0，并共同推荐：`1024×1024` 方形母图、`189×189` 普通位、`210×210` 副头版方图与 `15:8` 主头版扩图。

当前仍处于用户裁决前的结构候选，不是最终视觉 UI，也未修改 Godot、组件合同或 GDD。

## 交付物

- 可运行结构板：`docs/prototypes/weekly-editorial-two-spec-image-contract-review-v1/index.html`
- 使用与边界说明：`docs/prototypes/weekly-editorial-two-spec-image-contract-review-v1/README.md`
- `1920×1080` 主审阅图：`docs/screenshots/2026-07-21-weekly-editorial-two-spec-image-contract-review-v1/01-two-spec-contract-overview.png`
- 双页局部图：同目录 `02-two-page-square-layout-detail.png`
- 主头版比例局部图：同目录 `03-headliner-ratio-decision-detail.png`
- 机器审计：`docs/screenshots/2026-07-21-weekly-editorial-two-spec-image-contract-review-v1/audit.json`
- 证据纠偏记录：`2026-07-21-weekly-editorial-two-spec-image-contract-review-v1-evidence-loop-log.md`

## 推荐规格

| 用途 | 推荐规格 | 处理方式 |
| --- | --- | --- |
| 构图真源 | `1024×1024` | 每篇报道唯一核心构图 |
| 候选缩略图 | `64×64` | 方形母图直接缩放 |
| 普通版位 | `189×189` | 方形母图直接缩放 |
| 副头版 | `210×210` | 左方图 + `12px` 间隔 + `188×210` 文字栏 |
| 主头版 | `1920×1024 / 15:8` | 方形核心左右各扩 `448px`，运行显示 `410×219` |

`224×224` 副头版方图只保留为用户可明确选择的备选；它会把右侧文字栏压窄，不进入当前推荐稿。

## 结构处理

- 候选 `64×64` 已符合方图原则，不改候选卡外框。
- 副头版取消整宽横图，改为方图与右侧文字栏；无摘要字段时只显示标题、meta 与留白。
- 四个普通版位统一为方图，保留现有外槽与标题在图上方的阅读顺序，只压缩内部间距。
- 主头版保留横图，但横图只允许由方形母图向两侧补环境生成；两翼不得新增关键主体、线索或文字。
- 不产生第三种图片比例，也不允许从横图反裁方图。

## 验证

- 结构板视口与文档尺寸均为 `1920×1080`。
- 两张页面、三个审阅区均完整位于视口内。
- 决策区与底部声明重叠为 `0px`。
- 浏览器控制台错误与警告为 `0`。

## 待用户裁决

1. 是否冻结主头版 `15:8`。
2. 是否冻结副头版 `210×210` 方图。
3. 是否确认无摘要字段时保留留白，不新增字段。

用户放行后，下一轮才更新正式视觉包装候选中的图片框；组件合同、Godot 与 GDD 仍需另行授权。
