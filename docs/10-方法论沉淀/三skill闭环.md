# 三 skill 闭环

> deep-review-loop（审查）→ mem-wrap-up（收尾）→ self-evolution（沉淀）
> 建立时间：2026-07-16
> 当前版本：DRL v1.2.0 + mem-wrap-up v1.1.0 + self-evolution（TRAE 蒸馏版）
> 首次完整执行：2026-07-22 xiyouji 项目
> 最新案例：W086 v2.0.59 三 skill 闭环完整执行（DRL R1b 真收敛 + mem-wrap-up 7 步含 Step 4a/7a 协议升级首次完整实战验证 + self-evolution dim 1/5/9/11 四维度复盘）

---

## 一、问题背景

### 闭环断裂的代价

单 skill 执行无法覆盖完整工作流：
- 只跑 DRL 不收尾 → memory 文件不同步，跨 session 接续失败
- 只跑 mem-wrap-up 不审查 → 修复未落地，假收敛风险
- 只跑 self-evolution 不闭环 → 经验沉淀但未反向喂回 DRL

**典型断裂场景（2026-07-22 首次执行前）**：
- W042 闭环只跑 DRL，未跑 mem-wrap-up + self-evolution
- 跨 session 接续时发现 memory 文件不同步（W069 经验未沉淀到 user_profile）
- 复现 E1 铁律 8 次（跨 session git tracked 未验证）

### 复现计数器

- **闭环断裂**：多次复现，最近 W042
- **严重度**：严重（影响跨 session 接续 + 经验沉淀）

---

## 二、核心方法论

### 闭环方向（严格单向）

```
deep-review-loop（审查端，起点）
    ↓
mem-wrap-up（收尾端，中段）
    ↓
self-evolution（沉淀端，末端）
    ↓
反向喂回 DRL（dim 11 升级 DRL 协议）
```

**禁止反向执行**：self-evolution 不能直接驱动 DRL，必须通过 dim 11 反向喂回 DRL 协议层。

### 三 skill 位置

| Skill | 位置 | 版本 | 角色 |
|:---|:---|:---:|:---|
| deep-review-loop | `C:\Users\12739\.trae-cn\skills\deep-review-loop\SKILL.md` | v1.2.0 | 审查端（起点） |
| mem-wrap-up | `C:\Users\12739\.trae-cn\skills\mem-wrap-up\SKILL.md` | v1.1.0 | 收尾端（中段） |
| self-evolution | `C:\Users\12739\.trae-cn\skills\self-evolution\SKILL.md` | TRAE 蒸馏版 | 沉淀端（末端，反向喂回 DRL） |

---

## 三、正向触发链

### DRL → mem-wrap-up

DRL 收敛后 → 触发 mem-wrap-up Step 7 反向验证收尾本身。

**触发条件**：DRL R3 真收敛（P0=0/P1=0/P2≤N_max + ≥3 residual risk）

### mem-wrap-up → self-evolution

- mem-wrap-up Step 5 sediment → 喂给 self-evolution dim 1 经验复用
- mem-wrap-up Step 2 audit findings → 喂给 self-evolution dim 5 问题预防
- mem-wrap-up Step 4 work-log → 喂给 self-evolution dim 9 一次性工具沉淀

---

## 四、反向触发链

### DRL → self-evolution

- DRL R3 residual risk → 喂给 self-evolution dim 5 问题预防（含 P2 残留经验：按 5Why 处理但标记"接受残留"，不强制升级）
- DRL R1b class-level findings → 喂给 self-evolution dim 9 一次性工具沉淀（P3 由 DRL backlog 兜底，dim 9 不重复；P3 若属 class-level pattern 1 instance 则 DRL 升级为 P2 报告，dim 9 正常接收）

### self-evolution → DRL（反向喂回）

self-evolution dim 11 发现复盘流程撞坑 → 升级 DRL 协议（5 轮细节）。

**反向喂回路径**：
1. self-evolution dim 11 识别反模式（"修完即 OK" / "ad-hoc 加维度不沉淀" / "撞 N 次不主动升 H"）
2. 写入 retrospective.md
3. 下次 DRL 升级时纳入协议层
4. 更新 DRL SKILL.md + bump 版本号

---

## 五、运行时检查规则

### L5 处置：实际触发三 skill 闭环时

验证是否按声明顺序执行（DRL 收敛 → mem-wrap-up Step 7 → self-evolution dim 1/5/9/11）。

**如发现跳过某 skill**：视为闭环断裂，立即补跑被跳过的 skill。

### L1 处置：版本联动检查（动态化）

任一 skill 升级时：
1. 先 Read DRL SKILL.md §0 提取所有以"过拟合防护层 N"开头的条目（动态读取当前版本的全部层定义）
2. 再 Grep `Step [0-9]` + `dim [0-9]+` + `R[0-3]` + 动态提取的层关键词
3. 确认三 skill 间的联动编号 + 4 层防御概念引用未漂移
4. 漂移则同步更新所有 skill 的联动声明

**不硬编码层关键词**：避免未来 4 层升级到 5/6 层时检测规则失效。

