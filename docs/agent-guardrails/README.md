# agent-guardrails ——《详解西游记》AI 编码 agent 约束层

> 人工维护件（不带「生成来源」标记，`python scripts/gen_folder_docs.py --refresh` 不会覆写本文件）。
> 建立：2026-11-02。形态：**补丁 + 可执行检查**，不是规则长文——根目录 `CLAUDE.md` 已被宿主自动加载，本目录不再放第二份。

## 0. 一句话

规则用「可直接合并的补丁块」给（`merge-patch.md`）；自检 5 条只问事实（`self-check.md`）；检查一条命令、只扫本次改动文件（`scripts/guardrails/check_changed.*`）。阈值全部按本仓库实测基线定，**不设全仓红档**。

## 1. 文件清单

| 文件 | 作用 | 维护 |
|---|---|---|
| `merge-patch.md` | **唯一需要人工动的东西**：根 `CLAUDE.md` / `AGENTS.md` / `pyproject.toml` 的插入位置 + 可复制措辞 + 两套 ruff 配置的加载优先级 | 人工 |
| `self-check.md` | 5 条问事实的自检 + 正反例 | 人工 |
| `scripts/guardrails/ruff-structure.toml` | **结构档**：C90 / PLR0912 / PLR0915 / PLR1702（含 preview，隔离在本文件内） | 人工 |
| `scripts/guardrails/check_changed.ps1` | Windows 主力入口（PowerShell 7） | 人工 |
| `scripts/guardrails/check_changed.sh` | POSIX / CI 版（bash） | 人工 |
| `scripts/guardrails/once_call.py` | 报告「只被调用一次」的函数/方法 | 人工 |
| `scripts/guardrails/api_diff.py` | 对比 HEAD 与工作区的公开 API 变化 | 人工 |
| `scripts/guardrails/check_nested_comprehension.py` | 嵌套推导式检查（ruff 0.16.9 无对应规则） | 人工 |
| `tests/fixtures/_sample.py` | 故意违规样板，只用于验证检查确实会报 | 勿改 |

> 本目录的 `index.md` 与 `scripts/guardrails/` 下的 `index.md` / `README.md` 由仓库 `scripts/gen_folder_docs.py` 自动生成，已刷新到与磁盘一致，不手改；本文件是人工维护件（无「生成来源」标记，`--refresh` 不覆写）。

## 2. 怎么启用（按顺序做，全部是真实命令）

1. 按 `merge-patch.md` §2-§4 合并三处：根 `CLAUDE.md` 规则 17、根 `CLAUDE.md` 常用命令 2 行、`AGENTS.md` §6 规则 20。**不要**直接复制本目录的说明性段落。
2. 可选：按 `merge-patch.md` §7 在现役手写钩子 `.git/hooks/pre-commit` 里追加**暂存区 .py** 的结构检查（**不要** `pre-commit install`，会覆盖手写钩子）。
3. 可选：按 `merge-patch.md` §7 在 CI 加一步 `check_changed.sh --all`。
4. 日常：agent 收尾时按 `self-check.md` 逐条作答，答案必须带命令输出或行号。

> **部署注意（W1077）**：`pre-commit` 框架已装（实测 4.6.0）但现役执行路径是手写钩子；若有人误跑 `pre-commit install`，手写钩子会被框架重写。此时 guardrails 检查仍由 `.pre-commit-config.yaml` 的 `agent-guardrails` 本地 hook 提供；恢复手写钩子请重跑 `bash scripts/install_hooks.sh`（检测到框架接管会给出 WARN）。两条路径用 `git write-tree` 做同索引去重，同一次提交不会跑两遍。

常驻规则里出现的三条验证命令都是本仓库真实可执行的：

```
py -3 scripts/verify_delivery.py --scope auto     # 已有门禁（第 3 槽等 57 段）
py -3 -m pytest tests -q                          # 已有单测（pytest 8.4.2，tests/ 75 个文件）
pwsh -File scripts/guardrails/check_changed.ps1   # 本层新增（只扫改动文件）
```

## 3. 规则 ↔ 检查映射

| 规则（合并后） | 由什么兜底 | 是本层新增吗 |
|---|---|---|
| 根 CLAUDE 规则 17：Python 改动自检 | `check_changed.ps1/.sh`（ruff 两档 + 嵌套 + API + 一次性函数提示） | ✅ 新增 |
| 根 CLAUDE 规则 4：CSP 重跑 | `scripts/generate_csp.py`（既有门禁） | ❌ 已有 |
| 根 CLAUDE 常用命令：verify_delivery / pytest | `scripts/verify_delivery.py`、pytest（既有） | ❌ 已有 |
| 根 CLAUDE 规则 6：file:// 铁律 | `verify_delivery.py` 第 8 槽（site/data 内嵌回退） | ❌ 已有 |
| 根 CLAUDE 规则 3/10：计数与历史段 | `check_doc_sync.py` + 第 1/3/31 槽 | ❌ 已有 |
| 根 CLAUDE 环境注意：BOM/编码/Edit 串行 | 无自动检查（环境纪律） | ❌ 已有 |
| AGENTS §6-20：结构检查权威条 | 本层 `check_changed` | ✅ 新增 |

