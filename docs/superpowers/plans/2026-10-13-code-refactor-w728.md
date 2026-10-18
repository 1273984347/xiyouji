# 代码重构方案（W728 · scripts/ 门禁与工具链三文件）

> **📖 阅读契约（W712）**：查表型——W728 动工/复核/验收时读全文；日常只需 §1 结论与 §7 验收口径。  
> **执行状态**：**✅ 已执行（W728·2026-10-13「门禁与工具链代码重构批」·CHANGELOG W728 段实证；本状态行迟至 W792 核查批回写）**。

> **来源**：用户令「重构所的代码，保持原有功能、输入输出及外部接口完全不变，提升可读性可维护性；重点优化命名规范、拆分过长函数、消除重复逻辑、提取公共模块、加注释、统一风格」，并追加约束「所有内容必须可量化、可验证、可执行、可追踪、符合实际情况」+「开始之前必须写一个详细的计划方案，详细具体一点，不要笼统，不要大概，不要可能，要精确，采用可量化、可验证、可执行、可追踪、符合实际情况的描述」。  
> **授权上下文**：用户已明示「在这个 dev 分支可以随便操作不用在意，可以全仓重构」（当前分支=dev·已实证 `git branch --show-current`=dev）。

## 一、结论（先行）

1. **范围裁决：不做全仓 555 py + 787 js 的平铺重构**。理由可量化：单轮会话内无法对 1342 个文件完成「输出逐字节对比」级验证，违反用户自设的「可验证」硬约束；全仓机械改动无测试覆盖的文件（如 site/data 87 个可视化页内联 JS）风险不可控。**改法=先打样后推广**：本批对 3 个「有度量痛点 + 有验证抓手」的文件做深度重构并全量验证，把方法论（表驱动化/共享模块/通用 runner）固化成后续批次的模板。
2. **本批三目标**（按收益×风险比排序）：
   - **T1 `scripts/verify_delivery.py`**（1173 行·main() 905 行=全文件 77%·46 个门禁段中 35 个 subprocess 委托段共 608 行同构样板）；
   - **T2 `scripts/sync_docs.py` × `scripts/verify_delivery.py` 重复消除**（A_AREAS 六板块目录表 + `_count_content_md` 计数函数双份手工维护·sync_docs 源码注释自证「与 verify_delivery 同口径」）；
   - **T3 `scripts/security_scan.py`**（scan_sri 91 行内含 script/link 两个约 30 行近同构块）。
3. **验收硬标准**：重构后 4 种 scope 模式（full/docs/site/auto）输出与基线**逐字节一致**；pytest 296 全绿；ruff 0；security_scan 报告与基线一致。任一不符即回退（git 单批次可弃）。
4. **发布**：按项目铁律走 W728 批次（对账表登记 → batch_cascade 级联六文档 → pre-commit 门禁 → dev 分支提交），不用 `--no-verify`。

## 二、现状度量（重构前基线·全部可复现）

### 2.1 命令与结果（复现入口）

```bash
# 度量（AST 实测·2026-10-13）
python -c "import ast; ..."          # 见 §2.2 表
# 行为基线（4 模式·已存 /tmp/vd_baseline_*.txt）
python scripts/verify_delivery.py            # full : exit=0·53 行输出·0 FAIL
python scripts/verify_delivery.py --scope docs   # exit=0·79 行输出·0 FAIL
python scripts/verify_delivery.py --scope site   # exit=0·58 行输出·0 FAIL
python scripts/verify_delivery.py --scope auto   # 解析为 docs（工作树干净→空变更集→docs 档）·exit=0
# 测试基线
py -m pytest tests/ -q                 # 296 passed in 3.43s
py -m ruff check scripts/verify_delivery.py scripts/sync_docs.py scripts/security_scan.py   # All checks passed
```

### 2.2 复杂度度量表（AST 实测）

