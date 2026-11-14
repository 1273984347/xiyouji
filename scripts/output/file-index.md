## W1237 嵌套块棘轮批：PLR1702 十九条全清零（2026-11-15）

| 文件 | W | 说明 |
|---|---|---|
| scripts/cascade_lock.py | W1237 | _git_dir 解析拆 _gitdir_from_pointer（先读后判）·级联取锁语义不变 |
| scripts/check_chapter_stats_sync.py | W1237 | flat_check 单键对拍拆 _compare_value·自测过 |
| scripts/check_chart_data.py | W1237 | R1 sankey 引用判定拆 _check_sankey_refs·自测过 |
| scripts/check_chart_colorblind.py | W1237 | analyze 拆 _palette_lab_cache / _pair_violations·自测过 |
| scripts/check_content_consistency.py | W1237 | 逐元素对拍拆 _compare_list_item（每元素只记一条·上限 8 不变）+ 连带消 2 处嵌套推导式（拆 _is_node_array/_is_link_array） |
| scripts/check_embedded_stale_markers.py | W1237 | scan 拆 _iter_scope_files（yield from）/ _mark_lines·自测过 |
| scripts/check_icon_fields.py | W1237 | 单文件扫描拆 _scan_text（字段形态 + 数组形态两段） |
| scripts/check_parser_anchor_coverage.py | W1237 | 位置敏感盲区样本拆 _blind_samples·自测过 |
| scripts/export_design_tokens.py | W1237 | 只读对账逐产物拆 _diff_one（meta.generated 排除口径不变）·--check 0 差异 |
| scripts/lint_links.py | W1237 | 站内/外链判定拆 _emit_internal / _emit_external（打印序契约不变）·连带消 1 处嵌套推导式（拆 _is_excluded）·docs 5626 链接 0 broken |
| scripts/rag/xiyouji_rag.py | W1237 | 三处：_load_dotenv 拆 _apply_env_file·expand_query 拆 _expand_one·_load_docs 拆 _read_md |
| scripts/review_sweep.py | W1237 | 逐行套规则拆 _scan_lines·扫荡 0 命中 |
| CHANGELOG.md | W1237 | 本批段 |
| HANDOVER.md | W1237 | 里程碑块 |
| README.md | W1237 | 版本抬头行推进 |
| STRUCTURE.md | W1237 | 当前批次行推进 |
| docs/00-导读/项目说明.md | W1237 | 版本抬头行推进 |
| .github/workflows/README.md | W1237 | 批次里程碑行推进 |
| archive/docs/workflows-readme-history.md | W1237 | 里程碑历史滚入 |
| AGENTS.md | W1237 | 脚注条目 + 最老条目滚动迁档 |
| archive/docs/AGENTS-ARCHIVE.md | W1237 | 滚动迁入条目 |
| CITATION.cff | W1237 | 版本与日期同步 |
| site/index.html | W1237 | 页脚批次链插入 |
| site/data/cross-time-danmaku.html | W1237 | 页脚批次链插入 |
| site/data/tag-cloud.html | W1237 | 页脚批次链插入 |
| site/dukou-engine.html | W1237 | 页脚批次链插入 |
| site/rss.xml | W1237 | 第 73 槽产物新鲜度：随 CHANGELOG 新段重建条目 |
| scripts/output/file-index.md | W1237 | 本批段追加 |
| scripts/output/README.md | W1237 | 第 45 槽：目录说明随清单刷新 |
| scripts/output/INDEX.md | W1237 | 第 45 槽：目录清单随本批新件刷新 |
| scripts/output/stats.json | W1237 | 级联刷新统计快照 |
| scripts/output/tools-inventory.md | W1237 | 工具清单日期戳与计数刷新 |
| scripts/output/_vermilion_solid_cache.json | W1237 | 朱砂实底按页 hash 缓存随页脚变更更新 |
| scripts/output/_cascade_files_W1237.txt | W1237 | 级联写后自检的改动面清单 |
| scripts/output/_w1237_spec.json | W1237 | 本批规格（file_index_rows 即应动全集） |
| docs/00-导读/W批次编号对账表.md | W1237 | W1237 认领行 + W1236 台账 hash 回填 |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1237 | 台账腾窗：新增认领行使正本越窗 ⇒ 最老行迁入归档 |

## W1236 CI 首跑红清偿批：浏览器探针自测改挂 e2e job + pytest 侧接线守卫，并回填上一批台账（2026-11-15）

| 文件 | W | 说明 |
|---|---|---|
| tests/unit/test_w1230_execution_faces.py | W1236 | 15 件自测清单拆两档：13 件留 pytest，2 件浏览器探针移入 BROWSER_SELF_TEST_SCRIPTS + 新增 test_browser_self_tests_wired_in_ci 接线守卫 |
| .github/workflows/ci.yml | W1236 | e2e-interaction job 增 python 3.12 + 哈希化依赖 + 两件浏览器探针 --self-test 真跑 |
| .github/workflows/README.md | W1236 | Job 9 流程增补浏览器探针自测与接线守卫说明 |
| CHANGELOG.md | W1236 | 本批段 |
| HANDOVER.md | W1236 | 里程碑块 |
| scripts/output/_w1236_spec.json | W1236 | 本批规格（file_index_rows 即应动全集） |
| scripts/output/_cascade_files_W1236.txt | W1236 | 级联写后自检的改动面清单 |
| scripts/output/file-index.md | W1236 | 本批段追加 |
| scripts/output/stats.json | W1236 | 级联刷新统计快照 |
| scripts/output/tools-inventory.md | W1236 | 工具清单日期戳与计数刷新 |
| scripts/output/_vermilion_solid_cache.json | W1236 | 朱砂实底按页 hash 缓存随页脚变更更新 |
| docs/00-导读/W批次编号对账表.md | W1236 | W1236 认领行 + W1235 台账 hash 回填 |
| README.md | W1236 | 版本抬头行推进 |
| STRUCTURE.md | W1236 | 当前批次行推进 |
| docs/00-导读/项目说明.md | W1236 | 版本抬头行推进 |
| archive/docs/workflows-readme-history.md | W1236 | 里程碑历史滚入 |
| AGENTS.md | W1236 | 脚注条目 + 最老条目滚动迁档 |
| archive/docs/AGENTS-ARCHIVE.md | W1236 | 滚动迁入条目 |
| CITATION.cff | W1236 | 版本与日期同步 |
| site/index.html | W1236 | 页脚批次链插入 |
| site/data/cross-time-danmaku.html | W1236 | 页脚批次链插入 |
| site/data/tag-cloud.html | W1236 | 页脚批次链插入 |
| site/dukou-engine.html | W1236 | 页脚批次链插入 |
| site/rss.xml | W1236 | 第 73 槽产物新鲜度：随 CHANGELOG 新段重建条目 |
| pytest.ini | W1236 | stats 标记随 pytest 收集数 1679→1678 重算（两件浏览器探针移出参数化、新增一件接线守卫） |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1236 | stats 标记同步（pytest 收集数五处） |
| scripts/output/stats-changelog.json | W1236 | 级联 stats 刷新（含本批段） |
| scripts/output/stats-index.md | W1236 | 级联 stats 索引刷新 |
| scripts/output/INDEX.md | W1236 | 第 45 槽：目录清单随本批新件刷新 |
| scripts/output/README.md | W1236 | 第 45 槽：目录说明随清单刷新 |
| archive/docs/file-index-ARCHIVE.md | W1236 | 第 74 槽 C8 腾窗：迁 W1171-W1176 六段入归档 |
| archive/docs/CHANGELOG-ARCHIVE.md | W1236 | 两面同下界对齐：迁 W1171-W1176 六段入 CHANGELOG 归档 |

## W1235 推送前自查预红清偿批：品牌守卫判定面收窄 + 提交主张判据收窄 + 台账腾窗 + 三处明文中性化，并回填上一批台账（2026-11-15）

| 文件 | W | 说明 |
|---|---|---|
| scripts/check_no_brand_refs.py | W1235 | 判定面收窄：抽 is_local_dir_candidate（采集层与谓词层分离）·点号前缀与构建缓存不进采集·self-test 59→63 例 |
| scripts/check_doc_sync.py | W1235 | C4 提交主张收窄（首个 W 号＝主张严格判·其余 token 只 NOTE）+ T4b/T4c 回归锁·self-test 37→39 例 |
| CHANGELOG.md | W1235 | 新段 + W1230 段两处明文中性化（遗留项复判订正） |
| HANDOVER.md | W1235 | 里程碑块 + W1230 ⑥ 行明文中性化 |
| scripts/output/_w1230_spec.json | W1235 | 三处明文中性化（milestone_block 一处 + changelog_body 两处） |
| scripts/output/_w1235_spec.json | W1235 | 本批规格（file_index_rows 即应动全集） |
| scripts/output/_cascade_files_W1235.txt | W1235 | 级联写后自检的改动面清单（产物·历史同口径入库） |
| scripts/output/file-index.md | W1235 | 本批段追加 |
| scripts/output/README.md | W1235 | 第 45 槽：目录说明随清单刷新 |
| scripts/output/INDEX.md | W1235 | 第 45 槽：目录清单随两新件刷新 |
| scripts/output/stats.json | W1235 | 级联刷新统计快照 |
| scripts/output/_vermilion_solid_cache.json | W1235 | 朱砂实底按页 hash 缓存随四页脚变更更新（第 49 槽增量口径） |
| scripts/output/tools-inventory.md | W1235 | 工具清单日期戳与计数刷新（级联随批） |
| docs/00-导读/W批次编号对账表.md | W1235 | W1235 认领行 + W1234 台账 hash 回填 + 腾窗迁出 W1174-W1175 |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1235 | 台账腾窗迁入 W1174-W1175 两行 |
| README.md | W1235 | 版本抬头行推进 |
| STRUCTURE.md | W1235 | 当前批次行推进 |
| docs/00-导读/项目说明.md | W1235 | 版本抬头行推进 |
| .github/workflows/README.md | W1235 | 批次里程碑行推进 |
| archive/docs/workflows-readme-history.md | W1235 | 里程碑历史滚入 |
| AGENTS.md | W1235 | 脚注条目 + W1230 条目滚动迁档 |
| archive/docs/AGENTS-ARCHIVE.md | W1235 | W1230 脚注条目迁入 |
| CITATION.cff | W1235 | 版本与日期同步 |
| site/index.html | W1235 | 页脚批次链插入 |
| site/data/cross-time-danmaku.html | W1235 | 页脚批次链插入 |
| site/data/tag-cloud.html | W1235 | 页脚批次链插入 |
| site/dukou-engine.html | W1235 | 页脚批次链插入 |
| site/rss.xml | W1235 | 第 73 槽产物新鲜度：随 CHANGELOG 新段重建 W1235 条目 |
| scripts/output/_sync_analysis_manifest.json | W1235 | 分析包同步清单刷新（38 脚本·本次写入 6） |
| packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/AA_叙事实验/narrative_experiment.py | W1235 | 分析包同步：narrative_experiment 与源面同值（W1231 遗留漂移清偿） |
| packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/AB_视觉艺术/visual_art.py | W1235 | 分析包同步：visual_art 与源面同值（W1231 遗留漂移清偿） |
| packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/M_洞府房产/cave_estate.py | W1235 | 分析包同步：cave_estate 与源面同值（W1231 遗留漂移清偿） |
| packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/V_打工人职场/workplace.py | W1235 | 分析包同步：workplace 与源面同值（W1231 遗留漂移清偿） |
| packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/X_游戏网文/game_webnovel.py | W1235 | 分析包同步：game_webnovel 与源面同值（W1231 遗留漂移清偿） |
| packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/Y_伦理消费/ethics_consumption.py | W1235 | 分析包同步：ethics_consumption 与源面同值（W1231 遗留漂移清偿） |

## W1234 E2E 接线裁决批：visualization_assertions 入 CI + SKIP→FAIL + w266 恒真断言修复 + test_visual 裁决 manual（2026-11-15）

| 文件 | W | 说明 |
|---|---|---|
| tests/e2e/test_w266_e2e_extended.js | W1234 | 恒真断言修复：互链验证 >= 0 → >= 1（审计 #16 本体） |
| tests/e2e/test_site_quality.js | W1234 | 五处前置元素缺失 SKIP console.log → check(false) 计 bad（SKIP→FAIL·fail-closed） |
| tests/e2e/test_visualization_assertions.js | W1234 | 接入 CI（e2e-interaction 第二套件·本地 6 页 0 FAIL 实跑验证） |
| .github/workflows/ci.yml | W1234 | e2e-interaction job 增补 viz assertions 步骤（W1234） |
| .github/workflows/README.md | W1234 | Job 9 流程增补第二套件 + SKIP→FAIL 说明 + test_visual 裁决 manual 保留 |
| docs/00-导读/W批次编号对账表.md | W1234 | W1234 认领行 + W1230-W1233 四批 hash/末笔格回填（回填并入在途批·铁律 21①） |
| HANDOVER.md | W1234 | 里程碑块（cascade 写入） |
| CHANGELOG.md | W1234 | W1234 段（cascade 写入） |
| AGENTS.md | W1234 | 版本脚注滚动（cascade 写入） |
| scripts/output/file-index.md | W1234 | file-index 段（cascade 写入） |
| scripts/output/stats.json | W1234 | stats 刷新 |
| scripts/output/_w1234_spec.json | W1234 | 本批 spec |
| scripts/output/_cascade_files_W1234.txt | W1234 | 级联落盘清单 |
| scripts/output/_vermilion_solid_cache.json | W1234 | 朱砂缓存随页脚链 |
| site/data/cross-time-danmaku.html | W1234 | 页脚批次链滚动 |
| site/data/tag-cloud.html | W1234 | 页脚批次链滚动 |
| site/index.html | W1234 | 页脚批次链滚动 |
| README.md | W1234 | 版本面推进 |
| STRUCTURE.md | W1234 | 版本面推进 |
| CITATION.cff | W1234 | 版本面推进 |
| docs/00-导读/项目说明.md | W1234 | 版本面推进 |
| .github/workflows/README.md | W1234 | 版本面推进 |
| archive/docs/AGENTS-ARCHIVE.md | W1234 | 脚注滚动归档 |
| archive/docs/workflows-readme-history.md | W1234 | workflows README 历史归档 |
| pytest.ini | W1234 | pytest_collected 随动 |
| site/sitemap.xml | W1234 | sitemap 随动 |
| site/data/json/search-index-zh.js | W1234 | 搜索索引随动 |
| site/data/json/search-index-en.js | W1234 | 搜索索引随动 |
| scripts/output/search-index-zh.js | W1234 | 搜索索引随动 |
| scripts/output/search-index-en.js | W1234 | 搜索索引随动 |
| scripts/output/INDEX.md | W1234 | 目录文档刷新 |
| scripts/output/README.md | W1234 | 目录文档刷新 |
| tests/unit/INDEX.md | W1234 | 目录文档刷新 |
| tests/unit/README.md | W1234 | 目录文档刷新 |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1234 | 台账腾窗归档面（如触发） |
| scripts/guardrails/api_diff.py | W1234 | SystemExit 退出语义不计破坏性 raise 集合（W1233 拆解重构的 api_diff 语义放宽·随批入库） |
| scripts/output/tools-inventory.md | W1234 | 工具盘点随动 |
| site/dukou-engine.html | W1234 | 页脚批次链滚动 |
| site/rss.xml | W1234 | W1232 gen_rss 重建随动（W1233 链归档触发重刷） |

## W1233 复杂度棘轮批：C901 全清零（2026-11-15）

| 文件 | W | 说明 |
|---|---|---|
| scripts/gen_folder_docs.py | W1233 | main 29→拆 4 helper（_warn_untracked/_kinds_for/_process_one/_report）·--refresh 端到端实跑验证·45 槽 0 FAIL |
| scripts/tmpe_tidy.py | W1233 | RunLock.acquire 19→三阶段 helper（_degrade_or_raise/_inspect_lock/_takeover_stale/_create_and_write）·23/23 专项过·教训：_NullLock 同名方法首拆误插（find 第一命中）已当轮修正 |
| scripts/check_cross_line_rewrite.py | W1233 | scan 18→_iter_py_files/_classify_call 拆解·连带 9 条 PLR1702 消·自测 _self_test/_repl_kind_of_call 两 helper 补回（切片区间误吞）·9/9 过 |
| scripts/j1_name_audit.py | W1233 | main 18→_verify_landed_checks/_preflight_checks 双臂拆解·12/12 过 |
| scripts/B_人物/character_nlp.py | W1233 | build_cooccurrence 16→_count_and_pair/_scene_presents 拆解 |
| scripts/check_doc_numbers.py | W1233 | check_coverage 16→_resolve_targets/_assert_one 拆解 |
| scripts/bump_version.py | W1233 | main 16→_resolve_versions/_sync_range_and_footers/_sync_aux_version_docs/_append_file_index 拆解（STOP 防线实跑验证） |
| docs/00-导读/W批次编号对账表.md | W1233 | W1233 认领行登记 |
| .github/workflows/README.md | W1233 | 收官链随动件（refresh/stats/级联面） |
| AGENTS.md | W1233 | 收官链随动件（refresh/stats/级联面） |
| CHANGELOG.md | W1233 | 收官链随动件（refresh/stats/级联面） |
| CITATION.cff | W1233 | 收官链随动件（refresh/stats/级联面） |
| HANDOVER.md | W1233 | 收官链随动件（refresh/stats/级联面） |
| README.md | W1233 | 收官链随动件（refresh/stats/级联面） |
| STRUCTURE.md | W1233 | 收官链随动件（refresh/stats/级联面） |
| archive/docs/workflows-readme-history.md | W1233 | 收官链随动件（refresh/stats/级联面） |
| docs/00-导读/项目说明.md | W1233 | 收官链随动件（refresh/stats/级联面） |
| scripts/output/_cascade_files_W1233.txt | W1233 | 收官链随动件（refresh/stats/级联面） |
| scripts/output/_vermilion_solid_cache.json | W1233 | 收官链随动件（refresh/stats/级联面） |
| scripts/output/_w1233_spec.json | W1233 | 收官链随动件（refresh/stats/级联面） |
| scripts/output/file-index.md | W1233 | 收官链随动件（refresh/stats/级联面） |
| scripts/output/stats.json | W1233 | 收官链随动件（refresh/stats/级联面） |
| scripts/output/tools-inventory.md | W1233 | 收官链随动件（refresh/stats/级联面） |
| site/data/cross-time-danmaku.html | W1233 | 收官链随动件（refresh/stats/级联面） |
| site/data/tag-cloud.html | W1233 | 收官链随动件（refresh/stats/级联面） |
| site/dukou-engine.html | W1233 | 收官链随动件（refresh/stats/级联面） |
| site/index.html | W1233 | 收官链随动件（refresh/stats/级联面） |
| site/rss.xml | W1233 | 收官链随动件（refresh/stats/级联面） |
| site/sitemap.xml | W1233 | 收官链随动件（refresh/stats/级联面） |


## W1232 门禁挂槽批：三槽挂载（2026-11-14）

| 文件 | W | 说明 |
|---|---|---|
| scripts/verify_delivery.py | W1232 | 第 72/73/74 槽挂载（_StrictGate ×3 + EXPECTED 两处清单·79 段自洽） |
| scripts/check_emoji_icons.py | W1232 | 第 72 槽基线棘轮（--record 自动登记/超基线判红）+ run_browser/scan_static 拆 5 helper（宽档钉消号·判定逐字未改·623 计数自证） |
| scripts/check_reader_rss_fresh.py | W1232 | 新增：reader/RSS 产物新鲜度判据（git 视角·工作树 mtime 兜重建窗口·浅克隆 fail-closed） |
| scripts/check_doc_size_budget.py | W1232 | --gate 旗标 + 第 74 槽汇总行形态（判据本体零变化） |
| scripts/check_data_copy_chain.py | W1232 | #51：--record 须搭配 --approve（无批准拒绝 rc=1） |
| scripts/check_glossary.py | W1232 | #51：--build-baseline 须搭配 --approve |
| scripts/check_citability.py | W1232 | #51：--generate-baseline 须搭配 --approve |
| scripts/gen_rss.py | W1232 | 版段正则根修（现役 W 形态优先·v 形态回退——v 退役后恒解析空 ⇒ rss 自 10-22 静默陈旧根因） |
| scripts/build_reader.py | W1232 | 收尾自动 nav_inject --apply（重建洗导航正本流水线缺口·第 65 槽 15 页复踩根修） |
| scripts/output/emoji-residue-baseline.txt | W1232 | 新增：emoji 残留棘轮基线（623·W1232 首跑登记） |
| scripts/content-consistency-baseline.txt | W1232 | reader culture 7 篇新页同族抽取伪影登记（与已冻结 79 条同规则同形态） |
| scripts/output/script-coverage-baseline.txt | W1232 | 摘 check_emoji_icons.py 豁免行（W1014 C2 反向查·已挂槽不得仍豁免） |
| docs/agent/gates.md | W1232 | 第 72/73/74 槽全量定义 + 标题 marker 71→74 |
| AGENTS.md | W1232 | §4.2 三槽摘要（合并形态·C2 对账）+ gate_count marker 71→74 三处 + §4.3 三段详述下放指针（体积窗 C9 预算） |
| docs/00-导读/W批次编号对账表.md | W1232 | W1232 认领行 + 腾窗迁出 2 行（W1171-W1172） |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1232 | 台账腾窗归档面（W1171-W1172 迁入） |
| site/reader/ | W1232 | 重建 630 页（docs/02 11-11 变更清偿·首跑新鲜度判据抓到的欠账） |
| site/rss.xml | W1232 | 重建 20 条（W1231→W1211·gen_rss 根修后） |
| site/sitemap.xml | W1232 | gen_sitemap 862 URLs（reader 重建 7 新页收录） |
| site/data/timeline.html | W1232 | vm 灌入撤销回滚（W1231 遗留收尾） |
| site/reader/ 未跟踪新页 ×7 | W1232 | culture 专题新页（docs/04 11-11 新增重建产物） |
| scripts/output/stats.json | W1232 | stats 刷新（gate_count 74 等） |
| scripts/output/stats-changelog.json | W1232 | stats 刷新随动 |
| scripts/output/stats-index.md | W1232 | stats 刷新随动 |
| pytest.ini | W1232 | pytest_collected 计数随动 |
| tests/unit/test_w1232_gates.py | W1232 | 新增：#51 三拒绝 + 棘轮基线 + gen_rss 正则 + 新鲜度语义 + 挂槽登记 7 例回归锁 |
| scripts/output/search-index-zh.js | W1232 | 搜索索引刷新（reader 重建随动·第 46 槽） |
| scripts/output/search-index-en.js | W1232 | 搜索索引刷新随动 |
| site/data/json/ | W1232 | search-index 内嵌副本随动（第 46 槽双源） |
| CHANGELOG.md | W1232 | W1232 段落落盘（cascade 写入） |
| HANDOVER.md | W1232 | 里程碑块插入 + 版本行推进 |
| archive/docs/AGENTS-ARCHIVE.md | W1232 | AGENTS 脚注滚动归档 |
| archive/docs/workflows-readme-history.md | W1232 | workflows README 历史归档 |
| docs/00-导读/项目说明.md | W1232 | 版本面推进 |
| README.md | W1232 | 版本面推进 |
| STRUCTURE.md | W1232 | 版本面推进 |
| CITATION.cff | W1232 | 版本面推进 |
| .github/workflows/README.md | W1232 | 版本面推进 |
| docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md | W1232 | stats 计数随动 |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1232 | stats 计数随动 |
| scripts/output/file-index.md | W1232 | file-index 段（cascade 写入） |
| scripts/output/_cascade_files_W1232.txt | W1232 | 级联落盘清单 |
| scripts/output/_w1232_spec.json | W1232 | 本批 spec |
| scripts/output/INDEX.md | W1232 | 目录文档刷新 |
| scripts/output/README.md | W1232 | 目录文档刷新 |
| scripts/output/tools-inventory.md | W1232 | 工具盘点随动 |
| scripts/output/_vermilion_solid_cache.json | W1232 | 朱砂缓存随页脚链 |
| scripts/output/_vermilion_solid_report.json | W1232 | 朱砂报告随动 |
| site/data/cross-time-danmaku.html | W1232 | 页脚批次链滚动 |
| site/data/tag-cloud.html | W1232 | 页脚批次链滚动 |
| site/dukou-engine.html | W1232 | 页脚批次链滚动 |
| site/index.html | W1232 | 页脚批次链滚动 |
| site/data/json/search-index-zh.js | W1232 | 搜索索引内嵌副本（46 槽双源） |
| site/data/json/search-index-en.js | W1232 | 搜索索引内嵌副本随动 |
| tests/unit/INDEX.md | W1232 | 目录文档刷新（新测试文件） |
| tests/unit/README.md | W1232 | 目录文档刷新随动 |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-架构图 | W1232 | 架构图目录（stats 面随动·如触发） |
| scripts/INDEX.md | W1232 | 目录文档刷新 |
| scripts/batch_cascade.py | W1232 | precheck 全角括号判据（W1231/W1232 实证转判据·_paren_issues helper） |
| scripts/output/_w1167_nav_plan.json | W1232 | nav_inject --apply 全站分发计划随动 |
| site/data/search-index-zh.js | W1232 | 搜索索引刷新（46 槽双源） |
| site/en/search-index-en.js | W1232 | 搜索索引刷新（46 槽双源） |
| site/reader/culture/INDEX.md | W1232 | reader culture 新页（docs/04 11-11 新增重建产物） |
| site/reader/culture/README.md | W1232 | reader culture 新页（docs/04 11-11 新增重建产物） |
| site/reader/culture/index.html | W1232 | reader culture 新页（docs/04 11-11 新增重建产物） |
| site/reader/culture/三教合一明代思想史深化专题.html | W1232 | reader culture 新页（docs/04 11-11 新增重建产物） |
| site/reader/culture/且听下回分解套语专题.html | W1232 | reader culture 新页（docs/04 11-11 新增重建产物） |
| site/reader/culture/佛道思想.html | W1232 | reader culture 新页 |
| site/reader/culture/八十一难与正果专题.html | W1232 | reader culture 新页 |
| site/reader/culture/历史玄奘与小说玄奘专题.html | W1232 | reader culture 新页 |
| site/reader/culture/四大部洲与三界空间框架专题.html | W1232 | reader culture 新页 |
| site/reader/culture/天罡地煞与变化之术专题.html | W1232 | reader culture 新页 |
| site/reader/culture/成书背景.html | W1232 | reader culture 新页 |
| site/reader/culture/明代驿递交通制度对照专题.html | W1232 | reader culture 新页 |
| site/reader/culture/法器与兵器器物体系专题.html | W1232 | reader culture 新页 |
| site/reader/culture/版本演变.html | W1232 | reader culture 新页 |
| site/reader/culture/西游与道教全真派专题.html | W1232 | reader culture 新页 |
| site/reader/culture/西游东传与译介专题.html | W1232 | reader culture 新页 |
| site/reader/culture/西游记大事年表.html | W1232 | reader culture 新页 |
| site/reader/culture/金公木母与心猿意马称谓专题.html | W1232 | reader culture 新页 |
| site/reader/index.html | W1232 | reader 重建随动 |
| site/reader/people/唐僧.html | W1232 | reader 重建随动 |
| site/reader/people/太上老君.html | W1232 | reader 重建随动 |
| site/reader/people/孙悟空.html | W1232 | reader 重建随动 |
| site/reader/people/沙僧.html | W1232 | reader 重建随动 |
| site/reader/people/猪八戒.html | W1232 | reader 重建随动 |
| site/reader/people/白龙马.html | W1232 | reader 重建随动 |
| site/reader/people/菩提祖师-方向二深化.html | W1232 | reader 重建随动 |
| site/reader/people/菩提祖师.html | W1232 | reader 重建随动 |
| site/reader/people/观音.html | W1232 | reader 重建随动 |
| site/reader/people/金角银角-方向二深化.html | W1232 | reader 重建随动 |
| site/reader/people/铁扇公主.html | W1232 | reader 重建随动 |
| site/reader/people/高翠兰-方向二深化.html | W1232 | reader 重建随动 |
| site/reader/people/黑熊精-方向二深化.html | W1232 | reader 重建随动 |
| scripts/stats.py | W1232 | 收官链随动件（refresh/stats/versions/sweep 刷新） |

## W1231 单侧键 schema 分歧清理批：数据漂移门禁 v4 面板配对 + embed_json 三重根修 + 476 条隐性值漂移修复 + dataset 对齐生成面（2026-11-14）

