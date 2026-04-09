# full_chain

这个目录不再承载 Angus 的正式周循环逻辑。

## 当前用途

- 保留旧场景路径 `res://scenes/gameplay/full_chain/FullChainGame.tscn`
- 通过显式 shim 把历史入口转发到 `weekly_run/WeeklyRunGame.tscn`

## 维护规则

- 新功能只在 `../weekly_run/` 继续实现
- 如果后续确认没有任何兼容需求，再统一归档或删除这个目录
