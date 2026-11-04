### W1136（2026-11-04）：并行会话统筹调度批

**本批要点**（并行会话统筹调度批·协调层·零页面内容改动·不新增门禁槽 ⇒ 门禁 62 段不变·**新增坑表 1 条 E-185 ⇒ 计数链 268 → 269**）：① **实读全部并行面建占用矩阵**：12 个并行会话 / 6 棵工作树 / 共享预约表 / 台账正本 58 行 + 归档 416 行 / README §六 全文口径 86 行 / 坑表 268 条 / CHANGELOG 顶段 W1129 / 门禁 57 槽 ⇒ 据此定位 9 类碰撞（C1~C9）并逐项裁决 ② **登记号仲裁**：实读 §六 实测重复登记号 = [27, 35, 36, 69, 74]，其中 35/36 均为 T-29 ⇒ 判定为「同号两行」而非「缺号」（补第三行反而变三行同号）且 T-29 属他人历史交付物（补登记即越权改他方行）⇒ 裁定 W1133 批撤销补登记并只占 96 号、**97 号刻意空出**留后续 §六 治理批；终版分配 95(W1126)/96(W1133)/97(空)/98(W1130)/99(W1132)/100(W1135)/101(W1134)/102(W1136) ③ **写顺序仲裁**：touches 实测 W1133 与 W1130 重叠 7 面、W1132 与 W1130 重叠 6 面、W1135 与 W1130 重叠 5 面 ⇒ 五批同时跑收官链必然互相覆盖（生成面冲突须靠「取远端基底 + 重跑生成链」消解）⇒ 强制串行，裁定 W1130 批先收官、其余批基于合并后 origin/main 重跑收官链 ④ **计数链基线纠错**：门禁 preflight 打印的 267 系旧快照（打印值取自旧工作树），origin/main 实算为 268 ⇒ 基线裁定 268（链序 268 → 271 → 277 → 277+N → 本批 269）⑤ **E 号与登记号规则分离**：E 号起点 = 收官时实测 max + 1（在途未落库不构成占用）；README §六 登记号 = 先落地者保留的硬分配 ⇒ E-172~E-175 为空洞刻意不回收 ⑥ **双锚校验纪律（本轮 P0 澄清产出·已落 E-185）**：定位登记表须「章节标题 + 表头列」双锚定 + 全文与分段交叉对账，禁全文兜底匹配、禁按章节区间单点取段 ⇒ 实测登记表跨三段物理分布（文件首行 + §六 段内 58 行 + 文件末尾尾段 28 行），按区间取会漏读 28 行；**「登记行数骤减」类告警必须先排除「解析锚点错位」再判定「数据丢失」** ⑦ **主树占用风险处置**：主树 D:/xiyouji 落后 origin/main 14 提交且承载 5 件他方未提交改动 ⇒ 裁决迁独立 worktree（W1134 批已迁 D:/xiyouji-w1134）⑧ **PR #138 CONFLICTING 处置指引**：禁 --ours 批量覆盖生成面 + 合并三查（文件集差集 / 内容逐字比对 / 对方新增行为落点）+ 冲突标记逐文件复扫（门禁 C9 扫描面不含方案报告目录）⑨ **PR 节奏按 2026-11-04 二次口径**：回填/订正类永不单独开 PR、同会话当日多批合并一个 PR。

**文件**：
- docs/00-导读/W批次编号对账表.md
- docs/11-方案报告/计划方案/T90-任务计划执行与经验沉淀报告-2026-11-04.md
- docs/11-方案报告/README.md
- docs/agent/pitfalls.md
- AGENTS.md
- HANDOVER.md
- .agent/skills/puti-shouye/SKILL.md
- CHANGELOG.md
- scripts/output/file-index.md
- scripts/output/_w1136_spec.json
- scripts/output/_cascade_files_W1136.txt
- README.md
- STRUCTURE.md
- docs/00-导读/项目说明.md
- CITATION.cff
- site/data/search.html
- site/en/search.html
- .github/workflows/README.md
- scripts/output/stats.json
- scripts/output/stats-index.md
- scripts/output/stats-changelog.json
- scripts/output/tools-inventory.md
- archive/docs/AGENTS-ARCHIVE.md
- docs/INDEX.md
- scripts/INDEX.md
- scripts/output/INDEX.md
- scripts/output/README.md
- tests/unit/INDEX.md
- tests/unit/README.md
- pytest.ini

**认领登记 W1136**（占号 session=ROGSTRIX@xiyouji-w1136-4e5326·17:43:04 落占·preflight PASS·touches 12 面全清单登记）。

**验证**：登记号与 E 号两套号段无撞号（§六 95~102 各归一批）· 坑表六节声明 48/10/31/26/15/139 = 269 = 列表行实数 269 · 台账归档 416 行 / 416 唯一号 / 重复 0 · 第 48 门禁计划方案合规 PASS · 门禁 62 段 0 FAIL。
### W1134（2026-11-04）：前端质感 P0 批（暗色字重降档 / 中文防误发 / 阈值滚动 / 复制对勾 / 打印去硬编码）
> **来源**：W1095 盘点批（T50 报告）§3.4 分档排期的 P0 档四项 + 统筹会话仲裁（登记号与顺位）。
> - **文件**：docs/11-方案报告/计划方案/T89-任务计划执行与经验沉淀报告-2026-11-04.md · scripts/font_weight_probe.py · scripts/ime_scroll_probe.py
**本批要点**：
① **暗色字重降档**（site/tokens.css）：暗色令牌块补标题层级降档（h1 700→600 / h2·h3 600→500 / h4-h6 500→400）；**数字位/等宽/表格数值位一律豁免**（mono 族仅 400/500 两档·降档会落合成字重并破坏 tabular-nums 对齐）。降档规则用 `!important`——实测页内私有 `<style>` 块加载在 `<link>` **之后**，位置决定胜负（高特异性仍被覆盖）。
② **中文输入防误发**（site/data/ai-dialogue.html + site/en/ai-dialogue.html）：IME 选字期回车只完成选字不发送；选字完成后 500ms 内的回车被拦截；500ms 后正常发送（防误发不得变成永久禁用）。
③ **翻页不被拖拽**（同两页）：滚动改为阈值跟随——距底不足一行才跟随，用户上翻即停止并浮出「跳至最新」按钮；按钮放在渲染容器**之外**（D3 `container.selectAll("*").remove()` 会连带删除容器内元素）。
④ **复制对勾 2.5s 淡出**（site/static/js/cite-box.js·87 页外链引用）：成功时文案切 ✓，2.5s 后由 CSS 动画淡出并还原；连续复制可重触发；`prefers-reduced-motion` 下不播动画。
⑤ **打印样式去硬编码**（site/system.css + 330 页 INLINED 副本）：`border: 1px solid #ccc` → `var(--line)`；全站该硬编码归零（实测 330 处全在 `@media print` 块内 ⇒ 屏幕视觉零变化）。
⑥ **两个取证探针**（E-191）：J2 视觉回归的 31 项属性集**不含 font-weight** ⇒ 暗色字重类改动在 J2 上只会报「零差异」；`font_weight_probe.py` 直接读明暗双态计算样式（三条断言 + 8 例负样本自证），`ime_scroll_probe.py` 以合成 IME 事件序列驱动真实浏览器读行为结果（8 组断言 + 9 例负样本自证）。两探针首跑各抓出 3 项失败——**每一项都对应一个真实实现缺陷**（INLINED 副本未同步 / 页内私有样式覆盖 / D3 清空按钮）。
⑦ **传播面同步**：`inline_css.py --force` 重同步 330 页 INLINED 副本（值改与传播必须同批——否则改了共享层而页面没变）。
**验证**：字重探针 13 读数行失败 0 · 交互探针 8 组断言全过（含「过渡后 opacity=1」真可见性断言）· CSP 856 页零漂移（哈希 862→909）· pytest 1327 passed / 4 skipped · 两项门禁 FAIL 经基线态对照确认为环境性（缺 Node playwright·非本批引入）。
### W1133（2026-11-05）：台账回填 + 坑表经验入表 + W1125 批登记面缺陷修复

> **来源**：W1122 批三项遗留的收官批（W1125）+ 合并后核对清单实读发现的三处登记面缺陷。· 基线 = origin/main fbe9f3fd（W1130 批已合·坑表 271 条·台账正本 54 行·§六 末号 98）。
> - **文件**：docs/agent/pitfalls.md、AGENTS.md、HANDOVER.md、.agent/skills/puti-shouye/SKILL.md、docs/00-导读/W批次编号对账表.md、docs/11-方案报告/README.md、docs/11-方案报告/计划方案/T88-任务计划执行与经验沉淀报告-2026-11-04.md、CHANGELOG.md、scripts/output/file-index.md、scripts/output/_w1133_spec.json、scripts/output/_cascade_files_W1133.txt。

**本批要点**（登记面修复 + 沉淀面入表 + 回填类订正批·不新增门禁槽 ⇒ 门禁 62 段不变·坑表 271 → 277 条）：① **台账 W1125 行 git 反填回填**（0bf49abc·共 11 笔·P-43-01·回填/订正类不单开 PR·并入本批提交）；② **坑表 E-179 ~ E-184 六条经验入表**（W1125 批合并冲突四条教训 + 撤销补登记两条理由·流程/协作/取证节 141 → 147）+ 计数链 271 → 277 同步（坑表节标题 + AGENTS 总数与分项 + HANDOVER 三处 + SKILL 两处）；③ **修复 D1**——README §六 首行错位与 1/2/3 三号缺位（根因：重建登记面的脚本按行号猜插入位⇒覆盖首行历史登记行）⇒ 定点复原；④ **修复 D2**——§六 35/36 同号重复（两行均为 T-29·我方补登记引入）⇒ 撤销补登记（T-29 属他人历史交付物·缺口移交 §六 治理批·97 号留该批）；⑤ **D3**——file-index 正本 W1001 段残留由 W1136 批先行修复·本批不重复施工；⑥ **升基线后重放**（基线 fbe9f3fd·merge 不 rebase·生成面取远端基底后重跑生成链·治理面按锚点重放）。

**验证**：第 48 门禁 0 FAIL（第 32 项结构判据全项符合）· 第 31 门禁 C5e 0 FAIL · CSP 856 页 0 漂移 · §六 末号 96(T-88) 且 1/2/3 归位 · 35/36 各 1 份 · 全量 pytest 与 ci_sim --ref HEAD 读数见 T88 报告 §3.2。

### W1132（2026-11-04）：第 51 槽 merge 带入面归属劫持根修

**本批要点**（第 51 槽 merge 带入面归属劫持根修·工具层·零页面内容改动·不新增门禁槽 ⇒ 门禁 62 段不变·不新增坑表条目 ⇒ 计数链不动）：① **触发**：2026-11-04 代第三方解 W1125 与 main 的合并冲突时，第 51 槽把归属判成他批 W1127（而非本批 W1125）⇒ 提交面被拿他批 spec 判定 ⇒ 报「索引含本批 spec 之外的文件」。② **根因（实读确认）**：`pick_target_merged` 主路径已实现 merge 带入面剔除（W1129 批新增·有效），但其**兜底调用** `pick_target_with_coverage(index_text, head_text, staged)` **未透传 main_text / carried** ⇒ 兜底分支内「恰 1 个新增段且非顶位」判定用的是**含 main 侧带入段**的段集合⇒ merge 提交把 main 更高号批带入、而本提交自己的段在下方时 ⇒ 顶段判据落**带入段（他批）** ⇒ 归属劫持。③ **根修**：`pick_target_with_coverage` 增可选参数 `main_text=None` / `carried=None`（默认路径行为与 W1117 原实现逐字一致）+ 新增段集合改为「索引段 - HEAD 段 - main 侧带入段」+ 剔除后无新增段时用「剔除带入文件后的路径集」做 spec 覆盖性反查+ 兜底调用改为透传 main_text / carried。④ **单测 4 例**（带入段不劫持归属 / 兜底覆盖性反查命中本批 / 默认参数行为不变 / 真·代提仍判红）。⑤ **验证**：pytest **1321 passed / 4 skipped**（含 W1129 既有 4 例）· 全量门禁 **62 段 0 FAIL** · ruff 0 违规 · 坑表 268 不动。⑥ **纪律**：本批**不入坑表**（计数链零改动）⇒ 与并行会话（ROGSTRIX W1130 入 3 条、第五会话 W1131 零计数链）的入表时点严格串行。

> - **文件**：scripts/check_commit_scope.py、tests/unit/test_w1132_scope_carried_owner.py、scripts/output/_w1132_spec.json、scripts/output/_cascade_files_W1132.txt、docs/00-导读/W批次编号对账表.md、docs/11-方案报告/README.md、docs/11-方案报告/计划方案/T86-任务计划执行与经验沉淀报告-2026-11-04.md、CHANGELOG.md、scripts/output/file-index.md、HANDOVER.md

> - **状态**：已收官（第 51 槽归属劫持根修 + 单测 4 例 + 登记面；坑表入表待三方协调时点）
### W1130（2026-11-04）：C9 扫描面扩展 + 台账回填与腾窗 + 两面下界根修 + 三条教训入坑表

> **来源**：W1127 批遗留（① 报告件冲突标记残留未被门禁拦停·第 31 门禁 C9 原扫描面只有 5 个治理文件 ② 台账 W1127 行待 git 反填回填 ③ 三条教训待基线稳定后入坑表）· 基线 = #138 合并后 main（ed6b0cf6·坑表 268 条·台账正本 58 行）。
>
> - **文件**：scripts/check_doc_sync.py、tests/unit/test_w1130_c9_report_scope.py、docs/agent/pitfalls.md、AGENTS.md、HANDOVER.md、.agent/skills/puti-shouye/SKILL.md、docs/00-导读/W批次编号对账表.md、archive/docs/W批次编号对账表-ARCHIVE.md、docs/11-方案报告/README.md、docs/11-方案报告/计划方案/T84-任务计划执行与经验沉淀报告-2026-11-04.md、docs/11-方案报告/计划方案/T79-任务计划执行与经验沉淀报告-2026-11-04.md、CHANGELOG.md、scripts/output/file-index.md、scripts/output/_w1130_spec.json、scripts/output/_cascade_files_W1130.txt。

