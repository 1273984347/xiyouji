# Preflight 与 Subagent 模板——派 subagent 前的三轨验证与 fallback 机制

> 轨标：外部分享

## 引子

派 subagent 执行任务前，你是否验证过它将引用的 API、函数签名、配置项、源文件位置？还是直接把任务描述甩出去，让 subagent 自己摸索？

很多人在用 AI 代理协作时，习惯把任务"派出去"就万事大吉。任务模板写好、文件路径给清楚、目标说到位，剩下的交给 subagent 自己跑。结果一次通过率低得离谱：subagent 报"未找到该函数"，转而自己脑补了一个不存在的接口；引用了一段原文位置，line 号差了十几行；甚至"顺便修了一下"周边无关代码，把 atomic commit 原则踩在脚下。

更糟的是 subagent 失败后，主代理常常陷入两难：再派一次浪费 token，放弃则任务搁浅。反复派发不仅成本高，还可能让 subagent 在同样的盲区里再次栽跟头。

我们在大量 agent 协作实践中沉淀出一套"Preflight + Subagent 模板"方法论，核心就两句话：**派 subagent 前先验证事实，subagent 失败时主代理直接 fallback**。这篇文章把这套方法拆开讲清楚——三轨验证怎么验、prompt 模板的硬性约束长什么样、fallback 机制如何兜底，最后给一份可复用的执行清单。

需要强调的是，Preflight 不是 subagent 的前置负担，而是 主代理 的职责。主代理在派发前花几分钟验证事实，远比 subagent 摸黑探索后返工要高效。这套方法论适用于任何"主代理派 subagent 执行子任务"的协作场景，不限定具体技术栈。

这篇文章面向的读者是：在 AI 代理协作、多 agent 编排、自动化任务派发等场景里摸爬过的工程师和项目管理实践者。无论你用的是哪种 agent 框架、哪种 LLM、哪种任务编排工具，只要你有过"subagent 一次通过率低、返工频繁、scope 失控"的痛点，下面的方法论都能直接对应上你的场景。文中的例子会尽量保持通用——接口漂移、事实声明错误、line 号错位这些问题在任何一个代码库或文档库里都会出现。

---

## 一、为什么需要 Preflight

先看 subagent 失败的四种典型场景，每一种都源自"摸黑探索"。

### 1.1 接口漂移

计划文档假设的接口签名与实际代码漂移。比如 plan 写的是 `from lib.search import search`，实际代码里却是 `search_service.perform_keyword_search`；plan 假设 `rag_ask(question, top_k=3)`，实际签名是 `rag_ask(question, top_k_articles=5, top_k_passages=3, channel="all")`。subagent 拿着过期假设去实现，要么报错，要么自己编一个不存在的接口凑数。前者浪费时间，后者引入幻觉。

### 1.2 事实声明错误

任务模板里塞了错误的事实声明。比如模板说"某法宝是某妖王的法宝"，实际原文里这法宝归另一个人。subagent 基于错误事实去做"原文验证"，最后产出一份基于错误前提的"正确"分析——错得根正苗红。这类问题尤其隐蔽，因为 subagent 的推理过程看起来完全自洽，只是前提错了。

### 1.3 scope 蔓延

subagent 看到周边代码有 bug 或可改进的地方，忍不住"顺便修一下"。一次 commit 里混进了无关改动，atomic commit 原则被破坏。code review 时根本看不清这次到底改了什么、为什么要改。更麻烦的是，"顺便修"的改动往往没有经过同样的验证流程，可能引入新的回归。

### 1.4 context 丢失

长任务执行到一半，subagent 的 context 被截断或丢失，返回结果缺失关键字段。主代理拿到一份半成品，不知道该信任到什么程度，也不知道缺失的部分是否影响后续判断。

### 1.5 共性与根因

这四种场景的共性是：subagent 在 没有事实基础 的情况下被派出去，只能靠自己的"直觉"和"估算"补全信息。Preflight 的目标就是把事实基础在派发前就打牢——主代理亲自验证 API、验证事实、验证 line 号，把修正后的准确信息塞进 subagent prompt，让 subagent 在 已知正确 的基础上工作。

