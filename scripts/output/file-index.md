# xiyouji 文件反向索引

> 与 [CHANGELOG.md](../../CHANGELOG.md) 配套：给定文件，查它被改过几次、每次对应哪个 W 条目。
> W### 编号规则见 CHANGELOG.md 顶部。
> 创建于 2026-07-22（v0.8 双索引改造）
>
> **历史归档**：W031-W087（v2.0.4-v2.0.60）site/data/ 部分已迁移至 [file-index-ARCHIVE.md](../../archive/docs/file-index-ARCHIVE.md)；W422 再归档 W393-W416 段；W511 归档 W417-W448 段 + W449-W463 损坏区尾部清理。；W736 归档 W449-W699 段（与 CHANGELOG 现役边界统一至 W700）。本文件仅保留 W700+ 现役索引。
>
> **维护契约**：本索引按 W 追加登记（每文件 1 行 + 一句摘要），历史段禁改；新增/变更文件必须先有 CHANGELOG 对应 W 段再登记（双索引铁律），禁止无 W 段单独登记。

---


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

## W889 展示面复位批（2026-10-23）

| 文件 | W | 说明 |
|---|---|---|
| `.github/README.md` → `.github/README-internal.md` | W889 | 目录导读改名让位——原名会抢占 GitHub 仓库主页展示位（优先级 `.github/` > 根目录 > `docs/`）·转人工维护件（去生成来源标记） |
| `.github/index.md` | W889 | 目录清单刷新（文件 2→3 项·导读指针自适应指向 README-internal.md） |
| `scripts/gen_folder_docs.py` | W889 | 新增「主页展示位保护」常量与判定（精确单文件排除·不排整个 .github 树）+ index.md 导读指针自适应 |
| `scripts/check_folder_docs.py` | W889 | 第 45 门禁 C1 豁免与生成器同源（共用 gen.showcase_guarded） |
| `scripts/check_doc_sync.py` | W889 | 第 31 门禁新增 C7 断言（根 README 在位时 .github/README.md 必须不存在·self-test 增至 26 例） |
| `README.md` | W889 | 首屏整体重排 + 30 秒上手速览块 + 抬头四行降噪入开发者专区 |
| `docs/11-方案报告/计划方案/T13-任务计划执行与经验沉淀报告-2026-10-23.md` | W889 | 本批框架交付物（计划 / 决策 / 验收 / 复盘） |
| `docs/00-导读/W批次编号对账表.md` | W889 | W889 认领行登记（touches 12 项） |
| `docs/11-方案报告/README.md` | W889 | 计划方案目录索引登记 |
| `scripts/output/stats.json` | W889 | stats 实算刷新 |
| `scripts/output/_w889_spec.json` | W889 | 本批级联 spec（10 键） |

## W888 剩余素材接线批·两路（2026-10-23）

| 文件 | W | 说明 |
|---|---|---|
| site/data/（83 页） | W888 | 路 A：viz 4 张浅底图接中文数据页卷末位（插入锚点在 `</main>` 之前·不触碰图表容器与正文） |
| site/reader/（6 页：ch007/014/015/023/027/030） | W888 | 路 B：chap 1:1 百回母版接对应回目页页头（回目 H1 之后·配图位非封面位） |
| site/system.css | W888 | `.viz-illustration` / `.chapter-plate` 规则源（与各页内联副本双写·file:// 下 CSP 拦外链样式表） |
| scripts/build_reader.py | W888 | 生成器条件化（STYLE 常量 + CHAPTER_PLATES 映射 + `_render_one_page` 条件化插入） |
| scripts/_w888_wire.py | W888 | 路 A 接线脚本（母题映射 + 内联副本补规则 + 暗色模式隐藏） |
| scripts/_w888_chapter_plate.py | W888 | 路 B 母版接线脚本 |
| scripts/_w888_index_revert.py | W888 | 索引回退脚本 |
| scripts/output/_w888_spec.json | W888 | 本批级联 spec |
| docs/11-方案报告/计划方案/T12-任务计划执行与经验沉淀报告-2026-10-23.md | W888 | 本批框架交付物（消费位侦察先行 + 四类不做留证） |
| docs/11-方案报告/README.md | W888 | 计划方案目录索引登记 |

## W887 en 迁移批 2·收口批（2026-10-23）

| 文件 | W | 说明 |
|---|---|---|
| site/en/（110 页） | W887 | C 渠 126 条规则 + seal 淡底 110 页 + KPI 顶条规则 57 页 |
| scripts/_w886_en_migrate.py | W887 | 批 6 合并定义（批 2-5 合一） |
| scripts/output/_w886_en_audit_b6.json | W887 | 批 6 前置审计子集（C 809·实底 508） |
| scripts/output/_w886_en_audit_b6_after.json | W887 | 批 6 迁移后审计（C 213·实底 313） |
| scripts/output/_w887_needed.json | W887 | 待登记豁免清单（181 条·生成输入） |
| scripts/output/_w864_accent_exemptions.json | W887 | W887 分册 181 条（语义 64/功能 61/首卡 56·全簿 302） |
| scripts/check_vermilion_solid.js | W887 | scopePages 并入 en（范围 96→234 页） |
| scripts/output/_vermilion_solid_cache.json | W887 | 缓存重建（234 页） |
| docs/00-导读/W批次编号对账表.md | W887 | 认领行与收官回填 |
| CHANGELOG.md | W887 | W887 段 |
| scripts/output/file-index.md | W887 | 同批段回写 |

## W886 en 迁移批 1·入口与结构 28 页（2026-10-22）

| 文件 | W | 说明 |
|---|---|---|
| scripts/_w886_en_audit.py | W886 | 新增：en 四渠现状审计（C/实底 浏览器实测 + 令牌旧值/容器字面量静态） |
| scripts/_w886_en_migrate.py | W886 | 新增：en B 渠机械化驱动（seal→淡底 + KPI 顶条按行规则 + 批审计子集导出） |
| scripts/output/_w886_en_audit.json | W886 | en 全量审计（C 1,084/62 页·实底 767/135 页） |
| scripts/output/_w886_en_audit_b1.json | W886 | 批 1 前置审计子集（C 275·实底 259） |
| scripts/output/_w886_en_audit_b1_after.json | W886 | 批 1 迁移后审计（C 38·实底 205） |
| site/en/（28 页） | W886 | C 渠 49 条规则 + seal 淡底 28 页 + KPI 顶条规则 16 页 |
| scripts/output/_w864_accent_exemptions.json | W886 | W886 分册 25 条（四类口径·全簿 121 条） |
| docs/00-导读/W批次编号对账表.md | W886 | 认领行与收官回填 + W885 段状态翻转 |
| CHANGELOG.md | W886 | W886 段 + W885 段回补 |
| scripts/output/file-index.md | W886 | 同批两段回写 |

## W885 素材接线批（2026-10-22）

