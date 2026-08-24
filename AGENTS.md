# AGENTS.md — 《详解西游记》项目 Agent 指南

> 本文件面向进入本仓库工作的 AI Agent（及新接手的人类维护者），提供项目的用途、技术栈、目录结构、关键模块、依赖关系、构建运行方式与必须遵守的铁律。动手前请通读；更细的规则以文末「权威文档」为准。
>
> **维护契约（防乱写）**：本文档是 Agent 协作指南，只允许结构性编辑——① 保持 §1–§8 骨架不变；② 新增铁律/规则必须**就地并入对应章节**并全篇去重（禁止追加「速记 / 补充」尾部段落）；③ 版本脚注更新须与当前 HEAD（vX.Y.Z W###，用 `git rev-parse --short HEAD` 核对）一致；④ 与 交接文档 / 文档规范 / CHANGELOG 冲突时以后三者为准。

---

## 1. 项目用途与定位

**《详解西游记》**（xiyouji）是一个「一源多形 · 数字人文可视化解读《西游记》100 回」的项目。它把《西游记》的文本研究组织为四层产物：

- **文档（Docs）**：Markdown 写就的逐回解读、人物分析、主题专题、文化背景、诗词赏析、个人随笔。
- **站点（Site）**：可浏览的纯静态 HTML 站点，`file://` 双击即可打开，部署于 GitHub Pages（https://1273984347.github.io/xiyouji/ ）。
- **数据可视化**：约 86 个 D3.js / Three.js 可视化页（site/data/），覆盖 133 个数据维度（章节统计、人物关系网络、八十一难热力图、取经路线、情感热力图、AI 对话等 34 类主题 A–AH）。
- **可问询入口**：Web Agent「西游记·渡口问津」（xiyouji-agent-web/）——基于 CodeBuddy Agent SDK，可对话、检索 docs/source、跑脚本。

**核心内容规模**：A1–A6 内容板块共 611 篇（A1 逐回 100 / A2 随笔 44 / A3 人物 211 / A4 主题 209 / A5 文化 34 / A6 诗词 13）；英文站 site/en/ 138 页已全量英文化。

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
│   ├── data/              # 可视化页（87 个 HTML，D3/Three）
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
├── skills/                # 项目级 playbook skill（17 个，见 §4.5）
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

1. **六文档同步**（核心 2 硬门禁：CHANGELOG.md + 交接文档.md 必须含当前 v/W；辅助 4 仅 WARN：README / STRUCTURE / 项目说明 / file-index）
2. **范围漂移检测**（html 最高 W ≤ 文档+归档最高 W）
3. **A4 计数一致（209 篇）** + **A1-A6 真实计数（611 篇）**
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
16. **Skills 索引一致性**（check_skills_index.py，W498 转正：skills/ 目录数 == README 索引数 + 目录短名 ⊆ AGENTS §4.5 + skills/ 全部文件 git tracked（防 day-review 式建了未入库）+ frontmatter name == 目录名；配套本地工具 scripts/sync_skills.py --sync 仓库→全局）
17. **索引健康**（check_index_health.py，W500 转正：file-index 段完整性/唯一性/最新段残留（豁免 W449-W463 损坏区·仅防新增）+ 方法论 README 双向覆盖（目录 md ↔ 索引链接·待创建占位 0）+ CHANGELOG 编号规则段上限 == 最新 W 段 + 治理文档引用一致性（文档规范.md scripts 引用存在性·verify 挂载脚本存在性））
18. **元信息块 v2**（check_frontmatter.py，W501 挂载：内容可信度轨——新文件（不在基线清单内）必须含血缘 + 核验状态 4 字段：生成来源（skill@commit 或 人工撰写）/生成模型（含「未记录」合法·禁编造）/生成日期 YYYY-MM-DD/核验状态三值枚举；基线 frontmatter-baseline.txt 冻结存量 611 篇豁免；口径见文档规范 §4.6）
19. **术语一致性**（check_glossary.py，W502 挂载：术语表↔dataset/glossary.json 双向同步（--generate 解析生成·禁手改）+ 人物称谓组规范词锚定（传递归一 圣僧→唐僧→玄奘·复合词掩码 心猿意马/金公木母黄婆）；基线 glossary-baseline.txt 冻结存量 303 篇 383 条豁免·只拦新增；口径见文档规范 §4.7）
20. **原著引文硬验证**（check_citations.py，W503 挂载：`> 原文引文（第N回）：“…”` 行必须对 dataset/text-search.json 去空白归一后精确子串命中·防 AI 幻觉引文；--dir docs 全量·任何未命中 = FAIL·存量引文行 = 0 无豁免；语法见文档规范 §4.8）

