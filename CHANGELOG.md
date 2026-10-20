# 更新日志


> **📖 阅读契约（W707）**：查表型——判断「当前版本/最近批次」时只读**顶段 1 个版本段**；查历史段用 grep（`grep -A 30 "### vX"`）；完整通读非预期用法（历史细节在 archive/docs/CHANGELOG-ARCHIVE*.md·grep 单段查勿打开通读）。
本项目所有重要变更均记录于此。格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/)。

## [Unreleased]

> **W### 编号规则**：每个版本段标注唯一 W### ID（W001-W814），v0.8 内部细分 W008.1-W008.7（B0-B7）。每个 W 附四件套字段（来源/文件/验证/状态）。反向索引见 [scripts/output/file-index.md](scripts/output/file-index.md)（给定文件查改几次）。
>
> **v/W 双键口径（W706）**：时间点查询以 W 号为准（单调键）；v 号在 W659-W667 合并段/并行批次区间不单调（v2.3.262〔W661〕列于 v2.3.261〔W666〕后）；v 号形态演化（阶段标签化·方案 D）经盘点 docs/superpowers/plans/2026-10-11-version-space-inventory.md 后另批实施。
>
> **方案 D 形态切换（W711 生效）**：自 W711 段起，CHANGELOG 段标题去 v 号（新形态 `### W###（日期）：标题`）；W001-W710 段保留 `### vX.Y.Z（日期）：W###` 历史形态不改写；v 号降格为阶段标签（v2.3·无 patch）；CITATION.cff version 改批次号形态（"W###"·CFF free string）；file-index 历史条目保留 v 引用、新增条目 W only。
>
> **历史版本归档**：v0.1 - v2.3.17（W001-W399）已迁移至 [archive/docs/CHANGELOG-ARCHIVE-tier2.md](archive/docs/CHANGELOG-ARCHIVE-tier2.md)（W513 二级归档）；W422 再归档 v2.3.18-v2.3.31（W400-W416）段；W511 归档 v2.3.32-v2.3.82（W417-W464）段 + v2.3.83（W484）段至 [CHANGELOG-ARCHIVE.md](archive/docs/CHANGELOG-ARCHIVE.md)。W681 归档 v2.3.84-v2.3.249（W485-W649）段至 [CHANGELOG-ARCHIVE.md](archive/docs/CHANGELOG-ARCHIVE.md)。W736 再归档 v2.3.250-v2.3.293（W650-W699）段至 [CHANGELOG-ARCHIVE.md](archive/docs/CHANGELOG-ARCHIVE.md)（源文件超 50KB/500 行阈值）。本文件仅保留 W700+ 段（W650-W710 段用历史 vX.Y.Z 形态·W711+ 段用批次键 W### 形态）。
>
> **全站页数口径**（W459 建·W702 实跑刷新，各门禁分母不同）：HTML 共 857<!--stats:html_total--> 页（site/data 88<!--stats:site_data_html--> + site/en 138<!--stats:site_en_html--> + site 根 9<!--stats:site_root_html--> + site/reader 622<!--stats:site_reader_html-->）；CSP 覆盖 856<!--stats:csp_covered--> 页（排除 `_template.html`）；check_js_syntax/check_structure 扫 855<!--stats:scan_files--> 文件（再排除 `_shell.html`）；check_seo_head 扫 855<!--stats:seo_scanned--> 页（site 全树减两个模板壳）；inline_css 同步 330<!--stats:inline_css_pages--> 页（site 全树含 INLINED 标记页）；「可视化页 87<!--stats:visualization_pages-->」= site/data 88 减 `_shell.html`。
>
> **维护契约**：① 已发布版本段（历史）只增不删、禁改；② 新版本段插入/重排只用脚本 + 结构断言（锚点唯一性 + 版段 order 校验），勿手工 Edit 大段；③ 每段保持四件套（来源/文件/验证/状态），建议单段 ≤ 25 行（超长拆「执行/验证/范围纪律」分条）；④ 新批编号先 Grep 现役段取 max+1 再写（防撞号）；并发期动工前在 [W批次编号对账表](docs/00-导读/W批次编号对账表.md) 登记认领（W663 起·版段递延时以对账表为准）。

### W814（2026-10-20）：去品牌扩展批（另两个同类品牌字面全量清除）

> **来源**：用户裁决「另两个同类品牌字面与首轮已禁品牌同类·同样禁止并全面修改」——承接 W812 去旧厂商 Agent 工具品牌化批，把另两个同类品牌字面一并纳入禁令并全仓清除。
> - **文件**：docs/00-导读/W批次编号对账表.md、CHANGELOG.md、HANDOVER.md、CLAUDE.md、.gitignore、xiyouji-agent-web/server/engine/tools.ts、scripts/output/file-index.md、scripts/output/_w814_spec.json。
> - **按语义分治而非一刀切**（承 W812 机制·保住多 Agent 可区分性）：认领会话列的会话标识 → 「并行 Agent 会话」（与既有的「DSH」「主会话」并列·不塌缩为单一标识·对账表认领行逐条可追）；生成模型署名 → 「GLM（本地 Agent 会话 …）」（与认领会话列区分·前者指模型运行环境·后者指批次执行方）；厂商品牌复合表述 → 「旧厂商 Agent 品牌」/「（含另一同类品牌）」；已退役的凭证变量名（该厂商前缀的一组环境变量·形如 `<厂商前缀>_API_KEY` / `_AUTH_TOKEN` / `_BASE_URL` / `_INTERNET_ENVIRONMENT` / 通配前缀形式）→ 「旧厂商_*」；已退役 CLI 的用户级路径 → 「.旧厂商目录」。
> - **特例逐条定稿（不机械替换）**：① 归档检测器脚本 `archive/scripts/batches/misc/_audit_agentweb_baseline.py` 的**搜索模式字面**是「检测残留品牌」这一工具功能本身（改掉即失去检测能力）→ 按 W812 先例登记豁免保留；② 行为性代码 `xiyouji-agent-web/server/engine/tools.ts` 的 `SKIP_DIRS` 含该品牌目录名（防目录遍历扫进本地工具目录）→ 改为中性目录名，防护功能保留；③ 本地索引配置文件（未跟踪·含品牌字面）→ 先把其 24 条独有忽略规则**并入 .gitignore**（功能不丢）再备份至项目外 TEMP 并移除项目内副本（对齐 W812 对同类本地配置的处理）；④ 与新裁决矛盾的**现役叙述**（W812 批摘要里「某品牌不在禁令范围故保留原名」一句）→ 按文档规范 §4.11「撤销=新批次裁决反转并引用原段·禁改历史段」，CHANGELOG 历史段不改（由本段承载裁决变更）·HANDOVER 现役叙述就地订正。
> - **两处工程教训（本批实战暴露）**：① **git grep 路径转义**——git 默认把非 ASCII 路径转义成八进制，拿这种串去 `os.path.isfile` 必然失败 → 中文路径目录（`archive/docs/复盘报告/` 等）被**静默跳过**，首轮施工的「残留复算 0」是假绿；改用 `-c core.quotePath=false` 取真实路径后复算才真实。② **残留复算口径**——只复算「自己改过的文件」会漏掉「根本没被改到的文件里的残留」；改为**全盘复算**（含未改动与未跟踪文件）后才发现 24 条 S4 投稿树本地线与构建产物（均未被 git 跟踪·不入公开仓·按 W812 验收口径豁免）。
> - **验收**：跟踪域内全仓该字面**命中 0**（含 archive/ 归档面·现役面·spec·索引载荷）；非跟踪域残留经逐条定性为本地线/构建产物/二进制（不入公开仓）；派生面同步重生成搜索索引（docs=726 pages_zh=96 pages_en=138·zh 256199 / en 276197·恰好 2 页变更）+ CSP 重算（2 页已更新·856 页 0 漂移）+ 第 46 槽 0 FAIL。

### W813（2026-10-20）：review 修复批（W806-W812 对抗审读三项实证缺陷）

> **来源**：用户令「review 一遍这几个批次」后追加裁决「按顺序开始」——本批为 W806-W812 七批对抗审读所得三项实证缺陷的修复批。审读范围为 W806（GoatCounter 退役）/ W807（索引刷新）/ W808（Web Agent 全栈加固）/ W809（索引新鲜度门禁）/ W810（死代码清理）/ W811（CI 断链修复）/ W812（去旧厂商 Agent 工具品牌化）共 23 提交（1012 文件·+7178/-2420）。
> - **文件**：xiyouji-agent-web/server/errors.ts、xiyouji-agent-web/server/api.integration.test.ts、tests/unit/test_ci_wiring.py、scripts/requirements.txt、scripts/check_doc_sync.py、docs/agent/gates.md、AGENTS.md、scripts/output/_w813_spec.json。
> - **P1 契约回归（畸形 JSON 从 400 变 500）**：W808 新增全局错误处理中间件 `server/errors.ts`，其 `toErrorResponse` 只认 `AppError`，而 `express.json()` 的请求体解析失败抛的是 `SyntaxError`（body-parser 附带 `status=400`）——这类**客户端错误**被归入「编程错误」分支，客户端收到 500 +「服务器内部错误」。重构前（无全局处理器）Express 默认处理器返 **400**，故 W808 在引入全局处理器的瞬间把一类客户端错误升格成了服务端故障，且违反该批自述的「对外契约零改动」红线。连带影响：前端 `errorMessage.ts` 的 `isRetryable` 对 5xx 判 true、对 4xx 判 false，于是「请求体畸形」被误判为可重试的服务端故障。**修复**：异常自带 4xx 状态码即按该状态码返回，文案用固定表（400/413/415），不回显原始解析消息（防细节外泄）；日志分支新增「框架层客户端错误」记 warn 不记堆栈。**验证**：新增两条集成测试（畸形 JSON 返 400 而非 500 + 错误体不含堆栈/异常类名/原始解析消息），集成套件 20 项全过。
> - **P2 门禁真空（文件清单防线对前端件失效）**：第 31 门禁 C4-f 的 token 正则 `RE_FILE_TOKEN` 只认 `.py/.js/.mjs/.md/.json/.cff/.txt/.html/.css/.xml/.yml`，`.ts/.tsx/.cjs/.jsonl/.yaml/.toml/.ini/.cfg/.sh/.ps1/.csv/.svg/.example` 全部被**静默滤除**——而滤除即「不被校验」。实测：W808 段「文件」行声明 34 项，C4-f 实际只认 **5 项**（丢弃 29 项·全是 .ts/.tsx），即「手工件漏 add」这条防线在 W808 这类前端批上等于不存在。负样本对照实证：同一漏 add 形态，`.py` 判红、`.ts` 只出 NOTE 放行。**修复**：扩展正则覆盖仓内实际存在且会被手工编辑的文本类扩展名（二进制资产如 .png/.woff2/.ttf 不列——「文件」行本就只登记手工编辑件），并补 T19/T20 两条自测用例（.ts 漏 add 必红 + 多扩展名覆盖面回归锁）。**验证**：自测 18→**20/20 通过**；新旧正则对照实证「旧放行、新判红」证明用例抓的是真缺陷而非自证。
> - **P3 CI 防线静默失效（守卫在 CI 侧形同虚设）**：W811 的工作流 YAML 可解析性守卫有三条判据——J1 无制表符、J2 裸标量值不得含 ": "、J3 PyYAML 全量解析。实证两处漏洞：① **J2 只查 `name` 键**，但 YAML 映射歧义对任意键成立（实测 `run:` / `env:` / `if:` 三种形态同样让 GitHub 报「workflow file issue」0 秒失败该 workflow 且 PR 不生成 check，原判据全部放行）；② **J3 在 CI 恒跳过**——原实现为「PyYAML 不可用即 `continue`」，而 CI 的 `pytest-unit` job 只装 `scripts/requirements.txt`（当时其中无 PyYAML），于是唯一能拦住这三种形态的判据在 CI 侧从未执行，缺陷照旧潜伏（本地有 PyYAML 故本地绿）。**修复**：J2 判据扩到**任意映射键**的裸标量值（引号包裹与块标量起始标记除外）；PyYAML 登记进 `scripts/requirements.txt`（`PyYAML==6.0.2`）使 J3 在 CI 恒生效，并把 J3 的 `ImportError` 分支从「静默跳过」改为「判红」（可选依赖缺失时不得假装通过）；另补守卫自身的负样本实证用例（4 种坏形态必红 + 4 种形态 PyYAML 同样解析失败证明非误报 + 合法形态不误杀 + PyYAML 确已登记的回归锁）。**验证**：守卫 12→**22 项全过**；新旧判据对照实证「旧判据放行 run/env/if 三种、新判据全部拦下」；本机 `pip-audit -r` 实测 `PyYAML==6.0.2` 「No known vulnerabilities found」（6.x 线已修全部 loader 类 CVE）。
> - **审读其余面结论（不修·留档）**：交付全量门禁 51 段 0 FAIL；三个新增守卫单测 22 passed；改动文件混行尾 0；W812 目标字面全仓实测 0 命中（site/ 内 10 处残留经逐条核验全是退役说明注释·无实质埋点或外域引用·守卫按「具体形态」判定成立）；W812 移除 `.gitignore` 中该厂商工具目录规则后无兜底（本地目录已迁出项目·实测 `Test-Path` 为 False·属可接受风险敞口·按禁令意图刻意）；`并行 Agent 会话` 字面 234 处属不在当时禁令范围的品牌（与 旧厂商 Agent 品牌 同类·按裁决保留原名·**W814 已按用户新裁决一并清除**）。
> - **机械扫（八面）**：行尾 0 混行尾 / 双写 0 / 豁免链连续 / 文件行覆盖度对账（各批 token 认定数逐批实测）/ 门禁复跑全绿 / 垃圾件 0 / 临时探针已清（review 用探针写在 `tmpe/` 且完工即删·不入库）。

### W812（2026-10-20）：去旧厂商 Agent 工具品牌化批（工具环境解耦 + 全仓去品牌 + 多 Agent 机制保全）

> **来源**：用户令「本项目所有内容禁止使用某已退役厂商 Agent 工具的一切，全部重新修改」+ 追加裁决「本项目是由多 Agent 协作构成，因此需要考虑协作机制和通信机制以及通用机制，不能只考虑单一 Agent」——本批据此做「工具环境解耦 + 全仓去品牌 + 多 Agent 机制保全」三层改造，**不止于删字面**：品牌字面若只做机械替换会把多 Agent 的身份区分抹平，故本批一律改用角色化中性标识（主会话/并行 Agent 会话/平台内建/运行时 automation），保住认领会话列与责任人列的可区分性。
> - **工具环境层解耦（本批的实质动作，不止是文案）**：① **提交门禁 hook 解释器去厂商托管运行时**——`.git/hooks/pre-commit` 原硬编码 `<厂商托管 Python 路径>`，该运行时随工具退役即整条交付链失效；改为**与仓内工具清单同口径**取全局 Python 3.12（AGENTS.md §4.3「本机环境事实」明文「不以各机 PATH 状态为依据」）：首选 `py -3`（Windows 启动器·跨 shell 一致·PATH 无关·实测能吃 git-bash 的 POSIX 路径），回退系统 Python 3.12 绝对路径，两者均须实测可运行（`-c "import sys"` 返回 0）才选用。**订正依据**：实测本机两 shell 解析不同——PowerShell 侧 `python`/`python3` 指向 `WindowsApps/python.exe` 应用执行存根（命令存在但调用即 exit 9009·无输出无报错），git-bash 侧 `python`/`python3` 才解析到 `C:\Users\12739\bin\` 下的实解释器；故**按 PATH 形状挑解释器不可靠**（上一版自造「python3 → python → 绝对路径」候选序列即因此被订正，改为直接取清单口径的全局 Python 3.12）；**清单自身亦同步订正**——AGENTS.md §4.3 两条改写为「**三语境分清**：仓内文档/工具表/CI/Makefile 用可移植形态 `python -m <工具>`（CI 跑 `ubuntu-latest`·`py` 非跨平台）·本机 PowerShell 侧用 `py -3 -m <工具>`（该侧 `python` 是应用执行存根 rc=9009）·本机 git-bash 侧 `python` 可用」+「hook 与本清单同口径·不按 PATH 形状挑选」，并把两 shell 解析差异这一机器事实补进清单（机器相关事实本就属该节·不留指旧条目）。**工具表与速查层同源补指针**——`scripts/README.md` 表头与 `CLAUDE.md`「环境注意」段各增一行「调用形态」指引（表内/块内的 `python …` 保持可移植形态不变·仅加指针说明本机 PowerShell 侧的写法差异）——不刷 30 余行调用形态本身，因那会令文档在 CI/Linux 上失效。**此条亦是本批的一次自我订正**：上一订正曾把 `py -3` 写成全仓统一约定，与仓内可移植形态相悖。② **`.gitignore` 去该工具目录忽略规则**（2 行）。③ **本地该工具目录整体迁出项目**（8 件 / 168526 字节 → 先备份至项目外 TEMP 再删·`Test-Path` 复核已删），使「项目内零该工具痕迹」为可验证事实而非声明。④ `AGENTS.md` §4.3「本机环境事实」同步改写（机器相关事实不留在指旧的条目里）。
> - **脚本层解耦**：`scripts/preflight_check.py` 去工作树态统计的厂商目录排除分支（3 处：docstring / 排除 if / 说明行）+ `scripts/gen_folder_docs.py` 排除目录元组去该项 + `scripts/archive_file.py` 引用扫描去 `--exclude-dir` 项；`tests/unit/test_preflight_check.py` 同步（用例改测三态计数本身·不再依赖厂商特例；认领会话样例去品牌）。**归档扫描脚本顺修一处定位缺陷**：`archive/scripts/_scan_sd_anchors.py` 与 `_scan_sd_misplace.py` 归档后目录加深致 `ROOT` 解析错位（原位 `scripts/` 下 → 现为 `archive/scripts/`，守卫根与 ROOT 一并上溯三级对齐项目根，使「path escapes project root」语义成立），报告落 `tmpe/_reports/`（项目工地·gitignore 覆盖·不入库）而非厂商工具目录。`archive/scripts/w334_font_subset.py` 去托管 venv 硬编码路径。
> - **文档层去品牌（37 文件 / 153 处 / 全仓命中归零）**：对账表认领会话列 23 行、CHANGELOG 现役与历史段、6 份方案/复盘报告、3 份归档方案档、2 份归档批 spec、2 份归档杂项报告、2 份 plans、2 份 T01 计划/报告、`tmpe/README.md`、2 份现役 spec、两个搜索页索引载荷。**替换口径按语义分治而非一刀切**：认领/负责人/责任人/执行者 → 「主会话」；并行执行语境 → 「并行 Agent 会话」；工具能力语境 → 「平台内建」「运行时 automation」「Agent skills」；厂商品牌复合表述（与其他同类品牌并列出现处）→ 「旧厂商 Agent 品牌」；本地工具目录/记忆载体路径 → 「本地工具目录」「会话级记忆库」。**旧厂商 Agent 品牌 不在本次禁令范围故保留原名**。**本批自身记录同样不得出现该字样**（否则验收项「全仓命中 0」自我否定）——故对账表认领行、CHANGELOG 段、提交信息一律改用「旧厂商 Agent 工具」等中性表述。
> - **派生面同步（不重生成即失配）**：① **搜索索引重生成**——文档内容变更使索引载荷陈旧（第 46 槽新鲜度门禁 fail-closed 必红），跑 `scripts/_gen_search_index.py` 实测 `docs=726 pages_zh=96 pages_en=138`·载荷字节 `zh 256184 / en 276182`（较前各 +2 字节）→ **恰好 2 页变更**；② **CSP 哈希重算**——内联常量变更后跑 `scripts/generate_csp.py` 实测「2 页已更新 · 共 856 页」，随后 `--check` 复核「漂移/缺失 0 页」；③ 第 46 槽复跑「0 FAIL（zh 822 条 · en 864 条 与生成器实算一致）」。
> - **多 Agent 机制保全（本批的硬约束，不因改造而破）**：① **协作机制**——touches 交集拒绝机制原样生效（本批认领行登记 37 项共享面·动工前 `preflight_check.py --touches <清单> --self W812` 实测「与在途批次无交集」）；对账表 touches 列**历史行结构性修改必须列入**（依 pitfalls 明文：追加认领行属 append 安全操作可不列，但改历史行须列）——本批改了 W726-W750 共 23 行认领会话列，故整表列入。② **通信机制**——撞号判定与让号全程留痕：并行会话先落 W811（时序 13:15:39 vs 本会话 13:16:56），本批**主动让号改 W812**并跨会话书面告知（让号依据、37 项 touches 清单、共享面写顺序、禁 add -A）；对方 W811 提交用显式 pathspec 精确暂存 19 文件，本批 34 件在途改动未被卷入。③ **通用机制**——批次协议（对账表取号 → 认领 → 施工 → 级联 → 门禁 → 收官）全程照走；pre-commit hook 改造后仍跑全量 `--scope auto` 分级门禁。④ **撞号处置**——对方通报下一自由号为 W813 并由其写预留 bullet，本批收官**不再写 W813 预留**（避同号重复）。
> - **验证**：全仓该品牌字样终扫 0 命中（含本批自身记录）·搜索索引新鲜度门禁 0 FAIL（zh 822 · en 864 与生成器实算一致）·CSP `--check` 856 页 0 漂移 ·第 45 门禁目录文档新鲜度 0 FAIL / 178 目录 ·第 31 门禁文档口径体检 0 FAIL ·preflight 单测 12 passed ·ruff scripts/ 0 ·hook 语法 `sh -n` 通过且实测选出可用解释器 ·pytest 726 passed / 3 skipped（按仓内既定口径排除既有挂起文件 `tests/unit/test_visualization_data.py`——该文件在全量套件末尾挂起为**改动前既有现象**·经 HEAD worktree 复现同点·非本批引入）·verify_delivery 全量 51 段 0 FAIL。
> - **状态**：已落地（本地全绿）；级联+提交按批次流程执行（不 push）。
> - **文件**：.gitignore、AGENTS.md、CHANGELOG.md、archive/docs/CHANGELOG-ARCHIVE.md、archive/docs/file-index-ARCHIVE.md、archive/docs/plans/2026-09-09-service-experience-and-agent-ops-plans.md、archive/docs/plans/2026-09-17-agent-web-redesign-plan.md、archive/docs/plans/2026-10-07-agent-web-engine-swap-plan.md、archive/scripts/_scan_sd_anchors.py、archive/scripts/_scan_sd_misplace.py、archive/scripts/batches/misc/adversarial-review-integrated-2026-08-11.md、archive/scripts/batches/misc/link-audit-report.md、archive/scripts/batches/misc/perf_canvas_report.md、archive/scripts/batches/w5xx/_w568_spec.json、archive/scripts/batches/w5xx/_w596_spec.json、archive/scripts/batches/w6xx/_w684_spec.json、archive/scripts/w334_font_subset.py、docs/00-导读/W批次编号对账表.md、docs/11-方案报告/W761工具链可维护性重构报告-2026-10-16.md、docs/11-方案报告/工作复盘与优化分析报告/工作复盘与优化分析报告-2026-10-07-治理与引擎.md、docs/11-方案报告/工作复盘与优化分析报告/工作复盘与优化分析报告-2026-10-13.md、docs/11-方案报告/工作复盘与优化分析报告/工作复盘与优化分析报告-2026-10-14.md、docs/11-方案报告/工作复盘与优化分析报告/工作复盘与优化分析报告-2026-10-15.md、docs/11-方案报告/工作复盘与优化分析报告/工作复盘与优化分析报告-2026-10-17.md、docs/11-方案报告/计划方案/T01-任务计划执行与经验沉淀报告-2026-10-14.md、docs/11-方案报告/计划方案/执行前计划-T01.md、docs/superpowers/plans/2026-09-21-demand-side-optimization-master-plan.md、docs/superpowers/plans/2026-10-14-interference-governance-roadmap.md、scripts/archive_file.py、scripts/gen_folder_docs.py、scripts/output/_w745_spec.json、scripts/output/_w778_spec.json、scripts/preflight_check.py、site/data/search.html、site/en/search.html、tests/unit/test_preflight_check.py、tmpe/README.md、CLAUDE.md、scripts/README.md、scripts/output/_w812_spec.json。

### W811（2026-10-20）：CI 断链修复批（工作流 YAML 歧义语法修复 + 可解析性守卫）
> **来源**：W806 退役 GoatCounter 时在 `.github/workflows/ci.yml` 新增全站零 goatcounter 引用防回退守卫，step 名写成 `- name: Guard: no GoatCounter references (W806)`——裸标量值内含 ": "（冒号+空格）在 YAML 映射上下文里属歧义语法，GitHub 解析该工作流时直接报「This run likely failed because of a workflow file issue」，run 0 秒失败，且 pull_request 事件**根本不生成 check**（PR 上看不到 CI 结果）。**潜伏机理三项**：① 既有 CI 接线测试（tests/unit/test_ci_wiring.py）全为 grep/regex 型断言，对 YAML 语法无感 → 本地全绿；② ci.yml 的 `on.push` 只含 `main` → dev 分支 push 从不触发 CI → 缺陷潜伏至推送并开 PR 才暴露；③ W806 的验证只跑本地门禁与 pytest，无任何 YAML 解析步骤。**暴露面声明**：因该工作流此前不可解析，W803-W810 整段从未被 CI 实跑过（dev push 不触发 CI·PR 因工作流解析失败不生成 check）——本批修复后 PR 的 CI 方为该段的首次实跑。
> - **修复**：step 名加引号（`- name: "Guard: no GoatCounter references (W806)"`）→ ci.yml 重新可解析（本地 PyYAML 解析通过·10 个 job 全在：pages-smoke / lighthouse-performance / a11y-audit / dependency-scan / code-quality / pytest-unit / verify-delivery / e2e-interaction / agent-web-build / desktop-build）。
> - **守卫**：`tests/unit/test_ci_wiring.py` 增 W811 守卫（12 例全过）——J1 无制表符缩进（YAML 禁制表符）/ J2 映射项 name 的裸标量值不得含 ": "（加引号即合法）/ J3 PyYAML 可用时做全量解析（加严；不可用时由 J1+J2 覆盖本风险类·非静默跳过）。**负样本实证**：把 ci.yml 还原成 W806 形态（去掉引号）后跑真实守卫函数，按预期报错并指到 `ci.yml:353`；真实 9 个 workflow 文件全过。
> - **验证**：守卫单测 12 passed + 负样本实证按预期报错（指到 ci.yml:353）+ 真实 9 个 workflow 全过 + pytest 全量 726 passed / 3 skipped + verify_delivery 全量 51 段 0 FAIL。
> - **状态**：已落地（级联+提交按批次流程执行）。
> - **文件**：.github/workflows/ci.yml、tests/unit/test_ci_wiring.py、docs/00-导读/W批次编号对账表.md、scripts/output/index.md、scripts/output/README.md、scripts/output/_w811_spec.json。

### W810（2026-10-20）：站内搜索死代码清理批
> **来源**：W807 刷新站内搜索索引时遗留的清理候选——旧 `window.SEARCH_INDEX = [...]` 数组在换成 `SITE_SEARCH_INDEX_ZH/EN` 新常量后成为零引用死重（zh 2044 字符 / en 2328 字符），每页各背 2KB 余量。
> - **零引用三项核查**：① 页面 JS 只读 `SITE_SEARCH_INDEX_ZH/EN`（zh:1303 / en:1287），legacy 数组零引用；② `scripts/validate_en.py` 只认 `/* SEARCH_INDEX:BEGIN */…END` 包裹区，不读 legacy 数组；③ 生成器 `_gen_search_index.py` 的同名匹配仅为「缺标记时的兜底注入锚点」，而两页标记齐全故该分支不可达（生成器面不动·不属本批范围）。
> - **落地**：两页各删 1 行（−2271 / −2329 字节）+ `generate_csp.py` 重算该 2 页内联脚本哈希（恰好 2 页更新·其余 854 页 0 漂移）。**范围纪律**：本批不新增门禁、不改生成器与页面逻辑，纯粹删死代码。
> - **验证**：CSP `--check` 856 页 0 漂移 + 第 46 槽搜索索引新鲜度门禁 0 FAIL（zh 822·en 864 与生成器实算一致·删除未触及载荷块）+ check_structure 855 文件 1411 style 块 + check_js_syntax 855 文件 + e2e 站点质量套件全过（S1 rows=23 errors=[]·S1b rows=4 exactHit=true·与改动前逐字一致）+ pytest 719 passed / 3 skipped + verify_delivery 全量 51 段 0 FAIL。
> - **状态**：已落地（级联+提交按批次流程执行）。
> - **文件**：site/data/search.html、site/en/search.html、docs/00-导读/W批次编号对账表.md、scripts/output/_w810_spec.json。

### W809（2026-10-20）：站内搜索索引新鲜度门禁挂载批
> **来源**：W807 刷新站内搜索索引后遗留的登记余项——「索引新鲜度门禁未挂载」：内容批次改 `docs/` 或 `site/` 后忘重跑生成器，索引即静默陈旧（用户搜不到新文档·旧链接点不开），而**刷新动作本身无机器防线**。
> - **生成器函数化（挂槽前置）**：`scripts/_gen_search_index.py` 原实现把「算」与「写」同放模块级（import 即落盘），门禁无法安全复用 → 拆为 `build_indexes()` 纯计算 + `main()` 写盘；**实证**：import 后两页 sha256 不变（不落盘）、脚本实跑二跑 sha256 一致（仍幂等）。
> - **新建第 46 槽门禁**：`scripts/check_search_index_fresh.py`——三判据（C1 两页 `SEARCH_INDEX:BEGIN/END` 标记块存在·C2 zh 页内嵌载荷 == 实算载荷·C3 en 页同），逐条对拍 kind/标题/分类/摘要/URL/关键词（禁字节串比对：JSON 序列化细节变化会致假红）；期望载荷由生成器 `build_indexes()` 纯计算得出，**门禁只读不写**，刷新动作仍为 `python scripts/_gen_search_index.py` + 重算 CSP 哈希；**fail-closed**：jieba 缺失则 kw 退化为逐字、期望载荷不可信 → 报「环境缺依赖」并 FAIL，禁静默跳过假绿（与第 31/45 门禁同族纪律）。
> - **挂载三方编号对账**：`scripts/verify_delivery.py` 门禁元组 + `EXPECTED_SECTION_NAMES` + scope 归属（docs 与 site **两面**——任一面改动即令索引过期）+ `docs/agent/gates.md` 第 46 条 + `AGENTS.md` §4.2 摘要（45→46 槽）——第 41 门禁「编号三方对账」为该面的机器防线。
> - **单测**：`tests/unit/test_check_search_index_fresh.py` 5 例（现网实跑 0 FAIL / 自检 5-5 / 判据单元 4 类漂移 / jieba 缺失 fail-closed / 挂载一致性点检）。
> - **验证**：门禁 `--self-test` 5/5 + 单测 5 passed + 现网实跑 0 FAIL（zh 822 条 · en 864 条与实算一致）+ 第 41 门禁 0 FAIL + pytest 全量 + verify_delivery 全量 51 段 0 FAIL。
> - **状态**：已落地（级联+提交按批次流程执行）。
> - **文件**：scripts/check_search_index_fresh.py、scripts/_gen_search_index.py、tests/unit/test_check_search_index_fresh.py、scripts/verify_delivery.py、docs/agent/gates.md、AGENTS.md、README.md、scripts/index.md、tests/unit/index.md、scripts/output/index.md、scripts/output/README.md、scripts/output/stats.json、scripts/output/stats-index.md、docs/00-导读/W批次编号对账表.md、scripts/output/file-index.md、scripts/output/_w809_spec.json。

### W808（2026-10-20）：Web Agent 全栈加固批
> **来源**：用户令「全栈一遍（集成层 + 后端生产化）」+「测试三件套全上（单测 + 集成 + 前端 E2E）」+「完整 W808 批次施工但提交留用户」。审计 agent-web（仓库内唯一全栈应用：React 19 + Vite 8 + TS 前端 / Express 5 + better-sqlite3 后端）后发现三处**真实跨边界缺陷**与一批生产化缺口。
> - **真实缺陷①（反馈恒丢）**：`src/components/ChatMessages.tsx` 提交 `/api/feedback` 时**漏传 sessionId**，而服务端要求 sessionId + messageId + verdict 三者齐备 → 每次赞/踩恒 400，且前端 `.catch(() => {})` 静默吞掉 → **用户的赞/踩从未被记录且界面无任何异常表现**。修复：补齐 sessionId（`ChatPage` 透传）+ 改走统一 client + 失败回滚乐观 UI。
> - **真实缺陷②（错误被当成功数据）**：`src/utils/api.ts` **不判 `res.ok`**——服务端 500 的 `{error}` 响应体被 `await res.json()` 当成功数据返回，调用方拿到「成功的错误」故错误被静默吞掉；SSE 流 `/api/chat` 同样不判状态码，401/400 的 JSON 体被当流解析 → **「思考中…」永久挂起**。修复：统一 client 判状态码 + 类型化 `ApiError`（携带 status 与 body）+ SSE 路径补判非 2xx。
> - **真实缺陷③（开 token 即全站 401）**：服务端 `AGENT_WEB_TOKEN` 鉴权（P0-1）此前**前端从不携带该 token** → 一旦启用即全站 401 且无人察觉。修复：dev/preview 代理层注入（token 不进浏览器包·不落 localStorage）+ 前端 `VITE_AGENT_WEB_TOKEN` 兜底。
> - **后端生产化**：新建 `server/errors.ts`（类型化错误层级 + 全局错误处理中间件：运营错结构化返回·编程错只记日志返通用 500·不泄堆栈）+ `server/logger.ts`（结构化 JSON 日志 + 凭证脱敏）+ `server/requestId.ts`（request ID 全链路传播·响应头回写 + 上游 ID 沿用 + 畸形 ID 净化）+ `server/validation.ts`（Zod 边界校验·全部 /api 端点·零信任客户端）+ `server/shutdown.ts`（SIGTERM/SIGINT 优雅关闭：排空在途请求 + WAL checkpoint + 关库）；`/api/ready` 就绪探针新增（依赖不可用返 503）。
> - **前端集成层**：新增 `src/utils/apiTypes.ts`（前后端共享类型契约·两端字段改名即编译期报错）+ `src/utils/errorMessage.ts`（状态码 → 用户可读文案映射·此前失败只 `console.error` 吞掉·界面表现为空白无提示）；`useSessions`/`useModels`/`useChat`/`ChatMessages`/`SettingsPage` 五处裸 `fetch` 全部收敛到统一 client；`App.tsx` 新增失败横幅 + 重试。
> - **配置链修复**：`dotenv` 此前是 package.json 里**声明了却从未被 import** 的依赖 → 文档化的「复制 .env.example → .env」配置流程实际从未生效；本批补上加载（不覆盖既有环境变量）。
> - **产物遮蔽根修**：`tsc -b` 此前把 `vite.config.js` 吐在项目根，而 Vite 的配置解析**优先读 .js** → 改 `vite.config.ts` 静默失效（latent 接线缺失）；改为 `outDir=./.tsbuild` 产物移出源目录（40 个陈旧产物一并清理）。
> - **测试三件套**：① **单元**（vitest 5 + testing-library·40 例：api client 的 res.ok/token/基址三缺陷各有负样本 + 错误文案映射 + 会话 hook 失败态可见）；② **集成**（真实起服 + 真实 HTTP + 真实 SQLite·14 例：就绪探针 / request ID 全链路 / 边界校验 / 错误体形状恒为 `{error}` / 会话 CRUD 全链路落库 / 优雅关闭）；③ **E2E**（Playwright 真实浏览器 + 真实构建产物 + 真实后端 + 真实 SQLite·10 断言：输入 → 发送 → 流式渲染 → 落库 → 反馈全流程；外部大模型端点以 `e2e/mockLlm.mjs` 替身·被测系统全部真实实现）。
> - **契约红线**：对外路径/方法/字段名/状态码/SSE 事件序**零改动**；`/api/feedback` 校验失败保持既有 `400 invalid body`（`feedback.test.mjs` 钉此契约）；CORS 维持「无 CORS 中间件 + 回环绑定 + 可选 token + 限流」防护模型（不引入跨源面）。
> - **验证**：三层测试全绿（单测 40 passed / 集成 13 passed + 1 skipped〔SIGTERM 信号位为 POSIX 专属·真实执行位=CI（Linux）〕/ E2E 10 通过）+ 既有 `test:server` 67 passed（限流 429 与 token 鉴权负样本均绿·证明错误处理器重构未改契约）+ `npm run build` 成功 + 第 45 门禁 0 FAIL + verify 全量 50 段 0 FAIL。
> - **文件**：xiyouji-agent-web/server/errors.ts、server/logger.ts、server/requestId.ts、server/validation.ts、server/shutdown.ts、server/types.ts、server/index.ts、server/routes.ts、server/middleware.ts、server/config.ts、server/db.ts、server/api.integration.test.ts、xiyouji-agent-web/src/utils/api.ts、src/utils/apiTypes.ts、src/utils/errorMessage.ts、src/utils/api.test.ts、src/utils/errorMessage.test.ts、src/hooks/useSessions.ts、src/hooks/useModels.ts、src/hooks/useChat.ts、src/hooks/useSessions.test.tsx、src/components/ChatMessages.tsx、src/components/SettingsPage.tsx、src/pages/ChatPage.tsx、src/App.tsx、src/test/setup.ts、xiyouji-agent-web/e2e/chat.e2e.mjs、xiyouji-agent-web/e2e/mockLlm.mjs、xiyouji-agent-web/vite.config.ts、xiyouji-agent-web/vitest.config.ts、xiyouji-agent-web/tsconfig.node.json、xiyouji-agent-web/package.json、.github/workflows/ci.yml、.gitignore。

### W807（2026-10-20）：站内搜索索引刷新批
> **来源**：W806 退役 GoatCounter 时顺带盘点站内搜索，发现站内搜索索引自 2026-09-16 前后停更：全站 771 条索引仅含 61 篇 doc 条目，且 9 条链接仍指向已改名的 `docs/11-报告复盘/`（GitHub 侧 404）——**无任何门禁覆盖**，属远早于该批的历史债。
> - **生成器归位**：恢复 `scripts/_gen_search_index.py`（W573 原位·「常驻留档·内容批次收尾重跑」的设计意图）——归档副本 `archive/scripts/batches/misc/` 因目录加深两层致 `ROOT` 解析错位（指向 `archive/scripts/batches/`），不可直接运行；归档件按「禁改归档」纪律保持原样。
> - **实跑刷新**：`py -3 scripts/_gen_search_index.py` → `docs=726 pages_zh=96 pages_en=138`，两页索引常量 256182/276180 字节（≤500KB 预算内）；条目构成 doc 61→111（+50 篇文档首次可检索）·page 95→96·reader 615 不变；**失效目录引用 `docs/11-报告复盘/` 9→0**（改指 `docs/11-方案报告/`·28 处）。**幂等实证**：二次实跑两页 sha256 逐字节一致。
> - **CSP 重算**：内联常量变更 → `py -3 scripts/generate_csp.py` 重算该 2 页哈希（856 页 0 漂移）。
> - **常驻防线（新增）**：`tests/e2e/test_site_quality.js` 补两条断言（S1 搜索页离线检索有结果且无脚本错误；S1b 刷新后新增文档《协议边界速查》标题单元格精确命中·合计新增 40 行）——**负样本实证**：同款断言在 HEAD 旧索引上返回 1 行（弱 kw 命中《“变”的哲学：七十二变的能力边界》·sc=4）但 exactHit=false（标题单元格无全等命中·必红），故 S1b 具真实区分力（非文本包含式弱断言）。该套件已由 CI `e2e-interaction` job 接线。
> - **验证**：生成器实跑幂等（二跑 sha256 一致）+ CSP `--check` 856 页 0 漂移 + e2e 站点质量套件全过（含 S1/S1b 两条新断言·负样本实证旧索引必红）+ pytest 全量 719 passed / 3 skipped（排除既有挂起文件 `tests/unit/test_visualization_data.py`；解释器退出时挂起为既有现象）+ verify_delivery 全量 50 段 0 FAIL。
> - **登记余项**：**「索引新鲜度门禁」未挂载**——「页面内嵌索引 == 生成器实算输出」需要新增 verify_delivery 门禁段，而 `scripts/verify_delivery.py` 属管控文件（改动须经用户批准），故本批只加 e2e 功能面断言，不擅自加段；待批准后另立批挂载。
> - **状态**：已落地（级联+提交按批次流程执行）。
> - **文件**：scripts/_gen_search_index.py、site/data/search.html、site/en/search.html、tests/e2e/test_site_quality.js、scripts/index.md、docs/00-导读/W批次编号对账表.md、scripts/output/file-index.md、scripts/output/_w807_spec.json。

### W806（2026-10-20）：GoatCounter 统计链彻底退役批
> **来源**：GoatCounter 站点代码 1273984347 失效——`py -3 scripts/fetch_gate_stats.py --json` 实测 HTTP 404「not found」（断链自 2026-09-30，至裁决日未恢复）：页面埋点采不到任何数据，却仍在每页加载并产生一次无效外域请求。用户裁决「彻底退役」（选项 A）。
> - **退役范围（234 页）**：site 根 8 + site/data 88 + site/en 138 页移除 `<script data-goatcounter>` 埋点标签（全站 `data-goatcounter` 残留 0；`site/reader/**` 自建站起未注入·本就无残留）；CSP 生成源去掉计数端点后重算 **856 页** meta（其中 **546 页**原含该域放行），`site/_headers` 同步；`site/data/search.html` 与 `site/en/search.html` 摘除活的 `window.goatcounter.count` 搜索词上报分支（搜索词改为仅落本机 localStorage）。
> - **工具与脚本退役**：删除 `scripts/inject_goatcounter.py`（注入器）与 `site/static/js/goatcounter.js`（自托管 count.js）；`scripts/output/script-coverage-baseline.txt` 同步移除两条登记行（含一行与实现不符的注释）。
> - **防回退守卫（新增）**：`scripts/check_no_goatcounter.py`——四项判据（C1 页面无埋点标签 / C2 页面无外域放行 / C3 站点无追踪脚本 / C4 工具无注入器），自测 1 正 4 负（`--self-test` 输出 SELF_TEST_OK），单测 `tests/unit/test_check_no_goatcounter.py` 5 passed；接入 `.github/workflows/ci.yml` 的 `verify-delivery` job（CI 侧机器引用·满足第 42 门禁脚本覆盖口径）。
> - **RUM 口径改造**：`site/js/rum.js` 删除 GoatCounter 改道分支与随之失效的 `bucket()` 死函数，改为三条明确通道——① 本地 dev origin（localhost/127.0.0.1/[::1]）→ POST `/api/rum` 回流本地后端 ② 显式 `window.__RUM_CONFIG__.endpoint` → 按配置外发 ③ 其余（GitHub Pages 等纯静态托管）→ 零网络请求·仅 localStorage 备援；`site/js/visit-log.js`、`site/rum-viewer.html` 同步口径。
> - **文档口径同步**：`docs/00-导读/访问统计方案.md` 改写为《访问统计现状与退役记录》（退役依据/历史选型存档/恢复路径）；`docs/00-导读/V2可视化维度方案.md` 零外域请求口径改为全站零例外；`docs/11-方案报告/读者数据复盘.md` 与其目录 README 加 W806 现状声明（W626 判定结论予以保留·数据源重建前无法复算）；`scripts/fetch_gate_stats.py` 保留在库并加现状声明（纯 CLI 工具·账号重建后复用）。
> - **验证**：CSP `--check` 856 页 0 漂移；守卫实跑 0 FAIL + 自测 SELF_TEST_OK + 单测 5 passed；`node --check site/js/rum.js` 通过；pytest 全量 719 passed / 3 skipped（排除既有挂起文件 `tests/unit/test_visualization_data.py`；解释器退出时挂起为 HEAD worktree 对拍复现的既有现象·非本批引入）；verify_delivery 全量 50 段 0 FAIL。
> - **W805 遗留件补入**：`docs/00-导读/协议边界速查.md`（双协议适用范围 + 边界快速表·MIT/CC BY-NC 4.0）系 W805 会话已产出但未入库的新文档，file-index 仍记 W805；本批随提交一并入库，并同步 `docs/00-导读/README.md`、`docs/00-导读/index.md` 与 `docs/INDEX.md` 的登记（计数 12→13 / 718→719 篇）。
> - **状态**：已落地（级联+提交按批次流程执行）。
> - **文件**：scripts/check_no_goatcounter.py、tests/unit/test_check_no_goatcounter.py、scripts/generate_csp.py、site/js/rum.js、site/js/visit-log.js、site/rum-viewer.html、site/_headers、site/data/search.html、site/en/search.html、site/static/js/index.md、scripts/index.md、scripts/output/script-coverage-baseline.txt、scripts/fetch_gate_stats.py、eslint.config.mjs、.github/workflows/ci.yml、.github/workflows/perf.yml、tests/e2e/test_smoke.js、docs/00-导读/访问统计方案.md、docs/00-导读/V2可视化维度方案.md、docs/11-方案报告/读者数据复盘.md、docs/11-方案报告/README.md、docs/10-方法论沉淀/白屏三连根因复盘与防回归清单.md、docs/INDEX.md、docs/00-导读/W批次编号对账表.md、scripts/output/file-index.md、scripts/output/_w806_spec.json、docs/00-导读/协议边界速查.md。

### W805（2026-10-19）：跨平台测试守卫热修批
> **来源**：W804 推送后 dev→main PR 的 CI 首跑（run 39177553777）在 Linux 暴露 W803 引入的测试缺陷——`tests/test_xiyouji_mcp_extra.py::TestInheritedBehaviour::test_directory_as_target_file_raises_permission_error` 断言 `pytest.raises(PermissionError)`，而 Linux/macOS 读目录抛 `IsADirectoryError`（同属 OSError），致「1 failed / 729 passed」CI 红。
> - **缺陷定位**：W803 为 mcp-server 拆分新增该「继承行为守卫」测试，断言绑定 Windows 专属异常子类；本地 Windows 绿、未推送前 Linux 从未执行，属**平台口径缺陷**（非业务行为变更）。
> - **修复（仅测试面，行为零变更）**：断言改为跨平台 `pytest.raises(OSError)`，测试更名 `test_directory_as_target_file_raises_os_error`，docstring 明写「Windows PermissionError / Linux IsADirectoryError 同属 OSError，守卫点=目录当文件会抛异常，不绑定平台子类」；被测 `xiyouji_drl_spotcheck` 生产代码未动。
> - **验证（全绿）**：`pytest tests/test_xiyouji_mcp_extra.py -q` 67 passed；全量排除既有挂起文件 `pytest tests -q --ignore=tests/unit/test_visualization_data.py` 714 passed / 3 skipped；ruff `check scripts/` 0；verify_delivery 全量 50 段 0 FAIL；推送后 PR CI 复跑（Unit Tests pytest job）转绿为准。
> - **状态**：已落地（级联+提交按批次流程执行）。
> - **文件**：tests/test_xiyouji_mcp_extra.py、docs/00-导读/W批次编号对账表.md、scripts/output/_w805_spec.json

### W804（2026-10-19）：桌面版三平台安装包与自动更新批
> **来源**：用户令「给项目在 GitHub 仓库上面增加一个可以直接下载的安装包，并且支持自动更新」。方案裁定为离线全站桌面版：Electron 壳内嵌全部站点内容（87 可视化页 + 615 篇解读），三平台 GitHub Releases 分发 + electron-updater 自动更新。
> - **桌面应用（新建 xiyouji-desktop/）**：Electron 44 主进程 + 本地静态服务（纯 Node stdlib·127.0.0.1 随机端口·路径穿越防护·仅 GET/HEAD）+ 中文菜单与原生更新对话框 + 单实例锁与崩溃日志；`--self-test` 无窗口冒烟；`node --test` 33 项单测覆盖静态服务与内容版本解析。
> - **自动更新**：electron-updater 6.x（publish 指向本仓库 Releases）；启动 3 秒首次检查、之后每 4 小时复查，菜单「帮助→检查更新…」手动触发；发现新版本询问下载→下载进度→重启安装（选择稍后则退出时安装）；开发态与 `XIYOUJI_DISABLE_UPDATE=1` 安全降级。
> - **发布流水线（新建 .github/workflows/release.yml）**：tag v* 或 workflow_dispatch → 版本一致性闸门（tag 与 xiyouji-desktop/package.json 严格相等，内容批次从 CHANGELOG 首段动态提取）→ 三平台并行构建（Windows NSIS / macOS universal dmg+zip / Linux AppImage）→ 汇总上传 GitHub Release（latest*.yml 与 blockmap 自动更新元数据必传）+ 中文 release notes；Release 已存在时 clobber 更新（幂等重跑）。
> - **CI 接线**：ci.yml 新增 desktop-build job（npm ci + node --test + prepare:content + electron-builder --dir），防止桌面工程回归；workflows/README.md 登记 release.yml 与发布/自动更新流程。
> - **下载入口**：根 README 新增「桌面版下载（可安装·自动更新）」段（三平台固定直链 releases/latest/download/...）；STRUCTURE 顶层目录与 README 目录树登记 xiyouji-desktop/。
> - **验证（全绿）**：npm install + npm test 33 passed；`--self-test` 输出 SELF_TEST_OK（开发态与打包产物双跑）；dist:win 产出 xiyouji-desktop-win-x64.exe 130,705,240 B + latest.yml（sha512 实测对拍一致·app-update.yml 的 provider/owner/repo 正确）；pytest 714 passed / 3 skipped（tests/unit/test_visualization_data.py 末尾挂起为改动前既有现象·W803 已登记，本批排除该文件实跑）；ruff 0；actionlint 0 errors；verify_delivery 全量 50 段 0 FAIL。
> - **状态**：已落地（级联+提交按批次流程执行；tag v2.3.0 触发 .github/workflows/release.yml 三平台发布，资产以 GitHub Release 页为准）。
> - **文件**：xiyouji-desktop/、.github/workflows/release.yml、.github/workflows/ci.yml、.github/workflows/README.md、README.md、STRUCTURE.md、docs/00-导读/W批次编号对账表.md、scripts/output/_w804_spec.json

### W803（2026-10-19）：工具链行为保持重构批：公共骨架提取与长函数拆分
> **来源**：用户令「对本项目进行代码重构，在保持原有功能、输入输出及外部接口完全不变的前提下提升可读性与可维护性」。动工前先做重复形态普查（378 个 Python 文件 AST 扫描：同名函数体、helper 名频次、惯用法计数），按取证结果定面，不凭印象动刀。
> - **公共骨架提取（新建 scripts/utils/gate_common.py·250 行）**：把 `check_*` 门禁族各自内联的骨架收敛为单一实现——`ROOT`/`SCRIPTS_DIR` 常量、`read_text`（容错）与 `read_text_strict`（严格·两口径按门禁类型分治不互替）、`site_pages`（站点三源清单·支持二源变体）、`iter_style_blocks`（style 块正文+起始行号）、`run_case_batch`/`SelfTestTally`（自测计数与收尾行）、`cli_main`（`--self-test` 分发）；共 12 个公共符号。
> - **门禁族改为消费公共模块（7 个脚本）**：`check_css_decl_separators`/`check_css_orphan_selectors`/`check_css_var_refs`/`check_html_head_content`/`check_kpi_card_base`（第 33-37 门禁）+ `check_agents_layers`/`check_claude_md`（第 41/32 门禁）。判定内核函数名与签名全部未变；`--self-test` 与只读扫描的 stdout 逐字节不变。
> - **清死代码（1 处）**：`check_claude_md.py` 的 C3 行数计算原有连续两次赋值，第一次结果从未被读取（含两项恒为 0 的加法）——以 7 个边界样本（空串/无尾换行/有尾换行/仅换行/双换行）+ 真实 CLAUDE.md 实算证明旧新等值（0 处不一致）后删除。
> - **长函数拆分**：`lint_links.py` 的 `_process_file`（69 行）拆出链接提取与逐链接判定两段，`check_internal`/`try_fix` 的路径解析口径收敛为共用助手；`_check_external` 的循环内 import 提升为模块级。`mcp-server/xiyouji_mcp.py` 四个 MCP 工具（94-102 行）各拆为参数校验/判定/汇总若干私有助手，`EXPECTED_TYPES`/`SECTION_TITLES` 提为模块级常量、五处重复的 annotations 字典收敛为 `READONLY_TOOL_ANNOTATIONS`。
> - **Web Agent 服务端按职责分文件**：`server/index.ts` 710 → 51 行（路由注册/SSE/中间件/权限/配置/HTTP 工具各自成文件），`src/components/ToolCallsCollapse.tsx` 767 → 166 行（渲染分支拆为 `src/components/toolCalls/` 5 个模块），新增 `src/utils/` 三个复用模块。
> - **对拍取证（新增证据链）**：以 git worktree 重建 HEAD 旧态做同源对拍，避免路径伪差——8 个脚本 × 2 模式共 16 组，stdout 逐字节一致（`lint_links --dir docs` 一组首轮报差异，查明为 worktree 内未跟踪文件触发 gitignore 排除的**取证环境伪差**，改在同仓两跑后 sha256 完全相同）；MCP 模块以 30 组输入覆盖全分支（4 种 replacement 组合/5 种 JSON 失败 reason/越界/空目录/截断）返回字典序列化逐字节一致。Web Agent 以路由集合（14 条无丢失）、SSE `type` 取值集合（13 个无丢失）、导出符号与 `npm run build`、`npm run test:server` 为契约面。
> - **关于第 45 门禁**：本次新增目录与新文件触发目录文档新鲜度门禁，已按生成器刷新（`gen_folder_docs.py` + `--refresh`），不手改生成物。
> - **验证（全绿）**：ruff check scripts/ mcp-server/ 0；pytest 单元面 427 passed / 3 skipped（`tests/unit/test_visualization_data.py` 在全量套件末尾挂起属**改动前既有现象**，已用 HEAD worktree 复现同点同状态，非本批引入）；verify_delivery 全量 50 段 0 FAIL；`npm run build` 成功、`npm run test:server` 67 passed / 0 fail。
> - **状态**：已落地（级联+提交按批次流程执行）。
> - **文件**：scripts/utils/gate_common.py、scripts/check_css_decl_separators.py、scripts/check_css_orphan_selectors.py、scripts/check_css_var_refs.py、scripts/check_html_head_content.py、scripts/check_kpi_card_base.py、scripts/check_agents_layers.py、scripts/check_claude_md.py、scripts/lint_links.py、mcp-server/xiyouji_mcp.py、xiyouji-agent-web/server/、xiyouji-agent-web/src/、tests/test_xiyouji_mcp_extra.py、tests/unit/test_lint_links_refactor.py、docs/00-导读/W批次编号对账表.md、scripts/output/_w803_spec.json、scripts/output/_cascade_files_W803.txt

### W802（2026-10-19）：character_nlp 行为保持重构批·二
> **来源**：用户令「继续」——W801 的延续（同模块剩余两处）。对拍法修正：W801 首轮的 base/new 比较混入输出路径字符串伪差，本批改用**同路径两跑**（旧版 stash 后跑→存证→恢复→新版跑→diff）。
> - **拆分三（89 行 → 4 个函数）**：`find_dialogues_in_text` 拆出 `_build_dialogue_patterns`（标准/倒装两正则编译）/ `_collect_standard_dialogues`（返回引语列表 + 起始位置集供倒装去重）/ `_collect_inverted_dialogues`；别名 alternation 构建、去重规则、按位置排序原样保留。
> - **拆分四（85 行 → 4 个函数）**：`build_cooccurrence_timeline` 拆出 `_accumulate_timeline`（按回累加五组数据）/ `_build_binned_output`（每桶 Top 30 组装）/ `_build_top_pairs_curve`（Top 10 关系对曲线）；公开函数缩为取数与拼装。
> - **对拍（修正法）**：同路径两跑（PYTHONHASHSEED=0）——stdout 与 5 件 JSON（最大 dialogues.json 2.2MB）**逐字节一致**。
> - **模块终态**：character_nlp.py 1118 行，公开 API 未变；≥60 行函数从 4 个（W801 前）降为 0 个；`_` 前缀小函数承担全部单职责环节。
> - **验证（全绿）**：ruff 0；pytest 629 passed / 3 skipped；verify 全量 50 段 0 FAIL。
> - **状态**：已落地（级联+提交+推送按批次流程执行·PR #51 随批扩入）。
> - **文件**：scripts/B_人物/character_nlp.py、docs/00-导读/W批次编号对账表.md、scripts/output/_w802_spec.json、scripts/output/_cascade_files_W802.txt

### W801（2026-10-19）：character_nlp 行为保持重构批
> **来源**：用户令「对本项目进行代码重构·功能不变」。先做真实审计：全仓 ≥60 行函数 47 个，其中 4 个为 `_` 前缀一次性脚本、2 个（check_doc_sync.run_self_test / bump_version.main）W787 已裁定不动、其余按停 churn 纪律不碰；**唯一未被 W782–W787 覆盖的现役模块 = `scripts/B_人物/character_nlp.py`**（995 行·W783 重构的是同目录 character_appearance）。动工前 preflight PASS。
> - **拆分一（190 行 → 7 个函数）**：`build_dialogue_sentiment` 保留公开签名与 docstring，内部拆出 `_accumulate_dialogue_sentiment`（单循环四组累加）/ `_build_speaker_sentiment` / `_build_chapter_sentiment` / `_build_speaker_chapter_curve` / `_build_top_sentiment_words`；公开函数只做取数与拼装，注记块原位保留。
> - **拆分二（175 行 → 8 个函数）**：`main` 拆出 `_build_arg_parser` / `_load_chapters` / `_warn_missing_chapters` / `_write_json`（五处重复落盘收敛）/ `_emit_characters` / `_emit_cooccurrence` / `_emit_dialogues`（返回值供 sentiment 复用）/ `_emit_timeline` / `_emit_sentiment`；main 缩为 24 行编排。**print 文案与顺序逐字未变**。
> - **对拍（五维矩阵简化版）**：旧版（HEAD）与新版本跑同一份 100 回输入——`PYTHONHASHSEED=0` 下 5 件 JSON（characters/cooccurrence/cooccurrence_timeline/dialogue_sentiment/dialogues·最大 2.2MB）与 stdout **逐字节一致**；首轮 base/new 比较 `cooccurrence.json` 差异经查为**集合序非确定性**（同代码两次运行亦不同·固定种子即稳定），**非代码差异**。
> - **新发现登记**：B-109 `build_cooccurrence` 输出非确定（重跑产生无意义 diff）——修复属行为变更（输出序变），须单独立批，本批不修。
> - **未动清单（诚实边界）**：47 个 ≥60 行函数中仅 2 个被本批拆分；其余为一次性脚本与已裁定项；命名与风格统一限于本文件（模块内 `_` 私有前缀约定一致）。
> - **验证（全绿）**：ruff 0；pytest 629 passed / 3 skipped；verify 全量 50 段 0 FAIL。
> - **状态**：已落地（级联+提交+推送按批次流程执行·PR #51 随批扩入）。
> - **文件**：scripts/B_人物/character_nlp.py、docs/superpowers/plans/2026-09-30-maintenance-backlog-registry.md、docs/00-导读/W批次编号对账表.md、scripts/output/_w801_spec.json、scripts/output/_cascade_files_W801.txt

### W800（2026-10-19）：第四轮外部评审回应批
> **来源**：用户转发第四轮外部评审（文本/可视化/社区三线 + 认识论总结「可信度剧场」）。动工前 preflight PASS（W800 认领·零交集）。
> - **事实漂移核对**：评审称「W759 / 43 项门禁 / 600+ 提交」，实测 **W799 / 50 段（45 槽）/ 825 提交**——**基于旧快照**（与 W790 第三轮同症）；质量方差/工程 overhead/单人维护三条=**BL-26/27/28 的重复投递**，不重复登记。
> - **① 门禁边界（直答最尖锐一条）**：README「AI 生成说明」责任边界后新增——门禁保障**可机器判定的形式面**（引文真实/结构一致/术语/可达性），**不保障**内容判断（论点是否平庸/论证是否扎实/阐释是否有生命体验，由作者审读承担·篇目深浅不一）；明写「**门禁数量不是学术质量的背书**：它证明没有编造，不证明值得读」。
> - **② 阅读契约后移（读者优先）**：README 首屏由「契约在前」改为「一句话介绍在前」；契约压成一行并加「先读是什么/为什么」导引——回应「进门先签合同」的批评，W707 契约本体保留。
> - **③ 133 维性质分层**：README 口径注后 + 统计口径说明 §3 同步——A-L/Q+ 学术向、M-U/V-AH/Q++ 含趣味跨界、Q+++ 工具向；明写趣味维度是**刻意保留的雅集成分·不承担学术论证**（不删维度，画清边界）。
> - **④ 数据基础公开**：统计口径说明新增 **§8「文本与数据基础及适用性限制」**——原文底本（100 回·古诗文网·706,586 字符·未多版本校勘·BL-19 两真源未决）/ 分词（jieba·未做明代白话适配·词频为近似值）/ 情感极性（人工标注非通用词典）/ 数据生成双路径（run_all 链 + 残留扫）/ 引用建议（趋势相对比较可·绝对统计需复核·不提供学术级保证）。
> - **登记**：B-105 可视化叙事有效性（抽 5 页做结论-数据-图型审计·不预设删除）、B-106 D3 遗产化风险（现状单页零耦合·大改优先抽公共模块）、B-107 数据基础学术校验（涉投稿时单独立批）、**B-108 已落地即关**。
> - **验证（全绿）**：第 31 槽 0 FAIL（C5c 71 处 NOTE 为存量报告型）；stats 零差异；docs_index 718 篇最新；pytest 629 passed / 3 skipped；ruff 0；verify 全量 50 段 0 FAIL。
> - **状态**：已落地（级联+提交+推送按批次流程执行·PR #51 随批扩入）。
> - **文件**：README.md、docs/00-导读/统计口径说明.md、docs/superpowers/plans/2026-09-30-maintenance-backlog-registry.md、docs/00-导读/W批次编号对账表.md、scripts/output/_w800_spec.json、scripts/output/_cascade_files_W800.txt

### W799（2026-10-19）：截图桶 TTL 收紧批
> **来源**：用户令「改成 7 天，_shot 本来就是临时证据桶」。
> - **策略变更**：`tmpe/policy.yml` `ttl_days._shot` **30 → 7**（其余 TTL 不动：_misc 90 / _inbox 7 / _trash 7）；截图桶定位=临时证据·全部可再生（视觉基线另有 tests/e2e/baseline 版本化，不受影响）。
> - **按新规清理**：删除 **25 项 / 40.3MB**（目录 6 + 散文件 19·最老 11.9 天·含 `_c_review2_png` 10.8MB / `mqxs_pages` 10.2MB 等）；剩余 38 项 262MB 全部在 7 天内保留。
> - **口径修正（诚实留痕）**：tmpe 总量复核 **574MB**（du·文件实计 563.5MB）——W798 章记载的「1.8GB→615MB」中 615MB 系删除过程瞬时取样，本批以复核值为准；本轮总账=1.8GB → 574MB（降幅 68%）。
> - **验证（全绿）**：pytest 629 passed / 3 skipped；ruff 0；verify 全量 50 段 0 FAIL。
> - **状态**：已落地（级联+提交+推送按批次流程执行·PR #51 随批扩入）。
> - **文件**：tmpe/policy.yml、docs/00-导读/W批次编号对账表.md、scripts/output/_w799_spec.json、scripts/output/_cascade_files_W799.txt

### W798（2026-10-19）：对拍模板转正批
> **来源**：用户令「全都做」——tmpe 清理 ①②③ + 对拍模板转正（P-42-03）。本轮 tmpe 实测与处置见下。
> - **转正入库**：`tmpe/_templates/duipai/`（gitignored 工地层）→ `docs/_templates/duipai/`（随仓版本化）——duipai.py（6.4KB·snapshot 采集+计时归一ization / compare 逐行与 --sort 多重集）+ README（头部标注转正 + 用法路径改 `docs/_templates/duipai/`）；tmpe 副本删除。引用同步：`docs/10-方法论沉淀/批次交付流水线.md` §八模板路径改指。
> - **tmpe 清理实录（1.8GB → 615MB）**：① 归桶 `--apply --confirm` **30 项**（顶层 154→135·零删除·journal `tmpe/.journal/20261019-031223-*.jsonl` 可 --undo）；② 删 `_trash/_edge_cdp_profile` **174.6MB/113 件**（Edge CDP 浏览器残留）；③ 删 `_inbox/hf-poc/hf-cache` **1.15GB**（HuggingFace 模型缓存·可重下）；④ `_shot` 实测**无 30 天前项**（38 项 1-7 天 / 25 项 7-30 天·合计 303MB）按原定规则 0 删。
> - **保留待作者定**：`tmpe/_inbox/hf-poc/data` **252MB**（10-14/15 的嵌入实验数据·chunks/corpus/page_vectors·全仓零引用）——近作且可能不可再生，未删；本批与近期目录（w795/w796/w797 及一个非本批 verify 目录）在 48h 冻结窗内保留。
> - **验证（全绿）**：pytest 629 passed / 3 skipped；ruff 0；verify 全量 50 段 0 FAIL；第 45 槽满足（docs/_templates 新增 duipai 子目录·index 自动生成）。
> - **状态**：已落地（级联+提交+推送按批次流程执行·PR #51 随批扩入）。
> - **文件**：docs/_templates/duipai/README.md、docs/_templates/duipai/duipai.py、docs/_templates/duipai/index.md、docs/_templates/README.md、docs/_templates/index.md、docs/10-方法论沉淀/批次交付流水线.md、docs/00-导读/W批次编号对账表.md、scripts/output/_w798_spec.json、scripts/output/_cascade_files_W798.txt

### W797（2026-10-19）：历史模板归档批
> **来源**：用户令「办」——四文件处置（三模板归档 + PRD 留本地），并附「还有哪些文件需要归档 / tmpe 要不要动」两问（答复见批后结论，本批只执行模板归档）。动工前 preflight PASS（W797 认领·零交集）。
> - **归馆（git mv 保全历史）**：`docs/_templates/{article-template,handoff-checklist,validation-checklist}.md` → `archive/docs/templates/`；新增馆藏 `README.md`——含退休依据（2026-08-11 对抗审查实测**采用率 0%**·证据指向 archive/scripts/batches/misc/）、出生证明（archive/docs/specs/2026-07-29-w205-w206 设计档）与后代载体（文档规范 §12）。
> - **现役化（内容不随馆藏消失）**：两清单的有效条目提炼为 **「交付自检（10 项）」入 `docs/00-导读/文档规范.md` §12**——含判据与执行方式、机器可判项（2/5/6/7/8/9）要求跑命令不以声明代替证据、处置规则（10/10 接收·任一项退回·≥3 项接手）。
> - **目录定位**：`docs/_templates/` 保留为**现役模板位**（README/index 由目录治理生成·当前 0 直属文件）；未来新模板在此新建，馆藏勿改。
> - **PRD 处置（不进馆·明确例外）**：`docs/_dev/产品管理套件应用-2026-10-02/03-PRD-第28门禁…` 为 gitignored 本地件，且 W650 已裁决「真名防泄漏出库」——`archive/` 在公开仓库内，入馆等于重新公开，**维持原地不动**。
> - **引用面修复（断链 26 处）**：docs/01-09 README、00-导读 README/项目说明、CONTRIBUTING 共 12 文件的模板链接统一改指 `文档规范` §12（相对路径按文件计算）；STRUCTURE `_templates/` 段更新为「现役模板位」；数量表述 8/6 项 → 10 项。
> - **引用面修复（断链 26 处）**：docs/01-09 README、00-导读 README/项目说明、CONTRIBUTING 共 12 文件的模板链接统一改指 `文档规范` §12（相对路径按文件计算）；STRUCTURE `_templates/` 段更新为「现役模板位」；数量表述 8/6 项 → 10 项。
> - **验证（全绿）**：git mv 识别为 rename（历史连续）；pytest 629 passed / 3 skipped；ruff 0；verify 全量 50 段 0 FAIL；第 45 槽（docs/_templates 留 README/index 仍满足）；docs_index --check 零差异（模板本不在 INDEX·718 篇不变）。
> - **状态**：已落地（级联+提交+推送按批次流程执行·PR #51 随批扩入）。
> - **文件**：archive/docs/templates/README.md、archive/docs/templates/article-template.md、archive/docs/templates/handoff-checklist.md、archive/docs/templates/validation-checklist.md、docs/00-导读/文档规范.md、docs/_templates/README.md、docs/_templates/index.md、docs/00-导读/W批次编号对账表.md、scripts/output/_w797_spec.json、scripts/output/_cascade_files_W797.txt

### W796（2026-10-19）：提示词库整理入库批
> **来源**：用户令「把这个文件内容整理进项目目录内」（附 `C:\Users\12739\Desktop\Prompt.txt`·966 行/47KB·提示词合集+任务清单+素材混排）。按上一轮分析稿的模块化建议落地，Q-01~Q-05 五项决策全部记录于总目录 §三。动工前 preflight PASS（W796 认领·零交集）。
> - **拆分（12 文件·03/04 原文照录·其余 9 篇润色·逐行映射入各文件头）**：`docs/12-提示词库/`——00 总目录（模块索引+冲突处理+决策记录）/01 参考链接（8 站点）/02 写作与输出规范（计划要求·三润色 skill·成果要素·回答风格）/03 工作复盘系统提示词（L29-465 全文）/04 任务执行系统提示词（L466-829 全文）/05 项目审查任务书（7 段合并 R-1~R-7）/06 隐私与开源边界（独立前置）/07 安全架构准则（6 域）/08 团队角色与分工/09 导师提问流程/10 创意写作四题/11 色彩素材。
> - **冲突处理**：① 色值 20 组逐条校准——4 组 RGB≠HEX（玫瑰粉差 225/象牙白 30/柠檬黄 30/樱花粉 100）**判定以 HEX 为准**（HEX 与色名语义一致率 4/4·RGB 按 HEX 重算并保留原值可溯）+ 1 组微差（芭比粉 9/通道）；② 7 段代码审查合并为一篇 R-1~R-7；③ 隐私边界从审查段中间独立成篇并前置（00 开篇声明 + 06）；④ L911 单行（plan-ceo-review/autoplan）性质不明照录加注。
> - **润色二稿（同批）**：按用户令 03/04 两篇系统提示词保持照录不润色；其余 9 篇结构化重排——**05 补全首稿被截断的 R-3~R-7 五段**、修两处笔误（「AI 率为 5% 一下」→「以下」/「安wsl全」→「安全隐患」）、01 补全后 5 条链接、08/09/10 转为表格与任务卡、11 补判定口径与使用注记；全部语义未改，修订清单入 00-总目录 §五。
> - **工程面**：`docs_index.py` SECTION_TITLES 增第 13 板块「12 · 提示词库」；STRUCTURE.md 增设 12 段条目；目录治理自动生成 `README.md`/`index.md`（第 45 槽 0 FAIL·168 目录）；docs/INDEX.md 重建 704→718 篇。
> - **性质声明**：本目录为**素材归档非任务清单**——执行其中任何任务须用户单独授权（提示词 ≠ 待办），该约定写入 00 总目录 §四。
> - **验证（全绿）**：pytest 629 passed / 3 skipped；ruff 0；verify 全量 50 段 0 FAIL；第 45 槽 0 FAIL；docs_index --check 与 stats --check 均零差异。
> - **状态**：已落地（级联+提交+推送按批次流程执行·PR #52 随批开出）。
> - **文件**：docs/12-提示词库/00-总目录.md、docs/12-提示词库/01-参考链接.md、docs/12-提示词库/02-写作与输出规范.md、docs/12-提示词库/03-工作复盘提示词.md、docs/12-提示词库/04-任务执行提示词.md、docs/12-提示词库/05-项目审查任务书.md、docs/12-提示词库/06-隐私与开源边界.md、docs/12-提示词库/07-安全架构准则.md、docs/12-提示词库/08-团队角色分工.md、docs/12-提示词库/09-导师提问流程.md、docs/12-提示词库/10-创意写作题.md、docs/12-提示词库/11-colors.md、scripts/docs_index.py、STRUCTURE.md、docs/00-导读/W批次编号对账表.md、scripts/output/_w796_spec.json、scripts/output/_cascade_files_W796.txt

### W795（2026-10-19）：第 42 篇复盘报告入库批
> **来源**：用户令「合并 PR #50 → 写复盘第 42 篇」。PR #50 已于 2026-10-18T17:34Z 合并（98f2cadb·dev 与 main 归零），本批为复盘报告入库。
> - **复盘范围**：2026-10-17 23:10 – 2026-10-19 01:10（约 26 小时）·W777-W794 十八段·39 提交（30d989e7→b341d39a）·**未断档**（上篇 Q-11 教训保持）。
> - **三条主线**：① 外部输入三段处置闭环——收编六批（W782-W787 对拍零漂移）→ 对盘驳回（W789·提案已被 W775 完全吸收·15 项全标记·7 处余量全驳）→ 重复投递识别（W790·第三轮七项全同）；② 「本地绿 CI 红」第三型——W791 better-sqlite3@13 engines>=22 vs CI Node 20 错配（EBADENGINE 非致命·运行时才炸）·修复三件套（job 升 22/engines 收紧/子进程输出捕获）；③ 探针防虚构被自身证伪——W793 探针 8/8 选择器全绿但 W794 撤回 F-08（低分辨率误读·选择器命中≠主张为真）。
> - **核心判定**：全仓待办核查（W792）无假收敛——32 项 Backlog + 12 份计划 + 25 条短期待办逐项取证，5 处陈滞全朝「实已完成未标注」安全方向；唯一结构性缺口（内容冻结适用范围）已于 W793 立单一权威表述。
> - **沉淀**：新经验 E-17~E-24（八条·四条来自自查自纠）·问题族 FAM-37~39（文档陈滞/低分辨率误判/CI 运行时不匹配）·工作流 WF-06 探针防虚构升级与 WF-07 陈滞巡检·改进项 P-42-01~05。
> - **验证（全绿）**：pytest 629 passed / 3 skipped；ruff 0；verify 全量 50 段 0 FAIL；三连带（README 行 24 / STRUCTURE 28 与现役 24 篇 / INDEX 704 篇 / stats 零差异）；PR #50 合并前终态全绿（28 检查零失败·截图审查与 Dark-state 双 success）。
> - **状态**：已落地（级联+提交+推送按批次流程执行·PR #51 随批开出）。
> - **文件**：docs/11-方案报告/工作复盘与优化分析报告/工作复盘与优化分析报告-2026-10-19.md、docs/11-方案报告/README.md、STRUCTURE.md、docs/00-导读/W批次编号对账表.md、scripts/output/_w795_spec.json、scripts/output/_cascade_files_W795.txt

### W794（2026-10-19）：PD-3 裁决落地批
> **来源**：用户令「按推荐办」——PD-3-A1/A2/A3 三项裁决全采纳落地 + 自查撤回 F-08 假阳性。动工前 preflight PASS（W794 认领·零交集）。
> - **A1 首页补 06**：`site/index.html` 九卷索引在 05 与 07 之间补 06 个人随笔行（链 `reader/essays/index.html`·「随笔集 · 44 篇个人视角的现代解读」），节名「九卷索引」→「**全卷索引**」、引言「九卷通读」→「全卷通读」——44 篇 A2 主体内容自此有首页入口，跳号困惑消除。
> - **A2 DATA 文案**：`site/dashboard.html` 提示条由「嵌入快照 · file:// 直接打开（如需最新数据，请在 site/ 目录运行 py -m http.server 8000）」改为「**数据已内置，离线可直接打开（file://）；最新数据以本地服务模式为准。**」——公网页不再出现开发命令，「离线可读」卖点保留。
> - **A3 数字串图例**：专题区引言加「数字为对应维度计数（悬停可看明细）」；**30 张多数字卡**（`7·8·15·5` 形态·与维度词数对齐）加 `title` 属性（如「势力 7 · 法宝 8 · 搬救兵 15 · 贝尔宾 5」·悬停与读屏可得）；11 张单值卡（「2 场」「100 回」自解释）按推荐跳过。
> - **自查撤回（诚实修正）**：F-08「主题/专题混用」系 50% 缩放截图低分辨率误读——HTML 实为「51 个专题页」、`grep 主题` 5 处全合法（目录名 docs/03-主题与情节专题/A4 计数/卡片描述）；报告 F-08 标注撤回（8 条初判→7 条有效）、§1 增「假阳性撤回」条并记方法债（探针只校验选择器不校验文字主张）、登记表 B-104 同步撤回。
> - **视觉基线**：`tests/e2e/baseline/index.png` 与 `dashboard.png` 同步更新（布局变更必同步）；其余 8 张经 `--update-baseline` 出现的渲染抖动一并回退（仅留必要两张）——对比模式 10/10 通过（最大抖动 0.086% < 0.5% 阈值）。
> - **验证（全绿）**：PD-3 探针 7/7 命中（F-08 撤回后）；视觉对比 10/10；pytest 629 passed / 3 skipped；ruff 0；verify 全量 50 段 0 FAIL。
> - **状态**：已落地（级联+提交+推送按批次流程执行·PR #50 随批扩入）。
> - **文件**：site/index.html、site/dashboard.html、tests/e2e/baseline/index.png、tests/e2e/baseline/dashboard.png、docs/superpowers/plans/2026-10-18-pd3-heuristic-review-report.md、docs/superpowers/plans/2026-09-30-maintenance-backlog-registry.md、docs/00-导读/W批次编号对账表.md、scripts/output/_w794_spec.json、scripts/output/_cascade_files_W794.txt

### W793（2026-10-18）：PD-3 走查与 BL-31 退休批
> **来源**：用户令「三项都按你说的办」——产品设计套件 PD-3 执行包（PD 档 §10 D-3 已批范围=2 页）+ BL-31 sync_docs 退休 + 冻结适用范围立句。动工前 preflight PASS（W793 认领·零交集）。
> - **PD-3 执行（交付物按 PD 档规格）**：Playwright 真实渲染 index+dashboard × {file,http} × {浅,暗} 8 张全页截图矩阵（pageerror 逐张 0·manifest 入库 scripts/output/pd3-capture-manifest.json·截图本体 tmpe gitignored 可一条命令再生）；Nielsen 十启发式 20 格全覆盖（2 格「不适用+理由」）；**8 条 finding（S1×0 / S2×3 / S3×5）全部经 `--report` 探针回真实 DOM 校验（AC-1 8/8 命中·防虚构，同第 20 门禁防幻觉引文族）**。
> - **发现摘要**：S2 三条——九卷索引 05→07 跳号且 06 个人随笔（44 篇）全页零入口；dashboard 同一节两套 A1-A6 计数（引言 615 体系 vs 卡片 Σ575）；页脚 v2.3.79 陈旧（v-号体系已随 W711 退役）。S3 五条——footer 批次链 2232 字符长文（W724 上限管条数未管条长）、搜索卡「772 篇」vs 索引实测 771 条、DATA 提示含开发指令、专题卡数字串无图例、主题/专题术语混用。分流=工程五条登记 B-100~B-104，内容三条列裁决项 PD-3-A1~A3。
> - **走查方法论**：低分辨率截图曾产生三处「疑似乱码」误读（搜索提示/DATA 介绍/人物关系卡），原尺寸回读均为正确正文——**探针纪律（先排除工艺伪影与低分辨率误读再下判）实录**；reveal-in 滚动显现导致的截图空白同理排除未记 finding。
> - **BL-31 退休（替换而非裸删）**：release.py step1 由 sync_docs 改为 check_doc_sync（`python scripts/release.py` 实跑 step1 PASS 实证）；删除 scripts/sync_docs.py；Makefile release 注释与 doc_areas.py 历史注记同步；checklist 三处旧命令改现役路径（check_doc_sync / stats --w）。理由=职责被第 31 门禁完全覆盖且更强（18 负样本）、它不在 CI、存量 exit=1 无人发现——死重量标准画像（W562/W776/W788 同款裁定）。
> - **冻结适用范围立句（W793 立·单一权威表述）**：写入 HANDOVER 阻塞段——内容扩容维持 W626 冻结（UV 数据链 2026-09-30 起中断·fetch_gate_stats 实测 404·API 恢复后重判）；点名解冻项已全收官；工程/治理/门禁批不受限；新增内容扩容须用户点名或 judge_gate 判「继续分发」。
> - **W792 报告自修**：PD 行「待批复」系初稿误判（§10 已于 W651 全批·PD-1/5 已执行），本批修正并记录——自查自纠同批留痕。
> - **验证（全绿）**：探针 AC-1 8/8 + AC-3 pageerror 0；第 42 槽 0 FAIL（基线顺带清 2 条陈腐豁免）；第 31 门禁 0 FAIL；release.py step1 PASS；pytest 629 passed / 3 skipped；ruff 0；verify 全量 50 段 0 FAIL。
> - **状态**：已落地（级联+提交+推送按批次流程执行·PR #50 随批扩入）。
> - **文件**：docs/superpowers/plans/2026-10-18-pd3-heuristic-review-report.md、scripts/_pd3_finding_probe.js、scripts/output/pd3-capture-manifest.json、scripts/release.py、scripts/doc_areas.py、Makefile、HANDOVER.md、docs/11-方案报告/全仓待办计划方案状态核查报告-2026-10-18.md、docs/superpowers/plans/2026-09-30-maintenance-backlog-registry.md、docs/00-导读/W批次编号对账表.md、scripts/output/_w793_spec.json、scripts/output/_cascade_files_W793.txt

### W792（2026-10-18）：全仓待办计划状态核查批
> **来源**：用户令「全面审查项目文件中记录的所有待办、计划、方案，逐项核对完成状态」。核查范围=HANDOVER 四区（阻塞段/候选清单/Backlog 32 项/短期待办 25 条）+ docs/superpowers/plans/ 12 份计划 + 需求侧 WP 队列 + S 卡拍板记录 + 维护登记表 B-1~B-7 + S4 投稿树；方法=commit/门禁实跑/产物存在性/计划自载状态行四方交叉，五分类（已完成/未完成/陈滞/需决策/冻结）。
> - **总判定：无假收敛**——未发现任何「宣称完成实际未做」项；5 处陈滞全部朝「实际已完成或条件已变而文档未更新」的安全方向，本批全部修正。
> - **已完成（分组）**：需求侧 WP-A~M 十三项全收官；BL 六项已闭（BL-20/21/22/23/24/29·其中 BL-22 实于 W711 收官而 HANDOVER 未标注）；短期待办 25 条全 [x]（抽查无假勾）；计划文件六份收官（需求侧/gate28/agents 分层/方案 D/W728 重构/EN i18n 快赢层）；维护登记表 B-1/B-2/B-3/B-7 已落地、B-5 聚合器先行已出（dataset/entities 两类）、B-6 第一步已闭（第 28 门禁+基线 344 行）。
> - **未完成（分组·附原因）**：BL-1~BL-19 十八项开面（登记不开工·六项作者裁决）；BL-26/27/28 机制层持续管理（不设关闭项）；BL-30/31/32 低优先残项；B-4 Three.js 懒加载（动态 import 未实施·defer+3D 独立预算已缓解）；B-5 扩字段+学术梯队；B-6 第二步 PNG/SVG 导出（引用组件 87 页在位·导出仅 4 页）；EN i18n 根治层；产品设计套件待用户批复；干扰治理 3 纪律项+两周日志（窗口至 10-28）；S2 外部平台分发与 S4 投稿动作（用户侧）；内容质量深化方向（W626 冻结适用范围待明确）；V1-V4 候选；S-17/18 排期项；复盘第 42 篇（节奏未触发）。
> - **陈滞修正（5 处·本批落地）**：① BL-22 补 ✅（version-space-inventory §七·W711 实证）；② W728 计划状态行「待执行」→ ✅（CHANGELOG W728 段实证）；③ 维护登记表状态回写（B-1/2/3/7 ✅·B-5/B-6 ◐·B-4 ☐）；④ EN i18n 状态行「待排期」→ 快赢层 ✅（G2 六页整改）；⑤ 候选清单需求侧配额加终止注（WP-A 判定+全 WP 收官实证·W790/W791）。
> - **需用户决策 4 项**：① 内容扩容冻结的当前适用范围（W626 归档 vs W651 解冻点名·建议单一权威表述写入阻塞段）；② 产品设计套件 §10 逐条批复；③ S4 投稿选刊与时点；④ BL-31 sync_docs 三选一。
> - **验证（全绿）**：stats --check 16 键零差异；docs_index --check 703 篇通过；pytest 630 passed / 3 skipped；ruff 0；verify 全量 50 段 0 FAIL。
> - **状态**：已落地（级联+提交+推送按批次流程执行·PR #50 随批扩入）。
> - **文件**：docs/11-方案报告/全仓待办计划方案状态核查报告-2026-10-18.md、HANDOVER.md、docs/superpowers/plans/2026-09-30-maintenance-backlog-registry.md、docs/superpowers/plans/2026-09-29-en-data-i18n-display-plan.md、docs/superpowers/plans/2026-10-13-code-refactor-w728.md、docs/00-导读/W批次编号对账表.md、scripts/output/_w792_spec.json、scripts/output/_cascade_files_W792.txt

### W791（2026-10-18）：agent-web 攻击面负向测试批
> **来源**：用户令「①+②」——BL-29（三轮外部评审唯一实质增量：agent-web 攻击面负向测试缺口）主工 + 需求侧计划状态收尾搭车。动工前 preflight PASS（W791 认领·与在途零交集）。
> - **攻击面重映射（按真实防护模型·非按评审想象）**：① 「CORS 预检绕过」→ agent-web 无 CORS 中间件（防护模型=loopback 绑定+可选 AGENT_WEB_TOKEN+限流），对应面=token 鉴权负样本+权限模式白名单+cwd 钳制；② 「SSE 超时未清理」→ 守卫四路径单测（超时/断开/幂等/clearTimer）；③ 「超大 RAG top_k」→ agent-web 无此参数（检索为 grep 工具·钳制在 Python 侧 scripts/rag/rag_server.py·W412），映射说明已入 W790 回应报告。
> - **提取（行为逐字保留）**：index.ts 三处安全逻辑（sanitizePermissionMode/cwd 钳制/SSE 守卫）迁移至新模块 server/security.ts（14 增 54 删·CRLF 行尾纯净·git diff 无整文件翻动）；顺修 W568 漏改——正常完成/异常路径的 `req.off` 注销侧修正为 `res.off`（监听注册在 res·原注销从未生效·每请求泄漏一个 close 监听）。
> - **测试（新增 17 例·全套 67/67 过）**：权限净化 4 + cwd 钳制 6 + SSE 守卫 5（单测）+ 真实起服集成 2（限流第 31 次请求 429·token 无头/错头 401 与 x-agent-token/Authorization 双正确头式 200·spawn 范式沿用 feedback.test.mjs）；接入 package.json test:server（CI agent-web-build job 既有接线·test_ci_wiring 包含性断言不破·tsc -b 零错误）。
> - **搭车（计划状态收尾）**：需求侧主计划状态表 WP-D2/WP-E 由「待执行」回写 ✅（W659-W667 六批全关/W669·对账表实证·陈表系 W651 时点未更新）+ 计划头状态改「已全部收官」+ HANDOVER BL-23/24 关闭标注（AGENTS 脚注归档与分层拆分均已于 W709 落地·滚动机制常驻）。
> - **验证（全绿）**：agent-web test:server 67/67（约 4 秒）+ tsc -b 零错误 + pytest 630 passed / 3 skipped + ruff 0 + verify 全量 50 段 0 FAIL。
> - **状态**：已落地（级联+提交+推送按批次流程执行·PR #50 随批扩入）。
> - **文件**：xiyouji-agent-web/server/security.ts、xiyouji-agent-web/server/security.test.ts、xiyouji-agent-web/server/index.ts、xiyouji-agent-web/package.json、docs/superpowers/plans/2026-09-21-demand-side-optimization-master-plan.md、HANDOVER.md、docs/00-导读/W批次编号对账表.md、scripts/output/_w791_spec.json、scripts/output/_cascade_files_W791.txt

### W790（2026-10-18）：外部评审第三轮回应登记批
> **来源**：用户令「b」——外部评审第三轮（同一评审者·七项工程核查 + 末尾索要四项源码）回应登记。判定路径=对盘核验（CI 安装路径/门禁 severity 分布/视觉基线计数/agent-web 测试关键词扫描/覆盖率配置/脚本注册表/sync_docs 接线状态全量实测）+ 上轮报告（2026-10-17·W775）逐条比对。
> - **重复投递认定**：七项与上轮全同（依赖锁定/门禁数字/视觉回归/agent-web/覆盖率/脚本膨胀/sync_docs），末尾索要四项文件同一；间隔 15 批次（W775→W790）事实已漂移——门禁 44→50 槽、覆盖率项由 W776 决策关闭、归档脚本 45 个数字本轮属实。
> - **裁定：4 项不成立**——① 依赖锁定：CI 三处安装全锁（pip -r 钉版 + npm ci ×2·lockfile 在库），审计对象是锁定清单非浮动快照；② 门禁数字：现势 50 槽、severity 机制在但当前无 warn 级、无 warn-only 模式，内容/数据语义层硬门禁 8 项可枚举；⑤ 覆盖率：.coveragerc/fail_under 不存在，「配置了没生效」陷阱无从触发，W776 口径决策全文在 pytest.ini；⑥ 脚本注册表：script-coverage-baseline 43 条四分类 + 第 42 门禁机器强制（无引用未登记即 FAIL）。
> - **裁定：3 项部分成立**——③ 视觉回归：10/87 像素基线属实，但三层分工已建（10 关键页像素 + 87 页第 43 门禁语义断言 + 857 页截图审查），基线更新为手工命令·CI 不自动吞；④ agent-web：38 个 node --test 用例接 CI（tools 26/audit 7/citationGuard 5），但点名三类负向测试不存在；⑦ sync_docs：半退役脚本（校验器·非 CI 接线·仅 Makefile release·存量 exit=1·无单测），活跃同职责门禁 check_doc_sync 有 18 负样本。
> - **唯一实质增量**：agent-web 攻击面负向测试缺口（CORS 预检绕过/超大 RAG top_k/SSE 超时未清理·W411/W412 修复无回归固化）→ 登记 BL-29；另登记 BL-30（E2E playwright 浮动钉版 + 根级依赖指针）、BL-31（sync_docs 状态处置三选一）、BL-32（截图审查触发粒度）。
> - **交付**：回应报告归档 docs/11-方案报告/外部评审回应与逐项核查报告-2026-10-18.md（七节体例对齐上轮）+ 三连带（README 索引行 22 / STRUCTURE 现役报告 21→22 篇 / stats report_docs 25→26）+ docs/INDEX.md 重建 701→702 篇 + HANDOVER BL-29~32。
> - **验证（全绿）**：stats --check 16 键零差异；docs_index --check 通过；pytest 630 passed / 3 skipped；ruff 0；verify 全量 50 段 0 FAIL（含第 17 索引健康/第 31 C5d stats 对账/第 45 目录文档）。
> - **状态**：已落地（级联+提交+推送按批次流程执行·PR #50 随批更新）。
> - **文件**：docs/11-方案报告/外部评审回应与逐项核查报告-2026-10-18.md、HANDOVER.md、docs/11-方案报告/README.md、STRUCTURE.md、scripts/output/stats.json、docs/INDEX.md、docs/00-导读/W批次编号对账表.md、scripts/output/_w790_spec.json、scripts/output/_cascade_files_W790.txt

### W789（2026-10-18）：外部门禁重构提案对盘登记批
> **来源**：用户转发外部重构产出（三 gate 脚本 + 两公共模块「完整重构版本」·其自带批次编号未登记于对账表·外部异体系）。按流水线 §七 外部产出落地流程对盘：五文件逐字节提取并 round-trip 语法自检，与磁盘现势做 CRLF 归一 diff，15 项改动清单全标记核查。动工前 preflight PASS（W789 认领·与在途 W750/W764 零交集）。
> - **裁定：不执行（提案已被 W775 完全吸收）**——提案 15 项改动（probeInPage/judgeProbe/checkPage/jsLiteralToJson/main 拆分、常量化、v4NearMissPct 去重、BENIGN_CONSOLE_RE 死代码删除、命名规范化、基线检查合并、模式分发函数化、use strict、JSDoc）经逐字节 diff + 全标记核查证实已 100% 落地于磁盘现势（HEAD 7fabdd2c·W788 收官态·工作树干净）；提案与磁盘仅剩 7 处差异且全部驳回。
> - **驳回项①（改号）**：两公共模块 docstring 由 W775 改为外部自带编号——未登记 W### 入仓即造编号黑洞（C4 镜像拦·W724 同族），且断 W775 溯源链。
> - **驳回项②（回退 W788）**：playwright_gate_utils 提案版带回 const path 死导入、check_screenshot_gates 提案版带回 GATE_NAME 死常量——均系 W788 刚删除的无消费点代码，落回即回退上一批清理成果。
> - **驳回项③（正则腐蚀）**：check_data_drift 提案版尾逗号正则缺反斜杠（磁盘 od 实证为 W775 验证态）——W775 引号腐蚀同款症候，按提案落地将令含双逗号的内嵌块静默跳过、可比页数缩水。
> - **驳回项④（等价噪声）**：utf-8/utf8 与 } })()/})() 两组写法 Node 行为完全等价，零收益 churn（W787 同款裁定）。
> - **驳回项⑤（契约相悖）**：check_chart_values 提案版 buildReport 增 pathPointsTotal 报告字段——与提案自述「报告 JSON 字段名不变」相悖，且消费方 test_visualization_data.py 在盯，属交付阻断面无收益改动。
> - **现势健康验证（全绿·兼作已落地实证）**：第 43 门禁 self-test 12/12 exit 0；check_data_drift 全量 exit 0（可比 59 页·150 个 JSON 对比项·W775 引号腐蚀修复覆盖仍在）；chart_values gate 子集（tag-cloud+chapter-stats）0 FAIL；screenshot gate 子集 FAIL 0；pytest 630 passed / 3 skipped；ruff scripts/ 0。
> - **防重复收编**：本批即登记目的——证据（五份 diff + 五份逐字节提取件 + 健康快照）留存 tmpe 临时区（gitignored）；未来会话收到同族提案应先 diff 对盘勿直接落地（流水线 §七 红线）。
> - **状态**：登记批（零代码变更·施工前后 HEAD 不变）；级联+提交+推送按批次流程执行。
> - **文件**：CHANGELOG.md、docs/00-导读/W批次编号对账表.md、scripts/output/file-index.md、scripts/output/_w789_spec.json、scripts/output/_cascade_files_W789.txt

### W788（2026-10-18）：JS 门禁死代码清理批
> **来源**：W775 重构收尾（用户令「B」）——W775 落地批的独立验证中，Lead 与 provenance 复核共同确认两处残余死代码：一处是 W775 **新增**的死常量（非历史遗留），一处是**从落笔起就未使用**的导入。两处均属 W787「门禁脚本停止 churn」裁定之后新增的可读性瑕疵，本批以最小改动（净删 2 行）清理。动工前 preflight PASS（W788 认领·与在途 W750/W764 零交集）。
> - **改动 1**：`scripts/check_screenshot_gates.js` 删 `const GATE_NAME = 'screenshot-gates';`——该常量定义后全文件零引用（`Select-String -SimpleMatch GATE_NAME` 命中 1 = 仅定义行）。**为何是死代码**：本门禁无 `---- N FAIL ----` 汇总末行（唯一汇总行是 `[chart-gates] done in … FAIL N`），且不在 verify_delivery 45 槽内，CI 靠 `process.exit(bad.length?1:0)` 的**进程退出码**判定（`.github/workflows/screenshot-review.yml` 以 `nick-fields/retry` 包裹 + Summarize 段取 step outcome、不解析末行）——即 GATE_NAME 系 W775 照抄第 43 槽「汇总末行」模式时的**机械迁移残留**，本门禁并不需要它。反讽点：同一提交既删了旧死代码 `BENIGN_CONSOLE_RE`（T1 宣称属实·实测 pre=1/cur=0），又新增了此常量。
> - **改动 2**：`scripts/lib/playwright_gate_utils.js` 删 `const path = require('path');`——文件内零 `path.` 消费（`\bpath\b` 命中 1 = 仅 require 行）；该模块四导出（DEFAULT_VIEWPORT/launchHeadlessBrowser/createOfflinePage/gotoFileUrl）本不含 path，删后导出面不变。该文件由 W775 全量新增，故属**原生瑕疵**而非历史遗留。
> - **零行为变化论证**：两处均无任何消费点（源码 grep + 下游引用 + 行号脆弱断言三项核查），不动判据/阈值/消息文本/退出码。
> - **三态核验（W787 立的标准）**：① **干净态**——截图门禁全量 857 页 · FAIL 0 · exit 0，与改动前逐页 `fails` 比对（排序归一 worker 完成序，流水线 §八固有抖动）**857/857 完全相同**；② **破防态**——本门禁无 self-test 且无注入入口，故以同口径直接驱动判据函数 + 真实浏览器打开 `$env:TEMP` 临时缺陷页，注入 pageerror → G1 红、4000px 溢出 → G3 红（+2720px）、干净页对照 → 绿，3/3 通过（证明删常量未删出假绿）；③ **self-test**——第 43 槽 `--self-test` 12/12 通过 · exit 0。
> - **回归面**：pytest 630 passed / 3 skipped（`test_visualization_data.py` 18/18 单独复跑通过——全量连跑时该文件被 harness 中断，属环境抖动而非失败）；verify_delivery 全量 50 段核心全过。
> - **行尾与字节保真**：两文件删行后仍为纯 CRLF、无 BOM、无混行尾（HEAD blob 为 LF，`core.autocrlf=true` 下常规 add 即可，无 W553 翻转风险）；`git diff --numstat` 为 `0 1` / `0 1`（纯删除行，非整文件翻动）。
> - **不修清单的处置**：W775 验证中另发现两处**行为等价**差异（`pageerror` 统一 `.slice(0,300)` 截断、`gotoFileUrl` 默认参为死参数）——前者经全下游核查确认无行为影响（G1 只读 `.length`，`chart-gates.json` 全仓无消费者），后者属公共模块签名语义，两者均**不在本批范围**，留待下次因其他原因必改该模块的批次作伴随清理。
> - **状态**：已落地（三态核验全绿）；级联+提交+推送按批次流程执行。
> - **文件**：scripts/check_screenshot_gates.js、scripts/lib/playwright_gate_utils.js、docs/00-导读/W批次编号对账表.md、CHANGELOG.md、scripts/output/file-index.md、scripts/output/_w788_spec.json、scripts/output/_cascade_files_W788.txt

### W787（2026-10-18）：release.py 行为保持重构批
> **来源**：外部重构提案收编第六批（末批·用户令「全部做完之后合并」）。动工前 preflight PASS（W787 认领·零交集）。
> - **release.py**：_STEP_SEPARATOR/_REPO_SIZE_WARN_MB/_LOOSE_OBJECTS_WARN/_CHANGELOG_VERSION_RE 常量化（正则提模块级预编译·import re 随之上移）；step2 拆 _check_uncommitted/_check_unpushed；step3 拆 _parse_count_objects；main 版本解析提 _resolve_target_version；新增 _print_step_header 供步骤 2-5 复用（**步骤 1 保持独立实现**——原输出无前置空行·避免引入空行差异）；五步输出文本/前缀/短路顺序/退出码逐字保留。
> - **22 项门禁脚本改动点清单：裁定不执行**（工程裁定非遗漏）——① 交付阻断面：门禁脚本 FAIL 语义即发布闸门，W781 刚完成 verify 体系收口（注册表派生+启动期断言+锁反向查），连续 churn 违背「谨慎」本意；② 清单自身标注多数文件「已足够简洁」或「已做过 W730/W733/W761 拆分」；③ 其可证伪发现 5 项中 3 项经对盘系 W775 前旧快照（W780 已核）。未来如做：须逐门禁三态核验（干净/破防/self-test 输出与退出码逐字比对）+ 流水线 §八五维对拍。
> - **对拍（流水线 §八）**：完整运行前后各一轮，stdout 全文与退出码（存量 exit=1·sync_docs 一致性检查为存量失败态·与重构无关）**逐字相同**；pytest 630 passed；ruff 0；verify 全量 0 FAIL。
> - **状态**：已落地（对拍全绿）；级联+提交+推送按批次流程执行。
> - **文件**：scripts/release.py、docs/00-导读/W批次编号对账表.md、CHANGELOG.md、scripts/output/file-index.md、scripts/output/_w787_spec.json、scripts/output/_cascade_files_W787.txt

### W786（2026-10-18）：graph_seed_neo4j 行为保持重构批
> **来源**：外部重构提案收编第五批（用户令「全部做完之后合并」）。动工前 preflight PASS（W786 认领·零交集）。
> - **graph_seed_neo4j**：Cypher 拼装提 _build_cypher（纯字符串拼接·逐行字节稳定）；快照组装提 _build_snapshot；_OUTPUT 中间变量收敛路径拼接；Cypher 各行/json.dump 参数/_w536_guard_open 调用/日志文本逐字保留。
> - **rag 家族其余五件不收（工程裁定·与 character_nlp 同款原则）**：build_vectors（GPU 温度守护与断点续跑管线）、page_router（模型加载评测面）、rag_server（运行时服务）、rag_enhance（LLM 端点回退路径）、xiyouji_rag（800 行核心引擎）——重运行时对拍面+累计约 2100 行转录风险；对拍可行段（确定性产物 diff）无法覆盖其风险面（温度守护/断点/端点回退），留机械通道。
> - **对拍（流水线 §八）**：前后各一轮，rag_graph.json/neo4j_seed.cypher/运行日志**全部逐字节相等**；pytest 630 passed；ruff 0；verify 全量 0 FAIL。
> - **状态**：已落地（对拍全绿）；级联+提交+推送按批次流程执行。
> - **文件**：scripts/rag/graph_seed_neo4j.py、docs/00-导读/W批次编号对账表.md、CHANGELOG.md、scripts/output/file-index.md、scripts/output/_w786_spec.json、scripts/output/_cascade_files_W786.txt

### W785（2026-10-18）：api_server 行为保持重构批
> **来源**：外部重构提案收编第四批（重件档其一·用户令「全部做完之后合并」）。动工前 preflight PASS。
> - **常量提级**：_CORS_FILE_ORIGIN/_CORS_LOCAL_ORIGINS/_CORS_RESPONSE_ORIGIN（W681 回显常量防头注入语义保留）、_MIME_TYPES（自 _ctype 内联字典）、_SNIPPET_BEFORE/_SNIPPET_AFTER/_HITS_PER_DATASET_LIMIT。
> - **路由拆臂**：do_GET 拆 _handle_openapi/_handle_search/_handle_graph/_handle_dataset/_serve_static；新增 _send_error_json 统一 {error[,try]} 结构（响应体字段与嵌套不变）；文档页表格行渲染提 _render_dataset_row。
> - **逐字保留**：全部路由路径、状态码（200/400/404）、CORS 白名单判定、_resolve_static 的 startswith 边界、_recursive_search 片段窗口与省略号、openapi version v2.2.92、启动/停止日志；W337/W339/W681/P3-2 溯源保留。
> - **对拍（流水线 §八）**：起服务前后各一轮，11 个端点工件（health/datasets/openapi/search 火焰山/graph/graph_yuanqi/keys/CORS 头/404 状态/doc 页/服务日志）10 个逐字节相等，cors.txt 漂移经 diff 定性为 **HTTP Date 响应头时钟字段**（剥除后逐字节相同 908a1406）——§八抖动归一；pytest 630 passed；ruff scripts/api/ 0；verify 全量 0 FAIL。
> - **状态**：已落地（对拍全绿）；级联+提交+推送按批次流程执行。
> - **文件**：scripts/api/api_server.py、docs/00-导读/W批次编号对账表.md、CHANGELOG.md、scripts/output/file-index.md、scripts/output/_w785_spec.json、scripts/output/_cascade_files_W785.txt

### W784（2026-10-18）：分析与审计五小件行为保持重构批
> **来源**：外部重构提案收编第三批（小件档·用户令「全部做完之后合并」）。动工前 preflight PASS（W784 认领·零交集）。
> - **chapter_stats**：诗词计数拆 _count_poem_headers/_count_aligned_poem_blocks（阈值提 _POEM_CONSECUTIVE_THRESHOLD）；中文计数/占比提 _count_chinese_chars/_dialogue_ratio；聚合提 _aggregate_totals（键顺序保持·per_chapter 仍追加末尾）。
> - **word_frequency**：token 过滤提 _is_valid_token+_MIN_TOKEN_LENGTH；结果构造提 _build_frequency_result；DEFAULT_STOPWORDS 保持 set 不改 frozenset。
> - **narrative_experiment**：四份 JSON 写出拆 _write_json/_write_all_outputs、控制台汇总拆 _print_summary；build_summary 由两次调用改一次复用（确定性数据·结果不变）；三数据块逐字保留。
> - **hardships_81**：三标签字典提模块级（CAUSE/ENDING/DIFFICULTY_LABELS）；交叉统计拆 _build_cross_cause_ending、label 化拆 _relabel_hardships（W770/W760-F-2 溯源保留）；输出拆 _write_json/_write_all_outputs/_print_category/_print_summary；Counter.most_common 键序保留。
> - **line_check**：self_test 拆 _self_test_corpus_ok/_self_test_positive_samples/_self_test_negative_sample；查询分支提 _query_one/_parse_chapter_num；_TOTAL_CHAPTERS 替代三处裸 100；全部输出串与退出码逐字保留。
> - **对拍（流水线 §八）**：五脚本前后各一轮，11 个产物（chapter_stats/word_freq/ne 四件/h81 四件/line_check 自检输出含退出码与样本查询）**全部逐字节相等**；pytest 630 passed；ruff 四目录 0；verify 全量 0 FAIL。
> - **状态**：已落地（对拍全绿）；级联+提交+推送按批次流程执行。
> - **文件**：scripts/A_文本基础/chapter_stats.py、scripts/A_文本基础/word_frequency.py、scripts/AA_叙事实验/narrative_experiment.py、scripts/C_情节/hardships_81.py、scripts/audit/line_check.py、docs/00-导读/W批次编号对账表.md、CHANGELOG.md、scripts/output/file-index.md、scripts/output/_w784_spec.json、scripts/output/_cascade_files_W784.txt

### W783（2026-10-18）：B_人物行为保持重构批
> **来源**：外部重构提案收编第二批（用户令「做」）。动工前 preflight PASS（W783 认领·零交集）。
> - **character_appearance**：aggregate 内排行榜/矩阵/前端契约字段三段拆 _build_ranking/_build_matrix/_build_characters_out；first_chapter 计算提 _resolve_first_chapter 并**显式保住字面值先求值语义**（与原 dict.get 默认参数急切求值一致·防 first_appear 数据完整性判断静默变化）；正则提 _CHAPTER_NUM_RE；W643/W678/W565 溯源注释逐字保留。
> - **character_network**：单回共现累积拆 _accumulate_chapter；嵌套循环改 itertools.combinations（pair 键 tuple(sorted()) 等价）；节点/边结构与排序键逐字保留。
> - **character_nlp 不收**：提案整文件重写约千行，转录落地风险大于可读性收益；W101/W102 上下文排除规则与 W691 追踪集属密缘导管且无自动对拍面（run_all 各类仅执行目录首脚本·B 类=__init__.py·nlp 不在自动回归面）——留待机械通道（直接以文档驱动 apply+五产物 diff 的执行方式）。
> - **对拍（流水线 §八）**：两脚本全量前后各一轮，输出 character_appearance.json（89KB）/character_network.json（38KB）**逐字节相等**；pytest 630 passed；ruff scripts/ 全目录 0；verify 全量 0 FAIL。
> - **状态**：已落地（对拍全绿）；级联+提交+推送按批次流程执行。
> - **文件**：scripts/B_人物/character_appearance.py、scripts/B_人物/character_network.py、docs/00-导读/W批次编号对账表.md、CHANGELOG.md、scripts/output/file-index.md、scripts/output/_w783_spec.json、scripts/output/_cascade_files_W783.txt

### W782（2026-10-18）：utils 与 run_all 行为保持重构批
> **来源**：外部重构提案收编第一批（用户令「做」·全文 21938 行含约 30 文件重构方案与三轮项目批评·经对盘核实分档：JS 门禁部分 W775 已执行、5 项裁决发现 3 项旧快照、utils 与分析脚本部分仍然有效）。动工前 preflight PASS（W782 认领·零交集）。
> - **aliases**：global 手动懒加载改 lru_cache(maxsize=1)+setdefault；_build_reverse_index 更名 _alias_to_canonical（测试仅钉公开 API·改名安全已实证）；docstring 按盘面现实改写（提案「未来 character_nlp 应迁移」已过时·盘上三脚本早已 import 本表；过时「35 位」表述一并清除）；40 人物数据逐字保留。
> - **text_loader**：编码候选提 _ENCODING_CANDIDATES、标点集提 _PUNCTUATION_CHARS；load_text/load_chapter/load_all_chapters 内联逻辑拆 _read_with_fallback_encoding/_resolve_chapter_path/_collect_chapter_files；W563 溯源保留。
> - **analyzer_base**：_PROJECT_ROOT/_DEFAULT_CHAPTERS_DIR 提模块级；argparse 构建/输入路径解析/1 参 2 参兼容/写 JSON 拆 _build_arg_parser/_resolve_input_path/_invoke_analyze/_write_json；错误消息与日志前缀逐字保留。
> - **run_all**：300 提 SCRIPT_TIMEOUT_SECONDS（超时消息 f-string 动态拼接·文本不变）；过滤/执行/汇总拆 _parse_category_filter/_filter_scripts/_print_dry_run/_execute_scripts/_print_summary；退出码语义不变。
> - **path_guard 跳过**：其文件头自述「对账面·禁改写」，提案亦仅动 docstring 排版——零收益触碰面，不收。
> - **对拍（流水线 §八）**：run_all 全量 34/34 PASS 前后两轮；138 个输出产物 132 个逐字节相等；6 个 *_summary.json 漂移经三连实验定性为**存量无种子随机**（生成器类示例组合·同码连续两跑即不同·新旧 utils 四象限实验同判）——§八差异判定规则一「抖动归一」，与重构无关；stdout 逐行 diff 为空；aliases 新旧字典/反向映射/全别名解析行为经 importlib 双载逐项断言相等；pytest 630 passed / ruff scripts/ 全目录 0 / verify 全量 0 FAIL。
> - **状态**：已落地（对拍全绿）；级联+提交+推送按批次流程执行。
> - **文件**：scripts/utils/aliases.py、scripts/utils/text_loader.py、scripts/utils/analyzer_base.py、scripts/utils/__init__.py、scripts/run_all.py、docs/00-导读/W批次编号对账表.md、CHANGELOG.md、scripts/output/file-index.md、scripts/output/_w782_spec.json、scripts/output/_cascade_files_W782.txt

### W781（2026-10-18）：门禁防线收口批
> **来源**：用户令「1 to 2 to 3」三收口（复盘遗留改进菜单第一档两项+第二档一项·仿 W773 WS 多项一批先例）。动工前 preflight PASS（W781 认领·零交集）。
> - **R-1 挂槽注册表派生（verify_delivery）**：_GATE_SUMMARY_MARKERS 手工字典（20 条）删除，改由 _STRICT_GATES 元组派生（开发期对拍逐项相等零漂移）——挂槽手工面自五处收敛为两处（门禁元组+EXPECTED_SECTION_NAMES 顺序表）；新增 _assert_registry_consistent() 启动期四查（段名重复/元组段名缺顺序表/相对序漂移/scope 未覆盖段须显式登记 _FULL_ONLY_SECTIONS）、main() 入口调用，漏改启动期即红不再等 CI；段自洽锁补反向查（实跑多出声明外段即红·旧单向查放行实证=W780 第 45 槽漏 EXPECTED 顺序表而锁恒绿）+「实跑数」改打印真实 sections_ran 数；EXPECTED 顺序表补「目录文档」段名（50 段校数·W780 遗留盲区根治）；tests/unit/test_verify_registry.py 8 例（常态全绿+四查各负样本+锁双向）。
> - **R-2 spec desc 防线前移**：release_prep.check_fields 增 desc/head_sentence 禁以 W### 开头判据（W779 页脚双 token 根因在 spec 以 W779 领衔·W724 防线只能下一批级联时拦截——本次前移到 spec 时点）；batch_cascade._face_footers 插入前防御性剥离前导批次号（存量坏 spec 双保险）；test_release_prep 增 2 负样本。
> - **R-3 第 22 门禁转正**：check_governance_docs 命中即 exit 1 本就具备，2026-08-18 WARN 起步策略两月监测期满·转正时点 0 告警零成本切换——verify 治理契约段去 severity=warn（FAIL 阻断）；gates.md 第 22 条转正记录；脚本 docstring 同步。
> - **文档面**：gates.md 第 22 条转正 + pitfalls W698 scope 条目就地增补 R-1 演进（挂槽五处收敛两处+双实证）。
> - **验证（全绿）**：pytest 630 passed / 3 skipped / 0 failed（新增 10 例）；ruff 0；verify 三 scope——full 50 段 0 FAIL（自洽锁实跑==声明·含反向查）+docs/site 档除 C4-f 未提交残留（提交即消解）外零红；开发期派生注册表与手工字典逐项对拍相等；R-2 判据 live 负样本经单测断言。
> - **状态**：已落地（本地全绿）；级联+提交+推送按批次流程执行（dev 合 main PR 随批开出·合并留用户决策）。
> - **文件**：scripts/verify_delivery.py、scripts/release_prep.py、scripts/batch_cascade.py、scripts/check_governance_docs.py、docs/agent/gates.md、docs/agent/pitfalls.md、tests/unit/test_verify_registry.py、tests/unit/test_release_prep.py、tests/unit/index.md、tests/unit/README.md、docs/00-导读/W批次编号对账表.md、CHANGELOG.md、scripts/output/file-index.md、scripts/output/_w781_spec.json、scripts/output/_cascade_files_W781.txt

### W780（2026-10-18）：目录文档新鲜度门禁批
> **来源**：用户令「那你来做」——第 41 篇复盘报告「门禁自建即自曝」防线的延伸：把 W779 落地即登记的生成物漂移面（index.md 为生成时点快照·目录增删后清单过期且无机器防线）收进门禁。动工前 preflight PASS（W780 认领·零交集）；开工前接管另一会话的 W779 收尾（chore 571bb9f1 对账表 hash 回填 + W780 现势预留）。
> - **第 45 槽 check_folder_docs.py 挂载（--gate·timeout 240·目录文档段）**：全仓在管目录（gen_folder_docs@W779 口径·实测 167 目录）的「index.md 逐文件清单 ↔ 磁盘实况」对拍——C1 index/README 两件套在位 / C2 子目录清单（成员+计数）/ C3 文件清单（跨分组成员并集+计数）/ C4 H1 标题==目录名；漂移差异名直接进 FAIL 行（盘上多/文档多·各列前 5）；README 正文豁免（数字声明带「生成时点」时点限定·非现役谎报·文档规范 §4.9 形态）。
> - **单一事实源模块化（gen_folder_docs.py）**：GOVERNED_SKIP 自 main() 局部量提升模块级 + 新增 in_scope()（生成器主循环与门禁共用判定·生成器改口径门禁自动跟随）；新增 case_collides()（目录含 INDEX.md 等大小写变体即全模式跳过·os.listdir 真名小写判定两平台同构）——W780 门禁首跑实证 docs/ 目录分歧形态：Windows 把 INDEX.md 当 index.md 读到异构内容报 C2、Linux 会报 C1 缺件，同一目录两平台两种红法，根因即生成器 NTFS 覆写守卫只活了 Windows 判重路径。
> - **修复路径闭环（--refresh）**：门禁修复提示「重跑生成器」在默认模式不可达（跳过已存在件·刷不了陈旧清单），--force 则会误轰根 README.md 等人工维护档——新增 --refresh 安全刷新：按「生成来源：gen_folder_docs.py」元信息标记判所有权，仅重写生成物、人工维护件自动跳过（HAND 报告）。本批实测：3 目录 6 生成物刷新（scripts 死名单 5 项系另一会话施工期临时调试脚本已删、级联清单与测试文件各 1 项），6 人工维护件 HAND 跳过（mcp-server/scripts 根/packaging/site-en/agent-web 等 README 族）。
> - **门禁首跑自证（建 gate 即自我实证·W777 复盘 E 族教训）**：真仓首跑抓 4 处漂移（3 处真实清单漂移 + 1 处 docs/ 大小写跨平台分歧）——修复后 0 FAIL；--self-test 7 例注入式（1 正 6 负：fresh/增文件/删文件/增子目录/缺件/手改清单/H1 漂移）全过。
> - **跨平台纪律（pitfalls「latent 三问 + 双平台断言禁例」合规）**：全部比对基于名字符串（sorted(str) 码点序两平台一致）·零 os.name/盘符/大小写语义断言；负样本用系统临时目录合成树（两平台同构·不触仓库）；测试内先打 ROOT 补丁再调生成器（跨盘 relpath 会炸·C 盘临时目录 vs D 盘仓库根实测）。
> - **三方槽位同步**：verify_delivery 第 45 槽注册（_StrictGate·目录文档段·校数注释 38 委托/49 段按实跑回写）+ gates.md（全量定义第 45 条 + 组头 27-41→27-45 + 速查表 27-42→27-45——43/44 槽挂载时漏更的存量漂移顺修 + 标题 44→45 槽）+ AGENTS §4.2（阅读契约 45 条/本节 45 槽摘要/内含 45 槽/组头 27-45/新增条目 45）+ scripts/output/stats.json gate_count 44→45（--w W780·复查零漂移 16 键）。
> - **页脚双 token 顺修（W779 存量缺陷·W724 防线 fail-closed 拦截）**：W779 级联时 spec desc 以「W779」开头，四个 site 页脚链被叠插为「W779 W779…」且 index 与 dukou 两页为**整条目双份**——本批级联 dry-run 被 W724 页脚 token 重复防线当场拦截，顺修四页（删重一份整条目/折叠相邻双 token）后链恢复唯一 token，W780 方能入链；该缺陷随 W779 已提交上线（CI 无页脚链防线·级联时点防线本次首立功）。
> - **验证（全绿）**：pytest 620 passed / 3 skipped / 0 failed（新增 tests/unit/test_folder_docs_gate.py 16 例：合成树断言 9 + 大小写判定 + refresh 修复生成物 + refresh 保护人工件 + CLI 自测退出码 + round-trip 解析 + in_scope 豁免 + 漂移修复路径）；ruff 0；verify 全量 49 段 0 FAIL（第 45 槽在列·段自洽锁实跑==声明）；gen --dry-run 幂等（0 待写）；W779 推送 CI 全绿（五工作流含 Lighthouse 与截图审查）。
> - **状态**：已落地（本地全绿）；级联+提交+推送按批次流程执行（main 合并留待用户决策）。
> - **文件**：scripts/check_folder_docs.py、scripts/gen_folder_docs.py、scripts/verify_delivery.py、tests/unit/test_folder_docs_gate.py、docs/agent/gates.md、AGENTS.md、docs/00-导读/W批次编号对账表.md、scripts/index.md、scripts/output/index.md、scripts/output/README.md、tests/unit/index.md、tests/unit/README.md、scripts/output/stats.json、site/index.html、site/dukou-engine.html、site/data/cross-time-danmaku.html、site/data/tag-cloud.html、CHANGELOG.md、scripts/output/file-index.md、scripts/output/_w780_spec.json、scripts/output/_cascade_files_W780.txt

### W779（2026-10-18）：全仓目录索引补齐批
> **来源**：用户令「检查一下文件内所有文件夹，添加一下 index.md REMADE.md STRUCTURE.md」。三项裁决：① REMADE.md=README.md 误写（仓内 0 先例·用户确认）→ 补 README.md；② STRUCTURE.md 不逐目录复制（根级 STRUCTURE.md 已存·单一事实源·各新文件放指针指回）；③ 范围=245 个在管目录（排除 node_modules/__pycache__/tmpe/构建产物/缓存）。动工前 preflight PASS（W779 认领·零交集）。
> - **定位分工（消除同文重复）**：`index.md`=逐文件清单（机器可读·查「这里有什么」）/ `README.md`=目录导读（人读·「装什么、怎么加」）。首版两者同文=174 个目录纯重复，违反文档规范 §3「单一事实源」判据——verify 全量跑完后重设计分工，再全量重生成。
> - **产物**：`scripts/gen_folder_docs.py`（幂等·大小写不敏感判重·gitignored 过滤·治理树排除·`--dry-run`/`--force`）+ `index.md` ×167 + `README.md` ×151，覆盖 179 个在管目录；`docs/INDEX.md` 重建（697→701 篇）。
> - **三处设计债整改（均由 verify 全量实证驱动）**：① **Windows NTFS 大小写不敏感**——直接 `open('index.md','w')` 会整文件覆写已存在的 `INDEX.md`，S4 学术投稿 12 份索引与 `docs/INDEX.md` 会瞬间清空（实测探针实证）→ 判重改为大小写不敏感；② **gitignored 路径泄漏**——首版实测 344 条被 `.gitignore` 排除的路径被列名入库（含 W650 裁决移出仓的真名 PRD、`.env`、`SECURITY-AUDIT-*.password`、`docs/S2-*`/`S3`/`S4` 双盲树）——列名本身即泄漏 → 加 `git check-ignore` 过滤（两处口径坑：目录查询必须带尾斜杠；stdout 行需剥 CR，否则集合永不命中），整改后 2908 条实测 **0 泄漏**；③ **治理目录污染**——`docs/10-方法论沉淀/` 与 `docs/11-方案报告/` 受第 17 门禁「方法论 README 双向覆盖」断言且 `report_docs`/`methodology_docs` 是 stats 键，脚本写入 3 个子目录即令 stats 25→32 触发第 31 门禁 C5d「stats 与磁盘实算漂移」FAIL → 两棵树（含子目录）整体跳过，README 仍由治理流程人工维护。
> - **连带**：`scripts/output/script-coverage-baseline.txt` 登记 `gen_folder_docs.py`（第 42 门禁 C1：四面无引用且不在豁免清单即 FAIL）。
> - **验证（全绿）**：`verify_delivery.py` 全量 **49 段 0 FAIL**；`lint_links.py --dir .` 全仓 **19906 链接 0 broken**；`docs_index.py --check` exit 0；pytest 逐模块 **603 passed 0 failed**（基线 602）；`ruff` 0；`generate_csp --check`/`check_js_syntax --all`/`check_structure` 三检查全绿；生成器**幂等**（重跑写入 0 文件·已存在跳过 336）。
> - **状态**：施工完成·门禁全绿；级联四文档 + 对账表 + file-index 同批落盘，待 commit。
> - **文件**：scripts/gen_folder_docs.py、docs/INDEX.md、scripts/output/script-coverage-baseline.txt、docs/00-导读/W批次编号对账表.md、CHANGELOG.md、HANDOVER.md、README.md、STRUCTURE.md、CITATION.cff、scripts/output/file-index.md、site/dukou-engine.html、site/index.html、site/data/cross-time-danmaku.html、site/data/tag-cloud.html、.github/workflows/README.md、docs/00-导读/项目说明.md。**目录索引件共 318 份**（清单类 167、导读类 151·按顶层分布于 .github / archive / assets / dataset / docs / hyperframes / mcp-server / packaging / references / scripts / site / source / tests / timeline / tools / xiyouji-agent-web 及仓库根）——逐文件全清单登记于 scripts/output/file-index.md 的 W779 段，运行 `python scripts/gen_folder_docs.py --dry-run` 可复现。

### W778（2026-10-17）：第 41 篇改进项落地批
> **来源**：用户令「开始优化」——第 41 篇复盘报告 §8 计划中 主会话归属项（T-41-01/02/04、P-41-01、T-41-03）——三项落地、一项撤销（T-41-03 见下）。动工前 preflight PASS（W778 认领·零交集）。
> - **P-41-01 + P-41-04 合成 pitfalls 新条目（流程节 6→7·总 40→41）**：`docs/agent/pitfalls.md` 新增「**latent 三问 + 双平台断言禁例**」——① 接线缺失型（K11 动画规则自 W674 潜伏 6 周·E2E 零接线·查法=列套件在 `run:` 块出现次数）；② 平台序差型（INDEX 门禁 CI 红/本地绿·`sorted(Path)` 两平台语义差·查法=显式键+双平台可判负样本）；③ 引号腐蚀型（`c === '"'` 被吞成空串比较·分支死代码五批·查法=逐字节验字符+五维对拍）。**双平台禁例**：盘符存在性/大小写不敏感排序/`os.name` 默认值断言在 Windows 负样本不可辨——必须登记「真实执行位=CI（Linux）」并 docstring 注明（处置例 test_tmpe_tidy::test_check_same_volume）。**AGENTS §4.3 三处计数同步**（阅读契约 38→41 条 / 流程节 6→7 / 总 38→40→41 修述）。
> - **T-41-02 流水线文档增补两节**：`docs/10-方法论沉淀/批次交付流水线.md` 新增 **§七 外部产出落地七步**（提取 round-trip→静态契约核验→旧版快照→字节级落地→对拍→全量验证→差异定性表·红线=禁止直接 cp 覆盖）与 **§八 重构/替换的对拍 SOP**（五维矩阵表：self-test/纯函数面/子集/全量/产物格式·各带归一化与降级路径 + 差异判定三规则：抖动归一/契约零容忍/覆盖集合变化须追根因且不得回滚修复）；原 §七 关联文档顺延 §九（全仓无 §七 引用·零断链）。
> - **T-41-01 对拍模板落地**：`tmpe/_templates/duipai/`（duipai.py：`snapshot` 采集 stdout/stderr/exit/meta + 计时归一化；`compare` 逐行或多重集 diff + 退出码判定；README 快速用法与判定规则）——**自测通过**：计时差异（1.5s/42ms vs 9.9s/99ms）归一后 PASS·新增内容行 FAIL+exit 1。
> - **T-41-03 复盘提醒 automation：提案撤销**——用户既有规则（2026-10-13 U-01：全部自动化取消·巡检/提醒回归手动或按需）优先；本批一度误建「复盘 48h 节奏提醒」被用户当场纠正，已立即删除，复盘节奏改为**会话内主动提议**（每次会话开工读最新篇日期，>48h 主动提示补写）。Q-11 改进路径以手动/按需方式保留。
> - **报告第 41 篇补跨周期执行记录**：头部加 HTML 注释记录本批三项 P1/P2 落地与 automation 提案撤销（周期口径 W748-W776 不变·第 39 篇同款做法）。
> - **验证（全绿）**：pytest 602 passed / 3 skipped / 0 failed；verify_delivery 全量 49 段 0 FAIL；ruff 0；pitfalls 顶层条目实测 41 == 各节声明合计 41；duipai.py 自测 PASS/FAIL 双态实证。
> - **状态**：已落地（本地全绿）；级联+提交+推送按批次流程执行（main 合并留待用户决策）。
> - **文件**：docs/agent/pitfalls.md、AGENTS.md、docs/10-方法论沉淀/批次交付流水线.md、docs/11-方案报告/工作复盘与优化分析报告/工作复盘与优化分析报告-2026-10-17.md、docs/00-导读/W批次编号对账表.md、CHANGELOG.md、README.md、STRUCTURE.md、docs/00-导读/项目说明.md、HANDOVER.md、CITATION.cff、scripts/output/file-index.md、scripts/output/_w778_spec.json、scripts/output/_cascade_files_W778.txt。

### W777（2026-10-17）：第 41 篇复盘报告入库批
> **来源**：用户令「现在写」——第 40 篇（2026-10-15）后断档 2 天、积压 W748–W776 二十八段/60 提交，本篇为补课。动工前 preflight PASS（W777 认领·零交集）。
> - **报告内容（十节框架+附录·V1.0）**：`docs/11-方案报告/工作复盘与优化分析报告/工作复盘与优化分析报告-2026-10-17.md`——周期 2026-10-15 20:55–10-17 23:10（约 50 小时）·覆盖 W748–W776（W750 作废不计）二十八段·提交 30ec46e3→ec76e397 共 60 个。五项核心发现：① 审查→修复→复验闭环成为主形态（W760 全量对抗审查 4 HIGH → W763-W770 八批全部清零）；② **「门禁自建即自曝」三次实证**——W773 CI 接线首跑抓 K11 动画规则潜伏 6 周（E2E 写了未接线）、W774 自建 INDEX 门禁 CI 红/本地绿（sorted(Path) 跨平台序差）、W775 对拍抓第 9 门禁引号腐蚀潜伏五批（2 页静默跳过）；③ CI 实证位认知闭环（本地全绿≠交付·三次真实分歧代价）；④ 两批工具链重构全部对拍零漂移（W761 四工作流/W775 JS 三门禁五维对拍）；⑤ 外部评审对抗→回应闭环（W775 报告+W776 §7 四项）。
> - **经验与机制沉淀**：新经验 **E-09~E-16**（五维受控对拍/latent 三型取证/自建门禁即自曝/外部产出落地七步/死依赖治理/C4 表格行/gitignore 检查/审查 HIGH 追踪表）·问题族 **FAM-31~36**（本地绿 CI 红/静态扫描器腐蚀/接线缺失/行尾编码/依赖度量漂移/编号登记一致性）·工作流 **WF-03~05**（对拍优先重构/外部产出七步/审查修复复验）·11 项问题实例（**6 项潜伏型**·Q-11 复盘断档入清单）。
> - **诚实的流程自曝**：报告明确登记「本报告本身是断档补课产物」——复盘节奏此前纯靠用户发起、无机器提醒（2 天 28 段零复盘）；改进候选=automation（48h 未写复盘提醒·T-41-03·**待用户批准后方可创建**·本批不擅自建）。
> - **三连带**：README 现役报告 20→21 篇（新条目取末号第 21 行）·STRUCTURE report_docs 24→25 + 现役 21 篇 + 复盘系列 12 篇·docs_index 重建（696→697 篇·--check exit 0）·stats --w W777 刷新。
> - **验证（全绿）**：pytest 602 passed / 3 skipped / 0 failed；verify_delivery 全量 49 段 0 FAIL；ruff 0；docs_index --check exit 0。
> - **状态**：已落地（本地全绿）；级联+提交+推送按批次流程执行（main 合并留待用户决策）。
> - **文件**：docs/11-方案报告/工作复盘与优化分析报告/工作复盘与优化分析报告-2026-10-17.md、docs/11-方案报告/README.md、STRUCTURE.md、docs/INDEX.md、docs/00-导读/W批次编号对账表.md、CHANGELOG.md、README.md、docs/00-导读/项目说明.md、HANDOVER.md、AGENTS.md、CITATION.cff、scripts/output/file-index.md、scripts/output/_w777_spec.json、scripts/output/_cascade_files_W777.txt。

### W776（2026-10-17）：评审后续行动落地批
> **来源**：用户令「做完报告 §7」——W775《外部评审回应与逐项核查报告》§7 四项后续行动（A-01~A-04）正式立项执行。动工前 preflight PASS（W776 认领·与在途批次零交集）。
> - **A-01 覆盖率口径决策（实证驱动）**：pytest-cov 一次性实测——全 `scripts/` TOTAL **18%**（23,762 语句）·门禁层（check_* + utils + verify_delivery/docs_index/stats）**24%**（4,647 语句）·计时开销 **+82%**（45s→82s·pytest 602 passed 不变）。三条结构性失真证据：① 门禁验证主路径是**子进程**（verify_delivery 以 subprocess 跑 49 段、测试以 subprocess 调 JS 门禁），coverage.py 进程本地跨进程失明；② **双轨制**——浏览器 E2E/视觉套件按设计排除于 pytest（pytest.ini W401 注释），由 CI 独立 job 覆盖；③ 23k 语句多数是 34 类数据生成器脚本，其正确性由输出级门禁与 self-test 负样本保证。**决策**：不引入 CI 覆盖率门禁（阈值门禁在内容型项目诱发凑数），决策全文与实证基线写入 pytest.ini 注释，替代呈现=可机器核验资产清单（602 passed + E2E 三套件 + verify 49 段）。
> - **A-02 死依赖移除（由「精确钉版」升级）**：实证推翻原计划前提——全仓（含 `archive/`）**零 import** fonttools/brotli：W564 字体子集化的一次性工具已归档（archive/scripts/batches/misc/_check_font_coverage.py 亦不 import）、packaging/xiyouji-analysis 无依赖声明、Makefile 无引用；两条 `>=` 区间条目为纯死依赖。**处置**：从 `scripts/requirements.txt` 移除两行（消除供应链与 pip-audit 无效扫描面），`scripts/font-subset-guide.md` §3.1 改为按需安装注记（pyftsubset 回退路径可用性保留）；原「精确钉版」计划废止并在报告 §7 留痕。
> - **A-03 机制层风险登记**：`HANDOVER.md` Backlog 新增 BL-26（内容质量方差·AI 平庸化→写作规范 §4 五条反模式 + 对抗性审查批持续抽检）/ BL-27（工程 overhead 可持续性·断点可恢复性是主动权衡）/ BL-28（单点故障·无解已缓解到可转让），三条均标注**不设工程关闭项**；`docs/10-方法论沉淀/markdown写作规范.md` §4 新增 5 条「AI 内容生产特有」反模式（情节复述+主题套话/平庸安全结论/情感空转/流畅权威体/引文真推论假）。
> - **A-04 评审原文归档**：评审原文 235 行（原 txt L21705–L21939·三轮完整）逐字节提取至 `tmpe/review-w776/review-original.md` + 同目录 README（来源/提取方式/三轮结构与报告章节映射）；tmpe 为 gitignored 工地层不随仓库发布，报告为唯一权威回应。
> - **验证（全绿）**：pytest **602 passed / 3 skipped / 0 failed**；verify_delivery 全量 **49 段 0 FAIL**；ruff 0；docs_index --check exit 0。
> - **状态**：已落地（本地全绿）；级联+提交+推送按批次流程执行（main 合并留待用户决策）。
> - **文件**：pytest.ini、scripts/requirements.txt、scripts/font-subset-guide.md、HANDOVER.md、docs/10-方法论沉淀/markdown写作规范.md、docs/11-方案报告/外部评审回应与逐项核查报告-2026-10-17.md、docs/00-导读/W批次编号对账表.md、CHANGELOG.md、README.md、STRUCTURE.md、docs/00-导读/项目说明.md、AGENTS.md、CITATION.cff、scripts/output/file-index.md、scripts/output/_w776_spec.json、scripts/output/_cascade_files_W776.txt。

### W775（2026-10-17）：JS 门禁重构落地批
> **来源**：用户转交桌面重构产出（外部会话的 JS 门禁重构全文 + 5 条「需你裁决的发现」+ 两轮外部评审文本），指令三项并做——落地重构、裁决 5 条、回应评审。动工前 preflight PASS（W775 认领·与在途 W750/W764 零交集）。
> - **T1 重构落地（两个新公共模块 + 三门禁重写）**：新增 `scripts/lib/gate_common.js`（路径规范化/HTML 枚举/脚本注释剥离/worker 池/门禁汇总行·110 行）与 `scripts/lib/playwright_gate_utils.js`（统一 launch/离线页创建含外域拦截与 pageerror 收集/file:// 导航·53 行）；`check_chart_values.js`（1409→1529 行：probeInPage 拆 6 个统计函数、judgeProbe 拆 judgeV1~V5+makeVerdict、前置后置重复基线校验合并为 validateGateBaseline、模式分发函数化 main 200→80 行）、`check_screenshot_gates.js`（186→212 行：checkPage 拆 G1–G5 独立判据、删死代码 BENIGN_CONSOLE_RE、补 'use strict'）、`check_data_drift.js`（326→385 行：jsLiteralToJson 拆两纯函数、main 拆 collectCandidateJsonPaths/checkDeployedCopies/comparePageAgainstJson、47→EXPECTED_DEPLOYED_COPY_COUNT 常量化）。txt 提取经 round-trip 逐字节自检；外部会话携带的异体系溯源批号统一就地修正为本批号（防 W 号体系污染）。
> - **T2 静态契约核验（外部契约零漂移）**：`module.exports` 九项（judgeProbe/compareBaseline/parseBaseline/numEq/TH/ITEMS/CRITERIA/summarizeData/classifyFamily/discoverDataNames）逐项在册；CLI 参数面、退出码语义（gate 基线外新增=1/report=0/self-test 全过=0）、基线四段格式、stdout 末行 `---- 第 43 门禁 可视化数据断言：N FAIL ----` 全部保真；FAIL/OK/WARN 消息文本逐字节一致（sorted diff 实证）；W767/W770 行为点（深比对/基线豁免/部署副本优先解析/EMBEDDED 回退）逐段核对在位。
> - **T3 五维受控对拍（旧版快照 vs 新版重跑）**：self-test 12/12 同判定（仅 T10 打印序移位·纯装饰）；--judge 注入载荷输出**逐字节一致**；--gate 3 页（81-hardships/guanyin-six-roles-network/chapter-stats）**逐字节一致**（计时归一）；截图门禁 32 页子集**逐字节一致**（静态清单计数 sankey 26/link-canvas 36 不变）；--generate-baseline 格式一致（差异仅计时/像素固有抖动与两行注释性头精简·基线文件未入库且解析器跳过 # 行）。
> - **T4 潜伏缺陷修复（对拍意外收获·第 9 门禁覆盖缺口）**：`check_data_drift.js` 的 `jsLiteralToJson` 字符串归一化分支自安全加固改写起即被引号腐蚀（`c === ""` 空串比较·分支死代码）——含单引号 EMBEDDED 块的 timeline/journey-geo-semiotics 两页被静默跳过为「无内嵌块」达五个批次（W424 初版 `new Function` 动态求值 → 加固改写静态扫描器时引号字符被吞）。重构版恢复正确引号比较，两页纳入共路深比对且全绿：可比 **57→59 页**（147→150 对比项）·exit 0·全量 verify 第 9 槽通过。git 考古（9d434c9b→a460b889→c2846d82）确认腐蚀路径留档。
> - **T5 基建坑修复**：`.gitignore` 的 `lib/`（Python 模板残留）误伤 `scripts/lib/`——不修则新模块不入库、CI 必现 MODULE_NOT_FOUND；定向 negation（`!scripts/lib/` + `!scripts/lib/*.js`）修复，check-ignore 实证转白。
> - **T6 测试面跟随**：`test_ci_wiring.py` gate43 playwright 断言升级为「传递链两环」守护（门禁 → playwright_gate_utils → require('playwright')·任一环断裂即红），保留原意图（CI 装浏览器耦合探测）·11 passed。
> - **T7 五条待裁决发现裁定**：3.1 TH 重复键——随重构解决（删重复项·单一定义值 0.02 不变）；3.2 未用 text 参数——**不改**（5 条规则 4 条同构不用 text 是「规则族统一签名」设计形态·L1 注释明示·ruff 未开 ARG 规则）；3.3 短路表达式——**改**（去冗余 `and` 护栏+双 findall·与 parse_html 既有习语对齐·tuple 空集等价零行为变化）；3.4 死常量 MAX_LINES_MSG——**改**（删除·零引用实证）；3.5 分段循环——**不改**（接受原建议：合并会改 stdout 路径文本）。
> - **T8 外部评审回应**：`docs/11-方案报告/外部评审回应与逐项核查报告-2026-10-17.md`——七项工程指控逐条核查（4 不成立/2 部分成立/1 成立：唯一成立项为测试覆盖率数字缺席·登记后续候选）、索要四项材料的仓库实况（verify 注册段/pytest 配置/agent-web 安全三套件/sync_docs 源码）、两轮机制层批评的立场回应（质量方差成立属人的战场、工程 overhead 成立属主动权衡、单点故障成立已缓解到可转让）；评审文本三个存量数字（600+ 提交/W759/43 项门禁）与现势（772 提交/W774/44 槽）全部失配，证其所据为过期公开快照。
> - **验证（全绿）**：pytest 602 passed / 3 skipped / 0 failed；verify_delivery 全量 **49 段 0 FAIL**（含第 9 槽数据漂移 59 页·第 43 槽 87 页 V1–V5 0 FAIL·第 42 槽根级覆盖）；ruff 0；三门禁 self-test/直跑 exit 0；timeline/claude_md self-test 与默认跑双绿；node --check 五文件全过。
> - **状态**：已落地（本地全绿）；级联+提交+推送按批次流程执行（main 合并留待用户决策）。
> - **文件**：scripts/lib/gate_common.js、scripts/lib/playwright_gate_utils.js、scripts/check_chart_values.js、scripts/check_screenshot_gates.js、scripts/check_data_drift.js、tests/unit/test_ci_wiring.py、scripts/check_story_timeline_sync.py、scripts/check_claude_md.py、.gitignore、docs/11-方案报告/外部评审回应与逐项核查报告-2026-10-17.md、docs/11-方案报告/README.md、docs/INDEX.md、STRUCTURE.md、docs/00-导读/W批次编号对账表.md、CHANGELOG.md、README.md、docs/00-导读/项目说明.md、HANDOVER.md、AGENTS.md、CITATION.cff、scripts/output/file-index.md、scripts/output/_w775_spec.json、scripts/output/_cascade_files_W775.txt。

### W774（2026-10-17）：CI 首跑分歧修复批
> **来源**：W773 收官后用户指令闭环 AC-02——推送 origin/dev（10 提交·含 W771/W772 dev 积压）并开 PR #47 dev→main，CI 首跑暴露新缺陷，本批修复并复跑全绿。
> - **CI 首跑实况（run 39033092055）**：e2e-interaction job **success**（T-02 AC-02 核心判据达成·job 日志实证 K11 `animation-name=wordFloat`·22 断言全过——W674 遗留回归的修复在 CI 真实验证）；但 verify-delivery job **红**：本批自建的第 17 门禁「docs/INDEX.md 产物级校验」在 Linux 报 INDEX 过期（本地 Windows 全绿）。
> - **根因（第三项 latent·「本地绿/CI 红」分歧族）**：`docs_index.scan_docs` 裸 `sorted(Path)` 在 Windows 用 normcase（大小写不敏感）、Linux 用大小写敏感——`00-导读` 的 `design.md` 与 `10-方法论沉淀` 的大小写混排条目在两平台排序不同（实测 diff：design.md 位次 7↔10·方法论三条目位移），生成内容与入库 INDEX.md 失配。**且由本批自建门禁自曝**——新防线「违例必红」有效性的正面实证。
> - **修复**：scan_docs 两处排序显式加 `str(p).lower()` 键（纯 Python 串比较·平台无关·与存量 INDEX.md 顺序字节一致·重建零 churn 实测 `git diff` 为空）。
> - **回归防线**：新增 `tests/unit/test_docs_index.py` 三例——合成目录小写键序不变量（Beta/alpha/Gamma）、真实 docs/ 树不变量、磁盘与生成器逐字节一致。注意 Windows 上裸排与小写键等价（normcase），合成用例在 Windows 两法均绿——**真实执行位是 CI（Linux）**，与 W773「CI 才是实证位」同款保护模型（已入 docstring）。
> - **T-02 闭环记录**：PR #47（https://github.com/1273984347/xiyouji/pull/47）复跑 run [39034308443](https://github.com/1273984347/xiyouji/actions/runs/39034308443) **success**——E2E Interaction 与 Delivery Gate 双绿·全 9 job+矩阵过；计划文件 ST-04 与 AC-02 转闭环（两轮 run URL 留证）。
> - **范围纪律**：不动 verify_delivery.py·无 site 页面改动·INDEX.md 重建零 diff·视觉套件仍不入 CI。
> - **验证（全绿）**：pytest **602 passed / 3 skipped / 0 failed**（599+3 新增）；verify_delivery 全量 49 段 0 FAIL；ruff 0；gate 17 直跑 exit 0；docs_index --check exit 0；PR #47 CI 复跑 success。
> - **状态**：已落地并推送；PR #47 待用户合并（main 写操作按纪律留待用户决策）。
> - **文件**：scripts/docs_index.py、tests/unit/test_docs_index.py、docs/11-方案报告/计划方案/执行前计划-T02-工程基础设施薄弱点修复.md、docs/00-导读/W批次编号对账表.md、CHANGELOG.md、README.md、docs/00-导读/项目说明.md、HANDOVER.md、AGENTS.md、CITATION.cff、scripts/output/file-index.md、scripts/output/_w774_spec.json、scripts/output/_cascade_files_W774.txt。

### W773（2026-10-17）：工程基础设施薄弱点修复批
> **来源**：用户 2026-10-17 会话批准执行 T-02《执行前计划——工程基础设施薄弱点修复》（`docs/11-方案报告/计划方案/执行前计划-T02-工程基础设施薄弱点修复.md`·V1.0）——四项「有设施无防线」缺陷修复批，分 WS1~WS4 四波推进，本地五提交（W772 收官 chore / 波一 CI 接线+视觉 / WS3 英文站 a11y / WS4 索引门禁 / 本级联收尾）。
> - **WS1 CI 接线（缺陷①·8 个 JS E2E 套件零 workflow 调用）**：ci.yml 新增 e2e-interaction job（`node tests/e2e/test_site_quality.js`·npm ci --prefix scripts + playwright chromium·job 数 8→9）；test_ci_wiring.py 扩 W6 断言（判据锚 `run:` 块对抗步骤名伪装·负样本注释 run 行实测转红·恢复字节一致回绿·11 passed）。
> - **WS1 战果——K11 回归修复（接线首跑即抓）**：reduce 专属规则误置于 max-width:640px 媒体查询之后（顶层 !important·scalpel 演出动画对全部用户静默失效·K11 实证 computed animation-name 恒 none·自 W674 起潜伏 6 周——pytest.ini 排除 tests/e2e 故套件从未自动运行）；中英双页同修移入查询内，22 断言转全绿（「门禁建置即绿」铁则正面实证）。
> - **WS2 视觉回归（缺陷②·基线 PNG 被 gitignore 无版本化载体）**：.gitignore 取消 tests/e2e/baseline/ 排除（10 PNG 版本化·current/ 保持忽略）；test_visual.js 判据由「文件大小 ±15%」升级为 pngjs+pixelmatch 像素 diff（默认阈值 0.5%·宽高不一致直失败·稳定轮询兜力导向/演出动画抖动·文件大小降级为信息量）；对旧基线实跑 10/10 尺寸不一致（8 月至今内容演进·旧基线全废）→ 重灌 10 页·二次跑 10/10 0 FAIL（实测像素差异 0.000%~0.122%）；新增依赖 pngjs 7.0.0 + pixelmatch 5.3.0（CJS·v8 系 ESM 有 CI Node 20 兼容风险故弃用）。
> - **WS3 英文站 a11y（缺陷③·chart-a11y 覆盖 0/138）**：inject_chart_a11y.py 加 --dir（默认 site/data 行为不变·rel 前缀按目标目录相对 site/ 深度计算）；site/en 138 页全量注入·二次幂等 0·--check exit 0；chart-a11y.js 最小 i18n（摘要文本按 html lang 选 zh/en·缺省 zh·中文页行为逐字节不变·探针对拍实证）。
> - **WS3 连带修复（注入前探针暴露第二项 latent）**：8 个 EN 页 `<html lang="zh-CN">`（W394-W398 漏网·读屏语音/SEO/i18n 全错）修正为 en；validate_en 补第 3 项检查（文档 lang=en·WCAG 3.1.1·负样本实测转红·恢复一致）——指向中文版的回链 lang="zh-CN" 语义正确不误伤。覆盖口径：EN 图表页 83/83（80 静态 svg/canvas + 3 运行时渲染 ai-dialogue/century-dialogue/character-relationship-3d——ASM-09b「58 纯文本页」判断对这 3 页不成立·全页注入策略与 site/data 87/88 同规则）。
> - **WS4 索引门禁（缺陷④·INDEX.md 无产物级校验）**：check_index_health.py（第 17 门禁·D-01 决策扩面而非新增槽位·未触碰受保护件 verify_delivery.py）新增第 8 项检查 docs/INDEX.md 产物级一致性（复用 docs_index.py 生成逻辑逐字节比对·单一事实源）；负样本（删 1 条目）实测转红·恢复字节一致回绿；docs_index.py --check exit 0（695 篇·12 板块）——mcp-server「CI 同款」声明自本批起成为事实。
> - **范围纪律**：不动 verify_delivery.py（受保护件）；视觉套件本批不入 CI（D-02 首波只接 1 套件·V-02 首波目标 1/8 达成）；test_graph/test_newfeatures（API_PORT 在线断言）与 test_w266（@playwright/test 未声明）按 R-03/R-04 排除出首波；不做第 43 门禁豁免收敛；.github/workflows/README.md 同步新 job 文档（雷区 13.7）。
> - **验证（全绿）**：pytest **599 passed / 3 skipped / 0 failed**（基线 597 + 新增 2 接线断言）；verify_delivery 全量 **49 段 0 FAIL**；CSP 856 页零漂移；validate_en --all **138/138**（含新增 lang 检查）；ruff 0；JS 语法 855 文件；e2e 22 断言全绿；视觉二次跑 10/10；stats --check 零差异（16 键·本批无键值变更）。
> - **状态**：WS1~WS4 全部落地（本地）；**ST-04 未闭环**——github.com 主站被代理拦截（CONNECT 502·重试多次均失败·gh 与 api.github.com 正常），推送与 CI 实跑实证待网络恢复后执行（AC-02 余项如实登记·不虚构「CI 绿」）。
> - **文件**：.github/workflows/ci.yml、.github/workflows/README.md、.gitignore、tests/e2e/baseline/（10 PNG）、tests/e2e/test_visual.js、tests/unit/test_ci_wiring.py、scripts/package.json、scripts/package-lock.json、scripts/inject_chart_a11y.py、scripts/validate_en.py、scripts/check_index_health.py、site/static/js/chart-a11y.js、site/data/criticism-history.html、site/en/criticism-history.html、site/en/（138 页）、docs/11-方案报告/计划方案/执行前计划-T02-工程基础设施薄弱点修复.md、docs/00-导读/W批次编号对账表.md、CHANGELOG.md、README.md、docs/00-导读/项目说明.md、HANDOVER.md、AGENTS.md、CITATION.cff、scripts/output/file-index.md、scripts/output/_w773_spec.json、scripts/output/_cascade_files_W773.txt。

### W772（2026-10-17）：计划入库纯文档批
> **来源**：用户令「认领 W772『计划入库纯文档批』并完成全级联」——T-02 工程基础设施薄弱点修复计划（2026-10-17 落盘）与既有 T-01 计划及报告三件一并登记入 `docs/11-方案报告/README.md` 索引，完成报告计数与 docs 索引级联。
> - **计划方案三篇登记**：`docs/11-方案报告/计划方案/` 下 3 篇（`执行前计划-T01.md`、`T01-任务计划执行与经验沉淀报告-2026-10-14.md`、`执行前计划-T02-工程基础设施薄弱点修复.md`）此前**从未进入本目录索引**（README 全文 grep「计划方案」= 0 命中·存量登记缺口）——本批在 README 新建「二、计划方案（3 篇）」章节登记，原「二、历史归档指针」顺延为「三、」。
> - **现役报告计数不变**：README「一、现役报告（19 篇）」维持 19 篇——目录分区口径 = 现役报告 19 + 索引 README 1 + 计划方案 3 = 23，与 STRUCTURE 现役文字同源。
> - **报告计数三连带**：STRUCTURE.md `report_docs` 标记 22→23 + 现役文字「计划方案 2 篇」→「3 篇」+ `stats.py --w W772` 刷新（stats-changelog + stats-index 派生）·`--check` 零差异（16 键）。
> - **docs 索引重建**：`docs_index.py` 重建 `docs/INDEX.md`，清 2 条存量漂移（`W761工具链可维护性重构报告-2026-10-16.md`、`全量对抗审查报告-2026-10-16.md` 未入索引）·`--check` exit 0。
> - **T-02 计划要点（登记·非执行）**：四项「有设施无防线」缺陷——① 8 个 Playwright JS E2E 套件与视觉回归层零 workflow 接线；② 视觉基线 PNG 被 `.gitignore` 排除（无版本化载体）；③ 英文站 chart-a11y 覆盖 0 页（中文站 87/88）；④ `docs/INDEX.md` 无产物级一致性门禁。计划含 G-01 目标、AC-01~09（每条含命令与 exit/计数判据）、ST-01~10、V-01~10、R-01~08、D-01~06。
> - **状态**：**修复批未动工**——WS1~WS4 修复波次待用户批准 W 号与批次拆解后另批执行（本批仅登记入库·**零代码改动**）。
> - **验证（全绿）**：`stats.py --check` 零差异；`docs_index.py --check` exit 0；batch_cascade dry-run 十面预检全过；**pytest 597 passed**（+3 skipped·0 failed；**两段实测绿拼合**——全量除 viz 层 582 项 = 579 passed/3 skipped rc=0 30.6s，viz 层单跑 18 项 = 18 passed rc=0；本机 Windows 全量单进程在 ~39s 处被控制台 SIGINT 打断于 viz 层首例 `test_self_test_passes_and_covers_at_least_five_cases`，八面取证排除内存[峰值 RSS 95MB]/磁盘[余 239GB]/墙钟看门狗/Sleep 38s 后 spawn node 存活/测试内进程自杀[grep 0 命中]/单文件缺陷[viz 单跑与配对均绿]/Playwright 浏览器用例[deselect 仍打断]/本批引入[暂存 23 文件 .py 与 .js 计 0]；deselect viz 层 12 例 node 播种用例后全量 585 passed/3 skipped/12 deselected rc=0 38.2s 三面互证；**非仓内缺陷**——CI Linux main 分支全绿）；verify_delivery 全量 49 段 0 FAIL。
> - **文件**：docs/11-方案报告/计划方案/执行前计划-T02-工程基础设施薄弱点修复.md、docs/11-方案报告/README.md、STRUCTURE.md、CHANGELOG.md、README.md、docs/00-导读/项目说明.md、HANDOVER.md、AGENTS.md、CITATION.cff、.github/workflows/README.md、scripts/output/file-index.md、scripts/output/stats.json、scripts/output/stats-changelog.json、scripts/output/stats-index.md、scripts/output/_w772_spec.json、scripts/output/_cascade_files_W772.txt、docs/00-导读/W批次编号对账表.md、docs/INDEX.md、site/index.html、site/dukou-engine.html、site/data/tag-cloud.html、site/data/cross-time-danmaku.html、archive/docs/AGENTS-ARCHIVE.md。

### W771（2026-10-16）：编号空洞登记与门禁注释刷新批
> **来源**：用户令「F-9 现在做」——W760 全量对抗审查报告 F-9 跟踪项（10 个 W 号区间缺失且 CHANGELOG/对账表均无记载 + 门禁注释陈旧），W766-W770 五批修复后 F-1~F-8/F-10/F-11 均已闭环，本批收口最后两项。动工前 preflight_check 全绿（对账表 max=W770 → W771 认领·touches 交集 0）。
> - **T1 十缺号三源定性**（取证脚本 `tmpe/w771_evidence.py`·三源=CHANGELOG 现役+两归档/对账表表格行/git 全历史提交）：逐号定性后据实分三类处置——**A 类有提交未立段（2 号）**：W341（`1bad4374` 死链巡检修复·早批未立 CHANGELOG 段）、W392（`0dda530f` 内容导读层）；**B 类计划档明示未执行后重排（6 号）**：W466 归档维护 SOP、W470 dataset +2、W472 375px 回归、W473 a11y 达标（被 W493 替代）、W474 性能预算复核、加 W467/W468/W469 同家族连续预排号（`archive/docs/plans/2026-08-18-w464-phase3-quantified-roadmap.md` 处置列明文「❌ 未执行/重排新号」）；**C 类预排后由实际批次落地（3 号）**：W480/W481/W482 = phase-e 计划 E4/E5/E6 预排号，其**计划档执行表（L258-260）自证**由 W491/W492/W493 落地且已在 CHANGELOG 立段。十号均无 git 批次提交（W341/W392 的工作量合入相邻号提交），无 S4 双盲或预发表风险。
> - **T2 门禁注释刷新**（F-9 附带项）：`scripts/check_seo_head.py` docstring 与常量注释的 **233/230/229 页** 为陈旧数字（SEO 注入面实测 855、sitemap 收录面实测 851），现役代码行为与门禁实际一致、仅注释误导维护者；刷新为实测口径并对齐 `verify_delivery.py` 同行注释。**范围纪律**：注释-only（不触任何判定逻辑·第 26 槽不受影响）。
> - **T3 对账表登记**：W771 认领行 + 「递延批豁免登记」补 10 号去向 bullet（登记即豁免·doc-sync C4 口径）——不动任何历史行。
> - **验证（全绿）**：`py_compile` 通过；`ruff check` 零违例；十号三源表逐号有出处（git log --all 实证 hash + 计划档行号）;`check_seo_head.py` 实跑 **855 页通过·sitemap 集合一致**（注释刷新前后行为零变化）；`pytest 597 passed / 3 skipped`；`verify_delivery.py` 全量 49 段自洽锁 0 FAIL。
> - **状态**：已落地（本地）。
> - **文件**：scripts/check_seo_head.py、docs/00-导读/W批次编号对账表.md、CHANGELOG.md、README.md、STRUCTURE.md、docs/00-导读/项目说明.md、HANDOVER.md、.github/workflows/README.md、site/index.html、site/dukou-engine.html、site/data/tag-cloud.html、site/data/cross-time-danmaku.html、archive/docs/AGENTS-ARCHIVE.md、AGENTS.md、CITATION.cff、scripts/output/file-index.md、scripts/output/_w771_spec.json、scripts/output/_cascade_files_W771.txt。（取证脚本 `tmpe/w771_evidence.py` 留本地不入库·tmpe/ gitignored 既定策略·W768 先例）

### W770（2026-10-16）：引文豁免口径修正与数据链路对齐批
> **来源**：用户令「继续」（W760 审查遗留收口：F-2 经用户批准修脚本 + W767 登记的 hardships 对齐 + F-8 复核）。
> - **F-2 修复（check_citations.py·两判定面）**：① `_iter_checked_lines`（检查 1/2 豁免）——文首文件级标记（首个标题前的 `> 【文学演绎】`）此前因 head_level=0 置 fiction_until=0（0 即「不在豁免区」）而实为不豁免 → 新增 file_fiction 整文件豁免态；② `scan_reverse`（--reverse 候选）——原 `marked` 语义仅豁免到下一标题即清，与外传文类「h1 标题后的文首标记」冲突 → 改为与 `_iter_checked_lines` 同源的「标记时标题级·豁免至同级或更高级标题」+ 文件级豁免。**实证**：接引佛祖外传/日值功曹外传的假阳性候选（「一、凌云渡」「六、那一页」各 1）修复后归零；自测 +2 例（check_text/scan_reverse 双面）12/12。
> - **hardships_81 生成器 label 化输出对齐（W767 登记项）**：`C_情节/hardships_81.py` 输出的 `hardships` 清单由 code 形（arranged/taken/solo…）转 **label 形**（如来/观音安排/被接走（有背景）/悟空独立解决…·经 build_statistics 既有 label_maps 映射）——与页面 EMBEDDED 及 dataset/81-hardships.json 对齐；重生成 + `sync_data_json.py` 同步部署副本。
> - **副本回灌与自检工具恢复**：全站排查实证 `site/data/json/` 部署副本含 W678/W691 修复而 `scripts/output/data/` 原件未回灌（20 件·如 `/demo 求助观音`、`中将级`、`geo3d 到达回`、W691 口径注记等）——**回灌 20 件**（副本为准·含 project_review 副本侧重复后缀损坏修复×2）→ 47 副本与原件**字节全等**；恢复 `scripts/_check_json_copies.py`（W563 的本地字节级自检工具·W735 归档后门禁注释仍引用其职责·本轮实证其缺位正是回灌缺口无人报警的根因）。
> - **门禁解析 v3.1（check_data_drift.js）**：候选解析补两级——`json/…` 形态优先解析到 **tracked 副本**（CI 稳定：gitignored 原件在 CI 由 run_all 再生成·值可因生成器源差异漂移）+ 裸文件名形态（relationships.html 的 loadJson（…）族·此前整页跳过）。**实测覆盖跃升**：可比 45→57 页·JSON 对比项 73→147·全绿（豁免仅剩 visual-art 设计双形态 1 项）。
> - **F-8 复核（诚实留档）**：审查员「pytest 95% 静默终止」不可复现——本轮 6+ 次全量与两形态定向（`tests/unit` 单跑 413+3·全量 597+3）全绿；其建议的两项防护**均已在位**（probePage 逐探针 context.close :453 + 探针超时 :442 + subprocess timeout=300），其「仅全部跑完才 browser.close()」论断与代码实况不符。登记为观察项：若复发按其 bisect 表定位 + 考虑 --workers=1。
> - **验证（全绿）**：check_citations 自测 12/12 + 主检 423+112 命中率 100% + --reverse 候选 0；数据漂移 v3.1 门禁绿（覆盖 45→57 页/73→147 对·豁免 1）；47 副本字节全等；**pytest 597 passed**；verify_delivery 全量 49 段 0 核心 FAIL。
> - **状态**：已提交（本地）。
> - **文件**：scripts/check_citations.py、scripts/C_情节/hardships_81.py、scripts/_check_json_copies.py（新·自 archive 恢复）、scripts/check_data_drift.js、scripts/output/data-drift-baseline.txt、site/data/json/hardships_81.json、site/data/json/project_review.json、scripts/output/_w770_spec.json、docs/00-导读/W批次编号对账表.md、CHANGELOG.md、README.md、STRUCTURE.md、docs/00-导读/项目说明.md、HANDOVER.md、.github/workflows/README.md、site/index.html、site/dukou-engine.html、site/data/tag-cloud.html、site/data/cross-time-danmaku.html、archive/docs/AGENTS-ARCHIVE.md、AGENTS.md、CITATION.cff、scripts/output/file-index.md、scripts/output/_cascade_files_W770.txt。

### W769（2026-10-16）：动效时长归一与口径说明修正批
> **来源**：用户令「继续」（W760 审查 P1/P2 残余小项：F-4 动效盲区 + F-9/F-10 口径说明与文案）。
> - **WS1 动效时长归一（F-4）**：① 全站扫描实测——`.duration(N)` N>600 共 **37 处 / 20 页**（site/en 19 页 + dashboard；最大 journey-map-interactive 3000·与 W462 已归一的 zh 站形成对照）；② **37 处全部归一为 600**（DESIGN §5.1 全站硬指标 N ≤ 600·入场档上限；cultural-misreading 两处 900 经上下文核验系入场动画非 KPI count-up·不适用 900 白名单）；③ **第 13 门禁补规则**（check_motion_ban.py）——新增 `.duration(N)` N>600 判据（扫域=site/** 全部 HTML·天然覆盖 en 站·白名单仅 KPI count-up 900 须伴 easeOutExpo 上下文）；**负样本实证**（注入 9999 → 门禁转红且精确到路径+上下文 → 恢复转绿）。此前全仓无任何 duration 检查器（审查员面「扫描域盲区」归因修正为「规则缺位」）。
> - **WS2 口径说明修正（F-9/F-10）**：① `docs/00-导读/统计口径说明.md` §2 自相矛盾修正——标题「= 86 页」→「= 87 页」·算法行更新为「88 文件 − _shell = 87」（W694 起级联·W459 旧口径块注释替换）；② **现役叙述面 8 处 86→87 同步**——site/index.html ×4（KPI 数字块/「全部 86 页」/「86 个 D3.js」/「全站 86 个页面」）+ site/dashboard.html ×1 + DESIGN.md 首节 + HANDOVER.md「V 方向」节头 + 新Agent启动Prompt.md（Html=88·对外 87）；**历史记录保留口径**：HANDOVER「曾为静态博物馆」回顾段与 W445/W446 批次记录等历史语境数字不改写；S4 投稿冻结稿不在门禁分母（不改）。
> - **WS2b 门禁域扩展**：`check_doc_sync.py` C5 扫描域补入「统计口径说明.md」（该文件自称「唯一口径来源」却此前不在任何扫描域·F-9 根因）+ 装载器 + 自测夹具三处；**自测 18/18 通过**。
> - **验证（全绿）**：全站 duration 扫描 0 超限；check_motion_ban 负样本闭环；check_doc_sync 自测 18/18 + C5 扩展后零新告警；CSP 重注零漂移（改内联脚本 20 页后）；**pytest 597 passed**；verify_delivery 全量 49 段 0 核心 FAIL。
> - **状态**：已提交（本地）。
> - **文件**：scripts/check_motion_ban.py、scripts/check_doc_sync.py、docs/00-导读/统计口径说明.md、site/index.html、site/dashboard.html、site/en/（19 页）、DESIGN.md、HANDOVER.md、新Agent启动Prompt.md、scripts/output/_w769_spec.json、docs/00-导读/W批次编号对账表.md、CHANGELOG.md、README.md、STRUCTURE.md、docs/00-导读/项目说明.md、HANDOVER.md、.github/workflows/README.md、site/index.html、site/dukou-engine.html、site/data/tag-cloud.html、site/data/cross-time-danmaku.html、archive/docs/AGENTS-ARCHIVE.md、AGENTS.md、CITATION.cff、scripts/output/file-index.md、scripts/output/_cascade_files_W769.txt。

### W768（2026-10-16）：英文站校验接线批
> **来源**：用户令「继续」（遗留事项③·W760 审查 F-3 HIGH 收口——四 HIGH 最后一项）。W760 实证：`HANDOVER`/`V2可视化维度方案` 宣称「138 个 EN 页通过 validate_en.py」，实际三入口零接线（verify/CI/Makefile 均无引用）+ 被第 42 槽（根级脚本覆盖）豁免基线豁免，6 页违规（search 中文语料 5458 CJK + chart-design 132 / chapter-stats 102 / methodology-matrix 48 / character-appearance 35 / relationships 1）长期在绿。
> - **G1 校验器升级（validate_en.py）**：① 新增 `--all [root]` 批量模式（全站遍历·汇总行 `EN validate: OK=N FAIL=M`·任一页违规即退出码 1）；② 豁免区落地——`/* SEARCH_INDEX:BEGIN */…/* SEARCH_INDEX:END */` 包裹的全文检索语料索引为「引用语料区」（与第 20 槽「原文全文」豁免区同类·W768 用户口径），不计入 script CJK；③ 单页模式输出与旧版**逐字节兼容**（check_page 重构·对拍留档：非语料页输出 IDENTICAL）。
> - **G2 六页整改**：① chart-design——zh→en 字典（HOUR_EN/ACTGEN_EN/MSTATE_EN/SACT_EN/SKEY_EN 共 126 对）全域转形（数据+字典键同步·自映射保行为）；② methodology-matrix——MONSTER_EN/PHASE_EN/RESCUER_EN/RMONSTER_EN 32 对 + 四角标签键值化（左上→left_top 等）；③ character-appearance——ZH2EN_NAME 35 对转形；④ chapter-stats——「第N回」→「Chapter N」×102（循 chapters-map「Chapter 100」惯例）；⑤ relationships——调试串 `[DATA] EMBEDDED 单源:` → `single-source:`；⑥ search——语料索引按豁免区口径处理（0 改动·EXEMPT 生效）。
> - **G3 接线（第 44 槽）**：verify_delivery.py 五面注册（EXPECTED_SECTION_NAMES 49 段 / _STRICT_GATES 含 marker `EN validate:` / _GATE_SUMMARY_MARKERS / SCOPE_SITE_SECTIONS / 头注 46→49 段校正）；CI 经 verify-delivery job 自动生效；Makefile 新增 `validate-en` 目标并挂入 `ci` 链；第 42 槽豁免基线移除 `validate_en.py  # ①英文站校验` 行（接线后不再豁免）。
> - **G4 三方编号同步**：AGENTS §4.2（43→44 槽·清单补第 44 项）+ gates.md（标题 44 槽·补第 44 槽全量定义）+ stats `gate_count` 43→44（--w W768 刷新）+ README `<!--stats:gate_count-->` 标记 43→44。
> - **验证（全绿）**：`validate_en --all` **138/138 通过**；verify_delivery 全量 **49 段**（实跑==声明）0 核心 FAIL；CSP 重注零漂移（856 页/858 哈希·5 页内联脚本改动后重注）；单页输出与旧版对拍一致；**pytest 597 passed**。
> - **状态**：已提交（本地）。**W760 审查四项 HIGH 至此全部办结**（F-1a W763 / F-1b W766 / RCE W764 / 第 9 门禁 W767 / validate_en 本批）；余用户侧 `.env` 凭证轮换。
> - **文件**：scripts/validate_en.py、scripts/verify_delivery.py、Makefile、AGENTS.md、docs/agent/gates.md、README.md、scripts/output/script-coverage-baseline.txt、scripts/output/stats.json、scripts/output/stats-changelog.json、scripts/output/stats-index.md、site/en/chart-design.html、site/en/methodology-matrix.html、site/en/character-appearance.html、site/en/chapter-stats.html、site/en/relationships.html、scripts/output/_w768_spec.json、docs/00-导读/W批次编号对账表.md、CHANGELOG.md、README.md、STRUCTURE.md、docs/00-导读/项目说明.md、HANDOVER.md、.github/workflows/README.md、site/index.html、site/dukou-engine.html、site/data/tag-cloud.html、site/data/cross-time-danmaku.html、archive/docs/AGENTS-ARCHIVE.md、AGENTS.md、CITATION.cff、scripts/output/file-index.md、scripts/output/_cascade_files_W768.txt。

### W767（2026-10-16）：数据漂移门禁深比对批
> **来源**：用户令「继续」（遗留事项③·W760 审查 F-2 HIGH 门禁口径修复；顺带 F-7 P1 修正）。
> - **G1 门禁 v3（check_data_drift.js）**：增补**共路深比对**——递归遍历双方皆有的键（仅一侧有之键不计·W760 实证 949 项此类系内嵌子集/复合之设计形态）、数组按位对齐、标量严格比对；声明式基线 `scripts/output/data-drift-baseline.txt`（`页面 ⇄ 源 路径`·[N]→[*] 归一化匹配·no-new-drift 语义）；顶层数组长度口径与副本对账保留。
> - **G2 盲区实证（即刻）**：新口径当场暴露审查员深比对未覆盖的存量漂移——① `chapter_stats.json` 陈旧（源文经 W756 修订后未重跑 stats·该文件 gitignored 系本地产物·已重跑对齐 11 回·页嵌为现行值）；② cave-estate「中将级」= 第 38 门禁登记的**旧值标记**（页面全域「妖将级」·dataset 残留旧值）；③ language-style-radar 悟空色 ×2（#e67e22 旧 palette → #C9A063 现行 · 页余项已一致）；④ theological-intervention-network `var(--accent-1)`×5（页内 accent-1 出现 0 次）；⑤ character-relationship-3d kpi 名（悟空 vs 孙悟空）。
> - **F-7 双 KPI（数据自证真值）**：① character-relationship-3d `kpi[4]`——按 links 度数年 孙悟空 12 > 唐僧 7 → 修正 dataset 为「悟空 / 度数 12」（与 kpi[3] 及页嵌同名形）；② journey-map-interactive `kpi[2]`——isHardship 节点实数 8 → 修正 dataset「8」。两处均嵌侧正确、dataset 侧陈旧，双边同步后一致。
> - **81-hardships**：页嵌 3 处 `cause:"mind"` → `"人心自生的魔障"`（页内 label 字典 14 处齐备）；生成器（`C_情节/hardships_81.py`·code 规范）与页面（label 形）之约定分裂 → 基线声明 + 登记独立对齐批。
> - **visual-art**：`visual_art_ideas` 计数 vs 数组——页面注释显证「仅在 EMBEDDED 中」系设计双形态 → 基线声明。
> - **验证（全绿）**：门禁 v3 绿（深层比对一致·基线豁免 244 项）；**负样本实证**（向 radar 注入 #dead00 → 门禁转红且精确到 `$.characters[0].color` 路径 → 恢复转绿）；改页内联脚本后 CSP 重注 **零漂移**（856 页/858 哈希）；**pytest 597 passed**；verify_delivery 全量 48 段 0 FAIL。
> - **登记（独立批）**：hardships_81 生成器 code↔页面 label 约定对齐（含 deployed 副本形态）。
> - **状态**：已提交（本地）。
> - **文件**：scripts/check_data_drift.js、scripts/output/data-drift-baseline.txt（新）、dataset/cave-estate.json、dataset/character-relationship-3d.json、dataset/journey-map-interactive.json、dataset/language-style-radar.json、dataset/theological-intervention-network.json、site/data/81-hardships.html、scripts/output/_w767_spec.json、docs/00-导读/W批次编号对账表.md、CHANGELOG.md、README.md、STRUCTURE.md、docs/00-导读/项目说明.md、HANDOVER.md、.github/workflows/README.md、site/index.html、site/dukou-engine.html、site/data/tag-cloud.html、site/data/cross-time-danmaku.html、archive/docs/AGENTS-ARCHIVE.md、AGENTS.md、CITATION.cff、scripts/output/file-index.md、scripts/output/_cascade_files_W767.txt。

### W766（2026-10-16）：C 类引文静默删改修复批
> **来源**：用户令「继续」（遗留事项③·W760 审查 F-1b HIGH 修复）。审查证据 `tmpe/review-w760/content/c-violations.json` 59 条（sim≥0.7·C 类长引文静默删改·落在第 20 门禁两种语法族之外）。
> - **处置总量**：**51 处修复 + 8 处登记**（涉及 42 件文档；含未 flag 但同引文同形态的 8 件一致性扩散修复）。
> - **修复分类（51 处）**：① 单字/专名——鋋罗→棕罗、翙→躧、兼→咸（×3）、贫僧已发→我已发了（×6）、被父王→我父王（×2）、名山→山、该当何罪→语料原句「该问个钤束不严的罪名」；② 标点/句读——。→，（多处）、顿号→逗号、；→，、你算[，]他该、劫[。]每劫；③ 引号规范——『』→“”（6 条直角引号还原语料形态）；④ 补全截断——可不枉生世界之中[，不得久住天人之内]、咬断铁索走来[，却与朱紫国王消灾也]、晚辈[，元辰是家师的下宾]、托化妖魔[，看你师徒可有真心往西去也]、品级[，如何不好]、尘凡[；一灵真性……变得这般模样]；⑤ 恢复删节——保他家生者安全，亡者超脱（×2）、经不可轻传向时句、即唤阿傩式补字、八戒编谎长句按语料逐字（两处省略号标记）；⑥ 句式按语料——心经「行深般若波罗蜜多，时照见五蕴皆空」（3 文件）、袁守诚卦语「巳时发雷，午时下雨，未时雨足」、太白金星「上届/慈恩」、镇元子观音骂语全句、皇帝轮流做内层引号结构+补全（×4）。
> - **登记不修（8 处·语料疑点）**：① 第002回「惜修**生命**无他说」——遍检版本作「性命」（性命双修），doc 保持「性命」不向语料疑点看齐（×4 条）；② 第007回「**变**罢了」——通行本作「便罢了」，doc 保持「便」（×4 条）。两类均属语料仲裁批（与 007 生/在 重字、我把你/我怕你 同族）。
> - **过程自查（诚实记录）**：初版对「我现四大部洲」按记忆误修为「我观」，逐字核语料后回退——**教训：引文修改必须逐字对语料，禁用版本记忆直觉**（已入批内方法论）。
> - **验证（全绿）**：省略号感知全量核验 **51 合规 + 8 登记 = 59/59 办结**（按……切段·每段逐字为语料子串）；引文门禁 **423 规范引文 + 112 归属对白命中率 100%**（710 文件·修复新增 7 条归属对白全过）；**pytest 597 passed**；verify_delivery 全量 48 段 0 FAIL；级联面 dry-run 十面预检。
> - **状态**：已提交（本地）。W760 审查 4 HIGH 至此 3 项完成（F-1a/F-1b/RCE），余第 9 门禁口径与 validate_en 接线待后续批。
> - **文件**：docs/01-全书逐回解读/第001回-灵根育孕源流出.md、docs/02-人物深度分析/（28 件含方向二深化组/器物传记/外传/专题）、docs/03-主题与情节专题/（13 件）、scripts/output/_w766_spec.json、docs/00-导读/W批次编号对账表.md、CHANGELOG.md、README.md、STRUCTURE.md、docs/00-导读/项目说明.md、HANDOVER.md、.github/workflows/README.md、site/index.html、site/dukou-engine.html、site/data/tag-cloud.html、site/data/cross-time-danmaku.html、archive/docs/AGENTS-ARCHIVE.md、AGENTS.md、CITATION.cff、scripts/output/file-index.md、scripts/output/_cascade_files_W766.txt。

### W765（2026-10-16）：a11y 辅助族注释统一与解析规则拆分批
> **来源**：用户令「现在做」（遗留事项④·W761 报告 §9.3 登记的可选项收尾）。
> - **注释统一（增强审计辅助族）**：`audit_keyboard_navigation` / `validate_aria_completeness` 两函数 docstring 与节头注释统一标注「辅助族·parser 优先签名·不注册于 ALL_CHECKS·被规则 1/3 内部调用」——该族与 40 项规则族（html_content 优先签名）的签名差异此前仅在散落注释中间接可见，现集中声明（W761 决策 D-10 的落档）。
> - **rule_29_parsing 拆分（74 行 → 编排器 + 三检测臂）**：`_parsing_duplicate_ids`（重复 ID·P1）/ `_parsing_unclosed_tags`（未闭合非空元素·返回开放/闭合计数供第三臂复用）/ `_parsing_stray_end_tags`（悬垂结束标签·每标签只报首个）；void/optional-close 标签集合提为模块常量 `_PARSING_VOID_TAGS` / `_PARSING_OPTIONAL_CLOSE`；消息文本与 findings 顺序（①→②→③）逐字保留。
> - **验证（全绿）**：新旧版行为对拍**逐字节一致**——5 夹具（正常/重复 ID/未闭合/悬垂/混合）+ 整页 `audit_file(site/index.html)` findings JSON 全等；a11y 专项 53/53；AST 复扫 rule_29 退出「≥40 行」榜；**pytest 597 passed**（+3 skipped·0 failed）；`ruff check scripts/` 0 告警；verify_delivery 全量 48 段 0 FAIL。
> - **状态**：已提交（本地·未推送）。
> - **文件**：scripts/a11y_audit.py、scripts/output/_w765_spec.json、docs/00-导读/W批次编号对账表.md、CHANGELOG.md、README.md、STRUCTURE.md、docs/00-导读/项目说明.md、HANDOVER.md、.github/workflows/README.md、site/index.html、site/dukou-engine.html、site/data/tag-cloud.html、site/data/cross-time-danmaku.html、archive/docs/AGENTS-ARCHIVE.md、AGENTS.md、CITATION.cff、scripts/output/file-index.md、scripts/output/_cascade_files_W765.txt。

### W764（2026-10-16）：命令白名单 pager 逃逸修复批
> **来源**：用户令「现在做」（遗留事项③·W760 审查 F-11 HIGH·P0 安全修复）。W760 S-01 实证：`xiyouji-agent-web` 的 `run_command` 工具白名单可被 `git grep -O<pager>` 绕过——git 把 pager 交 `sh -c '<pager> "$@"'` 执行（参数未转义），`git grep -Oecho;echo W760_P1>pwned.txt` 在 `shell:false` 下真实落盘（GIT_TRACE + 落盘双证据）→ 任意命令执行。
> - **修复（`server/engine/tools.ts`）**：① git 参数层拦截扩展——`-O`（含 `-O=`/`-O<pager>` 粘连形态）/`--open-files-in-pager`/`--ext-diff`/`--pager=` 统一按 **token** 判定（原 `--no-index`/`--output=` 的裸字符串匹配同批升级为 token 级·兼容粘连）；② 全命令 **shell 元字符二次校验**（防御纵深）：`;` `&` `>` `<` 反引号与换行在参数中一律拒绝——白名单命令的合法参数集（脚本路径/ref/正则/包名）不含这些；`|` 与 `$` 保持放行（git grep 正则交替/锚点属合法用法·设计决策以放行用例钉死）。
> - **修复依据与边界**：`-O` 族是 git 内部再起 shell 的已知入口（同族含 `--ext-diff`/`--pager=`/`-c alias.*=!`——后者因前缀白名单要求子命令位列第二 token 已天然拦截）；shell:false 下 node 侧本无 shell，元字符校验兜底「命令内部再起 shell」的同类逃逸。
> - **单测（`server/engine/tools.test.ts`·+6 例）**：5 拒——`git grep -Oecho;echo pwn`（-O 粘连）·`git grep -O=touch`（=形态）·`git grep --open-files-in-pager=cat`（长形态）·`git log --ext-diff`（同族）·`git grep pwn > evil.txt`（元字符重定向）；1 放行——`git grep "master|main$"`（正则交替/锚点不被误伤·pin 设计决策）。
> - **验证（全绿）**：`node --test server/engine/tools.test.ts` **38/38**（W752 建 30 例 + W764 新增 6 + 前批增 2）；全套服务端 **49/49**（tools+audit+citationGuard）；`tsc --noEmit` 零错；引擎冒烟 `server/engine.smoke.mjs` **12 组断言全绿**；**pytest 597 passed**（本批不涉 Python）；verify_delivery 全量 48 段 0 FAIL。
> - **待用户执行（P0 之二）**：轮换根 `.env` 的 `LLM_API_KEY` 与 `GOATCOUNTER_API_TOKEN`（虽未入库，既是泄露后果也是 RCE 的目标——属凭证操作·工具侧不代持）。
> - **状态**：已提交（本地·未推送）。
> - **文件**：xiyouji-agent-web/server/engine/tools.ts、xiyouji-agent-web/server/engine/tools.test.ts、docs/agent/agent-web.md、scripts/output/_w764_spec.json、docs/00-导读/W批次编号对账表.md、CHANGELOG.md、README.md、STRUCTURE.md、docs/00-导读/项目说明.md、HANDOVER.md、.github/workflows/README.md、site/index.html、site/dukou-engine.html、site/data/tag-cloud.html、site/data/cross-time-danmaku.html、archive/docs/AGENTS-ARCHIVE.md、AGENTS.md、CITATION.cff、scripts/output/file-index.md、scripts/output/_cascade_files_W764.txt。

### W763（2026-10-16）：照录区字级篡改全量修复批
> **来源**：用户令「现在做」（遗留事项③·W760 审查 F-1a HIGH 修复）；审查报告 F-1 清单 15 处 + 本批独立全量比对新增 82 处 = 97 处全量修复。
> - **修复范围**：docs/01 九个回次文件的 `## 原文全文` 照录区（第 20 门禁永久豁免区·自称「原文照搬」但存在字级篡改）——以权威语料（source/原文/分回·与 dataset/text-search.json 逐字一致）为基准，空白归一后 difflib 对拍定位全部字级差异并逐处修复。
> - **修复方法**：独立比对器（`tmpe/w763/w763_f1a_fix.py`）——opcode 级修复按「归一化位置→原文位置」映射回原文施加（保留 span 外原始空白）；逐 span 断言校验；修复后复跑比对器终验 0 残留。
> - **典型修复（97 处）**：① 人名/专名改字——初江王→楚江王、子叉→木吒（12 处）、崔珪→崔珏（6 处）、木呼/木吐→木吒（4 处）、迎叶→迦叶、比丘增→比丘僧（×2）、游憎→游僧；② 实词/用字——般苦→般若、皤桃→蟠桃（3 处）、五帝→玉帝（4 处）、岭旨→领旨、锡枚→锡杖（2 处）、北巨→北俱、南赠→南赡、邪崇→邪祟、奈河→奈何、登极→登基、已时→巳时（2 处）、头防→头陀、暨岭→鹫岭、音沓→音杳、盘龙警→盘龙髻、神珍→神针、好亲→好杀、法天像地→法天相地、四键将→四健将、水廉洞→水帘洞、饶地→饶他、皤→蟠、袛园→衹园、孟兰盆→盂兰盆、与法→与汝、适→违、全→圣、憎→僧、谱→僧（2 处）、钻→钯、入→人、河→何；③ 删字补回——我怕你（漏怕）、法相如是（漏是）、即唤阿傩（漏阿）、喷将出去（漏出）、取经人（漏人）、语末补引号；④ 标点/编码残损——乖猴．→乖猴，、违法．→违法，、．→。（3 处）、￥→栴（货币符号系码位残损）、诗曰:→诗曰：、。”“→：；⑤ 3 处 W756 语料「徵→征」批联动（第068回×2·第091回×1）。
> - **登记不修（两类）**：① 僻字占位符约定 5 处（□【左「鱼」右「便」】类系统性转录约定·非篡改·维持现状）；② 语料 OCR 疑错 2 处（第007回「在因在凡间」「生长生变化」——照录区为正确形态·源文分回含重字 OCR 错误·修语料属仲裁批·本批只登记不传播）。
> - **验证（全绿）**：全量比对器终验 实改残留 0（占位符 5·语料疑点 2 为登记项）；9 文件行尾纯净（全 CRLF·零混尾）；**pytest 597 passed**（+3 skipped·0 failed）；verify_delivery 全量 48 段 0 FAIL；级联面经 batch_cascade dry-run 十面预检。
> - **状态**：已提交（本地·未推送）。F-1b（C 类 59 条·docs/02 为主）与其余 3 项 HIGH（第 9 门禁口径/validate_en 接线/agent-web RCE）待后续批次。
> - **文件**：docs/01-全书逐回解读/第003回-四海千山皆拱伏.md、docs/01-全书逐回解读/第004回-官封弼马心何足.md、docs/01-全书逐回解读/第006回-观音赴会问原因.md、docs/01-全书逐回解读/第007回-八卦炉中逃大圣.md、docs/01-全书逐回解读/第008回-我佛造经传极乐.md、docs/01-全书逐回解读/第009回-袁守诚妙算无私曲老龙王拙计犯天条.md、docs/01-全书逐回解读/第010回-二将军宫门镇鬼唐太宗地府还魂.md、docs/01-全书逐回解读/第068回-朱紫国唐僧论前世孙行者施为三折肱.md、docs/01-全书逐回解读/第091回-金平府元夜观灯玄英洞唐僧供状.md、scripts/output/_w763_spec.json、docs/00-导读/W批次编号对账表.md、CHANGELOG.md、README.md、STRUCTURE.md、docs/00-导读/项目说明.md、HANDOVER.md、.github/workflows/README.md、site/index.html、site/dukou-engine.html、site/data/tag-cloud.html、site/data/cross-time-danmaku.html、archive/docs/AGENTS-ARCHIVE.md、AGENTS.md、CITATION.cff、scripts/output/file-index.md、scripts/output/_cascade_files_W763.txt。

### W762（2026-10-16）：W761 重构报告晋升批
> **来源**：用户令「现在做」（遗留事项②：报告晋升）——W761 重构报告自 tmpe/w761/ 工地转正入 docs/11-方案报告/，完成三连带同步。
> - **报告入库**：`docs/11-方案报告/W761工具链可维护性重构报告-2026-10-16.md`（V3.0 收官版·十节全量：执行摘要/信息基础与假设/执行前计划/执行记录/验收证据/风险与偏差/决策记录/经验沉淀 12 条/可行性自评/附录）——头部已改注晋升说明（原「落点 tmpe 工地·晋升路径见 §9.3」→「已晋升入库·W760 在途障碍已随代收消解」）。
> - **报告内容要点**：四工作流重构（WS1 W536 守卫 14 处重复定义收敛为 utils/path_guard 公共模块·WS2 ccc l2/l2_runtime 26 行重复去重+check_page 拆分[峰值 cx 41→19]·WS3 tmpe_tidy main 三分派+三处去重·WS4 a11y 40 项规则族命名统一 rule_N_topic）+P-02 潜伏缺陷修复（4 工具守卫根改仓库根·用户裁断）；全部经机器对拍验证（pytest 594→600·ccc/tt 输出逐字节一致·守卫导入面对拍·AST 复扫）；另含应用户令代收 W760 的全过程（修其报告 118 行引文+三连带+代走发布链）。
> - **README 索引**：现役 18→19 篇·新报告置顶 #1·全表重编号（1-19 连续性脚本断言）。
> - **STRUCTURE/stats 三连带**：report_docs 标记 21→22·现役文字 18→19 篇·`stats.py --w W762` 刷新（stats-changelog+stats-index 派生）·`--check` 零差异（16 键）。
> - **验证（全绿）**：README 编号连续性断言过（1-19）；stats --check 零差异；级联面经 batch_cascade dry-run 十面预检；**pytest 597 passed**（+3 skipped·0 failed）；verify_delivery 全量 48 段 0 FAIL。
> - **状态**：已提交（本地·未推送）。
> - **文件**：docs/11-方案报告/W761工具链可维护性重构报告-2026-10-16.md、docs/11-方案报告/README.md、STRUCTURE.md、scripts/output/stats.json、scripts/output/stats-changelog.json、scripts/output/stats-index.md、scripts/output/_w762_spec.json、docs/00-导读/W批次编号对账表.md、CHANGELOG.md、README.md、STRUCTURE.md、docs/00-导读/项目说明.md、HANDOVER.md、.github/workflows/README.md、site/index.html、site/dukou-engine.html、site/data/tag-cloud.html、site/data/cross-time-danmaku.html、archive/docs/AGENTS-ARCHIVE.md、AGENTS.md、CITATION.cff、scripts/output/file-index.md、scripts/output/_cascade_files_W762.txt。

### W761（2026-10-16）：工具链可维护性重构批
> **来源**：用户 scene#15「日常开发」重构令（保持原有功能、输入输出及外部接口完全不变，提升可读性与可维护性）+ 19:49 追加令「都做，现在开始做」（a11y 命名体系统一+P-02 潜伏缺陷修复）。动工前 `preflight_check.py --touches` 全绿（对账表 max=W759 → W761 认领·W760 为并行会话在途预留 bullet·交集 0）；W760 收尾批（应用户令「你帮他做完」由本会话代修其报告 118 行引文+三连带+代走发布链·e4ff4faf+e121f53a）先于本批落地，级联编号锚点畅通。
> - **WS1 守卫单模块化**：W536 路径守卫 14 处逐字符重复定义（3 种 root 表达式/2 种根语义/3 处死定义）收敛为 `scripts/utils/path_guard.py` 公共模块——`make_guard(root)` 工厂 + PROJECT_ROOT/SCRIPTS_ROOT 双根显式传参（错误消息与历史实现逐字一致）；13 文件迁移（10 别名导入保原语义·3 死定义删除）；slice_screenshots 测试钉死的 `_W536_ROOT`/`_w536_guard_open` 名以别名保留（12/12 单测未改一字过）。新增 `tests/unit/test_path_guard.py` 6 例（双根放行/双外拒/消息文本/闭包独立性）。
> - **WS2 重复消除+复杂函数拆分**（check_content_consistency.py）：l2/l2_runtime 26 行逐字符重复的比较逻辑提取为 `_compare_embedded_vs_dataset` 公共内核；check_page（60 行·cx=41 全仓峰值）拆为编排器+5 个 `_rule_*` 函数；`js_of`→`extract_scripts`。三模式（--self-test/--gate/--dataset）输出与基线逐字节一致。
> - **WS3 拆分+去重+命名**（tmpe_tidy.py）：scan 优先级链 ⑤⑥ 外提 `_match_classify_rule`；main（68 行）→ `_cmd_tool_candidates`/`_cmd_plan`/`_cmd_apply` 三分发；`_group_by_bucket`（print_rows/write_report）、`_write_report_pair`（两个报告函数）、`_find_callers`（callers 扫描）三处去重；`human`→`human_size`。19/19 单测+CLI 四模式对拍零行为差异。
> - **WS4 命名体系统一**（a11y_audit.py）：40 项规则族统一为 `rule_N_topic`（N=E2-N 注册位序·与 R_* 常量同源）——19 个 check_* 函数改名+测试 38 处同步+规则 27-40 分组注释升级为逐规则注释（贴 def 惯例）；两增强辅助函数（audit_/validate_·parser 优先签名·被规则 1/3 内部调用）保留。53/53 单测；mcp-server 自包含实现不受影响。
> - **P-02 潜伏缺陷修复**（用户裁断）：inject_goatcounter/inject_rum/inject_visit_log/bump_footer_version 守卫根 SCRIPTS_ROOT→PROJECT_ROOT——原 root 与各自 site/ 写面相悖（守卫生效即必炸·仅被幂等跳过掩盖）；功能级验证 4/4（负样本仓外拒·正样本 site/ 写面放行）。**行为变化声明**：当前树态零可观察差异（全页面已注入·走 skip 路径），修复恢复工具 documented 行为。
> - **stats 归口**：report_docs 20→21 的刷新已归 W760 收尾批（其报告件入库·`--w W760`）——本批不含 stats 件。
> - **验证（全绿）**：pytest 594→600 collected（**pytest 597 passed**+3 skipped·0 failed）；`ruff check scripts/` 0 告警；ccc 三模式+tt 四模式 CLI 对拍逐字节一致；守卫导入面对拍根值等价（P-02 四处为批准的预期变更）；AST 峰值 cx 41→19；`stats.py --check` 零差异；a11y 门禁 E2-2 P0/P1=0；verify_delivery 全量 48 段 0 FAIL。
> - **范围纪律**：docs/11-方案报告/ 不碰（该面归 W760 收尾批·已先于本批提交）；不推送远端（推送需用户单独确认）。
> - **状态**：已提交（本地·未推送）；W760 收尾批（e4ff4faf+e121f53a）先于本批落地；完整报告 `tmpe/w761/W761-重构报告.md`（晋升 docs/11-方案报告/ 另议）。
> - **文件**：scripts/utils/path_guard.py、tests/unit/test_path_guard.py、scripts/bump_version.py、scripts/generate_csp.py、scripts/inline_css.py、scripts/slice_screenshots.py、scripts/rag/graph_seed_neo4j.py、scripts/rag/xiyouji_rag.py、scripts/inject_goatcounter.py、scripts/inject_rum.py、scripts/inject_visit_log.py、scripts/bump_footer_version.py、scripts/fetch_gate_stats.py、scripts/lint_links.py、scripts/security_scan.py、scripts/check_content_consistency.py、scripts/tmpe_tidy.py、scripts/a11y_audit.py、tests/unit/test_a11y_audit.py、scripts/README.md、scripts/output/_w761_spec.json、docs/00-导读/W批次编号对账表.md、CHANGELOG.md、README.md、STRUCTURE.md、docs/00-导读/项目说明.md、HANDOVER.md、.github/workflows/README.md、site/index.html、site/dukou-engine.html、site/data/tag-cloud.html、site/data/cross-time-danmaku.html、archive/docs/AGENTS-ARCHIVE.md、AGENTS.md、CITATION.cff、scripts/output/file-index.md、scripts/output/_cascade_files_W761.txt。

### W760（2026-10-16）：全量对抗性审查报告批
> **来源**：并行会话在途批（全量对抗性审查·对抗性审查报告-2026-10-16），应用户令由本会话收尾完成——修报告 118 行归属对白引文（第 20 门禁口径：引号内改逐字节原文、省略号移出引号外）+ 三连带同步（README 索引 17→18 篇·STRUCTURE 标记 20→21·stats --w W760 刷新）+ 干扰日志登记。
> - **审查范围**：3327 入库件·五可标准（可量化/可验证/可执行/可追踪/符合实际）·六个审查面（内容可信度/门禁有效性/数据一致性/工程基础设施/安全/文档治理）。
> - **11 项发现·4 HIGH**：① 引文门禁整改不完整——`## 原文全文` 照录区 17 处字级篡改（13 篇 docs/01·该区系第 20 门禁永久豁免区）+ C 类 59 条（sim≥0.7）静默删改（28 文件·docs/02 为主·落在门禁两种语法族之外）；② 第 9 门禁数据漂移口径全失明；③ validate_en 未接线 + en 站 duration 盲区；④ agent-web `git grep -O` 白名单绕过 RCE。
> - **MEDIUM 1 项**：门禁豁免判定口径缺陷——check_citations.py 演绎豁免只认标题节内 `> 【文学演绎】`，不认文首文件级标记，docs/02-06 外传文类标记在文首第 3 行致 --reverse 100 候选抽样 100% 假阳性；修该脚本属禁擅改清单，需用户批准。
> - **交叉复核更正（重要）**：内容面称 `太白金星-方向二深化.md:23`（sim 0.95）为「说话人被整体改写」——经权威语料逐字核验**归属正确**（第003回说话人确为太白长庚星·对白「臣启陛下，可念生化之慈恩」原文精确存在）；该引文确有 3 处静默删改（省开头长段铺陈·上届→上界·删末尾句不用省略号）——「静默删改」成立、「归属错误」不成立，已按证据更正定性。
> - **明确未发现违规（有证据）**：回次错置 0 条；演绎标注覆盖率 docs/01 的 159 个 SD 小节 100%；涉台/涉港澳表述 0 违规（W737 的 9 处修复经独立复验落实）。
> - **证据与复算**：25 个证据脚本全部 rc=0 可复跑；正面结论独立复算——stats 16 键全对上、引文核验 423 条规范引文 + 105 条归属对白命中率 100%、语料保真 100 回全等、CSP 0 漂移、file:// 88/88。
> - **本会话收尾修正**：报告 118 行归属对白引文形态按第 20 门禁 ATTRIB_RE 口径修正（引号内只留逐字节原文「臣启陛下，可念生化之慈恩」·省略号移至引号外），修正后引文门禁全绿（命中率 100%·709 文件扫描）。
> - **验证（全绿）**：引文门禁 423+105 命中率 100%；stats --check 零差异（16 键）；六文档同步与级联面经 batch_cascade dry-run 十面预检；**pytest 597 passed**（+3 skipped·0 failed）；verify_delivery 全量 48 段 0 FAIL。
> - **状态**：已提交（本地·未推送）；审查发现的 4 HIGH 修复批待用户排期（引文照录区/门禁口径/en 接线/agent-web 安全各需独立批·F-2 脚本修改需用户批准）。
> - **文件**：docs/11-方案报告/全量对抗审查报告-2026-10-16.md、docs/11-方案报告/README.md、STRUCTURE.md、scripts/output/stats.json、scripts/output/stats-changelog.json、scripts/output/stats-index.md、scripts/output/_w760_spec.json、docs/00-导读/W批次编号对账表.md、docs/superpowers/plans/2026-10-14-interference-governance-roadmap.md、CHANGELOG.md、README.md、STRUCTURE.md、docs/00-导读/项目说明.md、HANDOVER.md、.github/workflows/README.md、site/index.html、site/dukou-engine.html、site/data/tag-cloud.html、site/data/cross-time-danmaku.html、archive/docs/AGENTS-ARCHIVE.md、AGENTS.md、CITATION.cff、scripts/output/file-index.md、scripts/output/_cascade_files_W760.txt。

### W759（2026-10-16）：batch_cascade 脚注滚动根修批
> **来源**：用户令「开工」——W758 实证 AGENTS 脚注滚动连续性断言在编号空洞下必炸（被迫手工三步手术逃生），裁定根修不再手工迁档。动工前 `preflight_check.py --touches` 全绿（对账表 max=W758 → W759 认领·交集 0）。
> - **R1 滚动切分断言放松**：`_agents_entry_wn(_keep[0]) == _hi + 1` 假设脚注条目号连续，而编号空洞（W750 作废未产提交·W752/753 由 W751 并行单写）系永久历史→每次真实滚动必 FAIL；改 `> _hi` 严格递增——前序 `sorted(_nums)` 断言仍守乱序防线，新增拦切分边界重复号（负样本夹具实测仍红）。
> - **R2 指针注记刷新锚点失配根治**：滚动后「W###-W### 级联自动滚动·」区间注记刷新用字面锚 `W719 续迁 W708-W714·` 回插，而现役脚注前缀已是 `W713 续迁` 形态→即使断言过注记也静默失新（grep 实证）；改对 token 就地正则替换（保持 W725 单段化语义·仅留最新区间），无 token 时锚「脚注保留最近 5 条」前插并断言锚点在场。
> - **R3 真数据首跑**：本批级联自身即触发真实滚动（脚注 5 条 + 本批 = 6 条 → 迁 W751 入 ARCHIVE 尾块·区间注记就地翻新 W751-W751），修复代码首跑即真数据验证（W717「新锚真数据首跑」同款验证形态）。
> - **防回归（负样本）**：`scripts/output/_w759_negative_check.py`——切分边界重复号夹具（脚注内 W754→W751 造有序重复）实测断言转红「滚动切分乱序」+ 字节级恢复原状断言 + 阳性对照（未变异 dry-run 十面全过）。
> - **验证（全绿）**：`py_compile` 通过；`ruff check` 零违例；负样本真防线 1/1 + 恢复断言过；`batch_cascade --spec` dry-run 十面过 → `--apply` 写后自检全部通过；`verify_delivery.py` 全量 48 段自洽锁 OK。
> - **状态**：已落地并推送 dev；CI 侧以 PR 重跑为准。
> - **文件**：scripts/batch_cascade.py、scripts/output/_w759_negative_check.py、scripts/output/_w759_spec.json、docs/00-导读/W批次编号对账表.md、CHANGELOG.md、README.md、STRUCTURE.md、docs/00-导读/项目说明.md、HANDOVER.md、.github/workflows/README.md、site/index.html、site/dukou-engine.html、site/data/tag-cloud.html、site/data/cross-time-danmaku.html、archive/docs/AGENTS-ARCHIVE.md、AGENTS.md、CITATION.cff、scripts/output/file-index.md、scripts/output/_cascade_files_W759.txt。

### W758（2026-10-16）：CI 首跑暴露缺陷修复批
> **来源**：用户令「写 PR 进行合并」——PR #45（dev→main·W728-W757 共 64 提交弧线）首次真实 GitHub Actions 运行，26 项检查暴露 2 处必红 + 4 条 high 告警；**Delivery Gate 在首跑通过 = W757 接线修复（Playwright 安装）实测有效**。动工前 `preflight_check.py --touches` 全绿（对账表 max=W757 → W758 认领·交集 0）。
> - **F1 pytest 平台假设用例（CI 必红 1/2）**：`tests/unit/test_tmpe_tidy.py::test_check_same_volume` 断言「不存在的 `Z:` 盘 → 不同卷」依赖 Windows 盘符语义；POSIX `os.path.splitdrive` 恒返回空串（任何路径恒判同卷）→ Linux runner 上 `is False` 必败。修复=盘符断言加 `os.name == "nt"` 守卫，同卷正断言保留全平台覆盖。
> - **F2 markdown 依赖漏登记（CI 必红 2/2）**：`scripts/build_reader.py` 顶层 `import markdown`，本地环境已装而 `scripts/requirements.txt` 未登记 → CI `pip install -r requirements.txt` 后第 42 门禁根级脚本可导入性测试（`test_root_script_is_importable[build_reader.py]`）`ModuleNotFoundError` 必红。修复=requirements 补 `markdown==3.10.2`（本地实测版钉版）。
> - **F3 两门禁脚本 CodeQL 加固（high 告警 2/4）**：① `check_chart_values.js` `stripJsComments` 的 `<script>` 剥离正则无 `i` 标志（大写 `<SCRIPT>` 变体漏剥·Bad HTML filtering regexp）→ 加 `gi`；追加提交两轮收敛结束标签通配形态至 `<\/script[^>]*>`（CodeQL 变体告警两轮：空白 `</script >`→换行加属性 `</script\t\n bar>`·否定类天然跨换行一发覆盖）；实跑对拍 87 页 V1-V5 判据分布与改前逐项一致（0 FAIL·20.3s）。② `check_seo_head.py` R5 占位域名裸子串检测（incomplete URL substring sanitization）→ 改带左边界负向断言正则 `(?<![\w-])example\.com`（`notexample.com` 不再误报·`www.example.com` 仍命中）；实跑 855 页通过。
> - **F4 归档件告警豁免（high 告警 2/4·范围纪律）**：`archive/scripts/batches/w6xx/_w672_var_drift.py` 与 `archive/scripts/w286_merge_yuanwen_shendu.py`（铁律 9 禁重跑件）同报 Bad HTML filtering regexp——归档冻结件不改写（§11.2 精神），走 GitHub CodeQL 警报豁免（won't fix·注明一次性归档脚本不在现役管线）。
> - **F5 HANDOVER 当前 HEAD 句锚点修复（级联 dry-run 拦截·W757 遗留结构缺陷）**：实读磁盘发现「当前 HEAD = W757（…）」句内混入游离右括号与 W756 尾串残留 55 字（W757 批写 HANDOVER 时旧句未整段替换所致），致 batch_cascade 锚点正则 `[^）]*；详见 CHANGELOG）` 失配 fail-closed（防线实证有效）；本批按「先修复交接文档结构再级联」先例手工清残留（W756 内容在 CHANGELOG/对账表全量在档·零丢失）后重跑级联。
> - **验证（全绿）**：`pytest tests -q` **591 passed / 3 skipped**；`ruff check` 改动 py 全过；`node --check check_chart_values.js` 通过；`check_seo_head.py` **855 页通过**；`check_chart_values.js --gate` **0 FAIL**（87 页 / 20.3s·判据分布与改前一致）；`verify_delivery.py` 全量 48 段自洽锁 OK。
> - **状态**：代码面已落地并推送 dev；CI 侧以 PR #45 重跑为准，绿后按用户令合并 main。
> - **文件**：tests/unit/test_tmpe_tidy.py、scripts/requirements.txt、scripts/check_seo_head.py、scripts/check_chart_values.js、docs/00-导读/W批次编号对账表.md、scripts/output/_w758_spec.json、scripts/output/_w758_rotate.py、scripts/output/_cascade_files_W758.txt、CHANGELOG.md、README.md、STRUCTURE.md、docs/00-导读/项目说明.md、HANDOVER.md、.github/workflows/README.md、site/index.html、site/dukou-engine.html、site/data/tag-cloud.html、site/data/cross-time-danmaku.html、archive/docs/AGENTS-ARCHIVE.md、AGENTS.md、CITATION.cff、scripts/output/file-index.md。

### W757（2026-10-16）：CI 门禁接线缺陷修复批
> **来源**：用户令「对项目工程基础设施薄弱点取证并修复」——本 session 对用户三轮共 22 条论断逐条实读磁盘对拍（结论：已消解 8 / 证伪 6 / 成立 8），并**新发现四条用户未提及的硬缺陷**。动工前 `preflight_check.py --touches` 全绿（对账表 max=W756 → W757 认领·交集 0）。审计报告见 [docs/11-方案报告/工程基础设施薄弱点审计报告-2026-10-16.md](docs/11-方案报告/工程基础设施薄弱点审计报告-2026-10-16.md)。
> - **D1 第 43 门禁 CI 必红（最高优先级）**：`verify_delivery.py` 第 43 槽委托 `check_chart_values.js --gate`，该脚本第 904 行硬依赖 `require('playwright')`；而 `ci.yml` 的 verify-delivery job 只装 Python + Node，**从未安装 Playwright**（`scripts/node_modules` 被 `.gitignore` 忽略）。缺失即 `MODULE_NOT_FOUND` → `main().catch` 打印「1 FAIL」→ `_StrictGate` 记 FAIL → `verify_delivery.py` 整体 FAIL。**违反项目 E36-E42 铁则②「门禁建置即绿」**。修复=该 job 补 `actions/cache` 浏览器缓存（复用 W421 模式·key 绑 `scripts/package-lock.json`）+ `npm ci --prefix scripts` + `npx playwright install --with-deps chromium`。
> - **D2 W752 安全单测未接线**：`xiyouji-agent-web/package.json` 的 `test:server`（tools.test.ts 权限边界 / audit.test.ts 审计落盘 / citationGuard.test.ts 引文守卫）在**全部 workflow 中零引用**，CI 只做 build + golden-evals（结构校验）。修复=`agent-web-build` job 补 `npm run test:server` 步骤（本地实测 44/44 通过·0.5s）。
> - **D3 安全扫描盲区**：`security_scan.py` 的 `discover_files()` roots 不含 `xiyouji-agent-web/`、exts 不含 `.ts/.tsx/.mjs`——对「能读写仓库文件、运行脚本」的 React+Express 服务（项目自身认定的安全风险最集中处）**零覆盖**（全文件 grep `agent-web` 命中 0）。修复=roots 增 agent-web、exts 增三扩展名，并加 `_is_agent_web_build_artifact()` 按 `.gitignore` 同一契约排除 tsc 编译产物（`server/*.js`、`server/engine/*.js`、`vite.config.js` 及其 `.d.ts`），使**扫描面 == 入库面**。实测扫描面 1122 文件、agent-web 源文件 43 个入面、`high=0`（与改前基线一致）。
> - **D4 放大因子（登记·未修）**：本地 HEAD `2c1ec6cd`（W756）领先公开 `main` `80f77dd3`（W727）**63 个提交**，W728-W756 全部未推送，故 D1-D3 长期未被 CI 暴露，同时公开侧不存在 W751-W753 三批防护——解释了用户论断中 14 条失准（读的是 W727 快照）。推送属远端写操作，列范围外交用户决策。
> - **防回归（负样本验证）**：新增 `tests/unit/test_ci_wiring.py` 9 例 + `tests/unit/test_security_scan.py` 4 例。判据**锚定 `run:` 块命令体**而非字符串存在性——首版只做存在性断言时负样本实测**假绿**（把 `run:` 改成 `echo skipped` 后关键字仍在步骤名里），加固后 `scripts/_w757_negative_check.py` 四个负样本（摘 playwright 安装 / 摘浏览器缓存 / test:server 改 echo / 摘第 43 门禁挂载）**全部转红·真防线 4/4**。
> - **范围纪律**：不动 `verify_delivery.py`（§11.2 经用户确认清单）·不改 CHANGELOG 历史段·不改 `overrides` 依赖策略·不推送积压提交。
> - **验证（全绿）**：`pytest tests/unit/test_ci_wiring.py` **9 passed**；`pytest tests/unit/test_security_scan.py` **16 passed**；`_w757_negative_check.py` **真防线 4/4**；`security_scan.py --all` **high=0**（1122 文件）；agent-web `npm run test:server` **44 passed**；`check_chart_values.js --gate` 本地 **0 FAIL**（87 页 / 20.2s）；`verify_delivery.py` 全量 48 段自洽锁 OK。
> - **状态**：代码面已落地；**CI 侧效果待推送后验证**（本 session 无 origin 推送授权）。

### W756（2026-10-16）：人名用字语料纯度批
> **来源**：用户对 W699 A-04 盘点报告（[人名用字两态盘点-魏征-2026-10-11.md](docs/10-方法论沉淀/人名用字两态盘点-魏征-2026-10-11.md)）三选项的裁决——令「现在做」，执行其建议的**选项 3（仅清语料）+ 选项 2（口径登记）**。动工前 `preflight_check.py --touches` 全绿（对账表 max=W755 → W756 认领）。
> - **T1 选项 3 清语料（10 字 / 5 容器）**：`魏徵`→`魏征` 于 ① 权威源 `source/原文/分回/第068回.md`（2 处·唐三藏复述引语内）+ `source/原文/分回/第091回.md`（1 处）+ `source/原文/shendu/SD039.md`（1 处·分析性文字混入）；② **镜像容器同改**——`dataset/text-search.json`（3 处·第 20 门禁语料保真检对拍源）+ `site/static/js/text-search-app.js`（3 处·页面内嵌语料副本，W691 三容器纪律：分回 md + dataset json + app 内嵌）。改用一次性断言脚本 `scripts/output/_w756_corpus_fix.py`（逐文件先断言旧值数恰为预期再替换·拒绝盲改）。**语料面残留自检 0 处**。
> - **T2 选项 2 口径登记**：[统计口径说明.md](docs/00-导读/统计口径说明.md) 新增 **§7 人名用字口径**——语料与引文层强制简体「魏征」（权威源 + 两镜像容器）；散文与展示面两态并存**不作强制**（docs/02-04 散文、docs/01 原文照录区、dataset 可视化数据、site 页面对两种写法均予接受），并明确「任何批次禁以统一用字为名批量改展示面（全仓统一约 400 处属选项 1·未经作者裁决不得执行）」；附机器防线说明（第 20 门禁三检 + 改语料必须三容器同改）。
> - **T3 回填与索引**：盘点报告「处置选项」节补**执行记录**（改字范围/验证/边界/选项 1 仍待裁决）；[docs/10 README](docs/10-方法论沉淀/README.md) 索引第 20 行同步（原「W754 校：选项 3 至今未执行」→「W756 已执行选项 3+2」）。
> - **T4 边界声明（如实记账）**：展示面一律未动——含 `docs/01` 第068回/第091回的**原文照录区**（与语料同源但属展示面，3 处 `魏徵` 保留）、`docs/02`-`docs/04` 散文、`dataset/*.json` 可视化数据（underworld-power-network / music-structure / text-evolution）、`site/**` 页面（reader 页与可视化页）；全仓展示面 `魏徵` 存量按 W699 盘点口径（site 徵:征≈202:112）保持不变。
> - **验证（全绿）**：`check_citations.py --check-corpus` **语料保真通过**（text-search.json 100 回与分回逐回全等·语料面残留 0）；`check_citations.py --dir docs` **423 条规范引文 + 104 条归属对白命中率 100%**（705 文件扫描）；`node --check site/static/js/text-search-app.js` 通过；`dataset/text-search.json` JSON 合法（100 回）；`generate_csp.py --check` 856 页 / 858 内联哈希 **0 漂移**；verify_delivery 全量 48 段自洽锁 OK。
> - **状态**：已落地（级联+提交后以 gh run list 为准·本批未推送）。
> - **文件**：source/原文/分回/第068回.md、source/原文/分回/第091回.md、source/原文/shendu/SD039.md、dataset/text-search.json、site/static/js/text-search-app.js、docs/00-导读/统计口径说明.md、docs/10-方法论沉淀/人名用字两态盘点-魏征-2026-10-11.md、docs/10-方法论沉淀/README.md、docs/00-导读/W批次编号对账表.md、scripts/output/_w756_corpus_fix.py、scripts/output/_w756_spec.json、scripts/output/_cascade_files_W756.txt、CHANGELOG.md、README.md、STRUCTURE.md、docs/00-导读/项目说明.md、HANDOVER.md、.github/workflows/README.md、site/index.html、site/dukou-engine.html、site/data/tag-cloud.html、site/data/cross-time-danmaku.html、archive/docs/AGENTS-ARCHIVE.md、AGENTS.md、CITATION.cff、scripts/output/file-index.md。

### W755（2026-10-16）：方法论深度篇扩建与治理口径统一批
> **来源**：用户对 W754 审计报告「仍待拍板」四项的拍板（① 4 篇新增深度篇全建 ② 文档规范 §11 补分流行 ③ pitfalls 计数统一 ④ HANDOVER「三」指针化；推送项裁定暂不推送）。动工前 `preflight_check.py --touches` 全绿（对账表 max=W754 → W755 认领·交集零命中）。
> - **T1 四篇深度篇新增（docs/10-方法论沉淀/）**：① **[批次交付流水线](docs/10-方法论沉淀/批次交付流水线.md)**——取号认领→前置核验→施工→spec 三检→10 面级联→分级门禁→提交与收官 七步链（每步命令 + 判据 + 常见失败）+ **编号锚点三形态**（正常/跳号·合并段/递延补登记，含 W754 实证：max 停在 W751 时级联断言「批次号应为 W752」拒跑）+ 行尾与编码纪律（混行尾 fail-closed·CRLF-blob 文件须 `git -c core.autocrlf=false add`·NUL/BOM 禁）+ 失败模式速查表；② **[治理文档分层与按需查表](docs/10-方法论沉淀/治理文档分层与按需查表.md)**——L0 指针层/L1 摘要层/L2 全量层/L3 归档层四层职责与体量纪律 + 阅读契约三型（索引/通读/查表）+ 第 41 门禁四查 + 数字与指针纪律（W520/W704/标识符禁令）+ W754 反面案例四行；③ **[可视化数据正确性断言方法论](docs/10-方法论沉淀/可视化数据正确性断言方法论.md)**——三层既有防线盲区（第 24 槽只静态自洽·Python 模拟测试不验真实渲染·截图只看布局）+ 方法论四件套（真实渲染 file:// / **双签名稳定等待**防 count-up 中途值 / **先普查后定阈** p00=0.82·p05=2.8→S/L≥0.5 / 基线冻结 + fail-closed + na 缺口报告）+ 五判据 V1-V5 + 建线六步 + 适用边界；④ **[多 Agent 干扰治理与 touches 纪律](docs/10-方法论沉淀/多Agent干扰治理与touches纪律.md)**——N×p×T 暴露面（p 已被级联压低·T 为主）+ 机制三件套（touches 声明 / `preflight_check --touches` 交集拒绝 / safe_commit pathspec 互斥）+ 登记口径（该列/不列）+ **拦不住的两件事**（T 可见性/解析鲁棒性）+ 四批复现案例（含 W754 三写方 18 文件零交集实证）。四篇均按本目录体例：问题背景/方法论/判据/复现案例/关联文档，无元信息块需求（第 18 门禁扫描面仅 docs/01-06，[check_frontmatter.py](scripts/check_frontmatter.py) 实证）。
> - **T2 文档规范 §11 补分流权威条文**：[文档规范](docs/00-导读/文档规范.md) §11.1 管控表新增「辅助·索引」行（`docs/11-报告复盘/README.md` = 报告篇数唯一权威）+ 新增**目录分流规则（W755 成文）**四规则——按面向时态判定：报告/复盘/审查/调研 → `docs/11-报告复盘/`；可复利方法论深度篇 → `docs/10-方法论沉淀/`；学术投稿候选 → `docs/S2-学术投稿/`；已退役报告 → `archive/docs/复盘报告/`；边界件（复盘+清单混合体）以「是否承载可复用判据」定归属。同时把 touches 冲突声明块的「上表 8 类文件」改为「上表文件」（新增行后计数失效）并互链新深度篇。
> - **T3 pitfalls 计数口径统一**：三处不一（AGENTS §4.3 写 33 / 六节标题声明合计 34 / 顶层条目实测 38）→ 按**口径=各节顶层「- **」条目数**统一为 38：git/提交/并发节标题 8→12（其余五节声明与实测一致）；AGENTS §4.3 阅读契约 33→38、六主题目录计数 9/3/7/4/4/4→9/5/12/4/4/4 并就地注明口径与本次校正。
> - **T4 HANDOVER「三」指针化**：[HANDOVER.md](HANDOVER.md) §三新增**入口契约（W755）**——新经验按分工登记到现役载体（规则类→AGENTS §4.3/§6 或 pitfalls.md；门禁口径→gates.md；深度篇→docs/10 目录；批次级→CHANGELOG 现役段；子项目→agent-web.md），并声明其下 W### 条目为历史沉淀存档（截至 W691·按 E2 保留原值不再续写）；AGENTS §7 接手路径第 5 步同步改指针版。
> - **T5 索引与计数联动**：docs/10 README 目录索引 20→24 行（新增 21-24·报告指针顺延 25）；`Subagent盲信铁律.md` 内「本目录 19 篇主题」改引用式（防再次漂移）；`docs/INDEX.md` 重建（689 篇/12 板块）；stats 三件刷新（`methodology_docs` 20→24·`--w W755`）。
> - **验证（全绿）**：lint_links docs/10 229 链接 0 broken；check_index_health 通过（方法论 README 覆盖 23/23 主题）；check_doc_sync 第 31 门禁 0 FAIL；check_agents_layers 第 41 门禁 0 FAIL（三方编号 43=43=43）；verify_delivery 全量 48 段自洽锁 OK；纯 md 改动零 site 逻辑面（页脚/版本行为级联自动写）。
> - **状态**：已落地（级联+提交后以 gh run list 为准·本批未推送）。
> - **文件**：docs/10-方法论沉淀/批次交付流水线.md、docs/10-方法论沉淀/治理文档分层与按需查表.md、docs/10-方法论沉淀/可视化数据正确性断言方法论.md、docs/10-方法论沉淀/多Agent干扰治理与touches纪律.md、docs/10-方法论沉淀/README.md、docs/10-方法论沉淀/Subagent盲信铁律.md、docs/00-导读/文档规范.md、docs/agent/pitfalls.md、AGENTS.md、HANDOVER.md、docs/00-导读/W批次编号对账表.md、docs/INDEX.md、scripts/output/stats.json、scripts/output/stats-changelog.json、scripts/output/stats-index.md、scripts/output/_w755_spec.json、scripts/output/_cascade_files_W755.txt、CHANGELOG.md、README.md、STRUCTURE.md、docs/00-导读/项目说明.md、.github/workflows/README.md、site/index.html、site/dukou-engine.html、site/data/tag-cloud.html、site/data/cross-time-danmaku.html、archive/docs/AGENTS-ARCHIVE.md、CITATION.cff、scripts/output/file-index.md。

### W754（2026-10-16）：方法论目录口径整改批
> **来源**：用户令「docs/10-方法论沉淀 文件内的所有文件内容有需要更新或者新增的吗」——四组并行只读审计（18 篇逐件核 + 交叉复核）产出「必修 4 类 / 建议改 8 类 / 仍准确 4 篇 / 新增候选 4 篇」清单，用户裁定执行 B 范围（必修 + 建议改 + 索引重写·新增深度篇另行拍板）。动工前 `preflight_check.py --touches` 全绿（对账表 max=W753 → W754 认领）。
> - **T1 必修（结论级纠错·4 类）**：① **页面更名漏同步**——`narratology-13d-network` → `narratology-16d-network` 全目录 10 处（[可视化测试计划](docs/10-方法论沉淀/可视化测试计划-十七维叙事学图谱.md) 9 + [README 索引](docs/10-方法论沉淀/README.md) 1）：W700 断链清债只扫 docs/03 与 docs/S2，**docs/10 漏在 sweep 外**；第 38 门禁扫描面仅 site HTML 与 docs/01 md，且这些路径写在反引号内非 markdown 链接——lint_links 全绿也照放行（三重盲区实证）。② **agent-web 迁移评估结论反转**——原文 §零/§四「不合并·暂不迁移·ignore 未解除」已作废：迁移 W543-W548 落地、W568 关闭、`.github/dependabot.yml` 的 ignore 规则已删（2026-09-05 注释实证）、现役栈实测 TS 7.0.2 / Vite 8.3.1 / React 19.3.0 / Express 5.2.1 / Tailwind 4.3.3 / better-sqlite3 13.0.3；文件降级为历史评估档案。③ **记忆研究七处 line 锚点失效**——行号空间随语料分回化消失（`source/原文` 最长文件 302 行，全库无 >1000 行语料），定位策略改「回目 + 精确引文」（第 20 门禁 `check_citations.py` 对 `dataset/text-search.json` 精确子串）。④ **上游 skill 协议层失联声明**——三 skill 全局路径实测断链（junction 目标不存在）且仓内 `skills/` 已 W562 退役，10 篇文件的「上游 skill」节统一改指仓内载体（AGENTS.md §4.3/§6 + CLAUDE.md + docs/agent/*.md）。
> - **T2 建议改（口径与自洽·8 类）**：[README 索引](docs/10-方法论沉淀/README.md) 重写（报告篇数改引用式·复利经验总览表标注 W086 快照并指向 HANDOVER 三·「与上游 skill 关系」节改订为「与协议层/现役载体的关系」·维护规则补报告分流与载体铁律）；[E1 铁律](docs/10-方法论沉淀/E1铁律.md) 计数自洽（头部 23/23 vs 节标题 21/21 两值不一 → 去掉易漂移总分·以明细表为准）；[双索引改造](docs/10-方法论沉淀/双索引可追溯改造.md) 补 W700+ 索引边界与 W711 段形态 + 仓外 memory 链接改内链 + §六 手工维护规则标注工具化；[前端 SOP](docs/10-方法论沉淀/前端显示问题诊断SOP.md) 门禁对照表补槽号（第 8/9/10/11 槽）与表注（三个 `_` 前缀脚本降级为手动取证·实测无 CI 引用）+ 补第 43 槽；[白屏三连](docs/10-方法论沉淀/白屏三连根因复盘与防回归清单.md) 清单逐条标落点（第 10/11/24/43 槽）并标出唯一未落地项（`inline_css.py` 输出后括号校验）；[人机创意工作流](docs/10-方法论沉淀/人机创意工作流方法论.md) backlog 落地状态回填（第 19 槽 `check_glossary.py`·第 43 槽 `check_chart_values.js`）；[markdown 写作规范](docs/10-方法论沉淀/markdown写作规范.md) 补阅读契约标记例外与现役写作权威指针；[可视化测试计划](docs/10-方法论沉淀/可视化测试计划-十七维叙事学图谱.md) 补 P2 基线现状（基线已建·图像 diff 未引入）与 KPI 口径分歧提示。
> - **T3 范围纪律**：纯 md 改动（18 件·零 site/scripts 代码面）；历史值一律保留（E2 铁律）——新增说明就地并入既有小节，禁尾增速记段；两件判定「仍准确」不动（创意三明治工作流·人名用字两态盘点，后者系 W737 唯一登记保留在本目录的报告件）。
> - **T4 新增候选（未开工·待拍板）**：批次交付流水线（preflight_check + batch_cascade + release_prep + safe_commit 链路）/ 治理文档分层与按需查表（W707/W709 + 第 41 门禁）/ 可视化数据正确性断言方法论（W753 三层防线）/ 多 Agent 干扰治理（W739-W741 touches 纪律）——四篇深度篇登记为候选，本批不建；另记「报告/方法论分流规则未入文档规范 §11 管控表」为权威位缺口。
> - **T5 顺带修复三处仓库结构缺陷（级联前置取证发现问题·非本批原计划）**：① **W751 段头重复**——CHANGELOG 第 21/22 行为同一行 `### W751（…）`，使 batch_cascade 的「现役段标题行首唯一」断言失败、任何后续批次级联都无法运行（手工级联遗留），已去重；② **NUL 字节污染 2 处**——W736 批 spec 的 `\u0000` JSON 转义在落盘时被写成**真 NUL 字节**（CHANGELOG W736 段 + file-index W736 段各 1），两文件被编辑器判为二进制且 `check_edit` 类工具拒绝写入，已还原为字面 `\u0000` 转义（修复脚本 `scripts/output/_w754_fix_nul.py`·幂等）；③ **W752/W753 段缺失**——两批已收官（对账表有行·CHANGELOG 无段），依「条目文本由 Lead 在 W751 收官后插入」的既定约定补登记 CHANGELOG 段 + file-index 段（内容取自对账表行，来源逐段标注「递延补登记」），使 CHANGELOG 编号规则上限推进到 W754 与 file-index 段一一对应（第 17 门禁复绿）。④ **现役版本行递增数字收敛**——级联 desc 中的「19 篇」按 W520（递增数字禁字面量）改为不漂移表述（README/STRUCTURE/项目说明/HANDOVER/workflows README/四页脚共 12 处）。行尾保真：CHANGELOG/file-index 两文件 HEAD blob 为 CRLF，暂存用 `git -c core.autocrlf=false add` 保持，零整文件行尾翻动。
> - **验证（全绿）**：lint_links docs/10 182 链接 0 broken；check_doc_sync 第 31 门禁 0 FAIL；check_index_health 通过（方法论 README 覆盖 19/19）；verify_delivery 门禁全量 OK；行尾保真（16 件 LF 保持 LF·README 与双索引两件保持 CRLF·零混尾）；pytest 不变（纯 md）。
> - **状态**：已落地（级联+提交后以 gh run list 为准）。
> - **文件**：docs/10-方法论沉淀/README.md、docs/10-方法论沉淀/DRL真循环.md、docs/10-方法论沉淀/三skill闭环.md、docs/10-方法论沉淀/E1铁律.md、docs/10-方法论沉淀/E2文档同步区分历史vs现役.md、docs/10-方法论沉淀/Preflight与Subagent模板.md、docs/10-方法论沉淀/Subagent盲信铁律.md、docs/10-方法论沉淀/agent-web技术栈迁移评估.md、docs/10-方法论沉淀/dispatching-parallel-agents四subagent并行模式.md、docs/10-方法论沉淀/前端显示问题诊断SOP.md、docs/10-方法论沉淀/双索引可追溯改造.md、docs/10-方法论沉淀/可视化测试计划-十七维叙事学图谱.md、docs/10-方法论沉淀/并行Edit竞态问题.md、docs/10-方法论沉淀/改动后影响面扫描.md、docs/10-方法论沉淀/人机创意工作流方法论.md、docs/10-方法论沉淀/markdown写作规范.md、docs/10-方法论沉淀/白屏三连根因复盘与防回归清单.md、docs/10-方法论沉淀/记忆研究理论框架应用方法论.md、docs/00-导读/W批次编号对账表.md、AGENTS.md、HANDOVER.md、README.md、STRUCTURE.md、docs/00-导读/项目说明.md、CHANGELOG.md、CITATION.cff、.github/workflows/README.md、scripts/output/file-index.md、scripts/output/_w754_spec.json、scripts/output/_w754_fix_nul.py、scripts/output/_cascade_files_W754.txt。

### W753（2026-10-15）：可视化数据正确性断言批（第 43 门禁）
> **来源**：用户对项目三项薄弱点取证裁决之第三项——「87 个可视化页的渲染值 ↔ 页面数据源一致性无机器防线」。**递延补登记**：本段由 W754 批依对账表 W753 行补入（原批与 W751/W752 同会话并行收官，按同批约定「门禁面与文档面归 W751 单写、条目文本由 Lead 在 W751 收官后插入」，本段即该插入动作的落地）。
> - **T1 断言器（scripts/check_chart_values.js）**：Playwright `file://` 直开（禁起本地服务）+「图元数 + KPI 文本」双签名稳定等待（只数元素会采到 count-up 中途值·实测 chapter-stats 采到 96/100）逐页真实渲染，覆盖 87 个 site/data 可视化页。
> - **T2 五判据**：V1 无 pageerror（数据装载失败第一信号）/ V2 视图非空（SVG 图元·2D 画布像素·Three 场景子对象·表格行·DOM 数据项任一 > 0）/ V3 数据量级自洽（best-fit 数组长度 L 与图元数 S 满足 S/L ≥ 0.5·全站普查 p00=0.82·p05=2.8）/ V4 KPI 可复算（`[data-value]`/`.kpi-value` 类数字须由数据源复算·近失配差 <2% 而不等 = FAIL·对不上记 na 缺口禁静默跳过）/ V5 数据源四要素（复用第 28 槽 C1-C4·缺失只计缺口不 FAIL）。
> - **T3 基线冻结与缺口报告**：`scripts/output/chart-values-baseline.txt`（87 页 × 6 项 = 522 行·基线外新增/回归/图元数跌破 50% 恶化 = FAIL）+ `scripts/output/chart-values-report.json`（na 逐页逐条）+ fail-closed（探针异常/超时/未产出 → PROBE 与 V1-V5 全 FAIL）。**门禁面与文档面归 W751**：`scripts/verify_delivery.py`、`docs/agent/gates.md`、`AGENTS.md` 由 W751 批次单写，本批只提交条目文本。
> - **T4 E2E 扩面**：`tests/unit/test_visualization_data.py` + `tests/e2e/test_visualization_assertions.js`。
> - **验证**：87 页 20s（5 workers）·0 FAIL·0 probe_error；缺口 V3 9 页 / V4 17 页 / V2 1 页（逐页原因见报告）；门禁终态 43 槽（同会话 W751 段 T6 记录）；第 43 槽定义见 docs/agent/gates.md。
> - **状态**：已收官（0f4b0849 + 0827a401 收尾）。
> - **文件**：scripts/check_chart_values.js、scripts/output/chart-values-baseline.txt、scripts/output/chart-values-report.json、tests/unit/test_visualization_data.py、tests/e2e/test_visualization_assertions.js。

### W752（2026-10-15）：Web Agent 安全加固批
> **来源**：用户对项目三项薄弱点取证裁决之第二项——「Web Agent 工具面即攻击面」。**递延补登记**：本段由 W754 批依对账表 W752 行补入（同 W753 约定：门禁面归 W751 单写·条目文本后插）。
> - **T1 tools.ts 安全单测（30 例）**：工具面权限边界、参数校验与越界拒绝逐项断言（`server/engine/tools.test.ts`）。
> - **T2 写操作持久化审计**：新增 `server/audit.ts`（audit.jsonl 落盘）+ `/api/audit` 查询端点 + `server/audit.test.ts`。
> - **T3 细粒度写入允许域**：`AGENT_WEB_WRITE_SCOPE` 限定可写目录，白名单外拒绝（与权限四模式配合）。
> - **T4 门禁面归 W751**：`scripts/verify_delivery.py` 由 W751 批次单写，本批不列 touches、只提交条目文本。
> - **验证**：安全单测与审计单测全绿；文档面 `docs/agent/agent-web.md`、`SECURITY.md`、`xiyouji-agent-web/README.md`、`.env.example` 同步；同会话终态见 W751 段验证栏。
> - **状态**：已收官（d55e0479）。
> - **文件**：xiyouji-agent-web/server/engine/tools.ts、xiyouji-agent-web/server/engine/tools.test.ts、xiyouji-agent-web/server/index.ts、xiyouji-agent-web/server/audit.ts、xiyouji-agent-web/server/audit.test.ts、xiyouji-agent-web/package.json、xiyouji-agent-web/.env.example、xiyouji-agent-web/README.md、docs/agent/agent-web.md、SECURITY.md。

### W751（2026-10-15）：根级工具链防护批（第 42 门禁挂载）
> **来源**：用户对项目的三项薄弱点取证裁决（内容生产体系完成度高、工程基础设施最薄）之第一项——「为根级工具脚本补齐专项测试与门禁覆盖」。开工前实读磁盘取证：scripts/ 根级 101 个非 `_` 脚本做四面引用普查（tests ∪ verify_delivery ∪ CI workflow ∪ Makefile），**46/101 四面无引用**；用户点名的三件（new_page.py 页面脚手架 / embed_json.py JSON 嵌入器 / slice_screenshots.py 截图切片器）逐个复核成立——它们直接生成或改写站点产物，却既无专项测试也不被任何门禁点名。
> - **T1 三件专项测试（tests/unit/，共 44 例）**：①`test_new_page.py`（16 例）——P1 占位符全替换 / P2 模板缺失快速失败 / P3 name 白名单（`../evil`、`a/b`、大写、空格、中文、空串全拒）/ P4 索引条目插入位置（必须落 A-AH 区块第一个 `</ul>` 内且无关区块零损）/ P5 锚点缺失只警告不误写 / P6 dry-run 零写入 / P7 `--no-index` 不碰导航 / P8 重跑字节一致 + 零外域；路径三分（TEMPLATE/OUTPUT_DIR/INDEX）全部改道 tmp_path，末尾专用用例断言真实 site/index.html 未被触碰。②`test_embed_json.py`（16 例）——E1 括号深度边界（防贪婪截断）/ E2 JSON 字符串内 `{}` 不破坏深度计数 / E3 insert 三形态排版 + 产出仍是合法 JSON / E4 ensure 注入点（head→body→EOF 三级）/ E5 replace 只动目标键值 / E6 键名边界（`note` 不得命中 `note_extra`）/ E7 退出码契约 1/2/4 实测 + E8 备份语义（默认 `.bak`、`--no-backup` 不刷新）/ E9 中文不转义。③`test_slice_screenshots.py`（12 例）——S1 切片几何（2000/800 → 3 片且末片 400px·丢尾=页脚盲区）/ S1c 条纹图逐片取色证「按 y 递进」/ S2-S3 命名顺序与 posix 相对路径 / S4 clean_dir 只删 png 不递归 / S5 W536 守卫（scripts/ 外必拒且零落盘·内侧放行）/ S6 索引报告两视口 + 索引行与磁盘切片一一对应 / S7 重跑无残留；CLI 端到端必须落 scripts/ 内（守卫语义：`--output-dir` 不是逃逸口），用唯一子目录 `scripts/output/_w751_slice_probe/` 并自清。
> - **T2 根级 import 冒烟层（tests/unit/test_tool_scripts_cli.py·91 例）**：对全部根级脚本逐个动态 import（语法/依赖/import 期副作用三条底线），3 个 import 期即执行面/需外部资源的脚本走显式豁免表（`verify_delivery.py` / `pre_release_screenshot.py` / `pre-commit-validate.py`，每条写清理由且校验陈腐行）。**实测发现**：动态 import 必须先把模块注册进 `sys.modules`——`@dataclass` 经 `cls.__module__` 回查，不注册会误报 `AttributeError: 'NoneType' object has no attribute '__dict__'`（optimize-html-size.py 即此型假阳性）。
> - **T3 第 42 门禁挂载**（scripts/check_script_coverage.py + verify_delivery 第 42 槽 + `scripts/output/script-coverage-baseline.txt`）：覆盖口径=四面引用任一；C1 新增脚本四面无引用且未登记=FAIL（新增漂移即拦）/ C2 基线陈腐与重复行=FAIL / C3 fail-closed 下限（脚本 ≥50·覆盖集 ≥15·豁免集 ≥10）。存量冻结 35 条豁免**逐行注明四类理由**（①一次性/取证/人工审阅 ②会话直接执行 ③发布链/CI 编排 ④浏览器/布局），--self-test 6/6。**建线前后对比：46/101 四面无引用 → 68 四面引用 / 35 登记豁免 / 0 FAIL**。stats `gate_count` 41→43 经第 31 门禁 C5d 当场抓出并 `stats.py --w W751` 刷新（stats.json + changelog + index 三件），README 标记数字同步。
> - **T4 判据收窄（如实记账·本批最重要的负面结论）**：原拟用 `--help` 做 CLI 冒烟，全量普查（8s 超时逐个实测）发现 **17 个脚本忽略 `--help` 直接执行主逻辑**——`inline_css.py --help` 真重写了 857 个站点 HTML 的行尾、`export_design_tokens.py --help` 真改了 design-tokens.json 的 generated 日期，另有 `acceptance_snapshot.py` / `gen_sitemap.py` / `verify_delivery.py` 三个 `--help` 下直接跑全量主逻辑直至超时。**结论：根级脚本普遍没有「参数解析失败即退出」的 CLI 契约**，属系统性缺陷（本批不修但已登记为待办）；连带损伤已逐文件取证并 `git restore` 复原（623 个 site 页面 + rss.xml + 观测基线 + design-tokens + dataset 两件，全部零内容差异仅为行尾改写）。故第 42 门禁判据收窄为纯 import 面 + 四面引用面，不假装验证 CLI 契约。
> - **T5 门禁自身缺陷（自证价值实证）**：基线解析首版未剥行内分类注释，35 行豁免被全判「scripts/ 下无此文件」→ 门禁自伤 70 FAIL；该缺陷由本批自带单测（tests/unit/test_check_script_coverage.py 10 例，含 G1 现网 0 FAIL / G2 self-test / G3 报告模式 / G4 四类判据注入 / G5 基线纪律与「门禁自身不得登记豁免」）当场拦下。parser 修好后补 T6 回归用例（self-test 5→6 例）。
> - **编号说明（跳号批）**：W750 经前置实验证伪作废且**未产生提交**（见对账表 W750 行），故本批直接取 W751；batch_cascade 的编号锚点按「现役段 max+1」推导无法表达跳号，按 pitfalls「手工级联（跳号/合并段批）」先例执行，并自建 scripts/output/_cascade_files_W751.txt 清单。
> - **T6 并行批合流与终态数字**：批内与 W753（可视化数据断言）并行推进，两批的 verify 槽位与 AGENTS/gates.md 条目在同一工作树合流——**第 43 槽 check_chart_values.js 的 verify 挂载由本批统一执行**（`_StrictGate` 补 `runner` 字段以支持 node 门禁，默认 py 保既有 15 段行为不变），第 43 槽实测 87 页 / 0 FAIL / 22.7s；门禁终态 **43 槽**（结构=EXPECTED_SECTION_NAMES 48 段自洽锁 48==48），stats gate_count 41→43 二次刷新。
> - **验证（终态全量）**：新增 6 个测试文件共 **162 例**（new_page 16 + embed_json 16 + slice_screenshots 12 + import 冒烟 91 + 门禁自测 10 + 可视化数据 18·3 skip=登记豁免）；**pytest 559 passed / 3 skipped**（批前基线 415·净增 144）；ruff scripts/ 0 错；**verify_delivery 全量 48 段 0 FAIL·核心全绿**；第 42 门禁 self-test 6/6；第 43 门禁 0 FAIL；check_agents_layers 0 FAIL（三方编号 43=43=43）；check_doc_sync 0 FAIL；stats --check 零差异；check_w_range_literal 0 漂移；CSP 856 页 0 漂移。
> - **发现（未修·如实记账·含一次自身勘误）**：本机 `pytest tests` 存在**汇总行打印完成后进程不退出**的既有现象（本批改为 `--ignore` 逐文件/分组跑以取得退出码）。**勘误**：本条初稿把该现象归因于 `tests/unit/test_tmpe_tidy.py`，依据仅是该文件单独跑亦「无输出」——但 harness 以进程退出取输出，**「无输出」不足以证明是该文件**；并行批实测「去掉其测试文件同样复现」，故原判据不成立、归因撤销。现象本体（汇总后不退出·疑非 daemon 线程/句柄未释放）仍未定位，与本批改动无因果关系，建议单独立项排查——本批不掩盖、不假绿。
> - **（原验证记录保留）**：新增测试文件初版 145 例全绿；ruff scripts/ 与新增测试文件 0 错（tests/ 存量 17 项历史 ruff 发现不在 CI lint 轨内·未动）；第 42 门禁 0 FAIL·self-test 6/6；check_agents_layers 0 FAIL（三方编号 42=42=42）；check_doc_sync 0 FAIL；stats --check 零差异（16 键）；check_w_range_literal 0 漂移。
> - **状态**：已落地（级联+提交后以 gh run list 为准）。
> - **文件**：scripts/check_script_coverage.py、scripts/output/script-coverage-baseline.txt、scripts/verify_delivery.py、tests/unit/test_new_page.py、tests/unit/test_embed_json.py、tests/unit/test_slice_screenshots.py、tests/unit/test_tool_scripts_cli.py、tests/unit/test_check_script_coverage.py、scripts/output/stats.json、scripts/output/stats-changelog.json、scripts/output/stats-index.md、README.md、AGENTS.md、docs/agent/gates.md、docs/00-导读/文档规范.md、docs/00-导读/W批次编号对账表.md、HANDOVER.md、scripts/output/file-index.md。

### W749（2026-10-15）：ML 坑族防守补登批
> **来源**：第 40 篇复盘报告 A-02 行动（用户令开工）——W746 当日两坑从 MEMORY 补登进仓库 pitfalls（MEMORY 与日志均有完整记录·本批为仓库级固化）。
> - **T1 运行时节补两条（docs/agent/pitfalls.md）**：①**子线程首次 import 段错误**——http.server handler 子线程首次 import torch/ST → SIGSEGV exit 139 静默死亡（实证：/route 54s empty reply·服务静默终止）→ 服务端必须主线程启动预热（rag_server main 的 _get_router 范式）；②**ruff --fix isort 破坏 ST 顺序**——isort 排序规则把 plain import（torch）排到 from-import（sentence_transformers）之前·改坏「ST 先于 torch」关键顺序致 CLI 静默段错误（实证：--fix 后管道+tail 掩盖退出码·PIPESTATUS 才抓到 139）→ ML 脚本 ST import 块必须 `# noqa: I001` 防守。
> - **T2 查坑表补行**：shell 场景查坑表补「ML 脚本开跑前」行——五查（去 shebang / ST 先于 torch / noqa: I001 防守 / 子线程预热 / PIPESTATUS 验退出码）。
> - **T3 计数联动**：运行时节计数 3→5·AGENTS.md §4.3 坑位计数 31→33 同步。
> - **T4 检查单沉淀**：ML 脚本开跑前检查单（第 40 篇报告 S-38 任务卡）随 pitfalls 条目正式化。
> - **验证（全绿）**：纯 md 追加·pytest 415 不变；ruff scripts/ 全过；verify_delivery 全量四十六段 OK；check_doc_sync 0 FAIL。
> - **状态**：已落地（级联+提交后以 gh run list 为准）。
> - **文件**：docs/agent/pitfalls.md、AGENTS.md、docs/00-导读/W批次编号对账表.md、HANDOVER.md、scripts/output/file-index.md、scripts/output/_w749_spec.json、scripts/output/_cascade_files_W749.txt。

### W748（2026-10-15）：第40篇复盘入库批
> **来源**：用户提供「工作复盘与优化分析系统提示词」·第十一次执行（第 40 篇）——当日 W743-W747 五批收官周期复盘。
> - **T1 报告入库**：docs/11-报告复盘/工作复盘与优化分析报告-2026-10-15.md（十节+附录 A-E）——① 执行摘要（19:00-20:40 双线周期·11 提交）② 信息基础（I-01~06+ASM-01~04）③ 经验复用 8 项（E-01~08·微批安全模式/ML 三件套/发布链五步/证伪入档等 P0 级）④ 技能优化 3 项+skill-creator 任务卡（S-36 路由评测方法论/S-37 负面结果处置/S-38 ML 排错）⑤ 未用技能 4 项全暂缓（各有触发条件）⑥ 场景沉淀 3 个（SC-01 实验→入库/SC-02 负面收口/SC-04 评审闭环）⑦ 问题 10 项+8 问题族 FAM-23~30+PRE-31~39（代理直连 fallback/主线程预热/noqa 防守/PIPESTATUS/全量提交/先诊断后方案等）⑧ 工作流 2 条（WF-01 实验闭环瓶颈识别/WF-02 评审链）⑨ 行动 A-01~07（W748 编号改由本篇消费·原路由版改写候选顺延）⑩ 可行性自评（总体可行）·附录=批次弧线/四证伪数据卡/分差谱/假设清单/术语表。
> - **T2 索引与统计三连锁**：docs/11-报告复盘/README.md 索引加行（新报告编 1·原 1-15 顺延·现役 15→16 篇）+ STRUCTURE.md report_docs 标记 16→17（「现役 16 篇」文字同步）+ stats.py --w W748 派生三件刷新。
> - **T3 编号说明**：W748 原为「路由版改写批」预留候选——本篇复盘入库先行消费该号；路由版改写仍为后续候选（触发条件=dukou 要 top-1 直跳·不变）。
> - **验证（全绿）**：报告数据全部可溯源（git log 11 提交+实验区 tmpe 原始数据+当日日志）；pytest 415 不变（纯文档批）；ruff scripts/ 全过；verify_delivery 全量四十六段 OK；check_doc_sync 0 FAIL。
> - **状态**：已落地（级联+提交后以 gh run list 为准）。
> - **文件**：docs/11-报告复盘/工作复盘与优化分析报告-2026-10-15.md、docs/11-报告复盘/README.md、STRUCTURE.md、scripts/output/stats.json、scripts/output/stats-changelog.json、scripts/output/stats-index.md、docs/00-导读/W批次编号对账表.md、HANDOVER.md、AGENTS.md、scripts/output/file-index.md、scripts/output/_w748_spec.json、scripts/output/_cascade_files_W748.txt。

### W747（2026-10-15）：RAG 系统能力清单入库批
> **来源**：W746 收官后的整合动作（用户提供整合草稿·事实校核后落盘）。**编号说明**：W747 原计划为「路由排序加权批」·经前置实验（title 加权零效果/IDF 加权负效果·第四条证伪）后用户裁定「A 主 B 待触发」不开工·编号改用于本沉淀批。
> - **T1 README 扩写（scripts/rag/README.md）**：新增「系统能力总览与已知边界」节——①能力总览表（四档指标/主链 @5 0.487/智能路由 +0.041 至 0.528/路由 21 题/向量产物规模）②端点表（/query /graph /health /route·含懒加载语义）③**四条证伪清单**（MMR 敌我不分/长文本补足 −0.25/HyDE 嵌入桥≠重排桥/线性加权字面同权）④四条体系性边界（导语连续性/多 gold 天花板/C 类语义桥/路由 top-1 词汇鸿沟）⑤分差三层（毫厘不动作/中大都待/数量级靶子）⑥**元模式**（语义鸿沟领域线性方法失效·防下一轮重复投入）⑦资产索引（代码/产物/评测集/两坑）。
> - **T2 事实修正五处**（草稿校核）：①「+0.041」明确为智能路由形态增益（默认全改写实为 −0.032 负）②启动命令统一 py -3.12（ML 档需要·裸 python 仅零依赖档）③eval_compare 位置修正为实验区 tmpe（未入库）④图谱数据文件名修正为 dataset/yuanqi-graph.json ⑤端点表补 /route 懒加载语义。
> - **T3 沉淀价值**：recipe card/证伪清单原在 tmpe 实验区（gitignored）——实验区清理即知识断档；本批把「能做什么/不能做什么/怎么启动」固化为仓库件·后续会话与维护者可直接读。
> - **验证（全绿）**：README 结构与既有节无冲突（追加式·LightRAG 对照/档位/硬件纪律原样保留）；ruff/门禁不受影响（纯 md）；verify_delivery 全量四十六段 OK。
> - **状态**：已落地（级联+提交后以 gh run list 为准）。
> - **文件**：scripts/rag/README.md、docs/00-导读/W批次编号对账表.md、HANDOVER.md、AGENTS.md、scripts/output/file-index.md、scripts/output/_w747_spec.json、scripts/output/_cascade_files_W747.txt。

### W746（2026-10-15）：语义页面路由端点批
> **来源**：T-01 Phase-0 ST-06 转正（用户批准开工）——路由原型 21 题分层评测过目后走标准批次。
> - **T1 路由端点（rag_server.py）**：新增 /route?q=（懒加载 page_router·只读 87 页 title/desc 向量缓存·不触发 1077 篇 RAG BM25 索引）；/health 解绑索引（status + routes 数·dukou-engine 不消费 docs 字段已实证）。
> - **T2 模块转正（page_router.py）**：从 tmpe 实验区晋升 scripts/rag/——路径参数化（__file__ 定位）、缓存迁 scripts/output/（page_vectors.npy + page_index.json·gitignored）、CLI 三态（查询 / --eval / --rebuild）。
> - **T3 工程修复（两个实证坑）**：①路由模型主线程预热——torch/ST 在 handler 子线程首次 import 段错误（exit 139 静默死亡·实证）②ST-before-torch 顺序防回归——ruff --fix 的 isort 曾把顺序改坏致 CLI 段错误（noqa: I001 防守·已沉淀记忆）。
> - **T4 单测**：test_page_router.py 九例（题层判定 / title 清洗 / top-N 命中·纯函数零重依赖）。
> - **T5 评测与文档**：21 题分层评测回归与实验区一致（基线 top-1/top-3 均 9/10 持平·评测集 top-1 12/19 top-3 16/19·探针 R19/R21 miss 符合预期·难题 R20 top-1 命中）；README 语义页面路由节；recipe card 补 R17/R18 召回缺口与「无语义证据=机械口径无证据·语义待测」重定义（T-01 报告·本地件）。
> - **验证（全绿）**：CLI 冒烟 + /route 端点端到端（0.4s·预热版稳定）；pytest 415 passed；ruff scripts/ 全过；verify_delivery 全量四十六段 OK。
> - **状态**：已落地（级联+提交后以 gh run list 为准）。top-1 精度优化（泛词主导·中等层 2/8）留后续批次。
> - **文件**：scripts/rag/page_router.py、scripts/rag/rag_server.py、scripts/rag/README.md、tests/unit/test_page_router.py、.gitignore、docs/00-导读/W批次编号对账表.md、HANDOVER.md、AGENTS.md、scripts/output/file-index.md、scripts/output/_w746_spec.json、scripts/output/_cascade_files_W746.txt。

### W745（2026-10-15）：改写智能路由批
> **来源**：W744-6b 全量验证落地（用户令「全量 30 条跑一次改写对照」+「难例才调 LLM」）——7 条难查询的乐观结论经全量修正：改写默认全量 @5 −0.032（难层 +0.096 vs 简单层 −0.144·direct 型 −0.184）；按型路由模拟 @5 +0.041、@10 +0.107（逼近 Oracle 上界 0.707）。本批把路由实装进 rewrite 档，并附 W744 计数更正。
> - **T1 智能路由（should_rewrite）**：新增短实体判据——长度 ≤6 汉字、无「的」结构、无疑问词 → 短实体（跳过改写直走主链）；否则走改写并池。判据与评测集 direct 标签 30/30 一致（小样本·后续可用更多数据校准）。
> - **T2 接线（rewrite 档）**：retrieve_ranked 内路由——短实体不调 LLM（省改写调用与二次重排）、退化为主链（rerank 档行为）；跳过时 stderr 提示「智能路由：短实体查询→主链」。
> - **T3 单测与文档**：test_rag_enhance.py 扩十二例（短实体/描述句/「的」结构/疑问词/长度边界）；README rewrite 档行与说明更新（全量路由后 @5 +0.041 / @10 +0.107）。
> - **附：W744 计数更正**：W744 段旧计数 390 系离线预置四例加入前的数值，已更正为 394（CHANGELOG/HANDOVER/AGENTS/_w744_spec 四面同步随本批入库）；教训=新增测试落地后须重跑全量再定稿验证行计数。
> - **附：仓库卫生**：.gitignore 增 本地工具目录忽略（本地记忆/自动化文件所在工具目录·此前未忽略·本批实测 add -A 会误暂存·已撤出改显式清单）。
> - **验证（全绿）**：双冒烟——「白骨精」短实体跳过改写（stderr 提示+主链精准命中）、「把师徒四人装进袖子里的老道士」走改写（Q24 治愈复现·top2=镇元大仙）；pytest 406 passed；ruff scripts/ 全过；verify_delivery 全量四十六段 OK。
> - **状态**：已落地（级联+提交后以 gh run list 为准）。
> - **文件**：scripts/rag/rag_enhance.py、tests/unit/test_rag_enhance.py、scripts/rag/README.md、docs/00-导读/W批次编号对账表.md、HANDOVER.md、AGENTS.md、scripts/output/file-index.md、scripts/output/_w745_spec.json。

### W744（2026-10-15）：检索增强集成批
> **来源**：T-01 Phase-1 集成（用户令「开始」）——T-01 检索增强实验（30 查询评测集）验证过的管线正式集成进 scripts/rag：四档开关 + 向量构建工具 + 离线优先加载，完成从实验区（tmpe/hf-poc）到正式工具链的工程化落地。
> - **T1 增强引擎（新增 rag_enhance.py）**：稠密召回（bge-small-zh-v1.5·页级 max）+ 加权 RRF 池融合（bm25×1.0 + dense×2.0·k=60）+ cross-encoder 重排（bge-reranker-base·v1 导语 800 字配方）+ LLM 查询改写并池（原池 ∪ 改写池·按改写查询重排）；实测冠军 recall@5 0.487（三十查询）。
> - **T2 档位开关（RAG_ENHANCE·xiyouji_rag 分派）**：off（默认·零依赖行为零变化）/ dense / rerank / rewrite 四档；非法值 fail-fast；缺依赖/缺产物报修复指引；off 档不加载任何重依赖。
> - **T3 向量构建（新增 build_vectors.py）**：分块复刻 T-01 口径（同语料同算法·逐条一致实证）+ 微批嵌入（1500/冷却 35s/温度守护 90°C 中止/断点续跑）+ manifest 防混批 + 产物三件（rag_vectors.npy / rag_chunks.jsonl / rag_embed_meta.json）+ 陈旧检测（docs 指纹·加载时告警）。
> - **T4 离线优先加载（受限网络防护）**：HF 缓存探测→import 前预置 HF_HUB_OFFLINE=1（huggingface_hub offline 判定为 import 期常量·实测运行时设置无效）；本机代理证书链环境实证修复（etag 检查卡死）。
> - **T5 单测与文档**：test_rag_enhance.py 二十九例（档位解析/RRF 权重/并池/改写清理/映射/离线预置）；README 检索增强档节（四档实测表+启用步骤+硬件纪律）+ .env.rag.example 同步 + LLM_MODEL 示例更正 deepseek-flash；.gitignore 加向量产物忽略。
> - **验证（全绿）**：四档冒烟全通（off 零变化 / dense 38s / rerank 54s / rewrite 89s·治愈 Q29 池外查询）；pytest 394 passed；ruff scripts/ 全过；verify_delivery 全量四十六段 OK。
> - **状态**：已落地（级联+提交后以 gh run list 为准）；首建正式向量产物为后续运营动作（全量嵌入·重计算·硬件安全模式·待用户批准）。
> - **文件**：scripts/rag/rag_enhance.py、scripts/rag/build_vectors.py、scripts/rag/xiyouji_rag.py、tests/unit/test_rag_enhance.py、scripts/rag/README.md、scripts/rag/.env.rag.example、.gitignore、docs/00-导读/W批次编号对账表.md、HANDOVER.md、AGENTS.md、scripts/output/file-index.md、scripts/output/_w744_spec.json、scripts/output/_cascade_files_W744.txt。

### W743（2026-10-15）：检索融合层消融重构批
> **来源**：T-01 Phase-0 实测结论落地（用户令「开始」）——五系统对照实证现役检索融合层退化：四路等权 RRF 被「标题命中」「短语位置」两路异质榜单稀释（recall@5 0.239 vs 纯信号 0.367）。本批为纯代码批：融合层消融重构 + 实测验证。
> - **T1 融合层消融重构**：xiyouji_rag.retrieve 融合层由「四路等权 RRF」改为「加权 RRF（A 原始 BM25 ×1.0 + B 别名扩展 BM25 ×EXPANDED_WEIGHT=0.5）」；「标题命中」（_heading_hits）与「短语位置」两路移除；_rrf 支持 weights 参数（zip strict 等长校验）。决策依据=二十一组融合变体扫描（两轮 11+10 次运行·探索性脚本 tmpe/hf-poc/scripts/fusion_sweep.py·本地实验区）：四路全融 0.217~0.239 vs A+B 0.347~0.367（recall@5·十八查询）；B 权重 0.3~0.6 为实测平台·取中值 0.5。
> - **T2 实测验证（T-01 阵法复跑·十八查询）**：现役 bm25 recall@5 0.239→0.359（+50.2%）· recall@10 0.338→0.467（+38.2%）· MRR 0.343→0.603（+75.8%）；直接型 MRR 0.519→0.938；间接型 recall@5 0.141→0.261。评测数据与基线存 tmpe/hf-poc/ 实验区（本地）。
> - **T3 单测**：tests/unit/test_rag_fusion.py 新增四例（等权缺省/权重缩放/零权跳过/共识优先）。
> - **T4 干扰日志**：治理路线图 §8 追加开工观测行（非本会话 staged 暂态·确认为并行会话在途提交现场·损失零）。
> - **验证（全绿）**：pytest 361 passed；ruff scripts/ 全过；verify_delivery 全量四十六段 OK；T-01 评测复跑前后对照完整（基线 JSON 已备份）。
> - **状态**：已落地（级联+提交后以 gh run list 为准）。
> - **文件**：scripts/rag/xiyouji_rag.py、tests/unit/test_rag_fusion.py、docs/superpowers/plans/2026-10-14-interference-governance-roadmap.md、docs/00-导读/W批次编号对账表.md、HANDOVER.md、AGENTS.md、scripts/output/file-index.md、scripts/output/_w743_spec.json、scripts/output/_cascade_files_W743.txt。

### W742（2026-10-15）：复盘落地与引文门禁双向扩展批
> **来源**：用户三项裁决（2026-10-15：A-01 漏标反向扫描立项·PRE-25 中文计数纳入首版不接受 TODO·fix_quotes 随批归档）+ 第 39 篇复盘报告随批入库（第 38 篇先例）。动工前 preflight 五检（fetch 502 走 GitHub API 降级核验远端顶 5b7550b7 与本地一致·取号 W742·touches 申报七面无在途交集）。
> - **T1 第 39 篇复盘报告入库四连锁**：docs/11-报告复盘/工作复盘与优化分析报告-2026-10-14.md 落库（复盘系列迁移 11 目录首篇·三新族 FAM-20/21/22+PRE-25~30+裁决回填 10 处）+ README 索引 15 篇（新报告编 1·原 1-14 顺延·脚本断言）+ STRUCTURE report_docs 15→16 双同步 + stats --w W742 三件刷新。
> - **T2 S-35 漏标反向扫描器（A-01 落地）**：check_citations.py 新增 --reverse 模式（判据=文档规范 §4.12 逆向：未标记节内 ≥15 字引号内容与归属对白对全书语料未命中率 ≥50% 且样本 ≥2 → 候选·排除原文照录/延伸思考/已标节·规范引文行不抽）+ --fail-on-candidates 收紧开关 + self-test 扩 3 例（正向回归/对抗检出/真句零误报·9→12）；dry-run 底数=101 篇 11 候选节全部 100% 未命中（H1 跨回连载节与聚合文档子节两类结构盲区·公文体/口语形态不在检查 2 语法族）→ 11 处全部补标（050/051/052/054/062/063/084/085/086/087+100 回 3.3 节·批量脚本幂等+计数断言）→ 复扫 0 候选收敛。
> - **T3 PRE-25 release_prep 第四检（双形态）**：--check-spec 新增「②验证行计数对账」——changelog_body「pytest N passed」与 agents_note 中文计数双写一致+与 --pytest-count 实跑数对账（P-01/P-11 三类失真全拦）；新增 zh_num_to_int 中文数字转换器（零~万·段首十兜底/零占位语义·三百一十三=313）；单测扩至 30 例（含 W737 失真回放必拦/双写失步/缺双写/无声明 SKIP/截断风险）；CLI 级验证：失真态回放 FAIL·W741 真实 spec（338/三百三十八）OK。
> - **T4 fix_quotes 归档**：tmpe/review/fix_quotes×4 → archive/scripts/batches/w7xx/（gitignore 区纳管后移动·archive/README 台账 540→544+tmpe 晋升注记）——第 39 篇报告 SC-02/K-04 裁决落地。
> - **T5 文档件（PRE-26/28/30）**：gates.md 第 8 门禁补重建操作规程四连注（build_reader→inline_css→generate_csp→chapter-stats EMBEDDED 重灌）+ 文档规范新增 §4.13 源-产物同修原则 + HANDOVER §九交接流程增第 7 条质量分层声明模板（四行表）。
> - **T6 reader 重建四连（PRE-26 规程首跑）**：build_reader 622 页 → inline_css（102 reader 页重内联·全站 330 INLINED 恢复）→ generate_csp（856 页/858 哈希）→ chapter-stats 双源实测豁免（统计源不含 docs 标记行·漂移 0——第 4 步按门禁实测决定·四连规程价值实证）。
> - **验证（全绿）**：check_citations 三检全过（423 规范引文+104 归属对白 100% 命中·700 文件·语料保真 100/100）+ --reverse 复扫 0 候选 + self-test 12/12；pytest 357 passed；ruff scripts/ 全过；CSP 零漂移；chapter 双源一致。
> - **状态**：已落地（级联+提交后以 gh run list 为准）。
> - **文件**：docs/11-报告复盘/工作复盘与优化分析报告-2026-10-14.md、docs/11-报告复盘/README.md、STRUCTURE.md、scripts/output/stats.json、scripts/output/stats-changelog.json、scripts/output/stats-index.md、scripts/check_citations.py、scripts/release_prep.py、tests/unit/test_release_prep.py、archive/scripts/batches/w7xx/fix_quotes.py、archive/scripts/batches/w7xx/fix_quotes2.py、archive/scripts/batches/w7xx/fix_quotes3.py、archive/scripts/batches/w7xx/fix_quotes4.py、archive/README.md、docs/agent/gates.md、docs/00-导读/文档规范.md、HANDOVER.md、docs/00-导读/W批次编号对账表.md、docs/01-全书逐回解读/（10 件：S-35 反向扫描漏标补演绎标记）、site/reader/（622 页重建）、scripts/output/_w742_spec.json、scripts/output/_cascade_files_W742.txt。

### W741（2026-10-14）：干扰治理评估固化与 touches 加固批
> **来源**：用户三段裁定——① 评估部分不需要优化（逐类核对做了原分析没做的实证·N×p×T 补实测·W671 关键纠正·四个不做钉死范围），但该内核此前只存在于会话中未入库；② 实施叙述从操作流水重排为「交付加存量缺陷加活教材」三段；③ 狗粮击穿 startswith 不是修一下就好——解析层设计缺陷需加固并固化为回归。
> - **T1 评估与实施记录报告新建**：docs/11-报告复盘/多Agent干扰治理评估与实施记录-2026-10-14.md——§0 核心结论（touches 拦不住的两件事：并行会话认领前已改完=T 问题对策是可见性非锁；对账表格漂移击穿解析=鲁棒性已加固闭环）；§1 评估结论（逐类核对 16→5 已覆盖/4 值得做/7 登记收敛表加 N×p×T 实测——p 已被 batch_cascade 压过 T 为主要暴露面·write_receipt 与 --since 定位从加锁纠正为让窗口与漂移可见——加 W671 关键纠正加四项动作与四个不做）；§2 W739 实施三段（机制交付加存量缺陷三项表：对账表历史行五列不齐/文档规范相对链接少一层 W734 同款/startswith 击穿——加活教材并行会话抢跑 A 类实证验证 T 推论）；§3 touches 边界与加固（startswith→replace 双星→re.sub 全星号空白三段加固史加固定 token 方案不采纳理由）；§4 待办指向路线图不重复维护。
> - **T2 报告 README 索引**：现役 13→14 篇（新报告按时间倒序插编号 1·原 1-13 顺延 2-14·脚本处理含断言）。
> - **T3 is_inflight 加固**：replace(双星) 剥不到单星（*已收官* 形态仍误判）——升级 re.sub(r"[\s*]+","") 全量剥离星号与空白，任意强调/空白变体不影响判定；回归测试扩充单星/多星/空白/带 hash 六形态（test_inflight_with_bold_status_variants·单测 11→12 例）。
> - **验证（全绿）**：pytest 338 passed；ruff scripts/ 全过；verify_delivery 全量 46 段 OK；stats report_docs 14→15 三件刷新；索引脚本断言（计数/顺延/编号 1 位）全过。
> - **状态**：已落地（级联+提交后以 gh run list 为准）。
> - **文件**：docs/11-报告复盘/多Agent干扰治理评估与实施记录-2026-10-14.md、docs/11-报告复盘/README.md、scripts/preflight_check.py、tests/unit/test_preflight_check.py、docs/00-导读/W批次编号对账表.md、scripts/output/stats.json、scripts/output/stats-changelog.json、scripts/output/stats-index.md。
### W740（2026-10-14）：干扰治理路线图文档批
> **来源**：用户令「把穷举分析优化成决策加实施文档——做减法不做加法」，并给出七点问题诊断（信息过载/优先级缺实测依据/机制纪律学术未分层/缺生命周期/核心策略未前置/时间与恢复维度未进路线/减量缺失）与「只改三处」「只做一件事」收敛指令。本批纯内容批（单文档入库·无代码无门禁变更）。
> - **T1 路线图文档新建**：docs/superpowers/plans/2026-10-14-interference-governance-roadmap.md（约 110 行八节）——① 决策摘要五条（不追求零干扰/暂不 worktree/唯一写路径第一原则/只对高频高损建机制/机制必须有生命周期）；② 总纲（干扰三要素与不可能三条件加频率模型 N×p×T 加唯一写路径优于多写者加对账表升级为调度表）；③ 度量前置：两周干扰日志（2026-10-14 至 10-28 窗口·表内嵌文档追加式·N p T 度量产出与三档判定规则——度量驱动 P1 触发而非拍脑袋）；④ 实施路线 P0 六项（touches 与串行总纲两项标注已落地·并发禁区清单/单一 IDE/子代理允许写清单/干扰日志四项待推）加 P1 三项（write_receipt 加 agent_start 漂移提示加环境快照·均按日志观测触发）加 P2 五项（低频等事件）；⑤ 不建机制清单（逻辑时钟/worktree/事件溯源/不变式收敛/OS 锁/跨机一致性·升级条件=三个月两次）；⑥ 验收与退出（四运行指标加三退役条件——机制三月无事件降坑位/门禁半年无命中评估退役/S 卡关闭半年复核）；⑦ 季度减量周期（首个窗口 2027-01·五砍项）；⑧ 附录原十六类收敛为四组映射（G1 共享状态写冲突/G2 环境工具隔离/G3 操作纪律/G4 结构变更独占）加干扰日志表（首行已登记 W738 收官窗口险情·零损失）。
> - **T2 对账表**：W740 认领行（纯内容批·touches 空）。
> - **验证（全绿）**：pytest 338 passed；ruff scripts/ 全过；verify_delivery 全量 46 段 OK（级联前 C4-f 时序 FAIL 属预期）；对账表行列数断言通过（认领脚本）。
> - **状态**：已落地（级联+提交后以 gh run list 为准）。
> - **文件**：docs/superpowers/plans/2026-10-14-interference-governance-roadmap.md、docs/00-导读/W批次编号对账表.md。
### W739（2026-10-14）：多 Agent 干扰治理 touches 机制批
> **来源**：用户下发多 Agent 同仓协作干扰治理长文评估（A 至 P 十六类加第一性原理 N×p×T 框架）并裁定实施推荐项①「touches 字段加交集拒绝」。动工前 preflight 全绿（max=W738 → W739 认领）；动工中实证 A 类读→写窗口漂移：并行会话在两次 git 调用间完成 W738 主提交与 chore 并推送 origin/dev（本会话只读验证未造成损坏），即本批机制要拦的真实场景。
> - **T1 对账表扩 touches 列**：92 数据行加列（历史行留空·空集不参与交集判定；W687/W688 两行历史 5 列不齐行补空列至标准 7 列·内容零改动）；表头规则三句化四句新增④ touches 冲突声明条款（手工共享面登记·级联面由 batch_cascade 单写路径保护不列·对账表追加认领行不列·结构性修改必须列）；W739 认领行登记 5 项 touches。
> - **T2 preflight_check.py 第 6 检**：parse_ledger 扩展返回 rows（w/status/touches·兼容 6 列旧格式）；is_inflight 状态判定（已收官/已闭环 开头为 done·W681 式历史在途行 touches 空天然无害）；touches_conflict 纯函数；CLI 加 --touches（本批手工共享面清单）与 --self（本批 W 号·排除自己认领行）；在途盘点 NOTE 加交集 FAIL 拒绝并行（退出码 1）。
> - **T3 单测 10 例**：tests/unit/test_preflight_check.py 由 5 例扩至 10 例（touches 列解析/旧格式向后兼容/is_inflight 四态/touches_conflict 交集与多路径）；受控负样本实证：临时插入编号 999 的假在途批次行（touches 含 AGENTS.md）触发 FAIL rc=1·删行恢复后转绿。
> - **T4 文档面**：AGENTS §4.3 最高频铁则补 touches 条；pitfalls git/提交/并发节 7→8 条新增 touches 纪律条目（含 W738/W739 并行交错实证）；scripts/README preflight 工具表六检与参数更新；文档规范 §11.1 补 touches 说明段（修相对链接 agent→../agent 一处·lint_links 拦截）。
> - **验证（全绿）**：pytest 337 passed（332+5）；ruff scripts/ 全过；verify_delivery 全量 46 段 OK（级联前 C4-f 两项漏 add 时序 FAIL 属预期·add 后转绿）；行尾纯净（7 改动文件零混尾）；preflight 正路径 PASS 负样本 FAIL rc=1 双向实证。
> - **状态**：已落地（级联+提交后以 gh run list 为准）。
> - **文件**：scripts/preflight_check.py、tests/unit/test_preflight_check.py、docs/00-导读/W批次编号对账表.md、AGENTS.md、docs/agent/pitfalls.md、scripts/README.md、docs/00-导读/文档规范.md。
### W738（2026-10-14）：tmpe 临时文件体系批
> **来源**：用户令「请检查 D:\\xiyouji\\tmpe tmpe 文件我觉得应该和归档文件一样做一个 tmpe 临时文件体系」+ 长文方案 v1.0→v1.1 拍板（桶结构+契约+policy+盘点工具+并行锁+journal+_trash 受控可删除+工具晋升评估）。动工前并行侦察：取号 W738 无撞号·_edge_cdp_profile 无进程占用·全仓零引用。
> - **T1 契约 tmpe/README.md**：定位=工地而非第二个 archive（archive=博物馆·登记禁删可追溯；tmpe=工地·分类堆放+完工清场）——桶约定（w###/_bak/_shot/_profile/_misc/_inbox/_hold/_trash/_reports）+ 保留策略表 + 清理纪律（列清单+主人确认+回收站·禁 rm -rf·docx/pdf 个人稿件永冻）。
> - **T2 策略文件化 tmpe/policy.yml**：桶清单/TTL（_shot 30d、_misc 90d、_inbox 7d、_trash 7d）/备份代际 2/protect glob（个人稿件正则）/freeze 48h+活跃锁路径/排除项/cache_dirs（_edge_cdp_profile 可再生声明）/tool_promotion（九维评分·晋升阈值 14·观察阈值 8·禁自动晋升）；JSON 兼容语法（=YAML 子集·零硬依赖·CI 无需 pyyaml）。
> - **T3 工具 scripts/tmpe_tidy.py 重写为策略执行臂**：默认 dry-run·--apply 必须 --confirm 双闸门；--plan --json 与 --apply --from-plan 计划一致性；journal（.journal/*.jsonl 记 src/dst/sha1/mtime/rule）+ --undo 反向恢复；运行锁 .locks/tmpe_tidy.lock（stale 自动接管）+ 会话热区锁 .locks/*.json（TTL 过期忽略）；目标冲突时间戳后缀禁覆盖；同分区 os.rename、跨分区拒绝（禁 copy+delete）；优先级链 protect>active_lock>freeze>标准桶>分类规则>_inbox；--report 落 _reports/（md+json）；--tool-candidates 工具晋升评估（只读扫描+九维 18 分+候选报告·禁执行禁自动晋升）。
> - **T4 单测 19 例**：tests/unit/test_tmpe_tidy.py——用户点名 6 案例（w607_docxgen/w658_out2/a_note_bak/_c_review png/mqxs_pages/桶目录自排除）+ 优先级链 4 例 + protect 正则 glob + 过期锁忽略 + policy 加载 + 冲突后缀 + 同卷检测 + plan 过滤 + apply/undo 往返 + 运行锁占用 + 评分与只读断言；跑测中实证修复跨盘 relpath 崩溃（journal 展示健壮性）。
> - **T5 治理执行（P0 三批）**：顶层 115→40 项；95 项归桶（w### 8/_bak 5/_shot 25/_misc 56/_profile 1·零删除·journal 全程）；_edge_cdp_profile 174.6MB/113 件入 _trash（可 undo·7 天后经确认清）；dxbak 实际 2 代已达「保留最近 2 代」规则无需清；review/ 与 w736/ 并行会话冻结（48h 窗）；个人稿件 12 件永冻（docx/pdf/papercheck）。
> - **T6 git 纳入**：.gitignore 改 tmpe/ → tmpe/* + 文件级例外（!README.md !policy.yml）——体系件可复现、大文件留本地（目录级忽略后内部例外不生效的 git 规则实证）。
> - **验证（全绿）**：pytest 332 passed（313+19）；ruff scripts/ 全过；盘点复跑结构稳定（桶内实况 7 桶齐）；--tool-candidates 11 脚本全落观察档无晋升候选（评分保守符合禁自动晋升设计）；_trash 项 journal undo 可恢复。
> - **状态**：已落地（级联+提交后以 gh run list 为准）。
> - **文件**：tmpe/README.md、tmpe/policy.yml、scripts/tmpe_tidy.py、tests/unit/test_tmpe_tidy.py、.gitignore、docs/00-导读/W批次编号对账表.md、CHANGELOG.md、HANDOVER.md、AGENTS.md、STRUCTURE.md、README.md、scripts/output/file-index.md、scripts/output/_w738_spec.json、scripts/output/_cascade_files_W738.txt、CITATION.cff。

### W737（2026-10-14）：对抗性审查修复与报告归置批
> **来源**：用户令「对本项目进行最严格对抗性审查（五可标准：可量化/可验证/可执行/可追踪/符合实际情况）」+「全部开始修复·所有报告转移至 docs/11-报告复盘」。审查报告（六项发现·2 HIGH）落 docs/11-报告复盘/对抗性审查报告-2026-10-14.md；动工前 preflight 全绿（对账表 max=W736 → W737 认领）。
> - **T1 报告归置**：新建 docs/11-报告复盘/（README 索引+台账·现役 13 篇+归档 9 篇指针）——承接 10-方法论沉淀 的报告类条目 10 件、根目录项目GitHub参考调研报告、tmpe 对抗性审查报告与读者数据截图目录；10-方法论沉淀 README 重编号（方法论 20 条+魏征盘点+报告指针行）；全仓活引用同步（HANDOVER/demand 计划/product 计划/搜索页双页/README+AGENTS+STRUCTURE 目录树）；stats 新键 report_docs（methodology_docs 31→20·report_docs=14）；docs/INDEX 重建（682 篇/12 板块）。
> - **T2 演绎标注（F-3）**：100 篇逐回解读插入 310 处【文学演绎】标记（SD### 系列 159 + 深度解读区高未命中小节 151·判定=节内 ≥15 字引文未命中率 ≥50%·延伸思考问答区豁免）；3 篇外传 fiction 文档加文档级标记；文档规范新增 §4.12（演绎内容标注·标记语义·门禁豁免依据）。
> - **T3 引文门禁扩三检（F-1/F-2）**：check_citations.py 由单语法族扩为三检——① 规范引文行（原职能）；② `X道：「」` 归属对白行全书精确命中（防虚构台词冒充实录·豁免=原文全文照录区+演绎标记区）；③ 语料保真检（text-search.json vs 分回 md 逐回全等）；--self-test 扩至 9 例（含语料篡改负样本）；门禁分母收敛至入库内容（gitignore 感知·S2/S3/S4 本地工作区不再进分母）；gates.md 第 20 门禁定义同步。
> - **T4 失实引文整改（F-1）**：docs/01 全量 17 条归属对白失实逐条整改（完全虚构 3·静默删改 3·跨回误植 2·标点/截断 9）——含 023 虚构八戒台词、008 如来三藏引文删字、012 跨回误植等实证案；全部替换文本自重建语料程序化提取（逐字精确）；docs/02 两篇深化+docs/03 一篇共 3 处虚构对白同步整改；A4/A5 四文档 490 条规范引文行修复 4 条静默丢字（无名和尚×2/没钱使用/陪钱嫁汉）。
> - **T5 语料仲裁重建（F-2）**：text-search.json 与 source/原文/分回 修复前 100/100 回漂移（分回转换丢段 7 处+僻字降级 6 处+字级差异 87 处+旧 json 自身丢内容）——按「分回保内容完整+旧 json 清字基准」仲裁：恢复 7 丢段（ch3 金星招安/ch7 斩妖台/ch19/ch24/ch65/ch70/ch78）、僻字还原（狢/鯾/𤟹/斝/躘/狻/咪）、87 字级对齐、保留分回独有（ch69/99 回目联语等）；12 个分回 md 同步修正；corpus_note 记裁；终态 100/100 逐回全等。
> - **T6 CITATION 与合规（F-4/F-5）**：CITATION.cff 五计数刷新（人物 56→215/专题 78→209/文化 16→34/可视化 61→87/维度 132→133）+ preferred-citation 真 URL+双许可注；5 处涉台表述修正（台湾故宫博物院→中国台北故宫博物院等·reader 随源重建）。
> - **T7 陈旧态清理**：对账表「现势=W721」遗留块碑化（陈旧 16 号·人类陷阱）、陈旧预留 bullet 清理 10 条（W724-W733）、标题校正（W648 起回填）；AGENTS §5.1 补 make 依赖说明；AGENTS 脚注 W736 条目「五十三项」→「四十六段」措辞校正；site/index.html 字数口径 70.8→70.7 万（实测 706,586 字符·声明语料）。
> - **T8 产物重建**：reader 622 页重建（build_reader+inline_css+generate_csp 全链）+ chapter-stats.html EMBEDDED 重灌（740093→742357·双源复绿）+ 红蟒精用字修正（稀柿同→衕）+ docs/INDEX 重建。
> - **验证（全绿）**：check_citations 三检全过（423 规范引文+104 归属对白 100% 命中·语料保真 100/100·self-test 9/9）；全量门禁 46 段 OK（--scope full·C4-f 时序 FAIL 级联后消解）；CSP 零漂移（856 页/858 哈希）；chapter 双源一致；lint_links docs 0 broken；stats --check 16 键零差异；pytest 313 passed；ruff scripts/ 全过；混行尾 0。
> - **状态**：已落地（级联+提交后以 gh run list 为准）。
> - **文件**：scripts/check_citations.py、dataset/text-search.json、source/原文/分回/（12 件修正）、docs/01-全书逐回解读/（100 件：演绎标记+引文整改）、docs/02-人物深度分析/（外传 3 标记+深化 2+红蟒精）、docs/03-主题与情节专题/时间的政治学专题.md、docs/04-文化与历史背景/（版本演变+西游与民间信仰）、docs/05-诗词歌赋/原著景物诗赏析专题.md、source/引用与网络解读/学术论文索引.md、docs/11-报告复盘/（README+13 报告+读者数据截图 5 件·新建目录）、docs/10-方法论沉淀/README.md、docs/00-导读/文档规范.md、docs/00-导读/W批次编号对账表.md、docs/agent/gates.md、CITATION.cff、README.md、STRUCTURE.md、AGENTS.md、HANDOVER.md、site/index.html、site/data/search.html、site/en/search.html、site/data/chapter-stats.html、site/reader/（622 页重建）、docs/INDEX.md、scripts/output/stats.json、scripts/output/stats-changelog.json、scripts/output/stats-index.md。

### W736（2026-10-13）：发布链工具化与文档负载治理批
> **来源**：用户批准 S-31/32/33 三卡与实现形态、U-01 宿主定时巡检、文档负载治理批（file-index 289KB 超 50KB 阈值 5.8 倍）认领。动工前 preflight_check 全绿（fetch 正常·对账表 max=W735 → W736 认领·现势 bullet 交叉核验一致）。
> - **T1 S-33 前置核验器**：scripts/preflight_check.py 新建——五检（fetch/origin-main 顶部/对账表取号/工作树态/环境 py+ruff+pytest）+ fetch 故障降级 GitHub API 通道（W732 实证备路）；取号权威源=对账表表格 max+1（parse_ledger 修复双「现势」源冲突——顶部遗留块停 W721 曾致误取 bullet 残留 W697）+ 尾部 bullet 交叉核验；狗粮首跑即抓真 bug，工具价值实证。
> - **T2 S-31 发布预检器**：scripts/release_prep.py 新建——spec 三检（字段必填/分隔符黑名单/title 领衔/四件套文件行）+ 消息 W### 形态登记核验（C4 镜像·登记源=CHANGELOG 现役+两归档+对账表四件）+ 文件行 C4-f 镜像（在库/staged 且未 gitignore）+ --init 模板生成；判据精确镜像 batch_cascade.precheck。
> - **T3 单测 17 例**：tests/unit/test_release_prep.py + tests/unit/test_preflight_check.py——字段检/禁字符/领衔/W 号登记/porcelain 解析（\u0000 分隔形态）/路径 C4-f 镜像全覆盖。
> - **T4 S-32 形态拍板**：行为等价验证套件（四口径工具箱）=仓库脚本形态·随下个重构批触发（任务卡 YAGNI 约束·不预建）。
> - **T5 文档负载治理**：CHANGELOG W650-W699 段（v2.3.250-v2.3.293）迁 archive/docs/CHANGELOG-ARCHIVE.md（236KB→103KB）+ file-index W449-W699 段迁 archive/docs/file-index-ARCHIVE.md（289KB→35KB）——双文件归档边界统一 W700（check_index_health 段一一对应约束）；双文件头注/边界/「W736 一级归档」注记同步；C7 不变式 36/36 保持。
> - **T6 引用登记**：scripts/README.md 三工具登记（archive_file/preflight_check/release_prep）+ archive/README.md 台账 6 行路径前缀与滚动批次同步 + 对账表 W736 认领行；W735 复盘报告 6 件随批入库（第 38 篇 328 行 37KB + 方法论 README 索引 + STRUCTURE 实体标记 30→31 + stats 三件刷新）。
> - **验证（全绿）**：preflight 狗粮 PASS（五检+取号 W736）；release_prep spec 自检 PASS；pytest 313 passed（296+17 新例）；ruff scripts/ 全过（新测试文件含入·tests/ e2e 17 项历史存量不在本批口径）；stats --check 15 键零差异；全量门禁 53 项 OK；三登记件行尾保真（CRLF/LF 各归其位零混尾）。
> - **状态**：已落地（级联+提交后以 gh run list 为准）。
> - **文件**：scripts/preflight_check.py、scripts/release_prep.py、tests/unit/test_preflight_check.py、tests/unit/test_release_prep.py、CHANGELOG.md、archive/docs/CHANGELOG-ARCHIVE.md、archive/docs/file-index-ARCHIVE.md、scripts/output/file-index.md、docs/00-导读/W批次编号对账表.md、archive/README.md、scripts/README.md、HANDOVER.md、AGENTS.md、STRUCTURE.md、docs/10-方法论沉淀/README.md、docs/10-方法论沉淀/工作复盘与优化分析报告-2026-10-13.md、scripts/output/stats.json、scripts/output/stats-changelog.json、scripts/output/stats-index.md、scripts/output/_w736_spec.json、scripts/output/_cascade_files_W736.txt、CITATION.cff。

### W735（2026-10-13）：全仓归档大扫除批
> **来源**：用户令「按 ①→②→③ 推进（归档体系完善）」+「全项目搜索计划方案类：有哪些是已经做过了需要归档、哪些过时需要删除或再评估」。动工前 fetch 正常·对账表 W735 认领。
> - **T1 归档索引**：archive/README.md 新建——结构树（按类归置·用到才建）+ 归档台账（11 组登记·滚动/批次标注）+ 引用与检索约定（引用写新路径/检索/禁改/门禁关系）。
> - **T2 归档工具**：scripts/archive_file.py 新建——git mv 归位（类别自动判定 md/txt 入 docs、W 号自动分桶 batches/wNxx）+ 活引用扫描提示 + 台账登记；前置校验（存在/跟踪/工作树干净）+ --dry-run。
> - **T3 全仓归档迁移 728 件（3 件恢复后净 725）**：五分区——A 区 scripts/ 根下 310 件历史 spec/一次性脚本/中间产物（保留 _s4~_s7 活跃线）；B 区 scripts/_attic 32 件整迁 archive/scripts/attic/（自含 README）；C 区 scripts/output 335 件（含 83 个级联清单 W649-W727、历史 spec、review-pass3 全组 105 件、散件·保留活跃基线 34 件与 W728+ 批）；D 区 docs/superpowers 37 件已完结方案/计划/评估/设计稿（保留 9 件）；E 区 docs/_dev 10 件整迁；F 区复盘 4 件继 09-16 先例入 archive/docs/复盘报告/。
> - **保留判定四维**（防误伤·全量引用扫描驱动）：① 活跃线（_s4/_s5/_s7 前缀含 gitignore 本地件）；② 活跃基线（file-index/stats 系/各 baseline/perf-baseline/design-tokens/hreflang-pairs 等被门禁脚本读写的 34 件）；③ 被现役文档以操作指令形态引用者 18 件（白屏诊断族 8/引文工具族 2/指纹对账 1/暗色审计 1/S4 论文线 4/暗色门禁配套 1）——扫描中纠回 15 件+恢复 3 件；④ HANDOVER 待办联动 2 件（demand-side master-plan 配额继续·agents-layered BL-24 登记在册）。
> - **T4 引用同步与清理**：文档规范 1 处（设计依据→archive 路径）+ 10-方法论 README 4 条复盘链接（→archive/docs/复盘报告/）；scripts/_dayreview_shots 空目录删除；S4 论文线三脚本按「活跃工作文档引用」判据从归档恢复；归档连锁修复=stats.py --w W735 刷新技术键 methodology_docs 34→30（复盘 4 件迁出）+ STRUCTURE.md 实体标记同步。
> - **验证（全绿）**：728 件 git mv 成功率 100%（0 失败）；行尾纯净检查全量（唯一混尾=对账表插入行·已修纯 CRLF）；lint_links docs 全量 5181 链接 0 broken；归档后残留引用精确扫描 50 处逐条判定（历史叙述/代码注释/已同步链接·全部可接受）；pytest 296 passed；ruff scripts/ 全过；全量门禁 53 项 OK。
> - **状态**：已落地（级联+提交后以 gh run list 为准）。
> - **文件**：archive/README.md、scripts/archive_file.py、docs/00-导读/文档规范.md、docs/10-方法论沉淀/README.md、docs/00-导读/W批次编号对账表.md、CHANGELOG.md、HANDOVER.md、README.md、STRUCTURE.md、AGENTS.md、CITATION.cff、docs/00-导读/项目说明.md、.github/workflows/README.md、scripts/output/_w735_spec.json、scripts/output/_cascade_files_W735.txt、scripts/output/file-index.md（另 725 件归档迁移至 archive/docs/plans 等七组目录·逐项见 file-index W735 段）。

### W734（2026-10-13）：归档体系统一与交接文档更名批

> **来源**：用户令「同步（归档引用链）」+「把 交接文档.md 全部改换为 HANDOVER.md」，并确立归档新规：「以后超过文档内容大小的文件都要归档，全部归档到 D://xiyouji//archive，按照 docs 归档文档类内容、脚本类归档脚本内容等等以此类推按照文件格式统一储存」。动工前 fetch 正常·origin/main 无新批次·W734 认领。
> - **T1 归档体系统一**：docs/ARCHIVE→archive/docs（8 项：6 归档件 + w550-shot-review/ 11 件 + 复盘报告/ 5 件）；scripts/archive→archive/scripts（45 件）；scripts/audit/archive→archive/scripts/audit（10 件）；旧目录删除；用户先行更名的 HANDOVER-ARCHIVE.md / file-index-ARCHIVE.md 一并归位（git 改名识别·LF 归一后与 HEAD blob 全等核验·纯改名零内容改动）。
> - **T2 交接文档更名**：交接文档.md→HANDOVER.md（git mv·内容与行尾零改动）；全部 live 引用同步——工具链 15 文件（batch_cascade/verify_delivery/sync_docs/check_doc_sync/check_governance_docs/agent_start/check_w_range_literal/pre-commit-validate/release/review_sweep/safe_commit/bump_version/drl_contracts/Makefile/pyproject）+ 六文档与旁文档（README/STRUCTURE/AGENTS/项目说明/workflows README/CHANGELOG 顶注）+ agent 文档（gates/pitfalls）+ 根文档（CLAUDE/新Agent启动Prompt/LICENSE-CONTENT/PULL_REQUEST_TEMPLATE）；悬空链接清零（HANDOVER.md 内部归档链接 5 处 + file-index 顶部指针 + AGENTS 脚注归档指针 + S3 分享页 README（本地产物·gitignore））。
> - **T3 工具链路径同步**：batch_cascade handover 面路径与 _arc（AGENTS-ARCHIVE 滚动目标）；verify_delivery CORE_DOCS/A4_DOCS/ARCHIVE_DOCS/_DOC_FILES_RE 四组；lint_links 冻结档排除 docs/archive/→archive/；check_doc_sync ARCHIVE_CHANGELOGS（C4 登记集合）与交接读取；pyproject ruff 排除入 archive/。
> - **T4 文档规范重构**：§4.4 命名与归档条、§5 二级归档条、§8 健康指标、§11 管控表全量更新；新增「归档根与分类（W734 统一）」规则——archive/ 根·按类归置（文档类 archive/docs/、脚本类 archive/scripts/、其余以此类推）·触发=退役替换或体积超限（沿用 50KB/500 行与 1MB 分层阈值）。
> - **验证（全绿）**：全仓残留扫描（live 面旧名/旧路径清零·历史件与迁移说明按规保留）；lint_links docs 全量 0 broken；check_governance_docs 7 项全过；check_doc_sync self-test 18/18 + 直跑；check_agents_layers self-test 5/5；check_w_range_literal 0 漂移；ruff scripts/ 全过；pytest 296 passed；全量门禁 53 项 OK。
> - **状态**：已落地（级联+提交后以 gh run list 为准）。
> - **文件**：HANDOVER.md、CHANGELOG.md、README.md、STRUCTURE.md、AGENTS.md、CITATION.cff、CLAUDE.md、LICENSE-CONTENT.md、新Agent启动Prompt.md、pyproject.toml、Makefile、.github/PULL_REQUEST_TEMPLATE.md、.github/workflows/README.md、docs/00-导读/项目说明.md、docs/00-导读/文档规范.md、docs/00-导读/W批次编号对账表.md、docs/00-导读/V2可视化维度方案.md、docs/agent/gates.md、docs/agent/pitfalls.md、docs/10-方法论沉淀/README.md、docs/10-方法论沉淀/双索引可追溯改造.md、docs/_templates/validation-checklist.md、scripts/batch_cascade.py、scripts/verify_delivery.py、scripts/lint_links.py、scripts/check_doc_sync.py、scripts/check_governance_docs.py、scripts/agent_start.py、scripts/check_w_range_literal.py、scripts/pre-commit-validate.py、scripts/release.py、scripts/review_sweep.py、scripts/safe_commit.py、scripts/bump_version.py、scripts/sync_docs.py、scripts/drl_contracts.yaml、scripts/output/file-index.md、archive/docs/CHANGELOG-ARCHIVE.md、archive/docs/CHANGELOG-ARCHIVE-tier2.md、archive/docs/HANDOVER-ARCHIVE.md、archive/docs/file-index-ARCHIVE.md、archive/docs/AGENTS-ARCHIVE.md、archive/docs/STRUCTURE-ARCHIVE.md、archive/scripts/audit/README.md、site/index.html、site/data/cross-time-danmaku.html、site/data/tag-cloud.html、site/dukou-engine.html（另 archive/docs/w550-shot-review/、archive/docs/复盘报告/、archive/scripts/ 45 件、archive/scripts/audit/ 10 件目录级迁入·逐项见 file-index）。

### W733（2026-10-13）：达标收尾批

> **来源**：用户 quote「剩余 60-90 行函数可选做达标收尾批」——将 ≥80 行区间清零（除审计判定项）。动工前 fetch 正常·origin/main 无新批次·W733 认领。
> - **范围裁决（证据版·审计后）**：入选六目标——check_seo_head main 95（挂载门禁）+spot_check_nlp main 93+check_design_doc_drift main 89（StrictGate）+embed_json main 106+build_reader main 101+perf_monitor compare_trend 88；**审计判定不动**：bump_version main 82——W714 方案 D 停用守卫为死工具（任何调用检测到「当前批次」新形态即 STOP 退出），重构零收益；run_self_test 146 已判定。
> - **T1 check_seo_head.py（154→186 行·main 95→20）**：五 R 检查提取（_check_og_cover/_check_head/_load_pairs+_check_hreflang/_check_sitemap/_check_json_ld）。
> - **T2 spot_check_nlp.py（118→135 行·main 93→20）**：三数据段提取（_report_characters/_report_dialogues/_report_cooccurrence·返回码编排）。
> - **T3 check_design_doc_drift.py（141→177 行·main 89→30）**：六函数（_collect_token_facts/_collect_page_local/_check_doc_regeneration/_check_md_coverage_and_fabrication/_check_design_md_section/_check_dark_count·StrictGate marker 汇总行保留）。
> - **T4 embed_json.py（257→276 行·main 106→15）**：四函数（_parse_args/_load_inputs/_embed_key/_write_with_backup·全错误路径退出码保留）。
> - **T5 perf_monitor compare_trend（88→28）**：三段提取（_empty_trend_result/_diff_metric/_diff_all_pages）。
> - **T6 build_reader.py（326→350 行·main 101→40）**：五函数（_collect_section_files/_render_one_page/_render_section_index/_render_root_index/_prev_next_html 提级）。
> - **验证（全绿）**：三门禁输出逐字节 IDENTICAL（seo 855 页+spot 92 行+drift 汇总）+**drift 篡改负样本对拍**（旧版临时放回 scripts 跑·FAIL 行+exit=1 逐字节一致）；embed_json **12 场景 CLI 快照**（成功/错误/备份/ensure·含裸键 exit 4 路径）+compare_trend **9 场景快照**（含 ms 单位换算/坏 JSON/零值除零）全字段逐字节；build_reader **622 文件产物 sha 全等**（对拍后 checkout 恢复）；pytest 296+ruff 0+门禁 53 项 OK。
> - **踩坑记录（经验沉淀）**：① 负样本对拍需「旧版可执行」——备份文件在 tmpe 下 ROOT 推导错位，须临时复制回 scripts/ 跑完即删；② build_reader 直出为「未后处理版」（CSP/内联 CSS 由后续工具补）——提交版 reader ≠ 直出，对拍口径以直出为双方基准并跑后 checkout 恢复；③ 采集脚本标签不一致（「seo exit=」vs「exit=」）会造出假 diff——对比脚本须统一 echo 形态；④ 误操作 `echo >> 不存在路径` 会创建垃圾文件——发现即清理并 gito status 核验。
> - **状态**：已落地（级联+提交后以 gh run list 为准）。
> - **文件**：scripts/check_seo_head.py、scripts/spot_check_nlp.py、scripts/check_design_doc_drift.py、scripts/embed_json.py、scripts/perf_monitor.py、scripts/build_reader.py、CHANGELOG.md、docs/00-导读/W批次编号对账表.md、README.md、STRUCTURE.md、docs/00-导读/项目说明.md、交接文档.md、.github/workflows/README.md、site/index.html、site/data/cross-time-danmaku.html、site/data/tag-cloud.html、site/dukou-engine.html、AGENTS.md、CITATION.cff、scripts/output/file-index.md。

### W732（2026-10-13）：性能与文档工具链重构批

> **来源**：用户令「继续第五批」（承接 W728-W731 四批重构方法论固化）。动工前 fetch 失败（502 代理层故障）——改用 GitHub API 独立通道核验远端状态：origin/main 顶部仍 W727 无新批次·无撞号·W732 认领。
> - **范围裁决（证据版·W731 后 AST 重度量 TOP22）**：本批后全仓 ≥100 行函数清零（除已判定不动的 run_self_test 146）。三目标：perf_optimize.py（四函数 80/72/69/74·14 单测抓手）+ optimize-html-size.py（render_report 126·扫描器输出抓手）+ sync_docs.py（main 111·七规则输出抓手）。
> - **T1 perf_optimize.py（720→758 行·≥80 行函数 4→0）**：optimize_lcp 80→58（拆 _apply_lazy_pass 闭包工厂规避 B023+_collect_preload_lines）+ convert_svg_to_canvas 72→42（_build_canvas_bridge 桥接脚本模板提取）+ inline_critical_css 69→52（_resolve_critical_css 来源判定）+ generate_report 74→31（五模块段表驱动 _render_module_section+_fmt_stats 提级+头尾段）。
> - **T2 optimize-html-size.py（405→438 行·≥80 行函数 1→0）**：render_report 126→六段渲染（_render_summary_header/_render_top10_table/_render_full_table/_render_large_suggestions/_render_strategy_guide/_render_usage_section·固定文本段全保留）。
> - **T3 sync_docs.py（633→602 行·≥80 行函数 1→0）**：main 111→39 拆 _run_checks 七规则表驱动（横幅/OK 消息/检查函数/前置输出全参数化）；**横幅历史形态逐字节保留**——规则 1/3/4「标题 ===」含空格、规则 2/5/6/7「）===」无空格（表驱动统一格式会引入 diff·逐字节对比当场抓住·原样入表）。
> - **验证（全绿）**：perf fixture 快照全字段逐字节 IDENTICAL（返回 dict+文件 sha·含错误路径）+单测 14 passed；OHS stdout/报告双 IDENTICAL（46 大文件报告逐字节）；sync_docs 七规则输出逐字节 IDENTICAL（exit 码一致）；pytest 296 + ruff 0 + 全量门禁 53 项 OK。
> - **踩坑记录（经验沉淀）**：① 表驱动化前的「输出形态普查」——sync_docs 七条横幅存在历史不一致形态（4 条无空格 vs 3 条有空格），凭印象统一格式会引入 diff；逐字节对比当场抓住并原样入表——**格式统一是诱惑，逐字节保真是铁律**；② perf harness 需过滤 timestamp 行且归一化 report sha（含时间戳的产物 sha 每轮必变）；③ sync_docs 为 CRLF 工作树——LF 归一处理·写回恢复 CRLF（与 batch_cascade 同款，工具化后复用）。
> - **状态**：已落地（级联+提交后以 gh run list 为准）。
> - **文件**：scripts/perf_optimize.py、scripts/optimize-html-size.py、scripts/sync_docs.py、CHANGELOG.md、docs/00-导读/W批次编号对账表.md、README.md、STRUCTURE.md、docs/00-导读/项目说明.md、交接文档.md、.github/workflows/README.md、site/index.html、site/data/cross-time-danmaku.html、site/data/tag-cloud.html、site/dukou-engine.html、AGENTS.md、CITATION.cff、scripts/output/file-index.md。

### W731（2026-10-13）：发布工具链与安全扫描重构批

> **来源**：用户令「继续第四批」（承接 W728-W730 三批重构方法论固化）。动工前 fetch origin 确认无撞号（origin/main 仍 W727·W731 认领）。
> - **范围裁决（证据版·AST 度量 TOP25）**：全仓最长函数 `batch_cascade.py main` 347 行入选（发布流程核心工具·十面级联断言与改写全在单函数内）；`security_scan.py run` 91 行+`build_report` 81 行入选（有单测 12 例+报告对比抓手成熟）。排除：`check_doc_sync run_self_test` 146 行（W730 已审计判定表驱动形态不动）、`perf compare_trend` 88 行（留第五批与 perf 收尾合并）。
> - **T1 batch_cascade.py（429→492 行·main 347→33 行·≥80 行函数 1→0）**：十个面各提取一函数（_face_changelog 31/_face_three_docs 26/_handover_rotate_oldest 37/_face_handover 60/_face_workflows 17/_face_footers 9/_face_agents 41/_face_citation 9/_face_file_index 10）+ 页脚 _foot_insert 提模块级+_agents_entry_wn 提模块级 + 落盘 _apply_pend + 写后自检 _post_check + _Ctx 上下文承载跨面共享量；全部历史注释（53 条行首注释无损自检）与断言消息逐字节保留（W534→W727 教训链是文件核心资产）。
> - **T2 security_scan.py run 91→42**：拆 _prepare_scan_targets（--target/--all 文件集解析）/三阶段检查（_run_headers_check/_run_sri_check/_run_pip_audit_check）/落盘 _write_report_files/退出码 _exit_code。
> - **T3 security_scan.py build_report 81→编排体**：拆 _summarize_findings（统计+排序）+ 六段渲染（_render_md_header/rule_stats/details/rule_list/深化/fixes·md 行序列零改）+ 组装体。（文件 797→870 行·≥80 行函数 2→0）
> - **验证（对拍级·本批新增受控 apply 对拍手法）**：batch_cascade 以「19 个历史 spec + W731 草稿」全量 dry-run 输出对比（归一化 traceback 行号/函数名——重构的结构性变化·exit 码+stdout+错误消息逐字节一致）+ **受控 apply 对拍**（旧版落盘快照→git checkout 撤销→新版落盘→diff）——14 文件级联落盘 diff 265 行逐字节全等 + manifest 一致 + 写后自检全过；security_scan 单测 12 passed + --all 报告 JSON/MD 双 IDENTICAL（除 timestamp/耗时）+ CLI 三分支对拍（target 正常/不存在/无参数）一致；pytest 296 + ruff 0 + 全量门禁 53 项 OK。
> - **踩坑记录（经验沉淀）**：① _handover_rotate_oldest 提取时遗漏 return s（原就地修改→函数化须回传）——草稿 spec dry-run 立即 TypeError 抓住；19 个历史 spec 全部在早期断言失败（现役段号不匹配）覆盖不到 handover 面——**草稿 spec 走通全 10 面的必要性实证**；② dry-run 对比口径归一化：traceback 含行号/函数名/源码行（重构结构性变化不可比较），口径=exit 码+stdout+错误消息行；③ apply 对拍须排除重构文件自身 diff（basline 采于旧版时该文件=HEAD 无改动态）；④ batch_cascade 为 CRLF 工作树（autocrlf=true 检出）——切片重组脚本 LF 归一处理、写回恢复 CRLF、替换表逐行化+行首注释无损自检（53 条）防注释丢失；⑤ 消息文本的渲染段函数名缩写（w 加三位数字形态）被 C4 提交对账提取为未登记批次号 FAIL——reset --soft 重提交并改写为『深化』（amend 死锁：旧提交在 log -15 自查窗口内），消息与文档中函数名类引用此后须避开 W 加三位数字形态。
> - **状态**：已落地（级联+提交后以 gh run list 为准）。
> - **文件**：scripts/batch_cascade.py、scripts/security_scan.py、CHANGELOG.md、docs/00-导读/W批次编号对账表.md、README.md、STRUCTURE.md、docs/00-导读/项目说明.md、交接文档.md、.github/workflows/README.md、site/index.html、site/data/cross-time-danmaku.html、site/data/tag-cloud.html、site/dukou-engine.html、AGENTS.md、CITATION.cff、scripts/output/file-index.md。

### W730（2026-10-13）：门禁脚本长函数收尾重构批

> **来源**：用户令「第三批候选按同一方法论推进」（承接 W728 方案档 §七 / W729 报告末条）。动工前 fetch origin 确认无撞号（origin/main 仍 W727·W730 认领）。
> - **范围裁决（证据版·AST 度量）**：候选池三向比较——a11y 剩余最长仅 74 行（check_parsing·扫描器固有形态）排除；JS 侧最大非一次性文件仅 531 行且验证需 Playwright 重环境（抖动口径）排除；选定「两挂载门禁 + 一名命名候选」：check_doc_sync.py（evaluate 177 行·第 31 门禁·自带 self-test 18 例）+ lint_links.py（main 125 行·docs 链接门禁）+ perf_monitor.collect_rum_metrics（98 行·W729 遗留命名候选）。
> - **T1 check_doc_sync.py（592→618 行）**：evaluate 177→20 行编排体（拆 _check_c1_readme_head/_check_c2_jiaojie_head/_check_c3_agents_slots/_check_c4_commit_ledger/_check_c5_aggregate_stats/_check_c5d_stats_recheck 六个检查函数——每条检查消息逐字节保留·fail-closed 早退语义等价）；gather 82→65（提取 _git_output_lines 合并 staged/head_tree/status 三处同构 git subprocess 块·git log 块因错误捕获语义独特保留原样）；**run_self_test 146 行经审计判定已表驱动（逻辑约 30 行·116 行为测试数据表）不动——防过度重构**。
> - **T2 lint_links.py（442→473 行）**：main 125→33 行编排体（拆 _parse_args 参数构建/_resolve_scan_dir 目录解析与退出/_collect_scan_files 收集过滤/_process_file 单文件处理返回三计数——逐行打印序逐字节保留·args.fix→do_fix 参数化）。
> - **T3 perf_monitor.py（1085→1085 行·净零）**：collect_rum_metrics 98→约 40 行编排体（拆 _try_read_rum 读取早退/_normalize_rum_events 形态归一/_bucket_rum_events 按页归集/_summarize_rum_p75 双 P75 汇总）；文件最长函数降至 88 行（compare_trend）。
> - **验证（全绿）**：check_doc_sync 直跑输出 + --self-test 18/18 输出**双逐字节一致**；lint_links --dir docs 全量输出逐字节一致（5190 链接·0 broken）；collect_rum_metrics 11 形态合成 fixture 快照逐字节一致（正常/events 数组/裸数组/坏 JSON/缺失文件/内联 dict/内联 list/空 list/空 dict/非 dict 类型/不存在路径）+集成路径实测（--rum 数据流：events=5·2 页·alerts=2·aggregate 五键齐）；pytest 296 passed；ruff scripts/ 全量 0。
> - **方法论沉淀（本批新增）**：「拆分前先审计是否已达标」——run_self_test 146 行体量看着大、实为既有表驱动（数据表≠逻辑），判定不动；同构块合并须逐块核对错误语义（git log 块 error 捕获与其余三块不同→不强行统一）。
> - **状态**：已落地（级联+提交后以 gh run list 为准）。
> - **文件**：scripts/check_doc_sync.py、scripts/lint_links.py、scripts/perf_monitor.py、CHANGELOG.md、docs/00-导读/W批次编号对账表.md、README.md、STRUCTURE.md、docs/00-导读/项目说明.md、交接文档.md、.github/workflows/README.md、site/index.html、site/data/cross-time-danmaku.html、site/data/tag-cloud.html、site/dukou-engine.html、AGENTS.md、CITATION.cff、scripts/output/file-index.md。

### W729（2026-10-13）：性能与可访问性工具链重构批

> **来源**：用户令「重构第二批（a11y_audit/perf_monitor）按同一方法论推进」（承接 W728 方案档 §七扩展面·同流程=AST 度量选题→采行为基线→重构→对比验证→批次级联）。动工前 fetch origin 确认无撞号（origin/main 仍 W727·对账表 max=W728·W729 认领）。
> - **T1 perf_monitor.py（998→1056 行·净 +58 行换 9 个可测函数）**：build_report 189→67 行（提取 _summarize_results 统计/_render_vitals_table 逐页表/_render_optional_sections 四段可选子报告/_render_trend_details/_render_budget_details）；compare_trend 108→88（提取 _load_baseline——文件读取+pages/unit 提取+单位转换+错误早退）；check_budget 102→约 40（提取 _scan_resource_sizes 目录归集/_evaluate_budget 违规定级）；run 103→78（提取 _collect_vitals 采集降级 TBT 合并/_build_alerts_input 警报输入）。≥80 行函数 5→2（余 collect_rum_metrics 98 行=RUM 解析固有流程·下批候选）。
> - **T2 a11y_audit.py（2513→2561 行·净 +48 行）**：audit_directory 84→约 30（提取 _scan_html_files 发现+扫描/_count_by_rule 计数表/_emit_json/_emit_md 输出分流）；_render_md 82→约 45（提取 _top_files_by_findings Top5 统计/_render_top_findings Top10 详情/_render_priority_guide 优先级段）。≥80 行函数 2→0（余 check_parsing 74 行=WCAG 4.1.1 解析检查固有形态·rule_* 系列不动）。
> - **验证（全绿）**：a11y_audit --format json --quiet 全量输出与基线**逐字节一致**（仅 generated_at 时间戳·10228 条 findings/E2-2 P0/P1=0）+ MD 渲染对比一致（除生成时间戳）；perf_monitor --all 结构对比 10/10 全过——页集合 90/逐页字段集合/summary.total+errors/good+needs 总量 360/poor=0/报告顶层键/MD 八章序列/头部行/stdout 汇总量级全一致；pytest 296 passed；ruff scripts/ 全量 0。
> - **方法论修正（重要·沉淀）**：perf 实测数值**不允许逐字节对比**——Playwright 路径的 LCP/CLS 为真实浏览器度量，同一文件两轮固有抖动（timeline.html CLS 0→0.1236 即抖动越过警报阈值 0.1·alerts 6→7 条）。原「确定性假设」只对启发式降级路径成立。行为对比口径按采集路径分流：确定性扫描（a11y 全静态/启发式）走逐字节，真实度量（Playwright）走结构对比（集合/骨架/量级）。此前 W728 的 scan 报告对比同属静态路径故可逐字节。
> - **状态**：已落地（级联+提交后以 gh run list 为准）。
> - **文件**：scripts/perf_monitor.py、scripts/a11y_audit.py、CHANGELOG.md、docs/00-导读/W批次编号对账表.md、README.md、STRUCTURE.md、docs/00-导读/项目说明.md、交接文档.md、.github/workflows/README.md、site/index.html、site/data/cross-time-danmaku.html、site/data/tag-cloud.html、site/dukou-engine.html、AGENTS.md、CITATION.cff、scripts/output/file-index.md。

### W728（2026-10-13）：门禁与工具链代码重构批

> **来源**：用户令「重构所的代码，保持原有功能、输入输出及外部接口完全不变，提升可读性和可维护性」，并追加「开始之前必须写一个详细的计划方案，详细具体一点，不要笼统」+「所有内容必须可量化、可验证、可执行、可追踪、符合实际情况」。方案档先行入库（docs/superpowers/plans/2026-10-13-code-refactor-w728.md·八节含度量基线/符号级设计/风险表/验证协议/经验沉淀点）。
> - **撞号改号事件（过程记录·W659/W660 险情实证复发）**：本批原编号 W726，动工前未 fetch origin——并行 Agent 会话已于同日 03:18 向 main 推送其 W726（本地工具链修复）+W727（SVG 保护补打），与本批同号。按对账表「争议以 git 历史为唯一事实源判定+下一自由号=max+1」规则，本批改号 W728 并以 origin/main 为基重建（dev 旧两提交 1b12c2c5/1dacd962 入 reflog 可溯·force-with-lease 经用户确认后推送）。代码面双方零重叠（对方动 batch_cascade.py/SVG 修复脚本；本批动 verify_delivery/sync_docs/security_scan/doc_areas）。
> - **范围裁决（可量化）**：全仓 555 py + 787 js 单轮无法完成输出逐字节对比级验证（违反用户自设「可验证」硬约束）——改「先打样后推广」：按 AST 度量选三目标（复杂度痛点 × 有测试/行为基线），同方法论固化供后续批复用。显式排除 site/data 87 可视化页内联 JS、xiyouji-agent-web、a11y_audit.py（rule_* 30-60 行为规则扫描器固有形态·重复度低）。
> - **T1 verify_delivery.py（1173→1037 行·main() 905 行→约 55 行）**：46 段中 35 个 subprocess 委托段（608 行同构样板·占 main 67%）收敛为 2 个通用 runner + 2 张 NamedTuple 参数表（_SimpleGate×18/_StrictGate×15·差异全参数化：消息模板/超时/尾行切片/严重级/marker/ok_line）；11 个内联逻辑段 + 2 个 bespoke 段（docs链接/a11y）各提取为 _gate_* 函数；闭包上报器提取为 _Reporter 类；scope 态+补丁时序+跨段共享量收敛为 _GateContext。新增第 42 门禁从「抄 15 行」变「加 1 行表项」。
> - **T2 共享模块 doc_areas.py（新·42 行）**：verify_delivery 与 sync_docs 双份手工维护的 A_AREAS 六板块目录表 + _count_content_md 计数函数（sync_docs 注释自证同口径·任一侧改目录另一侧静默失配）收敛为单一事实源 AREA_DIRS + count_content_md；展示标签留消费方（verify 用长名/sync 用短键·呈现层不入模块）。
> - **T3 security_scan.py（809→797 行）**：scan_sri 内 script/link 两个约 30 行同构块（SRI-001/002 判定+findings 构造）提取 _check_resource_attrs(text, pattern, kind_label, rel) 通用体，主体 91 行→约 40 行。
> - **顺带修一处死代码**：原 L744-746 治理契约 except 块内遗留 Skills 索引一致性门禁（W498 已删除）的孤儿双 WARN 行——仅 check_governance_docs.py 崩溃时触发，删除。
> - **验证（全绿·改号后在 origin/main 新基线上重采基线复跑）**：verify_delivery 四模式（full/docs/site/auto）输出与同树态基线（stash 法）**逐字节 diff 全等**+exit 码一致；pytest 296 passed；ruff scripts/ 全量 0；security_scan --all 报告与基线仅差路径/时间戳/耗时元数据（findings high=0 medium=266 low=0 逐字节一致）；sync_docs 输出 stash 对比一致（存量 MISMATCH 非本次引入）；check_agents_layers self-test 5/5（第 41 门禁 C2 槽位对账不受影响）。
> - **踩坑记录（经验沉淀）**：① ruff B905 拦 zip() 缺 strict=（已补·顺带成长度断言）；② check_index_health 以正则扫 verify_delivery.py 源码计「挂载 check_* 33 个」——重构丢图表自洽段注释里的 check_screenshot_gates.js 引用致计数 33→32（已恢复注释·输出归位）——门禁脚本的注释文本也是被对账面；③ 方案档入库使引文扫描 +1 文件——行为基线必须同树态采（stash 法·跨树态对比必出假 diff）；④ 级联 apply 在 CRLF 工作树（autocrlf=true checkout）下曾致交接文档混行尾（原 W726 时点手工归一修复）——**该根因已由对方 W727 从工具层根修**（batch_cascade L176 rfind(nl)+1→+len(nl·CRLF 双字符 nl off-by-one），本批重级联不再复现；⑤ 撞号本身即最大踩坑——动工前必须 fetch origin 并以对账表 max 认领（本地台账滞后于远端认领·W659/W660 同型）。
> - **状态**：已落地（级联+提交后以 gh run list 为准）。
> - **文件**：scripts/verify_delivery.py、scripts/doc_areas.py、scripts/sync_docs.py、scripts/security_scan.py、docs/superpowers/plans/2026-10-13-code-refactor-w728.md、CHANGELOG.md、docs/00-导读/W批次编号对账表.md、README.md、STRUCTURE.md、docs/00-导读/项目说明.md、交接文档.md、.github/workflows/README.md、site/index.html、site/data/cross-time-danmaku.html、site/data/tag-cloud.html、site/dukou-engine.html、AGENTS.md、CITATION.cff、scripts/output/file-index.md。

### W727（2026-10-13）：SVG 保护补打与级联 CRLF 根修批

> **来源**：用户 quote 拍板批次 B（W726 缺陷 1 移交项·选项 1 直接打掉）——W726 修复 fix_svg 后首跑，对 35 个可视化页补打 clientWidth 最小宽度保护，make audit 的 SVG 检查自 W447 起死盲区至此复绿；顺带根修 W726 级联 apply 暴露的 batch_cascade CRLF off-by-one（本 worktree autocrlf=true 特有触发条件）。
> - **35 页保护补打（主任务）**：fix_svg 非 dry-run 实跑（35 页·clientWidth 类·radius 与 attr 宽度类存量已保护 0 命中）+ generate_csp.py 重注入（35 页 CSP·全站 856 页 858 哈希零漂移）+ audit dry-run 复跑 0 待改。根因回顾：W400 后新增页从未打上 const W = X.clientWidth || N 的 200px 下限保护（移动视口 clientWidth 为 0 时直接回落 960）。
> - **级联 CRLF off-by-one 根修（W726 提交内损坏·本批发现并修复）**：W726 级联 apply 在 CRLF 工作树触发 batch_cascade L176 rfind(nl)+1 双字符 nl 少进 1 字节——里程碑块插入把标题行尾 \r\n 撕成裸 \r（块插到 \r 与 \n 之间）+ 块尾多裸 \n，交接文档混行尾；W706 混行尾防线在 W727 dry-run 正确拦截（fail-closed 实证）。根修 +1→+len(nl)（LF 工作树 nl 单字符故旧写法恒正确·此前批次均运行于 LF 工作树所以未暴露）；受损交接文档两处字节级修复（裸 CR 补 LF 复标题换行·块尾 \r\n\n 归规范块间距 \r\n\r\n）·修复后 739 CRLF 纯净。
> - **验证**：fix_svg --dry-run 0 files rc=0 + generate_csp --check 856 页 0 漂移 + 交接文档 739 行 CRLF 纯净（混行尾 0）+ verify full 46 段 0 FAIL + pytest 296 passed + check_js_syntax 855 文件 0 违例 + lint_links（--dir docs）0 broken。
> - **状态**：已落地（CI 工作流以推送后 gh run list 为准）。
> - **文件**：scripts/archive/fix_svg_negative_widths.py、scripts/batch_cascade.py、交接文档.md、site/data 下 35 个可视化页（逐页列名见 file-index）、CHANGELOG.md、docs/00-导读/W批次编号对账表.md。

### W726（2026-10-13）：本地工具链修复批

> **来源**：用户令「排查代码中的报错」（无具体报错→主动全量扫描：verify full 41 门禁/pytest 296/ruff/check_js_syntax 855 文件/a11y/security/lint_links 逐项复跑）——CI 实跑范围全绿，本地工具链（make 目标）三项真实缺陷。
> - **缺陷 1（代码 bug·唯一必崩）**：scripts/archive/fix_svg_negative_widths.py L22 ROOT 少一级——W447（dff17dc5「45 个一次性脚本归档」）把脚本从 scripts/ 搬进 scripts/archive/ 未同步路径，parent.parent 指向 scripts/ 而非仓库根，致 site/data glob 静默空扫+dashboard.html read_text 崩（FileNotFoundError·make audit 每跑必挂）。沙盒同构验证：修复后 dry-run 实扫 87 页、报 35 页待打 clientWidth 保护（W400 后新增页从未打上·审计死盲区实况·移交 W727 处置）。
> - **缺陷 2（工作流断链）**：make data-validate 空目录 rc=1「未找到任何 .json 文件」——output/data/*.json 系 .gitignore 可重建产物，fresh clone 未跑 make analyze 即空目录，make ci 第 5 步必挂（CI 不跑此项·仅本地目标）。Makefile 加空目录跳过保护（提示先行 analyze·rc=0·不弱化校验语义）。
> - **缺陷 3（文档腐烂）**：lint_links 全仓 12 broken rc=1——README.md:169→drl-screenshot-review.md（gitignore 本地件）、学术论文索引.md 7×v08-embedded-data.js（构建产物）、4×心学方向-投稿版.md（W620 裁决出库件·本地留存）；门禁全绿原因=第 6 门禁只扫 docs/（lint_links --dir docs）。修法=清 tracked 文件死链（README 改指 CHANGELOG·v08 剥链保文·S4 改本地存档注记·不扩豁免——豁免机制只滤被扫文件不滤链接目标）。
> - **验证**：fix_svg 修复版 dry-run 实跑（87 页扫描·35 页待改·diff 合理）+ Makefile 守卫生效（空目录 rc=0+skip 提示）+ lint_links 全仓 19557 链接 0 broken + verify full 41 门禁 0 FAIL + pytest 296 passed + ruff（scripts/ CI 口径）All checks passed。
> - **状态**：已落地（CI 工作流以推送后 gh run list 为准）。
> - **文件**：scripts/archive/fix_svg_negative_widths.py、Makefile、README.md、source/引用与网络解读/学术论文索引.md、docs/00-导读/W批次编号对账表.md、CHANGELOG.md。

### W725（2026-10-12）：review 收官 mini 批

> **来源**：用户令「review 一遍这几次的改动」（W719 先例第九次·范围=W720-W724 十一提交）——机械扫+疑点深查+门禁复跑，发现三项轻度问题 mini 修。
> - **机械扫**：混行尾 17 文件 0 / 段标题双写（CHANGELOG+file-index）0 / 对账表豁免链 W725 连续 / 垃圾件 2 清除（PIPE 调试残留+废弃 chore msg·未跟踪无痕）。
> - **S-29 指针滚动注累积（发现→本批修）**：四段滚动注逐批累积（每段约 20 字符·批数线性膨胀）——batch_cascade 改单段化（插新注前 re.sub 剥全部旧「WNNN-WNNN 级联自动滚动·」·只留单段最新区间）；本批级联即自动收敛现指针（四段→单段 W720-W720）。
> - **文件行覆盖度对账（C4-f 反向抽查·本批新方法）**：W720-W722 缺「文件」行系 precheck 强制（W723）之前的历史形态·不再补（历史段禁改）；W723 全覆盖（19 token）；**W724 漏列 2 件**（AGENTS-ARCHIVE 迁入件+foot_rebuild 一次性脚本——均已在库无漏 add·纯列名不全）——现役段补列（本批 Edit）。
> - **验证**：verify full + pytest 296 + self-test（doc-sync 18/18·agents 5/5）+ stats --check 15 键零差异 + ruff 0（级联后复跑）。
> - **状态**：已落地（CI 工作流以推送后 gh run list 为准）。
> - **文件**：scripts/batch_cascade.py、CHANGELOG.md、docs/00-导读/W批次编号对账表.md、README.md、STRUCTURE.md、docs/00-导读/项目说明.md、交接文档.md、.github/workflows/README.md、site/index.html、site/data/cross-time-danmaku.html、site/data/tag-cloud.html、site/dukou-engine.html、AGENTS.md、CITATION.cff、scripts/output/file-index.md、docs/archive/AGENTS-ARCHIVE.md。

### W724（2026-10-12）：页脚链损坏修复与链长治理批

> **来源**：用户浏览器实见 site/index.html footer-meta 内容异常提问「为什么这个内容这么多」——取证定谳为重复损坏（非设计）。
> - **根因（W717 页脚锚定根修埋雷·六批自强化）**：缺陷一=插入代码回写 mm.group(0) 而 s[at:] 本身已含该段 → 每批把整条链复制一遍（W705「错位块链自强化」的页脚版）；缺陷二=800 字符搜索窗口截断 mm 致插入点落 token 中间（「v2.3.28W722」粘连实证）。六批累计：index footer-meta 9198 字符/329 token/重复 182、danmaku/tag-cloud 各 2700/135/127、dukou 14883/406/216；W718-W723 六批验证只 grep 链头未查重复=验收盲区。
> - **根修（batch_cascade 四页脚段重写）**：完整 footer 节点内定位首 token·纯前插**不回写** mm.group(0)·插入后批次段裁剪至 12 条+尾注「…更早批次详见 CHANGELOG.md」（**7B 链长治理就此落地**——损坏实害成立后从冻结转实施·历史权威在 CHANGELOG 零信息损失）+去重断言（节点内 W token 不得重复·防线）。
> - **四页重建**：一次性脚本按「token 首现段」打捞原始未损坏文本（每批首次插入时段=完整）——index/dukou 各 11 条、danmaku/tag-cloud 8 条（其链 W717 起才有·历史链在注释区）+尾注；重建后四页 0 重复·161-409 字符。
> - **验收盲区补防**：级联四页脚断言新增去重检查（写入前拦截）——重复损坏自本批起不可能再发生。
> - **验证**：四页重建后 0 重复 + 级联 dry/apply（新裁剪逻辑真数据：插 W724 后 12 条+尾注）+ verify full + pytest + ruff + C4-f 提交时自证。
> - **状态**：已落地（CI 工作流以推送后 gh run list 为准）。
> - **文件**：scripts/batch_cascade.py、site/index.html、site/data/cross-time-danmaku.html、site/data/tag-cloud.html、site/dukou-engine.html、CHANGELOG.md、README.md、STRUCTURE.md、docs/00-导读/项目说明.md、交接文档.md、.github/workflows/README.md、AGENTS.md、CITATION.cff、scripts/output/file-index.md、docs/archive/AGENTS-ARCHIVE.md、scripts/_s7_foot_rebuild_20261012.py、docs/00-导读/W批次编号对账表.md。

### W723（2026-10-12）：级联清单反向覆盖根修批

> **来源**：用户圈选 HANDOVER v2 登记的根修候选「级联清单反向覆盖断言」现做（手工件漏 add 三犯 W721/W722 的根因收口·W537③ 八批旧账一并清偿）。
> - **根修（C4-f 文件清单入库对账·第 31 门禁）**：现役段「文件」行的 repo 相对路径 token ⊆ HEAD 树∪staged 且无工作树未提交残留，违者 FAIL——级联清单（C4-e）只列级联面，**手工编辑件唯「文件」行可追溯**（W721/W722 三处漏 add 全是清单外手工件）；缺「文件」行/无路径 token → NOTE 起步策略（W719/W722 实证近期批次缺行）。
> - **数据源强制（级联 precheck）**：spec changelog_body 必含「**文件**：」行，缺则 PRECHECK-FAIL——四件套必填项（维护契约③）自此有机器保证。
> - **成文**：pitfalls git 类新条（文件行全量列名义务+三犯实证）+W537③ 更新（「无门禁覆盖」→「C4-f 已覆盖」）+文档规范 §5 版本段补文件行路径形态规范（禁纯描述列举）。
> - **本批自证**：本段「文件」行即首个规范形态示范（全量 repo 相对路径·级联面+手工件）；self-test 16→18 例（T17 漏入库必红/T18 工作树残留必红）。
> - **验证**：self-test 18/18 + ruff 0 + verify full + pytest（级联后复跑）+ 提交时 C4-f 真数据自证（staged 场景）。
> - **状态**：已落地（CI 工作流以推送后 gh run list 为准）。
> - **文件**：scripts/check_doc_sync.py、scripts/batch_cascade.py、docs/agent/pitfalls.md、docs/00-导读/文档规范.md、CHANGELOG.md、README.md、STRUCTURE.md、docs/00-导读/项目说明.md、交接文档.md、.github/workflows/README.md、site/index.html、site/data/cross-time-danmaku.html、site/data/tag-cloud.html、site/dukou-engine.html、AGENTS.md、CITATION.cff、scripts/output/file-index.md、docs/archive/AGENTS-ARCHIVE.md、docs/00-导读/W批次编号对账表.md。

### W722（2026-10-12）：八项裁决执行批

> **来源**：用户 userselect「1A 2A 3A 4A 5A 6A 7B 8A」（第十七次挑刺=对我方推荐清单的 5 处质量问题全认领·修正版清单 v2 拍板）——八项裁决一次执行。
> - **1A+5A+4A（S-28 例行化+S-30/S-27 成文·文档规范 §4.11 扩三节）**：「外部输入裁决流程」（S-27 落点=§4.11 裁决记录形态旁·pitfalls 系坑位不纳流程·用户修正采纳）+「处置自查扩面五项」（S-30 落点·①同型数字 grep②解析面枚举③未跟踪件④锚点语义对拍⑤流程面·基线 25%=W713-W719 三批 8/32 小样本 n=3 在案）——**S-28 例行化并入五项②（FAM-12 橙警强化落地·依赖 5A 已满足）**+「技能卡降级/重启契约」（禁频率低作理由·降级须列不受保护路径+重启触发）。
> - **2A（C4-e 级联清单强校验）**：doc-sync gather 加 staged 集合（pre-commit 语境·CI/普通跑为空不适用）——提交树 ⊇ 当批 _cascade_files 清单，漏 add 即红（W649 漏 add 族机械化）；清单不存在→NOTE；**自建义务成文 pitfalls git 类**（手工级联批·W691/W693 先例 70 份在库）；self-test 14→15 例（T15 漏 add 必红）。
> - **3A（S-26 降级）**：第 37 篇 S-26 卡状态注——降级后不受保护路径仅两条（手工 Edit/一次性脚本写共享文档·后者有写盘前断言软覆盖）；重启触发=事故 ≥1 次/月或单次 P1；降级契约入 §4.11。
> - **6A（a4_docs 三处同改·EXPECT_A4 实体化收口）**：stats.py META+build 加 a4_docs 键（docs/03 顶层 .md−README·introduced_by W722）+五处叙述面标记化（README/STRUCTURE/AGENTS/交接/项目说明各一处现役口径·唯一锚点断言一次性脚本）+verify 第 3 门禁 EXPECT_A4 双形态适配（裸「209 篇」或「209<!--stats:a4_docs--> 篇」正则·门禁名沿用不改）；stats 15 键 --check 零差异（a4_docs=209 磁盘对上）。
> - **7B+8A（双结案登记）**：四页脚链长治理=维持现状（无实测危害证据·A/C/D 备选登记待展示面偏好出现再启）；bump_version=维持停用（级联已全覆盖其职责）。
> - **验证**：doc-sync self-test 15/15 + 门禁 0 FAIL + stats --check 零差异（15 键）+ verify full 46 段绿 + pytest 296 + ruff 0。
> - **状态**：已落地（CI 工作流以推送后 gh run list 为准）。

### W721（2026-10-12）：复盘增补与脚注滚动根修批

> **来源**：用户令「写今天 12 复盘」（模板第八次执行）+中途裁决「添加进 10-12 那篇复盘报告里面」（并入第 37 篇不另立）；W719 登记的根修候选「级联内建脚注滚动」同批现做（S-29·E-09 制度内建教训兑现）。
> - **复盘增补（§十·并入第 37 篇）**：续弧线 W713-W720 六批统一复盘并入 工作复盘与优化分析报告-2026-10-12.md（头部范围+执行摘要指针更新·文末 §十 增补节）——新增经验 E-09~16（E-09 制度必须内建执行机制 4.75 领衔/E-10 自查扩面 4.50/E-11 升格优于原方案 4.25）、技能卡 S-29 已交付+S-30 待拍板、问题 P-14~26 十三例全闭环（P0=0·P1=1·P2=8·P3=4·含 trim2 三败写盘前断言零污染）、FAM 增量（**FAM-12 升橙警**·单周期 6 起历史最高·强化建议=S-28 触发条件改例行化待裁决；**FAM-14 制度无执行机制新族双根修当期落地**；FAM-13 连续 6 批零复发接近关闭；FAM-02 黄警根因再分析=清单 add 依赖人手·S-19 升级评估待裁决）、WBS A-06~10、自评增补（可行·两条待裁决）。曾按新篇起草后经用户裁决并入（-2 件删除·docs/10 目录数不变·stats 免刷新）。
> - **S-29 级联脚注滚动内建（根修·A-06 交付）**：batch_cascade AGENTS 脚注面加条后自动检查条目数，>5 时最老条迁 AGENTS-ARCHIVE 尾块（**级联第 12 面**）+指针上界刷新——W713 建立的「保留最近 5 条」制度自此有执行机制（W719 R1 破约根因=制度无执行机制·E-09）；断言含条目序/切分连续性/尾锚；**本批级联即真数据首跑**（脚注 7 条→自动迁 W715/W716 留 W717-W721 五条）。
> - **验证**：S-29 首跑真数据过 + ruff 0 + verify full 46 段 + pytest 296（级联后复跑）。
> - **状态**：已落地（CI 工作流以推送后 gh run list 为准）。

### W720（2026-10-12）：C4 认领行强制批

> **来源**：用户 userselect 圈选 W719 报告的流程遗漏项（动工前未在对账表登记认领行）根修现做。
> - **根因**：C4 只查「W 号 ∈ 版段 ∪ 对账表登记集合」，而登记集合混合了两种形态——认领「表格行」（| W### |）与预留「豁免 bullet」（- **WXXX**：现势下一自由号…，RE_TABLE_DEFER 收纳）；W719 动工未登记认领行，主提交时被当批现势豁免 bullet 救场，机器不可区分、流程违例不拦。
> - **根修（C4 细分强制）**：C4 新增判定——CHANGELOG 现役段 W 号必须在对账表有「表格行」登记（RE_TABLE_ROW_W 单独取集·豁免 bullet 不算认领），动工前未登记则主提交即红（self-test T14 注入仅 bullet 形态必红·13→14 例）；认领行强制同时是「对账表=并发认领唯一依据」（W663 表头规则①）的机器化——W719 教训闭环。
> - **流程面同步**：gates.md 第 31 条 C4 描述+14 例；pitfalls.md git 类新条目（认领流程五步：取号→表格加行进行中→动工→级联→主提交→收官翻已收官）；本批自身先登记认领行再动工（新防线首次合规执行）。
> - **边界说明（如实留档）**：浅克隆跳过 C4（pre-commit 本地为主执行点·与既有 C4 同域）；并行会话场景下他方未登记时本方提交可能被连带拦——对未登记方是正确施压（同 checkout 并行本有互斥纪律·W649）。
> - **验证**：doc-sync self-test 14/14 + 门禁 0 FAIL（现役段 W720 认领行在场实证）+ ruff 0 + verify full + pytest（级联后复跑）。
> - **状态**：已落地（CI 工作流以推送后 gh run list 为准）。

### W719（2026-10-12）：review 修复批

> **来源**：用户令「review 一遍所有变动」（W708 先例第七次执行）——范围=本会话 W713/W716/W717/W718 四批八提交（其间交错并行会话 W714/W715 不在范围）：机械扫+逐提交审读+门禁复跑。
> - **机械扫八面**：混行尾 19 文件 0 / 段标题双写（CHANGELOG+file-index W713-W718 六段）0 / 四页脚链头全 W718（W717 新锚二次实证）/ 对账表豁免链 W713-W719 连续 / 契约头 4 件全在 / ARCHIVE 尾块闭合正确；**口径误报澄清**：CHANGELOG 三处「双标点」（。。/；；/））；）系 W708 历史段对黑名单的引述记载（历史段禁改）——机械扫黑名单命中须豁免「括号引述形态」，本批记入口径注。
> - **真发现 R1（P2·制度破约·修复）**：AGENTS 脚注累积 11 条（W708-W718），破 W713 自建「保留最近 5 条」滚动制度——级联只加不滚、制度无执行机制（W713 建制时未同批根修级联·本批如实留档）；修复=滚动迁移 W708-W714 七条迁 AGENTS-ARCHIVE（保留 W715-W719）+指针更新；**根修候选登记**：级联 AGENTS 脚注面内建滚动（加条后自动迁最老条·涉 ARCHIVE 第 12 面·待独立小批）。
> - **真发现 R2（P2·漏 add 族·修复）**：未跟踪 8 件——本会话 W716/W717/W718 级联 spec+msg 6 件（同族 _s7_×4 已随 W714 考古补库·未续做）+并行会话级联清单 _cascade_files_W714/W715.txt 2 件（W649「清单随批入库」漏执行）；修复=8 件统一补库（file-index W719 段逐件登记）。
> - **门禁复跑**：verify full 46 段绿（零 WARN·W717 页脚新锚 W718 级联自动插对链头二次实证）+ pytest 296 + doc-sync 13/13 + agents-layers 5/5 + w_range 4/4 + stats --check 零差异；四主提交抽检净（段标题清洗/rows 对应/lambda 替换/迁移幂等）。
> - **状态**：已落地（CI 工作流以推送后 gh run list 为准）。

### W718（2026-10-12）：变更史可追踪补正批

> **来源**：用户挑刺第十六次（stats-changelog.json 专项 5 项：P0×1/P1×3/P2×1）——逐条磁盘取证三态裁决（采纳 3/部分 1 升格 1/驳回 0）并落地；含快照澄清与 W704 空条目 git 考古定谳。
> - **P0 W704 空记录（采纳·澄清来源不删史）**：git 考古=首入库 commit（19d8b586）时 stats.py 终版已是条件式 append（if changes）——该空条目终版逻辑不可产生，系建账批开发迭代产物、append-only 从未清理；处置=保留（变更史只增原则·建账时点标记有价值）+ migrate_hist 注入 note 字段（考古结论随条目）+ docstring 记载；报告「2 条」系快照——现文件已 3 条（W716 条 methodology 33→34 系挑刺快照后 W716 批新增）。
> - **P1「检查过≠没检查」（部分采纳且升格）**：拒绝 _checks 数组/--log-check 两形态（--check 只读语义不该有副作用·无门禁强制的流程项必漏）——改 **C5d 挂载第 31 门禁**（doc-sync gather 内联 subprocess 跑 stats.py --check·实测 0.3s·漂移当场 FAIL）：检查记录权威载体=verify 输出与 CHANGELOG 验证栏，「漂移未刷新」（W715 methodology 漏 --w 实例）自此有机器防线·每批 verify 恒跑；self-test 12→13 例（T13 注入漂移必红）+gates.md 第 31 条同步。
> - **P1 无时间维度（采纳）**：entry 加 time 字段（HH:MM:SS·迁移旧条目 null）——同日多批可区分。
> - **P1 无 schema（采纳·结构升级）**：stats-changelog-v1={_schema, _field_notes, entries}——旧 list 形态 load 时自动迁移（migrate_hist·无变更也写回一次）；_field_notes 内嵌字段语义（w/date/time/changes/note/shapes/checks 分工）。
> - **P2 反向查找不在 json（采纳-轻）**：不改双索引（消费端仅 render_index·量小·append-only 是流水账自然形态）——_field_notes.shape 声明分工「本文件=时序流水账权威·按 W 反查用 stats-index.md 反向段（本文件渲染产物）」。
> - **验证**：迁移实跑（v1 形态+W704 note+time null 落盘）+ doc-sync self-test 13/13 + doc-sync 门禁 0 FAIL + ruff 0 + verify full + pytest（级联后复跑）。
> - **状态**：已落地（CI 工作流以推送后 gh run list 为准）。

### W717（2026-10-12）：页脚链头锚定根修批

> **来源**：用户 userselect 圈选 W716 段登记的遗留候选「页脚区锚定根修」现做（独立小批·量级预告兑现）。
> - **根因**：级联四页脚插入锚系 v 形态（`v[\d.]+ ·? W\d+`）——手工时代置于链头的 W 形态 token（W711-W716）使其永远命中最先出现的 v 形态 token（在头块之下），新批 token 每批插在链中而非链头；dukou 新鲜度门禁读 `<footer>` 链头 → 每批恒 WARN、每批需手工归位（W713/W716 两度实证）。
> - **根修（batch_cascade 四页脚段重写）**：锚改 `<footer>` 区内**首个批次 token**（双形态 `(?:v[\d.]+ ?·? ?)?W\d+`·与第 1 门禁 dukou 解析同语义·四页均恰有一个 `<footer>`），新批 token 恒插链头；插入改**位置切片**（s[:at]+new+s[at:]），顺带消除旧 `s.replace(全文首处)` 的歧义隐患（mm.group(0) 若在页脚前正文复现会替换错处）。链头前各页固定文案（MIT License/分隔注释/佛法=AI）不含 W token·不受影响；门禁侧无需改（读链头语义不变）。
> - **真数据验证**：本批级联即新锚首跑——dry-run 四页脚断言过；apply 后四页链头=W717、dukou 新鲜度门禁 OK（链头=现役自洽·后续批次不再需要手工归位）。**首跑即暴露两页语义差异（如实留档）**：danmaku/tag-cloud 两页 `<footer>` 内原无批次链——其历史链（W711-W716）在页内注释区（旧 v 形态锚命中处·不可见面），footer-meta 系静态遗留 token（`v2.3.282 · W676`）；本批起新批 token 以 footer-meta 为链头（用户可见面回归「页脚随批升版」本意·旧实现把 token 插进不可见注释反而违四页脚契约），注释区历史链冻结于 W716 留档不改；index/dukou 两页链本就在 footer 内·行为不变。
> - **连带根治（级联 CHANGELOG 插入）**：changelog_body 经 re.sub replacement 串语义写入——body 含正则字面量（`\d` 等）即 bad escape 崩（本批 spec 实证·dry-run 拦截）；改 lambda 字面替换（`lambda m: _ins`）·body 今后可含任意字符。
> - **观察登记**：四链 token 数 12-17 持续增长（无淘汰契约）——链长治理（上限+尾淘汰）待用户定契约，本批不扩。
> - **验证**：dry-run 四页脚新锚真数据过（连带拦截 body 反斜杠雷）+ apply 后四页链头 grep=W717 + dukou 新鲜度 OK + verify full + pytest + ruff。
> - **状态**：已落地（CI 工作流以推送后 gh run list 为准）。

### W716（2026-10-12）：stats 实体化补正批

> **来源**：用户挑刺第十五次（stats 实体化专项 8 条：P0×2/P1×2/P2×2/P3×2）——逐条磁盘取证三态裁决（采纳 4/部分 3/驳回 1）并落地；另自查新增 1 项实锤并修（methodology_docs 磁盘漂移）。
> - **P0-1 json_count 退役（采纳·方案甲）**：stats.py 移除该键（META+build）——其域 scripts/output/data/*.json 系 gitignored 本地产物（.gitignore:59），依赖它的键在无本地产物环境 --check 必红，违反「tracked 基准 CI 可复现」原则（W703 声明对该键不成立）；实测修正：CI/Makefile 现并不跑 stats --check（「任何机器必崩」降级为原则违反）·消费面=STRUCTURE 输出行标记与 agent_start 口径行，两处同批改写（STRUCTURE 输出行去标记改本地产物描述·agent_start 删 data json 段）。
> - **P0-2 scan_files/seo_scanned 合并指控（驳回+注释补明）**：口径块设计原话「各门禁分母不同」——两键系两门禁独立分母刻意分开（C5 按句式上下文对账无重复对账·将来某器排除面变化时各自跟随），合并反而耦合；采纳-微=build 注释补明「同算式系近似实算·分母以各器实际排除集为准」（check_seo_head SEO_EXCLUDE=两模板壳实测与算式一致）。
> - **P1 字段语义补明（部分采纳）**：introduced_by=口径首次**正式化**批次（META 注释原义已有·补「非历史首次出现批次」）；last_changed_by=stats.py 检出值变更的最近批次（建账前变更不记）——两者加 generator 恒同值省略列一并写入 stats-index 表头注（自动渲染·非手改）。
> - **P2-6 reader 621→622（部分采纳·考古定谳）**：git 考古=主题枢纽页批次新增 site/reader/themes-hub.html 一页（a785a0f0）——历史段禁改不回填，本段留档；stats.json last_changed_by 不动（语义=建账后检出变更·见字段语义注）。
> - **P3-7 _generated 粒度（采纳）**：补时分秒（同日多批可区分·变更史 date 仍为日期）。
> - **P3-8 a4_docs 缺位（部分采纳·登记不开工）**：维持上轮裁决——EXPECT_A4 字面量绊线保留不改读 stats.json；完整形态=三处同改（stats 键+叙述面标记化+第 3 门禁匹配形态适配——「209 篇」子串在标记化后失配，系实体标记破坏既有解析器的同族地雷），待独立小批认领。
> - **自查新增（实锤）**：stats.py --check 实测 methodology_docs 33→34 漂移——复盘报告批（W715）入库第 34 篇方法论文档但未同批 --w 刷新，「改口径批次须同批刷新」纪律违反实例；本批 --w W716 刷新（变更史记 33→34）+STRUCTURE 对齐 34。
> - **验证**：stats --check 零差异（14 键·json_count 退役）+ doc-sync self-test 12/12 + doc-sync 门禁 0 FAIL + ruff 0 错 + verify full 与 pytest（级联后复跑）。
> - **状态**：已落地（CI 工作流以推送后 gh run list 为准）。

### W715（2026-10-11）：工作复盘报告批

> **来源**：用户令「写今天 12 复盘」并下发《工作复盘与优化分析系统提示词（AI Agent 专用版）》第七次执行——范围=W702-W714 十三批弧线（2026-10-11/12）。
> - **报告入库**：docs/10-方法论沉淀/工作复盘与优化分析报告-2026-10-12.md（第 37 篇）——E 经验 8 项量化排序（结构断言落盘前拦截 5.00/replace 保留锚点 4.75/多行脚本化 4.75/解析面机器枚举 4.25/防线自证 4.25/三态裁决 4.00/切片搬运指纹对账 3.75/并行文件界协作 3.75）；skill-creator 三卡 S-26 级联安全守护器/S-27 外部输入三态裁决模板/S-28 形态切换解析面枚举器（S-28 按 YAGNI 待触发）；未用技能 3 项维持决策；高优场景 5 个全沉淀；问题 13 例全闭环（P0=0·P1=4·P2=7·P3=2）——新族 FAM-11 级联结构自指与跨段操作（修复后 5 批零复发）/FAM-12 形态切换解析面漏项（S-28 待触发）/FAM-13 提交信息形态（%s 复核新增）·FAM-07 黄警强化（S-27 含 git 基准 hash）；WF 形态切换双形态改造流；WBS 五行动（A-01 S-26 实现领衔）+可行性自评可行。
> - **方法论 README 索引**：第 39 行。
> - **验证**：verify full 46 段绿；报告过第 18 门禁（元信息块 v2）；索引第 39 行在位。
> - **文件**：docs/10-方法论沉淀/工作复盘与优化分析报告-2026-10-12.md（新增）、docs/10-方法论沉淀/README.md（索引第 39 行）、六文档级联、对账表。
> - **状态**：已落地（CI 工作流以推送后 gh run list 为准）。

### W714（2026-10-11）：停用守卫与考古补库批

> **来源**：用户圈选 review 遗留⑤⑥（bump_version 过时声明+未跟踪 _s4_* 清理）。
> - **⑤ bump_version 方案 D 停用守卫**：main() 入口检测四辅助文档「当前批次」新形态——命中即 STOP 提示并 exit（原生 ERROR exit 2 之上的明确指引·防旧 v 形态写回破坏方案 D 形态）；docstring 级注记；**工具归 batch_cascade 管辖后的存量收敛场景改用一次性脚本（_w702_edits.py 形态参照）**。
> - **⑥ 未跟踪清理（分三类）**：① `_s4_*/_s5_*` 151 件=S4 双盲本地件→**.gitignore 降噪**（原地保留·正式收账随 S4 收账批·git status 噪声清零）；② **历史漏 add 考古补库 43 件**=_cascade_files_W651-W712 清单 24 件〔W649「清单随批入库」规则自 W651 起系统性漏执行〕+_w657/_w663/_w672/_w676/_w678/_w685/_w691/_w697 散件 15 件+_s7_×4〔W713 会话件〕+_s23/_a02 素材 2 件——**统一补入库**·file-index W714 段逐件登记（原属批次随行注明）；③ 其余零散确认无遗留。
> - **验证**：bump_version 守卫实测 STOP+exit 0（四文档新形态）；git status 未跟踪 194→43→0（S4/S5 除外）；verify full 46 段绿。
> - **文件**：scripts/bump_version.py（守卫）、.gitignore（_s4_*/_s5_*）、scripts/_s7_×4+scripts/output 考古补库 39 件、docs/00-导读/W批次编号对账表.md（W714 认领）、六文档级联。
> - **状态**：已落地（CI 工作流以推送后 gh run list 为准）。

### W713（2026-10-11）：挑刺第十四次补正批

> **来源**：用户挑刺第十四次（三报告：治理文档 13 条+L2 三件 13 条+九脚本 17 条=43 项）——逐条磁盘取证三态裁决（采纳 40/事后应验 0/驳回 3/部分 0）并落地；另自查新增 5 项同批并修（级联 W712 修复漏提交/CHANGELOG 段标题重复根因/agent_start 阻塞提取越段/file-index 重复规模=146 行/交接里程碑指针旋转语义漂移）。
> - **级联旋转语义根治（自查项·滚动窗口契约恢复）**：里程碑淘汰目标改「窗口最老块」+「历史概要」指针改取淘汰后剩余最老块 + 删前断言 CHANGELOG 有段（级联契约原文承诺恢复）；原实现指针←new_w 使下批淘汰上批最新块、更老块永不滚动（W710→W711 实跑实证）；W712 手工段指针漂移已归位。
> - **脚本形态补课（每轮低估定律再应验）**：agent_start 现役解析双形态（实跑曾显示 v2.3.304 W710）+阻塞提取锚段标题+TASK_MAP 指 L2；级联 fb/blocks 双形态（否则 W713 块插错位+W714 必崩）+file-index 段标题清洗正则根治+项目说明「当前版本」行 out2 失配补断言；index_health 检查5 双形态（新段漏检）+governance_refs 子目录扩面+governance 检查5 group 对齐+docstring 校正；w_range_literal 历史段 W 号 int(None) 隐患；agents_layers T3 自测复活（4/5→5/5·自 W709 挂 41 起即失效）；doc-sync C5 面补 CONTRIBUTING；verify _SCOPE_CORE 补 7 内联段（自洽锁盲区）+注释 32→35 校数。
> - **治理文档与 L2 补正**：AGENTS 40→41 两处+头部指针改 L2 三件+脚注滚动迁移（保留最近 5 条·早段迁 ARCHIVE）；gates.md 41 槽标题+第 41 槽归组+速查表 4 处截断缺字+615 实体标记+第 7 槽共槽注记；agent-web.md 技术栈 React18/Vite5→React19/Vite8/TS7（package.json 实证）+引擎层 bullet（六工具/冒烟实证）+README 权威入口；STRUCTURE 02 段 26→215（磁盘实测）；项目说明 86→87 页+W711 残留清正（孤儿括号）+阅读契约头部；README 09 树补苦难意义论；CHANGELOG 归档段双形态表述；豁免盘点结论先行点名 8 项构成；对账表 W712 行裁决数对齐 CHANGELOG（8/4/2/1）+版段列幻影清正+翻已收官。
> - **裁决驳回留档（3）**：①对账表「> ## 现势」渲染指控——GFM 引用块内 ## 正常渲染 H2，非层级丢失；②pitfalls「孤儿加粗」——同行前部有开标记（**修复 site/data/json…），加粗实配平；③EXPECT_A4 改 stats 化——字面量即设计（门禁名自declared「EXPECT_A4 字面量」·漂移绊线语义），stats 化属数字实体化扩展应走独立方案批。
> - **验证**：verify full 46 段绿（自洽锁 46==46）+ pytest 296 + ruff 0 错 + 各门禁 self-test 全绿（agents-layers 5/5·doc-sync 12/12·w_range 4/4）+ agent_start 实跑现役解析正确 + file-index 去重后索引健康绿。
> - **文件**：8 门禁脚本（batch_cascade/agent_start/verify_delivery/check_index_health/check_governance_docs/check_w_range_literal/check_agents_layers/check_doc_sync）+AGENTS/ARCHIVE+L2 三件+五治理文档+对账表+交接+file-index。
> - **状态**：已落地（CI 工作流以推送后 gh run list 为准）。

### W712（2026-10-11）：W712 方案档挑刺补正批

> **来源**：用户挑刺第十三次（两方案档 15 条·P0×2/P1×6/P2×7）——逐条三态裁决（采纳 8/事后应验 4/驳回 2/部分 1）并落地；含挑刺 #6 的实质补验（搬迁内容指纹对账）。
> - **实质补验（挑刺 #6 P0「bullet 计数抓不到句子级丢失」）**：指纹对账实跑——git a998581d 时代 AGENTS §4.2/§4.3 原文 vs docs/agent/gates.md/pitfalls.md 现文——**40 条门禁标题全在位、31 条坑位首句全命中、31 条整行级守恒 0 缺失（零丢失实证）**；根因=迁移脚本为整段切片搬运（非人工重抄）·挑刺担心的丢失模式实际未发生，但验收缺陷属实（指纹对账已补为标准）。
> - **W707 分层方案档补「执行实录与挑刺补正节」（§七）**：① L2 实建 3 份裁剪记录（workflow 并入 pitfalls git 组·tools/dirs 裁剪留 L1·挑刺 P0 采纳）② AGENTS 实测 292 行修正「2000+」预估（挑刺者 2500-3500 估计亦未实测·驳回）③ C2 节标题存在性检查实证（§4.3 摘要形态兼容·CLAUDE 指针未改）④ 机制 4 未单独落地补录 ⑤ BL-24 编号跳空指控驳回（BL-21/22/23 挑刺时点已在后续批登记·时点失真）⑥ 本批三件验收实录补记。+阅读契约头部。
> - **W706 盘点档补「执行状态与挑刺补正节」（§七）**：① 漏扫精确 1112 处（差值·挑刺 P2）② 合计含 E 注记（挑刺 P2）③ 344 边界定义（W706 时点快照·含 W705 前历史·挑刺 P1）④ 硬耦合 5 来源标注（方案作者提议·**W711 实施定案=(ver|None, wnum) 保留 ver 组**·与建议不同以实施为准·挑刺 P2）⑤ 「执行前补做」措辞修正（三项在本档 v2 内·挑刺 P1）⑥ CFF 外部平台注记（CITATION 行内注释补形态说明·项目未接入自动 CFF 消费平台·挑刺 P1）⑦ workflows 4 处 W711 已核（action 注释与历史批注）。+阅读契约头部。
> - **裁决驳回留档**：挑刺 #3（BL 编号跳空）系时点失真（BL-21/22/23 挑刺者所读旧版交接文档中尚未登记·现全部收口）；挑刺 #1 之「2500-3500 行」估计未实测（实数 292）。
> - **验证**：指纹对账 0 缺失 + verify full 46 段绿 + pytest 296 + ruff 0 错 + stats --check 零差异 + w_range_literal CITATION 注释行兼容（W711 批次号形态·第 27 门禁绿）。
> - **文件**：docs/superpowers/plans/2026-10-11-agents-layered-restructure.md（§七+契约）、docs/superpowers/plans/2026-10-11-version-space-inventory.md（§七+契约+措辞）、CITATION.cff（version 行注释）、docs/00-导读/W批次编号对账表.md（W712 认领）、六文档级联。
> - **状态**：已落地（CI 工作流以推送后 gh run list 为准）。

### W711（2026-10-11）：W711 方案D形态改造批

> **来源**：用户 userselect 全选五 Backlog 第三批（BL-22 收口·三决策点按倾向落地·盘点档 docs/superpowers/plans/2026-10-11-version-space-inventory.md 硬耦合 9 项逐项）——**v 号形态切换生效批：自本段起 CHANGELOG 段标题与治理文档抬头去 v 号（批次键唯一）**。
> - **决策点 1（甲·段标题去 v）**：本段即首个新形态段 `### W711（2026-10-11）：标题`；W001-W710 段保留 `### vX.Y.Z（日期）：W###` 历史形态不改写（维护契约①）；沿革机器面三条=① 头部方案 D 声明段 ② doc-sync C1/C2/C4 正则双形态（历史 v 形态与新 W 形态并存解析）③ batch_cascade 段锚点/三模板/HEAD 句/页脚/交接标题双形态。
> - **决策点 2（丙·CITATION=W 号）**：CITATION.cff version 自本批=批次号形态（`"W711"`·CFF free string 不强制 SemVer）；下游消费者核实=CI 无 cff 校验 job、仓库无自动化 CFF 消费者（盘点档 §五）。
> - **决策点 3（甲·file-index）**：历史条目保留 v 引用、新段 W only（级联 file-index 段标题去 ver·格式分裂由 CHANGELOG 头部声明）。
> - **硬耦合改造落地**：① doc-sync RE_CHANGELOG_TOP/SECT/READMEE_HEAD/JIAOJIE_HEAD 四正则双形态+changelog_top 返回 (date, wnum) 二元组+C1/C2 对比二元组化（self-test 12/12·base 换新形态样例）；② verify latest_version_from_changelog 双形态（ver 可 None）+期望批次段 W-only 展示+dukou footer 与 workflows 旁文档锚定改「footer 标签内联/调用处 anchor 参数」（parse_footer_version 加 anchor 参数·W708 宽匹配咬正文教训应用）+六文档区 ver 条件化；③ batch_cascade cur_anchor 双形态+新段标题 W-only+README/STRUCTURE/项目说明三模板换「当前批次」抬头+「起生效」/HEAD 句/workflows 页眉/两页脚 prepend 去 ver+「一、当前进度」标题替换串去 ver（锚点已双形态）+CITATION version=batch+file-index 段标题去 ver；④ tests/test_verify_delivery_version.py 补两用例（新段 ver=None/页脚 W-only·13 过）。
> - **workflows 4 处豁免**（盘点 v2 零命中确认表修正）：dependency-review/scorecard 系第三方 action 版本注释（v4.9.0/v2.4.4·与项目 v 号无关）、ci/perf 系 W263/W266 历史批注——均无需改。
> - **验证**：verify full 46 段绿（旧 v 形态全兼容）+pytest 295（+2 方案 D 用例）+doc-sync self-test 12/12+agents-layers 0 FAIL+级联 dry/apply 自检过（**本段即首个 W-only 新形态段·级联全链在真数据上验证**）。
> - **文件**：scripts/check_doc_sync.py、scripts/verify_delivery.py、scripts/batch_cascade.py、tests/test_verify_delivery_version.py、CHANGELOG.md（头部声明+本段）、README.md（版本号说明节）、docs/00-导读/文档规范.md（§4.11 已实施注记）、docs/00-导读/W批次编号对账表.md（W711 认领）、六文档级联（新形态首写）。
> - **状态**：已落地（CI 工作流以推送后 gh run list 为准）。

### v2.3.304（2026-10-11）：W710 BL-25与BL-21收口批

> **来源**：用户 userselect 全选五 Backlog 第二批（BL-25+BL-21）——BL-24/23 已随 W709 收官。
> - **BL-25 执行**：STRUCTURE 02/04 段建置沿革（v0.10-W075 补齐叙事·约 1.2K 字符）迁 docs/archive/STRUCTURE-ARCHIVE.md（原文零改动追加 W709→W710 迁入节）——正文换现数+指针（「已建 26 篇」「已建 4 篇」·沿革见 ARCHIVE 与 CHANGELOG）；README 拆分评估结论落档=**维持不拆**（外链/统计口径/EXPECT_A4 字面量位置影响>收益·受众分段已由 W707 阅读契约头部承担）。
> - **BL-21 执行**：首份门禁豁免清单周期盘点报告 docs/00-导读/门禁豁免盘点-2026-10-11.md——逐门禁十项豁免/基线现状对仓取数；结论=**豁免面健康无吞噬证据**（全部「冻结存量只拦新增」语义·拦截面=新增漂移不随豁免缩小）·第 28 可引用性为已收敛标杆（344→0→全量 FAIL）·第 22 与 C5c 起步态跟踪·第 29 色盲 17428 对大基线待专项收敛批（路径参考第 28）；**BL-21 关闭**（转例行动作·下次盘点随大版本段归档或 2027-01 季度点取先到）。
> - **验证**：verify full 46 段绿；STRUCTURE 残留 v 引用降至 18（板块建置标注=历史事实保留）。
> - **文件**：STRUCTURE.md（02/04 段）、docs/archive/STRUCTURE-ARCHIVE.md（迁入节）、docs/00-导读/门禁豁免盘点-2026-10-11.md（新增）、交接文档.md（BL-21/25 状态更新）、docs/00-导读/W批次编号对账表.md（W710 认领）、六文档级联。
> - **状态**：已落地（CI 工作流以推送后 gh run list 为准）。

### v2.3.303（2026-10-11）：W709 BL-24分层搬迁批

> **来源**：用户 userselect 全选五 Backlog（BL-22/24/25/23/21）——第一批执行 BL-24（方案档 docs/superpowers/plans/2026-10-11-agents-layered-restructure.md 按图施工）+BL-23 并入（同属 AGENTS 瘦身）。
> - **L2 三件落地**：docs/agent/gates.md（§4.2 全量 40 条迁入·五组重排：内容与同步 1-5/结构与加载 6-11/声明与完整性 12-15/数据与一致性 16-26/编号与质量防线 27-40·迁移脚本守恒断言）+docs/agent/pitfalls.md（§4.3 全量 31 条六主题重排：CSS/视觉渲染 9·JS/CSP/运行时 3·git/提交/并发 7·级联/CHANGELOG 4·数据/内容可信度 4·流程/协作/取证 4·**第九条 shell 场景查坑表并入**）+docs/agent/agent-web.md（§4.4）——内容零改动仅结构与分组，均含阅读契约与「何时读」引导。
> - **AGENTS 瘦身**：292→275 行、字符量 40K→14.9K（-60%+）；§4.2 换紧凑编号摘要（41 行·五组）+指针；§4.3 换主题视图+六主题目录+高频铁则；§4.4 换摘要+指针——doc-sync C3 解析形态保留（摘要含编号清单·零改造）。
> - **BL-23 并入**：脚注 W458-W700 沿革（约 20K 字符）迁 docs/archive/AGENTS-ARCHIVE.md（禁读型契约·grep 查）；脚注保留 W701-W708 十条+指针；batch_cascade 尾锚点形态不变=级联透明（W709 级联实跑验证）。
> - **第 41 门禁挂载**：check_agents_layers.py——C1 L2 三件存在含契约/C2 编号三方对账（AGENTS §4.2 摘要==gates.md 条目==verify 实况最高槽位）/C3 AGENTS 行数上限 ≤450/C4 指针目标存在；--self-test 5/5；verify 第 41 槽四处同改挂载（名单/docs scope/markers/section wrapper）·自洽锁 45→46 段；文档规范 §8 表格行补第 41 描述与上限；gates.md 与 AGENTS 摘要同步扩 41 条（C2 三方对账 41==41==41 实证）。
> - **C5 闭环实证**：第 41 槽挂载后 stats.py --check 当场抓 gate_count 40→41 漂移并 --w W709 记账刷新——stats 对账链首次捕获自身挂载事件。
> - **验证**：搬迁守恒断言（40/31/7）+agent_start 双模式+第 41 门禁 0 FAIL+self-test 5/5+verify full 46 段绿+pytest 293+ruff 0 错+stats --check 零差异。
> - **文件**：docs/agent/gates.md、docs/agent/pitfalls.md、docs/agent/agent-web.md（新增三件）、docs/archive/AGENTS-ARCHIVE.md（新增·BL-23）、AGENTS.md（摘要层重构+脚注切分）、scripts/check_agents_layers.py（新增·第 41 门禁）、scripts/verify_delivery.py（第 41 槽四处+自洽 46）、scripts/stats.py --w 刷新产物（stats.json/stats-changelog.json/stats-index.md）、scripts/_w709_migrate.py（一次性·守恒断言在案）、docs/00-导读/文档规范.md（§8 第 41）、docs/00-导读/W批次编号对账表.md（W709 认领）、六文档级联。
> - **状态**：已落地（CI 工作流以推送后 gh run list 为准）。

### v2.3.302（2026-10-11）：W708 全变动对抗复审修复批

> **来源**：用户令「review 一遍所有变动」——范围=本日 W702-W707 十提交（4cec0494..HEAD·140 文件 2565+/103-）；机械扫描八面+对抗审读五发现，修复三项、勘误一项、留档一项。
> - **机械扫描八面 0 异常**：双标点（；；/））；/。。）全治理文档 0；混行尾 17 文件 0（load 断言防线在位）；阅读契约 10 份全在位；对账表 W700-W707 各恰一行无重复；CLAUDE.md 44 行（≤60）；本批全部新脚本与级联产物 17 件 tracked；版本行新模板形态（无空格）✓；状态门禁复跑全绿（verify full/stats --check 零差异/doc-sync self-test 12/12/lint_links 19559 链接 0 broken）。
> - **对抗审读发现与处置**：① batch_cascade 交接结构三断言（主标题前非空/段序零一二/指针在位）原实现于写后 selfcheck（WARN 非阻断·脏盘已落才报告）——**前置到交接面 pend 落盘前 raise 阻断**（真 fail-closed·写后断言保留双保险）；② 文档规范 §4.11 引用的盘点数字为 v1（7679 处/265 文件+硬耦合 8 项）——更新为 v2 实数（8791 处/826 文件+硬耦合 9 项）；③ W704 段「本轮 22 处标记」**三重失真勘误**：分项和 10+4+6+6=26≠22、实测 31（CHANGELOG 10/README 5/AGENTS 9/STRUCTURE 7）——违反 W496「验收数字当批现测」铁律（写 spec 时拍脑袋未实数），历史段禁改走本段勘误追记，教训并入 W496 条目执行记录；④ scripts/output/_w704_ledger_msg.txt 漏 add（W702/703/705/706/707 的 msg 均入库唯独 704 漏）——本批补入库；⑤ W706 chore 提交信息「翻state」英文混入（已推送不可改·留档警示）。
> - **审读确认正常面**：batch_cascade 最终形态逐块复核（三模板 \s* 兼容/join 守卫/标题双形态锚点/段内首块与 drop 段内断言/load 混行尾逻辑四态验证）；check_doc_sync C5/C5b/C5c 与设计一致；stats.py 实体化+--check 零差异；交接文档终态（块链 W707/W706/W705 滚动·指针 W707·头链三条·HEAD 句）；CITATION 2.3.301；file-index W707 段在位；agent_start --task 七类分类实测；对账表 W700-W707 行结构完整。
> - **验证**：verify full 45 段绿 + pytest 293 + ruff 0 错 + 前置断言在重建态文件上实跑通过 + 机械八面复扫 0 异常。
> - **文件**：scripts/batch_cascade.py（结构断言前置）、docs/00-导读/文档规范.md（§4.11 数字）、scripts/output/_w704_ledger_msg.txt（补入库）、docs/00-导读/W批次编号对账表.md（W708 认领）、六文档级联。
> - **状态**：已落地（CI 工作流以推送后 gh run list 为准）。

### v2.3.301（2026-10-11）：W707 分层重构先行件与阅读契约批

> **来源**：用户方案第十条（AGENTS L0/L1/L2 树状化）与第十一条（八份治理文件阅读契约）——本批=先行件（方案档+头部提示+--task+契约头部），阶段 1/2 内容搬迁登记 BL-24 下批按图施工（doc-sync C3 解析源与 check_claude_md C2 锚点属精确性改造）。
> - **分层重构方案档入库**：docs/superpowers/plans/2026-10-11-agents-layered-restructure.md——目标结构（L0 CLAUDE 已就位/L1 AGENTS ≤400 行索引/L2 docs/agent 六文件）+内容搬迁映射（§4.2→gates.md 五组重排/§4.3→pitfalls.md 七主题〔含第九条 shell 查坑表〕/脚注→AGENTS-ARCHIVE〔=BL-23 合并执行〕）+硬耦合 7 项（doc-sync C3 双源/C2 锚点同步/级联锚点不变确认/W520 叙述面与 C5 扫描域豁免裁定〔L2 不入·头部声明历史引用〕/新校验门禁/--task 映射表）+验收清单（行数断言/指针可达/内容零丢失对账）。
> - **AGENTS 头部阅读契约**：索引型声明（不要线性通读·先跑 agent_start --task·§4.2/§4.3 按需查表·§1-3/§6/§7 必读）。
> - **agent_start.py --task**：按 git status 改动路径七类分类输出「本次任务相关」必读清单（TASK_MAP 常量·L2 就位后 BL-24 升级为文件级）——与 W705 全局摘要互补（摘要答项目什么状态/--task 答本次读什么）；heredoc 三败后按场景分层铁律改 Write 全量重写（教训自证）。
> - **阅读契约头部×10**（用户方案第十一条阶段 1）：CHANGELOG 查表型/交接 首段+查表/STRUCTURE 索引型/README 分段型/AGENTS 索引型/CLAUDE 通读型+归档 4 份禁读型（grep 单段查勿通读·用户明示授权头部元数据·历史内容零改动）——每份 3-5 行「类型/何时读/读多少/不要读」。
> - **BL-24/25 登记**：分层内容搬迁（阶段 1/2）+契约配套正文手术（STRUCTURE 沿革迁出/README 拆分评估登记不开工）。
> - **验证**：agent_start 双模式冒烟（全局摘要+--task 分类清单）+py_compile+ruff 0 错；verify full 45 段绿；契约头部 10 份 grep 在位。
> - **文件**：docs/superpowers/plans/2026-10-11-agents-layered-restructure.md（新增）、scripts/agent_start.py（--task+重写）、scripts/_w707_contracts.py（一次性）、AGENTS.md（头部契约）、CHANGELOG.md、交接文档.md、STRUCTURE.md、README.md、CLAUDE.md、docs/archive/×4（头部契约）、交接文档.md（BL-24/25）、docs/00-导读/W批次编号对账表.md（W707 认领）、六文档级联。
> - **状态**：已落地（CI 工作流以推送后 gh run list 为准）。

### v2.3.300（2026-10-11）：W706 编号空间盘点与元规则批

> **来源**：用户方案第四五阶段（结构性发现 10 项+v 号空间元规则）——本轮=盘点与元规则起草（方案 D 形态改造待 W707 三决策点拍板）；含用户对盘点 v1 的八项挑刺全采纳（E 类单列/零命中确认表/file-index 拆分与决策点 3/沿革机器面/丙选项/页脚边界/测试钉语义/词义句）。
> - **v 号使用点全量盘点**（docs/superpowers/plans/2026-10-11-version-space-inventory.md·v2）：**8791 处/826 文件**六类分域（A 历史段 1316/B 现役版本行 70/C 页脚站点 1009/D 脚本 137/E CITATION 1/F 叙述面 6258·file-index 系最大消费方 4652）+硬耦合 9 项+零命中确认表（CLAUDE.md 0 处=W664 设计实证·workflows 4 处非 0）+三决策点带倾向（① 段标题去 v+沿革机器面 ② CITATION version 丙=W 号形态 ③ file-index 甲=历史双列）+双键不单调实证（v2.3.262〔W661〕列于 v2.3.261〔W666〕后）。
> - **盘点自纠如实入档（保真度纪律）**：v1 首跑踩 W523 quotePath 坑（git ls-files 中文路径八进制转义→io.open 失败漏扫约 1100 处·交接文档-ARCHIVE 342/reader 中文页/对账表 80 等）——总数 7679→8791；E 类 CITATION 无 v 前缀形态被 pattern 排除误记 0——用户挑刺后单列。脚本随批修正并注明。
> - **文档规范 §4.11 编号空间与标识符纪律**：编号空间字典（W/S/B/A/E/P/SC/WF/FAM 各空间互不混用·引用带前缀禁裸编号）+v/W 双键元规则（时间点查询以 W 为准·v 号合并段区间不单调实证）+范围词汇定义（全量/现役/版本四语义）+标识符禁令（叙述引用用标题/键锚点禁行号）+裁决记录形态（来源字段+对账表双处·撤销=新批反转）。
> - **AGENTS 三处**：§4.3 主题视图索引块（CSS/JS/git/级联/数据/文档/Windows 七类按需查坑·正文不动）；§5.2 检查层次映射（md/site/py/数据面/CI 五层·本地绿≠CI 绿）；§8 清单间裁定链（文档规范 §11>CHANGELOG 现役段>交接·三视角清单声明）。
> - **配套**：CONTRIBUTING 权威清单补 CLAUDE.md；CHANGELOG 头部 v/W 双键口径声明；交接 Backlog 新增 BL-21（豁免清单周期盘点·用户挑刺 #6）与 BL-22（方案 D W707 预告·三决策点）。
> - **交接文档结构修复（用户第三次挑刺 P0 实锤·级联工具复合缺陷根治）**：W705 里程碑块错位于主标题前+「一、当前进度」标题缺失（零→二跳段）——考古=头部错位块链 W700 时代已现（batch_cascade 的 fb=re.search 全文找首块·错位后逐批自我强化），W702 级联 drop_block 跨段整块淘汰吞掉段标题（淘汰范围从头部 oldest 块跨到历史概要指针）；根治四件=① 标题替换锚点改双形态+count 断言（旧替换串丢 ver 前缀致下一批锚点静默失配）② 里程碑首块断言必须位于「一、当前进度」段内 ③ drop_block 最老块段内断言 ④ 交接文档手工重建（头部清零/段序零一二恢复/近 3 批块搬回/指针改 W702 及更早）；修复后级联 dry 在重建件上验证锚点全过。
> - **挑刺其余裁决（7 条中 3 真 4 旧快照）**：真=CONTRIBUTING 仍引用已脱节的 article-template（改「以目标目录实际结构为准·勿直接套用」）+CLAUDE.md 常用命令缺 agent_start（补一行·42/60）+AGENTS 脚注 200+ 行（**BL-23 登记待排期**·迁移须核级联锚点）；旧快照驳回 4 条=README「26 项门禁」（现值 40·W702 已改+C5 对账 gate_count 过）README/STRUCTURE 版本行 v2.3.294 滞后（级联逐批重写·现值 v2.3.299）CHANGELOG 279/280 缺空行与四件套（W702 已补录「（W702 补录」×4 在案）STRUCTURE「6 篇/30 类」（C5a 对账 33 篇/34 类通过即铁证）。
> - **shell 场景分层铁律（用户第八条消息·W706 三败教训制度化）**：单行命令任意 shell；多行/复杂转义一律落 Python 脚本文件（AGENTS §4.3 heredoc 条目升级——Git Bash python heredoc 同样有反斜杠四层转义/迭代器空/混行尾三类败·与 PowerShell 无关）；Windows Terminal 双 profile 装配为用户侧动作。
> - **验证**：verify full 45 段绿；vscan 修正后全量重扫实数入档；doc-sync self-test 12/12；交接结构自证（主标题前干净·零一二级序·段内块）。
> - **文件**：docs/superpowers/plans/2026-10-11-version-space-inventory.md（新增·v2）、scripts/_w706_vscan.py（新增·一次性·含 W523 修正注记）、docs/00-导读/文档规范.md（§4.11）、AGENTS.md（§4.3/§5.2/§8）、CONTRIBUTING.md、CHANGELOG.md（双键口径）、交接文档.md（BL-21/22）、docs/00-导读/W批次编号对账表.md（W706 认领）、六文档级联。
> - **状态**：已落地（CI 工作流以推送后 gh run list 为准）。

### v2.3.299（2026-10-11）：W705 Agent开局状态摘要批

> **来源**：用户方案第三阶段「Agent 惰性×文档膨胀联合治理」五步路线——本轮执行第 2 步（agent-start 状态摘要），第 3/4/5 步分级裁决（见下）；第 1 步已由 W703/W704 落地。另含对账表 W702 行首拆分修复（W704 登记 replace 误吞行首的损伤随 19d8b586 入仓·本轮 git 历史取证定位后还原）。
> - **scripts/agent_start.py**：会话开局实读磁盘输出当前事实摘要——现役三元组（CHANGELOG 顶段解析）/近 3 批次/stats.json 全键规模口径/对账表现势下一自由号/交接「零、当前阻塞」头部/开局三查与收尾纪律指针；无缓存无硬编码（值全部来自磁盘实时读取=防「记忆代读」的物理手段）；--json 供程序化消费；stdout UTF-8 兜底（Windows 控制台 GBK）。
> - **挂接**：AGENTS §7 快速上手路径新增第 0 步（开局先跑本脚本）；CLAUDE.md 接手导航首部插入同款指令（41/60 行约束内）。设计边界如实声明：宿主 system message 强制注入是宿主侧能力，项目侧最强形态=CLAUDE.md 自动加载指令 → Agent 开局看到指令 → 跑脚本刷新记忆。
> - **对账表 W702 行首拆分修复**：W704 登记时 replace 以 W702 行首为插入锚点但未保留锚点自身——W702 行首被替换为「W703 翻收官+W704 新行」，W702 正文并入 W704 行（两行合并·C4 表格行判定失真风险）；本轮定位后拆行还原 W702 行首+删除误复制的 W703 重复行。**教训沉淀：replace 插入语义的锚点必须包含「保留自身」——用「锚点前插入」形态（new=新行+锚点）而非「锚点替换为新行组」**。
> - **分级裁决（用户方案 3/4/5 步）**：阶段 3（rules.json+gen_claude_md 生成化）**驳回**——CLAUDE.md 系 W664「指针化·零漂移值·零维护成本」设计，生成化使 rules.json 成为与 AGENTS/文档规范并立的第三规则真源（副本数不减反增·违背「单一事实源」诊断）；阶段 4（state.json+状态指纹）**驳回**——现役版本/W/门禁数/篇数已在 CHANGELOG 顶段+stats.json+对账表三处权威，state.json 系第四份副本，「提交信息写指纹」污染 C4 对账；阶段 5（challenge.py 挑战-响应）**登记不开工**——用户自评「会被绕过·更适合诊断性而非阻断性」（登记态可随时重启）。
> - **验证**：agent_start 冒烟输出全键正确（现值与 stats.json 对账一致）；verify full 45 段绿；pytest 293；ruff 0 错；对账表 W700-W705 行结构完整（各恰一行）。
> - **文件**：scripts/agent_start.py（新增）、AGENTS.md（§7 第 0 步）、CLAUDE.md（接手导航）、docs/00-导读/W批次编号对账表.md（W705 认领+W702 行首修复+现势 W706）、六文档级联。
> - **状态**：已落地（CI 工作流以推送后 gh run list 为准）。

### v2.3.298（2026-10-11）：W704 数字实体化批

> **来源**：用户方案第二阶段「数字制度化/实体化」（W703 同日追加·修正「禁写数字」为「数字有身份」）——数字可写、必须写、且必须是实体：有 key、有生成器、有 W 号、有反查路径、有机检；渲染侧 HTML 注释在 GitHub 与 site/reader 双态均隐藏=视觉零损（决策点落定）。
> - **stats.json 实体化（entity-v1）**：每键 {value, domain, generator, introduced_by, last_changed_by}（META 登记制 15 键·domain 与口径起点 W459/W493/W505/W528/W591/W676/W070 考据落档）；变更史=scripts/output/stats-changelog.json（stats.py 重跑 diff 旧值自动追加·--w 记批次）→ scripts/output/stats-index.md 反向索引（正向 key 实体卡+反向 W→stats key 变更·与 file-index 同构·自动生成禁手改）。
> - **C5b 数字实体标记对账**：治理文档现役关键数字加 <!--stats:KEY--> 标记（数字紧贴·前置值==stats.json value·键未登记 fail-closed）——本轮 22 处（CHANGELOG 口径块 10/README 4/AGENTS 6+make analyze 双处/STRUCTURE 6）；标记处由 C5a 句式对账自然切换为 C5b 精确锚点。
> - **C5c 裸聚合数字报告**：标记/句式覆盖外的 N[页项篇个类] 记 NOTE（首跑 97 处=内容描述数字〔板块篇数/维度数/表格计数〕·报告型不阻断·起步策略收敛后评估转 FAIL）；行级豁免沿用。
> - **配套**：check_doc_sync --self-test 10→12 例（T11 标记失配必红/T12 未登记键必红·两例首版测试串数字与标记未紧贴自纠）；AGENTS §4.2 第 31 条目 C5b/C5c；文档规范 §4.10 增补「数字实体化」与「C5 三层分工」（C5b 权威锚点/C5a 句式兜底/C5c 报告起步）。
> - **验证**：self-test 12/12 + 首跑 0 FAIL·1 NOTE（C5c 97 处留观）+ stats.py --check 零差异 + verify full 45 段绿 + pytest 293 + ruff 0 错。
> - **文件**：scripts/stats.py（实体化重写）、scripts/output/stats.json（entity-v1）、scripts/output/stats-changelog.json（新增）、scripts/output/stats-index.md（新增）、scripts/check_doc_sync.py（C5b/C5c）、scripts/_w704_docsync.py 与 scripts/_w704_marks.py（一次性）、AGENTS.md、README.md、STRUCTURE.md、CHANGELOG.md（标记）、docs/00-导读/文档规范.md（§4.10 增补）、docs/00-导读/W批次编号对账表.md（W704 认领）、六文档级联。
> - **状态**：已落地（CI 工作流以推送后 gh run list 为准）。

### v2.3.297（2026-10-11）：W703 聚合数字对账门禁批

> **来源**：用户方案「40 个门禁仍漂移——根因诊断与 A+C 路线」（W702 挑刺 17 项裁决同日追加）——聚合数字系磁盘可计算量以手写常量散落叙述文本，逐点设防有天花板；按修正形态落地（A=stats.json 磁盘实算+C5 对账；C 裁剪为句式白名单+指针化规范——CHANGELOG 历史段须记录当批口径、README 内容规模数字面向读者且已受第 3 门禁磁盘对账，故全量禁写不采纳；占位符回填不采纳，循 W652 design-tokens 机器生成权威先例替代）。
> - **stats.py + stats.json**：scripts/stats.py 从磁盘实算 15 键（html_total 857〔site/data 88+en 138+根 9+reader 622〕/csp_covered 856/scan_files 与 seo_scanned 855/inline_css_pages 330/visualization_pages 87/gate_count 40〔verify 槽位实解〕/a1_a6_docs 615〔排除六板块 README·口径对齐第 3 门禁·首跑 621 差 6 即此〕/methodology_docs 33/json_count 135/script_classes 34）+ --check 零差异自证；stats.json tracked 入库（CI 可复现·「gitignored 不作基准」第 40 门禁教训同源）。
> - **C5 聚合数字对账**（第 31 门禁第 5 查）：18 式高危聚合句式×现役叙述面（README/STRUCTURE/AGENTS/项目说明全文+CHANGELOG 仅口径块行+AGENTS 版本脚注剥离）vs stats.json 实时对账——失配=FAIL、stats 缺键=fail-closed、基线/首跑时点值靠句式表设计豁免（第 33/34 门禁「235 页扫描」无 seo 语境自动放行实证）、行级豁免沿用；--self-test 7→10 例（T8 失配必红/T9 行级豁免放行/T10 stats 缺失 fail-closed）。
> - **首跑即产证**：C5 抓 AGENTS 版本脚注 W514 条目「约 86 个可视化页」时点实况（历史记录非漂移）——据此把脚注区剥离出扫描域（历史段豁免哲学），正文现役值全对账通过。
> - **配套规范**：AGENTS §4.2 第 31 条目扩 C5；文档规范新增 §4.10 聚合数字书写规范（唯一基准/现役叙述面句式对账/新增聚合量登记制/时点值豁免边界）。
> - **验证**：check_doc_sync --self-test 10/10 + 首跑 0 FAIL；stats.py --check 零差异；verify full 45 段绿；pytest 293；ruff 0 错。
> - **文件**：scripts/stats.py（新增）、scripts/output/stats.json（新增·tracked）、scripts/check_doc_sync.py（C5）、scripts/_w703_docsync.py（一次性）、AGENTS.md（第 31 条目）、docs/00-导读/文档规范.md（§4.10）、docs/00-导读/W批次编号对账表.md（W703 认领）、六文档级联。
> - **状态**：已落地（CI 工作流以推送后 gh run list 为准）。

### v2.3.296（2026-10-11）：W702 六文档口径清债批

> **来源**：外部「挑刺」报告（六治理文档口径与排版扫描·17 项 P0-P3）——逐条对仓取证裁决：实锤 15 项落地、误定位 1 项改址修复（双分号实为 AGENTS 脚注 4 处非 CHANGELOG）、1 项驳回（防新增漂移字面量）。
> - **P0 口径四件**：CHANGELOG 头部「全站页数口径」按实跑整段刷新（234/233/232/225/86 → 857/856/855/330·site/reader 622 页纳入·可视化页 87=88 减 _shell）；AGENTS §4.2 第 8 门禁「233 页」→856 页（generate_csp 实跑）；README AI 说明「26 项自动化门禁」→40 项（对齐 §4.2 现役 40 槽）；STRUCTURE 10-方法论沉淀「已建 6 篇」→33 篇（目录实数·补索引指针·原 6 篇标注为奠基篇目）。
> - **P1 两件**：STRUCTURE scripts 段「已建 30 类」→34 类子目录全建（磁盘枚举实证）+F 行可视化页补 story-timeline.html（W694 起·第 39 门禁双源）；AGENTS 第 6 门禁「三豁免」→「五豁免」（W700 lint_links 五改对齐）。
> - **P2 三件**：CHANGELOG v2.3.279/280 两段补录四件套缺失「文件/状态」字段（git show 7aaa1f59/27f07e7e 取证·只增不删带 W702 补录标记）+段间空行归一；AGENTS 第 26 门禁「334 页扫描」→855 页（check_seo_head 实跑·site 全树减两个模板壳）；CONTRIBUTING 三件套表后补 W### 认领对账表入口段。
> - **P3 排版与速查（含根治）**：README/STRUCTURE/项目说明版本行空格根治——batch_cascade 三处版本行模板去空格 + README/STRUCTURE 锚点同步 \s* 兼容（防逐批复发）；「（A4 209 篇 已含）」存量两处归一；AGENTS 脚注双分号 4 处归一 + batch_cascade join 去重守卫（前条目尾「；」时不再补）；CLAUDE.md 常用命令补 verify --scope auto 轻量档一行（≤60 行约束内·40/60）；AGENTS §4.2 前言补 pre-commit --scope auto 指引（对齐 §4.3）。
> - **顺带实数校真**：STRUCTURE「data/ 当前 131 个 JSON」→135（glob 实数）；STRUCTURE timeline/ 「取经路线图/人物时间线 待建」经 git ls-files 核实维持（仅大事年表已建·挑刺此条无需改）。
> - **驳回留档**：挑刺建议第 27 门禁条目补「W700 时现役上限=W700」静态字面量——违反 W520 递增数字禁字面量纪律（门禁本动态取 CHANGELOG max W 比对·静态化即制造下一个腐烂点）。
> - **验证**：verify full 45 段自洽绿 + lint_links 0 broken + ruff 0 错 + pytest 293 全过 + batch_cascade 原生 dry+apply 自检过（模板改动后锚点全过）+ generate_csp --check 0 漂移。
> - **文件**：CHANGELOG.md、README.md、STRUCTURE.md、AGENTS.md、CLAUDE.md、CONTRIBUTING.md、scripts/batch_cascade.py、docs/00-导读/W批次编号对账表.md、scripts/_w702_edits.py（一次性）、六文档级联。
> - **状态**：已落地（CI 工作流以推送后 gh run list 为准）。

### v2.3.295（2026-10-11）：W701 BL-20动工与S-26工具化批

> **来源**：用户圈选四项裁决（BL-20 动工另批/S-26 开工/A-03 优先序确认/报告正文同步）。
> - **BL-20 读屏替代文本/键盘导航落地**：site/static/js/chart-a11y.js 新模块（运行时为 svg/canvas 图表注入 tabindex+role=img+aria-label〔最近前驱标题〕+aria-describedby 指向 sr-only 摘要块〔图名+KPI 摘要+数据源指引〕·MutationObserver 兜晚渲染·幂等标记·零页面静态 DOM/CSS 改动·file:// 直开可用）+ scripts/inject_chart_a11y.py 注入器（幂等·--check 模式）·87 页全量注入（cite-box.js 同款外部本地脚本形态·无内联哈希需求）。
> - **验收**：_w701_a11y_probe.js 探针 87 页 file:// 全扫失败 0（无图页 N/A 判定=对话/搜索页纯文本+tag-cloud 词云 div 群对读屏天然可读+-view 壳页）+ 3 页键盘 Tab 焦点抽样 ✓（含 Three canvas 页）+ render_check 三页双态 PASS + verify 45 段全绿 + pytest 293。**EN 镜像页（site/en/）为登记余项**。
> - **S-26 worktree 预演器**：scripts/worktree_rehearse.py——E-14 三步手工封装（worktree add 临时树+工作区改动定向拷入+临时树内跑校验+always 清理·--tool lint/verify·--keep 调试），**首跑即拦注入器双 static 真 bug**（../static/static/js 拼接错·--check 存在性校验照不到路径正确性·docs 口径 lint 照不到 site——工具化当批即回本）。
> - **报告正文同步**：第四篇复盘 §3 三卡待拍板→已交付（W699）、§8 WBS A-01/A-02/A-04 排期→✅ 已交付+A-03 优先序经用户确认（A-02>A-01>A-03>A-04）；交接文档 Backlog BL-20 行翻已执行（EN 镜像登记余项）。
> - **级联外提交追记（W649 规）**：2bf126ed（W699 第 40 门禁挂载·verify 45 段）、a013c8b4（第四篇复盘增补一）、c64d3549（W700 review 收尾三件）、4cec0494（第四篇复盘增补二）。
> - **验证**：worktree_rehearse 全仓口径预演 0 broken + verify full 45 段 + pytest 293 + ruff 0 错 + 探针全绿。
> - **状态**：已落地（CI 工作流以推送后 gh run list 为准）。

### v2.3.294（2026-10-11）：W700 docs全量链接门禁与断链清债批

> **来源**：外部「挑刺」P1（docs 活文档断链+链接门禁覆盖缺口）与 P3-1/P3-2 捎带项，经用户裁决「①+捎带」落地。
> - **断链清债 22 条**：13d→16d 死链×8（docs/03 专题×4 文本+URL、docs/S2 学术候选×4——W676 重命名 sweep 漏网）+ skills 退役死链去链保文×7（docs/10 两篇方法论——W562 删除正源无存活承接载体）+ 并行批归档改链相对深度错×5（方法论 README ../../archive→../archive）+ STRUCTURE 根级双跳出×1 + 决策清单 S4 本地件去链×1。
> - **lint_links 五改**：① fenced/inline code 去噪（site-quality 方案档正则文本曾被误判为链接）② git check-ignore 豁免本地产物（docs/S4 双盲件 102 条噪音出清——字节流 UTF-8 防 GBK 错位+C 引号双反斜杠归一两坑实证）③ docs/archive/ 冻结档默认排除 ④ POSIX 根绝对路径跳过（agent-web Vite 入口形态）⑤ _w588_ce.html 快照件点名排除。
> - **第 6 门禁扩域**：docs01链接→**docs链接**（--dir docs 全量，挂载即绿：docs 口径 5191 链接 0 broken、全仓口径 19472 链接 0 broken），AGENTS §4.2 第 6 条措辞同步。
> - **ci.yml 残件清理**：screenshots-regression→**pages-smoke**（Site Smoke HTTP 200 存活烟测·名实相符），fallback 扫描与永不产出的 screenshots/diff artifact 两残件删除；真实截图回归仍在 screenshot-review.yml。
> - **验证**：lint docs 0 broken+全仓 0 broken；verify full 44 段自洽绿（docs/site 两 scoped 档实跑）+ ruff 0 错 + pytest 293 全过。
> - **文件**：scripts/lint_links.py、scripts/verify_delivery.py、.github/workflows/ci.yml、docs/03×4、docs/S2×4、docs/10×3、STRUCTURE.md、六文档级联、对账表。
> - **状态**：已落地（CI 工作流以推送后 gh run list 为准）。
