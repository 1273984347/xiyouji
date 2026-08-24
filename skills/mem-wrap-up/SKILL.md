---
name: mem-wrap-up
description: Enforces 7-step session wrap-up with memory audit, 6-face knowledge governance, and DRL. Invoke at session end, when user says "wrap up/收尾/继续/洁癖", or when docs and code mismatch.
metadata:
  author: distilled-from-claude-code-vault
  version: "1.1.0-trae-distilled-with-knowledge-governance"
  source: C:\Users\12739\.claude\skills\mem-wrap-up\SKILL.md (2026-06-24, 4488 bytes)
  bridge_note: "7 步 (skill 流水线) vs 4 段 schema (work-log append 格式) 桥接 — 步骤 4 work-log 追加按 4 段 schema 形式"
---

# mem-wrap-up Skill（TRAE 蒸馏版）

> 本 skill 由 Claude Code vault 版蒸馏而来：剥离 bash 脚本 / Python hooks / Node hooks / vault 路径 / H-rules 术语 / CLAUDE.md §6.1 / Obsidian wiki-link，保留 7 步流水线骨架 + 4 段 work-log schema + verdict 禁词合规 + Failure handling + residual risk 协议。Step 7 联动 deep-review-loop skill（已蒸馏）。

**Announce at start:** "I'm using the mem-wrap-up skill to run the 7-step session wrap-up pipeline."

## 平台适配（仓库版 2026-08-19 治理）

- `<memory_root>`：agent 记忆根目录占位符（TRAE = `c:\Users\12739\.trae-cn\memory`；其他平台按自身约定，与本仓库 [agent-session-loop](../agent-session-loop/SKILL.md) 的 memory 路径约定一致）。
- `<project-slug>` / `<YYYYMMDD>` / `<date>`：按当前 workspace 映射的项目记忆目录与日期目录。
- 工具映射：`RunCommand` → 终端命令（PowerShell / `shell_command`）；`Task subagent` → 平台子代理机制；`Grep/Read` → 文件检索与读取工具（`rg` / `Get-Content`）。
- 步骤 4a 的「6 个项目层文件」为本仓库 xiyouji 六文档清单；其他项目按自身文档清单替换。
- 文末 Reference 中的 `C:\Users\12739\...` / `d:\1\archive\...` 仅为来源溯源路径，不是运行路径。

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
> **不吸收**：双路径协议（保留 mem-wrap-up 固定 7 步骨架）/ 权限分级（适合 user_profile 声明而非 skill 内嵌）/ 平台路径速查（TRAE 单平台不需要）。
> neat-freak 完整版留作参考：`d:\1\archive\khazix-skills\neat-freak\SKILL.md`（原机归档路径，仅原机可用；本仓库不依赖。如需升级到方案 A 完整蒸馏，从此路径取；归档位置 2026-07-21 确定）。

## 在三 skill 闭环中的位置

**闭环方向**：deep-review-loop（审查）→ mem-wrap-up（收尾）→ self-evolution（沉淀）

> 单一事实源声明（2026-08-24 护栏）：闭环方向/阶段位置/交接契约的**权威定义以 `agent-session-loop/SKILL.md` 为准**，本段与 deep-review-loop / self-evolution 各自只列本 skill 特有的触发与喂回条目；三处若与整合版冲突，以整合版为准。

**本 skill 位置**：收尾端（闭环中段）

**正向触发**（本 skill → 下游）:
- mem-wrap-up Step 5 sediment → 喂给 **self-evolution** dim 1 经验复用
- mem-wrap-up Step 2 audit findings → 喂给 **self-evolution** dim 5 问题预防
- mem-wrap-up Step 4 work-log → 喂给 **self-evolution** dim 9 一次性工具沉淀

**反向触发**（上游 → 本 skill）:
- **deep-review-loop** 收敛后 → 触发本 skill Step 7 反向验证收尾本身
- **self-evolution** dim 11 发现收尾流程撞坑 → 升级本 skill 7 步协议


## 7 步（顺序固定，bridge_note 桥接 4 段 schema）

> **bridge_note**：本 skill 的 7 步流水线与步骤 4b 的 4 段 work-log schema 之间的桥接声明——收尾汇报时需显式说明 7 步产出如何落进 work-log 的 4 段结构（verification cost / throughput decoupling / ANED 3 指标 / session-end security scan），缺此声明视为收尾未闭环。

### 步骤 1: memory 健康检查
- **工具**：RunCommand（PowerShell）+ Grep 工具
- **动作**：
  1. 列 `<memory_root>/` 目录树大小：Get-ChildItem -Recurse | Measure-Object -Line
  2. Grep 工具扫 user_profile.md / 各 project_memory.md 的 P0/P1/P2 标记
  3. 统计 session_memory_*.jsonl 文件数 + 总行数
