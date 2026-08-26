# 更新日志

本项目所有重要变更均记录于此。格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/)。

## [Unreleased]

> **W### 编号规则**：每个版本段标注唯一 W### ID（W001-W526），v0.8 内部细分 W008.1-W008.7（B0-B7）。每个 W 附四件套字段（来源/文件/验证/状态）。反向索引见 [scripts/output/file-index.md](scripts/output/file-index.md)（给定文件查改几次）。
>
> **历史版本归档**：v0.1 - v2.3.17（W001-W399）已迁移至 [docs/archive/CHANGELOG-ARCHIVE-tier2.md](docs/archive/CHANGELOG-ARCHIVE-tier2.md)（W513 二级归档）；W422 再归档 v2.3.18-v2.3.31（W400-W416）段；W511 归档 v2.3.32-v2.3.82（W417-W464）段 + v2.3.83（W484）段至 [CHANGELOG-ARCHIVE.md](CHANGELOG-ARCHIVE.md)。本文件仅保留 v2.3.84+（W485+）。
>
> **全站页数口径**（W459 起，各门禁分母不同）：HTML 共 234 页（site/data 87 + site/en 138 + site 根 9）；CSP 覆盖 233 页（排除 `_template.html`）；check_js_syntax/check_structure 扫 232 文件（再排除 `_shell.html`）；inline_css 同步 225 页（site/data + site/en，site 根以 `<link>` 引外部 css）；「可视化页 86」= site/data 87 减 `_shell.html`。
>
> **维护契约**：① 已发布版本段（历史）只增不删、禁改；② 新版本段插入/重排只用脚本 + 结构断言（锚点唯一性 + 版段 order 校验），勿手工 Edit 大段；③ 每段保持四件套（来源/文件/验证/状态），建议单段 ≤ 25 行（超长拆「执行/验证/范围纪律」分条）；④ 新批编号先 Grep 现役段取 max+1 再写（防撞号）。

### v2.3.125（2026-08-26）：W526 索引健康门禁盲区封堵 — 段倒序断言 + 段缺失检测 + 旁文档同步第 23 门禁

> **来源**：W525 漂移审查实证三项漏网（file-index 段缺失/段乱序、workflows README 滞后）均未被既有门禁拦截——第 17 门禁只防空壳/重复/残留，不查缺失与顺序；旁文档在 verify 覆盖外。用户指令「把三项都补进门禁」驱动本批。
> - **执行（check_index_health 第 6 项）**：段倒序断言——豁免区外段必须 W 号严格递减（最新在前），W525 曾实证 W522-W524 尾部追加；负样本实测拦截（W519 置于 W524 前被抓）。
> - **执行（check_index_health 第 7 项）**：段缺失检测——CHANGELOG 每个现役版段必须都有 file-index 登记段，豁免区外缺失即 FAIL；负样本实测拦截（删 W504 段被抓）。修复过程中发现并修正：新增正则误用全角问号「？」导致解析失败（E1 铁律实证——写完必须负样本验证）。
> - **执行（verify_delivery 第 23 门禁）**：旁文档同步门禁——.github/workflows/README.md 头部版本行（vX.Y.Z W###）== 现役段 + 里程碑行 W450-W### 上限 == 现役 W，任一不符 FAIL；负样本实测拦截（头部改 v2.3.120 被抓）。
> - **文件**：scripts/check_index_health.py（检查 6/7 新增）、scripts/verify_delivery.py（第 23 门禁新增）、.github/workflows/README.md、docs/00-导读/文档规范.md、AGENTS.md、六文档。
> - **验证**：负样本 3/3（倒序/缺失/旁文档全拦截）；正样本 check_index_health exit=0（49 段）·verify_delivery 全绿。
> - **状态**：已落地（待提交）。

### v2.3.124（2026-08-26）：W525 漂移审查修复 — drift-audit 全仓体检 P1/P2 处置（file-index 结构修复 + 旁文档同步 + 门禁表对齐）

> **来源**：用户要求审查可信度轨落地（W501-W505）有无错误/优化点 → drift-audit 全仓体检发现 3 项 P1 + 1 项 P2（门禁全绿 ≠ 无漂移实证：第 17 门禁不查段缺失/不查顺序、旁文档不在 verify 覆盖内）。
> - **执行（P1-1/P1-2 file-index 修复）**：W504 段缺失补建（登记 611 篇打标 + 学术轨 105 篇补引文 + 3 一次性脚本 + 报告产物）；W522/W523/W524 三段从文件尾部剪切、倒序归位至 W521 之前（原为 bump 后手工插入定位错误追加到 W449 段后），三段尾部 bump 残留「当前版本」快照行删除（符合 W500 门禁"最新段残留必 FAIL"意图）。
> - **执行（P1-3 旁文档同步）**：workflows/README.md 头部版本行 v2.3.113 W514 → v2.3.123 W524，里程碑行 W450-W503 → W450-W524（补 W504-W524 摘要）——W499 修同型问题后再度复发的滞后。
> - **执行（P2-1 门禁表对齐）**：文档规范 §8 门禁表补漏列两项（学术研究轨显式引用 105 篇 + site/data 回退模式），与 AGENTS §4.2 22 条编号对齐（原自称 22 项却枚举 23 项且漏两门禁）。
> - **文件**：scripts/output/file-index.md（段重排 + W504 补段 + W525 段）、.github/workflows/README.md、docs/00-导读/文档规范.md、site/dukou-engine.html、六文档。
> - **验证**：check_index_health 通过（48 段 · 最高 W524 · 无重复）；verify_delivery 全绿。
> - **状态**：已落地（待提交）。

### v2.3.123（2026-08-25）：W524 bump 追加污染坑位补记 — --desc/--note 双触发固化（用户指令驱动）