Preflight 的成本是主代理的几次 Grep/Read 调用，收益是 subagent 一次通过率显著提升、返工次数大幅下降。这笔账怎么算都划算。

---

## 二、Preflight 三轨验证

三轨验证是 Preflight 的核心。它从 单轨 → 双轨 → 三轨 逐步升级而来，每一步升级都对应一类稳定盲区。

### 2.1 第一轨：line 号归属验证（Grep 验归属）

**触发条件**：任务需要引用源文件的具体 line 号位置（比如"原文第 X 行""配置文件第 Y 行"）。

**操作**：主代理用 Grep 验证 line 号确实归属它声称的位置。比如任务模板说"line 736 是某句关键台词"，主代理 Grep 该文件确认 line 736 的实际内容是否匹配。

**单轨的局限**：仅验归属会漏掉 内容错位。比如 line 736 确实归属第 5 回，但实际是土地公的回答，而任务想要的那句诗其实在 line 734。主代理基于估算给 line 号，没实际读内容，单轨验证发现不了这种错位——line 号"归属正确"但"内容错位"。

**典型反例**：任务模板声明"line 736 是关键诗句"，主代理 Grep 验证 line 736 确实在第 5 回范围内，于是直接采用。subagent 基于"line 736 = 关键诗句"去写分析，产出后主代理 spot-check 才发现 line 736 实际是土地公的对话，关键诗句在 line 734——返工一次。单轨验证在这里给了"归属正确"的假象，掩盖了内容错位。

### 2.2 第二轨：内容匹配验证（Read 验内容匹配）

**触发条件**：在第一轨基础上，line 号涉及具体内容引用时。

**操作**：主代理用 Read 读取 line 号附近的实际内容范围（如 line 730-740），核对内容是否匹配任务描述。不匹配就修正 line 号到正确位置。

**双轨的局限**：双轨验证了 line 号归属和内容匹配，但 仍会漏 chapter 归属错误。比如某 line 号内容确实匹配（"我佛造经传极乐"这句确实在那个位置），但被错误归属到第 12 回，实际属于第 8 回。这类错误在跨章节引用密集的场景里反复出现——内容对、归属错。

**典型反例**：任务模板声明"line 996 属于第 12 回，内容是某段经文描述"。主代理双轨验证：Grep 确认 line 996 归属无误，Read line 990-1000 确认内容确实是那段经文——双轨通过。subagent 基于"line 996 / 第 12 回"去写跨回目分析，产出后主代理 spot-check 用 `num:N` 复核才发现，line 996 实际属于第 8 回，第 12 回是另一个段落的经文。内容对、归属错，双轨没拦住。

### 2.3 第三轨：chapter 归属验证（Grep num:N 范围限定）

**触发条件**：在双轨基础上，line 号涉及章节/回目归属时。

**操作**：主代理用 Grep 的 `num:N` 字段验证 line 号所属的 chapter 范围。比如验证 line 996 是否真的属于第 8 回，而不是被错误归到第 12 回。`num:N` 用于限定 Grep 返回的行号范围，可以精确锁定某一段落的归属。

**三轨的稳定盲区**：第三轨虽然验证了 chapter 归属，但 同一 chapter 内不同段 的 line 段落归属仍可能出错。比如 line 7054 和 line 7062 都属于第 98 回，但前者在段头、后者在段尾，引用错位仍会引入问题。所以三轨验证之后，主代理的 spot-check（抽样复核）依然不可省略——三轨 + spot-check 才是真三轨。

**典型反例**：任务模板声明"line 7054 是第 98 回的某段结尾陈词"。主代理三轨验证：Grep 归属无误、Read 内容匹配、`num:N` 确认属于第 98 回——三轨通过。subagent 基于"line 7054 / 第 98 回段尾"去写分析，产出后主代理 spot-check 才发现 line 7054 实际是第 98 回段中，真正的段尾陈词在 line 7062。同 chapter 内的段落归属错位，三轨没拦住，只能靠 spot-check 兜底。

### 2.4 三轨对比