### L3 处置：显式声明

新 session 启动时，三 skill 闭环关系常驻 `user_profile.md`（每次都注入 system prompt），无需依赖 skill 内部声明发现闭环。

### L5+L3 处置：当前 session 立即验证原则

修改三 skill / user_profile 后，**当前 session 立即派 subagent 做运行时 self-test**，不把验证推到未来 session。

**理由**：推到未来 = 不确定性累积，当前消除 = 不确定性归零。

**self-test 内容**：
1. 派 1 个 Task subagent 模拟跑 DRL 一轮（给定测试场景：e.g. "批量修复 15 项后跑 DRL"）
2. 验证 subagent prompt 是否真含 4 层防护关键字段
3. subagent 读取 DRL SKILL.md，模拟 R0 项目阶段判定（输出 N_max + 依据）+ R1b 严重度门槛（输出 P3 过滤逻辑）+ R2 边际收益 gate（输出"建议接受残留"格式）+ R3 收敛曲线（按 P2≤N_max 判定）
4. subagent 产出自检报告：4 项是否全部触发 + 触发证据
5. inline me 读取报告，任一项未触发 → 立即修复，不结束当前 session

---

## 六、P2/P3 跨 skill 语义统一

### P2-8 修复（2026-07-21）

| Skill | P2 语义 | P3 语义 |
|:---|:---|:---|
| DRL | 体验问题（记录但不强制修复，允许残留 N 条） | 不报（class-level instance 例外升级 P2） |
| self-evolution | 等用户确认（沿用 DRL 语义） | nice-to-have（只记录，沿用 DRL 语义） |

**行动项优先级对齐**：self-evolution 行动项 P0/P1/P2/P3 优先级与 DRL 收敛判定表对齐：
- P0/P1 必须降到 0
- P2 允许残留 N
- P3 不计入

---

## 七、mem-wrap-up Step 7 DRL 降级判据

### 判据

mem-wrap-up Step 7 调用 DRL 审查 memory 文件时，可降级为 **1-subagent token-budget fallback** 模式；审查代码/HTML 时仍走标准 3-verifier。

### 理由

- memory 文件审查范围窄（通常 2-3 文件）
- 3-verifier token 成本 > 收益
- 代码审查范围广且 P1 风险高，必须 3-verifier

### 复现计数器

- 1/1（2026-07-22 xiyouji F1 Step 7：审查 work-log 60 行 + topics 5 行，降级 a11y-subagent，R1 发现 1 P1 + R2 修复，真收敛）

---

## 八、复现案例

### 案例 1：2026-07-22 首次完整执行

**场景**：xiyouji 项目 B6 R1→R4 后首次跑完整三 skill 闭环。

**执行记录**：
- DRL（B6 R1→R4）：4 轮收敛
- mem-wrap-up（F1 7 步）：memory 健康检查 + audit + work-log + sediment + 4-step verify + Step 7 联动 DRL（降级 1-subagent）
- self-evolution（F2 11 维）：产出 E1（跨 session git tracked 验证）+ E2（文档同步区分历史 vs 现役）2 条高价值经验，已毕业到 user_profile

**结果**：闭环完整执行，2 条高价值经验毕业。

### 案例 2：2026-07-23 v1.0 阶段闭环

**场景**：v1.0 阶段 W020-W024 5 个 DRL 审查全部真收敛后跑闭环。

**执行记录**：
- DRL Phase G（W020-W024）：5 个 DRL 审查全部真收敛
- mem-wrap-up：project_memory 更新 v1.0 状态 + topics 更新
- self-evolution：快速模式，沉淀 v1.0 阶段复利经验

### 案例 3：2026-07-24 W039 闭环

**场景**：W039 神佛体系续扩，发现 prior session 报告"DRL R1b P1 修复已落地"实际未落地。

**执行记录**：
- DRL：发现并修复二郎神.md 未落地 P1 问题
- mem-wrap-up：更新 project_memory v2.0.10→v2.0.12 + work-log + topics
- self-evolution：沉淀 E1 升级版（prior session 报告修复已落地但实际未落地，需 Grep spot-check 文件内容）

详见 [E1铁律.md](E1铁律.md)。

### 案例 4：2026-07-26 W069 闭环

**场景**：W069 A2 Batch 4 创建 4 篇随笔，prior session 系统性编造 27 处 line 号。

**执行记录**：
- DRL R1b：发现 27 P1 系统性 line 号编造
- DRL R2：修复后真收敛（"line XXXX" → "回目作锚点 + 转述"）
- DRL R3：≥3 residual risk + 收敛曲线记录
- mem-wrap-up：memory 健康检查 + work-log 4 段 schema + sediment E1 升级版第 3 次复现到 user_profile
- self-evolution：dim 9 一次性工具沉淀（text-search.html Grep 验证法）+ dim 11 反模式识别（subagent 系统性编造）

### W086 三 skill 闭环执行（2026-07-26·A2 Batch 10 + A4 Batch 9 双轨并发）

**闭环三阶段**：

