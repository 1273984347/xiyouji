# AGENTS.md — 《详解西游记》项目 Agent 指南

> **📖 阅读契约（W707）**：索引型——不要线性通读。先跑 `python scripts/agent_start.py --task` 拿「本次任务相关」清单按需读节；§4.2 全 83 槽门禁与 §4.3 全部坑位属按需查表（L2 已拆分落地：docs/agent/gates.md · pitfalls.md · agent-web.md·W709）；§1-§3/§6 铁律/§7 必读。
>
> 本文件面向进入本仓库工作的 AI Agent（及新接手的人类维护者），提供项目的用途、技术栈、目录结构、关键模块、依赖关系、构建运行方式与必须遵守的铁律。动手前按 §7 路径按需读节；更细的规则以文末「权威文档」为准。
>
> **维护契约（防乱写）**：本文档是 Agent 协作指南，只允许结构性编辑——① 保持 §1–§8 骨架不变；② 新增铁律/规则必须**就地并入对应章节**并全篇去重（禁止追加「速记 / 补充」尾部段落）；③ 版本脚注更新须与当前 HEAD（vX.Y.Z W###，用 `git rev-parse --short HEAD` 核对）一致；④ 与 HANDOVER / 文档规范 / CHANGELOG 冲突时以后三者为准；⑤ 摘要层纪律：条目一行一事，叙事与验证细节归 L2（gates/pitfalls/CHANGELOG），过期数字随批纠偏。

---

## 1. 项目用途与定位

**《详解西游记》**（xiyouji）是一个「一源多形 · 数字人文可视化解读《西游记》100 回」的项目。它把《西游记》的文本研究组织为四层产物：

- **文档（Docs）**：Markdown 写就的逐回解读、人物分析、主题专题、文化背景、诗词赏析、个人随笔。
- **站点（Site）**：可浏览的纯静态 HTML 站点，`file://` 双击即可打开，部署于 GitHub Pages（https://1273984347.github.io/xiyouji/ ）。
- **数据可视化**：90<!--stats:visualization_pages--> 个 D3.js / Three.js 可视化页（site/data/ 共 91<!--stats:site_data_html--> 个 HTML，「87」不含模板壳 _shell.html），覆盖 133 个<!--doc-sync:exempt--> 数据维度（章节统计、人物关系网络、八十一难热力图、取经路线、情感热力图、AI 对话等 34<!--stats:script_classes--> 类主题 A–AH）。
- **可问询入口**：Web Agent「西游记·渡口问津」（xiyouji-agent-web/）——自研 OpenAI-compatible 引擎（server/engine/·W680·全主流大模型端点适配），可对话、检索 docs/source、跑脚本。

**核心内容规模**：A1–A6 内容板块共 629<!--stats:a1_a6_docs--> 篇（A1 逐回 100 / A2 随笔 44 / A3 人物 215 / A4 主题 209 / A5 文化 35 / A6 诗词 13；算法与边界见 docs/00-导读/统计口径说明.md；W505 起 611→616）；英文站 site/en/ 138<!--stats:site_en_html--> 页已全量英文化。

**设计方向**：锁定「新中式·数字雅集」（宣纸底/墨文/朱砂点缀/零外域依赖）；**页面动效是强制契约**——时长三档预算（≤150/250/600ms）、reduced-motion 双守卫、tooltip 统一 `.chart-tooltip`、count-up fail-open 等，详见 DESIGN.md（视觉 §1-4、**动效 §5**）。

**版本号语义**：`vX.Y.Z` 是**内容发布批次编号，不适用 SemVer**。每个发布批次有唯一 W### ID；判断"改了什么"看 CHANGELOG.md，不要从版本号推断兼容性。

---

## 2. 技术栈

| 层 | 技术 |
|---|---|
| 可视化前端 | D3.js v7（本地化 `site/static/js/d3.v7.min.js`）、Three.js r128（`three.r128.min.js`，手动 OrbitControls） |
| 站点 | 原生 HTML/CSS/JS，纯静态，file:// 直开，内联 tokens.css + system.css |
| 文本分析 | Python（词频/共现/情感/术语 NLP，stdlib + 少量依赖，见 scripts/requirements.txt） |
| 代码规范 | Ruff（pyproject.toml，line-length 120，py311）|
| Web Agent | React 19 + Vite 8 + TypeScript + TDesign React + Express 5 + better-sqlite3 + 自研 OpenAI-compatible 引擎（server/engine/·W680） |
| 测试 | pytest + Playwright E2E（冒烟/交互/视觉回归） |
| CI/CD | GitHub Actions（pytest / Playwright / Lighthouse / pip-audit / npm-audit / Pages 部署 / 截图审查） |

