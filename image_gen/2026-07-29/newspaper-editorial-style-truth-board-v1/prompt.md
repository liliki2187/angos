# 报刊视觉语法真值板提示词记录

## 参考图权限

- `benchmark-board-01.png`、`benchmark-board-02.png`：主画法与情绪真源。负责现代怪新闻周刊拼贴、粗颗粒综合色面、尺度跳变、纸品关系、符号方言和好奇邀请感。
- 世界地图 A / 区域地图 R-21 并排图：仅负责跨屏综合色彩、纸张温度、WMW 眼睛 / 地球、索引签、夹具、条码、蓝色连接线和状态色职责；不提供报刊主头图的场景画法。
- 用户提供的两张符号裁切：负责手绘 globe、TOP SECRET、WMW / MW cutout、eye triangle、question warning、black hand、警示牌和票签的线重、剪纸边与错印感。
- 上一轮被否决的报刊完整界面不进入任何参考。

## 首轮真值板

画布只验证五项，不生成完整三栏：

1. 最终显示尺度的 M330 主头图。
2. 同一母图在候选缩略图中的复用。
3. 打开周刊的局部版式片段。
4. 不依赖长文案的“轨迹进入缺失纸洞，但仍盖 ON TIME / APPROVED”视觉黑色幽默。
5. WMW 三方言符号群：手工贴纸、机构印刷、状态索引。

画法主句：

`modern editorial collage / medium-coarse faceted color modeling / varied large polygon planes / active cool adjacent-color shifts / symbolic tabloid absurdity / flat printed cut-paper silhouettes / orthographic paper assembly / matte ink / visual curiosity before institutional order`

M330 目标：主体 `6–9` 个结构块，环境 `2–4` 个大块，`4–5` 档离散明度，`3–4` 个相关色相组，保留 `20–35%` 安静负空间。禁止逐窗、轨枕、地台、车站零件、真实纵深、电影照明、AO、渐变、均匀微三角、照片加 low-poly 滤镜。

## v2 定向修正

首轮板的拼贴、色彩和符号关系保留，只把三处列车统一改为同一母图：

- 无山体、地平线、写实车站和轨道透视。
- 列车只保留楔形车头、长车身、连续窗带、底盘、灯块与少量综合色面。
- 两条平面轨迹线直接进入缺失纸洞，不画轨枕。

结果关闭写实透视，但列车过度压缩成图标层，降级为 `over_minimal_train_diagnostic`。

## v3 颗粒度回调

继续只改三处列车母图：

- 保留 `7–9` 个主结构块，但以约 `12–16` 个大小不均的中大型综合色面塑造。
- 窗带仍是一条连续大块，只允许两段相邻明度，不生成独立窗户。
- 恢复烟熏钴蓝、灰蓝、冷青与一小块橄榄灰的相邻色变化。
- 环境只保留 `3–4` 个抽象纸面块，暗示不可能站台与夜班信号场，不恢复写实场景。

当前 v3 为 `medium_coarse_granularity_candidate_pending_user_review`。