## 4. 阈值决策表（候选 → 命中 → 选定 → 理由）

**计数口径**：`ruff check --select <规则> --config <阈值> --output-format concise .`（全仓，排除 `**/_*.py` 与 `archive/`）；文件数为剔除末行 `Found N errors` 汇总后的命中文件数。数字是 **2026-11-02 基线快照**；仓库持续被并行批次改动，复跑会小幅漂移（本批复测 PLR1702@3 已到 148 处）。

| 参数 | 候选值 | 命中（处） | 受影响文件 | 选定 | 一句话理由 |
|---|---|---|---|---|---|
| `PLR1702` 嵌套块数 | 3 | 145 | 53 | | 一次多出 105 处、多 30 个文件，等于开局让 3.6% 的文件全红 |
| | **4** | **40** | **23** | ✅ | 三层嵌套仍常见、五层才明显病态；受影响文件降到 1.6%，改动集模式下撞上的概率可接受 |
| | 5 | 7 | 5 | | 只剩 5 个文件「免检」，等于放过 5 层嵌套（样板 6 层仍会被抓，但真实长函数被放走） |
| `C90` 圈复杂度 | 12 | 62 | 48 | | 比 15 档多 32 处、多 22 个文件；老脚本一次性全红 |
| | **15** | **30** | **26** | ✅ | 业界常用阈值；能抓住 16-19 分支的长 if/elif 链（样板 17 分支即被报），受影响文件仅 1.8% |
| | 18 | 15 | 15 | | 放过 16-17 分支的链，正是最常见的一类 |
| | 20 | 11 | 11 | | 只剩 11 处，判据基本失效 |
| `PLR0912` 分支数 | 12（ruff 默认） | 57 | 46 | | 默认档直接全仓红 |
| | **16** | **20** | **19** | ✅ | 比默认宽 4 个分支避开存量；与 C901=15 形成重叠保护 |
| | 20 | 11 | 10 | | 只少 9 处命中却放宽 4 个分支，不划算 |
| `PLR0915` 语句数 | 60 | 12 | 12 | | 多 8 处，且这类长函数多为数据处理批处理，拆分收益低 |
| | **80** | **4** | **4** | ✅ | 约等于 120 行正文，只命中 4 个文件；作为「函数长度代理」够用 |
| | 100 | 2 | 2 | | 放过 80-99 语句的函数，代理失效 |
| 嵌套推导式深度 | **0（不允许嵌套）** | **20** | 20（`scripts/` 348 文件） | ✅ | 存量仅 20 处、更深层 0 处，收紧成本低；两层推导式可读性骤降 |
| | 1（允许一层） | 0 | 0 | | 等于不检查，样板里的双层推导式会被放过 |

> 结论：宽档（4 / 15 / 16 / 80 / 0）**保持不变**，没有为「更严格」再往下压。全仓结构档合计约 91 条，门禁只对改动文件生效。

## 5. 真实输出证据（`_sample.py`，故意 4 类违规）

命令：`pwsh -NoProfile -File scripts/guardrails/check_changed.ps1 -Paths tests/fixtures/_sample.py`

```
== check_changed（定向）：1 个 .py 文件 ==
All checks passed!
[OK] ruff 风格档（根 pyproject.toml，CI 同源）
tests\fixtures\_sample.py:16:5: too-many-nested-blocks: Too many nested blocks (6 > 4)
tests\fixtures\_sample.py:36:5: complex-structure: `long_elif_chain` is too complex (17 > 15)
Found 2 errors.
[FAIL] ruff 结构档（宽档阈值）
tests/fixtures/_sample.py:28  嵌套深度=1  list-comprehension
-- 扫描 1 个文件，嵌套深度 > 0 的 1 处
[FAIL] 嵌套推导式检查
tests/fixtures/_sample.py:31  once_helper  调用次数=1
-- 扫描定义 5 个（1 个文件），其中调用点 <= 1 的 4 个
[INFO] once_call（只报告，不计入阻断；判据见 self-check.md 第 1 条）
[OK] 公开 API 变化（提示）
== 结论：有阻断项，请修到 0 再提交 ==
```

（节选：`api_diff` 段原样还有 2 行「新增文件，无 API 变化可对比 / 变化 0 处，破坏性 无」。）

无 .py 改动时（实测 `-Paths` 指向一个非 .py 文件，退出码 0）：

```
[SKIP] 本次改动没有可检查的 .py 文件（非 Python / 已删除文件 1 个），无阻断项。
[SKIP] 非 Python 改动请另跑：py -3 scripts/generate_csp.py --check / py -3 scripts/verify_delivery.py --scope auto
```

