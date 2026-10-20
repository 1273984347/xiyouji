# AGENTS.md — 《详解西游记》项目 Agent 指南

> **📖 阅读契约（W707）**：索引型——不要线性通读。先跑 `python scripts/agent_start.py --task` 拿「本次任务相关」清单按需读节；§4.2 全 46 条门禁与 §4.3 全部坑位属按需查表（L2 已拆分落地：docs/agent/gates.md · pitfalls.md · agent-web.md·W709）；§1-§3/§6 铁律/§7 必读。
>
> 本文件面向进入本仓库工作的 AI Agent（及新接手的人类维护者），提供项目的用途、技术栈、目录结构、关键模块、依赖关系、构建运行方式与必须遵守的铁律。动手前请通读；更细的规则以文末「权威文档」为准。
>
> **维护契约（防乱写）**：本文档是 Agent 协作指南，只允许结构性编辑——① 保持 §1–§8 骨架不变；② 新增铁律/规则必须**就地并入对应章节**并全篇去重（禁止追加「速记 / 补充」尾部段落）；③ 版本脚注更新须与当前 HEAD（vX.Y.Z W###，用 `git rev-parse --short HEAD` 核对）一致；④ 与 HANDOVER / 文档规范 / CHANGELOG 冲突时以后三者为准。

---

## 1. 项目用途与定位

**《详解西游记》**（xiyouji）是一个「一源多形 · 数字人文可视化解读《西游记》100 回」的项目。它把《西游记》的文本研究组织为四层产物：

- **文档（Docs）**：Markdown 写就的逐回解读、人物分析、主题专题、文化背景、诗词赏析、个人随笔。
- **站点（Site）**：可浏览的纯静态 HTML 站点，`file://` 双击即可打开，部署于 GitHub Pages（https://1273984347.github.io/xiyouji/ ）。
- **数据可视化**：87<!--stats:visualization_pages--> 个 D3.js / Three.js 可视化页（site/data/ 共 88<!--stats:site_data_html--> 个 HTML，「87」不含模板壳 _shell.html），覆盖 133 个数据维度（章节统计、人物关系网络、八十一难热力图、取经路线、情感热力图、AI 对话等 34<!--stats:script_classes--> 类主题 A–AH）。
- **可问询入口**：Web Agent「西游记·渡口问津」（xiyouji-agent-web/）——自研 OpenAI-compatible 引擎（server/engine/·W680·全主流大模型端点适配），可对话、检索 docs/source、跑脚本。

**核心内容规模**：A1–A6 内容板块共 615<!--stats:a1_a6_docs--> 篇（A1 逐回 100 / A2 随笔 44 / A3 人物 215 / A4 主题 209 / A5 文化 34 / A6 诗词 13；算法与边界见 docs/00-导读/统计口径说明.md；W505 起 611→615）；英文站 site/en/ 138<!--stats:site_en_html--> 页已全量英文化。

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
│   ├── 06-个人随笔/       # A2 随笔（44 篇）
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
│   ├── data/              # 可视化页（88 个 HTML，D3/Three；「87 可视化页」口径不含模板壳 _shell.html）
│   ├── en/                # 英文站（138 页）
│   ├── static/js|css|fonts/  # 本地化 D3/Three、tokens.css/system.css、子集化字体
│   └── sitemap.xml
├── scripts/               # Python/JS 工具链（门禁、生成器、审计、诊断）
│   ├── verify_delivery.py # 交付门禁（pre-commit 强制，见 §5）
│   ├── generate_csp.py / inline_css.py / bump_version.py / lint_links.py
│   ├── check_*.py|js      # 各专项门禁
│   ├── run_all.py         # 批量运行 A-AH 34<!--stats:script_classes--> 类分析
│   ├── _*.py|js           # 一次性/诊断脚本（不入库门禁、不参与 CI）
│   └── output/            # data/*.json（可视化数据源）+ file-index.md + screenshots/
├── dataset/               # 结构化 JSON（可视化/API 数据源）
├── xiyouji-agent-web/     # Web Agent「西游记·渡口问津」（React+Vite+Express）
├── mcp-server/            # MCP 工具（xiyouji_mcp.py：drl_spotcheck 等）
├── tests/                 # pytest + Playwright E2E
├── assets/                # 字体源、图片
├── references/  timeline/  tools/  hyperframes/
├── README.md / STRUCTURE.md / CHANGELOG.md / DESIGN.md / HANDOVER.md / 新Agent启动Prompt.md / CLAUDE.md（AI 速查层·W664）
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

