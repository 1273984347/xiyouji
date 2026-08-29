---
name: agent-session-loop
description: >
  Manages the full agent session lifecycle as a single pipeline: deep review (审查) → wrap-up (收尾) →
  evolution (沉淀). Use at session end, after batch fixes or large docs, when the user says
  "收尾 / wrap up / 复检 / 复盘 / retro", or when docs and code mismatch and the session needs a complete
  close-out with memory sedimentation.
  将 Agent 会话完整生命周期整合为一条流水线：深度复检（审查）→ 7 步收尾 → 复盘沉淀。
  会话收尾、批量修复/长文档完成后、用户说「收尾/复检/复盘/retro」、或文档与代码不一致需完整闭环时使用。
license: Apache-2.0
compatibility: 千问办公 (QwenWork) 为主目标平台，方法论 Agent-agnostic。需子代理派发（Agent 工具）、文件检索（Grep/Read/Glob）与 memory 工具链；平台路径与工具细节见「运行平台：千问办公 QwenWork」段。
metadata:
  version: "1.2.0-qwenwork-native"
---

# agent-session-loop

> **真源声明（W533）**：本技能的唯一 master 是全局安装版 `~/.qwenworkcn/skills/agent-session-loop/`（千问办公实际加载与演进处）；任何仓库内副本（如 `D:\1\xiyouji\skills\agent-session-loop\`）均为**受控只读镜像**，仅可由 `python scripts/sync_skills.py --take-global agent-session-loop` 回写，禁止反向 `--sync` 覆盖 master。


> 一条流水线管理 Agent 会话的完整生命周期：**审查 → 收尾 → 沉淀**。
> 每个 session 结束时按此顺序闭环，把「验证过的结论」沉淀为「可复用的经验」。

**Announce at start:** "I'm using the agent-session-loop skill to run the session lifecycle pipeline (review → wrap-up → evolution)."

## 流水线总览

```
        Phase 1                 Phase 2                Phase 3
   ┌────────────────┐    ┌────────────────┐    ┌────────────────┐
   │  审查 (Review)  │ →  │  收尾 (Wrap-up) │ →  │  沉淀 (Evolution)│
   │ 5 轮深度复检     │    │ 7 步收尾流水线   │    │ 快速/全面复盘     │
   │ R0→R3 + V1→V5  │    │ memory 审计     │    │ 11 维度 + 知识升级 │
   └────────────────┘    └────────────────┘    └────────────────┘
       输出: 收敛结论         输出: 收尾报告         输出: 复利经验
        + residual risk       + sediment            + 规则升级
