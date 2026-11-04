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
## W1107 坑表编号唯一性体检与机器判据建置 + 档 3 前置（2026-11-03）

| 文件 | W | 说明 |
|---|---|---|
| .agent/skills/puti-shouye/SKILL.md | W1107 | 本批改动 |
| AGENTS.md | W1107 | 本批改动 |
| HANDOVER.md | W1107 | 本批改动 |
| docs/00-导读/W批次编号对账表.md | W1107 | 本批改动 |
| docs/agent/pitfalls.md | W1107 | 本批改动 |
| scripts/check_pitfall_id_unique.py | W1107 | 本批改动 |
| tests/unit/test_w1106_pitfall_id_unique.py | W1107 | 本批改动 |
| docs/11-方案报告/计划方案/T58-任务计划执行与经验沉淀报告-2026-11-03.md | W1107 | 本批改动 |
| docs/11-方案报告/计划方案/T59-任务计划执行与经验沉淀报告-2026-11-03.md | W1107 | 本批改动 |
| scripts/output/_w1106_spec.json | W1107 | 本批工具/产物 |
| scripts/output/_w1107_spec.json | W1107 | 本批工具/产物 |
| scripts/output/_cascade_files_W1106.txt | W1107 | 本批工具/产物 |
| scripts/output/_cascade_files_W1107.txt | W1107 | 本批工具/产物 |
| scripts/output/file-index.md | W1107 | 本批工具/产物 |
| scripts/output/stats.json | W1107 | 本批工具/产物 |
| scripts/output/stats-index.md | W1107 | 本批工具/产物 |
| scripts/output/stats-changelog.json | W1107 | 本批工具/产物 |
| scripts/output/INDEX.md | W1107 | 本批工具/产物 |
| scripts/output/README.md | W1107 | 本批工具/产物 |
| scripts/output/tools-inventory.md | W1107 | 本批工具/产物 |
| scripts/output/_vermilion_solid_cache.json | W1107 | 本批工具/产物 |
| docs/INDEX.md | W1107 | 本批工具/产物 |
| tests/unit/INDEX.md | W1107 | 本批工具/产物 |
| tests/unit/README.md | W1107 | 本批工具/产物 |
| pytest.ini | W1107 | 本批工具/产物 |
| CHANGELOG.md | W1107 | 本批工具/产物 |
| README.md | W1107 | 本批工具/产物 |
| STRUCTURE.md | W1107 | 本批工具/产物 |
| CITATION.cff | W1107 | 本批工具/产物 |
| docs/00-导读/项目说明.md | W1107 | 本批工具/产物 |
| docs/11-方案报告/README.md | W1107 | 本批工具/产物 |
| .github/workflows/README.md | W1107 | 本批工具/产物 |
| site/tokens.css | W1107 | 本批工具/产物 |
| site/index.html | W1107 | 本批工具/产物 |
| site/data/cross-time-danmaku.html | W1107 | 本批工具/产物 |
| site/data/tag-cloud.html | W1107 | 本批工具/产物 |
| site/dukou-engine.html | W1107 | 本批工具/产物 |

## W1106 图表色工程批·档 3 前置批（2026-11-03）

| 文件 | W | 说明 |
|---|---|---|
| site/data/business-model.html | W1106 | 页面（暗色令牌受益面） |
| site/data/cave-estate.html | W1106 | 页面（暗色令牌受益面） |
| site/data/character-appearance.html | W1106 | 页面（暗色令牌受益面） |
| site/data/cognitive-psychology.html | W1106 | 页面（暗色令牌受益面） |
| site/data/concept-device.html | W1106 | 页面（暗色令牌受益面） |
| site/data/customs-pass-route.html | W1106 | 页面（暗色令牌受益面） |
| site/data/deconstruction.html | W1106 | 页面（暗色令牌受益面） |
| site/data/four-dimensional-research-network.html | W1106 | 页面（暗色令牌受益面） |
| site/data/game-webnovel.html | W1106 | 页面（暗色令牌受益面） |
| site/data/global-pattern.html | W1106 | 页面（暗色令牌受益面） |
| site/data/hardship-difficulty-heatmap.html | W1106 | 页面（暗色令牌受益面） |
| site/data/hardship-heatmap.html | W1106 | 页面（暗色令牌受益面） |
| site/data/heaven-power-network.html | W1106 | 页面（暗色令牌受益面） |
| site/data/journey-map-interactive.html | W1106 | 页面（暗色令牌受益面） |
| site/data/journey-spacetime.html | W1106 | 页面（暗色令牌受益面） |
| site/data/jurisprudence.html | W1106 | 页面（暗色令牌受益面） |
| site/data/karma-reincarnation.html | W1106 | 页面（暗色令牌受益面） |
| site/data/ming-political-thought-comparison.html | W1106 | 页面（暗色令牌受益面） |
| site/data/monster-background.html | W1106 | 页面（暗色令牌受益面） |
| site/data/monster-capability-radar.html | W1106 | 页面（暗色令牌受益面） |
| site/data/monster-ecology-network.html | W1106 | 页面（暗色令牌受益面） |
| site/data/monster-hierarchy-network.html | W1106 | 页面（暗色令牌受益面） |
| site/data/monster-sociology.html | W1106 | 页面（暗色令牌受益面） |
| site/data/music-structure.html | W1106 | 页面（暗色令牌受益面） |
| site/data/narrative-experiment.html | W1106 | 页面（暗色令牌受益面） |
| site/data/philosophy.html | W1106 | 页面（暗色令牌受益面） |
| site/data/pilgrim-team-psychology-arc.html | W1106 | 页面（暗色令牌受益面） |
| site/data/poetry-rhythm-analysis.html | W1106 | 页面（暗色令牌受益面） |
| site/data/power-resources.html | W1106 | 页面（暗色令牌受益面） |
| site/data/risk-project.html | W1106 | 页面（暗色令牌受益面） |
| site/data/underworld-power-network.html | W1106 | 页面（暗色令牌受益面） |
| site/data/visual-art.html | W1106 | 页面（暗色令牌受益面） |
| site/en/customs-pass-route.html | W1106 | 页面（暗色令牌受益面） |
| site/en/four-dimensional-research-network.html | W1106 | 页面（暗色令牌受益面） |
| site/en/game-webnovel.html | W1106 | 页面（暗色令牌受益面） |
| site/en/heaven-power-network.html | W1106 | 页面（暗色令牌受益面） |
| site/en/monster-ecology-network.html | W1106 | 页面（暗色令牌受益面） |
| site/en/monster-hierarchy-network.html | W1106 | 页面（暗色令牌受益面） |
| site/en/music-structure.html | W1106 | 页面（暗色令牌受益面） |
| site/en/narrative-experiment.html | W1106 | 页面（暗色令牌受益面） |
| site/en/underworld-power-network.html | W1106 | 页面（暗色令牌受益面） |
| site/en/visual-art.html | W1106 | 页面（暗色令牌受益面） |
| site/tokens.css | W1106 | 本批工具/产物 |
| site/index.html | W1106 | 治理文档 |
| site/data/cross-time-danmaku.html | W1106 | 治理文档 |
| site/data/tag-cloud.html | W1106 | 治理文档 |
| site/dukou-engine.html | W1106 | 治理文档 |
| AGENTS.md | W1106 | 治理文档 |
| HANDOVER.md | W1106 | 治理文档 |
| CHANGELOG.md | W1106 | 治理文档 |
| README.md | W1106 | 治理文档 |
| STRUCTURE.md | W1106 | 治理文档 |
| CITATION.cff | W1106 | 治理文档 |
| docs/agent/pitfalls.md | W1106 | 治理文档 |
| docs/00-导读/W批次编号对账表.md | W1106 | 治理文档 |
| docs/00-导读/项目说明.md | W1106 | 治理文档 |
| docs/11-方案报告/README.md | W1106 | 治理文档 |
| docs/11-方案报告/计划方案/T58-任务计划执行与经验沉淀报告-2026-11-03.md | W1106 | 治理文档 |
| docs/INDEX.md | W1106 | 治理文档 |
| .agent/skills/puti-shouye/SKILL.md | W1106 | 治理文档 |
| .github/workflows/README.md | W1106 | 治理文档 |
| scripts/output/_w1106_spec.json | W1106 | 本批工具/产物 |
| scripts/output/_cascade_files_W1106.txt | W1106 | 本批工具/产物 |
| scripts/output/file-index.md | W1106 | 本批工具/产物 |
| scripts/output/stats.json | W1106 | 本批工具/产物 |
| scripts/output/stats-index.md | W1106 | 本批工具/产物 |
| scripts/output/stats-changelog.json | W1106 | 本批工具/产物 |
| scripts/output/INDEX.md | W1106 | 本批工具/产物 |
| scripts/output/README.md | W1106 | 本批工具/产物 |
| scripts/output/tools-inventory.md | W1106 | 本批工具/产物 |
| scripts/output/_vermilion_solid_cache.json | W1106 | 本批工具/产物 |
| pytest.ini | W1106 | 治理文档 |
| tests/unit/INDEX.md | W1106 | 治理文档 |
| tests/unit/README.md | W1106 | 治理文档 |
| docs/11-方案报告/计划方案/T59-任务计划执行与经验沉淀报告-2026-11-03.md | W1106 | 本批工具/产物 |
| scripts/check_pitfall_id_unique.py | W1106 | 本批工具/产物 |
| tests/unit/test_w1106_pitfall_id_unique.py | W1106 | 本批工具/产物 |
| scripts/output/_w1107_spec.json | W1106 | 本批工具/产物 |

## W1105 遗留清偿批（归档健康根修 + 第 31 门禁两盲区 + design 审查收口 + 站点守卫与 tooltip 对齐）（2026-11-02）
| 文件 | W | 说明 |
|---|---|---|
| .agent/skills/puti-shouye/SKILL.md | W1105 | governance-or-doc |
| AGENTS.md | W1105 | governance-or-doc |
| CHANGELOG.md | W1105 | governance-or-doc |
| DESIGN.md | W1105 | governance-or-doc |
| HANDOVER.md | W1105 | governance-or-doc |
| README.md | W1105 | governance-or-doc |
| STRUCTURE.md | W1105 | governance-or-doc |
| archive/README.md | W1105 | governance-or-doc |
| archive/docs/AGENTS-ARCHIVE.md | W1105 | governance-or-doc |
| archive/docs/CHANGELOG-ARCHIVE.md | W1105 | governance-or-doc |
| archive/docs/file-index-ARCHIVE.md | W1105 | governance-or-doc |
| assets/design/ai-concepts/README.md | W1105 | governance-or-doc |
| assets/design/tools/README.md | W1105 | governance-or-doc |
| docs/00-导读/W批次编号对账表.md | W1105 | governance-or-doc |
| docs/00-导读/项目说明.md | W1105 | governance-or-doc |
| docs/11-方案报告/README.md | W1105 | report |
| docs/11-方案报告/审查与评审/设计文件审查报告-2026-11-02.md | W1105 | report |
| docs/11-方案报告/计划方案/T56-任务计划执行与经验沉淀报告-2026-11-02.md | W1105 | report |
| docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md | W1105 | report |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1105 | report |
| docs/INDEX.md | W1105 | governance-or-doc |
| docs/agent/gates.md | W1105 | governance-or-doc |
| docs/agent/pitfalls.md | W1105 | governance-or-doc |
| pytest.ini | W1105 | governance-or-doc |
| scripts/INDEX.md | W1105 | script-or-artifact |
| scripts/cascade_lock.py | W1105 | script-or-artifact |
| scripts/check_archive_health.py | W1105 | script-or-artifact |
| scripts/check_chart_design_parity.py | W1105 | script-or-artifact |
| scripts/check_doc_sync.py | W1105 | script-or-artifact |
| scripts/cross_line_baseline.json | W1105 | script-or-artifact |
| scripts/export_design_tokens.py | W1105 | script-or-artifact |
| scripts/output/INDEX.md | W1105 | script-or-artifact |
| scripts/output/README.md | W1105 | script-or-artifact |
| scripts/output/_cascade_files_W1105.txt | W1105 | script-or-artifact |
| scripts/output/_vermilion_solid_cache.json | W1105 | script-or-artifact |
| scripts/output/_w1102_spec.json | W1105 | script-or-artifact |
| scripts/output/design-tokens.json | W1105 | script-or-artifact |
| scripts/output/stats-changelog.json | W1105 | script-or-artifact |
| scripts/output/stats-index.md | W1105 | script-or-artifact |
| scripts/output/stats.json | W1105 | script-or-artifact |
| scripts/output/tools-inventory.md | W1105 | script-or-artifact |
| scripts/verify_delivery.py | W1105 | script-or-artifact |
| scripts/visual_regression_probe.py | W1105 | script-or-artifact |
| site/dashboard.html | W1105 | page-change |
| site/data/81-hardships.html | W1105 | page-change |
| site/data/chapter-stats.html | W1105 | page-change |
| site/data/character-appearance.html | W1105 | page-change |
| site/data/cross-time-danmaku.html | W1105 | page-change |
| site/data/emotional-heatmap.html | W1105 | page-change |
| site/data/search.html | W1105 | page-change |
| site/data/tag-cloud.html | W1105 | page-change |
| site/dukou-engine.html | W1105 | page-change |
| site/en/aesthetics.html | W1105 | page-change |
| site/en/business-model.html | W1105 | page-change |
| site/en/cave-estate.html | W1105 | page-change |
| site/en/chapter-stats.html | W1105 | page-change |
| site/en/chapter-structure-graph.html | W1105 | page-change |
| site/en/character-appearance.html | W1105 | page-change |
| site/en/character-semantic-network.html | W1105 | page-change |
| site/en/chart-design.html | W1105 | page-change |
| site/en/counterfactual.html | W1105 | page-change |
| site/en/cultural-misreading.html | W1105 | page-change |
| site/en/deconstruction.html | W1105 | page-change |
| site/en/dialogue-sentiment.html | W1105 | page-change |
| site/en/ethics-consumption.html | W1105 | page-change |
| site/en/four-heavenly-kings-artifacts.html | W1105 | page-change |
| site/en/game-webnovel.html | W1105 | page-change |
| site/en/global-pattern.html | W1105 | page-change |
| site/en/guanyin-six-roles-network.html | W1105 | page-change |
| site/en/hardship-heatmap.html | W1105 | page-change |
| site/en/heaven-power-network.html | W1105 | page-change |
| site/en/intertextuality-network.html | W1105 | page-change |
| site/en/journey-geo-semiotics.html | W1105 | page-change |
| site/en/journey-map-interactive.html | W1105 | page-change |
| site/en/journey-route.html | W1105 | page-change |
| site/en/jurisprudence.html | W1105 | page-change |
| site/en/karma-reincarnation.html | W1105 | page-change |
| site/en/language-style-radar.html | W1105 | page-change |
| site/en/linguistics.html | W1105 | page-change |
| site/en/magic-system.html | W1105 | page-change |
| site/en/material-archaeology.html | W1105 | page-change |
| site/en/methodology-matrix.html | W1105 | page-change |
| site/en/ming-political-thought-comparison.html | W1105 | page-change |
| site/en/monster-background.html | W1105 | page-change |
| site/en/monster-female-network.html | W1105 | page-change |
| site/en/monster-hierarchy-network.html | W1105 | page-change |
| site/en/monster-sociology.html | W1105 | page-change |
| site/en/monster-victims-network.html | W1105 | page-change |
| site/en/narrative-experiment.html | W1105 | page-change |
| site/en/narrative-rhythm-curve.html | W1105 | page-change |
| site/en/narratology-12d-network.html | W1105 | page-change |
| site/en/narratology-16d-network.html | W1105 | page-change |
| site/en/philosophy.html | W1105 | page-change |
| site/en/power-resources.html | W1105 | page-change |
| site/en/search.html | W1105 | page-change |
| site/en/six-senses-narratology-network.html | W1105 | page-change |
| site/en/social-media.html | W1105 | page-change |
| site/en/tag-cloud.html | W1105 | page-change |
| site/en/text-evolution.html | W1105 | page-change |
| site/en/underworld-power-network.html | W1105 | page-change |
| site/en/visual-art.html | W1105 | page-change |
| site/en/workplace.html | W1105 | page-change |
| site/index.html | W1105 | page-change |
| tests/unit/INDEX.md | W1105 | test |
| tests/unit/README.md | W1105 | test |
| tests/unit/test_check_chart_design_parity.py | W1105 | test |

