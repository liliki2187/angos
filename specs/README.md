# 规格包说明

本目录用于保存按功能范围划分的工作规格包。

## 推荐结构

```text
specs/
  <feature-slug>/
    spec.md
    tasks.md
    handoff.md
```

## 规则

- 当一个功能跨越设计、代码、UI 或生产协作边界时，就应该建立 spec
- spec 应回链到相关的 `design/gdd/` 或 `docs/architecture/` 文档
- 使用 `handoff.md` 记录本次实际落地了什么，以及还剩下什么
