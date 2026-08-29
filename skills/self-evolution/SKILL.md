---
name: self-evolution
description: Runs retro after task completion. Quick mode = 3-question self-check. Full mode = 11-dimension deep analysis with knowledge upgrade. Invoke when user says "全面复盘/周汇总/retro/记住这个/capture/经验沉淀" or after task completion.
metadata:
  author: distilled-from-external-vault
  version: "1.2.0-qwenwork-native"
  source: 外部 vault 版原文件（来源路径已脱敏；v2.1.3，11-dimensions 模板已内联）
  templates_inlined: 11-dimensions-deep-retro.md, evolution-report.md, write-large-file-checklist.md
---

# self-evolution Skill（外部 vault 蒸馏版 · QwenWork）

> 本 skill 由外部记忆库/skill 库（vault）版蒸馏而来：剥离原脚本 hook（bash/Node/Python 脚本）/ 原目录结构 / 原规则术语引用 / 原经验捕获依赖 / 模板独立文件（11 维度模板已内联），保留双模式骨架 + 11 维度完整内容 + 5 件套 sync verify + 知识层升级 + 行动项分流 + verdict 禁词合规。

**Announce at start:** "I'm using the self-evolution skill to run retro (quick / full mode)."

## 运行平台：千问办公 QwenWork

1. 本 skill 运行于**千问办公（QwenWork）**；正文所有路径、工具、检索都按 QwenWork 原生写，不使用外部平台占位符。
2. 记忆根：`~/.qwenworkcn/awareness/main`（`MEMORY.md` 跨会话长期记忆 / `USER.md` 用户级偏好与铁律 / `memory/YYYY-MM-DD.md` 每日日志）。写入经 `memory` MCP 工具（target=`memory` / `user` / `daily`），检索经 `memory_search` / `memory_get`；`MEMORY.md` 与 `USER.md` **禁止直接 Edit/Write**。
3. 技能根：`~/.qwenworkcn/skills`；技能增改删用 `qwenwork_skill_manage`（action `create` / `patch` / `edit` / `delete`）。
4. 可用技能列表由会话 system-reminder 注入；调用某技能用 `Skill` 工具。
5. 工具映射：终端用 `Bash 工具`（PowerShell 语义可 `powershell.exe -Command "…"`；存在性/软链/行数/体量校验用 `test -e` / `readlink` / `wc -l < <FILE>` / `find -size +50k` / `ls -R`）；子代理用 `Agent 工具`（`subagent_type`：`general-purpose` / `Explore` / `Plan`，可并发 / 可后台）；文件读写 `Read` / `Write` / `Edit`，检索 `Grep` / `Glob`；记忆读写 `memory` / `memory_search` / `memory_get`。
6. 文件保护：删除一律进系统回收站（禁 `rm` / `del`）；改用户文件前先备份（Git 版本库内项目除外）。
7. QwenWork 项目不保证为 git 库；一致性校验一律走「治理层清单现场枚举 + Grep spot-check 现测」，不依赖版本库文件清单类校验。
8. 本 skill 主体不派子代理（详见「子代理不可用声明」）；与 deep-review-loop 联动时子代理经 `Agent 工具` 派发。

**记忆落点速查（正文各步骤引用）**

| 沉淀内容 | QwenWork 落点 | 写入方式 |
|:---|:---|:---|
| 用户级偏好与铁律 | `USER.md` | `memory` target=`user` |
| 项目级规则 / 长期经验 / 稳定速查 | `MEMORY.md`（条目带 `[项目名]` 前缀） | `memory` target=`memory` |
| 收尾 4 段日志 / 近期 topic / 当日经验记录 / 复盘报告 / Skill 缺口清单 | 当日 daily 日志 `memory/<YYYYMMDD>.md`（条目带 `[项目名]` 前缀） | `memory` target=`daily` |
| 稳定套路（pattern / heuristic 层） | `~/.qwenworkcn/skills/<name>/SKILL.md` | `qwenwork_skill_manage` 建/补 |
| policy 层规则 | `MEMORY.md` | **须人工确认后**并入 |

## 子代理不可用声明（2026-08-24 新增）

本 skill 的快速/全面两种模式的执行（3 问自检、11 维度分析、5 件套 verify、知识层升级）**均由主代理完成，不派 subagent**，因此子代理能力缺失不影响本 skill 主体流程。

仅当本 skill 与 deep-review-loop 联动（dim 5/9 消费 DRL 产出、dim 11 反向升级 DRL）时，DRL 侧的子代理不可用降级见 `deep-review-loop/SKILL.md`「子代理不可用降级」段，本 skill 不重复定义。

## 在三 skill 闭环中的位置

**闭环方向**：deep-review-loop（审查）→ mem-wrap-up（收尾）→ self-evolution（沉淀）

> 单一事实源声明（2026-08-24 护栏）：闭环方向/阶段位置/交接契约的**权威定义以 `agent-session-loop/SKILL.md` 为准**，本段与 deep-review-loop / mem-wrap-up 各自只列本 skill 特有的触发与喂回条目；三处若与整合版冲突，以整合版为准。