# xiyouji 文件反向索引

> 与 [CHANGELOG.md](../../CHANGELOG.md) 配套：给定文件，查它被改过几次、每次对应哪个 W 条目。
> W### 编号规则见 CHANGELOG.md 顶部。
> 创建于 2026-07-22（v0.8 双索引改造）
>
> **历史归档**：W031-W087（v2.0.4-v2.0.60）site/data/ 部分已迁移至 [file-index-ARCHIVE.md](../../archive/docs/file-index-ARCHIVE.md)；W422 再归档 W393-W416 段；W511 归档 W417-W448 段 + W449-W463 损坏区尾部清理。W736 归档 W449-W699 段（与 CHANGELOG 现役边界统一至 W700）。本文件正本按 110 段窗滚动（W960 窗口制·正本最老段随批推进）。
>
> **维护契约**：本索引按 W 追加登记（每文件 1 行 + 一句摘要），历史段禁改；新增/变更文件必须先有 CHANGELOG 对应 W 段再登记（双索引铁律），禁止无 W 段单独登记。

---

## W1104 开局事实摘要 stats 新鲜度告警（2026-11-02）

| 文件 | W | 说明 |
|---|---|---|
| scripts/visual_regression_probe.py | W1104 | 本批工具/产物 |
| tests/unit/test_w851_visual_regression_probe.py | W1104 | 本批工具/产物 |
| scripts/output/_vermilion_solid_cache.json | W1104 | 本批工具/产物 |
| scripts/output/_vermilion_solid_report.json | W1104 | 本批工具/产物 |
| archive/scripts/batches/w1100/_w1100_chart_color_inventory.py | W1104 | 本批工具/产物 |
| archive/scripts/batches/w1100/_w1100_layer3_pages.py | W1104 | 本批工具/产物 |
| archive/scripts/batches/w1100/_w1100_comp_provenance.py | W1104 | 本批工具/产物 |
| scripts/output/_w1100_inventory.json | W1104 | 本批工具/产物 |
| scripts/output/_w1100_layer3_pages.json | W1104 | 本批工具/产物 |
| archive/scripts/batches/w1100/_w1100_refresh_chain.py | W1104 | 本批工具/产物 |
| archive/scripts/batches/w1100/_w1100_comp_source.py | W1104 | 本批工具/产物 |
| archive/scripts/batches/w1100/README.md | W1104 | 本批工具/产物 |
| archive/scripts/batches/w1100/INDEX.md | W1104 | 本批工具/产物 |
| archive/scripts/batches/README.md | W1104 | 本批工具/产物 |
| archive/scripts/batches/INDEX.md | W1104 | 本批工具/产物 |
| scripts/output/_w1104_spec.json | W1104 | 本批工具/产物 |
| docs/11-方案报告/README.md | W1104 | 治理文档 |
| docs/00-导读/W批次编号对账表.md | W1104 | 治理文档 |
| docs/agent/pitfalls.md | W1104 | 治理文档 |
| .agent/skills/puti-shouye/SKILL.md | W1104 | 治理文档 |
| .github/workflows/README.md | W1104 | 治理文档 |
| AGENTS.md | W1104 | 治理文档 |
| CHANGELOG.md | W1104 | 治理文档 |
| CITATION.cff | W1104 | 治理文档 |
| HANDOVER.md | W1104 | 治理文档 |
| README.md | W1104 | 治理文档 |
| STRUCTURE.md | W1104 | 治理文档 |
| archive/docs/AGENTS-ARCHIVE.md | W1104 | 治理文档 |
| archive/docs/CHANGELOG-ARCHIVE.md | W1104 | 治理文档 |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1104 | 治理文档 |
| archive/docs/file-index-ARCHIVE.md | W1104 | 治理文档 |
| docs/00-导读/项目说明.md | W1104 | 治理文档 |
| docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md | W1104 | 治理文档 |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1104 | 治理文档 |
| docs/INDEX.md | W1104 | 治理文档 |
| scripts/output/INDEX.md | W1104 | 本批工具/产物 |
| scripts/output/README.md | W1104 | 本批工具/产物 |
| scripts/output/_cascade_files_W1104.txt | W1104 | 本批工具/产物 |
| scripts/output/file-index.md | W1104 | 本批工具/产物 |
| scripts/output/stats-changelog.json | W1104 | 本批工具/产物 |
| scripts/output/stats-index.md | W1104 | 本批工具/产物 |
| scripts/output/stats.json | W1104 | 本批工具/产物 |
| scripts/output/tools-inventory.md | W1104 | 本批工具/产物 |
| site/data/cross-time-danmaku.html | W1104 | 页面 |
| site/data/search.html | W1104 | 页面 |
| site/data/tag-cloud.html | W1104 | 页面 |
| site/dukou-engine.html | W1104 | 页面 |
| site/en/search.html | W1104 | 页面 |
| site/index.html | W1104 | 页面 |
| scripts/agent_start.py | W1104 | 本批工具/产物 |
| tests/unit/test_w1104_agent_start_freshness.py | W1104 | 本批工具/产物 |
| docs/11-方案报告/计划方案/T56-任务计划执行与经验沉淀报告-2026-11-02.md | W1104 | 治理文档 |

## W1103 图表色工程批·ΔL* 阈值机器判据（2026-11-02）

| 文件 | W | 说明 |
|---|---|---|
| .agent/skills/puti-shouye/SKILL.md | W1103 | 治理文档 |
| .github/workflows/README.md | W1103 | 治理文档 |
| AGENTS.md | W1103 | 治理文档 |
| CHANGELOG.md | W1103 | 治理文档 |
| CITATION.cff | W1103 | 治理文档 |
| HANDOVER.md | W1103 | 治理文档 |
| README.md | W1103 | 治理文档 |
| STRUCTURE.md | W1103 | 治理文档 |
| archive/docs/AGENTS-ARCHIVE.md | W1103 | 治理文档 |
| archive/docs/CHANGELOG-ARCHIVE.md | W1103 | 治理文档 |
| archive/docs/file-index-ARCHIVE.md | W1103 | 治理文档 |
| docs/00-导读/W批次编号对账表.md | W1103 | 治理文档 |
| docs/00-导读/项目说明.md | W1103 | 治理文档 |
| docs/11-方案报告/README.md | W1103 | 治理文档 |
| docs/11-方案报告/计划方案/T57-任务计划执行与经验沉淀报告-2026-11-02.md | W1103 | 治理文档 |
| docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md | W1103 | 治理文档 |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1103 | 治理文档 |
| docs/INDEX.md | W1103 | 治理文档 |
| docs/agent/pitfalls.md | W1103 | 治理文档 |
| pytest.ini | W1103 | 治理文档 |
| scripts/INDEX.md | W1103 | 本批工具/产物 |
| scripts/color_delta_guard.py | W1103 | 本批工具/产物 |
| scripts/output/INDEX.md | W1103 | 本批工具/产物 |
| scripts/output/README.md | W1103 | 本批工具/产物 |
| scripts/output/_cascade_files_W1103.txt | W1103 | 本批工具/产物 |
| scripts/output/_vermilion_solid_cache.json | W1103 | 本批工具/产物 |
| scripts/output/_w1103_spec.json | W1103 | 本批工具/产物 |
| scripts/output/file-index.md | W1103 | 本批工具/产物 |
| scripts/output/stats-changelog.json | W1103 | 本批工具/产物 |
| scripts/output/stats-index.md | W1103 | 本批工具/产物 |
| scripts/output/stats.json | W1103 | 本批工具/产物 |
| scripts/output/tools-inventory.md | W1103 | 本批工具/产物 |
| site/data/cross-time-danmaku.html | W1103 | 页面 |
| site/data/search.html | W1103 | 页面 |
| site/data/tag-cloud.html | W1103 | 页面 |
| site/dukou-engine.html | W1103 | 页面 |
| site/en/search.html | W1103 | 页面 |
| site/index.html | W1103 | 页面 |
| tests/unit/INDEX.md | W1103 | 本批工具/产物 |
| tests/unit/README.md | W1103 | 本批工具/产物 |
| tests/unit/test_w1103_color_delta_guard.py | W1103 | 本批工具/产物 |

## W1100 图表色工程批·档 3 落层分类盘点（2026-11-02）

| 文件 | W | 说明 |
|---|---|---|
| scripts/visual_regression_probe.py | W1100 | 本批工具/产物 |
| tests/unit/test_w851_visual_regression_probe.py | W1100 | 本批工具/产物 |
| scripts/output/_vermilion_solid_cache.json | W1100 | 本批工具/产物 |
| scripts/output/_vermilion_solid_report.json | W1100 | 本批工具/产物 |
| archive/scripts/batches/w1100/_w1100_chart_color_inventory.py | W1100 | 本批工具/产物 |
| archive/scripts/batches/w1100/_w1100_layer3_pages.py | W1100 | 本批工具/产物 |
| archive/scripts/batches/w1100/_w1100_comp_provenance.py | W1100 | 本批工具/产物 |
| scripts/output/_w1100_inventory.json | W1100 | 本批工具/产物 |
| scripts/output/_w1100_layer3_pages.json | W1100 | 本批工具/产物 |
| docs/11-方案报告/计划方案/T55-任务计划执行与经验沉淀报告-2026-11-02.md | W1100 | 治理文档 |
| archive/scripts/batches/w1100/_w1100_refresh_chain.py | W1100 | 本批工具/产物 |
|## W1099 图表色工程批·档 2 扩展批 3（2026-11-02）

| 文件 | W | 说明 |
|---|---|---|
| scripts/visual_regression_probe.py | W1099 | 本批工具/产物 |
| tests/unit/test_w851_visual_regression_probe.py | W1099 | 本批工具/产物 |
| scripts/output/_vermilion_solid_cache.json | W1099 | 本批工具/产物 |
| scripts/output/_vermilion_solid_report.json | W1099 | 本批工具/产物 |
| site/en/journey-map-interactive.html | W1099 | 页面 |
| site/en/philosophy.html | W1099 | 页面 |
| site/en/pilgrim-team-psychology-arc.html | W1099 | 页面 |
| site/en/social-media.html | W1099 | 页面 |
| docs/11-方案报告/计划方案/T54-任务计划执行与经验沉淀报告-2026-11-02.md | W1099 | 治理文档 |
| scripts/output/_w1099_spec.json | W1099 | 本批工具/产物 |
| docs/11-方案报告/README.md | W1099 | 治理文档 |
| docs/00-导读/W批次编号对账表.md | W1099 | 治理文档 |
| docs/agent/pitfalls.md | W1099 | 治理文档 |
| .agent/skills/puti-shouye/SKILL.md | W1099 | 治理文档 |
| .github/workflows/README.md | W1099 | 治理文档 |
| AGENTS.md | W1099 | 治理文档 |
| CHANGELOG.md | W1099 | 治理文档 |
| CITATION.cff | W1099 | 治理文档 |
| HANDOVER.md | W1099 | 治理文档 |
| README.md | W1099 | 治理文档 |
| STRUCTURE.md | W1099 | 治理文档 |
| archive/docs/AGENTS-ARCHIVE.md | W1099 | 治理文档 |
| archive/docs/CHANGELOG-ARCHIVE.md | W1099 | 治理文档 |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1099 | 治理文档 |
| archive/docs/file-index-ARCHIVE.md | W1099 | 治理文档 |
| docs/00-导读/项目说明.md | W1099 | 治理文档 |
| docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md | W1099 | 治理文档 |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1099 | 治理文档 |
| docs/INDEX.md | W1099 | 治理文档 |
| scripts/output/INDEX.md | W1099 | 本批工具/产物 |
| scripts/output/README.md | W1099 | 本批工具/产物 |
| scripts/output/_cascade_files_W1099.txt | W1099 | 本批工具/产物 |
| scripts/output/file-index.md | W1099 | 本批工具/产物 |
| scripts/output/stats-changelog.json | W1099 | 本批工具/产物 |
| scripts/output/stats-index.md | W1099 | 本批工具/产物 |
| scripts/output/stats.json | W1099 | 本批工具/产物 |
| scripts/output/tools-inventory.md | W1099 | 本批工具/产物 |
| site/data/cross-time-danmaku.html | W1099 | 页面 |
| site/data/search.html | W1099 | 页面 |
| site/data/tag-cloud.html | W1099 | 页面 |
| site/dukou-engine.html | W1099 | 页面 |
| site/en/search.html | W1099 | 页面 |
| site/index.html | W1099 | 页面 |