| 文件 | W | 说明 |
|---|---|---|
| scripts/check_data_drift.js | W1231 | v4：根级配对前置（pairForCompare 包壳/数组形态降级）+ 设计性单侧键族豁免 + 单行形态回退（保护面守恒 60 页）+ --self-test 8 例 |
| scripts/embed_json.py | W1231 | 三重根修：模式扩 EMBEDDED_DATA（46 页不可用→可用）+ 行锚定成员定位（括号扫描在文案含引号/括号页面失步）+ replace off-by-one 双闭合括号（快照永不重灌的结构性根因） |
| scripts/source_collate.py | W1231 | dataset/81-hardships.json 键改名联动（index→n 6 处消费点） |
| dataset/81-hardships.json | W1231 | 键改名 index→n ×81（向站侧对齐·W566 先例） |
| dataset/magic-system.json | W1231 | 键改名 kills→combat_record ×5（向站侧对齐） |
| dataset/cave-estate.json | W1231 | 对齐生成面（caves/by_owner_rank/by_region/top_luxury）+ subordinates_status 按 chapter 回合（2 条改名洞） |
| dataset/timeline.json | W1231 | 对齐撤销回滚 HEAD（页面语义快照 22 项·生成面 36 项为撞名另一语义·登记后续批次澄清命名） |
| dataset/music-structure.json | W1231 | 对齐生成面（summary/sounds/rhythm/symmetry/movement 五键合成） |
| dataset/text-evolution.json | W1231 | versions/variants/authors 对齐生成面 + field_status 按 version 名回合（6 条）·summary/commentators 保留 |
| dataset/README.md | W1231 | gen_dataset_index 刷新（大小/条目数随对齐更新） |
| tests/unit/test_w1231_data_drift.py | W1231 | 新增：门禁 v4 自测接入 + embed_json 行锚定/数组面板/roundtrip/双包裹 4 例回归锁 |
| scripts/output/tools-inventory.md | W1231 | 工具盘点时间戳随动 |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1231 | stats 计数随动（pytest_collected） |
| CHANGELOG.md | W1231 | W1231 段落落盘（cascade 写入） |
| HANDOVER.md | W1231 | 里程碑块插入（cascade 写入）+ 版本行推进（version_surface） |
| AGENTS.md | W1231 | 版本脚注滚动（cascade 写入） |
| archive/docs/AGENTS-ARCHIVE.md | W1231 | AGENTS 脚注滚动归档（cascade 写入） |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1231 | 台账行窗口腾窗迁出最老行（如触发） |
| archive/docs/workflows-readme-history.md | W1231 | workflows README 历史归档（version_surface） |
| docs/00-导读/W批次编号对账表.md | W1231 | W1231 认领行登记 |
| docs/00-导读/项目说明.md | W1231 | 版本面推进（version_surface） |
| README.md | W1231 | 版本面推进（version_surface） |
| STRUCTURE.md | W1231 | 版本面推进（version_surface） |
| CITATION.cff | W1231 | 版本面推进（version_surface） |
| .github/workflows/README.md | W1231 | 版本面推进（version_surface） |
| pytest.ini | W1231 | pytest_collected 计数随动 |
| scripts/output/file-index.md | W1231 | 本批 file-index 段（cascade 写入） |
| scripts/output/stats.json | W1231 | stats 重跑 |
| scripts/output/stats-changelog.json | W1231 | stats 重跑（CHANGELOG 面计数） |
| scripts/output/stats-index.md | W1231 | stats 重跑（索引面计数） |
| scripts/output/_cascade_files_W1231.txt | W1231 | 级联落盘清单（cascade 生成） |
| scripts/output/_vermilion_solid_cache.json | W1231 | 朱砂实底门禁增量缓存随页脚批次链更新（第 49 槽） |
| scripts/output/_vermilion_solid_report.json | W1231 | 朱砂实底门禁报告随动（第 49 槽） |
| site/dukou-engine.html | W1231 | 页脚批次链滚动（cascade 全档） |
| site/index.html | W1231 | 页脚批次链滚动（cascade 全档） |
| site/sitemap.xml | W1231 | gen_sitemap lastmod 随动（如触发） |
| scripts/output/INDEX.md | W1231 | 目录文档刷新（gen_folder_docs） |
| scripts/output/README.md | W1231 | 目录文档刷新（gen_folder_docs） |
| tests/unit/INDEX.md | W1231 | 目录文档刷新（gen_folder_docs·新测试文件触发） |
| tests/unit/README.md | W1231 | 目录文档刷新（gen_folder_docs·新测试文件触发） |
| scripts/output/_w1231_spec.json | W1231 | 本批 spec |
| scripts/AB_视觉艺术/visual_art.py | W1231 | W678 弱水勘正源头根修（水深仅 1m→弱水三千鹅毛不浮·修下游未修根清偿） |
| scripts/X_游戏网文/game_webnovel.py | W1231 | W678 源头根修（/demo 前缀删除 + 六耳 premise 悟空打杀·如来识破真身 + 钉耙性别条款删除） |
| scripts/Y_伦理消费/ethics_consumption.py | W1231 | W678/W693 ticker 全角冒号源头根修（STD：→STD: ×5） |
| scripts/AA_叙事实验/narrative_experiment.py | W1231 | W678 源头根修（芭蕉扇专克火系 + 钉耙性别条款删除） |
| scripts/V_打工人职场/workplace.py | W1231 | W678 成佛二人勘正源头根修（5 人晋升佛位→2 人） |
| scripts/M_洞府房产/cave_estate.py | W1231 | W678 妖将级勘正源头根修（rank_labels general 中将级→妖将级） |
| site/data/*.html（EMBEDDED 重灌页） | W1231 | 21 件同族随动（逐件明细见各批 CHANGELOG 段·分组立式 W1142） |
| site/data/json/*.json（部署副本同步） | W1231 | 47 件同族随动（逐件明细见各批 CHANGELOG 段·分组立式 W1142） |

## W1230 脚本接线/归档裁决批：第 42 槽 47 行 W1155 存量清偿 + packaging 同步接线 + 品牌守卫盲区根修（2026-11-14）

| 文件 | W | 说明 |
|---|---|---|
| scripts/output/script-coverage-baseline.txt | W1230 | 47 行 W1155 存量摘行 + check_untracked 旧行摘除 + 5 行合规重登记（逐条真实类别注记） |
| archive/scripts/site_audit.py | W1230 | 自 scripts/ 归档（被第 49 槽取代·审计 P3） |
| archive/scripts/refresh_icon_paths.py | W1230 | 自 scripts/ 归档（一次性同步器·审计 P3） |
| archive/scripts/accent_audit.py | W1230 | 自 scripts/ 归档（docstring 自述一次性） |
| archive/scripts/file_protocol_probe.py | W1230 | 自 scripts/ 归档（自述一次性诊断件·不入 CI） |
| archive/scripts/check_untracked.py | W1230 | 自 scripts/ 归档（休眠钩子已删 W1154 T13·恒 0） |
| archive/scripts/INDEX.md | W1230 | gen_folder_docs --refresh（5 件归档入列） |
| archive/scripts/README.md | W1230 | gen_folder_docs --refresh 随批再生成 |
| scripts/INDEX.md | W1230 | gen_folder_docs --refresh（5 件出列） |
| scripts/output/tools-inventory.md | W1230 | regen（工具清单随批刷新） |
| scripts/plates_verify.py | W1230 | docstring 旧名 _w945_plates_verify.py 订正（W1154 T4 声明≠落地遗留） |
| scripts/ci_sim.py | W1230 | GATES 增分析包同步 --check（14→15 项） |
| scripts/check_no_brand_refs.py | W1230 | ignored 顶层目录名告警（untracked_top_dir_names/warn_dir_names·self-test 56→59） |
| scripts/guardrails/check_changed.ps1 | W1230 | 改动集过滤 archive/* + ruff 两处 --force-exclude（配置排除生效对齐·修判据） |
| scripts/check_script_coverage.py | W1230 | CATEGORY_OF 摘 5 归档条目（防 --save-baseline 复活） |
| pyproject.toml | W1230 | per-file-ignores E402：两个 W1230 测试文件（裸导入判据形态） |
| tests/unit/test_script_hygiene.py | W1230 | PROMOTED_W1003 摘 4 归档名（防已删件假绿） |
| tests/unit/test_ci_sim.py | W1230 | 关键门禁断言 + 分析包同步项 |
| tests/unit/test_w1230_execution_faces.py | W1230 | 新增：15 件 --self-test 真跑 + 20 件字面导入执行面 |
| tests/unit/test_w1230_wire_archive.py | W1230 | 新增：check_crop/plates_verify/subject_band 实质图像判据（正反样本可证伪） |
| scripts/B_人物/character_network.py | W1230 | 嵌套推导式根修（显式循环·guardrails 当场拦截的存量消号） |
| scripts/C_情节/hardships_81.py | W1230 | 嵌套推导式根修（显式循环） |
| scripts/M_洞府房产/cave_estate.py | W1230 | 嵌套推导式根修（max 提升变量化） |
| packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/B_人物/character_network.py | W1230 | packaging 同步（随 scripts 根修） |
| packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/C_情节/hardships_81.py | W1230 | packaging 同步（随 scripts 根修） |
| packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/M_洞府房产/cave_estate.py | W1230 | packaging 同步（随 scripts 根修） |
| packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/AA_叙事实验/narrative_experiment.py | W1230 | packaging 同步（5 件漂移补齐） |
| packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/A_文本基础/章节切分.py | W1230 | packaging 同步新增目录（A_文本基础） |
| packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/A_文本基础/INDEX.md | W1230 | gen_folder_docs 生成（新目录文档） |
| packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/A_文本基础/README.md | W1230 | gen_folder_docs 生成（新目录文档） |
| scripts/output/_sync_analysis_manifest.json | W1230 | 同步清单（38/38 归零） |
| docs/00-导读/W批次编号对账表.md | W1230 | W1230 认领行登记 |
| scripts/output/_w1230_spec.json | W1230 | 本批 spec |
| CHANGELOG.md | W1230 | W1230 段落落盘（cascade 写入） |
| HANDOVER.md | W1230 | 里程碑块插入（cascade 写入） |
| AGENTS.md | W1230 | 版本脚注滚动（cascade 写入） |
| archive/docs/AGENTS-ARCHIVE.md | W1230 | AGENTS 脚注滚动归档（cascade 写入） |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1230 | 台账行窗口腾窗迁出最老行（如触发） |
| scripts/output/file-index.md | W1230 | 本批 file-index 段（cascade 写入） |
| scripts/output/stats.json | W1230 | stats 重跑 |
| scripts/output/stats-changelog.json | W1230 | stats 重跑（CHANGELOG 面计数） |
| scripts/output/stats-index.md | W1230 | stats 重跑（索引面计数） |
| scripts/output/_cascade_files_W1230.txt | W1230 | 级联落盘清单（cascade 生成） |
| README.md | W1230 | 版本面推进（version_surface） |
| STRUCTURE.md | W1230 | 版本面推进（version_surface） |
| CITATION.cff | W1230 | 版本面推进（version_surface） |
| docs/00-导读/项目说明.md | W1230 | 版本面推进（version_surface） |
| .github/workflows/README.md | W1230 | 版本面推进（version_surface） |
| archive/docs/workflows-readme-history.md | W1230 | workflows README 历史归档（version_surface） |
| pytest.ini | W1230 | pytest_collected 计数随动（1643→1666） |
| docs/11-方案报告/设计与架构方案/系统架构v2方案-目标态与落地路线-2026-10-25.md | W1230 | stats 计数随动（pytest_collected） |
| site/sitemap.xml | W1230 | gen_sitemap lastmod 随动 |
| site/data/cross-time-danmaku.html | W1230 | 页脚批次链滚动（cascade 全档） |
| site/data/tag-cloud.html | W1230 | 页脚批次链滚动（cascade 全档） |
| site/dukou-engine.html | W1230 | 页脚批次链滚动（cascade 全档） |
| site/index.html | W1230 | 页脚批次链滚动（cascade 全档） |
| scripts/output/INDEX.md | W1230 | 目录文档刷新（gen_folder_docs） |
| scripts/output/README.md | W1230 | 目录文档刷新（gen_folder_docs） |
| scripts/output/_vermilion_solid_cache.json | W1230 | 朱砂实底门禁增量缓存随页脚批次链更新（第 49 槽） |
| packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/INDEX.md | W1230 | 目录文档刷新（gen_folder_docs·新目录触发父级） |
| packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/README.md | W1230 | 目录文档刷新（gen_folder_docs·新目录触发父级） |
| tests/unit/INDEX.md | W1230 | 目录文档刷新（gen_folder_docs·新测试文件触发） |
| tests/unit/README.md | W1230 | 目录文档刷新（gen_folder_docs·新测试文件触发） |
| scripts/accent_audit.py | W1230 | git mv 迁出源侧（归档至 archive/scripts/） |
| scripts/check_untracked.py | W1230 | git mv 迁出源侧（归档至 archive/scripts/） |
| scripts/file_protocol_probe.py | W1230 | git mv 迁出源侧（归档至 archive/scripts/） |
| scripts/refresh_icon_paths.py | W1230 | git mv 迁出源侧（归档至 archive/scripts/） |
| scripts/site_audit.py | W1230 | git mv 迁出源侧（归档至 archive/scripts/） |

## W1229 登记面欠账清偿批：README 计数订正 + 台账 hash 机填与末笔格批处理（2026-11-14）

| 文件 | W | 说明 |
|---|---|---|
| docs/11-方案报告/README.md | W1229 | §二 21→16 + §六 110→119 计数订正（磁盘实算口径） |
| docs/00-导读/W批次编号对账表.md | W1229 | 8 行首笔 hash 机填 + 27 行末笔格订正 + W1228 token 回补 + W1229 认领行 |
| CHANGELOG.md | W1229 | 登记面欠账清偿批 |
| HANDOVER.md | W1229 | 里程碑块（cascade 写入） |
| AGENTS.md | W1229 | 版本脚注滚动（cascade 写入） |
| archive/docs/AGENTS-ARCHIVE.md | W1229 | AGENTS 脚注滚动归档（cascade 写入） |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1229 | 台账行窗口腾窗迁出最老行（如触发） |
| scripts/output/file-index.md | W1229 | 本批 file-index 段（cascade 写入） |
| scripts/output/stats.json | W1229 | stats 重跑 |
| scripts/output/_cascade_files_W1229.txt | W1229 | 级联落盘清单（cascade 生成） |
| scripts/output/_w1229_spec.json | W1229 | 本批 spec |
| README.md | W1229 | 版本面推进（version_surface） |
| STRUCTURE.md | W1229 | 版本面推进（version_surface） |
| CITATION.cff | W1229 | 版本面推进（version_surface） |
| docs/00-导读/项目说明.md | W1229 | 版本面推进（version_surface） |
| .github/workflows/README.md | W1229 | 版本面推进（version_surface） |
| archive/docs/workflows-readme-history.md | W1229 | workflows README 历史归档（version_surface） |
| scripts/output/INDEX.md | W1229 | 目录文档刷新（gen_folder_docs） |
| scripts/output/README.md | W1229 | 目录文档刷新（gen_folder_docs） |
| scripts/output/tools-inventory.md | W1229 | 工具盘点时间戳随动 |
| scripts/output/_vermilion_solid_cache.json | W1229 | 朱砂实底门禁增量缓存随页脚批次链更新（第 49 槽） |
| site/data/cross-time-danmaku.html | W1229 | 页脚批次链滚动（cascade 全档） |
| site/data/tag-cloud.html | W1229 | 页脚批次链滚动（cascade 全档） |
| site/dukou-engine.html | W1229 | 页脚批次链滚动（cascade 全档） |
| site/index.html | W1229 | 页脚批次链滚动（cascade 全档） |

## W1228 对抗审查回批 + P-43-01 根修批（2026-11-14）

| 文件 | W | 说明 |
|---|---|---|
| scripts/preflight_check.py | W1228 | P-43-01 描述段 W 形态 + 括号洞锚定修 + bullet 碑化降 NOTE |
| tests/unit/test_preflight_check.py | W1228 | 新增 5 回归锁（描述段形态/无 scope/散文负样本/双形态去重/merge 负样本） |
| scripts/archive_segments.py | W1228 | 归档名大小写错名修（对齐 tracked 实名·P2-1） |
| xiyouji-agent-web/server/compliance/audit-archive.ts | W1228 | purge 销毁留证事务化（P2-4） |
| docs/agent/adversarial-audit-prompt.md | W1228 | 模板校准 W1228 + 新增三个检查点 |
| docs/agent/periodic-ops-checklist.md | W1228 | 到期日补齐（P2-5） |
| docs/00-导读/W批次编号对账表.md | W1228 | W1228 认领行（token）+ W1200/W1213 补登 |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1228 | 台账行窗口腾窗迁出最老行（如触发） |
| CHANGELOG.md | W1228 | 对抗审查回批 + P-43-01 根修批 |
| HANDOVER.md | W1228 | 里程碑块（cascade 写入）+ bullet 对齐 |
| AGENTS.md | W1228 | 版本脚注滚动（cascade 写入） |
| archive/docs/AGENTS-ARCHIVE.md | W1228 | AGENTS 脚注滚动归档（cascade 写入） |
| scripts/output/file-index.md | W1228 | 本批 file-index 段（cascade 写入） |
| scripts/output/stats.json | W1228 | stats 重跑（pytest_collected 随动） |
| scripts/output/_cascade_files_W1228.txt | W1228 | 级联落盘清单（cascade 生成） |
| scripts/output/_w1228_spec.json | W1228 | 本批 spec |
| README.md | W1228 | 版本面推进（version_surface） |
| STRUCTURE.md | W1228 | 版本面推进（version_surface） |
| CITATION.cff | W1228 | 版本面推进（version_surface） |
| docs/00-导读/项目说明.md | W1228 | 版本面推进（version_surface） |
| .github/workflows/README.md | W1228 | 版本面推进（version_surface） |
| archive/docs/workflows-readme-history.md | W1228 | workflows README 历史归档（version_surface） |
| scripts/output/INDEX.md | W1228 | 目录文档刷新（gen_folder_docs） |
| scripts/output/README.md | W1228 | 目录文档刷新（gen_folder_docs） |
| scripts/output/tools-inventory.md | W1228 | 工具盘点时间戳随动 |
| scripts/output/_vermilion_solid_cache.json | W1228 | 朱砂实底门禁增量缓存随页脚批次链更新（第 49 槽） |
| site/data/cross-time-danmaku.html | W1228 | 页脚批次链滚动（cascade 全档） |
| site/data/tag-cloud.html | W1228 | 页脚批次链滚动（cascade 全档） |
| site/dukou-engine.html | W1228 | 页脚批次链滚动（cascade 全档） |
| site/index.html | W1228 | 页脚批次链滚动（cascade 全档） |

## W1227 Draft Release 处置批＝用户令「删」执行（2026-11-14）

| 文件 | W | 说明 |
|---|---|---|
| docs/11-方案报告/设计与架构方案/系统架构v2迁移施工手册-2026-11-13.md | W1227 | T-1 执行结果行补记（Draft 已删·弧线闭环） |
| CHANGELOG.md | W1227 | Draft Release 处置批 |
| HANDOVER.md | W1227 | 里程碑块（cascade 写入） |
| AGENTS.md | W1227 | 版本脚注滚动（cascade 写入） |
| archive/docs/AGENTS-ARCHIVE.md | W1227 | AGENTS 脚注滚动归档（cascade 写入） |
| docs/00-导读/W批次编号对账表.md | W1227 | W1227 认领行 |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1227 | 台账行窗口腾窗迁出最老行（如触发） |
| scripts/output/file-index.md | W1227 | 本批 file-index 段（cascade 写入） |
| scripts/output/stats.json | W1227 | stats 重跑 |
| scripts/output/_cascade_files_W1227.txt | W1227 | 级联落盘清单（cascade 生成） |
| scripts/output/_w1227_spec.json | W1227 | 本批 spec |
| README.md | W1227 | 版本面推进（version_surface） |
| STRUCTURE.md | W1227 | 版本面推进（version_surface） |
| CITATION.cff | W1227 | 版本面推进（version_surface） |
| docs/00-导读/项目说明.md | W1227 | 版本面推进（version_surface） |
| .github/workflows/README.md | W1227 | 版本面推进（version_surface） |
| archive/docs/workflows-readme-history.md | W1227 | workflows README 历史归档（version_surface） |
| scripts/output/INDEX.md | W1227 | 目录文档刷新（gen_folder_docs） |
| scripts/output/README.md | W1227 | 目录文档刷新（gen_folder_docs） |
| scripts/output/tools-inventory.md | W1227 | 工具盘点时间戳随动 |
| scripts/output/_vermilion_solid_cache.json | W1227 | 朱砂实底门禁增量缓存随页脚批次链更新（第 49 槽） |
| site/data/cross-time-danmaku.html | W1227 | 页脚批次链滚动（cascade 全档） |
| site/data/tag-cloud.html | W1227 | 页脚批次链滚动（cascade 全档） |
| site/dukou-engine.html | W1227 | 页脚批次链滚动（cascade 全档） |
| site/index.html | W1227 | 页脚批次链滚动（cascade 全档） |

## W1226 远端 tag v2.3.0 清理批＝T-1 落地（2026-11-14）

| 文件 | W | 说明 |
|---|---|---|
| scripts/output/_w1226_t1_tag_cleanup.json | W1226 | T-1 证据（预检三事实 + 动作 + 双验收 + 回滚路径） |
| docs/11-方案报告/设计与架构方案/系统架构v2迁移施工手册-2026-11-13.md | W1226 | T-1 三处终写（§1.3/§4.1/§6.1 已落地 + 遗留 Draft 登记） |
| .github/workflows/README.md | W1226 | 发布步骤示例命令去实名改 vX.Y.Z 占位（version_surface） |
| CHANGELOG.md | W1226 | T-1 清理批 |
| HANDOVER.md | W1226 | 里程碑块（cascade 写入） |
| AGENTS.md | W1226 | 版本脚注滚动（cascade 写入） |
| archive/docs/AGENTS-ARCHIVE.md | W1226 | AGENTS 脚注滚动归档（cascade 写入） |
| docs/00-导读/W批次编号对账表.md | W1226 | W1226 认领行 |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1226 | 台账行窗口腾窗迁出最老行（如触发） |
| scripts/output/file-index.md | W1226 | 本批 file-index 段（cascade 写入） |
| scripts/output/stats.json | W1226 | stats 重跑 |
| scripts/output/_cascade_files_W1226.txt | W1226 | 级联落盘清单（cascade 生成） |
| scripts/output/_w1226_spec.json | W1226 | 本批 spec |
| README.md | W1226 | 版本面推进（version_surface） |
| STRUCTURE.md | W1226 | 版本面推进（version_surface） |
| CITATION.cff | W1226 | 版本面推进（version_surface） |
| docs/00-导读/项目说明.md | W1226 | 版本面推进（version_surface） |
| archive/docs/workflows-readme-history.md | W1226 | workflows README 历史归档（version_surface） |
| scripts/output/INDEX.md | W1226 | 目录文档刷新（gen_folder_docs） |
| scripts/output/README.md | W1226 | 目录文档刷新（gen_folder_docs） |
| scripts/output/tools-inventory.md | W1226 | 工具盘点时间戳随动 |
| scripts/output/_vermilion_solid_cache.json | W1226 | 朱砂实底门禁增量缓存随页脚批次链更新（第 49 槽） |
| site/data/cross-time-danmaku.html | W1226 | 页脚批次链滚动（cascade 全档） |
| site/data/tag-cloud.html | W1226 | 页脚批次链滚动（cascade 全档） |
| site/dukou-engine.html | W1226 | 页脚批次链滚动（cascade 全档） |
| site/index.html | W1226 | 页脚批次链滚动（cascade 全档） |

## W1225 截图红警清偿批：scope 判据索引数据件归 skip + 批处理器仅认 HTML（2026-11-14）

| 文件 | W | 说明 |
|---|---|---|
| scripts/check_screenshot_scope.py | W1225 | SEARCH_INDEX_DATA_FILES ⇒ skip 根修 + 自测增 3 例 |
| scripts/batch_screenshots.js | W1225 | parseExtraPages 仅认 .html 兜底（非 HTML 告警跳过） |
| CHANGELOG.md | W1225 | 截图红警清偿批 |
| HANDOVER.md | W1225 | 里程碑块（cascade 写入） |
| AGENTS.md | W1225 | 版本脚注滚动（cascade 写入） |
| archive/docs/AGENTS-ARCHIVE.md | W1225 | AGENTS 脚注滚动归档（cascade 写入） |
| docs/00-导读/W批次编号对账表.md | W1225 | W1225 认领行 |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1225 | 台账行窗口腾窗迁出最老行（如触发） |
| scripts/output/file-index.md | W1225 | 本批 file-index 段（cascade 写入） |
| scripts/output/stats.json | W1225 | stats 重跑 |
| scripts/output/_cascade_files_W1225.txt | W1225 | 级联落盘清单（cascade 生成） |
| scripts/output/_w1225_spec.json | W1225 | 本批 spec |
| README.md | W1225 | 版本面推进（version_surface） |
| STRUCTURE.md | W1225 | 版本面推进（version_surface） |
| CITATION.cff | W1225 | 版本面推进（version_surface） |
| docs/00-导读/项目说明.md | W1225 | 版本面推进（version_surface） |
| .github/workflows/README.md | W1225 | 版本面推进（version_surface） |
| archive/docs/workflows-readme-history.md | W1225 | workflows README 历史归档（version_surface） |
| scripts/output/INDEX.md | W1225 | 目录文档刷新（gen_folder_docs） |
| scripts/output/README.md | W1225 | 目录文档刷新（gen_folder_docs） |
| scripts/output/tools-inventory.md | W1225 | 工具盘点时间戳随动 |
| scripts/output/_vermilion_solid_cache.json | W1225 | 朱砂实底门禁增量缓存随页脚批次链更新（第 49 槽） |
| site/data/cross-time-danmaku.html | W1225 | 页脚批次链滚动（cascade 全档） |
| site/data/tag-cloud.html | W1225 | 页脚批次链滚动（cascade 全档） |
| site/dukou-engine.html | W1225 | 页脚批次链滚动（cascade 全档） |
| site/index.html | W1225 | 页脚批次链滚动（cascade 全档） |

## W1224 容量阈值裁决批：#1 双线制 + #2 双口径 + 测量器越线清单（2026-11-14）

| 文件 | W | 说明 |
|---|---|---|
| scripts/check_capacity_budget.py | W1224 | #1 双线制 + #2 页特有/共享块双口径 + 越线页清单与计数（§8.3 修订实现） |
| scripts/output/_w1205_capacity_audit.json | W1224 | 容量证据刷新（修订后首跑读数·新 extra 形态） |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1224 | §8.3 两行修订 + 修订落地记录（含 stats sweep 随动） |
| docs/11-方案报告/设计与架构方案/系统架构v2迁移施工手册-2026-11-13.md | W1224 | T-2 状态行终写（E+R 全落地·T-2 闭环） |
| CHANGELOG.md | W1224 | 容量阈值裁决批 |
| HANDOVER.md | W1224 | 里程碑块（cascade 写入） |
| AGENTS.md | W1224 | 版本脚注滚动（cascade 写入） |
| archive/docs/AGENTS-ARCHIVE.md | W1224 | AGENTS 脚注滚动归档（cascade 写入） |
| docs/00-导读/W批次编号对账表.md | W1224 | W1224 认领行 |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1224 | 台账行窗口腾窗迁出最老行（archive 写入） |
| scripts/output/file-index.md | W1224 | 本批 file-index 段（cascade 写入） |
| scripts/output/stats.json | W1224 | stats 重跑 |
| scripts/output/stats-changelog.json | W1224 | stats 重跑产物 |
| scripts/output/stats-index.md | W1224 | stats 重跑产物 |
| scripts/output/_cascade_files_W1224.txt | W1224 | 级联落盘清单（cascade 生成） |
| scripts/output/_w1224_spec.json | W1224 | 本批 spec |
| README.md | W1224 | 版本面推进（version_surface） |
| STRUCTURE.md | W1224 | 版本面推进（version_surface） |
| CITATION.cff | W1224 | 版本面推进（version_surface） |
| docs/00-导读/项目说明.md | W1224 | 版本面推进（version_surface） |
| .github/workflows/README.md | W1224 | 版本面推进（version_surface） |
| archive/docs/workflows-readme-history.md | W1224 | workflows README 历史归档（version_surface） |
| site/data/search.html | W1224 | 搜索索引重建（方案/手册文档条目随动） |
| site/en/search.html | W1224 | 搜索索引重建（EN 版） |
| site/data/search-index-zh.js | W1224 | 索引数据件重写（生成器外置形态） |
| site/en/search-index-en.js | W1224 | 索引数据件重写（生成器外置形态） |
| scripts/output/INDEX.md | W1224 | 目录文档刷新（gen_folder_docs） |
| scripts/output/README.md | W1224 | 目录文档刷新（gen_folder_docs） |
| scripts/output/tools-inventory.md | W1224 | 工具盘点时间戳随动 |
| scripts/output/_vermilion_solid_cache.json | W1224 | 朱砂实底门禁增量缓存随页脚批次链更新（第 49 槽） |
| site/data/cross-time-danmaku.html | W1224 | 页脚批次链滚动（cascade 全档） |
| site/data/tag-cloud.html | W1224 | 页脚批次链滚动（cascade 全档） |
| site/dukou-engine.html | W1224 | 页脚批次链滚动（cascade 全档） |
| site/index.html | W1224 | 页脚批次链滚动（cascade 全档） |

## W1223 容量 #1 执行批：search 索引外置 + 第 46 槽判据域随迁 + #4 口径诚实化（2026-11-14）

| 文件 | W | 说明 |
|---|---|---|
| scripts/_gen_search_index.py | W1223 | main() 外科幂等改形：索引外置 JS 数据件 + 页面外链（docstring 同步） |
| scripts/check_search_index_fresh.py | W1223 | 第 46 槽判据域随迁：C1 双侧（数据件 + 页面外链）·自测 4→6 例 |
| scripts/check_capacity_budget.py | W1223 | #4 口径纳入两份索引数据件（诚实口径） |
| tests/unit/test_check_search_index_fresh.py | W1223 | G2 6/6 + G3 五类漂移同步 |
| site/data/search.html | W1223 | 内联索引段摘除 + 外链引用（460,148→112,449 B） |
| site/en/search.html | W1223 | 内联索引段摘除 + 外链引用（436,477→69,910 B） |
| site/data/search-index-zh.js | W1223 | 新增：ZH 索引数据件（348,805 B·标记对随迁） |
| site/en/search-index-en.js | W1223 | 新增：EN 索引数据件（367,673 B·标记对随迁） |
| CHANGELOG.md | W1223 | 容量 #1 执行批 |
| HANDOVER.md | W1223 | 里程碑块（cascade 写入） |
| AGENTS.md | W1223 | 版本脚注滚动（cascade 写入） |
| archive/docs/AGENTS-ARCHIVE.md | W1223 | AGENTS 脚注滚动归档（cascade 写入） |
| docs/00-导读/W批次编号对账表.md | W1223 | W1223 认领行 |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1223 | 台账行窗口腾窗迁出最老行（61>60·archive 写入） |
| scripts/output/file-index.md | W1223 | 本批 file-index 段（cascade 写入） |
| scripts/output/stats.json | W1223 | stats 重跑 |
| scripts/output/stats-changelog.json | W1223 | stats 重跑产物（cascade 刷新） |
| scripts/output/stats-index.md | W1223 | stats 重跑产物（cascade 刷新） |
| scripts/output/_cascade_files_W1223.txt | W1223 | 级联落盘清单（cascade 生成） |
| scripts/output/_w1223_spec.json | W1223 | 本批 spec |
| README.md | W1223 | 版本面推进（version_surface） |
| STRUCTURE.md | W1223 | 版本面推进（version_surface） |
| CITATION.cff | W1223 | 版本面推进（version_surface） |
| docs/00-导读/项目说明.md | W1223 | 版本面推进（version_surface） |
| .github/workflows/README.md | W1223 | 版本面推进（version_surface） |
| archive/docs/workflows-readme-history.md | W1223 | workflows README 历史归档（version_surface） |
| site/sitemap.xml | W1223 | sitemap 重建（search 两页 lastmod） |
| scripts/output/INDEX.md | W1223 | 目录文档刷新（gen_folder_docs） |
| scripts/output/README.md | W1223 | 目录文档刷新（gen_folder_docs） |
| scripts/output/tools-inventory.md | W1223 | 工具盘点时间戳随动（cascade） |
| scripts/output/_vermilion_solid_cache.json | W1223 | 朱砂实底门禁增量缓存随页脚批次链更新（第 49 槽） |
| site/data/cross-time-danmaku.html | W1223 | 页脚批次链滚动（cascade 全档） |
| site/data/tag-cloud.html | W1223 | 页脚批次链滚动（cascade 全档） |
| site/dukou-engine.html | W1223 | 页脚批次链滚动（cascade 全档） |
| site/index.html | W1223 | 页脚批次链滚动（cascade 全档） |

## W1222 容量阈值越线处置评估批：T-2 评估定稿 + T-3 运维制度化 + W1191 台账回填（2026-11-14）

| 文件 | W | 说明 |
|---|---|---|
| docs/11-方案报告/设计与架构方案/容量阈值越线处置评估-2026-11-14.md | W1222 | 新增：容量阈值越线处置评估报告（T-2 评估结论） |
| docs/11-方案报告/设计与架构方案/系统架构v2迁移施工手册-2026-11-13.md | W1222 | T-2/T-3 状态行与 §6.1/§6.2 订正（评估已交付·T-3 已落地） |
| docs/11-方案报告/README.md | W1222 | §二登记第 38 行 + 件数 20→21 |
| docs/agent/batch-closeout-checklist.md | W1222 | §9 增审计缺口窗口事件驱动行（T-3） |
| docs/agent/periodic-ops-checklist.md | W1222 | 新增：周期运维清单跟踪器（月/季/半年·T-3） |
| docs/agent/INDEX.md | W1222 | 目录文档刷新（gen_folder_docs·新增 periodic-ops-checklist） |
| docs/00-导读/W批次编号对账表.md | W1222 | W1191 行依证回填 + W1222 认领行 |
| CHANGELOG.md | W1222 | 容量阈值越线处置评估批 |
| HANDOVER.md | W1222 | 里程碑块（cascade 写入）+ HEAD 句 |
| AGENTS.md | W1222 | 版本脚注滚动（cascade 写入） |
| archive/docs/AGENTS-ARCHIVE.md | W1222 | AGENTS 脚注滚动归档（cascade 写入） |
| scripts/output/file-index.md | W1222 | 本批 file-index 段（cascade 写入） |
| scripts/output/stats.json | W1222 | stats 重跑（报告计数随新报告更新） |
| scripts/output/stats-changelog.json | W1222 | stats 重跑产物（cascade 刷新） |
| scripts/output/stats-index.md | W1222 | stats 重跑产物（cascade 刷新） |
| scripts/output/_cascade_files_W1222.txt | W1222 | 级联落盘清单（cascade 生成） |
| scripts/output/_w1222_spec.json | W1222 | 本批 spec |
| README.md | W1222 | 版本面推进（version_surface） |
| STRUCTURE.md | W1222 | 版本面推进（version_surface） |
| CITATION.cff | W1222 | 版本面推进（version_surface） |
| docs/00-导读/项目说明.md | W1222 | 版本面推进（version_surface） |
| .github/workflows/README.md | W1222 | 版本面推进（version_surface） |
| archive/docs/workflows-readme-history.md | W1222 | workflows README 历史归档（version_surface） |
| docs/INDEX.md | W1222 | 文档索引重建（docs_index） |
| site/data/search.html | W1222 | 搜索索引重建（新文档入索引） |
| site/en/search.html | W1222 | 搜索索引重建（EN 版） |
| site/sitemap.xml | W1222 | sitemap 重建（lastmod 刷新） |
| scripts/output/INDEX.md | W1222 | 目录文档刷新（gen_folder_docs） |
| scripts/output/README.md | W1222 | 目录文档刷新（gen_folder_docs） |
| scripts/output/tools-inventory.md | W1222 | 工具盘点时间戳随动（cascade） |
| scripts/output/_vermilion_solid_cache.json | W1222 | 朱砂实底门禁增量缓存随页脚批次链更新（第 49 槽） |
| site/data/cross-time-danmaku.html | W1222 | 页脚批次链滚动（cascade 全档） |
| site/data/tag-cloud.html | W1222 | 页脚批次链滚动（cascade 全档） |
| site/dukou-engine.html | W1222 | 页脚批次链滚动（cascade 全档） |
| site/index.html | W1222 | 页脚批次链滚动（cascade 全档） |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1222 | 报告类文档计数随动（stats sweep·181→182） |
| docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md | W1222 | 统计数字标记随动（stats sweep） |
| scripts/output/_w1205_capacity_audit.json | W1222 | 容量测量器复跑刷新（评估证据·固定输出路径） |

## W1221 架构 v2 迁移施工手册批：执行面重述 + 独立审查整改 + 入库登记（2026-11-13）

| 文件 | W | 说明 |
|---|---|---|
| docs/11-方案报告/设计与架构方案/系统架构v2迁移施工手册-2026-11-13.md | W1221 | 新增：架构 v2 迁移施工手册（执行面重述 + 独立审查整改） |
| docs/11-方案报告/README.md | W1221 | §二登记第 37 行 + 件数 19→20 |
| CHANGELOG.md | W1221 | 迁移施工手册批 |
| HANDOVER.md | W1221 | 里程碑块（cascade 写入） |
| AGENTS.md | W1221 | 版本脚注滚动（cascade 写入） |
| archive/docs/AGENTS-ARCHIVE.md | W1221 | AGENTS 脚注滚动归档（cascade 写入） |
| docs/00-导读/W批次编号对账表.md | W1221 | W1221 认领行 |
| scripts/output/file-index.md | W1221 | 本批 file-index 段（cascade 写入） |
| scripts/output/stats.json | W1221 | stats 重跑 |
| scripts/output/stats-changelog.json | W1221 | stats 重跑产物（cascade 刷新） |
| scripts/output/stats-index.md | W1221 | stats 重跑产物（cascade 刷新） |
| scripts/output/_cascade_files_W1221.txt | W1221 | 级联落盘清单（cascade 生成） |
| scripts/output/_w1221_spec.json | W1221 | 本批 spec |
| README.md | W1221 | 版本面推进（version_surface） |
| STRUCTURE.md | W1221 | 版本面推进（version_surface） |
| CITATION.cff | W1221 | 版本面推进（version_surface） |
| docs/00-导读/项目说明.md | W1221 | 版本面推进（version_surface） |
| docs/INDEX.md | W1221 | 文档索引重建（docs_index） |
| site/data/search.html | W1221 | 搜索索引重建（版本面推进后重建） |
| site/en/search.html | W1221 | 搜索索引重建（EN 版） |
| site/sitemap.xml | W1221 | sitemap 重建（lastmod 刷新） |
| scripts/output/INDEX.md | W1221 | 目录文档刷新（gen_folder_docs） |
| scripts/output/README.md | W1221 | 目录文档刷新（gen_folder_docs） |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1221 | 台账行窗口腾窗迁出最老行（archive 写入） |
| .github/workflows/README.md | W1221 | 版本面推进（version_surface） |
| archive/docs/workflows-readme-history.md | W1221 | workflows README 历史归档（version_surface） |
| docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md | W1221 | 统计数字标记随动（stats sweep） |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1221 | 报告类文档计数随动（stats sweep·180→181） |
| scripts/output/tools-inventory.md | W1221 | 工具盘点时间戳随动（cascade） |
| scripts/output/_vermilion_solid_cache.json | W1221 | 朱砂实底门禁增量缓存随页脚批次链更新（第 49 槽） |
| site/data/cross-time-danmaku.html | W1221 | 页脚批次链滚动（cascade 全档） |
| site/data/tag-cloud.html | W1221 | 页脚批次链滚动（cascade 全档） |
| site/dukou-engine.html | W1221 | 页脚批次链滚动（cascade 全档） |
| site/index.html | W1221 | 页脚批次链滚动（cascade 全档） |

## W1220 CI 提速批：pytest 时间黑洞根修 + 三片并行 + 站点作业路由（2026-11-13）

| 文件 | W | 说明 |
|---|---|---|
| .github/workflows/README.md | W1220 | ci.yml job 清单更新（12 job·三片并行与范围判定） |
| .github/workflows/ci-sim.yml | W1220 | 删除重复 pip 安装行 |
| .github/workflows/ci.yml | W1220 | changes 范围判定 + pytest 三片 + 聚合 + 缓存与路由 |
| AGENTS.md | W1220 | 版本脚注滚动（cascade 写入） |
| CHANGELOG.md | W1220 | CI 提速批 |
| CITATION.cff | W1220 | 版本面推进（version_surface） |
| HANDOVER.md | W1220 | 里程碑块（cascade 写入） |
| README.md | W1220 | 版本面推进（version_surface） |
| STRUCTURE.md | W1220 | 版本面推进（version_surface） |
| archive/docs/AGENTS-ARCHIVE.md | W1220 | AGENTS 脚注滚动归档（cascade 写入） |
| archive/docs/workflows-readme-history.md | W1220 | workflows README 历史归档（version_surface） |
| docs/00-导读/W批次编号对账表.md | W1220 | W1220 认领行 |
| docs/00-导读/项目说明.md | W1220 | 版本面推进（version_surface） |
| pitfalls.md | W1220 | 新增 E-231（import 期重活/可导入假绿）+ E-232（required check 名不可变） |
| scripts/a11y_audit.py | W1220 | a11y 扫描多进程并行（--jobs·ex.map 保序） |
| scripts/containment_block_scan.py | W1220 | 扫描移入 main() + 只扫 style 块（67.6s→0.8s） |
| scripts/output/INDEX.md | W1220 | 目录文档刷新（gen_folder_docs） |
| scripts/output/README.md | W1220 | 目录文档刷新（gen_folder_docs） |
| scripts/output/_cascade_files_W1220.txt | W1220 | 级联落盘清单（cascade 生成） |
| scripts/output/_w1220_spec.json | W1220 | 本批 spec |
| scripts/output/file-index.md | W1220 | 本批 file-index 段（cascade 写入） |
| scripts/output/stats.json | W1220 | stats 重跑（计数跟随） |
| scripts/output/tools-inventory.md | W1220 | 工具盘点时间戳随动（cascade） |
| site/data/cross-time-danmaku.html | W1220 | 页脚批次链滚动（cascade 全档） |
| site/data/tag-cloud.html | W1220 | 页脚批次链滚动（cascade 全档） |
| site/dukou-engine.html | W1220 | 页脚批次链滚动（cascade 全档） |
| site/index.html | W1220 | 页脚批次链滚动（cascade 全档） |
| tests/unit/test_ci_wiring.py | W1220 | required check 名与聚合结构锁 |
| tests/unit/test_tool_scripts_cli.py | W1220 | import 期时间预算判据（IMPORT_BUDGET_S） |

## W1219 归档维护批：段目录组行补登 + 一级归档分卷 + 临时区归桶（2026-11-13）

| 文件 | W | 说明 |
|---|---|---|
| .github/workflows/README.md | W1219 | 版本面推进（version_surface） |
| AGENTS.md | W1219 | 版本脚注滚动（cascade 写入） |
| CHANGELOG.md | W1219 | 归档维护批 |
| CITATION.cff | W1219 | 版本面推进（version_surface） |
| HANDOVER.md | W1219 | 里程碑块（cascade 写入） |
| README.md | W1219 | 版本面推进（version_surface） |
| STRUCTURE.md | W1219 | 版本面推进（version_surface） |
| archive/README.md | W1219 | 段目录组行补登（w1169/w1175/w1176） |
| archive/docs/AGENTS-ARCHIVE.md | W1219 | AGENTS 脚注滚动归档（cascade 写入） |
| archive/docs/CHANGELOG-ARCHIVE.md | W1219 | 一级归档分卷（迁出 W814-W874·回落 899KB） |
| archive/docs/CHANGELOG-ARCHIVE-tier2-W814-W874.md | W1219 | 新建二级归档分卷（59 段·196KB） |
| archive/docs/file-index-ARCHIVE.md | W1219 | 一级归档分卷（迁出 W980-W1023·回落 899KB） |
| archive/docs/file-index-ARCHIVE-tier2.md | W1219 | 二级归档追加 48 段（189KB） |
| archive/docs/INDEX.md | W1219 | 目录文档刷新（gen_folder_docs·新分卷入清单） |
| archive/docs/README.md | W1219 | 目录文档刷新（gen_folder_docs·新分卷入清单） |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1219 | 台账腾窗迁出最老行（archive 写入） |
| archive/docs/workflows-readme-history.md | W1219 | workflows README 历史归档（version_surface） |
| docs/00-导读/W批次编号对账表.md | W1219 | W1219 认领行 + 台账腾窗 |
| docs/00-导读/项目说明.md | W1219 | 版本面推进（version_surface） |
| scripts/output/stats.json | W1219 | stats 重跑生成时点刷新（值无变更） |
| scripts/output/INDEX.md | W1219 | 目录文档刷新（gen_folder_docs） |
| scripts/output/README.md | W1219 | 目录文档刷新（gen_folder_docs） |
| scripts/output/_cascade_files_W1219.txt | W1219 | 级联落盘清单（cascade 生成） |
| scripts/output/_w1219_spec.json | W1219 | 本批 spec |
| scripts/output/file-index.md | W1219 | 本批 file-index 段（cascade 写入） |
| scripts/output/tools-inventory.md | W1219 | 工具盘点时间戳随动（cascade） |
| site/data/cross-time-danmaku.html | W1219 | 页脚批次链滚动（cascade 全档） |
| site/data/tag-cloud.html | W1219 | 页脚批次链滚动（cascade 全档） |
| site/dukou-engine.html | W1219 | 页脚批次链滚动（cascade 全档） |
| site/index.html | W1219 | 页脚批次链滚动（cascade 全档） |

## W1218 审查整改批：LFS 判据 fail-closed + C5 前置 + 计数跟随（2026-11-13）

| 文件 | W | 说明 |
|---|---|---|
| .github/workflows/README.md | W1218 | 版本面推进（version_surface） |
| AGENTS.md | W1218 | 版本脚注滚动（cascade 写入） |
| CHANGELOG.md | W1218 | 审查整改批 |
| CITATION.cff | W1218 | 版本面推进（version_surface） |
| HANDOVER.md | W1218 | 里程碑块（cascade 写入） |
| README.md | W1218 | 版本面推进（version_surface） |
| STRUCTURE.md | W1218 | 版本面推进（version_surface） |
| archive/docs/AGENTS-ARCHIVE.md | W1218 | AGENTS 脚注滚动归档（cascade 写入） |
| archive/docs/workflows-readme-history.md | W1218 | workflows README 历史归档（version_surface） |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1218 | 台账腾窗迁出最老行（archive 写入） |
| docs/00-导读/W批次编号对账表.md | W1218 | W1218 认领行 + 台账腾窗 |
| docs/00-导读/项目说明.md | W1218 | 版本面推进（version_surface） |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1218 | stats 标记跟随（pytest_collected） |
| pytest.ini | W1218 | pytest_collected 标记跟随（新增 2 例） |
| scripts/check_folder_docs.py | W1218 | C5 前移到结构解析之前（抽 _c1_fails/_c5_precheck） |
| scripts/check_lfs_text_purity.py | W1218 | cat-file 返回码检查（fail-closed exit 2） |
| scripts/output/INDEX.md | W1218 | 目录文档刷新（gen_folder_docs） |
| scripts/output/README.md | W1218 | 目录文档刷新（gen_folder_docs） |
| scripts/output/_cascade_files_W1218.txt | W1218 | 级联落盘清单（cascade 生成） |
| scripts/output/_w1218_spec.json | W1218 | 本批 spec |
| scripts/output/file-index.md | W1218 | 本批 file-index 段（cascade 写入） |
| scripts/output/stats-changelog.json | W1218 | stats 变更史（pytest_collected） |
| scripts/output/stats-index.md | W1218 | stats 反向索引重渲 |
| scripts/output/stats.json | W1218 | stats 实算刷新（pytest_collected 1635→1637） |
| scripts/output/tools-inventory.md | W1218 | 工具盘点时间戳随动（cascade/gate） |
| scripts/output/_vermilion_solid_cache.json | W1218 | 朱砂门禁增量缓存随动（第 49 槽实跑刷新） |
| site/data/cross-time-danmaku.html | W1218 | 页脚批次链滚动（cascade 全档） |
| site/data/tag-cloud.html | W1218 | 页脚批次链滚动（cascade 全档） |
| site/dukou-engine.html | W1218 | 页脚批次链滚动（cascade 全档） |
| site/index.html | W1218 | 页脚批次链滚动（cascade 全档） |
| tests/unit/test_folder_docs_gate.py | W1218 | 新增 C5 指针消息 1 例 |
| tests/unit/test_lfs_text_purity.py | W1218 | 新增 cat-file fail-closed 1 例 |

## W1217 审查整改批：ci_sim 自跳过降级 + dry-run 零写盘 + 登记面校正（2026-11-13）

| 文件 | W | 说明 |
|---|---|---|
| .github/workflows/README.md | W1217 | 版本面推进（version_surface） |
| AGENTS.md | W1217 | 版本脚注滚动（cascade 写入） |
| CHANGELOG.md | W1217 | 审查整改批 |
| CITATION.cff | W1217 | 版本面推进（version_surface） |
| HANDOVER.md | W1217 | 里程碑块（cascade 写入） |
| README.md | W1217 | 版本面推进（version_surface） |
| STRUCTURE.md | W1217 | 版本面推进（version_surface） |
| archive/docs/AGENTS-ARCHIVE.md | W1217 | AGENTS 脚注滚动归档（cascade 写入） |
| archive/docs/workflows-readme-history.md | W1217 | workflows README 历史归档（version_surface） |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1217 | 台账腾窗迁出最老行（archive 写入） |
| docs/00-导读/W批次编号对账表.md | W1217 | W1217 认领行 + 台账腾窗 |
| docs/00-导读/项目说明.md | W1217 | 版本面推进（version_surface） |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1217 | stats 标记跟随（pytest_collected） |
| pytest.ini | W1217 | pytest_collected 标记跟随（新增 4 例） |
| scripts/batch_closeout.py | W1217 | dry-run 零写盘：cascade/archive/rebuild 增 dry 参数 |
| scripts/check_gov_doc_claims.py | W1217 | N3/N4 剥 stats 标记后匹配 + 自测补带标记句 |
| scripts/pre_push_gate.py | W1217 | 脏度前置快照 + ci_sim 自跳过计入判据降级 |
| scripts/output/INDEX.md | W1217 | 目录文档刷新（gen_folder_docs） |
| scripts/output/README.md | W1217 | 目录文档刷新（gen_folder_docs） |
| scripts/output/_cascade_files_W1217.txt | W1217 | 级联落盘清单（cascade 生成） |
| scripts/output/_w1216_spec.json | W1217 | 删未落地 sitemap 行（登记面校正） |
| scripts/output/_w1217_spec.json | W1217 | 本批 spec |
| scripts/output/file-index.md | W1217 | 本批 file-index 段（cascade 写入） |
| scripts/output/stats-changelog.json | W1217 | stats 变更史（pytest_collected） |
| scripts/output/stats-index.md | W1217 | stats 反向索引重渲 |
| scripts/output/stats.json | W1217 | stats 实算刷新（pytest_collected 1631→1635） |
| scripts/output/tools-inventory.md | W1217 | 工具盘点时间戳随动（cascade/gate） |
| scripts/output/_vermilion_solid_cache.json | W1217 | 朱砂门禁增量缓存随动（第 49 槽实跑刷新） |
| site/data/cross-time-danmaku.html | W1217 | 页脚批次链滚动（cascade 全档） |
| site/data/tag-cloud.html | W1217 | 页脚批次链滚动（cascade 全档） |
| site/dukou-engine.html | W1217 | 页脚批次链滚动（cascade 全档） |
| site/index.html | W1217 | 页脚批次链滚动（cascade 全档） |
| site/sitemap.xml | W1217 | sitemap 重渲（gen_sitemap） |
| tests/unit/test_check_placeholder_hash_carrier.py | W1217 | 槽总数派生改无界正则 |
| tests/unit/test_pre_push_gate.py | W1217 | 新增 plan_run 3 例（自跳过降级锁） |
| tests/unit/test_w1102_batch_closeout.py | W1217 | 新增 dry-run 零写盘 1 例 |
| tests/unit/test_w1141_gate_mount.py | W1217 | 槽号统计改无界正则 |

## W1216 收尾清偿批：台账 hash 回填 + 「71 槽」marker 化 + 复盘弧线交付（2026-11-12）

| 文件 | W | 说明 |
|---|---|---|
| .github/workflows/README.md | W1216 | 版本面推进（cascade/versions 写入） |
| AGENTS.md | W1216 | 71 槽 marker 化 ×3（gate_count） |
| CHANGELOG.md | W1216 | 收尾清偿批 |
| CITATION.cff | W1216 | 版本面推进（version_surface） |
| HANDOVER.md | W1216 | 71 槽 marker 化 ×2 + 里程碑块 |
| README.md | W1216 | 版本面推进（version_surface） |
| archive/docs/AGENTS-ARCHIVE.md | W1216 | AGENTS 脚注滚动归档（cascade 写入） |
| archive/docs/workflows-readme-history.md | W1216 | workflows README 历史归档（version_surface） |
| docs/00-导读/W批次编号对账表.md | W1216 | W1216 认领行 + W1214/W1215 hash 回填 |
| docs/11-方案报告/README.md | W1216 | 复盘弧线篇登记（19 件/新行/总览纠偏） |
| docs/11-方案报告/工作复盘与优化分析报告/工作复盘与优化分析报告-2026-11-12.md | W1216 | 新建：复盘弧线篇（W1212-W1215 弧线·三绿不同源主题） |
| docs/agent/gates.md | W1216 | 标题 71 槽 marker 化 |
| scripts/batch_closeout.py | W1216 | index 步内序根修（docs_index 在前·搜索内嵌派生字段陈旧族） |
| scripts/output/_vermilion_solid_cache.json | W1216 | 朱砂门禁增量缓存随动（惯例入库件） |
| docs/INDEX.md | W1216 | 文档索引重渲（+1 篇·docs_index） |
| scripts/output/_cascade_files_W1216.txt | W1216 | 级联落盘清单（cascade 生成） |
| scripts/output/_w1216_spec.json | W1216 | 本批 spec |
| scripts/output/file-index.md | W1216 | 本批 file-index 段（cascade 写入） |
| scripts/output/INDEX.md | W1216 | 目录文档刷新（gen_folder_docs） |
| scripts/output/README.md | W1216 | 目录文档刷新（gen_folder_docs） |
| scripts/output/stats-changelog.json | W1216 | stats 变更史（report_docs 等） |
| scripts/output/stats-index.md | W1216 | stats 反向索引重渲 |
| scripts/output/stats.json | W1216 | stats 实算刷新（report_docs +1） |
| scripts/output/tools-inventory.md | W1216 | 工具盘点时间戳随动（cascade） |
| STRUCTURE.md | W1216 | 版本面推进（version_surface） |
| docs/00-导读/项目说明.md | W1216 | 版本面推进（version_surface） |
| docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md | W1216 | sweep 存量面标记跟随（report_docs·自动） |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1216 | sweep 存量面标记跟随（report_docs·自动） |
| site/data/cross-time-danmaku.html | W1216 | 页脚四面批次版本随动（cascade 全档） |
| site/data/search.html | W1216 | 搜索索引重渲（自动） |
| site/data/tag-cloud.html | W1216 | 页脚四面批次版本随动（cascade 全档） |
| site/en/search.html | W1216 | 搜索索引重渲（自动） |
| site/dukou-engine.html | W1216 | 页脚四面批次版本随动（cascade 全档） |
| site/index.html | W1216 | 页脚四面批次版本随动 + C5b 标记面 |
| tests/unit/test_check_placeholder_hash_carrier.py | W1216 | 声明面断言剥标记容错（gate_count marker） |
| tests/unit/test_w1102_batch_closeout.py | W1216 | 行为锁随 index 内序对调更新（docs_index 在前） |
| tests/unit/test_w1141_gate_mount.py | W1216 | 槽数断言剥标记容错（gate_count marker） |

## W1215 一命令真全量与计数链生成器化批：pre_push_gate + 收官链接步 + 计数链 markers（2026-11-12）

| 文件 | W | 说明 |
|---|---|---|
| .agent/skills/puti-shouye/SKILL.md | W1215 | 一命令真全量与计数链生成器化批：坑位计数 markers 化 |
| AGENTS.md | W1215 | 一命令真全量与计数链生成器化批：就绪链可执行化 + 计数 markers + §5.2 登记 |
| CHANGELOG.md | W1215 | 一命令真全量与计数链生成器化批 |
| CLAUDE.md | W1215 | 一命令真全量与计数链生成器化批：pre_push_gate/closeout 命令登记 |
| HANDOVER.md | W1215 | 一命令真全量与计数链生成器化批：计数 markers + 里程碑块 |
| STRUCTURE.md | W1215 | 一命令真全量与计数链生成器化批：坑位计数 marker 化 |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1215 | 台账腾窗迁出 2 行（W1152-W1153·preflight 超窗前置清偿） |
| docs/00-导读/W批次编号对账表.md | W1215 | W1215 认领行 + 台账腾窗（61→59 行） |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1215 | sweep 存量面标记跟随（C5b 对账面·自动） |
| docs/agent/pitfalls.md | W1215 | 跳转壳坑位计数 marker 化 |
| pitfalls.md | W1215 | E-229 入表 + 六主题段头 markers |
| pytest.ini | W1215 | sweep 收集数标记跟随（新 16 例·自动） |
| scripts/batch_closeout.py | W1215 | cascade 链首 + gate 链尾接步 + _run_finalize 抽函数 |
| scripts/check_doc_sync.py | W1215 | pitfall_theme_counts 取数面 + C5e 剥标记补盲 + C5b 面扩展 |
| scripts/output/_cascade_files_W1215.txt | W1215 | 级联落盘清单（cascade 生成） |
| scripts/output/_w1215_spec.json | W1215 | 本批 spec |
| scripts/output/file-index.md | W1215 | 本批 file-index 段（cascade 写入） |
| scripts/output/stats-changelog.json | W1215 | stats 变更史（W1215·7 新键 + 坑位族） |
| scripts/output/stats-index.md | W1215 | stats 反向索引重渲 |
| scripts/output/stats.json | W1215 | stats 实算刷新（pitfalls 族 7 新键） |
| scripts/output/tools-inventory.md | W1215 | 工具盘点重渲（+1 件 pre_push_gate） |
| scripts/gen_sitemap.py | W1215 | sitemap lastmod UTC 钳（R3 时区窗根修·CI 回检补笔） |
| scripts/pre_push_gate.py | W1215 | 新建：一命令真全量编排器（guardrails→verify→pytest→ci_sim） |
| scripts/stats.py | W1215 | pitfalls 族 7 新键 + 窄域 sweep + 既有嵌套随档根修 |
| site/data/search.html | W1215 | 搜索索引重渲（文档计数随动·自动） |
| site/en/search.html | W1215 | 搜索索引重渲（文档计数随动·自动） |
| tests/unit/test_pre_push_gate.py | W1215 | 新建：pre_push_gate 纯逻辑 10 例 |
| tests/unit/test_w1114_version_surface.py | W1215 | 步序锁随链更新（cascade 链首/gate 链尾） |
| tests/unit/test_w1215_count_markers.py | W1215 | 新建：计数链生成器化 6 例（含窄域与盲区负样本） |
| tests/unit/test_w1124_closeout_rebuild.py | W1215 | 步序锁随链更新（cascade 链首/gate 链尾） |
| .github/workflows/README.md | W1215 | 版本面推进（head_entry·cascade/versions 写入） |
| CITATION.cff | W1215 | 版本面推进（version_surface） |
| README.md | W1215 | 版本面推进（version_surface） |
| archive/docs/AGENTS-ARCHIVE.md | W1215 | AGENTS 脚注滚动归档（cascade 写入） |
| archive/docs/workflows-readme-history.md | W1215 | workflows README 历史归档（version_surface） |
| docs/00-导读/项目说明.md | W1215 | 版本面推进（version_surface） |
| scripts/INDEX.md | W1215 | 目录文档刷新（+pre_push_gate·gen_folder_docs） |
| scripts/output/INDEX.md | W1215 | 目录文档刷新（gen_folder_docs） |
| scripts/output/README.md | W1215 | 目录文档刷新（gen_folder_docs） |
| site/data/cross-time-danmaku.html | W1215 | 页脚四面批次版本随动（cascade 全档） |
| site/data/tag-cloud.html | W1215 | 页脚四面批次版本随动（cascade 全档） |
| site/dukou-engine.html | W1215 | 页脚四面批次版本随动（cascade 全档） |
| site/index.html | W1215 | 页脚四面批次版本随动 + C5b 标记面 |
| site/sitemap.xml | W1215 | sitemap 重渲（gen_sitemap） |
| tests/unit/INDEX.md | W1215 | 目录文档刷新（+2 测试文件·gen_folder_docs） |
| tests/unit/README.md | W1215 | 目录文档刷新（gen_folder_docs） |
| Makefile | W1215 | gate 目标登记（编排面·第 42 槽 C1 四面引用） |
| tests/unit/test_w1102_batch_closeout.py | W1215 | 步序锁随链更新（真全量 gate 首跑抓漏） |
| scripts/output/_vermilion_solid_cache.json | W1215 | 朱砂门禁增量缓存随动（近四批惯例入库件） |

## W1214 LFS 文本文件根修批：文本文件移出 LFS + 第 45 槽 C5 防复发（2026-11-12）

| 文件 | W | 说明 |
|---|---|---|
| .agent/skills/puti-shouye/SKILL.md | W1214 | LFS 文本文件根修批：文本移出 LFS 与第 45 槽 C5 防复发 |
| .gitattributes | W1214 | LFS 文本文件根修批：文本移出 LFS 与第 45 槽 C5 防复发 |
| .github/workflows/README.md | W1214 | LFS 文本文件根修批：文本移出 LFS 与第 45 槽 C5 防复发 |
| AGENTS.md | W1214 | LFS 文本文件根修批：文本移出 LFS 与第 45 槽 C5 防复发 |
| CHANGELOG.md | W1214 | LFS 文本文件根修批：文本移出 LFS 与第 45 槽 C5 防复发 |
| CITATION.cff | W1214 | LFS 文本文件根修批：文本移出 LFS 与第 45 槽 C5 防复发 |
| HANDOVER.md | W1214 | LFS 文本文件根修批：文本移出 LFS 与第 45 槽 C5 防复发 |
| Makefile | W1214 | LFS 文本文件根修批：文本移出 LFS 与第 45 槽 C5 防复发 |
| README.md | W1214 | LFS 文本文件根修批：文本移出 LFS 与第 45 槽 C5 防复发 |
| STRUCTURE.md | W1214 | LFS 文本文件根修批：文本移出 LFS 与第 45 槽 C5 防复发 |
| archive/docs/AGENTS-ARCHIVE.md | W1214 | LFS 文本文件根修批：文本移出 LFS 与第 45 槽 C5 防复发 |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1214 | LFS 文本文件根修批：文本移出 LFS 与第 45 槽 C5 防复发 |
| archive/docs/workflows-readme-history.md | W1214 | LFS 文本文件根修批：文本移出 LFS 与第 45 槽 C5 防复发 |
| assets/promo/INDEX.md | W1214 | LFS 文本文件根修批：文本移出 LFS 与第 45 槽 C5 防复发 |
| assets/promo/hero-set/INDEX.md | W1214 | LFS 文本文件根修批：文本移出 LFS 与第 45 槽 C5 防复发 |
| assets/promo/hero-set/raw/INDEX.md | W1214 | LFS 文本文件根修批：文本移出 LFS 与第 45 槽 C5 防复发 |
| assets/promo/hero-set/raw/round-w1005/INDEX.md | W1214 | LFS 文本文件根修批：文本移出 LFS 与第 45 槽 C5 防复发 |
| assets/promo/hero-set/raw/round-w1005/README.md | W1214 | LFS 文本文件根修批：文本移出 LFS 与第 45 槽 C5 防复发 |
| assets/promo/output/INDEX.md | W1214 | LFS 文本文件根修批：文本移出 LFS 与第 45 槽 C5 防复发 |
| assets/promo/output/README.md | W1214 | LFS 文本文件根修批：文本移出 LFS 与第 45 槽 C5 防复发 |
| assets/promo/plate-set/INDEX.md | W1214 | LFS 文本文件根修批：文本移出 LFS 与第 45 槽 C5 防复发 |
| assets/promo/xiyouji-flyer-a4-en.html | W1214 | LFS 文本文件根修批：文本移出 LFS 与第 45 槽 C5 防复发 |
| assets/promo/xiyouji-flyer-a4.html | W1214 | LFS 文本文件根修批：文本移出 LFS 与第 45 槽 C5 防复发 |
| docs/00-导读/W批次编号对账表.md | W1214 | LFS 文本文件根修批：文本移出 LFS 与第 45 槽 C5 防复发 |
| docs/00-导读/项目说明.md | W1214 | LFS 文本文件根修批：文本移出 LFS 与第 45 槽 C5 防复发 |
| docs/11-方案报告/README.md | W1214 | LFS 文本文件根修批：文本移出 LFS 与第 45 槽 C5 防复发 |
| docs/11-方案报告/计划方案/T102-任务计划执行与经验沉淀报告-2026-11-12.md | W1214 | LFS 文本文件根修批：文本移出 LFS 与第 45 槽 C5 防复发 |
| docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md | W1214 | LFS 文本文件根修批：文本移出 LFS 与第 45 槽 C5 防复发 |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1214 | LFS 文本文件根修批：文本移出 LFS 与第 45 槽 C5 防复发 |
| docs/INDEX.md | W1214 | LFS 文本文件根修批：文本移出 LFS 与第 45 槽 C5 防复发 |
| docs/agent/gates.md | W1214 | LFS 文本文件根修批：文本移出 LFS 与第 45 槽 C5 防复发 |
| docs/agent/pitfalls.md | W1214 | LFS 文本文件根修批：文本移出 LFS 与第 45 槽 C5 防复发 |
| pitfalls.md | W1214 | LFS 文本文件根修批：文本移出 LFS 与第 45 槽 C5 防复发 |
| pytest.ini | W1214 | LFS 文本文件根修批：文本移出 LFS 与第 45 槽 C5 防复发 |
| scripts/INDEX.md | W1214 | LFS 文本文件根修批：文本移出 LFS 与第 45 槽 C5 防复发 |
| scripts/check_folder_docs.py | W1214 | LFS 文本文件根修批：文本移出 LFS 与第 45 槽 C5 防复发 |
| scripts/check_lfs_text_purity.py | W1214 | LFS 文本文件根修批：文本移出 LFS 与第 45 槽 C5 防复发 |
| scripts/ci_sim.py | W1214 | LFS 文本文件根修批：文本移出 LFS 与第 45 槽 C5 防复发 |
| scripts/output/INDEX.md | W1214 | LFS 文本文件根修批：文本移出 LFS 与第 45 槽 C5 防复发 |
| scripts/output/README.md | W1214 | LFS 文本文件根修批：文本移出 LFS 与第 45 槽 C5 防复发 |
| scripts/output/_cascade_files_W1214.txt | W1214 | LFS 文本文件根修批：文本移出 LFS 与第 45 槽 C5 防复发 |
| scripts/output/_vermilion_solid_cache.json | W1214 | LFS 文本文件根修批：文本移出 LFS 与第 45 槽 C5 防复发 |
| scripts/output/_w1214_spec.json | W1214 | LFS 文本文件根修批：文本移出 LFS 与第 45 槽 C5 防复发 |
| scripts/output/file-index.md | W1214 | LFS 文本文件根修批：文本移出 LFS 与第 45 槽 C5 防复发 |
| scripts/output/stats-changelog.json | W1214 | LFS 文本文件根修批：文本移出 LFS 与第 45 槽 C5 防复发 |
| scripts/output/stats-index.md | W1214 | LFS 文本文件根修批：文本移出 LFS 与第 45 槽 C5 防复发 |
| scripts/output/stats.json | W1214 | LFS 文本文件根修批：文本移出 LFS 与第 45 槽 C5 防复发 |
| scripts/output/tools-inventory.md | W1214 | LFS 文本文件根修批：文本移出 LFS 与第 45 槽 C5 防复发 |
| site/data/cross-time-danmaku.html | W1214 | LFS 文本文件根修批：文本移出 LFS 与第 45 槽 C5 防复发 |
| site/data/search.html | W1214 | LFS 文本文件根修批：文本移出 LFS 与第 45 槽 C5 防复发 |
| site/data/tag-cloud.html | W1214 | LFS 文本文件根修批：文本移出 LFS 与第 45 槽 C5 防复发 |
| site/dukou-engine.html | W1214 | LFS 文本文件根修批：文本移出 LFS 与第 45 槽 C5 防复发 |
| site/en/search.html | W1214 | LFS 文本文件根修批：文本移出 LFS 与第 45 槽 C5 防复发 |
| site/index.html | W1214 | LFS 文本文件根修批：文本移出 LFS 与第 45 槽 C5 防复发 |
| tests/unit/INDEX.md | W1214 | LFS 文本文件根修批：文本移出 LFS 与第 45 槽 C5 防复发 |
| tests/unit/README.md | W1214 | LFS 文本文件根修批：文本移出 LFS 与第 45 槽 C5 防复发 |
| tests/unit/test_lfs_text_purity.py | W1214 | LFS 文本文件根修批：文本移出 LFS 与第 45 槽 C5 防复发 |

## W1212 第 45 槽失败明细并入汇总行批：排障盲区根修（2026-11-12）

| 文件 | W | 说明 |
|---|---|---|
| .github/workflows/README.md | W1212 | 第 45 槽失败明细并入汇总行  排障盲区根修 |
| AGENTS.md | W1212 | 第 45 槽失败明细并入汇总行  排障盲区根修 |
| CHANGELOG.md | W1212 | 第 45 槽失败明细并入汇总行  排障盲区根修 |
| CITATION.cff | W1212 | 第 45 槽失败明细并入汇总行  排障盲区根修 |
| HANDOVER.md | W1212 | 第 45 槽失败明细并入汇总行  排障盲区根修 |
| README.md | W1212 | 第 45 槽失败明细并入汇总行  排障盲区根修 |
| STRUCTURE.md | W1212 | 第 45 槽失败明细并入汇总行  排障盲区根修 |
| archive/docs/AGENTS-ARCHIVE.md | W1212 | 第 45 槽失败明细并入汇总行  排障盲区根修 |
| archive/docs/workflows-readme-history.md | W1212 | 第 45 槽失败明细并入汇总行  排障盲区根修 |
| docs/00-导读/W批次编号对账表.md | W1212 | 第 45 槽失败明细并入汇总行  排障盲区根修 |
| docs/00-导读/项目说明.md | W1212 | 第 45 槽失败明细并入汇总行  排障盲区根修 |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1212 | 第 45 槽失败明细并入汇总行  排障盲区根修 |
| pytest.ini | W1212 | 第 45 槽失败明细并入汇总行  排障盲区根修 |
| scripts/check_folder_docs.py | W1212 | 第 45 槽失败明细并入汇总行  排障盲区根修 |
| scripts/output/INDEX.md | W1212 | 第 45 槽失败明细并入汇总行  排障盲区根修 |
| scripts/output/README.md | W1212 | 第 45 槽失败明细并入汇总行  排障盲区根修 |
| scripts/output/_cascade_files_W1212.txt | W1212 | 第 45 槽失败明细并入汇总行  排障盲区根修 |
| scripts/output/_w1212_spec.json | W1212 | 第 45 槽失败明细并入汇总行  排障盲区根修 |
| scripts/output/file-index.md | W1212 | 第 45 槽失败明细并入汇总行  排障盲区根修 |
| scripts/output/stats-changelog.json | W1212 | 第 45 槽失败明细并入汇总行  排障盲区根修 |
| scripts/output/stats-index.md | W1212 | 第 45 槽失败明细并入汇总行  排障盲区根修 |
| scripts/output/stats.json | W1212 | 第 45 槽失败明细并入汇总行  排障盲区根修 |
| scripts/output/tools-inventory.md | W1212 | 第 45 槽失败明细并入汇总行  排障盲区根修 |
| site/data/cross-time-danmaku.html | W1212 | 第 45 槽失败明细并入汇总行  排障盲区根修 |
| site/data/tag-cloud.html | W1212 | 第 45 槽失败明细并入汇总行  排障盲区根修 |
| site/dukou-engine.html | W1212 | 第 45 槽失败明细并入汇总行  排障盲区根修 |
| site/index.html | W1212 | 第 45 槽失败明细并入汇总行  排障盲区根修 |
| tests/unit/INDEX.md | W1212 | 第 45 槽失败明细并入汇总行  排障盲区根修 |
| tests/unit/README.md | W1212 | 第 45 槽失败明细并入汇总行  排障盲区根修 |
| tests/unit/test_folder_docs_summary.py | W1212 | 第 45 槽失败明细并入汇总行  排障盲区根修 |

## W1211 CI 修复与机制补强批：apt 源回退 + 第 71 槽接 ci_sim + Backlog 对账清偿（2026-11-12）

| 文件 | W | 说明 |
|---|---|---|
| .agent/skills/puti-shouye/SKILL.md | W1211 | CI 修复与机制补强  apt 源回退 + 第 71 槽接 ci_sim |
| .github/workflows/README.md | W1211 | CI 修复与机制补强  apt 源回退 + 第 71 槽接 ci_sim |
| .github/workflows/ci-sim.yml | W1211 | CI 修复与机制补强  apt 源回退 + 第 71 槽接 ci_sim |
| .github/workflows/ci.yml | W1211 | CI 修复与机制补强  apt 源回退 + 第 71 槽接 ci_sim |
| .github/workflows/screenshot-review.yml | W1211 | CI 修复与机制补强  apt 源回退 + 第 71 槽接 ci_sim |
| AGENTS.md | W1211 | CI 修复与机制补强  apt 源回退 + 第 71 槽接 ci_sim |
| CHANGELOG.md | W1211 | CI 修复与机制补强  apt 源回退 + 第 71 槽接 ci_sim |
| CITATION.cff | W1211 | CI 修复与机制补强  apt 源回退 + 第 71 槽接 ci_sim |
| HANDOVER.md | W1211 | CI 修复与机制补强  apt 源回退 + 第 71 槽接 ci_sim |
| README.md | W1211 | CI 修复与机制补强  apt 源回退 + 第 71 槽接 ci_sim |
| STRUCTURE.md | W1211 | CI 修复与机制补强  apt 源回退 + 第 71 槽接 ci_sim |
| archive/docs/AGENTS-ARCHIVE.md | W1211 | CI 修复与机制补强  apt 源回退 + 第 71 槽接 ci_sim |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1211 | CI 修复与机制补强  apt 源回退 + 第 71 槽接 ci_sim |
| archive/docs/workflows-readme-history.md | W1211 | CI 修复与机制补强  apt 源回退 + 第 71 槽接 ci_sim |
| docs/00-导读/W批次编号对账表.md | W1211 | CI 修复与机制补强  apt 源回退 + 第 71 槽接 ci_sim |
| docs/00-导读/项目说明.md | W1211 | CI 修复与机制补强  apt 源回退 + 第 71 槽接 ci_sim |
| docs/11-方案报告/README.md | W1211 | CI 修复与机制补强  apt 源回退 + 第 71 槽接 ci_sim |
| docs/11-方案报告/计划方案/T101-任务计划执行与经验沉淀报告-2026-11-12.md | W1211 | CI 修复与机制补强  apt 源回退 + 第 71 槽接 ci_sim |
| docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md | W1211 | CI 修复与机制补强  apt 源回退 + 第 71 槽接 ci_sim |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1211 | CI 修复与机制补强  apt 源回退 + 第 71 槽接 ci_sim |
| docs/INDEX.md | W1211 | CI 修复与机制补强  apt 源回退 + 第 71 槽接 ci_sim |
| docs/agent/pitfalls.md | W1211 | CI 修复与机制补强  apt 源回退 + 第 71 槽接 ci_sim |
| pitfalls.md | W1211 | CI 修复与机制补强  apt 源回退 + 第 71 槽接 ci_sim |
| pytest.ini | W1211 | CI 修复与机制补强  apt 源回退 + 第 71 槽接 ci_sim |
| scripts/INDEX.md | W1211 | CI 修复与机制补强  apt 源回退 + 第 71 槽接 ci_sim |
| scripts/ci_repair_apt_mirror.py | W1211 | CI 修复与机制补强  apt 源回退 + 第 71 槽接 ci_sim |
| scripts/ci_sim.py | W1211 | CI 修复与机制补强  apt 源回退 + 第 71 槽接 ci_sim |
| scripts/output/INDEX.md | W1211 | CI 修复与机制补强  apt 源回退 + 第 71 槽接 ci_sim |
| scripts/output/README.md | W1211 | CI 修复与机制补强  apt 源回退 + 第 71 槽接 ci_sim |
| scripts/output/_cascade_files_W1211.txt | W1211 | CI 修复与机制补强  apt 源回退 + 第 71 槽接 ci_sim |
| scripts/output/_w1211_spec.json | W1211 | CI 修复与机制补强  apt 源回退 + 第 71 槽接 ci_sim |
| scripts/output/file-index.md | W1211 | CI 修复与机制补强  apt 源回退 + 第 71 槽接 ci_sim |
| scripts/output/stats-changelog.json | W1211 | CI 修复与机制补强  apt 源回退 + 第 71 槽接 ci_sim |
| scripts/output/stats-index.md | W1211 | CI 修复与机制补强  apt 源回退 + 第 71 槽接 ci_sim |
| scripts/output/stats.json | W1211 | CI 修复与机制补强  apt 源回退 + 第 71 槽接 ci_sim |
| scripts/output/tools-inventory.md | W1211 | CI 修复与机制补强  apt 源回退 + 第 71 槽接 ci_sim |
| scripts/preflight_check.py | W1211 | CI 修复与机制补强  apt 源回退 + 第 71 槽接 ci_sim |
| site/data/cross-time-danmaku.html | W1211 | CI 修复与机制补强  apt 源回退 + 第 71 槽接 ci_sim |
| site/data/search.html | W1211 | CI 修复与机制补强  apt 源回退 + 第 71 槽接 ci_sim |
| site/data/tag-cloud.html | W1211 | CI 修复与机制补强  apt 源回退 + 第 71 槽接 ci_sim |
| site/dukou-engine.html | W1211 | CI 修复与机制补强  apt 源回退 + 第 71 槽接 ci_sim |
| site/en/search.html | W1211 | CI 修复与机制补强  apt 源回退 + 第 71 槽接 ci_sim |
| site/index.html | W1211 | CI 修复与机制补强  apt 源回退 + 第 71 槽接 ci_sim |
| tests/unit/INDEX.md | W1211 | CI 修复与机制补强  apt 源回退 + 第 71 槽接 ci_sim |
| tests/unit/README.md | W1211 | CI 修复与机制补强  apt 源回退 + 第 71 槽接 ci_sim |
| tests/unit/test_ci_repair_apt_mirror.py | W1211 | CI 修复与机制补强  apt 源回退 + 第 71 槽接 ci_sim |
| tests/unit/test_preflight_check.py | W1211 | CI 修复与机制补强  apt 源回退 + 第 71 槽接 ci_sim |

## W1210 占位符哈希载体常驻门禁批：第 71 槽挂载 + 存量 N2 解析器假红根修（2026-11-11）

| 文件 | W | 说明 |
|---|---|---|
| .github/workflows/README.md | W1210 | 改：占位符哈希载体门禁挂槽  第 71 槽 |
| AGENTS.md | W1210 | 改：占位符哈希载体门禁挂槽  第 71 槽 |
| CHANGELOG.md | W1210 | 改：占位符哈希载体门禁挂槽  第 71 槽 |
| CITATION.cff | W1210 | 改：占位符哈希载体门禁挂槽  第 71 槽 |
| HANDOVER.md | W1210 | 改：占位符哈希载体门禁挂槽  第 71 槽 |
| README.md | W1210 | 改：占位符哈希载体门禁挂槽  第 71 槽 |
| STRUCTURE.md | W1210 | 改：占位符哈希载体门禁挂槽  第 71 槽 |
| archive/docs/AGENTS-ARCHIVE.md | W1210 | 改：占位符哈希载体门禁挂槽  第 71 槽 |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1210 | 改：占位符哈希载体门禁挂槽  第 71 槽 |
| archive/docs/workflows-readme-history.md | W1210 | 改：占位符哈希载体门禁挂槽  第 71 槽 |
| docs/00-导读/W批次编号对账表.md | W1210 | 改：占位符哈希载体门禁挂槽  第 71 槽 |
| docs/00-导读/文档规范.md | W1210 | 改：占位符哈希载体门禁挂槽  第 71 槽 |
| docs/00-导读/项目说明.md | W1210 | 改：占位符哈希载体门禁挂槽  第 71 槽 |
| docs/11-方案报告/README.md | W1210 | 改：占位符哈希载体门禁挂槽  第 71 槽 |
| docs/11-方案报告/计划方案/T100-任务计划执行与经验沉淀报告-2026-11-11.md | W1210 | 改：占位符哈希载体门禁挂槽  第 71 槽 |
| docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md | W1210 | 改：占位符哈希载体门禁挂槽  第 71 槽 |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1210 | 改：占位符哈希载体门禁挂槽  第 71 槽 |
| docs/INDEX.md | W1210 | 改：占位符哈希载体门禁挂槽  第 71 槽 |
| docs/agent/gates.md | W1210 | 改：占位符哈希载体门禁挂槽  第 71 槽 |
| pytest.ini | W1210 | 改：占位符哈希载体门禁挂槽  第 71 槽 |
| scripts/INDEX.md | W1210 | 改：占位符哈希载体门禁挂槽  第 71 槽 |
| scripts/check_gov_doc_claims.py | W1210 | 改：占位符哈希载体门禁挂槽  第 71 槽 |
| scripts/check_placeholder_hash_carrier.py | W1210 | 改：占位符哈希载体门禁挂槽  第 71 槽 |
| scripts/output/INDEX.md | W1210 | 改：占位符哈希载体门禁挂槽  第 71 槽 |
| scripts/output/README.md | W1210 | 改：占位符哈希载体门禁挂槽  第 71 槽 |
| scripts/output/_cascade_files_W1210.txt | W1210 | 改：占位符哈希载体门禁挂槽  第 71 槽 |
| scripts/output/_vermilion_solid_cache.json | W1210 | 改：占位符哈希载体门禁挂槽  第 71 槽 |
| scripts/output/_w1210_spec.json | W1210 | 改：占位符哈希载体门禁挂槽  第 71 槽 |
| scripts/output/file-index.md | W1210 | 改：占位符哈希载体门禁挂槽  第 71 槽 |
| scripts/output/stats-changelog.json | W1210 | 改：占位符哈希载体门禁挂槽  第 71 槽 |
| scripts/output/stats-index.md | W1210 | 改：占位符哈希载体门禁挂槽  第 71 槽 |
| scripts/output/stats.json | W1210 | 改：占位符哈希载体门禁挂槽  第 71 槽 |
| scripts/output/tools-inventory.md | W1210 | 改：占位符哈希载体门禁挂槽  第 71 槽 |
| scripts/verify_delivery.py | W1210 | 改：占位符哈希载体门禁挂槽  第 71 槽 |
| site/data/cross-time-danmaku.html | W1210 | 改：占位符哈希载体门禁挂槽  第 71 槽 |
| site/data/search.html | W1210 | 改：占位符哈希载体门禁挂槽  第 71 槽 |
| site/data/tag-cloud.html | W1210 | 改：占位符哈希载体门禁挂槽  第 71 槽 |
| site/dukou-engine.html | W1210 | 改：占位符哈希载体门禁挂槽  第 71 槽 |
| site/en/search.html | W1210 | 改：占位符哈希载体门禁挂槽  第 71 槽 |
| site/index.html | W1210 | 改：占位符哈希载体门禁挂槽  第 71 槽 |
| tests/unit/INDEX.md | W1210 | 改：占位符哈希载体门禁挂槽  第 71 槽 |
| tests/unit/README.md | W1210 | 改：占位符哈希载体门禁挂槽  第 71 槽 |
| tests/unit/test_check_placeholder_hash_carrier.py | W1210 | 改：占位符哈希载体门禁挂槽  第 71 槽 |

## W1209 仓库体积治理批：历史改写 + LFS 迁移 + commit hash 回填（2026-11-11）

| 文件 | W | 说明 |
|---|---|---|
| .agent/skills/puti-shouye/SKILL.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| .gitattributes | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| .github/workflows/README.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| AGENTS.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| CHANGELOG.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| CITATION.cff | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| HANDOVER.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| README.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| STRUCTURE.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| assets/design/process/RECEIPT-W855.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/00-导读/W批次编号对账表.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/00-导读/文档规范.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/00-导读/统计口径说明.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/00-导读/项目说明.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/02-人物深度分析/菩提祖师-方向二深化.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/02-人物深度分析/金角银角-方向二深化.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/02-人物深度分析/高翠兰-方向二深化.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/02-人物深度分析/黑熊精-方向二深化.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/README.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/审查与评审/全仓逐逻辑深度审计报告-2026-11-06.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/审查与评审/全量对抗审查报告-2026-10-16.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/审查与评审/基础设施口径与门禁全量审计报告-2026-11-06.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/审查与评审/对抗审查报告-2026-11-06.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/审查与评审/对抗性审查报告-2026-10-14.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/审查与评审/工具脚本门禁体检与临时归档审计-2026-10-29.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/审查与评审/工程基础设施薄弱点审计报告-2026-10-16.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/审查与评审/站点交互流程审查第二轮复核报告-2026-10-31.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/审查与评审/站点交互流程审查第四轮复核报告-2026-11-05.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/审查与评审/计划方案三性审查报告-2026-10-20.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/审查与评审/设计文件审查报告-2026-11-02.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/工作复盘与优化分析报告/工作复盘与优化分析报告-2026-10-07-治理与引擎.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/工作复盘与优化分析报告/工作复盘与优化分析报告-2026-10-07.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/工作复盘与优化分析报告/工作复盘与优化分析报告-2026-10-10-2.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/工作复盘与优化分析报告/工作复盘与优化分析报告-2026-10-10-3.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/工作复盘与优化分析报告/工作复盘与优化分析报告-2026-10-10.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/工作复盘与优化分析报告/工作复盘与优化分析报告-2026-10-11.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/工作复盘与优化分析报告/工作复盘与优化分析报告-2026-10-12.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/工作复盘与优化分析报告/工作复盘与优化分析报告-2026-10-13.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/工作复盘与优化分析报告/工作复盘与优化分析报告-2026-10-14.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/工作复盘与优化分析报告/工作复盘与优化分析报告-2026-10-15.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/工作复盘与优化分析报告/工作复盘与优化分析报告-2026-10-17.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/工作复盘与优化分析报告/工作复盘与优化分析报告-2026-10-19.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/工作复盘与优化分析报告/工作复盘与优化分析报告-2026-10-30.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/工作复盘与优化分析报告/工作复盘与优化分析报告-2026-10-31.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/工作复盘与优化分析报告/工作复盘与优化分析报告-2026-11-07.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/治理与核查/W761工具链可维护性重构报告-2026-10-16.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/治理与核查/全仓待办计划方案状态核查报告-2026-10-18.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/治理与核查/多Agent干扰治理评估与实施记录-2026-10-14.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/计划方案/T01-任务计划执行与经验沉淀报告-2026-10-14.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/计划方案/T03-任务计划执行与经验沉淀报告-2026-10-20.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/计划方案/T06-任务计划执行与经验沉淀报告-2026-10-22.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/计划方案/T07-任务计划执行与经验沉淀报告-2026-10-21.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/计划方案/T09-任务计划执行与经验沉淀报告-2026-10-22.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/计划方案/T10-任务计划执行与经验沉淀报告-2026-10-22.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/计划方案/T11-任务计划执行与经验沉淀报告-2026-10-22.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/计划方案/T12-任务计划执行与经验沉淀报告-2026-10-23.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/计划方案/T13-任务计划执行与经验沉淀报告-2026-10-23.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/计划方案/T14-任务计划执行与经验沉淀报告-2026-10-23.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/计划方案/T15-任务计划执行与经验沉淀报告-2026-10-23.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/计划方案/T16-任务计划执行与经验沉淀报告-2026-10-23.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/计划方案/T17-任务计划执行与经验沉淀报告-2026-10-23.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/计划方案/T23-任务计划执行与经验沉淀报告-2026-10-25.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/计划方案/T26-任务计划执行与经验沉淀报告-2026-10-25.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/计划方案/T27-任务计划执行与经验沉淀报告-2026-10-26.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/计划方案/T28-任务计划执行与经验沉淀报告-2026-10-26.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/计划方案/T30-任务计划执行与经验沉淀报告-2026-10-27.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/计划方案/T31-任务计划执行与经验沉淀报告-2026-10-27.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/计划方案/T32-任务计划执行与经验沉淀报告-2026-10-27.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/计划方案/T34-任务计划执行与经验沉淀报告-2026-10-27.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/计划方案/T35-任务计划执行与经验沉淀报告-2026-10-28.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/计划方案/T36-任务计划执行与经验沉淀报告-2026-10-29.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/计划方案/T37-任务计划执行与经验沉淀报告-2026-10-29.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/计划方案/T38-任务计划执行与经验沉淀报告-2026-10-29.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/计划方案/T40-任务计划执行与经验沉淀报告-2026-10-31.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/计划方案/T41-任务计划执行与经验沉淀报告-2026-11-01.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/计划方案/T42-任务计划执行与经验沉淀报告-2026-11-02.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/计划方案/T43-任务计划执行与经验沉淀报告-2026-11-02.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/计划方案/T44-任务计划执行与经验沉淀报告-2026-11-02.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/计划方案/T45-任务计划执行与经验沉淀报告-2026-11-02.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/计划方案/T46-任务计划执行与经验沉淀报告-2026-11-02.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/计划方案/T47-任务计划执行与经验沉淀报告-2026-11-02.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/计划方案/T48-任务计划执行与经验沉淀报告-2026-11-02.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/计划方案/T49-任务计划执行与经验沉淀报告-2026-11-02.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/计划方案/T50-任务计划执行与经验沉淀报告-2026-11-02.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/计划方案/T51-任务计划执行与经验沉淀报告-2026-11-02.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/计划方案/T52-任务计划执行与经验沉淀报告-2026-11-02.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/计划方案/T53-任务计划执行与经验沉淀报告-2026-11-02.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/计划方案/T54-任务计划执行与经验沉淀报告-2026-11-02.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/计划方案/T55-任务计划执行与经验沉淀报告-2026-11-02.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/计划方案/T56-任务计划执行与经验沉淀报告-2026-11-02.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/计划方案/T57-任务计划执行与经验沉淀报告-2026-11-02.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/计划方案/T59-任务计划执行与经验沉淀报告-2026-11-03.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/计划方案/T60-任务计划执行与经验沉淀报告-2026-11-03.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/计划方案/T61-任务计划执行与经验沉淀报告-2026-11-03.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/计划方案/T62-任务计划执行与经验沉淀报告-2026-11-03.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/计划方案/T63-任务计划执行与经验沉淀报告-2026-11-03.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/计划方案/T66-任务计划执行与经验沉淀报告-2026-11-03.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/计划方案/T68-任务计划执行与经验沉淀报告-2026-11-04.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/计划方案/T71-任务计划执行与经验沉淀报告-2026-11-04.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/计划方案/T72-任务计划执行与经验沉淀报告-2026-11-04.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/计划方案/T74-任务计划执行与经验沉淀报告-2026-11-04.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/计划方案/T75-任务计划执行与经验沉淀报告-2026-11-04.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/计划方案/T79-任务计划执行与经验沉淀报告-2026-11-04.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/计划方案/T80-任务计划执行与经验沉淀报告-2026-11-04.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/计划方案/T81-任务计划执行与经验沉淀报告-2026-11-04.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/计划方案/T84-任务计划执行与经验沉淀报告-2026-11-04.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/计划方案/T86-任务计划执行与经验沉淀报告-2026-11-04.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/计划方案/T87-任务计划执行与经验沉淀报告-2026-11-05.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/计划方案/T88-任务计划执行与经验沉淀报告-2026-11-04.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/计划方案/T89-任务计划执行与经验沉淀报告-2026-11-04.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/计划方案/T90-任务计划执行与经验沉淀报告-2026-11-04.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/计划方案/T91-任务计划执行与经验沉淀报告-2026-11-09.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/计划方案/T92-任务计划执行与经验沉淀报告-2026-11-09.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/计划方案/T93-任务计划执行与经验沉淀报告-2026-11-09.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/计划方案/T94-任务计划执行与经验沉淀报告-2026-11-09.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/计划方案/T95-任务计划执行与经验沉淀报告-2026-11-09.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/计划方案/T96-任务计划执行与经验沉淀报告-2026-11-10.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/计划方案/T97-任务计划执行与经验沉淀报告-2026-11-11.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/计划方案/T99-任务计划执行与经验沉淀报告-2026-11-11.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/计划方案/执行前计划-T01.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/计划方案/执行前计划-T02-工程基础设施薄弱点修复.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/计划方案/执行前计划-T03-全项目审查第一批修复.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/计划方案/执行前计划-T04-站内阅读入口打通与阅读页体验封装.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/计划方案/执行前计划-T18-站内交互债整包.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/计划方案/执行前计划-T30-内页题图成套批第四组.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/计划方案/执行前计划-W1040-任务分级协议入库.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/agent-guardrails/merge-patch.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/agent/gates.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/agent/pitfalls.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/superpowers/plans/2026-09-21-demand-side-optimization-master-plan.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/superpowers/plans/2026-10-02-product-design-suite-applicability-plan.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/superpowers/plans/2026-10-11-agents-layered-restructure.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/superpowers/plans/2026-10-11-version-space-inventory.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| docs/superpowers/plans/2026-10-14-interference-governance-roadmap.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| pitfalls.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| scripts/INDEX.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| scripts/output/INDEX.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| scripts/output/README.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| scripts/output/_cascade_files_W1209.txt | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| scripts/output/_w1018_spec.json | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| scripts/output/_w1030_spec.json | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| scripts/output/_w1057_spec.json | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| scripts/output/_w1062_spec.json | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| scripts/output/_w1090_spec.json | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| scripts/output/_w1120_spec.json | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| scripts/output/_w1125_spec.json | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| scripts/output/_w1127_spec.json | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| scripts/output/_w1130_spec.json | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| scripts/output/_w1133_spec.json | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| scripts/output/_w1135_spec.json | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| scripts/output/_w1144_spec.json | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| scripts/output/_w1151_spec.json | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| scripts/output/_w1158_spec.json | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| scripts/output/_w1166_spec.json | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| scripts/output/_w1167_spec.json | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| scripts/output/_w1190_spec.json | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| scripts/output/_w1192_spec.json | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| scripts/output/_w1195_spec.json | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| scripts/output/_w1199_spec.json | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| scripts/output/_w1201_spec.json | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| scripts/output/_w1202_spec.json | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| scripts/output/_w1203_spec.json | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| scripts/output/_w1205_capacity_audit.json | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| scripts/output/_w1205_scorecard_alerts.json | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| scripts/output/_w1207_spec.json | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| scripts/output/_w761_spec.json | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| scripts/output/_w816_spec.json | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| scripts/output/_w827_spec.json | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| scripts/output/_w830_spec.json | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| scripts/output/_w877_spec.json | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| scripts/output/_w884_spec.json | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| scripts/output/_w893_spec.json | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| scripts/output/_w899_spec.json | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| scripts/output/_w905_spec.json | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| scripts/output/_w912_spec.json | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| scripts/output/_w954_review_evidence.json | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| scripts/output/_w976_spec.json | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| scripts/output/_w985_spec.json | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| scripts/output/_w986_spec.json | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| scripts/output/_w988_match.json | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| scripts/output/_w993_spec.json | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| scripts/output/_w995_spec.json | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| scripts/output/_w996_spec.json | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| scripts/output/file-index.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| scripts/output/stats-changelog.json | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| scripts/output/stats-index.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| scripts/output/stats.json | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| scripts/output/tools-inventory.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| scripts/rag/README.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| tests/unit/INDEX.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |
| tests/unit/README.md | W1209 | 改：仓库体积治理  历史改写+LFS 迁移  hash 回填 |

## W1208 C-8 守卫接入提交门禁批：第 70 槽挂载 + 注册表与槽数声明面同改（2026-11-11）

| 文件 | W | 说明 |
|---|---|---|
| .github/workflows/README.md | W1208 | 改：C-8 守卫接入提交门禁  第 70 槽 |
| AGENTS.md | W1208 | 改：C-8 守卫接入提交门禁  第 70 槽 |
| CHANGELOG.md | W1208 | 改：C-8 守卫接入提交门禁  第 70 槽 |
| CITATION.cff | W1208 | 改：C-8 守卫接入提交门禁  第 70 槽 |
| HANDOVER.md | W1208 | 改：C-8 守卫接入提交门禁  第 70 槽 |
| README.md | W1208 | 改：C-8 守卫接入提交门禁  第 70 槽 |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1208 | 改：C-8 守卫接入提交门禁  第 70 槽 |
| docs/00-导读/W批次编号对账表.md | W1208 | 改：C-8 守卫接入提交门禁  第 70 槽 |
| docs/00-导读/项目说明.md | W1208 | 改：C-8 守卫接入提交门禁  第 70 槽 |
| docs/11-方案报告/README.md | W1208 | 改：C-8 守卫接入提交门禁  第 70 槽 |
| docs/11-方案报告/计划方案/T98-任务计划执行与经验沉淀报告-2026-11-11.md | W1208 | 改：C-8 守卫接入提交门禁  第 70 槽 |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1208 | 改：C-8 守卫接入提交门禁  第 70 槽 |
| docs/agent/gates.md | W1208 | 改：C-8 守卫接入提交门禁  第 70 槽 |
| scripts/INDEX.md | W1208 | 改：C-8 守卫接入提交门禁  第 70 槽 |
| scripts/check_no_hardcoded_endpoint.py | W1208 | 改：C-8 守卫接入提交门禁  第 70 槽 |
| scripts/output/INDEX.md | W1208 | 改：C-8 守卫接入提交门禁  第 70 槽 |
| scripts/output/README.md | W1208 | 改：C-8 守卫接入提交门禁  第 70 槽 |
| scripts/output/_cascade_files_W1208.txt | W1208 | 改：C-8 守卫接入提交门禁  第 70 槽 |
| scripts/output/_w1208_spec.json | W1208 | 改：C-8 守卫接入提交门禁  第 70 槽 |
| scripts/output/file-index.md | W1208 | 改：C-8 守卫接入提交门禁  第 70 槽 |
| scripts/output/stats-changelog.json | W1208 | 改：C-8 守卫接入提交门禁  第 70 槽 |
| scripts/output/stats-index.md | W1208 | 改：C-8 守卫接入提交门禁  第 70 槽 |
| scripts/output/stats.json | W1208 | 改：C-8 守卫接入提交门禁  第 70 槽 |
| scripts/output/tools-inventory.md | W1208 | 改：C-8 守卫接入提交门禁  第 70 槽 |
| scripts/verify_delivery.py | W1208 | 改：C-8 守卫接入提交门禁  第 70 槽 |
| tests/unit/INDEX.md | W1208 | 改：C-8 守卫接入提交门禁  第 70 槽 |
| tests/unit/README.md | W1208 | 改：C-8 守卫接入提交门禁  第 70 槽 |

## W1207 C-8 全量占位符化 + 仓库体积处置 + 就绪探针暴露审计降级批（2026-11-11）

| 文件 | W | 说明 |
|---|---|---|
| .agent/skills/puti-shouye/SKILL.md | W1207 | 改：C-8 占位符化  仓库体积 1844→1201 MB  就绪探针暴露审计降级 |
| .github/workflows/README.md | W1207 | 改：C-8 占位符化  仓库体积 1844→1201 MB  就绪探针暴露审计降级 |
| AGENTS.md | W1207 | 改：C-8 占位符化  仓库体积 1844→1201 MB  就绪探针暴露审计降级 |
| CHANGELOG.md | W1207 | 改：C-8 占位符化  仓库体积 1844→1201 MB  就绪探针暴露审计降级 |
| CITATION.cff | W1207 | 改：C-8 占位符化  仓库体积 1844→1201 MB  就绪探针暴露审计降级 |
| HANDOVER.md | W1207 | 改：C-8 占位符化  仓库体积 1844→1201 MB  就绪探针暴露审计降级 |
| README.md | W1207 | 改：C-8 占位符化  仓库体积 1844→1201 MB  就绪探针暴露审计降级 |
| STRUCTURE.md | W1207 | 改：C-8 占位符化  仓库体积 1844→1201 MB  就绪探针暴露审计降级 |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1207 | 改：C-8 占位符化  仓库体积 1844→1201 MB  就绪探针暴露审计降级 |
| docs/00-导读/W批次编号对账表.md | W1207 | 改：C-8 占位符化  仓库体积 1844→1201 MB  就绪探针暴露审计降级 |
| docs/00-导读/项目说明.md | W1207 | 改：C-8 占位符化  仓库体积 1844→1201 MB  就绪探针暴露审计降级 |
| docs/11-方案报告/README.md | W1207 | 改：C-8 占位符化  仓库体积 1844→1201 MB  就绪探针暴露审计降级 |
| docs/11-方案报告/计划方案/T97-任务计划执行与经验沉淀报告-2026-11-11.md | W1207 | 改：C-8 占位符化  仓库体积 1844→1201 MB  就绪探针暴露审计降级 |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1207 | 改：C-8 占位符化  仓库体积 1844→1201 MB  就绪探针暴露审计降级 |
| docs/agent/pitfalls.md | W1207 | 改：C-8 占位符化  仓库体积 1844→1201 MB  就绪探针暴露审计降级 |
| pitfalls.md | W1207 | 改：C-8 占位符化  仓库体积 1844→1201 MB  就绪探针暴露审计降级 |
| scripts/INDEX.md | W1207 | 改：C-8 占位符化  仓库体积 1844→1201 MB  就绪探针暴露审计降级 |
| scripts/generate_csp.py | W1207 | 改：C-8 占位符化  仓库体积 1844→1201 MB  就绪探针暴露审计降级 |
| scripts/inject_service_endpoint.py | W1207 | 改：C-8 占位符化  仓库体积 1844→1201 MB  就绪探针暴露审计降级 |
| scripts/output/INDEX.md | W1207 | 改：C-8 占位符化  仓库体积 1844→1201 MB  就绪探针暴露审计降级 |
| scripts/output/README.md | W1207 | 改：C-8 占位符化  仓库体积 1844→1201 MB  就绪探针暴露审计降级 |
| scripts/output/_cascade_files_W1207.txt | W1207 | 改：C-8 占位符化  仓库体积 1844→1201 MB  就绪探针暴露审计降级 |
| scripts/output/_w1207_spec.json | W1207 | 改：C-8 占位符化  仓库体积 1844→1201 MB  就绪探针暴露审计降级 |
| scripts/output/file-index.md | W1207 | 改：C-8 占位符化  仓库体积 1844→1201 MB  就绪探针暴露审计降级 |
| scripts/output/stats-changelog.json | W1207 | 改：C-8 占位符化  仓库体积 1844→1201 MB  就绪探针暴露审计降级 |
| scripts/output/stats-index.md | W1207 | 改：C-8 占位符化  仓库体积 1844→1201 MB  就绪探针暴露审计降级 |
| scripts/output/stats.json | W1207 | 改：C-8 占位符化  仓库体积 1844→1201 MB  就绪探针暴露审计降级 |
| scripts/output/tools-inventory.md | W1207 | 改：C-8 占位符化  仓库体积 1844→1201 MB  就绪探针暴露审计降级 |
| scripts/rag/README.md | W1207 | 改：C-8 占位符化  仓库体积 1844→1201 MB  就绪探针暴露审计降级 |
| site/_headers | W1207 | 改：C-8 占位符化  仓库体积 1844→1201 MB  就绪探针暴露审计降级 |
| site/dashboard.html | W1207 | 改：C-8 占位符化  仓库体积 1844→1201 MB  就绪探针暴露审计降级 |
| site/data/81-hardships-view.html | W1207 | 改：C-8 占位符化  仓库体积 1844→1201 MB  就绪探针暴露审计降级 |
| site/data/cave-estate.html | W1207 | 改：C-8 占位符化  仓库体积 1844→1201 MB  就绪探针暴露审计降级 |
| site/data/character-relationship-3d-view.html | W1207 | 改：C-8 占位符化  仓库体积 1844→1201 MB  就绪探针暴露审计降级 |
| site/data/data-explorer.html | W1207 | 改：C-8 占位符化  仓库体积 1844→1201 MB  就绪探针暴露审计降级 |
| site/data/material-archaeology.html | W1207 | 改：C-8 占位符化  仓库体积 1844→1201 MB  就绪探针暴露审计降级 |
| site/dukou-engine.html | W1207 | 改：C-8 占位符化  仓库体积 1844→1201 MB  就绪探针暴露审计降级 |
| site/en/81-hardships-view.html | W1207 | 改：C-8 占位符化  仓库体积 1844→1201 MB  就绪探针暴露审计降级 |
| site/en/cave-estate.html | W1207 | 改：C-8 占位符化  仓库体积 1844→1201 MB  就绪探针暴露审计降级 |
| site/en/character-relationship-3d-view.html | W1207 | 改：C-8 占位符化  仓库体积 1844→1201 MB  就绪探针暴露审计降级 |
| site/en/data-explorer.html | W1207 | 改：C-8 占位符化  仓库体积 1844→1201 MB  就绪探针暴露审计降级 |
| site/en/dukou-engine.html | W1207 | 改：C-8 占位符化  仓库体积 1844→1201 MB  就绪探针暴露审计降级 |
| site/en/material-archaeology.html | W1207 | 改：C-8 占位符化  仓库体积 1844→1201 MB  就绪探针暴露审计降级 |
| site/index.html | W1207 | 改：C-8 占位符化  仓库体积 1844→1201 MB  就绪探针暴露审计降级 |
| site/static/js/dataset-view.js | W1207 | 改：C-8 占位符化  仓库体积 1844→1201 MB  就绪探针暴露审计降级 |
| site/static/js/rag-chat.js | W1207 | 改：C-8 占位符化  仓库体积 1844→1201 MB  就绪探针暴露审计降级 |
| tests/unit/INDEX.md | W1207 | 改：C-8 占位符化  仓库体积 1844→1201 MB  就绪探针暴露审计降级 |
| tests/unit/README.md | W1207 | 改：C-8 占位符化  仓库体积 1844→1201 MB  就绪探针暴露审计降级 |
| tests/unit/test_w1205_batch_scripts.py | W1207 | 改：C-8 占位符化  仓库体积 1844→1201 MB  就绪探针暴露审计降级 |
| xiyouji-agent-web/server/api.integration.test.ts | W1207 | 改：C-8 占位符化  仓库体积 1844→1201 MB  就绪探针暴露审计降级 |
| xiyouji-agent-web/server/audit.ts | W1207 | 改：C-8 占位符化  仓库体积 1844→1201 MB  就绪探针暴露审计降级 |
| xiyouji-agent-web/server/routes.ts | W1207 | 改：C-8 占位符化  仓库体积 1844→1201 MB  就绪探针暴露审计降级 |
| xiyouji-agent-web/src/utils/apiTypes.ts | W1207 | 改：C-8 占位符化  仓库体积 1844→1201 MB  就绪探针暴露审计降级 |

## W1206 公开仓敏感面清理批：本机绝对路径脱敏 + 可复跑扫描防线（2026-11-11）

| 文件 | W | 说明 |
|---|---|---|
| .agent/skills/puti-shouye/SKILL.md | W1206 | 改：本批公开面清理（本机绝对路径脱敏） |
| .github/workflows/README.md | W1206 | 改：本批公开面清理（本机绝对路径脱敏） |
| .gitignore | W1206 | 改：本批公开面清理（本机绝对路径脱敏） |
| AGENTS.md | W1206 | 改：本批公开面清理（本机绝对路径脱敏） |
| CHANGELOG.md | W1206 | 改：本批公开面清理（本机绝对路径脱敏） |
| CITATION.cff | W1206 | 改：本批公开面清理（本机绝对路径脱敏） |
| HANDOVER.md | W1206 | 改：本批公开面清理（本机绝对路径脱敏） |
| README.md | W1206 | 改：本批公开面清理（本机绝对路径脱敏） |
| STRUCTURE.md | W1206 | 改：本批公开面清理（本机绝对路径脱敏） |
| archive/docs/AGENTS-ARCHIVE.md | W1206 | 改：本批公开面清理（本机绝对路径脱敏） |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1206 | 改：本批公开面清理（本机绝对路径脱敏） |
| archive/docs/workflows-readme-history.md | W1206 | 改：本批公开面清理（本机绝对路径脱敏） |
| docs/00-导读/W批次编号对账表.md | W1206 | 改：本批公开面清理（本机绝对路径脱敏） |
| docs/00-导读/项目说明.md | W1206 | 改：本批公开面清理（本机绝对路径脱敏） |
| docs/10-方法论沉淀/DRL真循环.md | W1206 | 改：本批公开面清理（本机绝对路径脱敏） |
| docs/10-方法论沉淀/E1铁律.md | W1206 | 改：本批公开面清理（本机绝对路径脱敏） |
| docs/10-方法论沉淀/Preflight与Subagent模板.md | W1206 | 改：本批公开面清理（本机绝对路径脱敏） |
| docs/10-方法论沉淀/README.md | W1206 | 改：本批公开面清理（本机绝对路径脱敏） |
| docs/10-方法论沉淀/Subagent盲信铁律.md | W1206 | 改：本批公开面清理（本机绝对路径脱敏） |
| docs/10-方法论沉淀/markdown写作规范.md | W1206 | 改：本批公开面清理（本机绝对路径脱敏） |
| docs/10-方法论沉淀/三skill闭环.md | W1206 | 改：本批公开面清理（本机绝对路径脱敏） |
| docs/11-方案报告/计划方案/T09-任务计划执行与经验沉淀报告-2026-10-22.md | W1206 | 改：本批公开面清理（本机绝对路径脱敏） |
| docs/11-方案报告/计划方案/T41-任务计划执行与经验沉淀报告-2026-11-01.md | W1206 | 改：本批公开面清理（本机绝对路径脱敏） |
| docs/11-方案报告/计划方案/执行前计划-T05-取经编制表落库与编制位补全.md | W1206 | 改：本批公开面清理（本机绝对路径脱敏） |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1206 | 改：本批公开面清理（本机绝对路径脱敏） |
| docs/12-提示词库/00-总目录.md | W1206 | 改：本批公开面清理（本机绝对路径脱敏） |
| docs/12-提示词库/01-参考链接.md | W1206 | 改：本批公开面清理（本机绝对路径脱敏） |
| docs/12-提示词库/02-写作与输出规范.md | W1206 | 改：本批公开面清理（本机绝对路径脱敏） |
| docs/12-提示词库/03-工作复盘提示词.md | W1206 | 改：本批公开面清理（本机绝对路径脱敏） |
| docs/12-提示词库/04-任务执行提示词.md | W1206 | 改：本批公开面清理（本机绝对路径脱敏） |
| docs/12-提示词库/05-项目审查任务书.md | W1206 | 改：本批公开面清理（本机绝对路径脱敏） |
| docs/12-提示词库/06-隐私与开源边界.md | W1206 | 改：本批公开面清理（本机绝对路径脱敏） |
| docs/12-提示词库/07-安全架构准则.md | W1206 | 改：本批公开面清理（本机绝对路径脱敏） |
| docs/12-提示词库/08-团队角色分工.md | W1206 | 改：本批公开面清理（本机绝对路径脱敏） |
| docs/12-提示词库/09-导师提问流程.md | W1206 | 改：本批公开面清理（本机绝对路径脱敏） |
| docs/12-提示词库/10-创意写作题.md | W1206 | 改：本批公开面清理（本机绝对路径脱敏） |
| docs/12-提示词库/11-colors.md | W1206 | 改：本批公开面清理（本机绝对路径脱敏） |
| docs/agent/pitfalls.md | W1206 | 改：本批公开面清理（本机绝对路径脱敏） |
| pitfalls.md | W1206 | 改：本批公开面清理（本机绝对路径脱敏） |
| pytest.ini | W1206 | 改：本批公开面清理（本机绝对路径脱敏） |
| scripts/INDEX.md | W1206 | 改：本批公开面清理（本机绝对路径脱敏） |
| scripts/check_public_repo_secrets.py | W1206 | 改：本批公开面清理（本机绝对路径脱敏） |
| scripts/drl_contracts.yaml | W1206 | 改：本批公开面清理（本机绝对路径脱敏） |
| scripts/output/INDEX.md | W1206 | 改：本批公开面清理（本机绝对路径脱敏） |
| scripts/output/README.md | W1206 | 改：本批公开面清理（本机绝对路径脱敏） |
| scripts/output/_cascade_files_W1206.txt | W1206 | 改：本批公开面清理（本机绝对路径脱敏） |
| scripts/output/_vermilion_solid_cache.json | W1206 | 改：本批公开面清理（本机绝对路径脱敏） |
| scripts/output/_w1206_public_secrets.json | W1206 | 改：本批公开面清理（本机绝对路径脱敏） |
| scripts/output/_w1206_spec.json | W1206 | 改：本批公开面清理（本机绝对路径脱敏） |
| scripts/output/_w927_pg_runtime_evidence.txt | W1206 | 改：本批公开面清理（本机绝对路径脱敏） |
| scripts/output/file-index.md | W1206 | 改：本批公开面清理（本机绝对路径脱敏） |
| scripts/output/stats-changelog.json | W1206 | 改：本批公开面清理（本机绝对路径脱敏） |
| scripts/output/stats-index.md | W1206 | 改：本批公开面清理（本机绝对路径脱敏） |
| scripts/output/stats.json | W1206 | 改：本批公开面清理（本机绝对路径脱敏） |
| scripts/output/tools-inventory.md | W1206 | 改：本批公开面清理（本机绝对路径脱敏） |
| site/data/cross-time-danmaku.html | W1206 | 改：本批公开面清理（本机绝对路径脱敏） |
| site/data/search.html | W1206 | 改：本批公开面清理（本机绝对路径脱敏） |
| site/data/tag-cloud.html | W1206 | 改：本批公开面清理（本机绝对路径脱敏） |
| site/dukou-engine.html | W1206 | 改：本批公开面清理（本机绝对路径脱敏） |
| site/en/search.html | W1206 | 改：本批公开面清理（本机绝对路径脱敏） |
| site/index.html | W1206 | 改：本批公开面清理（本机绝对路径脱敏） |
| tests/unit/INDEX.md | W1206 | 改：本批公开面清理（本机绝对路径脱敏） |
| tests/unit/README.md | W1206 | 改：本批公开面清理（本机绝对路径脱敏） |
| tests/unit/test_check_public_repo_secrets.py | W1206 | 改：本批公开面清理（本机绝对路径脱敏） |

## W1205 档 2 收尾四件：面板归零 + 检索接入与地址注入 + 容量实测 + D-3 合规批（2026-11-11）

| 文件 | W | 说明 |
|---|---|---|
| .agent/skills/puti-shouye/SKILL.md | W1205 | mod:pitfall count declaration |
| .gitattributes | W1205 | mod:linguist-generated for site/** (Scorecard Fuzzing root cause) |
| .github/workflows/README.md | W1205 | mod:batch delivery (see CHANGELOG section + file-index) |
| AGENTS.md | W1205 | mod:rule pointer for E-221 + count chain |
| CHANGELOG.md | W1205 | mod:W1205 section |
| CITATION.cff | W1205 | mod:batch delivery (see CHANGELOG section + file-index) |
| HANDOVER.md | W1205 | mod:progress + methodology + count chain |
| README.md | W1205 | mod:batch delivery (see CHANGELOG section + file-index) |
| STRUCTURE.md | W1205 | mod:pitfall count declaration |
| archive/docs/AGENTS-ARCHIVE.md | W1205 | mod:batch delivery (see CHANGELOG section + file-index) |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1205 | mod:batch delivery (see CHANGELOG section + file-index) |
| archive/docs/workflows-readme-history.md | W1205 | mod:batch delivery (see CHANGELOG section + file-index) |
| docs/00-导读/W批次编号对账表.md | W1205 | mod:W1205 claim row |
| docs/00-导读/项目说明.md | W1205 | mod:batch delivery (see CHANGELOG section + file-index) |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1205 | mod:13.8 delivery section + 8.3 measured values + 3 threshold breaches |
| docs/agent/pitfalls.md | W1205 | mod:new E-222 / E-223 + count chain 315->317 |
| pitfalls.md | W1205 | mod:new E-222 / E-223 + count chain 315->317 |
| pytest.ini | W1205 | mod:batch delivery (see CHANGELOG section + file-index) |
| scripts/INDEX.md | W1205 | mod:batch delivery (see CHANGELOG section + file-index) |
| scripts/check_capacity_budget.py | W1205 | new:capacity threshold measurer (8.3 ten items) |
| scripts/check_no_hardcoded_endpoint.py | W1205 | new:C-8 guard (no hardcoded service address + negative self-test) |
| scripts/dismiss_scorecard_alerts.py | W1205 | new:code-scanning alert dismiss/revert script |
| scripts/gen_compliance_migration.mjs | W1205 | new:0003 migration generator (fact source + --check) |
| scripts/inject_service_endpoint.py | W1205 | new:deployment-time endpoint injection (two fail-closed profiles) |
| scripts/output/INDEX.md | W1205 | mod:batch delivery (see CHANGELOG section + file-index) |
| scripts/output/README.md | W1205 | mod:batch delivery (see CHANGELOG section + file-index) |
| scripts/output/_cascade_files_W1205.txt | W1205 | mod:batch delivery (see CHANGELOG section + file-index) |
| scripts/output/_vermilion_solid_cache.json | W1205 | mod:batch delivery (see CHANGELOG section + file-index) |
| scripts/output/_w1167_nav_plan.json | W1205 | mod:batch delivery (see CHANGELOG section + file-index) |
| scripts/output/_w1205_capacity_audit.json | W1205 | new:machine evidence for this batch |
| scripts/output/_w1205_compliance.json | W1205 | new:machine evidence for this batch |
| scripts/output/_w1205_retrieval_endpoint.json | W1205 | new:machine evidence for this batch |
| scripts/output/_w1205_scorecard_alerts.json | W1205 | new:machine evidence for this batch |
| scripts/output/_w1205_spec.json | W1205 | new:machine evidence for this batch |
| scripts/output/file-index.md | W1205 | mod:batch delivery (see CHANGELOG section + file-index) |
| scripts/output/stats-changelog.json | W1205 | mod:batch delivery (see CHANGELOG section + file-index) |
| scripts/output/stats-index.md | W1205 | mod:batch delivery (see CHANGELOG section + file-index) |
| scripts/output/stats.json | W1205 | mod:batch delivery (see CHANGELOG section + file-index) |
| scripts/output/tools-inventory.md | W1205 | mod:batch delivery (see CHANGELOG section + file-index) |
| scripts/rag/INDEX.md | W1205 | mod:batch delivery (see CHANGELOG section + file-index) |
| scripts/rag/retrieval_cli.py | W1205 | new:retrieval CLI entry |
| site/data/cross-time-danmaku.html | W1205 | mod:batch delivery (see CHANGELOG section + file-index) |
| site/data/search.html | W1205 | mod:batch delivery (see CHANGELOG section + file-index) |
| site/data/tag-cloud.html | W1205 | mod:batch delivery (see CHANGELOG section + file-index) |
| site/dukou-engine.html | W1205 | mod:batch delivery (see CHANGELOG section + file-index) |
| site/en/search.html | W1205 | mod:batch delivery (see CHANGELOG section + file-index) |
| site/index.html | W1205 | mod:batch delivery (see CHANGELOG section + file-index) |
| tests/unit/INDEX.md | W1205 | mod:batch delivery (see CHANGELOG section + file-index) |
| tests/unit/README.md | W1205 | mod:batch delivery (see CHANGELOG section + file-index) |
| tests/unit/test_check_no_hardcoded_endpoint.py | W1205 | new:regression tests for C-8 guard |
| tests/unit/test_dismiss_scorecard_alerts.py | W1205 | new:regression tests for dismiss script |
| tests/unit/test_w1205_batch_scripts.py | W1205 | mod:batch delivery (see CHANGELOG section + file-index) |
| xiyouji-agent-web/deploy/pg/migrations/0003_compliance_columns.sql | W1205 | new:compliance column migration (generated from schema fact source) |
| xiyouji-agent-web/deploy/pg/migrations/INDEX.md | W1205 | mod:batch delivery (see CHANGELOG section + file-index) |
| xiyouji-agent-web/deploy/pg/migrations/README.md | W1205 | mod:batch delivery (see CHANGELOG section + file-index) |
| xiyouji-agent-web/package.json | W1205 | mod:batch delivery (see CHANGELOG section + file-index) |
| xiyouji-agent-web/server/INDEX.md | W1205 | mod:batch delivery (see CHANGELOG section + file-index) |
| xiyouji-agent-web/server/README.md | W1205 | mod:batch delivery (see CHANGELOG section + file-index) |
| xiyouji-agent-web/server/audit.test.ts | W1205 | mod:structured audit events + F10 compliance degradation + purge evidence |
| xiyouji-agent-web/server/audit.ts | W1205 | mod:structured audit events + F10 compliance degradation + purge evidence |
| xiyouji-agent-web/server/chat.ts | W1205 | mod:grading tag on writes |
| xiyouji-agent-web/server/compliance/INDEX.md | W1205 | new:D-3 compliance (grading catalog / deploy baseline / retention / audit archive / error contract) |
| xiyouji-agent-web/server/compliance/README.md | W1205 | new:D-3 compliance (grading catalog / deploy baseline / retention / audit archive / error contract) |
| xiyouji-agent-web/server/compliance/audit-archive.test.ts | W1205 | new:D-3 compliance (grading catalog / deploy baseline / retention / audit archive / error contract) |
| xiyouji-agent-web/server/compliance/audit-archive.ts | W1205 | new:D-3 compliance (grading catalog / deploy baseline / retention / audit archive / error contract) |
| xiyouji-agent-web/server/compliance/audit-event.ts | W1205 | new:D-3 compliance (grading catalog / deploy baseline / retention / audit archive / error contract) |
| xiyouji-agent-web/server/compliance/baseline.example.json | W1205 | new:D-3 compliance (grading catalog / deploy baseline / retention / audit archive / error contract) |
| xiyouji-agent-web/server/compliance/baseline.ts | W1205 | new:D-3 compliance (grading catalog / deploy baseline / retention / audit archive / error contract) |
| xiyouji-agent-web/server/compliance/compliance.test.ts | W1205 | new:D-3 compliance (grading catalog / deploy baseline / retention / audit archive / error contract) |
| xiyouji-agent-web/server/compliance/data-class.ts | W1205 | new:D-3 compliance (grading catalog / deploy baseline / retention / audit archive / error contract) |
| xiyouji-agent-web/server/compliance/errors.ts | W1205 | new:D-3 compliance (grading catalog / deploy baseline / retention / audit archive / error contract) |
| xiyouji-agent-web/server/compliance/retention.ts | W1205 | new:D-3 compliance (grading catalog / deploy baseline / retention / audit archive / error contract) |
| xiyouji-agent-web/server/compliance/schema.ts | W1205 | new:D-3 compliance (grading catalog / deploy baseline / retention / audit archive / error contract) |
| xiyouji-agent-web/server/config.ts | W1205 | mod:compliance baseline self-check at startup |
| xiyouji-agent-web/server/index.ts | W1205 | mod:register retrieval routes |
| xiyouji-agent-web/server/retrieval.routes.ts | W1205 | new:retrieval layer wiring (O-4 / citation guard / degradation semantics) |
| xiyouji-agent-web/server/retrieval.test.ts | W1205 | new:retrieval layer wiring (O-4 / citation guard / degradation semantics) |
| xiyouji-agent-web/server/retrieval.ts | W1205 | new:retrieval layer wiring (O-4 / citation guard / degradation semantics) |
| xiyouji-agent-web/server/routes.ts | W1205 | mod:grading tag on writes + citation wiring |
| xiyouji-agent-web/server/storage/INDEX.md | W1205 | mod:storage contract + backends (C-6 grading tag / authoritative write time / encrypt-once) |
| xiyouji-agent-web/server/storage/README.md | W1205 | mod:storage contract + backends (C-6 grading tag / authoritative write time / encrypt-once) |
| xiyouji-agent-web/server/storage/dualwrite.test.ts | W1205 | mod:storage contract + backends (C-6 grading tag / authoritative write time / encrypt-once) |
| xiyouji-agent-web/server/storage/dualwrite.ts | W1205 | mod:storage contract + backends (C-6 grading tag / authoritative write time / encrypt-once) |
| xiyouji-agent-web/server/storage/encryption.test.ts | W1205 | new:column-level encryption (AES-256-GCM / AAD bound / idempotent) |
| xiyouji-agent-web/server/storage/encryption.ts | W1205 | new:column-level encryption (AES-256-GCM / AAD bound / idempotent) |
| xiyouji-agent-web/server/storage/postgres.ts | W1205 | mod:storage contract + backends (C-6 grading tag / authoritative write time / encrypt-once) |
| xiyouji-agent-web/server/storage/sqlite.ts | W1205 | mod:storage contract + backends (C-6 grading tag / authoritative write time / encrypt-once) |
| xiyouji-agent-web/server/storage/storage.test.ts | W1205 | mod:storage contract + backends (C-6 grading tag / authoritative write time / encrypt-once) |
| xiyouji-agent-web/server/storage/types.ts | W1205 | mod:storage contract + backends (C-6 grading tag / authoritative write time / encrypt-once) |

## W1204 v2 档 2 D-2 第二子批：双写期集合级三重对账器 + 切读/停写流程（2026-11-10）

| 文件 | W | 说明 |
|---|---|---|
| .agent/skills/puti-shouye/SKILL.md | W1204 | 改：本批级联/索引/统计产物刷新 |
| .github/workflows/README.md | W1204 | 改：本批级联/索引/统计产物刷新 |
| AGENTS.md | W1204 | 改：本批级联/索引/统计产物刷新 |
| CHANGELOG.md | W1204 | 立段：W1204 对账器与切读/停写流程 |
| CITATION.cff | W1204 | 改：本批级联/索引/统计产物刷新 |
| HANDOVER.md | W1204 | 改：本批级联/索引/统计产物刷新 |
| README.md | W1204 | 改：本批级联/索引/统计产物刷新 |
| STRUCTURE.md | W1204 | 改：本批级联/索引/统计产物刷新 |
| archive/docs/AGENTS-ARCHIVE.md | W1204 | 改：本批级联/索引/统计产物刷新 |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1204 | 改：台账行归档追加（腾窗迁出 W1140 僵尸预约占位行） |
| archive/docs/workflows-readme-history.md | W1204 | 改：本批级联/索引/统计产物刷新 |
| docs/00-导读/W批次编号对账表.md | W1204 | 登记：W1204 认领行 |
| docs/00-导读/项目说明.md | W1204 | 改：本批级联/索引/统计产物刷新 |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1204 | 改：§13.6 补记 D-2 第二子批交付与「真实 PG 实跑未做」 |
| docs/agent/pitfalls.md | W1204 | 改：本批级联/索引/统计产物刷新 |
| pitfalls.md | W1204 | 改：本批级联/索引/统计产物刷新 |
| scripts/archive_ledger_rows.py | W1204 | 改：真在途判定收敛为唯一实现（占位 touches 不算真在途）·补自测形态四 |
| scripts/output/INDEX.md | W1204 | 改：本批级联/索引/统计产物刷新 |
| scripts/output/README.md | W1204 | 改：本批级联/索引/统计产物刷新 |
| scripts/output/_cascade_files_W1204.txt | W1204 | 改：本批级联/索引/统计产物刷新 |
| scripts/output/_w1204_cutover_evidence.json | W1204 | 改：本批级联/索引/统计产物刷新 |
| scripts/output/_w1204_drill_dual.json | W1204 | 改：本批级联/索引/统计产物刷新 |
| scripts/output/_w1204_drill_dual_fixed.json | W1204 | 改：本批级联/索引/统计产物刷新 |
| scripts/output/_w1204_drill_redual.json | W1204 | 改：本批级联/索引/统计产物刷新 |
| scripts/output/_w1204_migrate_backfill.json | W1204 | 改：本批级联/索引/统计产物刷新 |
| scripts/output/_w1204_spec.json | W1204 | 新建：本批 spec |
| scripts/output/file-index.md | W1204 | 改：本批级联/索引/统计产物刷新 |
| scripts/output/stats.json | W1204 | 改：本批级联/索引/统计产物刷新 |
| scripts/output/tools-inventory.md | W1204 | 改：本批级联/索引/统计产物刷新 |
| site/data/cross-time-danmaku.html | W1204 | 改：本批级联/索引/统计产物刷新 |
| site/data/search.html | W1204 | 改：本批级联/索引/统计产物刷新 |
| site/data/tag-cloud.html | W1204 | 改：本批级联/索引/统计产物刷新 |
| site/dukou-engine.html | W1204 | 改：本批级联/索引/统计产物刷新 |
| site/en/search.html | W1204 | 改：本批级联/索引/统计产物刷新 |
| site/index.html | W1204 | 改：本批级联/索引/统计产物刷新 |
| xiyouji-agent-web/deploy/pg/README.md | W1204 | 改：补「切读 → 停写旧库」三步流程与回滚路径 |
| xiyouji-agent-web/deploy/pg/bin/INDEX.md | W1204 | 改：本批级联/索引/统计产物刷新 |
| xiyouji-agent-web/deploy/pg/bin/README.md | W1204 | 改：本批级联/索引/统计产物刷新 |
| xiyouji-agent-web/deploy/pg/bin/dualwrite-drill.ts | W1204 | 改：本批级联/索引/统计产物刷新 |
| xiyouji-agent-web/deploy/pg/bin/reconcile-dualwrite.test.ts | W1204 | 新建：对账器契约测试 4 例（含假对账被抓住） |
| xiyouji-agent-web/deploy/pg/bin/reconcile-dualwrite.ts | W1204 | 新建：双写期对账 CLI（SQLite×SQLite 与 SQLite×PG 两侧读适配） |
| xiyouji-agent-web/package.json | W1204 | 改：本批级联/索引/统计产物刷新 |
| xiyouji-agent-web/server/storage/INDEX.md | W1204 | 改：本批级联/索引/统计产物刷新 |
| xiyouji-agent-web/server/storage/README.md | W1204 | 改：本批级联/索引/统计产物刷新 |
| xiyouji-agent-web/server/storage/dualwrite.test.ts | W1204 | 改：本批级联/索引/统计产物刷新 |
| xiyouji-agent-web/server/storage/dualwrite.ts | W1204 | 改：本批级联/索引/统计产物刷新 |
| xiyouji-agent-web/server/storage/postgres.ts | W1204 | 改：本批级联/索引/统计产物刷新 |
| xiyouji-agent-web/server/storage/reconcile-core.ts | W1204 | 新建：对账判定核心（与数据源无关·三重对账·D-08 比集合不只比计数） |
| xiyouji-agent-web/server/storage/sqlite.ts | W1204 | 改：本批级联/索引/统计产物刷新 |
| xiyouji-agent-web/server/storage/storage.test.ts | W1204 | 改：本批级联/索引/统计产物刷新 |
| xiyouji-agent-web/server/storage/types.ts | W1204 | 改：本批级联/索引/统计产物刷新 |

## W1203 架构方案 v2 档 2 施工第二子批（2026-11-10）

| 文件 | W | 说明 |
|---|---|---|
| .github/workflows/README.md | W1203 | 改：本批级联/索引/统计产物刷新 |
| AGENTS.md | W1203 | 改：本批级联/索引/统计产物刷新 |
| CHANGELOG.md | W1203 | 立段：v2 档 2 施工第二子批 + W1202 终态收口 |
| CITATION.cff | W1203 | 改：本批级联/索引/统计产物刷新 |
| HANDOVER.md | W1203 | 改：本批级联/索引/统计产物刷新 |
| README.md | W1203 | 改：本批级联/索引/统计产物刷新 |
| STRUCTURE.md | W1203 | 改：本批级联/索引/统计产物刷新 |
| archive/docs/AGENTS-ARCHIVE.md | W1203 | 改：本批级联/索引/统计产物刷新 |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1203 | 改：本批级联/索引/统计产物刷新 |
| archive/docs/workflows-readme-history.md | W1203 | 改：本批级联/索引/统计产物刷新 |
| docs/00-导读/W批次编号对账表.md | W1203 | 回填：W1202 行关联 commit 0f820f37 + 状态已收官 + 本批认领行 |
| docs/00-导读/项目说明.md | W1203 | 改：本批级联/索引/统计产物刷新 |
| docs/11-方案报告/计划方案/T96-任务计划执行与经验沉淀报告-2026-11-10.md | W1203 | 改：§8.3 补记 W1202 收官批合并提交 0f820f37 |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1203 | 订正：§13.6 归属批次号（原 W935/W936/W937 已被占用）→ D-2b 重取 W1203·另两项标待取号 |
| scripts/output/INDEX.md | W1203 | 改：本批级联/索引/统计产物刷新 |
| scripts/output/README.md | W1203 | 改：本批级联/索引/统计产物刷新 |
| scripts/output/_cascade_files_W1203.txt | W1203 | 改：本批级联/索引/统计产物刷新 |
| scripts/output/_vermilion_solid_cache.json | W1203 | 改：本批级联/索引/统计产物刷新 |
| scripts/output/_w1203_spec.json | W1203 | 新建：本批 spec |
| scripts/output/file-index.md | W1203 | 改：本批级联/索引/统计产物刷新 |
| scripts/output/stats.json | W1203 | 改：本批级联/索引/统计产物刷新 |
| scripts/output/tools-inventory.md | W1203 | 改：本批级联/索引/统计产物刷新 |
| site/data/cross-time-danmaku.html | W1203 | 改：本批级联/索引/统计产物刷新 |
| site/data/tag-cloud.html | W1203 | 改：本批级联/索引/统计产物刷新 |
| site/dukou-engine.html | W1203 | 改：本批级联/索引/统计产物刷新 |
| site/index.html | W1203 | 改：本批级联/索引/统计产物刷新 |
| xiyouji-agent-web/package.json | W1203 | 改：test:server 挂入 dualwrite.test.ts |
| xiyouji-agent-web/server/storage/INDEX.md | W1203 | 改：本批级联/索引/统计产物刷新 |
| xiyouji-agent-web/server/storage/README.md | W1203 | 改：本批级联/索引/统计产物刷新 |
| xiyouji-agent-web/server/storage/dualwrite.test.ts | W1203 | 新建：双写层契约测试 4 例（两 SQLite 实例互为两侧·无外部依赖全跑） |
| xiyouji-agent-web/server/storage/dualwrite.ts | W1203 | 新建：双写后端（写两侧·读只走主库·副库写失败 fail-closed·返回值以主库为准·kind 沿用主库） |
| xiyouji-agent-web/server/storage/index.ts | W1203 | 改：接入 AGENT_WEB_DB_WRITE_MODE（primary/dual·非法取值 fail-closed）+ writeMode() 可查 |
| pitfalls.md | W1203 | 订正：E-220 就绪链补精确（batch_cascade 后须再 add 再刷目录索引·改 .ts 必先 tsc -b·类型层缺字段致 CI Agent Web Build 红的实证） |


## W1202 GitHub「Security and quality」面板归零收官批（2026-11-10）

| 文件 | W | 说明 |
|---|---|---|
| .github/workflows/README.md | W1202 | 改：本批级联/索引/统计产物刷新 |
| AGENTS.md | W1202 | 改：本批级联/索引/统计产物刷新 |
| CHANGELOG.md | W1202 | 立段：W1202 面板归零收官批（41 条 pillow 告警关闭）|
| CITATION.cff | W1202 | 改：本批级联/索引/统计产物刷新 |
| HANDOVER.md | W1202 | 改：本批级联/索引/统计产物刷新 |
| README.md | W1202 | 改：本批级联/索引/统计产物刷新 |
| STRUCTURE.md | W1202 | 改：本批级联/索引/统计产物刷新 |
| archive/docs/AGENTS-ARCHIVE.md | W1202 | 改：本批级联/索引/统计产物刷新 |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1202 | 改：本批级联/索引/统计产物刷新 |
| archive/docs/workflows-readme-history.md | W1202 | 改：本批级联/索引/统计产物刷新 |
| docs/00-导读/W批次编号对账表.md | W1202 | 登记：W1202 认领行 + W1201 回填（39b65372）|
| docs/00-导读/项目说明.md | W1202 | 改：本批级联/索引/统计产物刷新 |
| docs/11-方案报告/计划方案/T96-任务计划执行与经验沉淀报告-2026-11-10.md | W1202 | 改：新增 §8.3 终态读数回填（open 41→0·AC-11 达成·AC-10 在依赖图侧不可达）|
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1202 | 改：本批级联/索引/统计产物刷新 |
| pitfalls.md | W1202 | 订正：E-219 补最终处置（人工关闭 dismiss_reason=inaccurate + 可复跑脚本入仓）|
| pytest.ini | W1202 | 改：本批级联/索引/统计产物刷新 |
| scripts/INDEX.md | W1202 | 改：本批级联/索引/统计产物刷新 |
| scripts/dismiss_pillow_alerts.py | W1202 | 新建：41 条 pillow 告警的批量关闭/回滚脚本（--dry-run/--apply/--revert·依据链写在头注释）|
| scripts/output/INDEX.md | W1202 | 改：本批级联/索引/统计产物刷新 |
| scripts/output/README.md | W1202 | 改：本批级联/索引/统计产物刷新 |
| scripts/output/_cascade_files_W1202.txt | W1202 | 改：本批级联/索引/统计产物刷新 |
| scripts/output/_vermilion_solid_cache.json | W1202 | 改：本批实算/级联产物刷新 |
| scripts/output/_w1202_spec.json | W1202 | 新建：本批 spec |
| scripts/output/file-index.md | W1202 | 改：本批级联/索引/统计产物刷新 |
| scripts/output/stats-changelog.json | W1202 | 改：本批级联/索引/统计产物刷新 |
| scripts/output/stats-index.md | W1202 | 改：本批级联/索引/统计产物刷新 |
| scripts/output/stats.json | W1202 | 改：本批级联/索引/统计产物刷新 |
| scripts/output/tools-inventory.md | W1202 | 改：本批级联/索引/统计产物刷新 |
| site/data/cross-time-danmaku.html | W1202 | 改：本批级联/索引/统计产物刷新 |
| site/data/tag-cloud.html | W1202 | 改：本批级联/索引/统计产物刷新 |
| site/dukou-engine.html | W1202 | 改：本批级联/索引/统计产物刷新 |
| site/index.html | W1202 | 改：本批级联/索引/统计产物刷新 |
| tests/unit/INDEX.md | W1202 | 改：目录清单补入本批新件（新单测）|
| tests/unit/README.md | W1202 | 改：目录清单补入本批新件（新单测）|
| tests/unit/test_dismiss_pillow_alerts.py | W1202 | 新建：dismiss 脚本的目标筛选逻辑单测（第 42 门禁 C1 引用面·5 例） |

## W1201 重建态批·恢复仓库完整态 + 落仓路径 A 的否证结论（2026-11-10）

| 文件 | W | 说明 |
|---|---|---|
| .github/workflows/README.md | W1201 | 改：本批级联/索引/统计产物刷新 |
| AGENTS.md | W1201 | 改：本批级联/索引/统计产物刷新 |
| CHANGELOG.md | W1201 | 立段：W1201 重建态批（恢复完整态 + 路径 A 否证结论落仓） |
| CITATION.cff | W1201 | 改：本批级联/索引/统计产物刷新 |
| HANDOVER.md | W1201 | 改：本批级联/索引/统计产物刷新 |
| README.md | W1201 | 改：本批级联/索引/统计产物刷新 |
| STRUCTURE.md | W1201 | 改：本批级联/索引/统计产物刷新 |
| archive/docs/AGENTS-ARCHIVE.md | W1201 | 改：本批级联/索引/统计产物刷新 |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1201 | 改：本批级联/索引/统计产物刷新 |
| archive/docs/workflows-readme-history.md | W1201 | 改：本批级联/索引/统计产物刷新 |
| docs/00-导读/W批次编号对账表.md | W1201 | 登记：W1201 认领行 + W1199 回填（6dbf27dc） |
| docs/00-导读/项目说明.md | W1201 | 改：本批级联/索引/统计产物刷新 |
| docs/11-方案报告/计划方案/T96-任务计划执行与经验沉淀报告-2026-11-10.md | W1201 | 改：新增 §8.2 补记（删除态已被正确解析·残留仍在·AC-10/AC-11 在依赖图侧不可达） |
| pitfalls.md | W1201 | 订正：E-219 原结论作废并改写（删除态被正确解析后残留仍在⇒ 该动作无效·仓内无清除路径） |
| scripts/INDEX.md | W1201 | 改：本批级联/索引/统计产物刷新 |
| scripts/output/INDEX.md | W1201 | 改：本批级联/索引/统计产物刷新 |
| scripts/output/README.md | W1201 | 改：本批级联/索引/统计产物刷新 |
| scripts/output/_cascade_files_W1201.txt | W1201 | 改：本批级联/索引/统计产物刷新 |
| scripts/output/_vermilion_solid_cache.json | W1201 | 改：本批级联/索引/统计产物刷新 |
| scripts/output/_w1201_spec.json | W1201 | 新建：本批 spec |
| scripts/output/citability-report.json | W1201 | 改：本批级联/索引/统计产物刷新 |
| scripts/output/file-index.md | W1201 | 改：本批级联/索引/统计产物刷新 |
| scripts/output/stats.json | W1201 | 改：本批级联/索引/统计产物刷新 |
| scripts/output/tools-inventory.md | W1201 | 改：本批级联/索引/统计产物刷新 |
| scripts/requirements.txt | W1201 | 重建：逐字恢复（基准 70d8e51d·diff 0 行）⇒ 恢复 Dependabot 对 /scripts 的监控 |
| site/data/cross-time-danmaku.html | W1201 | 改：本批级联/索引/统计产物刷新 |
| site/data/tag-cloud.html | W1201 | 改：本批级联/索引/统计产物刷新 |
| site/dukou-engine.html | W1201 | 改：本批级联/索引/统计产物刷新 |
| site/index.html | W1201 | 改：本批级联/索引/统计产物刷新 |
| tests/unit/test_ci_wiring.py | W1201 | 改：加回监控面 PyYAML 第二段断言（安装面 + 监控面双覆盖） |


## W1199 提交前一次性就绪链落仓（2026-11-10）

| 文件 | W | 说明 |
|---|---|---|
| .agent/skills/puti-shouye/SKILL.md | W1199 | 改：坑表条数声明 313→314（两处） |
| .github/workflows/README.md | W1199 | 改：批头版本行与里程碑随 W1199 版本面推进 |
| .md | W1199 | 改：本批级联/索引/统计产物刷新 |
| AGENTS.md | W1199 | 改：最高频铁则段新增「提交前就绪链」一条 + 坑表总数 313→314 + 分项节计数 180→181 |
| CHANGELOG.md | W1199 | 立段：W1199 提交前一次性就绪链落仓批（E-220 + 规则入 AGENTS + 计数链同步） |
| CITATION.cff | W1199 | 改：版本条目随 W1199 版本面推进 |
| HANDOVER.md | W1199 | 改：方法论沉淀新增条目 + 坑表指针 313→314 + 最后更新行同批重复修复（恢复级联唯一写） |
| README.md | W1199 | 改：批头版本行与批次摘要随 W1199 版本面推进 |
| STRUCTURE.md | W1199 | 改：批头版本行随 W1199 版本面推进 |
| archive/docs/AGENTS-ARCHIVE.md | W1199 | 归档：AGENTS 脚注滚动历史段迁移 |
| archive/docs/workflows-readme-history.md | W1199 | 归档：workflow README 历史段滚动登记 |
| docs/00-导读/W批次编号对账表.md | W1199 | 登记：W1199 认领行 + W1198 收官回填（70d8e51d）|
| docs/00-导读/项目说明.md | W1199 | 改：批头版本行与摘要随 W1199 版本面推进 |
| docs/11-方案报告/计划方案/T96-任务计划执行与经验沉淀报告-2026-11-10.md | W1199 | 改：新增 §8 合并后实证订正（订正「逐 commit 处理」论证错误 + 记录合并后读数 + 修法升级为两步 PR）|
| pitfalls.md | W1199 | 入表：E-220 提交前就绪链 + 节计数 180→181；E-219 补注（删除态须单独成为 default branch head 才会被解析）+ 三处总数声明同步到 314 |
| scripts/INDEX.md | W1199 | 改：本批级联/索引/统计产物刷新 |
| scripts/output/INDEX.md | W1199 | 改：本批级联/索引/统计产物刷新 |
| scripts/output/README.md | W1199 | 改：本批级联/索引/统计产物刷新 |
| scripts/output/_cascade_files_W1199.txt | W1199 | 改：本批级联/索引/统计产物刷新 |
| scripts/output/_w1199_spec.json | W1199 | 新建：本批 spec（批级产物登记与提交范围判据的应动全集） |
| scripts/output/file-index.md | W1199 | 改：本批级联/索引/统计产物刷新 |
| scripts/output/stats.json | W1199 | 改：本批级联/索引/统计产物刷新 |
| scripts/output/tools-inventory.md | W1199 | 改：本批级联/索引/统计产物刷新 |
| scripts/requirements.txt | W1199 | 删除：删除态使该路径在 main head 上消失一次（Graph Update 只解析 head commit⇒删除态须单独成 head）|
| site/data/cross-time-danmaku.html | W1199 | 改：本批级联/索引/统计产物刷新 |
| site/data/tag-cloud.html | W1199 | 改：本批级联/索引/统计产物刷新 |
| site/dukou-engine.html | W1199 | 改：本批级联/索引/统计产物刷新 |
| site/index.html | W1199 | 改：本批级联/索引/统计产物刷新 |
| tests/unit/test_ci_wiring.py | W1199 | 改：暂删监控面 PyYAML 第二段断言（删除态下该文件不存在·W1200 加回）|


## W1198 Dependabot 41 条 Pillow 告警归零批（2026-11-10）

| 文件 | W | 说明 |
|---|---|---|
| .agent/skills/puti-shouye/SKILL.md | W1198 | W1198 | 改：坑表条数 312→313（两处声明·C5e 分项对拍）| |
| .github/workflows/README.md | W1198 | W1198 | 改：三个 job 的流程描述改指哈希化清单与 --require-hashes 安装形态 | |
| .github/workflows/ci.yml | W1198 | W1198 | 改：4 处 cache-dependency-path 与 1 处 pip-audit 扫描源改指 scripts/requirements-hashed.txt（CI 真实安装源·审计覆盖面 9→51 项） | |
| .github/workflows/screenshot-review.yml | W1198 | W1198 | 改：cache-dependency-path 改指 scripts/requirements-hashed.txt | |
| .github/workflows/security.yml | W1198 | W1198 | 改：cache-dependency-path 与 pip-audit 扫描源改指哈希化清单·删除文件缺失即静默跳过的条件分支（审计恒生效） | |
| AGENTS.md | W1198 | W1198 | 改：坑表条数 312→313 + PyYAML 登记表述改绑真实安装源 + 版本脚注滚动（W1198 入·W1193 出） | |
| CHANGELOG.md | W1198 | W1198 | 立段：W1198 Dependabot 41 条 Pillow 告警归零批（根因在依赖图条目累积·修法为删除后重建） | |
| CITATION.cff | W1198 | W1198 | 改：版本条目随本批版本面推进 | |
| HANDOVER.md | W1198 | W1198 | 改：坑表条数 312→313 + 最后更新行与当前进度区更新为 W1198 | |
| README.md | W1198 | W1198 | 改：批头版本行与批次摘要随本批推进 | |
| STRUCTURE.md | W1198 | W1198 | 改：批头版本行随本批推进 | |
| archive/docs/CHANGELOG-ARCHIVE.md | W1198 | 归档：CHANGELOG 版段迁出 51 段（W1117-W1170）以对齐两面下界与腾体积窗 |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1198 | W1198 | 归档：台账迁出 W1136-W1137 两行 | |
| archive/docs/file-index-ARCHIVE.md | W1198 | 归档：file-index 版段迁出 51 段以对齐两面下界与腾体积窗 |
| archive/docs/workflows-readme-history.md | W1198 | W1198 | 归档：workflow README 历史段滚动登记 | |
| docs/00-导读/W批次编号对账表.md | W1198 | W1198 | 登记：W1198 认领行与状态（并含台账行归档 2 行腾窗口） | |
| docs/00-导读/项目说明.md | W1198 | W1198 | 改：批头版本行与摘要随本批推进 | |
| docs/11-方案报告/README.md | W1198 | W1198 | 登记：T96 报告（登记号 110） | |
| docs/11-方案报告/计划方案/T96-任务计划执行与经验沉淀报告-2026-11-10.md | W1198 | W1198 | 新建：T96 收官报告（32 项结构判据全过） | |
| docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md | W1198 | 生成：stats 实算标记跟随刷新 |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1198 | 生成：stats 实算标记跟随刷新 |
| docs/INDEX.md | W1198 | 生成：文档索引刷新（含 T96 报告入册） |
| pitfalls.md | W1198 | W1198 | 入表：E-219 依赖图条目按 manifest 路径累积历史 blob（改内容不触发清理·须让路径消失一次）+ 节计数 179→180 | |
| scripts/INDEX.md | W1198 | W1198 | 生成：目录索引刷新（哈希化清单与依赖清单条目） | |
| scripts/README.md | W1198 | W1198 | 改：依赖段写明两份清单分工（CI 安装源与 Dependabot 监控面） | |
| scripts/check_search_index_fresh.py | W1198 | W1198 | 改：jieba 缺失提示里的安装命令改指哈希化清单 | |
| scripts/output/INDEX.md | W1198 | 生成：产物目录索引刷新 |
| scripts/output/README.md | W1198 | 生成：产物目录说明刷新 |
| scripts/output/_cascade_files_W1198.txt | W1198 | W1198 | 生成：本批级联落盘文件清单 | |
| scripts/output/_vermilion_solid_cache.json | W1198 | 生成：朱砂实底门禁增量缓存刷新 |
| scripts/output/_w1198_spec.json | W1198 | W1198 | 新建：本批 spec（批级产物登记与提交范围判据的应动全集）| |
| scripts/output/file-index.md | W1198 | W1198 | 生成：文件索引登记本批改动件 | |
| scripts/output/stats-changelog.json | W1198 | 生成：CHANGELOG 统计实算刷新 |
| scripts/output/stats-index.md | W1198 | 生成：索引统计实算刷新 |
| scripts/output/stats.json | W1198 | W1198 | 生成：统计实算刷新（批次与产物计数） | |
| scripts/output/tools-inventory.md | W1198 | W1198 | 改：本批改动 | |
| scripts/preflight_check.py | W1198 | W1198 | 改：ruff 版本对拍改读哈希化清单（对拍对象须是 CI 实际安装的清单） | |
| scripts/requirements.txt | W1198 | W1198 | 两步提交：第一步删除（触发依赖图移除该 manifest 贡献的全部条目）第二步逐字重建（内容零变化·git diff 行数 0）| |
| site/data/cross-time-danmaku.html | W1198 | W1198 | 生成：页脚版本行随本批版本面推进 | |
| site/data/search.html | W1198 | W1198 | 改：本批改动 | |
| site/data/tag-cloud.html | W1198 | W1198 | 生成：页脚版本行随本批版本面推进 | |
| site/dukou-engine.html | W1198 | W1198 | 生成：页脚版本行随本批版本面推进 | |
| site/en/search.html | W1198 | W1198 | 改：本批改动 | |
| site/index.html | W1198 | W1198 | 生成：页脚版本行随本批版本面推进 | |
| tests/unit/test_ci_wiring.py | W1198 | W1198 | 改：PyYAML 登记断言改绑 CI 真实安装源 requirements-hashed.txt（修 W1195 遗留判据漂移）并加回 Dependabot 监控面的第二段断言 | |
| scripts/batch_cascade.py | W1198 | 改：W534 契约的 CHANGELOG 检查面扩到归档面（归档机制 W960 落地后的机制缺口·正本无该段时假红）|

## W1197 守卫扫描面扩到全仓 shell 批（2026-11-10）

| 文件 | W | 说明 |
|---|---|---|
| scripts/external_rule_scope.py | W1197 | 新建：外部规则 shell 扫描面的共享识别（与 Scorecard isMatchingShellScriptFile 同源）|
| scripts/check_install_pins.py | W1197 | 改：扫描面扩到全仓 shell（安装命令面）+ 自证升至 20 例 |
| scripts/check_action_refs.py | W1197 | 改：扫描面扩到全仓 shell（不可变引用面）+ 自证新增 N9-N14 |
| scripts/check_external_rule_coverage.py | W1197 | 改：守卫扫描面表更新（两守卫已扩到全仓 shell）→覆盖缺口闭合 |
| .github/workflows/security.yml | W1197 | 改：dependency-pin job 新增 check_action_refs.py 步骤（无 paths 过滤·失败即阻断）|
| .github/workflows/workflow-lint.yml | W1197 | 改：paths 扩到 **/*.sh（shell 改动也触发守卫）|
| pitfalls.md | W1197 | 改：E-218 补充重褄理记录（缺口已修）|
| AGENTS.md | W1197 | 改：坑表计数链同步 |
| HANDOVER.md | W1197 | 改：坑表计数链同步 |
| .agent/skills/puti-shouye/SKILL.md | W1197 | 改：坑表计数链同步 |
| CHANGELOG.md | W1197 | 改：W1197 段 |
| docs/00-导读/W批次编号对账表.md | W1197 | 改：W1197 认领行 |
| scripts/output/_w1197_spec.json | W1197 | 新建：本批 spec |
| scripts/output/_cascade_files_W1197.txt | W1197 | 新建：级联清单 |
| .github/workflows/README.md | W1197 | 改：区间行推进（版本面） |
| CITATION.cff | W1197 | 改：version/date 推进（级联） |
| README.md | W1197 | 改：版本面推进（级联） |
| STRUCTURE.md | W1197 | 改：版本面推进（级联） |
| archive/docs/AGENTS-ARCHIVE.md | W1197 | 改：脚注沿革滚动（级联） |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1197 | 改：迁出行（级联） |
| archive/docs/workflows-readme-history.md | W1197 | 改：逐批明细追加（级联） |
| docs/00-导读/项目说明.md | W1197 | 改：版本面推进（级联） |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1197 | 改：stats 实体标记跟随（级联） |
| pytest.ini | W1197 | 改：pytest collected 计数标记跟随 stats 实算（新增守卫脚本） |
| scripts/output/file-index.md | W1197 | 改：W1197 段重建 |
| scripts/output/stats-changelog.json | W1197 | 改：stats 变更记录刷新（级联） |
| scripts/output/stats-index.md | W1197 | 改：stats 索引刷新（级联） |
| scripts/output/stats.json | W1197 | 改：stats 刷新（级联） |
| scripts/output/tools-inventory.md | W1197 | 改：工具清单刷新（含新增守卫） |
| site/data/cross-time-danmaku.html | W1197 | 改：页脚版本戳推进（级联） |
| site/data/tag-cloud.html | W1197 | 改：页脚版本戳推进（级联） |
| site/dukou-engine.html | W1197 | 改：页脚版本戳推进（级联） |
| site/index.html | W1197 | 改：页脚版本戳推进（级联） |
| scripts/output/INDEX.md | W1197 | 改：目录索引/说明刷新（级联）|
| scripts/output/README.md | W1197 | 改：目录索引/说明刷新（级联）|
| scripts/INDEX.md | W1197 | 改：目录索引刷新（级联）|
| scripts/output/_vermilion_solid_cache.json | W1197 | 改：朱砂实底缓存 sha1 跟随页面改动刷新（级联）|