| 文件                         | 总行数  | 最长函数                       | 痛点度量（实测值）                                                                                                    |
| -------------------------- | ---- | -------------------------- | ------------------------------------------------------------------------------------------------------------ |
| scripts/verify_delivery.py | 1173 | main() L265-1169=**905 行** | 46 段门禁中 35 段 subprocess 委托=**608 行**（占 main 67%）；20 个简单委托段共 299 行 + 15 个严格委托段共 309 行；subprocess.run 调用点 37 处 |
| scripts/sync_docs.py       | 645  | rule_counter_sum 69 行      | `A_AREAS`（8 行）+ `_count_content_md`（8 行）与 verify_delivery 重复；rule_stats 53 行/rule_wids 45 行（本批不动）            |
| scripts/security_scan.py   | 809  | scan_sri L302-392=91 行     | scan_sri 内 script/link 两块各约 30 行同构（SRI-001/SRI-002 判定+findings 构造逐条同构）                                       |

### 2.3 重复块清单（T1 的消除对象·逐段可点名）

- **简单委托段 ×18**（双源漂移/CSP漂移/腐蚀插件/内联语法/CSS平衡/token覆盖/动效禁令/INLINED完整/动态链接/治理契约/索引健康/元信息块/术语一致/引文核验/图表自洽/数据一致/W区间字面量/SEOhead）：同构于 `section→subprocess.run→tail 切片→ok/fail/warn` 五步式，仅消息模板/超时/尾行口径不同；
- **严格委托段 ×15**（可引用性/设计令牌对账/色盲安全/降级声明/文档口径/CLAUDE速查/head内容/CSS变量引用/声明分隔/孤立选择/kpi基类/内嵌残留/时间线双源/chapter双源/AGENTS分层）：同构于 `section→try run→crash 即 fail→exit≠0 fail→缺汇总行 fail→ok` 六步式；
- **bespoke 段 ×2**（docs链接=尾行按 BROKEN/校验完成过滤；a11y对比=JSON 解析 P0/P1）：保留为独立函数不入表。

## 三、重构设计（逐文件·精确到符号级）

### 3.1 T1 `scripts/verify_delivery.py`：905 行 main() → 表驱动编排

**不变式（接口契约·重构后必须逐字节保持）**：

1. 模块级公开符号全部保留：`EXPECTED_SECTION_NAMES`、`SCOPE_DOCS_SECTIONS`、`SCOPE_SITE_SECTIONS`、`_SCOPE_CORE`、`_GATE_SUMMARY_MARKERS`、`CORE_DOCS`、`AUX_DOCS`、`DOCS`、`HTML`、`A4_DOCS`、`EXPECT_A4`、`ARCHIVE_DOCS`、`A_AREAS`、`_parse_scope`、`_git_changed_files`、`_classify_scope`、`latest_version_from_changelog`、`parse_footer_version`（tests/test_verify_delivery_version.py 依赖后两个·不得改名）；
2. 46 个段名、段顺序、每条 OK/WARN/FAIL 消息文本、退出码语义（核心 FAIL→1）完全不变；
3. `--scope` 四态分级与 subprocess monkey-patch 短路语义不变（补丁安装时机必须在 `_git_changed_files()` 之后——否则 auto 档 git 探测会吃到伪造结果，这是原代码注释明示的坑）；
4. 第 41 门禁（check_agents_layers.py C2）以 `第\s*(\d+)\s*(?:槽|门禁)` 正则扫本文件取 max 槽位——重构后「第 28-41 门禁」字面量必须保留在严格段消息/汇总行标记中（max=41 不变）。

**重构后结构**（模块级新增符号·命名对齐现有 `_` 前缀风格）：

