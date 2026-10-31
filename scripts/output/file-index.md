# xiyouji 文件反向索引

> 与 [CHANGELOG.md](../../CHANGELOG.md) 配套：给定文件，查它被改过几次、每次对应哪个 W 条目。
> W### 编号规则见 CHANGELOG.md 顶部。
> 创建于 2026-07-22（v0.8 双索引改造）
>
> **历史归档**：W031-W087（v2.0.4-v2.0.60）site/data/ 部分已迁移至 [file-index-ARCHIVE.md](../../archive/docs/file-index-ARCHIVE.md)；W422 再归档 W393-W416 段；W511 归档 W417-W448 段 + W449-W463 损坏区尾部清理。W736 归档 W449-W699 段（与 CHANGELOG 现役边界统一至 W700）。本文件正本按 110 段窗滚动（W960 窗口制·正本最老段随批推进）。
>
> **维护契约**：本索引按 W 追加登记（每文件 1 行 + 一句摘要），历史段禁改；新增/变更文件必须先有 CHANGELOG 对应 W 段再登记（双索引铁律），禁止无 W 段单独登记。

---

## W1068 触发面补漏批 + paths 自我纠正 + 方法论篇 + tmpe 清场批（2026-10-31）

| 文件 | W | 说明 |
|---|---|---|
| docs/10-方法论沉淀/CI提速与门禁健壮性方法论.md | W1068 | 本批新增（方法论深度篇·提速四步序 + 判据自证 + action ref 红线 + paths 过滤陷阱 + 收官自查清单） |
| docs/10-方法论沉淀/README.md | W1068 | 本批修改（方法论索引登记第 28 行） |
| docs/agent/pitfalls.md | W1068 | 本批修改（新增 E-83 schannel TLS 指纹 / E-84 paths 过滤不得缩小验证面·流程组 81→83·含对 W1066 批登记建议的自我纠正） |
| .github/workflows/screenshot-review.yml | W1068 | 本批修改（paths 补 check_contract_smoke.js / check_screenshot_gates.js ⇒ 改了门禁脚本也会触发门禁） |
| .github/workflows/workflow-lint.yml | W1068 | 本批修改（paths 收窄到 .github/workflows/** + 判据脚本·其覆盖面本就是工作流文件自身） |
| AGENTS.md | W1068 | 本批修改（坑表条数计数链同步 + 级联脚注滚动） |
| HANDOVER.md | W1068 | 本批修改（坑表条数计数链同步 + 级联同步面） |
| .agent/skills/puti-shouye/SKILL.md | W1068 | 本批修改（坑表条数计数链同步） |
| scripts/output/tools-inventory.md | W1068 | 本批修改（工具清单刷新·收录新增方法论篇） |
| pytest.ini | W1068 | 本批修改（stats 实体标记跟随） |
| CHANGELOG.md | W1068 | 本批修改（W1068 段·级联写入） |
| docs/00-导读/W批次编号对账表.md | W1068 | 本批修改（W1068 台账行·手工登记） |
## W1067 CI action ref 根修批 + 记忆与项目沉淀同步批（2026-10-31）

| 文件 | W | 说明 |
|---|---|---|
| scripts/check_action_refs.py | W1067 | 本批新增（action ref 完整性门禁·形态离线 + 存在性联网双 endpoint 复核·自测 6/6 可证伪） |
| .github/workflows/screenshot-review.yml | W1067 | 本批修改（merge job 的 action ref 改用仓内已验证 v7 SHA·修 39 位编造 SHA 致 Set up job 阶段失败） |
| .github/workflows/workflow-lint.yml | W1067 | 本批修改（挂 action ref 形态判据每次 PR 恒生效 + 存在性扫描周级/手动·不带 token） |
| docs/agent/pitfalls.md | W1067 | 本批修改（新增 E-77~E-82 六条·流程组 75→81·含两条自私有记忆固化入仓） |
| .agent/skills/puti-shouye/SKILL.md | W1067 | 本批修改（坑表条数计数链同步） |
| AGENTS.md | W1067 | 本批修改（坑表条数计数链同步 + 级联脚注滚动） |
| HANDOVER.md | W1067 | 本批修改（坑表条数计数链同步 + 级联同步面） |
| docs/11-方案报告/计划方案/T40-任务计划执行与经验沉淀报告-2026-10-31.md | W1067 | 本批修改（§4.6 后续批次 W1067 进展段·根因与修法如实记录） |
| pytest.ini | W1067 | 本批修改（stats 实体标记跟随） |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1067 | 本批修改（stats 实体标记跟随） |
| scripts/index.md | W1067 | 本批修改（目录清单刷新·收录新增判据脚本） |
| scripts/output/tools-inventory.md | W1067 | 本批修改（工具清单刷新·收录新增判据脚本） |
| scripts/output/index.md | W1067 | 本批修改（目录清单刷新） |
| scripts/output/README.md | W1067 | 本批修改（目录清单刷新） |
## W1066 CI 提速批（2026-10-31）

| 文件 | W | 说明 |
|---|---|---|
| scripts/_audit_render_states.js | W1066 | 本批新增/修改（按需等待 waitForStable/waitForChange + CONC 6 + --shard 分片 + --out 产物路径） |
| scripts/batch_screenshots.js | W1066 | 本批新增/修改（多 context 并发 CONC 4·capture() 本已每页独立 context） |
| scripts/check_screenshot_gates.js | W1066 | 本批新增/修改（--only 支持逗号分隔多值·定向时只跑变更页） |
| scripts/check_dark_state_gate.js | W1066 | 本批新增/修改（--current 指定分片合并后的产物） |
| scripts/check_chart_data.py | W1066 | 本批新增/修改（<script>/<style> 剥离改大小写不敏感·CodeQL 告警） |
| scripts/check_chart_values.js | W1066 | 本批新增/修改（name 正则完整转义反斜杠·CodeQL 告警） |
| .github/workflows/screenshot-review.yml | W1066 | 本批新增/修改（暗色门禁 4 分片并行 + 合并判定 job + chart-gates 定向） |
| docs/agent/pitfalls.md | W1066 | 本批新增/修改（E-74~E-76 三条·162→165） |
| AGENTS.md | W1066 | 本批新增/修改（坑位计数 162→165 + 流程组分项 72→75） |
| HANDOVER.md | W1066 | 本批新增/修改（头链首 + §一 + 计数 162→165） |
| README.md | W1066 | 本批新增/修改（抬头当前批次行） |
| CHANGELOG.md | W1066 | 本批新增/修改（W1066 段 + 编号规则 W001-W1066） |
| CITATION.cff | W1066 | 本批新增/修改（version W1065→W1066） |
| .github/workflows/README.md | W1066 | 本批新增/修改（头部版本 + 里程碑行 W450-W1066） |
| docs/00-导读/W批次编号对账表.md | W1066 | 本批新增/修改（W1066 认领行 + 收官回填） |
| .agent/skills/puti-shouye/SKILL.md | W1066 | 本批新增/修改（计数链 162→165 两点） |
| docs/11-方案报告/README.md | W1066 | 本批新增/修改（移除已删文件的登记行） |
| docs/11-方案报告/调研与数据复盘/西游记GitHub生态全景调研报告-2026-10-31.md | W1066 | 本批新增/修改（承接说明去死链·用户有意删除 W358 旧报告） |
| docs/11-方案报告/调研与数据复盘/项目GitHub参考调研报告.md | W1066 | 本批删除（用户 2026-10-31 有意删除·不再需要） |
| scripts/output/_w1063_spec.json | W1066 | 本批新增/修改（级联 spec·55 件） |

## W1065 《西游记》GitHub 生态全景调研批（2026-10-31）

| 文件 | W | 说明 |
|---|---|---|
| docs/11-方案报告/调研与数据复盘/西游记GitHub生态全景调研报告-2026-10-31.md | W1065 | 本批新增（78 KB·四域生态全景·72 项实跑取证·含附录 A–D） |
| docs/11-方案报告/调研与数据复盘/项目GitHub参考调研报告.md | W1065 | 本批新增/修改（W358 存量调研承接·7 个失效链接修正见报告 §5.13.1） |
| docs/11-方案报告/README.md | W1065 | 本批新增/修改（W1065 登记行） |
| CHANGELOG.md | W1065 | 本批新增/修改（W1065 段 + 编号规则上限） |
| HANDOVER.md | W1065 | 本批新增/修改（抬头更新链 + §一 概要块） |
| docs/00-导读/W批次编号对账表.md | W1065 | 本批新增/修改（W1065 认领/收官行） |
| scripts/output/file-index.md | W1065 | 本批新增/修改（本段） |

## W1063 并行会话滞后提交收口批（2026-10-31）

| 文件 | W | 说明 |
|---|---|---|
| scripts/check_cross_line_rewrite.py | W1063 | 并行会话在途件收口（ruff 清理·io.open → open） |
| scripts/ledger_backfill.py | W1063 | 并行会话在途件收口（ruff 清理·死变量与变量名遮蔽） |
| scripts/security_scan.py | W1063 | SEC-002 过宽前瞻根修（改白名单式收紧·防真密钥漏检） |
| scripts/sec002_negative_probe.py | W1063 | 本批新增（SEC-002 负样本自证 9/9·含「真密钥混汉字」边界） |
| .github/workflows/security.yml | W1063 | 本批新增/修改（SEC-002 负样本自证独立 job） |
| docs/agent/pitfalls.md | W1063 | 本批新增/修改（E-71 误报放行须白名单式收紧 + E-72 收口在途件先三方比对·156→161） |
| AGENTS.md | W1063 | 本批新增/修改（坑位计数 159→161 + 流程组分项 69→71） |
| HANDOVER.md | W1063 | 本批新增/修改（头链首 + §一 + 坑表计数 159→161） |
| README.md | W1063 | 本批新增/修改（抬头当前批次行） |
| CHANGELOG.md | W1063 | 本批新增/修改（W1063 段 + 编号规则 W001-W1063） |
| CITATION.cff | W1063 | 本批新增/修改（version W1062→W1063） |
| .github/workflows/README.md | W1063 | 本批新增/修改（头部版本 + 里程碑行 W450-W1063） |
| docs/00-导读/W批次编号对账表.md | W1063 | 本批新增/修改（W1063 认领行 + 收官回填） |
| .agent/skills/puti-shouye/SKILL.md | W1063 | 本批新增/修改（计数链 159→161 两点） |
| scripts/output/_w1063_spec.json | W1063 | 本批新增（级联 spec） |
| site/index.html | W1063 | 本批新增/修改（页脚链首） |
| site/dukou-engine.html | W1063 | 本批新增/修改（页脚链首） |
| site/data/tag-cloud.html | W1063 | 本批新增/修改（页脚链首） |
| site/data/cross-time-danmaku.html | W1063 | 本批新增/修改（页脚链首） |

## W1062 README 换图未生效根修批（2026-10-31）

| 文件 | W | 说明 |
|---|---|---|
| scripts/requirements.txt | W1062 | 本批新增/修改（登记 numpy 2.4.4 + playwright 1.63.0·CI pytest 5 failed 清零） |
| scripts/check_no_brand_refs.py | W1062 | 本批新增/修改（core.quotepath=false 根修 + 声明性豁免 + fail-closed + 自测 56/56） |
| AGENTS.md | W1062 | 本批新增/修改（坑位计数 156→159 + 流程组分项 66→69 + 六主题目录） |
| HANDOVER.md | W1062 | 本批新增/修改（头链首 + §一 当前进度 + 坑表计数 156→159） |
| README.md | W1062 | 本批新增/修改（抬头当前批次行） |
| CHANGELOG.md | W1062 | 本批新增/修改（W1062 段 + 编号规则 W001-W1062） |
| CITATION.cff | W1062 | 本批新增/修改（version W1061→W1062） |
| .github/workflows/README.md | W1062 | 本批新增/修改（头部版本 + 里程碑行 W450-W1062） |
| docs/agent/pitfalls.md | W1062 | 本批新增/修改（E-68~E-70 三条 + 流程组 66→69） |
| .agent/skills/puti-shouye/SKILL.md | W1062 | 本批新增/修改（计数链 156→159 两点） |
| docs/00-导读/W批次编号对账表.md | W1062 | 本批新增/修改（W1062 认领行 + 收官回填） |
| docs/11-方案报告/计划方案/T40-任务计划执行与经验沉淀报告-2026-10-31.md | W1062 | 本批新增（框架第 40 次执行报告） |
| docs/11-方案报告/README.md | W1062 | 本批新增/修改（T40 登记行） |
| docs/11-方案报告/审查与评审/工具脚本门禁体检与临时归档审计-2026-10-29.md | W1062 | 本批新增/修改（品牌字面量清零 1 处） |
| docs/11-方案报告/计划方案/T04-任务计划执行与经验沉淀报告-2026-10-21.md | W1062 | 本批新增/修改（品牌字面量清零 1 处） |
| docs/11-方案报告/设计与架构方案/取经编制表-工具与技能挂位-2026-10-20.md | W1062 | 本批新增/修改（品牌字面量清零 1 处） |
| scripts/output/_w1062_spec.json | W1062 | 本批新增（级联 spec） |
| site/index.html | W1062 | 本批新增/修改（页脚链首） |
| site/dukou-engine.html | W1062 | 本批新增/修改（页脚链首） |
| site/data/tag-cloud.html | W1062 | 本批新增/修改（页脚链首） |
| site/data/cross-time-danmaku.html | W1062 | 本批新增/修改（页脚链首） |

## W1061 私有记忆同步批（2026-10-31）

| 文件 | W | 说明 |
|---|---|---|
| AGENTS.md | W1061 | 本批新增/修改（铁律 19 + §4.3 两条 + 分项 66 + 级联脚注） |
| CLAUDE.md | W1061 | 本批新增/修改（速查第 14 行禁 CodeBuddy·三问顺延 15·51/60 行） |
| docs/agent/pitfalls.md | W1061 | 本批新增/修改（+10 条 E-58~E-67·156·流程组 66） |
| HANDOVER.md | W1061 | 本批新增/修改（坑表计数链 156 + 级联面） |
| .agent/skills/puti-shouye/SKILL.md | W1061 | 本批新增/修改（计数链 156） |
| CHANGELOG.md | W1061 | 收官面（顶段 W1061·验证栏含三问结论） |
| README.md | W1061 | 级联面（版本行） |
| STRUCTURE.md | W1061 | 级联面（版本行） |
| CITATION.cff | W1061 | 级联面（版本同步） |
| docs/00-导读/项目说明.md | W1061 | 级联面（当前版本行） |
| docs/00-导读/W批次编号对账表.md | W1061 | 台账（W1061 行新增） |
| docs/INDEX.md | W1061 | 登记面（docs 索引） |
| index.md | W1061 | 登记面（根索引） |
| archive/docs/AGENTS-ARCHIVE.md | W1061 | 级联归档滚动 |
| archive/docs/CHANGELOG-ARCHIVE.md | W1061 | 级联归档滚动（体积窗若触发） |
| archive/docs/file-index-ARCHIVE.md | W1061 | 级联归档滚动（体积窗若触发） |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1061 | 级联归档滚动（体积窗若触发） |
| .github/workflows/README.md | W1061 | 级联面（里程碑行同步） |
| site/index.html | W1061 | 级联面（页脚批次链插入） |
| site/data/cross-time-danmaku.html | W1061 | 级联面（页脚批次链插入） |
| site/data/tag-cloud.html | W1061 | 级联面（页脚批次链插入） |
| site/dukou-engine.html | W1061 | 级联面（页脚批次链插入·含 head_sentence） |
| scripts/output/stats.json | W1061 | 登记面产物（stats 实体） |
| scripts/output/stats-changelog.json | W1061 | 登记面产物（变更史） |
| scripts/output/stats-index.md | W1061 | 登记面产物（统计索引） |
| scripts/output/file-index.md | W1061 | 登记面产物（反向索引） |
| scripts/output/index.md | W1061 | 登记面产物（output 索引） |
| scripts/output/tools-inventory.md | W1061 | 登记面产物（工具清单） |
| scripts/output/README.md | W1061 | 登记面产物（output 说明） |
| scripts/output/chart-values-report.json | W1061 | 登记面产物（第 43 槽报告） |
| scripts/output/_vermilion_solid_cache.json | W1061 | 登记面产物（第 49 槽机器缓存自跟随） |
| scripts/cross_line_baseline.json | W1061 | 登记面产物（跨行基线·扫描随批） |
| scripts/output/_cascade_files_W1061.txt | W1061 | 级联清单（本批产物） |
| scripts/output/_w1061_spec.json | W1061 | 本批 spec |

## W1060 CI 提效批（2026-10-31）

| 文件 | W | 说明 |
|---|---|---|
| .github/workflows/ci.yml | W1060 | 本批新增/修改（A11y 矩阵 9→1·artifact 名去 matrix 引用） |
| .github/workflows/dependency-review.yml | W1060 | 本批新增/修改（补 concurrency） |
| .github/workflows/workflow-lint.yml | W1060 | 本批新增/修改（补 concurrency） |
| .github/workflows/scorecard.yml | W1060 | 本批新增/修改（补 concurrency） |
| CHANGELOG.md | W1060 | 收官面（顶段 W1060） |
| HANDOVER.md | W1060 | 级联面（最后更新/进度） |
| README.md | W1060 | 级联面（版本行） |
| STRUCTURE.md | W1060 | 级联面（版本行） |
| AGENTS.md | W1060 | 级联面（脚注滚动） |
| CITATION.cff | W1060 | 级联面（版本同步） |
| docs/00-导读/项目说明.md | W1060 | 级联面（当前版本行） |
| docs/00-导读/W批次编号对账表.md | W1060 | 台账（W1060 行新增） |
| docs/INDEX.md | W1060 | 登记面（docs 索引） |
| index.md | W1060 | 登记面（根索引） |
| .github/workflows/README.md | W1060 | 级联面（里程碑行同步） |
| archive/docs/AGENTS-ARCHIVE.md | W1060 | 级联归档滚动 |
| archive/docs/CHANGELOG-ARCHIVE.md | W1060 | 级联归档滚动（体积窗若触发） |
| archive/docs/file-index-ARCHIVE.md | W1060 | 级联归档滚动（体积窗若触发） |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1060 | 级联归档滚动（体积窗若触发） |
| site/index.html | W1060 | 级联面（页脚批次链插入） |
| site/data/cross-time-danmaku.html | W1060 | 级联面（页脚批次链插入） |
| site/data/tag-cloud.html | W1060 | 级联面（页脚批次链插入） |
| site/dukou-engine.html | W1060 | 级联面（页脚批次链插入·含 head_sentence） |
| scripts/output/stats.json | W1060 | 登记面产物（stats 实体） |
| scripts/output/stats-changelog.json | W1060 | 登记面产物（变更史） |
| scripts/output/stats-index.md | W1060 | 登记面产物（统计索引） |
| scripts/output/file-index.md | W1060 | 登记面产物（反向索引） |
| scripts/output/index.md | W1060 | 登记面产物（output 索引） |
| scripts/output/tools-inventory.md | W1060 | 登记面产物（工具清单） |
| scripts/output/README.md | W1060 | 登记面产物（output 说明） |
| scripts/output/_cascade_files_W1060.txt | W1060 | 级联清单（本批产物） |
| scripts/output/_w1060_spec.json | W1060 | 本批 spec |

## W1059 第 46 篇工作复盘与优化分析报告入库批（2026-10-31）

| 文件 | W | 说明 |
|---|---|---|
| docs/11-方案报告/工作复盘与优化分析报告/工作复盘与优化分析报告-2026-10-31.md | W1059 | 本批新增（第 46 篇复盘报告） |
| docs/11-方案报告/README.md | W1059 | 本批新增/修改（分区表 #52 登记） |
| CHANGELOG.md | W1059 | 收官面（顶段 W1059·标题含「工作复盘」三信号 A） |
| HANDOVER.md | W1059 | 级联面（最后更新/进度/里程碑） |
| README.md | W1059 | 级联面（版本行） |
| STRUCTURE.md | W1059 | 级联面（版本行） |
| AGENTS.md | W1059 | 级联面（脚注滚动） |
| CITATION.cff | W1059 | 级联面（版本同步） |
| docs/00-导读/项目说明.md | W1059 | 级联面（当前版本行） |
| docs/00-导读/W批次编号对账表.md | W1059 | 台账（W1059 认领行在案·收官回填另笔） |
| docs/INDEX.md | W1059 | 登记面（docs 索引） |
| index.md | W1059 | 登记面（根索引） |
| archive/docs/AGENTS-ARCHIVE.md | W1059 | 级联归档滚动 |
| archive/docs/CHANGELOG-ARCHIVE.md | W1059 | 级联归档滚动（体积窗若触发） |
| archive/docs/file-index-ARCHIVE.md | W1059 | 级联归档滚动（体积窗若触发） |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1059 | 级联归档滚动（体积窗若触发） |
| .github/workflows/README.md | W1059 | 级联面（里程碑行同步） |
| site/index.html | W1059 | 级联面（页脚批次链插入） |
| site/data/cross-time-danmaku.html | W1059 | 级联面（页脚批次链插入） |
| site/data/tag-cloud.html | W1059 | 级联面（页脚批次链插入） |
| site/dukou-engine.html | W1059 | 级联面（页脚批次链插入·含 head_sentence） |
| scripts/output/stats.json | W1059 | 登记面产物（stats 实体） |
| scripts/output/stats-changelog.json | W1059 | 登记面产物（变更史） |
| scripts/output/stats-index.md | W1059 | 登记面产物（统计索引） |
| scripts/output/file-index.md | W1059 | 登记面产物（反向索引） |
| scripts/output/index.md | W1059 | 登记面产物（output 索引） |
| scripts/output/tools-inventory.md | W1059 | 登记面产物（工具清单） |
| scripts/output/README.md | W1059 | 登记面产物（output 说明） |
| site/data/search.html | W1059 | 派生面（搜索索引刷新·README 新行） |
| site/en/search.html | W1059 | 派生面（搜索索引刷新） |
| scripts/output/_cascade_files_W1059.txt | W1059 | 级联清单（本批产物） |
| scripts/output/_w1059_spec.json | W1059 | 本批 spec |

## W1058 SKILL.md 计数链漂移订正 + C5e 对账面扩 SKILL（2026-10-31）

| 文件 | W | 说明 |
|---|---|---|
| AGENTS.md | W1058 | 级联面（脚注滚动） |
| .agent/skills/puti-shouye/SKILL.md | W1058 | 本批新增/修改（计数 144→146 两处） |
| scripts/check_doc_sync.py | W1058 | 本批新增/修改（C5e 对账面扩 SKILL.md 两形态） |
| CHANGELOG.md | W1058 | 收官面（顶段 W1058） |
| HANDOVER.md | W1058 | 级联面（最后更新/进度） |
| README.md | W1058 | 级联面（版本行） |
| STRUCTURE.md | W1058 | 级联面（版本行） |
| CITATION.cff | W1058 | 级联面（版本同步） |
| docs/00-导读/项目说明.md | W1058 | 级联面（当前版本行） |
| docs/00-导读/W批次编号对账表.md | W1058 | 台账（W1058 行新增） |
| docs/INDEX.md | W1058 | 登记面（docs 索引） |
| index.md | W1058 | 登记面（根索引） |
| archive/docs/AGENTS-ARCHIVE.md | W1058 | 级联归档滚动 |
| archive/docs/CHANGELOG-ARCHIVE.md | W1058 | 级联归档滚动（体积窗若触发） |
| archive/docs/file-index-ARCHIVE.md | W1058 | 级联归档滚动（体积窗若触发） |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1058 | 级联归档滚动（体积窗若触发） |
| .github/workflows/README.md | W1058 | 级联面（里程碑行同步） |
| site/index.html | W1058 | 级联面（页脚批次链插入） |
| site/data/cross-time-danmaku.html | W1058 | 级联面（页脚批次链插入） |
| site/data/tag-cloud.html | W1058 | 级联面（页脚批次链插入） |
| site/dukou-engine.html | W1058 | 级联面（页脚批次链插入·含 head_sentence） |
| scripts/output/stats.json | W1058 | 登记面产物（stats 实体） |
| scripts/output/stats-changelog.json | W1058 | 登记面产物（变更史） |
| scripts/output/stats-index.md | W1058 | 登记面产物（统计索引） |
| scripts/output/file-index.md | W1058 | 登记面产物（反向索引） |
| scripts/output/index.md | W1058 | 登记面产物（output 索引） |
| scripts/output/tools-inventory.md | W1058 | 登记面产物（工具清单） |
| scripts/output/README.md | W1058 | 登记面产物（output 说明） |
| scripts/output/_cascade_files_W1058.txt | W1058 | 级联清单（本批产物） |
| scripts/output/_w1058_spec.json | W1058 | 本批 spec |

## W1057 Backlog 对账批（2026-10-31）

| 文件 | W | 说明 |
|---|---|---|
| HANDOVER.md | W1057 | 本批新增/修改（四、待办压缩 12→1 形态锚 + 对账注记 + 级联面） |
| CHANGELOG.md | W1057 | 收官面（顶段 W1057 对账记录） |
| README.md | W1057 | 级联面（版本行） |
| STRUCTURE.md | W1057 | 级联面（版本行） |
| AGENTS.md | W1057 | 级联面（脚注滚动） |
| CITATION.cff | W1057 | 级联面（版本同步） |
| docs/00-导读/项目说明.md | W1057 | 级联面（当前版本行） |
| docs/00-导读/W批次编号对账表.md | W1057 | 台账（W1057 行·状态列含对账 token） |
| docs/INDEX.md | W1057 | 登记面（docs 索引） |
| index.md | W1057 | 登记面（根索引） |
| archive/docs/AGENTS-ARCHIVE.md | W1057 | 级联归档滚动 |
| archive/docs/CHANGELOG-ARCHIVE.md | W1057 | 级联归档滚动（体积窗若触发） |
| archive/docs/file-index-ARCHIVE.md | W1057 | 级联归档滚动（体积窗若触发） |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1057 | 级联归档滚动（体积窗若触发） |
| .github/workflows/README.md | W1057 | 级联面（里程碑行同步） |
| site/index.html | W1057 | 级联面（页脚批次链插入） |
| site/data/cross-time-danmaku.html | W1057 | 级联面（页脚批次链插入） |
| site/data/tag-cloud.html | W1057 | 级联面（页脚批次链插入） |
| site/dukou-engine.html | W1057 | 级联面（页脚批次链插入·含 head_sentence） |
| scripts/output/stats.json | W1057 | 登记面产物（stats 实体） |
| scripts/output/stats-changelog.json | W1057 | 登记面产物（变更史） |
| scripts/output/stats-index.md | W1057 | 登记面产物（统计索引） |
| scripts/output/file-index.md | W1057 | 登记面产物（反向索引） |
| scripts/output/index.md | W1057 | 登记面产物（output 索引） |
| scripts/output/tools-inventory.md | W1057 | 登记面产物（工具清单） |
| scripts/output/README.md | W1057 | 登记面产物（output 说明） |
| scripts/output/chart-values-report.json | W1057 | 登记面产物（第 43 槽报告·上批余波） |
| scripts/output/_vermilion_solid_cache.json | W1057 | 登记面产物（第 49 槽机器缓存自跟随） |
| scripts/output/_cascade_files_W1057.txt | W1057 | 级联清单（本批产物） |
| scripts/output/_w1057_spec.json | W1057 | 本批 spec |

## W1056 提交前三问自检流程契约（2026-10-31）

| 文件 | W | 说明 |
|---|---|---|
| AGENTS.md | W1056 | 本批新增/修改（铁律 18 + 分项 56 + 级联脚注） |
| CLAUDE.md | W1056 | 本批新增/修改（速查第 14 行·50/60 行） |
| docs/agent/pitfalls.md | W1056 | 本批新增/修改（+1 spec 漏列形态·146·流程组 56） |
| HANDOVER.md | W1056 | 本批新增/修改（坑表计数链 146 + 级联面） |
| docs/00-导读/W批次编号对账表.md | W1056 | 台账（W1056 行新增） |
| CHANGELOG.md | W1056 | 收官面（顶段 W1056·验证栏含三问结论） |
| README.md | W1056 | 级联面（版本行） |
| STRUCTURE.md | W1056 | 级联面（版本行） |
| CITATION.cff | W1056 | 级联面（版本同步） |
| docs/00-导读/项目说明.md | W1056 | 级联面（当前版本行） |
| docs/INDEX.md | W1056 | 登记面（docs 索引） |
| index.md | W1056 | 登记面（根索引） |
| archive/docs/AGENTS-ARCHIVE.md | W1056 | 级联归档滚动 |
| archive/docs/CHANGELOG-ARCHIVE.md | W1056 | 级联归档滚动（体积窗若触发） |
| archive/docs/file-index-ARCHIVE.md | W1056 | 级联归档滚动（体积窗若触发） |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1056 | 级联归档滚动（体积窗若触发） |
| .github/workflows/README.md | W1056 | 级联面（里程碑行同步） |
| site/index.html | W1056 | 级联面（页脚批次链插入） |
| site/data/cross-time-danmaku.html | W1056 | 级联面（页脚批次链插入） |
| site/data/tag-cloud.html | W1056 | 级联面（页脚批次链插入） |
| site/dukou-engine.html | W1056 | 级联面（页脚批次链插入·含 head_sentence） |
| scripts/output/stats.json | W1056 | 登记面产物（stats 实体） |
| scripts/output/stats-changelog.json | W1056 | 登记面产物（变更史） |
| scripts/output/stats-index.md | W1056 | 登记面产物（统计索引） |
| scripts/output/file-index.md | W1056 | 登记面产物（反向索引） |
| scripts/output/index.md | W1056 | 登记面产物（output 索引） |
| scripts/output/tools-inventory.md | W1056 | 登记面产物（工具清单） |
| scripts/output/README.md | W1056 | 登记面产物（output 说明） |
| scripts/output/_cascade_files_W1056.txt | W1056 | 级联清单（本批产物） |
| scripts/output/_w1056_spec.json | W1056 | 本批 spec |

## W1055 G-03 清偿第二轮（2026-10-31）

| 文件 | W | 说明 |
|---|---|---|
| scripts/check_chart_values.js | W1055 | 本批新增/修改（G-03 清偿①时序重试②前缀扩展③影子分层） |
| CHANGELOG.md | W1055 | 收官面（顶段 W1055） |
| HANDOVER.md | W1055 | 收官面（最后更新/进度/级联） |
| README.md | W1055 | 级联面（版本行） |
| STRUCTURE.md | W1055 | 级联面（版本行） |
| CITATION.cff | W1055 | 级联面（版本同步） |
| AGENTS.md | W1055 | 级联面（脚注滚动） |
| docs/00-导读/项目说明.md | W1055 | 级联面（当前版本行） |
| docs/00-导读/W批次编号对账表.md | W1055 | 台账（W1055 行新增） |
| docs/INDEX.md | W1055 | 登记面（docs 索引） |
| index.md | W1055 | 登记面（根索引） |
| archive/docs/AGENTS-ARCHIVE.md | W1055 | 级联归档滚动 |
| archive/docs/CHANGELOG-ARCHIVE.md | W1055 | 级联归档滚动（体积窗若触发） |
| archive/docs/file-index-ARCHIVE.md | W1055 | 级联归档滚动（体积窗若触发） |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1055 | 级联归档滚动（体积窗若触发） |
| .github/workflows/README.md | W1055 | 级联面（里程碑行同步） |
| site/index.html | W1055 | 级联面（页脚批次链插入） |
| site/data/cross-time-danmaku.html | W1055 | 级联面（页脚批次链插入） |
| site/data/tag-cloud.html | W1055 | 级联面（页脚批次链插入） |
| site/dukou-engine.html | W1055 | 级联面（页脚批次链插入·含 head_sentence） |
| scripts/output/stats.json | W1055 | 登记面产物（stats 实体） |
| scripts/output/stats-changelog.json | W1055 | 登记面产物（变更史） |
| scripts/output/stats-index.md | W1055 | 登记面产物（统计索引） |
| scripts/output/file-index.md | W1055 | 登记面产物（反向索引） |
| scripts/output/index.md | W1055 | 登记面产物（output 索引） |
| scripts/output/tools-inventory.md | W1055 | 登记面产物（工具清单） |
| scripts/output/README.md | W1055 | 登记面产物（output 说明） |
| scripts/output/_cascade_files_W1055.txt | W1055 | 级联清单（本批产物） |
| scripts/output/_w1055_spec.json | W1055 | 本批 spec |
| scripts/output/_vermilion_solid_cache.json | W1055 | 登记面产物（第 49 槽机器缓存自跟随） |
| scripts/index.md | W1055 | 登记面（scripts 目录索引） |

## W1054 G-03 清偿第一轮（2026-10-31）

| 文件 | W | 说明 |
|---|---|---|
| scripts/check_chart_values.js | W1054 | 本批新增/修改（G-03 清偿①时序重试②前缀扩展③影子分层） |
| CHANGELOG.md | W1054 | 收官面（顶段 W1054） |
| HANDOVER.md | W1054 | 收官面（最后更新/进度/级联） |
| README.md | W1054 | 级联面（版本行） |
| STRUCTURE.md | W1054 | 级联面（版本行） |
| CITATION.cff | W1054 | 级联面（版本同步） |
| AGENTS.md | W1054 | 级联面（脚注滚动） |
| docs/00-导读/项目说明.md | W1054 | 级联面（当前版本行） |
| docs/00-导读/W批次编号对账表.md | W1054 | 台账（W1054 行新增） |
| docs/INDEX.md | W1054 | 登记面（docs 索引） |
| index.md | W1054 | 登记面（根索引） |
| archive/docs/AGENTS-ARCHIVE.md | W1054 | 级联归档滚动 |
| archive/docs/CHANGELOG-ARCHIVE.md | W1054 | 级联归档滚动（体积窗若触发） |
| archive/docs/file-index-ARCHIVE.md | W1054 | 级联归档滚动（体积窗若触发） |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1054 | 级联归档滚动（体积窗若触发） |
| .github/workflows/README.md | W1054 | 级联面（里程碑行同步） |
| site/index.html | W1054 | 级联面（页脚批次链插入） |
| site/data/cross-time-danmaku.html | W1054 | 级联面（页脚批次链插入） |
| site/data/tag-cloud.html | W1054 | 级联面（页脚批次链插入） |
| site/dukou-engine.html | W1054 | 级联面（页脚批次链插入·含 head_sentence） |
| scripts/output/stats.json | W1054 | 登记面产物（stats 实体） |
| scripts/output/stats-changelog.json | W1054 | 登记面产物（变更史） |
| scripts/output/stats-index.md | W1054 | 登记面产物（统计索引） |
| scripts/output/file-index.md | W1054 | 登记面产物（反向索引） |
| scripts/output/index.md | W1054 | 登记面产物（output 索引） |
| scripts/output/tools-inventory.md | W1054 | 登记面产物（工具清单） |
| scripts/output/README.md | W1054 | 登记面产物（output 说明） |
| scripts/output/_cascade_files_W1054.txt | W1054 | 级联清单（本批产物） |
| scripts/output/_w1054_spec.json | W1054 | 本批 spec |
| scripts/output/_vermilion_solid_cache.json | W1054 | 登记面产物（第 49 槽机器缓存自跟随） |
| scripts/index.md | W1054 | 登记面（scripts 目录索引） |

## W1053 W1046 方案实施收尾（2026-10-31）

| 文件 | W | 说明 |
|---|---|---|
| scripts/check_inlined_css.py | W1053 | 本批新增/修改（G-02 特征断言·self-test 2 例） |
| scripts/check_chart_values.js | W1053 | 本批新增/修改（G-03 na 影子报数·不进 FAIL） |
| scripts/check_gsap_motion.py | W1053 | 本批新增/修改（G-04 扫描域扩全+剥注释+J8 glob·self-test 11 例） |
| scripts/check_frontmatter.py | W1053 | 本批新增/修改（G-05 日期语义+哈希形态·self-test 5 例） |
| scripts/check_governance_docs.py | W1053 | 本批新增/修改（G-06 self-test 3 例） |
| scripts/check_glossary.py | W1053 | 本批新增/修改（G-06 self-test 3 例） |
| scripts/check_corruption.py | W1053 | 本批新增/修改（G-06 self-test 3 例） |
| scripts/ledger_close_check.py | W1053 | 本批新增/修改（P-01/P-02 C3 五问+回归锁·3 例自测） |
| scripts/check_review_trigger.py | W1053 | 本批新增/修改（M-03 T4 触发器·2 例自测） |
| scripts/stats.py | W1053 | 本批新增/修改（M-02 w864_entries/icon_allowlist_entries 两键） |
| scripts/patch_ratio.py | W1053 | 本批新增（M-01 补丁比影子脚本·不挂槽） |
| docs/00-导读/文档规范.md | W1053 | 本批新增/修改（I-01 豁免分级审批条款 + I-03 改动分级列 14 行） |
| scripts/output/_w864_accent_exemptions.json | W1053 | 本批新增/修改（I-02 owner/review_by 字段化 256 条） |
| AGENTS.md | W1053 | 本批新增/修改（铁律 16 之⑦ + 级联脚注） |
| CHANGELOG.md | W1053 | 收官面（顶段 W1053） |
| HANDOVER.md | W1053 | 收官面（最后更新/进度/级联） |
| README.md | W1053 | 级联面（版本行） |
| STRUCTURE.md | W1053 | 级联面（版本行） |
| CITATION.cff | W1053 | 级联面（版本同步） |
| docs/00-导读/项目说明.md | W1053 | 级联面（当前版本行） |
| docs/INDEX.md | W1053 | 登记面（docs 索引） |
| index.md | W1053 | 登记面（根索引） |
| archive/docs/AGENTS-ARCHIVE.md | W1053 | 级联归档滚动 |
| archive/docs/CHANGELOG-ARCHIVE.md | W1053 | 级联归档滚动（体积窗若触发） |
| archive/docs/file-index-ARCHIVE.md | W1053 | 级联归档滚动（体积窗若触发） |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1053 | 级联归档滚动（体积窗若触发） |
| .github/workflows/README.md | W1053 | 级联面（里程碑行同步） |
| site/index.html | W1053 | 级联面（页脚批次链插入） |
| site/data/cross-time-danmaku.html | W1053 | 级联面（页脚批次链插入） |
| site/data/tag-cloud.html | W1053 | 级联面（页脚批次链插入） |
| site/dukou-engine.html | W1053 | 级联面（页脚批次链插入·含 head_sentence） |
| scripts/output/stats.json | W1053 | 登记面产物（stats 实体·含 M-02 两新键） |
| scripts/output/stats-changelog.json | W1053 | 登记面产物（变更史） |
| scripts/output/stats-index.md | W1053 | 登记面产物（统计索引） |
| scripts/output/file-index.md | W1053 | 登记面产物（反向索引） |
| scripts/output/index.md | W1053 | 登记面产物（output 索引） |
| scripts/output/tools-inventory.md | W1053 | 登记面产物（工具清单） |
| scripts/output/README.md | W1053 | 登记面产物（output 说明） |
| scripts/output/_cascade_files_W1053.txt | W1053 | 级联清单（本批产物） |
| scripts/output/_w1053_spec.json | W1053 | 本批 spec |
| docs/00-导读/W批次编号对账表.md | W1053 | 台账（W1053 行新增） |

## W1052 补丁治理实施第一批（2026-10-31）

| 文件 | W | 说明 |
|---|---|---|
| AGENTS.md | W1052 | 本批新增/修改（G-01 双写去重 + 分项 55 + 级联脚注） |
| scripts/check_doc_sync.py | W1052 | 本批新增/修改（C8 同段重复判据 + T30/T31 自测 + 覆盖面先前已收 gates.md） |
| scripts/reserve_w.py | W1052 | 本批新增/修改（G-07 占号支撑检测 + self_test 三例 + UP009/E702 微修） |
| docs/agent/pitfalls.md | W1052 | 本批新增/修改（+1 条占号逃避形态·145·流程组 55） |
| HANDOVER.md | W1052 | 本批新增/修改（坑表计数链 145 + 级联面） |
| docs/11-方案报告/计划方案/执行前计划-W1046-补丁治理与门禁判据加固.md | W1052 | 本批新增/修改（方案钉订正：批准项计数 9→11） |
| docs/00-导读/W批次编号对账表.md | W1052 | 台账（W992 滞留状态回填 + W1052 行新增） |
| CHANGELOG.md | W1052 | 收官面（顶段 W1052） |
| README.md | W1052 | 级联面（版本行） |
| STRUCTURE.md | W1052 | 级联面（版本行） |
| CITATION.cff | W1052 | 级联面（版本同步） |
| docs/00-导读/项目说明.md | W1052 | 级联面（当前版本行） |
| docs/INDEX.md | W1052 | 登记面（docs 索引） |
| index.md | W1052 | 登记面（根索引） |
| archive/docs/AGENTS-ARCHIVE.md | W1052 | 级联归档滚动 |
| archive/docs/CHANGELOG-ARCHIVE.md | W1052 | 级联归档滚动（体积窗若触发） |
| archive/docs/file-index-ARCHIVE.md | W1052 | 级联归档滚动（体积窗若触发） |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1052 | 级联归档滚动（体积窗若触发） |
| .github/workflows/README.md | W1052 | 级联面（里程碑行同步） |
| site/index.html | W1052 | 级联面（页脚批次链插入） |
| site/data/cross-time-danmaku.html | W1052 | 级联面（页脚批次链插入） |
| site/data/tag-cloud.html | W1052 | 级联面（页脚批次链插入） |
| site/dukou-engine.html | W1052 | 级联面（页脚批次链插入·含 head_sentence） |
| scripts/output/stats.json | W1052 | 登记面产物（stats 实体） |
| scripts/output/stats-changelog.json | W1052 | 登记面产物（变更史） |
| scripts/output/stats-index.md | W1052 | 登记面产物（统计索引） |
| scripts/output/file-index.md | W1052 | 登记面产物（反向索引） |
| scripts/output/index.md | W1052 | 登记面产物（output 索引） |
| scripts/output/tools-inventory.md | W1052 | 登记面产物（工具清单） |
| scripts/output/README.md | W1052 | 登记面产物（output 说明） |
| scripts/output/_cascade_files_W1052.txt | W1052 | 级联清单（本批产物） |
| scripts/output/_w1052_spec.json | W1052 | 本批 spec |

## W1051 复盘触发器口径根修（2026-10-31）

| 文件 | W | 说明 |
|---|---|---|
| scripts/check_review_trigger.py | W1051 | 本批新增/修改（上篇复盘识别三信号 + 目录面独立证据源·判定本体根修） |
| tests/unit/test_review_trigger.py | W1051 | 本批新增/修改（单测 +7 例·契约同步 source 键·三负样本可证伪） |
| docs/agent/pitfalls.md | W1051 | 本批新增/修改（E-57 识别口径绑死单一字面量 ⇒ 同族登记形态逃逸） |
| AGENTS.md | W1051 | 级联面（脚注滚动 + 坑表计数链两处） |
| HANDOVER.md | W1051 | 级联面（最后更新 / 一、当前进度 + 计数链两处） |
| .agent/skills/puti-shouye/SKILL.md | W1051 | 计数链（坑表总条数两处·15 条硬判据不动） |
| README.md | W1051 | 级联面（版本行） |
| STRUCTURE.md | W1051 | 级联面（版本行） |
| docs/00-导读/项目说明.md | W1051 | 级联面（当前版本行） |
| CITATION.cff | W1051 | 级联面（版本同步） |
| CHANGELOG.md | W1051 | 收官面（顶段 W1051 + W1042 段标题补点题标识） |
| docs/00-导读/W批次编号对账表.md | W1051 | 台账（W1051 认领行新增 + 收官回填） |
| docs/11-方案报告/计划方案/执行前计划-W1051-复盘触发器口径根修.md | W1051 | 方案报告（执行前计划件·五表 + 自包含检查 12 项） |
| docs/11-方案报告/README.md | W1051 | 登记面（方案报告索引） |
| docs/INDEX.md | W1051 | 登记面（docs 索引） |
| index.md | W1051 | 登记面（根索引） |
| archive/docs/AGENTS-ARCHIVE.md | W1051 | 级联归档滚动 |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1051 | 级联归档滚动 |
| archive/docs/CHANGELOG-ARCHIVE.md | W1051 | 级联归档滚动（体积窗若触发） |
| archive/docs/file-index-ARCHIVE.md | W1051 | 级联归档滚动（体积窗若触发） |
| .github/workflows/README.md | W1051 | 级联面（里程碑行同步） |
| site/index.html | W1051 | 级联面（页脚批次链插入） |
| site/data/cross-time-danmaku.html | W1051 | 级联面（页脚批次链插入） |
| site/data/tag-cloud.html | W1051 | 级联面（页脚批次链插入） |
| site/dukou-engine.html | W1051 | 级联面（页脚批次链插入·含 head_sentence） |
| scripts/output/stats.json | W1051 | 登记面产物（stats 实体） |
| scripts/output/stats-changelog.json | W1051 | 登记面产物（变更史） |
| scripts/output/stats-index.md | W1051 | 登记面产物（统计索引） |
| scripts/output/file-index.md | W1051 | 登记面产物（反向索引） |
| scripts/output/index.md | W1051 | 登记面产物（output 索引） |
| scripts/output/tools-inventory.md | W1051 | 登记面产物（工具清单） |
| scripts/output/README.md | W1051 | 登记面产物（output 说明） |
| scripts/output/_cascade_files_W1051.txt | W1051 | 级联清单（本批产物） |
| scripts/output/_w1051_spec.json | W1051 | 本批 spec |
| pytest.ini | W1051 | 连带产物（stats 标记跟随·pytest_collected 1087 → 1094·本批新增 7 例） |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1051 | 连带产物（stats 标记跟随·pytest_collected 1087 → 1094） |
| site/data/search.html | W1051 | 连带产物（站内搜索索引刷新·条目数对齐 948） |
| site/en/search.html | W1051 | 连带产物（站内搜索索引刷新·条目数对齐 948） |
| docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md | W1051 | 连带产物（stats 标记面跟随·pytest_collected 1087 → 1094） |

## W1050 门禁判据加固（2026-10-31）

| 文件 | W | 说明 |
|---|---|---|
| scripts/verify_delivery.py | W1050 | 本批新增/修改（第 3 槽 A1-A6 计数 fallback·用户批准动门禁本体·py_compile+全量跑通） |
| scripts/check_doc_sync.py | W1050 | 本批新增/修改（c5b_extra_surfaces 加 gates.md·sweep 覆盖面修复） |
| docs/agent/gates.md | W1050 | 本批新增/修改（L26 判据文本同步 fallback 描述） |
| CHANGELOG.md | W1050 | 收官面（顶段 W1050） |
| HANDOVER.md | W1050 | 收官面（最后更新/一、当前进度） |
| README.md | W1050 | 级联面（版本行） |
| STRUCTURE.md | W1050 | 级联面（版本行） |
| AGENTS.md | W1050 | 级联面（脚注滚动） |
| CITATION.cff | W1050 | 级联面（版本同步） |
| docs/00-导读/项目说明.md | W1050 | 级联面（当前版本行） |
| docs/00-导读/W批次编号对账表.md | W1050 | 台账（W1050 行新增） |
| docs/INDEX.md | W1050 | 登记面（docs 索引） |
| index.md | W1050 | 登记面（根索引） |
| archive/docs/AGENTS-ARCHIVE.md | W1050 | 级联归档滚动 |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1050 | 级联归档滚动 |
| archive/docs/CHANGELOG-ARCHIVE.md | W1050 | 级联归档滚动（体积窗若触发） |
| archive/docs/file-index-ARCHIVE.md | W1050 | 级联归档滚动（体积窗若触发） |
| .github/workflows/README.md | W1050 | 级联面（里程碑行同步） |
| site/index.html | W1050 | 级联面（页脚批次链插入） |
| site/data/cross-time-danmaku.html | W1050 | 级联面（页脚批次链插入） |
| site/data/tag-cloud.html | W1050 | 级联面（页脚批次链插入） |
| site/dukou-engine.html | W1050 | 级联面（页脚批次链插入·含 head_sentence） |
| scripts/output/stats.json | W1050 | 登记面产物（stats 实体） |
| scripts/output/stats-changelog.json | W1050 | 登记面产物（变更史） |
| scripts/output/stats-index.md | W1050 | 登记面产物（统计索引） |
| scripts/output/file-index.md | W1050 | 登记面产物（反向索引） |
| scripts/output/index.md | W1050 | 登记面产物（output 索引） |
| scripts/output/tools-inventory.md | W1050 | 登记面产物（工具清单） |
| scripts/output/README.md | W1050 | 登记面产物（output 说明） |
| scripts/output/_cascade_files_W1050.txt | W1050 | 级联清单（本批产物） |
| scripts/output/_w1050_spec.json | W1050 | 本批 spec |

## W1049 回次 og:image 全覆盖批·第五轮（2026-10-31）

| 文件 | W | 说明 |
|---|---|---|
| .agent/skills/puti-shouye/SKILL.md | W1049 | 本批新增/修改 |
| AGENTS.md | W1049 | 本批新增/修改 |
| CHANGELOG.md | W1049 | 本批新增/修改 |
| HANDOVER.md | W1049 | 本批新增/修改 |
| STRUCTURE.md | W1049 | 本批新增/修改 |
| archive/scripts/batches/w10xx/README.md | W1049 | 本批新增/修改 |
| archive/scripts/batches/w10xx/_w1049_cascade_manifest.py | W1049 | 本批工具脚本（归档批次区） |
| archive/scripts/batches/w10xx/_w1049_derive_prepare.py | W1049 | 本批工具脚本（归档批次区） |
| archive/scripts/batches/w10xx/_w1049_derive_stage.py | W1049 | 本批工具脚本（归档批次区） |
| archive/scripts/batches/w10xx/_w1049_derive_verify.py | W1049 | 本批工具脚本（归档批次区） |
| archive/scripts/batches/w10xx/_w1049_download.py | W1049 | 本批工具脚本（归档批次区） |
| archive/scripts/batches/w10xx/_w1049_fix_p2.py | W1049 | 本批工具脚本（归档批次区） |
| archive/scripts/batches/w10xx/_w1049_gate_isolation.py | W1049 | 本批工具脚本（归档批次区） |
| archive/scripts/batches/w10xx/_w1049_handover.py | W1049 | 本批工具脚本（归档批次区） |
| archive/scripts/batches/w10xx/_w1049_isolate_w1050.py | W1049 | 本批工具脚本（归档批次区） |
| archive/scripts/batches/w10xx/_w1049_make_spec.py | W1049 | 本批工具脚本（归档批次区） |
| archive/scripts/batches/w10xx/_w1049_master.py | W1049 | 本批工具脚本（归档批次区） |
| archive/scripts/batches/w10xx/_w1049_park_fileindex.py | W1049 | 本批工具脚本（归档批次区） |
| archive/scripts/batches/w10xx/_w1049_park_w1050.py | W1049 | 本批工具脚本（归档批次区） |
| archive/scripts/batches/w10xx/_w1049_park_w1050_faces.py | W1049 | 本批工具脚本（归档批次区） |
| archive/scripts/batches/w10xx/_w1049_pick_verify.py | W1049 | 本批工具脚本（归档批次区） |
| archive/scripts/batches/w10xx/_w1049_pitfalls.py | W1049 | 本批工具脚本（归档批次区） |
| archive/scripts/batches/w10xx/_w1049_prepare.py | W1049 | 本批工具脚本（归档批次区） |
| archive/scripts/batches/w10xx/_w1049_readme_register.py | W1049 | 本批工具脚本（归档批次区） |
| archive/scripts/batches/w10xx/_w1049_refresh_folders.py | W1049 | 本批工具脚本（归档批次区） |
| archive/scripts/batches/w10xx/_w1049_reissue.py | W1049 | 本批工具脚本（归档批次区） |
| archive/scripts/batches/w10xx/_w1049_reissue_97.py | W1049 | 本批工具脚本（归档批次区） |
| archive/scripts/batches/w10xx/_w1049_reissue_fetch.py | W1049 | 本批工具脚本（归档批次区） |
| archive/scripts/batches/w10xx/_w1049_reissue_og.py | W1049 | 本批工具脚本（归档批次区） |
| archive/scripts/batches/w10xx/_w1049_stage.py | W1049 | 本批工具脚本（归档批次区） |
| archive/scripts/batches/w10xx/_w1049_stage_faces.py | W1049 | 本批工具脚本（归档批次区） |
| archive/scripts/batches/w10xx/_w1049_stage_ledger.py | W1049 | 本批工具脚本（归档批次区） |
| archive/scripts/batches/w10xx/_w1049_sync_staged.py | W1049 | 本批工具脚本（归档批次区） |
| archive/scripts/batches/w10xx/_w1049_verify.py | W1049 | 本批工具脚本（归档批次区） |
| archive/scripts/batches/w10xx/index.md | W1049 | 本批新增/修改 |
| assets/promo/plate-set/index.md | W1049 | 本批新增/修改 |
| assets/promo/plate-set/plate-line-100-ch050-huode-xingjun.png | W1049 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-100-ch050-huode-xingjun.webp | W1049 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-101-ch055-nvguo-guowang.png | W1049 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-101-ch055-nvguo-guowang.webp | W1049 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-102-ch084-miefo-guowang.png | W1049 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-102-ch084-miefo-guowang.webp | W1049 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-103-ch005-sida-tianwang.png | W1049 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-103-ch005-sida-tianwang.webp | W1049 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-104-ch018-gao-taigong.png | W1049 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-104-ch018-gao-taigong.webp | W1049 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-105-ch032-yinjiao-dawang.png | W1049 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-105-ch032-yinjiao-dawang.webp | W1049 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-106-ch056-shidai-yanjun.png | W1049 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-106-ch056-shidai-yanjun.webp | W1049 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-107-ch067-honglin-damang.png | W1049 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-107-ch067-honglin-damang.webp | W1049 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-108-ch058-diting.png | W1049 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-108-ch058-diting.webp | W1049 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-97-ch016-jinchi-zhanglao.png | W1049 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-97-ch016-jinchi-zhanglao.webp | W1049 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-98-ch039-wenshu-pusa.png | W1049 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-98-ch039-wenshu-pusa.webp | W1049 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-99-ch046-luli-daxian.png | W1049 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-99-ch046-luli-daxian.webp | W1049 | 新增母版（1200×1600） |
| assets/promo/plate-set/preview-contact-sheet.png | W1049 | 拼图预览（含本批 12 张） |
| assets/promo/plate-set/preview-contact-sheet.webp | W1049 | 拼图预览（含本批 12 张） |
| assets/promo/plate-set/raw/README.md | W1049 | 本批新增/修改 |
| assets/promo/plate-set/raw/index.md | W1049 | 本批新增/修改 |
| assets/promo/plate-set/raw/round18/README.md | W1049 | 出图原件（12 份·含 3 张重出） |
| assets/promo/plate-set/raw/round18/index.md | W1049 | 出图原件（12 份·含 3 张重出） |
| assets/promo/plate-set/raw/round18/plate-line-100-ch050-huode-xingjun.png | W1049 | 出图原件（12 份·含 3 张重出） |
| assets/promo/plate-set/raw/round18/plate-line-101-ch055-nvguo-guowang.png | W1049 | 出图原件（12 份·含 3 张重出） |
| assets/promo/plate-set/raw/round18/plate-line-102-ch084-miefo-guowang.jpg | W1049 | 出图原件（12 份·含 3 张重出） |
| assets/promo/plate-set/raw/round18/plate-line-103-ch005-sida-tianwang.jpg | W1049 | 出图原件（12 份·含 3 张重出） |
| assets/promo/plate-set/raw/round18/plate-line-104-ch018-gao-taigong.jpg | W1049 | 出图原件（12 份·含 3 张重出） |
| assets/promo/plate-set/raw/round18/plate-line-105-ch032-yinjiao-dawang.jpg | W1049 | 出图原件（12 份·含 3 张重出） |
| assets/promo/plate-set/raw/round18/plate-line-106-ch056-shidai-yanjun.jpg | W1049 | 出图原件（12 份·含 3 张重出） |
| assets/promo/plate-set/raw/round18/plate-line-107-ch067-honglin-damang.png | W1049 | 出图原件（12 份·含 3 张重出） |
| assets/promo/plate-set/raw/round18/plate-line-108-ch058-diting.jpg | W1049 | 出图原件（12 份·含 3 张重出） |
| assets/promo/plate-set/raw/round18/plate-line-97-ch016-jinchi-zhanglao.jpg | W1049 | 出图原件（12 份·含 3 张重出） |
| assets/promo/plate-set/raw/round18/plate-line-98-ch039-wenshu-pusa.jpg | W1049 | 出图原件（12 份·含 3 张重出） |
| assets/promo/plate-set/raw/round18/plate-line-99-ch046-luli-daxian.jpg | W1049 | 出图原件（12 份·含 3 张重出） |
| docs/00-导读/W批次编号对账表.md | W1049 | 台账（认领行与收官回填） |
| docs/11-方案报告/README.md | W1049 | 方案报告（索引/架构方案） |
| docs/11-方案报告/计划方案/执行前计划-W1049-回次og-image全覆盖第五轮.md | W1049 | 方案报告（执行前计划件） |
| docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md | W1049 | 方案报告（索引/架构方案） |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1049 | 方案报告（索引/架构方案） |
| docs/agent/pitfalls.md | W1049 | 坑表（+3 条·出图接口/密排纹理/og 幂等派生） |
| scripts/output/_cascade_files_W1049.txt | W1049 | 登记面产物（索引/统计/工具清单） |
| scripts/output/_w1049_batch.json | W1049 | 本批出图批次与结果件 |
| scripts/output/_w1049_gen_all.json | W1049 | 本批出图批次与结果件 |
| scripts/output/_w1049_gen_b1.json | W1049 | 本批出图批次与结果件 |
| scripts/output/_w1049_gen_b2.json | W1049 | 本批出图批次与结果件 |
| scripts/output/_w1049_gen_b3.json | W1049 | 本批出图批次与结果件 |
| scripts/output/_w1049_gen_b4.json | W1049 | 本批出图批次与结果件 |
| scripts/output/_w1049_gen_p1.json | W1049 | 本批出图批次与结果件 |
| scripts/output/_w1049_gen_p2.json | W1049 | 本批出图批次与结果件 |
| scripts/output/_w1049_gen_probe.json | W1049 | 本批出图批次与结果件 |
| scripts/output/_w1049_pick.json | W1049 | 本批出图批次与结果件 |
| scripts/output/_w1049_reissue.json | W1049 | 本批出图批次与结果件 |
| scripts/output/_w1049_reissue_107.json | W1049 | 本批出图批次与结果件 |
| scripts/output/_w1049_reissue_97.json | W1049 | 本批出图批次与结果件 |
| scripts/output/_w1049_spec.json | W1049 | 本批出图批次与结果件 |
| scripts/output/file-index.md | W1049 | 登记面产物（索引/统计/工具清单） |
| scripts/output/stats-changelog.json | W1049 | 登记面产物（索引/统计/工具清单） |
| scripts/output/stats-index.md | W1049 | 登记面产物（索引/统计/工具清单） |
| scripts/output/stats.json | W1049 | 登记面产物（索引/统计/工具清单） |
| site/reader/ch005.html | W1049 | 缺口回目页接入题图 + 换专属 og:image |
| site/reader/ch016.html | W1049 | 缺口回目页接入题图 + 换专属 og:image |
| site/reader/ch018.html | W1049 | 缺口回目页接入题图 + 换专属 og:image |
| site/reader/ch032.html | W1049 | 缺口回目页接入题图 + 换专属 og:image |
| site/reader/ch039.html | W1049 | 缺口回目页接入题图 + 换专属 og:image |
| site/reader/ch046.html | W1049 | 缺口回目页接入题图 + 换专属 og:image |
| site/reader/ch050.html | W1049 | 缺口回目页接入题图 + 换专属 og:image |
| site/reader/ch055.html | W1049 | 缺口回目页接入题图 + 换专属 og:image |
| site/reader/ch056.html | W1049 | 缺口回目页接入题图 + 换专属 og:image |
| site/reader/ch058.html | W1049 | 缺口回目页接入题图 + 换专属 og:image |
| site/reader/ch067.html | W1049 | 缺口回目页接入题图 + 换专属 og:image |
| site/reader/ch084.html | W1049 | 缺口回目页接入题图 + 换专属 og:image |
| site/static/images/README.md | W1049 | 本批新增/修改 |
| site/static/images/index.md | W1049 | 本批新增/修改 |
| site/static/images/og-plate-line-100-ch050-huode-xingjun.webp | W1049 | 专属 og:image（1200×630） |
| site/static/images/og-plate-line-101-ch055-nvguo-guowang.webp | W1049 | 专属 og:image（1200×630） |
| site/static/images/og-plate-line-102-ch084-miefo-guowang.webp | W1049 | 专属 og:image（1200×630） |
| site/static/images/og-plate-line-103-ch005-sida-tianwang.webp | W1049 | 专属 og:image（1200×630） |
| site/static/images/og-plate-line-104-ch018-gao-taigong.webp | W1049 | 专属 og:image（1200×630） |
| site/static/images/og-plate-line-105-ch032-yinjiao-dawang.webp | W1049 | 专属 og:image（1200×630） |
| site/static/images/og-plate-line-106-ch056-shidai-yanjun.webp | W1049 | 专属 og:image（1200×630） |
| site/static/images/og-plate-line-107-ch067-honglin-damang.webp | W1049 | 专属 og:image（1200×630） |
| site/static/images/og-plate-line-108-ch058-diting.webp | W1049 | 专属 og:image（1200×630） |
| site/static/images/og-plate-line-97-ch016-jinchi-zhanglao.webp | W1049 | 专属 og:image（1200×630） |
| site/static/images/og-plate-line-98-ch039-wenshu-pusa.webp | W1049 | 专属 og:image（1200×630） |
| site/static/images/og-plate-line-99-ch046-luli-daxian.webp | W1049 | 专属 og:image（1200×630） |
| site/static/images/plate-line-100-ch050-huode-xingjun.webp | W1049 | 站点版（母版裁切·只裁上部留白） |
| site/static/images/plate-line-101-ch055-nvguo-guowang.webp | W1049 | 站点版（母版裁切·只裁上部留白） |
| site/static/images/plate-line-102-ch084-miefo-guowang.webp | W1049 | 站点版（母版裁切·只裁上部留白） |
| site/static/images/plate-line-103-ch005-sida-tianwang.webp | W1049 | 站点版（母版裁切·只裁上部留白） |
| site/static/images/plate-line-104-ch018-gao-taigong.webp | W1049 | 站点版（母版裁切·只裁上部留白） |
| site/static/images/plate-line-105-ch032-yinjiao-dawang.webp | W1049 | 站点版（母版裁切·只裁上部留白） |
| site/static/images/plate-line-106-ch056-shidai-yanjun.webp | W1049 | 站点版（母版裁切·只裁上部留白） |
| site/static/images/plate-line-107-ch067-honglin-damang.webp | W1049 | 站点版（母版裁切·只裁上部留白） |
| site/static/images/plate-line-108-ch058-diting.webp | W1049 | 站点版（母版裁切·只裁上部留白） |
| site/static/images/plate-line-97-ch016-jinchi-zhanglao.webp | W1049 | 站点版（母版裁切·只裁上部留白） |
| site/static/images/plate-line-98-ch039-wenshu-pusa.webp | W1049 | 站点版（母版裁切·只裁上部留白） |
| site/static/images/plate-line-99-ch046-luli-daxian.webp | W1049 | 站点版（母版裁切·只裁上部留白） |

## W1048 P2 治理与孤儿批收编（2026-10-31）

| 文件 | W | 说明 |
|---|---|---|
| CLAUDE.md | W1048 | 本批新增/修改（P2·补铁律 15/16/17 速查行·49/60 行） |
| docs/agent/gates.md | W1048 | 本批新增/修改（P2·计数旧值 615→616·四源印证） |
| scripts/check_doc_sync.py | W1048 | W1044 收编（C5e 坑表六主题分项逐项对拍·fail-closed） |
| scripts/check_plan_template.py | W1048 | W1044 收编（计划目录卫生判据·拦无 .md 扩展名/0 字节坏件） |
| pytest.ini | W1048 | W1044 收编（pytest_collected 1085→1087 标记跟随） |
| scripts/output/_vermilion_solid_cache.json | W1048 | 登记面产物（第 49 槽机器缓存自跟随） |
| archive/scripts/batches/w10xx/_w1013_download.py | W1048 | W1044 收编（minimax 回退清除·铁律 16③） |
| archive/scripts/batches/w10xx/_w1018_download.py | W1048 | W1044 收编（minimax 回退清除·铁律 16③） |
| archive/scripts/batches/w10xx/_w1043_download.py | W1048 | W1044 收编（minimax 回退清除·铁律 16③） |
| archive/scripts/batches/w10xx/_w1043_make_spec.py | W1048 | W1044 收编（minimax 回退清除·铁律 16③） |
| archive/scripts/batches/w10xx/_w1043_master.py | W1048 | W1044 收编（minimax 回退清除·铁律 16③） |
| archive/scripts/batches/w10xx/_w1043_pick.py | W1048 | W1044 收编（minimax 回退清除·铁律 16③） |
| archive/scripts/batches/w10xx/_w1043_prepare.py | W1048 | W1044 收编（minimax 回退清除·铁律 16③） |
| archive/scripts/batches/w10xx/_w1043_verify.py | W1048 | W1044 收编（minimax 回退清除·铁律 16③） |
| archive/scripts/batches/w10xx/_w1044_make_spec.py | W1048 | W1044 收编（本批 spec 生成器归档） |
| docs/11-方案报告/计划方案/执行前计划-W1043-回次og-image全覆盖第四轮.md | W1048 | W1043 收官口径订正（slug 111→112·随本批入库） |
| docs/11-方案报告/计划方案/执行前计划-W1046-补丁治理与门禁判据加固.md | W1048 | W1046 收编（方案件入库·只出方案不实施·待用户审批） |
| docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md | W1048 | 登记面产物（stats 标记自动跟随·W1047 收官余波随本批入库） |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1048 | 登记面产物（stats 标记自动跟随·W1047 收官余波随本批入库） |
| CHANGELOG.md | W1048 | 收官面（顶段 W1048·含 W1047 段订正注） |
| HANDOVER.md | W1048 | 收官面（最后更新/一、当前进度/四、待办正式登记） |
| README.md | W1048 | 级联面（版本行） |
| STRUCTURE.md | W1048 | 级联面（版本行） |
| AGENTS.md | W1048 | 级联面（脚注滚动） |
| CITATION.cff | W1048 | 级联面（版本同步） |
| docs/00-导读/项目说明.md | W1048 | 级联面（当前版本行） |
| docs/00-导读/W批次编号对账表.md | W1048 | 台账（W1044 行补·W1046 行回填·W1048 行新增） |
| docs/INDEX.md | W1048 | 登记面（docs 索引） |
| index.md | W1048 | 登记面（根索引） |
| archive/docs/AGENTS-ARCHIVE.md | W1048 | 级联归档滚动 |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1048 | 级联归档滚动 |
| scripts/output/stats.json | W1048 | 登记面产物（stats 实体） |
| scripts/output/stats-changelog.json | W1048 | 登记面产物（变更史） |
| scripts/output/stats-index.md | W1048 | 登记面产物（统计索引） |
| scripts/output/file-index.md | W1048 | 登记面产物（反向索引） |
| scripts/output/index.md | W1048 | 登记面产物（output 索引） |
| scripts/output/tools-inventory.md | W1048 | 登记面产物（工具清单） |
| scripts/output/README.md | W1048 | 登记面产物（output 说明） |
| scripts/output/_cascade_files_W1048.txt | W1048 | 级联清单（本批产物） |
| scripts/output/_w1048_spec.json | W1048 | 本批 spec |

## W1047 图表判据剥标签根修（2026-10-31）

| 文件 | W | 说明 |
|---|---|---|
| .agent/skills/puti-shouye/SKILL.md | W1045 | 本批新增/修改 |
| .github/workflows/README.md | W1045 | 本批新增/修改 |
| AGENTS.md | W1045 | 本批新增/修改 |
| CHANGELOG.md | W1045 | 本批新增/修改 |
| CITATION.cff | W1045 | 本批新增/修改 |
| HANDOVER.md | W1045 | 本批新增/修改 |
| README.md | W1045 | 本批新增/修改 |
| STRUCTURE.md | W1045 | 本批新增/修改 |
| archive/docs/AGENTS-ARCHIVE.md | W1045 | 本批新增/修改 |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1045 | 本批新增/修改 |
| archive/scripts/batches/w10xx/README.md | W1045 | 本批新增/修改 |
| archive/scripts/batches/w10xx/_w1047_make_spec.py | W1045 | 本批新增/修改 |
| archive/scripts/batches/w10xx/index.md | W1045 | 本批新增/修改 |
| docs/00-导读/W批次编号对账表.md | W1045 | 台账（认领行与收官回填） |
| docs/00-导读/项目说明.md | W1045 | 台账（认领行与收官回填） |
| docs/11-方案报告/计划方案/执行前计划-W1047-图表判据剥标签根修.md | W1045 | 方案报告（执行前计划 + 复核报告 / README 登记归位与件数实算） |
| docs/INDEX.md | W1045 | 本批新增/修改 |
| docs/agent/pitfalls.md | W1045 | 治理面（槽数口径 / 坑表 +5 条） |
| index.md | W1045 | 本批新增/修改 |
| scripts/batch_cascade.py | W1045 | 级联工具（上一批成果·本批未改） |
| scripts/check_chart_data.py | W1045 | 图表判据（剥标签按语法约束 + 注释优先剥离 + 2 例可证伪锁） |
| scripts/output/README.md | W1045 | 登记面产物（索引/统计/工具清单） |
| scripts/output/_cascade_files_W1047.txt | W1045 | 登记面产物（索引/统计/工具清单） |
| scripts/output/_w1047_spec.json | W1045 | 登记面产物（索引/统计/工具清单） |
| scripts/output/file-index.md | W1045 | 登记面产物（索引/统计/工具清单） |
| scripts/output/index.md | W1045 | 登记面产物（索引/统计/工具清单） |
| scripts/output/stats-changelog.json | W1045 | 登记面产物（索引/统计/工具清单） |
| scripts/output/stats-index.md | W1045 | 登记面产物（索引/统计/工具清单） |
| scripts/output/stats.json | W1045 | 登记面产物（索引/统计/工具清单） |
| scripts/output/tools-inventory.md | W1045 | 登记面产物（索引/统计/工具清单） |
| site/data/cross-time-danmaku.html | W1045 | 本批新增/修改 |
| site/data/search.html | W1045 | 本批新增/修改 |
| site/data/tag-cloud.html | W1045 | 本批新增/修改 |
| site/dukou-engine.html | W1045 | 本批新增/修改 |
| site/en/search.html | W1045 | 本批新增/修改 |
| site/index.html | W1045 | 本批新增/修改 |

## W1045 改写面候选逐处复核 + 存量陈旧清理 + og 切头 A+ 修复（2026-10-31）

| 文件 | W | 说明 |
|---|---|---|
| .agent/skills/puti-shouye/SKILL.md | W1045 | 本批新增/修改 |
| .github/workflows/README.md | W1045 | 本批新增/修改 |
| AGENTS.md | W1045 | 本批新增/修改 |
| CHANGELOG.md | W1045 | 本批新增/修改 |
| CITATION.cff | W1045 | 本批新增/修改 |
| HANDOVER.md | W1045 | 本批新增/修改 |
| README.md | W1045 | 本批新增/修改 |
| STRUCTURE.md | W1045 | 本批新增/修改 |
| archive/docs/AGENTS-ARCHIVE.md | W1045 | 本批新增/修改 |
| archive/docs/CHANGELOG-ARCHIVE.md | W1045 | 本批新增/修改 |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1045 | 本批新增/修改 |
| archive/docs/file-index-ARCHIVE.md | W1045 | 本批新增/修改 |
| archive/scripts/batches/w10xx/README.md | W1045 | 本批新增/修改 |
| archive/scripts/batches/w10xx/_w1042_make_spec.py | W1045 | 本批新增/修改 |
| archive/scripts/batches/w10xx/_w1045_make_spec.py | W1045 | 本批新增/修改 |
| archive/scripts/batches/w10xx/index.md | W1045 | 本批新增/修改 |
| archive/scripts/batches/w6xx/_w661_close_cascade.py | W1045 | 归档件·跨行吞并真缺陷修复（两处排除符补换行符） |
| archive/scripts/batches/w6xx/_w662_close_cascade.py | W1045 | 归档件·跨行吞并真缺陷修复（两处排除符补换行符） |
| archive/scripts/batches/w6xx/_w663_close_cascade.py | W1045 | 归档件·跨行吞并真缺陷修复（两处排除符补换行符） |
| archive/scripts/batches/w6xx/_w666_close_cascade.py | W1045 | 归档件·跨行吞并真缺陷修复（两处排除符补换行符） |
| archive/scripts/batches/w6xx/_w667_close_cascade.py | W1045 | 归档件·跨行吞并真缺陷修复（两处排除符补换行符） |
| archive/scripts/batches/w6xx/_w668_close_cascade.py | W1045 | 归档件·跨行吞并真缺陷修复（两处排除符补换行符） |
| archive/scripts/batches/w6xx/_w669_close_cascade.py | W1045 | 归档件·跨行吞并真缺陷修复（两处排除符补换行符） |
| archive/scripts/batches/w6xx/_w670_close_cascade.py | W1045 | 归档件·跨行吞并真缺陷修复（两处排除符补换行符） |
| archive/scripts/batches/w6xx/_w671_close_cascade.py | W1045 | 归档件·跨行吞并真缺陷修复（两处排除符补换行符） |
| archive/scripts/batches/w6xx/_w676_close_cascade.py | W1045 | 归档件·跨行吞并真缺陷修复（两处排除符补换行符） |
| archive/scripts/batches/w6xx/_w679_close_cascade.py | W1045 | 归档件·跨行吞并真缺陷修复（两处排除符补换行符） |
| archive/scripts/batches/w6xx/_w684_close_cascade.py | W1045 | 归档件·跨行吞并真缺陷修复（两处排除符补换行符） |
| archive/scripts/batches/w6xx/_w691_close_cascade.py | W1045 | 归档件·跨行吞并真缺陷修复（两处排除符补换行符） |
| docs/00-导读/W批次编号对账表.md | W1045 | 台账（认领行与收官回填） |
| docs/00-导读/项目说明.md | W1045 | 台账（认领行与收官回填） |
| docs/11-方案报告/README.md | W1045 | 方案报告（执行前计划 + 复核报告 / README 登记归位与件数实算） |
| docs/11-方案报告/审查与评审/改写面候选逐处复核与存量陈旧清理报告-W1045.md | W1045 | 方案报告（执行前计划 + 复核报告 / README 登记归位与件数实算） |
| docs/11-方案报告/计划方案/执行前计划-W1045-改写面候选逐处复核与存量陈旧清理.md | W1045 | 方案报告（执行前计划 + 复核报告 / README 登记归位与件数实算） |
| docs/INDEX.md | W1045 | 本批新增/修改 |
| docs/agent/gates.md | W1045 | 治理面（槽数口径 / 坑表 +5 条） |
| docs/agent/pitfalls.md | W1045 | 治理面（槽数口径 / 坑表 +5 条） |
| index.md | W1045 | 本批新增/修改 |
| scripts/README.md | W1045 | 本批新增/修改 |
| scripts/batch_cascade.py | W1045 | 级联工具（CITATION.cff 面补行数断言） |
| scripts/check_crop.py | W1045 | og 裁切根修与判据加固（配套 A+ 修复·本批核实后入库） |
| scripts/check_cross_line_rewrite.py | W1045 | 跨行扫描器（基线键升四输入 + 跨行判定补 \s 盲区） |
| scripts/cross_line_baseline.json | W1045 | 跨行判据基线（四输入键·失效项已清理） |
| scripts/output/README.md | W1045 | 登记面产物（索引/统计/工具清单） |
| scripts/output/_cascade_files_W1045.txt | W1045 | 登记面产物（索引/统计/工具清单） |
| scripts/output/_vermilion_solid_cache.json | W1045 | 登记面产物（索引/统计/工具清单） |
| scripts/output/_w1043_batch_a.json | W1045 | 登记面产物（索引/统计/工具清单） |
| scripts/output/_w1045_spec.json | W1045 | 登记面产物（索引/统计/工具清单） |
| scripts/output/file-index.md | W1045 | 登记面产物（索引/统计/工具清单） |
| scripts/output/index.md | W1045 | 登记面产物（索引/统计/工具清单） |
| scripts/output/stats-changelog.json | W1045 | 登记面产物（索引/统计/工具清单） |
| scripts/output/stats-index.md | W1045 | 登记面产物（索引/统计/工具清单） |
| scripts/output/stats.json | W1045 | 登记面产物（索引/统计/工具清单） |
| scripts/output/tools-inventory.md | W1045 | 登记面产物（索引/统计/工具清单） |
| scripts/subject_band.py | W1045 | og 裁切根修与判据加固（配套 A+ 修复·本批核实后入库） |
| site/data/cross-time-danmaku.html | W1045 | 本批新增/修改 |
| site/data/search.html | W1045 | 本批新增/修改 |
| site/data/tag-cloud.html | W1045 | 本批新增/修改 |
| site/dukou-engine.html | W1045 | 本批新增/修改 |
| site/en/search.html | W1045 | 本批新增/修改 |
| site/index.html | W1045 | 本批新增/修改 |
| site/static/images/og-plate-line-59-ch089-huangshi.webp | W1045 | og 社交卡（A+ 保留：真被切者修复·其余回退） |
| site/static/images/og-plate-line-81-ch074-qingshi.webp | W1045 | og 社交卡（A+ 保留：真被切者修复·其余回退） |
| site/static/images/og-plate-line-85-ch053-ruyizhenxian.webp | W1045 | og 社交卡（A+ 保留：真被切者修复·其余回退） |
| site/static/images/og-plate-line-87-ch094-taiyinxingjun.webp | W1045 | og 社交卡（A+ 保留：真被切者修复·其余回退） |
| site/static/images/og-plate-line-88-ch073-duomuguai.webp | W1045 | og 社交卡（A+ 保留：真被切者修复·其余回退） |
| site/static/images/og-plate-line-90-ch090-yijiukutianzun.webp | W1045 | og 社交卡（A+ 保留：真被切者修复·其余回退） |
| site/static/images/og-plate-line-91-ch071-jiuling-shiba.webp | W1045 | og 社交卡（A+ 保留：真被切者修复·其余回退） |
| site/static/images/og-plate-line-92-ch086-bihan-bishu.webp | W1045 | og 社交卡（A+ 保留：真被切者修复·其余回退） |
| site/static/images/og-plate-line-93-ch095-yumian.webp | W1045 | og 社交卡（A+ 保留：真被切者修复·其余回退） |
| site/static/images/og-plate-line-94-ch029-bengpo-baboren.webp | W1045 | og 社交卡（A+ 保留：真被切者修复·其余回退） |
| site/static/images/og-plate-line-95-ch085-diyongfuren.webp | W1045 | og 社交卡（A+ 保留：真被切者修复·其余回退） |
| site/static/images/og-plate-line-96-ch097-xiniu.webp | W1045 | og 社交卡（A+ 保留：真被切者修复·其余回退） |
| tests/unit/test_cross_line_rewrite.py | W1045 | 键口径回归锁（4 条） |

## W1043 回次 og:image 全覆盖批·第四轮（2026-10-31）

| 文件 | W | 说明 |
|---|---|---|
| .agent/skills/puti-shouye/SKILL.md | W1043 | 本批新增/修改 |
| .github/workflows/README.md | W1043 | 本批新增/修改 |
| AGENTS.md | W1043 | 本批新增/修改 |
| CHANGELOG.md | W1043 | 本批新增/修改 |
| CITATION.cff | W1043 | 本批新增/修改 |
| HANDOVER.md | W1043 | 本批新增/修改 |
| README.md | W1043 | 本批新增/修改 |
| STRUCTURE.md | W1043 | 本批新增/修改 |
| archive/docs/AGENTS-ARCHIVE.md | W1043 | 本批新增/修改 |
| archive/docs/CHANGELOG-ARCHIVE.md | W1043 | 本批新增/修改 |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1043 | 本批新增/修改 |
| archive/docs/file-index-ARCHIVE.md | W1043 | 本批新增/修改 |
| archive/scripts/batches/misc/_localize_cdn_libs.py | W1043 | 归档件·跨行删改真缺陷修复（排除符补换行符） |
| archive/scripts/batches/w10xx/README.md | W1043 | 本批新增/修改 |
| archive/scripts/batches/w10xx/_w1042_make_spec.py | W1043 | 本批新增/修改 |
| archive/scripts/batches/w10xx/_w1043_derive_prepare.py | W1043 | 本批工具脚本（归档批次区） |
| archive/scripts/batches/w10xx/_w1043_derive_stage.py | W1043 | 本批工具脚本（归档批次区） |
| archive/scripts/batches/w10xx/_w1043_derive_verify.py | W1043 | 本批工具脚本（归档批次区） |
| archive/scripts/batches/w10xx/_w1043_download.py | W1043 | 本批工具脚本（归档批次区） |
| archive/scripts/batches/w10xx/_w1043_make_spec.py | W1043 | 本批工具脚本（归档批次区） |
| archive/scripts/batches/w10xx/_w1043_master.py | W1043 | 本批工具脚本（归档批次区） |
| archive/scripts/batches/w10xx/_w1043_pick.py | W1043 | 本批工具脚本（归档批次区） |
| archive/scripts/batches/w10xx/_w1043_prepare.py | W1043 | 本批工具脚本（归档批次区） |
| archive/scripts/batches/w10xx/_w1043_probe_pages.py | W1043 | 本批工具脚本（归档批次区） |
| archive/scripts/batches/w10xx/_w1043_sheet.py | W1043 | 本批工具脚本（归档批次区） |
| archive/scripts/batches/w10xx/_w1043_stage.py | W1043 | 本批工具脚本（归档批次区） |
| archive/scripts/batches/w10xx/_w1043_verify.py | W1043 | 本批工具脚本（归档批次区） |
| archive/scripts/batches/w10xx/index.md | W1043 | 本批新增/修改 |
| archive/scripts/batches/w4xx/_w478_migrate.py | W1043 | 归档件·跨行删改真缺陷修复（排除符补换行符） |
| archive/scripts/batches/w4xx/_w490_migrate.py | W1043 | 归档件·跨行删改真缺陷修复（排除符补换行符） |
| archive/scripts/batches/w4xx/_w491_en_migrate.py | W1043 | 归档件·跨行删改真缺陷修复（排除符补换行符） |
| archive/scripts/batches/w9xx/_w974_cascade.py | W1043 | 归档件·跨行删改真缺陷修复（排除符补换行符） |
| assets/promo/plate-set/index.md | W1043 | 本批新增/修改 |
| assets/promo/plate-set/plate-line-85-ch053-ruyizhenxian.png | W1043 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-85-ch053-ruyizhenxian.webp | W1043 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-86-ch033-chuikouxian.png | W1043 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-86-ch033-chuikouxian.webp | W1043 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-87-ch094-taiyinxingjun.png | W1043 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-87-ch094-taiyinxingjun.webp | W1043 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-88-ch073-duomuguai.png | W1043 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-88-ch073-duomuguai.webp | W1043 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-89-ch069-ziyangzhenren.png | W1043 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-89-ch069-ziyangzhenren.webp | W1043 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-90-ch090-yijiukutianzun.png | W1043 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-90-ch090-yijiukutianzun.webp | W1043 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-91-ch071-jiuling-shiba.png | W1043 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-91-ch071-jiuling-shiba.webp | W1043 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-92-ch086-bihan-bishu.png | W1043 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-92-ch086-bihan-bishu.webp | W1043 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-93-ch095-yumian.png | W1043 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-93-ch095-yumian.webp | W1043 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-94-ch029-bengpo-baboren.png | W1043 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-94-ch029-bengpo-baboren.webp | W1043 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-95-ch085-diyongfuren.png | W1043 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-95-ch085-diyongfuren.webp | W1043 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-96-ch097-xiniu.png | W1043 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-96-ch097-xiniu.webp | W1043 | 新增母版（1200×1600） |
| assets/promo/plate-set/preview-contact-sheet.png | W1043 | 拼图预览（含本批 12 张） |
| assets/promo/plate-set/preview-contact-sheet.webp | W1043 | 拼图预览（含本批 12 张） |
| assets/promo/plate-set/preview-w1043-sheet.png | W1043 | 拼图预览（本批 12 张） |
| assets/promo/plate-set/raw/README.md | W1043 | 本批新增/修改 |
| assets/promo/plate-set/raw/index.md | W1043 | 本批新增/修改 |
| assets/promo/plate-set/raw/round17/README.md | W1043 | 出图原件（12 份·含 1 张重出） |
| assets/promo/plate-set/raw/round17/index.md | W1043 | 出图原件（12 份·含 1 张重出） |
| assets/promo/plate-set/raw/round17/plate-line-85-ch053-ruyizhenxian.jpg | W1043 | 出图原件（12 份·含 1 张重出） |
| assets/promo/plate-set/raw/round17/plate-line-86-ch033-chuikouxian.jpg | W1043 | 出图原件（12 份·含 1 张重出） |
| assets/promo/plate-set/raw/round17/plate-line-87-ch094-taiyinxingjun.jpg | W1043 | 出图原件（12 份·含 1 张重出） |
| assets/promo/plate-set/raw/round17/plate-line-88-ch073-duomuguai.jpg | W1043 | 出图原件（12 份·含 1 张重出） |
| assets/promo/plate-set/raw/round17/plate-line-89-ch069-ziyangzhenren.jpg | W1043 | 出图原件（12 份·含 1 张重出） |
| assets/promo/plate-set/raw/round17/plate-line-90-ch090-yijiukutianzun.png | W1043 | 出图原件（12 份·含 1 张重出） |
| assets/promo/plate-set/raw/round17/plate-line-91-ch071-jiuling-shiba.png | W1043 | 出图原件（12 份·含 1 张重出） |
| assets/promo/plate-set/raw/round17/plate-line-92-ch086-bihan-bishu.jpg | W1043 | 出图原件（12 份·含 1 张重出） |
| assets/promo/plate-set/raw/round17/plate-line-93-ch095-yumian.jpg | W1043 | 出图原件（12 份·含 1 张重出） |
| assets/promo/plate-set/raw/round17/plate-line-94-ch029-bengpo-baboren.jpg | W1043 | 出图原件（12 份·含 1 张重出） |
| assets/promo/plate-set/raw/round17/plate-line-95-ch085-diyongfuren.jpg | W1043 | 出图原件（12 份·含 1 张重出） |
| assets/promo/plate-set/raw/round17/plate-line-96-ch097-xiniu.jpg | W1043 | 出图原件（12 份·含 1 张重出） |
| docs/00-导读/W批次编号对账表.md | W1043 | 台账（认领行与收官回填） |
| docs/00-导读/项目说明.md | W1043 | 台账（认领行与收官回填） |
| docs/11-方案报告/README.md | W1043 | 方案报告（目录索引·W1044 订正说明列） |
| docs/11-方案报告/计划方案/执行前计划-W1043-回次og-image全覆盖第四轮.md | W1043 | 方案报告（执行前计划件） |
| docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md | W1043 | 方案报告（架构方案·stats report_docs 标记级联） |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1043 | 方案报告（架构方案·stats report_docs 标记级联） |
| docs/INDEX.md | W1043 | 本批新增/修改 |
| docs/agent/pitfalls.md | W1043 | 坑表（+1 条·判据脆性） |
| scripts/_w1042_make_spec.py | W1043 | 本批改名·旧名（已由 archive/scripts/batches/w10xx/_w1042_make_spec.py 取代） |
| scripts/check_cross_line_rewrite.py | W1043 | 本批新增/修改 |
| scripts/cross_line_baseline.json | W1043 | 本批新增/修改 |
| scripts/index.md | W1043 | 本批新增/修改 |
| scripts/output/README.md | W1043 | 登记面产物（索引/统计/工具清单） |
| scripts/output/_cascade_files_W1043.txt | W1043 | 登记面产物（索引/统计/工具清单） |
| scripts/output/_vermilion_solid_cache.json | W1043 | 登记面产物（索引/统计/工具清单） |
| scripts/output/_w1043_batch.json | W1043 | 本批出图批次与结果件 |
| scripts/output/_w1043_batch_a.json | W1043 | 本批出图批次与结果件 |
| scripts/output/_w1043_batch_b.json | W1043 | 本批出图批次与结果件 |
| scripts/output/_w1043_batch_c.json | W1043 | 本批出图批次与结果件 |
| scripts/output/_w1043_gen_a.json | W1043 | 本批出图批次与结果件 |
| scripts/output/_w1043_gen_b.json | W1043 | 本批出图批次与结果件 |
| scripts/output/_w1043_gen_c.json | W1043 | 本批出图批次与结果件 |
| scripts/output/_w1043_spec.json | W1043 | 本批出图批次与结果件 |
| scripts/output/file-index.md | W1043 | 登记面产物（索引/统计/工具清单） |
| scripts/output/index.md | W1043 | 登记面产物（索引/统计/工具清单） |
| scripts/output/stats-changelog.json | W1043 | 登记面产物（索引/统计/工具清单） |
| scripts/output/stats-index.md | W1043 | 登记面产物（索引/统计/工具清单） |
| scripts/output/stats.json | W1043 | 登记面产物（索引/统计/工具清单） |
| scripts/output/tools-inventory.md | W1043 | 登记面产物（索引/统计/工具清单） |
| site/data/cross-time-danmaku.html | W1043 | 本批新增/修改 |
| site/data/search.html | W1043 | 本批新增/修改 |
| site/data/tag-cloud.html | W1043 | 本批新增/修改 |
| site/dukou-engine.html | W1043 | 本批新增/修改 |
| site/en/search.html | W1043 | 本批新增/修改 |
| site/index.html | W1043 | 本批新增/修改 |
| site/reader/ch029.html | W1043 | 缺口回目页接入题图 + 换专属 og:image |
| site/reader/ch033.html | W1043 | 缺口回目页接入题图 + 换专属 og:image |
| site/reader/ch053.html | W1043 | 缺口回目页接入题图 + 换专属 og:image |
| site/reader/ch069.html | W1043 | 缺口回目页接入题图 + 换专属 og:image |
| site/reader/ch071.html | W1043 | 缺口回目页接入题图 + 换专属 og:image |
| site/reader/ch073.html | W1043 | 缺口回目页接入题图 + 换专属 og:image |
| site/reader/ch085.html | W1043 | 缺口回目页接入题图 + 换专属 og:image |
| site/reader/ch086.html | W1043 | 缺口回目页接入题图 + 换专属 og:image |
| site/reader/ch090.html | W1043 | 缺口回目页接入题图 + 换专属 og:image |
| site/reader/ch094.html | W1043 | 缺口回目页接入题图 + 换专属 og:image |
| site/reader/ch095.html | W1043 | 缺口回目页接入题图 + 换专属 og:image |
| site/reader/ch097.html | W1043 | 缺口回目页接入题图 + 换专属 og:image |
| site/static/images/README.md | W1043 | 本批新增/修改 |
| site/static/images/index.md | W1043 | 本批新增/修改 |
| site/static/images/og-plate-line-85-ch053-ruyizhenxian.webp | W1043 | 专属 og:image（1200×630） |
| site/static/images/og-plate-line-86-ch033-chuikouxian.webp | W1043 | 专属 og:image（1200×630） |
| site/static/images/og-plate-line-87-ch094-taiyinxingjun.webp | W1043 | 专属 og:image（1200×630） |
| site/static/images/og-plate-line-88-ch073-duomuguai.webp | W1043 | 专属 og:image（1200×630） |
| site/static/images/og-plate-line-89-ch069-ziyangzhenren.webp | W1043 | 专属 og:image（1200×630） |
| site/static/images/og-plate-line-90-ch090-yijiukutianzun.webp | W1043 | 专属 og:image（1200×630） |
| site/static/images/og-plate-line-91-ch071-jiuling-shiba.webp | W1043 | 专属 og:image（1200×630） |
| site/static/images/og-plate-line-92-ch086-bihan-bishu.webp | W1043 | 专属 og:image（1200×630） |
| site/static/images/og-plate-line-93-ch095-yumian.webp | W1043 | 专属 og:image（1200×630） |
| site/static/images/og-plate-line-94-ch029-bengpo-baboren.webp | W1043 | 专属 og:image（1200×630） |
| site/static/images/og-plate-line-95-ch085-diyongfuren.webp | W1043 | 专属 og:image（1200×630） |
| site/static/images/og-plate-line-96-ch097-xiniu.webp | W1043 | 专属 og:image（1200×630） |
| site/static/images/plate-line-85-ch053-ruyizhenxian.webp | W1043 | 站点版（母版裁切·只裁上部留白） |
| site/static/images/plate-line-86-ch033-chuikouxian.webp | W1043 | 站点版（母版裁切·只裁上部留白） |
| site/static/images/plate-line-87-ch094-taiyinxingjun.webp | W1043 | 站点版（母版裁切·只裁上部留白） |
| site/static/images/plate-line-88-ch073-duomuguai.webp | W1043 | 站点版（母版裁切·只裁上部留白） |
| site/static/images/plate-line-89-ch069-ziyangzhenren.webp | W1043 | 站点版（母版裁切·只裁上部留白） |
| site/static/images/plate-line-90-ch090-yijiukutianzun.webp | W1043 | 站点版（母版裁切·只裁上部留白） |
| site/static/images/plate-line-91-ch071-jiuling-shiba.webp | W1043 | 站点版（母版裁切·只裁上部留白） |
| site/static/images/plate-line-92-ch086-bihan-bishu.webp | W1043 | 站点版（母版裁切·只裁上部留白） |
| site/static/images/plate-line-93-ch095-yumian.webp | W1043 | 站点版（母版裁切·只裁上部留白） |
| site/static/images/plate-line-94-ch029-bengpo-baboren.webp | W1043 | 站点版（母版裁切·只裁上部留白） |
| site/static/images/plate-line-95-ch085-diyongfuren.webp | W1043 | 站点版（母版裁切·只裁上部留白） |
| site/static/images/plate-line-96-ch097-xiniu.webp | W1043 | 站点版（母版裁切·只裁上部留白） |

## W1042 工具面根因修复与判据补覆盖批（2026-10-30）

| 文件 | W | 说明 |
|---|---|---|
| .agent/skills/puti-shouye/SKILL.md | W1042 | 本批新增/修改 |
| .github/workflows/README.md | W1042 | 本批新增/修改 |
| AGENTS.md | W1042 | 计数链同步（坑表条数指针） |
| CHANGELOG.md | W1042 | 本批新增/修改 |
| CITATION.cff | W1042 | 本批新增/修改 |
| HANDOVER.md | W1042 | 计数链同步（坑表条数指针） |
| Makefile | W1042 | 本地 CI 编排（完成提示归位） |
| README.md | W1042 | 本批新增/修改 |
| STRUCTURE.md | W1042 | 本批新增/修改 |
| archive/docs/AGENTS-ARCHIVE.md | W1042 | 本批新增/修改 |
| archive/docs/CHANGELOG-ARCHIVE.md | W1042 | 本批新增/修改 |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1042 | 本批新增/修改 |
| archive/docs/file-index-ARCHIVE.md | W1042 | 本批新增/修改 |
| docs/00-导读/W批次编号对账表.md | W1042 | 台账（认领行与收官回填） |
| docs/00-导读/项目说明.md | W1042 | 台账（认领行与收官回填） |
| docs/11-方案报告/审查与评审/跨行改写面逐处复核报告-2026-10-30.md | W1042 | 方案报告（执行前计划 + 复盘报告） |
| docs/11-方案报告/工作复盘与优化分析报告/工作复盘与优化分析报告-2026-10-30.md | W1042 | 方案报告（执行前计划 + 复盘报告） |
| docs/11-方案报告/计划方案/执行前计划-W1042-工具面根因修复与判据补覆盖.md | W1042 | 方案报告（执行前计划 + 复盘报告） |
| docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md | W1042 | 方案报告（执行前计划 + 复盘报告） |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1042 | 方案报告（执行前计划 + 复盘报告） |
| docs/INDEX.md | W1042 | 本批新增/修改 |
| docs/agent/pitfalls.md | W1042 | 坑表（+4 条教训） |
| pytest.ini | W1042 | 本批新增/修改 |
| scripts/A_文本基础/章节切分.py | W1042 | 本批新增/修改 |
| scripts/_w1042_make_spec.py | W1042 | 本批工具脚本 |
| scripts/check_cross_line_rewrite.py | W1042 | 本批新增/修改 |
| scripts/cross_line_baseline.json | W1042 | 本批新增/修改 |
| scripts/index.md | W1042 | 本批新增/修改 |
| scripts/ledger_backfill.py | W1042 | 台账回填工具（显式参数生效根因修复） |
| scripts/output/README.md | W1042 | 登记面产物（索引/统计/工具清单） |
| scripts/output/_cascade_files_W1042.txt | W1042 | 登记面产物（索引/统计/工具清单） |
| scripts/output/_vermilion_solid_cache.json | W1042 | 登记面产物（索引/统计/工具清单） |
| scripts/output/_w1042_spec.json | W1042 | 本批 spec 与级联清单 |
| scripts/output/file-index.md | W1042 | 登记面产物（索引/统计/工具清单） |
| scripts/output/index.md | W1042 | 登记面产物（索引/统计/工具清单） |
| scripts/output/stats-changelog.json | W1042 | 登记面产物（索引/统计/工具清单） |
| scripts/output/stats-index.md | W1042 | 登记面产物（索引/统计/工具清单） |
| scripts/output/stats.json | W1042 | 登记面产物（索引/统计/工具清单） |
| scripts/output/tools-inventory.md | W1042 | 登记面产物（索引/统计/工具清单） |
| site/data/cross-time-danmaku.html | W1042 | 本批新增/修改 |
| site/data/search.html | W1042 | 本批新增/修改 |
| site/data/tag-cloud.html | W1042 | 本批新增/修改 |
| site/dukou-engine.html | W1042 | 本批新增/修改 |
| site/en/search.html | W1042 | 本批新增/修改 |
| site/index.html | W1042 | 本批新增/修改 |
| tests/unit/test_archive_segments.py | W1042 | 本批单测（判据覆盖） |
| tests/unit/test_cross_line_rewrite.py | W1042 | 本批单测（判据覆盖） |
| tests/unit/test_plan_template_read_disk.py | W1042 | 本批单测（判据覆盖） |

## W1041 批次号预约机制（2026-10-30）

| 文件 | W | 说明 |
|---|---|---|
| .github/workflows/README.md | W1041 | 本批新增/修改 |
| AGENTS.md | W1041 | 本批新增/修改 |
| CHANGELOG.md | W1041 | 本批新增/修改 |
| CITATION.cff | W1041 | 本批新增/修改 |
| HANDOVER.md | W1041 | 本批新增/修改 |
| README.md | W1041 | 本批新增/修改 |
| STRUCTURE.md | W1041 | 本批新增/修改 |
| archive/docs/AGENTS-ARCHIVE.md | W1041 | 本批新增/修改 |
| docs/00-导读/W批次编号对账表.md | W1041 | 本批新增/修改 |
| docs/00-导读/项目说明.md | W1041 | 本批新增/修改 |
| docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md | W1041 | 本批新增/修改 |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1041 | 本批新增/修改 |
| docs/agent/pitfalls.md | W1041 | 本批新增/修改 |
| scripts/output/_vermilion_solid_cache.json | W1041 | 本批新增/修改 |
| scripts/output/_w1041_spec.json | W1041 | 本批新增/修改 |
| scripts/output/file-index.md | W1041 | 本批新增/修改 |
| scripts/output/stats-changelog.json | W1041 | 本批新增/修改 |
| scripts/output/stats-index.md | W1041 | 本批新增/修改 |
| scripts/output/tools-inventory.md | W1041 | 本批新增/修改 |
| scripts/reserve_w.py | W1041 | 本批新增/修改 |
| site/index.html | W1041 | 本批新增/修改 |

## W1040 任务分级协议入库（2026-10-30）

| 文件 | W | 说明 |
|---|---|---|
| docs/10-方法论沉淀/任务分级协议.md | W1040 | 本批新增 |
| docs/10-方法论沉淀/README.md | W1040 | 索引登记第 27 号 |
| docs/11-方案报告/README.md | W1040 | §六 登记执行前计划行（T-39） |
| docs/11-方案报告/计划方案/执行前计划-W1040-任务分级协议入库.md | W1040 | 本批新增（计划归档·W1033 T05 先例·框架号 T-39） |
| docs/INDEX.md | W1040 | 索引重生成 |
| docs/00-导读/W批次编号对账表.md | W1040 | 认领登记与收官回填 |
| scripts/output/_w1040_spec.json | W1040 | 本批新增 |
| scripts/output/_cascade_files_W1040.txt | W1040 | 级联清单 |
| CHANGELOG.md | W1040 | 级联·现役段 |
| README.md | W1040 | 级联 |
| STRUCTURE.md | W1040 | 级联+stats 标记 sweep |
| HANDOVER.md | W1040 | 级联 |
| AGENTS.md | W1040 | 级联（agents_note 脚注轮换） |
| CITATION.cff | W1040 | 级联（version/date 随批） |
| docs/00-导读/项目说明.md | W1040 | 级联 |
| .github/workflows/README.md | W1040 | 级联 |
| site/index.html | W1040 | 级联 |
| site/data/cross-time-danmaku.html | W1040 | 级联 |
| site/data/tag-cloud.html | W1040 | 级联 |
| site/dukou-engine.html | W1040 | 级联 |
| site/data/search.html | W1040 | 搜索索引重建 |
| site/en/search.html | W1040 | 搜索索引重建 |
| scripts/output/file-index.md | W1040 | 级联 |
| scripts/output/stats.json | W1040 | methodology_docs 25→26 |
| archive/docs/AGENTS-ARCHIVE.md | W1040 | 回窗（脚注窗轮换时·未触发删行） |
| archive/docs/CHANGELOG-ARCHIVE.md | W1040 | 回窗（段窗轮换·上轮同窗位已触发） |
| archive/docs/file-index-ARCHIVE.md | W1040 | 回窗（段窗轮换·上轮同窗位已触发） |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1040 | 回窗（台账行窗轮换·已触发：迁出 W980-W981） |
| scripts/output/README.md | W1040 | 目录文档 refresh（scripts/output 新件触发时） |
| scripts/output/index.md | W1040 | 目录文档 refresh（同上） |
| scripts/output/tools-inventory.md | W1040 | 工具面 refresh（触发时） |

## W1039 用户级记忆五则入项目铁律（2026-10-30）

| 文件 | W | 说明 |
|---|---|---|
| .github/workflows/README.md | W1039 | 本批新增/修改 |
| AGENTS.md | W1039 | 本批新增/修改 |
| CHANGELOG.md | W1039 | 本批新增/修改 |
| CITATION.cff | W1039 | 本批新增/修改 |
| HANDOVER.md | W1039 | 本批新增/修改 |
| README.md | W1039 | 本批新增/修改 |
| STRUCTURE.md | W1039 | 本批新增/修改 |
| archive/docs/AGENTS-ARCHIVE.md | W1039 | 本批新增/修改 |
| docs/00-导读/W批次编号对账表.md | W1039 | 本批新增/修改 |
| docs/00-导读/项目说明.md | W1039 | 本批新增/修改 |
| docs/agent/pitfalls.md | W1039 | 本批新增/修改 |
| scripts/output/_w1039_spec.json | W1039 | 本批新增/修改 |
| scripts/output/file-index.md | W1039 | 本批新增/修改 |
| site/index.html | W1039 | 本批新增/修改 |

## W1038 a11y 性能优化（2026-10-30）

| 文件 | W | 说明 |
|---|---|---|
| .github/workflows/README.md | W1038 | 本批新增/修改 |
| AGENTS.md | W1038 | 本批新增/修改 |
| CHANGELOG.md | W1038 | 本批新增/修改 |
| CITATION.cff | W1038 | 本批新增/修改 |
| HANDOVER.md | W1038 | 本批新增/修改 |
| README.md | W1038 | 本批新增/修改 |
| STRUCTURE.md | W1038 | 本批新增/修改 |
| archive/docs/AGENTS-ARCHIVE.md | W1038 | 本批新增/修改 |
| docs/00-导读/W批次编号对账表.md | W1038 | 本批新增/修改 |
| docs/00-导读/项目说明.md | W1038 | 本批新增/修改 |
| scripts/a11y_audit.py | W1038 | 本批新增/修改 |
| scripts/output/_w1038_spec.json | W1038 | 本批新增/修改 |
| scripts/output/file-index.md | W1038 | 本批新增/修改 |
| site/index.html | W1038 | 本批新增/修改 |

## W1037 门禁耗时剖析（2026-10-30）

| 文件 | W | 说明 |
|---|---|---|
| .github/workflows/README.md | W1037 | 本批新增/修改 |
| AGENTS.md | W1037 | 本批新增/修改 |
| CHANGELOG.md | W1037 | 本批新增/修改 |
| CITATION.cff | W1037 | 本批新增/修改 |
| HANDOVER.md | W1037 | 本批新增/修改 |
| README.md | W1037 | 本批新增/修改 |
| STRUCTURE.md | W1037 | 本批新增/修改 |
| archive/docs/AGENTS-ARCHIVE.md | W1037 | 本批新增/修改 |
| docs/00-导读/W批次编号对账表.md | W1037 | 本批新增/修改 |
| docs/00-导读/项目说明.md | W1037 | 本批新增/修改 |
| scripts/output/_w1037_spec.json | W1037 | 本批新增/修改 |
| scripts/output/file-index.md | W1037 | 本批新增/修改 |
| scripts/verify_delivery.py | W1037 | 本批新增/修改 |
| site/index.html | W1037 | 本批新增/修改 |

## W1036 授业官 skill 按编制定名（2026-10-30）

| 文件 | W | 说明 |
|---|---|---|
| .agent/skills/puti-shouye/SKILL.md | W1036 | 本批新增/修改 |
| .agent/skills/xiyouji-guard/SKILL.md | W1036 | 本批新增/修改 |
| .github/workflows/README.md | W1036 | 本批新增/修改 |
| AGENTS.md | W1036 | 本批新增/修改 |
| CHANGELOG.md | W1036 | 本批新增/修改 |
| CITATION.cff | W1036 | 本批新增/修改 |
| HANDOVER.md | W1036 | 本批新增/修改 |
| README.md | W1036 | 本批新增/修改 |
| STRUCTURE.md | W1036 | 本批新增/修改 |
| archive/docs/AGENTS-ARCHIVE.md | W1036 | 本批新增/修改 |
| docs/00-导读/W批次编号对账表.md | W1036 | 本批新增/修改 |
| docs/00-导读/项目说明.md | W1036 | 本批新增/修改 |
| docs/11-方案报告/设计与架构方案/取经编制表-工具与技能挂位-2026-10-20.md | W1036 | 本批新增/修改 |
| scripts/output/_vermilion_solid_cache.json | W1036 | 本批新增/修改 |
| scripts/output/_w1036_spec.json | W1036 | 本批新增/修改 |
| scripts/output/file-index.md | W1036 | 本批新增/修改 |
| site/index.html | W1036 | 本批新增/修改 |

## W1035 三份职责书（2026-10-30）

| 文件 | W | 说明 |
|---|---|---|
| .github/workflows/README.md | W1035 | 本批新增/修改 |
| AGENTS.md | W1035 | 本批新增/修改 |
| CHANGELOG.md | W1035 | 本批新增/修改 |
| CITATION.cff | W1035 | 本批新增/修改 |
| HANDOVER.md | W1035 | 本批新增/修改 |
| README.md | W1035 | 本批新增/修改 |
| STRUCTURE.md | W1035 | 本批新增/修改 |
| archive/docs/AGENTS-ARCHIVE.md | W1035 | 本批新增/修改 |
| docs/00-导读/W批次编号对账表.md | W1035 | 本批新增/修改 |
| docs/00-导读/项目说明.md | W1035 | 本批新增/修改 |
| docs/agent/README.md | W1035 | 本批新增/修改 |
| docs/agent/closeout-agent-prompt.md | W1035 | 本批新增/修改 |
| docs/agent/index.md | W1035 | 本批新增/修改 |
| docs/agent/reconcile-agent-prompt.md | W1035 | 本批新增/修改 |
| docs/agent/text-audit-agent-prompt.md | W1035 | 本批新增/修改 |
| scripts/output/_w1035_spec.json | W1035 | 本批新增/修改 |
| scripts/output/file-index.md | W1035 | 本批新增/修改 |
| scripts/output/tools-inventory.md | W1035 | 本批新增/修改 |
| site/index.html | W1035 | 本批新增/修改 |

## W1034 授业官位补全（2026-10-30）

| 文件 | W | 说明 |
|---|---|---|
| .agent/skills/xiyouji-guard/SKILL.md | W1034 | 本批新增/修改 |
| .github/workflows/README.md | W1034 | 本批新增/修改 |
| .gitignore | W1034 | 本批新增/修改 |
| AGENTS.md | W1034 | 本批新增/修改 |
| CHANGELOG.md | W1034 | 本批新增/修改 |
| CITATION.cff | W1034 | 本批新增/修改 |
| HANDOVER.md | W1034 | 本批新增/修改 |
| README.md | W1034 | 本批新增/修改 |
| STRUCTURE.md | W1034 | 本批新增/修改 |
| archive/docs/AGENTS-ARCHIVE.md | W1034 | 本批新增/修改 |
| docs/00-导读/W批次编号对账表.md | W1034 | 本批新增/修改 |
| docs/00-导读/项目说明.md | W1034 | 本批新增/修改 |
| scripts/output/_w1034_spec.json | W1034 | 本批新增/修改 |
| scripts/output/file-index.md | W1034 | 本批新增/修改 |
| site/index.html | W1034 | 本批新增/修改 |

## W1033 T05 计划状态校正（2026-10-30）

| 文件 | W | 说明 |
|---|---|---|
| .github/workflows/README.md | W1033 | 本批新增/修改 |
| AGENTS.md | W1033 | 本批新增/修改 |
| CHANGELOG.md | W1033 | 本批新增/修改 |
| CITATION.cff | W1033 | 本批新增/修改 |
| HANDOVER.md | W1033 | 本批新增/修改 |
| README.md | W1033 | 本批新增/修改 |
| STRUCTURE.md | W1033 | 本批新增/修改 |
| archive/docs/AGENTS-ARCHIVE.md | W1033 | 本批新增/修改 |
| docs/00-导读/W批次编号对账表.md | W1033 | 本批新增/修改 |
| docs/00-导读/项目说明.md | W1033 | 本批新增/修改 |
| docs/11-方案报告/计划方案/执行前计划-T05-取经编制表落库与编制位补全.md | W1033 | 本批新增/修改 |
| scripts/output/_w1033_spec.json | W1033 | 本批新增/修改 |
| scripts/output/file-index.md | W1033 | 本批新增/修改 |
| site/index.html | W1033 | 本批新增/修改 |

## W1032 编制表环境依赖纠错（2026-10-30）

| 文件 | W | 说明 |
|---|---|---|
| .github/workflows/README.md | W1032 | 本批新增/修改 |
| AGENTS.md | W1032 | 本批新增/修改 |
| CHANGELOG.md | W1032 | 本批新增/修改 |
| CITATION.cff | W1032 | 本批新增/修改 |
| HANDOVER.md | W1032 | 本批新增/修改 |
| README.md | W1032 | 本批新增/修改 |
| STRUCTURE.md | W1032 | 本批新增/修改 |
| archive/docs/AGENTS-ARCHIVE.md | W1032 | 本批新增/修改 |
| docs/00-导读/W批次编号对账表.md | W1032 | 本批新增/修改 |
| docs/00-导读/项目说明.md | W1032 | 本批新增/修改 |
| docs/11-方案报告/设计与架构方案/取经编制表-工具与技能挂位-2026-10-20.md | W1032 | 本批新增/修改 |
| docs/agent/pitfalls.md | W1032 | 本批新增/修改 |
| scripts/output/_w1032_spec.json | W1032 | 本批新增/修改 |
| scripts/output/file-index.md | W1032 | 本批新增/修改 |
| site/index.html | W1032 | 本批新增/修改 |

## W1031 取经编制表数据重核（2026-10-30）

| 文件 | W | 说明 |
|---|---|---|
| .github/workflows/README.md | W1031 | 本批新增/修改 |
| AGENTS.md | W1031 | 本批新增/修改 |
| CHANGELOG.md | W1031 | 本批新增/修改 |
| CITATION.cff | W1031 | 本批新增/修改 |
| HANDOVER.md | W1031 | 本批新增/修改 |
| README.md | W1031 | 本批新增/修改 |
| STRUCTURE.md | W1031 | 本批新增/修改 |
| archive/docs/AGENTS-ARCHIVE.md | W1031 | 本批新增/修改 |
| docs/00-导读/W批次编号对账表.md | W1031 | 本批新增/修改 |
| docs/00-导读/项目说明.md | W1031 | 本批新增/修改 |
| docs/11-方案报告/设计与架构方案/取经编制表-工具与技能挂位-2026-10-20.md | W1031 | 本批新增/修改 |
| scripts/output/_w1031_spec.json | W1031 | 本批新增/修改 |
| scripts/output/file-index.md | W1031 | 本批新增/修改 |
| site/index.html | W1031 | 本批新增/修改 |

## W1030 方案报告抽查 + 归档覆盖口径入规范（2026-10-30）

| 文件 | W | 说明 |
|---|---|---|
| .github/workflows/README.md | W1030 | 本批新增/修改 |
| AGENTS.md | W1030 | 本批新增/修改 |
| CHANGELOG.md | W1030 | 本批新增/修改 |
| CITATION.cff | W1030 | 本批新增/修改 |
| HANDOVER.md | W1030 | 本批新增/修改 |
| README.md | W1030 | 本批新增/修改 |
| STRUCTURE.md | W1030 | 本批新增/修改 |
| archive/docs/AGENTS-ARCHIVE.md | W1030 | 本批新增/修改 |
| docs/00-导读/W批次编号对账表.md | W1030 | 本批新增/修改 |
| docs/00-导读/文档规范.md | W1030 | 本批新增/修改 |
| docs/00-导读/项目说明.md | W1030 | 本批新增/修改 |
| scripts/output/_w1030_spec.json | W1030 | 本批新增/修改 |
| scripts/output/file-index.md | W1030 | 本批新增/修改 |
| site/index.html | W1030 | 本批新增/修改 |

## W1029 方案报告归档判断（2026-10-30）

| 文件 | W | 说明 |
|---|---|---|
| .github/workflows/README.md | W1029 | 本批新增/修改 |
| AGENTS.md | W1029 | 本批新增/修改 |
| CHANGELOG.md | W1029 | 本批新增/修改 |
| CITATION.cff | W1029 | 本批新增/修改 |
| HANDOVER.md | W1029 | 本批新增/修改 |
| README.md | W1029 | 本批新增/修改 |
| STRUCTURE.md | W1029 | 本批新增/修改 |
| archive/docs/AGENTS-ARCHIVE.md | W1029 | 本批新增/修改 |
| docs/00-导读/W批次编号对账表.md | W1029 | 本批新增/修改 |
| docs/00-导读/项目说明.md | W1029 | 本批新增/修改 |
| docs/11-方案报告/README.md | W1029 | 本批新增/修改 |
| scripts/output/_w1029_spec.json | W1029 | 本批新增/修改 |
| scripts/output/file-index.md | W1029 | 本批新增/修改 |
| site/index.html | W1029 | 本批新增/修改 |

## W1028 归档系统与临时文件系统诊断（2026-10-30）

| 文件 | W | 说明 |
|---|---|---|
| .github/workflows/README.md | W1028 | 本批新增/修改 |
| AGENTS.md | W1028 | 本批新增/修改 |
| CHANGELOG.md | W1028 | 本批新增/修改 |
| CITATION.cff | W1028 | 本批新增/修改 |
| HANDOVER.md | W1028 | 本批新增/修改 |
| README.md | W1028 | 本批新增/修改 |
| STRUCTURE.md | W1028 | 本批新增/修改 |
| archive/docs/AGENTS-ARCHIVE.md | W1028 | 本批新增/修改 |
| docs/00-导读/W批次编号对账表.md | W1028 | 本批新增/修改 |
| docs/00-导读/项目说明.md | W1028 | 本批新增/修改 |
| docs/agent/batch-closeout-checklist.md | W1028 | 本批新增/修改 |
| scripts/output/_w1028_spec.json | W1028 | 本批新增/修改 |
| scripts/output/file-index.md | W1028 | 本批新增/修改 |
| site/index.html | W1028 | 本批新增/修改 |

## W1027 治理文档文字审查 A 档（2026-10-30）

| 文件 | W | 说明 |
|---|---|---|
| .github/workflows/README.md | W1027 | 本批新增/修改 |
| AGENTS.md | W1027 | 本批新增/修改 |
| CHANGELOG.md | W1027 | 本批新增/修改 |
| CITATION.cff | W1027 | 本批新增/修改 |
| HANDOVER.md | W1027 | 本批新增/修改 |
| README.md | W1027 | 本批新增/修改 |
| STRUCTURE.md | W1027 | 本批新增/修改 |
| archive/docs/AGENTS-ARCHIVE.md | W1027 | 本批新增/修改 |
| docs/00-导读/W批次编号对账表.md | W1027 | 本批新增/修改 |
| docs/00-导读/项目说明.md | W1027 | 本批新增/修改 |
| scripts/output/_w1027_spec.json | W1027 | 本批新增/修改 |
| scripts/output/file-index.md | W1027 | 本批新增/修改 |
| site/index.html | W1027 | 本批新增/修改 |

## W1026 HANDOVER 已完成内容归档 + 归档机制诊断（2026-10-30）

| 文件 | W | 说明 |
|---|---|---|
| .github/workflows/README.md | W1026 | 本批新增/修改 |
| AGENTS.md | W1026 | 本批新增/修改 |
| CHANGELOG.md | W1026 | 本批新增/修改 |
| CITATION.cff | W1026 | 本批新增/修改 |
| HANDOVER.md | W1026 | 本批新增/修改 |
| README.md | W1026 | 本批新增/修改 |
| STRUCTURE.md | W1026 | 本批新增/修改 |
| archive/docs/AGENTS-ARCHIVE.md | W1026 | 本批新增/修改 |
| archive/docs/HANDOVER-ARCHIVE.md | W1026 | 本批新增/修改 |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1026 | 本批新增/修改 |
| docs/00-导读/W批次编号对账表.md | W1026 | 本批新增/修改 |
| docs/00-导读/项目说明.md | W1026 | 本批新增/修改 |
| scripts/output/_w1026_spec.json | W1026 | 本批新增/修改 |
| scripts/output/file-index.md | W1026 | 本批新增/修改 |
| site/index.html | W1026 | 本批新增/修改 |

## W1025 坑表计数升机器判据（2026-10-30）

| 文件 | W | 说明 |
|---|---|---|
| .github/workflows/README.md | W1025 | 本批新增/修改 |
| AGENTS.md | W1025 | 本批新增/修改 |
| CHANGELOG.md | W1025 | 本批新增/修改 |
| CITATION.cff | W1025 | 本批新增/修改 |
| HANDOVER.md | W1025 | 本批新增/修改 |
| README.md | W1025 | 本批新增/修改 |
| STRUCTURE.md | W1025 | 本批新增/修改 |
| archive/docs/AGENTS-ARCHIVE.md | W1025 | 本批新增/修改 |
| docs/00-导读/项目说明.md | W1025 | 本批新增/修改 |
| scripts/check_doc_sync.py | W1025 | 本批新增/修改 |
| scripts/output/_w1025_spec.json | W1025 | 本批新增/修改 |
| scripts/output/file-index.md | W1025 | 本批新增/修改 |
| site/index.html | W1025 | 本批新增/修改 |

## W1024 本次任务教训固化对账（2026-10-30）

| 文件 | W | 说明 |
|---|---|---|
| .github/workflows/README.md | W1024 | 本批新增/修改 |
| AGENTS.md | W1024 | 本批新增/修改 |
| CHANGELOG.md | W1024 | 本批新增/修改 |
| CITATION.cff | W1024 | 本批新增/修改 |
| HANDOVER.md | W1024 | 本批新增/修改 |
| README.md | W1024 | 本批新增/修改 |
| STRUCTURE.md | W1024 | 本批新增/修改 |
| archive/docs/AGENTS-ARCHIVE.md | W1024 | 本批新增/修改 |
| docs/00-导读/W批次编号对账表.md | W1024 | 本批新增/修改 |
| docs/00-导读/项目说明.md | W1024 | 本批新增/修改 |
| docs/agent/batch-closeout-checklist.md | W1024 | 本批新增/修改 |
| docs/agent/pitfalls.md | W1024 | 本批新增/修改 |
| scripts/output/_w1024_spec.json | W1024 | 本批新增/修改 |
| scripts/output/file-index.md | W1024 | 本批新增/修改 |
| site/index.html | W1024 | 本批新增/修改 |

## W1023 提示词库派发骨架补齐（2026-10-30）

| 文件 | W | 说明 |
|---|---|---|
| .github/workflows/README.md | W1023 | 本批新增/修改 |
| AGENTS.md | W1023 | 本批新增/修改 |
| CHANGELOG.md | W1023 | 本批新增/修改 |
| CITATION.cff | W1023 | 本批新增/修改 |
| HANDOVER.md | W1023 | 本批新增/修改 |
| README.md | W1023 | 本批新增/修改 |
| STRUCTURE.md | W1023 | 本批新增/修改 |
| archive/docs/AGENTS-ARCHIVE.md | W1023 | 本批新增/修改 |
| docs/00-导读/W批次编号对账表.md | W1023 | 本批新增/修改 |
| docs/00-导读/项目说明.md | W1023 | 本批新增/修改 |
| docs/12-提示词库/03-工作复盘提示词.md | W1023 | 本批新增/修改 |
| docs/12-提示词库/05-项目审查任务书.md | W1023 | 本批新增/修改 |
| docs/12-提示词库/09-导师提问流程.md | W1023 | 本批新增/修改 |
| scripts/output/_w1023_spec.json | W1023 | 本批新增/修改 |
| scripts/output/file-index.md | W1023 | 本批新增/修改 |
| site/index.html | W1023 | 本批新增/修改 |

## W1022 对抗式审查批（2026-10-30）

| 文件 | W | 说明 |
|---|---|---|
| .github/workflows/README.md | W1022 | 本批新增/修改 |
| AGENTS.md | W1022 | 本批新增/修改 |
| CHANGELOG.md | W1022 | 本批新增/修改 |
| CITATION.cff | W1022 | 本批新增/修改 |
| HANDOVER.md | W1022 | 本批新增/修改 |
| README.md | W1022 | 本批新增/修改 |
| STRUCTURE.md | W1022 | 本批新增/修改 |
| archive/docs/AGENTS-ARCHIVE.md | W1022 | 本批新增/修改 |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1022 | 本批新增/修改 |
| docs/00-导读/W批次编号对账表.md | W1022 | 本批新增/修改 |
| docs/00-导读/项目说明.md | W1022 | 本批新增/修改 |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1022 | 本批新增/修改 |
| pytest.ini | W1022 | 本批新增/修改 |
| scripts/check_audit_trigger.py | W1022 | 本批新增/修改 |
| scripts/check_backlog_review.py | W1022 | 本批新增/修改 |
| scripts/check_motion_ban.py | W1022 | 本批新增/修改 |
| scripts/check_token_coverage.py | W1022 | 本批新增/修改 |
| scripts/inline_css.py | W1022 | 本批新增/修改 |
| scripts/output/_w1022_spec.json | W1022 | 本批新增/修改 |
| scripts/output/file-index.md | W1022 | 本批新增/修改 |
| scripts/output/stats-changelog.json | W1022 | 本批新增/修改 |
| scripts/output/stats-index.md | W1022 | 本批新增/修改 |
| scripts/output/stats.json | W1022 | 本批新增/修改 |
| site/_template.html | W1022 | 本批新增/修改 |
| site/data/81-hardships-view.html | W1022 | 本批新增/修改 |
| site/data/81-hardships.html | W1022 | 本批新增/修改 |
| site/data/_shell.html | W1022 | 本批新增/修改 |
| site/data/aesthetics.html | W1022 | 本批新增/修改 |
| site/data/ai-dialogue.html | W1022 | 本批新增/修改 |
| site/data/business-model.html | W1022 | 本批新增/修改 |
| site/data/cave-estate.html | W1022 | 本批新增/修改 |
| site/data/century-dialogue.html | W1022 | 本批新增/修改 |
| site/data/chapter-stats.html | W1022 | 本批新增/修改 |
| site/data/chapter-structure-graph.html | W1022 | 本批新增/修改 |
| site/data/character-appearance.html | W1022 | 本批新增/修改 |
| site/data/character-dynamic-network.html | W1022 | 本批新增/修改 |
| site/data/character-presence-timeline.html | W1022 | 本批新增/修改 |
| site/data/character-relationship-3d-view.html | W1022 | 本批新增/修改 |
| site/data/character-relationship-3d.html | W1022 | 本批新增/修改 |
| site/data/character-semantic-network.html | W1022 | 本批新增/修改 |
| site/data/character-sentiment-arc.html | W1022 | 本批新增/修改 |
| site/data/chart-design.html | W1022 | 本批新增/修改 |
| site/data/cognitive-psychology.html | W1022 | 本批新增/修改 |
| site/data/concept-device.html | W1022 | 本批新增/修改 |
| site/data/counterfactual.html | W1022 | 本批新增/修改 |
| site/data/criticism-history.html | W1022 | 本批新增/修改 |
| site/data/cross-time-danmaku.html | W1022 | 本批新增/修改 |
| site/data/cultural-misreading.html | W1022 | 本批新增/修改 |
| site/data/customs-pass-route.html | W1022 | 本批新增/修改 |
| site/data/data-explorer.html | W1022 | 本批新增/修改 |
| site/data/deconstruction.html | W1022 | 本批新增/修改 |
| site/data/dialogue-sentiment.html | W1022 | 本批新增/修改 |
| site/data/ecology.html | W1022 | 本批新增/修改 |
| site/data/emotional-heatmap.html | W1022 | 本批新增/修改 |
| site/data/ethics-consumption.html | W1022 | 本批新增/修改 |
| site/data/famous-time-travel.html | W1022 | 本批新增/修改 |
| site/data/four-dimensional-research-network.html | W1022 | 本批新增/修改 |
| site/data/four-heavenly-kings-artifacts.html | W1022 | 本批新增/修改 |
| site/data/game-webnovel.html | W1022 | 本批新增/修改 |
| site/data/global-pattern.html | W1022 | 本批新增/修改 |
| site/data/graph-explorer.html | W1022 | 本批新增/修改 |
| site/data/guanyin-six-roles-network.html | W1022 | 本批新增/修改 |
| site/data/hardship-difficulty-heatmap.html | W1022 | 本批新增/修改 |
| site/data/hardship-heatmap.html | W1022 | 本批新增/修改 |
| site/data/heaven-power-network.html | W1022 | 本批新增/修改 |
| site/data/intertextuality-network.html | W1022 | 本批新增/修改 |
| site/data/journey-geo-3d.html | W1022 | 本批新增/修改 |
| site/data/journey-geo-semiotics.html | W1022 | 本批新增/修改 |
| site/data/journey-map-interactive.html | W1022 | 本批新增/修改 |
| site/data/journey-route.html | W1022 | 本批新增/修改 |
| site/data/journey-spacetime.html | W1022 | 本批新增/修改 |
| site/data/jurisprudence.html | W1022 | 本批新增/修改 |
| site/data/karma-reincarnation.html | W1022 | 本批新增/修改 |
| site/data/language-style-radar.html | W1022 | 本批新增/修改 |
| site/data/linguistics.html | W1022 | 本批新增/修改 |
| site/data/magic-system.html | W1022 | 本批新增/修改 |
| site/data/material-archaeology.html | W1022 | 本批新增/修改 |
| site/data/mbti-evolution.html | W1022 | 本批新增/修改 |
| site/data/methodology-matrix.html | W1022 | 本批新增/修改 |
| site/data/ming-political-thought-comparison.html | W1022 | 本批新增/修改 |
| site/data/monster-background.html | W1022 | 本批新增/修改 |
| site/data/monster-capability-radar.html | W1022 | 本批新增/修改 |
| site/data/monster-ecology-network.html | W1022 | 本批新增/修改 |
| site/data/monster-female-network.html | W1022 | 本批新增/修改 |
| site/data/monster-hierarchy-network.html | W1022 | 本批新增/修改 |
| site/data/monster-sociology.html | W1022 | 本批新增/修改 |
| site/data/monster-victims-network.html | W1022 | 本批新增/修改 |
| site/data/music-structure.html | W1022 | 本批新增/修改 |
| site/data/narrative-experiment.html | W1022 | 本批新增/修改 |
| site/data/narrative-rhythm-curve.html | W1022 | 本批新增/修改 |
| site/data/narratology-12d-network.html | W1022 | 本批新增/修改 |
| site/data/narratology-16d-network.html | W1022 | 本批新增/修改 |
| site/data/perf-canvas-rendering.html | W1022 | 本批新增/修改 |
| site/data/philosophy.html | W1022 | 本批新增/修改 |
| site/data/pilgrim-team-dynamic-network.html | W1022 | 本批新增/修改 |
| site/data/pilgrim-team-psychology-arc.html | W1022 | 本批新增/修改 |
| site/data/poetry-rhythm-analysis.html | W1022 | 本批新增/修改 |
| site/data/power-resources.html | W1022 | 本批新增/修改 |
| site/data/relationships.html | W1022 | 本批新增/修改 |
| site/data/risk-project.html | W1022 | 本批新增/修改 |
| site/data/search.html | W1022 | 本批新增/修改 |
| site/data/six-senses-narratology-network.html | W1022 | 本批新增/修改 |
| site/data/social-media.html | W1022 | 本批新增/修改 |
| site/data/story-timeline.html | W1022 | 本批新增/修改 |
| site/data/tag-cloud.html | W1022 | 本批新增/修改 |
| site/data/text-evolution.html | W1022 | 本批新增/修改 |
| site/data/text-search.html | W1022 | 本批新增/修改 |
| site/data/theological-intervention-network.html | W1022 | 本批新增/修改 |
| site/data/timeline.html | W1022 | 本批新增/修改 |
| site/data/underworld-power-network.html | W1022 | 本批新增/修改 |
| site/data/visual-art.html | W1022 | 本批新增/修改 |
| site/data/workplace.html | W1022 | 本批新增/修改 |
| site/dukou-engine.html | W1022 | 本批新增/修改 |
| site/en/81-hardships-view.html | W1022 | 本批新增/修改 |
| site/en/81-hardships.html | W1022 | 本批新增/修改 |
| site/en/academic-papers.html | W1022 | 本批新增/修改 |
| site/en/aesthetics.html | W1022 | 本批新增/修改 |
| site/en/ai-dialogue.html | W1022 | 本批新增/修改 |
| site/en/bestiary.html | W1022 | 本批新增/修改 |
| site/en/business-model.html | W1022 | 本批新增/修改 |
| site/en/cave-estate.html | W1022 | 本批新增/修改 |
| site/en/century-dialogue.html | W1022 | 本批新增/修改 |
| site/en/chapter-stats.html | W1022 | 本批新增/修改 |
| site/en/chapter-structure-graph.html | W1022 | 本批新增/修改 |
| site/en/chapters-map.html | W1022 | 本批新增/修改 |
| site/en/character-appearance.html | W1022 | 本批新增/修改 |
| site/en/character-bailongma.html | W1022 | 本批新增/修改 |
| site/en/character-bajie.html | W1022 | 本批新增/修改 |
| site/en/character-dynamic-network.html | W1022 | 本批新增/修改 |
| site/en/character-presence-timeline.html | W1022 | 本批新增/修改 |
| site/en/character-relationship-3d-view.html | W1022 | 本批新增/修改 |
| site/en/character-relationship-3d.html | W1022 | 本批新增/修改 |
| site/en/character-semantic-network.html | W1022 | 本批新增/修改 |
| site/en/character-sentiment-arc.html | W1022 | 本批新增/修改 |
| site/en/character-shaseng.html | W1022 | 本批新增/修改 |
| site/en/character-tangseng.html | W1022 | 本批新增/修改 |
| site/en/character-wukong.html | W1022 | 本批新增/修改 |
| site/en/characters.html | W1022 | 本批新增/修改 |
| site/en/chart-design.html | W1022 | 本批新增/修改 |
| site/en/cognitive-psychology.html | W1022 | 本批新增/修改 |
| site/en/concept-device.html | W1022 | 本批新增/修改 |
| site/en/counterfactual.html | W1022 | 本批新增/修改 |
| site/en/criticism-history.html | W1022 | 本批新增/修改 |
| site/en/cross-time-danmaku.html | W1022 | 本批新增/修改 |
| site/en/cultural-misreading.html | W1022 | 本批新增/修改 |
| site/en/customs-pass-route.html | W1022 | 本批新增/修改 |
| site/en/dashboard.html | W1022 | 本批新增/修改 |
| site/en/data-explorer.html | W1022 | 本批新增/修改 |
| site/en/deconstruction.html | W1022 | 本批新增/修改 |
| site/en/dialogue-sentiment.html | W1022 | 本批新增/修改 |
| site/en/dukou-engine.html | W1022 | 本批新增/修改 |
| site/en/ecology.html | W1022 | 本批新增/修改 |
| site/en/emotional-heatmap.html | W1022 | 本批新增/修改 |
| site/en/essay-ai-era.html | W1022 | 本批新增/修改 |
| site/en/essay-buddhist-chan.html | W1022 | 本批新增/修改 |
| site/en/essay-chapter-couplets.html | W1022 | 本批新增/修改 |
| site/en/essay-character-fu.html | W1022 | 本批新增/修改 |
| site/en/essay-cipai-linjiangxian.html | W1022 | 本批新增/修改 |
| site/en/essay-cipai-mantingfang.html | W1022 | 本批新增/修改 |
| site/en/essay-cipai-shuidiaogetou.html | W1022 | 本批新增/修改 |
| site/en/essay-cipai-xijiangyue.html | W1022 | 本批新增/修改 |
| site/en/essay-composition-origins.html | W1022 | 本批新增/修改 |
| site/en/essay-divine-bureaucracy.html | W1022 | 本批新增/修改 |
| site/en/essay-folk-belief.html | W1022 | 本批新增/修改 |
| site/en/essay-historical-xuanzang.html | W1022 | 本批新增/修改 |
| site/en/essay-information-cocoon.html | W1022 | 本批新增/修改 |
| site/en/essay-ming-economy.html | W1022 | 本批新增/修改 |
| site/en/essay-ming-examination.html | W1022 | 本批新增/修改 |
| site/en/essay-ming-garrison.html | W1022 | 本批新增/修改 |
| site/en/essay-ming-intellectual-history.html | W1022 | 本批新增/修改 |
| site/en/essay-ming-judiciary.html | W1022 | 本批新增/修改 |
| site/en/essay-ming-literary-thought.html | W1022 | 本批新增/修改 |
| site/en/essay-ming-maritime-ban.html | W1022 | 本批新增/修改 |
| site/en/essay-ming-metaphor.html | W1022 | 本批新增/修改 |
| site/en/essay-ming-military.html | W1022 | 本批新增/修改 |
| site/en/essay-ming-politics.html | W1022 | 本批新增/修改 |
| site/en/essay-ming-religion.html | W1022 | 本批新增/修改 |
| site/en/essay-ming-social-customs.html | W1022 | 本批新增/修改 |
| site/en/essay-modern-management.html | W1022 | 本批新增/修改 |
| site/en/essay-original-poetry.html | W1022 | 本批新增/修改 |
| site/en/essay-poetry-imagery.html | W1022 | 本批新增/修改 |
| site/en/essay-poetry-opening.html | W1022 | 本批新增/修改 |
| site/en/essay-quanzhen-daoism.html | W1022 | 本批新增/修改 |
| site/en/essay-rhythm-analysis.html | W1022 | 本批新增/修改 |
| site/en/essay-scenery-poems.html | W1022 | 本批新增/修改 |
| site/en/essay-thematic-poetry.html | W1022 | 本批新增/修改 |
| site/en/essay-three-teachings.html | W1022 | 本批新增/修改 |
| site/en/essay-version-evolution.html | W1022 | 本批新增/修改 |
| site/en/essay-zen-koan-vs-neidan.html | W1022 | 本批新增/修改 |
| site/en/ethics-consumption.html | W1022 | 本批新增/修改 |
| site/en/famous-time-travel.html | W1022 | 本批新增/修改 |
| site/en/four-dimensional-research-network.html | W1022 | 本批新增/修改 |
| site/en/four-heavenly-kings-artifacts.html | W1022 | 本批新增/修改 |
| site/en/game-webnovel.html | W1022 | 本批新增/修改 |
| site/en/global-pattern.html | W1022 | 本批新增/修改 |
| site/en/graph-explorer.html | W1022 | 本批新增/修改 |
| site/en/guanyin-six-roles-network.html | W1022 | 本批新增/修改 |
| site/en/guide.html | W1022 | 本批新增/修改 |
| site/en/hardship-difficulty-heatmap.html | W1022 | 本批新增/修改 |
| site/en/hardship-heatmap.html | W1022 | 本批新增/修改 |
| site/en/heaven-power-network.html | W1022 | 本批新增/修改 |
| site/en/index.html | W1022 | 本批新增/修改 |
| site/en/intertextuality-network.html | W1022 | 本批新增/修改 |
| site/en/journey-geo-semiotics.html | W1022 | 本批新增/修改 |
| site/en/journey-map-interactive.html | W1022 | 本批新增/修改 |
| site/en/journey-route.html | W1022 | 本批新增/修改 |
| site/en/journey-spacetime.html | W1022 | 本批新增/修改 |
| site/en/jurisprudence.html | W1022 | 本批新增/修改 |
| site/en/karma-reincarnation.html | W1022 | 本批新增/修改 |
| site/en/language-style-radar.html | W1022 | 本批新增/修改 |
| site/en/linguistics.html | W1022 | 本批新增/修改 |
| site/en/magic-system.html | W1022 | 本批新增/修改 |
| site/en/material-archaeology.html | W1022 | 本批新增/修改 |
| site/en/mbti-evolution.html | W1022 | 本批新增/修改 |
| site/en/methodology-matrix.html | W1022 | 本批新增/修改 |
| site/en/methodology.html | W1022 | 本批新增/修改 |
| site/en/ming-political-thought-comparison.html | W1022 | 本批新增/修改 |
| site/en/monster-background.html | W1022 | 本批新增/修改 |
| site/en/monster-capability-radar.html | W1022 | 本批新增/修改 |
| site/en/monster-ecology-network.html | W1022 | 本批新增/修改 |
| site/en/monster-female-network.html | W1022 | 本批新增/修改 |
| site/en/monster-hierarchy-network.html | W1022 | 本批新增/修改 |
| site/en/monster-sociology.html | W1022 | 本批新增/修改 |
| site/en/monster-victims-network.html | W1022 | 本批新增/修改 |
| site/en/music-structure.html | W1022 | 本批新增/修改 |
| site/en/narrative-experiment.html | W1022 | 本批新增/修改 |
| site/en/narrative-rhythm-curve.html | W1022 | 本批新增/修改 |
| site/en/narratology-12d-network.html | W1022 | 本批新增/修改 |
| site/en/narratology-16d-network.html | W1022 | 本批新增/修改 |
| site/en/perf-canvas-rendering.html | W1022 | 本批新增/修改 |
| site/en/philosophy.html | W1022 | 本批新增/修改 |
| site/en/pilgrim-team-dynamic-network.html | W1022 | 本批新增/修改 |
| site/en/pilgrim-team-psychology-arc.html | W1022 | 本批新增/修改 |
| site/en/poetry-rhythm-analysis.html | W1022 | 本批新增/修改 |
| site/en/power-resources.html | W1022 | 本批新增/修改 |
| site/en/relationships.html | W1022 | 本批新增/修改 |
| site/en/risk-project.html | W1022 | 本批新增/修改 |
| site/en/search.html | W1022 | 本批新增/修改 |
| site/en/site-map.html | W1022 | 本批新增/修改 |
| site/en/six-senses-narratology-network.html | W1022 | 本批新增/修改 |
| site/en/social-media.html | W1022 | 本批新增/修改 |
| site/en/tag-cloud.html | W1022 | 本批新增/修改 |
| site/en/text-evolution.html | W1022 | 本批新增/修改 |
| site/en/text-search.html | W1022 | 本批新增/修改 |
| site/en/theological-intervention-network.html | W1022 | 本批新增/修改 |
| site/en/timeline.html | W1022 | 本批新增/修改 |
| site/en/tribulations.html | W1022 | 本批新增/修改 |
| site/en/underworld-power-network.html | W1022 | 本批新增/修改 |
| site/en/visual-art.html | W1022 | 本批新增/修改 |
| site/en/visualizations.html | W1022 | 本批新增/修改 |
| site/en/workplace.html | W1022 | 本批新增/修改 |
| site/index.html | W1022 | 本批新增/修改 |
| site/reader/ch001.html | W1022 | 本批新增/修改 |
| site/reader/ch002.html | W1022 | 本批新增/修改 |
| site/reader/ch003.html | W1022 | 本批新增/修改 |
| site/reader/ch004.html | W1022 | 本批新增/修改 |
| site/reader/ch005.html | W1022 | 本批新增/修改 |
| site/reader/ch006.html | W1022 | 本批新增/修改 |
| site/reader/ch007.html | W1022 | 本批新增/修改 |
| site/reader/ch008.html | W1022 | 本批新增/修改 |
| site/reader/ch009.html | W1022 | 本批新增/修改 |
| site/reader/ch010.html | W1022 | 本批新增/修改 |
| site/reader/ch011.html | W1022 | 本批新增/修改 |
| site/reader/ch012.html | W1022 | 本批新增/修改 |
| site/reader/ch013.html | W1022 | 本批新增/修改 |
| site/reader/ch014.html | W1022 | 本批新增/修改 |
| site/reader/ch015.html | W1022 | 本批新增/修改 |
| site/reader/ch016.html | W1022 | 本批新增/修改 |
| site/reader/ch017.html | W1022 | 本批新增/修改 |
| site/reader/ch018.html | W1022 | 本批新增/修改 |
| site/reader/ch019.html | W1022 | 本批新增/修改 |
| site/reader/ch020.html | W1022 | 本批新增/修改 |
| site/reader/ch021.html | W1022 | 本批新增/修改 |
| site/reader/ch022.html | W1022 | 本批新增/修改 |
| site/reader/ch023.html | W1022 | 本批新增/修改 |
| site/reader/ch024.html | W1022 | 本批新增/修改 |
| site/reader/ch025.html | W1022 | 本批新增/修改 |
| site/reader/ch026.html | W1022 | 本批新增/修改 |
| site/reader/ch027.html | W1022 | 本批新增/修改 |
| site/reader/ch028.html | W1022 | 本批新增/修改 |
| site/reader/ch029.html | W1022 | 本批新增/修改 |
| site/reader/ch030.html | W1022 | 本批新增/修改 |
| site/reader/ch031.html | W1022 | 本批新增/修改 |
| site/reader/ch032.html | W1022 | 本批新增/修改 |
| site/reader/ch033.html | W1022 | 本批新增/修改 |
| site/reader/ch034.html | W1022 | 本批新增/修改 |
| site/reader/ch035.html | W1022 | 本批新增/修改 |
| site/reader/ch036.html | W1022 | 本批新增/修改 |
| site/reader/ch037.html | W1022 | 本批新增/修改 |
| site/reader/ch038.html | W1022 | 本批新增/修改 |
| site/reader/ch039.html | W1022 | 本批新增/修改 |
| site/reader/ch040.html | W1022 | 本批新增/修改 |
| site/reader/ch041.html | W1022 | 本批新增/修改 |
| site/reader/ch042.html | W1022 | 本批新增/修改 |
| site/reader/ch043.html | W1022 | 本批新增/修改 |
| site/reader/ch044.html | W1022 | 本批新增/修改 |
| site/reader/ch045.html | W1022 | 本批新增/修改 |
| site/reader/ch046.html | W1022 | 本批新增/修改 |
| site/reader/ch047.html | W1022 | 本批新增/修改 |
| site/reader/ch048.html | W1022 | 本批新增/修改 |
| site/reader/ch049.html | W1022 | 本批新增/修改 |
| site/reader/ch050.html | W1022 | 本批新增/修改 |
| site/reader/ch051.html | W1022 | 本批新增/修改 |
| site/reader/ch052.html | W1022 | 本批新增/修改 |
| site/reader/ch053.html | W1022 | 本批新增/修改 |
| site/reader/ch054.html | W1022 | 本批新增/修改 |
| site/reader/ch055.html | W1022 | 本批新增/修改 |
| site/reader/ch056.html | W1022 | 本批新增/修改 |
| site/reader/ch057.html | W1022 | 本批新增/修改 |
| site/reader/ch058.html | W1022 | 本批新增/修改 |
| site/reader/ch059.html | W1022 | 本批新增/修改 |
| site/reader/ch060.html | W1022 | 本批新增/修改 |
| site/reader/ch061.html | W1022 | 本批新增/修改 |
| site/reader/ch062.html | W1022 | 本批新增/修改 |
| site/reader/ch063.html | W1022 | 本批新增/修改 |
| site/reader/ch064.html | W1022 | 本批新增/修改 |
| site/reader/ch065.html | W1022 | 本批新增/修改 |
| site/reader/ch066.html | W1022 | 本批新增/修改 |
| site/reader/ch067.html | W1022 | 本批新增/修改 |
| site/reader/ch068.html | W1022 | 本批新增/修改 |
| site/reader/ch069.html | W1022 | 本批新增/修改 |
| site/reader/ch070.html | W1022 | 本批新增/修改 |
| site/reader/ch071.html | W1022 | 本批新增/修改 |
| site/reader/ch072.html | W1022 | 本批新增/修改 |
| site/reader/ch073.html | W1022 | 本批新增/修改 |
| site/reader/ch074.html | W1022 | 本批新增/修改 |
| site/reader/ch075.html | W1022 | 本批新增/修改 |
| site/reader/ch076.html | W1022 | 本批新增/修改 |
| site/reader/ch077.html | W1022 | 本批新增/修改 |
| site/reader/ch078.html | W1022 | 本批新增/修改 |
| site/reader/ch079.html | W1022 | 本批新增/修改 |
| site/reader/ch080.html | W1022 | 本批新增/修改 |
| site/reader/ch081.html | W1022 | 本批新增/修改 |
| site/reader/ch082.html | W1022 | 本批新增/修改 |
| site/reader/ch083.html | W1022 | 本批新增/修改 |
| site/reader/ch084.html | W1022 | 本批新增/修改 |
| site/reader/ch085.html | W1022 | 本批新增/修改 |
| site/reader/ch086.html | W1022 | 本批新增/修改 |
| site/reader/ch087.html | W1022 | 本批新增/修改 |
| site/reader/ch088.html | W1022 | 本批新增/修改 |
| site/reader/ch089.html | W1022 | 本批新增/修改 |
| site/reader/ch090.html | W1022 | 本批新增/修改 |
| site/reader/ch091.html | W1022 | 本批新增/修改 |
| site/reader/ch092.html | W1022 | 本批新增/修改 |
| site/reader/ch093.html | W1022 | 本批新增/修改 |
| site/reader/ch094.html | W1022 | 本批新增/修改 |
| site/reader/ch095.html | W1022 | 本批新增/修改 |
| site/reader/ch096.html | W1022 | 本批新增/修改 |
| site/reader/ch097.html | W1022 | 本批新增/修改 |
| site/reader/ch098.html | W1022 | 本批新增/修改 |
| site/reader/ch099.html | W1022 | 本批新增/修改 |
| site/reader/ch100.html | W1022 | 本批新增/修改 |
| site/reader/index.html | W1022 | 本批新增/修改 |
| site/reader/themes-hub.html | W1022 | 本批新增/修改 |
| tests/unit/test_style_block_judgement.py | W1022 | 本批新增/修改 |

## W1021 Backlog 对账触发器常驻化（2026-10-30）

| 文件 | W | 说明 |
|---|---|---|
| .github/workflows/README.md | W1021 | 本批新增/修改 |
| AGENTS.md | W1021 | 本批新增/修改 |
| CHANGELOG.md | W1021 | 本批新增/修改 |
| CITATION.cff | W1021 | 本批新增/修改 |
| HANDOVER.md | W1021 | 本批新增/修改 |
| README.md | W1021 | 本批新增/修改 |
| STRUCTURE.md | W1021 | 本批新增/修改 |
| archive/docs/AGENTS-ARCHIVE.md | W1021 | 本批新增/修改 |
| docs/00-导读/W批次编号对账表.md | W1021 | 本批新增/修改 |
| docs/00-导读/项目说明.md | W1021 | 本批新增/修改 |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1021 | 本批新增/修改 |
| pytest.ini | W1021 | 本批新增/修改 |
| scripts/check_backlog_review.py | W1021 | 本批新增/修改 |
| scripts/output/_w1021_spec.json | W1021 | 本批新增/修改 |
| scripts/output/file-index.md | W1021 | 本批新增/修改 |
| scripts/output/stats-changelog.json | W1021 | 本批新增/修改 |
| scripts/output/stats-index.md | W1021 | 本批新增/修改 |
| scripts/output/stats.json | W1021 | 本批新增/修改 |
| scripts/preflight_check.py | W1021 | 本批新增/修改 |
| site/index.html | W1021 | 本批新增/修改 |
| tests/unit/test_backlog_review.py | W1021 | 本批新增/修改 |

## W1020 Backlog 登记面对账批（2026-10-30）

| 文件 | W | 说明 |
|---|---|---|
| .github/workflows/README.md | W1020 | 本批新增/修改 |
| AGENTS.md | W1020 | 本批新增/修改 |
| CHANGELOG.md | W1020 | 本批新增/修改 |
| CITATION.cff | W1020 | 本批新增/修改 |
| HANDOVER.md | W1020 | 本批新增/修改 |
| README.md | W1020 | 本批新增/修改 |
| STRUCTURE.md | W1020 | 本批新增/修改 |
| archive/docs/AGENTS-ARCHIVE.md | W1020 | 本批新增/修改 |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1020 | 本批新增/修改 |
| docs/00-导读/W批次编号对账表.md | W1020 | 本批新增/修改 |
| docs/00-导读/统计口径说明.md | W1020 | 本批新增/修改 |
| docs/00-导读/项目说明.md | W1020 | 本批新增/修改 |
| docs/agent/pitfalls.md | W1020 | 本批新增/修改 |
| scripts/README.md | W1020 | 本批新增/修改 |
| scripts/output/_w1020_spec.json | W1020 | 本批新增/修改 |
| scripts/output/file-index.md | W1020 | 本批新增/修改 |
| site/index.html | W1020 | 本批新增/修改 |

## W1019 BL-33/BL-29 收官批（2026-10-30）

| 文件 | W | 说明 |
|---|---|---|
| .github/workflows/README.md | W1019 | 本批新增/修改 |
| AGENTS.md | W1019 | 本批新增/修改 |
| CHANGELOG.md | W1019 | 本批新增/修改 |
| CITATION.cff | W1019 | 本批新增/修改 |
| DESIGN.md | W1019 | 本批新增/修改 |
| HANDOVER.md | W1019 | 本批新增/修改 |
| README.md | W1019 | 本批新增/修改 |
| STRUCTURE.md | W1019 | 本批新增/修改 |
| archive/docs/AGENTS-ARCHIVE.md | W1019 | 本批新增/修改 |
| docs/00-导读/W批次编号对账表.md | W1019 | 本批新增/修改 |
| docs/00-导读/项目说明.md | W1019 | 本批新增/修改 |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1019 | 本批新增/修改 |
| pytest.ini | W1019 | 本批新增/修改 |
| scripts/inline_css.py | W1019 | 本批新增/修改 |
| scripts/output/_vermilion_solid_cache.json | W1019 | 本批新增/修改 |
| scripts/output/file-index.md | W1019 | 本批新增/修改 |
| scripts/output/stats-changelog.json | W1019 | 本批新增/修改 |
| scripts/output/stats-index.md | W1019 | 本批新增/修改 |
| scripts/output/stats.json | W1019 | 本批新增/修改 |
| site/_template.html | W1019 | 本批新增/修改 |
| site/data/81-hardships-view.html | W1019 | 本批新增/修改 |
| site/data/81-hardships.html | W1019 | 本批新增/修改 |
| site/data/_shell.html | W1019 | 本批新增/修改 |
| site/data/aesthetics.html | W1019 | 本批新增/修改 |
| site/data/ai-dialogue.html | W1019 | 本批新增/修改 |
| site/data/business-model.html | W1019 | 本批新增/修改 |
| site/data/cave-estate.html | W1019 | 本批新增/修改 |
| site/data/century-dialogue.html | W1019 | 本批新增/修改 |
| site/data/chapter-stats.html | W1019 | 本批新增/修改 |
| site/data/chapter-structure-graph.html | W1019 | 本批新增/修改 |
| site/data/character-appearance.html | W1019 | 本批新增/修改 |
| site/data/character-dynamic-network.html | W1019 | 本批新增/修改 |
| site/data/character-presence-timeline.html | W1019 | 本批新增/修改 |
| site/data/character-relationship-3d-view.html | W1019 | 本批新增/修改 |
| site/data/character-relationship-3d.html | W1019 | 本批新增/修改 |
| site/data/character-semantic-network.html | W1019 | 本批新增/修改 |
| site/data/character-sentiment-arc.html | W1019 | 本批新增/修改 |
| site/data/chart-design.html | W1019 | 本批新增/修改 |
| site/data/cognitive-psychology.html | W1019 | 本批新增/修改 |
| site/data/concept-device.html | W1019 | 本批新增/修改 |
| site/data/counterfactual.html | W1019 | 本批新增/修改 |
| site/data/criticism-history.html | W1019 | 本批新增/修改 |
| site/data/cross-time-danmaku.html | W1019 | 本批新增/修改 |
| site/data/cultural-misreading.html | W1019 | 本批新增/修改 |
| site/data/customs-pass-route.html | W1019 | 本批新增/修改 |
| site/data/data-explorer.html | W1019 | 本批新增/修改 |
| site/data/deconstruction.html | W1019 | 本批新增/修改 |
| site/data/dialogue-sentiment.html | W1019 | 本批新增/修改 |
| site/data/ecology.html | W1019 | 本批新增/修改 |
| site/data/emotional-heatmap.html | W1019 | 本批新增/修改 |
| site/data/ethics-consumption.html | W1019 | 本批新增/修改 |
| site/data/famous-time-travel.html | W1019 | 本批新增/修改 |
| site/data/four-dimensional-research-network.html | W1019 | 本批新增/修改 |
| site/data/four-heavenly-kings-artifacts.html | W1019 | 本批新增/修改 |
| site/data/game-webnovel.html | W1019 | 本批新增/修改 |
| site/data/global-pattern.html | W1019 | 本批新增/修改 |
| site/data/graph-explorer.html | W1019 | 本批新增/修改 |
| site/data/guanyin-six-roles-network.html | W1019 | 本批新增/修改 |
| site/data/hardship-difficulty-heatmap.html | W1019 | 本批新增/修改 |
| site/data/hardship-heatmap.html | W1019 | 本批新增/修改 |
| site/data/heaven-power-network.html | W1019 | 本批新增/修改 |
| site/data/intertextuality-network.html | W1019 | 本批新增/修改 |
| site/data/journey-geo-3d.html | W1019 | 本批新增/修改 |
| site/data/journey-geo-semiotics.html | W1019 | 本批新增/修改 |
| site/data/journey-map-interactive.html | W1019 | 本批新增/修改 |
| site/data/journey-route.html | W1019 | 本批新增/修改 |
| site/data/journey-spacetime.html | W1019 | 本批新增/修改 |
| site/data/jurisprudence.html | W1019 | 本批新增/修改 |
| site/data/karma-reincarnation.html | W1019 | 本批新增/修改 |
| site/data/language-style-radar.html | W1019 | 本批新增/修改 |
| site/data/linguistics.html | W1019 | 本批新增/修改 |
| site/data/magic-system.html | W1019 | 本批新增/修改 |
| site/data/material-archaeology.html | W1019 | 本批新增/修改 |
| site/data/mbti-evolution.html | W1019 | 本批新增/修改 |
| site/data/methodology-matrix.html | W1019 | 本批新增/修改 |
| site/data/ming-political-thought-comparison.html | W1019 | 本批新增/修改 |
| site/data/monster-background.html | W1019 | 本批新增/修改 |
| site/data/monster-capability-radar.html | W1019 | 本批新增/修改 |
| site/data/monster-ecology-network.html | W1019 | 本批新增/修改 |
| site/data/monster-female-network.html | W1019 | 本批新增/修改 |
| site/data/monster-hierarchy-network.html | W1019 | 本批新增/修改 |
| site/data/monster-sociology.html | W1019 | 本批新增/修改 |
| site/data/monster-victims-network.html | W1019 | 本批新增/修改 |
| site/data/music-structure.html | W1019 | 本批新增/修改 |
| site/data/narrative-experiment.html | W1019 | 本批新增/修改 |
| site/data/narrative-rhythm-curve.html | W1019 | 本批新增/修改 |
| site/data/narratology-12d-network.html | W1019 | 本批新增/修改 |
| site/data/narratology-16d-network.html | W1019 | 本批新增/修改 |
| site/data/perf-canvas-rendering.html | W1019 | 本批新增/修改 |
| site/data/philosophy.html | W1019 | 本批新增/修改 |
| site/data/pilgrim-team-dynamic-network.html | W1019 | 本批新增/修改 |
| site/data/pilgrim-team-psychology-arc.html | W1019 | 本批新增/修改 |
| site/data/poetry-rhythm-analysis.html | W1019 | 本批新增/修改 |
| site/data/power-resources.html | W1019 | 本批新增/修改 |
| site/data/relationships.html | W1019 | 本批新增/修改 |
| site/data/risk-project.html | W1019 | 本批新增/修改 |
| site/data/search.html | W1019 | 本批新增/修改 |
| site/data/six-senses-narratology-network.html | W1019 | 本批新增/修改 |
| site/data/social-media.html | W1019 | 本批新增/修改 |
| site/data/story-timeline.html | W1019 | 本批新增/修改 |
| site/data/tag-cloud.html | W1019 | 本批新增/修改 |
| site/data/text-evolution.html | W1019 | 本批新增/修改 |
| site/data/text-search.html | W1019 | 本批新增/修改 |
| site/data/theological-intervention-network.html | W1019 | 本批新增/修改 |
| site/data/timeline.html | W1019 | 本批新增/修改 |
| site/data/underworld-power-network.html | W1019 | 本批新增/修改 |
| site/data/visual-art.html | W1019 | 本批新增/修改 |
| site/data/workplace.html | W1019 | 本批新增/修改 |
| site/dukou-engine.html | W1019 | 本批新增/修改 |
| site/en/81-hardships-view.html | W1019 | 本批新增/修改 |
| site/en/81-hardships.html | W1019 | 本批新增/修改 |
| site/en/academic-papers.html | W1019 | 本批新增/修改 |
| site/en/aesthetics.html | W1019 | 本批新增/修改 |
| site/en/ai-dialogue.html | W1019 | 本批新增/修改 |
| site/en/bestiary.html | W1019 | 本批新增/修改 |
| site/en/business-model.html | W1019 | 本批新增/修改 |
| site/en/cave-estate.html | W1019 | 本批新增/修改 |
| site/en/century-dialogue.html | W1019 | 本批新增/修改 |
| site/en/chapter-stats.html | W1019 | 本批新增/修改 |
| site/en/chapter-structure-graph.html | W1019 | 本批新增/修改 |
| site/en/chapters-map.html | W1019 | 本批新增/修改 |
| site/en/character-appearance.html | W1019 | 本批新增/修改 |
| site/en/character-bailongma.html | W1019 | 本批新增/修改 |
| site/en/character-bajie.html | W1019 | 本批新增/修改 |
| site/en/character-dynamic-network.html | W1019 | 本批新增/修改 |
| site/en/character-presence-timeline.html | W1019 | 本批新增/修改 |
| site/en/character-relationship-3d-view.html | W1019 | 本批新增/修改 |
| site/en/character-relationship-3d.html | W1019 | 本批新增/修改 |
| site/en/character-semantic-network.html | W1019 | 本批新增/修改 |
| site/en/character-sentiment-arc.html | W1019 | 本批新增/修改 |
| site/en/character-shaseng.html | W1019 | 本批新增/修改 |
| site/en/character-tangseng.html | W1019 | 本批新增/修改 |
| site/en/character-wukong.html | W1019 | 本批新增/修改 |
| site/en/characters.html | W1019 | 本批新增/修改 |
| site/en/chart-design.html | W1019 | 本批新增/修改 |
| site/en/cognitive-psychology.html | W1019 | 本批新增/修改 |
| site/en/concept-device.html | W1019 | 本批新增/修改 |
| site/en/counterfactual.html | W1019 | 本批新增/修改 |
| site/en/criticism-history.html | W1019 | 本批新增/修改 |
| site/en/cross-time-danmaku.html | W1019 | 本批新增/修改 |
| site/en/cultural-misreading.html | W1019 | 本批新增/修改 |
| site/en/customs-pass-route.html | W1019 | 本批新增/修改 |
| site/en/dashboard.html | W1019 | 本批新增/修改 |
| site/en/data-explorer.html | W1019 | 本批新增/修改 |
| site/en/deconstruction.html | W1019 | 本批新增/修改 |
| site/en/dialogue-sentiment.html | W1019 | 本批新增/修改 |
| site/en/dukou-engine.html | W1019 | 本批新增/修改 |
| site/en/ecology.html | W1019 | 本批新增/修改 |
| site/en/emotional-heatmap.html | W1019 | 本批新增/修改 |
| site/en/essay-ai-era.html | W1019 | 本批新增/修改 |
| site/en/essay-buddhist-chan.html | W1019 | 本批新增/修改 |
| site/en/essay-chapter-couplets.html | W1019 | 本批新增/修改 |
| site/en/essay-character-fu.html | W1019 | 本批新增/修改 |
| site/en/essay-cipai-linjiangxian.html | W1019 | 本批新增/修改 |
| site/en/essay-cipai-mantingfang.html | W1019 | 本批新增/修改 |
| site/en/essay-cipai-shuidiaogetou.html | W1019 | 本批新增/修改 |
| site/en/essay-cipai-xijiangyue.html | W1019 | 本批新增/修改 |
| site/en/essay-composition-origins.html | W1019 | 本批新增/修改 |
| site/en/essay-divine-bureaucracy.html | W1019 | 本批新增/修改 |
| site/en/essay-folk-belief.html | W1019 | 本批新增/修改 |
| site/en/essay-historical-xuanzang.html | W1019 | 本批新增/修改 |
| site/en/essay-information-cocoon.html | W1019 | 本批新增/修改 |
| site/en/essay-ming-economy.html | W1019 | 本批新增/修改 |
| site/en/essay-ming-examination.html | W1019 | 本批新增/修改 |
| site/en/essay-ming-garrison.html | W1019 | 本批新增/修改 |
| site/en/essay-ming-intellectual-history.html | W1019 | 本批新增/修改 |
| site/en/essay-ming-judiciary.html | W1019 | 本批新增/修改 |
| site/en/essay-ming-literary-thought.html | W1019 | 本批新增/修改 |
| site/en/essay-ming-maritime-ban.html | W1019 | 本批新增/修改 |
| site/en/essay-ming-metaphor.html | W1019 | 本批新增/修改 |
| site/en/essay-ming-military.html | W1019 | 本批新增/修改 |
| site/en/essay-ming-politics.html | W1019 | 本批新增/修改 |
| site/en/essay-ming-religion.html | W1019 | 本批新增/修改 |
| site/en/essay-ming-social-customs.html | W1019 | 本批新增/修改 |
| site/en/essay-modern-management.html | W1019 | 本批新增/修改 |
| site/en/essay-original-poetry.html | W1019 | 本批新增/修改 |
| site/en/essay-poetry-imagery.html | W1019 | 本批新增/修改 |
| site/en/essay-poetry-opening.html | W1019 | 本批新增/修改 |
| site/en/essay-quanzhen-daoism.html | W1019 | 本批新增/修改 |
| site/en/essay-rhythm-analysis.html | W1019 | 本批新增/修改 |
| site/en/essay-scenery-poems.html | W1019 | 本批新增/修改 |
| site/en/essay-thematic-poetry.html | W1019 | 本批新增/修改 |
| site/en/essay-three-teachings.html | W1019 | 本批新增/修改 |
| site/en/essay-version-evolution.html | W1019 | 本批新增/修改 |
| site/en/essay-zen-koan-vs-neidan.html | W1019 | 本批新增/修改 |
| site/en/ethics-consumption.html | W1019 | 本批新增/修改 |
| site/en/famous-time-travel.html | W1019 | 本批新增/修改 |
| site/en/four-dimensional-research-network.html | W1019 | 本批新增/修改 |
| site/en/four-heavenly-kings-artifacts.html | W1019 | 本批新增/修改 |
| site/en/game-webnovel.html | W1019 | 本批新增/修改 |
| site/en/global-pattern.html | W1019 | 本批新增/修改 |
| site/en/graph-explorer.html | W1019 | 本批新增/修改 |
| site/en/guanyin-six-roles-network.html | W1019 | 本批新增/修改 |
| site/en/guide.html | W1019 | 本批新增/修改 |
| site/en/hardship-difficulty-heatmap.html | W1019 | 本批新增/修改 |
| site/en/hardship-heatmap.html | W1019 | 本批新增/修改 |
| site/en/heaven-power-network.html | W1019 | 本批新增/修改 |
| site/en/index.html | W1019 | 本批新增/修改 |
| site/en/intertextuality-network.html | W1019 | 本批新增/修改 |
| site/en/journey-geo-semiotics.html | W1019 | 本批新增/修改 |
| site/en/journey-map-interactive.html | W1019 | 本批新增/修改 |
| site/en/journey-route.html | W1019 | 本批新增/修改 |
| site/en/journey-spacetime.html | W1019 | 本批新增/修改 |
| site/en/jurisprudence.html | W1019 | 本批新增/修改 |
| site/en/karma-reincarnation.html | W1019 | 本批新增/修改 |
| site/en/language-style-radar.html | W1019 | 本批新增/修改 |
| site/en/linguistics.html | W1019 | 本批新增/修改 |
| site/en/magic-system.html | W1019 | 本批新增/修改 |
| site/en/material-archaeology.html | W1019 | 本批新增/修改 |
| site/en/mbti-evolution.html | W1019 | 本批新增/修改 |
| site/en/methodology-matrix.html | W1019 | 本批新增/修改 |
| site/en/methodology.html | W1019 | 本批新增/修改 |
| site/en/ming-political-thought-comparison.html | W1019 | 本批新增/修改 |
| site/en/monster-background.html | W1019 | 本批新增/修改 |
| site/en/monster-capability-radar.html | W1019 | 本批新增/修改 |
| site/en/monster-ecology-network.html | W1019 | 本批新增/修改 |
| site/en/monster-female-network.html | W1019 | 本批新增/修改 |
| site/en/monster-hierarchy-network.html | W1019 | 本批新增/修改 |
| site/en/monster-sociology.html | W1019 | 本批新增/修改 |
| site/en/monster-victims-network.html | W1019 | 本批新增/修改 |
| site/en/music-structure.html | W1019 | 本批新增/修改 |
| site/en/narrative-experiment.html | W1019 | 本批新增/修改 |
| site/en/narrative-rhythm-curve.html | W1019 | 本批新增/修改 |
| site/en/narratology-12d-network.html | W1019 | 本批新增/修改 |
| site/en/narratology-16d-network.html | W1019 | 本批新增/修改 |
| site/en/perf-canvas-rendering.html | W1019 | 本批新增/修改 |
| site/en/philosophy.html | W1019 | 本批新增/修改 |
| site/en/pilgrim-team-dynamic-network.html | W1019 | 本批新增/修改 |
| site/en/pilgrim-team-psychology-arc.html | W1019 | 本批新增/修改 |
| site/en/poetry-rhythm-analysis.html | W1019 | 本批新增/修改 |
| site/en/power-resources.html | W1019 | 本批新增/修改 |
| site/en/relationships.html | W1019 | 本批新增/修改 |
| site/en/risk-project.html | W1019 | 本批新增/修改 |
| site/en/search.html | W1019 | 本批新增/修改 |
| site/en/site-map.html | W1019 | 本批新增/修改 |
| site/en/six-senses-narratology-network.html | W1019 | 本批新增/修改 |
| site/en/social-media.html | W1019 | 本批新增/修改 |
| site/en/tag-cloud.html | W1019 | 本批新增/修改 |
| site/en/text-evolution.html | W1019 | 本批新增/修改 |
| site/en/text-search.html | W1019 | 本批新增/修改 |
| site/en/theological-intervention-network.html | W1019 | 本批新增/修改 |
| site/en/timeline.html | W1019 | 本批新增/修改 |
| site/en/tribulations.html | W1019 | 本批新增/修改 |
| site/en/underworld-power-network.html | W1019 | 本批新增/修改 |
| site/en/visual-art.html | W1019 | 本批新增/修改 |
| site/en/visualizations.html | W1019 | 本批新增/修改 |
| site/en/workplace.html | W1019 | 本批新增/修改 |
| site/index.html | W1019 | 本批新增/修改 |
| site/reader/ch001.html | W1019 | 本批新增/修改 |
| site/reader/ch002.html | W1019 | 本批新增/修改 |
| site/reader/ch003.html | W1019 | 本批新增/修改 |
| site/reader/ch004.html | W1019 | 本批新增/修改 |
| site/reader/ch005.html | W1019 | 本批新增/修改 |
| site/reader/ch006.html | W1019 | 本批新增/修改 |
| site/reader/ch007.html | W1019 | 本批新增/修改 |
| site/reader/ch008.html | W1019 | 本批新增/修改 |
| site/reader/ch009.html | W1019 | 本批新增/修改 |
| site/reader/ch010.html | W1019 | 本批新增/修改 |
| site/reader/ch011.html | W1019 | 本批新增/修改 |
| site/reader/ch012.html | W1019 | 本批新增/修改 |
| site/reader/ch013.html | W1019 | 本批新增/修改 |
| site/reader/ch014.html | W1019 | 本批新增/修改 |
| site/reader/ch015.html | W1019 | 本批新增/修改 |
| site/reader/ch016.html | W1019 | 本批新增/修改 |
| site/reader/ch017.html | W1019 | 本批新增/修改 |
| site/reader/ch018.html | W1019 | 本批新增/修改 |
| site/reader/ch019.html | W1019 | 本批新增/修改 |
| site/reader/ch020.html | W1019 | 本批新增/修改 |
| site/reader/ch021.html | W1019 | 本批新增/修改 |
| site/reader/ch022.html | W1019 | 本批新增/修改 |
| site/reader/ch023.html | W1019 | 本批新增/修改 |
| site/reader/ch024.html | W1019 | 本批新增/修改 |
| site/reader/ch025.html | W1019 | 本批新增/修改 |
| site/reader/ch026.html | W1019 | 本批新增/修改 |
| site/reader/ch027.html | W1019 | 本批新增/修改 |
| site/reader/ch028.html | W1019 | 本批新增/修改 |
| site/reader/ch029.html | W1019 | 本批新增/修改 |
| site/reader/ch030.html | W1019 | 本批新增/修改 |
| site/reader/ch031.html | W1019 | 本批新增/修改 |
| site/reader/ch032.html | W1019 | 本批新增/修改 |
| site/reader/ch033.html | W1019 | 本批新增/修改 |
| site/reader/ch034.html | W1019 | 本批新增/修改 |
| site/reader/ch035.html | W1019 | 本批新增/修改 |
| site/reader/ch036.html | W1019 | 本批新增/修改 |
| site/reader/ch037.html | W1019 | 本批新增/修改 |
| site/reader/ch038.html | W1019 | 本批新增/修改 |
| site/reader/ch039.html | W1019 | 本批新增/修改 |
| site/reader/ch040.html | W1019 | 本批新增/修改 |
| site/reader/ch041.html | W1019 | 本批新增/修改 |
| site/reader/ch042.html | W1019 | 本批新增/修改 |
| site/reader/ch043.html | W1019 | 本批新增/修改 |
| site/reader/ch044.html | W1019 | 本批新增/修改 |
| site/reader/ch045.html | W1019 | 本批新增/修改 |
| site/reader/ch046.html | W1019 | 本批新增/修改 |
| site/reader/ch047.html | W1019 | 本批新增/修改 |
| site/reader/ch048.html | W1019 | 本批新增/修改 |
| site/reader/ch049.html | W1019 | 本批新增/修改 |
| site/reader/ch050.html | W1019 | 本批新增/修改 |
| site/reader/ch051.html | W1019 | 本批新增/修改 |
| site/reader/ch052.html | W1019 | 本批新增/修改 |
| site/reader/ch053.html | W1019 | 本批新增/修改 |
| site/reader/ch054.html | W1019 | 本批新增/修改 |
| site/reader/ch055.html | W1019 | 本批新增/修改 |
| site/reader/ch056.html | W1019 | 本批新增/修改 |
| site/reader/ch057.html | W1019 | 本批新增/修改 |
| site/reader/ch058.html | W1019 | 本批新增/修改 |
| site/reader/ch059.html | W1019 | 本批新增/修改 |
| site/reader/ch060.html | W1019 | 本批新增/修改 |
| site/reader/ch061.html | W1019 | 本批新增/修改 |
| site/reader/ch062.html | W1019 | 本批新增/修改 |
| site/reader/ch063.html | W1019 | 本批新增/修改 |
| site/reader/ch064.html | W1019 | 本批新增/修改 |
| site/reader/ch065.html | W1019 | 本批新增/修改 |
| site/reader/ch066.html | W1019 | 本批新增/修改 |
| site/reader/ch067.html | W1019 | 本批新增/修改 |
| site/reader/ch068.html | W1019 | 本批新增/修改 |
| site/reader/ch069.html | W1019 | 本批新增/修改 |
| site/reader/ch070.html | W1019 | 本批新增/修改 |
| site/reader/ch071.html | W1019 | 本批新增/修改 |
| site/reader/ch072.html | W1019 | 本批新增/修改 |
| site/reader/ch073.html | W1019 | 本批新增/修改 |
| site/reader/ch074.html | W1019 | 本批新增/修改 |
| site/reader/ch075.html | W1019 | 本批新增/修改 |
| site/reader/ch076.html | W1019 | 本批新增/修改 |
| site/reader/ch077.html | W1019 | 本批新增/修改 |
| site/reader/ch078.html | W1019 | 本批新增/修改 |
| site/reader/ch079.html | W1019 | 本批新增/修改 |
| site/reader/ch080.html | W1019 | 本批新增/修改 |
| site/reader/ch081.html | W1019 | 本批新增/修改 |
| site/reader/ch082.html | W1019 | 本批新增/修改 |
| site/reader/ch083.html | W1019 | 本批新增/修改 |
| site/reader/ch084.html | W1019 | 本批新增/修改 |
| site/reader/ch085.html | W1019 | 本批新增/修改 |
| site/reader/ch086.html | W1019 | 本批新增/修改 |
| site/reader/ch087.html | W1019 | 本批新增/修改 |
| site/reader/ch088.html | W1019 | 本批新增/修改 |
| site/reader/ch089.html | W1019 | 本批新增/修改 |
| site/reader/ch090.html | W1019 | 本批新增/修改 |
| site/reader/ch091.html | W1019 | 本批新增/修改 |
| site/reader/ch092.html | W1019 | 本批新增/修改 |
| site/reader/ch093.html | W1019 | 本批新增/修改 |
| site/reader/ch094.html | W1019 | 本批新增/修改 |
| site/reader/ch095.html | W1019 | 本批新增/修改 |
| site/reader/ch096.html | W1019 | 本批新增/修改 |
| site/reader/ch097.html | W1019 | 本批新增/修改 |
| site/reader/ch098.html | W1019 | 本批新增/修改 |
| site/reader/ch099.html | W1019 | 本批新增/修改 |
| site/reader/ch100.html | W1019 | 本批新增/修改 |
| site/reader/index.html | W1019 | 本批新增/修改 |
| site/reader/themes-hub.html | W1019 | 本批新增/修改 |
| site/system.css | W1019 | 本批新增/修改 |
| tests/unit/test_inline_css_resync.py | W1019 | 本批新增/修改 |
| tests/unit/test_rag_server_clamp.py | W1019 | 本批新增/修改 |

## W1018 回次 og:image 全覆盖批·第三轮（2026-10-29）

| 文件 | W | 说明 |
|---|---|---|
| .github/workflows/README.md | W1018 | 本批新增/修改 |
| AGENTS.md | W1018 | 本批新增/修改 |
| CHANGELOG.md | W1018 | 本批新增/修改 |
| CITATION.cff | W1018 | 本批新增/修改 |
| HANDOVER.md | W1018 | 本批新增/修改 |
| README.md | W1018 | 本批新增/修改 |
| STRUCTURE.md | W1018 | 本批新增/修改 |
| archive/docs/AGENTS-ARCHIVE.md | W1018 | 本批新增/修改 |
| archive/docs/CHANGELOG-ARCHIVE.md | W1018 | 本批新增/修改 |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1018 | 本批新增/修改 |
| archive/docs/file-index-ARCHIVE.md | W1018 | 本批新增/修改 |
| assets/promo/plate-set/index.md | W1018 | 本批新增/修改 |
| assets/promo/plate-set/plate-line-73-ch020-huxianfeng.png | W1018 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-73-ch020-huxianfeng.webp | W1018 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-74-ch024-qingfeng.png | W1018 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-74-ch024-qingfeng.webp | W1018 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-75-ch034-bashanhu.png | W1018 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-75-ch034-bashanhu.webp | W1018 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-76-ch043-tuolong.png | W1018 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-76-ch043-tuolong.webp | W1018 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-77-ch044-yangli.png | W1018 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-77-ch044-yangli.webp | W1018 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-78-ch049-laoyuan.png | W1018 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-78-ch049-laoyuan.webp | W1018 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-79-ch051-qingniu.png | W1018 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-79-ch051-qingniu.webp | W1018 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-80-ch064-xingxian.png | W1018 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-80-ch064-xingxian.webp | W1018 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-81-ch074-qingshi.png | W1018 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-81-ch074-qingshi.webp | W1018 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-82-ch091-bidun.png | W1018 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-82-ch091-bidun.webp | W1018 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-83-ch096-kouyuanwai.png | W1018 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-83-ch096-kouyuanwai.webp | W1018 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-84-ch008-jinding.png | W1018 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-84-ch008-jinding.webp | W1018 | 新增母版（1200×1600） |
| assets/promo/plate-set/preview-contact-sheet.png | W1018 | 拼图预览（含本批 12 张） |
| assets/promo/plate-set/preview-contact-sheet.webp | W1018 | 拼图预览（含本批 12 张） |
| assets/promo/plate-set/preview-w1018-sheet.png | W1018 | 拼图预览（含本批 12 张） |
| assets/promo/plate-set/raw/README.md | W1018 | 出图原件目录清单（索引/说明） |
| assets/promo/plate-set/raw/index.md | W1018 | 出图原件目录清单（索引/说明） |
| assets/promo/plate-set/raw/round16/README.md | W1018 | 出图原件目录清单（索引/说明） |
| assets/promo/plate-set/raw/round16/index.md | W1018 | 出图原件目录清单（索引/说明） |
| assets/promo/plate-set/raw/round16/plate-line-73-ch020-huxianfeng.jpg | W1018 | 出图原件（12 张·含 3 张重出） |
| assets/promo/plate-set/raw/round16/plate-line-74-ch024-qingfeng.jpg | W1018 | 出图原件（12 张·含 3 张重出） |
| assets/promo/plate-set/raw/round16/plate-line-75-ch034-bashanhu.jpg | W1018 | 出图原件（12 张·含 3 张重出） |
| assets/promo/plate-set/raw/round16/plate-line-76-ch043-tuolong.jpg | W1018 | 出图原件（12 张·含 3 张重出） |
| assets/promo/plate-set/raw/round16/plate-line-77-ch044-yangli.jpg | W1018 | 出图原件（12 张·含 3 张重出） |
| assets/promo/plate-set/raw/round16/plate-line-78-ch049-laoyuan.jpg | W1018 | 出图原件（12 张·含 3 张重出） |
| assets/promo/plate-set/raw/round16/plate-line-79-ch051-qingniu.jpg | W1018 | 出图原件（12 张·含 3 张重出） |
| assets/promo/plate-set/raw/round16/plate-line-80-ch064-xingxian.jpg | W1018 | 出图原件（12 张·含 3 张重出） |
| assets/promo/plate-set/raw/round16/plate-line-81-ch074-qingshi.jpg | W1018 | 出图原件（12 张·含 3 张重出） |
| assets/promo/plate-set/raw/round16/plate-line-82-ch091-bidun.png | W1018 | 出图原件（12 张·含 3 张重出） |
| assets/promo/plate-set/raw/round16/plate-line-83-ch096-kouyuanwai.jpg | W1018 | 出图原件（12 张·含 3 张重出） |
| assets/promo/plate-set/raw/round16/plate-line-84-ch008-jinding.jpg | W1018 | 出图原件（12 张·含 3 张重出） |
| docs/00-导读/W批次编号对账表.md | W1018 | 登记面（报告/坑表/计数链/台账） |
| docs/00-导读/项目说明.md | W1018 | 登记面（报告/坑表/计数链/台账） |
| docs/11-方案报告/README.md | W1018 | 登记面（报告/坑表/计数链/台账） |
| docs/11-方案报告/计划方案/T38-任务计划执行与经验沉淀报告-2026-10-29.md | W1018 | 登记面（报告/坑表/计数链/台账） |
| docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md | W1018 | 登记面（报告/坑表/计数链/台账） |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1018 | 登记面（报告/坑表/计数链/台账） |
| docs/INDEX.md | W1018 | 登记面（报告/坑表/计数链/台账） |
| docs/agent/pitfalls.md | W1018 | 登记面（报告/坑表/计数链/台账） |
| scripts/_w1018_closeout_faces.py | W1018 | 本批工具/产物 |
| scripts/_w1018_derive_prepare.py | W1018 | 本批工具/产物 |
| scripts/_w1018_derive_stage.py | W1018 | 本批工具/产物 |
| scripts/_w1018_derive_verify.py | W1018 | 本批工具/产物 |
| scripts/_w1018_download.py | W1018 | 本批工具/产物 |
| scripts/_w1018_fix_index_order.py | W1018 | 本批工具/产物 |
| scripts/_w1018_fix_names_order.py | W1018 | 本批工具/产物 |
| scripts/_w1018_fix_refs.py | W1018 | 本批工具/产物 |
| scripts/_w1018_fix_round16.py | W1018 | 本批工具/产物 |
| scripts/_w1018_make_spec.py | W1018 | 本批工具/产物 |
| scripts/_w1018_master.py | W1018 | 本批工具/产物 |
| scripts/_w1018_pick2.py | W1018 | 本批工具/产物 |
| scripts/_w1018_prepare.py | W1018 | 本批工具/产物 |
| scripts/_w1018_probe_covered.py | W1018 | 本批工具/产物 |
| scripts/_w1018_retry.py | W1018 | 本批工具/产物 |
| scripts/_w1018_sheet.py | W1018 | 本批工具/产物 |
| scripts/_w1018_stage.py | W1018 | 本批工具/产物 |
| scripts/_w1018_verify.py | W1018 | 本批工具/产物 |
| scripts/index.md | W1018 | 本批工具/产物 |
| scripts/output/README.md | W1018 | 本批工具/产物 |
| scripts/output/_cascade_files_W1018.txt | W1018 | 本批工具/产物 |
| scripts/output/_vermilion_solid_cache.json | W1018 | 本批工具/产物 |
| scripts/output/_w1016_batch.json | W1018 | 本批工具/产物 |
| scripts/output/_w1016_batch_a.json | W1018 | 本批工具/产物 |
| scripts/output/_w1016_batch_b.json | W1018 | 本批工具/产物 |
| scripts/output/_w1016_manifest.json | W1018 | 本批工具/产物 |
| scripts/output/_w1016_retry.json | W1018 | 本批工具/产物 |
| scripts/output/_w1018_spec.json | W1018 | 本批工具/产物 |
| scripts/output/file-index.md | W1018 | 本批工具/产物 |
| scripts/output/index.md | W1018 | 本批工具/产物 |
| scripts/output/stats-changelog.json | W1018 | 本批工具/产物 |
| scripts/output/stats-index.md | W1018 | 本批工具/产物 |
| scripts/output/stats.json | W1018 | 本批工具/产物 |
| scripts/output/tools-inventory.md | W1018 | 本批工具/产物 |
| site/data/cross-time-danmaku.html | W1018 | 本批新增/修改 |
| site/data/search.html | W1018 | 本批新增/修改 |
| site/data/tag-cloud.html | W1018 | 本批新增/修改 |
| site/dukou-engine.html | W1018 | 本批新增/修改 |
| site/en/search.html | W1018 | 本批新增/修改 |
| site/index.html | W1018 | 本批新增/修改 |
| site/reader/ch008.html | W1018 | 回目页接入题图 + 换专属 1200×630 og:image |
| site/reader/ch020.html | W1018 | 回目页接入题图 + 换专属 1200×630 og:image |
| site/reader/ch024.html | W1018 | 回目页接入题图 + 换专属 1200×630 og:image |
| site/reader/ch034.html | W1018 | 回目页接入题图 + 换专属 1200×630 og:image |
| site/reader/ch043.html | W1018 | 回目页接入题图 + 换专属 1200×630 og:image |
| site/reader/ch044.html | W1018 | 回目页接入题图 + 换专属 1200×630 og:image |
| site/reader/ch049.html | W1018 | 回目页接入题图 + 换专属 1200×630 og:image |
| site/reader/ch051.html | W1018 | 回目页接入题图 + 换专属 1200×630 og:image |
| site/reader/ch064.html | W1018 | 回目页接入题图 + 换专属 1200×630 og:image |
| site/reader/ch074.html | W1018 | 回目页接入题图 + 换专属 1200×630 og:image |
| site/reader/ch091.html | W1018 | 回目页接入题图 + 换专属 1200×630 og:image |
| site/reader/ch096.html | W1018 | 回目页接入题图 + 换专属 1200×630 og:image |
| site/static/images/README.md | W1018 | 本批新增/修改 |
| site/static/images/index.md | W1018 | 本批新增/修改 |
| site/static/images/og-plate-line-73-ch020-huxianfeng.webp | W1018 | 专属 og:image（1200×630·由母版裁切） |
| site/static/images/og-plate-line-74-ch024-qingfeng.webp | W1018 | 专属 og:image（1200×630·由母版裁切） |
| site/static/images/og-plate-line-75-ch034-bashanhu.webp | W1018 | 专属 og:image（1200×630·由母版裁切） |
| site/static/images/og-plate-line-76-ch043-tuolong.webp | W1018 | 专属 og:image（1200×630·由母版裁切） |
| site/static/images/og-plate-line-77-ch044-yangli.webp | W1018 | 专属 og:image（1200×630·由母版裁切） |
| site/static/images/og-plate-line-78-ch049-laoyuan.webp | W1018 | 专属 og:image（1200×630·由母版裁切） |
| site/static/images/og-plate-line-79-ch051-qingniu.webp | W1018 | 专属 og:image（1200×630·由母版裁切） |
| site/static/images/og-plate-line-80-ch064-xingxian.webp | W1018 | 专属 og:image（1200×630·由母版裁切） |
| site/static/images/og-plate-line-81-ch074-qingshi.webp | W1018 | 专属 og:image（1200×630·由母版裁切） |
| site/static/images/og-plate-line-82-ch091-bidun.webp | W1018 | 专属 og:image（1200×630·由母版裁切） |
| site/static/images/og-plate-line-83-ch096-kouyuanwai.webp | W1018 | 专属 og:image（1200×630·由母版裁切） |
| site/static/images/og-plate-line-84-ch008-jinding.webp | W1018 | 专属 og:image（1200×630·由母版裁切） |
| site/static/images/plate-line-73-ch020-huxianfeng.webp | W1018 | 站点版（母版裁切·只裁上部留白） |
| site/static/images/plate-line-74-ch024-qingfeng.webp | W1018 | 站点版（母版裁切·只裁上部留白） |
| site/static/images/plate-line-75-ch034-bashanhu.webp | W1018 | 站点版（母版裁切·只裁上部留白） |
| site/static/images/plate-line-76-ch043-tuolong.webp | W1018 | 站点版（母版裁切·只裁上部留白） |
| site/static/images/plate-line-77-ch044-yangli.webp | W1018 | 站点版（母版裁切·只裁上部留白） |
| site/static/images/plate-line-78-ch049-laoyuan.webp | W1018 | 站点版（母版裁切·只裁上部留白） |
| site/static/images/plate-line-79-ch051-qingniu.webp | W1018 | 站点版（母版裁切·只裁上部留白） |
| site/static/images/plate-line-80-ch064-xingxian.webp | W1018 | 站点版（母版裁切·只裁上部留白） |
| site/static/images/plate-line-81-ch074-qingshi.webp | W1018 | 站点版（母版裁切·只裁上部留白） |
| site/static/images/plate-line-82-ch091-bidun.webp | W1018 | 站点版（母版裁切·只裁上部留白） |
| site/static/images/plate-line-83-ch096-kouyuanwai.webp | W1018 | 站点版（母版裁切·只裁上部留白） |
| site/static/images/plate-line-84-ch008-jinding.webp | W1018 | 站点版（母版裁切·只裁上部留白） |
| assets/promo/plate-set/preview-w1016-sheet.png | W1018 | 本批改名·旧名（已由 assets/promo/plate-set/preview-w1018-sheet.png 取代） |
| scripts/_w1016_derive_prepare.py | W1018 | 本批改名·旧名（已由 scripts/_w1018_derive_prepare.py 取代） |
| scripts/_w1016_derive_stage.py | W1018 | 本批改名·旧名（已由 scripts/_w1018_derive_stage.py 取代） |
| scripts/_w1016_download.py | W1018 | 本批改名·旧名（已由 scripts/_w1018_download.py 取代） |
| scripts/_w1016_fix_round16.py | W1018 | 本批改名·旧名（已由 scripts/_w1018_fix_round16.py 取代） |
| scripts/_w1016_master.py | W1018 | 本批改名·旧名（已由 scripts/_w1018_master.py 取代） |
| scripts/_w1016_pick2.py | W1018 | 本批改名·旧名（已由 scripts/_w1018_pick2.py 取代） |
| scripts/_w1016_prepare.py | W1018 | 本批改名·旧名（已由 scripts/_w1018_prepare.py 取代） |
| scripts/_w1016_retry.py | W1018 | 本批改名·旧名（已由 scripts/_w1018_retry.py 取代） |
| scripts/_w1016_sheet.py | W1018 | 本批改名·旧名（已由 scripts/_w1018_sheet.py 取代） |
| scripts/_w1016_stage.py | W1018 | 本批改名·旧名（已由 scripts/_w1018_stage.py 取代） |

## W1017 产物目录归位 + 临时区清理批（2026-10-29）

| 文件 | W | 说明 |
|---|---|---|
| CHANGELOG.md | W1017 | 产物目录归位 / 临时区清理 |
| STRUCTURE.md | W1017 | 产物目录归位 / 临时区清理 |
| archive/README.md | W1017 | 产物目录归位 / 临时区清理 |
| docs/00-导读/W批次编号对账表.md | W1017 | 产物目录归位 / 临时区清理 |

## W1016 教训固化批（2026-10-29）

| 文件 | W | 说明 |
|---|---|---|
| AGENTS.md | W1016 | 教训固化 |
| docs/00-导读/W批次编号对账表.md | W1016 | 教训固化 |
| docs/00-导读/新Agent启动Prompt.md | W1016 | 教训固化 |
| docs/agent/pitfalls.md | W1016 | 教训固化 |
| scripts/batch_cascade.py | W1016 | 教训固化 |
| scripts/check_doc_sync.py | W1016 | 教训固化 |
| tests/unit/test_cascade_precheck.py | W1016 | 教训固化 |
| tests/unit/test_status_z_parse.py | W1016 | 教训固化 |

## W1015 工具链稳健性补强①（2026-10-29）

| 文件 | W | 说明 |
|---|---|---|
| scripts/check_cross_line_rewrite.py | W1015 | 跨行改写扫描器（改写面高危 0 处·自带 4 例负样本自证） |
| scripts/check_plan_template.py | W1015 | 第 48 门禁读盘路径补覆盖（self_test 第 ⑧ 例） |
| scripts/ci_sim.py | W1015 | CI 侧预演接线（新增第 8 项跨行扫描） |
| tests/unit/test_cross_line_rewrite.py | W1015 | 扫描器单测 5 例 |
| tests/unit/test_plan_template_read_disk.py | W1015 | 读盘路径单测 4 例 |
| docs/00-导读/W批次编号对账表.md | W1015 | 台账认领行（精确暂存·未代提他方在途件） |

## W1014 工具链体检整改批（2026-10-29）

| 文件 | W | 说明 |
|---|---|---|
| .github/workflows/ci.yml | W1014 | 工具链体检整改 |
| .pre-commit-config.yaml | W1014 | 工具链体检整改 |
| AGENTS.md | W1014 | 工具链体检整改 |
| Makefile | W1014 | 工具链体检整改 |
| archive/README.md | W1014 | 工具链体检整改 |
| archive/scripts/batches/w10xx/_w1013_align_files.py | W1014 | 工具链体检整改 |
| archive/scripts/batches/w10xx/_w1013_derive_prepare.py | W1014 | 工具链体检整改 |
| archive/scripts/batches/w10xx/_w1013_download.py | W1014 | 工具链体检整改 |
| archive/scripts/batches/w10xx/_w1013_fix_desc.py | W1014 | 工具链体检整改 |
| archive/scripts/batches/w10xx/_w1013_inventory.py | W1014 | 工具链体检整改 |
| archive/scripts/batches/w10xx/_w1013_make_spec.py | W1014 | 工具链体检整改 |
| archive/scripts/batches/w10xx/_w1013_master.py | W1014 | 工具链体检整改 |
| archive/scripts/batches/w10xx/_w1013_prepare.py | W1014 | 工具链体检整改 |
| archive/scripts/batches/w10xx/_w1013_read.py | W1014 | 工具链体检整改 |
| archive/scripts/batches/w10xx/_w1013_retry.py | W1014 | 工具链体检整改 |
| archive/scripts/batches/w10xx/_w1013_retry2.py | W1014 | 工具链体检整改 |
| archive/scripts/batches/w10xx/_w1013_roster_check.py | W1014 | 工具链体检整改 |
| archive/scripts/batches/w10xx/_w1013_sheet.py | W1014 | 工具链体检整改 |
| archive/scripts/batches/w10xx/_w1013_shot.py | W1014 | 工具链体检整改 |
| archive/scripts/batches/w10xx/_w1013_stage.py | W1014 | 工具链体检整改 |
| archive/scripts/batches/w10xx/_w1013_verify.py | W1014 | 工具链体检整改 |
| docs/00-/345/257/274/350/257/273/W/346/211/271/346/254/241/347/274/226/345/217/267/345/257/271/350/264/246/350/241/250.md | W1014 | 工具链体检整改 |
| docs/11-/346/226/271/346/241/210/346/212/245/345/221/212//345/256/241/346/237/245/344/270/216/350/257/204/345/256/241//345/267/245/345/205/267/350/204/232/346/234/254/351/227/250/347/246/201/344/275/223/346/243/200/344/270/216/344/270/264/346/227/266/345/275/222/346/241/243/345/256/241/350/256/241-2026-10-29.md | W1014 | 工具链体检整改 |
| docs/11-/346/226/271/346/241/210/346/212/245/345/221/212/README.md | W1014 | 工具链体检整改 |
| scripts/A_/346/226/207/346/234/254/345/237/272/347/241/200//347/253/240/350/212/202/345/210/207/345/210/206.py | W1014 | 工具链体检整改 |
| scripts/batch_cascade.py | W1014 | 工具链体检整改 |
| scripts/batch_screenshots.js | W1014 | 工具链体检整改 |
| scripts/check_archive_health.py | W1014 | 工具链体检整改 |
| scripts/check_audit_trigger.py | W1014 | 工具链体检整改 |
| scripts/check_chart_values.js | W1014 | 工具链体检整改 |
| scripts/check_commit_scope.py | W1014 | 工具链体检整改 |
| scripts/check_doc_size_budget.py | W1014 | 工具链体检整改 |
| scripts/check_doc_sync.py | W1014 | 工具链体检整改 |
| scripts/check_emoji_icons.py | W1014 | 工具链体检整改 |
| scripts/check_plan_template.py | W1014 | 工具链体检整改 |
| scripts/check_script_coverage.py | W1014 | 工具链体检整改 |
| scripts/file_protocol_probe.py | W1014 | 工具链体检整改 |
| scripts/judge_gate.py | W1014 | 工具链体检整改 |
| scripts/lib/py_launch.js | W1014 | 工具链体检整改 |
| scripts/output/script-coverage-baseline.txt | W1014 | 工具链体检整改 |
| scripts/preflight_check.py | W1014 | 工具链体检整改 |
| scripts/rag/build_vectors.py | W1014 | 工具链体检整改 |
| scripts/refresh_icon_paths.py | W1014 | 工具链体检整改 |
| scripts/scan_targets.py | W1014 | 工具链体检整改 |
| scripts/security_scan.py | W1014 | 工具链体检整改 |
| scripts/site_audit.py | W1014 | 工具链体检整改 |
| scripts/subject_band.py | W1014 | 工具链体检整改 |
| scripts/tmpe_tidy.py | W1014 | 工具链体检整改 |
| scripts/verify_delivery.py | W1014 | 工具链体检整改 |
| tests/unit/test_cascade_line_anchor.py | W1014 | 工具链体检整改 |
| tests/unit/test_doc_size_budget.py | W1014 | 工具链体检整改 |
| tests/unit/test_milestone_block_regex.py | W1014 | 工具链体检整改 |
| tests/unit/test_tmpe_tidy.py | W1014 | 工具链体检整改 |
| tmpe/policy.yml | W1014 | 工具链体检整改 |

## W1013 回次 og:image 全覆盖批·第二轮（2026-10-29）

| 文件 | W | 说明 |
|---|---|---|
| AGENTS.md | W1013 | 本批新增/修改 |
| HANDOVER.md | W1013 | 本批新增/修改 |
| assets/promo/plate-set/plate-line-61-ch002-puti.png | W1013 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-61-ch002-puti.webp | W1013 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-62-ch012-jinchanzi.png | W1013 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-62-ch012-jinchanzi.webp | W1013 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-63-ch013-taibaixingxing.png | W1013 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-63-ch013-taibaixingxing.webp | W1013 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-64-ch021-lingji.png | W1013 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-64-ch021-lingji.webp | W1013 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-65-ch038-wujiguowang.png | W1013 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-65-ch038-wujiguowang.webp | W1013 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-66-ch045-huli.png | W1013 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-66-ch045-huli.webp | W1013 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-67-ch078-zhizhujing.png | W1013 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-67-ch078-zhizhujing.webp | W1013 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-68-ch082-bailujing.png | W1013 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-68-ch082-bailujing.webp | W1013 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-69-ch083-laoshujing.png | W1013 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-69-ch083-laoshujing.webp | W1013 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-70-ch086-bichandawang.png | W1013 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-70-ch086-bichandawang.webp | W1013 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-71-ch087-yuhuawang.png | W1013 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-71-ch087-yuhuawang.webp | W1013 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-72-ch092-dizang.png | W1013 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-72-ch092-dizang.webp | W1013 | 新增母版（1200×1600） |
| assets/promo/plate-set/preview-contact-sheet.png | W1013 | 拼图预览（含本批 12 张） |
| assets/promo/plate-set/preview-contact-sheet.webp | W1013 | 拼图预览（含本批 12 张） |
| assets/promo/plate-set/preview-w1013-sheet.png | W1013 | 拼图预览（含本批 12 张） |
| assets/promo/plate-set/raw/round15/plate-line-61-ch002-puti.jpg | W1013 | 出图原件（12 张·含 5 张重出） |
| assets/promo/plate-set/raw/round15/plate-line-62-ch012-jinchanzi.jpg | W1013 | 出图原件（12 张·含 5 张重出） |
| assets/promo/plate-set/raw/round15/plate-line-63-ch013-taibaixingxing.jpg | W1013 | 出图原件（12 张·含 5 张重出） |
| assets/promo/plate-set/raw/round15/plate-line-64-ch021-lingji.jpg | W1013 | 出图原件（12 张·含 5 张重出） |
| assets/promo/plate-set/raw/round15/plate-line-65-ch038-wujiguowang.jpg | W1013 | 出图原件（12 张·含 5 张重出） |
| assets/promo/plate-set/raw/round15/plate-line-66-ch045-huli.jpg | W1013 | 出图原件（12 张·含 5 张重出） |
| assets/promo/plate-set/raw/round15/plate-line-67-ch078-zhizhujing.jpg | W1013 | 出图原件（12 张·含 5 张重出） |
| assets/promo/plate-set/raw/round15/plate-line-68-ch082-bailujing.jpg | W1013 | 出图原件（12 张·含 5 张重出） |
| assets/promo/plate-set/raw/round15/plate-line-69-ch083-laoshujing.jpg | W1013 | 出图原件（12 张·含 5 张重出） |
| assets/promo/plate-set/raw/round15/plate-line-70-ch086-bichandawang.jpg | W1013 | 出图原件（12 张·含 5 张重出） |
| assets/promo/plate-set/raw/round15/plate-line-71-ch087-yuhuawang.jpg | W1013 | 出图原件（12 张·含 5 张重出） |
| assets/promo/plate-set/raw/round15/plate-line-72-ch092-dizang.jpg | W1013 | 出图原件（12 张·含 5 张重出） |
| docs/11-方案报告/README.md | W1013 | 登记面（报告/坑表/计数链/台账） |
| docs/11-方案报告/计划方案/T37-任务计划执行与经验沉淀报告-2026-10-29.md | W1013 | 登记面（报告/坑表/计数链/台账） |
| docs/11-方案报告/计划方案/执行前计划-T32-回次ogimage全覆盖第二轮.md | W1013 | 登记面（报告/坑表/计数链/台账） |
| docs/agent/pitfalls.md | W1013 | 登记面（报告/坑表/计数链/台账） |
| scripts/_w1013_derive_prepare.py | W1013 | 本批工具/产物 |
| scripts/_w1013_download.py | W1013 | 本批工具/产物 |
| scripts/_w1013_inventory.py | W1013 | 本批工具/产物 |
| scripts/_w1013_make_spec.py | W1013 | 本批工具/产物 |
| scripts/_w1013_master.py | W1013 | 本批工具/产物 |
| scripts/_w1013_prepare.py | W1013 | 本批工具/产物 |
| scripts/_w1013_read.py | W1013 | 本批工具/产物 |
| scripts/_w1013_retry.py | W1013 | 本批工具/产物 |
| scripts/_w1013_retry2.py | W1013 | 本批工具/产物 |
| scripts/_w1013_roster_check.py | W1013 | 本批工具/产物 |
| scripts/_w1013_sheet.py | W1013 | 本批工具/产物 |
| scripts/_w1013_shot.py | W1013 | 本批工具/产物 |
| scripts/_w1013_stage.py | W1013 | 本批工具/产物 |
| scripts/_w1013_verify.py | W1013 | 本批工具/产物 |
| scripts/check_js_syntax.py | W1013 | 本批工具/产物 |
| scripts/output/_w1013_batch.json | W1013 | 本批工具/产物 |
| scripts/output/_w1013_batch_a.json | W1013 | 本批工具/产物 |
| scripts/output/_w1013_batch_b.json | W1013 | 本批工具/产物 |
| scripts/output/_w1013_inventory.json | W1013 | 本批工具/产物 |
| scripts/output/_w1013_manifest.json | W1013 | 本批工具/产物 |
| scripts/output/_w1013_read.json | W1013 | 本批工具/产物 |
| scripts/output/_w1013_retry.json | W1013 | 本批工具/产物 |
| scripts/output/_w1013_retry2.json | W1013 | 本批工具/产物 |
| scripts/output/_w1013_spec.json | W1013 | 本批工具/产物 |
| site/reader/ch002.html | W1013 | 回目页接入题图 + 换专属 1200×630 og:image |
| site/reader/ch012.html | W1013 | 回目页接入题图 + 换专属 1200×630 og:image |
| site/reader/ch013.html | W1013 | 回目页接入题图 + 换专属 1200×630 og:image |
| site/reader/ch021.html | W1013 | 回目页接入题图 + 换专属 1200×630 og:image |
| site/reader/ch038.html | W1013 | 回目页接入题图 + 换专属 1200×630 og:image |
| site/reader/ch045.html | W1013 | 回目页接入题图 + 换专属 1200×630 og:image |
| site/reader/ch078.html | W1013 | 回目页接入题图 + 换专属 1200×630 og:image |
| site/reader/ch082.html | W1013 | 回目页接入题图 + 换专属 1200×630 og:image |
| site/reader/ch083.html | W1013 | 回目页接入题图 + 换专属 1200×630 og:image |
| site/reader/ch086.html | W1013 | 回目页接入题图 + 换专属 1200×630 og:image |
| site/reader/ch087.html | W1013 | 回目页接入题图 + 换专属 1200×630 og:image |
| site/reader/ch092.html | W1013 | 回目页接入题图 + 换专属 1200×630 og:image |
| site/static/images/og-plate-line-61-ch002-puti.webp | W1013 | 专属 og:image（1200×630·由母版裁切） |
| site/static/images/og-plate-line-62-ch012-jinchanzi.webp | W1013 | 专属 og:image（1200×630·由母版裁切） |
| site/static/images/og-plate-line-63-ch013-taibaixingxing.webp | W1013 | 专属 og:image（1200×630·由母版裁切） |
| site/static/images/og-plate-line-64-ch021-lingji.webp | W1013 | 专属 og:image（1200×630·由母版裁切） |
| site/static/images/og-plate-line-65-ch038-wujiguowang.webp | W1013 | 专属 og:image（1200×630·由母版裁切） |
| site/static/images/og-plate-line-66-ch045-huli.webp | W1013 | 专属 og:image（1200×630·由母版裁切） |
| site/static/images/og-plate-line-67-ch078-zhizhujing.webp | W1013 | 专属 og:image（1200×630·由母版裁切） |
| site/static/images/og-plate-line-68-ch082-bailujing.webp | W1013 | 专属 og:image（1200×630·由母版裁切） |
| site/static/images/og-plate-line-69-ch083-laoshujing.webp | W1013 | 专属 og:image（1200×630·由母版裁切） |
| site/static/images/og-plate-line-70-ch086-bichandawang.webp | W1013 | 专属 og:image（1200×630·由母版裁切） |
| site/static/images/og-plate-line-71-ch087-yuhuawang.webp | W1013 | 专属 og:image（1200×630·由母版裁切） |
| site/static/images/og-plate-line-72-ch092-dizang.webp | W1013 | 专属 og:image（1200×630·由母版裁切） |
| site/static/images/plate-line-61-ch002-puti.webp | W1013 | 站点版（母版裁切·只裁上部留白） |
| site/static/images/plate-line-62-ch012-jinchanzi.webp | W1013 | 站点版（母版裁切·只裁上部留白） |
| site/static/images/plate-line-63-ch013-taibaixingxing.webp | W1013 | 站点版（母版裁切·只裁上部留白） |
| site/static/images/plate-line-64-ch021-lingji.webp | W1013 | 站点版（母版裁切·只裁上部留白） |
| site/static/images/plate-line-65-ch038-wujiguowang.webp | W1013 | 站点版（母版裁切·只裁上部留白） |
| site/static/images/plate-line-66-ch045-huli.webp | W1013 | 站点版（母版裁切·只裁上部留白） |
| site/static/images/plate-line-67-ch078-zhizhujing.webp | W1013 | 站点版（母版裁切·只裁上部留白） |
| site/static/images/plate-line-68-ch082-bailujing.webp | W1013 | 站点版（母版裁切·只裁上部留白） |
| site/static/images/plate-line-69-ch083-laoshujing.webp | W1013 | 站点版（母版裁切·只裁上部留白） |
| site/static/images/plate-line-70-ch086-bichandawang.webp | W1013 | 站点版（母版裁切·只裁上部留白） |
| site/static/images/plate-line-71-ch087-yuhuawang.webp | W1013 | 站点版（母版裁切·只裁上部留白） |
| site/static/images/plate-line-72-ch092-dizang.webp | W1013 | 站点版（母版裁切·只裁上部留白） |

## W1012 产物目录瘦身 + 在途收口批（2026-10-29）

| 文件 | W | 说明 |
|---|---|---|
| .github/workflows/README.md | W1012 | 产物瘦身 / 在途收口 |
| AGENTS.md | W1012 | 产物瘦身 / 在途收口 |
| CHANGELOG.md | W1012 | 产物瘦身 / 在途收口 |
| CITATION.cff | W1012 | 产物瘦身 / 在途收口 |
| HANDOVER.md | W1012 | 产物瘦身 / 在途收口 |
| README.md | W1012 | 产物瘦身 / 在途收口 |
| STRUCTURE.md | W1012 | 产物瘦身 / 在途收口 |
| archive/README.md | W1012 | 产物瘦身 / 在途收口 |
| archive/docs/AGENTS-ARCHIVE.md | W1012 | 产物瘦身 / 在途收口 |
| archive/docs/CHANGELOG-ARCHIVE.md | W1012 | 产物瘦身 / 在途收口 |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1012 | 产物瘦身 / 在途收口 |
| archive/docs/file-index-ARCHIVE.md | W1012 | 产物瘦身 / 在途收口 |
| archive/scripts/batches/w8xx/README.md | W1012 | 产物瘦身 / 在途收口 |
| archive/scripts/batches/w8xx/_w851_visual_snapshot_after.json | W1012 | 产物瘦身 / 在途收口 |
| archive/scripts/batches/w8xx/_w851_visual_snapshot_before.json | W1012 | 产物瘦身 / 在途收口 |
| archive/scripts/batches/w8xx/_w876_baseline_after.json | W1012 | 产物瘦身 / 在途收口 |
| archive/scripts/batches/w8xx/_w876_baseline_before.json | W1012 | 产物瘦身 / 在途收口 |
| archive/scripts/batches/w8xx/index.md | W1012 | 产物瘦身 / 在途收口 |
| docs/00-导读/W批次编号对账表.md | W1012 | 产物瘦身 / 在途收口 |
| docs/00-导读/项目说明.md | W1012 | 产物瘦身 / 在途收口 |
| docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md | W1012 | 产物瘦身 / 在途收口 |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1012 | 产物瘦身 / 在途收口 |
| pytest.ini | W1012 | 产物瘦身 / 在途收口 |
| scripts/output/README.md | W1012 | 产物瘦身 / 在途收口 |
| scripts/output/_cascade_files_W1012.txt | W1012 | 产物瘦身 / 在途收口 |
| scripts/output/_vermilion_solid_cache.json | W1012 | 产物瘦身 / 在途收口 |
| scripts/output/_w1012_spec.json | W1012 | 产物瘦身 / 在途收口 |
| scripts/output/file-index.md | W1012 | 产物瘦身 / 在途收口 |
| scripts/output/index.md | W1012 | 产物瘦身 / 在途收口 |
| scripts/output/stats.json | W1012 | 产物瘦身 / 在途收口 |
| scripts/output/tools-inventory.md | W1012 | 产物瘦身 / 在途收口 |
| site/data/cross-time-danmaku.html | W1012 | 产物瘦身 / 在途收口 |
| site/data/tag-cloud.html | W1012 | 产物瘦身 / 在途收口 |
| site/dukou-engine.html | W1012 | 产物瘦身 / 在途收口 |
| site/index.html | W1012 | 产物瘦身 / 在途收口 |

## W1011 仓库整理分类批（2026-10-29）

|---|---|---|

| 文件 | W | 说明 |
| AGENTS.md | W1011 | 整理分类（归位/布局门禁/断链修复） |
| README.md | W1011 | 整理分类（归位/布局门禁/断链修复） |
| STRUCTURE.md | W1011 | 整理分类（归位/布局门禁/断链修复） |
| archive/scripts/batches/misc/_tmp_chap_sheet.py | W1011 | 整理分类（归位/布局门禁/断链修复） |
| docs/00-导读/W批次编号对账表.md | W1011 | 整理分类（归位/布局门禁/断链修复） |
| docs/00-导读/协议边界速查.md | W1011 | 整理分类（归位/布局门禁/断链修复） |
| docs/00-导读/文档规范.md | W1011 | 整理分类（归位/布局门禁/断链修复） |
| docs/00-导读/新Agent启动Prompt.md | W1011 | 整理分类（归位/布局门禁/断链修复） |
| docs/04-文化与历史背景/西游记大事年表.md | W1011 | 整理分类（归位/布局门禁/断链修复） |
| docs/10-方法论沉淀/例-佛法AI框架原始对话.txt | W1011 | 整理分类（归位/布局门禁/断链修复） |
| docs/INDEX.md | W1011 | 整理分类（归位/布局门禁/断链修复） |
| docs/agent/gates.md | W1011 | 整理分类（归位/布局门禁/断链修复） |
| scripts/A_文本基础/章节切分.py | W1011 | 整理分类（归位/布局门禁/断链修复） |
| scripts/check_gov_doc_claims.py | W1011 | 整理分类（归位/布局门禁/断链修复） |
| scripts/check_governance_docs.py | W1011 | 整理分类（归位/布局门禁/断链修复） |
| scripts/check_repo_layout.py | W1011 | 整理分类（归位/布局门禁/断链修复） |
| scripts/check_w_range_literal.py | W1011 | 整理分类（归位/布局门禁/断链修复） |
| scripts/output/_vermilion_solid_cache.json | W1011 | 整理分类（归位/布局门禁/断链修复） |
| scripts/output/tools-inventory.md | W1011 | 整理分类（归位/布局门禁/断链修复） |
| scripts/verify_delivery.py | W1011 | 整理分类（归位/布局门禁/断链修复） |
| site/reader/ch001.html | W1011 | 整理分类（归位/布局门禁/断链修复） |
| site/reader/ch003.html | W1011 | 整理分类（归位/布局门禁/断链修复） |
| site/reader/ch009.html | W1011 | 整理分类（归位/布局门禁/断链修复） |
| site/reader/ch011.html | W1011 | 整理分类（归位/布局门禁/断链修复） |
| site/reader/ch022.html | W1011 | 整理分类（归位/布局门禁/断链修复） |
| site/reader/ch028.html | W1011 | 整理分类（归位/布局门禁/断链修复） |
| site/reader/ch047.html | W1011 | 整理分类（归位/布局门禁/断链修复） |
| site/reader/ch063.html | W1011 | 整理分类（归位/布局门禁/断链修复） |
| site/reader/ch066.html | W1011 | 整理分类（归位/布局门禁/断链修复） |
| site/reader/ch079.html | W1011 | 整理分类（归位/布局门禁/断链修复） |
| site/reader/ch089.html | W1011 | 整理分类（归位/布局门禁/断链修复） |
| site/reader/ch093.html | W1011 | 整理分类（归位/布局门禁/断链修复） |
| tests/unit/test_repo_layout.py | W1011 | 整理分类（归位/布局门禁/断链修复） |

## W1010 级联自动回窗批（2026-10-29）

| 文件 | W | 说明 |
|---|---|---|
| AGENTS.md | W1010 | 级联自动回窗 |
| CHANGELOG.md | W1010 | 级联自动回窗 |
| CITATION.cff | W1010 | 级联自动回窗 |
| HANDOVER.md | W1010 | 级联自动回窗 |
| README.md | W1010 | 级联自动回窗 |
| STRUCTURE.md | W1010 | 级联自动回窗 |
| .github/workflows/README.md | W1010 | 级联自动回窗 |
| docs/00-导读/项目说明.md | W1010 | 级联自动回窗 |
| docs/00-导读/W批次编号对账表.md | W1010 | 级联自动回窗 |
| scripts/batch_cascade.py | W1010 | 级联自动回窗 |
| tests/unit/test_batch_spec.py | W1010 | 级联自动回窗 |
| archive/docs/AGENTS-ARCHIVE.md | W1010 | 级联自动回窗 |
| archive/docs/CHANGELOG-ARCHIVE.md | W1010 | 级联自动回窗 |
| archive/docs/FILE-INDEX-ARCHIVE.md | W1010 | 级联自动回窗 |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1010 | 级联自动回窗 |
| scripts/output/file-index.md | W1010 | 级联自动回窗 |
| scripts/output/tools-inventory.md | W1010 | 级联自动回窗 |
| scripts/output/_w1010_spec.json | W1010 | 级联自动回窗 |
| scripts/output/_cascade_files_W1010.txt | W1010 | 级联自动回窗 |
| scripts/output/_vermilion_solid_cache.json | W1010 | 级联自动回窗 |

## W1009 流程收口批（2026-10-29）

| 文件 | W | 说明 |
|---|---|---|
| AGENTS.md | W1009 | 流程收口（stats 自动 + spec 单点） |
| CHANGELOG.md | W1009 | 流程收口（stats 自动 + spec 单点） |
| CITATION.cff | W1009 | 流程收口（stats 自动 + spec 单点） |
| HANDOVER.md | W1009 | 流程收口（stats 自动 + spec 单点） |
| README.md | W1009 | 流程收口（stats 自动 + spec 单点） |
| STRUCTURE.md | W1009 | 流程收口（stats 自动 + spec 单点） |
| .github/workflows/README.md | W1009 | 流程收口（stats 自动 + spec 单点） |
| docs/00-导读/项目说明.md | W1009 | 流程收口（stats 自动 + spec 单点） |
| docs/00-导读/W批次编号对账表.md | W1009 | 流程收口（stats 自动 + spec 单点） |
| docs/agent/pitfalls.md | W1009 | 流程收口（stats 自动 + spec 单点） |
| scripts/batch_spec.py | W1009 | 流程收口（stats 自动 + spec 单点） |
| scripts/batch_cascade.py | W1009 | 流程收口（stats 自动 + spec 单点） |
| scripts/safe_commit.py | W1009 | 流程收口（stats 自动 + spec 单点） |
| scripts/check_commit_scope.py | W1009 | 流程收口（stats 自动 + spec 单点） |
| tests/unit/test_batch_spec.py | W1009 | 流程收口（stats 自动 + spec 单点） |
| archive/docs/AGENTS-ARCHIVE.md | W1009 | 流程收口（stats 自动 + spec 单点） |
| scripts/output/file-index.md | W1009 | 流程收口（stats 自动 + spec 单点） |
| scripts/output/tools-inventory.md | W1009 | 流程收口（stats 自动 + spec 单点） |
| scripts/output/_w1009_spec.json | W1009 | 流程收口（stats 自动 + spec 单点） |
| scripts/output/_cascade_files_W1009.txt | W1009 | 流程收口（stats 自动 + spec 单点） |

## W1008 回窗 + 触发器归档盲区批（2026-10-29）

| 文件 | W | 说明 |
|---|---|---|
| AGENTS.md | W1008 | 回窗 / 归档盲区修复 |
| CHANGELOG.md | W1008 | 回窗 / 归档盲区修复 |
| CITATION.cff | W1008 | 回窗 / 归档盲区修复 |
| HANDOVER.md | W1008 | 回窗 / 归档盲区修复 |
| README.md | W1008 | 回窗 / 归档盲区修复 |
| STRUCTURE.md | W1008 | 回窗 / 归档盲区修复 |
| .github/workflows/README.md | W1008 | 回窗 / 归档盲区修复 |
| docs/00-导读/项目说明.md | W1008 | 回窗 / 归档盲区修复 |
| docs/00-导读/W批次编号对账表.md | W1008 | 回窗 / 归档盲区修复 |
| docs/agent/pitfalls.md | W1008 | 回窗 / 归档盲区修复 |
| scripts/check_audit_trigger.py | W1008 | 回窗 / 归档盲区修复 |
| tests/unit/test_audit_trigger.py | W1008 | 回窗 / 归档盲区修复 |
| archive/docs/AGENTS-ARCHIVE.md | W1008 | 回窗 / 归档盲区修复 |
| archive/docs/CHANGELOG-ARCHIVE.md | W1008 | 回窗 / 归档盲区修复 |
| archive/docs/FILE-INDEX-ARCHIVE.md | W1008 | 回窗 / 归档盲区修复 |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1008 | 回窗 / 归档盲区修复 |
| scripts/output/file-index.md | W1008 | 回窗 / 归档盲区修复 |
| scripts/output/tools-inventory.md | W1008 | 回窗 / 归档盲区修复 |
| scripts/output/_w1008_spec.json | W1008 | 回窗 / 归档盲区修复 |
| scripts/output/_cascade_files_W1008.txt | W1008 | 回窗 / 归档盲区修复 |

## W1007 提交范围门禁批（2026-10-29）

| 文件 | W | 说明 |
|---|---|---|
| AGENTS.md | W1007 | 提交范围门禁（第 51 槽） |
| CHANGELOG.md | W1007 | 提交范围门禁（第 51 槽） |
| CITATION.cff | W1007 | 提交范围门禁（第 51 槽） |
| HANDOVER.md | W1007 | 提交范围门禁（第 51 槽） |
| README.md | W1007 | 提交范围门禁（第 51 槽） |
| STRUCTURE.md | W1007 | 提交范围门禁（第 51 槽） |
| .github/workflows/README.md | W1007 | 提交范围门禁（第 51 槽） |
| docs/00-导读/项目说明.md | W1007 | 提交范围门禁（第 51 槽） |
| docs/00-导读/W批次编号对账表.md | W1007 | 提交范围门禁（第 51 槽） |
| docs/00-导读/文档规范.md | W1007 | 提交范围门禁（第 51 槽） |
| docs/agent/gates.md | W1007 | 提交范围门禁（第 51 槽） |
| docs/agent/pitfalls.md | W1007 | 提交范围门禁（第 51 槽） |
| scripts/check_commit_scope.py | W1007 | 提交范围门禁（第 51 槽） |
| scripts/verify_delivery.py | W1007 | 提交范围门禁（第 51 槽） |
| tests/unit/test_commit_scope.py | W1007 | 提交范围门禁（第 51 槽） |
| archive/docs/AGENTS-ARCHIVE.md | W1007 | 提交范围门禁（第 51 槽） |
| scripts/output/file-index.md | W1007 | 提交范围门禁（第 51 槽） |
| scripts/output/tools-inventory.md | W1007 | 提交范围门禁（第 51 槽） |
| scripts/output/_w1007_spec.json | W1007 | 提交范围门禁（第 51 槽） |
| scripts/output/_cascade_files_W1007.txt | W1007 | 提交范围门禁（第 51 槽） |

## W1006 防代提硬拦批（safe_commit --expect-spec）（2026-10-29）

| 文件 | W | 说明 |
|---|---|---|
| .github/workflows/README.md | W1006 | 防代提硬拦（--expect-spec）+ 口径入仓 |
| AGENTS.md | W1006 | 防代提硬拦（--expect-spec）+ 口径入仓 |
| CHANGELOG.md | W1006 | 防代提硬拦（--expect-spec）+ 口径入仓 |
| CITATION.cff | W1006 | 防代提硬拦（--expect-spec）+ 口径入仓 |
| HANDOVER.md | W1006 | 防代提硬拦（--expect-spec）+ 口径入仓 |
| README.md | W1006 | 防代提硬拦（--expect-spec）+ 口径入仓 |
| STRUCTURE.md | W1006 | 防代提硬拦（--expect-spec）+ 口径入仓 |
| archive/docs/AGENTS-ARCHIVE.md | W1006 | 防代提硬拦（--expect-spec）+ 口径入仓 |
| archive/scripts/batches/w10xx/README.md | W1006 | 防代提硬拦（--expect-spec）+ 口径入仓 |
| archive/scripts/batches/w10xx/_w1005_fix_c6.py | W1006 | 防代提硬拦（--expect-spec）+ 口径入仓 |
| archive/scripts/batches/w10xx/_w1005_fix_head_sentence.py | W1006 | 防代提硬拦（--expect-spec）+ 口径入仓 |
| archive/scripts/batches/w10xx/_w1005_fix_tail_sep.py | W1006 | 防代提硬拦（--expect-spec）+ 口径入仓 |
| archive/scripts/batches/w10xx/_w1005_handover_line.py | W1006 | 防代提硬拦（--expect-spec）+ 口径入仓 |
| archive/scripts/batches/w10xx/_w1005_heroes.py | W1006 | 防代提硬拦（--expect-spec）+ 口径入仓 |
| archive/scripts/batches/w10xx/_w1005_patch_changelog_files.py | W1006 | 防代提硬拦（--expect-spec）+ 口径入仓 |
| archive/scripts/batches/w10xx/_w1005_probe_asset_sizes.py | W1006 | 防代提硬拦（--expect-spec）+ 口径入仓 |
| archive/scripts/batches/w10xx/_w1005_probe_cascade_line.py | W1006 | 防代提硬拦（--expect-spec）+ 口径入仓 |
| archive/scripts/batches/w10xx/_w1005_probe_changelog_files.py | W1006 | 防代提硬拦（--expect-spec）+ 口径入仓 |
| archive/scripts/batches/w10xx/_w1005_probe_faces.py | W1006 | 防代提硬拦（--expect-spec）+ 口径入仓 |
| archive/scripts/batches/w10xx/_w1005_probe_head.py | W1006 | 防代提硬拦（--expect-spec）+ 口径入仓 |
| archive/scripts/batches/w10xx/_w1005_probe_readme.py | W1006 | 防代提硬拦（--expect-spec）+ 口径入仓 |
| archive/scripts/batches/w10xx/_w1005_render_flyer.py | W1006 | 防代提硬拦（--expect-spec）+ 口径入仓 |
| archive/scripts/batches/w10xx/_w1005_serve.py | W1006 | 防代提硬拦（--expect-spec）+ 口径入仓 |
| archive/scripts/batches/w10xx/_w1005_spec.py | W1006 | 防代提硬拦（--expect-spec）+ 口径入仓 |
| archive/scripts/batches/w10xx/_w1005_sync_faces.py | W1006 | 防代提硬拦（--expect-spec）+ 口径入仓 |
| archive/scripts/batches/w10xx/index.md | W1006 | 防代提硬拦（--expect-spec）+ 口径入仓 |
| docs/00-导读/W批次编号对账表.md | W1006 | 防代提硬拦（--expect-spec）+ 口径入仓 |
| docs/00-导读/项目说明.md | W1006 | 防代提硬拦（--expect-spec）+ 口径入仓 |
| docs/agent/pitfalls.md | W1006 | 防代提硬拦（--expect-spec）+ 口径入仓 |
| scripts/check_script_coverage.py | W1006 | 防代提硬拦（--expect-spec）+ 口径入仓 |
| scripts/index.md | W1006 | 防代提硬拦（--expect-spec）+ 口径入仓 |
| scripts/output/README.md | W1006 | 防代提硬拦（--expect-spec）+ 口径入仓 |
| scripts/output/_cascade_files_W1006.txt | W1006 | 防代提硬拦（--expect-spec）+ 口径入仓 |
| scripts/output/_vermilion_solid_cache.json | W1006 | 防代提硬拦（--expect-spec）+ 口径入仓 |
| scripts/output/_w1006_spec.json | W1006 | 防代提硬拦（--expect-spec）+ 口径入仓 |
| scripts/output/file-index.md | W1006 | 防代提硬拦（--expect-spec）+ 口径入仓 |
| scripts/output/index.md | W1006 | 防代提硬拦（--expect-spec）+ 口径入仓 |
| scripts/output/stats-changelog.json | W1006 | 防代提硬拦（--expect-spec）+ 口径入仓 |
| scripts/output/stats-index.md | W1006 | 防代提硬拦（--expect-spec）+ 口径入仓 |
| scripts/output/stats.json | W1006 | 防代提硬拦（--expect-spec）+ 口径入仓 |
| scripts/output/tools-inventory.md | W1006 | 防代提硬拦（--expect-spec）+ 口径入仓 |
| scripts/safe_commit.py | W1006 | 防代提硬拦（--expect-spec）+ 口径入仓 |
| site/data/cross-time-danmaku.html | W1006 | 防代提硬拦（--expect-spec）+ 口径入仓 |
| site/data/tag-cloud.html | W1006 | 防代提硬拦（--expect-spec）+ 口径入仓 |
| site/dukou-engine.html | W1006 | 防代提硬拦（--expect-spec）+ 口径入仓 |
| site/index.html | W1006 | 防代提硬拦（--expect-spec）+ 口径入仓 |
| tests/unit/README.md | W1006 | 防代提硬拦（--expect-spec）+ 口径入仓 |
| tests/unit/index.md | W1006 | 防代提硬拦（--expect-spec）+ 口径入仓 |
| tests/unit/test_safe_commit_expect_spec.py | W1006 | 防代提硬拦（--expect-spec）+ 口径入仓 |

## W1005 hero 水墨图人数修正（2026-10-29）

| 文件 | W | 说明 |
|---|---|---|
| "archive/docs/W\346\211\271\346\254\241\347\274\226\345\217\267\345\257\271\350\264\246\350\241\250-ARCHIVE.md" | W1005 | 本批改动 |
| "docs/00-\345\257\274\350\257\273/\351\241\271\347\233\256\350\257\264\346\230\216.md" | W1005 | 本批改动 |
| "docs/11-\346\226\271\346\241\210\346\212\245\345\221\212/\350\256\276\350\256\241\344\270\216\346\236\266\346\236\204\346\226\271\346\241\210/\347\263\273\347\273\237\346\236\266\346\236\204\346\226\271\346\241\210v2-\347\233\256\346\240\207\346\200\201\344\270\216\350\220\275\345\234\260\350\267\257\347\272\277-2026-10-25.md" | W1005 | 本批改动 |
| DESIGN.md | W1005 | 本批改动 |
| archive/README.md | W1005 | 本批改动 |
| archive/docs/CHANGELOG-ARCHIVE.md | W1005 | 本批改动 |
| archive/docs/file-index-ARCHIVE.md | W1005 | 本批改动 |
| archive/scripts/batches/w9xx/README.md | W1005 | 本批改动 |
| archive/scripts/batches/w9xx/index.md | W1005 | 本批改动 |
| assets/promo/hero-set/raw/index.md | W1005 | 本批改动 |
| assets/promo/hero-set/raw/round-w1005/README.md | W1005 | 本批改动 |
| assets/promo/hero-set/raw/round-w1005/hero-01-xihai-yunhai.jpg | W1005 | 本批改动 |
| assets/promo/hero-set/raw/round-w1005/index.md | W1005 | 本批改动 |
| assets/promo/hero-set/raw/round-w1005/ink-mountains-hero.jpg | W1005 | 本批改动 |
| assets/promo/output/xiyouji-flyer-a4-en-front.png | W1005 | flyer A4 正面 PNG 重渲染（静态快照同步新图） |
| assets/promo/output/xiyouji-flyer-a4-front.png | W1005 | flyer A4 正面 PNG 重渲染（静态快照同步新图） |
| docs/agent/adversarial-audit-prompt.md | W1005 | 登记面 |
| docs/agent/gates.md | W1005 | 登记面 |
| docs/agent/pitfalls.md | W1005 | 登记面 |
| pytest.ini | W1005 | 本批改动 |
| scripts/_w1005_fix_c6.py | W1005 | 本批工具/产物 |
| scripts/_w1005_fix_head_sentence.py | W1005 | 本批工具/产物 |
| scripts/_w1005_handover_line.py | W1005 | 本批工具/产物 |
| scripts/_w1005_heroes.py | W1005 | 本批工具/产物 |
| scripts/_w1005_probe_faces.py | W1005 | 本批工具/产物 |
| scripts/_w1005_probe_head.py | W1005 | 本批工具/产物 |
| scripts/_w1005_probe_readme.py | W1005 | 本批工具/产物 |
| scripts/_w1005_render_flyer.py | W1005 | 本批工具/产物 |
| scripts/_w1005_serve.py | W1005 | 本批工具/产物 |
| scripts/_w1005_spec.py | W1005 | 本批工具/产物 |
| scripts/_w1005_sync_faces.py | W1005 | 本批工具/产物 |
| scripts/accent_audit.py | W1005 | 本批工具/产物 |
| scripts/check_audit_trigger.py | W1005 | 本批工具/产物 |
| scripts/check_crop.py | W1005 | 本批工具/产物 |
| scripts/check_emoji_icons.py | W1005 | 本批工具/产物 |
| scripts/check_page_admission.py | W1005 | 本批工具/产物 |
| scripts/check_script_coverage.py | W1005 | 本批工具/产物 |
| scripts/check_vermilion_solid.js | W1005 | 本批工具/产物 |
| scripts/file_protocol_probe.py | W1005 | 本批工具/产物 |
| scripts/icon_probe.js | W1005 | 本批工具/产物 |
| scripts/index.md | W1005 | 本批工具/产物 |
| scripts/j1_name_audit.py | W1005 | 本批工具/产物 |
| scripts/output/README.md | W1005 | 本批工具/产物 |
| scripts/output/_vermilion_solid_cache.json | W1005 | 本批工具/产物 |
| scripts/output/_w1004_spec.json | W1005 | 本批工具/产物 |
| scripts/output/_w1005_batch.json | W1005 | 本批工具/产物 |
| scripts/output/_w1005_heroes.json | W1005 | 本批工具/产物 |
| scripts/output/_w1005_map.json | W1005 | 本批工具/产物 |
| scripts/output/_w1005_spec.json | W1005 | 本批工具/产物 |
| scripts/output/tools-inventory.md | W1005 | 本批工具/产物 |
| scripts/refresh_icon_paths.py | W1005 | 本批工具/产物 |
| scripts/scan_targets.py | W1005 | 本批工具/产物 |
| scripts/site_audit.py | W1005 | 本批工具/产物 |
| scripts/subject_band.py | W1005 | 本批工具/产物 |
| scripts/visual_regression_probe.py | W1005 | 本批工具/产物 |
| site/static/images/hero-01-xihai-yunhai.webp | W1005 | 原地替换（人数修正·4 人形 + 1 匹白马） |
| site/static/images/ink-mountains-hero.webp | W1005 | 原地替换（人数修正·4 人形 + 1 匹白马） |
| tests/unit/README.md | W1005 | 本批改动 |
| tests/unit/index.md | W1005 | 本批改动 |
| tests/unit/test_audit_trigger.py | W1005 | 本批改动 |
| tests/unit/test_script_hygiene.py | W1005 | 本批改动 |
| tests/unit/test_w851_j1_name_audit.py | W1005 | 本批改动 |
| tests/unit/test_w851_visual_regression_probe.py | W1005 | 本批改动 |

## W1004 转正清零 + 审查触发器判据修正批（B1 字样≠事件 / B2 max / B4 台账归位）（2026-10-29）

| 文件 | W | 说明 |
|---|---|---|
| .github/workflows/README.md | W1004 | 本批新增/修改（09146cf1 代提入库·收口补登） |
| AGENTS.md | W1004 | 本批新增/修改（09146cf1 代提入库·收口补登） |
| CHANGELOG.md | W1004 | 本批新增/修改（09146cf1 代提入库·收口补登） |
| CITATION.cff | W1004 | 本批新增/修改（09146cf1 代提入库·收口补登） |
| DESIGN.md | W1004 | 本批新增/修改（09146cf1 代提入库·收口补登） |
| HANDOVER.md | W1004 | 本批新增/修改（09146cf1 代提入库·收口补登） |
| README.md | W1004 | 本批新增/修改（09146cf1 代提入库·收口补登） |
| STRUCTURE.md | W1004 | 本批新增/修改（09146cf1 代提入库·收口补登） |
| archive/README.md | W1004 | 本批新增/修改（09146cf1 代提入库·收口补登） |
| archive/docs/AGENTS-ARCHIVE.md | W1004 | 本批新增/修改（09146cf1 代提入库·收口补登） |
| archive/docs/CHANGELOG-ARCHIVE.md | W1004 | 本批新增/修改（09146cf1 代提入库·收口补登） |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1004 | 本批新增/修改（09146cf1 代提入库·收口补登） |
| archive/docs/file-index-ARCHIVE.md | W1004 | 本批新增/修改（09146cf1 代提入库·收口补登） |
| archive/scripts/batches/w9xx/README.md | W1004 | 本批新增/修改（09146cf1 代提入库·收口补登） |
| archive/scripts/batches/w9xx/index.md | W1004 | 本批新增/修改（09146cf1 代提入库·收口补登） |
| assets/promo/hero-set/raw/index.md | W1004 | 本批新增/修改（09146cf1 代提入库·收口补登） |
| assets/promo/hero-set/raw/round-w1005/README.md | W1004 | 本批新增/修改（09146cf1 代提入库·收口补登） |
| assets/promo/hero-set/raw/round-w1005/hero-01-xihai-yunhai.jpg | W1004 | 本批新增/修改（09146cf1 代提入库·收口补登） |
| assets/promo/hero-set/raw/round-w1005/index.md | W1004 | 本批新增/修改（09146cf1 代提入库·收口补登） |
| assets/promo/hero-set/raw/round-w1005/ink-mountains-hero.jpg | W1004 | 本批新增/修改（09146cf1 代提入库·收口补登） |
| docs/00-导读/W批次编号对账表.md | W1004 | 本批新增/修改（09146cf1 代提入库·收口补登） |
| docs/00-导读/项目说明.md | W1004 | 本批新增/修改（09146cf1 代提入库·收口补登） |
| docs/agent/adversarial-audit-prompt.md | W1004 | 本批新增/修改（09146cf1 代提入库·收口补登） |
| docs/agent/gates.md | W1004 | 本批新增/修改（09146cf1 代提入库·收口补登） |
| docs/agent/pitfalls.md | W1004 | 本批新增/修改（09146cf1 代提入库·收口补登） |
| scripts/AD_认知心理/index.md | W1004 | 本批新增/修改（09146cf1 代提入库·收口补登） |
| scripts/accent_audit.py | W1004 | 本批新增/修改（09146cf1 代提入库·收口补登） |
| scripts/check_audit_trigger.py | W1004 | 本批新增/修改（09146cf1 代提入库·收口补登） |
| scripts/check_crop.py | W1004 | 本批新增/修改（09146cf1 代提入库·收口补登） |
| scripts/check_emoji_icons.py | W1004 | 本批新增/修改（09146cf1 代提入库·收口补登） |
| scripts/check_page_admission.py | W1004 | 本批新增/修改（09146cf1 代提入库·收口补登） |
| scripts/check_script_coverage.py | W1004 | 本批新增/修改（09146cf1 代提入库·收口补登） |
| scripts/check_vermilion_solid.js | W1004 | 本批新增/修改（09146cf1 代提入库·收口补登） |
| scripts/file_protocol_probe.py | W1004 | 本批新增/修改（09146cf1 代提入库·收口补登） |
| scripts/icon_probe.js | W1004 | 本批新增/修改（09146cf1 代提入库·收口补登） |
| scripts/index.md | W1004 | 本批新增/修改（09146cf1 代提入库·收口补登） |
| scripts/j1_name_audit.py | W1004 | 本批新增/修改（09146cf1 代提入库·收口补登） |
| scripts/output/_cascade_files_W1003.txt | W1004 | 本批新增/修改（09146cf1 代提入库·收口补登） |
| scripts/output/_vermilion_solid_cache.json | W1004 | 本批新增/修改（09146cf1 代提入库·收口补登） |
| scripts/output/_w1003_spec.json | W1004 | 本批新增/修改（09146cf1 代提入库·收口补登） |
| scripts/output/_w1004_spec.json | W1004 | 本批新增/修改（09146cf1 代提入库·收口补登） |
| scripts/output/file-index.md | W1004 | 本批新增/修改（09146cf1 代提入库·收口补登） |
| scripts/output/stats-changelog.json | W1004 | 本批新增/修改（09146cf1 代提入库·收口补登） |
| scripts/output/stats-index.md | W1004 | 本批新增/修改（09146cf1 代提入库·收口补登） |
| scripts/output/stats.json | W1004 | 本批新增/修改（09146cf1 代提入库·收口补登） |
| scripts/refresh_icon_paths.py | W1004 | 本批新增/修改（09146cf1 代提入库·收口补登） |
| scripts/scan_targets.py | W1004 | 本批新增/修改（09146cf1 代提入库·收口补登） |
| scripts/site_audit.py | W1004 | 本批新增/修改（09146cf1 代提入库·收口补登） |
| scripts/subject_band.py | W1004 | 本批新增/修改（09146cf1 代提入库·收口补登） |
| scripts/visual_regression_probe.py | W1004 | 本批新增/修改（09146cf1 代提入库·收口补登） |
| tests/unit/test_audit_trigger.py | W1004 | 本批新增/修改（09146cf1 代提入库·收口补登） |
| tests/unit/test_script_hygiene.py | W1004 | 本批新增/修改（09146cf1 代提入库·收口补登） |
| tests/unit/test_w851_j1_name_audit.py | W1004 | 本批新增/修改（09146cf1 代提入库·收口补登） |
| tests/unit/test_w851_visual_regression_probe.py | W1004 | 本批新增/修改（09146cf1 代提入库·收口补登） |

## W1003 agent-web chat 集成验证与死重清退批（2026-10-29）

| 文件 | W | 说明 |
|---|---|---|
| xiyouji-agent-web/package.json | W1003 | 移除零引用死重依赖 @tdesign-react/aigc（W401 带入） |
| xiyouji-agent-web/package-lock.json | W1003 | 随 aigc 清退同步重锁 |
| xiyouji-agent-web/e2e/chat.e2e.mjs | W1003 | 前端端口 4232→4600（迁出 WinNAT 保留段 4138-4237·EACCES 假故障修根） |

## W1002 脚本三档归位批（2026-10-29）

| 文件 | W | 说明 |
|---|---|---|
| AGENTS.md | W1002 | §3 目录注释改写 + §4.3 坑位计数同步（95 条·git 节 23） |
| Makefile | W1002 | ledger 目标改 `scripts/ledger_mutation_test.py` |
| archive/README.md | W1002 | 归档结构补 w8xx/w9xx/w10xx 桶 + 归档台账追加 W1002 组行 |
| archive/scripts/batches/w10xx/README.md | W1002 | 一次性/批次脚本移入归档桶（三档归位·第 42 门禁 C4 起判） |
| archive/scripts/batches/w10xx/_w1001_clean_locks.py | W1002 | 一次性/批次脚本移入归档桶（三档归位·第 42 门禁 C4 起判） |
| archive/scripts/batches/w10xx/_w1001_final.py | W1002 | 一次性/批次脚本移入归档桶（三档归位·第 42 门禁 C4 起判） |
| archive/scripts/batches/w10xx/_w1001_finish_faces.py | W1002 | 一次性/批次脚本移入归档桶（三档归位·第 42 门禁 C4 起判） |
| archive/scripts/batches/w10xx/_w1001_fix_index.py | W1002 | 一次性/批次脚本移入归档桶（三档归位·第 42 门禁 C4 起判） |
| archive/scripts/batches/w10xx/_w1001_fix_rule_anchor.py | W1002 | 一次性/批次脚本移入归档桶（三档归位·第 42 门禁 C4 起判） |
| archive/scripts/batches/w10xx/_w1001_probe_faces.py | W1002 | 一次性/批次脚本移入归档桶（三档归位·第 42 门禁 C4 起判） |
| archive/scripts/batches/w10xx/_w1001_restore_changelog_head.py | W1002 | 一次性/批次脚本移入归档桶（三档归位·第 42 门禁 C4 起判） |
| archive/scripts/batches/w10xx/_w1001_stage.py | W1002 | 一次性/批次脚本移入归档桶（三档归位·第 42 门禁 C4 起判） |
| archive/scripts/batches/w10xx/index.md | W1002 | 一次性/批次脚本移入归档桶（三档归位·第 42 门禁 C4 起判） |
| archive/scripts/batches/w9xx/_w954_review_evidence.py | W1002 | 一次性/批次脚本移入归档桶（三档归位·第 42 门禁 C4 起判） |
| archive/scripts/batches/w9xx/_w978_review_evidence.py | W1002 | 一次性/批次脚本移入归档桶（三档归位·第 42 门禁 C4 起判） |
| archive/scripts/batches/w9xx/_w983_derive.py | W1002 | 一次性/批次脚本移入归档桶（三档归位·第 42 门禁 C4 起判） |
| archive/scripts/batches/w9xx/_w983_download.py | W1002 | 一次性/批次脚本移入归档桶（三档归位·第 42 门禁 C4 起判） |
| archive/scripts/batches/w9xx/_w983_insert_plates.py | W1002 | 一次性/批次脚本移入归档桶（三档归位·第 42 门禁 C4 起判） |
| archive/scripts/batches/w9xx/_w983_make_prompts.py | W1002 | 一次性/批次脚本移入归档桶（三档归位·第 42 门禁 C4 起判） |
| archive/scripts/batches/w9xx/_w983_make_spec.py | W1002 | 一次性/批次脚本移入归档桶（三档归位·第 42 门禁 C4 起判） |
| archive/scripts/batches/w9xx/_w983_precheck_pages.py | W1002 | 一次性/批次脚本移入归档桶（三档归位·第 42 门禁 C4 起判） |
| archive/scripts/batches/w9xx/_w983_prepare.py | W1002 | 一次性/批次脚本移入归档桶（三档归位·第 42 门禁 C4 起判） |
| archive/scripts/batches/w9xx/_w983_retry.py | W1002 | 一次性/批次脚本移入归档桶（三档归位·第 42 门禁 C4 起判） |
| archive/scripts/batches/w9xx/_w983_serve.py | W1002 | 一次性/批次脚本移入归档桶（三档归位·第 42 门禁 C4 起判） |
| archive/scripts/batches/w9xx/_w983_sheet.py | W1002 | 一次性/批次脚本移入归档桶（三档归位·第 42 门禁 C4 起判） |
| archive/scripts/batches/w9xx/_w983_zoom.py | W1002 | 一次性/批次脚本移入归档桶（三档归位·第 42 门禁 C4 起判） |
| archive/scripts/batches/w9xx/_w984_derive.py | W1002 | 一次性/批次脚本移入归档桶（三档归位·第 42 门禁 C4 起判） |
| archive/scripts/batches/w9xx/_w984_download.py | W1002 | 一次性/批次脚本移入归档桶（三档归位·第 42 门禁 C4 起判） |
| archive/scripts/batches/w9xx/_w984_insert_plates.py | W1002 | 一次性/批次脚本移入归档桶（三档归位·第 42 门禁 C4 起判） |
| archive/scripts/batches/w9xx/_w984_make_prompts.py | W1002 | 一次性/批次脚本移入归档桶（三档归位·第 42 门禁 C4 起判） |
| archive/scripts/batches/w9xx/_w984_make_spec.py | W1002 | 一次性/批次脚本移入归档桶（三档归位·第 42 门禁 C4 起判） |
| archive/scripts/batches/w9xx/_w984_precheck_pages.py | W1002 | 一次性/批次脚本移入归档桶（三档归位·第 42 门禁 C4 起判） |
| archive/scripts/batches/w9xx/_w984_prepare.py | W1002 | 一次性/批次脚本移入归档桶（三档归位·第 42 门禁 C4 起判） |
| archive/scripts/batches/w9xx/_w984_retry.py | W1002 | 一次性/批次脚本移入归档桶（三档归位·第 42 门禁 C4 起判） |
| archive/scripts/batches/w9xx/_w984_serve.py | W1002 | 一次性/批次脚本移入归档桶（三档归位·第 42 门禁 C4 起判） |
| archive/scripts/batches/w9xx/_w984_sheet.py | W1002 | 一次性/批次脚本移入归档桶（三档归位·第 42 门禁 C4 起判） |
| archive/scripts/batches/w9xx/_w984_zoom.py | W1002 | 一次性/批次脚本移入归档桶（三档归位·第 42 门禁 C4 起判） |
| archive/scripts/batches/w9xx/_w986_make_prompts.py | W1002 | 一次性/批次脚本移入归档桶（三档归位·第 42 门禁 C4 起判） |
| archive/scripts/batches/w9xx/_w986_make_spec.py | W1002 | 一次性/批次脚本移入归档桶（三档归位·第 42 门禁 C4 起判） |
| archive/scripts/batches/w9xx/_w987_family_scan.py | W1002 | 一次性/批次脚本移入归档桶（三档归位·第 42 门禁 C4 起判） |
| archive/scripts/batches/w9xx/_w987_insert_scenes.py | W1002 | 一次性/批次脚本移入归档桶（三档归位·第 42 门禁 C4 起判） |
| archive/scripts/batches/w9xx/_w987_make_spec.py | W1002 | 一次性/批次脚本移入归档桶（三档归位·第 42 门禁 C4 起判） |
| archive/scripts/batches/w9xx/_w988_card_sheet.py | W1002 | 一次性/批次脚本移入归档桶（三档归位·第 42 门禁 C4 起判） |
| archive/scripts/batches/w9xx/_w988_docs.py | W1002 | 一次性/批次脚本移入归档桶（三档归位·第 42 门禁 C4 起判） |
| archive/scripts/batches/w9xx/_w988_fix_cascade.py | W1002 | 一次性/批次脚本移入归档桶（三档归位·第 42 门禁 C4 起判） |
| archive/scripts/batches/w9xx/_w988_fix_eol.py | W1002 | 一次性/批次脚本移入归档桶（三档归位·第 42 门禁 C4 起判） |
| archive/scripts/batches/w9xx/_w988_fix_gates.py | W1002 | 一次性/批次脚本移入归档桶（三档归位·第 42 门禁 C4 起判） |
| archive/scripts/batches/w9xx/_w988_insert.py | W1002 | 一次性/批次脚本移入归档桶（三档归位·第 42 门禁 C4 起判） |
| archive/scripts/batches/w9xx/_w988_inventory.py | W1002 | 一次性/批次脚本移入归档桶（三档归位·第 42 门禁 C4 起判） |
| archive/scripts/batches/w9xx/_w988_make_assets.py | W1002 | 一次性/批次脚本移入归档桶（三档归位·第 42 门禁 C4 起判） |
| archive/scripts/batches/w9xx/_w988_make_spec.py | W1002 | 一次性/批次脚本移入归档桶（三档归位·第 42 门禁 C4 起判） |
| archive/scripts/batches/w9xx/_w988_match.py | W1002 | 一次性/批次脚本移入归档桶（三档归位·第 42 门禁 C4 起判） |
| archive/scripts/batches/w9xx/_w988_pitfalls.py | W1002 | 一次性/批次脚本移入归档桶（三档归位·第 42 门禁 C4 起判） |
| archive/scripts/batches/w9xx/_w988_plan.py | W1002 | 一次性/批次脚本移入归档桶（三档归位·第 42 门禁 C4 起判） |
| archive/scripts/batches/w9xx/_w988_precheck.py | W1002 | 一次性/批次脚本移入归档桶（三档归位·第 42 门禁 C4 起判） |
| archive/scripts/batches/w9xx/_w988_sheet.py | W1002 | 一次性/批次脚本移入归档桶（三档归位·第 42 门禁 C4 起判） |
| archive/scripts/batches/w9xx/_w988_subject.py | W1002 | 一次性/批次脚本移入归档桶（三档归位·第 42 门禁 C4 起判） |
| archive/scripts/batches/w9xx/_w988_verify.py | W1002 | 一次性/批次脚本移入归档桶（三档归位·第 42 门禁 C4 起判） |
| archive/scripts/batches/w9xx/_w990_map.py | W1002 | 一次性/批次脚本移入归档桶（三档归位·第 42 门禁 C4 起判） |
| archive/scripts/batches/w9xx/_w990_master.py | W1002 | 一次性/批次脚本移入归档桶（三档归位·第 42 门禁 C4 起判） |
| archive/scripts/batches/w9xx/_w990_og_gap.py | W1002 | 一次性/批次脚本移入归档桶（三档归位·第 42 门禁 C4 起判） |
| archive/scripts/batches/w9xx/_w990_pick.py | W1002 | 一次性/批次脚本移入归档桶（三档归位·第 42 门禁 C4 起判） |
| archive/scripts/batches/w9xx/_w990_read.py | W1002 | 一次性/批次脚本移入归档桶（三档归位·第 42 门禁 C4 起判） |
| archive/scripts/batches/w9xx/_w990_roster.py | W1002 | 一次性/批次脚本移入归档桶（三档归位·第 42 门禁 C4 起判） |
| archive/scripts/batches/w9xx/_w990_split.py | W1002 | 一次性/批次脚本移入归档桶（三档归位·第 42 门禁 C4 起判） |
| archive/scripts/batches/w9xx/_w999_closeout.py | W1002 | 一次性/批次脚本移入归档桶（三档归位·第 42 门禁 C4 起判） |
| archive/scripts/batches/w9xx/_w999_crop_recheck.py | W1002 | 一次性/批次脚本移入归档桶（三档归位·第 42 门禁 C4 起判） |
| archive/scripts/batches/w9xx/_w999_derive_prepare.py | W1002 | 一次性/批次脚本移入归档桶（三档归位·第 42 门禁 C4 起判） |
| archive/scripts/batches/w9xx/_w999_diag.py | W1002 | 一次性/批次脚本移入归档桶（三档归位·第 42 门禁 C4 起判） |
| archive/scripts/batches/w9xx/_w999_fix_t35.py | W1002 | 一次性/批次脚本移入归档桶（三档归位·第 42 门禁 C4 起判） |
| archive/scripts/batches/w9xx/_w999_fix_wnum.py | W1002 | 一次性/批次脚本移入归档桶（三档归位·第 42 门禁 C4 起判） |
| archive/scripts/batches/w9xx/_w999_insert.py | W1002 | 一次性/批次脚本移入归档桶（三档归位·第 42 门禁 C4 起判） |
| archive/scripts/batches/w9xx/_w999_ledger_fill.py | W1002 | 一次性/批次脚本移入归档桶（三档归位·第 42 门禁 C4 起判） |
| archive/scripts/batches/w9xx/_w999_make_spec.py | W1002 | 一次性/批次脚本移入归档桶（三档归位·第 42 门禁 C4 起判） |
| archive/scripts/batches/w9xx/_w999_prepare.py | W1002 | 一次性/批次脚本移入归档桶（三档归位·第 42 门禁 C4 起判） |
| archive/scripts/batches/w9xx/_w999_probe.py | W1002 | 一次性/批次脚本移入归档桶（三档归位·第 42 门禁 C4 起判） |
| archive/scripts/batches/w9xx/_w999_probe_h1.py | W1002 | 一次性/批次脚本移入归档桶（三档归位·第 42 门禁 C4 起判） |
| archive/scripts/batches/w9xx/_w999_rebuild_missing_og.py | W1002 | 一次性/批次脚本移入归档桶（三档归位·第 42 门禁 C4 起判） |
| archive/scripts/batches/w9xx/_w999_redo.py | W1002 | 一次性/批次脚本移入归档桶（三档归位·第 42 门禁 C4 起判） |
| archive/scripts/batches/w9xx/_w999_redo2.py | W1002 | 一次性/批次脚本移入归档桶（三档归位·第 42 门禁 C4 起判） |
| archive/scripts/batches/w9xx/_w999_redo_map.py | W1002 | 一次性/批次脚本移入归档桶（三档归位·第 42 门禁 C4 起判） |
| archive/scripts/batches/w9xx/_w999_register.py | W1002 | 一次性/批次脚本移入归档桶（三档归位·第 42 门禁 C4 起判） |
| archive/scripts/batches/w9xx/_w999_renumber.py | W1002 | 一次性/批次脚本移入归档桶（三档归位·第 42 门禁 C4 起判） |
| archive/scripts/batches/w9xx/_w999_sheet.py | W1002 | 一次性/批次脚本移入归档桶（三档归位·第 42 门禁 C4 起判） |
| archive/scripts/batches/w9xx/_w999_sync_counts.py | W1002 | 一次性/批次脚本移入归档桶（三档归位·第 42 门禁 C4 起判） |
| archive/scripts/batches/w9xx/_w999_verify.py | W1002 | 一次性/批次脚本移入归档桶（三档归位·第 42 门禁 C4 起判） |
| assets/promo/plate-set/README.md | W1002 | 验算脚本改转正名 + 逐批 prep 路径死链修正 |
| docs/00-导读/文档规范.md | W1002 | §5 归档新增「脚本三档归位（W1002 定式）」条款 |
| docs/11-方案报告/README.md | W1002 | 判据表路径改转正名 `plan_template_review.py` |
| docs/11-方案报告/工作复盘与优化分析报告/工作复盘与优化分析报告-2026-10-26.md | W1002 | 取证脚本链接改归档路径（lint_links 活链校正） |
| docs/agent/pitfalls.md | W1002 | 坑表：「`_` 前缀=一次性」口径改写为「脚本三档归位」（94→95 条）+ E-05/E-19 转正名 |
| scripts/check_crop.py | W1002 | 转正：去 `_` 前缀（跨批裁切判据）+ 仓根硬编码改 `dirname(dirname(__file__))` |
| scripts/check_plan_template.py | W1002 | import 与 docstring 改转正名 |
| scripts/check_script_coverage.py | W1002 | 第 42 门禁新增 C4（历史批滞留必红 + 转正候选棘轮 8 件）+ 自测 6→9 例 |
| scripts/ledger_mutation_test.py | W1002 | 转正：去 `_` 前缀（Makefile ledger 目标调用·W933 建） |
| scripts/output/tools-inventory.md | W1002 | 重生成（152 件） |
| scripts/plan_template_review.py | W1002 | 转正：去 `_` 前缀（第 48 门禁判据表·W857 建） |
| scripts/plates_verify.py | W1002 | 转正：去 `_` 前缀（跨批素材判据 J1–J10·W945 建） |
| tests/unit/test_script_hygiene.py | W1002 | C4 判据纯函数 + 转正件加载性 + 门禁自测端到端（5 例） |
| .github/workflows/README.md | W1002 | 本批新增/修改 |
| CHANGELOG.md | W1002 | 本批新增/修改 |
| CITATION.cff | W1002 | 本批新增/修改 |
| HANDOVER.md | W1002 | 本批新增/修改 |
| README.md | W1002 | 本批新增/修改 |
| STRUCTURE.md | W1002 | 本批新增/修改 |
| archive/docs/AGENTS-ARCHIVE.md | W1002 | 滚动归档回窗（4 段/2 行迁出） |
| archive/docs/CHANGELOG-ARCHIVE.md | W1002 | 滚动归档回窗（4 段/2 行迁出） |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1002 | 滚动归档回窗（4 段/2 行迁出） |
| archive/docs/file-index-ARCHIVE.md | W1002 | 滚动归档回窗（4 段/2 行迁出） |
| archive/scripts/batches/README.md | W1002 | 一次性/批次脚本移入归档桶（三档归位） |
| archive/scripts/batches/index.md | W1002 | 一次性/批次脚本移入归档桶（三档归位） |
| archive/scripts/batches/w9xx/README.md | W1002 | 一次性/批次脚本移入归档桶（三档归位） |
| archive/scripts/batches/w9xx/index.md | W1002 | 一次性/批次脚本移入归档桶（三档归位） |
| docs/00-导读/W批次编号对账表.md | W1002 | 台账认领行 + 行归档回窗（W942-W943 迁出） |
| docs/00-导读/项目说明.md | W1002 | 本批新增/修改 |
| docs/11-方案报告/工作复盘与优化分析报告/工作复盘与优化分析报告-2026-10-27.md | W1002 | 取证脚本链接改归档路径（lint_links 活链校正） |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1002 | 本批新增/修改 |
| pytest.ini | W1002 | 本批新增/修改 |
| scripts/index.md | W1002 | 目录索引重生成（scripts/ 根减 84 件） |
| scripts/output/_cascade_files_W1002.txt | W1002 | 本批新增/修改 |
| scripts/output/_vermilion_solid_cache.json | W1002 | 本批新增/修改 |
| scripts/output/_w1002_spec.json | W1002 | 本批级联 spec |
| scripts/output/file-index.md | W1002 | 本批新增/修改 |
| scripts/output/stats-changelog.json | W1002 | 本批新增/修改 |
| scripts/output/stats-index.md | W1002 | 本批新增/修改 |
| scripts/output/stats.json | W1002 | C5d 实算对账刷新（--w W1002） |
| site/data/cross-time-danmaku.html | W1002 | 本批新增/修改 |
| site/data/tag-cloud.html | W1002 | 本批新增/修改 |
| site/dukou-engine.html | W1002 | 本批新增/修改 |
| site/index.html | W1002 | 本批新增/修改 |
| scripts/output/README.md | W1002 | 本批新增/修改 |
| scripts/output/index.md | W1002 | 本批新增/修改 |
| tests/unit/README.md | W1002 | 本批新增/修改 |
| tests/unit/index.md | W1002 | 本批新增/修改 |

## W1001 回次 og:image 全覆盖批·第一轮试点（2026-10-28）

| 文件 | W | 说明 |
|---|---|---|
| .github/workflows/README.md | W1001 | 本批新增/修改 |
| AGENTS.md | W1001 | 本批新增/修改 |
| CHANGELOG.md | W1001 | 本批新增/修改 |
| CITATION.cff | W1001 | 本批新增/修改 |
| HANDOVER.md | W1001 | 本批新增/修改 |
| README.md | W1001 | 本批新增/修改 |
| STRUCTURE.md | W1001 | 本批新增/修改 |
| archive/docs/AGENTS-ARCHIVE.md | W1001 | 本批新增/修改 |
| assets/promo/plate-set/plate-line-49-ch001-xianshi.png | W1001 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-49-ch001-xianshi.webp | W1001 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-50-ch003-aoguang.png | W1001 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-50-ch003-aoguang.webp | W1001 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-51-ch009-yuanshoucheng.png | W1001 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-51-ch009-yuanshoucheng.webp | W1001 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-52-ch011-xiaoyu.png | W1001 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-52-ch011-xiaoyu.webp | W1001 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-53-ch022-liushahe.png | W1001 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-53-ch022-liushahe.webp | W1001 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-54-ch028-qunyao.png | W1001 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-54-ch028-qunyao.webp | W1001 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-55-ch047-tongtianhe.png | W1001 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-55-ch047-tongtianhe.webp | W1001 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-56-ch063-jiutou.png | W1001 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-56-ch063-jiutou.webp | W1001 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-57-ch066-mile.png | W1001 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-57-ch066-mile.webp | W1001 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-58-ch079-nanpo.png | W1001 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-58-ch079-nanpo.webp | W1001 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-59-ch089-huangshi.png | W1001 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-59-ch089-huangshi.webp | W1001 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-60-ch093-geigu.png | W1001 | 新增母版（1200×1600） |
| assets/promo/plate-set/plate-line-60-ch093-geigu.webp | W1001 | 新增母版（1200×1600） |
| assets/promo/plate-set/preview-contact-sheet.png | W1001 | 本批新增/修改 |
| assets/promo/plate-set/preview-contact-sheet.webp | W1001 | 本批新增/修改 |
| assets/promo/plate-set/raw/round14/README.md | W1001 | 出图原件（12 张·含重出） |
| assets/promo/plate-set/raw/round14/index.md | W1001 | 出图原件（12 张·含重出） |
| assets/promo/plate-set/raw/round14/plate-line-49-ch001-xianshi.jpg | W1001 | 出图原件（12 张·含重出） |
| assets/promo/plate-set/raw/round14/plate-line-50-ch003-aoguang.jpg | W1001 | 出图原件（12 张·含重出） |
| assets/promo/plate-set/raw/round14/plate-line-51-ch009-yuanshoucheng.jpg | W1001 | 出图原件（12 张·含重出） |
| assets/promo/plate-set/raw/round14/plate-line-52-ch011-xiaoyu.jpg | W1001 | 出图原件（12 张·含重出） |
| assets/promo/plate-set/raw/round14/plate-line-53-ch022-liushahe.jpg | W1001 | 出图原件（12 张·含重出） |
| assets/promo/plate-set/raw/round14/plate-line-54-ch028-qunyao.jpg | W1001 | 出图原件（12 张·含重出） |
| assets/promo/plate-set/raw/round14/plate-line-55-ch047-tongtianhe.jpg | W1001 | 出图原件（12 张·含重出） |
| assets/promo/plate-set/raw/round14/plate-line-56-ch063-jiutou.jpg | W1001 | 出图原件（12 张·含重出） |
| assets/promo/plate-set/raw/round14/plate-line-57-ch066-mile.jpg | W1001 | 出图原件（12 张·含重出） |
| assets/promo/plate-set/raw/round14/plate-line-58-ch079-nanpo.jpg | W1001 | 出图原件（12 张·含重出） |
| assets/promo/plate-set/raw/round14/plate-line-59-ch089-huangshi.jpg | W1001 | 出图原件（12 张·含重出） |
| assets/promo/plate-set/raw/round14/plate-line-60-ch093-geigu.jpg | W1001 | 出图原件（12 张·含重出） |
| docs/00-导读/W批次编号对账表.md | W1001 | 登记面（报告/坑表/计数链/方法论/台账） |
| docs/00-导读/项目说明.md | W1001 | 登记面（报告/坑表/计数链/方法论/台账） |
| docs/10-方法论沉淀/素材批处理与判据自证方法论.md | W1001 | 登记面（报告/坑表/计数链/方法论/台账） |
| docs/11-方案报告/README.md | W1001 | 登记面（报告/坑表/计数链/方法论/台账） |
| docs/11-方案报告/计划方案/T35-任务计划执行与经验沉淀报告-2026-10-28.md | W1001 | 登记面（报告/坑表/计数链/方法论/台账） |
| docs/agent/pitfalls.md | W1001 | 登记面（报告/坑表/计数链/方法论/台账） |
| scripts/_w1001_stage.py | W1001 | 本批工具/产物 |
| scripts/_w951_check_crop.py | W1001 | 本批工具/产物 |
| scripts/_w990_map.py | W1001 | 本批工具/产物 |
| scripts/_w990_master.py | W1001 | 本批工具/产物 |
| scripts/_w990_og_gap.py | W1001 | 本批工具/产物 |
| scripts/_w990_read.py | W1001 | 本批工具/产物 |
| scripts/_w990_roster.py | W1001 | 本批工具/产物 |
| scripts/_w990_split.py | W1001 | 本批工具/产物 |
| scripts/_w999_closeout.py | W1001 | 本批工具/产物 |
| scripts/_w999_derive_prepare.py | W1001 | 本批工具/产物 |
| scripts/_w999_insert.py | W1001 | 本批工具/产物 |
| scripts/_w999_make_spec.py | W1001 | 本批工具/产物 |
| scripts/_w999_prepare.py | W1001 | 本批工具/产物 |
| scripts/_w999_rebuild_missing_og.py | W1001 | 本批工具/产物 |
| scripts/_w999_redo.py | W1001 | 本批工具/产物 |
| scripts/_w999_redo2.py | W1001 | 本批工具/产物 |
| scripts/_w999_sheet.py | W1001 | 本批工具/产物 |
| scripts/_w999_verify.py | W1001 | 本批工具/产物 |
| scripts/output/_w1001_spec.json | W1001 | 本批工具/产物 |
| scripts/output/file-index.md | W1001 | 本批工具/产物 |
| site/data/cross-time-danmaku.html | W1001 | 本批新增/修改 |
| site/data/tag-cloud.html | W1001 | 本批新增/修改 |
| site/dukou-engine.html | W1001 | 本批新增/修改 |
| site/index.html | W1001 | 本批新增/修改 |
| site/reader/ch001.html | W1001 | 回目页接入题图 + 换专属 1200×630 og:image |
| site/reader/ch003.html | W1001 | 回目页接入题图 + 换专属 1200×630 og:image |
| site/reader/ch009.html | W1001 | 回目页接入题图 + 换专属 1200×630 og:image |
| site/reader/ch011.html | W1001 | 回目页接入题图 + 换专属 1200×630 og:image |
| site/reader/ch022.html | W1001 | 回目页接入题图 + 换专属 1200×630 og:image |
| site/reader/ch028.html | W1001 | 回目页接入题图 + 换专属 1200×630 og:image |
| site/reader/ch047.html | W1001 | 回目页接入题图 + 换专属 1200×630 og:image |
| site/reader/ch063.html | W1001 | 回目页接入题图 + 换专属 1200×630 og:image |
| site/reader/ch066.html | W1001 | 回目页接入题图 + 换专属 1200×630 og:image |
| site/reader/ch079.html | W1001 | 回目页接入题图 + 换专属 1200×630 og:image |
| site/reader/ch089.html | W1001 | 回目页接入题图 + 换专属 1200×630 og:image |
| site/reader/ch093.html | W1001 | 回目页接入题图 + 换专属 1200×630 og:image |
| site/static/images/og-plate-line-40-ch023-sichan.webp | W1001 | 专属 og:image（1200×630·由母版裁切） |
| site/static/images/og-plate-line-41-ch027-bailong.webp | W1001 | 专属 og:image（1200×630·由母版裁切） |
| site/static/images/og-plate-line-42-ch030-sancha.webp | W1001 | 专属 og:image（1200×630·由母版裁切） |
| site/static/images/og-plate-line-43-luoshanv.webp | W1001 | 专属 og:image（1200×630·由母版裁切） |
| site/static/images/og-plate-line-44-kuimulang.webp | W1001 | 专属 og:image（1200×630·由母版裁切） |
| site/static/images/og-plate-line-45-zhaoan-topic.webp | W1001 | 专属 og:image（1200×630·由母版裁切） |
| site/static/images/og-plate-line-46-fushi-topic.webp | W1001 | 专属 og:image（1200×630·由母版裁切） |
| site/static/images/og-plate-line-47-jingwu-topic.webp | W1001 | 专属 og:image（1200×630·由母版裁切） |
| site/static/images/og-plate-line-48-xuanzang-topic.webp | W1001 | 专属 og:image（1200×630·由母版裁切） |
| site/static/images/og-plate-line-49-ch001-xianshi.webp | W1001 | 专属 og:image（1200×630·由母版裁切） |
| site/static/images/og-plate-line-50-ch003-aoguang.webp | W1001 | 专属 og:image（1200×630·由母版裁切） |
| site/static/images/og-plate-line-51-ch009-yuanshoucheng.webp | W1001 | 专属 og:image（1200×630·由母版裁切） |
| site/static/images/og-plate-line-52-ch011-xiaoyu.webp | W1001 | 专属 og:image（1200×630·由母版裁切） |
| site/static/images/og-plate-line-53-ch022-liushahe.webp | W1001 | 专属 og:image（1200×630·由母版裁切） |
| site/static/images/og-plate-line-54-ch028-qunyao.webp | W1001 | 专属 og:image（1200×630·由母版裁切） |
| site/static/images/og-plate-line-55-ch047-tongtianhe.webp | W1001 | 专属 og:image（1200×630·由母版裁切） |
| site/static/images/og-plate-line-56-ch063-jiutou.webp | W1001 | 专属 og:image（1200×630·由母版裁切） |
| site/static/images/og-plate-line-57-ch066-mile.webp | W1001 | 专属 og:image（1200×630·由母版裁切） |
| site/static/images/og-plate-line-58-ch079-nanpo.webp | W1001 | 专属 og:image（1200×630·由母版裁切） |
| site/static/images/og-plate-line-59-ch089-huangshi.webp | W1001 | 专属 og:image（1200×630·由母版裁切） |
| site/static/images/og-plate-line-60-ch093-geigu.webp | W1001 | 专属 og:image（1200×630·由母版裁切） |
| site/static/images/plate-line-49-ch001-xianshi.webp | W1001 | 站点版（母版裁切·只裁上部留白） |
| site/static/images/plate-line-50-ch003-aoguang.webp | W1001 | 站点版（母版裁切·只裁上部留白） |
| site/static/images/plate-line-51-ch009-yuanshoucheng.webp | W1001 | 站点版（母版裁切·只裁上部留白） |
| site/static/images/plate-line-52-ch011-xiaoyu.webp | W1001 | 站点版（母版裁切·只裁上部留白） |
| site/static/images/plate-line-53-ch022-liushahe.webp | W1001 | 站点版（母版裁切·只裁上部留白） |
| site/static/images/plate-line-54-ch028-qunyao.webp | W1001 | 站点版（母版裁切·只裁上部留白） |
| site/static/images/plate-line-55-ch047-tongtianhe.webp | W1001 | 站点版（母版裁切·只裁上部留白） |
| site/static/images/plate-line-56-ch063-jiutou.webp | W1001 | 站点版（母版裁切·只裁上部留白） |
| site/static/images/plate-line-57-ch066-mile.webp | W1001 | 站点版（母版裁切·只裁上部留白） |
| site/static/images/plate-line-58-ch079-nanpo.webp | W1001 | 站点版（母版裁切·只裁上部留白） |
| site/static/images/plate-line-59-ch089-huangshi.webp | W1001 | 站点版（母版裁切·只裁上部留白） |
| site/static/images/plate-line-60-ch093-geigu.webp | W1001 | 站点版（母版裁切·只裁上部留白） |

## W1000 对抗式审查常驻化批（2026-10-28）

| 文件 | W | 说明 |
|---|---|---|
| scripts/check_audit_trigger.py | W1000 | 新建对抗式审查触发器（台账即事实源·四态自测） |
| docs/agent/adversarial-audit-prompt.md | W1000 | 派发 prompt 模板（W998 实战沉淀·收尾义务四条） |
| scripts/preflight_check.py | W1000 | 触发器提示位接线 |

## W999 必守纪律晋升批（2026-10-28）

| 文件 | W | 说明 |
|---|---|---|
| AGENTS.md | W999 | §6 铁律 14 修实例必修根（权威落点） |
| CLAUDE.md | W999 | 速查第 12 行（指向 §6-14 与 pitfalls 流程组） |

## W998 对抗式审查修复批（2026-10-28）

| 文件 | W | 说明 |
|---|---|---|
| scripts/check_doc_size_budget.py | W998 | C4 移出 HANDOVER 门控（死门控+fline NameError 修复） |
| scripts/cascade_lock.py | W998 | 创建中短重试防双持 + CLI --pid |
| scripts/batch_cascade.py | W998 | finally release 传 pid + [SCRIPTS] 口径随 W992 |
| docs/agent/pitfalls.md | W997 | 子节标题计数校准（级联 9·流程 20） |

## W997 协作纪律入库批（2026-10-27）

| 文件 | W | 说明 |
|---|---|---|
| docs/agent/pitfalls.md | W997 | 流程组新增「修实例必修根+检查按字面范围」（89→90） |
| AGENTS.md | W997 | §4.3 计数两处同步（90 条·流程 20） |
| scripts/archive_ledger_rows.py | W997 | A4 收紧为真在途判据（已停止行不误伤） |

## W996 流程提示位批（2026-10-28）

| 文件 | W | 说明 |
|---|---|---|
| scripts/ledger_close_check.py | W996 | C2 判据：反向迭代台账——已收官+hash 落地+无级联段（现役+归档两面）=漏跑 batch_cascade；豁免让号/并号/已停止/空壳/作废/补录/追记；--allow-open 不豁免本判据；self-test 扩 C2 三态
| docs/00-导读/W批次编号对账表.md | W996 | W996 认领行与收官回填
| CHANGELOG.md | W996 | W996 段
| HANDOVER.md | W996 | 级联头尾链与里程碑块
| README.md | W996 | 当前批次版本行
| STRUCTURE.md | W996 | 当前批次版本行
| docs/00-导读/项目说明.md | W996 | 当前批次版本行
| .github/workflows/README.md | W996 | 工作流层版本面推进 W996
| site/index.html | W996 | 页脚批次链插入 W996
| site/data/cross-time-danmaku.html | W996 | 页脚批次链插入 W996
| site/data/tag-cloud.html | W996 | 页脚批次链插入 W996
| site/dukou-engine.html | W996 | 页脚批次链插入 W996
| AGENTS.md | W996 | 版本脚注条目
| archive/docs/AGENTS-ARCHIVE.md | W996 | 脚注滚动迁入的最老条目
| CITATION.cff | W996 | version 同步为 W996
| scripts/output/file-index.md | W996 | W996 段插入
| scripts/output/_w996_spec.json | W996 | 本批级联 spec
| scripts/output/_cascade_files_W996.txt | W996 | 级联落盘清单

## W995 tier2 按W段拆分批（2026-10-28）

| 文件 | W | 说明 |
|---|---|---|
| archive/docs/CHANGELOG-ARCHIVE-tier2.md | W995 | 拆分：1044KB→746KB（W001-W399·210 段留存·范围件 W400-W559 抽出）
| archive/docs/CHANGELOG-ARCHIVE-tier2-W400-W559.md | W995 | 新建范围件（W400-W559·144 段 299KB·范围命名约定首件）
| scripts/archive_tier2.py | W995 | 追加逻辑升级：容量判断（容器+迁出 >1MB → 自动开范围命名新件·合规头部生成）+ LIMIT 常量
| scripts/check_archive_health.py | W995 | T1b 升格：tier2 破线从登记观察升为 problem（拆分约定后可执行）+ glob 扩范围件 + run(prefix) 参数
| scripts/batch_cascade.py | W995 | 收官提示位扩展（W994 延后件·W992 校准提交后落）：[ARCHIVE] 健康行 + [TMPE] 上次清理活动日期（独立尾部块）
| scripts/verify_delivery.py | W995 | ARCHIVE_DOCS 登记 +2（file-index-ARCHIVE-tier2.md·CHANGELOG-ARCHIVE-tier2-W400-W559.md·§11.2 tier2 须登记条款）
| archive/README.md | W995 | 台账 2 行（范围件/file-index-tier2）+ 结构树补范围件
| docs/00-导读/W批次编号对账表.md | W995 | W995 认领行与收官回填
| CHANGELOG.md | W995 | W995 段
| HANDOVER.md | W995 | 级联头尾链与里程碑块
| README.md | W995 | 当前批次版本行
| STRUCTURE.md | W995 | 当前批次版本行
| docs/00-导读/项目说明.md | W995 | 当前批次版本行
| .github/workflows/README.md | W995 | 工作流层版本面推进 W995
| site/index.html | W995 | 页脚批次链插入 W995
| site/data/cross-time-danmaku.html | W995 | 页脚批次链插入 W995
| site/data/tag-cloud.html | W995 | 页脚批次链插入 W995
| site/dukou-engine.html | W995 | 页脚批次链插入 W995
| AGENTS.md | W995 | 版本脚注条目
| archive/docs/AGENTS-ARCHIVE.md | W995 | 脚注滚动迁入的最老条目
| CITATION.cff | W995 | version 同步为 W995
| scripts/output/file-index.md | W995 | W995 段插入
| scripts/output/_w995_spec.json | W995 | 本批级联 spec（补建）
| scripts/output/_cascade_files_W995.txt | W995 | 级联落盘清单

## W994 归档系统打磨批（2026-10-28）

| 文件 | W | 说明 |
|---|---|---|
| scripts/check_archive_health.py | W994 | 新建：归档区健康探针（T1 tier-2 判距/T2 台账组行计数对账/T3 冷存储警告在位/T4 汇总·报告型 --strict 门禁候选·--self-test）
| scripts/archive_tier2.py | W994 | 新建：二级归档常驻工具（键序前缀切分·守恒五道·§11.2 1MB 线执行器·--self-test）
| tests/unit/test_archive_health.py | W994 | 单测 5 例（T1 三态/T2 语义含 batches 门面件排除/切分前缀/混层键 0）
| archive/docs/CHANGELOG-ARCHIVE.md | W994 | tier-2 实跑回线：1198KB→900KB（迁出 144 段 W400-W559 至 tier2·指针行入头部链）
| archive/docs/CHANGELOG-ARCHIVE-tier2.md | W994 | 承接 144 段（W400-W559·298KB）
| archive/docs/file-index-ARCHIVE.md | W994 | tier-2 实跑回线：1070KB→816KB（迁出 10 目录节至 tier2·指针行入头部链）
| archive/docs/file-index-ARCHIVE-tier2.md | W994 | 新建（§11.2 二级归档层·首批 10 节 254KB）
| archive/README.md | W994 | 存量组行补登记 3 条（顶层 47 件/w4xx 11 件/w5xx 149 件·此前仅结构树目录级提及·探针 T2 对账基线）
| archive/scripts/batches/README.md | W994 | 冷存储警告补入（W836 ROOT 上溯失效·禁直接运行·T3 判据标的）
| scripts/README.md | W994 | 场景速查 +2 行（二级归档/健康体检路由）
| docs/00-导读/W批次编号对账表.md | W994 | W994 认领行与收官回填
| CHANGELOG.md | W994 | W994 段
| HANDOVER.md | W994 | 级联头尾链与里程碑块
| README.md | W994 | 当前批次版本行
| STRUCTURE.md | W994 | 当前批次版本行
| docs/00-导读/项目说明.md | W994 | 当前批次版本行
| .github/workflows/README.md | W994 | 工作流层版本面推进 W994
| site/index.html | W994 | 页脚批次链插入 W994
| site/data/cross-time-danmaku.html | W994 | 页脚批次链插入 W994
| site/data/tag-cloud.html | W994 | 页脚批次链插入 W994
| site/dukou-engine.html | W994 | 页脚批次链插入 W994
| AGENTS.md | W994 | 版本脚注条目
| archive/docs/AGENTS-ARCHIVE.md | W994 | 脚注滚动迁入的最老条目
| CITATION.cff | W994 | version 同步为 W994
| scripts/output/file-index.md | W994 | W994 段插入
| scripts/output/_w994_spec.json | W994 | 本批级联 spec
| scripts/output/_cascade_files_W994.txt | W994 | 级联落盘清单
| scripts/gen_folder_docs.py | W994 | 冷存储警告模板级注入（archive/scripts/batches README·防 refresh 覆写） |

## W993 全仓行尾定形批（2026-10-27）

| 文件 | W | 说明 |
|---|---|---|
| .gitattributes | W993 | text=auto eol=lf + 二进制显式排除 |
| .git-blame-ignore-revs | W993 | 登记定形提交 84cce358 |
| docs/agent/pitfalls.md | W993 | 行尾定形时代结束条目（CRLF 锚定作废） |
| AGENTS.md | W993 | 坑位计数 88→89 两处同步 |

## W992 一次性件定向退役与提示位口径校准批（2026-10-27）

| 文件 | W | 说明 |
|---|---|---|
| archive/scripts/batches/w9xx/ | W992 | 迁入 4 件（_w988 族·零引用） |
| scripts/batch_cascade.py | W992 | [SCRIPTS] 提示位口径校准 |

## W991 级联运行锁与提交隔离批（2026-10-27）

| 文件 | W | 说明 |
|---|---|---|
| scripts/cascade_lock.py | W991 | 新建级联运行锁（O_EXCL·陈旧夺·损坏夺·五态自测） |
| scripts/batch_cascade.py | W991 | --apply 全程持锁（finally 必释放） |
| scripts/preflight_check.py | W991 | 活动锁 WARN 接线（共享面中态警示） |
| scripts/safe_commit.py | W991 | 无 pathspec+有暂存即拒（守卫纯函数三态） |

## W990 内联纪律收口批（2026-10-27）

| 文件 | W | 说明 |
|---|---|---|
| docs/agent/pitfalls.md | W990 | 查坑表补报错原文 literal（truncated \xXX escape/unicodeescape/invalid escape sequence·撞错 grep 即中）+ 新增条目「并行会话在场的未提交工作树编辑会被吸收或覆盖」（git 节 21→22·总数 87→88）
| AGENTS.md | W990 | 坑位数 87→88（阅读契约+主题视图·git 节 21→22·W990 校）+ 版本脚注条目
| HANDOVER.md | W990 | 坑位数指针 87→88 两处 + 级联头尾链与里程碑块
| docs/00-导读/W批次编号对账表.md | W990 | W990 认领行与收官回填
| CHANGELOG.md | W990 | W990 段
| README.md | W990 | 当前批次版本行
| STRUCTURE.md | W990 | 当前批次版本行
| docs/00-导读/项目说明.md | W990 | 当前批次版本行
| .github/workflows/README.md | W990 | 工作流层版本面推进 W990
| site/index.html | W990 | 页脚批次链插入 W990
| site/data/cross-time-danmaku.html | W990 | 页脚批次链插入 W990
| site/data/tag-cloud.html | W990 | 页脚批次链插入 W990
| site/dukou-engine.html | W990 | 页脚批次链插入 W990
| CITATION.cff | W990 | version 同步为 W990
| scripts/output/file-index.md | W990 | W990 段插入
| scripts/output/_w990_spec.json | W990 | 本批级联 spec
| scripts/output/_cascade_files_W990.txt | W990 | 级联落盘清单

## W989 脚注定形收紧批（2026-10-27）

| 文件 | W | 说明 |
|---|---|---|
| scripts/check_doc_size_budget.py · scripts/batch_cascade.py | W989 | C4 300→120 双写点收紧 |
| AGENTS.md | W989 | 五条脚注重写为索引体（55-65 字）·头注 ≤120 |
| scripts/archive_ledger_rows.py | W989 | 台账回窗 61→59 |

## W988 水墨卡族投放批（2026-10-27）

| 文件 | W | 说明 |
|---|---|---|
| site/reader/ch004.html | W988 | og:image 换专属 1200×630 裁切版 |
| site/reader/ch007.html | W988 | og:image 换专属 1200×630 裁切版 |
| site/reader/ch010.html | W988 | og:image 换专属 1200×630 裁切版 |
| site/reader/ch014.html | W988 | og:image 换专属 1200×630 裁切版 |
| site/reader/ch015.html | W988 | og:image 换专属 1200×630 裁切版 |
| site/reader/ch019.html | W988 | 接入落位（横幅/场景图）+ og:image 换专属图 |
| site/reader/ch023.html | W988 | og:image 换专属 1200×630 裁切版 |
| site/reader/ch027.html | W988 | og:image 换专属 1200×630 裁切版 |
| site/reader/ch030.html | W988 | og:image 换专属 1200×630 裁切版 |
| site/reader/ch031.html | W988 | 接入落位（横幅/场景图）+ og:image 换专属图 |
| site/reader/culture/历史玄奘与小说玄奘专题.html | W988 | og:image 换专属 1200×630 裁切版 |
| site/reader/culture/明代科举制度对照专题.html | W988 | og:image 换专属 1200×630 裁切版 |
| site/reader/culture/西游与佛教禅宗专题.html | W988 | 接入落位（横幅/场景图）+ og:image 换专属图 |
| site/reader/essays/西游与服饰学.html | W988 | og:image 换专属 1200×630 裁切版 |
| site/reader/essays/西游与民俗学.html | W988 | og:image 换专属 1200×630 裁切版 |
| site/reader/people/九灵元圣-方向二深化.html | W988 | og:image 换专属 1200×630 裁切版 |
| site/reader/people/二郎神.html | W988 | og:image 换专属 1200×630 裁切版 |
| site/reader/people/取经团队动力学深化专题.html | W988 | 接入落位（横幅/场景图）+ og:image 换专属图 |
| site/reader/people/哪吒.html | W988 | og:image 换专属 1200×630 裁切版 |
| site/reader/people/地府体系深化专题.html | W988 | og:image 换专属 1200×630 裁切版 |
| site/reader/people/大鹏金翅雕.html | W988 | og:image 换专属 1200×630 裁切版 |
| site/reader/people/太上老君.html | W988 | og:image 换专属 1200×630 裁切版 |
| site/reader/people/奎木狼外传.html | W988 | og:image 换专属 1200×630 裁切版 |
| site/reader/people/女儿国国王.html | W988 | og:image 换专属 1200×630 裁切版 |
| site/reader/people/如来.html | W988 | og:image 换专属 1200×630 裁切版 |
| site/reader/people/嫦娥外传.html | W988 | og:image 换专属 1200×630 裁切版 |
| site/reader/people/孙悟空.html | W988 | 接入落位（横幅/场景图）+ og:image 换专属图 |
| site/reader/people/托塔李天王外传.html | W988 | og:image 换专属 1200×630 裁切版 |
| site/reader/people/昴日星官.html | W988 | og:image 换专属 1200×630 裁切版 |
| site/reader/people/沙僧-方向二深化.html | W988 | 接入落位（横幅/场景图）+ og:image 换专属图 |
| site/reader/people/沙僧.html | W988 | 接入落位（横幅/场景图）+ og:image 换专属图 |
| site/reader/people/沙僧外传.html | W988 | 接入落位（横幅/场景图）+ og:image 换专属图 |
| site/reader/people/火焰山土地外传.html | W988 | 接入落位（横幅/场景图）+ og:image 换专属图 |
| site/reader/people/灵感大王.html | W988 | og:image 换专属 1200×630 裁切版 |
| site/reader/people/灵感大王外传.html | W988 | og:image 换专属 1200×630 裁切版 |
| site/reader/people/牛魔王.html | W988 | og:image 换专属 1200×630 裁切版 |
| site/reader/people/独角兕大王.html | W988 | og:image 换专属 1200×630 裁切版 |
| site/reader/people/狮驼岭三魔-方向二深化.html | W988 | 接入落位（横幅/场景图）+ og:image 换专属图 |
| site/reader/people/猪八戒-方向二深化.html | W988 | 接入落位（横幅/场景图）+ og:image 换专属图 |
| site/reader/people/猪八戒.html | W988 | 接入落位（横幅/场景图）+ og:image 换专属图 |
| site/reader/people/猪八戒深化专题.html | W988 | 接入落位（横幅/场景图）+ og:image 换专属图 |
| site/reader/people/玉兔精.html | W988 | og:image 换专属 1200×630 裁切版 |
| site/reader/people/玉帝.html | W988 | og:image 换专属 1200×630 裁切版 |
| site/reader/people/白骨精.html | W988 | og:image 换专属 1200×630 裁切版 |
| site/reader/people/白骨精外传.html | W988 | 接入落位（横幅/场景图）+ og:image 换专属图 |
| site/reader/people/白鹿精-方向二深化.html | W988 | 接入落位（横幅/场景图）+ og:image 换专属图 |
| site/reader/people/白龙马.html | W988 | og:image 换专属 1200×630 裁切版 |
| site/reader/people/百眼魔君.html | W988 | og:image 换专属 1200×630 裁切版 |
| site/reader/people/紧箍儿的内侧-器物传记.html | W988 | og:image 换专属 1200×630 裁切版 |
| site/reader/people/红孩儿.html | W988 | og:image 换专属 1200×630 裁切版 |
| site/reader/people/罗刹女外传.html | W988 | og:image 换专属 1200×630 裁切版 |
| site/reader/people/老鼋外传.html | W988 | og:image 换专属 1200×630 裁切版 |
| site/reader/people/老鼠精.html | W988 | og:image 换专属 1200×630 裁切版 |
| site/reader/people/蜘蛛精.html | W988 | 接入落位（横幅/场景图）+ og:image 换专属图 |
| site/reader/people/蝎子精.html | W988 | og:image 换专属 1200×630 裁切版 |
| site/reader/people/观音.html | W988 | og:image 换专属 1200×630 裁切版 |
| site/reader/people/赛太岁.html | W988 | og:image 换专属 1200×630 裁切版 |
| site/reader/people/车迟国三国师外传.html | W988 | og:image 换专属 1200×630 裁切版 |
| site/reader/people/金角大王.html | W988 | og:image 换专属 1200×630 裁切版 |
| site/reader/people/金角银角深化专题.html | W988 | og:image 换专属 1200×630 裁切版 |
| site/reader/people/铁扇公主.html | W988 | og:image 换专属 1200×630 裁切版 |
| site/reader/people/银角大王.html | W988 | og:image 换专属 1200×630 裁切版 |
| site/reader/people/镇元大仙.html | W988 | og:image 换专属 1200×630 裁切版 |
| site/reader/people/黄眉老佛外传.html | W988 | og:image 换专属 1200×630 裁切版 |
| site/reader/people/黄袍怪.html | W988 | og:image 换专属 1200×630 裁切版 |
| site/reader/people/黄风怪外传.html | W988 | og:image 换专属 1200×630 裁切版 |
| site/reader/people/黑熊精.html | W988 | og:image 换专属 1200×630 裁切版 |
| site/reader/poetry/原著景物诗分类赏析专题.html | W988 | 接入落位（横幅/场景图）+ og:image 换专属图 |
| site/reader/poetry/原著景物诗赏析专题.html | W988 | 接入落位（横幅/场景图）+ og:image 换专属图 |
| site/reader/poetry/西游诗词意象谱系专题.html | W988 | og:image 换专属 1200×630 裁切版 |
| site/reader/themes/二十八星宿专题.html | W988 | og:image 换专属 1200×630 裁切版 |
| site/reader/themes/五方揭谛专题.html | W988 | og:image 换专属 1200×630 裁切版 |
| site/reader/themes/佛学AI西游三维语义映射表.html | W988 | 接入落位（横幅/场景图）+ og:image 换专属图 |
| site/reader/themes/六丁六甲专题.html | W988 | og:image 换专属 1200×630 裁切版 |
| site/reader/themes/兵器的自我修养专题.html | W988 | og:image 换专属 1200×630 裁切版 |
| site/reader/themes/取经团队-凭什么走到西天.html | W988 | 接入落位（横幅/场景图）+ og:image 换专属图 |
| site/reader/themes/取经密码学专题.html | W988 | og:image 换专属 1200×630 裁切版 |
| site/reader/themes/取经教育学专题.html | W988 | 接入落位（横幅/场景图）+ og:image 换专属图 |
| site/reader/themes/取经路径地理符号学专题.html | W988 | og:image 换专属 1200×630 裁切版 |
| site/reader/themes/取经路线地理专题.html | W988 | og:image 换专属 1200×630 裁切版 |
| site/reader/themes/唐僧-凡躯圣心.html | W988 | og:image 换专属 1200×630 裁切版 |
| site/reader/themes/器物传记学专题.html | W988 | og:image 换专属 1200×630 裁切版 |
| site/reader/themes/四值功曹专题.html | W988 | og:image 换专属 1200×630 裁切版 |
| site/reader/themes/大闹天宫-英雄还是悲剧.html | W988 | og:image 换专属 1200×630 裁切版 |
| site/reader/themes/小妖生命史专题.html | W988 | 接入落位（横幅/场景图）+ og:image 换专属图 |
| site/reader/themes/招安的两种结局专题.html | W988 | og:image 换专属 1200×630 裁切版 |
| site/reader/themes/无字真经专题.html | W988 | 接入落位（横幅/场景图）+ og:image 换专属图 |
| site/reader/themes/水帘洞-瀑布门的世界.html | W988 | 接入落位（横幅/场景图）+ og:image 换专属图 |
| site/reader/themes/水帘洞专题.html | W988 | og:image 换专属 1200×630 裁切版 |
| site/reader/themes/沙僧-沉默者的智慧.html | W988 | 接入落位（横幅/场景图）+ og:image 换专属图 |
| site/reader/themes/法宝系统专题.html | W988 | og:image 换专属 1200×630 裁切版 |
| site/reader/themes/混世四猴专题.html | W988 | og:image 换专属 1200×630 裁切版 |
| site/reader/themes/猪八戒-不愿承认的自己.html | W988 | 接入落位（横幅/场景图）+ og:image 换专属图 |
| site/reader/themes/猴王到行者-五次蜕变.html | W988 | og:image 换专属 1200×630 裁切版 |
| site/reader/themes/真假美猴王专题.html | W988 | og:image 换专属 1200×630 裁切版 |
| site/reader/themes/神学干预机制专题.html | W988 | og:image 换专属 1200×630 裁切版 |
| site/reader/themes/空间叙事学专题.html | W988 | 接入落位（横幅/场景图）+ og:image 换专属图 |
| site/reader/themes/筋斗云专题.html | W988 | og:image 换专属 1200×630 裁切版 |
| site/reader/themes/紧箍咒专题.html | W988 | og:image 换专属 1200×630 裁切版 |
| site/reader/themes/蟠桃园-体制内的秘密.html | W988 | og:image 换专属 1200×630 裁切版 |
| site/reader/themes/西游与死亡研究专题.html | W988 | og:image 换专属 1200×630 裁切版 |
| site/reader/themes/金箍棒的重量-一万三千五百斤的秘密.html | W988 | og:image 换专属 1200×630 裁切版 |
| docs/11-方案报告/计划方案/T34-任务计划执行与经验沉淀报告-2026-10-27.md | W988 | 终稿报告件（计划 + 执行合一·含 27 张落位表） |
| docs/11-方案报告/README.md | W988 | §六 计划方案补登记 3 行（序号 41/42/43·T-18 / T-21 / T-34）· 件数 43 → 44 |
| docs/agent/pitfalls.md | W988 | 坑表 +7 条（80 → 87：行尾二次替换 / 设备像素当 CSS 像素 / 主体检测排除朱砂赭金 / 关键词法双重失效 / 主体顶裁前提 / 判据自身缺陷） |
| docs/10-方法论沉淀/素材批处理与判据自证方法论.md | W988 | 新增 §2.9「既有资产投放：落位表先行 + 三族资产三套类名 + 派生裁切的主体检测」 |
| docs/00-导读/W批次编号对账表.md | W988 | W988 认领行 + 收官状态 |
| AGENTS.md | W988 | 坑位条数声明 80 → 87 |
| HANDOVER.md | W988 | 坑位条数指针 80 → 87 |
| CHANGELOG.md | W988 | W988 段 |
| README.md | W988 | 当前批次版本行 |
| STRUCTURE.md | W988 | 当前批次版本行 |
| docs/00-导读/项目说明.md | W988 | 当前批次版本行 |
| .github/workflows/README.md | W988 | 工作流层版本面推进 W988 |
| site/index.html | W988 | 页脚批次链插入 W988 |
| site/data/cross-time-danmaku.html | W988 | 页脚批次链插入 W988 |
| site/data/tag-cloud.html | W988 | 页脚批次链插入 W988 |
| site/dukou-engine.html | W988 | 页脚批次链插入 W988 |
| archive/docs/AGENTS-ARCHIVE.md | W988 | 脚注滚动迁入的最老条目 |
| CITATION.cff | W988 | version 同步为 W988 |
| scripts/output/file-index.md | W988 | W988 段插入 |
| scripts/check_seo_head.py | W988 | og:image 白名单改**目录派生式**（W988 依用户指令「分回次 og:image」授权改管控件·W922 先例） |
| scripts/_w988_plan.py | W988 | 本批工具/产物 |
| scripts/_w988_subject.py | W988 | 本批工具/产物 |
| scripts/_w988_inventory.py | W988 | 本批工具/产物 |
| scripts/_w988_match.py | W988 | 本批工具/产物 |
| scripts/_w988_precheck.py | W988 | 本批工具/产物 |
| scripts/_w988_make_assets.py | W988 | 本批工具/产物 |
| scripts/_w988_insert.py | W988 | 本批工具/产物 |
| scripts/_w988_fix_eol.py | W988 | 本批工具/产物 |
| scripts/_w988_verify.py | W988 | 本批工具/产物 |
| scripts/_w988_sheet.py | W988 | 本批工具/产物 |
| scripts/_w988_card_sheet.py | W988 | 本批工具/产物 |
| scripts/_w988_pitfalls.py | W988 | 本批工具/产物 |
| scripts/_w988_docs.py | W988 | 本批工具/产物 |
| scripts/_w988_make_spec.py | W988 | 本批工具/产物 |
| scripts/_w988_fix_cascade.py | W988 | 本批工具/产物 |
| scripts/_w988_fix_gates.py | W988 | 本批工具/产物 |
| scripts/check_seo_head.py | W988 | 本批工具/产物 |
| scripts/output/_w988_spec.json | W988 | 本批工具/产物 |
| scripts/output/_w988_precheck.json | W988 | 本批工具/产物 |
| scripts/output/_w988_assets.json | W988 | 本批工具/产物 |
| scripts/output/_w988_inventory.json | W988 | 本批工具/产物 |
| scripts/output/_w988_match.json | W988 | 本批工具/产物 |
| scripts/output/_w988_card_map.json | W988 | 本批工具/产物 |
| scripts/output/_w988_card_sheet.png | W988 | 本批工具/产物 |
| scripts/output/_w988_sheet-banner.png | W988 | 本批工具/产物 |
| scripts/output/_w988_sheet-og.png | W988 | 本批工具/产物 |
| scripts/output/_cascade_files_W988.txt | W988 | 本批工具/产物 |

## W987 水墨意境卡族启用批（2026-10-27）

| 文件 | W | 说明 |
|---|---|---|
| site/reader/ch007.html | W987 | 新增场景图（`.chapter-scene`·第 007 回八卦炉意境图） |
| site/reader/ch014.html | W987 | 新增场景图（第 014 回猴形剪影意境图） |
| site/reader/ch015.html | W987 | 新增场景图（第 015 回白马崖意境图） |
| site/reader/ch023.html | W987 | 新增场景图（第 023 回静坐烛影意境图） |
| site/reader/ch027.html | W987 | 新增场景图（第 027 回三背影茅屋意境图） |
| site/reader/ch030.html | W987 | 新增场景图（第 030 回黑虎洞穴意境图） |
| assets/promo/README.md | W987 | 新增「水墨意境卡族」节（成员 33 张·规范边界表·投放位置建议·维护约定） |
| docs/11-方案报告/计划方案/T33-任务计划执行与经验沉淀报告-2026-10-27.md | W987 | 终稿报告件（计划 + 执行合一） |
| docs/00-导读/W批次编号对账表.md | W987 | W987 认领行 + 收官状态 |
| docs/11-方案报告/README.md | W987 | §六 计划方案登记 +1 行（序号 40·T-33）· 件数 42 → 43 |
| docs/agent/pitfalls.md | W987 | 坑表 +3 条（77 → 80：资产族归族登记 / 类名隔开规范 / 同页两图首屏留主资产） |
| AGENTS.md | W987 | 坑位条数声明 77 → 80 |
| HANDOVER.md | W987 | 坑位条数指针 77 → 80 |
| CHANGELOG.md | W987 | W987 段 |
| README.md | W987 | 当前批次版本行 |
| STRUCTURE.md | W987 | 当前批次版本行 |
| docs/00-导读/项目说明.md | W987 | 当前批次版本行 |
| .github/workflows/README.md | W987 | 工作流层版本面推进 W987 |
| site/index.html | W987 | 页脚批次链插入 W987 |
| site/data/cross-time-danmaku.html | W987 | 页脚批次链插入 W987 |
| site/data/tag-cloud.html | W987 | 页脚批次链插入 W987 |
| site/dukou-engine.html | W987 | 页脚批次链插入 W987 |
| archive/docs/AGENTS-ARCHIVE.md | W987 | 脚注滚动迁入的最老条目 |
| CITATION.cff | W987 | version 同步为 W987 |
| scripts/output/file-index.md | W987 | W987 段插入 |
| scripts/_w987_family_scan.py | W987 | 族盘点 + 插入点实测（成员/尺寸/引用/行号） |
| scripts/_w987_insert_scenes.py | W987 | 6 页场景图接入（`.chapter-scene`·幂等） |
| scripts/output/_w987_family_scan.json | W987 | 族盘点报告 |
| scripts/output/_w987_spec.json | W987 | 本批级联 spec |
| scripts/output/_cascade_files_W987.txt | W987 | 级联落盘清单 |

## W986 回目页 6 张线描版换主体重出批（2026-10-27）

| 文件 | W | 说明 |
|---|---|---|
docs/11-方案报告/计划方案/T32-任务计划执行与经验沉淀报告-2026-10-27.md
docs/00-导读/W批次编号对账表.md
docs/agent/pitfalls.md
docs/10-方法论沉淀/素材批处理与判据自证方法论.md
docs/11-方案报告/README.md
| assets/promo/plate-set/plate-line-37..42.png/.webp | W986 | 同名覆盖重出：巨灵神 / 六贼头目 / 惠岸行者木叉 / 黎山老母 / 巡河夜叉 / 御马监丞（已由 9841c05d 落地） |
| assets/promo/plate-set/raw/round13/plate-line-37..42.jpg | W986 | 出图原件 6 份（已由 9841c05d 落地） |
| site/static/images/plate-line-37..42.webp | W986 | 站点版 6 个（已由 9841c05d 落地） |
| site/reader/{ch007,ch014,ch015,ch023,ch027,ch030}.html | W986 | 6 页题图 alt 文本更新为新主体（img src 不变·已由 9841c05d 落地） |
| assets/promo/plate-set/README.md | W986 | 第七组清单改新主体 + 存量归档节补演进（已由 9841c05d 落地） |
| scripts/_w986_make_prompts.py | W986 | 换主体出图参数生成器（母版段逐字复用 + 同名覆盖前提断言） |
| scripts/output/_w986_batch1.json | W986 | 本批出图参数（6 条） |
| scripts/output/_w986_gen.json | W986 | node_id ↔ 文件名映射 |
| scripts/output/_w986_sheet.png | W986 | 本批 6 张复核拼图 |
| CHANGELOG.md | W986 | W986 段 |
| HANDOVER.md | W986 | 坑位条数指针 75 → 77 |
| README.md | W986 | 当前批次版本行 |
| STRUCTURE.md | W986 | 当前批次版本行 |
| docs/00-导读/项目说明.md | W986 | 当前批次版本行 |
| .github/workflows/README.md | W986 | 工作流层版本面推进 W986 |
| site/index.html | W986 | 页脚批次链插入 W986 |
| site/data/cross-time-danmaku.html | W986 | 页脚批次链插入 W986 |
| site/data/tag-cloud.html | W986 | 页脚批次链插入 W986 |
| site/dukou-engine.html | W986 | 页脚批次链插入 W986 |
| AGENTS.md | W986 | 坑位条数声明 75 → 77 |
| archive/docs/AGENTS-ARCHIVE.md | W986 | 脚注滚动迁入的最老条目 |
| CITATION.cff | W986 | version 同步为 W986 |
| scripts/output/file-index.md | W986 | W986 段插入 |
| scripts/output/_w986_spec.json | W986 | 本批级联 spec |
| scripts/output/_cascade_files_W986.txt | W986 | 级联落盘清单 |

## W985 工具文档三件批（2026-10-27）

| 文件 | W | 说明 |
|---|---|---|
| scripts/README.md | W985 | 场景速查路由表（15 场景→工具）+ 归档计数指针化（45 个→历次治理台账指针）+ 全量清单指针 + docs_index 321 篇字面量指针化
| scripts/gen_tools_inventory.py | W985 | 新建：顶层工具清单机器生成器（tracked 顶层逐件·docstring 提取·分类规则·--check 对账·--self-test）
| scripts/output/tools-inventory.md | W985 | 机器生成清单首版（171 件·七类分节·禁手改·随刷新链更新）
| scripts/gen_folder_docs.py | W985 | --refresh 刷新链挂载工具清单再生成（失败留痕不阻断）
| tests/unit/test_tools_inventory.py | W985 | 单测 5 例（分类优先级/用途提取/分节渲染/check 漂移判据/实盘行数回归锁）
| docs/00-导读/W批次编号对账表.md | W985 | W985 认领行与收官回填
| CHANGELOG.md | W985 | W985 段
| HANDOVER.md | W985 | 级联头尾链与里程碑块
| README.md | W985 | 当前批次版本行
| STRUCTURE.md | W985 | 当前批次版本行
| docs/00-导读/项目说明.md | W985 | 当前批次版本行
| .github/workflows/README.md | W985 | 工作流层版本面推进 W985
| site/index.html | W985 | 页脚批次链插入 W985
| site/data/cross-time-danmaku.html | W985 | 页脚批次链插入 W985
| site/data/tag-cloud.html | W985 | 页脚批次链插入 W985
| site/dukou-engine.html | W985 | 页脚批次链插入 W985
| AGENTS.md | W985 | 版本脚注条目
| archive/docs/AGENTS-ARCHIVE.md | W985 | 脚注滚动迁入的最老条目
| CITATION.cff | W985 | version 同步为 W985
| scripts/output/file-index.md | W985 | W985 段插入
| scripts/output/_w985_spec.json | W985 | 本批级联 spec
| scripts/output/_cascade_files_W985.txt | W985 | 级联落盘清单

## W984 内页题图成套批·第四组（2026-10-27）

| 文件 | W | 说明 |
|---|---|---|
| site/static/images/plate-line-37-ch007-bagua-lu.webp | W984 | 新增·站点版（37-ch007-bagua-lu） |
| site/static/images/plate-line-38-ch014-liubei.webp | W984 | 新增·站点版（38-ch014-liubei） |
| site/static/images/plate-line-39-ch015-yingchou.webp | W984 | 新增·站点版（39-ch015-yingchou） |
| site/static/images/plate-line-40-ch023-sichan.webp | W984 | 新增·站点版（40-ch023-sichan） |
| site/static/images/plate-line-41-ch027-bailong.webp | W984 | 新增·站点版（41-ch027-bailong） |
| site/static/images/plate-line-42-ch030-sancha.webp | W984 | 新增·站点版（42-ch030-sancha） |
| site/static/images/plate-line-43-luoshanv.webp | W984 | 新增·站点版（43-luoshanv） |
| site/static/images/plate-line-44-kuimulang.webp | W984 | 新增·站点版（44-kuimulang） |
| site/static/images/plate-line-45-zhaoan-topic.webp | W984 | 新增·站点版（45-zhaoan-topic） |
| site/static/images/plate-line-46-fushi-topic.webp | W984 | 新增·站点版（46-fushi-topic） |
| site/static/images/plate-line-47-jingwu-topic.webp | W984 | 新增·站点版（47-jingwu-topic） |
| site/static/images/plate-line-48-xuanzang-topic.webp | W984 | 新增·站点版（48-xuanzang-topic） |
| site/reader/ch007.html | W984 | 接入题图（第 007 回 八卦炉与五行山（替换浓墨版·原图保留）） |
| site/reader/ch014.html | W984 | 接入题图（第 014 回 六贼剪径（替换浓墨版·原图保留）） |
| site/reader/ch015.html | W984 | 接入题图（第 015 回 鹰愁涧意马收缰（替换浓墨版·原图保留）） |
| site/reader/ch023.html | W984 | 接入题图（第 023 回 四圣试禅心（替换浓墨版·原图保留）） |
| site/reader/ch027.html | W984 | 接入题图（第 027 回 白龙归水（替换浓墨版·原图保留）） |
| site/reader/ch030.html | W984 | 接入题图（第 030 回 邪魔侵正法（替换浓墨版·原图保留）） |
| site/reader/people/罗刹女外传.html | W984 | 接入题图（罗刹女） |
| site/reader/people/奎木狼外传.html | W984 | 接入题图（奎木狼） |
| site/reader/themes/招安的两种结局专题.html | W984 | 接入题图（招安的两种结局） |
| site/reader/essays/西游与服饰学.html | W984 | 接入题图（西游与服饰学） |
| site/reader/poetry/原著景物诗分类赏析专题.html | W984 | 接入题图（原著景物诗分类赏析） |
| site/reader/culture/历史玄奘与小说玄奘专题.html | W984 | 接入题图（历史玄奘与小说玄奘） |
| assets/promo/plate-set/plate-line-25~36-*.png/.webp | W984 | 新增 12 张母版（1200×1600·线描墨稿·含 3 张重出生效件） |
| assets/promo/plate-set/raw/round13/ | W984 | 出图原件 12 份（含 #26/#27/#36 三张重出生效件） |
| assets/promo/plate-set/preview-contact-sheet.png/.webp | W984 | 全目录 64 张缩略拼图（刷新） |
| assets/promo/plate-set/README.md | W984 | 口径更新（52→64 张·第六组清单·本批已知取舍） |
| scripts/_w984_make_prompts.py | W984 | 母版复用生成器（249 字符母版逐字复用·四条断言·stem 冲突负样本自证） |
| scripts/_w984_precheck_pages.py | W984 | 落位页先验（存在 + 无题图 + 结构锚点·负样本自证） |
| scripts/_w984_derive.py | W984 | 施工脚本程序化派生器（替换表 + 残留硬编码断言） |
| scripts/_w984_prepare.py | W984 | 成品派生（裁 3:4 → 缩放 → 纸色归一 → 母版/站点版 → 拼图·作用域限 raw/round13） |
| scripts/_w984_download.py | W984 | 出图原件下载（node_id → 短链 → 落盘·按 node_id↔文件名映射） |
| scripts/_w984_insert_plates.py | W984 | 12 页 chapter-plate 接入（幂等） |
| scripts/_w984_retry.py | W984 | 单张重出修正器（行内短锚点替换 + 重建 batch + 断言修正点入 prompt） |
| scripts/_w984_sheet.py | W984 | 本批 12 张核对拼图生成器 |
| scripts/_w984_zoom.py | W984 | 关键部位放大核对图生成器 |
| scripts/_w984_serve.py | W984 | 本地验收静态服务（补 webp/js/css MIME） |
| scripts/_w945_plates_verify.py | W984 | 素材成套判据 J1–J10（自归档恢复为现役·判据逻辑逐字未改） |
| scripts/_w951_check_crop.py | W984 | 站点版裁切验算（自归档恢复为现役·判据逻辑逐字未改） |
| docs/11-方案报告/计划方案/执行前计划-T31-内页题图成套批第五组.md | W984 | 执行前计划件（框架号 T-31） |
| docs/11-方案报告/计划方案/T31-任务计划执行与经验沉淀报告-2026-10-27.md | W984 | 终稿报告件（执行记录/验收/复盘/经验沉淀） |
| docs/11-方案报告/README.md | W984 | §六 计划方案登记（+2 行·件数十 37→39） |
| docs/agent/pitfalls.md | W984 | 坑表 +6 条（64→70·视觉渲染 12→15 / 流程 10→13） |
| docs/10-方法论沉淀/素材批处理与判据自证方法论.md | W984 | 新增 §2.7 判据覆盖面的边界 + 4 条复现案例 |
| docs/00-导读/W批次编号对账表.md | W984 | W984 认领行 + W982 行 git 反填 |
| site/data/search.html | W984 | 搜索索引重建（新文档入索引）+ CSP 哈希同步 |
| site/en/search.html | W984 | 搜索索引重建（新文档入索引）+ CSP 哈希同步 |
| CHANGELOG.md | W984 | W984 段 |
| docs/00-导读/W批次编号对账表.md | W984 | W984 认领行 |
| README.md | W984 | 当前批次版本行 |
| STRUCTURE.md | W984 | 当前批次版本行 |
| docs/00-导读/项目说明.md | W984 | 当前批次版本行 |
| .github/workflows/README.md | W984 | 工作流层版本面推进 W984 |
| site/index.html | W984 | 页脚批次链插入 W984 |
| site/data/cross-time-danmaku.html | W984 | 页脚批次链插入 W984 |
| site/data/tag-cloud.html | W984 | 页脚批次链插入 W984 |
| site/dukou-engine.html | W984 | 页脚批次链插入 W984 |
| AGENTS.md | W984 | 版本脚注条目 + 坑位条数声明 64→70 |
| archive/docs/AGENTS-ARCHIVE.md | W984 | 脚注滚动迁入的最老条目 |
| CITATION.cff | W984 | version 同步为 W984 |
| scripts/output/file-index.md | W984 | W984 段插入 |

## W983 内页题图成套批·第四组（2026-10-27）

| 文件 | W | 说明 |
|---|---|---|
| site/static/images/plate-line-25-rulai.webp | W983 | 新增·站点版（25-rulai） |
| site/static/images/plate-line-26-yudi.webp | W983 | 新增·站点版（26-yudi） |
| site/static/images/plate-line-27-baiyan-mojun.webp | W983 | 新增·站点版（27-baiyan-mojun） |
| site/static/images/plate-line-28-change.webp | W983 | 新增·站点版（28-change） |
| site/static/images/plate-line-29-shenxue-ganyu-topic.webp | W983 | 新增·站点版（29-shenxue-ganyu-topic） |
| site/static/images/plate-line-30-lujing-ditu-topic.webp | W983 | 新增·站点版（30-lujing-ditu-topic） |
| site/static/images/plate-line-31-mima-pan-topic.webp | W983 | 新增·站点版（31-mima-pan-topic） |
| site/static/images/plate-line-32-minsu-taofu-topic.webp | W983 | 新增·站点版（32-minsu-taofu-topic） |
| site/static/images/plate-line-33-yixiang-puxi-topic.webp | W983 | 新增·站点版（33-yixiang-puxi-topic） |
| site/static/images/plate-line-34-keju-zhidu-topic.webp | W983 | 新增·站点版（34-keju-zhidu-topic） |
| site/static/images/plate-line-35-ch010-weizheng.webp | W983 | 新增·站点版（35-ch010-weizheng） |
| site/static/images/plate-line-36-ch004-bimawen.webp | W983 | 新增·站点版（36-ch004-bimawen） |
| site/reader/people/如来.html | W983 | 接入题图（如来（人物）） |
| site/reader/people/玉帝.html | W983 | 接入题图（玉帝（人物）） |
| site/reader/people/百眼魔君.html | W983 | 接入题图（百眼魔君（人物）） |
| site/reader/people/嫦娥外传.html | W983 | 接入题图（嫦娥（人物）） |
| site/reader/themes/神学干预机制专题.html | W983 | 接入题图（神学干预机制（主题）） |
| site/reader/themes/取经路径地理符号学专题.html | W983 | 接入题图（取经路径地理符号学（主题）） |
| site/reader/themes/取经密码学专题.html | W983 | 接入题图（取经密码学（主题）） |
| site/reader/essays/西游与民俗学.html | W983 | 接入题图（西游与民俗学（跨学科）） |
| site/reader/poetry/西游诗词意象谱系专题.html | W983 | 接入题图（西游诗词意象谱系（跨学科）） |
| site/reader/culture/明代科举制度对照专题.html | W983 | 接入题图（明代科举制度对照（跨学科）） |
| site/reader/ch010.html | W983 | 接入题图（第 010 回 魏征斩龙（回目页）） |
| site/reader/ch004.html | W983 | 接入题图（第 004 回 官封弼马（回目页）） |
| assets/promo/plate-set/plate-line-25~36-*.png/.webp | W983 | 新增 12 张母版（1200×1600·线描墨稿·含 3 张重出生效件） |
| assets/promo/plate-set/raw/round12/ | W983 | 出图原件 12 份（含 #26/#27/#36 三张重出生效件） |
| assets/promo/plate-set/preview-contact-sheet.png/.webp | W983 | 全目录 64 张缩略拼图（刷新） |
| assets/promo/plate-set/README.md | W983 | 口径更新（52→64 张·第六组清单·本批已知取舍） |
| scripts/_w983_make_spec.py | W983 | 级联 spec 生成器（文件清单从磁盘实算·不手抄） |
| scripts/_w983_make_prompts.py | W983 | 母版复用生成器（249 字符母版逐字复用·四条断言·stem 冲突负样本自证） |
| scripts/_w983_precheck_pages.py | W983 | 落位页先验（存在 + 无题图 + 结构锚点·负样本自证） |
| scripts/_w983_derive.py | W983 | 施工脚本程序化派生器（替换表 + 残留硬编码断言） |
| scripts/_w983_prepare.py | W983 | 成品派生（裁 3:4 → 缩放 → 纸色归一 → 母版/站点版 → 拼图·作用域限 raw/round12） |
| scripts/_w983_download.py | W983 | 出图原件下载（node_id → 短链 → 落盘·按 node_id↔文件名映射） |
| scripts/_w983_insert_plates.py | W983 | 12 页 chapter-plate 接入（幂等） |
| scripts/_w983_retry.py | W983 | 单张重出修正器（行内短锚点替换 + 重建 batch + 断言修正点入 prompt） |
| scripts/_w983_sheet.py | W983 | 本批 12 张核对拼图生成器 |
| scripts/_w983_zoom.py | W983 | 关键部位放大核对图生成器 |
| scripts/_w983_serve.py | W983 | 本地验收静态服务（补 webp/js/css MIME） |
| scripts/_w945_plates_verify.py | W983 | 素材成套判据 J1–J10（自归档恢复为现役·判据逻辑逐字未改） |
| scripts/_w951_check_crop.py | W983 | 站点版裁切验算（自归档恢复为现役·判据逻辑逐字未改） |
| docs/11-方案报告/计划方案/执行前计划-T30-内页题图成套批第四组.md | W983 | 执行前计划件（框架号 T-30） |
| docs/11-方案报告/计划方案/T30-任务计划执行与经验沉淀报告-2026-10-27.md | W983 | 终稿报告件（执行记录/验收/复盘/经验沉淀） |
| docs/11-方案报告/README.md | W983 | §六 计划方案登记（+2 行·件数十 37→39） |
| docs/agent/pitfalls.md | W983 | 坑表 +6 条（64→70·视觉渲染 12→15 / 流程 10→13） |
| docs/10-方法论沉淀/素材批处理与判据自证方法论.md | W983 | 新增 §2.7 判据覆盖面的边界 + 4 条复现案例 |
| docs/00-导读/W批次编号对账表.md | W983 | W983 认领行 + W982 行 git 反填 |
| site/data/search.html | W983 | 搜索索引重建（新文档入索引）+ CSP 哈希同步 |
| site/en/search.html | W983 | 搜索索引重建（新文档入索引）+ CSP 哈希同步 |
| CHANGELOG.md | W983 | W983 段 |
| docs/00-导读/W批次编号对账表.md | W983 | W983 认领行 |
| README.md | W983 | 当前批次版本行 |
| STRUCTURE.md | W983 | 当前批次版本行 |
| docs/00-导读/项目说明.md | W983 | 当前批次版本行 |
| .github/workflows/README.md | W983 | 工作流层版本面推进 W983 |
| site/index.html | W983 | 页脚批次链插入 W983 |
| site/data/cross-time-danmaku.html | W983 | 页脚批次链插入 W983 |
| site/data/tag-cloud.html | W983 | 页脚批次链插入 W983 |
| site/dukou-engine.html | W983 | 页脚批次链插入 W983 |
| AGENTS.md | W983 | 版本脚注条目 + 坑位条数声明 64→70 |
| archive/docs/AGENTS-ARCHIVE.md | W983 | 脚注滚动迁入的最老条目 |
| CITATION.cff | W983 | version 同步为 W983 |
| scripts/output/file-index.md | W983 | W983 段插入 |

## W982 手搓绕过级联治理批（2026-10-27）

| 文件 | W | 说明 |
|---|---|---|
| scripts/check_doc_size_budget.py | W982 | C7 版本面契约（三层方案②）：三面锚尾/HEAD 句/链条≤3（排除创建于误计）/概要块>6 判红·挂 verify+开工双面
| scripts/preflight_check.py | W982 | ③手搓前置劝导：级联面脏件 NOTE（quotePath=false 二次取数·实弹验证过）
| tests/unit/test_doc_size_budget.py | W982 | C7 单测 2 例（良构零 FAIL/三破坏 FAIL 锁）
| HANDOVER.md | W982 | 候选条目标记 W982 落地（①文件锁缓建裁决）+ 级联头尾链与里程碑块
| docs/00-导读/W批次编号对账表.md | W982 | W982 认领行与收官回填
| CHANGELOG.md | W982 | W982 段
| README.md | W982 | 当前批次版本行
| STRUCTURE.md | W982 | 当前批次版本行
| docs/00-导读/项目说明.md | W982 | 当前批次版本行
| .github/workflows/README.md | W982 | 工作流层版本面推进 W982
| site/index.html | W982 | 页脚批次链插入 W982
| site/data/cross-time-danmaku.html | W982 | 页脚批次链插入 W982
| site/data/tag-cloud.html | W982 | 页脚批次链插入 W982
| site/dukou-engine.html | W982 | 页脚批次链插入 W982
| AGENTS.md | W982 | 版本脚注条目
| archive/docs/AGENTS-ARCHIVE.md | W982 | 脚注滚动迁入的最老条目
| CITATION.cff | W982 | version 同步为 W982
| scripts/output/file-index.md | W982 | W982 段插入
| scripts/output/_w982_spec.json | W982 | 本批级联 spec
| scripts/output/_cascade_files_W982.txt | W982 | 级联落盘清单

## W981 数据链恢复重判批（2026-10-27）

| 文件 | W | 说明 |
|---|---|---|
| scripts/judge_gate.py | W981 | --report 路径随目录分区修正（10-方法论沉淀→11-方案报告/调研与数据复盘·旧路径静默不落盘）
| docs/11-方案报告/调研与数据复盘/读者数据复盘.md | W981 | W806 声明追加订正注（数据链实测恢复·账号 10-01 重启·重判中间态 78）+ 末尾判定记录（judge_gate --report 首次真正落盘）
| docs/00-导读/访问统计方案.md | W981 | W981 恢复注记（API 侧恢复·beacon 链退役裁决不变·守卫维持）
| docs/00-导读/W批次编号对账表.md | W981 | W981 认领行与收官回填
| CHANGELOG.md | W981 | W981 段
| HANDOVER.md | W981 | 零段冻结表述订正 + 级联头尾链与里程碑块
| README.md | W981 | 当前批次版本行
| STRUCTURE.md | W981 | 当前批次版本行
| docs/00-导读/项目说明.md | W981 | 当前批次版本行
| .github/workflows/README.md | W981 | 工作流层版本面推进 W981
| site/index.html | W981 | 页脚批次链插入 W981
| site/data/cross-time-danmaku.html | W981 | 页脚批次链插入 W981
| site/data/tag-cloud.html | W981 | 页脚批次链插入 W981
| site/dukou-engine.html | W981 | 页脚批次链插入 W981
| AGENTS.md | W981 | 版本脚注条目
| archive/docs/AGENTS-ARCHIVE.md | W981 | 脚注滚动迁入的最老条目
| CITATION.cff | W981 | version 同步为 W981
| scripts/output/file-index.md | W981 | W981 段插入
| scripts/output/_w981_spec.json | W981 | 本批级联 spec
| scripts/output/_cascade_files_W981.txt | W981 | 级联落盘清单

## W980 stats 标记同步机器化批（2026-10-27）

| 文件 | W | 说明 |
|---|---|---|
| scripts/stats.py | W980 | P-44-05：sweep_markers() 标记自动跟随（面=check_doc_sync 权威面·CHANGELOG 口径块截断防历史污染·正则与 RE_STATS_MARK 同源含数字键）
| tests/unit/test_stats_sync.py | W980 | 新增单测 4 例（失配更新/相等不动/历史段防污染/扩展面计划方案目录排除回归锁）
| pytest.ini | W980 | pytest_collected 925→929（sweep 自动跟随·非手工）
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W980 | pytest_collected 925→929（sweep 自动跟随）
| scripts/output/stats.json | W980 | 实算刷新（pytest_collected 929）
| scripts/output/stats-changelog.json | W980 | 变更史 W980 条目
| scripts/output/stats-index.md | W980 | 反向索引重渲染
| archive/docs/W批次编号对账表-ARCHIVE.md | W980 | W681 追加订正注（进行中→已闭环·事实收官·追加合规原行未动）
| docs/00-导读/W批次编号对账表.md | W980 | W980 认领行与收官回填
| CHANGELOG.md | W980 | W980 段
| HANDOVER.md | W980 | 级联头尾链与里程碑块
| README.md | W980 | 当前批次版本行
| STRUCTURE.md | W980 | 当前批次版本行
| docs/00-导读/项目说明.md | W980 | 当前批次版本行
| .github/workflows/README.md | W980 | 工作流层版本面推进 W980
| site/index.html | W980 | 页脚批次链插入 W980
| site/data/cross-time-danmaku.html | W980 | 页脚批次链插入 W980
| site/data/tag-cloud.html | W980 | 页脚批次链插入 W980
| site/dukou-engine.html | W980 | 页脚批次链插入 W980
| AGENTS.md | W980 | 版本脚注条目
| archive/docs/AGENTS-ARCHIVE.md | W980 | 脚注滚动迁入的最老条目
| CITATION.cff | W980 | version 同步为 W980
| scripts/output/file-index.md | W980 | W980 段插入
| scripts/output/_w980_spec.json | W980 | 本批级联 spec
| scripts/output/_cascade_files_W980.txt | W980 | 级联落盘清单

## W979 收官提示位扩展批（2026-10-27）

| 文件 | W | 说明 |
|---|---|---|
| scripts/batch_cascade.py | W979 | 收官提示位集合化 _close_hints()：[SIZE] 超窗回窗提示 + [TMPE] TTL 超龄报数 + [SCRIPTS] 顶层下划线件计数（P-44-01/02/03）
| docs/00-导读/W批次编号对账表.md | W979 | W979 认领行与收官回填
| CHANGELOG.md | W979 | W979 段
| HANDOVER.md | W979 | 级联头尾链与里程碑块
| README.md | W979 | 当前批次版本行
| STRUCTURE.md | W979 | 当前批次版本行
| docs/00-导读/项目说明.md | W979 | 当前批次版本行
| .github/workflows/README.md | W979 | 工作流层版本面推进 W979
| site/index.html | W979 | 页脚批次链插入 W979
| site/data/cross-time-danmaku.html | W979 | 页脚批次链插入 W979
| site/data/tag-cloud.html | W979 | 页脚批次链插入 W979
| site/dukou-engine.html | W979 | 页脚批次链插入 W979
| AGENTS.md | W979 | 版本脚注条目
| archive/docs/AGENTS-ARCHIVE.md | W979 | 脚注滚动迁入的最老条目
| CITATION.cff | W979 | version 同步为 W979
| scripts/output/file-index.md | W979 | W979 段插入
| scripts/output/_w979_spec.json | W979 | 本批级联 spec
| scripts/output/_cascade_files_W979.txt | W979 | 级联落盘清单

## W978 第 44 篇工作复盘批（2026-10-27）

| 文件 | W | 说明 |
|---|---|---|
| docs/11-方案报告/工作复盘与优化分析报告/工作复盘与优化分析报告-2026-10-27.md | W978 | 第 44 篇工作复盘（W955-W977 区间·触发清单与周期栏带入）
| scripts/_w978_review_evidence.py | W978 | 复盘取证脚本（全篇数字唯一源头·复算入口）
| scripts/output/_w978_review_evidence.json | W978 | 取证产物（92 提交 / 21 段 / 23 行 / T3）
| docs/11-方案报告/README.md | W978 | §五 登记行 26（第 44 篇）
| docs/00-导读/W批次编号对账表.md | W978 | W978 认领行与收官回填
| CHANGELOG.md | W978 | W978 段
| HANDOVER.md | W978 | 级联头尾链与里程碑块
| README.md | W978 | 当前批次版本行
| STRUCTURE.md | W978 | 当前批次版本行
| docs/00-导读/项目说明.md | W978 | 当前批次版本行
| .github/workflows/README.md | W978 | 工作流层版本面推进 W978
| site/index.html | W978 | 页脚批次链插入 W978
| site/data/cross-time-danmaku.html | W978 | 页脚批次链插入 W978
| site/data/tag-cloud.html | W978 | 页脚批次链插入 W978
| site/dukou-engine.html | W978 | 页脚批次链插入 W978
| AGENTS.md | W978 | 版本脚注条目
| archive/docs/AGENTS-ARCHIVE.md | W978 | 脚注滚动迁入的最老条目
| CITATION.cff | W978 | version 同步为 W978
| scripts/output/file-index.md | W978 | W978 段插入
| scripts/output/_w978_spec.json | W978 | 本批级联 spec
| scripts/output/_cascade_files_W978.txt | W978 | 级联落盘清单

## W977 一次性件批量退役批（2026-10-27）

| 文件 | W | 说明 |
|---|---|---|
| archive/README.md | W977 | 归档台账组行 5 条（misc 60 + w6xx 2 + w7xx 31 + w8xx 42 + w9xx 152 = 287 件）
| scripts/index.md | W977 | 目录文档刷新（顶层 _ 件 454 → 167：286 入档 + 152 S4 本地件 + 15 现役保留）
| scripts/output/index.md | W977 | 目录文档刷新核对（output/ 自有 _w7xx 件与 spec 在位·零僵尸行）
| archive/scripts/batches/README.md | W977 | 目录文档刷新（batches 总览）
| archive/scripts/batches/index.md | W977 | 目录文档刷新（batches 索引）
| archive/scripts/batches/misc/README.md | W977 | 目录文档刷新（misc 组）
| archive/scripts/batches/misc/index.md | W977 | 目录文档刷新（misc 索引）
| archive/scripts/batches/w6xx/README.md | W977 | 目录文档刷新
| archive/scripts/batches/w6xx/index.md | W977 | 目录文档刷新
| archive/scripts/batches/w7xx/README.md | W977 | 目录文档刷新
| archive/scripts/batches/w7xx/index.md | W977 | 目录文档刷新
| archive/scripts/batches/w8xx/README.md | W977 | 目录文档刷新（w8xx 新建组）
| archive/scripts/batches/w8xx/index.md | W977 | 目录文档刷新（w8xx 新建组）
| archive/scripts/batches/w9xx/README.md | W977 | 目录文档刷新（w9xx 本批最大组 +152）
| archive/scripts/batches/w9xx/index.md | W977 | 目录文档刷新
| docs/00-导读/W批次编号对账表.md | W977 | W977 认领行与收官回填
| CHANGELOG.md | W977 | W977 段
| HANDOVER.md | W977 | 级联头尾链与里程碑块
| README.md | W977 | 当前批次版本行
| STRUCTURE.md | W977 | 当前批次版本行
| docs/00-导读/项目说明.md | W977 | 当前批次版本行
| .github/workflows/README.md | W977 | 工作流层版本面推进 W977
| site/index.html | W977 | 页脚批次链插入 W977
| site/data/cross-time-danmaku.html | W977 | 页脚批次链插入 W977
| site/data/tag-cloud.html | W977 | 页脚批次链插入 W977
| site/dukou-engine.html | W977 | 页脚批次链插入 W977
| AGENTS.md | W977 | 版本脚注条目
| archive/docs/AGENTS-ARCHIVE.md | W977 | 脚注滚动迁入的最老条目
| CITATION.cff | W977 | version 同步为 W977
| scripts/output/file-index.md | W977 | W977 段插入
| scripts/output/_w977_spec.json | W977 | 本批级联 spec
| scripts/output/_cascade_files_W977.txt | W977 | 级联落盘清单

## W976 工具链体检修复批（2026-10-27）

| 文件 | W | 说明 |
|---|---|---|
| scripts/archive_ledger_rows.py | W976 | A5 断言修复（归档块保持源相对顺序·不再要求号升序）+ move 参数化 + 自测重写走 move() 全链路（升序/降序穿插/无迁出三形态）
| scripts/check_doc_size_budget.py | W976 | 修法指引按文件种类分治（台账指向 archive_ledger_rows·段式工具不管台账）+ 自测补台账案例
| scripts/preflight_check.py | W976 | rejection_pairs 纯函数 + 主流程拒绝集排除本批自身（认领后复跑不再自撞）
| scripts/batch_cascade.py | W976 | 收官 [TMPE] 提示位（批次桶计数 + 沉淀扫描指引·防只进不出复发）
| tests/unit/test_doc_size_budget.py | W976 | 新增台账修法指引单测（C3 死路指引回归锁）
| tests/unit/test_preflight_touches.py | W976 | 新增 self 排除单测（认领后自撞回归锁）
| docs/agent/pitfalls.md | W976 | 数据/内容可信度 +1 条（自测样本必须覆盖判据会失败的最小形态·8→9 条）
| AGENTS.md | W976 | 坑位数 63→64（阅读契约与主题视图两处·数据类 8→9）+ 版本脚注条目
| HANDOVER.md | W976 | 坑位数指针 63→64 两处 + 级联头尾链与里程碑块
| docs/00-导读/W批次编号对账表.md | W976 | W962 伪阻塞闭环回填 + W976 认领行 + 修剪迁出 W914-W916（61→59 回窗）
| archive/docs/W批次编号对账表-ARCHIVE.md | W976 | 台账修剪迁入 W914-W916 三行（号序切分）
| archive/docs/CHANGELOG-ARCHIVE.md | W976 | 段式归档迁入 W856-W857 两段
| archive/docs/file-index-ARCHIVE.md | W976 | 段式归档迁入 W856-W857 两段
| CHANGELOG.md | W976 | W976 段（现役 111→109 回窗后立新段）
| README.md | W976 | 当前批次版本行
| STRUCTURE.md | W976 | 当前批次版本行
| docs/00-导读/项目说明.md | W976 | 当前批次版本行
| .github/workflows/README.md | W976 | 工作流层版本面推进 W976
| site/index.html | W976 | 页脚批次链插入 W976
| site/data/cross-time-danmaku.html | W976 | 页脚批次链插入 W976
| site/data/tag-cloud.html | W976 | 页脚批次链插入 W976
| site/dukou-engine.html | W976 | 页脚批次链插入 W976
| CITATION.cff | W976 | version 同步为 W976
| scripts/output/file-index.md | W976 | W976 段插入
| scripts/output/_w976_spec.json | W976 | 本批级联 spec
| scripts/output/_cascade_files_W976.txt | W976 | 级联落盘清单
| scripts/output/_vermilion_solid_cache.json | W976 | 朱砂门禁缓存补随批入库（W975 末笔搜索刷新后再生成·上批漏提）

## W975 跨 Agent 经验沉淀入仓批（2026-10-27）

| 文件 | W | 说明 |
|---|---|---|
| docs/agent/pitfalls.md | W975 | 坑表 +6 条（57→63·四节标题条数同步·共享机制条目补 W974 复发注） |
| AGENTS.md | W975 | §4.3 主题视图 + 坑位条数声明 57→63（门禁 N4 口径） |
| HANDOVER.md | W975 | 「三、方法论沉淀」与「雷区权威」两处指针 57→63 |
| docs/10-方法论沉淀/素材批处理与判据自证方法论.md | W975 | 新增深度篇（编号 26·五段结构） |
| docs/10-方法论沉淀/README.md | W975 | 目录索引登记编号 26 |
| scripts/_w975_sink_experience.py | W975 | 入仓同步器（坑表/AGENTS/HANDOVER/深篇登记/台账认领行） |
| scripts/_w975_tweak.py | W975 | 通用「字面替换 + 精确暂存」工具（基底取索引版） |
| scripts/_w975_cascade.py | W975 | 四面登记 + 当前态指针 |
| scripts/output/_cascade_files_W975.txt | W975 | 当批级联清单 |
| CHANGELOG.md | W975 | W975 版段 |
| docs/00-导读/W批次编号对账表.md | W975 | W975 认领行 |

## W974 内页题图成套批·第三组（12 张）（2026-10-27）

| 文件 | W | 说明 |
|---|---|---|
| site/static/images/plate-line-13-jinjiaodawang.webp | W974 | 新增·金角大王（人物） |
| site/static/images/plate-line-14-yinjiaodawang.webp | W974 | 新增·银角大王（人物） |
| site/static/images/plate-line-15-huangmeidawang.webp | W974 | 新增·黄眉大王（人物） |
| site/static/images/plate-line-16-heixiongjing.webp | W974 | 新增·黑熊精（人物） |
| site/static/images/plate-line-17-tuota-lijing.webp | W974 | 新增·托塔李靖（人物） |
| site/static/images/plate-line-18-yutujing.webp | W974 | 新增·玉兔精（人物） |
| site/static/images/plate-line-19-nvziguo-topic.webp | W974 | 新增·女儿国主题（主题） |
| site/static/images/plate-line-20-chelingguo-topic.webp | W974 | 新增·车迟国斗法主题（主题） |
| site/static/images/plate-line-21-shituoling-topic.webp | W974 | 新增·狮驼岭主题（主题） |
| site/static/images/plate-line-22-tonghehe-topic.webp | W974 | 新增·通天河主题（主题） |
| site/static/images/plate-line-23-pansidong-topic.webp | W974 | 新增·盘丝洞主题（主题） |
| site/static/images/plate-line-24-wudidong-topic.webp | W974 | 新增·无底洞主题（主题） |
| site/reader/people/金角银角深化专题.html | W974 | 接入题图（金角大王） |
| site/reader/people/银角大王.html | W974 | 接入题图（银角大王） |
| site/reader/people/黄眉老佛外传.html | W974 | 接入题图（黄眉大王） |
| site/reader/people/黑熊精.html | W974 | 接入题图（黑熊精） |
| site/reader/people/托塔李天王外传.html | W974 | 接入题图（托塔李靖） |
| site/reader/people/玉兔精.html | W974 | 接入题图（玉兔精） |
| site/reader/people/女儿国国王.html | W974 | 接入题图（女儿国主题） |
| site/reader/people/车迟国三国师外传.html | W974 | 接入题图（车迟国斗法主题） |
| site/reader/people/狮驼岭三魔-方向二深化.html | W974 | 接入题图（狮驼岭主题） |
| site/reader/people/老鼋外传.html | W974 | 接入题图（通天河主题） |
| site/reader/people/蜘蛛精.html | W974 | 接入题图（盘丝洞主题） |
| site/reader/people/老鼠精.html | W974 | 接入题图（无底洞主题） |
| assets/promo/plate-set/plate-line-13~24-*.png/.webp | W974 | 新增 12 张母版（1200×1600·线描墨稿） |
| assets/promo/plate-set/raw/round11/ | W974 | 出图原件 12 份（含 15 号两次重出的生效件） |
| assets/promo/plate-set/zoom-w974/ | W974 | 人眼放大复核图（12 张主体区全图 + 12 张局部放大 + 分组拼图） |
| assets/promo/plate-set/README.md | W974 | 口径更新（40→52 张·第五组清单·抗噪口径·已知取舍） |
| scripts/_w974_prepare.py | W974 | 本批专用成品处理（**主体顶抗噪口径**·只处理 raw/round11·不重写既有 40 张） |
| scripts/_w974_make_prompts.py | W974 | 母版复用生成器（读 W953 JSON·三条断言 + 冲突检查负样本自证） |
| scripts/_w974_insert_plates.py | W974 | 12 页 chapter-plate 接入（幂等） |
| scripts/_w974_probe_subjtop.py | W974 | bbox 顶 vs 主体顶 全目录 52 张口径对比探针 |
| scripts/_w974_negative_sample.py | W974 | 多维负样本合成器（J2/J3/J6/J8 四条可证伪） |
| scripts/_w974_stats.py | W974 | 实测汇总（数字唯一源头·README 数字程序化回填） |
| scripts/output/_w974_stats.json | W974 | 实测统计产物 |
| scripts/output/_cascade_files_W974.txt | W974 | 当批级联清单 |
| CHANGELOG.md | W974 | W974 版段 |
| docs/00-导读/W批次编号对账表.md | W974 | W974 认领行 |

## W973 HANDOVER 五区清理批（2026-10-26）

| 文件 | W | 说明 |
|---|---|---|
| HANDOVER.md | W973 | 五区清理：87.2→40.6KB（历史迁档+指针化） |
| archive/docs/HANDOVER-ARCHIVE.md | W973 | 迁入五区历史（零阻塞+候选+方法论+雷区+待办） |
| scripts/check_doc_size_budget.py | W973 | C6 HANDOVER 45KB 硬判据 |

## W972 CodeQL 三高危修复批（2026-10-26）

| 文件 | W | 说明 |
|---|---|---|
| scripts/_w955_motion_audit.py · scripts/check_interaction_binding.py | W972 | 内联脚本块正则宽容空白变体 |
| scripts/check_data_drift.js | W972 | 转义先反斜杠后引号（顺序正确性） |

## W971 存量段状态回填批（2026-10-26）

| 文件 | W | 说明 |
|---|---|---|
| CHANGELOG.md | W971 | 102 段补状态行（99 已收官+1 补号+2 保留） |
| scripts/_w929_stats_sync.py | W971 | 品牌字面量残留清偿（PR #66 品牌检查红项） |

## W970 台账归档行工具批（2026-10-26）

| 文件 | W | 说明 |
|---|---|---|
| scripts/archive_ledger_rows.py | W970 | 新建台账行归档工具（号序切分·守恒五道·C5 修法） |
| docs/00-导读/W批次编号对账表.md | W970 | 首跑回窗 61→59（W908/W909 迁档） |
| archive/docs/W批次编号对账表-ARCHIVE.md | W970 | 迁入 2 行 + 迁入注记 |

## W969 W1000 号位迁移批（2026-10-26）

| 文件 | W | 说明 |
|---|---|---|
| scripts/*.py（22 文件） | W969 | 三位号正则 69 处迁 3-4 位兼容（W1000 错读拆除） |
| tests/unit/test_four_digit_wnum.py | W969 | 四位号解析单测 4 例（防错读负样本） |
| tests/unit/test_release_prep.py | W969 | 四位号设计反转测试（提取交注册表核验） |
| docs/00-导读/W批次编号对账表.md | W969 | D2 豁免登记 W1000 + ASCII 纪律升位注记 |

## W968 台账对账表窗口制拆分批（2026-10-26）

| 文件 | W | 说明 |
|---|---|---|
| docs/00-导读/W批次编号对账表.md | W968 | 窗口制拆分：446.6→150.3KB（留 60 行 W908-W968·ASCII 段迁档注记） |
| archive/docs/W批次编号对账表-ARCHIVE.md | W968 | 新容器：迁入 256 行（W648-W907·号占用留痕合看为准） |
| scripts/check_doc_size_budget.py | W968 | C5 台账 60 行窗硬判据（ledger 计数形态） |
| scripts/check_parser_anchor_coverage.py | W968 | M5 台账探针合看归档（316/316） |

## W967 治理文档数字断言全面对账批（2026-10-26）

| 文件 | W | 说明 |
|---|---|---|
| docs/00-导读/协议边界速查.md | W967 | 六板块字母与篇数纠偏（系统性错位一格）+ S1 残迹订正 |
| docs/00-导读/文档规范.md | W967 | 「全量」段数 45→55（随挂槽演进措辞） |
| docs/agent/gates.md | W967 | 根级脚本数冻结快照改活口径 |
| CLAUDE.md | W967 | 接手导航「通读」矛盾改按需读节 |
| scripts/check_gov_doc_claims.py | W967 | 新建数字断言对账器（五组断言·preflight 提示位接线·报告型） |
| scripts/ledger_backfill.py | W967 | 写路径行尾归一（append 裸 LF 边界病根）+ E741 |

## W966 AGENTS 摘要层纠偏与去冗批（2026-10-26）

| 文件 | W | 说明 |
|---|---|---|
| AGENTS.md | W966 | 摘要层纠偏与去冗（过期数字四处·矛盾消除·条目收敛·26.6→23.9KB） |

## W965 脚注重生成与探针沉淀批（2026-10-26）

| 文件 | W | 说明 |
|---|---|---|
| AGENTS.md | W965 | 留存五条脚注重写（全阿拉伯日期头·无截断残迹·≤300 字） |
| scripts/check_parser_anchor_coverage.py | W965 | 新建解析器锚点覆盖面扫描（七机制·报告型·基线 ② 登记·W964 双虫探针常驻化） |
| scripts/check_doc_size_budget.py | W965 | C4 脚注逐条定形判据（>300 字或头不可解析即红） |
| HANDOVER.md | W965 | 候选清单立「手搓绕过级联治理」议题（三起实证·三层候选方案） |
| tests/unit/test_doc_size_budget.py | W965 | C4 负样本单测 |

## W964 AGENTS 版本脚注治理批（2026-10-26）

| 文件 | W | 说明 |
|---|---|---|
| scripts/batch_cascade.py | W964 | 滚动切分器双日期形态 + precheck agents_note 定形断言 + 里程碑块正则括注放宽 |
| scripts/check_doc_size_budget.py | W960 | 体积门禁 C3：AGENTS 脚注 >4KB 硬判据（W964 加） |
| tests/unit/test_doc_size_budget.py | W964 | 脚注 4KB 负样本回归锁 |
| AGENTS.md | W964 | 版本脚注 85.7→3.3 KB（75 真条目拆分·留 5 定形）·文件 110.1→27.2 KB |
| archive/docs/AGENTS-ARCHIVE.md | W964 | 迁入 70 条（W807-W928·新 fenced 块） |
| HANDOVER.md | W964 | 里程碑窗口 15→5 归一（6 失明块现形）·指针 W956 |

## W963 GSAP 动效差异化推广批（入口层 8 页 + cards 模式）（2026-10-26）

| 文件 | W | 说明 |
|---|---|---|
| site/static/js/motion-gsap.js | W963 | 修改：新增 cards 模式（data-gsap-target 可配置 + stagger 自适应）+ sections 单元收窄为 h2 |
| site/reader/index.html | W963 | 修改：入口层接线（cards 模式·目标 .reader-idx a·增量 229 B） |
| site/reader/themes-hub.html | W963 | 修改：入口层接线（增量 229 B） |
| site/reader/themes/index.html | W963 | 修改：入口层接线（增量 238 B） |
| site/reader/people/index.html | W963 | 修改：入口层接线（增量 238 B） |
| site/reader/essays/index.html | W963 | 修改：入口层接线（增量 238 B） |
| site/reader/culture/index.html | W963 | 修改：入口层接线（增量 238 B） |
| site/reader/poetry/index.html | W963 | 修改：入口层接线（增量 238 B） |
| site/guide.html | W963 | 修改：入口层接线（cards 模式·目标 .path-card·增量 215 B） |
| scripts/_w962_wire_entry.py | W963 | 新增：入口层接线器（字节级·断言命中数·幂等·单页增量上限 250 B） |
| scripts/_w957_motion_probe.py | W963 | 修改：加 --pages 参数（默认清单不变）以便按新接入面实跑 |
| docs/00-导读/W批次编号对账表.md | W963 | 登记：W963 认领行（让号留痕）+ 收官回填 |
| HANDOVER.md | W963 | 同步：一、当前进度增 W963 条目 + 最后更新链前置 + 当前 HEAD |
| CHANGELOG.md | W963 | 新增：W963 版段（四件套） |
| scripts/output/file-index.md | W963 | 登记：W963 段（本段） |

## W961 GSAP 写法机检挂槽批 + F9 假阳性订正批（2026-10-26）

| 文件 | W | 说明 |
|---|---|---|
| scripts/verify_delivery.py | W961 | 修改：挂第 50 门禁「GSAP 写法」（EXPECTED_SECTION_NAMES + _STRICT_GATES 两处·marker 自动派生）+ _SCOPE_CORE 恒跑 |
| scripts/check_gsap_motion.py | W961 | 修改：加汇总行 marker + 显式豁免机制（J3/J4/J7 可豁免·J2 不可豁免·逐条打印） |
| scripts/_w955_motion_audit.py | W961 | 修改：裸 ease 判据加负向前查（修假阳性：原命中数据字段名 `avg_ease` / `most_ease` 与令牌定义） |
| scripts/output/_w955_motion_audit.json | W961 | 刷新：F9 复扫产物（存量裸 ease 49 处 / 25 页·按「禁新增」口径不计欠账） |
| scripts/_w960_pilot_shots.py | W961 | 新增：试点页实跑截图工具（终态截图 + 入场序列分解帧 + 编排单元可见性 JSON） |
| AGENTS.md | W961 | 修改：§4.2 门禁清单补第 50 条「GSAP 动效写法槽」 |
| docs/11-方案报告/计划方案/执行前计划-T28-GSAP动效体系引入批.md | W961 | 修改：订正 4 处「裸 ease 欠账」表述（假阳性作废·存量不计欠账） |
| docs/11-方案报告/计划方案/T28-任务计划执行与经验沉淀报告-2026-10-26.md | W961 | 修改：订正 2 处同款表述 |
| docs/00-导读/W批次编号对账表.md | W961 | 登记：W961 认领行（让号留痕）+ W955 行订正 1 处 |
| README.md · pytest.ini · 系统架构方案 ×2 | W961 | 修改：统计标记同步（gate_count 49→50·pytest_collected 900→902） |
| HANDOVER.md | W961 | 同步：一、当前进度增 W961 条目 + 最后更新链前置 + 当前 HEAD |
| CHANGELOG.md | W961 | 新增：W961 版段（四件套） |
| scripts/output/file-index.md | W961 | 登记：W961 段（本段） |

## W960 治理文档体积归档批（2026-10-26）

| 文件 | W | 说明 |
|---|---|---|
| scripts/check_doc_size_budget.py | W960 | 新建体积窗口门禁（CHANGELOG/file-index 各 110 段窗·超窗 preflight 判红·KB 行数为报告值） |
| scripts/archive_segments.py | W960 | 新建常驻搬段工具（W921 守恒断言沉淀为五道·changelog 插顶与 file-index 尾追双模式） |
| scripts/preflight_check.py | W960 | 体积窗口硬判据接线（超窗拦截开工·故障降级 WARN 禁静默） |
| scripts/batch_cascade.py | W960 | 落盘后体积提示位（每批收官报四文件体积态） |
| docs/00-导读/文档规范.md | W960 | §8 重标：窗口制替代 50KB/500 行旧线（两制打架消除） |
| archive/docs/CHANGELOG-ARCHIVE.md | W960 | 迁入 38 段（W803-W842·插顶） |
| archive/docs/file-index-ARCHIVE.md | W960 | 迁入 140 段（W700-W842·尾追+归档时间链） |
| tests/unit/test_doc_size_budget.py | W960 | 体积门禁单测 4 例（含现网防回退锚） |
| tests/unit/test_archive_segments.py | W960 | 搬段工具单测 4 例（三种段形态解析与负样本） |
| pytest.ini · 系统架构方案v2 | W960 | pytest_collected 标记归一 910（并行竞态三数字拼接修复） |

## W959 T10 V1.1 计数口径订正批（2026-10-26）

| 文件 | W | 说明 |
|---|---|---|
| docs/11-方案报告/计划方案/T10-任务计划执行与经验沉淀报告-2026-10-22.md | W959 | 修改：V1.1 计数口径订正（31 条四态 + 开放项双口径 + §18 口径说明 + 4 处商榷落实·结论未改） |
| scripts/_w959_t10_v11.py | W959 | 新增：V1.1 订正脚本（行号 + 断言片段双重约束·字节级改写保行尾·31 条作业·倒序应用·幂等） |
| docs/11-方案报告/README.md | W959 | 登记：§六 T-10 行版本标注更新为 V1.1（W959 计数口径订正批） |
| docs/00-导读/W批次编号对账表.md | W959 | 登记：W959 认领行（让号留痕）+ 收官回填 |
| HANDOVER.md | W959 | 同步：一、当前进度增 W959 条目 + 最后更新链前置 + 当前 HEAD |
| CHANGELOG.md | W959 | 新增：W959 版段（四件套） |
| scripts/output/file-index.md | W959 | 登记：W959 段（本段） |

## W957 GSAP 动效体系引入批·施工批（公共动效载体 + 试点 5 页三类动效 + 机检）（2026-10-26）

| 文件 | W | 说明 |
|---|---|---|
| site/static/js/motion-gsap.js | W957 | 新增：公共动效载体（RM 双守卫 + fail-open + 三模式 intro/sections/fold + 排除 reveal-in） |
| site/static/js/gsap.min.js | W957 | 新增：GSAP 3.12.5 外链 vendored（72,214 B·不内联） |
| site/static/js/ScrollTrigger.min.js | W957 | 新增：ScrollTrigger 3.12.5 外链 vendored（43,380 B） |
| site/index.html | W957 | 修改：试点接入（data-gsap=intro + 三脚本外链·增量 187 B） |
| site/reader/ch007.html | W957 | 修改：试点接入（data-gsap=sections + 三脚本外链·增量 199 B） |
| site/reader/themes/西游与死亡研究专题.html | W957 | 修改：试点接入（增量 208 B） |
| site/reader/people/黄风怪外传.html | W957 | 修改：试点接入（增量 208 B） |
| site/reader/people/白骨精.html | W957 | 修改：试点接入（增量 208 B） |
| scripts/_w956_pilot_pick.py | W957 | 新增：试点页机选探针（3 条规则 · 527 候选 · 可复算） |
| scripts/_w957_wire_pilot.py | W957 | 新增：试点页接入器（字节级改写保行尾 · 断言命中数 · 幂等） |
| scripts/_w957_motion_probe.py | W957 | 新增：浏览器实跑探针（30 组 · RM 判据 + 环境类分离） |
| scripts/check_gsap_motion.py | W957 | 新增：GSAP 写法机检（8 项判据 + 自测 8/8·独立脚本不改管控件） |
| scripts/_w957_ledger_claim.py | W957 | 新增：台账认领行追加器（只追加不改历史行 / 幂等 / 混行尾 fail-closed） |
| scripts/output/_w956_pilot_pick.json | W957 | 新增：试点机选产物（5 页清单 + 527 候选特征量） |
| scripts/output/_w957_motion_probe.json | W957 | 新增：实跑产物（30 组采集 + 判定 PASS） |
| docs/11-方案报告/计划方案/T28-任务计划执行与经验沉淀报告-2026-10-26.md | W957 | 新增：T-28 施工报告（执行记录 / 12 条 AC 验收 / 8 条经验 E-01~E-08 / 5 条偏差留档） |
| docs/11-方案报告/README.md | W957 | 登记：§六 增 T-28 报告行（序号 34）+ 件数刷新 |
| docs/00-导读/W批次编号对账表.md | W957 | 登记：W957 认领行（让号留痕）+ 收官回填 |
| HANDOVER.md | W957 | 同步：一、当前进度增 W957 条目 + 最后更新链前置 + 当前 HEAD |
| CHANGELOG.md | W957 | 新增：W957 版段（四件套） |
| scripts/output/file-index.md | W957 | 登记：W957 段（本段） |

## W956 登记面治理批（2026-10-26）

| 文件 | W | 说明 |
|---|---|---|
| scripts/preflight_check.py | W956 | 在途判定加 git 条件（登记滞后告警不拒绝·P-43-01）+ 复盘触发器提示位接线 |
| scripts/check_review_trigger.py | W956 | 新建复盘触发器（天数/批次/提交三判据任一触发即提示·preflight 接线·不持台账写面） |
| scripts/ledger_backfill.py | W956 | --from-git 收官状态 git 反填（P-43-01 后半·显式值可覆盖） |
| scripts/batch_cascade.py | W956 | 段状态认领登记 W 号一致性断言（E-28/P-43-05 防线） |
| scripts/backfill_changelog.py | W956 | 归档面合看修复（E-27·原实现 67 归档段误报待补）+ --only 限域 + 同款段状态断言 |
| scripts/check_db_schema.py | W956 | 门禁路径跟上 W934 存储层门面化（P1-P3 db.ts→storage/sqlite.ts·假红修复） |
| scripts/check_emoji_icons.py | W956 | ruff 机械清理（死赋值移除·UP009/I001/F841） |
| scripts/output/_w884_spec.json | W956 | W884 补位 spec（Playwright 全谱审计·按 W863 先例标补位） |
| tests/unit/test_preflight_check.py | W956 | 提交索引与在途二分单测 5 例 |
| tests/unit/test_review_trigger.py | W956 | 复盘触发器单测 9 例（含负样本） |
| tests/unit/test_batch_cascade_status_wnum.py | W956 | 段状态断言单测 4 例（含 E-28 实形态负样本） |
| docs/agent/pitfalls.md | W956 | 复盘经验五条上移（级联 5→8·git 17→18·流程 8→9·总数 52→57） |
| AGENTS.md | W956 | §4.3 坑位计数链追记（总数 52→57） |

## W955 GSAP 动效体系引入批第一子批（前置体检 + 执行前计划）（2026-10-26）

| 文件 | W | 说明 |
|---|---|---|
| docs/11-方案报告/计划方案/执行前计划-T28-GSAP动效体系引入批.md | W955 | 新增：T-28 执行前计划（3 目标 + 12 条 AC + 16 条 ASM + 14 步 ST + 9 指标 + 8 风险 + 9 决策 + 12 项自包含检查） |
| scripts/_w955_motion_audit.py | W955 | 新增：动效体检取证脚本（8 组事实·数字唯一源头·禁词基线复用 check_motion_ban 正则） |
| scripts/output/_w955_motion_audit.json | W955 | 新增：体检基线快照（页面分布 / 动效存量 / RM 覆盖 / 体积预算 / GSAP 体量测算） |
| scripts/_w955_ledger_claim.py | W955 | 新增：台账认领行追加器（只追加不改历史行 / 幂等 / 混行尾 fail-closed） |
| scripts/_w955_version_sync.py | W955 | 新增：版本面同步脚本（9 处替换 + 5 处插入·断言命中数·倒序锚点） |
| docs/00-导读/W批次编号对账表.md | W955 | 登记：W955 认领行（认领即占号·单独提交） |
| docs/11-方案报告/README.md | W955 | 登记：§六 增 T-28 执行前计划行（序号 33）+ 件数刷新 |
| HANDOVER.md | W955 | 同步：一、当前进度增 W955 条目 + 最后更新链前置 W955 |
| CHANGELOG.md | W955 | 新增：W955 版段（四件套） |
| scripts/output/file-index.md | W955 | 登记：W955 段（本段） |
| docs/INDEX.md | W955 | 重建：新增 T-28 执行前计划后重生成（765 篇文档 · 13 板块） |
| site/data/search.html | W955 | 刷新：站内搜索索引（中文）重嵌入（含新计划件条目） |
| site/en/search.html | W955 | 刷新：站内搜索索引（英文）重嵌入 |
| site/**（2 页 meta CSP） | W955 | 重算：搜索页内联脚本变更后的 CSP 哈希同步（2 页 · 861 个内联脚本哈希） |

## W954 第 43 篇工作复盘批（2026-10-26）

| 文件 | W | 说明 |
|---|---|---|
| docs/11-方案报告/工作复盘与优化分析报告/工作复盘与优化分析报告-2026-10-26.md | W954 | 新增：第 43 篇复盘（W795–W953 全区间·149 段 / 154 行 / 354 提交·八条核心发现·E-25~E-31 / FAM-40~42 / WF-08~09 / P-43-01~05） |
| docs/11-方案报告/计划方案/执行前计划-T27-第43篇工作复盘批.md | W954 | 新增：T-27 执行前计划（9 条 AC / 9 步 ST / 7 项 V 指标 / 8 条决策 / 12 项自包含检查） |
| docs/11-方案报告/计划方案/T27-任务计划执行与经验沉淀报告-2026-10-26.md | W954 | 新增：T-27 执行与经验沉淀报告（9 步执行记录 / 验收表 / 6 条偏差 / 6 条经验 E-01~E-06） |
| scripts/_w954_review_evidence.py | W954 | 新增：复盘取证脚本（CHANGELOG 现役面 + 归档面 + 对账表 + git 提交图四源合取 + 五类漂移分类 + 12 组主题分组） |
| scripts/_w954_ledger_backfill.py | W954 | 新增：台账回写脚本（8 行状态订正 + 认领行追加·先断言后写·幂等可重跑） |
| scripts/output/_w954_review_evidence.json | W954 | 新增：取证产物（区间事实与漂移分档的机器可读快照） |
| docs/11-方案报告/README.md | W954 | 登记：§五 增第 43 篇行（序号 25）+ §六 增 T-27 两行（序号 31/32）+ 件数刷新 |
| docs/00-导读/W批次编号对账表.md | W954 | 登记：W954 认领行 + 回写 7 批陈旧在途状态 + W937 标「已停止」并清零 touches |
| HANDOVER.md | W954 | 同步：一、当前进度增 W954 条目 + 最后更新链前置 W954 |
| CHANGELOG.md | W954 | 新增：W954 版段（四件套） |
| scripts/output/file-index.md | W954 | 登记：W954 段（本段） |