| 文件 | W | 说明 |
|---|---|---|
| site/data/*.html（87 页） | W885 | 改：`.hero` 暗带接入深底直显版装饰插画 img + 内联副本补 .hero-ornament 规则（按页名映射四类母题） |
| site/en/*.html（126 页） | W885 | 改：同 site/data（英文侧同款装饰插画与规则） |
| site/system.css | W885 | 改：追加 .hero-ornament 规则（源·下次 inline_css 重跑继承） |
| site/index.html | W885 | 改：浅色 .masthead 铺 hero-01 山河云海横幅（文字落在图底部留白带） |
| site/static/images/viz-dark-01-network.webp | W885 | 新增：深底直显版装饰插画 01/04·根须网（640×640·深底映射为 alpha 渐变） |
| site/static/images/viz-dark-02-heatmap.webp | W885 | 新增：深底直显版装饰插画 02/04·疏密墨点阵（640×640·默认母题） |
| site/static/images/viz-dark-03-radar.webp | W885 | 新增：深底直显版装饰插画 03/04·放射线（640×640） |
| site/static/images/viz-dark-04-timeline.webp | W885 | 新增：深底直显版装饰插画 04/04·纵向刻痕序列（640×640） |
| scripts/_w885_wire.py | W885 | 新增：接线批处理脚本（system.css 规则 + 213 页装饰 img + 内联副本补规则 + 首页底图·幂等） |
| scripts/_w885_viz_alpha.py | W885 | 新增：深底插画 alpha 化脚本（按亮度把深底映射为透明渐变·消除方框） |
| scripts/_w885_index_revert.py | W885 | 新增：搜索索引他方在途条目回退器（逐条比对·源文件未入库者按 HEAD 版回退） |
| scripts/output/_w885_spec.json | W885 | 本批 spec 十字段（CHANGELOG 版段递延·待补段批按号序回写） |
| docs/00-导读/W批次编号对账表.md | W885 | 认领行与收官回填 |


## W883 阶段 5 机检门禁批（2026-10-22）

| 文件 | W | 说明 |
|---|---|---|
| scripts/check_vermilion_solid.js | W883 | 新增：第 49 门禁朱砂实底限额（浏览器实测+豁免登记簿+增量缓存+自检 14 例） |
| tests/unit/test_vermilion_solid.py | W883 | 新增：第 49 门禁单测（自检/纯逻辑/接线/范围 11 例） |
| scripts/verify_delivery.py | W883 | 第 49 槽 StrictGate 接线（段名+scope+gate 定义） |
| scripts/output/_w864_accent_exemptions.json | W883 | W883 分册 24 条（四类存量裁决·全簿 96 条） |
| scripts/output/_vermilion_solid_cache.json | W883 | 新增：增量缓存（96 页 sha1+分类计数·随批入库） |
| scripts/output/_vermilion_solid_report.json | W883 | 新增：门禁报告（每页实测/豁免/非豁免/状态） |
| site/dashboard.html | W883 | .seal 徽章实底→淡底（v4 §3.2·与 W864 批 .seal 转换同模式） |
| scripts/_w876_site_audit.py | W883 | fill 口径校正（≥3px/盒面积 → ≥2px/条带面积） |
| scripts/output/_w876_site_audit_head.json | W883 | 校正复跑（HEAD 快照·fill 457/89 与原审计一致） |
| scripts/output/_w876_site_audit_final.json | W883 | 校正复跑（终态·457/89） |
| AGENTS.md | W883 | §4.2 48→49 槽 + 第 49 槽条目 + 组号范围 |
| docs/agent/gates.md | W883 | 49 槽标题/速查表/第 49 槽完整定义 |
| README.md STRUCTURE.md docs/00-导读/项目说明.md | W883 | 版本行与门禁计数（48→49） |
| pytest.ini | W883 | collected 计数 823→834（+11 例） |
| docs/11-方案报告/系统架构方案-分层模块与部署-2026-10-20.md | W883 | gate_count 48→49 |
| scripts/output/stats.json | W883 | 刷新（gate_count 49·2 键） |
| site/data/search.html | W883 | 搜索索引刷新（gates.md 标题变更·CSP 重算） |
| docs/00-导读/W批次编号对账表.md | W883 | 认领行与收官回填 + W877-W882 六行段状态翻转 + W877 豁免划销 |
| CHANGELOG.md | W883 | W883 段 + W877-W882 六段按号序回补（174→180 段） |
| scripts/output/file-index.md | W883 | 同批七段回写（174→180） |

## W882 缺口第 4–6 项合并批（2026-10-22）

| 文件 | W | 说明 |
|---|---|---|
| site/static/images/post-01-wukong.webp | W882 | 新增：竖版海报 01/06·悟空（3:4 1200×1600·背身持棒·净空带 438px） |
| site/static/images/post-02-tangseng.webp | W882 | 新增：竖版海报 02/06·唐僧（3:4·僧影锡杖背光·净空带 514px） |
| site/static/images/post-03-bajie.webp | W882 | 新增：竖版海报 03/06·八戒（3:4·长耳钉耙虎纹裙·净空带 438px） |
| site/static/images/post-04-shaseng.webp | W882 | 新增：竖版海报 04/06·沙僧（3:4·卷发深须宝杖·净空带 437px） |
| site/static/images/post-05-bailongma.webp | W882 | 新增：竖版海报 05/06·白龙马（3:4·白马回首·朱砂鞍鞯·净空带 503px） |
| site/static/images/post-06-changlu.webp | W882 | 新增：竖版海报 06/06·西行长路（3:4·远山长路·朱砂小旗·净空带 545px） |
| site/static/images/chap-07.webp | W882 | 新增：百回母版 01/06·回 07 八卦炉（同一母版·丹炉火光·净空带 423px） |
| site/static/images/chap-14.webp | W882 | 新增：百回母版 02/06·回 14 心猿归正（同一母版·断树猿影·净空带 376px） |
| site/static/images/chap-15.webp | W882 | 新增：百回母版 03/06·回 15 蛇盘山（同一母版·蛇形长脊·净空带 384px） |
| site/static/images/chap-23.webp | W882 | 新增：百回母版 04/06·回 23 试禅心（同一母版·寺门菩提·净空带 450px） |
| site/static/images/chap-27.webp | W882 | 新增：百回母版 05/06·回 27 三打白骨精（同一母版·月下破寺白影·净空带 364px） |
| site/static/images/chap-30.webp | W882 | 新增：百回母版 06/06·回 30 宝象国（同一母版·宫室屋脊白马·净空带 427px） |
| site/static/images/viz-01-network.webp | W882 | 新增：可视化插画 01/04·网络图页（根须网·朱砂结点·640×640） |
| site/static/images/viz-02-heatmap.webp | W882 | 新增：可视化插画 02/04·热力图页（疏密墨点阵·640×640） |
| site/static/images/viz-03-radar.webp | W882 | 新增：可视化插画 03/04·雷达图页（放射线·朱砂端点·640×640） |
| site/static/images/viz-04-timeline.webp | W882 | 新增：可视化插画 04/04·时间线页（纵向刻痕序列·640×640） |
| scripts/output/_w882_spec.json | W882 | 本批 spec 十字段（CHANGELOG 版段递延·待补段批按号序回写） |
| docs/00-导读/W批次编号对账表.md | W882 | 认领行与收官回填 |


## W881 人物补位素材批（2026-10-22）

| 文件 | W | 说明 |
|---|---|---|
| site/static/images/card-13-bajie-yuexia.webp | W881 | 新增：人物方图 13/24·八戒月下负囊（背身·长耳·赭金虎纹裙·净空带 349px） |
| site/static/images/card-14-bajie-choupa.webp | W881 | 新增：人物方图 14/24·八戒持耙守关（九齿钉耙·朱砂缨·净空带 400px） |
| site/static/images/card-15-bajie-zuoxie.webp | W881 | 新增：人物方图 15/24·八戒坐歇担前（杖横膝·朱砂结·净空带 395px·横贯硬线已程序化修复） |
| site/static/images/card-16-bajie-yunzhong.webp | W881 | 新增：人物方图 16/24·八戒雨中奔行（斗笠遮面·湿笔雨丝·净空带 344px） |
| site/static/images/card-17-bajie-denggao.webp | W881 | 新增：人物方图 17/24·八戒登高远眺（崖边背身·云海·朱砂小旗·净空带 249px） |
| site/static/images/card-18-bajie-daodan.webp | W881 | 新增：人物方图 18/24·八戒挑担赶路（侧身·担挑双囊·净空带 401px） |
| site/static/images/card-19-shaseng-dujiang.webp | W881 | 新增：人物方图 19/24·沙僧负杖渡江（卷发深须·降妖宝杖·朱砂佛珠·净空带 400px） |
| site/static/images/card-20-shaseng-zhenshui.webp | W881 | 新增：人物方图 20/24·沙僧宝杖镇水（杖立水中·涟漪·净空带 301px） |
| site/static/images/card-21-shaseng-shouye.webp | W881 | 新增：人物方图 21/24·沙僧守夜（石上独坐·孤灯光晕·净空带 407px） |
| site/static/images/card-22-shaseng-fuzhong.webp | W881 | 新增：人物方图 22/24·沙僧负重前行（负囊登阶·雨中·净空带 300px） |
| site/static/images/card-23-shixiong-bingli.webp | W881 | 新增：人物方图 23/24·师徒山径并肩（八戒在前挑担·沙僧持杖在后·朱砂小旗·净空带 341px） |
| site/static/images/card-24-shixiong-shanmen.webp | W881 | 新增：人物方图 24/24·师徒山门前对峙（八戒持耙在前·沙僧持杖在后·朱砂门印·净空带 310px） |
| site/static/images/og-03-bailongma.webp | W881 | 修：白龙马 OG 图的横贯硬线伪影（提示词字面化产物）·程序化渐变回填修复 |
| site/static/img/og-cover-ink-en.jpg | W881 | 修：英文站 og:image 的横贯硬线伪影（该图即英文站每次分享的封面）·程序化渐变回填修复 |
| site/static/img/og-cover-ink-en.png | W881 | 修：英文站 og:image 无损母版的横贯硬线伪影·程序化渐变回填修复 |
| scripts/_w881_rule_line_scan.py | W881 | 新增：横贯硬线伪影检测器（按行暗像素占比 ≥65% 且邻行骤降判定·可复算） |
| scripts/_w881_fix_rule_line.py | W881 | 新增：横贯硬线定点修复器（规则行块＋向下并入洗边暗行→逐列垂直渐变回填） |
| scripts/output/_w881_spec.json | W881 | 本批 spec 十字段（CHANGELOG 版段递延·待补段批按号序回写） |
| docs/00-导读/W批次编号对账表.md | W881 | 认领行与收官回填 |


## W880 分语言 og:image 接线批（2026-10-22）

| 文件 | W | 说明 |
|---|---|---|
| scripts/_w880_og_image_split.py | W880 | 新增：一次性批处理脚本·全站 855 页 og:image 分语言改指新 URL（页内旧 URL 全出现处一并替换·含内联 JSON-LD·行尾原样保留） |
| scripts/check_seo_head.py | W880 | 改（管控件·用户已批准）：R1 逐页期望值改分语言（og_image_for(rel)·en/ 前缀为英文站）+ R4 改校两张现役分享图（旧排版卡保留存在性与体积校） |
| scripts/inject_seo_head.py | W880 | 改：全站 SEO 注入器按 is_en 分流 og:image（生成端同步·防下次再注入回退） |
| scripts/build_reader.py | W880 | 改：reader 生成器（仅产出中文页）og:image 取中文站分享图（生成端同步·防下次重建回退） |
| scripts/gen_og_cover.py | W880 | 改：文档字符串注明其产出（排版卡）已降级为旧版留档·现行分享图为两张水墨图·切勿再手改生成物 |
| site/static/img/og-cover.png | W880 | 改：恢复为 gen_og_cover.py 的生成物版本（49,490 B·可复现）——W879 的手工水墨图被移至非生成物的新文件 |
| site/（855 页） | W880 | 改：og:image 一行分语言改指新 URL（中文 717 页 → og-cover-ink-zh.jpg·英文 138 页 → og-cover-ink-en.jpg）·含内联 JSON-LD 的 image 字段 |
| scripts/output/_w880_spec.json | W880 | 本批 spec 十字段（CHANGELOG 版段递延·待补段批按号序回写） |
| docs/00-导读/W批次编号对账表.md | W880 | 认领行与收官回填 |


## W879 暗底/夜读适配水墨素材批（2026-10-22）

| 文件 | W | 说明 |
|---|---|---|
| site/static/images/ink-mountains-hero.webp | W879 | 改：现役 848 页共用的暗色诗段底图·原地替换为「浅底浓墨」显影版（合成后亮度跨度 0.0080→0.0789·×9.9） |
| site/static/images/ink-mountains-path.webp | W879 | 新增：暗底适配底图 02/04·长路入山（浓墨林影+朱砂灯点·显影跨度 0.0768·×9.6） |
| site/static/images/ink-mountains-pine.webp | W879 | 新增：暗底适配底图 03/04·松崖孤塔（浓墨崖松+朱砂崖印·显影跨度 0.0718·×9.0） |
| site/static/images/ink-mountains-night.webp | W879 | 新增：暗底适配底图 04/04·深底浅墨直显版（夜读模式专用·自身对比度 0.5205） |
| site/static/img/og-cover.png | W879 | 改：全站 855 页共用的 og 分享图·原地替换为水墨图（取 og-09 山口关隘·PNG-8 256 色 143.0KB·门禁 R4 上限 300KB·URL 不变故 R1 全绿） |
| site/static/img/og-cover-ink-zh.jpg | W879 | 新增：分语言版分享图（中文·取 og-09 山口关隘·JPG 129.6KB·微信与 Facebook 不吃 webp 故出 JPG·备而未接线） |
| site/static/img/og-cover-ink-en.jpg | W879 | 新增：分语言版分享图（英文·取 og-03 白龙马·JPG 53.1KB·备而未接线） |
| site/static/img/og-cover-ink-zh.png | W879 | 新增：分语言版分享图无损母版（中文·PNG 497.2KB） |
| site/static/img/og-cover-ink-en.png | W879 | 新增：分语言版分享图无损母版（英文·PNG 162.7KB） |
| scripts/output/stats.json | W879 | 改：inline_css_pages 850→330（更正 W878 刷入的并行重生成中途瞬时值·磁盘实算零差异） |
| scripts/output/stats-changelog.json | W879 | 改：随 stats 刷新的变更史追加一条 |
| scripts/output/stats-index.md | W879 | 改：随 stats 刷新的反向索引重渲染 |
| CHANGELOG.md | W879 | 改：顶部「全站页数口径」块与键值枚举的 inline_css_pages 标记 850→330 |
| docs/11-方案报告/系统架构方案-分层模块与部署-2026-10-20.md | W879 | 改：§113「内联 CSS 覆盖页」表行标记 850→330 |
| scripts/output/_w879_spec.json | W879 | 本批 spec 十字段（CHANGELOG 版段递延·待补段批按号序回写） |
| docs/00-导读/W批次编号对账表.md | W879 | 认领行与收官回填 |


## W878 OG 分享缩略图素材成套批（2026-10-22）

| 文件 | W | 说明 |
|---|---|---|
| site/static/images/og-01-kongkong.webp | W878 | 新增：OG 分享图 01/12·悟空（猴相背影+金箍棒+红绦·净空带 222px·二版） |
| site/static/images/og-02-tangseng.webp | W878 | 新增：OG 分享图 02/12·唐僧（僧影+锡杖+背光晕·净空带 185px） |
| site/static/images/og-03-bailongma.webp | W878 | 新增：OG 分享图 03/12·白龙马（白马回首·鬃如云·朱砂鞍鞯·净空带 294px） |
| site/static/images/og-04-jingubang.webp | W878 | 新增：OG 分享图 04/12·金箍棒（棒身金环+朱砂缠绳·净空带 163px） |
| site/static/images/og-05-bajiaoshan.webp | W878 | 新增：OG 分享图 05/12·芭蕉扇（半展大叶·朱砂扇柄结·净空带 198px） |
| site/static/images/og-06-jingping.webp | W878 | 新增：OG 分享图 06/12·净瓶（白玉瓶+柳枝+朱砂丝绦·净空带 204px·二版） |
| site/static/images/og-07-qujingchuanshan.webp | W878 | 新增：OG 分享图 07/12·曲径穿山（远峰层叠+朱砂小旗·净空带 187px·二版） |
| site/static/images/og-08-hequshiqiao.webp | W878 | 新增：OG 分享图 08/12·河曲石桥（石桥+舟+朱砂小灯·净空带 182px·二版） |
| site/static/images/og-09-shankouguanai.webp | W878 | 新增：OG 分享图 09/12·山口关隘（断崖石阶+孤塔+朱砂崖印·净空带 222px·二版） |
| site/static/images/og-10-canjuan.webp | W878 | 新增：OG 分享图 10/12·半展残卷（空卷+轴头+朱砂签条·净空带 222px·二版） |
| site/static/images/og-11-gudeng.webp | W878 | 新增：OG 分享图 11/12·孤灯（铜台灯+灯焰光晕+浓墨夜色·净空带 195px） |
| site/static/images/og-12-tongjing.webp | W878 | 新增：OG 分享图 12/12·铜镜（古镜+淡影+朱砂小印·净空带 252px） |
| scripts/output/_w878_spec.json | W878 | 本批 spec 十字段（CHANGELOG 版段递延·待补段批按号序回写） |
| docs/00-导读/W批次编号对账表.md | W878 | 认领行与收官回填 |


## W877 计划方案未落地项核查批（2026-10-22）

| 文件 | W | 说明 |
|---|---|---|
| docs/11-方案报告/计划方案/T09-任务计划执行与经验沉淀报告-2026-10-22.md | W877 | 计划方案未落地项核查 + 模板符合性复核报告（217 项核销 · 32 判据矩阵） |
| docs/11-方案报告/README.md | W877 | §二 登记 T-09（计数 10→12 篇 + 编号列订正 1–12）+ 新增 §四 交付物模板规范（强制） |
| docs/INDEX.md | W877 | 文档索引重建（736 → 737 篇） |
| scripts/output/_w877_spec.json | W877 | 本批 spec 十字段（供补段批按号序回写 W875–W877） |
| scripts/output/_w877_template_matrix.json | W877 | 11 份计划件 × 32 项判据符合性矩阵 |
| scripts/output/colorblind-baseline.txt | W877 | 色盲安全存量基线重冻（17417 → 17430 对·代做 W876 阶段 5 机检门禁） |
| scripts/output/stats.json | W877 | report_docs 45→46 刷新（stats.py --w W877） |
| scripts/output/stats-changelog.json | W877 | 同批 stats 变更史刷新 |
| scripts/output/stats-index.md | W877 | 同批 stats 索引刷新 |
| site/data/search.html | W877 | 站内搜索索引重生成（新增 T-09 条目·zh 840 / en 882） |
| site/en/search.html | W877 | 英文站搜索索引重生成 + CSP 哈希重算（2 页·856 页零漂移） |
| STRUCTURE.md | W877 | report_docs 标记 45→46 同步 |
| docs/11-方案报告/系统架构方案-分层模块与部署-2026-10-20.md | W877 | report_docs 标记 45→46 同步（连带面） |
| docs/00-导读/W批次编号对账表.md | W877 | W877 认领行 + 递延版段豁免 bullet + W858/W860/W865 三行收官回填 |


## W876 对比度专项批·C 渠与值切换（2026-10-22）

| 文件 | W | 说明 |
|---|---|---|
| site/tokens.css | W876 | --chart-3 #C9A063→#B38F58 · 暗色 --accent #E0604F→#E46250 |
| site/data/（63 页） | W876 | C 渠规则级换色 173 条 color 规则（--accent→--accent-text） |
| site/en/ site/reader/（326 页） | W876 | INLINED 副本两处令牌值靶向同步（不走 regenerate·保迁移成果） |
| site/dukou-engine.html | W876 | 根级 INLINED 页两处令牌值靶向修复（inline_css 根级 skip 绕过） |
| scripts/_w876_c_text_swap.py | W876 | C 渠规则级换色器（类名+标签双模式·--audit 指定审计） |
| scripts/_w876_value_check.py | W876 | 值切换计算样式锚点校验（搜索式断言·重建版·四组锚点） |
| scripts/_w876_site_audit.py | W876 | 新增：C 渠+朱砂实底审计器（原审计器未入库·按产物校准复现 1087/457） |
| scripts/_w876_diff_audit.py | W876 | 新增：静态 diff 分类审计（三类之外与 HEAD 逐字节一致·负向查视） |
| scripts/_w876_baseline_probe.py | W876 | 新增：24 页前后计算样式对拍（只现三类预期变迁） |
| scripts/_w876_backfill_w875.py | W876 | 新增：W875 单段补数驱动（补段工具无筛选·防误补 W877-W881） |
| scripts/output/_w876_site_audit.json | W876 | 前置审计（1,087 处落 bg·64 页） |
| scripts/output/_w876_site_audit_final.json | W876 | 终态审计（253 处·27 页·复评清单 6 页） |
| scripts/output/_w876_site_audit_head.json | W876 | HEAD 快照校准审计（精确复现 1,087/64·验证快照=审计输入态） |
| scripts/output/_w876_baseline_before.json | W876 | 24 页 before 计算样式快照（HEAD 树·双主题） |
| scripts/output/_w876_baseline_after.json | W876 | 24 页 after 计算样式快照（重建树·双主题） |
| scripts/output/_w876_baseline_diff.json | W876 | 对拍分类结果（2,195 处差异零未预期·T1-T4 四类） |
| scripts/output/_w876_c_swap_report.json | W876 | 换色报告（63 页·173 规则·复评清单） |
| scripts/output/_w876_spec.json | W876 | 本批 spec 十字段 |
| docs/00-导读/design.md | W876 | 设计文档令牌表（两处值切换同步） |
| scripts/output/design-tokens.json | W876 | 令牌导出版（两处值切换同步） |
| scripts/index.md | W876 | 脚本册（+4 个 _w876 脚本） |
| scripts/output/index.md | W876 | 产物册（+4 个 _w876 JSON） |
| scripts/output/README.md | W876 | 产物目录说明（计数同步） |
| docs/00-导读/W批次编号对账表.md | W876 | 认领行与收官回填 + BL-33 登记 |

## W875 设计迁移 B11 阅读页 622 页（2026-10-22）

| 文件 | W | 说明 |
|---|---|---|
| scripts/build_reader.py | W875 | STYLE 常量 18 处补丁（容器 760→--container-read · 间距 11 处 · 文本色 7 处两值互换） |
| site/reader/（622 页） | W875 | 全量重生成（100 章回 + 216 人物 + 210 主题 + 35 文化 + 14 诗词 + 45 延伸 + 目录/hub） |
| scripts/output/_w875_spec.json | W875 | 本批 spec 十字段 |
| docs/00-导读/W批次编号对账表.md | W875 | 认领行与收官回填 |


## W874 递延版段补写批（2026-10-22）

| 文件 | W | 说明 |
|---|---|---|
| CHANGELOG.md | W874 | 补写 W865-W873 九段（162→171 段·号序完好）+ 本批 W874 段 |
| scripts/output/file-index.md | W874 | 补写九段反向索引（162→171 段） |
| scripts/output/_w874_spec.json | W874 | 本批 spec 十字段 |
| docs/00-导读/W批次编号对账表.md | W874 | 认领行与收官回填·九批豁免登记转历史 |


## W873 设计迁移 B10 工具与检索 8 页（2026-10-22）

| 文件 | W | 说明 |
|---|---|---|
| site/data/data-explorer.html | W873 | B10 迁移：容器令牌化 + 间距（选中态进豁免） |
| site/data/graph-explorer.html | W873 | B10 迁移：容器令牌化（零实底·纯令牌化） |
| site/data/search.html | W873 | B10 迁移：容器令牌化（选中态进豁免） |
| site/data/material-archaeology.html | W873 | B10 迁移：容器令牌化 + KPI 顶条 4→1 + artifact-card 8→1 + seal 淡底（tag ×3 进豁免） |
| site/data/ming-political-thought-comparison.html | W873 | B10 迁移：容器令牌化 + KPI 顶条 6→1 + seal 淡底（a.active 进豁免） |
| site/data/power-resources.html | W873 | B10 迁移：容器令牌化 + seal 淡底（faction-card 进豁免） |
| site/data/magic-system.html | W873 | B10 迁移：容器令牌化 + seal 淡底（rank-badge ×5 进豁免） |
| site/data/theological-intervention-network.html | W873 | B10 迁移：容器 1280→1120 归并 + KPI 顶条 5→1 + seal 淡底 |
| scripts/output/_w873_accent_audit.json | W873 | 新增：B10 朱砂落点审计 |
| scripts/output/_w873_diff_review.json | W873 | 新增：B10 diff 归渠审查产物 |
| scripts/output/_w864_accent_exemptions.json | W873 | 登记簿增 W873 分册（语义色片 15 处） |
| scripts/output/_w873_spec.json | W873 | 本批 spec 十字段 |
| docs/00-导读/W批次编号对账表.md | W873 | 认领行与收官回填 |


## W872 设计迁移 B9 视觉与叙事实验 10 页（2026-10-22）

| 文件 | W | 说明 |
|---|---|---|
| site/data/aesthetics.html | W872 | B9 迁移：容器令牌化 + KPI 顶条 4→1 + seal 淡底（热力条 ×4 进豁免） |
| site/data/visual-art.html | W872 | B9 迁移：容器令牌化 + seal 淡底（sc-cat ×5 进豁免） |
| site/data/cross-time-danmaku.html | W872 | B9 迁移：容器令牌化 + seal 淡底（级联页脚面·只动 CSS） |
| site/data/emotional-heatmap.html | W872 | B9 迁移：容器令牌化 + seal 淡底（scholar-card 进豁免） |
| site/data/chart-design.html | W872 | B9 迁移：容器令牌化 + KPI 顶条 5→1 + seal 淡底（domino ×7 进豁免） |
| site/data/perf-canvas-rendering.html | W872 | B9 迁移：容器令牌化 + seal 淡底（主行动 btn 进豁免） |
| site/data/global-pattern.html | W872 | B9 迁移：容器令牌化 + KPI 顶条 4→1 + seal 淡底（p-country 进豁免） |
| site/data/four-dimensional-research-network.html | W872 | B9 迁移：容器令牌化 + seal 淡底（badge 进豁免） |
| site/data/four-heavenly-kings-artifacts.html | W872 | B9 迁移：容器令牌化 + KPI 顶条 5→1 + seal 淡底（king-card 进豁免） |
| site/data/tag-cloud.html | W872 | B9 迁移：容器令牌化 + seal 淡底（rc-size ×5 / tab-btn 进豁免·级联页脚面） |
| scripts/output/_w872_accent_audit.json | W872 | 新增：B9 朱砂落点审计 |
| scripts/output/_w872_diff_review.json | W872 | 新增：B9 diff 归渠审查产物 |
| scripts/output/_w864_accent_exemptions.json | W872 | 登记簿增 W872 分册（语义色片 29 处） |
| scripts/output/_w872_spec.json | W872 | 本批 spec 十字段 |
| docs/00-导读/W批次编号对账表.md | W872 | 认领行与收官回填 |


## W871 设计迁移 B8 跨学科与实验 10 页（2026-10-22）

| 文件 | W | 说明 |
|---|---|---|
| site/data/cognitive-psychology.html | W871 | B8 迁移：容器令牌化 + seal 淡底 + 间距（char-card 进豁免） |
| site/data/social-media.html | W871 | B8 迁移：容器令牌化 + KPI 顶条 4→1 + seal 淡底（platform-badge 进豁免） |
| site/data/business-model.html | W871 | B8 迁移：容器令牌化 + seal 淡底（monster-card 进豁免） |
| site/data/game-webnovel.html | W871 | B8 迁移：容器令牌化 + KPI 顶条 5→1 + seal 淡底（cc-stat-fill ×10 进豁免） |
| site/data/mbti-evolution.html | W871 | B8 迁移：容器令牌化 + KPI 顶条 4→1 + seal 淡底（stage-btn 进豁免） |
| site/data/risk-project.html | W871 | B8 迁移：容器令牌化 + seal 淡底（char-card c-tang 进豁免） |
| site/data/concept-device.html | W871 | B8 迁移：容器令牌化 + seal 淡底（cipher-back ×5 / idev ×5 进豁免） |
| site/data/workplace.html | W871 | B8 迁移：容器令牌化 + KPI 顶条 4→1 + seal 淡底（alert-badge ×7 进豁免） |
| site/data/ethics-consumption.html | W871 | B8 迁移：容器令牌化 + KPI 顶条 5→1 + seal 淡底（ipo-outcome ×5 / veg-badge ×4 进豁免） |
| site/data/criticism-history.html | W871 | B8 迁移：容器令牌化 + seal 淡底（candidate-card main 进豁免） |
| scripts/output/_w871_accent_audit.json | W871 | 新增：B8 朱砂落点审计 |
| scripts/output/_w871_diff_review.json | W871 | 新增：B8 diff 归渠审查产物 |
| scripts/output/_w864_accent_exemptions.json | W871 | 登记簿增 W871 分册（语义色片 42 处） |
| scripts/output/_w871_spec.json | W871 | 本批 spec 十字段 |
| docs/00-导读/W批次编号对账表.md | W871 | 认领行与收官回填 |


## W870 设计迁移 B7 文本与思想 10 页（2026-10-22）

| 文件 | W | 说明 |
|---|---|---|
| site/data/text-evolution.html | W870 | B7 迁移：容器令牌化 + seal 淡底 + 间距（evo-step.first ×6 进豁免） |
| site/data/text-search.html | W870 | B7 迁移：容器令牌化 + seal 淡底 |
| site/data/linguistics.html | W870 | B7 迁移：容器令牌化 + KPI 顶条 3→1 + seal 淡底（色片/教派卡进豁免） |
| site/data/famous-time-travel.html | W870 | B7 迁移：容器令牌化 + seal 淡底 |
| site/data/cultural-misreading.html | W870 | B7 迁移：容器令牌化 + KPI 顶条 4→1 + seal 淡底 |
| site/data/century-dialogue.html | W870 | B7 迁移：容器令牌化 + seal 淡底（speech-bubble 整改后 3 处在限额内） |
| site/data/counterfactual.html | W870 | B7 迁移：容器令牌化 + seal 淡底（validity 等级 ×7 进豁免） |
| site/data/philosophy.html | W870 | B7 迁移：容器令牌化 + seal 淡底 |
| site/data/jurisprudence.html | W870 | B7 迁移：容器令牌化 + seal 淡底（severity ×8 + artifact 分类 ×2 进豁免） |
| site/data/karma-reincarnation.html | W870 | B7 迁移：容器令牌化 + seal 淡底（轮回道分类卡进豁免） |
| scripts/output/_w870_accent_audit.json | W870 | 新增：B7 朱砂落点审计 |
| scripts/output/_w870_diff_review.json | W870 | 新增：B7 diff 归渠审查产物 |
| scripts/output/_w864_accent_exemptions.json | W870 | 登记簿增 W870 分册（语义色片 33 处） |
| scripts/output/_w870_spec.json | W870 | 本批 spec 十字段 |
| docs/00-导读/W批次编号对账表.md | W870 | 认领行与收官回填 |


## W869 设计迁移 B6 叙事学 10 页（2026-10-22）

| 文件 | W | 说明 |
|---|---|---|
| site/data/narrative-experiment.html | W869 | B6 迁移：容器令牌化 + narr-card 顶条 12→1 收敛 + 间距令牌化（chips/owner 进豁免） |
| site/data/narrative-rhythm-curve.html | W869 | B6 迁移：容器令牌化 + KPI 顶条 5→1 + seal 淡底（主行动 btn 进豁免） |
| site/data/narratology-12d-network.html | W869 | B6 迁移：容器令牌化 + KPI 顶条 6→1 + seal 淡底 |
| site/data/narratology-16d-network.html | W869 | B6 迁移：容器令牌化 + KPI 顶条 6→1 + seal 淡底 |
| site/data/intertextuality-network.html | W869 | B6 迁移：容器令牌化 + KPI 顶条 6→1 + seal 淡底 |
| site/data/deconstruction.html | W869 | B6 迁移：容器令牌化 + KPI 顶条 4→1 + seal 淡底（tag ×5 进豁免） |
| site/data/six-senses-narratology-network.html | W869 | B6 迁移：容器令牌化 + KPI 顶条 6→1 + seal 淡底 |
| site/data/poetry-rhythm-analysis.html | W869 | B6 迁移：容器令牌化 + KPI 顶条 5→1 + seal 淡底（progress-fill 进豁免） |
| site/data/music-structure.html | W869 | B6 迁移：容器令牌化 + seal 淡底（tag ×35 进豁免） |
| site/data/language-style-radar.html | W869 | B6 迁移：容器令牌化 + KPI 顶条 5→1 + seal 淡底 |
| scripts/output/_w869_accent_audit.json | W869 | 新增：B6 朱砂落点审计 |
| scripts/output/_w869_diff_review.json | W869 | 新增：B6 diff 归渠审查产物 |
| scripts/output/_w864_accent_exemptions.json | W869 | 登记簿增 W869 分册（语义色片 50 处） |
| scripts/output/_w869_spec.json | W869 | 本批 spec 十字段 |
| docs/00-导读/W批次编号对账表.md | W869 | 认领行与收官回填 |


## W868 设计迁移 B5 取经与行迹 10 页（2026-10-22）

| 文件 | W | 说明 |
|---|---|---|
| site/data/guanyin-six-roles-network.html | W868 | B5 迁移：容器令牌化 + KPI 顶条 6→1 + seal 淡底 + 间距令牌化 |
| site/data/pilgrim-team-dynamic-network.html | W868 | B5 迁移：同上（顶条 5→1·ctrl-btn/phase-card 进豁免） |
| site/data/pilgrim-team-psychology-arc.html | W868 | B5 迁移：同上（顶条 5→1·progress-fill 进豁免） |
| site/data/journey-route.html | W868 | B5 迁移：同上（顶条 4→1·标签重判连带 8） |
| site/data/journey-geo-3d.html | W868 | B5 迁移：容器令牌化 + seal 淡底 |
| site/data/journey-geo-semiotics.html | W868 | B5 迁移：冻结解除·正式消费 v4 令牌 |
| site/data/journey-map-interactive.html | W868 | B5 迁移：容器令牌化 + 顶条 5→1 + seal 淡底（主行动 btn 进豁免） |
| site/data/journey-spacetime.html | W868 | B5 迁移：容器令牌化 + 顶条 4→1 + seal 淡底（progress-fill 进豁免） |
| site/data/customs-pass-route.html | W868 | B5 迁移：容器令牌化 + 顶条 4→1 + seal 淡底 |
| site/data/cave-estate.html | W868 | B5 迁移：容器令牌化 + 顶条 4→1 + seal 淡底 + 间距（tag.king ×19 进豁免·标签重判连带 16） |
| scripts/output/_w868_accent_audit.json | W868 | 新增：B5 朱砂落点审计 |
| scripts/output/_w868_diff_review.json | W868 | 新增：B5 diff 归渠审查产物 |
| scripts/output/_w864_accent_exemptions.json | W868 | 登记簿增 W868 分册（语义变体 26 处） |
| scripts/output/_w868_spec.json | W868 | 本批 spec 十字段 |
| docs/00-导读/W批次编号对账表.md | W868 | 认领行与收官回填 |


## W867 设计迁移 B4 妖怪与神力 10 页（2026-10-22）

| 文件 | W | 说明 |
|---|---|---|
| site/data/monster-background.html | W867 | B4 迁移：容器 + 页脚两处 1280→1120 归并 + seal 淡底 + 间距令牌化 |
| site/data/monster-capability-radar.html | W867 | B4 迁移：容器令牌化 + KPI 顶条 4→1 + seal 淡底 + 间距令牌化 |
| site/data/monster-ecology-network.html | W867 | B4 迁移：容器令牌化 + seal 淡底 + 间距令牌化（tab-btn active 进豁免） |
| site/data/monster-female-network.html | W867 | B4 迁移：容器令牌化 + KPI 顶条 6→1 + seal 淡底 + 间距令牌化 |
| site/data/monster-hierarchy-network.html | W867 | B4 迁移：容器令牌化 + KPI 顶条按行收敛 + seal 淡底 + 间距令牌化 |
| site/data/monster-sociology.html | W867 | B4 迁移：容器令牌化 + seal 淡底 + 间距令牌化（signal-card 三态进豁免） |
| site/data/monster-victims-network.html | W867 | B4 迁移：容器令牌化 + KPI 顶条 6→1 + seal 淡底 + 间距令牌化（victim-card/swatch-bar 进豁免） |
| site/data/ecology.html | W867 | B4 迁移：容器令牌化 + seal 淡底 + 间距令牌化（damage-pill ×9 / compare-card 进豁免） |
| site/data/heaven-power-network.html | W867 | B4 迁移：容器令牌化 + KPI 顶条按行收敛 + seal 淡底 + 间距令牌化（role-card.r-king 进豁免） |
| site/data/underworld-power-network.html | W867 | B4 迁移：容器令牌化 + KPI 顶条按行收敛 + seal 淡底 + 间距令牌化（role-card.r-king 进豁免） |
| scripts/output/_w867_accent_audit.json | W867 | 新增：B4 朱砂落点审计（文字 54 处·实底逐页定性） |
| scripts/output/_w867_diff_review.json | W867 | 新增：B4 diff 归渠审查产物 |
| scripts/output/_w864_accent_exemptions.json | W867 | 登记簿增 W867 分册（语义变体条 18 处·七类） |
| scripts/output/_w867_spec.json | W867 | 本批 spec 十字段 |
| docs/00-导读/W批次编号对账表.md | W867 | 认领行与收官回填 |


## W866 设计迁移 B3 人物主线 9 页（2026-10-22）

| 文件 | W | 说明 |
|---|---|---|
| site/data/character-appearance.html | W866 | B3 迁移：容器令牌化 + KPI 顶条 4→1 + seal 淡底 + 间距 12 处 |
| site/data/character-presence-timeline.html | W866 | B3 迁移：容器令牌化 + seal 淡底 + 间距 9 处（顶条已合规） |
| site/data/character-semantic-network.html | W866 | B3 迁移：容器 1280→1120 归并 + 顶条 6→1 + seal 淡底 + 间距 21 处 |
| site/data/character-dynamic-network.html | W866 | B3 迁移：容器令牌化 + 顶条 4→1 + seal 淡底 + 间距 18 处 |
| site/data/character-sentiment-arc.html | W866 | B3 迁移：容器令牌化 + seal 淡底 + 间距 15 处 |
| site/data/character-relationship-3d.html | W866 | B3 迁移：容器令牌化 + 顶条 5→1 + seal 淡底 + 间距 14 处 |
| site/data/character-relationship-3d-view.html | W866 | B3 迁移：容器令牌化 + seal 淡底 + 间距 18 处 |
| site/data/dialogue-sentiment.html | W866 | B3 迁移：容器令牌化 + seal 淡底 + 间距 21 处 |
| site/data/ai-dialogue.html | W866 | B3 迁移：容器令牌化 + seal 淡底 + step-num 徽章 ×4 淡底 + 间距 21 处 |
| scripts/output/_w866_accent_audit.json | W866 | 新增：B3 朱砂落点审计（文字 58 处·实底逐页定性） |
| scripts/output/_w866_diff_review.json | W866 | 新增：B3 diff 归渠审查产物 |
| scripts/output/_w864_accent_exemptions.json | W866 | 升级多批登记簿 + W866 增补（选中态 4·负向指示 1·主行动 1） |
| scripts/output/_w866_spec.json | W866 | 本批 spec 十字段 |
| docs/00-导读/W批次编号对账表.md | W866 | 认领行与收官回填 |


## W865 首页三任务区重组 + 目录页检索动线批（2026-10-22）

| 文件 | W | 说明 |
|---|---|---|
| site/index.html | W865 | 改：首页三任务区重组（顶层块 9→6·三区各 1 个 h2·搜索降为工具条·装饰 SVG 与开篇诗移出首屏·stats 收进看数据区·移动端 mega 降为紧凑计量） |
| site/reader/index.html | W865 | 改：总目录页加检索工具条（即时过滤 + 回号直达 + 6 组跳转锚点 + 命中计数·由生成器产出） |
| site/reader/**（101 页） | W865 | 改：INLINED CSS 块回注同步（此前陈旧·缺 W856 的 .brand-mark 样式）·内容零变化 |
| site/js/reader-enhance.js | W865 | 改：加总目录页检索逻辑（DOM 守卫·其余 621 页行为零变化·零外域·file:// 可用） |
| scripts/build_reader.py | W865 | 改：_render_root_index 出检索工具条 + 分组锚点（生成器是真源·产物与生成器同源） |
| scripts/_w865_layout_probe.mjs | W865 | 新增：双页面布局与交互探针（无头 Chrome CDP·首页层级/首屏入口 + 目录页过滤与回号直达实测） |
| scripts/output/_w865_layout_metrics.json | W865 | 新增：5 组实测度量（首页 1440/768/375 + 目录页 1440/375） |


## W864 设计迁移 B2 结构页 10 页（2026-10-22）

| 文件 | W | 说明 |
|---|---|---|
| site/data/chapter-structure-graph.html | W864 | B2 迁移：容器令牌化 + KPI 顶条收敛 + seal 淡底 + 间距令牌化 9 处 |
| site/data/chapter-stats.html | W864 | B2 迁移：同上（间距 8 处） |
| site/data/story-timeline.html | W864 | B2 迁移：同上（间距 7 处） |
| site/data/timeline.html | W864 | B2 迁移：容器令牌化 + seal 淡底 + 间距 23 处（顶条已合规） |
| site/data/relationships.html | W864 | B2 迁移：容器令牌化 + 顶条收敛（alt 变体不动）+ seal 淡底 + 间距 45 处 |
| site/data/81-hardships.html | W864 | B2 迁移：容器令牌化 + seal 淡底 + 间距 16 处（90 tag 进豁免清单） |
| site/data/81-hardships-view.html | W864 | B2 迁移：容器令牌化 + 顶条收敛 + seal 淡底 + 间距 18 处 |
| site/data/hardship-heatmap.html | W864 | B2 迁移：容器令牌化 + 顶条收敛 + seal 淡底 + 间距 23 处 |
| site/data/hardship-difficulty-heatmap.html | W864 | B2 迁移：容器令牌化 + 顶条收敛 + seal 淡底 + 间距 20 处 |
| site/data/methodology-matrix.html | W864 | B2 迁移：容器令牌化 + 顶条收敛 + seal 淡底 + 间距 47 处 |
| scripts/_w864_migrate.py | W864 | 新增：B2 施工件（A 容器 + B 顶条规则 + B seal·块扫描·dry-run） |
| scripts/_w864_accent_audit.py | W864 | 新增：朱砂落点审计（文字 + 实底双尺子·计算样式） |
| scripts/output/_w864_accent_audit.json | W864 | 新增：审计产物（10 页文字与实底落点） |
| scripts/output/_w864_accent_exemptions.json | W864 | 新增：裁决 2 豁免清单首批（数据语义色片 + 选中态实底） |
| scripts/output/_w864_spec.json | W864 | 本批 spec 十字段 |
| docs/00-导读/W批次编号对账表.md | W864 | 认领行与收官回填 |

## W863 递延版段补写批（2026-10-22）

| 文件 | W | 说明 |
|---|---|---|
| CHANGELOG.md | W863 | 补写 W852-W862 十一段（149→160 段·号序降序完好）+ 本批 W863 段 |
| scripts/output/file-index.md | W863 | 补写 W852-W862 十一段反向索引（149→160 段） |
| scripts/output/_w854_spec.json | W863 | 新增：补位 spec（按 W854 feat 提交与台账行整理） |
| scripts/output/_w856_spec.json | W863 | 新增：补位 spec（Logo 定稿落地·按提交记录整理） |
| scripts/output/_w858_spec.json | W863 | 新增：补位 spec（交互流程审查·按提交记录整理） |
| scripts/output/_w859_spec.json | W863 | 新增：补位 spec（设计资产归档·按提交记录整理） |
| scripts/output/_w861_spec.json | W863 | 新增：补位 spec（设计资产归档收尾·按提交记录整理） |
| scripts/output/_w863_spec.json | W863 | 本批 spec 十字段 |
| docs/00-导读/W批次编号对账表.md | W863 | 认领行与收官回填·递延豁免区状态更新 |

## W862 设计迁移 B1 根页与入口 8 页（2026-10-22）

| 文件 | W | 说明 |
|---|---|---|
| site/index.html | W862 | B1 迁移：kicker 落 --bg 改 --accent-text（ask-hero 内恢复 --accent）· 间距令牌化 25 处 |
| site/guide.html | W862 | B1 迁移：kicker 改 --accent-text · 间距令牌化 12 处 |
| site/curated.html | W862 | B1 迁移：kicker 改 --accent-text · 间距令牌化 9 处 |
| site/dashboard.html | W862 | B1 迁移：容器 1536→--container-wide · KPI 大字归墨色 · masthead/section-kick 改 --accent-text · 间距令牌化 49 处 |
| site/dukou-engine.html | W862 | B1 迁移：容器 1320→--container-wide · 徽章实底→--accent-tint 淡底 · header h1 改 --accent-text · 间距令牌化 14 处 |
| site/rum-viewer.html | W862 | B1 迁移：容器 1024→--container-content · .btn 字色改 --accent-text 并令牌化朱砂字面量 · 间距令牌化 10 处 |
| site/visit-viewer.html | W862 | B1 迁移：间距令牌化 7 处 |
| scripts/_w862_tokenize_spacing.py | W862 | 新增：值保留式间距令牌化（dry-run·跳过 INLINED 块·负值防护） |
| scripts/_w862_accent_text_audit.py | W862 | 新增：朱砂文字落点机器分类（计算样式有效背景链） |
| scripts/_w862_diff_review.py | W862 | 新增：迁移 diff 全量归渠聚合（不截断） |
| scripts/output/_w862_accent_text_audit.json | W862 | 新增：朱砂文字落点审计产物（20 处落 bg） |
| scripts/output/_w862_diff_review.json | W862 | 新增：B1 迁移 diff 归渠审查产物 |
| scripts/output/_w862_spec.json | W862 | 本批 spec 十字段 |
| docs/00-导读/W批次编号对账表.md | W862 | 认领行与收官回填 |


## W861 设计资产归档收尾批（2026-10-22）

| 文件 | W | 说明 |
|---|---|---|
| assets/design/alternatives/ | W861 | 新增：四个未选定方向的图形标矢量源 4 件 |
| assets/design/screenshots/ | W861 | 新增：过程截图 13 张（拼版/特写/实拍/预览页） |
| assets/design/process/RECEIPT-W855.md | W861 | 新增：跨会话回执底稿 |
| assets/design/README.md | W861 | 索引更新（三块新增登记） |
| docs/00-导读/W批次编号对账表.md | W861 | 认领行与补段批回填 |


## W860 计划方案合规门禁挂槽批（2026-10-22）

| 文件 | W | 说明 |
|---|---|---|
| scripts/check_plan_template.py | W860 | 新增：第 48 门禁「计划方案合规」的增量判定入口（--gate 门禁模式 / --self-test 7 例负样本） |
| scripts/_w857_plan_template_review.py | W860 | 改：抽出 judge()/fail_set() 纯函数供门禁复用；新增「执行摘要」等效形式识别 |
| scripts/verify_delivery.py | W860 | 改：挂载第 48 槽（_StrictGate）+ EXPECTED_SECTION_NAMES 与 SCOPE_DOCS_SECTIONS 同步（门禁段 52→53） |
| tests/unit/test_check_plan_template.py | W860 | 新增：第 48 槽单测 4 例（纯逻辑面·git 端到端用例不入 pytest） |
| AGENTS.md · docs/agent/gates.md · README.md · pytest.ini · HANDOVER.md | W860 | 改：门数口径四处同步（47→48 槽 + gate_count 标记 + pytest_collected 标记 + 交接块） |
| scripts/output/stats.json | W860 | 改：gate_count 47→48 · pytest_collected 818→823（stats.py --w W860 实测刷新） |


## W859 设计资产归档批（2026-10-22）

| 文件 | W | 说明 |
|---|---|---|
| assets/design/logo/ | W859 | 新增：Logo 定稿源文件 10 件（图形标/组合标/图标三档/favicon 四档） |
| assets/design/ai-concepts/ | W859 | 新增：AI 概念稿 18 张 + 逐张母题判定表 |
| assets/design/tools/ | W859 | 新增：可复算工具链 |
| assets/design/README.md | W859 | 新增：素材区索引与口径说明 |
| docs/00-导读/W批次编号对账表.md | W859 | 认领行与补段批回填 |


## W858 站点交互流程审查报告批（2026-10-21）

| 文件 | W | 说明 |
|---|---|---|
| docs/11-方案报告/计划方案/T07-任务计划执行与经验沉淀报告-2026-10-21.md | W858 | 新增：交互流程审查报告（3 条 P0 + 8 条 P1-P3 + 施工计划与经验） |
| docs/00-导读/文档规范.md | W858 | §4.9 新增「框架类交付物必须落进仓内目录并登记索引」 |
| CLAUDE.md | W858 | 第 11 条指针（权威正文在文档规范） |
| docs/11-方案报告/README.md | W858 | §二「计划方案」8→9 篇 |
| docs/INDEX.md | W858 | 重建（report_docs 42→43） |
| site/data/search.html、site/en/search.html | W858 | 搜索索引重建 + CSP 哈希重算 |
| scripts/output/stats.json、stats-index.md、stats-changelog.json | W858 | 报告计数与会话统计刷新 |
| docs/00-导读/W批次编号对账表.md | W858 | 认领行与补段批回填 |


## W857 计划方案模板符合性复核批（2026-10-21）

| 文件 | W | 说明 |
|---|---|---|
| scripts/_w857_plan_template_review.py | W857 | 新增：计划方案对模板的结构符合性复核探针（32 项结构判据 + 配对并集 §12 十项覆盖 + 编号体系 + 模糊词；纯标准库·一次性诊断件·不入 CI） |
| scripts/output/_w857_plan_template_review.json | W857 | 新增：8 份文档 × 32 判据的机器可读矩阵 + 3 组配对并集判定（复核证据原始数据） |
| scripts/output/_w857_spec.json | W857 | 新增：本批 CHANGELOG 版段素材（10 键齐·供 backfill_changelog.py 按号序补段） |


## W856 Logo 定稿落地批（2026-10-21）

| 文件 | W | 说明 |
|---|---|---|
| site/static/icons/ | W856 | icon-192/512/maskable-512 重做 + logo-mark-light.svg + logo-lockup-light.svg |
| site/index.html | W856 | 六处元信息 + 页眉 seal→图形标 + hero h1 + 页脚品牌位（《取经录》） |
| site/system.css | W856 | 新增 .brand-mark 纯加法规则（.seal 保留·其余 857 页零影响） |
| site/manifest.webmanifest | W856 | name / short_name → 取经录 |
| site/rss.xml | W856 | 随生成脚本重出（RSS 标题同步） |
| site/static/img/og-cover.png | W856 | 随生成脚本重出 |
| xiyouji-desktop/ | W856 | 桌面端应用名同步 |
| README.md、CITATION.cff | W856 | 品牌名与项目名同步 |
| docs/00-导读/W批次编号对账表.md | W856 | 认领行与补段批回填 |


## W855 架构评审报告批（2026-10-21）

| 文件 | W | 说明 |
|---|---|---|
| docs/11-方案报告/架构评审报告-2026-10-21.md | W855 | 新增：现役架构五维体检报告（P0 五条 / P1 十一条 / P2 择要 + 五维评级 + 三梯队 16 项 + 与 W820/W818 边界对齐 + 8 项未验证项 + 12 条复算命令附录） |
| docs/11-方案报告/README.md | W855 | 目录索引登记（现役报告 32 → 33 篇·新增第 33 行·W854 并行批第 32 行原样保留） |
| docs/INDEX.md | W855 | 产物级重建（新增报告入索引·docs_index.py 重跑·第 17 门禁逐字节比对依据） |
| scripts/output/_w855_spec.json | W855 | 本批 spec 十字段（CHANGELOG 版段递延·待补段批按号序回写 W852 至 W855 四段及双索引） |
| docs/00-导读/W批次编号对账表.md | W855 | 认领行（touches 声明 4 项 + 版段递延登记·已收官） |


## W854 界面布局审计批（2026-10-21）

| 文件 | W | 说明 |
|---|---|---|
| docs/11-方案报告/界面布局审计报告-2026-10-21.md | W854 | 新增：界面布局审计报告（四痛点全查·18 条问题逐条取证与理由） |
| scripts/_w854_cdp.mjs | W854 | 新增：布局审计 CDP 量测探针 |
| scripts/_w854_layout_probe.mjs | W854 | 新增：站点布局度量探针 |
| scripts/_w854_layout_probe_app.mjs | W854 | 新增：桌面端布局度量探针 |
| scripts/output/_w854_layout_metrics.json | W854 | 新增：站点布局度量产物 |
| scripts/output/_w854_layout_metrics_app.json | W854 | 新增：桌面端布局度量产物 |
| docs/11-方案报告/README.md | W854 | §二 报告登记（随 W855 提交带入） |
| docs/00-导读/W批次编号对账表.md | W854 | 认领行（随 W855 提交带入）与补段批回填 |


## W853 卡片封面素材图成套批（2026-10-21）

| 文件 | W | 说明 |
|---|---|---|
| site/static/images/card-01-huoshan.webp | W853 | 新增：卡片封面 01/12·火焰山（赭金山脊+朱砂山光+一缕烟·净空带 299px） |
| site/static/images/card-02-tongtianhe.webp | W853 | 新增：卡片封面 02/12·通天河（冰河中央水道+渡舟与旅人剪影·净空带 324px） |
| site/static/images/card-03-shituoling.webp | W853 | 新增：卡片封面 03/12·狮驼岭（崖上三魔剪影·无面目·净空带 299px） |
| site/static/images/card-04-dushuangxuejiang.webp | W853 | 新增：卡片封面 04/12·寒江独钓（蓑笠翁与孤舟·大留白·净空带 617px） |
| site/static/images/card-05-mingyuesongjian.webp | W853 | 新增：卡片封面 05/12·明月松间（赭金月轮+松针枯笔·净空带 424px） |
| site/static/images/card-06-yunshenzhibu.webp | W853 | 新增：卡片封面 06/12·云深不知处（层叠山脊+云隙小寺与石阶·净空带 311px） |
| site/static/images/card-07-baiyao.webp | W853 | 新增：卡片封面 07/12·百妖列阵（九种妖形剪影并排·无面目·净空带 443px） |
| site/static/images/card-08-zhuowuquan.webp | W853 | 新增：卡片封面 08/12·濯垢泉（洞中蛛网+垂丝+泉池·净空带 364px） |
| site/static/images/card-09-sanyao.webp | W853 | 新增：卡片封面 09/12·三妖剪径（虎鹿羊三形+朱砂残旗·净空带 334px） |
| site/static/images/card-10-gusichenzhong.webp | W853 | 新增：卡片封面 10/12·古刹晨钟（古刹藏于老松+晨雾+孤僧·净空带 400px） |
| site/static/images/card-11-songyunshitan.webp | W853 | 新增：卡片封面 11/12·松云石坛（崖上古松+云气+石坛·净空带 300px） |
| site/static/images/card-12-shuyuanxingtantan.webp | W853 | 新增：卡片封面 12/12·书院杏坛（低案两列+梅枝+学子剪影·净空带 299px） |
| scripts/output/_w853_spec.json | W853 | 本批 spec 十字段（CHANGELOG 版段递延·待号序链恢复后补写） |
| docs/00-导读/W批次编号对账表.md | W853 | 认领行与收官回填 |


## W852 站点 Hero 素材图成套批（2026-10-21）

| 文件 | W | 说明 |
|---|---|---|
| site/static/images/hero-01-xihai-yunhai.webp | W852 | 新增：Hero 素材 01/06·西行山河云海（山脊云海+七人单行+朱砂小旗·净空带 599px） |
| site/static/images/hero-02-shitu-wuxing.webp | W852 | 新增：Hero 素材 02/06·师徒五人组像（白马+猴+猪+二僧·净空带 320px·二版） |
| site/static/images/hero-03-fabao-qiji.webp | W852 | 新增：Hero 素材 03/06·法宝器物静物（金箍棒+七宝妙树+袈裟+九环锡杖·净空带 568px·三版） |
| site/static/images/hero-04-tiangting-yunmo.webp | W852 | 新增：Hero 素材 04/06·天庭云阙（宫阙+云台+右侧幽冥门与水影·净空带 423px·三版） |
| site/static/images/hero-05-huangmo-gulu.webp | W852 | 新增：Hero 素材 05/06·荒漠孤旅（风蚀峡谷+孤旅与白马+朱砂布条·净空带 513px·三版） |
| site/static/images/hero-06-fotu-chengque.webp | W852 | 新增：Hero 素材 06/06·佛国城阙（石柱牌坊+层叠殿顶+五人来朝·净空带 491px） |
| scripts/output/_w852_spec.json | W852 | 本批 spec 十字段（CHANGELOG 版段递延·待顶段推进后补写） |
| docs/00-导读/W批次编号对账表.md | W852 | 认领行与收官回填 |


## W851 设计迁移阶段 1 令牌落地批（2026-10-21）

| 文件 | W | 说明 |
|---|---|---|
| site/tokens.css | W851 | v4 令牌增量落地：34 个零消费新名 / 35 处定义（间距 13 + 语义 gap 6 + 容器三档 3 + 栅格 2 + 排版角色 9 + accent-text 浅暗各 1）·20,799 → 23,039 B |
| scripts/_w851_j1_name_audit.py | W851 | 新增：J1 命名冲突审计（三面交集 + var() 零消费 + defer 复证 + defer 持有·双向可失败） |
| scripts/_w851_visual_regression_probe.py | W851 | 新增：J2 视觉回归探针（15s 地板 + DOM 静默收敛 + 29 属性固定序对拍·自测 4/4） |
| tests/unit/test_w851_visual_regression_probe.py | W851 | 新增：12 例（计数不齐不掩属性·属性定位·采样面 ≥20·PROPS 固定序·地板常量） |
| tests/unit/test_w851_j1_name_audit.py | W851 | 新增：9 例（-- 前缀回归·defer 双向可失败·暗色块并集·对真实 tokens.css 的 defer 持有） |
| scripts/output/_w851_j1_name_audit.json | W851 | 新增：J1 审计产物（预检 + 落地复验） |
| scripts/output/_w851_tokens_prelanding.css | W851 | 新增：落地前 tokens.css 副本（预检对拍基准·git show HEAD 取证） |
| scripts/output/_w851_visual_snapshot_before.json | W851 | 新增：J2 before 快照（23 页 × 双主题·置换前态） |
| scripts/output/_w851_visual_snapshot_after.json | W851 | 新增：J2 after 快照（终态·与 before 对拍零差异） |
| scripts/output/_w851_visual_snapshot_freeze_before.json | W851 | 新增：预支页冻结前快照（探针缺陷发现证据） |
| scripts/output/_w851_visual_snapshot_freeze_after.json | W851 | 新增：预支页冻结后快照 |
| scripts/output/design-tokens.json | W851 | 再生成：132 键（light 103 / dark 29·+35 处 v4 增量） |
| docs/00-导读/design.md | W851 | 再生成：设计令牌消费文档（与 tokens.css 逐字节一致） |
| DESIGN.md | W851 | §4A.8 tokens 预算 +2KB → +3KB（基线 20,799 → 上限 23,799·废止 v3 前口径）·新增 §4C v4 设计迁移章 |
| site/data/journey-geo-semiotics.html | W851 | 预支引用冻结：var(--space-N, 回退值) → 当前字面值（11 处·渲染零变化） |
| site/en/journey-geo-semiotics.html | W851 | 预支引用冻结：同上（11 处） |
| pytest.ini | W851 | collected 标记 797 比 818（新增 21 例） |
| docs/00-导读/W批次编号对账表.md | W851 | 认领行订正（34 名/35 处口径·三坑实录）与收官回填 |
| scripts/output/_w851_spec.json | W851 | 本批 spec 十字段 |
| scripts/output/_w851_j2_evidence.json | W851 | 新增：J2 判词摘要（零差异 + 双快照 sha256 + 逐页元素计数） |

## W850 Q2 取数基建批（2026-10-21）

| 文件 | W | 说明 |
|---|---|---|
| scripts/obs_sample.py | W850 | 新增：Q2 采样件（OBS-10 静态扫描 / OBS-11 每页 3 次取中位实测 LCP / OBS-14 首 token·显式开关·按指标计十批） |
| tests/unit/test_obs_sample.py | W850 | 新增：9 例（含启发式拒收、中位数剔除尖峰、代理陷阱、按指标进度、去重覆盖） |
| scripts/output/obs_samples.json | W850 | 新增：OBS 样本库（首笔含 OBS-10 全站扫描与 OBS-11 五页每页三次中位实测） |
| pytest.ini | W850 | collected 标记 787 比 797（新增 9 例加新脚本 import 冒烟） |
| AGENTS.md | W850 | §4.2 导读与正文槽数 46 与 45 顺修至 47·分组头 27-45 顺修至 27-47 |
| docs/11-方案报告/系统架构方案-分层模块与部署-2026-10-20.md | W850 | §12.2 Q2 行与 §11.2 采样件说明·「46 槽」14 处与 A-04 期望值顺修至 47 |
| docs/11-方案报告/静态站前端框架化选型对比-2026-10-20.md | W850 | 「46 槽」8 处存量漂移顺修至 47 |
| scripts/output/stats.json | W850 | pytest_collected 797 刷新（gate_count 仍 47） |
| scripts/output/_w850_spec.json | W850 | 本批 spec 十字段 |
| docs/00-导读/W批次编号对账表.md | W850 | 认领行与收官回填 |

## W849 性能门禁挂槽批（2026-10-21）

| 文件 | W | 说明 |
|---|---|---|
| scripts/check_perf_shadow.py | W849 | 新增：性能影子槽判据件（六项静态成本代理·C1 缺页即红·--record/--ingest/--self-test） |
| scripts/verify_delivery.py | W849 | 挂第 47 槽「性能影子」（严格委托段 + EXPECTED + site scope）；段数注释 51→52 订正 |
| scripts/output/perf_shadow.json | W849 | 新增：影子基线（按批样本·同批重跑覆盖） |
| AGENTS.md | W849 | §4.2 门禁清单补第 47 条 |
| docs/agent/gates.md | W849 | 第 47 条全量定义 + 标题计数 45→47 订正 + 速查表分组 27-47 |
| pytest.ini | W849 | collected 标记 786→787（新脚本入 import 冒烟参数化）·段数 51→52 |
| README.md | W849 | gate_count 内联标记 46→47 |
| docs/11-方案报告/系统架构方案-分层模块与部署-2026-10-20.md | W849 | gate_count 内联标记 46→47 |
| scripts/output/stats.json | W849 | gate_count 47 / pytest_collected 787 刷新 |
| scripts/output/_w849_spec.json | W849 | 本批 spec 十字段 |
| docs/00-导读/W批次编号对账表.md | W849 | 认领行与收官回填 |

## W848 Q5 裁决落档批（2026-10-21）

| 文件 | W | 说明 |
|---|---|---|
| scripts/rag/README.md | W848 | Q5 裁决段（为什么升/何时开/何时别开/CPU 纪律）+ 档位表表头口径标注与基线表指针 |
| scripts/rag/build_vectors.py | W848 | 注释里的模型体积口径统一为「约 92 MiB／≈96 MB」双单位（无行为改动） |
| docs/11-方案报告/系统架构方案-分层模块与部署-2026-10-20.md | W848 | §12.2 Q5 翻已裁决、§7.1 S8 采纳列同步、状态口径改为开放项只剩 Q2 |
| scripts/output/_w848_spec.json | W848 | 本批 spec 十字段 |
| docs/00-导读/W批次编号对账表.md | W848 | 认领行与收官回填 |

## W847 阅读页体验封装批（2026-10-21）

| 文件 | W | 说明 |
|---|---|---|
| scripts/build_reader.py | W847 | 折叠段/工具条/反馈块的生成逻辑 + 对应样式（FOLD_SECTIONS / fold_sections / toolbar_html / feedback_html） |
| site/js/reader-enhance.js | W847 | 新增：进度记忆/书签/字号/进度条/展开全部（localStorage 三键·file:// 可用·降级不抛错） |
| docs/11-方案报告/计划方案/执行前计划-T04-站内阅读入口打通与阅读页体验封装.md | W847 | AC-22~25 改判 + 附录 D 实测分布与根因 |
| scripts/output/_w847_spec.json | W847 | 本批 spec 十字段 |
| docs/00-导读/W批次编号对账表.md | W847 | 认领行与收官回填 |
| site/reader/ch008.html | W847 | 代表页：折叠/工具条/进度条/反馈块（全部 622 页同批重建） |

## W846 阅读页正文回灌批（2026-10-21）

| 文件 | W | 说明 |
|---|---|---|
| site/reader/ch008.html | W846 | 重建回灌：正文头防→头陀等字级修正（代表页·本批共 51 页） |
| site/reader/ch009.html | W846 | 重建回灌：正文字级修正（代表页） |
| site/reader/ch010.html | W846 | 重建回灌：正文字级修正（代表页） |
| scripts/output/_w846_spec.json | W846 | 本批 spec 十字段 |
| docs/00-导读/W批次编号对账表.md | W846 | 认领行与收官回填 |

## W845 阅读页重建影响面量化批（2026-10-21）

| 文件 | W | 说明 |
|---|---|---|
| docs/11-方案报告/计划方案/执行前计划-T04-站内阅读入口打通与阅读页体验封装.md | W845 | AC-21 改判已达标（262 行 ≤ 2000）·AC-25 生成侧已证·V-15 转实测·新增附录 C 口径与复现命令 |
| docs/00-导读/W批次编号对账表.md | W845 | 认领行与收官回填 |
| scripts/output/_w845_spec.json | W845 | 本批 spec 十字段 |

## W844 系统架构批四项落地（2026-10-21）

| 文件 | W | 说明 |
|---|---|---|
| xiyouji-agent-web/server/backup.ts | W844 | 新增：会话库与审计日志快照（VACUUM INTO 一致性快照 + 保留策略 + 启动钩子） |
| xiyouji-agent-web/server/backup.test.ts | W844 | 新增：备份 9 例回归（行数一致/幂等/份数/超龄/跳过仍清理/缺失不抛/dry-run） |
| xiyouji-agent-web/server/metrics.ts | W844 | 新增：首 token 滚动窗口（100 样本·p50/p95·脏数据丢弃） |
| xiyouji-agent-web/server/metrics.test.ts | W844 | 新增：指标窗 7 例回归（空窗给 null/分位/淘汰/脏数据/快照语义） |
| xiyouji-agent-web/server/chat.ts | W844 | 改：OBS-14 首 token 计时（handler 起算 + 首个 delta 记录 + 无文本记 no_text_delta） |
| xiyouji-agent-web/server/routes.ts | W844 | 改：新增只读 GET /api/metrics（首 token 窗口摘要） |
| xiyouji-agent-web/server/index.ts | W844 | 改：listen 回调挂 backupOnStartup（失败不阻断启动） |
| xiyouji-agent-web/server/db.ts | W844 | 改：导出 databasePath() 供备份复用同一解析结果 |
| xiyouji-agent-web/package.json | W844 | 改：test:server 加入 backup.test.ts 与 metrics.test.ts |
| docs/agent/agent-web.md | W844 | 改：补会话库备份与保留期、OBS-14 首 token 两节 |
| docs/11-方案报告/系统架构方案-分层模块与部署-2026-10-20.md | W844 | 改：S8 口径纠正（dense 增益实测）+ 档 2 触发条件细化 + Q1/Q3/Q4 裁决回填 + 新增 Q5 |
| scripts/rag/eval/queries_30q_frozen.jsonl | W844 | 新增：30 题冻结集原样迁入（与工地原件字节一致） |
| scripts/rag/eval/queries_100q.jsonl | W844 | 新增：100 题评测集（30 冻结 + 70 标题派生·gold 由脚本解析） |
| scripts/rag/eval/make_queries.py | W844 | 新增：题集生成器（锚点表 + gold 解析 + --check 一致性） |
| scripts/rag/eval/eval_retrieval.py | W844 | 新增：检索复算入口（三档 + recall@1/5/10 + 报告生成） |
| scripts/rag/README.md | W844 | 改：补检索评测节（题集构成/复算入口/基线/与历史数字关系/局限） |
| scripts/output/rag_eval_report.md | W844 | 新增：检索评测报告（生成物·可重跑覆盖） |
| scripts/output/_w844_spec.json | W844 | 新增：本批 spec（级联唯一来源） |

## W843 pitfalls 增补批（2026-10-21）

| 文件 | W | 说明 |
|---|---|---|
| docs/agent/pitfalls.md | W843 | 改：级联节增第 48 条（desc 禁含内嵌 W 号·页脚链 token 撞车）+ 数据节增第 49 条（双源同旧值假绿）；节标题 4→5、4→5 |
| AGENTS.md | W843 | 改：§4.3 坑位总数 47→49、六主题目录级联节 4→5 与数据节 4→5、补 W843 计数口径注 |
| scripts/output/_w843_spec.json | W843 | 新增：本批 spec（级联唯一来源） |
| scripts/output/index.md | W843 | 改：登记 _w843_spec.json 与 _cascade_files_W843.txt |

## W842 CHANGELOG 递延补段工具批（2026-10-21）

| 文件 | W | 说明 |
|---|---|---|
| scripts/backfill_changelog.py | W842 | 新增：CHANGELOG 递延补段工具（两阶段：按降序补段 + 当前态六面推到新顶段·段数与降序断言 fail-closed） |
| scripts/output/_w842_spec.json | W842 | 新增：本批 spec（级联唯一来源） |
| pytest.ini | W842 | 改：头注 collected 实体标记 785 改 786（顺手修真漂移·W839 少记一例） |
| scripts/output/index.md | W842 | 改：登记 backfill_changelog.py 与 _w842_spec.json + 文件计数刷新 |

## W841 版本行分隔符兜底门禁批（2026-10-21）

| 文件 | W | 说明 |
|---|---|---|
| scripts/check_doc_sync.py | W841 | 改：新增 C6 版本行 desc 分隔符体检（三面 · ； — 禁入 + 形态不识别 fail-closed）+ 自测 22 增至 24 例 |
| scripts/output/_w841_spec.json | W841 | 新增：本批 spec 入库（版段递延用） |
| scripts/output/index.md | W841 | 改：登记 _w841_spec.json + 文件计数 246 改 247 |


## W840 pitfalls 坑位沉淀批（2026-10-21）

| 文件 | W | 说明 |
|---|---|---|
| docs/agent/pitfalls.md | W840 | 改：流程节新增第 47 条（fail-closed 跳过路径 _SkipResult 守卫）· 节标题 7 条改 8 条 |
| AGENTS.md | W840 | 改：§4.3 坑位计数校准 41 改 47（git 节 12 改 17 · 流程节 7 改 8） |
| scripts/output/_w840_spec.json | W840 | 新增：本批 spec 入库（版段递延用） |
| scripts/output/index.md | W840 | 改：登记 _w840_spec.json + 文件计数 244 改 245 |
| docs/00-导读/W批次编号对账表.md | W840 | 改：W840 认领行登记与收官回填 |


## W839 fail-closed 跳过路径回归修复批（2026-10-21）

| 文件 | W | 说明 |
|---|---|---|
| scripts/verify_delivery.py | W839 | 改：_gate_a11y 加 isinstance(_SkipResult) 守卫（scope 跳过伪造结果不得判红·W834 回归修复） |
| tests/unit/test_verify_failclosed.py | W839 | 改：新增 2 例回归锁（跳过结果零上报 / 简单段跳过不判红） |
| pytest.ini | W839 | 改：头注 collected 实体标记 783→785 |
| scripts/output/stats.json | W839 | 改：pytest_collected 783→785 |
| scripts/output/_w839_spec.json | W839 | 新增：本批 spec 入库（版段递延用） |
| scripts/output/index.md | W839 | 改：登记 _w839_spec.json + 文件计数 243→244 |
| docs/00-导读/W批次编号对账表.md | W839 | 改：W839 认领行登记（回归修复批） |


## W838 取经编制表勘误批（2026-10-21）

| 文件 | W | 说明 |
|---|---|---|
| docs/11-方案报告/取经编制表-工具与技能挂位-2026-10-20.md | W838 | 改：V1.1a 勘误五处（§6.2 自查脚本正则块引限定·旁文档指针面 9→13 处三处统一·附录 A 时点行更新·行 13 引用 §6.4→§6.5·第 31 门禁 C4/C5b 拆分·版本行与状态行同步） |
| scripts/output/_w838_spec.json | W838 | 新增：本批 spec 入库（版段递延用） |
| scripts/output/index.md | W838 | 改：登记 _w838_spec.json + 文件计数 242→243 |
| docs/00-导读/W批次编号对账表.md | W838 | 改：W838 认领行登记（取经编制表勘误批·只读审查转修订） |


## W837 并发实况沉淀批（2026-10-20）

| 文件 | W | 说明 |
|---|---|---|
| docs/agent/pitfalls.md | W837 | 改：「git / 提交 / 并发」段新增 5 条（W833/W836 批实证：临时索引假红 / index.lock 全程持锁 / C5b-C5d 互锁 / 管道 BOM / 守卫自指）· 段计数 12→17 |
| docs/00-导读/W批次编号对账表.md | W837 | 改：W837 认领行登记（含版段递延说明·顶段序约束） |


## W836 品牌字面量零命中守卫批（2026-10-20）

| 文件 | W | 说明 |
|---|---|---|
| scripts/check_no_brand_refs.py | W836 | 新建：品牌字面量零命中守卫（字面量 base64 存储·扫已跟踪文件含 archive/·退出码 0/1/2 分流·--self-test 32 例） |
| .github/workflows/security.yml | W836 | 改：新增 brand-refs 作业（品牌字面量扫描 + 自检复核·守卫失效即阻断） |
| scripts/gen_folder_docs.py | W836 | 改：点开头顶层目录改为整体排除（去掉逐名列举的明文字面量·对未来同类目录免疫） |
| docs/11-方案报告/计划方案/执行前计划-T05-取经编制表落库与编制位补全.md | W836 | 改：路径引用改为不落被禁品牌明文 |
| archive/scripts/batches/misc/_audit_agentweb_baseline.py | W836 | 改：移除已成空转且含被禁字面量的品牌扫描段（其余按 §11.2 不回溯修复·检测能力已由活面承接） |
| docs/00-导读/W批次编号对账表.md | W836 | 改：W836 认领行登记（含版段递延说明·顶段序约束） |


## W835 服务端暴露面收口批（2026-10-20）

| 文件 | W | 说明 |
|---|---|---|
| xiyouji-agent-web/server/security.ts | W835 | 改：新增 normalizeHostname 与 isAllowedHost 纯函数（Host 归一化与白名单判定·fail-closed） |
| xiyouji-agent-web/server/config.ts | W835 | 改：新增 ALLOWED_HOSTS（默认回环三形态 + 追加项）与 REQUIRE_TOKEN 两个启动期配置 |
| xiyouji-agent-web/server/middleware.ts | W835 | 改：新增 hostGuard 关卡（挂在 request ID 之后、限流之前） |
| xiyouji-agent-web/server/index.ts | W835 | 改：启动期暴露面自检（强制 token 无 token 拒绝启动 + 未设 token 记 WARN） |
| xiyouji-agent-web/server/security.test.ts | W835 | 改：新增纯函数 3 例与真起服负样本 2 例（rebinding 主机名 403 / 强制 token 拒绝启动） |
| xiyouji-agent-web/.env.example | W835 | 改：新增 AGENT_WEB_REQUIRE_TOKEN 与 AGENT_WEB_ALLOWED_HOSTS 的说明 |
| docs/agent/agent-web.md | W835 | 改：新增暴露面收口条目（Host 白名单与 token 硬开关·含挂载序与回归面） |
| docs/00-导读/W批次编号对账表.md | W835 | 改：W835 认领行登记（含版段递延说明·顶段序约束） |
| scripts/output/index.md | W835 | 派生面：目录文档文件清单（收录 _w835_spec.json） |
| scripts/output/README.md | W835 | 派生面：目录说明的文件计数（新增 _w835_spec.json 后重算） |


## W834 门禁 fail-open 根修批（2026-10-20）

| 文件 | W | 说明 |
|---|---|---|
| scripts/verify_delivery.py | W834 | 改：B1/B2 fail-open 根修（_run_simple_gate 异常路径 WARN→FAIL·_gate_a11y 三处 fail-open→FAIL·missing_warn 登记式降级保留·模块 docstring 补 fail-closed 语义段） |
| tests/unit/test_verify_failclosed.py | W834 | 新增：fail-closed 语义负样本测试 12 例（B1 崩溃/未登记缺失/登记缺失保留/快乐径/退出码径 + B2 解析失败/缺 summary/缺 E2-2/崩溃/快乐径/P0P1 阻断/非零退出） |
| pytest.ini | W834 | 改：头注 collected 实体标记 770→782（本批 12 例入库·C5b 扩展面对账） |
| scripts/output/stats.json | W834 | 改：pytest_collected 770→782·report_docs 37→39（并行 W831 落库） |
| STRUCTURE.md | W834 | 改：report_docs 标记 38→39（并行 W831 取经编制表批落库·含 T05 计划件与抓位文档） |
| docs/11-方案报告/系统架构方案-分层模块与部署-2026-10-20.md | W834 | 改：report_docs 实体标记 38→39（C5b 扩展面对账） |
| docs/11-方案报告/计划方案三性审查报告-2026-10-20.md | W834 | 改：§五.5 pytest 标记 770→782 + W834 复测注（含三度顺延取号记录） |
| docs/11-方案报告/计划方案/执行前计划-T04-站内阅读入口打通与阅读页体验封装.md | W834 | 改：AC-07/ASM-08 订正注更新至现役 39（W831 取经编制表批落库后） |
| docs/00-导读/W批次编号对账表.md | W834 | 改：W834 认领行（7 格）+ W830 行递延注记更新（顶段链因并行落库移位） |


## W833 交付链与工具链静默失效根修批（2026-10-20）

| 文件 | W | 说明 |
|---|---|---|
| .github/workflows/workflow-lint.yml | W833 | 新建：工作流 YAML 可解析性守卫（独立于 ci.yml·W806 同型事故根修） |
| .github/workflows/ci.yml | W833 | 改：mypy 去掉 --non-interactive（该选项使命令在参数解析阶段即报错·配合忽略失败写法导致类型检查从未执行） |
| .github/workflows/security.yml | W833 | 改：两处去掉 npm ci 失败即回退 npm install 的写法——锁与 manifest 失配即红 |
| .github/workflows/README.md | W833 | 改：登记 Workflow Lint 工作流（触发条件与 W806 事故机理说明） |
| .github/workflows/index.md | W833 | 派生面：目录文档文件清单 9→10（含 workflow-lint.yml） |
| docs/00-导读/W批次编号对账表.md | W833 | 改：W833 认领行登记（含版段递延说明·顶段序约束） |
| scripts/output/README.md | W833 | 派生面：目录说明的文件计数（新增 _w833_spec.json 后重算） |
| scripts/output/index.md | W833 | 派生面：目录文档文件清单（收录 _w833_spec.json） |


## W832 agent-web 生产面加固批（2026-10-20）

| 文件 | W | 说明 |
|---|---|---|
| xiyouji-agent-web/server/chat.ts | W832 | 改：保存消息失败的 detail 与聊天异常 SSE error 帧改固定文案（形状不变·原文进 logger） |
| xiyouji-agent-web/server/routes.ts | W832 | 改：/api/ready 探针的 detail 改固定文案 + 原文进 logger |
| xiyouji-agent-web/server/db.ts | W832 | 改：库路径支持 AGENT_WEB_DB_PATH 覆盖（默认不变·供端到端测试用临时库） |
| xiyouji-agent-web/e2e/chat.e2e.mjs | W832 | 改：改跑临时库 + 真实库零改动断言 + 指向真实库时拒绝启动且跳过清理（守卫三处同源） |
| xiyouji-agent-web/src/hooks/useChat.streaming.test.ts | W832 | 改：改用 Vite 的 import.meta.glob 以原始文本读源文件（前端 tsconfig 无 node types） |
| docs/00-导读/W批次编号对账表.md | W832 | 改：W832 认领行登记（含版段递延说明·顶段序约束） |


## W831 取经编制表落库与编制位补全批（2026-10-20）

| 文件 | W | 说明 |
|---|---|---|
| docs/11-方案报告/取经编制表-工具与技能挂位-2026-10-20.md | W831 | 新增：项目级编制说明（§0 一分钟速览 + §1 编制总表 17 位 × 6 列 + §2 编制卡 17 位五问 + §3 三处空缺编制位诊断与补全步骤 + §4 挂位表 28 项 + §5 术语权威指针 27 条 + §6 复现命令；15 条引文逐字命中；V1.1 增补丁组「归档与工地」2 位：酆都判官崔珏=archive/ 档案官、扫地道人=tmpe/ 场地官） |
| docs/11-方案报告/取经编制表-工具与技能挂位-2026-10-20.html | W831 | 新增：零外域依赖编制表预览页（file:// 直开·Playwright 实测 17 卡 / 17 引用块 / 53 挂载标签 / extEls=0 / 无控制台错误） |
| docs/11-方案报告/计划方案/执行前计划-T05-取经编制表落库与编制位补全.md | W831 | 新增：框架第五次执行的执行前计划（14 条 AC · 23 条 ASM · 12 步 ST · 8 指标 · 10 风险 · 10 决策 · 16 项自检 + §0.5 零前置知识速览） |
| docs/11-方案报告/README.md | W831 | 改：§一 现役报告 30→31 篇（追加编制表索引行）· §二 计划方案 6→7 篇（追加 T-05 索引行）；三项结构自校验实测通过（表头计数 == 实际行数 · 编号升序连续 · 表内无断裂空行） |
| docs/00-导读/W批次编号对账表.md | W831 | 改：追加 W831 认领行（7 格严式·touches 落末格 = docs/11-方案报告/README.md·状态 进行中） |
| docs/superpowers/plans/2026-10-14-interference-governance-roadmap.md | W831 | 改：§8 干扰日志追加一行（G1-A 漂移 + G1-F 号段邻接占用·W832 并行避让·0 实质损失） |
| scripts/output/_w831_spec.json | W831 | 新增：W831 落段 spec（10 键·供顶段推进后 batch_cascade 补写用） |
| scripts/output/_cascade_files_W831.txt | W831 | 新增：W831 落地件清单（C4-e 强校验要求） |


## W830 计划方案三性审查与快照漂移门禁修复批（2026-10-20）

| 文件 | W | 说明 |
|---|---|---|
| docs/11-方案报告/计划方案三性审查报告-2026-10-20.md | W830 | 新增：9 份计划方案三性审查报告（逐份结论表 + 约 60 断言复验证据 + 四类真问题分级 + 本批修复清单 + 后续建议 + 复算附录） |
| scripts/check_doc_sync.py | W830 | 改：C5b 实体标记对账扩展面（11-方案报告根层 + pytest.ini·只跑标记不跑句式与裸数字·计划方案子目录除外）+ 标记判据助手提取 + 自测 20→22 例（T21/T22 双向锁） |
| scripts/stats.py | W830 | 改：新增 pytest_collected 键（pytest --collect-only 实算·fail-closed 判据未执行即红）+ C5d timeout 60→180s |
| pytest.ini | W830 | 改：头注 collected 计数实体化（602 字面量→770 实体标记）+ verify_delivery 49 段→51 段 |
| docs/11-方案报告/系统架构方案-分层模块与部署-2026-10-20.md | W830 | 改：report_docs 实体标记 30→37（C5b 扩展面纳入后订正·原值无门禁兜底） |
| docs/11-方案报告/静态站前端框架化选型对比-2026-10-20.md | W830 | 改：site/data 合计 9,272,531→9,722,504（均值 110,483×88 对账值·原误植与 9.27 MB 注解矛盾） |
| docs/11-方案报告/计划方案/执行前计划-T03-全项目审查第一批修复.md | W830 | 改：头五要素状态字段执行中→已收官（W816 落地 55b9b8c0·终稿报告已在库） |
| docs/11-方案报告/计划方案/执行前计划-T04-站内阅读入口打通与阅读页体验封装.md | W830 | 改：AC-07/ASM-08 加开工重测注记（现役 report_docs 37 非 34/35·聚合数字当批现测） |
| docs/11-方案报告/README.md | W830 | 改：§一 现役报告索引登记三性审查报告（29→30 篇） |
| STRUCTURE.md | W830 | 改：report_docs 36→37 + 现役报告 29→30 篇 + 去过期「在途 2 篇」括注 |
| docs/agent/gates.md | W830 | 改：第 31 条追加 W830 C5b 扩展面定义（扫描域、子目录除外理由、建置即红实证、pytest_collected 键） |
| docs/00-导读/W批次编号对账表.md | W830 | 改：W830 认领行（7 格）+ W830 bullet（取号说明 + W829 占用实证 + B1/B2 待办登记） |


## W827 站内阅读入口打通施工批（2026-10-21）

| 文件 | W | 说明 |
|---|---|---|
| site/index.html | W827 | 改：补 5 处阅读入口（主导航 阅读 项 / 首屏开始阅读 CTA / 4 条场景化直达 / 全卷索引逐回精读行 编号 01 + 原 11 条顺延 02-11） |
| site/guide.html | W827 | 改：主导航 + 首条阅读路径卡各补 1 条 reader/index.html 入口 |
| docs/11-方案报告/计划方案/T04-任务计划执行与经验沉淀报告-2026-10-21.md | W827 | 新增：T-04 施工批终稿报告（20 条 AC 实测 / 4 条偏差 / 5 条决策 / 3 条经验） |
| docs/11-方案报告/README.md | W827 | 改：§二 计划方案 7 篇改 8 篇 + 登记 T-04 终稿报告行 |
| STRUCTURE.md | W827 | 改：report_docs 标记 39 改 40（计划方案 7 篇改 8 篇） |
| docs/11-方案报告/系统架构方案-分层模块与部署-2026-10-20.md | W827 | 改：report_docs 标记 39 改 40（C5b 双向锁） |
| scripts/output/_w827_spec.json | W827 | 新增：本批 spec（级联用） |
| scripts/output/index.md | W827 | 改：登记 _w827_spec.json + 文件计数 245 改 246 |

## W826 界面视觉重设计细化规格批（2026-10-20）

| 文件 | W | 说明 |
|---|---|---|
| docs/11-方案报告/界面视觉重设计细化规格-v4-2026-10-20.md | W826 | 新建：五项裁决落地细则 + 对比度实算三条修法 + 24 组件规格卡 + v4 令牌终稿 + 11 批迁移清单 + 阶段 1 六判据 |
| docs/11-方案报告/界面视觉重设计方向-v4-2026-10-20.md | W826 | 改：v1.1 订正——§4.3 对比度表改实算值（ink-3 3.09:1 已达标→撤销加深）· §10 待裁决项改裁决记录 |
| scripts/_w826_contrast_audit.py | W826 | 新建：WCAG 2.1 对比度实算（17 组比值 + 5 项未达标 + 三条修法取值推导） |
| scripts/_w826_container_survey.py | W826 | 新建：容器宽度现状测绘（1320 实际主导·1200 仅存规范条文→待迁移面 18 页） |
| scripts/_w826_migration_plan_check.py | W826 | 新建：迁移批次清单对拍（site/data 87 + 根 8 页 0 漏 0 重 · 每批 ≤10 · reader 622 单批） |
| scripts/output/_w826_contrast_audit.json | W826 | 产物：对比度实算数据（浅/暗两组比值 + 修法取值） |
| scripts/output/_w826_container_survey.json | W826 | 产物：容器宽度分布数据（按目录） |
| scripts/output/_w826_migration_plan_check.json | W826 | 产物：批次清单对拍结果（判定 PASS） |
| docs/11-方案报告/README.md | W826 | 新增：现役报告索引第 29 行（细化规格）· 篇数 28→29 |
| docs/00-导读/W批次编号对账表.md | W826 | 认领行（W826·7 格）+ 收官回填（hash 9114d968 + 状态已收官 + CHANGELOG 版段已立）+ W827 现势 bullet |
| CHANGELOG.md | W826 | 新增 W826 版段（顶段）· 编号规则行 W001-W825→W001-W826 |
| README.md | W826 | 版本指针同步：当前批次 W825→W826 |
| STRUCTURE.md | W826 | 版本指针同步：当前批次 W825→W826 |
| HANDOVER.md | W826 | 版本指针同步：头链 + 「一、当前进度」新增 W826 条目 + 当前 HEAD 句 |
| docs/00-导读/项目说明.md | W826 | 版本指针同步：头部 + 「当前版本」行 |
| .github/workflows/README.md | W826 | 版本指针同步：头部版本行 + 里程碑行上限 W825→W826 |
| CITATION.cff | W826 | 外部引用面：version W825→W826 |
| site/data/search.html | W826 | 派生面：搜索索引机械刷新（无语义变更） |
| site/en/search.html | W826 | 派生面：搜索索引机械刷新（无语义变更） |
| scripts/index.md | W826 | 派生面：目录清单（列本批三个脚本） |
| scripts/output/index.md | W826 | 派生面：目录清单（列本批三份产物） |

## W825 审查发现第二批修复批（2026-10-20）

| 文件 | W | 说明 |
|---|---|---|
| xiyouji-agent-web/src/utils/sseStream.ts | W825 | 改：新增 createSseLineSplitter（跨块行缓冲·末尾半行留待下一片+流末冲刷）并由 readChatStream 采用（帧跨片不再整帧丢失） |
| xiyouji-agent-web/src/utils/sseStream.test.ts | W825 | 新建 7 例：半行不提前吐出 + 流末冲刷幂等 + 200KB 大帧两片还原 + 逐字符切片还原 + 多字节跨片无替换符 + 整帧一次到达回归锚 + 心跳与非法帧跳过回归锚 |
| xiyouji-agent-web/src/hooks/useChat.ts | W825 | 改：内联 SSE 解析改用共享行缓冲器（与 sseStream 共用单一实现）+ catch 分支双 id 匹配 + finally 兜底复位流式态 + 错误文案追加为文本块 + AbortController 接线与停止/卸载 abort |
| xiyouji-agent-web/src/hooks/useChat.streaming.test.ts | W825 | 新建 4 例源码级回归锚：catch 双 id 匹配 / finally 复位流式态 / fetch 带 signal 且停止调 abort / 错误文案追加为文本块 |
| scripts/preflight_check.py | W825 | 改：状态列与 touches 列按内容定位（状态右起紧匹配「已收官/已闭环」形态格 + touches 取末格 + 占位符归一空集）·消除 8 格错位行与占位行造成的幻影在途批次 |
| tests/unit/test_preflight_check.py | W825 | 新增 4 例：摘要含裸竖线的 8 格行状态与 touches 仍定位正确 / 占位符 touches 归一空集 / 主题含「已收官」不误认状态 / 标准 7 格行解析结果不变 |

## W824 站内阅读入口打通批（2026-10-20）

| 文件 | W | 说明 |
|---|---|---|
| docs/11-方案报告/计划方案/执行前计划-T04-站内阅读入口打通与阅读页体验封装.md | W824 | 新增：T-04 执行前计划（外部评审稿逐条对盘 + 622 页 reader 内容站内入链为 0 的实证 + 入口打通 20 条验收判据 + 阅读页体验封装 W827 候选 + 12 项自检全过） |
| docs/11-方案报告/README.md | W824 | 改：§二 登记 T-04 执行前计划（计划方案 5→6 篇） |
| docs/00-导读/W批次编号对账表.md | W824 | 改：W824 认领行登记（两度让号后归位·严格 7 格）+ 现势 bullet 链 W824/W825/W826/W827 |
| STRUCTURE.md | W824 | 改：report_docs 计数 34→36（现役报告 29〔含在途 2〕+ 索引 README 1 + 计划方案 6） |
| scripts/output/stats.json | W824 | 改：report_docs 34→36（last_changed_by=W824） |
| scripts/output/stats-changelog.json | W824 | 改：变更史登记本批（W824·report_docs 34→36） |
| scripts/output/stats-index.md | W824 | 改：stats 反向索引重生成 |
| scripts/output/_w824_spec.json | W824 | 新增：本批 spec 入库 |
| scripts/output/_cascade_files_W824.txt | W824 | 新增：本批级联面清单 |
| docs/superpowers/plans/2026-10-14-interference-governance-roadmap.md | W824 | 改：§8 干扰日志补登 1 行（开工漂移 + 交集拒绝 + 两度号段争用·即时登记） |
| docs/INDEX.md | W824 | 改：目录索引重生成（727 篇·含本执行前计划） |

## W823 数据库表设计审查报告落档批（2026-10-20）

| 文件 | W | 说明 |
|---|---|---|
| docs/11-方案报告/数据库表设计审查报告-2026-10-20.md | W823 | 新增：agent-web SQLite 存储层表设计审查报告（四维审查 + 13 项发现按影响程度分级 + 9 项库副本实跑复现 + 四包落地顺序 + 六条验收判据 + 复算附录） |
| scripts/_w823_db_schema_probe.py | W823 | 新增：表设计审查取证脚本（四子命令 `schema`/`faults`/`bench`/`hygiene`·仅标准库·写入类取证全在库副本上进行·判据未执行即非零退出·计时附实返行数校验） |
| scripts/output/_w823_spec.json | W823 | 新增：本批 spec 入库 |
| docs/11-方案报告/README.md | W823 | 改：§一 索引登记本报告 + 篇数计数 +1 |
| docs/00-导读/W批次编号对账表.md | W823 | 改：W823 认领行登记（数据库表设计审查报告落档批·只读审查 + 修复未动工） |

## W822 §8 干扰日志机器触发点批（2026-10-20）

| 文件 | W | 说明 |
|---|---|---|
| scripts/preflight_check.py | W822 | 改：touches 交集拒绝真触发时输出「§8 干扰日志待登记」提示行（只加提示·不改判定与退出码）+ 提示常量与纯函数 + 原拟触发①按用户裁决删除并留注 |
| scripts/safe_commit.py | W822 | 改：ref-lock 竞争重试真触发时输出同款提示行（只加提示·不改判定与退出码）+ 提示常量与纯函数 |
| tests/unit/test_preflight_check.py | W822 | 改：新增 3 例（提示含载体路径与窗口 / 调用点须处于条件分支内按缩进块向上找 if / safe_commit 同款守卫）·12→19 例 |
| docs/agent/pitfalls.md | W822 | 改：shell 场景查坑表新增「靠自觉的机制」行（禁只写条款不加机器触发点 + 提醒只在真触发时出） |
| docs/10-方法论沉淀/多Agent干扰治理与touches纪律.md | W822 | 改：新增「§四之二·§8 干扰日志的机器触发点」节（治靠自觉必然掉档 + 两触发点表 + 触发①删除的代价登记 + 判定口径加严指针） |
| docs/00-导读/W批次编号对账表.md | W822 | 改：追加 W822 认领行（append 安全操作·touches 按规范不列对账表） |
| scripts/output/_w824_spec.json | W822 | 改：本批 spec（级联唯一来源） |

## W821 系统架构方案批（2026-10-20）

| 文件 | W | 说明 |
|---|---|---|
| docs/11-方案报告/系统架构方案-分层模块与部署-2026-10-20.md | W821 | 新增：系统架构方案报告（八维成文：整体分层 L0-L4 加治理横切面 / 17 模块拆分与依赖矩阵 / 三条数据流加一条治理链路 / 8 候选存储裁定与升级触发条件 / 三档触发式扩展与 8 条容量阈值 / 8 故障域降级矩阵含 RTO 与 RPO / 四通道部署拓扑 / 四层观测面与 14 条指标阈值与 6 条 SLO / 5 张 Mermaid 架构图 / 10 条验收标准 / 11 条复算命令） |
| docs/11-方案报告/README.md | W821 | 改：现役报告索引追加本报告行（系统架构方案八维成文） |
| docs/00-导读/W批次编号对账表.md | W821 | 改：W821 认领行登记（系统架构方案批·3 项 touches）+ 收官回填 hash 与状态 + 现势 bullet 轮换 |
| scripts/output/_w821_spec.json | W821 | 新增：batch_cascade 原生级联 spec（十面改写字段） |

## W820 干扰治理日志补登与机制自身缺陷修复批（2026-10-20）

| 文件 | W | 说明 |
|---|---|---|
| docs/superpowers/plans/2026-10-14-interference-governance-roadmap.md | W820 | 改：§8 干扰日志补登 4 行（10-17~10-20 断档·带可核验证据·含延迟登记标注）+ §2 判定口径加严（表不完整不是有效结论·须先验登记完整性·不得据残表坐实 P1 缓建） |
| docs/00-导读/W批次编号对账表.md | W820 | 改：追加 W820 认领行（append 安全操作·touches 按规范不列对账表） |
| scripts/output/_w820_spec.json | W820 | 改：本批 spec（级联唯一来源） |

## W819 界面视觉重设计方向批（2026-10-20）

| 文件 | W | 说明 |
|---|---|---|
| docs/11-方案报告/界面视觉重设计方向-v4-2026-10-20.md | W819 | 新增：界面视觉层级 / 配色与字体体系 / 间距栅格 / 组件样式统一的设计方向（保留原有功能结构不动·§10 含五个待裁决项·未改 site/ 任何现役页面） |
| docs/11-方案报告/v4-design-language-preview.html | W819 | 新增：零外域视觉预览页（设计方向的可视化验证件·不改现役页面） |
| scripts/_w819_design_audit.py | W819 | 新增：设计方向一次性只读取证脚本（现状取证用·按 AGENTS §2 不入 CI 门禁） |
| scripts/output/_w819_design_audit.json | W819 | 新增：设计方向取证产物（脚本输出） |
| docs/11-方案报告/README.md | W819 | 改：§一 现役报告索引新增 W819 报告行 |
| docs/00-导读/W批次编号对账表.md | W819 | 改：W819 认领行登记 + 收官回填（062ad3e8） |

## W818 静态站前端框架化选型评估批（2026-10-20）

| 文件 | W | 说明 |
|---|---|---|
| docs/11-方案报告/静态站前端框架化选型对比-2026-10-20.md | W818 | 新增：静态站与可视化页前端框架化技术选型对比（问题域/硬约束界定 + 现状盘点 + 五候选定义 + 五维对齐 + file:// 与构建链实测 + 加权排序 4.50/4.30/2.70/2.65/2.45 + 推荐路线三档 + 明确不做清单 + 风险遗留 + 复算附录） |
| docs/11-方案报告/README.md | W818 | 改：§一 现役报告计数 21 → 26（订正历史漂移 3 篇 + 本批 + 并行会话 W819 两行）+ 新增第 25/26 行登记本批与 W819 报告 |
| docs/00-导读/W批次编号对账表.md | W818 | 改：W818 认领行登记（五维对齐选型评估批·8 项 touches）+ 收官回填 hash 与状态 + 台账 W817/W819 行结构归一（多列致解析错位） |
| STRUCTURE.md | W818 | 改：11-方案报告目录计数标记 report_docs 30 → 34（含并行会话在途 2 篇）+ 「现役报告」拆解同步 |
| scripts/_w818_inventory.py | W818 | 新增：现状盘点取证脚本（仅标准库·零网络零依赖）·输出页面体量分布/内联结构/数据回退形态/本地化依赖体积；`--ecosystem` 追加 npm + GitHub 一手数据 |
| scripts/_w818_file_protocol_probe.py | W818 | 新增：file:// 协议三判据 + 构建产物对照探针（Playwright·判据未执行即非零退出·不静默跳过） |
| scripts/index.md | W818 | 改：gen_folder_docs.py --refresh 重生成（新增两个 _ 前缀取证脚本入清单） |
| scripts/output/_w818_spec.json | W818 | 新增：batch_cascade 原生级联 spec（十面改写字段） |

## W817 agent-web 工具层边界加固批（2026-10-20）

| 文件 | W | 说明 |
|---|---|---|
| xiyouji-agent-web/server/engine/tools.ts | W817 | 改：受保护路径黑名单去仓库根锚定（会话库 cwd 无关形态 + 门禁脚本基名形态）+ 路径守卫取 realpath 判越界并返回解析后路径 + `git --output` 空格形态整 token 拦截 + 遍历类工具（glob/grep）过黑名单 |
| xiyouji-agent-web/server/engine/tools.test.ts | W817 | 新增 9 例：会话库 cwd 无关（含 wal/shm）/ 仓外目录链接不可读 / 仓外文件链接不可写 / git --output 空格形态 / 等号形态回归锚 / 只读 git 放行锚 / 门禁脚本 cwd 无关 / 遍历面不触及受保护路径 / 遍历面未误伤普通文件 |
| docs/00-导读/W批次编号对账表.md | W817 | 改：W817 认领行登记（工具层边界加固·5 处同源绕过 + 负样本自证） |

## W816 门禁判据可信化批（2026-10-20）

| 文件 | W | 说明 |
|---|---|---|
| scripts/check_citations.py | W816 | 改：相对 `--dir` 按脚本 ROOT 解析（cwd 无关）+ 零文件守卫（判据未执行 exit 1 / 输入错误 exit 2）+ 自测 +3 例（15/15） |
| scripts/security_scan.py | W816 | 改：tsc 产物排除补 `.tsbuild`（outDir 迁移致本地红 CI 绿分裂）+ 新增 XSS-007（d3 `.html(` 动态实参）/ XSS-008（`.innerHTML +=`）·判据排除静态字面量与回调首参 |
| tests/unit/test_security_scan.py | W816 | 新增 6 例：XSS-007 命中 / XSS-008 命中 / XSS-001 回归锚 / site 降级口径 / 非 site 保持 high / tsbuild 产物排除 |
| docs/11-方案报告/计划方案/执行前计划-T03-全项目审查第一批修复.md | W816 | 新建：T-03《执行前计划》— 全项目审查第一批修复（门禁判据可信化·12 项自检全过） |
| docs/11-方案报告/README.md | W816 | 改：§二 计划方案索引登记 T-03《执行前计划》条目（3 篇 → 4 篇） |
| docs/00-导读/W批次编号对账表.md | W816 | 改：W813/W814/W815 认领行 commit 与状态列回填为已收官 + 现势 bullet 标 W813 已消费并追加 W816 + W816 认领行登记 |

## W815 shell 查坑表补两条（2026-10-20）

| 文件 | W | 说明 |
|---|---|---|
| docs/agent/pitfalls.md | W815 | 改：shell 场景查坑表补两行（内联 Python 含美元符变量名的展开坑 + 含引号时的配对坑·附实测结论与处置分层） |

## W814 去品牌扩展批（2026-10-20）

| 文件 | W | 说明 |
|---|---|---|
| docs/00-导读/W批次编号对账表.md | W814 | 改：认领会话列 23 处会话标识去品牌化（改为并行 Agent 会话·多 Agent 区分保留）+ W812 行「保留原名」决定随新裁决反转的注记 |
| CHANGELOG.md | W814 | 改：现役与历史段该品牌字面去品牌化（认领会话/生成模型署名/品牌复合表述/退役凭证变量名四类分治） |
| HANDOVER.md | W814 | 改：现役批摘要该品牌字面去品牌化 + 与新裁决矛盾的「保留原名」表述就地订正 |
| CLAUDE.md | W814 | 改：元信息块生成模型署名去品牌化（改为本地 Agent 会话） |
| .gitignore | W814 | 改：删该本地索引配置的忽略规则（2 行）+ 并入其 24 条独有忽略规则（功能不丢·备份在项目外 TEMP） |
| xiyouji-agent-web/server/engine/tools.ts | W814 | 改：目录跳过项该品牌目录名改中性名（遍历防护功能保留） |
| scripts/output/file-index.md | W814 | 改：文件索引条该品牌字面去品牌化 |
| scripts/output/_w814_spec.json | W814 | 改：本批 spec（级联唯一来源） |

## W813 review 修复批（2026-10-20）

| 文件 | W | 说明 |
|---|---|---|
| xiyouji-agent-web/server/errors.ts | W813 | 改：全局错误处理中间件的框架层四百类保真（异常自带四百状态码即按原状态码返回·固定文案表防细节外泄·日志新增客户端错误分支记警告不记堆栈） |
| xiyouji-agent-web/server/api.integration.test.ts | W813 | 改：补两条集成测试（请求体畸形返四百而非五百 + 错误体不含堆栈与异常类名与原始解析消息） |
| tests/unit/test_ci_wiring.py | W813 | 改：YAML 守卫 J2 判据扩至任意映射键（原只查名称键）+ J3 的依赖缺失由静默跳过改为判红 + 补守卫负样本实证（4 种坏形态必红 + 4 种形态真属解析失败 + 合法形态不误杀 + 依赖已登记回归锁） |
| scripts/requirements.txt | W813 | 改：登记 PyYAML==6.0.2（使守卫 J3 全量解析在持续集成侧恒生效·原实现因依赖缺失恒静默跳过） |
| scripts/check_doc_sync.py | W813 | 改：文件清单路径正则扩展覆盖 .ts/.tsx/.cjs/.jsonl/.yaml/.toml/.ini/.cfg/.sh/.ps1/.csv/.svg/.example（原先静默滤除·滤除即不被校验）+ 自测补 T19/T20 两条 |
| docs/agent/gates.md | W813 | 改：第 31 门禁条目补记 C4-f 覆盖面扩面事实与自测例数 |
| AGENTS.md | W813 | 改：§4.3 本机环境事实补记 PyYAML 为守卫依赖（持续集成恒有） |

## W812 去旧厂商 Agent 工具品牌化批（2026-10-20）

| 文件 | W | 说明 |
|---|---|---|
| .gitignore | W812 | 改：删该厂商工具目录的忽略规则（2 行） |
| AGENTS.md | W812 | 改：机器环境事实条两条——「提交门禁 hook 解释器」改写为遵循仓内工具清单口径（全局 Python 3.12·`py -3` 优先·去掉厂商托管运行时指向）+「全局 Python 3.12」条补三语境分清（仓内文档/CI/Makefile 用可移植 `python`·本机 PowerShell 用 `py -3`） |
| CHANGELOG.md | W812 | 改：现役与历史段该品牌字样去品牌化（认领/来源/环境事实类叙述） |
| archive/docs/CHANGELOG-ARCHIVE.md | W812 | 改：归档段该品牌字样去品牌化（豁免登记/环境事实/硬性排除三类） |
| archive/docs/file-index-ARCHIVE.md | W812 | 改：归档文件索引条该品牌字样去品牌化 |
| archive/docs/plans/2026-09-09-service-experience-and-agent-ops-plans.md | W812 | 改：品牌清零类裁决叙述去品牌化（复合表述改为旧厂商 Agent 品牌含 旧厂商 Agent 品牌） |
| archive/docs/plans/2026-09-17-agent-web-redesign-plan.md | W812 | 改：v2 修订说明/清理范围/验收判据/遗留登记四处去品牌化 |
| archive/docs/plans/2026-10-07-agent-web-engine-swap-plan.md | W812 | 改：用户裁决链/目标/文档面验收/W681 判据/收官判据五处去品牌化 |
| archive/scripts/_scan_sd_anchors.py | W812 | 改：ROOT 与守卫根上溯三级对齐项目根（顺修归档后目录加深的解析错位）+ 报告落 tmpe/_reports/ |
| archive/scripts/_scan_sd_misplace.py | W812 | 改：ROOT 与守卫根上溯三级对齐项目根 + 报告落 tmpe/_reports/ + docstring 同步 |
| archive/scripts/batches/misc/adversarial-review-integrated-2026-08-11.md | W812 | 改：记忆/技能路径与工具名叙述去品牌化（6 处） |
| archive/scripts/batches/misc/link-audit-report.md | W812 | 改：链接扫描排除目录默认值叙述去品牌化（3 处） |
| archive/scripts/batches/misc/perf_canvas_report.md | W812 | 改：运行时模块路径写法去品牌化（2 处） |
| archive/scripts/batches/w5xx/_w568_spec.json | W812 | 改：归档批 spec 的环境事实叙述去品牌化 |
| archive/scripts/batches/w5xx/_w596_spec.json | W812 | 改：归档批 spec 的豁免登记叙述去品牌化 |
| archive/scripts/batches/w6xx/_w684_spec.json | W812 | 改：归档批 spec 的品牌清零登记叙述去品牌化 |
| archive/scripts/w334_font_subset.py | W812 | 改：字体子集脚本的托管虚拟环境路径改指系统解释器 |
| docs/00-导读/W批次编号对账表.md | W812 | 改：W726-W750 共 23 行认领会话列去品牌化（结构性修改·按 pitfalls 列入 touches）+ W812 认领行与 bullet |
| docs/11-方案报告/W761工具链可维护性重构报告-2026-10-16.md | W812 | 改：报告头负责人署名去品牌化 |
| docs/11-方案报告/工作复盘与优化分析报告/工作复盘与优化分析报告-2026-10-07-治理与引擎.md | W812 | 改：复盘范围叙述的品牌清零表述去品牌化 |
| docs/11-方案报告/工作复盘与优化分析报告/工作复盘与优化分析报告-2026-10-13.md | W812 | 改：元信息块/信息来源/自动化项/经验库结构/假设清单五处去品牌化 |
| docs/11-方案报告/工作复盘与优化分析报告/工作复盘与优化分析报告-2026-10-14.md | W812 | 改：元信息块/跨周期自证/工具依赖/经验库落点/衔接说明五处去品牌化 |
| docs/11-方案报告/工作复盘与优化分析报告/工作复盘与优化分析报告-2026-10-15.md | W812 | 改：报告头/责任人/任务卡/坑族/知识资产各表署名列去品牌化（27 处） |
| docs/11-方案报告/工作复盘与优化分析报告/工作复盘与优化分析报告-2026-10-17.md | W812 | 改：报告头/责任人/任务卡/行动项/优先级各表署名列去品牌化（15 处） |
| docs/11-方案报告/计划方案/T01-任务计划执行与经验沉淀报告-2026-10-14.md | W812 | 改：报告头/记忆落点/验收判据三处去品牌化 |
| docs/11-方案报告/计划方案/执行前计划-T01.md | W812 | 改：负责人/验收判据/假设表/任务表八处去品牌化 |
| docs/superpowers/plans/2026-09-21-demand-side-optimization-master-plan.md | W812 | 改：豁免域登记叙述去品牌化 |
| docs/superpowers/plans/2026-10-14-interference-governance-roadmap.md | W812 | 改：干扰日志表会话列去品牌化（4 行·保留并行会话语义） |
| scripts/archive_file.py | W812 | 改：引用扫描去掉该厂商目录的排除项 |
| scripts/gen_folder_docs.py | W812 | 改：目录文档生成的排除目录元组去掉该项 |
| scripts/output/_w745_spec.json | W812 | 改：现役 spec 的仓库卫生与文件行叙述去品牌化 |
| scripts/output/_w778_spec.json | W812 | 改：现役 spec 的来源叙述去品牌化 |
| scripts/preflight_check.py | W812 | 改：工作树态统计去掉该厂商目录的排除分支（3 处·说明行/docstring/排除 if） |
| site/data/search.html | W812 | 改：内嵌搜索索引载荷随文档变更重生成 + CSP 哈希重算 |
| site/en/search.html | W812 | 改：内嵌搜索索引载荷随文档变更重生成 + CSP 哈希重算 |
| tests/unit/test_preflight_check.py | W812 | 改：用例改测工作树态三态计数本身 + 认领会话样例去品牌化 |
| tmpe/README.md | W812 | 改：活跃冻结区并行会话表述去品牌化 |
| CLAUDE.md | W812 | 改：环境注意段增「调用形态」指针一行——本机 PowerShell 侧 `python` 是应用执行存根（调用即静默失败）→ 该侧改写 `py -3`（可移植形态仍为 `python`·CI/Linux/macOS 通用） |
| scripts/README.md | W812 | 改：工具表头增「调用形态」指针一行——表内 `python <脚本>` 为可移植形态，本机 PowerShell 侧改写 `py -3 <脚本>` |

## W811 CI 断链修复批（2026-10-20）

| 文件 | W | 说明 |
|---|---|---|
| .github/workflows/ci.yml | W811 | 修复：step 名加引号（W806 裸标量含冒号空格致 YAML 映射歧义·GitHub 0 秒失败该 workflow） |
| tests/unit/test_ci_wiring.py | W811 | 增：工作流 YAML 可解析性守卫（三判据·负样本实证·CI 恒生效不依赖 PyYAML） |

## W810 站内搜索死代码清理批（2026-10-20）

| 文件 | W | 说明 |
|---|---|---|
| site/data/search.html | W810 | 删 legacy 死数组 `window.SEARCH_INDEX = [...]`（−2271 字节）+ CSP 哈希重算 |
| site/en/search.html | W810 | 删 legacy 死数组 `window.SEARCH_INDEX = [...]`（−2329 字节）+ CSP 哈希重算 |

## W809 站内搜索索引新鲜度门禁挂载批（2026-10-20）

| 文件 | W | 说明 |
|---|---|---|
| scripts/check_search_index_fresh.py | W809 | 新建：站内搜索索引新鲜度门禁（第 46 槽·三判据·fail-closed·只读不写） |
| scripts/_gen_search_index.py | W809 | 函数化：算与写分离（build_indexes 纯计算 + main 写盘·挂槽前置） |
| tests/unit/test_check_search_index_fresh.py | W809 | 新建：第 46 槽门禁专项单测 5 例（含 fail-closed 与挂载一致性） |
| scripts/verify_delivery.py | W809 | 挂载第 46 槽门禁（元组 + 段名表 + docs/site 两面 scope 归属） |
| docs/agent/gates.md | W809 | 新增第 46 槽门禁定义（编号三方对账的一端） |

## W808 Web Agent 全栈加固批（2026-10-20）

| 文件 | W | 说明 |
|---|---|---|
| xiyouji-agent-web/server/errors.ts | W808 | 新建：类型化错误层级 + 全局错误处理中间件（运营错结构化返回·编程错只记日志返通用 500·不泄堆栈） |
| xiyouji-agent-web/server/logger.ts | W808 | 新建：结构化 JSON 日志 + 凭证脱敏 + request ID 上下文 |
| xiyouji-agent-web/server/requestId.ts | W808 | 新建：request ID 生成与传播（响应头回写 + 上游 ID 沿用 + 畸形 ID 净化） |
| xiyouji-agent-web/server/validation.ts | W808 | 新建：Zod 边界校验（全部 /api 端点入参·零信任客户端） |
| xiyouji-agent-web/server/shutdown.ts | W808 | 新建：优雅关闭（SIGTERM/SIGINT 排空在途请求 + WAL checkpoint + 关库） |
| xiyouji-agent-web/server/api.integration.test.ts | W808 | 新建：第二层集成测试（真实起服 + 真实 HTTP + 真实 SQLite·14 例·禁 mock 冒充） |
| xiyouji-agent-web/src/utils/api.ts | W808 | 重写：统一 API client（补 res.ok 判定 + 类型化 ApiError + 共享 token 注入 + 可配基址） |
| xiyouji-agent-web/src/utils/apiTypes.ts | W808 | 新建：前后端共享 API 契约类型（字段改名即编译期报错） |
| xiyouji-agent-web/src/utils/errorMessage.ts | W808 | 新建：状态码 → 用户可读文案映射（此前失败只 console.error 吞掉） |
| xiyouji-agent-web/src/utils/api.test.ts | W808 | 新建：前端单元测试 17 例（res.ok/token/基址三缺陷各有负样本） |
| xiyouji-agent-web/src/utils/errorMessage.test.ts | W808 | 新建：错误文案映射单元测试（4xx/5xx/网络不可达全覆盖） |
| xiyouji-agent-web/src/hooks/useSessions.test.tsx | W808 | 新建：会话 hook 失败态可见性测试（错误不得被当数据塞进列表） |
| xiyouji-agent-web/src/hooks/useSessions.ts | W808 | 改：收敛到统一 client + 新增 error/isLoading 状态（失败可见） |
| xiyouji-agent-web/src/hooks/useModels.ts | W808 | 改：收敛到统一 client + 新增 error 状态 |
| xiyouji-agent-web/src/hooks/useChat.ts | W808 | 改：SSE 路径补判非 2xx（此前 401 被当流解析致永久挂起）+ 权限回执走统一 client |
| xiyouji-agent-web/src/components/ChatMessages.tsx | W808 | 修真实缺陷：反馈补传 sessionId（此前恒 400 且静默丢弃·赞踩从未记录） |
| xiyouji-agent-web/src/components/SettingsPage.tsx | W808 | 改：check-login 走统一 client（此前 401/500 被当成功数据） |
| xiyouji-agent-web/src/pages/ChatPage.tsx | W808 | 改：透传 sessionId 给消息区（反馈接口必填） |
| xiyouji-agent-web/src/App.tsx | W808 | 改：新增加载失败横幅 + 重试入口（此前空白无提示） |
| xiyouji-agent-web/src/test/setup.ts | W808 | 新建：vitest 全局准备（jest-dom + jsdom 缺失 API 补齐） |
| xiyouji-agent-web/e2e/chat.e2e.mjs | W808 | 新建：第三层 E2E（真实浏览器 + 真实构建产物 + 真实后端 + 真实 SQLite·10 断言） |
| xiyouji-agent-web/e2e/mockLlm.mjs | W808 | 新建：OpenAI-compatible 假 LLM 端点（外部依赖替身·被测系统全真实） |
| xiyouji-agent-web/vite.config.ts | W808 | 改：代理层注入共享 token（不进浏览器包）+ 代理目标可配 + preview 代理 |
| xiyouji-agent-web/vitest.config.ts | W808 | 新建：前端单元测试配置（jsdom + setup + 包含面） |
| xiyouji-agent-web/tsconfig.node.json | W808 | 根修：编译产物改 outDir=./.tsbuild（此前 vite.config.js 遮蔽 .ts·配置改动静默失效） |
| xiyouji-agent-web/server/config.ts | W808 | 修：补 dotenv 加载（此前声明了依赖却从未 import·.env 流程实际从未生效） |
| xiyouji-agent-web/server/index.ts | W808 | 改：全局错误处理 + /api 404 兜底 + 优雅关闭接线 |
| xiyouji-agent-web/server/routes.ts | W808 | 改：入参经 Zod 校验 + 类型化错误（对外状态码与文案逐字不变） |
| xiyouji-agent-web/server/middleware.ts | W808 | 改：request ID + 访问日志 + 限流改抛类型化错误 |
| xiyouji-agent-web/server/db.ts | W808 | 新增：closeDatabase（WAL checkpoint + 关库·优雅关闭用） |
| xiyouji-agent-web/package.json | W808 | 改：新增 test:client / test:integration / test:e2e / test:all 脚本 + zod 直依赖 |
| .github/workflows/ci.yml | W808 | 改：agent-web-build job 接线三层测试（单测 + 集成 + E2E 含 Playwright chromium） |
| .gitignore | W808 | 改：新增 xiyouji-agent-web/.tsbuild/ 忽略（编译产物移出源目录） |

## W807 站内搜索索引刷新批（2026-10-20）

| 文件 | W | 说明 |
|---|---|---|
| scripts/_gen_search_index.py | W807 | 恢复 W573 原位（常驻留档·内容批次收尾重跑）：全站搜索索引生成器 |
| site/data/search.html | W807 | 搜索索引刷新（doc 条目 61→111·失效目录引用 9→0）+ CSP 哈希重算 |
| site/en/search.html | W807 | 搜索索引刷新（doc 条目 61→111）+ CSP 哈希重算 |
| tests/e2e/test_site_quality.js | W807 | 新增 S1/S1b 两条搜索页常驻断言（负样本实证旧索引必红） |

## W806 GoatCounter 统计链彻底退役批（2026-10-20）

| 文件 | W | 说明 |
|---|---|---|
| scripts/check_no_goatcounter.py | W806 | 新建：GoatCounter 退役防回退守卫（四项判据·自测 1 正 4 负·CI 接线） |
| tests/unit/test_check_no_goatcounter.py | W806 | 新建：守卫专项单测 5 例（现网实跑/自检/判据单元/忽略规则/退出码） |
| scripts/generate_csp.py | W806 | connect-src 去 GoatCounter 计数端点（856 页 CSP 重算·546 页放行回收） |
| site/js/rum.js | W806 | 上报通道三口径改造（删 GoatCounter 改道分支与 bucket 死函数·线上零外发） |
| site/js/visit-log.js | W806 | 注释口径同步（GoatCounter 已退役·本文件为现役唯一访问记录面） |
| site/rum-viewer.html | W806 | 说明段改写（生产无 CWV 外发通道·dev origin 回流口径） |
| site/data/search.html | W806 | 摘除活的 window.goatcounter.count 搜索词上报分支（仅留 localStorage） |
| site/en/search.html | W806 | 摘除活的 window.goatcounter.count 搜索词上报分支（仅留 localStorage） |
| site/_headers | W806 | 平台层 CSP connect-src 去 GoatCounter 域 |
| scripts/fetch_gate_stats.py | W806 | 加 W806 现状声明（后端失效·保留在库供账号重建后复用） |
| docs/00-导读/访问统计方案.md | W806 | 改写为《访问统计现状与退役记录》（退役依据/历史选型存档/恢复路径） |
| docs/00-导读/V2可视化维度方案.md | W806 | 零外域请求口径改为全站零例外 |
| docs/11-方案报告/读者数据复盘.md | W806 | 加 W806 现状声明（W626 判定保留·数据源重建前无法复算） |

## W805 跨平台测试守卫热修批（2026-10-19）

| 文件 | W | 说明 |
|---|---|---|
| tests/test_xiyouji_mcp_extra.py | W805 | 目录目标守卫跨平台化（PermissionError → OSError·测试更名 os_error·生产代码零改动） |

## W804 桌面版三平台安装包与自动更新批（2026-10-19）

| 文件 | W | 说明 |
|---|---|---|
| xiyouji-desktop/package.json | W804 | 桌面版工程（electron 44.9.0 + electron-builder 26.15.3 + electron-updater 6.8.9·version 2.3.0） |
| xiyouji-desktop/electron-builder.yml | W804 | 三平台打包配置（NSIS/macOS universal dmg+zip/Linux AppImage·产物名固定字面量·publish=GitHub Releases） |
| xiyouji-desktop/src/main.cjs | W804 | Electron 主进程（单实例/窗口/菜单/安全策略/--self-test 无窗口冒烟） |
| xiyouji-desktop/src/server.cjs | W804 | 本地静态服务（127.0.0.1 随机端口/穿越防护/仅 GET+HEAD/MIME/缓存头） |
| xiyouji-desktop/src/updater.cjs | W804 | electron-updater 自动更新（3 秒首查·4 小时复查·下载/重启中文对话框） |
| xiyouji-desktop/scripts/prepare-content.mjs | W804 | 构建期内容版本清单注入（CHANGELOG 首段动态批次 + stats 计数） |
| xiyouji-desktop/tests/ | W804 | node --test 33 项（静态服务/内容准备/打包配置契约） |
| .github/workflows/release.yml | W804 | 三平台桌面发布工作流（版本闸门→构建→Release+latest*.yml 自动更新元数据） |
| .github/workflows/ci.yml | W804 | 新增 desktop-build job（npm ci + node --test + electron-builder --dir 打包回归） |

## W803 工具链行为保持重构批：公共骨架提取与长函数拆分（2026-10-19）

| 文件 | W | 说明 |
|---|---|---|
| scripts/utils/gate_common.py | W803 | 新建·门禁族公共骨架（12 个公共符号：路径/读取/站点清单/样式块/自测跑批/CLI 分发） |
| scripts/check_css_decl_separators.py | W803 | 消费 gate_common·第 35 门禁 stdout 逐字节不变 |
| scripts/check_css_orphan_selectors.py | W803 | 消费 gate_common·二源变体用 site_pages(root=False) |
| scripts/check_css_var_refs.py | W803 | 消费 gate_common·第 34 门禁 stdout 逐字节不变 |
| scripts/check_html_head_content.py | W803 | 消费 gate_common·第 33 门禁 stdout 逐字节不变 |
| scripts/check_kpi_card_base.py | W803 | 消费 gate_common·第 37 门禁 stdout 逐字节不变 |
| scripts/check_agents_layers.py | W803 | 消费 gate_common·SelfTestTally 收敛自测计数 |
| scripts/check_claude_md.py | W803 | 消费 gate_common·清 C3 行数计算死代码（7 边界样本证明等值） |
| scripts/lint_links.py | W803 | _process_file 69→拆分·路径解析口径去重·import 提模块级·逐字节对拍一致 |
| mcp-server/xiyouji_mcp.py | W803 | 4 个 MCP 工具拆分（长函数 5→1·最长 102→66）·常量提升·注解收敛·30 组对拍一致 |
| xiyouji-agent-web/server/index.ts | W803 | 710→51 行·按职责拆为 chat/config/http/middleware/permissions/routes/sse |
| xiyouji-agent-web/src/components/ToolCallsCollapse.tsx | W803 | 767→166 行·渲染分支拆为 src/components/toolCalls/ 五模块 |

## W802 character_nlp 行为保持重构批·二（2026-10-19）

| 文件 | W | 说明 |
|---|---|---|
| scripts/B_人物/character_nlp.py | W802 | 行为保持重构·二：引语扫描 89→4 函数·时间线 85→4 函数 |

## W801 character_nlp 行为保持重构批（2026-10-19）

| 文件 | W | 说明 |
|---|---|---|
| scripts/B_人物/character_nlp.py | W801 | 行为保持重构：情感构建 190→7 函数·main 175→9 函数·五处写盘收敛 |
| docs/superpowers/plans/2026-09-30-maintenance-backlog-registry.md | W801 | B-109 登记（cooccurrence 输出非确定） |

## W800 第四轮外部评审回应批（2026-10-19）

| 文件 | W | 说明 |
|---|---|---|
| README.md | W800 | 门禁边界（保真不保质）+ 阅读契约后移 + 133 维性质分层 |
| docs/00-导读/协议边界速查.md | W805 | 双协议适用范围 + 边界快速表（MIT/CC BY-NC 4.0） |
| docs/00-导读/统计口径说明.md | W800 | §3 维度分层 + §8 文本与数据基础及适用性限制 |
| docs/superpowers/plans/2026-09-30-maintenance-backlog-registry.md | W800 | B-105~B-108 登记（第四轮评审） |

## W799 截图桶 TTL 收紧批（2026-10-19）

| 文件 | W | 说明 |
|---|---|---|
| tmpe/policy.yml | W799 | ttl_days._shot 30→7（临时证据桶收紧） |

## W798 对拍模板转正批（2026-10-19）

| 文件 | W | 说明 |
|---|---|---|
| docs/_templates/duipai/README.md | W798 | 新增：对拍模板入库版说明（路径与定位更新） |
| docs/_templates/duipai/duipai.py | W798 | 新增：对拍模板脚本（snapshot/compare） |
| docs/10-方法论沉淀/批次交付流水线.md | W798 | §八模板路径改指 docs/_templates/duipai/ |

## W797 历史模板归档批（2026-10-19）

| 文件 | W | 说明 |
|---|---|---|
| archive/docs/templates/README.md | W797 | 新增：历史模板馆藏说明（退休依据/出生证明/后代载体） |
| archive/docs/templates/article-template.md | W797 | 迁入：docs/_templates/ 退休（0% 采用） |
| archive/docs/templates/handoff-checklist.md | W797 | 迁入：docs/_templates/ 退休（subagent 协议已演化） |
| archive/docs/templates/validation-checklist.md | W797 | 迁入：docs/_templates/ 退休（同上） |
| docs/00-导读/文档规范.md | W797 | 新增 §12 交付自检（10 项） |
| docs/_templates/README.md | W797 | 目录刷新（现役模板位·0 直属文件） |

## W796 提示词库整理入库批（2026-10-19）

| 文件 | W | 说明 |
|---|---|---|
| docs/12-提示词库/00-总目录.md | W796 | 新增：模块索引+冲突处理+Q-01~Q-05 决策记录 |
| docs/12-提示词库/01-参考链接.md | W796 | 新增：8 设计灵感站点 |
| docs/12-提示词库/02-写作与输出规范.md | W796 | 新增：计划要求/润色 skill/成果要素/回答风格 |
| docs/12-提示词库/03-工作复盘提示词.md | W796 | 新增：复盘系统提示词全文（L29-465） |
| docs/12-提示词库/04-任务执行提示词.md | W796 | 新增：任务系统提示词全文（L466-829） |
| docs/12-提示词库/05-项目审查任务书.md | W796 | 新增：7 段审查合并 R-1~R-7 |
| docs/12-提示词库/06-隐私与开源边界.md | W796 | 新增：隐私边界（独立前置） |
| docs/12-提示词库/07-安全架构准则.md | W796 | 新增：安全六域 |
| docs/12-提示词库/08-团队角色分工.md | W796 | 新增：角色清单/工具/职责 |
| docs/12-提示词库/09-导师提问流程.md | W796 | 新增：15 问流程 |
| docs/12-提示词库/10-创意写作题.md | W796 | 新增：创意四题 |
| docs/12-提示词库/11-colors.md | W796 | 新增：20 组色彩素材+RGB/HEX 校准表 |
| scripts/docs_index.py | W796 | 新增第 13 板块「12 · 提示词库」标题 |
| STRUCTURE.md | W796 | 新增 12-提示词库 段条目 |

## W795 第 42 篇复盘报告入库批（2026-10-19）

| 文件 | W | 说明 |
|---|---|---|
| docs/11-方案报告/工作复盘与优化分析报告/工作复盘与优化分析报告-2026-10-19.md | W795 | 新增：第 42 篇复盘（W777-W794 十八段·E-17~E-24） |
| docs/11-方案报告/README.md | W795 | 索引行 24（第 42 篇） |
| STRUCTURE.md | W795 | 11-方案报告计数 23→24（标记 27→28） |

## W794 PD-3 裁决落地批（2026-10-19）

| 文件 | W | 说明 |
|---|---|---|
| site/index.html | W794 | A1：补 06 个人随笔行 + 九卷→全卷命名 |
| site/dashboard.html | W794 | A2：DATA 提示改读者语；A3：图例半句 + 30 卡 title |
| tests/e2e/baseline/index.png | W794 | 视觉基线同步（06 行新增） |
| tests/e2e/baseline/dashboard.png | W794 | 视觉基线同步（提示与图例变更） |
| docs/superpowers/plans/2026-10-18-pd3-heuristic-review-report.md | W794 | F-08 撤回 + §5 落地记录 |
| docs/superpowers/plans/2026-09-30-maintenance-backlog-registry.md | W794 | B-104 撤回 |

## W793 PD-3 走查与 BL-31 退休批（2026-10-18）

| 文件 | W | 说明 |
|---|---|---|
| docs/superpowers/plans/2026-10-18-pd3-heuristic-review-report.md | W793 | 新增：PD-3 两页启发式走查报告（8 findings·20 格·AC-1 8/8） |
| scripts/_pd3_finding_probe.js | W793 | 新增：双模式取证/防虚构探针（capture + report） |
| scripts/sync_docs.py | W793 | 删除：退役（职责并入第 31 门禁 check_doc_sync） |
| scripts/release.py | W793 | step1 改指 check_doc_sync + checklist 旧命令更新 |
| HANDOVER.md | W793 | 冻结适用范围单一权威表述（W793 立） |
| docs/superpowers/plans/2026-09-30-maintenance-backlog-registry.md | W793 | B-100~B-104 追加（PD-3 工程分流） |
| docs/11-方案报告/全仓待办计划方案状态核查报告-2026-10-18.md | W793 | PD 行陈滞自修（待批复→已批+已执行） |
| Makefile | W793 | release 注释 doc-sync 化 |

## W792 全仓待办计划状态核查批（2026-10-18）

| 文件 | W | 说明 |
|---|---|---|
| docs/11-方案报告/全仓待办计划方案状态核查报告-2026-10-18.md | W792 | 新增：全仓待办核查报告（五分类+5 处陈滞修正+4 决策项） |
| HANDOVER.md | W792 | BL-22 ✅ 标注 + 候选清单配额终止注 |
| docs/superpowers/plans/2026-09-30-maintenance-backlog-registry.md | W792 | B-1~B-7 状态回写（4 ✅·2 ◐·1 ☐） |
| docs/superpowers/plans/2026-09-29-en-data-i18n-display-plan.md | W792 | 状态行回写（快赢层 ✅·根治层排期） |
| docs/superpowers/plans/2026-10-13-code-refactor-w728.md | W792 | 执行状态行回写（✅ 已执行） |

## W791 agent-web 攻击面负向测试批（2026-10-18）

| 文件 | W | 说明 |
|---|---|---|
| xiyouji-agent-web/server/security.ts | W791 | 新增：安全边界纯函数与 SSE 守卫（BL-29 提取） |
| xiyouji-agent-web/server/security.test.ts | W791 | 新增：17 例攻击面负向测试（BL-29） |
| xiyouji-agent-web/server/index.ts | W791 | 安全逻辑提取至 security.ts（14 增 54 删）+ W568 漏改修正 |
| xiyouji-agent-web/package.json | W791 | test:server 接入 security.test.ts |
| docs/superpowers/plans/2026-09-21-demand-side-optimization-master-plan.md | W791 | D2/E 状态行陈滞回写 ✅ + 计划头状态收官 |
| HANDOVER.md | W791 | BL-23/24 关闭标注 |

## W790 外部评审第三轮回应登记批（2026-10-18）

| 文件 | W | 说明 |
|---|---|---|
| docs/11-方案报告/外部评审回应与逐项核查报告-2026-10-18.md | W790 | 新增：外部评审第三轮回应报告（重复投递认定+七项裁定+BL-29~32） |
| HANDOVER.md | W790 | Backlog 登记 BL-29~32 |
| docs/11-方案报告/README.md | W790 | 索引加行 22 |
| STRUCTURE.md | W790 | 11-方案报告段现役报告计数 21→22 |
| scripts/output/stats.json | W790 | report_docs 25→26·--w W790 刷新 |
| docs/INDEX.md | W790 | 重建纳入新报告（701→702 篇） |

## W789 外部门禁重构提案对盘登记批（2026-10-18）

| 文件 | W | 说明 |
|---|---|---|
| docs/00-导读/W批次编号对账表.md | W789 | W789 认领登记（外部门禁重构提案对盘裁定不执行） |

## W788 JS 门禁死代码清理批（2026-10-18）

| 文件 | W | 说明 |
|---|---|---|
| scripts/check_screenshot_gates.js | W788 | 清理：删 W775 新增的死常量 GATE_NAME（零引用·该门禁靠退出码判定不需汇总末行） |
| scripts/lib/playwright_gate_utils.js | W788 | 清理：删未使用导入 path（该文件由 W775 全量新增·原生瑕疵） |
| docs/00-导读/W批次编号对账表.md | W788 | W788 认领登记 |

## W787 release.py 行为保持重构批（2026-10-18）

| 文件 | W | 说明 |
|---|---|---|
| scripts/release.py | W787 | 行为保持重构：常量化+拆函数（步进标题复用） |
| docs/00-导读/W批次编号对账表.md | W787 | W787 认领登记 |

## W786 graph_seed_neo4j 行为保持重构批（2026-10-18）

| 文件 | W | 说明 |
|---|---|---|
| scripts/rag/graph_seed_neo4j.py | W786 | 行为保持重构：_build_cypher/_build_snapshot 提函数 |
| docs/00-导读/W批次编号对账表.md | W786 | W786 认领登记 |

## W785 api_server 行为保持重构批（2026-10-18）

| 文件 | W | 说明 |
|---|---|---|
| scripts/api/api_server.py | W785 | 行为保持重构：常量提级+路由拆臂+错误结构统一+行渲染提函数 |
| docs/00-导读/W批次编号对账表.md | W785 | W785 认领登记 |

## W784 分析与审计五小件行为保持重构批（2026-10-18）

| 文件 | W | 说明 |
|---|---|---|
| scripts/A_文本基础/chapter_stats.py | W784 | 行为保持重构：诗词计数拆双函数+聚合提函数 |
| scripts/A_文本基础/word_frequency.py | W784 | 行为保持重构：token 过滤提函数+常量化 |
| scripts/AA_叙事实验/narrative_experiment.py | W784 | 行为保持重构：输出/口志拆函数（build_summary 单次复用） |
| scripts/C_情节/hardships_81.py | W784 | 行为保持重构：标签字典提模块级+输出拆函数 |
| scripts/audit/line_check.py | W784 | 行为保持重构：self_test 拆三查+查询提函数 |
| docs/00-导读/W批次编号对账表.md | W784 | W784 认领登记 |

## W783 B_人物行为保持重构批（2026-10-18）

| 文件 | W | 说明 |
|---|---|---|
| scripts/B_人物/character_appearance.py | W783 | 行为保持重构：聚合拆三函数+首回计算提函数（保急切求值） |
| scripts/B_人物/character_network.py | W783 | 行为保持重构：共现累积拆函数+combinations 等价 |
| docs/00-导读/W批次编号对账表.md | W783 | W783 认领登记 |

## W782 utils 与 run_all 行为保持重构批（2026-10-18）

| 文件 | W | 说明 |
|---|---|---|
| scripts/utils/aliases.py | W782 | 行为保持重构：lru_cache+setdefault·更名 _alias_to_canonical·docstring 现实化 |
| scripts/utils/text_loader.py | W782 | 行为保持重构：常量提取+三函数拆分（W563 溯源保留） |
| scripts/utils/analyzer_base.py | W782 | 行为保持重构：路径常量提模块级+四函数拆分 |
| scripts/utils/__init__.py | W782 | docstring 升级为模块清单（含 path_guard） |
| scripts/run_all.py | W782 | 行为保持重构：超时常量化+五函数拆分 |
| docs/00-导读/W批次编号对账表.md | W782 | W782 认领登记 |

## W781 门禁防线收口批（2026-10-18）

| 文件 | W | 说明 |
|---|---|---|
| scripts/verify_delivery.py | W781 | R-1 注册表派生+启动期四查+自洽锁反向查+EXPECTED 补目录文档（50 段） |
| scripts/release_prep.py | W781 | R-2 desc/head_sentence 禁以 W### 开头判据 |
| scripts/batch_cascade.py | W781 | R-2 页脚插入防御性剥离前导批次号 |
| scripts/check_governance_docs.py | W781 | R-3 转正 FAIL（docstring 同步） |
| docs/agent/gates.md | W781 | 第 22 条转正记录 |
| docs/agent/pitfalls.md | W781 | W698 scope 条目增补 R-1 演进（就地·条目数不变） |
| tests/unit/test_verify_registry.py | W781 | 新建：8 例（四查负样本+锁双向+派生覆盖） |
| tests/unit/test_release_prep.py | W781 | 增 2 例（desc/head_sentence 批次号开头负样本） |
| docs/00-导读/W批次编号对账表.md | W781 | W781 认领登记 |

## W780 目录文档新鲜度门禁批（2026-10-18）

| 文件 | W | 说明 |
|---|---|---|
| scripts/check_folder_docs.py | W780 | 新建：目录文档新鲜度门禁（第 45 槽·四判据对拍·--self-test 7 例） |
| scripts/gen_folder_docs.py | W780 | 模块化（GOVERNED_SKIP/in_scope/case_collides）+ --refresh 安全刷新（所有权标记判定） |
| scripts/verify_delivery.py | W780 | 第 45 槽注册（目录文档段·_StrictGate）+ 校数注释按实跑回写 |
| tests/unit/test_folder_docs_gate.py | W780 | 新建：16 例（合成树断言 + refresh 修复/保护 + 大小写判定 + CLI 退出码） |
| docs/agent/gates.md | W780 | 第 45 槽全量定义 + 速查表 27-42→27-45 存量漂移顺修 |
| AGENTS.md | W780 | §4.2 计数 44→45（四处）+ 新增条目 45 |
| docs/00-导读/W批次编号对账表.md | W780 | W780 认领登记 |
| scripts/output/stats.json | W780 | gate_count 44→45（--w W780） |

## W779 全仓目录索引补齐批（2026-10-18）

| 文件 | W | 说明 |
|---|---|---|
| scripts/gen_folder_docs.py | W779 | 目录索引生成器（幂等·大小写判重防覆写 INDEX.md·gitignored 过滤·治理树排除·--dry-run/--force） |
| docs/INDEX.md | W779 | 重建（697→701 篇·docs_index.py·第 17 门禁产物级一致） |
| scripts/output/script-coverage-baseline.txt | W779 | 登记 gen_folder_docs.py 豁免行（第 42 门禁 C1） |
| docs/00-导读/W批次编号对账表.md | W779 | W779 认领登记 |
| CHANGELOG.md | W779 | 新增 W779 版段 + 编号规则 W001-W778→W779 |
| HANDOVER.md | W779 | 最后更新链首 + 当前进度段 W779 摘要 |
| README.md | W779 | 抬头当前批次 W778→W779 |
| STRUCTURE.md | W779 | 抬头当前批次 W778→W779 + 工具与输出表新增「目录索引生成」行 |
| CITATION.cff | W779 | version W778→W779（外部引用面·第 27 门禁 R2） |
| scripts/output/file-index.md | W779 | 本段（W779 per-file 登记） |
| .github/（index.md ×3） | W779 | 逐文件索引（机器可读）·.github 根 + ISSUE_TEMPLATE + workflows |
| archive/（index.md ×20） | W779 | 逐文件索引（机器可读）·archive 根 + docs/scripts 全子树 20 个 |
| assets/（index.md ×5） | W779 | 逐文件索引（机器可读）·根 + fonts/images/maps/fonts-source |
| dataset/（index.md ×2） | W779 | 逐文件索引（机器可读）·根 + entities |
| docs/（index.md ×8） | W779 | 逐文件索引（机器可读）·docs 根 + 00-导读/07/08/09/_templates/agent/superpowers/plans |
| hyperframes/（index.md ×4） | W779 | 逐文件索引（机器可读）·根 + compositions/d3-visualizations + output |
| index.md（根级 ×1） | W779 | 仓库根逐文件索引（机器可读）·列顶层 16 个子目录与根级文件 |
| mcp-server/（index.md ×1） | W779 | 逐文件索引（机器可读） |
| packaging/（index.md ×37） | W779 | 逐文件索引（机器可读）·xiyouji-analysis/src 全树（34 类 analyses 逐一建） |
| references/（index.md ×1） | W779 | 逐文件索引（机器可读） |
| scripts/（index.md ×43） | W779 | 逐文件索引（机器可读）·根 + A-AH 34 类 + api/audit/lib/output/output-data/figures/rag/utils |
| site/（index.md ×22） | W779 | 逐文件索引（机器可读）·根 + chapters/characters/data/data-json/en/en-json/js/reader×5/static×7/themes |
| source/（index.md ×5） | W779 | 逐文件索引（机器可读）·根 + 原文/分回/shendu + 引用与网络解读 |
| tests/（index.md ×4） | W779 | 逐文件索引（机器可读）·根 + unit/e2e/e2e-baseline |
| timeline/（index.md ×1） | W779 | 逐文件索引（机器可读） |
| tools/（index.md ×1） | W779 | 逐文件索引（机器可读） |
| xiyouji-agent-web/（index.md ×9） | W779 | 逐文件索引（机器可读）·根 + server/server-engine/src/src-components/hooks/pages/utils/evals |
| .github/（README.md ×2） | W779 | 目录导读（人读）·.github 根 + ISSUE_TEMPLATE |
| archive/（README.md ×17） | W779 | 目录导读（人读）·archive 根 + docs/scripts 子树 17 个 |
| assets/（README.md ×5） | W779 | 目录导读（人读）·根 + fonts/images/maps/fonts-source |
| dataset/（README.md ×1） | W779 | 目录导读（人读） |
| docs/（README.md ×5） | W779 | 目录导读（人读）·docs 根 + _templates/agent/superpowers/superpowers-plans |
| hyperframes/（README.md ×3） | W779 | 目录导读（人读）·根 + compositions/d3-visualizations |
| packaging/（README.md ×36） | W779 | 目录导读（人读）·xiyouji-analysis 全树 36 个 |
| references/（README.md ×1） | W779 | 目录导读（人读） |
| scripts/（README.md ×41） | W779 | 目录导读（人读）·根 + A-AH 34 类 + api/audit/lib/output/output-data/figures/utils |
| site/（README.md ×21） | W779 | 目录导读（人读）·根 + chapters/characters/data/data-json/en-json/js/reader×5/static×6/themes |
| source/（README.md ×5） | W779 | 目录导读（人读）·根 + 原文/分回/shendu + 引用与网络解读 |
| tests/（README.md ×4） | W779 | 目录导读（人读）·根 + unit/e2e/e2e-baseline |
| timeline/（README.md ×1） | W779 | 目录导读（人读） |
| tools/（README.md ×1） | W779 | 目录导读（人读） |
| xiyouji-agent-web/（README.md ×8） | W779 | 目录导读（人读）·根 + server/server-engine/src/src-components/hooks/pages/utils/evals |

> 全量 318 个目录索引件（index.md 167 + README.md 151）逐文件清单由 `python scripts/gen_folder_docs.py --dry-run` 复现；生成器幂等（重跑写 0 文件）。

## W778 第 41 篇改进项落地批（2026-10-17）

| 文件 | W | 说明 |
|---|---|---|
| docs/agent/pitfalls.md | W778 | 流程节增「latent 三问 + 双平台断言禁例」（6→7 条·总 41） |
| AGENTS.md | W778 | §4.3 读数契约与计数三处同步（41 条/流程 7/总 40→41） |
| docs/10-方法论沉淀/批次交付流水线.md | W778 | 新增 §七 外部产出落地七步 + §八 对拍 SOP（原 §七→§九） |
| docs/11-方案报告/工作复盘与优化分析报告/工作复盘与优化分析报告-2026-10-17.md | W778 | 头部补跨周期执行记录（改进项落地留痕） |
| docs/00-导读/W批次编号对账表.md | W778 | W778 认领登记 |

## W777 第 41 篇复盘报告入库批（2026-10-17）

| 文件 | W | 说明 |
|---|---|---|
| docs/11-方案报告/工作复盘与优化分析报告/工作复盘与优化分析报告-2026-10-17.md | W777 | 第 41 篇复盘（W748-W776 二十八段/60 提交·断档 2 天补课·E-09~E-16/FAM-31~36/WF-03~05） |
| docs/11-方案报告/README.md | W777 | 现役报告索引 20→21 篇（第 21 行） |
| STRUCTURE.md | W777 | report_docs 24→25 + 现役 21 篇 + 复盘系列 12 篇 |
| docs/INDEX.md | W777 | docs_index 重建 696→697 篇 |
| docs/00-导读/W批次编号对账表.md | W777 | W777 认领登记 |

## W776 评审后续行动落地批（2026-10-17）

| 文件 | W | 说明 |
|---|---|---|
| pytest.ini | W776 | 覆盖率口径决策注释（实证 18%/24%/+82%·不引 --cov 门禁·替代=资产清单） |
| scripts/requirements.txt | W776 | 移除 fonttools/brotli 死依赖（全仓零 import 实证·指南改按需安装） |
| scripts/font-subset-guide.md | W776 | §3.1 注记：fonttools/brotli 按需安装（pyftsubset 回退路径） |
| HANDOVER.md | W776 | Backlog 新增 BL-26/27/28（内容质量方差/工程 overhead/单点故障·均不设工程关闭项） |
| docs/10-方法论沉淀/markdown写作规范.md | W776 | §4 增 5 条 AI 内容生产特有反模式 |
| docs/11-方案报告/外部评审回应与逐项核查报告-2026-10-17.md | W776 | §7 四项行动状态更新为已完成（含 A-02 升级处置留痕） |
| docs/00-导读/W批次编号对账表.md | W776 | W776 认领登记 |

## W775 JS 门禁重构落地批（2026-10-17）

| 文件 | W | 说明 |
|---|---|---|
| scripts/lib/gate_common.js | W775 | 新增：门禁公共工具（路径规范化/HTML 枚举/注释剥离/worker 池/汇总行·110 行） |
| scripts/lib/playwright_gate_utils.js | W775 | 新增：Playwright 公共辅助（launch/离线页/file:// 导航·53 行） |
| scripts/check_chart_values.js | W775 | 重构：probeInPage 拆 6 统计函数 + judgeProbe 拆 V1-V5 + validateGateBaseline 合并 + TH 重复键修复（契约对拍零漂移） |
| scripts/check_screenshot_gates.js | W775 | 重构：checkPage 拆 G1-G5 + 删死代码 BENIGN_CONSOLE_RE + 补 use strict（输出逐字节一致） |
| scripts/check_data_drift.js | W775 | 重构 + 潜伏缺陷修复：jsLiteralToJson 引号腐蚀致 2 页静默跳过（可比 57→59·exit 0） |
| tests/unit/test_ci_wiring.py | W775 | gate43 playwright 断言升级传递链两环守护（11 passed） |
| scripts/check_story_timeline_sync.py | W775 | 裁决 3.3：去冗余 and 护栏 + 双 findall（与 parse_html 习语对齐·零行为变化） |
| scripts/check_claude_md.py | W775 | 裁决 3.4：删死常量 MAX_LINES_MSG |
| .gitignore | W775 | scripts/lib/ 定向 negation（lib/ 规则误伤修复） |
| docs/11-方案报告/外部评审回应与逐项核查报告-2026-10-17.md | W775 | 外部评审七项指控逐条核查 + 四项材料实况 + 机制层立场回应 |
| docs/11-方案报告/README.md | W775 | 现役报告索引登记第 20 篇 |
| docs/00-导读/W批次编号对账表.md | W775 | W775 认领登记 |

## W774 CI 首跑分歧修复批（2026-10-17）

| 文件 | W | 说明 |
|---|---|---|
| scripts/docs_index.py | W774 | scan_docs 两处排序显式 str(p).lower() 键（跨平台确定性·CI 首跑分歧根修） |
| tests/unit/test_docs_index.py | W774 | 新增三例：小写键序不变量/真实树不变量/磁盘与生成器一致 |
| docs/11-方案报告/计划方案/执行前计划-T02-工程基础设施薄弱点修复.md | W774 | ST-04 与 AC-02 转闭环（两轮 CI run URL 留证）+不完成定义附记 |
| docs/00-导读/W批次编号对账表.md | W774 | W774 认领行登记 |
| scripts/output/_w774_spec.json | W774 | 本批 spec 入库 |

## W773 工程基础设施薄弱点修复批（2026-10-17）

| 文件 | W | 说明 |
|---|---|---|
| .github/workflows/ci.yml | W773 | 新增 e2e-interaction job（node tests/e2e/test_site_quality.js·8→9 job） |
| .github/workflows/README.md | W773 | Job 9 e2e-interaction 文档节+job 清单 8→9+阈值表补行 |
| tests/unit/test_ci_wiring.py | W773 | 扩 W6 断言（run: 块锚定+Playwright 运行条件·负样本实证） |
| .gitignore | W773 | 取消 tests/e2e/baseline/ 排除（current/ 保持忽略） |
| tests/e2e/baseline/（10 PNG） | W773 | 视觉回归基线版本化入库 |
| tests/e2e/test_visual.js | W773 | 判据升级像素 diff（pngjs+pixelmatch·阈值 0.5%·稳定轮询）+require 解析修复 |
| scripts/package.json | W773 | 新增依赖 pngjs 7.0.0 + pixelmatch 5.3.0 |
| scripts/package-lock.json | W773 | pngjs/pixelmatch 锁文件 |
| site/data/criticism-history.html | W773 | K11 回归修复：reduce 规则移入媒体查询（W674 遗留） |
| site/en/criticism-history.html | W773 | 同族修复（EN 镜像页） |
| scripts/inject_chart_a11y.py | W773 | 加 --dir 参数（rel 按目录深度算·默认行为不变） |
| site/static/js/chart-a11y.js | W773 | 最小 i18n（zh/en·中文页逐字节不变） |
| site/en/（138 页） | W773 | chart-a11y 加载器全量注入+8 页 lang zh-CN→en |
| scripts/validate_en.py | W773 | 补第 3 项检查：文档 lang=en（WCAG 3.1.1·负样本实证） |
| scripts/check_index_health.py | W773 | 第 17 门禁新增第 8 项：docs/INDEX.md 产物级校验 |
| docs/11-方案报告/计划方案/执行前计划-T02-工程基础设施薄弱点修复.md | W773 | 执行记录追加 ST-01~ST-10（含偏差与修正） |
| docs/00-导读/W批次编号对账表.md | W773 | W773 认领行+W772 收官登记+W774 预留 bullet |
| scripts/output/_w773_spec.json | W773 | 本批 spec 入库 |

## W772 计划入库纯文档批（2026-10-17）

| 文件 | W | 说明 |
|---|---|---|
| docs/11-方案报告/计划方案/执行前计划-T02-工程基础设施薄弱点修复.md | W772 | T-02 计划登记入库（四项基础设施缺陷·AC-01~09·修复未动工） |
| docs/11-方案报告/README.md | W772 | 新建「二、计划方案（3 篇）」章节+原二顺延为三 |
| STRUCTURE.md | W772 | report_docs 标记 22→23+现役文字 计划方案 2 篇→3 篇 |
| scripts/output/stats.json | W772 | report_docs 22→23（计划方案 3 篇登记） |
| docs/00-导读/W批次编号对账表.md | W772 | W772 认领行登记 |
| scripts/output/_w772_spec.json | W772 | 本批 spec 入库 |

## W771 编号空洞登记与门禁注释刷新批（2026-10-16）

| 文件 | W | 说明 |
|---|---|---|
| scripts/check_seo_head.py | W771 | 注释陈旧数字刷新 233/230/229→855/851（注释-only·判定零改） |
| scripts/output/_w771_spec.json | W771 | 本批 spec 入库 |
| docs/00-导读/W批次编号对账表.md | W771 | W771 认领行登记 + 递延豁免补十号去向 bullet |

## W770 引文豁免口径修正与数据链路对齐批（2026-10-16）

| 文件 | W | 说明 |
|---|---|---|
| scripts/check_citations.py | W770 | F-2：文首文件级演绎标记识别（两判定面）+ 自测 +2 例（12/12） |
| scripts/C_情节/hardships_81.py | W770 | 输出 hardships 清单 label 化（与页面/dataset 对齐） |
| scripts/_check_json_copies.py | W770 | 自 archive 恢复：47 副本字节级自检（W563 职责回归） |
| scripts/check_data_drift.js | W770 | 候选解析 v3.1（json 形态优先 tracked 副本 + 裸文件名·覆盖 45→57 页） |
| site/data/json/hardships_81.json | W770 | 部署副本 label 化（与源/页面对齐） |
| site/data/json/project_review.json | W770 | 副本侧重复后缀损坏修复 ×2 |
| scripts/output/data-drift-baseline.txt | W770 | 撤 hardships 3 行豁免（对齐后恢复全量管控） |
| scripts/output/_w770_spec.json | W770 | 本批 spec 入库 |

## W769 动效时长归一与口径说明修正批（2026-10-16）

| 文件 | W | 说明 |
|---|---|---|
| scripts/check_motion_ban.py | W769 | 补 .duration(N) N>600 判据（DESIGN §5.1·count-up 900 白名单） |
| scripts/check_doc_sync.py | W769 | C5 扫描域补统计口径说明.md（装载+夹具同步·自测 18/18） |
| docs/00-导读/统计口径说明.md | W769 | §2 86→87（唯一口径来源自相矛盾修正） |
| site/index.html | W769 | 4 处 86→87 + duration 归一 |
| site/dashboard.html | W769 | 86→87 + duration 归一 |
| site/en/（19 页） | W769 | duration 全部归一 ≤600 |
| DESIGN.md | W769 | 首节 86→87 |
| HANDOVER.md | W769 | V 方向节头 86→87 |
| 新Agent启动Prompt.md | W769 | 可视化页 87（Html=88） |
| scripts/output/_w769_spec.json | W769 | 本批 spec 入库 |

## W768 英文站校验接线批（2026-10-16）

| 文件 | W | 说明 |
|---|---|---|
| scripts/validate_en.py | W768 | --all 批量模式 + SEARCH_INDEX 语料豁免区 + check_page 重构（单页输出逐字节兼容） |
| scripts/verify_delivery.py | W768 | 第 44 槽挂载（段数 48→49·五面注册） |
| Makefile | W768 | validate-en 目标 + ci 链挂载 |
| AGENTS.md | W768 | §4.2 43→44 槽（清单补第 44 项） |
| docs/agent/gates.md | W768 | 44 槽标题 + 第 44 槽全量定义 |
| README.md | W768 | gate_count 标记 43→44 |
| scripts/output/script-coverage-baseline.txt | W768 | 移除 validate_en 豁免行（接线后不再豁免） |
| site/en/chart-design.html | W768 | zh→en 字典 126 对全域转形 |
| site/en/methodology-matrix.html | W768 | 字典 32 对 + 四角标签键值化 |
| site/en/character-appearance.html | W768 | ZH2EN_NAME 35 对转形 |
| site/en/chapter-stats.html | W768 | 第N回→Chapter N ×102 |
| site/en/relationships.html | W768 | 调试串英译 |
| scripts/output/_w768_spec.json | W768 | 本批 spec 入库 |

## W767 数据漂移门禁深比对批（2026-10-16）

| 文件 | W | 说明 |
|---|---|---|
| scripts/check_data_drift.js | W767 | v3 共路深比对（递归共键·数组按位·标量严格比）+声明式基线+no-new-drift |
| scripts/output/data-drift-baseline.txt | W767 | 基线新建（81-hardships 生成器/页面约定分裂 + visual-art 设计双形态·含归因注释） |
| dataset/cave-estate.json | W767 | 中将级→妖将级（第 38 门禁旧值标记清理） |
| dataset/character-relationship-3d.json | W767 | F-7：kpi[4] → 悟空/度数 12（links 度数自证·与 kpi[3]/页嵌同名形） |
| dataset/journey-map-interactive.json | W767 | F-7：kpi[2] 难点 9→8（isHardship 节点实数自证） |
| dataset/language-style-radar.json | W767 | 悟空色 ×2 → #C9A063（现行 palette） |
| dataset/theological-intervention-network.json | W767 | accent-1×5 → accent-2（页内 accent-1 零出现） |
| site/data/81-hardships.html | W767 | 页嵌 cause mind×3 → 人心自生的魔障 + CSP 重注 |
| scripts/output/_w767_spec.json | W767 | 本批 spec 入库 |

## W766 C 类引文静默删改修复批（2026-10-16）

| 文件 | W | 说明 |
|---|---|---|
| docs/01-全书逐回解读/第001回-灵根育孕源流出.md | W766 | C 类引文修复（补回「不得久住天人之内」） |
| docs/02-人物深度分析/（28 件） | W766 | C 类引文静默删改修复（单字/标点/引号/截断/删节五类·含 4 条语料疑点登记） |
| docs/03-主题与情节专题/（13 件） | W766 | C 类引文修复（『』→“”还原·字形/句读/补全·含 4 条语料疑点登记） |
| scripts/output/_w766_spec.json | W766 | 本批 spec 入库 |
| docs/00-导读/W批次编号对账表.md | W766 | W766 认领行登记 |

## W765 a11y 辅助族注释统一与解析规则拆分批（2026-10-16）

| 文件 | W | 说明 |
|---|---|---|
| scripts/a11y_audit.py | W765 | 辅助族注释统一 + rule_29_parsing 拆分（编排器+三检测臂·对拍一致） |
| scripts/output/_w765_spec.json | W765 | 本批 spec 入库 |

## W764 命令白名单 pager 逃逸修复批（2026-10-16）

| 文件 | W | 说明 |
|---|---|---|
| xiyouji-agent-web/server/engine/tools.ts | W764 | 参数层拦截扩展（git pager 族 token 级 + shell 元字符二次校验·W760 S-01 RCE 修复） |
| xiyouji-agent-web/server/engine/tools.test.ts | W764 | +6 例（5 拒 1 放行·-O/=形态/长形态/ext-diff/元字符/正则放行） |
| docs/agent/agent-web.md | W764 | 安全边界描述同步（run_command 参数层拦截 W680→W764 收口） |
| scripts/output/_w764_spec.json | W764 | 本批 spec 入库 |

## W763 照录区字级篡改全量修复批（2026-10-16）

| 文件 | W | 说明 |
|---|---|---|
| docs/01-全书逐回解读/第003回-四海千山皆拱伏.md | W763 | 照录区字级篡改修复 8 处（初江王→楚江王等） |
| docs/01-全书逐回解读/第004回-官封弼马心何足.md | W763 | 照录区修复 2 处（我怕你·领旨） |
| docs/01-全书逐回解读/第006回-观音赴会问原因.md | W763 | 照录区修复 10 处（子叉→木吒 8·神针·嚷处） |
| docs/01-全书逐回解读/第007回-八卦炉中逃大圣.md | W763 | 照录区修复 2 处（斝·即唤阿傩） |
| docs/01-全书逐回解读/第008回-我佛造经传极乐.md | W763 | 照录区修复 58 处（般若/蟠桃/玉帝/迦叶/锡杖/￥→栴等） |
| docs/01-全书逐回解读/第009回-袁守诚妙算无私曲老龙王拙计犯天条.md | W763 | 照录区修复 4 处（登基·巳时×2·冒号） |
| docs/01-全书逐回解读/第010回-二将军宫门镇鬼唐太宗地府还魂.md | W763 | 照录区修复 8 处（崔珏×6·邪祟·奈何） |
| docs/01-全书逐回解读/第068回-朱紫国唐僧论前世孙行者施为三折肱.md | W763 | 照录区修复 2 处（魏征·W756 语料联动） |
| docs/01-全书逐回解读/第091回-金平府元夜观灯玄英洞唐僧供状.md | W763 | 照录区修复 1 处（魏征·W756 语料联动） |
| scripts/output/_w763_spec.json | W763 | 本批 spec 入库 |
| docs/00-导读/W批次编号对账表.md | W763 | W763 认领行登记 |

## W762 W761 重构报告晋升批（2026-10-16）

| 文件 | W | 说明 |
|---|---|---|
| docs/11-方案报告/W761工具链可维护性重构报告-2026-10-16.md | W762 | W761 重构报告晋升入库（V3.0·十节全量） |
| docs/11-方案报告/README.md | W762 | 索引加行+现役 18→19 篇+全表重编号 1-19 |
| STRUCTURE.md | W762 | report_docs 标记 21→22+现役文字 18→19 篇 |
| scripts/output/stats.json | W762 | report_docs 21→22（新报告件入库） |
| docs/00-导读/W批次编号对账表.md | W762 | W762 认领行登记 |
| scripts/output/_w762_spec.json | W762 | 本批 spec 入库 |

## W761 工具链可维护性重构批（2026-10-16）

| 文件 | W | 说明 |
|---|---|---|
| scripts/utils/path_guard.py | W761 | 新建：W536 路径守卫公共模块（make_guard 工厂+双根·收敛 14 处重复定义） |
| scripts/check_content_consistency.py | W761 | l2/l2_runtime 去重+check_page 拆分（峰值 cx 41→19）+js_of→extract_scripts |
| scripts/tmpe_tidy.py | W761 | scan 分类链外提+main 三分派+三处去重+human_size |
| scripts/a11y_audit.py | W761 | 40 项规则族命名统一 rule_N_topic（19 改名+测试 38 同步+注释升级） |
| scripts/inject_rum.py | W761 | P-02 修复：守卫根 SCRIPTS_ROOT→PROJECT_ROOT（同批 inject×3+bump_footer_version） |
| scripts/bump_version.py | W761 | 守卫迁移至 path_guard（仓库根语义·W576 注释精华保留） |
| scripts/fetch_gate_stats.py | W761 | 删除 W536 死定义（零调用点·同批 lint_links/security_scan） |
| tests/unit/test_path_guard.py | W761 | 新建：守卫公共模块 6 例（双根放行/双外拒/消息文本/闭包独立） |
| tests/unit/test_a11y_audit.py | W761 | 同步 a11y 规则族改名（38 处引用） |
| scripts/README.md | W761 | utils 共享模块表补 path_guard 行 |
| docs/00-导读/W批次编号对账表.md | W761 | W761 认领行登记（chore 翻收官） |
| scripts/output/_w761_spec.json | W761 | 本批 spec 入库 |

## W760 全量对抗性审查报告批（2026-10-16）

| 文件 | W | 说明 |
|---|---|---|
| docs/11-方案报告/全量对抗审查报告-2026-10-16.md | W760 | 全量对抗性审查报告（11 发现 4 HIGH+25 证据脚本+正面结论复算） |
| docs/11-方案报告/README.md | W760 | 索引加行+现役 17→18 篇+全表重编号 |
| STRUCTURE.md | W760 | report_docs 标记 20→21+现役文字 17→18 篇 |
| scripts/output/stats.json | W760 | report_docs 20→21（新报告件入库） |
| docs/00-导读/W批次编号对账表.md | W760 | W760 认领行登记（原预留 bullet 转正） |
| scripts/output/_w760_spec.json | W760 | 本批 spec 入库 |

## W759 batch_cascade 脚注滚动根修批（2026-10-16）

| 文件 | W | 说明 |
|---|---|---|
| scripts/batch_cascade.py | W759 | 脚注滚动断言放松为严格递增加指针注记就地刷新（编号空洞兼容根修） |
| scripts/output/_w759_negative_check.py | W759 | 负样本：切分边界重复号夹具断言转红加字节级恢复原状 |
| scripts/output/_w759_spec.json | W759 | 本批 spec 入库 |
| docs/00-导读/W批次编号对账表.md | W759 | W759 认领行登记 |

## W758 CI 首跑暴露缺陷修复批（2026-10-16）

| 文件 | W | 说明 |
|---|---|---|
| tests/unit/test_tmpe_tidy.py | W758 | 盘符断言加 os.name nt 守卫（POSIX splitdrive 恒空串·Linux runner 必红根修） |
| scripts/requirements.txt | W758 | 补 markdown==3.10.2 钉版（build_reader 依赖登记·CI 首跑暴露） |
| scripts/check_seo_head.py | W758 | R5 占位域名检测改左边界负向断言正则（CodeQL 加固） |
| scripts/check_chart_values.js | W758 | stripJsComments 剥离正则加 gi 大小写不敏感（CodeQL 加固） |
| docs/00-导读/W批次编号对账表.md | W758 | W758 认领行登记 |
| scripts/output/_w758_spec.json | W758 | 本批 spec 入库 |
| scripts/output/_w758_rotate.py | W758 | 一次性脚本：手工执行 AGENTS 脚注滚动迁 W749 入 ARCHIVE（编号空洞使级联断言失配的先例处置） |

## W757 CI 门禁接线缺陷修复批（2026-10-16）

| 文件 | W | 说明 |
|---|---|---|
| .github/workflows/ci.yml | W757 | verify-delivery job 补 Playwright（缓存+`npm ci --prefix scripts`+`playwright install`·D1）；agent-web-build job 补 `test:server`（D2） |
| scripts/security_scan.py | W757 | discover_files roots 增 xiyouji-agent-web、exts 增 .ts/.tsx/.mjs、按 gitignore 契约排除 tsc 编译产物（D3） |
| tests/unit/test_ci_wiring.py | W757 | 新增 9 例 CI 接线回归测试（锚 `run:` 块命令体·负样本 4/4 验证） |
| tests/unit/test_security_scan.py | W757 | 补 4 例扫描扩面断言（agent-web 覆盖/TS 扩展名/产物排除/规模下限） |
| scripts/_w757_negative_check.py | W757 | 负样本验证器（逐条摘除接线断言测试必红） |
| docs/11-方案报告/工程基础设施薄弱点审计报告-2026-10-16.md | W757 | 三轮论断对拍 + 四条新发现缺陷 + 修复记录（报告正文） |
| docs/11-方案报告/README.md | W757 | 索引登记（现役报告 16→17 篇） |
| docs/00-导读/W批次编号对账表.md | W757 | W757 认领行登记 |

## W756 人名用字语料纯度批（2026-10-16）

| 文件 | W | 说明 |
|---|---|---|
| source/原文/分回/第068回.md | W756 | 语料纯度：魏徵→魏征 2 处（唐三藏复述引语内·与 json/app 三容器同改） |
| source/原文/分回/第091回.md | W756 | 语料纯度：魏徵→魏征 1 处 |
| source/原文/shendu/SD039.md | W756 | 语料纯度：魏徵→魏征 1 处（分析性文字混入） |
| dataset/text-search.json | W756 | 语料镜像同改 3 处（第 20 门禁语料保真检对拍源） |
| site/static/js/text-search-app.js | W756 | 页面内嵌语料副本同改 3 处（W691 三容器纪律） |
| docs/00-导读/统计口径说明.md | W756 | 新增 §7 人名用字口径（语料/引文强制简体·展示面两态并存·禁批量改展示面） |
| docs/10-方法论沉淀/人名用字两态盘点-魏征-2026-10-11.md | W756 | 处置选项节补执行记录（范围/验证/边界·选项 1 仍待裁决） |
| docs/10-方法论沉淀/README.md | W756 | 索引第 20 行同步（选项 3 已执行） |
| scripts/output/_w756_corpus_fix.py | W756 | 一次性语料改字脚本（先断言后替换·幂等防盲改） |
| docs/00-导读/W批次编号对账表.md | W756 | W756 认领行登记 |
| scripts/output/_w756_spec.json | W756 | 本批 spec 入库 |

## W755 方法论深度篇扩建与治理口径统一批（2026-10-16）

| 文件 | W | 说明 |
|---|---|---|
| docs/10-方法论沉淀/批次交付流水线.md | W755 | 新建·七步交付链 + 编号锚点三形态 + 行尾编码纪律 + 失败模式速查 |
| docs/10-方法论沉淀/治理文档分层与按需查表.md | W755 | 新建·L0-L3 四层职责与体量纪律 + 阅读契约三型 + 第 41 门禁四查 + 数字指针纪律 |
| docs/10-方法论沉淀/可视化数据正确性断言方法论.md | W755 | 新建·真实渲染 + 双签名稳定等待 + 先普查后定阈 + 基线冻结 + 五判据 V1-V5 + 建线六步 |
| docs/10-方法论沉淀/多Agent干扰治理与touches纪律.md | W755 | 新建·N×p×T 暴露面 + 机制三件套 + 登记口径 + 两条边界 + 四批复现案例 |
| docs/10-方法论沉淀/README.md | W755 | 目录索引 20→24 行（新增 21-24·报告指针顺延 25） |
| docs/10-方法论沉淀/Subagent盲信铁律.md | W755 | 「本目录 19 篇主题」改引用式（篇数以目录索引为准·防漂移） |
| docs/00-导读/文档规范.md | W755 | §11.1 新增「辅助·索引」行 + 目录分流规则四则 + touches 块计数表述修正 + 互链新篇 |
| docs/agent/pitfalls.md | W755 | git/提交/并发节计数 8→12（口径=顶层条目数） |
| AGENTS.md | W755 | §4.3 坑位计数 33→38 + 六主题计数 9/5/12/4/4/4 + 口径注 + §7 接手路径第 5 步改指针版 |
| HANDOVER.md | W755 | §三 新增入口契约（经验总入口指针化 + 历史条目存档声明） |
| docs/INDEX.md | W755 | 重建（689 篇/12 板块） |
| scripts/output/stats.json | W755 | methodology_docs 20→24（stats.py --w W755 派生三件） |
| docs/00-导读/W批次编号对账表.md | W755 | W755 认领行登记 |
| scripts/output/_w755_spec.json | W755 | 本批 spec 入库 |

## W754 方法论目录口径整改批（2026-10-16）

| 文件 | W | 说明 |
|---|---|---|
| docs/10-方法论沉淀/README.md | W754 | 索引重写（报告篇数引用式 + 复利总览标 W086 快照 + 协议层节改订 + 维护规则补报告分流/载体铁律 + 13d→16d） |
| docs/10-方法论沉淀/DRL真循环.md | W754 | 上游 skill 失联注记 + 案例表截至 W086 指针 + 手工 Preflight 补现役工具行 + zip 步骤标非现役 |
| docs/10-方法论沉淀/三skill闭环.md | W754 | 三 skill 位置列改指仓内等价载体 + 行号证据不可核验注记 + 补现役级联/核验工具 |
| docs/10-方法论沉淀/E1铁律.md | W754 | 计数自洽（去易漂移总分·以明细表为准）+ commit 不在当前历史注记 + neat-freak 载体退役 + CHANGELOG 指针改归档 |
| docs/10-方法论沉淀/E2文档同步区分历史vs现役.md | W754 | file-index W700+ 边界 + 第 31 门禁机器化补记 + W711 段形态注 + 归档段指向修正 |
| docs/10-方法论沉淀/Preflight与Subagent模板.md | W754 | 三轨语料路径换代（text-search.html → dataset/text-search.json + text-search-app.js）+ 开工侧工具化登记 + 上游路径改指 |
| docs/10-方法论沉淀/Subagent盲信铁律.md | W754 | 上游 skill 失联改指仓内 + 「共 4 篇」标 W235-S1 批次历史值 + 现役目录篇数注 |
| docs/10-方法论沉淀/agent-web技术栈迁移评估.md | W754 | 状态行（迁移 W543-W548 已完成·ignore 已删·现役栈实测）+ 结论反转标注 + 版本回填 + 选项 A 终止 |
| docs/10-方法论沉淀/dispatching-parallel-agents四subagent并行模式.md | W754 | 新增「现役并行纪律」节（touches 交集 + safe_commit）+ 三 skill 兜底改指仓内 |
| docs/10-方法论沉淀/前端显示问题诊断SOP.md | W754 | 门禁对照表补槽号（8/9/10/11）+ 表注（.js 与 .py 两实现 + 三 `_` 脚本降级手动取证）+ 补第 43 槽 |
| docs/10-方法论沉淀/双索引可追溯改造.md | W754 | W700+ 索引边界与 W711 段形态 + 仓外 memory 链接改内链 + §六 维护规则标工具化 + 归档段指向 |
| docs/10-方法论沉淀/可视化测试计划-十七维叙事学图谱.md | W754 | 页面更名 13d→16d 9 处 + 测试真实路径 tests/e2e/ + 行号锚点改键锚 + P2 基线与 KPI 口径提示 + 投稿件路径 |
| docs/10-方法论沉淀/并行Edit竞态问题.md | W754 | 补跨 Agent touches 层（机制未被取代）+ 上游路径改指 + CHANGELOG 段改归档指向 |
| docs/10-方法论沉淀/改动后影响面扫描.md | W754 | 补机制层工具化（batch_cascade 10 面 + 清单 + preflight --touches + lint_links）+ 归档指向修正 |
| docs/10-方法论沉淀/人机创意工作流方法论.md | W754 | backlog 落地状态回填（第 19/43 槽）+ audit 归档路径 + skills 退役 + .github 模板实测 |
| docs/10-方法论沉淀/markdown写作规范.md | W754 | 阅读契约标记例外 + 关联文档补现役写作权威指针（§4.9/§4.10/§6） |
| docs/10-方法论沉淀/白屏三连根因复盘与防回归清单.md | W754 | 改进清单逐条标落点（第 10/11/24/43 槽）+ 唯一未落地项（inline_css 括号校验）+ 页数现状括注 |
| docs/10-方法论沉淀/记忆研究理论框架应用方法论.md | W754 | 七处 line 锚点换代（改回目+引文·第 20 门禁口径）+ §三 定位策略改写 + 九段式行同步 |
| docs/00-导读/W批次编号对账表.md | W754 | W754 认领行登记 |
| scripts/output/_w754_spec.json | W754 | 本批 spec 入库 |

## W753 可视化数据正确性断言批（第 43 门禁）（2026-10-15）

> **递延补登记**：本段由 W754 批依对账表 W753 行补入（原批条目文本按同会话约定后插·CHANGELOG 对应段同批补登记）。

| 文件 | W | 说明 |
|---|---|---|
| scripts/check_chart_values.js | W753 | 第 43 门禁本体（Playwright file:// 真实渲染·五判据 V1-V5·87 页·基线冻结 + fail-closed） |
| scripts/output/chart-values-baseline.txt | W753 | 基线冻结（87 页 × 6 项 = 522 行·只增） |
| scripts/output/chart-values-report.json | W753 | 缺口报告（na 逐页逐条：V3 9 页 / V4 17 页 / V2 1 页） |
| tests/unit/test_visualization_data.py | W753 | 断言器单测 |
| tests/e2e/test_visualization_assertions.js | W753 | E2E 扩面 |

## W752 Web Agent 安全加固批（2026-10-15）

> **递延补登记**：本段由 W754 批依对账表 W752 行补入（同 W753 约定：门禁面归 W751 单写·条目文本后插）。

| 文件 | W | 说明 |
|---|---|---|
| xiyouji-agent-web/server/engine/tools.ts | W752 | 工具面安全加固（安全单测 30 例对应实现面） |
| xiyouji-agent-web/server/engine/tools.test.ts | W752 | tools 安全单测 30 例 |
| xiyouji-agent-web/server/index.ts | W752 | /api/audit 端点接线 |
| xiyouji-agent-web/server/audit.ts | W752 | 写操作持久化审计（audit.jsonl） |
| xiyouji-agent-web/server/audit.test.ts | W752 | 审计单测 |
| xiyouji-agent-web/package.json | W752 | 依赖与脚本同步 |
| xiyouji-agent-web/.env.example | W752 | AGENT_WEB_WRITE_SCOPE 细粒度写入允许域示例 |
| xiyouji-agent-web/README.md | W752 | 安全边界文档同步 |
| docs/agent/agent-web.md | W752 | Web Agent L2 文档同步（安全面） |
| SECURITY.md | W752 | 安全记录同步 |

## W751 根级工具链防护批（第 42 门禁挂载）（2026-10-15）

| 文件 | W | 说明 |
|---|---|---|
| scripts/check_script_coverage.py | W751 | 新增·第 42 门禁根级脚本覆盖（四面引用·基线冻结·self-test 6 例） |
| scripts/output/script-coverage-baseline.txt | W751 | 新增·35 条豁免逐行注明四类理由 |
| scripts/verify_delivery.py | W751 | 挂第 42 槽（段名脚本覆盖·EXPECTED_SECTION_NAMES 47 段） |
| tests/unit/test_new_page.py | W751 | 新增·页面脚手架专项 16 例 |
| tests/unit/test_embed_json.py | W751 | 新增·JSON 嵌入器专项 16 例 |
| tests/unit/test_slice_screenshots.py | W751 | 新增·截图切片器专项 12 例 |
| tests/unit/test_tool_scripts_cli.py | W751 | 新增·根级 import 冒烟层 91 例（3 件显式豁免） |
| tests/unit/test_check_script_coverage.py | W751 | 新增·第 42 门禁自测 10 例（含解析器自伤回归） |
| AGENTS.md | W751 | §4.2 门禁计数 41→42 + 第 42 条摘要 + 阅读契约同步 + 版本脚注 |
| docs/agent/gates.md | W751 | 标题 42 槽 + 速查表 + 第 42 条全量定义 |
| docs/00-导读/文档规范.md | W751 | 门禁体系编号 41→42 |
| README.md | W751 | 门禁数量标记 42<!--stats:gate_count--> + 当前批次抬头 W751 |
| STRUCTURE.md | W751 | 当前批次抬头 W749→W751 |
| docs/00-导读/项目说明.md | W751 | 当前批次行与「当前版本」列表行 W749→W751 |
| HANDOVER.md | W751 | 最后更新链 + 进度节 W751 + 当前 HEAD 句 W751 |
| CITATION.cff | W751 | version W749→W751（W 号区间字面量门禁同步面） |
| .github/workflows/README.md | W751 | 头部版本 + 里程碑上限 W450-W751 + 批次链补 W751 条 |
| scripts/output/stats.json | W751 | gate_count 41→42（stats.py --w W751 派生三件） |
| scripts/output/stats-changelog.json | W751 | gate_count 变更史登记 |
| scripts/output/stats-index.md | W751 | gate_count 反向索引登记 |
| scripts/output/_w751_spec.json | W751 | 本批 spec 入库 |
| scripts/output/_cascade_files_W751.txt | W751 | 手工级联清单（跳号批自建义务·W722 成文） |

## W749 ML 坑族防守补登批（2026-10-15）

| 文件 | W | 说明 |
|---|---|---|
| docs/agent/pitfalls.md | W749 | 运行时节补两条 ML import 坑 + 查坑表补 ML 五查行（计数 3→5） |
| AGENTS.md | W749 | §4.3 坑位计数 31→33 联动 |
| docs/00-导读/W批次编号对账表.md | W749 | W749 认领行登记 |
| scripts/output/_w749_spec.json | W749 | 本批 spec 入库 |

## W748 第40篇复盘入库批（2026-10-15）

| 文件 | W | 说明 |
|---|---|---|
| docs/11-报告复盘/工作复盘与优化分析报告-2026-10-15.md | W748 | 第 40 篇复盘报告入库（十节+附录·双线收官） |
| docs/11-报告复盘/README.md | W748 | 索引加行（新报告编 1·原编号顺延·现役 15→16 篇） |
| STRUCTURE.md | W748 | report_docs 实体标记 16→17+现役文字同步 |
| scripts/output/stats.json | W748 | report_docs 16→17（stats.py --w W748 派生三件） |
| docs/00-导读/W批次编号对账表.md | W748 | W748 认领行登记 |
| scripts/output/_w748_spec.json | W748 | 本批 spec 入库 |

## W747 RAG 系统能力清单入库批（2026-10-15）

| 文件 | W | 说明 |
|---|---|---|
| scripts/rag/README.md | W747 | 扩写「系统能力总览与已知边界」节（四档指标/端点/证伪/边界/分差三层/元模式/资产索引） |
| docs/00-导读/W批次编号对账表.md | W747 | W747 认领行登记（原排序加权批作废·编号改用记录） |
| scripts/output/_w747_spec.json | W747 | 本批 spec 入库 |

## W746 语义页面路由端点批（2026-10-15）

| 文件 | W | 说明 |
|---|---|---|
| scripts/rag/page_router.py | W746 | 新增：语义页面路由（晋升转正·路径参数化+缓存+CLI+21 题评测） |
| scripts/rag/rag_server.py | W746 | /route 懒加载端点 + /health 解绑 BM25 + 主线程预热 |
| tests/unit/test_page_router.py | W746 | 新增：路由纯逻辑单测九例 |
| scripts/rag/README.md | W746 | 语义页面路由节（端点用法+实测+已知边界） |
| .gitignore | W746 | 路由产物忽略（page_vectors/page_index/page_route_eval） |
| docs/00-导读/W批次编号对账表.md | W746 | W746 认领行登记 |
| scripts/output/_w746_spec.json | W746 | 本批 spec 入库 |

## W745 改写智能路由批（2026-10-15）

| 文件 | W | 说明 |
|---|---|---|
| scripts/rag/rag_enhance.py | W745 | 智能路由（should_rewrite 短实体判据·rewrite 档接线） |
| tests/unit/test_rag_enhance.py | W745 | 路由单测扩十二例（共四十五例） |
| scripts/rag/README.md | W745 | rewrite 档行与说明更新（路由后 @5 +0.041 / @10 +0.107） |
| docs/00-导读/W批次编号对账表.md | W745 | W745 认领行登记 |
| scripts/output/_w745_spec.json | W745 | 本批 spec 入库 |

## W744 检索增强集成批（2026-10-15）

| 文件 | W | 说明 |
|---|---|---|
| scripts/rag/rag_enhance.py | W744 | 新增：检索增强引擎（稠密召回+池融合+重排+改写·离线优先加载） |
| scripts/rag/build_vectors.py | W744 | 新增：向量构建（微批安全模式+防混批 manifest+陈旧检测） |
| scripts/rag/xiyouji_rag.py | W744 | RAG_ENHANCE 四档分派（off 零变化·向后兼容） |
| tests/unit/test_rag_enhance.py | W744 | 新增：增强层单测二十九例 |
| scripts/rag/README.md | W744 | 检索增强档节 + LLM_MODEL 示例更正 deepseek-flash |
| scripts/rag/.env.rag.example | W744 | RAG_ENHANCE/RAG_DEVICE 示例同步 |
| .gitignore | W744 | 向量产物忽略（rag_vectors/rag_chunks/rag_embed_meta） |
| docs/00-导读/W批次编号对账表.md | W744 | W744 认领行登记 |
| scripts/output/_w744_spec.json | W744 | 本批 spec 入库 |

## W743 检索融合层消融重构批（2026-10-15）

| 文件 | W | 说明 |
|---|---|---|
| scripts/rag/xiyouji_rag.py | W743 | 融合层消融重构（四路等权 RRF→加权 A+B·移除标题命中/短语位置） |
| tests/unit/test_rag_fusion.py | W743 | 加权 RRF 单测新增四例 |
| docs/superpowers/plans/2026-10-14-interference-governance-roadmap.md | W743 | 干扰日志 §8 追加开工观测行 |
| docs/00-导读/W批次编号对账表.md | W743 | W743 认领行登记 |
| scripts/output/_w743_spec.json | W743 | 本批 spec 入库 |

## W742 复盘落地与引文门禁双向扩展批（2026-10-15）

| 文件 | W | 说明 |
|---|---|---|
| docs/11-报告复盘/工作复盘与优化分析报告-2026-10-14.md | W742 | 第 39 篇复盘报告入库（复盘系列迁移 11 目录首篇·三新族+PRE-25~30+三项裁决回填） |
| docs/11-报告复盘/README.md | W742 | 现役索引 14→15 篇（第 39 篇编 1·原编号顺延） |
| STRUCTURE.md | W742 | report_docs 实体标记 15→16+现役文字同步 |
| scripts/output/stats.json | W742 | report_docs 15→16（stats.py --w W742 派生三件） |
| scripts/check_citations.py | W742 | S-35 反向扫描 --reverse（判据 §4.12 逆向+--fail-on-candidates+self-test 9→12 例） |
| scripts/release_prep.py | W742 | PRE-25 第四检双形态（验证行计数对账+zh_num_to_int 中文数字转换器） |
| tests/unit/test_release_prep.py | W742 | 单测扩至 30 例（转换器 11+对账 7 场景+W737 失真回放） |
| archive/scripts/batches/w7xx/（fix_quotes×4） | W742 | tmpe 晋升归档（用户裁决·SC-02/K-04 落地） |
| archive/README.md | W742 | batches 台账 540→544+tmpe 晋升注记 |
| docs/agent/gates.md | W742 | 第 8 门禁补重建操作规程四连注（PRE-26） |
| docs/00-导读/文档规范.md | W742 | 新增 §4.13 源-产物同修原则（PRE-28） |
| HANDOVER.md | W742 | §九交接流程增第 7 条质量分层声明模板（PRE-30） |
| docs/00-导读/W批次编号对账表.md | W742 | W742 认领行登记（touches 七面申报） |
| docs/01-全书逐回解读/（10 件） | W742 | S-35 反向扫描漏标补【文学演绎】标记（11 节·H1 连载节+聚合子节盲区） |
| site/reader/（622 页） | W742 | PRE-26 四连重建（11 处标记随源生效·CSP 零漂移） |
| scripts/output/_w742_spec.json | W742 | 本批 spec 入库 |

## W741 干扰治理评估固化与 touches 加固批（2026-10-14）

| 文件 | W | 说明 |
|---|---|---|
| docs/11-报告复盘/多Agent干扰治理评估与实施记录-2026-10-14.md | W741 | 评估与实施记录新建（逐类核对/N×p×T/W739 三段/touches 边界加固） |
| docs/11-报告复盘/README.md | W741 | 现役索引 13→14 篇（新报告编 1·原编号顺延） |
| scripts/preflight_check.py | W741 | is_inflight 升级 re.sub 全星号剥离（单星变体防御） |
| tests/unit/test_preflight_check.py | W741 | 回归扩充单星/多星/空白变体（11→12 例） |
| docs/00-导读/W批次编号对账表.md | W741 | W741 认领行登记 |

## W740 干扰治理路线图文档批（2026-10-14）

| 文件 | W | 说明 |
|---|---|---|
| docs/superpowers/plans/2026-10-14-interference-governance-roadmap.md | W740 | 干扰治理路线图新建（决策摘要/总纲/度量前置/P0-P2/不建清单/验收退出/减量周期/四组映射/日志表） |
| docs/00-导读/W批次编号对账表.md | W740 | W740 认领行登记 |

## W739 多 Agent 干扰治理 touches 机制批（2026-10-14）

| 文件 | W | 说明 |
|---|---|---|
| scripts/preflight_check.py | W739 | 第 6 检 touches（rows 解析/在途判定/交集拒绝/--touches --self CLI） |
| tests/unit/test_preflight_check.py | W739 | touches 单测 5→10 例（列解析/向后兼容/在途四态/交集×2） |
| docs/00-导读/W批次编号对账表.md | W739 | touches 列扩容（92 行）+表头规则④+W739 认领行 |
| AGENTS.md | W739 | §4.3 最高频铁则补 touches 条 |
| docs/agent/pitfalls.md | W739 | git/提交/并发节 7→8 条·touches 纪律条目 |
| scripts/README.md | W739 | preflight_check 工具表六检+参数更新 |
| docs/00-导读/文档规范.md | W739 | §11.1 补 touches 说明段（含相对链接修复） |

## W738 tmpe 临时文件体系批（2026-10-14）

| 文件 | W | 说明 |
|---|---|---|
| tmpe/README.md | W738 | tmpe 临时区契约新建（定位/桶约定/保留策略/清理纪律） |
| tmpe/policy.yml | W738 | 策略文件新建（桶/TTL/代际/protect/freeze/tool_promotion·JSON 兼容零依赖） |
| scripts/tmpe_tidy.py | W738 | 策略化治理工具重写（双闸门/journal/undo/锁/优先级链/九维晋升评估） |
| tests/unit/test_tmpe_tidy.py | W738 | 单测 19 例（点名 6 案例+优先级链+roundtrip+锁+评分） |
| .gitignore | W738 | tmpe/* + 文件级例外（体系件入 git·大文件本地） |
| docs/00-导读/W批次编号对账表.md | W738 | W738 认领行登记 |

## W737 对抗性审查修复与报告归置批（2026-10-14）

| 文件 | W | 说明 |
|---|---|---|
| scripts/check_citations.py | W737 | 三检扩展（归属对白核验+演绎豁免+语料保真检+gitignore 分母收敛·self-test 9 例） |
| dataset/text-search.json | W737 | 语料仲裁重建（7 丢段恢复+僻字还原 6+字级对齐 87·100/100 回与分回全等·corpus_note 记裁） |
| source/原文/分回/（12 件） | W737 | 分回 md 同步修正（补丢段/僻字/字级差异·与 json 逐字一致） |
| docs/01-全书逐回解读/（100 件） | W737 | 演绎标记 310 处 + 17 条失实归属对白逐条整改（程序化提取原文） |
| docs/02-人物深度分析/（6 件） | W737 | 外传 3 篇文档级演绎标记 + 深化 2 篇虚构对白整改 + 红蟒精用字修正 |
| docs/03-主题与情节专题/时间的政治学专题.md | W737 | 虚构对白整改（水陆大会场景对齐第 12 回原文） |
| docs/04-文化与历史背景/（2 件） | W737 | 涉台表述修正（版本演变/西游与民间信仰） |
| docs/05-诗词歌赋/原著景物诗赏析专题.md | W737 | 涉台表述修正（出版地补中国台湾） |
| source/引用与网络解读/学术论文索引.md | W737 | 涉台表述修正（台湾故宫博物院→中国台北故宫博物院） |
| docs/11-报告复盘/（新建目录） | W737 | README 索引+13 篇现役报告+读者数据截图 5 件（报告统一归置） |
| docs/10-方法论沉淀/README.md | W737 | 报告类条目迁出重编号（方法论 20+魏征盘点+指针行） |
| docs/00-导读/文档规范.md | W737 | 新增 §4.12 演绎内容标注（标记语义+门禁豁免依据） |
| docs/00-导读/W批次编号对账表.md | W737 | W737 认领行+现势块碑化+陈旧 bullet 清理 10 条+标题校正 |
| docs/agent/gates.md | W737 | 第 20 门禁定义更新（三检口径+豁免区+分母收敛） |
| CITATION.cff | W737 | 五计数刷新+preferred-citation 真 URL+双许可注 |
| README.md | W737 | 目录树补 11-报告复盘 |
| STRUCTURE.md | W737 | 新增 11-报告复盘节（report_docs 实体标记） |
| AGENTS.md | W737 | 目录树+§5.1 make 依赖说明+脚注 W736 措辞校正 |
| HANDOVER.md | W737 | 当前进度/最后更新（级联面） |
| site/index.html | W737 | 字数口径 70.8→70.7 万（实测 706,586 字符） |
| site/data/search.html | W737 | 文档清单路径同步至 11-报告复盘（9 处） |
| site/en/search.html | W737 | 文档清单路径同步至 11-报告复盘（9 处） |
| site/data/chapter-stats.html | W737 | EMBEDDED 重灌（740093→742357·双源复绿+CSP 重哈希） |
| site/reader/（622 页） | W737 | 全链重建（演绎标记/引文整改/涉台修正随源生效） |
| docs/INDEX.md | W737 | 重建（682 篇/12 板块） |
| scripts/output/stats.json | W737 | report_docs 新键+methodology_docs 31→20（stats.py --w W737 派生三件） |

## W736 发布链工具化与文档负载治理批（2026-10-13）

| 文件 | W | 说明 |
|---|---|---|
| scripts/preflight_check.py | W736 | 前置核验器新建（五检+fetch 故障 GitHub API 降级+取号权威源 max+1） |
| scripts/release_prep.py | W736 | 发布预检器新建（spec 三检+消息 W 号核验+文件行 C4-f 镜像+--init 模板） |
| tests/unit/test_preflight_check.py | W736 | preflight 单测（含 porcelain \u0000 分隔解析） |
| tests/unit/test_release_prep.py | W736 | release_prep 单测 17 例组 |
| archive/docs/CHANGELOG-ARCHIVE.md | W736 | W650-W699 段迁入（一级归档·与 file-index 同界 W700） |
| archive/docs/file-index-ARCHIVE.md | W736 | W449-W699 段迁入（与 CHANGELOG 同界） |
| archive/README.md | W736 | 台账 6 行路径前缀与滚动批次同步 |
| scripts/README.md | W736 | 三工具登记（archive_file/preflight_check/release_prep） |
| docs/00-导读/W批次编号对账表.md | W736 | W736 认领行登记 |
| docs/10-方法论沉淀/工作复盘与优化分析报告-2026-10-13.md | W736 | 第 38 篇复盘报告入库（328 行 37KB） |
| docs/10-方法论沉淀/README.md | W736 | 复盘报告索引登记 |
| STRUCTURE.md | W736 | 方法论文档实体标记 30→31 |
| scripts/output/stats.json | W736 | methodology 计数刷新（stats.py --w W736 派生 stats-changelog/stats-index） |

## W735 全仓归档大扫除批（2026-10-13）

| 文件 | W | 说明 |
|---|---|---|
| archive/README.md | W735 | 归档总索引+台账新建（结构树/11 组登记/检索约定） |
| scripts/archive_file.py | W735 | 归档工具新建（git mv 归位+引用扫描+台账登记+dry-run） |
| archive/docs/plans/（28 件） | W735 | docs/superpowers 已完结方案归档（保留 9 件活跃/待办/被引用） |
| archive/docs/specs/（8 件） | W735 | 早期设计稿归档 |
| archive/docs/_dev/（10 件） | W735 | 开发草稿区归档（v07v08/v0.8/2026-10-02 报告组） |
| archive/scripts/attic/（32 件） | W735 | scripts/_attic 整迁 |
| archive/scripts/batches/（540 件） | W735 | 批次一次性产物归档（spec/级联清单/脚本·按 W 段分桶） |
| archive/scripts/review-pass3/（105 件） | W735 | W557 三轮审查产物组级归档 |
| docs/00-导读/文档规范.md | W735 | 设计依据引用同步至 archive 路径 |
| docs/10-方法论沉淀/README.md | W735 | 4 条复盘链接同步至 archive 路径 |
| docs/00-导读/W批次编号对账表.md | W735 | W735 认领行登记 |

## W734 归档体系统一与交接文档更名批（2026-10-13）

| 文件 | W | 说明 |
|---|---|---|
| HANDOVER.md | W734 | 交接文档更名（git mv·全部 live 引用同步） |
| archive/docs/ | W734 | 自 docs/ARCHIVE 迁入（6 归档件+2 子目录·git 改名内容零改动） |
| archive/scripts/ | W734 | 自 scripts/archive 迁入（45 件） |
| archive/scripts/audit/ | W734 | 自 scripts/audit/archive 迁入（10 件） |
| scripts/batch_cascade.py | W734 | handover 面路径与 _arc 同步（HANDOVER.md / archive/docs） |
| scripts/verify_delivery.py | W734 | CORE_DOCS/A4_DOCS/ARCHIVE_DOCS/_DOC_FILES_RE 四组路径同步 |
| docs/00-导读/文档规范.md | W734 | 归档规范重构（archive 根·按类·阈值沿用）+全量引用同步 |

## W733 达标收尾批（2026-10-13）

| 文件 | W | 说明 |
|---|---|---|
| scripts/check_seo_head.py | W733 | main 95→20（五 R 检查函数提取）·输出逐字节验证 |
| scripts/spot_check_nlp.py | W733 | main 93→20（三数据段提取·返回码编排） |
| scripts/check_design_doc_drift.py | W733 | main 89→30（六函数·StrictGate marker 保留）·篡改负样本对拍 |
| scripts/embed_json.py | W733 | main 106→15（四函数·全错误路径退出码保留）·12 场景 CLI 快照 |
| scripts/perf_monitor.py | W733 | compare_trend 88→28（三段提取）·9 场景快照 |
| scripts/build_reader.py | W733 | main 101→40（五函数）·622 文件产物 sha 全等 |
| docs/00-导读/W批次编号对账表.md | W733 | W733 认领行登记 |

## W732 性能与文档工具链重构批（2026-10-13）

| 文件 | W | 说明 |
|---|---|---|
| scripts/perf_optimize.py | W732 | 四长函数拆分（80/72/69/74→58/42/52/31·8 新函数）·fixture 快照+14 单测验证 |
| scripts/optimize-html-size.py | W732 | render_report 126→六段渲染（summary/top10/full/suggestions/strategy/usage）·报告双一致 |
| scripts/sync_docs.py | W732 | main 111→39+_run_checks 七规则表驱动·横幅历史形态逐字节保留·输出逐字节一致 |
| docs/00-导读/W批次编号对账表.md | W732 | W732 认领行登记 |

## W731 发布工具链与安全扫描重构批（2026-10-13）

| 文件 | W | 说明 |
|---|---|---|
| scripts/batch_cascade.py | W731 | main 347→33（十面函数化+_Ctx+_foot_insert/_agents_entry_wn+_apply_pend/_post_check）·dry-run 全量+apply 对拍验证 |
| scripts/security_scan.py | W731 | run 91→42（5 提取）+build_report 81→编排体（_summarize_findings+六段渲染）·单测+报告双一致 |
| docs/00-导读/W批次编号对账表.md | W731 | W731 认领行登记 |

## W730 门禁脚本长函数收尾重构批（2026-10-13）

| 文件 | W | 说明 |
|---|---|---|
| scripts/check_doc_sync.py | W730 | evaluate 177→20（拆 _check_c1..c5d 六检查函数）+gather 提取 _git_output_lines（三块合一） |
| scripts/lint_links.py | W730 | main 125→33（拆 _parse_args/_resolve_scan_dir/_collect_scan_files/_process_file） |
| scripts/perf_monitor.py | W730 | collect_rum_metrics 98→编排体（拆 _try_read_rum/_normalize_rum_events/_bucket_rum_events/_summarize_rum_p75） |
| docs/00-导读/W批次编号对账表.md | W730 | W730 认领行登记 |

## W729 性能与可访问性工具链重构批（2026-10-13）

| 文件 | W | 说明 |
|---|---|---|
| scripts/perf_monitor.py | W729 | build_report/compare_trend/check_budget/run 四长函数拆分（≥80 行 5→2·净 +58 行换 9 函数） |
| scripts/a11y_audit.py | W729 | audit_directory/_render_md 拆分（≥80 行 2→0·净 +48 行换 7 函数） |
| docs/00-导读/W批次编号对账表.md | W729 | W729 认领行登记 |

## W728 门禁与工具链代码重构批（2026-10-13）

| 文件 | W | 说明 |
|---|---|---|
| scripts/verify_delivery.py | W728 | main() 905 行表驱动化：_Reporter/_GateContext/_SimpleGate×18/_StrictGate×15/2 runner/13 段函数 |
| scripts/doc_areas.py | W728 | 新建共享模块：AREA_DIRS 六板块目录+count_content_md 计数口径单一事实源 |
| scripts/sync_docs.py | W728 | 接入 doc_areas（A_AREAS 派生+count_content_md·消除双份手工表） |
| scripts/security_scan.py | W728 | scan_sri script/link 同构块提取 _check_resource_attrs 通用体 |
| docs/superpowers/plans/2026-10-13-code-refactor-w728.md | W728 | 重构方案档（八节·度量基线/符号级设计/风险表/验证协议/经验沉淀） |
| docs/00-导读/W批次编号对账表.md | W728 | W728 认领行登记（含撞号改号事件记录） |

## W727 SVG 保护补打与级联 CRLF 根修批（2026-10-13）

| 文件 | W | 说明 |
|---|---|---|
| scripts/archive/fix_svg_negative_widths.py | W727 | 35 页 clientWidth 保护补打（W726 修复后首跑·radius/attr 类存量已保护 0 命中） |
| scripts/batch_cascade.py | W727 | L176 rfind(nl)+1 → +len(nl（CRLF 工作树 off-by-one 根修·W726 提交内交接文档混行尾损坏源） |
| 交接文档.md | W727 | W726 级联 CRLF 损坏两处字节级修复（裸 CR 补 LF·块尾裸 LF 归规范块间距） |
| site/data/chapter-stats.html | W727 | clientWidth 最小宽度保护补打（200px 下限·CSP 哈希随重注入更新） |
| site/data/chapter-structure-graph.html | W727 | clientWidth 最小宽度保护补打（200px 下限·CSP 哈希随重注入更新） |
| site/data/character-appearance.html | W727 | clientWidth 最小宽度保护补打（200px 下限·CSP 哈希随重注入更新） |
| site/data/character-presence-timeline.html | W727 | clientWidth 最小宽度保护补打（200px 下限·CSP 哈希随重注入更新） |
| site/data/customs-pass-route.html | W727 | clientWidth 最小宽度保护补打（200px 下限·CSP 哈希随重注入更新） |
| site/data/dialogue-sentiment.html | W727 | clientWidth 最小宽度保护补打（200px 下限·CSP 哈希随重注入更新） |
| site/data/emotional-heatmap.html | W727 | clientWidth 最小宽度保护补打（200px 下限·CSP 哈希随重注入更新） |
| site/data/four-dimensional-research-network.html | W727 | clientWidth 最小宽度保护补打（200px 下限·CSP 哈希随重注入更新） |
| site/data/four-heavenly-kings-artifacts.html | W727 | clientWidth 最小宽度保护补打（200px 下限·CSP 哈希随重注入更新） |
| site/data/graph-explorer.html | W727 | clientWidth 最小宽度保护补打（200px 下限·CSP 哈希随重注入更新） |
| site/data/guanyin-six-roles-network.html | W727 | clientWidth 最小宽度保护补打（200px 下限·CSP 哈希随重注入更新） |
| site/data/hardship-difficulty-heatmap.html | W727 | clientWidth 最小宽度保护补打（200px 下限·CSP 哈希随重注入更新） |
| site/data/hardship-heatmap.html | W727 | clientWidth 最小宽度保护补打（200px 下限·CSP 哈希随重注入更新） |
| site/data/heaven-power-network.html | W727 | clientWidth 最小宽度保护补打（200px 下限·CSP 哈希随重注入更新） |
| site/data/intertextuality-network.html | W727 | clientWidth 最小宽度保护补打（200px 下限·CSP 哈希随重注入更新） |
| site/data/journey-map-interactive.html | W727 | clientWidth 最小宽度保护补打（200px 下限·CSP 哈希随重注入更新） |
| site/data/journey-spacetime.html | W727 | clientWidth 最小宽度保护补打（200px 下限·CSP 哈希随重注入更新） |
| site/data/mbti-evolution.html | W727 | clientWidth 最小宽度保护补打（200px 下限·CSP 哈希随重注入更新） |
| site/data/ming-political-thought-comparison.html | W727 | clientWidth 最小宽度保护补打（200px 下限·CSP 哈希随重注入更新） |
| site/data/monster-background.html | W727 | clientWidth 最小宽度保护补打（200px 下限·CSP 哈希随重注入更新） |
| site/data/monster-capability-radar.html | W727 | clientWidth 最小宽度保护补打（200px 下限·CSP 哈希随重注入更新） |
| site/data/monster-ecology-network.html | W727 | clientWidth 最小宽度保护补打（200px 下限·CSP 哈希随重注入更新） |
| site/data/monster-female-network.html | W727 | clientWidth 最小宽度保护补打（200px 下限·CSP 哈希随重注入更新） |
| site/data/monster-hierarchy-network.html | W727 | clientWidth 最小宽度保护补打（200px 下限·CSP 哈希随重注入更新） |
| site/data/monster-victims-network.html | W727 | clientWidth 最小宽度保护补打（200px 下限·CSP 哈希随重注入更新） |
| site/data/narrative-rhythm-curve.html | W727 | clientWidth 最小宽度保护补打（200px 下限·CSP 哈希随重注入更新） |
| site/data/narratology-12d-network.html | W727 | clientWidth 最小宽度保护补打（200px 下限·CSP 哈希随重注入更新） |
| site/data/narratology-16d-network.html | W727 | clientWidth 最小宽度保护补打（200px 下限·CSP 哈希随重注入更新） |
| site/data/pilgrim-team-dynamic-network.html | W727 | clientWidth 最小宽度保护补打（200px 下限·CSP 哈希随重注入更新） |
| site/data/pilgrim-team-psychology-arc.html | W727 | clientWidth 最小宽度保护补打（200px 下限·CSP 哈希随重注入更新） |
| site/data/poetry-rhythm-analysis.html | W727 | clientWidth 最小宽度保护补打（200px 下限·CSP 哈希随重注入更新） |
| site/data/relationships.html | W727 | clientWidth 最小宽度保护补打（200px 下限·CSP 哈希随重注入更新） |
| site/data/six-senses-narratology-network.html | W727 | clientWidth 最小宽度保护补打（200px 下限·CSP 哈希随重注入更新） |
| site/data/theological-intervention-network.html | W727 | clientWidth 最小宽度保护补打（200px 下限·CSP 哈希随重注入更新） |
| site/data/underworld-power-network.html | W727 | clientWidth 最小宽度保护补打（200px 下限·CSP 哈希随重注入更新） |

## W726 本地工具链修复批（2026-10-13）

| 文件 | W | 说明 |
|---|---|---|
| scripts/archive/fix_svg_negative_widths.py | W726 | ROOT 三级上溯根修（W447 搬迁失同步·glob 静默空扫+dashboard 读崩）+站点目录存在性 fail-closed |
| Makefile | W726 | data-validate 空目录跳过保护（output/data gitignore·fresh clone 不再挂 make ci） |
| README.md | W726 | drl-screenshot-review.md 死链改指 CHANGELOG（本地件不入库） |
| source/引用与网络解读/学术论文索引.md | W726 | 11 处死链清理（7×v08 剥链保文·4×S4 改本地存档注记） |

## W725 review 收官 mini 批（2026-10-12）

| 文件 | W | 说明 |
|---|---|---|
| scripts/batch_cascade.py | W725 | S-29 指针滚动注单段化（插前剥旧·防逐批膨胀） |

## W724 页脚链损坏修复与链长治理批（2026-10-12）

| 文件 | W | 说明 |
|---|---|---|
| scripts/batch_cascade.py | W724 | 四页脚双重缺陷根修（去回写+完整节点+12 条裁剪尾注+去重断言·7B 治理落地） |
| site/index.html | W724 | footer-meta 链重建（去重 182·11 条+尾注） |
| site/data/cross-time-danmaku.html | W724 | footer-meta 链重建（去重 127·8 条+尾注） |
| site/data/tag-cloud.html | W724 | footer-meta 链重建（去重 127·8 条+尾注） |
| site/dukou-engine.html | W724 | 页脚链重建（去重 216·11 条+尾注） |

## W723 级联清单反向覆盖根修批（2026-10-12）

| 文件 | W | 说明 |
|---|---|---|
| scripts/check_doc_sync.py | W723 | C4-f 文件清单入库对账（file_list_paths 解析+dirty 双断言+T17/T18·self-test 18 例） |
| scripts/batch_cascade.py | W723 | precheck 强制 body 含「文件」行（数据源源头保证） |
| docs/agent/pitfalls.md | W723 | git 类文件行义务新条+W537③ 更新指向 C4-f |
| docs/00-导读/文档规范.md | W723 | §5 版本段文件行路径形态规范（禁描述列举） |

## W722 八项裁决执行批（2026-10-12）

| 文件 | W | 说明 |
|---|---|---|
| scripts/check_doc_sync.py | W722 | C4-e 级联清单强校验（staged 集合+T15·self-test 15 例） |
| scripts/stats.py | W722 | a4_docs 键（META+build·introduced_by W722） |
| scripts/output/stats.json | W722 | 15 键重生成（a4_docs=209） |
| scripts/output/stats-changelog.json | W722 | W722 变更条（a4_docs 新键） |
| scripts/output/stats-index.md | W722 | 实体卡刷新（a4_docs 行） |
| scripts/verify_delivery.py | W722 | EXPECT_A4 双形态适配（第 3 门禁·正则） |
| docs/00-导读/文档规范.md | W722 | §4.11 扩三节（裁决流程/自查扩面五项/降级重启契约） |
| docs/agent/pitfalls.md | W722 | git 类两条（自建清单义务/多组 add 禁 2>/dev/null） |
| docs/10-方法论沉淀/工作复盘与优化分析报告-2026-10-12.md | W722 | S-26 卡降级状态注（W722 裁决） |
| docs/00-导读/项目说明.md | W722 | A4 计数实体标记化（6A） |
| docs/00-导读/W批次编号对账表.md | W722 | W722 认领+现势递延 |

## W721 复盘增补与脚注滚动根修批（2026-10-12）

| 文件 | W | 说明 |
|---|---|---|
| docs/10-方法论沉淀/工作复盘与优化分析报告-2026-10-12.md | W721 | §十 续弧线增补节（W713-W720 六批·E-09~16/P-14~26/S-29·S-30/FAM 增量/A-06~10）+头部范围更新 |
| scripts/batch_cascade.py | W721 | S-29 脚注滚动内建（AGENTS 面自动迁移+ARCHIVE 第 12 面+指针刷新·断言三重） |
| docs/archive/AGENTS-ARCHIVE.md | W721 | 脚注 W715/W716 条目自动滚动迁入（S-29 首跑） |

## W720 C4 认领行强制批（2026-10-12）

| 文件 | W | 说明 |
|---|---|---|
| scripts/check_doc_sync.py | W720 | C4 认领行强制（表格行与豁免 bullet 细分+T14·self-test 14 例） |
| docs/agent/gates.md | W720 | 第 31 条 C4 描述+14 例 |
| docs/agent/pitfalls.md | W720 | git 类新条目（认领流程五步·W720 强制） |

## W719 review 修复批（2026-10-12）

| 文件 | W | 说明 |
|---|---|---|
| scripts/_s7_w716_spec.json | W719 | 挑刺第十五次级联 spec 考古补库（W714 先例续做） |
| scripts/_s7_w716_msg.txt | W719 | W716 提交信息件补库 |
| scripts/_s7_w717_spec.json | W719 | 页脚根修批级联 spec 补库 |
| scripts/_s7_w717_msg.txt | W719 | W717 提交信息件补库 |
| scripts/_s7_w718_spec.json | W719 | 变更史补正批级联 spec 补库 |
| scripts/_s7_w718_msg.txt | W719 | W718 提交信息件补库 |
| scripts/output/_cascade_files_W714.txt | W719 | 并行会话级联清单漏 add 补库（W649 规则） |
| scripts/output/_cascade_files_W715.txt | W719 | 并行会话级联清单漏 add 补库（W649 规则） |
| scripts/_s7_footnote_trim2_20261012.py | W719 | 脚注滚动迁移一次性件（W708-W714 迁 ARCHIVE·用后保留） |
| docs/archive/AGENTS-ARCHIVE.md | W719 | AGENTS 脚注 W708-W714 段原文迁入 |

## W718 变更史可追踪补正批（2026-10-12）

| 文件 | W | 说明 |
|---|---|---|
| scripts/stats.py | W718 | 变更史 schema v1（migrate_hist 自动迁移+W704 note+entry time）+docstring 分工与建账说明 |
| scripts/output/stats-changelog.json | W718 | v1 形态落盘（_schema/_field_notes/entries·W704 条目考古注） |
| scripts/output/stats.json | W718 | 例行重跑（无变更·_generated 刷新） |
| scripts/check_doc_sync.py | W718 | C5d 挂载（gather 内联 stats --check+evaluate 判定+T13·self-test 13/13） |
| docs/agent/gates.md | W718 | 第 31 条目补 C5d 与 13 例 |

## W717 页脚链头锚定根修批（2026-10-12）

| 文件 | W | 说明 |
|---|---|---|
| scripts/batch_cascade.py | W717 | 四页脚链头锚定根修（<footer> 区首 token 双形态+位置切片·消 replace 歧义） |

## W716 stats 实体化补正批（2026-10-12）

| 文件 | W | 说明 |
|---|---|---|
| scripts/stats.py | W716 | json_count 退役+build 近似注释+_generated 时分秒+index 表头注+META 语义补明 |
| scripts/output/stats.json | W716 | 14 键重生成（json_count 退役·methodology 34）+_generated 带时分 |
| scripts/output/stats-changelog.json | W716 | W716 变更条（methodology 33→34） |
| scripts/output/stats-index.md | W716 | 表头字段语义注+实体卡刷新 |
| STRUCTURE.md | W716 | 输出行去 json_count 标记改本地产物描述+方法论 33→34 |
| scripts/agent_start.py | W716 | 内容口径行删 data json 段 |

## W715 工作复盘报告批（2026-10-11）

| 文件 | W | 说明 |
|---|---|---|
| docs/10-方法论沉淀/工作复盘与优化分析报告-2026-10-12.md | W715 | 新增：第 37 篇复盘（W702-W714 十三批弧线） |
| docs/10-方法论沉淀/README.md | W715 | 索引第 39 行 |
| docs/00-导读/W批次编号对账表.md | W715 | W715 认领 + 现势 W716 |

## W714 停用守卫与考古补库批（2026-10-11）

| 文件 | W | 说明 |
|---|---|---|
| scripts/_s7_fileindex_dedup_20261011.py | W714 | 考古补库（原属 W713 会话·一次性） |
| scripts/_s7_footnote_trim_20261011.py | W714 | 考古补库（原属 W713 会话·一次性） |
| scripts/_s7_w713_msg.txt | W714 | 考古补库（W713 提交信息档） |
| scripts/_s7_w713_spec.json | W714 | 考古补库（W713 级联 spec） |
| scripts/output/_a02_matrix_body.md | W714 | 考古补库（原属 W699 素材） |
| scripts/output/_s23_full_matrix.md | W714 | 考古补库（原属 W699 素材） |
| scripts/output/_cascade_files_W651.txt | W714 | 考古补库（W651 级联清单·漏 add 存量） |
| scripts/output/_cascade_files_W652.txt | W714 | 考古补库（W652 级联清单） |
| scripts/output/_cascade_files_W653.txt | W714 | 考古补库（W653 级联清单） |
| scripts/output/_cascade_files_W654.txt | W714 | 考古补库（W654 级联清单） |
| scripts/output/_cascade_files_W655.txt | W714 | 考古补库（W655 级联清单） |
| scripts/output/_cascade_files_W656.txt | W714 | 考古补库（W656 级联清单） |
| scripts/output/_cascade_files_W657.txt | W714 | 考古补库（W657 级联清单） |
| scripts/output/_cascade_files_W657_pages.txt | W714 | 考古补库（W657 页清单） |
| scripts/output/_cascade_files_W658.txt | W714 | 考古补库（W658 级联清单） |
| scripts/output/_cascade_files_W680.txt | W714 | 考古补库（W680 级联清单） |
| scripts/output/_cascade_files_W698.txt | W714 | 考古补库（W698 级联清单） |
| scripts/output/_cascade_files_W700.txt | W714 | 考古补库（W700 级联清单） |
| scripts/output/_cascade_files_W701.txt | W714 | 考古补库（W701 级联清单） |
| scripts/output/_cascade_files_W702.txt | W714 | 考古补库（W702 级联清单） |
| scripts/output/_cascade_files_W703.txt | W714 | 考古补库（W703 级联清单） |
| scripts/output/_cascade_files_W704.txt | W714 | 考古补库（W704 级联清单） |
| scripts/output/_cascade_files_W705.txt | W714 | 考古补库（W705 级联清单） |
| scripts/output/_cascade_files_W706.txt | W714 | 考古补库（W706 级联清单） |
| scripts/output/_cascade_files_W707.txt | W714 | 考古补库（W707 级联清单） |
| scripts/output/_cascade_files_W708.txt | W714 | 考古补库（W708 级联清单） |
| scripts/output/_cascade_files_W709.txt | W714 | 考古补库（W709 级联清单） |
| scripts/output/_cascade_files_W710.txt | W714 | 考古补库（W710 级联清单） |
| scripts/output/_cascade_files_W711.txt | W714 | 考古补库（W711 级联清单） |
| scripts/output/_cascade_files_W712.txt | W714 | 考古补库（W712 级联清单） |
| scripts/output/_w657_cite_inject.py | W714 | 考古补库（原属 W657） |
| scripts/output/_w657_cons2.txt | W714 | 考古补库（原属 W657） |
| scripts/output/_w657_spec.json | W714 | 考古补库（W657 级联 spec） |
| scripts/output/_w663_t4_shapin.py | W714 | 考古补库（原属 W663 T4） |
| scripts/output/_w672_baseline_head.txt | W714 | 考古补库（W672 基线） |
| scripts/output/_w672_baseline_orphans.txt | W714 | 考古补库（W672 基线） |
| scripts/output/_w672_baseline_semicolons.txt | W714 | 考古补库（W672 基线） |
| scripts/output/_w672_baseline_vars_kpi.txt | W714 | 考古补库（W672 基线） |
| scripts/output/_w676_commit_msg.txt | W714 | 考古补库（W676 提交信息档） |
| scripts/output/_w678_commit_msg.txt | W714 | 考古补库（W678 提交信息档） |
| scripts/output/_w685_cascade_spec.json | W714 | 考古补库（W685 级联 spec） |
| scripts/output/_w691_review_commit_msg.txt | W714 | 考古补库（W691 review 信息档） |
| scripts/output/_w697_archive_msg.txt | W714 | 考古补库（W697 归档信息档） |
| scripts/bump_version.py | W714 | 方案 D 停用守卫（新形态检测 STOP） |
| .gitignore | W714 | _s4_*/_s5_* 降噪（151 件 S4 双盲） |
| docs/00-导读/W批次编号对账表.md | W714 | W714 认领 + 现势 W715 |