- **输出**：metrics（P0/P1/P2 数量 + fileCount + line count）

### 步骤 2: memory audit（5 phase）
- **工具**：Grep 工具 + Read 工具 + RunCommand
- **动作**：
  1. **frontmatter audit**：Grep ^---$ 验证每个 .md 文件有 frontmatter
  2. **dup audit**：Grep 工具跨文件查重复条目（e.g. 同一规则在 user_profile 和 project_memory 双写）
  3. **empty audit**：Read 工具检查空文件 / 只有 frontmatter 的 stub
  4. **big-file audit**：RunCommand Get-ChildItem -Recurse | Where-Object {$_.Length -gt 50KB} 找超大文件
  5. **broken-link audit**：Grep 工具 pattern file:///|\.md\) 找链接，逐个 Test-Path 验证目标存在
- **输出**：5 phase 报告 + 6 面状态矩阵（见下）

#### 6 面状态矩阵（吸收自 neat-freak v3.0.0，知识治理扩展）

在 5 phase 文件结构审计之外，加审 6 个事实面的**内容一致性**。每面标状态：`verified-current` / `changed-and-verified` / `pending` / `out-of-scope` / `not-applicable`。

| 事实面 | 要回答的问题 | 常见证据 | 本 session 状态 |
|:-------|:-----------|:---------|:--------------|
| 代码 | 现在真正实现了什么？ | 当前分支、schema、配置、测试 | <状态> |
| 运行态 | 用户实际得到什么？ | deploy marker、服务、真实页面/API、控制台 | <状态> |
| 文档 | 人和下游看到的是不是现役答案？ | README、架构、接入、运维文档 | <状态> |
| 规则 | Agent 收到的约束是否同源、可执行、无死引用？ | CLAUDE.md/AGENTS.md/rules、override、hooks | <状态> |
| 记忆 | 快照是否仍准确且允许修改？ | user_profile/project_memory/topics、索引 | <状态> |
| 工作区 | 是否仍有未集成或未审计的残留？ | 会话残留文件、worktree、分支、临时库 | <状态> |

**判定原则**：
- 小项目不必硬凑六面：没有部署 → 运行态标 `not-applicable`；无记忆系统 → 记忆面标 `not-applicable`，不编造证据
- `git status` 干净 / PR 已合并 / 测试通过 ≠ 「全部同步」，必须逐面验证
- 发布状态区分：draft / PR / merged / deployed / live verified / knowledge closed / cleaned
- 发现矛盾时记录 `source of truth → stale surfaces → intended action → verification`，不当场改则标 `pending`


### 步骤 3: project_memory.md fileCount sync
- **工具**：RunCommand + Grep 工具 + Read 工具
- **动作**：
  1. RunCommand 统计实际 memory 文件数：Get-ChildItem "<memory_root>" -Recurse -File | Measure-Object
  2. Read 工具读 project_memory.md 头部 frontmatter（如有 fileCount 声明）
  3. 对比实际 vs 声明，drift > 5% 触发警告
- **输出**：实际 total vs 声明 fileCount 漂移报告
### 步骤 4: 项目层文档同步 Grep spot-check + work-log 追加 4 段 schema（bridge_note 桥接）

#### 4a: 项目层文档同步 Grep spot-check（E1 升级版铁律·2026-07-26 W083/W084/W085 3/3 证据毕业加入）

> **触发条件**：本 session 涉及版本 bump / W### 推进（如 v2.0.X W###），且 prior session summary 或本 session 主代理声明"6 文件文档同步已落地"
> **根因（5Why）**：prior session Edit 工具成功 → prior session 基于 Edit 返回值判断"已落地" → 但 Edit 工具可能因 old_string 不匹配静默失败，或并行 Edit 竞态导致前序 Edit 丢失（user_profile "并行 Edit 竞态问题"），或 Edit 后未 Grep 验证 → prior session 报告"已落地"但实际文件未修改 → 本 session 信任 prior session 报告 → 误判修复已落地（**E1 升级版铁律**，与 E1 跨 session git tracked 验证互补）
> **铁律**：Grep spot-check 文件内容，验证版本号 + W ID 在 6 个项目层文件的实际出现，**不信任 prior session 的"已落地"声明**

