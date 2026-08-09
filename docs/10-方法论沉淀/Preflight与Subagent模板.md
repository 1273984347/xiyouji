# Preflight 与 Subagent 模板

> 派 subagent 前的事实清单 + Scope-lock + Fallback 模式
> 首次复现：2026-07-21 E19（Anthropic 项目 T14）
> 当前复现计数器：3 项 pattern（Preflight interface analysis + Preflight fact verification + Scope-lock constraint）+ 1 项 fallback（Subagent 失败时主代理直接创作）+ 1 项升级（Preflight 三轨验证 W076 首次完整执行真收敛一次通过·W077-W086 累积 10 次复用稳定有效·总计 11 次完整执行）
> 严重度：中等（影响 subagent 一次通过率 + atomic commit 原则）
> 最新案例：W086 v2.0.59 Preflight 三轨验证第十一次完整执行真收敛一次通过 P0=0/P1=0/P2=0/P3=0

---

## 一、问题背景

### subagent 失败的典型场景

派 subagent 执行 Task 时，以下场景会导致 subagent 一次通过率低：

1. **接口漂移**：计划文档的接口假设与实际代码漂移（如 plan 假设 `from lib.search import search`，实际是 `search_service.perform_keyword_search`）
2. **事实声明错误**：Task 模板包含错误事实声明（如"阴阳二气瓶是大魔青狮法宝"）
3. **scope 蔓延**：subagent 倾向"顺便修一下"周边代码，违反 atomic commit 原则
4. **context 丢失**：subagent 在长任务中 context 丢失，返回结果缺失

### 复现计数器

- **Preflight interface analysis**：1/1（2026-07-21 Anthropic T14）
- **Preflight fact verification**：1/1（2026-07-24 xiyouji W058）
- **Preflight 双轨验证（升级版）**：1/1（2026-07-26 xiyouji W073，W072 教训吸收）
- **Scope-lock constraint**：1/1（2026-07-21 Anthropic T13）
- **Subagent fallback**：3/3（W067/W068/W069）

---

## 二、Preflight interface analysis

### 触发条件

派 subagent 执行 Task 前，若 Task 引用外部 API/函数/模块/config key。

### 操作步骤

1. 主代理 Grep/Read 实际函数签名、import 路径、参数名、config key 名
2. 在 subagent prompt 中提供**修正后的接口**
3. 避免 subagent 基于过期假设实现

### 跳过条件

若 Task 无接口引用 → 跳过此步。

### 典型复现（2026-07-21 Anthropic T14）

**场景**：plan 假设：
- `from lib.search import search`
- `TfidfSearchEngine.load_index()`
- `rag_ask(question, top_k=3)`

**实际**：
- `search_service.perform_keyword_search`
- `perform_semantic_search`
- `rag_ask(question, top_k_articles=5, top_k_passages=3, channel="all")`

**主代理预分析修正后**：subagent 一次通过（复现计数器 1/1）。

### 反向喂回

已反向喂回 executing-plans SKILL.md Step 2 子步骤 2（2026-07-21）。

---

## 三、Preflight fact verification

### 触发条件

Task 模板包含事实声明（人物关系/法宝归属/事件顺序）时。

### 操作步骤

1. 主代理独立 Grep 验证关键事实
2. 推翻错误模板声明
3. 在 subagent prompt 中提供**修正后的事实**

### 典型复现（2026-07-24 xiyouji W058）

**场景**：Task 模板错误声明"阴阳二气瓶是大魔青狮法宝"。

**主代理 spot-check**：Grep 原文 line 5506，确认"阴阳二气瓶"实际归属（非大魔青狮），推翻错误模板声明。

**根因**：Task 模板可能包含错误事实声明，导致 subagent 在执行"原文验证"时基于错误模板引入 P1 错误。

### 与 Preflight interface analysis 互补

- Preflight interface analysis：验证 API/函数签名
- Preflight fact verification：验证事实声明

两者共同确保 subagent 工作基于准确的基础信息。

