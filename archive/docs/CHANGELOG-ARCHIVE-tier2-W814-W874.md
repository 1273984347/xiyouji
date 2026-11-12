# CHANGELOG-ARCHIVE-tier2-W814-W874（二级归档容器·范围件）

> **📖 阅读契约（W707）**：禁通读——本文件为 archive\docs\CHANGELOG-ARCHIVE.md 的二级归档层（文档规范 §11.2·W513 先例）。
> 拆分约定（W995）：范围命名 `*-tier2-W<lo>-W<hi>.md`·单件 ≤1MB（check_archive_health T1b 监视）。
> 归档时间：2026-11-13（W995 首建）

> 归档追加：2026-11-13（W994 迁入 W814-W874）

### W814（2026-10-20）：去品牌扩展批（另两个同类品牌字面全量清除）

> **来源**：用户裁决「另两个同类品牌字面与首轮已禁品牌同类·同样禁止并全面修改」——承接 W812 去旧厂商 Agent 工具品牌化批，把另两个同类品牌字面一并纳入禁令并全仓清除。
> - **文件**：docs/00-导读/W批次编号对账表.md、CHANGELOG.md、HANDOVER.md、CLAUDE.md、.gitignore、xiyouji-agent-web/server/engine/tools.ts、scripts/output/file-index.md、scripts/output/_w814_spec.json。
> - **按语义分治而非一刀切**（承 W812 机制·保住多 Agent 可区分性）：认领会话列的会话标识 → 「并行 Agent 会话」（与既有的「DSH」「主会话」并列·不塌缩为单一标识·对账表认领行逐条可追）；生成模型署名 → 「GLM（本地 Agent 会话 …）」（与认领会话列区分·前者指模型运行环境·后者指批次执行方）；厂商品牌复合表述 → 「旧厂商 Agent 品牌」/「（含另一同类品牌）」；已退役的凭证变量名（该厂商前缀的一组环境变量·形如 `<厂商前缀>_API_KEY` / `_AUTH_TOKEN` / `_BASE_URL` / `_INTERNET_ENVIRONMENT` / 通配前缀形式）→ 「旧厂商_*」；已退役 CLI 的用户级路径 → 「.旧厂商目录」。
> - **特例逐条定稿（不机械替换）**：① 归档检测器脚本 `archive/scripts/batches/misc/_audit_agentweb_baseline.py` 的**搜索模式字面**是「检测残留品牌」这一工具功能本身（改掉即失去检测能力）→ 按 W812 先例登记豁免保留；② 行为性代码 `xiyouji-agent-web/server/engine/tools.ts` 的 `SKIP_DIRS` 含该品牌目录名（防目录遍历扫进本地工具目录）→ 改为中性目录名，防护功能保留；③ 本地索引配置文件（未跟踪·含品牌字面）→ 先把其 24 条独有忽略规则**并入 .gitignore**（功能不丢）再备份至项目外 TEMP 并移除项目内副本（对齐 W812 对同类本地配置的处理）；④ 与新裁决矛盾的**现役叙述**（W812 批摘要里「某品牌不在禁令范围故保留原名」一句）→ 按文档规范 §4.11「撤销=新批次裁决反转并引用原段·禁改历史段」，CHANGELOG 历史段不改（由本段承载裁决变更）·HANDOVER 现役叙述就地订正。
> - **两处工程教训（本批实战暴露）**：① **git grep 路径转义**——git 默认把非 ASCII 路径转义成八进制，拿这种串去 `os.path.isfile` 必然失败 → 中文路径目录（`archive/docs/复盘报告/` 等）被**静默跳过**，首轮施工的「残留复算 0」是假绿；改用 `-c core.quotePath=false` 取真实路径后复算才真实。② **残留复算口径**——只复算「自己改过的文件」会漏掉「根本没被改到的文件里的残留」；改为**全盘复算**（含未改动与未跟踪文件）后才发现 24 条 S4 投稿树本地线与构建产物（均未被 git 跟踪·不入公开仓·按 W812 验收口径豁免）。
> - **验收**：跟踪域内全仓该字面**命中 0**（含 archive/ 归档面·现役面·spec·索引载荷）；非跟踪域残留经逐条定性为本地线/构建产物/二进制（不入公开仓）；派生面同步重生成搜索索引（docs=726 pages_zh=96 pages_en=138·zh 256199 / en 276197·恰好 2 页变更）+ CSP 重算（2 页已更新·856 页 0 漂移）+ 第 46 槽 0 FAIL。

### W815（2026-10-20）：shell 查坑表补两条（PowerShell $ 变量展开 + 引号配对冲突）

> **来源**：用户在 W813/W814 施工后提供 PowerShell `$` 变量展开的处置方案（单引号包裹 / `--%` 停止解析符 / stdin 管道 / 反引号转义），本批据此把该类坑固化进仓内坑表。
> - **文件**：docs/agent/pitfalls.md、docs/00-导读/W批次编号对账表.md、scripts/output/_w815_spec.json。
> - **起因**：W813/W814 施工中两次内联 `py -3 -c "..."` 失败（一次 Python 侧报 `SyntaxError: unterminated string literal`、一次 PowerShell 侧报「字符串缺少终止符」），触发一次根因取证。
> - **pwsh 7.6.7 实证结论（对照实验·非凭记忆）**：① **双引号内 `$变量名` 会被展开成空**——实测 `py -3 -c "print('[$myvar]')"` 得 `[]`（Python 收到空串），改单引号得 `[$myvar]`（原样透传）；**`--%` 停止解析符**同效。② **孤立 `$` 不受影响**——`$` 后不跟合法变量名时 PowerShell 不展开，故正则行尾锚（`r'^ab$'` / `r'^W(\d+)$'`）在双引号内**实测正常**（`['123']`）；即「正则里有 `$`」本身不是坑。③ **两次真实失败的根因是引号配对而非 `$`**——逐片段拆解实测：外层双引号 + Python 侧单引号 → 引号配对被破坏而失败；同一段代码落文件执行 → 正常。④ 因此处置分两层：含 `$变量名` 用单引号或 `--%`；含引号（几乎所有真实逻辑）一律**落 Python 脚本文件再调用**（仓内 W706 场景分层铁律的既定正解）——**内联只适合无引号无 `$` 的极短表达式**。
> - **用户所给四方案的适用面核对**：`--%` 与单引号在「代码含双引号」时同样失败（引号配对问题依旧存在），故两者只解决「`$` 展开」这一类；stdin 管道（方案三）确实最彻底但改变了调用形态、且仓内已有「落脚本文件」这一等价且更简的路径；反引号转义可读性差故不采。
> - **附带订正**：W814 收官时漏了认领行状态回填（仍为「进行中」）→ preflight 判定 W814 为在途批次·W815 改同一共享文件被拒（交集拒绝机制按设计生效）·据对账表规则「本会话自己的行允许更新状态列」回填为已收官。
> - **验证**：坑表两行已落（`docs/agent/pitfalls.md` 第 16-17 行）+ 四组 pwsh 对照实验实测结论一致 + 交付全量门禁 51 段 0 FAIL。

### W816（2026-10-20）：门禁判据可信化批（审查第一批）

> **来源**：2026-10-20 对本仓库的全项目只读审查（先审 12 个未推送提交·后按用户指令扩到全项目文件内容）——三轮审查共产生 20+ 项发现，其中 3 项属「门禁判据自身不可信」（判据未执行却报绿）。本批处理其中**不触碰管控件与归档面**的子集；`scripts/verify_delivery.py`（管控件·须用户批准）与 `archive/**`（文档规范 §11.2 禁回溯修改）另起 W817 待授权。
> - **文件**：scripts/check_citations.py、scripts/security_scan.py、tests/unit/test_security_scan.py、docs/00-导读/W批次编号对账表.md、docs/11-方案报告/计划方案/执行前计划-T03-全项目审查第一批修复.md、docs/11-方案报告/计划方案/T03-任务计划执行与经验沉淀报告-2026-10-20.md、docs/11-方案报告/README.md、scripts/output/_w816_spec.json。
> - **缺陷①（引文门禁 cwd 依赖 + 零文件假绿）**：`check_citations.py` 自身已定义正确 `ROOT`（`os.path.dirname(os.path.dirname(os.path.abspath(__file__)))`），但 `--dir docs` 是相对路径且被直接交给 `os.walk` → 以**调用方 cwd** 为基准。实证：cwd=仓库根 → 「423 条规范引文 + 112 条归属对白 · 命中率 100%（744 个文件扫描）」exit 0；cwd=`%TEMP%` → **「共 0 条规范引文 + 0 条归属对白 · 命中率 100%（0 个文件扫描）」exit 0**——第 20 门禁被完全中性化并自报成功，违反铁则「不允许从未运行/从未通过的门禁存在」。**修**：新增 `resolve_scan_base()`（相对目录按脚本 ROOT 解析）与 `scan_files_guard()`（零文件守卫，目录不存在→exit 2「输入错误」/ 目录存在但扫到 0 篇→exit 1「判据未执行」，二者语义不同故不同码）；`--reverse` 面的基目录同步改为 ROOT 解析。**验证**：从 `%TEMP%` 调用 → **745 个文件扫描**（含本批新增报告文件）·命中率 100%·exit 0；空目录 → exit 1 并明示「判据未执行·不得判绿」；不存在目录 → exit 2；`--self-test` **12/12 → 15/15**（+3 判据面负样本：相对目录未按 ROOT 解析 / 零文件未判红 / 目录不存在未判输入错误）。
> - **缺陷②（安全扫描构建产物排除失效·本地红 CI 绿）**：`security_scan.py` 的 `_AGENT_WEB_BUILD_ARTIFACT_RE` 只匹配 `xiyouji-agent-web/server/**` 与 `server/engine/**`，而 `xiyouji-agent-web/tsconfig.node.json` 的实际 `"outDir": "./.tsbuild"` → 编译测试夹具被纳入扫描。实证：排除正则对 `.tsbuild/server/engine/tools.test.js` **匹配=False**；全量扫描报 **high=2**（`AGENT_WEB_TOKEN = "unit-test-token-should-not-leak"`、`SECRET = "w791-test-secret"`），而 `.tsbuild/` 已被 `.gitignore:124` 忽略 → CI 上不存在该目录 → **CI 恒绿、本机恒红**，正是 W757 当年为此专门加排除正则所要防的分裂，在 outDir 迁移后失效。**修**：通用排除段补 `.tsbuild`（覆盖任意嵌套深度）且同步正则加 `.tsbuild/.*` 分支。**验证**：全量 `--all`（1165 文件）→ **high 2 → 0**；新增单测 `test_discover_files_excludes_tsbuild_artifacts`（全量扫描面断言无 `.tsbuild` 段）与 `test_agent_web_build_artifact_regex_covers_tsbuild`（正则层直证·含旧形态回归锚）。
> - **缺陷③（XSS 规则对主流 sink 形态零覆盖）**：`XSS-001` 正则 `\.innerHTML\s*=` 既不匹配 `.innerHTML +=`，也**完全没有 d3 `.html(` 的规则**——而 site/ 内 `.html(` 有 **1328 行**、`.innerHTML +=` 有 **4 行**，此前对门禁**零信号**。**修**：新增 XSS-007（d3 `.html()` 动态实参）与 XSS-008（`.innerHTML +=`），并入 `XSS_DOWNGRADE_RULES`（site/ 沿用既有降级口径·非 site/ 仍 high）。XSS-007 判据只取**动态实参**（真 sink）：整参静态字面量与 d3 回调首参不算（前者无注入面·后者是 DOM 构造）——判据自检 **8/8 合成样本符合预期**（静态字面量/双引号字面量/拼接插值/模板插值/裸标识符实参/成员访问实参/回调首参/非 .html 形态）。**验证**：全量扫描 XSS-007 命中 **758**（真实动态 sink 数）·XSS-008 命中 **4**·XSS-001 仍命中 262（未破坏既有规则）；单测 `test_security_scan.py` **16 → 22 passed**（+6：XSS-007 命中 / XSS-008 命中 / XSS-001 回归锚 / site 降级口径 / 非 site 保持 high / tsbuild 排除）。
> - **附带订正（认领行状态回填）**：W813/W814/W815 三行「关联 commit」列仍写「待提交」而对应提交早已落地（4fb0f300 / 09b1b27e+fa1c2b4f / 4bc6dede），状态列仍为「进行中」→ `preflight_check.py` 判定三者皆为在途批次 → **实测 exit 1**（两条 touches 交集 FAIL），任何后续批次无法开工；现势 bullet 停在 W813 且未标已消费 → 与 max+1 不衔接。**修**：三行 commit 与状态列按 `git log --oneline` 实证回填为「已收官」，W813 bullet 标已消费并追加 W816 bullet。**验证**：`preflight_check.py --no-fetch --touches <本批清单>` → **exit 0**（修复前 1）·「现势 bullet 交叉核验：W816 与 max+1 一致」·「PREFLIGHT PASS——无风险项，可动工」。
> - **偏差记录**：执行中实测「XSS 新规则使 medium 计数由 264 升至 1026（+762）」，超出执行前计划 AC-06 设定的「medium 增量 ≤ 564」。原因：AC-06 的阈值系估算值，而收窄后的判据捕获的是**真实动态 sink 数**（XSS-007 命中 758 处），非噪声。影响：CI 的 security job 只拦 high（实测 high=0），阻断信号未变；`scripts/output/security-report.md` 为 gitignore 件（不入库·不进提交），报告体积不影响提交。处置：保留该规则与实测计数，AC-06 阈值按实测值订正（以执行前计划为基线不改写，偏差留档于本段与终稿报告）。
> - **验证**：引文门禁 --self-test 15/15 + 主检 745 文件命中率 100%；安全扫描 --all high=0 / medium=1026 / low=1（1165 文件·8.34 s）；`pytest tests/unit/test_security_scan.py` 22 passed；`ruff check scripts/` 0 违规；`check_doc_sync.py` 0 FAIL + `--self-test` 20/20；`verify_delivery.py` 全量 51 段 0 FAIL；`generate_csp.py --check` 856 页 0 漂移；preflight exit 0。
> - **状态**：已落地（本地提交 55b9b8c0·未推送）；终稿报告见 `docs/11-方案报告/计划方案/T03-任务计划执行与经验沉淀报告-2026-10-20.md`（执行记录 / 验收证据 / 偏差留档 / 经验沉淀）。

### W817（2026-10-20）：agent-web 工具层边界加固批（会话库黑名单 cwd 无关 + symlink 逃逸 + git --output 空格形态 + 遍历面过黑名单）

> **来源**：2026-10-20 全项目只读审查（服务端面）实证的五处同源缺陷——根因同一：**受保护路径判据假定 cwd 是仓库根**，而实际不是。
> - **文件**：xiyouji-agent-web/server/engine/tools.ts、xiyouji-agent-web/server/engine/tools.test.ts、docs/00-导读/W批次编号对账表.md、scripts/output/_w817_spec.json。
> - **根因（先说清，否则后面的修法看不懂）**：工具集根 = **请求 cwd**（`server/chat.ts:134` `workingDir = resolveWorkingDir(cwd, PROJECT_CWD)` → `:219` `createToolset(workingDir)`），而 `guardPath` 的 `relPosix = toRelPosix(root, target)` 是**相对 cwd** 计算；受保护路径黑名单却按**仓库根相对**书写（`^xiyouji-agent-web/data/`、`^scripts/(verify_delivery|bump_version|batch_cascade)\.py$`）。二者错位 ⇒ 换 cwd 即失配。`resolveWorkingDir` 允许 PROJECT_CWD 内**任意子目录**（前端 `NewChatDialog` 的 cwd 是用户可输入的自由文本框），故这不是理论路径。
> - **缺陷①（会话库可读，C1）**：`DENY_READ` 的会话库规则为 `^xiyouji-agent-web/data/`（仓库根锚定）→ cwd=`xiyouji-agent-web` 时 `relPosix` 形如 `data/chat.db` → **失配放行**。该库实存 184 KB + wal 226 KB + shm 33 KB，存全部会话正文与**工具结果原文**（`chat.ts:262-273` 写入 `tool_calls`）——正是该黑名单注释声明要防的「二次外泄」。**修**：会话库三件套改 cwd 无关形态 `/(^|\/)data\/chat\.db(-wal|-shm)?$/i`，并把仓库根相对那条去掉 `^` 锚。**验**：cwd=子目录下 `data/chat.db` 与 `data/chat.db-wal|-shm` 全部被拒且不泄内容。
> - **缺陷②（symlink/junction 逃逸未被拦，C2）**：`guardPath` 的 `mustExist` 分支只写 `fs.realpathSync(target);` 而**丢弃返回值**，其注释声称的「symlink 指向仓外则解析后判越界」**在代码里并不存在**；`mustExist=false`（写面）只从 `path.dirname(target)` 起做祖先 realpath，**从不解析 target 本身** ⇒ 指向仓外的**文件级**链接可被读出/写穿。**修**：`mustExist` 分支改为取 realpath → 判「在 root 之下」→ **返回解析后的绝对路径**（后续读写跟随它·不再二次跟随链接）；写面补「target 已存在时先解析后判定」。**验**：指向仓外的目录链接（Windows junction·POSIX symlink）读出被拒且不泄内容；仓外文件内容哈希不变。
> - **缺陷③（git 输出重定向空格形态，C3）**：`GIT_DANGER` 只认 `--output=` 带等号形态，而 `git log --output <file>` 是**独立取值**形态 → 放行。实证：TEMP 隔离仓库内 `git diff --output <file>` 与 `git log --output <file>` 均 **exit 0 且文件已生成**（越出工作目录边界）。**修**：`--output` 按整 token 拦截。**附带订正**：短形式 `-o` 经实测是 `--only`（限提交·报 "invalid object name"）**不是**输出重定向，故不拦（避免误伤）。**验**：空格形态被拒且目标文件零落盘；等号形态仍被拒；`git status` 仍放行。
> - **缺陷④（门禁脚本写面可绕，C4）**：门禁脚本规则 `^scripts/(...)\.py$` 同为仓库根锚定 → cwd=`scripts` 时 `relPosix` 形如 `verify_delivery.py`（无 `scripts/` 段）→ 失配 ⇒ 铁律 8 门禁脚本可被改写。**修**：改基名形态 `/(^|\/)(verify_delivery|bump_version|batch_cascade)\.py$/`。**分层口径保持**（W680）：门禁脚本只在**写面**受保护，读面按设计放行（脚本本身是公开件）。**验**：cwd=scripts 下写 `verify_delivery.py` / `bump_version.py` 均被拒且 sha256 未变。
> - **缺陷⑤（遍历类工具完全不过黑名单，C5）**：`glob` 与 `grep` 从不调用 `checkProtected`（`walkFiles` 只按名跳过 `.env`）⇒ 会话库内容**可经 grep 外泄**，路径可经 glob 泄露——恰是该黑名单的设立目的。**修**：`walkFiles` 内按 read 面过滤受保护路径（新增不抛异常的 `isProtected()` 判定）。**验**：grep 搜会话库特征串零命中、glob 零列出；普通文件仍可 grep（未误伤）。
> - **负样本自证（关键·本仓纪律「负样本必红」）**：把 `tools.ts` 的源码修复单独 stash（保留测试）后实跑 → **C1/C1b/C2/C3/C4/C5 六条逐条变红**（C3 更实锤：命令真被执行，git 报 exit 128）；控制组 C3b/C3c/C5b 保持绿（证明未误伤既有行为）；C2b 因本机 Windows 无文件级建链权限而以 `t.skip()` **诚实标注跳过**（CI 的 Linux 必执行·禁静默通过）。
> - **验证**：`npm run test:server` → **76 pass / 1 skip / 0 fail**（原 67 → +9）；`api.integration.test.ts` → **19 pass / 1 skip / 0 fail**；`tsc --noEmit` → **0 错**；verify_delivery 全量 51 段 0 FAIL；ruff 0 违规。
> - **状态**：已落地（本地提交 b1d125fc·未推送）。

### W818（2026-10-20）：静态站前端框架化选型评估批