- **工具**：Grep 工具 + RunCommand（git ls-files）
- **6 个项目层文件**（验证清单）：
  1. README.md（项目根说明）
  2. STRUCTURE.md（目录结构）
  3. CHANGELOG.md（变更日志）
  4. docs/00-导读/项目说明.md（项目状态）
  5. 交接文档.md（跨 session 交接）
  6. scripts/output/file-index.md（反向索引）

- **Grep spot-check 协议**：
  1. **Grep "v2.0.X"**（替换为当前版本号）：每个文件至少 1 处匹配，且应出现在头部"当前版本"段或对应新版本段（非历史变更日志段）
  2. **Grep "W###"**（替换为当前 W ID）：每个文件至少 1 处匹配
  3. **历史 vs 现役区分**（按 user_profile E2 铁律）：CHANGELOG v0.X 历史段 / STRUCTURE 版本史行保留旧值；README 头部 / STRUCTURE 表格 / 项目说明.md / 交接文档.md 当前版本段必须更新
  4. **E1 跨 session git tracked 验证（user_profile E1 铁律）**：RunCommand `git ls-files <file>` 验证每个声明同步的文件实际被 git tracked（Edit 成功 ≠ git tracked）

- **判据**：
  - 任一文件 v2.0.X / W### 命中数 < 1 → **P1 假收敛**，立即重新 Edit 修复
  - 任一文件未被 git tracked → **E1 铁律复现**，立即 `git add`
  - 历史段误改 → **E2 铁律违规**，回滚
- **输出**：6 文件 Grep spot-check 报告（每个文件的 v2.0.X 命中数 + W### 命中数 + tracked 状态 + 历史段是否误改）
- **降级条件**：无版本 bump / 无 W### 推进的 session（如纯调试 session）→ 4a 标 `not-applicable`，直接走 4b

#### 4b: work-log 追加 4 段 schema
- **工具**：Write 工具（追加到 `<memory_root>/projects/<project-slug>/<YYYYMMDD>/work-log.md`，无则新建）
- **路径**：`<memory_root>/projects/<project-slug>/<YYYYMMDD>/work-log.md`（按日期分目录）
- **4 段 schema**（必含）：
  1. **verification cost**：本 session 实证了多少 verification command（Grep/Read/RunCommand 调用计数）
  2. **throughput decoupling**：per-dim decision 跟 user final decision 分离记录（我建议 vs user 选）
  3. **ANED 3 指标**：actual vs nominal vs estimated delta（任务实际耗时 vs 名义 vs 估算差值）
  4. **session-end security scan**：4+1 pattern grep（敏感信息 / 密钥 / token / 内部 URL / PII）
- **必含字段**：date / session_id / milestones / retro_link
- **Caveat**：如工作流已 sediment，不强制 Bash → Write discipline

### 步骤 5: heuristic sediment -> memory 文件
- **工具**：Read 工具 + Edit 工具（追加到 user_profile.md 或 project_memory.md 对应章节）
- **写入协议（user_profile.md 写入协议铁律 1-3，2026-07-30 建立）**：
  - **Read-before-Edit**：Edit user_profile.md 前必须 Read 当前实际内容（不信任 cache），基于实际内容计算 old_string
  - **Grep-verify-after-Edit**：Edit 后必须 Grep 验证新值落地 + 旧值消失
  - **Retry-on-fail**：Grep 验证失败时重新 Read + Edit（最多 3 次），3 次仍失败放弃并记录 session_memory
  - **案例不写入 user_profile.md**：历史案例归档 retrospective.md，user_profile.md 只放 active 规则 + 指针
- **动作**：
  1. 提炼本 session 的复利经验（5Why ≥3 层）
  2. 判断归属：用户级偏好 → user_profile.md；项目级规则 → project_memory.md；近期 topic → topics.md
  3. **Edit 前先 Read 目标文件当前内容**（user_profile.md 必须执行，project_memory.md 同理推荐）
  4. Edit 工具追加到对应文件末尾（保留编号接续，e.g.「复利经验 #N+1」）
  5. **Edit 后 Grep 验证新值落地**（铁律 2），失败则 Retry（铁律 3）
  6. 如有 retrospective 文档，同步追加到项目内 retrospective
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
    - 流程/步骤 → `skills/<skill>/SKILL.md`（改后跑 `scripts/sync_skills.py --sync` 仓库→全局）
    - 一次性工具 → `scripts/_*.py` 或永久化 `scripts/*.py`（视复现频次）
  - **不毕业的情况**：一次性事故、个人偏好、未稳定的探索性结论 → 保留在 memory，不动
  - **判据应用**：Step 5 sediment 时对每条经验先过毕业判据，符合则走"毕业路径"（同步到项目载体 + 登记交接文档「三」），不符合走"普通 sediment 路径"（追加到 memory）