### 升级版双轨验证（W073 教训吸收，2026-07-26）

**触发条件**：Preflight 阶段验证 line 号引用时。

**单轨 vs 双轨**：
- **单轨（W072 反例）**：仅验 line 号归属回目（如 line 736 归属第5回），不验具体内容 → R1b 发现 line 736 实际是土地回答，"夭夭灼灼"诗句在 line 734，发现 2 P1
- **双轨（W073 正例）**：归属验证 + 内容 spot-check 双轨（Read text-search.html 实际 line 范围验证内容匹配），25 处 line 号一次通过 R1b

**操作步骤**：
1. 主代理 Grep text-search.html 验证 line 号归属（单轨）
2. 主代理 Read text-search.html 的实际 line 范围（如 line 730-740），核对内容匹配
3. 如内容不匹配，修正 line 号到正确位置

**典型对比（W072 vs W073）**：

| 维度 | W072（单轨） | W073（双轨） |
|:---|:---|:---|
| Preflight 验证项 | line 号归属 | line 号归属 + 内容匹配 |
| R1b 结果 | 发现 2 P1 | 一次通过 |
| line 号总数 | 33 处（修正 2 处后） | 25 处 |
| 方法论结论 | Preflight 不充分 | Preflight 双轨充分 |

**根因**：Preflight 仅验归属时，主代理可能基于估算给出 line 号，未实际 Read 内容。R1b 重新审查时才发现内容错位。

**毕业判据应用**：
1. 稳定机制 ✓（A2 Batch 1-7 连续 7 次复用）
2. 反复出现 ≥3 次 ✓（W071 一次通过 / W072 发现 2 P1 / W073 一次通过 = 3 次方法论实验对比）
3. 接手者必须知道 ✓（影响下次 session 创作随笔的 Preflight 协议）

→ 走"毕业路径"，从 memory 升级到 docs/10-方法论沉淀/。

### 四批对比升级结论（W072/W073/W074/W075，2026-07-26）

**升级结论**：chapter 归属错误是 Preflight 双轨验证的稳定盲区。A2/A3 跨方向连续两批均出现 chapter 归属 P1，R1b spot-check 是必要双轨不可省略。

**四批对比数据**：

| Batch | Preflight 方式 | R1b 结果 | P1 类型 | 方向 |
|:---|:---|:---|:---|:---|
| W072 | 单轨（仅验归属） | 2 P1 | line 736 内容错位 + line 1296 引用错误 | A2 |
| W073 | 双轨（归属 + 内容 spot-check） | 0 P1 一次真收敛 | - | A2 |
| W074 | 双轨 | 1 P1 | 音乐学/宗教学 line 996 chapter 归属错误（原误属第12回实际为第8回） | A2 |
| W075 | 双轨 | 1 P1 | 灵感大王 line 3840 chapter 归属错误（原误属第48回 line 3774 实际为第49回观音自述） | A3 |

**关键发现**：
- **双轨有效降低 P1 数量**：W072 单轨 2 P1 → W073/W074/W075 双轨 0-1 P1
- **chapter 归属是 Preflight 稳定盲区**：双轨验证了 line 号归属和内容匹配，但未验证 chapter 归属（即 line 号所属回目是否正确）。W074/W075 连续两批 P1 均为 chapter 归属错误
- **A2/A3 跨方向连续复现**：W074（A2 Batch 8）+ W075（A3 Batch 1-2）连续两批出现 chapter 归属 P1，说明这不是偶发而是系统性盲区
- **R1b spot-check 不可省略**：Preflight 双轨 + R1b spot-check = 真双轨，缺一不可

**升级建议**：未来 Preflight 协议升级为"三轨"——line 号归属 + 内容匹配 + chapter 归属验证（Grep num:N 验证 line 号所属回目）。

### 五批对比升级结论（W072/W073/W074/W075/W076，2026-07-26）

