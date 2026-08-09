# 方法论沉淀

> 本目录沉淀 xiyouji 项目过程中积累的可复利方法论经验。
> 创建于 2026-07-26（v2.0.43 W070 落地）·当前版本 v2.0.60（W087 落地）
> 与 [项目根目录 README.md](../../README.md) / [STRUCTURE.md](../../STRUCTURE.md) / [CHANGELOG.md](../../CHANGELOG.md) / [交接文档.md](../../交接文档.md) 配套使用。

---

## 目录索引

| 编号 | 主题 | 文件 | 一句话核心 |
|:---:|:---|:---|:---|
| 1 | DRL 真循环 | [DRL真循环.md](DRL真循环.md) | 审查→修复→**重新审查**的循环，直到连续 N 轮 0 问题才收敛 |
| 2 | 三 skill 闭环 | [三skill闭环.md](三skill闭环.md) | deep-review-loop → mem-wrap-up → self-evolution，闭环不可断裂 |
| 3 | E1 铁律 | [E1铁律.md](E1铁律.md) | prior session 报告 ≠ 实际状态，主代理必须 spot-check 验证 |
| 4 | Preflight 与 Subagent 模板 | [Preflight与Subagent模板.md](Preflight与Subagent模板.md) | 派 subagent 前先验证事实，subagent 失败时主代理直接 fallback |
| 5 | 双索引可追溯改造 | [双索引可追溯改造.md](双索引可追溯改造.md) | CHANGELOG 正向时间线 + file-index 反向文件索引 |
| 6 | E2 文档同步区分历史 vs 现役 | （待创建·详见 user_profile） | 文档同步时区分历史变更日志条目（保留旧值）和现役描述（必须更新为新值） |
| 7 | E1 升级版铁律（毕业判据满足） | [E1铁律.md](E1铁律.md) §三 | prior session 报告"修复已落地"时主代理必须 Grep spot-check 验证文件内容·3/3 毕业判据满足·已驱动 mem-wrap-up Step 4a/7a 协议升级落地 |
| 8 | 并行 Edit 竞态问题 | （待创建·详见 user_profile） | 同一文件的多个 Edit 并行执行时后者覆盖前者·应串行执行或 replace_all |

---

## 阅读路径

### 新读者快速路径（5 分钟）

按 1→2→3→4→5 顺序读，每篇 5-10 分钟。

### 项目接手者路径

1. **必读**：[DRL真循环.md](DRL真循环.md) + [三skill闭环.md](三skill闭环.md) — 决定如何审查工作
2. **重要**：[E1铁律.md](E1铁律.md) — 决定如何验证 prior session 报告
3. **可选**：[Preflight与Subagent模板.md](Preflight与Subagent模板.md) — 决定如何派 subagent
4. **参考**：[双索引可追溯改造.md](双索引可追溯改造.md) — 决定如何追溯变更

### 方法论作者路径

每篇文档遵循统一结构：
- **问题背景**：撞坑场景 + 复现计数器
- **方法论**：核心原则 + 操作步骤
- **复现案例**：N 次复现记录 + 严重度评级
- **修复策略**：具体可执行动作
- **关联文档**：跨文件链接 + 上游 skill 位置

---

## 复利经验总览

| 经验名 | 复现次数 | 严重度 | 首次出现 | 最近复现 |
|:---|:---:|:---:|:---|:---|
| DRL 假收敛 | 多次 | 严重 | 2026-07-12 | W086 |
| E1 跨 session git tracked | 23/23（含 W085/W086 预防成功 0 文件） | 严重 | 2026-07-22 | W086 |
| E1 升级版修复落地验证 | 3/3 毕业判据满足（W083→W084→W085）+ W086 毕业后首例新案例 | 严重 | 2026-07-24 W039 | W086 |
| Subagent 工具证据盲信 | 多次 | 严重 | 2026-07-19 | 2026-07-21 |
| W069 系统性编造 line 号 | 1/1 | 严重 | 2026-07-26 | W069 |
| 并行 Edit 竞态 | 7/7+ | 中等 | 2026-07-23 | W086 |
| 改动后影响面扫描 | 1/1 | 中等 | 2026-07-22 | 2026-07-22 |
| Preflight 三轨验证 | 11/11 完整执行（W076-W086） | 中等 | 2026-07-26 W076 | W086 |
| chapter 归属稳定盲区 | 3/3（W074/W075/W082） | 中等 | 2026-07-26 W074 | W082 |

---

## 与上游 skill 关系

本目录是**项目内沉淀层**，对应上游 TRAE skill：

- `C:\Users\12739\.trae-cn\skills\deep-review-loop\SKILL.md`（v1.2.0 含 4 层防护）
- `C:\Users\12739\.trae-cn\skills\mem-wrap-up\SKILL.md`（v1.1.0 含 6 面状态矩阵）
- `C:\Users\12739\.trae-cn\skills\self-evolution\SKILL.md`

skill 文件是**协议层**（约束 + 流程定义），本目录是**案例层**（项目内复现记录 + 修复策略）。两者互补：skill 文件不变，本目录按项目实际复现追加。

---

## 维护规则

1. **新增经验**：每次新撞坑（P0/P1）必须追加到对应主题文件 + 本 README 复利经验总览表
2. **复现计数器**：每次同根因复现必须更新计数器（不重置，累加）
3. **跨文件链接**：所有"详见 [xxx]" 必须用相对路径 + 锚点
4. **不修改上游 skill**：本目录只记录项目内案例，skill 协议升级走 skill 文件
5. **关联到 W### ID**：每条经验必须关联到首次出现的 W### ID（CHANGELOG 索引）
6. **W087 新增规则**：E1 升级版铁律毕业后，新复现案例不再累积到 3/3 计数器，作为毕业后处置段独立记录（详见 [E1铁律.md](E1铁律.md) §三 E1 升级版 row 7）

---

## 关联文档

- [../../README.md](../../README.md)：项目说明（当前版本 v2.0.60）
- [../../STRUCTURE.md](../../STRUCTURE.md)：目录结构
- [../../CHANGELOG.md](../../CHANGELOG.md)：变更日志（W001-W087）
- [../../交接文档.md](../../交接文档.md)：跨 session 交接
- [../../scripts/output/file-index.md](../../scripts/output/file-index.md)：反向文件索引
