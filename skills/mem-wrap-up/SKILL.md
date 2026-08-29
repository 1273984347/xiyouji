---
name: mem-wrap-up
description: Enforces 7-step session wrap-up with memory audit, 6-face knowledge governance, and DRL. Invoke at session end, when user says "wrap up/收尾/继续/洁癖", or when docs and code mismatch.
metadata:
  author: distilled-from-external-vault
  version: "1.3.0-qwenwork-native"
  source: 外部 vault 版原文件（来源路径已脱敏；2026-06-24）
  bridge_note: "7 步 (skill 流水线) vs 4 段 schema (daily 日志追加格式) 桥接 — 步骤 4 的 daily 日志追加按 4 段 schema 形式"
---

# mem-wrap-up Skill

> 本 skill 由外部记忆库/skill 库（vault）版蒸馏而来：剥离原脚本 hook（bash 脚本 / Python hooks / Node hooks）/ 原目录结构与路径 / 原规则术语引用 / 原笔记链接格式，保留 7 步流水线骨架 + 4 段 daily 日志 schema + verdict 禁词合规 + Failure handling + residual risk 协议。Step 7 联动 deep-review-loop skill（已蒸馏）。

**Announce at start:** "I'm using the mem-wrap-up skill to run the 7-step session wrap-up pipeline."

## 运行平台：千问办公 QwenWork

1. 本 skill 运行于**千问办公（QwenWork）**；正文所有路径、工具、检索都按 QwenWork 原生写，不使用外部平台占位符。
2. 记忆根：`~/.qwenworkcn/awareness/main`（`MEMORY.md` 跨会话长期记忆 / `USER.md` 用户级偏好与铁律 / `memory/YYYY-MM-DD.md` 每日日志）。写入经 `memory` MCP 工具（target=`memory` / `user` / `daily`），检索经 `memory_search` / `memory_get`；`MEMORY.md` 与 `USER.md` **禁止直接 Edit/Write**。
3. 技能根：`~/.qwenworkcn/skills`；技能增改删用 `qwenwork_skill_manage`（action `create` / `patch` / `edit` / `delete`）。
4. 可用技能列表由会话 system-reminder 注入；调用某技能用 `Skill` 工具。
5. 工具映射：终端用 `Bash 工具`（PowerShell 语义可 `powershell.exe -Command "…"`；存在性/软链/行数/体量校验用 `test -e` / `readlink` / `wc -l < <FILE>` / `find -size +50k` / `ls -R`）；子代理用 `Agent 工具`（`subagent_type`：`general-purpose` / `Explore` / `Plan`，可并发 / 可后台）；文件读写 `Read` / `Write` / `Edit`，检索 `Grep` / `Glob`；记忆读写 `memory` / `memory_search` / `memory_get`。
6. 文件保护：删除一律进系统回收站（禁 `rm` / `del`）；改用户文件前先备份（Git 版本库内项目除外）。
7. QwenWork 项目不保证为 git 库；一致性校验一律走「治理层清单现场枚举 + Grep spot-check 现测」，不依赖版本库文件清单类校验。
8. 步骤 4a 的「项目层文档」为**全局通用机制**：运行时现场枚举当前工作区的治理层文档，不预置任何具体项目清单（本文件服务所有项目）；项目专有清单留在各项目自身仓库副本，不进全局。

**记忆落点速查（正文各步骤引用）**

| 沉淀内容 | QwenWork 落点 | 写入方式 |
|:---|:---|:---|
| 用户级偏好与铁律 | `USER.md` | `memory` target=`user` |
| 项目级规则 / 长期经验 / 稳定速查 | `MEMORY.md`（条目带 `[项目名]` 前缀） | `memory` target=`memory` |
| 收尾 4 段日志 / 近期 topic / 当日经验记录 / 复盘报告 / Skill 缺口清单 | 当日 daily 日志 `memory/<YYYYMMDD>.md`（条目带 `[项目名]` 前缀） | `memory` target=`daily` |
| 稳定套路（pattern / heuristic 层） | `~/.qwenworkcn/skills/<name>/SKILL.md` | `qwenwork_skill_manage` 建/补 |
| policy 层规则 | `MEMORY.md` | **须人工确认后**并入 |

