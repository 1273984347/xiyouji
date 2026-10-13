# 全面对抗性审查 · 整合总报告（2026-08-11）

> **整合来源**（3 份子报告）：
> 1. `adversarial-review-2026-08-11.md` —— 文档层审查（E1 铁律：声明 ≠ 落地）
> 2. `adversarial-review-deepdive-2026-08-11.md` —— 全量深挖（可视化/脚本/CI/英文站/安全/内容）
> 3. `content-quality-5classes-2026-08-11.md` —— 5 类内容质量抽样（A1/A2/A4/A5/A6）
> （注：上述 3 份子报告为工作底稿，内容已并入本整合稿，未单独留存为文件——2026-08-13 复盘批次标注）
>
> **关联报告（未并入全文，单独成篇）**：
> - `agent-web-security-2026-08-11.md` —— ①「渡口问津」Web Agent 安全审查
> - `viz-triage-2026-08-11.md` + `screenshots/viz/*.png` —— ③ 可视化正确性截图核验（进行中）
> （注：`viz-triage-2026-08-11.md` 与截图底稿未单独留存，核验结论已并入 §12/§13——2026-08-13 复盘批次标注）
>
> **方法论**：E1 铁律——凡文档声称的事实，一律 `ls`/实际运行/计数核验；凡门禁声称"全绿"，一律实际跑一遍。本报告只"找问题 + 量化证据"，未改动任何文件。
>
> **编号约定**：因两份子报告各自使用了 `P0-1/P0-2` 指向不同问题，本整合稿**统一重编号**（P0-1~P0-4 为 P0 级，P1-x / P2-x 按域细分），并在 §12 保留"撤回/更正"原始记录。
>
> **HEAD**：`dc292c9` v2.3.38 **W423**（已 commit，**未 push**）。

---

## 1. 项目认知摘要

- **性质**：一源多形数字人文项目《详解西游记》，纯静态站点（`file://` 可双击打开）+ RAG 后端 + Web Agent「渡口问津」。
- **规模（已核验）**：A1-A6 内容文档 **611 篇**（100+44+211+209+34+13，各板块恰 1 个 README.md 已剔除）；`site/data/` 可视化页 **86 个**；`docs/` 实际 **18 个子目录**。
- **协作模式**：多 session / 多 Agent，靠"六文档同步 + 双索引 + pre-commit 门禁（verify_delivery.py）"维持跨 session 连续性；沉淀大量"铁律/反模式"方法论。

---

## 2. 发现总览矩阵（统一编号）

| 级 | 域 | 发现 | 证据 |
|----|----|------|------|
| **P0** | 数据完整性 | A4 计数门禁"假绿"（断言 201，实际 209） | verify_delivery.py:50；实际计数 209 |
| **P0** | 接手陷阱 | 记忆系统路径全面失效（指向不存在的 `.trae-cn/`） | 文档规范.md:198；`ls` 实测 not found |
| **P0** | 部署/CI | security.yml E8-4 门禁永久失败（永远红 + 真实依赖零覆盖） | security.yml:130-144；security_scan.py:453 |
| **P0** | 部署 | 2 个 Three.js 3D 页脚本顺序 bug 线上真坏 | character-relationship-3d main() 早于 defer THREE |
| **P1** | 一致性 | v2.3.38 日期两值（08-10 / 08-11） | README:5 vs CHANGELOG:11 |
| **P1** | 一致性 | 当前 W 编号同文件自相矛盾（W422/W423） | 交接文档.md:96 vs :564 vs :353 |
| **P1** | 一致性 | 旁文档 4 份全部滞后 W422 | 项目概览/认知总览/交接参考手册 |
| **P1** | 一致性 | README 目录树严重过时（"十大板块"实为 18 目录） | README.md:90-116 |
| **P1** | 安全 | CSP 在 GitHub Pages 实际不存在（false-green） | security-report CSP-001=158；Pages 不消费 `_headers` |
| **P1** | 英文站 | `site/en/journey-geo-semiotics.html` 整页系统化损坏 | :4-9, :702-794 `Ch.` 注入 |
| **P1** | 英文站 | `site/en/chapters-map.html` 未译（CJK 主导） | 语言比 1.51 |
| **P1** | 供应链 | 96 处 CDN 脚本无 SRI | grep d3js.org=94；SRI-001/002=95+95 |
| **P2** | 工具漂移 | TodoWrite 引用失效（应为 TaskCreate 系列） | 文档规范.md:208/213 |
| **P2** | 工具漂移 | 三 skill 闭环路径指向 Trae（WorkBuddy 路径失效） | 交接文档.md:296-298 |
| **P2** | 文档 | 新Agent启动Prompt.md 滞后 W419 | 未涵盖 W420-W423 |
| **P2** | 安全工具 | API-004 "2 findings" 系扫描器自匹配假阳性 | grep verify=False 仅现于规则文本 |
| **P2** | 版本工具 | bump_version 不更新权威版本锚点 | bump_version.py:176 |
| **P2** | 脚本 | w286 SD 误映射兜底（SD号≠回号） | w286:143-150 |
| **P2** | 链接工具 | lint_links 根绝对路径误判 broken | lint_links.py:118-132 |
| **P2** | 脚本 | w286 硬编码绝对路径 `d:\1\xiyouji` | w286_merge_yuanwen_shendu.py:19 |
| **P2** | 脚本 | 依赖漂移：bs4/yaml/playwright 被 import 但不在 requirements.txt | 3 文件 / drl_spotcheck / perf_monitor |
| **P2** | 脚本 | w102 cwd 相对 sys.path，换目录即崩 | w102_check_sanzang.py:2 |
| **P2** | 脚本 | 62 处 `except Exception` 静默吞错 | lint_links/verify_delivery/bump_version |
| **P3** | 战略 | 真实读者量验证未决（卡 GoatCounter/Netlify） | 交接文档:344 |
| **P3** | 战略 | CSP 仍含 unsafe-inline 待部署切换 | 交接文档:345 |
| **P3** | 发布 | W423 已 commit 未 push | git log origin/main..HEAD |