> **📖 阅读契约（W709）**：索引型——本节=46 槽摘要；完整定义（口径/豁免/历史实证）→ [docs/agent/gates.md](docs/agent/gates.md)；失败排查时按编号查 gates.md。

verify_delivery.py 是提交前唯一硬门禁入口（`.git/hooks/pre-commit` → 本脚本·W698 起本地传 `--scope auto` 分级，CI 与批收尾恒全量，核心 FAIL 返回非 0 阻断）。内含 45 槽，五组：

**内容与同步类（1-5）**：
1. **六文档同步**
2. **范围漂移检测**
3. **A4 计数一致（EXPECT_A4 字面量「209 篇」）**
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
16. **Skills 索引一致性**
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

**编号与质量防线类（27-45）**：
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

**完整定义 → [docs/agent/gates.md](docs/agent/gates.md)**（原文全量·五组分节·内容零改动）。

### 4.3 工具链要点（摘要层 · 坑位全量已迁 L2）

> **📖 阅读契约（W709）**：索引型——41 条坑位按六主题迁 [docs/agent/pitfalls.md](docs/agent/pitfalls.md)（含 shell 场景查坑表）；本节保留主题视图与高频铁则。

**主题视图（W706·按需查坑·正文按批次序不动）**：CSS 类=W557 基类丢失/W558 缺分号/W673 三门禁/W571 inline_css 分发/W582-W589 暗色族；JS 类=W575 空选区与触屏坑/W568 Express close 语义/W674 defer 时序/W656 audit 单模块；git 提交类=W649 级联清单与并行互斥/W698 scope+safe_commit/W537 三新规/W514 heredoc/W509 BOM 禁；级联类=W553 CRLF 翻倍/W664 desc 分隔符/W663 跳号手工先例/W679 日期串误报/W705 插入保留锚点；数据类=W691 计数钉与旧值扫描/W693 残留标记门禁/W565 部署态冒烟/W703-704 stats 对账；文档类=W520 字面量禁/W496 数字现测/W663 doc-sync/W706 元规则与标识符禁令；Windows 类=W509 BOM/W514 heredoc/W535 路径实参/W706 终端编码兜底。

**最高频铁则（全文见 pitfalls.md）**：改内联脚本必跑 generate_csp.py；批量改 CSS/JS 验括号平衡；多行逻辑禁 shell heredoc 落 Python 文件；同文件 Edit 串行；级联后按清单 git add；认领批次登记 touches·动工前 `preflight_check.py --touches <清单> --self W###` 查在途交集（跨 Agent 版「同文件串行」）。

**六主题目录 → [docs/agent/pitfalls.md](docs/agent/pitfalls.md)**：CSS/视觉渲染（9）· JS/CSP/运行时（5）· git/提交/并发（12）· 级联/CHANGELOG（4）· 数据/内容可信度（4）· 流程/协作/取证（7）。计数口径 = 各节顶层「- **」条目数（W757 校：流程节新增 2 条「门禁建置即红检测法·接线断言锚 run 块」由 4 升至 6；W778 增「latent 三问 + 双平台断言禁例」升至 7，总 40→41）。

