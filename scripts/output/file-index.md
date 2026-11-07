## W1151 v4 type/grid 族消费批（2026-11-07）

| 文件 | W | 说明 |
|---|---|---|
| site/tokens.css | W1151 | 改：type 九定义值序订正「字重 族 字号/行高」→「字重 字号/行高 族」（font shorthand 合法序·IACVT 死令牌根修·四值语义零变化·订正时消费位 0） |
| site/system.css | W1151 | 改：--type-number 等值消费 ×2（.kpi .kpi-value 与 .kpi-card .value/.kpi-value·font: var() + color/variant 补位·四值簇逐字全等） |
| site/dukou-engine.html | W1151 | 改：页内 kpi 影子副本 --type-number 消费 ×2（与 system.css 同位）+ INLINED 副本同步 |
| DESIGN.md | W1151 | 改：§4C 现况表订正（W1144 gap 3 页 12 位补录 + type 首角色启用 + grid 0 裁定）+ 根修与消费记录 + 后续批范围三条 |
| docs/11-方案报告/设计与架构方案/界面视觉重设计细化规格-v4-2026-10-20.md | W1151 | 改：§4 补 W1151 订正行（原稿字面保留存历史·以 tokens.css 现行序为准） |
| docs/00-导读/design.md | W1151 | 改：令牌导出再生成（export_design_tokens·134 键） |
| scripts/output/design-tokens.json | W1151 | 改：令牌导出再生成（反篡改比对源） |
| docs/00-导读/W批次编号对账表.md | W1151 | 改：W1144/W1145/W1149 行 hash+状态回填 + W1148 行补建（8f724d1f·PR #145）+ W1145/W1149 状态格正名 + W1151 认领行 + 腾窗迁出 2 行（W1085-W1088） |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1151 | 改：台账腾窗接收 W1085-W1088 两行 |
| scripts/output/tools-inventory.md | W1151 | 改：工具清单时间戳刷新 |
| CHANGELOG.md | W1151 | 改：W1151 段落（级联） |
| HANDOVER.md | W1151 | 改：最后更新链+里程碑块（级联） |
| AGENTS.md | W1151 | 改：脚注+版本（级联） |
| archive/docs/AGENTS-ARCHIVE.md | W1151 | 改：AGENTS 脚注滚动归档（级联） |
| README.md | W1151 | 改：版本面推进（级联 versions·幂等） |
| STRUCTURE.md | W1151 | 改：版本面推进（级联·幂等） |
| CITATION.cff | W1151 | 改：版本面推进（级联·幂等） |
| docs/00-导读/项目说明.md | W1151 | 改：版本面推进（级联·幂等） |
| .github/workflows/README.md | W1151 | 改：版本抬头推进（级联·幂等） |
| docs/00-导读/统计口径说明.md | W1151 | 改：stats 刷新连带（级联） |
| docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md | W1151 | 改：版本抬头推进（级联 versions·幂等） |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1151 | 改：版本抬头推进（级联·幂等） |
| scripts/output/file-index.md | W1151 | 改：file-index 段（级联） |
| scripts/output/stats.json | W1151 | 改：stats 刷新（级联） |
| scripts/output/stats-index.md | W1151 | 改：stats 索引（级联） |
| scripts/output/stats-changelog.json | W1151 | 改：stats changelog 面（级联） |
| docs/INDEX.md | W1151 | 改：docs_index 刷新（级联 index 步） |
| scripts/INDEX.md | W1151 | 改：gen_folder_docs 刷新（级联） |
| scripts/output/INDEX.md | W1151 | 改：gen_folder_docs 刷新（级联） |
| scripts/output/README.md | W1151 | 改：gen_folder_docs 刷新（级联） |
| scripts/output/_w1151_spec.json | W1151 | 新增：本批 spec |
| scripts/output/_cascade_files_W1151.txt | W1151 | 新增：级联清单（级联） |
| scripts/output/_vermilion_solid_cache.json | W1151 | 改：朱砂实底增量缓存刷新（门禁产物） |
| scripts/output/_vermilion_solid_report.json | W1151 | 改：朱砂实底报告刷新（门禁产物） |
| scripts/batch_closeout.py | W1151 | 改：_add_paths 巨批分块根修（WinError 206·851 页单条 git add 超 CreateProcess 32767 字符上限·W1151 实证炸链） |
| tests/unit/test_w1151_closeout_add_chunk.py | W1151 | 新增：3 例回归锁（巨批 450 件分 3 块 / 小批单块不退化 / 块失败中止 fail-closed） |
| scripts/check_doc_sync.py | W1151 | 改：C4 登记面读两面根修（现役表 ∪ 台账归档表 glob·腾窗与 C4 互搏 W1085 假红实证） |
| tests/unit/test_w1151_c4_archive_table.py | W1151 | 新增：3 例回归锁（归档表行计入注册 / 提交提归档号通过 / 真未登记仍红） |
| docs/agent/gates.md | W1151 | 改：第 31 条补 W1151 台账归档面根修段 |
| scripts/cross_line_baseline.json | W1151 | 改：跨行改写基线刷新（check_doc_sync 编辑致锚点变·存量单行 token 剥离复核无害） |
| site/（2 件） | W1151 | inline_css 副本同步（tokens/system 根修与消费传播·_template.html + dukou-engine·dukou-engine 兼手改主体行） |
| site/data/（89 件） | W1151 | inline_css 副本同步（同上·W1142 分组登记） |
| site/en/（138 件） | W1151 | inline_css 副本同步（同上·W1142 分组登记） |
| site/reader/（622 件） | W1151 | inline_css 副本同步（同上·W1142 分组登记） |

## W1150 全站 UI/UX 修复升级批（2026-11-07）

| 文件 | W | 说明 |
|---|---|---|
| .agent/skills/puti-shouye/（1 件） | W1150 | 改：坑表计数 292 两处同步 |
| .github/workflows/（1 件） | W1150 | 改：级联 workflows README 面（本批） |
| archive/docs/（2 件） | W1150 | 改：级联脚注滚动（历史沿革迁档） |
| docs/00-导读/（2 件） | W1150 | 改：W1150 认领行+W1139 幻影冲突回填+腾窗 61→59 段 |
| docs/agent/（1 件） | W1150 | 改：新增 E-198+流程节计数 161 |
| scripts/（2 件） | W1150 | 改：head 模板+重定向 stub 补 favicon 三行（T5 根修） |
| scripts/output/（8 件） | W1150 | 改：级联反向索引段（本批·目录分组立式） |
| site/（2 件） | W1150 | 改：级联页脚短令牌（本批） |
| site/data/（2 件） | W1150 | 改：级联页脚短令牌（本批） |
| site/reader/（102 件） | W1150 | 改：favicon 三行 head 注入（build_reader 模板根修重生 |
| site/reader/culture/（36 件） | W1150 | 改：favicon 三行 head 注入（build_reader 模板根修重生 |
| site/reader/essays/（45 件） | W1150 | 改：favicon 三行 head 注入（build_reader 模板根修重生 |
| site/reader/people/（216 件） | W1150 | 改：favicon 三行 head 注入（build_reader 模板根修重生 |
| site/reader/poetry/（14 件） | W1150 | 改：favicon 三行 head 注入（build_reader 模板根修重生 |
| site/reader/themes/（210 件） | W1150 | 改：favicon 三行 head 注入（build_reader 模板根修重生 |
| xiyouji-agent-web/src/（2 件） | W1150 | 改：通配路由+会话不存在提示卡+加载态消费+重试按钮 loading（T2/T3 |
| xiyouji-agent-web/src/components/（10 件） | W1150 | 改：映射键改引擎真名+run_command 危险标记+token 化（T1/T |
| xiyouji-agent-web/src/components/toolCalls/（5 件） | W1150 | 改：引擎工具名归一根修+色板 token 化（T1/T4） |
| xiyouji-agent-web/src/hooks/（4 件） | W1150 | 改：权限回执失败保留卡片+截断提示+草稿持久化+init 导航（T2/T3） |
| xiyouji-agent-web/src/pages/（1 件） | W1150 | 改：messagesLoading 防闪现+cwd 默认去硬编码（T3） |
| CHANGELOG.md | W1150 | 改：级联现役段（本批） |
| HANDOVER.md | W1150 | 改：级联现役段（本批） |
| README.md | W1150 | 改：级联批头版本行（本批） |
| STRUCTURE.md | W1150 | 改：级联批头版本行（本批） |
| AGENTS.md | W1150 | 改：级联脚注滚动+坑表计数 292+主题分项 161 |
| CITATION.cff | W1150 | 改：级联版本面（本批） |

## W1149 reader/dataset 审计修复批（2026-11-06）