**本 skill 位置**：沉淀端（闭环末端，反向喂回 DRL）

**正向触发**（本 skill → 反向喂回）:
- dim 11 发现复盘流程撞坑 → 升级 **deep-review-loop** 协议（5 轮细节）
- dim 1/5/9 从 **deep-review-loop** residual risk + **mem-wrap-up** sediment/audit/daily 日志 提取经验

**反向触发**（上游 → 本 skill）:
- **deep-review-loop** R3 residual risk → 喂给 dim 5 问题预防（含 P2 残留经验：按 5Why 处理但标记"接受残留"，不强制升级）
- **deep-review-loop** R1b class-level findings → 喂给 dim 9 一次性工具沉淀（P3 由 DRL backlog 兜底，dim 9 不重复；P3 若属 class-level pattern 1 instance 则 DRL 升级为 P2 报告，dim 9 正常接收）
- **mem-wrap-up** Step 5 sediment → 喂给 dim 1 经验复用
- **mem-wrap-up** Step 2 audit findings → 喂给 dim 5 问题预防
- **mem-wrap-up** Step 4 daily 日志（4 段 schema）→ 喂给 dim 9 一次性工具沉淀

**P2/P3 跨 skill 语义统一（P2-8 修复）**:
- DRL P2 = 体验问题（记录但不强制修复，允许残留 N 条）= self-evolution P2 = 等用户确认（沿用 DRL 语义）
- DRL P3 = 不报（class-level instance 例外升级 P2）= self-evolution P3 = nice-to-have（只记录，沿用 DRL 语义）
- self-evolution 行动项 P0/P1/P2/P3 优先级与 DRL 收敛判定表对齐：P0/P1 必须降到 0，P2 允许残留 N，P3 不计入


## 两种模式

| 模式 | 触发 | 深度 | 输出 |
|:---|:---|:---|:---|
| **快速** | 任务完成时自动 | 3 问自检 | 当日 daily 日志经验段（+ Skill 缺口段） |
| **全面** | 手动触发 | 11 维度分析 | 当日 daily 日志复盘段 + 经验段（稳定项并入 MEMORY.md） |

---

## 模式 A：快速复盘（任务完成后自动执行）

每个任务完成时执行；若项目为 git 仓库，则在 commit 之前。

> **与整合版并用时**：若与 [agent-session-loop](../agent-session-loop/SKILL.md)（三阶段整合流水线）同仓/同环境使用，触发与裁剪遵循整合版的场景裁剪规则（如纯调试 session 可标 `not-applicable`）；独立调用时按本节执行。

### 触发条件
- 任务标记为 completed 时
- 提交前（如项目有版本库，则 commit 前）
- 不需要用户显式触发

### 执行步骤

**Step 1：3 问自检（必须回答，全否也要写出"全否"）**

```
① 有新发现？→ 方法/模式/工具首次使用或优化
② 踩了坑？→ 错误、根因、修复方案
③ 有 Skill 缺口？→ 本该用但没用的 Skill
```

**Step 2：根据答案决定动作**

| 答案 | 动作 |
|:---|:---|
| 全否 | 跳过，不写文件 |
| 有发现/踩坑/缺口 | 执行写入（见下方） |

**写入步骤**（直接执行，不需要调用其他 skill；格式与质量标准详见 [references/experience-capture-format.md](references/experience-capture-format.md)，激活本节时读取）：

1. 经 `memory` 工具 target=`daily` 追加到当日 daily 日志 `~/.qwenworkcn/awareness/main/memory/<date>.md`（条目带 `[项目名]` 前缀）：
```markdown
## [日期] — [任务名称] | **Tags:** [tag1, tag2]

### [新发现 / 踩坑 / Skill 缺口]
[具体内容]

### 根因（如果是踩坑）
[分析]

### 下次怎么做
[具体行动方案]
```

2. 如有明确规则的经验（稳定速查），经 `memory` 工具 target=`memory` 并入 `MEMORY.md` 的 `[项目名]` 速查条目：
```
[项目名] [编号] [关键词] — [一句话规则]
```

3. 如有 Skill 缺口，追加到当日 daily 日志的「Skill 缺口」清单段；同类缺口确认后经 `qwenwork_skill_manage` 建/补相应 skill：
```
| [Skill名] | [场景] | [为什么没用] |
```

**Step 3：模式升级检查**

如果同类问题在 daily 日志 / `MEMORY.md` 经验条目中出现 ≥3 次，触发升级：稳定套路经 `qwenwork_skill_manage` 并入相应 skill 的 SKILL.md（pattern / heuristic 层套路段）（本 step 负责）。

---
## 模式 B：全面复盘（手动触发）

说"全面复盘"、"跑一下验收"、"周汇总"、"复盘"、"retro"时执行。覆盖整个会话或一段时间的工作。

### 执行步骤

**Step 1：数据收集（分层读取，避免 token 爆炸）**