## W1099 图表色工程批·档 2 扩展批 3（2026-11-02）

| 文件 | W | 说明 |
|---|---|---|
| scripts/visual_regression_probe.py | W1099 | 本批工具/产物 |
| tests/unit/test_w851_visual_regression_probe.py | W1099 | 本批工具/产物 |
| scripts/output/_vermilion_solid_cache.json | W1099 | 本批工具/产物 |
| scripts/output/_vermilion_solid_report.json | W1099 | 本批工具/产物 |
| site/en/journey-map-interactive.html | W1099 | 页面 |
| site/en/philosophy.html | W1099 | 页面 |
| site/en/pilgrim-team-psychology-arc.html | W1099 | 页面 |
| site/en/social-media.html | W1099 | 页面 |
| docs/11-方案报告/计划方案/T54-任务计划执行与经验沉淀报告-2026-11-02.md | W1099 | 治理文档 |
| scripts/output/_w1099_spec.json | W1099 | 本批工具/产物 |
| docs/11-方案报告/README.md | W1099 | 治理文档 |
| docs/00-导读/W批次编号对账表.md | W1099 | 治理文档 |
| docs/agent/pitfalls.md | W1099 | 治理文档 |
| .agent/skills/puti-shouye/SKILL.md | W1099 | 治理文档 |
| .github/workflows/README.md | W1099 | 治理文档 |
| AGENTS.md | W1099 | 治理文档 |
| CHANGELOG.md | W1099 | 治理文档 |
| CITATION.cff | W1099 | 治理文档 |
| HANDOVER.md | W1099 | 治理文档 |
| README.md | W1099 | 治理文档 |
| STRUCTURE.md | W1099 | 治理文档 |
| archive/docs/AGENTS-ARCHIVE.md | W1099 | 治理文档 |
| archive/docs/CHANGELOG-ARCHIVE.md | W1099 | 治理文档 |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1099 | 治理文档 |
| archive/docs/file-index-ARCHIVE.md | W1099 | 治理文档 |
| docs/00-导读/项目说明.md | W1099 | 治理文档 |
| docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md | W1099 | 治理文档 |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1099 | 治理文档 |
| docs/INDEX.md | W1099 | 治理文档 |
| scripts/output/INDEX.md | W1099 | 本批工具/产物 |
| scripts/output/README.md | W1099 | 本批工具/产物 |
| scripts/output/_cascade_files_W1099.txt | W1099 | 本批工具/产物 |
| scripts/output/file-index.md | W1099 | 本批工具/产物 |
| scripts/output/stats-changelog.json | W1099 | 本批工具/产物 |
| scripts/output/stats-index.md | W1099 | 本批工具/产物 |
| scripts/output/stats.json | W1099 | 本批工具/产物 |
| scripts/output/tools-inventory.md | W1099 | 本批工具/产物 |
| site/data/cross-time-danmaku.html | W1099 | 页面 |
| site/data/search.html | W1099 | 页面 |
| site/data/tag-cloud.html | W1099 | 页面 |
| site/dukou-engine.html | W1099 | 页面 |
| site/en/search.html | W1099 | 页面 |
| site/index.html | W1099 | 页面 |

## W1098 图表色工程批·档 2 扩展批 2（2026-11-02）

| 文件 | W | 说明 |
|---|---|---|
| site/en/monster-capability-radar.html | W1098 | 页面 |
| site/en/monster-sociology.html | W1098 | 页面 |
| site/en/narrative-rhythm-curve.html | W1098 | 页面 |
| site/en/power-resources.html | W1098 | 页面 |
| site/en/monster-victims-network.html | W1098 | 页面 |
| site/en/journey-spacetime.html | W1098 | 页面 |
| site/en/narrative-experiment.html | W1098 | 页面 |
| site/en/poetry-rhythm-analysis.html | W1098 | 页面 |
| site/en/character-appearance.html | W1098 | 页面 |
| site/en/hardship-difficulty-heatmap.html | W1098 | 页面 |
| scripts/visual_regression_probe.py | W1098 | 本批工具/产物 |
| tests/unit/test_w851_visual_regression_probe.py | W1098 | 本批工具/产物 |
| docs/11-方案报告/计划方案/T53-任务计划执行与经验沉淀报告-2026-11-02.md | W1098 | 治理文档 |
| scripts/output/_vermilion_solid_cache.json | W1098 | 本批工具/产物 |
| scripts/output/_vermilion_solid_report.json | W1098 | 本批工具/产物 |
| scripts/output/_w1098_spec.json | W1098 | 本批工具/产物 |
| docs/11-方案报告/README.md | W1098 | 治理文档 |
| docs/00-导读/W批次编号对账表.md | W1098 | 治理文档 |
| docs/agent/pitfalls.md | W1098 | 治理文档 |
| .agent/skills/puti-shouye/SKILL.md | W1098 | 治理文档 |
| .github/workflows/README.md | W1098 | 治理文档 |
| AGENTS.md | W1098 | 治理文档 |
| CHANGELOG.md | W1098 | 治理文档 |
| CITATION.cff | W1098 | 治理文档 |
| HANDOVER.md | W1098 | 治理文档 |
| README.md | W1098 | 治理文档 |
| STRUCTURE.md | W1098 | 治理文档 |
| archive/docs/AGENTS-ARCHIVE.md | W1098 | 治理文档 |
| archive/docs/CHANGELOG-ARCHIVE.md | W1098 | 治理文档 |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1098 | 治理文档 |
| archive/docs/file-index-ARCHIVE.md | W1098 | 治理文档 |
| docs/00-导读/项目说明.md | W1098 | 治理文档 |
| docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md | W1098 | 治理文档 |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1098 | 治理文档 |
| docs/INDEX.md | W1098 | 治理文档 |
| scripts/output/INDEX.md | W1098 | 本批工具/产物 |
| scripts/output/README.md | W1098 | 本批工具/产物 |
| scripts/output/_cascade_files_W1098.txt | W1098 | 本批工具/产物 |
| scripts/output/file-index.md | W1098 | 本批工具/产物 |
| scripts/output/stats-changelog.json | W1098 | 本批工具/产物 |
| scripts/output/stats-index.md | W1098 | 本批工具/产物 |
| scripts/output/stats.json | W1098 | 本批工具/产物 |
| scripts/output/tools-inventory.md | W1098 | 本批工具/产物 |
| site/data/cross-time-danmaku.html | W1098 | 页面 |
| site/data/search.html | W1098 | 页面 |
| site/data/tag-cloud.html | W1098 | 页面 |
| site/dukou-engine.html | W1098 | 页面 |
| site/en/search.html | W1098 | 页面 |
| site/index.html | W1098 | 页面 |

## W1097 图表色工程批·档 2 扩展批 1（2026-11-02）

| 文件 | W | 说明 |
|---|---|---|
| site/en/business-model.html | W1097 | 页面 |
| site/en/cognitive-psychology.html | W1097 | 页面 |
| site/en/jurisprudence.html | W1097 | 页面 |
| site/en/concept-device.html | W1097 | 页面 |
| site/en/guanyin-six-roles-network.html | W1097 | 页面 |
| site/en/risk-project.html | W1097 | 页面 |
| site/en/character-sentiment-arc.html | W1097 | 页面 |
| site/en/heaven-power-network.html | W1097 | 页面 |
| site/en/underworld-power-network.html | W1097 | 页面 |
| site/en/karma-reincarnation.html | W1097 | 页面 |
| scripts/visual_regression_probe.py | W1097 | 本批工具/产物 |
| tests/unit/test_w851_visual_regression_probe.py | W1097 | 本批工具/产物 |
| docs/11-方案报告/计划方案/T52-任务计划执行与经验沉淀报告-2026-11-02.md | W1097 | 治理文档 |
| docs/11-方案报告/README.md | W1097 | 治理文档 |
| docs/00-导读/W批次编号对账表.md | W1097 | 治理文档 |
| docs/agent/pitfalls.md | W1097 | 治理文档 |
| scripts/output/_w1097_spec.json | W1097 | 本批工具/产物 |
| .agent/skills/puti-shouye/SKILL.md | W1097 | 治理文档 |
| .github/workflows/README.md | W1097 | 治理文档 |
| pytest.ini | W1097 | 本批修改（stats 实体标记跟随·pytest_collected 1108 → 1112·本批新增 4 例单测） |
| AGENTS.md | W1097 | 治理文档 |
| CHANGELOG.md | W1097 | 治理文档 |
| CITATION.cff | W1097 | 治理文档 |
| HANDOVER.md | W1097 | 治理文档 |
| README.md | W1097 | 治理文档 |
| STRUCTURE.md | W1097 | 治理文档 |
| archive/docs/AGENTS-ARCHIVE.md | W1097 | 治理文档 |
| archive/docs/CHANGELOG-ARCHIVE.md | W1097 | 治理文档 |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1097 | 治理文档 |
| archive/docs/file-index-ARCHIVE.md | W1097 | 治理文档 |
| docs/00-导读/项目说明.md | W1097 | 治理文档 |
| docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md | W1097 | 治理文档 |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1097 | 治理文档 |
| docs/INDEX.md | W1097 | 治理文档 |
| scripts/output/INDEX.md | W1097 | 本批工具/产物 |
| scripts/output/README.md | W1097 | 本批工具/产物 |
| scripts/output/_cascade_files_W1097.txt | W1097 | 本批工具/产物 |
| scripts/output/file-index.md | W1097 | 本批工具/产物 |
| scripts/output/stats-changelog.json | W1097 | 本批工具/产物 |
| scripts/output/stats-index.md | W1097 | 本批工具/产物 |
| scripts/output/stats.json | W1097 | 本批工具/产物 |
| scripts/output/tools-inventory.md | W1097 | 本批工具/产物 |
| site/data/cross-time-danmaku.html | W1097 | 页面 |
| site/data/search.html | W1097 | 页面 |
| site/data/tag-cloud.html | W1097 | 页面 |
| site/dukou-engine.html | W1097 | 页面 |
| site/en/search.html | W1097 | 页面 |
| site/index.html | W1097 | 页面 |

## W1096 INDEX 大小写统一 + design 审查 + 归档清偿（2026-11-02）