**运行时要求**：Node ≥ 20（Web Agent）；Python 3.11+（脚本）。

---

## 3. 目录结构

```
xiyouji/
├── docs/                  # Markdown 文档主体（内容真载体）
│   ├── 00-导读/           # 项目说明、文档规范、术语表、统计口径
│   ├── 01-全书逐回解读/   # 100 回逐回解读（A1）
│   ├── 02-人物深度分析/   # A3 人物谱系
│   ├── 03-主题与情节专题/ # A4 主题专题（209<!--stats:a4_docs--> 篇）
│   ├── 04-文化与历史背景/ # A5 文化背景
│   ├── 05-诗词歌赋/       # A6 诗词
│   ├── 06-个人随笔/       # A2 随笔（44<!--stats:a2_docs--> 篇）
│   ├── 07-09/             # 学以致用 / 提升认知 / 精神塑造
│   ├── 10-方法论沉淀/     # 复盘、诊断 SOP、DRL 真循环等可复利经验
│   ├── 11-方案报告/       # 复盘/审查/调研报告统一归档（W737 建·W757 改名·报告类不再入 10）
│   ├── S2/S3/S4/          # 外部分享 / 方法论外部分享 / 学术投稿候选
│   ├── superpowers/       # 开发过程 spec/plan 档案
│   ├── _dev/  _templates/ # 开发内部文档 / 内容模板（勿直接套用）
│   └── INDEX.md           # 文档索引（docs_index.py 生成）
├── source/                # 原著原文（分回）+ 引用与网络解读（含学术论文索引）
├── site/                  # 可浏览 HTML 站点
│   ├── index.html dashboard.html dukou-engine.html curated.html 等
│   ├── data/              # 可视化页（91<!--stats:site_data_html--> 个 HTML，D3/Three；「90<!--stats:visualization_pages--> 可视化页」口径不含模板壳 _shell.html）
│   ├── en/                # 英文站（138<!--stats:site_en_html--> 页）
│   ├── static/js|css|fonts/  # 本地化 D3/Three、tokens.css/system.css、子集化字体
│   └── sitemap.xml
├── scripts/               # Python/JS 工具链（门禁、生成器、审计、诊断）
│   ├── verify_delivery.py # 交付门禁（pre-commit 强制，见 §5）
│   ├── generate_csp.py / inline_css.py / bump_version.py / lint_links.py
│   ├── check_*.py|js      # 各专项门禁
│   ├── run_all.py         # 批量运行 A-AH 34<!--stats:script_classes--> 类分析
│   ├── _*.py|js           # 现行脚本（一次性件按「三档归位」处置·历史批 `_` 件由第 42 门禁 C4 拦）
│   └── output/            # data/*.json（可视化数据源）+ file-index.md + screenshots/
├── dataset/               # 结构化 JSON（可视化/API 数据源）
├── xiyouji-agent-web/     # Web Agent「西游记·渡口问津」（React+Vite+Express）
├── mcp-server/            # MCP 工具（xiyouji_mcp.py：drl_spotcheck 等）
├── tests/                 # pytest + Playwright E2E
├── assets/                # 字体源、图片
├── README.md / STRUCTURE.md / CHANGELOG.md / DESIGN.md / HANDOVER.md / [新Agent启动Prompt](docs/00-导读/新Agent启动Prompt.md)（入口文档·W1011 归位 docs/00-导读）/ CLAUDE.md（AI 速查层·W664）
└── LICENSE + LICENSE-CONTENT.md  # 双协议
```

---

## 4. 关键模块与依赖关系

### 4.1 四层架构（数据流）

```
source/（原著+引用）──生成──► docs/（解读文档）
                                │
docs/ ──分析/抽取──► scripts/output/data/*.json ──► site/data/*.html（可视化页，fetch JSON + EMBEDDED 回退）
                                │
docs/ ──渲染──► site/（导航/索引页，直接链 docs）
```

- **单一事实源**：设计令牌 `site/tokens.css` + 组件层 `site/system.css`，经 `scripts/inline_css.py` 内联进各 HTML（页面自包含、file:// 直开）。
- **数据回退铁律**：所有 site/data 可视化页必须内嵌 `EMBEDDED_DATA`/`EMBEDDED` 回退，fetch 失败时仍可渲染（file:// 双击可用）。

### 4.2 交付门禁体系（verify_delivery.py，pre-commit 强制 · 摘要层）

> **📖 阅读契约（W709）**：索引型——本节=83 槽摘要；完整定义（口径/豁免/历史实证）→ [docs/agent/gates.md](docs/agent/gates.md)；失败排查时按编号查 gates.md。