```
第一层：摘要（必须，~2k tokens）
□ 版本推进摘要：git log --oneline + git diff --stat（仅当项目为 git 仓库；否则改用当日 daily 日志里程碑段 + 本 session 改动清单）
□ 当日 daily 日志经验段尾部（最新条目）

第二层：按需读取（只在对应维度需要时读取）
□ 维度 1 需要 → Grep `MEMORY.md` 的 `[项目名]` 速查条目匹配本次关键词
□ 维度 2 需要 → 读取本次使用的 Skill 的 SKILL.md（只读 description）
□ 维度 3 需要 → Grep 历史 daily 日志「Skill 缺口」段匹配本次任务类型
□ 维度 5 需要 → `memory_search` 检索同类问题条目（daily 日志 + MEMORY.md）
□ 维度 7 需要 → 读取相应 skill 的 SKILL.md 套路段 / `MEMORY.md` pattern 条目

第三层：深度读取（只在发现异常时读取）
□ 某个经验条目需要详细分析 → 读取该条目完整内容
□ 某个 Skill 需要优化 → 读取完整 SKILL.md
```

**原则**：先读摘要，发现需要深入时再读全文。不要一次性把所有文件读入上下文。

**Step 2：11 维度分析**

按以下 11 个维度逐一分析，每个维度输出结论。完整模板见下方内联内容。

**11 维度清单**（dim 9 必走，不可跳过）：
1. 经验复用梳理 | 2. 技能优化评估 | 3. 未用技能审视 | 4. 场景沉淀识别 | 5. 问题与预防机制
6. 工作流优化方案 | 7. 问题总结与计划制定 | 8. 元认知反思 | 9. 一次性工具沉淀（必走）
10. 工具链 sub-protocol 反思（可选） | 11. 复盘过程中出现的问题（必走）

---

## 11 维度完整模板（内联）

### 维度 1：经验复用梳理

**输入**：当日 daily 日志经验段 + `MEMORY.md` `[项目名]` 速查条目
**分析**：
- 本次复用了哪些历史经验？（列出具体条目）
- 本次新增了哪些可复用经验？
- 哪些经验被反复使用？（≥3 次 → 考虑升级为 heuristic）
- 每条经验量化评分（见下方评分标准）

**经验量化评分标准**：

| 维度 | 权重 | 评分标准 |
|:---|:---:|:---|
| 普适性 | 0.4 | 1=仅限当前项目, 3=同类项目可用, 5=跨领域通用 |
| 可迁移性 | 0.4 | 1=需要大量修改, 3=小调整可用, 5=直接复用 |
| 预期效果 | 0.2 | 1=效果不明确, 3=有明显改善, 5=显著提升效率/质量 |

**综合得分** = 普适性×0.4 + 可迁移性×0.4 + 预期效果×0.2。得分 ≥4 → 标记"高价值经验"，重点沉淀。

**输出物**：《结构化经验复用清单》

| ID | 经验描述 | 来源项目 | 适用场景 | 复用方法 | 预期效果 | 评分 | 等级 |
|:---|:---|:---|:---|:---|:---|:---:|:---|
| E1 | [描述] | [项目] | [场景] | [步骤] | [效果] | 4.2 | 高价值 |

### 维度 2：技能优化评估

**输入**：本次使用的 Skills 列表
**分析**：每个 Skill 的多维度评估 + 识别 3-5 项"优先提升技能" + 制定提升方案

**技能评估矩阵**：

| Skill | 掌握水平 | 应用频率 | 质量影响 | 优化潜力 | 综合优先级 |
|:---|:---:|:---:|:---:|:---:|:---:|
| [Skill1] | 高/中/低 | 高/中/低 | 高/中/低 | 高/中/低 | [计算] |

综合优先级判定：
- 高影响 + 低掌握 = 最高优先
- 高频率 + 高优化潜力 = 高优先
- 低影响 + 低频率 = 不优化

**技能提升计划表**（对优先提升技能）：

| Skill | 当前水平 | 目标水平 | 具体措施 | 时间节点 | 成功指标 |
|:---|:---|:---|:---|:---|:---|
| [Skill1] | 中 | 高 | [措施] | [时间] | [可衡量指标] |

### 维度 3：未用技能审视

**输入**：会话 system-reminder 注入的可用技能列表 + 本次任务描述 + 维度 5 的问题清单
**分析**：
- 本次任务中，哪些 Skill 应该用但没用？
- 每项未用技能能否解决维度 5 中的某个问题？
- 每项未用技能能否优化维度 6 中的某个流程瓶颈？
- 引入可行性论证

**未用技能引入可行性论证**：

| Skill | 引入理由 | 预期效益 | 引入成本 | 实施路径 | 结论 |
|:---|:---|:---|:---|:---|:---|
| [Skill1] | 对接 [问题X] | [效益] | 低/中/高 | [路径] | 建议引入/暂缓/放弃 |

结论判定：
- 能解决维度 5 的"严重"及以上问题 → 建议引入
- 能优化维度 6 的"高影响"瓶颈 → 建议引入
- 无关联场景 → 暂无应用场景