| 文件 | W | 说明 |
|---|---|---|
| .github/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| .github/ISSUE_TEMPLATE/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| .github/workflows/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| archive/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| archive/docs/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| archive/docs/_dev/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| archive/docs/_dev/产品管理套件应用-2026-10-02/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| archive/docs/_dev/科技服务顾问-数字人文资助渠道-2026-10-02/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| archive/docs/plans/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| archive/docs/specs/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| archive/docs/templates/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| archive/docs/w550-shot-review/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| archive/docs/复盘报告/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| archive/scripts/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| archive/scripts/attic/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| archive/scripts/audit/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| archive/scripts/batches/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| archive/scripts/batches/misc/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| archive/scripts/batches/w1071/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| archive/scripts/batches/w1073/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| archive/scripts/batches/w1074/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| archive/scripts/batches/w1076/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| archive/scripts/batches/w1078/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| archive/scripts/batches/w1079/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| archive/scripts/batches/w1080/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| archive/scripts/batches/w1089/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| archive/scripts/batches/w10xx/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| archive/scripts/batches/w4xx/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| archive/scripts/batches/w5xx/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| archive/scripts/batches/w6xx/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| archive/scripts/batches/w7xx/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| archive/scripts/batches/w8xx/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| archive/scripts/batches/w9xx/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| archive/scripts/review-pass3/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| archive/scripts/review-pass3/prompts/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| assets/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| assets/design/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| assets/design/ai-concepts/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| assets/design/alternatives/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| assets/design/logo/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| assets/design/process/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| assets/design/screenshots/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| assets/design/tools/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| assets/fonts/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| assets/fonts/source/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| assets/images/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| assets/maps/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| assets/promo/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| assets/promo/hero-set/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| assets/promo/hero-set/raw/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| assets/promo/hero-set/raw/round-w1005/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| assets/promo/output/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| assets/promo/plate-set/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| assets/promo/plate-set/raw/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| assets/promo/plate-set/raw/round1/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| assets/promo/plate-set/raw/round10/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| assets/promo/plate-set/raw/round11/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| assets/promo/plate-set/raw/round12/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| assets/promo/plate-set/raw/round13/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| assets/promo/plate-set/raw/round14/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| assets/promo/plate-set/raw/round15/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| assets/promo/plate-set/raw/round16/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| assets/promo/plate-set/raw/round17/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| assets/promo/plate-set/raw/round18/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| assets/promo/plate-set/raw/round2/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| assets/promo/plate-set/raw/round3/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| assets/promo/plate-set/raw/round4/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| assets/promo/plate-set/raw/round5/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| assets/promo/plate-set/raw/round6/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| assets/promo/plate-set/raw/round7/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| assets/promo/plate-set/raw/round8/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| assets/promo/plate-set/raw/round9/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| assets/promo/plate-set/zoom-w948/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| assets/promo/plate-set/zoom-w952/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| assets/promo/plate-set/zoom-w953/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| assets/promo/plate-set/zoom-w974/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| dataset/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| dataset/entities/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| docs/00-导读/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| docs/07-学以致用/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| docs/08-提升认知/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| docs/09-精神塑造/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| docs/12-提示词库/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| docs/_templates/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| docs/_templates/duipai/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| docs/agent-guardrails/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| docs/agent/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| docs/superpowers/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| docs/superpowers/plans/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| hyperframes/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| hyperframes/compositions/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| hyperframes/compositions/d3-visualizations/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| hyperframes/output/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| mcp-server/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| packaging/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| packaging/xiyouji-analysis/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| packaging/xiyouji-analysis/src/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| packaging/xiyouji-analysis/src/xiyouji_analysis/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/AA_叙事实验/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/AB_视觉艺术/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/AC_方法论矩阵/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/AD_认知心理/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/AE_生态学/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/AF_法理经济/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/AG_物质考古/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/AH_语言学/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/B_人物/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/C_情节/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/D_关系/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/E_地理/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/G_哲学/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/H_风险与项目/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/I_妖怪社会学/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/J_权力与资源/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/K_命运与轮回/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/L_商业模型/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/M_洞府房产/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/N_法术阵法/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/O_美学时尚/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/P_音乐声效/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/Q_源流演变/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/R_解构作品/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/S_全球模式/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/T_反事实推断/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/U_文化错位/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/V_打工人职场/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/W_社媒人设/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/X_游戏网文/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/Y_伦理消费/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/Z_图表设计/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| scripts/AA_叙事实验/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| scripts/AB_视觉艺术/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| scripts/AC_方法论矩阵/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| scripts/AD_认知心理/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| scripts/AE_生态学/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| scripts/AF_法理经济/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| scripts/AG_物质考古/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| scripts/AH_语言学/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| scripts/A_文本基础/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| scripts/B_人物/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| scripts/C_情节/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| scripts/D_关系/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| scripts/E_地理/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| scripts/F_时间/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| scripts/G_哲学/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| scripts/H_风险与项目/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| scripts/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| scripts/I_妖怪社会学/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| scripts/J_权力与资源/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| scripts/K_命运与轮回/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| scripts/L_商业模型/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| scripts/M_洞府房产/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| scripts/N_法术阵法/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| scripts/O_美学时尚/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| scripts/P_音乐声效/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| scripts/Q_源流演变/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| scripts/R_解构作品/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| scripts/S_全球模式/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| scripts/T_反事实推断/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| scripts/U_文化错位/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| scripts/V_打工人职场/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| scripts/W_社媒人设/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| scripts/X_游戏网文/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| scripts/Y_伦理消费/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| scripts/Z_图表设计/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| scripts/api/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| scripts/audit/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| scripts/guardrails/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| scripts/lib/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| scripts/output/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| scripts/output/data/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| scripts/output/figures/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| scripts/rag/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| scripts/rag/eval/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| scripts/utils/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| site/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| site/chapters/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| site/characters/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| site/data/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| site/data/json/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| site/en/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| site/en/json/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| site/js/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| site/reader/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| site/reader/culture/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| site/reader/essays/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| site/reader/people/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| site/reader/poetry/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| site/reader/themes/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| site/static/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| site/static/css/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| site/static/fonts/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| site/static/icons/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| site/static/icons/ui/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| site/static/images/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| site/static/img/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| site/static/js/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| site/themes/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| source/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| source/原文/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| source/原文/shendu/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| source/原文/分回/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| source/引用与网络解读/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| tests/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| tests/e2e/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| tests/e2e/baseline/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| tests/fixtures/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| tests/unit/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| xiyouji-agent-web/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| xiyouji-agent-web/deploy/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| xiyouji-agent-web/deploy/pg/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| xiyouji-agent-web/deploy/pg/bin/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| xiyouji-agent-web/deploy/pg/migrations/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| xiyouji-agent-web/e2e/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| xiyouji-agent-web/evals/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| xiyouji-agent-web/server/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| xiyouji-agent-web/server/engine/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| xiyouji-agent-web/server/storage/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| xiyouji-agent-web/src/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| xiyouji-agent-web/src/components/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| xiyouji-agent-web/src/components/toolCalls/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| xiyouji-agent-web/src/hooks/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| xiyouji-agent-web/src/pages/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| xiyouji-agent-web/src/test/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| xiyouji-agent-web/src/utils/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| xiyouji-desktop/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| xiyouji-desktop/assets/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| xiyouji-desktop/scripts/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| xiyouji-desktop/src/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| xiyouji-desktop/tests/INDEX.md | W1096 | 目录清单改名（index.md → INDEX.md·全仓统一） |
| .github/ISSUE_TEMPLATE/README.md | W1096 | 目录导读（引用文字同步） |
| STRUCTURE.md | W1096 | 治理面 |
| archive/docs/README.md | W1096 | 目录导读（引用文字同步） |
| archive/docs/_dev/README.md | W1096 | 目录导读（引用文字同步） |
| archive/docs/_dev/产品管理套件应用-2026-10-02/README.md | W1096 | 目录导读（引用文字同步） |
| archive/docs/_dev/科技服务顾问-数字人文资助渠道-2026-10-02/README.md | W1096 | 目录导读（引用文字同步） |
| archive/docs/plans/README.md | W1096 | 目录导读（引用文字同步） |
| archive/docs/specs/README.md | W1096 | 目录导读（引用文字同步） |
| archive/docs/w550-shot-review/README.md | W1096 | 目录导读（引用文字同步） |
| archive/docs/复盘报告/README.md | W1096 | 目录导读（引用文字同步） |
| archive/scripts/README.md | W1096 | 目录导读（引用文字同步） |
| archive/scripts/batches/README.md | W1096 | 目录导读（引用文字同步） |
| archive/scripts/batches/misc/README.md | W1096 | 目录导读（引用文字同步） |
| archive/scripts/batches/w1071/README.md | W1096 | 目录导读（引用文字同步） |
| archive/scripts/batches/w1073/README.md | W1096 | 目录导读（引用文字同步） |
| archive/scripts/batches/w1074/README.md | W1096 | 目录导读（引用文字同步） |
| archive/scripts/batches/w1076/README.md | W1096 | 目录导读（引用文字同步） |
| archive/scripts/batches/w1078/README.md | W1096 | 目录导读（引用文字同步） |
| archive/scripts/batches/w1079/README.md | W1096 | 目录导读（引用文字同步） |
| archive/scripts/batches/w1080/README.md | W1096 | 目录导读（引用文字同步） |
| archive/scripts/batches/w1089/README.md | W1096 | 目录导读（引用文字同步） |
| archive/scripts/batches/w10xx/README.md | W1096 | 目录导读（引用文字同步） |
| archive/scripts/batches/w4xx/README.md | W1096 | 目录导读（引用文字同步） |
| archive/scripts/batches/w5xx/README.md | W1096 | 目录导读（引用文字同步） |
| archive/scripts/batches/w6xx/README.md | W1096 | 目录导读（引用文字同步） |
| archive/scripts/batches/w7xx/README.md | W1096 | 目录导读（引用文字同步） |
| archive/scripts/batches/w8xx/README.md | W1096 | 目录导读（引用文字同步） |
| archive/scripts/batches/w9xx/README.md | W1096 | 目录导读（引用文字同步） |
| archive/scripts/review-pass3/README.md | W1096 | 目录导读（引用文字同步） |
| archive/scripts/review-pass3/prompts/README.md | W1096 | 目录导读（引用文字同步） |
| assets/README.md | W1096 | 目录导读（引用文字同步） |
| assets/design/ai-concepts/README.md | W1096 | 目录导读（引用文字同步） |
| assets/design/alternatives/README.md | W1096 | 目录导读（引用文字同步） |
| assets/design/logo/README.md | W1096 | 目录导读（引用文字同步） |
| assets/design/process/README.md | W1096 | 目录导读（引用文字同步） |
| assets/design/screenshots/README.md | W1096 | 目录导读（引用文字同步） |
| assets/design/tools/README.md | W1096 | 目录导读（引用文字同步） |
| assets/fonts/README.md | W1096 | 目录导读（引用文字同步） |
| assets/fonts/source/README.md | W1096 | 目录导读（引用文字同步） |
| assets/images/README.md | W1096 | 目录导读（引用文字同步） |
| assets/maps/README.md | W1096 | 目录导读（引用文字同步） |
| assets/promo/README.md | W1096 | 目录导读（引用文字同步） |
| assets/promo/hero-set/README.md | W1096 | 目录导读（引用文字同步） |
| assets/promo/hero-set/raw/round-w1005/README.md | W1096 | 目录导读（引用文字同步） |
| assets/promo/output/README.md | W1096 | 目录导读（引用文字同步） |
| assets/promo/plate-set/README.md | W1096 | 目录导读（引用文字同步） |
| assets/promo/plate-set/raw/README.md | W1096 | 目录导读（引用文字同步） |
| assets/promo/plate-set/raw/round1/README.md | W1096 | 目录导读（引用文字同步） |
| assets/promo/plate-set/raw/round10/README.md | W1096 | 目录导读（引用文字同步） |
| assets/promo/plate-set/raw/round11/README.md | W1096 | 目录导读（引用文字同步） |
| assets/promo/plate-set/raw/round12/README.md | W1096 | 目录导读（引用文字同步） |
| assets/promo/plate-set/raw/round13/README.md | W1096 | 目录导读（引用文字同步） |
| assets/promo/plate-set/raw/round14/README.md | W1096 | 目录导读（引用文字同步） |
| assets/promo/plate-set/raw/round15/README.md | W1096 | 目录导读（引用文字同步） |
| assets/promo/plate-set/raw/round16/README.md | W1096 | 目录导读（引用文字同步） |
| assets/promo/plate-set/raw/round17/README.md | W1096 | 目录导读（引用文字同步） |
| assets/promo/plate-set/raw/round18/README.md | W1096 | 目录导读（引用文字同步） |
| assets/promo/plate-set/raw/round2/README.md | W1096 | 目录导读（引用文字同步） |
| assets/promo/plate-set/raw/round3/README.md | W1096 | 目录导读（引用文字同步） |
| assets/promo/plate-set/raw/round4/README.md | W1096 | 目录导读（引用文字同步） |
| assets/promo/plate-set/raw/round5/README.md | W1096 | 目录导读（引用文字同步） |
| assets/promo/plate-set/raw/round6/README.md | W1096 | 目录导读（引用文字同步） |
| assets/promo/plate-set/raw/round7/README.md | W1096 | 目录导读（引用文字同步） |
| assets/promo/plate-set/raw/round8/README.md | W1096 | 目录导读（引用文字同步） |
| assets/promo/plate-set/raw/round9/README.md | W1096 | 目录导读（引用文字同步） |
| assets/promo/plate-set/zoom-w948/README.md | W1096 | 目录导读（引用文字同步） |
| assets/promo/plate-set/zoom-w952/README.md | W1096 | 目录导读（引用文字同步） |
| assets/promo/plate-set/zoom-w953/README.md | W1096 | 目录导读（引用文字同步） |
| assets/promo/plate-set/zoom-w974/README.md | W1096 | 目录导读（引用文字同步） |
| dataset/entities/README.md | W1096 | 目录导读（引用文字同步） |
| docs/00-导读/协议边界速查.md | W1096 | 文档 |
| docs/12-提示词库/README.md | W1096 | 目录导读（引用文字同步） |
| docs/INDEX.md | W1096 | 文档 |
| docs/README.md | W1096 | 目录导读（引用文字同步） |
| docs/_templates/README.md | W1096 | 目录导读（引用文字同步） |
| docs/agent-guardrails/README.md | W1096 | 目录导读（引用文字同步） |
| docs/agent/README.md | W1096 | 目录导读（引用文字同步） |
| docs/agent/gates.md | W1096 | 治理面 |
| docs/superpowers/README.md | W1096 | 目录导读（引用文字同步） |
| docs/superpowers/plans/README.md | W1096 | 目录导读（引用文字同步） |
| hyperframes/compositions/README.md | W1096 | 目录导读（引用文字同步） |
| hyperframes/compositions/d3-visualizations/README.md | W1096 | 目录导读（引用文字同步） |
| hyperframes/output/README.md | W1096 | 目录导读（引用文字同步） |
| packaging/README.md | W1096 | 目录导读（引用文字同步） |
| packaging/xiyouji-analysis/src/README.md | W1096 | 目录导读（引用文字同步） |
| packaging/xiyouji-analysis/src/xiyouji_analysis/README.md | W1096 | 目录导读（引用文字同步） |
| packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/AA_叙事实验/README.md | W1096 | 目录导读（引用文字同步） |
| packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/AB_视觉艺术/README.md | W1096 | 目录导读（引用文字同步） |
| packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/AC_方法论矩阵/README.md | W1096 | 目录导读（引用文字同步） |
| packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/AD_认知心理/README.md | W1096 | 目录导读（引用文字同步） |
| packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/AE_生态学/README.md | W1096 | 目录导读（引用文字同步） |
| packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/AF_法理经济/README.md | W1096 | 目录导读（引用文字同步） |
| packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/AG_物质考古/README.md | W1096 | 目录导读（引用文字同步） |
| packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/AH_语言学/README.md | W1096 | 目录导读（引用文字同步） |
| packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/B_人物/README.md | W1096 | 目录导读（引用文字同步） |
| packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/C_情节/README.md | W1096 | 目录导读（引用文字同步） |
| packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/D_关系/README.md | W1096 | 目录导读（引用文字同步） |
| packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/E_地理/README.md | W1096 | 目录导读（引用文字同步） |
| packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/G_哲学/README.md | W1096 | 目录导读（引用文字同步） |
| packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/H_风险与项目/README.md | W1096 | 目录导读（引用文字同步） |
| packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/I_妖怪社会学/README.md | W1096 | 目录导读（引用文字同步） |
| packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/J_权力与资源/README.md | W1096 | 目录导读（引用文字同步） |
| packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/K_命运与轮回/README.md | W1096 | 目录导读（引用文字同步） |
| packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/L_商业模型/README.md | W1096 | 目录导读（引用文字同步） |
| packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/M_洞府房产/README.md | W1096 | 目录导读（引用文字同步） |
| packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/N_法术阵法/README.md | W1096 | 目录导读（引用文字同步） |
| packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/O_美学时尚/README.md | W1096 | 目录导读（引用文字同步） |
| packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/P_音乐声效/README.md | W1096 | 目录导读（引用文字同步） |
| packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/Q_源流演变/README.md | W1096 | 目录导读（引用文字同步） |
| packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/README.md | W1096 | 目录导读（引用文字同步） |
| packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/R_解构作品/README.md | W1096 | 目录导读（引用文字同步） |
| packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/S_全球模式/README.md | W1096 | 目录导读（引用文字同步） |
| packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/T_反事实推断/README.md | W1096 | 目录导读（引用文字同步） |
| packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/U_文化错位/README.md | W1096 | 目录导读（引用文字同步） |
| packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/V_打工人职场/README.md | W1096 | 目录导读（引用文字同步） |
| packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/W_社媒人设/README.md | W1096 | 目录导读（引用文字同步） |
| packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/X_游戏网文/README.md | W1096 | 目录导读（引用文字同步） |
| packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/Y_伦理消费/README.md | W1096 | 目录导读（引用文字同步） |
| packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/Z_图表设计/README.md | W1096 | 目录导读（引用文字同步） |
| scripts/AA_叙事实验/README.md | W1096 | 本批工具/产物 |
| scripts/AB_视觉艺术/README.md | W1096 | 本批工具/产物 |
| scripts/AC_方法论矩阵/README.md | W1096 | 本批工具/产物 |
| scripts/AD_认知心理/README.md | W1096 | 本批工具/产物 |
| scripts/AE_生态学/README.md | W1096 | 本批工具/产物 |
| scripts/AF_法理经济/README.md | W1096 | 本批工具/产物 |
| scripts/AG_物质考古/README.md | W1096 | 本批工具/产物 |
| scripts/AH_语言学/README.md | W1096 | 本批工具/产物 |
| scripts/A_文本基础/README.md | W1096 | 本批工具/产物 |
| scripts/B_人物/README.md | W1096 | 本批工具/产物 |
| scripts/C_情节/README.md | W1096 | 本批工具/产物 |
| scripts/D_关系/README.md | W1096 | 本批工具/产物 |
| scripts/E_地理/README.md | W1096 | 本批工具/产物 |
| scripts/F_时间/README.md | W1096 | 本批工具/产物 |
| scripts/G_哲学/README.md | W1096 | 本批工具/产物 |
| scripts/H_风险与项目/README.md | W1096 | 本批工具/产物 |
| scripts/I_妖怪社会学/README.md | W1096 | 本批工具/产物 |
| scripts/J_权力与资源/README.md | W1096 | 本批工具/产物 |
| scripts/K_命运与轮回/README.md | W1096 | 本批工具/产物 |
| scripts/L_商业模型/README.md | W1096 | 本批工具/产物 |
| scripts/M_洞府房产/README.md | W1096 | 本批工具/产物 |
| scripts/N_法术阵法/README.md | W1096 | 本批工具/产物 |
| scripts/O_美学时尚/README.md | W1096 | 本批工具/产物 |
| scripts/P_音乐声效/README.md | W1096 | 本批工具/产物 |
| scripts/Q_源流演变/README.md | W1096 | 本批工具/产物 |
| scripts/R_解构作品/README.md | W1096 | 本批工具/产物 |
| scripts/S_全球模式/README.md | W1096 | 本批工具/产物 |
| scripts/T_反事实推断/README.md | W1096 | 本批工具/产物 |
| scripts/U_文化错位/README.md | W1096 | 本批工具/产物 |
| scripts/V_打工人职场/README.md | W1096 | 本批工具/产物 |
| scripts/W_社媒人设/README.md | W1096 | 本批工具/产物 |
| scripts/X_游戏网文/README.md | W1096 | 本批工具/产物 |
| scripts/Y_伦理消费/README.md | W1096 | 本批工具/产物 |
| scripts/Z_图表设计/README.md | W1096 | 本批工具/产物 |
| scripts/api/README.md | W1096 | 本批工具/产物 |
| scripts/audit/README.md | W1096 | 本批工具/产物 |
| scripts/check_folder_docs.py | W1096 | 本批工具/产物 |
| scripts/check_repo_layout.py | W1096 | 本批工具/产物 |
| scripts/docs_index.py | W1096 | 本批工具/产物 |
| scripts/gen_folder_docs.py | W1096 | 本批工具/产物 |
| scripts/guardrails/README.md | W1096 | 本批工具/产物 |
| scripts/lib/README.md | W1096 | 本批工具/产物 |
| scripts/output/README.md | W1096 | 本批工具/产物 |
| scripts/output/data/README.md | W1096 | 本批工具/产物 |
| scripts/output/figures/README.md | W1096 | 本批工具/产物 |
| scripts/output/file-index.md | W1096 | 治理面 |
| scripts/output/stats-changelog.json | W1096 | 本批工具/产物 |
| scripts/output/stats-index.md | W1096 | 本批工具/产物 |
| scripts/output/stats.json | W1096 | 本批工具/产物 |
| scripts/output/tools-inventory.md | W1096 | 本批工具/产物 |
| scripts/rag/eval/README.md | W1096 | 本批工具/产物 |
| scripts/utils/README.md | W1096 | 本批工具/产物 |
| site/README.md | W1096 | 页面 |
| site/chapters/README.md | W1096 | 页面 |
| site/characters/README.md | W1096 | 页面 |
| site/data/README.md | W1096 | 页面 |
| site/data/json/README.md | W1096 | 页面 |
| site/data/search.html | W1096 | 页面 |
| site/en/json/README.md | W1096 | 页面 |
| site/en/search.html | W1096 | 页面 |
| site/js/README.md | W1096 | 页面 |
| site/reader/README.md | W1096 | 页面 |
| site/reader/culture/README.md | W1096 | 页面 |
| site/reader/essays/README.md | W1096 | 页面 |
| site/reader/people/README.md | W1096 | 页面 |
| site/reader/poetry/README.md | W1096 | 页面 |
| site/reader/themes/README.md | W1096 | 页面 |
| site/static/README.md | W1096 | 页面 |
| site/static/css/README.md | W1096 | 页面 |
| site/static/fonts/README.md | W1096 | 页面 |
| site/static/icons/README.md | W1096 | 页面 |
| site/static/icons/ui/README.md | W1096 | 页面 |
| site/static/images/README.md | W1096 | 页面 |
| site/static/img/README.md | W1096 | 页面 |
| site/static/js/README.md | W1096 | 页面 |
| site/themes/README.md | W1096 | 页面 |
| source/README.md | W1096 | 目录导读（引用文字同步） |
| source/原文/README.md | W1096 | 目录导读（引用文字同步） |
| source/原文/shendu/README.md | W1096 | 目录导读（引用文字同步） |
| source/原文/分回/README.md | W1096 | 目录导读（引用文字同步） |
| source/引用与网络解读/README.md | W1096 | 目录导读（引用文字同步） |
| tests/README.md | W1096 | 目录导读（引用文字同步） |
| tests/e2e/README.md | W1096 | 目录导读（引用文字同步） |
| tests/e2e/baseline/README.md | W1096 | 目录导读（引用文字同步） |
| tests/fixtures/README.md | W1096 | 目录导读（引用文字同步） |
| tests/unit/README.md | W1096 | 目录导读（引用文字同步） |
| tests/unit/test_folder_docs_gate.py | W1096 | 文档 |
| xiyouji-agent-web/deploy/README.md | W1096 | 目录导读（引用文字同步） |
| xiyouji-agent-web/deploy/pg/bin/README.md | W1096 | 目录导读（引用文字同步） |
| xiyouji-agent-web/deploy/pg/migrations/README.md | W1096 | 目录导读（引用文字同步） |
| xiyouji-agent-web/e2e/README.md | W1096 | 目录导读（引用文字同步） |
| xiyouji-agent-web/evals/README.md | W1096 | 目录导读（引用文字同步） |
| xiyouji-agent-web/server/README.md | W1096 | 目录导读（引用文字同步） |
| xiyouji-agent-web/server/engine/README.md | W1096 | 目录导读（引用文字同步） |
| xiyouji-agent-web/server/storage/README.md | W1096 | 目录导读（引用文字同步） |
| xiyouji-agent-web/src/README.md | W1096 | 目录导读（引用文字同步） |
| xiyouji-agent-web/src/components/README.md | W1096 | 目录导读（引用文字同步） |
| xiyouji-agent-web/src/components/toolCalls/README.md | W1096 | 目录导读（引用文字同步） |
| xiyouji-agent-web/src/hooks/README.md | W1096 | 目录导读（引用文字同步） |
| xiyouji-agent-web/src/pages/README.md | W1096 | 目录导读（引用文字同步） |
| xiyouji-agent-web/src/test/README.md | W1096 | 目录导读（引用文字同步） |
| xiyouji-agent-web/src/utils/README.md | W1096 | 目录导读（引用文字同步） |
| xiyouji-desktop/assets/README.md | W1096 | 目录导读（引用文字同步） |
| xiyouji-desktop/scripts/README.md | W1096 | 目录导读（引用文字同步） |
| xiyouji-desktop/src/README.md | W1096 | 目录导读（引用文字同步） |
| xiyouji-desktop/tests/README.md | W1096 | 目录导读（引用文字同步） |