verify_delivery.py 是提交前唯一硬门禁入口（`.git/hooks/pre-commit` → 本脚本·W698 起本地传 `--scope auto` 分级，CI 与批收尾恒全量，核心 FAIL 返回非 0 阻断）。内含 83 槽，五组：

**内容与同步类（1-5）**：
1. **六文档同步**
2. **范围漂移检测**
3. **A4 计数一致（EXPECT_A4 字面量「209 篇<!--doc-sync:exempt-->」）**
4. **学术研究轨显式引用**
5. **A1 导航相邻性**

**结构与加载类（6-11）**：
6. **docs 全量链接校验**
7. **sitemap 覆盖**
8. **CSP 漂移**
9. **数据漂移**
10. **内联脚本语法**
11. **CSS 结构平衡**

**声明与完整性类（12-15）**：
12. **token 覆盖率**
13. **动效禁止清单**
14. **a11y 对比度**
15. **INLINED CSS 完整性**

**数据与一致性类（16-26）**：
16. **Skills 索引一致性**（W562 退役·编号保留——gates.md 已注明）→ gates.md
17. **索引健康**
18. **元信息块 v2**
19. **术语一致性**
20. **原著引文硬验证**
21. **动态链接门禁**
22. **治理文档维护契约**
23. **旁文档同步**
24. **图表静态自洽**
25. **数据内容一致性**
26. **SEO head**

**编号与质量防线类（27-67）**：
27. **W 号区间字面量**
28. **可视化可引用性**
29. **色盲安全**
30. **窄屏降级声明**
31. **文档口径体检**
32. **CLAUDE.md 速查层完整性**
33. **head 内容合法性**
34. **CSS 变量引用**
35. **声明分隔**
36. **孤立选择器**
37. **kpi-card 基类**
38. **页面内嵌残留标记**
39. **故事内时间线双源同步**
40. **chapter_stats 双源同步**
41. **AGENTS 分层完整性**
42. **根级脚本覆盖**
43. **可视化数据断言**（check_chart_values.js·W753）→ gates.md
44. **英文站 CJK 校验**（validate_en.py·W768）→ gates.md
45. **目录文档新鲜度**（check_folder_docs.py·W780）→ gates.md
46. **搜索索引新鲜度**（check_search_index_fresh.py·W809）→ gates.md
47. **性能影子槽**（check_perf_shadow.py·W849）→ gates.md
48. **计划方案合规槽**（check_plan_template.py·W860）→ gates.md
49. **朱砂实底限额**（check_vermilion_solid.js·W883）→ gates.md
50. **GSAP 动效写法槽**（check_gsap_motion.py·W961）→ gates.md
51. **提交范围槽**（check_commit_scope.py·W1007）→ gates.md
52. **仓库布局槽**（check_repo_layout.py·W1011）→ gates.md
53. **图表中英对拍槽**（check_chart_design_parity.py·W1105）→ gates.md
54. **坑表编号唯一槽**（check_pitfall_id_unique.py·W1110）→ gates.md
55. **PowerShell 解析槽**（check_powershell_parse.py·W1110）→ gates.md
56. **CSP 增量漂移槽**（check_csp_drift.py·W1110）→ gates.md
57. **CSS 变量自引用槽**（check_css_var_selfref.py·W1110）→ gates.md
58. **动效守卫覆盖槽**（check_motion_guard.py·W1135）→ gates.md
59. **design 资产清单对拍槽**（check_design_asset_manifest.py·W1135）→ gates.md
60. **tooltip 多行间距槽**（check_tooltip_spacing.py·W1135）→ gates.md
61. **数据集溯源槽**（check_dataset_provenance.py·W1141）→ gates.md
62. **reader 完整性**（check_reader_integrity.py·W1149）→ gates.md
63. **数据集清单**（check_dataset_manifest.py·W1149）→ gates.md
64. **移动视口**（check_mobile_viewport.py·W1165）→ gates.md
65. **导航一致性**（check_nav_parity.py·W1167）→ gates.md
66. **数据徽标**（check_data_badge_coverage.py·W1167）→ gates.md
67. **统计事件契约**（check_stat_events.py·W1168）→ gates.md

