# AGENTS.md — 《详解西游记》项目 Agent 指南

> **📖 阅读契约（W707）**：索引型——不要线性通读。先跑 `python scripts/agent_start.py --task` 拿「本次任务相关」清单按需读节；§4.2 全 69 槽门禁与 §4.3 全部坑位属按需查表（L2 已拆分落地：docs/agent/gates.md · pitfalls.md · agent-web.md·W709）；§1-§3/§6 铁律/§7 必读。
>
> 本文件面向进入本仓库工作的 AI Agent（及新接手的人类维护者），提供项目的用途、技术栈、目录结构、关键模块、依赖关系、构建运行方式与必须遵守的铁律。动手前按 §7 路径按需读节；更细的规则以文末「权威文档」为准。
>
> **维护契约（防乱写）**：本文档是 Agent 协作指南，只允许结构性编辑——① 保持 §1–§8 骨架不变；② 新增铁律/规则必须**就地并入对应章节**并全篇去重（禁止追加「速记 / 补充」尾部段落）；③ 版本脚注更新须与当前 HEAD（vX.Y.Z W###，用 `git rev-parse --short HEAD` 核对）一致；④ 与 HANDOVER / 文档规范 / CHANGELOG 冲突时以后三者为准；⑤ 摘要层纪律：条目一行一事，叙事与验证细节归 L2（gates/pitfalls/CHANGELOG），过期数字随批纠偏。

---

## 1. 项目用途与定位

**《详解西游记》**（xiyouji）是一个「一源多形 · 数字人文可视化解读《西游记》100 回」的项目。它把《西游记》的文本研究组织为四层产物：

- **文档（Docs）**：Markdown 写就的逐回解读、人物分析、主题专题、文化背景、诗词赏析、个人随笔。
- **站点（Site）**：可浏览的纯静态 HTML 站点，`file://` 双击即可打开，部署于 GitHub Pages（https://1273984347.github.io/xiyouji/ ）。
- **数据可视化**：89<!--stats:visualization_pages--> 个 D3.js / Three.js 可视化页（site/data/ 共 90<!--stats:site_data_html--> 个 HTML，「87」不含模板壳 _shell.html），覆盖 133 个<!--doc-sync:exempt--> 数据维度（章节统计、人物关系网络、八十一难热力图、取经路线、情感热力图、AI 对话等 34<!--stats:script_classes--> 类主题 A–AH）。
- **可问询入口**：Web Agent「西游记·渡口问津」（xiyouji-agent-web/）——自研 OpenAI-compatible 引擎（server/engine/·W680·全主流大模型端点适配），可对话、检索 docs/source、跑脚本。

**核心内容规模**：A1–A6 内容板块共 623<!--stats:a1_a6_docs--> 篇（A1 逐回 100 / A2 随笔 44 / A3 人物 215 / A4 主题 209 / A5 文化 35 / A6 诗词 13；算法与边界见 docs/00-导读/统计口径说明.md；W505 起 611→616）；英文站 site/en/ 138<!--stats:site_en_html--> 页已全量英文化。

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
│   ├── data/              # 可视化页（90<!--stats:site_data_html--> 个 HTML，D3/Three；「89 可视化页」口径不含模板壳 _shell.html）
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

> **📖 阅读契约（W709）**：索引型——本节=69 槽摘要；完整定义（口径/豁免/历史实证）→ [docs/agent/gates.md](docs/agent/gates.md)；失败排查时按编号查 gates.md。