`api_diff.py` 破坏性变更检测（内存 AST 自测，真实输出）：

```
~ f: 参数变化 (a, b=1, c=2) → (a, b=3, c=2)
~ f: 返回注解变化 -> int → -> str
~ f: 新增 raise KeyError
BREAKING = True
```

## 6. 收紧路线（只写触发条件，不设日期）

观察窗口统一为「**连续 3 个 W 批次的改动集运行**」：每个批次 `check_changed` 退出码 0，且目标规则在改动集里命中数为 0。满足即执行下一阶段；任一阶段触发后全仓新增量超过表中预期，暂停并在本文件记录原因。

| 阶段 | 变更 | 预计新增存量（全仓） | 触发条件 |
|---|---|---|---|
| 1 | `PLR1702` 4 → 3 | +105 处、23 → 53 个文件（+30） | 连续 3 批改动集 PLR1702 命中 = 0 |
| 2 | `C90` 15 → 12 | +32 处、26 → 48 个文件（+22） | 连续 3 批改动集 C901 命中 = 0 |
| 3 | `PLR0912` 16 → 12 | +37 处、19 → 46 个文件（+27） | 连续 3 批改动集 PLR0912 命中 = 0 |
| 4 | `PLR0915` 80 → 60 | +8 处、4 → 12 个文件（+8） | 连续 3 批改动集 PLR0915 命中 = 0 |
| 5 | 并入 `pyproject.toml` 并让 CI 跑全仓 | 0（前四阶段已清） | 全仓四条规则命中连续 3 批为 0（见 `merge-patch.md` §5） |

每阶段落地动作：改 `scripts/guardrails/ruff-structure.toml` 的默认值 + 把 `check_changed` 的 `-Strict` 覆盖值整体下移一档（保持「Strict 比默认再紧一档」）。验收：`check_changed.ps1 -Strict` 退出码 0，且全仓命中数不超过表中「预计新增」。

## 7. 已知限制

1. **只覆盖 .py**：js/ts/html/css 不在本层（仓库有 `eslint.config.mjs`，未接入 `check_changed`）。
2. `once_call.py` 是**名字级**启发式：同名函数、`getattr`/回调/装饰器注册会误判；`visit_*`、`@property`/`@fixture` 已跳过；测试里的调用也算数。它只作线索，不做门禁。
3. `api_diff.py` 只比较 AST 可表达的信息，注解/默认值是文本级比较（引号、空白差异可能误报）；不追踪 re-export 与 `*args` 展开。
4. 改动集口径：`git diff --name-only HEAD` + `git ls-files --others`；与根 `pyproject.toml` 一致豁免 `_` 前缀脚本；**已排除 gitignored 的 `tmpe/` 临时脚本区**（否则历史脚本会刷一屏 `SyntaxWarning`，`once_call` 也已跳过该目录并静音解析告警）。共享工作树下会连带检查其他会话未提交的 .py（实测曾报出 `scripts/visual_regression_probe.py` 的 2 处嵌套超限），只想核自己的改动用 `-Paths`。
5. Windows 上把脚本输出接 PowerShell 的 `2>&1 |` 管道时，MSYS 的 `echo` 偶发 `write error: Bad file descriptor`；重定向到文件或直接执行正常，不影响退出码。
6. **目录位置约定（W1077 起）**：脚本在 `scripts/guardrails/`（第 42 槽只扫 `scripts/` **顶层**文件，子目录不进 C1 扫描）；文档在 `docs/agent-guardrails/`（非编号目录，`docs_index.py` 只收数字前缀目录 ⇒ 不触发 `docs/INDEX.md` 逐字节校验）；`_sample.py` 在 `tests/fixtures/`，`pytest.ini` 的 `python_files = test_*.py` 已实测不会收集它。
7. **阈值数字会漂移**：表中数字是 2026-11-02 快照，仓库持续被并行批次改动（复测 PLR1702@3 已到 148），不影响阈值选择，但复核时要接受 ±3 的漂移。
8. **脏工作区会让 CSP 门禁红**：改动 site 内联脚本后必须按根 `CLAUDE.md` 规则 4 重跑 `generate_csp.py`（勘察当天曾实测到 `site/index.html` 漂移，复核时已归零）。

## 8. 与仓库既有约定的关系

- 根 `CLAUDE.md`（52 行速查层）、根 `AGENTS.md`（31 KB 治理手册）、`.agent/skills/puti-shouye/SKILL.md`（15 条高频判据）**继续有效**；本层只补「可执行 + 有阈值」的一块，并通过 `merge-patch.md` 正式登记进去。
- 本目录**不提供**常驻 `CLAUDE.md`/`AGENTS.md`——那会形成第二份规则源且不会被自动加载。