68. **dashboard KPI**（check_dashboard_kpi.py·W1170）→ gates.md
69. **模板结构契约**（check_template_contract.py·W1178）→ gates.md
70. **产物服务地址**（check_no_hardcoded_endpoint.py·W1208）→ gates.md
71. **占位符哈希载体**（check_placeholder_hash_carrier.py·W1210）→ gates.md
72. **emoji 残留棘轮**（W1232）→ gates.md
73. **reader/RSS 产物新鲜度**（W1232）→ gates.md
74. **治理文档体积窗口**（W1232·P2-4 升格）→ gates.md
75. **明暗两态截图差异**（W1264·E-245 机器化）→ gates.md
76. **公共层样式覆盖率**（W1264·样式治理棘轮）→ gates.md
77. **视觉身份判据**（W1264·E-250 机器化）→ gates.md
81. **W1265 新增四槽**（78=EN 数据源语言隔离 / 79=回退块保真度 / 80=SVG 文字对比度 / 81=页面引用闭合性；基线冻结 + `--strict` 零容忍）→ gates.md
82. **图表内容完备度**（W1266·内容层四项：来源标注/结论段/tooltip/图例；渲染级复核 + 页面哈希防绕过闸；存量 175 条）→ gates.md
83. **SVG 标签裁切与重叠**（W1266·四向越界 + 同容器重叠）→ gates.md
**完整定义 → [docs/agent/gates.md](docs/agent/gates.md)**（原文全量·五组分节·内容零改动）。

### 4.3 工具链要点（摘要层 · 坑位全量已迁 L2）

> **⚡ 菩提授业 skill（W1034 建 / W1036 定名 `puti-shouye`）**：16 条最高频硬判据已固化为项目级 skill [`.agent/skills/puti-shouye/SKILL.md`](.agent/skills/puti-shouye/SKILL.md)——**动手前扫一眼**即可避开本项目 90% 的返工（批次收官顺序 / 判据脆弱特征 / 历史段不改写 / 命令禁用省略号等）。完整 390<!--stats:pitfalls_total--> 条见 [pitfalls.md](pitfalls.md)；两者是「速查 → 详查」关系，不重复维护。
> **🔥 火眼金睛 skill（W1149 建·`huoyan-jinjing`）**：全仓巡检速查 [`.agent/skills/huoyan-jinjing/SKILL.md`](.agent/skills/huoyan-jinjing/SKILL.md)——五维扫描（覆盖/失败语义/CI 形态/数据血缘/同类复发）+ 判据 fail-closed + 数据分级 + manifest 对拍 + 链接/内联 + 修复三原则；完整方法论文档在 [docs/10-方法论沉淀/全仓深度审计SOP-可复用.md](docs/10-方法论沉淀/全仓深度审计SOP-可复用.md)，可执行入口 `scripts/audit_repo.py`。

> **📖 阅读契约（W709）**：索引型——390<!--stats:pitfalls_total--> 条坑位按六主题迁 [pitfalls.md](pitfalls.md)（含 shell 场景查坑表）；本节保留主题视图与高频铁则。

**主题视图（W706·按需查坑·正文按批次序不动）**：CSS 类=W557 基类丢失/W558 缺分号/W673 三门禁/W571 inline_css 分发/W582-W589 暗色族；JS 类=W575 空选区/W568 Express close/W674 defer 时序/W656 audit 单模块；git 类=W649 级联清单/W698 scope+safe_commit/W537 三新规/W514 heredoc/W509 BOM 禁；级联类=W553 CRLF/W664 desc 分隔符/W663 跳号先例/W679 日期串误报/W705 插入保留锚点/W1005 跨行吞并；数据类=W691 计数钉/W693 残留标记/W565 部署态冒烟/W703-704 stats 对账；文档类=W520 字面量禁/W496 数字现测/W663 doc-sync/W706 元规则；Windows 类=W509 BOM/W514 heredoc/W535 路径实参/W706 终端编码兜底；视觉类另含素材出图规格（W974 三条：bbox 顶≠主体顶·器物形状>数量·落位页先验）。

**提交前就绪链（W1198 立·W1215 收敛）**——收官 = `python scripts/batch_closeout.py --spec scripts/output/_w###_spec.json`·推送判据 = `python scripts/pre_push_gate.py`；步序细节锚各步 docstring 与坑表 E-229/E-228（正文 → pitfalls）。

**收官链时间纪律（W1266 立·实测单轮浪费 ≈25–30 分钟六则入仓）**——① 提交期门禁分层：提交只靠 pre-commit 的 `--scope auto` 子集复验，全量 verify 恒属 pre_push_gate 不重复跑（E-265）；② 长任务（探针/全量门禁/收官链 >2 分钟）一律后台运行＋输出落文件，前台只做秒级判据（E-266）；③ 门禁红先跑快判据三件套（第 51/74/31 槽＋目标 pytest）再全量（E-268）；④ 收官链失败先单跑失败步续跑，禁整链从头重跑（E-267）；⑤ 渲染/探针报告按页面内容 hash 判定重跑，页面未变即复用（E-270）；⑥ spec 的 file_index_rows 形态一次定形，>200 行直接逐行（E-269）。全量 L2 → [批次交付流水线 §九](docs/10-方法论沉淀/批次交付流水线.md)。

