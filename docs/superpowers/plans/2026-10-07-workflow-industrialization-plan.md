# 动态 Workflow 工业化方案（Workflow Industrialization Plan · V1.0）

> **头五要素**
> - **版本**：V1.0（首发）
> - **日期**：2026-10-07
> - **来源**：ZCode session 2026-10-07 全仓实测扫描（取证方法与覆盖面见附录 A）
> - **状态**：已批准开工（2026-10-07 用户令「开工」）——WF-1 前置 WP-1.0 已落地并入本批 W679（对账表现势），WF-1 主跑阻断于 P0-1（用户凭证，见 §5.6 执行记录）；WF-2 随站点质量批次四（W676）启用；WF-3/WF-4 建议建置（周期型）；WF-5 事件驱动按需建置；WF-6 仅登记触发条件不建置
> - **读者**：执行 Agent（跨 session）/ 项目维护者。本文自包含：执行所需的全部事实、命令、判据、运行时契约均在本文件内，无需回看任何会话历史。
>
> 生成来源：人工撰写（Agent 起草·2026-10-07 全仓实测扫描）·生成模型：GLM（ZCode session 2026-10-07）·生成日期：2026-10-07·核验状态：已核验（§二全部基线数字为 2026-10-07 当日命令实测，取证命令逐条列出；动态 workflow 运行时契约引自 zcode 官方 dynamic-workflows skill 权威文本，见附录 B）
>
> **本文件当前 untracked。入库方式二选一：随批次四（W676）顺带提交，或动工批自行认领 W 号提交（§十一）。已按第 18 门禁（元信息块 v2）要求携带血缘 4 字段。**

---

## 一、目的与范围

### 1.1 目的

把本仓库已识别的 6 类「多子代理扇出 + 类型化产出」工作，固化为可保存（`.zcode/workflows/*.dwf.ts`）、可重跑、可修订（AmendWorkflow 缓存复用）的动态 workflow，替代当前「主 agent 手工逐个派发子代理」的做法，压缩取证/修复产出段的墙钟时间。

### 1.2 范围内

- WF-1 Agent 黄金评估集 LLM 基线（`xiyouji-agent-web/evals/`，W598 建置后 0 次执行）
- WF-2 批次修复扇出（站点质量批次四~六 W676-W678 方案档 §十四扇出矩阵的执行载体）
- WF-3 存量冻结基线抽查（8 份基线只拦新增、存量零抽查的缺口）
- WF-4 复盘报告取证包（docs/10-方法论沉淀/ 已有 11 份复盘报告的重复取证劳动）
- WF-5 外部输入逐条裁决（W634 外部路线图 40+ 提案、九轮外部审查的裁决流水线化）
- WF-6 触发条件登记（不建置，写死启动条件防误启动）

### 1.3 范围外（明确不做，防误用）

| 不做的工作 | 原因（可判定） |
|---|---|
| 37 道门禁、`verify_delivery.py`、`check_*` 家族 | 确定性单进程 Python/JS 脚本，执行时间以秒计，workflow 化零收益 |
| `batch_cascade.py` 级联、`inline_css.py --force`、`generate_csp.py` | 同上，且属共享可变状态的串行链（铁律：同文件 Edit 串行） |
| git 提交/推送/CHANGELOG 维护 | workflow 脚本无 git 写能力（world.run 命令集在提交确认时冻结，提交链必须主 context 串行拥有） |
| Playwright e2e、截图采集、`_audit_render_states.js` 暗色审计 | 已是机器脚本且自带并发 worker（`--conc` 参数），代理扇出无增量 |
| 周期性体检（每日 make ci / gh run list / GoatCounter 数据采集） | 属定时自动化（cron 调度固定命令），不是多代理编排；用宿主定时任务实现，本文 WF-6 登记 |
| hardships 重分类、B-8 口径类数据语义变更 | 作者裁决惯例：登记不直改（W651/W668 已裁决），任何 workflow 无权代裁 |

---

## 二、事实基线（2026-10-07 实测，HEAD = ffaa9e4，branch main，现役 v2.3.272 W675）

以下全部数字为 2026-10-07 当日实测，取证命令随行。**执行批动工时须按 §4.9「数字当批现测」重跑本表命令并以当日值为准**（本表数字仅证明方案落笔日的状态）。

