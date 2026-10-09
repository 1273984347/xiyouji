# 更新日志

本项目所有重要变更均记录于此。格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/)。

## [Unreleased]

> **W### 编号规则**：每个版本段标注唯一 W### ID（W001-W676），v0.8 内部细分 W008.1-W008.7（B0-B7）。每个 W 附四件套字段（来源/文件/验证/状态）。反向索引见 [scripts/output/file-index.md](scripts/output/file-index.md)（给定文件查改几次）。
>
> **历史版本归档**：v0.1 - v2.3.17（W001-W399）已迁移至 [docs/archive/CHANGELOG-ARCHIVE-tier2.md](docs/archive/CHANGELOG-ARCHIVE-tier2.md)（W513 二级归档）；W422 再归档 v2.3.18-v2.3.31（W400-W416）段；W511 归档 v2.3.32-v2.3.82（W417-W464）段 + v2.3.83（W484）段至 [CHANGELOG-ARCHIVE.md](docs/archive/CHANGELOG-ARCHIVE.md)。W681 归档 v2.3.84-v2.3.249（W485-W649）段至 [CHANGELOG-ARCHIVE.md](docs/archive/CHANGELOG-ARCHIVE.md)。本文件仅保留 v2.3.250+（W650+）。
>
> **全站页数口径**（W459 起，各门禁分母不同）：HTML 共 234 页（site/data 87 + site/en 138 + site 根 9）；CSP 覆盖 233 页（排除 `_template.html`）；check_js_syntax/check_structure 扫 232 文件（再排除 `_shell.html`）；inline_css 同步 225 页（site/data + site/en，site 根以 `<link>` 引外部 css）；「可视化页 86」= site/data 87 减 `_shell.html`。
>
> **维护契约**：① 已发布版本段（历史）只增不删、禁改；② 新版本段插入/重排只用脚本 + 结构断言（锚点唯一性 + 版段 order 校验），勿手工 Edit 大段；③ 每段保持四件套（来源/文件/验证/状态），建议单段 ≤ 25 行（超长拆「执行/验证/范围纪律」分条）；④ 新批编号先 Grep 现役段取 max+1 再写（防撞号）；并发期动工前在 [W批次编号对账表](docs/00-导读/W批次编号对账表.md) 登记认领（W663 起·版段递延时以对账表为准）。

### v2.3.282（2026-10-09）：W676 站点质量修复批次四 — WP-4.1 fetch 数据装载族 + WP-4.2 可视化正确性 + WP-4.3 命名语义与页脚 sweep + WP-4.4 a11y + WP-4.5 Backlog

> **来源**：站点质量修复六批方案 V1.7（docs/superpowers/plans/2026-10-05-site-quality-remediation-plans.md）批次四（原拟 W675 被复盘批占号顺延为 W676）——第五轮外部审视坐实的 JS 运行期/数据语义/命名一致性/a11y 修复，全部改动 ZH+EN 镜像对称落地。
> - **WP-4.1 fetch 数据装载族四项**：narratology fetchJson 协议反转删除（http 恢复实时装载路径，对齐 12d 形态）；monster-female-network buildSankeyGraph/renderSankey/renderRadar 参数化（函数内 EMBEDDED 直引清零，loadData 死回退摘除）；monster-victims-network renderForce/Sankey/Radar/Timeline 参数化（victimColors/victimNames 改由传入 victims 派生）；monster-ecology-network links 深拷贝（防 forceLink 原地污染 EMBEDDED_DATA）。
> - **WP-4.2 可视化正确性五项**：monster-ecology-network 手搓桑基重写为 d3.sankey()（yPositions 公式错乱根治，补 d3-sankey.min.js 本地引用）；mbti-evolution 雷达/色标/图例三 scale domain[0,8]改[0,10] 加网格圆 [2,4,6,8,10]（值 9 越界根治）；magic-system 预算图删 0.9249 折算两条 bar 仅留盈余条（量纲脱节根治）；monster-background renderKPI 补前置清空。
> - **WP-4.3 命名语义六项**：narratology-13d 改名 narratology-16d 全牵连重命名（页内 canonical/og:url/hreflang/cite/EN 链/fetch 路径 16 处 加全站 26 文件 51 处 加 sitemap 加 hreflang-pairs.json 加 tests 4 件 加视觉基线 png，git mv 双语，site/ 全树清零）；poetry-rhythm 词牌分布改诗词类别分布（实含 7 类，标题/svg title/注释）；magic-system kills 字段改 combat_record 加表头战斗记录（EN 表头已是 Combat Record）；monster-background 存活率差距 10.7 倍改之比约 10.7；window.__clusterOrder 全局泄漏改 renderForce 局部 const；页脚停滞 sweep 162 页（ZH81 加 EN81，v2.2.86·W334 改 v2.3.282·W676，含 bump 污染链 2 页收敛）。
> - **WP-4.4 a11y 两项**：mbti-evolution 4 个 stage-btn 补 aria-controls（单共享面板语义，role=tabpanel 落 radar-wrap——机判原文 tabpanel 计 4 按真实 UI 语义修正为 1，不造假空面板，偏差随档留痕）；全站带 aria 的 svg role=img 覆盖率 143/143（仅 mbti 4 svg 缺，已补）。
> - **WP-4.5 Backlog**：交接文档新增 Backlog 段五条（EMBEDDED 命名分裂/fetchJson 命名统一/og:image 差异化/全站统一 encode[并 W674 登记]/a11y 运行时审计盲区[预登记 BL-5]），全部登记不开工。
> - **证伪留档**（方案标「修复时核对」三项复核不符）：monster-background makeTooltip 实为 d3.select('#tooltip') 单例 select（元素在位无追加）；renderCases 已有前置清空；monster-capability-radar 全部渲染函数已有清空。
> - **验证**：verify_delivery 核心全绿（42 段）；generate_csp --check 855 页 0 漂移（19 页重生成）；check_js_syntax 854 文件过；check_structure 过；ruff 新脚本 0 错；e2e test_smoke 89/89、test_site_quality 全过（含 W676 新增 5 断言：ecology EMBEDDED 不被污染/桑基 5 节点在位/victims 与 female 连续 resize 计数恒定/background KPI 恰 4 卡加 tooltip 单例）；pytest test_narratology_data 36/36；doc-sync C4 补 W691 递延豁免登记（W690 收官级联提交文本提前引用 W691 所致存量失配，D2 通道补记，下一自由号仍为 W691）。test_deep 4 项失败经 HEAD 基线 stash 对照为本地 file:// 环境既有抖动（dashboard hero/index quick-links/narratology hover/chapter-stats，HEAD 同样失败），非本批引入，CI 面为准。
> - **文件**：site/data 与 site/en 各 81 页页脚、monster-ecology-network/monster-female-network/monster-victims-network/monster-background/mbti-evolution/magic-system/poetry-rhythm-analysis 七页双语、narratology-16d-network.html（改名自 13d）双语、site/sitemap.xml、site/index.html、site/dukou-engine.html、site/tag-cloud.html、site/search.html、site/perf-canvas-rendering.html、site/pilgrim-team-psychology-arc.html、site/en/visualizations.html 及 EN 镜像同名页、site/reader/themes 4 页、site/static/js/datahub-index.js、scripts/output/hreflang-pairs.json、tests/e2e/test_narratology_render.py、tests/test_narratology_data.py、tests/e2e/test_deep.js、tests/e2e/test_visual.js、tests/e2e/test_site_quality.js（加 W676 断言）、scripts/_w676_* 五件一次性工具、交接文档.md（Backlog 段）、docs/00-导读/W批次编号对账表.md（W676 认领翻转加现势加 W691 豁免登记）、六文档级联、19 页 CSP 重生成。
> - **处置收尾**：12 张 skill-creator S 卡维持待用户拍板（skills/ 已 W562 退役，不自动建置）；dataset/narratology-13d-network.json 真源与 hyperframes 引用超批次四禁改边界留档未动；12 张 S 卡移交诉求随本批入账不随批执行。
> - **状态**：已落地（CI 五工作流以推送后 gh run list 为准）。

### v2.3.281（2026-10-08）：W690 安全告警处置批 — Dependabot 三包真修 + CodeQL 三条按族 dismiss + Scorecard 维持登记

> **来源**：用户问「GitHub 上 Dependabot alerts 与 Code scanning 为什么还有警告」并令处置——实时取证三类账面（Dependabot 3 / CodeQL 3 / Scorecard 18）三分性裁定后全量处置。
> - **执行（Dependabot 首账真修）**：W683 依赖图开启后首批告警（H-02 预言兑现）三包全修——shell-quote 1.9.0→1.11.0（critical·命令注入·concurrently dev 链·overrides 精确钉）/ katex ^0.16→0.18.2+（low·原型污染·cherry-markdown 与 @vscode/markdown-it-katex runtime 链·overrides）/ brace-expansion→5.0.12（medium·scripts eslint→minimatch 链·npm update 即达）——npm audit 双域 0 vulnerabilities；验证 agent-web build exit 0 + engine.smoke 12 组断言全绿。
> - **执行（CodeQL 按族 dismiss）**：py/bad-tag-filter ×3（scripts/_attic/_w672_* 三件·W685 收档入库后被 CodeQL 首次扫描命中）——dismissed（won't fix·理由：一次性诊断脚本·五处引用零命中·无运行时路径·可重开）；2026 API 形态变证实测（键名 dismissed_reason 过去式+自然语言枚举「won't fix」·旧 dismissal_reason 键 422）。
> - **执行（Scorecard 维持）**：18 条信息级评分条非漏洞·W683 登记裁决不动·H-01 每周 ±3 监控。
> - **验证**：verify_delivery 核心全绿（内容批+级联批）；npm audit（agent-web + scripts）双域 0；Code scanning open 仅余 Scorecard 18（与登记账一致）。
> - **文件**：xiyouji-agent-web/package.json（overrides +2）+ package-lock.json、scripts/package-lock.json、docs/00-导读/W批次编号对账表.md（W690 认领+W689 翻收官+现势 W691）、六文档级联、AGENTS 脚注、四页脚、CITATION、file-index。
> - **处置收尾**：后续每次推送后照常一眼 open 数（W681 习惯）；katex override 为跨次版本强制（cherry-markdown 编辑器数学渲染若有异常先查此处·低危可回退）。
> - **状态**：已落地（CI 五工作流以推送后 gh run list 为准）。

### v2.3.280（2026-10-08）：W689 全变动对抗复审修复批——15 项发现闭环＋DHR 前置区重建＋明清注号重排与数据修正

> **来源**：用户令「review 一遍所有变动」——机械一致性脚本全扫＋独立对抗审读代理（15 项发现＝P1×1＋P2×5＋P3×9·行号级证据）双轨复核当日全部改动。
> - **机械扫确认修复**：数字人文研究适配版前置区三对重复「中图分类号/作者简介」重建（各唯一·次序规范化）；15 份渠道副本按源刷新；`06-文献/md/` stray 旧 INDEX 删除＋正主 INDEX 更新（104 PDF＋md/ 目录批注）；南艺/艺术百家适配版仪表盘措辞补 hedge。
> - **对抗审读确认修复**：P1 数字人文研究版参考文献 [6] 题名「claims」→「data」（Crossref 全题名裁定·脚注版本正确）；P2 适配版「## 一、引言」章级标题补回＋参考文献表收录口径说明与按首现顺序重排＋[3][14] 补引用日期；P2 明清稿注号 ㉑㉒/⑱-⑳ 按出现顺序环换重排（⑱⑲ 制度史·⑳-㉒ GIS·头注同步）＋「86 个回目」显性化为首末回次差口径（第 12 至 98 回）＋空白段「九回无关文节点」口径修正＋「州郡县四处入集」数据修正（玉华县/金平府/铜台府/凤仙郡·原「仅玉华县一处」与表 1 矛盾）＋「严格遵循」配套软化。
> - **P3 采纳**：误报句限定终测口径＋英摘补「另 3 条」分母披露＋[^8] 补「14 类归并三失效模式」勾连＋心学稿「结论所拒斥」指涉修正＋§4.4 四要素改述防复写＋行内 [14]-[19] 标记撤除统一零夹注体例＋明清「并行/平行」自缠消除＋「驿、递、铺三系」展开＋设计稿直角引号规范。
> - **登记待办**：设计稿 AI 声明模型名 V4/V4.1 写法须作者确认统一；心学稿 line 号裸露存量；母题线候选文献验真；类型学描述性定位维持。
> - **验证**：verify_delivery 核心全绿；引文 486 条 100%；ruff scripts/ 全绿；受影响 docx（数字人文研究版/南艺版/艺术百家版）重生成 COM 验收 22/13/13 页。
### v2.3.279（2026-10-08）：W688 第六轮复审处置迷你批——HALLMARK 数字驳回＋摘要/结论/仪表盘措辞轻改＋DHR 英摘去重＋文献清单建账