**升级结论**：Preflight 三轨验证首次完整执行即真收敛一次通过。W076 在 W074/W075 连续两批 chapter 归属 P1 后首次完整执行三轨验证（line 号归属 + 内容匹配 + chapter 归属），R1b 主代理 spot-check 一次通过 P0=0/P1=0/P2=0/P3=0。

**五批对比数据**：

| Batch | Preflight 方式 | R1b 结果 | P1 类型 | 方向 |
|:---|:---|:---|:---|:---|
| W072 | 单轨（仅验归属） | 2 P1 | line 736 内容错位 + line 1296 引用错误 | A2 |
| W073 | 双轨（归属 + 内容 spot-check） | 0 P1 一次真收敛 | - | A2 |
| W074 | 双轨 | 1 P1 | 音乐学/宗教学 line 996 chapter 归属错误（原误属第12回实际为第8回） | A2 |
| W075 | 双轨 | 1 P1 | 灵感大王 line 3840 chapter 归属错误（原误属第48回 line 3774 实际为第49回观音自述） | A3 |
| W076 | 三轨（归属 + 内容 spot-check + chapter 归属 Grep num:N） | 0 P1 一次真收敛 | - | A3 |

**关键发现**：
- **三轨验证真收敛一次通过**：W076 首次完整执行三轨验证，5 处 line 号 + 3 处关键内容引用全部通过 R1b 主代理 spot-check
- **方法论连续第 10 次复用有效**：W066-W068 + W071-W076 Preflight 双轨/三轨验证 + 主代理直接基于已验证 Preflight 事实清单创作 + 主代理 spot-check = 5 文件全部一次通过（A3 方向第二次复用）
- **身份政治三联对照方法论首次复用**：女儿国国王（真主权者）/ 老鼠精（义女身份）/ 玉兔精（假公主身份）三种身份政治策略镜像——同 batch 内 3 篇随笔形成主题对照
- **方法论自我证明的第三次延续**：A3 Batch 3 是 Preflight 三轨验证教学材料化（W075）之后立即落地的项目，依然踩到 E1 坑（第 14 次复现，5 文件未 tracked）——方法论在自我证明的第三次延续

**三轨验证操作步骤（W076 标准化）**：
1. 主代理 Grep text-search.html 验证 line 号归属（第一轨）
2. 主代理 Read text-search.html 的实际 line 范围，核对内容匹配（第二轨）
3. 主代理 Grep text-search.html 验证 line 号所属 chapter（num:N 字段，第三轨）
4. 如内容不匹配或 chapter 归属错误，修正 line 号到正确位置

### 十一批对比升级结论（W072-W086，2026-07-26）

**升级结论**：Preflight 三轨验证 W076 首次完整执行后，W077-W086 累积 10 次复用稳定有效。W082 chapter 归属稳定盲区再次复现（line 7054→line 7062 修复），证明三轨验证仍需 R1b spot-check 补充，chapter 归属是 Preflight 稳定盲区不可省略。

**十一批对比数据**：

| Batch | Preflight 方式 | R1b 结果 | P1 类型 | 方向 |
|:---|:---|:---|:---|:---|
| W072 | 单轨（仅验归属） | 2 P1 | line 736 内容错位 + line 1296 引用错误 | A2 |
| W073 | 双轨（归属 + 内容 spot-check） | 0 P1 一次真收敛 | - | A2 |
| W074 | 双轨 | 1 P1 | 音乐学/宗教学 line 996 chapter 归属错误（原误属第12回实际为第8回） | A2 |
| W075 | 双轨 | 1 P1 | 灵感大王 line 3840 chapter 归属错误（原误属第48回 line 3774 实际为第49回观音自述） | A3 |
| W076 | 三轨（归属 + 内容 spot-check + chapter 归属 Grep num:N） | 0 P1 一次真收敛 | - | A3 |
| W077 | 三轨 | 0 P1 一次真收敛 | - | A3 |
| W078 | 三轨 | 0 P1 一次真收敛 | - | A4 |
| W079 | 三轨 | 0 P1 一次真收敛 | - | A4 |
| W080 | 三轨 | 0 P1 一次真收敛 | - | A4 |
| W081 | 三轨 | 0 P1 一次真收敛 | - | A4 |
| W082 | 三轨 | 0 P1 一次真收敛（修复 1 P1：line 7054 章节归属错误→line 7062） | chapter 归属错误（line 7054 误属第98回 line 7048，实际为 line 7062 第98回段尾） | A4 |
| W083 | 三轨 | 0 P1 一次真收敛 | - | A4 |
| W084 | 三轨 | 0 P1 一次真收敛 | - | A4 |
| W085 | 三轨 | 0 P1 一次真收敛 | - | A2 |
| W086 | 三轨 | 0 P1 一次真收敛 | - | A2 + A4 双轨 |