> **来源**：W523 批收尾实测发现 bump_version.py `--note` 参数同样向 STRUCTURE.md 头部 / docs/00-导读/项目说明.md 的上一版本行**追加**「 + W523（…）」残留——AGENTS §4.3 此前仅登记 `--desc` 单触发面；用户指令「现在补记到 AGENTS.md 并再发一版」驱动本批。
> - **根因**：bump_version.py 对 `--desc` 与 `--note` 共用同一追加路径，坑位登记只覆盖 `--desc` 形成盲区；另全局替换会在 file-index 历史段生成空壳段（重复标题无内容待手工补全）——两现象均多次复现。
> - **修复**：AGENTS §4.3 bump_version 条目修订（已知坑②扩为 --desc/--note 双触发 + 坑①补充空壳段现象）；六文档 + AGENTS 版本脚注 + dukou-engine.html 页脚全量同步至 v2.3.123 W524。
> - **验证**：verify_delivery.py 当批现测核心全绿 0 WARN（验收数字当批现抄）；本次推送含 site/dukou-engine.html ∈ site/** → pages/perf/screenshot-review 三 workflow 必触发，Screenshot Review 预期命中 W421 内部 skip 分支（页脚/doc-only ~1min）——该机制首次运行时实证。
> - **影响**：后续任何批次跑 bump_version.py 后，无论 --desc 还是 --note 都必须 Grep 校验 STRUCTURE 头部 / 项目说明 / file-index 三处并手工净化；W421 提速机制获得运行时背书。
> - **文件**：AGENTS.md、CHANGELOG.md、交接文档.md、README.md、STRUCTURE.md、docs/00-导读/项目说明.md、scripts/output/file-index.md、site/dukou-engine.html。
> - **状态**：已落地（2026-08-25）；CI 五跑观察结果随批记录。
### v2.3.122（2026-08-25）：W523 截图审查恒全量根因修复 — scope diff 加 core.quotePath=false（用户提问驱动）

> **来源**：用户问「为什么每次 Screenshot Review 都这么慢」→ 取证链：job steps API 各步 conclusion 均 success（非 skipped）+ 运行日志「Found 87 visualization pages + 2 top-level pages」证实执行了全量；而 site 相关 diff 仅含页脚豁免的 dukou-engine.html，理应 skip。
> - **根因**：git 默认 core.quotePath=true 把中文路径输出为带双引号的八进制转义串（如 "\344\272\244\346\216\245\346\226\207\346\243\243.md"＝交接文档.md），在 scope 步骤 bash case 中不匹配任何免审模式（连 *.md / docs/* 都失配——首尾引号破坏 glob）→ 落入 *) 保守全量；铁律 #1 要求每批同步交接文档.md（中文文件名）→ 每次推送必然触发 ~11min 全量截图（run 32849348659 实测 11m07s；历史近 40 次成功 run 仅纯 ASCII 的 W478 批 2.4m 命中过定向档）。
> - **修复**：screenshot-review.yml scope 步骤三处 git diff 调用点（push 零 SHA 兜底 HEAD~1 / push BEFORE..SHA / PR base...sha）统一加 -c core.quotePath=false，中文路径按原始 UTF-8 输出正常命中免审模式。
> - **验证**：本地 Git Bash 复刻 yml case 块逐字逻辑，对 W522 实际范围（16a1911..6a47804）双向模拟——旧命令两条中文路径均落 *) 判 needed=true scope=full（精确复现）、新命令 docs/* 与 *.md 双命中判 needed=false scope=skip；全 workflows 排查确认 git-diff 路径分类仅此一处，无同类隐患。
> - **影响**：此后纯 docs/页脚-only 批次 CI 截图审查由 ~11min 降为秒级 skip；本批因含 workflow 自身变更仍按设计走一次全量，属预期。
> - **文件**：.github/workflows/screenshot-review.yml（三处调用点 + 注释一行）。
> - **状态**：已落地（2026-08-25）；修复后 CI 首跑待观察。
### v2.3.121（2026-08-25）：W522 CI 红灯修复 — scripts/ ruff 16 错误清零（E41 远端核对发现）

> **来源**：新 session 启动按 E41 铁律核对远端状态，发现本地 main 领先 origin/main 25 个提交（W504-W521 全部未推送）、远端最后一次 CI（W503 run 32746567085）Code Quality FAILURE 且在当前 HEAD 仍复现；Unit Tests 收集失败项（test_fix_svg_negative_widths.py ImportError）已由 W506 删除该测试根治。用户批复「修完再推」。
> - **根因**：inject_goatcounter.py:68 `.replace('\', '/')` 反斜杠转义闭引号致字符串未闭合（W425 GoatCounter 注入脚本·级联 4 个 invalid-syntax）+ 12 个普通 lint 分布 7 文件（F841×1 / F401×2 / B905×1 / UP009×4 / E401+I001×2）。
> - **修复（行为零变更）**：inject_goatcounter.py `'\\'` 还原本意（Windows 分隔符→正斜杠）；check_dynamic_links.py self_test 删未用变量 good_rel；check_glossary.py diff_c1 zip 补 strict=True（前置分组序列守卫已保证等长）；其余 10 处 ruff --fix 自动修复（F401 删未用 import re/subprocess、UP009 删冗余 UTF-8 声明 ×4、extract_strings 与 validate_en import 拆行排序）。
> - **文件**：scripts/ 8 个（inject_goatcounter / check_dynamic_links / check_glossary / check_governance_docs / check_motion_ban / check_token_coverage / extract_strings / validate_en）+ 六文档 + AGENTS.md 脚注。
> - **验证**：ruff check scripts/ 16→0 All checks passed；git diff --stat 范围核对恰好 8 目标文件（+8/-11）零越界；pytest 收集 302 正常；verify_delivery.py 当批现测核心全绿。
> - **状态**：已落地（2026-08-25）。

### v2.3.120（2026-08-25）：W521 存量裸字面量清剿 + W463 三坑补登记（P2 两项用户批复执行）

> **来源**：W520 收尾汇报两项 P2 待确认（DRL F2 全树存量清剿 + E45 编号空间完整化），用户批复「执行」。
> - **执行（提案 1·存量裸字面量清剿）**：DRL F2 class-level enumeration 15 文件逐项按 E2/门禁依赖/检查指引三分类裁决——真现状声明改引用式（en-translation L149 / character-content desc / characters-knowledge L45 / roster L1 / skills/README L17 / version-bump SKILL desc）+ 现役口径/检查指引加注「随批次校正、以实际为准」（drift-audit SKILL L100 + reference L79 / plan-review L102 / visual-batch L50 / quality-gates L22）+ 门禁回写模板/历史批次记录豁免（version-bump reference 固定串、visual-batch 批次验收）。
> - **执行（提案 2·W463 补登记）**：交接文档「三」新增 W463 段（E45 W 批收尾三坑——bump --desc 追加污染 / CHANGELOG 大段手工编辑 / 版本号撞号，三 bullet 模板 + 补登记标识），使编号空间完整（W520 段 E46 顺延的占用方现已在「三」区可见）。
> - **文件**：skills 10 文件（character-content SKILL+quality-gates / characters-knowledge SKILL+roster / drift-audit SKILL+reference / en-translation / plan-review / version-bump / visual-batch SKILL，sync_skills --sync 双轨一致）+ 交接文档.md。
> - **验证**：W520 规则落点 Grep 复核 13 处 0 遗漏；sync_skills --sync 输出「10 个文件更新」+「仓库版与全局版完全一致，无漂移」；pytest 全量 302 passed（基线不变·本批未触碰 Python/测试代码）；verify_delivery.py 当批现测核心全绿。
> - **状态**：已落地（2026-08-25）。

### v2.3.119（2026-08-25）：W520 递增数字禁字面量 + skills 内文数字比对维度（P2 三提案用户批复落地）

> **来源**：W519 交付后用户指令「你先复盘一下这次都出现了哪些问题，以后怎么避免重复出现类似错误」→ self-evolution 全面复盘产出 P2 三提案，用户批复「执行」授权按新批次落地。
> - **执行（提案 1·写作侧根治）**：plan-authoring SKILL 去模糊化成文标准新增第 5 条「递增数字引用式」（随批次演化的计数在现役状态描述中禁写无时点锚裸字面量，一律引用式表述或绑定实测时点与来源）+ 陷阱清单同步 + 完成验证清单新增自查项（version 1.1.0→1.2.0）；day-review SKILL 步骤 4 新增第 8 条「递增数字字面量扫描」+ 陷阱 9（version 1.1.0→1.2.0）。
> - **执行（提案 2·体检侧兜底）**：drift-audit SKILL 步骤 5 第 4 条由「skill 内部数字引用」扩展固化为「skill 内部数字引用 vs 权威值比对」固定维度（对照 verify 输出/README/统计口径说明三权威源 + 无时点锚裸字面量 = P2）；reference.md 步骤 5 命令区新增 3 条排查命令 + 案例库「举一反三型」新增 W520 扩展段（结构性盲区收编）（version 1.0.0→1.1.0）。
> - **执行（提案 3·经验沉淀）**：交接文档「三」新增 W520 段（E46 递增数字禁字面量·三 bullet 模板·复现计数器 3/3；E45 已由 W460-W463「W 批收尾三坑」在 project_memory 占用——未登记「三」区，顺延 E46 并注明）。
> - **执行（自体病例治愈）**：day-review 验证清单「六项核对完成」→「逐项以步骤 4 现行清单为准」（清单实为 7 条仍写「六项」的自体漂移）；drift-audit reference「修复后验证」区「17 门禁全绿」→「全部门禁全绿（随批次递增，以输出为准）」。两处均为「递增数字字面量」规则的活体病例，同批治愈以证规则落地。
> - **文件**：skills/xiyouji-plan-authoring/SKILL.md、xiyouji-day-review/SKILL.md、xiyouji-drift-audit/SKILL.md + reference.md（4 文件 sync_skills --sync 双轨一致）+ 交接文档.md。
> - **验证**：三 skill 修改处 Grep 复核 0 遗漏（限定新增文本范围）；sync_skills --sync 输出「4 个文件更新」+「仓库版与全局版完全一致，无漂移」；pytest 全量 302 passed（基线不变·本批未触碰 Python/测试代码）；verify_delivery.py 当批现测核心全绿。
> - **验证（DRL 复验补充）**：deep-review-loop 全流程（R1a 3 verifier + R1b 对抗 + R2 独立审计）发现并修复 8 项——F1 规则补「门禁依赖豁免」边界（verify_delivery EXPECT_A4「209 篇」/README「共 N 篇」为门禁解析目标禁改引用式，三 skill 规则同补）+ P2-1/P2-2 reference 排查命令实测修正（`ls -d skills/*/` 全量 19 含 4 会话流程 skill + grep 改可命中模式）+ P2-3 防线口径统一「两道」（交接文档「三道」→「两道」）+ P2-4 扫描范围补 AGENTS.md + P3-5 补 E2 判据指针 + P3-6 案例批次归属修正 + F3 验证措辞限定 + version-bump reference:26 错锚快照（「W425 时」锚点/当前值错位）修正；F2 全树 ~30 处存量裸字面量治理按边际收益 gate 接受残留单列 W521。
> - **状态**：已落地（2026-08-25）。

### v2.3.118（2026-08-25）：W519 Skills 全目录审查与 SKILL.md 内容优化（A+B+C+D 用户批复全量）

> **来源**：用户指令「d:\1\xiyouji/skills 把这个文件夹里面的内容审查一遍，其中要把 skill.md 的内容进行优化」——通读 19 个 SKILL.md + 配套文件后识别四类问题，经 AskUserQuestion 两问批复：Q1 选「A+B+C 全部修复」，Q2 选「D 类一并纳入」。
> - **执行（A 类·计数漂移 14 处）**：211→215 ×4（characters-knowledge roster.md 标题 / 同 SKILL.md 角色名录行、character-content desc、skills/README.md 索引表 roster 计数）；共 611→共 615 ×10（version-bump SKILL.md ×3 + reference.md ×4、en-translation 收尾提示 ×1、drift-audit SKILL.md 启动 Prompt 计数转述示例 ×1 + reference.md 排查命令示例 ×1·经核实启动 Prompt 已是 615 口径）。
> - **执行（B 类·门禁数去硬编码 8 处）**：drift-audit SKILL.md ×4 + reference.md ×3 + day-review SKILL.md ×1——按 drift-audit 自身药方，将「现 17 条」类硬编码改为「全部门禁（随批次递增、以 verify 输出为准）」表述；其 reference.md:138 历史案例引文按 E2 判据（历史事件描述保留旧值）保留不动。
> - **执行（C 类）**：AGENTS.md §3 目录树注释「playbook skill（17 个）」→「（19 个）」（README 索引与 §4.5 分类清单本就正确，仅树注释漏更）。
> - **执行（D 类·frontmatter 补齐 7 文件）**：角色 5（sun-wukong/zhu-bajie/sha-seng/tangseng/bai-longma）+ 内容/知识 2（character-content/characters-knowledge）各新增顶层 `version: 1.0.0`——现 15 skill 具顶层 version；4 会话流程组维持 metadata 嵌套风格不动。zhu-bajie/tangseng description 不补「外传」词（E1 实测两组配套文件与 docs/02 均无外传内容，硬补即虚假声明）。
> - **文件**：skills/ 下 15 文件（xiyouji-version-bump SKILL+reference、en-translation、characters-knowledge SKILL+roster.md、character-content、drift-audit SKILL+reference、day-review、角色 5 SKILL、skills/README.md 索引表）+ AGENTS.md；技能目录内 14 文件经 sync_skills.py --sync 同步全局双轨一致零漂移，skills/README.md 为仓库权威索引（同步脚本范围外）。
> - **验证**：陈旧计数全 skills 复扫二轮（611/211 双模式）0 残留；门禁数历史案例引文 reference.md:138 按 E2 判据保留不动；`^version:` 计 15 处无重复；pytest 全量 302 passed（基线不变·本批未触碰 Python/测试代码）；verify_delivery.py 当批现测核心全绿。
> - **状态**：已落地（2026-08-25）。

### v2.3.117（2026-08-25）：W518 期望版本动态化 + 尾页脚新鲜度门禁（用户批复两项遗留候选）

> **来源**：W515 收尾报告两项遗留候选经用户逐条批复授权（「1.纳入 day-review 步骤清单或轻量校验。2.改为动态取最新版」）。根因一：verify_delivery 六文档期望版本锚定 dukou-engine.html 页脚（滞后型手工工件，辅助文档升版反报「不含旧版」噪音 WARN）；根因二：交接文档「最后更新」链（头部滚动链 + 尾页脚历史链两处）W505-W517 多批连续漏更（本批检查部署即拦下活体：头部链首 v2.3.115 W516、尾页脚链首 v2.3.114 W515，双双落后现役段 W517）。
> - **执行（项②·TDD）**：verify_delivery.py 新增纯函数 latest_version_from_changelog（`^###\s+v…（…）：\s*W…` 取倒序首段＝现役段）与 parse_footer_version；main() 期望 ver/wnum 改由 CHANGELOG 动态推导（解析失败 FAIL），dukou-engine 页脚降级为新鲜度被检对象（落后现役段仅 WARN 不阻断）；六文档核心 2 FAIL／辅助 4 WARN 与范围漂移语义不变。
> - **执行（项①）**：check_governance_docs.py 新增检查 7 footer_freshness_issues——交接文档全部「最后更新」行（头部滚动链 + 尾页脚历史链）链首条目须均 == CHANGELOG 现役段（finditer 全量扫描·部署即拦下活体：头部 W516 / 尾页脚 W515 双双漏更），不一致报 issue（caller 维持 WARN 起步策略）；day-review SKILL.md 步骤 4 新增第 7 条清单项（随批前置·只前置不回填）+ version 1.1.0，sync_skills --sync 已同步全局。
> - **文件**：scripts/verify_delivery.py、scripts/check_governance_docs.py、skills/xiyouji-day-review/SKILL.md（+全局同步）、tests/test_verify_delivery_version.py（新建）、六文档、AGENTS.md（§4.2 第 1/22 条+脚注）、docs/00-导读/文档规范.md（§8 门禁数 20→22+动态版本源口径）、site/dukou-engine.html 页脚。
> - **验证**：TDD 红→绿（新增测试 11 个）；pytest 全量 302 passed（基线 291＋11）；py_compile 双脚本通过；verify_delivery 当批现测——治理检查 7 部署即命中活体漂移（WARN 拦截），文档同步后全绿。
> - **状态**：已落地（2026-08-25）。

