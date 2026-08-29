# Phase 2：收尾（Wrap-up）详案

> 精简版注记（2026-08-19 治理）：本文件是 agent-session-loop 的快速路径精简版；完整协议以同仓库 `skills/mem-wrap-up/SKILL.md` 为准，冲突时以独立 skill 当前版本为准。

> 本文件在 Phase 2 激活时读取。7 步流水线（顺序固定），把 session 状态、文档、记忆审计到「可交接」状态并沉淀经验。

## 7 步总览

| 步骤 | 内容 | 工具 |
|:---|:---|:---|
| 1 | memory 健康检查 | Bash + memory_search/memory_get |
| 2 | memory audit（5 phase）+ 6 面状态矩阵 | Grep + Read + Bash |
| 3 | fileCount sync | Bash + Grep |
| 4 | 文档同步 spot-check + daily 日志追加 4 段 schema | Grep + Bash 现测 |
| 5 | 经验沉淀（sediment）→ 记忆落点（USER.md/MEMORY.md/daily 日志） | memory_search/memory_get + memory 工具 |
| 6 | 4-step verify | Grep + Read + Bash |
| 7 | memory 层 spot-check + 反向审查 | Grep + 调用 Phase 1 |

## 步骤 1：memory 健康检查
1. 列记忆根规模：Bash `wc -l ~/.qwenworkcn/awareness/main/MEMORY.md ~/.qwenworkcn/awareness/main/USER.md` + `ls ~/.qwenworkcn/awareness/main/memory/`
2. Grep / `memory_search` 扫 `USER.md` / `MEMORY.md` 的 P0/P1/P2 标记
3. 统计 `memory/*.md` 日志文件数 + 总行数
- **输出**：metrics（P0/P1/P2 数量 + fileCount + line count）

## 步骤 2：memory audit（5 phase）
1. **frontmatter audit**：Grep `^---$` 验证每个 .md 有 frontmatter
2. **dup audit**：跨文件查重复条目（同一规则双写）
3. **empty audit**：检查空文件 / stub
4. **big-file audit**：找 >50KB 超大文件
5. **broken-link audit**：Grep `file:///|\.md\)` 找链接，逐个 Bash `test -e` 验证
- **输出**：5 phase 报告 + 6 面状态矩阵

**6 面状态矩阵**：代码 / 运行态 / 文档 / 规则 / 记忆 / 工作区。每面标 `verified-current` / `changed-and-verified` / `pending` / `out-of-scope` / `not-applicable`。
- 小项目不硬凑六面（无部署 → 运行态 not-applicable；无记忆系统 → 记忆面 not-applicable）
- 版本库工作区干净（如项目有版本库）/ 测试通过 ≠ 全部同步，必须逐面验证
- 发现矛盾记录 `source of truth → stale surfaces → intended action → verification`，不当场改标 pending

## 步骤 3：fileCount sync
- Bash `find ~/.qwenworkcn/awareness/main -type f -name "*.md" | wc -l` 统计实际记忆文件数 vs `MEMORY.md` / 交接文档头部声明，drift >5% 触发警告

## 步骤 4：文档同步 spot-check + daily 日志追加 4 段 schema

### 4a 项目层文档同步 Grep spot-check（验证铁律）

> **铁律**：Grep spot-check 文件内容，验证版本号 + 任务 ID 实际出现，**不信任 prior session 的「已落地」声明**（Edit 成功 ≠ 内容已修改）。

- Grep 当前版本号：每个项目层文件 ≥1 命中（在「当前版本」段，非历史段）
- Grep 任务 ID：每个文件 ≥1 命中
- 历史 vs 现役区分：CHANGELOG 历史段保留旧值；README 头部/当前段必须更新
- 一致性以「治理层清单现场枚举 + Grep spot-check 现测」为准（不依赖版本库文件清单类校验）
- 判据：命中 <1 → P1 假收敛立即修；清单来源未留痕 → 补留痕；历史段误改 → 回滚

