# 派遣签批台 V17.2 实际生图记录与复审

> 日期：2026-06-22  
> 状态：目标效果稿候选 / not production benchmark  
> 输入：`dispatch-signoff-v17-2-imagegen-handoff.md` + V17.1 默认图 / overlay / no-text 候选  

## 1. 产物

| 文件 | 用途 | 结论 |
| --- | --- | --- |
| `docs/screenshots/2026-06-22-dispatch-signoff-v17-2-imagegen/01-v17-2-no-text-asset-master-candidate-a.png` | no-text asset master 候选 | 可作为无字资产母版方向候选；不是生产 atlas。 |
| `docs/screenshots/2026-06-22-dispatch-signoff-v17-2-imagegen/04-v17-2-filled-state-text-mock-candidate-c.png` | filled-state text mock 主候选 | 三张里最接近目标效果稿，可作为下一轮 Godot 目标对照。 |
| `docs/screenshots/2026-06-22-dispatch-signoff-v17-2-imagegen/06-v17-2-candidate-hover-expanded-candidate-b.png` | candidate hover 展开候选 | 可作为 hover / 展开状态目标稿候选；密度接近上限。 |

其余候选保留为过程样本：

- `02-v17-2-filled-state-text-mock-candidate-a.png`：图文融合可参考，但器材层曾退回“托盘”语义。
- `03-v17-2-filled-state-text-mock-candidate-b.png`：修正器材语义，左下状态基线仍有偏差。
- `05-v17-2-candidate-hover-expanded-candidate-a.png`：展开态思路可参考，但原始比例不是 16:9。

所有交付主候选均已归一为 `1920x1080`；raw 文件保留同目录用于追溯。

## 2. 美术指导复审结论

`angus_art_director` 生成后复审结论：有条件通过为 V17.2 目标效果稿候选；不能称为生产标杆 / 资源标杆 / 真源候选；也不只是偏差案例。

通过点：

- 深海军蓝主场成立，没有回到灰蓝 SaaS 或旧报纸档案墙。
- 象牙白纸面干净，没有明显泛黄、脏污、旧档案感。
- 红橙签批、CTA、短标签清楚，符合 Angus 的紧迫 / 盖章 / 发行语义。
- 功能面大体正交，没有斜纸张不可用问题。
- 像素、半调、裁切点、套印边缘已经进入画面语言。

未达生产标杆原因：

- 半调 / 像素点仍有一部分像角落装饰，尚未完全成为签批、连接、状态、禁入区、字段分隔的结构语言。
- 绿色 `移出 / + / 撤回` 按钮仍偏通用后台 / 手游素材包。
- 候选角色头像风格不齐，需另交角色美术专审。
- 底部资源抽屉展开后密度接近上限，仍有 SaaS 面板风险。
- 尚未输出明确的 `content_rects / no_text_rects / hit_rects` 拆层 overlay 与组件状态矩阵。

## 3. 下一步 Gate

不得直接从这批 filled-state mock 裁生产资产。进入下一环前必须补：

1. 基于 V17.2 主候选重新绘制安全区 overlay，明确 content / no-text / hit rect。
2. 把半调 / 套印从角落装饰整理成稳定结构语言：签批、队伍连线、候选来源、可签批状态、印章结果。
3. 把绿色按钮改成 Angus 语境内的贴签 / 压章 / 夹条 / 机器按键语言。
4. 角色头像另交 `angus_character_pixel_director` 专审，避免普通插画头像和高清微像素 Q 版混用。
5. Godot / 运行时必须渲染所有中文、数值、头像、按钮文案；生图文字只作为效果 mock。