## W1196 外部规则覆盖面审计批（2026-11-10）

| 文件 | W | 说明 |
|---|---|---|
| scripts/check_external_rule_coverage.py | W1196 | 新建：外部规则覆盖面审计守卫（shell 面安装命令 / 各生态清单源 / 守卫覆盖缺口）|
| .github/workflows/security.yml | W1196 | 改：安装命令面守卫 job 新增「校验外部规则覆盖面」步骤 |
| pitfalls.md | W1196 | 改：E-218 入表（守卫扫描面宽于外部规则的扫描面）|
| AGENTS.md | W1196 | 改：坑表计数链同步 |
| HANDOVER.md | W1196 | 改：坑表计数链同步 |
| .agent/skills/puti-shouye/SKILL.md | W1196 | 改：坑表计数链同步 |
| CHANGELOG.md | W1196 | 改：W1196 段 |
| docs/00-导读/W批次编号对账表.md | W1196 | 改：W1196 认领行 |
| scripts/output/_w1196_spec.json | W1196 | 新建：本批 spec |
| scripts/output/_cascade_files_W1196.txt | W1196 | 新建：级联清单 |


## W1195 Scorecard Pinned-Dependencies 真修批（2026-11-09）

| 文件 | W | 说明 |
|---|---|---|
| scripts/requirements-hashed.txt | W1195 | 新建：哈希化依赖清单（51 项闭包·直接 9 + 测试传递 8 + CI 工具包与传递 34）|
| scripts/check_install_pins.py | W1195 | 改：判据改为与 Scorecard 源码同源（pip 需 --require-hashes·npm 需 npm ci）+ 自证用例升级为 14 例 |
| .github/workflows/ci.yml | W1195 | 改：npm 安装改 npm ci --prefix scripts（去掉零调用的 @playwright/test）+ pip 安装改 --require-hashes 哈希化清单 + 删除 black 遗留安装 |
| .github/workflows/ci-sim.yml | W1195 | 改：pip 自身升级带 --hash + 清单安装改 --require-hashes |
| .github/workflows/perf.yml | W1195 | 改：lhci 安装改 npm ci --prefix scripts/lighthouse（新建独立 lock）+ 调用改本地 bin |
| .github/workflows/screenshot-review.yml | W1195 | 改：npm 安装改 npm ci --prefix scripts + pip 安装改 --require-hashes |
| .github/workflows/security.yml | W1195 | 改：pip-audit 安装改 --require-hashes 哈希化清单 |
| .github/workflows/workflow-lint.yml | W1195 | 改：PyYAML 安装改 --require-hashes 哈希化清单 |
| scripts/lighthouse/package.json | W1195 | 新建：lhci 独立安装单元（@lhci/cli 0.16.0·含 basic-ftp 的 overrides 6.2.6）|
| scripts/lighthouse/package-lock.json | W1195 | 新建：lhci 锁文件（356 包·resolved 全为 registry.npmjs.org·basic-ftp 锁 6.2.6·无 extract-zip）|
| pitfalls.md | W1195 | 改：E-215 入表（外部规则必须读判据源码）|
| AGENTS.md | W1195 | 改：坑表计数链同步 |
| HANDOVER.md | W1195 | 改：坑表计数链同步 |
| .agent/skills/puti-shouye/SKILL.md | W1195 | 改：坑表计数链同步 |
| CHANGELOG.md | W1195 | 改：W1195 段 |
| docs/00-导读/W批次编号对账表.md | W1195 | 改：W1195 认领行 |
| docs/11-方案报告/README.md | W1195 | 改：§六 登记 T95（登记号 109）|
| docs/11-方案报告/计划方案/T95-任务计划执行与经验沉淀报告-2026-11-09.md | W1195 | 新建：Scorecard Pinned-Dependencies 真修报告 |
| docs/11-方案报告/计划方案/T94-任务计划执行与经验沉淀报告-2026-11-09.md | W1195 | 改：V1.0 → V1.1（后续发现说明）|
| scripts/output/_w1195_spec.json | W1195 | 新建：本批 spec |
| scripts/output/_cascade_files_W1195.txt | W1195 | 新建：级联清单 |
| scripts/lighthouse/INDEX.md | W1195 | 新建：目录索引（级联）|
| scripts/lighthouse/README.md | W1195 | 新建：目录说明（级联）|
| CITATION.cff | W1195 | 改：version/date 推进（级联） |
| README.md | W1195 | 改：版本面推进（级联） |
| STRUCTURE.md | W1195 | 改：版本面推进（级联） |
| docs/00-导读/项目说明.md | W1195 | 改：版本面推进（级联） |
| docs/INDEX.md | W1195 | 改：docs 目录索引重建（含 T95 报告） |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1195 | 改：stats 实体标记跟随（级联） |
| docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md | W1195 | 改：stats 实体标记跟随（级联） |
| archive/docs/AGENTS-ARCHIVE.md | W1195 | 改：脚注沿革滚动（级联） |
| archive/docs/workflows-readme-history.md | W1195 | 改：逐批明细追加（级联） |
| .github/workflows/README.md | W1195 | 改：区间行推进（版本面） |
| site/index.html | W1195 | 改：页脚版本戳推进（级联） |
| site/data/cross-time-danmaku.html | W1195 | 改：页脚版本戳推进（级联） |
| site/data/tag-cloud.html | W1195 | 改：页脚版本戳推进（级联） |
| site/dukou-engine.html | W1195 | 改：页脚版本戳推进（级联） |
| site/data/search.html | W1195 | 改：搜索索引刷新 + CSP meta 重哈希 |
| site/en/search.html | W1195 | 改：搜索索引刷新 + CSP meta 重哈希 |
| scripts/output/stats.json | W1195 | 改：stats 刷新（级联） |
| scripts/output/tools-inventory.md | W1195 | 改：工具清单刷新（含新增脚本） |
| scripts/output/README.md | W1195 | 改：目录文档刷新（级联） |
| scripts/output/file-index.md | W1195 | 改：W1195 段重建（含二轮交付面） |
| scripts/output/stats-changelog.json | W1195 | 改：stats 变更记录刷新（级联） |
| scripts/output/stats-index.md | W1195 | 改：stats 索引刷新（级联） |
| scripts/INDEX.md | W1195 | 改：目录索引刷新（含新增 scripts/lighthouse）（级联） |
| scripts/output/INDEX.md | W1195 | 改：目录索引刷新（级联） |
| scripts/output/_vermilion_solid_cache.json | W1195 | 改：朱砂实底缓存 sha1 跟随页面改动刷新（级联）|