### 维度 4：场景沉淀识别

**输入**：本次任务中的关键场景
**分析**：
- 哪些场景是首次遇到？（新模式）
- 哪些场景是重复出现？（≥3 次 → 值得沉淀）
- 用四象限模型筛选 Top 20% 高优先级场景
- 为高优先级场景设计 SOP

**频率-重要性四象限模型**：

```
重要性 ↑
  高 │ ② 重要+低频        │ ① 重要+高频（Top 20%）
     │ 观察，准备模板       │ 立即沉淀 SOP
     ├────────────────────┼────────────────────
  低 │ ④ 不重要+低频       │ ③ 不重要+高频
     │ 忽略               │ 标准化但不重点投入
     └────────────────────┴────────────────────→ 频率
       低                   高
```

**关键场景沉淀方案**（Top 20% 场景）：

| 场景 | 触发条件 | 标准操作步骤（SOP） | 所需资源 | 注意事项 | 关联模板 |
|:---|:---|:---|:---|:---|:---|
| [场景1] | [条件] | [步骤1→2→3] | [资源] | [注意] | [模板链接] |
### 维度 5：问题与预防机制

**输入**：本次踩坑记录
**分析**：每个问题分类 + 严重度评级 + "严重"及以上问题强制 5Why + 鱼骨图分析 + 预防措施落实到维度 6 或维度 2

**问题分类体系**：

| 分类 | 典型问题 |
|:---|:---|
| 流程 | 步骤遗漏、顺序错误、缺少门禁 |
| 技能 | 不知道方法、方法使用错误 |
| 工具 | 工具不可用、配置错误、版本问题 |
| 沟通 | 需求不清、假设不同步 |
| 外部 | API 故障、依赖不可用、网络问题 |

**严重度等级**：

| 等级 | 定义 | 处理 |
|:---|:---|:---|
| 致命 | 数据丢失、安全漏洞、生产崩溃 | 立即修复 + 5Why |
| 严重 | 功能失效、阻塞后续工作 | 当次会话修复 + 5Why |
| 一般 | 体验问题、效率降低 | 记录 + 常规分析 |
| 轻微 | 风格不一致、小改进 | 记录即可 |

**5Why 分析模板**：

```
问题：[描述]
Why 1: [直接原因]
Why 2: [为什么会有直接原因]
Why 3: [更深层原因]
Why 4: [继续深挖]
Why 5: [根本原因]
→ 根本原因：[结论]
→ 预防措施：[具体行动]
```

**输出物**：《问题分析与预防措施库》

| ID | 问题 | 分类 | 严重度 | 根本原因 | 预防措施 | 落实到 | 状态 |
|:---|:---|:---|:---:|:---|:---|:---|:---|
| P1 | [描述] | 流程 | 严重 | [5Why 结论] | [措施] | 维度 6 [步骤X] | 待执行 |

### 维度 6：工作流优化方案

**输入**：本次工作流程 + 维度 5 的问题根源所在环节
**分析**：绘制当前流程 + 标注瓶颈/冗余/等待/返工 + 评估影响 + 识别并行/自动化机会

**流程标注符号**：

| 符号 | 含义 | 说明 |
|:---|:---|:---|
| ⏸ | 等待 | 需要人工确认或外部依赖 |
| 🔄 | 返工 | 需要重复执行 |
| ⚡ | 瓶颈 | 耗时最长的步骤 |
| 🤖 | 可自动化 | 当前手动但可自动化 |
| ∥ | 可并行 | 当前串行但无依赖 |

**输出物**：《流程优化建议书》

| 步骤 | 当前耗时 | 影响度 | 问题标注 | 优化方案 | 预期效果 | 对应预防措施 |
|:---|:---:|:---:|:---:|:---|:---|:---|
| [步骤1] | 30min | 高 | ⚡瓶颈 | [方案] | 节省 20min | P1 措施 |

### 维度 7：问题总结与计划制定

**输入**：维度 1-6 的结论
**分析**：跨模块汇总 + 用"影响程度-紧急程度"矩阵统一排序 + 制定实施计划 + 评估经验升级为规则

**影响程度-紧急程度矩阵**：

```
紧急程度 ↑
  高 │ ② 高影响+低紧急    │ ① 高影响+高紧急
     │ 纳入下周计划       │ 立即执行
     ├────────────────────┼────────────────────
  低 │ ④ 低影响+低紧急    │ ③ 低影响+高紧急
     │ 低优先级           │ 快速处理或委托
     └────────────────────┴────────────────────→ 影响程度
       低                   高
```

**输出物**：《行动计划表》

| # | 任务 | 影响 | 紧急 | 象限 | 负责 | 时间节点 | 前置任务 | 监控指标 | 状态 |
|:--|:---|:---:|:---:|:---:|:---|:---|:---|:---|:---|
| 1 | [任务1] | 高 | 高 | ① | [人] | [时间] | [依赖] | [指标] | 待执行 |

**经验→规则升级评估表**（每个新增经验都过一遍）：