### v2.3.116（2026-08-25）：W517 共享机制载体铁律 — 仓库内文件为真源（W516 载体错误教训固化）

> **来源**：2026-08-25 会话——W516 将上移机制写入全局版 mem-wrap-up（`c:\Users\...\.trae-cn\skills\`），用户指出「其他 Agent 读不到你的 mem-wrap-up SKILL.md」，实证项目 session 读的是仓库版且 `sync_skills.py` 为仓库→全局单向（全局修改会被覆盖）。
> - **执行（规则固化）**：AGENTS §4.3 新增「共享机制必须写入仓库内文件（git tracked）」规则——禁止只写全局路径；改 skills/ 下任何 skill 必须改仓库版后 `sync_skills.py --sync` 同步全局。
> - **执行（登记）**：交接文档「三」新增 W517 段（经验名 + 处置 + 复现计数器）。
> - **执行（修正补记）**：W516 载体错误本身已于 commit 72a9276 修正（上移映射表重写入仓库版 mem-wrap-up + sync 覆盖全局版），本批为教训固化。
> - **文件**：AGENTS.md、交接文档.md、CHANGELOG.md、scripts/output/file-index.md、README/STRUCTURE/项目说明/site/dukou-engine.html。
> - **验证**：AGENTS §4.3「共享机制必须写入仓库内文件」落地；交接文档「三」W517 段落地；verify_delivery 核心全绿；pytest 291 passed。
> - **状态**：已落地（待提交）。

### v2.3.115（2026-08-25）：W516 经验上移机制固化 + 剩余经验补上移（E44/E34/E41/E36-42）

> **来源**：2026-08-25 会话「Memory 经验上移项目机制后续怎么做」——盘点发现上移机制仅一次性（W509），无周期性触发点；memory 中尚有 E44/E34/E41/E36-42 五组高价值经验未进项目公共载体。
> - **执行（机制固化）**：mem-wrap-up Step 5 毕业路径强化——新增「上移映射表」（规则→AGENTS §4.3/§6、批次方法论→交接文档「三」、深度篇→docs/10-方法论沉淀/、流程→skills/、工具→scripts/）+ 强制登记交接文档「三」（杜绝"上移了但项目内查不到"）。每批收尾自动执行，不依赖 user 询问。
> - **执行（补上移）**：交接文档「三」新增 W516 段登记 E44（三 skill 触发门控三时刻）/ E34（PowerShell heredoc 替代）/ E41（跨 session 先确认远端）/ E36-42（workflow/CI 类 7 条）；AGENTS §4.3 补录 Windows heredoc 禁（Write 临时文件 + -F 参数）+ 跨 session 先确认远端 两条工具链规则。
> - **文件**：AGENTS.md、交接文档.md、CHANGELOG.md、scripts/output/file-index.md、README/STRUCTURE/项目说明/site/dukou-engine.html。
> - **验证**：mem-wrap-up 全局版 L149-150 含「上移映射表」+「W516 强化」；交接文档「三」W516 段落地；AGENTS §4.3 两条新规则落地；verify_delivery 核心全绿；pytest 282 passed。
> - **状态**：已落地（待提交）。

### v2.3.114（2026-08-25）：W515 渲染抽查常驻化 + 门禁正文引用存在性检查

> **来源**：W514 复盘沉淀 P2 两项（用户确认执行）：① 渲染抽查模式常驻为 scripts/render_check.js 并修复 xiyouji-day-review 两处 `_shot_check.js` 失效指针（脚本删除后失效指针静默存活多批·X4 类腐化）；② check_skills_index.py 扩展「skill 正文引用资产存在性」检查。
> - **执行（P2②·TDD）**：check_skills_index.py 新增检查 5——SCRIPT_REF_RE 提取 skills/**/*.md 正文中的 scripts/*.py|.js 引用（尾部前瞻防 .json 被误切成 .js）对磁盘断言；DEFAULT_ALLOWED_MISSING 冻结豁免 3 个文档示意占位名（scripts/xx.py、scripts/脚本A.py、scripts/脚本B.py）；新增 tests/test_skills_reference_integrity.py（9 测试：提取 4 + 缺失判定 4 + 真实仓库冒烟 1）。指针修复前实跑 exit 1 精确报出缺失 2 处。
> - **执行（P2①）**：新增 scripts/render_check.js（Playwright 常驻抽查：--page 可重复 / 内容断言 / styled 背景非透明 / 390·414 视口溢出 / pageerror 全计失败 / console 白名单放行 file:// 设计内回退 / --dark 暗色截图）；dukou-engine.html 冒烟 exit 0（bg=rgb(250,247,240) 命中 --paper #faf7f2、双视口溢出 0，light+dark 双截图落盘）。指针修复：xiyouji-day-review SKILL.md L59 与 reference.md L42 改指 node scripts/render_check.js。
> - **文件**：scripts/check_skills_index.py、scripts/render_check.js（新建）、tests/test_skills_reference_integrity.py（新建）、skills/xiyouji-day-review/SKILL.md、skills/xiyouji-day-review/reference.md、六文档。
> - **验证**：pytest 全量回归通过（含新增 9 测试）；py -3 check_skills_index.py exit 0（md 51 个 / 引用 51 条 / 缺失 0——修复前缺失 2）；node --check 过；verify_delivery.py 核心全绿。
> - **状态**：已完成（2026-08-25）。

### v2.3.113（2026-08-25）：W514 治理文档口径修复 — 五元文档数字校正与门禁清单补录

> 方案档：docs/superpowers/plans/2026-08-25-w514-governance-doc-consistency-fix.md

- **来源**：W505（commit cd6d7b8）向 docs/02 追加 4 篇方向二深化文档，磁盘计数 611→615、A3 211→215、CSP 覆盖页 1173→1189；README 已同步而其余元文档漏更，且统计口径说明 §2 与 CHANGELOG W459 口径块自相矛盾（87 vs「86 含 _shell」）。
- **执行**：五元文档共 18 处单点替换（新Agent启动Prompt ×4、AGENTS ×6、统计口径说明 ×6、文档规范 ×1、项目说明 ×1）+ 六文档同步组 S1-S6；AGENTS §4.2 补录第 21 门禁 check_dynamic_links.py（动态链接）与第 22 门禁 check_governance_docs.py（治理文档维护契约）登记。
- **验证**：verify_delivery.py 全绿；陈旧模式全仓扫描 0 残留（方案档 §4 表 A2）；保护位反向抽查通过（方案档 §0.3）；generate_csp.py --check 0 漂移。
- **状态**：已完成（2026-08-25）。

### v2.3.112（2026-08-25）：W513 归档二级归档（方案 A）— CHANGELOG-ARCHIVE W001-W399 下移 tier2

> **来源**：W511 审查时识别归档文件持续增长（CHANGELOG-ARCHIVE 900KB / file-index-archive 646KB / 交接文档-archive 269KB），用户采纳方案 A（内容二级归档：archive 超 1MB 时最老块下移二级层）。
> - **执行**：`scripts/_w513_archive_tier2.py` 将 CHANGELOG-ARCHIVE.md 的 W001-W399 原始块（L8-L4602·4595 行·745KB）迁移至新建 `docs/archive/CHANGELOG-ARCHIVE-tier2.md`（自含头部 + 指向现役/中间层指针）；CHANGELOG-ARCHIVE.md 保留 W400+ 归档段（W422/W511 段）并更新头部标注（标题改「W400+」+ 二级归档指针）。**917KB → 150.4KB**。
> - **执行（门禁联动）**：verify_delivery.py `ARCHIVE_DOCS` 新增 tier2 文件（W001-W399 仍纳入范围漂移可追溯扫描，避免误报）。
> - **执行（规范固化）**：文档规范 §5 新增「二级归档」规则（归档三件套任一 >1MB → 最老块迁 `docs/archive/<原名>-tier2.md` + 登记 ARCHIVE_DOCS + tier2 历史段同受禁改约束）；§8 健康指标表新增「归档三件套 >1MB → 二级归档」。
> - **文件**：CHANGELOG-ARCHIVE.md、docs/archive/CHANGELOG-ARCHIVE-tier2.md（新建）、scripts/verify_delivery.py、docs/00-导读/文档规范.md、scripts/_w513_archive_tier2.py（入库）、六文档。
> - **验证**：CHANGELOG-ARCHIVE 917→150.4KB；tier2 745.7KB 结构完整（自含头部+W001-W399）；verify_delivery 核心全绿（含 tier2 入 ARCHIVE_DOCS 后范围漂移正常）；pytest 282 passed。
> - **状态**：已落地（待提交）。

### v2.3.111（2026-08-25）：W512 CI 安全批次 — security_scan pip-audit 超时误报修复（DEP-001 归零）

> **来源**：W511 审查时 security_scan --all 实测发现 pip-audit「1 漏洞」，排查确认为 `security_scan.py` 内 pip-audit 子进程 **120s 超时**误报（非真实依赖漏洞）——单独 `pip_audit --timeout 300` 实测「No known vulnerabilities found」，用户确认处理。
> - **执行**：`scripts/security_scan.py` `_run_audit_on_requirements` 的 pip-audit `timeout=120 → 300`（pip-audit 首次需下载 advisory 数据库，120s 不足）。
> - **验证**：重跑 `security_scan.py --all`——DEP-001 **0**（此前 1）；耗时 124s → **40.8s**（数据库已缓存）；high=0 medium=261（259 XSS-001 存量 innerHTML 噪音 + 2 API-004 均为 security_scan.py 自身工具代码 verify=False，非生产代码；真实依赖漏洞 = 0）。
> - **文件**：scripts/security_scan.py、六文档。
> - **状态**：已落地（待提交）。

### v2.3.110（2026-08-25）：W511 治理文档健康指标归档 — 三文档超阈值瘦身（CHANGELOG/file-index/交接文档概要）

> **来源**：W510 审查登记的健康指标超标待办（CHANGELOG 810 行/158KB · file-index 958 行/82KB · 交接文档里程碑概要 408 行 均超 §8 阈值），用户确认处理。
> - **执行（CHANGELOG 归档）**：迁移 W417-W448（v2.3.32-v2.3.63）段 + W449-W464（v2.3.64-v2.3.82）段 + W484（v2.3.83）段至 CHANGELOG-ARCHIVE.md（脚本 `_w511_archive.py` + `_w511_archive2.py`，按 W422 归档段先例追加 `## W511 归档段`/`## W511 归档段-2` 块）；现役 158KB/810 行 → **49KB/235 行**；顺带修复 W417 段缺失标题（`### v2.3.32` 标题补全）。
> - **执行（file-index 归档）**：迁移 W417-W448 段 + W449-W463 损坏区尾部清理至 file-index-archive.md（脚本 `_w511_archive.py`）；现役 82KB/958 行 → **35.8KB/335 行**。
> - **执行（交接文档概要）**：里程碑概要保留最近 5 版（v2.3.105 W506 - v2.3.109 W510），W505 及更早 405 行归档至 交接文档-archive.md（脚本 `_w511_trim_summary.py`）；概要 408 行 → **19 行**。
> - **文件**：CHANGELOG.md、CHANGELOG-ARCHIVE.md、scripts/output/file-index.md、scripts/output/file-index-archive.md、交接文档.md、交接文档-archive.md、scripts/_w511_*.py（3 个归档脚本入库）、六文档。
> - **验证**：三文档体积/行数实测达标（<50KB/<500 行）；verify_delivery 核心全绿（含范围漂移/引文 423 条 100%）；pytest 282 passed。
> - **状态**：已落地（待提交）。