## 子代理不可用降级（2026-08-24 新增）

**触发**：平台派发 subagent 返回不可用/FORBIDDEN（如定价限制 code 112），或环境中无子代理机制。

**降级规则**（降级不是跳过，收尾报告必须显式标注 `subagent-unavailable` + 影响面）：

- 步骤 7b DRL 的 R1a（3 verifier）→ 降为主代理自走 3-lens 串行（factual → completeness → reusability 逐一自查，各用不同工具模式，每视角附工具证据）或 1 个可用 subagent 全视角。
- 步骤 7b R1b/R2 → 主代理以 refuted=true 心态自审 + 换工具/换目录视角重审，声明"独立审计降级为自审"。
- 步骤 4/6/7a 的 Grep spot-check / 4-step verify 不依赖 subagent，照常执行。
- 与 7b 既有「DRL 未安装降级」并列：二者独立触发，可同时存在（标注 `DRL downgraded (not installed)` + `subagent-unavailable`）。

> 与「Token 超额降级」区别：Token 降级是主动裁剪（等 user 拍板），本降级是平台能力缺失的强制降级，无需征求许可但必须显式声明。

执行 session 收尾 7 步流水线。每次 session 收尾或 sediment 工作落地后必走。

## neat-freak 边界声明（v1.1.0 吸收）

> neat-freak 边界：本 skill v1.1.0 仅吸收 neat-freak v3.0.0 的「6 面状态矩阵 + 记忆毕业判据 + 分阶段汇报模板」3 项机制。
> **不吸收**：双路径协议（保留 mem-wrap-up 固定 7 步骨架）/ 权限分级（适合 `USER.md` 声明而非 skill 内嵌）/ 平台路径速查（单平台运行不需要）。
> neat-freak 完整版留作外部参考（外部 skill 库归档，来源路径已脱敏；本仓库不依赖。如需升级到方案 A 完整蒸馏，从外部归档取）。

## 在三 skill 闭环中的位置

**闭环方向**：deep-review-loop（审查）→ mem-wrap-up（收尾）→ self-evolution（沉淀）

> 单一事实源声明（2026-08-24 护栏）：闭环方向/阶段位置/交接契约的**权威定义以 `agent-session-loop/SKILL.md` 为准**，本段与 deep-review-loop / self-evolution 各自只列本 skill 特有的触发与喂回条目；三处若与整合版冲突，以整合版为准。

**本 skill 位置**：收尾端（闭环中段）

**正向触发**（本 skill → 下游）:
- mem-wrap-up Step 5 sediment → 喂给 **self-evolution** dim 1 经验复用
- mem-wrap-up Step 2 audit findings → 喂给 **self-evolution** dim 5 问题预防
- mem-wrap-up Step 4 daily 日志（4 段 schema）→ 喂给 **self-evolution** dim 9 一次性工具沉淀

**反向触发**（上游 → 本 skill）:
- **deep-review-loop** 收敛后 → 触发本 skill Step 7 反向验证收尾本身
- **self-evolution** dim 11 发现收尾流程撞坑 → 升级本 skill 7 步协议


## 7 步（顺序固定，bridge_note 桥接 4 段 schema）

> **bridge_note**：本 skill 的 7 步流水线与步骤 4b 的 4 段 daily 日志 schema 之间的桥接声明——收尾汇报时需显式说明 7 步产出如何落进当日 daily 日志的 4 段结构（verification cost / throughput decoupling / ANED 3 指标 / session-end security scan），缺此声明视为收尾未闭环。