> **来源**：用户令「技术选型对比：候选方案的定位与生态、核心能力覆盖度、性能与成本、上手成本与踩坑记录、长期维护活跃度都对齐，最后给一个推荐结论」，并经四项确认（问题域=静态站与可视化页是否值得前端框架化或换渲染方案 / 候选由本批给出并排序 / 硬约束=Windows 本机可跑且零额外付费仅宽松许可 / 交付形态=落仓正式文档并同步治理面与跑门禁）。
> - **文件**：docs/11-方案报告/静态站前端框架化选型对比-2026-10-20.md、docs/11-方案报告/README.md、docs/00-导读/W批次编号对账表.md、STRUCTURE.md、scripts/_w818_inventory.py、scripts/_w818_file_protocol_probe.py、scripts/index.md、scripts/output/_w818_spec.json。
> - **取证①（现状盘点·`scripts/_w818_inventory.py` 实跑）**：site 全站 857 页（site/data 88 + site/en 138 + site/reader 622 + 根 9）总体积 49,334,618 B（47.05 MB）；site/data 88 页合计 9,272,531 B（9.27 MB）·均值 110,483 B（107.9 KB）·中位 103,109 B（100.7 KB）·最大 373,002 B（relationships.html）；内联 <style> 块 358（88/88 页）·内联 <script> 块 183（88/88 页）·外链 script 623·CSP meta 88 页全覆盖·**type=module 脚本 0 页**（现役资产天然适配 file://）·on* 内联事件属性 7 处/3 页；EMBEDDED 标记 88/88 页·fetch 调用 59/88 页（59 页为「fetch + 回退」双态）；本地化资产 text-search-app.js 2,177,796 B + three.r128.min.js 603,445 B + d3.v7.min.js 279,706 B；**site/reader 622 页（10,718,220 B）为 scripts/build_reader.py 生成物** ⇒ 迁移面从「857 页手改」收缩为「87 手写可视化页 + 138 EN 页 + 9 根页 + 2 个生成器」。
> - **取证②（file:// 三判据·`scripts/_w818_file_protocol_probe.py` 实测）**——Chromium + Playwright 1.63.0：判据 A `<script type="module" src>` 被 CORS 拦截（`origin 'null'`·`net::ERR_FAILED`·脚本零执行）·判据 B classic `<script src>` 正常执行 ·判据 C `fetch('./x.json')` 报 `URL scheme "file" is not supported` ⇒ 59 页双态回退是必需设计而非冗余。
> - **取证③（构建链产物对照·Vite 8.3.4 + Node v24.14.0 本机实跑）**：P1 默认 ESM 构建（index.html 238 B + assets/index-*.js 728 B）→ file:// 直开**失败**（CORS 拦截·DOM 停在 pending）·P2 加 vite-plugin-singlefile 全量内联（933 B 单文件）→ **通过** ·P3 React 19.3.1 + singlefile（219,875 B = 214.7 KB 空页）→ **通过**；对照现役单页均值 107.9 KB ⇒ React 路线单页体积 ×1.99 起，87 页逐页内联则全站 +18.25 MB。三个实测坑：默认 ESM 产物违 file:// 铁律 · singlefile 内联后仍保留 `type="module"` 属性（不可凭「已内联」判定可用）· 构建入口与 config 绑定错（rc=0 不等于产物合契约）。
> - **取证④（生态一手数据·npm registry + GitHub API 当刻实取）**：vite 8.3.4（MIT·近周 119,005,168 下载·83,415 stars·push 2026-10-20）·react 19.3.1（MIT·116,163,376·251,450 stars）·astro 7.4.1（MIT·4,784,961·63,337 stars）·lit 3.3.3（BSD-3-Clause·3,965,350·末次发版 2026-05-14 为四候选最慢）·vite-plugin-singlefile 2.3.4（MIT·1,199,696）·typescript 7.0.2（Apache-2.0）—— 许可全属宽松许可且上游均活跃 ⇒ **两条用户硬约束对五候选全部放行**，不构成淘汰理由。
> - **结论（加权 30/25/20/15/10·能力覆盖度/上手成本/维护活跃度/性能成本/定位生态）**：**A 维持现役原生管线 4.50 > B 局部构建化 4.30 > E Lit 3 2.70 > C React 19 全面框架化 2.65 > D Astro 7 islands 2.45**。推荐路线三档：档 0 维持现役并把「file:// 直开 + 体积上限 + 第 43 槽真渲染」固化为新建页准入检查 ·档 1 **新建页可走 Vite 8 + TypeScript 7 + singlefile（存量 87 页不迁）** ·档 2 若档 1 连续 3 个新页验证有效再评估迁移 build_reader.py 生成器（生成物·迁移面最小）。明确不做：87 页可视化页迁 UI 框架 ·全站迁静态生成器 ·在 site/ 引入 type=module 脚本 ·以外链共享 JS 换体积。
> - **处理声明（隐性强约束）**：用户未把「file:// + 零外域依赖」列入硬约束选项，但该条是 AGENTS.md §6-5 第 5 条仓内铁律，本批按一票否决处理并在报告 §2.2 显式声明；另按用户「上手成本与长期维护活跃度优先于性能」的口径自设权重 30/25/20/15/10（报告 §1.2 与 §5.6 逐项列出依据，可由用户改权重重算）。
> - **范围纪律**：本批为只读评估 + 新增 1 份报告 + 2 个一次性取证脚本（`scripts/_*.py`·按 AGENTS §2 不入 CI 门禁）+ 治理面计数订正；**未改 site/ 任何页面、未改 xiyouji-agent-web/ 代码、未改管控脚本（verify_delivery.py 等按文档规范 §11.2 禁擅改）、未改 archive/** 面。
> - **验证**：两份取证脚本实跑复现报告全部计数（inventory 退出 0）·file:// 探针三判据与预期一致（退出 0）·`py -3 scripts/verify_delivery.py` 全量 51 段 0 FAIL ·`py -3 scripts/generate_csp.py --check` 0 漂移 ·`py -3 scripts/check_doc_sync.py` 0 FAIL ·`py -3 scripts/stats.py --check` 零差异 ·pytest 全量通过。
> - **状态**：已落地（本地提交 088e1bf2·未推送）；终稿报告见 `docs/11-方案报告/静态站前端框架化选型对比-2026-10-20.md`（六节正文 + 五维对齐表 + 加权排序 + 推荐路线三档 + 明确不做清单 + 复算附录）。

### W819（2026-10-20）：界面视觉重设计方向批（v4 刻本秩序 · 五轴决策 + 零外域视觉预览）

> **来源**：用户令「帮我给界面出一版重设计：视觉层级、配色与字体体系、间距栅格、组件样式统一都要升级，保留原有功能结构不乱动，先出设计方向再细化」。
> - **文件**：docs/11-方案报告/界面视觉重设计方向-v4-2026-10-20.md、docs/11-方案报告/v4-design-language-preview.html、docs/11-方案报告/README.md、docs/00-导读/W批次编号对账表.md、scripts/_w819_design_audit.py、scripts/output/_w819_design_audit.json、site/data/search.html、site/en/search.html、scripts/index.md、scripts/output/index.md。
> - **取证①（分层盘点·`scripts/_w819_design_audit.py` 实跑·2026-10-20）**：857 页按「公共层 / 页面层」分层——公共层 INLINED CSS 覆盖 **330 页 · 15,425,481 B**（单页最大 47,808 B · 裸 hex **72,934** 个）；页面层 3,264,180 B。
> - **取证②（页面层自建同名核心组件·页数）**：`.kpi-card` **119** · `.chart-block` **98** · `.insight-box` **79**（DESIGN.md §4.8 有规范而 system.css 实现 **0** 处）· `.hero` **58** · `.section` **35** · `.table-wrap` **25** · `.empty-state` **25** · `.badge` 6 · `.btn` 6 · `.chart-tooltip` 5（违 §5.4「禁页面私有 tooltip 盒」契约）。
> - **取证③（间距无刻度）**：`site/tokens.css` 的 `--space*` 令牌命中 **0**；页面层间距字面量 Top25 合计 20,201 处，其中刻度外值六类（9/34/26/22/5/30px）合计 **2,760** 处；容器宽度四档并存（760/1200/1320/1536）。
> - **取证④（同名组件两套异形）**：`site/dashboard.html` 自建 `.kpi-card`/`.filter-tab`/`.search-box`/`.category-badge` 与 system.css 并存（padding 22/20px · 数字 34/32px · 朱砂/墨色）。
> - **方向决策（五轴）**：A 视觉层级＝页级五段式（eyebrow→title→lead→meta→action）+ 区块三段式 + 层级三杠杆（留白 96/32/16/8 · 墨色深浅 · 朱砂实底每页 ≤3 处）；B 配色＝四族角色（纸/墨/彩/夜）+ 三档色阶统一 color-mix + 图表色板双组驱动暗色（替代约 200 条 hex 补丁表）+ 对比度硬指标；C 字体＝宋/黑/等宽三族分工保留 + 九个排版角色 + CJK 行高 1.80 + 字重预算（黑体只 400/500）；D 间距栅格＝4px 基准十三级 + 语义别名 + 容器三档（760/1120/1320）+ 12 栏栅格；E 组件统一＝24 组件清单 + 五态规格卡 + dashboard 第二套回收 + 补齐缺实现组件 + 新增第 47 槽门禁「页面层禁覆盖核心组件」。另附六阶段落地路线与五个待用户裁决项（对比度基线 / 朱砂实底限额 / 容器档位 / 夜读模式地位 / 迁移节奏）。
> - **视觉预览**：`docs/11-方案报告/v4-design-language-preview.html`（45,691 B · 零外域依赖 · file:// 双击直开 · 浅色/暗色双主题 · 现状 vs 提案逐项对照 · 含整页骨架样张）。
> - **范围纪律**：本批**只出方向**——`site/` 857 页**视觉 0 改动**（仅搜索索引 2 页机械刷新，派生面无设计变更）· `DESIGN.md` 宪法 0 改动 · `tokens.css`/`system.css` 0 改动 · DOM 类名与功能结构 0 改动（用户硬约束「保留原有功能结构不乱动」）。
> - **验证**：盘点脚本实跑复现全部计数（`py -3 scripts/_w819_design_audit.py` 退出 0 · JSON 落 `scripts/output/_w819_design_audit.json`）· 预览页自检全过（CSS 括号/引号平衡 · 0 外域引用 · 本地字体文件存在 · 6 个锚点与文档链接可解析）· 第 46 门禁搜索索引 0 FAIL（zh 827 · en 869）· `generate_csp.py --check` 856 页 0 漂移 · 第 31 门禁 0 FAIL。
> - **状态**：已落地（本地提交·未推送）；方向文档见 `docs/11-方案报告/界面视觉重设计方向-v4-2026-10-20.md`（五轴决策 + 六阶段路线 + 五个待裁决项 + 复算附录）；**待用户裁决后进入细化阶段**（令牌 v4 纯加法 → 组件层 v4 → 逐页迁移 → reader 一次改造 → 门禁固化）。

### W820（2026-10-20）：干扰治理日志补登与机制自身缺陷修复批

> **来源**：用户问「项目内多 Agent 并行是怎么处理的？」→「为什么从来没有更新记录呢？」→ 查明 §8 干扰日志表最后一行停在 2026-10-16，而 10-17~10-20 四天 128 个提交零登记；用户令「按顺序做」（三步：补登 / 加机器触发点 / 改判定口径），本批为第一步与第三步（第二步涉管控脚本另立批）。
> - **文件**：docs/superpowers/plans/2026-10-14-interference-governance-roadmap.md、docs/00-导读/W批次编号对账表.md、scripts/output/_w820_spec.json。
> - **断档事实（取证·非凭记忆）**：§8 表原 4 行全在 10-14~10-16，末行 10-16 20:42（e4ff4faf）；此后 10-17/18/19/20 各 21/31/26/28 提交共 **128 个**，零登记。而 W741（5ed27784）自定的**强制录入触发**明列三种情形——① 开工 `git status` 发现非本会话变更 ② `safe_commit` 触发重试 ③ preflight 交集拒绝触发——**该期间至少发生两次**：W812 撞号让号（14eeabcd 提交信息含「让号/撞号/preflight/交集/并行会话」五词）与 W815 被 preflight 交集拒绝（4bc6dede 载「W814 收官漏认领行状态回填 → 致 W815 被 preflight 交集拒绝（机制按设计生效）·已回填」）。
> - **补登 4 行（每行带可核验证据·如实标注延迟登记）**：G1-B 撞号让号（W812·commit 14eeabcd）/ G1-C 机制自身缺陷致交集拒绝（W815·commit 4bc6dede）/ G1-A 开工观测漂移（W820 开工见 36 条变更·30 件已暂存全为 W818 产物·preflight 输出实证）/ G1-D 机制自身缺陷（认领行列数错位·下述）。**延迟登记本身是该机制的第一个真实样本**——它暴露的正是「无机器触发点则必然掉档」这一结构问题。
> - **判定口径加严（治「不完整被误读为低发」）**：§2 原写「空表本身也是有效结论（两周零事件 = 共享面事件低于阈值 → P1 缓建坐实）」——该结论**只在登记完整的前提下成立**。现补：**表不完整（应有登记行而缺失）同样不是有效结论**，10-28 复盘时须先验**登记完整性**（对照 §2 强制触发三项逐条回查该窗口提交与门禁输出），完整性不达标时判为**度量失败**并重记，**不得据残表做 P1 触发决策**。实证依据：按残表计算会把 10-17~10-20 的高发期误判为低发期并错误坐实 P1 缓建（实际发生 ≥2 次强制触发）。
> - **机制自身缺陷登记（G1-D·本批自查发现）**：**W819 认领行有 8 个单元格（标准 7 格）**——状态列位置多写了一个「W819」字段，致后三格整体右移：状态列='W819'·认领会话列='**进行中**'·touches 列='主会话 2026-10-20'·**真实 touches 落到第 8 格**（`preflight_check.py` 的 `parse_ledger` 读 `cells[6]` 读不到）→ **该批声明的共享面完全不在交集判定内**（别的批次改 docs/11-方案报告/ 等面不会被拦）；在途判定侥幸成立仅因「W819」不以「已收官」开头（`is_inflight` 判 True）——**属偶然而非设计**。按对账表规则「不改他方行」，本批**不擅改 W819 行**，仅登记发现、留待其收官时由该批自修。
> - **本批自身的机制遵循**：认领行按表头规则④「对账表追加认领行属 append 安全操作·不列」——初次认领时误列了对账表致 preflight 判与在途 W818 冲突（exit 1），据规范订正 touches 后放行；动工前 `preflight_check.py --touches <路线图> --self W820` 复跑 PASS（与在途 W818/W819 无交集）；提交用显式 pathspec，**不碰对方在途件**（工作树 36 条变更中 30 件为 W818 产物·本批全程规避）。
> - **验证**：§8 事件行 4→**8 行**（补登 4 行）+ §2 口径加严段已落 + 交付全量门禁 51 段 0 FAIL。

### W821（2026-10-20）：系统架构方案批（分层模块数据流存储扩展容灾部署监控八维成文）

> **来源**：用户令「帮我设计一套系统架构方案：整体分层、模块拆分与依赖、数据流与存储选型、扩展性与容灾、部署与监控都写到位，附几张架构图说明图」，并经四项确认（业务场景与规模 = 基于当前仓库 xiyouji 文档真源到静态站点到可视化到 Web Agent 问答加桌面端、DAU 百级、内容千级、单机可承载 / 技术栈 = 沿用现有栈 / 硬约束 = 极低成本且无云厂商绑定加合规审计可回滚可溯源 / 交付形态 = Markdown 方案文档加 Mermaid 架构图落 docs/11-方案报告/）。
> - **文件**：docs/11-方案报告/系统架构方案-分层模块与部署-2026-10-20.md、docs/11-方案报告/README.md、docs/00-导读/W批次编号对账表.md、scripts/output/_w821_spec.json。
> - **现状盘点（2026-10-20 实测·可复算）**：全站 857<!--stats:html_total--> 页（site/data 88<!--stats:site_data_html--> + site/en 138<!--stats:site_en_html--> + site/reader 622<!--stats:site_reader_html--> + 根 9<!--stats:site_root_html-->）·可视化页 87<!--stats:visualization_pages--> 页·CSP 覆盖 856<!--stats:csp_covered--> 页·A1-A6 内容 615<!--stats:a1_a6_docs--> 篇·A4 209<!--stats:a4_docs--> 篇·分析器 34<!--stats:script_classes--> 类·交付门禁 46<!--stats:gate_count--> 槽；结构面：docs 全树 1,210 md、scripts 348 py 加 1,370 js、tests 38 py、workflows 9 个 yml、dataset 45 json、source 215 md、site 16 js 加 2 css；`site/**/*.html` 实测 857 与 stats.json 的 html_total 857 两条独立路径同值互证。
> - **架构裁定（五条·本批结论）**：① **依赖单向向下**——L0 事实源到 L1 加工到 L2 交付到 L3 服务到 L4 消费，**产物不得反向成为事实源**（docs 只能引 source，不得引 site 或 dataset 的派生值）；② **存储沿用 Git 文件树加 JSON 加单文件 SQLite 三件套**，不引入外部数据库、缓存、对象存储、搜索引擎与向量库（当前 DAU 百级，引入即需常驻服务，与极低成本且无云厂商绑定冲突）；③ **扩展走三档触发式演进**（每档带 DAU、页体积、语料量、门禁时长四项量化开关，未触发不写代码）；④ **容灾主战场是降级可用**（静态站与文档本就可离线，问答降级为只检索，产物漂移靠门禁前置拦截与回退）；⑤ **监控即门禁**（零付费前提下把可观测性做进 46 槽门禁与 CI 5 个 job）。
> - **分层与依赖**：L0 事实源（source 215 md、docs 1,210 md、dataset 45 json）→ L1 加工（34 类分析器 + 3 类生成器 + 46 槽门禁）→ L2 交付（857 页静态站，零服务端）→ L3 服务（Express 5 + React 19 + SQLite WAL 三表 + 工具集 + 权限审计 + Electron 桌面壳 + MCP 只读工具）→ L4 消费（Pages 访客、file:// 读者、桌面用户、MCP 客户端），治理面（W 批次号 + 四件套 + 46 槽门禁）横切贯穿；**六条层间铁律**（含「治理面只读事实不用产物反推内容正确性」「服务层不得直接触达交付层」）；**17 个模块的依赖矩阵**（矩阵上三角为空即编码方向性）；**六条禁止依赖形态**（各附实证教训：产物回写事实源、手改 EMBEDDED、门禁自建即自曝、cwd 锚定可绕、CI 依赖本地产物、服务层解析站点 HTML）。
> - **数据流与存储**：三条主链路加一条治理链路（内容生产流为确定性可重跑，故产物可随时丢弃重建；交付发布流为 push 到 CI 到 Pages 与 tag 到 Release 三平台安装包；问答交互流为 SSE 到引擎到受限工具面到 SQLite；治理审计流为取号到认领到级联到门禁到提交到回填）。**8 个存储候选逐项裁定**（Git 文件树、JSON 数据集、SQLite 采纳；对象存储、Postgres、Redis、搜索引擎、向量库不采纳且各写明升级触发条件：DAU 大于 5,000 或并发写会话大于 50 引入 Postgres、语料大于 5,000 篇评估向量召回、语料大于 20,000 篇评估独立检索）。
> - **扩展性与容灾**：容量模型 6 维瓶颈预测（首个瓶颈为构建与 CI 时长而非服务端）；三档路线（档 0 维持现役 / 档 1 局部构建化仅新页 / 档 2 服务化 / 档 3 规模化）；**8 条容量阈值**（单页大于 200 KB、内联 CSS 大于 60 KB、全站大于 120 MB、搜索脚本大于 3 MB、门禁全量大于 600 s、仓库大于 1 GB、单批文件数大于 500）；**8 个故障域 F1 至 F8 的降级矩阵**（每行含用户可见表现、降级路径、RTO、RPO、恢复动作、演练方式六列）；备份原则「只有不可重建的东西才需要备份」→ 全仓仅两件不可重建（内容真源已有 Git、会话库缺备份，待裁决项 Q1）。
> - **部署与监控**：四条交付通道（Pages 公网、file:// 本地、Electron 桌面三平台安装包与自动更新、Web Agent 自建回环）+ 无云厂商绑定可验证口径 6 维（真正绑定点只有托管方与 LLM 供应商两处）；**四层观测面**（代码层、交付层、运行层、业务层）+ **14 条指标与阈值表**（新增口径 OBS-10 至 OBS-14 五条中三条先作告警级，连续 10 批稳定后再升硬门槛）+ **6 条 SLO**（站点可用性大于等于 99.5%、首屏 LCP 小于 1.5 s、问答首 token 小于 2 s 等）+ 零付费告警路径 + 6 条巡检清单。
> - **架构图**：5 张 Mermaid 图分别对应整体分层图（图 1）、模块依赖图（图 2）、数据流图（图 3）、容灾降级图（图 4）、部署拓扑图（图 5）；**验收标准 10 条**（AC-01 至 AC-10，每条含检查方式与期望输出）；**复算命令 11 条**（A-01 至 A-11，逐条给出命令与期望输出）。
> - **处理声明**：用户未把 file:// 直开与零外域依赖列入本次四项确认的勾选范围，但该项属 AGENTS.md 第 6 节第 5 条仓内铁律，本批按一票否决处理并在报告第二章显式声明；性能硬指标（首屏小于 1.5 s、可视化 60 fps、问答首 token 小于 2 s）由本批默认写入 SLO 并标注为本次新增口径。
> - **范围纪律**：只读盘点加新增报告与一份级联 spec，不改 site/ 页面、不改 xiyouji-agent-web/ 代码、不改管控脚本（verify_delivery.py 等按文档规范 11.2 禁擅改）、不改 archive/ 面。
> - **验证**：链接校验 19,728 链接 0 broken（含本报告新增链接）；第 31 门禁文档口径体检 0 FAIL；第 45 门禁目录文档新鲜度 0 FAIL；交付门禁全量 0 FAIL；Mermaid 图 5 处与 AC-01 期望一致；禁用措辞扫描 0 命中。
> - **状态**：已落地（本地提交 37287c80·未推送）；终稿报告见 `docs/11-方案报告/系统架构方案-分层模块与部署-2026-10-20.md`（十四章正文 + 五张 Mermaid 架构图 + 十条验收标准 + 十一条复算命令）。
### W822（2026-10-20）：§8 干扰日志机器触发点批

> **来源**：用户问「项目内多 Agent 并行是怎么处理的？」→「为什么从来没有更新记录呢？」→ 查明 §8 干扰日志断档 4 天 128 提交零登记；用户令「按顺序做」（三步：补登 / 加机器触发点 / 改判定口径）——本批为第二步（第一步 W820·第三步亦在 W820 落），管控脚本改动经用户明确批准。
> - **文件**：scripts/preflight_check.py、scripts/safe_commit.py、tests/unit/test_preflight_check.py、docs/agent/pitfalls.md、docs/10-方法论沉淀/多Agent干扰治理与touches纪律.md、docs/superpowers/plans/2026-10-14-interference-governance-roadmap.md、docs/00-导读/W批次编号对账表.md、scripts/output/_w822_spec.json、scripts/output/_cascade_files_W822.txt、docs/INDEX.md。
> - **根因（非「条款不硬」而是「无机器防线」）**：W741 立的录入触发条款明列三种强制情形且注「保证日志不空表」——但查遍 `scripts/` 与 `tests/`，**零活代码引用该日志**，纯靠会话自己记得去开文件、想起来该写一行。对照本仓最成熟的「级联清单逐面 add」纪律（有 C4-e 门禁强制 + safe_commit 兜底 + 自测用例）所以那条从没断过——**机制有没有机器防线，决定它会不会掉档**。
> - **落地（只加提示行·不改任何判定与退出码）**：② `scripts/safe_commit.py` ref-lock 竞争重试路径（`if retry:`）输出提示；③ `scripts/preflight_check.py` touches 交集拒绝（`if bad:`）输出提示。提示文案含日志载体路径（`docs/superpowers/plans/2026-10-14-interference-governance-roadmap.md` §8）与登记窗口（2026-10-14 → 10-28）+ 命中原因，供被提醒者直接照字段补登。
> - **原拟第三触发点按用户裁决删除（如实记账）**：「开工发现非本会话变更」在 preflight 内**无法可靠区分**本会话与他方变更——工作树里的已暂存件可能来自并行会话（本会话开工时它是干净的），按「staged>0 即提示」会在正常态误报（端到端实证已复现：正常态也打出提示），变成用户明确不要的常态提醒、反降注意力。**代价登记**：该情形仍无机械提醒，兜底仍是「动工前 `git status` 识别并行增量」这条人工纪律。
> - **用户裁决留痕**：两轮询问均按用户选择落地——① 「只在真正触发时才提示·不输出常态提醒」；② 「删掉触发①·只保留②③（零假阳性）」。
> - **端到端实证（三问·不靠单元测试自证）**：Q1 真触发（与在途 W818 批次 touches 交集非空）→ **提示出现**且 exit=1；Q2 正常态（声明不交集的面）→ **无提示**且 exit=0；Q3 退出码不变（真触发仍 1 / 正常态仍 0）——**判定与退出码逐字未变**。
> - **单测**：tests/unit/test_preflight_check.py 12→**15 项全过**（新增 3 例：提示含载体路径与窗口 / 调用点必须处于条件分支内（按缩进块向上找 if·禁常态输出）/ safe_commit 同款守卫）；`safe_commit.py --self-test` 4/4 仍通过。
> - **载体同步**：方法论《多Agent干扰治理与touches纪律》新增「§四之二·机器触发点」节（治「靠自觉必然掉档」+ 触发点表 + 代价登记 + 判定口径加严指针）+「号段纪律」段（号段占用的三个占用面 + 级联链位规则 + 先落地者保留）；坑表 shell 场景表新增两行（「靠自觉的机制」禁只写条款不加机器触发点 + 提醒只在真触发时出／「判某批次号是否被占用」须三个占用面同看）；§8 干扰日志补登 G1-E 行（号段占用面漏判·当场登记）。
> - **号段链与一次「误归属」事故（如实登记·经对方复算订正）**：本批原编 W824·因「级联要求 CHANGELOG 顶段+1」与三方并发抢号形成死结·一度把 **W822** 判为「口头预留未落地的虚位号」并改名占用 `scripts/output/_w822_spec.json` 同名路径 → 我方**据以反推的三个 `_w822_*.py` 脚本实为他批（界面视觉重设计细化批·容器三档底数 / WCAG 对比度实算 / 迁移批次对拍）的产物**，我方误当成了「对方本批产物」→ 得出「对方 spec 被覆盖·需重建」的**错误结论**并向对方报障。**对方复算订正（我方已复核·订正成立）**：① 对方 spec 于 18:39:10 已迁至 `_w823_spec.json`·18:45:18 写入 `_w824_spec.json`——我方写入 `_w822_spec.json` 时刻该路径**无对方内容可覆盖**；② 对方本批唯一脚本 `_w823_db_schema_probe.py`（23,246 B·四子命令）与报告（30,912 B）与 spec 全部完好；③ git 历史中 `_w822_spec.json` 路径仅我方一条提交。**故该次「覆盖」不构成对对方内容的破坏**，我方原报障属误判。**真正的教训（可复用的判据修正）**：文件归属须看**内容与批次主题的语义对应**，**不看文件名前缀**——同号域内 `_w822_*` 前缀可能属第三批（W818 收官会话与我方均曾误判）。次要教训：**号段占用面不止「台账认领行 + spec 文件」**，还有工具脚本与产物前缀（但前缀只作「号被使用」的信号·不作物主判据）。该事件已登记进 §8 干扰日志（G1-E·号段占用面漏判）——**这正是该机制该记的事件类型**。

> - **与他方同文件并行施工的处置**：对方同期在 `preflight_check.py` 加了「状态列/touches 列按内容定位」的解析层加固（针对 8 格错位）·双方改动一度混在同一文件的索引里。已用行区间精确分离——我方版本只含 W821 提示（对方的 `_locate_status` / `_locate_touches` / `_TOUCHES_PLACEHOLDERS` 已剥离）·对方版本另存 TEMP 备份供其取用·**不越权代提交他方改动**；`test_preflight_check.py` 同法剥离对方的 4 个 W822 用例（故单测数为 15 而非剥离前的 19）。
> - **验证**：preflight 单测 15 passed + safe_commit 自测 4/4 + 端到端实证 Q1/Q2/Q3 全绿 + 交付全量门禁 51 段 0 FAIL。

### W823（2026-10-20）：数据库表设计审查报告落档批（agent-web SQLite 存储层·13 项发现·修复未动工）

> **来源**：用户令「审一遍数据库表设计：字段类型与约束、索引与查询模式、范式与冗余取舍、扩展性与历史数据处理都看看，按影响程度给改进建议」+ 本会话实读磁盘 + 真实库副本实跑取证。
> - **文件**：docs/11-方案报告/数据库表设计审查报告-2026-10-20.md、scripts/_w823_db_schema_probe.py、scripts/output/_w823_spec.json、docs/11-方案报告/README.md、docs/00-导读/W批次编号对账表.md。
> - **总判定**：表结构本身无「设计错了」的问题——三张表的划分、范式选择、字段类型选择基本是对的。风险集中在三处「声明了但没生效」的约束：外键强制从未启用（`ON DELETE CASCADE` 自建库至今一次未执行）、`feedback` 唯一索引维度选错（允许同一消息同时 up 与 down）、迁移机制不存在。三者叠加放大出一条可复现的数据串档路径：旧会话正文泄漏进新建的同名会话。
> - **P0 四项**（库副本实跑复现）：① `PRAGMA foreign_keys = 0`，删会话后消息 before=2 / after=2，级联未触发，且父会话不存在的消息写入被接受；② `clearAllData()` 不清 `feedback`，清库后 sessions=0 / messages=0 / feedback=1，悬空反馈行 = 1；③ 唯一索引为 `(message_id, verdict)`，同一 `message_id` 并存 up 与 down 两行；④ 客户端可控主键（`chat.ts:159`）叠加孤儿行，重建同 id 后 `getMessagesBySession` 返回旧会话正文。
> - **P1 三项**：会话列表 N+1 且全量物化 `content` 与 `tool_calls`（65 会话 → 66 次查询 / 物化 129 行；合成 2000 会话 103.8 ms 对 GROUP BY 2.1 ms）；会话列表无 LIMIT 无分页（5 万会话无索引无 LIMIT 81.63 ms，有索引加 LIMIT 50 为 0.06 ms）；缺 4 个关键索引，三条现役查询计划各含一处临时 B 树排序。
> - **P2 三项**：`created_at` 无格式约束，窗口边界 `2026-09-20T18:00:00.000Z` 下非 ISO 写法被误排除；JSON 存 TEXT 无 `json_valid` 约束且消费端裸 `JSON.parse`（一行脏数据致整会话 500）；长度与枚举约束只在 Zod 层，DDL 层零防线。
> - **P3 四项**：无迁移框架（`PRAGMA user_version = 0`，手写 ALTER 的异常被吞）；`CREATE TABLE IF NOT EXISTS` 对已有库永远无效（改表定义对旧库零效果）；JSON 列无 schema 版本；缺软删除与归档。
> - **正面结论（同样经实测）**：现役数据零违规——129 条消息时间戳 100% 为严格 ISO-8601 Z 格式，58 条 `tool_calls` 100% 为合法 JSON 数组，会话内时间戳并列 = 0，`integrity_check = ok`，`freelist_count = 0`，孤儿行三项均为 0。即缺陷全部是「机制缺失」而非「数据已脏」，现役库此刻无需数据修复。
> - **撞号让号（本批自身·两次让号）**：① 本批初编 W820，取证脚本落于 18:15:21，但**编号认领登记晚于**「干扰治理日志补登批」的 W820 认领（台账行 18:20:25 + CHANGELOG W820 段在库）→ 按 W812 先例（比较**认领登记时序**而非任意文件落盘时序）让号 W822。② 让号 W822 后，「界面视觉重设计细化批」会话已在 W822 号下**在途**施工（对比度实算 `_w822_contrast_audit.py` 与容器测绘 `_w822_container_survey.py` 自 18:35 起落盘，其 CHANGELOG 段将以 W822 为键）；两批同时占用 W822 将致 CHANGELOG 出现两个同键版本段（锚点唯一性断言必红）并使在途级联互相覆盖 → 本批**再让一号**，定号 **W823**。③ 本批 spec 曾与干扰治理批同名路径 `scripts/output/_w820_spec.json` 相撞，18:21:33 该批级联以同名文件覆盖本批 spec 内容（已按对方通知改为唯一路径 `_w823_spec.json` 重写，未覆盖对方现库内容）。取证脚本改名 `_w823_db_schema_probe.py`，报告与脚本内本批编号字样已一并改 W823。
> - **验证（全绿）**：新增取证脚本 `scripts/_w823_db_schema_probe.py`（四子命令 `schema` / `faults` / `bench` / `hygiene`；写入类取证全部在库副本上进行，原库只读；判据未执行即非零退出）实跑 exit 0；引文门禁单文件 0 条规范引文 0 条归属对白 命中率 100%；术语一致性门禁 C1 同步 0 差异、新违规 0；`release_prep.py --check-spec` 四检通过。
> - **状态**：报告已落档，**修复未动工**（处置落地包见报告 §七，含四个包的依赖顺序、具体 SQL 与六条验收判据）。本批为只读审查 + 报告落档，未改动现役库数据（65 / 129 / 0 行不变）与任何 agent-web 源码。

### W824（2026-10-20）：站内阅读入口打通批（T-04 执行前计划落库·实证 622 页 reader 阅读内容站内入链为 0·施工待下一轮）

> **来源**：用户 2026-10-20 会话指令「按 docs/11-方案报告/计划方案 目录内的模板先写方案」+ 前轮《产品、数据、用户思维》外部评审稿的逐条对盘核实（本批方案件即 T-04《执行前计划》）。
> - **文件**：docs/11-方案报告/计划方案/执行前计划-T04-站内阅读入口打通与阅读页体验封装.md、docs/11-方案报告/README.md、docs/00-导读/W批次编号对账表.md、STRUCTURE.md、scripts/output/stats.json、scripts/output/stats-changelog.json、scripts/output/stats-index.md、scripts/output/_w824_spec.json、scripts/output/_cascade_files_W824.txt、docs/superpowers/plans/2026-10-14-interference-governance-roadmap.md、docs/INDEX.md。
> - **对盘结论（外部评审稿不可照做）**：评审稿主张的 11 项「缺失」实已存在（站内搜索 / 100 回阅读页 / 上下回导航 / 55 KPI 看板 / 87 个可视化页 / rum 与 visit-log 埋点 / en 镜像 / 夜读模式 / 响应式 / 阅读指南 / Issue 模板）——它是照 README.md 单页做的评审而非站点面；另含 2 处会改坏仓库的硬伤：① A1-A6 真实口径为**六个内容板块 615 篇**（统计口径说明 §一）而非六种解读维度，照抄将破 verify_delivery 的计数断言；② CI grep W 编号规则会误杀 793 个页面里的溯源注记。
> - **实证 P0（本批目标）**：**622 页 reader 阅读内容站内入链 = 0**——site/index.html 主导航 5 项与全卷索引 9 条全指向 guide.html 或 data/*.html；reader/index.html（已链全部 100 回、已进 sitemap）全树搜入链 0 命中，非搜索页对 reader/ch0XX 引用 0；reader 页顶栏单向可回首页。即**用户搜得到、爬虫抓得到，但点不到**。
> - **两批立项**：W824 入口打通（改 site/index.html 与 site/guide.html，不新增页面 → 页数、统计口径、CSP 与搜索索引口径均不变）；阅读页体验封装（速览深读折叠 / 进度书签 / 字号 / 每页反馈）须改 build_reader.py 重建 622 页，diff 未量化 → 另起 W827 候选（阈值 2000 行）。
> - **撞号让号（本批自身·两度让号后归位）**：初按台账 max+1 认领 W824；随后发现 W825 已被「agent-web SSE 修复」批先落标记（sseStream.ts 18:45:21 / useChat.ts 18:46:45）→ 按先落地者保留让出 W825；W824 曾被「界面视觉重设计细化批」与「机器触发点批」短暂占用，二者均已自行改号让出 → **四面扫描**（台账行 / 磁盘件 / 源码注释 / spec）确认 W824 无在用面 → 归位 W824（= CHANGELOG 顶段 W823 + 1），号段链接上 W822→W823→W824→W825→W826→W827。
> - **验证**：CSP 856 页 0 漂移；搜索索引新鲜度 0 FAIL（zh 830 条 / en 872 条）；结构门禁 OK；stats 16 键零差异（report_docs 34→36 = 现役报告 29〔含在途 2〕+ 索引 README 1 + 计划方案 6）；目录文档新鲜度 0 FAIL / 178 目录；台账认领行以 preflight_check.parse_ledger 实证回读（严格 7 格、状态落 cells[4]、touches 落 cells[6]、max=826 与 bullet=W827 交叉核验一致）。
> - **状态**：方案件已落库，**施工未动工**（入口打通与六文档收官级联随下一轮施工批补）。
### W825（2026-10-20）：审查发现第二批修复批（前端流式链路三项 + 门禁解析层格式鲁棒性）

> **来源**：2026-10-20 全项目只读审查（前端面 + 门禁判据面）实证的缺陷，叠加并行会话 W818 批反馈的台账格式错位问题。
> - **文件**：xiyouji-agent-web/src/utils/sseStream.ts、xiyouji-agent-web/src/utils/sseStream.test.ts、xiyouji-agent-web/src/hooks/useChat.ts、xiyouji-agent-web/src/hooks/useChat.streaming.test.ts、scripts/preflight_check.py、tests/unit/test_preflight_check.py、docs/00-导读/W批次编号对账表.md、scripts/output/_w825_spec.json。
> - **缺陷①（SSE 帧跨片整帧丢失）**：服务端帧格式为 `data: <JSON>\n\n`（`server/sse.ts:58`），而一次网络读**不保证落在帧边界**——`tool_result` 帧可达 256KB 至 1MB（`server/engine/tools.ts` 的 READ_MAX_BYTES 与 RUN_MAX_BUFFER）必然被切成多片。旧实现逐片 `chunk.split('\n')` 独立处理：第一片是半截 JSON → 解析失败被 `catch {}` 静默丢弃；第二片是 JSON 残段 → 不以 `data: ` 开头被跳过 ⇒ **整帧事件凭空消失，无报错无日志**（工具条目永远停在「执行中…」、文本增量丢字）。且 `src/utils/sseStream.ts`（原设计的复用层）从未被引用，解析逻辑在两处各存一份。**修**：新增 `createSseLineSplitter()`（跨块行缓冲：末尾半行留待下一片，流结束时冲刷），`readChatStream` 与 `useChat` 内联解析**共用同一实现**（单一修复点，两处不再分叉）。**验**：帧被切成两片/逐字符时事件均被完整还原；200KB 大帧跨片还原零丢失；控制组（整帧一次到达、心跳与非法 JSON 帧跳过）行为不变。
> - **缺陷②（流失败后永久「思考中…」且错误文案不可见）**：`init` 事件把消息 id 由 `tempAssistantMessageId` 改写为 `realAssistantMessageId`，而 catch 分支只按 temp 匹配 ⇒ **init 之后的任何异常都匹配不到任何消息** → 错误文案写不进、`isStreaming` 永为 true（`finally` 只复位 `isLoading`）→ 前端永久显示「思考中…」、反馈/复制/重新生成按钮永不出现。另一路径：SSE `error` 事件只写 `content`，而 `ChatMessages.renderAssistantContent` 优先渲染 `contentBlocks`（非空即跳过 content）⇒ **有内容块时错误提示完全不可见**。**修**：catch 分支同时匹配两个 id；finally 分支兜底复位消息流式态；错误文案**追加为文本块**（保留已生成的部分回答且错误可见）。**验**：源码级回归锚四条（catch 双 id 匹配、finally 复位、错误追加为文本块、停止链路 abort 接线）逐条钉住。
> - **缺陷③（「停止」按钮不停止生成）**：`handleStop` 只 `setIsLoading(false)`，请求无 `AbortController` ⇒ 流继续推进、答案继续增长、服务端继续跑完本轮；且 `isLoading` 复位后可再次发送 ⇒ 同一会话两条并发流同时写状态；组件卸载也无清理（切页后无人观察的流继续改全局会话）。**修**：`AbortController` 接线（fetch 带 signal）+ 停止按钮 `abort()` + 卸载清理 + 停止时结束流式态。
> - **缺陷④（台账解析层按固定下标读列 ⇒ 幻影在途行）**：认领行摘要若含裸竖线，Markdown 按竖线分列 ⇒ 行被切成 8/9 格（标准 7 格）⇒ `parse_ledger` 的 `cells[4]` 读到摘要残段（把批次号当状态）→ **已收官批次被永久判为在途**；`cells[6]` 读到认领会话列 → touches 变成非路径垃圾串。实测两行幻影：W764（8 格·状态读成「W764」·touches 读成「DSH 2026-10-16」）与 W750（touches 占位符「—」被当成一个路径条目）。**修**：状态列改为**右起首个紧匹配**「已收官/已闭环」形态的格（整格即状态，避免主题里偶然出现同词被误认），无匹配则回退 `cells[4]`；touches 改为**取末格**（touches 是固定末列，摘要里的裸竖线只让前列右移、末格不动）；touches 占位符归一为空集。**验**：修复前两条用例逐条变红、幻影在途行复现；修复后 W750 与 W764 两行幻影消失，在途清单只剩真实在途批次。
> - **并发回退处置（如实记账）**：本批的解析层修复曾被 W822 批的整仓提交（`7fa31d82`）覆盖丢失（其特性已落 HEAD、我方改动被回退），按「并发提交回退的正确处置」**定点补回并单独提交**；同时 W822 批遗留未提交的 3 条干扰日志用例随本批一并入库（其源码特性已在 HEAD·测试悬空），提交信息中逐条标注归属。
> - **验证**：前端 vitest **51 passed / 5 files**（原 41 → +10：帧缓冲 7 + 源码级不变量锚 4，含 2 条控制组保持绿）；`tsc --noEmit` **0 错**；agent-web 服务端测试 64 pass / 1 skip / 0 fail；`pytest tests/unit/test_preflight_check.py` **19 passed**（含 W822 遗留 3 条）；`ruff check scripts/` 0 违规；`check_doc_sync.py` 0 FAIL；`verify_delivery.py` 全量 51 段 0 FAIL。
> - **状态**：已落地（本地提交·未推送）。

### W826（2026-10-20）：界面视觉重设计细化规格批（五项裁决落地 + 实算参数 + 迁移批次清单）

> **来源**：用户令「帮我给界面出一版重设计：视觉层级、配色与字体体系、间距栅格、组件样式统一都要升级，保留原有功能结构不乱动，**先出设计方向再细化**」——W819 交付设计方向后，用户就方向文档 §10 的五个议题**逐条选中推荐选项**（对比度基线 / 朱砂实底限额 / 容器档位 / 夜读模式地位 / 迁移节奏），本批据此把方向翻译为**可执行规格**。
> - **文件**：docs/11-方案报告/界面视觉重设计细化规格-v4-2026-10-20.md、docs/11-方案报告/界面视觉重设计方向-v4-2026-10-20.md（v1.1 订正）、docs/11-方案报告/README.md、docs/00-导读/W批次编号对账表.md、scripts/_w826_contrast_audit.py、scripts/_w826_container_survey.py、scripts/_w826_migration_plan_check.py、scripts/output/_w826_contrast_audit.json、scripts/output/_w826_container_survey.json、scripts/output/_w826_migration_plan_check.json、scripts/index.md、scripts/output/index.md、site/data/search.html、site/en/search.html。
> - **五项裁决（2026-10-20 用户逐条确认）**：① 对比度基线＝正文 AA+ ≥7:1 作目标线 · AA ≥4.5:1 作红线（元信息/图形边界 ≥3:1）；② 朱砂实底每页 ≤3 处（严口径）；③ 容器三档 760 / 1120 / 1320（dashboard 1536 降档）；④ 夜读模式继续与浅色平级（改造量翻倍）；⑤ 迁移每批 ≤10 页灰度。
> - **取证①（对比度实算·`scripts/_w826_contrast_audit.py`·WCAG 2.1）**：17 组比值实跑，**5 项未达标**并给出三条修法取值——朱砂落页面底 4.47→**4.50**（新增 `--accent-text: #C7463A`）· 图表赭金 2.42→**3.01**（深档 `--chart-3: #B38F58`）· 暗色朱砂 4.35→**4.50**（`#E46250`）；另 `--accent-soft` 1.80:1 → 降为纯装饰、**禁作交互边界**，`--chart-5` 米灰 1.55:1 → 仅作底色。
> - **取证②（推翻 W819 估算·两处）**：`--ink-3` 现役 `#9A9280` 实测 **3.09:1 已达标** → **撤销**方向文档「加深至 #8A8271」的结论；容器「四档并存」实为**现役主力 1320**（data/en 合计 166 页纯 1320，1200 仅存于 DESIGN.md §3.1 规范条文）→ 待迁移面由「四档并存」收敛为 **18 页**（`scripts/_w826_container_survey.py` 实测）。
> - **取证③（迁移批次对拍·`scripts/_w826_migration_plan_check.py`）**：§6 批次清单对拍磁盘——site/data 87 页 + 根 8 页 **0 漏 0 重** · 每批 ≤10 · reader 622 页单批 → 判定 PASS。
> - **规格交付（细化规格文档 11 节）**：§3 五项裁决逐条落地细则（朱砂实底定义与白名单、容器迁移映射 18 页明细、暗色双组色板与三档硬指标）· §4 **v4 令牌终稿**（纯加法 +62 变量 ≈ +2.9 KB·不改任何现役取值⇒857 页视觉零变化·须同批上调 DESIGN.md §4A.8 预算至 +3 KB）· §5 **24 组件规格卡**（含 10 张重点卡：用途 / 结构 / 令牌 / 五态 / 禁改项）· §6 迁移批次清单 11 批 · §7 **阶段 1 六判据**（含 J2「现役页面 computed-style 全量快照零差异」探针设计·仓内首次落视觉回归载体）· §8 W819 估算值订正表；同步将 W819 方向文档升 v1.1（§4.3 对比度表改实算值、§10「待裁决项」改「裁决记录」）。
> - **让号链（两次让号·可复算时间线）**：原编 W822（干扰治理批已落地：safe_commit.py 18:37:43 · preflight_check.py 18:41:41 · CHANGELOG W822 段在库）→ 让至 W824（干扰治理批改号后所占）→ 再让至 **W826**（台账 max=825·站内阅读批取 W825·现势 bullet 已指 W827）；本批文件名前缀与台账行号统一为 W826。
> - **范围纪律**：**细化 ≠ 实施**——未落任何令牌/组件/页面改动，`site/` 857 页**视觉 0 改动**（仅搜索索引 2 页机械刷新）· DESIGN.md 0 改动 · tokens.css/system.css 0 改动 · DOM 类名与功能结构 0 改动（用户硬约束「保留原有功能结构不乱动」）。
> - **验证**：三脚本实跑复现全部计数与比值（退出 0）· 批次清单对拍 PASS · 第 45 槽 0 FAIL · 第 46 槽 0 FAIL（zh 830 / en 872 与生成器实算一致）· `generate_csp.py --check` 856 页 0 漂移 · `py -3 scripts/stats.py --check` 16 键零差异。
> - **状态**：已落地（本地提交 9114d968 + 收官登记 9ab0b094·未推送）；终稿规格见 `docs/11-方案报告/界面视觉重设计细化规格-v4-2026-10-20.md`；**下一步待用户确认**：阶段 1（令牌 v4 纯加法落地·首次触碰全站共享层 tokens.css 并触发 856 页内联级联）开工与否。