| 维度 | 单轨 | 双轨 | 三轨 |
|:---|:---|:---|:---|
| 验证项 | line 号归属 | 归属 + 内容匹配 | 归属 + 内容匹配 + chapter 归属 |
| 漏掉的盲区 | 内容错位 | chapter 归属错误 | chapter 内 line 段落归属 |
| 一次通过率 | 低 | 中 | 高（仍需 spot-check） |
| 适用场景 | 仅需验归属 | 引用具体内容 | 跨章节引用密集 |

### 2.5 三轨为什么缺一不可

实战数据反复印证：单轨漏内容错位、双轨漏 chapter 归属、三轨漏 chapter 内段落归属。每一轨都对应一类稳定盲区，跳过任何一轨都会让特定类型的错误溜过去。三轨不是 过度工程，而是 用最小验证集覆盖 已知 三类盲区。

第三轨之后的 spot-check 也不是冗余——它兜底的是"chapter 内 line 段落归属"这类三轨仍可能漏的盲区。Preflight 越完善，spot-check 越轻松；但 spot-check 永远不能省。

### 2.6 方法论的演进逻辑

三轨验证不是一开始就设计出来的，而是在反复踩坑中 逐步升级 而来。演进的逻辑很清晰：每一次升级都对应一类被实战反复打脸的稳定盲区。

最初只有"单轨"——主代理 Grep 验证 line 号归属，觉得"归属对就行"。结果反复出现"归属对、内容错"的返工，于是加上第二轨"内容匹配"。双轨上线后错误率下降，但跨章节引用密集的场景里又开始出现"内容对、归属错"的 chapter 归属错误，于是加上第三轨"chapter 归属"。三轨上线后错误率进一步下降，但同 chapter 内段落归属错位仍偶发——这时不再加第四轨，而是用主代理 spot-check 兜底，因为这类错误率已经很低，spot-check 的抽样复核成本远低于全量第四轨验证。

这个演进逻辑可以提炼为一条原则：**每一轨都对应一类稳定盲区，加轨的判据是"该盲区反复出现且影响一次通过率"，减轨的判据是"该盲区已被前一轨覆盖"**。读者在自己的项目里落地时，不必照搬三轨，而应该先观察自己场景里哪类盲区最频繁，针对性地加轨。如果你的场景几乎没有跨章节引用，第三轨可以省；如果你的场景 line 号引用很少，三轨都可以省，把精力放在接口验证和事实验证上。

方法论不是教条，而是 经验沉淀的起点。三轨验证是我们场景下的最小有效集，你的场景可能需要不同的轨数——但"每一轨对应一类稳定盲区"的演进逻辑是通用的。

---

## 三、Subagent prompt 模板的硬性约束

Preflight 验证完事实，下一步是把这些事实以 硬性约束 的形式写进 subagent prompt。模板包含四块必备内容。

### 3.1 Preflight interface analysis（接口分析）

派 subagent 执行 Task 前，若 Task 引用外部 API/函数/模块/config key，主代理必须：

1. Grep/Read 实际函数签名、import 路径、参数名、config key 名
2. 在 subagent prompt 中提供 **修正后的接口**，而非 plan 里的过期假设
3. 跳过条件：Task 无接口引用时可跳过此步

这一步直接消灭"接口漂移"——subagent 拿到的就是当前代码的真实签名，没有脑补空间。主代理在 Context 段里直接写出修正后的 import 语句和函数签名，让 subagent 不需要自己去翻代码。

### 3.2 Scope-lock constraint（scope 锁定）

subagent prompt 必含一段硬性约束文本：

```
Only modify files listed in the Files section.
Do NOT modify any other files, even if you notice bugs or improvements in surrounding code.
```

中文版：

```
仅修改 Files 段列出的文件，禁止碰其他文件，
即使发现周边代码有 bug 或可改进。
```

无此约束时，subagent 倾向"顺便修一下"周边代码。验证方法：主代理在 subagent 返回后必须 `git show <commit> --stat` 验证文件范围，不能只信 subagent 的口头报告。subagent 报"未碰其他代码"与实际是否碰了其他代码，是两回事——主代理必须用工具验证，而非信任声明。