verify_delivery.py 是提交前唯一硬门禁入口（`.git/hooks/pre-commit` → 本脚本·W698 起本地传 `--scope auto` 分级，CI 与批收尾恒全量，核心 FAIL 返回非 0 阻断）。内含 69 槽，五组：

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
16. **Skills 索引一致性**（W562 退役·编号保留——gates.md 已注明·摘要侧补记 W1154）
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
43. **可视化数据断言**（check_chart_values.js·W753）
44. **英文站 CJK 校验**（validate_en.py·W768）
45. **目录文档新鲜度**（check_folder_docs.py·W780）
46. **搜索索引新鲜度**（check_search_index_fresh.py·W809）
47. **性能影子槽**（check_perf_shadow.py·W849·影子模式不判红）
48. **计划方案合规槽**（check_plan_template.py·W860·增量口径·只判本次变更引入的新缺项）
49. **朱砂实底限额**（check_vermilion_solid.js·W883·v4 规格 §3.2 阶段 5 落地·浏览器计算样式实测·每页非豁免 >3 处 FAIL·豁免读 _w864_accent_exemptions.json·增量缓存按页 hash）
50. **GSAP 动效写法槽**（check_gsap_motion.py·W961·site/static/js/ 自有 JS 动效判据——时长 ≤600ms/缓动白名单/禁大角度旋转与无限循环/只动 transform+opacity·J2 宪法级禁词不可豁免）
51. **提交范围槽**（check_commit_scope.py·W1007·代提三次同一处方）——归属批次取索引态 CHANGELOG 顶段（新增段=本批，否则 HEAD 现役段=回填），该批 `scripts/output/_w####_spec.json` 的 `file_index_rows` 即应动全集；索引态路径集多出即 FAIL（＝一份提交夹带他方在途件）。恒跑（_SCOPE_CORE·docs/site 提交也判）；无暂存件 NOTE 放行、spec 缺失 WARN 放行（不伪造红）。
52. **仓库布局槽**（check_repo_layout.py·W1011·「整理分类」的长期形态）——L1 根目录只放治理与配置（白名单 ROOT_FILES·出现未声明文件即 FAIL 并给去向）；L2 顶层目录必须已在 TOP_DIRS 与 STRUCTURE.md 声明角色；L3 声明了但磁盘不存在 ⇒ FAIL（防白名单陈腐）。判据按 **git 视角**（被 .gitignore 忽略的本地件不计）；毫秒级·登记 `_SCOPE_CORE` 恒跑。
53. **图表中英对拍槽**（check_chart_design_parity.py·W1105）——chart-design 中英两版（site/data/chart-design.html 与 site/en/chart-design.html）逐键数值对拍：数值必须全等（非数值专名差异属本地化预期·只列不判红·单侧键即 FAIL）+ **强制契约标记中英齐平**（reduced-motion JS 守卫 `MOYUN_RM` / tooltip 统一类名 `chart-tooltip` / CSS 兜底 `prefers-reduced-motion`）——一侧缺标记即 FAIL（实证：EN 版缺 JS 守卫正是本槽抓出）。基础设施缺失（页面或 summary.json 不可读）按 fail-closed 退出码 2·不静默放过。
54. **坑表编号唯一槽**（check_pitfall_id_unique.py·W1110）——坑表条目的 E-NN 编号是「按编号检索教训」的唯一键，但第 31 门禁只统计**条数**、不校验**编号唯一性** ⇒ 两批各占同一号时计数链五处全绿、CI 全绿，而检索静默取到错的那一条（W1109 收敛 16 组真重号后本槽成为常驻防线）。判据分层：**新增条目撞既有编号 ⇒ FAIL**（本批引入的）· 存量同号 ⇒ NOTE（不判红·避免存量拖死新批）· 条目本体口径（行首「- **」且含「（W#### 实证·E-NN）」⇒ 正文引用不算本体）。恒跑（任何提交都可能改坑表）。
55. **PowerShell 解析槽**（check_powershell_parse.py·W1110）——仓内 `.ps1` 此前**零机器判据**：语法写坏只在运行时才报错 ⇒ pre-commit 守门链**静默失效**；且含非 ASCII 的 `.ps1` 缺 UTF-8 BOM 时 Windows PowerShell 5.1 的 `-File` 加载器回退 ANSI 代码页 ⇒ CJK 关键字**解析静默死亡**（E-68·而 pwsh 7 默认 UTF-8 ⇒ 本机跑得通 ≠ 5.1 跑得通）。两判据：C1 用官方 AST 解析器（`Parser::ParseFile`·只读不执行）逐文件解析，语法错误即 FAIL·解析器缺失按 fail-closed 退出码 2；C2 含非 ASCII 必须带 UTF-8 BOM（纯 ASCII 无 BOM 安全·不判红）。扫描域=tracked 的 `.ps1`（`archive/` 豁免）。
56. **CSP 增量漂移槽**（check_csp_drift.py·W1110）——既有第 8 槽 `generate_csp.py --check` 是**全站**校验，不区分「谁改的」且无归因信息 ⇒ 存量漂移掩盖本批真问题、本批漂移被存量噪音淹没。增量口径：**交集判红**（本批改动页 ∩ CSP 漂移页 ≠ ∅ 即 FAIL）+ **merge-base 基点**逐段字节比对（只对本批碰过的内联段判漂移·CI 浅克隆无基点时退化为全段判·不漏判）+ **失败信息三要素**（漂移页 / 命中段标识 / 修复命令 `python scripts/generate_csp.py`）。
57. **CSS 变量自引用槽**（check_css_var_selfref.py·W1110）——W1108 批把 chart-design 两页 INLINED 副本 `:root` 里的图表令牌定义改成「`--chart-1: var(--chart-1)`」**自引用** ⇒ 浏览器在 computed-value time 判为**无效值** ⇒ `getComputedStyle` 返回**空串** ⇒ 连带动使用它的 `--accent` 一并失效 ⇒ 图表主题色回落为黑/继承色（实测：改前 `--chart-1=#C8463A`·改后空串）。此类缺陷**全链无红灯**（CSP/结构/内联语法等门禁都不看 CSS 变量语义·页面照常渲染只是颜色不对）⇒ 机器判据缺位是根因。判据：扫 `site/**/*.html` 的全部 `<style>` 块 + `site/tokens.css`，任何 `--X: var(--X)` 同名自引用 ⇒ FAIL（带 fallback 的自引用仍判红·fallback 只在变量未定义时生效）。恒跑（毫秒级·与改动范围无关）。
58. **动效守卫覆盖槽**（check_motion_guard.py·W1135）——站内 reduced-motion 契约（DESIGN.md §5.3）要求用户开启「减少动态效果」时 d3 图表的 `.duration()/.delay()` 必须归零，但既有门禁只清零**裸数字实参**（BARE）⇒ **表达式实参**（EXPR）未套守卫 ⇒ reduced-motion 用户仍会经历动效与延迟（机器判据缺位是根因）。判据：实参取宽口径（括号平衡扫描·窄口径正则会漏掉含嵌套括号的实参）后分档——GUARDED（实参含守卫变量 `MOYUN_RM` 或 `REDUCE_MOTION`·站内两种命名皆可）/ EXPR / BARE，GUARDED 之外一律判红；含调用点的页另须声明守卫变量。退出码：0 = 通过 / 1 = 判红 / 2 = 基础设施缺失（fail-closed）；`--report` 只报不判红。
59. **design 资产清单对拍槽**（check_design_asset_manifest.py·W1135）——`assets/design/` 目录文档声明过磁盘上不存在的文件，且代码块里的旧目录树整段指向已废弃的一次性工作区 ⇒ 清单失准只能靠人工发现。判据：条目取三来源并集（反引号条目 + 代码块目录树按**缩进栈**还原层级 + 命令形态路径条目）；**硬错**只判「声明存在但磁盘不存在」，外部引用 / 通配占位 / 枚举合并 / 仓库根引用四类降为 NOTE 不判红，「磁盘存在但未声明」只作 NOTE。退出码：0 = 通过 / 1 = 判红 / 2 = 基础设施缺失（fail-closed）；`--report` 只报不判红。
60. **tooltip 多行间距槽**（check_tooltip_spacing.py·W1135）——W1105 批把 EN 站私有 `.tooltip{}` 盒样式收敛为规范 `.chart-tooltip`，但遗留 ZH 页的旧类名规则从未命中（死代码）⇒ tooltip 多行内容一直挤在一起。判据（运行层·playwright·file:// 直开·亮/暗双主题）：CSSOM 中命中规范规则 `.chart-tooltip div + div` + 第二行计算样式 `margin-top` == `--space-2` 解析值 + 旧死规则 `.tooltip div + div` 残留为零 + 双主题读数一致。退出码：0 = 通过 / 1 = 判红 / 2 = 基础设施缺失（playwright/浏览器不可用·fail-closed）；`--report` 只报不判红。
61. **数据集溯源槽**（check_dataset_provenance.py·W1141）——dataset 必填字段 / 引用闭合 / 权重区间 / 引文精确性四类判据 + 两个数据集的专项校验（完整定义见 gates.md）。
62. **reader 完整性**（check_reader_integrity.py·W1149）——`site/reader` 独立生成、此前无专属判据：C1 可见正文禁「（待补）/待完善/TODO」；C2 GitHub `blob|tree/main/<path>` 必须映射仓内真实文件；C3 内容页恰一个 h1（跳转页豁免）；C4 标题唯一。恒跑（扫全量 reader 页·秒级·`_SCOPE_CORE`）；汇总行恒为 `---- 第 62 门禁 reader 完整性：N FAIL（扫描 N 页） ----`；自测 6 例；单测 `tests/unit/test_w1149_reader_dataset.py`。
63. **数据集清单**（check_dataset_manifest.py·W1149）——dataset 快照层防退化：C1 README 行 ↔ 磁盘 ↔ 大小/条目数；C2 `_schema.weight_scale` 量纲与 sankey 端点索引；C3 `chapter/回目` 只允许 1–100 或 `null`+`chapter_scope`（禁 0 哨兵）；C4 空数组/null 必须有状态归类；C5 `deprecated` 必须有 note + 存在的 replacement_page。恒跑（读 46 JSON·毫秒级·`_SCOPE_CORE`）；汇总行恒为 `---- 第 63 门禁 数据集清单：N FAIL（扫描 N 文件） ----`；自测 6 例；单测同 62。
64. **移动视口**（check_mobile_viewport.py·W1165）——375px/320px 触摸目标与内容可达性静态契约（A 层契约 7 项<!--doc-sync:exempt 契约数由 CONTRACT_IDS 派生的功能描述·非漂移值（原条目同款豁免随压缩保留）-->）+ 双视口探针报告采信（完整定义见 gates.md）。
65. **导航一致性**（check_nav_parity.py·W1167）——audit-1 唯一 major（跨页主导航不一致）的判据化：主导航正本 `scripts/w1167_nav_inject.py` 全站分发后，「一致率 100%」不再靠人眼。判据四则（MARK 恰一次 / nav-item 文本序==正本 ZH·EN 六项 / aria-current ≤1 / 有 MARK 无结构=破损红）；判据**同源引用**正本模块不复制清单（W1120 引用不复制纪律）。恒跑（静态扫描·毫秒级·`_SCOPE_CORE`）；汇总行恒为 `---- 第 65 门禁 导航一致性：页面 N · 违规 M · OK|FAIL ----`；自测 5 例（含双高亮与结构剥壳负样本）；退出码 0/1/2（正本不可读=fail-closed）。
66. **数据徽标**（check_data_badge_coverage.py·W1167）——三态徽标 100% 覆盖 + 读者语言判据化（MARK 恰一次 / data-status 分类 / ds-label 逐字，完整定义见 gates.md）。
67. **统计事件契约**（check_stat_events.py·W1168）——删调用/改事件名/清单与代码漂移此前全链零红灯。清单正本 `scripts/output/_w1168_stat_events.json`（11 组 21 名）+ 判据六则：C1 slug 唯一 / C2 有清单必有落点（`file`·`files` 同等）/ C3-C4 源面与页面面反向对拍未登记名即红 / C5 metric 反向链（结构性要求·gitignore 件缺失只作 NOTE）/ C6 `runtime_layer` ∈ {bridge, goatcounter} 必填（探针按声明层取数，读错面即恒 0 假红）。恒跑·`_SCOPE_CORE`；汇总行形态同 65/66 槽；自测 10 例；运行面 `scripts/stat_event_probe.py`（P1-P7·手动跑）。