| 符号                                                            | 形态         | 职责                                                                                                                      |
| ------------------------------------------------------------- | ---------- | ----------------------------------------------------------------------------------------------------------------------- |
| `_Reporter`                                                   | class      | 原 main() 内 fail/warn/ok 三闭包 → fails/warns 计数 + 打印                                                                       |
| `_GateContext`                                                | class      | scope 解析态 + `sections_ran` 段登记 + `_scoped_run` 补丁 + `_SkipResult` + 跨段共享量（ver/wnum/max_w_html/doc_all）                  |
| `_SimpleGate`                                                 | NamedTuple | 简单委托段参数表行：section/script/args/timeout/ok_msg/fail_msg/warn_msg/tail_out/tail_err/fail_tail/runner/missing_warn/severity |
| `_StrictGate`                                                 | NamedTuple | 严格委托段参数表行：section/script/args/timeout/marker/crash_msg/fail_msg/marker_msg/ok_msg/ok_line/fail_tail                     |
| `_SIMPLE_GATES_PRE_A11Y` / `_SIMPLE_GATES_POST_A11Y`          | list       | 18 个简单段按执行序分两张表（a11y对比夹在中间·第 20 段）                                                                                      |
| `_STRICT_GATES`                                               | list       | 15 个严格段按执行序一张表                                                                                                          |
| `_run_simple_gate(ctx, gate)` / `_run_strict_gate(ctx, gate)` | func       | 两个通用 runner（各约 25 行·替代 608 行样板）                                                                                         |
| `_gate_expected_version` … `_gate_embedded_fallback`          | func ×11   | 11 个内联逻辑段各提取为 `_gate_*(ctx)` 函数（期望版本/dukou页脚/六文档同步/旁文档同步/范围漂移/A4计数/A1-A6计数/学术引用/A1导航/sitemap覆盖/内嵌回退）                    |
| `_gate_docs_links` / `_gate_a11y`                             | func       | 2 个 bespoke 段（保留各自特化逻辑）                                                                                                 |
| `_probe_health` / `_check_section_lock` / `_print_summary`    | func       | 收尾三段（health 探活/段自洽锁/汇总退出码）                                                                                              |
| `main()`                                                      | func       | 905 行 → 约 55 行编排：建 ctx → 按序调 11 内联 + 2 bespoke + 18 简单表 + 15 严格表 → 收尾                                                   |

**关键正确性细节（实现时逐条对拍）**：

- 简单段 fail 消息统一 `"%s（exit %d）：%s" % (fail_msg, rc, " / ".join(tail[:6]))`：实测 18 段中 12 段用 `tail[:6]`、6 段用全 tail——因 tail 上限 4 条，两者等价；唯一例外=治理契约 `tail[:4]`（tail 上限 6 条）且非零退出走 WARN 不 FAIL → 以 `severity="warn"` + `fail_tail=4` 参数化；
- 严格段 ok 消息取行：多数取 `stdout[-1]`，内嵌残留/时间线双源/chapter双源/AGENTS分层 取 `stdout[-2]`（且 `len>=2` 否则「无输出」）→ `ok_line` 参数（-1/-2）；
- AGENTS分层 fail 消息用 `stdout[-4:]` 而非标准 tail → `fail_tail="stdout4"` 参数；
- 可引用性 marker 校验字面量是 `"---- 第 28 门禁："`（比 `_GATE_SUMMARY_MARKERS` 中的条目短）→ 表内逐段照抄不改写；
- 简单段 FileNotFoundError：仅 2 个 node 段（双源漂移/内联语法）有专用 WARN（「node 不可用，跳过…」）→ `missing_warn` 参数，其余段走通用 `warn_msg % e`；
- docs链接/a11y 保持 bespoke（a11y 内 `import json as _json` 别名改直接用模块级 `json`·行为等价）；
- **顺带修复一处死代码**：L744-746 治理契约 except 块内遗留 `warn("Skills 索引一致性门禁执行异常（W498）: %s" % e)`（W498 门禁已删除后的孤儿行·仅在 check_governance_docs.py 崩溃时触发双 WARN）→ 删除并在 CHANGELOG 段点名。

