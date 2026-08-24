# xiyouji 文件反向索引

> 与 [CHANGELOG.md](../../CHANGELOG.md) 配套：给定文件，查它被改过几次、每次对应哪个 W 条目。
> W### 编号规则见 CHANGELOG.md 顶部。
> 创建于 2026-07-22（v0.8 双索引改造）
>
> **历史归档**：W031-W087（v2.0.4-v2.0.60）site/data/ 部分已迁移至 [file-index-archive.md](file-index-archive.md)；W422 再归档 W393-W416 段；W511 归档 W417-W448 段 + W449-W463 损坏区尾部清理。本文件仅保留 W449+ 现役索引。
>
> **维护契约**：本索引按 W 追加登记（每文件 1 行 + 一句摘要），历史段禁改；新增/变更文件必须先有 CHANGELOG 对应 W 段再登记（双索引铁律），禁止无 W 段单独登记。

---

## W512 CI 安全批次（2026-08-25·v2.3.111）

| 文件 | W | 说明 |
|---|---|---|
| scripts/security_scan.py | W512 | v2.3.111 修改·pip-audit 子进程 timeout 120→300（消除 DEP-001 超时误报·真实依赖漏洞=0） |

## W511 治理文档健康指标归档（2026-08-25·v2.3.110）

| 文件 | W | 说明 |
|---|---|---|
| CHANGELOG.md | W511 | v2.3.110 修改·W417-W464 段归档（158KB→49KB·235 行）·头部归档标注更新（仅保留 v2.3.83+/W484+）·编号上限 W511 |
| CHANGELOG-ARCHIVE.md | W511 | v2.3.110 修改·追加 W511 归档段（W417-W448）+ 归档段-2（W449-W464）·头部归档时间更新 |
| scripts/output/file-index.md | W511 | v2.3.110 修改·W417-W448 段 + 损坏区清理归档（82KB→35.8KB·335 行）·头部「仅保留 W449+」更新 |
| scripts/output/file-index-archive.md | W511 | v2.3.110 修改·追加 W511 归档段·头部归档时间更新 |
| 交接文档.md | W511 | v2.3.110 修改·里程碑概要保留最近 5 版（W506-W510）·W505 及更早归档·概要 408→19 行 |
| 交接文档-archive.md | W511 | v2.3.110 修改·追加 W511 里程碑概要归档段·头部扩容说明更新 |
| scripts/_w511_archive.py 等 3 个 | W511 | v2.3.110 新增·归档批次脚本（CHANGELOG/file-index/交接文档 三档瘦身） |

## W510 治理文档修复（2026-08-25·v2.3.109）

| 文件 | W | 说明 |
|---|---|---|
| docs/00-导读/文档规范.md | W510 | v2.3.109 修改·§8 门禁数 17→20（补 W501-503 三项）+ §11.4 第 9 项「核心 6 文档」→「核心 2 硬+辅助 4 WARN」口径统一；健康指标超标登记待办 |
| CHANGELOG.md / 交接文档.md / README.md / STRUCTURE.md / 项目说明.md / file-index.md | W510 | v2.3.109 修改·六文档同步（编号上限 W001-W510） |

## W509 经验上移共享（2026-08-25·v2.3.108）

| 文件 | W | 说明 |
|---|---|---|
| AGENTS.md | W509 | v2.3.108 修改·§4.3 工具链新增 3 条强制规则（Set-Content BOM 禁/同文件 Edit 串行/引文探针+canonical 预查）+ §6 铁律新增第 13 条内容可信度轨 |
| 交接文档.md | W509 | v2.3.108 修改·「三、方法论沉淀」登记 W505-508 四类规则 + W507-508 上移机制方法论 |
| CHANGELOG.md / 交接文档.md / README.md / STRUCTURE.md / 项目说明.md / file-index.md | W509 | v2.3.108 修改·六文档同步（编号上限 W001-W509） |

## W508 复盘剩余项收口（2026-08-25·v2.3.107）

| 文件 | W | 说明 |
|---|---|---|
| scripts/_check_pipeline_consistency.py | W508 | v2.3.107 新增·管线一致性轻量校验（P3-7：C1 管线标记/C2 生成来源须 创意三明治管线@/C3 引文 ≥3·不入库门禁） |
| skills/xiyouji-character-content/SKILL.md | W508 | v2.3.107 修改·Step 4 新增第 7 步管线一致性检查（--file 模式） |
| skills/xiyouji-character-content/references/creative-methods.md | W508 | v2.3.107 修改·方法四去重为速查摘要+指向 SKILL 管线章节为协议单一事实源（修数字漂移 50→≥20） |
| CHANGELOG.md / 交接文档.md / README.md / STRUCTURE.md / 项目说明.md / file-index.md | W508 | v2.3.107 修改·六文档同步（编号上限 W001-W508） |

## W507 复盘沉淀落地（2026-08-25·v2.3.106）

| 文件 | W | 说明 |
|---|---|---|
| scripts/_cite_probe.py | W507 | v2.3.106 新增·引文候选提取探针（E-A 沉淀永久化：--kw/--chap/--min-len/--max-len/--frag·写引文前从 text-search.json 提取候选·禁凭记忆编造） |
| skills/xiyouji-day-review/SKILL.md | W507 | v2.3.106 修改·步骤 4 新增第 6 项「归档/删除脚本查 tests/ 引用」（W506 教训固化） |
| skills/xiyouji-character-content/SKILL.md | W507 | v2.3.106 修改·深化专题步补引文探针工具引用（写引文前先跑 _cite_probe.py） |
| CHANGELOG.md / 交接文档.md / README.md / STRUCTURE.md / 项目说明.md / file-index.md | W507 | v2.3.106 修改·六文档同步（编号上限 W001-W507） |

## W506 处置遗留（2026-08-25·v2.3.105）