68. **dashboard KPI**（check_dashboard_kpi.py·W1170）——首页 KPI 卡片硬编码数与 stats.json 磁盘实算对拍（完整定义见 gates.md）。
69. **模板结构契约**（check_template_contract.py·W1178）——模板与新页必须含四项完整标签串（类名/CSS 命中不算证据，完整定义见 gates.md）。
**完整定义 → [docs/agent/gates.md](docs/agent/gates.md)**（原文全量·五组分节·内容零改动）。

### 4.3 工具链要点（摘要层 · 坑位全量已迁 L2）

> **⚡ 菩提授业 skill（W1034 建 / W1036 定名 `puti-shouye`）**：15 条最高频硬判据已固化为项目级 skill [`.agent/skills/puti-shouye/SKILL.md`](.agent/skills/puti-shouye/SKILL.md)——**动手前扫一眼**即可避开本项目 90% 的返工（批次收官顺序 / 判据脆弱特征 / 历史段不改写 / 命令禁用省略号等）。完整 224 条仍在本节下方的 pitfalls；两者是「速查 → 详查」关系，不重复维护。
> **🔥 火眼金睛 skill（W1149 建·`huoyan-jinjing`）**：全仓巡检速查 [`.agent/skills/huoyan-jinjing/SKILL.md`](.agent/skills/huoyan-jinjing/SKILL.md)——五维扫描（覆盖/失败语义/CI 形态/数据血缘/同类复发）+ 判据 fail-closed + 数据分级 + manifest 对拍 + 链接/内联 + 修复三原则；完整方法论文档在 [docs/10-方法论沉淀/全仓深度审计SOP-可复用.md](docs/10-方法论沉淀/全仓深度审计SOP-可复用.md)，可执行入口 `scripts/audit_repo.py`。