### v2.3.109（2026-08-25）：W510 治理文档修复 — 文档规范门禁数 17→20 + 核心口径统一 + 健康指标超标登记

> **来源**：用户审查文档规范.md 发现 3 处问题（P1-1 §8 门禁数 17 项遗漏 W501-503 三项 / P2-1 §11.4「核心 6 文档」口径与 §11.1「核心 2」矛盾 / P1-2 §8 健康指标超阈值未归档），确认修复。
> - **执行（§8 门禁数）**：17 项 → 20 项，列举补元信息块 v2（W501）/ 术语一致性（W502）/ 原著引文硬验证（W503）——与 AGENTS §4.2 对齐。
> - **执行（§11.4 口径）**：第 9 项「核心 6 文档版本」→「六文档含页脚 v/W（核心 2 硬门禁 CHANGELOG+交接文档 · 辅助 4 WARN）」——与 §11.1 统一。
> - **执行（健康指标登记）**：CHANGELOG 643 行/158KB · file-index 772 行/82KB · 交接文档里程碑概要 408 行 均超 §8 阈值但未归档——规则本身正确（超标即行动），属执行缺口，登记为待办（下批归档批次处理）。
> - **文件**：docs/00-导读/文档规范.md、六文档。
> - **验证**：文档规范门禁数/口径 Grep 一致性通过（§8 20 项 = AGENTS §4.2 20 项）；verify_delivery exit 0。
> - **状态**：已落地（待提交）。

### v2.3.108（2026-08-25）：W509 经验上移共享 — memory 规则进项目公共载体（防多 Agent 重复犯错）

> **来源**：用户问「memory 经验有哪些可进项目目录、如何让多 Agent 避免重复犯错」——按 W070 上移模式，把 agent 私有层（experience-log/quickref/project_memory）的高价值规则同步进项目公共载体。
> - **执行（AGENTS.md）**：§4.3 工具链要点新增 3 条强制规则——批量改 md 禁 PowerShell Set-Content（BOM）/同文件多 Edit 必须串行/写引文前先跑 `_cite_probe.py` + 变体称谓须带 canonical；§6 铁律新增第 13 条「内容可信度轨」（引文/术语/归档查测试/管线校验汇总）。
> - **执行（交接文档）**：「三、方法论沉淀」登记 W505-W508 内容可信度轨四类规则 + W507-W508 复盘行动项闭环方法论（memory→项目 上移机制）。
> - **文件**：AGENTS.md（§4.3/§6 规则）、交接文档.md（三、方法论沉淀）、六文档。
> - **验证**：AGENTS 维护契约 Grep 通过（骨架/去重/脚注/HEAD 一致）；verify_delivery exit 0。
> - **状态**：已落地（待提交）。

### v2.3.107（2026-08-25）：W508 复盘剩余项收口 — 管线协议去重 + 管线一致性轻量校验

> **来源**：W501-W506 全面复盘（2026-08-25 retrospective）剩余 P2/P3 项落地——P2-6（SKILL 管线章节 ↔ creative-methods.md 方法四去重互指）+ P3-7（管线执行轻量校验）。
> - **执行（P2-6 去重）**：creative-methods.md 方法四改为「速查摘要 + 指向 SKILL.md 创意三明治管线章节为协议单一事实源」；修正数字漂移（方法四原「50 个切入点」vs SKILL「≥20」已统一为指向 SKILL）。
> - **执行（P3-7 校验）**：新建 scripts/_check_pipeline_consistency.py（_ 前缀不入库门禁）：C1 管线标记存在性 / C2 生成来源须以 `创意三明治管线@` 开头（禁 character-content@）/ C3 引文 ≥3 条；character-content SKILL Step 4 新增第 7 步管线一致性检查。
> - **文件**：scripts/_check_pipeline_consistency.py（新）、skills/xiyouji-character-content/SKILL.md + references/creative-methods.md（sync_skills 已同步全局版）、六文档。
> - **验证**：_check_pipeline_consistency.py 全量扫描 615 文件 exit 0（4 篇管线文档 PASS：生成来源 创意三明治管线@cd6d7b8 · 引文 3 条各）；sync_skills --check 漂移 0；verify_delivery exit 0；pytest 282 passed。
> - **状态**：已落地（待提交）。

### v2.3.106（2026-08-25）：W507 复盘沉淀落地 — 引文探针永久化 + 归档查测试规则入 skill

> **来源**：W501-W506 全面复盘（2026-08-25 retrospective）P2 项落地——E-A 引文探针永久化 + E49 归档脚本查 tests/ 引用规则。
> - **执行（引文探针）**：新建 scripts/_cite_probe.py（由 _w505_probe_cites.py 改进为通用参数化：--kw 多关键词/--chap 回目区间/--min-len/--max-len/--frag 片段模式），写 `> 原文引文` 前从 text-search.json 提取候选句，禁止凭记忆编造引文（W505 高翠兰篇编造 FAIL 教训）。
> - **执行（skill 规则）**：xiyouji-day-review SKILL.md 步骤 4 新增第 6 项「归档/删除脚本查 tests/ 引用」（W506 教训固化：W447 归档 fix_svg_negative_widths.py 漏删配套测试致 pytest 收集失败）；character-content SKILL.md 深化专题步补引文探针工具引用。
> - **文件**：scripts/_cite_probe.py（新·_ 前缀不入库门禁）、skills/xiyouji-day-review/SKILL.md、skills/xiyouji-character-content/SKILL.md（sync_skills 已同步全局版）、六文档。
> - **验证**：_cite_probe.py 三用例实测通过（须菩提祖师/黑熊精/高翠兰 多关键词+单回+区间+片段模式）；sync_skills --check 漂移 0；verify_delivery exit 0；pytest 282 passed。
> - **状态**：已落地（待提交）。

### v2.3.105（2026-08-25）：W506 处置遗留 — 删除失锚测试 test_fix_svg_negative_widths.py

> **来源**：W505 收尾时发现 `pytest tests -q` 收集失败（ModuleNotFoundError: fix_svg_negative_widths）——W447 归档 45 个一次性脚本时漏删配套测试。处置类操作，按铁律须记 CHANGELOG。
> - **执行**：git rm tests/test_fix_svg_negative_widths.py（脚本 scripts/fix_svg_negative_widths.py 已于 W447 归档至 scripts/archive/，明确不入库门禁、不参与 CI；测试引用已归档模块失锚）。
> - **验证**：`pytest tests -q` = 282 passed（此前需 `--ignore` 绕过，现全量通过）；verify_delivery exit 0。
> - **状态**：已落地（待提交）。

### v2.3.104（2026-08-25）：W505 创意流程闭环落地 — 可信度轨收官（试点 4 篇方向二深化）

> **来源**：《内容可信度与溯源体系》方案 W505——W499 已暂存创意方法论 2 篇做管线化 + 试点。§9 试点人物经用户选择为「都做」→ 4 篇（方案原 M2 口径 1 篇，用户授权扩大，已回写方案档登记偏差）。
> - **执行（管线章节）**：skills/xiyouji-character-content/SKILL.md 新增「创意三明治管线」章节——四步固定流程（AI 发散 ≥20 极端切入点 → 人类收敛 ≤3 种子手写骨架 → AI 补全 2 版 → 人类裁决加闲笔/留白）；触发条件 = 用户显式说「用创意流程」；元信息块 `生成来源` 记录 `创意三明治管线@<commit>`。
> - **执行（试点）**：4 篇方向二深化走完整四步管线落 docs/02-人物深度分析/（菩提祖师/黑熊精/金角银角/高翠兰），各含 3 条 `> 原文引文（第N回）` 精确命中行 + v2 血缘 4 字段（核验状态：引文已核验）+ 创意三明治管线标记。
> - **执行（索引核验）**：docs/10-方法论沉淀/README.md 已含 2 篇方法论文档索引（W499 暂存版，核验跳过）；sync_skills.py --sync 仓库→全局后 --check 漂移 0。
> - **文件**：skills/xiyouji-character-content/SKILL.md、docs/02-人物深度分析/4 篇新文档、方案档（回写 W505 完成态）、六文档（README/STRUCTURE/项目说明计数 611→615）。
> - **验证**：4 篇 × 三门禁全过（check_frontmatter 元信息块 v2 · check_citations 引文 12/12 命中率 100% · check_glossary C2 新违规 0——初写 3 篇违规经 canonical 补齐修复）；全站引文 423 条 100%；sync_skills 漂移 0；check_index_health 通过；verify_delivery exit 0（A1-A6 计数 615 同步 README）。
> - **状态**：已落地（待提交）。

### v2.3.103（2026-08-25）：W504 存量核验状态基线 + 学术轨 105 篇引文核验（A+ 路径）— 可信度轨收尾