**多副本写入的派生值权威必须由发起方一次生成并两侧同传（W1204）**——详述与契约闸门见坑表 E-221（正文 → pitfalls）。

**最高频铁则（全文见 pitfalls.md）**：改内联脚本必跑 generate_csp.py；批量改 CSS/JS 验括号平衡；多行逻辑禁 shell heredoc 落 Python 文件；同文件 Edit 串行；级联后按清单 git add；认领批次登记 touches·动工前 `preflight_check.py --touches <清单> --self W###` 查在途交集（跨 Agent 版「同文件串行」）；批次收官提交一律 `safe_commit.py --expect-spec scripts/output/_w###_spec.json`（索引只许含本批件·防代提硬拦 W1006）。

**占号共享区纪律（W1110·E-128）**——取号三源并集＋session 仓路径指纹＋跨克隆撞号预警；落段前复核本批号仍在预约集内（正文 → pitfalls E-128）。

**六主题目录 → [pitfalls.md](pitfalls.md)**：CSS / 视觉渲染（80<!--stats:pitfalls_css-->）·JS / CSP / 运行时（12<!--stats:pitfalls_js-->）·git / 提交 / 并发（39<!--stats:pitfalls_git-->）·级联 / CHANGELOG（26<!--stats:pitfalls_cascade-->）·数据 / 内容可信度（17<!--stats:pitfalls_data-->）·流程 / 协作 / 取证（216<!--stats:pitfalls_flow-->）

**本机环境事实（Windows 单机·机器相关不入 L2·随实测滚动更新）**：
- `make` 未安装：Makefile 目标不可用，直调 `python scripts/<对应脚本>`（映射见 Makefile 注释）。
- 全局 Python 3.12·无项目 `.venv`：`pytest`/`playwright`/`pip_audit` 加 `-m` 前缀调用，**三语境分清**——① 仓内文档/工具表/CI/Makefile 一律写可移植形态 `python -m <工具>`（CI 在 Linux·`py` 不存在）；② 本机 PowerShell 侧统一 `py -3 -m`（该侧 `python` 是应用执行存根·调用即 exit 9009 无输出）；③ 本机 git-bash 侧 `python` 为实解释器可直呼。`py -3` 两 shell 一致指向全局 3.12，但**不得写成全仓约定**（`py` 非跨平台·CI/Linux 失效）。`ruff`/`uv`/`node`/`npm`/`git`/`gh`/`pwsh` 可直呼。
- `pwsh`（PowerShell 7）与 `powershell`（5.1）并存：需 PowerShell 时一律用 `pwsh`（默认 UTF-8 无 BOM）；`powershell` 是 5.1（GBK 默认·W509 BOM 坑源），且仍遵守仓内「禁 PowerShell 写仓内文件」铁则。
- 提交门禁 hook（.git/hooks/pre-commit）与本清单同口径取解释器：首选 `py -3`，回退系统 Python 3.12 绝对路径，两者均须实测可运行（`-c "import sys"` 返回 0）才选用；**不按 PATH 上的 `python`/`python3` 形状挑选**（两 shell 解析不同·见上一条）·不依赖任何厂商托管运行时路径。
- pre-commit 框架**已装**（实测 4.6.0·W1014 订正本条与磁盘现势的矛盾）但**禁 `install`**：`pre-commit install` 会覆盖手写 `.git/hooks/pre-commit`，破坏零依赖门禁。`.pre-commit-config.yaml` 仅为「误 install 后核心门禁不丢」的等价备份（W424），现役执行路径恒为手写钩子；W1014 已删其指向退役件 `sync_docs.py` 的坏 hook 段。
- 本机取数与命令坑（W902 自 Agent 记忆固化·长期实测）：`curl` 必须 `--ssl-no-revoke`（本机代理链下否则大面积失败）；`/tmp` 对 Windows Python 不可见（Git Bash 的 /tmp 是 MSYS 虚拟路径·Python 侧须用 `tempfile` 或仓内 tmpe/）；`gh api` 查询含中文的 search 语句必须走 `-f` 参数（URL 参数形态中文被编码截断）；PMC 取 PDF 常挂 Cloudflare → 用 Europe PMC `fullTextXML` 端点兜底。
- **Bash 工具工作目录跨调用持久（W596 两犯）**：某条命令 `cd 子目录` 后，后续所有相对路径命令都落在子目录——长批次开头 `cd /d/xiyouji` 归位或全程绝对路径；「找不到文件」先查 pwd。
- **Edit 工具前置 Read**：Edit 前必须先用 Read 工具读过该文件（sed/grep 的 Bash 读取不算）——直接 Edit 报 "File has not been read yet"；批量编辑前先对每个目标文件发 Read。
- `pyyaml==6.0.2` 已登记进 CI 真实安装源 `scripts/requirements-hashed.txt`（W813 立判据·W1195 起 CI 安装源改哈希化清单·W1198 改绑）：工作流 YAML 可解析性守卫（test_ci_wiring.py J3）依赖它，依赖缺失即**判红**（禁静默跳过假绿）。