> **📖 阅读契约（W709）**：索引型——314 条坑位按六主题迁 [pitfalls.md](pitfalls.md)（含 shell 场景查坑表）；本节保留主题视图与高频铁则。

**主题视图（W706·按需查坑·正文按批次序不动）**：CSS 类=W557 基类丢失/W558 缺分号/W673 三门禁/W571 inline_css 分发/W582-W589 暗色族；JS 类=W575 空选区与触屏坑/W568 Express close 语义/W674 defer 时序/W656 audit 单模块；git 提交类=W649 级联清单与并行互斥/W698 scope+safe_commit/W537 三新规/W514 heredoc/W509 BOM 禁；级联类=W553 CRLF 翻倍/W664 desc 分隔符/W663 跳号手工先例/W679 日期串误报/W705 插入保留锚点/W1005 跨行吞并+尾缀白名单；数据类=W691 计数钉与旧值扫描/W693 残留标记门禁/W565 部署态冒烟/W703-704 stats 对账；文档类=W520 字面量禁/W496 数字现测/W663 doc-sync/W706 元规则与标识符禁令；Windows 类=W509 BOM/W514 heredoc/W535 路径实参/W706 终端编码兜底；视觉渲染类另含素材出图规格（W974 三条：bbox 顶≠主体顶·出图器物形状类别>数量计数·落位页先验）。