## W713 挑刺第十四次补正批（2026-10-11）

| 文件 | W | 说明 |
|---|---|---|
| scripts/batch_cascade.py | W713 | 旋转语义根治（淘汰最老块+pm←剩余最老块+删前断言）+fb/blocks 双形态+title 模板清洗+out2 失配断言+W712 漏提交级联修复补收 |
| scripts/agent_start.py | W713 | 现役解析双形态（实跑曾显示 W710）+阻塞提取锚段标题+TASK_MAP 指 L2 三件 |
| scripts/verify_delivery.py | W713 | _SCOPE_CORE 补 7 内联段（自洽锁盲区闭合）+注释 subprocess 计数校数 35 |
| scripts/check_index_health.py | W713 | 检查5 双形态+governance_refs 子目录扩面（排除 output/ 产物区）+EXEMPT_W 注释补因 |
| scripts/check_governance_docs.py | W713 | 检查5 group(2)/group(3) 对齐+footer docstring 批次键化 |
| scripts/check_w_range_literal.py | W713 | current_state 历史段 W 号 int(None) 隐患修复+None 显示批次键 |
| scripts/check_agents_layers.py | W713 | T3 自测改删 41 注入（4/5→5/5 复活） |
| scripts/check_doc_sync.py | W713 | C5 扫描面补 CONTRIBUTING（自测夹具同步·12/12） |
| AGENTS.md | W713 | 40→41 两处+头部指针改 L2+脚注滚动迁移（保留最近 5 条·早段迁 ARCHIVE） |
| docs/archive/AGENTS-ARCHIVE.md | W713 | AGENTS 脚注早段（W701-W707）原文迁入 |
| docs/agent/gates.md | W713 | 41 槽标题+第 41 槽归组+速查表 4 处补字+615 实体标记+第 7 槽共槽注记 |
| docs/agent/pitfalls.md | W713 | 场景分层铁律条目双标点修复 |
| docs/agent/agent-web.md | W713 | 技术栈 React19/Vite8/TS7（package.json 实证）+引擎层 bullet+README 权威入口 |
| docs/00-导读/项目说明.md | W713 | 当前版本 W711 残留清正（孤儿括号）+86→87 页+阅读契约头部 |
| docs/00-导读/W批次编号对账表.md | W713 | W712 行裁决数对齐 CHANGELOG+版段列清正+翻已收官+W711 行版段补正+W713 认领+现势递延 |
| docs/00-导读/门禁豁免盘点-2026-10-11.md | W713 | 结论先行点名 8 项构成（表 10 行对应） |
| STRUCTURE.md | W713 | 02 段 26→215 篇（磁盘实测 216 含 README） |
| README.md | W713 | 09 目录树补苦难意义论 |
| 交接文档.md | W713 | 头部块引用合并+空行收敛+pm 指针归位（级联追加） |
| scripts/output/file-index.md | W713 | 段标题重复 146 行全量去重（级联追记） |