### W827（2026-10-21）：站内阅读入口打通施工批（622 页 reader 从站内 0 入链到首页一跳可达）

> **来源**：用户「可以」批准 —— T-04 执行前计划（`6b02c346`·W824 方案件）的施工落地。计划核心判据：`site/` 全树（排除 `site/reader/`）对 `reader/index.html` 命中 0，620 页正文解读处于站内孤岛。
> - **文件**：site/index.html、site/guide.html、docs/11-方案报告/计划方案/T04-任务计划执行与经验沉淀报告-2026-10-21.md、docs/11-方案报告/README.md、docs/11-方案报告/系统架构方案-分层模块与部署-2026-10-20.md、STRUCTURE.md、scripts/output/stats.json、scripts/output/stats-changelog.json、scripts/output/stats-index.md、scripts/output/_w827_spec.json、scripts/output/index.md、docs/00-导读/W批次编号对账表.md。
> - **五处入口**：① 首页主导航新增「阅读」指向 `reader/index.html`（原 6 项无一项通向阅读）；② 首屏 masthead 加「开始阅读 · 第 1 回 灵根育孕源流出 →」CTA 指向 `reader/ch001.html`；③ 新增「从哪一回读起」区块，4 张卡直达第 1 回（开篇）/ 第 5 回（大闹天宫）/ 第 27 回（三打白骨精）/ 第 58 回（真假美猴王），回目名由 `site/reader/index.html` 程序化提取非记忆；④ 全卷索引「开卷有益」后插入「逐回精读」行（编号 01），原 11 条 00-10 顺延为 02-11，脚本内前置断言 `len(rows)==11 and nos==range(11)` 不符即停；⑤ 导读页 `guide.html` 主导航 + 首条阅读路径卡各补 1 条。
> - **范围纪律**：不改 `site/reader/**` 622 页（体验封装属 W829 候选·未获批）；不新增任何页面；零外域请求与外域脚本；不改管控件与 archive；不推送远端。
> - **计划偏差（如实留档 4 条）**：AC-04 原按「索引 9 条 00-08」编写，开工实测 11 条 00-10（计划时点后新增 curated 等行）→ 按实质判据执行；AC-07 计数基线 34→（计划自带的 39 订正）→ 本批实测 40；AC-01 的 `../reader/` 形态表述有歧义（两页均在 site 根，形态同为 `reader/index.html`）→ 按「两页各至少 1 条」验收；AC-18 干扰日志未命中（开工 staged=0，无已暂存变更）→ 不虚构登记。
> - **验证**：AC-01~AC-20 逐条实测（报告 §二 表格留证）；9 条门禁逐条 rc=0（`_gen_search_index` / `check_search_index_fresh` / `lint_links --internal` / `generate_csp --check` / `check_seo_head` / `a11y_audit` / `check_structure` / `check_doc_sync` / `verify_delivery`）；页数四项 88/138/622/9 不变；`report_docs` 39→40 且三处标记同步；连通性探针实证首页一跳直达两个目标、非搜索页对 `reader/ch0\d\d` 引用数 0→1。
> - **状态**：已落地（本地提交·未推送）；本批为递延链解链批（顶段 W826 + 1 → 版段由级联直接落下）。

### W830（2026-10-20）：计划方案三性审查与快照漂移门禁修复批（9 份文档约 60 断言复算 + C5b 扩展面 + pytest_collected 键 + 六处订正）

> **来源**：用户令「这些计划方案你审查遍是否符合实际是否量化是否可验证」+ 同轮对话批准「开始」执行修复建议。
> - **文件**：scripts/check_doc_sync.py、scripts/stats.py、pytest.ini、docs/11-方案报告/计划方案三性审查报告-2026-10-20.md、docs/11-方案报告/系统架构方案-分层模块与部署-2026-10-20.md、docs/11-方案报告/静态站前端框架化选型对比-2026-10-20.md、docs/11-方案报告/计划方案/执行前计划-T03-全项目审查第一批修复.md、docs/11-方案报告/计划方案/执行前计划-T04-站内阅读入口打通与阅读页体验封装.md、docs/11-方案报告/README.md、STRUCTURE.md、docs/agent/gates.md、docs/00-导读/W批次编号对账表.md、scripts/output/stats.json、scripts/output/stats-changelog.json、scripts/output/stats-index.md、scripts/output/index.md、docs/INDEX.md、site/data/search.html、site/en/search.html。
> - **审查结论**：9 份文档三性全部达标，约 60 断言实跑复算绝大多数字节级一致（reader/index.html 108,699 B、tokens.css 20,799 B、text-search-app.js 2,177,796 B、relationships.html 373,002 B、81 难数据集序号逐点命中、DB 基线探针复现），无编造数据；问题集中于三类——快照数字漂移无门禁兜底（系统架构方案 report_docs 字面 30 过期、pytest 计数 600/602 vs 实测 770、W818 site/data 合计 9,272,531 与自身均值 110,483 矛盾）、W829 撞号（并行会话在途占用且无认领行）、B1/B2 fail-open 遗留（原定批次 W817 被 agent-web 加固批占用）。
> - **修复① C5b 扩展面**（check_doc_sync.py）：`docs/11-方案报告/` 根层现役报告 + `pytest.ini` 入 stats 实体标记对账——只跑标记、不跑句式白名单与 C5c 裸数字（辅助叙述面宁窄勿误）；**计划方案/ 子目录刻意除外**（计划件为时点快照，其引用的基线数字随批次冻结，同 CHANGELOG 历史段纪律禁回溯改写，由计划自身「聚合数字当批现测」条款在开工批复核——T04 AC-07 34/35 vs 现役 37 实例）；**建置即红实证**（先红后绿：扩展面纳入当场抓出系统架构方案 30≠36 与 stats 新键未刷新→订正刷新后转绿）；自测 20→22 例（T21 扩展面标记失配必红 / T22 一致放行·双向锁）。
> - **修复② stats 新增 pytest_collected 键**（stats.py）：`pytest --collect-only -q` 实算·fail-closed（pytest 不可用/收集失败/解析失败即 FAIL·禁静默写坏 stats.json·与「不允许从未运行的门禁存在」铁则同族）；C5d 子进程 timeout 60→180s 同步留裕量。
> - **修复③ 六处文档订正**：系统架构方案 report_docs 30→37；W818 site/data 合计 9,272,531→9,722,504（=均值 110,483×88 对账值·与「9.27 MB」注解自洽·原误植留档）；pytest.ini 头注 602→770 实体标记 + 49 段→51 段；T03 计划状态字段执行中→已收官（W816 落地 55b9b8c0）；T04 计划 AC-07/ASM-08 加开工重测注记（现役 37 非 34/35）；STRUCTURE 36→37 并去过期「在途 2 篇」括注。
> - **修复④ 治理登记**：对账表 W830 认领行 + bullet——W829 在途占用实证（工作树 4 文件注释带 W829 标记·内容为 agent-web 错误回显加固 + E2E 临时库隔离·对账表无认领行·按「先落地者保留」判例视为已占·T04 候选应顺延）；B1/B2 待用户单独批准并指定批号（W830 之后）——修复前「全量 0 FAIL」结论对子进程崩溃类故障不具备背书力。
> - **连带链路**（新增报告进索引载荷·W806/W807 同型）：docs/INDEX.md 重生 727→728 篇；`_gen_search_index.py` 重生（zh 831 条 / en 873 条）；`generate_csp.py` 重生 2 页内联哈希·`--check` 856 页 0 漂移。
> - **验证（全绿）**：doc-sync 主检 0 FAIL（C5b 扩展面生效·C4-f 三项未暂存残留随本批提交自解）+ self-test 22/22；`stats.py --check` 17 键零差异（report_docs 36→37 + pytest_collected 770 新键）；ruff scripts/ 0 违规；pytest 767 passed + 3 skipped / 0 failed（搜索索引用例曾因新报告条目红→重生索引后转绿·留档）；check_search_index_fresh 0 FAIL；generate_csp --check 856 页 0 漂移；verify_delivery 全量见收官记录。
> - **状态**：已落地（本地提交·未推送）；B1/B2 与 W829 撞号处置留待用户裁量（见审查报告 §六）。

### W831（2026-10-20）：取经编制表落库与编制位补全批（17 位编制表 + 归档与工地两套治理系统纳入 + 零前置知识速览 + 三处编制位空缺诊断）
> **来源**：用户 2026-10-20 会话三问——①「帮我推荐适合我的工具/技能」→ ② 纠正「难道不应该贴合本项目来做吗？本项目是西游记，你就按照西游记里面的角色人物来看看哪个比较贴合」→ ③ 纠正过程产物落位（`.tmp/` 非 sanctioned 临时区）→「先把方案写出来」→ 再要求「写清楚内容，从没看过本项目的任何人包括 Agent 都能读取知道了解详细内容」。
> - **文件**：docs/11-方案报告/取经编制表-工具与技能挂位-2026-10-20.md、docs/11-方案报告/取经编制表-工具与技能挂位-2026-10-20.html、docs/11-方案报告/计划方案/执行前计划-T05-取经编制表落库与编制位补全.md、docs/11-方案报告/README.md、docs/00-导读/W批次编号对账表.md、docs/superpowers/plans/2026-10-14-interference-governance-roadmap.md、scripts/output/_w831_spec.json、scripts/output/_cascade_files_W831.txt。
> - **编制轴（17 位 × 6 列）**：甲组取经四众 4 位（孙悟空=施工官/唐僧=持经人/猪八戒=挑刺官/沙悟净=收官官）· 乙组天庭编制 5 位（玉皇大帝=号牌官/太白金星=传令官/太上老君=器物官/观音菩萨=仲裁官/如来佛祖=框架官）· 丙组旁证与方法 6 位（菩提祖师=授业官/千里眼·顺风耳=取证官/谛听=只验证/六耳猕猴=反面角色·假收敛/红孩儿=高风险项/牛魔王=失控面·禁令）。每位列「谁→负责什么→挂什么→怎么用→不能做什么」五问，并给出「在役 / 位空·建议建 / 在役（禁令）」三态。
> - **回目标与引文（全部实测·非凭记忆）**：10 组回目标由 `py scripts/_cite_probe.py` 实测提取（六耳猕猴与谛听同在第 58 回·太白金星第 3/4/21/44/71/74/83/92 回·菩提祖师第 1 回·太上老君 17 回·猪刚鬣第 18/19/63 回·沙悟净第 22/29/100 回·玉皇大帝第 15/17/63/71 回·白龙马第 31/40/52/65/82 回·观音菩萨 30 回）；15 条原文引文逐字比对 `dataset/text-search.json` **15/15 命中**。**排版纪律实证**：初版 2 条引文被把内层 `“…”` 改成 `‘…’` 而破坏「语料精确子串」保证 → 已修正为语料原样 + 外框统一 `「」`，并写入 ASM-15 与编制表 §6.1。
> - **三处编制位空缺（实测诊断）**：① 器物官位——`mavis mcp list` 实测 0 个 MCP 服务器，仓内 `mcp-server/xiyouji_mcp.py` 5 只读工具齐备且背后 5 脚本实测全在位，唯一缺口 `fastmcp` 未装（补全 = 2 条命令，`command` 须为 `py -3` 因本机 `python` 是应用执行存根）；② 收官官位——`mavis agent list` 实测仅 explore/worker/verifier 三个通用角色，46 条门禁与 9 处旁文档指针面无专属执行体（旁文档滞后已由并行会话 2 次检出）；③ 授业官位——本地技能目录实测为空，`docs/agent/pitfalls.md` 已沉淀可复用避坑条目但模型改文件前不会主动加载（补全 = 1 次 Agent 创建 + 1 次 Skill 固化，**均须用户逐项批准**）。
> - **零前置知识可读（AC-13）**：编制表含 §0 一分钟速览（项目四层产物 + 本文档是什么 + 三条阅读路径 + 5 词最小词汇集）、§5 前置知识清单（27 条术语各配一句解释 + 权威指针）、§6 复现命令（引文复现 / 逐字一致性自查 / 缺位诊断复现）——任何没读过本项目的人或 Agent 可独立读懂并自行下钻。
> - **HTML 预览页（零外域依赖·file:// 直开）**：Playwright 实测 15 卡 / 15 引用块 / 45 挂载标签 / `extEls=0` / 无控制台错误 / 无横向溢出 / 底色 `rgb(250,247,240)`。**范围纪律**：本批不使用 `<!--stats:*-->` 实体标记（编制表内容与报告篇数无关；改动者请勿擅自添加，见 D-10）。
> - **并行避让（W832 在途批）**：对方已声明 touches 7 项（对账表 + `_w832_spec.json` + `xiyouji-agent-web/` 6 文件），**与本批 touches（`docs/11-方案报告/README.md`）交集为空**；其另在改但未声明 `STRUCTURE.md` / `scripts/output/stats.json` / `系统架构方案-*.md` / `三性审查报告-*.md` / `pytest.ini` / `scripts/verify_delivery.py`——本批**一律不碰**，`stats.json` 的 `report_docs` 漂移（实算 39 vs stats 38）登记为待刷项交对方批收尾时刷新（收敛到 39）。**号段未撞**：我方 W831 · 对方 W832 → 链 W830→W831→W832 连续无空号。
> - **门禁轨迹**：第 31 门禁在本批推进过程中 FAIL 由 5 → 1（3 处 C5b 系对方未提交刷新所致并已被其同步；C4-f 需提交后清）→ 本批落件后 0 FAIL。**版段递延**：顶段仍为 W826 且 W827 已被预留占用，`batch_cascade` 断言「批次号 = 顶段+1」→ 本批按 W830 先例走 spec 入库 + 待顶段推进后以 chore 补写路径（见 T-05 §5.7 R-01）。
> - **范围纪律**：不改 site/ 任何现役页面 · 不改 DESIGN.md 宪法 · 不改 verify_delivery.py / check_doc_sync.py / batch_cascade.py / preflight_check.py 等管控脚本 · 不动 W827/W828/W829/W830 他方认领行与版段 · 不动 W832 在途批所持有面 · 不推送远端 · 临时产物全进 `tmpe/_shot/` 与 `tmpe/_misc/`（不在仓库根另建临时区） · 仓外三动作（fastmcp 装包 / MCP 注册 / 建 Agent 与 Skill）不占 W 号且须用户批准后执行
### W832（2026-10-20）：agent-web 生产面加固批（错误原文回显收口 + 端到端测试改跑临时库）