### 4.3 脚本工具链要点

- **改任何内联脚本后，必须重跑 `python scripts/generate_csp.py`**——否则 CSP sha256 哈希失配，整个内联脚本被浏览器拒执行（症状：无 pageerror 但内容空白、`window.__data` 未设置）。
- **批量正则改 CSS/JS 后必须验证括号/引号平衡**（`check_structure.py` / `_find_css_breaks.py`）。
- **CHANGELOG/方案档验收数字必须当批现测**（W496 铁律）：写 M 指标/内联字节数等数字前先跑 `python scripts/acceptance_snapshot.py` 从输出抄，禁止从上一批 CHANGELOG 复制（W493「28385B」跨批复制曾掩盖全站 INLINED 清空事故）。
- **bump_version.py** 一键补齐辅助 4 文档版本行；**两个已知坑（均多次复现）**：① 全局替换会污染 file-index 历史段；② `--desc` 会往 STRUCTURE.md 头部 / docs/00-导读/项目说明.md 的上一版本行**追加**「 + W46X(...)」而非替换主描述——跑完必须 Grep 校验这三处并手工净化。
- **CHANGELOG 多版段插入/重排只用脚本 + 结构断言**（锚点唯一性 + 版段 order 校验），手工 Edit 大段会吞相邻版段标题；**新批版本号先 Grep 现役段取 max+1 再写**（防撞号）。
- **批量改 md 一律 Python `open(encoding='utf-8')`，禁用 PowerShell `Set-Content`**（后者默认写 UTF-8 BOM，项目 W427 曾全库清 BOM；`Add-Content` 同理慎用）。
- **同文件多个 Edit 必须串行执行**（并行 Edit 基于同一原始内容计算 diff，后写覆盖先写——W505 复现 4 次：金角银角「唐僧肉」/CHANGELOG W506 段/项目说明头部/交接文档标题均丢失）；并行批次后必须 Grep 验证所有修改点。
- **写 `> 原文引文` 行前先跑 `python scripts/_cite_probe.py --kw <关键词> --chap <回目>`** 从 text-search.json 提取候选，禁止凭记忆编造（W503 门禁只拦截"写入后未命中"，无法拦截"恰好像原文的编造"）；新文档（非基线豁免）用变体称谓（行者/唐僧/圣僧等）必须同时含 canonical（孙悟空/玄奘），写作前 Grep `dataset/glossary.json` 称谓组。
- `_` 前缀脚本为一次性/诊断脚本，不入库门禁、不参与 CI。

### 4.4 Web Agent（xiyouji-agent-web/）

- 后端 `server/index.ts`（Express + SSE 流式 + SQLite `data/chat.db`），前端 `src/`（React18 + Vite5 + TDesign）。
- 凭证 `CODEBUDDY_API_KEY`（`.env`，由 `.env.example` 复制，已 gitignore）。
- 默认 `PROJECT_CWD=D:/1/xiyouji`；专属 Agent「渡口问津」内置项目 sysprompt；默认权限 `bypassPermissions`（可切回 `acceptEdits`/`default`）。
- 核心入口：`server/index.ts`、`src/hooks/useAgents.ts`（DEFAULT_AGENT）、`src/config.ts`（主题色 #c8463a「西」Logo）、`src/pages/ChatPage.tsx`。

### 4.5 项目级 Skills（skills/）

- 会话流程（4 个）：agent-session-loop（审查→收尾→沉淀 整合流水线）、deep-review-loop（DRL 5 轮审查）、mem-wrap-up（7 步收尾）、self-evolution（复盘沉淀）
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
node scripts/check_js_syntax.js          # 全站内联脚本语法
python scripts/check_structure.py        # 全站 CSS 结构平衡
python scripts/lint_links.py             # 死链 0 broken
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