## W712 方案档挑刺补正批（2026-10-11）

| 文件 | W | 说明 |
|---|---|---|
| docs/superpowers/plans/2026-10-11-agents-layered-restructure.md | W712 | §七执行实录与挑刺补正节+契约头部 |
| docs/superpowers/plans/2026-10-11-version-space-inventory.md | W712 | §七执行状态与挑刺补正节+契约+措辞精确化 |
| CITATION.cff | W712 | version 行补形态注释（CFF free string） |
| docs/00-导读/W批次编号对账表.md | W712 | W712 认领 + 现势 W713 |

## W711 方案D形态改造批（2026-10-11）

| 文件 | W | 说明 |
|---|---|---|
| scripts/check_doc_sync.py | W711 | 四正则双形态+changelog_top (date,wnum)+C1/C2 二元组 |
| scripts/verify_delivery.py | W711 | latest_version 双形态+dukou footer 内联锚+workflows anchor 参数+六文档 ver 条件化 |
| scripts/batch_cascade.py | W711 | 段锚点双形态+新段 W-only+三模板/HEAD/页脚/CITATION/file-index 去 ver |
| tests/test_verify_delivery_version.py | W711 | 补方案 D 两用例（13 过） |
| CHANGELOG.md | W711 | 头部方案 D 切换声明+首个 W-only 新形态段 |
| README.md | W711 | 版本号说明节改方案 D 语义+抬头批次化 |
| docs/00-导读/文档规范.md | W711 | §4.11 方案 D 已实施注记 |
| CITATION.cff | W711 | version=批次号形态 |
| docs/00-导读/W批次编号对账表.md | W711 | W711 认领 + 现势 W712 |