> **来源**：第五轮审读方复核四稿修订版后的第六份意见（三项核心批判重评估＋HALLMARK 数字主张＋措辞建议）——按逐条验真规程处置。
> - **HALLMARK「2,526→2,525」修正建议驳回**：arXiv:2607.18360 摘要逐字在案「2,526 BibTeX entries spanning 14 hallucination types, three difficulty tiers」（export.arxiv.org API 2026-10-08）；审读方所据 GitHub 仓库条目数与论文口径不一致时，引用论文数为正确实践；反向补 HALLMARK 入 00-文献清单 §3.1（此前注⑧合并时漏建账）＋Resnik DOI Crossref 复核注记。
> - **措辞三处采纳（轻）**：可验证性稿中英摘要与结论的「全部命中/100% hit rate」改「逐字命中公开底本 / 100% verbatim match rate against the public base text」；§五（一）补误报观察句（本批 439/439 即观察误报 0·系统性留待影子模式）；设计稿「常得到一块仪表盘」降为「很容易做成」。
> - **自查事故如实入账**：数字人文研究适配版英文摘要重复（建版时未察觉原稿自带）——本轮发现即修，Abstract 唯一化。
> - **docx 重生成 5 份全 COM 验收**：可验证性主稿 21 页 14,238 字（<15000 ✓·20 条圈号注 PASS）/数字人文研究版 22 页 14,676 字/装饰版·南艺版·艺术百家版各 13 页。
> - **登记待办**：心学判定标准进一步具体化；「程序母题线」叙事学框架对话（候选文献未验不入稿）。
> - **门禁**：引文 486 条 100%。
### v2.3.278（2026-10-08）：W687 S4 四方向外部审读处置与投稿体系批——审读裁决八批同日执行＋CNKI 核验＋渠道要求落夹＋文献 md 化

> **来源**：用户转交第五轮外部审视报告（四方向稿＋文献清单·前提/逻辑/缺失审视）并逐段指令执行——圈选修订菜单、开放知网机构会话、「跑」「下」「添加生成」「装」等八道指令同日闭环。
> - **第五轮审视裁决**：约 40 判定单元＝驳回 12（含报告自身虚构 4 处实录：苗族/花腰傣、YouTube 评论、华中科技 2026、GPTZero 300 篇）·部分采纳 12·采纳 5·方向建议 6——裁决档案＋保真度地图＋修订菜单入档 03-审查与核验/外部审读处置-四方向前提逻辑审视-2026-10-08.md（§1-§11 八批执行追记全）。
> - **四稿修订（批一）**：心学稿新增 §4.4 对读的边界＋可反驳条件＋文献 [14]-[19]；可验证性稿五工具具名（[^18] 群引）＋正交句限定＋[^13] 回写；明清稿「程序母题线」限定＋备择解释＋降格＋GIS/制度史注⑱-㉒；设计稿注释⑭降格＋新中式注⑱⑲＋设计理论注⑯⑰＋竺洪波 [5] 出版社勘正——投稿版＋匿名稿同步。
> - **CNKI 核验（批二/三）**：学术索引 N03-N06 四幻觉条目证伪撤除（对照组甄别法）＋真实文献替补（杨翌琳/姚大勇/王睿文/阳达肖慧）＋N01 年份勘正＋N07 新增＋修订记录 v1.4/v1.5；心学稿近年文献四条（含贾广瑞 2011 撞题划界）＋唐楚涵 2019；全仓扫描确认幻觉零下游污染。
> - **撞题终检（批四）**：三稿核心主张 CNKI 检索全部干净——「西游记 通关文牒」全库仅 2 条非学术（明清稿定位获证）、「引文核验 大语言模型」等三组合零命中（[^13] 回写完成）、心学稿工夫论对读空白确认。
> - **文献体系（批五/八）**：10 篇 CNKI 核验文献 PDF 经机构会话下载存档（18MB·完整性校验过）＋清单 §3.1 十行「已存档」注记；06-文献 全量 PDF→markdown（99 文本层＋5 OCR·md/ 目录 104 份全覆盖）。
> - **投稿体系（批六/七）**：三份 docx 重生成并 COM 验收（可验证性 20 页·20 条圈号注〔五工具群引并注·体例红线 ①—⑳ 维持〕·装饰版/匿名版各 13 页）；14 家期刊官方投稿须知落夹（三路调研代理 211 次调用·官方/二手分级·负结果在案·装饰复核发现「中图分类号疑混入」差异）；25 处渠道副本刷新＋三份体例适配版生成（数字人文研究版 22 页/南艺版 13 页/艺术百家版 13 页·docx/md 双形态）。
> - **门禁**：引文核验 486 条 100% 命中·ruff scripts/ 全绿·术语新违规 0；学术论文索引 v1.4/v1.5 修订记录落账（本批唯一入库正文变更面）。
### v2.3.277（2026-10-08）：W686 动态 Workflow 工业化方案退役 — 方案文件删除 + W682 预留作废（用户裁决等后续重新设计）

> **来源**：用户裁决「把这个方案所有 workflow 都删了·等后续再重新设计」并追令「把这个计划方案也删除」——W679 入库的《动态 Workflow 工业化方案 V1.0》整体退役。
> - **执行**：① git rm docs/superpowers/plans/2026-10-07-workflow-industrialization-plan.md（458 行）——WF-1~WF-6 六提案全部随之作废；退役前实查：方案从未建置到任何实体（.zcode/workflows/ 项目与宿主全局保存件均为 0），无 workflow 代码可删；唯一落地件 WP-1.0（run_eval dotenv 密钥引导）已于 W680 随引擎更换重写移除——零代码残留。② 对账表：W682 预留行注记作废（WF-1 复活随方案退役）、W686 认领行登记、现势翻 W687。③ 保留面：W598 评估资产三件套（golden-50.jsonl/run_eval.mjs/validate.mjs）早于本方案、服务评估基线本身，不动；方案文件头「本文件当前 untracked」过时注记（W679 入库时漏删）随删除消解。
> - **验证**：verify_delivery 核心全绿；全仓引用扫描——活引用 0（仅 scripts/output/_w679_spec.json/_w680_spec.json 两份历史级联 spec 档案提及路径，按历史档不动）；第 31 门禁 C4 预留号拦截 W680 同族二犯实测（W685 级联提交文本「现势 W686」在进入近 15 提交窗口后被点名）并按 AGENTS 规程解除（动工前登记即豁免）。
> - **文件**：docs/superpowers/plans/2026-10-07-workflow-industrialization-plan.md（删除）、docs/00-导读/W批次编号对账表.md（W686 认领+W682 作废+现势 W687）、六文档级联、AGENTS 脚注、四页脚、CITATION、file-index。
> - **处置收尾**：后续 workflow 重新设计时按对账表规程另认领新号，不复活 W682；WF-2 扇出若随批次四重启亦以届时方案为准。dynamic-workflows 能力本体（宿主侧）不受影响，仅本仓方案退役。
> - **状态**：已落地（CI 五工作流以推送后 gh run list 为准）。

### v2.3.276（2026-10-08）：W685 复盘下半场报告入库与工具收尾批 — 投稿体系第二报告入库（序号 32 修位）+ sync_docs 校准 + visit-viewer 清理 + S4 收账

> **来源**：用户令「全都做完」——清算 12 份工作复盘报告未竟事项中 Agent 侧全部可执行项：并行 S4 会话滞留的投稿体系下半场复盘报告入库（其自身 A-05 + W684 报告 A-06「README 索引行合并登记」一并闭环）+ sync_docs 校准（W684 P-11/A-03 存量红）+ visit-viewer 两期 Could 悬项清理 + S4 会话工作区收账。
> - **执行（报告入库）**：docs/10-方法论沉淀/工作复盘与优化分析报告-2026-10-07-2.md（投稿体系建构与方向命名周期·第二报告）入库——方法论 README 索引第 32 行（并行在途行序号 31 与 W684 已入库行撞号→改为 32 并移至其后；S 卡号与 W684 报告 S-10~S-12 撞车→全文重编号 S-13~S-15·承接句同步对齐）。
> - **执行（工具收尾）**：① scripts/sync_docs.py 校准——规则 2 现值化（STATIC_EXPECTED 硬编码 611 改磁盘实数·README/STRUCTURE 聚合声明与项目说明分面声明分列校验）+ 规则 3 预留号豁免（对账表登记即豁免·连续性改按版段标题 W 集合断言·file-index 对账只查主 W 号）+ 规则 5 状态标记正则收紧（只认「状态=进行中」形态）——校准前 9 处 MISMATCH 清零、7 规则全绿 exit 0、合成负样本自证真跳号仍抓获；② site/visit-viewer.html 接入 tokens.css（裸色 7 处 var 化 + fixed 表格布局 + overflow-wrap 治横向溢出——09-13/09-16 两期 Could 悬项清零）；③ scripts/_attic 收档 _w672 扫描器 6 件（第 33-37 门禁常驻后零引用）；④ S4 会话收账——46 件已跟踪脚本路径 sweep（S4 目录重组+方向改名）入账、中性一次性工具 24 件入账，期刊探针族脚本与抓取中间产物按双盲纪律保持本地不入公共库。
> - **验证**：verify_delivery 核心全绿（42 段·内容批实跑）；generate_csp --check 855 页 0 漂移；sync_docs 7 规则 exit 0；ruff scripts/ 0 错；visit-viewer 门禁 33/34/35 口径 0 违例。
> - **文件**：docs/10-方法论沉淀/工作复盘与优化分析报告-2026-10-07-2.md（新增）、docs/10-方法论沉淀/README.md（索引第 32 行修位）、scripts/sync_docs.py（校准）、site/visit-viewer.html（tokens+溢出）、scripts/（46 件 sweep+24 件入账）、scripts/_attic/（+6 收档）、docs/00-导读/W批次编号对账表.md（W685 认领+翻转+现势 W686）、六文档级联、AGENTS 脚注、四页脚、CITATION、file-index。
> - **处置收尾**：批次四~六（W676-W678）维持预留——12 张 skill-creator 卡（S-04~S-09/S-10~S-12/S-13~S-15）随批次四移交；W681 真端点联调与 W682 golden-50 基线仍待用户三键；pre-10-01 复盘悬项点账结论（四项：三吸收一挂批次四）随本批入账。
> - **状态**：已落地（CI 五工作流以推送后 gh run list 为准）。