> **来源**：2026-10-20 全项目只读审查（服务端面 + 端到端测试面）实证的两项缺陷。
> - **文件**：xiyouji-agent-web/server/chat.ts、xiyouji-agent-web/server/routes.ts、xiyouji-agent-web/server/db.ts、xiyouji-agent-web/e2e/chat.e2e.mjs、xiyouji-agent-web/src/hooks/useChat.streaming.test.ts、docs/00-导读/W批次编号对账表.md、scripts/output/_w832_spec.json。
> - **缺陷①（底层错误原文回显客户端）**：三处把内部异常原文直接交给客户端——① `server/chat.ts` 保存消息失败时 `detail` 带 SQLite 错误原文（含库文件绝对路径）；② `server/chat.ts` 聊天异常 catch 块把 `error.message` 送进 SSE error 帧（上游引擎错误体含前 300 字原文，可能回显请求内容或账号信息）；③ `server/routes.ts` 的 `/api/ready` 探针 `detail` 带数据库异常原文。**与本仓既有红线冲突**：`server/errors.ts` 的对外契约明定「编程错误 → 固定文案 + 不泄细节」，而这三处绕过了该收敛层（走 `sendError` 旁路）。**修**：三处**形状全部不变**（`detail`/SSE `message` 字段仍在），只把取值换成固定文案（`数据库写入失败` / `服务器内部错误` / `数据库不可用`），原文照旧进 `logger`；已核实全仓无消费方读取这些取值（前端 `ChatInput.tsx` 的 `e?.detail` 读的是 DOM 异常对象，不是本仓响应体）。**验**：集成测试 19 pass / 1 skip；响应体形状与状态码零变化。
> - **缺陷②（端到端测试会删开发者真实会话）**：`server/db.ts` 的库路径写死为 `data/chat.db`，而 `e2e/chat.e2e.mjs` 的收尾清理按「最近更新的 session」删 feedback/messages/sessions → 若本轮聊天未落库而库中已有历史会话，被删的就是**真实会话**（含工具结果原文·不可逆·无备份）。**修**：① `server/db.ts` 支持 `AGENT_WEB_DB_PATH` 覆盖（默认路径不变·生产形态零变化）；② 端到端测试起后端时指向**临时库**，断言与清理只用该临时库；③ 收尾断言**真实库零改动**（大小 + mtime 双比对）；④ 硬守卫：`DB_PATH` 指向真实库时**拒绝启动**且**跳过全部清理**。
> - **负样本自证事故（如实记账·已复原）**：为验证硬守卫，把 `AGENT_WEB_DB_PATH` 指向真实库跑了一次负样本 —— **我方新增的「删临时库文件」块当时没有守卫**（守卫只在启动侧），且「真实库零改动」断言排在该删除块**之后** ⇒ 该次自证把真实 `data/chat.db` 连同 `-wal`/`-shm` 删除。**复原**：用 W828 批 `VACUUM INTO` 留下的快照 `tmpe/w828/backup_probe_dir/chat-20261020.db`（184320 字节·与被删文件字节数一致）恢复 → `integrity_check=ok`·**65 会话 / 129 消息全量复原**；快照内最新会话为 2026-10-18 21:13 ⇒ 快照后本机未产生新会话 ⇒ **实际数据零丢失**。**根因订正（已落地）**：守卫改为**三处同源**——① 启动侧拒绝 ② 清理侧不删（`DB_IS_REAL` 判定）③ 断言移到全部清理之后；复测负样本：拒绝启动 + 真实库 size 与 mtime **完全未变**。**教训**：破坏性清理路径的守卫必须覆盖**删除动作本身**，且安全断言必须排在所有破坏性动作**之后**——「只在入口设防」不构成保护。
> - **验证**：端到端测试实跑 **11 通过 / 0 失败**（含新增「真实库零改动」断言）· 负样本自证（指向真实库）**拒绝启动 exit 1 且真实库零改动** · `npm run test:server` 64 pass / 1 skip / 0 fail · 集成测试 19 pass / 1 skip · `tsc --noEmit` 0 错 · 前端 vitest 51 passed。
> - **状态**：已落地（本地提交·未推送）。CHANGELOG 版段因顶段序约束（batch 必须等于顶段+1·当前顶段为 W826·W827 至 W831 的段均待补写）**递延**，待顶段推进后以 chore 批补写十面；本批内容与认领行已入库。

### W833（2026-10-20）：交付链与工具链静默失效根修批（分支保护零强制点 + 独立工作流守卫 + 锁失配即红 + 类型检查真跑）

> **来源**：2026-10-20 全项目只读审查（交付链面 + 工具链面）实证的四项缺陷。
> - **文件**：.github/workflows/workflow-lint.yml、.github/workflows/ci.yml、.github/workflows/security.yml、.github/workflows/README.md、.github/workflows/index.md、scripts/output/_w833_spec.json、scripts/output/README.md、scripts/output/index.md、docs/00-导读/W批次编号对账表.md。.github/workflows/README.md、.github/workflows/index.md、docs/00-导读/W批次编号对账表.md、scripts/output/_w833_spec.json。
> - **缺陷①（main 分支零强制点）**：远端实测 `repos/1273984347/xiyouji/branches/main/protection` 的 `required_status_checks` 与 `required_pull_request_reviews` **均为 ABSENT**、`rulesets` 为空 ⇒ 整条交付链（51 段硬门禁 / 10 个 CI job / pre-commit hook）**全部是建议性的**：CI 红可合、CI 未运行也可合——这正是「事故静默复发」的根条件（W806 同型事故：工作流整体不可解析 → run 0 秒失败 → PR 根本不生成 check，在无人察觉下复发过一次）。**修**：以「读→改→写」方式加 `required_status_checks` = 两个始终运行的 job（`Delivery Gate (verify_delivery.py)` + `Unit Tests (pytest)`·strict=false），其余键原样保留（`enforce_admins` true；`lock_branch` / `required_linear_history` / `required_signatures` / `required_conversation_resolution` 均 false——**此前审查结论称 linear_history/signatures 已启用·经复核不属实·此处按实测纠正**）。回滚命令：`gh api -X DELETE repos/1273984347/xiyouji/branches/main/protection`。
> - **缺陷②（工作流守卫与被守卫同生共死）**：事故机理——ci.yml 某 step 的裸标量值内含冒号加空格 → YAML 映射歧义 → GitHub 解析该工作流直接失败、报「workflow file issue」、run 0 秒失败且 `pull_request` **不生成 check**；而当时唯一的可解析性守卫（W811 增的 pytest 用例）住在 **ci.yml 的 pytest-unit job 内** ⇒ 守卫与被守卫同生共死，ci.yml 坏掉时守卫根本不启动，缺陷遂复发。**修**：新增 `.github/workflows/workflow-lint.yml`——**独立存在**、`push`/`pull_request` 不限分支、只做一件事（PyYAML 全量解析全部工作流并指出失败文件与常见成因），ci.yml 坏掉时它仍能照亮问题；实测本机 10 个工作流全部可解析（0 失败）。
> - **缺陷③（锁失配被回退静默吞掉）**：security.yml 两处 `npm ci` 失败即回退 `npm install`——lock 与 manifest 失配时会按**浮动版本**重新解析出一棵与 CI 构建、本地安装都不同的依赖树，随后 npm audit 审计的也是那棵树，而「锁不同步」这一最该暴露的信号被吞掉。**修**：去掉回退，失配即红（fail-closed）并给出可判定的错误说明。
> - **缺陷④（类型检查从未真正执行）**：ci.yml 的 mypy 命令带 `--non-interactive`——mypy ≥ 1.11 起该选项**必须**搭配 `--install-types`，单独使用直接在参数解析阶段报错（实测：`error: --non-interactive is only supported with --install-types`）→ 配合忽略失败的写法整条命令静默失败 ⇒ **类型检查一次都没跑过**。**修**：去掉该参数（保留 report-only 不阻断），输出截尾 5 行避免 3000+ 行日志淹没 CI；实测去掉参数后真跑：`Found 3353 errors in 275 files`——此前一次都没跑过。
> - **验证**：10 个 workflow 全部 PyYAML 可解析（0 失败）· main 保护复验 `required_status_checks` 已含两个检查且其余键未变 · 交付门禁未受影响（本批只改 workflow 与远端设置）。
> - **状态**：已落地（本地提交·未推送）。CHANGELOG 版段因顶段序约束（batch 必须等于顶段+1·当前顶段为 W826·W827 至 W832 的段均待补写）**递延**，待顶段推进后以 chore 批补写十面；本批内容与认领行已入库。

### W834（2026-10-20）：门禁 fail-open 根修批（B1/B2 用户批准·verify_delivery fail-closed 化 + 12 例负样本）

> **来源**：用户令「开始」——批准执行 W830 审查报告 §六建议 1（B1/B2 修复·CLAUDE.md 第 10 条授权改管控件 scripts/verify_delivery.py）。
> - **文件**：scripts/verify_delivery.py、tests/unit/test_verify_failclosed.py、pytest.ini、scripts/output/stats.json、scripts/output/stats-changelog.json、scripts/output/stats-index.md、scripts/output/_w834_spec.json、STRUCTURE.md、docs/11-方案报告/系统架构方案-分层模块与部署-2026-10-20.md、docs/11-方案报告/计划方案三性审查报告-2026-10-20.md、docs/11-方案报告/计划方案/执行前计划-T04-站内阅读入口打通与阅读页体验封装.md、docs/00-导读/W批次编号对账表.md。
> - **B1 根修**（_run_simple_gate·T03 D-01 遗留）：两条异常路径由 WARN 改 FAIL——子进程崩溃/超时 = 判据不可执行，原 WARN 使 18/33 委托段崩溃即降级而整轮仍报「核心全部通过 ✅」+ exit 0（假绿面根除·对齐 _run_strict_gate 语义）；唯一保留 WARN 为 Gate.missing_warn 登记的运行期缺失降级（W424 M2·仅 2 个 node 段·显式 opt-in·docstring 已注明）。
> - **B2 根修**（_gate_a11y）：三处 fail-open 全改 FAIL——① JSON 解析异常原记 rep.ok「summary 解析跳过」；② 缺 summary/E2-2 键原走 p01=0 静默判绿；③ 外层异常原记 rep.warn。现为解析失败/结构不符/子进程异常一律 FAIL（fail-closed·_count_by_rule 预置全规则 0 值故干净态恒有 E2-2·快乐径不受影响·回归锁钉住）。
> - **同族全扫**（建置即红纪律）：verify_delivery.py 内 except 路径的 rep.ok/rep.warn 仅此 4 处（:645/:648/:1009/:1014·本批实证）；scope 跳过路径（:343·登记式分级）与 _probe_health（登记式可选探活）不属缺陷面；无隐藏同类。
> - **负样本测试**：新增 tests/unit/test_verify_failclosed.py 12 例全过——B1×5（崩溃必红且零 OK 零 WARN / 未登记 missing_warn 必红 / 登记缺失保留 WARN / 快乐径回归 / 退出码径回归）+ B2×7（解析失败必红 / 缺 summary 必红 / 缺 E2-2 必红 / 子进程异常必红 / 干净态 OK 回归 / P0+P1 阻断回归 / 非零退出回归）。
> - **行为不变性**：退出码口径与快乐径消息文本零变化（5 例回归锁）；门禁段数 51 不变（段自洽锁实证 51==51）；全量 verify 核心全部通过。
> - **连带刷新**：stats pytest_collected 770→782（本批 12 例入库）、report_docs 37→39（并行 W831 取经编制表批落库·W761 先例 glob 计磁盘口径）；STRUCTURE 与系统架构方案 report_docs 标记同步 39；pytest.ini 标记 770→782；W830 行递延注记更新。
> - **取号与版段**：原拟 W831 被并行「取经编制表」批占用（d560a8d7）、W832 被 agent-web 加固批占用（990fa068）、W833 被并行「交付链与工具链根修」批占用（_w833_spec.json 22:09 + workflow 在途件）→ **三度顺延 W834**；CHANGELOG 版段递延（顶段序约束 batch==顶段+1·顶段仍 W826·W830-W833 同处递延·号序链待 W827/W828 落地后恢复·spec 已入库）。
> - **状态**：已落地（本地提交·未推送）。

### W835（2026-10-20）：服务端暴露面收口批（Host 头白名单防 DNS rebinding + token 硬开关 + 启动暴露面告警）

> **来源**：2026-10-20 全项目只读审查（服务端面）所得的两项暴露面缺陷。
> - **文件**：xiyouji-agent-web/server/security.ts、xiyouji-agent-web/server/config.ts、xiyouji-agent-web/server/middleware.ts、xiyouji-agent-web/server/index.ts、xiyouji-agent-web/server/security.test.ts、xiyouji-agent-web/.env.example、docs/agent/agent-web.md、docs/00-导读/W批次编号对账表.md、scripts/output/_w835_spec.json、scripts/output/index.md、scripts/output/README.md。
> - **缺陷①（服务端无 Host 校验 → DNS rebinding 可驱动本地 Agent）**：服务端只绑定回环地址（127.0.0.1）且默认免认证，但**浏览器发往 127.0.0.1 的请求会带上攻击者可控的 Host 头**——攻击者把 evil.com 的 DNS 解析到 127.0.0.1（DNS rebinding），浏览器便以 `Host: evil.com:3000` 请求本地 API；服务端若不校验 Host，这次请求与正常本地请求无异 ⇒ **攻击者网页可驱动本地 Agent**（读文件 / 执行命令）。**回环绑定挡不住这条路**（请求确实是打向 127.0.0.1 的）。**修**：① `server/security.ts` 新增纯函数 `normalizeHostname()`（去端口 / IPv6 去方括号 / 小写 / 去 FQDN 尾点 / 畸形判空）与 `isAllowedHost()`（白名单判定·空与畸形一律判否·fail-closed）；② `server/config.ts` 新增 `ALLOWED_HOSTS`（默认只认回环三形态 127.0.0.1 / localhost / ::1，`AGENT_WEB_ALLOWED_HOSTS` 为**追加**项）；③ `server/middleware.ts` 新增 `hostGuard` 关卡，挂载序=request ID → **Host 校验** → 限流 → 安全头 → 可选鉴权（不在白名单即 403，**不进限流桶、不触达任何路由**；响应体沿用既有 AppError 契约 `{ error: <文案> }`，前端契约零改动）。**端口不参与判定**（与 Django ALLOWED_HOSTS 同口径）：dev proxy（changeOrigin 改写 Host 为代理目标）、随机端口测试、Electron 桌面端都是同主机名不同端口，判端口会误伤。
> - **缺陷②（token 口径无法硬化）**：`AGENT_WEB_TOKEN` 未设时 `/api/*` 免认证，此前**没有任何强制手段**——用户想「必须带 token」时只能靠自觉，进程不会拒绝在免认证模式下跑起来。**修**：① `AGENT_WEB_REQUIRE_TOKEN=1` 时若未设 `AGENT_WEB_TOKEN` 则**拒绝启动**（fail-closed·不静默降级为免认证）；② 未设 token 时启动记 WARN 并报当前暴露面与加固指引。**口径未改**：W808 固化的「无 CORS 中间件 + 回环绑定 + 可选 token + 限流」防护模型保持不变（本批只加严、不加面），对外契约（路径/字段/状态码）零变化。
> - **自测当场抓出实现缺陷（负样本自证）**：`normalizeHostname` 初版按「首个冒号」截断端口，把白名单里的**裸 IPv6 `::1`** 归一化成空串 ⇒ `[::1]:3000` 反被判否——**实现比判据先错**；改为按冒号个数判定（恰一个才截端口·两个及以上视为裸 IPv6 整体保留）后通过。教训：白名单里同时存在「带端口形态」与「裸 IPv6 形态」时，端口剥离规则必须按形态判定，不能按「第一个冒号」这种位置判定。
> - **验证**：`npm run test:server` **82 例 / 81 通过 / 0 失败 / 1 跳过**（既有 skip）· 集成测试 20 例 / 19 通过 / 0 失败 / 1 跳过 · `tsc --noEmit` **0 错** · 端到端 **11 通过 / 0 失败**（真实后端 + 真实前端代理链路未被打断）· 真起服负样本：`Host: evil.com` / `evil.com:3213` / `127.0.0.1.evil.com` 均 **403**，`127.0.0.1:3213` 与 `localhost:3213` 均 **200**；`AGENT_WEB_REQUIRE_TOKEN=1` 且未设 token → **退出码非 0 且打印拒绝原因**。
> - **状态**：已落地（本地提交·未推送）。CHANGELOG 版段因顶段序约束（batch 必须等于顶段+1·当前顶段为 W826·W827 至 W834 的段均待补写）**递延**，待顶段推进后以 chore 批补写十面；本批内容与认领行已入库。

### W836（2026-10-20）：品牌字面量零命中守卫批（归档检测器活面复活 + 三处品牌回退修复 + CI 挂载）