**本批要点**（治理面根修 + 登记面订正批·不新增门禁槽 ⇒ 门禁 62 段不变·坑表 268 → 271 条）：① **C9 扫描面根修**——第 31 门禁 C9「治理面文档禁含 Git 冲突标记」原扫描面只有 CHANGELOG / HANDOVER / 台账 / AGENTS / STRUCTURE 五个文件 ⇒ docs/11-方案报告/ 全树不在扫描面内 ⇒ 报告件里的冲突标记（含夹带的他人报告全文）无人扫 ⇒ **门禁 0 FAIL 而冲突标记已入库**；本批把扫描面扩到 docs/11-方案报告/ 全树递归 ⇒ 扩展落地后**当场抓到本方 T79 报告残留的 3 处冲突标记**并清理。② **台账四行处理 + 腾窗**——W1127 行 git 反填回填（7b616df5·共 1 笔）+ W1125 行收官回填（0bf49abc·共 11 笔）+ W1125 行 touches 错引订正（第三方 W1125 报告已改号 T80，其认领行仍指向旧号 T75 ⇒ 读者按行找不到文件）+ W1130 认领行登记；按统筹会话共享面仲裁执行腾窗（迁出 W1072-W1076 共 5 行 ⇒ 正本 **54 行** W1077..W1130 ≤ 窗口 60）⇒ 腾窗后三组读数 = 正本 **54 行 / 54 唯一号 / 重复 0** + 归档 **421 行 / 421 唯一号 / 重复 0** + **两面交集 0**；**W1070 与 W1071 各 1 份**（避开已在归档的两行 ⇒ 零真重复·E-168 同族风险已规避）；归档件注记同步（正本保留行数 60 → 54 + 追加 W1130 迁入注记）。③ **两面下界根修**——收官链 rebuild 步报「两面同 W 号下界未对齐」（CHANGELOG W1049 / file-index W1001）⇒ 根因 = #135 批删了 CHANGELOG 的 W1001 段但未同步 file-index 侧 ⇒ 迁出 file-index 的 W1001 段 ⇒ 两面同下界 **W1049** ✓。④ **三条教训入坑表 E-176 ~ E-178**（结构缺陷类门禁扫描面盲区 / 复核须读目标 ref 的树且同文件两候选版本逐行取优 / 跨层写脚本时转义被外层模板串提前吃掉致退出码 0 但零输出）+ 计数链全量同步（268 → 271·6 处）。⑤ **T79 报告读数订正**：归档读数由合并前快照 411 行订正为合并后实读 414 行（行数随各批腾窗变化·以合并后实读为准）。

**验证**：第 31 门禁 0 FAIL + 全量 pytest + 收官链 14 步全绿 + ci_sim --ref HEAD 验提交态。

> - **状态**：已收官（C9 扫描面扩展 + 台账四行处理与腾窗 + 两面下界根修 + 教训入坑表 + T79 读数订正）
### W1129（2026-11-04）：PR 节奏纪律变更 + 提交范围门禁多批归属支持

**本批要点**（PR 节奏纪律变更 + 提交范围门禁多批归属支持·铁律层 + 工具面·零页面内容改动·不新增门禁槽 ⇒ 门禁 62 段不变·**不新增坑表条目 ⇒ 计数链不动**）：① **用户 2026-11-04 裁定的新 PR 节奏**（实测 11-04 开 9 个 PR、11-03 开 11 个·两日 20 个·其中 **7 个是纯回填/订正**·无一带新功能）：**回填与订正类改动永不单独开 PR**（台账行回填 / CHANGELOG 数字订正 / 复盘补记 一律并入**下次在途批**的 PR）+ **同一会话当日多个批次合并进同一个 PR**（批次号仍各自登记占号 / 认领行 / CHANGELOG 段 / 报告）+ 跨会话仍各自开 PR（不牺牲并行度）⇒ 落 AGENTS §6 **铁律 21**（改写 W1118「一批一 PR」旧口径；每 PR ≈ 25 个 job ⇒ **PR 数是 job 数的乘数**，触发面治理与 PR 节奏治理是同一问题的两面）。② **配套工具根修**：第 51 槽「提交范围门禁」原按「新增段集合恰 1 个」定归属 ⇒ 多批同 PR 时新增段 > 1 ⇒ 归属落空并拿**单批** spec 当应动全集 ⇒ 本提交里前几批的交付面被判「spec 之外」⇒ **假红** ⇒ 根修 = 新增 _multi_batch_scope：新增段 > 1 时归属取**批号最小**者、应动全集取**各批 spec 并集**；**真·代提仍判红**（不在任何一批 spec 内的文件仍红·并集不含者照红）⇒ 判据强度不降，且单批提交路径逐字未变（既有 6 例自测仍 6/6）。③ **实跑读数**：MULTI_TARGET=1129 · MULTI_PATHS=['/a.py','/b.py'] · PLAN_ALL_IN_SCOPE=True · PLAN_WITH_EVIL=False extra=['/evil.py']；新增单测 4 例全过。④ **不新增坑表条目** ⇒ 计数链零改动（并行会话 W1125 未合并·远端 267 vs 其 261 口径·此刻动必对撞）⇒ 两条教训（多批归属·PR 数是 job 数乘数）暂落 T78 报告 §5，待下一批入坑表（拟 E-172 起）。

**文件**：
- docs/agent/pitfalls.md- AGENTS.md- .agent/skills/puti-shouye/SKILL.md- HANDOVER.md- scripts/batch_closeout.py- scripts/batch_cascade.py- scripts/check_repo_layout.py- tests/unit/test_w1124_closeout_rebuild.py- scripts/output/_w1124_spec.json- scripts/output/_cascade_files_W1124.txt- docs/00-导读/W批次编号对账表.md- archive/docs/W批次编号对账表-ARCHIVE.md- docs/11-方案报告/计划方案/T75-任务计划执行与经验沉淀报告-2026-11-04.md- docs/11-方案报告/README.md- CHANGELOG.md- scripts/output/file-index.md- README.md- STRUCTURE.md- docs/00-导读/项目说明.md- CITATION.cff- site/data/search.html- site/en/search.html- .github/workflows/README.md- scripts/output/stats.json- scripts/output/stats-index.md- scripts/output/stats-changelog.json- scripts/output/tools-inventory.md- archive/docs/AGENTS-ARCHIVE.md- docs/INDEX.md- scripts/INDEX.md- scripts/output/INDEX.md- scripts/output/README.md- tests/unit/INDEX.md- tests/unit/README.md- pytest.ini- docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md- docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md- site/index.html- site/data/cross-time-danmaku.html- site/data/tag-cloud.html- site/dukou-engine.html- scripts/cascade_idempotence.py- scripts/batch_cascade.py- scripts/backfill_changelog.py- tests/unit/test_w1122_cascade_idempotence.py- tests/unit/test_w1122_pending_faces.py- docs/00-导读/W批次编号对账表.md- docs/11-方案报告/计划方案/T74-任务计划执行与经验沉淀报告-2026-11-04.md- docs/11-方案报告/README.md- scripts/output/_w1122_spec.json- scripts/output/_cascade_files_W1122.txt- CHANGELOG.md- scripts/output/file-index.md- HANDOVER.md- AGENTS.md- .github/workflows/README.md- site/index.html- site/data/cross-time-danmaku.html- site/data/tag-cloud.html- site/dukou-engine.html- README.md- STRUCTURE.md- docs/00-导读/项目说明.md- CITATION.cff- scripts/output/tools-inventory.md- scripts/output/stats.json- scripts/output/stats-index.md- scripts/output/stats-changelog.json- archive/docs/AGENTS-ARCHIVE.md- pytest.ini- docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md- docs/INDEX.md- scripts/INDEX.md- archive/docs/W批次编号对账表-ARCHIVE.md- docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md- site/data/search.html- site/en/search.html- scripts/output/INDEX.md- scripts/output/README.md- tests/unit/INDEX.md- tests/unit/README.md- tests/unit/test_w1102_batch_closeout.py- tests/unit/test_w1128_pycompile_gate.py- docs/11-方案报告/计划方案/T77-任务计划执行与经验沉淀报告-2026-11-04.md- scripts/output/_w1128_spec.json- scripts/output/_cascade_files_W1128.txt- scripts/check_commit_scope.py- tests/unit/test_w1129_commit_scope_multibatch.py- docs/11-方案报告/计划方案/T78-任务计划执行与经验沉淀报告-2026-11-04.md- scripts/output/_w1129_spec.json- scripts/output/_cascade_files_W1129.txt

**认领登记 W1129**（占号 session=mvs_1d2745db…·preflight PASS·touches 全清单登记·W1128 批收官后顺延）。

**验证**：收官链 14 步全绿（含 pycompile 门禁步·CSP 856 页 0 漂移）· 门禁 62 段 0 FAIL（CI 同档 full）· 全量 pytest 0 failed · ruff check scripts/ 0 违规 · 新增单测 4 例 + 既有 6 例自测 6/6。

### W1128（2026-11-04）：收官链 py_compile 语法自检门禁

**本批要点**（收官链 py_compile 语法自检门禁·工具面·零页面内容改动·不新增门禁槽 ⇒ 门禁 62 段不变·**不新增坑表条目 ⇒ 计数链不动**）：① **病根**：批量写 .py 后若落盘出现语法错（字面两字符反斜杠 n、缺引号、续行残缺），此前**无任何机器门禁拦截** ⇒ 坏文件直接进索引进提交，而本地跑的是好版本 ⇒ 本地全绿、提交里是坏版本 ⇒ 直到 CI 才暴露（2026-11-04 实测：8 个文件同时触发 3 个 job 红灯）。② **根修 = 收官链新增 pycompile 步**（排在 add 之后·紧随其后）：对**三态清单**（索引态 + 工作树态 + 未跟踪·排除 .gitignore）的全部 .py 逐件 compile()（**只编译不落盘**·不污染 __pycache__）⇒ 任一件 SyntaxError 即打印「文件:行号 + 错误」并**中止整条收官链**（fail-closed·宁可停在收官前也不让坏件进提交）；纯逻辑抽为 _compile_check 便于负样本直喂。③ **负样本实测**：在工作树放入语法错文件 ⇒ 门禁拦停（退出码 3·报出 文件:1: invalid syntax）⇒ 删除探针后复跑「3 件 .py 语法自检通过」⇒ 证明该门禁真会拦而非只跑通。④ **顺序锁同步**：既有行为锁只锁 add→refresh→stats→index→csp→cspcheck 的相对顺序 ⇒ 插入 pycompile 不破坏它；另**追加**一条行为锁「pycompile 实际被调用且排在 add 之后」+ 声明顺序断言（pycompile == add + 1），防 STEPS 与 main 双写漂移。⑤ **号段让号**：W1127 于 15:11:09 被并行会话先落地占号 ⇒ 我方顺延用 W1128；台账因新增认领行达 61 段超窗 ⇒ 先腾窗迁出 W1065-W1066（正本 59 行）再动工。⑥ **不新增坑表条目** ⇒ 计数链零改动（避与并行会话 W1125 未合并批的计数链对撞）· 本批教训暂落 T77 报告 §5 · 待下一批入表。

**文件**：
- docs/agent/pitfalls.md- AGENTS.md- .agent/skills/puti-shouye/SKILL.md- HANDOVER.md- scripts/batch_closeout.py- scripts/batch_cascade.py- scripts/check_repo_layout.py- tests/unit/test_w1124_closeout_rebuild.py- scripts/output/_w1124_spec.json- scripts/output/_cascade_files_W1124.txt- docs/00-导读/W批次编号对账表.md- archive/docs/W批次编号对账表-ARCHIVE.md- docs/11-方案报告/计划方案/T75-任务计划执行与经验沉淀报告-2026-11-04.md- docs/11-方案报告/README.md- CHANGELOG.md- scripts/output/file-index.md- README.md- STRUCTURE.md- docs/00-导读/项目说明.md- CITATION.cff- site/data/search.html- site/en/search.html- .github/workflows/README.md- scripts/output/stats.json- scripts/output/stats-index.md- scripts/output/stats-changelog.json- scripts/output/tools-inventory.md- archive/docs/AGENTS-ARCHIVE.md- docs/INDEX.md- scripts/INDEX.md- scripts/output/INDEX.md- scripts/output/README.md- tests/unit/INDEX.md- tests/unit/README.md- pytest.ini- docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md- docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md- site/index.html- site/data/cross-time-danmaku.html- site/data/tag-cloud.html- site/dukou-engine.html- scripts/cascade_idempotence.py- scripts/batch_cascade.py- scripts/backfill_changelog.py- tests/unit/test_w1122_cascade_idempotence.py- tests/unit/test_w1122_pending_faces.py- docs/00-导读/W批次编号对账表.md- docs/11-方案报告/计划方案/T74-任务计划执行与经验沉淀报告-2026-11-04.md- docs/11-方案报告/README.md- scripts/output/_w1122_spec.json- scripts/output/_cascade_files_W1122.txt- CHANGELOG.md- scripts/output/file-index.md- HANDOVER.md- AGENTS.md- .github/workflows/README.md- site/index.html- site/data/cross-time-danmaku.html- site/data/tag-cloud.html- site/dukou-engine.html- README.md- STRUCTURE.md- docs/00-导读/项目说明.md- CITATION.cff- scripts/output/tools-inventory.md- scripts/output/stats.json- scripts/output/stats-index.md- scripts/output/stats-changelog.json- archive/docs/AGENTS-ARCHIVE.md- pytest.ini- docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md- docs/INDEX.md- scripts/INDEX.md- archive/docs/W批次编号对账表-ARCHIVE.md- docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md- site/data/search.html- site/en/search.html- scripts/output/INDEX.md- scripts/output/README.md- tests/unit/INDEX.md- tests/unit/README.md- tests/unit/test_w1102_batch_closeout.py- tests/unit/test_w1128_pycompile_gate.py- docs/11-方案报告/计划方案/T77-任务计划执行与经验沉淀报告-2026-11-04.md- scripts/output/_w1128_spec.json- scripts/output/_cascade_files_W1128.txt

**认领登记 W1128**（占号 session=mvs_1d2745db…·W1127 已让给并行会话·preflight PASS·touches 全清单登记）。

