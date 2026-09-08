# 2026-09-03 MapField 侧栏内容注册越界误判 Loop Log

## 结论

`05-fullscreen-north-selected-warning-1920x1080.png` 与 `06-fullscreen-east-selected-locked-1920x1080.png` 失去交付资格。它们把本应局限于 MapField 的视觉 fixture 扩大为左卡与 Dossier 重组，造成图片、标题、正文和纸壳注册错位，玩家第一眼呈现明显的强行拼贴。

## 用户反馈

用户圈出右侧 Dossier 与左侧 RegionCard，明确指出“大量文字和图片不对应，拼贴感严重”。右侧照片压入标题与正文，左侧标题、状态、照片和锁记没有服从同一视觉槽位。

## 错误发生在哪里

1. 本轮原始任务是 MapField dynamic overlay fixture；父级为了证明 East `selected+locked` 的原子更新，未经新的组件装配 Gate 就扩大范围，重组了左卡和 Dossier。
2. 合成脚本把合同中的逻辑槽位坐标直接套到包含透明 bleed、夹子、叠纸和状态层的美术母件上，没有先验证资产实际 alpha origin、内容原点和 state overlay 的可见边界。
3. 机器审计只检查 MapField、canonical 图片比例和状态差分，没有把所有被改动的左卡/Dossier 文字—图片—纸壳注册纳入 Gate。
4. 父级目视复核主要盯着 MapField 的 selected、Beacon 与 Evidence，未逐个以 100% 检查左栏和右栏，却把两张整屏列为主要交付图。

## 为什么已有规则没拦住

- “原子消费者必须同步”是运行时状态合同，不等于允许在视觉 fixture 阶段伪造未验证的侧栏装配。
- `left_region_card.json` 与 `right_dossier_page.json` 的 rect 证明逻辑槽位，不证明任意 ImageGen 母件都可以直接以同一图片边界作为坐标原点。
- MapField 的 `machine_pass=true` 被错误扩大成了完整整屏机器通过；审计范围与交付声明不一致。

## 立即止损

- 保留 `03`、`04` 两张 `960×902` MapField 状态图与 `07` 局部 A/B 板，继续等待用户判断 Beacon、selected、label 与 Evidence。
- 将 `05`、`06` 两张错误整屏标记为 `rejected_side_registration_composite / diagnostic_only`，不得继续展示为视觉目标或实现输入。
- 新整屏 `12-fullscreen-north-mapfield-only-corrected-1920x1080.png` 从已验证的 `world-map-filled-state-legibility-v2` 整屏恢复左右栏，只替换冻结 MapField rect。
- East 仅保留 MapField 局部伴随态；左卡、Dossier、CTA 的 East 原子更新延后到各组件正式装配或隔离 runtime preview，不再用未经验证的静态拼贴冒充。

## 新防线

1. **范围一致性 Gate**：MapField fixture 默认只能改 `[432,154,960,902]`；任何跨出该矩形的视觉变化必须新开组件 brief 和独立注册审计。
2. **Touched-region 100% Gate**：交付整屏前，对每个被触碰组件输出 100% crop；只检查中央区域不得宣称整屏通过。
3. **Alpha-origin Gate**：使用无字美术母件前，必须记录文件尺寸、alpha bbox、FrontCarrier 原点和各状态层可见 bbox；合同 rect 不得替代资产原点测量。
4. **声明范围 Gate**：机器报告必须显式列出 touched rect；审计没有覆盖的区域不得写入 PASS。
5. **运行时原子更新边界**：静态美术 Gate 可用局部伴随态证明状态语言；跨组件原子更新必须由正式装配或 runtime state preview 证明。

## 修复证据

- 修正整屏：`image_gen/2026-09-03/world-map-mapfield-dynamic-overlay-fixture-v1/12-fullscreen-north-mapfield-only-corrected-1920x1080.png`
- 范围审计：`image_gen/2026-09-03/world-map-mapfield-dynamic-overlay-fixture-v1/13-corrected-fullscreen-scope-audit.json`
- 审计结果：MapField 外逐像素一致；左栏逐像素一致；Dossier 逐像素一致。

## 当前阶段

`corrected_mapfield_context_fixture / pending_user_visual_gate`

不进入 Godot、atlas、manifest 或 `WeeklyRunGame`；不冻结 Beacon wrapper、label 或 hit rect。

## 后续追查：旧 Dossier 夹具本身也有内容错配

A344 后按用户“继续”建立 North Carrier 原生原点注册纵切时，进一步发现历史 `15-dossier-filled-warning-expanded-x2.png` 并非单纯被整屏脚本放错位置：该组件夹具自身就把“北美禁区带 / 洗衣店漂海”的文字与东亚/金字塔照片混配。`18-dossier-state-matrix-audit.json` 只检查尺寸、比例、CTA 位移与状态语义，没有核对地区 ID、标题 payload、正文 payload 和 canonical 图片 resource 是否属于同一内容实体，因此曾出现机器未报错但玩家第一眼错误的假安全。

新增防线：

1. **内容身份 Gate**：每个 filled fixture 必须记录 `content_id / selected_region_id / canonical_resource_path / canonical_sha256 / title_fixture_id / body_fixture_id`，并断言均属于同一地区。
2. **像素同源 Gate**：RegionCard 与 Dossier 两个照片槽必须分别逐像素等于同一母图直接等比缩放；只验证比例相同不够。
3. **原生原点 Gate**：组件完整画布 `[0,0]` 是唯一 root；alpha、visible、tight bbox 永远只作诊断。页面只挂组件 root，禁止重新装配内部照片、文字或状态层。
4. **历史证据降级**：旧 Dossier 填充图只保留无字壳几何与状态层历史参考，不再承担内容注册证明。

修复证据：

- `image_gen/2026-09-03/world-map-native-origin-registration-slice-v1/01-world-map-component-registration-matrix-v1.json`
- `image_gen/2026-09-03/world-map-native-origin-registration-slice-v1/02-north-carrier-native-origin-board-1920x1080.png`
- `image_gen/2026-09-03/world-map-native-origin-registration-slice-v1/03-north-carrier-registration-audit.json`（14/14）
- `image_gen/2026-09-03/world-map-native-origin-registration-slice-v1/04-north-carrier-integrity-closeups-1920x1080.png`

该追查仍只关闭实施前注册合同，不授权 Godot、atlas、最终 manifest 或 `WeeklyRunGame`。

## 防线实测：三地区正向通过，错配负向必拒绝

- North、East、Pacific 均改由唯一 `content_bundle_id` 解析 Card、Dossier、图片、状态与 CTA，页面或组件不得再独立选择这些字段。
- 三地区正向样本合计 41 项机器断言全部通过；每区 Card 与 Dossier 的图片槽均逐像素等于同一 canonical 母图直接缩放。
- 负向用例以 East 为基础，真实注入 North photo bundle 与 North headline bundle；验证器返回 `east_negative_case_pass=false`、`negative_failure_detected=true` 和两个明确失败原因。
- 该负向结果证明新 Gate 能拦截“几何完全正确但内容跨地区”的错误，而不仅是记录一份说明文字。
- 证据：`image_gen/2026-09-03/world-map-content-identity-binding-slice-v1/06-region-content-binding-audit.json`。

本次关闭 content-binding 错配防线；运行时字体、动态交互与整屏状态同步仍属于后续阶段。
