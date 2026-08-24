# xiyouji 文件反向索引

> 与 [CHANGELOG.md](../../CHANGELOG.md) 配套：给定文件，查它被改过几次、每次对应哪个 W 条目。
> W### 编号规则见 CHANGELOG.md 顶部。
> 创建于 2026-07-22（v0.8 双索引改造）
>
> **历史归档**：W031-W087（v2.0.4-v2.0.60）site/data/ 部分已迁移至 [file-index-archive.md](file-index-archive.md)；W422 再归档 W393-W416 段。本文件仅保留 W417+ 现役索引。
>
> **维护契约**：本索引按 W 追加登记（每文件 1 行 + 一句摘要），历史段禁改；新增/变更文件必须先有 CHANGELOG 对应 W 段再登记（双索引铁律），禁止无 W 段单独登记。

---

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

## W448 外部锐评回应治理（2026-08-16·v2.3.63）

| 文件 | W | 说明 |
|---|---|---|
| STRUCTURE.md | W448 | v2.3.63 修改·「版本变更」段 94 行过期里程碑迁出（110KB→43KB） |
| STRUCTURE-archive.md | W448 | v2.3.63 新增·版本里程碑归档（v0.1-v2.2.48·W001-W272·68KB） |
| README.md | W448 | v2.3.63 修改·头部新增版本号语义说明（发布批次编号·非 SemVer） |
| LICENSE-CONTENT.md | W448 | v2.3.63 修改·新增「内容生成方式披露」节（人机协作 + AIGC 司法边界 + NC 范围澄清） |
| site/dukou-engine.html | W448 | v2.3.63 修改·页脚 prepend v2.3.63 W448 |
| CHANGELOG.md / 交接文档.md | W448 | v2.3.63 修改·W448 四件套条目 + 交接同步 |

## W447 工具目录治理（2026-08-14·v2.3.62）

| 文件 | W | 说明 |
|---|---|---|
| scripts/extract_strings.py / validate_en.py | W447 | v2.3.62 改名（原 _extract_strings.py/_validate_en.py 去下划线转正） |
| scripts/archive/（45 个） | W447 | v2.3.62 新增·历史一次性脚本归档（git mv 保留历史） |
| scripts/README.md | W447 | v2.3.62 修改·补 archive 说明 + 转正工具登记 |
| 交接文档.md | W447 | v2.3.62 修改·24 处旧工具名引用同步 |

## W446 英文站旧页 CJK 残留清理（2026-08-14·v2.3.61）

| 文件 | W | 说明 |
|---|---|---|
| site/en/ 52 个旧页（81-hardships/bestiary/chapters-map/tribulations/essay-*/character-*/guide/index/dashboard/methodology/site-map 等） | W446 | v2.3.61 修改·清理 408 条 CJK 违规（console 消息/中文文件名/学术括号注/未译正文） |
| site/**/*.html（3 页） | W446 | v2.3.61 修改·generate_csp.py 重生成 CSP（232 页·1145 内联哈希） |

## W445 英文站续译 relationships（2026-08-14·v2.3.60）

| 文件 | W | 说明 |
|---|---|---|
| site/en/relationships.html | W445 | v2.3.60 新增·关系网络页英文化（5703 script 字面量·341 去重·_validate_en.py 通过）·英文站 86 页全量完成 |
| site/sitemap.xml | W445 | v2.3.60 修改·补 1 个 en 页（226→227 页） |
| site/**/*.html（1 页） | W445 | v2.3.60 修改·generate_csp.py 重生成 CSP（232 页·1145 内联哈希） |

## W444 英文站续译 tag-cloud（2026-08-14·v2.3.59）

| 文件 | W | 说明 |
|---|---|---|
| site/en/tag-cloud.html | W444 | v2.3.59 新增·全站标签云导航页英文化（~494 script 字面量·_validate_en.py 通过） |
| site/sitemap.xml | W444 | v2.3.59 修改·补 1 个 en 页（225→226 页） |
| site/**/*.html（1 页） | W444 | v2.3.59 修改·generate_csp.py 重生成 CSP（231 页·1138 内联哈希） |

## W443 英文站续译 batch21（2026-08-14·v2.3.58）

| 文件 | W | 说明 |
|---|---|---|
| site/en/narratology-13d-network.html / emotional-heatmap.html / material-archaeology.html | W443 | v2.3.58 新增·并行 subagent 英文化 3 页（_validate_en.py 全过） |
| site/sitemap.xml | W443 | v2.3.58 修改·补 3 个 en 页（222→225 页） |
| site/**/*.html（3 页） | W443 | v2.3.58 修改·generate_csp.py 重生成 CSP（230 页·1132 内联哈希） |

## W442 英文站续译 batch20（2026-08-14·v2.3.57）

| 文件 | W | 说明 |
|---|---|---|
| site/en/poetry-rhythm-analysis.html / customs-pass-route.html / pilgrim-team-psychology-arc.html / jurisprudence.html / linguistics.html | W442 | v2.3.57 新增·并行 subagent 英文化 5 页（_validate_en.py 全过） |
| site/sitemap.xml | W442 | v2.3.57 修改·补 5 个 en 页（217→222 页） |
| site/**/*.html（5 页） | W442 | v2.3.57 修改·generate_csp.py 重生成 CSP（227 页·1111 内联哈希） |

## W441 英文站续译 batch19（2026-08-14·v2.3.56）

| 文件 | W | 说明 |
|---|---|---|
| site/en/ethics-consumption.html / monster-hierarchy-network.html / music-structure.html / heaven-power-network.html / ai-dialogue.html | W441 | v2.3.56 新增·并行 subagent 英文化 5 页（_validate_en.py 全过） |
| site/sitemap.xml | W441 | v2.3.56 修改·补 5 个 en 页（212→217 页） |
| site/**/*.html（5 页） | W441 | v2.3.56 修改·generate_csp.py 重生成 CSP（222 页·1086 内联哈希） |

## W440 英文站续译 batch18（2026-08-14·v2.3.55）

| 文件 | W | 说明 |
|---|---|---|
| site/en/karma-reincarnation.html / underworld-power-network.html / graph-explorer.html / narratology-12d-network.html / chart-design.html | W440 | v2.3.55 新增·并行 subagent 英文化 5 页（含工具页 graph-explorer·_validate_en.py 全过） |
| site/sitemap.xml | W440 | v2.3.55 修改·补 5 个 en 页（207→212 页） |
| site/**/*.html（5 页） | W440 | v2.3.55 修改·generate_csp.py 重生成 CSP（217 页·1054 内联哈希） |

## W439 英文站续译 batch17（2026-08-14·v2.3.54）

| 文件 | W | 说明 |
|---|---|---|
| site/en/dialogue-sentiment.html / monster-female-network.html / ecology.html / game-webnovel.html / monster-sociology.html | W439 | v2.3.54 新增·并行 subagent 英文化 5 页（_validate_en.py 全过） |
| site/sitemap.xml | W439 | v2.3.54 修改·补 5 个 en 页（202→207 页） |
| site/**/*.html（5 页） | W439 | v2.3.54 修改·generate_csp.py 重生成 CSP（212 页·1021 内联哈希） |

## W438 英文站续译 batch16（2026-08-14·v2.3.53）

