# xiyouji 文件反向索引

> 与 [CHANGELOG.md](../../CHANGELOG.md) 配套：给定文件，查它被改过几次、每次对应哪个 W 条目。
> W### 编号规则见 CHANGELOG.md 顶部。
> 创建于 2026-07-22（v0.8 双索引改造）
>
> **历史归档**：W031-W087（v2.0.4-v2.0.60）site/data/ 部分已迁移至 [file-index-ARCHIVE.md](../../archive/docs/file-index-ARCHIVE.md)；W422 再归档 W393-W416 段；W511 归档 W417-W448 段 + W449-W463 损坏区尾部清理。W736 归档 W449-W699 段（与 CHANGELOG 现役边界统一至 W700）。本文件正本按 110 段窗滚动（W960 窗口制·正本最老段随批推进）。
>
> **维护契约**：本索引按 W 追加登记（每文件 1 行 + 一句摘要），历史段禁改；新增/变更文件必须先有 CHANGELOG 对应 W 段再登记（双索引铁律），禁止无 W 段单独登记。

---


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

## W953 themes 库专题题图批（12 张）（2026-10-26）

| 文件 | W | 说明 |
|---|---|---|
| site/static/images/plate-line-01-zhenjia-meihouwang.webp | W953 | 新增·真假美猴王专题 |
| site/static/images/plate-line-02-pantao-yuan.webp | W953 | 新增·蟠桃园-体制内的秘密 |
| site/static/images/plate-line-03-danaotian-gong.webp | W953 | 新增·大闹天宫-英雄还是悲剧 |
| site/static/images/plate-line-04-shuilandong.webp | W953 | 新增·水帘洞专题 |
| site/static/images/plate-line-05-hunshi-sihou.webp | W953 | 新增·混世四猴专题 |
| site/static/images/plate-line-06-bingqi-xiuyang.webp | W953 | 新增·兵器的自我修养专题 |
| site/static/images/plate-line-07-ershiba-xingsu.webp | W953 | 新增·二十八星宿专题 |
| site/static/images/plate-line-08-sizhi-gongcao.webp | W953 | 新增·四值功曹专题 |
| site/static/images/plate-line-09-wufang-jiedi.webp | W953 | 新增·五方揭谛专题 |
| site/static/images/plate-line-10-liuding-liujia.webp | W953 | 新增·六丁六甲专题 |
| site/static/images/plate-line-11-jingubang-zhongliang.webp | W953 | 新增·金箍棒的重量专题 |
| site/static/images/plate-line-12-qiwu-zhuanji.webp | W953 | 新增·器物传记学专题 |
| site/reader/themes/真假美猴王专题.html | W953 | 接入题图（真假美猴王专题） |
| site/reader/themes/蟠桃园-体制内的秘密.html | W953 | 接入题图（蟠桃园-体制内的秘密） |
| site/reader/themes/大闹天宫-英雄还是悲剧.html | W953 | 接入题图（大闹天宫-英雄还是悲剧） |
| site/reader/themes/水帘洞专题.html | W953 | 接入题图（水帘洞专题） |
| site/reader/themes/混世四猴专题.html | W953 | 接入题图（混世四猴专题） |
| site/reader/themes/兵器的自我修养专题.html | W953 | 接入题图（兵器的自我修养专题） |
| site/reader/themes/二十八星宿专题.html | W953 | 接入题图（二十八星宿专题） |
| site/reader/themes/四值功曹专题.html | W953 | 接入题图（四值功曹专题） |
| site/reader/themes/五方揭谛专题.html | W953 | 接入题图（五方揭谛专题） |
| site/reader/themes/六丁六甲专题.html | W953 | 接入题图（六丁六甲专题） |
| site/reader/themes/金箍棒的重量-一万三千五百斤的秘密.html | W953 | 接入题图（金箍棒的重量专题） |
| site/reader/themes/器物传记学专题.html | W953 | 接入题图（器物传记学专题） |
| assets/promo/plate-set/ | W953 | 母版 + 站点版 + 拼图 + README（累计 40 张） |
| scripts/_w953_make_prompts.py | W953 | 母版复用生成器（读上批 JSON 取母版·断言逐字一致） |
| scripts/_w953_insert_plates.py | W953 | 12 页 chapter-plate 接入（幂等） |
| scripts/_w953_cascade.py | W953 | 四面登记 + 当前态指针（共享面精确暂存·文件行自动生成） |
| scripts/output/_w953_batch1~3.json | W953 | 出图参数 12 条 |
| scripts/output/_cascade_files_W953.txt | W953 | 当批级联清单 |
| CHANGELOG.md | W953 | W953 版段 |
| docs/00-导读/W批次编号对账表.md | W953 | W953 认领行 |

## W952 内页人物题图续批第二组（12 张·人物+主题混合）（2026-10-25）

| 文件 | W | 说明 |
|---|---|---|
| site/static/images/plate-line-01-bailongma.webp | W952 | 新增·白龙马 |
| site/static/images/plate-line-02-dujiao-shengwang.webp | W952 | 新增·独角兕大王 |
| site/static/images/plate-line-03-linggan.webp | W952 | 新增·灵感大王 |
| site/static/images/plate-line-04-huangfengguai.webp | W952 | 新增·黄风怪 |
| site/static/images/plate-line-05-saitaisui.webp | W952 | 新增·赛太岁 |
| site/static/images/plate-line-06-jiuLingyuansheng.webp | W952 | 新增·九灵元圣 |
| site/static/images/plate-line-07-nezha.webp | W952 | 新增·哪吒 |
| site/static/images/plate-line-08-angrixingguan.webp | W952 | 新增·昴日星官 |
| site/static/images/plate-line-09-jingu-topic.webp | W952 | 新增·紧箍咒专题 |
| site/static/images/plate-line-10-jindouyun-topic.webp | W952 | 新增·筋斗云专题 |
| site/static/images/plate-line-11-fabao-topic.webp | W952 | 新增·法宝系统专题 |
| site/static/images/plate-line-12-wuzi-jing-topic.webp | W952 | 新增·无字真经专题 |
| site/reader/people/白龙马.html | W952 | 接入题图（白龙马） |
| site/reader/people/独角兕大王.html | W952 | 接入题图（独角兕大王） |
| site/reader/people/灵感大王.html | W952 | 接入题图（灵感大王） |
| site/reader/people/黄风怪外传.html | W952 | 接入题图（黄风怪） |
| site/reader/people/赛太岁.html | W952 | 接入题图（赛太岁） |
| site/reader/people/九灵元圣-方向二深化.html | W952 | 接入题图（九灵元圣） |
| site/reader/people/哪吒.html | W952 | 接入题图（哪吒） |
| site/reader/people/昴日星官.html | W952 | 接入题图（昴日星官） |
| site/reader/themes/紧箍咒专题.html | W952 | 接入题图（紧箍咒主题） |
| site/reader/themes/筋斗云专题.html | W952 | 接入题图（筋斗云主题） |
| site/reader/themes/法宝系统专题.html | W952 | 接入题图（法宝系统主题） |
| site/reader/themes/无字真经专题.html | W952 | 接入题图（无字真经主题） |
| assets/promo/plate-set/ | W952 | 母版 + 站点版 + 拼图 + README（累计 28 张） |
| scripts/_w952_make_prompts.py | W952 | 母版复用生成器 + 两条断言（批内一致 / 风格段与上批一致） |
| scripts/_w952_insert_plates.py | W952 | 12 页 chapter-plate 接入（幂等） |
| scripts/_w952_cascade.py | W952 | 四面登记 + 当前态指针（共享面精确暂存） |
| scripts/_w945_plates_verify.py | W952 | J2 顶部留白带口径 28% → 10%（新旧两批交集） |
| scripts/output/_w952_batch1~3.json | W952 | 出图参数 12 条 |
| CHANGELOG.md | W952 | W952 版段 |
| docs/00-导读/W批次编号对账表.md | W952 | W952 认领行 |

## W951 题图版式批（站点版裁掉上部留白·16 张）（2026-10-25）

| 文件 | W | 说明 |
|---|---|---|
| site/static/images/plate-line-0[1-8]-*.webp | W951 | 16 张站点版重出（只裁上部留白·主体顶对齐 6 px·保留下部地面留白） |
| assets/promo/plate-set/plate-line-*.png / *.webp | W951 | 完整母版 16 张（1200×1600·含上部留白·供卡片叠字用） |
| assets/promo/plate-set/preview-site-sheet.png / .webp | W951 | 站点版拼图（16 张·页面实际呈现） |
| assets/promo/plate-set/README.md | W951 | 资产分层说明 + 四版方案迭代记录 |
| scripts/_w951_check_crop.py | W951 | 站点版验算判据（主体顶/底未切 + 地面留白 > 0） |
| scripts/_w951_site_sheet.py | W951 | 站点版拼图生成器 |
| scripts/_w945_prepare.py | W951 | 站点版生成逻辑改为「只裁上部留白·保留下部地面留白」 |
| scripts/_w951_cascade.py | W951 | 四面登记 + 当前态指针（含共享面精确暂存） |
| scripts/output/_cascade_files_W951.txt | W951 | 当批级联清单 |
| CHANGELOG.md | W951 | W951 版段 |
| docs/00-导读/W批次编号对账表.md | W951 | W951 认领行 |

## W950 图标集打磨优化批（重画 13 枚 + 光学尺寸归一 + 1967 处内联 SVG 图形同步 + 唯一事实源刷新器）
（2026-10-25）