---

## 3. P0 级发现（数据完整性假绿 / 接手陷阱 / 部署实质缺陷）

### P0-1 · A4 计数门禁"假绿"：verify 断言 201 篇，实际 209 篇
- `scripts/verify_delivery.py:50` → `EXPECT_A4 = "201 篇"`。
- 实际计数：`docs/03-主题与情节专题/` = 210 个 `.md` − 1 个 `README.md` = **209 篇内容**。
- 同一次运行：`OK  A1-A6 真实文件计数 611 篇 == README 声明 611 篇` → 611−(100+44+211+34+13) = **209**，数学强制 A4=209。
- `README.md:5` 同一行既写"共 611 篇"（需 A4=209）又写"（A4 W342 gap-fill 199→201 篇 已含）"（称 A4=201）→ 自相矛盾。
- 矛盾矩阵：称 "201 篇" = README/STRUCTURE/项目说明/文档规范/交接文档/verify；称 "209 篇" = 交接文档:115,147,366 / 项目交接参考手册 / CHANGELOG-ARCHIVE(W417) / file-index-archive(W400 "A4 201→209")。
- **影响**：项目自诩反"假收敛"的旗舰门禁，反而自己"声明 ≠ 落地"——用**字符串存在性**掩盖真实计数漂移（201 是 W342 冻结值，后被涨到 209，但 `EXPECT_A4` 字面量与四文档 parenthetical 从未更新）。新 Agent 若只跑 verify 会误信 A4=201。
- **修复**：`EXPECT_A4` → `"209 篇"`（或改动态读取实际计数），统一四文档 parenthetical。