**验证**：收官链 12 步全绿（含新增 pycompile 步·regsurface OK·CSP 856 页 0 漂移）· 门禁 62 段 0 FAIL（CI 同档 full）· 全量 pytest 1310 passed / 4 skipped · ruff check scripts/ 0 违规 · 新增单测 4 例 + 行为锁 1 例 · 负样本实测门禁拦停（退出码 3）。

### W1127（2026-11-04）：治理收官批·台账回填 + 滚动独立入口 + 历史缺口体检

> **来源**：T74（W1122 批）报告遗留 R-2（滚动重跑守卫的独立入口）与 R-B 前置（历史缺口按序补齐的前置体检）· 归集自 W1122 批收官登记。
>
> - **文件**：scripts/batch_cascade.py、scripts/check_segment_gaps.py、tests/unit/test_w1127_closeout_tools.py、scripts/output/_w1127_spec.json、scripts/output/_cascade_files_W1127.txt、docs/00-导读/W批次编号对账表.md、archive/docs/W批次编号对账表-ARCHIVE.md、docs/11-方案报告/计划方案/T79-任务计划执行与经验沉淀报告-2026-11-04.md、docs/11-方案报告/README.md、CHANGELOG.md、scripts/output/file-index.md、HANDOVER.md、AGENTS.md、.github/workflows/README.md、README.md、STRUCTURE.md、docs/00-导读/项目说明.md、CITATION.cff、site/data/search.html、site/en/search.html、site/index.html、site/data/cross-time-danmaku.html、site/data/tag-cloud.html、site/dukou-engine.html、scripts/output/stats.json、scripts/output/stats-index.md、scripts/output/stats-changelog.json、scripts/output/tools-inventory.md、docs/INDEX.md、scripts/INDEX.md、scripts/output/INDEX.md、scripts/output/README.md、tests/unit/INDEX.md、tests/unit/README.md、pytest.ini、docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md、docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md。

**一、台账回填与腾窗**：台账 W1124 行 git 反填回填（hash 18a06a80·共 3 笔·指纹 de8ab24caa72）并入本批提交（不单开 PR）；台账腾窗迁出最老两行（W1065-W1066）使正本回到窗口内；W1127 认领行登记（含 touches 全清单）。

**二、里程碑滚动独立入口（根修 T74 R-C）**：此前滚动只能作为「本批块插入」的副动作发生，若某批只想滚动或需重跑滚动，没有独立入口 ⇒ 只能手工改文档。W1124 已把幂等守卫下沉到_handover_rotate_oldest 内部（本批块已在链上 ⇒ 零变化），本批补上独立入口 --rotate-only：独立重跑同样零变化（零红灯·不丢信息），且不落盘时只报 dry-run。

**三、历史缺口体检工具（根修 T74 R-B 前置）**：此前「立段/落段只看一面」根修后暴露的历史缺口只散落在运行输出里，既无法复核，也无法判断内容能否复原 ⇒ 新增 scripts/check_segment_gaps.py：盘点台账（正本 + 归档）出现过的批次号，与 CHANGELOG 与 file-index 两面正本的段集合做差集，输出缺口清单并逐件给出可复原来源提示（CHANGELOG 归档 / file-index 归档 / 台账归档是否含该批号）。本工具**只体检不补段**（补段须先评估可复原性，避免造段）⇒ **实测当前基线缺口 0 项**（两面正本已覆盖台账全部批次）⇒ T74 遗留 B 的补段动作无需执行。

### W1126（2026-11-04）：截图审查 scope 判定根修（EN 搜索页定向 + 搜索索引内容级免审）

> **来源**：用户 2026-11-04「为什么不直接在 main 分支进行」追问后引出「为什么 Screenshot Review 每次都要跑」诊断 → 用户选定「把 B+C 方案落成 W1126 的施工计划」。
>
> - **文件**：scripts/check_screenshot_scope.py、tests/unit/test_w1126_screenshot_scope.py、docs/11-方案报告/计划方案/T81-任务计划执行与经验沉淀报告-2026-11-04.md、docs/11-方案报告/README.md、docs/00-导读/W批次编号对账表.md、CHANGELOG.md、scripts/output/_w1126_spec.json、scripts/output/_cascade_files_W1126.txt。

**一、诊断根因（三段错配·非配置过严）**：Screenshot Review 每批必跑的真实原因 = ① 收官链每批必改 `site/en/search.html`（版本面推进 + 搜索索引刷新）② bash case 的 `site/*` 在 `site/data/*` 之后命中 ⇒ 掉进「未知路径 ⇒ 保守全量」兜底 ⇒ **为 2 行零视觉改动付全站 88 页截图代价**。PR #130 实测坐实：39 个改动文件逐文件复现，`site/en/search.html` 判定为 FULL，其余 4 个页脚页 SKIP、`site/data/search.html` TARGETED；该文件实际改动仅 2 行（1 行 CSP `sha256-` 哈希 + 1 行 230,455 字符的内嵌搜索索引常量）⇒ 零布局改动、零样式改动、零 DOM 结构改动。

**二、B+C 两条修法（判据强度不降）**：**B** 新增 `site/en/*` ⇒ targeted 分支（截该页 + 入口页·保留该页视觉审查强度·只削范围）；**C** 内容级免审判据（变更行集合 ⊆ {CSP 哈希行, 内嵌索引数据行} ⇒ 免审·白名单式最保守·任一未识别行变化即不 skip）。**判据抽为仓内脚本** `scripts/check_screenshot_scope.py`（单一事实源·可单测·可复算·workflow 只调用不内联）。

**三、协作事故与隔离处置（DV-03）**：施工中共享工作树曾被清空未提交内容（reflog 实测 15:18:32）⇒ 依 AGENTS 铁律 24 迁独立 worktree `D:/xiyouji-w1126` 重建，共享树他方在途改动**不动·不代提·不回滚**；报告号两次主动让号（T-76 → T-79 → T-81）以避让他方同号文件。

**四、验证**：第 48 门禁计划方案合规 0 FAIL（T81 全项符合）· 第 51 门禁提交范围 0 FAIL · 第 46 门禁搜索索引新鲜度 0 FAIL · 第 31 门禁文档口径体检 0 FAIL · CSP 856 页 0 漂移 · 脚本自测 22 例全过 · 单测 26 例全过。

> - **状态**：已收官（截图审查 scope 判定根修 + B/C 两规则落地 + 判据脚本化 + 单测自证）

### W1125（2026-11-04）：自举产物教训入坑表 + W1001 段清理 + 档 3 消费方式原型



> **来源**：W1122 批登记的三项遗留（① W1123 自举产物教训入坑表 ② 正本与归档并存的存量 W1001 段清理·须用户批准 ③ 档 3 剩余可施工面近耗尽·需先改消费方式）· 用户 2026-11-04 裁决：W1001 段删正本那份保留归档、档 3 本批出方案并做 1 页原型验证。
>
> - **文件**：docs/agent/pitfalls.md、AGENTS.md、HANDOVER.md、.agent/skills/puti-shouye/SKILL.md、CHANGELOG.md、docs/00-导读/W批次编号对账表.md、docs/11-方案报告/计划方案/T80-任务计划执行与经验沉淀报告-2026-11-04.md、docs/11-方案报告/README.md、site/data/chart-design.html、scripts/output/_w1125_spec.json、scripts/output/_cascade_files_W1125.txt、archive/docs/W批次编号对账表-ARCHIVE.md、scripts/INDEX.md、docs/11-方案报告/计划方案/T79-任务计划执行与经验沉淀报告-2026-11-04.md。

**本批要点**（清理与沉淀批 + 1 页原型·不新增门禁槽 ⇒ 门禁 62 段不变·坑表 267 → 268 条）：① **坑表 E-164 入表**——W1123 实证的「自举产物（spec / 级联清单 / 工具生成的清单文件）必须被它自己声明的应动全集收录，否则提交后 CI 干净 checkout 判「本批无 spec·判据不可执行」」⇒ 计数链全量同步（267 → 268·基于最新 origin/main 的 267 条基线重算）；**本批一处自我纠错如实留痕**：首次同步把计数链误改为「总数 268 / 级联 26 / 流程 138」（当时取自并行会话 7 条混入共享树的中间态，非 HEAD 干净基线；HEAD 实为 260 / 22 / 134）⇒ 经 git show HEAD 干净对照后回正为 261 / 22 / 135；**合并并行会话 W1124 批（E-165 ~ E-171，7 条）后按最新基线 267 重算 ⇒ 现役声明为总数 268 / 级联 26 / 流程 138**，第 31 门禁 C5e 复跑 0 FAIL。② **正本与归档并存的存量 W1001 段清理**（用户已批准「删正本那份·保留归档」）——逐行实证两份**段本体 15 行逐字完全相同**（此前「35 行仅差 1 行」的表象源于切段口径把段后文件级块一并纳入）；删除边界 = 正本 CHANGELOG.md 行 1313–1327，段后 19 行文件级块（# 更新日志标题 + 阅读契约 + Unreleased + 编号规则行 + 全站页数口径 + 维护契约）**原样保留**；前置断言三条全过：段本体与归档逐字一致、编号规则锚点行（行 1337）在删除区间外、删除后锚点计数仍为 1 ⇒ 版本面推进器锚点完好；归档 CHANGELOG-ARCHIVE.md 行 833–847 原样未动。③ **档 3 消费方式：实算推翻既有判断 + 1 页原型**——复现 W1100 归档盘点口径实算：全站调色板色 1658 处 / 331 页、豁免登记页 181 页、排除豁免页后余 **153 页且每页恰好 1 处**；**决定性发现**：那 153 处**全部是同一条暗色补偿规则的逐页副本**（`html[data-theme="dark"] svg [fill="#3a6b8c" i] { fill: #7d99a9; }`，全站 328 页各存一份），而**真实图表消费面 1330 处 100% 落在 181 个豁免页内**、非豁免页为 0 ⇒ 既有登记「每页 ≤2 处⇒近耗尽」把补偿规则副本误计为可施工面，**逐页改造 153 页属无效功**（改的不是图表消费位·且补偿收口按 W1100 定案排在档 3 之后·禁改）。原型实证（site/data/chart-design.html·144 图元·浏览器计算样式实测非源码推断）：10 处硬编码 #e9b885 → `var(--chart-5)` 后**浅色态实际值 rgb(216,207,188) ≡ 改前 #e9b885（逐值等价）**、暗色态一致（--chart-5 暗色未定义⇒沿用浅色）、图元数 144/144、错误未增、CSP 违规 0 ⇒ **表现属性位 .attr('fill') 确实解析 var()**（W1097/W1108 口径再证）；原型期两次真实失败均已归因：改内联脚本未重算 CSP 哈希 ⇒ 浏览器拒执行 ⇒ 渲染塌缩 144→3（须 Set-Location 到 worktree 再跑 generate_csp.py）；令牌槽位映射错误（#e9b885 误映射 --chart-3=#B38F58，真值为 --chart-5=#D8CFBC）⇒ 视觉回归。④ **工作树隔离**：三方会话共用 D:\xiyouji 造成级联/收官链互相覆盖 ⇒ 本批全程迁独立 worktree（D:\xiyouji-w1125·基线 30a73582）施工，共享树恢复零污染；并行会话 W1124 与我方 W1125 号段无冲突。

**验证**：合并后 worktree 内 verify_delivery --scope auto **62 段中 2 项 FAIL 属环境性假红**（第 43 槽可视化数据断言 + 朱砂实底槽：两棵工作树均无 node_modules ⇒ 无 playwright 浏览器环境，门禁拒绝在无浏览器环境出具结论；同一提交在 CI 侧「Delivery Gate (verify_delivery.py)」pass 即为绿证）· 第 31 门禁 C5e 0 FAIL · 第 54 槽坑表编号唯一性 0 FAIL · CSP 856 页 0 漂移 · 原型页双态浏览器实测逐值等价 · 归档 W1001 段行 833–847 逐字未动 · 编号规则锚点计数 = 1。

> - **状态**：已收官（坑表 E-164 + W1001 段清理 + 档 3 实算与原型 + 台账 W1122 行回填 + W1125 认领行登记；档 3 全量施工待口径重建后另批）

### W1124（2026-11-04）：治理收尾批·教训入坑表 + 重建入口收进收官链

> **来源**：T74 报告遗留 R-A（重建入口收进收官链）/ R-C（里程碑滚动重跑守卫）/ R-D（教训入坑表）· 归集自 W1122 批收官登记。
>
> - **文件**：docs/agent/pitfalls.md、AGENTS.md、.agent/skills/puti-shouye/SKILL.md、HANDOVER.md、scripts/batch_closeout.py、scripts/batch_cascade.py、tests/unit/test_w1124_closeout_rebuild.py、scripts/output/_w1124_spec.json、scripts/output/_cascade_files_W1124.txt、docs/00-导读/W批次编号对账表.md、docs/11-方案报告/计划方案/T75-任务计划执行与经验沉淀报告-2026-11-04.md、docs/11-方案报告/README.md、CHANGELOG.md、scripts/output/file-index.md、README.md、STRUCTURE.md、docs/00-导读/项目说明.md、CITATION.cff、site/data/search.html、site/en/search.html、.github/workflows/README.md、scripts/output/stats.json、scripts/output/stats-index.md、scripts/output/stats-changelog.json、scripts/output/tools-inventory.md、archive/docs/AGENTS-ARCHIVE.md、docs/INDEX.md、scripts/INDEX.md、scripts/output/INDEX.md、scripts/output/README.md、tests/unit/INDEX.md、tests/unit/README.md、pytest.ini、docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md、docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md。

**一、教训入坑表（根修 T74 R-D）**：W1122 批七条教训入表 E-165 ~ E-171 —— ① 同一机制的多个实现点若无统一判定原语则行为必然分裂；② 幂等化的对象不止是插入动作，还包括有状态的配套副作用；③ 多副本实现收敛到同一入口；④ 立段落段判定若只看一面则另一面的缺口永远补不上；⑤ 兜底保护要先于自动补段；⑥ 定位区间不得用条目正文内可能出现的分隔符界定；⑦ 链式面必须按批号序落位。坑表 260 → 267 条，计数链 13 处同步（坑表六个主题节标题 + AGENTS 阅读契约与六主题分项行 + HANDOVER 两处总计数与一处历史滞后补平 + SKILL 两处）。