### 步骤 1: memory 健康检查
- **工具**：Bash 工具 + `memory_search` / `memory_get`
- **动作**：
  1. 列 memory 体量：Bash `wc -l ~/.qwenworkcn/awareness/main/MEMORY.md ~/.qwenworkcn/awareness/main/USER.md` + `ls ~/.qwenworkcn/awareness/main/memory/`
  2. `memory_search` 扫 MEMORY.md / USER.md 里的 P0/P1/P2 标记
  3. 统计 `memory/*.md` 日志文件数与总行数
- **输出**：metrics（P0/P1/P2 数量 + fileCount + line count）

### 步骤 2: memory audit（5 phase）
- **工具**：Grep 工具 + Read 工具 + Bash 工具
- **动作**：
  1. **frontmatter audit**：Grep ^---$ 验证每个 .md 文件有 frontmatter
  2. **dup audit**：Grep 工具跨文件查重复条目（e.g. 同一规则在 `USER.md` 和 `MEMORY.md` 双写）
  3. **empty audit**：Read 工具检查空文件 / 只有 frontmatter 的 stub
  4. **big-file audit**：Bash `find ~/.qwenworkcn/awareness/main -type f -size +50k` 找超大文件
  5. **broken-link audit**：Grep 工具 pattern file:///|\.md\) 找链接，逐个 Bash `test -e` 验证目标存在
- **输出**：5 phase 报告 + 6 面状态矩阵（见下）

#### 6 面状态矩阵（吸收自 neat-freak v3.0.0，知识治理扩展）

在 5 phase 文件结构审计之外，加审 6 个事实面的**内容一致性**。每面标状态：`verified-current` / `changed-and-verified` / `pending` / `out-of-scope` / `not-applicable`。

| 事实面 | 要回答的问题 | 常见证据 | 本 session 状态 |
|:-------|:-----------|:---------|:--------------|
| 代码 | 现在真正实现了什么？ | 当前分支、schema、配置、测试 | <状态> |
| 运行态 | 用户实际得到什么？ | deploy marker、服务、真实页面/API、控制台 | <状态> |
| 文档 | 人和下游看到的是不是现役答案？ | README、架构、接入、运维文档 | <状态> |
| 规则 | Agent 收到的约束是否同源、可执行、无死引用？ | AGENTS.md/工作手册/rules、override、hooks | <状态> |
| 记忆 | 快照是否仍准确且允许修改？ | USER.md/MEMORY.md/daily 日志、索引 | <状态> |
| 工作区 | 是否仍有未集成或未审计的残留？ | 会话残留文件、worktree、分支、临时库 | <状态> |

**判定原则**：
- 小项目不必硬凑六面：没有部署 → 运行态标 `not-applicable`；无记忆系统 → 记忆面标 `not-applicable`，不编造证据
- 版本库工作区干净（如项目有版本库）/ PR 已合并 / 测试通过 ≠ 「全部同步」，必须逐面验证
- 发布状态区分：draft / PR / merged / deployed / live verified / knowledge closed / cleaned
- 发现矛盾时记录 `source of truth → stale surfaces → intended action → verification`，不当场改则标 `pending`


### 步骤 3: memory 文件数 sync
- **工具**：Bash 工具 + Read 工具
- **动作**：
  1. Bash 统计实际 memory 文件数：`find ~/.qwenworkcn/awareness/main -type f -name "*.md" | wc -l`
  2. 若 MEMORY.md / 交接文档声明了文件数，Read 工具读其头部声明
  3. 对比实际 vs 声明，drift > 5% 触发警告
- **输出**：实际 total vs 声明 fileCount 漂移报告
### 步骤 4: 项目层文档同步 Grep spot-check + 当日 daily 日志追加 4 段 schema（bridge_note 桥接）

#### 4a: 项目层文档同步 Grep spot-check（E1 升级版铁律·2026-07-26 W083/W084/W085 3/3 证据毕业加入）