### 步骤 6: 4-step verify（E92 范式）
- **工具**：Grep 工具 + Read 工具 + RunCommand
- **4 步**（治本 bash hang / 文件缺失）：
  1. **file exists**：RunCommand Test-Path <FILE> 验每个声称写入的文件
  2. **content count**：Grep 工具 output_mode=count 验关键内容命中
  3. **link target**：RunCommand Get-Item <LINK> | Select-Object Target 验软链
  4. **wc -l**：RunCommand (Get-Content <FILE>).Count 验行数
- **输出**：P0=0 P1=0、P2 ≤ N_max（N_max 按项目阶段：比赛级 0 / 生产 3 / 原型 10，对齐 deep-review-loop 层 1 P2 残留规则；不写 OK / 完成，列数据 + 实证）

### 步骤 7: memory 层同步 Grep spot-check + deep-review-loop（联动已蒸馏 skill）

#### 7a: memory 层同步 Grep spot-check（E1 升级版铁律·2026-07-26 W083/W084/W085 3/3 证据毕业加入）

> **触发条件**：本 session 涉及 W### 推进，且 prior session summary 或本 session 主代理声明"memory 文件已更新"（appended retrospective analysis / updated topics.md / appended work-log.md）
> **根因（5Why）**：与 4a 同源——prior session Edit 工具成功 ≠ memory 文件内容已修改（**3/3 证据毕业**：W083/W084/W085 连续三次 memory 层假收敛，prior session 报告"已更新 memory"但实际 work-log.md / topics.md / retrospective.md 三件套 W### 段全部缺失）
> **铁律**：Grep spot-check memory 文件内容，验证 W### 在三件套的实际出现，**不信任 prior session 的"已更新 memory"声明**

- **工具**：Grep 工具
- **3 个 memory 文件**（验证清单）：
  1. work-log.md（`<memory_root>/projects/<project-slug>/<YYYYMMDD>/work-log.md`）
  2. topics.md（`<memory_root>/projects/<project-slug>/<YYYYMMDD>/topics.md`）
  3. retrospective.md（项目内或 memory 层 retrospective 文档）

- **Grep spot-check 协议**：
  1. **Grep "W###"**：每个文件至少 1 处匹配（work-log.md 应有完整 4 段 schema 段，topics.md 应有 topic_summary_time 行，retrospective.md 应有 dim 1/5/9/11 四段）
  2. **Grep "session_id"**：每个文件至少 1 处匹配（验证 session_id 字段存在）
  3. **Grep "milestones"**：work-log.md 应有 milestones 字段
  4. **Grep "dim 1|dim 5|dim 9|dim 11"**：retrospective.md 应有 4 维度全段（self-evolution 模式 A 简化执行）

- **判据**：
  - 任一文件 W### 命中数 < 1 → **P1 memory 层假收敛**，立即重新 Edit 补齐
  - W### 命中但 dim 1/5/9/11 段缺失 → **P2 retro 段不完整**，立即补齐
- **输出**：3 memory 文件 Grep spot-check 报告（每个文件的 W### 命中数 + dim 段命中数 + 字段完整性）
- **降级条件**（按 user_profile E3 规则）：memory 文件审查范围窄可降级为主代理直接 spot-check（不派 subagent），但 spot-check 必执行不可省略

#### 7b: DRL 5 轮闭环
- **工具**：Skill 工具调用 deep-review-loop（已安装时），或 Read `skills/deep-review-loop/SKILL.md`（仓库版，未安装但可获取文档时）手动执行
- **5 轮**：
  - **R0**：surface check（file size + verdict 字眼 grep + expected hits 必现 + 项目阶段判定 → N_max）
  - **R1a**：3 独立 verifier 交叉验证（3 Task subagents parallel，factual / completeness / reusability 3-lens）
  - **R1b**：对抗性 subagent 审查（1 Task subagent，default refuted=true + class-level scope + **严重度门槛**，过拟合防护层 4）
  - **R2**：独立审计 + self-revision（1 Task subagent，NOT inline + **边际收益 gate**，过拟合防护层 2）
  - **R3**：残余风险确认 + N residual risk（≥3）+ 收敛曲线 + **过拟合警报**（层 3，震荡/回归率触发 STOP）