## W1094 图表色工程批·档 1 尾批（2026-11-02）

| 文件 | W | 说明 |
|---|---|---|
| site/en/hardship-difficulty-heatmap.html | W1094 | 页面 |
| site/en/hardship-heatmap.html | W1094 | 页面 |
| site/en/journey-spacetime.html | W1094 | 页面 |
| site/en/magic-system.html | W1094 | 页面 |
| site/en/monster-sociology.html | W1094 | 页面 |
| site/en/philosophy.html | W1094 | 页面 |
| site/en/pilgrim-team-psychology-arc.html | W1094 | 页面 |
| docs/11-方案报告/计划方案/T49-任务计划执行与经验沉淀报告-2026-11-02.md | W1094 | 治理文档 |
| docs/11-方案报告/README.md | W1094 | 治理文档 |
| docs/00-导读/W批次编号对账表.md | W1094 | 治理文档 |
| scripts/output/_w1094_spec.json | W1094 | 本批工具/产物 |
| STRUCTURE.md | W1094 | 治理文档 |
| docs/11-方案报告/计划方案/T47-任务计划执行与经验沉淀报告-2026-11-02.md | W1094 | 治理文档 |
| docs/11-方案报告/计划方案/T48-任务计划执行与经验沉淀报告-2026-11-02.md | W1094 | 治理文档 |
| docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md | W1094 | 治理文档 |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1094 | 治理文档 |
| docs/INDEX.md | W1094 | 治理文档 |
| scripts/output/README.md | W1094 | 本批工具/产物 |
| scripts/output/index.md | W1094 | 本批工具/产物 |
| scripts/output/stats-changelog.json | W1094 | 本批工具/产物 |
| scripts/output/stats-index.md | W1094 | 本批工具/产物 |
| scripts/output/stats.json | W1094 | 本批工具/产物 |
| scripts/output/tools-inventory.md | W1094 | 本批工具/产物 |
| site/data/search.html | W1094 | 页面 |
| site/en/search.html | W1094 | 页面 |
| .github/workflows/README.md | W1094 | 治理文档 |
| AGENTS.md | W1094 | 治理文档 |
| CHANGELOG.md | W1094 | 治理文档 |
| CITATION.cff | W1094 | 治理文档 |
| HANDOVER.md | W1094 | 治理文档 |
| README.md | W1094 | 治理文档 |
| archive/docs/AGENTS-ARCHIVE.md | W1094 | 治理文档 |
| archive/docs/CHANGELOG-ARCHIVE.md | W1094 | 治理文档 |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1094 | 治理文档 |
| archive/docs/file-index-ARCHIVE.md | W1094 | 治理文档 |
| docs/00-导读/项目说明.md | W1094 | 治理文档 |
| scripts/output/_cascade_files_W1094.txt | W1094 | 本批工具/产物 |
| scripts/output/file-index.md | W1094 | 本批工具/产物 |
| site/data/cross-time-danmaku.html | W1094 | 页面 |
| site/data/tag-cloud.html | W1094 | 页面 |
| site/dukou-engine.html | W1094 | 页面 |
| site/index.html | W1094 | 页面 |
| scripts/output/_vermilion_solid_cache.json | W1094 | 本批工具/产物 |
| tmp_ledger_head.md | W1094 | 治理文档 |
| tmp_readme_head.md | W1094 | 治理文档 |
| tmp_t50_head.md | W1094 | 治理文档 |

## W1090 J2 视觉回归探针扩展（2026-11-02）

| 文件 | W | 说明 |
|---|---|---|
| scripts/visual_regression_probe.py | W1090 | 本批工具/产物 |
| tests/unit/test_w851_visual_regression_probe.py | W1090 | 本批工具/产物 |
| scripts/output/README.md | W1090 | 本批工具/产物 |
| scripts/output/_cascade_files_W1090.txt | W1090 | 本批工具/产物 |
| scripts/output/_vermilion_solid_cache.json | W1090 | 本批工具/产物 |
| scripts/output/_w1090_spec.json | W1090 | 本批工具/产物 |
| scripts/output/file-index.md | W1090 | 本批工具/产物 |
| scripts/output/index.md | W1090 | 本批工具/产物 |
| scripts/output/stats-changelog.json | W1090 | 本批工具/产物 |
| scripts/output/stats-index.md | W1090 | 本批工具/产物 |
| scripts/output/stats.json | W1090 | 本批工具/产物 |
| scripts/output/tools-inventory.md | W1090 | 本批工具/产物 |
| .github/workflows/README.md | W1090 | 治理文档 |
| .agent/skills/puti-shouye/SKILL.md | W1090 | 治理文档 |
| AGENTS.md | W1090 | 治理文档 |
| CHANGELOG.md | W1090 | 治理文档 |
| CITATION.cff | W1090 | 治理文档 |
| HANDOVER.md | W1090 | 治理文档 |
| README.md | W1090 | 治理文档 |
| STRUCTURE.md | W1090 | 治理文档 |
| archive/docs/AGENTS-ARCHIVE.md | W1090 | 治理文档 |
| archive/docs/CHANGELOG-ARCHIVE.md | W1090 | 治理文档 |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1090 | 治理文档 |
| archive/docs/file-index-ARCHIVE.md | W1090 | 治理文档 |
| docs/00-导读/W批次编号对账表.md | W1090 | 治理文档 |
| docs/00-导读/项目说明.md | W1090 | 治理文档 |
| docs/11-方案报告/README.md | W1090 | 治理文档 |
| docs/11-方案报告/计划方案/T48-任务计划执行与经验沉淀报告-2026-11-02.md | W1090 | 治理文档 |
| docs/agent/pitfalls.md | W1090 | 治理文档 |
| archive/scripts/batches/w1089/index.md | W1090 | 治理文档 |
| docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md | W1090 | 治理文档 |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1090 | 治理文档 |
| docs/INDEX.md | W1090 | 治理文档 |
| pytest.ini | W1090 | 治理文档 |
| site/data/cross-time-danmaku.html | W1090 | 页面 |
| site/data/search.html | W1090 | 页面 |
| site/data/tag-cloud.html | W1090 | 页面 |
| site/dukou-engine.html | W1090 | 页面 |
| site/en/search.html | W1090 | 页面 |
| site/index.html | W1090 | 页面 |
| tests/unit/test_w851_visual_regression_probe.py | W1090 | 治理文档 |
| scripts/output/design-tokens.json | W1090 | 本批工具/产物 |

## W1089 图表色工程批·档 1 扩展批 1（2026-11-02）