## W710 BL-25与BL-21收口批（2026-10-11·v2.3.304）

| 文件 | W | 说明 |
|---|---|---|
| docs/00-导读/门禁豁免盘点-2026-10-11.md | W710 | 新增：BL-21 首份豁免盘点报告（十项） |
| STRUCTURE.md | W710 | BL-25：02/04 段沿革迁出正文换现数 |
| docs/archive/STRUCTURE-ARCHIVE.md | W710 | 迁入节：02/04 沿革原文 |
| 交接文档.md | W710 | BL-21 关闭 + BL-25 执行记录 |
| docs/00-导读/W批次编号对账表.md | W710 | W710 认领 + 现势 W711 |

## W709 BL-24分层搬迁批（2026-10-11·v2.3.303）

| 文件 | W | 说明 |
|---|---|---|
| docs/agent/gates.md | W709 | 新增：门禁全量 40+41 条五组重排（L2） |
| docs/agent/pitfalls.md | W709 | 新增：坑位 31 条六主题+shell 查坑表（L2） |
| docs/agent/agent-web.md | W709 | 新增：Web Agent 主题（L2） |
| docs/archive/AGENTS-ARCHIVE.md | W709 | 新增：脚注 W458-W700 沿革归档（BL-23） |
| AGENTS.md | W709 | 摘要层重构（§4.2/4.3/4.4+脚注切分） |
| scripts/check_agents_layers.py | W709 | 新增：第 41 门禁 AGENTS 分层完整性（self-test 5） |
| scripts/verify_delivery.py | W709 | 第 41 槽四处同改+自洽锁 46 段 |
| scripts/_w709_migrate.py | W709 | 一次性：搬迁器（守恒断言） |
| scripts/output/stats.json | W709 | gate_count 41（--w W709 记账） |
| docs/00-导读/文档规范.md | W709 | §8 第 41 描述与上限 |
| docs/00-导读/W批次编号对账表.md | W709 | W709 认领 + 现势 W710 |