### 3.3 Preflight fact verification（事实声明验证）

任务模板包含事实声明（人物关系/法宝归属/事件顺序/数据来源/业务规则）时，主代理必须：

1. 独立 Grep 验证关键事实
2. 推翻错误模板声明
3. 在 subagent prompt 中提供 **修正后的事实**

这一步与接口分析互补——前者验 API，后者验事实。两者共同确保 subagent 工作基于准确的基础信息。事实验证尤其重要，因为 subagent 的推理再严谨，前提错了结论也全错。

### 3.4 Fallback 机制（subagent 失败时主代理直接接管）

当 subagent 在 context 丢失或返回结果缺失时未交付，主代理不能 跳过任务，也不能 反复派发。正确做法：

1. 主代理基于已完成 Preflight + 已验证事实清单 直接创作
2. **不跳过**——必须直接执行
3. 完成后主代理 Grep 关键 line 范围 + 跨范围侵入检查 = 真收敛

这条与"主代理 spot-check subagent 声明"原则互补：subagent 报告 ≠ 实际状态，主代理必须验证；subagent 失败时，主代理必须直接执行而非跳过。两条加起来才能形成闭环——验证声明兜底 subagent 的"谎报"，fallback 兜底 subagent 的"未交付"。

### 3.5 完整 prompt 模板

```markdown
# Task: [任务名]

## Context

[提供完整上下文，包括：
- 项目背景
- 当前进度
- 相关文件路径
- 接口签名（Preflight interface analysis 修正后）
- 事实声明（Preflight fact verification 验证后）]

## Files

[列出 subagent 允许修改的文件，绝对路径]

## Scope-lock constraint

Only modify files listed in the Files section.
Do NOT modify any other files, even if you notice bugs or improvements in surrounding code.

## Output Requirements

[明确输出格式：
- 修改文件列表
- 验证命令 + 输出
- 收敛曲线（如适用）]

## Verification

[明确验证要求：
- Grep 验证修复后的值
- 不得仅依赖 Edit 工具返回值]
```

模板的每一块都不是装饰：Context 段承载 Preflight 的修正结果，Files 段定义 scope 边界，Scope-lock 段是硬性约束，Verification 段强制 subagent 自证。跳过任何一块都会留下对应的盲区。

### 3.6 一条额外约束：禁止编造 line 号

如果 subagent 在产出物里需要引用源文件 line 号（比如生成文档、写注释、做分析），必须强制要求：

```
subagent 创建产出物时禁止编造 line 号；
若需引用原文位置，必须 Grep 源文件验证后使用真实 line 号；
无法验证时用"章节作锚点 + 转述方式"代替
（如"原文中那一段""那一段写得极冷"）
```

验证方法：主代理 Grep spot-check subagent 产出物中的 line 号，抽样 3-5 处验证实际位置，差异超过 5 行就全量验证 + 修复。这条约束防止 subagent 在"看起来需要 line 号"时凭印象编造，引入难以追溯的错误。

### 3.7 常见误区

实践中我们见过几类反复出现的误区，列出来供读者避坑：

**误区一：把 Preflight 当成可选优化**。有人认为 Preflight 是"锦上添花"，时间紧时可以跳过。实际数据反复印证：跳过 Preflight 的 subagent 任务，返工率显著上升，返工消耗的 token 远超 Preflight 本身的成本。Preflight 不是优化项，而是 必要项。

**误区二：信任 subagent 的口头报告**。subagent 报"未碰其他代码""已验证 line 号"与实际是否如此，是两回事。主代理必须用工具（`git show --stat`、Grep spot-check）验证，而非信任声明。这条原则与"信任但验证"一脉相承——验证是主代理的职责，不是对 subagent 的不信任。

**误区三：subagent 失败时反复派发**。subagent context 丢失或返回缺失时，有人习惯"再派一次试试"。但同样的任务在同样的盲区里往往会再次失败，反复派发只是浪费 token。正确做法是触发 fallback——主代理基于已完成 Preflight 直接接管，比再派一次更快更稳。