**本机环境事实（Windows 单机·2026-10-17 实测·机器相关不入 L2）**：
- `make` 未安装：Makefile 目标不可用，直调 `python scripts/<对应脚本>`（映射见 Makefile 注释）。
- 全局 Python 3.12·无项目 `.venv`：`pytest`/`playwright`/`pip_audit` 约定加 `-m` 前缀调用，**三语境分清**——① **仓内文档 / 工具表 / CI / Makefile 一律写可移植形态 `python -m <工具>`**（CI 跑在 `ubuntu-latest`·`py` 在 Linux/macOS 不存在·Makefile 亦注明「Windows 兼容：使用 python（非 python3）」）；② **本机 PowerShell 侧**用 `py -3 -m <工具>`——该侧 `python`/`python3` 指向 `WindowsApps/python.exe` 应用执行存根（**命令存在但调用即 exit 9009·无输出无报错**）；③ **本机 git-bash 侧** `python`/`python3` 均为实解释器（`C:\Users\12739\bin\`）·可直接写 `python`。**2026-10-20 实测（本机两 shell 解析不同·写文档时勿凭直觉）**：`py -3` 两 shell 一致指向全局 Python 3.12（`AppData\Local\Programs\Python\Python312`）且能吃 git-bash 的 POSIX 路径——故**本机 PowerShell 侧统一用 `py -3`**，但**不得把它写成全仓约定**（`py` 非跨平台·会令文档在 CI/Linux 上失效）。`ruff`/`uv`/`node`/`npm`/`git`/`gh`/`pwsh` 可直呼。
- `pwsh`（PowerShell 7）与 `powershell`（5.1）并存：需 PowerShell 时一律用 `pwsh`（默认 UTF-8 无 BOM）；`powershell` 是 5.1（GBK 默认·W509 BOM 坑源），且仍遵守仓内「禁 PowerShell 写仓内文件」铁则。
- 提交门禁 hook（.git/hooks/pre-commit）与本清单同口径取解释器：首选 `py -3`，回退系统 Python 3.12 绝对路径，两者均须实测可运行（`-c "import sys"` 返回 0）才选用；**不按 PATH 上的 `python`/`python3` 形状挑选**（两 shell 解析不同·见上一条）·不依赖任何厂商托管运行时路径。
- pre-commit 框架未装且**禁装**：`pre-commit install` 会覆盖手写 `.git/hooks/pre-commit`，破坏零依赖门禁。

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
5. **file:// 铁律**：新页面必须内嵌 EMBEDDED 回退、零外域依赖（D3/Three 本地引用 `site/static/js/`，禁 d3js.org/cdnjs 外域 CDN）。
6. **新页落地**：可视化页进 site/data/、索引进 site/ 根 + tag-cloud + sitemap；禁往 site/chapters|characters|themes（空遗留目录）。
7. **先取证再假设**：诊断前端显示问题，先拿截图 + Console + 复现条件，再下根因结论（见 docs/10-方法论沉淀/前端显示问题诊断SOP.md）。
8. **禁止擅改**：CHANGELOG 历史段、归档 3 份、.env、SECURITY-AUDIT 档、verify_delivery.py、bump_version.py 等门禁脚本（详见文档规范 §11.2）。
9. **禁重跑 w286_merge_yuanwen_shendu.py**（A1 深度解读 SD 编号会再次错位）。
10. **批量重写脚本改完**：`git diff --name-only` 对比改动范围，非必要改动 `git restore` 回退。
11. **双协议**：代码 MIT + 文本 CC BY-NC 4.0（非商用），拆分 LICENSE / LICENSE-CONTENT.md。
12. **动效契约（W463 固化）**：新增/修改可视化页动效必须遵守 DESIGN.md §5——时长 ≤600ms（白名单仅 hero 600 / count-up 900）、reduced-motion JS 守卫（D3 transition 不受 CSS media 控制，须 `MOYUN_RM` 调用点级或 prototype 级短路）、tooltip 统一 `.chart-tooltip` + `.classed('visible')`；批量改动后重跑 generate_csp.py + duration≤600 扫描。
13. **内容可信度轨（W505-W508 固化）**：docs/01-06 新内容必须走元信息块 v2（第 18 门禁）+ 术语一致性（第 19 门禁）+ 引文硬验证（第 20 门禁）；引文须经 `_cite_probe.py` 提取候选（§4.3），管线产出须过 `_check_pipeline_consistency.py`；归档/删除脚本须同步查 tests/ 引用（W506 教训，见 day-review skill 步骤 4-6）。

---

## 7. 快速上手路径（新 Agent 接手）

0. 开局先跑 `python scripts/agent_start.py`——实读磁盘输出当前事实摘要（现役三元组/近 3 批次/stats 全键/对账表现势/阻塞·W705）——防「记忆代读」，值全部来自磁盘实时读取。
1. 读 `CLAUDE.md`（AI 速查层，1 分钟）→ 必守规则与常用命令速览（W664 起，宿主自动加载）。
2. 读 `HANDOVER.md`「零、当前阻塞」+「一、当前进度」→ 当前 HEAD（vX.Y.Z W###）、下一 W 编号、遗留待办。
3. 读 `README.md` → 项目全貌、内容规模、在线站点、双协议。
4. 读 `docs/00-导读/文档规范.md` §11 → 文件管控清单（必同步/禁擅改/接手速查 6 步/同步核对 10 项）。
5. 读 `HANDOVER.md`「三、方法论沉淀」→ 经验**总入口**（W755 起指针化：现役坑位/门禁读 [docs/agent/pitfalls.md](docs/agent/pitfalls.md) 与 [docs/agent/gates.md](docs/agent/gates.md)，深度篇读 [docs/10-方法论沉淀/](docs/10-方法论沉淀/README.md)）。
6. 深挖结构看 `STRUCTURE.md`、`scripts/output/file-index.md`（反向索引）、`CHANGELOG.md`（正向时间线）。
7. 动手前跑 `python scripts/verify_delivery.py` 确认基线全绿。

---

## 8. 权威文档（冲突时以此为准）

> **清单间裁定链（W706）**：文档规范 §11（文件管控）> CHANGELOG 现役段 > HANDOVER。本节与 CLAUDE.md（速查指针）、CONTRIBUTING（贡献者协作面）系三视角清单，内容不一致时按裁定链与本节为准。

- 进度中枢 / 规则：`HANDOVER.md`、`新Agent启动Prompt.md`（速用精简版）、`CLAUDE.md`（AI 速查层·W664）
- 文档规范：`docs/00-导读/文档规范.md`（尤其 §11 文件管控）
- 设计规范：`DESIGN.md`（§1-4 视觉 / **§5 动效契约**）
- 目录结构：`STRUCTURE.md`
- 变更日志：`CHANGELOG.md`（正向）+ `scripts/output/file-index.md`（反向）
- 诊断 SOP：`docs/10-方法论沉淀/前端显示问题诊断SOP.md`

---

*本文件由 AGENTS 通读项目后生成于 2026-08-16（v2.3.73 W458）；W458-W707 沿革已迁 [archive/docs/AGENTS-ARCHIVE.md](archive/docs/AGENTS-ARCHIVE.md)（W709 BL-23 建·W713 续迁 W701-W707·W719 续迁 W708-W714·W802-W802 级联自动滚动·脚注保留最近 5 条·grep 查勿通读）；2026-10-19（W803）工具链行为保持重构批：用户令在功能与输入输出与外部接口完全不变前提下提升可读性与可维护性——动工前先做重复形态普查（三百七十八个 Python 文件 AST 扫描同名函数体与 helper 名频次与惯用法），按取证定面；新建 scripts/utils/gate_common.py 收敛门禁族公共骨架（路径常量与容错及严格两种读取与站点三源清单与样式块提取与自测跑批与命令行分发共十二个公共符号），七个门禁脚本改为消费该模块且判定内核函数名与签名及标准输出逐字节不变；清理 check_claude_md 行数计算死代码（七边界样本加真实文件实算证明等值）；拆分 lint_links 的 _process_file 六十九行与收敛两处路径解析口径，提升循环内 import 为模块级；拆分 mcp-server 四个 MCP 工具（长函数由五降为一、最长由一百零二行降为六十六行）并把两处函数内大字典提为模块级常量与五处重复注解字典收敛为一；Web Agent 服务端按职责分文件（index.ts 由七百一十行降为五十一行、ToolCallsCollapse 由七百六十七行降为一百六十六行，新增 src/utils 三模块与 toolCalls 五模块）；对拍取证以 git worktree 重建 HEAD 旧态同源比较，八脚本乘两模式共十六组标准输出逐字节一致（其中 lint_links 全仓文档口径一组首轮报差异经查为 worktree 内未跟踪文件触发 gitignore 排除的取证环境伪差，同仓两跑 sha256 相同），MCP 三十组输入覆盖全分支返回字典一致；验证等于 ruff 零 加 pytest 单元面四百二十七 passed 三 skipped 加 verify 全量五十段零 FAIL 加 npm build 成功 加 test:server 六十七 passed 零 fail；另查明 tests/unit/test_visualization_data.py 在全量套件末尾挂起为改动前既有现象（HEAD worktree 复现同点），非本批引入；2026-10-19（W804）桌面版三平台安装包与自动更新批：用户令给项目在 GitHub 仓库增加可直接下载的安装包并支持自动更新——方案裁定离线全站桌面版，新建 xiyouji-desktop 桌面工程（Electron 四十四主进程加本地静态服务仅监听 127.0.0.1 随机端口并做路径穿越防护且仅接受 GET 与 HEAD 加中文菜单与原生更新对话框加单实例锁与崩溃文件日志加无窗口 self-test 冒烟）；自动更新基于 electron-updater 六点八（发布源指向本仓库 Releases），启动三秒后首次检查且此后每四小时复查并支持菜单手动检查，发现新版本询问下载、下载进度回显、下载完成询问重启安装（选择稍后则退出时安装），开发态与禁用环境变量下安全降级；发布流水线新建 .github/workflows/release.yml（tag v 星号或 workflow_dispatch 触发，版本一致性闸门校验 tag 与桌面工程 package.json 严格相等并从 CHANGELOG 首段动态提取内容批次，三平台并行构建 Windows NSIS 与 macOS universal dmg 加 zip 与 Linux AppImage，汇总上传 GitHub Release 含 latest 系列 yml 与 blockmap 自动更新元数据并生成中文 release notes，Release 已存在时 clobber 幂等更新）；ci.yml 末尾新增 desktop-build job 做 npm ci 加 node --test 加内容准备加 electron-builder --dir 打包回归；根 README 新增桌面版下载段（三平台固定直链）且 STRUCTURE 顶层目录与 README 目录树登记 xiyouji-desktop；验证等于 npm install 成功加 npm test 三十三项通过加 self-test 输出 SELF_TEST_OK（开发态与打包产物双跑）加 Windows 安装包 130705240 字节且 latest.yml 的 sha512 与安装包实算一致并对拍 app-update.yml 发布源正确加 pytest 七百一十四 passed 三 skipped（可视化数据测试文件末尾挂起为改动前既有现象，本批排除该文件实跑）加 ruff 零加 actionlint 零错误加 verify 全量五十段零 FAIL；2026-10-19（W805）跨平台测试守卫热修批：W804 推送后 dev 到 main 的 PR CI 首跑在 Linux 暴露 W803 引入的测试缺陷——tests/test_xiyouji_mcp_extra.py 的目录目标守卫断言 pytest.raises(PermissionError) 绑定 Windows 专属异常子类，而 Linux 与 macOS 读目录抛 IsADirectoryError（同属 OSError），导致单元测试任务一失败七百二十九通过；修复仅动测试面（断言改为跨平台 OSError、测试更名为 test_directory_as_target_file_raises_os_error、docstring 明写 Windows PermissionError 与 Linux IsADirectoryError 同属 OSError 且守卫点等于目录当文件会抛异常不绑定平台子类），被测 xiyouji_drl_spotcheck 生产代码零改动行为不变；验证等于目标测试六十七 passed 加全量排除既有挂起文件七百一十四 passed 三 skipped 加 ruff 零加 verify 全量五十段零 FAIL 加以推送后 PR CI 复跑转绿为准；2026-10-20（W806）GoatCounter 统计链彻底退役批：站点代码 1273984347 失效，fetch_gate_stats 实测 HTTP 404 且断链自 2026-09-30 未恢复——页面埋点采不到任何数据，却仍每页加载并产生一次无效外域请求，用户裁决彻底退役；落地为 site 根 8 加 site/data 88 加 site/en 138 共 234 页移除埋点标签且全站 data-goatcounter 残留归零，CSP 生成源去掉计数端点后重算 856 页 meta（其中 546 页原含该域放行）并同步 site/_headers，搜索两页摘除活的 window.goatcounter.count 分支，删除注入器 scripts/inject_goatcounter.py 与自托管 count.js，rum.js 删除改道分支与随之失效的 bucket 死函数并改为本地 dev 回流、显式配置外发、纯静态托管零外发三条通道，新建防回退守卫 scripts/check_no_goatcounter.py（四项判据加自测 1 正 4 负加单测 5 项并接入 ci.yml），访问统计方案改写为现状与退役记录并同步四处文档口径；验证等于守卫实跑 0 FAIL 加自测 SELF_TEST_OK 加单测 5 passed 加 CSP 零漂移加 pytest 七百一十九 passed 三 skipped（退出时挂起为 HEAD worktree 对拍复现的既有现象非本批引入）加 verify 全量五十段零 FAIL；2026-10-20（W807）站内搜索索引刷新批：W806 退役 GoatCounter 时顺带盘点站内搜索，发现索引自二〇二六年九月十六日前后停更——全站七百七十一条索引仅含六十一篇文档条目，且九条链接仍指向已改名的文档十一报告复盘目录导致 GitHub 侧四〇四，且全链无任何门禁覆盖；本批把生成器恢复到 W573 原位（归档副本因目录加深两层致根路径解析错位不可直接运行·归档件按禁改归档纪律保持原样），实跑刷新得到文档七百二十六篇与两个索引常量二十五万六千与二十七万六千字节（均在五十万字节预算内），文档条目由六十一增至一百一十一（五十篇文档首次可检索），失效目录引用由九条归零改指文档十一方案报告，内联常量变更后重算该两页内容安全策略哈希且八百五十六页零漂移；新增常驻防线两条——端到端套件补搜索页离线检索有结果且无脚本错误、以及刷新后新增文档协议边界速查标题单元格精确命中，同款断言在旧索引上返回一行（弱关键词命中但标题单元格无全等命中）必红故具真实区分力；登记余项为索引新鲜度门禁未挂载（需新增交付校验门禁段而该脚本属管控文件·改动须经用户批准）；验证等于生成器二跑散列一致加内容安全策略零漂移加端到端全过加全量测试加交付校验五十段零 FAIL；二〇二六年十月二十日（W808）Web Agent 全栈加固批：用户令全栈一遍并测试三件套全上；审计仓库内唯一全栈应用（渡口问津 Web Agent）发现三处真实跨边界缺陷——反馈提交漏传会话标识致服务端恒返四百且前端静默吞掉故用户赞踩从未被记录、接口客户端不判响应成功标志致服务端错误体被当成功数据返回故错误被静默吞掉且流式路径的未授权响应被当流解析致思考中永久挂起、前端从不携带共享令牌故服务端一旦启用鉴权即全站未授权且无人察觉；本批建类型化错误层级与全局错误处理（运营错结构化返回编程错只记日志返通用五百且不泄堆栈）、结构化 JSON 日志含凭证脱敏、请求标识全链路传播与畸形净化、Zod 边界校验覆盖全部接口入参、信号触发的优雅关闭含排空在途请求与预写日志检查点与关库、新增就绪探针于依赖不可用时返五零三；前端建统一客户端（判状态码、注令牌、可配基址）、前后端共享类型契约、状态码到用户可读文案的映射与会话与模型两个钩子的失败态可见与横幅重试；另修两处配置链缺陷——点env依赖声明却从未被引入致文档化的配置文件流程实际从未生效、编译产物吐在项目根而打包器优先读编译副本致改配置文件静默失效（产物改出源目录并清理四十个陈旧产物）；测试建三层——单元四十例（三个缺陷各有负样本）、集成十四例（真实起服真实请求真实落库断言、信号位为类 Unix 专属且真实执行位为持续集成）、端到端十断言（真实浏览器真实构建产物真实后端真实数据库走完输入发送流式渲染落库反馈全流程，外部大模型端点以替身接入而被测系统全部真实实现）；验证等于三层测试全绿、既有服务端六十七例全过含限流与鉴权负样本以证契约未改、构建成功与交付校验五十段零失败；二〇二六年十月二十日（W809）站内搜索索引新鲜度门禁挂载批：W807 刷新站内搜索索引后遗留登记余项——刷新动作本身无机器防线，内容批次改文档或站点页面后忘重跑生成器，索引即静默陈旧，用户搜不到新文档且旧链接点不开；本批先把生成器从「算与写同在模块级·导入即落盘」拆为纯计算函数与写盘主函数（门禁只读不写·刷新动作不变），再建第四十六槽门禁（两页索引块存在、零语内嵌载荷逐条对拍生成器实算、缺分词依赖即不可判定判红禁静默跳过），并完成门禁元组与段名表、文档槽位归属两侧、门禁清单文档第四十六条、智能体指南摘要层四十五到四十六槽的三方编号对账接线（编号三方对账门禁即该面的机器防线）；验证等于门禁自测五例全过加单测五例通过加现网实跑零失败（零语八百二十二条与英语八百六十四条与实算一致）加编号对账门禁零失败加全量测试加交付校验全量五十一段零失败；二〇二六年十月二十日（W810）站内搜索死代码清理批：W807 刷新站内搜索索引时遗留的清理候选——旧 window 空格 SEARCH 空格 INDEX 赋值数组在换成新常量后成为零引用死重，每页各背两千余字节余量；本批先做零引用三项核查（页面脚本只读新常量、旧数组未被校验脚本读取、生成器同名匹配仅为缺标记时的兜底注入锚点而两页标记齐全故不可达），确认后两页各删一行并重算该两页内联脚本哈希，恰好两页更新而其余八百五十四页零漂移；验证等于内容安全策略零漂移加第四十六槽搜索索引新鲜度门禁零失败加端到端套件与改动前逐字一致加全量测试七百一十九通过三跳过加交付校验全量五十一段零失败；二〇二六年十月二十日（W811）CI 断链修复批：W806 退役 GoatCounter 时在 CI 工作流新增全站零引用防回退守卫，该步骤名误写成未加引号且含冒号空格的裸标量，构成 YAML 映射歧义语法，GitHub 解析工作流时直接判定为工作流文件问题并零秒失败，且拉取请求事件根本不生成检查项，故本批修复为加引号并补可解析性守卫三判据（禁制表符、映射项裸标量禁含冒号空格、有解析器时全量解析），负样本实证可复现并指到具体行号；另声明暴露面：因该工作流此前不可解析，其间批次整段从未被持续集成实跑，本批修复后方为首次实跑；二〇二六年十月二十日（W812）去旧厂商 Agent 工具品牌化批：按用户令清除全仓对某已退役厂商 Agent 工具的一切依赖与署名痕迹，改造分三层——工具环境层把提交门禁钩子的解释器从厂商托管运行时改为遵循仓内工具清单口径的全局 Python 3.12（首选启动器·路径无关·不按各机路径状态挑选）、删除忽略规则并把本地该工具目录备份后迁出项目；脚本层去掉三处脚本与单测中的厂商特例并顺修两个归档扫描脚本因目录加深导致的根路径解析错位；文档层三十七文件一百五十三处按语义分治改写为角色化中性标识以保全多 Agent 身份区分而非塌缩为单一标识，同时保留不在禁令范围的其他品牌原名。派生面同步重生成搜索索引与重算内容安全策略哈希。多 Agent 协作机制、通信机制与通用机制全程保全：共享面按触碰清单登记并经前置核验确认无交集，撞号按先落地者保留主动让号并跨会话书面告知，批次协议照走，下一自由号预留不重复；验证等于 pytest 七百二十六通过三跳过（按仓内既定口径排除既有挂起文件）加交付校验全量五十一段零失败。。如与上述权威文档冲突，以权威文档为准。*
