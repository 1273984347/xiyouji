# AGENTS.md — 《详解西游记》项目 Agent 指南

> **📖 阅读契约（W707）**：索引型——不要线性通读。先跑 `python scripts/agent_start.py --task` 拿「本次任务相关」清单按需读节；§4.2 全 40 条门禁与 §4.3 全部坑位属按需查表（L2 拆分见 docs/superpowers/plans/2026-10-11-agents-layered-restructure.md·BL-24）；§1-§3/§6 铁律/§7 必读。
>
> 本文件面向进入本仓库工作的 AI Agent（及新接手的人类维护者），提供项目的用途、技术栈、目录结构、关键模块、依赖关系、构建运行方式与必须遵守的铁律。动手前请通读；更细的规则以文末「权威文档」为准。
>
> **维护契约（防乱写）**：本文档是 Agent 协作指南，只允许结构性编辑——① 保持 §1–§8 骨架不变；② 新增铁律/规则必须**就地并入对应章节**并全篇去重（禁止追加「速记 / 补充」尾部段落）；③ 版本脚注更新须与当前 HEAD（vX.Y.Z W###，用 `git rev-parse --short HEAD` 核对）一致；④ 与 交接文档 / 文档规范 / CHANGELOG 冲突时以后三者为准。

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
│   ├── 03-主题与情节专题/ # A4 主题专题（209 篇）
│   ├── 04-文化与历史背景/ # A5 文化背景
│   ├── 05-诗词歌赋/       # A6 诗词
│   ├── 06-个人随笔/       # A2 随笔（44 篇）
│   ├── 07-09/             # 学以致用 / 提升认知 / 精神塑造
│   ├── 10-方法论沉淀/     # 复盘、诊断 SOP、DRL 真循环等可复利经验
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
├── README.md / STRUCTURE.md / CHANGELOG.md / DESIGN.md / 交接文档.md / 新Agent启动Prompt.md / CLAUDE.md（AI 速查层·W664）
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

> **📖 阅读契约（W709）**：索引型——本节=40 槽摘要；完整定义（口径/豁免/历史实证）→ [docs/agent/gates.md](docs/agent/gates.md)；失败排查时按编号查 gates.md。

verify_delivery.py 是提交前唯一硬门禁入口（`.git/hooks/pre-commit` → 本脚本·W698 起本地传 `--scope auto` 分级，CI 与批收尾恒全量，核心 FAIL 返回非 0 阻断）。内含 40 槽，五组：

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

**编号与质量防线类（27-41）**：
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

**完整定义 → [docs/agent/gates.md](docs/agent/gates.md)**（原文全量·五组分节·内容零改动）。

### 4.3 工具链要点（摘要层 · 坑位全量已迁 L2）

> **📖 阅读契约（W709）**：索引型——31 条坑位按六主题迁 [docs/agent/pitfalls.md](docs/agent/pitfalls.md)（含 shell 场景查坑表）；本节保留主题视图与高频铁则。

**主题视图（W706·按需查坑·正文按批次序不动）**：CSS 类=W557 基类丢失/W558 缺分号/W673 三门禁/W571 inline_css 分发/W582-W589 暗色族；JS 类=W575 空选区与触屏坑/W568 Express close 语义/W674 defer 时序/W656 audit 单模块；git 提交类=W649 级联清单与并行互斥/W698 scope+safe_commit/W537 三新规/W514 heredoc/W509 BOM 禁；级联类=W553 CRLF 翻倍/W664 desc 分隔符/W663 跳号手工先例/W679 日期串误报/W705 插入保留锚点；数据类=W691 计数钉与旧值扫描/W693 残留标记门禁/W565 部署态冒烟/W703-704 stats 对账；文档类=W520 字面量禁/W496 数字现测/W663 doc-sync/W706 元规则与标识符禁令；Windows 类=W509 BOM/W514 heredoc/W535 路径实参/W706 终端编码兜底。

**最高频铁则（全文见 pitfalls.md）**：改内联脚本必跑 generate_csp.py；批量改 CSS/JS 验括号平衡；多行逻辑禁 shell heredoc 落 Python 文件；同文件 Edit 串行；级联后按清单 git add。

**六主题目录 → [docs/agent/pitfalls.md](docs/agent/pitfalls.md)**：CSS/视觉渲染（9）· JS/CSP/运行时（3）· git/提交/并发（7）· 级联/CHANGELOG（4）· 数据/内容可信度（4）· 流程/协作/取证（4）。

### 4.4 Web Agent（xiyouji-agent-web/ · 摘要层）