### v2.3.275（2026-10-07）：W684 工作复盘与优化分析报告入库 — 治理与引擎周期复盘（含 W681 部分/W683 合并登记）
> **来源**：用户令按「工作复盘与优化分析系统提示词（AI Agent 专用版）」复盘；周期=2026-10-07 治理与引擎更换弧线（W679-W683·13 提交全绿）。合并登记：W681 部分（文档清零+归档治理+CodeQL 首账·联调待凭证仍进行中）与 W683（三 starter 收官）随本段补录（D1 式合并段）。
> - **执行（报告）**：docs/10-方法论沉淀/工作复盘与优化分析报告-2026-10-07-治理与引擎.md——执行摘要+九章+附录：E-01~E-10 十项经验量化排序（独立安全审查先行 5.0/手工级联复制改造 4.75/崩溃前写盘 git 重建 4.5/告警按族裁决 4.5/归档三规则 4.5 等）+S-10~S-12 三张 skill-creator 任务卡（引擎冒烟模板/告警裁决流水线/手工级联生成器·均含规格五要素与周级时间表）+U 四项三态决策（dynamic-workflows 暂缓沿用 W675 裁决等）+SC 五场景量化（跳号收官 4.40 最高）+P-01~P-14 问题登记（P0×2 已闭环：铁令跨 session 载体/引擎密钥可读）+WF 两流程（引擎更换批复盘+告警处置 ≥20% 目标）+WBS 七行动（关键路径=A-01 联调→A-02 基线·唯一外部依赖=用户三键）。
> - **合并登记·W681 部分**（4801650+e51d067+82e40d0）：品牌现役面 31 处/10 文件清零（含 agent-web 三 md 与 .workbuddy 功能排除）+三归档件移 docs/archive/ 统一大写 ARCHIVE 后缀+CHANGELOG 滚动归档迁 W485-W649 段 166 节（1861→273 行）+文档规范 §5 固化归档三规则+CodeQL 42 告警首账清零（真修 3：api_server realpath 边界/CORS 常量化/agent-web /api/* 限流·其余按族 dismiss 理由随条）——状态=进行中（剩余=真端点联调待用户 LLM 三键+权限矩阵）。
> - **合并登记·W683**（bdc3fb8+1c8ba10+4b27de2）：三 starter workflow（dependency-review/stale/scorecard·全 action SHA 钉）三首跑全绿+依赖图开启（vulnerability-alerts PUT 204·dep-review 首跑红根因）+SECURITY.md 新增与 stale 权限收 job 级（scorecard 首账快修 2）——状态=已收官。
> - **验证**：verify_delivery 核心全绿（37 门禁 42 段·级联后实跑）；报告全部数字取自 git log/gh api/机判套件当批实测；假设 H-01~H-04 显式标注并给验证法；可行性自评 7/7 可行。
> - **文件**：docs/10-方法论沉淀/工作复盘与优化分析报告-2026-10-07-治理与引擎.md（新增）、SECURITY.md（W683 追记）、.github/workflows/ 三 starter yml（W683 追记）、docs/00-导读/W批次编号对账表.md（W684 认领+W681/W683 版段列同步）、六文档级联、AGENTS 脚注、四页脚、CITATION、file-index。
> - **处置收尾**：A-01 真端点联调（用户配 LLM_API_BASE/LLM_API_KEY/LLM_MODEL 三键·唯一外部依赖）→A-02 golden-50 基线（W682）；方法论 README 索引行随并行会话 README 批合并登记（本批不触碰该文件在途改动）；sync_docs 存量陈旧登记 A-03。
> - **状态**：已落地（CI 五工作流以推送后 gh run list 为准）。

### v2.3.274（2026-10-07）：W680 agent-web 引擎更换批次一
> **来源**：用户两次指令（项目弃用原厂商 CLI 与凭证路线+完全删除其全部品牌内容）与三选一裁决（agent-web 整体退役/保留换引擎/只清提及）——裁决为保留渡口问津但更换驱动引擎；蓝图 docs/superpowers/plans/2026-10-07-agent-web-engine-swap-plan.md（V1.0·集成面 826 行实读量化）。
> - **执行（批次一·引擎替换）**：① 新建 server/engine 四模块——types.ts（契约）、openai-compat.ts（chat/completions 流式驱动：SSE 容忍 CRLF 与注释行与 usage-only chunk、tool_calls 增量按 index 装配、reasoning_content 类推理字段有意忽略、[DONE] 缺失容错）、tools.ts（服务端六工具 read_file/glob/grep/write_file/edit_file/run_command + 权限三分类 + W536/W537 同源安全：realpath 路径守卫/无 shell spawn/命令白名单/读写上限）、agent-loop.ts（maxTurns 封顶工具循环·权限桥逐调用接续）；② index.ts 重接线——SSE 八事件契约逐字段不变（src/ 零改动·前端 fullContent 追加语义实测兼容增量 delta）、权限桥策略保留（bypass 直通/read 放行/plan 只读/acceptEdits 放行写/其余走前端许可）、会话历史改从 SQLite 重建（替代旧 SDK resume·表结构零迁移）、引擎中止信号接线（客户端断开即中止 LLM 流消费）、引擎未配置 400 快速失败；③ evals/run_eval.mjs 重写——spawn 起服（W600 同款模式·AGENT_WEB_ALLOW_BYPASS=1 无人值守）驱动 /api/chat 全链路，机判三规则/self-check/产物形状不变；④ engine.smoke.mjs 常驻冒烟——mock LLM 全链路 4 组机判断言全绿（SSE 事件序列对拍 init,tool,tool_result,text,done/工具真实读盘断言/越界路径被守卫拒绝/文本增量拼接）；⑤ SettingsPage 凭证区改引擎配置状态 + .env.example 换 LLM_API_BASE/LLM_API_KEY/LLM_MODEL 三键与九家主流端点预设表；⑥ package.json 移除旧厂商 SDK 依赖（lockfile 同步）。
> - **全主流适配口径**：引擎代码零厂商分支，端点/模型全配置化；协议层为行业事实标准 OpenAI-compatible（GLM/DeepSeek/Kimi/Qwen/OpenAI/Gemini/Claude 兼容层/ollama/vLLM 均提供该协议端点），预设表入 .env.example。
> - **验证（当批现测）**：npm run build（tsc -b + vite build）exit 0；engine.smoke.mjs 4 组断言全绿 exit 0；feedback.test.mjs 5/5（拆卸噪声与既有先例同族·退出码 0）；run_eval --self-check 4/4；npm audit --omit=dev --audit-level=high exit 0 且 npm ls 旧 SDK 零输出；agent-web 现役面品牌引用 grep 零命中（历史段与迁移蓝图按豁免口径另见 W681）。
> - **文件**：xiyouji-agent-web/server/engine/（新增四模块）、server/engine.smoke.mjs（新增）、server/index.ts（重接线）、server/feedback.test.mjs（注释清理）、src/components/SettingsPage.tsx（引擎配置状态）、evals/run_eval.mjs（重写）、.env.example（换键+预设表）、package.json+package-lock.json（去依赖）、.gitignore（engine 编译副产物）、docs/superpowers/plans/2026-10-07-agent-web-engine-swap-plan.md（新增蓝图）、2026-10-07-workflow-industrialization-plan.md（WF-1 改道记录）、scripts/output/_w680_brand_scrub.py（一次性）、docs/00-导读/W批次编号对账表.md、六文档级联、AGENTS 脚注、三页脚、CITATION、file-index。
> - **处置收尾**：W681=真端点联调（用户配 LLM_API_BASE/LLM_API_KEY/LLM_MODEL 三键）+权限四模式矩阵实测+治理文档品牌引用清零（AGENTS/README/STRUCTURE/交接/Makefile/site/dukou-engine.html/agent-web 三 md）；W682=WF-1 复活（golden-50 在新引擎跑基线）。
> - **状态**：已落地（CI 五工作流以推送后 gh run list 为准）。

### v2.3.273（2026-10-07）：W679 动态 Workflow 工业化方案入库
> **来源**：用户裁决批准《动态 Workflow 工业化方案 V1.0》（2026-10-07 全仓实测扫描·事实基线 B1-B31 逐项带取证命令）并令「开工」；本批 = 方案入库 + WF-1 前置 WP-1.0（对账表现势 W680·W676-W678 批次四~六预留不变）。
> - **执行**：① 方案 V1.0 入库 docs/superpowers/plans/——六提案（WF-1 评估 LLM 基线〔W598 建置起唯一已立项未执行项〕/WF-2 批次修复扇出〔批次四~六 W676-W678 载体·包装站点质量方案档 §十四扇出矩阵〕/WF-3 存量冻结基线抽查〔8 份基线 19,545 行只拦新增零抽查缺口〕/WF-4 复盘报告取证包〔11 份复盘报告重复取证劳动〕/WF-5 外部输入逐条裁决〔W634 先例流水线化〕/WF-6 触发条件登记不建置）+ 运行时硬约束 9 条 + 事实基线 31 项 + 产出契约 TypeScript interface + 验收表逐条命令+期望输出 + §1.3 范围外反向清单（门禁/级联/提交链/e2e 等六类禁 workflow 化）；② WP-1.0 run_eval.mjs .env 密钥引导补丁 9 行——只载 CODEBUDDY_* 前缀变量（PROJECT_CWD 等不碰·example 内为过期路径）、已存在环境变量优先、.env 缺失静默跳过。
> - **探测实证（当批现测）**：node --check exit 0；--self-check 输出 4/4 通过；--limit 1 探测 → 用例 chapter-001 报 SDK「Authentication required. Please use /login」+ exit 0 落盘 score 0/1（垃圾产物已删除）——凭证缺失实锤（.env 不存在 + 无全局 CODEBUDDY_API_KEY + ~/.codebuddy 实查为 CLI 工作目录非凭证库）＝方案 R3 预设场景；据此方案 WP-1.2 增补 score=0 熔断守卫（workflow 不信 exit code 单值）。
> - **验证**：verify_delivery 核心全绿（提交前实跑·37 门禁 42 段锁）；run_eval.mjs --self-check 4/4；node --check exit 0；方案文档过第 18 门禁（4 新文件检查含本件）。
> - **文件**：docs/superpowers/plans/2026-10-07-workflow-industrialization-plan.md（新增·方案 V1.0 六提案+执行记录 §5.6）、xiyouji-agent-web/evals/run_eval.mjs（更新·密钥引导）、docs/00-导读/W批次编号对账表.md（现势 W680 + W679 认领行）、scripts/output/_w679_spec.json（spec 档案）、六文档级联、AGENTS 脚注、三页脚、CITATION、file-index、_cascade_files_W679.txt（级联清单）。
> - **处置收尾**：WF-1 主跑阻断于 P0-1 用户凭证（xiyouji-agent-web/.env 配 CODEBUDDY_API_KEY 或 CLI /login 二选一），凭证就位后按方案 §5.3 WP-1.1 单例实测 → WP-1.2 工作流建置继续（届时另认领 W 号）；WF-2 随站点质量批次四 W676 启用；批次四~六编号预留 W676-W678 不变。
> - **状态**：已落地（CI 五工作流以推送后 gh run list 为准）。

### v2.3.272（2026-10-06）：W675 工作复盘与优化分析报告（W666-W674 站点质量前三批周期）入库
> **来源**：用户指令「先复盘再继续」——按 skill@工作复盘系统提示词（AI Agent 专用版）对 W672-W674 站点质量修复周期全量复盘；沿 W666 先例入库 docs/10-方法论沉淀 并登记方法论 README 索引第 29 行。
> - **报告结构**：执行摘要/信息基础与假设（H-01~H-04 全标注）/经验复用 10 项量化排序（E-01 渲染等值确定性五件套 5.0 分 ~ E-10 defer 时序核查 4.0 分）/技能矩阵 6 项+skill-creator 三卡（S-04 渲染等值工具 CLI 化·S-05 批量修复器模板·S-06 e2e 探针规约——均为本周期已验证模式的固化，验收绑定批次四实战）/未用技能 4 项决策（U-01 dynamic-workflows 暂缓至批次六复评/U-04 LHCI 本地化条件触发）/高优场景 3 个（SC-01/03 已沉淀·SC-02 由 S-05 承接）/问题 15 例登记全闭环（P0=0·P1×4·分类技能 47%/流程 33%·同型复发四族——CSP×3、W621 假 0×3、W633 lint×2、提交切分×2——全部本体根治或规则升级）。
> - **P0 改进两项（随批次四首日落地）**：A-01「凡改内联脚本，探针/机判前必 regen CSP」前置化（P-07 三犯族）；A-02 暗色审计器内建「服务在位断言」（P-11 W621 假 0 三犯族）。
> - **量化数据**：三批缺陷修复 ≈1,617 处/项；门禁 32→37 槽（42 段锁）；11 提交全绿；CI 红枪 11（真红 4/伪红+外部 7）——真红全部被既有门禁实抓，无一入产线。
> - **验证**：报告内全部数字标注来源（git log/gh run/门禁输出/机判套件实测）；假设 H-01~H-04 显式声明并给验证法；可行性自评 7 项结论「可行」+1 项「需调整」（A-05 test:e2e 存量适配降级为裁决项）。
> - **文件**：docs/10-方法论沉淀/工作复盘与优化分析报告-2026-10-06.md（新增·约 200 行）、docs/10-方法论沉淀/README.md（索引第 29 行）、docs/00-导读/W批次编号对账表.md（W675 认领+翻转·批次四顺延 W676 注记）、六文档级联、四页脚、CITATION、file-index。
> - **处置收尾**：站点质量批次四~六编号顺延 W676-W678（W675 由本报告批占用·方案「冲突即顺延」条款）；A-01/A-02 与 S-04~S-06 随批次四首日落地；批次四动工前按对账表认领 W676。
> - **状态**：已落地（随本批级联提交；CI 五工作流以推送后 gh run list 为准）。

### v2.3.271（2026-10-06）：W674 站点质量批次三 — JS 交互缺陷 10 项修复 + D4 默认 A + 第四轮四项/P3 清理包 + e2e 补盲
> **来源**：站点质量修复六批方案 V1.7 批次三（§五 WP-3.1–3.15·批次一/二 W672/W673 已收官）。
> - **WP-3.1/3.2 cross-time-danmaku（ZH+EN）**：escapeHtml 从 renderHeroStarMap 提升至主脚本顶层（renderWorldMap 越界引用 ReferenceError 实证）；hero section 补 <svg id="hero-canvas">（原 d3.select 空选区·星图永不渲染——节点数 0→10 e2e 实证）；EN 镜像更重病=tooltip 挂载 div 根本不存在（JS 引用空选区·桌面同失效）随批新建。
> - **WP-3.7 tooltip 定位三页（ZH+EN）**：criticism-history 宿主 section 补 position:relative（坐标按 stageRect 计算而 offsetParent 错位）；cross-time-danmaku #hero-tooltip 移入既有 relative 的 .hero（坐标系对齐·坐标计算不改）；chart-design sundial-tip 改 position:fixed（挂 body+视口坐标——absolute 随滚动错位·fixed 恒对视口；scatter/spiral 两处实测证伪=挂载容器内联 relative 本在位、偏差即设计偏移 +14/-10）。
> - **WP-3.3/3.4/3.5 character-dynamic-network（ZH）**：播放边界 >=100 → >= STAGE_RANGES[currentStage].to（播放语义=播放当前阶段）；label selection 存 _labelSel 与 _nodeSel 同 dim（0.15/1）；setStage 首行调 exitNeighborhood()（切阶段清邻域残留全暗）。EN 镜像系不同代实现无此三病（已记录）。
> - **WP-3.6/3.8 character-semantic-network（ZH+EN）**：renderForce tooltip 单例获取（3 调用+resize 重渲染原每次 append 泄漏；EN 为 .tooltip 类变体同病同修）；scaleSequential 去二次归一化（accessor 已除 maxWeight 再叠 domain 压缩——max 格色=interpolateYlOrRd(1) e2e 实证）。
> - **WP-3.9 数据三项（ZH+EN）**：relationship-3d 度数 KPI 改「悟空/度数 12」（links 实算 12/7·CENTRALITY 同悟空不改）；图例 swatch 三处错色等量替换对齐 GROUP_COLORS（取经团 #e67e22/妖界 #5a7a3a/龙族 #7a5230）；presence-timeline 三张模拟派生图 caption 追加「出场为区间×固定密度模拟（非逐回真实数据）·曲线基于 31 个抽样回目」（EN 同步）。
> - **WP-3.10 微优化**：relationship-3d 循环内 new Vector3 O(n²) → 顶层共享 _tmpV3（**惰性创建于 init3D：three.r128 为 defer，顶层语句时 THREE 未定义——初版顶层 new 致整块崩、e2e K9 抓获自纠**）；cross-time-danmaku loadMessages 模块级缓存+写入失效（弹幕循环每 2.5s JSON.parse）。
> - **WP-3.11 P3**：81-hardships renderInsights 签名去参（洞察为注释性文字非派生）；concept-device commentators 9 条死数据实证 0 消费但删除与 §十一 dataset 冻结（批次一至五）+ 第 9 门禁对账冲突——让行保留、登记 Backlog 随批次六三方同步（dataset 真源+生成器+页面）；_shell.html 旧 audit 块 5 个删除（页面已是 W656 单模块）。
> - **WP-3.13 D4 裁决默认 A（criticism-history ZH+EN）**：一次性演出语义保持+「重演」按钮（重置 animation 强制 reflow 恢复）+ reduced-motion 专项豁免（0.01ms 快进仍停「文字消失」终态——animation:none 回基础可见态）+ DESIGN.md §5 白名单登记（wordFloat 5s/bladeCut 6s/crackOpen 6s）。
> - **WP-3.14 第四轮四项**：journey-geo-3d vertexColors:true（r128 废弃 API·EN 无此镜像页）+ WebGL catch 分支补 __geo3dStats（探针漏报防）；dialogue-sentiment KPI 实算改 819/1941/3787/3515 条 53.7%（json 真源实算·EN 回滚保持与其 EMBEDDED 旧快照自洽——EN 数据副本陈旧登记批次六）；journey-map-interactive「9 大难点」→「8 处难点」（isHardship 实测 8·文案/图例/KPI 四处·ZH+EN·FILE_INDEX 历史注释保留登记）。
> - **WP-3.15 P3 清理包**：W042 a11y 空注释 78 文件删除（注释下方无实现·system.css 已有 :focus-visible）；game-webnovel rarity-pie-svg/element-donut-svg → rarity-treemap-svg/element-treemap-svg（ZH+EN·实渲染 treemap）；journey-spacetime 死函数 chapterNumFromDataChapter 删除；GitHub blob URL encode 维持 Backlog（方案既定不开工）。
> - **WP-3.12 e2e 补盲**：tests/e2e/test_site_quality.js 15 断言（A1–A8+K9–K11）W674-E2E-PASS；scripts/package.json test:e2e 串联；test_smoke/test_deep 补 playwright 解析回退+字体 CORS 本地白名单（**test:e2e 套件无 CI workflow 引用（W204 时代本地套件）·本地首跑暴露 smoke/deep 存量 file:// 失败 10 项（13d tooltip/dashboard hero/quick-links/timeline hover 等——涉事页本批零改动·非本批回归·如实登记）**）。
> - **验证**：ruff 全过；verify_delivery 核心全绿（37 门禁 42 段）；check_js_syntax 854 文件通过；三扫描器（head/缺分号/孤立）0；CSP 重生成（多轮·每改内联脚本必 regen 三度实证：探针全灭→replay 死代码→哈希失配）；e2e 15 断言全绿。dark-state-gate 与 Screenshot Review 以推送后 CI 为准。
> - **文件**：site/data/*.html ×55、site/en/*.html ×36（JS 交互修复+镜像+清理包）、site/data/_shell.html、DESIGN.md（§5.1 白名单 +1 条）、tests/e2e/test_site_quality.js（新增）、tests/e2e/test_smoke.js、tests/e2e/test_deep.js（解析回退+白名单）、scripts/package.json（test:e2e 串联）、docs/00-导读/W批次编号对账表.md（W674 认领+翻转）、六文档级联、四页脚、CITATION、file-index。
> - **处置收尾**：Backlog 新增两项——①concept-device commentators 三方同步（随批次六·§十一冻结让行）；②test:e2e smoke/deep 存量 file:// 失败 10 项适配（http 环境/用例更新·登记不开工）；批次四至六（W675-W677）按方案 §六-§八续作，批次四动工前按对账表认领 W675。
> - **状态**：已落地（随本批级联提交；CI 五工作流以推送后 gh run list 为准）。

### v2.3.270（2026-10-06）：W673 站点质量批次二 — kpi-card 全局基类 122 页 + CSS 机械修复 526 处 + 第 35/36/37 门禁挂载
> **来源**：站点质量修复六批方案 V1.7 批次二（§四 WP-2.1–2.6·批次一 W672 已收官）。
> - **WP-2.1 前置审计**：有页面级 .kpi-card 私有基类的 18 页 117 条声明集提取留档（scripts/output/_w673_kpi_private_audit.csv）——私有规则零删除（页面私有 style 在 INLINED 块后加载，覆盖全局，行为不变）。
> - **WP-2.2 全局基类 + 分发**：system.css 在 .kpi 块后新增 .kpi-card 全局别名基类（与 .kpi 平行：position:relative 宿主 + border-top:3px solid var(--accent) 恢复 W557 被洗形态 + hover 升起 elev-2 + .label/.value/.desc 与 .kpi-label/.kpi-value/.kpi-desc 双套子类名兼容 + 全 token 引用零裸色 + 时长全部 var(--dur-base) 合 DESIGN §5 预算）；inline_css.py --force 重分发 328 页（INLINED 完整性门禁 min 43137B 绿）+ CSP --check 855 页 0 漂移；aesthetics .kpi-card::before absolute 飞至文档左上（无定位宿主）随 position:relative 复位。
> - **WP-2.3 缺分号 442 处**：_w673_fix_semicolons.py（扫描器 1 同款内核=剥注释后换行形态+同行双通道·规则末条豁免；换行形态行尾补 ;、同行形态在被吞属性名前插 ;·CRLF 保持）——实测换行 147+同行 295=442，逐文件自断言修复后残留 0（首版两坑自纠：漏剥注释 5641 假阳性、同 span 多命中互相覆盖 79 文件假残留）。
> - **WP-2.4 孤立选择器 214 行**：_w673_fix_orphans.py——84 处扫描命中 + 130 行同文连带残缀（如 EN underworld 4 连 header 与后继规则拼成四级死后代选择器；text-search footer. 三连）共删 214 行；.detail- 族（timeline ZH/EN）按方案考古（git log -S detail-icon 仅初始提交 v2.2.42=胎带损坏无历史形态）删除孤立行含 @media 内豁免残缀。
> - **WP-2.5 降级对齐 2 页**：chapter-stats 声明 simplified→scroll-x；两页私有块追加 .chart-block{overflow-x:auto} + .chart-block svg{max-width:none;width:auto}——width:auto 为对抗 system.css .chart-block svg{width:100%}（375 视口实测 svg 被压至 325px 容器不滚，补后 maxBlock 1174/984）。
> - **WP-2.6 第 35/36/37 门禁**：check_css_decl_separators.py（self-test 3/3）+ check_css_orphan_selectors.py（2/2）+ check_kpi_card_base.py（C1 system.css 含基类 + C2 使用页 INLINED 含规则·link 直引 system.css 豁免·模板壳排除·2/2）挂第 35/36/37 槽（wrapper 防静默跳过同款）+ 段自洽锁 39→42 段；AGENTS §4.2 补录三条目 + 文档规范 §8 编号至第 37 门禁。
> - **验证**：动工前基线复测 442/84/122 与冻结一致 → 修后扫描器 1/2 归零 + 三门禁首跑全零（234 页）+ verify_delivery 核心全绿（37 门禁 42 段）+ check_structure 854 文件平衡 + token 覆盖率 0 新增 + CSP 0 漂移 + Playwright 机判 _w673_verify.js 全绿（W673-VERIFY-PASS：kpi 10 页抽样 computed bg≠transparent/border-top=3px、aesthetics 左上 12×12 无 accent 像素、CSSOM 断言 .source-list 规则从损坏后代选择器复活为合法顶层规则（全站无消费元素系死规则·以规则级验证为准）、timeline .detail-icon@480 bg=rgb(241,235,221)/fs=54.4px=3.4rem（renderDetailCard(0) 触发渲染）、降级 2 页 doc=375 且容器滚到内容宽 1174/984、81-hardships .filter-row select background 复活 rgb(255,255,255)）。dark-state-gate 与 Screenshot Review 以推送后 CI 为准。
> - **文件**：site/system.css（+kpi-card 基类块）、site 页 ×329（WP-2.3/2.4 机械修复 + aesthetics/chapter-stats 降级对齐 + 328 页 INLINED 重分发）、scripts/check_css_decl_separators.py、scripts/check_css_orphan_selectors.py、scripts/check_kpi_card_base.py、scripts/verify_delivery.py（+3 槽）、scripts/_w673_fix_semicolons.py、scripts/_w673_fix_orphans.py、scripts/_w673_kpi_audit.py、scripts/_w673_verify.js、scripts/output/_w673_kpi_private_audit.csv、AGENTS.md（§4.2 三条目）、docs/00-导读/文档规范.md（§8 编号 37）、docs/00-导读/W批次编号对账表.md（W673 认领+翻转）、六文档级联、四页脚、CITATION、file-index。
> - **处置收尾**：批次三至六（W674-W677）按方案 §五-§八续作，批次三动工前按对账表认领 W674；方案 §四 验收「.source-list computed=8px/0.78rem」以 CSSOM 规则级断言兑现（元素全站不存在）。
> - **状态**：已落地（随本批级联提交；CI 五工作流以推送后 gh run list 为准）。

### v2.3.269（2026-10-06）：W672 站点质量批次一 — dataSource 50 页移位 + CSS 变量漂移 648 处映射根治 + 第 33/34 门禁挂载
> **来源**：站点质量修复六批方案 V1.7 批次一（docs/superpowers/plans/2026-10-05-site-quality-remediation-plans.md·2026-10-05/06 九轮外部审查裁决合并；W671 已被共享载体治理批占用，六批顺延 W672-W677，方案档与对账表已更正）。
> - **WP-1.1 dataSource 移位（50 页）**：W657 注入器把 <div id="dataSource">（含 cite-block 整套 details/summary/button 等 7-8 种标签）写进 </head> 之前，浏览器 foster parenting 将其移到 body 顶部渲染——视觉侥幸正确、源码畸形。_w672_move_datasource.py 按 div 嵌套平衡截取完整块移位至 <body> 首子节点（与实际渲染位置一致）；site/static/js/cite-box.js 实测未被 git 跟踪而 86 页引用（W657 漏 add：线上 404、复制按钮静默降级）——本批补入库。渲染等值验收：5 页抽样×2 视口 Playwright 逐像素 diff = 0（确定性口径：mulberry32 固定种子 + performance.now 虚拟时钟 rAF 泵 + reduced-motion + fonts.ready + getAnimations 冻结 + 滚动穿透；过程实证两处同代码漂移的根因为晚启 d3 过渡被泵冻结在真实时钟依赖的中间态、以及字体量宽竞态被 DOM 时序翻转——均以口径收敛归零，未用白名单放行）。
> - **WP-1.2 变量漂移映射替换（616 处 style 块内 + 32 处块外 JS/内联引用）**：62 种未定义变量四组处置。A 组直映射 23 种：--border→--line、--muted/--text-muted/--text-secondary→--ink-soft、--card/--table-stripe→--paper、--fg/--text-primary→--ink、--accent-primary→--accent、--accent-secondary/--accent2/--accent-1→--accent-2、--accent-tertiary→--accent-3、--accent-quaternary→--accent-4、--line-soft→--line、--bg-primary→--bg、--bg-secondary/--table-header/--paper-card/--paper-deep→--paper-warm、--hero-meta→--ink-faint、--tooltip-bg→--dark、--shadow-md→--shadow-lift。C 组语义 5 种：--pos→--accent-4（苔绿正向）、--neu→--accent-3（赭石中性）、--neg→--accent（朱砂负向）、--accent-5/--accent-6→--accent-4（最近可用序数）。D 组直映射 26 种（四路子代理只读扇出取证·JS colorMap/图例 hex 十六进制就近）：--r-warrior→--chart-4、--r-king→--chart-1、--r-judge→--chart-3、--r-marginal→--chart-6、--r-buddha→--accent-3（裁决改：保留与 r-judge 的区分度）、--r-taoist/--r-bodhi→--chart-2、--r-mortal→--chart-4、--t-lone→--rebel、--t-family→--chart-3、--t-alliance→--chart-4、--water→--chart-2、--fire→--chart-1、--mountain→--chart-3、--sky→--chart-4、--cinnabar→--accent、--indigo→--accent-2、--jade→--accent-4、--shadow-deep→--elev-3、--rarity-ur→--chart-3、--rarity-ssr→--accent-3、--rarity-sr→--accent-2、--rarity-r→--accent-4、--rarity-n→--ink-soft、--svg-color→--chart-1、--canvas-color→--chart-2。D 组回退式 6 种：--r-mount→var(--r-mount, var(--chart-6))、--t-bureau→var(--t-bureau, var(--chart-2))（现役调色板无紫系）、--space-2/3/4/6→像素回退 8/12/16/24px（tokens.css 无间距 token）。B 组语境二分：--shadow-hover 22 处 hover/focus/active→--elev-2、常态→--shadow（附录 B 规则）。--gold 按文件三分（数据叙事金→chart-3×3 文件；成套 accent-3 场景→accent-3×2 文件）+ visual-art 按选择器二分（kpi-card.gold/spec-item→accent-3；artistic-statement/wave-tip 深底→chart-3）。判读：10 页抽样（62 文件序 1/8/15/21/28/35/42/48/55/62）前后 diff 区域全部落在被映射变量的选择器作用区（magic-system energy-law 引块赭金竖线复活、monster-ecology 图例四色 swatch 归位、版面增高 1-35px 系塌陷边框/间距复活）。
> - **WP-1.6 自引用删除（24 处/8 文件）**：--paper:var(--paper) 形态自引用环触发 computed-value invalid（纸面底色失效）——外科手术式移除声明（同 :root 其余合法声明保留），INLINED tokens 定义获胜（81-hardships-view / character-relationship-3d-view / data-explorer / search 及 EN 镜像）。
> - **WP-1.3/1.4 第 33/34 门禁挂载**：check_html_head_content.py（head 区间按序剥离 script/style/noscript 内容与注释后仅允许 head 合法开标签·234 页首跑 0 违例·--self-test 2/2）+ check_css_var_refs.py（style 块无 fallback var(--x) 须命中已知定义集·口径裁决=扫描器 3 宽口径 tokens∪页内 style∪内联属性∪JS 文本，--chain-color JS 运行时定义 32 处豁免与 §1.2 甄别一致·234 页首跑 0 违例·--self-test 2/2）；verify_delivery 挂第 33/34 槽（wrapper 防静默跳过同款）+ 段自洽锁 37→39 段；AGENTS §4.2 补录两条目 + 文档规范 §8 编号至第 34 门禁。
> - **WP-1.5 W657 注入器处置**：注入器=scripts/output/_w657_cite_inject.py（一次性脚本·W649 清账入库）——按方案不修复、不复活，防再犯由第 33 门禁承担。
> - **验证**：附录 A 五扫描器动工前当批复测与冻结基线一致（缺分号 442/孤立 84/未定义 616·62 种·62 文件/自引用 24/head 50/度数悟空 12-唐僧 7）→ 修后扫描器 3 全零（undef 0/0/0+selfref 0）、扫描器 4=0、86 页 id="dataSource" 恰 1 次；verify_delivery 核心全绿（34 槽·39 段锁·含新 33/34 槽）；generate_csp 重生成（8 页 JS 串引用改写）后 --check 855 页 0 漂移；token 覆盖率 0 新增裸色；CSS 结构平衡 854 文件通过；check_js_syntax 854 文件通过；a11y 审计 exit 0（无新增 P0/P1）。dark-state-gate 与 Screenshot Review 以推送后 CI 为准。
> - **文件**：docs/superpowers/plans/2026-10-05-site-quality-remediation-plans.md（方案档入库·编号顺延更正）、site/data/*.html ×50（WP-1.1 移位）、site/data+site/en/*.html ×70（WP-1.2/1.6 变量映射+自引用；其中 8 页含 JS 串改写经 CSP 重生成）、scripts/check_html_head_content.py、scripts/check_css_var_refs.py、scripts/verify_delivery.py（+2 槽）、scripts/_w672_move_datasource.py、scripts/_w672_var_drift.py、scripts/_w672_shot_equiv.js（渲染等值验收工具·批次二/三复用）、site/static/js/cite-box.js（补 W657 漏 add）、AGENTS.md（§4.2 两条目）、docs/00-导读/文档规范.md（§8 编号 34）、docs/00-导读/W批次编号对账表.md（W672 认领+翻转）、六文档级联、四页脚、CITATION、file-index。
> - **处置收尾**：Backlog 新增一项——第 15 门禁增强候选「script src 资产 tracked 校验」（cite-box.js 漏 add 实证·登记不开工）；批次二至六（W673-W677）按方案 §四-§八续作，批次二动工前按对账表认领 W673。
> - **状态**：已落地（随本批级联提交；CI 五工作流以推送后 gh run list 为准）。

### v2.3.268（2026-10-05）：W671 共享载体治理 — 子代理派发政策入 AGENTS §4.3 + 默认路径普查三发现入 backlog 登记档
> **来源**：用户指出「写进私有项目记忆的内容不在项目内显示，多 Agent 协作仍会出问题」——W516/W517 载体铁律（共享机制必须写仓库 tracked 文件·禁只写全局路径）对私有记忆的同型适用；本会话两处「只写记忆」的载体错误就地落仓。
> - **AGENTS §4.3 新增**：子代理显式派发三类场景（①独立取证扇出 ②只读调研可并行 ③长等待空档禁纯 sleep）+主 context 保留三类（裁决冻结史/串行变更链/跨步骤即时发现）+机器门禁优先于 agent review+子代理产出落仓库公共载体。
> - **backlog 登记档第五节**：默认路径风险面普查三发现登记不开工（R-1/R-2 中级：spot_check_nlp/data_validate 默认输入依赖未 tracked 产物·管线后校验器属设计；R-3 低级：extract_datasets.js README 模板示例误导性引用）——源自 W670 Explore 子代理 420 脚本普查（544K tokens·与级联并行·风险面基本清零）。
> - **验证**：纯文档批；verify_delivery 核心全绿（32 槽+37 段锁+doc-sync 0 FAIL）。
> - **文件**：AGENTS.md（§4.3 新条目）、docs/superpowers/plans/2026-09-30-maintenance-backlog-registry.md（第五节）、docs/00-导读/W批次编号对账表.md（W671 认领+翻转）、六文档、四页脚、CITATION、file-index。
> - **状态**：已落地（本批提交并 push origin/main）。

### v2.3.267（2026-10-05）：W670 开放项双闭 — blob 预算口径裁定落档（阅读流为准）+ character_nlp 默认源切权威分回目录
> **来源**：用户 userselect 圈定两项开放项（W661 blob 口径登记 / W668 text-search 提取脱节登记）要求处置。
> - **blob 预算口径裁定**：阅读流为准——预算语义=D-1「读者点内容链接不外跳」（W593），topnav「在 GitHub 查看」为刻意源访问功能不计入；阅读流 813 ≤ 1000 达标维持，全量 1428 仅作盘点参考值。历史段 W661 的「待用户裁定」开放项就此关闭（裁定记录随本段，历史段不改写）。
> - **text-search 提取脱节处置**：character_nlp.py 默认 --input 由 site/data/text-search.html 改为 source/原文/分回/（语料迁出系历史批刻意行为·页内批注明载；旧提取正则对其恒 0 回为 W668 实证）；无参冒烟加载 100 回、输出与显式路径逐字一致；docstring/argparse help 同步；extract_chapters_from_html 兼容保留供显式旧格式输入。verify_chapters.py 盘点=无 tests/CI/run_all 接线零调用方，留档不删。
> - **验证**：ruff 全过；无参冒烟 100 回（3515/-0.4694 与显式路径零差异）；verify_delivery 核心全绿（32 槽+37 段锁）。
> - **文件**：scripts/B_人物/character_nlp.py、docs/00-导读/W批次编号对账表.md（W670 认领+翻转）、六文档、四页脚、CITATION、file-index。
> - **状态**：已落地（本批提交并 push origin/main）。

### v2.3.266（2026-10-05）：W669 WP-E 内容发现架构 — A4 主题导航 hub + dashboard tab 口径对齐 + mobile-index 退役（W651 已启动项·master plan 工程线收官）
> **来源**：W651 全量启动裁决六项的最后一项（其余五项 B-5/B-6 第二步/B-7/B-9①②/WP-D2 已于 W655-W662 收官）——master plan §WP-E 三条 + 第 4 条否决项维持（viz 相关推荐不做·防重复评估）。
> - **A4 主题导航 hub**：build_reader.py 新增 --hub 模式与 build_themes_hub()（全量跑同步重建防重渲删页）；分组依据=docs/03 README 命名规范前缀族（实测 README 无文章列表）：取经X 34 / 西游与X 22 / 其余 153 音序平铺；site/reader/themes-hub.html 机判 209 链接全唯一 == EXPECT_A4 同源；总目录顶部 hub 入口链接；sitemap +1（0.6）。
> - **dashboard tab 口径对齐**：7 tab 文案按实测对齐——全部 41→**51**（全站去重 data/*.html 链接·蓝图实测口径）、A-L 8→12、M-U 9、V-AH 14、Q+ 2、Q++ 3、Q+++ 5（分类卡面去重；51 的构成=六分类 45+数据中枢 5+全站检索 1·尾差构成已注明）；口径句「41 个专题」→「51 个专题页」。
> - **mobile-index.html 退役**：文件删除+3 处引用收敛（data/search.html 搜索索引条目删除、zh/en tag-cloud ?q= 注释来源改 dashboard；dukou-engine 历史修正叙述按「历史不改写」保留）+ gen_sitemap 重生成（**850 净稳**：+themes-hub −mobile-index）+ 搜索索引重生成（pages_zh 95：−mobile-index +themes-hub——后者按 W669 例外规则入索引补发现性）。
> - **过程两误两获（如实）**：①页域过滤用 os.path.join 反斜杠前缀对正斜杠路径永假（本会话已文档化坑的三犯）→ 改 '/reader/' in 包含式；②最后一次索引重生成跑在 generate_csp 之后 → search.html CSP hash 过期拦内联脚本、黄金查询假象 20/30——「改内联脚本必跑 generate_csp」铁律自违自查，apply 后 30/30 恢复；generate_csp 覆盖面经查无盲区（纯流程顺序违例）。
> - **验证**：hub 209/209；黄金查询 30/30；lint_links site 14040 链接 0 broken；CSP 855 页 0 漂移；verify_delivery 核心全绿（32 槽+37 段锁）。
> - **文件**：scripts/build_reader.py、scripts/_gen_search_index.py、site/reader/themes-hub.html（新增）、site/reader/index.html、site/dashboard.html、site/sitemap.xml、site/data/search.html、site/data/tag-cloud.html、site/en/tag-cloud.html、site/mobile-index.html（删除）、docs/00-导读/W批次编号对账表.md、六文档、四页脚、CITATION、file-index。
> - **状态**：已落地（本批提交并 push origin/main）。

### v2.3.265（2026-10-05）：W668 外部数据评审裁决落地 — hardships 三难重分类 mind + dialogue 口径注记 + B-C 级 16 页性质标注
> **来源**：用户转发外部数据层评审（47 个 JSON 分级 A/B/C + 修正建议）→ 本会话逐条对仓取证裁决（四主张：三妖 first_chapter 系旧快照 W643 已修/cave 两文件一致性主张误判/如来样本偏差属实但扩别名前提不成立/hardships 重分类属 W639 作者裁决项）→ 用户三项拍板后本批执行。
> - **T1 hardships 三难重分类**：五庄观中/难活人参/金銮殿变虎 cause→mind（镇元子地仙、奎木狼天神下凡皆非野怪）；生成器 C_情节/hardships_81.py 为单一事实源，全线传播：scripts/output/data 重生成 + dataset/81-hardships.json 明细三行与聚合字段重算 + site/data/json 部署副本 + 81-hardships.html EMBEDDED 四块 + 三难明细行 + 页面 3 条洞察叙述重算（野怪 26 难中 18 被打死 69.2% / 安排 26 难 22 接走 4 收编 / 心魔 13 难 7 被打死）+ CSP 重生成；终态分布 arranged 26 / wild 26 / mount 16 / mind 13（总 81 不变·ending/difficulty 不变）。过程修正：旧 output/data 副本「明细旧聚合新」内部矛盾与重生成 cwd 默认路径坑（生成器默认相对 scripts/）如实处理。
> - **T2 dialogue_sentiment 口径注记**：实测推翻评审「扩别名」前提——别名表已含佛祖/世尊/释迦牟尼/如来佛祖（utils/aliases.py 单源），如来 58 条为「带引号直引语」口径全集（原文如来系说话模式 51 处+倒装≈口径上限）；落地其有效部分=生成器 data_scope_note 常驻 + 输入源切换分回目录权威路径重生成（total 6565→6547、如来 58→59、孙悟空 3521→3515——系输入文本微差非规则变化）+ site/data/json 字节同步 + dialogue-sentiment.html EMBEDDED sentiment 块整体替换 + 叙述 8 处数字同步 + CSP。
> - **T3 B/C 级性质标注**：评审「C 级 27 文件移出数据目录」撞 W636 冻结裁决（可视化砍到 20 已否决）+86 页口径门禁+B-9 登记不开工——不采纳结构重组，落地弱形式：16 页 cite-block 注入「数据性质」行（9 页趣味向：cave-estate/mbti-evolution/social-media/game-webnovel/narrative-experiment/workplace/famous-time-travel/century-dialogue/ai-dialogue；7 页方法论总结展示：chart-design/visual-art/ethics-consumption/deconstruction/cultural-misreading/methodology-matrix/risk-project）；counterfactual 主数据 A 级排除不标；纯 HTML 文本零样式零脚本（CSP 哈希不涉·token 覆盖率门禁兼容）。
> - **验证**：ruff 全过；verify_delivery 核心全绿（32 槽+37 段锁）；CSP 855 页 0 漂移；生成器自洽断言（明细聚合==by_cause 字段）两副本全过；数据漂移门禁对账过（部署副本与生成器输出一致）。
> - **文件**：scripts/C_情节/hardships_81.py、scripts/B_人物/character_nlp.py、dataset/81-hardships.json、site/data/json/hardships_81.json + dialogue_sentiment.json、site/data/81-hardships.html + dialogue-sentiment.html + 16 页标注、scripts/output/_w668_t3_inject.py（工具存档）、docs/00-导读/W批次编号对账表.md、六文档、四页脚、CITATION、file-index。
> - **状态**：已落地（本批提交并 push origin/main）。

### v2.3.264（2026-10-05）：W662 暗色审计 reader 新页入基线 + 遗漏收敛（W659 蓝图预留批·WP-D2 收官批）
> **来源**：用户「继续」启动 W659 蓝图预留批 W662（§4 实现批拆分末行·WP-D2 收官批）。
> - **暗色审计扩样**（_audit_render_states.js 新增 --prefix 页域过滤·与 --scope charts 叠加可组合）：site/reader 621 页 × S2-desktop-dark 全量实测——fatal=0、isDarkBg=true 621/621（tokens 暗色映射对文本页全部生效）、lowContrast/invisibleShapes/canvasIssues/hOverflow/errors 四类缺陷零命中。
> - **假 0 现场自纠**：首跑误起 8123 端口（脚本写死 8000）→ 621 行全 CONNECTION_REFUSED 且 errors=[] 呈「0 缺陷」假象——以 fatal 行数 + isDarkBg 覆盖双断言识破后 8000 复跑取真数（W569「须起 site 根 http 服务」教训的连接拒绝变体·探针 0 必须配内容在位断言的二度实证）。
> - **基线并入**：render-state-audit-baseline.jsonl 163→784 行（+621 reader·按 page 键去重）；gate compare 只遍历 charts scope 当前输出侧，reader 行不参与比对（并入安全）；本地复验 check_dark_state_gate.js：784 基线/163 当前/零新增 OK。
> - **Screenshot Review 定向**：paths 机制既有（site/reader 触发·W661 实证），本批无页面变更。
> - **遗漏收敛盘点**：sitemap reader 850 条（W660）/搜索索引 reader 615 条（W661）/CSP 855 页 0 漂移/黄金查询 30/30——全 ✓；**WP-D2 六批（W659 规划 + W660/W661/W662 实现）全部收官**；唯一开放项=blob 全量口径 topnav 615 链接是否计入预算（W661 登记待用户裁定·不阻塞后续批次）。
> - **验收机判（蓝图 §4）**：CI 五工作流绿（随本批推送验证）。
> - **文件**：scripts/_audit_render_states.js（--prefix）、scripts/output/render-state-audit-baseline.jsonl（784 行）、scripts/output/render-state-audit.jsonl（charts 163 行当前输出）、docs/00-导读/W批次编号对账表.md（W662 认领+翻转）、六文档、四页脚、CITATION、file-index。
> - **状态**：已落地（本批提交并 push origin/main）。

### v2.3.263（2026-10-05）：W667 复盘三卡防漂移落地 — batch_cascade 预校验 + CLAUDE.md 指针门禁第 32 槽 + doc-sync 扩面评估
> **来源**：用户「全部做完」拍板启动复盘报告 §3.3 三张 skill-creator 任务卡（W667 认领）。
> - **S-01 batch_cascade 预校验**：precheck() 在 dry-run 断言前拦截「能落盘但破坏下一批锚点正则」的 spec——desc 禁 ·；—（写入版本行）、head_sentence 禁 ；—（·实证无害·全角括号既有断言管）、title 须以 batch 领衔；**历史回放校准**：W663 spec 拦截 2 项（正是当年 W664 dry-run 失败的 desc·/head_sentence；肇因）、W664/W666 spec 预检通过。
> - **S-02 CLAUDE.md 指针门禁（第 32 槽）**：check_claude_md.py 四查——C1 指针文件存在 / C2 章节锚点对拍（§N 标题+§N-M 条目）/ C3 行数 ≤60 / C4 正文禁漂移字面量（元信息块血缘行豁免）；--self-test 7/7（含血缘豁免正例）；AGENTS §4.2 补第 32 条目（doc-sync C3 联动·清单 32==槽位 32）；**自洽锁实战抓漏**：新槽漏挂 section 上报被 VERIFY_SECTIONS 当场点名，补挂后 37/37。
> - **S-03 扩面评估**：近 10 批漂移实例 10/10 已有防线、裸露且高频=0 → 不扩面（白名单维持 4 类）；文档规范 §4.9 新增前置纪律句「新增当前态声明须同步纳管（白名单 or 引用式二选一）」；重开触发=下周期裸露实例 ≥1。报告 docs/superpowers/plans/2026-10-05-doc-sync-coverage-evaluation.md。
> - **验证**：ruff 全过；verify_delivery 核心全绿（32 槽+37 段自洽锁）；三份历史 spec 回放判定全对；check_claude_md 实跑 0 FAIL。
> - **文件**：scripts/batch_cascade.py（precheck）、scripts/check_claude_md.py（新增·常驻）、scripts/verify_delivery.py（第 32 槽+自洽锁 37）、AGENTS.md（§4.2 第 32 条目）、docs/superpowers/plans/2026-10-05-doc-sync-coverage-evaluation.md（新增）、docs/00-导读/文档规范.md（§4.9 纪律句）、docs/00-导读/W批次编号对账表.md（W667 认领+翻转）、六文档、四页脚、CITATION、file-index。
> - **状态**：已落地（本批提交并 push origin/main）。

### v2.3.262（2026-10-05）：W661 WP-D2 搜索索引站内化扩量 + footer-meta blob 改链收敛 + blob 预算复核（W659 蓝图预留批·含 W665 chore 版段追记）
> **来源**：用户「开工」指令启动 W659 蓝图预留批 W661（§4 实现批拆分第三行）；W665 chore 版段随本段追记（D2 豁免通道兑现·A-02）。
> - **搜索索引站内化**（_gen_search_index.py）：新增 02-06 五板块映射（people/themes/culture/poetry/essays）+ os.path.exists 回退——docs/02-06 515 条 kind=doc(blob)→kind=reader；docs 676 条终态 reader 615/doc 61（61=README/治理类正确回退）；site/data 与 site/en 双索引重生成（zh 234KB/en 255KB）。
> - **footer-meta 改链**（build_reader.py ①规则）：板块内 README.md「返回本辑」blob→板块目录页 index.html；621 页全量重渲（52 页导航块变化·其余页因 CSP 重注入触达）。
> - **blob 预算复核**：reader 全量 1428（topnav「在 GitHub 查看」源文档外链 615 为刻意源访问入口）；阅读流口径 **813 ≤1000 达标**；全量口径 1428>1000——topnav 是否计入预算属口径裁定，随批报请用户（blueprint 验收行未定义计数口径）。
> - **CSP**：generate_csp 重注入 623 页（reader 重渲后 CSP meta 恢复+search.html 数据块哈希更新）·855 页 0 漂移。
> - **验收机判（蓝图 §4 三条）**：黄金查询 30/30 ✓；lint_links reader 域 8818 链接 0 broken ✓；blob 阅读流 ≤1000 ✓。verify_delivery 核心全绿。
> - **W665 追记**：chore(w665)（1650aa4·review-fix 三处）版段随本段补录——对账表 W665 行版段列同步 v2.3.262。
> - **文件**：scripts/build_reader.py、scripts/_gen_search_index.py、site/data/search.html、site/en/search.html、site/reader/ 621 页、docs/00-导读/W批次编号对账表.md、六文档、四页脚、CITATION、file-index。
> - **状态**：已落地（本批提交并 push origin/main）。

### v2.3.261（2026-10-05）：W666 工作复盘与优化分析报告（W663-W665 周期）入库 + 方法论 README 索引 28
> **来源**：用户指令按「工作复盘与优化分析系统提示词（AI Agent 专用版）」对 W663-W665 周期出标准化复盘报告并入库（循 W660 追加批先例）。
> - **报告**：docs/10-方法论沉淀/工作复盘与优化分析报告-2026-10-05.md（296 行·元信息块 v2 齐备）——七维度全覆盖：经验复用 7 项综合得分排序（doc-sync 反向对拍 4.75/负样本自证 4.75/移植方案体例 4.5/指针化零漂移 4.5/对账表认领 4.25/review 保真度地图 4.25/CRLF 行级纪律 4.0）；技能矩阵按筛选规则 **0 命中**（最低效果 4 分），按「新立机制试运行护航」原则立 3 张预防性 skill-creator 任务卡（S-01 batch_cascade spec 预校验/S-02 CLAUDE.md 指针校验第 32 槽/S-03 doc-sync 扩面评估——**均待用户拍板启动**）；未用技能 4 项三态决策（引入 skill-creator/暂缓 dynamic-workflows·judge_gate/放弃 de-AI 三技能）；场景沉淀 3 项已落地；问题 10 例（P2×6/P3×4·流程 40% 文档 20% 工具 20% 环境 20%）全闭环，历史 P0/P1 家族 0 复发；工作流瓶颈=Screenshot 等待，定向截图已实测减 57%（21m13s→9m3s）；WBS 六项挂靠对账表批号。
> - **验证**：报告全部数字取自 git log/CI 运行记录/门禁输出实测；4 组【假设】+1 组【待验证】显式标注（A-1 verify 耗时/A-2 接手成本/A-3 skill-creator 消费力/A-4 频率外推）；verify_delivery 核心全绿；方法论 README 索引 28 行在位。
> - **文件**：docs/10-方法论沉淀/工作复盘与优化分析报告-2026-10-05.md（新增）、docs/10-方法论沉淀/README.md（索引 +1 行）、docs/00-导读/W批次编号对账表.md（W666 认领+翻转）、六文档、四页脚、CITATION、file-index。
> - **状态**：已落地（本批提交并 push origin/main）。

### v2.3.260（2026-10-05）：W664 CLAUDE.md AI 速查层 + 文档规范 §4.9 写作可验证纪律（宿主自动加载·指针化零漂移设计）
> **来源**：用户拍板建 CLAUDE.md——W663 三仓治理评阅的收尾动作；本条纪律的落点经两轮讨论裁决（生效时机决定位置：自动加载层收速查入口，正文权威归文档规范写作规则章，AGENTS.md 保持 SOP 操作层不加节）。
> - **CLAUDE.md（新建·39 行 ≤60 上限）**：必守规则速查 10 条（每条一行+权威指针：E1/写作纪律/现役口径/CSP/结构平衡/file://引文探针/级联并发对账/commit 规范/禁擅改）+ 常用命令 5 条 + 环境注意 4 条 + 接手导航；**禁写会漂移的数字与现役值**（无版本号/无计数/W 区间字面量——零逐批维护成本）；维护契约三条（新规则先落权威层再登记一行/每次改动复核指针目标/行数上限 60）。
> - **验收（按 §4.9 自身标准）**：指针逐条 grep 实证 15/15 过；正则抽查无 v2.3.x 现役字面量、无 W001-Wxxx 区间字面量；行数 39≤60。
> - **文档规范 §4.9 写作可验证纪律（正文唯一权威）**：总判据=读者无需额外解释即可准确理解与复算；禁词清单（适当/尽快/酌情/相关/必要时/尽量）；验收标准含期望输出+负样本自证；交付文档头五要素自包含；数字当批现测；正反例各 1。
> - **锚点**：AGENTS.md §3 目录树 / §7 上手第 1 步 / §8 权威文档行 + STRUCTURE.md 顶层结构表 + 对账表 W664 认领行。
> - **验证**：verify_delivery 核心全绿（31 槽+36 段自洽锁）；doc-sync 0 FAIL；CLAUDE.md 指针 15/15；级联 dry-run 断言全过。
> - **文件**：CLAUDE.md（新增）、docs/00-导读/文档规范.md（§4.9）、AGENTS.md（三处锚点）、STRUCTURE.md（顶层表行）、docs/00-导读/W批次编号对账表.md（认领+翻转）、六文档、四页脚、CITATION、file-index。
> - **状态**：已落地（本批提交并 push origin/main·CI 实跑见 gh run list）。

### v2.3.259（2026-10-05）：W663 治理经验移植批 — W 批次编号对账表 + doc-sync 口径体检第 31 门禁 + verify 段计数自洽锁 + CI 加固 61 处 SHA 钉（含 W659-W660 追记合并登记·D1 裁决）
> **来源**：W659-W663 三批合并登记（D1 裁决·追记于 W663——w659/w660 提交先于版段落库、CHANGELOG 曾 0 登记的现状经 W663/T1 对账表可见化，本段一次性补录）；W663 为 GateKeeper / 绿洲共享田园 / 千问办公大赛三仓治理评阅的反向移植批（方案 docs/superpowers/plans/2026-10-05-governance-experience-transplant-plan.md·D1-D3 经用户 2026-10-05 裁决）。
> - **W659（d733e1a）**：WP-D2 阅读器扩量启动规划批——实施蓝图入档（六板块映射 + 520 篇实测 + 链接形态普查定稿 + 实现批拆分 W660/W661/W662·验收机判表）。
> - **W660（a8c0e47 + 288b0cb + fc14592）**：WP-D2 阅读器扩量实现——520 篇 reader 页落地（02-06 五板块·build_reader 多板块映射驱动）+ sitemap 850 条 + lastmod UTC 跨日修正 + 工作复盘与优化分析报告入库（W648-W660 全周期）。
> - **W663/T1（b1aafb0 立项 + 5b6d410）**：docs/00-导读/W批次编号对账表.md（W648-W663 全行 hash 实证·并发认领规则三句·下一自由号标尺）+ 交接「八」雷区索引化 13 行 + 新增条目「验证：」字段纪律（权威源文档规范 §11.5）+ AGENTS §4.3 / CHANGELOG 契约④ 锚点。
> - **W663/T2（16ededf）**：doc-sync 文档口径体检挂**第 31 门禁**（scripts/check_doc_sync.py·四类窄句式反向对拍——C1 README 抬头 / C2 交接头链 / C3 门禁清单上限 / C4 近 15 提交 W 号 ⊆ 版段 ∪ 对账表登记（D2：登记即豁免）；行级 exempt 标记·浅克隆跳过 C4·--self-test 7 例）；首跑捕获 C3 一处（AGENTS §4.2 清单止于 28 vs 实况 30）修复至 0 FAIL 并补录 §4.2 第 29/30/31 条目；留证 scripts/output/doc-sync-first-run.md。
> - **W663/T3（763ea94 + e6d9f59）**：verify_delivery 门禁段计数自洽锁 VERIFY_SECTIONS——EXPECTED_SECTION_NAMES 36 项 + 每段 section() 上报 + 收尾缺段断言（负样本实测：注释任一上报行必红并逐名点名）；坑 #14 入册（恢复备份吞噬改动·cmp 须对改动后快照）。
> - **W663/T4（b14b64b）**：CI 加固——5 个 workflow 61 处 uses 改 commit SHA 钉（git ls-remote 实测·「@SHA # vN」注释式·改写器 _w663_t4_shapin.py 复核 0 残留）+ 顶层 permissions: contents: read 收敛 4 文件（CodeQL job 级提权保留）+ security.yml 补 workflow_dispatch。
> - **验证**：verify_delivery 核心全绿（36 段自洽锁 + 31 槽）；check_doc_sync --check 0 FAIL / --self-test 7/7；ruff 0 错；workflow YAML safe_load 5/5；SHA 钉残留复核 0；负样本两组（自洽锁缺段 / doc-sync 改值）实测必红、恢复必绿。
> - **文件**：docs/superpowers/plans/2026-10-05-governance-experience-transplant-plan.md（新增）、docs/00-导读/W批次编号对账表.md（新增）、scripts/check_doc_sync.py（新增·常驻）、scripts/verify_delivery.py（第 31 槽 + 自洽锁）、scripts/output/doc-sync-first-run.md（新增留证）、scripts/output/_w663_t3_inject.py 与 _w663_t4_shapin.py（工具存档）、.github/workflows/ 5 yml、六文档、四页脚、CITATION、file-index。
> - **状态**：已落地（本批提交并 push origin/main·CI 实跑见 gh run list）。

### v2.3.258（2026-10-04）：W658 B-7 分析方法 pip 包 0.1.0 — xiyouji-analysis（32 自包含脚本+CLI list/run/run-all+同步机制）venv 全链路冒烟 + setuptools build 缓存混包抓取
> **来源**：全量启动队列第八批——B-7 按 registry 启动注记（「解耦与打包开工」）执行；解耦担忧经普查大幅收窄：37 个分析脚本仅 5 个耦合仓库语料（utils/+source//dataset/·jieba），32 个自包含纯 stdlib——**0.1.0 正确边界=只收 32 个零修改入包**，5 个排除登记（参数化留 0.2）。
> - **包**：packaging/xiyouji-analysis/（pyproject+README+src/xiyouji_analysis/{__init__,cli}.py）——脚本以仓库原样分发（类目结构保留·零修改）；CLI `xiyouji-analysis list|run <类目/脚本>|run-all`（subprocess 透传 --output·与仓库「py 类目/xxx.py --output」用法同构）。
> - **同步机制**：scripts/package_analysis_sync.py（单一事实源 scripts/→包 analyses/·非 _ 前缀·COUPLED 5 个排除+manifest 登记·--check 幂等核验）。
> - **冒烟（venv 全链路）**：install→list=32→run G_哲学/philosophy OK→run Q_源流演变/text_evolution OK→输出 8 JSON 结构有效→wheel 构建成功→临时件清理。
> - **过程抓取两个包工程坑（入册）**：①importlib.resources 对无 __init__ 目录返回 MultiplexedPath（Windows os.listdir 炸）→改 Path(__file__) 相对定位；②**setuptools build/ 目录缓存混入旧拷贝**（删 5 个 coupled 后 wheel 仍 37 个·--no-cache-dir 无效·必须删项目 build/ 目录）——README 已写警示。
> - **验证**：ruff 0 错；sync --check 幂等；venv 冒烟全链路过；包边界核验（32 入/5 排除/0 残留）。
> - **文件**：packaging/xiyouji-analysis/（pyproject.toml、README.md、src/xiyouji_analysis/__init__.py、cli.py、analyses/ 32 脚本）、scripts/package_analysis_sync.py（新增·常驻）、scripts/output/_sync_analysis_manifest.json、六文档、四页脚、CITATION、file-index。
> - **状态**：已落地（本批提交并 push origin/main）。

### v2.3.257（2026-10-04）：W657 B-6 第二步可引用性组件 — 86 页 cite-block 静态注入（数据源+APA/BibTeX+下载）+ cite-box.js 交互模块 + 第 28 门禁基线 327→0 全量收紧（C1-C4 86/86·D4 兑现·转全量 FAIL 模式）
> **来源**：全量启动队列第七批——B-6 第二步按 registry 启动注记（用户 2026-10-03「全部启动」·免另立 PRD）执行：86 页引用组件（APA/MLA/BibTeX 复制）+ 导出。
> - **静态注入（_w657_cite_inject.py）**：81 页 append-to-dataSource / new-dataSource + 5 页 body 后新建（view/explorer/search 五特殊页无 dataSource 区与 noscript）——块内容全部真实信息零编造：数据源（fetch 页=json/xxx.json 路径·EMBEDDED 页=内嵌数据声明+scripts/run_all.py 批量生成入口+「快照 2026-10-04」）+ 引用格式 details 折叠（默认收起视觉零扰动·APA 与 BibTeX 预生成文本·title/canonical 从页面提取）+ fetch 页 a[download] JSON 下载入口。
> - **交互模块 cite-box.js**（src 挂载 86 页·W656 同款形态）：复制按钮事件委托（navigator.clipboard 优先·file:// execCommand 降级·2s 反馈）+ token 样式动态注入（零裸色·覆盖率门禁合规·details 收起不动 W550 验收面）；无组件页零开销。
> - **第 28 门禁基线全量收紧（D4 兑现）**：注入后 86 页 C1/C2/C3/C4 四项全过（86/86）——基线 missing 327→0（--generate-baseline 重生成 344 行全 ok）·门禁转全量 FAIL 模式（未来任何页缺任一项即红·零豁免）；W638「存在性对≠分级对」教训闭环：本次是真实修复后的收敛非判据放宽。
> - **验证**：ruff 0 错；check_citability gate 基线外 0·可收紧 0；第 29/30 门禁与 verify 核心全绿；playwright 探针（citeBox 在位/2 复制按钮/details 可展开/cite-box.js 加载执行/零 pageerror）；CSP 不涉（无内联脚本改动·cite-box 为 src）。
> - **文件**：site/static/js/cite-box.js（新增）、site/data 86 页（cite-block 注入+cite-box 挂载）、scripts/output/citability-baseline.txt（刷新 0 missing）、scripts/output/_w657_cite_inject.py（工具存档）、scripts/output/_cascade_files_W657_pages.txt、六文档、四页脚、CITATION、file-index。
> - **状态**：已落地（本批提交并 push origin/main）。

### v2.3.256（2026-10-04）：W656 B-9① audit 六族补丁合并单模块 — chart-audit.js（src 加载+data-families 传参·84 页净删 20524 行）+ 等价性探针五页逐数一致 + file:// 直开验证
> **来源**：全量启动队列第六批——B-9① 按 registry「audit-* 六族补丁合并为单模块渲染后一次执行（85/86 页分布）」执行。
> - **模块**：site/static/js/chart-audit.js——六族合并（axisfix 底轴旋转/axesvar 方差判轴/avoidall 全标签防重叠/numfix 数值优先/netlabels 网络标签/content 热力旋转）；**axisfix2 与 axisfix3 逐字节同逻辑仅 domain 守卫差·合并为无守卫版（=原 axisfix3 终态超集·同 800/2600/5000 时序一次执行·运行时全页扫描减半）**；隐藏型四族统一 svg[data-audit-skip] 豁免（W553 机制·原仅 monster-female-network 变体携带·旋转型不识别守卫沿 W553 决议维持 W550 已验收外观）；window.ChartAudit.run 手动 API+__avoidOverlap 兼容保留（现网 0 消费方）。
> - **接入形态（关键裁决）**：84 页七块补丁（230-300 行/页）→ **1 行 defer src+data-families 传参**——d3 同款 src 形态（file:// 与 Pages 双态三年验证·vis-tools「内联避 404」注释系特殊预览服务器根的历史遗留非 file:// 约束）；currentScript 读 data-families（defer 时序：DOM 解析完执行·早于 load·家族时序表内 setTimeout 语义不变）。**净删 20,524 行**（84 页 +186/-20710·平均 244 行/页——registry「省 300-500 行」以 src 形态兑现·内联形态实测反而 +31 行/页已否决）。
> - **等价性验证（本批生命线）**：playwright 探针五页（标准五族/netlabels/热力 content/skip 变体七族/var 化页）DOM 终态 before/after 逐数一致（rotatedTicks/hiddenTexts/hiddenNoTitle/heatRotated）；file:// 直开探针 rotated 39 一致；pageerrors 全程 0。过程抓取一次 CSP 未重发致模块被静默拦截（探针 ChartAudit undefined+零 pageerror 定位·AGENTS 铁律「改内联脚本必跑 generate_csp」连等价探针都被坑的现场实证——src 形态根治此类风险）。
> - **验证**：node --check 模块+check_js_syntax 334 文件过；lint_links 1917 链接 0 broken（src 引用存在性）；第 29/30 门禁与全 verify 核心绿；CSP 重生成（84 页哈希表缩减）；drift 门禁绿。
> - **文件**：site/static/js/chart-audit.js（新增·单一事实源）、site/data 84 页（七块→1 行 src）、scripts/output/_w656_replace_audit.py 与 _w656_src_tag.py 与 _w656_equiv_probe.js（工具存档）、scripts/output/_cascade_files_W656_pages.txt（页面清单）、六文档、四页脚、CITATION、file-index。
> - **状态**：已落地（本批提交并 push origin/main）。

### v2.3.255（2026-10-04）：W655 B-9② D3 字面色值→CSS 变量 — 405 处 var 化（46 页·attr→style 230+style→var 175）+ 暗块补 chart 系列暗值 4 行（对齐 accent 暗值零新色）+ 全量暗色审计
> **来源**：全量启动队列第四批（依赖序：PD-5 design-tokens.json 真值已就位·PD-1 触页批已错批）——B-9② 按 registry 登记「D3 字面色值改读 CSS 变量·删暗色 fill 硬编码映射」执行。
> - **转换**：405 处 var 化（attr→style 230 + style 字面量→var 175·触及 46 页）——赋值语境（.attr/.style 的 fill/stroke/color）精确匹配 design-tokens light 值（大小写不敏感）→ var(--token)；chart-N 同值令牌优先用于 fill/stroke（系列语义）·color 语境用语义令牌（accent/ink）。**attr→style 转换为必要形态**：SVG 表现属性不支持 var() 替换——这正是 140 条属性选择器映射存在的历史根因。
> - **暗块补系列暗值 4 行**：--chart-1 #E0604F/--chart-2 #7FA8C9/--chart-4 #9DB98A/--chart-6 #C9A96B（全部对齐既有 accent 系暗值·零新色发明·W587 亮度规则核算 chart-2 L=0.133 需提亮/chart-1 0.170 与 chart-6 0.167 边界一并对齐）；chart-3/5 亮度可读（0.385/0.629）继承不覆写。
> - **映射清理实况（如实）**：140 条属性选择器映射本轮删除 0 条——余下映射的 literal 仍以运行时形态存在（colorMap/EMBEDDED 驱动的属性赋值·删则破坏那些图的暗色渲染）；其退场路径=相关页色板 token 化（B-5/B-6 后续批）·非本批一刀切。
> - **暗色审计**：86 页×4 态全量（_audit_render_states·W584 并行化）——invisible/lowContrast/缺陷页 0（var 化+暗值对齐后三态零回归）。
> - **验证**：ruff 0 错；色盲门禁基线外 0（存量 17428→17417·转换消解 11 对·var 解析路径语义不变）；drift/第 26-30 门禁全过；verify_delivery 核心全绿；CSP 重生成 0 漂移；inline_css --force 327 页重分发。
> - **文件**：site/tokens.css（暗块+4）、site/data 46 页（var 化）、scripts/output/design-tokens.json 与 docs/00-导读/design.md（97 键重导出）、scripts/output/_w655_literal_to_var.py（转换脚本存档）、六文档、四页脚、CITATION、file-index。
> - **状态**：已落地（本批提交并 push origin/main）。

### v2.3.254（2026-10-03）：W654 PD-1b 图表选型章与降级门禁 — DESIGN.md §4B 九族 45 格（并行会话实现·本批接续收尾）+ check_chart_degrade 挂第 30 槽（86 页 chart-degrade 声明全落）+ check_chart_data R3/spec-check/自检 6 例 + R3 力导向签名补自定义力布局 + B-5 聚合器与 entities 两 JSON 同批入账
> **来源**：全量启动队列第三批（依赖序：PD-5 真值→PD-1a 色盲门禁已就位）——PD-1b 按适用性方案 §3 执行；并行会话已完成 §4B 选型章与 check_chart_data 主体（未提交·本批接续收尾并同批入账，跨批协作二次实践）。
> - **DESIGN.md §4B 图表选型与数据契约**（D-2 裁决 (a) §4A 插章先例）：9 族 × 5 字段（数据形态约束→图型→禁用条件→站内代表页→窄屏降级方案）45 格零空格（AC-4：--spec-check 表体行 9·空单元格 0）；每格锚真实页面（git ls-files 核对）。
> - **第 30 门禁挂载**：check_chart_degrade.py（静态解析不启浏览器·D-5 只 site/data 86 页·_shell/_template 跳过同口径）——页内 `<!-- chart-degrade: stacked|scroll-x|simplified|n/a -->` 声明缺失/非法=FAIL；86 页声明按 §4B 族签名推导全落（stacked/simplified/scroll-x/n-a 按视觉主导族）·wrapper 防静默跳过同前（AC-3 未声明页==0）。
> - **check_chart_data 扩充**：R3 措辞×实现错配（§4B 词表联动·辖区 site/data·自定义实现以关键词在位为准）；--spec-check 子命令；--self-test 3→6 例（R1/R2/R3 负样本+好样本+R3 正样本）。**R3 首跑抓 2 页真错配并同批处置**：graph-explorer/character-relationship-3d 页面写「力导向」但无 d3.force 签名——诊断为手写迭代力布局（nodePos/iters 收敛/velocity 积分·非 d3.force），R3 力导向实现签名补自定义力布局标记（nodePos|iters=）后两页正确识别为力导向（非误报非漏报）。
> - **B-5 聚合器先行同批入账**：scripts/agg_entities.py 读 docs/01 100 回 chapter-meta 注释 → dataset/entities/characters.json（56 名·悟空 96/唐僧 92/沙僧 76）+ locations.json（61 处）——100/100 覆盖断言·纯聚合零新造事实·不做别名归并（学术裁决面）·drift 门禁绿（未被 fetch 的新文件不触发 47 副本基线）。
> - **AC 对照**：AC-1 扫描 86==N-DATA ✓；AC-2 self-test 6/6 ✓；AC-3 未声明 0 ✓；AC-4 行 9 格 0 ✓；AC-5 verify 核心全绿+两新门禁在输出 ✓；AC-6 CSP 335 页 0 漂移（页改动仅 HTML 注释·非渲染面）✓；AC-7 暗色——页改动为零渲染面注释（bite-level 论证）·CI Screenshot Review 定向截图兜底 ✓。
> - **验证**：ruff 全部 0 错；check_chart_data 三模式（gate/spec-check/self-test）全过；check_chart_degrade 86/86 声明；verify_delivery 核心全绿（第 29/30 门禁实测）；级联 dry-run→apply 10 面断言过。
> - **文件**：DESIGN.md（§4B）、scripts/check_chart_data.py（R3/spec-check/自检）、scripts/check_chart_degrade.py（新增）、scripts/verify_delivery.py（挂第 30 槽）、site/data 86 页（chart-degrade 声明注释）、scripts/agg_entities.py、dataset/entities/characters.json、dataset/entities/locations.json（B-5·均新增）、scripts/output/_cascade_files_W654.txt、六文档、四页脚、CITATION、file-index。
> - **状态**：已落地（本批提交并 push origin/main）。

### v2.3.253（2026-10-03）：W653 PD-1a 图表配色色盲安全门禁 — check_chart_colorblind（Machado 二型模拟+CIEDE2000·ΔE<10·WARN+基线 17428 对冻结）挂第 29 槽 + 形态普查 + 口径偏差入账（light 静态·暗色归 PD-4）
> **来源**：全量启动队列第二批（依赖序：PD-5 真值清单已就位）——PD-1a 按适用性方案 §3 执行（PD-1b §4B 选型章+降级门禁+R3 留 W654）。
> - **门禁**：check_chart_colorblind.py 挂 verify_delivery 第 29 槽（wrapper 防静默跳过同前两门禁：crash 即拦+汇总行校验）——Machado et al. 2009 deuteranopia/protanopia 矩阵（sRGB 线性域）+ CIEDE2000 纯 stdlib 实现；页内系列色板两两求 min(ΔE_deuter, ΔE_protan)<10 判违规；D-6 裁决 WARN+基线冻结（colorblind-baseline.txt·17428 对·1,059,178B）·基线外新增 FAIL·收敛后转 FAIL 不预设日期。
> - **形态普查**（先于正则·AGENTS 第 28 项教训）：colorblind-survey.json——86 页色值书写变体 hex 22334/rgb 7915/hsl 0/var 28605/d3.scheme 2/渐变 stop 0。
> - **抽取口径三轮迭代**（普查实证驱动）：v1 全赋值语境→命中面失控（EMBEDDED_DATA 生成期节点色混入·单页色板 190）；v2 剔除 EMBEDDED 数据块+ΔE<3 聚类去重→仍 86/86 页超阈豁免失效；v3 定稿四族系列色板（chart 变量/d3 scheme/colorMap 字面映射/fill-stroke 赋值·不含 color: 文本色）——UI 修饰色不入系列色板（色盲安全是数据系列问题）。
> - **口径偏差入账（计划最高风险项的规避）**：静态解析限定 light 主题真值——暗色 computed 态色盲检查需 http 渲染（W589 口径），归 PD-4 异常态矩阵，本门禁输出注明口径。
> - **首跑发现（入 PD-1b 选型章语料）**：86/86 页坍缩后仍有 25-30 族——本语料图型以高基数分类网络与连续色阶为主（66 页 scale 豁免+20 页多分类全检），ΔE 成对检查在颜色维度对高基数页不构成可行动约束，其色盲安全抓手=交互编码冗余（形状/标签）而非换色；代表性真违规对：W334 色板 --chart-1 朱砂×--chart-4 苔绿 ΔE=7.9（deuter）已在基线冻结。
> - **性能**：模拟态 Lab 预计算缓存（每色每模拟一次·配对复用）——全量分析 4.7s（verify 120s 超时内）。
> - **验证**：ruff 0 错；--self-test 4/4（好坏/中性/连续色阶豁免构造页）；基线冻结后 --gate 基线外违规 0；verify_delivery 核心全绿（第 29 槽含汇总行校验实测）；级联 dry-run→apply 10 面断言过。零页面改动·暗色态无回归面（AC-7 由 W650 已绿基线承接）。
> - **文件**：scripts/check_chart_colorblind.py、scripts/verify_delivery.py（挂第 29 槽）、scripts/output/colorblind-baseline.txt（新增·冻结）、scripts/output/colorblind-survey.json（新增·普查）、scripts/output/_cascade_files_W653.txt、六文档、四页脚、CITATION、file-index。
> - **状态**：已落地（本批提交并 push origin/main）。

### v2.3.252（2026-10-03）：W652 PD-5 设计令牌机器可读导出 + 文档对账门禁 — design-tokens.json（93 键·DTCG 简化·B-9② 前置真值）+ docs/00-导读/design.md（机器生成）+ check_design_doc_drift 五层检查挂 verify + DESIGN.md §2.1 六处值漂移同步
> **来源**：全量启动队列第一批（依赖序首位·纯只读不改页·先于 B-9② 色值→变量拿真值）——PD-5 按适用性方案 §3 详规与 §10.1 批复（D-4 落 docs/00-导读·D-5 只 site/data）执行。
> - **导出器**：scripts/export_design_tokens.py 解析 site/tokens.css（按「;」切分声明·一行多声明兼容·尾注释捕获为 $description·选择器推断主题 :root=light/html[data-theme=dark]=dark·节注释为 group）→ scripts/output/design-tokens.json（W3C DTCG 简化：93 键=声明 93·light 69/dark 24·$value/$type/$description+group/line）+ docs/00-导读/design.md（按主题/节分表·D-4 裁决落位）。--check-count=AC-1（93==93 PASS）。
> - **对账门禁**：check_design_doc_drift.py 五层全机判——①反篡改（design.md 再生成逐字节比对·文档不含生成日期等易变字段保证长期成立）②覆盖（CSS 声明在 design.md 全记载==0 缺）③虚构（design.md 与 DESIGN.md §2 令牌名必须在 CSS ∪ 站点页面本地声明中存在·W610 先例·页面本地 95 名按 AC-2 白名单条款放行）④值同步（DESIGN.md §2 手写表 light 值↔CSS 主题感知比对）⑤暗色计数（JSON dark==CSS dark）。挂 verify_delivery（无编号·wrapper 防静默跳过与第 28 门禁同款：crash 即拦+汇总行校验）。
> - **首跑实证并已同步**：DESIGN.md §2.1 六处值漂移（--ink #2c2418→#23201A·--ink-soft #6b5e4d→#6B6455·--accent-3 #7a5230→#8A6D3B·--accent-4 #5a7a3a→#6B8E5A·--line #d9cdb8→#E5DFD0·--shadow 旧 rgba(60,40,20)→现行 rgba(35,32,26)+--bg 大小写统一）——正是「源-副本一致性缺口族」活样本（W577 P1 根因同类）；§2.2 的 15 个 badge/focus/cross-table 令牌为 dashboard.html 页面本地定义（非虚构·白名单放行）。
> - **AC-4/AC-5**：design-tokens.json json.tool 有效；check_inlined_css 224 页完整+generate_csp 0 漂移（只读批零变化实证）。
> - **验证**：ruff 三脚本 0 错；AC-1…AC-5 全过；verify_delivery 核心全绿（新门禁含汇总行校验实测）；级联 dry-run→apply 10 面断言过。
> - **文件**：scripts/export_design_tokens.py、scripts/check_design_doc_drift.py、scripts/verify_delivery.py（挂载）、scripts/output/design-tokens.json、docs/00-导读/design.md（均新增）、DESIGN.md（§2.1 同步）、scripts/output/_cascade_files_W652.txt、六文档、四页脚、CITATION、file-index。
> - **状态**：已落地（本批提交并 push origin/main）。

### v2.3.251（2026-10-03）：W651 全量启动裁决入档 — B-5/B-6 第二步/B-7/B-9①②/WP-D2/WP-E 六项启动（用户「全部启动」·排除 Docker 验证与 B 轨《装饰》投稿）+ PD 档 D-1…D-7 批复 + Traffic API 快照机制首采 + master plan/交接陈旧状态修正
> **来源**：用户盘点「记录了但没做」全清单后裁决「全部启动·不做 Docker 和 B 轨《装饰》投稿」——本批为启动裁决入档+快速项落地，工程批次按依赖序随后展开（PD-5→PD-1→B-9②→B-9①→B-6 第二步→B-5→B-7→WP-D2→WP-E）。
> - **六项启动**：B-5（聚合器先行·扩字段与学术梯队随批）、B-6 第二步（86 页引用组件+PNG/SVG 导出·免另立 PRD）、B-7（脚本解耦+pip 打包）、B-9①（audit-* 六族补丁合并）、B-9②（D3 色值→CSS 变量·先决核查 --ink-faint 扫描口径）、WP-D2/WP-E（reader 扩量 515 篇+发现架构——工程呈现层非内容生产·用户点名解除 W626 冻结）。registry 四行+master plan §8.3 两行启动注记。
> - **明确排除**：Docker 镜像验证、B 轨《装饰》投稿（用户点名不做）；WP-B-ALT 维持冻结（触发条件未满足·部署需用户平台与密钥决策）；B-8 hardships 重分类维持待作者学术裁决。
> - **PD 档 D-1…D-7 批复**（用户「全部启动」总批复·落档内默认项）：D-1 (b) 口径行维持+差额查因并入 PD-1a；D-2 (a) §4B 插章；D-3 (a) 2 页；D-4 (a) docs/00-导读；D-5 (a) 只 site/data；D-6 (a) WARN+基线；D-7 (a) PD-1…PD-5 按 §7 队列开工。已记入 PD 档 §10.1。
> - **Traffic API 快照机制首采**：scripts/_traffic_snapshot.py 新增（gh api 四端点·14 日窗防过期不可回溯）+ 首采 scripts/output/traffic-snapshots/traffic-snapshot-2026-10-03.json（views 5/4·clones 2623/231·referrers Nothing to display 与后台一致）。
> - **master plan/交接陈旧修正**：§8.3 WP-A 行 🔄→✅（W626 终态回写·原系回写滞后）；交接文档两笔陈旧勾选补 [x]（agent-web 迁移 W543-W548 已完成+走查关闭；真实读者量验证 W425/W426+W626 已完成）。
> - **验证**：快照脚本实跑出盘；verify_delivery 核心全绿；级联 dry-run→apply 10 面断言过。
> - **文件**：scripts/_traffic_snapshot.py（新增）、scripts/output/traffic-snapshots/traffic-snapshot-2026-10-03.json（新增）、PD 档（§10.1）、registry（四行）、master plan（三行）、交接文档（两笔）、六文档、四页脚、CITATION、file-index。
> - **状态**：已落地（本批提交并 push origin/main）。

### v2.3.250（2026-10-02）：W650 第 28 门禁三项加固（C2 判据收紧+基线刷新·wrapper 防静默跳过·docstring 校正）+ PRD 移出公开仓库（真名防泄漏·用户裁决）+ workflows README 累积链瘦身
> **来源**：W649 落地后全量审查（用户发起）发现一项 P1 与四项小项，用户裁决处置——PRD 整份移出公开仓库 + 四项全修。
> - **P1·PRD 出库**：W649 入库的两份第 28 门禁 PRD（_dev 副本+plans 权威版）含项目 Owner 真实姓名，系全仓首次出现（此前 CITATION.cff/LICENSE/git 作者均刻意不用真名）——`git rm --cached` 出库+gitignore（W620 出库先例）·本地文件保留·registry 引用改「本地留存未入公开仓库」说明。git 历史仍含（f5b20ea 已公开·不可变），当前文件面已清。
> - **C2 判据收紧**：路径含子目录不再视为「有参数/口径说明」，须命中参数提示词（生成/参数/口径/阈值/样本/语料/模型/权重/归一）——否则仅写裸脚本路径的页假通过；实测翻转 1 页（hardship-heatmap）→ 基线刷新 missing 326→327（C2 9/86→8/86）·门禁绿·self-test 6/6。
> - **wrapper 防静默跳过（对齐 W631）**：verify_delivery 第 28 门禁执行异常由 WARN 升 FAIL（crash 即拦不静默放过）+ exit 0 但输出缺「---- 第 28 门禁：」汇总行判 FAIL（防未真正扫描的空真）。
> - **docstring 校正**：check_citability.py 头部自检说明「4 负样本+1 正样本」→「6 例：4 负样本+1 正样本+1 构建工具回归」（与实际用例数对齐·W649 审查发现）。
> - **workflows README 累积链瘦身**：级联每批追加的「无 workflow 结构改动」链已膨胀至 5590 字符（150+ 批挤一行）——重写为实质批次清单（git log 排除 README.md 实测仅 W523/W536/W563/W571/W578 五批实质改动 workflow 文件+W464 perf 基线单列）+「其余各批无 workflow 结构改动·明细见 CHANGELOG」；级联三锚点（W450-W 前缀/单次 marker/首行版本）全保留实测兼容。
> - **验证**：ruff 0 错；check_citability --self-test 6/6；基线刷新后 --gate 基线外违规 0；verify_delivery 核心全绿（第 28 门禁含新汇总行校验）；级联 dry-run→apply 10 面断言过。
> - **文件**：scripts/check_citability.py、scripts/verify_delivery.py、.gitignore、docs/superpowers/plans/2026-09-30-maintenance-backlog-registry.md、.github/workflows/README.md、scripts/output/citability-baseline.txt（刷新）、citability-report.json（刷新）、两份 PRD（出库·git rm --cached）、scripts/output/_cascade_files_W650.txt、六文档、四页脚、CITATION、file-index。
> - **状态**：已落地（本批提交并 push origin/main）。

