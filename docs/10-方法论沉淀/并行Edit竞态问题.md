# 并行 Edit 竞态问题（E20 候选）

> 同一文件的多个 Edit 并行执行时后执行的 Edit 可能基于原始内容覆盖先执行的 Edit 结果，导致前序 Edit 丢失
> 首次复现：2026-07-23 xiyouji
> 当前复现计数器：7/7+ 证据
> 严重度：中等（影响单文件多 Edit 场景的修改完整性）
> 最新案例：W086 v2.0.59 文档同步阶段 subagent 并行 Edit 6 文件同步前 3 文件部分 Edit 丢失

---

## 一、问题背景

### 触发场景

主代理或 subagent 在同一文件上并行执行多个 Edit 操作（例如同时修改 README 头部版本号 + README 中段描述 + README footer 链接）。Edit 工具返回成功，但实际文件中部分修改丢失，仅最后一个写入的 Edit 生效。

### 典型表现

- Edit 工具返回成功（无报错）
- Grep 验证时发现部分修改点未生效
- 重新 Read 文件发现前序 Edit 的修改被覆盖

### 共同根因

Edit 工具无文件级锁，并行 Edit 同一文件时基于同一原始文件内容独立计算 diff，写入时后者覆盖前者，无冲突检测。

---

## 二、核心铁律

### 处置原则

> 同一文件的多个 Edit 必须串行执行；若多行有共同模式，用 `replace_all=true` 一次性处理。

### 当前 session 立即验证原则

> 并行 Edit 同一文件后，必须 Grep 验证所有修改点是否生效，发现丢失立即重新修复。

### 操作步骤

1. **识别同文件多 Edit 场景**：在派 subagent 或主代理自己执行 Edit 前，识别是否会对同一文件做多次 Edit
2. **改并行 → 串行**：同一文件的多个 Edit 必须改为串行执行（一个 Edit 完成后再执行下一个）
3. **replace_all 优先**：若多行有共同模式（如统一替换版本号、统一替换链接前缀），用 `replace_all=true` 一次性处理
4. **Grep 验证**：Edit 完成后 Grep 所有修改点，确认全部生效
5. **发现丢失立即修复**：若 Grep 发现部分修改丢失，立即重新执行该 Edit

### 5Why 根因分析

```
Why 1: 同一文件的多个 Edit 并行执行 →
Why 2: 各 Edit 基于同一原始文件内容独立计算 diff →
Why 3: 各 Edit 写入时无文件级锁 →
Why 4: 后执行的 Edit 基于原始内容覆盖先执行的 Edit 结果 →
Why 5: Edit 工具无冲突检测，前序 Edit 静默丢失

  根本原因：Edit 工具无文件级锁，并行写入无冲突检测
  预防措施：同一文件的多个 Edit 串行执行 + replace_all 优先 + Grep 验证
```

---

## 三、复现计数器（7/7+ 证据）

| # | 时间 | 场景 | 详情 |
|:---:|:---|:---|:---|
| 1 | 2026-07-23 xiyouji | 早期文档同步 | 主代理并行 Edit README 多处修改版本号 + 描述 + footer，Grep 验证发现 footer 修改丢失 |
| 2 | 2026-07-24 xiyouji | STRUCTURE 表格多行更新 | subagent 并行 Edit STRUCTURE 表格 3 行（目录索引 + 版本史 + 当前结构），Grep 验证发现版本史行未生效 |
| 3 | 2026-07-25 xiyouji | CHANGELOG 多段同步 | subagent 并行 Edit CHANGELOG 当前段 + 历史段补遗，Grep 验证发现历史段补遗丢失 |
| 4 | 2026-07-26 xiyouji W070 | 方法论沉淀 6 文件 footer 双索引 | subagent 并行 Edit 6 个方法论文件 footer，Grep 验证发现 2 文件 footer 部分链接丢失 |
| 5 | 2026-07-26 xiyouji W076 | A3 Batch 3 随笔 footer 同步 | subagent 并行 Edit 5 篇随笔 footer 双索引，Grep 验证发现 1 篇 footer W### 反向索引丢失 |
| 6 | 2026-07-26 xiyouji W083 | A4 Batch 6 文档同步 | subagent 并行 Edit 八十一难结构学专题.md 多处（标题 + 描述 + footer），Grep 验证发现描述段修改丢失 |
| 7 | 2026-07-26 xiyouji W086 | 6 文件文档同步 v2.0.59 | subagent 并行 Edit 6 文件同步前 3 文件（README/STRUCTURE/CHANGELOG）部分 Edit 丢失，主代理 Grep spot-check v2.0.59 命中数不足后重新串行修复，最终 30 处命中全部通过 |

### 复现频率声明

