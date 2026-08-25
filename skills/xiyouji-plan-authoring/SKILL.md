---
name: xiyouji-plan-authoring
description: 西游记项目（D:\1\xiyouji）W 批次跨批次路线图方案撰写 playbook。步骤：读上游方案 + DESIGN.md + tokens.css → 实测取证（git HEAD/页数/体量/脚本存在性/覆盖扫描）→ Grep 复核现役最大 W 编号 → 按固定结构（现状基线表/分批计划表/M 指标三段式验收/派生命令清单/裁掉项显式化/统一门禁/风险与依赖/前置探针/待确认项/落地状态回写）成文落 docs/superpowers/plans/YYYY-MM-DD-*.md → wc -l 核验落地 → 启动前三问收尾。当用户要求"写方案"、"路线图"、"roadmap"、"下一阶段计划"、"W 批次方案"、"阶段规划"、"升级方案"、"视觉升级方案"时触发。
version: 1.2.0
---

# 西游记项目 W 批次路线图方案撰写

给 xiyouji 项目（`D:\1\xiyouji`）撰写跨批次路线图/方案文档的固定流程。产出与仓库既有 plan（Phase 3 量化路线图 / Phase E 视觉升级方案）同构，主代理与新接任 Agent 均可逐字复现。核心信条：**先取证、后假设**——方案里每个数字都必须实测，禁止凭记忆或经验编造。

## 何时触发

触发（正向）：

- 用户要求"写方案"、"路线图"、"roadmap"、"下一阶段计划"、"W 批次方案"、"阶段规划"、"升级方案"、"视觉升级方案"。
- 在既有方案基础上衍生新轨（如上游路线图之上再开视觉/工程轨）。

排除（反向）：

- 方案评估/评审（读取+核验+出意见，用 `xiyouji-plan-review`）。
- 单批落地（每批落地时另拆单批 plan/spec，不属本流程）。
- 版本 bump（用 `xiyouji-version-bump`）、论文投稿（用 `xiyouji-s4-submission`）。

## 前置条件

- 项目在 `D:\1\xiyouji`，git 分支 `main`。
- 上游文档：`docs/superpowers/plans/` 最新方案、`DESIGN.md`、`site/tokens.css`（+ `site/system.css`）、`docs/00-导读/` 相关方案。
- 落库目录：`docs/superpowers/plans/`。
- 硬约束（方案不得违反，写进 §0 或正文）：file:// 直开（零外域、字体本地）、CSP 内联哈希、perf-budget（`scripts/output/perf-budget.json`）、动效契约 DESIGN.md §5（≤600ms + RM 双守卫）、EMBEDDED 回退。

## 标准流程（六步）

### 第 1 步：读上游

`ls -t docs/superpowers/plans/` 取最近方案，Read 最新方案 + DESIGN.md + tokens.css + 相关导读方案。记下与目标冲突的现有规范（如 DESIGN.md 明文"无厚重阴影、0-2px 圆角"而方案要加阴影/渐变 → 方案必须含"宪改先行"步骤，否则规范自相矛盾）。

### 第 2 步：Grep 复核现役最大 W 编号

```bash
cd /d/1/xiyouji && grep -oE 'W[0-9]{3}' CHANGELOG.md 交接文档.md docs/superpowers/plans/*.md | sort -u | tail -5
```

取最大值，新批次从其后续编。多 session 并发，禁止凭记忆复用旧编号；**启动前（E0 批次）须再复核一次**防碰撞。

### 第 3 步：实测取证

全部数字现场实测（勿信快照），常用命令速查见 `reference.md` §3，核心：

```bash
cd /d/1/xiyouji && git rev-parse --short HEAD && git status --porcelain | wc -l
cd /d/1/xiyouji && ls site/data/*.html | grep -v _shell | wc -l   # CN 可视化页数
cd /d/1/xiyouji && ls site/en/*.html | wc -l                       # EN 页数
cd /d/1/xiyouji && wc -c site/tokens.css site/system.css           # 体量（体积红线依据）
cd /d/1/xiyouji && ls scripts/<关键脚本>                             # 脚本存在性
cd /d/1/xiyouji && grep -l '<pattern>' site/data/*.html | wc -l    # 覆盖扫描
cd /d/1/xiyouji && cat scripts/output/perf-budget.json && grep -c '<loc>' site/sitemap.xml
```

### 第 4 步：成文（§0-§9 固定结构 + §10 落地状态记录）

按 `reference.md` §1 骨架写：头部元信息块（版本/适用基线【须标注实测 HEAD：`git rev-parse --short HEAD` 实测值】/实测日期/性质/上游依据/目标读者/待确认项）→ §0 现状基线（实测快照表：维度|现值|来源|差距项）→ §1 目标与原则 → §2 维度/阶段拆解 → §3 批次计划（W 号+优先级 P0/P1/P2+交付物+验收【三段式，见下方去模糊化标准①】；条件批标注"待用户确认"）→ §4 工作量与排期 → §5 统一验收门禁（挂 verify_delivery/LHCI/a11y_audit.py，每批必跑）→ §6 风险与依赖 → §7 前置取证（E0 探针清单）→ §8 与既有方案的关系 → §9 待用户确认项（启动前三问）→ §10 落地状态记录（见去模糊化标准④，随执行回写）。