**二、重建入口收进收官链（根修 T74 R-A）**：rebuild_section.py 此前是独立入口（W1120 建）⇒ 段内容与 spec 不一致时只能人工想起单独跑它 ⇒ 改完段内容后重建这一步在流程里是断的 ⇒ 段与 spec 长期漂移。本批把它接入收官链主链：段已存在且内容一致则零变化（不写盘），内容不一致则就地重建本批段（历史段逐段比对断言不变），两面皆未立段则跳过（建段归级联与补段工具）。顺序锁：rebuild 必须排在 precheck 之前 —— precheck 是 fail-closed 中止，修复步排其后即死路径（W1117 同族教训：腾窗步前置）。

**三、里程碑滚动幂等守卫（根修 T74 R-C）**：滚动淘汰的跳过守卫此前只在调用点（插入路径）生效 ⇒ 单独重跑滚动逻辑仍会再淘汰一块（指针指向的块被淘汰后指针移到新最老块 ⇒ 再跑一次就再淘汰一块 ⇒ 信息丢失且零红灯）。本批把守卫下沉到函数内：本批块已存在于链上即视为本批已滚动过 ⇒ 直接返回（零变化）；本批块不在链上时滚动照常执行（守卫不得变成一律跳过）。

**四、台账订正与自证**：台账 W1122 行自证例数由 24 订正为 36（声明与落地对齐）并完成 git 反填回填；新增自证 12 例（收官链步骤顺序锁 4 例 + 幂等段重建 4 例 + 滚动守卫 2 例 + 布局门禁 worktree 形态适配 2 例）。

### W1123（2026-11-04）：预约释放语义根修 + 提交范围门禁 merge 场景归属根修

**本批要点**（预约释放语义根修 + 提交范围门禁 merge 场景归属根修·不新增门禁槽 ⇒ 门禁 62 段不变·坑表 258 → 260 条）：① **release 删除语义根修**：预约表有多个落点（本工作树表 + 同机兄弟克隆表 + 用户级共享表），写回函数统一走「先合并所有可见记录再 update」⇒ 释放操作也走同一路径 ⇒ 合并步骤把磁盘旧记录（含刚删的那条）重新合回 ⇒ **已释放的号复活**（自报已释放而 list 仍在⇒ 他方取号跳段）⇒ 根修 = 删除走独立「替换语义」路径 + 删除后**逐落点回读断言**（打印成功不算证据）+ 他人同号记录仅 session 相同时才删；新增 4 例单测；**由真实让号操作证明**（release W1122 真删除并回读校验通过）。② **第 51 槽 merge 场景归属根修**：并行会话 W1120 实证——我方 PR 先合入 main 后对方把新 main 合进自己分支 ⇒ 索引相对 HEAD 的新增段集合含他批段 ⇒ 归属判到他批 ⇒ 本提交交付面被判 spec 之外（假红）⇒ 根修 = 剔除「merge 带入面」（带入的段 = origin/main 侧已存在·带入的文件 = 索引 blob sha 与 origin/main 侧相同）⇒ 剔除后新增段集合为空则用剩余路径集做 spec 覆盖性反查定位归属；**判据强度不降**（内容与 main 不同者仍进判定⇒ 真越界仍判红）；新增 5 例单测。③ **号段让号**：取号两次得 W1122 与 W1123 ⇒ 主动 release W1122 让给并行会话（先声明者保留）· 我方用 W1123。④ **经验入库**：坑表 E-162（共享表写回的删除语义与合并语义不能混用）与 E-163（按索引态新增段定归属的门禁在 merge 场景会误判他批交付面为越界）+ 计数链 7 处同步（258 → 260）。

**文件**：
- .github/workflows/README.md- AGENTS.md- CHANGELOG.md- CITATION.cff- HANDOVER.md- README.md- STRUCTURE.md- archive/docs/AGENTS-ARCHIVE.md- archive/docs/W批次编号对账表-ARCHIVE.md- docs/00-导读/W批次编号对账表.md- docs/00-导读/文档规范.md- docs/00-导读/项目说明.md- docs/11-方案报告/README.md- docs/11-方案报告/计划方案/T68-任务计划执行与经验沉淀报告-2026-11-04.md- docs/11-方案报告/计划方案/T72-任务计划执行与经验沉淀报告-2026-11-04.md- docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md- docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md- docs/INDEX.md- pytest.ini- scripts/INDEX.md- scripts/batch_cascade.py- scripts/check_doc_size_budget.py- scripts/output/INDEX.md- scripts/output/README.md- scripts/output/_cascade_files_W1120.txt- scripts/output/_vermilion_solid_cache.json- scripts/output/_w1120_spec.json- scripts/output/file-index.md- scripts/output/stats-changelog.json- scripts/output/stats-index.md- scripts/output/stats.json- scripts/output/tools-inventory.md- scripts/rebuild_section.py- site/data/cross-time-danmaku.html- site/data/search.html- site/data/tag-cloud.html- site/dukou-engine.html- site/en/search.html- site/index.html- tests/unit/INDEX.md- tests/unit/README.md- tests/unit/test_w1120_cascade_file_index_idempotence.py- tests/unit/test_w1120_size_threshold_and_rebuild.py- .agent/skills/puti-shouye/SKILL.md- docs/11-方案报告/计划方案/T71-任务计划执行与经验沉淀报告-2026-11-04.md- docs/agent/pitfalls.md- scripts/batch_closeout.py- scripts/check_registration_surface.py- scripts/ledger_backfill.py- scripts/output/_cascade_files_W1121.txt- scripts/output/_w1121_spec.json- scripts/reserve_w.py- tests/unit/test_w1121_reserve_w.py- scripts/check_commit_scope.py- docs/11-方案报告/计划方案/T73-任务计划执行与经验沉淀报告-2026-11-04.md- tests/unit/test_w1123_commit_scope_merge.py- tests/unit/test_w1123_reserve_release.py

**认领登记 W1123**（占号 session=mvs_1d2745db…·跨克隆可见性根修后取得·W1122 已主动让给并行会话·preflight 无风险项 PASS）。

**验证**：收官链 12 步全绿（含腾窗步·regsurface OK·CSP 856 页 0 漂移）· 门禁 62 段 0 FAIL（CI 同档 full）· 全量 pytest 1256 passed / 4 skipped · ruff check scripts/ 0 违规 · 新增单测 9 例。

### W1122（2026-11-04）：级联插入型面幂等原语 + 补段工具双面判定根修

> **来源**：W1120 批登记的两项遗留（① 补段工具「已立段」判定只看 CHANGELOG 一面 ⇒ file-index 段永远补不上；② 级联插段仍非幂等 ⇒ 落段后无法重跑级联）· 归集自 W1117 §6.1 R-01。

> - **文件**：scripts/cascade_idempotence.py、scripts/batch_cascade.py、scripts/backfill_changelog.py、tests/unit/test_w1122_cascade_idempotence.py、tests/unit/test_w1122_pending_faces.py、docs/00-导读/W批次编号对账表.md、docs/11-方案报告/计划方案/T74-任务计划执行与经验沉淀报告-2026-11-04.md、docs/11-方案报告/README.md、scripts/output/_w1122_spec.json、scripts/output/_cascade_files_W1122.txt、CHANGELOG.md、scripts/output/file-index.md、HANDOVER.md、AGENTS.md、.github/workflows/README.md、site/index.html、site/data/cross-time-danmaku.html、site/data/tag-cloud.html、site/dukou-engine.html、README.md、STRUCTURE.md、docs/00-导读/项目说明.md、CITATION.cff、scripts/output/tools-inventory.md、scripts/output/stats.json、scripts/output/stats-index.md、scripts/output/stats-changelog.json。

**一、幂等 upsert 原语（新增单一事实源）**：新增 scripts/cascade_idempotence.py，提供 upsert_entry 与 locate_entry 两个纯函数——本批条目不存在⇒插入（既有行为不变）·已存在且内容一致⇒**零变化**（可重复执行）·已存在但内容不一致⇒**替换**为新内容。各面只提供各自的定位规则，判定逻辑单点收敛。

**二、六个插入型面接入（根修「静默重复」与「断言炸」并存）**：病根是各插入型面**各自为战**、无统一的「本批号在本面是否已落内容」判定⇒ 交接文档头链 entry 与里程碑块、AGENTS 脚注条目、workflows 里程碑尾标记**静默重复**（重跑级联内容越滚越多且不报错），而 CHANGELOG 段与页脚链 token 则 fail-closed（重跑即断言炸）⇒ 「落段后无法重跑级联」。本批把六面统一到原语：交接文档头链与里程碑块、AGENTS 脚注条目、workflows 尾标记、页脚链 token 四面由「静默重复」改为「一致零变化·不一致替换」；CHANGELOG 段改为「已立段⇒不重复插入·内容不一致⇒fail-closed 并指引 scripts/rebuild_section.py 重建」（与 W1120 的 file-index 面同策略）；里程碑滚动（淘汰最老块）属有状态操作⇒ 重跑路径**跳过滚动**，避免二次淘汰丢信息。

**三、补段工具双面独立判定（根修遗留 A）**：backfill_changelog 的立段判定原只看 CHANGELOG 一面 ⇒ 某批 CHANGELOG 已立段而 file-index 未立段时被判「已立段」整批跳过 ⇒ **file-index 段永远补不上**。本批改为两面分判、只补真缺的那一面，并把字段完整性检查按「写入去向」拆成两面所需字段（判据强度不降：该面缺字段仍 fail-closed）。另加**历史缺口保护**：待补 W 号低于已立段 max 时默认只提示不自动补（补老段会改现役面并撞体积窗）⇒ 须显式 --only 确认。实测暴露一处真实历史缺口（两面皆无段的旧批次）⇒ 登记待下一批按序补齐。

**四、台账回填与自证**：顺带回填台账前批两行（git 反填·行指纹复核一致）；新增自证 36 例（幂等原语与六面接入 31 例 + 双面独立判定 5 例），其中负样本直接实证原缺陷形态：脚注条目重跑出现同号重复、页脚链重跑触发 token 去重断言。

**五、追加根修（PR #130 CI 红项回灌）**：CI 第 31 门禁 C2 判红「交接文档头链链首 W1122 ≠ CHANGELOG 顶段 W1123」⇒ 根因是里程碑块**无条件插到链首**⇒ 低号批（W1122 < 现役 W1123）占据链首 ⇒ 改为按批号序落位（单一事实源 _upsert_handover_milestone·含位置校正），并把块区间**有界于进度段**（原实现对链尾块返回 end=len(s)⇒ 替换会吞掉后文）。同一轮复查又抓出脚注条目区间按「下一个『；』」界定 ⇒ **条目正文含分号时区间被截断** ⇒ 每次重跑判定「内容不一致」⇒ 同号条目无限累积（实测脚注累积到 4 份）⇒ 改为按**下一个条目 token** 定界并收敛同号副本。

### W1121（2026-11-04）：收官链缺陷根修 + 跨克隆占号机制根修 + 台账回填

**本批要点**（收官链缺陷根修 + 跨克隆占号机制根修 + 台账回填·不新增门禁槽 ⇒ 门禁 62 段不变·坑表 256 → 258 条）：① **静默失效根修**：W1119 新增收官链腾窗步在读台账行数时用了 io.open 却**未 import io** ⇒ NameError 被同函数宽 except Exception 捕获后 return True ⇒ **台账行窗口判定从未真正触发**（每批收官都「成功」rc=0·缺陷零红灯·可持续数周）⇒ 根修 = 改仓内主流 open(..., encoding=) 写法 + except 收窄到 ImportError 与 OSError ⇒ 代码缺陷类异常直接抛出（宁可整链中止也不静默通过）。② **W605 修复**：_rule_upper 的 docstring 内反斜杠 d 未转义 ⇒ ruff W605 ⇒ 改 raw string ⇒ scripts 全量 ruff 由 10 错转 0（CI 的 Code Quality job 由红转绿）。③ **跨克隆占号机制根修**：批次号预约表写在仓内 tmpe（.gitignore ⇒ 随仓不随 git）⇒ 跨 worktree 与跨克隆并行时互不可见 ⇒ **2026-11-04 实测双方各占 W1120**（各打印 W1120·零红灯·未设 WB_SESSION 时 session 回落 hostname 致两条记录同名不可仲裁）⇒ 根修 = 取号集合改为「本仓表 + 同机兄弟克隆表 + 用户级共享表」三源合并取并集（同名取 ts 最新·写共享表前先合并他人记录不覆盖）+ session 标识含仓路径指纹 + 同号多会话即打印跨克隆撞号预警 + release 只撤本工作树登记且 session 相同的号 ⇒ **实测取号由 W1120 正确让至 W1121**。④ **台账列定位根修**：ledger_backfill 按「从右起固定偏移」定位且状态修正循环左边界写死为 5 ⇒ 对多一列 files 的 10 格行整体错位一格（status 会写进认领会话列·hash 写进级联列）⇒ 改以**状态格内容**为锚点定位（9 格与 10 格皆成立·锚点缺失即 fail-closed·判据强度不降）。⑤ **台账回填**：W1118 与 W1119 两行用 git 反填真正回填（W1119 批主题与 T70 报告虽声称已回填·实际该行仍在途——本批订正该假收敛）。⑥ **经验同步**：坑表 E-160（互斥机制的共享面必须覆盖实际并行作用域·否则是假互斥）+ E-161（宽 except 吞缺陷 ⇒ 新增保护逻辑在异常路径上等于没有）+ E-159 补注（同族复发·写说明文字时描述正则须用 raw string）+ 计数链 12 处同步（256 → 258）+ AGENTS 新增铁律 23（异常分类必须与失败语义对齐）与占号共享区纪律段改写。