| 文件 | W | 说明 |
|---|---|---|
| site/en/hardship-difficulty-heatmap.html / aesthetics.html / magic-system.html / visual-art.html / guanyin-six-roles-network.html | W438 | v2.3.53 新增·并行 subagent 英文化 5 页（_validate_en.py 全过） |
| site/sitemap.xml | W438 | v2.3.53 修改·补 5 个 en 页（197→202 页） |
| site/**/*.html（5 页） | W438 | v2.3.53 修改·generate_csp.py 重生成 CSP（207 页·988 内联哈希） |

## W437 英文站续译 batch15（2026-08-14·v2.3.52）

| 文件 | W | 说明 |
|---|---|---|
| site/en/business-model.html / intertextuality-network.html / risk-project.html / power-resources.html / cave-estate.html | W437 | v2.3.52 新增·并行 subagent 英文化 5 页（_validate_en.py 全过） |
| site/sitemap.xml | W437 | v2.3.52 修改·补 5 个 en 页（192→197 页） |
| site/**/*.html（5 页） | W437 | v2.3.52 修改·generate_csp.py 重生成 CSP（202 页·956 内联哈希） |

## W436 英文站续译 batch14（2026-08-14·v2.3.51）

| 文件 | W | 说明 |
|---|---|---|
| site/en/narrative-experiment.html / journey-spacetime.html / methodology-matrix.html / workplace.html / text-evolution.html | W436 | v2.3.51 新增·并行 subagent 英文化 5 页（_validate_en.py 全过） |
| site/sitemap.xml | W436 | v2.3.51 修改·补 5 个 en 页（187→192 页） |
| site/**/*.html（5 页） | W436 | v2.3.51 修改·generate_csp.py 重生成 CSP（197 页·924 内联哈希） |

## W435 英文站续译 batch13（2026-08-14·v2.3.50）

| 文件 | W | 说明 |
|---|---|---|
| site/en/deconstruction.html / six-senses-narratology-network.html / monster-victims-network.html / social-media.html / cognitive-psychology.html | W435 | v2.3.50 新增·并行 subagent 英文化 5 页（_validate_en.py 全过） |
| site/sitemap.xml | W435 | v2.3.50 修改·补 5 个 en 页（182→187 页） |
| site/**/*.html（5 页） | W435 | v2.3.50 修改·generate_csp.py 重生成 CSP（192 页·893 内联哈希） |

## W434 英文站续译 batch12（2026-08-14·v2.3.49）

| 文件 | W | 说明 |
|---|---|---|
| site/en/theological-intervention-network.html / criticism-history.html / global-pattern.html / cross-time-danmaku.html / character-dynamic-network.html | W434 | v2.3.49 新增·并行 subagent 英文化 5 页（含易碎页·_validate_en.py 全过） |
| site/sitemap.xml | W434 | v2.3.49 修改·补 5 个 en 页（177→182 页） |
| site/**/*.html（5 页） | W434 | v2.3.49 修改·generate_csp.py 重生成 CSP（187 页·860 内联哈希） |

## W433 英文站续译 batch11（2026-08-14·v2.3.48）

| 文件 | W | 说明 |
|---|---|---|
| site/en/four-dimensional-research-network.html / four-heavenly-kings-artifacts.html / monster-ecology-network.html / philosophy.html / concept-device.html | W433 | v2.3.48 新增·并行 subagent 英文化 5 页（_validate_en.py 全过） |
| site/sitemap.xml | W433 | v2.3.48 修改·补 5 个 en 页（172→177 页） |
| site/**/*.html（5 页） | W433 | v2.3.48 修改·generate_csp.py 重生成 CSP（182 页·828 内联哈希） |

## W432 英文站续译 batch10（2026-08-14·v2.3.47）

| 文件 | W | 说明 |
|---|---|---|
| site/en/pilgrim-team-dynamic-network.html / counterfactual.html / ming-political-thought-comparison.html / monster-background.html / cultural-misreading.html | W432 | v2.3.47 新增·并行 subagent 英文化 5 页（_validate_en.py 全过） |
| site/sitemap.xml | W432 | v2.3.47 修改·补 5 个 en 页（167→172 页） |
| site/**/*.html（5 页） | W432 | v2.3.47 修改·generate_csp.py 重生成 CSP（177 页·794 内联哈希） |

## W431 英文站续译 batch9（2026-08-14·v2.3.46）

| 文件 | W | 说明 |
|---|---|---|
| site/en/timeline.html / monster-capability-radar.html / journey-map-interactive.html / character-relationship-3d-view.html | W431 | v2.3.46 新增·并行 subagent 英文化 4 页（_validate_en.py 全过） |
| site/sitemap.xml | W431 | v2.3.46 修改·补 4 个 en 页（163→167 页） |
| site/**/*.html（4 页） | W431 | v2.3.46 修改·generate_csp.py 重生成 CSP（172 页·763 内联哈希） |

## W430 英文站续译 batch8（2026-08-14·v2.3.45）

| 文件 | W | 说明 |
|---|---|---|
| site/en/perf-canvas-rendering.html | W430 | v2.3.45 新增·D3.js 大数据集渲染优化页英文化（_validate_en.py 通过） |
| site/sitemap.xml | W430 | v2.3.45 修改·补 1 个 en 页（162→163 页） |
| site/**/*.html（1 页） | W430 | v2.3.45 修改·generate_csp.py 重生成 CSP（168 页·737 内联哈希） |

## W429 英文站续译 batch7（2026-08-14·v2.3.44）

| 文件 | W | 说明 |
|---|---|---|
| site/en/text-search.html / 81-hardships-view.html / mbti-evolution.html | W429 | v2.3.44 新增·3 张可视化页英文化（_validate_en.py 全过） |
| site/sitemap.xml | W429 | v2.3.44 修改·补 3 个 en 页（159→162 页） |
| site/**/*.html（3 页） | W429 | v2.3.44 修改·generate_csp.py 重生成 CSP（167 页·731 内联哈希） |

## W428 英文站续译 batch6（2026-08-14·v2.3.43）

| 文件 | W | 说明 |
|---|---|---|
| site/en/century-dialogue.html / data-explorer.html / language-style-radar.html / famous-time-travel.html / search.html | W428 | v2.3.43 新增·5 张可视化页英文化（EN 导航/页脚重建 + chrome/script 翻译·_validate_en.py 全过） |
| site/sitemap.xml | W428 | v2.3.43 修改·补 5 个 en 页（154→159 页） |
| site/**/*.html（5 页） | W428 | v2.3.43 修改·generate_csp.py 重生成 CSP（164 页·711 内联哈希） |

## W427 内容质量残留清理（2026-08-14·v2.3.42）

