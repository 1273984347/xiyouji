# AGENTS.md — 《详解西游记》项目 Agent 指南

> 本文件面向进入本仓库工作的 AI Agent（及新接手的人类维护者），提供项目的用途、技术栈、目录结构、关键模块、依赖关系、构建运行方式与必须遵守的铁律。动手前请通读；更细的规则以文末「权威文档」为准。
>
> **维护契约（防乱写）**：本文档是 Agent 协作指南，只允许结构性编辑——① 保持 §1–§8 骨架不变；② 新增铁律/规则必须**就地并入对应章节**并全篇去重（禁止追加「速记 / 补充」尾部段落）；③ 版本脚注更新须与当前 HEAD（vX.Y.Z W###，用 `git rev-parse --short HEAD` 核对）一致；④ 与 交接文档 / 文档规范 / CHANGELOG 冲突时以后三者为准。

---

## 1. 项目用途与定位

**《详解西游记》**（xiyouji）是一个「一源多形 · 数字人文可视化解读《西游记》100 回」的项目。它把《西游记》的文本研究组织为四层产物：

- **文档（Docs）**：Markdown 写就的逐回解读、人物分析、主题专题、文化背景、诗词赏析、个人随笔。
- **站点（Site）**：可浏览的纯静态 HTML 站点，`file://` 双击即可打开，部署于 GitHub Pages（https://1273984347.github.io/xiyouji/ ）。
- **数据可视化**：86 个 D3.js / Three.js 可视化页（site/data/ 共 87 个 HTML，「86」不含模板壳 _shell.html），覆盖 133 个数据维度（章节统计、人物关系网络、八十一难热力图、取经路线、情感热力图、AI 对话等 34 类主题 A–AH）。
- **可问询入口**：Web Agent「西游记·渡口问津」（xiyouji-agent-web/）——基于 CodeBuddy Agent SDK，可对话、检索 docs/source、跑脚本。

**核心内容规模**：A1–A6 内容板块共 615 篇（A1 逐回 100 / A2 随笔 44 / A3 人物 215 / A4 主题 209 / A5 文化 34 / A6 诗词 13；算法与边界见 docs/00-导读/统计口径说明.md；W505 起 611→615）；英文站 site/en/ 138 页已全量英文化。

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
| Web Agent | React 18 + Vite 5 + TypeScript + TDesign React + Express 4 + better-sqlite3 + `@tencent-ai/agent-sdk`（CodeBuddy Agent SDK） |
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
│   ├── data/              # 可视化页（87 个 HTML，D3/Three；「86 可视化页」口径不含模板壳 _shell.html）
│   ├── en/                # 英文站（138 页）
│   ├── static/js|css|fonts/  # 本地化 D3/Three、tokens.css/system.css、子集化字体
│   └── sitemap.xml
├── scripts/               # Python/JS 工具链（门禁、生成器、审计、诊断）
│   ├── verify_delivery.py # 交付门禁（pre-commit 强制，见 §5）
│   ├── generate_csp.py / inline_css.py / bump_version.py / lint_links.py
│   ├── check_*.py|js      # 各专项门禁
│   ├── run_all.py         # 批量运行 A-AH 34 类分析
│   ├── _*.py|js           # 一次性/诊断脚本（不入库门禁、不参与 CI）
│   └── output/            # data/*.json（可视化数据源）+ file-index.md + screenshots/
├── dataset/               # 结构化 JSON（可视化/API 数据源）
├── xiyouji-agent-web/     # Web Agent「西游记·渡口问津」（React+Vite+Express）
├── skills/                # 项目级 playbook skill（19 个，见 §4.5）
├── mcp-server/            # MCP 工具（xiyouji_mcp.py：drl_spotcheck 等）
├── tests/                 # pytest + Playwright E2E
├── assets/                # 字体源、图片
├── references/  timeline/  tools/  hyperframes/
├── README.md / STRUCTURE.md / CHANGELOG.md / DESIGN.md / 交接文档.md / 新Agent启动Prompt.md
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

### 4.2 交付门禁体系（verify_delivery.py，pre-commit 强制）