**文件**：
- .github/workflows/README.md- CHANGELOG.md- CITATION.cff- HANDOVER.md- README.md- STRUCTURE.md- .agent/skills/puti-shouye/SKILL.md- AGENTS.md- archive/docs/CHANGELOG-ARCHIVE.md- archive/docs/file-index-ARCHIVE.md- archive/docs/W批次编号对账表-ARCHIVE.md- docs/00-导读/W批次编号对账表.md- docs/00-导读/项目说明.md- docs/11-方案报告/README.md- docs/11-方案报告/计划方案/T71-任务计划执行与经验沉淀报告-2026-11-04.md- docs/agent/pitfalls.md- docs/INDEX.md- scripts/INDEX.md- scripts/batch_closeout.py- scripts/check_registration_surface.py- scripts/ledger_backfill.py- scripts/reserve_w.py- scripts/output/INDEX.md- scripts/output/README.md- scripts/output/_w1121_spec.json- scripts/output/file-index.md- scripts/output/stats-changelog.json- scripts/output/stats-index.md- scripts/output/stats.json- scripts/output/tools-inventory.md- scripts/output/_cascade_files_W1121.txt- scripts/output/_vermilion_solid_cache.json- site/data/search.html- site/en/search.html- tests/unit/INDEX.md- tests/unit/README.md- tests/unit/test_w1121_reserve_w.py- archive/docs/AGENTS-ARCHIVE.md- docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md- pytest.ini- site/data/cross-time-danmaku.html- site/data/tag-cloud.html- site/dukou-engine.html- site/index.html

**认领登记 W1121**（占号 session=mvs_1d2745db779a427db4fb4a15ef5d2f7e·跨克隆可见性根修后取得·preflight touches 交集检查通过·与并行会话 W1120 声明面零交集·对方已书面确认不碰本批涉及的 batch_closeout 与 check_registration_surface）。

**验证**：收官链 12 步全绿（含腾窗步·regsurface OK·CSP 856 页 0 漂移）· 门禁 62 段 0 FAIL（CI 同档 full）· 全量 pytest 通过 · ruff check scripts/ 0 违规 · 新增单测 4 例（跨克隆合并·撞号检出·session 可辨·release 不误删）。

### W1120（2026-11-04）：幂等段重建独立入口 + 体积第二阈值接入 + T68 事实订正

**本批要点**（幂等段重建独立入口 + 体积第二阈值接入 + T68 事实订正 + 台账回填·不新增门禁槽 ⇒ 门禁 62 段不变·坑表 256 条不变 ⇒ 不占任何 E-NN）：

① **幂等段重建独立入口**（scripts/rebuild_section.py）：段体一律由 spec 经 backfill_changelog 的块生成函数产出（单一事实源·只引用不复制）· 只动本批段（历史段逐段比对断言·违者零落盘）· 内容一致即零变化（二次执行零 diff）· 两面同 W 号下界对齐检查（不对齐即拒）· 行尾按原文件主导行尾归一写回· **不接收官链主链**（收官链属对方 W1119 批已动面 ⇒ 本批不双改·零同文件冲突）。

② **体积第二阈值接入**（check_doc_size_budget.py 新增 C8 判据）：段数窗口只管条数管不住单条超长（实测段面曾达 390.8KB / 109 段·段数在窗内而体积已超 256KiB 约 1.5 倍）⇒ 正本窗口改为**双阈值先到者为准**：段数 ≤ 110 且体积字节 ≤ 262144（台账为数据行 ≤ 60 且字节 ≤ 262144）· 字节上限**只引用** batch_closeout 顶层 MAX_DOC_BYTES（不复制·不新建中立模块⇒持有方零改动·省一组 CI）· 台账行窗口同源引用 LEDGER_WINDOW · 同源引用失败即 fail-closed 判红（体积判据不可执行不得静默放行）。

③ **结构档等价拆分**（check_doc_size_budget.collect）：本批改动该文件后 ruff 宽档结构阈值即扫到其既有复杂度超标（复杂度 21 > 15 / 分支 22 > 16）⇒ 按仓内先例（W1114 结构档根因拆分）把 HANDOVER 与 AGENTS 两面判据与 C7 版本行锚尾检查抽为三个私有函数·**判据与文案逐字不变**（既有 12 例单测全绿即等价性证据）。

④ **T68 事实订正**（新增 §2.4·不改 §6.1 本体）：W1117 登记的 R-05（_w1115_spec.json 含裸控制字符致 JSON 不可解析）在当前基线**不复现**（末次改动 b5b64423·json.load 正常）⇒ 撤回修复动作·保留 W1117 已落地的防御性容错·现状为准结案。

⑤ **台账回填与腾窗**：W1118 行与 W1119 行状态与 hash 列仍为待回填（git 反填算出新指纹 403fcdf6953b 与 572a98b2d681·其中 403fcdf6953b 与对方 W1119 批声称的 verify 值一致）⇒ 本批并入回填（省一次 PR）· 台账腾窗迁 W1059 行（正本 60 数据行 = 窗口 60）。

⑥ **自证 10 例**（字节阈值 5 + 重建 5：边界 / 缺件 fail-closed / 双阈值独立 / 现网在窗 / 降序位插入 / 幂等 / 只动本批段 / 篡改可检出 / 下界失配可检出）。

**文件**：
-.github/workflows/README.md
-AGENTS.md
-CHANGELOG.md
-CITATION.cff
-HANDOVER.md
-README.md
-STRUCTURE.md
-archive/docs/AGENTS-ARCHIVE.md
-archive/docs/W批次编号对账表-ARCHIVE.md
-docs/00-导读/W批次编号对账表.md
-docs/00-导读/文档规范.md
-docs/00-导读/项目说明.md
-docs/11-方案报告/README.md
-docs/11-方案报告/计划方案/T68-任务计划执行与经验沉淀报告-2026-11-04.md
-docs/11-方案报告/计划方案/T72-任务计划执行与经验沉淀报告-2026-11-04.md
-docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md
-docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md
-docs/INDEX.md
-pytest.ini
-scripts/INDEX.md
-scripts/batch_cascade.py
-scripts/check_doc_size_budget.py
-scripts/output/INDEX.md
-scripts/output/README.md
-scripts/output/_cascade_files_W1120.txt
-scripts/output/_vermilion_solid_cache.json
-scripts/output/_w1120_spec.json
-scripts/output/file-index.md
-scripts/output/stats-changelog.json
-scripts/output/stats-index.md
-scripts/output/stats.json
-scripts/output/tools-inventory.md
-scripts/rebuild_section.py
-site/data/cross-time-danmaku.html
-site/data/search.html
-site/data/tag-cloud.html
-site/dukou-engine.html
-site/en/search.html
-site/index.html
-tests/unit/INDEX.md
-tests/unit/README.md
-tests/unit/test_w1120_cascade_file_index_idempotence.py
-tests/unit/test_w1120_size_threshold_and_rebuild.py
-.agent/skills/puti-shouye/SKILL.md
-docs/11-方案报告/计划方案/T71-任务计划执行与经验沉淀报告-2026-11-04.md
-docs/agent/pitfalls.md
-scripts/batch_closeout.py
-scripts/check_registration_surface.py
-scripts/ledger_backfill.py
-scripts/output/_cascade_files_W1121.txt
-scripts/output/_w1121_spec.json
-scripts/reserve_w.py
-tests/unit/test_w1121_reserve_w.py

**认领登记 W1120**（主仓共享区占号 session=session_237a5e53-…·preflight touches 交集检查通过·与对方 W1119 零同文件冲突）。

**验证**：全量 pytest 1241 passed / 3 skipped / 0 failed · 新增自证 10 例 + 既有 12 例全绿 · 体积门禁字节双阈值三面 0 FAIL · 门禁 62 段 0 FAIL（CI 同档 full）。

### W1119（2026-11-04）：CI 成本治理 + 档 3 第二批 + 归档规则工具化

**本批要点**（CI 成本治理 + 档 3 第二批 + 归档规则工具化·不新增门禁槽 ⇒ 门禁 62 段不变·坑表 242 → 256 条）：① **档 3 第二批施工**（relationships / narrative-experiment / jurisprudence 中英各一对）：实测三对页的图色主体走 D3 .attr() 与 canvas（SVG presentation attribute 与 Canvas fillStyle 均不支持 var()）且带 e-track-exempt chart-data-colors 门禁豁免登记 ⇒ 只改安全位（style 属性 + CSS 声明）共 40 行；首轮替换误改 6 处暗色补偿规则的选择器 LHS ⇒ 已按 HEAD 原文逐行复原（残留越界选择器行 = 0·补偿表与指纹零改动）。② **盘点结论**：全站剩余调色板色 1320 处 / 139 页（W1113 三对已归零）；排除 181 页带 chart-data-colors 豁免登记的页后，可安全令牌化面 **每页 <= 2 处** ⇒ 档 3 可施工对象已近耗尽，后续需先改消费方式（属独立工具批）。③ **归档规则工具化**：archive_segments 增 --max-bytes / --chunk 与两面同 W 号下界对齐 + 迁完断言；A3 编号规则行断言由全文计数收紧为留存前缀内计数（批量迁移下原口径恒假红）；batch_closeout 增腾窗步并**置于 precheck 之前**（precheck fail-closed ⇒ 腾窗排其后即死路径）；顺序锁单测同步（test_w1102 新增 archive 步断言·test_w1114 首步断言改为 archive 并留痕）。④ **两面腾窗**：CHANGELOG 与 file-index 各迁出 W996 段（留存 109）+ 台账迁出 W1058 行 + W1119 认领行 ⇒ 台账 60/60；CHANGELOG 段位由 109 段（390.8KB）经体积模式降至 60 段（<= 256KiB）；⑤ **经验同步**：坑表 E-159（反斜杠字面量须转义）+ E-146 补注（--force-with-lease 例外）+ 计数链 12 处同步（255 → 256）+ CHANGELOG 孤立 CR 归一。

**文件**：
- .github/workflows/README.md- CHANGELOG.md- CITATION.cff- HANDOVER.md- README.md- STRUCTURE.md- .agent/skills/puti-shouye/SKILL.md- AGENTS.md- .github/workflows/perf.yml- .github/workflows/screenshot-review.yml- archive/docs/CHANGELOG-ARCHIVE.md- archive/docs/file-index-ARCHIVE.md- archive/docs/W批次编号对账表-ARCHIVE.md- docs/00-导读/W批次编号对账表.md- docs/00-导读/项目说明.md- docs/11-方案报告/README.md- docs/11-方案报告/计划方案/T70-任务计划执行与经验沉淀报告-2026-11-04.md- docs/agent/pitfalls.md- docs/INDEX.md- scripts/INDEX.md- scripts/archive_segments.py- scripts/batch_closeout.py- scripts/output/INDEX.md- scripts/output/README.md- scripts/output/_w1118_spec.json- scripts/output/file-index.md- scripts/output/stats-changelog.json- scripts/output/stats-index.md- scripts/output/stats.json- scripts/output/tools-inventory.md- scripts/output/_cascade_files_W1118.txt- site/data/relationships.html- site/en/relationships.html- site/data/narrative-experiment.html- site/en/narrative-experiment.html- site/data/jurisprudence.html- site/en/jurisprudence.html- tests/unit/test_w1102_batch_closeout.py- tests/unit/test_w1114_version_surface.py

**认领登记 W1119**（主仓共享区占号 session=mvs_1d2745db…·preflight touches 交集检查通过·8 项与在途声明方零交集）。

**验证**：收官链 11 步全绿（含腾窗步·regsurface OK·CSP 856 页 0 漂移）· 门禁 62 段 0 FAIL（CI 同档 full）· 全量 pytest 1228 passed / 4 skipped。

### W1118（2026-11-04）：CI 成本治理与经验同步入仓