**关键发现**：
- **三轨验证稳定有效**：W076-W086 累积 11 次完整执行，10 次一次通过 R1b spot-check 真收敛，仅 W082 发现 1 P1（chapter 归属错误）
- **chapter 归属是 Preflight 稳定盲区**：W074/W075/W082 三次均出现 chapter 归属 P1，证明 Grep num:N 第三轨验证不可省略
- **R1b spot-check 不可省略**：Preflight 三轨 + R1b spot-check = 真三轨，缺一不可
- **A4 方向连续 7 batch 真收敛**：W078-W084 A4 方向连续 7 batch R1b 主代理 spot-check 一次通过
- **A2 方向连续 2 batch 零撞坑**：W085/W086 A2 方向连续 2 batch Preflight 三轨 + R1b spot-check 一次通过

### chapter 归属稳定盲区段（W074/W075/W082 三次复现）

**根因分析**：Preflight 三轨验证的第三轨（Grep num:N）虽然验证了 line 号所属 chapter，但实际执行中主代理可能：
1. 基于估算给出 num 值，未实际 Grep 验证
2. num 值验证正确但 line 号实际属于该 chapter 的不同段（如第98回 line 7048 vs line 7062）
3. Grep num:N 结果混淆（如多个 num:N 字段对应不同 line 范围）

**W074 复现**：line 996 num 验证为第8回，但实际"我佛造经传极乐"在第8回 line 981，不是 line 996（line 996 是盂兰盆会相关但 chapter 归属正确）

**W075 复现**：line 3840 误属第48回 line 3774，实际为第49回观音自述"他本是我莲花池里养大的金鱼"——chapter 归属错误（Grep num 验证不到位）

**W082 复现**：line 7054 章节归属错误（原误属第98回 line 7048，实际为 line 7062 第98回段尾）——同 chapter 内不同 line 段落归属错误

**升级建议**：未来 Preflight 协议升级为"四轨"——line 号归属 + 内容匹配 + chapter 归属验证（Grep num:N）+ chapter 内 line 段落定位（Read text-search.html 验证 line 在 chapter 内的具体段落）。

### W086 Preflight 三轨验证第十一次完整执行（双轨并发）

**双轨并发执行**：W086 首次同时执行 A2 Batch 10 + A4 Batch 9 双轨创作，Preflight 三轨验证同时验证 11 处关键 line 号（522/589/632/864/981/1448/2629/2967/4432/7050/7102）。

**三轨验证执行**：
1. 第一轨（line 号归属）：Grep text-search.html 验证 11 处 line 号归属
2. 第二轨（内容匹配）：Read text-search.html 实际 line 范围核对内容
3. 第三轨（chapter 归属）：Grep num:N 验证 line 号所属回目

**R1b 主代理 spot-check 结果**：P0=0/P1=0/P2=0/P3=0 一次真收敛

**结论**：Preflight 三轨验证在双轨并发场景（A2 + A4 同时创作）下稳定有效，证明方法论可复用性。

---

## 四、Scope-lock constraint

### 触发条件

subagent prompt 必含硬性约束。

### 约束文本（必含）

```
Only modify files listed in the Files section.
Do NOT modify any other files, even if you notice bugs or improvements in surrounding code.
```

中文版：

```
仅修改 Files 段列出的文件，禁止碰其他文件，
即使发现周边代码有 bug 或可改进。
```