**提交前就绪链（W1198·E-220）**：定位走局部判据单跑（check_doc_sync / check_plan_template / 相关 pytest / 守卫脚本）·全量 verify_delivery 只在提交前跑一次；就绪链一次跑完且顺序不可换（git add → **batch_cascade --apply** → gen_folder_docs --refresh → docs_index → _gen_search_index → generate_csp → stats --w → rebuild_section → **gen_folder_docs --refresh（rebuild 改 file-index 后须再刷目录索引）** → spec/touches 同步 → 一次全量门禁）·一次 push 带齐全部内容（禁中途追加 commit·一 push = 一轮 CI）·外部工具判据先读源码/--help 读全·spec 只写一次按最终 git status 生成。

**最高频铁则（全文见 pitfalls.md）**：改内联脚本必跑 generate_csp.py；批量改 CSS/JS 验括号平衡；多行逻辑禁 shell heredoc 落 Python 文件；同文件 Edit 串行；级联后按清单 git add；认领批次登记 touches·动工前 `preflight_check.py --touches <清单> --self W###` 查在途交集（跨 Agent 版「同文件串行」）；批次收官提交一律 `safe_commit.py --expect-spec scripts/output/_w###_spec.json`（索引只许含本批件·防代提硬拦 W1006）。

**占号共享区纪律（W1110·E-128·W1121 根修）**：`reserve_w.py` 的预约集在 W1120 前只写工作树内 `tmpe/_w_reservations.json`（已 gitignore）⇒ 共享范围=工作树而非仓库 ⇒ 隔离 clone/并行 worktree 的占号他方看不见 ⇒ 实测撞号。**W1121 根修**＝取号集合改「本仓表 + 同机兄弟克隆表 + 用户级共享表」三源并集（同名取 ts 最新·写共享表前先合并他人记录不覆盖）+ session 标识含仓路径指纹 + 同号多会话打印跨克隆撞号预警 + release 只撤本工作树且 session 相同的号。**纪律**：落段前复核「本批号仍在预约集内」，且占号必须在与并行会话共享的克隆里执行（叙事与实证细节 → pitfalls E-128）。