## W1194 Scorecard 告警真项收口批（2026-11-09）

| 文件 | W | 说明 |
|---|---|---|
| .github/workflows/ci.yml | W1194 | 改：pip-audit 钉 2.10.1 + black/mypy 钉 26.10.1/2.4.1 |
| .github/workflows/security.yml | W1194 | 改：pip-audit 钉 2.10.1 + 新增 docker-pin job（打印期望 digest + 跑严格判据） |
| .github/workflows/perf.yml | W1194 | 改：@lhci/cli 由 0.13.x 钉精确版 0.13.0 |
| .github/workflows/screenshot-review.yml | W1194 | 改：两处 playwright/@playwright/test 钉 1.63.0 |
| .github/workflows/ci-sim.yml | W1194 | 改：pip 自身钉版 26.3 |
| .github/workflows/stale.yml | W1194 | 改：删 job 级多余 contents: write（权限最小化） |
| .github/workflows/release.yml | W1194 | 改：顶层 contents: write 收窄为 contents: read + 仅 release job 级提权 |
| scripts/check_docker_pin.py | W1194 | 新建：Dockerfile 基础镜像 digest 钉版守卫（5 例负样本自证） |
| docs/00-导读/W批次编号对账表.md | W1194 | 改：W1194 认领行 |
| docs/11-方案报告/README.md | W1194 | 改：§六 登记 T94（登记号 108） |
| docs/11-方案报告/计划方案/T94-任务计划执行与经验沉淀报告-2026-11-09.md | W1194 | 新建：Scorecard 告警真项收口报告 |
| scripts/output/_w1194_spec.json | W1194 | 新建：本批 spec |
| .github/workflows/ci.yml | W1194 | 改：pip-audit 钉 2.10.1 + black/mypy 钉 26.10.1/2.4.1 |
| .github/workflows/security.yml | W1194 | 改：pip-audit 钉 2.10.1 + 新增 dependency-pin job（打印期望 digest + 跑两道钉版判据） |
| .github/workflows/perf.yml | W1194 | 改：@lhci/cli 由 0.13.x 钉精确版 0.13.0 |
| .github/workflows/screenshot-review.yml | W1194 | 改：两处 playwright/@playwright/test 钉 1.63.0 |
| .github/workflows/ci-sim.yml | W1194 | 改：pip 自身钉版 26.3 |
| .github/workflows/stale.yml | W1194 | 改：删 job 级多余 contents: write（权限最小化） |
| .github/workflows/release.yml | W1194 | 改：顶层 contents: write 收窄为 contents: read + 仅 release job 级提权 |
| scripts/check_docker_pin.py | W1194 | 新建：Dockerfile 基础镜像 digest 钉版守卫（5 例负样本自证） |
| scripts/check_install_pins.py | W1194 | 新建：workflow 安装命令钉版守卫（9 例负样本自证） |
| docs/11-方案报告/计划方案/T94-任务计划执行与经验沉淀报告-2026-11-09.md | W1194 | 新建：Scorecard 告警真项收口报告 |
| scripts/output/_w1194_spec.json | W1194 | 新建：本批 spec |
| scripts/output/_cascade_files_W1194.txt | W1194 | 新建：级联清单 |
| xiyouji-agent-web/Dockerfile | W1194 | 改：FROM node:22-alpine 钉到 sha256:0e1754758c2df4cfa3e68d59e2e1b7374bb7fd9ea6328eaaacf15cc934af8202 |
| xiyouji-agent-web/package-lock.json | W1194 | 改：26 条 resolved 从第三方镜像站归一为 registry.npmjs.org（integrity 26/26 逐条核对一致） |
| scripts/check_install_pins.py | W1194 | 改：扩供应链面判据（lock 的 resolved 只允许官方注册表）+4 例负样本自证 |
| pitfalls.md | W1194 | 改：E-213 + E-214 两条（外部告警面逐面重核 + 取值双证与供应链归因）|
| AGENTS.md | W1194 | 改：坑表计数链同步（307→308 与分项一处）|
| HANDOVER.md | W1194 | 改：坑表计数链同步（两处）|
| .agent/skills/puti-shouye/SKILL.md | W1194 | 改：坑表计数链同步（两处）|

