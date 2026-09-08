# 世界地图 Dossier 真实内容填入版 v1｜交付清单

## 结论

本轮完成一张 `1920×1080` 的三地区 Dossier filled-state 风格 / 容量验证板：北美、东亚、太平洋由同一个 ImageGen 无字母壳像素级复制，三张现有 `1104×704 / 69:44` 母图放入统一 `414×264` 合同槽的等比预览，真实中文与状态差异由精确合成层恢复。

UX 老哥最终回归与 UI Designer 终审一度判 `PASS / P0=0 / P1=0`，但用户随后否决玩家可见排版：文字没有对准真实纸件，字号与层级失真，整体呈现强行程序拼贴。用户 Gate 覆盖 agent 结论；本板当前只保留为同壳、同图槽、状态数据诊断，不再是视觉 / 容量目标，不进入 atlas、manifest、Godot 或 `WeeklyRunGame`。

## 2026-08-21 用户复核修订

- 当前状态：`rejected_by_user_text_registration_and_type_scale_mismatch / diagnostic_only`。
- 失败原因：ImageGen 母壳可见纸面与 frozen slot 未注册；程序又覆盖标题纸、图片框、正文纸、Disclosure、preview 与 CTA，并逐字段自由缩字。
- 下一步：停止三联 beauty board，先做一张 `468×1032` North 1:1 内容注册稿；建立 `frozen slot / visual_write_rect / no_text_rect` 三层证据，固定 type tokens，分别验证 collapsed / expanded。
- 复盘：`2026-08-21-world-map-dossier-text-registration-mismatch-loop-log.md`。

## Router Card

- 任务类型：现有 UI 的 filled-state 风格 / 内容容量 / 状态差异验证。
- 风险等级：`risky / experimental`。
- 当前产物类型：`filled_state_content / capacity / state_delta concept`。
- 必调链：现有 UI 改进先由 `ux_laoge` 定义内容与状态边界，再由 `ui_designer` 给出 A+ 三壳板规格；生成后按同一顺序回归。
- 美术例外：clean-low-poly weekly 支线直接对照两张 benchmark，不调用旧像素 / 半调坐标系美术指导。
- 不验证：正式状态语义、locked Disclosure 最终行为、preview 最终承载位、runtime 字体、disabled 对比、atlas 或 Godot。

## 用户裁决

A317 已登记：用户确认上一张 Dossier 正交组件板的版面样式方向没有问题，并要求下一步使用统一地区图片规格与真实文字制作 filled-state 风格稿。该采纳只覆盖版面 / 组件语言方向，不等于 exact 几何或生产放行。

## 输入真值

### 美术参考

- `design/art-direction/references/clean-lowpoly-weekly-branch/benchmark-board-01.png`
- `design/art-direction/references/clean-lowpoly-weekly-branch/benchmark-board-02.png`
- `image_gen/2026-08-19/world-map-dossier-orthogonal-component-board-v1/02-imagegen-native-art-board.png`

### frozen 合同

- `design/ui-contracts/world-map/right_dossier_page.json`
- `design/ui-contracts/world-map/right_mission_intel_button.json`

### canonical 地区图

- `north_america_story_1104x704.png`
- `east_asia_story_1104x704.png`
- `pacific_story_1104x704.png`

三张均为 `1104×704 = 69:44`。板内采用 `345×220 = 69:44`，即源图 `5/16` 等比缩放；完整画幅，无裁切、无拉伸、无另做缩略图。

## 交付物

### 主审图

- `image_gen/2026-08-21/world-map-dossier-real-content-filled-state-v1/04-real-content-filled-state-style-target-1920x1080.png`
- 尺寸：`1920×1080`
- SHA256：`9D09D2A7C4E11954BE7E8C5D2B2B32EDC80F3CCD67573D00CD6372618CA0B3E9`

### ImageGen 美术母壳

- 初始无字母壳：`02-imagegen-master-shell.png`
  - 尺寸：`845×1862`
  - SHA256：`59976993E34C30032A6FA3622A32A66C97D117F2911835DC6DB47604316C63A7`
  - 状态：大夹子遮挡 title 安全区，只保留为第一轮美术 donor / 修正前证据。