**六主题目录 → [pitfalls.md](pitfalls.md)**：CSS / 视觉渲染（48）·JS / CSP / 运行时（12）·git / 提交 / 并发（32）·级联 / CHANGELOG（26）·数据 / 内容可信度（15）·流程 / 协作 / 取证（181）

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
5. **file:// 铁律**：新页面必须内嵌 EMBEDDED 回退、零外域依赖（D3/Three 本地引用 `site/static/js/`，禁 d3js.org/cdnjs 外域 CDN）。**具名例外**（W1167 G0-1 拍板·W1168 收敛为单轨·铁律 16⑦ 留痕）：唯一放行外域是 GoatCounter 回传域 `connect-src https://1273984347.goatcounter.com`；`script-src` 自 W1168 起再次为空集——GA4 轨退役（账号未建 + 大陆可达性差 + web vitals/自定义事件改由自托管链承载），统计改由自托管 `goatcounter.js` + `site/static/js/stats.js` 桥发起。例外全集唯一定义在 `scripts/generate_csp.py`（`EXTERNAL_SCRIPT_HOSTS`/`ANALYTICS_CONNECT_HOSTS`），与配置端点不一致由第 67 槽 C5 + 第 56 槽增量漂移拦下；例外之外任何外域仍为门禁违规。例外仅在线 http(s) 生效，`file://` 下统计桥短路、页面渲染零依赖统计。
6. **新页落地**：可视化页进 site/data/、索引进 site/ 根 + tag-cloud + sitemap；禁往 site/chapters|characters|themes（空遗留目录）。
7. **先取证再假设**：诊断前端显示问题，先拿截图 + Console + 复现条件，再下根因结论（见 docs/10-方法论沉淀/前端显示问题诊断SOP.md）。
8. **禁止擅改**：CHANGELOG 历史段、归档 3 份、.env、SECURITY-AUDIT 档、verify_delivery.py、bump_version.py 等门禁脚本（详见文档规范 §11.2）。
9. **禁重跑 w286_merge_yuanwen_shendu.py**（A1 深度解读 SD 编号会再次错位）。
10. **批量重写脚本改完**：`git diff --name-only` 对比改动范围，非必要改动 `git restore` 回退。
11. **双协议**：代码 MIT + 文本 CC BY-NC 4.0（非商用），拆分 LICENSE / LICENSE-CONTENT.md。
12. **动效契约（W463 固化）**：新增/修改可视化页动效必须遵守 DESIGN.md §5——时长 ≤600ms（白名单仅 hero 600 / count-up 900）、reduced-motion JS 守卫（D3 transition 不受 CSS media 控制，须 `MOYUN_RM` 调用点级或 prototype 级短路）、tooltip 统一 `.chart-tooltip` + `.classed('visible')`；批量改动后重跑 generate_csp.py + duration≤600 扫描。
13. **内容可信度轨（W505-W508 固化）**：docs/01-06 新内容必须走元信息块 v2（第 18 门禁）+ 术语一致性（第 19 门禁）+ 引文硬验证（第 20 门禁）；引文须经 `_cite_probe.py` 提取候选（§4.3），管线产出须过 `_check_pipeline_consistency.py`；归档/删除脚本须同步查 tests/ 引用（W506 教训，见 day-review skill 步骤 4-6）。
14. **修实例必修根（W998 固化）**：修复暴露同类风险时，同批或次批根治，禁止「值得排期/等点号」收尾（真需用户决策的仅限外发动作）；检查任务按委托字面范围执行；跨会话教训权威落坑表与本节，私有记忆仅作镜像（W516 载体铁则·治理季三次用户问责实证）。
15. **禁止补丁加补丁，修复必须从根因（W1039 用户令）**：一个修法若只是「让当前报错消失」，而没消除产生它的结构性原因，就是补丁。四种典型形态——① **为迎合脆弱判据补数据/补标记**（而不是修判据本身）；② 在调用处加特例分支绕过；③ 用豁免/白名单把红灯压下去；④ 修完症状不追问「**为什么会被触发**」。正确顺序：先问「判据/机制为什么会被触发」→ **修判据或机制** → 再改数据；并把教训变成**机器判据**（硬守卫/断言/自测），使下批不可能再犯，而不是写进文档等人记住。**实证（W1019）**：为压体积剥离 CSS 注释后，门禁的「跳过 INLINED 副本」判据靠块内注释串识别而失效；第一版往副本里塞回人工识别行去迎合判据＝补丁；根因修法是把判据改为按 `<!-- INLINED CSS -->` 标记配对识别，两个消费者共用，并补 3 例回归锁。
16. **协作与环境约束（W1039 用户令六则 + I-01 增补⑦·违反即返工）**：① **不主动创建 automation**（定时任务/提醒）——用户 2026-10-13 令取消全部；需周期性事务时写进待办清单由其口令触发，或由用户自行在界面建；「开始优化/都做」**不等于**批准 automation，须单独一句明确同意。② **GPU 重负载须先获批并分批**——用户笔记本在持续 GPU 满载（嵌入/训练量级）下会保护性关机（Kernel-Power 41 实证 2 次，插电 99% 时仍断电）；重计算前先征得同意，小批 + 冷却间隔，禁连续挂满。③ **禁用 `~/.minimax/` 任何内容**（auth / 权限 / 渠道绑定 / config 属个人数据）——需判断某工具是否安装时，用项目面证据（import 测试 / 仓内文件 / 会话内工具清单）替代对 profile 目录的枚举。④ **给用户复制粘贴的命令与路径必须完整**，禁 `...` 缩写——用户会原样照抄（W1025 实证：钩子里的 python 路径被吃掉，导致提交被阻止）；多行命令给整块代码块，并标注「整行替换」还是「插入到第 N 行之后」。⑤ **涉及「选哪个 / 怎么做」的答复必须显式给推荐**——先给明确推荐与一句话理由，再给备选与代价；不以「看你定」结尾，也不只罗列选项让用户自己判断。⑥ **有复用价值的教训，项目内必须留载体**——只写进 AI 记忆＝未落地；判定：另一个会话、另一个 Agent、另一个接手者能否在项目内检索到它。⑦ **豁免/白名单/基线新增条目必须用户批准**（W1053 I-01·W1046 方案）——豁免只增不减为默认，纠正误判类可做但须 CHANGELOG 决策记录留痕；存量对账走 stats.json 两键与触发器 T4。
17. **开批先预约号（W1041 立·reserve_w.py）**：并行会话共享同一工作树时，台账是「事后登记」——两会话各自从自己看到的台账 max 取号必撞（2026-10-30 实战撞 W1039，后由并行会话续占 W1040、本批顺延 W1041）。开批第一步必须跑 `python scripts/reserve_w.py` 占号，stdout 即本批 W 号；**未占号不动手**。candidate = max(台账 max W, CHANGELOG 顶段 W, 已预约集合) + 1，写入 `tmpe/_w_reservations.json`（24h TTL 防占而不交，收官后 `release <W号>` 释放）。注意：仅同一工作树内有效；不同 clone 不共享该文件，仍靠 git log + 台账兜底。
18. **提交前三问自检（W1056 立·用户令）**：每笔提交（含回填/扫尾小笔）前必须自答三问并把结论落到收官材料（CHANGELOG 验证栏或台账备注），不通过不得提交——钩子在门禁绿后强制弹出：① 本批过程中遇到的问题是否全部在本批内解决或登记去向（无「顺手跳过」）；② 同类问题是否会再次犯错——防复发机器判据/坑表条目是否已落地（无判据的教训＝未解决）；③ 本项目是多 Agent 协作，其他 Agent 能否从项目内文件（AGENTS/CHANGELOG/pitfalls/台账）了解本批全部决策与遗留——**凡写入私有记忆文件的教训必须同步落仓**（16-⑥ 载体铁则的提交时机强化）。
19. **禁用 CodeBuddy/WorkBuddy（W1061 入必载层·用户 2026-10-07 两度重申·此前仅存私有记忆=三问 ③ 违规实例）**：项目一切 AI 功能不使用 CodeBuddy/WorkBuddy 及其任何残留；agent-web 的三选一裁决=保留但换引擎（OpenAI-compatible 自研·W680 收官/W681 事实收官）。任何会话不得引入、恢复或仿建该品牌工具链。