*本文件由 AGENTS 通读项目后生成于 2026-08-16（v2.3.73 W458），2026-08-17（v2.3.78 W463）墨韵系列复盘增补动效契约（§1/§6-12/§8）与 W 批收尾坑（§4.3），2026-08-18（v2.3.80 W477）增补维护契约与文档治理段，2026-08-19（v2.3.83 W484）skills 治理：§4.5 补录 4 个会话流程 skill（共 14 个），2026-08-19（v2.3.84 W485）收录视觉/方案专项 3 skill（visual-batch / plan-authoring / plan-review，共 17 个），2026-08-19（v2.3.85 W486）四会话流程 skill 协议同步（verdict 7 词 / R0 4 件套 / 警报增强 / P2 残留 / work-log 路径 / 整合版协调），2026-08-19（v2.3.86 W487）四会话流程 skill 二轮同步（DRL 未安装降级声明 + experience-capture 格式规范 + 触发词扩充），2026-08-22（v2.3.93 W494）Phase E 收官同步：§4.2 补录 W493 转正三门禁（token 覆盖率 / 动效禁止清单 / a11y 对比度，现 14 条），2026-08-22（v2.3.94 W495）P0 热修复同步：§4.2 补录 INLINED CSS 完整性门禁（现 15 条），2026-08-22（v2.3.95 W496）优化收尾同步：§4.3 补录验收数字当批现测铁律（acceptance_snapshot.py），2026-08-24（v2.3.96 W497）skills 治理同步：§4.5 补录 day-review（流程类 4 个·共 18 个）+ 版本脚注，2026-08-24（v2.3.97 W498）防漂移门禁：§4.2 补录第 16 门禁 check_skills_index（Skills 索引一致性）+ §4.5 注明配套 sync_skills.py 同步工具，2026-08-24（v2.3.98 W499）GitHub 协作模板 + 创意方法论沉淀批次：无 § 结构性变更（.github issue/PR 模板 + 创意方法论 2 篇 + character-content 创意方法引用 + 方法论 README 索引修复 + file-index 结构注记），仅版本脚注同步，2026-08-24（v2.3.99 W500）索引健康门禁：§4.2 补录第 17 门禁 check_index_health（file-index 段完整性/方法论 README 覆盖/编号上限·豁免 W449-W463 损坏区），2026-08-24（v2.3.100 W501）内容可信度轨启动：§4.2 补录第 18 门禁 check_frontmatter（元信息块 v2·新文件血缘+核验状态 4 字段·基线豁免 611 篇·口径文档规范 §4.6），2026-08-24（v2.3.101 W502）术语一致性门禁：§4.2 补录第 19 门禁 check_glossary（术语库类型化·称谓组规范词锚定·基线豁免 303 篇 383 条·口径文档规范 §4.7），2026-08-24（v2.3.102 W503）原著引文硬验证：§4.2 补录第 20 门禁 check_citations（引文行对 text-search.json 精确命中·防 AI 幻觉引文·口径文档规范 §4.8），2026-08-25（v2.3.103 W504）存量核验状态基线：无 § 结构性变更（611 篇核验状态全覆盖 + 学术轨 105 篇 A+ 引文核验·content-trust-report 产出），仅版本脚注同步，2026-08-25（v2.3.104 W505）创意流程闭环落地：无 § 结构性变更（character-content 新增创意三明治管线章节 + 4 篇试点方向二深化），仅版本脚注同步，2026-08-25（v2.3.105 W506）处置遗留：无 § 结构性变更（删除失锚测试 test_fix_svg_negative_widths.py），仅版本脚注同步，2026-08-25（v2.3.106 W507）复盘沉淀落地：无 § 结构性变更（引文探针 _cite_probe.py 永久化 + day-review 归档查测试规则），仅版本脚注同步，2026-08-25（v2.3.107 W508）复盘剩余项收口：无 § 结构性变更（creative-methods 方法四去重指向 SKILL 管线章节 + _check_pipeline_consistency.py 管线一致性轻量校验），仅版本脚注同步，2026-08-25（v2.3.108 W509）经验上移共享：§4.3 工具链新增 3 条强制规则（Set-Content BOM 禁 / 同文件 Edit 串行 / 引文探针+canonical 预查）+ §6 铁律新增第 13 条内容可信度轨，2026-08-25（v2.3.109 W510）治理文档修复：无 § 结构性变更（文档规范 §8 门禁数 17→20 + §11.4 核心口径统一），仅版本脚注同步，2026-08-25（v2.3.110 W511）治理文档健康指标归档：无 § 结构性变更（CHANGELOG/file-index/交接文档概要 三档瘦身·W417-W464 段归档），仅版本脚注同步。如与上述权威文档冲突，以权威文档为准。*