## W1193 Security and quality 面板残余收口批（2026-11-09）

| 文件 | W | 说明 |
|---|---|---|
| scripts/package.json | W1193 | 改：加 minimatch 精确版本选择器 override（>=9.0.0 <11.0.1 → ^11.0.5） |
| scripts/package-lock.json | W1193 | 改：lock 同步（minimatch 10.2.6 → 11.0.5） |
| scripts/requirements.txt | W1193 | 改：Pillow 依赖名大小写归一（触发 Dependabot 重算·钉版 13.0.0 不变） |
| xiyouji-desktop/package.json | W1193 | 改：加 minimatch 精确版本选择器 override |
| xiyouji-desktop/package-lock.json | W1193 | 改：lock 同步（minimatch 9.0.9 / 10.2.6 → 11.0.5） |
| docs/00-导读/W批次编号对账表.md | W1193 | 改：W1193 认领行 |
| docs/11-方案报告/README.md | W1193 | 改：§六 登记 T93（登记号 107） |
| docs/11-方案报告/计划方案/T93-任务计划执行与经验沉淀报告-2026-11-09.md | W1193 | 新建：面板残余收口报告 |
| scripts/output/_w1193_spec.json | W1193 | 新建：本批 spec |
| scripts/output/_cascade_files_W1193.txt | W1193 | 新建：级联清单 |
| CHANGELOG.md | W1193 | 改：W1193 段 + W1194 段（级联·两批共用） |
| scripts/output/file-index.md | W1193 | 改：W1193 段 + W1194 段（级联·两批共用） |
| HANDOVER.md | W1193 | 改：最后更新行 + 当前进度（级联） |
| CITATION.cff | W1193 | 改：version/date 推进（级联） |
| README.md | W1193 | 改：版本面推进（级联） |
| STRUCTURE.md | W1193 | 改：版本面推进（级联） |
| docs/00-导读/项目说明.md | W1193 | 改：版本面推进（级联） |
| AGENTS.md | W1193 | 改：版本脚注推进（级联） |
| archive/docs/AGENTS-ARCHIVE.md | W1193 | 改：脚注沿革滚动（级联） |
| .github/workflows/README.md | W1193 | 改：区间行推进（版本面） |
| archive/docs/workflows-readme-history.md | W1193 | 改：逐批明细追加（级联） |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1193 | 改：迁入 W1132-W1133 两行（台账正本段数回体积窗 60） |
| site/index.html | W1193 | 改：页脚版本戳推进（级联） |
| site/data/cross-time-danmaku.html | W1193 | 改：页脚版本戳推进（级联） |
| site/data/tag-cloud.html | W1193 | 改：页脚版本戳推进（级联） |
| site/dukou-engine.html | W1193 | 改：页脚版本戳推进（级联） |
| site/data/search.html | W1193 | 改：搜索索引刷新 + CSP meta 重哈希 |
| site/en/search.html | W1193 | 改：搜索索引刷新 + CSP meta 重哈希 |
| scripts/output/stats.json | W1193 | 改：stats 刷新（级联） |
| scripts/output/stats-changelog.json | W1193 | 改：stats 变更记录刷新（级联） |
| scripts/output/stats-index.md | W1193 | 改：stats 索引刷新（级联） |
| scripts/output/tools-inventory.md | W1193 | 改：工具清单刷新（gen_folder_docs） |
| scripts/output/_vermilion_solid_cache.json | W1193 | 改：朱砂实底缓存 sha1 跟随页面改动刷新 |
| pytest.ini | W1193 | 改：pytest collected 计数标记跟随 stats 实算（新增 2 个守卫脚本） |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1193 | 改：stats 实体标记跟随（级联） |
| docs/INDEX.md | W1193 | 改：docs 目录索引重建（docs_index.py） |
| scripts/INDEX.md | W1193 | 改：目录文档刷新（gen_folder_docs） |
| scripts/output/INDEX.md | W1193 | 改：目录文档刷新（gen_folder_docs） |
| scripts/output/README.md | W1193 | 改：目录文档刷新（gen_folder_docs） |
| docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md | W1193 | 改：stats 实体标记跟随（级联） |

