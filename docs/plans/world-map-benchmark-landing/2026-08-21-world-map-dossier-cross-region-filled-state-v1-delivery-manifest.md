# 世界地图 Dossier 跨地区同壳与整屏 filled-state v1 交付清单

> **2026-08-24 身份修订（优先于下文旧结论）**：本图只证明右侧 Dossier 的跨地区同壳与整屏回嵌，当前身份改为 `right_dossier_full_screen_reinsert_proof / left_column_reference_only`。UX 像素差分确认左栏仍与 A291 清理版逐像素相同，未形成真实 RegionCard / Schedule 组件；下文“完整 filled-state target / pending user confirmation”声明撤销。
>
> RegionCard 继续按 A305 与 `left_region_card.json` v1.0.0 的 `340×170` 正式合同执行，旧 `86:41` 规格不得回流。Schedule 依 A296 不显示具体剩余天数。详见 A321 与 `2026-08-24-world-map-left-column-baked-reference-misclassified-as-filled-state-loop-log.md`。
>
> 本次修订不否定右侧 Dossier 的同壳、文字容量与图片复用证据；它只撤销“右栏完成等于整屏完成”的错误放大。

## 结论

North 文字注册基准已获用户确认，并已在不改变 `468×1032` 壳体、固定 type token、动态槽与 `69:44` 图片合同的前提下扩展 East / Pacific。最终 A291 整屏只回填 North `warning / collapsed`，当前状态：

`filled_state_visual_target / pending_user_confirmation`

## 用户主审图

- `image_gen/2026-08-21/world-map-dossier-cross-region-filled-state-v1/08-fullscreen-filled-state-north-collapsed-1920x1080.png`
  - SHA-256：`132F1115E77432CE8AAD4EAF76242AB4B540D17F97DD522F10A63D58DC70CD1D`
  - North Dossier frozen rect：`[1416,24,468,1032]`
  - 首帧：North selected / warning / collapsed；唯一主 CTA `进入地区任务台`。

## 跨地区单卡

- East locked / collapsed：`03-east-locked-collapsed-468x1032.png`
  - SHA-256：`D1415CA3EC5820D0E858D1A92AC787FC295B7BF72FB0F16D6345C987E4EFCF9E`
  - 不显示任务；CTA `暂不可进入`。
- Pacific locked / expanded：`04-pacific-locked-expanded-468x1032.png`
  - SHA-256：`A1424F0774F68B698B4E17609E1DD6372F64EFB74AA799C8B6FDD983852DD177`
  - 只显示两条只读解锁条件；连续索引纸使用 A319 低挡边。

## QA 与机器证据

- `05-cross-region-same-shell-qa-1920x1080.png`
  - SHA-256：`46B92B47895C22B494DAA7B96805A7CD40DCF5DE28FACCA8253392BB9B52F5C9`
- `06-cross-region-capacity-audit.json`
  - SHA-256：`1A2B697CEA37C7714ECE97F08125608712AF7DC373AFF0A396E81AB1430E2535`
  - 所有 kicker / title / headline / body / Disclosure / preview / CTA 宽度探针通过。

## 真实 ImageGen 美术来源

- locked / disabled BaseSkin：`01-imagegen-locked-base-shell.png`
  - SHA-256：`EBDA5D60A152E84A9CB6E17DECE028F1201DAE6E3A6535AADAB212395E9208AA`
  - 只将 status outline 与 CTA 改为中性 disabled 色；壳体和纸件几何不动。
- A291 时间文案清理：`09-imagegen-a291-no-region-deadline.png`
  - SHA-256：`A052D61496200DC98209905169BDDA6465B8EBB3D75F5EC59818798DB0635312`
  - 只删除 North 左卡已撤销的“截稿倒计时7天”。
- 最终 prompts：`10-imagegen-prompts.md`。
- North BaseSkin / ExpandedPreviewSkin / low lip：沿用 `world-map-dossier-north-text-registration-v1` 已确认来源。

## 内容与状态

- East：`locked / collapsed`；显示正式 `声望≥55` 或罗斯威尔残页解锁缺口，无任务泄漏。
- Pacific：`locked / expanded`；正文保留完整“北美禁区带连续追踪第 2 环 / 可靠线人许可”语义；索引纸仅显示两条解锁条件。
- locked CTA：同位 `暂不可进入`，静态视觉为 disabled；真实 no-hit / hover / press 留待 runtime。
- locked Disclosure：当前文案与 `＋/－` 只证明视觉容量，正式 interaction owner 仍 pending。
- kicker / headline /部分桥接 copy 仍为 fixture，身份只在 QA 外部说明。

## 关闭的问题

- 三地区图片同为 `1104×704` canonical 源，完整等比落入 `414×264 / 69:44`；
- 三地区同壳、同字号、同基线，不使用 `fit_text`；
- East/Pacific locked 不产生第二种图片规格或组件尺寸；
- A319 高袋角未回流；
- Pacific 正式条件恢复完整语义并用三行排版通过容量审计；
- A291 旧“截稿倒计时7天”已清除，不再与 Schedule “剩余7天”形成双时间源；
- 最终整屏不堆三张 Dossier，只显示 North collapsed；
- 没有程序补纸、程序按钮底板或新任务卡。

## 双审

- UX 老哥：首轮 `FAIL / P1=2`，关闭旧时间文案和 Pacific 正式条件缩写后回归 `PASS / P0=0 / P1=0 / P2=1`。
- UI Designer：最终 `PASS / P0=0 / P1=0`；同壳、fixed token、locked 皮肤、low lip、A291 融合与强行拼贴问题通过。

## 继续冻结

- 当前不是生产切片、atlas、manifest、Godot runtime 或 hit 接线证据；
- ISSUE 票签 exact rect 未冻结；
- RegionCard `2:1 / 86:41` 冲突未解；
- locked Disclosure owner、kicker payload、fixture 正式归属未解；
- 不进入 `WeeklyRunGame`。