| 经验 | 违反次数 | 可自动化 | 升级条件 | 升级去向 |
|:---|:---:|:---:|:---|:---|
| [经验1] | N 次 | 是/否 | ≥3次 + 可自动化 + 有行动方案 | SKILL.md 套路段 / MEMORY.md 条目（policy 须人工确认） |

升级判定标准：
- experience → pattern：同类事件 ≥3 次 + 跨任务 + 根因一致
- pattern → heuristic：成功率 >80% + 不引入新问题
- heuristic → policy：效果显著 + 人工确认

### 维度 8：元认知反思（复盘本身的复盘）

**输入**：本次复盘过程
**分析**：
- 数据源是否完整？有没有遗漏的日志/经验文件？
- 分析深度是否足够？有没有哪个维度只是走过场？
- 结论是否可执行？行动计划是否具体到可以直接开工？
- 本次复盘本身有什么问题？（耗时太长？遗漏了什么？）

**输出**：元认知反思（本次复盘的质量评估 + 改进方向）

> 这个维度的价值：without-skill 的 agent 会自发做这个分析，但 skill 如果不规定，它反而不会做。加入 skill 确保每次复盘都有质量闭环。
### 维度 9：一次性工具沉淀清单（必走，不可跳过）

> **触发**：任务过程中临时写的脚本 / Python one-liner / shell 命令 — **用完即弃**还是**沉淀模板**? 撞 1 次也走,不依赖撞次累门槛。
> **跟维度 4 区别**：维度 4 = 通用场景沉淀识别（撞 ≥3 才升级 pattern）；维度 9 = 一次性工具专项沉淀决策（4 类决策，撞 1 也走）。
> **跟维度 6 区别**：维度 6 = 工作流优化方案（流程层）；维度 9 = 工具层产物沉淀（代码/脚本层）。

**输入**：本次任务期间写的所有一次性脚本 / 工具 / 命令
**分析**：
- 工具描述 + 用在哪
- 沉淀价值评分（高 / 中 / 低）：
  - 高 = 撞 P0 critical / 再用频率高 / 协议必走
  - 中 = 单 session 内部多次复用
  - 低 = 一次性专用
- 沉淀形式：并入相应 skill 的 SKILL.md 段 / `MEMORY.md` `[项目名]` 速查条目 / 新 skill

**4 类决策表**：

| 决策 | 条件 | 沉淀形式 |
|:---|:---|:---|
| skill 候选 | 跨 session 复用 + 协议化 | 新 skill 文件夹 + SKILL.md |
| 永久化 | 单项目内高频 | 项目内 scripts/ 或 tools/ |
| 模板 | 结构化重复 | 并入相应 skill 的 SKILL.md 段（不再建独立模板目录） |
| 弃用 | 一次性专用 | 不沉淀，记录即可 |

**输出物**：《一次性工具沉淀清单表》

| 一次性工具 | 用在哪 | 沉淀价值 | 沉淀形式 |
|:---|:---|:---:|:---|
| [工具/脚本] | [场景] | 高/中/低 | SKILL.md 段 / MEMORY.md 速查条目 |

**Skip conditions**：
- Mode A（快速复盘）：dim 9 optional
- Mode B with no 1-time tools used：dim 9 = NONE（显式标记 NONE，不静默跳过）

### 维度 10：工具链 sub-protocol 反思（可选）

> **触发**：复盘期间撞**工具链层**反复出（Bash / Write / Edit / Read / Grep）→ 局限版分析（单工具链）。
> **跟维度 11 区别**：维度 10 = 单工具链层撞坑反思（局限）；维度 11 = 复盘流程任何撞坑（泛化）。
> **何时跳过**：本次复盘期间**没**撞工具链层反复问题（≥3 次同类）→ 跳过本维度，直接进维度 11。

**输入**：本次复盘期间撞的工具链层问题
**分析**：
- 撞坑 trace + 修法
- 5Why 根因（聚焦"工具链协议遗漏"）
- sub-protocol 沉淀（N 层 + N 条）→ 跟现有协议**配对**扩展

**输出**：工具链 sub-protocol vN.0 沉淀（并入相应 skill 的 SKILL.md 或 `MEMORY.md`，不再建独立 checklist 模板文件）

**示例**：Write 工具沙箱不可信 sub-protocol v1.0（路径 / heredoc / `>>` 追加 / 验证 4 层）→ 落到对应 skill 或 `MEMORY.md` 附录。

### 维度 11：复盘过程中出现的问题（必走，不可跳过）

> **触发**：维度 11 是 retro 流程**范式转移** — 从"复盘什么"扩展到"复盘过程中出了什么"。必走，不可跳过。
> **跟维度 5 区别**：维度 5 = 任务执行撞坑（业务层）；维度 11 = 复盘过程本身撞坑（元层）。
> **跟维度 10 区别**：维度 10 = 单工具链（局限）；维度 11 = 复盘流程任何撞坑（泛化）。

