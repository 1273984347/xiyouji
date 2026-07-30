# Subagent 工具证据不可盲信铁律

> DRL R1b/R2 subagent 可能产生幻觉，其 prompt 虽要求附工具调用证据，但证据本身仍可能被误读。主代理在关键路径/声明上必须执行直接 Read/LS/Grep 验证，不可仅因 subagent 报告"0 finding"或"已验证"就采信
> 首次复现：2026-07-19 xiyouji
> 当前复现计数器：多次（2026-07-19 首次 + 2026-07-21 E14 补充）
> 严重度：严重（影响关键路径决策 + subagent 报告可信度）
> 最新案例：2026-07-21 E14 第二次复现（ripgrep 跳过二进制文件导致 subagent 误判 baichuan2-technical-report.md + cais/paper.md 无 ## 中文翻译 标注）

---

## 一、问题背景

### 触发场景

DRL R1b/R2 subagent 报告以下声明时，主代理不可盲信：
- "已保护 X 不受影响"
- "未找到 X"
- "0 finding"
- "已验证 X"

subagent 的 prompt 虽要求附工具调用证据，但证据本身仍可能被误读。典型场景：subagent 基于 ripgrep 结果误判（ripgrep 检测到 NUL 字节后跳过二进制文件，返回"binary file matches"不显示具体行），从而报告"未找到 X"，实际 X 在二进制文件中存在。

### 典型复现：ripgrep 跳过二进制文件

**场景（2026-07-21 E14 第二次复现）**：DRL R1a 3 verifier 均报告 baichuan2-technical-report.md + cais/paper.md 无 `## 中文翻译` 标注（P1 finding）。

**主代理 spot-check**：用 Python 脚本读取 PDF 二进制文件末尾字节，确认标注存在（字节 2057954 / 3159768），推翻 subagent 误判。

**根因**：ripgrep 检测到 NUL 字节后跳过二进制文件（返回"binary file matches"不显示具体行），subagent 基于 ripgrep 结果误判"未找到"。

### 共同根因

subagent 报告 ≠ 实际状态。subagent 的工具调用证据可能：
- 基于二进制文件被 ripgrep 跳过的结果误判
- 基于部分匹配结果的过度概括
- 基于上下文不足的语义误读

---

## 二、核心铁律

### 不可盲信声明清单

> 主代理在以下 subagent 声明上必须执行独立工具调用 spot-check：
> - "已保护 X 不受影响" → 用 Grep/Read 验证 X 是否确实未变
> - "未找到 X" → 用 Python 脚本/Grep 范围限定/Read 验证 X 是否真的不存在
> - "0 finding" → 用独立 Grep 验证关键声明
> - "已验证 X" → 用独立工具调用验证

### E14 子类：二进制文件 ripgrep 跳过

subagent 报告中"已保护 X 不受影响"/"未找到 X"的声明，主代理必须用独立工具调用（Python 脚本统计字符 / Grep 范围限定）spot-check。

**根因**：ripgrep 检测到 NUL 字节后跳过二进制文件（返回"binary file matches"不显示具体行），subagent 基于 ripgrep 结果误判。

### 操作步骤

1. **识别关键路径声明**：subagent 报告中的"已保护/未找到/0 finding/已验证"等声明
2. **选择独立工具**：Python 脚本（二进制文件）/ Grep 范围限定（上下文验证）/ Read（直接读取）
3. **执行 spot-check**：用独立工具调用验证声明真实性
4. **发现误判立即纠正**：若 spot-check 发现 subagent 误判，立即纠正并重新执行相关步骤

### 5Why 根因分析

```
Why 1: subagent 报告"未找到 X" →
Why 2: subagent 基于 ripgrep 结果判断 →
Why 3: ripgrep 检测到 NUL 字节后跳过二进制文件 →
Why 4: ripgrep 返回"binary file matches"不显示具体行 →
Why 5: subagent 误判"未找到 X"，实际 X 在二进制文件中存在

  根本原因：subagent 工具调用证据可能被误读（ripgrep 跳过二进制文件是典型场景）
  预防措施：主代理在关键路径声明上必须执行独立工具调用 spot-check
```

---

## 三、复现计数器（多次）

| # | 时间 | 场景 | 详情 |
|:---:|:---|:---|:---|
| 1 | 2026-07-19 xiyouji 首次 | DRL R1b subagent 报告"0 finding" | 主代理 spot-check 发现 subagent 漏报 P1 finding，subagent 报告"0 finding"实际存在多处问题 |
| 2 | 2026-07-21 xiyouji E14 第二次复现 | DRL R1a 3 verifier 均报告 baichuan2-technical-report.md + cais/paper.md 无 `## 中文翻译` 标注 | 主代理用 Python 脚本读取 PDF 二进制文件末尾字节，确认标注存在（字节 2057954 / 3159768），推翻 subagent 误判。**根因**：ripgrep 检测到 NUL 字节后跳过二进制文件 |
| 3+ | 多次（详见 user_profile.md 对应条目） | 多个 DRL R1b/R2 subagent 报告场景 | 详见 user_profile.md "Subagent 工具证据不可盲信" 段 |

### 复现频率声明

"多次"表示已记录的复现案例不止 2 次，但部分早期案例未独立记录到本计数器（详见 user_profile.md 对应条目）。本铁律已纳入 E1 铁律 §四 作为 L3 spot-check 层级，详见 [E1铁律.md](E1铁律.md) §四。

---