> **触发条件**：本 session 涉及版本 bump / W### 推进（如 v2.0.X W###），且 prior session summary 或本 session 主代理声明"项目层文档同步已落地"
> **根因（5Why）**：prior session Edit 工具成功 → prior session 基于 Edit 返回值判断"已落地" → 但 Edit 工具可能因 old_string 不匹配静默失败，或并行 Edit 竞态导致前序 Edit 丢失（`USER.md`「并行 Edit 竞态问题」条目），或 Edit 后未 Grep 验证 → prior session 报告"已落地"但实际文件未修改 → 本 session 信任 prior session 报告 → 误判修复已落地（**E1 升级版铁律**：不信任 prior session 的“已落地”声明）
> **铁律**：Grep spot-check 文件内容，验证版本号 + W ID 在当前工作区「治理层文档清单」中每个文件的实际出现，**不信任 prior session 的"已落地"声明**

- **工具**：Grep 工具
- **验证清单 = 当前工作区「治理层文档」，运行时现场枚举，不预置任何具体项目路径**（本文件全局通用，服务所有项目；项目专有清单留在各项目自身仓库副本，不进全局）：
  1. **优先读登记**：若项目在 `AGENTS.md` / README 文档索引 / 仓库内 skills 适配表中显式登记了自己的治理文档清单，据此清单校验；
  2. **否则现场枚举**：`ls` 项目根 + `docs/`（或等效结构），按文件名模式识别治理层文档——项目说明（`README*` / `*项目说明*`）、目录结构（`STRUCTURE*`）、变更日志（`CHANGELOG*`）、跨 session 交接（`*交接*`）、设计方案（`DESIGN*`）、迭代路线（`ROADMAP*`）、反向索引（`*index*`）等**实际存在者**，取命中集合为本 session 清单；
  3. **降级**：项目若无多文档同步约定（治理层文档 < 2 或均为单文件），本步降级为"仅校验本次实际改动过的文档"，**不得对不存在的文件报缺失**；
  4. **留痕**：收尾报告须标注「清单来源 = 登记引用 / 现场枚举 / 降级」三选一 + 命中文件名，供人工复核。

- **Grep spot-check 协议**：
  1. **Grep "v2.0.X"**（替换为当前版本号）：每个文件至少 1 处匹配，且应出现在头部"当前版本"段或对应新版本段（非历史变更日志段）
  2. **Grep "W###"**（替换为当前 W ID）：每个文件至少 1 处匹配
  3. **历史 vs 现役区分**（按 `USER.md` E2 铁律）：CHANGELOG 历史段 / STRUCTURE 版本史行保留旧值；本次清单中代表"当前版本"的文件（如 README 头部 / STRUCTURE 表格 / 交接文档）当前版本段必须更新

- **判据**：
  - 任一文件 v2.0.X / W### 命中数 < 1 → **P1 假收敛**，立即重新 Edit 修复
  - 历史段误改 → **E2 铁律违规**，回滚
- **输出**：清单内各文件 Grep spot-check 报告（每个文件的 v2.0.X 命中数 + W### 命中数 + 历史段是否误改）
- **降级条件**：无版本 bump / 无 W### 推进的 session（如纯调试 session）→ 4a 标 `not-applicable`，直接走 4b

#### 4b: 当日 daily 日志追加 4 段 schema
- **工具**：`memory` MCP 工具 target=`daily`（QwenWork 记忆文件不允许直接 Write/Edit 覆盖写入）
- **路径**：`~/.qwenworkcn/awareness/main/memory/<YYYYMMDD>.md`（天然按日期分文件；条目带 `[项目名]` 前缀）
- **4 段 schema**（必含）：
  1. **verification cost**：本 session 实证了多少 verification command（Grep/Read/Bash 调用计数）
  2. **throughput decoupling**：per-dim decision 跟 user final decision 分离记录（我建议 vs user 选）
  3. **ANED 3 指标**：actual vs nominal vs estimated delta（任务实际耗时 vs 名义 vs 估算差值）
  4. **session-end security scan**：4+1 pattern grep（敏感信息 / 密钥 / token / 内部 URL / PII）