**输入**：写本 retro 前 10 维度期间撞的所有坑（修了 → 整合进本维度）
**分析**：
- 撞坑分类：工具链层 / 协议层 / 流程层 / memory 维护层 / 任何 future 撞坑
- 撞坑评分（反思 4 强制公式）：严重度 × 频率 × 影响 = 整合优先级
  - P0 × 单次 = 立即整合 retro
  - P1 × N 次同类 = 升 E 候选
  - P0 × N 次同类 = 升 H 协议
- 复盘反模式识别（元层）："修完即 OK" / "ad-hoc 加维度不沉淀" / "撞 N 次不主动升 H"
- 整合路径：撞 1 次 → E 候选；撞 N 次同类 → 升 H 协议

**撞坑分类表模板**：

| 类别 | 例 | 修法 | 评分 (P0/P1 × 频率) |
|:---|:---|:---|:---:|
| 工具链层 | shell 引号嵌套 / Write silent skip | heredoc + `>>` 追加 + `test -e` 验证 | P1 × N |
| 协议层 | 未走 5 轮 DRL / 未 verify | 强制 deep-review-loop skill | P0 × 单 |
| 流程层 | daily 日志经验段漂移 / 5 件套未 sync | 5-piece bundle verify | P1 × N |
| memory 维护层 | `USER.md` 指针断链 / 旧路径残留 | Grep 记忆根确认无残留 | P1 × N |
| 任何 future 撞坑 | (留作未来) | (留作未来) | — |

**反模式速查表**：

| 反模式 | 撞同根因 | 修法 |
|:---|:---|:---|
| "修完即 OK" 不整合 retro | AI 即兴分析丢弃 | 撞 1 次立即整合维度 11 |
| ad-hoc 加维度不持久化模板 | 改 skill + 模板 + memory 三处不全 | A+B+C 三处全改 |
| 撞 N 次不主动升 H | 用户短纠才触发 | 撞 N 次同类**主动**升 H，不等用户触发 |

**输出**：
1. 撞坑分类表（类别 | 例 | 修法 | 评分）
2. 5Why 根因（聚焦"复盘流程本身"）
3. 修复整合（跟维度 5/6/9/10 配对，不重复）
4. 反模式升 E/H 候选（跟维度 7 经验→规则升级表配对）

> **这个维度的价值**：维度 11 是元层兜底 — 之前 10 维度都聚焦"复盘什么"，维度 11 强制"复盘过程本身是否健康"。必走，不可跳过。跟维度 8（元认知反思）配对成元层闭环：维度 8 = 复盘质量评估（事后），维度 11 = 复盘过程撞坑整合（事中）。
**Step 3：生成报告**

报告经 `memory` 工具 target=`daily` 写入当日 daily 日志 `~/.qwenworkcn/awareness/main/memory/<YYYYMMDD>.md` 的复盘段，格式：

```markdown
# YYYY-MM-DD 全面复盘

**项目**: [项目名]
**工作内容**: [概述]
**产出**: N 项版本推进/交付（如适用记 commit 数），N 文件变更，N 行代码

---

## 1. 经验复用梳理
[维度 1 输出]

## 2. 技能优化评估
[维度 2 输出]

## 3. 未用技能审视
[维度 3 输出]

## 4. 场景沉淀识别
[维度 4 输出]

## 5. 问题与预防机制
[维度 5 输出]

## 6. 工作流优化方案
[维度 6 输出]

## 7. 问题总结与计划制定
[维度 7 输出：行动计划 + 经验升级评估表]

## 8. 元认知反思
[维度 8 输出：本次复盘的质量评估 + 改进方向]

## 9. 一次性工具沉淀清单（必走）
[维度 9 输出：4 类决策表 + 沉淀价值评分 + 沉淀形式]

## 10. 工具链 sub-protocol 反思（可选）
[维度 10 输出：工具链层撞坑反思 + sub-protocol vN.0 沉淀]

## 11. 复盘过程中出现的问题（必走）
[维度 11 输出：撞坑分类表 + 5Why 元层根因 + 反模式识别 + 升 E/H 候选]
```

**Step 3.5：5 件套同步 verify（强制）**

> **触发证据**：复盘类指令必同步多个真理源，漏任一件 = 复盘未闭环。

报告生成后，**强制 verify 以下 5 件套全部同步**：

| # | 件 | 路径 | 检查方法 |
|:--|:---|:-----|:--------|
| 1 | **复盘主段** | 当日 daily 日志复盘段（`~/.qwenworkcn/awareness/main/memory/<YYYYMMDD>.md`） | `memory_get` / Read 确认复盘段存在、11 节齐 |
| 2 | **MEMORY.md 项目条目更新** | `MEMORY.md` `[项目名]` 条目 | `memory_search` / Grep 记忆根文件，本次 session 关键词 ≥ 1 |
| 3 | **USER.md 更新**（如涉及用户级偏好） | `USER.md` | `memory_search` 本次新增条目 ≥ 1（如适用） |
| 4 | **daily 日志经验备忘段** | 当日 daily 日志经验段 | `memory_get` / Grep 本次 session 编号 ≥ 1 |
| 5 | **E-rule 候选** | `MEMORY.md` `[项目名]` 速查条目 | Grep 记忆根文件 "E[0-9]+ 候选" ≥ 1 新增 |

