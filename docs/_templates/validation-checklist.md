# 主代理验证 checklist

> 主代理收到 subagent 交付声明后，对其产出执行的 6 项 spot-check。
> 与 [handoff-checklist.md](handoff-checklist.md) 配对使用：subagent 自检 8 项 + 主代理复核 6 项。
> 任一项失败即判定未通过，退回 subagent 修复。

---

## spot-check 项

- [ ] **1. 文件存在**：用 LS 验证 subagent 报告的新建文件路径实际存在
- [ ] **2. 内容命中**：用 Grep 验证文档包含本次任务要求的关键术语（至少 2 个核心术语命中）
- [ ] **3. 双索引一致**：CHANGELOG.md 的 W### ID 段 ↔ file-index.md 的本文件条目，两侧 W### ID 与文件名互相匹配
- [ ] **4. 风格一致**：文档实际写作风格与 subagent 声明的双轨写作表风格匹配（大众普及/学术研究/教学讲解/个人创作）
- [ ] **5. CHANGELOG 命中**：Grep 本次 W### ID 在 CHANGELOG.md 中命中，且四件套字段（来源/文件/验证/状态）齐全
- [ ] **6. 无占位符**：Grep `<!-- TODO` 在交付文档中返回空结果

---

## 验证命令参考

```bash
# 1. 文件存在
# 用 LS 工具列出 subagent 报告的文件路径

# 2. 内容命中（替换 <术语> 为本次任务关键术语）
# 用 Grep 工具，pattern="<术语>"，path 指向新建文档

# 3. 双索引一致
# 用 Grep 工具，pattern="<W### ID>"，path 指向 CHANGELOG.md
# 用 Grep 工具，pattern="<文件名>"，path 指向 scripts/output/file-index.md

# 4. 风格一致（定性检查，无固定命令）
# 人工核对交付文档的写作风格与 docs/00-导读/项目说明.md 的双轨写作表是否一致

# 5. CHANGELOG 命中
# 用 Grep 工具，pattern="<W### ID>"，path 指向 CHANGELOG.md

# 6. 无占位符
# 用 Grep 工具，pattern="<!-- TODO"，path 指向交付文档，预期 0 命中
```

---

## 处置规则

- **6/6 通过**：接收交付，主代理继续后续同步（README/STRUCTURE/项目说明/交接文档/file-index 由主代理统一同步）
- **任一项失败**：退回 subagent，附失败项 + 证据，要求修复后重新提交 handoff-checklist 声明
- **失败 ≥ 3 项**：视为 subagent 任务理解偏差，主代理直接 fallback 接手修复，记录到方法论沉淀