- **必含字段**：date / session_id / milestones / retro_link
- **Caveat**：如工作流已 sediment，不强制 Bash → Write discipline

### 步骤 5: heuristic sediment -> memory 文件
- **工具**：`memory_search` / `memory_get`（或 Read 记忆根文件）取证 + `memory` 工具 target=`user`/`memory`/`daily` 写入（`MEMORY.md` / `USER.md` 禁止直接 Edit/Write）
- **写入协议（记忆写入协议铁律 1-3，2026-07-30 建立，适用于 `USER.md` / `MEMORY.md`）**：
  - **Read-before-Edit**：修改 `USER.md` / `MEMORY.md` 前必须先取回当前实际内容（`memory_get` 或 Read，不信任 cache），基于实际内容构造新值
  - **Grep-verify-after-Edit**：写入后必须经 `memory_search` / Grep 记忆根文件验证新值落地 + 旧值消失
  - **Retry-on-fail**：验证失败时重新取回 + 重写（最多 3 次），3 次仍失败放弃并记录到当日 daily 日志
  - **案例不写入 `USER.md`**：历史案例归档到当日 daily 日志复盘段（稳定后并入 `MEMORY.md`），`USER.md` 只放 active 规则 + 指针
- **动作**：
  1. 提炼本 session 的复利经验（5Why ≥3 层）
  2. 判断归属：用户级偏好 → `USER.md`（target=`user`）；项目级规则 → `MEMORY.md` `[项目名]` 前缀条目（target=`memory`）；近期 topic → 当日 daily 日志（target=`daily`）
  3. **写入前先取回目标当前内容**（`USER.md` 必须执行，`MEMORY.md` 同理推荐）
  4. 经 `memory` 工具追加到对应目标末尾（保留编号接续，e.g.「复利经验 #N+1」）
  5. **写入后 Grep / `memory_search` 验证新值落地**（铁律 2），失败则 Retry（铁律 3）
  6. 如当日 daily 日志已有复盘段（或项目内有复盘文档），同步追加
- **输出**：sediment 记录（编号 + 标题 + 5Why 链 + 与已有经验互补关系）
- **记忆毕业判据（吸收自 neat-freak v3.0.0）**：
  - **何时毕业到 docs/规则层**：满足以下任一即从 memory 升级到权威文档
    1. 讲的是稳定机制（非一次性场景）
    2. 同一教训已反复出现（≥3 次）
    3. 接手者也必须知道（影响下次 session 恢复）
  - **毕业后处置（W516 强化：上移检查子步骤）**：把结论并入项目公共载体后，memory 位置缩成指针或交给生成管线整合，**不复制成第二处真相**；具体按「上移映射表」落到项目公共载体并**强制登记交接文档「三、方法论沉淀」**（W### + 经验名 + 简述 + 复现计数器），杜绝"上移了但项目内查不到/不知情"。
  - **上移映射表（按经验类型选载体，防多 Agent 重复犯错的核心机制）**：
    - 规则/铁律/工具链坑 → `AGENTS.md` §4.3（工具链要点）或 §6（铁律），就地并入并全篇去重
    - 批次方法论/复利经验 → `交接文档.md`「三、方法论沉淀」（每轮 W 编号完成时登记，格式 W### + 经验名 + 简述 + 复现计数器）
    - 深度篇（诊断 SOP / 复盘根因）→ `docs/10-方法论沉淀/`（并在其 README 登记）
    - 流程/步骤 → `skills/<skill>/SKILL.md`（改后从仓库副本同步到全局 master，同步后 diff 校验）
    - 一次性工具 → `scripts/_*.py` 或永久化 `scripts/*.py`（视复现频次）
  - **不毕业的情况**：一次性事故、个人偏好、未稳定的探索性结论 → 保留在 memory，不动
  - **判据应用**：Step 5 sediment 时对每条经验先过毕业判据，符合则走"毕业路径"（同步到项目载体 + 登记交接文档「三」），不符合走"普通 sediment 路径"（追加到 memory）