> **📖 阅读契约（W709）**：索引型——引擎/前端/权限细节 → [docs/agent/agent-web.md](docs/agent/agent-web.md)。

后端 `server/index.ts`（Express + SSE 流式 + SQLite）+ 自研 OpenAI-compatible 引擎 `server/engine/`（W680·全主流大模型端点适配）；凭证 `LLM_API_BASE`/`LLM_API_KEY`/`LLM_MODEL` 配服务端 .env；核心入口与安全边界（权限四模式/受保护路径/命令白名单）见 L2。
## 5. 构建与运行方式

### 5.1 统一编排（Makefile）

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

1. **六文档同步（W393 降级）**：每完成一个 W 批次，核心 2（CHANGELOG + 交接文档）必须写，辅助 4（README/STRUCTURE/项目说明/file-index）里程碑时跑 bump_version.py 补齐。
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
2. 读 `交接文档.md`「零、当前阻塞」+「一、当前进度」→ 当前 HEAD（vX.Y.Z W###）、下一 W 编号、遗留待办。
3. 读 `README.md` → 项目全貌、内容规模、在线站点、双协议。
4. 读 `docs/00-导读/文档规范.md` §11 → 文件管控清单（必同步/禁擅改/接手速查 6 步/同步核对 10 项）。
5. 读 `交接文档.md`「三、方法论沉淀」→ 可复利经验。
6. 深挖结构看 `STRUCTURE.md`、`scripts/output/file-index.md`（反向索引）、`CHANGELOG.md`（正向时间线）。
7. 动手前跑 `python scripts/verify_delivery.py` 确认基线全绿。

---

## 8. 权威文档（冲突时以此为准）

> **清单间裁定链（W706）**：文档规范 §11（文件管控）> CHANGELOG 现役段 > 交接文档。本节与 CLAUDE.md（速查指针）、CONTRIBUTING（贡献者协作面）系三视角清单，内容不一致时按裁定链与本节为准。

- 进度中枢 / 规则：`交接文档.md`、`新Agent启动Prompt.md`（速用精简版）、`CLAUDE.md`（AI 速查层·W664）
- 文档规范：`docs/00-导读/文档规范.md`（尤其 §11 文件管控）
- 设计规范：`DESIGN.md`（§1-4 视觉 / **§5 动效契约**）
- 目录结构：`STRUCTURE.md`
- 变更日志：`CHANGELOG.md`（正向）+ `scripts/output/file-index.md`（反向）
- 诊断 SOP：`docs/10-方法论沉淀/前端显示问题诊断SOP.md`

---