**verify 失败时**：立即补漏（每件 < 5 min），不要等下次 session。

**输出汇总**：

```markdown
### 5 件套同步 verify

| # | 件 | 状态 |
|:--|:---|:----:|
| 1 | 复盘主段 | ✅ 当日 daily 日志复盘段 |
| 2 | MEMORY.md 项目条目更新 | ✅ MEMORY.md:[项目名] 条目 LLL |
| 3 | USER.md 更新 | ✅ USER.md:LLL（如适用） |
| 4 | daily 日志经验备忘段 | ✅ memory/<YYYYMMDD>.md 经验段 |
| 5 | E-rule 候选 | ✅ E78 升 N/3 + E79 新 1/3 |
```

---

**Step 4：知识层升级（experience → pattern → heuristic → policy）**

只负责经验→规则的知识层级升级，不涉及具体行动项（行动项在 Step 5）。

| 条件 | 升级动作 | 执行方式 |
|:---|:---|:---|
| 同类经验 ≥3 次 + 跨任务 + 根因一致 | 经 `qwenwork_skill_manage` 并入相应 skill 的 SKILL.md（pattern 层套路段） | **自动建/补 skill** |
| 某 pattern 成功率 >80% + 不引入新问题 | 经 `qwenwork_skill_manage` 并入相应 skill 的 SKILL.md（heuristic 层规则段） | **自动建/补 skill** |
| 某 heuristic 效果显著 | 经 `memory` 工具并入 `MEMORY.md` `[项目名]` 条目（policy 层） | **需人工确认** |

**沉淀条目 / skill 段 frontmatter 标准**：
```yaml
---
name: [short-kebab-case]
description: [one-line summary]
type: pattern / heuristic / policy
id: [optional]
level: [optional]
tags: [optional]
---
```

**安全规则**：
- 对 skill 只建/补不删除（删除需 `qwenwork_skill_manage` action=`delete` 且人工确认）
- 目标段落已存在 → 追加内容，不覆盖
- policy 层升级一律需人工确认后并入 `MEMORY.md`

每个升级动作执行后：`✅ 已写入 [路径]` 或 `⚠️ 需确认 [原因]`。

**Step 5：执行行动计划（按优先级分流）**

维度 7 产出的行动计划，按优先级决定执行方式：

| 优先级 | 执行方式 | 说明 |
|:---|:---|:---|
| **P0**（崩溃/安全/数据丢失） | **立即自动执行** | 不等确认，执行后报告 |
| **P1**（核心功能失效） | **立即自动执行** | 不等确认，执行后报告 |
| **P2**（体验优化/非核心） | **等用户确认** | 列出待确认项，用户说"执行"再动 |
| **P3**（nice-to-have） | **只记录** | 写入计划文件，不主动执行 |

**自动执行的动作类型 + 具体格式**：

| 动作类型 | 执行方式 | 输出格式 |
|:---|:---|:---|
| 沉淀可复用模板 | 并入相应 skill 的 SKILL.md 段（`qwenwork_skill_manage`） | 段落须含使用示例 |
| 更新 Skill | `qwenwork_skill_manage`（action=`patch`/`edit`）改 `~/.qwenworkcn/skills/<name>/SKILL.md` | 修改前先 Read，自动备份 |
| 追加经验条目 | `memory` 工具 target=`daily` 追加到当日 daily 日志（带 `[项目名]` 前缀） | 格式见模式 A |
| 更新速查表 | `memory` 工具 target=`memory` 并入 `MEMORY.md` `[项目名]` 速查条目 | 格式：`[项目名] [编号] [关键词] — [规则]` |
| 沉淀 pattern 套路 | `qwenwork_skill_manage` 补相应 skill 的 SKILL.md | 含 When/Pattern/Evidence/Related 段 |
| 沉淀 heuristic 规则 | `qwenwork_skill_manage` 补相应 skill 的 SKILL.md（或 `MEMORY.md` 条目） | 含 Rule/Success Rate/Evidence 段 |
| 更新 Skill 缺口清单 | `memory` 工具 target=`daily` 追加当日 daily 日志缺口段 | 格式：`| [Skill] | [场景] | [触发词] |` |

**每个动作执行前必须**：
1. 检查目标位置现状（`memory_get` / Read / Bash `test -e`）
2. 已存在 → 追加，不覆盖（memory 类经 `memory` 工具，skill 类经 `qwenwork_skill_manage`）
3. 不存在 → 创建，带完整 frontmatter（memory 类经 `memory` 工具，skill 类经 `qwenwork_skill_manage` action=`create`）

**执行后输出汇总**：

```markdown
### 执行汇总

**自动执行（P0/P1）**：
- ✅ [动作1] — [结果]
- ✅ [动作2] — [结果]

**待确认（P2）**：
- ⏳ [动作3] — 说"执行"开始
- ⏳ [动作4] — 说"执行"开始

**已记录（P3）**：
- 📝 [动作5] — 写入 plans/
```