**误区四：三轨验证后跳过 spot-check**。三轨验证显著降低错误率，但 chapter 内 line 段落归属仍是稳定盲区。三轨之后跳过 spot-check，等于在最后一道防线上放水。三轨 + spot-check 才是真三轨，缺一不可。

**误区五：scope-lock 写得太软**。有人把 scope-lock 写成"建议只修改 Files 段的文件"或"尽量不碰其他代码"。这种软约束对 subagent 几乎没有约束力——subagent 看到"顺便修一下"的机会就会上手。scope-lock 必须是 硬性约束，用"Do NOT""禁止"这类祈使语气，不留解释空间。

---

## 四、可复用的执行清单

把上面所有内容提炼成一份可执行 checklist，派 subagent 前逐条对照。

1. **接口验证**：Task 引用 API/函数/config key 时，主代理 Grep/Read 实际签名，把修正后的接口写进 prompt 的 Context 段。
2. **事实验证**：Task 包含事实声明时，主代理独立 Grep 验证，推翻错误声明，提供修正后的事实。
3. **line 号归属验证（第一轨）**：Task 引用源文件 line 号时，主代理 Grep 验证 line 号归属。
4. **内容匹配验证（第二轨）**：Read line 号附近实际内容范围，核对内容匹配，不匹配就修正。
5. **chapter 归属验证（第三轨）**：Grep `num:N` 验证 line 号所属 chapter 范围，防止跨章节归属错误。
6. **scope-lock 写入**：prompt 必含"仅修改 Files 段列出的文件"硬性约束文本，中英文任选其一。
7. **Files 段明确**：列出 subagent 允许修改的文件，绝对路径，不留模糊空间。
8. **Verification 段明确**：要求 subagent 用 Grep 验证修复值，不得仅依赖 Edit 返回值。
9. **返回后 spot-check**：主代理 `git show --stat` 验证文件范围，Grep spot-check 产出物中的 line 号，不能只信 subagent 报告。
10. **禁止编造 line 号**：subagent 引用 line 号必须 Grep 验证；无法验证时用"章节锚点 + 转述"代替。
11. **fallback 触发**：subagent context 丢失或返回缺失时，主代理基于已验证事实清单直接创作，不跳过、不反复派发。
12. **真收敛验证**：主代理完成后 Grep 关键 line 范围 + 跨范围侵入检查，确认真收敛，而非"差不多就行"。

这 12 条不是 必须全用，而是 按需取用。接口验证在无接口引用时可跳过，事实验证在无事实声明时可跳过，三轨验证在无 line 号引用时可跳过。但 scope-lock、返回后 spot-check、fallback 触发、真收敛验证这四条是 任何场景 都该守住的底线。

---

## 五、适用场景与边界

这套方法论不是万能药，有其明确的适用边界。说清楚什么时候用、什么时候不用，比夸大它的作用更有价值。

### 5.1 适用场景

- **多 agent 编排**：主代理派发多个 subagent 并行或串行执行子任务时，Preflight 能显著降低 subagent 间的接口与事实漂移。
- **长文档/大代码库协作**：subagent 需要引用具体 line 号、chapter、文件位置时，三轨验证能有效防止位置错位。
- **atomic commit 严格要求的场景**：code review、合规审计、回滚频繁的项目里，scope-lock 是守住 commit 原子性的关键。
- **subagent 一次通过率低的反复返工**：如果你发现自己反复派发同一类任务，说明 subagent 拿到的事实基础不够扎实，Preflight 正是对症下药。

### 5.2 不适用或可简化的场景

- **一次性、低风险、无引用的简单任务**：subagent 不需要引用 API、不需要 line 号、不需要事实声明的纯生成任务（比如"写一段示例代码"），Preflight 的开销大于收益，可以直接派发。
- **subagent 与主代理共享同一 context 的场景**：如果主代理和 subagent 在同一上下文里工作（而非独立派发），很多验证天然已存在，Preflight 可以大幅简化。
- **场景里没有"章节/line 号"概念**：如果你的任务完全不涉及源文件位置引用，三轨验证可以整体跳过，只保留接口验证、事实验证、scope-lock、fallback 这四块。

### 5.3 边界与局限

