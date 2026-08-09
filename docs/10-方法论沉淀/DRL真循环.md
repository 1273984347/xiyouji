# DRL 真循环

> Deep Review Loop（深度审查循环）方法论沉淀
> 首次训诫：2026-07-12 用户明确训诫
> 升级时间：2026-07-16 4 层过拟合防护
> 当前版本：v1.2.0（含 4 层防护 + R0-R3 完整流程）
> 最新案例：W086 v2.0.59 DRL R1b 主代理 spot-check 真收敛一次通过 P0=0/P1=0/P2=0/P3=0（A2 Batch 10 + A4 Batch 9 双轨并发·Preflight 三轨验证第十一次完整执行）
> 上游 skill：[C:\Users\12739\.trae-cn\skills\deep-review-loop\SKILL.md](file:///C:/Users/12739/.trae-cn/skills/deep-review-loop/SKILL.md)

---

## 一、问题背景

### 假收敛的代价

DRL 不是线性"审查→修复→验证"单次流程。如果只跑 1 路快速审查（如仅 Grep 验证）就判定"0 问题"，下一轮深度审查会反弹——这是严重失误，用户曾因此严厉批评。

**典型假收敛链（W068 第031回 footer 链接）**：
1. R1 审查发现 P1：footer 链接错误
2. R2 修复声明"已落地"
3. R3 Grep 验证未发现新问题（**仅 1 路验证**）
4. R4 深度审查反弹：发现修复实际未落地，prior session Edit 工具静默失败
5. R5 真正修复 + 验证落地

### 复现计数器

- **DRL 假收敛**：多次复现，最近 W069（27 P1 修复后真收敛）
- **严重度**：严重（用户零容忍）

---

## 二、核心方法论

### 真收敛判据

**问题数严格单调递减到 0**，且**下一轮重新审查仍未发现新问题**（如 R9 → R10 均为 0）。

| 状态 | 判据 |
|:---|:---|
| 假收敛 | 1 路快速审查判定 0 问题，下一轮反弹 |
| 真收敛 | 连续 N 轮（N≥2）深度审查均 0 问题 |

### 收敛循环结构

```
审查（R1a 3 verifier + R1b 对抗性）
    ↓
修复（基于 R1b 报告）
    ↓
重新审查（R2 独立审计）← 关键步骤，不可省略
    ↓
确认收敛（R3 残余风险 + 收敛曲线）
    ↓
如未收敛 → 回到审查
```

### 每轮修复后必须重新审查

**修复可能引入回归**（典型：短路子 clause 副作用）。不重新审查就无法发现：
- W068 R7→R8→R9 副作用链：每次修复引入新问题，导致 14.3% 回归率→0%
- W069 27 P1 修复后必须 R2 重新审查，确认 0 回归

---

## 三、4 层过拟合防护

### 层 1：P2 残留 N 规则

P0/P1 必须降到 0；P2 允许残留 N 条；P3 不计入收敛判定，记录到 backlog。

| 项目阶段 | N_max |
|:---|:---:|
| 比赛级 | 0 |
| 生产 | 3 |
| 原型 | 10 |

### 层 2：边际收益 gate

修复成本 > 问题危害 × 3 → 接受残留。

**格式**：`接受残留=P1:A1/P2:A2`，A1>0 才允许 P1 持平，A2>0 才允许 P2 持平。

### 层 3：过拟合警报

震荡 3 轮不单调 / 回归率 >30% → STOP 报告。

**警报 A 例外条款**：边际收益 gate 采纳的残留导致的 P1/P2 持平不触发警报 A。收敛曲线需记录"接受残留=P1:A1/P2:A2"字段作为证据。

### 层 4：严重度门槛

P3 及以下不报。class-level instance 例外升级 P2（一个 pattern 出现 1 instance 就升级，避免类问题被低估）。

---

## 四、R0-R3 完整流程

### R0：surface check

- file size 验证（声称写入的文件实际存在 + 大小合理）
- verdict 字眼 grep（禁词：完成/PASS/12/12/闭环/OK/没问题/looks good）
- 路径验证（声称修改的路径实际存在）

### R1a：3 独立 verifier 交叉验证

派 3 个 Task subagent **并行**，3-lens 审查：

| Lens | 关注 | 输出 |
|:---|:---|:---|
| Factual | 事实是否准确 | P0/P1/P2 findings |
| Completeness | 是否遗漏 | P0/P1/P2 findings |
| Reusability | 是否可复用 | P0/P1/P2 findings |

**硬性要求**（v1.2.0 新增）：
- verifier 必须附工具调用证据
- 目录存在性声明必须附 LS
- 文件存在性声明必须附 Read/LS
- 路径声明必须附 Read
- 0 finding 也要附证据
- Subagent prompt 必含此硬性要求
- 违反处置

### R1b：对抗性 subagent 审查

1 个 Task subagent，**default refuted=true**（默认推翻主代理声明）+ class-level scope + 严重度门槛（层 4）。

### R2：独立审计 + self-revision

1 个 Task subagent，**NOT inline**（不基于主代理上下文）+ 边际收益 gate（层 2）。

**关键**：R2 必须重新审查，不能因为 R1b 报告 0 finding 就跳过。R2 的价值在于：
- 独立视角发现 R1b 漏掉的问题
- 边际收益 gate 评估修复成本 vs 问题危害

### R3：残余风险确认 + 收敛曲线

- ≥3 residual risk（L5 subagent 盲点 / L1 sample-time-point / L3 跨 session）
- 收敛曲线（每轮 P0/P1/P2/P3 数 + 接受残留字段）
- 过拟合警报判定（层 3）

---

## 五、收敛曲线记录要求

每轮问题数必须**单独记录**，标注假收敛/真收敛，不允许只报最终"0 问题"。

### 标准格式

```
| 轮次 | P0 | P1 | P2 | P3 | 状态 |
|:---:|:---:|:---:|:---:|:---:|:---|
| R1a | 0 | 7 | 8 | 0 | 审查 |
| R2  | 0 | 0 | 3 | 0 | 接受残留 A2=3 |
| R3  | 0 | 0 | 0 | 0 | 真收敛 |
```

### 接受残留标注

```
接受残留=P1:A1/P2:A2

A1 = 边际收益 gate 采纳的 P1 残留数
A2 = 边际收益 gate 采纳的 P2 残留数
```

---

## 六、复现案例

### 案例 1：W069 系统性 line 号编造（2026-07-26）

**场景**：W069 A2 Batch 4 创建 4 篇随笔，prior session 系统性编造 27 处 line 号。

**收敛曲线**：
| 轮次 | P0 | P1 | P2 | P3 | 状态 |
|:---:|:---:|:---:|:---:|:---:|:---|
| R1b | 0 | 27 | 0 | 0 | 审查 |
| R2  | 0 | 0 | 0 | 0 | 修复后真收敛 |
| R3  | 0 | 0 | 0 | 0 | 验证无残留 |

**结果**：27 P1 全部修复（"line XXXX" → "回目作锚点 + 转述"），R2 真收敛。详见 [E1铁律.md W069 案例](E1铁律.md#五w069-系统性编造-line-号)。

### 案例 2：Phase F v1.1 W026 docs 5 回内容深化（2026-07-23）

**场景**：5 回内容深化，R1 P1=8/P2=5 → R2 P1=6/P2=7（2 条降级）→ R3 P1=1/P2=2（**假收敛**）→ R4+R5 P1=0/P2=0 真收敛。

**假收敛教训**：R2 修复引入四神标签不一致 + 剖心归属断裂 + 预存章回错误，R3 才发现。回归率 14.3%→0%。

### 案例 3：Phase B v0.8（2026-07-22）

**场景**：v0.8 12 文件改动，R1 P0=0/P1=4/P2=8 → R2 一轮 P1=0/P2=3 → R3 P1=0/P2=3 → R2 二轮 P1=0/P2=0 → R4 真收敛。

**关键**：12→0→3→0→0，0% 回归率。如果不跑 R3 重新审查，会误判 R2 一轮已收敛。

### 案例 4：W070 S1 教学材料化假收敛（2026-07-26）

**场景**：W070 创建 6 篇方法论文件，prior session 报告"R0+R1b+R2 真收敛 P0=0/P1=0/P2=0/P3=0 一次通过"，实际 R2 跨文件链接一致性未发现 4 处 P1。

**收敛曲线**：
| 轮次 | P0 | P1 | P2 | P3 | 状态 |
|:---:|:---:|:---:|:---:|:---:|:---|
| prior R2 | 0 | 0 | 0 | 0 | **假收敛**（声明一次通过） |
| 本次 R1b | 0 | 4 | 0 | 0 | 审查（4 P1 class-level） |
| 本次 R2  | 0 | 0 | 0 | 0 | 修复后真收敛 |

**4 P1 详情**：
1. README.md:50 — 复利经验总览表 E1 跨 session git tracked 仍写 9/9，实际 E1铁律.md 已更新到 10/10（W070 第 10 次复现）
2. 双索引可追溯改造.md:112 — 引用 E1铁律.md "改动后主动影响面扫描"锚点不存在（实际在 user_profile.md E4 毕业经验）
3. 双索引可追溯改造.md:232 — 同 #2
4. 双索引可追溯改造.md:259 — 显示文本承诺"改动后主动影响面扫描"段落，但 E1铁律.md 无此段

**假收敛根因**：prior session R2 声称"6 文件内部跨文件链接 18 处全部解析正确"，实际未 spot-check 锚点真实存在性 + 未同步 E1铁律.md 计数器到 README.md 总览表。

**修复策略**：4 处全部修复（README 9/9→10/10 + 双索引 3 处锚点改为 file:/// user_profile.md 外部链接），R2 验证修复落地 + git tracked 状态 + 链接可达性 = 真收敛。

**讽刺之处**：W070 是 DRL 真循环方法论教学材料化项目，DRL 真循环自身在沉淀过程中再次假收敛——方法论在自我证明。与 E1 铁律第 10 次复现（W070 文件未 git tracked）同属"方法论自我证明"案例。

**教训**：教学材料类任务的 R2 不能只验证"相对路径 + 锚点格式正确"，必须 spot-check 锚点目标真实存在 + 跨文件计数器同步（如 E1铁律.md 计数器 10/10 vs README.md 总览表 9/9）。

### 案例 5：W086 v2.0.59 DRL R1b 真收敛（A2 Batch 10 + A4 Batch 9 双轨并发·2026-07-26）

**场景**：W086 v2.0.59 双轨创作——A2 Batch 10 物理学/认知科学/演化论 3 篇随笔 + A4 Batch 9 经济学专题 1 篇。

**DRL R1b 主代理 spot-check 执行**：
- Preflight 三轨验证第十一次完整执行（line 号归属 + 内容匹配 + chapter 归属）
- 11 处关键 line 号 spot-check（522/589/632/864/981/1448/2629/2967/4432/7050/7102）
- 关联文档链接真实性核查

**结果**：P0=0/P1=0/P2=0/P3=0 一次真收敛（无需 R2 修复）

**方法论意义**：
- 双轨并发场景下 DRL R1b 真收敛证明方法论可复用性
- Preflight 三轨验证稳定有效（W076-W086 累积 11 次完整执行，10 次一次通过）
- 与 W085 共同证明 A2 方向连续 2 次零撞坑

---

## 七、修复策略

### 7.1 修复前 Preflight

派 subagent 修复前，主代理必须：
1. **Preflight fact verification**：Grep 验证关键事实（人物关系/法宝归属/事件顺序）
2. **Scope-lock constraint**：subagent prompt 必含"仅修改 Files 段列出文件"约束

详见 [Preflight与Subagent模板.md](Preflight与Subagent模板.md)。

### 7.2 修复后验证（三件套）

| 验证项 | 工具 | 通过判据 |
|:---|:---|:---|
| JS 语法 | RunCommand `node -c file.js` | 0 syntax error |
| Grep 落地 | Grep 修复后的值 | 全部命中 |
| zip 重新打包 | RunCommand `Compress-Archive` | 包含修复后文件 |

### 7.3 修复后必跑 R2 重新审查

修复后不能直接 R3，必须跑 R2 独立审计（NOT inline + 边际收益 gate）。R2 的价值：
- 发现修复引入的回归
- 评估修复成本 vs 问题危害（边际收益 gate）

---

## 八、Verdict 字眼禁令

DRL 报告中**禁用**以下字眼：

```
完成 | PASS | 12/12 | 闭环 | OK | 没问题 | looks good
```

**替换为**：
- "完成" → "P0=0 P1=0 P2=0 三零达成"
- "PASS" → 列具体数据 + 实证
- "闭环" → 列收敛曲线 + residual risk
- "OK" → 列具体验证命令 + 输出

---

## 九、关联文档

### 上游 skill

- [C:\Users\12739\.trae-cn\skills\deep-review-loop\SKILL.md](file:///C:/Users/12739/.trae-cn/skills/deep-review-loop/SKILL.md)（v1.2.0 协议层）

### 项目内关联

- [三skill闭环.md](三skill闭环.md)：DRL 在三 skill 闭环中的位置（审查端）
- [E1铁律.md](E1铁律.md)：DRL R1b/R2 subagent 报告 spot-check
- [Preflight与Subagent模板.md](Preflight与Subagent模板.md)：DRL R1b/R2 subagent prompt 模板
- [../../CHANGELOG.md](../../CHANGELOG.md)：每个 W### 的 DRL 收敛记录

### 项目内 DRL 历史记录

- [../../scripts/output/drl-screenshot-review.md](../../scripts/output/drl-screenshot-review.md)：Phase Screenshot Review 收敛记录
- [../../scripts/output/drl-r1-findings.md](../../scripts/output/drl-r1-findings.md)：Phase C v0.9 收敛记录

### mem-wrap-up Step 4a/7a 协议联动

- **Step 4a 项目层 Grep spot-check**：DRL 收敛后，mem-wrap-up Step 4a 协议升级首次完整实战验证发现 W086 prior session 报告"6 文件已落地"实际全部停留在 v2.0.58 W085，主代理 Grep spot-check 后派 subagent 串行同步修复（详见 [E1铁律.md](E1铁律.md) row 7 + 毕业后处置段）
- **Step 7a memory 层 Grep spot-check**：DRL 收敛后，mem-wrap-up Step 7a 协议升级验证 W086 三件套（work-log/topics/retrospective）W086 段全部存在
- **联动声明**：DRL R1b 主代理 spot-check + mem-wrap-up Step 4a/7a = 完整三阶段验证（DRL 内容审查 + 项目层文档落地验证 + memory 层落地验证），任一阶段不可省略

---

## 十、维护规则

1. **复现案例追加**：每次 DRL 假收敛复现必须追加到第六节案例表
2. **收敛曲线记录**：每个 W### 的 DRL 收敛曲线必须记录到 CHANGELOG W### 段
3. **不修改上游 skill**：本文件只记录项目内案例，skill 协议升级走 skill 文件
4. **关联到 W### ID**：每条案例必须关联到首次出现的 W### ID