### 步骤 6: 4-step verify（E92 范式）
- **工具**：Grep 工具 + Read 工具 + Bash 工具
- **4 步**（治本 shell hang / 文件缺失）：
  1. **file exists**：Bash `test -e <FILE>` 验每个声称写入的文件
  2. **content count**：Grep 工具 output_mode=count 验关键内容命中
  3. **link target**：Bash `readlink <LINK>` 验软链
  4. **wc -l**：Bash `wc -l < <FILE>` 验行数
- **输出**：P0=0 P1=0、P2 ≤ N_max（N_max 按项目阶段：比赛级 0 / 生产 3 / 原型 10，对齐 deep-review-loop 层 1 P2 残留规则；不写 OK / 完成，列数据 + 实证）

### 步骤 7: memory 层同步 Grep spot-check + deep-review-loop（联动已蒸馏 skill）

#### 7a: memory 层同步 Grep spot-check（E1 升级版铁律·2026-07-26 W083/W084/W085 3/3 证据毕业加入）

> **触发条件**：本 session 涉及 W### 推进，且 prior session summary 或本 session 主代理声明"memory 文件已更新"（appended 复盘分析 / 更新近期 topic / 追加收尾 4 段日志）
> **根因（5Why）**：与 4a 同源——prior session Edit 工具成功 ≠ memory 文件内容已修改（**3/3 证据毕业**：W083/W084/W085 连续三次 memory 层假收敛，prior session 报告"已更新 memory"但实际当日 daily 日志的收尾段 / topic 段 / 复盘段三处 W### 全部缺失）
> **铁律**：Grep spot-check memory 文件内容，验证 W### 在三件套的实际出现，**不信任 prior session 的"已更新 memory"声明**

- **工具**：Grep 工具
- **3 处 memory 落点**（验证清单）：
  1. 当日 daily 日志收尾段（`~/.qwenworkcn/awareness/main/memory/<YYYYMMDD>.md`，4 段 schema）
  2. 当日 daily 日志 topic 段（近期 topic 条目）
  3. 复盘段/复盘文档（当日 daily 日志复盘段，或项目内复盘文档）

- **Grep spot-check 协议**：
  1. **Grep "W###"**：每处至少 1 处匹配（收尾段应有完整 4 段 schema，topic 段应有 topic_summary_time 行，复盘段应含 dim 1/5/9/11 四段）
  2. **Grep "session_id"**：每个文件至少 1 处匹配（验证 session_id 字段存在）
  3. **Grep "milestones"**：daily 日志收尾段 应有 milestones 字段
  4. **Grep "dim 1|dim 5|dim 9|dim 11"**：daily 日志复盘段 应有 4 维度全段（self-evolution 模式 A 简化执行）

- **判据**：
  - 任一处 W### 命中数 < 1 → **P1 memory 层假收敛**，立即重新补齐（daily 日志经 `memory` 工具写入）
  - W### 命中但 dim 1/5/9/11 段缺失 → **P2 retro 段不完整**，立即补齐
- **输出**：3 处落点 Grep spot-check 报告（每处的 W### 命中数 + dim 段命中数 + 字段完整性）
- **降级条件**（按 `USER.md` E3 规则）：memory 文件审查范围窄可降级为主代理直接 spot-check（不派 subagent），但 spot-check 必执行不可省略