- 小夹子定点修正版：`02b-imagegen-master-shell-small-clip.png`
  - 尺寸：`887×1774`
  - SHA256：`D1538F4B6BAA04B786333B816A5084A9439C6E0160D6F7965BDE5465FA632B26`
  - 通过第二次真实 ImageGen 只把夹子缩回顶部；程序先中心裁为 `468:1032` 关系后再缩放，不拉伸 donor。
- prompt：`01-imagegen-master-shell-prompt.md`

### 精确合成层

- `03-compose-filled-state-board.py`
- 只负责：同壳复制、`69:44` 图片复用、真实中文、expanded / collapsed / locked 差异、FORMAL / STORY FIXTURE / PENDING 板外标识、8 字标题压力、North collapsed crop 与 QA 文案。
- 不负责生成文件夹、纸材、综合色、夹子、接触阴影或低多边形地区图。

## 内容矩阵

### 北美 Expanded

- 正式地区名：`北美禁区带`。
- story fixture：`洗衣店里出现了一片海`。
- status：`红线升温`只作为容量样例，并在板外标 `PENDING`。
- Disclosure：`已显示 2 / 共 4 条` 与 `－`。
- 正式预览：
  - `51 区外围公路｜线索 · 耗时 2 天`
  - `罗斯威尔档案残页｜线索 · 耗时 1 天`
- 两条预览只读，不画按钮，不显示第三、第四条。

### 东亚 Locked / Collapsed

- 正式地区名与解锁缺口；story headline / body 明确标 fixture。
- 不泄漏正式任务；CTA disabled。
- Disclosure 行为继续 `PENDING`，静态板不裁决可展开或 disabled。

### 太平洋 Locked / Collapsed

- 正式地区名与解锁缺口；story headline / body 明确标 fixture。
- 正式任务数据为空，不为视觉密度伪造任务；CTA disabled。

## 回归修正

UX 首审将第一版判为“风格草稿 PASS、最终容量证明 FAIL”，要求关闭五个 P1。最终版已完成：

1. 删除任务行右侧与“线索”统计冲突的 `常驻 / 限时`。
2. 删除 ExpandedPreviewSkin 内重复的 `已显示 2 / 共 4 条`。
3. North collapsed 证据改为可读 headline / body / Disclosure crop。
4. 通过真实 ImageGen 把夹子缩回顶部，并用实际 BaseSkin 同框证明 8 字标题 / status 安全区。
5. 恢复 `PREVIEW CARRIER PENDING` 板外说明；当前仅临时采用 `expanded_body_capacity`。

UX 回归后判 `PASS / P0=0 / P1=0`。

## UI 终审

- 三壳同源与统一规格：PASS。
- clean-low-poly weekly 综合色与稿夹气氛：PASS。
- 真实文字密度：PASS，没有滑回后台表格。
- locked 蓝色空袋：本轮可接受；不伪造任务。
- QA rail：不抢三份 Dossier 主视觉。
- P0：0；P1：0。
- P2：locked 空袋的柔亮纹理后续可改为更平、更哑光的 `4–6` 个宽钴蓝块面；disabled CTA、fixture metadata 与小字需在正式 runtime 阶段复核。

## 当前状态

`rejected_by_user_text_registration_and_type_scale_mismatch / diagnostic_only`

## 用户当前裁决

三联版玩家可见排版未通过；不再要求用户从当前图判断内容密度或 locked 空袋效果。下一有效审阅物应是 1:1 North 单页内容注册稿，而不是当前图的局部挪字版。

## 阶段边界

- `红线升温`正式可见语义仍未裁决。
- locked Disclosure 行为仍未裁决。
- `region_body / expanded_body_capacity` owner 冲突仍未裁决。
- 东亚、太平洋 story copy 与北美 metadata 仍有 fixture。
- 三张 canonical 图当前仍是 runtime preview asset，不是生产美术母版。
- 不进入 atlas、asset manifest、Godot、`WeeklyRunGame` 或正式壳体制作。