### 3.2 T2 共享模块 `scripts/doc_areas.py`（新文件·约 45 行）

```python
AREA_DIRS = (docs/01-全书逐回解读, docs/06-个人随笔, docs/02-人物深度分析,
             docs/03-主题与情节专题, docs/04-文化与历史背景, docs/05-诗词歌赋)  # 六板块唯一事实源
def count_content_md(area_dir): ...  # 原 _count_content_md 逐字节同口径（-1/排除 README.md）
```

- 消费侧：verify_delivery `A_AREAS = list(zip(_AREA_LABELS, AREA_DIRS))`（展示标签「A1 逐回解读」…留本文件·属呈现层）；sync_docs `A_AREAS = list(zip(("A1".."A6"), AREA_DIRS))`（短键标签不变·rule_stats 的 disk 字典键不变）；
- 导入方式：`from doc_areas import AREA_DIRS, count_content_md`（两文件均以 `python scripts/xxx.py` 直跑·sys.path[0]=scripts/ 自动可导；tests/conftest.py 亦已注入 scripts/）；
- 命名不带 `_` 前缀（非常性一次性脚本·AGENTS §3 约定 `_*.py`=一次性诊断件）。

### 3.3 T3 `scripts/security_scan.py`：scan_sri 去重

- 提取 `_check_resource_attrs(text, pattern, kind_label)`：入参 HTML 文本 + 编译正则（SCRIPT_SRC_RE/LINK_HREF_RE）+ 类型标签（「外部脚本」/「外部样式」），内部完成 `_is_external_resource` 过滤、行号计算、integrity/crossorigin 判定、SRI-001/SRI-002 findings 构造；
- scan_sri 主体 91 行 → 约 40 行（目录遍历保留·两个 30 行同构块各缩为 3 行调用）；
- findings 逐字段不变（rule/file/line/description/severity/snippet·snippet=tag[:120]）；
- 验证抓手：`py scripts/security_scan.py --all --output <tmp>` before/after 报告 diff + pytest 296（含 test_security_scan 12 例）。

## 四、风险登记表（逐条有缓解措施）

| #  | 风险                                 | 概率 | 影响               | 缓解                                                                                   |
| -- | ---------------------------------- | -- | ---------------- | ------------------------------------------------------------------------------------ |
| R1 | 消息模板抄漏一字导致输出 diff                  | 中  | 验收不过             | §6.1 逐字节 diff 全模式兜底；参数表逐段对照原码构建                                                      |
| R2 | subprocess 补丁安装时机变化破坏 --scope auto | 中  | auto 档误跳过 git 探测 | 补丁在 `_GateContext.__init__` 末段安装（scope 解析之后）·对照原 L285 vs L321 时序                     |
| R3 | 第 41 门禁 C2 槽位 max 漂移               | 低  | 门禁误红             | 严格段「第 NN 门禁」字面量全保留·改后跑 check_agents_layers self-test（5/5）                            |
| R4 | doc_areas 新模块导入路径失败                | 低  | 脚本起手崩            | 三种入口实测：`python scripts/verify_delivery.py`、`py -m pytest`、pre-commit hook（托管 python） |
| R5 | 门禁段自洽锁（46 段集合）漏段                   | 低  | 假绿/误红            | 自洽锁本身即防线·四模式跑过即证明                                                                    |
| R6 | pre-commit 拦截提交                    | 中  | 流程卡点             | 级联后先手动跑 verify full + pytest 再提交；不跳 hook                                             |

## 五、执行顺序（可追踪·每步有完成判据）