内容三铁律：

1. **宪改先行**：与 DESIGN.md 冲突 → 先列修宪步骤再动手。
2. **体积红线**：tokens/system.css 内联进每一页，+1KB × 全站页数 = 实际增量，须设硬预算并记录 perf-budget。
3. **闸门联动**：上游决策闸门必须映射本轨冻结边界（如"W465 判归档 → 本轨冻结于 E1 完成态"）。

去模糊化成文标准（与三铁律并列，违反即返工）：

1. **验收三段式**：每条验收统一写「指标 = 阈值（测量方法）」，禁止「覆盖率 100%」「结构一致」等不可验表述。主观目标（如"高级感"）须先翻译为代理指标表（M 系列，每条只认数字，如对比度 ≥4.5:1、UI 裸 hex = 0、裸 box-shadow = 0、duration ≤600ms、单页 CSS ≤33KB、LHCI 三指标、pageerror = 0）。铁律：**无测量命令的条款不得写入方案**。
2. **派生命令清单**：页面/文件清单写派生命令（如 `grep -l 'forceSimulation' site/data/*.html`）而非手写名单；执行批次时粘贴命令输出入批次记录表。
3. **裁掉项显式化**：裁掉/挂起项单列清单，每项附理由，避免后续 Agent 当遗漏补做。
4. **落地状态记录（§10）**：方案落库后随执行回写——已执行批次标 ✅ + commit（`git rev-parse --short HEAD`）+ 关键数字；未执行/挂起标 ⏸；与原计划的偏差显式记录（含移入批次，如"图标集移 E5"）。
5. **递增数字引用式（W520 固化）**：随批次演化的计数（门禁数/篇数/页数/skill 数等）在现役状态描述中禁写无时点锚的裸字面量（如"共 22 条门禁"），一律引用式表述（"以 verify_delivery 输出为准""见 README 权威值/统计口径说明"）；确需写快照值必须绑定实测时点与来源（§0 表"现值|来源"列即此语义），使未来漂移可被识别而非误导。**门禁依赖豁免**：verify_delivery 强制 README/STRUCTURE/项目说明/交接文档字面含「A4 209 篇」「共 N 篇」（EXPECT_A4 与 A1-A6 计数门禁解析目标）——此类受门禁保护的现役快照行禁改引用式，属本规则豁免（W519 复盘教训：存量持久文档的门禁数多处滞后成错误指引，且游离于六文档同步契约与计数门禁两道防线之外）。

### 第 5 步：落库核验

Write 到 `docs/superpowers/plans/YYYY-MM-DD-<slug>.md`（日期=当天，slug 英文小写连字符），然后：

```bash
cd /d/1/xiyouji && wc -l docs/superpowers/plans/<新文件> && ls docs/superpowers/plans/
```

声明≠实现，文件必须实际存在。再 Grep 一次 W 编号防并行 session 冲突。

### 第 6 步：汇报（结论先行）

方案定位一句话 + 批次数；关键取舍逐条说明；列出 §9 启动前三问，**等用户确认后再开跑**，不得单方执行。

## 陷阱清单

- **快照失真**：多 session 并发，git 状态/文件数一律现场实测，勿信历史或他 session 快照。
- **W 编号冲突**：编号时与启动前各 Grep 一次现役最大 W。
- **宪改冲突不列步骤**：DESIGN.md 明文限制与方案目标相悖时，方案自相矛盾、无法落地。
- **体积预算漏写**：内联架构下每 KB 增量 × 全站 200+ 页，必须写明预算与折算。
- **闸门冻结不写**：上游决策闸门未映射到本轨冻结边界 → 执行期无依据可停。
- **声明≠实现**：写完不核验 wc -l/ls，文件可能并未落地。
- **验收不可验**：条款无测量命令（如"覆盖率 100%"）→ 违反三段式标准，方案无法验证，必返工。
- **三问不列**：方案必须以"待用户确认项"收尾；启动前三问未答复前不执行。
- **递增数字写死**：门禁数/篇数/页数等裸字面量随批次演化后变误导性陈述（W519 教训），按去模糊化标准⑤用引用式表述根治。

## 完成验证清单

- [ ] 上游方案/DESIGN.md/tokens.css 已读，冲突规范已识别
- [ ] 最大 W 编号已 Grep 复核，新批次编号不冲突
- [ ] §0 基线表全部数字实测且有来源列
- [ ] 版本头含实测基线 HEAD（git rev-parse --short HEAD）+ 实测日期
- [ ] 每条验收均为「指标 = 阈值（测量方法）」三段式，主观目标已译 M 代理指标表
- [ ] 页面清单为派生命令（grep -l <pattern>），裁掉项已单列理由
- [ ] §0-§9 结构完整，含 §5 统一门禁与 §9 三问；§10 落地状态已建表（✅ commit / ⏸ / 偏差行）
- [ ] 文件已落 `docs/superpowers/plans/YYYY-MM-DD-*.md`，wc -l + ls 核验通过
- [ ] 递增数字均为引用式表述或绑定实测时点与来源（去模糊化标准⑤）
- [ ] 已向用户汇报定位/取舍/三问

详细骨架模板、基线表示例、取证命令速查与汇报模板见 `reference.md`。