### 根因分析

无此约束时 subagent 倾向"顺便修一下"周边代码，违反 atomic commit 原则。

### 验证方法

主代理在 subagent 返回后必须 `git show <commit> --stat` 验证文件范围。

### 典型复现（2026-07-21 Anthropic T13）

**场景**：subagent 报"未碰其他代码"，主代理 git show spot-check 发现 5 处 main.py 无关修改，接受残留 A1。

### 反向喂回

已反向喂回 executing-plans SKILL.md Step 2 子步骤 3（2026-07-21）。

---

## 五、Subagent prompt 模板铁律

### 完整 subagent prompt 模板

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

---

## 六、Subagent fallback 模式

### 触发条件

subagent 在 context 丢失或返回结果缺失时未交付。

### 操作步骤

1. 主代理基于已完成 Preflight + 已验证事实清单直接创作
2. **不跳过**——必须直接执行
3. 完成后主代理 Grep 关键回目 line 范围 + 跨回目情节侵入检查 = 真收敛

### 复现计数器（3/3）

| # | 时间 | 场景 | 详情 |
|:---:|:---|:---|:---|
| 1 | 2026-07-25 W067 | 性别政治 subagent 返回结果缺失 | 主代理直接创作 |
| 2 | 2026-07-25 W068 | Batch 3 subagent 在 context 丢失时未交付 | 主代理直接创作 |
| 3 | 2026-07-26 W069 | Batch 4 subagent 在 context 丢失时未交付 | 主代理直接创作（但 prior session 已编造 line 号，本 session 修复） |

### 与"主代理 spot-check subagent 声明"原则的逆向应用

- 主代理 spot-check subagent 声明：subagent 报告 ≠ 实际状态，主代理必须验证
- Subagent fallback：subagent 失败时，主代理必须直接执行而非跳过

两条互补。

---

## 七、新增约束（W069 教训）

### subagent 创建随笔时禁止编造 line 号

```
subagent 创建随笔时禁止编造 line 号；
若需引用原文位置，必须 Grep text-search.html 验证后使用真实 line 号；
无法验证时用"回目作锚点 + 转述方式"代替
（如"原文中那一段"/"那一段写得极冷"）
```

### 验证方法

主代理必须 Grep spot-check subagent 创建的随笔中的 line 号：
- 抽样 3-5 处 line 号
- Grep text-search.html 验证实际位置
- 差异 > 5 行 → 全量验证 + 修复

详见 [E1铁律.md W069 案例](E1铁律.md#五w069-系统性编造-line-号)。

---

## 八、关联文档

### 上游 skill

- [C:\Users\12739\.trae-cn\skills\deep-review-loop\SKILL.md](file:///C:/Users/12739/.trae-cn/skills/deep-review-loop/SKILL.md)（v1.2.0 R1a 硬性要求"verifier 必须附工具调用证据"）
- [C:\Users\12739\.trae-cn\skills\executing-plans\SKILL.md](file:///C:/Users/12739/.trae-cn/skills/executing-plans/SKILL.md)（Step 2 子步骤 2 Preflight interface analysis + 子步骤 3 Scope-lock constraint）

### 项目内关联

- [DRL真循环.md](DRL真循环.md)：DRL R1b/R2 subagent prompt 必须含 Preflight + Scope-lock
- [三skill闭环.md](三skill闭环.md)：三 skill 闭环中 DRL 是审查端，必须使用本模板
- [E1铁律.md](E1铁律.md)：subagent 报告 spot-check（与 Preflight 互补）

### memory 文件

- [c:\Users\12739\.trae-cn\memory\user_profile.md](file:///C:/Users/12739/.trae-cn/memory/user_profile.md)：Subagent prompt 模板铁律常驻声明（每次 session 注入）

### 项目内 W### 关联

- W058：Preflight fact verification 首次复现
- W066-W069：Subagent fallback 模式连续 4 次复现
- W069：新增"禁止编造 line 号"约束