| 文件 | W | 说明 |
|---|---|---|
| site/en/visual-art.html | W1089 | 页面 |
| site/en/karma-reincarnation.html | W1089 | 页面 |
| site/en/risk-project.html | W1089 | 页面 |
| site/en/monster-capability-radar.html | W1089 | 页面 |
| site/en/journey-map-interactive.html | W1089 | 页面 |
| site/en/poetry-rhythm-analysis.html | W1089 | 页面 |
| archive/scripts/batches/w1089/_w1089_chart_color_shapes.py | W1089 | 本批工具/产物 |
| scripts/chart_render_probe.py | W1089 | 本批工具/产物 |
| scripts/output/README.md | W1089 | 本批工具/产物 |
| scripts/output/_cascade_files_W1089.txt | W1089 | 本批工具/产物 |
| scripts/output/_vermilion_solid_cache.json | W1089 | 本批工具/产物 |
| scripts/output/_w1089_shapes_after.json | W1089 | 本批工具/产物 |
| scripts/output/_w1089_shapes_before.json | W1089 | 本批工具/产物 |
| scripts/output/_w1089_spec.json | W1089 | 本批工具/产物 |
| scripts/output/_w1089_style_fill_stroke_after.json | W1089 | 本批工具/产物 |
| scripts/output/_w1089_style_fill_stroke_before.json | W1089 | 本批工具/产物 |
| scripts/output/file-index.md | W1089 | 本批工具/产物 |
| scripts/output/index.md | W1089 | 本批工具/产物 |
| scripts/output/stats-changelog.json | W1089 | 本批工具/产物 |
| scripts/output/stats-index.md | W1089 | 本批工具/产物 |
| scripts/output/stats.json | W1089 | 本批工具/产物 |
| scripts/output/tools-inventory.md | W1089 | 本批工具/产物 |
| .github/workflows/README.md | W1089 | 治理文档 |
| .agent/skills/puti-shouye/SKILL.md | W1089 | 治理文档 |
| AGENTS.md | W1089 | 治理文档 |
| CHANGELOG.md | W1089 | 治理文档 |
| CITATION.cff | W1089 | 治理文档 |
| HANDOVER.md | W1089 | 治理文档 |
| README.md | W1089 | 治理文档 |
| STRUCTURE.md | W1089 | 治理文档 |
| archive/docs/AGENTS-ARCHIVE.md | W1089 | 治理文档 |
| archive/docs/CHANGELOG-ARCHIVE.md | W1089 | 治理文档 |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1089 | 治理文档 |
| archive/docs/file-index-ARCHIVE.md | W1089 | 治理文档 |
| docs/00-导读/W批次编号对账表.md | W1089 | 治理文档 |
| docs/00-导读/项目说明.md | W1089 | 治理文档 |
| docs/11-方案报告/README.md | W1089 | 治理文档 |
| docs/11-方案报告/计划方案/T47-任务计划执行与经验沉淀报告-2026-11-02.md | W1089 | 治理文档 |
| docs/agent/pitfalls.md | W1089 | 治理文档 |
| scripts/output/_w1089_probe_after_en__visual-art.html.json | W1089 | 本批工具/产物 |
| scripts/output/_w1089_probe_before_en__visual-art.html.json | W1089 | 本批工具/产物 |
| scripts/output/_w1089_probe_after_en__karma-reincarnation.html.json | W1089 | 本批工具/产物 |
| scripts/output/_w1089_probe_before_en__karma-reincarnation.html.json | W1089 | 本批工具/产物 |
| scripts/output/_w1089_probe_after_en__risk-project.html.json | W1089 | 本批工具/产物 |
| scripts/output/_w1089_probe_before_en__risk-project.html.json | W1089 | 本批工具/产物 |
| scripts/output/_w1089_probe_after_en__monster-capability-radar.html.json | W1089 | 本批工具/产物 |
| scripts/output/_w1089_probe_before_en__monster-capability-radar.html.json | W1089 | 本批工具/产物 |
| scripts/output/_w1089_probe_after_en__journey-map-interactive.html.json | W1089 | 本批工具/产物 |
| scripts/output/_w1089_probe_before_en__journey-map-interactive.html.json | W1089 | 本批工具/产物 |
| scripts/output/_w1089_probe_after_en__poetry-rhythm-analysis.html.json | W1089 | 本批工具/产物 |
| scripts/output/_w1089_probe_before_en__poetry-rhythm-analysis.html.json | W1089 | 本批工具/产物 |
| archive/scripts/batches/README.md | W1089 | 本批工具/产物 |
| archive/scripts/batches/index.md | W1089 | 本批工具/产物 |
| archive/scripts/batches/w1089/README.md | W1089 | 本批工具/产物 |
| archive/scripts/batches/w1089/index.md | W1089 | 本批工具/产物 |
| docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md | W1089 | 治理文档 |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1089 | 治理文档 |
| docs/INDEX.md | W1089 | 治理文档 |
| site/data/cross-time-danmaku.html | W1089 | 页面 |
| site/data/search.html | W1089 | 页面 |
| site/data/tag-cloud.html | W1089 | 页面 |
| site/dukou-engine.html | W1089 | 页面 |
| site/en/search.html | W1089 | 页面 |
| site/index.html | W1089 | 页面 |

## W1086 图表色工程批·档 1 试点施工（2026-11-02）

| 文件 | W | 说明 |
|---|---|---|
| .github/workflows/README.md | W1086 | 治理文档 |
| .agent/skills/puti-shouye/SKILL.md | W1086 | 治理文档 |
| AGENTS.md | W1086 | 治理文档 |
| CHANGELOG.md | W1086 | 治理文档 |
| CITATION.cff | W1086 | 治理文档 |
| HANDOVER.md | W1086 | 治理文档 |
| README.md | W1086 | 治理文档 |
| STRUCTURE.md | W1086 | 治理文档 |
| archive/docs/AGENTS-ARCHIVE.md | W1086 | 治理文档 |
| archive/docs/CHANGELOG-ARCHIVE.md | W1086 | 治理文档 |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1086 | 治理文档 |
| archive/docs/file-index-ARCHIVE.md | W1086 | 治理文档 |
| docs/00-导读/W批次编号对账表.md | W1086 | 治理文档 |
| docs/00-导读/项目说明.md | W1086 | 治理文档 |
| docs/11-方案报告/README.md | W1086 | 治理文档 |
| docs/11-方案报告/计划方案/T44-任务计划执行与经验沉淀报告-2026-11-02.md | W1086 | 治理文档 |
| docs/11-方案报告/计划方案/T45-任务计划执行与经验沉淀报告-2026-11-02.md | W1086 | 治理文档 |
| docs/11-方案报告/计划方案/T46-任务计划执行与经验沉淀报告-2026-11-02.md | W1086 | 治理文档 |
| docs/agent/pitfalls.md | W1086 | 治理文档 |
| scripts/chart_render_probe.py | W1086 | 本批工具/产物 |
| scripts/output/README.md | W1086 | 本批工具/产物 |
| scripts/output/_cascade_files_W1086.txt | W1086 | 本批工具/产物 |
| scripts/output/_vermilion_solid_cache.json | W1086 | 本批工具/产物 |
| scripts/output/_w1086_j2_after | W1086 | 本批工具/产物 |
| scripts/output/_w1086_j2_before_1page.json | W1086 | 本批工具/产物 |
| scripts/output/_w1086_probe.json | W1086 | 本批工具/产物 |
| scripts/output/_w1086_spec.json | W1086 | 本批工具/产物 |
| scripts/output/file-index.md | W1086 | 本批工具/产物 |
| scripts/output/index.md | W1086 | 本批工具/产物 |
| scripts/output/stats.json | W1086 | 本批工具/产物 |
| scripts/output/tools-inventory.md | W1086 | 本批工具/产物 |
| site/data/cross-time-danmaku.html | W1086 | 页面 |
| site/data/search.html | W1086 | 页面 |
| site/data/tag-cloud.html | W1086 | 页面 |
| site/dukou-engine.html | W1086 | 页面 |
| site/en/global-pattern.html | W1086 | 页面 |
| site/en/search.html | W1086 | 页面 |
| site/index.html | W1086 | 页面 |
| tests/unit/README.md | W1086 | 本批工具/产物 |
| tests/unit/index.md | W1086 | 本批工具/产物 |
| tests/unit/test_chart_render_probe.py | W1086 | 本批工具/产物 |
| docs/11-方案报告/设计与架构方案/界面与交互优化施工方案-2026-10-31.md | W1086 | 治理文档 |
| docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md | W1086 | 治理文档 |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1086 | 治理文档 |
| docs/INDEX.md | W1086 | 治理文档 |
| docs/agent/batch-closeout-checklist.md | W1086 | 治理文档 |
| scripts/output/stats-changelog.json | W1086 | 本批工具/产物 |
| scripts/output/stats-index.md | W1086 | 本批工具/产物 |
| pytest.ini | W1086 | 治理文档 |

## W1084 图表色工程批·塌缩真因定位（2026-11-02）

| 文件 | W | 说明 |
|---|---|---|
| .github/workflows/README.md | W1084 | 治理文档 |
| .agent/skills/puti-shouye/SKILL.md | W1084 | 治理文档 |
| AGENTS.md | W1084 | 治理文档 |
| CHANGELOG.md | W1084 | 治理文档 |
| CITATION.cff | W1084 | 治理文档 |
| HANDOVER.md | W1084 | 治理文档 |
| README.md | W1084 | 治理文档 |
| STRUCTURE.md | W1084 | 治理文档 |
| archive/docs/AGENTS-ARCHIVE.md | W1084 | 治理文档 |
| archive/docs/CHANGELOG-ARCHIVE.md | W1084 | 治理文档 |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1084 | 治理文档 |
| archive/docs/file-index-ARCHIVE.md | W1084 | 治理文档 |
| pytest.ini | W1084 | 治理文档 |
| docs/00-导读/W批次编号对账表.md | W1084 | 治理文档 |
| docs/00-导读/项目说明.md | W1084 | 治理文档 |
| docs/INDEX.md | W1084 | 治理文档 |
| docs/11-方案报告/README.md | W1084 | 治理文档 |
| docs/11-方案报告/计划方案/T44-任务计划执行与经验沉淀报告-2026-11-02.md | W1084 | 治理文档 |
| docs/11-方案报告/计划方案/T45-任务计划执行与经验沉淀报告-2026-11-02.md | W1084 | 治理文档 |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1084 | 治理文档 |
| docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md | W1084 | 治理文档 |
| docs/agent/pitfalls.md | W1084 | 治理文档 |
| scripts/chart_render_probe.py | W1084 | 本批工具/产物 |
| tests/unit/test_chart_render_probe.py | W1084 | 本批工具/产物 |
| tests/unit/index.md | W1084 | 本批工具/产物 |
| tests/unit/README.md | W1084 | 本批工具/产物 |
| scripts/index.md | W1084 | 本批工具/产物 |
| scripts/output/README.md | W1084 | 本批工具/产物 |
| scripts/output/_cascade_files_W1084.txt | W1084 | 本批工具/产物 |
| scripts/output/_vermilion_solid_cache.json | W1084 | 本批工具/产物 |
| scripts/output/_w1084_probe.json | W1084 | 本批工具/产物 |
| scripts/output/_w1084_probe_diag.json | W1084 | 本批工具/产物 |
| scripts/output/_w1084_spec.json | W1084 | 本批工具/产物 |
| scripts/output/file-index.md | W1084 | 本批工具/产物 |
| scripts/output/stats-changelog.json | W1084 | 本批工具/产物 |
| scripts/output/stats-index.md | W1084 | 本批工具/产物 |
| scripts/output/index.md | W1084 | 本批工具/产物 |
| scripts/output/stats.json | W1084 | 本批工具/产物 |
| scripts/output/tools-inventory.md | W1084 | 本批工具/产物 |
| site/data/cross-time-danmaku.html | W1084 | 页面 |
| site/data/search.html | W1084 | 页面 |
| site/data/tag-cloud.html | W1084 | 页面 |
| site/dukou-engine.html | W1084 | 页面 |
| site/en/search.html | W1084 | 页面 |
| site/index.html | W1084 | 页面 |

## W1083 图表色工程批·结论链自审（2026-11-02）

| 文件 | W | 说明 |
|---|---|---|
| AGENTS.md | W1083 | 治理文档 |
| CHANGELOG.md | W1083 | 治理文档 |
| HANDOVER.md | W1083 | 治理文档 |
| README.md | W1083 | 治理文档 |
| STRUCTURE.md | W1083 | 治理文档 |
| docs/00-导读/W批次编号对账表.md | W1083 | 治理文档 |
| docs/00-导读/项目说明.md | W1083 | 治理文档 |
| docs/11-方案报告/计划方案/T44-任务计划执行与经验沉淀报告-2026-11-02.md | W1083 | 治理文档 |
| scripts/output/README.md | W1083 | 本批工具/产物 |
| scripts/output/_w1083_spec.json | W1083 | 本批工具/产物 |
| scripts/output/file-index.md | W1083 | 本批工具/产物 |
| scripts/output/index.md | W1083 | 本批工具/产物 |
| scripts/output/stats.json | W1083 | 本批工具/产物 |
| scripts/output/tools-inventory.md | W1083 | 本批工具/产物 |

## W1082 图表色工程批·档 1′ 试点（2026-11-02）

| 文件 | W | 说明 |
|---|---|---|
| .agent/skills/puti-shouye/SKILL.md | W1082 | 治理文档 |
| AGENTS.md | W1082 | 治理文档 |
| CHANGELOG.md | W1082 | 治理文档 |
| HANDOVER.md | W1082 | 治理文档 |
| README.md | W1082 | 治理文档 |
| STRUCTURE.md | W1082 | 治理文档 |
| docs/00-导读/W批次编号对账表.md | W1082 | 治理文档 |
| docs/00-导读/项目说明.md | W1082 | 治理文档 |
| docs/11-方案报告/计划方案/T44-任务计划执行与经验沉淀报告-2026-11-02.md | W1082 | 治理文档 |
| docs/agent/pitfalls.md | W1082 | 治理文档 |
| scripts/output/README.md | W1082 | 本批工具/产物 |
| scripts/output/_w1082_j2_after.json | W1082 | 本批工具/产物 |
| scripts/output/_w1082_j2_diff.json | W1082 | 本批工具/产物 |
| scripts/output/_w1082_spec.json | W1082 | 本批工具/产物 |
| scripts/output/file-index.md | W1082 | 本批工具/产物 |
| scripts/output/index.md | W1082 | 本批工具/产物 |
| scripts/output/stats.json | W1082 | 本批工具/产物 |
| scripts/output/tools-inventory.md | W1082 | 本批工具/产物 |