7 次为已记录的明确复现案例，实际可能更多（部分早期案例未独立记录到本计数器）。"+" 表示计数器仍在累积，待毕业后纳入 user_profile 常驻铁律。

---

## 四、修复策略

### 三种处置方案

| 方案 | 适用场景 | 操作 | 优点 | 缺点 |
|:---|:---|:---|:---|:---|
| 串行 Edit | 同文件多 Edit 不可合并 | 一个 Edit 完成后再执行下一个 | 100% 避免竞态 | 速度慢 |
| replace_all=true | 多行有共同模式 | 一次 Edit 替换所有匹配 | 速度快 + 无竞态 | 仅适用共同模式 |
| 多文件分发 | 多文件各自单 Edit | 不同文件的 Edit 可并行 | 速度快 + 无竞态 | 仅适用多文件场景 |

### 决策树

```
是否同一文件？
├─ 是 → 是否多行有共同模式？
│       ├─ 是 → 用 replace_all=true 一次性处理
│       └─ 否 → 串行 Edit（一个完成后再执行下一个）
└─ 否 → 不同文件的 Edit 可并行执行（无竞态风险）
```

### 验证流程

1. Edit 完成后立即 Grep 所有修改点
2. 若 Grep 命中数 < 预期 → 立即重新执行丢失的 Edit
3. 重新 Edit 后再次 Grep 验证
4. 直到所有修改点全部命中才视为完成

---

## 五、预防措施

### 派 subagent 时

subagent prompt 必含约束：

```
subagent 执行多 Edit 时：
1. 同一文件的多个 Edit 必须串行执行（一个完成后再执行下一个）
2. 若多行有共同模式，用 replace_all=true 一次性处理
3. Edit 完成后必须 Grep 验证所有修改点是否生效
4. 发现丢失立即重新执行该 Edit
5. 不可基于"Edit 工具返回成功"判断修改已生效，必须 Grep 验证
```

### 主代理自己执行 Edit 时

1. 识别同文件多 Edit 场景，主动改并行 → 串行
2. 优先用 replace_all 处理共同模式
3. Edit 完成后 Grep 验证

### 与 E1 升级版铁律协同

E1 升级版要求"Grep spot-check 验证新值落地"，本铁律补充"并行 Edit 后必须 Grep 验证所有修改点"。两者互补：

| 铁律 | 验证对象 | 触发条件 |
|:---|:---|:---|
| E1 升级版 | prior session 报告"已落地" | prior session 报告 |
| 并行 Edit 竞态（本铁律） | 当前 session 并行 Edit 后的修改完整性 | 当前 session 并行 Edit 同一文件 |

### 与 mem-wrap-up Step 4a 协议升级协同

W086 Step 4a 协议升级首次完整实战验证中，subagent 串行同步 6 文件（避免并行 Edit 竞态·本铁律）+ 主代理独立 Grep 验证 30 处命中全部通过。本铁律是 Step 4a 修复阶段的关键约束。

---

## 六、关联文档

### 项目内关联

- [E1铁律.md](E1铁律.md) §三 E1 升级版：本铁律与 E1 升级版协同（E1 验证"是否落地"，本铁律验证"并行 Edit 后修改完整性"）
- [E2文档同步区分历史vs现役.md](E2文档同步区分历史vs现役.md)：E2 文档同步时若需多 Edit，应用本铁律
- [三skill闭环.md](三skill闭环.md)：mem-wrap-up Step 4a 协议升级中本铁律是修复阶段关键约束
- [Preflight与Subagent模板.md](Preflight与Subagent模板.md)：subagent prompt 模板含本铁律约束

### 上游 skill

- [C:\Users\12739\.trae-cn\skills\mem-wrap-up\SKILL.md](file:///C:/Users/12739/.trae-cn/skills/mem-wrap-up/SKILL.md)（Step 4a 项目层 Grep spot-check·串行 Edit 约束）

### memory 文件

- [c:\Users\12739\.trae-cn\memory\user_profile.md](file:///C:/Users/12739/.trae-cn/memory/user_profile.md)：并行 Edit 竞态铁律常驻声明（候选 E20）
- [c:\Users\12739\.trae-cn\memory\projects\-d-1-xiyouji\project_memory.md](file:///C:/Users/12739/.trae-cn/memory/projects/-d-1-xiyouji/project_memory.md)：项目内复现记录

### 双索引

- 正向时间线：[../../CHANGELOG.md](../../CHANGELOG.md)（W086 v2.0.59 文档同步 6 文件串行 Edit + Grep spot-check 30 处命中全部通过）
- 反向文件索引：[../../scripts/output/file-index.md](../../scripts/output/file-index.md)
- W235 反向索引：W235-S1 方法论沉淀·本文件为第 2 篇（共 4 篇）

---

W235-S1 方法论沉淀·v2.2.41·2026-07-30