### P0-2 · 记忆系统路径全面失效（新 Agent 接手陷阱）
- `文档规范.md:198`、`新Agent启动Prompt.md:39`、`交接文档.md:259/538/540` 要求改/查 `user_profile.md` / `project_memory.md` / `work-log.md` / `topics.md` / `retrospective.md` 与 `C:\Users\12739\.trae-cn\memory\`。
- 实测：这些文件在仓库根与 `.trae-cn/` 均 **not found**。
- 当前真实记忆系统：`C:\Users\12739\.workbuddy\MEMORY.md` + `D:\1\xiyouji\.workbuddy\memory\`。
- **影响**：E1 铁律"memory spot-check"让新 Agent 查**不存在的文件** → 误判 memory 缺失，或在仓库根新建 `user_profile.md` **污染 repo**；§11.2 把"user_profile.md"列为禁改项，但该对象根本不存在。
- **修复**：所有 memory 引用改为 WorkBuddy 实际路径；`.trae-cn/` 标注"历史(Trae)遗留，已废弃"。

### P0-3 · security.yml E8-4 安全门禁永久失败（永远红 + 真实依赖零覆盖）
- `security_scan.py --all` 对**本地 Python 环境**跑 `pip-audit`，把环境依赖漏洞计入 `DEP-001`（high）。本次 high=103，**全部是 `(environment)`**（gradio/keras/cryptography/bleach…），非仓库 `requirements.txt` 钉版依赖。
- 因 high>0，脚本退出码 **1** → `security.yml` E8-4（:130-144）对每个 push 都红 → 门禁失效/纯噪音；一旦启用分支保护，全部合并被挡。
- **根因（已核实源码）**：`security_scan.py:453` `_find_requirements_files()` 用 `ROOT.glob("requirements*.txt")` **非递归**扫描，`ROOT = 项目根`（:37），真实钉版在 `scripts/requirements.txt`（一级子目录）→ **抓不到** → 回退 `_run_audit_on_environment()`（:421）扫**当前 Python 环境**。故 103 个 `(environment)` high 全来自环境包，项目**真实依赖从未被审计**——门禁既永久红、又对真实依赖零覆盖（假绿）。`E8-2` 的 `pip-audit -r scripts/requirements.txt --strict` 才是正确的依赖审计路径。
- **修复**：E8-4 仅统计仓库 `requirements.txt` 的 pip-audit（复用 E8-2），或将 `DEP-001` 降为不阻断。

### P0-4 · 2 个 Three.js 3D 页脚本顺序 bug（线上真坏）
虽 P0-1（34+页空白）整体误判，运行时审计仍暴露**一个真实缺陷**：`character-relationship-3d.html` 与 `character-relationship-3d-view.html` 在**任何浏览器**都只显示"Three.js 加载失败，请检查网络。"而非 3D 图。
- `:8-9`：d3 / three 均为 `<script **defer** src=...>`。
- `:819-1262`：主初始化脚本是**普通 `<script>`（无 defer）**，解析到此处**立即执行**；`:1261` 调 `main()`。
- `main()`（`:1250-1258`）：`if (typeof THREE !== "undefined") { init3D(); } else { 显示"Three.js 加载失败" }`。
- 问题：`:1261` 的 `main()` 在**解析期**执行，此时 defer 的 three **尚未加载** → `typeof THREE === undefined` → 永远走 else 分支 → canvas 永不创建。
- 运行时审计（http 模式）：两页 `canvas=0, svg=0, pageError=[]`（静默降级），与静态代码一致。cdnjs 在沙箱可达（curl 200），排除"CDN 不可达"。
- **后果**：2 个旗舰 3D 可视化线上不可用（优雅降级，不崩站）。
- **修复**：主初始化 `<script>`（`:819`）也加 `defer`，或把 `main()` 调用改为 `window.addEventListener('load', main)`。

> ⚠️ **已撤回（误判·运行时证伪）**：初版"P0-1 · 34+ 可视化页线上空白"不成立。装 chromium 后跑 `_p1_viz_audit_http.js`（本地 HTTP 服务根 `site/`，`fetch('../../scripts/output/data/*.json')` 解析到 `/scripts/...` **404**，精确复现 GitHub Pages；CDN 走 https）审计**全部 86 页：86/86 渲染，0 空白、0 溢出、0 pageError**。初判"无回退"用的正则 `EMBEDDED_DATA|const data=|var data=|let data=` 过窄——9 个以为"必空白"的页实际用 `const EMBEDDED = {...}`（无 `_DATA` 后缀）内联；`loadJson()` 是"fetch 优先、EMBEDDED 回退"，file:// 与 Pages 下 fetch 失败均自动回退 → 渲染正常。站点 fetch+EMBEDDED 回退模式健壮。详见 §12。

---

## 4. P1 级发现（一致性 / 安全 / 英文站 / 供应链）

### P1-1 · v2.3.38 日期两值
`README.md:5`、`docs/00-导读/项目说明.md:5` 写 **2026-08-10**；`CHANGELOG.md:11`、`STRUCTURE.md:4` 写 **2026-08-11**。verify 只校验版本字符串存在，不校验日期 → 又一处假绿。

### P1-2 · 当前 W 编号自相矛盾（同一文件内）
`交接文档.md:96`："W### 已用到 **W423** … 下一 **W424**"；`:564`："当前 **W422** · 下一 **W423**"；`:353`（§五 索引）："README.md … 当前版本 **v2.3.37**"（实际 v2.3.38）。

### P1-3 · 旁文档 4 份全部滞后 W422
`项目概览.md:3/100`、`项目认知总览.md:4/80`、`项目交接参考手册.md:4` 仍写 "HEAD = **v2.3.37 · W422**（2026-08-10）· 下一 W423"。违反 §11.4 第 8 项（里程碑须同步旁文档 4 份）。W423 完成但未 bump 这 4 份。

### P1-4 · README 目录树严重过时（"十大板块"实为 18 目录）
`README.md:90-116` 仅列 `docs/` 00-10（还称"十大板块"，实际列了 11 个），漏列：`S2-外部分享` / `S2-学术投稿` / `S3-方法论外部分享` / `S4-学术投稿` / `superpowers` / `_dev` / `_templates`（共 7 个）。命名混乱：`S2-外部分享` 与 `S2-学术投稿` 两个不同后缀目录并存。

### P1-5 · CSP 在 GitHub Pages 实际不存在（false-green）
安全扫描 `HDR-001=0` 声称 `site/_headers` 含 5 安全头 → 但 **GitHub Pages 不消费 `_headers`**。同时 `CSP-001=158`：158 个 HTML 页面**无 meta CSP** 声明。结论：线上**零 CSP**。XSS-001 仍标 156 处 `innerHTML`（可视化页已路径降级为 medium，但无 CSP 兜底）。**修复**：在 HTML `<head>` 注入 `<meta http-equiv="Content-Security-Policy" ...>`，或迁移到消费 `_headers` 的平台（Netlify/Cloudflare）。

### P1-6 · 单页系统化损坏：`site/en/journey-geo-semiotics.html`
整页（含内联 CSS）被 `Ch.` 注入腐蚀，模式"**非数字后的数字前插 `Ch.`**"：
```
:4   <meta charset="UTF-Ch.8">                         (应 UTF-8)
:5   initial-scale=Ch.1.Ch.0                           (应 1.0)
:6   content="#FAFCh.7FCh.0"                           (应 #FAF7F0)
:8   https://dCh.3js.org/dCh.3.vCh.7.min.js            (应 d3js.org/d3.v7.min.js)
:9   color:#CCh.8463A;padding:Ch.12px                  (应 #C8463A;12px)
:702-794  全部 CSS 数值腐蚀：Ch.1px / Ch.0.Ch.85rem / #fCh.5eCh.9dCh.4 / rgba(Ch.0,Ch.0,Ch.0,Ch.0.Ch.25)
```
CN 版同位置干净。→ D3 加载失败 + 布局全崩，**该 EN 页完全不可用**。污染集中在**唯一** EN 文件；其余 EN 页的 `Ch.41`/`Ch.27` 是合法"Chapter"缩写，非污染。**根因**：翻译/文本变换管线对该模式无防护。**修复**：用 CN 版重新生成该 EN 页；审查翻译管线对"数字/十六进制/URL"的防护。

### P1-7 · EN 翻译缺口：`site/en/chapters-map.html`
语言比扫描（CJK/Latin）：65 个 EN 页中 **64 个比 ≤0.21（英文到位）**，唯独 `chapters-map.html` 比 **1.51**（CJK=3041 / LAT=2019）→ 正文未译，CJK 主导。属英文站英文化长期任务的遗留缺口。

### P1-8 · CDN 依赖无 SRI（供应链风险）
`grep d3js.org` = **94** 处；`cdnjs.cloudflare.com` = 2 处。全部外部 `<script>` **缺 `integrity` + `crossorigin`**（SRI-001=95 / SRI-002=95）。线上运行时**强依赖 d3js.org 可用性**；无 SRI 则 CDN 被篡改无校验。**修复**：把 d3/three vendored 到 `site/static/`（顺带消除外部运行时依赖），或补 SRI + crossorigin。

---

## 5. P2 级发现（工具漂移 / 安全工具 / 脚本缺陷）

### P2-1 · TodoWrite 引用失效
`文档规范.md:208/213`、`新Agent启动Prompt.md:37` 要求"TodoWrite 逐项勾选"。TodoWrite 是 Claude Code 工具，WorkBuddy 用 TaskCreate/TaskList/TaskUpdate。

### P2-2 · 三 skill 闭环路径指向 Trae
`交接文档.md:296-298`、`项目交接参考手册.md:178`、`docs/10-方法论沉淀/三skill闭环.md` 等指向 `C:\Users\12739\.trae-cn\skills\...`。WorkBuddy skills 在 `~/.workbuddy/skills/`，路径失效。

### P2-3 · 新Agent启动Prompt.md 本身滞后
创建/更新止于 W419（2026-08-10），未涵盖 W420-W423 关键变更（verify 4 新门禁、perf 预算收紧、CSP 仍含 unsafe-inline 待办）。虽声明"以交接文档为准"，但其"配套/更新"段会误导新 Agent 低估近 4 个版本的治理成果与遗留项。

### P2-4 · 安全扫描器自匹配（API-004 假阳性）
报告 `API-004=2`，但全仓 grep `verify=False` **仅现于 `security_scan.py:12,101` 自身的规则文本**，项目代码无任何真实 `verify=False`。扫描器扫描了自身/报告文件 → 自匹配。

### P2-5 · bump_version 版本漂移陷阱
脚本同步 9 份辅助文档，但**明确不更新 `site/dukou-engine.html` 页脚**——而该页脚是 `verify_delivery` 的"当前版本"真值锚点（bump_version.py:176 提示需人工插入）。漏做即版本漂移。→ 建议把页脚纳入脚本或加校验。

### P2-6 · w286 SD 误映射兜底
无元数据注释的 SD 文件按 `SD(\d+)` 名直接映射到同名回号（w286:143-150）。但 W419 已确认 SD 编号≠真实回号（SD101/102/103 对应 56/99 回等）。重跑会误合并。→ 移除兜底或强制元数据。

### P2-7 · lint_links 根绝对路径误判
`check_internal`（lint_links.py:118-132）对 `/data/foo.html` 类根绝对路径按本地文件系统解析 → 误报 broken；若站点用根绝对路径则死链审计失真。→ 识别根绝对路径并按站点根解析。

### P2-8 · scripts 硬编码绝对路径（w286）
`scripts/w286_merge_yuanwen_shendu.py:19` `WORKSPACE = Path(r"d:\1\xiyouji")` 硬编码开发者绝对路径。换机器/移动仓库即崩溃。`bs4` 也在此文件 :17 被 import（见 P2-9）。

### P2-9 · 依赖漂移（requirements.txt 缺 3 个被真实 import 的包）
`scripts/requirements.txt` 仅含 jieba/Pillow/ruff/pytest（已钉死），但以下被真实 import：
- `bs4`（beautifulsoup4）：`optimize-html-size.py:42`、`w286_fix_ch69_99.py:12`、`w286_merge_yuanwen_shendu.py:17` → 干净环境 ImportError。
- `yaml`（PyYAML）：`drl_spotcheck.py:70` → 干净环境 ImportError。
- `playwright`（Python 包）：`perf_monitor.py:131` → 干净环境 ImportError（`package.json` 仅覆盖 JS 版 playwright）。
**影响**：CI/新环境跑这些脚本必失败。建议把 beautifulsoup4 / PyYAML / playwright 加入 requirements.txt。

### P2-10 · w102 cwd 相对 sys.path
`scripts/audit/archive/w102_check_sanzang.py:2` `sys.path.insert(0,'scripts')` 是 cwd 相对路径，且仅当 cwd==仓库根时 `from B_人物.character_nlp import ...`（B_人物 无 `__init__.py`，靠 namespace package）才成立。换目录运行即 ModuleNotFoundError。脆弱但不算硬崩。

### P2-11 · 62 处 `except Exception` 静默吞错
`lint_links.py:129/143/178/196/253/263/310`、`verify_delivery.py:83`、`bump_version.py:52` 等。审计/校验类脚本吞错可能把"失败"误报为"通过"（如 lint_links 读取异常只 `continue` 跳过该文件）。建议至少记录告警而非静默。

> 注：`scripts/` 安全专项（已核验阴性）：无真实 `eval`/`exec`/`os.system`/命令注入点，无硬编码密钥，无裸 `except`，`FIXME=0`，`py_compile` 全过（130 .py 0 失败）、`node --check` 全过（34 自定义 .js 0 失败）。

---

## 6. P3 级发现（战略 / 发布待办）

### P3-1 · 真实读者量验证未决
整个"有流量继续分发 / 无流量停内容"策略卡在这，至今无真实跨访客数据（依赖 GoatCounter / Netlify 部署）。

### P3-2 · CSP 仍含 unsafe-inline
GitHub Pages 不消费 `_headers`，`script-src` 去 `unsafe-inline` 待部署平台切换。已知开放安全项。

### P3-3 · W423 已 commit 未 push
`git log origin/main..HEAD` = `dc292c9` 未推送。交付未完成；对 W423 的 CI/Security/Deploy/Screenshot/Lighthouse"全绿"**尚未发生**（文档对 W423 状态写"待测"，诚实，但 README/页脚已标 W423 为当前）。

---

## 7. 门禁有效性客观评估（合并）

| 门禁项 | 类型 | 本次实测 | 结论 |
|---|---|---|---|
| A1-A6 真实计数 611==611 | 真校验（读目录） | 通过 | ✅ 属实 |
| A1 导航相邻性 100/100 | 真校验（正则断言 N-1/N+1） | 通过 | ✅ 属实 |
| sitemap 154 页覆盖 | 真校验（walk vs loc） | 通过 | ✅ 属实 |
| site/data 86 页内嵌回退 | 真校验（正则） | 通过 | ✅ 属实 |
| 范围漂移（html 最高 W ≤ 文档最高 W） | 真校验 | 通过 | ✅ 属实 |
| **A4 "201 篇" 一致性** | **字符串存在性** | **通过（但值错）** | ❌ **假绿** |
| **版本日期正确性** | **未校验** | 不触发 | ❌ **假绿** |
| **security E8-4 DEP-001** | **扫错对象（环境）** | **永远红** | ❌ **假绿 + 永久红** |

---

## 8. 内容质量抽样（A1/A2/A4/A5/A6 五类）

> 方法：只读分析（脚本扫描 + 关键文件人工精读），未修改任何文件。每类按序号均匀散布抽样（A6=13、A5=30、其余 20–30 篇），覆盖首尾与中段。A3 人物深度分析另见 §9 深化。

### 8.1 目录定位（每类精确路径）

| 类 | 业务名 | 目录路径 | 实际文档数* | 背景宣称总数 |
|:---|:---|:---|:---:|:---:|
| A1 | 逐回精读 | `docs/01-全书逐回解读` | 100 | 100 |
| A2 | 随笔/杂谈 | `docs/06-个人随笔` | 44 | 44 |
| A4 | 主题 | `docs/03-主题与情节专题` | 209 | 209 |
| A5 | 文化 | `docs/04-文化与历史背景` | 34 | 35** |
| A6 | 诗词 | `docs/05-诗词歌赋` | 13 | 13/14** |

\* 实际文档数 = 目录下 `.md` 文件数 − 1（每目录含一个 `README.md`）。
\** 背景数含 README 故多 1；A5 实为 34 篇内容、A6 实为 13 篇内容。

### 8.2 是否存在"每类专属模板/SPEC"文件？
**结论：没有逐类专属模板文件。** 项目实际用于约束内容的规范分散在通用文件：`docs/_templates/article-template.md`（通用骨架：顶部 `> 元信息` + 六段式标题 + 双索引）、`_templates/handoff-checklist.md`（8 项自检 + 每目录写作风格）、`_templates/validation-checklist.md`、`docs/00-导读/文档规范.md`（元规则）、`docs/10-方法论沉淀/markdown写作规范.md`（写作反模式）、`docs/00-导读/项目说明.md`（双轨写作表）。
**关键发现**：`article-template.md` 的 `> 元信息` 区块 + 六段式标题 + 双索引，在 5 个内容类中**实际采用率为 0%**——线上内容用的是每类各自约定结构（A1 用 `<!-- chapter-meta -->` JSON + `> 轨标`；A4/A5 用 `> W###` 或 `> 轨标`）。即：**文档化的交付模板与线上内容实际结构严重脱节**（治理层发现，非内容质量问题）。

### 8.3 合规率（两层口径）

- **L1 规范贴合率**：对照 `article-template.md` / `handoff-checklist.md`（元信息块 + 双索引 + 六段式 + 无 TODO）。5 类全部 **0%**。
- **L2 内容质量率**：对照每类**实际使用**的结构与完整性（元数据区存在、无占位符、非残篇、相对链接有效、章节号一致）。这才是内容质量口径。

| 类 | 抽样/总数 | L2 内容质量率 | L1 规范贴合率 | 干净篇数 |
|:---|:---:|:---:|:---:|:---:|
| A1 逐回精读 | 30 / 100 | **96.7%** | 0% | 29/30 |
| A2 随笔 | 25 / 44 | **100%** | 0% | 25/25 |
| A4 主题 | 30 / 209 | **33.3%** | 0% | 10/30 |
| A5 文化 | 30 / 34 | **70.0%** | 0% | 21/30 |
| A6 诗词 | 13 / 13 | **92.3%** | 0% | 12/13 |

### 8.4 各类明细

- **A1（30/100，96.7%）**：占位符 1 篇（`第001回-灵根育孕源流出.md` 第 6 行"示例文本"样张字样）；2 篇标题置于元数据块之后（脚本误报，精读确认非缺陷）；相对链接 0 断链；章节号 30/30 命中。结论：最佳类之一。
- **A2（25/44，100%）**：占位符/残篇/断链/重复均 0。最干净类。
- **A4（30/209，33.3%）**：低率**主要由元数据可追溯性缺口驱动**，正文质量高。缺 `W###` 出处 ID（有 `轨标` 块但无 W 编号）18 篇（示例：八十一难结构学专题、反抗与束缚的永恒循环专题、取经团队决策论专题、名字的政治学专题、法宝系统专题、筋斗云专题…）；完全无元数据区 2 篇（`真假美猴王-二心之战.md`、`蟠桃园-体制内的秘密.md`）；占位符/残篇/断链 0。
- **A5（30/34，70.0%）**：缺 `W###` 出处 ID 9 篇（示例：佛道思想、历史玄奘与小说玄奘专题、成书背景、明代隐喻、版本演变、西游与禅宗公案专题…）；完全无元数据区 0；占位符/残篇/断链/重复 0。
- **A6（13/13，92.3%）**：占位符 1 篇（`主题诗词创作.md` 第 17 行 `**主题**：XXX` 未填）；缺 ID/断链/残篇 0。

### 8.5 跨类共性结论
1. **规范贴合（L1）全面 0%**：建议将内容实际结构回填进模板与门禁，或在文档规范中明确承认内容类豁免六段式骨架。
2. **占位符残留**：A1（示例文本）、A6（XXX）各 1 篇，易修。
3. **元数据可追溯性缺口**（最大系统性风险）：A4（~67%）+ A5（~30%）部分文档缺 `W###` 出处 ID，影响 `file-index.md` 双向索引与 CHANGELOG 追溯。
4. **相对链接健康**：5 类抽样 0 断链。
5. **事实一致性（抽查）**：A1 章节号 30/30 命中；精读 A4 `不可靠叙述专题`、A5 `佛道思想` 等未发现明显内矛盾。

### 8.6 五类修复优先级

| 优先级 | 项 | 影响类 |
|:---:|:---|:---|
| 高 | 补 `W###` 出处 ID（A4 18 + A5 9 + A4 2 全缺） | A4、A5 |
| 中 | 清理遗留占位符（示例文本 / XXX） | A1、A6 |
| 低 | 统一标题位置（A1 个别标题置于元数据块后） | A1 |
| 治理 | 对齐"实际结构"与"文档化模板"，消除规范脱节 | 全部 |

---

## 9. A3 人物（A4 主题之外）模板合规深化

> 来自深挖报告 A3 抽样（agent 执行），定位与 §8 不同：此处"A4"指**人物深度分析**（docs/02-人物深度分析/，211 篇），与 §8 的"A4 主题"命名撞字但为不同类。

- **未发现 A4 人物"七段模板"独立 spec**；基础人物为 **de-facto 七段**（顶部 blockquote 元信息 + 一~六 + footer 双索引）。
- 目录分四套模板家族：基础 41 / 外传 78 / 方向二深化 47 / 深化专题 30 / 其他 23。
- **抽样 30 篇基础人物：30/30 含一~六且顺序正确 ≈100%，元信息 41/41，空段 0** → 结构合规率高，质量良好。
- **主要问题（非阻塞）**：footer 收尾两派并存（31 篇 `> 导航` vs 5 篇 `## 双索引` 等；另有 5 篇以 `> Preflight 三轨验证`/`## 关联人物` 收尾）；**A1 逐回解读超链接 0/41 缺失**（导航仅指向人物谱系表 + A4 主题专题，无 A1 回目超链接）；缺显式七段 spec。
- **结论**：七段模板仅约束 41 篇基础人物（合规 ≈100%）；其余 170 篇分属外传/方向二/九段式深化/合集等合法模板，不宜以七段单一标准衡量。建议把基础七段写入显式 spec，统一 footer 为 `## 双索引`（含 CHANGELOG + file-index + A1 反链）。

---

## 10. 关联报告摘要：①「渡口问津」Web Agent 安全审查

> 完整报告见 `agent-web-security-2026-08-11.md`（未并入本整合稿）。

**总体结论**：本地开发/单人使用安全；**不建议公网/局域网无防护暴露**。已含多项前序"P0-1/P0-2"修复，水位高于典型玩具项目。未发现硬编码真实密钥、命令注入或 SQL 注入。10 项发现：
1. 硬编码密钥 P3（无真实 KEY，仅 `.env.example` 占位符；check-login 已脱敏）
2. AGENT_WEB_TOKEN 认证 **P1（默认关闭）**——未设 token 时 `/api/*` 免认证；但服务仅绑 127.0.0.1（index.ts:761），本地可接受
3. 路径穿越 P2（resolveWorkingDir :73-79 startsWith 校验已缓解；Windows 8.3 理论残留，且无文件读取 API）
4. 命令/代码注入 P2（应用自身无 eval/exec/child_process；唯一来源 SDK Bash 工具，经 canUseTool 权限确认链路 :537-589，默认不直接放行）
5. 提示注入 P2（message 直送 Agent，systemPrompt 可由请求体覆盖 :599；受 cwd+权限确认约束，无法逃逸取密钥）
6. CORS P3（无 cors 中间件=默认拒绝，安全）
7. **bypassPermissions P1（默认关闭）**——ALLOW_BYPASS 需显式=1，sanitizePermissionMode 拒绝白名单外值；若开启=PROJECT_CWD 内实质 RCE
8. 依赖 P3（lockfile 解析版本均较新；无法离线 npm audit，仅 @tdesign-react/aigc 为 alpha 需注意供应链）
9. SQLite P3（全部预处理语句+占位符，动态列名走代码内固定白名单，无注入）
10. XSS P3（用户消息 React 自动转义；助手消息经 DOMPurify.sanitize 后交 ChatMarkdown；全仓无 dangerouslySetInnerHTML/innerHTML）

**最高优先级**：任何暴露需求 → 开启 `AGENT_WEB_TOKEN` 并**保持 `AGENT_WEB_ALLOW_BYPASS` 关闭**；`PROJECT_CWD` 指向不含密钥、损坏后果可接受的副本。

---

## 11. 已验证干净 / 阴性（平衡结论）

- **站内死链**：site 2627 链接、docs 4860 链接，**全部 0 broken**（lint_links 内部模式；与 §8.5 五类抽样 0 断链一致）。
- **英文站整体**：64/65 页英文比 ≤0.21，翻译基本到位（仅 chapters-map 缺口 + journey-geo-semiotics 损坏）。
- **密钥泄漏**：无 `sk-`/AWS 密钥（SEC-005/003 干净，W411/W412 加固生效）。
- **Workflow 触发**：6 个 workflow 均有正确 `push: branches:[main]`（W422 修复落地，无"门禁从未运行"回归）。
- **JS 语法门禁**：86 页 + dashboard 全部通过 Node 语法检查（check_js_syntax.py --all）。
- **A1-A6 计数**：verify_delivery 611==611；A4 真实=209（文档层"EXPECT_A4=201 篇"为假绿，见 P0-1）。
- **scripts 安全**：无真实 eval/exec/命令注入、无硬编码密钥、0 编译错误。

---

## 12. 方法边界与更正（保留原始记录）

**更正 1（P2 仓库卫生假阳性，已撤回）**：初报称"`SECURITY-AUDIT-2026-08-09.7z` + `.password` 明文密码入库"。核实后更正：`.gitignore:109-110` 已忽略二者，且 `git ls-files` 确认**未跟踪**——非提交入仓。仅作本地工作区卫生提示。

**更正 2（Playwright 事实）**：初报称"Playwright 未装→只能静态分析"，实为 **Playwright 包已装（`scripts/node_modules`）但浏览器二进制缺失**。本次已尝试 `playwright install chromium`，因沙箱封锁 `ms-playwright/__dirlock` 的 trash 操作失败 → 改用 `PLAYWRIGHT_BROWSERS_PATH=scripts/.pw-browsers` 项目本地安装成功，runtime 审计得以执行。

**撤回（P0-1 旧编号 · 34+页空白）**：静态推断"34+ 页空白"不成立。装 chromium 后跑 `_p1_viz_audit_http.js`（复现 Pages 的 fetch→404）+ `_p1_viz_audit_local.js`（file://），**86/86 渲染，0 空白**——因漏看 `const EMBEDDED = {...}` 回退而误判。仅保留 P0-4（2 个 3D 页脚本顺序 bug）为真实残留缺陷。

**已补齐的核查**：
- workflow 实为 **5 个 YAML**（`README.md` 非 workflow），全部已读，无遗漏。
- EN 8 个高 `script_cjk` 脆弱页经签名扫描 **无 `Ch.` 类损坏**，仅 `journey-geo-semiotics` 单页损坏（P1-6）。

---

## 13. 优先级修复路线（合并两份建议）

**立即（建议 W424 顺带处置）**
1. `verify_delivery.py:50` `EXPECT_A4` → `"209 篇"`（或动态计数）；统一 README/STRUCTURE/项目说明/文档规范 四处 "199→201" parenthetical。（P0-1）
2. `README.md:5` / `项目说明.md:5` 日期 2026-08-10 → **2026-08-11**。（P1-1）
3. bump 旁文档 4 份到 v2.3.38 W423。（P1-3）
4. memory / skill 路径引用改为 WorkBuddy 实际路径，`.trae-cn/` 标注废弃。（P0-2 / P2-2）
5. 修 `character-relationship-3d*`（P0-4）与 `security.yml` E8-4（P0-3）。

**短期**
6. 重写 README 目录树到 18 目录；修正"S2-外部分享 / S2-学术投稿"命名。（P1-4）
7. 更新 `新Agent启动Prompt.md` 到 W423。（P2-3）
8. TodoWrite → TaskCreate 系列（全文档替换）。（P2-1）
9. CSP 注入 / 修复 journey-geo-semiotics 损坏页 / 补译 chapters-map / CDN-SRI 或 vendored。（P1-5/6/7/8）
10. security_scan.py:453 指向 `scripts/requirements.txt`；补 requirements.txt 缺的 bs4/yaml/playwright；w286 硬编码路径改相对；62 处静默 except 加告警。（P0-3 / P2-8/9/11）
11. bump_version 纳入页脚锚点；w286 去 SD 兜底；lint_links 根路径解析。（P2-5/6/7）

**战略 / 治理**
12. 推进真实读者量验证（GoatCounter / Netlify）。（P3-1）
13. 择机迁移消费 `_headers` 的平台去 unsafe-inline。（P3-2）
14. 推送 W423 完成交付闭环。（P3-3）
15. 补 A4/A5 的 `W###` 出处 ID；清理 A1/A6 占位符；对齐"实际结构"与"文档化模板"。（§8.6）
16. agent-web 暴露前开 `AGENT_WEB_TOKEN` 并保持 `AGENT_WEB_ALLOW_BYPASS` 关闭。（§10）