## W1192 CI 五处红灯清偿批（2026-11-09）

| 文件 | W | 说明 |
|---|---|---|
| scripts/check_dark_state_gate.js | W1192 | 改：断言域限定到采集面内 + 已下线页白名单门禁（自测 5 → 9 负样本） |
| scripts/_render_scope.js | W1192 | 新建：采集面口径单点来源（listPages / chartsPages） |
| scripts/_audit_render_states.js | W1192 | 改：候选页枚举与 charts 判定改用 _render_scope.js |
| scripts/stat_event_probe.py | W1192 | 改：远端 goatcounter 判定改 hostname 标签精确比对（CodeQL #120）+ 7 例自测 |
| tests/e2e/test_site_quality.js | W1192 | 改：A1 派发 PointerEvent（对齐 W1169 事件族迁移） |
| xiyouji-agent-web/evals/golden-50.jsonl | W1192 | 改：dataset-039/041 改指现存等价数据集（dataset/dashboard.json 已于 W1157 删除） |
| docs/11-方案报告/计划方案/T92-任务计划执行与经验沉淀报告-2026-11-09.md | W1192 | 新建：五处红灯清偿报告 |
| docs/11-方案报告/README.md | W1192 | 改：§六 登记 T92（登记号 106） |
| docs/00-导读/W批次编号对账表.md | W1192 | 改：W1192 认领行 |
| scripts/output/_w1192_spec.json | W1192 | 新建：本批 spec |
| scripts/output/_cascade_files_W1192.txt | W1192 | 新建：级联清单 |
| CHANGELOG.md | W1192 | 改：W1181 段 4 条链接路径订正 + W1192 段（级联） |
| scripts/output/file-index.md | W1192 | 改：W1192 段（级联） |
| HANDOVER.md | W1192 | 改：最后更新行 + 当前进度（级联） |
| CITATION.cff | W1192 | 改：version/date 推进（级联） |
| README.md | W1192 | 改：版本面推进（级联） |
| STRUCTURE.md | W1192 | 改：版本面推进（级联） |
| docs/00-导读/项目说明.md | W1192 | 改：版本面推进（级联） |
| AGENTS.md | W1192 | 改：版本脚注推进（级联） |
| archive/docs/AGENTS-ARCHIVE.md | W1192 | 改：脚注沿革滚动（级联） |
| .github/workflows/README.md | W1192 | 改：区间行推进（版本面） |
| archive/docs/workflows-readme-history.md | W1192 | 改：逐批明细追加（级联） |
| site/index.html | W1192 | 改：页脚版本戳推进（级联） |
| site/data/cross-time-danmaku.html | W1192 | 改：页脚版本戳推进（级联） |
| site/data/tag-cloud.html | W1192 | 改：页脚版本戳推进（级联） |
| site/dukou-engine.html | W1192 | 改：页脚版本戳推进（级联） |
| site/data/search.html | W1192 | 改：搜索索引刷新 + CSP meta 重哈希 |
| site/en/search.html | W1192 | 改：搜索索引刷新 + CSP meta 重哈希 |
| scripts/output/stats.json | W1192 | 改：stats 刷新（级联） |
| scripts/output/tools-inventory.md | W1192 | 改：工具清单刷新（gen_folder_docs） |
| xiyouji-agent-web/fuzz/INDEX.md | W1192 | 改：目录文档刷新（gen_folder_docs） |
| scripts/archive_segments.py | W1192 | 改：A3 末尾块断言方向根修（原写法与 split_tail_block 行为矛盾 ⇒ 体积迁移恒红） |
| tests/unit/test_w1130_archive_tail_block.py | W1192 | 改：补 3 条 A3 回归锁（末尾块留在正本末尾 / 前缀被改拦截 / 末尾块被搬走拦截） |
| archive/docs/CHANGELOG-ARCHIVE.md | W1192 | 改：迁入 W1108-W1116 共 9 段（正本体积窗 236837 B） |
| archive/docs/file-index-ARCHIVE.md | W1192 | 改：追加 W1108-W1116 共 9 段（正本体积窗 244634 B） |
| pytest.ini | W1192 | 改：pytest collected 计数标记跟随 stats 实算（1530 → 1533·新增 3 条 A3 回归锁） |
| scripts/output/stats-changelog.json | W1192 | 改：stats 变更记录刷新（级联） |
| scripts/output/stats-index.md | W1192 | 改：stats 索引刷新（级联） |
| scripts/output/_vermilion_solid_cache.json | W1192 | 改：朱砂实底缓存 sha1 跟随页面改动刷新 |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1192 | 改：stats 实体标记跟随（级联） |
| docs/INDEX.md | W1192 | 改：docs 目录索引重建（docs_index.py·870 篇） |
| scripts/INDEX.md | W1192 | 改：目录文档刷新（gen_folder_docs） |
| scripts/output/INDEX.md | W1192 | 改：目录文档刷新（gen_folder_docs） |
| scripts/output/README.md | W1192 | 改：目录文档刷新（gen_folder_docs） |
| docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md | W1192 | 改：stats 实体标记跟随（级联） |