#### 7b: DRL 5 轮闭环
- **工具**：Skill 工具调用 deep-review-loop（已安装时），或 Read `skills/deep-review-loop/SKILL.md`（仓库版，未安装但可获取文档时）手动执行
- **5 轮**：
  - **R0**：surface check（file size + verdict 字眼 grep + expected hits 必现 + 项目阶段判定 → N_max）
  - **R1a**：3 独立 verifier 交叉验证（3 个 Agent 工具子代理并发，factual / completeness / reusability 3-lens）
  - **R1b**：对抗性 subagent 审查（1 个 Agent 工具子代理，default refuted=true + class-level scope + **严重度门槛**，过拟合防护层 4）
  - **R2**：独立审计 + self-revision（1 个 Agent 工具子代理，NOT inline + **边际收益 gate**，过拟合防护层 2）
  - **R3**：残余风险确认 + N residual risk（≥3）+ 收敛曲线 + **过拟合警报**（层 3，震荡/回归率触发 STOP）
- **输出**：5 轮闭环报告 + 收敛曲线 + ≥3 residual risk
- **未安装 deep-review-loop 时**（Skill 工具调用失败 = skill 未安装）：Step 7b 降级为精简审查（R0 表面检查 + 1 独立 subagent 审查 + R3 ≥3 residual risk + 收敛曲线），收尾报告显式标注 `DRL downgraded (deep-review-loop not installed)`；如需完整 5 轮，提示用户安装 deep-review-loop 后重跑。**降级不是跳过**——精简审查必须执行，不允许静默省略（对齐「裁剪必须显式标注」原则）
- **4 层过拟合防护继承声明**：本 skill Step 7 调用 DRL 时，自动继承 DRL v1.3.1 的 4 层防护（层 1 P2 残留 N / 层 2 边际收益 gate / 层 3 过拟合警报含 v1.3.1 增强·区分持平/反弹+严重度分层+窗口 4 轮+被动验证 / 层 4 严重度门槛）。细节以 DRL SKILL.md 当前版本为准（已安装时直接调用；未安装时按上方降级声明执行），本 skill 不重复定义
- **R1a 硬性要求继承（v1.2.0 新增）**：本 skill Step 7 调用 DRL 时，R1a subagent prompt 必须包含 DRL v1.3.1 的 7 条硬性要求声明（verifier 必须附工具调用证据 / 目录存在性声明必须附目录列举（Bash `ls`）/ 文件存在性声明必须附 Read/目录列举 / 路径声明必须附 Read / 0 finding 也要附证据 / Subagent prompt 必含此硬性要求 / 违反处置）。subagent 无文档访问权限，不可仅引用 DRL SKILL.md，必须 inline 完整声明
- **R1b 硬性要求继承（v1.3.1 新增）**：本 skill Step 7 调用 DRL 时，R1b subagent prompt 必须包含 DRL v1.3.1 的 R1b 硬性要求声明（R1b finding 必须附工具调用证据 / R1b 0 finding 也必须附证据 / R1b class-level enumeration 必须列出 ALL affected files 清单 / R1b 严重度降级必须附依据 / 违反处置）。与 R1a 硬性要求对齐，subagent 无文档访问权限，必须 inline 完整声明
- **R1b 反模式清单继承（v1.3.1 新增）**：本 skill Step 7 调用 DRL 时，R1b subagent prompt 必须包含 DRL v1.3.1 的 7 项反模式清单（silent skip / 正例 bias / 0 finding 滥用 / 严重度降级 / class-level 偷懒 / residual 敷衍 / 工具证据缺失），subagent 必须自检是否触发任一反模式

## 触发条件
- 用户说「收尾」/「wrap up」/「session 收尾」
- 用户说「继续」但工作流已 sediment（context-window-aware session）
- 主动判断：session 已跑 30+ 轮 / token 接近上限 / 重大里程碑达成
- 怀疑 session 不完整收尾（e.g. 修复后未 verify、sediment 未沉淀）

## Verdict 字眼合规自检
- 全文 Grep 禁词：完成|PASS|12/12|闭环|OK|没问题|looks good
- 必含对抗性 verify（步骤 7 R1b，default refuted=true）
- 必含 5Why ≥3 层（写入 sediment 段时触发）
- 历史 log 文件例外（步骤 4 daily 日志收尾段引用过往 verdict 不算违规）