- **输出**：5 轮闭环报告 + 收敛曲线 + ≥3 residual risk
- **未安装 deep-review-loop 时**（Skill 工具调用失败 = skill 未安装）：Step 7b 降级为精简审查（R0 表面检查 + 1 独立 subagent 审查 + R3 ≥3 residual risk + 收敛曲线），收尾报告显式标注 `DRL downgraded (deep-review-loop not installed)`；如需完整 5 轮，提示用户安装 deep-review-loop 后重跑。**降级不是跳过**——精简审查必须执行，不允许静默省略（对齐「裁剪必须显式标注」原则）
- **4 层过拟合防护继承声明**：本 skill Step 7 调用 DRL 时，自动继承 DRL v1.3.1 的 4 层防护（层 1 P2 残留 N / 层 2 边际收益 gate / 层 3 过拟合警报含 v1.3.1 增强·区分持平/反弹+严重度分层+窗口 4 轮+被动验证 / 层 4 严重度门槛）。细节以 DRL SKILL.md 当前版本为准（已安装时直接调用；未安装时按上方降级声明执行），本 skill 不重复定义
- **R1a 硬性要求继承（v1.2.0 新增）**：本 skill Step 7 调用 DRL 时，R1a subagent prompt 必须包含 DRL v1.3.1 的 7 条硬性要求声明（verifier 必须附工具调用证据 / 目录存在性声明必须附 LS / 文件存在性声明必须附 Read/LS / 路径声明必须附 Read / 0 finding 也要附证据 / Subagent prompt 必含此硬性要求 / 违反处置）。subagent 无文档访问权限，不可仅引用 DRL SKILL.md，必须 inline 完整声明
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
- 历史 log 文件例外（步骤 4 work-log 引用过往 verdict 不算违规）

## Failure handling
- 任一步骤失败 → 不继续下一步，stderr 报告
- Task subagent idle fallback：撞 NEEDS_CONTEXT ≥3 走 fallback prompt（缩小 scope + 给具体 file:line）
- Token 超额（步骤 7 R1a 派 3 subagent）→ abort 走 3 选 1：
  1. 降级为 1 subagent（牺牲 coverage）
  2. 分批派（先 factual，再 completeness + reusability）
  3. 等 user 拍板（明确放弃 R1a 多视角）
## Residual Risk 协议（引用 deep-review-loop）

本 skill Step 7 联动 deep-review-loop 时，residual risk 由 DRL R3 产出，不重复定义。三类 residual risk（L5 subagent 盲点 / L1 sample-time-point / L3 跨 session）详见 `skills/deep-review-loop/SKILL.md`（仓库版）§5 R3。

## Related（TRAE 路径，非 vault wiki-link）
- **deep-review-loop skill（仓库版）**：`skills/deep-review-loop/SKILL.md`（步骤 7 联动）
- **agent-session-loop（仓库版）**：`skills/agent-session-loop/SKILL.md`（三阶段整合流水线入口）
- **user_profile**：`<memory_root>/user_profile.md`（步骤 5 sediment 用户级偏好）
- **project_memory**：`<memory_root>/projects/<project-slug>/project_memory.md`（步骤 5 sediment 项目级规则）
- **topics**：`<memory_root>/projects/<project-slug>/<YYYYMMDD>/topics.md`（步骤 5 sediment 近期 topic）
- **retrospective**：项目内 retrospective 文档（如存在，步骤 5 复利经验同步）

> <project-slug> 为当前 workspace 对应的 memory 项目目录名（e.g. -d-1、-d-1-Vannevar、-d-1-Anthropic）。执行时按当前 cwd 映射。

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
- bridge_note 声明（7 步流水线 vs 4 段 work-log schema 桥接）
- 与 deep-review-loop skill 联动声明（步骤 7b 不重复 5 轮细节，引用已蒸馏 skill）
- **E1 升级版 spot-check 已执行**（4a 项目层 + 7a memory 层，2026-07-26 W083/W084/W085 3/3 证据毕业加入）

## Reference
- **源 skill（原机溯源，非运行路径）**：C:\Users\12739\.claude\skills\mem-wrap-up\SKILL.md（2026-06-24, 4488 bytes）
- **deep-review-loop skill（已蒸馏，仓库版）**：`skills/deep-review-loop/SKILL.md`
- **user 训诫（原机溯源）**：c:\Users\12739\.trae-cn\memory\user_profile.md § DRL 真循环铁律（2026-07-12）
- **蒸馏原则**：剥离 bash/Python/Node hooks + vault 路径 + H-rules + CLAUDE.md §6.1 + Obsidian wiki-link；保留 7 步骨架 + 4 段 schema + verdict 禁词 + Failure handling + residual risk 协议；嫁接 TRAE 工具映射 + deep-review-loop 联动
- **位置**：本仓库 `skills/mem-wrap-up/SKILL.md`（仓库版，平台适配见文首）；TRAE 全局另有副本