## W1191 GitHub「Security and quality」全清批（2026-11-09）

| 文件 | W | 说明 |
|---|---|---|
| .github/workflows/workflow-lint.yml | W1191 | 改：联网扫描步注入 GH_TOKEN（匿名配额不足） |
| .github/workflows/security.yml | W1191 | 改：CodeQL action v3 → v4（2026-12 弃用） |
| .github/workflows/fuzz.yml | W1191 | 新建：Jazzer + fast-check 双层 fuzz 工作流 |
| .github/CODEOWNERS | W1191 | 新建：Scorecard CodeReview 检查的 CODEOWNERS（11 条规则） |
| xiyouji-agent-web/fuzz.js | W1191 | 新建：Jazzer 入口（路径语义两轮实证·须落包根） |
| xiyouji-agent-web/fuzz/fuzz.ts | W1191 | 新建：Jazzer.js fuzz target（tools.ts 真实导出·白名单+凭证过滤） |
| xiyouji-agent-web/fuzz/fastcheck.test.ts | W1191 | 新建：fast-check 属性测试（Scorecard Fuzzing 检查的检出面） |
| xiyouji-agent-web/package.json | W1191 | 改：electron/fast-check 依赖 + fuzz 与 test:prop 脚本 |
| xiyouji-agent-web/package-lock.json | W1191 | 改：lock 同步（qs 6.17.1 等·npm audit 0 vulnerabilities） |
| xiyouji-desktop/package.json | W1191 | 改：electron 44.9.0 → 44.9.1 |
| xiyouji-desktop/package-lock.json | W1191 | 改：lock 同步（fast-uri 3.1.9） |
| xiyouji-desktop/tests/updater-config.test.mjs | W1191 | 改：electron 版本硬断言同步为 44.9.1 |
| scripts/check_action_refs.py | W1191 | 改：新增 api_auth_decision()（--api 无 token 走匿名兜底）+ 自测 N7/N8 |
| scripts/requirements.txt | W1191 | 改：Pillow 13.0.0 复核痕（触发 Dependabot 重解析） |
| scripts/verify_delivery.py | W1191 | 改：URL 剥离改等价非正则实现（消跨行高危判红） |
| scripts/cross_line_baseline.json | W1191 | 改：基线刷新（只删 1 条陈旧键·零新增） |
| scripts/check_chart_values.js | W1191 | 改：基线生成器补「判据口径」协议行（重生成不再丢行） |
| scripts/output/chart-values-baseline.txt | W1191 | 改：可视化基线 88 → 89 页（纳入 glossary 新页） |
| scripts/output/_w876_site_audit_final.json | W1191 | 改：朱砂实底台账纯新增 11 行（zh 审计面 98 → 99 页） |
| scripts/output/_vermilion_solid_cache.json | W1191 | 改：级联/探针缓存刷新 |
| site/data/glossary.html | W1191 | 改：补 ANALYTICS 块（统计事件门禁的唯一未注入页） |
| site/data/search.html | W1191 | 改：搜索索引刷新 + CSP 重哈希 |
| site/en/search.html | W1191 | 改：搜索索引刷新 + CSP 重哈希 |
| AGENTS.md | W1191 | 改：§4.2 五条槽摘要下放 gates.md（正文 51273 → 46702 B·入 48KB 窗口） |
| README.md | W1191 | 改：OpenSSF Best Practices 徽章（图片走 Scorecard SVG·链接指向 CII criteria） |
| SECURITY.md | W1191 | 改：补漏洞报告渠道 / 支持版本 / 公开披露策略三段 |
| docs/00-导读/协议边界速查.md | W1191 | 改：A5 篇数 35 → 42（磁盘实算对齐） |
| docs/00-导读/文档规范.md | W1191 | 改：verify full 段数 71 → 75（实数对齐） |
| docs/00-导读/新Agent启动Prompt.md | W1191 | 改：统计键 616/88/89 → 623/89/90（实算对齐） |
| docs/11-方案报告/README.md | W1191 | 改：§六 登记 T91（登记号 105） |
| docs/11-方案报告/计划方案/T91-任务计划执行与经验沉淀报告-2026-11-09.md | W1191 | 新建：两批收官报告 |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1191 | 改：台账归档滚动（迁 W1128–W1130） |
| docs/00-导读/W批次编号对账表.md | W1191 | 改：W1190/W1191 认领行 + 归档至 58 行 |
| STRUCTURE.md | W1191 | 改：版本面推进（级联） |
| docs/00-导读/项目说明.md | W1191 | 改：版本面推进（级联） |
| scripts/output/stats.json | W1191 | 改：stats 刷新（级联） |
| site/index.html | W1191 | 改：页脚版本戳推进（级联） |
| site/dukou-engine.html | W1191 | 改：页脚版本戳推进（级联） |
| site/data/tag-cloud.html | W1191 | 改：页脚版本戳推进（级联） |
| site/data/cross-time-danmaku.html | W1191 | 改：页脚版本戳推进（级联） |
| archive/docs/AGENTS-ARCHIVE.md | W1191 | 改：脚注沿革滚动（级联） |
| archive/docs/workflows-readme-history.md | W1191 | 改：逐批明细追加（级联） |
| scripts/output/INDEX.md | W1191 | 改：目录文档刷新（gen_folder_docs） |
| scripts/output/README.md | W1191 | 改：目录文档刷新（gen_folder_docs） |
| docs/00-导读/INDEX.md | W1191 | 改：目录文档刷新（gen_folder_docs） |
| docs/00-导读/README.md | W1191 | 改：目录文档刷新（gen_folder_docs） |
| xiyouji-agent-web/fuzz/INDEX.md | W1191 | 新建：fuzz 目录索引（目录文档） |
| xiyouji-agent-web/fuzz/README.md | W1191 | 新建：fuzz 目录说明（目录文档） |
| .github/INDEX.md | W1191 | 改：目录文档刷新（gen_folder_docs） |
| .github/workflows/INDEX.md | W1191 | 改：目录文档刷新（gen_folder_docs） |
| xiyouji-agent-web/INDEX.md | W1191 | 改：目录文档刷新（gen_folder_docs） |
| scripts/output/tools-inventory.md | W1191 | 改：工具清单刷新（gen_folder_docs） |
| docs/INDEX.md | W1191 | 改：docs 目录索引重建（docs_index.py） |
| scripts/output/stats-changelog.json | W1191 | 改：stats 变更记录刷新（stats.py） |
| scripts/output/stats-index.md | W1191 | 改：stats 索引刷新（stats.py） |
| docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md | W1191 | 改：stats 实体标记跟随（stats.py） |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1191 | 改：stats 实体标记跟随（stats.py） |
| scripts/output/_w1191_spec.json | W1191 | 新建：本批 spec |
| CHANGELOG.md | W1191 | 改：W1191 段（级联） |
| scripts/output/file-index.md | W1191 | 改：W1191 段（级联） |
| HANDOVER.md | W1191 | 改：最后更新行 + 当前进度（级联） |
| CITATION.cff | W1191 | 改：version/date 推进（级联） |
| .github/workflows/README.md | W1191 | 改：区间行推进（版本面） |
| scripts/output/_cascade_files_W1191.txt | W1191 | 新建：级联清单 |

## W1190 CI 周级联网扫描根修批（2026-11-09）

| 文件 | W | 说明 |
|---|---|---|
| .github/workflows/workflow-lint.yml | W1190 | 改：联网扫描步注入 GH_TOKEN（匿名配额不足） |
| .github/workflows/security.yml | W1190 | 改：CodeQL action v3 → v4（2026-12 弃用） |
| .github/workflows/fuzz.yml | W1190 | 新建：Jazzer + fast-check 双层 fuzz 工作流 |
| .github/CODEOWNERS | W1190 | 新建：Scorecard CodeReview 检查的 CODEOWNERS（11 条规则） |
| xiyouji-agent-web/fuzz.js | W1190 | 新建：Jazzer 入口（路径语义两轮实证·须落包根） |
| xiyouji-agent-web/fuzz/fuzz.ts | W1190 | 新建：Jazzer.js fuzz target（tools.ts 真实导出·白名单+凭证过滤） |
| xiyouji-agent-web/fuzz/fastcheck.test.ts | W1190 | 新建：fast-check 属性测试（Scorecard Fuzzing 检查的检出面） |
| xiyouji-agent-web/package.json | W1190 | 改：electron/fast-check 依赖 + fuzz 与 test:prop 脚本 |
| xiyouji-agent-web/package-lock.json | W1190 | 改：lock 同步（qs 6.17.1 等·npm audit 0 vulnerabilities） |
| xiyouji-desktop/package.json | W1190 | 改：electron 44.9.0 → 44.9.1 |
| xiyouji-desktop/package-lock.json | W1190 | 改：lock 同步（fast-uri 3.1.9） |
| xiyouji-desktop/tests/updater-config.test.mjs | W1190 | 改：electron 版本硬断言同步为 44.9.1 |
| scripts/check_action_refs.py | W1190 | 改：新增 api_auth_decision()（--api 无 token 走匿名兜底）+ 自测 N7/N8 |
| scripts/requirements.txt | W1190 | 改：Pillow 13.0.0 复核痕（触发 Dependabot 重解析） |
| scripts/verify_delivery.py | W1190 | 改：URL 剥离改等价非正则实现（消跨行高危判红） |
| scripts/cross_line_baseline.json | W1190 | 改：基线刷新（只删 1 条陈旧键·零新增） |
| scripts/check_chart_values.js | W1190 | 改：基线生成器补「判据口径」协议行（重生成不再丢行） |
| scripts/output/chart-values-baseline.txt | W1190 | 改：可视化基线 88 → 89 页（纳入 glossary 新页） |
| scripts/output/_w876_site_audit_final.json | W1190 | 改：朱砂实底台账纯新增 11 行（zh 审计面 98 → 99 页） |
| scripts/output/_vermilion_solid_cache.json | W1190 | 改：级联/探针缓存刷新 |
| site/data/glossary.html | W1190 | 改：补 ANALYTICS 块（统计事件门禁的唯一未注入页） |
| site/data/search.html | W1190 | 改：搜索索引刷新 + CSP 重哈希 |
| site/en/search.html | W1190 | 改：搜索索引刷新 + CSP 重哈希 |
| AGENTS.md | W1190 | 改：§4.2 五条槽摘要下放 gates.md（正文 51273 → 46702 B·入 48KB 窗口） |
| README.md | W1190 | 改：OpenSSF Best Practices 徽章（图片走 Scorecard SVG·链接指向 CII criteria） |
| SECURITY.md | W1190 | 改：补漏洞报告渠道 / 支持版本 / 公开披露策略三段 |
| docs/00-导读/协议边界速查.md | W1190 | 改：A5 篇数 35 → 42（磁盘实算对齐） |
| docs/00-导读/文档规范.md | W1190 | 改：verify full 段数 71 → 75（实数对齐） |
| docs/00-导读/新Agent启动Prompt.md | W1190 | 改：统计键 616/88/89 → 623/89/90（实算对齐） |
| docs/11-方案报告/README.md | W1190 | 改：§六 登记 T91（登记号 105） |
| docs/11-方案报告/计划方案/T91-任务计划执行与经验沉淀报告-2026-11-09.md | W1190 | 新建：两批收官报告 |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1190 | 改：台账归档滚动（迁 W1128–W1130） |
| docs/00-导读/W批次编号对账表.md | W1190 | 改：W1190/W1191 认领行 + 归档至 58 行 |
| STRUCTURE.md | W1190 | 改：版本面推进（级联） |
| docs/00-导读/项目说明.md | W1190 | 改：版本面推进（级联） |
| scripts/output/stats.json | W1190 | 改：stats 刷新（级联） |
| site/index.html | W1190 | 改：页脚版本戳推进（级联） |
| site/dukou-engine.html | W1190 | 改：页脚版本戳推进（级联） |
| site/data/tag-cloud.html | W1190 | 改：页脚版本戳推进（级联） |
| site/data/cross-time-danmaku.html | W1190 | 改：页脚版本戳推进（级联） |
| archive/docs/AGENTS-ARCHIVE.md | W1190 | 改：脚注沿革滚动（级联） |
| archive/docs/workflows-readme-history.md | W1190 | 改：逐批明细追加（级联） |
| scripts/output/INDEX.md | W1190 | 改：目录文档刷新（gen_folder_docs） |
| scripts/output/README.md | W1190 | 改：目录文档刷新（gen_folder_docs） |
| docs/00-导读/INDEX.md | W1190 | 改：目录文档刷新（gen_folder_docs） |
| docs/00-导读/README.md | W1190 | 改：目录文档刷新（gen_folder_docs） |
| xiyouji-agent-web/fuzz/INDEX.md | W1190 | 新建：fuzz 目录索引（目录文档） |
| xiyouji-agent-web/fuzz/README.md | W1190 | 新建：fuzz 目录说明（目录文档） |
| .github/INDEX.md | W1190 | 改：目录文档刷新（gen_folder_docs） |
| .github/workflows/INDEX.md | W1190 | 改：目录文档刷新（gen_folder_docs） |
| xiyouji-agent-web/INDEX.md | W1190 | 改：目录文档刷新（gen_folder_docs） |
| scripts/output/tools-inventory.md | W1190 | 改：工具清单刷新（gen_folder_docs） |
| docs/INDEX.md | W1190 | 改：docs 目录索引重建（docs_index.py） |
| scripts/output/stats-changelog.json | W1190 | 改：stats 变更记录刷新（stats.py） |
| scripts/output/stats-index.md | W1190 | 改：stats 索引刷新（stats.py） |
| docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md | W1190 | 改：stats 实体标记跟随（stats.py） |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1190 | 改：stats 实体标记跟随（stats.py） |
| scripts/output/_w1190_spec.json | W1190 | 新建：本批 spec |
| CHANGELOG.md | W1190 | 改：W1190 段（级联） |
| scripts/output/file-index.md | W1190 | 改：W1190 段（级联） |
| HANDOVER.md | W1190 | 改：最后更新行 + 当前进度（级联） |
| CITATION.cff | W1190 | 改：version/date 推进（级联） |
| .github/workflows/README.md | W1190 | 改：区间行推进（版本面） |
| scripts/output/_cascade_files_W1190.txt | W1190 | 新建：级联清单 |

## W1189 集成连通：A5 文化背景系列 ↔ 角色/器物文档 双向补链（2026-11-09）

| 文件 | W | 说明 |
|---|---|---|
| docs/04-文化与历史背景/金公木母与心猿意马称谓专题.md | W1189 | 改：前向补「关联角色」块（链孙悟空/猪八戒/沙僧/白龙马） |
| docs/04-文化与历史背景/八十一难与正果专题.md | W1189 | 改：前向补「关联角色」块（链唐僧/观音/孙悟空/猪八戒/沙僧/白龙马） |
| docs/04-文化与历史背景/天罡地煞与变化之术专题.md | W1189 | 改：前向补「关联角色」块（链孙悟空/猪八戒/沙僧/菩提祖师） |
| docs/04-文化与历史背景/法器与兵器器物体系专题.md | W1189 | 改：前向补「关联器物与角色」块（链金箍棒/芭蕉扇/紧箍/铁扇公主/太上老君/猪八戒） |
| docs/04-文化与历史背景/四大部洲与三界空间框架专题.md | W1189 | 改：前向补「关联角色」块（链孙悟空/如来） |
| docs/02-人物深度分析/孙悟空.md | W1189 | 改：反向补「关联文化背景」行（链金公木母/八十一难/天罡地煞/法器与兵器/四大部洲） |
| docs/02-人物深度分析/猪八戒.md | W1189 | 改：反向补「关联文化背景」行（链金公木母/八十一难/天罡地煞/法器与兵器） |
| docs/02-人物深度分析/沙僧.md | W1189 | 改：反向补「关联文化背景」行（链金公木母/八十一难） |
| docs/02-人物深度分析/白龙马.md | W1189 | 改：反向补「关联文化背景」行（链金公木母/八十一难） |
| docs/02-人物深度分析/唐僧.md | W1189 | 改：反向补「关联文化背景」行（链八十一难与正果） |
| docs/02-人物深度分析/观音.md | W1189 | 改：反向补「关联文化背景」行（链八十一难与正果） |
| docs/02-人物深度分析/菩提祖师.md | W1189 | 改：反向补「关联文化背景」行（链天罡地煞） |
| docs/02-人物深度分析/铁扇公主.md | W1189 | 改：反向补「关联文化背景」行（链法器与兵器） |
| docs/02-人物深度分析/太上老君.md | W1189 | 改：反向补「关联文化背景」行（链法器与兵器） |
| scripts/output/_w1189_spec.json | W1189 | 新建：本批 spec |
| CHANGELOG.md | W1189 | 改：W1189 段（级联） |
| docs/00-导读/W批次编号对账表.md | W1189 | 改：W1189 认领行 |
| site/index.html | W1189 | 改：页脚版本戳推进（级联） |
| scripts/output/file-index.md | W1189 | 改：W1189 段（级联） |
| scripts/output/stats.json | W1189 | 改：stats 刷新（级联） |
| scripts/output/INDEX.md | W1189 | 改：级联/目录刷新产物 |
| scripts/output/README.md | W1189 | 改：级联/目录刷新产物 |
| scripts/output/tools-inventory.md | W1189 | 改：级联/目录刷新产物 |
| scripts/output/_vermilion_solid_cache.json | W1189 | 改：级联/目录刷新产物 |
| site/data/cross-time-danmaku.html | W1189 | 改：级联/目录刷新产物 |
| site/data/tag-cloud.html | W1189 | 改：级联/目录刷新产物 |
| site/dukou-engine.html | W1189 | 改：级联/目录刷新产物 |
| scripts/output/_cascade_files_W1189.txt | W1189 | 新建：级联清单 |
| README.md | W1189 | 改：版本面推进（级联） |
| STRUCTURE.md | W1189 | 改：版本面推进（级联） |
| docs/00-导读/项目说明.md | W1189 | 改：版本面推进（级联） |
| HANDOVER.md | W1189 | 改：最后更新行 + 当前进度（级联） |
| AGENTS.md | W1189 | 改：级联/目录刷新产物 |
| CITATION.cff | W1189 | 改：version/date 推进（级联） |
| .github/workflows/README.md | W1189 | 改：区间行推进（版本面） |
| archive/docs/AGENTS-ARCHIVE.md | W1189 | 改：脚注沿革滚动（级联） |
| archive/docs/workflows-readme-history.md | W1189 | 改：逐批明细追加（W1189·级联） |

## W1188 读者路径验收与导航修复（2026-11-09）

| 文件 | W | 说明 |
|---|---|---|
| docs/04-文化与历史背景/金公木母与心猿意马称谓专题.md | W1188 | 改：补标准页脚（双索引/导航）修复读者返回路径 |
| docs/04-文化与历史背景/八十一难与正果专题.md | W1188 | 改：补标准页脚（双索引/导航）修复读者返回路径 |
| site/index.html | W1188 | 改：工具网格新增术语速查入口卡 + 注记去「两件」数词 |
| site/dashboard.html | W1188 | 改：标签云横幅旁新增术语速查横幅入口 |
| site/data/glossary.html | W1188 | 改：深度解读区小标题去旧批次口径（W1180–W1182→W1180–W1187） |
| scripts/output/_w1188_spec.json | W1188 | 新建：本批 spec |
| CHANGELOG.md | W1188 | 改：W1188 段（级联） |
| docs/00-导读/W批次编号对账表.md | W1188 | 改：W1188 认领行 |
| scripts/output/file-index.md | W1188 | 改：W1188 段（级联） |
| scripts/output/stats.json | W1188 | 改：stats 刷新（级联） |
| site/data/cross-time-danmaku.html | W1188 | 改：级联/目录刷新产物 |
| site/data/tag-cloud.html | W1188 | 改：级联/目录刷新产物 |
| site/dukou-engine.html | W1188 | 改：级联/目录刷新产物 |
| scripts/output/_cascade_files_W1188.txt | W1188 | 新建：级联清单 |
| README.md | W1188 | 改：版本面推进（级联） |
| STRUCTURE.md | W1188 | 改：版本面推进（级联） |
| docs/00-导读/项目说明.md | W1188 | 改：版本面推进（级联） |
| HANDOVER.md | W1188 | 改：最后更新行 + 当前进度（级联） |
| AGENTS.md | W1188 | 改：级联/目录刷新产物 |
| CITATION.cff | W1188 | 改：version/date 推进（级联） |
| .github/workflows/README.md | W1188 | 改：区间行推进（版本面） |
| archive/docs/AGENTS-ARCHIVE.md | W1188 | 改：脚注沿革滚动（级联） |
| archive/docs/workflows-readme-history.md | W1188 | 改：逐批明细追加（W1188·级联） |

## W1187 A5 佛教术语专题（2026-11-09）

| 文件 | W | 说明 |
|---|---|---|
| docs/04-文化与历史背景/八十一难与正果专题.md | W1187 | 新建：A5 佛教术语专题·9432 字符·8 条逐字核验引文·难簿与正果授职实证 |
| docs/04-文化与历史背景/README.md | W1187 | 改：系列段扩为 W1180–W1187 + 新增一行 |
| site/data/glossary.html | W1187 | 改：深度解读区加「二、佛教术语」反向入口 |
| docs/00-导读/统计口径说明.md | W1187 | 改：分板块表格 A5 41→42（合计 623） |
| site/dashboard.html | W1187 | 改：A5 KPI 卡片 41→42 + A1-A6 段落 622→623（第 68 槽） |
| docs/INDEX.md | W1187 | 改：docs_index.py 重建（868 篇·13 板块） |
| docs/00-导读/W批次编号对账表.md | W1187 | 改：W1187 认领行 |
| scripts/output/_w1187_spec.json | W1187 | 新建：本批 spec |
| scripts/output/_cascade_files_W1187.txt | W1187 | 新建：级联清单 |
| CHANGELOG.md | W1187 | 改：W1187 段落（级联） |
| scripts/output/file-index.md | W1187 | 改：W1187 段（级联） |
| site/data/search.html | W1187 | 改：搜索索引重生成（第 46 槽） |
| site/en/search.html | W1187 | 改：搜索索引重生成（同上） |
| README.md | W1187 | 改：A1-A6 计数标记跟随 + 版本行（级联） |
| STRUCTURE.md | W1187 | 改：版本行推进（级联） |
| HANDOVER.md | W1187 | 改：最后更新行 + 当前进度（级联） |
| .github/workflows/README.md | W1187 | 改：区间行推进（版本面） |
| CITATION.cff | W1187 | 改：version/date 推进（级联） |
| archive/docs/AGENTS-ARCHIVE.md | W1187 | 改：脚注沿革滚动（级联） |
| archive/docs/workflows-readme-history.md | W1187 | 改：逐批明细追加（W1187·级联） |
| docs/00-导读/项目说明.md | W1187 | 改：版本行推进（级禁） |
| scripts/output/stats.json | W1187 | 改：a5_docs 41→42 / a1_a6_docs 622→623 |
| scripts/output/INDEX.md | W1187 | 改：再生成/验证缓存（级联） |
| scripts/output/README.md | W1187 | 改：再生成/验证缓存（级联） |
| scripts/output/_vermilion_solid_cache.json | W1187 | 改：再生成/验证缓存（级联） |
| scripts/output/tools-inventory.md | W1187 | 改：再生成/验证缓存（级联） |
| AGENTS.md | W1187 | 改：级联/目录刷新产物 |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1187 | 改：级联/目录刷新产物 |
| docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md | W1187 | 改：级联/目录刷新产物 |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1187 | 改：级联/目录刷新产物 |
| docs/agent/gates.md | W1187 | 改：级联/目录刷新产物 |
| scripts/output/stats-changelog.json | W1187 | 改：级联/目录刷新产物 |
| scripts/output/stats-index.md | W1187 | 改：级联/目录刷新产物 |
| site/data/cross-time-danmaku.html | W1187 | 改：级联/目录刷新产物 |
| site/data/tag-cloud.html | W1187 | 改：级联/目录刷新产物 |
| site/dukou-engine.html | W1187 | 改：级联/目录刷新产物 |
| site/index.html | W1187 | 改：级联/目录刷新产物 |