```

**阶段输入输出契约**（每阶段产出喂给下一阶段）：

| 交接点 | 上游产出 | 下游消费 |
|:---|:---|:---|
| 审查 → 收尾 | 收敛曲线 + ≥3 residual risk | 收尾 Step 4/7 的验证清单 + 待沉淀项 |
| 收尾 → 沉淀 | sediment（编号+5Why 链）+ 当日 daily 日志（4 段 schema 收尾段） | 复盘维度 1/5/9 的输入 |
| 沉淀 → 下一 session | 知识层升级 + 行动项 | 下次会话的规则与 checklist |

## 触发条件

- 会话收尾（用户说「收尾 / wrap up」）
- 批量修复（>10 项）或长文档/方案/skill 写完后
- 用户说「复检 / 收敛 / DRL / 复盘 / retro」
- session 已跑 30+ 轮 / token 接近上限 / 重大里程碑达成
- 怀疑假收敛 / 文档与代码不一致，需要完整闭环

## 精简执行（按场景裁剪）

不是每次收尾都要跑满三阶段。按场景裁剪：

| 场景 | 必走 | 可裁剪 |
|:---|:---|:---|
| 纯调试 session（无版本推进、无新经验） | Phase 2 收尾（最小化） | Phase 1 / Phase 3 标 `not-applicable` |
| 批量修复 / 长文档完成后 | Phase 1 审查（全量） | Phase 3 用快速模式 |
| 周汇总 / 用户明确要求复盘 | Phase 3 全面模式 | Phase 1 降为 R0 表面检查 |
| 完整 session 收尾 | 全三阶段 | — |

> 裁剪不是跳过：被裁剪的阶段必须显式标注 `not-applicable` 并说明理由，不允许静默跳过（对齐「不编造证据」原则）。

---

## Phase 1：审查（Deep Review）

**目标**：在收尾前先证明「本 session 的产出真的没问题」——不收敛就谈不上收尾。

**核心协议**（详情见 [references/01-review.md](references/01-review.md)）：

1. **R0 表面检查**：file size + verdict 字眼 grep + expected hits 必现 + 项目阶段判定（N_max）
2. **R1a 3 独立 verifier**（3 subagent parallel，factual / completeness / reusability，必附工具证据）
3. **R1b 对抗性审查**（1 subagent，default refuted=true + class-level scope + 严重度门槛）
4. **R2 独立审计**（1 subagent，NOT inline，边际收益 gate）
5. **R3 收敛判定**（≥3 residual risk + 收敛曲线 + 过拟合警报）

**4 层过拟合防护**（本阶段强制执行）：
- 层 1：P2 残留 N（比赛级 0 / 生产 3 / 原型 10）；P0/P1 必须为 0
- 层 2：边际收益 gate（修复成本 > 危害 × 3 → 标记接受残留）
- 层 3：过拟合警报（增强版：P0 反弹 1 轮即 STOP / P1 反弹连续 2 轮 / P0/P1 持平走 4 轮窗口停滞观察 / 回归率 >30% → STOP 报告；被动验证见 references/01-review.md）
- 层 4：严重度门槛（P3 及以下不报；class-level instance 例外升级 P2）

**阶段出口条件**：真收敛（P0=0 AND P1=0 AND 连续 2 轮无新 P0/P1）→ 携带收敛曲线 + residual risk 进入 Phase 2。

> 本阶段优先调用本仓库已收录的独立 skill [skills/deep-review-loop/SKILL.md](../deep-review-loop/SKILL.md)；references/01-review.md 为精简快速路径，冲突时以独立 skill 当前版本为准。

## Phase 2：收尾（Wrap-up）

**目标**：把 session 的状态、文档、记忆审计到「可交接」状态，并沉淀本次经验。

**核心协议**（详情见 [references/02-wrap-up.md](references/02-wrap-up.md)）：

1. **memory 健康检查**：记忆根体量 + P0/P1/P2 标记 + `memory/*.md` 日志文件统计
2. **memory audit（5 phase）**：frontmatter / dup / empty / big-file / broken-link + 6 面状态矩阵
3. **fileCount sync**：实际文件数 vs 声明，drift >5% 告警
4. **文档同步 spot-check**：Grep 验证版本号 + 任务 ID 落地（**不信任 prior session 声明**）+ 当日 daily 日志追加 4 段收尾 schema
5. **经验沉淀（sediment）**：Read-before-Edit → Grep-verify-after-Edit → 毕业判据分流
6. **4-step verify**：file exists / content count / link target / 行数
7. **反向验证**：Grep spot-check memory 层 + 调用 Phase 1 审查收尾本身

**阶段出口条件**：收尾报告（影响 / 改动 / 待确认 / 遗留）+ sediment 记录 → 进入 Phase 3。

> 本阶段优先调用本仓库已收录的独立 skill [skills/mem-wrap-up/SKILL.md](../mem-wrap-up/SKILL.md)；references/02-wrap-up.md 为精简快速路径，冲突时以独立 skill 当前版本为准。

## Phase 3：沉淀（Evolution）

**目标**：把 session 的经验升级为可复利的规则，喂回下一 session。

**核心协议**（详情见 [references/03-evolution.md](references/03-evolution.md)）：

1. **快速模式**（默认，任务完成自动）：3 问自检 → 写入当日 daily 日志（经验段 + Skill 缺口清单段）；稳定速查经 `memory` 工具并入 `MEMORY.md` `[项目名]` 条目
2. **全面模式**（周汇总 / 用户要求）：11 维度分析 → 复盘报告写入当日 daily 日志复盘段 → 5 件套 sync verify
3. **知识层升级**：experience → pattern → heuristic → policy（pattern/heuristic 层经 `qwenwork_skill_manage` 并入相应 skill；policy 层须人工确认后并入 `MEMORY.md`）
4. **行动项分流**：P0/P1 立即执行，P2 等确认，P3 只记录

**阶段出口条件**：复利经验入库 + 行动项清单（含待确认项）→ 闭环完成。

> 本阶段优先调用本仓库已收录的独立 skill [skills/self-evolution/SKILL.md](../self-evolution/SKILL.md)；references/03-evolution.md 为精简快速路径，冲突时以独立 skill 当前版本为准。

---

## 子代理不可用降级（2026-08-24 新增）

**触发**：平台派发 subagent 返回不可用/FORBIDDEN（如定价限制 code 112），或环境中无子代理机制。

**降级规则**（降级不是跳过——三阶段各自的检查面必须保留，执行者换成主代理；收尾报告显式标注 `subagent-unavailable`）：

- Phase 1 审查：R1a 降为主代理自走 3-lens 串行（factual → completeness → reusability，各用不同工具模式，每视角附工具证据）或 1 个可用 subagent 全视角；R1b 以 refuted=true 心态自审；R2 换工具/换目录视角重审并声明"独立审计降级为自审"。细节见 `deep-review-loop/SKILL.md`「子代理不可用降级」。
- Phase 2 收尾：步骤 7b DRL 同降级规则；步骤 4/6/7a 的 Grep spot-check 不依赖 subagent 照常执行。
- Phase 3 沉淀：self-evolution 两模式均主代理执行，不派 subagent，不受影响（见其「子代理不可用声明」）。

> 与「Token 超额降级」区别：Token 降级是主动裁剪（等 user 拍板），本降级是平台能力缺失的强制降级，无需征求许可但必须显式声明。

## 运行平台：千问办公 QwenWork

1. 本 skill 运行于**千问办公（QwenWork）**；正文所有路径、工具、检索都按 QwenWork 原生写，不使用外部平台占位符。
2. 记忆根：`~/.qwenworkcn/awareness/main`（`MEMORY.md` 跨会话长期记忆 / `USER.md` 用户级偏好与铁律 / `memory/YYYY-MM-DD.md` 每日日志）。写入经 `memory` MCP 工具（target=`memory` / `user` / `daily`），检索经 `memory_search` / `memory_get`；`MEMORY.md` 与 `USER.md` **禁止直接 Edit/Write**。
3. 技能根：`~/.qwenworkcn/skills`；技能增改删用 `qwenwork_skill_manage`（action `create` / `patch` / `edit` / `delete`）。
4. 可用技能列表由会话 system-reminder 注入；调用某技能用 `Skill` 工具。
5. 工具映射：终端用 `Bash 工具`（PowerShell 语义可 `powershell.exe -Command "…"`；存在性/软链/行数/体量校验用 `test -e` / `readlink` / `wc -l < <FILE>` / `find -size +50k` / `ls -R`）；子代理用 `Agent 工具`（`subagent_type`：`general-purpose` / `Explore` / `Plan`，可并发 / 可后台）；文件读写 `Read` / `Write` / `Edit`，检索 `Grep` / `Glob`；记忆读写 `memory` / `memory_search` / `memory_get`。
6. 文件保护：删除一律进系统回收站（禁 `rm` / `del`）；改用户文件前先备份（Git 版本库内项目除外）。
7. QwenWork 项目不保证为 git 库；一致性校验一律走「治理层清单现场枚举 + Grep spot-check 现测」，不依赖版本库文件清单类校验。
8. 日期占位符 `<date>` / `<YYYYMMDD>` 表示当日（daily 日志文件名 `memory/<date>.md`）；跨项目区分用条目内 `[项目名]` 前缀，不派生项目目录名。

**记忆落点速查（正文各步骤引用）**

| 沉淀内容 | QwenWork 落点 | 写入方式 |
|:---|:---|:---|
| 用户级偏好与铁律 | `USER.md` | `memory` target=`user` |
| 项目级规则 / 长期经验 / 稳定速查 | `MEMORY.md`（条目带 `[项目名]` 前缀） | `memory` target=`memory` |
| 收尾 4 段日志 / 近期 topic / 当日经验记录 / 复盘报告 / Skill 缺口清单 | 当日 daily 日志 `memory/<YYYYMMDD>.md`（条目带 `[项目名]` 前缀） | `memory` target=`daily` |
| 稳定套路（pattern / heuristic 层） | `~/.qwenworkcn/skills/<name>/SKILL.md` | `qwenwork_skill_manage` 建/补 |
| policy 层规则 | `MEMORY.md` | **须人工确认后**并入 |

## Verdict 字眼合规自检
- 全文 Grep 禁词：`完成|PASS|12/12|闭环|OK|没问题|looks good`
- 用「数据 + 实证 + residual risk 列表」代替 verdict 字眼
- 历史 log 文件例外（引用过往 verdict 不算违规）

## Failure handling
- 任一步骤失败 → 不继续下一步，stderr 报告
- 裁剪必须显式标注 `not-applicable` + 理由，不允许静默跳过
- Token 超额（Phase 1 派 3 subagent）→ 降级为 1 subagent / 分批派 / 等 user 拍板

## Self-Disclosure
- 0 verdict 字眼
- 三阶段按序执行，被裁剪阶段显式标注 `not-applicable`
- Phase 1 必出收敛曲线 + ≥3 residual risk
- Phase 2 必出收尾报告 + 验证铁律 spot-check（项目层 + memory 层）
- Phase 3 必出 sediment / 复盘报告 + 5 件套 sync verify
- 4 层过拟合防护必走（P2 残留 N / 边际收益 gate / 过拟合警报 / 严重度门槛）

## Reference
- **组成**：三阶段分别对应本仓库独立 skill `skills/deep-review-loop` / `skills/mem-wrap-up` / `skills/self-evolution`（另有上游 GitHub 仓库）；本仓库为整合流水线，references/ 为各阶段精简详案（完整协议以独立 skill 当前版本为准）
- **设计来源**：从真实编码会话中蒸馏的「三 skill 闭环」（2026-07 建立）——审查 → 收尾 → 沉淀，多次假收敛 / 声明未落地教训固化