| 文件 | W | 说明 |
|---|---|---|
| tests/test_fix_svg_negative_widths.py | W506 | v2.3.105 删除·W447 归档 fix_svg_negative_widths.py 时漏删的配套测试（引用已归档模块致 pytest 收集失败）；脚本仍在 scripts/archive/ 可追溯 |
| CHANGELOG.md / 交接文档.md / README.md / STRUCTURE.md / 项目说明.md / file-index.md | W506 | v2.3.105 修改·六文档同步（编号上限 W001-W506） |

## W505 创意流程闭环落地（2026-08-25·v2.3.104）

| 文件 | W | 说明 |
|---|---|---|
| skills/xiyouji-character-content/SKILL.md | W505 | v2.3.104 修改·新增「创意三明治管线」章节（四步固定流程·显式触发·生成来源记 创意三明治管线@commit） |
| docs/02-人物深度分析/菩提祖师-方向二深化.md | W505 | v2.3.104 新增·创意三明治管线试点（种子：师父与逐出+算无遗策+心学隐喻·3 条引文 100% 命中·核验状态 引文已核验） |
| docs/02-人物深度分析/黑熊精-方向二深化.md | W505 | v2.3.104 新增·创意三明治管线试点（种子：被招安+品味+守山后半生·3 条引文 100% 命中·核验状态 引文已核验） |
| docs/02-人物深度分析/金角银角-方向二深化.md | W505 | v2.3.104 新增·创意三明治管线试点（种子：烧火童子出差+五件套悖论+职场关系学·3 条引文 100% 命中·核验状态 引文已核验） |
| docs/02-人物深度分析/高翠兰-方向二深化.md | W505 | v2.3.104 新增·创意三明治管线试点（种子：沉默翠兰+婚姻经济学+三次回家·3 条引文 100% 命中·核验状态 引文已核验） |
| docs/10-方法论沉淀/README.md | W505 | v2.3.104 核验·2 篇方法论文档索引已含（W499 暂存版，双向覆盖核验跳过） |
| CHANGELOG.md / 交接文档.md / README.md / STRUCTURE.md / 项目说明.md / file-index.md | W505 | v2.3.104 修改·六文档同步（编号上限 W001-W505·A1-A6 计数 611→615） |

## W503 原著引文硬验证（2026-08-24·v2.3.102）

| 文件 | W | 说明 |
|---|---|---|
| scripts/check_citations.py | W503 | v2.3.102 新增·第 20 门禁（原文引文行对 text-search.json 精确子串命中·去空白归一·--file/--dir 模式·越界/空引文/非全角引号均报错） |
| scripts/verify_delivery.py | W503 | v2.3.102 修改·挂载第 20 门禁原著引文核验（--dir docs 全量） |
| docs/00-导读/文档规范.md | W503 | v2.3.102 修改·§4.8 原著引文语法新立 + §4.6 核验状态引用补实脚本路径 |
| skills/xiyouji-character-content/SKILL.md | W503 | v2.3.102 修改·深化专题硬规则 ≥3 条引文行 + Step 4 引文核验步 |
| skills/xiyouji-s4-submission/SKILL.md | W503 | v2.3.102 修改·阶段 2 补 check_citations.py 调用说明 |
| site/dukou-engine.html | W503 | v2.3.102 修改·长链页脚 prepend W503 条目 |
| CHANGELOG.md / 交接文档.md / README.md / STRUCTURE.md / 项目说明.md / file-index.md | W503 | v2.3.102 修改·六文档同步（编号上限 W001-W503） |

## W502 术语一致性门禁（2026-08-24·v2.3.101）

| 文件 | W | 说明 |
|---|---|---|
| scripts/check_glossary.py | W502 | v2.3.101 新增·第 19 门禁（C1 术语表↔json 双向同步 + C2 称谓组规范词锚定·传递归一·复合词掩码·--generate/--build-baseline/--file 模式） |
| dataset/glossary.json | W502 | v2.3.101 新增·机器可读术语库（6 组 59 条目·--generate 解析生成·禁手改） |
| scripts/output/glossary-baseline.txt | W502 | v2.3.101 新增·存量违规基线（303 篇 383 条·2026-08-24 实测冻结） |
| scripts/verify_delivery.py | W502 | v2.3.101 修改·挂载第 19 门禁术语一致性 |
| docs/00-导读/文档规范.md | W502 | v2.3.101 修改·§4.7 术语一致性新立（单一事实源/C1/C2/基线豁免/已知局限） |
| site/dukou-engine.html | W502 | v2.3.101 修改·长链页脚 prepend W502 条目 |
| CHANGELOG.md / 交接文档.md / README.md / STRUCTURE.md / 项目说明.md / file-index.md | W502 | v2.3.101 修改·六文档同步（编号上限 W001-W502） |

## W501 元信息块 v2（2026-08-24·v2.3.100）

| 文件 | W | 说明 |
|---|---|---|
| scripts/check_frontmatter.py | W501 | v2.3.100 新增·第 18 门禁（新文件血缘+核验状态 4 字段：生成来源/生成模型/生成日期/核验状态三值·基线豁免） |
| scripts/output/frontmatter-baseline.txt | W501 | v2.3.100 新增·存量 611 篇豁免清单（docs/01-06 冻结基线） |
| scripts/verify_delivery.py | W501 | v2.3.100 修改·挂载第 18 门禁元信息块 v2 |
| docs/00-导读/文档规范.md | W501 | v2.3.100 修改·§4.6 元信息块 v2 新立（4 字段枚举口径 + 空真防护 + 门禁挂载说明） |
| skills/xiyouji-character-content/SKILL.md | W501 | v2.3.100 修改·Step 2 追加 v2 血缘 4 字段必填模板 |
| docs/superpowers/plans/2026-08-24-content-trust-provenance-w501-w505.md | W501 | v2.3.100 新增·《内容可信度与溯源体系》方案（W501-W505 路线图·含口径修正 109→105） |
| site/dukou-engine.html | W501 | v2.3.100 修改·长链页脚 prepend W501 条目 |
| CHANGELOG.md / 交接文档.md / README.md / STRUCTURE.md / 项目说明.md / file-index.md | W501 | v2.3.100 修改·六文档同步（编号上限 W001-W501） |