**本批要点**（CI 成本治理 + 经验同步入仓·不新增门禁槽 ⇒ 门禁 62 段不变）：① **归因实测**：最近 60 个 run 的 run 级墙钟 418.1 分钟，我方 37 run / 330.7 分钟 = 79.1%，对方 23 run / 87.5 分钟 = 20.9%；PR 数 14:6。② **根修一**：暗色态门禁的跳过判定此前只挂 push 事件 ⇒ PR 事件下无任何跳过路径 ⇒ 每次命中 site/** 即跑全站约 163 页 × 4 分片，是本仓最大成本单点 ⇒ 判定扩展到 pull_request，且 schedule 与 workflow_dispatch 恒为全量。③ **根修二**：Lighthouse CI 只采集 5 个页面，未触及这 5 页即跳过采集。④ 搜索索引数据页 site/data/search.html 与 site/en/search.html 进非渲染面免审名单，其布局仍由主截图 job 的定向截图与每周定时全量审查覆盖。⑤ **经验同步入仓**：Agent Memory 内 W1114~W1118 的 13 条教训落坑表 E-141 ~ E-153，坑表 242 → 255 条。⑥ **节奏收紧**：一批一 PR 一 push，收官链产物必须在提交前生成完毕。

**文件**：
- .github/workflows/screenshot-review.yml：暗色态门禁跳过判定补 PR 事件 + 非渲染面免审名单 + merge job 跳过联动
- .github/workflows/perf.yml：Lighthouse CI 采集页未变即跳过采集 + Checkout 加 fetch-depth 0
- docs/agent/pitfalls.md：新增 E-141 ~ E-153 共 13 条跨项目通用教训
- AGENTS.md：坑表总数与六主题分项声明同步 + 纪律增行
- HANDOVER.md 与 .agent/skills/puti-shouye/SKILL.md：坑表条数指针同步
- docs/00-导读/W批次编号对账表.md：W1118 认领登记行
- docs/11-方案报告/计划方案/T69-任务计划执行与经验沉淀报告-2026-11-04.md：本批交付报告
- docs/11-方案报告/README.md：第六节第 84 号登记

**认领登记 W1118**（主仓共享区占号 session=mvs_1d2745db…·preflight touches 交集检查通过）。

**验证**：门禁 62 段 0 FAIL · 坑表 255 条 0 重号 · 两个 workflow YAML 解析通过 · 台账正本数据行不超过窗口 60。

### W1117（2026-11-04）：版本面幂等修复与编号规则并入版本面（修描述含分号时二次推进失配）
> **来源**：并行会话 W1113 批独立复核实测（2026-11-04）——我方 W1114 批的版本面推进器**在批次描述含分号时，二次推进会 fail-closed**（非幂等）⇒ 我方 W1114 报告与 CHANGELOG 段中「六个文件全『已是目标态』」的表述在该形态下不成立 ⇒ 本批根修并订正该表述。
> - **文件**：`scripts/version_surface.py` · `scripts/batch_cascade.py` · `scripts/batch_closeout.py` · `scripts/backfill_changelog.py` · `tests/unit/test_w1117_version_surface_idempotence.py` · `tests/unit/test_w1102_batch_closeout.py` · `scripts/output/_w1117_spec.json` · `docs/11-方案报告/计划方案/T68-任务计划执行与经验沉淀报告-2026-11-04.md` · `docs/11-方案报告/计划方案/T65-任务计划执行与经验沉淀报告-2026-11-03.md` · `docs/11-方案报告/README.md` · `docs/00-导读/W批次编号对账表.md` · `CHANGELOG.md` · `scripts/output/file-index.md` · `archive/docs/CHANGELOG-ARCHIVE.md` · `archive/docs/file-index-ARCHIVE.md`

**本批要点**（工具层·零页面内容逻辑改动·不新增条目 => 计数链条数不变）：

① **根修版本面推进的二次失配**：交接文档「一、当前进度」标题与「当前 HEAD」句的描述匹配段原为 `[^；]*`（隐含假设描述不含分号）⇒ 描述一旦含分号，第一次推进后文本出现两个分号，第二次推进即正则失配而 fail-closed ⇒ 非幂等。⇒ 改为 `[^

）]*`（行内·容许分号·不跨行·遇右括号止）⇒ 二次推进零变化。

② **尾部锚点唯一性断言**：描述若含右括号会使正则提前闭合 ⇒ 断言尾部锚点各恰一处，否则 **fail-closed**（明确报错·不静默产出坏文本）⇒ 该面从「静默失效」改为「显式失效」。

③ **批次级单调守卫（低号批不回退现役面）**：版本面表达的是「**现在是什么**」⇒ 只能指向**最高号**批次。落段批号与合并次序可以不一致（并行会话乱序合并：对方 W1118 先合入 main，我方 W1117 后落段）⇒ 原语义会把 README / STRUCTURE / 项目说明 / CITATION / workflows README / HANDOVER / 编号规则段**全部回退**到低号，抹掉已合并批次的现役标记（且与 `backfill_changelog.py` 明文的「当前态六面该指向最高号」相悖）⇒ 推进器改为**单调**：目标批号 ≤ 该文件现役批号 ⇒ 该文件零变化（不回退·不 fail-closed）；编号规则段上限同步改为只升不降（与 `backfill_changelog.py` 同名规则一致）。

④ **CHANGELOG 编号规则段上限并入版本面**：原由级联在插段时一并改写（与段插入耦合·属非幂等面）⇒ 本批划为**版本面字面量**（新增 `advance_changelog_rule` 并入 POINTS），级联改为**调用同一实现**（单一事实源·只引用不复制·幂等）⇒ 今后随版本面自动推进，**不再需要手工 bump**。口径区分留痕：**历史段本体不改**（只订正新增/修改段）vs **编号规则段属现役面可推进**。

⑤ **收官链 index 步移到 versions 之后**：版本面推进会改 README / STRUCTURE / 项目说明等 docs 条目 ⇒ 索引若早于推进则内嵌索引陈旧（第 46 槽判红）⇒ 步序改为 precheck → selfref → add → refresh → stats → versions → index → docnums → regsurface → csp → cspcheck（csp / cspcheck 恒为末两步）。

⑥ **落段方式改用仓内既有工具**：本批号低于已合入 main 的 W1118 ⇒ 按 `backfill_changelog.py` 的既定语义「段按批号降序排列·新段插在第一个号小于自己的段之前·当前态六面只指向最高号」，本段落在 **W1118 段之下、W1116 段之上**（降序位），编号规则段上限只升不降（保持 W001-W1118）；两面先各腾窗一段（正本 110 → 109）再插段，落段后正本与索引各 110 段（窗口 110）。

⑦ **补段工具的完整性检查顺序根修**：补段工具原在判断「该号是否已立段」**之前**对**每一个** spec 做字段完整性检查 ⇒ 任何一个**已立段**的老 spec（实测 `_w1077_spec.json` 缺 `changelog_body` / `milestone_block` / `agents_note`）都会把补段流程整个阻断（本批实测 AssertionError）⇒ 检查移到「未立段」判定之后（完整性只对**待补段**有意义·待补段缺字段仍 fail-closed·判据强度不降）。

⑧ **二次幂等自证与单调守卫自证**：本批单测共 9 例（幂等自证 5 例：描述含分号 / 含右括号 / 两者皆含 / 编号规则 bump 幂等 / 逐文件逐点二次零变化；单调守卫 4 例：现役批号提取 / 低号批不回退 / 高号批正常推进不误伤 / 编号规则只升不降）⇒ 全量 pytest **1228 passed / 3 skipped / 0 failed**（本地工地的历史一次性探针已按治理处置移出仓外·此前本地恒 2 failed 的污染源已清零）· 双档 ruff 全绿。

⑨ **对 W1114 表述的订正**：W1114 段与 T65 报告称「六个文件全『已是目标态』」，该读数在描述**不含**分号时成立（实测），在**含**分号时因上述缺陷不成立 ⇒ 本段与 T65 §2.6 的相应表述一并订正为**按描述形态分述**（W1114 段本体不改·历史段禁改·以本段留痕）。

⑩ **提交范围门禁的归属判定扩展（乱序落段）**：第 51 门禁（提交范围）原判据只认「索引态 CHANGELOG `**顶段**`」⇒ 隐含假设「新增批必是顶段」。低号批在更高号批之后落段（对方 W1118 先合入 main，我方 W1117 后落段）⇒ 本提交新增的段**不在顶位** ⇒ 归属错落到 W1118 ⇒ 拿他批 spec 当应动全集 ⇒ 假红「索引含本批 spec 之外的文件」。⇒ 归属判定扩展为「索引态相对 HEAD 的新增段集合；恰有 1 个新增段 ⇒ 归属它（无论是否顶位）」，多个或无新增段时沿用原判据（顶段优先·回填取 HEAD）⇒ **判据强度不降**（仍要求索引态路径集 ⊆ 归属批 spec 的应动全集），并在单测中**追加**一例（不改他人既有断言）。

**验证**：门禁 62 段 0 FAIL · 全量 pytest 1228 passed / 3 skipped · CSP 856 页零漂移 · CHANGELOG 与 file-index 正本各 110 段（窗口 110）· 台账正本 60 数据行（窗口 60）· 坑表不新增条目。

### W1116（2026-11-04）：收官链自检闸（文案数字对表 + 登记面一致性）

> **来源**：跨批复盘（W1105~W1117）共识 P0-1 / P0-2 · 用户 2026-11-04 批准。
> - **文件**：scripts/check_doc_numbers.py · scripts/check_registration_surface.py · scripts/batch_closeout.py · tests/unit/test_w1116_selfcheck_gates.py · tests/unit/test_w1114_version_surface.py · pytest.ini · docs/11-方案报告/计划方案/T67-任务计划执行与经验沉淀报告-2026-11-04.md · docs/11-方案报告/README.md · docs/00-导读/W批次编号对账表.md · scripts/output/_w1116_spec.json

**本批要点**（工具层·**零页面内容改动**·**不新增门禁槽 ⇒ 门禁 62 段不变**·**不新增坑表条目 ⇒ 坑表 242 条不变**）：

① **P0-1 文案数字 ↔ 证据件对表闸**（scripts/check_doc_numbers.py）：把「收官读数须与最终落盘产物对表」从人工核对变成机器断言 —— 每批在 spec 的 doc_numbers 段声明「哪处文案 ↔ 哪个证据键」，收官链末位逐项断言（source 支持 json 键 / git numstat 单 ref 与 A..B 双 ref / count 正则 / literal；pattern 用具名捕获组 v）；另加 **coverage 类**（对一组目标逐项断言「N 个文件全 X」这类枚举声明·采纳并行会话 W1117 建议）。

② **P0-2 登记面一致性闸**（scripts/check_registration_surface.py）：六项 —— 台账本批认领行存在 · HANDOVER 最后更新链首 == CHANGELOG 现役段 · CHANGELOG 编号规则段上限 == 现役段 · HANDOVER 最后更新链条目 ≤3 · file-index 含本批段 · 台账正本数据行 ≤ 窗口（行口径**复用 scripts/archive_ledger_rows.py 的 ROW_RE**·唯一事实源·不另写正则）。

③ **接入收官链末位**：STEPS 增 docnums + regsurface（versions 之后 · csp/cspcheck 之前 ⇒ **W1112 既有「csp 末两步」承诺不破**）；判据缺失即 fail-closed 中止；未声明 doc_numbers 的批次跳过（不伪造红·不阻塞在途批）。

④ **闸自跑即抓出自身三处缺陷（价值实证）**：把新闸指向本批自身（spec 声明 → 闸实跑）⇒ 首跑红三条 —— ① count 源用行首锚点却未加 re.MULTILINE ⇒ **取到假零 0**（与 W1113「假零」同族）② pattern 写 **62 段** 而正文实为 **62 段 0 FAIL** ⇒ 尾部闭合不匹配且缺捕获组 ⇒ 报「未匹配到任何位置」③ 新增单测实为 **17 例**（非 14）⇒ 报告与 pytest 标记同步订正 ⇒ 复跑全绿（对表闸 4 项全一致）。

⑤ **共享面连带同步**：改 STEPS 破坏并行会话 W1114 的顺序锁单测（断言 versions 与 csp 紧邻）⇒ 已同步该断言（放宽为 versions 在 stats 之后 · csp 之前 + 加两闸位置断言·比原断言更强）· 全量 pytest 复跑 0 failed。

⑤b **跨批留痕（改的是哪一批的哪个断言 · 放宽理由 · 新的更强表述原文）**：本批改动了 **W1114 批落盘的 `tests/unit/test_w1114_version_surface.py::test_closeout_steps_put_versions_between_stats_and_csp`**（原断言「versions 紧邻 csp」）。**放宽理由**：本批两道闸必须读**版本面推进后的最终产物面**（versions 之后才成立）⇒ 原断言在新链序下必然不成立，故把「紧邻」放宽为「versions 在 stats 之后 · csp 之前」。**新的更强表述原文**：`assert order.index('versions') == order.index('stats') + 1` · `assert order.index('versions') < order.index('csp')` · `assert order[-2:] == ['csp', 'cspcheck']` · `assert 'docnums' in order and 'regsurface' in order` · `assert order.index('versions') < order.index('docnums') < order.index('csp')` ⇒ 替代表述**多断言了两闸的相对位置**（比原断言更强）。**对方 W1114 批已书面确认接受该放宽**（回执七十八），其 W1117 批报告将引用本表述以免两批文档各说一套。

**验证**：门禁 62 段 0 FAIL · 单测 1217 passed / 4 skipped / 0 failed（新增 17 例含 10 个负样本）· ruff 双档全绿 · CSP 856 页 / 909 内联哈希 / 0 漂移 · 台账正本 58 数据行（窗口 60）· 坑表 242 条不变（不占 E-NN）· 本批自身过自己的两道闸。

### W1115（2026-11-03）：图表色工程批收官订正批（承接独立盲审 F1~F8 · 纯文档 · 零页面内容改动）

> **来源**：并行会话对 W1113 的独立盲审最终报告（判 FAIL：订正数值全部正确，但报告内仍有 5 处同类旧数未订正 + 「同口径」措辞口径混用）。
> - **文件**：docs/11-方案报告/计划方案/T64-任务计划执行与经验沉淀报告-2026-11-03.md · docs/11-方案报告/计划方案/T66-任务计划执行与经验沉淀报告-2026-11-03.md · docs/00-导读/W批次编号对账表.md · archive/docs/W批次编号对账表-ARCHIVE.md · docs/11-方案报告/README.md · HANDOVER.md · README.md · STRUCTURE.md · CITATION.cff · .github/workflows/README.md · docs/00-导读/项目说明.md · scripts/output/_w1115_spec.json（版本面推进与索引生成物另见 spec 应动全集）

**本批要点**（**零人工页面内容改动**（仅 site/data/search.html 与 site/en/search.html 的内嵌搜索索引由搜索索引生成器同步）·**不新增坑表条目 ⇒ 计数链条数不变**）：

① **承接盲审 F1（口径混用·阻断·已由 #119 落地）**：盲审指出「56 → 0」前后两数非同一口径（56 = W1100 旧口径基线·引号必需；0 = 本批修正引号盲区后的新口径复算）⇒ 我方以权威脚本自身层正则逻辑独立复算确认成立：**旧口径基线 56 → 0** 与 **新口径基线 64 → 0** 两条都成立（两口径下当前态均为 0）⇒ 据此在 CHANGELOG / 台账 / HANDOVER / T64 / 坑表 E-138 共 10 处补口径注（该笔为 #119，已合并入 main）。

② **承接盲审 F2~F8（本批）**：T64 报告内 5 处同类旧数未订正 —— AC-01 仍写「10 → 0」⇒ 56 → 0 · AC-02 仍写「542 条差异」⇒ 552 · V 表坑表条数 241 ⇒ 242 · ST 表「E-133~E-136」⇒ E-133~E-140 · §3.2「各页 18~24 行 + 坑表 7 条」⇒ 新增口径 12~14 行 + 8 条；另订正附录 A 的「2350 类读数」（不可复现 ⇒ 删具体数保留定性）与「同口径复算」措辞（⇒「分别标注口径」）⇒ **报告的验收表、V 表、ST 表与正文不再自相矛盾**。

③ **台账登记面补齐**：用仓内 `scripts/ledger_backfill.py --w 1113 --cascade "W1113（2026-11-03）"` 回填 W1113 行的 CHANGELOG 版段列（—（待回填）→ W1113（2026-11-03）·行指纹 290ef506621f → 14275162d6b7）· 状态格补记后续订正 3 笔（#116/#117/#119）· 台账腾窗迁出 2 行（W1054-W1055·正本 58 数据行 ≤ 窗口 60）。

④ **第 51 槽归属说明（本批为何新立批次号而非并入他批）**：提交范围门禁按**索引态 CHANGELOG 顶段**定归属批次 ⇒ 补订他批交付物时归属必落现役批（W1114）⇒ 他批 spec 不含该文件 ⇒ 判红 ⇒ 正解是**新增批次段**（归属随索引顶段切到本批）+ 本批 spec 登记应动全集 ⇒ 顺带暴露该门禁「补他批交付物」场景的固有局限（登记去向）。

**验证**：门禁 62 段 0 FAIL · 单测 1198 passed / 4 skipped · CSP 856 页 / 909 哈希 / 0 漂移 · 台账正本 58 数据行（窗口 60）· 坑表 242 条不变（不占 E-NN）· 行指纹复核 `ledger_backfill.py --w 1113 --verify 14275162d6b7`。

### W1114（2026-11-03）：落段收官链加版本面幂等推进步（并根修收官脚本两处工具缺陷）


> **来源**：并行会话 W1113 批 rebase 实测（2026-11-03）——版本面是**跨文件字面量同步面**，rebase 只解内容冲突、不自动同步现役批次号字面量；且级联工具把「版本面字面量」与「CHANGELOG/file-index 段插入」耦合在同一条**非幂等**命令里，落段后想单独同步版本面无路可走。
> - **文件**：scripts/version_surface.py · scripts/batch_cascade.py · scripts/batch_closeout.py · tests/unit/test_w1114_version_surface.py · tests/unit/test_w1102_batch_closeout.py · scripts/output/_w1114_spec.json · docs/11-方案报告/计划方案/T65-任务计划执行与经验沉淀报告-2026-11-03.md · docs/00-导读/W批次编号对账表.md · CHANGELOG.md

**本批要点**（工具层·零页面内容逻辑改动·不新增条目 => 计数链条数不变）：

① 新增 **scripts/version_surface.py**（版本面幂等推进器）：只做**跨文件字面量**的现役批次号推进（README 抬头 / STRUCTURE 头部 / 项目说明头部与列表行 / CITATION.cff / workflows README 区间 / 交接文档当前进度标题与当前 HEAD 句）⇒ **已是目标态则不动**（幂等·可重复跑）⇒ 与「段插入」彻底解耦。

② 级联工具的版本面改为**调用同一共享模块**（只引用不复制·避免两份实现漂移）。（**勘误**：本段初稿曾写「修掉交接文档当前 HEAD 句缺失导致级联整链 assert 失败」——该判断为**误判**：W1114 批复核时以级联 dry-run 实测通过（10 面全过）证伪，真相是该句藏在 HANDOVER 超长段落末尾、被打印截断吃掉；详见 T63 §2.2 B-01。）

③ 收官脚本加**版本面推进**步（插在 stats 之后、csp 之前 ⇒ **csp/cspcheck 仍为末两步**·既有承诺不破）并补 **add 收尾**（末位生成器产物必须再暂存一次）。

④ 单测锁定（**12 例**）：版本面幂等性（重复执行零变化）·各字面量点逐一推进 · fail-closed 负样本 · 收官链 STEPS 顺序 · add 收尾 · precheck 行数口径负样本。⑤ **根修收官脚本两处工具缺陷**：(a) **add 步静默失效**——pathspec 含尚不存在的路径时 git add 整体放弃（不做部分暂存）而脚本仍打印「已 add N 件」⇒ 改为过滤 + 如实报告跳过数 + 检查退出码并中止；(b) **precheck 行数口径 off-by-one**——原用 startswith(| W) 计数，台账**表头行**同形被计入 ⇒ 读数恒多 1 ⇒ 窗口 60（数据行 ≤ 60）被误判超窗 ⇒ 收官工具在本仓恒判超窗、实际不可用 ⇒ 改为复用 scripts/archive_ledger_rows.py 的 ROW_RE（单一事实源）并补负样本（数据行 60 PASS / 61 FAIL / 表头不计入）。⑥ 台账按数据行口径腾窗与迁回：正本 **60 数据行**（窗口 60·表头不计）。

⑦ **对 W1112 段的订正留痕**：W1112 段把「precheck 拦下『台账正本 61 行超过窗口 60』」记为正面案例，W1114 批复核发现该拦下是**口径缺陷导致的假阳**——precheck 原用 startswith(| W) 逐行计数，而台账**表头行**同样以「| W」开头 ⇒ 读数恒比真实**数据行**多 1；窗口 60 的真实语义是「数据行 ≤ 60」（唯一事实源：scripts/archive_ledger_rows.py 的 ROW_RE，--keep 默认 59 = 窗口 60 − 当批认领 1）⇒ 该收官工具在本仓恒判超窗、实际不可用。⇒ W1114 已改为复用 ROW_RE（单一事实源·不另写正则）并补负样本单测（数据行 60 PASS / 61 FAIL / 表头行不计入）。W1112 段原文不改（历史段禁改）⇒ 订正以本段留痕。

**验证**：门禁 62 段 0 FAIL · 单测 12 例全绿（本批文件）· 版本面真机幂等自证（6 点「已是目标态」）· CSP 856 页 / 909 哈希 / 0 漂移 · 台账正本 60 数据行（窗口 60·数据行口径·表头不计）。

### W1113（2026-11-03）：图表色工程档 3 铺开第一批（3 对 6 页·chart 色常量令牌化）

> **来源**：用户 2026-11-03 指令「那继续」（承接 W1110 档 3 施工前置批）。
> - **文件**：site/data/character-sentiment-arc.html · site/en/character-sentiment-arc.html · site/data/concept-device.html · site/en/concept-device.html · site/data/monster-victims-network.html · site/en/monster-victims-network.html · docs/agent/pitfalls.md · docs/11-方案报告/计划方案/T64-任务计划执行与经验沉淀报告-2026-11-03.md · scripts/output/_w1113_spec.json · scripts/output/_w1113_delta.json

**本批要点**（档 3 铺开第一批·**6 页·78 行**）：

① **范围**：3 对 6 页（character-sentiment-arc · concept-device · monster-victims-network，中英同批），施工面 = 图表色常量改读 `var(--chart-N)`；档 3 权威口径（`archive/scripts/batches/w1100/_w1100_layer3_pages.py`·互斥归类 L2/L4/L5）复算本批 6 页残留归零（**旧口径基线 56 处 → 0 处**；引号盲区修正后的**新口径基线 64 处**（差 8 处 = arc 页 L4 无引号内联色 4 处 × 中英）⇒ **两口径下当前态均为 0** ⇒ 归零结论不受口径影响）。

② **本批最大产出＝施工期越界动作的自我纠正（补偿机制）**：施工初稿曾按 W1108 先例把每页的字面值型补偿规则 LHS 由 `#xxx` 改写为 `var(--chart-N)`，并新增 `[fill^="var("]` 前缀规则。二者均**越界**：W1100 台账「工程次序定案」明确「**补偿收口排在档 3 之后**（补偿表含调色板色条目且当前仍生效，先删会让 1412 处暗色变暗）」，且站内补偿表是**每页 112 条同源指纹**（330 页逐页条数一致·其中 328 页共享同一指纹、chart-design 中英 2 页为 W1108 原型批遗留的另一种指纹·规则条数同为 112），改 LHS 即破指纹。DOM 级取证（规则命中面对拍）实测该越界造成两类真实缺陷：① 新增前缀规则命中了**基线中早已是 `var()`** 的元素（它们在基线本就不吃亮度补偿）⇒ 凭空多出 22 处 filter；② 改写 LHS 后仍有字面值元素失配 ⇒ 9 处补偿值互换（其中 8 处为**暗色态变暗**回归）。**处置**：撤销两条越界改动，补偿机制原样保留（与 W1100 定案一致），6 页各 1 条前缀规则删除 + 1 条字面值规则还原。

③ **补齐 10 处施工缺口**（权威口径复算所得）：arc 页 pairs 常量（对象字面量 `color:` 形式，被首版脚本的行首锚定正则排除）· concept-device 页渐变 `stop-color` 两处 · monster 页 `catColors` 数组字面量两处。

④ **呈现色等效核档**（J2 双态对拍·**浅色零差异 + 元素零损失**）：暗色态 552 条差异（按属性 fill 226 / filter 212 / stroke 44 / background-color 46 / 其余 24），逐颜色属性按「computed 颜色叠加 CSS filter（brightness 后 saturate·drop-shadow 不改主体色）」实算呈现色后分档：**OK 166 / WARN 122 / BLOCK 52**，方向变亮 268 / 变暗 72，**改后取暗色令牌值 340/340**。BLOCK 52 条全部为「改前裸浅色 → 改后暗色令牌」的**令牌口径差**（`--chart-2` / `--chart-4` 暗色令牌值本身与其「浅色值×站内补偿等效值」的差），与站内既有口径对照读数一致（`--chart-2` dL 18.83 / `--chart-6` dL 17.34 BLOCK 是 W1103 已登记的既有口径差），**非本批引入的回归** ⇒ 登记为补偿收口批的去向，不在本批改补偿机制。

⑤ **防线**：复用 W1110 新增四槽（第 54 坑表编号唯一 / 第 55 PowerShell 解析 / 第 56 CSP 增量漂移 / 第 57 CSS 变量自引用）· CSP 856 页零漂移（909 内联哈希）· 档 3 权威口径复算归零。

**验证**：元素数 12 组零不一致（5512 元素·探针 SCHEMA 6 含 stop-color）· 浅色态 0 差异 · 档 3 残留 **旧口径基线 56 → 0**（引号盲区修正后新口径基线 **64 → 0**·两口径当前态均 0·真归零） · CSP 零漂移 · 第 56/57 槽 0 FAIL · 坑表本体 **234 → 242 条**（本批新增 **E-133 ~ E-140 八条**·E-130~E-132 为 W1110 既有条目）· 计数链同步。

**收官订正**（2026-11-03·PR #117）：本段三处数字经复算订正为与仓内证据件逐字对齐——改动面 60 → **78 行**（`git diff --numstat` site 6 页实测 14+12+13 × 中英）· 残留起点 10 → **56 处**（W1100 基线盘点表逐页读数：arc 中英各 8 · device 中英各 8 · monster 中英各 12；该 56 为**旧口径**（色值须带引号）·引号盲区修正后**新口径**基线 = **64**（差 8 处 = arc 页 L4 无引号内联色 4 处 × 中英）⇒ **两口径下当前态均 = 0**）· 坑表 241 → **242 条 / E-140**（条目实测 242·max E-140）。原值系收官前未复核的旧读数（其中「10 处」为首版脚本漏改的中间态·非权威口径读数）。核档读数（552 条差异 / OK 166·WARN 122·BLOCK 52 / 改后取暗色令牌值 340/340 / 元素数 5512）经 `scripts/output/_w1113_delta.json` 复算一致。

### W1112（2026-11-03）：落段收官一键脚本（八步固定顺序·refresh 迭代收敛·csp 恒末位）


> **来源**：W1109 批 CI 三次红项（第 45 槽 ×2 + CSP 漂移 ×1）的根因方案化。
> - **文件**：.github/workflows/README.md · AGENTS.md · CHANGELOG.md · CITATION.cff · HANDOVER.md · README.md · STRUCTURE.md · archive/docs/AGENTS-ARCHIVE.md · archive/docs/CHANGELOG-ARCHIVE.md · archive/docs/W批次编号对账表-ARCHIVE.md · archive/docs/file-index-ARCHIVE.md · docs/00-导读/W批次编号对账表.md · docs/00-导读/项目说明.md · docs/11-方案报告/README.md · docs/11-方案报告/计划方案/T63-任务计划执行与经验沉淀报告-2026-11-03.md · docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md · docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md · docs/INDEX.md · pytest.ini · scripts/INDEX.md · scripts/batch_closeout.py · scripts/output/INDEX.md · scripts/output/README.md · scripts/output/_cascade_files_W1112.txt · scripts/output/_vermilion_solid_cache.json · scripts/output/_w1106_spec.json · scripts/output/_w1112_spec.json · scripts/output/file-index.md · scripts/output/stats-changelog.json · scripts/output/stats-index.md · scripts/output/stats.json · scripts/output/tools-inventory.md · site/data/cross-time-danmaku.html · site/data/search.html · site/data/tag-cloud.html · site/dukou-engine.html · site/en/search.html · site/index.html · tests/unit/INDEX.md · tests/unit/README.md · tests/unit/test_w1102_batch_closeout.py · tests/unit/test_w1112_judge_fix.py

**本批要点**（工具层·**零页面内容逻辑改动**（级联页脚链 4 页 + 搜索页内嵌索引/CSP 哈希 2 页由生成器改写）·不新增条目 ⇒ 计数链条数不变）：

① 新增 **scripts/batch_closeout.py**（落段收官一键脚本）八步固定顺序：precheck（台账同号多行/行数窗口预检·不通过即中止并给修复指引）=> selfref（CSS 变量自引用体检·**只引用**第 57 槽既有判据不复制实现）=> add（按 spec.rows 显式 pathspec·禁 git add -A）=> refresh（**迭代至索引快照不再变化**·实测第 2 轮才收敛）=> 搜索索引 + 文档索引 => stats => **csp（恒末位·因前面步骤会改内联脚本）** => csp --check（零漂移）。

② **单测全绿**（batch_closeout **10 例** = 7 计划 + 3 收官笔行为锁·判据正向锁 3 例·合计 13 例） + **真实仓跑通取证**：precheck 当场拦下「台账正本 61 行超窗口 60」并给修复指引 · refresh 第 2 轮收敛 · CSP 856 页零漂移。

③ 台账腾窗迁 3 行（W1050-W1052） + 登记 **W1111 空号·让号行**（先例 W1101/W1102）⇒ 段序连续无空洞。

④ **诚实边界**：本批**不改任何门禁脚本与判据**（主会话 W1110 已根治·避免同文件对改）；chart-design 两页残留的补偿规则越界动作属我方 W1108 遗留，另立小批撤销。

⑤ **收官笔（CI 三红修复）**：PR #113 首次 CI 判红三项（ruff 6 error / 站内搜索索引陈旧 / 判据测试调旧私有 API）⇒ 根因为「落段漏跑生成链」与「主会话 #110 已把私有 _resolve_base 改为公开 resolve_base()」；修法：逐处清裸 l（ruff check scripts/ 0 error）+ 跑本批收官脚本八步链（refresh 第 2 轮收敛 · CSP 856 页零漂移）+ 判据测试改写为正向回归锁 3 例。

⑥ **归档迁移（体积窗口治理·由级联工具自动执行·非手工搬移）**：W989 段由 CHANGELOG 迁入 archive/docs/CHANGELOG-ARCHIVE.md（逐字比对零丢失）· AGENTS 的 W1106 脚注迁入 archive/docs/AGENTS-ARCHIVE.md · file-index 归档时间行同步。CHANGELOG 与 file-index 段数窗口各 110 段（满窗后由级联归档 1 段）。

**验证**：门禁 62 段 0 FAIL · 单测 13 passed（batch_closeout 10 + 判据正向锁 3）· 全量 pytest 本地 1184 passed / 3 skipped（2 failed 为本地工地 scripts/_s4_* 污染·157 件·CI 检出树不含）· CSP 856 页零漂移 · 台账 60/60 窗口内。

### W1110（2026-11-03）：图表色工程档 3 施工前置批（门禁与接线四槽 + CSS 令牌自引用根修）

> **来源**：用户 2026-11-03 指令「开 W1110（54 槽编号唯一性 + 55 槽 PowerShell 解析 + P-3 L2 接线 + CSP 零漂移门禁 + 24 处差异 ΔL* 双口径核档 + 占号纪律），一个 PR、CI 跑一次，且合并只看 required 两项」。
> - **文件**：scripts/verify_delivery.py · scripts/check_powershell_parse.py · scripts/check_csp_drift.py · scripts/check_css_var_selfref.py · scripts/check_pitfall_id_unique.py · scripts/doc_areas.py · scripts/check_doc_sync.py · scripts/agent_start.py · site/data/chart-design.html · site/en/chart-design.html · scripts/guardrails/check_changed.ps1 · scripts/install_hooks.ps1 · xiyouji-agent-web/cleanup.ps1 · docs/agent/gates.md · docs/agent/pitfalls.md · AGENTS.md · HANDOVER.md · .agent/skills/puti-shouye/SKILL.md

**本批要点**（门禁与接线批·**新槽四个**·工具面为主·页面改动 2 件）：

① **第 54 槽「坑表编号唯一」**：W1106 建置的判据自此**兑现接线**（W1107 已登记为「下一批接线」）—— 坑表 E-NN 编号是「按编号检索教训」的唯一键，而第 31 门禁只统计条数不校验编号唯一性 ⇒ 两批各占同号时计数链五处全绿而检索静默取到错条目；本槽常驻后新增条目撞号**当场判红**。

② **第 55 槽「PowerShell 解析」**：仓内 .ps1 此前**零机器判据**。C1 用官方 AST 解析器（只读不执行）逐文件解析⇒语法错误即 FAIL（解析器缺失按 fail-closed 退出码 2）；C2 含非 ASCII 必须带 UTF-8 BOM（PS 5.1 的 -File 加载器回退 ANSI 代码页 ⇒ CJK 关键字**解析静默死亡**·E-68）。本槽**当场抓出 3 个存量缺陷并同批根治**（scripts/guardrails/check_changed.ps1 · scripts/install_hooks.ps1 · xiyouji-agent-web/cleanup.ps1 均含非 ASCII 且无 BOM）—— 加 BOM 后 PS 5.1 解析实测通过。

③ **P-3 L2 接线（复用 C10 同一复算式）**：W1104 批（P-3 L1）落地四类 stats 告警时挂账「口径一致性待异源复算（C10）落地后接入」⇒ 本批把 C10 的板块篇数复算式**抽到 scripts/doc_areas.py** 作共享单一事实源（C10 与 agent_start **同源复用**），agent_start 新增第 5 类告警（口径漂移）。正样本零告警、负样本（注入 a2_docs 漂移）实测命中。

④ **第 56 槽「CSP 增量漂移」**：既有第 8 槽是全站校验，不区分「谁改的」且无归因信息 ⇒ 存量漂移掩盖本批真问题。本槽按**交集判红**（本批改动页 ∩ 漂移页 ≠ ∅）+ **merge-base 基点**逐段字节比对（只对本批碰过的内联段判）+ **失败信息三要素**（漂移页 / 命中段标识 / 修复命令）。端到端负样本实测：注入内联脚本不重算 CSP ⇒ 精准报出「第 3 段内联块（哈希 sha256-IYSkkgjHaoho）」；按提示重算后转绿。

⑤ **双口径核档 ⇒ 抓出并根修 W1108 真实缺陷（本批最大产出）**：对 W1108 的 24 处差异逐项核 ΔL*+ΔE76 时，核档数据与「24 处差异全为同向转换」的既有结论**不一致** ⇒ 追根：W1108 批把 chart-design 两页 INLINED 副本 `:root` 里的图表令牌定义改成「`--chart-1: var(--chart-1)`」**自引用** ⇒ 浏览器在 computed-value time 判为**无效值** ⇒ `getComputedStyle` 返回**空串** ⇒ 连带动使用它的 `--accent` 一并失效 ⇒ 图表主题色回落为继承色。Playwright 受控对照实测：改前 `--chart-1=#C8463A`·主题色 `rgb(200,70,58)` ✔；改后空串·`rgb(35,32,26)` ✘。**根修**：两页副本的 4 条自引用恢复为站点令牌真值（各 4 行·真源 site/tokens.css 完好未动）。**新增第 57 槽「CSS 变量自引用」**把该类缺陷变成常驻机器判据（负样本注入实测判红）。

⑥ **占号共享区纪律 + 落段前占用复核判据**写入 AGENTS §4.3 最高频铁则与坑表 E-128（预约集在工作树内 ⇒ 共享范围=工作树 ⇒ 隔离 clone 占号他方不可见必撞号）。

⑦ **顺带收口 W1088 僵尸行**：该行「登记为在途」但内容早已随 W1086 提交落地（§3.1 迁移批效率协议四条 + 收官清单 step 7 均在 main）且自身无 `type(w1088)` 标签提交 ⇒ preflight 恒红拒绝所有碰 HANDOVER.md 的新批次；本批核实后按收官流程回填状态列（**内容零改动·只改登记面**）。

**验证**：四槽自测 22 例全绿 · 第 41 门禁三方编号对账 0 FAIL（AGENTS/gates/verify 三方同为 57 槽）· CSP 856 页零漂移（909 哈希）· 计数链 229 → **231**（流程段 110 → 112）· 坑表本体 101 条 0 重号（现役最大 E-129）。

### W1109（2026-11-03）：坑表编号重号收敛（18 条改号与本体清零）

> **来源**：W1107 体检批（随 PR #104 落段）登记的存量去向。
> - **文件**：docs/agent/pitfalls.md

**本批要点**（纯文档面·零页面改动·计数链条数不变）：

① **16 组真重号全部跨批次**（同批次 0 组）⇒ 引用可按批次号精确判定 ⇒ 保留各组**批次最早**的一条原号，其余 **18 条改号**（E-110~E-127）⇒ 坑表本体编号重号 **清零**。

② **引用同步**：本体 99 处「（W### 实证·E-NN）」随改号自动同步；「坑表/pitfalls … E-NN」宽松形态的引用按**无歧义口径**（同句含被改批次号 + 旧编号）同步，**其余指向待人工判读**（已登记去向）⇒ 历史报告自有的裸 E-NN 量化经验编号**不动**（两套编号体系并存）。

③ **口径不变**：先落地者保留 + 编号连续（现役最大 E-127）；**条数不变 ⇒ 计数链数值不变（229）**。

**验证**：本体重号自检 0 · 判据脚本 scripts/check_pitfall_id_unique.py 输出存量 NOTE 清单 · 门禁 0 FAIL。

### W1108（2026-11-03）：图表色工程批·档 3 原型验证批（读令牌喂图表 + J2 双态取证）

> **来源**：用户 2026-11-03 裁决「先做 chart-design 这一对原型页，验过机理再按 ≤10 页/批铺开剩余 145 页」。
>
> - **文件**：site/data/chart-design.html · site/en/chart-design.html · docs/11-方案报告/计划方案/T60-任务计划执行与经验沉淀报告-2026-11-03.md · docs/agent/pitfalls.md

**本批要点**（档 3 首支原型批 · 中英成对）：

① **机理验证通过**：站内图表为自研 D3 + 自绘 SVG（全站 echarts 字样 0 处），色值经 .style(--chain-color, color) CSS 变量中转 ⇒ 常量内调色板 hex 可直写 var(--chart-N)；该页已有 10 处 attr(fill/stroke, var(...)) 先例且无任何色值运算 ⇒ 换 var() 不破坏运算。

② **改动面**：两页四常量共 24 处裸 hex，其中 15 处有 --chart-N 对应本次令牌化；其余 9 处（#d97706 / #C9A063 / #e9b885 / #6B6455 / #1a1410 / #d9cdb8）登记去向，待铺开批统一处理（不新增令牌，避免扩大原型批风险面）。

③ **取证读数**：J2 双态逐属性对拍 ⇒ 浅色态 0 差异；暗色态 24 处差异全部为同一方向颜色转换（rgb(200,70,58) → rgb(224,96,79)，即 #c8463a → --chart-1 暗色值）；元素数 750 → 751 / 749（零损失）；非属性类差异 0 ⇒ 非塌缩、无渲染错位。

④ **塌缩防线**：首轮对拍元素数掉到 112，根因为改了内联 JS 未重算 CSP 哈希 ⇒ 浏览器拒绝执行该段脚本 ⇒ 整页图表失效（W1082 同型机理）；重算后恢复 ⇒ 写入坑表 E-108 与 E-109，并建议 W1110 增门禁：diff 命中页面内联 script ⇒ 必须 --check 零漂移。

⑤ **E-108 与 E-109** + 计数链六段求和 = 229（CSS 48 / JS 10 / git 26 / 级联 20 / 数据 15 / 流程 110）。

**验证**：J2 双态 24 处同向颜色转换 + 元素零损失 · 第 53 槽 0 FAIL（专名本地化 2 项属预期）· CSP --check 零漂移 · 第 31 门禁 0 FAIL · 体积窗口 0 FAIL · 推前 ci_sim 干净检出预演全 PASS。

# 更新日志


> **📖 阅读契约（W707）**：查表型——判断「当前版本/最近批次」时只读**顶段 1 个版本段**；查历史段用 grep（`grep -A 30 "### vX"`）；完整通读非预期用法（历史细节在 archive/docs/CHANGELOG-ARCHIVE*.md·grep 单段查勿打开通读）。
本项目所有重要变更均记录于此。格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/)。

## [Unreleased]

> **W### 编号规则**：每个版本段标注唯一 W### ID（W001-W1136），v0.8 内部细分 W008.1-W008.7（B0-B7）。每个 W 附四件套字段（来源/文件/验证/状态）。反向索引见 [scripts/output/file-index.md](scripts/output/file-index.md)（给定文件查改几次）。
>
> **v/W 双键口径（W706）**：时间点查询以 W 号为准（单调键）；v 号在 W659-W667 合并段/并行批次区间不单调（v2.3.262〔W661〕列于 v2.3.261〔W666〕后）；v 号形态演化（阶段标签化·方案 D）经盘点 docs/superpowers/plans/2026-10-11-version-space-inventory.md 后另批实施。
>
> **方案 D 形态切换（W711 生效）**：自 W711 段起，CHANGELOG 段标题去 v 号（新形态 `### W###（日期）：标题`）；W001-W1000 段保留 `### vX.Y.Z（日期）：W###` 历史形态不改写；v 号降格为阶段标签（v2.3·无 patch）；CITATION.cff version 改批次号形态（"W###"·CFF free string）；file-index 历史条目保留 v 引用、新增条目 W only。
>
> **历史版本归档**：v0.1 - v2.3.17（W001-W1000）已迁移至 [archive/docs/CHANGELOG-ARCHIVE-tier2.md](archive/docs/CHANGELOG-ARCHIVE-tier2.md)（W513 二级归档）；W422 再归档 v2.3.18-v2.3.31（W400-W416）段；W511 归档 v2.3.32-v2.3.82（W417-W464）段 + v2.3.83（W484）段至 [CHANGELOG-ARCHIVE.md](archive/docs/CHANGELOG-ARCHIVE.md)。W681 归档 v2.3.84-v2.3.249（W485-W649）段至 [CHANGELOG-ARCHIVE.md](archive/docs/CHANGELOG-ARCHIVE.md)。W736 再归档 v2.3.250-v2.3.293（W650-W699）段至 [CHANGELOG-ARCHIVE.md](archive/docs/CHANGELOG-ARCHIVE.md)（源文件超 50KB/500 行阈值）。本文件正本按 110 段窗滚动（W960 窗口制·正本最老段随批推进·早期形态：W650-W710 段用历史 vX.Y.Z 形态·W711+ 段用批次键 W### 形态）。
>
> **全站页数口径**（W459 建·W702 实跑刷新，各门禁分母不同）：HTML 共 857<!--stats:html_total--> 页（site/data 88<!--stats:site_data_html--> + site/en 138<!--stats:site_en_html--> + site 根 9<!--stats:site_root_html--> + site/reader 622<!--stats:site_reader_html-->）；CSP 覆盖 856<!--stats:csp_covered--> 页（排除 `_template.html`）；check_js_syntax/check_structure 扫 855<!--stats:scan_files--> 文件（再排除 `_shell.html`）；check_seo_head 扫 855<!--stats:seo_scanned--> 页（site 全树减两个模板壳）；inline_css 同步 330<!--stats:inline_css_pages--> 页（site 全树含 INLINED 标记页）；「可视化页 87<!--stats:visualization_pages-->」= site/data 88 减 `_shell.html`。
>
> **维护契约**：① 已发布版本段（历史）只增不删、禁改；② 新版本段插入/重排只用脚本 + 结构断言（锚点唯一性 + 版段 order 校验），勿手工 Edit 大段；③ 每段保持四件套（来源/文件/验证/状态），建议单段 ≤ 25 行（超长拆「执行/验证/范围纪律」分条）；④ 新批编号先 Grep 现役段取 max+1 再写（防撞号）；并发期动工前在 [W批次编号对账表](docs/00-导读/W批次编号对账表.md) 登记认领（W663 起·版段递延时以对账表为准）。