## W708 全变动对抗复审修复批（2026-10-11·v2.3.302）

| 文件 | W | 说明 |
|---|---|---|
| scripts/batch_cascade.py | W708 | 交接结构三断言前置 pend 落盘前阻断（W708 review ①） |
| docs/00-导读/文档规范.md | W708 | §4.11 盘点引用更新 v2 数字（W708 review ②） |
| scripts/output/_w704_ledger_msg.txt | W708 | 补入库（W704 chore msg 漏 add·review ④） |
| CHANGELOG.md | W708 | W704「22 处」三重失真勘误追记（review ③）+ W708 段 |
| docs/00-导读/W批次编号对账表.md | W708 | W708 认领 + 现势 W709 |

## W707 分层重构先行件与阅读契约批（2026-10-11·v2.3.301）

| 文件 | W | 说明 |
|---|---|---|
| docs/superpowers/plans/2026-10-11-agents-layered-restructure.md | W707 | 新增：AGENTS 分层重构方案档（L0/L1/L2+硬耦合 7 项） |
| scripts/agent_start.py | W707 | --task 改动路径分类清单+全量重写（场景分层铁律自证） |
| scripts/_w707_contracts.py | W707 | 一次性：阅读契约头部注入器（10 份） |
| AGENTS.md | W707 | 头部索引型阅读契约 |
| CHANGELOG.md | W707 | 头部查表型阅读契约 |
| 交接文档.md | W707 | 头部首段型契约 + BL-24/25 登记 |
| STRUCTURE.md | W707 | 头部索引型阅读契约 |
| README.md | W707 | 头部分段型阅读契约 |
| CLAUDE.md | W707 | 头部通读型阅读契约（42→44 行） |
| docs/archive/×4 | W707 | 头部禁读型契约（历史内容零改动） |
| docs/00-导读/W批次编号对账表.md | W707 | W707 认领 + 现势 W708 |