## W1186 A5 人物称谓专题（2026-11-09）

| 文件 | W | 说明 |
|---|---|---|
| docs/04-文化与历史背景/金公木母与心猿意马称谓专题.md | W1186 | 新建：A5 人物称谓专题·11347 字符·6 条逐字核验引文·百回分布实算 |
| docs/04-文化与历史背景/README.md | W1186 | 改：系列段扩为 W1180–W1186 + 新增一行 |
| site/data/glossary.html | W1186 | 改：深度解读区加「一、人物称谓」反向入口 |
| docs/00-导读/统计口径说明.md | W1186 | 改：分板块表格 A5 40→41（合计 622） |
| site/dashboard.html | W1186 | 改：A5 KPI 卡片 40→41 + A1-A6 段落 621→622（第 68 槽） |
| docs/INDEX.md | W1186 | 改：docs_index.py 重建（867 篇·13 板块） |
| docs/00-导读/W批次编号对账表.md | W1186 | 改：W1186 认领行 |
| scripts/output/_w1186_spec.json | W1186 | 新建：本批 spec |
| scripts/output/_cascade_files_W1186.txt | W1186 | 新建：级联清单 |
| CHANGELOG.md | W1186 | 改：W1186 段落（级联） |
| scripts/output/file-index.md | W1186 | 改：W1186 段（级联） |
| site/data/search.html | W1186 | 改：搜索索引重生成（第 46 槽） |
| site/en/search.html | W1186 | 改：搜索索引重生成（同上） |
| README.md | W1186 | 改：A1-A6 计数标记跟随 + 版本行（级联） |
| STRUCTURE.md | W1186 | 改：版本行推进（级联） |
| HANDOVER.md | W1186 | 改：最后更新行 + 当前进度（级禁） |
| .github/workflows/README.md | W1186 | 改：区间行推进（版本面） |
| CITATION.cff | W1186 | 改：version/date 推进（级联） |
| archive/docs/AGENTS-ARCHIVE.md | W1186 | 改：脚注沿革滚动（级联） |
| archive/docs/workflows-readme-history.md | W1186 | 改：逐批明细追加（W1186·级联） |
| docs/00-导读/项目说明.md | W1186 | 改：版本行推进（级联） |
| scripts/output/stats.json | W1186 | 改：a5_docs 40→41 / a1_a6_docs 621→622 |
| scripts/output/INDEX.md | W1186 | 改：再生成/验证缓存（级联） |
| scripts/output/README.md | W1186 | 改：再生成/验证缓存（级联） |
| scripts/output/_vermilion_solid_cache.json | W1186 | 改：再生成/验证缓存（级联） |
| scripts/output/tools-inventory.md | W1186 | 改：再生成/验证缓存（级联） |
| AGENTS.md | W1186 | 改：级联/目录刷新产物 |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1186 | 改：级联/目录刷新产物 |
| docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md | W1186 | 改：级联/目录刷新产物 |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1186 | 改：级联/目录刷新产物 |
| docs/agent/gates.md | W1186 | 改：级联/目录刷新产物 |
| scripts/output/stats-changelog.json | W1186 | 改：级联/目录刷新产物 |
| scripts/output/stats-index.md | W1186 | 改：级联/目录刷新产物 |
| site/data/cross-time-danmaku.html | W1186 | 改：级联/目录刷新产物 |
| site/data/tag-cloud.html | W1186 | 改：级联/目录刷新产物 |
| site/dukou-engine.html | W1186 | 改：级联/目录刷新产物 |
| site/index.html | W1186 | 改：级联/目录刷新产物 |

## W1185 A5 章回套语专题（2026-11-09）

| 文件 | W | 说明 |
|---|---|---|
| docs/04-文化与历史背景/且听下回分解套语专题.md | W1185 | 新建：A5 章回套语专题·10879 字符·6 条逐字核验引文·百回分布实算 |
| docs/04-文化与历史背景/README.md | W1185 | 改：系列段扩为 W1180–W1185 + 新增一行 |
| site/data/glossary.html | W1185 | 改：深度解读区加「四、回目结构」反向入口 |
| docs/00-导读/统计口径说明.md | W1185 | 改：分板块表格 A5 39→40（合计 621） |
| site/dashboard.html | W1185 | 改：A5 KPI 卡片 39→40 + A1-A6 段落 620→621（第 68 槽） |
| docs/INDEX.md | W1185 | 改：docs_index.py 重建（866 篇·13 板块） |
| docs/00-导读/W批次编号对账表.md | W1185 | 改：W1185 认领行 |
| scripts/output/_w1185_spec.json | W1185 | 新建：本批 spec |
| scripts/output/_cascade_files_W1185.txt | W1185 | 新建：级联清单 |
| CHANGELOG.md | W1185 | 改：W1185 段落（级联） |
| scripts/output/file-index.md | W1185 | 改：W1185 段（级联） |
| site/data/search.html | W1185 | 改：搜索索引重生成（第 46 槽） |
| site/en/search.html | W1185 | 改：搜索索引重生成（同上） |
| README.md | W1185 | 改：A1-A6 计数标记跟随 + 版本行（级联） |
| STRUCTURE.md | W1185 | 改：版本行推进（级联） |
| HANDOVER.md | W1185 | 改：最后更新行 + 当前进度（级联） |
| .github/workflows/README.md | W1185 | 改：区间行推进（版本面） |
| CITATION.cff | W1185 | 改：version/date 推进（级联） |
| archive/docs/AGENTS-ARCHIVE.md | W1185 | 改：脚注沿革滚动（级联） |
| archive/docs/workflows-readme-history.md | W1185 | 改：逐批明细追加（W1185·级联） |
| docs/00-导读/项目说明.md | W1185 | 改：版本行推进（级联） |
| scripts/output/stats.json | W1185 | 改：a5_docs 39→40 / a1_a6_docs 620→621 |
| scripts/output/INDEX.md | W1185 | 改：再生成/验证缓存（级联） |
| scripts/output/README.md | W1185 | 改：再生成/验证缓存（级联） |
| scripts/output/_vermilion_solid_cache.json | W1185 | 改：再生成/验证缓存（级联） |
| scripts/output/tools-inventory.md | W1185 | 改：再生成/验证缓存（级联） |
| AGENTS.md | W1185 | 改：级联/目录刷新产物 |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1185 | 改：级联/目录刷新产物 |
| docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md | W1185 | 改：级联/目录刷新产物 |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1185 | 改：级联/目录刷新产物 |
| docs/agent/gates.md | W1185 | 改：级联/目录刷新产物 |
| scripts/output/stats-changelog.json | W1185 | 改：级联/目录刷新产物 |
| scripts/output/stats-index.md | W1185 | 改：级联/目录刷新产物 |
| site/data/cross-time-danmaku.html | W1185 | 改：级联/目录刷新产物 |
| site/data/tag-cloud.html | W1185 | 改：级联/目录刷新产物 |
| site/dukou-engine.html | W1185 | 改：级联/目录刷新产物 |
| site/index.html | W1185 | 改：级联/目录刷新产物 |

## W1184 A5 空间框架专题（2026-11-09）

| 文件 | W | 说明 |
|---|---|---|
| docs/04-文化与历史背景/四大部洲与三界空间框架专题.md | W1184 | 新建：A5 系列第 4 篇·12419 字符·9 条逐字核验引文 |
| docs/04-文化与历史背景/README.md | W1184 | 改：系列段扩为 W1180–W1184 + 新增 W1184 行 |
| site/data/glossary.html | W1184 | 改：深度解读区增第 4 条反向入口 |
| docs/00-导读/统计口径说明.md | W1184 | 改：分板块表格 A5 38→39（合计 620） |
| site/dashboard.html | W1184 | 改：A5 KPI 卡片 38→39 + A1-A6 段落 619→620（第 68 槽） |
| docs/INDEX.md | W1184 | 改：docs_index.py 重建（865 篇·13 板块） |
| docs/00-导读/W批次编号对账表.md | W1184 | 改：W1184 认领行 |
| scripts/output/_w1184_spec.json | W1184 | 新建：本批 spec |
| scripts/output/_cascade_files_W1184.txt | W1184 | 新建：级联清单 |
| CHANGELOG.md | W1184 | 改：W1184 段落（级联） |
| scripts/output/file-index.md | W1184 | 改：W1184 段（级联） |
| site/data/search.html | W1184 | 改：搜索索引重生成（第 46 槽） |
| site/en/search.html | W1184 | 改：搜索索引重生成（同上） |
| README.md | W1184 | 改：A1-A6 计数标记跟随 + 版本行（级联） |
| STRUCTURE.md | W1184 | 改：版本行推进（级联） |
| HANDOVER.md | W1184 | 改：最后更新行 + 当前进度（级联） |
| .github/workflows/README.md | W1184 | 改：区间行推进（版本面） |
| CITATION.cff | W1184 | 改：version/date 推进（级联） |
| archive/docs/AGENTS-ARCHIVE.md | W1184 | 改：脚注沿革滚动（级联） |
| archive/docs/workflows-readme-history.md | W1184 | 改：逐批明细追加（W1184·级联） |
| docs/00-导读/项目说明.md | W1184 | 改：版本行推进（级联） |
| scripts/output/stats.json | W1184 | 改：a5_docs 38→39 / a1_a6_docs 619→620 |
| scripts/output/INDEX.md | W1184 | 改：再生成/验证缓存（级联） |
| scripts/output/README.md | W1184 | 改：再生成/验证缓存（级联） |
| scripts/output/_vermilion_solid_cache.json | W1184 | 改：再生成/验证缓存（级联） |
| scripts/output/tools-inventory.md | W1184 | 改：再生成/验证缓存（级联） |
| AGENTS.md | W1184 | 改：级联/目录刷新产物 |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1184 | 改：级联/目录刷新产物 |
| docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md | W1184 | 改：级联/目录刷新产物 |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1184 | 改：级联/目录刷新产物 |
| docs/agent/gates.md | W1184 | 改：级联/目录刷新产物 |
| scripts/output/stats-changelog.json | W1184 | 改：级联/目录刷新产物 |
| scripts/output/stats-index.md | W1184 | 改：级联/目录刷新产物 |
| site/data/cross-time-danmaku.html | W1184 | 改：级联/目录刷新产物 |
| site/data/tag-cloud.html | W1184 | 改：级联/目录刷新产物 |
| site/dukou-engine.html | W1184 | 改：级联/目录刷新产物 |
| site/index.html | W1184 | 改：级联/目录刷新产物 |

## W1183 A5 系列收口批（2026-11-09）

| 文件 | W | 说明 |
|---|---|---|
| docs/04-文化与历史背景/README.md | W1183 | 改：新增「近期专题系列（W1180–W1182）」索引段 |
| docs/04-文化与历史背景/天罡地煞与变化之术专题.md | W1183 | 改：补「系列关联」段（→ W1181/W1182 + 板块 README） |
| docs/04-文化与历史背景/西游东传与译介专题.md | W1183 | 改：补「系列关联」段（→ W1180/W1182 + 板块 README） |
| scripts/new_page.py | W1183 | 改：render_template 增加 "static/→"../static/ 路径重写（图标链接根修） |
| site/data/glossary.html | W1183 | 改：新增「深度解读」区 + 修正 3 处图标相对路径 |
| site/data/cultural-misreading.html | W1183 | 改：新增「关联解读」行指向译介专题 |
| site/data/deconstruction.html | W1183 | 改：新增「关联解读」行指向译介专题 |
| docs/00-导读/W批次编号对账表.md | W1183 | 改：W1183 认领行 |
| scripts/output/_w1183_spec.json | W1183 | 新建：本批 spec |
| scripts/output/_cascade_files_W1183.txt | W1183 | 新建：级联清单 |
| CHANGELOG.md | W1183 | 改：W1183 段落（级联） |
| scripts/output/file-index.md | W1183 | 改：W1183 段（级联） |
| site/data/search.html | W1183 | 改：搜索索引重生成（第 46 槽） |
| site/en/search.html | W1183 | 改：搜索索引重生成（同上） |
| docs/INDEX.md | W1183 | 改：docs_index.py 重建 |
| README.md | W1183 | 改：版本行推进（级联） |
| STRUCTURE.md | W1183 | 改：版本行推进（级联） |
| HANDOVER.md | W1183 | 改：最后更新行 + 当前进度（级联） |
| .github/workflows/README.md | W1183 | 改：区间行推进（版本面） |
| CITATION.cff | W1183 | 改：version/date 推进（级联） |
| archive/docs/AGENTS-ARCHIVE.md | W1183 | 改：脚注沿革滚动（级联） |
| archive/docs/workflows-readme-history.md | W1183 | 改：逐批明细追加（W1183·级联） |
| docs/00-导读/项目说明.md | W1183 | 改：版本行推进（级联） |
| scripts/output/stats.json | W1183 | 改：stats 刷新（级联） |
| scripts/output/INDEX.md | W1183 | 改：再生成/验证缓存（级联） |
| scripts/output/README.md | W1183 | 改：再生成/验证缓存（级联） |
| scripts/output/_vermilion_solid_cache.json | W1183 | 改：再生成/验证缓存（级联） |
| scripts/output/tools-inventory.md | W1183 | 改：再生成/验证缓存（级联） |
| AGENTS.md | W1183 | 改：级联/目录刷新产物 |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1183 | 改：级联/目录刷新产物 |
| site/data/cross-time-danmaku.html | W1183 | 改：级联/目录刷新产物 |
| site/data/tag-cloud.html | W1183 | 改：级联/目录刷新产物 |
| site/dukou-engine.html | W1183 | 改：级联/目录刷新产物 |
| site/index.html | W1183 | 改：级联/目录刷新产物 |

## W1182 A5 文化专题第二篇（2026-11-09）

| 文件 | W | 说明 |
|---|---|---|
| docs/04-文化与历史背景/法器与兵器器物体系专题.md | W1182 | 新建：A5 文化专题第二篇·12990 字符·9 条逐字核验引文 |
| docs/00-导读/统计口径说明.md | W1182 | 改：分板块表格 A5 37→38（合计 619） |
| site/dashboard.html | W1182 | 改：A5 KPI 卡片 37→38 + A1-A6 段落 618→619（第 68 槽） |
| docs/INDEX.md | W1182 | 改：docs_index.py 重建（864 篇·13 板块） |
| docs/00-导读/W批次编号对账表.md | W1182 | 改：W1182 认领行 |
| scripts/output/_w1182_spec.json | W1182 | 新建：本批 spec |
| scripts/output/_cascade_files_W1182.txt | W1182 | 新建：级联清单 |
| CHANGELOG.md | W1182 | 改：W1182 段落（级联） |
| scripts/output/file-index.md | W1182 | 改：W1182 段（级联） |
| site/data/search.html | W1182 | 改：搜索索引重生成（第 46 槽） |
| site/en/search.html | W1182 | 改：搜索索引重生成（同上） |
| README.md | W1182 | 改：A1-A6 计数标记跟随 + 版本行（级联） |
| STRUCTURE.md | W1182 | 改：版本行推进（级联） |
| HANDOVER.md | W1182 | 改：最后更新行 + 当前进度（级联） |
| .github/workflows/README.md | W1182 | 改：区间行推进（版本面） |
| CITATION.cff | W1182 | 改：version/date 推进（级联） |
| archive/docs/AGENTS-ARCHIVE.md | W1182 | 改：脚注沿革滚动（级联） |
| archive/docs/workflows-readme-history.md | W1182 | 改：逐批明细追加（W1182·级联） |
| docs/00-导读/项目说明.md | W1182 | 改：版本行推进（级联） |
| scripts/output/stats.json | W1182 | 改：a5_docs 37→38 / a1_a6_docs 618→619 |
| scripts/output/INDEX.md | W1182 | 改：再生成/验证缓存（级联） |
| scripts/output/README.md | W1182 | 改：再生成/验证缓存（级联） |
| scripts/output/_vermilion_solid_cache.json | W1182 | 改：再生成/验证缓存（级联） |
| scripts/output/tools-inventory.md | W1182 | 改：再生成/验证缓存（级联） |
| AGENTS.md | W1182 | 改：级联/目录刷新产物 |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1182 | 改：级联/目录刷新产物 |
| docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md | W1182 | 改：级联/目录刷新产物 |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1182 | 改：级联/目录刷新产物 |
| docs/agent/gates.md | W1182 | 改：级联/目录刷新产物 |
| scripts/output/stats-changelog.json | W1182 | 改：级联/目录刷新产物 |
| scripts/output/stats-index.md | W1182 | 改：级联/目录刷新产物 |
| site/data/cross-time-danmaku.html | W1182 | 改：级联/目录刷新产物 |
| site/data/tag-cloud.html | W1182 | 改：级联/目录刷新产物 |
| site/dukou-engine.html | W1182 | 改：级联/目录刷新产物 |
| site/index.html | W1182 | 改：级联/目录刷新产物 |

## W1181 A5 文化专题（2026-11-09）

| 文件 | W | 说明 |
|---|---|---|
| docs/04-文化与历史背景/西游东传与译介专题.md | W1181 | 新建：A5 文化专题·14551 字符·4 条逐字核验引文·仅据索引已收录条目立论 |
| docs/00-导读/统计口径说明.md | W1181 | 改：分板块表格 A5 36→37（合计 618） |
| site/dashboard.html | W1181 | 改：A5 KPI 卡片 36→37 + A1-A6 段落 617→618（第 68 槽） |
| docs/INDEX.md | W1181 | 改：docs_index.py 重建（863 篇·13 板块） |
| docs/00-导读/W批次编号对账表.md | W1181 | 改：W1181 认领行 |
| scripts/output/_w1181_spec.json | W1181 | 新建：本批 spec |
| scripts/output/_cascade_files_W1181.txt | W1181 | 新建：级联清单 |
| CHANGELOG.md | W1181 | 改：W1181 段落（级联） |
| scripts/output/file-index.md | W1181 | 改：W1181 段（级联） |
| site/data/search.html | W1181 | 改：搜索索引重生成（第 46 槽） |
| site/en/search.html | W1181 | 改：搜索索引重生成（同上） |
| README.md | W1181 | 改：A1-A6 计数标记跟随 + 版本行（级联） |
| STRUCTURE.md | W1181 | 改：版本行推进（级联） |
| HANDOVER.md | W1181 | 改：最后更新行 + 当前进度（级联） |
| .github/workflows/README.md | W1181 | 改：区间行推进（版本面） |
| CITATION.cff | W1181 | 改：version/date 推进（级联） |
| archive/docs/AGENTS-ARCHIVE.md | W1181 | 改：脚注沿革滚动（级联） |
| archive/docs/workflows-readme-history.md | W1181 | 改：逐批明细追加（W1181·级联） |
| docs/00-导读/项目说明.md | W1181 | 改：版本行推进（级联） |
| scripts/output/stats.json | W1181 | 改：a5_docs 36→37 / a1_a6_docs 617→618 |
| scripts/output/INDEX.md | W1181 | 改：再生成/验证缓存（级联） |
| scripts/output/README.md | W1181 | 改：再生成/验证缓存（级联） |
| scripts/output/_vermilion_solid_cache.json | W1181 | 改：再生成/验证缓存（级联） |
| scripts/output/tools-inventory.md | W1181 | 改：再生成/验证缓存（级联） |
| AGENTS.md | W1181 | 改：级联/目录刷新产物 |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1181 | 改：级联/目录刷新产物 |
| docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md | W1181 | 改：级联/目录刷新产物 |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1181 | 改：级联/目录刷新产物 |
| docs/agent/gates.md | W1181 | 改：级联/目录刷新产物 |
| scripts/output/stats-changelog.json | W1181 | 改：级联/目录刷新产物 |
| scripts/output/stats-index.md | W1181 | 改：级联/目录刷新产物 |
| site/data/cross-time-danmaku.html | W1181 | 改：级联/目录刷新产物 |
| site/data/tag-cloud.html | W1181 | 改：级联/目录刷新产物 |
| site/dukou-engine.html | W1181 | 改：级联/目录刷新产物 |
| site/index.html | W1181 | 改：级联/目录刷新产物 |

## W1180 A5 内容深化首批（2026-11-09）

| 文件 | W | 说明 |
|---|---|---|
| docs/04-文化与历史背景/天罡地煞与变化之术专题.md | W1180 | 新建：A5 内容深化首批·14469 字符·8 条逐字核验引文 |
| docs/00-导读/统计口径说明.md | W1180 | 改：分板块表格 A5 34→36（合计与标题 617 一致） |
| scripts/agent_start.py | W1180 | 改：清单补第五类 new-doc + git add 顺序硬约束（自测 7/7） |
| AGENTS.md | W1180 | 改：§7 第 0 步「四类」→「五类」 |
| docs/00-导读/W批次编号对账表.md | W1180 | 改：W1180 认领行 |
| scripts/output/_w1180_spec.json | W1180 | 新建：本批 spec |
| scripts/output/_cascade_files_W1180.txt | W1180 | 新建：级联清单 |
| CHANGELOG.md | W1180 | 改：W1180 段落（级联） |
| scripts/output/file-index.md | W1180 | 改：W1180 段（级联） |
| site/data/search.html | W1180 | 改：搜索索引重生成（第 46 槽） |
| site/en/search.html | W1180 | 改：搜索索引重生成（同上） |
| README.md | W1180 | 改：A1-A6 计数标记跟随 + 版本行（级联） |
| STRUCTURE.md | W1180 | 改：版本行推进（级联） |
| HANDOVER.md | W1180 | 改：最后更新行 + 当前进度（级联） |
| .github/workflows/README.md | W1180 | 改：区间行推进（版本面） |
| CITATION.cff | W1180 | 改：version/date 推进（级联） |
| archive/docs/AGENTS-ARCHIVE.md | W1180 | 改：脚注沿革滚动（级联） |
| archive/docs/workflows-readme-history.md | W1180 | 改：逐批明细追加（W1180·级联） |
| docs/00-导读/项目说明.md | W1180 | 改：版本行推进（级联） |
| scripts/output/stats.json | W1180 | 改：a5_docs 35→36 / a1_a6_docs 616→617 |
| scripts/output/INDEX.md | W1180 | 改：再生成/验证缓存（级联） |
| scripts/output/README.md | W1180 | 改：再生成/验证缓存（级联） |
| scripts/output/_vermilion_solid_cache.json | W1180 | 改：再生成/验证缓存（级联） |
| scripts/output/tools-inventory.md | W1180 | 改：再生成/验证缓存（级联） |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1180 | 改：级联/目录刷新产物 |
| docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md | W1180 | 改：级联/目录刷新产物 |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1180 | 改：级联/目录刷新产物 |
| docs/agent/gates.md | W1180 | 改：级联/目录刷新产物 |
| scripts/output/stats-changelog.json | W1180 | 改：级联/目录刷新产物 |
| scripts/output/stats-index.md | W1180 | 改：级联/目录刷新产物 |
| site/data/cross-time-danmaku.html | W1180 | 改：级联/目录刷新产物 |
| site/data/tag-cloud.html | W1180 | 改：级联/目录刷新产物 |
| site/dukou-engine.html | W1180 | 改：级联/目录刷新产物 |
| site/index.html | W1180 | 改：级联/目录刷新产物 |
| docs/INDEX.md | W1180 | 改：第二轮修复产物 |
| site/dashboard.html | W1180 | 改：第二轮修复产物 |

## W1179 变更类型→必跑清单批（2026-11-09）

| 文件 | W | 说明 |
|---|---|---|
| scripts/agent_start.py | W1179 | 改：--task 输出四类必跑清单 + --checklist/--checklist-selftest；changed_entries 保留状态码；current_batch_w 与 next_batch_w 分离 |
| scripts/verify_delivery.py | W1179 | 改：_SCOPE_CORE 注释恒跑段计数 19→20（第 69 槽已入恒跑） |
| AGENTS.md | W1179 | 改：§7 第 0 步补 W1179 必跑清单用法 |
| docs/00-导读/W批次编号对账表.md | W1179 | 改：W1179 认领行 |
| scripts/output/_w1179_spec.json | W1179 | 新建：本批 spec |
| scripts/output/_cascade_files_W1179.txt | W1179 | 新建：级联清单 |
| CHANGELOG.md | W1179 | 改：W1179 段落（级联） |
| scripts/output/file-index.md | W1179 | 改：W1179 段（级联） |
| site/data/search.html | W1179 | 改：搜索索引重生成（AGENTS 文档改动·第 46 槽） |
| site/en/search.html | W1179 | 改：搜索索引重生成（同上） |
| .github/workflows/README.md | W1179 | 改：区间行推进（版本面） |
| CITATION.cff | W1179 | 改：version/date 推进（级联） |
| README.md | W1179 | 改：版本行推进（级联） |
| STRUCTURE.md | W1179 | 改：版本行推进（级联） |
| HANDOVER.md | W1179 | 改：最后更新行 + 当前进度（级联） |
| archive/docs/AGENTS-ARCHIVE.md | W1179 | 改：脚注沿革滚动（级联） |
| archive/docs/workflows-readme-history.md | W1179 | 改：逐批明细追加（W1179·级联） |
| docs/00-导读/项目说明.md | W1179 | 改：版本行推进（级联） |
| scripts/output/stats.json | W1179 | 改：stats 刷新（级联） |
| scripts/output/INDEX.md | W1179 | 改：再生成/验证缓存（级联） |
| scripts/output/README.md | W1179 | 改：再生成/验证缓存（级联） |
| scripts/output/_vermilion_solid_cache.json | W1179 | 改：再生成/验证缓存（级联） |
| scripts/output/tools-inventory.md | W1179 | 改：再生成/验证缓存（级联） |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1179 | 改：级联/目录刷新产物 |
| site/data/cross-time-danmaku.html | W1179 | 改：级联/目录刷新产物 |
| site/data/tag-cloud.html | W1179 | 改：级联/目录刷新产物 |
| site/dukou-engine.html | W1179 | 改：级联/目录刷新产物 |
| site/index.html | W1179 | 改：级联/目录刷新产物 |

## W1178 检索假阳性判据化批（2026-11-08）

| 文件 | W | 说明 |
|---|---|---|
| scripts/check_template_contract.py | W1178 | 新建：第 69 槽 · 模板结构契约与可复算检索证据 |
| scripts/verify_delivery.py | W1178 | 改：挂第 69 槽 _StrictGate |
| scripts/new_page.py | W1178 | 改：--post 追加第 8 步模板契约自检（run_post 接收 name） |
| AGENTS.md | W1178 | 改：§4.2 第 69 条 + 槽数三处 68→69 + 坑表计数 |
| docs/agent/gates.md | W1178 | 改：第 69 条（有序列表 + 详细定义）+ 标题槽数 |
| pitfalls.md | W1178 | 改：新增 E-212 + 流程段 172→173 |
| HANDOVER.md | W1178 | 改：槽数/坑表计数 + 最后更新行（级联） |
| .agent/skills/puti-shouye/SKILL.md | W1178 | 改：坑表计数 305→306 |
| docs/00-导读/W批次编号对账表.md | W1178 | 改：W1178 认领行 |
| scripts/output/_w1178_spec.json | W1178 | 新建：本批 spec |
| scripts/output/_cascade_files_W1178.txt | W1178 | 新建：级联清单 |
| CHANGELOG.md | W1178 | 改：W1178 段落（级联） |
| scripts/output/file-index.md | W1178 | 改：W1178 段（级联） |
| .github/workflows/README.md | W1178 | 改：区间行推进（版本面） |
| CITATION.cff | W1178 | 改：version/date 推进（级联） |
| README.md | W1178 | 改：版本行推进（级联） |
| STRUCTURE.md | W1178 | 改：版本行推进（级联） |
| archive/docs/AGENTS-ARCHIVE.md | W1178 | 改：脚注沿革滚动（级联） |
| archive/docs/workflows-readme-history.md | W1178 | 改：逐批明细追加（W1178·级联） |
| docs/00-导读/项目说明.md | W1178 | 改：版本行推进（级联） |
| scripts/output/stats.json | W1178 | 改：stats 刷新（级联） |
| scripts/output/INDEX.md | W1178 | 改：再生成/验证缓存（级联） |
| scripts/output/README.md | W1178 | 改：再生成/验证缓存（级联） |
| scripts/output/_vermilion_solid_cache.json | W1178 | 改：再生成/验证缓存（级联） |
| scripts/output/tools-inventory.md | W1178 | 改：再生成/验证缓存（级联） |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1178 | 改：级联/目录刷新产物 |
| archive/scripts/batches/w1176/INDEX.md | W1178 | 改：级联/目录刷新产物 |
| docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md | W1178 | 改：级联/目录刷新产物 |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1178 | 改：级联/目录刷新产物 |
| pytest.ini | W1178 | 改：级联/目录刷新产物 |
| scripts/INDEX.md | W1178 | 改：级联/目录刷新产物 |
| scripts/output/stats-changelog.json | W1178 | 改：级联/目录刷新产物 |
| scripts/output/stats-index.md | W1178 | 改：级联/目录刷新产物 |
| site/data/cross-time-danmaku.html | W1178 | 改：级联/目录刷新产物 |
| site/data/tag-cloud.html | W1178 | 改：级联/目录刷新产物 |
| site/dukou-engine.html | W1178 | 改：级联/目录刷新产物 |
| site/index.html | W1178 | 改：级联/目录刷新产物 |
| site/data/search.html | W1178 | 改：索引重生成产物 |
| site/en/search.html | W1178 | 改：索引重生成产物 |

## W1177 新增页上线自动化批（2026-11-08）

| 文件 | W | 说明 |
|---|---|---|
| scripts/new_page.py | W1177 | 改：加 --post/--batch，run_post 按依赖序跑七步（fail-fast）；description/cite 占位符替换 |
| site/_template.html | W1177 | 改：补 description / chart-degrade 声明 / div#dataSource 锚点 / cite-block HTML 结构 |
| docs/00-导读/W批次编号对账表.md | W1177 | 改：W1177 认领行 |
| scripts/output/_w1177_spec.json | W1177 | 新建：本批 spec |
| scripts/output/_cascade_files_W1177.txt | W1177 | 新建：级联清单 |
| CHANGELOG.md | W1177 | 改：W1177 段落（级联） |
| scripts/output/file-index.md | W1177 | 改：W1177 段（级联） |
| scripts/output/colorblind-baseline.txt | W1177 | 改：探针页增删后重冻结（终态回 18292） |
| site/sitemap.xml | W1177 | 改：探针页增删后重生成（终态回 855） |
| site/（2 件） | W1177 | 搜索索引重生成 + CSP 重哈希（探针页增删的终态） |
| .github/workflows/README.md | W1177 | 改：区间行推进（版本面） |
| CITATION.cff | W1177 | 改：version/date 推进（级联） |
| README.md | W1177 | 改：版本行推进（级联） |
| STRUCTURE.md | W1177 | 改：版本行推进（级联） |
| HANDOVER.md | W1177 | 改：最后更新行 + 当前进度（级联） |
| AGENTS.md | W1177 | 改：脚注沿革滚动（级联） |
| archive/docs/AGENTS-ARCHIVE.md | W1177 | 改：脚注沿革滚动（级联） |
| archive/docs/workflows-readme-history.md | W1177 | 改：逐批明细追加（W1177·级联） |
| docs/00-导读/项目说明.md | W1177 | 改：版本行推进（级联） |
| scripts/output/stats.json | W1177 | 改：stats 刷新（级联） |
| scripts/output/INDEX.md | W1177 | 改：再生成/验证缓存（级联） |
| scripts/output/README.md | W1177 | 改：再生成/验证缓存（级联） |
| scripts/output/_vermilion_solid_cache.json | W1177 | 改：再生成/验证缓存（级联） |
| scripts/output/tools-inventory.md | W1177 | 改：再生成/验证缓存（级联） |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1177 | 改：级联/修复产物 |
| archive/scripts/batches/w1175/INDEX.md | W1177 | 改：级联/修复产物 |
| scripts/output/_w1167_nav_plan.json | W1177 | 改：级联/修复产物 |
| scripts/_w1176_glossary_page.py | W1177 | 删：W1176 一次性脚本归档迁入 archive/scripts/batches/w1176/ |
| archive/scripts/batches/w1176/_w1176_glossary_page.py | W1177 | 新建：归档 |
| archive/scripts/batches/INDEX.md | W1177 | 改：归档产物 |
| archive/scripts/batches/README.md | W1177 | 改：归档产物 |
| archive/scripts/batches/w1176/INDEX.md | W1177 | 改：归档产物 |
| archive/scripts/batches/w1176/README.md | W1177 | 改：归档产物 |
| scripts/INDEX.md | W1177 | 改：归档产物 |

> **维护契约**：本索引按 W 追加登记（每文件 1 行 + 一句摘要），历史段禁改；新增/变更文件必须先有 CHANGELOG 对应 W 段再登记（双索引铁律），禁止无 W 段单独登记。