> **来源**：2026-10-20 全项目只读审查（归档面存活性）所得的 N2 项 + 用户 2026-10-20 对禁令范围的确认（三枚品牌字面量均在禁令范围·不在允许品牌之列）。
> - **文件**：scripts/check_no_brand_refs.py（新建）、.github/workflows/security.yml、scripts/gen_folder_docs.py、docs/11-方案报告/计划方案/执行前计划-T05-取经编制表落库与编制位补全.md、archive/scripts/batches/misc/_audit_agentweb_baseline.py、docs/00-导读/W批次编号对账表.md、scripts/output/_w836_spec.json、scripts/index.md、scripts/README.md、scripts/output/index.md、scripts/output/README.md。
> - **缺口（为何需要机器防线）**：W812/W814 两批把三枚品牌字面量从全仓清零，**验收方式是人工终扫**——仓内没有任何机器防线。与此同时，仓里唯一一处「品牌字面量扫描器」是归档件 `archive/scripts/batches/misc/_audit_agentweb_baseline.py`：它在归档后仍按「脚本所在目录上溯两级」计算 ROOT ⇒ ROOT 落到 `archive/scripts`（应为仓库根·上溯四级）⇒ 第 31 行读 `archive/scripts/xiyouji-agent-web/…` 直接抛错，**第 110 行的品牌扫描段永不可达**。于是「品牌回归」既无扫描器也无防线：**后写的文档把字面量带回来也没人拦**。
> - **实测回退（守卫不是空跑）**：W831 会话新引入的点开头会话运行态目录名（含被禁字面量）出现在 `scripts/gen_folder_docs.py` 与计划件 T05 中——全仓明文命中 **6 行 / 4 文件**（「全仓归零」状态已被回退）。
> - **修①（活面守卫·N2 的「复活到活面」路径）**：新建 `scripts/check_no_brand_refs.py`——① **字面量以 base64 存储**（运行时解码）：禁令要求的是「全仓明文 0 命中」，守卫若明文写出被禁字面量即自己违规；编码后明文扫描仍为 0，而守卫依旧能检出回归；② **扫描面 = git 已跟踪文件**（含 `archive/**`；未跟踪的会话运行态目录与本地临时产物不入库·不进判定面）；③ **fail-closed 且退出码分流**（0=零命中 · 1=有命中 · 2=判据未执行：字面量解码失败/扫描面为空/git 不可用）——沿用 W816 引文门禁的 1/2 分流口径；④ `--self-test` 合成样本自检（正例**由解码结果在运行时派生**，避免探针硬编码导致守卫自指违规；反例覆盖允许品牌与允许的中性标识）。
> - **修②③④（三处明文回退）**：`scripts/gen_folder_docs.py` 去掉逐名列举，改为**排除全部点开头的顶层目录**（既去字面量，又对未来新出现的同类会话运行态目录免疫）；计划件 T05 的路径引用改为不落明文；归档检测器移除其**已成空转**（被扫依赖随 W812/W814 退役而消失）且**自身含被禁字面量**的品牌扫描段，并注明检测能力已由活面承接——**归档件其余部分按文档规范 §11.2 不回溯修复**（其 ROOT 层级错配仍在归档态存在·需要的检测能力一律走活面）。
> - **修⑤（CI 挂载·机器防线成形）**：`.github/workflows/security.yml` 新增 `brand-refs` 作业（跑扫描 + 跑 `--self-test` 复核：守卫本身瞎了即阻断）——**不挂 `verify_delivery.py`**（管控件·CLAUDE.md 第 10 条须用户批准才改）。
> - **守卫当场抓出我方自伤两处（如实记账）**：① 我在 `gen_folder_docs.py` 的注释里**写出了明文字面量**（3 处命中）——守卫上线即报；② 自检探针若硬编码字面量，守卫**入库后会把自己判红**（自指违规）⇒ 探针改为由解码结果在运行时派生。两处均已修。
> - **验证**：`--self-test` **32/32 通过** · 全仓扫描 **0 命中**（**3897 个已跟踪文件·含 archive/**）· 把未跟踪的新文件一并计入后**仍 0 命中**（模拟入库后状态）· 退出码分流 0/1/2 逐条自检通过。
> - **状态**：已落地（本地提交·未推送）。CHANGELOG 版段因顶段序约束（batch 必须等于顶段+1·当前顶段为 W826·W827 至 W835 的段均待补写）**递延**，待顶段推进后以 chore 批补写十面；本批内容与认领行已入库。

### W837（2026-10-20）：并发实况沉淀批（部分提交临时索引 + index.lock 全程持锁 + C5b/C5d 互锁 + 管道 BOM + 守卫自指）

> **来源**：2026-10-20 全项目只读审查的落地过程（W833/W835/W836 三批）——并行交付在共享工作区里暴露的五条可复算坑位，均已沉淀进 `docs/agent/pitfalls.md`「git / 提交 / 并发」段（12 → 17 条）。
> - **文件**：docs/agent/pitfalls.md、docs/00-导读/W批次编号对账表.md、scripts/output/_w837_spec.json。
> - **沉淀①（部分提交的钩子跑在临时索引上）**：`git commit -- <pathspec>` 构造临时索引（HEAD + 本次 pathspec 的工作树内容）供 pre-commit 钩子使用 ⇒ 并行会话已暂存未提交的件在钩子视角下成为「工作树未提交残留」；若该件在现役顶段「文件」行内，第 31 门禁 C4-f 即判红——**与本批无关的假红**（手动跑同一门禁为绿·两者结论相反即识别判据）。解法：把该件纳入本次 pathspec，或先请他方落库；禁为此改门禁。
> - **沉淀②（index.lock 被钩子全时长持有）**：并行会话提交期间 `index.lock` 存在数分钟 ⇒ 另一会话的提交报 `Unable to create index.lock`。活锁不删（有 git 进程就等）；确认无 git 进程后残留锁方可清理。
> - **沉淀③（C5d 与 C5b 互锁）**：stats.json 刷新后，实体标记（`<!--stats:KEY-->` 形态的数字）必须同步，否则 C5b 反向判红；不刷新 stats.json 则 C5d 判红——两侧互锁，改任一侧后两侧都要刷。
> - **沉淀④（PowerShell 管道加 BOM）**：`Get-Content x | py -3 script.py` 传入的行首带 U+FEFF ⇒ 台账行成为 `U+FEFF| W### | …` ⇒ C4 登记正则不匹配 ⇒ 判「未在对账表登记」红且明面不可见。登记行必须以文件直写传入。
> - **沉淀⑤（守卫不能把自己判红）**：被禁字面量守卫的字面量以 base64 存储运行时解码；自检的正例探针由解码结果在运行时派生（硬编码会让守卫入库后自指违规）。守卫上线后先跑自身扫描——它会当场报出你刚写下的字面量。
> - **验证**：pitfalls.md 段计数 12→17（5 条新条目）· 行首 BOM 清理（见 W835 批记账）· 门禁核心全部通过。
> - **状态**：已落地（本地提交·未推送）。CHANGELOG 版段因顶段序约束递延，待顶段推进后以 chore 批补写十面。

### W838（2026-10-21）：取经编制表勘误批（V1.1a·自查脚本正则/指针面计数/附录时点行/交叉引用/术语）

> **来源**：用户令审查取经编制表文档（三性标准：符合实际/量化/可验证）+「开始」批准修复。
> - **文件**：docs/11-方案报告/取经编制表-工具与技能挂位-2026-10-20.md、scripts/output/_w838_spec.json、scripts/output/index.md、docs/00-导读/W批次编号对账表.md。
> - **审查结论**：文档整体高质量——抽验 12 项事实断言全过（615/857/87/46 与 stats 一致·5 个 MCP 工具脚本在位且工具名对·fastmcp 未装·块引原文引文 15/15 逐字命中语料·碎片模式小 max-len 静默失败声明精确复现·被引 tmpe/archive 契约文件全在位·17 位分组自洽）；问题集中于可验证口径与量化数字。
> - **勘误①（必修·可验证硬伤）**：§6.2 引文自查脚本正则 `「([^」]+)」` 过宽，把全文 75 处强调引号计入「引文」——实跑 94 条 vs 命中 19，按本节自写判据（命中数==引文条数）**在自己的文档上不过**。真实原文引文（块引 15 条）15/15 全命中，实质无误、发布口径错。修正为 `^> 「([^」]+)」`（re.M 块引限定），实跑复验 **15 15** 通过，并将勘误缘由留档节内。
> - **勘误②（必修·量化失实）**：「旁文档指针面」三处口径互不相容（§3.1/§3.2 写 9 处、§5 列举 14 项），实证为 batch_cascade 实际改写 **13 个文件**（9 文档面 + 4 站点页脚·W823 提交记录同载 13 面）。三处统一订正为 13 处并给出分解，§5 列举补齐缺失的 AGENTS 与 workflows README、删除臆造的 HANDOVER×4。
> - **勘误③（应修）**：附录 A 两条数据来源行停留 V1.0 时点（「15 位编制位」现 17 位、「10 组回目锚点」口径不明）→ 更新为 17 位（含丁组 2 位）与 13 位有回目锚点（4 位无：孙悟空/千里眼·顺风耳/红孩儿〔未获批〕/牛魔王），取值时间标 W838 勘误复核。
> - **勘误④（应修）**：行 13 交叉引用「原因见 §6.4」实为 §6.5（§6.4 是归档工地复现）→ 已改。
> - **勘误⑤（小瑕）**：§5「第 31 门禁（C5b）」条目混同 C4（提交-版段对账）与 C5b（标记对账）→ 拆为「C4 + C5b」双标签并分工描述，同时补注 W830 起的 C5b 扩展面（11-方案报告根层 + pytest.ini）。
> - **版本处理**：文档升至 V1.1a（编制位内容零变化·纯勘误），版本行与状态行同步标注。
> - **数据边界留档**：审查过程中一度枚举用户 profile 下 `.minimax` 目录，应用户令「不用 .minimax 文件里面的所有内容」全部弃用，由其派生的「技能目录状态」一条结论已撤回、改列不可验（文档引用该路径的复现命令只审写法不代执行）；边界规则已入用户级记忆。
> - **验证**：修正后 §6.2 脚本实跑 15 15（判据在自己的文档上通过）· doc-sync 0 FAIL · 全量 verify 核心全部通过 · 无残留旧值（9 处/§6.4 引用均为 0）。
> - **状态**：已落地（本地提交·未推送）；CHANGELOG 版段递延（顶段序约束·spec 已入库）。

### W839（2026-10-21）：fail-closed 跳过路径回归修复批（_gate_a11y 对 _SkipResult 误判红 + 2 例回归锁）

> **来源**：W838 收官 chore 提交时被 a11y 段拦截（「审计输出不可解析」）→ 根因定位为 W834 B2 修复自身引入的回归 → 用户「继续」推进下修复。
> - **文件**：scripts/verify_delivery.py、tests/unit/test_verify_failclosed.py、pytest.ini、scripts/output/stats.json、scripts/output/stats-changelog.json、scripts/output/stats-index.md、scripts/output/_w839_spec.json、scripts/output/index.md、docs/00-导读/W批次编号对账表.md。
> - **回归机理**：_GateContext 把全局 subprocess.run 猴补为 _scoped_run——scope 跳过时返回 _SkipResult（returncode=0·stdout=「（--scope X 跳过）」提示串，跳过行已由其打印）。W834 的 _gate_a11y 改 fail-closed 后对该伪造结果继续走 json.loads → 提示串在 char 0 即失败 → 判「审计输出不可解析」→ **docs 档（auto scope）提交必红**；全量档不受影响（a11y 真跑）。
> - **实证**：W838 收官 chore 两次被拦；`--scope auto` 实跑显示「OK 跳过 [a11y对比]」后紧接一条 FAIL（同一段双消息）；同形 subprocess 手动复跑两次均正常（3.1M 字符合法 JSON）——排除瞬态，确认为跳过路径回归。
> - **修复**：_gate_a11y 在 rc 检查前加 `isinstance(r, _SkipResult)` 守卫——跳过不是「判据不可执行」，直接返回、不重复上报；真实路径（rc/解析/结构检查）语义零变化。
> - **回归锁**：新增 2 例——① _SkipResult 注入 → 零 fail 零 ok 零 warn（不得判红、不得重复上报）；② 简单委托段收到 _SkipResult → 走既有 rc=0 OK 路径不判红（旁证既有 W698 双行噪声非故障）。pytest 收集 783→785。
> - **验证**：test_verify_failclosed 14 passed；`verify_delivery --scope auto` 原必红场景转绿（a11y 真跑通过）；doc-sync 0 FAIL；ruff 净；stats --w W839 刷新（pytest_collected 783→785）；pytest.ini 标记同步；全量 verify 核心全部通过。
> - **状态**：已落地（本地提交·未推送）；CHANGELOG 版段递延（顶段序约束·spec 已入库）。

### W840（2026-10-21）：pitfalls 坑位沉淀批（fail-closed 跳过路径入查坑表 + AGENTS §4.3 计数校准 41→47）

> **来源**：用户令「加」——W839 收官后我提出该坑值得进仓内查坑表（凡改 bespoke 门禁的人都会撞上一次），用户批准。
> - **文件**：docs/agent/pitfalls.md、AGENTS.md、scripts/output/_w840_spec.json、scripts/output/index.md、docs/00-导读/W批次编号对账表.md。
> - **新增条目（第 47 条·流程/协作/取证 7→8）**：「把 subprocess 输出解析改成 fail-closed 前，先识别 scope 跳过的伪造结果」——根因=_GateContext 把全局 subprocess.run 猴补为 _scoped_run，--scope 不覆盖某段时返回 _SkipResult（rc=0、stdout 只有跳过提示串，消息已由其自打印）；事故=W834 把 a11y 段改 fail-closed 后提示串被送 json.loads → 判「输出不可解析」→ docs 档提交必红而全量档全绿（W838 收官两度被拦）；判据=同一次 --scope auto 同段打出「OK 跳过」+「FAIL 判红」双消息，且绕过 monkeypatch 手动复跑两次均正常（排除瞬态）；修法=rc 检查前 isinstance(_SkipResult) 守卫直接 return（跳过不是判据不可执行·不重复上报），回归锁 2 例；同族口径=凡 bespoke 段自行 parse subprocess 输出（json/正则/结构），改 fail-closed 时必须先过此守卫。
> - **附带校准（既存漂移·非本批引入）**：AGENTS.md §4.3 两处计数——「41 条坑位」改 47；六主题目录 git/提交/并发 12 改 17（W837 沉淀五条时只改 pitfalls 节标题、未同步本行）、流程/协作/取证 7 改 8；括注补 W840 校准事实。
> - **验证**：脚本实跑各节计数 9/5/17/4/4/8 = 47，与六节标题声明值逐节相等（0 节不一致）；git diff 3 文件 6 增 3 删（无 Edit 吞行）；doc-sync 0 FAIL；全量 verify 核心全部通过（51 段）；提交后 docs 档 pre-commit 核心全部通过。
> - **状态**：已落地（本地提交·未推送）；CHANGELOG 版段递延（顶段序约束·spec 已入库）。

### W841（2026-10-21）：版本行分隔符兜底门禁批（check_doc_sync C6 + 自测 22 增至 24 例）

> **来源**：用户令「写」——W827 施工中撞上「三处版本行锚点全失配、任何批都级联不了」，追根因后提出的守卫，用户批准落地。
> - **文件**：scripts/check_doc_sync.py、scripts/output/_w841_spec.json、scripts/output/index.md、docs/00-导读/W批次编号对账表.md。
> - **缺陷链条**：W826 批 desc 含「·」→ 三处版本行（README `·A1-A6` / STRUCTURE `—A1-A6` / 项目说明 `·详细变更见`）锚点正则全部失配 → 后续任何批无法级联落段。W827 施工时把三处 · 改为 、后十面断言立即全过，坐实因果。
> - **关键查明（纠正了一个错误判断）**：batch_cascade.py 的 precheck() **早已存在且 fail-closed**（desc 禁 · ； —，违例 return 1）。W826 漏网的原因是它**没走 batch_cascade**——output 下只有三个 _w826_*.py 审计脚本、没有 _w826_spec.json，段为手工写入，precheck 从未被调用。所以真缺口是「手工写段无兜底」，不是 precheck 缺失。
> - **落地**：check_doc_sync.py 新增 **C6 版本行 desc 分隔符体检**——对三处版本行取 desc 段（先截掉已知尾锚点）断言不含 · ； —；文档非空但版本行形态不识别按 FAIL 计（形态变更会让本支静默失效，这是 W813「滤除即不被校验」同族）；空文档跳过（合成输入场景）。版本行是 desc 的唯一落点，扫它即可覆盖手工路径。
> - **回归锁**：自测 22 例增至 **24 例**——T23 负样本（desc 含 · 必红）、T24 正样本（三面均用「、」分隔须放行，防误伤）。另用四组真文件注入验过：README/STRUCTURE/项目说明三面分别含 · / — / ；均判红，形态不识别亦判红。
> - **验证**：`--self-test` 24/24 通过；ruff 净；check_doc_sync 实跑 0 C6 FAIL（真实文件三面均干净）；全量 verify 核心全部通过；段自洽锁 51 段不变（未改 verify_delivery.py 结构）。
> - **状态**：已落地（本地提交·未推送）；CHANGELOG 版段递延（顶段 W827·W828 缺口未补·spec 已入库）。

### W842（2026-10-21）：CHANGELOG 递延补段工具批（backfill_changelog.py + 12 批欠账一次补齐）

> **来源**：用户令「现在解决」——W830 起版段递延链卡死十二批，CHANGELOG 顶段停在 W827，此后所有批只能「内容先落 + spec 入库 + 递延登记」。用户要的是结构性解法，不是先补 W828 的功能四项再回头收拾。
> - **文件**：scripts/backfill_changelog.py、scripts/output/_w842_spec.json、CHANGELOG.md、scripts/output/file-index.md、scripts/output/index.md、scripts/output/_cascade_files_W842.txt、pytest.ini、scripts/output/stats.json、README.md、STRUCTURE.md、docs/00-导读/项目说明.md、HANDOVER.md、AGENTS.md、CITATION.cff、.github/workflows/README.md、docs/00-导读/W批次编号对账表.md、scripts/check_script_coverage.py、scripts/output/script-coverage-baseline.txt、scripts/index.md、scripts/output/README.md。
> - **根因（两条叠加，先后查明）**：① **号序缺口 W828**——batch_cascade 断言 `batch == 顶段+1`，W828 没立段则顶段恒为 W827，W829 起任何批都过不了断言；② **W826 desc 含「·」**致三处版本行锚点（`·A1-A6` / `—A1-A6` / `·详细变更见`）全部失配，连「本该能落的那一批」也落不下（W827 施工时撞上并把三处 · 改为 、，十面断言随即全过，坐实因果）。②修好后 W827 立段成功，但①仍在，W830-W841 十二批继续积压。
> - **落地**：新建 `scripts/backfill_changelog.py`，两阶段设计——① **补段**：按降序把待补批插到「第一个号小于自己的段」之前（`insert_before_smaller`，找不到锚点直接 AssertionError 拒绝执行，防高号误走补段路径绕过正常级联）；② **当前态同步**：补完顶段号变了，README / STRUCTURE / 项目说明三处版本行、HANDOVER 交接头、workflows README、AGENTS 版本脚注、CITATION、四页脚必须跟着走，否则 C1（README 抬头 ≡ 顶段）当场红——故 `--refresh-current` 直接复用 batch_cascade 的六个 `_face_*` 函数，把「现在是什么」这一层推到新顶段。
> - **落盘前全量断言（fail-closed）**：段数 = 补前段数 + 待补数、W 号严格降序、无重复号、每段标题锚点唯一、file-index 段数与序同 CHANGELOG——任一不过即零落盘。
> - **本次实跑**：CHANGELOG 127→**139** 段、file-index 127→**139** 段、规则 `W001-W827`→`W001-W841`；当前态同步 11 面（六函数 + 落盘清单 `_cascade_files_W841.txt`）。**号序链恢复**：顶段 W841，本批 W842 起回到 batch_cascade 正常级联，补段工具从此只作应急。
> - **顺手修真漂移**：`stats.py` 实算 pytest 收集数 785→**786**——W839 收官刷新时少记一例（该批 CHANGELOG 原文写「783→785」，与磁盘实算不符，且 C5b 因两边同为旧值而假绿）；pytest.ini 头注标记同步 785→786。
> - **验证**：check_doc_sync 0 FAIL（C1 README 抬头 ≡ W841、C2 交接头链、C4 提交-版段对账、C5d stats 实算、C6 版本行分隔符全绿）；`stats.py --w W842` 刷新 1 键；补段段数/降序/锚点断言全过。
> - **状态**：已落地（本地提交·未推送）；W830-W841 十二批台账「CHANGELOG 版段」列由「递延」翻「已立段」。

### W843（2026-10-21）：pitfalls 增补批（第 48 条 desc 内嵌 W 号 + 第 49 条双源同旧值假绿）

> **来源**：用户令「继续做完」——W842 收尾时我提了两条建议，第一条是「先写个小批把今天新踩的坑固化进 pitfalls」，用户批准按此顺序推进。
> - **文件**：docs/agent/pitfalls.md、AGENTS.md、docs/00-导读/W批次编号对账表.md、scripts/output/_w843_spec.json、scripts/output/_cascade_files_W843.txt。
> - **第 48 条（级联 / CHANGELOG 节 · 4→5）**：`spec` 的 `desc` 禁含**内嵌** W 号。`_face_footers` 把 `desc` 拼进四页脚批次链（`f"{ctx.batch} {desc}"`），`_foot_insert` 末行断言 `len(_wns) == len(set(_wns))`。W781 建的剥离防线只有 `re.sub(r"^W\d{3}\s*", "", desc)`——**只治行首**。W842 首版 desc 写「补段工具一次补齐 W830 到 W841 十二批欠账…」，链上已有的 W841 与 desc 里的 W841 撞，`batch_cascade` dry-run 直接抛 `AssertionError: 页脚链 token 重复（W724 防线）`。改法 = desc 用不含 W 号的量词表述，批号引用移到 `changelog_body`（body 不进链）。
> - **第 49 条（数据 / 内容可信度节 · 4→5）**：双源互锁在两侧都停在旧值时**必然假绿**。C5b 比对 `pytest.ini` 标记与 `stats.json` 值，C5d 才是 `stats.json` 与磁盘实算。W839 收官刷新少记一例（该批正文写「783→785」而实算 786），C5b 因为两边都是 785 而一路绿，直到 W842 跑 `stats.py --w` 触发 C5d 才照出来。结论：**标记↔缓存的对账只能证明两者彼此一致，不能证明它们与事实一致**，凡存在实算源就必须让实算支路常驻门禁。
> - **同批校准 AGENTS §4.3**：坑位总数 47→**49**、级联节（4）→（5）、数据节（4）→（5），并在计数口径注里补 W843 一行说明。这不是形式主义——W840 刚实证过「沉淀时只改 pitfalls 节标题、不改本行」会让总数静默漂移。
> - **实跑校准**：计数脚本按 `^### ` 切节、按 `^- \*\*` 数顶层条目，得 9/5/17/5/5/8 = **49**，与六个节标题、与 AGENTS 本行三者自洽。
> - **顺带**：台账「现势下一自由号」bullet 从 W827 轮换到 W843——preflight 的 WARN「现势 bullet 与 max+1 不衔接」由黄转 NOTE。
> - **验证**：check_doc_sync 0 FAIL；全量 verify 核心全部通过（51/51）；ruff 净；目录文档新鲜度 0 FAIL。
> - **状态**：已落地（本地提交·未推送）。

### W844（2026-10-21）：系统架构批四项落地（会话库备份 + 首 token 计时 + 两项裁决回填 + 检索题集入仓）

> **来源**：用户令「继续做完」。原 W828 批（2026-10-20 用户批「可以」的 Q1/Q3/Q4/OBS-14 四项）因当时 CHANGELOG 号序链断裂（W828 缺口）始终无法级联立段，内容一直停在备料件。W842 修复号序链后，本批以新号 W844 承接落地。
> - **文件**：xiyouji-agent-web/server/backup.ts、xiyouji-agent-web/server/backup.test.ts、xiyouji-agent-web/server/metrics.ts、xiyouji-agent-web/server/metrics.test.ts、xiyouji-agent-web/server/db.ts、xiyouji-agent-web/server/index.ts、xiyouji-agent-web/server/chat.ts、xiyouji-agent-web/server/routes.ts、xiyouji-agent-web/package.json、docs/agent/agent-web.md、docs/11-方案报告/系统架构方案-分层模块与部署-2026-10-20.md、scripts/rag/eval/queries_30q_frozen.jsonl、scripts/rag/eval/queries_100q.jsonl、scripts/rag/eval/make_queries.py、scripts/rag/eval/eval_retrieval.py、scripts/rag/README.md、scripts/output/rag_eval_report.md、scripts/output/_w844_spec.json、docs/00-导读/W批次编号对账表.md。
> - **Q1 会话库备份**：`chat.db` 是全仓唯一不可重建的数据（gitignored 且无备份）。新增 `server/backup.ts`——用 `VACUUM INTO` 生成一致性快照（**禁文件拷贝**：库有 WAL 伴生文件，只拷主文件会丢最近未 checkpoint 的提交）；备份两件（库快照 + 审计日志副本）、每日一份、留 7 份、清 90 天；份数与天数两条件**独立取并集**（备料件首跑曾把超龄判断嵌进「仅在超份数时才查」，致 90 天规则实际失效）；落点仓外 `%LOCALAPPDATA%\xiyouji\backups\`（`XIYOUJI_BACKUP_DIR` 可覆盖）；年龄以文件名日期为主、mtime 兜底；幂等跳过时仍执行清理。挂载在 `listen` 回调，**失败只记日志不阻断启动**，`NODE_ENV=test` 跳过。回归面 9 例。
> - **OBS-14 首 token**：`/api/chat` handler **最前**取 `reqStartedAt`（入参校验与会话读写也属用户等待，靠后计时会系统性低估），首个 text delta 记 `firstTokenMs` 并打结构化日志；整轮无文本增量时记 `reason: no_text_delta`，**不把缺样本当 0 ms**。新增 `server/metrics.ts`（滚动 100 样本·最近秩法 p50/p95·脏数据丢弃）与 `GET /api/metrics` 只读端点，不落盘不外发。回归面 7 例。
> - **Q3 多租户不预加**：三条触发条件写死（第 2 个真实使用者 / 需按用户导出删除 / 会话数超 5,000）+ 提前记账的代价清单（三表改 schema、查询路径加 WHERE、老数据归属规则等约 1 批工作量），回填 §8.2 档 2 与 §12.2 Q3。
> - **Q4 检索维持现役 + 评测集入仓**：30 题冻结集**逐行原样**迁入（与原件字节一致·sha256 `8d9385b5…`），另由 `make_queries.py` 按文档标题锚点派生 70 题（gold 由脚本解析·只认索引内文档），合计 100 题；`eval_retrieval.py` 为复算入口，出 `scripts/output/rag_eval_report.md`（总表 + 题源分组 + 题型分组 + 逐题明细 + 口径局限）。
> - **一处必须纠正的旧结论**：备料件写着「dense 仅 +0.003，不成立」。复算后 off 档 100 题 recall@5 = 0.573、frozen 30 = 0.382、dense = 0.712 / 0.446——增益远大于 +0.003。查明原因是历史数字跑在 T-01 冻结索引（1,077 篇）上，与现役索引（768 篇）语料面不同，**不可互引**。故「dense 无增益」论据作废，**默认档仍为 off，但理由换成成本与可移植性**（四重依赖 + 约 96 MB 模型 + 124 MB 产物、离线不可复算），并把「dense 是否升为可选档」登记为**新开放项 Q5** 交用户裁决。体积口径按实测值写，未用估算。
> - **验证**：`npm run test:server` 98 例中 97 通过（唯一失败 W817-C2b 为**本机环境限制**：沙箱下 `fs.symlinkSync` 不抛错也不建链，用例前置假设不成立，CI 为 Linux 必执行面；该文件本批未改动）；`tsc -b` 零错误；`make_queries --check` 一致；ruff 净；`eval_retrieval` 4.3 s 跑完 100 题。
> - **状态**：已落地（本地提交·未推送）。

### W845（2026-10-21）：阅读页重建影响面量化批（W829 前置门槛实测 262 行）

> **来源**：用户令「继续」。候选批 W829（阅读页体验封装）在计划里留了一道前置门槛（AC-21）：重建 diff ≤ 2000 行才允许进入施工。本批把这道门槛实测掉，同时纠正量法本身。
> - **文件**：docs/11-方案报告/计划方案/执行前计划-T04-站内阅读入口打通与阅读页体验封装.md、docs/00-导读/W批次编号对账表.md、scripts/output/_w845_spec.json。
> - **口径纠正（本批最有价值的产出）**：计划原写法是「临时副本试跑 `build_reader.py` 量 diff」。实测单跑这一步得到 **122,366 行**（622 页全变）——因为 reader 页现状是三段管线的产物，只跑第一步会把已内联的 CSS（`tokens.css` + `system.css`）与 CSP meta 全部剥掉，等于拿「少了两道后处理」当「内容漂移」。正确量法是 `build_reader.py` → `inline_css.py` → `generate_csp.py` 三段跑完再比。**按旧口径执行会直接假红（12.2 万 > 2000），把一个本来可做的批挡在门外。**
> - **实测**：隔离副本 43 MB（六板块源 + reader 基线 + 三脚本 + 两份 CSS，不复制 1.1 GB 的 `docs/S4-学术投稿`）按三段管线重建 622 页，逐文件比对得 **51 文件 · 131 增 131 删 · 合计 262 行**，占 622 页的 8.2%，距阈值一个数量级余量。
> - **漂移性质（比行数更有价值）**：51 处全是正文文字差异（头防→头陀、般苦→般若、锡枚→锡杖、盂兰盆会、迦叶 等），即 `docs/` 源的字级修复（W763 那批 97 处）从未回灌到 reader 页。分布 people 28 / themes 13 / 回目 10。**mtime 新不等于内容新**：这些页 2026-10-20 被 W806 为删埋点机械改过，mtime 比源新，正文却停在 10-16 之前。
> - **幂等与收尾**：三段连跑两次 → 二次 diff = **0**，AC-25 的生成侧风险先行证伪；副本内 `generate_csp.py --check` 报 622 页 0 漂移。
> - **结论**：AC-21 达标（262 ≤ 2000），W829 可进入施工。副产品：全量重建会顺带把 51 页正文拉回与源一致——这不是纯改造，也是一次欠账清偿。
> - **未做**：未改 `site/reader` 任何一页（W829 未获批）、未动生成器、未推送远端。
> - **验证**：`check_doc_sync.py` 0 FAIL；`verify_delivery.py --scope full` 核心全部通过；页数四项（88/138/622/9）零漂移。
> - **状态**：已收官。

### W846（2026-10-21）：阅读页正文回灌批（三段管线重建·字级修复回灌 51 页）

> **来源**：用户令「开工全部做完」。W845 已把这道前置门槛实测掉（重建 diff 262 行 ≤ 2000），本批按「先回灌、后改造」的拆法落地第一步：只把正文拉回与源一致，不碰生成器逻辑。
> - **文件**：site/reader/ch008.html、site/reader/ch009.html、site/reader/ch010.html（代表页，全部变动页见本批 git diff）、scripts/output/_w846_spec.json、docs/00-导读/W批次编号对账表.md。
> - **做了什么**：在真仓按 `build_reader.py` → `inline_css.py` → `generate_csp.py` 三段一次跑通，重建 622 页。逐文件比对结果与 W845 副本实测完全一致——**51 文件 · 131 增 131 删 · 262 行**，无新增页、无删页、无结构变化。
> - **变动内容**：全是正文文字层面的字级修复回灌（头防→头陀、般苦→般若、锡枚→锡杖、盂兰盆会、迦叶 等），即 `docs/` 源早已改好、reader 页一直没重新生成的那批欠账。分布 `people/` 28 页 · `themes/` 13 页 · 回目 10 页。
> - **为什么不只跑渲染脚本**：单跑 `build_reader.py` 会把已内联的 CSS 与 CSP meta 全剥掉，制造十二万行假 diff（W845 附录 C 实证）。三段管线的顺序也不可颠倒——CSP 哈希基于内联后的脚本内容。
> - **验证**：`generate_csp.py --check` 856 页 0 漂移；`stats.py --check` 17 键零差异（页数四项 88/138/622/9 不变）；`check_doc_sync.py` 0 FAIL；`verify_delivery.py --scope full` 核心全部通过。
> - **未做**：未改 `build_reader.py` 任何逻辑（折叠/进度/字号/反馈属 W847）、未动 `docs/` 源、未推送远端。
> - **状态**：已收官。

### W847（2026-10-21）：阅读页体验封装批（速览折叠 + 进度书签字号 + 每页反馈 + 幂等复验）

> **来源**：用户令「开工全部做完」。W846 已把正文回灌做完，本批落地 W829 的体验封装本体四项（计划 AC-22~25）。
> - **文件**：scripts/build_reader.py、site/js/reader-enhance.js、site/reader/、docs/11-方案报告/计划方案/执行前计划-T04-站内阅读入口打通与阅读页体验封装.md、scripts/output/_w847_spec.json、docs/00-导读/W批次编号对账表.md。
> - **AC-22 速览/深读折叠**：生成器把「剧情梗概 / 深度解读 / 原文全文」三段包进 `<details>`，折叠态只留一行标题；工具条加「展开全部 / 收起全部」一键切换。**为什么是三段不是两段**：只折 AC 字面的两节时，100 页实测折叠态高度平均仍有 84.2%、仅 17/100 达标——原文全文独占正文约 48.9%，不折它页面降不下来。加折原文后平均 45.1%、中位 40.2%、≤60% 达标 77/100。
> - **AC-22 阈值如实记账（部分达标）**：仍有 23 页超 60%（最差 81.3%）。根因是这些页的深读内容不是单节，而是拆成多条独立 H2 分节（如「八、最后一个晨」占 27%），不在折叠集合内。要 100/100 达标须把「一、」到「九、」的分节也折叠，那样速览页会变成一排折叠条——本批不做，实测分布留档待按读者反馈再调。
> - **AC-23 进度/书签/字号**：新增 `site/js/reader-enhance.js`（ES5 IIFE·零依赖·零外域）。三键 `reader.progress`（每页滚动百分比 map）/ `reader.bookmark`（收藏页清单）/ `reader.fontsize`（15–21px），顶部 3px 进度条实时反映位置；页面标识取生成器写入的 `data-page`，不用 `location.pathname`（后者在 file:// 与 http:// 下形态不同，会让同一页进度互不认）；localStorage 不可用时静默降级为无状态，不抛错。
> - **AC-24 每页反馈**：文末「这页有帮助吗？」👍 / 👎 两条纯 `<a>`，跳 GitHub Issue 新建页并预填标题（含回目名）与正文（含页面 canonical URL），零外域脚本。
> - **AC-25 幂等**：改造落地后在真仓连跑两次三段管线，二次 diff = **0 文件**。
> - **验证**：Playwright 17 项交互断言全过（三键写入/刷新保持/跨页保持/字号生效/进度恢复/进度条宽度/展开全部），http 与 `file://` 双环境均可用；`generate_csp.py --check` 856 页 0 漂移；`stats.py --check` 17 键零差异（页数四项 88/138/622/9 不变）；`node --check` 通过；`check_doc_sync.py` 0 FAIL；`verify_delivery.py --scope full` 核心全部通过。
> - **未做**：不动 `docs/` 源、不加外域请求、不推送远端。
> - **状态**：已收官。

### W848（2026-10-21）：Q5 裁决落档批（dense 升为显式可选档·默认仍 off）

> **来源**：用户裁决 Q5——dense 档升为显式可选档、默认仍 off。W844 把「dense 增益到底真不真」量清楚了，本批只做落档：把裁决写进人真正会读到的地方。
> - **文件**：scripts/rag/README.md、scripts/rag/build_vectors.py、docs/11-方案报告/系统架构方案-分层模块与部署-2026-10-20.md、scripts/output/_w848_spec.json、docs/00-导读/W批次编号对账表.md。
> - **代码侧本来就绪**：`RAG_ENHANCE` 四档（off/dense/rerank/rewrite）早已实现，默认 off、零依赖。缺的不是能力，是「让人知道有这回事」。故本批**零行为改动**（`build_vectors.py` 只改了一句注释里的体积口径），只补文档与裁决落点。
> - **README 新增裁决段**：为什么升（现役索引 100 题 recall@5 从 0.573 升到 0.712，人工 30 题 0.382 → 0.446）／什么时候值得开（查询以自然语言描述为主、能接受约 220 MB 本地产物、可一次性构建）／什么时候别开（要求零依赖直接跑、CI 与离线只读、结果需随仓分发复现）／本机纪律（重计算任务优先 `--device cpu`，守微批与冷却，勿并行多开）。
> - **顺带修一处同 README 内的口径冲突**：档位表 recall 列还是 T-01 冻结索引（1,077 篇）的旧数，dense 写 0.396；而下方基线表写现役 0.712。两个数并排放着，读者只看上面那行会以为 dense 没用。表头改为「T-01 冻结索引口径·非现役基线」并加一句提醒指向基线表——**数字一个没改，只标口径**。
> - **架构方案回填**：§12.2 Q5 由「新增未决」翻「已裁决：选 ②（显式可选档）」，§7.1 S8 采纳列同步；状态口径改为「开放项只剩 Q2」。
> - **验证**：`check_doc_sync.py` 0 FAIL；`verify_delivery.py --scope full` 核心全部通过；页数与 CSP 零漂移（`site/` 仅四页脚批次链由级联写入，页面结构与内联脚本未动）。
> - **顺带修两处**：① AGENTS 脚注 W847 条目末尾叠出的双句号（模板自动补句号与 note 自带句号相撞）；② 模型体积口径统一——`du -sm` 报的 92 是 **MiB**，与档位表里「约 96 MB」（十进制）本是同一个量，但两个数并排出现像互相矛盾，两处改为「约 92 MiB／≈96 MB」双单位标注。
> - **未做**：不改检索代码、不改默认档行为、不重建向量产物、不推送远端。
> - **状态**：已收官。

### W849（2026-10-21）：性能门禁挂槽批（第 47 槽·影子模式不判红·攒够样本再裁阈值）

> **来源**：用户令「开 W849 做性能门禁挂槽」。这是 W828 备料件 §五 单列的审批项，口径写死为「只挂 1 槽·不改阈值·不碰体积预算」。
> - **文件**：scripts/verify_delivery.py、scripts/check_perf_shadow.py、scripts/output/perf_shadow.json、AGENTS.md、docs/agent/gates.md、pytest.ini、README.md、docs/11-方案报告/系统架构方案-分层模块与部署-2026-10-20.md、scripts/output/stats.json、scripts/output/_w849_spec.json、docs/00-导读/W批次编号对账表.md。
> - **补的是什么洞**：perf.yml 是唯一性能门禁（Lighthouse CI · desktop · 5 URL · 3 runs · LCP ≤4000ms/CLS ≤0.3/TBT ≤300ms·3D 页 12000/900），但它在 pre-commit 路径上**不可执行**（要 Chrome + @lhci/cli，5 URL × 3 runs 分钟级），CI 结果也从未回流成仓内基线——「这次提交有没有让页面变慢」在每次提交时都没有数据可答。
> - **设计取舍（与 W828 §五 字面的偏离，此处明示）**：约定写「复用既有 LHCI 判据」，落地改为**采静态成本代理**、不跑浏览器。三条理由：① pre-commit 每次提交都跑，分钟级 + 依赖浏览器的门禁会被绕过或拖垮流程；② 影子期要的是同口径连续样本，静态量确定性复算、跨机器同值，而 CI 的 LCP 受 runner 冷启与网络抖动影响、单点不可比；③ 真数不另立口径——`--ingest .lighthouseci/assertion-results.json` 把 CI 的 LCP/CLS/TBT 并进**同一批样本**的 `lhci` 字段。**若要求槽内真跑 LHCI，须换成 `--scope perf` 显式 opt-in 轨道另议。**
> - **采六项（每页）**：`html_bytes` / `head_bytes` / `inline_script_bytes`（无 src 脚本内容字节）/ `local_dep_bytes`（本地外链依赖实测字节）/ `remote_refs`（外域引用条数）/ `blocking_head_refs`（head 内同步脚本 + 非 print 样式表）。全部零依赖可算。
> - **判据只有一条会红（C1）**：perf.yml `collect.url` 的 5 页必须真实存在——缺页等于 CI 必 404 的真断链，不是阈值判断；其余数字只记录、不判红。
> - **自测首跑照出的真 bug**：属性解析只认 `key=value`，`defer`/`async` 这类布尔属性被静默丢掉——首版把 index.html 三个 defer 脚本全算成阻塞，基线第一笔就是脏的。改为布尔属性也收，并把「defer 与 media=print 不计」写进自测锁死。
> - **本批首笔基线（不判读、不下结论）**：dashboard 91,791 B · 阻塞头 3；index 51,071 B · 3；timeline 93,207 B · 5；3D 78,575 B · 5；text-search 66,694 B · 5。攒满 10 批后再由用户裁决阈值（3D 页单独分档）。段内数字为落盘时实测，权威值以 `scripts/output/perf_shadow.json` 为准。
> - **连带同步**：门禁段 51→52；AGENTS §4.2 与 gates.md 的第 47 条（含 gates.md 标题从「45 槽」订正为「47 槽」——W809 补第 46 槽时漏改的标题计数）；stats 两键刷新（`gate_count` 47 · `pytest_collected` 787——新脚本被 `test_tool_scripts_cli.py` 的根级脚本参数化收进 import 冒烟，故 +1 属预期）；三处内联标记（README / 架构方案 / pytest.ini）同步。
> - **验证**：`check_perf_shadow --self-test` 7/7；全量 52 段核心全部通过；`check_doc_sync` 0 FAIL；`check_agents_layers` 0 FAIL（三方编号同为 47）；`check_script_coverage` 0 FAIL；stats 17 键零差异；CSP 与页数零漂移。
> - **未做**：不改 perf.yml 阈值、不装 lhci、不跑浏览器、不设任何阈值、不推送远端。
> - **状态**：已收官。

### W850（2026-10-21）：Q2 取数基建批（OBS-10 至 14 采样件·显式开关才测·按指标计批）

> **来源**：用户引我上一段结论原话「接下来唯一待办是 Q2（OBS-10 至 14 什么时候升为硬门槛），需要连续 10 批样本才能决定；从现在开始，每批收尾时运行一次 python scripts/check_perf_shadow.py --record，样本就会积累起来」，据此推进取数基建。
> - **文件**：scripts/obs_sample.py、tests/unit/test_obs_sample.py、scripts/output/obs_samples.json、scripts/output/stats.json、pytest.ini、AGENTS.md、docs/11-方案报告/系统架构方案-分层模块与部署-2026-10-20.md、docs/11-方案报告/静态站前端框架化选型对比-2026-10-20.md、docs/00-导读/W批次编号对账表.md、scripts/output/_w850_spec.json。
> - **先说清 Q2 悬空的真因**：不是「样本还没攒够」，是**根本没有采集机制**。W849 的 perf_shadow.py 只采六项静态成本代理，不碰 OBS-10 至 14 任何一条；而 OBS-11 要浏览器实测、OBS-14 要本地起服务，两者都不是静态可算的。所以「等十批」在过去两个月里是个空转的口号——没有任何脚本会在批次收尾时自动去量 LCP 或首 token。
> - **本批产物**：`scripts/obs_sample.py`，三条 OBS 指标各一个采集通道，统一 `--record` 入库 `scripts/output/obs_samples.json`，`--status` 按指标分别打印 n 比 10 进度。OBS-10 静态全站扫描（0.0 秒）；OBS-11 子进程复用 `perf_monitor.py` 实测五页 LCP；OBS-14 本地起服务实测首 token。
> - **采样纪律（写进代码与用例）**：不猜数（没测记 `measured=false` 加 `reason`）、不补历史、不判红、按指标分别计十批。三条各自攒满十批才够裁决，不因其中一条先满就提前下结论。
> - **显式开关才测**：默认 `--record` 只采静态的 OBS-10；OBS-11 要 `--lcp`、OBS-14 要 `--first-token`。理由是重负载纪律：OBS-11 每次实测都是无头浏览器，用户的笔记本在持续 GPU 重负载下会保护性关机，默认跑等于给每批收尾埋雷。
> - **实测照出的第二个洞：单次 LCP 不可作数**。首采时同机两轮给出 dashboard 116 ms 与 1140 ms——相差十倍，第三次回落到 104 ms。一次 spike 就能把结论从「远低于 SLO」扭成「贴近 SLO」，单次取值的基线完全被噪声支配。改为**每页跑 3 次取中位数**（与 Lighthouse 自身多跑取中位的口径对齐），原始三轮值一并入库 `runs_ms` 供查方差。改后首采：3D 页三轮 268 比 392 比 272，中位 272 把 392 的尖峰剔掉。代价是采集从约 35 秒涨到约 100 秒，仍是 `--lcp` 显式开关内的事。
> - **首笔样本推翻了一个隐含假设**：若今天把 OBS-10 升为硬门槛，第一天就会红——现役 857 页中已有 9 页超 200 KB 上限，最大 `site/en/relationships.html` 403,323 B；另有 172 页超 100 KB。这条数据直接支撑 Q2 的「选 ②」倾向（先告警级、攒够样本再裁），也说明升硬门槛前必须先有分批治理计划。
> - **OBS-11 首笔样本（每页 3 次取中位·无节流本机口径·仅本机可比）**：dashboard 108 ms、index 192 ms、timeline 244 ms、3D 272 ms、text-search 236 ms，最大 272 ms，远低于 1.5 秒 SLO。注意这是无节流本机数，与 CI 的 Lighthouse 口径不可直接互比，只用于看同机趋势。
> - **OBS-14 首记「未测」**：本地没有常驻服务，按纪律记 `measured=false` 与原因，不猜数。这也顺带暴露一个实现坑：urllib 默认吃系统代理，127.0.0.1 探测会被代理截走、端口无人听时回 502，把「不可达」误报成「服务返回 502」——已改为 `ProxyHandler({})` 并写进单测 docstring 锁死。
> - **验证**：`obs_sample --self-test` 7 比 7（含新增的「中位数剔除尖峰」负样本）；`tests/unit/test_obs_sample.py` 9 passed；ruff 两件全过；全量 52 段核心全部通过；`check_doc_sync` 0 FAIL；`check_agents_layers` 0 FAIL。段内数字为落盘时实测，权威值以 `scripts/output/obs_samples.json` 与 `scripts/output/perf_shadow.json` 为准。
> - **同步**：stats 两键刷新（`pytest_collected` 787 比 797——新增 9 例单测加新脚本被 `test_tool_scripts_cli.py` 根级参数化收进 import 冒烟的 1；`gate_count` 仍 47，本批不碰门禁）；pytest.ini collected 标记 787 比 797；README 与架构方案的 `gate_count` 内联标记无需动（W849 已同步为 47）；架构方案 §12.2 Q2 行与 §11.2 注明采样件与本批实测发现。
> - **顺带修：门禁槽数字面量存量漂移 24 处**。本批为写架构方案 §12.2 去核对现役槽数时发现：`<!--stats:gate_count-->` 标记两处是新的，但**同一批文档里的裸字面量没跟着走**——架构方案 14 处「46 槽」加附录 A-04 期望值 `46`（W809 补第 46 槽时漏更，W849 又只同步了标记）、选型对比 8 处「46 槽」、AGENTS §4.2 三处（导读「46 槽摘要」、正文「内含 45 槽」、分组头「27-45」——分别陈滞在 W809 与 W780 时代）。全部改为 47，与 gates.md 标题和 stats 实算对齐。这类漂移无门禁兜底（doc-sync C5b 只扫标记不扫裸数），只能靠批次收尾人工核对，是本批顺带处理的直接原因。
> **状态**：**已收官**（W850 d51d778b·git 反填·共 2 笔·W971 存量回填）

### W851（2026-10-21）：设计迁移阶段 1 令牌落地批（v4 令牌纯加法·34 个零消费新名 / 35 处定义）

> **来源**：用户令「开工」，接 W850 收官后我改口的推荐——Q2 无截止期而设计迁移自 W826 规格就绪后二十余批零页推进，故先迁设计后裁阈值。W851 = 阶段 1 令牌落地（W826 §7 的 J1-J6 验收）。
> - **文件**：site/tokens.css、DESIGN.md、scripts/_w851_j1_name_audit.py、scripts/_w851_visual_regression_probe.py、scripts/_w851_j2_evidence.py、tests/unit/test_w851_visual_regression_probe.py、tests/unit/test_w851_j1_name_audit.py、scripts/output/_w851_j1_name_audit.json、scripts/output/_w851_j2_evidence.json、scripts/output/_w851_tokens_prelanding.css、scripts/output/_w851_visual_snapshot_before.json、scripts/output/_w851_visual_snapshot_after.json、scripts/output/_w851_visual_snapshot_freeze_before.json、scripts/output/_w851_visual_snapshot_freeze_after.json、scripts/output/design-tokens.json、docs/00-导读/design.md、site/data/journey-geo-semiotics.html、site/en/journey-geo-semiotics.html、pytest.ini、docs/00-导读/W批次编号对账表.md、scripts/output/_w851_spec.json。
> - **落地口径**：W826 §4 终稿剔掉 4 组撞名项后落 34 个零消费新名 / 35 处定义——间距刻度 13（4px 基准 + 2/10 半格）+ 语义 gap 6 + 容器三档 3（760/1120/1320·裁决 3）+ 栅格 2 + 排版角色 9 + `--accent-text` 浅暗各 1（裁决 1 修法·暗色同名第二处）。tokens.css 20,799 → 23,039 B（+2,240 B·J4 上限 23,799·§4A.8 预算同批由 +2KB 上调 +3KB·Phase E 的「5.7→7.7KB」为 v3 前口径已废止）。
> - **撞名项显式 defer**：`--chart-1..6` 重述（`--chart-3` 改值命中 42 消费页）、`--accent-soft` 重述（332 消费页·同值空转）、暗色 `--accent` 改值（#E0604F→#E46250）、暗色 `--chart-3/5` 新增——J1 口径「同名即语义改变 → 破坏纯加法」，随迁移批逐页 proof 后再落。审计脚本对 defer 组做**复证机检**（组内现役名必须确已撞名，否则 defer 理由不成立直接 FAIL）。
> - **J1 双向真绿**：落地前对拍现役名（tokens.css / system.css / 全页面内联）交集 0、页面内联抢先定义 0、全站 `var()` 引用 0；落地后复验 34 名 / 35 处全在 tokens.css、暗色组同名再定义在位、4 组 defer 项原值未动（浅色 chart-3 #C9A063 / accent-soft #E9B885、暗色 accent #E0604F 未改·暗色组无 chart-3/5 偷新增）。
> - **零消费机检抓出预支页**：`journey-geo-semiotics` 中英两页早在 W676 前后就以 `var(--space-N, 回退值)` 预支了 v4 名，且回退值（8/12/16px）与终稿刻度（4/8/12px）不一致——直接落地会改这两页渲染。处置：冻结为当前字面值（11 处/页·渲染零变化），令牌 adoption 留到该页迁移批。冻结效果由探针对该两页单独前后对拍证明。
> - **探针三段实证坑（本批最深的工程收获）**：① 首版把 settle 等在了采集**之后**（`wait_for_timeout` 跟在 evaluate 后），被采页面从未获得 settle；② `chart-audit.js` 六族标签修复按 setTimeout 波次执行（最远 14s·波间空隙最大 3000ms），任何静默窗都在波间空隙提前到期——同态两采出现元素数 124↔125、font-size 9px↔10px 跳变（axesvar/numfix 族直接赋值 `style.fontSize`）；③ diff 在元素数不齐时 `continue` 短路，把整页属性比拍掩掉。修法：采集前 15s 固定地板等待 + MutationObserver 静默收敛 + diff 计数不齐仍对拍公共前缀。修后同态两采 23 页 × 双主题 × 22,328 元素零差异。
> - **审计脚本自身也抓出一个假绿**：首版 `_DEF_RE` 捕获组漏 `--` 前缀而 `LANDING_NAMES` 带前缀，致「交集」与「落地完整」两个方向全部空转——单向永绿的检查等于没有检查。修为双向可失败（defer 组须报撞、落地名须报在），并抽 `_preflight_verdict` 纯函数锁进单测。
> - **J2 视觉零变化**：探针对 23 页（J2 采样 21 + 预支页 2）浅暗双主题、15s 地板 + 静默收敛后采集 computed style（29 属性固定序·含 SVG 子元素），置换前（prelanding tokens + 未冻结页）与终态（落地令牌 + 冻结页 + `inline_css.py --force` 同步内联副本）前后对拍**零差异**。
> - **机器可读导出同批同步**：`export_design_tokens.py` 再生成 `docs/00-导读/design.md` + `scripts/output/design-tokens.json`（132 声明 = light 103 / dark 29·AC-1 键数一致）；`check_design_doc_drift.py` 五层对账 0 问题——反篡改（逐字节再生成）与暗色计数两层不跑就会被 J6 抓红。
> - **J3 CSP 零漂移**：CSS 增量不走 CSP 哈希面（style-src 为 unsafe-inline·只哈希内联 `<script>`），`generate_csp.py --check` 全站 0 页漂移。
> - **新增单测 21 例**（pytest 797 → 818）：探针 12 例（计数不齐不掩属性、属性定位、采样面 ≥20、PROPS 固定序、地板/静默常量）+ 审计 9 例（`--` 前缀回归、defer 双向可失败、暗色块并集、落地/defer 集不相交、对真实 tokens.css 的 defer 持有）。
> **状态**：**已收官**（W851 9985da6d·git 反填·共 2 笔·W971 存量回填）

### W852（2026-10-21）：站点 Hero 素材图成套批（六张 16:9 水墨淡彩·风格锚点统一·底部净空带供叠字）

> **来源**：用户令「帮我做几张素材图」，并先问三事——用在哪里、要几张、有无参考风格；本会话按用户选择（用途=站点顶部 Hero 大图、数量=6 张、参考=无参考由本会话按项目气质定一版、主题=行路山河/人物群像/法宝器物/三界秩序四类全覆盖）执行。
> - **文件**：scripts/output/_w852_spec.json、docs/00-导读/W批次编号对账表.md。
> - **风格锚点**：六张共用同一段 art direction 提示词（宣纸 #FAF7F0 纸底 / 玄墨 #221D16 墨线 / 淡墨 #6B6455 / 单一朱砂 #C8463A 强调 / 赭金 #E9B885 点彩），逐字复用六次——成套一致性靠「同段提示词」保证，不靠事后调色。
> - **量化验收**（脚本量测·非目视断言）：成品 2560×1440 = 精确 16:9（源图 2752×1536 实为 1.7917，裁切时按「顶端有深墨则裁底、否则裁顶」的规则保住底部净空带）；底部净空带 320 至 599 px（22.2% 至 41.6%）；上 72% 主体墨量 37.7% 至 46.7%；朱砂占比 0.54% 至 4.43%（上限 8%）；主底色跨图落在 #F8F3E9 / #F9F4EA / #FAF5EC / #FBF3EA 四色同族内；单件 114 至 292 KB。
> - **两轮返工（各因不同）**：首轮 02 人物组像与 03 法宝静物偏线稿插画、与另四张脱节 → 加「松散枯笔/湿染/禁硬描边」子句重做二版；二轮 01/03/04/05 的底部净空带仅 227 至 276 px（叠字区偏窄）→ 把「元素止于 66% 高度、下方三分之一必须完全空白」写成硬边界重做三版。
> - **无文字纪律**：六张均无文字、落款、印章与水印（站内既有 hero 图 ink-mountains-hero.webp 带生成水印，新图不沿袭）。
> - **范围纪律**：只新增 site/static/images/ 下六个素材文件，不改任何页面与门禁件，不推送远端。
> **状态**：**已收官**（W852 7206fac2·git 反填·共 2 笔·W971 存量回填）

### W853（2026-10-21）：卡片封面素材图成套批（十二张 1:1 水墨淡彩·沿用 W852 提示词锚点·底部净空带供叠字）

> **来源**：用户再令「再帮我做几张素材图」，开工前同样先问三事——用在哪里、要几张、有无参考风格；本会话按用户选择（用途=卡片与列表封面、画幅=1:1 方图、数量=12 张、参考=沿用上批宣纸水墨、主题=回目场景/诗词意境/妖怪谱系/三教哲思四类全覆盖）执行。
> - **文件**：scripts/output/_w853_spec.json、docs/00-导读/W批次编号对账表.md。
> - **锚点复用口径**：art direction 段（宣纸 #FAF7F0 纸底、玄墨 #221D16 墨线、淡墨 #6B6455、单一朱砂 #C8463A 强调、赭金 #E9B885 点彩）、松散枯笔湿染笔触句与禁项清单**逐字复用**上批，仅构图几何随 1:1 方图改写（横幅批的「16:9 宽幅」改为「1:1 方幅」，其余规则含「元素止于 66% 高度、下方三分之一完全空白」原样保留）——两批 18 张跨批成套性由此保证。
> - **量化验收**（脚本量测·非目视断言）：成品 1200×1200 = 精确 1:1（源图 2048×2048 等比缩放·不裁切·底部净空带按比例整体保留）；底部净空带 299 至 617 px（24.9% 至 51.4%）；上 66% 主体墨量 18.6% 至 79.9%；严格朱砂口径 0.00% 至 1.03%；主底色 12 值全落 #F8F1E9 至 #FCF6EC 暖白同族；单件 51.6 至 122.9 KB。
> - **测量口径的一处订正**：沿用上批的「暖色」检测器（R-B 大于 60 且 R 大于 110）会把赭金 #E9B885 一并计入（该色 G=184 远高于朱砂），card-05 明月松间照因此先报 8.79% 超阈；加严口径（R-B 大于 100 且 G 小于 120）复量为 0.01%——**是赭金月轮被误判，非朱砂超标**。两口径同时报，避免把「暖色总量」误读为「朱砂占比」。
> - **四主题各三张**：回目场景（火焰山/通天河/狮驼岭）、诗词意境（寒江独钓/明月松间/云深不知处）、妖怪谱系（百妖列阵/濯垢泉蛛网/三妖剪径）、三教哲思（古刹晨钟/松云石坛/书院杏坛）。
> - **无文字纪律**：十二张均无文字、落款、印章与水印。
> - **范围纪律**：只新增 site/static/images/ 下十二个素材文件，不改任何页面与门禁件，不推送远端。
> **状态**：**已收官**（W853 c2a2da12·git 反填·共 2 笔·W971 存量回填）

### W854（2026-10-21）：界面布局审计批（信息层级·区块分布与留白·操作动线·多屏适配·只审计不动代码）

> **来源**：用户令「优化现有界面布局·每处调整讲清理由」。答复取「两套都过（先站点后应用）+ 四痛点全查 + 只出审计报告」口径——本批只审计，不改代码。
> - **文件**：docs/11-方案报告/界面布局审计报告-2026-10-21.md、docs/11-方案报告/README.md、docs/00-导读/W批次编号对账表.md、scripts/_w854_cdp.mjs、scripts/_w854_layout_probe.mjs、scripts/_w854_layout_probe_app.mjs、scripts/output/_w854_layout_metrics.json、scripts/output/_w854_layout_metrics_app.json、scripts/index.md、scripts/output/index.md、scripts/output/stats.json、STRUCTURE.md、docs/11-方案报告/系统架构方案-分层模块与部署-2026-10-20.md。
> - **范围**：补 v4 规格（W819 方向 / W826 细化）未覆盖的两面——「操作动线」与「逐档屏幕适配」，并把已定令牌落成 8 条可判定判据。
> - **产出**：18 条问题逐条附取证（CDP 量测脚本 + 度量 JSON）与调整理由，按影响用户程度排序。
> - **纪律**：0 处 HTML/CSS/JS 改动（报告批）；落库随并行 W855 会话提交带入 7 件（报告正文 + 3 探针 + 2 度量 JSON + scripts/index.md），归属本批。
> - **版段**：本批不落段，CHANGELOG 顶段不变、指针面零改动，随补段批（W863）按号序回写。
> **状态**：**已收官**（W854 324bc3c1·git 反填·共 1 笔·W971 存量回填）

### W855（2026-10-21）：架构评审报告批（现役架构五维体检·模块耦合/性能瓶颈/可用性隐患/扩展性天花板/运维复杂度·只审计不动代码）

> **来源**：用户令「帮我评审现有架构的问题：模块耦合、性能瓶颈、可用性隐患、扩展性天花板、运维复杂度都盘一遍，指出硬伤并给优先级」；答复 = 先审仓内实际架构（文档 + 代码 + 实跑数据，文档已足故不必另收），用户随后令「把这份评审落成仓内产物」。
> - **文件**：docs/11-方案报告/架构评审报告-2026-10-21.md、docs/11-方案报告/README.md、docs/INDEX.md、scripts/output/_w855_spec.json、docs/00-导读/W批次编号对账表.md。
> - **核心判定**：不是「架构差」而是「无构建系统」——治理纪律极强（47 槽编号门禁 / 52 执行段 / 表驱动编排 / 段自洽锁 / 4 级 scope 分级），但所有下游产物（站点页面、英文镜像、数据副本、导航注册、CSP 哈希、版本指针）都是 Markdown 真载体的手工派生物；耦合的真实形态不是「模块互相 import」，而是「物理复制 + 靠门禁定期校准」，而复制速度已超过校准覆盖面——这是全部硬伤的共同根因。
> - **量化底账**（2026-10-21 当盘实跑）：857 页 HTML 50.9 MB · 内联 CSS 1,415 块 18.9 MB 占站点 37% · 内联 JS 3,392 块 7.5 MB · 带内嵌数据页 144 页 2.23 MB · 运行时 fetch json 的页 13 页 25 次 · 门禁套件 143.7 至 156.7 s（a11y_audit 50.1 s + lint_links 27.4 s 占一半）· Agent 工具全仓扫描 11,407 文件 2.6 GB（readdir 1,044 ms + statSync 11,409 次 378 ms 同步阻塞事件循环）· 数据副本同名 47 个中 24 个内容已不同（138,214 B）· 治理文档 CHANGELOG 503,792 B / file-index 156,677 B / AGENTS 66,395 B。
> - **P0 五条**：① 站点页面聚合数字不在任何门禁扫描域（`site/index.html` 写「全站 772 篇」而实测内嵌索引 834 条，差 62；`site/dashboard.html` 同节并存 615 与 575 两套计数）② Agent 检索层缺失 + 全仓同步扫描 1.4 s 冻结事件循环，且扫描域被 `.git` 260 MB、`tmpe/` 890 MB、本地 PDF 库 566.8 MB 污染 ③ 问答链路零重试零退避零续传（SSE 无 `id:` 行，断流整轮作废）④ CSS 单一事实源物化 857 份，改一行 `tokens.css` 触发约 1,190 个文件 diff ⑤ 前后端两份「真相」已漂移（系统提示词文字已不同；前端工具名词表覆盖旧 SDK 的 12 个名字，与后端现役 6 工具有 3 个对不上）。
> - **判据自纠两处**（本批最值得记的工程收获）：① 「同源数据双发 30 页 / 1.10 MB」在严格判据（同源 = 内嵌对象键 ⊆ JSON 顶层键）下复测为 2 页 / 1,444 B，量级不成立故不采信原值；② 「9 页 fetch 无回退」实为正则漏匹配 `EMBEDDED_*` 前缀变体与 `var` 声明，复测后 0 页违反 file:// 铁律（13 个 fetch 页均有 mock 或内嵌兜底）——**先质疑判据、再质疑产物**。
> - **与既有方案的关系**：不重复 W820 目标架构方案（目标态）与 W818 前端选型结论（不做全面框架化），只补「现役缺陷 + 优先级」这一维；建议动作按三梯队给出 16 项，第一梯队 4 项（站点聚合数字定点门禁 / 检索域收窄到 git 跟踪文件 / SSE 补 `id:` 与退避重试 / 收敛前后端两份真相）均不需要推翻现有架构。
> - **并发期归因分离**：评审期间有并行会话在途（W851 级联暂存、W854 界面布局审计），首次门禁实跑出现的 2 项核心 FAIL（第 31 门禁 17 FAIL / 第 45 门禁 2 FAIL）经二次实跑复验为并发在途改动引起、非常设缺陷（干净态复跑 0 核心 FAIL）。
> - **范围纪律**：只读审计，0 处 `site/` 与 `xiyouji-agent-web/` 代码改动，未改任何管控脚本（`verify_delivery.py` 等按文档规范 11.2 禁擅改）。
> - **状态**：报告入库 + 目录索引登记（现役报告 32 → 33 篇）+ `docs/INDEX.md` 产物级重建 + spec 入库；CHANGELOG 版段按 W852 / W853 先例递延，待号序链恢复后由 `backfill_changelog.py` 按号序回写 W852 至 W855 四段及 file-index 双索引。
> **状态**：**已收官**（W855 37ad250b·git 反填·共 1 笔·W971 存量回填）

### W856（2026-10-21）：Logo 定稿落地批（方向 H「山·门槛」·品牌名《取经录》·一级品牌位统一）

> **来源**：用户令做站点 Logo 与品牌名。两轮探索——抽象制图 4 向经用户否决作废；具象符号 5 向（棒 / 幡 / 卷 / 山 / 图）+ AI 概念稿 18 张（14 可用 4 判废）——收敛到方向 H「山·门槛」图形，品牌名《取经录》。
> - **文件**：site/static/icons/（icon-192/512/maskable-512 重做 + logo-mark-light.svg + logo-lockup-light.svg）、site/index.html（六处元信息 + 页眉图形标 + hero h1 + 页脚品牌位）、site/system.css（新增 .brand-mark 纯加法规则）、site/manifest.webmanifest、site/rss.xml、site/static/img/og-cover.png、xiyouji-desktop/、README.md、CITATION.cff、docs/00-导读/W批次编号对账表.md。
> - **图形口径**：64 单位域 · 思源宋体 Heavy 字标路径化 · 零字体依赖；山脊一笔连绵（起收顿挫、提按变化）；地平线与云气为淡墨次级；山顶一点朱砂（远寺的灯）全图只此一处；四向并排按视觉面积归一化，体量差 ≤15%。
> - **落地面**：图标三档（图形占比 72%·maskable 收到 56% 留圆形裁切安全区）+ 页眉图形标与组合标；index 六处元信息（title / RSS title / JSON-LD name / meta description / og:title / og:site_name）+ 页眉 seal→图形标 + hero h1 + 页脚品牌位；manifest name/short_name → 取经录；system.css `.brand-mark` 纯加法（`.seal` 保留·其余 857 页旧印面标识不受影响）；桌面端应用名同步。
> - **版段**：本批不落段（并行会话在途），随补段批（W863）按号序回写。
> **状态**：**已收官**（W856 7d18eb6a·git 反填·共 3 笔·W971 存量回填）

### W857（2026-10-21）：计划方案模板符合性复核批（既有 8 份计划文档 × 模板 32 项结构判据·只复核不改文档）

> **来源**：用户 2026-10-21 23:50 会话指令「按你的建议来。先把计划方案 review 一遍是否符合模板」；模板全文由用户同会话 23:44 提供（本批为该模板在仓内既有计划文档上的首次符合性复核）
> - **文件**：scripts/_w857_plan_template_review.py、scripts/output/_w857_plan_template_review.json、scripts/output/_w857_spec.json、scripts/index.md、scripts/output/index.md、docs/00-导读/W批次编号对账表.md。
> - **落地口径**：8 份文档（5 份《执行前计划》+ 3 份《任务计划执行与经验沉淀报告》）逐份对模板 32 项结构判据机械判定，并另判「计划件 + 报告件」配对并集对 §12 十项的覆盖。**本批 0 处既有文档改动**——复核只出结论与判据，改文档属后续 T-06 批。
> - **核心判定**：① 5 份计划件按 §5.1~§5.9 严格排布，最佳 21/23 判据全符合；② 3 份报告件是**裁剪版**（T04 报告仅 85 行、3/13 编号种类），模板 §12 十项无一全量落在单件内；③ 配对并集 T03 达 8/10、T01 与 T04 仅 4/10；④ 真·模糊词违规 ≤4 处（其余命中均为文档自身「模糊词已清除 ✅」自检行或引文，已在探针内排除）；⑤ 编号 13 类中 G/P/A/WF/SC/PRE 七类基本未落地。
> - **判据校准三处（先质疑判据再质疑产物）**：① 模板把一份报告拆两件落库 → 判据须按件型分判，不适用项判 N/A；② 「本章结论/待确认事项」仓内用「本批不做/待验证/待用户」等效形式 → 增等效识别；③ 模糊词命中先排除自检行与引文块，剩余为真违规。
> - **验证**：py -3 scripts/_w857_plan_template_review.py 复算 8/8 文档矩阵（单件 + 配对并集）；人工抽查 2 份（执行前计划-T01、T04 报告）与探针判定一致；门禁全量档核心全部通过。
> - **状态**：复核完成；既有计划文档的补齐属后续 T-06 批（首页三任务区重组 + 目录页动线）范围。
> **状态**：**已收官**（W857 9b4059f5·git 反填·共 1 笔·W971 存量回填）


### W858（2026-10-21）：站点交互流程审查报告批（857 页 / 2876 控件全量审查·只审查不改代码）

> **来源**：用户令「审一遍我网站的交互流程：页面跳转路径、按钮与状态反馈、表单填写与出错提示、空状态和异常分支是否合理，按影响用户的程度排序给改进建议」；同日追加《任务计划、执行与经验沉淀系统提示词（AI Agent 专用版）》框架与「模板必须落进项目文件夹内 docs/11-方案报告/计划方案」的长期要求。
> - **文件**：docs/11-方案报告/计划方案/T07-任务计划执行与经验沉淀报告-2026-10-21.md、docs/11-方案报告/README.md、docs/00-导读/文档规范.md、docs/00-导读/W批次编号对账表.md、CLAUDE.md、STRUCTURE.md、docs/11-方案报告/系统架构方案-分层模块与部署-2026-10-20.md、docs/INDEX.md、scripts/output/stats.json、scripts/output/stats-index.md、scripts/output/stats-changelog.json、site/data/search.html、site/en/search.html。
> - **产出**：公共站 857 页 / 2876 控件全量交互审查——**3 条 P0**（中文版渡口页 4 按钮 + 输入框 + 夜读钮全失效·根因 W780 模板重建覆盖 306 行页级脚本·线上同款已生效 / 访客「问」浮窗必得「请在终端运行 rag_server.py」且兜底链接指向失效页致闭环死路 / 主导航被 ESC 与 resize 永久隐藏·运行时已复现）+ 8 条 P1/P2/P3 + Web Agent 6 条（独立应用·另批）；含后续施工批 10 步 / 11 条 AC / 7 项风险 / 6 条决策 / 6 条经验。
> - **纪律固化**：`docs/00-导读/文档规范.md` §4.9 增「框架类交付物必须落进仓内目录并登记索引」，CLAUDE.md 增第 11 条指针。
> - **登记与索引**：docs/11-方案报告/README.md §二「计划方案」8→9 篇；report_docs 42→43（stats.py 实算）；docs/INDEX.md 重建；搜索索引与 CSP 哈希随生成器重算。
> - **纪律**：只审查不改代码；版段不落（随补段批 W863 按号序回写）。
> **状态**：**已收官**（W858 e74286c6·git 反填·共 2 笔·W971 存量回填）

### W859（2026-10-22）：设计资产归档批（AI 概念稿 18 张 + Logo 源文件 + 可复算工具链 → assets/design/）

> **来源**：Logo 设计资产此前只存在于临时区 tmpe/_reports/（`_shot` 桶 TTL 7 天），到期即清、无正式留档位置。本批把有长期价值的资产移入仓内 `assets/design/` 单独存档。
> - **文件**：assets/design/logo/（10 件）、assets/design/ai-concepts/（18 张 + 逐张判定表）、assets/design/tools/（可复算工具链）、assets/design/README.md、docs/00-导读/W批次编号对账表.md。
> - **为什么放 assets/ 而非 site/static/**：`site/` 是站点构建面（桌面端把整个 site/ 打进安装包），设计源资产（概念稿与工具链）不进站点；`assets/` 是仓级素材区，与 fonts / images / maps 并列。
> - **目录**：`logo/` 10 件——矢量图形标与组合标 SVG、icon-192/512/maskable-512、favicon-16/32/48 与 favicon.ico（站点在用版本在 site/static/icons/，同批产出两处一致）；`ai-concepts/` 18 张——AI 纯图形概念稿（两批），附逐张「母题 / 判定 / 说明」表；`tools/` 可复算工具链。
> - **纪律**：只新增 assets/ 下素材与登记，不改任何页面与门禁件；版段不落（随补段批 W863 按号序回写）。
> **状态**：**已收官**（W859 9bafb5f3·git 反填·共 3 笔·W971 存量回填）

### W860（2026-10-22）：计划方案合规门禁挂槽批（第 48 槽·用户明令「探针进门禁」·既有计划方案先不做）

> **来源**：用户 2026-10-22 会话指令「探针进门禁，计划方案先不做」——前半句批准把 W857 复核批的模板符合性探针接成常驻门禁槽，后半句明确**既有计划文档本批不动**（补齐属后续施工批）。本批为管控件改动（`scripts/verify_delivery.py` 属管控文件），经用户明示批准。
> - **文件**：scripts/check_plan_template.py、scripts/_w857_plan_template_review.py、scripts/verify_delivery.py、tests/unit/test_check_plan_template.py、AGENTS.md、docs/agent/gates.md、README.md、pytest.ini、HANDOVER.md、scripts/output/stats.json、scripts/index.md、scripts/output/index.md、docs/00-导读/W批次编号对账表.md、docs/11-方案报告/系统架构方案-分层模块与部署-2026-10-20.md。
> - **落地口径**：第 48 槽「计划方案合规」挂进 `verify_delivery.py`（`_StrictGate`·crash 即拦 + 汇总行防静默跳过）；门禁段 52→53；`EXPECTED_SECTION_NAMES` 与 `SCOPE_DOCS_SECTIONS` 同步；判据表（32 项结构判据）复用 W857 的 `_w857_plan_template_review.py`，本批只加增量判定层。
> - **增量口径（核心设计）**：新增文件全项判（任一「不符合」判红）；修改文件取 HEAD 版本同判据求差集（**只判本次引入的新不符合项**·存量不符合项只 NOTE 提示）；未变更文件不看。**为何必须增量**：W857 实测存量 8 份里最弱的仅 6/13 判据符合，若整量判红则本槽上线即全红、形同虚设。
> - **判据三处校准（继承 W857·先质疑判据再质疑产物）**：① 模板 §12 要求「一份交付物含十项」，仓内惯例拆《执行前计划》+《执行记录报告》两件落库 → 判据按件型分流（不适用项判 N/A·不计不符合）+ 另判两件并集覆盖度；② 「执行摘要/本章结论/待确认事项」认等效形式（「0. 任务背景」「本批不做」「待验证」「待用户」）；③ 模糊词扫描排除文档自证行与引文块（否则自命中假红）。
> - **负样本自证 7 例（--self-test，全过）**：新增合规→绿 / 新增缺项→必红 / 存量缺项仅改别处→不误判红 / 存量合规改出缺项→必红 / 补齐→恢复必绿 / git 端到端（未跟踪缺项文件进变更集→必红）/ 清理后不再命中；另 pytest 单测 4 例（纯逻辑面·git 级用例不进 pytest 避免 CI 里往仓内写文件）。
> - **端到端实跑（负样本真拦）**：在 计划方案/ 内造一份缺整节文档 → 第 48 槽 FAIL → `verify_delivery.py --scope docs` exit=1 阻断提交 → 撤除后复跑 exit=0 转绿。
> - **口径同步四处**：AGENTS.md §4.2（新增第 48 条 + 两处「47 槽」→48 槽）、docs/agent/gates.md（标题 47→48 槽 + 第 48 槽全量定义 + 根级脚本数 103→118 实数）、README.md 与 系统架构方案 的 `<!--stats:gate_count-->` 标记（47→48，架构方案另同步 17 处裸「47 槽」字面量）、stats.json（gate_count 47→48·pytest_collected 818→823）+ pytest.ini 标记（818→823·实测值非 +1：新脚本被根级脚本覆盖测试参数化自动纳入 +1、新单测 +4）。
> - **本批边界**：**既有计划文档 0 处改动**（用户令「计划方案先不做」）；不落段（CHANGELOG 顶段不变·指针面零改动）；不改门禁脚本的其他判据。
> - **验证**：全量档 `verify_delivery.py --scope full` exit=0（52→53 段·第 48 槽 0 FAIL）；`check_doc_sync.py` 0 FAIL；`check_folder_docs.py` 0 FAIL；`stats.py --check` 17 键零差异；pytest 新增 4 例全过 + 脚本自证 7/7。
> - **状态**：门禁已挂载；补齐既有计划文档属后续施工批（框架号 T-06·施工批号待定）。
> **状态**：**已收官**（W860 42b3d245·git 反填·共 3 笔·W971 存量回填）

### W861（2026-10-22）：设计资产归档收尾批（过程截图 13 张 + 4 个未选定方向备选 SVG + 跨会话回执底件）

> **来源**：W859 把 Logo 源文件、18 张概念稿与可复算工具链归档进 assets/design/ 后，临时区 tmpe/_reports/ 下仍留有过程材料。本批把其中**有留档价值**的部分移入仓内，其余（工具脚本、门禁输出、提交信息、已入库的资产副本）随临时区一并清空。
> - **文件**：assets/design/alternatives/（4 件）、assets/design/screenshots/（13 张）、assets/design/process/RECEIPT-W855.md（1 件）、assets/design/README.md、docs/00-导读/W批次编号对账表.md。
> - **新增三块**：`alternatives/` 4 件——四个未选定方向的图形标矢量源（棒《取经录》/ 幡《问津》/ 卷《拾遗》/ 图《十万八千里》），与定稿共用同一套笔触引擎与配色令牌，改方向不必重画；`screenshots/` 13 张——视觉留档（五方向 × 深浅底拼版、两批概念稿拼版、四方向分区呈现、落地图标三档实测、组合标预览、方向 I 特写、站点实拍、预览页整页）；`process/` 1 件——跨会话回执底稿 RECEIPT-W855.md。
> - **附修**：19 条死链 hotfix（临时区文件搬走后引用路径失效，随批修正）。
> - **纪律**：只新增 assets/ 下素材与引用修正，不改任何页面行为与门禁判据；版段不落（随补段批 W863 按号序回写）。
> **状态**：**已收官**（W861 9f3723e6·git 反填·共 3 笔·W971 存量回填）

### W862（2026-10-22）：设计迁移 B1 根页与入口 8 页（容器归并·朱砂合规·对比度修法·间距令牌化）

> **来源**：用户令「下一批就是迁移批本体 B1（根页与入口 8 页），探针已备好」，接 W851 令牌阶段 1 之后。W862 = W826 §6 迁移清单第一批（B1·根页与入口 8 页）。
> - **文件**：site/index.html、site/guide.html、site/curated.html、site/dashboard.html、site/dukou-engine.html、site/rum-viewer.html、site/visit-viewer.html、scripts/_w862_tokenize_spacing.py、scripts/_w862_accent_text_audit.py、scripts/_w862_diff_review.py、scripts/output/_w862_accent_text_audit.json、scripts/output/_w862_diff_review.json、scripts/output/_w862_spec.json、docs/00-导读/W批次编号对账表.md。
> - **迁移口径（四渠·每处 diff 必可归因）**：A 容器归并——dashboard `.container` 1536→`--container-wide`（§3.3「1536 降档 1320」）、rum-viewer `.wrap` 1024→`--container-content`（§3.3「根 1 页 1024 归并 1120」）、dukou-engine `.page-wrap` 现役 1320 字面量→`--container-wide`（令牌化·零视觉变化）；B 朱砂合规——dashboard KPI 大字 `--accent-deep`→`--ink`（§5.2②「禁朱砂数字·统一墨色」）、dukou `.seal` 徽章实底→`--accent-tint` 淡底+朱砂字（§3.2「徽章实底改朱砂字+淡底」）、dukou 四处朱砂实底逐处定性后计数 2 处（≤3✓·两处 2px 线走白名单）；C 对比度修法——朱砂文字落 `--bg` 处改 `--accent-text`（§3.1 裁决 1 修法·**机器分类非目测**：`_w862_accent_text_audit.py` 按计算样式解析有效背景，20 处落 bg 收敛到 5 个选择器：`.kicker`×12、`.section-kick`×5、dukou `header h1`、rum `.btn`；`--accent-text` 至此有了第一批消费者）；D 间距令牌化——padding/margin 家族里与 v4 刻度**精确等值**的 132 处字面量换 `var(--space-N)`（不等值一律不动·值保留故零视觉变化）。
> - **defer 四项本批不动**：`--chart-3` 改值（B1 无图表消费者·随 B2 数据页批）、暗色 `--accent` 改值（全局爆弹·待消费者迁移到位）、暗色 `--chart-3/5`（同 B2）、`--accent-soft` 重述（同值空转·不落）。
> - **验收方式（迁移批≠零差异）**：J2 探针 24 页（B1 八页 + 探针原 21 面其余 16 页 作全局金丝雀）浅暗双主题前后对拍；`_w862_diff_review.py` 全量归渠聚合——每处 diff 必须落进 A/B/C 三渠，D 令牌化若值保留正确应产生 0 diff；金丝雀页必须 0 diff（证明没碰全局令牌）。**判词：PASS——700 处 diff 全部归渠零剩余**：dashboard 630（60 张 KPI 卡大字 `--accent-deep`→`--ink` 600 + kicker 改 accent-text 30）· index 25 / curated 20 / guide 15（kicker 系）· dukou 5（header h1）· rum-viewer 6（容器 1024→1120 的 margin 位移 4 + btn 字色 2）；**16 页金丝雀与自包含页全部 0 diff**（全局令牌未动·D 令牌化值保留实证）。
> - **J2 抓到一个真错（本批最值钱的发现）**：404.html 的间距令牌化把全部值坍成 0px——该页第 25 行自注「W572 D-2 自包含 404 页·无 tokens.css 链接·字面值为三色直译，有意设计」，`var(--space-N)` 在无令牌页解析失败落初始值。**处置：整页回退**（该页不在令牌体系内·迁移不适用），复采并入 after 快照后 404 归零。教训：令牌化的前置条件是页面真的引了令牌——D 渠必须先查 `<link tokens.css>` 或内联块，自包含页跳过。另：dukou `.seal` 为死规则（无 DOM 消费者·改动无 diff）——徽章实底改淡底的改动保留（未来启用即合规），如实记录无视觉证明。
> - **工具三件**：`_w862_tokenize_spacing.py`（值保留式令牌化·dry-run 先行·跳过 INLINED 块防循环定义）、`_w862_accent_text_audit.py`（朱砂文字落点机器分类·按计算样式解析有效背景链）、`_w862_diff_review.py`（全量 diff 归渠聚合·探针内置 20 条上限不够迁移审查用）。
> - **范围纪律**：只动 site/ 根 8 页（`_template.html` 按 §6 不迁移）；不改 site/tokens.css 与 system.css（金丝雀 13 页 0 diff 即证）；CSP 只哈希内联脚本且本批无脚本改动。
> **状态**：**已收官**（W862 e561ae95·git 反填·共 2 笔·W971 存量回填）

### W863（2026-10-22）：递延版段补写批（W852-W862 十一段回写·号序链重新接上）

> **来源**：用户令「你决定，继续」。决定先清 CHANGELOG 号序链欠账再进 B2：`batch_cascade` 的 `assert batch == W顶段+1` 是段序保护，但 W852 起十一个批因并行在途全部递延，顶段停在 W851——每立一个新批的段都会被这条断言拦住，B2 也过不去。
> - **文件**：CHANGELOG.md、scripts/output/file-index.md、scripts/output/_w854_spec.json、scripts/output/_w856_spec.json、scripts/output/_w858_spec.json、scripts/output/_w859_spec.json、scripts/output/_w861_spec.json、scripts/output/_w863_spec.json、docs/00-导读/W批次编号对账表.md。
> - **做法**：`backfill_changelog.py`（W842 建）第二次使用。待补 11 段（W852-W862）——其中 W852/W853/W855/W857/W860/W862 六批 spec 原本在位；W854/W856/W858/W859/W861 五批 spec 缺失，按各自 feat 提交信息与台账行**新建补位 spec**（内容只照记录、不添油加醋，agents_note 前注明「补位 spec」）。工具按号序把每段插到「第一个号小于自己的段」之前，file-index 同批回写；规则行 W001-W851 → W001-W862。
> - **本批自身**：顶段推进到 W862 后，本批经 `batch_cascade` 正常立 W863 段并把「当前态六面」（README / STRUCTURE / 项目说明版本行·交接里程碑·AGENTS·CITATION·三简单页脚）统一推进到 W863——这是补段工具不做、必须级联做的部分。
> - **不改历史**：补段只插入、不清洗、不重排、不改写既有段任何字符；不动任何页面行为与门禁判据（页脚三简面由级联按正常批口径更新）。
> **状态**：**已收官**（W863 a8e66ffb·git 反填·共 2 笔·W971 存量回填）

### W864（2026-10-22）：设计迁移 B2 结构页 10 页（容器令牌化·朱砂实底合规·间距令牌化）

> **来源**：用户「可以」批准 `--chart-3` 拆专批方案后启动。W864 = W826 §6 迁移清单第二片（结构页 10 页）。
> - **文件**：site/data/chapter-structure-graph.html、site/data/chapter-stats.html、site/data/story-timeline.html、site/data/timeline.html、site/data/relationships.html、site/data/81-hardships.html、site/data/81-hardships-view.html、site/data/hardship-heatmap.html、site/data/hardship-difficulty-heatmap.html、site/data/methodology-matrix.html、scripts/_w864_migrate.py、scripts/_w864_accent_audit.py、scripts/output/_w864_accent_audit.json、scripts/output/_w864_accent_exemptions.json、scripts/output/_w864_spec.json、docs/00-导读/W批次编号对账表.md。
> - **A 容器**：十页均现役 1320px（= 目标档），`max-width: 1320px` 字面量换 `var(--container-wide)`，零视觉变化。
> - **B 朱砂实底**：机检按计算样式量（背景色 == 朱砂且面积 >400px²，或 top 边框色 == 朱砂且 ≥2px 且面积 >400px²）。**KPI 顶条收敛**——八页 `.kpi-row` 的 3px 朱砂顶条按裁决 2「整页仅首屏首卡可带」收敛为：首卡保留 3px 朱砂，其余非 alt 变体卡片降 1px 线（alt-2/3/4 非朱砂不动）；`.seal` 徽章实底（40×40 朱砂块）转 `--accent-tint` 淡底 + 朱砂字（十页同款）。**数据语义色片进豁免清单**（`scripts/output/_w864_accent_exemptions.json`·首批）：81-hardships 的 90 个 `.tag`（cause/ending/difficulty 分类编码）、relationships 的 5 个 `.role-tag.primary`（阵营编码）、methodology 的 8 个 quad/phase 徽章、以及选中态实底（组件卡③明定 `--accent` 底）——白名单「图表语义不属界面装饰」的落地形态。
> - **D 间距**：216 处精确等值字面量 → `var(--space-N)`（值保留·零视觉变化）。
> - **C 渠与 chart-3 defer**：数据页的 117 处朱砂文字跨 12 条 scoped 规则（`.design-purpose strong` / `td.num` / `.ec-axis` / `.ibox-label`…），且存在 tint 背景第三态（裁决的两态口径未覆盖），逐规则核对成本与风险高于本批价值——**拆「对比度专项批」**，与 `--chart-3` 值切换（42 消费页）同批，用全站审计 + 专属对拍面一次 proof。
> - **验收**：J2 探针 24 页（10 页 + 14 页金丝雀）浅暗双主题前后对拍 + 全量 diff 归渠。**判词：PASS——302 处 diff 全部归渠零剩余**：KPI 顶条收敛 96 处（25 张非首卡 × 2 属性 × 双主题）+ `.seal` 徽章 198 处（8 页 × 2 个 seal 元素 × 6 属性 × 双主题）+ **顶条回流连带 8 处**（hardship-heatmap 2 个 SVG 标签 font-size 9→10px：顶条 3px→1px 让布局回流 2px，chart-audit 修复器重判后不再压缩——复采确定性已验证）。A（容器令牌化）与 D（间距 216 处）**零 diff**——值保留实证。金丝雀 13 页 0 diff。**施工中抓到一个 CSP 级事故**：令牌化改动了内联脚本里模板字面量的 CSS（`margin-top:4px` → `margin-top:var(--space-2)`），脚本哈希变化而 CSP 未重算 → 采集时脚本被拦、两页元素数塌陷（905→176/76→52）；并行会话随后重算哈希，本批重采 10 页并合并后归零。**教训：动到内联脚本文本（哪怕只是模板里的 CSS 值）必须同批重算 CSP 哈希**。另：timeline 的 accent-2/3/4 彩条属非朱砂顶条，首轮通用规则压平了它——按「限额只针对朱砂」回退（彩条恢复）。
> **状态**：**已收官**（W864 3b3d77fb·git 反填·共 2 笔·W971 存量回填）

### W865（2026-10-22）：首页三任务区重组 + 目录页检索动线批（接 W854 审计的 D1/D2 裁决）

> **来源**：用户 2026-10-22 00:39「按你的建议来」（W854 界面布局审计的 D1/D2 裁决获批）+ 02:45「现在做」（开工授权）；框架交付物 T-08。
> - **文件**：site/index.html、site/reader/**（622 页中 101 页 INLINED 块同步 + 总目录页新功能）、site/js/reader-enhance.js、site/data/search.html、site/en/search.html、scripts/build_reader.py、scripts/_w865_layout_probe.mjs、scripts/output/_w865_layout_metrics.json、scripts/output/_w865_spec.json、scripts/index.md、scripts/output/index.md、scripts/output/stats.json、docs/11-方案报告/计划方案/T08-任务计划执行与经验沉淀报告-2026-10-22.md、docs/11-方案报告/README.md、docs/INDEX.md、STRUCTURE.md、docs/11-方案报告/系统架构方案-分层模块与部署-2026-10-20.md、docs/00-导读/W批次编号对账表.md。
> - **D1 首页**（接 W854 审计 S1/S2/S3/S4）：按「读 / 查 / 看」三任务区重组——① 顶层块 9 → 6（masthead / 读区 / 装饰 SVG 转场 / 查资料区 / 开篇诗转场 / 看数据与工具区）；② 三区各恰 1 个 h2（从哪一回读起 / 查资料 / 看数据与工具）；③ 站内搜索由首屏英雄区降为「查资料」区内的工具条（h2 → 工具级标题，治「占满首屏的标题比内容标题小 12px」的层级倒挂）；④ 装饰 SVG 与开篇诗移出首屏（转场位）；⑤ stats 收进「看数据与工具」区；⑥ ≤768 档 mega 数字降为紧凑计量（桌面保留品牌大字）。**实测**（无头 Chrome·375/768/1440）：顶层块 6 · 首屏可见 h2 = 1（内容类·「从哪一回读起」）· 首屏可见内容入口链接 4 / 5 / 2（改前 0）· 首屏内容起点 497 / 550 / 564px（改前 857 / 1102）· @375 下 h2−h3 字号差 4px（改前 0px·同 20px）。
> - **D2 目录页**（接 W854 审计 S8/S9）：加检索工具条——即时过滤 + 回号直达 + 6 组跳转锚点 + 命中计数。**目录页是生成产物**（`scripts/build_reader.py` 写）→ 改生成器不手改页面；逻辑落 `site/js/reader-enhance.js` 并以 DOM 守卫（`[data-catalog-tools]`）只对总目录页生效 → 其余 621 页行为零变化，且不写 inline script（守 CSP `script-src 'self'`）。**实测**：输入「42」命中 1 / 615 条 ·「孙悟空」命中 8 条 · 重置回 615 条 · 回号直达「100」定位到 `ch100.html`「第 100回 径回东土五圣成真」（到达第 100 回 = 1 次输入 + 1 次回车 = 2 次操作·原为滚 37 屏）。
> - **重建纪律（关键）**：全量重建对现役 622 页产生 128,254 行漂移（超 T04 计划立的 2,000 行阈值）→ 漂移源是**后处理链注入**（CSP meta / SEO 块 / INLINED CSS 块）不在生成器输出里；实测 `inject_seo_head.py` + `inline_css.py` + `generate_csp.py` **幂等**（重跑 site/ 零变化）→ 「重建 + 三条链回注」后 621 页逐字节一致，101 页顺带同步了此前陈旧的 INLINED 块（缺 W856 的 `.brand-mark` 样式）·总 diff **1,063 行**（+955 / −108）在阈值内。
> - **两次翻车与判据修正（留痕）**：① 首跑把 `/^\\d{1,3}$/` 写成双反斜杠 → 回号直达整条链路静默失效（过滤仍「看起来正常」·数字路径单独失效）；② 探针把 href **值**拿去匹配 `href="` 模式 → 首屏内容链接误报 0。两处都是**判据/实现层的转义错误**，不是产品缺陷——修法：正则一律单反斜杠 + 探针对属性值用 `^` 锚定。
> - **本批边界**：既有计划方案文档 **0 处改动**（用户 2026-10-22 明令「计划方案先不做」）；不碰 `site/data/**`（并行 W864 在途·D4 另批）；不落段（CHANGELOG 顶段不变·指针面零改动·素材交 backfill 按号序补）。
> - **验证**：无头 Chrome CDP 探针 `scripts/_w865_layout_probe.mjs` 实测双页面 5 组（首页 1440/768/375 + 目录页 1440/375）·度量落 `scripts/output/_w865_layout_metrics.json`；`generate_csp.py --check` 0 漂移；`check_structure.py` 结构平衡通过；全量档 `verify_delivery.py` 核心全部通过。
> - **状态**：D1/D2 施工完成并经实测；D3（移动端卡片 1 列）/ D4（可视化页 KPI 降级·撞 W864 在途）/ D5（应用响应式）/ D6（死令牌清理）四批待另起。
> **状态**：**已收官**（W865 1dd17a7c·git 反填·共 1 笔·W971 存量回填）


### W866（2026-10-22）：设计迁移 B3 人物主线 9 页（容器归并·朱砂实底合规·间距令牌化）

> **来源**：用户令「开始」，接 W864（B2）之后。W866 = W826 §6 迁移清单第三片（人物主线 9 页）。
> - **文件**：site/data/character-appearance.html、site/data/character-presence-timeline.html、site/data/character-semantic-network.html、site/data/character-dynamic-network.html、site/data/character-sentiment-arc.html、site/data/character-relationship-3d.html、site/data/character-relationship-3d-view.html、site/data/dialogue-sentiment.html、site/data/ai-dialogue.html、scripts/output/_w866_spec.json、scripts/output/_w866_accent_audit.json、scripts/output/_w866_diff_review.json、scripts/output/_w864_accent_exemptions.json、docs/00-导读/W批次编号对账表.md。
> - **A 容器**：八页 1320px 字面量 → `var(--container-wide)`（零视觉变化）；**character-semantic-network 的 `.container` 1280 → `var(--container-content)` 1120**——§3.3 枚举的「data 三页 1280 归并」之一，本批唯一有视觉位移的容器改动（−160px 居中）。
> - **B 朱砂实底**：KPI 顶条收敛四页（appearance 4→1 · semantic-network 6→1 · dynamic-network 4→1 · relationship-3d 5→1，非首卡降 1px 线）；`.seal` 徽章八页有效（第九页 character-relationship-3d-view 的规则无 DOM 消费者）转 `--accent-tint` 淡底 + 朱砂字；**ai-dialogue 的 4 个 step-num 编号徽章**（24×24 圆·朱砂底白字）转淡底 + 朱砂字（裁决 2 徽章实底规则）。豁免登记簿升级为多批结构并增补 W866 条目（选中态 4 处·负向指示 1 处·主行动按钮 1 处）。
> - **D 间距**：149 处精确等值字面量 → `var(--space-N)`（值保留·零视觉变化）。
> - **C 渠与 `--chart-3` 值切换继续 defer** 至「对比度专项批」（本批文字落 bg 共 58 处·跨多规则·同 W864 口径）。
> - **验收**：J2 探针 23 页（9 + 14 金丝雀·index.html 因 W865 并行在途剔出）双主题前后对拍 + diff 全量归渠；金丝雀零 diff。**施工纪律（W864 教训）**：令牌化可能改到内联脚本模板字面量里的 CSS，采集前必先 `generate_csp.py` 重算哈希。**判词：PASS——296 处 diff 全部归渠零剩余**：KPI 顶条收敛 68 处（17 张非首卡 × 2 属性 × 双主题） + `.seal` 徽章 204 处（8 页有效 × 2 元素 × 6 属性 × 双主题·character-relationship-3d-view 的 .seal 为死规则无 DOM 消费者） + ai-dialogue step-num 徽章 20 处（字色 white→accent 及 currentColor 边框连带）+ character-semantic-network 容器居中位移 4 处（1280→1120 后 margin 0→3.2px·A 渠唯一真实位移）。**D 间距 149 处零 diff**（值保留实证）；金丝雀 14 页 0 diff；元素数双采完全一致（24,996 == 24,996）——CSP 先重算再采集的纪律生效。
> **状态**：**已收官**（W866 89432726·git 反填·共 2 笔·W971 存量回填）

### W867（2026-10-22）：设计迁移 B4 妖怪与神力 10 页（容器归并·朱砂实底合规·间距令牌化）

> **来源**：用户令「开始」，接 W866（B3）之后。W867 = W826 §6 迁移清单第四片（妖怪与神力 10 页）。
> - **文件**：site/data/monster-background.html、site/data/monster-capability-radar.html、site/data/monster-ecology-network.html、site/data/monster-female-network.html、site/data/monster-hierarchy-network.html、site/data/monster-sociology.html、site/data/monster-victims-network.html、site/data/ecology.html、site/data/heaven-power-network.html、site/data/underworld-power-network.html、scripts/output/_w867_spec.json、scripts/output/_w867_accent_audit.json、scripts/output/_w867_diff_review.json、scripts/output/_w864_accent_exemptions.json、docs/00-导读/W批次编号对账表.md。
> - **A 容器**：九页 1320px 令牌化；**monster-background 的 `.container` 与 `footer` 两处 1280 → `var(--container-content)` 1120**——§3.3「data 三页 1280」的第二户，页脚随容器对齐一并归并（否则页脚比正文宽 160px）。
> - **B 朱砂实底**：KPI 顶条收敛六页（capability-radar 4→1 · female 6→1 · hierarchy 4→每行首卡保留 · victims 6→1 · heaven 4→每行首卡 · underworld 4→每行首卡）；`.seal` 徽章十页转淡底。**语义变体条进豁免登记簿**（`_w864_accent_exemptions.json` 的 W867 分册·18 处）：`.signal-card.s-active`（状态三态之一）、`.compare-card.invasive`（入侵态）、`.role-card.r-king`（角色编码·用 `--chart-1` 调色板）、`.victim-card`（高亮标记）、`.swatch-bar`（图例色块）、`.tab-btn.active`（选中态）、`.damage-pill.damage-high`（伤害等级编码 ×9）。
> - **发现一处跨批线索**：`role-card.r-judge` 用 `var(--chart-3)` 编码觐官角色——**图表调色板被 UI 消费**，chart-3 值切换专项批须连带审计这类点（不只 SVG 图表）。
> - **D 间距**：219 处精确等值字面量 → `var(--space-N)`（值保留·零视觉变化）。
> - **C 渠与 `--chart-3` 值切换继续 defer** 至对比度专项批（本批文字落 bg 54 处）。
> - **验收**：J2 探针 23 页（10 + 13 金丝雀·index 已由 W865 提交、回归金丝雀位）双主题前后对拍 + diff 全量归渠；金丝雀零 diff；令牌化后先 `generate_csp.py` 再采集。**判词：PASS——372 处 diff 全部归渠零剩余**：KPI 顶条收敛 140 处（70 张非首卡 × 2 属性 × 双主题） + `.seal` 徽章 220 处（10 页 × 元素 × 6 属性 × 双主题）+ 容器归并连带 8 处（monster-background 页脚 1280→1120 后居中 margin 0→80px = (1280−1120)/2 精确对账）+ 顶条回流连带 4 处（capability-radar 2 个 SVG 标签 font-size 10→9px：顶条降 2px 后 chart-audit 重判为需压缩）。**D 间距 219 处零 diff**（值保留实证）；金丝雀 13 页 0 diff；元素数双采一致（25,410 == 25,410）。
> **状态**：**已收官**（W867 66274869·git 反填·共 2 笔·W971 存量回填）

### W868（2026-10-22）：设计迁移 B5 取经与行迹 10 页（容器令牌化·朱砂实底合规·间距令牌化）

> **来源**：用户令「B5–B10 一次做完」，六批连做第一片。W868 = W826 §6 迁移清单第五片（取经与行迹 10 页）。
> - **文件**：site/data/guanyin-six-roles-network.html、site/data/pilgrim-team-dynamic-network.html、site/data/pilgrim-team-psychology-arc.html、site/data/journey-route.html、site/data/journey-geo-3d.html、site/data/journey-geo-semiotics.html、site/data/journey-map-interactive.html、site/data/journey-spacetime.html、site/data/customs-pass-route.html、site/data/cave-estate.html、scripts/output/_w868_spec.json、scripts/output/_w868_accent_audit.json、scripts/output/_w868_diff_review.json、scripts/output/_w864_accent_exemptions.json、docs/00-导读/W批次编号对账表.md。
> - **A 容器**：十页 1320px 字面量 → `var(--container-wide)`（零视觉变化·本片无 1280 归并）。
> - **B 朱砂实底**：KPI 顶条收敛六页（guanyin 6→1 · dynamic 5→1 · psychology 5→1 · route 4→1 · map-interactive 5→1 · spacetime 4→1 · customs 4→1 · cave-estate 4→1）；`.seal` 徽章十页转淡底。**26 处语义变体进豁免登记簿 W868 分册**：role-card 角色条 / swatch-bar 图例 / ctrl-btn.active / phase-card.active / progress-fill ×2（进度数值） / 主行动 btn / **tag.king ×19（妖王分类色片·与 B2 的 .tag 同型）**。
> - **冻结解除**：journey-geo-semiotics——W851 审计发现其预支 `var(--space-N)` 且回退值与终稿刻度不符，当时冻结为字面值；本批作为迁移批正式消费 v4 令牌（mech-card 单条不超限未动）。
> - **D 间距**：166 处精确等值字面量 → `var(--space-N)`（值保留）。
> - **C 渠与 `--chart-3` 值切换继续 defer** 至对比度专项批（本批文字落 bg 64 处）。
> - **验收**：J2 探针（大 before 68 页同源 + 本批 after 10 页）双主题对拍 + diff 全量归渠。**判词：PASS——360 处 diff 全部归渠零剩余**：KPI 顶条 116（58 张非首卡 × 2 属性 × 双主题）+ `.seal` 220 + 顶条回流连带 24（cave-estate 16 + journey-route 8：SVG 标签 font-size 9↔10 / 11.2→9px 重判）。D 166 处零 diff；元素数双采无异常。
> **状态**：**已收官**（W868 aa8e97c5·git 反填·共 2 笔·W971 存量回填）

### W869（2026-10-22）：设计迁移 B6 叙事学 10 页（容器令牌化·朱砂实底合规·间距令牌化）

> **来源**：用户令「B5–B10 一次做完」，六批连做第二片。W869 = W826 §6 迁移清单第六片（叙事学 10 页）。
> - **文件**：site/data/narrative-experiment.html、site/data/narrative-rhythm-curve.html、site/data/narratology-12d-network.html、site/data/narratology-16d-network.html、site/data/intertextuality-network.html、site/data/deconstruction.html、site/data/six-senses-narratology-network.html、site/data/poetry-rhythm-analysis.html、site/data/music-structure.html、site/data/language-style-radar.html、scripts/output/_w869_spec.json、scripts/output/_w869_accent_audit.json、scripts/output/_w869_diff_review.json、scripts/output/_w864_accent_exemptions.json、docs/00-导读/W批次编号对账表.md。
> - **A 容器**：十页 1320px 令牌化（零视觉变化·本片无 1280 归并）。
> - **B 朱砂实底**：KPI 顶条收敛九页（5/6/6/6/4/6/5/1/5→1）；**narrative-experiment 的 12 张 narr-card 网格顶条按裁决 2 收敛**（`.narr-card ~ .narr-card` 降 1px 线——12 张全同色是装饰网格、非数据编码，判据见豁免登记簿 W867 分册注释）；`.seal` 徽章九页转淡底。**50 处语义色片进豁免登记簿 W869 分册**：sc-chip ×4 / sc-cat / gh-tag / hc-owner ×2 / tag ×5（deconstruction）/ **tag ×35（music-structure 曲牌分类）** / progress-fill / 主行动 btn。
> - **D 间距**：211 处精确等值字面量 → `var(--space-N)`（值保留）。
> - **C 渠与 `--chart-3` 值切换继续 defer** 至对比度专项批（本批文字落 bg 128 处·为六批最多——music-structure 65 处、narrative-experiment 37 处）。
> - **验收**：J2 大 before + 本批 after 双主题对拍 + diff 全量归渠。**判词：PASS——446 处 diff 全部归渠零剩余**：顶条收敛 222 处（KPI 九页 47 张非首卡 + narr-card 网格 11 张 × 2 属性 × 双主题·同组聚合）+ `.seal` 220 处（10 页 × 2 元素 × 6 属性 × 双主题）+ 标签重判连带 4 处（deconstruction 2 个 SVG 标签 9→10px·顶条回流后修复器重判）。**D 211 处零 diff**；元素数双采无异常。
> **状态**：**已收官**（W869 118618fc·git 反填·共 2 笔·W971 存量回填）

### W870（2026-10-22）：设计迁移 B7 文本与思想 10 页（容器令牌化·朱砂实底合规·间距令牌化）

> **来源**：用户令「B5–B10 一次做完」，六批连做第三片。W870 = W826 §6 第七片（文本与思想 10 页）。
> - **文件**：site/data/text-evolution.html、site/data/text-search.html、site/data/linguistics.html、site/data/famous-time-travel.html、site/data/cultural-misreading.html、site/data/century-dialogue.html、site/data/counterfactual.html、site/data/philosophy.html、site/data/jurisprudence.html、site/data/karma-reincarnation.html、scripts/output/_w870_spec.json、scripts/output/_w870_accent_audit.json、scripts/output/_w870_diff_review.json、scripts/output/_w864_accent_exemptions.json、docs/00-导读/W批次编号对账表.md。
> - **A 容器**：十页 1320px 令牌化。
> - **B 朱砂实底**：KPI 顶条收敛四页（evolution 1 · linguistics 3→1 · misreading 4→1 · counterfactual 1 · karma 1）；`.seal` 十页转淡底。**33 处语义色片进豁免登记簿 W870 分册**：evo-step.first ×6（演化链条首步·位置编码）· linguistics 无类名色片 ×5 + mbti-card ×1 + char-card.c-buddhist ×3 · counterfactual validity-high ×7 · jurisprudence severity-pill ×8 + artifact-card.c-low ×2 · karma char-card.c-chusheng ×1。
> - **D 间距**：266 处（值保留）。
> - **C 渠与 `--chart-3` 值切换继续 defer** 至对比度专项批（本批文字落 bg 175 处·philosophy 46 / text-evolution 39 / cultural-misreading 21 为最多三页）。
> - **验收**：J2 大 before + 本批 after 双主题对拍 + 全量归渠。**判词：PASS——260 处 diff 全部归渠零剩余**：顶条 36 处 + `.seal` 220 处 + 标签重判连带 4 处（text-evolution 2 个 SVG 标签 9→10px）。D 266 处零 diff；元素数双采无异常。
> **状态**：**已收官**（W870 c000e406·git 反填·共 2 笔·W971 存量回填）

### W871（2026-10-22）：设计迁移 B8 跨学科与实验 10 页（容器令牌化·朱砂实底合规·间距令牌化）

> **来源**：用户令「B5–B10 一次做完」，六批连做第四片。W871 = W826 §6 第八片（跨学科与实验 10 页）。
> - **文件**：site/data/cognitive-psychology.html、site/data/social-media.html、site/data/business-model.html、site/data/game-webnovel.html、site/data/mbti-evolution.html、site/data/risk-project.html、site/data/concept-device.html、site/data/workplace.html、site/data/ethics-consumption.html、site/data/criticism-history.html、scripts/output/_w871_spec.json、scripts/output/_w871_accent_audit.json、scripts/output/_w871_diff_review.json、scripts/output/_w864_accent_exemptions.json、docs/00-导读/W批次编号对账表.md。
> - **A 容器**：十页 1320px 令牌化。
> - **B 朱砂实底**：KPI 顶条收敛六页（social 4→1 · business 1 · game 5→1 · mbti 4→1 · workplace 4→1 · ethics 5→1）；`.seal` 十页转淡底。**42 处语义色片进豁免登记簿 W871 分册**：cc-stat-fill ×10（数值进度条）· alert-badge ×7 · ipo-outcome ×5 · cipher-back ×5（翻卡背面皮肤·非网格顶条）· idev ×5 · veg-badge ×4 · 分类卡 ×3 · platform-badge ×1 · stage-btn.active ×1。
> - **D 间距**：350 处（值保留·六批最多）。
> - **C 渠与 `--chart-3` 值切换继续 defer** 至对比度专项批（本批文字落 bg 259 处）。
> - **验收**：J2 大 before + 本批 after 双主题对拍 + 全量归渠。**判词：PASS——308 处 diff 全部归渠零剩余**：顶条 80 处 + `.seal` 220 处 + 标签重判连带 8 处（social-media / workplace 各 2 个 SVG 标签 9→10px）。D 350 处零 diff；元素数双采无异常。
> **状态**：**已收官**（W871 f1197e31·git 反填·共 2 笔·W971 存量回填）

### W872（2026-10-22）：设计迁移 B9 视觉与叙事实验 10 页（容器令牌化·朱砂实底合规·间距令牌化）

> **来源**：用户令「B5–B10 一次做完」，六批连做第五片。W872 = W826 §6 第九片（视觉与叙事实验 10 页）。
> - **文件**：site/data/aesthetics.html、site/data/visual-art.html、site/data/cross-time-danmaku.html、site/data/emotional-heatmap.html、site/data/chart-design.html、site/data/perf-canvas-rendering.html、site/data/global-pattern.html、site/data/four-dimensional-research-network.html、site/data/four-heavenly-kings-artifacts.html、site/data/tag-cloud.html、scripts/output/_w872_spec.json、scripts/output/_w872_accent_audit.json、scripts/output/_w872_diff_review.json、scripts/output/_w864_accent_exemptions.json、docs/00-导读/W批次编号对账表.md。
> - **A 容器**：十页 1320px 令牌化（含 cross-time-danmaku 与 tag-cloud 两个级联页脚面页·只动 CSS 不动页脚）。
> - **B 朱砂实底**：KPI 顶条收敛六页（aesthetics 4→1 · chart-design 5→1 · global 4→1 · four-heavenly 5→1）；`.seal` 十页转淡底。**29 处语义色片进豁免登记簿 W872 分册**：scene-bar ×4（热力图行内数据条）· sc-cat ×5 · rc-size ×5（字号档位图例）· domino-card ×4（连锁隐喻展示卡·非列表网格）· domino-hardship ×3 · 分类卡徽章 ×4 · 选中态 ×2 · 主行动按钮 ×2。
> - **D 间距**：233 处（值保留）。
> - **C 渠与 `--chart-3` 值切换继续 defer** 至对比度专项批（本批文字落 bg 111 处·chart-design 与 emotional-heatmap 各 30 处）。
> - **验收**：J2 大 before + 本批 after 双主题对拍 + 全量归渠。**判词：PASS——344 处 diff 全部归渠零剩余**：顶条 108 处 + `.seal` 220 处 + 标签重判连带 16 处（global-pattern / four-dimensional 各 2 个 SVG 标签 9↔10px）。D 233 处零 diff；元素数双采无异常。
> **状态**：**已收官**（W872 5cb1b8b2·git 反填·共 2 笔·W971 存量回填）

### W873（2026-10-22）：设计迁移 B10 工具与检索 8 页（容器归并·朱砂实底合规·间距令牌化）

> **来源**：用户令「B5–B10 一次做完」，六批连做末片。W873 = W826 §6 第十片（工具与检索 8 页）——**数据+根 95 页迁移清单至此收口**。
> - **文件**：site/data/data-explorer.html、site/data/graph-explorer.html、site/data/search.html、site/data/material-archaeology.html、site/data/ming-political-thought-comparison.html、site/data/power-resources.html、site/data/magic-system.html、site/data/theological-intervention-network.html、scripts/output/_w873_spec.json、scripts/output/_w873_accent_audit.json、scripts/output/_w873_diff_review.json、scripts/output/_w864_accent_exemptions.json、docs/00-导读/W批次编号对账表.md。
> - **A 容器**：七页 1320px 令牌化；**theological-intervention-network 的 `.container` 1280 → `var(--container-content)` 1120**——§3.3「data 三页 1280」第三户（三户至此全部归并：semantic-network W866 / monster-background W867 / 本页）。
> - **B 朱砂实底**：KPI 顶条收敛四页（material 4→1 · ming 6→1 · theological 5→1）；**material-archaeology 的 8 张 artifact-card 网格顶条按裁决 2 收敛**（d3 生成·8 张全同色=装饰网格）；`.seal` 五页转淡底。**15 处语义色片进豁免登记簿 W873 分册**：rank-badge rank-S+ ×5（法术等级）· tag.palace ×3 · vt-btn/keytab.active ×4 · a.active ×2 · faction-card ×1。
> - **D 间距**：186 处（值保留）。
> - **C 渠与 `--chart-3` 值切换继续 defer** 至对比度专项批（本批文字落 bg 135 处·material 48 / magic-system 43 / power-resources 38）。
> - **验收**：J2 大 before + 本批 after 双主题对拍 + 全量归渠。**判词：PASS——216 处 diff 全部归渠零剩余**（5 页有 diff·data-explorer / graph-explorer / search 纯豁免与零变化令牌化故 0 diff）：顶条 88 处 + `.seal` 110 处 + 标签重判连带 10 处（material / theological）+ **容器归并连带 8 处**（theological 居中 margin 0→3.2px）。D 186 处零 diff；元素数双采无异常。
> **状态**：**已收官**（W873 0b56990b·git 反填·共 2 笔·W971 存量回填）

### W874（2026-10-22）：递延版段补写批（W865-W873 九段回写·号序链重新接上）

> **来源**：用户令「按建议走」，选「补段批先做」——W865（首页三任务区重组）与 B5-B10 六批全部递延，顶段停在 W864，`batch_cascade` 的「顶段+1」断言会拦住 B11。
> - **文件**：CHANGELOG.md、scripts/output/file-index.md、scripts/output/_w874_spec.json、docs/00-导读/W批次编号对账表.md。
> - **做法**：`backfill_changelog.py`（W842 建）第三次上岗。待补九段（W865-W873）——九批 spec 全部在位，无需新建补位 spec；工具按号序把每段插到「第一个号小于自己的段」之前，file-index 同批回写，规则行 W001-W864 → W001-W873。
> - **本批自身**：顶段推进到 W873 后，本批经 `batch_cascade` 正常立 W874 段并把「当前态六面」统一推进到 W874。
> - **不改历史**：只插入、不清洗、不重排、不改写既有段任何字符；不动页面与门禁判据。
> - **判词**：CHANGELOG 162→171 段 + 本批 W874 段（共 172）· file-index 同批 162→171 · 号序降序完好 · 九批的豁免区登记与对账表状态同步翻转。
> **状态**：**已收官**（W874 6e24428e·git 反填·共 2 笔·W971 存量回填）