## W500 索引健康门禁（2026-08-24·v2.3.99）

| 文件 | W | 说明 |
|---|---|---|
| scripts/check_index_health.py | W500 | v2.3.99 新增·第 17 门禁（file-index 段完整性/唯一性/最新段残留 + 方法论 README 双向覆盖 + CHANGELOG 编号上限）·豁免 W449-W463 损坏区 |
| scripts/verify_delivery.py | W500 | v2.3.99 修改·挂载第 17 门禁索引健康 |
| scripts/bump_version.py | W500 | v2.3.99 修改·bump_version_line 扩展支持 `- **当前版本**：` 次级行（仅换版本号不追加 W） |
| CHANGELOG.md / 交接文档.md / README.md / STRUCTURE.md / 项目说明.md / file-index.md | W500 | v2.3.99 修改·六文档同步（编号上限 W001-W500） |
| AGENTS.md | W500 | v2.3.99 修改·§4.2 补录第 17 门禁正文 + 版本脚注同步 |
| docs/00-导读/文档规范.md | W500 | v2.3.99 修改·§7/§8/§11 与 17 门禁同步（file-index 行门禁列·17 门禁表·禁改清单补两脚本·bump W500 增强·行号 45→47） |
| skills/xiyouji-day-review/SKILL.md | W500 | v2.3.99 修改·步骤 4 补治理文档内容引用核验 + 陷阱第 8 条 + 验证清单五项（已同步全局版） |
| .github/workflows/README.md | W500 | v2.3.99 修改·旁文档同步（头部版本 W449→W500·W450-W500 里程碑行·Job 8 17 门禁说明·§8 双索引更新） |

## W499 GitHub 协作模板 + 创意方法论沉淀（2026-08-24·v2.3.98）

| 文件 | W | 说明 |
|---|---|---|
| .github/ISSUE_TEMPLATE/bug_report.md | W499 | v2.3.98 新建·bug 报告模板 |
| .github/ISSUE_TEMPLATE/config.yml | W499 | v2.3.98 新建·issue 模板配置 |
| .github/ISSUE_TEMPLATE/feature_request.md | W499 | v2.3.98 新建·功能请求模板 |
| .github/ISSUE_TEMPLATE/question.md | W499 | v2.3.98 新建·提问模板 |
| .github/PULL_REQUEST_TEMPLATE.md | W499 | v2.3.98 新建·PR 模板 |
| docs/10-方法论沉淀/创意三明治工作流.md | W499 | v2.3.98 新建·AI 发散→人类收敛→AI 补全→人类裁决四层交替 |
| docs/10-方法论沉淀/人机创意工作流方法论.md | W499 | v2.3.98 新建·反向约束/跨时空嫁接/幻觉驱动四层创意飞轮 + backlog 备忘 |
| docs/10-方法论沉淀/README.md | W499 | v2.3.98 修改·索引补登 8 个存量 + 修正 2 条待创建 + 关联文档版本刷新 |
| skills/xiyouji-character-content/SKILL.md | W499 | v2.3.98 修改·补创意方法引用（外传/方向二/随笔可选） |
| skills/xiyouji-character-content/references/creative-methods.md | W499 | v2.3.98 新建·四层创意方法速查（提示词模板 + 红线） |
| scripts/output/file-index.md | W499 | v2.3.98 修改·W498 段内补维护注记（W449-W463 结构问题·查历史以 CHANGELOG 为准） |
| CHANGELOG.md / 交接文档.md / README.md / STRUCTURE.md / 项目说明.md / file-index.md | W499 | v2.3.98 修改·六文档同步 |

## W498 防漂移门禁（2026-08-24·v2.3.97）

| 文件 | W | 说明 |
|---|---|---|
| scripts/check_skills_index.py | W498 | v2.3.97 新增·Skills 索引一致性门禁（目录==README==AGENTS §4.5 + 全文件 git tracked + name==目录名）·挂 verify_delivery 第 16 门禁 |
| scripts/sync_skills.py | W498 | v2.3.97 新增·本地同步工具（--check 漂移清单 / --sync 仓库→全局，不入 CI） |
| scripts/verify_delivery.py | W498 | v2.3.97 修改·挂载第 16 门禁 Skills 索引一致性 |
| skills/xiyouji-plan-authoring/.skill-metadata.yaml | W498 | v2.3.97 修改·全局版回拷（含 §10 三段式表述，统一仓库为真源） |
| skills/xiyouji-version-bump/SKILL.md | W498 | v2.3.97 修改·第 8 步补 sync_skills.py --sync + check_skills_index 必跑 |
| AGENTS.md | W498 | v2.3.97 修改·§4.2 补录第 16 门禁 + 脚注 |
| site/dukou-engine.html | W498 | v2.3.97 修改·footer 版本链 prepend v2.3.97 W498 |
| CHANGELOG.md / 交接文档.md / README.md / STRUCTURE.md / 项目说明.md / file-index.md | W498 | v2.3.97 修改·六文档同步 |

> **维护注记（2026-08-24 全面审查）**：本文件 W449-W463 区间存在历史遗留结构问题——W457/W458/W461/W462/W463 段登记内容缺失（空表格）、W451/W452/W453/W460 空壳重复段、W454/W455 乱序、尾部残留 v2.3.65-v2.3.78 旧版本快照行。经审查确认**维持现状不重排**（历史段禁改），该区间查历史变更一律以 [CHANGELOG.md](../../CHANGELOG.md) 为准。

## W497 skills 治理同步（2026-08-24·v2.3.96）