## W1081 图表色工程批·档 1′ 因果复核与试点口径定案（2026-11-02）

| 文件 | W | 说明 |
|---|---|---|
| AGENTS.md | W1081 | 治理文档 |
| CHANGELOG.md | W1081 | 治理文档 |
| HANDOVER.md | W1081 | 治理文档 |
| README.md | W1081 | 治理文档 |
| STRUCTURE.md | W1081 | 治理文档 |
| docs/00-导读/W批次编号对账表.md | W1081 | 治理文档 |
| docs/00-导读/项目说明.md | W1081 | 治理文档 |
| docs/11-方案报告/计划方案/T44-任务计划执行与经验沉淀报告-2026-11-02.md | W1081 | 治理文档 |
| scripts/output/README.md | W1081 | 本批工具/产物 |
| scripts/output/_w1081_rev_a.json | W1081 | 本批工具/产物 |
| scripts/output/_w1081_rev_b.json | W1081 | 本批工具/产物 |
| scripts/output/_w1081_spec.json | W1081 | 本批工具/产物 |
| scripts/output/file-index.md | W1081 | 本批工具/产物 |
| scripts/output/index.md | W1081 | 本批工具/产物 |
| scripts/output/stats.json | W1081 | 本批工具/产物 |
| scripts/output/tools-inventory.md | W1081 | 本批工具/产物 |

## W1080 图表色工程批·档 1 假设证伪与回退（2026-11-02）

| 文件 | W | 说明 |
|---|---|---|
| AGENTS.md | W1080 | 治理文档 |
| CHANGELOG.md | W1080 | 治理文档 |
| HANDOVER.md | W1080 | 治理文档 |
| README.md | W1080 | 治理文档 |
| STRUCTURE.md | W1080 | 治理文档 |
| archive/scripts/batches/w1079/index.md | W1080 | 本批工具/产物 |
| archive/scripts/batches/w1080/_w1080_make_spec.py | W1080 | 本批工具/产物 |
| archive/scripts/batches/w1080/_w1080_revert_style_tokenize.py | W1080 | 本批工具/产物 |
| archive/scripts/batches/w1080/_w1080_style_tokenize.py | W1080 | 本批工具/产物 |
| docs/00-导读/W批次编号对账表.md | W1080 | 治理文档 |
| docs/00-导读/项目说明.md | W1080 | 治理文档 |
| docs/11-方案报告/计划方案/T44-任务计划执行与经验沉淀报告-2026-11-02.md | W1080 | 治理文档 |
| scripts/_w1080_make_spec.py | W1080 | 本批工具/产物 |
| scripts/_w1080_style_tokenize.py | W1080 | 本批工具/产物 |
| scripts/index.md | W1080 | 本批工具/产物 |
| scripts/output/README.md | W1080 | 本批工具/产物 |
| scripts/output/_w1080_j2_after | W1080 | 本批工具/产物 |
| scripts/output/_w1080_j2_before | W1080 | 本批工具/产物 |
| scripts/output/_w1080_j2_diff.json | W1080 | 本批工具/产物 |
| scripts/output/_w1080_spec.json | W1080 | 本批工具/产物 |
| scripts/output/file-index.md | W1080 | 本批工具/产物 |
| scripts/output/index.md | W1080 | 本批工具/产物 |
| scripts/output/stats.json | W1080 | 本批工具/产物 |
| scripts/output/tools-inventory.md | W1080 | 本批工具/产物 |

## W1079 图表色工程批·形态取证与三档方案（2026-11-02）

| 文件 | W | 说明 |
|---|---|---|
| AGENTS.md | W1079 | 治理文档 |
| CHANGELOG.md | W1079 | 治理文档 |
| HANDOVER.md | W1079 | 治理文档 |
| README.md | W1079 | 治理文档 |
| STRUCTURE.md | W1079 | 治理文档 |
| archive/scripts/batches/w1080/_w1079_js_color_shapes.py | W1079 | 本批工具/产物 |
| archive/scripts/batches/w1080/_w1079_make_spec.py | W1079 | 本批工具/产物 |
| docs/00-导读/W批次编号对账表.md | W1079 | 治理文档 |
| docs/00-导读/项目说明.md | W1079 | 治理文档 |
| docs/11-方案报告/README.md | W1079 | 治理文档 |
| docs/11-方案报告/计划方案/T44-任务计划执行与经验沉淀报告-2026-11-02.md | W1079 | 治理文档 |
| docs/INDEX.md | W1079 | 治理文档 |
| ocs/11-方案报告/README.md | W1079 | 治理文档 |
| scripts/_w1079_js_color_shapes.py | W1079 | 本批工具/产物 |
| scripts/_w1079_make_spec.py | W1079 | 本批工具/产物 |
| scripts/output/README.md | W1079 | 本批工具/产物 |
| scripts/output/_w1079_spec.json | W1079 | 本批工具/产物 |
| scripts/output/file-index.md | W1079 | 本批工具/产物 |
| scripts/output/index.md | W1079 | 本批工具/产物 |
| scripts/output/stats.json | W1079 | 本批工具/产物 |
| scripts/output/tools-inventory.md | W1079 | 本批工具/产物 |

## W1078 全站硬编码颜色盘点（2026-11-02）

| 文件 | W | 说明 |
|---|---|---|
| AGENTS.md | W1078 | 治理文档 |
| CHANGELOG.md | W1078 | 治理文档 |
| HANDOVER.md | W1078 | 治理文档 |
| README.md | W1078 | 治理文档 |
| STRUCTURE.md | W1078 | 治理文档 |
| archive/scripts/batches/w1078/_w1078_color_inventory.py | W1078 | 本批工具/产物 |
| archive/scripts/batches/w1078/_w1078_make_spec.py | W1078 | 本批工具/产物 |
| cripts/output/_w851_j1_name_audit.json | W1078 | 治理文档 |
| docs/00-导读/W批次编号对账表.md | W1078 | 治理文档 |
| docs/00-导读/项目说明.md | W1078 | 治理文档 |
| docs/11-方案报告/README.md | W1078 | 治理文档 |
| docs/11-方案报告/计划方案/T43-任务计划执行与经验沉淀报告-2026-11-02.md | W1078 | 治理文档 |
| docs/INDEX.md | W1078 | 治理文档 |
| ocs/11-方案报告/README.md | W1078 | 治理文档 |
| scripts/_w1078_color_inventory.py | W1078 | 本批工具/产物 |
| scripts/_w1078_make_spec.py | W1078 | 本批工具/产物 |
| scripts/output/README.md | W1078 | 本批工具/产物 |
| scripts/output/_w1078_color_inventory.json | W1078 | 本批工具/产物 |
| scripts/output/_w1078_color_inventory.md | W1078 | 本批工具/产物 |
| scripts/output/_w1078_spec.json | W1078 | 本批工具/产物 |
| scripts/output/file-index.md | W1078 | 本批工具/产物 |
| scripts/output/index.md | W1078 | 本批工具/产物 |
| scripts/output/stats.json | W1078 | 本批工具/产物 |
| scripts/output/tools-inventory.md | W1078 | 本批工具/产物 |

## W1077 agent-guardrails 迁移：脚本进 scripts/guardrails/·文档进 docs/agent-guardrails/（2026-11-02）

| 文件 | W | 说明 |
|---|---|---|

| CHANGELOG.md | W1077 | 治理文档 |
| CLAUDE.md | W1077 | 治理文档（规则 17 + 常用命令 2 行） |
| AGENTS.md | W1077 | 治理文档（§6-20） |
| HANDOVER.md | W1077 | 治理文档 |
| STRUCTURE.md | W1077 | 治理文档 |
| docs/index.md | W1077 | 目录索引（生成物） |
| docs/agent-guardrails/README.md | W1077 | 人工维护文档（迁移） |
| docs/agent-guardrails/merge-patch.md | W1077 | 人工维护文档（迁移） |
| docs/agent-guardrails/self-check.md | W1077 | 人工维护文档（迁移） |
| docs/agent-guardrails/index.md | W1077 | 目录索引（生成物） |
| scripts/index.md | W1077 | 目录索引（生成物） |
| scripts/guardrails/index.md | W1077 | 目录索引（生成物） |
| scripts/guardrails/README.md | W1077 | 目录索引（生成物） |
| scripts/guardrails/check_changed.ps1 | W1077 | 本批工具（迁移） |
| scripts/guardrails/check_changed.sh | W1077 | 本批工具（迁移） |
| scripts/guardrails/once_call.py | W1077 | 本批工具（迁移） |
| scripts/guardrails/api_diff.py | W1077 | 本批工具（迁移） |
| scripts/guardrails/check_nested_comprehension.py | W1077 | 本批工具（迁移） |
| scripts/guardrails/ruff-structure.toml | W1077 | 本批工具（迁移） |
| scripts/guardrails/precommit_entry.py | W1077 | pre-commit 本地 hook 入口 |
| scripts/install_hooks.sh | W1077 | 幂等安装脚本 |
| scripts/install_hooks.ps1 | W1077 | 安装脚本薄封装 |
| .pre-commit-config.yaml | W1077 | 框架本地 hook（防 install 丢失） |
| tests/index.md | W1077 | 目录索引（生成物） |
| tests/fixtures/_sample.py | W1077 | 测试 fixture（迁移） |
| tests/fixtures/index.md | W1077 | 目录索引（生成物） |
| tests/fixtures/README.md | W1077 | 目录索引（生成物） |
| .github/workflows/README.md | W1077 | 旁文档版本面（头部 + 里程碑） |
| README.md | W1077 | 治理文档（当前批次行） |
| docs/00-导读/项目说明.md | W1077 | 治理文档（当前批次 + 当前版本两处） |
| CITATION.cff | W1077 | 外部引用面版本 |
| docs/agent/pitfalls.md | W1077 | 坑表（E-73） |
| site/dukou-engine.html | W1077 | 页脚批次链（手工工件） |
| site/data/search.html | W1077 | 站内搜索索引重建（自动产物） |
| site/en/search.html | W1077 | 站内搜索索引重建（自动产物） |
| scripts/output/file-index.md | W1077 | 本文件 |
| scripts/output/index.md | W1077 | 目录索引（生成物） |
| scripts/output/_w1077_spec.json | W1077 | 本批规格 |
| scripts/output/_vermilion_solid_cache.json | W1077 | 第 49 槽增量缓存（自动产物） |
| docs/00-导读/W批次编号对账表.md | W1077 | 批次台账 |

## W1076 v4 视觉体系迁移首站：根页与入口八页消费 v4 令牌（2026-11-02）

| 文件 | W | 说明 |
|---|---|---|

| .agent/skills/puti-shouye/SKILL.md | W1076 | 治理文档 |
| .github/workflows/README.md | W1076 | 治理文档 |
| AGENTS.md | W1076 | 治理文档 |
| CHANGELOG.md | W1076 | 治理文档 |
| CITATION.cff | W1076 | 治理文档 |
| HANDOVER.md | W1076 | 治理文档 |
| README.md | W1076 | 治理文档 |
| STRUCTURE.md | W1076 | 治理文档 |
| archive/docs/AGENTS-ARCHIVE.md | W1076 | 本批工具/产物 |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1076 | 本批工具/产物 |
| archive/scripts/batches/README.md | W1076 | 本批工具/产物 |
| archive/scripts/batches/index.md | W1076 | 本批工具/产物 |
| archive/scripts/batches/w1076/README.md | W1076 | 本批工具/产物 |
| archive/scripts/batches/w1076/_w1076_cjk_value_marks.py | W1076 | 本批工具/产物 |
| archive/scripts/batches/w1076/_w1076_j2_diff_report.py | W1076 | 本批工具/产物 |
| archive/scripts/batches/w1076/_w1076_j2_splice_dashboard.py | W1076 | 本批工具/产物 |
| archive/scripts/batches/w1076/_w1076_make_spec.py | W1076 | 本批工具/产物 |
| archive/scripts/batches/w1076/_w1076_space_tokens.py | W1076 | 本批工具/产物 |
| archive/scripts/batches/w1076/index.md | W1076 | 本批工具/产物 |
| docs/00-导读/W批次编号对账表.md | W1076 | 治理文档 |
| docs/00-导读/项目说明.md | W1076 | 治理文档 |
| docs/11-方案报告/README.md | W1076 | 治理文档 |
| docs/11-方案报告/计划方案/T42-任务计划执行与经验沉淀报告-2026-11-02.md | W1076 | 治理文档 |
| docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md | W1076 | 治理文档 |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1076 | 治理文档 |
| docs/INDEX.md | W1076 | 治理文档 |
| docs/agent/pitfalls.md | W1076 | 治理文档 |
| scripts/_w1076_cjk_value_marks.py | W1076 | 本批工具/产物 |
| scripts/_w1076_make_spec.py | W1076 | 本批工具/产物 |
| scripts/_w1076_space_tokens.py | W1076 | 本批工具/产物 |
| scripts/check_repo_layout.py | W1076 | 本批工具/产物 |
| scripts/output/README.md | W1076 | 本批工具/产物 |
| scripts/output/_cascade_files_W1076.txt | W1076 | 本批工具/产物 |
| scripts/output/_vermilion_solid_cache.json | W1076 | 本批工具/产物 |
| scripts/output/_vermilion_solid_report.json | W1076 | 本批工具/产物 |
| scripts/output/_w1076_j2_after | W1076 | 本批工具/产物 |
| scripts/output/_w1076_j2_after_root3.json | W1076 | 本批工具/产物 |
| scripts/output/_w1076_j2_before | W1076 | 本批工具/产物 |
| scripts/output/_w1076_j2_before_root3.json | W1076 | 本批工具/产物 |
| scripts/output/_w1076_j2_dashboard_only.json | W1076 | 本批工具/产物 |
| scripts/output/_w1076_j2_diff_report.json | W1076 | 本批工具/产物 |
| scripts/output/_w1076_spec.json | W1076 | 本批工具/产物 |
| scripts/output/file-index.md | W1076 | 本批工具/产物 |
| scripts/output/index.md | W1076 | 本批工具/产物 |
| scripts/output/stats-changelog.json | W1076 | 本批工具/产物 |
| scripts/output/stats-index.md | W1076 | 本批工具/产物 |
| scripts/output/stats.json | W1076 | 本批工具/产物 |
| scripts/output/tools-inventory.md | W1076 | 本批工具/产物 |
| scripts/visual_regression_probe.py | W1076 | 本批工具/产物 |
| site/404.html | W1076 | 页面（v4 令牌消费） |
| site/curated.html | W1076 | 页面（v4 令牌消费） |
| site/dashboard.html | W1076 | 页面（v4 令牌消费） |
| site/data/cross-time-danmaku.html | W1076 | 页面（v4 令牌消费） |
| site/data/search.html | W1076 | 页面（v4 令牌消费） |
| site/data/tag-cloud.html | W1076 | 页面（v4 令牌消费） |
| site/dukou-engine.html | W1076 | 页面（v4 令牌消费） |
| site/en/search.html | W1076 | 页面（v4 令牌消费） |
| site/guide.html | W1076 | 页面（v4 令牌消费） |
| site/index.html | W1076 | 页面（v4 令牌消费） |
| site/rum-viewer.html | W1076 | 页面（v4 令牌消费） |
| site/system.css | W1076 | 页面（v4 令牌消费） |