> **来源**：《内容可信度与溯源体系》方案 W504——§9 用户选 A+ 路径（为学术轨 105 篇逐篇补 ≥3 条可验证原著引文再核验，非默认 A·G=0）。
> - **执行（字段全覆盖）**：scripts/_w504_trust_baseline.py 为 docs/01–06 全部 611 篇补「核验状态：未核验」字段（幂等·插入于元信息块）。
> - **执行（A+ 引文）**：2 篇漏标直接标绿（记忆伦理 5 条/成书背景 4 条已 100% 命中）+ 9 篇无引文用 _w504_batch_insert.py（复用 _w504_cite_find 逻辑从 text-search.json 实取句体·零手抄·去换行·内置校验·幂等重写）补 3 条/篇 + 标绿；3 篇历史引文引入 variant 违规（全真派/版本演变·意马、明代盐法·圣僧）经替换或删除修复。
> - **执行（报告）**：scripts/_w504_report.py 生成 content-trust-report.json/.md（三值分布 + 未核验学术轨清单 + 时间戳）。
> - **文件**：docs/01–06 611 篇（核验状态 + 11 篇引文）、scripts/_w504_*.py 5 件（_ 前缀不入库门禁）、scripts/output/content-trust-report.json/.md + _w504_acad_list.txt + _w504_spec.json、方案档、六文档。
> - **验证**：三值 未核验 506 + 引文已核验 105 + 专家已核验 0 = 611（合计校验通过）；学术轨 105/105 绿标（A+ 目标 G=105 达成）；引文 411 条命中率 100%；防空真 0 违规（每篇 ≥3 条）；术语 C2 新违规 0（D8 交互风险坐实并修复：A+ 插引文向非基线学术轨引入 variant 被拦，3 篇已修）；引文回目分布单回 ≤9%（≤20% 阈值）。
> - **状态**：已落地（待提交）。

### v2.3.102（2026-08-24）：W503 原著引文硬验证 — 第 20 门禁 check_citations.py 挂载（防 AI 幻觉引文）

> **来源**：《内容可信度与溯源体系》方案 W503——存量锚定引文行实测 = 0（172 个文件含"原文"一词但全是散文叙述），引文无法机器验证；绿标「引文已核验」需要可信的命中工具。
> - **执行（语法）**：文档规范 §4.8 新立——`> 原文引文（第N回）：“……”`，N ∈ 1–100，引文必须是 dataset/text-search.json chapters[N-1].text 的**精确子串**（去空白归一后逐字匹配，禁省略号节引）。
> - **执行（脚本）**：新建 scripts/check_citations.py（--file/--dir 两模式），挂 verify_delivery 第 20 门禁（--dir docs 全量）；任何引文行未命中 = FAIL，存量引文行 = 0 无历史豁免。
> - **执行（skill）**：character-content 深化专题硬规则（≥3 条引文行 + 命中率 100%）+ Step 4 引文核验步；s4-submission 阶段 2 补 check_citations 调用说明（已同步全局版）。
> - **文件**：scripts/check_citations.py（新）、scripts/verify_delivery.py、docs/00-导读/文档规范.md（§4.8 新立 + §4.6 引用补实路径）、两 skill、方案档、六文档。
> - **验证**：正样本 1/1（第 1 回真实诗曰句命中）+ 负样本 2/2（改字未命中 + 第 999 回越界均被抓）；全量 791 文件扫描 0.3s（≤30s 阈值）；基线引文行 = 0 实测（B0=0）。
> - **状态**：已落地（待提交）。

### v2.3.101（2026-08-24）：W502 术语一致性门禁 — 第 19 门禁 check_glossary.py 挂载（术语库类型化 + 规范词锚定）

> **来源**：《内容可信度与溯源体系》方案 W502——术语漂移无门禁；实测术语表 6 组仅称谓组有变体映射，统一结构会产生假违规，故按组类型化。
> - **执行（术语库）**：dataset/glossary.json 由 check_glossary.py --generate 逐行解析术语表.md 生成（禁手抄）——6 组 59 条目（人物称谓 10 变体条目 + 佛教/道教/回目/地理/法宝 49 单名条目）。
> - **执行（门禁）**：scripts/check_glossary.py 挂 verify_delivery 第 19 门禁——C1 双向同步 diff=0；C2 规范词锚定仅人物称谓组（传递归一：圣僧→唐僧→玄奘；复合词掩码：心猿意马/金公木母黄婆 防子串误报）。
> - **执行（基线）**：存量违规实测 303 篇 383 条冻结于 scripts/output/glossary-baseline.txt，门禁只拦新增违规。
> - **文件**：scripts/check_glossary.py（新）、dataset/glossary.json（新）、scripts/output/glossary-baseline.txt（新）、scripts/verify_delivery.py、docs/00-导读/文档规范.md（§4.7 新立）、方案档、六文档。
> - **验证**：负样本 2/2（C2 缺规范词被抓 + C1 json 删条被抓）；基线冻结后门禁模式 exit=0；verify_delivery 全绿。
> - **状态**：已落地（待提交）。

### v2.3.100（2026-08-24）：W501 元信息块 v2 — 第 18 门禁 check_frontmatter.py 挂载（血缘 + 核验状态 4 字段）

> **来源**：《内容可信度与溯源体系》方案（docs/superpowers/plans/2026-08-24-content-trust-provenance-w501-w505.md）W501——大厂分析评估移植项 1：内容不可溯源、无可信度分级；存量锚定引文行实测 = 0，绿标须防空真。
> - **执行（规范）**：文档规范 §4.6 新立元信息块 v2——新文件必填 4 字段（生成来源 skill@commit 或 人工撰写 / 生成模型 含「未记录」合法枚举·禁编造 / 生成日期 YYYY-MM-DD / 核验状态 三值枚举·0 条引文禁标「引文已核验」空真防护）。
> - **执行（门禁）**：新建 scripts/check_frontmatter.py 挂 verify_delivery 第 18 门禁——仅扫描不在基线清单内的 docs/01-06 新文件；基线 frontmatter-baseline.txt 冻结存量 611 篇豁免（wc -l = 611 实测）。
> - **执行（skill）**：character-content SKILL.md Step 2 追加 v2 血缘 4 字段必填模板。
> - **口径澄清**：学术轨实测 105 篇（verify 首匹配口径）；锚定 grep 109 为假阳性（4 篇跨界趣谈正文含「学术研究」引用行），AGENTS「105 篇」无滞后。
> - **文件**：scripts/check_frontmatter.py（新）、scripts/output/frontmatter-baseline.txt（新）、scripts/verify_delivery.py、docs/00-导读/文档规范.md、skills/xiyouji-character-content/SKILL.md、方案档、六文档。
> - **验证**：正样本 1/1 + 负样本 1/1（缺「核验状态」exit=1 被抓）；new 模式 0 新文件 exit=0；check_index_health exit=0（治理引用 5 脚本全存在）；verify_delivery 全绿。
> - **状态**：已落地（待提交）。

### v2.3.99（2026-08-24）：W500 索引健康门禁 — 第 17 门禁转正 + bump 次级版本行增强

> **来源**：W499 全面审查教训——file-index 空壳/重复/残留、方法论 README 漏登记、CHANGELOG 编号上限手工漏改，三类漂移此前均无自动防线；用户确认「先做 1+2（门禁 + bump 增强）」。
> - **执行（第 17 门禁转正）**：新建 scripts/check_index_health.py 挂 verify_delivery——①file-index 段完整性（豁免区外空壳段必 FAIL：W449-W463 历史损坏区维持现状不重排·仅防新增）；②file-index 段唯一性（豁免区外 W 号重复必 FAIL）；③最新段残留"当前版本"快照行必 FAIL（历史段 bump 残留豁免）；④方法论 README 双向覆盖（目录 md ↔ 索引表链接差集 + "待创建"占位 0）；⑤CHANGELOG 编号规则段上限 == 最新 W 段（W499 曾手工漏改仅 WARN）；⑥治理文档引用一致性（文档规范.md scripts 引用存在性·verify 挂载脚本存在性——W499 审查盲区复盘补强）。负样本 4/4 自测（空壳段/待创建占位/编号不符/死链引用全被抓）。
> - **执行（审查防线补强）**：day-review skill 步骤 4 补"治理文档内容引用核验"（文档规范.md §8/§11 门禁数·脚本清单·行号 + AGENTS §4.2 清单）+ 陷阱第 8 条（治理文档引用会漂移），已 sync 全局版；AGENTS.md §4.2 补录第 17 门禁正文；文档规范.md §7/§8/§11 与 17 门禁同步（P1 修复：file-index 行门禁列滞后·17 门禁表缺失·禁改清单缺两脚本·bump 描述过时·行号 45→47）。
> - **执行（bump 增强）**：bump_version.py bump_version_line 扩展支持 `- **当前版本**：` 格式（项目说明次级版本行）——次级行历史格式仅版本号无 W 后缀，只替换版本号不追加 W token（防格式漂移）。W001-W### 编号上限同步 W417 增强已有，本次验证覆盖。
> - **验收**：verify_delivery 17 门禁全绿；负样本 4/4；bump 单元测试双格式 PASS。
> - **文件**：scripts/check_index_health.py（新建）+ scripts/verify_delivery.py（第 17 门禁挂载）+ scripts/bump_version.py（次级行增强）+ docs/00-导读/文档规范.md（§7/§8/§11 门禁清单同步）+ skills/xiyouji-day-review/SKILL.md（审查核验补强）+ .github/workflows/README.md（旁文档同步）+ 六文档 + AGENTS。
> - **验证**：负样本 4/4 + 正样本全绿 + bump 单元测试双格式 PASS。
> - **状态**：待提交（W499 批次在暂存区先行提交，本批随后）。

### v2.3.98（2026-08-24）：W499 GitHub 协作模板 + 创意方法论沉淀 + 索引漂移修复