| # | 对象 | 实测值 | 取证命令 |
|---|---|---|---|
| B1 | 评估用例数 | 50 行 | `wc -l xiyouji-agent-web/evals/golden-50.jsonl` → `50` |
| B2 | 用例 schema | 6 字段：`id`/`category`/`question`/`expect_source_paths`/`must_mention`/`forbid` | `head -1 xiyouji-agent-web/evals/golden-50.jsonl` |
| B3 | 评估运行器三模式 | `--self-check`（判分器自检 4 用例·无 LLM）/ `--limit N`（前 N 条真跑）/ 全量 50 条真跑 | `head -10 xiyouji-agent-web/evals/run_eval.mjs` |
| B4 | 机判三规则 | ① 回答含全部 `expect_source_path` 且路径磁盘存在（`/`与`\`均认可）② `must_mention` 全命中 ③ `forbid` 零命中 | run_eval.mjs `judge()` 函数（L28-37） |
| B5 | 基线规则 | 首跑仅建基线不设阈值；连续两批 score 下降 ≥10 个百分点为回归告警 | run_eval.mjs L7 注释 |
| B6 | **run_eval.mjs 无 .env 加载** | 全 94 行无 `process.env`/`dotenv` 读取；L6 注释声称「需 .env CODEBUDDY_API_KEY」但脚本不自读——密钥必须由 shell 环境注入，否则 SDK 鉴权必失败 | `grep -c "process.env\|dotenv" xiyouji-agent-web/evals/run_eval.mjs` → `0` |
| B7 | **密钥文件缺失** | `xiyouji-agent-web/.env` 不存在 | `test -f xiyouji-agent-web/.env && echo exists \|\| echo missing` → `missing` |
| B8 | SDK 在位 | `@tencent-ai/agent-sdk` 已安装 | `test -d xiyouji-agent-web/node_modules/@tencent-ai/agent-sdk` → 0（存在） |
| B9 | 评估结果历史 | **0 份**（LLM 基线自 W598 建置起从未执行） | `ls xiyouji-agent-web/evals/results-*.json` → 无匹配 |
| B10 | frontmatter 基线 | 611 行（冻结存量豁免） | `wc -l scripts/output/frontmatter-baseline.txt` → `611` |
| B11 | 术语基线 | 383 行 | `wc -l scripts/output/glossary-baseline.txt` → `383` |
| B12 | 内容一致性基线 | 84 行 | `wc -l scripts/content-consistency-baseline.txt` → `84` |
| B13 | 可引用性基线 | 349 行 | `wc -l scripts/output/citability-baseline.txt` → `349` |
| B14 | 色盲安全基线 | 17431 行 | `wc -l scripts/output/colorblind-baseline.txt` → `17431` |
| B15 | 渲染状态审计基线 | 784 行 | `wc -l scripts/output/render-state-audit-baseline.jsonl` → `784` |
| B16 | 合同冒烟基线 | 163 行 | `wc -l scripts/output/contract-smoke-baseline.jsonl` → `163` |
| B17 | A1–A6 目录计数 | 101/45/216/210/35/14 = 621 个 .md（每目录含 1 个非内容文件，内容口径 615） | `for d in docs/0{1,2,3,4,5,6}-*; do find "$d" -maxdepth 1 -name '*.md' \| wc -l; done` |
| B18 | docs 全树 .md | 891 个（< files.glob 2000 上限，可单次枚举） | `find docs -name "*.md" \| wc -l` → `891` |
| B19 | 可视化页 | site/data/ 87 个 HTML（86 可视化 + _shell.html） | `ls site/data/*.html \| wc -l` → `87` |
| B20 | 英文站 | site/en/ 140 个 HTML（登记口径 138 页 + 2） | `ls site/en \| wc -l` → `140` |
| B21 | EN 数据副本 | site/en/json/ 恰 7 个 JSON（W627「七副本」实证） | `ls site/en/json/ \| wc -l` → `7` |
| B22 | i18n 工具链 | 生成器 `scripts/_w627_gen_en_data.py`、对账器 `scripts/_check_en_json_parity.py`（均 `_` 前缀=一次性脚本） | `ls scripts/ \| grep -i "en_data\|parity"` |
| B23 | dataset 真源 | 43 个 JSON | `ls dataset/*.json \| wc -l` → `43` |
| B24 | 生成器输出 | scripts/output/data/ 135 个 JSON | `ls scripts/output/data/*.json \| wc -l` → `135` |
| B25 | 对账表现势 | 下一自由号 = W676（站点质量批次四拟用；批次四~六顺延 W676-W678） | `sed -n '10,12p' docs/00-导读/W批次编号对账表.md` |
| B26 | 复盘报告存量 | 11 份（9 份工作复盘：09-05/09-06/09-08/09-13/09-16/10-01/10-04/10-05/10-06 + 白屏三连根因复盘 + 读者数据复盘） | `ls docs/10-方法论沉淀/ \| grep -c 复盘` → `11` |
| B27 | 最新复盘模板结构 | 11 个二级标题（执行摘要/一 信息基础与假设/二 经验复用梳理/三 技能优化评估与 skill-creator 任务卡/四 未用技能审视/五 场景沉淀识别/六 问题与预防机制/七 工作流优化方案/八 问题总结与计划制定/九 方案可行性自评/附录 A 量化数据表/附录 B 编号与术语） | `grep -c "^## " docs/10-方法论沉淀/工作复盘与优化分析报告-2026-10-06.md` → `12`（含「目录」） |
| B28 | 批次扇出矩阵 | 方案档 §十四：批次四 6 lane / 批次五 4 lane / 批次六 3 lane；并发 ≤4；subagent 只读+产出补丁不落盘 | docs/superpowers/plans/2026-10-05-site-quality-remediation-plans.md:337 |
| B29 | 外部裁决先例 | W634 外部路线图裁决（docs/superpowers/plans/2026-09-30-maintenance-backlog-registry.md）；九轮外部审查裁决（同方案档 §十） | 文件存在性 |
| B30 | 保存的 workflow | 0 个（`.zcode/workflows/` 为空目录） | `ListSavedWorkflows` → count=0 |
| B31 | `.zcode/` 可入库 | `.zcode/workflows/` 不在 .gitignore（仅 `.zcodeignore` 一条无关规则），保存的 workflow 定义可 git track | `git check-ignore -v .zcode/workflows/x` → 无匹配 |

---

## 三、运行时硬约束（全部 workflow 共同遵守）

### 3.1 动态 workflow 运行时契约（速查全文见附录 B）

1. 脚本为 strict TypeScript：禁 `import`/`export`/`declare`、禁 `Date.now()`/`Math.random()`/`fetch`/`fs`。
2. `world.run(cmd, args)` 的 `cmd` 必须是编译期字面量（提交确认时向用户展示完整命令集）；运行期值只能进 `args` 数组。默认超时 300000ms，用 `timeoutMs` 覆盖。非零 exit code 是返回值不是异常。
3. `files.glob` 上限 2000 文件、`files.grep` 上限 2000 命中/256KB——超限**拒绝而非截断**。
4. `report()` 每次运行上限 256 条、单条 32KB、仅 JSON 可序列化。**随产随报**（中途失败已产出项仍可送达）。
5. `phase()` 必须覆盖全脚本；phase 名为编译期字面量、面向用户可读中文；每个 phase 至少含 1 个 `ask` 或 1 个 `world.run`。
6. 子代理名在单次运行内唯一（缓存键）；`agent()` 在循环/扇出内禁止字面量重名。
7. 修订一律 `AmendWorkflow`（编辑脚本文件后传 `path`），禁止重写；缓存命中条件=子代理名稳定 + ask 文本逐字节相同；首个活写入（或活 world.run）后缓存失效。
8. 最终 `return` 用 `WorkflowReport` 形状：`{conclusion, findings, verified, notCovered}`，四字段全部中文。
9. 子代理每 ask 至多 3 次 escalation；provider 侧错误由运行时无限重试，脚本禁写重试循环。

### 3.2 项目级纪律（本方案即用户批准载体）

1. **workflow 不拥有提交链**：所有 workflow 的产出是类型化结果/补丁 diff；应用补丁、`generate_csp.py`、`inline_css.py --force`、`batch_cascade.py`、六文档同步、`git commit/push` 全部由主 context 串行执行。
2. **文件独占**：同一文件同一时间仅一个 writer；扇出任务按文件分组，跨任务触碰同文件时合并为一个子代理（沿用方案档 §十四总原则 1）。
3. **禁触清单**（所有 workflow 的子代理 persona 中显式写入）：`site/tokens.css`、`site/system.css`、`scripts/verify_delivery.py`、`dataset/` 生成器、`docs/00-导读/` 治理文档、CHANGELOG 历史段、归档 3 份、`.env`。
4. **并发上限**：WF-2 显式 `max_concurrency: 4`（方案档 §十四总原则 3，源自在仓 judge 并发限额浮动经验）；其余 workflow 由运行时自适应，不设上限。
5. **禁随机数 → 等距抽样规约**：运行时禁 `Math.random()`，凡需抽样一律用确定性等距取样——目标集合经 `files.glob` 取得（字典序已排序），`stride = floor(N / n)`，取索引 `0, stride, 2×stride, …`（共 n 个）。任何 session 按同一算法复算得同一集合。
6. **W 号认领**：每个 workflow 首次实战即一个 W 批次，动工前在 `docs/00-导读/W批次编号对账表.md` 登记认领；取号 = 当日对账表 `max(W#)+1`，且避开 W676-W678（站点质量批次四~六预留，对账表 B25 行现势）。
7. **表述纪律**：本方案及其派生的所有 ask/验收句遵守文档规范 §4.9——禁「适当/尽快/酌情/相关/必要时/尽量」，量化必带单位与比较符，验收必含命令 + 可复算判据。
8. **保存入库**：每个 workflow 首跑验收全绿后，经用户确认方调 `SaveWorkflow` 存入 `.zcode/workflows/`（project scope，B31 已证可 tracked）；未经确认不保存。

---

## 四、工作流总览

| 编号 | 保存名 | 形态 | 扇出单元 | 主要产出 | W 号关系 | 优先级 |
|---|---|---|---|---|---|---|
| WF-1 | `evals-llm-baseline` | 一次性建基线 | 50 用例 → 10 个判分组（组内共享上下文×5 用例，组间独立） | `evals/results-<日期>.json`（机判）+ 语义判读报告（artifact） | 自行认领（预期 ≥W679，动工日以对账表为准） | **建议开工**（W598 唯一遗留待执行项） |
| WF-2 | `batch-fix-fanout` | 每批次参数化重跑 | 方案档 §十四 lane（批次四 6 / 五 4 / 六 3） | 逐 lane 补丁 diff + LOCATE 核对 + grep 自证 | = W676-W678 本体（不新增号） | 随批次四启用 |
| WF-3 | `baseline-sample-audit` | 周期型（每季度或大版本后） | 110 个抽样判定点 | 抽查 verdict 清单（合规/违规/存疑） | 自行认领 | 建议建置 |
| WF-4 | `retro-evidence-pack` | 周期型（每复盘周期） | 取证维度 4 组（提交史/CHANGELOG 段/门禁史/问题闭环） | 取证包 markdown（量化附录），非最终报告 | 自行认领 | 建议建置 |
| WF-5 | `claim-adjudication` | 事件驱动 | 每条外部主张 1 个取证代理 | 逐条裁决表（坐实/证伪/部分坐实/属裁决项/无法判定） | 自行认领 | 下一次外部输入时建置 |
| WF-6 | —（不建置） | 触发条件登记 | — | — | — | 仅登记 |

---

## 五、WF-1 `evals-llm-baseline`：Agent 黄金评估集 LLM 基线

### 5.1 背景与缺口

W598 建置黄金评估集三件套（golden-50.jsonl / run_eval.mjs / validate.mjs），机检（validate.mjs + run_eval.mjs --self-check）已过，但 **LLM 基线 0 次执行**（B9：无任何 results-*.json）。缺口归因两条，均已实证：

1. **阻断**：密钥缺失（B7 `.env` 不存在）。
2. **脚本缺口**：run_eval.mjs 不自读 .env（B6），即使密钥落盘到 .env，直接运行仍无密钥可载——须先补 dotenv 引导或以 shell 导出。

### 5.2 前置条件（全部满足方可开工）

| 编号 | 条件 | 核验命令 | 期望输出 |
|---|---|---|---|
| P0-1 | 用户配置 `CODEBUDDY_API_KEY` 至 `xiyouji-agent-web/.env`（对照 `.env.example` 键名） | `grep -c "CODEBUDDY_API_KEY" xiyouji-agent-web/.env` | `≥1` |
| P0-2 | dotenv 引导补丁落地（见 WP-1.0） | `grep -c "dotenv\|process.env.CODEBUDDY_API_KEY" xiyouji-agent-web/evals/run_eval.mjs` | `≥1` |
| P0-3 | SDK 依赖在位 | `test -d xiyouji-agent-web/node_modules/@tencent-ai/agent-sdk` | exit 0 |
| P0-4 | 判分器自检过 | `cd xiyouji-agent-web && node evals/run_eval.mjs --self-check` | stdout 含 `[SELF-CHECK] 4/4 通过` 且 exit 0 |

**用户动作**：P0-1 只有用户能做（凭证属 .env，gitignored，Agent 禁触）。其余三项执行批自助完成。

### 5.3 工作项

**WP-1.0 run_eval.mjs dotenv 引导（脚本改动，主 context 串行做）**

- 改动：文件头部 import 区后加 3 行——从 `xiyouji-agent-web/.env` 读入 `CODEBUDDY_API_KEY` 并注入 `process.env`（自写 8 行内解析或引入 `dotenv` 依赖二选一；选自写解析以免动 package.json 依赖树）。已存在环境变量时不覆盖。
- 验收：
  - `node --check xiyouji-agent-web/evals/run_eval.mjs` → exit 0；
  - `cd xiyouji-agent-web && node evals/run_eval.mjs --self-check` → `[SELF-CHECK] 4/4 通过`，exit 0；
  - 按 W537 三新规④，推送前以真实参数冒烟一次：`node evals/run_eval.mjs --limit 1` → 产出含 `"id": "chapter-001"` 的 results json 或输出明确的 SDK 鉴权错误（鉴权错误=凭证问题，非脚本问题，回报用户）。

**WP-1.1 单例耗时实测（定 timeout 用，禁止拍脑袋）**

- 命令：`cd xiyouji-agent-web && time node evals/run_eval.mjs --limit 5`
- 产出：单例平均墙钟 T（秒）= 总耗时 / 5。
- 全量运行超时公式：`timeoutMs ≥ T × 50 × 2`（2 倍安全系数），下限 600000ms。

**WP-1.2 workflow 脚本建置（`.zcode/workflows/evals-llm-baseline.dwf.ts`）**

阶段与控制流（phase 名即用户所见节点名）：

1. **「机判全量跑测」**：`world.run("node", ["xiyouji-agent-web/evals/run_eval.mjs"], { timeoutMs: <WP-1.1 实测值> })`。exit≠0 **或 score=0** 时该次运行以 findings 报告失败点并 return（W679 探测实证：SDK 鉴权失败时运行器逐条打印 `SDK 异常` 后仍以 exit 0 落盘 score 0/1 的 results json——workflow 不得只信 exit code，score=0 且逐条 textLen 异常即视为运行面失败，禁止进入语义判读段）；机判输出文件已随 report 落盘，不重跑。
2. **「解析机判结果」**：`files.read("xiyouji-agent-web/evals/results-<日期>.json")`（运行器固定写当日日期），脚本内解析出 `score/total` 与逐条 `missingPaths/missingMention/hitForbid`。
3. **「语义判读 10 组并行」**：50 用例按 golden-50.jsonl 顺序切成 10 组×5 条；每组 1 个共享上下文判读子代理（`agent("judging-group-<n>")`，n=0..9），ask 携带该组 5 条的 `id/question/机判结果`，子代理自行打开对应 `expect_source_paths` 文档核对回答的语义忠实度（是否真讲了该文档要点、有无编造路径外的幻觉内容），返回类型化结果：

```ts
interface CaseSemanticVerdict {
  /** 用例 id，如 "chapter-001"。 */
  caseId: string;
  /** 语义判定：pass=回答忠实覆盖文档要点；partial=部分覆盖或含轻量不精确；fail=答非所问/幻觉。 */
  semantic: "pass" | "partial" | "fail";
  /** 一句话依据，引用文档原文片段或回答原文片段。 */
  evidence: string;
}
```

4. **「基线报告落档」**：聚合为 markdown artifact（primary）——机判 score、语义三档分布、逐条明细表、回归告警规则引用（B5：连续两批 ≥10 个百分点下降为回归）。`report()` 逐组随产随报（10 条 < 256 上限）。
5. **「返回与未覆盖声明」**：return WorkflowReport；`notCovered` 必须声明：语义判读为单代理单轮（无二次确证，首跑基线只定性不追责）、`maxTurns:3` 内未完成的用例计 FAIL 属运行器口径。

### 5.4 验收（执行批逐条勾）

| # | 验收项 | 命令/判据 | 期望输出 |
|---|---|---|---|
| A1-1 | 机判基线存在 | `ls xiyouji-agent-web/evals/results-*.json \| wc -l` | `≥1` |
| A1-2 | 全量口径 | results json 内 `total` 字段 | `= 50` |
| A1-3 | 语义判读覆盖 | WorkflowReport.findings 覆盖 caseId 去重数 | `= 50` |
| A1-4 | 产物可开 | artifact 列表含 1 个 primary markdown | 存在 |
| A1-5 | 首跑不设阈值 | 报告含「基线批次·无回归判定」字样 | 存在 |
| A1-6 | 门禁无回归 | `python scripts/verify_delivery.py` | 核心全绿 |

### 5.5 边界声明

- 语义轨是机判三规则的**叠加定性轨**，不替代、不覆写 run_eval.mjs 的 score。
- 本 workflow 的子代理是 ZCode 代理，仅做**判读**；被测对象是 `@tencent-ai/agent-sdk` 驱动的「渡口问津」agent（经 run_eval.mjs），两者不可混——禁止把用例直接发给 ZCode 子代理跑分，那测的是错误的对象。

### 5.6 执行记录（W679 批，2026-10-07）

- **WP-1.0 已落地**（本批 W679 提交）：run_eval.mjs 头部新增 9 行 `.env` 密钥引导——只载入 `CODEBUDDY_*` 前缀变量（不碰 `PROJECT_CWD`/`PORT` 等；`.env.example` 现载 `PROJECT_CWD=D:/1/xiyouji` 为过期路径，全量载入有害）、已存在环境变量优先不覆盖、`.env` 缺失时静默跳过由 SDK 显式报鉴权错误。验收实测：`node --check` exit 0；`node evals/run_eval.mjs --self-check` 输出 `[SELF-CHECK] 4/4 通过`。
- **密钥在位性探测已执行**（WP-1.0 验收第 3 项）：`node evals/run_eval.mjs --limit 1` → 用例 chapter-001 报 `SDK 异常: Authentication required. Please use /login command to sign in to your account`，exit 0、落盘 score 0/1（产物已删除不入库）。判定 = R3 预设场景：凭证问题非脚本缺陷。SDK 鉴权走账号登录态或 `.env` 凭证，`~/.codebuddy/` 实查为 CLI 工作目录（sessions/logs）非凭证库。
- **P0-1 处置改判（2026-10-07 用户二次裁决）**：用户裁决项目**不用 CodeBuddy**（含 CLI 与 API key 路线全部排除）且 agent-web **保留但更换驱动引擎**（三选一裁决，详见 docs/superpowers/plans/2026-10-07-agent-web-engine-swap-plan.md）→ 本节 CODEBUDDY_API_KEY 指引作废、被测对象改判；WP-1.0 的 `CODEBUDDY_*` dotenv 引导补丁随引擎批（W680）移除重写。**WF-1 改道：暂停至新引擎就位后执行（引擎方案 §五 W682）**——golden-50 用例、机判三规则、score=0 熔断守卫、WP-1.1 timeout 公式、语义判读 10 组、验收 A1-1~6 全部保留，仅运行载体从 sdkQuery 换为 engine 直调。
- **dotenv 链路端到端验证（2026-10-07·假 key 实测·随引擎更换一并退役的结论）**：以临时假 key 写入 `.env` 跑 `--limit 1`，错误形态由「Please use /login」变为 `401 (token-type:ApiKey, token-length:37)` 且 SDK 明示 `Environment variable CODEBUDDY_API_KEY is set`——链路本身可通；该验证随 CodeBuddy 路线整体作废。
- **WP-1.1 未执行**（阻断于引擎更换）：全量 timeout 值在 WP-1.1 实测前不得臆写。

---

## 六、WF-2 `batch-fix-fanout`：批次修复扇出（W676-W678 执行载体）

### 6.1 与现有方案的关系

**包装，不重定义**。任务清单、文件分组、产出契约、禁触清单全部沿用方案档 §十四（B28），本节只把这些 lane 翻译成 workflow 控制流。两处运行时适配：

1. §十四「subagent 只读 + 产出补丁不落盘」与动态 workflow 子代理的天然形态一致（子代理有编辑工具但 ask 中明令「不写任何文件，补丁以 diff 文本返回」）。
2. `max_concurrency: 4`（§十四总原则 3；本方案经用户批准即为该设置的有效授权）。

### 6.2 Lane 清单（引用 + 固化）

以方案档 §十四表格为准；为防版本漂移，首批（批次四）6 lane 在此固化：

| lane | 文件组 | 组内工作项 |
|---|---|---|
| L1 | narratology-13d | WP-4.1① |
| L2 | monster-female + monster-victims | WP-4.1②③ |
| L3 | monster-ecology | WP-4.1④ + WP-4.2①（同文件组内串行：A-05 → A-02） |
| L4 | mbti-evolution | WP-4.2② + WP-4.4② |
| L5 | magic-system | WP-4.2③ |
| L6 | monster-background + monster-capability | WP-4.2④⑤（方案档已合并的交叠组） |

批次五 4 lane、批次六 3 lane 于各启动日从方案档 §十四当期版抄录进脚本 lane 数组（脚本以 `args.plan_section` 不做——lane 硬编码在脚本内，每批次一份独立脚本文件，避免 ask 文本含可变量破坏缓存）。

### 6.3 子代理产出契约（每 lane 一个）

```ts
interface LanePatch {
  /** lane 编号，如 "L1"。 */
  lane: string;
  /** 补丁全文（unified diff 形态，含足够上下文行供 git apply 校验）。 */
  patch: string;
  /** 方案档 LOCATE 定位串逐一核对结果：每条 {locate, found: boolean}。 */
  locateChecks: { locate: string; found: boolean }[];
  /** 自证命令（grep/ python -c）与输出摘录，至少 1 条。 */
  selfCheck: string;
  /** 任一 LOCATE 未命中或自证失败时为 false，此时 patch 必须为空串。 */
  complete: boolean;
}
```

**失败语义**：`complete=false` 的 lane 不进入应用阶段，其定位串核对结果随 report 送主 context 人工介入；禁止子代理「自由发挥」绕过未命中（§十四扇出禁令复述条目原文收进 persona）。

### 6.4 主 context 串行应用流程（workflow 之外，每批次固定七步）

1. 逐 lane `git apply --check <patch>`（先验后施）→ 全过再逐 lane 施patch；
2. `python scripts/generate_csp.py` + `--check` → 0 漂移；
3. 涉内联样式/脚本批量改动时 `python scripts/inline_css.py --force`（W571 铁律）；
4. `python scripts/verify_delivery.py` → 核心全绿；
5. 方案档对应批次「验收汇总」行的机判命令逐条跑（如批次四：check_js_syntax --all 绿 + e2e test_site_quality.js 追加断言绿）；
6. `batch_cascade.py` dry-run → apply → 按 `scripts/output/_cascade_files_<批号>.txt` 清单逐面 `git add`；
7. Write 临时提交信息文件 + `git commit -F` + push + `gh run list` 确认。

### 6.5 禁扇出清单（照抄 §十四，执行时不得增删）

门禁 33–37 编写与挂载、`system.css`/`tokens.css` 改动、`inline_css.py --force` 全站分发、batch_cascade 级联、git 提交/推送、WP-4.3① 文件重命名的执行、WP-6.1/6.4 的 dataset 生成器与管线改动、全部跨文件断言验收。

---

## 七、WF-3 `baseline-sample-audit`：存量冻结基线抽查

### 7.1 背景与缺口

项目门禁哲学是「只拦新增、存量冻结豁免」（第 18/19/25/28 门禁均挂基线文件）。**基线外的第一天起有门禁，基线内的存量自冻结日起零复验**。8 份冻结基线（B10-B16，合计 19,545 行）的存量正确性当前完全依赖人工抽查，实际抽查次数 = 0（无任何抽查产物入库）。

### 7.2 抽样规约（确定性，任何 session 可复算）

- 集合枚举：`files.glob` 按各门禁原扫描域枚举（字典序）；基线条目按基线文件行序。
- 算法：`stride = floor(N / n)`，取第 `0, stride, 2×stride, …` 共 n 项；N 与 n 见 §7.3。
- 首批规模（固定值，写成脚本常量）：

| 目标 | 总量 N | 首批抽样 n | 判定内容 |
|---|---|---|---|
| frontmatter 基线文档 | 611 | 30 | 血缘 4 字段在位且格式合规（§4.6 口径） |
| 术语基线条目 | 383 | 40 | 规范词锚定成立（称谓组 canonical 在场） |
| 内容一致性基线条目 | 84 | 20 | 冻结时人工裁决的理由在原文可追溯 |
| 可引用性基线条目 | 349 | 20 | C1-C4 四判据现状（W657 后应为全量合规，抽现存零漂移） |
| **合计** | — | **110** | — |

### 7.3 产出契约

```ts
interface SampleVerdict {
  /** 抽样域：frontmatter | glossary | content-consistency | citability。 */
  domain: string;
  /** 被查文件仓库相对路径；基线条目类附基线行号。 */
  target: string;
  /** 判定：compliant=合规；violation=违规；uncertain=证据不足需人工。 */
  verdict: "compliant" | "violation" | "uncertain";
  /** 判定依据：文件路径:行号 + 关键字段值或原文摘录。 */
  evidence: string;
}
```

### 7.4 执行与验收

- 每域 1-3 个判定子代理（110 项 ÷ 每代理 20-40 项），verdict 随产随 report（110 < 256 上限）。
- 验收：
  - A3-1 verdict 总数 `= 110`，无缺号；
  - A3-2 每个 violation/uncertain 均含 `路径:行号` 形态证据（grep 抽验 `grep -c "\.md:[0-9]" 报告` 计数与 violation+uncertain 数一致）；
  - A3-3 处置闭环：violation → 主 context 裁决（登记不直改 or 排入下一批次）；uncertain → 列明缺什么证据；
  - A3-4 报告落 docs/10-方法论沉淀/ 或 scripts/output/（执行批定），且不含对基线文件的任何写操作。
- 周期：每季度 1 次，或任一基线文件被门禁批刷新后 1 周内加跑 1 次。

---

## 八、WF-4 `retro-evidence-pack`：复盘报告取证包

### 8.1 背景与既有模板

B26/B27：11 份复盘报告、最新模板 11 个二级标题。其中「一、信息基础与假设」与「附录 A 量化数据表」两节的取证劳动（提交史清点、CHANGELOG 段解析、门禁史、问题闭环对账）每周期重复，适合扇出；「经验定级/根因 5Why/改进计划」属主 context 裁决，**不进 workflow**。

### 8.2 输入

`args.since` / `args.until`（ISO 日期，如 `2026-10-06`/`2026-10-07`）或 `args.w_range`（如 `W672-W674`，脚本内映射为对应日期段——映射表从 CHANGELOG 现役段解析，解析失败即 escalation）。

### 8.3 取证四组（每组 1 个子代理，并行）

| 组 | 数据源 | 命令/方法 | 产出 |
|---|---|---|---|
| G1 提交史 | git | `world.run("git", ["log", "--oneline", "--since=<since>", "--until=<until>"])`（日期经 args 插入 args 数组，cmd 保持字面量；绕开 git.log 100 条上限） | 提交清单 + 增删行数（`--shortstat` 二次跑） |
| G2 CHANGELOG 段 | CHANGELOG.md | files.read + 脚本内切出区间内 W 版段 | 每批四件套摘要（来源/执行/验证/状态） |
| G3 门禁与 CI | 交接文档 + gh | `world.run("gh", ["run", "list", "--limit", "30"])` + 交接文档「一」段读取 | 红灯/热修清单 |
| G4 问题闭环 | 上期复盘报告 | files.read 上期报告「六 问题与预防机制」节 | 逐项闭环状态对账表 |

### 8.4 产出

- artifact：`retro-evidence-pack-<起止>.md`（primary）——含量化附录 A 所需全部数字表，每个数字可溯源到 G1-G4 的命令输出（溯源行随表附）。
- 明确不做：经验复用梳理、根因分析、skill-creator 任务卡、可行性自评——这些是主 context 在取证包基础上写的裁决内容。
- 验收：A4-1 四组产出齐且数字两两对账一致（如 G1 提交数 = G2 段落数对应的提交引用数，不一致即 escalation）；A4-2 取证包内每个数字带溯源标记。

---

## 九、WF-5 `claim-adjudication`：外部输入逐条裁决

### 9.1 先例与本工作流的定位

先例两起：W634 外部路线图 40+ Issue 提案逐条裁决（B29）；站点质量九轮外部审查每条主张的 repo 取证判真伪（方案档 §十裁决记录，累计坐实 60+ 项、证伪 16+ 项）。当前做法是主 context 逐条手工取证，单轮耗时以小时计且挤占裁决精力。

### 9.2 输入与主张切分

- `args.document`：外部输入文档的仓库内路径（外部分析先落 `scripts/output/` 或 `docs/_dev/`，不入 docs/ 正文）。
- 切分步骤：1 个切分子代理通读文档，返回主张清单：`{claim_id: "C01"...", claim_text, source_section, claim_type: "事实断言" | "缺陷主张" | "战略建议"}`。
- 事实断言/缺陷主张 → 进入取证扇出；战略建议 → 不取证，直接归「属裁决项」待用户对照冻结裁决（memory 判例：旧快照审读把已完成项当未修问题三度复现，战略建议必须对照 Backlog/冻结裁决归位）。

### 9.3 取证扇出契约

```ts
interface ClaimVerdict {
  /** 主张编号，与切分输出一致。 */
  claimId: string;
  /** 裁决：confirmed=坐实；refuted=证伪；partial=部分坐实；author-call=属裁决项；indeterminable=无法判定。 */
  verdict: "confirmed" | "refuted" | "partial" | "author-call" | "indeterminable";
  /** 取证命令及输出摘录，confirmed/refuted/partial 必须至少 1 条。 */
  evidenceCommands: string[];
  /** 仓库引用（路径:行号），同上必须性。 */
  repoRefs: string[];
  /** 一句话裁决理由。 */
  reason: string;
}
```

- 取证子代理只读（persona 明令：不编辑任何文件）；每主张 1 个代理，独立上下文防锚定。
- 保真度纪律（memory: review-claims-fidelity-bounds）：输出必须含保真度声明——全量实测了什么、抽样了什么、没测什么；确定性可扫描的主张优先 `world.run` 跑仓内现成扫描器（如第 33-37 门禁脚本）而非代理目测。

### 9.4 验收

- A5-1 verdict 数 = 主张数，无缺号（切分数与裁决数 diff = 0）；
- A5-2 confirmed/refuted/partial 三类的 `evidenceCommands` 与 `repoRefs` 均非空（脚本内断言，违反即该代理结果判废重派）；
- A5-3 汇总表 artifact 按 verdict 分组计数，`author-call` 项逐条挂对应冻结裁决/Backlog 登记的指针。

---

## 十、WF-6 触发条件登记（不建置）

| 候选 | 触发条件（满足才启动，否则保持登记） | 启动时建置要点 |
|---|---|---|
| i18n 扩语种 | 用户裁决新增语种（如日文站） | 复用 `_w627_gen_en_data.py` 生成器 + `_check_en_json_parity.py` 对账器模式（B22）；扇出 = 每数据副本 1 代理翻译 + parity 门禁 + 每页镜像验收 |
| A2-A6 批量新篇 | 用户批准含明确篇目清单的新篇批次 | 扇出 = 每篇 1 写作代理（文件独占）→ 每篇过第 18/19/20 门禁 + `_cite_probe.py` 引文探针（§4.3 铁律）→ 聚合失败项回修 |
| 读者数据定期采集 | 用户要求周期化 GoatCounter 留档（W629/W648 两起手工先例） | 用宿主定时自动化（cron），**不是**动态 workflow——固定命令无多代理控制流 |

---

## 十一、实施顺序与批次映射

| 顺序 | 动作 | W 号 | 依赖 |
|---|---|---|---|
| 1 | 用户裁决本方案（批准/裁剪/否决各 WF） | —（方案批可随 W676 入库或自行认领） | 本文 |
| 2 | WF-1 开工：WP-1.0 → WP-1.1 → WP-1.2 → §5.4 验收 → SaveWorkflow（经确认） | 动工日对账表 `max(W#)+1`（避开 W676-W678） | P0-1 用户配钥 |
| 3 | WF-2 随批次四首次实战（W676），批次五/六复用脚本形态 | W676-W678（已预留） | 批次四启动 |
| 4 | WF-3/WF-4 建置与首跑 | 各自认领 | 无硬依赖；WF-3 建议排在批次六（W678）数据面修复后，抽最新状态 |
| 5 | WF-5 建置 | 下一次外部输入到达时 | 外部输入 |

提交方式：本方案文件随顺序 1 的裁决批入库；各 workflow 的 `.dwf.ts` 保存后随对应批次 `git add`（B31 已证 `.zcode/workflows/` 可 tracked；漏 add 即 W595/W632 同族教训）。

---

## 十二、风险与对策

| # | 风险 | 对策（可判定） |
|---|---|---|
| R1 | judge 并发限额浮动（在仓经验，方案档 §十四引用） | WF-2 显式 `max_concurrency: 4`；其余 workflow 遇 provider 限流由运行时自适应，脚本不写重试 |
| R2 | run_eval 单例耗时尚无实测值 | WP-1.1 强制先测 5 例再定全量 timeout；timeout 公式固定（T×50×2，下限 600000ms） |
| R3 | SDK 鉴权失败误判为脚本缺陷 | WP-1.0 冒烟判据已区分：鉴权错误=凭证问题回报用户，非鉴权错误才修脚本 |
| R4 | workflow 中途失败丢失已完成工作 | 全部 workflow 用 `report()` 随产随报（§3.1 条 4），errored/stopped 均可读已报项；修复走 AmendWorkflow 不重跑 |
| R5 | 修订脚本报废缓存 | 子代理名稳定 + 可调常量只进控制流不进 ask 文本（附录 B §B-13 缓存规则） |
| R6 | 子代理越权写共享文件 | persona 显式禁触清单（§3.2 条 3）+ WF-2 补丁不落盘契约（§6.3）+ 主 context `git apply --check` 先验后施 |
| R7 | workflow 化被误用到范围外工作（§1.3 清单） | 本文 §1.3 反向清单 + SaveWorkflow 的 whenToUse 字段写明适用/不适用边界 |
| R8 | 报告数字跨批复制失真（W493 同族） | §二声明「执行批须当批重测」；WF-4 取证包每个数字带溯源命令 |

---

## 十三、收官判据（DoD）

本方案整体收官 = 以下全部为真：

1. §四表中 WF-1/2/3/4/5 每项处于三态之一：已建置且首跑验收全绿（§5.4/§6.4/§7.4/§8.4/§9.4 对应表逐条勾毕）、已按 §十一排期、或 WF-6 登记在案；
2. 已建置且验收通过的 workflow 均已 SaveWorkflow 至 `.zcode/workflows/` 且 git tracked（`git ls-files .zcode/workflows/` 计数 = 已保存数）；
3. 每个实战批次按 §3.2 条 6 完成对账表登记，CHANGELOG 有对应版段（四件套齐全）；
4. `python scripts/verify_delivery.py` 核心全绿，且第 18 门禁对本方案文件与新入库文档 0 违规；
5. 范围外清单（§1.3）对应工作仍由既有机器脚本/主 context 串行链承担，无一例被 workflow 化（`git log` 抽查可证）。

---

## 附录 A：扫描覆盖与方法（保真度声明）

**本会话实测（2026-10-07，命令与输出见 §二 B1-B31）**：evals 三件套内容与运行器全文（94 行逐段读）、密钥与 SDK 在位性、8 份冻结基线行数、A1-A6 六目录计数、site/data 与 site/en 与 dataset 与 output/data 文件数、EN 七副本与 i18n 工具链存在性、W 对账表现势、复盘报告存量与模板结构、§十四扇出矩阵原文、`.zcode/` gitignore 状态、`docs` 全树 md 计数（891 < glob 上限 2000）。

**引用既有文档未重新全文验证**：方案档 §十四的批次五/六 lane 细节（引用原文，批次四 lane 已逐条核对文件组）、W634 裁决文档内容（仅核存在性）、文档规范 §4.6/§4.7/§4.8 门禁口径（引用 AGENTS.md 摘要）。

**未扫描面（诚实声明）**：`hyperframes/compositions/` 内容（目录结构显示无批量扇出特征，未逐个确认）；`xiyouji-agent-web/src/` 交互面（与 workflow 候选判定无关）；golden-50 用例的逐条内容质量（仅验 schema 与条数，用例内容质量属 WF-1 语义轨的判定对象本身）。

**数字时效**：§二全部数字为 2026-10-07 快照，执行批按 §4.9 当批现测。

## 附录 B：动态 workflow 运行时契约速查（自包含）

供未来读者不回看官方 skill 即可理解本文全部运行时引用。与官方 skill 冲突时以官方 skill 为准。

- **B-1 脚本形态**：strict TypeScript，文件后缀 `.dwf.ts`（保存态），顶部可带 `/* zcode-workflow` YAML 元数据块（保存时由工具写入）。禁 `import/export/declare`、禁 `Date.now/Math.random/fetch/fs`、禁 Node/Web API。
- **B-2 类型化结果**：`ask<T>()` 的 T 为脚本内 `interface`；属性上的 JSDoc 注释会成为子代理实际读到的字段说明（校准手段，勿省）。
- **B-3 子代理**：`agent(name?, persona?)` 创建；名在单次运行内唯一且是缓存键；扇出/循环内禁止字面量重名（编译器抓字面量形态，运行期拼名重名则整运行失败）；persona 冻建于创建时。
- **B-4 world.run**：`cmd` 编译期字面量（提交确认时展示命令集，仅这些命令可执行）；运行期值进 `args`；无 shell（无管道/重定向/变量展开）；默认 300s 超时；stdout/stderr 各 256KB 上限；非零 exit 是返回值非异常。
- **B-5 files/git**：glob 上限 2000 文件、grep 上限 2000 命中/256KB，超限拒绝不截断；git.* 只读且观察经日志重放；`git.log(count)` 上限 100 条（需区间/更多用 `world.run("git", [...])`）。
- **B-6 report/artifact**：report ≤256 条/run、单条 ≤32KB、仅 JSON；随产随报，中途失败已报项仍送达。artifact 内容类（file/markdown）为效果（可拒统，重发升版本）；preset 类（chart/table/metrics/board）为声明（同步、不触文件），id 均须编译期字面量；≤32 id、每 id ≤16 版本、文件 ≤20MiB、markdown ≤256KB。
- **B-7 phase**：必须覆盖全脚本；名 = 编译期字面量、面向用户的中文短语；每 phase ≥1 ask 或 world.run；标记作用于所在块剩余部分；同名标记合一 phase（循环体保持一节点）。
- **B-8 并发与汇合**：不 await 即并发；`Promise.all` 是 barrier——逐项接续的流水线在每项回调内链式接续、末端一次汇合；一项失败不应连坐时在回调内 catch 或用 `Promise.allSettled`。
- **B-9 fresh eyes**：起草者看不见自己的缺口——计划/报告交给从未见过草稿的独立子代理审；审「会坏在哪、缺什么」而非「好不好」。
- **B-10 验证分级**：机器可判的用 world.run 当门（exit code 即确证，不再派确认代理）；代理发现的关键结论由独立第二个代理复现确证，未确证者标注 unconfirmed 保留不删；同一检查不被猎手/确证者/门各跑一遍。
- **B-11 escalation**：子代理每 ask 至多 3 次；第 4 次降级为按己最佳判断继续；question 经通知或 `GetWorkflowRun` 的 pendingQuestions 可见。
- **B-12 终态与修订**：completed/errored（不可续，Amend 换脚本）/stopped（可 Resume）；修订一律 `AmendWorkflow` + `path`（字节未变会拒，改并发/模型除外）；缓存 = 按名匹配 + ask 逐字节相同；首个活写入后缓存失效；修补运行中的运行越早越省。
- **B-13 缓存友好**：可调常量（阈值/轮数上限）只放脚本控制流，不进 ask 文本——改常量不洗缓存；改 ask 文本即强制该 ask 及下游重跑。
- **B-14 报告形状**：最终 return 用 `{conclusion, findings: [{where, what, evidence, status, severity}], verified, notCovered}` 四字段结构；全部以用户语言（本仓 = 中文）书写。