### 4.4 Web Agent（xiyouji-agent-web/ · 摘要层）

> **📖 阅读契约（W709）**：索引型——引擎/前端/权限细节 → [docs/agent/agent-web.md](docs/agent/agent-web.md)。

后端 `server/index.ts`（Express + SSE 流式 + SQLite）+ 自研 OpenAI-compatible 引擎 `server/engine/`（W680·全主流大模型端点适配）；凭证 `LLM_API_BASE`/`LLM_API_KEY`/`LLM_MODEL` 配服务端 .env；核心入口与安全边界（权限四模式/受保护路径/命令白名单）见 L2。
## 5. 构建与运行方式

### 5.1 统一编排（Makefile）

> **环境依赖**：Makefile 目标需预装 `make`（Unix/WSL 原生；Windows 若无 make，可直接调 `python scripts/` 下对应脚本——各目标的脚本映射见 Makefile 注释）。

```bash
make help          # 查看全部目标
make analyze       # 批量运行 A-AH 34<!--stats:script_classes--> 类分析（scripts/run_all.py）
make test          # pytest tests/ -q
make audit         # 表格无容器 + JS 语法 + SVG 负宽度检查
make lint          # ruff + eslint
make links         # 全仓库链接校验（lint_links.py --dir .）
make ci            # lint + test + audit + links + data-validate + docs-index（本地预跑 CI）
make release       # 发布前体检（release.py）
make screenshots   # Playwright 双视口截图
```

### 5.2 交付门禁（提交前必跑）

```bash
python scripts/verify_delivery.py        # 全部门禁，核心全绿才可提交
python scripts/pre_push_gate.py          # W1215：一命令真全量（推送判据·四步见 --steps）
python scripts/batch_closeout.py --spec scripts/output/_wNNNN_spec.json  # W1215：收官链单入口（cascade→…→gate）
python scripts/generate_csp.py --check   # CSP 0 漂移
python scripts/check_js_syntax.py --all  # 全站内联脚本语法（与 make ci / CI 同轨）
python scripts/check_structure.py        # 全站 CSS 结构平衡
python scripts/lint_links.py --dir .     # 全仓链接校验（与 make links 同轨）
```

**检查层次映射（W706·什么改动跑哪层）**：md 治理文档→verify --scope docs（pre-commit auto 分类）；site HTML/CSS/JS→verify --scope site + generate_csp --check + check_structure；scripts Python→ruff + pytest 全量（计数钉）；数据面（dataset/生成器/内嵌副本）→对应双源门禁（第 39/40）+ 旧值标记扫描；CI 推送恒全量不缩水；本地绿≠CI 绿——目标侧不入仓件先 worktree 预演（W700 教训）。

### 5.3 站点本地浏览

```bash
# 纯静态，直接双击 site/index.html（file:// 直开，无需任何软件）
# 或用本地 http 服务（部分页面的 fetch 实时数据源需 http 模式）：
python -m http.server 8000   # 然后访问 http://127.0.0.1:8000/site/
```

### 5.4 Web Agent 运行

```bash
cd xiyouji-agent-web
npm install
npm run dev          # 同时拉后端 :3000 + 前端 :5173
# 需先复制 .env.example → .env 并填入 LLM_API_BASE / LLM_API_KEY / LLM_MODEL
```

### 5.5 测试

```bash
pytest tests -q                        # pytest 全量（含 MCP 工具测试）
cd scripts && npm install && npm run test:e2e   # 三层 E2E
```

---

## 6. 必须遵守的铁律