| 文件 | W | 说明 |
|---|---|---|
| skills/xiyouji-visual-batch/SKILL.md | W497 | v2.3.96 同步全局版 v1.2.0（W478 脚本迁移六规则 + W488 可感知验收/暗色夜读 + M-A1 ≥1%） |
| skills/xiyouji-visual-batch/reference.md | W497 | v2.3.96 同步全局版 v1.2.0 |
| skills/xiyouji-plan-authoring/SKILL.md | W497 | v2.3.96 同步全局版 v1.1.0（验收三段式/派生命令/裁掉项/§10 落地回写） |
| skills/xiyouji-plan-authoring/reference.md | W497 | v2.3.96 同步全局版 v1.1.0 |
| skills/xiyouji-day-review/（3 文件） | W497 | v2.3.96 新增入库（SKILL.md + reference.md + .skill-metadata.yaml·此前从未 git add） |
| skills/xiyouji-characters-knowledge/SKILL.md | W497 | v2.3.96 修改·全文检索入口 text-search.html（语料已迁出）→ dataset/text-search.json |
| skills/xiyouji-version-bump/SKILL.md | W497 | v2.3.96 修改·新增第 8 步收尾三同步（AGENTS 脚注/路线图/方案档§10）·流程改九步·v1.1.0 |
| skills/agent-session-loop/SKILL.md | W497 | v2.3.96 修改·补子代理不可用降级声明 |
| skills/deep-review-loop/SKILL.md | W497 | v2.3.96 修改·补子代理不可用降级声明 + 闭环单一事实源护栏 |
| skills/mem-wrap-up/SKILL.md | W497 | v2.3.96 修改·补子代理不可用降级声明 + 闭环单一事实源护栏 |
| skills/self-evolution/SKILL.md | W497 | v2.3.96 修改·补子代理不可用声明 + 闭环单一事实源护栏 |
| AGENTS.md | W497 | v2.3.96 修改·§4.5 流程类补录 day-review（总数 18）+ 版本脚注 |
| skills/README.md | W497 | v2.3.96 修改·索引补 day-review 行·标题 17→18·治理注释补 W497 |
| site/dukou-engine.html | W497 | v2.3.96 修改·footer 版本链 prepend v2.3.96 W497 |
| CHANGELOG.md / 交接文档.md / README.md / STRUCTURE.md / 项目说明.md / file-index.md | W497 | v2.3.96 修改·六文档同步 |

## W496 优化收尾（2026-08-22·v2.3.95）

| 文件 | W | 说明 |
|---|---|---|
| site/js/theme-init.js | W496 | v2.3.95 修改·无 .theme-toggle 页注入夜读浮动切换钮（225 页生效·根页跳过·零 CSP 改动） |
| tests/e2e/test_smoke.js | W496 | v2.3.95 修改·检查 6 样式生效断言（html/body 背景不得同时透明） |
| scripts/acceptance_snapshot.py | W496 | v2.3.95 新增·验收数字当批现测速览（M5/M2M3/M4/M1/断点五组） |
| AGENTS.md | W496 | v2.3.95 修改·§4.3 验收数字禁跨批复制铁律 |
| docs/00-导读/V2可视化维度方案.md | W496 | v2.3.95 修改·fps 遗留实测关闭回写（落地状态表+验收清单） |
| CHANGELOG.md / 交接文档.md / README.md / STRUCTURE.md / 项目说明.md / file-index.md | W496 | v2.3.95 修改·六文档同步 |

## W495 P0 热修复（2026-08-22·v2.3.94）