## W706 编号空间盘点与元规则批（2026-10-11·v2.3.300）

| 文件 | W | 说明 |
|---|---|---|
| docs/superpowers/plans/2026-10-11-version-space-inventory.md | W706 | 新增：v 号使用点盘点 v2（8791 处六类+硬耦合 9 项+三决策点） |
| scripts/_w706_vscan.py | W706 | 一次性：v 号扫描器（含 W523 quotePath 修正注记） |
| docs/00-导读/文档规范.md | W706 | 新增 §4.11 编号空间与标识符纪律 |
| AGENTS.md | W706 | §4.3 主题视图+§5.2 层次映射+§8 裁定链 |
| CONTRIBUTING.md | W706 | 权威清单补 CLAUDE.md |
| CHANGELOG.md | W706 | 头部 v/W 双键口径声明 |
| 交接文档.md | W706 | Backlog BL-21 豁免盘点+BL-22 方案 D 预告 |
| docs/00-导读/W批次编号对账表.md | W706 | W706 认领 + 现势 W707 |
| 交接文档.md | W706 | 结构修复（头部清零+段序零一二级序+近 3 批块搬回）+BL-21/22/23 |

## W705 Agent开局状态摘要批（2026-10-11·v2.3.299）

| 文件 | W | 说明 |
|---|---|---|
| scripts/agent_start.py | W705 | 新增：开局状态摘要（实读磁盘防记忆代读·--json） |
| AGENTS.md | W705 | §7 快速上手路径第 0 步挂接 |
| CLAUDE.md | W705 | 接手导航插 agent_start 指令（41/60 行） |
| docs/00-导读/W批次编号对账表.md | W705 | W705 认领 + W702 行首拆分修复 + 现势 W706 |