1. **六文档同步（W393 降级）**：每完成一个 W 批次，核心 2（CHANGELOG + HANDOVER）必须写，辅助 4（README/STRUCTURE/项目说明/file-index）里程碑时跑 bump_version.py 补齐。
2. **E1 铁律（声明 ≠ 落地）**：每个文件修改后 Grep spot-check 验证落地，禁止假收敛。
3. **改内联脚本 → 重跑 generate_csp.py**（CSP 哈希失配会整脚本被拒）。
4. **批量改 CSS/JS → 验证括号/引号平衡**（check_structure.py）。
5. **file:// 铁律**——规则一句版与判据细节归 RULES.md / pitfalls.md 对应条目（本层只留标题检索锚）
6. **新页落地**：可视化页进 site/data/、索引进 site/ 根 + tag-cloud + sitemap；禁往 site/chapters|characters|themes（空遗留目录）。
7. **先取证再假设**：诊断前端显示问题，先拿截图 + Console + 复现条件，再下根因结论（见 docs/10-方法论沉淀/前端显示问题诊断SOP.md）。
8. **禁止擅改**：CHANGELOG 历史段、归档 3 份、.env、SECURITY-AUDIT 档、verify_delivery.py、bump_version.py 等门禁脚本（详见文档规范 §11.2）。
9. **禁重跑 w286_merge_yuanwen_shendu.py**（A1 深度解读 SD 编号会再次错位）。
10. **批量重写脚本改完**：`git diff --name-only` 对比改动范围，非必要改动 `git restore` 回退。
11. **双协议**：代码 MIT + 文本 CC BY-NC 4.0（非商用），拆分 LICENSE / LICENSE-CONTENT.md。
12. **动效契约**——规则一句版与判据细节归 RULES.md / pitfalls.md 对应条目（本层只留标题检索锚）
13. **内容可信度轨（W505-W508 固化）**：docs/01-06 新内容必须走元信息块 v2（第 18 门禁）+ 术语一致性（第 19 门禁）+ 引文硬验证（第 20 门禁）；引文须经 `_cite_probe.py` 提取候选（§4.3），管线产出须过 `_check_pipeline_consistency.py`；归档/删除脚本须同步查 tests/ 引用（W506 教训，见 day-review skill 步骤 4-6）。
14. **修实例必修根（W998 固化）**：修复暴露同类风险时，同批或次批根治，禁止「值得排期/等点号」收尾（真需用户决策的仅限外发动作）；检查任务按委托字面范围执行；跨会话教训权威落坑表与本节，私有记忆仅作镜像（W516 载体铁则·治理季三次用户问责实证）。
15. **禁止补丁加补丁，修复必须从根因**——规则一句版与判据细节归 RULES.md / pitfalls.md 对应条目（本层只留标题检索锚）
16. **协作与环境约束**——规则一句版与判据细节归 RULES.md / pitfalls.md 对应条目（本层只留标题检索锚）
17. **开批先预约号**——规则一句版与判据细节归 RULES.md / pitfalls.md 对应条目（本层只留标题检索锚）
18. **提交前三问自检**——规则一句版与判据细节归 RULES.md / pitfalls.md 对应条目（本层只留标题检索锚）
19. **禁用 CodeBuddy/WorkBuddy（W1061 入必载层·用户 2026-10-07 两度重申·此前仅存私有记忆=三问 ③ 违规实例）**：项目一切 AI 功能不使用 CodeBuddy/WorkBuddy 及其任何残留；agent-web 的三选一裁决=保留但换引擎（OpenAI-compatible 自研·W680 收官/W681 事实收官）。任何会话不得引入、恢复或仿建该品牌工具链。

20. **Python 改动结构检查（W1077 立·用户令）**：改动 .py 后必须跑 `pwsh -File scripts/guardrails/check_changed.ps1`（ruff 风格档/结构档/嵌套推导式，退出码 0 才过；`api_diff.py` 报破坏性变化须在提交说明写明）；阈值与收紧路线见 docs/agent-guardrails/README.md；新增阈值/豁免须按 16-⑦ 报批。
21. **CI 推送节奏**——规则一句版与判据细节归 RULES.md / pitfalls.md 对应条目（本层只留标题检索锚）
22. **治理文档体积上限与批量归档**——规则一句版与判据细节归 RULES.md / pitfalls.md 对应条目（本层只留标题检索锚）
23. **异常分类必须与失败语义对齐**——规则一句版与判据细节归 RULES.md / pitfalls.md 对应条目（本层只留标题检索锚）

24. **并行会话必须工作树隔离**——规则一句版与判据细节归 RULES.md / pitfalls.md 对应条目（本层只留标题检索锚）

---

## 7. 快速上手路径（新 Agent 接手）