**阶段 1: DRL 真循环**（审查端·起点）
- R1b 主代理 spot-check 一次通过
- P0=0/P1=0/P2=0/P3=0 真收敛
- 11 处关键 line 号 spot-check 全部通过
- Preflight 三轨验证第十一次完整执行

**阶段 2: mem-wrap-up 7 步流水线**（收尾端·中段）
- Step 1: memory 健康检查
- Step 2: memory audit（5 phase + 6 面状态矩阵）
- Step 3: project_memory.md fileCount sync
- Step 4: 项目层文档同步 work-log 追加
- **Step 4a: 项目层 Grep spot-check（E1 升级版铁律·协议升级首次完整实战验证）**：发现 prior session 报告"6 文件已落地"实际全部停留在 v2.0.58 W085，主代理 Grep spot-check 后派 subagent 串行同步修复，主代理独立 Grep 验证 30 处命中全部通过
- Step 5: sediment 沉淀
- Step 6: -
- Step 7: 反向验证
- **Step 7a: memory 层 Grep spot-check（协议升级首次完整实战验证）**：验证 W086 三件套（work-log/topics/retrospective）W086 段全部存在

**阶段 3: self-evolution**（沉淀端·末端·反向喂回 DRL）
- dim 1 经验复用：W086 预防策略有效（A2 方向连续 2 次零撞坑）
- dim 5 问题预防：Step 4a/7a 协议升级有效性验证
- dim 9 一次性工具沉淀：subagent 串行同步工具
- dim 11 收尾流程撞坑：E1 升级版毕业后首次复现（项目层文档同步维度）

---

## 九、Failure Handling

### 任一步骤失败

任一 skill 失败 → 不继续下一步，stderr 报告。

### Task subagent idle fallback

撞 NEEDS_CONTEXT ≥3 走 fallback prompt（缩小 scope + 给具体 file:line）。

### Token 超额（mem-wrap-up Step 7 R1a 派 3 subagent）

abort 走 3 选 1：
1. 降级为 1 subagent（牺牲 coverage）
2. 分批派（先 factual，再 completeness + reusability）
3. 等 user 拍板（明确放弃 R1a 多视角）

---

## 十、关联文档

### 上游 skill

- [C:\Users\12739\.trae-cn\skills\deep-review-loop\SKILL.md](file:///C:/Users/12739/.trae-cn/skills/deep-review-loop/SKILL.md)
- [C:\Users\12739\.trae-cn\skills\mem-wrap-up\SKILL.md](file:///C:/Users/12739/.trae-cn/skills/mem-wrap-up/SKILL.md)
- [C:\Users\12739\.trae-cn\skills\self-evolution\SKILL.md](file:///C:/Users/12739/.trae-cn/skills/self-evolution/SKILL.md)

### 项目内关联

- [DRL真循环.md](DRL真循环.md)：审查端细节
- [E1铁律.md](E1铁律.md)：跨 session 接续验证（DRL 之前必须验证 prior session 报告）
- [Preflight与Subagent模板.md](Preflight与Subagent模板.md)：DRL R1b/R2 subagent prompt 模板

### 项目内闭环执行记录

- [../../scripts/output/drl-screenshot-review.md](../../scripts/output/drl-screenshot-review.md)：Phase Screenshot Review DRL 收敛记录
- [../../scripts/output/drl-r1-findings.md](../../scripts/output/drl-r1-findings.md)：Phase C v0.9 DRL 收敛记录

### memory 文件

- [c:\Users\12739\.trae-cn\memory\user_profile.md](file:///C:/Users/12739/.trae-cn/memory/user_profile.md)：三 skill 闭环常驻声明（每次 session 注入）
- [c:\Users\12739\.trae-cn\memory\projects\-d-1-xiyouji\project_memory.md](file:///C:/Users/12739/.trae-cn/memory/projects/-d-1-xiyouji/project_memory.md)：项目内三 skill 闭环执行记录

---

## 十一、协议升级联动

### Step 4a/7a 协议升级首次完整实战验证（W086·2026-07-26）

**协议升级背景**：E1 升级版铁律毕业判据满足（W083→W084→W085 3/3 证据累积），驱动 mem-wrap-up SKILL.md 协议升级：
- Step 4a（Line 88-118）：项目层 Grep spot-check 验证 v2.0.X/W### 在 6 文件出现
- Step 7a（Line 155-181）：memory 层 Grep spot-check 验证 W### 在三件套出现
- Line 255：Self-Disclosure E1 升级版 spot-check 已执行声明

**W086 首次完整实战验证三阶段**：
1. **发现**：主代理 Grep spot-check v2.0.59/W086 在 6 文件出现 → 6 文件全部停留在 v2.0.58 W085（命中旧值）
2. **修复**：派 subagent 串行同步 6 文件（避免并行 Edit 竞态·E20 铁律） → 6 文件全部更新为 v2.0.59 W086
3. **验证**：主代理独立 Grep spot-check 30 处命中全部通过

**结论**：Step 4a/7a 协议升级有效——发现 + 修复 + 验证三阶段全部走通，证明 E1 升级版铁律毕业后仍能持续发现新案例并修复。