## W1075 合并前红灯修复微批（2026-10-31）

| 文件 | W | 说明 |
|---|---|---|
| docs/00-导读/W批次编号对账表.md | W1075 | 本批修改（W1075 认领行） |
| scripts/cross_line_baseline.json | W1075 | 本批修改（跨行基线确认清单 54→55·人工复核无害） |
| scripts/output/tools-inventory.md | W1075 | 级联生成（stats 快照与索引） |
| site/reader/themes/index.html | W1075 | 本批修改（跳转页可见链接补 ../） |

## W1074 交互修复第二+三批（2026-10-31）

| 文件 | W | 说明 |
|---|---|---|
| scripts/_w1074_batches23.py | W1074 | 级联生成（六文档同步面） |
| scripts/index.md | W1074 | 级联生成（六文档同步面） |
| scripts/output/_vermilion_solid_cache.json | W1074 | 级联生成（stats 快照与索引） |
| scripts/output/tools-inventory.md | W1074 | 级联生成（stats 快照与索引） |
| site/404.html | W1074 | 本批修改（R-08 返回上一页·含单段内联脚本） |
| site/dashboard.html | W1074 | 本批修改（N-02 fetch 移除 + drill 文案） |
| site/data/chapter-structure-graph.html | W1074 | 本批修改（R-03 两个 vis 页入口） |
| site/data/cross-time-danmaku.html | W1074 | 本批修改（R-11 aria-label） |
| site/data/graph-explorer.html | W1074 | 本批修改（R-11 aria-label ×2） |
| site/data/journey-map-interactive.html | W1074 | 本批修改（R-11 aria-label） |
| site/data/narrative-rhythm-curve.html | W1074 | 本批修改（R-11 aria-label） |
| site/data/search.html | W1074 | 本批修改（N-02 /datasets 在线分支移除 + 文案读者化） |
| site/index.html | W1074 | 本批修改（N-08 根修 CSS / N-07 16D / N-09 EN 去重 / R-07 双 role / 级联页脚行） |
| site/reader/ch001.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch002.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch003.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch004.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch005.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch006.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch007.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch008.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch009.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch010.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch011.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch012.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch013.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch014.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch015.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch016.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch017.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch018.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch019.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch020.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch021.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch022.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch023.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch024.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch025.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch026.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch027.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch028.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch029.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch030.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch031.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch032.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch033.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch034.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch035.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch036.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch037.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch038.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch039.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch040.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch041.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch042.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch043.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch044.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch045.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch046.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch047.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch048.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch049.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch050.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch051.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch052.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch053.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch054.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch055.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch056.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch057.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch058.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch059.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch060.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch061.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch062.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch063.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch064.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch065.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch066.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch067.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch068.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch069.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch070.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch071.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch072.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch073.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch074.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch075.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch076.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch077.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch078.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch079.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch080.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch081.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch082.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch083.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch084.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch085.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch086.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch087.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch088.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch089.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch090.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch091.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch092.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch093.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch094.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch095.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch096.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch097.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch098.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch099.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/ch100.html | W1074 | 本批修改（N-04 返回导读站内化 ×100） |
| site/reader/index.html | W1074 | 本批修改（N-05 壳+h1+R-03 hub 行） |
| site/reader/themes/index.html | W1074 | 本批修改（R-04 归一跳转 stub + SEO og 块） |

## W1073 D-1 首屏插画深色变体批（2026-11-01）

| 文件 | W | 说明 |
|---|---|---|
| site/index.html | W1073 | 本批修改（D-1 深色机制：首帧 CSS 指向 -dark 变体 + 轮播 darkSrc + data-theme 监听） |
| site/static/images/hero-line-01-ruyi-staff-dark.webp | W1073 | 本批新增（深色变体插画·2400×1017 webp） |
| site/static/images/hero-line-02-journey-scroll-dark.webp | W1073 | 本批新增（深色变体插画·2400×1017 webp） |
| site/static/images/hero-line-03-classic-scroll-dark.webp | W1073 | 本批新增（深色变体插画·2400×1017 webp） |
| site/static/images/hero-line-04-tight-crown-dark.webp | W1073 | 本批新增（深色变体插画·2400×1017 webp） |
| site/static/images/hero-line-05-lotus-dark.webp | W1073 | 本批新增（深色变体插画·2400×1017 webp） |
| site/static/images/hero-line-06-nine-ring-staff-dark.webp | W1073 | 本批新增（深色变体插画·2400×1017 webp） |
| site/static/images/hero-line-07-banana-fan-dark.webp | W1073 | 本批新增（深色变体插画·2400×1017 webp） |
| site/static/images/hero-line-08-jade-vase-dark.webp | W1073 | 本批新增（深色变体插画·2400×1017 webp） |
| site/static/images/hero-line-09-somersault-cloud-dark.webp | W1073 | 本批新增（深色变体插画·2400×1017 webp） |
| scripts/_w1073_dark_verify.py | W1073 | 本批新增（深色变体机器判据·J1-J9 + K1-K3） |
| scripts/_w1073_paper_normalize.py | W1073 | 本批新增（纸底精确归一·重建 W938 口径） |
| scripts/_w1073_derive.py | W1073 | 本批新增（程序化派生·09 专项） |
| scripts/_w1073_fix_band.py | W1073 | 本批新增（底部亮带清除·09 专项） |
| scripts/_w1073_probe.py | W1073 | 本批新增（D-1 验收探针·真实 Chromium） |
| scripts/_w1073_baseline_shot.py | W1073 | 本批新增（浅色基线补拍） |
| scripts/output/_w1073_spec.json | W1073 | 本批新增（批次 spec） |

## W1072 可复用 Skill 盘点与取经编制表角色优化批（2026-11-01）

| 文件 | W | 说明 |
|---|---|---|
| docs/11-方案报告/计划方案/T41-任务计划执行与经验沉淀报告-2026-11-01.md | W1072 | 本批新增（Skill 盘点与编制表角色优化报告） |
| docs/11-方案报告/README.md | W1072 | 本批修改（§六 计划方案分区登记第 59 行） |
| docs/00-导读/W批次编号对账表.md | W1072 | 本批修改（W1072 认领行） |
| HANDOVER.md | W1072 | 本批修改（当前进度 + 最后更新行） |
| scripts/output/_w1072_spec.json | W1072 | 本批新增（批次 spec） |

## W1071 交互修复第一批（2026-10-31）

| 文件 | W | 说明 |
|---|---|---|
| site/data/search.html | W1071 | 本批修改（SITE_DOC_MAP 612 条内嵌 + renderOffline 行链接化 + Drill 站内化） |
| site/static/js/rag-chat.js | W1071 | 本批修改（生产环境早退·A 案） |
| site/index.html | W1071 | 本批修改（616/87 加 stats 标记 + 双入口 ask-note） |
| site/guide.html | W1071 | 本批修改（data-gsap 属性移入开标签） |
| site/reader/index.html | W1071 | 本批修改（data-gsap 属性移入开标签） |
| site/reader/essays/index.html | W1071 | 本批修改（data-gsap 属性移入开标签） |
| site/reader/themes-hub.html | W1071 | 本批修改（data-gsap 属性移入开标签） |
| archive/scripts/batches/w1071/_w1071_search_docmap.py | W1071 | 本批新增（映射构建一次性脚本·批内归档） |
| CHANGELOG.md | W1071 | 级联生成（本批顶段） |
| HANDOVER.md | W1071 | 级联生成（现役三元组与进度） |
| docs/00-导读/W批次编号对账表.md | W1071 | 本批修改（追加 W1071 认领行） |
| scripts/output | W1071 | 级联生成（stats 快照与 file-index） |

## W1070 站内交互审查第二轮复核 + 界面优化施工方案落库批（2026-10-31）

| 文件 | W | 说明 |
|---|---|---|
| docs/11-方案报告/审查与评审/站点交互流程审查第二轮复核报告-2026-10-31.md | W1070 | 本批新增（生产态第二轮复核·W926 十二条闭环表 + 新增十条 + 判据自纠四条 + 复算命令附录） |
| docs/11-方案报告/设计与架构方案/界面与交互优化施工方案-2026-10-31.md | W1070 | 本批新增（四维度取证 + 现势基线 + 施工序列八批按收益排序 + 3 项待用户决策） |
| docs/11-方案报告/README.md | W1070 | 本批修改（§一登记第 51 行 + §二登记第 33 行 + 两个分区计数更新） |
| docs/00-导读/W批次编号对账表.md | W1070 | 本批修改（追加 W1070 认领行·在途） |
| CHANGELOG.md | W1070 | 级联生成（本批顶段） |
| HANDOVER.md | W1070 | 级联生成（现役三元组与进度） |
| scripts/output | W1070 | 级联生成（搜索索引 / file-index / stats 快照） |

## W1069 效率与防护打包批（2026-10-31）

| 文件 | W | 说明 |
|---|---|---|
| scripts/check_corruption.py | W1069 | 本批新增/修改（R3 BOM 扫描·tracked 文本面·ps1 例外·self-test 6 例） |
| scripts/preflight_check.py | W1069 | 本批新增/修改（env-sync：ruff 实际版本 vs requirements 对拍·上线即抓真漂移 0.16.7≠0.16.9） |
| docs/agent/pitfalls.md | W1069 | 本批新增/修改（+5 条 E-68~E-72·181·流程组 88·数据组对齐 19） |
| docs/11-方案报告/计划方案/执行前计划-W1069-微批轻量通道设计.md | W1069 | 本批新增（微批轻量通道设计 V1.0·三档+准入判据·待批） |
| CLAUDE.md | W1069 | 本批新增/修改（批次节奏行 15·52/60 行） |
| CHANGELOG.md | W1069 | 收官面（顶段 W1069） |
| HANDOVER.md | W1069 | 级联面（计数链 181/最后更新/进度） |
| README.md | W1069 | 级联面（版本行） |
| STRUCTURE.md | W1069 | 级联面（版本行） |
| AGENTS.md | W1069 | 级联面（计数链 181/脚注滚动） |
| CITATION.cff | W1069 | 级联面（版本同步） |
| docs/00-导读/项目说明.md | W1069 | 级联面（当前版本行） |
| docs/00-导读/W批次编号对账表.md | W1069 | 台账（W1069 行新增） |
| docs/INDEX.md | W1069 | 登记面（docs 索引） |
| INDEX.md | W1069 | 登记面（根索引） |
| archive/docs/AGENTS-ARCHIVE.md | W1069 | 级联归档滚动 |
| archive/docs/CHANGELOG-ARCHIVE.md | W1069 | 级联归档滚动（体积窗若触发） |
| archive/docs/file-index-ARCHIVE.md | W1069 | 级联归档滚动（体积窗若触发） |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1069 | 级联归档滚动（体积窗若触发） |
| .github/workflows/README.md | W1069 | 级联面（里程碑行同步） |
| site/index.html | W1069 | 级联面（页脚批次链插入） |
| site/data/cross-time-danmaku.html | W1069 | 级联面（页脚批次链插入） |
| site/data/tag-cloud.html | W1069 | 级联面（页脚批次链插入） |
| site/dukou-engine.html | W1069 | 级联面（页脚批次链插入·含 head_sentence） |
| scripts/output/stats.json | W1069 | 登记面产物（stats 实体） |
| scripts/output/stats-changelog.json | W1069 | 登记面产物（变更史） |
| scripts/output/stats-index.md | W1069 | 登记面产物（统计索引） |
| scripts/output/file-index.md | W1069 | 登记面产物（反向索引） |
| scripts/output/index.md | W1069 | 登记面产物（output 索引） |
| scripts/output/tools-inventory.md | W1069 | 登记面产物（工具清单） |
| scripts/output/README.md | W1069 | 登记面产物（output 说明） |
| scripts/output/chart-values-report.json | W1069 | 登记面产物（第 43 槽报告） |
| scripts/output/_vermilion_solid_cache.json | W1069 | 登记面产物（第 49 槽机器缓存自跟随） |
| scripts/output/_cascade_files_W1069.txt | W1069 | 级联清单（本批产物） |
| scripts/output/_w1069_spec.json | W1069 | 本批 spec |

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
| INDEX.md | W1061 | 登记面（根索引） |
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
| INDEX.md | W1060 | 登记面（根索引） |
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
| INDEX.md | W1059 | 登记面（根索引） |
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
| INDEX.md | W1058 | 登记面（根索引） |
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
| INDEX.md | W1057 | 登记面（根索引） |
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
| INDEX.md | W1056 | 登记面（根索引） |
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
| INDEX.md | W1055 | 登记面（根索引） |
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
| INDEX.md | W1054 | 登记面（根索引） |
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
| INDEX.md | W1053 | 登记面（根索引） |
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
| INDEX.md | W1052 | 登记面（根索引） |
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
| INDEX.md | W1051 | 登记面（根索引） |
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
| INDEX.md | W1050 | 登记面（根索引） |
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


## W1001 回次 og:image 全覆盖批·第一轮试点（12 张线描立像/场面）

| 文件 | W | 说明 |
|---|---|---|
| CHANGELOG.md | W1001 | 本批新增/修改（W1001 段 + 编号规则段上限本体所在段） |