---

## 与现有系统的关系（含三 skill 闭环）

### 三 skill 闭环

**闭环方向**：deep-review-loop（审查）→ mem-wrap-up（收尾）→ self-evolution（沉淀）

**本 skill 位置**：沉淀端（闭环末端，反向喂回 DRL）

**维度级联动点**：

| 本 skill 维度 | 输入来源 | 上游 skill / 步骤 |
|:---|:---|:---|
| dim 1 经验复用 | DRL residual + mem-wrap-up Step 5 sediment | deep-review-loop R3 + mem-wrap-up Step 5 |
| dim 5 问题预防 | DRL residual（含 P2 残留经验）+ mem-wrap-up audit | deep-review-loop R3 + mem-wrap-up Step 2 |
| dim 9 一次性工具沉淀 | DRL class-level（P3 由 DRL backlog 兜底）+ mem-wrap-up daily 日志 | deep-review-loop R1b + mem-wrap-up Step 4 |
| dim 11 复盘撞坑 | 反向喂回 → 升级 DRL 协议 | → deep-review-loop 5 轮细节 |

### 系统分工表

| 系统 | 角色 | 分工边界 |
|:---|:---|:---|
| self-evolution（本 skill） | **分析 + 升级 + 执行** | 快速模式直接写入 3 处落点（daily 日志经验段 / MEMORY.md 速查条目 / daily 日志缺口段）；全面模式做 11 维度分析 + 知识层升级 + 行动项执行 |
| 当日 daily 日志经验段 | 按次经验记录入口（当日流水权威） | self-evolution 快速模式写入 |
| `MEMORY.md` `[项目名]` 速查条目 | 稳定速查表（从 daily 日志经验段蒸馏） | self-evolution 快速/全面模式更新 |
| 当日 daily 日志「Skill 缺口」段 | Skill 使用检查清单 | self-evolution 快速模式记录缺口 |
| deep-review-loop skill | 5 轮深度审查 | dim 5/9 输入源；dim 11 反向升级目标 |
| mem-wrap-up skill | session 收尾 7 步流水线 | dim 1/5/9 输入源；与 self-evolution 互补 |

### 单一事实源原则

```
当日 daily 日志经验段（按次记录）→ 每次任务的发现和教训
  ↓（同类 ≥3 次 / 稳定后蒸馏）
MEMORY.md `[项目名]` 速查条目（稳定经验权威源 + 索引）→ 再沉淀进相应 skill 的 SKILL.md
  ↓
当日 daily 日志复盘段（分析报告）→ 引用上述两层，不重复内容
```

---

## 边界限制

- 不改变已有 Skills 的核心职责
- 不自动删除 Skill
- 快速复盘是 Completion Protocol 的一部分，不可跳过
- 全面复盘的 dim 9（一次性工具沉淀）和 dim 11（复盘过程撞坑）必走，不可跳过

## Verdict 字眼合规自检
- 全文 Grep 禁词：`完成|PASS|12/12|闭环|OK|没问题|looks good`
- 用"数据 + 实证 + residual risk 列表"代替 verdict 字眼
- 历史 log 文件例外（引用过往 verdict 不算违规）

## Self-Disclosure
- 0 verdict 字眼
- 11 维度完整内联（dim 1-11），dim 9 + dim 11 必走
- 5 件套 sync verify 强制（Step 3.5）
- 知识层升级安全规则（只创建新文件，policies 需人工确认）
- 行动项 P0/P1 立即执行，P2 等确认，P3 只记录

## Reference
- **外部 vault 蒸馏来源（路径已脱敏）**：由外部记忆库/skill 库蒸馏而来，蒸馏原则见下条；原 user 训诫（DRL 真循环铁律 2026-07-12）现已常驻 `USER.md`。
- **内联模板清单**：`11-dimensions-deep-retro.md`（367 行，已内联）+ `evolution-report.md`（已内联）+ `write-large-file-checklist.md`（已用「工具链 sub-protocol 反思」维度替代）
- **deep-review-loop skill（已蒸馏，仓库版）**：`skills/deep-review-loop/SKILL.md`
- **mem-wrap-up skill（已蒸馏，仓库版）**：`skills/mem-wrap-up/SKILL.md`
- **agent-session-loop（仓库版）**：`skills/agent-session-loop/SKILL.md`（三阶段整合流水线入口）
- **蒸馏原则**：剥离原脚本 hook（bash/Node/Python）+ 原目录结构 + 原规则术语引用 + 原经验捕获依赖 + 模板独立文件（11 维度内联）；保留双模式 + 11 维度完整 + 5 件套 sync verify + 知识层升级 + 行动项分流 + verdict 禁词；嫁接 QwenWork 工具映射 + deep-review-loop/mem-wrap-up 联动
- **位置**：本 skill 的 master 副本位于 `~/.qwenworkcn/skills/self-evolution/SKILL.md`；仓库归档副本位于 `D:\1\QwenWork\skills\self-evolution\`
