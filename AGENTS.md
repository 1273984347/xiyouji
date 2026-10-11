# AGENTS.md — 《详解西游记》项目 Agent 指南

> **📖 阅读契约（W707）**：索引型——不要线性通读。先跑 `python scripts/agent_start.py --task` 拿「本次任务相关」清单按需读节；§4.2 全 41 条门禁与 §4.3 全部坑位属按需查表（L2 已拆分落地：docs/agent/gates.md · pitfalls.md · agent-web.md·W709）；§1-§3/§6 铁律/§7 必读。
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

> **📖 阅读契约（W709）**：索引型——本节=41 槽摘要；完整定义（口径/豁免/历史实证）→ [docs/agent/gates.md](docs/agent/gates.md)；失败排查时按编号查 gates.md。

verify_delivery.py 是提交前唯一硬门禁入口（`.git/hooks/pre-commit` → 本脚本·W698 起本地传 `--scope auto` 分级，CI 与批收尾恒全量，核心 FAIL 返回非 0 阻断）。内含 41 槽，五组：

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

*本文件由 AGENTS 通读项目后生成于 2026-08-16（v2.3.73 W458）；W458-W707 沿革已迁 [docs/archive/AGENTS-ARCHIVE.md](docs/archive/AGENTS-ARCHIVE.md)（W709 BL-23 建·W713 续迁 W701-W707·W719 续迁 W708-W714·W715-W716 级联自动滚动·脚注保留最近 5 条·grep 查勿通读）；2026-10-12（W717）页脚链头锚定根修批（用户 userselect 圈选上批遗留候选现做）：四页脚级联锚改 footer 区内首个批次 token 双形态（根修 v 形态锚落手工时代 W 形态头块之下致新批每批插链中加 dukou 新鲜度门禁读链头恒 WARN 需手工归位两度实证）加 插入改位置切片消除 replace 全文首处歧义隐患加 本批级联即新锚真数据首跑（四页链头=W717 加 dukou 门禁自洽后续免手工归位）加 链长治理（四链 12-17 token 无淘汰契约）登记观察待契约；2026-10-12（W718）变更史可追踪补正批（用户挑刺第十六次 stats-changelog 专项 5 项裁决 采纳 3/部分升格 1/快照澄清 1）：W704 空条目考古定谳（首入库时终版 append 逻辑已条件式·系建账批开发迭代产物·保留加 note 不删史加报告 2 条系快照现 3 条）加 变更史 schema v1（_schema 加 _field_notes 加 entries·旧 list 自动迁移）加 entry time 字段（迁移旧条目 null）加 反向查找分工声明（流水账权威加反查走 stats_index 反向段）加 C5d 挂载第 31 门禁（doc-sync 内联 subprocess 跑 stats check 0.3s 恒跑·漂移当场 FAIL·W715 漏刷实例机器防线·self-test 12→13 例）；2026-10-12（W719）review 修复批（用户令 review 一遍·本会话四批八提交对抗复查）：机械扫八面净（混行尾 19 文件 0 加 段标题双写 0 加 四页脚链头全 W718 加 豁免链连续加 契约头全在）加 口径误报澄清（CHANGELOG 三处双标点系 W708 历史段黑名单引述·历史段禁改·机械扫须豁免括号引述形态）加 R1 脚注滚动修复（AGENTS 脚注 11 条破 W713 保留最近 5 条制度·级联只加不滚根因·W708-W714 七条迁 ARCHIVE 保留 W715-W719 加 级联内建滚动登记根修候选）加 R2 补库收口（级联 spec 加 msg 6 件加 并行会话级联清单 2 件统一入库）加 门禁复跑全绿（verify 46 段零 WARN 加 pytest 296 加 self-test 四连加 stats 零差异）；2026-10-12（W720）C4 认领行强制批（用户 userselect 圈选 W719 流程遗漏根修）：C4 细分强制（CHANGELOG 现役段 W 号须有对账表表格行认领加预留豁免 bullet 不算认领加动工未登记主提交即红加 W719 被豁免 bullet 救场实证不可区分根因）加 self-test 13→14 例（T14 仅 bullet 形态必红）加 gates 第 31 条与 pitfalls 认领流程五步同步加 本批先登记认领行再动工（新防线首次合规执行）加 浅克隆同既有 C4 跳过；2026-10-12（W721）复盘增补与脚注滚动根修批（用户令复盘第八次执行加中途裁决并入第 37 篇）：复盘增补 §十（续弧线 W713-W720 六批加 E-09 制度必须内建执行机制领衔加 S-29 已交付加 S-30 待拍板加 P-14~26 十三例全闭环加 FAM-12 升橙警单周期 6 起·强化建议 S-28 例行化待裁决加 FAM-14 制度无执行机制新族双根修落地加 FAM-02 黄警根因再分析清单 add 机械化待裁决）加 S-29 级联脚注滚动内建交付（batch_cascade AGENTS 脚注面加条后超 5 条自动迁最老条至 AGENTS-ARCHIVE 尾块第 12 面加指针上界刷新加条目序切分连续性尾锚断言加本批 7 条迁 2 留 5 真数据首跑·W719 R1 制度破约根因闭环）。如与上述权威文档冲突，以权威文档为准。*