*本文件由 AGENTS 通读项目后生成于 2026-08-16（v2.3.73 W458）；W458-W700 沿革已迁 [docs/archive/AGENTS-ARCHIVE.md](docs/archive/AGENTS-ARCHIVE.md)（W709 BL-23·grep 查勿通读）；2026-10-11（v2.3.295 W701）BL-20动工与S-26工具化批（用户圈选四项裁决）：BL-20 读屏替代文本/键盘导航落地（chart-a11y.js 模块+注入器 87 页 aria 摘要层+tabable 焦点·探针 87 页全绿·EN 镜像登记余项）加 S-26 worktree_rehearse.py 预演器（首跑即拦双 static 真 bug）加 第四篇复盘正文状态同步与交接 BL-20 闭账 加 级联外提交追记四笔（2bf126ed/a013c8b4/c64d3549/4cec0494）；2026-10-11（v2.3.296 W702）六文档口径清债批（外部挑刺 17 项裁决）：P0 口径四件（CHANGELOG 头部页数口径按实跑刷新 857/856/855/330 加 AGENTS 第 8 门禁 233→856 页 加 README 26→40 项门禁 加 STRUCTURE 方法论沉淀 6→33 篇）加 P1 两件（scripts 30→34 类全建+F 行 story-timeline 补录 加 第 6 门禁三豁免→五豁免对齐 W700）加 P2 三件（v2.3.279/280 补录四件套只增不删 加 第 26 门禁 334→855 页校真 加 CONTRIBUTING 补对账表认领入口）加 P3 排版与速查（batch_cascade 三版本行模板去空格加锚点同步 加 AGENTS 脚注 join 双分号守卫与存量 4 处归一 加 CLAUDE.md 补 --scope auto 加 §4.2 前言 scope 指引）加 顺带实数校真（STRUCTURE JSON 131→135 加 timeline 待建经 git ls-files 维持）加 驳回 1 项（第 27 门禁补静态现役上限字面量——违反 W520 禁漂移字面量纪律）；2026-10-11（v2.3.297 W703）聚合数字对账门禁批（用户方案 A+C 修正形态）：scripts/stats.py 磁盘实算 15 键生成 scripts/output/stats.json（tracked·CI 可复现）加 第 31 门禁扩 C5 聚合数字对账（18 式高危句式×现役叙述面〔README/STRUCTURE/AGENTS/项目说明全文+CHANGELOG 口径块行+AGENTS 脚注剥离〕vs stats.json·self-test 7→10 例·首跑抓 W514 脚注时点值即产证后剥域）加 AGENTS §4.2 第 31 条目扩 C5 加 文档规范新增 §4.10 聚合数字书写规范（新增聚合量登记制+时点值豁免边界）加 全量禁写与占位符回填不采纳（CHANGELOG 历史段记录当批口径+README 面向读者+W652 机器生成先例）；2026-10-11（v2.3.298 W704）数字实体化批（用户方案第二阶段「数字制度化」）：stats.json 实体化 entity-v1（每键 value/domain/generator/introduced_by/last_changed_by·META 15 键登记制）加 stats-changelog.json 自动变更史与 stats-index.md 反向索引（W→stats key·与 file-index 同构）加 C5b 数字实体标记对账（治理文档 22 处 <!--stats:KEY--> 前置数字==value·键未登记 fail-closed）加 C5c 裸聚合数字 NOTE 报告型（首跑 97 处内容描述数字留观·起步策略）加 self-test 10→12 例（T11/T12 标记负样本·测试串紧贴形态自纠）加 AGENTS §4.2 第 31 条目 C5b/C5c 与文档规范 §4.10 增补（数字实体化+C5 三层分工）；2026-10-11（v2.3.299 W705）Agent开局状态摘要批（用户方案第三阶段第 2 步·3/4/5 分级裁决）：scripts/agent_start.py 开局实读磁盘输出当前事实摘要（现役三元组/近 3 批次/stats 全键/对账表现势/阻塞/三查纪律·--json·stdout UTF-8 兜底）加 AGENTS §7 第 0 步与 CLAUDE.md 接手导航挂接（宿主注入=宿主侧能力的边界如实声明）加 对账表 W702 行首拆分修复（W704 登记 replace 误吞锚点致两行合并·教训=插入语义必须保留锚点自身）加 分级裁决留档（阶段 3 rules.json 生成化驳回=第三规则真源违单一事实源/阶段 4 state.json 驳回=第四份副本/阶段 5 challenge 登记不开工=用户自评诊断性）；2026-10-11（v2.3.300 W706）编号空间盘点与元规则批（用户方案第四五阶段·八项挑刺全采纳）：v 号使用点全量盘点 v2（8791 处/826 文件六类分域+硬耦合 9 项+零命中确认表 CLAUDE.md 0 处实证+三决策点带倾向〔段标题去 v/CITATION 丙=W 号/file-index 甲〕·盘点档 docs/superpowers/plans/2026-10-11-version-space-inventory.md）加 盘点自纠入档（v1 首跑 W523 quotePath 坑漏扫约 1100 处 7679→8791+CITATION 误记 0 单列）加 文档规范 §4.11 编号空间与标识符纪律（编号空间字典/vW 双键元规则/范围词汇定义/行号禁令/裁决记录形态）加 AGENTS §4.3 主题视图索引块与 §5.2 检查层次映射与 §8 清单裁定链加 CONTRIBUTING 补 CLAUDE.md 加 CHANGELOG 头部双键口径加 交接 BL-21/22加 交接文档结构修复（用户挑刺 P0 实锤：W705 块错位主标题前+一、当前进度标题缺失——根因=batch_cascade fb 全文搜首块的错位链自我强化+drop_block 跨段淘汰吞标题·根治四件含标题锚点双形态与段内断言）加 挑刺裁决 3 真 4 旧快照（真=CONTRIBUTING 脱节模板/CLAUDE 缺 agent_start/AGENTS 脚注 BL-23 登记·驳回 4 条附证据）；2026-10-11（v2.3.301 W707）分层重构先行件与阅读契约批（用户方案第十、十一条）：分层重构方案档入库（L0/L1/L2 目标结构+§4.2→gates.md §4.3→pitfalls.md 搬迁映射+硬耦合 7 项〔doc-sync C3 双源/C2 锚点/叙述面豁免裁定〕+验收清单·BL-24 下批按图施工）加 AGENTS 头部索引型阅读契约加 agent_start.py --task 改动路径七类分类输出必读清单（与 W705 全局摘要互补·heredoc 三败后按场景分层铁律 Write 全量重写自证）加 阅读契约头部×10（CHANGELOG 查表/交接 首段/STRUCTURE 索引/README 分段/CLAUDE 通读/归档 4 份禁读·用户明示授权头部元数据历史内容零改动）加 BL-24/25 登记（内容搬迁+正文手术）；2026-10-11（v2.3.302 W708）全变动对抗复审修复批（用户令 review·范围 W702-W707 十提交 140 文件）：机械扫八面 0 异常（双标点/混行尾/契约 10 份/对账表行结构/CLAUDE 44 行/新脚本 17 件 tracked/版本行模板/门禁复跑全绿）加 对抗审读五发现——① batch_cascade 交接结构三断言前置 pend 落盘前 raise（原写后 WARN 性违 fail-closed·双保险保留）② 文档规范 §4.11 盘点引用更新 v2（8791 处/826 文件+9 项）③ W704 段「22 处标记」三重失真勘误（分项和 26 实测 31·W496 现测铁律执行记录·历史段禁改走勘误）④ _w704_ledger_msg.txt 漏 add 补入库 ⑤ W706 chore「翻state」混入留档；审读确认正常面=级联四断言/C5 三层/stats 实体化/交接终态/CITATION/file-index/--task 实测；2026-10-11（v2.3.303 W709）BL-24分层搬迁批（用户 userselect 全选五 Backlog 第一批·BL-23 并入）：L2 三件落地（docs/agent/gates.md 40 条五组重排/pitfalls.md 31 条六主题+shell 查坑表/agent-web.md·内容零改动）加 AGENTS 瘦身（292→275 行·字符 40K→14.9K·摘要层+指针·doc-sync C3 形态保留零改造）加 BL-23 脚注 W458-W700 迁 docs/archive/AGENTS-ARCHIVE.md（尾锚点不变级联透明）加 第 41 门禁 check_agents_layers.py 挂载（C1 L2 三件/C2 三方编号对账/C3 行数上限/C4 指针·self-test 5/5·verify 四处同改自洽 46 段·文档规范 §8 对齐）加 C5 闭环实证（gate_count 40→41 漂移当场被抓并记账）；2026-10-11（v2.3.304 W710）BL-25 与 BL-21 收口批（用户 userselect 第二批）：BL-25 STRUCTURE 02/04 段建置沿革迁 STRUCTURE-ARCHIVE（正文换现数与指针·原文零改动迁入）加 README 拆分评估结论维持不拆（影响大于收益·受众分段由阅读契约承担）加 BL-21 首份豁免盘点报告 docs/00-导读/门禁豁免盘点-2026-10-11.md（十项对仓取数·结论豁免面健康无吞噬证据·第 28 收敛标杆·第 22 与 C5c 起步态跟踪·第 29 大基线待专项收敛·BL-21 关闭转例行）；2026-10-11（W711）方案D形态改造批（用户 userselect 第三批·BL-22 收口·三决策点按倾向落地）：自本段起 CHANGELOG 段标题与治理文档抬头去 v 号（新形态 ### W###（date）：标题·W001-W710 历史形态保留）加 CITATION version 改批次号形态（"W711"·CFF free string·下游无自动化消费者已核）加 file-index 新段 W only（历史双列保留）加 doc-sync 四正则双形态与 changelog_top 二元组化（self-test 12/12）加 verify latest_version 双形态与 dukou/workflows 锚定改造（footer 内联正则/anchor 参数·W708 宽匹配教训应用）加 batch_cascade 段锚点三模板 HEAD 句页脚去 ver（锚点双形态）加 tests 补两用例（295 过）加 workflows 4 处豁免确认（action 版本注释与历史批注·与项目 v 号无关）；2026-10-11（W712）方案档挑刺补正批（用户挑刺第十三次 15 条·三态裁决）：两方案档补执行实录与挑刺补正节（W707 档=L2 实建 3 份裁剪记录加 AGENTS 292 行实测修正加 C2 应验加指纹对账结果；W706 档=漏扫精确 1112 处加含 E 注记加 344 边界加硬耦合 5 实施定案 ver 可 None 加 §五措辞加 CFF 外部平台注记）加 搬迁内容指纹对账实跑（40 条标题+31 条整行守恒 0 缺失·零丢失实证·挑刺 P0 闭环）加 CITATION.cff 补 version 形态注释行（CFF free string）加 阅读契约头部两档加 驳回留档（BL 编号跳空系时点失真/行数估计未实测）。如与上述权威文档冲突，以权威文档为准。*