### 4b 当日 daily 日志追加 4 段 schema
- 路径：`~/.qwenworkcn/awareness/main/memory/<date>.md` 收尾段（经 `memory` 工具 target=`daily`，条目带 `[项目名]` 前缀）
- 4 段 schema（必含）：verification cost / throughput decoupling / ANED 3 指标 / session-end security scan（4+1 pattern：敏感信息/密钥/token/内部 URL/PII）
- 必含字段：date / session_id / milestones / retro_link

## 步骤 5：经验沉淀（sediment）

**写入协议（memory 写入协议）**：
- **Read-before-Edit**：Edit 前必须 Read 当前实际内容（不信任 cache）
- **Grep-verify-after-Edit**：Edit 后必须 Grep 验证新值落地 + 旧值消失
- **Retry-on-fail**：失败重新取回 + 重写（最多 3 次），3 次仍失败记录到当日 daily 日志
- **案例不写入 `USER.md`**：只放 active 规则 + 指针，案例归档到当日 daily 日志复盘段

**动作**：提炼复利经验（5Why ≥3 层）→ 判断归属（用户级 → `USER.md` / 项目级 → `MEMORY.md` `[项目名]` 条目 / 近期 topic → 当日 daily 日志）→ 经 `memory` 工具追加 → Grep / `memory_search` 验证 → 同步 daily 日志复盘段

**记忆毕业判据**（何时从 memory 升级到权威文档）：
1. 讲的是稳定机制（非一次性）
2. 同一教训反复出现（≥3 次）
3. 接手者必须知道（影响下次 session 恢复）
- 毕业后：结论并入 docs，memory 缩成指针，**不复制成第二处真相**
- 不毕业：一次性事故 / 个人偏好 / 未稳定探索 → 留在 memory

## 步骤 6：4-step verify
1. file exists：Bash `test -e <FILE>`
2. content count：Grep count 验关键内容命中
3. link target：Bash `readlink <LINK>` 验软链
4. 行数：Bash `wc -l < <FILE>`
- **输出**：P0=0 P1=0、P2 ≤ N_max（N_max 按项目阶段：比赛级 0 / 生产 3 / 原型 10，对齐 DRL 层 1 P2 残留规则；列数据 + 实证，不写 OK/完成）

## 步骤 7：memory 层 spot-check + 反向审查

### 7a memory 层 Grep spot-check
- 3 处落点：当日 daily 日志收尾段 / topic 段 / 复盘段（或项目内复盘文档）
- Grep 任务 ID：每处 ≥1；Grep `session_id`：每处 ≥1；Grep milestones：收尾段；Grep 复盘维度关键词：复盘段
- 判据：命中 <1 → P1 memory 层假收敛立即补；维度段缺失 → P2 立即补齐

### 7b 反向审查（调用 Phase 1）
- 5 轮 DRL：R0 表面检查 → R1a 3 verifier（必附工具证据）→ R1b 对抗性 → R2 独立审计（NOT inline）→ R3 ≥3 residual + 收敛曲线
- 继承 4 层过拟合防护 + R1a/R1b 硬性要求 + R1b 7 项反模式清单（silent skip / 正例 bias / 0 finding 滥用 / 严重度降级 / class-level 偷懒 / residual 敷衍 / 工具证据缺失）

## 分阶段汇报模板

```text
## mem-wrap-up 收尾完成

**影响**：<消除了哪些误导、风险或交接成本>

**改动 / 新建**
- <文件> — <改了什么，为什么>

**待你确认**
- 删除候选：<文件 + 理由>；未确认前一个都没删
- 无法裁决：<矛盾 + 两边证据>

**遗留**：<pending / out-of-scope / 未消除 warning；没有就写「无」>
```

**强制要求**：必须明确列出 `pending`、`out-of-scope` 和未消除 warning；不能用「保证干净」掩盖；与 verdict 禁词互补。

## Failure handling
- 任一步骤失败 → 不继续下一步，stderr 报告
- subagent idle fallback：撞 NEEDS_CONTEXT ≥3 → 缩小 scope + 给具体 file:line
- Token 超额 → 降级 1 subagent / 分批派 / 等 user 拍板

## 触发条件
- 用户说「收尾 / wrap up / session 收尾」；「继续」但工作流已 sediment
- 主动判断：30+ 轮 / token 接近上限 / 重大里程碑
- 怀疑 session 不完整收尾