## W704 数字实体化批（2026-10-11·v2.3.298）

| 文件 | W | 说明 |
|---|---|---|
| scripts/stats.py | W704 | 实体化重写：entity-v1+stats-changelog 自动 diff+stats-index 反向索引 |
| scripts/output/stats.json | W704 | 实体形态 entity-v1（15 键） |
| scripts/output/stats-changelog.json | W704 | 新增：stats 变更史（--w 记批次） |
| scripts/output/stats-index.md | W704 | 新增：数字反向索引（W→stats key） |
| scripts/check_doc_sync.py | W704 | 扩 C5b 标记对账+C5c 裸数字报告（self-test 12 例） |
| scripts/_w704_docsync.py | W704 | 一次性：C5b/C5c 编辑器 |
| scripts/_w704_marks.py | W704 | 一次性：实体标记编辑器（22 处） |
| AGENTS.md | W704 | §1/第 8/26 门禁/make analyze 实体标记 + 第 31 条目 C5b/C5c |
| README.md | W704 | 版本行/可视化入口/门禁数实体标记 |
| STRUCTURE.md | W704 | 版本行/类数/篇数/JSON 实体标记 |
| CHANGELOG.md | W704 | 口径块 10 处实体标记 |
| docs/00-导读/文档规范.md | W704 | §4.10 增补数字实体化与 C5 三层分工 |
| docs/00-导读/W批次编号对账表.md | W704 | W704 认领 + 现势 W705 |

## W703 聚合数字对账门禁批（2026-10-11·v2.3.297）

| 文件 | W | 说明 |
|---|---|---|
| scripts/stats.py | W703 | 新增：聚合数字统计器（15 键磁盘实算·--check 自证） |
| scripts/output/stats.json | W703 | 新增：第 31 门禁 C5 对账基准（tracked） |
| scripts/check_doc_sync.py | W703 | 扩 C5 聚合数字对账（18 式句式表+self-test 10 例） |
| scripts/_w703_docsync.py | W703 | 一次性：C5 编辑器 |
| AGENTS.md | W703 | §4.2 第 31 条目扩 C5 |
| docs/00-导读/文档规范.md | W703 | 新增 §4.10 聚合数字书写规范 |
| docs/00-导读/W批次编号对账表.md | W703 | W703 认领 + 现势 W704 |

## W702 六文档口径清债批（2026-10-11·v2.3.296）

| 文件 | W | 说明 |
|---|---|---|
| CHANGELOG.md | W702 | 头部页数口径块实跑刷新 + v2.3.279/280 四件套补录（W702 标记） |
| README.md | W702 | AI 说明门禁数 26→40 + 版本行空格归一 |
| STRUCTURE.md | W702 | 方法论 6→33 篇 + scripts 34 类全建 + F 行/JSON 实数 + 版本行归一 |
| AGENTS.md | W702 | 第 6/8/26 门禁口径 + §4.2 前言 scope auto + 脚注双分号×4 归一 |
| CLAUDE.md | W702 | 常用命令补 verify --scope auto 轻量档行 |
| CONTRIBUTING.md | W702 | 补 W### 认领对账表入口段 |
| scripts/batch_cascade.py | W702 | 版本行模板去空格×3 + AGENTS 脚注 join 双分号守卫 |
| docs/00-导读/W批次编号对账表.md | W702 | W702 认领 + 现势 W703 |
| scripts/_w702_edits.py | W702 | 一次性：挑刺裁决 26 处编辑器（跑完删除） |

## W701 BL-20动工与S-26工具化批（2026-10-11·v2.3.295）

| 文件 | W | 说明 |
|---|---|---|
| site/static/js/chart-a11y.js | W701 | 新增：图表 aria 摘要层与 tabable 焦点模块（BL-20） |
| scripts/inject_chart_a11y.py | W701 | 新增：a11y 加载器注入器（幂等·--check） |
| scripts/worktree_rehearse.py | W701 | 新增：S-26 worktree 预演器 |
| scripts/_w701_a11y_probe.js | W701 | 一次性：BL-20 验收探针（87 页+焦点抽样） |
| docs/10-方法论沉淀/工作复盘与优化分析报告-2026-10-11.md | W701 | 正文状态同步（三卡已交付/A 项排期确认） |
| 交接文档.md | W701 | Backlog BL-20 行翻已执行 |

## W700 docs全量链接门禁与断链清债批（2026-10-11·v2.3.294）

| 文件 | W | 说明 |
|---|---|---|
| scripts/lint_links.py | W700 | 五改：code 去噪+check-ignore+archive 排除+POSIX 跳过+快照件 |
| scripts/verify_delivery.py | W700 | 第 6 门禁扩域 docs 全量改名 docs链接 |
| .github/workflows/ci.yml | W700 | pages-smoke 更名去残件 |
| docs/03-主题与情节专题 | W700 | 13d→16d 死链修复×4 |
| docs/S2-学术投稿 | W700 | 13d→16d 死链修复×4 |
| docs/10-方法论沉淀 | W700 | skills 去链×7+归档深度×5+决策清单去链 |