20. **Python 改动结构检查（W1077 立·用户令）**：改动 .py 后必须跑 `pwsh -File scripts/guardrails/check_changed.ps1`（ruff 风格档/结构档/嵌套推导式，退出码 0 才过；`api_diff.py` 报破坏性变化须在提交说明写明）；阈值与收紧路线见 docs/agent-guardrails/README.md；新增阈值/豁免须按 16-⑦ 报批。
21. **CI 推送节奏（当日一 PR 一 push·W1129 修订·取代 W1118「一批一 PR」口径）**：① **回填与订正类改动永不单独开 PR** —— 台账行 hash/status 回填、CHANGELOG 数字订正、复盘补记、口径修正等，一律并入**下一次在途批**的 PR；② **同一会话当日多个批次合并进同一个 PR**（批次号仍各自登记：占号 / 台账认领行 / CHANGELOG 段 / 报告 / 编号），当日该会话只开一个 PR；③ 跨会话仍各自开 PR（不牺牲并行度），但第①条对所有会话生效；④ 收官链产物仍必须在**提交前**全部生成完毕，一次 git add + 一次 commit + 一次 push；禁「先提交再补产物」的追加提交 —— 实测 W1116 一批推四笔 ⇒ 约当全部 run 的一半，且连推多笔会放大 checkout 挂起导致的 runner 死锁。**依据**：用户 2026-11-04 裁定（实测两日 PR 数与其中纯回填/订正类占比见 T78 报告 §3.2）⇒ **PR 数与 CI 轮数成正比、PR 数是 job 数的乘数**（触发面治理与 PR 节奏治理是同一问题的两面）。**配套**：多批同 PR 时第 51 槽的归属须支持多批（新增段集合 > 1 ⇒ 取各批 spec 并集）⇒ 已在本批实现。判据：提交前 git status 不得残留未暂存的生成产物。
22. **治理文档体积上限与批量归档（W1119）**：CHANGELOG.md 与 file-index.md 正本各 **<= 262144 字节（256KiB）**；台账正本 **<= 60 数据行** 且 **<= 262144 字节**（先到者为准）。**仅当超阈值才搬**（未超阈值零动作）；每次搬**最老 50 段**（W 段号优先序）、循环到达标（最后一批可不足 50）；**两面必须迁到同一 W 号下界**（迁完断言两面正本剩余最小 W 号相同）；正文至少保留最近二十个批次段。超窗处置优先序（W1142 定形）：① **段行压缩**——巨批登记面按目录分组立式（单一原语 `batch_spec.fi_group_rows`·阈值 200 行·单段超限由体积窗门禁密度判据拦·spec 恒全量为应动全集权威不受体积窗管）；② **归档搬段**——最老 50 段、两面同下界、迁后正本剩余段 <20 即禁止搬段（须先压缩·W1139 曾 29 段被迁剩 1 段实证）；③ 仍超限方考虑拆批。能用压缩解决的不搬段。工具 = scripts/archive_segments.py（--max-bytes / --chunk / --keep 兼容旧路径）；收官链已内置腾窗步（**置于 precheck 之前**：precheck 是 fail-closed 中止，腾窗排其后即死路径·W1117 实证）。
23. **异常分类必须与失败语义对齐（W1121 立·E-161）**：新增的「检查/保护」逻辑若被宽 `except Exception` 包住并 `return True`，则缺陷路径与正常路径**同样成功**⇒ 零红灯且可持续数周（实测：腾窗步漏 `import io` ⇒ NameError 被吞 ⇒ 台账行窗口判定**从未真正触发**）⇒ 依赖缺失走 ImportError、文件不可读走 OSError，**代码缺陷类（NameError/TypeError/AttributeError）直接抛出**，宁可整链中止；且每条新增保护逻辑必须配一条「它真的生效」的正向证据（单测/自检）。