| 步  | 动作                                              | 完成判据                                                       |
| -- | ----------------------------------------------- | ---------------------------------------------------------- |
| S1 | 写本方案档入库                                         | 文件存在+元信息块完整                                                |
| S2 | T1 重构 verify_delivery.py                        | ast 解析通过+ruff 0+main()≤60 行                                |
| S3 | T1 行为对比（full/docs/site/auto ×基线）                | 4 个 diff 全空+exit 码一致                                       |
| S4 | T2 建 doc_areas.py+两侧接入                          | ruff 0+sync_docs `--help`/干跑不崩+两文件 A_AREAS 派生自同一 AREA_DIRS |
| S5 | T3 重构 scan_sri                                  | ruff 0+security_scan --all 报告与基线 diff 空                    |
| S6 | 全量回归：pytest 296 + verify full + ruff 全 scripts/ | 全绿                                                         |
| S7 | W728 级联（对账表+batch_cascade spec）                 | 级联清单 10 面全落盘+precheck 0 issue                              |
| S8 | dev 分支提交                                        | pre-commit 自动 verify --scope auto 通过+commit 落地             |

## 六、验证协议（验收口径·可复现）

### 6.1 逐字节对比（T1 主验收）

```bash
python scripts/verify_delivery.py > /tmp/vd_new_full.txt 2>&1; echo "exit=$?" >> /tmp/vd_new_full.txt
diff /tmp/vd_baseline_full.txt /tmp/vd_new_full.txt   # 必须空
# docs/site/auto 同法；auto 档在工作树干净时解析为 docs（基线同·可对比）
```

### 6.2 测试与静态检查

```bash
py -m pytest tests/ -q                          # 期望 296 passed
py -m ruff check scripts/                       # 期望 All checks passed
python scripts/check_agents_layers.py --self-test   # 期望 5/5（第 41 门禁 C2 对账不受重构影响）
```

### 6.3 T2/T3 专项

```bash
# T2：sync_docs 干跑不崩且统计口径不变（rule_stats 输出 diff）
py scripts/sync_docs.py 2>&1 | tail -20          # 与重构前同输出（无 MISMATCH 新增）
# T3
py scripts/security_scan.py --all --output /tmp/sec_new.md --no-pip-audit   # 与基线报告 diff 空
```

## 七、不在本批范围（显式排除·防范围蔓延）

1. site/data 87 个可视化页内联 JS、xiyouji-agent-web/（59514 文件·React+TS 前端·独立验证体系）；
2. a11y_audit.py 2513 行（rule\_* 30-60 行为规则扫描器固有形态·重复度低·改造需 JSON 输出对比·留待后续批）；
3. sync_docs.py rule\_* 系列（53/45/69 行·逻辑各异非重复·按 W520「同类只留最佳」原则无收益不动）；
4. 任何文档内容改写（六文档只按 W728 级联机制更新版本元信息）。

## 八、经验沉淀点（为什么这样决策·供后续批次复用）

1. **「可验证」约束直接决定范围粒度**：用户自设五性中「可验证」最硬——没有行为基线（4 模式输出/296 测试/报告 diff）的文件不动。方法论=先采基线再动手，而不是先动手再补测。
2. **表驱动化是消除「段样板」类重复的标准解法**：35 个委托段的问题不是长而是同构——把差异（消息/超时/尾行/严重级）收进参数表、把同构收进 runner，新增第 42 门禁时从「抄 15 行」变「加 1 行表项」。
3. **monkey-patch 时序是隐式契约**：`_scoped_run` 依赖「安装前完成真实 git 探测」——重构移动代码时这类时序约束不会写在任何签名里，只能靠原注释+逐行对拍保住（本次以 R2 登记）。
4. **共享模块的边界按「口径」切不按「文件」切**：A_AREAS 目录表+计数函数是口径（漂移即数据失真），展示标签是呈现（各消费方不同）——只共享口径层，避免为统一标签而改 sync_docs 输出键。
5. **门禁脚本自带对账防御**：第 41 门禁 C2 用正则扫 verify_delivery 源码对账槽位——重构门禁脚本自身时，先读「谁在解析我」（check_agents_layers/check_doc_sync/doc-sync C3），再动刀。