## 四、修复策略

### 三种独立工具调用 spot-check

| 工具 | 适用场景 | 操作 | 优点 |
|:---|:---|:---|:---|
| Python 脚本 | 二进制文件（PDF/图片等） | 读取文件字节，统计字符出现位置 | 不受 ripgrep 二进制跳过影响 |
| Grep 范围限定 | 文本文件上下文验证 | `Grep "X" -A N -B N` 验证上下文 | 验证匹配是否在预期上下文 |
| Read | 关键文件直接读取 | 直接 Read 文件相关行 | 100% 准确，但仅适用小范围 |

### 决策树

```
subagent 报告声明类型？
├─ "未找到 X" + X 可能在二进制文件 → Python 脚本读取字节验证
├─ "未找到 X" + X 在文本文件 → Grep 范围限定验证
├─ "已保护 X 不受影响" → Grep 验证 X 是否确实未变
├─ "0 finding" → Grep 验证关键声明
└─ "已验证 X" → Read 关键文件相关行
```

### 典型案例处置（2026-07-21 E14）

| 步骤 | 动作 | 结果 |
|:---:|:---|:---|
| 1 | subagent 报告"无 `## 中文翻译` 标注" | 3 verifier 均报告 |
| 2 | 主代理识别为关键路径声明 | 触发 spot-check |
| 3 | Python 脚本读取 PDF 二进制文件末尾字节 | 字节 2057954 / 3159768 处确认标注存在 |
| 4 | 推翻 subagent 误判 | 标注实际存在，subagent 漏报 |
| 5 | 纠正 P1 finding | 标注实际存在，P1 finding 不成立 |

---

## 五、预防措施

### 派 subagent 时

subagent prompt 必含约束：

```
subagent 报告"未找到 X"时：
1. 必须明确说明搜索范围（哪些文件 / 哪些行范围）
2. 必须明确说明使用的工具（Grep / Read / Python 脚本）
3. 若搜索二进制文件，必须用 Python 脚本而非 ripgrep
4. 报告"0 finding"时必须附完整搜索证据（搜索命令 + 命中数）
5. 不可基于 ripgrep "binary file matches" 结果判断"未找到"
```

### 主代理自己执行 spot-check 时

1. **关键路径声明必 spot-check**：subagent 报告中"已保护/未找到/0 finding/已验证"等声明
2. **二进制文件必用 Python 脚本**：不可依赖 ripgrep
3. **spot-check 后再决策**：未 spot-check 不可基于 subagent 报告做关键路径决策

### 与 E1 铁律 L3 层级协同

E1 铁律 §四 已将本铁律纳入 L3 spot-check 层级：

| 层级 | 验证对象 | 工具 | 触发条件 |
|:---|:---|:---|:---|
| L1 | git tracked 状态 | `git ls-files <file>` | prior session 报告"edits made" |
| L2 | 文件内容修复落地 | `Grep "修复后的值"` | prior session 报告"修复已落地" |
| L3 | subagent 报告真实性 | Python 脚本 / Grep 范围限定 / Read | subagent 报告"已保护/未找到" |

本铁律即 L3 层级的具体化。

### 与 DRL 真循环协同

DRL R1b/R2 subagent spot-check 是本铁律的下游应用。DRL R1a 3 verifier 均报告同一 P1 finding 时，主代理必须独立 spot-check 验证（不可因"3 verifier 一致"就采信）。

---

## 六、关联文档

### 项目内关联

- [E1铁律.md](E1铁律.md) §四 Subagent 工具证据不可盲信：本铁律是 E1 铁律 §四 的独立铁律化（L3 层级具体化）
- [DRL真循环.md](DRL真循环.md)：DRL R1b/R2 subagent spot-check 是本铁律的下游应用
- [Preflight与Subagent模板.md](Preflight与Subagent模板.md)：subagent prompt 模板含本铁律约束（禁止盲信 ripgrep 二进制跳过结果）
- [三skill闭环.md](三skill闭环.md)：DRL 真循环是三 skill 闭环的第一环，本铁律在 DRL 阶段执行

### 上游 skill

- [C:\Users\12739\.trae-cn\skills\deep-review-loop\SKILL.md](file:///C:/Users/12739/.trae-cn/skills/deep-review-loop/SKILL.md)（v1.2.0 R1a 硬性要求"verifier 必须附工具调用证据"·本铁律补充"证据本身仍需主代理 spot-check"）

### memory 文件

- [c:\Users\12739\.trae-cn\memory\user_profile.md](file:///C:/Users/12739/.trae-cn/memory/user_profile.md)：Subagent 工具证据不可盲信铁律常驻声明（每次 session 注入）
- [c:\Users\12739\.trae-cn\memory\projects\-d-1-xiyouji\project_memory.md](file:///C:/Users/12739/.trae-cn/memory/projects/-d-1-xiyouji/project_memory.md)：项目内复现记录（2026-07-19 首次 + 2026-07-21 E14 补充）

### 双索引

- 正向时间线：[../../CHANGELOG.md](../../CHANGELOG.md)（2026-07-19 首次复现 + 2026-07-21 E14 第二次复现 ripgrep 跳过二进制文件）
- 反向文件索引：[../../scripts/output/file-index.md](../../scripts/output/file-index.md)
- W235 反向索引：W235-S1 方法论沉淀·本文件为第 3 篇（共 4 篇）

---

W235-S1 方法论沉淀·v2.2.41·2026-07-30