24. **并行会话必须工作树隔离（W1124 立·三方共用工作树实证）**：本仓的级联/收官链会**整面重写** HANDOVER / CHANGELOG / AGENTS / SKILL / 坑表 / 台账 ⇒ 多个会话**共用同一工作树**时，一方跑链即覆盖另两方未提交改动；计数类面会按「含他方条目的中间态」算出漂移值（本次实测：坑表流程节标题被算成 138 而真值为 135）；一方整文件 `git add` 即**代提**他方改动 ⇒ 违反禁代提纪律。**纪律**：并行会话各自 `git worktree add <独立路径> -b <独立分支> <基线>`（或独立克隆）⇒ worktree 共享 `.git` 故**分支名不可重名**；迁出后必须**精确回滚**自己在共享树里的残留（按自己条目的唯一前缀匹配，禁整文件覆盖以免反吃他方并发改动）；迁出与回滚须**书面告知其余会话**并给出「正确计数基线」，避免他方按中间态校准。（W1157 去重：原第 25 条与本条完全同文双写，系 W1124 入载事故——删重复尾条不改号。）

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

*本文件由 AGENTS 通读项目后生成于 2026-08-16（v2.3.73 W458）；W458-W707 沿革已迁 [archive/docs/AGENTS-ARCHIVE.md](archive/docs/AGENTS-ARCHIVE.md)（W709 BL-23 建·W713 续迁 W701-W707·W719 续迁 W708-W714·W1194-W1194 级联自动滚动·脚注保留最近 5 条·每条 ≤120 字（W989 收紧）·日期一律阿拉伯形态（W964 定形契约·中文数字形态曾致滚动器失明）·grep 查勿通读）；2026-11-09（W1195）Scorecard Pinned-Dependencies 真修：pip 哈希化清单 + npm ci 化；2026-11-10（W1196）外部规则覆盖面审计：守卫扫描面宽于规则面 + 盲区监控守卫；2026-11-10（W1197）守卫扫描面扩到全仓 shell：两守卫扩面 + 接入 CI 阻断；2026-11-10（W1198）Dependabot 41 条 Pillow 告警归零：删除后重建依赖清单触发依赖图重算；2026-11-10（W1199）提交前一次性就绪链落仓：E-220 入坑表 + 规则正文入 AGENTS + 计数链同步 + W1198 终态读数回填。如与上述权威文档冲突，以权威文档为准。*