0. 开局先跑 `python scripts/agent_start.py`——实读磁盘输出当前事实摘要（现役三元组/近 3 批次/stats 全键/对账表现势/阻塞·W705）——防「记忆代读」，值全部来自磁盘实时读取。
   **W1179 必跑清单**：`python scripts/agent_start.py --task` 除必读节外，另按 git 改动路径输出「变更类型 → 必跑动作」（新增页 / 新增内容文档 / 新增门禁槽 / 改共享 CSS / 改口径块五类，命令由台账批号与改动路径实况推导，可直接粘贴）；工作树干净时动手前用 `python scripts/agent_start.py --checklist all` 主动查，或 `--checklist new-page` 等按类型查；`--checklist-selftest` 验四类命中、批号口径与命令完整性。每条带坑表 E-NN / 门禁槽号 / W 批次依据锚，便于 Grep 检索核对，防清单与源漂移。
1. 读 `CLAUDE.md`（AI 速查层，1 分钟）→ 必守规则与常用命令速览（W664 起，宿主自动加载）；**四文档体系分工**（W1157 建）：规则全量查 `RULES.md` / 坑位表查 `pitfalls.md` / 本文件=项目全貌·工作流程（§7）与门禁摘要正本。
2. 读 `HANDOVER.md`「零、当前阻塞」+「一、当前进度」→ 当前 HEAD（vX.Y.Z W###）、下一 W 编号、遗留待办。
3. 读 `README.md` → 项目全貌、内容规模、在线站点、双协议。
4. 读 `docs/00-导读/文档规范.md` §11 → 文件管控清单（必同步/禁擅改/接手速查 6 步/同步核对 10 项<!--doc-sync:exempt-->）。
5. 读 `HANDOVER.md`「三、方法论沉淀」→ 经验**总入口**（W755 起指针化：现役坑位/门禁读 [pitfalls.md](pitfalls.md) 与 [docs/agent/gates.md](docs/agent/gates.md)，深度篇读 [docs/10-方法论沉淀/](docs/10-方法论沉淀/README.md)）。
6. 深挖结构看 `STRUCTURE.md`、`scripts/output/file-index.md`（反向索引）、`CHANGELOG.md`（正向时间线）。
7. 动手前跑 `python scripts/verify_delivery.py` 确认基线全绿。

---

## 8. 权威文档（冲突时以此为准）

> **清单间裁定链（W706）**：文档规范 §11（文件管控）> CHANGELOG 现役段 > HANDOVER。本节与 CLAUDE.md（速查指针）、CONTRIBUTING（贡献者协作面）系三视角清单，内容不一致时按裁定链与本节为准。

- 进度中枢 / 规则：`HANDOVER.md`、[docs/00-导读/新Agent启动Prompt.md](docs/00-导读/新Agent启动Prompt.md)（速用精简版）、`CLAUDE.md`（AI 速查层·W664）
- **规则与流程入口（W1157 四文档体系）**：[RULES.md](RULES.md)（必守规则单一入口·索引层）+ [pitfalls.md](pitfalls.md)（坑位表正本·本批自 docs/agent/ 迁根）；工作流程以本文件 §7 为正本
- 文档规范：`docs/00-导读/文档规范.md`（尤其 §11 文件管控）
- 设计规范：`DESIGN.md`（§1-4 视觉 / **§5 动效契约**）
- 目录结构：`STRUCTURE.md`
- 变更日志：`CHANGELOG.md`（正向）+ `scripts/output/file-index.md`（反向）
- 诊断 SOP：`docs/10-方法论沉淀/前端显示问题诊断SOP.md`

---

*本文件由 AGENTS 通读项目后生成于 2026-08-16（v2.3.73 W458）；W458-W707 沿革已迁 [archive/docs/AGENTS-ARCHIVE.md](archive/docs/AGENTS-ARCHIVE.md)（W709 建·W1271-W1271 级联自动滚动·脚注保留最近 5 条·每条 ≤120 字·日期阿拉伯形态·grep 查勿通读）；2026-11-18（W1272）：台账回填三缺陷根修（首笔语义倒置 / 列位错位 / 认领行形态）+ 脚注尾锚点契约同源 + 上一批收官尾段闭合；2026-11-18（W1273）：公共层归并铺开 + 内联 CSS 残渣判据 + 批三范围建议；2026-11-18（W1274）：公共层外链化样板 + 外链化工具 + 覆盖率实际加载面新维度 + 铺开计划；2026-11-18（W1275）：公共层外链化 site/en 全站 138 页 + 索引口径同源 + 外链形态优先；2026-11-18（W1276）：公共层外链化铺开第一批 site/en 全站 138 页 + 两处门禁口径修订。；2026-11-19（W1277）：对抗审查 P3 五项根修 + verify 回放缓存（同树免重跑全量）+ 83 基线重生成。；2026-11-19（W1278）：pitfalls 二层化（407.6→284.8KB·221+15 条归档）+ AGENTS 摘要化（48.2→31.8KB）+ 74 槽挂窗。如与上述权威文档冲突，以权威文档为准。*