| 文件 | W | 说明 |
|---|---|---|
| scripts/build_reader.py | W1149 | 改：BLOB 路径映射（docs/ vs 仓库根）+ 多 h1 降级 + themes 跳转 canonical + 根目录 h1 + 生成后自动内联 reader CSS |
| scripts/inline_css.py | W1149 | 改：新增 `--reader` 与 `inline_dir()`（reader 单文件自包含恢复） |
| scripts/check_inlined_css.py | W1149 | 改：扫描面扩 `site/reader/**/*.html` + 跳转桩豁免 |
| scripts/check_reader_integrity.py | W1149 | 新增：第 62 槽（占位/GitHub 链接/单 h1/标题唯一） |
| scripts/check_dataset_manifest.py | W1149 | 新增：第 63 槽（README/量纲/端点/哨兵/空值/废弃） |
| scripts/check_dataset_provenance.py | W1149 | 改：第 61 槽扩展 quote_status |
| scripts/gen_dataset_index.py | W1149 | 新增：从磁盘生成 dataset/README 索引 |
| scripts/audit_repo.py | W1149 | 新增：全仓审计四子命令（只读） |
| scripts/verify_delivery.py | W1149 | 改：新增第 62/63 槽 + `_SCOPE_CORE` |
| tests/unit/test_w1149_reader_dataset.py | W1149 | 新增：9 例回归锁 |
| docs/01-全书逐回解读 … docs/06-个人随笔 | W1149 | 改：207 文件删除「双索引链接…（待补）」块；3 篇同题标题加区分（逐文件清单见 git diff） |
| site/reader/**/*.html | W1149 | 改：重生成 623 页（补齐《西游记大事年表》；199 条 GitHub 链接修复；33 页多 h1 归零） |
| site/data/monster-female-network.html · site/data/monster-hierarchy-network.html · site/data/underworld-power-network.html | W1149 | 改：chapter=0→null+scope + tooltip null 守卫（EN 三页同步） |
| site/data/search.html · site/en/search.html | W1149 | 改：搜索索引刷新 + CSP 重算 |
| site/sitemap.xml | W1149 | 改：新增 reader 页收录（854→855 URL） |
| dataset/*.json（19 件） | W1149 | 改：chapter null / weight_scale / sankey schema / 空值状态 / quote_status / 13d 废弃 |
| dataset/README.md · dataset/CODING.md | W1149 | 改：README 改磁盘生成；CODING §2.4 schema 约定 + §9 校验说明 |
| AGENTS.md · docs/agent/gates.md · HANDOVER.md · CHANGELOG.md | W1149 | 改：第 62/63 槽摘要/全量定义/进度/版段 |
| docs/10-方法论沉淀/全仓深度审计SOP-可复用.md | W1149 | 新增：五维矩阵 + 七步流程 + 四类根因 + 准入三件套 |
| .agent/skills/huoyan-jinjing/SKILL.md | W1149 | 新增：悟空火眼金睛·全仓巡检速查 skill |
| docs/11-方案报告/审查与评审/全仓逐逻辑深度审计报告-2026-11-06.md · 基础设施口径与门禁全量审计报告-2026-11-06.md · docs/11-方案报告/设计与架构方案/数据分层与reader-dataset修复方案-2026-11-06.md | W1149 | 新增：审计报告与修复方案入库 |
| docs/11-方案报告/README.md · docs/10-方法论沉淀/README.md · docs/INDEX.md | W1149 | 改：登记与索引刷新 |
| scripts/archive_ledger_rows.py | W1149 | 改：在途行保留集（防最老在途行被迁走） |
| scripts/cross_line_baseline.json | W1149 | 改：补 1 条人工复核安全候选（URL host strip） |
| docs/00-导读/W批次编号对账表.md · archive/docs/W批次编号对账表-ARCHIVE.md | W1149 | 改：认领行 W1149 + 迁出 W1086（窗口 61→60） |
| scripts/output/stats.json · stats-index.md · stats-changelog.json · file-index.md | W1149 | 改：计数链刷新 |

## W1148 懒读治理批（2026-11-06）

| 文件 | W | 说明 |
|---|---|---|
| scripts/check_doc_size_budget.py | W1148 | 改：_agents_budget AGENTS 正本双预算判据（C9·正本 ≤48KB + 铁律 ≤30 条§6 段内计数·a 方案） |
| scripts/agent_start.py | W1148 | 改：--task 增最小铁律集注入（b 方案·恒真 7 条 ∪ touches 路径敏感·抽整条原文带回指锚·单条 400 字截断） |
| tests/unit/test_w1142_volume_remedies.py | W1148 | 改：TestAgentsBudget 5 例（现树绿/条数超限红/§6 外不计/字节超限红/尾句剥离） |
| scripts/output/_w1148_spec.json | W1148 | 新增：本批 spec |
| docs/00-导读/W批次编号对账表.md | W1148 | 改：W1148 认领行登记 |
| CHANGELOG.md | W1148 | 改：W1148 段落（级联） |
| HANDOVER.md | W1148 | 改：最后更新链+里程碑（级联） |
| scripts/output/file-index.md | W1148 | 改：file-index 段（级联） |
| AGENTS.md | W1148 | 改：脚注+版本（级联） |
| site/dukou-engine.html | W1148 | 改：页脚短令牌（级联） |
| site/data/cross-time-danmaku.html | W1148 | 改：页脚短令牌（级联） |
| site/data/tag-cloud.html | W1148 | 改：页脚短令牌（级联） |
| scripts/output/stats.json | W1148 | 改：stats 刷新（级联） |
| scripts/output/stats-index.md | W1148 | 改：stats 索引（级联） |
| scripts/output/stats-changelog.json | W1148 | 改：stats 面（级联） |
| README.md | W1148 | 改：版本面（级联·幂等） |
| STRUCTURE.md | W1148 | 改：版本面（级联·幂等） |
| CITATION.cff | W1148 | 改：版本面（级联·幂等） |
| docs/00-导读/项目说明.md | W1148 | 改：版本面（级联·幂等） |
| .github/workflows/README.md | W1148 | 改：版本抬头（级联·幂等） |
| docs/INDEX.md | W1148 | 改：docs_index（级联） |
| scripts/output/_cascade_files_W1148.txt | W1148 | 新增：级联清单 |
| archive/docs/AGENTS-ARCHIVE.md | W1148 | 改：AGENTS 脚注滚动归档（级联） |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1148 | 改：台账腾窗归档（级联） |
| docs/10-方法论沉淀/README.md | W1148 | 改：两篇沉淀登记 |
| scripts/containment_block_scan.py | W1148 | 新增：包含块退化静态扫描固化（W1146 探针移出 tmpe·用户令） |
| scripts/fixed_ancestor_probe.py | W1148 | 新增：offsetParent 运行时探针固化（W1146 机检范式·用户令移出 tmpe） |
| scripts/output/_w1139_spec.json | W1148 | 改：恢复全量逐行 867 行（职责分工定形执行件·W1139 台账注记配套） |
| scripts/output/tools-inventory.md | W1148 | 改：gen_folder_docs --refresh 产物（184 件） |


## W1147 方法论沉淀固化批（2026-11-06）

| 文件 | W | 说明 |
|---|---|---|
| scripts/containment_block_scan.py | W1147 | 新增：包含块退化族静态扫描（临时桶固化正名） |
| scripts/fixed_ancestor_probe.py | W1147 | 新增：运行时 offsetParent 退化探针（375/745/1440 参数化·临时桶固化） |
| scripts/interaction_state_probe.py | W1147 | 新增：12 类开合组件交互后态探针（清单驱动·W1147 待办①） |
| scripts/interaction_components.py | W1147 | 新增：开合组件清单单一事实源（12 类×五元组） |
| docs/10-方法论沉淀/CSS包含块退化与交互后态机检范式.md | W1147 | 新增：沉淀第 29 号 |
| docs/10-方法论沉淀/幂等守卫与判定口径三类自相矛盾根修.md | W1147 | 新增：沉淀第 30 号 |
| docs/10-方法论沉淀/README.md | W1147 | 改：登记第 29/30 号（第 28 行后插入） |
| tests/unit/test_w1147_probes.py | W1147 | 新增：探针引用锁 6 例（第 42 槽 C1 引用面） |
| tests/unit/test_w1142_volume_remedies.py | W1147 | 改：745 溢出断言入抽屉锁（待办②常态化） |
| scripts/output/_w1147_spec.json | W1147 | 新增：本批 spec |
| scripts/output/_cascade_files_W1147.txt | W1147 | 新增：级联清单（级联） |
| CHANGELOG.md | W1147 | 改：W1147 段落（级联） |
| HANDOVER.md | W1147 | 改：最后更新链+里程碑块（级联） |
| scripts/output/file-index.md | W1147 | 改：file-index 段（级联） |
| AGENTS.md | W1147 | 改：脚注+版本（级联） |
| site/dukou-engine.html | W1147 | 改：页脚短令牌推进（级联） |
| site/data/cross-time-danmaku.html | W1147 | 改：页脚短令牌推进（级联） |
| site/data/tag-cloud.html | W1147 | 改：页脚短令牌推进（级联） |
| site/index.html | W1147 | 改：页脚短令牌推进（级联） |
| scripts/output/stats.json | W1147 | 改：stats 刷新（级联） |
| scripts/output/stats-index.md | W1147 | 改：stats 索引（级联） |
| scripts/output/stats-changelog.json | W1147 | 改：stats changelog 面（级联） |
| scripts/output/INDEX.md | W1147 | 改：gen_folder_docs 刷新（级联） |
| scripts/output/README.md | W1147 | 改：gen_folder_docs 刷新（级联） |
| scripts/output/tools-inventory.md | W1147 | 改：工具清单刷新（级联） |
| README.md | W1147 | 改：版本面推进（级联·幂等） |
| STRUCTURE.md | W1147 | 改：版本面推进（级联·幂等） |
| CITATION.cff | W1147 | 改：版本面推进（级联·幂等） |
| docs/00-导读/项目说明.md | W1147 | 改：版本面推进（级联·幂等） |
| .github/workflows/README.md | W1147 | 改：版本抬头推进（级联·幂等） |
| docs/INDEX.md | W1147 | 改：docs_index 刷新（级联 index 步） |
| docs/00-导读/W批次编号对账表.md | W1147 | 改：W1147 认领行登记 |
| archive/docs/AGENTS-ARCHIVE.md | W1147 | 改：AGENTS 脚注滚动归档（级联） |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1147 | 改：台账腾窗归档（级联） |
| docs/11-方案报告/README.md | W1147 | 改：登记第 105/106 号（两篇沉淀） |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1147 | 改：版本抬头推进（级联·幂等） |
| pytest.ini | W1147 | 改：pytest 标记跟随（stats C5b 面·W1143 同族） |
| scripts/INDEX.md | W1147 | 改：gen_folder_docs 刷新（级联） |
| scripts/archive_ledger_rows.py | W1147 | 改：腾窗迁出集合排除在途行（A4 死锁解·_status_of 帮手与 A4 同源判定） |
| tests/unit/INDEX.md | W1147 | 改：gen_folder_docs 刷新（级联） |
| tests/unit/README.md | W1147 | 改：gen_folder_docs 刷新（级联） |
| scripts/output/_w1144_spec.json | W1144 | 新增：本批 spec |
| scripts/output/_w1139_spec.json | W1144 | 改：五批集成载体增补（W1138/1139/1141/1142/1143 并集 933 行·multi-batch 归属载体） |
| scripts/agent_start.py | W1144 | 集成载体登记：改：现势快照连带的 agent_start 面（多批共有·W1147 集成载体登记） |
| scripts/check_doc_size_budget.py | W1144 | 集成载体登记：改：_agents_face 切片根修+密度判据（W1144 主体·W1145 连带暂存） |
| site/data/wukong-tangseng-benchmark.html | W1147 | 同步：W1143 兄弟批标杆页 EMBEDDED 索引随本批搜索索引刷新连带（集成载体登记） |
| site/en/search.html | W1147 | 同步：EN 内嵌索引刷新连带（集成载体登记） |
| site/data/character-relationship-3d.html | W1147 | 同步：W1141 兄弟批 3D 页 EMBEDDED 索引连带（集成载体登记） |
| site/data/search.html | W1147 | 同步：内嵌索引刷新连带（第 46 槽·集成载体登记） |
| docs/11-方案报告/审查与评审/包含块退化族举一反三扫描报告-2026-11-06.md | W1147 | 新增：举一反三扫描报告（56 组页面×视口 0 退化 0 溢出·机检范式固化来源） |
| scripts/output/_vermilion_solid_cache.json | W1147 | 改：朱砂实底增量缓存刷新（门禁产物·多批共有） |
| site/data/character-relationship-3d-view.html | W1147 | 同步：W1141 兄弟批 3D-view 页 EMBEDDED 索引连带（集成载体登记） |
| scripts/output/_w1148_spec.json | W1148 | 新增：懒读治理批 spec（前置代合并随 W1147 入库·兄弟会话同树） |
| scripts/output/_cascade_files_W1148.txt | W1148 | 新增：级联清单（前置代合并随 W1147 入库） |
| docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md | W1147 | 改：版本抬头推进（级联 versions·幂等） |


## W1145 引文精确性槽批（2026-11-06）

| 文件 | W | 说明 |
|---|---|---|
| scripts/check_dataset_provenance.py | W1145 | 改：新增引文精确性判据（text-search 原文精确子串） |
| tests/unit/test_w1145_quote_exactness.py | W1145 | 新增：引文精确性三例回归锁 |
| dataset/CODING.md | W1145 | 改：§9 校验说明补引文精确性 |
| dataset/README.md | W1145 | 改：校验说明补引文精确性 |
| dataset/INDEX.md | W1145 | 改：目录索引刷新（级联） |
| docs/agent/gates.md | W1145 | 改：第 61 条补引文精确性与 9 例自测 |
| AGENTS.md | W1145 | 改：第 61 槽摘要补引文精确性 + 脚注（级联） |
| docs/00-导读/W批次编号对账表.md | W1145 | 改：新增认领行 |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1145 | 改：台账窗口归档（级联） |
| archive/docs/AGENTS-ARCHIVE.md | W1145 | 改：脚注滚动归档（级联） |
| CHANGELOG.md | W1145 | 改：新增 W1145 段（级联） |
| HANDOVER.md | W1145 | 改：当前进度/头链/里程碑（级联） |
| README.md | W1145 | 改：版本面推进（级联 versions·幂等） |
| STRUCTURE.md | W1145 | 改：版本面推进（级联·幂等） |
| docs/00-导读/项目说明.md | W1145 | 改：版本面推进（级联·幂等） |
| CITATION.cff | W1145 | 改：版本面推进（级联·幂等） |
| .github/workflows/README.md | W1145 | 改：版本抬头推进（级联·幂等） |
| docs/INDEX.md | W1145 | 改：docs_index 刷新（级联 index 步） |
| docs/00-导读/统计口径说明.md | W1145 | 改：stats 刷新连带（级联） |
| docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md | W1145 | 改：版本抬头推进（级联·幂等） |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1145 | 改：版本抬头推进（级联·幂等） |
| scripts/output/file-index.md | W1145 | 改：本批条目（级联） |
| scripts/output/stats.json | W1145 | 改：stats 刷新（级联） |
| scripts/output/stats-index.md | W1145 | 改：stats 索引（级联） |
| scripts/output/stats-changelog.json | W1145 | 改：stats changelog 面（级联） |
| scripts/output/tools-inventory.md | W1145 | 改：工具清单刷新（级联） |
| scripts/output/INDEX.md | W1145 | 改：gen_folder_docs 刷新（级联） |
| scripts/output/README.md | W1145 | 改：gen_folder_docs 刷新（级联） |
| scripts/output/_vermilion_solid_cache.json | W1145 | 改：朱砂实底增量缓存刷新（门禁产物） |
| scripts/output/_vermilion_solid_report.json | W1145 | 改：朱砂实底报告刷新（门禁产物） |
| tests/unit/INDEX.md | W1145 | 改：目录索引收录新测试（级联） |
| tests/unit/README.md | W1145 | 改：测试计数刷新（级联） |
| pytest.ini | W1145 | 改：pytest collected 统计标记（级联） |
| scripts/output/_w1145_spec.json | W1145 | 新增：本批 spec |
| scripts/output/_cascade_files_W1145.txt | W1145 | 新增：级联清单（级联） |

## W1144 v4 语义令牌第一批（2026-11-06）

| 文件 | W | 说明 |
|---|---|---|
| site/index.html | W1144 | 改：gap: var(--space-3/5/6/7) → var(--gap-tight/base/loose/block) 4 位（语义角色族第一批·别名等值·J2 零差异） |
| site/guide.html | W1144 | 改：gap 族等值替换 2 位（同上） |
| site/dashboard.html | W1144 | 改：gap 族等值替换 6 位（同上） |
| docs/00-导读/W批次编号对账表.md | W1144 | 改：W1138/W1139/W1141/W1142 四行 hash 与状态回填（PR #143·96dfb12b） |
| scripts/output/_w1144_spec.json | W1144 | 新增：本批 spec |
| scripts/output/_cascade_files_W1144.txt | W1144 | 新增：级联清单（级联） |
| CHANGELOG.md | W1144 | 改：W1144 段落（级联） |
| HANDOVER.md | W1144 | 改：最后更新链+里程碑块（级联） |
| scripts/output/file-index.md | W1144 | 改：file-index 段（级联） |
| AGENTS.md | W1144 | 改：脚注+版本（级联） |
| site/dukou-engine.html | W1144 | 改：页脚短令牌推进（级联） |
| site/data/cross-time-danmaku.html | W1144 | 改：页脚短令牌推进（级联） |
| site/data/tag-cloud.html | W1144 | 改：页脚短令牌推进（级联） |
| scripts/output/stats.json | W1144 | 改：stats 刷新（级联） |
| scripts/output/stats-index.md | W1144 | 改：stats 索引（级联） |
| scripts/output/stats-changelog.json | W1144 | 改：stats changelog 面（级联） |
| scripts/output/INDEX.md | W1144 | 改：gen_folder_docs 刷新（级联） |
| scripts/output/README.md | W1144 | 改：gen_folder_docs 刷新（级联） |
| README.md | W1144 | 改：版本面推进（级联 versions·幂等） |
| STRUCTURE.md | W1144 | 改：版本面推进（级联·幂等） |
| CITATION.cff | W1144 | 改：版本面推进（级联·幂等） |
| docs/00-导读/项目说明.md | W1144 | 改：版本面推进（级联·幂等） |
| .github/workflows/README.md | W1144 | 改：版本抬头推进（级联·幂等） |
| docs/INDEX.md | W1144 | 改：docs_index 刷新（级联 index 步） |
| scripts/batch_cascade.py | W1144 | 改：rotate 三重根修（幂等守卫超限放行补滚 / 淘汰目标严格口径 min 块自愈指针 / _remain 与 W534 两处潜伏炸点修复·P1-1 复发真根因闭环） |

## W1143 唐僧—孙悟空标杆页批（2026-11-06）

| 文件 | W | 说明 |
|---|---|---|
| dataset/edge-wukong-tangseng.json | W1143 | 新增：9 组事件单边档案（引文/权重/争议） |
| dataset/README.md | W1143 | 改：数据索引与标杆档案说明 |
| dataset/character-relationship-3d.json | W1143 | 改：唐僧→悟空边补 28-31/56 回 |
| dataset/CODING.md | W1143 | 改：第 61 槽扩展说明 |
| dataset/INDEX.md | W1143 | 改：目录索引收录标杆 JSON |
| site/data/wukong-tangseng-benchmark.html | W1143 | 新增：单边档案标杆页 |
| site/about.html | W1143 | 改：七页主线 + 第 07 项 |
| site/data/character-relationship-3d.html | W1143 | 改：逐边档案链接 + EMBEDDED 回目同步 |
| site/data/tag-cloud.html | W1143 | 改：标签云收录标杆页 |
| site/data/search.html | W1143 | 改：搜索索引重建 |
| site/en/search.html | W1143 | 改：英文搜索索引重建 |
| site/sitemap.xml | W1143 | 改：收录标杆页 |
| site/data/INDEX.md | W1143 | 改：数据页目录收录 |
| site/data/README.md | W1143 | 改：数据页计数刷新 |
| site/INDEX.md | W1143 | 改：站点目录收录 |
| site/README.md | W1143 | 改：站点计数刷新 |
| site/index.html | W1143 | 改：页脚 W 令牌推进 |
| site/data/cross-time-danmaku.html | W1143 | 改：页脚 W 令牌推进 |
| site/dukou-engine.html | W1143 | 改：页脚 W 令牌推进 |
| scripts/check_dataset_provenance.py | W1143 | 改：第 61 槽扩展校验标杆档案 |
| tests/unit/test_w1143_benchmark.py | W1143 | 新增：标杆档案四例回归锁 |
| tests/unit/test_w1138_dataset_provenance.py | W1143 | 改：双数据集自测与页面同步 |
| tests/unit/INDEX.md | W1143 | 改：目录索引收录新测试 |
| tests/unit/README.md | W1143 | 改：测试计数刷新 |
| AGENTS.md | W1143 | 改：第 61 槽摘要补标杆数据 |
| docs/agent/gates.md | W1143 | 改：第 61 条补标杆数据判据 |
| docs/00-导读/W批次编号对账表.md | W1143 | 改：新增认领行 |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1143 | 改：台账窗口归档 |
| archive/docs/AGENTS-ARCHIVE.md | W1143 | 改：脚注滚动归档 |
| CHANGELOG.md | W1143 | 改：新增 W1143 段 |
| HANDOVER.md | W1143 | 改：当前进度/头链/里程碑 |
| README.md | W1143 | 改：版本行同步 |
| STRUCTURE.md | W1143 | 改：版本行同步 |
| docs/00-导读/项目说明.md | W1143 | 改：版本行同步 |
| CITATION.cff | W1143 | 改：版本面同步 |
| .github/workflows/README.md | W1143 | 改：版本面同步 |
| scripts/output/file-index.md | W1143 | 改：本批条目 |
| scripts/output/stats.json | W1143 | 改：7 键统计刷新 |
| scripts/output/stats-changelog.json | W1143 | 改：变更史追加 |
| scripts/output/stats-index.md | W1143 | 改：反向索引重渲染 |
| scripts/output/_w1143_spec.json | W1143 | 新增：本批 spec |
| scripts/output/_cascade_files_W1143.txt | W1143 | 新增：级联文件清单 |
| scripts/output/tools-inventory.md | W1143 | 改：工具清单刷新 |
| scripts/output/INDEX.md | W1143 | 改：目录索引刷新 |
| scripts/output/README.md | W1143 | 改：目录计数刷新 |
| pytest.ini | W1143 | 改：pytest collected 统计标记 |

## W1142 治理维护批（2026-11-06）

| 文件 | W | 说明 |
|---|---|---|
| scripts/batch_spec.py | W1142 | 改：fi_group_rows 分组原语 + FI_SEGMENT_GROUP_THRESHOLD=200（体积根修①·登记面/应动全集职责分工定形） |
| scripts/backfill_changelog.py | W1142 | 改：file_index_block 写入侧自动分组（行数超阈值→目录分组行·单一原语） |
| scripts/batch_cascade.py | W1142 | 改：_face_file_index 写入侧自动分组（与 backfill 同口径） |
| scripts/archive_segments.py | W1142 | 改：体积模式迁出后剩余段 ≥20 断言（体积根修③·铁律 22 保留条款机器化·不足指引压缩而非归档） |
| scripts/check_doc_size_budget.py | W1142 | 改：_fileindex_row_density 段行密度判据 cap 200（体积根修④·拦绕过写入侧的段） |
| scripts/batch_closeout.py | W1142 | 改：collect_paths 分组行展开兜底（体积根修②·防分组态 add 静默跳过） |
| scripts/output/file-index.md | W1142 | 改：W1137/W1134/W1139 三巨段按新立式分组重写（246KB→107KB·存量清偿） |
| scripts/output/_w1139_spec.json | W1142 | 改：恢复全量逐行（职责分工定形配套·8 special+858 页+4 判据脚本行） |
| HANDOVER.md | W1142 | 改：Backlog 对账（T6·W1095 条目实证移出 + W1142 对账注记·触发器 84 批）+ 最后更新链（级联） |
| docs/11-方案报告/审查与评审/对抗审查报告-2026-11-06.md | W1142 | 新增：对抗审查派发回报（T5·W1072 以来 69 批变更面·七项清单） |
| docs/11-方案报告/设计与架构方案/界面交互迭代施工方案-W1137-2026-11-05.md | W1142 | 改：§2 欠账路线体积矛盾行改注已根修（四层） |
| scripts/output/_w1142_spec.json | W1142 | 新增：本批 spec |
| docs/00-导读/W批次编号对账表.md | W1142 | 改：W1142 认领行登记（含「对抗审查已派发」token） |
| tests/unit/test_w1142_volume_remedies.py | W1142 | 新增：体积根修回归锁 11 例（对抗审查 P2-1·铁律 18-②） |
| AGENTS.md | W1142 | 改：铁律 22 就地并入超窗处置优先序（①压缩②搬段③拆批·对抗审查 E 项采纳） |

## W1141 数据集溯源门禁挂载批（2026-11-06）

| 文件 | W | 说明 |
|---|---|---|
| scripts/check_dataset_provenance.py | W1141 | 改：门禁化输出（固定汇总行 + 0/1/2 退出码） |
| scripts/verify_delivery.py | W1141 | 改：新增第 61 槽 数据集溯源 + _SCOPE_CORE 恒跑 |
| docs/agent/gates.md | W1141 | 改：补第 61 条完整定义 |
| AGENTS.md | W1141 | 改：§4.2 补第 61 槽摘要 + 陈旧「57 槽」订正为「61 槽」 |
| docs/00-导读/文档规范.md | W1141 | 改：verify full 段数 65 → 66 |
| tests/unit/test_w1141_gate_mount.py | W1141 | 新增：门禁挂载回归锁三例 |
| tests/unit/INDEX.md | W1141 | 改：目录索引收录新测试 |
| tests/unit/README.md | W1141 | 改：测试计数刷新 |
| dataset/README.md | W1141 | 改：校验入口改为第 61 门禁 |
| dataset/CODING.md | W1141 | 改：校验说明改为第 61 门禁同源 |
| pytest.ini | W1141 | 改：pytest collected 统计标记刷新 |
| CHANGELOG.md | W1141 | 改：新增 W1141 段 |
| HANDOVER.md | W1141 | 改：当前进度/头链/里程碑块 |
| README.md | W1141 | 改：版本行同步 |
| STRUCTURE.md | W1141 | 改：版本行同步 |
| docs/00-导读/项目说明.md | W1141 | 改：版本行同步 |
| CITATION.cff | W1141 | 改：版本面同步 |
| .github/workflows/README.md | W1141 | 改：版本面同步 |
| scripts/output/file-index.md | W1141 | 改：本批条目 |
| scripts/output/stats.json | W1141 | 改：gate_count 61 与 pytest_collected 刷新 |
| scripts/output/stats-changelog.json | W1141 | 改：变更史追加 |
| scripts/output/stats-index.md | W1141 | 改：反向索引重渲染 |
| scripts/output/_w1141_spec.json | W1141 | 新增：本批 spec |
| scripts/output/_cascade_files_W1141.txt | W1141 | 新增：级联文件清单 |
| archive/docs/AGENTS-ARCHIVE.md | W1141 | 改：脚注滚动归档 |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1141 | 改：台账行窗口归档 |
| site/index.html | W1141 | 改：页脚 W 令牌推进 |
| site/data/cross-time-danmaku.html | W1141 | 改：页脚 W 令牌推进 |
| site/data/tag-cloud.html | W1141 | 改：页脚 W 令牌推进 |
| site/dukou-engine.html | W1141 | 改：页脚 W 令牌推进 |
| docs/00-导读/W批次编号对账表.md | W1141 | 改：新增认领行 |

## W1139 R-02 模板层去工程化批（2026-11-06）

| 文件 | W | 说明 |
|---|---|---|
| archive/docs/（1 件） | W1139 | 改：file-index 窗口归档连带 |
| docs/11-方案报告/设计与架构方案/（1 件） | W1139 | 改：§2 欠账路线 R-02 行改注已落地（含测绘修正：可见面涉页 515） |
| scripts/（5 件） | W1139 | 改：_strip_v1_provenance 两级变换（纯溯源块整剥→机读注释  |
| scripts/output/（2 件） | W1139 | 新增：本批 spec（618 面） |
| site/（10 件） | W1139 | 改：v1/v2 溯源元信息块出访客可见面（→机读注释·学术面保留）或零改动重写 |
| site/data/（88 件） | W1139 | 改：v1/v2 溯源元信息块出访客可见面（→机读注释·学术面保留）或零改动重写 |
| site/en/（138 件） | W1139 | 改：v1/v2 溯源元信息块出访客可见面（→机读注释·学术面保留）或零改动重写 |
| site/reader/（102 件） | W1139 | 改：v1/v2 溯源元信息块出访客可见面（→机读注释·学术面保留）或零改动重写 |
| site/reader/culture/（35 件） | W1139 | 改：v1/v2 溯源元信息块出访客可见面（→机读注释·学术面保留）或零改动重写 |
| site/reader/essays/（45 件） | W1139 | 改：v1/v2 溯源元信息块出访客可见面（→机读注释·学术面保留）或零改动重写 |
| site/reader/people/（216 件） | W1139 | 改：v1/v2 溯源元信息块出访客可见面（→机读注释·学术面保留）或零改动重写 |
| site/reader/poetry/（14 件） | W1139 | 改：v1/v2 溯源元信息块出访客可见面（→机读注释·学术面保留）或零改动重写 |
| site/reader/themes/（210 件） | W1139 | 改：v1/v2 溯源元信息块出访客可见面（→机读注释·学术面保留）或零改动重写 |

## W1138 作品集入口与数据地基批（2026-11-05）

| 文件 | W | 说明 |
|---|---|---|
| site/about.html | W1138 | 新增：作品集入口页（方法与边界） |
| site/index.html | W1138 | 改：主导航/页脚加关于入口 + 全卷索引第 15 行 |
| site/guide.html | W1138 | 改：导航/页脚加关于入口 |
| site/data/cross-time-danmaku.html | W1138 | 改：页脚 W 令牌推进 |
| site/data/tag-cloud.html | W1138 | 改：页脚 W 令牌推进 |
| site/dukou-engine.html | W1138 | 改：页脚 W 令牌推进 |
| README.md | W1138 | 改：作品集速览段 + 30 秒上手表入口 |
| CHANGELOG.md | W1138 | 改：新增 W1138 段 + 全站页数口径刷新 |
| HANDOVER.md | W1138 | 改：当前进度/头链/里程碑块 |
| AGENTS.md | W1138 | 改：版本脚注批次注记 |
| STRUCTURE.md | W1138 | 改：版本行同步 |
| docs/00-导读/项目说明.md | W1138 | 改：版本行同步 |
| docs/00-导读/W批次编号对账表.md | W1138 | 改：新增认领行 |
| docs/agent/gates.md | W1138 | 改：stats 标记数值同步 |
| docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md | W1138 | 改：stats 标记数值同步 |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1138 | 改：stats 标记数值同步 |
| site/sitemap.xml | W1138 | 改：新增 about.html 条目 |
| site/data/search.html | W1138 | 改：搜索索引重建 |
| site/en/search.html | W1138 | 改：搜索索引重建 |
| scripts/output/stats.json | W1138 | 改：统计基线 5 键刷新 |
| scripts/output/stats-changelog.json | W1138 | 改：变更史追加 |
| scripts/output/stats-index.md | W1138 | 改：反向索引重渲染 |
| scripts/output/file-index.md | W1138 | 改：本批条目 |
| scripts/output/INDEX.md | W1138 | 改：目录文档 refreshing 收录新页 |
| scripts/output/README.md | W1138 | 改：目录文档计数刷新 |
| scripts/output/tools-inventory.md | W1138 | 改：工具清单刷新 |
| site/INDEX.md | W1138 | 改：目录文档收录 about.html |
| site/README.md | W1138 | 改：直属文件计数 19→20 |
| scripts/output/_vermilion_solid_cache.json | W1138 | 改：朱砂实底门禁缓存纳入 about.html |
| scripts/output/_vermilion_solid_report.json | W1138 | 改：朱砂实底门禁报告 scope 235 与 about.html 读数 |
| scripts/output/_w1138_spec.json | W1138 | 新增：本批 spec |
| scripts/output/_cascade_files_W1138.txt | W1138 | 新增：级联文件清单 |
| CITATION.cff | W1138 | 改：版本面同步 |
| .github/workflows/README.md | W1138 | 改：版本面同步 |
| archive/docs/AGENTS-ARCHIVE.md | W1138 | 改：脚注滚动归档 |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1138 | 改：台账行窗口归档 |
| dataset/CODING.md | W1138 | 新增：人物关系编码手册 |
| dataset/character-relationship-3d.json | W1138 | 改：22 节点/32 边补溯源字段 |
| dataset/README.md | W1138 | 改：编码与溯源入口 |
| site/data/character-relationship-3d.html | W1138 | 改：EMBEDDED 同步 + 数据源脚注 |
| scripts/check_dataset_provenance.py | W1138 | 新增：数据集溯源校验器 |
| tests/unit/test_w1138_dataset_provenance.py | W1138 | 新增：溯源校验器回归锁 |
| tests/unit/INDEX.md | W1138 | 改：目录索引收录新测试 |
| tests/unit/README.md | W1138 | 改：测试计数刷新 |
| .github/ISSUE_TEMPLATE/data_correction.yml | W1138 | 新增：数据纠错/编码争议模板 |
| .github/ISSUE_TEMPLATE/README.md | W1138 | 改：模板数量说明 |
| .github/ISSUE_TEMPLATE/INDEX.md | W1138 | 改：目录索引收录新模板 |
| dataset/INDEX.md | W1138 | 改：目录索引收录 CODING.md |
| scripts/INDEX.md | W1138 | 改：目录索引收录溯源校验器 |
| pytest.ini | W1138 | 改：pytest collected 统计标记 1391→1392 |

## W1137 界面交互迭代批·四轮复核落地（2026-11-05）

| 文件 | W | 说明 |
|---|---|---|
| .agent/skills/puti-shouye/（1 件） | W1137 | 改：坑表总数引用 288→290（两处） |
| .github/（2 件） | W1137 | 删：dependabot 永久降噪（用户 2026-11-05 批准·12 PR |
| .github/workflows/（1 件） | W1137 | 改：版本抬头推进 W450-W1137（级联 versions·幂等） |
| archive/docs/（1 件） | W1137 | 改：脚注滚动归档（级联） |
| docs/（1 件） | W1137 | 改：gen_folder_docs 刷新（级联） |
| docs/00-导读/（2 件） | W1137 | 改：版本面推进（级联 versions 步·幂等） |
| docs/11-方案报告/（1 件） | W1137 | 改：登记第 103/104 号（四轮复核报告 + W1137 施工方案·尾部段末 |
| docs/11-方案报告/审查与评审/（1 件） | W1137 | 新增：四轮复核报告（W926/W1070 遗留闭环核验 + 五维度现势 + N- |
| docs/11-方案报告/设计与架构方案/（3 件） | W1137 | 新增：本批施工方案（方案即落地记录·欠账路线 v4 语义族/R-02 模板层） |
| docs/agent/（1 件） | W1137 | 改：W1095 收编 E-196/E-197 续号入表（流程节 158→160· |
| scripts/（3 件） | W1137 | 改：_face_footers 短令牌根修（R-02）+ 级联续跑容忍（规则行已 |
| scripts/output/（10 件） | W1137 | 新增：本批 spec（file_index_rows 864 面·含 857 页 |
| site/（9 件） | W1137 | 改：favicon 品牌图标注入（三行 link·复用 static/icons |
| site/data/（88 件） | W1137 | 改：favicon 品牌图标注入（三行 link·复用 static/icons |
| site/en/（138 件） | W1137 | 改：favicon 品牌图标注入（三行 link·复用 static/icons |
| site/reader/（102 件） | W1137 | 改：favicon 品牌图标注入（三行 link·复用 static/icons |
| site/reader/culture/（35 件） | W1137 | 改：favicon 品牌图标注入（三行 link·复用 static/icons |
| site/reader/essays/（45 件） | W1137 | 改：favicon 品牌图标注入（三行 link·复用 static/icons |
| site/reader/people/（216 件） | W1137 | 改：favicon 品牌图标注入（三行 link·复用 static/icons |
| site/reader/poetry/（14 件） | W1137 | 改：favicon 品牌图标注入（三行 link·复用 static/icons |
| site/reader/themes/（210 件） | W1137 | 改：favicon 品牌图标注入（三行 link·复用 static/icons |
| site/static/js/（1 件） | W1137 | 改：W1071 生产守卫块去重（5 份→1 份·行为零变化） |
| tests/unit/（3 件） | W1137 | 改：TestFixC/TestDecide 夹具改用 _csp_index_li |
| DESIGN.md | W1137 | 改：新增 §2.6 品牌图标（favicon 单一事实源 = static/icons·禁第二标记·页脚短令牌契约） |
| AGENTS.md | W1137 | 改：坑位计数 288→290（§4.3）+ 脚注 W1137 条目（级联） |
| HANDOVER.md | W1137 | 改：坑表总数 288→290（两处）+ W1095 待办勾选 + 最后更新链（级联） |
| CHANGELOG.md | W1137 | 改：W1137 段落（级联） |
| README.md | W1137 | 改：版本面推进（级联 versions 步·幂等） |
| STRUCTURE.md | W1137 | 改：版本面推进（级联 versions 步·幂等） |
| CITATION.cff | W1137 | 改：版本面推进（级联 versions 步·幂等） |

## W1136 并行会话统筹调度批（2026-11-04）

| 文件 | W | 说明 |
|---|---|---|
| docs/00-导读/W批次编号对账表.md | W1136 | 改：W1136 认领行登记（touches 12 面全清单） |
| docs/11-方案报告/计划方案/T90-任务计划执行与经验沉淀报告-2026-11-04.md | W1136 | 新增：本批任务计划执行与经验沉淀报告（统筹调度） |
| docs/11-方案报告/README.md | W1136 | 改：登记第 102 号（尾部段末·双锚校验定位） |
| docs/agent/pitfalls.md | W1136 | 改：E-185 入表 + 流程节计数 138 → 139 |
| AGENTS.md | W1136 | 改：坑表总计数 268 → 269 + 六主题分项（流程 139） |
| HANDOVER.md | W1136 | 改：坑表计数三处 267/268 → 269 |
| .agent/skills/puti-shouye/SKILL.md | W1136 | 改：坑表总计数两处 268 → 269 |
| CHANGELOG.md | W1136 | 改：W1136 段 |
| scripts/output/file-index.md | W1136 | 改：W1136 段 |
| scripts/output/_w1136_spec.json | W1136 | 新增：本批 spec（应动全集单一事实源） |
| scripts/output/_cascade_files_W1136.txt | W1136 | 新增：级联文件清单 |
| README.md | W1136 | 改：版本行（幂等推进·跟随现役段） |
| STRUCTURE.md | W1136 | 改：版本行（幂等推进） |
| docs/00-导读/项目说明.md | W1136 | 改：版本行（幂等推进） |
| CITATION.cff | W1136 | 改：版本与日期（幂等推进） |
| site/data/search.html | W1136 | 改：版本面字面量（副作用面） |
| site/en/search.html | W1136 | 改：版本面字面量（副作用面） |
| .github/workflows/README.md | W1136 | 改：版本面字面量（副作用面） |
| scripts/output/stats.json | W1136 | 改：统计产物 |
| scripts/output/stats-index.md | W1136 | 改：统计产物 |
| scripts/output/stats-changelog.json | W1136 | 改：统计产物 |
| scripts/output/tools-inventory.md | W1136 | 改：工具清单（收官链产物刷新） |
| archive/docs/AGENTS-ARCHIVE.md | W1136 | 改：AGENTS 脚注滚动迁入的最老条目归档件（副作用面） |
| docs/INDEX.md | W1136 | 改：文档索引（索引刷新步产物·副作用面） |
| scripts/INDEX.md | W1136 | 改：脚本索引（索引刷新步产物·副作用面） |
| scripts/output/INDEX.md | W1136 | 改：产物索引（索引刷新步产物·副作用面） |
| scripts/output/README.md | W1136 | 改：产物说明（索引刷新步产物·副作用面） |
| tests/unit/INDEX.md | W1136 | 改：单测索引（索引刷新步产物·副作用面） |
| tests/unit/README.md | W1136 | 改：单测说明（索引刷新步产物·副作用面） |
| pytest.ini | W1136 | 改：统计面 pytest 用例计数（实体化字面量·stats 同步） |
| docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md | W1136 | 改：统计面 pytest 用例计数（实体化字面量·stats 同步） |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1136 | 改：统计面 pytest 用例计数（实体化字面量·stats 同步） |
| scripts/output/_vermilion_solid_cache.json | W1136 | 改：朱砂实底扫描缓存（收官链刷新产物·副作用面） |
| site/data/cross-time-danmaku.html | W1136 | 改：版本面字面量（页脚链 token·副作用面） |
| site/data/tag-cloud.html | W1136 | 改：版本面字面量（页脚链 token·副作用面） |
| site/dukou-engine.html | W1136 | 改：版本面字面量（页脚链 token·副作用面） |
| site/index.html | W1136 | 改：版本面字面量（页脚链 token·副作用面） |
| scripts/check_doc_sync.py | W1136 | 改：C4/C5 组判据死代码根修·补 return 与修缩进（E-195） |
| scripts/check_motion_guard.py | W1136 | 改：CodeQL bad-html-filtering-regexp 根修·标签与属性名大小写不敏感（E-194） |
| tests/unit/test_w1135_gates.py | W1136 | 改：新增大小写盲区鉴别用例 2 例（E-194） |
| scripts/generate_csp.py | W1136 | 改：内联脚本块提取正则统一（标签/属性名大小写不敏感 + 结束标签可带属性·E-194 同族根修） |
| scripts/check_csp_drift.py | W1136 | 改：与 generate_csp.py 的 SCRIPT_RE 逐字一致（E-194 同族根修·口径不得分叉） |
| scripts/check_js_syntax.py | W1136 | 改：内联脚本块提取正则统一（E-194 同族根修） |
| scripts/check_js_syntax.js | W1136 | 改：内联脚本块提取正则统一（E-194 同族根修） |


## W1135 遗留清偿批 · d3 动效守卫表达式实参根治 + tooltip 死规则收口 + design 清单生成源根修 + 盲审 6 条处置（2026-11-05）

| 文件 | W | 说明 |
|---|---|---|
| AGENTS.md | W1135 | 本批实质/生成链连带 |
| CHANGELOG.md | W1135 | 本批实质/生成链连带 |
| HANDOVER.md | W1135 | 本批实质/生成链连带 |
| README.md | W1135 | 本批实质/生成链连带 |
| STRUCTURE.md | W1135 | 本批实质/生成链连带 |
| assets/design/README.md | W1135 | 本批实质/生成链连带 |
| assets/design/index.html | W1135 | 本批实质/生成链连带 |
| assets/design/logo/README.md | W1135 | 本批实质/生成链连带 |
| assets/design/screenshots/README.md | W1135 | 本批实质/生成链连带 |
| assets/design/tools/build_assets.py | W1135 | 本批实质/生成链连带 |
| docs/00-导读/W批次编号对账表.md | W1135 | 本批实质/生成链连带 |
| docs/00-导读/文档规范.md | W1135 | 本批实质/生成链连带 |
| docs/11-方案报告/README.md | W1135 | 本批实质/生成链连带 |
| docs/11-方案报告/审查与评审/设计文件审查报告-2026-11-02.md | W1135 | 本批实质/生成链连带 |
| docs/11-方案报告/计划方案/T87-任务计划执行与经验沉淀报告-2026-11-05.md | W1135 | 本批实质/生成链连带 |
| docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md | W1135 | 本批实质/生成链连带 |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1135 | 本批实质/生成链连带 |
| docs/INDEX.md | W1135 | 本批实质/生成链连带 |
| docs/agent/gates.md | W1135 | 本批实质/生成链连带 |
| docs/agent/pitfalls.md | W1135 | 本批实质/生成链连带 |
| pytest.ini | W1135 | 本批实质/生成链连带 |
| scripts/INDEX.md | W1135 | 本批实质/生成链连带 |
| scripts/check_design_asset_manifest.py | W1135 | 本批实质/生成链连带 |
| scripts/check_motion_guard.py | W1135 | 本批实质/生成链连带 |
| scripts/check_tooltip_spacing.py | W1135 | 本批实质/生成链连带 |
| scripts/cross_line_baseline.json | W1135 | 本批实质/生成链连带 |
| scripts/output/INDEX.md | W1135 | 本批实质/生成链连带 |
| scripts/output/README.md | W1135 | 本批实质/生成链连带 |
| scripts/output/_w1135_spec.json | W1135 | 本批实质/生成链连带 |
| scripts/output/file-index.md | W1135 | 本批实质/生成链连带 |
| scripts/output/stats-changelog.json | W1135 | 本批实质/生成链连带 |
| scripts/output/stats-index.md | W1135 | 本批实质/生成链连带 |
| scripts/output/stats.json | W1135 | 本批实质/生成链连带 |
| scripts/output/tools-inventory.md | W1135 | 本批实质/生成链连带 |
| scripts/verify_delivery.py | W1135 | 本批实质/生成链连带 |
| site/dashboard.html | W1135 | 本批实质/生成链连带 |
| site/data/81-hardships.html | W1135 | 本批实质/生成链连带 |
| site/data/cave-estate.html | W1135 | 本批实质/生成链连带 |
| site/data/chapter-stats.html | W1135 | 本批实质/生成链连带 |
| site/data/character-appearance.html | W1135 | 本批实质/生成链连带 |
| site/data/chart-design.html | W1135 | 本批实质/生成链连带 |
| site/data/counterfactual.html | W1135 | 本批实质/生成链连带 |
| site/data/cultural-misreading.html | W1135 | 本批实质/生成链连带 |
| site/data/deconstruction.html | W1135 | 本批实质/生成链连带 |
| site/data/emotional-heatmap.html | W1135 | 本批实质/生成链连带 |
| site/data/ethics-consumption.html | W1135 | 本批实质/生成链连带 |
| site/data/game-webnovel.html | W1135 | 本批实质/生成链连带 |
| site/data/global-pattern.html | W1135 | 本批实质/生成链连带 |
| site/data/hardship-difficulty-heatmap.html | W1135 | 本批实质/生成链连带 |
| site/data/hardship-heatmap.html | W1135 | 本批实质/生成链连带 |
| site/data/heaven-power-network.html | W1135 | 本批实质/生成链连带 |
| site/data/journey-geo-semiotics.html | W1135 | 本批实质/生成链连带 |
| site/data/journey-route.html | W1135 | 本批实质/生成链连带 |
| site/data/journey-spacetime.html | W1135 | 本批实质/生成链连带 |
| site/data/magic-system.html | W1135 | 本批实质/生成链连带 |
| site/data/mbti-evolution.html | W1135 | 本批实质/生成链连带 |
| site/data/methodology-matrix.html | W1135 | 本批实质/生成链连带 |
| site/data/ming-political-thought-comparison.html | W1135 | 本批实质/生成链连带 |
| site/data/monster-capability-radar.html | W1135 | 本批实质/生成链连带 |
| site/data/monster-hierarchy-network.html | W1135 | 本批实质/生成链连带 |
| site/data/narrative-experiment.html | W1135 | 本批实质/生成链连带 |
| site/data/pilgrim-team-psychology-arc.html | W1135 | 本批实质/生成链连带 |
| site/data/poetry-rhythm-analysis.html | W1135 | 本批实质/生成链连带 |
| site/data/search.html | W1135 | 本批实质/生成链连带 |
| site/data/social-media.html | W1135 | 本批实质/生成链连带 |
| site/data/text-evolution.html | W1135 | 本批实质/生成链连带 |
| site/data/underworld-power-network.html | W1135 | 本批实质/生成链连带 |
| site/data/visual-art.html | W1135 | 本批实质/生成链连带 |
| site/data/workplace.html | W1135 | 本批实质/生成链连带 |
| site/en/cave-estate.html | W1135 | 本批实质/生成链连带 |
| site/en/chapter-stats.html | W1135 | 本批实质/生成链连带 |
| site/en/character-appearance.html | W1135 | 本批实质/生成链连带 |
| site/en/chart-design.html | W1135 | 本批实质/生成链连带 |
| site/en/counterfactual.html | W1135 | 本批实质/生成链连带 |
| site/en/cultural-misreading.html | W1135 | 本批实质/生成链连带 |
| site/en/deconstruction.html | W1135 | 本批实质/生成链连带 |
| site/en/ethics-consumption.html | W1135 | 本批实质/生成链连带 |
| site/en/game-webnovel.html | W1135 | 本批实质/生成链连带 |
| site/en/global-pattern.html | W1135 | 本批实质/生成链连带 |
| site/en/hardship-difficulty-heatmap.html | W1135 | 本批实质/生成链连带 |
| site/en/hardship-heatmap.html | W1135 | 本批实质/生成链连带 |
| site/en/journey-geo-semiotics.html | W1135 | 本批实质/生成链连带 |
| site/en/journey-route.html | W1135 | 本批实质/生成链连带 |
| site/en/journey-spacetime.html | W1135 | 本批实质/生成链连带 |
| site/en/magic-system.html | W1135 | 本批实质/生成链连带 |
| site/en/mbti-evolution.html | W1135 | 本批实质/生成链连带 |
| site/en/methodology-matrix.html | W1135 | 本批实质/生成链连带 |
| site/en/ming-political-thought-comparison.html | W1135 | 本批实质/生成链连带 |
| site/en/monster-capability-radar.html | W1135 | 本批实质/生成链连带 |
| site/en/narrative-experiment.html | W1135 | 本批实质/生成链连带 |
| site/en/pilgrim-team-psychology-arc.html | W1135 | 本批实质/生成链连带 |
| site/en/poetry-rhythm-analysis.html | W1135 | 本批实质/生成链连带 |
| site/en/search.html | W1135 | 本批实质/生成链连带 |
| site/en/social-media.html | W1135 | 本批实质/生成链连带 |
| site/en/text-evolution.html | W1135 | 本批实质/生成链连带 |
| site/en/visual-art.html | W1135 | 本批实质/生成链连带 |
| site/en/workplace.html | W1135 | 本批实质/生成链连带 |
| tests/unit/INDEX.md | W1135 | 本批实质/生成链连带 |
| tests/unit/README.md | W1135 | 本批实质/生成链连带 |
| tests/unit/test_w1135_gates.py | W1135 | 本批实质/生成链连带 |


## W1134 前端质感 P0 批（2026-11-04）

| 文件 | W | 说明 |
|---|---|---|
| .agent/skills/puti-shouye/（1 件） | W1134 | 治理文档 |
| .github/workflows/（1 件） | W1134 | 治理文档 |
| archive/docs/（1 件） | W1134 | 治理文档 |
| docs/（1 件） | W1134 | 治理文档 |
| docs/00-导读/（2 件） | W1134 | 治理文档 |
| docs/11-方案报告/（1 件） | W1134 | 治理文档 |
| docs/11-方案报告/计划方案/（4 件） | W1134 | 治理文档 |
| docs/11-方案报告/设计与架构方案/（2 件） | W1134 | 治理文档 |
| docs/agent/（1 件） | W1134 | 治理文档 |
| scripts/（5 件） | W1134 | 本批工具/产物 |
| scripts/output/（18 件） | W1134 | 本批工具/产物 |
| site/（5 件） | W1134 | 页面 |
| site/data/（88 件） | W1134 | 页面 |
| site/en/（138 件） | W1134 | 页面 |
| site/reader/（102 件） | W1134 | 页面 |
| site/static/js/（1 件） | W1134 | 治理文档 |
| tests/unit/（4 件） | W1134 | 本批工具/产物 |
| AGENTS.md | W1134 | 治理文档 |
| CHANGELOG.md | W1134 | 治理文档 |
| CITATION.cff | W1134 | 治理文档 |
| HANDOVER.md | W1134 | 治理文档 |
| README.md | W1134 | 治理文档 |
| STRUCTURE.md | W1134 | 治理文档 |
| pytest.ini | W1134 | 治理文档 |


## W1133 自举产物教训入坑表 + W1001 段清理 + 档 3 消费方式原型（2026-11-04）

| 文件 | W | 说明 |
|---|---|---|
| .agent/skills/puti-shouye/SKILL.md | W1125 | 本批工具/产物 |
| AGENTS.md | W1125 | 本批工具/产物 |
| CHANGELOG.md | W1125 | 本批工具/产物 |
| HANDOVER.md | W1125 | 本批工具/产物 |
| docs/00-导读/W批次编号对账表.md | W1125 | 本批工具/产物 |
| docs/11-方案报告/README.md | W1125 | 本批工具/产物 |
| docs/11-方案报告/计划方案/T80-任务计划执行与经验沉淀报告-2026-11-04.md | W1125 | 本批工具/产物 |
| docs/INDEX.md | W1125 | 本批工具/产物 |
| docs/agent/pitfalls.md | W1125 | 本批工具/产物 |
| scripts/output/INDEX.md | W1125 | 本批工具/产物 |
| scripts/output/README.md | W1125 | 本批工具/产物 |
| scripts/output/_w1125_spec.json | W1125 | 本批工具/产物 |
| scripts/output/file-index.md | W1125 | 本批工具/产物 |
| scripts/output/stats.json | W1125 | 本批工具/产物 |
| scripts/output/tools-inventory.md | W1125 | 本批工具/产物 |
| site/data/chart-design.html | W1125 | 本批工具/产物 |
| site/data/search.html | W1125 | 本批工具/产物 |
| site/en/search.html | W1125 | 本批工具/产物 |
| STRUCTURE.md | W1125 | 生成链连带：报告件数变动后的结构口径同步 |
| docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md | W1125 | 生成链连带：报告件数标记面跟随 |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1125 | 生成链连带：报告件数标记面跟随 |
| scripts/output/stats-changelog.json | W1125 | 生成物：CHANGELOG 统计与现役口径同步 |
| scripts/output/stats-index.md | W1125 | 生成物：索引面统计同步 |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1125 | 台账腾窗：迁出 2 行至归档 |
| scripts/INDEX.md | W1125 | 生成链连带：scripts 目录索引（含补回文件）|
| docs/11-方案报告/计划方案/T79-任务计划执行与经验沉淀报告-2026-11-04.md | W1125 | 修复 main 侧遗留冲突标记残留（对方 W1127 批报告·首行冲突标记 + 夹带 T78 全文）|
| docs/11-方案报告/计划方案/T88-任务计划执行与经验沉淀报告-2026-11-04.md | W1133 | 新增：本批任务计划执行与经验沉淀报告 |


## W1132 第 51 槽 merge 带入面归属劫持根修（2026-11-04）

| 文件 | W | 说明 |
|---|---|---|
| scripts/check_commit_scope.py | W1132 | 改：兜底分支透传 main 带入面 + 新增段集合剔除带入段 + 剔除后走覆盖性反查 |
| tests/unit/test_w1132_scope_carried_owner.py | W1132 | 新增：归属劫持根修单测 4 例 |
| scripts/output/_w1132_spec.json | W1132 | 新增：本批 spec（应动全集单一事实源） |
| scripts/output/_cascade_files_W1132.txt | W1132 | 新增：本批级联清单 |
| docs/00-导读/W批次编号对账表.md | W1132 | 改：W1132 认领行 |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1132 | 改：腾窗迁出（如触发） |
| docs/11-方案报告/README.md | W1132 | 改：§六 第 100 号登记行（T86） |
| docs/11-方案报告/计划方案/T86-任务计划执行与经验沉淀报告-2026-11-04.md | W1132 | 新增：本批任务计划执行与经验沉淀报告 |
| CHANGELOG.md | W1132 | 改：W1132 段（降序位插段） |
| scripts/output/file-index.md | W1132 | 改：W1132 段 |
| HANDOVER.md | W1132 | 改：条目 + 最后更新行 |
| AGENTS.md | W1132 | 本批工具/产物 |
| README.md | W1132 | 本批工具/产物 |
| STRUCTURE.md | W1132 | 本批工具/产物 |
| CITATION.cff | W1132 | 本批工具/产物 |
| docs/00-导读/项目说明.md | W1132 | 本批工具/产物 |
| docs/INDEX.md | W1132 | 本批工具/产物 |
| .github/workflows/README.md | W1132 | 本批工具/产物 |
| archive/docs/AGENTS-ARCHIVE.md | W1132 | 本批工具/产物 |
| scripts/output/INDEX.md | W1132 | 本批工具/产物 |
| scripts/output/README.md | W1132 | 本批工具/产物 |
| scripts/output/stats.json | W1132 | 本批工具/产物 |
| scripts/output/stats-index.md | W1132 | 本批工具/产物 |
| scripts/output/stats-changelog.json | W1132 | 本批工具/产物 |
| scripts/output/tools-inventory.md | W1132 | 本批工具/产物 |
| tests/unit/INDEX.md | W1132 | 本批工具/产物 |
| tests/unit/README.md | W1132 | 本批工具/产物 |
| pytest.ini | W1132 | 本批工具/产物 |
| site/index.html | W1132 | 本批工具/产物 |
| site/data/search.html | W1132 | 本批工具/产物 |
| site/en/search.html | W1132 | 本批工具/产物 |
| site/data/cross-time-danmaku.html | W1132 | 本批工具/产物 |
| site/data/tag-cloud.html | W1132 | 本批工具/产物 |
| site/dukou-engine.html | W1132 | 本批工具/产物 |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1132 | 本批工具/产物 |
| docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md | W1132 | 本批工具/产物 |


## W1130 C9 扫描面扩展 + 台账回填与腾窗 + 两面下界根修 + 三条教训入坑表（2026-11-04）

| 文件 | W | 说明 |
|---|---|---|
| .agent/skills/puti-shouye/SKILL.md | W1130 | 生成链连带/生成物 |
| .github/workflows/README.md | W1130 | 生成链连带/生成物 |
| AGENTS.md | W1130 | 生成链连带/生成物 |
| CHANGELOG.md | W1130 | 生成链连带/生成物 |
| CITATION.cff | W1130 | 生成链连带/生成物 |
| HANDOVER.md | W1130 | 生成链连带/生成物 |
| README.md | W1130 | 生成链连带/生成物 |
| STRUCTURE.md | W1130 | 生成链连带/生成物 |
| archive/docs/CHANGELOG-ARCHIVE.md | W1130 | 本批实质：CHANGELOG 49 段迁入（两面同下界 W1108 对齐） |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1130 | 本批实质：台账腾窗迁出 W1072-W1076 共 5 行 + 迁入注记同步（正本 60 → 54 行） |
| archive/docs/file-index-ARCHIVE.md | W1130 | 本批实质：file-index 50 段迁入（体积模式归档·两侧同下界对齐） |
| docs/00-导读/W批次编号对账表.md | W1130 | 本批实质：台账四行处理（W1127 回填 / W1125 回填与错引订正 / W1130 认领行）+ 腾窗至 54 行 |
| docs/00-导读/项目说明.md | W1130 | 生成链连带/生成物 |
| docs/11-方案报告/README.md | W1130 | 本批实质：§六 第 98 号登记（T84） |
| docs/11-方案报告/计划方案/T79-任务计划执行与经验沉淀报告-2026-11-04.md | W1130 | 本批实质：归档读数订正 411 → 414（以合并后实读为准） |
| docs/11-方案报告/计划方案/T84-任务计划执行与经验沉淀报告-2026-11-04.md | W1130 | 本批新增：本批报告 |
| docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md | W1130 | 生成链连带/生成物 |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1130 | 生成链连带/生成物 |
| docs/INDEX.md | W1130 | 生成链连带/生成物 |
| docs/agent/pitfalls.md | W1130 | 本批实质：三条教训 E-176 ~ E-178 入表 + 计数链 138 → 141 |
| pytest.ini | W1130 | 生成链连带/生成物 |
| scripts/archive_segments.py | W1130 | 本批实质：归档迁出不得吞正本末尾文件级块根修（_tail_block_start + split_tail_block + A3 断言扩展） |
| scripts/check_doc_sync.py | W1130 | 本批实质：C9 冲突标记扫描面扩展（方案报告全树递归） |
| scripts/output/INDEX.md | W1130 | 生成链连带/生成物 |
| scripts/output/README.md | W1130 | 生成链连带/生成物 |
| scripts/output/_cascade_files_W1130.txt | W1130 | 本批自举产物：级联落盘清单 |
| scripts/output/_w1130_spec.json | W1130 | 本批自举产物：spec 本身 |
| scripts/output/file-index.md | W1130 | 生成链连带/生成物 |
| scripts/output/stats-changelog.json | W1130 | 生成链连带/生成物 |
| scripts/output/stats-index.md | W1130 | 生成链连带/生成物 |
| scripts/output/stats.json | W1130 | 生成链连带/生成物 |
| scripts/output/tools-inventory.md | W1130 | 生成链连带/生成物 |
| site/data/cross-time-danmaku.html | W1130 | 生成链连带/生成物 |
| site/data/search.html | W1130 | 生成链连带/生成物 |
| site/data/tag-cloud.html | W1130 | 生成链连带/生成物 |
| site/dukou-engine.html | W1130 | 生成链连带/生成物 |
| site/en/search.html | W1130 | 生成链连带/生成物 |
| site/index.html | W1130 | 生成链连带/生成物 |
| tests/unit/INDEX.md | W1130 | 生成链连带/生成物 |
| tests/unit/README.md | W1130 | 生成链连带/生成物 |
| tests/unit/test_w1130_archive_tail_block.py | W1130 | 本批新增：归档末尾块根修单测 5 例 |
| tests/unit/test_w1130_c9_report_scope.py | W1130 | 本批实质：C9 扫描面扩展单测 5 例 |

## W1129 PR 节奏纪律变更 + 提交范围门禁多批归属支持（2026-11-04）

| 文件 | W | 说明 |
|---|---|---|
| docs/agent/pitfalls.md | W1124 | 改：七条教训入表 E-165 ~ E-171 + 两处主题节标题计数 |
| AGENTS.md | W1124 | 改：阅读契约总计数 + 六主题分项行 + 版本脚注条目 |
| .agent/skills/puti-shouye/SKILL.md | W1124 | 改：坑表总计数两处 |
| HANDOVER.md | W1124 | 改：坑表总计数三处（含历史滞后补平）+ 头链 entry + 里程碑块 + 脚注条目 |
| scripts/batch_closeout.py | W1124 | 改：收官链接入幂等段重建步（rebuild·排在 precheck 之前） |
| scripts/batch_cascade.py | W1124 | 改：里程碑滚动幂等守卫下沉到函数内 |
| scripts/check_repo_layout.py | W1124 | 改：布局门禁适配 worktree 形态（根目录 .git 指针文件不计入根文件清单·judge 层判据强度不降） |
| tests/unit/test_w1124_closeout_rebuild.py | W1124 | 新增：收官链顺序锁 + 重建幂等 + 滚动守卫自证 10 例 |
| scripts/output/_w1124_spec.json | W1124 | 新增：本批 spec（应动全集单一事实源） |
| scripts/output/_cascade_files_W1124.txt | W1124 | 新增：级联文件清单 |
| docs/00-导读/W批次编号对账表.md | W1124 | 改：W1124 认领行登记 + W1122 行回填与例数订正 |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1124 | 改：台账腾窗迁出的最老行（收官链 archive 步产物·副作用面） |
| docs/11-方案报告/计划方案/T75-任务计划执行与经验沉淀报告-2026-11-04.md | W1124 | 新增：本批任务计划执行与经验沉淀报告 |
| docs/11-方案报告/README.md | W1124 | 改：登记第 90 号 |
| CHANGELOG.md | W1124 | 改：W1124 段 |
| scripts/output/file-index.md | W1124 | 改：W1124 段 |
| README.md | W1124 | 改：版本行（幂等推进） |
| STRUCTURE.md | W1124 | 改：版本行（幂等推进） |
| docs/00-导读/项目说明.md | W1124 | 改：版本行（幂等推进） |
| CITATION.cff | W1124 | 改：版本与日期（幂等推进） |
| site/data/search.html | W1124 | 改：版本面字面量（搜索页版本行·副作用面） |
| site/en/search.html | W1124 | 改：版本面字面量（搜索页版本行·副作用面） |
| .github/workflows/README.md | W1124 | 改：版本面字面量（副作用面） |
| scripts/output/stats.json | W1124 | 改：统计产物 |
| scripts/output/stats-index.md | W1124 | 改：统计产物 |
| scripts/output/stats-changelog.json | W1124 | 改：统计产物 |
| scripts/output/tools-inventory.md | W1124 | 改：工具清单（收官链产物刷新） |
| archive/docs/AGENTS-ARCHIVE.md | W1124 | 改：AGENTS 脚注滚动迁入的最老条目归档件（副作用面） |
| docs/INDEX.md | W1124 | 改：文档索引（索引刷新步产物·副作用面） |
| scripts/INDEX.md | W1124 | 改：脚本索引（索引刷新步产物·副作用面） |
| scripts/output/INDEX.md | W1124 | 改：产物索引（索引刷新步产物·副作用面） |
| scripts/output/README.md | W1124 | 改：产物说明（索引刷新步产物·副作用面） |
| tests/unit/INDEX.md | W1124 | 改：单测索引（索引刷新步产物·副作用面） |
| tests/unit/README.md | W1124 | 改：单测说明（索引刷新步产物·副作用面） |
| pytest.ini | W1124 | 改：统计面 pytest 用例计数（实体化字面量·stats 同步） |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1124 | 改：统计面 pytest 用例计数（实体化字面量·stats 同步） |
| docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md | W1124 | 改：统计面 pytest 用例计数（实体化字面量·stats 同步） |
| site/index.html | W1124 | 改：页脚批次链 token（W1124·副作用面） |
| site/data/cross-time-danmaku.html | W1124 | 改：页脚批次链 token（W1124·副作用面） |
| site/data/tag-cloud.html | W1124 | 改：页脚批次链 token（W1124·副作用面） |
| site/dukou-engine.html | W1124 | 改：页脚批次链 token（W1124·副作用面） |
| scripts/cascade_idempotence.py | W1122 | 新增：级联插入型面幂等 upsert 原语（单一事实源·不存在⇒插入/一致⇒零变化/不一致⇒替换） |
| scripts/batch_cascade.py | W1122 | 改：六个插入型面接幂等原语（交接头链与里程碑块/AGENTS 脚注/workflows 尾标记/页脚链 token/CHANGELOG 段/file-index 段） |
| scripts/backfill_changelog.py | W1122 | 改：立段判定改双面独立（CHANGELOG 面与 file-index 面分判·只补缺的一面·历史缺口须显式确认才补） |
| tests/unit/test_w1122_cascade_idempotence.py | W1122 | 新增：幂等原语与六面接入自证 19 例 |
| tests/unit/test_w1122_pending_faces.py | W1122 | 新增：双面独立判定自证 5 例 |
| docs/00-导读/W批次编号对账表.md | W1122 | 改：W1120 与 W1121 两行回填 + W1122 认领行登记 |
| docs/11-方案报告/计划方案/T74-任务计划执行与经验沉淀报告-2026-11-04.md | W1122 | 新增：本批任务计划执行与经验沉淀报告 |
| docs/11-方案报告/README.md | W1122 | 改：登记第 89 号 |
| scripts/output/_w1122_spec.json | W1122 | 新增：本批 spec（应动全集单一事实源） |
| scripts/output/_cascade_files_W1122.txt | W1122 | 新增：级联文件清单 |
| CHANGELOG.md | W1122 | 改：W1122 段 |
| scripts/output/file-index.md | W1122 | 改：W1122 段 |
| HANDOVER.md | W1122 | 改：头链 entry 与里程碑块与进度标题与 HEAD 句（幂等） |
| AGENTS.md | W1122 | 改：版本脚注条目（幂等） |
| .github/workflows/README.md | W1122 | 改：里程碑尾标记（幂等） |
| site/index.html | W1122 | 改：页脚批次链 token（幂等） |
| site/data/cross-time-danmaku.html | W1122 | 改：页脚批次链 token（幂等） |
| site/data/tag-cloud.html | W1122 | 改：页脚批次链 token（幂等） |
| site/dukou-engine.html | W1122 | 改：页脚批次链 token（幂等） |
| README.md | W1122 | 改：版本行（幂等推进） |
| STRUCTURE.md | W1122 | 改：版本行（幂等推进） |
| docs/00-导读/项目说明.md | W1122 | 改：版本行（幂等推进） |
| CITATION.cff | W1122 | 改：版本与日期（幂等推进） |
| scripts/output/tools-inventory.md | W1122 | 改：工具清单（新增模块入册） |
| scripts/output/stats.json | W1122 | 改：统计产物 |
| scripts/output/stats-index.md | W1122 | 改：统计产物 |
| scripts/output/stats-changelog.json | W1122 | 改：统计产物 |
| archive/docs/AGENTS-ARCHIVE.md | W1122 | 改：AGENTS 脚注滚动迁入的最老条目归档件（级联副作用面） |
| pytest.ini | W1122 | 改：统计面 pytest 用例计数（实体化字面量·stats 同步） |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1122 | 改：统计面 pytest 用例计数（实体化字面量·stats 同步） |
| docs/INDEX.md | W1122 | 改：文档索引（级联/索引刷新步产物·副作用面） |
| scripts/INDEX.md | W1122 | 改：脚本索引（级联/索引刷新步产物·副作用面） |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1122 | 改：台账腾窗迁出的最老行（收官链 archive 步产物·副作用面） |
| docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md | W1122 | 改：统计面 pytest 用例计数（实体化字面量·stats 同步） |
| site/data/search.html | W1122 | 改：版本面字面量（搜索页版本行·幂等推进·副作用面） |
| site/en/search.html | W1122 | 改：版本面字面量（搜索页版本行·幂等推进·副作用面） |
| scripts/output/INDEX.md | W1122 | 改：产物索引（索引刷新步产物·副作用面） |
| scripts/output/README.md | W1122 | 改：产物说明（索引刷新步产物·副作用面） |
| tests/unit/INDEX.md | W1122 | 改：单测索引（索引刷新步产物·副作用面） |
| tests/unit/README.md | W1122 | 改：单测说明（索引刷新步产物·副作用面） |
| tests/unit/test_w1102_batch_closeout.py | W1128 | 本批工具/产物 |
| tests/unit/test_w1128_pycompile_gate.py | W1128 | 本批工具/产物 |
| docs/11-方案报告/计划方案/T77-任务计划执行与经验沉淀报告-2026-11-04.md | W1128 | 本批工具/产物 |
| scripts/output/_w1128_spec.json | W1128 | 本批工具/产物 |
| scripts/output/_cascade_files_W1128.txt | W1128 | 本批工具/产物 |
| scripts/check_commit_scope.py | W1129 | 本批工具/产物 |
| tests/unit/test_w1129_commit_scope_multibatch.py | W1129 | 本批工具/产物 |
| docs/11-方案报告/计划方案/T78-任务计划执行与经验沉淀报告-2026-11-04.md | W1129 | 本批工具/产物 |
| scripts/output/_w1129_spec.json | W1129 | 本批工具/产物 |
| scripts/output/_cascade_files_W1129.txt | W1129 | 本批工具/产物 |

## W1128 收官链 py_compile 语法自检门禁（2026-11-04）

| 文件 | W | 说明 |
|---|---|---|
| docs/agent/pitfalls.md | W1124 | 改：七条教训入表 E-165 ~ E-171 + 两处主题节标题计数 |
| AGENTS.md | W1124 | 改：阅读契约总计数 + 六主题分项行 + 版本脚注条目 |
| .agent/skills/puti-shouye/SKILL.md | W1124 | 改：坑表总计数两处 |
| HANDOVER.md | W1124 | 改：坑表总计数三处（含历史滞后补平）+ 头链 entry + 里程碑块 + 脚注条目 |
| scripts/batch_closeout.py | W1124 | 改：收官链接入幂等段重建步（rebuild·排在 precheck 之前） |
| scripts/batch_cascade.py | W1124 | 改：里程碑滚动幂等守卫下沉到函数内 |
| scripts/check_repo_layout.py | W1124 | 改：布局门禁适配 worktree 形态（根目录 .git 指针文件不计入根文件清单·judge 层判据强度不降） |
| tests/unit/test_w1124_closeout_rebuild.py | W1124 | 新增：收官链顺序锁 + 重建幂等 + 滚动守卫自证 10 例 |
| scripts/output/_w1124_spec.json | W1124 | 新增：本批 spec（应动全集单一事实源） |
| scripts/output/_cascade_files_W1124.txt | W1124 | 新增：级联文件清单 |
| docs/00-导读/W批次编号对账表.md | W1124 | 改：W1124 认领行登记 + W1122 行回填与例数订正 |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1124 | 改：台账腾窗迁出的最老行（收官链 archive 步产物·副作用面） |
| docs/11-方案报告/计划方案/T75-任务计划执行与经验沉淀报告-2026-11-04.md | W1124 | 新增：本批任务计划执行与经验沉淀报告 |
| docs/11-方案报告/README.md | W1124 | 改：登记第 90 号 |
| CHANGELOG.md | W1124 | 改：W1124 段 |
| scripts/output/file-index.md | W1124 | 改：W1124 段 |
| README.md | W1124 | 改：版本行（幂等推进） |
| STRUCTURE.md | W1124 | 改：版本行（幂等推进） |
| docs/00-导读/项目说明.md | W1124 | 改：版本行（幂等推进） |
| CITATION.cff | W1124 | 改：版本与日期（幂等推进） |
| site/data/search.html | W1124 | 改：版本面字面量（搜索页版本行·副作用面） |
| site/en/search.html | W1124 | 改：版本面字面量（搜索页版本行·副作用面） |
| .github/workflows/README.md | W1124 | 改：版本面字面量（副作用面） |
| scripts/output/stats.json | W1124 | 改：统计产物 |
| scripts/output/stats-index.md | W1124 | 改：统计产物 |
| scripts/output/stats-changelog.json | W1124 | 改：统计产物 |
| scripts/output/tools-inventory.md | W1124 | 改：工具清单（收官链产物刷新） |
| archive/docs/AGENTS-ARCHIVE.md | W1124 | 改：AGENTS 脚注滚动迁入的最老条目归档件（副作用面） |
| docs/INDEX.md | W1124 | 改：文档索引（索引刷新步产物·副作用面） |
| scripts/INDEX.md | W1124 | 改：脚本索引（索引刷新步产物·副作用面） |
| scripts/output/INDEX.md | W1124 | 改：产物索引（索引刷新步产物·副作用面） |
| scripts/output/README.md | W1124 | 改：产物说明（索引刷新步产物·副作用面） |
| tests/unit/INDEX.md | W1124 | 改：单测索引（索引刷新步产物·副作用面） |
| tests/unit/README.md | W1124 | 改：单测说明（索引刷新步产物·副作用面） |
| pytest.ini | W1124 | 改：统计面 pytest 用例计数（实体化字面量·stats 同步） |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1124 | 改：统计面 pytest 用例计数（实体化字面量·stats 同步） |
| docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md | W1124 | 改：统计面 pytest 用例计数（实体化字面量·stats 同步） |
| site/index.html | W1124 | 改：页脚批次链 token（W1124·副作用面） |
| site/data/cross-time-danmaku.html | W1124 | 改：页脚批次链 token（W1124·副作用面） |
| site/data/tag-cloud.html | W1124 | 改：页脚批次链 token（W1124·副作用面） |
| site/dukou-engine.html | W1124 | 改：页脚批次链 token（W1124·副作用面） |
| scripts/cascade_idempotence.py | W1122 | 新增：级联插入型面幂等 upsert 原语（单一事实源·不存在⇒插入/一致⇒零变化/不一致⇒替换） |
| scripts/batch_cascade.py | W1122 | 改：六个插入型面接幂等原语（交接头链与里程碑块/AGENTS 脚注/workflows 尾标记/页脚链 token/CHANGELOG 段/file-index 段） |
| scripts/backfill_changelog.py | W1122 | 改：立段判定改双面独立（CHANGELOG 面与 file-index 面分判·只补缺的一面·历史缺口须显式确认才补） |
| tests/unit/test_w1122_cascade_idempotence.py | W1122 | 新增：幂等原语与六面接入自证 19 例 |
| tests/unit/test_w1122_pending_faces.py | W1122 | 新增：双面独立判定自证 5 例 |
| docs/00-导读/W批次编号对账表.md | W1122 | 改：W1120 与 W1121 两行回填 + W1122 认领行登记 |
| docs/11-方案报告/计划方案/T74-任务计划执行与经验沉淀报告-2026-11-04.md | W1122 | 新增：本批任务计划执行与经验沉淀报告 |
| docs/11-方案报告/README.md | W1122 | 改：登记第 89 号 |
| scripts/output/_w1122_spec.json | W1122 | 新增：本批 spec（应动全集单一事实源） |
| scripts/output/_cascade_files_W1122.txt | W1122 | 新增：级联文件清单 |
| CHANGELOG.md | W1122 | 改：W1122 段 |
| scripts/output/file-index.md | W1122 | 改：W1122 段 |
| HANDOVER.md | W1122 | 改：头链 entry 与里程碑块与进度标题与 HEAD 句（幂等） |
| AGENTS.md | W1122 | 改：版本脚注条目（幂等） |
| .github/workflows/README.md | W1122 | 改：里程碑尾标记（幂等） |
| site/index.html | W1122 | 改：页脚批次链 token（幂等） |
| site/data/cross-time-danmaku.html | W1122 | 改：页脚批次链 token（幂等） |
| site/data/tag-cloud.html | W1122 | 改：页脚批次链 token（幂等） |
| site/dukou-engine.html | W1122 | 改：页脚批次链 token（幂等） |
| README.md | W1122 | 改：版本行（幂等推进） |
| STRUCTURE.md | W1122 | 改：版本行（幂等推进） |
| docs/00-导读/项目说明.md | W1122 | 改：版本行（幂等推进） |
| CITATION.cff | W1122 | 改：版本与日期（幂等推进） |
| scripts/output/tools-inventory.md | W1122 | 改：工具清单（新增模块入册） |
| scripts/output/stats.json | W1122 | 改：统计产物 |
| scripts/output/stats-index.md | W1122 | 改：统计产物 |
| scripts/output/stats-changelog.json | W1122 | 改：统计产物 |
| archive/docs/AGENTS-ARCHIVE.md | W1122 | 改：AGENTS 脚注滚动迁入的最老条目归档件（级联副作用面） |
| pytest.ini | W1122 | 改：统计面 pytest 用例计数（实体化字面量·stats 同步） |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1122 | 改：统计面 pytest 用例计数（实体化字面量·stats 同步） |
| docs/INDEX.md | W1122 | 改：文档索引（级联/索引刷新步产物·副作用面） |
| scripts/INDEX.md | W1122 | 改：脚本索引（级联/索引刷新步产物·副作用面） |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1122 | 改：台账腾窗迁出的最老行（收官链 archive 步产物·副作用面） |
| docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md | W1122 | 改：统计面 pytest 用例计数（实体化字面量·stats 同步） |
| site/data/search.html | W1122 | 改：版本面字面量（搜索页版本行·幂等推进·副作用面） |
| site/en/search.html | W1122 | 改：版本面字面量（搜索页版本行·幂等推进·副作用面） |
| scripts/output/INDEX.md | W1122 | 改：产物索引（索引刷新步产物·副作用面） |
| scripts/output/README.md | W1122 | 改：产物说明（索引刷新步产物·副作用面） |
| tests/unit/INDEX.md | W1122 | 改：单测索引（索引刷新步产物·副作用面） |
| tests/unit/README.md | W1122 | 改：单测说明（索引刷新步产物·副作用面） |
| tests/unit/test_w1102_batch_closeout.py | W1128 | 本批工具/产物 |
| tests/unit/test_w1128_pycompile_gate.py | W1128 | 本批工具/产物 |
| docs/11-方案报告/计划方案/T77-任务计划执行与经验沉淀报告-2026-11-04.md | W1128 | 本批工具/产物 |
| scripts/output/_w1128_spec.json | W1128 | 本批工具/产物 |
| scripts/output/_cascade_files_W1128.txt | W1128 | 本批工具/产物 |

## W1127 治理收官批·台账回填 + 滚动独立入口 + 历史缺口体检（2026-11-04）

| 文件 | W | 说明 |
|---|---|---|
| scripts/batch_cascade.py | W1127 | 改：增里程碑滚动独立入口 --rotate-only（幂等守卫沿用函数内·零变化） |
| scripts/check_segment_gaps.py | W1127 | 新增：历史缺口体检工具（台账有认领行而两面正本皆无段·含可复原来源提示） |
| tests/unit/test_w1127_closeout_tools.py | W1127 | 新增：滚动独立入口与缺口体检自证 6 例 |
| scripts/output/_w1127_spec.json | W1127 | 新增：本批 spec（应动全集单一事实源） |
| scripts/output/_cascade_files_W1127.txt | W1127 | 新增：级联文件清单 |
| docs/00-导读/W批次编号对账表.md | W1127 | 改：W1127 认领行登记 + W1124 行回填与例数订正 + 台账腾窗 |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1127 | 改：台账腾窗迁出的最老行（收官链 archive 步产物·副作用面） |
| archive/docs/AGENTS-ARCHIVE.md | W1127 | 改：AGENTS 脚注滚动迁入的最老条目归档件（级联副作用面） |
| docs/11-方案报告/计划方案/T79-任务计划执行与经验沉淀报告-2026-11-04.md | W1127 | 新增：本批任务计划执行与经验沉淀报告 |
| docs/11-方案报告/README.md | W1127 | 改：登记第 92 号 |
| CHANGELOG.md | W1127 | 改：W1127 段 |
| scripts/output/file-index.md | W1127 | 改：W1127 段 |
| HANDOVER.md | W1127 | 改：头链 entry 与里程碑块与进度标题与 HEAD 句（幂等） |
| AGENTS.md | W1127 | 改：版本脚注条目（幂等） |
| .github/workflows/README.md | W1127 | 改：里程碑尾标记（幂等） |
| README.md | W1127 | 改：版本行（幂等推进） |
| STRUCTURE.md | W1127 | 改：版本行（幂等推进） |
| docs/00-导读/项目说明.md | W1127 | 改：版本行（幂等推进） |
| CITATION.cff | W1127 | 改：版本与日期（幂等推进） |
| site/data/search.html | W1127 | 改：版本面字面量（搜索页版本行·副作用面） |
| site/en/search.html | W1127 | 改：版本面字面量（搜索页版本行·副作用面） |
| site/index.html | W1127 | 改：页脚批次链 token（副作用面） |
| site/data/cross-time-danmaku.html | W1127 | 改：页脚批次链 token（副作用面） |
| site/data/tag-cloud.html | W1127 | 改：页脚批次链 token（副作用面） |
| site/dukou-engine.html | W1127 | 改：页脚批次链 token（副作用面） |
| scripts/output/stats.json | W1127 | 改：统计产物 |
| scripts/output/stats-index.md | W1127 | 改：统计产物 |
| scripts/output/stats-changelog.json | W1127 | 改：统计产物 |
| scripts/output/tools-inventory.md | W1127 | 改：工具清单（新增脚本入册） |
| docs/INDEX.md | W1127 | 改：文档索引（索引刷新步产物·副作用面） |
| scripts/INDEX.md | W1127 | 改：脚本索引（索引刷新步产物·副作用面） |
| scripts/output/INDEX.md | W1127 | 改：产物索引（索引刷新步产物·副作用面） |
| scripts/output/README.md | W1127 | 改：产物说明（索引刷新步产物·副作用面） |
| tests/unit/INDEX.md | W1127 | 改：单测索引（索引刷新步产物·副作用面） |
| tests/unit/README.md | W1127 | 改：单测说明（索引刷新步产物·副作用面） |
| pytest.ini | W1127 | 改：统计面 pytest 用例计数（实体化字面量·stats 同步） |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1127 | 改：统计面 pytest 用例计数（实体化字面量·stats 同步） |
| docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md | W1127 | 改：统计面 pytest 用例计数（实体化字面量·stats 同步） |


## W1126 截图审查 scope 判定根修（2026-11-04）

| 文件 | W | 说明 |
|---|---|---|
| .github/workflows/README.md | W1126 | 改：本批交付面（scope 判据脚本 + 单测 + 施工前对齐件 + 登记面） |
| CHANGELOG.md | W1126 | 改：本批交付面（scope 判据脚本 + 单测 + 施工前对齐件 + 登记面） |
| HANDOVER.md | W1126 | 改：本批交付面（scope 判据脚本 + 单测 + 施工前对齐件 + 登记面） |
| README.md | W1126 | 改：本批交付面（scope 判据脚本 + 单测 + 施工前对齐件 + 登记面） |
| STRUCTURE.md | W1126 | 改：本批交付面（scope 判据脚本 + 单测 + 施工前对齐件 + 登记面） |
| docs/00-导读/W批次编号对账表.md | W1126 | 改：本批交付面（scope 判据脚本 + 单测 + 施工前对齐件 + 登记面） |
| docs/00-导读/项目说明.md | W1126 | 改：本批交付面（scope 判据脚本 + 单测 + 施工前对齐件 + 登记面） |
| docs/11-方案报告/README.md | W1126 | 改：本批交付面（scope 判据脚本 + 单测 + 施工前对齐件 + 登记面） |
| docs/11-方案报告/计划方案/T79-任务计划执行与经验沉淀报告-2026-11-04.md | W1126 | 改：本批交付面（scope 判据脚本 + 单测 + 施工前对齐件 + 登记面） |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1126 | 改：本批交付面（scope 判据脚本 + 单测 + 施工前对齐件 + 登记面） |
| docs/INDEX.md | W1126 | 改：本批交付面（scope 判据脚本 + 单测 + 施工前对齐件 + 登记面） |
| pytest.ini | W1126 | 改：本批交付面（scope 判据脚本 + 单测 + 施工前对齐件 + 登记面） |
| scripts/INDEX.md | W1126 | 改：本批交付面（scope 判据脚本 + 单测 + 施工前对齐件 + 登记面） |
| scripts/check_screenshot_scope.py | W1126 | 改：本批交付面（scope 判据脚本 + 单测 + 施工前对齐件 + 登记面） |
| scripts/output/INDEX.md | W1126 | 改：本批交付面（scope 判据脚本 + 单测 + 施工前对齐件 + 登记面） |
| scripts/output/README.md | W1126 | 改：本批交付面（scope 判据脚本 + 单测 + 施工前对齐件 + 登记面） |
| scripts/output/_cascade_files_W1126.txt | W1126 | 改：本批交付面（scope 判据脚本 + 单测 + 施工前对齐件 + 登记面） |
| scripts/output/_vermilion_solid_cache.json | W1126 | 改：本批交付面（scope 判据脚本 + 单测 + 施工前对齐件 + 登记面） |
| scripts/output/_w1126_spec.json | W1126 | 改：本批交付面（scope 判据脚本 + 单测 + 施工前对齐件 + 登记面） |
| scripts/output/file-index.md | W1126 | 改：本批交付面（scope 判据脚本 + 单测 + 施工前对齐件 + 登记面） |
| scripts/output/stats-changelog.json | W1126 | 改：本批交付面（scope 判据脚本 + 单测 + 施工前对齐件 + 登记面） |
| scripts/output/stats-index.md | W1126 | 改：本批交付面（scope 判据脚本 + 单测 + 施工前对齐件 + 登记面） |
| scripts/output/stats.json | W1126 | 改：本批交付面（scope 判据脚本 + 单测 + 施工前对齐件 + 登记面） |
| scripts/output/tools-inventory.md | W1126 | 改：本批交付面（scope 判据脚本 + 单测 + 施工前对齐件 + 登记面） |
| site/data/search.html | W1126 | 改：本批交付面（scope 判据脚本 + 单测 + 施工前对齐件 + 登记面） |
| site/en/search.html | W1126 | 改：本批交付面（scope 判据脚本 + 单测 + 施工前对齐件 + 登记面） |
| tests/unit/INDEX.md | W1126 | 改：本批交付面（scope 判据脚本 + 单测 + 施工前对齐件 + 登记面） |
| tests/unit/README.md | W1126 | 改：本批交付面（scope 判据脚本 + 单测 + 施工前对齐件 + 登记面） |
| tests/unit/test_w1126_screenshot_scope.py | W1126 | 改：本批交付面（scope 判据脚本 + 单测 + 施工前对齐件 + 登记面） |

## W1125 自举产物教训入坑表 + W1001 段清理 + 档 3 消费方式原型（2026-11-04）

| 文件 | W | 说明 |
|---|---|---|
| .agent/skills/puti-shouye/SKILL.md | W1125 | 本批工具/产物 |
| AGENTS.md | W1125 | 本批工具/产物 |
| CHANGELOG.md | W1125 | 本批工具/产物 |
| HANDOVER.md | W1125 | 本批工具/产物 |
| docs/00-导读/W批次编号对账表.md | W1125 | 本批工具/产物 |
| docs/11-方案报告/README.md | W1125 | 本批工具/产物 |
| docs/11-方案报告/计划方案/T80-任务计划执行与经验沉淀报告-2026-11-04.md | W1125 | 本批工具/产物 |
| docs/INDEX.md | W1125 | 本批工具/产物 |
| docs/agent/pitfalls.md | W1125 | 本批工具/产物 |
| scripts/output/INDEX.md | W1125 | 本批工具/产物 |
| scripts/output/README.md | W1125 | 本批工具/产物 |
| scripts/output/_w1125_spec.json | W1125 | 本批工具/产物 |
| scripts/output/file-index.md | W1125 | 本批工具/产物 |
| scripts/output/stats.json | W1125 | 本批工具/产物 |
| scripts/output/tools-inventory.md | W1125 | 本批工具/产物 |
| site/data/chart-design.html | W1125 | 本批工具/产物 |
| site/data/search.html | W1125 | 本批工具/产物 |
| site/en/search.html | W1125 | 本批工具/产物 |
| STRUCTURE.md | W1125 | 生成链连带：报告件数变动后的结构口径同步 |
| docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md | W1125 | 生成链连带：报告件数标记面跟随 |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1125 | 生成链连带：报告件数标记面跟随 |
| scripts/output/stats-changelog.json | W1125 | 生成物：CHANGELOG 统计与现役口径同步 |
| scripts/output/stats-index.md | W1125 | 生成物：索引面统计同步 |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1125 | 台账腾窗：迁出 2 行至归档 |
| scripts/INDEX.md | W1125 | 生成链连带：scripts 目录索引（含补回文件）|
| docs/11-方案报告/计划方案/T79-任务计划执行与经验沉淀报告-2026-11-04.md | W1125 | 修复 main 侧遗留冲突标记残留（对方 W1127 批报告·首行冲突标记 + 夹带 T78 全文）|


## W1124 治理收尾批·教训入坑表 + 重建入口收进收官链（2026-11-04）

| 文件 | W | 说明 |
|---|---|---|
| docs/agent/pitfalls.md | W1124 | 改：七条教训入表 E-165 ~ E-171 + 两处主题节标题计数 |
| AGENTS.md | W1124 | 改：阅读契约总计数 + 六主题分项行 + 版本脚注条目 |
| .agent/skills/puti-shouye/SKILL.md | W1124 | 改：坑表总计数两处 |
| HANDOVER.md | W1124 | 改：坑表总计数三处（含历史滞后补平）+ 头链 entry + 里程碑块 + 脚注条目 |
| scripts/batch_closeout.py | W1124 | 改：收官链接入幂等段重建步（rebuild·排在 precheck 之前） |
| scripts/batch_cascade.py | W1124 | 改：里程碑滚动幂等守卫下沉到函数内 |
| scripts/check_repo_layout.py | W1124 | 改：布局门禁适配 worktree 形态（根目录 .git 指针文件不计入根文件清单·judge 层判据强度不降） |
| tests/unit/test_w1124_closeout_rebuild.py | W1124 | 新增：收官链顺序锁 + 重建幂等 + 滚动守卫自证 10 例 |
| scripts/output/_w1124_spec.json | W1124 | 新增：本批 spec（应动全集单一事实源） |
| scripts/output/_cascade_files_W1124.txt | W1124 | 新增：级联文件清单 |
| docs/00-导读/W批次编号对账表.md | W1124 | 改：W1124 认领行登记 + W1122 行回填与例数订正 |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1124 | 改：台账腾窗迁出的最老行（收官链 archive 步产物·副作用面） |
| docs/11-方案报告/计划方案/T75-任务计划执行与经验沉淀报告-2026-11-04.md | W1124 | 新增：本批任务计划执行与经验沉淀报告 |
| docs/11-方案报告/README.md | W1124 | 改：登记第 90 号 |
| CHANGELOG.md | W1124 | 改：W1124 段 |
| scripts/output/file-index.md | W1124 | 改：W1124 段 |
| README.md | W1124 | 改：版本行（幂等推进） |
| STRUCTURE.md | W1124 | 改：版本行（幂等推进） |
| docs/00-导读/项目说明.md | W1124 | 改：版本行（幂等推进） |
| CITATION.cff | W1124 | 改：版本与日期（幂等推进） |
| site/data/search.html | W1124 | 改：版本面字面量（搜索页版本行·副作用面） |
| site/en/search.html | W1124 | 改：版本面字面量（搜索页版本行·副作用面） |
| .github/workflows/README.md | W1124 | 改：版本面字面量（副作用面） |
| scripts/output/stats.json | W1124 | 改：统计产物 |
| scripts/output/stats-index.md | W1124 | 改：统计产物 |
| scripts/output/stats-changelog.json | W1124 | 改：统计产物 |
| scripts/output/tools-inventory.md | W1124 | 改：工具清单（收官链产物刷新） |
| archive/docs/AGENTS-ARCHIVE.md | W1124 | 改：AGENTS 脚注滚动迁入的最老条目归档件（副作用面） |
| docs/INDEX.md | W1124 | 改：文档索引（索引刷新步产物·副作用面） |
| scripts/INDEX.md | W1124 | 改：脚本索引（索引刷新步产物·副作用面） |
| scripts/output/INDEX.md | W1124 | 改：产物索引（索引刷新步产物·副作用面） |
| scripts/output/README.md | W1124 | 改：产物说明（索引刷新步产物·副作用面） |
| tests/unit/INDEX.md | W1124 | 改：单测索引（索引刷新步产物·副作用面） |
| tests/unit/README.md | W1124 | 改：单测说明（索引刷新步产物·副作用面） |
| pytest.ini | W1124 | 改：统计面 pytest 用例计数（实体化字面量·stats 同步） |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1124 | 改：统计面 pytest 用例计数（实体化字面量·stats 同步） |
| docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md | W1124 | 改：统计面 pytest 用例计数（实体化字面量·stats 同步） |
| site/index.html | W1124 | 改：页脚批次链 token（W1124·副作用面） |
| site/data/cross-time-danmaku.html | W1124 | 改：页脚批次链 token（W1124·副作用面） |
| site/data/tag-cloud.html | W1124 | 改：页脚批次链 token（W1124·副作用面） |
| site/dukou-engine.html | W1124 | 改：页脚批次链 token（W1124·副作用面） |

## W1123 预约释放语义根修 + 提交范围门禁 merge 场景归属根修（2026-11-04）

| 文件 | W | 说明 |
|---|---|---|
| .github/workflows/README.md | W1120 | 本批工具/产物 |
| AGENTS.md | W1120 | 本批工具/产物 |
| CHANGELOG.md | W1120 | 本批工具/产物 |
| CITATION.cff | W1120 | 本批工具/产物 |
| HANDOVER.md | W1120 | 本批工具/产物 |
| README.md | W1120 | 本批工具/产物 |
| STRUCTURE.md | W1120 | 本批工具/产物 |
| archive/docs/AGENTS-ARCHIVE.md | W1120 | 本批工具/产物 |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1120 | 本批工具/产物 |
| docs/00-导读/W批次编号对账表.md | W1120 | 本批工具/产物 |
| docs/00-导读/文档规范.md | W1120 | 本批工具/产物 |
| docs/00-导读/项目说明.md | W1120 | 本批工具/产物 |
| docs/11-方案报告/README.md | W1120 | 本批工具/产物 |
| docs/11-方案报告/计划方案/T68-任务计划执行与经验沉淀报告-2026-11-04.md | W1120 | 本批工具/产物 |
| docs/11-方案报告/计划方案/T72-任务计划执行与经验沉淀报告-2026-11-04.md | W1120 | 本批工具/产物 |
| docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md | W1120 | 本批工具/产物 |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1120 | 本批工具/产物 |
| docs/INDEX.md | W1120 | 本批工具/产物 |
| pytest.ini | W1120 | 本批工具/产物 |
| scripts/INDEX.md | W1120 | 本批工具/产物 |
| scripts/batch_cascade.py | W1120 | 本批工具/产物 |
| scripts/check_doc_size_budget.py | W1120 | 本批工具/产物 |
| scripts/output/INDEX.md | W1120 | 本批工具/产物 |
| scripts/output/README.md | W1120 | 本批工具/产物 |
| scripts/output/_cascade_files_W1120.txt | W1120 | 本批工具/产物 |
| scripts/output/_vermilion_solid_cache.json | W1120 | 本批工具/产物 |
| scripts/output/_w1120_spec.json | W1120 | 本批工具/产物 |
| scripts/output/file-index.md | W1120 | 本批工具/产物 |
| scripts/output/stats-changelog.json | W1120 | 本批工具/产物 |
| scripts/output/stats-index.md | W1120 | 本批工具/产物 |
| scripts/output/stats.json | W1120 | 本批工具/产物 |
| scripts/output/tools-inventory.md | W1120 | 本批工具/产物 |
| scripts/rebuild_section.py | W1120 | 本批工具/产物 |
| site/data/cross-time-danmaku.html | W1120 | 本批工具/产物 |
| site/data/search.html | W1120 | 本批工具/产物 |
| site/data/tag-cloud.html | W1120 | 本批工具/产物 |
| site/dukou-engine.html | W1120 | 本批工具/产物 |
| site/en/search.html | W1120 | 本批工具/产物 |
| site/index.html | W1120 | 本批工具/产物 |
| tests/unit/INDEX.md | W1120 | 本批工具/产物 |
| tests/unit/README.md | W1120 | 本批工具/产物 |
| tests/unit/test_w1120_cascade_file_index_idempotence.py | W1120 | 本批工具/产物 |
| tests/unit/test_w1120_size_threshold_and_rebuild.py | W1120 | 本批工具/产物 |
| .agent/skills/puti-shouye/SKILL.md | W1120 | 本批工具/产物 |
| docs/11-方案报告/计划方案/T71-任务计划执行与经验沉淀报告-2026-11-04.md | W1120 | 本批工具/产物 |
| docs/agent/pitfalls.md | W1120 | 本批工具/产物 |
| scripts/batch_closeout.py | W1120 | 本批工具/产物 |
| scripts/check_registration_surface.py | W1120 | 本批工具/产物 |
| scripts/ledger_backfill.py | W1120 | 本批工具/产物 |
| scripts/output/_cascade_files_W1121.txt | W1120 | 本批工具/产物 |
| scripts/output/_w1121_spec.json | W1120 | 本批工具/产物 |
| scripts/reserve_w.py | W1120 | 本批工具/产物 |
| tests/unit/test_w1121_reserve_w.py | W1120 | 本批工具/产物 |
| scripts/check_commit_scope.py | W1123 | 本批工具/产物 |
| docs/11-方案报告/计划方案/T73-任务计划执行与经验沉淀报告-2026-11-04.md | W1123 | 本批工具/产物 |
| tests/unit/test_w1123_commit_scope_merge.py | W1123 | 本批工具/产物 |
| tests/unit/test_w1123_reserve_release.py | W1123 | 本批工具/产物 |
| scripts/output/_w1123_spec.json | W1123 | 本批工具/产物 |
| scripts/output/_cascade_files_W1123.txt | W1123 | 本批工具/产物 |

## W1122 级联插入型面幂等原语 + 补段工具双面判定根修（2026-11-04）

| 文件 | W | 说明 |
|---|---|---|
| scripts/cascade_idempotence.py | W1122 | 新增：级联插入型面幂等 upsert 原语（单一事实源·不存在⇒插入/一致⇒零变化/不一致⇒替换） |
| scripts/batch_cascade.py | W1122 | 改：六个插入型面接幂等原语（交接头链与里程碑块/AGENTS 脚注/workflows 尾标记/页脚链 token/CHANGELOG 段/file-index 段） |
| scripts/backfill_changelog.py | W1122 | 改：立段判定改双面独立（CHANGELOG 面与 file-index 面分判·只补缺的一面·历史缺口须显式确认才补） |
| tests/unit/test_w1122_cascade_idempotence.py | W1122 | 新增：幂等原语与六面接入自证 19 例 |
| tests/unit/test_w1122_pending_faces.py | W1122 | 新增：双面独立判定自证 5 例 |
| docs/00-导读/W批次编号对账表.md | W1122 | 改：W1120 与 W1121 两行回填 + W1122 认领行登记 |
| docs/11-方案报告/计划方案/T74-任务计划执行与经验沉淀报告-2026-11-04.md | W1122 | 新增：本批任务计划执行与经验沉淀报告 |
| docs/11-方案报告/README.md | W1122 | 改：登记第 89 号 |
| scripts/output/_w1122_spec.json | W1122 | 新增：本批 spec（应动全集单一事实源） |
| scripts/output/_cascade_files_W1122.txt | W1122 | 新增：级联文件清单 |
| CHANGELOG.md | W1122 | 改：W1122 段 |
| scripts/output/file-index.md | W1122 | 改：W1122 段 |
| HANDOVER.md | W1122 | 改：头链 entry 与里程碑块与进度标题与 HEAD 句（幂等） |
| AGENTS.md | W1122 | 改：版本脚注条目（幂等） |
| .github/workflows/README.md | W1122 | 改：里程碑尾标记（幂等） |
| site/index.html | W1122 | 改：页脚批次链 token（幂等） |
| site/data/cross-time-danmaku.html | W1122 | 改：页脚批次链 token（幂等） |
| site/data/tag-cloud.html | W1122 | 改：页脚批次链 token（幂等） |
| site/dukou-engine.html | W1122 | 改：页脚批次链 token（幂等） |
| README.md | W1122 | 改：版本行（幂等推进） |
| STRUCTURE.md | W1122 | 改：版本行（幂等推进） |
| docs/00-导读/项目说明.md | W1122 | 改：版本行（幂等推进） |
| CITATION.cff | W1122 | 改：版本与日期（幂等推进） |
| scripts/output/tools-inventory.md | W1122 | 改：工具清单（新增模块入册） |
| scripts/output/stats.json | W1122 | 改：统计产物 |
| scripts/output/stats-index.md | W1122 | 改：统计产物 |
| scripts/output/stats-changelog.json | W1122 | 改：统计产物 |
| archive/docs/AGENTS-ARCHIVE.md | W1122 | 改：AGENTS 脚注滚动迁入的最老条目归档件（级联副作用面） |
| pytest.ini | W1122 | 改：统计面 pytest 用例计数（实体化字面量·stats 同步） |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1122 | 改：统计面 pytest 用例计数（实体化字面量·stats 同步） |
| docs/INDEX.md | W1122 | 改：文档索引（级联/索引刷新步产物·副作用面） |
| scripts/INDEX.md | W1122 | 改：脚本索引（级联/索引刷新步产物·副作用面） |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1122 | 改：台账腾窗迁出的最老行（收官链 archive 步产物·副作用面） |
| docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md | W1122 | 改：统计面 pytest 用例计数（实体化字面量·stats 同步） |
| site/data/search.html | W1122 | 改：版本面字面量（搜索页版本行·幂等推进·副作用面） |
| site/en/search.html | W1122 | 改：版本面字面量（搜索页版本行·幂等推进·副作用面） |
| scripts/output/INDEX.md | W1122 | 改：产物索引（索引刷新步产物·副作用面） |
| scripts/output/README.md | W1122 | 改：产物说明（索引刷新步产物·副作用面） |
| tests/unit/INDEX.md | W1122 | 改：单测索引（索引刷新步产物·副作用面） |
| tests/unit/README.md | W1122 | 改：单测说明（索引刷新步产物·副作用面） |


## W1121 收官链缺陷根修 + 跨克隆占号机制根修 + 台账回填（2026-11-04）

| 文件 | W | 说明 |
|---|---|---|
| .github/workflows/README.md | W1121 | 本批工具/产物 |
| CHANGELOG.md | W1121 | 本批工具/产物 |
| CITATION.cff | W1121 | 本批工具/产物 |
| HANDOVER.md | W1121 | 本批工具/产物 |
| README.md | W1121 | 本批工具/产物 |
| STRUCTURE.md | W1121 | 本批工具/产物 |
| .agent/skills/puti-shouye/SKILL.md | W1121 | 本批工具/产物 |
| AGENTS.md | W1121 | 本批工具/产物 |
| archive/docs/CHANGELOG-ARCHIVE.md | W1121 | 本批工具/产物 |
| archive/docs/file-index-ARCHIVE.md | W1121 | 本批工具/产物 |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1121 | 本批工具/产物 |
| docs/00-导读/W批次编号对账表.md | W1121 | 本批工具/产物 |
| docs/00-导读/项目说明.md | W1121 | 本批工具/产物 |
| docs/11-方案报告/README.md | W1121 | 本批工具/产物 |
| docs/11-方案报告/计划方案/T71-任务计划执行与经验沉淀报告-2026-11-04.md | W1121 | 本批工具/产物 |
| docs/agent/pitfalls.md | W1121 | 本批工具/产物 |
| docs/INDEX.md | W1121 | 本批工具/产物 |
| scripts/INDEX.md | W1121 | 本批工具/产物 |
| scripts/batch_closeout.py | W1121 | 本批工具/产物 |
| scripts/check_registration_surface.py | W1121 | 本批工具/产物 |
| scripts/ledger_backfill.py | W1121 | 本批工具/产物 |
| scripts/reserve_w.py | W1121 | 本批工具/产物 |
| scripts/output/INDEX.md | W1121 | 本批工具/产物 |
| scripts/output/README.md | W1121 | 本批工具/产物 |
| scripts/output/_w1121_spec.json | W1121 | 本批工具/产物 |
| scripts/output/file-index.md | W1121 | 本批工具/产物 |
| scripts/output/stats-changelog.json | W1121 | 本批工具/产物 |
| scripts/output/stats-index.md | W1121 | 本批工具/产物 |
| scripts/output/stats.json | W1121 | 本批工具/产物 |
| scripts/output/tools-inventory.md | W1121 | 本批工具/产物 |
| scripts/output/_cascade_files_W1121.txt | W1121 | 本批工具/产物 |
| scripts/output/_vermilion_solid_cache.json | W1121 | 本批工具/产物 |
| site/data/search.html | W1121 | 本批工具/产物 |
| site/en/search.html | W1121 | 本批工具/产物 |
| tests/unit/INDEX.md | W1121 | 本批工具/产物 |
| tests/unit/README.md | W1121 | 本批工具/产物 |
| tests/unit/test_w1121_reserve_w.py | W1121 | 本批工具/产物 |
| archive/docs/AGENTS-ARCHIVE.md | W1121 | 本批工具/产物 |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1121 | 本批工具/产物 |
| pytest.ini | W1121 | 本批工具/产物 |
| site/data/cross-time-danmaku.html | W1121 | 本批工具/产物 |
| site/data/tag-cloud.html | W1121 | 本批工具/产物 |
| site/dukou-engine.html | W1121 | 本批工具/产物 |
| site/index.html | W1121 | 本批工具/产物 |
| docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md | W1121 | 本批工具/产物 |
## W1120 幂等段重建独立入口 + 体积第二阈值接入 + T68 事实订正（2026-11-04）

| 文件 | W | 说明 |
|---|---|---|
| .github/workflows/README.md | W1120 | 本批工具/产物 |
| AGENTS.md | W1120 | 本批工具/产物 |
| CHANGELOG.md | W1120 | 本批工具/产物 |
| CITATION.cff | W1120 | 本批工具/产物 |
| HANDOVER.md | W1120 | 本批工具/产物 |
| README.md | W1120 | 本批工具/产物 |
| STRUCTURE.md | W1120 | 本批工具/产物 |
| archive/docs/AGENTS-ARCHIVE.md | W1120 | 本批工具/产物 |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1120 | 本批工具/产物 |
| docs/00-导读/W批次编号对账表.md | W1120 | 本批工具/产物 |
| docs/00-导读/文档规范.md | W1120 | 本批工具/产物 |
| docs/00-导读/项目说明.md | W1120 | 本批工具/产物 |
| docs/11-方案报告/README.md | W1120 | 本批工具/产物 |
| docs/11-方案报告/计划方案/T68-任务计划执行与经验沉淀报告-2026-11-04.md | W1120 | 本批工具/产物 |
| docs/11-方案报告/计划方案/T72-任务计划执行与经验沉淀报告-2026-11-04.md | W1120 | 本批工具/产物 |
| docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md | W1120 | 本批工具/产物 |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1120 | 本批工具/产物 |
| docs/INDEX.md | W1120 | 本批工具/产物 |
| pytest.ini | W1120 | 本批工具/产物 |
| scripts/INDEX.md | W1120 | 本批工具/产物 |
| scripts/batch_cascade.py | W1120 | 本批工具/产物 |
| scripts/check_doc_size_budget.py | W1120 | 本批工具/产物 |
| scripts/output/INDEX.md | W1120 | 本批工具/产物 |
| scripts/output/README.md | W1120 | 本批工具/产物 |
| scripts/output/_cascade_files_W1120.txt | W1120 | 本批工具/产物 |
| scripts/output/_vermilion_solid_cache.json | W1120 | 本批工具/产物 |
| scripts/output/_w1120_spec.json | W1120 | 本批工具/产物 |
| scripts/output/file-index.md | W1120 | 本批工具/产物 |
| scripts/output/stats-changelog.json | W1120 | 本批工具/产物 |
| scripts/output/stats-index.md | W1120 | 本批工具/产物 |
| scripts/output/stats.json | W1120 | 本批工具/产物 |
| scripts/output/tools-inventory.md | W1120 | 本批工具/产物 |
| scripts/rebuild_section.py | W1120 | 本批工具/产物 |
| site/data/cross-time-danmaku.html | W1120 | 本批工具/产物 |
| site/data/search.html | W1120 | 本批工具/产物 |
| site/data/tag-cloud.html | W1120 | 本批工具/产物 |
| site/dukou-engine.html | W1120 | 本批工具/产物 |
| site/en/search.html | W1120 | 本批工具/产物 |
| site/index.html | W1120 | 本批工具/产物 |
| tests/unit/INDEX.md | W1120 | 本批工具/产物 |
| tests/unit/README.md | W1120 | 本批工具/产物 |
| tests/unit/test_w1120_cascade_file_index_idempotence.py | W1120 | 本批工具/产物 |
| tests/unit/test_w1120_size_threshold_and_rebuild.py | W1120 | 本批工具/产物 |
| .agent/skills/puti-shouye/SKILL.md | W1120 | 本批工具/产物 |
| docs/11-方案报告/计划方案/T71-任务计划执行与经验沉淀报告-2026-11-04.md | W1120 | 本批工具/产物 |
| docs/agent/pitfalls.md | W1120 | 本批工具/产物 |
| scripts/batch_closeout.py | W1120 | 本批工具/产物 |
| scripts/check_registration_surface.py | W1120 | 本批工具/产物 |
| scripts/ledger_backfill.py | W1120 | 本批工具/产物 |
| scripts/output/_cascade_files_W1121.txt | W1120 | 本批工具/产物 |
| scripts/output/_w1121_spec.json | W1120 | 本批工具/产物 |
| scripts/reserve_w.py | W1120 | 本批工具/产物 |
| tests/unit/test_w1121_reserve_w.py | W1120 | 本批工具/产物 |


## W1119 CI 成本治理 + 档 3 第二批 + 归档规则工具化（2026-11-04）

| 文件 | W | 说明 |
|---|---|---|
| .github/workflows/README.md | W1119 | 本批工具/产物 |
| CHANGELOG.md | W1119 | 本批工具/产物 |
| CITATION.cff | W1119 | 本批工具/产物 |
| HANDOVER.md | W1119 | 本批工具/产物 |
| README.md | W1119 | 本批工具/产物 |
| STRUCTURE.md | W1119 | 本批工具/产物 |
| .agent/skills/puti-shouye/SKILL.md | W1119 | 本批工具/产物 |
| AGENTS.md | W1119 | 本批工具/产物 |
| .github/workflows/perf.yml | W1119 | 本批工具/产物 |
| .github/workflows/screenshot-review.yml | W1119 | 本批工具/产物 |
| archive/docs/CHANGELOG-ARCHIVE.md | W1119 | 本批工具/产物 |
| archive/docs/file-index-ARCHIVE.md | W1119 | 本批工具/产物 |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1119 | 本批工具/产物 |
| docs/00-导读/W批次编号对账表.md | W1119 | 本批工具/产物 |
| docs/00-导读/项目说明.md | W1119 | 本批工具/产物 |
| docs/11-方案报告/README.md | W1119 | 本批工具/产物 |
| docs/11-方案报告/计划方案/T70-任务计划执行与经验沉淀报告-2026-11-04.md | W1119 | 本批工具/产物 |
| docs/agent/pitfalls.md | W1119 | 本批工具/产物 |
| docs/INDEX.md | W1119 | 本批工具/产物 |
| scripts/INDEX.md | W1119 | 本批工具/产物 |
| scripts/archive_segments.py | W1119 | 本批工具/产物 |
| scripts/batch_closeout.py | W1119 | 本批工具/产物 |
| scripts/output/INDEX.md | W1119 | 本批工具/产物 |
| scripts/output/README.md | W1119 | 本批工具/产物 |
| scripts/output/_w1118_spec.json | W1119 | 本批工具/产物 |
| scripts/output/file-index.md | W1119 | 本批工具/产物 |
| scripts/output/stats-changelog.json | W1119 | 本批工具/产物 |
| scripts/output/stats-index.md | W1119 | 本批工具/产物 |
| scripts/output/stats.json | W1119 | 本批工具/产物 |
| scripts/output/tools-inventory.md | W1119 | 本批工具/产物 |
| scripts/output/_cascade_files_W1118.txt | W1119 | 本批工具/产物 |
| site/data/relationships.html | W1119 | 本批工具/产物 |
| site/en/relationships.html | W1119 | 本批工具/产物 |
| site/data/narrative-experiment.html | W1119 | 本批工具/产物 |
| site/en/narrative-experiment.html | W1119 | 本批工具/产物 |
| site/data/jurisprudence.html | W1119 | 本批工具/产物 |
| site/en/jurisprudence.html | W1119 | 本批工具/产物 |
| tests/unit/test_w1102_batch_closeout.py | W1119 | 本批工具/产物 |
| tests/unit/test_w1114_version_surface.py | W1119 | 本批工具/产物 |

## W1118 CI 成本治理与经验同步入仓（2026-11-04）

| 文件 | W | 说明 |
|---|---|---|
| .github/workflows/screenshot-review.yml | W1118 | 本批 CI 触发面根修 |
| .github/workflows/perf.yml | W1118 | 本批 CI 触发面根修 |
| .github/workflows/README.md | W1118 | 本批工具/产物 |
| docs/agent/pitfalls.md | W1118 | 本批坑表新增 E-141 ~ E-153 |
| AGENTS.md | W1118 | 本批纪律增行 |
| HANDOVER.md | W1118 | 本批工具/产物 |
| .agent/skills/puti-shouye/SKILL.md | W1118 | 本批计数链同步 |
| docs/00-导读/W批次编号对账表.md | W1118 | 本批认领登记行 |
| docs/00-导读/项目说明.md | W1118 | 本批工具/产物 |
| docs/11-方案报告/README.md | W1118 | 本批登记行 |
| docs/11-方案报告/计划方案/T69-任务计划执行与经验沉淀报告-2026-11-04.md | W1118 | 本批交付报告 |
| scripts/output/_w1118_spec.json | W1118 | 本批 spec |
| CHANGELOG.md | W1118 | 本批版段 |
| README.md | W1118 | 本批工具/产物 |
| STRUCTURE.md | W1118 | 本批工具/产物 |
| CITATION.cff | W1118 | 本批工具/产物 |
| docs/INDEX.md | W1118 | 本批工具/产物 |
| scripts/INDEX.md | W1118 | 本批工具/产物 |
| scripts/output/INDEX.md | W1118 | 本批工具/产物 |
| scripts/output/README.md | W1118 | 本批工具/产物 |
| scripts/output/file-index.md | W1118 | 本批工具/产物 |
| scripts/output/stats.json | W1118 | 本批工具/产物 |
| scripts/output/stats-index.md | W1118 | 本批工具/产物 |
| scripts/output/stats-changelog.json | W1118 | 本批工具/产物 |
| scripts/output/tools-inventory.md | W1118 | 本批工具/产物 |
| site/data/search.html | W1118 | 本批工具/产物 |
| site/en/search.html | W1118 | 本批工具/产物 |

## W1117 版本面幂等修复与编号规则并入版本面（2026-11-04）

| 文件 | W | 说明 |
|---|---|---|
| CHANGELOG.md | W1117 | 本批版段 + 编号规则段上限（只升不降） |
| STRUCTURE.md | W1117 | 本批生成物（报告类文档计数标记 137 -> 138） |
| archive/docs/CHANGELOG-ARCHIVE.md | W1117 | 本批段面腾窗迁出段（W995） |
| archive/docs/file-index-ARCHIVE.md | W1117 | 本批段面腾窗迁出段（W995） |
| docs/00-导读/W批次编号对账表.md | W1117 | 本批认领登记行 |
| docs/11-方案报告/README.md | W1117 | 本批登记行 |
| docs/11-方案报告/计划方案/T65-任务计划执行与经验沉淀报告-2026-11-03.md | W1117 | 本批 §2.6 订正小节 |
| docs/11-方案报告/计划方案/T68-任务计划执行与经验沉淀报告-2026-11-04.md | W1117 | 本批交付报告 |
| docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md | W1117 | 本批生成物（报告类文档计数标记） |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1117 | 本批生成物（报告类文档计数标记） |
| docs/INDEX.md | W1117 | 本批生成物（文档索引） |
| pytest.ini | W1117 | 本批生成物（pytest collected 标记对账） |
| scripts/backfill_changelog.py | W1117 | 本批工具改动（完整性检查移到已立段判定之后 + 坏件容错） |
| scripts/batch_cascade.py | W1117 | 本批工具改动（级联改调共享实现） |
| scripts/batch_closeout.py | W1117 | 本批工具改动（index 步后置 + 内容阶段抽取） |
| scripts/check_commit_scope.py | W1117 | 本批工具改动（归属判定支持新增段非顶位） |
| scripts/output/INDEX.md | W1117 | 本批生成物（脚本索引） |
| scripts/output/README.md | W1117 | 本批生成物（脚本目录索引） |
| scripts/output/_w1117_spec.json | W1117 | 本批 spec |
| scripts/output/file-index.md | W1117 | 本批 file-index 段 + 段面腾窗 |
| scripts/output/stats-changelog.json | W1117 | 本批生成物（统计） |
| scripts/output/_vermilion_solid_cache.json | W1117 | 本批生成物（朱砂实底扫描缓存·搜索页变更后刷新） |
| scripts/output/stats-index.md | W1117 | 本批生成物（统计） |
| scripts/output/stats.json | W1117 | 本批生成物（统计） |
| scripts/output/tools-inventory.md | W1117 | 本批生成物（工具清单） |
| scripts/version_surface.py | W1117 | 本批工具改动（幂等 + 批次级单调守卫） |
| site/data/search.html | W1117 | 本批生成物（搜索索引） |
| site/en/search.html | W1117 | 本批生成物（搜索索引） |
| tests/unit/INDEX.md | W1117 | 本批生成物（测试索引） |
| tests/unit/README.md | W1117 | 本批生成物（测试目录索引） |
| tests/unit/test_commit_scope.py | W1117 | 本批归属判定新例（追加·未改他人既有断言） |
| tests/unit/test_w1102_batch_closeout.py | W1117 | 本批行为锁更新 |
| tests/unit/test_w1117_version_surface_idempotence.py | W1117 | 本批新增自证 9 例 |

## W1116 收官链自检闸（2026-11-04）

| 文件 | W | 说明 |
|---|---|---|
| scripts/check_doc_numbers.py | W1116 | 本批工具/产物 |
| docs/00-导读/项目说明.md | W1116 | 本批工具/产物 |
| .github/workflows/README.md | W1116 | 本批工具/产物 |
| CITATION.cff | W1116 | 本批工具/产物 |
| STRUCTURE.md | W1116 | 本批工具/产物 |
| README.md | W1116 | 本批工具/产物 |
| scripts/check_registration_surface.py | W1116 | 本批工具/产物 |
| scripts/batch_closeout.py | W1116 | 本批工具/产物 |
| tests/unit/test_w1116_selfcheck_gates.py | W1116 | 本批工具/产物 |
| tests/unit/test_w1114_version_surface.py | W1116 | 本批工具/产物 |
| pytest.ini | W1116 | 本批工具/产物 |
| CHANGELOG.md | W1116 | 本批工具/产物 |
| docs/00-导读/W批次编号对账表.md | W1116 | 本批工具/产物 |
| docs/11-方案报告/README.md | W1116 | 本批工具/产物 |
| docs/11-方案报告/计划方案/T67-任务计划执行与经验沉淀报告-2026-11-04.md | W1116 | 本批工具/产物 |
| scripts/output/_w1116_spec.json | W1116 | 本批工具/产物 |
| docs/INDEX.md | W1116 | 本批工具/产物 |
| scripts/output/stats.json | W1116 | 本批工具/产物 |
| scripts/output/stats-index.md | W1116 | 本批工具/产物 |
| scripts/output/stats-changelog.json | W1116 | 本批工具/产物 |
| scripts/output/tools-inventory.md | W1116 | 本批工具/产物 |
| scripts/output/file-index.md | W1116 | 本批工具/产物 |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1116 | 本批工具/产物 |
| archive/docs/CHANGELOG-ARCHIVE.md | W1116 | 本批工具/产物 |
| archive/docs/file-index-ARCHIVE.md | W1116 | 本批工具/产物 |

## W1115 图表色工程批收官订正批（2026-11-03）

| 文件 | W | 说明 |
|---|---|---|
| .github/workflows/README.md | W1115 | 本批工具/产物 |
| CITATION.cff | W1115 | 本批工具/产物 |
| CHANGELOG.md | W1115 | 本批工具/产物 |
| HANDOVER.md | W1115 | 本批工具/产物 |
| README.md | W1115 | 本批工具/产物 |
| STRUCTURE.md | W1115 | 本批工具/产物 |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1115 | 本批工具/产物 |
| docs/00-导读/W批次编号对账表.md | W1115 | 本批工具/产物 |
| docs/00-导读/项目说明.md | W1115 | 本批工具/产物 |
| docs/11-方案报告/README.md | W1115 | 本批工具/产物 |
| docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md | W1115 | 本批工具/产物 |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1115 | 本批工具/产物 |
| docs/11-方案报告/计划方案/T64-任务计划执行与经验沉淀报告-2026-11-03.md | W1115 | 本批工具/产物 |
| docs/11-方案报告/计划方案/T66-任务计划执行与经验沉淀报告-2026-11-03.md | W1115 | 本批工具/产物 |
| docs/INDEX.md | W1115 | 本批工具/产物 |
| scripts/output/INDEX.md | W1115 | 本批工具/产物 |
| scripts/output/README.md | W1115 | 本批工具/产物 |
| scripts/output/_w1115_spec.json | W1115 | 本批工具/产物 |
| scripts/output/file-index.md | W1115 | 本批工具/产物 |
| scripts/output/stats-changelog.json | W1115 | 本批工具/产物 |
| scripts/output/stats-index.md | W1115 | 本批工具/产物 |
| scripts/output/stats.json | W1115 | 本批工具/产物 |
| scripts/output/tools-inventory.md | W1115 | 本批工具/产物 |
| site/data/search.html | W1115 | 本批工具/产物 |
| site/en/search.html | W1115 | 本批工具/产物 |

## W1114 落段收官链加版本面幂等推进步（2026-11-03）

| 文件 | W | 说明 |
|---|---|---|
| scripts/version_surface.py | W1114 | 本批工具/产物 |
| scripts/batch_cascade.py | W1114 | 本批工具/产物 |
| scripts/batch_closeout.py | W1114 | 本批工具/产物 |
| tests/unit/test_w1114_version_surface.py | W1114 | 本批工具/产物 |
| tests/unit/test_w1102_batch_closeout.py | W1114 | 本批工具/产物 |
| scripts/output/_w1114_spec.json | W1114 | 本批工具/产物 |
| scripts/output/_cascade_files_W1114.txt | W1114 | 本批工具/产物 |
| CHANGELOG.md | W1114 | 本批工具/产物 |
| README.md | W1114 | 本批工具/产物 |
| STRUCTURE.md | W1114 | 本批工具/产物 |
| docs/00-导读/项目说明.md | W1114 | 本批工具/产物 |
| HANDOVER.md | W1114 | 本批工具/产物 |
| AGENTS.md | W1114 | 本批工具/产物 |
| CITATION.cff | W1114 | 本批工具/产物 |
| .github/workflows/README.md | W1114 | 本批工具/产物 |
| scripts/output/file-index.md | W1114 | 本批工具/产物 |
| site/index.html | W1114 | 本批工具/产物 |
| site/data/cross-time-danmaku.html | W1114 | 本批工具/产物 |
| site/data/tag-cloud.html | W1114 | 本批工具/产物 |
| site/dukou-engine.html | W1114 | 本批工具/产物 |
| archive/docs/AGENTS-ARCHIVE.md | W1114 | 本批工具/产物 |
| archive/docs/CHANGELOG-ARCHIVE.md | W1114 | 本批工具/产物 |
| archive/docs/file-index-ARCHIVE.md | W1114 | 本批工具/产物 |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1114 | 本批工具/产物 |
| docs/00-导读/W批次编号对账表.md | W1114 | 本批工具/产物 |
| docs/11-方案报告/README.md | W1114 | 本批工具/产物 |
| docs/11-方案报告/计划方案/T65-任务计划执行与经验沉淀报告-2026-11-03.md | W1114 | 本批工具/产物 |
| scripts/output/stats-changelog.json | W1114 | 本批工具/产物 |
| scripts/output/stats-index.md | W1114 | 本批工具/产物 |
| scripts/output/stats.json | W1114 | 本批工具/产物 |
| scripts/output/tools-inventory.md | W1114 | 本批工具/产物 |
| scripts/output/INDEX.md | W1114 | 本批工具/产物 |
| scripts/output/README.md | W1114 | 本批工具/产物 |
| scripts/output/_vermilion_solid_cache.json | W1114 | 本批工具/产物 |
| site/data/search.html | W1114 | 本批工具/产物 |
| site/en/search.html | W1114 | 本批工具/产物 |
| docs/INDEX.md | W1114 | 本批工具/产物 |
| scripts/INDEX.md | W1114 | 本批工具/产物 |
| tests/unit/INDEX.md | W1114 | 本批工具/产物 |
| tests/unit/README.md | W1114 | 本批工具/产物 |
| pytest.ini | W1114 | 本批工具/产物 |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1114 | 本批工具/产物 |
| docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md | W1114 | 本批工具/产物 |

## W1113 图表色工程档 3 铺开第一批（2026-11-03）
| 文件 | W | 说明 |
|---|---|---|
| site/data/character-sentiment-arc.html | W1113 | 本批工具/产物 |
| site/en/character-sentiment-arc.html | W1113 | 本批工具/产物 |
| site/data/concept-device.html | W1113 | 本批工具/产物 |
| site/en/concept-device.html | W1113 | 本批工具/产物 |
| site/data/monster-victims-network.html | W1113 | 本批工具/产物 |
| site/en/monster-victims-network.html | W1113 | 本批工具/产物 |
| docs/agent/pitfalls.md | W1113 | 本批工具/产物 |
| docs/11-方案报告/计划方案/T64-任务计划执行与经验沉淀报告-2026-11-03.md | W1113 | 本批工具/产物 |
| scripts/output/_w1113_spec.json | W1113 | 本批工具/产物 |
| scripts/output/_w1113_delta.json | W1113 | 本批工具/产物 |
| STRUCTURE.md | W1113 | 本批工具/产物 |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1113 | 本批工具/产物 |
| docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md | W1113 | 本批工具/产物 |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1113 | 本批工具/产物 |
| scripts/output/stats-changelog.json | W1113 | 本批工具/产物 |
| scripts/output/stats-index.md | W1113 | 本批工具/产物 |
| scripts/output/stats.json | W1113 | 本批工具/产物 |
| dataset/concept-device.json | W1113 | 本批工具/产物 |
| dataset/monster-victims-network.json | W1113 | 本批工具/产物 |
| docs/INDEX.md | W1113 | 本批工具/产物 |
| scripts/output/INDEX.md | W1113 | 本批工具/产物 |
| scripts/output/README.md | W1113 | 本批工具/产物 |
| scripts/output/tools-inventory.md | W1113 | 本批工具/产物 |
| site/data/search.html | W1113 | 本批工具/产物 |
| site/en/search.html | W1113 | 本批工具/产物 |
| .agent/skills/puti-shouye/SKILL.md | W1113 | 本批工具/产物 |
| .github/workflows/README.md | W1113 | 本批工具/产物 |
| AGENTS.md | W1113 | 本批工具/产物 |
| CHANGELOG.md | W1113 | 本批工具/产物 |
| CITATION.cff | W1113 | 本批工具/产物 |
| HANDOVER.md | W1113 | 本批工具/产物 |
| README.md | W1113 | 本批工具/产物 |
| archive/docs/AGENTS-ARCHIVE.md | W1113 | 本批工具/产物 |
| docs/00-导读/W批次编号对账表.md | W1113 | 本批工具/产物 |
| docs/00-导读/项目说明.md | W1113 | 本批工具/产物 |
| docs/11-方案报告/README.md | W1113 | 本批工具/产物 |
| scripts/output/_cascade_files_W1113.txt | W1113 | 本批工具/产物 |
| scripts/output/_vermilion_solid_cache.json | W1113 | 本批工具/产物 |
| scripts/output/file-index.md | W1113 | 本批工具/产物 |
| site/data/cross-time-danmaku.html | W1113 | 本批工具/产物 |
| site/data/tag-cloud.html | W1113 | 本批工具/产物 |
| site/dukou-engine.html | W1113 | 本批工具/产物 |
| site/index.html | W1113 | 本批工具/产物 |
| archive/docs/CHANGELOG-ARCHIVE.md | W1113 | 本批工具/产物 |
| archive/docs/file-index-ARCHIVE.md | W1113 | 本批工具/产物 |
| archive/scripts/batches/w1100/_w1100_layer3_pages.py | W1113 | 本批工具/产物 |
| scripts/visual_regression_probe.py | W1113 | 本批工具/产物 |
| tests/unit/test_w851_visual_regression_probe.py | W1113 | 本批工具/产物 |

## W1112 落段收官一键脚本（2026-11-03）
| 文件 | W | 说明 |
|---|---|---|
| .github/workflows/README.md | W1112 | 本批工具/产物 |
| AGENTS.md | W1112 | 本批工具/产物 |
| CHANGELOG.md | W1112 | 本批工具/产物 |
| CITATION.cff | W1112 | 本批工具/产物 |
| HANDOVER.md | W1112 | 本批工具/产物 |
| README.md | W1112 | 本批工具/产物 |
| STRUCTURE.md | W1112 | 本批工具/产物 |
| archive/docs/AGENTS-ARCHIVE.md | W1112 | 本批工具/产物 |
| archive/docs/CHANGELOG-ARCHIVE.md | W1112 | 本批工具/产物 |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1112 | 本批工具/产物 |
| archive/docs/file-index-ARCHIVE.md | W1112 | 本批工具/产物 |
| docs/00-导读/W批次编号对账表.md | W1112 | 本批工具/产物 |
| docs/00-导读/项目说明.md | W1112 | 本批工具/产物 |
| docs/11-方案报告/README.md | W1112 | 本批工具/产物 |
| docs/11-方案报告/计划方案/T63-任务计划执行与经验沉淀报告-2026-11-03.md | W1112 | 本批工具/产物 |
| docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md | W1112 | 本批工具/产物 |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1112 | 本批工具/产物 |
| docs/INDEX.md | W1112 | 本批工具/产物 |
| pytest.ini | W1112 | 本批工具/产物 |
| scripts/INDEX.md | W1112 | 本批工具/产物 |
| scripts/batch_closeout.py | W1112 | 本批工具/产物 |
| scripts/output/INDEX.md | W1112 | 本批工具/产物 |
| scripts/output/README.md | W1112 | 本批工具/产物 |
| scripts/output/_cascade_files_W1112.txt | W1112 | 本批工具/产物 |
| scripts/output/_vermilion_solid_cache.json | W1112 | 本批工具/产物 |
| scripts/output/_w1106_spec.json | W1112 | 本批工具/产物 |
| scripts/output/_w1112_spec.json | W1112 | 本批工具/产物 |
| scripts/output/file-index.md | W1112 | 本批工具/产物 |
| scripts/output/stats-changelog.json | W1112 | 本批工具/产物 |
| scripts/output/stats-index.md | W1112 | 本批工具/产物 |
| scripts/output/stats.json | W1112 | 本批工具/产物 |
| scripts/output/tools-inventory.md | W1112 | 本批工具/产物 |
| site/data/cross-time-danmaku.html | W1112 | 本批工具/产物 |
| site/data/search.html | W1112 | 本批工具/产物 |
| site/data/tag-cloud.html | W1112 | 本批工具/产物 |
| site/dukou-engine.html | W1112 | 本批工具/产物 |
| site/en/search.html | W1112 | 本批工具/产物 |
| site/index.html | W1112 | 本批工具/产物 |
| tests/unit/INDEX.md | W1112 | 本批工具/产物 |
| tests/unit/README.md | W1112 | 本批工具/产物 |
| tests/unit/test_w1102_batch_closeout.py | W1112 | 本批工具/产物 |
| tests/unit/test_w1112_judge_fix.py | W1112 | 本批工具/产物 |

## W1110 图表色工程档 3 施工前置批（2026-11-03）

| 文件 | W | 说明 |
|---|---|---|
| scripts/verify_delivery.py | W1110 | 本批工具/产物 |
| scripts/check_powershell_parse.py | W1110 | 本批工具/产物 |
| scripts/check_csp_drift.py | W1110 | 本批工具/产物 |
| scripts/check_css_var_selfref.py | W1110 | 本批工具/产物 |
| scripts/check_pitfall_id_unique.py | W1110 | 本批工具/产物 |
| scripts/doc_areas.py | W1110 | 本批工具/产物 |
| scripts/check_doc_sync.py | W1110 | 本批工具/产物 |
| scripts/agent_start.py | W1110 | 本批工具/产物 |
| site/data/chart-design.html | W1110 | 本批工具/产物 |
| site/en/chart-design.html | W1110 | 本批工具/产物 |
| scripts/guardrails/check_changed.ps1 | W1110 | 本批工具/产物 |
| scripts/install_hooks.ps1 | W1110 | 本批工具/产物 |
| xiyouji-agent-web/cleanup.ps1 | W1110 | 本批工具/产物 |
| docs/agent/gates.md | W1110 | 本批工具/产物 |
| docs/agent/pitfalls.md | W1110 | 本批工具/产物 |
| AGENTS.md | W1110 | 本批工具/产物 |
| HANDOVER.md | W1110 | 本批工具/产物 |
| .agent/skills/puti-shouye/SKILL.md | W1110 | 本批工具/产物 |
| docs/00-导读/W批次编号对账表.md | W1110 | 本批工具/产物 |
| docs/11-方案报告/README.md | W1110 | 本批工具/产物 |
| docs/11-方案报告/计划方案/T62-任务计划执行与经验沉淀报告-2026-11-03.md | W1110 | 本批工具/产物 |
| scripts/output/_w1110_spec.json | W1110 | 本批工具/产物 |
| scripts/output/_w1110_w1108_delta.json | W1110 | 本批工具/产物 |
| scripts/output/stats.json | W1110 | 本批工具/产物 |
| scripts/output/stats-changelog.json | W1110 | 本批工具/产物 |
| scripts/output/stats-index.md | W1110 | 本批工具/产物 |
| scripts/output/file-index.md | W1110 | 本批工具/产物 |
| CHANGELOG.md | W1110 | 本批工具/产物 |
| README.md | W1110 | 本批工具/产物 |
| README.en.md | W1110 | 本批工具/产物 |
| STRUCTURE.md | W1110 | 本批工具/产物 |
| CITATION.cff | W1110 | 本批工具/产物 |
| docs/00-导读/项目说明.md | W1110 | 本批工具/产物 |
| .github/workflows/README.md | W1110 | 本批工具/产物 |
| scripts/output/_cascade_files_W1110.txt | W1110 | 本批工具/产物 |

## W1109 坑表编号重号收敛（2026-11-03）

| 文件 | W | 说明 |
|---|---|---|
| .github/workflows/README.md | W1109 | governance-or-doc |
| AGENTS.md | W1109 | governance-or-doc |
| CHANGELOG.md | W1109 | governance-or-doc |
| CITATION.cff | W1109 | governance-or-doc |
| HANDOVER.md | W1109 | governance-or-doc |
| README.md | W1109 | governance-or-doc |
| STRUCTURE.md | W1109 | governance-or-doc |
| archive/docs/AGENTS-ARCHIVE.md | W1109 | governance-or-doc |
| archive/docs/CHANGELOG-ARCHIVE.md | W1109 | governance-or-doc |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1109 | governance-or-doc |
| archive/docs/file-index-ARCHIVE.md | W1109 | governance-or-doc |
| docs/00-导读/W批次编号对账表.md | W1109 | governance-or-doc |
| docs/00-导读/项目说明.md | W1109 | governance-or-doc |
| docs/agent/pitfalls.md | W1109 | governance-or-doc |
| scripts/output/_vermilion_solid_cache.json | W1109 | tool |
| scripts/output/_vermilion_solid_report.json | W1109 | tool |
| scripts/output/file-index.md | W1109 | tool |
| scripts/output/stats.json | W1109 | tool |
| site/data/cross-time-danmaku.html | W1109 | governance-or-doc |
| site/data/tag-cloud.html | W1109 | governance-or-doc |
| site/dukou-engine.html | W1109 | governance-or-doc |
| site/index.html | W1109 | governance-or-doc |
| scripts/output/_cascade_files_W1109.txt | W1109 | tool |
| scripts/output/_w1109_spec.json | W1109 | tool |

## W1108 图表色工程批·档 3 原型验证批（2026-11-03）

| 文件 | W | 说明 |
|---|---|---|
| .agent/skills/puti-shouye/SKILL.md | W1108 | 本批工具/产物 |
| .github/workflows/README.md | W1108 | 本批工具/产物 |
| AGENTS.md | W1108 | 本批工具/产物 |
| CHANGELOG.md | W1108 | 本批工具/产物 |
| CITATION.cff | W1108 | 本批工具/产物 |
| HANDOVER.md | W1108 | 本批工具/产物 |
| README.md | W1108 | 本批工具/产物 |
| STRUCTURE.md | W1108 | 本批工具/产物 |
| archive/docs/AGENTS-ARCHIVE.md | W1108 | 本批工具/产物 |
| archive/docs/CHANGELOG-ARCHIVE.md | W1108 | 本批工具/产物 |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1108 | 本批工具/产物 |
| archive/docs/file-index-ARCHIVE.md | W1108 | 本批工具/产物 |
| docs/00-导读/W批次编号对账表.md | W1108 | 本批工具/产物 |
| docs/00-导读/项目说明.md | W1108 | 本批工具/产物 |
| docs/11-方案报告/README.md | W1108 | 本批工具/产物 |
| docs/11-方案报告/计划方案/T60-任务计划执行与经验沉淀报告-2026-11-03.md | W1108 | 本批工具/产物 |
| docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md | W1108 | 本批工具/产物 |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1108 | 本批工具/产物 |
| docs/INDEX.md | W1108 | 本批工具/产物 |
| docs/agent/pitfalls.md | W1108 | 本批工具/产物 |
| scripts/output/INDEX.md | W1108 | 本批工具/产物 |
| scripts/output/README.md | W1108 | 本批工具/产物 |
| scripts/output/_cascade_files_W1108.txt | W1108 | 本批工具/产物 |
| scripts/output/_w1108_spec.json | W1108 | 本批工具/产物 |
| scripts/output/file-index.md | W1108 | 本批工具/产物 |
| scripts/output/stats-changelog.json | W1108 | 本批工具/产物 |
| scripts/output/stats-index.md | W1108 | 本批工具/产物 |
| scripts/output/stats.json | W1108 | 本批工具/产物 |
| scripts/output/tools-inventory.md | W1108 | 本批工具/产物 |
| site/data/chart-design.html | W1108 | 本批工具/产物 |
| site/data/cross-time-danmaku.html | W1108 | 本批工具/产物 |
| site/data/search.html | W1108 | 本批工具/产物 |
| site/data/tag-cloud.html | W1108 | 本批工具/产物 |
| site/dukou-engine.html | W1108 | 本批工具/产物 |
| site/en/chart-design.html | W1108 | 本批工具/产物 |
| site/en/search.html | W1108 | 本批工具/产物 |
| site/index.html | W1108 | 本批工具/产物 |
> **维护契约**：本索引按 W 追加登记（每文件 1 行 + 一句摘要），历史段禁改；新增/变更文件必须先有 CHANGELOG 对应 W 段再登记（双索引铁律），禁止无 W 段单独登记。