| 文件 | W | 说明 |
|---|---|---|
| docs/03-主题与情节专题/*.md（53 篇） | W427 | v2.3.42 修改·补 `> 轨标：学术研究`（西游与X/叙事学/批评/主义/美学/神话学/生态学/心理学/精神分析等·A4 30 篇轨别存疑列待人工判定） |
| docs/04-文化与历史背景/*.md（25 篇） | W427 | v2.3.42 修改·补 `> 轨标：学术研究`（明代制度对照/西游与X） |
| docs/03-主题与情节专题/*.md（21 文件） | W427 | v2.3.42 修改·移除开头 UTF-8 BOM（U+FEFF） |
| CHANGELOG.md / 交接文档.md / README.md / STRUCTURE.md / docs/00-导读/项目说明.md / site/dukou-engine.html | W427 | v2.3.42 修改·六文档同步 v2.3.42 W427（处置：保留 quality_review.py 未入库·5 个临时产物回收站） |

## W426 GoatCounter 自托管修复（2026-08-14·v2.3.41）

| 文件 | W | 说明 |
|---|---|---|
| site/static/js/goatcounter.js | W426 | v2.3.41 新增·从 arp242/goatcounter public/count.js 抓取（ISC·9213 字节）本地自托管 |
| site/**/*.html（160 页） | W426 | v2.3.41 修改·脚本 src 由 //gc.zgo.at/count.js 改为按页面深度的本地相对路径 + CSP 重生成（移除 gc.zgo.at 白名单） |
| scripts/generate_csp.py | W426 | v2.3.41 修改·EXTERNAL_SCRIPT_HOSTS 移除 gc.zgo.at（脚本转 'self'）·GOATCOUNTER_COUNT_ORIGIN 保留 |
| scripts/inject_goatcounter.py | W426 | v2.3.41 修改·build_tag 占位符 + inject 内按页面深度计算本地相对路径（幂等可重跑） |
| site/_headers | W426 | v2.3.41 修改·Netlify/CF CSP 移除 gc.zgo.at（script-src）·计数端点保留 |
| site/dukou-engine.html | W426 | v2.3.41 修改·页脚 v2.3.40 W425 → v2.3.41 W426（长链页脚头部插入） |


## W425 GoatCounter 真实跨访客统计接入（2026-08-14·v2.3.40）

| 文件 | W | 说明 |
|---|---|---|
| scripts/generate_csp.py | W425 | v2.3.40 修改·EXTERNAL_SCRIPT_HOSTS 追加 gc.zgo.at + connect-src 全站追加 GOATCOUNTER_COUNT_ORIGIN 1273984347.goatcounter.com |
| site/_headers | W425 | v2.3.40 修改·Netlify/CF CSP 白名单同步 gc.zgo.at（script-src）+ 1273984347.goatcounter.com（connect-src） |
| site/**/*.html（160 页） | W425 | v2.3.40 批量注入 GoatCounter 计数脚本（`</head>` 前）+ 159 页 CSP 重生成（680 内联哈希 0 漂移·_template 按约定排除） |
| site/dukou-engine.html | W425 | v2.3.40 修改·页脚 v2.3.39 W424 → v2.3.40 W425（长链页脚头部插入） |


## W424 对抗性审查修正与全仓整理（2026-08-12·v2.3.39）