> **来源**：用户准备（社区协作入口 + 创意方法论沉淀） + 2026-08-24 全面审查发现（方法论 README 索引漂移·file-index W449-W463 结构问题）。
> - **执行（社区协作入口）**：新增 .github/ISSUE_TEMPLATE 4 个（bug_report/feature_request/question/config.yml）+ PULL_REQUEST_TEMPLATE.md——社区提交 issue/PR 的规范入口。
> - **执行（创意方法论）**：docs/10-方法论沉淀/ 新增 创意三明治工作流.md（AI 发散→人类收敛→AI 补全→人类裁决四层交替·"荒谬起点"激发原创视角）与 人机创意工作流方法论.md（反向约束/跨时空嫁接/幻觉驱动四层创意飞轮 + 工程侧 backlog 备忘）；方法论 README 索引修复——补登 8 个存量文件（Subagent 盲信铁律/markdown 写作规范/前端显示问题诊断 SOP/十七维叙事学图谱测试计划/改动后影响面扫描/白屏三连复盘/记忆研究理论框架/dispatching 四 subagent）+ 修正 2 条"待创建"占位（E2 文档同步/并行 Edit 竞态·文件实际已存在）+ 关联文档版本刷新（v2.0.60→v2.3.97·W087→W498）。
> - **执行（skill 扩充）**：xiyouji-character-content 新增 references/creative-methods.md（四层创意方法速查·含提示词模板与红线）+ SKILL.md 补创意方法引用（外传/方向二/随笔可选·链接 references/creative-methods.md）。
> - **执行（索引修复）**：file-index W498 段补维护注记——W449-W463 区间历史遗留结构问题（W457/458/461/462/463 空表·W451/452/453/460 重复·W454/455 乱序·残留 v2.3.65-78 快照行）维持现状不重排（历史段禁改），查历史以 CHANGELOG 为准。
> - **验收**：verify_delivery 16 门禁全绿；方法论目录 17 文件 100% 登记；README 索引链接 0 broken；skills 双轨 0 漂移。
> - **文件**：.github/ISSUE_TEMPLATE/*（新建 4）+ .github/PULL_REQUEST_TEMPLATE.md（新建）+ docs/10-方法论沉淀/创意三明治工作流.md（新建）+ docs/10-方法论沉淀/人机创意工作流方法论.md（新建）+ docs/10-方法论沉淀/README.md（索引修复）+ skills/xiyouji-character-content/SKILL.md（修改）+ skills/xiyouji-character-content/references/creative-methods.md（新建）+ scripts/output/file-index.md（注记）+ 六文档。
> - **验证**：verify 全绿 + 目录登记 100% + 链接 0 broken。
> - **状态**：批次暂存中，未 commit/push。

### v2.3.97（2026-08-24）：W498 防漂移门禁 — skills 索引一致性门禁转正 + 仓库↔全局同步工具 + 18 skill 全量部署

> **来源**：W497 教训（day-review 建了未入库 + 索引/AGENTS §4.5 漏收录 + 仓库版与全局版漂移）——单靠流程提醒防不住，用户确认「全做（门禁+脚本）」：把防线升级为自动检测。
> - **执行（第 16 门禁转正）**：新建 scripts/check_skills_index.py 挂 verify_delivery——①skills/ 目录数 == README 表格行数（双向差集）；②目录短名 ⊆ AGENTS.md §4.5；③skills/ 全部文件 git tracked（git ls-files 差集，抓 day-review 式建了未 add）；④SKILL.md frontmatter name == 目录名。负样本 2/2 自测（未跟踪文件/无索引目录均被抓住）。
> - **执行（同步工具）**：新建 scripts/sync_skills.py（本地工具不入 CI）：--check 列仓库版 vs 全局版 ~/.qwenworkcn/skills/ 漂移（孤儿只报 xiyouji-*，忽略 QwenWork 内置 skill）；--sync 以仓库为真源单向复制 + 自检。plan-authoring/.skill-metadata.yaml 全局版较新（含 §10 三段式表述），先反向回拷仓库再统一真源。
> - **执行（全量部署）**：--sync 把仓库 18 个 skill（含 4 会话流程 + 12 个此前从未安装的 xiyouji-*）全量部署到全局版，44 文件更新，自检 0 漂移。
> - **执行（流程固化）**：version-bump 第 8 步补「改/新增 skill 后必须 sync_skills.py --sync + check_skills_index.py 过门禁」；AGENTS.md §4.2 补录第 16 门禁。
> - **验收**：verify_delivery 核心全绿（含新门禁）；sync_skills.py --check 0 漂移；负样本 2/2。
> - **文件**：scripts/check_skills_index.py（新建）+ scripts/sync_skills.py（新建）+ scripts/verify_delivery.py（第 16 门禁挂载）+ skills/xiyouji-plan-authoring/.skill-metadata.yaml（全局→仓库回拷）+ skills/xiyouji-version-bump/SKILL.md（第 8 步补 sync）+ AGENTS.md（§4.2/§4.5/脚注）+ 六文档。
> - **验证**：门禁负样本 2/2 + 全量部署自检 0 漂移 + verify 全绿。
> - **状态**：本次提交（W498）将推送 origin/main。

### v2.3.96（2026-08-24）：W497 skills 治理同步 — 仓库版 skill 与全局版对齐 + day-review 入库 + 收尾三同步固化

> **来源**：skills 目录审查（2026-08-24）发现 3 处 P1——仓库版 visual-batch/plan-authoring 落后全局安装版（W478 脚本迁移/W488 可感知验收未回写）、day-review 从未 git 入库、characters-knowledge 引用已迁出的 text-search 内嵌语料；用户确认全部修复。
> - **执行（skill 漂移同步）**：visual-batch 同步全局版 v1.2.0（SKILL.md+reference.md：W478 _w478_migrate.py 六规则脚本迁移管线 + W488 可感知升级批/暗色夜读/M-A1 前后对比验收 ≥1%）；plan-authoring 同步 v1.1.0（验收三段式「指标=阈值（测量方法）」/派生命令/裁掉项显式化/§10 落地状态回写）。
> - **执行（day-review 入库）**：git add skills/xiyouji-day-review/（SKILL.md+reference.md+.skill-metadata.yaml）；AGENTS.md §4.5 流程类补录（4 个，项目 skill 总数 18）；skills/README.md 索引补行 + 标题 17→18。
> - **执行（失效引用修复）**：characters-knowledge 全文检索入口 text-search.html（内嵌语料已迁出页面）→ dataset/text-search.json。
> - **执行（收尾流程补全）**：version-bump 新增第 8 步「收尾三同步」（AGENTS 脚注/路线图状态段/方案档 §10 回填，W494 教训固化）+ 陷阱/完成清单同步，流程改九步；四会话流程 skill（agent-session-loop/deep-review-loop/mem-wrap-up/self-evolution）补「子代理不可用降级」声明（平台派发 FORBIDDEN 时 3-lens/对抗/独立审计降为主代理执行、不静默跳过）+ 三独立 skill 补闭环单一事实源护栏。
> - **验收**：_check_skills.py 自检 18 个 SKILL.md 全过（frontmatter/openai 残留/references 链接）；仓库版 vs 全局版 4 个漂移文件 diff IDENTICAL；verify_delivery 核心全绿。
> - **文件**：skills/ 下 8 个 skill 文件（visual-batch×2 + plan-authoring×2 + day-review×3 + characters-knowledge + version-bump）+ AGENTS.md（§4.5 + 脚注）+ skills/README.md + CHANGELOG/交接文档/file-index/dukou-engine footer。
> - **验证**：diff 4 文件 IDENTICAL + _check_skills 18/18 + verify 全绿。
> - **状态**：本次提交（W497）将推送 origin/main。

### v2.3.95（2026-08-22）：W496 优化收尾 — 夜读切换钮全站 + 样式断言固化 + 验收现测工具 + fps 遗留关闭

> **来源**：W495 审查后用户指令「不要下次再做，现在做完」——四项优化当批清零。
> - **执行（夜读切换钮）**：theme-init.js 扩展——无 .theme-toggle 的页面（data/EN 225 页）DOMReady 注入浮动切换钮（40px 圆·z-40·月/日 SVG·aria-label 双语·运行时 <style> 走 style-src unsafe-inline）；点击切 data-theme + 写 xy-theme；根页 6 自有切换器跳过注入。零 HTML 改动、零 CSP 改动（外部脚本 'self'）。
> - **执行（样式断言固化）**：tests/e2e/test_smoke.js 新增检查 6（html/body computed 背景不得同时透明）——W457/W495 教训固化为 CI 冒烟，与第 15 门禁双保险；全量 89/89 过。
> - **执行（验收现测工具）**：新建 scripts/acceptance_snapshot.py（M5 内联字节/M2M3/M4/M1/断点 五组当批现测）；AGENTS.md §4.3 立铁律：CHANGELOG 验收数字从本工具抄、禁跨批复制。
> - **执行（fps 遗留关闭）**：_perf_measure.js 首跑（geo-3d 6s trace Layout=3/Paint=8 无风暴）+ _w464_perf_measure.js 五核心页 LCP≤188ms/CLS≤0.001/TBT≤140 全过阈值；V2 方案档落地状态表+验收清单回写关闭（拖拽 fps 以代理证据关闭，诚实注记）。
> - **验收（acceptance_snapshot 当批现测）**：M5 min/max 30653B ≤33792B；M2/M3 裸色 246 全登记·裸 shadow 0；M4 命中 0；M1 P0/P1=0；断点白名单外 0。切换钮探针：data/EN 注入+切换+持久化全过·index 跳过·375px 无溢出·pageerror=0；test_smoke 89/89；CSP 1189 哈希 0 漂移；verify 核心全绿。
> - **文件**：site/js/theme-init.js + tests/e2e/test_smoke.js + scripts/acceptance_snapshot.py（新建）+ AGENTS.md（§4.3 铁律）+ docs/00-导读/V2可视化维度方案.md（回写）+ 六文档。
> - **验证**：切换钮探针 4 项 + 89/89 冒烟 + verify 全绿。
> - **状态**：本次提交（W496）将推送 origin/main。

### v2.3.94（2026-08-22）：W495 P0 热修复 — W493 回归处置：全站 INLINED CSS 恢复 + 完整性门禁转正

> **来源**：2026-08-22 审查发现 W493 一次性修复脚本误清空 224 个 data+EN 页的 INLINED CSS 块（tokens+system 约 30KB），全站渲染裸文本（含线上 Pages）；既有 14 门禁无一拦截（空块括号平衡/CSP 只查脚本/pageerror 只抓 JS 错/溢出检查在无样式页 trivially 过）。
> - **执行（恢复）**：修 inline_css.py --force 短路缺陷（已内联页 link 标签已移除被 skip-no-link 跳过、--force 失效）→ --force 重同步 225 页 INLINED 块恢复（实测 30659B ≤33KB 预算）；W493 私有块修复成果不受影响（--force 仅替换 INLINED 块）。
> - **执行（门禁转正）**：新建 scripts/check_inlined_css.py 挂 verify_delivery（第 15 门禁）：带 INLINED 标记页块内容必须 ≥20000B；负样本自测能抓清空（exit 1）。
> - **执行（回归重测）**：W494「5 视口 FAIL=0」测于无样式页作废 → 7 视口（375/390/414/480/640/768/1024）× 7 页（根+data+EN）「样式+溢出+pageerror」三重断言 ALL PASS；light/dark 截图目视恢复。
> - **执行（卫生回填）**：baseline_snapshot.py + 观测基线快照.md 入库（M6 证据链此前断裂）；E3/E4/E5/E6/W494 五方案档补落地状态段与 commit 回填（含 M5/W494 回归数据作废的诚实注记）；交接文档过期「下一版本 W465/W495」行纠正。
> - **验收**：CSP 1189 哈希 0 漂移；check_structure 0 失衡；verify_delivery 核心全绿（含新 INLINED 门禁）。
> - **文件**：site/data+en 225 页（INLINED 恢复）+ scripts/inline_css.py（缺陷修复）+ scripts/check_inlined_css.py（新建）+ verify_delivery.py（门禁挂载）+ scripts/baseline_snapshot.py + scripts/output/观测基线快照.md（入库）+ 5 方案档 + 六文档。
> - **验证**：负样本 1/1 + 7 视口三重回归 ALL PASS + verify 全绿。
> - **状态**：本次提交（W495）将推送 origin/main。

### v2.3.93（2026-08-22）：W494 Phase E 遗留收尾 — 断点规范化 + 图表降级（字体切片关闭）

> **来源**：用户 2026-08-22 指令把收口报告遗留项排进 W494；字体专项与断点/图表降级同批执行。
> - **执行（断点常量规范化）**：全站 380 处非白名单断点映射到白名单 {375,480,640,768,1024,1280,1536}（两轮：5xx-9xx 按最近白名单 238 处 + 小断点 220-420→375/480 与大断点 1000-1440→1024/1280/1536 142 处）；残留 0。
> - **执行（图表 ≤640px 降级）**：system.css 新增 W494 段（图例纵排/轴文字 10px/容器 padding 收窄/tooltip max-width 220px），CSS 显示层降级、D3 渲染不变；inline_css --force 传播 225 页。
> - **执行（存量响应式缺陷）**：tag-cloud（CN+EN）搜索 input 缺 box-sizing:border-box 致 375px 溢出；81-hardships（CN+EN）图表 svg 固定 360px 在 1024px 溢出 → 均修复。
> - **执行（字体专项：判定关闭）**：① unicode-range 切片不可行——data/en 225 页内联架构（无外部 link 锚点），切片声明只能进 tokens.css，16 片 134KB×225 远超预算线；② Serif VF 子集化收益 ≈0（3636→3555KB，VF 轴全保留），已回滚。字体现状（Sans 9340 字子集化 773KB + Serif VF 标题字）判定可接受，关闭该项。
> - **验收**：5 视口（375/480/640/768/1024）× 11 页（根页+data+EN）溢出 FAIL=0；inline_css 传播后 CSP 6 页漂移 → 重跑归零（1189 哈希 0 漂移）；check_structure 0 失衡；verify_delivery 核心全绿（含 W493 三门禁）。
> - **文件**：site/*.html + site/data/*.html + site/en/*.html（断点映射/溢出修复/CSP 重跑）+ site/system.css（图表降级）+ docs/superpowers/plans/2026-08-22-phase-e-w494-legacy-closure.md（新）+ 六文档。
> - **验证**：5 视口回归 + 五门禁全绿。
> - **状态**：本次提交（W494）将推送 origin/main。

### v2.3.92（2026-08-22）：W493 Phase E6 验收收口 — 三门禁转正 + M1-M7 全达标（Phase E 主线收官）

> **来源**：W492 E5 后用户 2026-08-22 指令 W493 按推荐执行 = E6（验收收口 + 三门禁转正）。
> - **执行（三门禁转正挂 verify_delivery）**：① scripts/check_token_coverage.py 新建（M2/M3：私有 <style> 块 UI 裸色——无豁免注释页必须 0、带 e-track-exempt 注释页 ≤ 登记 N；真裸 box-shadow 必须 0；INLINED 副本跳过）；② scripts/check_motion_ban.py 新建（D4：cubic-bezier 负值/360° 旋转/infinite/parallax，白名单 chart-loading/chart-fade-in）；③ a11y_audit.py 挂载（M1：E2-2 P0+P1=0 阻断）。三门禁**负样本自测**各构造 1 坏文件确认能抓（token 抓到 ui=2+sh=1 / motion 抓到 2 处 / a11y 标 P1）后删除。
> - **执行（门禁前置修复）**：私有块 UI 裸色三轮回补映射 1193→246 处（paper-warm/dark-text/accent-soft/dark/accent-2/3/ink-soft/line/elev 等 20+ 色值变体 + color-mix 保留 alpha）；93 页 e-track-exempt 豁免登记（N 精确对应）；263 处裸 box-shadow 按 blur 映射 elev-1~4（var(--shadow*) 令牌引用保留）；10 处历史 infinite 动画改一次性（criticism-history wordFloat/bladeCut/crackOpen + concept-device danmakuFly，CN+EN）；mobile-index 1 处真裸阴影特例修复。
> - **验收（M1-M7 全达标）**：M1 a11y E2-2 全站 P0/P1=0；M2 私有块裸色 246 全豁免登记、无注释页 0；M3 真裸 box-shadow 0；M4 motion_ban 0 命中；M5 内联 28385B ≤33KB；M6 沿用 W464 baseline（无布局改动）；M7 各批 pageerror=0。verify_delivery 核心全绿（含新三门禁）。
> - **范围纪律**：字体 unicode-range 切片/断点规范化/图表 ≤640px 降级 三项遗留显式记录（收口报告 §四），非遗漏。
> - **文件**：scripts/check_token_coverage.py + check_motion_ban.py（新建入库）+ verify_delivery.py（+3 门禁）+ 93 页豁免登记/色值修复 + 4 页 infinite 修复 + docs/superpowers/plans/2026-08-22-phase-e-e6-closure-report.md（新）+ Phase E 路线图回写 + 六文档。
> - **验证**：负样本 3/3 + verify_delivery 核心全绿（含新门禁）。
> - **状态**：本次提交（W493）将推送 origin/main。

### v2.3.91（2026-08-22）：W492 Phase E5 响应式+微交互 — 导航抽屉 + 图标收尾（字体切片/断点/图表降级推迟）

> **来源**：W491 E4 完成后用户 2026-08-22 指令 W492 按推荐执行 = E5（响应式 + 微交互 + 字体专项）。
> - **执行（导航抽屉）**：system.css 新增 .nav-toggle/.nav-mask + ≤768 `.topnav:has(.nav-toggle) nav` 滑出面板（display:none 关闭态避免 fixed 溢出 + JS 双 rAF 过渡 + elev-4 + 遮罩 + ESC + 窗口放大自动关 + RM 走全局）；4 根页（index/dashboard/curated/guide）加汉堡按钮 + 遮罩 + JS；**dashboard 缺 `<link system.css>` 补上**（抽屉规则不生效根因，此前仅靠页面私有样式）。
> - **执行（图标/触摸）**：根页 emoji 扫描 = 0（W488 已换完）；index ask-chip 触摸目标 padding 6px→10px。
> - **验收**：375px 4/4 抽屉开/遮罩关/关闭态零溢出（scrollWidth ≤ clientWidth+1）/pageerror=0；数据页 + EN 抽查 375px 无溢出（:has 保护 data 页 480 下 display:none 无回归）；check_structure 0 失衡 / check_js_syntax 0 错 / CSP 1189 哈希 0 漂移 / lint_links 4354 链接 0 broken / verify_delivery 核心全绿。
> - **范围纪律（显式推迟 W493，非遗漏）**：① 字体 unicode-range 切片——多片 @font-face 声明 ~60KB 进 tokens.css 会撑爆 225 页内联预算，需独立 CSS 文件专项；② 断点常量规范化——存量非白名单 520/720/960/600/900/860/820 等 100+ 处，改断点风险高无感知收益；③ 图表 ≤640px 降级 + D3 resize——86 页批量风险高且移动端现状可读；④ dukou-engine/mobile-index 无 topnav 结构豁免抽屉。
> - **文件**：site/system.css + 4 根页（index/dashboard/curated/guide）+ docs/superpowers/plans/2026-08-22-phase-e-e5-batch-record.md（新）+ Phase E 路线图回写 + 六文档。
> - **验证**：五门禁全绿（见上）。
> - **状态**：本次提交（W492）将推送 origin/main。

### v2.3.90（2026-08-22）：W491 Phase E4 EN 站同步 — 85 同名可视化页令牌化对齐

> **来源**：W490 E3 收官后用户 2026-08-22 指令 W491 按推荐执行 = E4（EN 站同步对齐）。
> - **执行**：EN 85 同名可视化页（CN data 86 减 journey-geo-3d，同名派生）；_w491_en_migrate.py 复用六规则（改 DATA 路径 site/en/）；tokens/system 同源（W489 已传播 INLINED 块），本批只迁移页私有 <style>；3D 页 character-relationship-3d 仅 UI 层。
> - **验收**：validate_en.py 85/85 PASS（chrome CJK 白名单 + script CJK=0）；85 页 Playwright pageerror=0；CN/EN 同页截图对照 10 页目视一致（chapter-stats/emotional-heatmap/81-hardships/relationships/tag-cloud/philosophy/criticism-history/journey-spacetime/monster-ecology-network/narratology-13d-network）；check_structure 0 失衡 / check_js_syntax 0 错 / CSP 1185 哈希 0 漂移 / lint_links 4353 链接 0 broken / verify_delivery 核心全绿。
> - **范围纪律**：EN 根页（index/guide/dashboard 等非可视化页）不在此批，随 E5 根页口径处理。
> - **文件**：site/en/ 85 页 + scripts/_w491_en_migrate.py（一次性不入库）+ docs/superpowers/plans/2026-08-22-phase-e-e4-batch-record.md（新）+ Phase E 路线图回写 + 六文档。
> - **验证**：五门禁全绿（见上）。
> - **状态**：本次提交（W491）将推送 origin/main。

### v2.3.89（2026-08-22）：W490 Phase E3 CN 可视化页传播 II — 30 页令牌化收尾（86 页传播 100%）

> **来源**：W489 全站暗色完成后，用户 2026-08-22 指令 W490 按推荐执行 = E3（CN 传播 II 余 30 页），Phase E 传播批收官。
> - **执行**：E3 派生 = 86 减 E2 批 56（`git diff 68168a6 --name-only` 精确，3D/Canvas 2 页 character-relationship-3d + journey-geo-3d、时间线/地图、静态/表格、text-search 等）；新建 _w490_migrate.py 复用六规则（R-SHADOW/R-RADIUS/R-TRANS/R-FOCUS/裸色白名单/R-EXEMPT）；3D 页深度令牌仅用于 UI 层（图例/按钮/tooltip），场景材质不动。
> - **验收**：30 页 Playwright pageerror 全部 0；3D 专项 canvas.width>0 断言通过；check_structure 0 失衡 / check_js_syntax 0 错 / CSP 1185 哈希 0 漂移 / lint_links 4353 链接 0 broken / verify_delivery 核心全绿。
> - **范围纪律**：D1 图表 8 色/顺序色不建（批内页无新系列色需求）；M2 严格清零（按钮白字/JS 内数据色等存量）移 E6 收口门禁转正时处理。
> - **文件**：site/data/ 30 页 + scripts/_w490_migrate.py（一次性不入库）+ docs/superpowers/plans/2026-08-22-phase-e-e3-batch-record.md（新）+ Phase E 路线图回写 + 六文档。
> - **验证**：五门禁全绿（见上）。
> - **状态**：本次提交（W490）将推送 origin/main。

### v2.3.88（2026-08-22）：W489 全站暗色模式 — dark 令牌全局化 + 225 页传播 + 共享 theme-init

> **来源**：W488 第一批暗色仅覆盖 6 根页（dark 令牌走页面内联），用户 2026-08-22 指令 W489 按推荐执行——把暗色扩展到全站（86 数据页 + EN 138 + 根页），E3-E6 余项留后续批。
> - **执行（令牌全局化）**：dark 令牌组迁入 tokens.css（html[data-theme="dark"] 覆盖 15 组变量 + 深色 elev + color-scheme，+1494B）；新增全局图表适配（SVG path/circle/rect 数据色 brightness(1.12)+saturate(1.05) 提亮、.chart-tooltip 边框跟随）；inline_css.py --force 重新同步 225 页（data+EN 全获 dark UI 层适配，同时 W488 的 system.css hover/指示条升级同步传播）。
> - **执行（防 FOUC 共享脚本）**：新增 site/js/theme-init.js（同步加载，读 xy-theme → 挂 html[data-theme]，prefers-color-scheme 跟随，fail-open）；批量插入 226 页 head（CN 根 9 + data 86 + EN 138 - 2 诊断页 rum-viewer/visit-viewer 无锚点豁免；6 根页 W488 已有内联防 FOUC 故跳过）；外部脚本免 CSP hash（script-src 'self'），CSP 1185 哈希 0 漂移。
> - **执行（去重）**：5 根页（index/curated/guide/dashboard/mobile-index）删除内联 dark 通用令牌块（与 tokens.css 重复，每页 -1170B），保留页面特有适配（dark-band 边框/mega-num 朱砂/hero 渐变/ask-form 按钮/dashboard 环图 filter/dukou-engine 双变量体系全保留）。
> - **执行（验收）**：全站 dark 冒烟 12 页（CN 根 2 + data 6 + EN 4）theme=dark + body bg #221D16 + pageerror=0 + FOUC=0；dark 抽样截图目视（emotional-heatmap/chapter-stats/EN）渲染正常；单页内联 CSS 28385B ≤ 33KB 预算线；五道门禁全绿。
> - **文件**：site/tokens.css（+dark 组）+ site/js/theme-init.js（新增）+ 226 页 head 插引用 + 5 根页去重 + 六文档。
> - **验证**：check_structure 0 失衡 / check_js_syntax 0 错 / CSP 1185 哈希 0 漂移 / lint_links 0 broken / verify_delivery 核心全绿。
> - **状态**：本次提交（W489）将推送 origin/main。

### v2.3.87（2026-08-22）：W488 根页视觉重设计 + 夜读模式 — Phase E 方向 A 第一批（可感知升级 + 暗色提前）

> **来源**：W487 复盘发现 Phase E（W476-478）验收 M1-M7 全为工程卫生指标、worktree 前后截图实测 E1 仅 index 有可见变化、E2 56 页等值迁移零感知；用户 2026-08-22 拍板方向 A（根页视觉重设计）+ 暗色模式排进第一批，方案落 docs/superpowers/plans/2026-08-22-rootpages-visual-and-nightmode.md，M-A1 前后对比截图强制入验收。
> - **执行（感知升级，6 用户可见根页）**：index hero "100" 数字朱砂强调（accent-deep+tabular-nums）；dashboard "数据看板"标题 + 4 个 KPI 大数字朱砂、八十一难交叉表表头淡朱砂底（accent 14% mix）+ 深朱砂字、route-strip 顶部 3px 朱砂线、KPI 卡圆角 2→6px；curated 28 卡 / guide 7 路径卡 / system.css .card/.kpi hover 升级（elev-2 + translateY(-3px) + 1.5px 朱砂外描边 40%）；guide 7 个 + mobile-index 6 个 emoji → 朱砂线条内联 SVG（stroke 1.5/currentColor/24×24）；dukou-engine header 标题 26→30px + 底部朱砂双线；导航 active 指示条（.topnav nav a::after scaleX 滑动，含 nav-strong/aria-current）；reveal-in JS 接入（html.js-reveal + IO 一次性 + reduced-motion 直达终态，fail-open）。
> - **执行（暗色夜读，6 根页）**：dark 令牌组走**页面内联**覆盖（不落全局 tokens/system，data/en 225 页零波及）；玄墨 #221D16 底 / 宣纸 #F2EBDC 文字反相 / 朱砂提亮 #E0604F / 深色 elev 阴影；topnav/hero 右侧夜读切换器（月亮/太阳 SVG）；localStorage `xy-theme` + prefers-color-scheme 跟随 + head 首屏内联 script 防 FOUC；dashboard 环图序列色 brightness(1.14) 提亮；dukou-engine 双变量体系（自有 :root + tokens）全量覆盖。
> - **执行（验收，M-A1 前后对比强制项）**：before=65890b2 worktree 同机位全页截图 vs after；PIL 差异像素率 6/6 ≥1%（index 2.35 / dashboard 5.05 / curated 2.84 / guide 5.88 / dukou-engine 25.98 / mobile-index 7.07）+ 目视清单 6 页 × ≥3 处（w488-verify/M-A1-visual-checklist.md）；dark 冒烟 6 页 pageerror=0 + FOUC=0；禁 JS 回退 6 页浅色正常；html 增量每页 +3.2~6.6KB；tokens.css 7750B 未增、system.css +644B（hover/指示条）。
> - **执行（治理）**：教训入库 plan-review skill v1.0.1（陷阱 9「视觉目标 ≠ 工程卫生验收」+ 阶段 1 动作 6 感知验收取证 + reference §1.6 worktree 截图法，双副本同步）；Phase E 路线图 §3/§10 回写 E2 完成态（68168a6·56 页）+ 感知验收后补。
> - **文件**：site/{system.css,index,dashboard,curated,guide,dukou-engine,mobile-index}.html + skills/xiyouji-plan-review/{SKILL.md,reference.md}（双副本）+ docs/superpowers/plans/2026-08-18-phase-e-visual-elevation-roadmap.md（回写）+ 2026-08-22-rootpages-visual-and-nightmode.md（新方案）+ 六文档。
> - **验证**：check_structure 0 失衡 / check_js_syntax 0 错 / CSP 1185 哈希 0 漂移 / lint_links 0 broken / verify_delivery 核心全绿。
> - **状态**：本次提交（W488）将推送 origin/main。

### v2.3.86（2026-08-19）：W487 四会话 skill 二轮同步 — DRL 降级声明 + experience-capture 格式规范

> **来源**：用户 2026-08-19 在 Claude Code 中再次更新 4 个开源 skill 仓库（agent-session-loop / deep-review-loop / mem-wrap-up / self-evolution），要求复查 xiyouji/skills 副本。
> - **执行（复查筛选）**：4 仓库新 commit 中 agent-session-loop / deep-review-loop 仅 README/CONTRIBUTING 文档更新（不进项目副本）；mem-wrap-up 新增「deep-review-loop 未安装时 Step 7b 降级声明」（精简审查 + `DRL downgraded` 标注 + 降级≠跳过）；self-evolution 触发词扩充（记住这个 / capture / 经验沉淀）+ 快速模式写入步骤引用新增 `references/experience-capture-format.md` 格式规范（97 行：写入格式 / 质量标准 / 边界纪律 / 手动触发 / 通用编号前缀）。
> - **执行（边界）**：README / CONTRIBUTING / evals / CI 等工程件不入 xiyouji（项目副本非发布镜像）。
> - **文件**：skills/mem-wrap-up/SKILL.md + skills/self-evolution/{SKILL.md,references/experience-capture-format.md（新增）} + AGENTS.md + README.md + STRUCTURE.md + skills/README.md + 六文档。
> - **验证**：触发词 / 降级声明 / 格式引用 Grep 落地；`verify_delivery.py` 核心全绿。
> - **状态**：本次提交（W487）将推送 origin/main。

### v2.3.85（2026-08-19）：W486 四会话 skill 协议同步 — 上游 Claude Code 修正入库

> **来源**：用户 2026-08-19 在 Claude Code 中更新 4 个开源 skill 仓库（agent-session-loop / deep-review-loop / mem-wrap-up / self-evolution），随后要求核对 xiyouji/skills 副本并同步。
> - **执行（协议同步）**：xiyouji 副本为项目内私有版（W484 平台适配 + 内部路径），按内容层对齐上游 7 项协议修正——① verdict 禁词 6 词 → 7 词全序（补 looks good：deep-review-loop 5 处 + agent-session-loop references 2 处）；② R0 表面检查 3 件套 → 4 件套（补 expected hits 必现：agent-session-loop SKILL + mem-wrap-up 7b）；③ 过拟合警报层 3 升级增强版（P0 反弹 1 轮 / P1 反弹 2 轮 / 持平 4 轮窗口）；④ mem-wrap-up Step 6 输出三零目标 → P0=0 P1=0、P2 ≤ N_max（对齐 DRL 层 1）；⑤ mem-wrap-up 4b work-log 路径矛盾修正（logs/{YYYY-MM}.md → memory 路径约定）；⑥ bridge_note 定义补入 mem-wrap-up 正文；⑦ self-evolution 快速模式补「与整合版并用时」协调声明。
> - **执行（边界）**：evals/CI/marketplace/fragment-lint 等开源工程件不入 xiyouji（项目副本非发布镜像）；runtime-audit.py 插件路径说明不同步（本仓库未收录该脚本）。
> - **文件**：skills/agent-session-loop/{SKILL.md,references/01-review.md,references/02-wrap-up.md} + skills/deep-review-loop/SKILL.md + skills/mem-wrap-up/SKILL.md + skills/self-evolution/SKILL.md + AGENTS.md + README.md + STRUCTURE.md + skills/README.md + 六文档。
> - **验证**：旧 6 词禁词 / 三零目标 / 旧警报 / 路径矛盾 Grep 残留 0；`verify_delivery.py` 核心全绿。
> - **状态**：本次提交（W486）将推送 origin/main。

### v2.3.84（2026-08-19）：W485 收录三项目 playbook — visual-batch / plan-authoring / plan-review 入库 skills/

> **来源**：用户提供 `D:\1\skills` 下三个项目 playbook（Phase E 视觉批次执行 / W 批次方案撰写 / 方案评估），此前仅存在于全局目录、仓库无副本无登记（AGENTS.md 只到 14 个）。
> - **执行（收录）**：三 skill 整目录复制入库 `skills/`（SKILL.md + reference.md + .skill-metadata.yaml）；plan-review 补 .skill-metadata.yaml（两个示例，与另两份格式对齐）；plan-authoring description 九段括号列举修正。
> - **执行（文档）**：AGENTS.md §4.5 / README / STRUCTURE / skills/README 同步 14→17 个；版本脚注补 W485。
> - **文件**：skills/xiyouji-visual-batch/、skills/xiyouji-plan-authoring/、skills/xiyouji-plan-review/（新增 9 文件）+ AGENTS.md + README.md + STRUCTURE.md + skills/README.md + 六文档。
> - **验证**：`scripts/_check_skills.py` 全过（17 skill）；`verify_delivery.py` 核心全绿。
> - **状态**：本次提交（W485）已推送 origin/main。

