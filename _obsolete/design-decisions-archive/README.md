# design-decisions 拆分前全文归档

- `archive-raw-adoption-log.md`：`docs/设计采纳记录.md` 在 2026-06-15 拆分为总索引 + 分册前的全文归档（151KB）。2026-07-08 从 `docs/design-decisions/` 挪入 `_obsolete/`：它不是新增写入口，与活分册同目录时容易被全文检索误命中为现行决策。现行真源为 `docs/设计采纳记录.md` 总索引与 `docs/design-decisions/` 各分册；仅在需要考证拆分前原文时读取本文件。