Preflight 解决的是"事实基础不准"导致的 subagent 失败，不解决以下问题：

- **subagent 推理能力不足**：如果任务本身的推理难度超出 subagent 能力上限，Preflight 再扎实也无济于事，需要换更强的模型或拆分任务。
- **subagent 工具调用失败**：网络中断、API 限流、工具 bug 等基础设施问题，Preflight 无法预防，需要重试或 fallback 机制兜底。
- **需求本身模糊**：如果任务描述本身就是歧义的，Preflight 验证再多也无法消除歧义，需要先回到需求澄清。

换句话说，Preflight 是"把已知事实打牢"，不是"把未知变已知"。它能消灭接口漂移、事实声明错误、line 号错位、scope 蔓延、context 丢失这五类已知失败模式，但不能替代清晰的需求、合格的模型、稳定的工具链。

---

## 总结

Preflight 与 Subagent 模板的核心方法论可以用一句话概括：**派 subagent 前先验证事实，subagent 失败时主代理直接 fallback**。

三轨验证（line 号归属 + 内容匹配 + chapter 归属）不是 过度工程，而是用最小验证集覆盖三类稳定盲区。每跳过一轨，就有一类特定错误会溜过去。三轨之后仍需主代理 spot-check，因为 chapter 内 line 段落归属仍是稳定盲区——三轨 + spot-check 才是真三轨，缺一不可。

prompt 模板的四块硬性约束（接口分析 + scope 锁定 + 事实验证 + fallback 机制）形成一个闭环：subagent 拿到的是 已验证 的事实基础，被 锁定 在明确 scope 内，失败时 主代理 直接接管。这套组合下来，subagent 一次通过率会显著提升，atomic commit 原则也能守住。每一块约束都对应一类已知失败模式，跳过任何一块都会留下对应的盲区。

fallback 机制是最容易被忽略的一环。很多人在 subagent 失败时陷入"再派一次"或"放弃任务"的两难，反复派发浪费 token，放弃则任务搁浅。正确做法是主代理基于已完成 Preflight 直接执行——Preflight 已经把事实基础打牢，主代理手里有修正后的接口、验证后的事实、明确的 scope，直接创作比再派一次 subagent 更快更稳。fallback 不是"主代理亲自下场"的妥协，而是 Preflight 投资的兑现。

最后强调一点：Preflight 的成本是主代理的几次 Grep/Read 调用，收益是 subagent 一次通过率显著提升、返工次数大幅下降、atomic commit 原则得以守住。把验证前置、把事实打牢、把 scope 锁死、把 fallback 备好——这套方法论的核心就这么简单。它不依赖任何特定框架或工具，只要你的协作模式是"主代理派 subagent 执行子任务"，这套方法就能直接用上。

如果你打算在自己的项目里落地，建议从最小集开始：先守住 scope-lock 和返回后 spot-check 这两条底线（成本最低、收益最直接），再根据自己场景里高频出现的失败模式逐步加轨。不要一上来就照搬三轨——如果你的场景几乎没有 line 号引用，三轨是空转；但如果你的场景里 subagent 反复在接口漂移上栽跟头，那 Preflight interface analysis 就是第一个该加的轨。方法论的价值在于 对症下药，而非照本宣科。

最后一点提醒：这套方法论本身也在演进。三轨验证是当前场景下的最小有效集，未来如果出现新的稳定盲区，会继续加轨；如果某类盲区在新工具/新模型下消失，也会减轨。读者在自己的实践中如果发现了我们没覆盖到的失败模式，欢迎补充——方法论的生命力来自持续迭代的实战检验，而不是一次性的文档沉淀。

回到开头那个问题：派 subagent 执行任务前，你是否验证过它将引用的 API、函数签名、配置项、源文件位置？如果答案是否定的，那么下一次派发前，不妨先花几分钟做一次 Preflight——你会惊讶于这几分钟能省下多少返工的 token 和时间。subagent 一次通过率低，往往不是模型不够强，而是 派发前的事实基础不够扎实。把事实打牢，剩下的交给 subagent，失败了主代理直接接管——这就是 Preflight 与 Subagent 模板的全部要义。