| 文件 | W | 说明 |
|---|---|---|
| site/data/*.html + site/en/*.html 225 页 | W495 | v2.3.94 修改·INLINED CSS 块恢复（W493 误清空·--force 重同步 30659B） |
| scripts/inline_css.py | W495 | v2.3.94 修改·修 --force 的 skip-no-link 短路缺陷（已内联页可重同步） |
| scripts/check_inlined_css.py | W495 | v2.3.94 新增·第 15 门禁（INLINED 块 ≥20KB 断言·负样本自测过） |
| scripts/verify_delivery.py | W495 | v2.3.94 修改·挂载 INLINED CSS 门禁 |
| scripts/baseline_snapshot.py + scripts/output/观测基线快照.md | W495 | v2.3.94 补入库（W464 宣称入库但从未提交·M6 证据链修复） |
| docs/superpowers/plans/2026-08-22-phase-e-{e3,e4,e5,e6,w494}*.md 5 份 | W495 | v2.3.94 修改·落地状态段 + commit 回填 + 证据作废注记 |
| CHANGELOG.md / 交接文档.md / README.md / STRUCTURE.md / 项目说明.md / file-index.md | W495 | v2.3.94 修改·六文档同步 |

## W494 Phase E 遗留收尾（2026-08-22·v2.3.93）

| 文件 | W | 说明 |
|---|---|---|
| site/*.html + data/*.html + en/*.html（全站） | W494 | v2.3.93 修改·断点映射 380 处 + tag-cloud/81-hardships 溢出修复 + CSP 重跑 |
| site/system.css | W494 | v2.3.93 修改·图表 ≤640px 降级段（图例纵排/轴文字/tooltip 收窄） |
| docs/superpowers/plans/2026-08-22-phase-e-w494-legacy-closure.md | W494 | v2.3.93 新增·遗留收尾批次记录（字体切片关闭根因） |
| CHANGELOG.md / 交接文档.md / README.md / STRUCTURE.md / 项目说明.md / file-index.md | W494 | v2.3.93 修改·六文档同步 |

## W493 Phase E6 验收收口（2026-08-22·v2.3.92）

| 文件 | W | 说明 |
|---|---|---|
| scripts/check_token_coverage.py | W493 | v2.3.92 新增·M2/M3 门禁（私有块 UI 裸色=0/豁免≤N + 真裸 box-shadow=0） |
| scripts/check_motion_ban.py | W493 | v2.3.92 新增·D4 动效禁止清单门禁 |
| scripts/verify_delivery.py | W493 | v2.3.92 修改·挂载 token/动效/a11y 三门禁 |
| site/*.html 93 页（data/en/根） | W493 | v2.3.92 修改·e-track-exempt 豁免登记（新增 6+更新 84）+ 色值/阴影映射修复 |
| site/data/criticism-history.html + en 同名 + concept-device ×2 | W493 | v2.3.92 修改·10 处 infinite 动画改一次性 |
| docs/superpowers/plans/2026-08-22-phase-e-e6-closure-report.md | W493 | v2.3.92 新增·Phase E 收口报告（M1-M7 + 遗留项） |
| CHANGELOG.md / 交接文档.md / README.md / STRUCTURE.md / 项目说明.md / file-index.md | W493 | v2.3.92 修改·六文档同步 |

## W492 Phase E5 响应式+微交互（2026-08-22·v2.3.91）

| 文件 | W | 说明 |
|---|---|---|
| site/system.css | W492 | v2.3.91 修改·导航抽屉组件（.nav-toggle/.nav-mask/≤768 滑出面板 display:none 关闭态） |
| site/index.html / dashboard.html / curated.html / guide.html | W492 | v2.3.91 修改·汉堡按钮 + 遮罩 + 抽屉 JS（双 rAF）；dashboard 补 system.css link |
| docs/superpowers/plans/2026-08-22-phase-e-e5-batch-record.md | W492 | v2.3.91 新增·E5 批次记录（推迟项显式化） |
| CHANGELOG.md / 交接文档.md / README.md / STRUCTURE.md / 项目说明.md / file-index.md | W492 | v2.3.91 修改·六文档同步 |

## W491 Phase E4 EN 站同步（2026-08-22·v2.3.90）

| 文件 | W | 说明 |
|---|---|---|
| site/en/*.html（85 页）| W491 | v2.3.90 修改·EN 同名可视化页六规则令牌化（CN 86 减 journey-geo-3d） |
| docs/superpowers/plans/2026-08-22-phase-e-e4-batch-record.md | W491 | v2.3.90 新增·E4 批次记录（85 页迁移清单表） |
| docs/superpowers/plans/2026-08-18-phase-e-visual-elevation-roadmap.md | W491 | v2.3.90 修改·E4 段 ✅ 回写 |
| CHANGELOG.md / 交接文档.md / README.md / STRUCTURE.md / 项目说明.md / file-index.md | W491 | v2.3.90 修改·六文档同步 |

## W490 Phase E3 CN 可视化页传播 II（2026-08-22·v2.3.89）

| 文件 | W | 说明 |
|---|---|---|
| site/data/*.html（30 页）| W490 | v2.3.89 修改·E3 令牌化（86−E2 56 余量）：R-SHADOW/R-RADIUS/R-TRANS/裸色白名单/R-EXEMPT 六规则；3D 2 页仅 UI 层 |
| docs/superpowers/plans/2026-08-22-phase-e-e3-batch-record.md | W490 | v2.3.89 新增·E3 批次记录（30 页迁移清单表） |
| docs/superpowers/plans/2026-08-18-phase-e-visual-elevation-roadmap.md | W490 | v2.3.89 修改·E3 段 ✅ 回写 + §10 表格 + 基线行 |
| CHANGELOG.md / 交接文档.md / README.md / STRUCTURE.md / 项目说明.md / file-index.md | W490 | v2.3.89 修改·六文档同步 |

## W489 全站暗色模式（2026-08-22·v2.3.88）

| 文件 | W | 说明 |
|---|---|---|
| site/tokens.css | W489 | v2.3.88 修改·dark 令牌组全局化（html[data-theme] 覆盖 15 组变量 + 深色 elev + SVG 数据色提亮 filter）+1494B |
| site/js/theme-init.js | W489 | v2.3.88 新增·全站 theme 初始化（xy-theme→data-theme·同步防 FOUC·fail-open） |
| site/*.html（根 9）| W489 | v2.3.88 修改·head 插 theme-init 引用（诊断 2 页豁免）；5 根页删内联 dark 通用令牌块 -1170B/页 |
| site/data/*.html（86）| W489 | v2.3.88 修改·head 插 theme-init + inline_css --force 重新内联（dark 令牌 + hover 升级传播） |
| site/en/*.html（138）| W489 | v2.3.88 修改·head 插 theme-init + inline_css --force 重新内联（EN 全获 dark UI 适配） |
| CHANGELOG.md / 交接文档.md / README.md / STRUCTURE.md / 项目说明.md / file-index.md | W489 | v2.3.88 修改·六文档同步 |

## W488 根页视觉重设计 + 夜读模式（2026-08-22·v2.3.87）

| 文件 | W | 说明 |
|---|---|---|
| site/system.css | W488 | v2.3.87 修改·.card/.kpi hover 升级（-3px + 朱砂外描边 40%）+ 导航指示条（::after scaleX 滑动，含 nav-strong/aria-current）+644B |
| site/index.html | W488 | v2.3.87 修改·hero "100" 朱砂强调 + 夜读按钮 + dark 内联覆盖 + 防 FOUC + reveal + 交互 JS |
| site/dashboard.html | W488 | v2.3.87 修改·标题/KPI 数字朱砂 + 表头淡朱砂 + route-strip 朱砂线 + KPI 圆角 2→6 + 夜读 + 环图 dark 提亮 |
| site/curated.html | W488 | v2.3.87 修改·卡片 hover 描边 + 夜读 + reveal |
| site/guide.html | W488 | v2.3.87 修改·7 emoji→朱砂 SVG + 卡片 hover 描边 + 夜读 + reveal |
| site/dukou-engine.html | W488 | v2.3.87 修改·header 标题加大 + 朱砂双线 + 夜读按钮 + dark 双变量覆盖 + footer 版本链 prepend |
| site/mobile-index.html | W488 | v2.3.87 修改·6 emoji→朱砂 SVG + hero 夜读按钮 + dark 覆盖 |
| skills/xiyouji-plan-review/SKILL.md | W488 | v2.3.87 修改·v1.0.1：陷阱 9「视觉目标 ≠ 工程卫生验收」+ 阶段 1 动作 6 + 阶段 0 目标性质登记 + 速查表 + 验证清单（双副本同步） |
| skills/xiyouji-plan-review/reference.md | W488 | v2.3.87 修改·§1.6 worktree 截图法 + 历史案例 7（双副本同步） |
| docs/superpowers/plans/2026-08-18-phase-e-visual-elevation-roadmap.md | W488 | v2.3.87 修改·E2 完成态回写（68168a6·56 页）+ 感知验收后补 |
| docs/superpowers/plans/2026-08-22-rootpages-visual-and-nightmode.md | W488 | v2.3.87 新增·方向 A 第一批方案（M-A1 感知验收强制项 + 夜读模式） |
| CHANGELOG.md / 交接文档.md / README.md / STRUCTURE.md / 项目说明.md / file-index.md | W488 | v2.3.87 修改·六文档同步 |

## W487 四会话 skill 二轮同步（2026-08-19·v2.3.86）

| 文件 | W | 说明 |
|---|---|---|
| skills/mem-wrap-up/SKILL.md | W487 | v2.3.86 修改·Step 7b 补 deep-review-loop 未安装降级声明（精简审查 + `DRL downgraded` 标注 + 降级≠跳过） |
| skills/self-evolution/SKILL.md | W487 | v2.3.86 修改·触发词扩充（记住这个/capture/经验沉淀）+ 写入步骤引用格式规范 |
| skills/self-evolution/references/experience-capture-format.md | W487 | v2.3.86 新增·经验捕获格式规范（97 行：写入格式 / 质量标准 / 边界纪律 / 手动触发 / 通用编号前缀） |
| AGENTS.md / README.md / STRUCTURE.md / skills/README.md | W487 | v2.3.86 修改·版本脚注 + 版本行 + skills 索引注记 |
| 交接文档.md / CHANGELOG.md / docs/00-导读/项目说明.md / scripts/output/file-index.md / site/dukou-engine.html | W487 | v2.3.86 修改·六文档同步 |
## W486 四会话 skill 协议同步（2026-08-19·v2.3.85）

| 文件 | W | 说明 |
|---|---|---|
| skills/agent-session-loop/{SKILL.md,references/01-review.md,references/02-wrap-up.md} | W486 | v2.3.85 修改·R0 4 件套 + 过拟合警报增强版 + verdict 7 词全序 + P2 ≤ N_max（对齐上游 Claude Code 修正） |
| skills/deep-review-loop/SKILL.md | W486 | v2.3.85 修改·verdict 禁词 5 处 6 词→7 词全序 + file size 目标 ≤500 行 / 5000 tokens |
| skills/mem-wrap-up/SKILL.md | W486 | v2.3.85 修改·Step 6 P2 ≤ N_max + work-log 路径修正 + R0 4 件套 + bridge_note 定义 |
| skills/self-evolution/SKILL.md | W486 | v2.3.85 修改·快速模式补「与整合版并用时」协调声明 |
| AGENTS.md / README.md / STRUCTURE.md / skills/README.md | W486 | v2.3.85 修改·版本脚注 + 版本行 + skills 索引注记 |
| 交接文档.md / CHANGELOG.md / docs/00-导读/项目说明.md / scripts/output/file-index.md / site/dukou-engine.html | W486 | v2.3.85 修改·六文档同步 |

## W485 收录三项目 playbook（2026-08-19·v2.3.84）

| 文件 | W | 说明 |
|---|---|---|
| skills/xiyouji-visual-batch/{SKILL.md,reference.md,.skill-metadata.yaml} | W485 | v2.3.84 新增·Phase E 视觉批次执行管线 playbook（W476/W477 实测验证） |
| skills/xiyouji-plan-authoring/{SKILL.md,reference.md,.skill-metadata.yaml} | W485 | v2.3.84 新增·W 批次路线图/方案撰写 playbook（九段结构） |
| skills/xiyouji-plan-review/{SKILL.md,reference.md,.skill-metadata.yaml} | W485 | v2.3.84 新增·方案/文档评估 playbook（取证硬门槛 + 五维评估）；metadata 为本次补写 |
| AGENTS.md | W485 | v2.3.84 修改·§4.5 补录 3 视觉/方案专项 skill（14→17）+ 版本脚注 |
| README.md / STRUCTURE.md / skills/README.md | W485 | v2.3.84 修改·skills 计数 14→17 + 新增行 |
| 交接文档.md / CHANGELOG.md / docs/00-导读/项目说明.md / scripts/output/file-index.md | W485 | v2.3.84 修改·六文档同步 |

## W484 Skills 目录治理（2026-08-19·v2.3.83）

| 文件 | W | 说明 |
|---|---|---|
| skills/xiyouji-{sun-wukong,zhu-bajie,sha-seng,tangseng,bai-longma}/agents/openai.yaml | W484 | v2.3.83 修改·System.Collections.Hashtable 占位符还原为真实中文描述 |
| skills/deep-review-loop/SKILL.md | W484 | v2.3.83 修改·新增平台适配段 + memory 路径占位符 + 工具映射 + 溯源标注 |
| skills/mem-wrap-up/SKILL.md | W484 | v2.3.83 修改·7 步收尾协议路径占位化 + 平台适配段 |
| skills/self-evolution/SKILL.md | W484 | v2.3.83 修改·平台适配 + 5 件套 sync verify 术语统一 |
| skills/agent-session-loop/SKILL.md + references/01-03.md | W484 | v2.3.83 修改·编排指向仓库内独立 skill + 三 references 精简版注记 |
| skills/xiyouji-tangseng/SKILL.md | W484 | v2.3.83 修改·「如二弟子」→「如来二弟子」错字修复 |
| skills/xiyouji-version-bump/SKILL.md | W484 | v2.3.83 修改·陷阱清单重复条目去重 |
| skills/xiyouji-en-translation/SKILL.md | W484 | v2.3.83 修改·footer 版本模板 v2.2.86·W334 → vX.Y.Z·W### 占位符 |
| skills/xiyouji-characters-knowledge/references/data-sources.md | W484 | v2.3.83 修改·EN 人物页计数 10→12 |
| skills/README.md | W484 | v2.3.83 新增·14 个 skill 索引表 + 平台适配说明 |
| scripts/_check_skills.py | W484 | v2.3.83 新增·skill 目录自检脚本（不入 gate） |
| AGENTS.md | W484 | v2.3.83 修改·§4.5 补录 4 会话流程 skill（10→14）+ 版本脚注 |
| README.md / STRUCTURE.md / 交接文档.md / docs/00-导读/项目说明.md / CHANGELOG.md / scripts/output/file-index.md | W484 | v2.3.83 修改·六文档同步 + 交接文档三 skill 闭环位置仓库化 + HEAD 修正 |

## W478 Phase E2 CN 可视化页传播 I（2026-08-18·v2.3.81）

| 文件 | W | 说明 |
|---|---|---|
| site/data 53 页 | W478 | v2.3.81 批量·_w478_migrate.py 六规则迁移（阴影→elev/圆角→radius/时长→dur/focus 派生/裸色白名单/豁免登记） |
| site/data/{hardship-heatmap,intertextuality-network,chapter-stats}.html | W478 | v2.3.81 试点·并行 session 3549327 人工迁移定范式 |
| docs/superpowers/plans/2026-08-18-phase-e-e2-batch-record.md | W478 | v2.3.81 修改·56 行迁移登记表 + 验收实测 |
| scripts/_w478_migrate.py | W478 | v2.3.81 新增·E2 迁移一次性脚本（不入门禁） |
| scripts/_w477_shot_check.js / scripts/output/e2_list.txt | W478 | v2.3.81 修改/新增·全批 56 页 pageerror 断言 + 派生清单 |
| site/dukou-engine.html | W478 | v2.3.81 修改·长链页脚 prepend |

## W477 Phase E1 组件层 v2 + 根页模板化（2026-08-18·v2.3.80）

| 文件 | W | 说明 |
|---|---|---|
| site/system.css | W477 | v2.3.80 修改·v2：card/kpi/chart-block elev-1+hover elev-2+radius-md·btn 五态+朱砂微渐变白名单·tab/badge/search pill·tooltip elev-3·颜色令牌化·微交互工具类（+2455B） |
| site/index.html | W477 | v2.3.80 修改·提问框全令牌化（elev/radius/渐变按钮/focus 光圈/chip pill） |
| site/dashboard.html | W477 | v2.3.80 修改·footer 统一 site-footer + 版本 v2.2.86→v2.3.79 + focus 派生统一 |
| site/curated.html / site/guide.html | W477 | v2.3.80 修改·卡片海拔化（elev-1/2 + radius-lg + 时长令牌） |
| site/mobile-index.html | W477 | v2.3.80 修改·nav-card/kpi-item 令牌化 |
| site/data/text-search.html | W477 | v2.3.80 修改·--focus-ring 未定义缺陷修复（color-mix 光圈） |
| site/static/fonts/NotoSansSC-{Regular,Medium}.woff2 | W477 | v2.3.80 覆写·子集化 9340 字（771/783→755/766KB） |
| site/data+en 225 页 | W477 | v2.3.80 批量·inline_css --force 重内联 system.css v2 |
| site/dukou-engine.html | W477 | v2.3.80 修改·长链页脚 prepend |

## W476 Phase E0 纸感轻立体宪改 + tokens v3（2026-08-18·v2.3.79）

| 文件 | W | 说明 |
|---|---|---|
| docs/superpowers/plans/2026-08-18-phase-e-visual-elevation-roadmap.md | W476 | v2.3.79 新增·Phase E 视觉高级感升级路线图 v1.1（W476-W483·六维度·三问已决） |
| docs/superpowers/plans/2026-08-18-phase-e-e0-probe-report.md | W476 | v2.3.79 新增·E0 探针取证报告 P1-P6 |
| DESIGN.md | W476 | v2.3.79 修改·§4A 纸感轻立体体系新立（8 节：演进声明/四级海拔/渐变白名单/排版阶梯/圆角边框/断点/微交互清单/体积预算）+ §1.1 演进指针 |
| site/tokens.css | W476 | v2.3.79 修改·v2→v3：--elev-0~4 海拔 + --radius-sm~pill + --border-hairline/accent + 色阶派生（--accent-deep/tint/wash + --ink-tint）+ 语义色 --ok~info + --text-step-0~5/--text-hero/--leading×3（+2035B） |
| site/data+en 225 页 | W476 | v2.3.79 批量·inline_css --force 重内联 tokens v3 + system.css |
| site/dukou-engine.html | W476 | v2.3.79 修改·长链页脚 prepend v2.3.79 W476 |

## W464 Phase 3 观测基线确立（2026-08-18·v2.3.82）

| 文件 | W | 说明 |
|---|---|---|
| scripts/baseline_snapshot.py | W464 | v2.3.82 新增·观测基线快照生成器（计数+性能+UV 手填栏+闸门阈值） |
| scripts/output/观测基线快照.md | W464 | v2.3.82 新增·机器生成基线表（611/86/138/228 + 性能三值 + UV 待回填） |
| scripts/output/perf-baseline.json | W464 | v2.3.82 修改·W464 实测（5 核心页 LCP/CLS/TBT） |
| scripts/_w464_perf_measure.js | W464 | v2.3.82 新增·一次性性能实测脚本 |
| site/dukou-engine.html | W464 | v2.3.82 修改·长链页脚 prepend |

## W460 墨韵全站动效体系 P0+样板批（2026-08-17·v2.3.75）

| 文件 | W | 说明 |
|---|---|---|
| site/tokens.css | W460 | v2.3.75 修改·新增动效令牌：--dur-fast/base/slow 三级时长 + --ease-out-quart/expo + --ease-in-out-soft 三系缓动 + --shadow-lift 浮起阴影 |
| site/system.css | W460 | v2.3.75 修改·六组升级：表格行 hover 暖底+朱砂指示条+数字列加深（blanket）；opt-in .table-anim 行入场 stagger（--row-i·封顶 220ms）与 .table-wrap--sticky（>30 行）；.btn:active 按压；.kpi/.card hover 浮起；.link-ink 下划线生长；.chart-tooltip 统一 tooltip 类；.card/.search-box 裸 ease 补齐 |
| site/index.html | W460 | v2.3.75 修改·stats count-up 脚本（900ms easeOutExpo·IO 触发一次·fail-open）+ 页脚版本 |
| site/dashboard.html | W460 | v2.3.75 修改·KPI count-up 脚本（纯数字正则过滤·文本型跳过） |
| site/data/chapter-stats.html | W460 | v2.3.75 修改·3 图 D3 入场编排（轴 200/网格 100+300/柱+点 500 stagger 封顶 400·easeCubicOut·折线 draw-in by getTotalLength）+ tooltip 收编 .chart-tooltip（视口钳制）+ ANIMATE 首帧门控 + reduced-motion 守卫 |
| site/data/character-appearance.html | W460 | v2.3.75 修改·条形/热力图对角波浪/散点 stagger + tipShow/tipMove/tipHide 统一 tooltip + ANIMATE 门控 + reduced-motion 守卫 |
| site/data/81-hardships.html | W460 | v2.3.75 修改·treemap×3 scale+fade 入场 + 桑基节点/流带淡入 + 交叉表/81 难表 .table-anim 行入场（--row-i）+ 难表（81 行）.table-wrap--sticky + 统一 tooltip + ANIMATE 门控 |
| site/data/emotional-heatmap.html | W460 | v2.3.75 修改·热力图对角波浪 stagger + 曲线按人物级联入场 + 轴/网格淡入 + 双 tooltip 收编 .chart-tooltip（内部结构样式保留·宣纸底配色重映射）+ ANIMATE 门控 |
| site/data/*.html（其余 81 页）+ site/en/*.html（138 页） | W460 | v2.3.75 修改·inline_css --force 同步 tokens/system 新动效样式（被动受益：表格 hover/按钮按压/卡片浮起全站生效） |
| docs/superpowers/w-b-critique.md | W460 | v2.3.75 新增·W-b 样板批 critique 评审报告（33/40·Keep/Fix 清单·过程缺陷记录） |
| site/data/cross-time-danmaku.html / site/data/tag-cloud.html | W460 | v2.3.75 修改·页脚版本同步（bump_version） |
| site/dukou-engine.html | W460 | v2.3.75 修改·页脚 prepend v2.3.75 W460 |
| CHANGELOG.md / 交接文档.md / README.md / STRUCTURE.md / docs/00-导读/项目说明.md / scripts/output/file-index.md | W460 | v2.3.75 修改·六文档同步（W460 四件套 + 接续编号 W461） |

## W459 V2 审查收尾（2026-08-17·v2.3.74）

| 文件 | W | 说明 |
|---|---|---|
| site/data/journey-spacetime.html | W459 | v2.3.74 修改·D2 回目跳转死链修复：A1_DOC_MAP 内嵌 100 条真实文件名映射 + chapterDocUrl 查表/目录回退 + 路径深度 ../→../../ |
| scripts/check_dynamic_links.py | W459 | v2.3.74 新增·动态链接门禁（内联 script 字面量链接存在性校验·--self-test 负样本自测） |
| scripts/verify_delivery.py | W459 | v2.3.74 修改·挂入 check_dynamic_links.py 动态链接门禁 |
| site/data/tag-cloud.html | W459 | v2.3.74 修改·dashboard 条目死链修复（file:"dashboard.html"→"../dashboard.html"） |
| site/en/ming-political-thought-comparison.html | W459 | v2.3.74 修改·source_doc 虚构英文化路径改诚实 ASCII 注记 |
| docs/00-导读/V2可视化维度方案.md | W459 | v2.3.74 修改·落地状态记录表 + Three 本地化条文回写 + D2 约定勘误 + 动态链接盲区风险条 + 验证清单更新 |
| site/index.html | W459 | v2.3.74 修改·精选必看补西游地理 3D 卡片（差异化描述）·note 八→九个入口 |
| site/dukou-engine.html | W459 | v2.3.74 修改·页脚 prepend v2.3.74 W459 |
| CHANGELOG.md / 交接文档.md | W459 | v2.3.74 修改·W459 四件套条目 + 交接同步（阻塞段陈旧 HEAD 行修正 + 方法论沉淀新增 JS 拼接链接盲区） |

## W449 冗余文档清理（2026-08-16·v2.3.64）

| 文件 | W | 说明 |
|---|---|---|
| 项目概览.md / 项目认知总览.md / 项目交接参考手册.md | W449 | v2.3.64 删除·判定与 交接文档.md 冗余（git rm·保留历史可恢复） |
| README.md | W449 | v2.3.64 修改·链接改指 交接文档.md |
| docs/00-导读/文档规范.md | W449 | v2.3.64 修改·§11.1/§11.4 旁文档 4→1（已先行提交） |
| scripts/output/file-index.md | W449 | v2.3.64 修改·移除 10 条三冗余文档反向索引 |
| MEMORY.md | W449 | v2.3.64 修改·修订陈旧 W423（未 push/无远端）记忆 + 英文站 138 页 + 空 legacy 目录 |
| site/dukou-engine.html | W449 | v2.3.64 修改·页脚 prepend v2.3.64 W449 |
| CHANGELOG.md / 交接文档.md | W449 | v2.3.64 修改·W449 四件套条目 + 交接同步 |