## Failure handling
- 任一步骤失败 → 不继续下一步，stderr 报告
- Agent 工具子代理 idle fallback：撞 NEEDS_CONTEXT ≥3 走 fallback prompt（缩小 scope + 给具体 file:line）
- Token 超额（步骤 7 R1a 派 3 subagent）→ abort 走 3 选 1：
  1. 降级为 1 subagent（牺牲 coverage）
  2. 分批派（先 factual，再 completeness + reusability）
  3. 等 user 拍板（明确放弃 R1a 多视角）
## Residual Risk 协议（引用 deep-review-loop）

本 skill Step 7 联动 deep-review-loop 时，residual risk 由 DRL R3 产出，不重复定义。三类 residual risk（L5 subagent 盲点 / L1 sample-time-point / L3 跨 session）详见 `skills/deep-review-loop/SKILL.md`（仓库版）§5 R3。

## Related（QwenWork 原生路径）
- **deep-review-loop skill（仓库版）**：`skills/deep-review-loop/SKILL.md`（步骤 7 联动）
- **agent-session-loop（仓库版）**：`skills/agent-session-loop/SKILL.md`（三阶段整合流水线入口）
- **USER.md**（`memory` target=`user`）：步骤 5 sediment 用户级偏好
- **MEMORY.md**（`memory` target=`memory`，条目带 `[项目名]` 前缀）：步骤 5 sediment 项目级规则
- **当日 daily 日志**（`memory` target=`daily`，`~/.qwenworkcn/awareness/main/memory/<YYYYMMDD>.md`）：步骤 4b/5 收尾 4 段 schema、近期 topic、复利经验条目
- **复盘段/复盘文档**：当日 daily 日志复盘段或项目内复盘文档（如存在，步骤 5 复利经验同步）

> QwenWork 记忆不分项目子目录：跨项目区分一律用条目内 `[项目名]` 前缀（如 `[GateKeeper]` / `[xiyouji]`），不派生项目子目录名。

## 分阶段汇报模板（吸收自 neat-freak v3.0.0）

session 收尾完成后按以下 4 段模板输出，只列有行动价值的内容：

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

**强制要求**：
- 必须明确列出 `pending`、`out-of-scope` 和未消除的 warning
- 不能用「保证干净」掩盖它们
- 与 verdict 字眼禁令互补：本模板管"汇报结构"，verdict 禁令管"用词合规"
- 体量超过 platform budget 70% 时才报告读数

## Self-Disclosure
- 0 verdict 字眼（完成 / PASS / 12/12 / 闭环 / OK / 没问题 / looks good）
- ≥3 residual risk（per 步骤 7b R3 协议）
- bridge_note 声明（7 步流水线 vs 4 段 daily 日志 schema 桥接）
- 与 deep-review-loop skill 联动声明（步骤 7b 不重复 5 轮细节，引用已蒸馏 skill）
- **E1 升级版 spot-check 已执行**（4a 项目层 + 7a memory 层，2026-07-26 W083/W084/W085 3/3 证据毕业加入）

## Reference
- **外部 vault 蒸馏来源（路径已脱敏）**：由外部记忆库/skill 库蒸馏而来，蒸馏原则见下条；原 user 训诫（DRL 真循环铁律 2026-07-12）现已常驻 `USER.md`。
- **deep-review-loop skill（已蒸馏，仓库版）**：`skills/deep-review-loop/SKILL.md`
- **蒸馏原则**：剥离原脚本 hook（bash/Python/Node hooks）+ 原目录结构 + 原规则术语引用 + 原笔记链接格式；保留 7 步骨架 + 4 段 schema + verdict 禁词 + Failure handling + residual risk 协议；嫁接 QwenWork 工具映射 + deep-review-loop 联动
- **位置**：本 skill 的 master 副本位于 `~/.qwenworkcn/skills/mem-wrap-up/SKILL.md`；仓库归档副本位于 `D:\1\QwenWork\skills\mem-wrap-up\`