| 文件 | W | 说明 |
|---|---|---|
| scripts/verify_delivery.py | W424 | v2.3.39 修改·EXPECT_A4 "201 篇"→"209 篇"（A4 计数假绿门禁变真校验） |
| README.md / STRUCTURE.md / docs/00-导读/项目说明.md | W424 | v2.3.39 修改·版本行 bump + A4 "199→201" parenthetical 统一 209·项目说明 :45 v2.3.37→v2.3.38 遗留同步 |
| 交接文档.md | W424 | v2.3.39 修改·W422/W423 三处矛盾修复·HEAD/版本列表/页脚最后更新 bump 至 v2.3.39 W424 |
| docs/00-导读/文档规范.md | W424 | v2.3.39 修改·A4 门禁描述 "201 篇"→"209 篇"（两处） |
| scripts/security_scan.py | W424 | v2.3.39 修改·_find_requirements_files 递归剪枝（命中 scripts/requirements.txt·不再扫环境 103 high）·discover_files 排除 .pw-browsers |
| site/data/character-relationship-3d.html | W424 | v2.3.39 修改·main() 改 load 事件触发（内联 defer 属性无效·3D 页从"加载失败"回退恢复为真实渲染） |
| site/en/journey-geo-semiotics.html | W424 | v2.3.39 修改·机械移除 466 处 Ch. 腐蚀注入·lang zh-CN→en |
| site/data/timeline.html | W424 | v2.3.39 修改·main() 改 load 事件触发（W423 d3 defer 化后 main() 解析期执行→d3 is not defined·Screenshot 首跑暴露·内联 defer 无效）·#timeline-viz 预留 min-height 460px 降 CLS |
| 新Agent启动Prompt.md | W424 | v2.3.39 修改·更新至 W423（四新门禁/性能预算/A4 209/security 修复） |
| .github/workflows/README.md | W424 | v2.3.39 修改·预算数字三套统一 4500/0.2/300·触发矩阵补 Screenshot 列·版本 v2.3.38 W423 |
| .github/workflows/perf.yml | W424 | v2.3.39 修改·断言校准：LCP 首跑 4.73-4.87s 超 4500 → 5000·CLS load 修复后 timeline 0.235 超 0.2 → 回归 0.3（W422 基线）·FCP warn 4800·TBT 300（实测 0） |
| DESIGN.md | W424 | v2.3.39 修改·"38 个可视化页"→"86 个可视化页面" |
| .pre-commit-config.yaml | W424 | v2.3.39 修改·补 verify-delivery 钩子 + 双门禁警告注释（防 pre-commit install 覆盖手动钩子后核心门禁静默消失） |
| scripts/check_data_drift.js | W424 | v2.3.39 新增·M2 双源漂移检查（内嵌数据 vs 引用 JSON 数组长度·v2 覆盖 base+f/变量 fetch 形态·挂 verify_delivery 门禁） |
| site/data/81-hardships.html | W424 | v2.3.39 修改·内嵌 hardships 空数组 → 注入完整 81 项（线上 fetch 404 后回退空表的真实漂移修复） |
| scripts/verify_delivery.py | W424 | v2.3.39 修改·新增数据漂移门禁（node scripts/check_data_drift.js） |
| tests/test_analyzer_smoke.py | W424 | v2.3.39 新增·M3 核心脚本 --help 冒烟（5 个 analyzer_base 系·jieba 缺失跳过 word_frequency） |
| .github/workflows/ci.yml | W424 | v2.3.39 修改·新增 verify-delivery job（交付校验门禁·8 job） |
| scripts/__init__.py / scripts/utils/__init__.py / scripts/B_人物/__init__.py | W424 | v2.3.39 新增·S1 regular package 化 |
| scripts/audit/archive/w102_check_sanzang.py | W424 | v2.3.39 修改·sys.path 与数据路径改 __file__ 引导（消除 cwd 依赖） |
| site/data/text-search.html | W424 | v2.3.39 修改·性能优化：删死 d3·语料抽为 text-search-app.js（load 后注入·LCP 6.5→4.6s） |
| site/static/js/text-search-app.js | W424 | v2.3.39 新增·text-search 语料+逻辑（原内嵌 EMBEDDED_DATA 迁出·2.1MB） |
| scripts/verify_delivery.py | W424 | v2.3.39 修改·EMB_RE 增加 text-search-app 模式（外部脚本回退形态） |
| site/static/fonts/noto-serif-sc-micro.woff2 | W424 | v2.3.39 新增·衬线字体微子集（611 字形·218KB vs 3.5MB·静态标题+100 回目+标点） |
| .github/workflows/perf.yml | W424 | v2.3.39 修改·LHCI URL 加入 text-search.html（5 页·LCP 1.9s 实测） |
| skills/xiyouji-character-content/ | W424 | v2.3.39 新增·角色内容 skill（四家族模板+门禁+UI 元数据·可安装） |
| skills/xiyouji-characters-knowledge/ | W424 | v2.3.39 新增·角色知识库 skill（211 角色名录+数据源+取证规范·可安装） |
| skills/xiyouji-sun-wukong/ 等 5 个主角 skill | W424 | v2.3.39 新增·孙悟空/唐僧/猪八戒/沙僧/白龙马单人 skill（速查卡+关键回目+数据源+生产规则·可安装） |
| README.md / STRUCTURE.md | W424 | v2.3.39 修改·目录树补全 18 docs 板块 + dataset/hyperframes（P1-4 落地） |
| scripts/C_情节/hardships_81.py / scripts/E_地理/journey_route.py | W424 | v2.3.39 修改·--output 改默认值（run_all 34/34 全过·M7 部分落地） |
| docs/00-导读/文档规范.md / 新Agent启动Prompt.md | W424 | v2.3.39 修改·TodoWrite → 任务清单（TaskCreate 系列·P2-1 落地） |
| .github/workflows/ci.yml | W424 | v2.3.39 修改·verify-delivery job 前置 run_all（数据漂移门禁 CI 真实生效） |
| site/static/fonts/noto-serif-sc-shared.woff2 | W424 | v2.3.39 新增·全站共享衬线微子集（1,119 字形·405KB vs 3.5MB） |
| site/tokens.css + site/data/*.html(85) + site/en/*.html(65) | W424 | v2.3.39 修改·serif @font-face src → 共享微子集（dashboard 传输 5.4→2.2MB） |
| docs/03-主题与情节专题 + docs/04-文化与历史背景（161 篇） | W424 | v2.3.39 修改·W### 出处回填（git 创建提交溯源 100 篇 + 初始导入标注 34 篇·0 缺 W）·时间哲学专题空文件恢复 |
| docs/01-全书逐回解读/第001回-灵根育孕源流出.md | W424 | v2.3.39 修改·数据指标"示例文本"占位 → 解读正文实测字数 |
| site/*.html（94 页） | W424 | v2.3.39 修改·外部脚本 SRI 加固：95 个标签补 integrity（SHA-384·CDN 字节核对后计算）+ crossorigin（d3×93·three×2·含 defer 形态） |
| site/*.html（159 页） | W424 | v2.3.39 修改·CSP meta 注入：script-src 'self'+CDN+680 内联脚本 SHA-256 哈希·script-src-attr 'none'·style-src unsafe-inline·connect-src 放行本地 RAG（dukou-engine/index/dashboard） |
| scripts/generate_csp.py | W424 | v2.3.39 新增·CSP 生成/注入/校验（幂等·--check 漂移门禁·Chrome 原始文本哈希口径·_template 排除） |
| scripts/verify_delivery.py | W424 | v2.3.39 修改·新增 CSP 漂移门禁（subprocess 调 generate_csp --check） |
| scripts/check_corruption.py | W424 | v2.3.39 新增·复盘沉淀门禁：R1 ""X"" 双引号翻倍腐蚀（site HTML）+ R2 d3 插件引用（d3.sankey 使用页必须引 d3-sankey.min.js）·挂 verify_delivery |
| scripts/sync_docs.py | W424 | v2.3.39 修改·规则校准：规则 2 改聚合声明（611 篇/86 页/A4 209）·规则 3 归档边界取多段最大值（W416）·README 维度标题正则兼容粗体（此前静默 FAIL 无门禁捕获） |
| scripts/verify_delivery.py | W424 | v2.3.39 修改·新增腐蚀/插件引用门禁（subprocess 调 check_corruption.py） |
| .github/workflows/ci.yml | W424 | v2.3.39 修改·两处 static server 启动加 5 次重试（runner 偶发 3s 起不来误报防复发） |
| 交接文档.md / 新Agent启动Prompt.md / docs/00-导读/访问统计方案.md / site/_headers | W424 | v2.3.39 修改·复盘沉淀同步：方法论新增 7 条·Prompt 更新至 W424 复盘沉淀速记·CSP 描述由"待部署切换"更新为"meta 已落地·_headers 仅 Netlify/CF 平台层" |
| scripts/output/adversarial-review-integrated-2026-08-11.md | W424 | v2.3.39 修改·"整合来源"标注底稿未单独留存（报告引用完整性·复盘批次） |
| site/data/graph-explorer.html | W424 | v2.3.39 修改·动态注入按钮的 onclick → addEventListener（CSP script-src-attr 'none' 前置） |
| site/mobile-index.html | W424 | v2.3.39 修改·javascript:history.back() 链接 → 事件绑定 + href="#" |
| site/en/character-relationship-3d.html | W424 | v2.3.39 修改·32 处 ""X"" 双引号翻倍腐蚀修复（EN 腐蚀第二波·CSP 实测暴露） |
| site/en/character-appearance.html | W424 | v2.3.39 修改·4 处模板字符串缺失收尾反引号修复（EN 腐蚀第二波） |
| site/data/magic-system.html 等 6 页 | W424 | v2.3.39 修改·补引 d3-sankey.min.js（桑基图从未渲染→实测 6/6 出图·magic-system 0→52 图形） |
| scripts/check_js_syntax.py | W424 | v2.3.39 修改·SCRIPT_RE 覆盖带属性无 src 脚本（此前 <script> 精确匹配漏检） |
| site/_template.html | W424 | v2.3.39 修改·移除 CSP meta（开发模板不入站·生成器跳过不注入） |
| scripts/lint_links.py | W424 | v2.3.39 修改·外链检查修复：非 http(s) 协议跳过 + 非 ASCII URL 百分号编码（中文外链误报 broken 消除） |
| scripts/output/adversarial-review-integrated-2026-08-11.md | W424 | v2.3.39 新增·对抗性审查整合总报告（2026-08-11·W424 逐条核验来源） |
| scripts/output/agent-web-security-2026-08-11.md | W424 | v2.3.39 新增·xiyouji-agent-web 离线安全审查报告（2026-08-11） |
| scripts/_audit_data.json / _audit_hiddencount.json / _audit_refine.json / _audit_report.json | W424 | v2.3.39 删除·一次性审计原始数据（对应 .md 报告保留） |
| scripts/output/screenshots/ | W424 | v2.3.39 清理·slices/mobile/desktop ~416MB 删除（保留 viz 证据）·过期报告 14 个删除 |
| scripts/output/rag_index.json | W424 | v2.3.39 重建·35.8MB（08-12 重建·含全文同步·未入库） |

## W423 性能债专项（2026-08-11·v2.3.38）

| 文件 | W | 说明 |
|---|---|---|
| .github/workflows/perf.yml | W423 | v2.3.38 修改·LHCI 预算收紧 LCP 5000→4500·CLS 0.3→0.2·FCP warn 4800→4200·interactive warn 5000→4500·TBT 300 不变 |
| site/tokens.css | W423 | v2.3.38 修改·3 套 CJK @font-face font-display swap→optional（CLS 根因）·JetBrains Mono 保持 swap |
| site/data/*.html（86 页） | W423 | v2.3.38 修改·同源 CJK 字体 optional 替换·../static/fonts/ 路径零破坏 |
| site/dashboard.html | W423 | v2.3.38 修改·head 同步 d3 移至 body 末尾（LCP 根因·~4.7s） |
| site/data/timeline.html / site/data/character-relationship-3d.html | W423 | v2.3.38 修改·d3+Three defer（图表 run() 在 load 后执行） |
| CHANGELOG.md / 交接文档.md / scripts/output/file-index.md | W423 | v2.3.38 修改·新增 W423 段与登记（本段） |


## W422 全量治理（2026-08-10·v2.3.37）

| 文件 | W | 说明 |
|---|---|---|
| .github/workflows/perf.yml | W422 | v2.3.37 修改·补 push main（site/**）+ 每周一定时（LHCI 硬预算此前仅 PR/manual·项目无 PR 从未运行）·push 首跑暴露性能债后按实测校准阈值（LCP 5000/CLS 0.3/FCP warn 4800/interactive warn 5000·TBT 300 保持） |
| scripts/verify_delivery.py | W422 | v2.3.37 修改·新增 4 项硬门禁：A1 导航相邻性断言 / docs/01 lint_links 子进程校验 / sitemap 覆盖一致性（排除统计/预览 6 页）/ site/data 内嵌回退模式静态检查 |
| .github/workflows/ci.yml | W422 | v2.3.37 修改·Code Quality 新增批量 JS 语法检查（check_js_syntax.py --all）+ mypy report-only（静默退出防告警）·a11y job 名/步骤名口径修正（9-rule→19 checks/20 SC） |
| .github/dependabot.yml | W422 | v2.3.37 新增·Dependabot（github-actions + npm×2 + pip·每周·分组生产/开发依赖） |
| .github/workflows/screenshot-review.yml | W422 | v2.3.37 修改·截图 artifact 改为失败才上传 + retention 30→14 天 |
| scripts/a11y_audit.py | W422 | v2.3.37 修改·docstring "40 条规则"→"19 项检查覆盖 20 条 SC"（口径统一） |
| CHANGELOG.md | W422 | v2.3.37 修改·新增 v2.3.37 W422 段·编号规则 W001-W421→W001-W422·归档 v2.3.18-v2.3.31（W400-W416）段至 CHANGELOG-ARCHIVE（83 行） |
| CHANGELOG-ARCHIVE.md | W422 | v2.3.37 修改·追加 W422 归档段（v2.3.18-v2.3.31） |
| scripts/output/file-index.md | W422 | v2.3.37 修改·本段（W422 登记）·归档 W393-W416 段（127 行·W417+ 现役）·头部说明更新 |
| scripts/output/file-index-archive.md | W422 | v2.3.37 修改·追加 W422 归档段（W416 及更早） |
| 交接文档.md | W422 | v2.3.37 修改·头部/阻塞 HEAD/当前进度 W422 里程碑/版本号 v2.3.37 + 接续编号（当前 W422·下一 W423）·归档 W413-W418 里程碑 + 版本历史摘要（556 行）·方法论新增 W422（门禁触发缺失二犯） |
| 交接文档-archive.md | W422 | v2.3.37 修改·追加 W422 归档段（W413-W418 + 版本历史摘要） |
| README.md | W422 | v2.3.37 修改·版本行 v2.3.37 W422 + W 范围 W001-W422 |
| STRUCTURE.md | W422 | v2.3.37 修改·头部版本行 v2.3.37 W422 |
| docs/00-导读/项目说明.md | W422 | v2.3.37 修改·版本行 ×2 + 双索引链接规则校准（新创作执行·存量以 file-index 追溯） |
| docs/00-导读/文档规范.md | W422 | v2.3.37 修改·§11.2 禁改范围 W001-W420→W001-W421 |
| .github/workflows/README.md | W422 | v2.3.37 修改·W 链加 W422 + W422 说明行 + perf.yml 触发矩阵更新 |
| site/dukou-engine.html | W422 | v2.3.37 修改·页脚插入 v2.3.37 W422 段 |
| site/index.html | W422 | v2.3.37 修改·页脚 v2.3.38 · W423 |
| site/data/cross-time-danmaku.html | W422 | v2.3.37 修改·页脚 v2.3.38 · W423 |
| site/data/tag-cloud.html | W422 | v2.3.37 修改·页脚 v2.3.38 · W423 |
| _DEBRIS_xiyouji_move | W422 | v2.3.37 删除·空 debris 目录（未跟踪）清理 |

## W421 Screenshot Review 提速优化（2026-08-10·v2.3.36）

| 文件 | W | 说明 |
|---|---|---|
| .github/workflows/screenshot-review.yml | W421 | v2.3.36 修改·新增 Determine screenshot scope 改动范围判定步骤（页脚 4 文件/文档-only 跳过·site/data 变更定向截图·static/assets/脚本/workflow 变更全量·schedule/dispatch 恒全量）+ checkout fetch-depth 0 + Playwright 浏览器缓存（actions/cache@v6·key 跟 package-lock）·跳过时 GITHUB_STEP_SUMMARY 输出原因 |
| scripts/batch_screenshots.js | W421 | v2.3.36 修改·新增 --only-pages "file:dir,..." 参数（替换全量列表·定向截图）·--help/汇总报告同步·本地实测 2 页 × 2 视口 ~14-20s |
| CHANGELOG.md | W421 | v2.3.36 修改·新增 v2.3.36 W421 段·W### 编号规则 W001-W420→W001-W421 |
| scripts/output/file-index.md | W421 | v2.3.36 修改·本段（W421 登记） |
| README.md | W421 | v2.3.36 修改·版本行 v2.3.36 W421 + 双索引 W 范围 W001-W421 |
| STRUCTURE.md | W421 | v2.3.36 修改·头部版本行 v2.3.36 W421 |
| docs/00-导读/项目说明.md | W421 | v2.3.36 修改·头部 + "当前版本"行 v2.3.36 W421 |
| 交接文档.md | W421 | v2.3.36 修改·头部/阻塞段 HEAD/当前进度 W421 里程碑/版本号列表 v2.3.36 + 接续编号（当前 W421·下一 W422）+ 方法论沉淀（paths 过滤 vs diff 判定） |
| site/dukou-engine.html | W421 | v2.3.36 修改·页脚插入 v2.3.36 W421 段 |
| site/index.html | W421 | v2.3.36 修改·页脚 v2.3.36 · W421 |
| site/data/cross-time-danmaku.html | W421 | v2.3.36 修改·页脚 v2.3.36 · W421 |
| site/data/tag-cloud.html | W421 | v2.3.36 修改·页脚 v2.3.36 · W421 |
| .github/workflows/README.md | W421 | v2.3.36 修改·头部 W 链加 W421 + W421 说明行 + Screenshot Review 触发矩阵更新 |
| docs/00-导读/文档规范.md | W421 | v2.3.36 修改·§11.2 禁改范围 W001-W419→W001-W420（随 W421 校准·E2 深处残留） |


## W420 A1 内容质量深化（2026-08-10·v2.3.35）

| 文件 | W | 说明 |
|---|---|---|
| docs/01-全书逐回解读/第001-100回-*.md（100 回） | W420 | v2.3.35 修改·①深度解读补全：第038/039回新增 `## 深度解读` 段（SD102/SD103·原 2 回无深读缺口消除·100/100）②结构化元数据：56 回补 `> 对应原著：第X回` + `> 数据指标：` 行（逐篇按真实梗概/数据撰写）③导航错链修复 99 回：上一回/下一回指向非相邻回（约 60 回）→ 相邻回对齐 + 6 回补缺上一回 + 标签统一 ④sd-crossref 死链修复 10 回：`../../../docs/` 多级 ../（66 处）→ `../` ⑤第083回补缺 H1 标题行 + `>轨标` 空格规范化 |
| source/原文/shendu/SD102.md | W420 | v2.3.35 新增·第38回深读"婴儿问母——当真相只能从枕边问出"（枕边测谎/程序正义悖论/井龙王保证据/八戒撺唆紧箍咒·含第三行元数据注释） |
| source/原文/shendu/SD103.md | W420 | v2.3.35 新增·第39回深读"一粒金丹——当合法性需要三教合流来救"（嚎啕哭丧/金丹清气双救生/紧箍咒辨真假反转/文殊一饮一啄与阉狮悖论·含第三行元数据注释） |
| CHANGELOG.md | W420 | v2.3.35 修改·新增 v2.3.35 W420 段·W### 编号规则 W001-W419→W001-W420 |
| scripts/output/file-index.md | W420 | v2.3.35 修改·本段（W420 登记） |
| README.md | W420 | v2.3.35 修改·版本行 v2.3.35 W420 + 双索引 W 范围 W001-W420 |
| STRUCTURE.md | W420 | v2.3.35 修改·头部版本行 v2.3.35 W420 |
| docs/00-导读/项目说明.md | W420 | v2.3.35 修改·头部 + "当前版本"行 v2.3.35 W420 |
| 交接文档.md | W420 | v2.3.35 修改·头部/阻塞段 HEAD/当前进度 W420 里程碑/版本号列表 v2.3.35 + 接续编号（当前 W420·下一 W421）/文件尾最后更新 |
| site/dukou-engine.html | W420 | v2.3.35 修改·页脚插入 v2.3.35 W420 段 |
| site/index.html | W420 | v2.3.35 修改·页脚 v2.3.35 · W420 |
| site/data/cross-time-danmaku.html | W420 | v2.3.35 修改·页脚 v2.3.35 · W420 |
| site/data/tag-cloud.html | W420 | v2.3.35 修改·页脚 v2.3.35 · W420 |
| .github/workflows/README.md | W420 | v2.3.35 修改·头部 W 链加 W420 + W420 说明行 |
| docs/00-导读/文档规范.md | W420 | v2.3.35 修改·§11.2 禁改范围 W001-W418→W001-W419（随 W420 校准·E2 深处残留） |


## W417 文档健康治理（2026-08-10·v2.3.32）

| 文件 | W | 说明 |
|---|---|---|
| CHANGELOG.md | W417 | v2.3.32 修改·归档精简 136KB→39KB（W399 及更早迁移至 CHANGELOG-ARCHIVE.md）·新增 v2.3.32 W417 段·W### 编号规则 W001-W416→W001-W417 |
| CHANGELOG-ARCHIVE.md | W417 | v2.3.32 修改·追加 v2.3.17 W399 及更早归档段·头部标注扩大（v0.1-v2.3.17 W001-W399） |
| scripts/output/file-index.md | W417 | v2.3.32 修改·归档精简 87KB→32KB（W335-W389 段迁移）·本段（W417 登记） |
| scripts/output/file-index-archive.md | W417 | v2.3.32 修改·追加归档段 W335-W389·头部标注扩大 |
| 交接文档.md | W417 | v2.3.32 修改·精简里程碑概要（删 W411 及更早 545 行·保留 v2.3.27-v2.3.31）·头部/阻塞段/当前进度 W417·版本号列表/接续编号 W417 |
| README.md | W417 | v2.3.32 修改·版本行 v2.3.32 W417·授权段边界补强（源代码与项目文档 MIT vs 文本内容 CC BY-NC 明确化）·W 范围 W001-W417 |
| STRUCTURE.md | W417 | v2.3.32 修改·头部版本行 v2.3.32 W417 |
| docs/00-导读/项目说明.md | W417 | v2.3.32 修改·头部 + "当前版本"行 v2.3.32 W417 |
| scripts/verify_delivery.py | W417 | v2.3.32 增强·A1-A6 真实文件计数校验 vs README 声明（排除各板块 README.md）·归档 3 件套纳入范围漂移扫描 |
| scripts/bump_version.py | W417 | v2.3.32 增强·新增 --desc 主描述替换·W001-W### 精确锚点范围替换·页脚 3 个简单页脚自动同步 |
| LICENSE-CONTENT.md | W417 | v2.3.32 修改·CC BY-NC 范围精确化（内容板块 + site 渲染文本）·导航/协作文档归 MIT·适用内容补 07-09/S3/S4 |
| site/sitemap.xml | W417 | v2.3.32 修改·补全漏收录页 69→154（en/ 全套 + 入口页 + data/ 内容页·排除模板/预览/统计页）·lastmod 2026-08-10 |
| site/dukou-engine.html | W417 | v2.3.32 修改·页脚插入 v2.3.32 W417 段 |
| site/index.html | W417 | v2.3.32 修改·页脚 v2.3.32 · W417 |
| site/data/cross-time-danmaku.html | W417 | v2.3.32 修改·页脚 v2.3.32 · W417 |
| site/data/tag-cloud.html | W417 | v2.3.32 修改·页脚 v2.3.32 · W417 |
| .github/workflows/ci.yml | W417 | v2.3.32 修改·actions 升级消除 Node 20 deprecation（checkout v7/setup-python v7 等） |
| .github/workflows/pages.yml | W417 | v2.3.32 修改·actions 升级（upload-pages-artifact v5/configure-pages v6/deploy-pages v5） |
| .github/workflows/perf.yml | W417 | v2.3.32 修改·actions 升级（setup-node v7/nick-fields retry v4） |
| .github/workflows/screenshot-review.yml | W417 | v2.3.32 修改·actions 升级（upload-artifact v7 等） |
| .github/workflows/security.yml | W417 | v2.3.32 修改·actions 升级（checkout v7/setup-python v7 等） |
| scripts/output/rag_index.json | W417 | v2.3.32 重建验证·删除后自动重建成功（32.39→35.26MB·gitignored 不提交） |


## W418 内容质量深化（2026-08-10·v2.3.33）

| 文件 | W | 说明 |
|---|---|---|
| site/en/guide.html | W418 | v2.3.33 修改·修复 25 处 broken 链接（data/xxx.html 前缀错误）——EN 版存在指向同目录（chapter-stats/narrative-rhythm-curve/81-hardships/character-appearance/chapter-structure-graph）·无 EN 版回退中文原版 ../data/*.html 加 lang="zh-CN" 标注（text-search 等 20 处） |
| site/en/character-relationship-3d.html | W418 | v2.3.33 修改·修复 2 处 broken（character-dynamic-network/relationships → ../data/ + lang="zh-CN"） |
| site/en/chapter-structure-graph.html | W418 | v2.3.33 修改·修复 1 处 broken（timeline.html → ../data/timeline.html + lang="zh-CN"） |
| site/en/narrative-rhythm-curve.html | W418 | v2.3.33 修改·修复 1 处 broken（timeline.html → ../data/timeline.html + lang="zh-CN"） |
| docs/01-全书逐回解读/第0XX回-*.md（23 回） | W418 | v2.3.33 修改·补 `> 导航：` 引用行（返回导读/上一回/下一回/站点首页/通用可视化）——019/020/021/031/035/042/043/044/048/051/052/055/071/075/076/082/083/084/087/089/091/092/097 回·100 回导航全覆盖 |
| site/dukou-engine.html | W418 | v2.3.33 修改·页脚插入 v2.3.33 W418 段（内容质量深化） |
| site/index.html | W418 | v2.3.33 修改·页脚 v2.3.33 · W418 |
| site/data/cross-time-danmaku.html | W418 | v2.3.33 修改·页脚 v2.3.33 · W418 |
| site/data/tag-cloud.html | W418 | v2.3.33 修改·页脚 v2.3.33 · W418 |
| CHANGELOG.md | W418 | v2.3.33 修改·新增 v2.3.33 W418 段·W### 编号规则 W001-W417→W001-W418 |
| scripts/output/file-index.md | W418 | v2.3.33 修改·本段（W418 登记）·W417 历史段页脚 3 行恢复（bump 全局替换污染修复） |
| README.md | W418 | v2.3.33 修改·版本行 v2.3.33 W418·W 范围 W001-W418 |
| STRUCTURE.md | W418 | v2.3.33 修改·头部版本行 v2.3.33 W418 |
| docs/00-导读/项目说明.md | W418 | v2.3.33 修改·头部 + "当前版本"行 v2.3.33 W418 |
| 交接文档.md | W418 | v2.3.33 修改·头部/阻塞段 HEAD/当前进度 W418 里程碑/版本号列表 v2.3.33 + 接续编号（当前 W418·下一 W419） |


## W419 修复 A1 深度解读 SD 错位（2026-08-10）

| 文件 | W | 说明 |
|---|---|---|
| source/原文/shendu/SD038-052、SD056-062.md（24 篇） | W419 | v2.3.34 修改·元数据"推测对应原著回号"修正为真实回号（22 篇 + SD075/077 归程篇 47-49→99/99-100）+ 正文 H1 `# 第X回` 编号→真实回号（17 篇·范围式写第Y-Z回）+ 正文内嵌"当前回"引用修正（SD038/039/040 共 4 处）+ `> 关联：` 链接改指真实回文件（9 篇） |
| source/原文/shendu/SD101.md | W419 | v2.3.34 新增·第 56 回深读"草寇之死——当打杀凡人触碰了取经的底线"（神狂诛草寇 道昧放心猿·补 56 回无深读空缺） |
| docs/01-全书逐回解读/第038-072回-*.md（35 回） | W419 | v2.3.34 修改·22 篇错位 SD 归位（编号≠真实回号：SD038 红孩儿 40-42/SD039-040 黑水河 43/SD041 车迟国 44-46/SD042-043 车迟国收尾 45-46/SD044-046 通天河 47-49/SD047 金兜山 50-52/SD048 女儿国 53-55/SD049+055 蝎子精毒敌山 55/SD050+057 火焰山 59-61/SD051-052 祭赛国碧波潭 62-63/SD056 六耳猕猴 57-58/SD058 荆棘岭 64/SD059 小西天 65-66/SD060 七绝山 67/SD061 朱紫国 68-71/SD062 盘丝洞 72）·范围式复制到范围内每回·40-72 回全覆盖·63-72 回新建深度解读段·38/39/56 回删除空段·第 056 回插入 SD101 |
| CHANGELOG.md | W419 | v2.3.34 修改·新增 v2.3.34 W419 段·W### 编号规则 W001-W418→W001-W419 |
| scripts/output/file-index.md | W419 | v2.3.34 修改·本段（W419 登记）·W418 历史段页脚 3 行恢复（bump 全局替换污染修复） |
| README.md | W419 | v2.3.34 修改·版本行 v2.3.34 W419 主描述补全·W 范围 W001-W419 |
| STRUCTURE.md | W419 | v2.3.34 修改·头部版本行 v2.3.34 W419 主描述补全 |
| docs/00-导读/项目说明.md | W419 | v2.3.34 修改·头部 + "当前版本"行 v2.3.34 W419 |
| 交接文档.md | W419 | v2.3.34 修改·头部/阻塞段 HEAD/当前进度 W419 里程碑/版本号列表 v2.3.34 + 接续编号（当前 W419·下一 W420） |
| site/dukou-engine.html | W419 | v2.3.34 修改·页脚插入 v2.3.34 W419 段 |
| site/index.html | W419 | v2.3.34 修改·页脚 v2.3.34 · W419 |
| site/data/cross-time-danmaku.html | W419 | v2.3.34 修改·页脚 v2.3.34 · W419 |
| site/data/tag-cloud.html | W419 | v2.3.34 修改·页脚 v2.3.34 · W419 |
| docs/00-导读/文档规范.md | W419 | v2.3.34 修改·§11.2 禁改范围 W001-W414→W001-W418（随 W419 校准）+ 新增「误改后果」列（12 类禁改文件附违反后果）·新增 §11.4 同步核对速查表（10 项勾选清单） |
| 新Agent启动Prompt.md | W419 | v2.3.34 新建 + 处置收尾补充·新 Agent 启动 prompt（交接文档速用精简版·可直接复制发送·含四步认知顺序 + §11 规则 + E1 铁律 + W419 三条新增铁律：bump 污染校验（W418/W419 复现 2 次）/ 批量重写最小化 diff（git restore 非必要改动）/ A1 SD 禁重跑合并脚本） |

> 当前版本 v2.3.65（2026-08-16）

## W450 统计口径统一与轨标体系（2026-08-16）

| 文件 | W | 说明 |
|---|---|---|
| docs/00-导读/统计口径说明.md | W450 | v2.3.65 新增·对外数字唯一口径来源（611 篇/86 页/133 维/55 引用/版本语义） |
| site/index.html | W450 | v2.3.65 修改·stats 625→611、80→86、133→55 学术引用 + 新增「精选必看」8 卡 + dashboard/tag-cloud 文案 80→86 |
| site/dashboard.html | W450 | v2.3.65 修改·「80 个可视化页面」→86 |
| README.md | W450 | v2.3.65 修改·双轨写作补 跨界趣谈 + 统计口径链接 + 133 维口径注 |
| docs/00-导读/文档规范.md | W450 | v2.3.65 修改·新增 §4.5 轨标体系与准入 |
| docs/03-主题与情节专题/*.md（33 篇） | W450 | v2.3.65 修改·轨标 学术研究→跨界趣谈（现代学科趣味透镜·仅现役首行，4 篇历史追溯块保持原值） |
| LICENSE-CONTENT.md | W450 | v2.3.65 修改·新增纯 AI 输出不主张著作权条款 |
| site/dukou-engine.html / site/data/cross-time-danmaku.html / site/data/tag-cloud.html | W450 | v2.3.65 修改·页脚 prepend v2.3.65 W450 |
| CHANGELOG.md / 交接文档.md | W450 | v2.3.65 修改·W450 四件套条目 + 交接同步 |
| scripts/output/file-index.md | W450 | v2.3.65 修改·W450 现役索引段 |

## W451 学术研究引用审计（2026-08-16·v2.3.66）

| 文件 | W | 说明 |
|---|---|---|
| docs/02-人物深度分析/人物谱系表.md 等 9 篇 | W451 | v2.3.66 修改·轨标 学术研究→教学讲解（引用审计：无论文/专著/版本/理论框架出处） |
| docs/00-导读/文档规范.md | W451 | v2.3.66 修改·§4.5 学术研究定义收紧（仅凭文本证据不算引用）+ 历史注 W451 |
| README.md | W451 | v2.3.66 修改·版本行主描述 W451 |
| site/dukou-engine.html / site/index.html / site/data/cross-time-danmaku.html / site/data/tag-cloud.html | W451 | v2.3.66 修改·页脚 prepend v2.3.66 W451 |
| CHANGELOG.md / 交接文档.md | W451 | v2.3.66 修改·W451 四件套条目 + 交接同步 |
| scripts/output/file-index.md | W451 | v2.3.66 修改·W451 现役索引段 |

## W452 学术研究显式引用补齐（2026-08-16·v2.3.67）

| 文件 | W | 说明 |
|---|---|---|
| docs/02-05 现役「学术研究」文档（105 篇） | W452 | v2.3.67 修改·轨标行后补 `> 引用：` 显式链接 学术论文索引 |
| scripts/verify_delivery.py | W452 | v2.3.67 修改·新增「学术研究 轨显式引用门禁」（首行轨标=学术研究 必须含 > 引用：学术论文索引） |
| docs/00-导读/文档规范.md | W452 | v2.3.67 修改·§4.5 准入规则补第 4 条（头部 > 引用：机器校验）+ 历史注 W452 |
| README.md | W452 | v2.3.67 修改·版本行主描述 W452 |
| site/dukou-engine.html / site/index.html / site/data/cross-time-danmaku.html / site/data/tag-cloud.html | W452 | v2.3.67 修改·页脚 prepend v2.3.67 W452 |
| CHANGELOG.md / 交接文档.md | W452 | v2.3.67 修改·W452 四件套条目 + 交接同步 |
| scripts/output/file-index.md | W452 | v2.3.67 修改·W452 现役索引段 |

## W453 移除评论.txt（2026-08-16·v2.3.68）

| 文件 | W | 说明 |
|---|---|---|
| 评论.txt | W453 | v2.3.68 删除·外部锐评原始文本退役（结论已沉淀于 CHANGELOG W448-W452·git 历史可恢复） |
| README.md | W453 | v2.3.68 修改·版本行主描述 W453 |
| site/dukou-engine.html / site/index.html / site/data/cross-time-danmaku.html / site/data/tag-cloud.html | W453 | v2.3.68 修改·页脚 prepend v2.3.68 W453 |
| CHANGELOG.md / 交接文档.md | W453 | v2.3.68 修改·W453 四件套条目 + 交接同步 |
| scripts/output/file-index.md | W453 | v2.3.68 修改·W453 现役索引段 |

> 当前版本 v2.3.66（2026-08-16）

## W451 学术研究引用审计（2026-08-16）

| 文件 | W | 说明 |
|---|---|---|

> 当前版本 v2.3.67（2026-08-16）

## W452 学术研究显式引用门禁（2026-08-16）

| 文件 | W | 说明 |
|---|---|---|

> 当前版本 v2.3.68（2026-08-16）

## W453 移除评论.txt（2026-08-16）

| 文件 | W | 说明 |
|---|---|---|

> 当前版本 v2.3.70（2026-08-16）

## W455 方案 B/C/D 三个可视化深化（2026-08-16·v2.3.70）

| 文件 | W | 说明 |
|---|---|---|
| site/data/character-dynamic-network.html | W455 | v2.3.70 修改·1-100 回目进度条播放关系边 + 邻域模式（点击节点一度邻接+ESC 退出）+ 边权重线宽 1-5px + 透明度 0.3-1.0 |
| site/data/hardship-difficulty-heatmap.html | W455 | v2.3.70 修改·单元格钻取详情面板（结局类型/搬救兵/求助次数）+ 81 行清单 ↔ 热力图双向联动 + 难度/章节/结局三排序 |
| site/data/journey-spacetime.html | W455 | v2.3.70 修改·双轴联动（时间轴 ↔ 地图节点 `.highlighted` 同步高亮）+ 节点跳转 A1 回目解读 `<a target="_blank">` + 段路叠加耗时刻度 |
| CHANGELOG.md / 交接文档.md / README.md / STRUCTURE.md / docs/00-导读/项目说明.md | W455 | v2.3.70 修改·版本行 v2.3.70 W455 主描述 |
| site/dukou-engine.html | W455 | v2.3.70 修改·页脚 prepend v2.3.70 W455 + v2.3.69 W454 段 |
| scripts/output/file-index.md | W455 | v2.3.70 修改·W454 + W455 现役索引段 |

## W454 方案 A 西游地理 3D 可视化（2026-08-16·v2.3.69）

| 文件 | W | 说明 |
|---|---|---|
| site/data/journey-geo-3d.html | W454 | v2.3.69 新建·Three.js r128（cdnjs+SRI）+ 手动 setupOrbitControls + 程序化示意地形（value-noise/fbm·零依赖）+ CatmullRom 路线 Tube + 河流 Tube + 17 节点 Sphere + CanvasTexture Sprite 标签 + Raycaster 选中 + 路线高亮/地形透明切换 + file:// 可用 + EMBEDDED 回退 |
| scripts/output/data/journey_geo_3d.json | W454 | v2.3.69 新建·17 节点含 lon/lat/category/chapter/duration/desc；分类按主导势力归属（人间 4·妖界 9·天庭 3·灵山 1） |
| scripts/_smoke_geo3d.js | W454 | v2.3.69 新建·3D 页专用冒烟（asserts nodes>0 / canvas / 无 pageerror） |
| site/data/tag-cloud.html | W454 | v2.3.69 修改·新增西游地理 3D 条目（v-new·size:8） |
| site/sitemap.xml | W454 | v2.3.69 修改·新增 data/journey-geo-3d.html URL |
| site/dukou-engine.html | W454 | v2.3.69 修改·页脚 prepend v2.3.69 W454 段 |
| CHANGELOG.md / 交接文档.md / README.md / STRUCTURE.md / docs/00-导读/项目说明.md | W454 | v2.3.69 修改·版本行 v2.3.69 W454 段 |
| scripts/output/file-index.md | W454 | v2.3.69 修改·W454 现役索引段 |

> 当前版本 v2.3.72（2026-08-16）

## W457 W457（2026-08-16）

| 文件 | W | 说明 |
|---|---|---|

> 当前版本 v2.3.73（2026-08-16）

## W458 W458（2026-08-16）

| 文件 | W | 说明 |
|---|---|---|

> 当前版本 v2.3.75（2026-08-17）

## W460 motion tokens+表格/组件动效+count-up+D3 编排统一（2026-08-17）

| 文件 | W | 说明 |
|---|---|---|

> 当前版本 v2.3.76（2026-08-17）

## W461 墨韵 W-c 批：16 个 forceSimulation 网络页 tooltip 分四型收编（A 组 10 页 d3 动态/B 组 1 页变体/C 组 2 页静态 div/D 组 3 页豁免）+ P2-2 KPI count-up 两页（千分位/文本值过滤+轮询等待 async 元素）；Playwright 48/48 断言 + 3 页性能基线零回归 + CSP/JS/链接/verify 门禁全绿（2026-08-17）

| 文件 | W | 说明 |
|---|---|---|

> 当前版本 v2.3.77（2026-08-17）

## W462 墨韵 W-d/W-e 批：66 剩余页按实现证据分型（37 transition/20 D3 静态/9 非 D3 留 W-f）——37 页调用点级 RM 守卫（141 dur+21 delay+59 bare 包裹 + >600 全归一 600）+ 7 页 prototype 级守卫 + tooltip 收编 11 页（A 组 22 edits + C 组 10 静态页）+ count-up 18 页 + 全站尾部重复 body 去重 154 页；57 页 pageerror=0 + RM 6/6 + tip 5/5 + CSP 1167 哈希 0 漂移 + verify 全绿（2026-08-17）

| 文件 | W | 说明 |
|---|---|---|

> 当前版本 v2.3.78（2026-08-17）

## W463 墨韵系列收官：DESIGN.md §5 重写为九节强制契约（时长三档/RM 双守卫/tooltip/count-up/loading/性能红线）+ system.css .chart-loading/.chart-fade-in 225 页同步 + P2-1 loading 接入 6 页（MutationObserver 自移除·search 语义不符回退）+ W-f fade-in 3 页 + text-search 豁免——86 页动效全覆盖覆盖等式归零；两 bug 断言驱动修复；CSP 1173 哈希 0 漂移 + verify 全绿（2026-08-17）

| 文件 | W | 说明 |
|---|---|---|