`scripts/verify_delivery.py` 是提交前唯一硬门禁入口（`.git/hooks/pre-commit` → 本脚本，核心 FAIL 返回非 0 阻断）。内含：

1. **六文档同步**（核心 2 硬门禁：CHANGELOG.md + 交接文档.md 必须含当前 v/W——期望版本由 verify_delivery 动态取自 CHANGELOG 现役版段，dukou-engine.html 页脚降级为新鲜度 WARN（W518 起）；辅助 4 仅 WARN：README / STRUCTURE / 项目说明 / file-index）
2. **范围漂移检测**（html 最高 W ≤ 文档+归档最高 W）
3. **A4 计数一致（EXPECT_A4 字面量「209 篇」）** + **A1-A6 真实计数（六板块顶层 .md 磁盘计数 == README「共 N 篇」声明，当前 N=615）**
4. **学术研究轨显式引用**（105 篇）
5. **A1 导航相邻性**（上一回=N-1·下一回=N+1）
6. **docs/01 链接校验**（lint_links 0 broken）
7. **sitemap 覆盖**、**site/data 回退模式**
8. **CSP 漂移**（generate_csp.py --check，233 页哈希 0 漂移）
9. **数据漂移**（check_data_drift.js）、**腐蚀/插件**（check_corruption.py）
10. **内联脚本语法**（check_js_syntax.js，node vm.Script 批量编译，含 EN 站）
11. **CSS 结构平衡**（check_structure.py，括号/引号/url 闭合）
12. **token 覆盖率**（check_token_coverage.py，W493 转正：页面私有 `<style>` 块 UI 裸色——无豁免注释页必须 0、带 `e-track-exempt` 注释页 ≤ 登记 N；真裸 box-shadow 必须 0；INLINED 副本跳过，私有块识别靠 `tokens.css —` 注释特征）
13. **动效禁止清单**（check_motion_ban.py，W493 转正：cubic-bezier 负值 / 360° 旋转 / animation infinite / parallax，白名单仅 .chart-loading/.chart-fade-in）
14. **a11y 对比度**（a11y_audit.py E2-2，W493 挂载：P0+P1=0 阻断，WCAG 2.2 AA 正文 ≥4.5:1）
15. **INLINED CSS 完整性**（check_inlined_css.py，W495 转正：data/EN 页 INLINED 标记块内容 ≥20KB——防 W493 式「224 页内联块被清空而 14 门禁全绿漏网」回归）
16. **Skills 索引一致性**（check_skills_index.py，W498 转正：skills/ 目录数 == README 索引数 + 目录短名 ⊆ AGENTS §4.5 + skills/ 全部文件 git tracked（防 day-review 式建了未入库）+ frontmatter name == 目录名 + 正文引用资产存在性（W515 检查 5：skills/**/*.md 内 scripts/*.py|.js 引用对磁盘断言·DEFAULT_ALLOWED_MISSING 冻结豁免文档示意占位名——堵 _shot_check.js 式失效指针）；配套本地工具 scripts/sync_skills.py：--check 带漂移方向判定（frontmatter 版本号优先、mtime 弱证据），--sync 对「全局更新/同版冲突」默认拒绝以防静默降级（--force 越权），--take-global 反向回写，--self-test 负样本自检；比对统一 CRLF→LF 归一化，W531；W533 新增 MIRROR_SKILLS 显式归属策略（agent-session-loop / deep-review-loop / mem-wrap-up / self-evolution 以全局为 master，--sync/--force 均不得覆盖镜像方向）
17. **索引健康**（check_index_health.py，W500 转正：file-index 段完整性/唯一性/最新段残留（豁免 W449-W463 损坏区·仅防新增）+ 方法论 README 双向覆盖（目录 md ↔ 索引链接·待创建占位 0）+ CHANGELOG 编号规则段上限 == 最新 W 段 + 治理文档引用一致性（文档规范.md scripts 引用存在性·verify 挂载脚本存在性）；W526 扩展：段倒序断言（豁免区外 W 号严格递减·防尾部追加）+ 段缺失检测（CHANGELOG 现役版段须均有 file-index 登记段））
18. **元信息块 v2**（check_frontmatter.py，W501 挂载：内容可信度轨——新文件（不在基线清单内）必须含血缘 + 核验状态 4 字段：生成来源（skill@commit 或 人工撰写）/生成模型（含「未记录」合法·禁编造）/生成日期 YYYY-MM-DD/核验状态三值枚举；基线 frontmatter-baseline.txt 冻结存量 611 篇豁免；口径见文档规范 §4.6）
19. **术语一致性**（check_glossary.py，W502 挂载：术语表↔dataset/glossary.json 双向同步（--generate 解析生成·禁手改）+ 人物称谓组规范词锚定（传递归一 圣僧→唐僧→玄奘·复合词掩码 心猿意马/金公木母黄婆）；基线 glossary-baseline.txt 冻结存量 303 篇 383 条豁免·只拦新增；口径见文档规范 §4.7）
20. **原著引文硬验证**（check_citations.py，W503 挂载：`> 原文引文（第N回）：“…”` 行必须对 dataset/text-search.json 去空白归一后精确子串命中·防 AI 幻觉引文；--dir docs 全量·任何未命中 = FAIL·存量引文行 = 0 无豁免；语法见文档规范 §4.8）
21. **动态链接门禁**（check_dynamic_links.py，W459 挂载：解析页面 JS 内拼接生成的链接目标（A1_DOC_MAP 映射、EN source_doc 等）并对仓库路径存在性断言，补 lint_links 静态盲区，死链 = FAIL 阻断提交）
22. **治理文档维护契约**（check_governance_docs.py，挂载即生效：七项检查扫描六文档——历史段遭改写 / 现役值残留多份 / 尾部追加速记段 / 「最后更新」新鲜度（W518 挂载：头部滚动链与尾页脚历史链两处链首条目均须 == CHANGELOG 现役段·finditer 全量扫描），命中记 WARN 不阻断提交（起步策略），为后续转 FAIL 积累监测数据）
23. **旁文档同步**（W526 挂载：.github/workflows/README.md 头部版本行（vX.Y.Z W###）== CHANGELOG 现役段 + 里程碑行 W450-W### 上限 == 现役 W，任一不符 FAIL——W499/W525 两次实证旁文档滞后漏网，verify 覆盖外盲区封堵）

### 4.3 脚本工具链要点

- **改任何内联脚本后，必须重跑 `python scripts/generate_csp.py`**——否则 CSP sha256 哈希失配，整个内联脚本被浏览器拒执行（症状：无 pageerror 但内容空白、`window.__data` 未设置）。
- **批量正则改 CSS/JS 后必须验证括号/引号平衡**（`check_structure.py` / `_find_css_breaks.py`）。
- **CHANGELOG/方案档验收数字必须当批现测**（W496 铁律）：写 M 指标/内联字节数等数字前先跑 `python scripts/acceptance_snapshot.py` 从输出抄，禁止从上一批 CHANGELOG 复制（W493「28385B」跨批复制曾掩盖全站 INLINED 清空事故）。
- **bump_version.py** 一键补齐辅助 4 文档版本行；**三个已知坑（①②多次复现 W524 扩证·③W528 实证）**：① 全局替换会污染 file-index 历史段（生成「WXXX WXXX」重复标题的空壳段、登记表为空，需手工补全当批文件表）；② `--desc` 与 `--note` **均会**往 STRUCTURE.md 头部 / docs/00-导读/项目说明.md 的上一版本行**追加**「 + WXYY(...)」而非替换主描述（W523 实测 `--note` 同样触发——此前仅登记 `--desc` 单触发面）；③ 三简单页脚（index/cross-time-danmaku/tag-cloud）同步为替换式、只匹配"链首 == 解析版本"的条目，页脚一旦滞后就永不被命中（W528 实证停在 W453 脱节 74 批）——跑完必须 Grep 校验版本行三处 + 三页脚版本实际前进并手工净化。
- **CHANGELOG 多版段插入/重排只用脚本 + 结构断言**（锚点唯一性 + 版段 order 校验），手工 Edit 大段会吞相邻版段标题；**新批版本号先 Grep 现役段取 max+1 再写**（防撞号）。
- **批量改 md 一律 Python `open(encoding='utf-8')`，禁用 PowerShell `Set-Content`**（后者默认写 UTF-8 BOM，项目 W427 曾全库清 BOM；`Add-Content` 同理慎用）。
- **同文件多个 Edit 必须串行执行**（并行 Edit 基于同一原始内容计算 diff，后写覆盖先写——W505 复现 4 次：金角银角「唐僧肉」/CHANGELOG W506 段/项目说明头部/交接文档标题均丢失）；并行批次后必须 Grep 验证所有修改点。
- **写 `> 原文引文` 行前先跑 `python scripts/_cite_probe.py --kw <关键词> --chap <回目>`** 从 text-search.json 提取候选，禁止凭记忆编造（W503 门禁只拦截"写入后未命中"，无法拦截"恰好像原文的编造"）；新文档（非基线豁免）用变体称谓（行者/唐僧/圣僧等）必须同时含 canonical（孙悟空/玄奘），写作前 Grep `dataset/glossary.json` 称谓组。
- **Windows 多行字符串/heredoc 一律走 Write 临时文件 + 命令 `-F` 参数 + Delete 临时文件**，禁用 `cat <<'EOF'` heredoc（PowerShell 不支持，报错；W514 git commit -F 中文提交信息二度复用教训）。
- **跨 session / 涉及远端状态**：执行前先 `git log --oneline -5` + `gh run list` 确认最新状态，识别并行交付真实增量（E41）；workflow 触发条件必须匹配真实开发流、门禁建置即绿、引用文件先 `git ls-files` 确认（E36-E42 CI 类，详见交接文档「三」W516 段）。
- **共享机制必须写入仓库内文件（git tracked）**：任何要让其他 Agent 读到的机制/规则/经验，一律写仓库内公共载体（AGENTS.md / 交接文档 / skills/ / docs/10-方法论沉淀/），**禁止只写全局路径**（如 `c:\Users\...\.trae-cn\skills\`）——其他 Agent 在项目 session 读的是仓库版，且 `sync_skills.py --sync` 为仓库→全局单向（全局修改会被覆盖）。改 skills/ 下任何 skill 必须改仓库版后 `python scripts/sync_skills.py --sync` 同步全局（W516 教训：上移机制曾误写全局版，被用户指出载体错误）。**例外**：§4.5 的 4 个镜像技能以全局为 master——仓库侧改动用 `--take-global` 回写，`--sync`/`--force` 会被 MIRROR_SKILLS 拒绝（W537 补交叉引用，此前与本节矛盾）。
- **workflow/脚本用 git diff 输出做路径分类必须加 `-c core.quotePath=false`**（W523）：git 默认把非 ASCII 路径输出为带双引号的八进制转义串（交接文档.md → `"\344\272\244..."`），首尾引号破坏 bash case/glob 匹配（连 `*.md`、`docs/*` 都失配）→ 免审/定向分支被静默架空、恒走兜底全量（Screenshot Review scope 步骤曾因此每次推送 ~11min 全量截图）；验证靠本地 Git Bash 复刻分类逻辑对真实范围双向模拟。
- **W537 三新规（W536 批次声明失真复盘）**：① CHANGELOG「验证」栏必须以当批实跑 `verify_delivery` 的输出为准填写，「状态」栏仅在提交/推送实际落地后为真——自制批量文档脚本绕过 bump_version 防护时同样适用（W536 实证：声明先于验证 → 4 项 FAIL 状态下写出「全绿 + 已推送」）；② 版本行/页脚更新须整行替换并同步改描述文本——第 22/23 门禁只校验 W 号不校验描述（三简单页脚「W536 号挂 W535 描述」串号实证）；③ CHANGELOG「文件」清单中的新建文件必须 `git add`——无门禁覆盖「清单 ⊆ tracked」，漏 add 即静默丢失（eslint.config.mjs 实证）。
- `_` 前缀脚本为一次性/诊断脚本，不入库门禁、不参与 CI。

### 4.4 Web Agent（xiyouji-agent-web/）

- 后端 `server/index.ts`（Express + SSE 流式 + SQLite `data/chat.db`），前端 `src/`（React18 + Vite5 + TDesign）。
- 凭证 `CODEBUDDY_API_KEY`（`.env`，由 `.env.example` 复制，已 gitignore）。
- 默认 `PROJECT_CWD=D:/1/xiyouji`（env 可覆盖）；专属 Agent「渡口问津」内置项目 sysprompt；权限默认 `default`（UI 可切 `acceptEdits`/`plan`；`bypassPermissions` 仅当服务端 env `AGENT_WEB_ALLOW_BYPASS=1` 时放行，否则降级 default——W411 加固，W537 文档校正）。
- 核心入口：`server/index.ts`、`src/hooks/useAgents.ts`（DEFAULT_AGENT）、`src/config.ts`（主题色 #c8463a「西」Logo）、`src/pages/ChatPage.tsx`。

### 4.5 项目级 Skills（skills/）

- 会话流程（4 个）：agent-session-loop（审查→收尾→沉淀 整合流水线）、deep-review-loop（DRL 5 轮审查）、mem-wrap-up（7 步收尾）、self-evolution（复盘沉淀）。**归属（W533）**：这 4 个通用会话流程 skill 的唯一 master 是全局安装版 `~/.qwenworkcn/skills/`，本仓库 `skills/` 副本是 git tracked 受控镜像（满足「共享机制须入库」铁律），只允许 `sync_skills.py --take-global` 回写，`--sync`/`--force` 均不得覆盖（`MIRROR_SKILLS` 强制）；其余 15 个 xiyouji-* 仍以本仓库为真源
- 角色 skill（5 个）：sun-wukong / zhu-bajie / sha-seng / tangseng / bai-longma
- 内容/知识：character-content、characters-knowledge
- 流程（5 个）：version-bump、en-translation、s4-submission、day-review（当日 W 批次收尾审查）、drift-audit（任意时刻全仓漂移体检，与 day-review 互补）
- 视觉/方案专项（3 个）：visual-batch（Phase E 视觉批次执行）、plan-authoring（W 批次方案撰写）、plan-review（方案评估）

### 4.6 MCP 服务（mcp-server/）

`xiyouji_mcp.py` 暴露项目 MCP 工具（如 `drl_spotcheck`），供外部 Agent 调用。

---

## 5. 构建与运行方式

### 5.1 统一编排（Makefile）

```bash
make help          # 查看全部目标
make analyze       # 批量运行 A-AH 34 类分析（scripts/run_all.py）
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
# 需先复制 .env.example → .env 并填入 CODEBUDDY_API_KEY
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

1. 读 `交接文档.md`「零、当前阻塞」+「一、当前进度」→ 当前 HEAD（vX.Y.Z W###）、下一 W 编号、遗留待办。
2. 读 `README.md` → 项目全貌、内容规模、在线站点、双协议。
3. 读 `docs/00-导读/文档规范.md` §11 → 文件管控清单（必同步/禁擅改/接手速查 6 步/同步核对 10 项）。
4. 读 `交接文档.md`「三、方法论沉淀」→ 可复利经验。
5. 深挖结构看 `STRUCTURE.md`、`scripts/output/file-index.md`（反向索引）、`CHANGELOG.md`（正向时间线）。
6. 动手前跑 `python scripts/verify_delivery.py` 确认基线全绿。

---

## 8. 权威文档（冲突时以此为准）

- 进度中枢 / 规则：`交接文档.md`、`新Agent启动Prompt.md`（速用精简版）
- 文档规范：`docs/00-导读/文档规范.md`（尤其 §11 文件管控）
- 设计规范：`DESIGN.md`（§1-4 视觉 / **§5 动效契约**）
- 目录结构：`STRUCTURE.md`
- 变更日志：`CHANGELOG.md`（正向）+ `scripts/output/file-index.md`（反向）
- 诊断 SOP：`docs/10-方法论沉淀/前端显示问题诊断SOP.md`

---

*本文件由 AGENTS 通读项目后生成于 2026-08-16（v2.3.73 W458），2026-08-17（v2.3.78 W463）墨韵系列复盘增补动效契约（§1/§6-12/§8）与 W 批收尾坑（§4.3），2026-08-18（v2.3.80 W477）增补维护契约与文档治理段，2026-08-19（v2.3.83 W484）skills 治理：§4.5 补录 4 个会话流程 skill（共 14 个），2026-08-19（v2.3.84 W485）收录视觉/方案专项 3 skill（visual-batch / plan-authoring / plan-review，共 17 个），2026-08-19（v2.3.85 W486）四会话流程 skill 协议同步（verdict 7 词 / R0 4 件套 / 警报增强 / P2 残留 / work-log 路径 / 整合版协调），2026-08-19（v2.3.86 W487）四会话流程 skill 二轮同步（DRL 未安装降级声明 + experience-capture 格式规范 + 触发词扩充），2026-08-22（v2.3.93 W494）Phase E 收官同步：§4.2 补录 W493 转正三门禁（token 覆盖率 / 动效禁止清单 / a11y 对比度，现 14 条），2026-08-22（v2.3.94 W495）P0 热修复同步：§4.2 补录 INLINED CSS 完整性门禁（现 15 条），2026-08-22（v2.3.95 W496）优化收尾同步：§4.3 补录验收数字当批现测铁律（acceptance_snapshot.py），2026-08-24（v2.3.96 W497）skills 治理同步：§4.5 补录 day-review（流程类 4 个·共 18 个）+ 版本脚注，2026-08-24（v2.3.97 W498）防漂移门禁：§4.2 补录第 16 门禁 check_skills_index（Skills 索引一致性）+ §4.5 注明配套 sync_skills.py 同步工具，2026-08-24（v2.3.98 W499）GitHub 协作模板 + 创意方法论沉淀批次：无 § 结构性变更（.github issue/PR 模板 + 创意方法论 2 篇 + character-content 创意方法引用 + 方法论 README 索引修复 + file-index 结构注记），仅版本脚注同步，2026-08-24（v2.3.99 W500）索引健康门禁：§4.2 补录第 17 门禁 check_index_health（file-index 段完整性/方法论 README 覆盖/编号上限·豁免 W449-W463 损坏区），2026-08-24（v2.3.100 W501）内容可信度轨启动：§4.2 补录第 18 门禁 check_frontmatter（元信息块 v2·新文件血缘+核验状态 4 字段·基线豁免 611 篇·口径文档规范 §4.6），2026-08-24（v2.3.101 W502）术语一致性门禁：§4.2 补录第 19 门禁 check_glossary（术语库类型化·称谓组规范词锚定·基线豁免 303 篇 383 条·口径文档规范 §4.7），2026-08-24（v2.3.102 W503）原著引文硬验证：§4.2 补录第 20 门禁 check_citations（引文行对 text-search.json 精确命中·防 AI 幻觉引文·口径文档规范 §4.8），2026-08-25（v2.3.103 W504）存量核验状态基线：无 § 结构性变更（611 篇核验状态全覆盖 + 学术轨 105 篇 A+ 引文核验·content-trust-report 产出），仅版本脚注同步，2026-08-25（v2.3.104 W505）创意流程闭环落地：无 § 结构性变更（character-content 新增创意三明治管线章节 + 4 篇试点方向二深化），仅版本脚注同步，2026-08-25（v2.3.105 W506）处置遗留：无 § 结构性变更（删除失锚测试 test_fix_svg_negative_widths.py），仅版本脚注同步，2026-08-25（v2.3.106 W507）复盘沉淀落地：无 § 结构性变更（引文探针 _cite_probe.py 永久化 + day-review 归档查测试规则），仅版本脚注同步，2026-08-25（v2.3.107 W508）复盘剩余项收口：无 § 结构性变更（creative-methods 方法四去重指向 SKILL 管线章节 + _check_pipeline_consistency.py 管线一致性轻量校验），仅版本脚注同步，2026-08-25（v2.3.108 W509）经验上移共享：§4.3 工具链新增 3 条强制规则（Set-Content BOM 禁 / 同文件 Edit 串行 / 引文探针+canonical 预查）+ §6 铁律新增第 13 条内容可信度轨，2026-08-25（v2.3.109 W510）治理文档修复：无 § 结构性变更（文档规范 §8 门禁数 17→20 + §11.4 核心口径统一），仅版本脚注同步，2026-08-25（v2.3.110 W511）治理文档健康指标归档：无 § 结构性变更（CHANGELOG/file-index/交接文档概要 三档瘦身·W417-W464 段归档），仅版本脚注同步，2026-08-25（v2.3.111 W512）CI 安全批次：无 § 结构性变更（security_scan pip-audit 超时 120→300s·DEP-001 误报归零），仅版本脚注同步，2026-08-25（v2.3.112 W513）归档二级归档：无 § 结构性变更（CHANGELOG-ARCHIVE W001-W399 下移 docs/archive/tier2·归档三件套 >1MB 触发规则入文档规范 §5/§8），仅版本脚注同步，2026-08-25（v2.3.113 W514）治理文档口径修复：§1 规模数字校正（核心内容 611→615·A3 人物 211→215·「约 86 个可视化页」注明＝site/data 87 个 HTML 减 _shell.html）+ §4.2 第 3 条改为动态口径（磁盘==README 声明）+ §4.2 补录第 21 门禁 check_dynamic_links（动态链接）与第 22 门禁 check_governance_docs（治理契约），2026-08-25（v2.3.114 W515）渲染抽查常驻化与门禁扩展：§4.2 第 16 门禁补录正文引用资产存在性子检查（堵 _shot_check.js 式失效指针），无其他 § 结构性变更，仅版本脚注同步，2026-08-25（v2.3.115 W516）经验上移机制固化：§4.3 补录 Windows heredoc 禁（Write 临时文件 + -F 参数）+ 跨 session 先确认远端 / workflow CI 类经验（E41/E36-42·详见交接文档「三」W516 段）；mem-wrap-up Step 5 固化上移检查子步骤（毕业路径 + 上移映射表 + 强制登记交接文档「三」），2026-08-25（v2.3.116 W517）共享机制载体铁律：§4.3 补录「共享机制必须写入仓库内文件（git tracked）」——禁只写全局路径（其他 Agent 读仓库版 + sync_skills 仓库→全局单向·W516 载体错误教训固化），2026-08-25（v2.3.117 W518）期望版本动态化 + 尾页脚新鲜度门禁：§4.2 第 1 条补录动态版本源（verify_delivery 期望版本动态取自 CHANGELOG 现役版段·dukou-engine.html 页脚降级为新鲜度 WARN）+ 第 22 门禁扩为七项检查（新增「最后更新」新鲜度：头尾两处链首现役校验·finditer 全量），2026-08-25（v2.3.118 W519）skills 全目录审查与 SKILL.md 内容优化：§3 目录树注释 skill 数 17→19（README 与 §4.5 本就正确·树注释漏更修正），无其他 § 结构性变更，2026-08-25（v2.3.119 W520）递增数字禁字面量 + skills 内文数字比对维度：无 § 结构性变更（plan-authoring 去模糊化标准⑤ + day-review 步骤 4 第 8 条 + drift-audit 步骤 5 第 4 条固化·E46 登记交接文档「三」，E45 已被 W460-W463 三坑占用顺延），仅版本脚注同步，2026-08-25（v2.3.120 W521）存量裸字面量清剿 + W463 三坑补登记：无 § 结构性变更（DRL F2 15 文件三分类裁决——现状声明改引用式/口径加注/门禁模板豁免·交接文档「三」补 W463 段 E45 编号空间完整化），仅版本脚注同步，2026-08-25（v2.3.121 W522）CI 红灯修复：无 § 结构性变更（scripts/ ruff 16 错误清零——inject_goatcounter.py:68 字符串未闭合根因修复 + 12 lint 机械清理 7 文件·行为零变更），仅版本脚注同步，2026-08-25（v2.3.122 W523）截图审查恒全量根因修复：§4.3 工具链新增「workflow/脚本用 git diff 输出做路径分类必须加 -c core.quotePath=false」条目（中文路径八进制转义致 case 匹配失效·曾静默架空 W421 截图提速机制），2026-08-25（v2.3.123 W524）bump 追加污染坑位补记：§4.3 bump_version.py 条目修订——已知坑②扩为 --desc/--note 双触发（W523 实测 --note 同样追加污染·非仅 --desc）+ 坑①补充 file-index 空壳段现象，2026-08-26（v2.3.124 W525）漂移审查修复：无 § 结构性变更（drift-audit 处置 file-index W504 段缺失补建 + W522-W524 尾部追加重排归位·workflows README 同步至 W524·文档规范 §8 门禁表对齐 AGENTS §4.2 22 条），2026-08-26（v2.3.125 W526）索引健康门禁盲区封堵：§4.2 第 17 门禁扩展（段倒序断言 + 段缺失检测）+ 新增第 23 门禁 check 旁文档同步（workflows/README.md 头部版本行 + 里程碑行上限 == 现役 W），2026-08-26（v2.3.126 W527）drift-audit 技能补漏维度：无 § 结构性变更（SKILL.md v1.2.0 步骤 3 段缺失双向核对 + 豁免区外新增乱序 P1 判级——W525 实证对齐·reference 命令/案例同步·sync 双轨一致），2026-08-26（v2.3.127 W528）存量漂移点统一修复：§4.3 bump_version 条目扩坑③（三简单页脚替换式盲区·滞后即永久脱节——W528 实证停 W453 脱节 74 批）+ 交接文档「三」W528 段登记；六文档 9 处静态描述对齐现役口径（skills 17→19·A3 211→215·学术索引 50→55·site/data 46→86·D3 本地化·README 索引去版本号）+ index/cross-time-danmaku/tag-cloud 三页脚补现役 W528，2026-08-26（v2.3.128 W529）R6 拦截落地 + W464 方案 v7 回填：§4.3 bump_version 坑③修复首次运行时验证（三页脚链首==解析版本被正常替换）；无其他 § 结构性变更（goatcounter beacon 纵深防御拦截 5 点 + 方案 12 处表述具体化），2026-08-26（v2.3.129 W530）决策闸门工程落地：无 § 结构性变更（judge_gate.py 新建 + 读者数据复盘模板 + 方法论索引登记），仅版本脚注同步，2026-08-29（v2.3.130 W531）skills 三真源降级保护：§4.2 第 16 门禁配套工具条目修订（sync_skills 增 judge_direction 方向判定 + --sync 降级拦截 + --take-global 反向回写 + LF 归一化比对 + --self-test 4 负样本——W531 实证旧 --sync 会把 QwenWork 侧演进的 4 个通用技能静默降级），2026-08-29（v2.3.131 W532）交接文档滚动链治理：无 § 结构性变更（第 7 行「最后更新」9 批堆叠裁回维护契约②上限 3 批·删 6 批前逐批断言 CHANGELOG 有段·第 22 门禁只校验链首不校验长度），2026-08-29（v2.3.132 W533）skills 归属策略显式化：§4.5 四通用会话流程 skill 标注 master=全局安装版/仓库副本为受控镜像（MIRROR_SKILLS 禁 --sync/--force），§4.2 第 16 门禁条目补记该策略与 --self-test 5 负样本，2026-08-30（v2.3.133 W534）治理文档递增数字字面量修复：无 § 结构性变更（交接文档「九、使用说明」第 2 条「接续 W 编号」写死 W 号改引用式表述 + 六份治理文档全量复扫 0 残留），仅版本脚注同步；2026-08-30（v2.3.134 W535）决策闸门取数自动化：§4.3 bump_version 条目新增坑⑨（全文模式替换会污染交接文档历史段·检测用逐行相似度 0.80≤r<1.0 再过滤 LF/CRLF 噪声）+ 坑⑤适用面由「git commit -F」扩至 Windows 原生程序一切路径实参（version-bump v1.6.0 收录）·无其他 § 结构性变更；2026-09-02（v2.3.135 W536）依赖积压治理：无 § 结构性变更（dependabot ignore semver-major + eslint.config.mjs 新建·迁移评估出档；收尾补 Mimosa 闸门 77 高危清零——全仓脚本写路径守卫/去动态执行/请求边界加固/server 工作目录钳制），仅版本脚注同步；2026-09-05（v2.3.136 W537）全仓对抗性审查修复：§4.3 新增 W537 三新规·§4.3 sync 指引补 MIRROR_SKILLS 例外交叉引用·§4.4 权限默认值校正·§5.2 命令对齐 CI 同轨。如与上述权威文档冲突，以权威文档为准。*