| 文件 | W | 说明 |
|---|---|---|
| site/static/icons/ui/（45 枚 SVG 资产重生成） | W950 | 批次产物（据 CHANGELOG W950 段「文件」字段补录） |
| scripts/_w939_gen_icons.py | W950 | 批次产物（据 CHANGELOG W950 段「文件」字段补录） |
| scripts/_w946_gen_timeline_icons.py（生成器接入归一参数） | W950 | 批次产物（据 CHANGELOG W950 段「文件」字段补录） |
| scripts/_w950_normalize.py（新增·光学尺寸归一器） | W950 | 批次产物（据 CHANGELOG W950 段「文件」字段补录） |
| scripts/_w950_refresh_icon_paths.py（新增·图形同步刷新器） | W950 | 批次产物（据 CHANGELOG W950 段「文件」字段补录） |
| scripts/output/_w950_icon_normalize.json（新增·45 枚归一参数） | W950 | 批次产物（据 CHANGELOG W950 段「文件」字段补录） |
| scripts/output/_w946_timeline_icons.js | W950 | 批次产物（据 CHANGELOG W950 段「文件」字段补录） |
| scripts/output/_cascade_files_W950.txt | W950 | 批次产物（据 CHANGELOG W950 段「文件」字段补录） |
| xiyouji-agent-web/src/components/UiIcons.tsx（由资产重建） | W950 | 批次产物（据 CHANGELOG W950 段「文件」字段补录） |
| site/**（1967 处内联 SVG 图形同步 · 646 个文件） | W950 | 批次产物（据 CHANGELOG W950 段「文件」字段补录） |
| docs/11-方案报告/计划方案/T26-任务计划执行与经验沉淀报告-2026-10-25.md | W950 | 批次产物（据 CHANGELOG W950 段「文件」字段补录） |
| docs/00-导读/W批次编号对账表.md | W950 | 批次产物（据 CHANGELOG W950 段「文件」字段补录） |
| CHANGELOG.md | W950 | 批次产物（据 CHANGELOG W950 段「文件」字段补录） |
| HANDOVER.md | W950 | 批次产物（据 CHANGELOG W950 段「文件」字段补录） |
| README.md | W950 | 批次产物（据 CHANGELOG W950 段「文件」字段补录） |
| STRUCTURE.md | W950 | 批次产物（据 CHANGELOG W950 段「文件」字段补录） |
| docs/00-导读/项目说明.md | W950 | 批次产物（据 CHANGELOG W950 段「文件」字段补录） |
| CITATION.cff。 | W950 | 批次产物（据 CHANGELOG W950 段「文件」字段补录） |

## W949 图标治理换路径复核批（第二次追问「确定做完了吗」· 堵数据源回归漏洞 + 字段图标位判据入机检 + 登记剩余 71 条）
（2026-10-25）

| 文件 | W | 说明 |
|---|---|---|
| dataset/timeline.json（数据源 22 个 icon 字段 emoji → 图标名） | W949 | 批次产物（据 CHANGELOG W949 段「文件」字段补录） |
| scripts/_w949_fix_dataset.py | W949 | 批次产物（据 CHANGELOG W949 段「文件」字段补录） |
| scripts/_w949_allowlist.py | W949 | 批次产物（据 CHANGELOG W949 段「文件」字段补录） |
| scripts/check_icon_fields.py（字段图标位判据） | W949 | 批次产物（据 CHANGELOG W949 段「文件」字段补录） |
| scripts/check_emoji_icons.py（第 50 门禁挂入 A2 段） | W949 | 批次产物（据 CHANGELOG W949 段「文件」字段补录） |
| scripts/output/_w949_icon_field_allowlist.json | W949 | 批次产物（据 CHANGELOG W949 段「文件」字段补录） |
| docs/11-方案报告/计划方案/T26-任务计划执行与经验沉淀报告-2026-10-25.md | W949 | 批次产物（据 CHANGELOG W949 段「文件」字段补录） |
| docs/00-导读/W批次编号对账表.md | W949 | 批次产物（据 CHANGELOG W949 段「文件」字段补录） |
| CHANGELOG.md | W949 | 批次产物（据 CHANGELOG W949 段「文件」字段补录） |
| HANDOVER.md | W949 | 批次产物（据 CHANGELOG W949 段「文件」字段补录） |
| README.md | W949 | 批次产物（据 CHANGELOG W949 段「文件」字段补录） |
| STRUCTURE.md | W949 | 批次产物（据 CHANGELOG W949 段「文件」字段补录） |
| docs/00-导读/项目说明.md | W949 | 批次产物（据 CHANGELOG W949 段「文件」字段补录） |
| CITATION.cff。 | W949 | 批次产物（据 CHANGELOG W949 段「文件」字段补录） |

## W948 内页专题题图续批（8 张线描人物题图·累计 16 张）（2026-10-25）

| 文件 | W | 说明 |
|---|---|---|
| site/static/images/plate-line-01-jinjiao.webp | W948 | 新增·金角大王（紫金红葫芦 + 朱红封带） |
| site/static/images/plate-line-02-niumowang.webp | W948 | 新增·牛魔王（牛首 + 混铁棍） |
| site/static/images/plate-line-03-tieshanggongzhu.webp | W948 | 新增·铁扇公主（叶形芭蕉扇） |
| site/static/images/plate-line-04-xiezi.webp | W948 | 新增·蝎子精（上翘蝎尾毒钩 + 倒马毒桩） |
| site/static/images/plate-line-05-huangpaoguai.webp | W948 | 新增·黄袍怪（狼首 + 金钢琢） |
| site/static/images/plate-line-06-zhenyuan.webp | W948 | 新增·镇元大仙（人参果 + 拂尘） |
| site/static/images/plate-line-07-dapeng.webp | W948 | 新增·大鹏金翅雕（鹏翼 + 阴阳二气瓶） |
| site/static/images/plate-line-08-taishanglaojun.webp | W948 | 新增·太上老君（太极图 + 拂尘） |
| assets/promo/plate-set/ | W948 | 成品 16 张 + raw/round4 原件 + README 扩写 + 拼图 |
| scripts/_w948_make_prompts.py | W948 | 母版逐字复用生成器（读上批 JSON 取母版） |
| scripts/_w948_insert_plates.py | W948 | 8 页 chapter-plate 接入（幂等） |
| scripts/_w948_cascade.py | W948 | 四面登记 + 当前态指针 |
| scripts/_w945_plates_verify.py | W948 | 判据扩面：写死清单 → 目录扫描（16 张） |
| scripts/output/_w948_batch1.json | W948 | 出图参数 01–04 |
| scripts/output/_w948_batch2.json | W948 | 出图参数 05–08 |
| CHANGELOG.md | W948 | W948 版段 |
| docs/00-导读/W批次编号对账表.md | W948 | W948 认领行 |

## W947 图标治理复验与补治批（用户追问「你确定现在已经做完图标了吗」→ 三路全量复验 + 补治两处遗漏范围 + 更正一处误判）
（2026-10-25）

| 文件 | W | 说明 |
|---|---|---|
| scripts/_w947_add_icons.py（通用图标集补 2 枚） | W947 | 批次产物（据 CHANGELOG W947 段「文件」字段补录） |
| scripts/_w939_gen_icons.py（并入 note / link） | W947 | 批次产物（据 CHANGELOG W947 段「文件」字段补录） |
| site/static/icons/ui/note.svg | W947 | 批次产物（据 CHANGELOG W947 段「文件」字段补录） |
| site/static/icons/ui/link.svg | W947 | 批次产物（据 CHANGELOG W947 段「文件」字段补录） |
| site/static/js/rag-chat.js（🔗 前缀 → 内联 SVG） | W947 | 批次产物（据 CHANGELOG W947 段「文件」字段补录） |
| xiyouji-agent-web/src/components/UiIcons.tsx（新建·内联 SVG 图标组件） | W947 | 批次产物（据 CHANGELOG W947 段「文件」字段补录） |
| xiyouji-agent-web/src/components/PermissionDialog.tsx（⚠️ 📝 → 组件） | W947 | 批次产物（据 CHANGELOG W947 段「文件」字段补录） |
| xiyouji-agent-web/src/components/InlinePermissionCard.tsx（⚠️ → 组件） | W947 | 批次产物（据 CHANGELOG W947 段「文件」字段补录） |
| scripts/check_emoji_icons.py（标题改号） | W947 | 批次产物（据 CHANGELOG W947 段「文件」字段补录） |
| docs/11-方案报告/计划方案/T26-任务计划执行与经验沉淀报告-2026-10-25.md | W947 | 批次产物（据 CHANGELOG W947 段「文件」字段补录） |
| docs/00-导读/W批次编号对账表.md | W947 | 批次产物（据 CHANGELOG W947 段「文件」字段补录） |
| CHANGELOG.md | W947 | 批次产物（据 CHANGELOG W947 段「文件」字段补录） |
| HANDOVER.md | W947 | 批次产物（据 CHANGELOG W947 段「文件」字段补录） |
| README.md | W947 | 批次产物（据 CHANGELOG W947 段「文件」字段补录） |
| STRUCTURE.md | W947 | 批次产物（据 CHANGELOG W947 段「文件」字段补录） |
| docs/00-导读/项目说明.md | W947 | 批次产物（据 CHANGELOG W947 段「文件」字段补录） |
| CITATION.cff。 | W947 | 批次产物（据 CHANGELOG W947 段「文件」字段补录） |

## W946 图标治理续作批（.ico 描边参数修复 + 时间线专属图标 16 枚 + 第 50 门禁「UI 图标位零残留 · 图标渲染正确性」）
（2026-10-25）

| 文件 | W | 说明 |
|---|---|---|
| site/system.css（`.ico` 基类补 fill/stroke/linecap/linejoin 描边参数） | W946 | 批次产物（据 CHANGELOG W946 段「文件」字段补录） |
| site/static/icons/ui/tl-*.svg（16 枚时间线专属图标） | W946 | 批次产物（据 CHANGELOG W946 段「文件」字段补录） |
| site/data/timeline.html | W946 | 批次产物（据 CHANGELOG W946 段「文件」字段补录） |
| site/en/timeline.html（22 条事件数据字段 + 渲染改内联 SVG + TL_ICO 映射内联 + CSP 重算） | W946 | 批次产物（据 CHANGELOG W946 段「文件」字段补录） |
| scripts/_w946_gen_timeline_icons.py | W946 | 批次产物（据 CHANGELOG W946 段「文件」字段补录） |
| scripts/_w946_apply_timeline_icons.py | W946 | 批次产物（据 CHANGELOG W946 段「文件」字段补录） |
| scripts/check_emoji_icons.py（第 50 门禁） | W946 | 批次产物（据 CHANGELOG W946 段「文件」字段补录） |
| scripts/_w939_emoji_to_svg.py（svg_tag 模板补 SVG 属性） | W946 | 批次产物（据 CHANGELOG W946 段「文件」字段补录） |
| scripts/output/_w946_timeline_icons.js | W946 | 批次产物（据 CHANGELOG W946 段「文件」字段补录） |
| docs/11-方案报告/计划方案/T26-任务计划执行与经验沉淀报告-2026-10-25.md | W946 | 批次产物（据 CHANGELOG W946 段「文件」字段补录） |
| docs/00-导读/W批次编号对账表.md | W946 | 批次产物（据 CHANGELOG W946 段「文件」字段补录） |
| CHANGELOG.md | W946 | 批次产物（据 CHANGELOG W946 段「文件」字段补录） |
| HANDOVER.md | W946 | 批次产物（据 CHANGELOG W946 段「文件」字段补录） |
| README.md | W946 | 批次产物（据 CHANGELOG W946 段「文件」字段补录） |
| STRUCTURE.md | W946 | 批次产物（据 CHANGELOG W946 段「文件」字段补录） |
| docs/00-导读/项目说明.md | W946 | 批次产物（据 CHANGELOG W946 段「文件」字段补录） |
| scripts/output/file-index.md。 | W946 | 批次产物（据 CHANGELOG W946 段「文件」字段补录） |

## W945 内页专题题图成套（8 张 3:4 线描人物题图）（2026-10-25）

| 文件 | W | 说明 |
|---|---|---|
| site/static/images/plate-line-01-wukong.webp | W945 | 新增·大圣悟空（金箍棒 + 凤翅紫金冠） |
| site/static/images/plate-line-02-tangseng.webp | W945 | 新增·唐僧（五佛冠 + 念珠 + 九环锡杖） |
| site/static/images/plate-line-03-bajie.webp | W945 | 新增·猪八戒（九齿钉耙 + 蒲扇耳） |
| site/static/images/plate-line-04-shaseng.webp | W945 | 新增·沙僧（降妖宝杖 + 骷髅念珠） |
| site/static/images/plate-line-05-guanyin.webp | W945 | 新增·观音（玉净瓶插杨柳 + 莲座） |
| site/static/images/plate-line-06-erlangshen.webp | W945 | 新增·二郎神（三尖两刃刀 + 额间竖目） |
| site/static/images/plate-line-07-baigujing.webp | W945 | 新增·白骨精（三变残影） |
| site/static/images/plate-line-08-honghaier.webp | W945 | 新增·红孩儿（火尖枪 + 三昧真火） |
| assets/promo/plate-set/ | W945 | 出图原件 + 逐张清单 + J8 自检表 + 拼图 |
| scripts/_w945_plates_verify.py | W945 | J1–J7 机器判据 + J8 题材自检表 |
| scripts/_w945_insert_plates.py | W945 | 8 页 chapter-plate 接入（幂等） |
| scripts/_w945_cascade.py | W945 | 四面登记 + 当前态指针 |
| CHANGELOG.md | W945 | W945 版段 |
| docs/00-导读/W批次编号对账表.md | W945 | W945 认领行 |

## W944 章回插画新组（6 张按回目情节重出）（2026-10-25）

| 文件 | W | 说明 |
|---|---|---|
| site/static/images/chap-07.webp | W944 | 重出·第 007 回 八卦炉（三足丹炉 + 火焰） |
| site/static/images/chap-14.webp | W944 | 重出·第 014 回 心猿归正（猴形剪影 + 金箍 + 勒绳） |
| site/static/images/chap-15.webp | W944 | 重出·第 015 回 鹰愁涧（惊马扬蹄 + 缰绳 + 瀑布崖） |
| site/static/images/chap-23.webp | W944 | 重出·第 023 回 四圣试禅心（打坐僧 + 孤灯 + 雾中两影·去黑框） |
| site/static/images/chap-27.webp | W944 | 重出·第 027 回 尸魔三戏（三道人影渐次消散 + 月 + 茅屋） |
| site/static/images/chap-30.webp | W944 | 重出·第 030 回 邪魔侵正法（蛇形妖影 + 洞口 + 螺旋墨风） |
| scripts/_w944_cascade.py | W944 | 四面登记 + 当前态指针 |
| CHANGELOG.md | W944 | W944 版段（四件套） |
| docs/00-导读/W批次编号对账表.md | W944 | W944 认领行 |

## W943 全站图片审查（227 张逐类目视·修 3 处真缺陷）（2026-10-25）

| 文件 | W | 说明 |
|---|---|---|
| site/static/images/og-15-shijian-liejian.webp | W943 | 重出（线上分享图·去掉抽象墨块中 3 处「LI」字母残留） |
| assets/design/ai-concepts/concept-03-scroll.png | W943 | 重出（去掉卷面潦草伪汉字·改空白纸面 + 抽象笔触） |
| assets/design/ai-concepts/concept-06-bodhi-leaf.png | W943 | 重出（菩提叶形制：水滴 / 火苗形 → 心形叶 + 中脉分叉叶脉 + 叶柄 + 露珠） |
| scripts/_w943_cascade.py | W943 | 四面登记 + 当前态指针 |
| CHANGELOG.md | W943 | W943 版段（四件套） |
| docs/00-导读/W批次编号对账表.md | W943 | W943 认领行 |

## W942 Hero 素材全量复审（14 张逐张放大目视·修正 2 处形制偏差）（2026-10-25）

| 文件 | W | 说明 |
|---|---|---|
| assets/promo/hero-set/hero-line-04-tight-crown.png | W942 | 重出「紧箍儿」母版（金圈内缘补足九个倒刺钩） |
| assets/promo/hero-set/hero-line-04-tight-crown.webp | W942 | 同上 WebP |
| assets/promo/hero-set/hero-line-07-banana-fan.png | W942 | 重出「芭蕉扇」母版（正圆团扇 → 叶形扇 + 中脉细脉 + 短柄缠绳） |
| assets/promo/hero-set/hero-line-07-banana-fan.webp | W942 | 同上 WebP |
| assets/promo/hero-set/raw/hero-04c-tight-crown.jpg | W942 | 紧箍儿重出原件 |
| assets/promo/hero-set/raw/hero-07c-banana-fan.jpg | W942 | 芭蕉扇重出原件 |
| assets/promo/hero-set/preview-contact-sheet.png | W942 | 9 张成套拼图刷新 |
| assets/promo/hero-set/README.md | W942 | J8 自检表细化到形制级（倒刺钩数 / 扇形 / 环数 / 瓶插枝） |
| site/static/images/hero-line-04-tight-crown.webp | W942 | 站点版重出（带九倒刺） |
| site/static/images/hero-line-07-banana-fan.webp | W942 | 站点版重出（叶形扇） |
| scripts/_w942_cascade.py | W942 | 四面登记 + 自检表更新 + 当前态指针 |
| CHANGELOG.md | W942 | W942 版段（四件套） |
| docs/00-导读/W批次编号对账表.md | W942 | W942 认领行 |

## W941 UI 图标位 emoji 治理批（2026-10-25）

| 文件 | W | 说明 |
|---|---|---|
| site/data/81-hardships-view.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/data/81-hardships.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/data/_shell.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/data/aesthetics.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/data/ai-dialogue.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/data/business-model.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/data/cave-estate.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/data/century-dialogue.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/data/chapter-stats.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/data/chapter-structure-graph.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/data/character-appearance.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/data/character-dynamic-network.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/data/character-presence-timeline.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/data/character-relationship-3d-view.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/data/character-relationship-3d.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/data/character-semantic-network.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/data/character-sentiment-arc.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/data/chart-design.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/data/cognitive-psychology.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/data/concept-device.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/data/counterfactual.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/data/criticism-history.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/data/cross-time-danmaku.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/data/cultural-misreading.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/data/customs-pass-route.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/data/data-explorer.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/data/deconstruction.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/data/dialogue-sentiment.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/data/ecology.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/data/emotional-heatmap.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/data/ethics-consumption.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/data/famous-time-travel.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/data/four-dimensional-research-network.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/data/four-heavenly-kings-artifacts.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/data/game-webnovel.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/data/global-pattern.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/data/graph-explorer.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/data/guanyin-six-roles-network.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/data/hardship-difficulty-heatmap.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/data/hardship-heatmap.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/data/heaven-power-network.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/data/intertextuality-network.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/data/journey-geo-3d.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/data/journey-geo-semiotics.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/data/journey-map-interactive.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/data/journey-route.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/data/journey-spacetime.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/data/jurisprudence.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/data/karma-reincarnation.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/data/language-style-radar.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/data/linguistics.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/data/magic-system.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/data/material-archaeology.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/data/mbti-evolution.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/data/methodology-matrix.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/data/ming-political-thought-comparison.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/data/monster-background.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/data/monster-capability-radar.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/data/monster-ecology-network.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/data/monster-female-network.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/data/monster-hierarchy-network.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/data/monster-sociology.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/data/monster-victims-network.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/data/music-structure.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/data/narrative-experiment.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/data/narrative-rhythm-curve.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/data/narratology-12d-network.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/data/narratology-16d-network.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/data/perf-canvas-rendering.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/data/philosophy.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/data/pilgrim-team-dynamic-network.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/data/pilgrim-team-psychology-arc.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/data/poetry-rhythm-analysis.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/data/power-resources.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/data/relationships.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/data/risk-project.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/data/search.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/data/six-senses-narratology-network.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/data/social-media.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/data/story-timeline.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/data/tag-cloud.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/data/text-evolution.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/data/text-search.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/data/theological-intervention-network.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/data/timeline.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/data/underworld-power-network.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/data/visual-art.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/data/workplace.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/81-hardships-view.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/81-hardships.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/academic-papers.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/aesthetics.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/ai-dialogue.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/bestiary.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/business-model.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/cave-estate.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/century-dialogue.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/chapter-stats.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/chapter-structure-graph.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/chapters-map.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/character-appearance.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/character-bailongma.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/character-bajie.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/character-dynamic-network.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/character-presence-timeline.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/character-relationship-3d-view.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/character-relationship-3d.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/character-semantic-network.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/character-sentiment-arc.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/character-shaseng.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/character-tangseng.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/character-wukong.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/characters.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/chart-design.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/cognitive-psychology.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/concept-device.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/counterfactual.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/criticism-history.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/cross-time-danmaku.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/cultural-misreading.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/customs-pass-route.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/dashboard.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/data-explorer.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/deconstruction.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/dialogue-sentiment.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/dukou-engine.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/ecology.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/emotional-heatmap.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/essay-ai-era.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/essay-buddhist-chan.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/essay-chapter-couplets.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/essay-character-fu.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/essay-cipai-linjiangxian.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/essay-cipai-mantingfang.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/essay-cipai-shuidiaogetou.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/essay-cipai-xijiangyue.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/essay-composition-origins.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/essay-divine-bureaucracy.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/essay-folk-belief.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/essay-historical-xuanzang.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/essay-information-cocoon.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/essay-ming-economy.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/essay-ming-examination.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/essay-ming-garrison.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/essay-ming-intellectual-history.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/essay-ming-judiciary.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/essay-ming-literary-thought.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/essay-ming-maritime-ban.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/essay-ming-metaphor.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/essay-ming-military.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/essay-ming-politics.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/essay-ming-religion.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/essay-ming-social-customs.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/essay-modern-management.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/essay-original-poetry.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/essay-poetry-imagery.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/essay-poetry-opening.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/essay-quanzhen-daoism.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/essay-rhythm-analysis.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/essay-scenery-poems.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/essay-thematic-poetry.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/essay-three-teachings.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/essay-version-evolution.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/essay-zen-koan-vs-neidan.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/ethics-consumption.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/famous-time-travel.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/four-dimensional-research-network.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/four-heavenly-kings-artifacts.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/game-webnovel.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/global-pattern.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/graph-explorer.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/guanyin-six-roles-network.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/guide.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/hardship-difficulty-heatmap.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/hardship-heatmap.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/heaven-power-network.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/index.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/intertextuality-network.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/journey-geo-semiotics.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/journey-map-interactive.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/journey-route.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/journey-spacetime.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/jurisprudence.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/karma-reincarnation.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/language-style-radar.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/linguistics.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/magic-system.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/material-archaeology.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/mbti-evolution.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/methodology-matrix.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/methodology.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/ming-political-thought-comparison.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/monster-background.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/monster-capability-radar.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/monster-ecology-network.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/monster-female-network.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/monster-hierarchy-network.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/monster-sociology.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/monster-victims-network.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/music-structure.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/narrative-experiment.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/narrative-rhythm-curve.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/narratology-12d-network.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/narratology-16d-network.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/perf-canvas-rendering.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/philosophy.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/pilgrim-team-dynamic-network.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/pilgrim-team-psychology-arc.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/poetry-rhythm-analysis.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/power-resources.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/relationships.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/risk-project.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/search.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/site-map.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/six-senses-narratology-network.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/social-media.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/tag-cloud.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/text-evolution.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/text-search.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/theological-intervention-network.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/timeline.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/tribulations.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/underworld-power-network.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/visual-art.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/visualizations.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/en/workplace.html | W941 | UI 图标位 emoji → 内联 SVG 图标（W941） |
| site/js/reader-enhance.js | W941 | 收藏按钮运行时态切换：文字 ★/☆ → DOM 克隆图标（W941） |
| site/reader/ch001.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch002.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch003.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch004.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch005.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch006.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch007.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch008.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch009.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch010.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch011.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch012.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch013.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch014.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch015.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch016.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch017.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch018.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch019.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch020.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch021.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch022.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch023.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch024.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch025.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch026.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch027.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch028.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch029.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch030.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch031.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch032.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch033.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch034.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch035.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch036.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch037.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch038.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch039.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch040.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch041.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch042.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch043.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch044.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch045.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch046.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch047.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch048.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch049.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch050.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch051.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch052.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch053.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch054.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch055.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch056.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch057.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch058.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch059.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch060.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch061.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch062.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch063.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch064.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch065.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch066.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch067.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch068.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch069.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch070.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch071.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch072.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch073.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch074.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch075.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch076.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch077.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch078.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch079.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch080.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch081.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch082.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch083.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch084.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch085.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch086.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch087.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch088.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch089.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch090.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch091.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch092.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch093.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch094.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch095.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch096.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch097.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch098.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch099.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/ch100.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/culture/三教合一明代思想史深化专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/culture/佛道思想.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/culture/历史玄奘与小说玄奘专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/culture/成书背景.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/culture/明代军事制度对照专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/culture/明代医学养生制度对照专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/culture/明代卫所制度对照专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/culture/明代司法制度深化专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/culture/明代婚姻家庭制度对照专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/culture/明代宗教制度对照专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/culture/明代宗教政策对照专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/culture/明代宫廷与宦官制度对照专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/culture/明代市井百态对照专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/culture/明代思想史对照专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/culture/明代政治制度对照专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/culture/明代文学体裁与西游对照专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/culture/明代文学思想对照专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/culture/明代服饰舆服制度对照专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/culture/明代海禁政策对照专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/culture/明代盐法开中制度对照专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/culture/明代社会风俗对照专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/culture/明代神祇官僚体系对照专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/culture/明代科举制度对照专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/culture/明代经济制度对照专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/culture/明代隐喻.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/culture/明代驿递交通制度对照专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/culture/版本演变.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/culture/版本演变补遗-平话层.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/culture/西游与佛教禅宗专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/culture/西游与明代商业经济专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/culture/西游与明代民间宗教专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/culture/西游与民间信仰专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/culture/西游与禅宗公案专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/culture/西游与道教全真派专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/essays/现代视角解读.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/essays/西游与AI时代.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/essays/西游与人类学.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/essays/西游与代理悖论.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/essays/西游与传播学.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/essays/西游与伦理学.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/essays/西游与体育学.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/essays/西游与信息茧房.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/essays/西游与化学.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/essays/西游与医学.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/essays/西游与博弈论.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/essays/西游与地理学.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/essays/西游与天文学.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/essays/西游与媒介史.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/essays/西游与宗教学.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/essays/西游与平台经济.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/essays/西游与建筑学.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/essays/西游与心理学.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/essays/西游与性别政治.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/essays/西游与情绪劳动.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/essays/西游与教育学.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/essays/西游与数学.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/essays/西游与明代嘉靖镜像.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/essays/西游与服饰学.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/essays/西游与比较文学.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/essays/西游与民俗学.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/essays/西游与法理政治.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/essays/西游与流亡者.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/essays/西游与演化论.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/essays/西游与物理学.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/essays/西游与现代组织管理.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/essays/西游与生态学.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/essays/西游与社会学.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/essays/西游与神话学.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/essays/西游与符号学.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/essays/西游与经济学.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/essays/西游与美学.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/essays/西游与翻译学.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/essays/西游与考古学.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/essays/西游与认知科学.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/essays/西游与语言学.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/essays/西游与音乐学.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/essays/西游与项目管理.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/essays/西游与饮食学.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/index.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/万圣公主外传.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/严嵩与牛魔王对照专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/乌巢禅师外传.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/乌鸡国国王-方向二深化.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/九头虫.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/九头驸马外传.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/九灵元圣-方向二深化.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/二十八宿外传.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/二郎神-方向二深化.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/二郎神.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/二郎神外传.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/二郎神深化专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/人物分类增补专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/人物谱系表.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/六耳猕猴-方向二深化.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/六耳猕猴.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/六耳猕猴深化专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/刘伯钦外传.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/南极仙翁外传.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/卵二姐外传.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/取经五众关系网络深化.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/取经团队动力学深化专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/变的哲学-方向二深化.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/哪吒.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/哪吒外传.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/哪吒深化专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/唐僧-方向二深化.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/唐僧.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/唐僧深化专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/四值功曹五方揭谛六丁六甲外传.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/四大天王合集专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/国师王菩萨.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/土地公-方向二深化.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/多目怪-方向二深化.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/大鹏金翅雕.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/大鹏金翅雕外传.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/天庭体系深化专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/太上老君-方向二深化.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/太上老君.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/太上老君外传.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/太上老君深化专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/太宗李世民外传.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/太白金星-方向二深化.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/太白金星.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/奎木狼-方向二深化.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/奎木狼不负前情外传.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/奎木狼外传.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/女儿国国王-方向二深化.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/女儿国国王.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/女儿国国王深化专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/如意真仙外传.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/如来.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/如来佛祖-方向二深化.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/如来佛祖-方向二深化B.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/妖怪群体组织形态深化.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/妖怪谱系深度分析.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/嫦娥外传.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/孙悟空-方向二深化.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/孙悟空.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/孙悟空外传.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/孙悟空深化专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/宝象国国王后外传.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/宝象国国王外传.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/小妖外传.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/张居正与玉帝权术对照专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/弥勒佛外传.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/悟空-方向二深化.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/托塔李天王外传.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/扫塔人外传.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/接引佛祖外传.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/推云童子外传.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/敖广外传.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/文殊与普贤外传.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/日值功曹外传.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/明代历史原型对照专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/昴日星官.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/昴日星官外传.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/有来有去外传.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/李贽与悟空对照专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/杏仙外传.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/次要人物关系网络深化.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/殷温娇外传.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/沙僧-方向二深化.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/沙僧.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/沙僧外传.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/沙僧深化专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/泥鳅外传.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/泾河龙王外传.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/海瑞与悟空直谏对照专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/火焰山土地外传.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/灵吉菩萨.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/灵感大王-方向二深化.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/灵感大王.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/燃灯古佛外传.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/牛魔王-方向二深化.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/牛魔王-方向二深化B.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/牛魔王.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/牛魔王深化专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/独角兕大王.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/狮驼岭三魔-方向二深化.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/猪八戒-方向二深化.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/猪八戒.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/猪八戒深化专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/玄奘-方向二深化.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/玄奘外传.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/玉兔精-方向二深化.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/玉兔精.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/玉兔精深化专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/玉帝.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/玉帝深化专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/玉皇大帝-方向二深化.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/玉皇大帝外传.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/玉面狐狸深化专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/王母娘娘.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/王母娘娘深化专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/王阳明与唐僧心学对照专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/白象精.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/白骨精-方向二深化.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/白骨精.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/白骨精外传.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/白骨精深化专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/白鹿精-方向二深化.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/白龙马-方向二深化.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/白龙马-方向二深化B.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/白龙马.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/白龙马外传.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/白龙马深化专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/百眼魔君.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/百眼魔君外传.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/百花羞-方向二深化.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/百花羞外传.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/紫金铃外传.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/红孩儿-方向二深化.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/红孩儿.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/红孩儿外传.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/红孩儿深化专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/红蟒精.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/给孤独长者外传.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/罗刹女外传.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/老鼋外传.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/老鼠精-方向二深化.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/老鼠精.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/老鼠精深化专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/芭蕉扇外传.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/荆棘岭外传.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/菩提祖师-方向二深化.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/菩提祖师.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/菩提祖师外传.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/菩提祖师深化专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/虎先锋外传.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/虾兵外传.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/虾兵外传B.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/蜘蛛精-方向二深化.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/蜘蛛精.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/蜘蛛精七姐妹合集专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/蜘蛛精七姐妹深化专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/蜘蛛精外传.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/蝎子精-方向二深化.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/蝎子精.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/蝎子精深化专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/袁守诚外传.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/被借来的道具-方向二深化.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/观音.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/观音外传.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/观音菩萨-方向二深化.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/观音菩萨深化专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/规矩的多重面孔-方向二深化.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/赛太岁-方向二深化.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/赛太岁.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/车迟国三国师-方向二深化.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/车迟国三国师外传.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/辟寒辟暑辟尘-方向二深化.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/边缘神祇深化专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/迦叶外传.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/通臂猿猴外传.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/金刚琢外传.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/金圣宫娘娘-方向二深化.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/金圣宫娘娘外传.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/金圣宫娘娘深化专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/金池长老外传.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/金箍棒-方向二深化.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/金蝉子外传.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/金角大王.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/金角银角-方向二深化.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/金角银角外传.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/金角银角深化专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/铁扇公主-方向二深化.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/铁扇公主.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/铁扇公主深化专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/铜台府外传.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/银角大王.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/镇元大仙-方向二深化.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/镇元大仙.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/阿傩迦叶外传.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/陈关保外传.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/青牛精-方向二深化.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/青狮精.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/驼罗庄外传.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/高翠兰-方向二深化.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/高翠兰外传.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/高翠兰深化专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/鱼篮观音外传.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/黄眉老佛外传.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/黄袍怪-方向二深化.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/黄袍怪.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/黄袍怪外传.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/黄风怪-方向二深化.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/黄风怪外传.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/黎山老母外传.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/黑熊精-方向二深化.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/people/黑熊精.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/poetry/主题诗词创作.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/poetry/原著人物赋诗词赏析专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/poetry/原著景物诗分类赏析专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/poetry/原著景物诗赏析专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/poetry/原著诗词赏析.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/poetry/回目对联分析专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/poetry/开篇诗专题深化.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/poetry/西游与临江仙词牌赏析专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/poetry/西游与水调歌头词牌赏析专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/poetry/西游与满庭芳词牌赏析专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/poetry/西游与西江月词牌赏析专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/poetry/西游诗词意象谱系专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/poetry/西游诗词韵律分析专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes-hub.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/不可靠叙述专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/二十八星宿专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/二郎神与悟空-自由观碰撞.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/互文性叙事学专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/五方揭谛专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/五次蜕变专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/人参果-人与欲望的关系.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/佛学AI西游三维语义映射表.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/修辞叙事学专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/倒果为因专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/元叙事学专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/全世界重写西游记.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/全球重写专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/八十一难专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/八十一难结构学专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/八十一难风险管理学专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/六丁六甲专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/兵器的自我修养专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/创伤叙事学专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/动物研究专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/历史叙事学专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/反抗与束缚的永恒循环专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/取经人类学专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/取经传播学专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/取经伦理学专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/取经历史学专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/取经叙事经济学专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/取经团队-凭什么走到西天.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/取经团队决策论专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/取经团队动力学.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/取经团队心理学专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/取经团队组织学专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/取经团队身体地理学专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/取经地理批评专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/取经声音政治学专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/取经媒介考古学专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/取经密码学专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/取经情感结构专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/取经拓扑学专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/取经政治学专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/取经教育学专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/取经数字人文专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/取经气候学专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/取经生态学专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/取经社会学专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/取经神话政治学专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/取经空间生产专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/取经符号学专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/取经网络叙事学专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/取经网络叙事学深化专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/取经美学专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/取经考古学专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/取经路径地理符号学专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/取经路线社会学研究专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/名字的政治学专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/后人类主义专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/后殖民叙事学专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/听觉叙事学专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/味觉叙事学专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/唐僧-凡躯圣心.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/嗅觉叙事学专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/器物传记学专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/四值功曹专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/增补一三十九位神祇总序与编制表专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/增补七很多很多劫之后专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/增补三土地公与山神专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/增补二全员集结专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/增补五老亥的日常生活专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/增补八值日功曹的最后一笔专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/增补六波罗僧揭谛的前身暗示专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/增补四值月功曹的花册与节气专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/大闹天宫-英雄还是悲剧.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/大闹天宫专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/女性主义叙事学专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/妖怪伦理学专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/妖怪生态学专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/妖怪经济学专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/妖怪身份政治专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/妖魔谱系政治学专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/小妖生命史专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/底层叙事学专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/开篇诗-被跳过的总纲.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/开篇诗专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/情感叙事学专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/招安对比重写专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/招安的两种结局专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/接受美学专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/文化记忆专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/无字真经-灵山的玩笑.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/无字真经专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/时间叙事学专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/时间哲学专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/时间的政治学专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/明代司法制度镜像专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/暗数据遗忘者列传.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/权力五联对照专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/根器专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/比较文学专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/水帘洞-瀑布门的世界.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/水帘洞专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/沙僧-沉默者的智慧.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/法宝政治学专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/法宝系统专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/混世四猴专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/物质生态学专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/猪八戒-不愿承认的自己.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/猴王到行者-五次蜕变.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/生态批评专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/白龙马-沉默龙的真相.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/真假美猴王-二心之战.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/真假美猴王专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/神学干预机制专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/神话学专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/空间叙事学专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/空间政治学专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/筋斗云与高铁-速度焦虑.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/筋斗云专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/紧箍儿咒-四百年回响.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/紧箍咒专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/缘起即算法-章节体.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/缘起即算法专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/翻译学专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/芭蕉扇-终极灭火器的关系.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/蟠桃园-体制内的秘密.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/西游与信息论专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/西游与全球神话比较专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/西游与后结构主义专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/西游与复杂性科学专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/西游与媒介理论专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/西游与媒介生态学专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/西游与存在主义专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/西游与弗洛伊德精神分析专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/西游与拉康精神分析专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/西游与政治思想史专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/西游与游戏学专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/西游与社会理论延伸专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/西游与符号学专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/西游与系统论专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/西游与经济学专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/西游与经济学派深化专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/西游与荣格分析心理学专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/西游与解构主义专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/西游与解释学专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/西游与认知科学专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/西游与记忆技术专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/西游体检-你走到第几回了.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/西游体检专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/西游四维研究专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/西游渡元定义.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/西游渡第一讲专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/西游渡第三十讲专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/西游渡第二十一讲专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/西游渡第二十七讲专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/西游渡第二十三讲专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/西游渡第二十九讲专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/西游渡第二十二讲专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/西游渡第二十五讲专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/西游渡第二十八讲专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/西游渡第二十六讲专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/西游渡第二十四讲专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/西游渡第二十讲专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/西游渡第二讲专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/西游渡第十七讲专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/西游渡第十九讲专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/西游渡第十五讲专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/西游渡第十八讲专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/西游渡第十六讲专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/西游职场学第一讲专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/西游职场学第七讲专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/西游职场学第三讲专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/西游职场学第二讲专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/西游职场学第五讲专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/西游职场学第六讲专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/西游职场学第四讲专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/西游职场学终讲专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/西游职场学附篇专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/西游记原著与黑神话悟空长生体系对比总结专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/西游败局第一讲专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/西游败局第七讲专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/西游败局第三讲专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/西游败局第九讲专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/西游败局第二讲专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/西游败局第五讲专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/西游败局第八讲专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/西游败局第六讲专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/西游败局第十一讲专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/西游败局第十二讲专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/西游败局第十讲专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/西游败局第四讲专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/西游败局终讲专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/视觉叙事学专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/触觉叙事学专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/认知叙事学专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/记忆之场专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/记忆伦理专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/身体政治学专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/金箍棒的重量-一万三千五百斤的秘密.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/长生之后神仙为什么死了专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/长生之道专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/长生之道的代价专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/长生之道的政治经济学专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/长生之道的权力谱系专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/长生之道终章专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/集体记忆专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/须菩提祖师-消失的师父.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/reader/themes/黑神话拒绝金箍专题.html | W941 | 阅读页：收藏 ★/反馈 👍👎 → 内联 SVG 图标（W941） |
| site/static/js/rag-chat.js | W941 | 检索来源/相关语料标签前缀 emoji → 内联 SVG（W941） |
| site/static/js/text-search-app.js | W941 | 空态图标 emoji → 内联 SVG（W941） |
| site/static/icons/ui/alchemy.svg | W941 | 新增：东方线描图标资产（24×24 / stroke 1.5 / currentColor） |
| site/static/icons/ui/book-open.svg | W941 | 新增：东方线描图标资产（24×24 / stroke 1.5 / currentColor） |
| site/static/icons/ui/book.svg | W941 | 新增：东方线描图标资产（24×24 / stroke 1.5 / currentColor） |
| site/static/icons/ui/cap.svg | W941 | 新增：东方线描图标资产（24×24 / stroke 1.5 / currentColor） |
| site/static/icons/ui/chart.svg | W941 | 新增：东方线描图标资产（24×24 / stroke 1.5 / currentColor） |
| site/static/icons/ui/check.svg | W941 | 新增：东方线描图标资产（24×24 / stroke 1.5 / currentColor） |
| site/static/icons/ui/child.svg | W941 | 新增：东方线描图标资产（24×24 / stroke 1.5 / currentColor） |
| site/static/icons/ui/close.svg | W941 | 新增：东方线描图标资产（24×24 / stroke 1.5 / currentColor） |
| site/static/icons/ui/cross.svg | W941 | 新增：东方线描图标资产（24×24 / stroke 1.5 / currentColor） |
| site/static/icons/ui/globe.svg | W941 | 新增：东方线描图标资产（24×24 / stroke 1.5 / currentColor） |
| site/static/icons/ui/inspect.svg | W941 | 新增：东方线描图标资产（24×24 / stroke 1.5 / currentColor） |
| site/static/icons/ui/menu.svg | W941 | 新增：东方线描图标资产（24×24 / stroke 1.5 / currentColor） |
| site/static/icons/ui/pause.svg | W941 | 新增：东方线描图标资产（24×24 / stroke 1.5 / currentColor） |
| site/static/icons/ui/pen.svg | W941 | 新增：东方线描图标资产（24×24 / stroke 1.5 / currentColor） |
| site/static/icons/ui/pin.svg | W941 | 新增：东方线描图标资产（24×24 / stroke 1.5 / currentColor） |
| site/static/icons/ui/play.svg | W941 | 新增：东方线描图标资产（24×24 / stroke 1.5 / currentColor） |
| site/static/icons/ui/quote.svg | W941 | 新增：东方线描图标资产（24×24 / stroke 1.5 / currentColor） |
| site/static/icons/ui/radio.svg | W941 | 新增：东方线描图标资产（24×24 / stroke 1.5 / currentColor） |
| site/static/icons/ui/schoolbag.svg | W941 | 新增：东方线描图标资产（24×24 / stroke 1.5 / currentColor） |
| site/static/icons/ui/scroll.svg | W941 | 新增：东方线描图标资产（24×24 / stroke 1.5 / currentColor） |
| site/static/icons/ui/search.svg | W941 | 新增：东方线描图标资产（24×24 / stroke 1.5 / currentColor） |
| site/static/icons/ui/sprout.svg | W941 | 新增：东方线描图标资产（24×24 / stroke 1.5 / currentColor） |
| site/static/icons/ui/star-solid.svg | W941 | 新增：东方线描图标资产（24×24 / stroke 1.5 / currentColor） |
| site/static/icons/ui/star.svg | W941 | 新增：东方线描图标资产（24×24 / stroke 1.5 / currentColor） |
| site/static/icons/ui/thumb-down.svg | W941 | 新增：东方线描图标资产（24×24 / stroke 1.5 / currentColor） |
| site/static/icons/ui/thumb-up.svg | W941 | 新增：东方线描图标资产（24×24 / stroke 1.5 / currentColor） |
| site/static/icons/ui/warn.svg | W941 | 新增：东方线描图标资产（24×24 / stroke 1.5 / currentColor） |
| scripts/_w939_gen_icons.py | W941 | 新增：图标集生成器（27 枚·单一事实源） |
| scripts/_w939_scan_targets.py | W941 | 新增：UI 图标位基准扫描器（机检判据·可复跑） |
| scripts/_w939_emoji_to_svg.py | W941 | 新增：emoji → 内联 SVG 批量替换器（每规则带独立预期命中数） |
| scripts/output/_w939_targets.json | W941 | 新增：基准扫描器输出（治理后复扫：UI 图标位 = 0） |
| scripts/output/_w939_replacements.json | W941 | 新增：37 条规则逐条命中统计 |
| docs/11-方案报告/计划方案/执行前计划-T26-UI图标emoji治理批.md | W941 | 新增：执行前计划（T26） |
| docs/11-方案报告/计划方案/T26-任务计划执行与经验沉淀报告-2026-10-25.md | W941 | 新增：交付报告（T26） |
| docs/11-方案报告/README.md | W941 | 新增：T-26 登记行 |
| docs/00-导读/W批次编号对账表.md | W941 | W941 认领行与收官回填 |

## W940 Hero 素材题材辨识度修正（2026-10-25）

| 文件 | W | 说明 |
|---|---|---|
| assets/promo/hero-set/hero-line-04-tight-crown.png | W940 | 新增「紧箍儿」母版（西游独占物件·替代司南） |
| assets/promo/hero-set/hero-line-04-tight-crown.webp | W940 | 同上 WebP |
| assets/promo/hero-set/hero-line-09-somersault-cloud.png | W940 | 新增「筋斗云」母版（替代判不合格的取经四众） |
| assets/promo/hero-set/hero-line-09-somersault-cloud.webp | W940 | 同上 WebP |
| assets/promo/hero-set/raw/hero-04b-tight-crown.jpg | W940 | 紧箍儿出图原件（重出基准） |
| assets/promo/hero-set/raw/hero-05b-somersault-cloud.png | W940 | 筋斗云出图原件 |
| assets/promo/hero-set/hero-line-04-sinan-compass.png | W940 | 删除（司南·通用意象非西游独占） |
| assets/promo/hero-set/hero-line-09-pilgrim-four.png | W940 | 删除（画成农夫挑担·无西游标志物） |
| assets/promo/hero-set/preview-contact-sheet.png | W940 | 9 张成套拼图刷新 |
| assets/promo/hero-set/README.md | W940 | 逐张清单更新 + 新增「题材辨识度自检表（J8 人工关）」 |
| site/static/images/hero-line-04-tight-crown.webp | W940 | 站点版（新增） |
| site/static/images/hero-line-09-somersault-cloud.webp | W940 | 站点版（新增） |
| site/index.html | W940 | 图集引用换图（04→紧箍儿·09→筋斗云） |
| scripts/_w931_hero_verify.py | W940 | 判据清单换名（04/09） |
| scripts/_w938_apply_home.py | W940 | 幂等补丁同步（含 SLIDES/aria-label 换图） |
| scripts/_w940_cascade.py | W940 | 四面登记脚本（认领行 + CHANGELOG 段 + file-index 段 + 当前态指针） |
| CHANGELOG.md | W940 | W940 版段（四件套） |
| docs/00-导读/W批次编号对账表.md | W940 | W940 认领行 |

## W938 首屏版式重做 + 图集逐张复核（2026-10-25）

| 文件 | W | 说明 |
|---|---|---|
| site/index.html | W938 | 左侧文字重排（眉题→标题组→主张句→细线→数据带→标签→CTA→切换器）+ 插画切换器归位左侧文字列内 + 第 9 张换图 |
| site/static/images/hero-line-09-pilgrim-four.webp | W938 | 新增收尾图（取经四众西行·2400×1017·站点版） |
| assets/promo/hero-set/hero-line-09-pilgrim-four.png | W938 | 收尾图母版（PNG） |
| assets/promo/hero-set/hero-line-09-pilgrim-four.webp | W938 | 收尾图 WebP |
| assets/promo/hero-set/raw/hero-09-pilgrim-four.jpg | W938 | 收尾图出图原件（重出基准） |
| assets/promo/hero-set/hero-line-07-banana-fan.png | W938 | 芭蕉扇重出（首版扇面顶边被裁成半截圆面） |
| assets/promo/hero-set/hero-line-07-banana-fan.webp | W938 | 芭蕉扇重出 WebP |
| assets/promo/hero-set/raw/hero-07-banana-fan.jpg | W938 | 芭蕉扇重出原件（覆盖首版） |
| assets/promo/hero-set/preview-contact-sheet.png | W938 | 9 张成套拼图刷新 |
| assets/promo/hero-set/preview-contact-sheet.webp | W938 | 9 张成套拼图 WebP |
| assets/promo/hero-set/README.md | W938 | 目录导读更新（8 张 → 9 张 + 第 9 张换图留证） |
| scripts/_w931_hero_verify.py | W938 | 判据清单加第 9 张（9/9 PASS） |
| scripts/_w938_cascade.py | W938 | 三面级联登记脚本（认领行 + CHANGELOG 段 + file-index 段·含段序断言） |
| CHANGELOG.md | W938 | W938 版段（四件套） |
| docs/00-导读/W批次编号对账表.md | W938 | W938 认领行 |

## W937 首屏版式修正——「100 回」数据块移入左侧文字区（2026-10-25）

| 文件 | W | 说明 |
|---|---|---|
| site/index.html | W937 | 「100 回」数据块由右侧巨型块移入左侧文字区做横排一行（数字降档 clamp 44–64px）·删纸色渐变遮罩 · 移动端 mega 尺寸规则改作用域形式 · 删 `.masthead-mega` 死规则 |
| CHANGELOG.md | W937 | W937 版段（四件套） |
| docs/00-导读/W批次编号对账表.md | W937 | W937 认领行 |
| scripts/_w937_cascade.py | W937 | 三面级联登记脚本（认领行 + CHANGELOG 段 + file-index 段·含段序断言） |
| site/reader/themes/取经路线地理专题.html | W937 | 题图落位修正：五行山与两界山（原在「取经地理学专题」——地理学理论页·题材不贴） |
| site/reader/people/灵感大王外传.html | W937 | 题图落位修正：东海龙宫水殿（原在「四海龙王：下雨的人」——讲降雨职能·题材不贴） |
| scripts/_w937_move_plates.py | W937 | 题图移动脚本（旧页移除 figure 与 chapter-plate CSS·不留死规则） |

## W936 首屏图集接入 + 专题题图落位（2026-10-25）

| 文件 | W | 说明 |
|---|---|---|
| site/index.html | W936 | 首页 9 张图集轮播（JS 定时切换 + WCAG 2.2.2 暂停机制 + reduced-motion 降级）+ 右侧「100 回」数字区纸色渐变底 |
| site/reader/people/地府体系深化专题.html | W936 | 题图：冥府判官队列浓墨剪影 |
| site/reader/people/紧箍儿的内侧-器物传记.html | W936 | 题图：紧箍与金刚杵静物对置 |
| site/reader/themes/取经地理学专题.html | W936 | 题图：五行山与两界山（浓墨山峦 + 锁链） |
| site/reader/people/四海龙王外传.html | W936 | 题图：东海龙宫水殿 |
| site/reader/themes/西游与死亡研究专题.html | W936 | 题图：六道轮回抽象水墨 |
| site/static/images/hero-line-01~08.webp | W936 | W931 线描横幅接入站点（8 件·首页图集用） |
| site/static/images/plate-*.webp | W936 | W932 浓墨 5 张题图副本（plate- 前缀·避开 hero- 序列语义） |
| scripts/_w936_insert_plates.py | W936 | 题图插入脚本（chapter-plate 范式·行尾归一修正） |
| scripts/_w936_cascade.py | W936 | 三面级联登记脚本（认领行 + CHANGELOG 段 + file-index 段·含段序断言） |
| CHANGELOG.md | W936 | W936 版段（四件套） |
| docs/00-导读/W批次编号对账表.md | W936 | W936 认领行（W935 在途跳号依据） |

## W935 速赢两处批（2026-10-25）

| 文件 | W | 说明 |
|---|---|---|
| site/dukou-engine.html | W935 | 渡口档案 LINE 数组 4 条工程引用去除（溯源移入源码注释） |
| site/en/visualizations.html | W935 | source-note 段目录型死链改纯文本（site/data/ 无 index.html·线上 404） |
| docs/11-方案报告/计划方案/T25-任务计划执行与经验沉淀报告-2026-10-25.md | W935 | 速赢两处批交付报告（32/32 判据符合） |
| docs/00-导读/W批次编号对账表.md | W935 | W935 认领行与收官回填 |
| docs/11-方案报告/README.md | W935 | 计划方案分区登记（第 27 行·T-25） |
| scripts/output/_w935_spec.json | W935 | 本批级联 spec |
| CHANGELOG.md | W935 | W935 段 |
| HANDOVER.md | W935 | 级联头尾链与里程碑块 |
| README.md | W935 | 当前批次版本行 |
| STRUCTURE.md | W935 | 当前批次版本行 |
| docs/00-导读/项目说明.md | W935 | 当前批次版本行 |
| site/index.html | W935 | 页脚批次链插入 W935 |
| site/dukou-engine.html | W935 | 页脚批次链插入 W935 |
| AGENTS.md | W935 | 版本脚注条目 |
| archive/docs/AGENTS-ARCHIVE.md | W935 | 脚注滚动迁入的最老条目 |
| CITATION.cff | W935 | version 同步为 W935 |
| scripts/output/file-index.md | W935 | W935 段插入 |

## W934 D-2 应用迁移批第一子批（2026-10-25）

| 文件 | W | 说明 |
|---|---|---|
| xiyouji-agent-web/server/storage/types.ts | W934 | 新增：M12 存储层接口 `StorageBackend` + DTO + 语义约定（两后端必须一致的 7 条） |
| xiyouji-agent-web/server/storage/sqlite.ts | W934 | 新增：现役 SQLite 实现逐字搬迁 + `kind` + `healthCheck`（DDL / 3 版迁移 / 12 函数零语义改写） |
| xiyouji-agent-web/server/storage/postgres.ts | W934 | 新增：PG 后端（连接池 + 事务 + 参数化查询 + 健康探针 + schema 隔离 + 时间列边界转换） |
| xiyouji-agent-web/server/storage/index.ts | W934 | 新增：后端工厂（缺省 sqlite·非法值 fail-closed）+ StorageBackend 契约逐项转发 |
| xiyouji-agent-web/server/storage/storage.test.ts | W934 | 新增：双后端契约测试（同一套断言跑 SQLite 与 PostgreSQL·PG 侧隔离在专用 schema） |
| xiyouji-agent-web/server/db.ts | W934 | 由「SQLite 实现本体」降为**门面**（16 个现役导出名齐备·实现搬进 server/storage/） |
| xiyouji-agent-web/server/routes.ts | W934 | 存储调用改 await（接口异步化·业务逻辑零改动）+ 就绪探针改走 healthCheck |
| xiyouji-agent-web/server/chat.ts | W934 | 存储调用改 await + rebuildHistory 改异步 |
| xiyouji-agent-web/server/index.ts | W934 | 启动日志按实际后端取值（不再写死 SQLite）+ PG 后端跳过文件级快照（走 pg_basebackup） |
| xiyouji-agent-web/server/shutdown.ts | W934 | closeDatabase 契约放宽为 `void | Promise<void>` 并 await（PG 池关闭是 Promise） |
| xiyouji-agent-web/package.json | W934 | 新增依赖 `pg@8.23.1` + `@types/pg`；test:server 纳入契约测试 |
| xiyouji-agent-web/package-lock.json | W934 | 随 pg / @types/pg 锁定 |
| xiyouji-agent-web/deploy/pg/migrations/0002_app_tables.sql | W934 | 新增：业务三表 schema（sessions / messages / feedback + 索引 + role CHECK + message_id 唯一维度 + 外键级联·时间列 TIMESTAMPTZ） |
| xiyouji-agent-web/deploy/pg/bin/migrate-sqlite-to-pg.ts | W934 | 新增：SQLite→PG 迁移器（源库只读 + 参数化 + 迁移序列记账 + 行数/主键集合/逐行内容三重对账） |
| xiyouji-agent-web/deploy/pg/bin/initdb-bootstrap.sh | W934 | 授权模型修三处：ALTER DEFAULT PRIVILEGES 补 FOR ROLE + 权限先于建表 + 记账表 owner 转给应用账号 |
| xiyouji-agent-web/deploy/pg/bin/verify-baseline.py | W934 | 71 → 95 项（新增 C5 组）+ 新增 strip_ts_comments（断言不再命中文档注释里的示例代码） |
| xiyouji-agent-web/deploy/pg/bin/_mutation_test.py | W934 | 14 → 23 组变异（M14~M22·逐条证明 C5 组新判据可证伪） |
| xiyouji-agent-web/deploy/pg/README.md | W934 | §4.3 待实跑清单 3→2 项（迁移器端到端已收官）+ 新增 §4.5 W934 实跑结果与三处授权缺陷 |
| docs/11-方案报告/计划方案/执行前计划-T23-D2应用迁移批.md | W934 | 新增：执行前计划（16 AC + 20 ASM + 22 ST + 13 V + 11 风险 + 11 决策 + 12 项自包含检查） |
| docs/11-方案报告/计划方案/T23-任务计划执行与经验沉淀报告-2026-10-25.md | W934 | 新增：交付报告（执行记录 + 16 条 AC 验收 + 8 条经验沉淀 + 9 条偏差 + 7 项未验证项声明） |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W934 | 新增 §13.6 W934 实跑结果（7 项实跑 + 3 个静默型真缺陷 + D-2 未完成声明） |
| docs/11-方案报告/README.md | W934 | 登记表新增 T-23 两行（执行前计划 + 交付报告） |
| docs/00-导读/W批次编号对账表.md | W934 | W934 认领行与收官回填 |
| scripts/output/_w934_d2a_migrate.json | W934 | 迁移实跑机器证据（三重对账结果） |
| scripts/output/_w934_d2a_residue_before.txt | W934 | 清理前演练残留快照（证明清理对象是 W928 演练产物而非应用数据） |
| scripts/output/_w934_d2a_grants.txt | W934 | 授权模型实查（owner / acl / 只读账号写入被拒） |
| scripts/output/_w934_spec.json | W934 | 本批级联 spec |
| scripts/output/_cascade_files_W934.txt | W934 | 级联落盘清单 |
| CHANGELOG.md | W934 | W934 段 |
| HANDOVER.md | W934 | 级联头尾链与里程碑块 |
| README.md | W934 | 当前批次版本行 |
| STRUCTURE.md | W934 | 当前批次版本行 |
| docs/00-导读/项目说明.md | W934 | 当前批次版本行 |
| .github/workflows/README.md | W934 | 工作流层区间与里程碑尾标记 |
| site/index.html | W934 | 页脚批次链插入 W934 |
| site/data/cross-time-danmaku.html | W934 | 页脚批次链插入 W934 |
| site/data/tag-cloud.html | W934 | 页脚批次链插入 W934 |
| site/dukou-engine.html | W934 | 页脚批次链插入 W934 |
| AGENTS.md | W934 | 版本脚注条目 |
| archive/docs/AGENTS-ARCHIVE.md | W934 | 脚注滚动迁入的最老条目 |
| CITATION.cff | W934 | version 同步为 W934 |
| scripts/output/file-index.md | W934 | W934 段插入 |

## W933 共享面串行化机制批（2026-10-25）

| 文件 | W | 说明 |
|---|---|---|
| docs/11-方案报告/计划方案/T22-任务计划执行与经验沉淀报告-2026-10-25.md | W933 | 共享面串行化机制交付报告（计划/执行/验收/复盘/经验沉淀·32/32 判据符合） |
| docs/00-导读/文档规范.md | W933 | §11.0 共享面并发纪律（认领即占号 / 回填独占 / 收官回填三件套） |
| scripts/preflight_check.py | W933 | 判据 A 撞号检测（台账同号多行）+ B′ 台账脏行提示 + D 反引号剥离 + E 登记类共享面排除 |
| scripts/ledger_backfill.py | W933 | 判据 B 独占回填工具（--expect 基线指纹 / --verify 提交前复核 / --append-claim 纯追加认领） |
| scripts/ledger_close_check.py | W933 | 判据 C 收官回填体检（现役段 W 号须 hash 非占位 + 状态以已收官开头·不挂 verify_delivery 阻塞段） |
| scripts/_w933_mutation_test.py | W933 | 四判据可证伪性验证（4 组突变 + 4 组对照） |
| Makefile | W933 | 新增 ledger 目标并接进 ci（第 42 门禁四面引用口径） |
| scripts/output/_w933_spec.json | W933 | 本批级联 spec |
| docs/00-导读/W批次编号对账表.md | W933 | W933 认领行与收官回填 |
| docs/11-方案报告/README.md | W933 | 计划方案分区登记（第 26 行·T-22） |
| CHANGELOG.md | W933 | W933 段 |
| HANDOVER.md | W933 | 级联头尾链与里程碑块 |
| README.md | W933 | 当前批次版本行 |
| STRUCTURE.md | W933 | 当前批次版本行 |
| docs/00-导读/项目说明.md | W933 | 当前批次版本行 |
| site/index.html | W933 | 页脚批次链插入 W933 |
| site/dukou-engine.html | W933 | 页脚批次链插入 W933 |
| AGENTS.md | W933 | 版本脚注条目 |
| archive/docs/AGENTS-ARCHIVE.md | W933 | 脚注滚动迁入的最老条目 |
| CITATION.cff | W933 | version 同步为 W933 |
| scripts/output/file-index.md | W933 | W933 段插入 |

## W932 站点 Hero 素材图成套批（2026-10-25）

| 文件 | W | 说明 |
|---|---|---|
| site/static/images/hero-10-mingfu-panwang.webp | W932 | 新增：Hero 素材 04/06·冥府判官队列（宣判官+队列纵深+朱砂灯笼·净空带 364px·三轮版） |
| site/static/images/hero-11-chiping-boshan.webp | W932 | 新增：Hero 素材 05/06·持瓶菩萨立像（背向剪影+赭金光环+朱砂飘带·净空带 379px·印面归一） |
| site/static/images/hero-12-jingu-jingangchui.webp | W932 | 新增：Hero 素材 06/06·紧箍与金刚杵静物（黑墨双器+朱砂绳·净空带 557px·三轮版） |
| site/static/images/hero-13-wujingshan-liangjie.webp | W932 | 新增：Hero 素材 07/06·五行山两界山（裂隙崖壁+锁链布幡+朱砂小旗·净空带 282px·印面归一） |
| site/static/images/hero-14-donghai-longgong.webp | W932 | 新增：Hero 素材 08/06·东海龙宫水殿（墨龙盘殿+朱砂龙珠·净空带 363px·印面归一） |
| site/static/images/hero-15-liudao-lunhui.webp | W932 | 新增：Hero 素材 09/06·六道轮回轮（三重枯笔环+六墨块+朱砂段·净空带 377px·印面归一） |
| scripts/_w929_gen_args.py | W932 | 首轮生成参数（锚点复用 W893 + 浓墨剪影改造 + 六张主体描述） |
| scripts/_w929_gen_args_v2.py | W932 | 二轮返工参数（钤印形态写死正方形） |
| scripts/_w929_gen_args_v3.py | W932 | 三轮返工参数（钤印印面去字形化） |
| scripts/_w929_process.py | W932 | 交付端处理（裁切精确 16:9 + 缩放 2560×1440 + 转 webp） |
| scripts/_w929_seal_normalize.py | W932 | 交付端印面归一（自动定框 + 只重绘印面·主体零改动） |
| scripts/_w929_verify.py | W932 | 五道判据量化复验（尺寸/净空带/主体墨量/朱砂/规则线） |
| scripts/output/_w932_spec.json | W932 | 本批 spec 十字段 |
| scripts/output/_cascade_files_W932.txt | W932 | 本批级联件清单 |
| site/static/images/index.md | W932 | 目录索引刷新（文件 78 → 84·补入六件 Hero） |
| docs/00-导读/W批次编号对账表.md | W932 | 认领行与收官回填 |

## W931 首页 Hero 横幅素材图成套批·线描版 8 张（2026-10-25）

| 文件 | W | 说明 |
|---|---|---|
| assets/promo/hero-set/hero-line-01-ruyi-staff.png | W931 | 成品母版 2400×1017·如意金箍棒（黑铁杆 + 赭金云纹端头）·左侧 46% 留白 |
| assets/promo/hero-set/hero-line-02-journey-scroll.png | W931 | 成品母版 2400×1017·行程图卷轴（山路 / 路线 / 河曲） |
| assets/promo/hero-set/hero-line-03-classic-scroll.png | W931 | 成品母版 2400×1017·经卷 + 篆香（竖行纹理非可读文字） |
| assets/promo/hero-set/hero-line-04-sinan-compass.png | W931 | 成品母版 2400×1017·司南（铜盘回纹刻度 + 匙柄） |
| assets/promo/hero-set/hero-line-05-lotus.png | W931 | 成品母版 2400×1017·莲花（层瓣线描 + 赭金叶脉） |
| assets/promo/hero-set/hero-line-06-nine-ring-staff.png | W931 | 成品母版 2400×1017·九环锡杖（赭金环 + 白杆） |
| assets/promo/hero-set/hero-line-07-banana-fan.png | W931 | 成品母版 2400×1017·芭蕉扇（线描叶脉 + 纸色透出·第二版·首版黑色实心块已废弃） |
| assets/promo/hero-set/hero-line-08-jade-vase.png | W931 | 成品母版 2400×1017·玉净瓶（白瓷瓶 + 柳枝） |
| assets/promo/hero-set/hero-line-01-ruyi-staff.webp | W931 | 站点用 WebP q90（8 张全套同规格） |
| assets/promo/hero-set/hero-line-02-journey-scroll.webp | W931 | 站点用 WebP q90 |
| assets/promo/hero-set/hero-line-03-classic-scroll.webp | W931 | 站点用 WebP q90 |
| assets/promo/hero-set/hero-line-04-sinan-compass.webp | W931 | 站点用 WebP q90 |
| assets/promo/hero-set/hero-line-05-lotus.webp | W931 | 站点用 WebP q90 |
| assets/promo/hero-set/hero-line-06-nine-ring-staff.webp | W931 | 站点用 WebP q90 |
| assets/promo/hero-set/hero-line-07-banana-fan.webp | W931 | 站点用 WebP q90 |
| assets/promo/hero-set/hero-line-08-jade-vase.webp | W931 | 站点用 WebP q90 |
| assets/promo/hero-set/preview-contact-sheet.png | W931 | 成套一览拼图 2×4（8 张缩略·一眼验一致性） |
| assets/promo/hero-set/preview-contact-sheet.webp | W931 | 成套一览拼图 WebP |
| assets/promo/hero-set/raw/hero-01-ruyi-staff.jpg | W931 | 出图原件 3168×1344（重出基准·模型不可复现） |
| assets/promo/hero-set/raw/hero-02-journey-scroll.jpg | W931 | 出图原件 3168×1344 |
| assets/promo/hero-set/raw/hero-03-classic-scroll.jpg | W931 | 出图原件 3168×1344 |
| assets/promo/hero-set/raw/hero-04-sinan-compass.jpg | W931 | 出图原件 3168×1344 |
| assets/promo/hero-set/raw/hero-05-lotus.jpg | W931 | 出图原件 3168×1344 |
| assets/promo/hero-set/raw/hero-06-nine-ring-staff.jpg | W931 | 出图原件 3168×1344 |
| assets/promo/hero-set/raw/hero-07-banana-fan.jpg | W931 | 出图原件 3168×1344（第二版） |
| assets/promo/hero-set/raw/hero-08-jade-vase.jpg | W931 | 出图原件 3168×1344 |
| assets/promo/hero-set/README.md | W931 | 目录导读（规格 / 接入方法 / 维护约定 / 已知取舍） |
| assets/promo/hero-set/index.md | W931 | 目录文件索引（生成器产物） |
| assets/promo/hero-set/raw/README.md | W931 | 出图原件目录导读（含废弃首版留证） |
| assets/promo/hero-set/raw/index.md | W931 | 出图原件目录文件索引（生成器产物） |
| assets/promo/index.md | W931 | 上级目录索引刷新（新增 hero-set 子目录登记） |
| STRUCTURE.md | W931 | promo 段登记行（promo/hero-set/ 目录用途） |
| docs/00-导读/W批次编号对账表.md | W931 | W931 认领行（取号依据 + touches 声明） |
| CHANGELOG.md | W931 | W931 版段（四件套·来源 / 文件 / 验证 / 状态） |
| scripts/_w931_hero_verify.py | W931 | 成套判据脚本（7 条 J1–J7 + 负样本可证伪自检） |
| scripts/_w931_claim_row.py | W931 | 对账表认领行登记脚本（幂等·绝不覆盖他人认领） |
| scripts/_w931_changelog_seg.py | W931 | CHANGELOG 段插入脚本（段序结构断言 + 让号后重定位） |

## W930 界面布局复核与落地方案（2026-10-25）

| 文件 | W | 说明 |
|---|---|---|
| docs/11-方案报告/计划方案/T21-任务计划执行与经验沉淀报告-2026-10-25.md | W930 | 四维复核结论（18 条现状表）+ 三条新发现 + 六批可施工落地方案 + 6 条未验证项 |
| docs/11-方案报告/计划方案/执行前计划-T21-界面布局复核与落地方案.md | W930 | T-21 框架件·执行前计划（九表齐备：标识/目标/边界/ASM/ST/V/R/D/自包含） |
| docs/11-方案报告/README.md | W930 | §六 计划方案 +1 行（篇数 24→25） |
| docs/00-导读/W批次编号对账表.md | W930 | W930 认领行（二次让号依据 + touches 声明） |
| scripts/_w930_layout_static.py | W930 | 静态复算（间距刻度 / 令牌消费 / 断点清点·原口径 + 修正口径两套输出） |
| scripts/_w930_layout_diff.py | W930 | 新旧逐项对拍（缺失字段标 MISSING 不填 0） |
| scripts/_w930_layout_attr.py | W930 | 增量归因（区分布局劣化与内容增量） |
| scripts/_w930_layout_detail.py | W930 | 标题字号序列 + 应用侧几何对拍 |
| scripts/_w930_layout_residual.py | W930 | 容器档位 / 长段字数每行 / 顶栏入口数 / 应用侧留白 |
| scripts/_w930_layout_probe.mjs | W930 | 站点渲染探针 11 组（复用 W854 探针改落点 + 目录自建） |
| scripts/_w930_layout_probe_app.mjs | W930 | 应用渲染探针 6 组（复用 W854 探针改落点） |
| scripts/_w930_claim_row.py | W930 | 台账认领行登记脚本（幂等·不覆盖他人认领的号） |
| scripts/_w930_rename_prefix.py | W930 | 产物前缀统一改名脚本（幂等 + 残留校验） |
| scripts/_w930_report_normalize.py | W930 | 报告件归一为纯报告侧（去触发词 + 补报告侧 token） |
| scripts/output/_w930_layout_static.json | W930 | 静态复算证据 |
| scripts/output/_w930_layout_metrics.json | W930 | 站点渲染实测证据（11 组） |
| scripts/output/_w930_layout_metrics_app.json | W930 | 应用渲染实测证据（6 组） |
| scripts/output/_w930_layout_diff.json | W930 | 新旧对拍证据 |
| scripts/output/_w930_layout_attr.json | W930 | 增量归因证据 |
| scripts/output/_w930_visible_leak.json | W930 | 可见工程批次号复算证据（796 页 6,827 处） |
| scripts/output/_w930_plan_review.json | W930 | 第 48 门禁判据矩阵证据（双件全项符合） |
| scripts/output/_w930_spec.json | W930 | 本批级联 spec |

## W928 D-1 实跑批（2026-10-25）

| 文件 | W | 说明 |
|---|---|---|
| xiyouji-agent-web/deploy/pg/postgresql.conf.base | W928 | 删除 server_encoding（initdb 固定参数·写进 conf 致 PG FATAL 拒绝启动）+ 增补实测口径注释 |
| xiyouji-agent-web/deploy/pg/pg_hba.conf.base | W928 | 实跑核验（最小权限 + 兜底 reject 生效·scram 认证通过） |
| xiyouji-agent-web/deploy/pg/bin/initdb-bootstrap.sh | W928 | 实跑核验幂等性（连跑两次·第二次全「已存在，跳过创建」） |
| xiyouji-agent-web/deploy/pg/bin/backup.sh | W928 | 去 -z（目录格式不能压缩·PG 报错）+ 显式 -U（pg_basebackup 默认用当前 OS 用户）+ 跨平台 df 分盘判据（MINGW/MSYS 族） |
| xiyouji-agent-web/deploy/pg/bin/restore-drill.sh | W928 | 重写恢复逻辑：铺满整个备份目录（base/ 与 global/ 是兄弟）+ 删 standby.signal + 接 WAL 归档做 PITR + 重写 postgresql.auto.conf + 业务库断言 + 源库行数一致比对 + 跨平台 restore_command 适配 |
| xiyouji-agent-web/deploy/pg/bin/verify-baseline.py | W928 | 66 → 71 项（新增禁形态：server_encoding / `#` 注释 / `-D` 配 `-z`） |
| xiyouji-agent-web/deploy/pg/bin/_mutation_test.py | W928 | 11 → 14 组变异（新增 M11/M12/M13 对应上述三个禁形态） |
| xiyouji-agent-web/deploy/pg/migrations/0001_baseline.sql | W928 | `#` 注释全改 `--`（PG 的 SQL 只认 `--`·否则 psql 语法错误） |
| xiyouji-agent-web/deploy/pg/README.md | W928 | §4 待实跑清单 → 实跑状态（已通过 6 项 / 真缺陷 4 条 / 仍待实跑 3 项 / 平台适配与两处跨平台判据坑） |
| scripts/output/_w927_pg_runtime_evidence.txt | W928 | D-1 实跑机器证据（真实 PG 16.4·111 行原始输出） |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W928 | §13.3 第 2 条（PG 未实跑）改判 + 新增 §13.5 实跑结果（6 项通过 + 4 个真缺陷 + 跨平台判据坑） |
| docs/11-方案报告/计划方案/T20-任务计划执行与经验沉淀报告-2026-10-25.md | W928 | 附录 A.3 改写为实跑结果（6 项通过 + 4 个真缺陷 + 两处跨平台坑 + 仍待实跑 3 项） |
| docs/11-方案报告/README.md | W928 | §二 架构方案行补 W928 实跑摘要 + §六 T-20 报告行补实跑结果 |
| docs/00-导读/W批次编号对账表.md | W928 | W928 认领行与收官回填 |
| CHANGELOG.md | W928 | W928 段 |
| HANDOVER.md | W928 | 级联头尾链与里程碑块 |
| README.md | W928 | 当前批次版本行 |
| STRUCTURE.md | W928 | 当前批次版本行 |
| docs/00-导读/项目说明.md | W928 | 当前批次版本行 |
| .github/workflows/README.md | W928 | 工作流层区间与里程碑尾标记 |
| site/index.html | W928 | 页脚批次链插入 W928 |
| site/data/cross-time-danmaku.html | W928 | 页脚批次链插入 W928 |
| site/data/tag-cloud.html | W928 | 页脚批次链插入 W928 |
| site/dukou-engine.html | W928 | 页脚批次链插入 W928 |
| AGENTS.md | W928 | 版本脚注条目 |
| archive/docs/AGENTS-ARCHIVE.md | W928 | 脚注滚动迁入的最老条目 |
| CITATION.cff | W928 | version 同步为 W928 |
| scripts/output/file-index.md | W928 | W928 段插入 |
| scripts/output/_w928_spec.json | W928 | 本批级联 spec |
| scripts/output/_cascade_files_W928.txt | W928 | 级联落盘清单 |

## W927 架构方案 v2 裁决落档 + D-1 离线施工件 + W926 交叉对账（2026-10-25）

| 文件 | W | 说明 |
|---|---|---|
| xiyouji-agent-web/deploy/pg/README.md | W927 | D-1 施工件说明（口径对照 + 目标机执行顺序 + 机器背书 + 9 项待实跑清单 + 边界声明） |
| xiyouji-agent-web/deploy/pg/postgresql.conf.base | W927 | PG 16 配置基线（WAL 归档 / TLS / 内存 / 日志 / 编码 / 自动清理·禁 listen_addresses='*'） |
| xiyouji-agent-web/deploy/pg/pg_hba.conf.base | W927 | 认证基线（最小权限 + 兜底 reject + 禁 trust + 禁明文口令） |
| xiyouji-agent-web/deploy/pg/bin/initdb-bootstrap.sh | W927 | 幂等初始化（角色/库/权限/迁移记账表·PG 版本门槛 + 只读角色最小权限） |
| xiyouji-agent-web/deploy/pg/bin/backup.sh | W927 | 每日全量备份（pg_basebackup）+ 保留期轮转（7 份 / WAL 14 天）+ 空壳自检 + 备份归档分盘校验 |
| xiyouji-agent-web/deploy/pg/bin/restore-drill.sh | W927 | 恢复演练（独立端口临时实例 + 表/列/行数断言 + trap 清理） |
| xiyouji-agent-web/deploy/pg/bin/verify-baseline.py | W927 | 静态校验器（C1 配置 / C2 认证 / C3 脚本 / C4 迁移·66 项不变量·本批实跑 66/66） |
| xiyouji-agent-web/deploy/pg/bin/_mutation_test.py | W927 | 反向验证（11 组变异改坏必红 + 基线未变异必绿·本批实跑 11/11 可证伪） |
| xiyouji-agent-web/deploy/pg/migrations/0001_baseline.sql | W927 | 迁移序列骨架（schema_migrations 记账 + audit_archive 带 data_class CHECK L1–L4·单事务包裹） |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W927 | 裁决落档（O-1~O-4 + 六处连带更新）+ 交叉对账 §13.4 + 新增 §10.6 配置面缺口 + 契约 C-8 + 禁止依赖形态 #8 |
| docs/11-方案报告/计划方案/执行前计划-T20-裁决落档与D1施工件.md | W927 | T-20 框架件·执行前计划（12 AC + 15 ASM + 18 ST + 12 V + 8 风险 + 7 决策 + 14 自检） |
| docs/11-方案报告/计划方案/T20-任务计划执行与经验沉淀报告-2026-10-25.md | W927 | T-20 框架件·执行报告（18 步执行记录 + 12 条验收 + 7 条可行性自评 + 7 条经验 + 5 条偏差 + PG 未验证声明） |
| docs/11-方案报告/README.md | W927 | §六 计划方案 +2 行（篇数 22→24）· §二 架构方案行更新为「W925 建 / W927 裁决落档 + 施工件 + 对账」 |
| docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md | W927 | report_docs 实体标记随 stats.json 刷新（60→62·C5b 对账） |
| STRUCTURE.md | W927 | report_docs 标记刷新 + 六子目录篇数同步（计划方案 22→24） |
| scripts/output/_w927_pg_baseline.json | W927 | 静态校验证据（total=66 / passed=66 / failed=0） |
| docs/00-导读/W批次编号对账表.md | W927 | W927 认领行与收官回填 |
| CHANGELOG.md | W927 | W927 段 |
| HANDOVER.md | W927 | 级联头尾链与里程碑块 |
| README.md | W927 | 当前批次版本行 |
| docs/00-导读/项目说明.md | W927 | 当前批次版本行 |
| .github/workflows/README.md | W927 | 工作流层区间与里程碑尾标记 |
| site/index.html | W927 | 页脚批次链插入 W927 |
| site/data/cross-time-danmaku.html | W927 | 页脚批次链插入 W927 |
| site/data/tag-cloud.html | W927 | 页脚批次链插入 W927 |
| site/dukou-engine.html | W927 | 页脚批次链插入 W927 |
| AGENTS.md | W927 | 版本脚注条目 |
| archive/docs/AGENTS-ARCHIVE.md | W927 | 脚注滚动迁入的最老条目 |
| CITATION.cff | W927 | version 同步为 W927 |
| scripts/output/file-index.md | W927 | W927 段插入 |
| scripts/output/_w927_spec.json | W927 | 本批级联 spec |
| scripts/output/_cascade_files_W927.txt | W927 | 级联落盘清单 |

## W926 站点交互流程审查复核报告批（2026-10-25）

| 文件 | W | 说明 |
|---|---|---|
| docs/11-方案报告/审查与评审/站点交互流程审查复核报告-2026-10-25.md | W926 | 站点交互流程审查复核报告（857 页四维复核·10 条问题按访客影响排序·附前次 17 条闭环表与 9 项正面结论） |
| scripts/_w926_ia_audit.py | W926 | 全量交互结构扫描器（跳转路径/按钮反馈/表单报错/空态异常四维·判据自纠三处） |
| scripts/_w926_ia_extract.py | W926 | 可疑判定逐条落到「文件是否存在」的实证提取器 |
| scripts/_w926_visible_leak.py | W926 | 访客可见文本的内部术语外泄扫描（剥离 script/style/注释后统计） |
| scripts/_w926_fix_report.py | W926 | 报告修订脚本（依独立盲审 B1-B6 + N1-N8·26 处替换带命中数断言·防盲改） |
| scripts/_w926_fix_report2.py | W926 | 报告第二轮整理（R-11/R-12 入清单·排序与小节化·剩余数字订正） |
| scripts/_w926_verify_numbers.py | W926 | 报告数字机器对拍（20 项数字 + 4 项结构断言·报告文本 ↔ 证据 JSON 逐项比对） |
| scripts/output/_w926_ia_audit.json | W926 | 全量扫描结构化证据 |
| scripts/output/_w926_ia_evidence.json | W926 | 死链与缺失目标实证证据 |
| scripts/output/_w926_visible_leak.json | W926 | 可见术语外泄明细 |
| docs/00-导读/W批次编号对账表.md | W926 | W926 认领行与收官回填 |
| docs/11-方案报告/README.md | W926 | §一 审查与评审分区登记（第 35 行·节头计数同步） |
| CHANGELOG.md | W926 | W926 段 |
| HANDOVER.md | W926 | 级联头尾链与里程碑块 |
| README.md | W926 | 当前批次版本行 |
| STRUCTURE.md | W926 | 当前批次版本行 |
| docs/00-导读/项目说明.md | W926 | 当前批次版本行 |
| site/index.html | W926 | 页脚批次链插入 W926 |
| site/dukou-engine.html | W926 | 页脚批次链插入 W926 |
| AGENTS.md | W926 | 版本脚注条目 |
| archive/docs/AGENTS-ARCHIVE.md | W926 | 脚注滚动迁入的最老条目 |
| CITATION.cff | W926 | version 同步为 W926 |
| scripts/output/file-index.md | W926 | W926 段插入 |
| scripts/output/_w926_spec.json | W926 | 本批级联 spec |
| scripts/output/_cascade_files_W926.txt | W926 | 级联落盘清单 |

## W925 系统架构方案 v2（2026-10-25）

| 文件 | W | 说明 |
|---|---|---|
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W925 | 架构方案 v2 正文（八维 + 存储裁定修订 + 等保合规横切面 + 6 处 Mermaid 源码为图件事实源） |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-架构图-2026-10-25.html | W925 | 零外域架构图可视化页（手写内联 SVG·file:// 直开·6 图） |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-架构图/（6 张 PNG） | W925 | 架构图 PNG 导出产物（Playwright 实测渲染·外域请求数 = 0） |
| docs/11-方案报告/计划方案/执行前计划-T19-系统架构方案v2.md | W925 | T-19 框架件·执行前计划（11 AC + 20 ASM + 15 ST + 12 V + 8 风险 + 8 决策 + 14 自检） |
| docs/11-方案报告/计划方案/T19-任务计划执行与经验沉淀报告-2026-10-25.md | W925 | T-19 框架件·执行报告（15 步执行记录 + 18 条验收 + 10 条经验 + 6 条偏差 + 6 条未验证项） |
| docs/11-方案报告/README.md | W925 | §二 设计与架构方案 +1 行（篇数 5→6）· §六 计划方案 +2 行（篇数 20→22） |
| docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md | W925 | report_docs 实体标记随 stats.json 刷新（56→59·C5b 对账） |
| scripts/_render_arch_png.mjs | W925 | 架构图 PNG 导出脚本（Playwright ESM·零外域请求断言 + --check 模式） |
| docs/INDEX.md | W925 | 文档索引重建（750 篇·13 板块） |
| scripts/index.md | W925 | 脚本索引刷新 |
| STRUCTURE.md | W925 | report_docs 标记刷新 + 六子目录篇数同步（设计与架构方案 5→6·计划方案 20→22） |
| scripts/output/stats.json | W925 | report_docs 56→59 |
| docs/00-导读/W批次编号对账表.md | W925 | W925 认领行与收官回填 |
| CHANGELOG.md | W925 | W925 段 |
| HANDOVER.md | W925 | 级联头尾链与里程碑块 |
| README.md | W925 | 当前批次版本行 |
| docs/00-导读/项目说明.md | W925 | 当前批次版本行 |
| .github/workflows/README.md | W925 | 工作流层区间与里程碑尾标记 |
| site/index.html | W925 | 页脚批次链插入 W925 |
| site/data/cross-time-danmaku.html | W925 | 页脚批次链插入 W925 |
| site/data/tag-cloud.html | W925 | 页脚批次链插入 W925 |
| site/dukou-engine.html | W925 | 页脚批次链插入 W925 |
| AGENTS.md | W925 | 版本脚注条目 |
| archive/docs/AGENTS-ARCHIVE.md | W925 | 脚注滚动迁入的最老条目 |
| CITATION.cff | W925 | version 同步为 W925 |
| scripts/output/file-index.md | W925 | W925 段插入 |
| scripts/output/_w925_spec.json | W925 | 本批级联 spec |
| scripts/output/_cascade_files_W925.txt | W925 | 级联落盘清单 |

## W924 Q2 裁决落地批（2026-10-24）

| 文件 | W | 说明 |
|---|---|---|
| scripts/check_perf_shadow.py | W924 | Q2 裁决落地：第 47 槽 C2 OBS-10 双层判红（硬 500KB FAIL·软 200KB WARN 观察清单·全站扫描）·汇总行升格口径·自测 5→9 例（OBS-10 双层正负样本） |
| docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md | W924 | §12.2 Q2 行裁决回填（三指标分治）+ §11.5 OBS-10/11/14 三行状态更新 |
| scripts/output/obs_samples.json | W924 | 现势补采（16→17 批·静态口径） |
| docs/00-导读/W批次编号对账表.md | W924 | W924 认领行与收官回填 |
| CHANGELOG.md | W924 | W924 段 |
| HANDOVER.md | W924 | 级联头尾链与里程碑块 |
| README.md | W924 | 当前批次版本行 |
| STRUCTURE.md | W924 | 当前批次版本行 |
| docs/00-导读/项目说明.md | W924 | 当前批次版本行 |
| .github/workflows/README.md | W924 | 工作流层区间与里程碑尾标记 |
| site/index.html | W924 | 页脚批次链插入 W924 |
| site/data/cross-time-danmaku.html | W924 | 页脚批次链插入 W924 |
| site/data/tag-cloud.html | W924 | 页脚批次链插入 W924 |
| site/dukou-engine.html | W924 | 页脚批次链插入 W924 |
| AGENTS.md | W924 | 版本脚注条目 |
| archive/docs/AGENTS-ARCHIVE.md | W924 | 脚注滚动迁入的最老条目 |
| CITATION.cff | W924 | version 同步为 W924 |
| scripts/output/file-index.md | W924 | W924 段插入 |
| scripts/output/_w924_spec.json | W924 | 本批级联 spec |
| scripts/output/_cascade_files_W924.txt | W924 | 级联落盘清单 |

## W923 review 修复批（2026-10-24）

| 文件 | W | 说明 |
|---|---|---|
| docs/00-导读/W批次编号对账表.md | W923 | review 修复：W907 让号行状态前缀消幻影在途 + W910/W911 补让号登记行（跳号须登记字典规则） |
| CHANGELOG.md | W923 | W923 段 |
| HANDOVER.md | W923 | 级联头尾链与里程碑块 |
| README.md | W923 | 当前批次版本行 |
| STRUCTURE.md | W923 | 当前批次版本行 |
| docs/00-导读/项目说明.md | W923 | 当前批次版本行 |
| .github/workflows/README.md | W923 | 工作流层区间与里程碑尾标记 |
| site/index.html | W923 | 页脚批次链插入 W923 |
| site/data/cross-time-danmaku.html | W923 | 页脚批次链插入 W923 |
| site/data/tag-cloud.html | W923 | 页脚批次链插入 W923 |
| site/dukou-engine.html | W923 | 页脚批次链插入 W923 |
| AGENTS.md | W923 | 版本脚注条目 |
| archive/docs/AGENTS-ARCHIVE.md | W923 | 脚注滚动迁入的最老条目 |
| CITATION.cff | W923 | version 同步为 W923 |
| scripts/output/file-index.md | W923 | W923 段插入 |
| scripts/output/_w923_spec.json | W923 | 本批级联 spec |
| scripts/output/_cascade_files_W923.txt | W923 | 级联落盘清单 |

## W922 E 裁决落地批（2026-10-24）

| 文件 | W | 说明 |
|---|---|---|
| site/static/js/rag-chat.js | W922 | 裁决①浮窗文案：生成式问答指向桌面版渡口问津（本地检索预期说对）
| docs/superpowers/plans/2026-10-14-interference-governance-roadmap.md | W922 | 裁决⑧干扰日志窗口收官归档（15 行封档·机器触发点常驻·新事件改登对账表）
| scripts/preflight_check.py | W922 | 触发点提示常量随窗口收官更新
| scripts/check_seo_head.py | W922 | 裁决⑨og:image 判据白名单化（现役+12 张主题图·管控件经用户裁决批准）
| site/index.html 等 12 页 | W922 | og:image 主题接线（og-01..12 按页分配·855 页 SEO 门禁全过）
| docs/11-方案报告/计划方案/执行前计划-T18-站内交互债整包.md | W922 | 裁决⑫项全部登记（四件落地+八项结论）
| docs/00-导读/W批次编号对账表.md | W922 | W922 认领行与收官回填 |
| CHANGELOG.md | W922 | W922 段 |
| HANDOVER.md | W922 | 级联头尾链与里程碑块 |
| README.md | W922 | 当前批次版本行 |
| STRUCTURE.md | W922 | 当前批次版本行 |
| docs/00-导读/项目说明.md | W922 | 当前批次版本行 |
| .github/workflows/README.md | W922 | 工作流层区间与里程碑尾标记 |
| site/data/cross-time-danmaku.html | W922 | 页脚批次链插入 W922 |
| site/data/tag-cloud.html | W922 | 页脚批次链插入 W922 |
| site/dukou-engine.html | W922 | 页脚批次链插入 W922 |
| AGENTS.md | W922 | 版本脚注条目 |
| archive/docs/AGENTS-ARCHIVE.md | W922 | 脚注滚动迁入的最老条目 |
| CITATION.cff | W922 | version 同步为 W922 |
| scripts/output/file-index.md | W922 | W922 段插入 |
| scripts/output/_w922_spec.json | W922 | 本批级联 spec |
| scripts/output/_cascade_files_W922.txt | W922 | 级联落盘清单 |

## W921 CHANGELOG 主动瘦身批（2026-10-24）

| 文件 | W | 说明 |
|---|---|---|
| CHANGELOG.md | W921 | B-W855-05 主动瘦身：W700-W802 共 102 段迁一级归档（679KB→363KB·低于 503KB 基线）·段守恒 693 断言过
| archive/docs/CHANGELOG-ARCHIVE.md | W921 | 承接 102 段迁入（978KB·未触 1MB tier2 阈·滚动分支零启用）·头部归档注记
| docs/00-导读/W批次编号对账表.md | W921 | W921 认领行与收官回填 |
| HANDOVER.md | W921 | 级联头尾链与里程碑块 |
| README.md | W921 | 当前批次版本行 |
| STRUCTURE.md | W921 | 当前批次版本行 |
| docs/00-导读/项目说明.md | W921 | 当前批次版本行 |
| .github/workflows/README.md | W921 | 工作流层区间与里程碑尾标记 |
| site/index.html | W921 | 页脚批次链插入 W921 |
| site/data/cross-time-danmaku.html | W921 | 页脚批次链插入 W921 |
| site/data/tag-cloud.html | W921 | 页脚批次链插入 W921 |
| site/dukou-engine.html | W921 | 页脚批次链插入 W921 |
| AGENTS.md | W921 | 版本脚注条目 |
| archive/docs/AGENTS-ARCHIVE.md | W921 | 脚注滚动迁入的最老条目 |
| CITATION.cff | W921 | version 同步为 W921 |
| scripts/output/file-index.md | W921 | W921 段插入 |
| scripts/output/_w921_spec.json | W921 | 本批级联 spec |
| scripts/output/_cascade_files_W921.txt | W921 | 级联落盘清单 |

## W920 副本链值级对账门禁批（2026-10-24）

| 文件 | W | 说明 |
|---|---|---|
| scripts/check_data_copy_chain.py | W920 | 新增：数据副本链值级对账门禁（JSON 深度相等·基线冻结防增量·CI 态 NOTE 登记·self-test 5/5）——B-W855-04 清偿
| scripts/output/data-copy-chain-baseline.json | W920 | 存量漂移基线（24 件登记态·方向定性另批）
| tests/unit/test_check_data_copy_chain.py | W920 | 新增：门禁专项单测 2 例
| scripts/ci_sim.py | W920 | GATES 清单 +副本链对账（第 11 项）
| docs/00-导读/W批次编号对账表.md | W920 | W920 认领行与收官回填 |
| CHANGELOG.md | W920 | W920 段 |
| HANDOVER.md | W920 | 级联头尾链与里程碑块 |
| README.md | W920 | 当前批次版本行 |
| STRUCTURE.md | W920 | 当前批次版本行 |
| docs/00-导读/项目说明.md | W920 | 当前批次版本行 |
| .github/workflows/README.md | W920 | 工作流层区间与里程碑尾标记 |
| site/index.html | W920 | 页脚批次链插入 W920 |
| site/data/cross-time-danmaku.html | W920 | 页脚批次链插入 W920 |
| site/data/tag-cloud.html | W920 | 页脚批次链插入 W920 |
| site/dukou-engine.html | W920 | 页脚批次链插入 W920 |
| AGENTS.md | W920 | 版本脚注条目 |
| archive/docs/AGENTS-ARCHIVE.md | W920 | 脚注滚动迁入的最老条目 |
| CITATION.cff | W920 | version 同步为 W920 |
| scripts/output/file-index.md | W920 | W920 段插入 |
| scripts/output/_w920_spec.json | W920 | 本批级联 spec |
| scripts/output/_cascade_files_W920.txt | W920 | 级联落盘清单 |

## W919 DB 三包批（2026-10-24）

| 文件 | W | 说明 |
|---|---|---|
| xiyouji-agent-web/server/db.ts | W919 | B-DB-04 迁移框架（MIGRATIONS v1-v3 单调记账·删 try/catch 手写探测迁移）+ B-DB-02 四查询索引 + v3 feedback 表重建（旧库补外键/单维唯一索引/CHECK·含索引重建修复）+ listSessionsWithMessageCount 单 SQL 版
| xiyouji-agent-web/server/routes.ts | W919 | B-DB-02 N+1 改写（子查询·limit 默认 50 上限 200）+ B-DB-03 JSON.parse 脏数据降级 null
| xiyouji-agent-web/server/api.integration.test.ts | W919 | 反馈集成测试对齐外键时代（先落真实 session/message 底数·断言与清理同步）
| docs/agent/agent-web.md | W919 | schema 变更规范固化（改表定义对旧库无效·一律走 MIGRATIONS·禁探测式迁移）
| docs/00-导读/W批次编号对账表.md | W919 | W919 认领行与收官回填 |
| CHANGELOG.md | W919 | W919 段 |
| HANDOVER.md | W919 | 级联头尾链与里程碑块 |
| README.md | W919 | 当前批次版本行 |
| STRUCTURE.md | W919 | 当前批次版本行 |
| docs/00-导读/项目说明.md | W919 | 当前批次版本行 |
| .github/workflows/README.md | W919 | 工作流层区间与里程碑尾标记 |
| site/index.html | W919 | 页脚批次链插入 W919 |
| site/data/cross-time-danmaku.html | W919 | 页脚批次链插入 W919 |
| site/data/tag-cloud.html | W919 | 页脚批次链插入 W919 |
| site/dukou-engine.html | W919 | 页脚批次链插入 W919 |
| AGENTS.md | W919 | 版本脚注条目 |
| archive/docs/AGENTS-ARCHIVE.md | W919 | 脚注滚动迁入的最老条目 |
| CITATION.cff | W919 | version 同步为 W919 |
| scripts/output/file-index.md | W919 | W919 段插入 |
| scripts/output/_w919_spec.json | W919 | 本批级联 spec |
| scripts/output/_cascade_files_W919.txt | W919 | 级联落盘清单 |

## W918 检索降级批（2026-10-24）

| 文件 | W | 说明 |
|---|---|---|
| xiyouji-agent-web/server/chat.ts | W918 | B-ARCH-01 检索降级：LLM 上游不可达（5xx/429/ECONNREFUSED 族）时 SSE 返回降级说明+done 而非裸 5xx（已送达的 tool_result 检索引用仍有效·W821「降级可用」语义落地）
| docs/00-导读/W批次编号对账表.md | W918 | W918 认领行与收官回填 |
| CHANGELOG.md | W918 | W918 段 |
| HANDOVER.md | W918 | 级联头尾链与里程碑块 |
| README.md | W918 | 当前批次版本行 |
| STRUCTURE.md | W918 | 当前批次版本行 |
| docs/00-导读/项目说明.md | W918 | 当前批次版本行 |
| .github/workflows/README.md | W918 | 工作流层区间与里程碑尾标记 |
| site/index.html | W918 | 页脚批次链插入 W918 |
| site/data/cross-time-danmaku.html | W918 | 页脚批次链插入 W918 |
| site/data/tag-cloud.html | W918 | 页脚批次链插入 W918 |
| site/dukou-engine.html | W918 | 页脚批次链插入 W918 |
| AGENTS.md | W918 | 版本脚注条目 |
| archive/docs/AGENTS-ARCHIVE.md | W918 | 脚注滚动迁入的最老条目 |
| CITATION.cff | W918 | version 同步为 W918 |
| scripts/output/file-index.md | W918 | W918 段插入 |
| scripts/output/_w918_spec.json | W918 | 本批级联 spec |
| scripts/output/_cascade_files_W918.txt | W918 | 级联落盘清单 |

## W917 DB 正确性包一（2026-10-24）

| 文件 | W | 说明 |
|---|---|---|
| xiyouji-agent-web/server/db.ts | W917 | B-DB-01 四 P0 之三：pragma foreign_keys=ON（级联生效）/ clearAllData 补 feedback / 反馈唯一索引 (message_id,verdict)→(message_id) 单维 + upsert 改判 / INSERT OR IGNORE→ON CONFLICT 覆盖
| xiyouji-agent-web/server/chat.ts | W917 | B-DB-01 P0 之四：会话主键服务端生成 uuidv4()（客户端可控 id 是串档路径·真值经响应返回）
| scripts/check_db_schema.py | W917 | 新增：DB schema 门禁（四不变量静态锁定·self-test 3/3）——B-DB-05 清偿
| tests/unit/test_check_db_schema.py | W917 | 新增：门禁专项单测 2 例
| scripts/ci_sim.py | W917 | GATES 清单 +DB schema（第 10 项）
| docs/00-导读/W批次编号对账表.md | W917 | W917 认领行与收官回填 |
| CHANGELOG.md | W917 | W917 段 |
| HANDOVER.md | W917 | 级联头尾链与里程碑块 |
| README.md | W917 | 当前批次版本行 |
| STRUCTURE.md | W917 | 当前批次版本行 |
| docs/00-导读/项目说明.md | W917 | 当前批次版本行 |
| .github/workflows/README.md | W917 | 工作流层区间与里程碑尾标记 |
| site/index.html | W917 | 页脚批次链插入 W917 |
| site/data/cross-time-danmaku.html | W917 | 页脚批次链插入 W917 |
| site/data/tag-cloud.html | W917 | 页脚批次链插入 W917 |
| site/dukou-engine.html | W917 | 页脚批次链插入 W917 |
| AGENTS.md | W917 | 版本脚注条目 |
| archive/docs/AGENTS-ARCHIVE.md | W917 | 脚注滚动迁入的最老条目 |
| CITATION.cff | W917 | version 同步为 W917 |
| scripts/output/file-index.md | W917 | W917 段插入 |
| scripts/output/_w917_spec.json | W917 | 本批级联 spec |
| scripts/output/_cascade_files_W917.txt | W917 | 级联落盘清单 |

## W916 波二第三件批（2026-10-24）

| 文件 | W | 说明 |
|---|---|---|
| scripts/check_page_admission.py | W916 | 新增：新建页准入门禁（静态版·禁 type=module + 零外域 script src·857 页 0 FAIL·self-test 3/3）——C-W818-01 清偿
| tests/unit/test_check_page_admission.py | W916 | 新增：门禁专项单测 2 例
| scripts/ci_sim.py | W916 | GATES 清单 +页准入（第 9 项·每 PR 实跑）
| docs/00-导读/W批次编号对账表.md | W916 | W916 认领行与收官回填 |
| CHANGELOG.md | W916 | W916 段 |
| HANDOVER.md | W916 | 级联头尾链与里程碑块 |
| README.md | W916 | 当前批次版本行 |
| STRUCTURE.md | W916 | 当前批次版本行 |
| docs/00-导读/项目说明.md | W916 | 当前批次版本行 |
| .github/workflows/README.md | W916 | 工作流层区间与里程碑尾标记 |
| site/index.html | W916 | 页脚批次链插入 W916 |
| site/data/cross-time-danmaku.html | W916 | 页脚批次链插入 W916 |
| site/data/tag-cloud.html | W916 | 页脚批次链插入 W916 |
| site/dukou-engine.html | W916 | 页脚批次链插入 W916 |
| AGENTS.md | W916 | 版本脚注条目 |
| archive/docs/AGENTS-ARCHIVE.md | W916 | 脚注滚动迁入的最老条目 |
| CITATION.cff | W916 | version 同步为 W916 |
| scripts/output/file-index.md | W916 | W916 段插入 |
| scripts/output/_w916_spec.json | W916 | 本批级联 spec |
| scripts/output/_cascade_files_W916.txt | W916 | 级联落盘清单 |

## W915 波二余件一·二批（2026-10-24）

| 文件 | W | 说明 |
|---|---|---|
| docs/agent/gates.md | W915 | 第 43 槽去时点快照数字（缺口三数/耗时/770→指向报告与基线文件·时点快照不入判据文档）——A-T02-01 清偿
| site/404.html | W915 | v4 间距令牌迁移（:root 页内副本 + 24/48/40 等值替换 var(--space-6/9/8)·非刻度值按 W891 等值纪律保留）——C-B02 清偿
| docs/00-导读/W批次编号对账表.md | W915 | W915 认领行与收官回填 |
| CHANGELOG.md | W915 | W915 段 |
| HANDOVER.md | W915 | 级联头尾链与里程碑块 |
| README.md | W915 | 当前批次版本行 |
| STRUCTURE.md | W915 | 当前批次版本行 |
| docs/00-导读/项目说明.md | W915 | 当前批次版本行 |
| .github/workflows/README.md | W915 | 工作流层区间与里程碑尾标记 |
| site/index.html | W915 | 页脚批次链插入 W915 |
| site/data/cross-time-danmaku.html | W915 | 页脚批次链插入 W915 |
| site/data/tag-cloud.html | W915 | 页脚批次链插入 W915 |
| site/dukou-engine.html | W915 | 页脚批次链插入 W915 |
| AGENTS.md | W915 | 版本脚注条目 |
| archive/docs/AGENTS-ARCHIVE.md | W915 | 脚注滚动迁入的最老条目 |
| CITATION.cff | W915 | version 同步为 W915 |
| scripts/output/file-index.md | W915 | W915 段插入 |
| scripts/output/_w914_spec.json | W915 | 本批级联 spec |
| scripts/output/_cascade_files_W915.txt | W915 | 级联落盘清单 |

## W914 英文版 README（2026-10-24）

| 文件 | W | 说明 |
|---|---|---|
| README.en.md | W914 | 英文版 README（完整对照版·零版本号·站内链接指向 /en/·同款配图） |
| README.md | W914 | 顶部加语言切换行 + 目录树补 README.en.md 一行 |
| docs/00-导读/W批次编号对账表.md | W914 | W914 认领行与收官回填 |
| scripts/output/_w914_spec.json | W914 | 本批级联 spec（10 面改写参数） |
| scripts/output/_cascade_files_W914.txt | W914 | 级联落盘清单 |
| scripts/output/_vermilion_solid_cache.json | W914 | 朱砂门禁增量缓存刷新（本批级联改四页脚后按 sha1 重扫对齐） |
| CHANGELOG.md | W914 | W914 段 |
| HANDOVER.md | W914 | 头尾链与里程碑块 |
| STRUCTURE.md | W914 | 当前批次版本行 |
| docs/00-导读/项目说明.md | W914 | 当前批次版本行 |
| .github/workflows/README.md | W914 | 工作流层区间与里程碑尾标记 |
| site/index.html | W914 | 页脚批次链插入 W914 |
| site/data/cross-time-danmaku.html | W914 | 页脚批次链插入 W914 |
| site/data/tag-cloud.html | W914 | 页脚批次链插入 W914 |
| site/dukou-engine.html | W914 | 页脚批次链插入 W914 |
| AGENTS.md | W914 | 版本脚注条目 |
| CITATION.cff | W914 | version 同步为 W914 |
| scripts/output/file-index.md | W914 | W914 段插入 |

## W913 波二小项四件批（2026-10-24）

| 文件 | W | 说明 |
|---|---|---|
| docs/11-方案报告/计划方案/执行前计划-T04-站内阅读入口打通与阅读页体验封装.md | W913 | 头状态行订正：施工未动工→已收官（W827 入口 + W845-847 阅读页·原文备档）——D-W830-02 清偿
| .github/workflows/ci.yml | W913 | E2E 依赖钉版：playwright 无约束安装→钉 1.63.0 对齐 scripts/package-lock.json（T10 实证真漂移面）——D-W792-02 清偿
| site/index.html | W913 | 站点聚合数字失真修正：「全站 772 篇」→「615<!--stats:a1_a6_docs--> 篇（A1-A6）」——B-W855-01 数字半边
| scripts/check_doc_sync.py | W913 | C5b 扩展面纳入 site/index.html（站点聚合数字从此有标记对账防线·防回退半边）——B-W855-01 防线半边
| docs/11-方案报告/计划方案/执行前计划-T18-站内交互债整包.md | W913 | C 档波二状态更新（四项完成/关闭·余五项在列）
| docs/00-导读/W批次编号对账表.md | W913 | W913 认领行与收官回填
| CHANGELOG.md | W913 | W913 段
| HANDOVER.md | W913 | 级联头尾链与里程碑块
| README.md | W913 | 当前批次版本行
| STRUCTURE.md | W913 | 当前批次版本行
| docs/00-导读/项目说明.md | W913 | 当前批次版本行
| .github/workflows/README.md | W913 | 工作流层区间与里程碑尾标记
| site/index.html（页脚批次链） | W913 | 页脚批次链插入 W913
| site/data/cross-time-danmaku.html | W913 | 页脚批次链插入 W913
| site/data/tag-cloud.html | W913 | 页脚批次链插入 W913
| site/dukou-engine.html | W913 | 页脚批次链插入 W913
| AGENTS.md | W913 | 版本脚注条目
| archive/docs/AGENTS-ARCHIVE.md | W913 | 脚注滚动迁入的最老条目
| CITATION.cff | W913 | version 同步为 W913
| scripts/output/file-index.md | W913 | W913 段插入
| scripts/output/_w913_spec.json | W913 | 本批级联 spec
| scripts/output/_cascade_files_W913.txt | W913 | 级联落盘清单

## W912 未落地任务首波清偿（2026-10-24）

| 文件 | W | 说明 |
|---|---|---|
| site/dukou-engine.html | W912 | 渡口页主脚本考古回灌（W333 原装 10.4KB 自 git 历史提取·W333 后某批剥离致交互全失效的根修）+ 补 themeToggle 绑定（历史原装即缺）+ CSP 重算
| site/index.html | W912 | 抽屉桌面 display:none 副作用修复（close 仅移动端置 none）+ ask-chip 键盘可达（tabindex+Enter/Space 委托）
| site/curated.html | W912 | 同款抽屉修复
| site/dashboard.html | W912 | 同款抽屉修复
| site/guide.html | W912 | 同款抽屉修复
| site/sw.js | W912 | 预缓存死链清理（mobile-index.html 两处）
| site/data/text-search.html | W912 | 注入失败可见错误条（role=alert·非仅 console.warn）
| site/data/cross-time-danmaku.html | W912 | 假 LIVE 文案改真实口径（LIVE 弹幕→弹幕回放·aria 同步）
| site/404.html | W912 | 补夜读防 FOUC theme-init（与全站 W488 同款）
| scripts/check_interaction_binding.py | W912 | 新增：交互绑定门禁（注册控件对账 P1 + 泛化 NOTE P2·fail-closed·self-test 3/3）·接 ci_sim 第 8 项（每 PR 实跑·挂 verify 槽另批）
| tests/unit/test_check_interaction_binding.py | W912 | 新增：门禁专项单测 3 例（self-test 绿/注册表锚点防漂/HEAD 实跑）
| tests/unit/test_preflight_touches.py | W912 | +2 例：嵌套括号长尾收官格识别 / 碎行下右起定位（19/19）
| scripts/preflight_check.py | W912 | _STATUS_CELL_RE 放宽为前缀匹配（原单层括号紧匹配拒识长尾收官格→回退固定下标被碎行击穿·W912 认领拦截实测根修）
| scripts/ci_sim.py | W912 | GATES 清单 +交互绑定（第 8 项）
| docs/11-方案报告/计划方案/执行前计划-T18-站内交互债整包.md | W912 | 新增：未落地任务全量盘点（T-09 基线×现势复核·A–E 五档含价值筛选 D2 冻结档）+ 本批计划（32 判据全项）
| pytest.ini | W912 | pytest_collected 861→867
| scripts/output/stats.json | W912 | --w W912 刷新
| docs/00-导读/W批次编号对账表.md | W912 | W912 认领行（两度让号并行批）与收官回填
| CHANGELOG.md | W912 | W912 段
| HANDOVER.md | W912 | 级联头尾链与里程碑块
| README.md | W912 | 当前批次版本行（同日并行在途首屏改动正交·按清单携带）
| STRUCTURE.md | W912 | 当前批次版本行
| docs/00-导读/项目说明.md | W912 | 当前批次版本行
| .github/workflows/README.md | W912 | 工作流层区间与里程碑尾标记
| site/index.html（页脚批次链） | W912 | 页脚批次链插入 W912
| site/data/cross-time-danmaku.html（页脚批次链） | W912 | 页脚批次链插入 W912
| site/data/tag-cloud.html | W912 | 页脚批次链插入 W912
| site/dukou-engine.html（页脚批次链） | W912 | 页脚批次链插入 W912
| AGENTS.md | W912 | 版本脚注条目
| archive/docs/AGENTS-ARCHIVE.md | W912 | 脚注滚动迁入的最老条目
| CITATION.cff | W912 | version 同步为 W912
| scripts/output/file-index.md | W912 | W912 段插入
| scripts/output/_w912_spec.json | W912 | 本批级联 spec
| scripts/output/_cascade_files_W912.txt | W912 | 级联落盘清单

## W909 README 专业化改版（2026-10-24）

| 文件 | W | 说明 |
|---|---|---|
| README.md | W909 | README 专业化改版（单一 H1 + 两个 H2 分区 + 顶部主视觉 banner + 可视化样例小节 + 宣传单页预览图 + 徽章并行 + 文案修正） |
| docs/00-导读/W批次编号对账表.md | W909 | W909 认领行与收官回填 + 顺带修三处表格结构损坏（W892 粘连段 · W764/W906 未转义管道符） |
| scripts/output/_w909_spec.json | W909 | 本批级联 spec（10 面改写参数） |
| scripts/output/_cascade_files_W909.txt | W909 | 级联落盘清单 |
| scripts/output/_vermilion_solid_cache.json | W909 | 朱砂门禁增量缓存刷新（本批级联改四页脚后按 sha1 重扫对齐） |
| CHANGELOG.md | W909 | W909 段 |
| HANDOVER.md | W909 | 头尾链与里程碑块 |
| STRUCTURE.md | W909 | 当前批次版本行 |
| docs/00-导读/项目说明.md | W909 | 当前批次版本行 |
| .github/workflows/README.md | W909 | 工作流层区间与里程碑尾标记 |
| site/index.html | W909 | 页脚批次链插入 W909 |
| site/data/cross-time-danmaku.html | W909 | 页脚批次链插入 W909 |
| site/data/tag-cloud.html | W909 | 页脚批次链插入 W909 |
| site/dukou-engine.html | W909 | 页脚批次链插入 W909 |
| AGENTS.md | W909 | 版本脚注条目 |
| CITATION.cff | W909 | version 同步为 W909 |
| scripts/output/file-index.md | W909 | W909 段插入 |
| site/data/search.html | W909 | 站内搜索索引内嵌刷新（zh） |
| site/en/search.html | W909 | 站内搜索索引内嵌刷新（en） |

## W906 C4-f 三态化（2026-10-24）

| 文件 | W | 说明 |
|---|---|---|
| scripts/check_doc_sync.py | W906 | C4-f 三态化（管控件·用户批准）：declared 文件残留为「他方批次登记行纯追加」（零删改+全 | WNNN 形态）降 NOTE 放行·在位编辑仍红；新增 _foreign_append_only 探测（git diff 逐 dirty 文件）+ RE_BATCH_REGISTRY_ROW + self-test T32/T33（33/33） |
| docs/11-方案报告/审查与评审/机制脚本门禁审查报告-2026-10-24.md | W906 | 新增 F5 节（C4-f 并行误拦实录与修复）+ 遗留盘点表两行更新（F1 已修/W906 落地） |
| docs/00-导读/W批次编号对账表.md | W906 | W906 认领行与收官回填 |
| CHANGELOG.md | W906 | W906 段 |
| HANDOVER.md | W906 | 级联头尾链与里程碑块 |
| README.md | W906 | 当前批次版本行 |
| STRUCTURE.md | W906 | 当前批次版本行 |
| docs/00-导读/项目说明.md | W906 | 当前批次版本行 |
| .github/workflows/README.md | W906 | 工作流层区间与里程碑尾标记 |
| site/index.html | W906 | 页脚批次链插入 W906 |
| site/data/cross-time-danmaku.html | W906 | 页脚批次链插入 W906 |
| site/data/tag-cloud.html | W906 | 页脚批次链插入 W906 |
| site/dukou-engine.html | W906 | 页脚批次链插入 W906 |
| AGENTS.md | W906 | 版本脚注条目 |
| archive/docs/AGENTS-ARCHIVE.md | W906 | 脚注滚动迁入的最老条目 |
| CITATION.cff | W906 | version 同步为 W906 |
| scripts/output/file-index.md | W906 | W906 段插入 |
| scripts/output/_w906_spec.json | W906 | 本批级联 spec |
| scripts/output/_cascade_files_W906.txt | W906 | 级联落盘清单 |

## W905 两项存量红项清理（2026-10-24）

| 文件 | W | 说明 |
|---|---|---|
| site/data/character-semantic-network.html | W905 | 暗色态补色规则（rgb(163, 1, 38) → #ce7e88·修 W674 色阶变更遗留的 invisible 缺陷） |
| site/en/character-semantic-network.html | W905 | 暗色态补色规则（同上·英文版同步） |
| xiyouji-agent-web/package.json | W905 | 依赖升级（dompurify ^3.4.17）+ overrides 抬版（markdown-it ^14.3.3 / zod ^4.6.7 / vite ^8.3.5） |
| xiyouji-agent-web/package-lock.json | W905 | 锁文件同步（4 包版本推进·lock 变更最小化） |
| scripts/output/_vermilion_solid_cache.json | W905 | 朱砂门禁增量缓存刷新（本批级联改四页脚后按 sha1 重扫对齐） |
| scripts/output/_w905_spec.json | W905 | 本批级联 spec（10 面改写参数） |
| scripts/output/_cascade_files_W905.txt | W905 | 级联落盘清单 |
| docs/00-导读/W批次编号对账表.md | W905 | 认领行与收官回填 |
| CHANGELOG.md | W905 | W905 段 |
| HANDOVER.md | W905 | 头尾链与里程碑块 |
| README.md | W905 | 当前批次版本行 |
| STRUCTURE.md | W905 | 当前批次版本行 |
| docs/00-导读/项目说明.md | W905 | 当前批次版本行 |
| .github/workflows/README.md | W905 | 工作流层区间与里程碑尾标记 |
| site/index.html | W905 | 页脚批次链插入 W905 |
| site/data/cross-time-danmaku.html | W905 | 页脚批次链插入 W905 |
| site/data/tag-cloud.html | W905 | 页脚批次链插入 W905 |
| site/dukou-engine.html | W905 | 页脚批次链插入 W905 |
| AGENTS.md | W905 | 版本脚注条目 |
| CITATION.cff | W905 | version 同步为 W905 |
| scripts/output/file-index.md | W905 | W905 段插入 |

## W904 C5c 裸聚合收敛（2026-10-24）

| 文件 | W | 说明 |
|---|---|---|
| scripts/stats.py | W904 | 增 7 板块键（a2/a3/a5/a6/learn/cognition/spirit·口径对齐 a4_docs 顶层排 README）——C5c 收敛的键位供给
| scripts/check_doc_sync.py | W904 | C5c 由 NOTE 转 FAIL（W703 终态）+ 新增命中后置精确豁免（只豁免该命中·同行标记对账照跑）+ 整行豁免收紧为行首形态（原「行内含即整行跳」会吞后置豁免行的标记对账·T30 负样本实证）+ RE_BARE_AGG 词边界（S1 项目/A2 个人类编号假阳性修复）+ self-test 增 T27-T31（31/31）
| README.md | W904 | C5c 三分治：34 类实体化 / 44 篇实体化 / 常量豁免×2 / 「18 个板块」陈旧数改写为描述式
| STRUCTURE.md | W904 | C5c 三分治 32 处：A3/A5/learn/cognition/spirit/A2/A4/site_en 实体化（**A5「已建 4 篇」陈旧值纠正为实数 34**）/ 六子目录构成与时点史实后置豁免 / 「321 篇」陈旧索引数改写去数
| AGENTS.md | W904 | C5c 三分治 6 处：a2/site_data/site_en 实体化 / 133 维度与 §11 十项常量豁免 / EXPECT_A4 判据字面量转述豁免
| docs/00-导读/项目说明.md | W904 | C5c 三分治 20 处：A2/A3/A5/A6/可视化实体化 / S1-S3 时点史实与功能常量豁免
| CONTRIBUTING.md | W904 | §12 自检十项与 fallback 三项常量豁免×3
| docs/00-导读/统计口径说明.md | W904 | 615/87 实体化 / W505 历史事件计数豁免×2
| docs/11-方案报告/审查与评审/机制脚本门禁审查报告-2026-10-24.md | W904 | F4 状态订正为已收口 + 遗留盘点表更新
| docs/11-方案报告/README.md（登记行 34） | W904 | F4 状态订正为已由 W904 收口
| scripts/output/stats.json | W904 | 新 7 键落盘（--w W904 刷新）
| docs/00-导读/W批次编号对账表.md | W904 | W904 认领行与收官回填 |
| CHANGELOG.md | W904 | W904 段 |
| HANDOVER.md | W904 | 级联头尾链与里程碑块 |
| README.md（版本行） | W904 | 当前批次版本行 |
| STRUCTURE.md（版本行） | W904 | 当前批次版本行 |
| docs/00-导读/项目说明.md（版本行） | W904 | 当前批次版本行 |
| .github/workflows/README.md | W904 | 工作流层区间与里程碑尾标记 |
| site/index.html | W904 | 页脚批次链插入 W904 |
| site/data/cross-time-danmaku.html | W904 | 页脚批次链插入 W904 |
| site/data/tag-cloud.html | W904 | 页脚批次链插入 W904 |
| site/dukou-engine.html | W904 | 页脚批次链插入 W904 |
| AGENTS.md（版本脚注） | W904 | 版本脚注条目 |
| archive/docs/AGENTS-ARCHIVE.md | W904 | 脚注滚动迁入的最老条目 |
| CITATION.cff | W904 | version 同步为 W904 |
| scripts/output/file-index.md | W904 | W904 段插入 |
| scripts/output/_w904_spec.json | W904 | 本批级联 spec |
| scripts/output/_cascade_files_W904.txt | W904 | 级联落盘清单 |

## W903 审查发现修复（2026-10-24）

| 文件 | W | 说明 |
|---|---|---|
| scripts/preflight_check.py | W903 | F1 修复（管控件·用户批准）：_split_touches 注记归一（全角括号内不切且整段丢弃·扫描式 tokenizer）+ touches_conflict 对称目录前缀匹配（X/** 与 X/ 形态）——通配/带注记声明不再恒不命中假绿 |
| scripts/verify_delivery.py | W903 | F2 修复（管控件·用户批准）：第 45 门禁 fail_msg 补「先 git add 本批新件再 refresh」顺序（生成器按 Git 索引收集·W896 口径·W900/W901 连踩） |
| tests/unit/test_preflight_touches.py | W903 | 新增语义归一族单测 6 例（先红后绿：旧码下 5 例红实证·新码 17/17 绿） |
| docs/11-方案报告/审查与评审/机制脚本门禁审查报告-2026-10-24.md | W903 | 状态行 F1/F2「待批」订正为已落地 |
| docs/11-方案报告/README.md | W903 | 登记行 34 的 F1/F2 状态订正为已由 W903 修复 |
| docs/00-导读/W批次编号对账表.md | W903 | W903 认领行与收官回填 |
| CHANGELOG.md | W903 | W903 段 |
| HANDOVER.md | W903 | 级联头尾链与里程碑块 |
| README.md | W903 | 当前批次版本行 |
| STRUCTURE.md | W903 | 当前批次版本行 |
| docs/00-导读/项目说明.md | W903 | 当前批次版本行 |
| .github/workflows/README.md | W903 | 工作流层区间与里程碑尾标记 |
| site/index.html | W903 | 页脚批次链插入 W903 |
| site/data/cross-time-danmaku.html | W903 | 页脚批次链插入 W903 |
| site/data/tag-cloud.html | W903 | 页脚批次链插入 W903 |
| site/dukou-engine.html | W903 | 页脚批次链插入 W903 |
| AGENTS.md | W903 | 版本脚注条目 |
| archive/docs/AGENTS-ARCHIVE.md | W903 | 脚注滚动迁入的最老条目 |
| CITATION.cff | W903 | version 同步为 W903 |
| scripts/output/file-index.md | W903 | W903 段插入 |
| scripts/output/_w903_spec.json | W903 | 本批级联 spec |
| scripts/output/_cascade_files_W903.txt | W903 | 级联落盘清单 |

## W902 机制脚本门禁全量审查与记忆固化入仓（2026-10-24）

| 文件 | W | 说明 |
|---|---|---|
| docs/11-方案报告/审查与评审/机制脚本门禁审查报告-2026-10-24.md | W902 | 新增：机制层全量审查（三层面·四发现·记忆固化迁移清单·遗留盘点） |
| docs/11-方案报告/README.md | W902 | 审查报告登记行 34 + 维护契约 ① 补「唯一落盘位」常设指令句 |
| docs/agent/pitfalls.md | W902 | 记忆固化 +3 条（canvas 边层 / CSP 写路径盲区 / 暗色审计 http 前置假 0）+ 三节计数 9→10·5→6·5→6 |
| AGENTS.md | W902 | 六主题计数同步（49→52）+ §4.3 本机环境事实补 4 条（curl --ssl-no-revoke / /tmp 不可见 / Europe PMC 兜底 / gh api -f） |
| docs/00-导读/文档规范.md | W902 | §11.1 管控表新增「常设指令」行：方案/审查/调研/复盘/计划类交付物唯一落盘位 = docs/11-方案报告/ |
| CLAUDE.md | W902 | 速查层新增「报告落位」条目（46 行·预算 60 内） |
| docs/superpowers/plans/2026-10-14-interference-governance-roadmap.md | W902 | §8 干扰日志补 2 行延迟登记（W825/W893 覆盖事件·考古补·如实标注） |
| docs/00-导读/W批次编号对账表.md | W902 | W902 认领行与收官回填 |
| CHANGELOG.md | W902 | W902 段 |
| HANDOVER.md | W902 | 级联头尾链与里程碑块 |
| README.md | W902 | 当前批次版本行 |
| STRUCTURE.md | W902 | 当前批次版本行 |
| docs/00-导读/项目说明.md | W902 | 当前批次版本行 |
| .github/workflows/README.md | W902 | 工作流层区间与里程碑尾标记 |
| site/index.html | W902 | 页脚批次链插入 W902 |
| site/data/cross-time-danmaku.html | W902 | 页脚批次链插入 W902 |
| site/data/tag-cloud.html | W902 | 页脚批次链插入 W902 |
| site/dukou-engine.html | W902 | 页脚批次链插入 W902 |
| AGENTS.md（版本脚注） | W902 | 版本脚注条目 |
| archive/docs/AGENTS-ARCHIVE.md | W902 | 脚注滚动迁入的最老条目 |
| CITATION.cff | W902 | version 同步为 W902 |
| scripts/output/file-index.md | W902 | W902 段插入 |
| scripts/output/_w902_spec.json | W902 | 本批级联 spec |
| scripts/output/_cascade_files_W902.txt | W902 | 级联落盘清单 |

## W901 C5b 对账面恢复 + W900 披露项清偿（2026-10-24）

| 文件 | W | 说明 |
|---|---|---|
| scripts/check_doc_sync.py | W901 | C5b 扩展面 glob 根层改递归（管控件·用户 2026-10-24 批准；计划方案/ 时点快照豁免原样保留——实测该子目录 8 件带冻结 stats 标记·入面即假红） |
| docs/11-方案报告/README.md | W901 | T-16/T-17 两件补登计划方案表（W893/W896 遗留登记缺口）+ 节头计数订正 + C5b 提示行更新为已恢复口径 + 登记缺口披露行撤除 |
| CHANGELOG.md | W901 | W757 段 1 条审计报告链接随批准改指新址（仅地址不改叙事）+ W901 段 |
| docs/00-导读/W批次编号对账表.md | W901 | W901 认领行与收官回填 |
| HANDOVER.md | W901 | 级联头尾链与里程碑块 |
| README.md | W901 | 当前批次版本行 |
| STRUCTURE.md | W901 | 当前批次版本行 |
| docs/00-导读/项目说明.md | W901 | 当前批次版本行 |
| .github/workflows/README.md | W901 | 工作流层区间与里程碑尾标记 |
| site/index.html | W901 | 页脚批次链插入 W901 |
| site/data/cross-time-danmaku.html | W901 | 页脚批次链插入 W901 |
| site/data/tag-cloud.html | W901 | 页脚批次链插入 W901 |
| site/dukou-engine.html | W901 | 页脚批次链插入 W901 |
| AGENTS.md | W901 | 版本脚注条目 |
| archive/docs/AGENTS-ARCHIVE.md | W901 | 脚注滚动迁入的最老条目 |
| CITATION.cff | W901 | version 同步为 W901 |
| scripts/output/file-index.md | W901 | W901 段插入 |
| scripts/output/_w901_spec.json | W901 | 本批级联 spec |
| scripts/output/_cascade_files_W901.txt | W901 | 级联落盘清单 |

## W900 11-方案报告目录分类重组（2026-10-24）

| 文件 | W | 说明 |
|---|---|---|
| docs/11-方案报告/审查与评审/对抗性审查报告-2026-10-14.md | W900 | 根层迁入分类子目录「审查与评审」（链接面同步见 README/INDEX/搜索索引行） |
| docs/11-方案报告/审查与评审/全量对抗审查报告-2026-10-16.md | W900 | 根层迁入分类子目录「审查与评审」（链接面同步见 README/INDEX/搜索索引行） |
| docs/11-方案报告/审查与评审/工程基础设施薄弱点审计报告-2026-10-16.md | W900 | 根层迁入分类子目录「审查与评审」（链接面同步见 README/INDEX/搜索索引行） |
| docs/11-方案报告/审查与评审/外部评审回应与逐项核查报告-2026-10-17.md | W900 | 根层迁入分类子目录「审查与评审」（链接面同步见 README/INDEX/搜索索引行） |
| docs/11-方案报告/审查与评审/外部评审回应与逐项核查报告-2026-10-18.md | W900 | 根层迁入分类子目录「审查与评审」（链接面同步见 README/INDEX/搜索索引行） |
| docs/11-方案报告/审查与评审/计划方案三性审查报告-2026-10-20.md | W900 | 根层迁入分类子目录「审查与评审」（链接面同步见 README/INDEX/搜索索引行） |
| docs/11-方案报告/审查与评审/架构评审报告-2026-10-21.md | W900 | 根层迁入分类子目录「审查与评审」（链接面同步见 README/INDEX/搜索索引行） |
| docs/11-方案报告/审查与评审/界面布局审计报告-2026-10-21.md | W900 | 根层迁入分类子目录「审查与评审」（链接面同步见 README/INDEX/搜索索引行） |
| docs/11-方案报告/审查与评审/数据库表设计审查报告-2026-10-20.md | W900 | 根层迁入分类子目录「审查与评审」（链接面同步见 README/INDEX/搜索索引行） |
| docs/11-方案报告/审查与评审/难簿序与dataset对拍报告-2026-10-11.md | W900 | 根层迁入分类子目录「审查与评审」（链接面同步见 README/INDEX/搜索索引行） |
| docs/11-方案报告/设计与架构方案/界面视觉重设计方向-v4-2026-10-20.md | W900 | 根层迁入分类子目录「设计与架构方案」（链接面同步见 README/INDEX/搜索索引行） |
| docs/11-方案报告/设计与架构方案/界面视觉重设计细化规格-v4-2026-10-20.md | W900 | 根层迁入分类子目录「设计与架构方案」（链接面同步见 README/INDEX/搜索索引行） |
| docs/11-方案报告/设计与架构方案/v4-design-language-preview.html | W900 | 根层迁入分类子目录「设计与架构方案」（链接面同步见 README/INDEX/搜索索引行） |
| docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md | W900 | 根层迁入分类子目录「设计与架构方案」（链接面同步见 README/INDEX/搜索索引行） |
| docs/11-方案报告/设计与架构方案/静态站前端框架化选型对比-2026-10-20.md | W900 | 根层迁入分类子目录「设计与架构方案」（链接面同步见 README/INDEX/搜索索引行） |
| docs/11-方案报告/设计与架构方案/取经编制表-工具与技能挂位-2026-10-20.md | W900 | 根层迁入分类子目录「设计与架构方案」（链接面同步见 README/INDEX/搜索索引行） |
| docs/11-方案报告/设计与架构方案/取经编制表-工具与技能挂位-2026-10-20.html | W900 | 根层迁入分类子目录「设计与架构方案」（链接面同步见 README/INDEX/搜索索引行） |
| docs/11-方案报告/治理与核查/W761工具链可维护性重构报告-2026-10-16.md | W900 | 根层迁入分类子目录「治理与核查」（链接面同步见 README/INDEX/搜索索引行） |
| docs/11-方案报告/治理与核查/多Agent干扰治理评估与实施记录-2026-10-14.md | W900 | 根层迁入分类子目录「治理与核查」（链接面同步见 README/INDEX/搜索索引行） |
| docs/11-方案报告/治理与核查/全仓待办计划方案状态核查报告-2026-10-18.md | W900 | 根层迁入分类子目录「治理与核查」（链接面同步见 README/INDEX/搜索索引行） |
| docs/11-方案报告/调研与数据复盘/项目GitHub参考调研报告.md | W900 | 根层迁入分类子目录「调研与数据复盘」（链接面同步见 README/INDEX/搜索索引行） |
| docs/11-方案报告/调研与数据复盘/读者数据复盘.md | W900 | 根层迁入分类子目录「调研与数据复盘」（链接面同步见 README/INDEX/搜索索引行） |
| docs/11-方案报告/调研与数据复盘/读者数据截图/dashboard-pages-2026-09-30.png | W900 | 随读者数据复盘迁入「调研与数据复盘」 |
| docs/11-方案报告/调研与数据复盘/读者数据截图/dashboard-top-2026-09-30.png | W900 | 随读者数据复盘迁入「调研与数据复盘」 |
| docs/11-方案报告/调研与数据复盘/读者数据截图/dashboard-top-2026-10-02.png | W900 | 随读者数据复盘迁入「调研与数据复盘」 |
| docs/11-方案报告/调研与数据复盘/读者数据截图/dashboard-topref-2026-10-02.png | W900 | 随读者数据复盘迁入「调研与数据复盘」 |
| docs/11-方案报告/调研与数据复盘/读者数据截图/uv-curve-2026-09.svg | W900 | 随读者数据复盘迁入「调研与数据复盘」 |
| docs/11-方案报告/README.md | W900 | 唯一索引分区重构（目录树 + 33 行总表机械分五区编号不重排 + 计划方案游离行合并 + T-16/T-17 登记缺口披露 + C5b 覆盖提示） |
| docs/10-方法论沉淀/多Agent干扰治理与touches纪律.md | W900 | 2 条入链随迁修正（多 Agent 干扰治理评估全文新址） |
| docs/INDEX.md | W900 | 再生成（20 行路径随迁） |
| site/data/search.html | W900 | 站内搜索索引再生成（zh 848 条）+ CSP 哈希重算 |
| site/en/search.html | W900 | 站内搜索索引再生成（en 890 条）+ CSP 哈希重算 |
| HANDOVER.md | W900 | 零段「复盘存档」陈旧路径（W757 改名前旧址）订正 + 级联头尾链与里程碑块 |
| STRUCTURE.md | W900 | §11 构成散文行按分区实况改写（54 总数不变）+ 版本行 |
| docs/00-导读/W批次编号对账表.md | W900 | W900 认领行与收官回填 |
| CHANGELOG.md | W900 | W900 段 |
| README.md | W900 | 当前批次版本行 |
| docs/00-导读/项目说明.md | W900 | 当前批次版本行 |
| .github/workflows/README.md | W900 | 工作流层区间与里程碑尾标记 |
| site/index.html | W900 | 页脚批次链插入 W900 |
| site/data/cross-time-danmaku.html | W900 | 页脚批次链插入 W900 |
| site/data/tag-cloud.html | W900 | 页脚批次链插入 W900 |
| site/dukou-engine.html | W900 | 页脚批次链插入 W900 |
| AGENTS.md | W900 | 版本脚注条目 |
| archive/docs/AGENTS-ARCHIVE.md | W900 | 脚注滚动迁入的最老条目 |
| CITATION.cff | W900 | version 同步为 W900 |
| scripts/output/file-index.md | W900 | W900 段插入 |
| scripts/output/_w900_spec.json | W900 | 本批级联 spec |
| scripts/output/_cascade_files_W900.txt | W900 | 级联落盘清单 |
| site/static/icons/ui/note.svg | W947 | 新增：便签与文档图标（折角纸页·替 📝） |
| site/static/icons/ui/link.svg | W947 | 新增：双环链条图标（替 🔗） |
| xiyouji-agent-web/src/components/UiIcons.tsx | W947 | 新增：agent-web 内联 SVG 图标组件（WarnIcon / NoteIcon / LinkIcon·与静态站资产同源） |
| xiyouji-agent-web/src/components/PermissionDialog.tsx | W947 | ⚠️📝 纯图标位 → 内联 SVG 组件（W947） |
| xiyouji-agent-web/src/components/InlinePermissionCard.tsx | W947 | ⚠️ 图标位 → 内联 SVG 组件（W947） |
| scripts/_w947_add_icons.py | W947 | 新增：通用图标集补 2 枚（note / link） |
| dataset/timeline.json | W949 | 数据源：22 个 icon 字段 emoji → 语义专属图标名（与中英页面逐位对拍·堵回归漏洞） |
| scripts/_w949_fix_dataset.py | W949 | 新增：数据源 icon 字段治理器（含与页面副本逐位对拍） |
| scripts/_w949_allowlist.py | W949 | 新增：字段图标位白名单重建器（扫描器实测产出 + 程序附理由） |
| scripts/check_icon_fields.py | W949 | 新增：字段图标位判据（avatar/icon/flag/stage·与白名单逐条比对） |
| scripts/check_emoji_icons.py | W949 | 第 50 门禁新增 A2 段（挂入字段图标位判据） |
| scripts/output/_w949_icon_field_allowlist.json | W949 | 新增：字段图标位白名单（71 条·扫描器实测产出） |
| scripts/_w950_normalize.py | W950 | 新增：图标光学尺寸归一器（量墨色外接框 → 统一边长 + 居中） |
| scripts/_w950_refresh_icon_paths.py | W950 | 新增：图标图形同步刷新器（资产 → 内联 SVG·复合键反查） |
| scripts/output/_w950_icon_normalize.json | W950 | 新增：45 枚图标的光学尺寸归一参数 |
| scripts/output/_cascade_files_W950.txt | W950 | 新增：本批级联清单 |

## W899 合并后收尾修正（2026-10-23）

| 文件 | W | 说明 |
|---|---|---|
| assets/promo/output/README.md | W899 | output 目录导读计数订正为实况 6 件 |
| scripts/output/_vermilion_solid_cache.json | W899 | 增量缓存重建（3 页 sha1 对齐当前页面字节） |
| scripts/output/_w899_spec.json | W899 | 本批级联 spec（10 面改写参数） |
| scripts/output/_cascade_files_W899.txt | W899 | 级联落盘清单 |
| docs/00-导读/W批次编号对账表.md | W899 | 认领行与收官回填 |
| CHANGELOG.md | W899 | W899 段 |
| HANDOVER.md | W899 | 头尾链与里程碑块 |
| README.md | W899 | 当前批次版本行 |
| STRUCTURE.md | W899 | 当前批次版本行 |
| docs/00-导读/项目说明.md | W899 | 当前批次版本行 |
| .github/workflows/README.md | W899 | 工作流层区间与里程碑尾标记 |
| site/index.html | W899 | 页脚批次链插入 W899 |
| site/data/cross-time-danmaku.html | W899 | 页脚批次链插入 W899 |
| site/data/tag-cloud.html | W899 | 页脚批次链插入 W899 |
| site/dukou-engine.html | W899 | 页脚批次链插入 W899 |
| AGENTS.md | W899 | 版本脚注条目 |
| archive/docs/AGENTS-ARCHIVE.md | W899 | 脚注滚动迁入的最老条目 |
| CITATION.cff | W899 | version 同步为 W899 |
| scripts/output/file-index.md | W899 | W899 段插入 |

## W898 宣传物料投放接线与派生（2026-10-23）

| 文件 | W | 说明 |
|---|---|---|
| assets/promo/xiyouji-flyer-a4-en.html | W898 | 英文版单页（同一栅格·EN 版专属排版微调·两页 0px 溢出） |
| assets/promo/output/xiyouji-flyer-a4-en.pdf | W898 | 英文版双面 PDF（2 页 A4） |
| assets/promo/output/xiyouji-flyer-a4-en-front.png | W898 | 英文版正面 PNG（1240×1754） |
| assets/promo/output/xiyouji-flyer-a4-en-back.png | W898 | 英文版背面 PNG（1240×1754） |
| assets/promo/README.md | W898 | 目录导读补英文版与投放接线说明 |
| scripts/_w892_export_flyer.mjs | W898 | 导出脚本加 `--en` 档（英文版 PDF + PNG） |
| README.md | W898 | 新增「📄 宣传单页（A4 双面）」物料小节 |
| site/index.html | W898 | 「看数据与工具」区新增宣传单页入口（指向仓库物料目录） |
| docs/00-导读/文档规范.md | W898 | §11.2 受管资产表新增 assets/promo/ 一行 |
| docs/00-导读/W批次编号对账表.md | W898 | 认领行与收官回填 |
| CHANGELOG.md | W898 | W898 段 |
| scripts/output/file-index.md | W898 | 同批段回写 |

## W897 协作防护修复（2026-10-23）

| 文件 | W | 说明 |
|---|---|---|
| scripts/preflight_check.py | W897 | touches 分隔符根修（`_split_touches` 兼容五种分隔符·台账与命令行同源） |
| tests/unit/test_preflight_touches.py | W897 | 新增单测 11 例（多分隔符 / 台账列解析 / 占位符归一 / 交集判定） |
| .github/workflows/ci-sim.yml | W897 | CI 侧预演 workflow（PR + push dev·干净检出跑 7 项关键门禁） |
| .github/workflows/README.md | W897 | 里程碑行上限随现役号同步 |
| scripts/output/stats.json | W897 | pytest_collected 随新增单测刷新 |
| pytest.ini | W897 | pytest_collected 标记同步 |
| docs/00-导读/W批次编号对账表.md | W897 | 认领行与收官回填 |
| CHANGELOG.md | W897 | W897 段 |
| scripts/output/file-index.md | W897 | 同批段回写 |

## W896 门禁实算口径改造（2026-10-23）

| 文件 | W | 说明 |
|---|---|---|
| scripts/tracked_files.py | W896 | 目标提交树口径单一事实源（tracked_files / tracked_in_dir / tracked_subdirs / is_tracked） |
| scripts/ci_sim.py | W896 | CI 侧预演工具（worktree 干净检出 + 关键门禁 + 自动清理·只读零风险） |
| scripts/check_folder_docs.py | W896 | 第 45 槽实算改索引口径 + 三态判据 + 计数自洽 + 口径开关 |
| scripts/gen_folder_docs.py | W896 | 生成器同步改索引口径 + 磁盘口径平行实现（自测与降级用） |
| scripts/stats.py | W896 | 全部 glob 计数改索引口径（目标提交树实算） |
| scripts/docs_index.py | W896 | scan_docs 默认 tracked_only（写盘与门禁比对共用同一函数） |
| scripts/output/stats.json | W896 | report_docs 53→54·pytest_collected 835→836·inline_css_pages 归实况 330 |
| scripts/output/stats-changelog.json | W896 | W896 变更史登记 |
| scripts/output/stats-index.md | W896 | 反向索引同步 |
| scripts/index.md | W896 | 目录清单同步（新增两脚本） |
| docs/INDEX.md | W896 | 文档索引重建（745 篇·索引口径） |
| docs/11-方案报告/计划方案/T17-任务计划执行与经验沉淀报告-2026-10-23.md | W896 | 框架第十七次执行（口径改造 + AC 表 + 3 条经验） |
| docs/00-导读/W批次编号对账表.md | W896 | 认领行与收官回填 |
| CHANGELOG.md | W896 | W896 段 |
| scripts/output/file-index.md | W896 | 同批段回写 |

## W895 BL-33 收敛批（2026-10-23）

| 文件 | W | 说明 |
|---|---|---|
| site/system.css | W895 | BL-33 收敛：page-wrap 令牌 / seal 淡底 / kpi-row 规则升全局 |
| scripts/inline_css.py | W895 | 护栏：--force 只重同步已内联页·外链转内联须 --inline-links |
| site/data/（88）site/en/（138）site/reader/（102） | W895 | 内联块按源重生成（集合差零差异） |
| scripts/_w895_bl33_inventory.py | W895 | 新增：内联块与事实源差异盘点 |
| scripts/_w895_regen_preview.py | W895 | 新增：重生成预演（sync 前证明反冲风险） |
| scripts/_w895_verify_blocks.py | W895 | 新增：重生成后集合差校验（226/226 零差异） |
| scripts/output/_w864_accent_exemptions.json | W895 | 按新实测保守核查（余 256 条） |
| docs/00-导读/W批次编号对账表.md | W895 | 认领行与收官回填 |
| CHANGELOG.md | W895 | W895 段 |
| scripts/output/file-index.md | W895 | 同批段回写 |

## W893 四画幅素材图成套批（2026-10-23）

| 文件 | W | 说明 |
|---|---|---|
| site/static/images/hero-07-liudao-lingyun.webp | W893 | 新增：Hero 素材 07/09·六盘山岭云海（山脊云海+七人单行+朱砂小旗·净空带 473px） |
| site/static/images/hero-08-yunhai-chengqiao.webp | W893 | 新增：Hero 素材 08/09·云海石拱桥（云海+石桥+白马与僧影+朱砂彩带·净空带 451px） |
| site/static/images/hero-09-shijue-wangluo.webp | W893 | 新增：Hero 素材 09/09·石觉网罗（根须网+朱砂节点+赭金连接弧·净空带 485px） |
| site/static/images/card-25-santiebaigujing.webp | W893 | 新增：卡片封面 25/27·三打白骨精（石窟+骷髅剪影+朱砂布条·净空带 378px） |
| site/static/images/card-26-wukong-jingu.webp | W893 | 新增：卡片封面 26/27·悟空金箍棒（背身持棒+虎纹围裙+朱砂绦·净空带 392px） |
| site/static/images/card-27-rejiao-fenxi.webp | W893 | 新增：卡片封面 27/27·热力分析（情感点阵+朱砂色带+赭金散点·净空带 404px） |
| site/static/images/post-07-gu-shan-yingxue.webp | W893 | 新增：竖版长图 07/09·孤山映雪（古峰+崖松+朱砂塔灯·净空带 456px） |
| site/static/images/post-08-tangseng-chanshi.webp | W893 | 新增：竖版长图 08/09·唐僧禅释（背身持锡杖+背光晕+朱砂念珠·净空带 534px） |
| site/static/images/post-09-bajiaoshan-zhaoyun.webp | W893 | 新增：竖版长图 09/09·八戒造云（背身扛耙+朱砂领结·净空带 487px） |
| site/static/images/og-13-changgui-shanmen.webp | W893 | 新增：分享图 13/15·残破山门（断门+荒草薄雾+朱砂经幡·净空带 169px） |
| site/static/images/og-14-shaseng-denggao.webp | W893 | 新增：分享图 14/15·沙僧登高（石矶+苍鹭展翅+朱砂浮标·净空带 253px） |
| site/static/images/og-15-shijian-liejian.webp | W893 | 新增：分享图 15/15·时间刻痕（刻痕序列+朱砂刻度+赭金标记·净空带 264px） |
| scripts/_w893_gen_args.py | W893 | 十二张生成参数（锚点沿用 W882 改写版·四画幅各三张·拉丁方主题） |
| scripts/_w893_finalize.py | W893 | 定稿脚本（覆盖缩放 + 保主体/保净空带裁切 + WebP 落盘） |
| scripts/_w893_verify.py | W893 | 五道量化验收脚本（尺寸/净空带/主体墨量/朱砂/规则线） |
| scripts/output/_w893_spec.json | W893 | 本批 spec 十字段（CHANGELOG 版段递延·待顶段推进后补写） |
| docs/11-方案报告/计划方案/T16-任务计划执行与经验沉淀报告-2026-10-23.md | W893 | 新增：T-16 框架报告（四画幅素材图成套批） |
| docs/00-导读/W批次编号对账表.md | W893 | 认领行与收官回填 |

## W892 宣传单页批（2026-10-23）

| 文件 | W | 说明 |
|---|---|---|
| assets/promo/xiyouji-flyer-a4.html | W892 | 宣传单页唯一真源（A4 双面·12 栏栅格·10 枚内联 SVG·零外域） |
| assets/promo/hero-main-visual.png | W892 | 本批新生成专属主视觉（宣纸浓墨山影 + 朱砂钤记·色归一化到 #FAF7F0） |
| assets/promo/output/xiyouji-flyer-a4.pdf | W892 | 双面 PDF（2 页 A4·子集嵌入思源宋体） |
| assets/promo/output/xiyouji-flyer-a4-front.png | W892 | 正面 PNG（1240×1754·150dpi） |
| assets/promo/output/xiyouji-flyer-a4-back.png | W892 | 背面 PNG（1240×1754·150dpi） |
| assets/promo/README.md | W892 | 目录导读（真源说明 + 复算命令 + 数字口径警示） |
| scripts/_w892_export_flyer.mjs | W892 | 三件套导出（内置静态服务器 + 字体/外域/溢出三探针） |
| scripts/_w892_probe.mjs | W892 | 版式判据探针（末块底边 vs 内容底边·两页须 0px 溢出） |
| docs/11-方案报告/计划方案/T15-任务计划执行与经验沉淀报告-2026-10-23.md | W892 | 框架第十五次执行（规划五表 + AC 验收 + 5 条经验） |
| docs/11-方案报告/README.md | W892 | §二 补登记 T-15（篇数 17→18） |
| STRUCTURE.md | W892 | assets 段新增 promo/ 登记 + report_docs 标记同步 |
| docs/00-导读/W批次编号对账表.md | W892 | 认领行与收官回填 |
| CHANGELOG.md | W892 | W892 段 |
| scripts/output/file-index.md | W892 | 同批段回写 |

## W891 en 收尾批（2026-10-23）

| 文件 | W | 说明 |
|---|---|---|
| site/en/（138 页） | W891 | A 渠 15 处容器归并 + nav-back 49 页文字态 + 间距令牌化 3,353 处 |
| scripts/_w891_en_survey.py | W891 | en 收尾前置盘点（容器值/断点/nav-back 变体/间距量） |
| scripts/_w891_en_migrate.py | W891 | A 渠 + nav-back 迁移驱动（INLINED 跳过·@media 占位保护） |
| scripts/output/_w864_accent_exemptions.json | W891 | W887 分册 −46 条 nav-back（随批递减·全簿 256） |
| docs/00-导读/W批次编号对账表.md | W891 | 认领行与收官回填 |
| CHANGELOG.md | W891 | W891 段 |
| scripts/output/file-index.md | W891 | 同批段回写 |

## W890 CI 阻塞项清偿批（2026-10-23）

| 文件 | W | 说明 |
|---|---|---|
| `tests/unit/test_vermilion_solid.py` | W890 | scope 断言改判为新契约（zh 审计面 ∪ en 全量·W887 扩范围后） |
| `scripts/_w851_j1_name_audit.py` | W890 | DEFER_HOLD_CHECKS 收敛为 1 条（删 W876 已改值的两项·原值未动契约对已落地项不适用） |
| `scripts/tmpe_tidy.py` | W890 | 新增 `_pid_alive()` 跨平台存活探针（Windows 用 OpenProcess+GetExitCodeProcess·非终止式）+ RunLock 默认参数改运行时解析 |
| `scripts/check_no_brand_refs.py` | W890 | ruff 四项清零（UP009 删 encoding 声明 / UP015 删冗余 mode / F841 删死变量 args / B007 循环变量改名） |
| `scripts/check_plan_template.py` | W890 | ruff 两项清零（UP009 删 encoding 声明 / E741 歧义变量名改名） |
| `scripts/requirements.txt` | W890 | Pillow 12.3.0→13.0.0（清 25 个 CVE·含 GHSA-78g4-xqwv-q3g8） |
| `docs/11-方案报告/计划方案/T14-任务计划执行与经验沉淀报告-2026-10-23.md` | W890 | 本批框架交付物（取证 / 修复 / 验收 / 复盘） |
| `docs/00-导读/W批次编号对账表.md` | W890 | W890 认领行 + 收官回填 |
| `docs/11-方案报告/README.md` | W890 | 计划方案目录索引登记 |
| `scripts/output/_w890_spec.json` | W890 | 本批级联 spec（10 键） |
| `scripts/output/_cascade_files_W890.txt` | W890 | 本批级联落盘清单 |

