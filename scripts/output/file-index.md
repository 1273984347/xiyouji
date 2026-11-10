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

## W1176 术语表可视化页（2026-11-08）

| 文件 | W | 说明 |
|---|---|---|
| site/data/glossary.html | W1176 | 新建：术语表速查页（KPI 四卡 + 6 组筛选 + 搜索 + 59 术语卡 + 对照表） |
| site/_template.html | W1176 | 改：说明注释里的 `<script>` 字面量改为「script 标签」（防被解析器当真标签） |
| scripts/check_glossary.py | W1176 | 改：parse_md 保留「含义/出处说明/书中用法」列（原只取前 1-2 列） |
| dataset/glossary.json | W1176 | 改：重生成（6 组 59 条·含完整三列） |
| scripts/_w1176_glossary_page.py | W1176 | 新建：术语页内容填充脚本 |
| scripts/output/colorblind-baseline.txt | W1176 | 改：色盲基线重冻结（+847 新页配对·其余零变化） |
| site/sitemap.xml | W1176 | 改：补 data/glossary.html |
| docs/00-导读/W批次编号对账表.md | W1176 | 改：W1176 认领行 |
| scripts/output/_w1176_spec.json | W1176 | 新建：本批 spec |
| scripts/output/_cascade_files_W1176.txt | W1176 | 新建：级联清单 |
| CHANGELOG.md | W1176 | 改：W1176 段落（级联） |
| scripts/output/file-index.md | W1176 | 改：W1176 段（级联） |
| site/（5 件） | W1176 | 搜索索引重生成 + CSP 重哈希 + 页脚版本推进 |
| site/data/（89 件） | W1176 | CSP 重哈希 + 导航/徽标注入（幂等·实际改动仅新页） |
| .github/workflows/README.md | W1176 | 改：区间行推进（版本面） |
| CITATION.cff | W1176 | 改：version/date 推进（级联） |
| README.md | W1176 | 改：版本行推进（级联） |
| STRUCTURE.md | W1176 | 改：版本行推进（级联） |
| HANDOVER.md | W1176 | 改：最后更新行 + 当前进度（级联） |
| AGENTS.md | W1176 | 改：脚注沿革滚动（级联） |
| archive/docs/AGENTS-ARCHIVE.md | W1176 | 改：脚注沿革滚动（级联） |
| archive/docs/workflows-readme-history.md | W1176 | 改：逐批明细追加（W1176·级联） |
| docs/00-导读/项目说明.md | W1176 | 改：版本行推进（级联） |
| scripts/output/stats.json | W1176 | 改：stats 刷新（级联） |
| scripts/output/INDEX.md | W1176 | 改：再生成/验证缓存（级联） |
| scripts/output/README.md | W1176 | 改：再生成/验证缓存（级联） |
| scripts/output/_vermilion_solid_cache.json | W1176 | 改：再生成/验证缓存（级联） |
| scripts/output/tools-inventory.md | W1176 | 改：再生成/验证缓存（级联） |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1176 | 改：级联/目录刷新产物 |
| scripts/INDEX.md | W1176 | 改：级联/目录刷新产物 |
| scripts/output/_vermilion_solid_report.json | W1176 | 改：级联/目录刷新产物 |
| scripts/output/_w1167_nav_plan.json | W1176 | 改：级联/目录刷新产物 |
| scripts/output/citability-report.json | W1176 | 改：级联/目录刷新产物 |
| archive/scripts/batches/w1175/_w1175_datasource_wording.py | W1176 | 改：级联/修复产物 |
| dataset/README.md | W1176 | 改：级联/修复产物 |
| docs/00-导读/统计口径说明.md | W1176 | 改：级联/修复产物 |
| docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md | W1176 | 改：级联/修复产物 |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1176 | 改：级联/修复产物 |
| docs/agent/gates.md | W1176 | 改：级联/修复产物 |
| scripts/output/stats-changelog.json | W1176 | 改：级联/修复产物 |
| scripts/output/stats-index.md | W1176 | 改：级联/修复产物 |
| scripts/_w1175_datasource_wording.py | W1176 | 删：W1175 一次性脚本归档迁入 archive/scripts/batches/w1175/ |
| archive/scripts/batches/INDEX.md | W1176 | 改：修复产物 |
| archive/scripts/batches/README.md | W1176 | 改：修复产物 |
| archive/scripts/batches/w1175/INDEX.md | W1176 | 改：修复产物 |
| archive/scripts/batches/w1175/README.md | W1176 | 改：修复产物 |

## W1175 方案 §7 核验订正批（2026-11-08）

| 文件 | W | 说明 |
|---|---|---|
| docs/11-方案报告/设计与架构方案/全站改版方案与门禁扩展-v5-2026-11-08.md | W1175 | 改：§7 四条逐条复算订正 + 核验纪律 + 同批补记 W1172-W1174 真缺陷 |
| docs/00-导读/W批次编号对账表.md | W1175 | 改：W1175 认领行 |
| scripts/output/_w1175_spec.json | W1175 | 新建：本批 spec |
| scripts/output/_cascade_files_W1175.txt | W1175 | 新建：级联清单 |
| CHANGELOG.md | W1175 | 改：W1175 段落（级联） |
| scripts/output/file-index.md | W1175 | 改：W1175 段（级联） |
| .github/workflows/README.md | W1175 | 改：区间行推进（版本面） |
| CITATION.cff | W1175 | 改：version/date 推进（级联） |
| README.md | W1175 | 改：版本行推进（级联） |
| STRUCTURE.md | W1175 | 改：版本行推进（级联） |
| HANDOVER.md | W1175 | 改：最后更新行 + 当前进度（级联） |
| AGENTS.md | W1175 | 改：脚注沿革滚动（级联） |
| archive/docs/AGENTS-ARCHIVE.md | W1175 | 改：脚注沿革滚动（级联） |
| archive/docs/workflows-readme-history.md | W1175 | 改：逐批明细追加（W1175·级联） |
| docs/00-导读/项目说明.md | W1175 | 改：版本行推进（级联） |
| scripts/output/stats.json | W1175 | 改：stats 刷新（级联） |
| scripts/output/INDEX.md | W1175 | 改：再生成/验证缓存（级联） |
| scripts/output/README.md | W1175 | 改：再生成/验证缓存（级联） |
| scripts/output/_vermilion_solid_cache.json | W1175 | 改：再生成/验证缓存（级联） |
| scripts/output/tools-inventory.md | W1175 | 改：再生成/验证缓存（级联） |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1175 | 改：级联/目录刷新产物 |
| site/data/cross-time-danmaku.html | W1175 | 改：级联/目录刷新产物 |
| site/data/tag-cloud.html | W1175 | 改：级联/目录刷新产物 |
| site/dukou-engine.html | W1175 | 改：级联/目录刷新产物 |
| site/index.html | W1175 | 改：级联/目录刷新产物 |

## W1174 移动端全量确认 + 数据源表述统一批（2026-11-08）

| 文件 | W | 说明 |
|---|---|---|
| scripts/_w1175_datasource_wording.py | W1174 | 新建：数据源前缀词统一脚本（三重防线·逐层补映射） |
| scripts/output/mobile_viewport_report.json | W1174 | 改：375px 报告升级为全量 859 页（FAIL 0） |
| scripts/output/mobile_viewport_report_320.json | W1174 | 改：320px 报告升级为全量 859 页（FAIL 0） |
| site/data/（89 件） | W1174 | 改：数据源前缀词统一 30 页 32 处 + 搜索索引/CSP 跟随 |
| docs/00-导读/W批次编号对账表.md | W1174 | 改：W1174 认领行 |
| scripts/output/_w1174_spec.json | W1174 | 新建：本批 spec |
| scripts/output/_cascade_files_W1174.txt | W1174 | 新建：级联清单 |
| CHANGELOG.md | W1174 | 改：W1174 段落（级联） |
| scripts/output/file-index.md | W1174 | 改：W1174 段（级联） |
| site/（3 件） | W1174 | 搜索索引重生成（search 页内嵌索引跟随） |
| .github/workflows/README.md | W1174 | 改：区间行推进（版本面） |
| CITATION.cff | W1174 | 改：version/date 推进（级联） |
| README.md | W1174 | 改：版本行推进（级联） |
| STRUCTURE.md | W1174 | 改：版本行推进（级联） |
| HANDOVER.md | W1174 | 改：最后更新行 + 当前进度（级联） |
| AGENTS.md | W1174 | 改：脚注沿革滚动（级联） |
| archive/docs/AGENTS-ARCHIVE.md | W1174 | 改：脚注沿革滚动（级联） |
| archive/docs/workflows-readme-history.md | W1174 | 改：逐批明细追加（W1174·级联） |
| docs/00-导读/项目说明.md | W1174 | 改：版本行推进（级联） |
| scripts/output/stats.json | W1174 | 改：stats 刷新（级联） |
| scripts/output/INDEX.md | W1174 | 改：再生成/验证缓存（级联） |
| scripts/output/README.md | W1174 | 改：再生成/验证缓存（级联） |
| scripts/output/_vermilion_solid_cache.json | W1174 | 改：再生成/验证缓存（级联） |
| scripts/output/tools-inventory.md | W1174 | 改：再生成/验证缓存（级联） |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1174 | 改：级联/目录刷新产物 |
| scripts/INDEX.md | W1174 | 改：级联/目录刷新产物 |
| scripts/output/citability-report.json | W1174 | 改：级联/目录刷新产物 |

## W1173 移动端覆盖面与视口补齐批（2026-11-08）

| 文件 | W | 说明 |
|---|---|---|
| scripts/mobile_viewport_probe.py | W1173 | 改：list_pages 加 scope(+en/reader/all) 与 reader_sample 抽样·修正 reader 子目录递归遗漏 |
| scripts/check_mobile_viewport.py | W1173 | 改：B 层加 B3 采信 320px 报告（FAIL 须 0·缺失仅 NOTE） |
| site/system.css | W1173 | 改：移动端补 button{min-height:24px}（W1165 规则漏 button） |
| scripts/output/mobile_viewport_report_320.json | W1173 | 新建：320px 三目录报告（268 页·FAIL 0） |
| scripts/output/mobile_viewport_report.json | W1173 | 改：375px 重跑为三目录口径（268 页·FAIL 0） |
| AGENTS.md | W1173 | 改：第 64 槽 B 层补 320 采信与双盲区说明 |
| docs/agent/gates.md | W1173 | 改：第 64 槽补 W1173 双盲区段落 |
| docs/00-导读/W批次编号对账表.md | W1173 | 改：W1173 认领行 |
| scripts/output/_w1173_spec.json | W1173 | 新建：本批 spec |
| scripts/output/_cascade_files_W1173.txt | W1173 | 新建：级联清单 |
| CHANGELOG.md | W1173 | 改：W1173 段落（级联） |
| scripts/output/file-index.md | W1173 | 改：W1173 段（级联） |
| site/（3 件） | W1173 | inline_css 副本同步（button 规则传播） |
| site/data/（89 件） | W1173 | inline_css 副本同步（同上·W1142 分组登记） |
| site/en/（138 件） | W1173 | inline_css 副本同步（同上·W1142 分组登记） |
| site/reader/（622 件） | W1173 | inline_css 副本同步（同上·W1142 分组登记） |
| .github/workflows/README.md | W1173 | 改：区间行推进（版本面） |
| CITATION.cff | W1173 | 改：version/date 推进（级联） |
| README.md | W1173 | 改：版本行推进（级联） |
| STRUCTURE.md | W1173 | 改：版本行推进（级联） |
| HANDOVER.md | W1173 | 改：最后更新行 + 当前进度（级联） |
| archive/docs/AGENTS-ARCHIVE.md | W1173 | 改：脚注沿革滚动（级联） |
| archive/docs/workflows-readme-history.md | W1173 | 改：逐批明细追加（W1173·级联） |
| docs/00-导读/项目说明.md | W1173 | 改：版本行推进（级联） |
| scripts/output/stats.json | W1173 | 改：stats 刷新（级联） |
| scripts/output/INDEX.md | W1173 | 改：再生成/验证缓存（级联） |
| scripts/output/README.md | W1173 | 改：再生成/验证缓存（级联） |
| scripts/output/_vermilion_solid_cache.json | W1173 | 改：再生成/验证缓存（级联） |
| scripts/output/tools-inventory.md | W1173 | 改：再生成/验证缓存（级联） |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1173 | 改：级联/目录刷新产物 |

## W1172 表格窄屏溢出根修批（2026-11-08）

| 文件 | W | 说明 |
|---|---|---|
| site/system.css | W1172 | 改：移动端块加 table{display:block;overflow-x:auto}（宽表格横向滚动·断点 640） |
| docs/00-导读/W批次编号对账表.md | W1172 | 改：W1172 认领行 |
| scripts/output/_w1172_spec.json | W1172 | 新建：本批 spec |
| scripts/output/_cascade_files_W1172.txt | W1172 | 新建：级联清单 |
| CHANGELOG.md | W1172 | 改：W1172 段落（级联） |
| scripts/output/file-index.md | W1172 | 改：W1172 段（级联） |
| site/（3 件） | W1172 | inline_css 副本同步（table 规则传播·_template/dukou-engine/search） |
| site/data/（89 件） | W1172 | inline_css 副本同步（同上·W1142 分组登记） |
| site/en/（138 件） | W1172 | inline_css 副本同步（同上·W1142 分组登记） |
| site/reader/（622 件） | W1172 | inline_css 副本同步（同上·W1142 分组登记） |
| .github/workflows/README.md | W1172 | 改：区间行推进（版本面） |
| CITATION.cff | W1172 | 改：version/date 推进（级联） |
| README.md | W1172 | 改：版本行推进（级联） |
| STRUCTURE.md | W1172 | 改：版本行推进（级联） |
| HANDOVER.md | W1172 | 改：最后更新行 + 当前进度（级联） |
| AGENTS.md | W1172 | 改：脚注沿革滚动（级联） |
| archive/docs/AGENTS-ARCHIVE.md | W1172 | 改：脚注沿革滚动（级联） |
| archive/docs/workflows-readme-history.md | W1172 | 改：逐批明细追加（W1172·级联） |
| docs/00-导读/项目说明.md | W1172 | 改：版本行推进（级联） |
| scripts/output/stats.json | W1172 | 改：stats 刷新（级联） |
| scripts/output/INDEX.md | W1172 | 改：再生成/验证缓存（级联） |
| scripts/output/README.md | W1172 | 改：再生成/验证缓存（级联） |
| scripts/output/_vermilion_solid_cache.json | W1172 | 改：再生成/验证缓存（级联） |
| scripts/output/tools-inventory.md | W1172 | 改：再生成/验证缓存（级联） |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1172 | 改：级联/目录刷新产物 |
| scripts/output/mobile_viewport_report_320.json | W1172 | 改：级联/目录刷新产物 |

## W1171 坑表补强批（2026-11-08）

| 文件 | W | 说明 |
|---|---|---|
| pitfalls.md | W1171 | 改：E-11 补第三种形态（Python 默认 CRLF）+ 新增 E-211 元教训 + 流程段 171→172 |
| AGENTS.md | W1171 | 改：坑表计数 304→305 + 分项 171→172 |
| HANDOVER.md | W1171 | 改：坑表计数 304→305（两处）+ 最后更新行 + 当前进度（级联） |
| .agent/skills/puti-shouye/SKILL.md | W1171 | 改：坑表计数 304→305（两处） |
| docs/00-导读/W批次编号对账表.md | W1171 | 改：W1171 认领行 |
| scripts/output/_w1171_spec.json | W1171 | 新建：本批 spec |
| scripts/output/_cascade_files_W1171.txt | W1171 | 新建：级联清单 |
| CHANGELOG.md | W1171 | 改：W1171 段落（级联） |
| scripts/output/file-index.md | W1171 | 改：W1171 段（级联） |
| .github/workflows/README.md | W1171 | 改：区间行推进（版本面） |
| CITATION.cff | W1171 | 改：version/date 推进（级联） |
| README.md | W1171 | 改：版本行推进（级联） |
| STRUCTURE.md | W1171 | 改：版本行推进（级联） |
| docs/00-导读/项目说明.md | W1171 | 改：版本行推进（级联） |
| archive/docs/workflows-readme-history.md | W1171 | 改：逐批明细追加（W1171·级联） |
| archive/docs/AGENTS-ARCHIVE.md | W1171 | 改：级联/目录刷新产物 |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1171 | 改：级联/目录刷新产物 |
| archive/scripts/batches/w1169/INDEX.md | W1171 | 改：级联/目录刷新产物 |
| scripts/output/INDEX.md | W1171 | 改：级联/目录刷新产物 |
| scripts/output/README.md | W1171 | 改：级联/目录刷新产物 |
| scripts/output/stats.json | W1171 | 改：级联/目录刷新产物 |
| scripts/output/tools-inventory.md | W1171 | 改：级联/目录刷新产物 |
| site/data/cross-time-danmaku.html | W1171 | 改：级联/目录刷新产物 |
| site/data/tag-cloud.html | W1171 | 改：级联/目录刷新产物 |
| site/dukou-engine.html | W1171 | 改：级联/目录刷新产物 |
| site/index.html | W1171 | 改：级联/目录刷新产物 |

## W1170 dashboard KPI 对拍批（2026-11-08）

| 文件 | W | 说明 |
|---|---|---|
| site/dashboard.html | W1170 | 改：A2-A6 五张 KPI 卡片值对齐 stats.json + 段落合计 615→616、A5 34→35 |
| scripts/check_dashboard_kpi.py | W1170 | 新建：第 68 槽（C1 卡片存在性 / C2 值与 stats 一致 / C3 段落合计·自测 4 例） |
| scripts/verify_delivery.py | W1170 | 改：挂第 68 槽 + EXPECTED_SECTION_NAMES + _SCOPE_CORE 登记 |
| AGENTS.md | W1170 | 改：§4.2 第 68 条摘要 + 槽数 67→68（三处） |
| docs/agent/gates.md | W1170 | 改：第 68 条完整定义 + 标题槽数与沿革 |
| docs/00-导读/文档规范.md | W1170 | 改：verify full 现役段数 69→73 |
| HANDOVER.md | W1170 | 改：六十七槽→六十八槽 + 最后更新行 + 当前进度（级联） |
| docs/00-导读/W批次编号对账表.md | W1170 | 改：W1170 认领行 |
| scripts/output/_w1170_spec.json | W1170 | 新建：本批 spec |
| scripts/output/_cascade_files_W1170.txt | W1170 | 新建：级联清单 |
| CHANGELOG.md | W1170 | 改：W1170 段落（级联） |
| scripts/output/file-index.md | W1170 | 改：W1170 段（级联） |
| .github/workflows/README.md | W1170 | 改：区间行推进（版本面） |
| CITATION.cff | W1170 | 改：version/date 推进（级联） |
| README.md | W1170 | 改：版本行推进（级联） |
| STRUCTURE.md | W1170 | 改：版本行推进（级联） |
| archive/docs/AGENTS-ARCHIVE.md | W1170 | 改：脚注沿革滚动（级联） |
| archive/docs/workflows-readme-history.md | W1170 | 改：逐批明细追加（W1170·级联） |
| docs/00-导读/项目说明.md | W1170 | 改：版本行推进（级联） |
| scripts/output/stats.json | W1170 | 改：stats 刷新（gate_count 67→68） |
| scripts/output/stats-changelog.json | W1170 | 改：stats 生成件跟随 |
| scripts/output/stats-index.md | W1170 | 改：stats 生成件跟随 |
| scripts/output/INDEX.md | W1170 | 改：再生成/验证缓存（级联） |
| scripts/output/README.md | W1170 | 改：再生成/验证缓存（级联） |
| scripts/output/_vermilion_solid_cache.json | W1170 | 改：再生成/验证缓存（级联） |
| scripts/output/tools-inventory.md | W1170 | 改：再生成/验证缓存（级联） |
| scripts/INDEX.md | W1170 | 改：目录清单刷新（新增 check_dashboard_kpi.py） |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1170 | 改：台账腾窗迁出（号序切分） |
| docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md | W1170 | 改：stats 标记 gate_count 67→68 |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1170 | 改：stats 标记 gate_count 67→68（同上） |
| pytest.ini | W1170 | 改：stats 标记 pytest_collected 跟随刷新 |
| site/data/cross-time-danmaku.html | W1170 | 改：级联产物（页脚版本推进 / 标注跟随） |
| site/data/tag-cloud.html | W1170 | 改：级联产物（页脚版本推进 / 标注跟随） |
| site/dukou-engine.html | W1170 | 改：级联产物（页脚版本推进 / 标注跟随） |
| site/index.html | W1170 | 改：级联产物（页脚版本推进 / 标注跟随） |
| archive/scripts/batches/w1169/_w1169_touch_events.py | W1170 | 改：级联/归档产物（页脚版本推进·W1169 一次性脚本归档） |
| site/data/search.html | W1170 | 改：级联/归档产物（页脚版本推进·W1169 一次性脚本归档） |
| site/en/search.html | W1170 | 改：级联/归档产物（页脚版本推进·W1169 一次性脚本归档） |
| scripts/_w1169_touch_events.py | W1170 | 删：W1169 一次性改造脚本归档迁入 archive/scripts/batches/w1169/ |
| archive/scripts/batches/INDEX.md | W1170 | 改：目录清单刷新（归档迁入后的目录文档） |
| archive/scripts/batches/README.md | W1170 | 改：目录清单刷新（归档迁入后的目录文档） |
| archive/scripts/batches/w1169/INDEX.md | W1170 | 改：目录清单刷新（归档迁入后的目录文档） |
| archive/scripts/batches/w1169/README.md | W1170 | 改：目录清单刷新（归档迁入后的目录文档） |

## W1169 图表触摸交互批（2026-11-08）

| 文件 | W | 说明 |
|---|---|---|
| site/data/chapter-stats.html | W1169 | 改：3 组 tooltip 事件 mousemove/mouseleave → pointer* |
| site/data/story-timeline.html | W1169 | 改：mouseover/mouseout → pointerover/pointerout |
| site/data/tag-cloud.html | W1169 | 改：mousemove/mouseleave/mouseenter → pointer* |
| site/data/timeline.html | W1169 | 改：2 组 mousemove/mouseleave/mouseenter → pointer* |
| site/data/cross-time-danmaku.html | W1169 | 改：2 组 mousemove/mouseleave/mouseenter → pointer* |
| scripts/_w1169_touch_events.py | W1169 | 新建：一次性改造脚本（锚点预检 + 替换断言·三重防线） |
| docs/00-导读/W批次编号对账表.md | W1169 | 改：W1169 认领行 |
| CHANGELOG.md | W1169 | 改：W1169 段落（级联） |
| HANDOVER.md | W1169 | 改：最后更新行 + 当前进度（级联） |
| scripts/output/_w1169_spec.json | W1169 | 新建：本批 spec |
| scripts/output/file-index.md | W1169 | 改：W1169 段（级联） |
| scripts/output/_cascade_files_W1169.txt | W1169 | 新建：级联清单 |
| .github/workflows/README.md | W1169 | 改：区间行推进（版本面） |
| CITATION.cff | W1169 | 改：version/date 推进（级联） |
| README.md | W1169 | 改：版本行推进（级联） |
| STRUCTURE.md | W1169 | 改：版本行推进（级联） |
| archive/docs/AGENTS-ARCHIVE.md | W1169 | 改：脚注沿革滚动（级联） |
| archive/docs/workflows-readme-history.md | W1169 | 改：逐批明细追加（W1169·级联） |
| docs/00-导读/项目说明.md | W1169 | 改：版本行推进（级联） |
| scripts/output/stats.json | W1169 | 改：stats 刷新（级联） |
| scripts/output/INDEX.md | W1169 | 改：再生成/验证缓存（级联） |
| scripts/output/README.md | W1169 | 改：再生成/验证缓存（级联） |
| scripts/output/_vermilion_solid_cache.json | W1169 | 改：再生成/验证缓存（级联） |
| scripts/output/tools-inventory.md | W1169 | 改：再生成/验证缓存（级联） |
| AGENTS.md | W1169 | 改：脚注沿革滚动（级联） |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1169 | 改：台账腾窗迁出（号序切分） |
| site/dukou-engine.html | W1169 | 改：页脚版本推进（级联） |
| site/index.html | W1169 | 改：页脚版本推进（级联） |
| scripts/INDEX.md | W1169 | 改：目录清单刷新（新增改造脚本·gen_folder_docs --refresh） |

## W1168 统计单轨收敛批（2026-11-08）

| 文件 | W | 说明 |
|---|---|---|
| .agent/skills/puti-shouye/（1 件） | W1168 | 改：坑表总数引用同步 304 条 |
| docs/（1 件） | W1168 | 改：收官链级联写入（六文档同步 / 台账 / 索引） |
| docs/00-导读/（2 件） | W1168 | 改：stats 计数标记随实算刷新（gate_count 66→67 / pyt |
| docs/11-方案报告/设计与架构方案/（1 件） | W1168 | 改：W1168 续批留痕（§2 决策台账 G0-1-R·§4.1 第 67 槽五 |
| docs/agent/（1 件） | W1168 | 改：标题沿革 66→67 槽 + 第 67 槽全量定义（含 C6 运行层） |
| scripts/（6 件） | W1168 | 改：具名例外域 4→1（EXTERNAL_SCRIPT_HOSTS 归空集 +  |
| scripts/output/（8 件） | W1168 | 改：ga4_measurement_id 由待填项降为退役说明位（_note 写 |
| site/（12 件） | W1168 | 改：统计块迁移 ANALYTICS v2 单轨 + stats.js 桥随块分发 |
| site/data/（89 件） | W1168 | 改：统计块迁移 ANALYTICS v2 单轨 + stats.js 桥随块分发 |
| site/en/（138 件） | W1168 | 改：统计块迁移 ANALYTICS v2 单轨 + stats.js 桥随块分发 |
| site/js/（3 件） | W1168 | 改：reader_progress 档位上报（25/50/75/100 每访问每 |
| site/reader/（102 件） | W1168 | 改：统计块迁移 ANALYTICS v2 单轨 + stats.js 桥随块分发 |
| site/reader/culture/（36 件） | W1168 | 改：统计块迁移 ANALYTICS v2 单轨 + stats.js 桥随块分发 |
| site/reader/essays/（45 件） | W1168 | 改：统计块迁移 ANALYTICS v2 单轨 + stats.js 桥随块分发 |
| site/reader/people/（216 件） | W1168 | 改：统计块迁移 ANALYTICS v2 单轨 + stats.js 桥随块分发 |
| site/reader/poetry/（14 件） | W1168 | 改：统计块迁移 ANALYTICS v2 单轨 + stats.js 桥随块分发 |
| site/reader/themes/（210 件） | W1168 | 改：统计块迁移 ANALYTICS v2 单轨 + stats.js 桥随块分发 |
| site/static/js/（3 件） | W1168 | 改：copy_citation 上报（只报页标识，不回传引文内容） |
| tests/unit/（1 件） | W1168 | 新建：第 67 槽 + 桥 + CSP 单域 + 探针分层 23 例（含 N11 |
| AGENTS.md | W1168 | 改：铁律 5 例外域收缩为单域 + §4.2 计数 66→67 + 条目 67 摘要 + 坑位计数五面 |
| HANDOVER.md | W1168 | 改：槽数与坑数引用（六十七槽 / 304 条） |
| pitfalls.md | W1168 | 改：W1168 新形态 7 条（E-204~E-210·仪器单源/读错层/gitignore 硬判据/死轨待填位/夹具落点面/分支未覆盖/node 桩全局） |
| CHANGELOG.md | W1168 | 改：收官链级联写入（六文档同步 / 台账 / 索引） |
| README.md | W1168 | 改：收官链级联写入（六文档同步 / 台账 / 索引） |
| STRUCTURE.md | W1168 | 改：收官链级联写入（六文档同步 / 台账 / 索引） |
| pytest.ini | W1168 | 改：收官链级联写入（六文档同步 / 台账 / 索引） |

## W1167 MVP 迁移批（2026-11-08）

| 文件 | W | 说明 |
|---|---|---|
| .agent/skills/puti-shouye/（1 件） | W1167 | 改：随本批级联刷新 |
| .github/workflows/（1 件） | W1167 | 改：随本批级联刷新 |
| archive/docs/（3 件） | W1167 | 改：归档面随级联刷新 |
| docs/（1 件） | W1167 | 改：stats 计数标记随实算刷新（gate_count 64→66 / pyt |
| docs/00-导读/（3 件） | W1167 | 改：stats 计数标记随实算刷新（gate_count 64→66 / pyt |
| docs/11-方案报告/（1 件） | W1167 | 改：stats 计数标记随实算刷新（gate_count 64→66 / pyt |
| docs/11-方案报告/设计与架构方案/（3 件） | W1167 | 新建：改版方案仓内正本（决策台账 G0-1/2·Ask1/2/4·六项实况·门禁 |
| docs/agent/（1 件） | W1167 | 改：stats 计数标记随实算刷新（gate_count 64→66 / pyt |
| scripts/（12 件） | W1167 | 改：随本批级联刷新 |
| scripts/output/（12 件） | W1167 | 改：门禁/统计生成产物刷新（stats / 缓存 / 计划面） |
| site/（12 件） | W1167 | 改：导航正本分发（含 nav_click 埋点属性）+ 三态数据徽标 + 双轨统 |
| site/data/（89 件） | W1167 | 改：导航正本分发（含 nav_click 埋点属性）+ 三态数据徽标 + 双轨统 |
| site/en/（138 件） | W1167 | 改：导航正本分发（含 nav_click 埋点属性）+ 三态数据徽标 + 双轨统 |
| site/js/（2 件） | W1167 | 改：上报通道注释「统计链已退役」失真订正 + 与注入轨不重复计数声明 |
| site/reader/（102 件） | W1167 | 改：导航正本分发（含 nav_click 埋点属性）+ 三态数据徽标 + 双轨统 |
| site/reader/culture/（36 件） | W1167 | 改：导航正本分发（含 nav_click 埋点属性）+ 三态数据徽标 + 双轨统 |
| site/reader/essays/（45 件） | W1167 | 改：导航正本分发（含 nav_click 埋点属性）+ 三态数据徽标 + 双轨统 |
| site/reader/people/（216 件） | W1167 | 改：导航正本分发（含 nav_click 埋点属性）+ 三态数据徽标 + 双轨统 |
| site/reader/poetry/（14 件） | W1167 | 改：导航正本分发（含 nav_click 埋点属性）+ 三态数据徽标 + 双轨统 |
| site/reader/themes/（210 件） | W1167 | 改：导航正本分发（含 nav_click 埋点属性）+ 三态数据徽标 + 双轨统 |
| site/static/js/（3 件） | W1167 | 改：随本批级联刷新 |
| tests/unit/（5 件） | W1167 | 改：随本批级联刷新 |
| .gitignore | W1167 | 改：spark-output/ 工作目录不入库（改版方案正本已落 docs/11-方案报告，链路产物不作规则载体） |
| AGENTS.md | W1167 | 改：随本批级联刷新 |
| CHANGELOG.md | W1167 | 改：随本批级联刷新 |
| CITATION.cff | W1167 | 改：随本批级联刷新 |
| HANDOVER.md | W1167 | 改：随本批级联刷新 |
| README.md | W1167 | 改：随本批级联刷新 |
| STRUCTURE.md | W1167 | 改：随本批级联刷新 |
| pitfalls.md | W1167 | 改：随本批级联刷新 |
| pytest.ini | W1167 | 改：pytest collected 计数标记刷新 |

## W1166 移动端收尾微批（2026-11-07）

| 文件 | W | 说明 |
|---|---|---|
| site/system.css | W1166 | 改：移动端 .site-footer 安全区（80px + body:has(.rag-fab) 104px）+ 纯视觉图例项 min-height 32px |
| scripts/check_mobile_viewport.py | W1166 | 改：A6 页脚安全区契约（padding-bottom≥54px）+ 自测 5→6 例 |
| AGENTS.md | W1166 | 改：第 64 槽摘要补 A6 与自测例数 |
| docs/agent/gates.md | W1166 | 改：第 64 槽 A6 判据与自测 6 例、契约数 5→6 |
| docs/00-导读/文档规范.md | W1166 | 改：verify full 现役段数 68→69（W1165 挂第 64 槽后实况） |
| HANDOVER.md | W1166 | 改：里程碑滚动淘汰最老块 + 最后更新行 + 当前进度 |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1166 | 改：台账腾窗迁入 W1104（archive_ledger_rows 号序切分） |
| docs/00-导读/W批次编号对账表.md | W1166 | 改：W1166 认领行 + W1165 收官回填（b64a4435） |
| scripts/output/_w1166_spec.json | W1166 | 新建：本批 spec |
| scripts/output/_cascade_files_W1166.txt | W1166 | 新建：级联清单 |
| scripts/output/_cascade_files_W1165.txt | W1166 | 改：里程碑滚动清单同步 |
| scripts/output/mobile_viewport_report.json | W1166 | 改：探针复跑（FAIL 0 无回归） |
| site/（3 件） | W1166 | inline_css 副本同步 + 搜索索引重生成（_template.html / dukou-engine.html / search.html） |
| site/data/（89 件） | W1166 | inline_css 副本同步（同上·W1142 分组登记） |
| site/en/（138 件） | W1166 | inline_css 副本同步（同上·W1142 分组登记） |
| site/reader/（622 件） | W1166 | inline_css 副本同步（同上·W1142 分组登记） |
| CHANGELOG.md | W1166 | 改：W1166 段落（级联） |
| scripts/output/file-index.md | W1166 | 改：W1166 段（级联） |
| .github/workflows/README.md | W1166 | 改：区间行推进（版本面） |
| CITATION.cff | W1166 | 改：version/date 推进（级联） |
| README.md | W1166 | 改：版本行推进（级联） |
| STRUCTURE.md | W1166 | 改：版本行推进（级联） |
| archive/docs/AGENTS-ARCHIVE.md | W1166 | 改：脚注沿革滚动（级联） |
| archive/docs/workflows-readme-history.md | W1166 | 改：逐批明细追加（W1166·级联） |
| docs/00-导读/项目说明.md | W1166 | 改：版本行推进（级联） |
| scripts/output/stats.json | W1166 | 改：stats 刷新（级联） |
| scripts/output/INDEX.md | W1166 | 改：再生成/验证缓存（级联） |
| scripts/output/README.md | W1166 | 改：再生成/验证缓存（级联） |
| scripts/output/_vermilion_solid_cache.json | W1166 | 改：再生成/验证缓存（级联） |
| scripts/output/tools-inventory.md | W1166 | 改：再生成/验证缓存（级联） |

## W1165 V4 移动端 375px 回归批（2026-11-07）

| 文件 | W | 说明 |
|---|---|---|
| scripts/mobile_viewport_probe.py | W1165 | 新建：375px 视口探针（四类判据·file:// 加载·自测 9 例） |
| scripts/check_mobile_viewport.py | W1165 | 新建：第 64 槽（A 层 5 项静态契约 + B 层报告采信·自测 5 例） |
| scripts/verify_delivery.py | W1165 | 改：挂第 64 槽 + EXPECTED_SECTION_NAMES 加「移动视口」+ _SCOPE_CORE 登记 |
| site/system.css | W1165 | 改：cite 组件段新增（样式自 JS 归位）+ 页脚 nav flex-wrap/nowrap + 移动端图例与表单触摸尺寸 |
| site/static/js/cite-box.js | W1165 | 改：剥离 CSS 注入（样式归位 system.css），仅保留复制交互 |
| site/dashboard.html | W1165 | 改：私有 .flinks 页脚触摸尺寸（外链 CSS 页不走内联） |
| site/data/pilgrim-team-dynamic-network.html | W1165 | 改：.phase-timeline 窄屏 5 列→2 列（375px 下卡片溢出被裁剪） |
| scripts/output/mobile_viewport_report.json | W1165 | 新建：探针全量报告（99 页终值 FAIL 0） |
| tests/unit/test_w1165_mobile_viewport.py | W1165 | 新建：13 例回归锁（探针分级语义 / 门禁解析器两处缺陷形态 / 仓库契约） |
| site/（3 件） | W1165 | inline_css 副本同步 + 搜索索引重生成（_template.html / dukou-engine.html / search.html） |
| site/data/（89 件） | W1165 | inline_css 副本同步（同上·W1142 分组登记） |
| site/en/（138 件） | W1165 | inline_css 副本同步（同上·W1142 分组登记） |
| site/reader/（622 件） | W1165 | inline_css 副本同步（同上·W1142 分组登记） |
| docs/00-导读/W批次编号对账表.md | W1165 | 改：W1165 认领行 + W1102/1103 腾窗迁出 + W1164 收官回填 |
| pitfalls.md | W1165 | 改：+E-200（组件样式不得寄生脚本·尺寸缺陷须有真实渲染判据）+ 分项计数 163 |
| docs/agent/gates.md | W1165 | 改：第 64 槽定义（契约与口径） |
| AGENTS.md | W1165 | 改：§4.2 第 64 槽摘要 + 槽数 63→64（三处） |
| CHANGELOG.md | W1165 | 改：W1165 段落（级联） |
| HANDOVER.md | W1165 | 改：最后更新行 + 当前进度（级联） |
| scripts/output/_w1165_spec.json | W1165 | 新建：本批 spec |
| scripts/output/file-index.md | W1165 | 改：W1165 段（级联） |
| scripts/output/_cascade_files_W1165.txt | W1165 | 新建：级联清单 |
| .github/workflows/README.md | W1165 | 改：区间行推进（版本面） |
| CITATION.cff | W1165 | 改：version/date 推进（级联） |
| README.md | W1165 | 改：版本行推进（级联） |
| STRUCTURE.md | W1165 | 改：版本行推进（级联） |
| archive/docs/AGENTS-ARCHIVE.md | W1165 | 改：脚注沿革滚动（级联） |
| archive/docs/workflows-readme-history.md | W1165 | 改：逐批明细追加（W1165·级联） |
| docs/00-导读/项目说明.md | W1165 | 改：版本行推进（级联） |
| scripts/output/stats.json | W1165 | 改：stats 刷新（级联） |
| scripts/output/INDEX.md | W1165 | 改：再生成/验证缓存（级联） |
| scripts/output/README.md | W1165 | 改：再生成/验证缓存（级联） |
| scripts/output/_vermilion_solid_cache.json | W1165 | 改：再生成/验证缓存（级联） |
| scripts/output/tools-inventory.md | W1165 | 改：再生成/验证缓存（级联） |
| docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md | W1165 | 改：stats 标记 gate_count 63→64（stats.py 标记面跟随） |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1165 | 改：stats 标记 gate_count 63→64（同上） |
| pytest.ini | W1165 | 改：stats 标记 pytest_collected 随本批新增单测更新 |
| scripts/output/stats-changelog.json | W1165 | 改：stats 生成件跟随（stats.py --w 1165） |
| scripts/output/stats-index.md | W1165 | 改：stats 生成件跟随（同上） |
| .agent/skills/puti-shouye/SKILL.md | W1165 | 改：坑表计数 293→294（菩提授业 skill 双处） |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1165 | 改：台账腾窗迁入 W1102-W1103（archive_ledger_rows --apply） |
| scripts/INDEX.md | W1165 | 改：目录清单刷新（gen_folder_docs --refresh·新增两脚本） |
| tests/unit/INDEX.md | W1165 | 改：目录清单刷新（同上·新增 W1165 单测） |
| tests/unit/README.md | W1165 | 改：目录清单刷新（同上） |

## W1164 触发器硬拦升格批（2026-11-07）

| 文件 | W | 说明 |
|---|---|---|
| scripts/check_review_trigger.py | W1164 | 改：HARD_MULTIPLIER+hard_triggered+hard_triggered_today+自测五态锁 |
| scripts/check_audit_trigger.py | W1164 | 改：hard_triggered（40 批）+ledger_text_for_preflight+自测 hard 双态锁 |
| scripts/check_backlog_review.py | W1164 | 改：hard_triggered（50 批）+ledger_text_for_preflight+自测 hard 双态锁 |
| scripts/preflight_check.py | W1164 | 改：三 _step_* 接线（签名加 problems+hard 判据 FAIL 进 problems） |
| docs/00-导读/W批次编号对账表.md | W1164 | 改：W1164 认领行+W1160/1163 收官回填（含双 token 保留） |
| CHANGELOG.md | W1164 | 改：W1164 段落（级联） |
| HANDOVER.md | W1164 | 改：最后更新行（级联） |
| scripts/output/_w1164_spec.json | W1164 | 新建：本批 spec |
| scripts/output/file-index.md | W1164 | 改：W1164 段（级联） |
| scripts/output/_cascade_files_W1164.txt | W1164 | 新建：级联清单 |

## W1163 收尾微批（2026-11-07）

| 文件 | W | 说明 |
|---|---|---|
| scripts/safe_commit.py | W1163 | 改：--expect-spec 逗号分隔多 spec 并集判定（21② 形态·向后兼容单值） |
| docs/00-导读/W批次编号对账表.md | W1163 | 改：W1163 认领行+W1162 hash 回填 |
| CHANGELOG.md | W1163 | 改：W1163 段落（级联） |
| HANDOVER.md | W1163 | 改：最后更新行（级联） |
| scripts/output/_w1163_spec.json | W1163 | 新建：本批 spec |
| scripts/output/file-index.md | W1163 | 改：W1163 段（级联） |
| scripts/output/_cascade_files_W1163.txt | W1163 | 新建：级联清单 |

## W1162 微批轻量通道实施批（2026-11-07）

| 文件 | W | 说明 |
|---|---|---|
| scripts/batch_cascade.py | W1162 | 改：--light 通道（跳页脚四面/workflows/agents/citation·留五面）+准入硬守卫（非 md 触碰即拒）+ctx.light |
| docs/11-方案报告/设计与架构方案/微批轻量通道设计-三档与准入判据-2026-10-31.md | W1162 | 改：V1.0 待批 → V1.1 已批准实施（三前提落位说明·微批档暂不开通） |
| docs/00-导读/W批次编号对账表.md | W1162 | 改：W1162 认领行 |
| CHANGELOG.md | W1162 | 改：W1162 段落（级联） |
| scripts/output/_w1162_spec.json | W1162 | 新建：本批 spec |
| scripts/output/file-index.md | W1162 | 改：W1162 段（级联） |
| scripts/output/_cascade_files_W1162.txt | W1162 | 新建：级联清单 |

## W1161 存量复杂度棘轮第 1 轮（2026-11-07）

| 文件 | W | 说明 |
|---|---|---|
| scripts/check_gsap_motion.py | W1161 | 改：check_carrier_text 34→4（9 个 _carrier_* helper·J1-J7 拆解·输出逐字节一致） |
| scripts/perf_monitor.py | W1161 | 改：_render_optional_sections 16→绿 |
| scripts/check_perf_shadow.py | W1161 | 改：report 16→绿 |
| scripts/check_governance_docs.py | W1161 | 改：main 17→绿 |
| scripts/ledger_close_check.py | W1161 | 改：main 17→绿 |
| scripts/plates_verify.py | W1161 | 改：main 17→绿 |
| scripts/scan_targets.py | W1161 | 改：classify_file 17→绿 |
| scripts/visual_regression_probe.py | W1161 | 改：_diff_snapshots 17→绿 |
| docs/00-导读/W批次编号对账表.md | W1161 | 改：W1161 认领行 |
| CHANGELOG.md | W1161 | 改：W1161 段落（级联） |
| HANDOVER.md | W1161 | 改：最后更新行（级联） |
| scripts/output/_w1161_spec.json | W1161 | 新建：本批 spec |
| scripts/output/file-index.md | W1161 | 改：W1161 段（级联） |
| scripts/output/_cascade_files_W1161.txt | W1161 | 新建：级联清单 |

## W1160 治理欠账清偿批（2026-11-07）

| 文件 | W | 说明 |
|---|---|---|
| scripts/preflight_check.py | W1160 | 改：DONE_PREFIXES 补「已合并/已让号/已撤销」（is_inflight 词表根修·每批 19 条滞后误报归零） |
| tests/unit/test_preflight_check.py | W1160 | 改：+test_inflight_recognizes_merged_status 回归锁 |
| docs/11-方案报告/工作复盘与优化分析报告/工作复盘与优化分析报告-2026-11-07.md | W1160 | 新建：第 53 篇复盘（W1157-W1160 四批·五条复利经验+五道新判据表） |
| docs/11-方案报告/README.md | W1160 | 改：复盘登记面 16→17 篇+编号 53 行 |
| archive/docs/CHANGELOG-ARCHIVE.md | W1160 | 改：tier2 腾窗（1384KB→898KB·迁 138 段） |
| archive/docs/CHANGELOG-ARCHIVE-tier2-W673-W813.md | W1160 | 新建：二级归档（W673-W813） |
| archive/docs/file-index-ARCHIVE.md | W1160 | 改：tier2 腾窗（1706KB→899KB·迁 579 段） |
| archive/docs/file-index-ARCHIVE-tier2-W335-W979.md | W1160 | 新建：二级归档（W335-W979） |
| archive/README.md | W1160 | 改：台账登记（tier2 两件） |
| archive/INDEX.md | W1160 | 改：再生成 |
| archive/docs/INDEX.md | W1160 | 改：再生成（tier2 两件+台账迁出） |
| archive/docs/README.md | W1160 | 改：再生成 |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1160 | 改：台账腾窗迁出 3 行（W1097-W1099） |
| docs/00-导读/W批次编号对账表.md | W1160 | 改：W1160 认领行（含对抗审查 token）+腾窗迁出+19 行反填 |
| HANDOVER.md | W1160 | 改：坑表计数+Backlog 对账注记+级联 |
| CHANGELOG.md | W1160 | 改：W1160 段落（级联） |
| scripts/output/_w1160_spec.json | W1160 | 新建：本批 spec |
| scripts/output/file-index.md | W1160 | 改：W1160 段（级联） |
| scripts/output/_cascade_files_W1160.txt | W1160 | 新建：级联清单 |
| .github/workflows/README.md | W1160 | 改：W450-W1160 区间行推进（版本面） |
| AGENTS.md | W1160 | 改：版本脚注滚动（级联） |
| CITATION.cff | W1160 | 改：version/date 推进（级联） |
| README.md | W1160 | 改：版本行推进（级联） |
| STRUCTURE.md | W1160 | 改：版本行推进（级联） |
| archive/docs/AGENTS-ARCHIVE.md | W1160 | 改：脚注沿革滚动（级联） |
| archive/docs/workflows-readme-history.md | W1160 | 改：逐批明细追加（W1160） |
| docs/00-导读/项目说明.md | W1160 | 改：版本行推进（级联） |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1160 | 改：级联面 |
| pytest.ini | W1160 | 改：级联面 |
| scripts/guardrails/INDEX.md | W1160 | 改：级联面 |
| scripts/guardrails/README.md | W1160 | 改：级联面 |
| scripts/output/_vermilion_solid_cache.json | W1160 | 改：级联面 |
| scripts/output/stats-changelog.json | W1160 | 改：stats 级联 |
| scripts/output/stats-index.md | W1160 | 改：stats 级联 |
| scripts/output/stats.json | W1160 | 改：stats 刷新（级联） |
| site/data/cross-time-danmaku.html | W1160 | 改：页脚链推进（级联） |
| site/data/tag-cloud.html | W1160 | 改：页脚链推进（级联） |
| site/dukou-engine.html | W1160 | 改：页脚链推进（级联） |
| site/index.html | W1160 | 改：页脚链推进（级联） |
| docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md | W1160 | 改：stats 标记面跟随（report_docs/report_docs 键刷新） |
| docs/INDEX.md | W1160 | 改：再生成（复盘新件 860 篇） |
| scripts/output/INDEX.md | W1160 | 改：再生成 |
| scripts/output/README.md | W1160 | 改：再生成 |
| scripts/output/tools-inventory.md | W1160 | 改：再生成 |
| site/data/search.html | W1160 | 改：内嵌搜索索引再生成（复盘报告入索引） |
| site/en/search.html | W1160 | 改：内嵌搜索索引再生成（同上） |
| scripts/check_gov_doc_claims.py | W1160 | 改：P1-1 根修——_pitfalls_count 改读根 pitfalls.md（第四取数面跟随） |
| scripts/guardrails/check_rewrite_integrity.py | W1160 | 改：P1-2 根修——DEF_RE 支持 async def+T6/T7 负样本（自测 7 例）+P3-1 死代码简化 |
| scripts/backfill_changelog.py | W1160 | 改：P2-2 docstring 统一为规范化语义（删旧 fail-closed 双文案） |
| docs/agent/pitfalls.md | W1160 | 改：P2-1 跳转壳计数 292→293（计数链第六处） |

## W1159 坑表 E-199 批（2026-11-07）

| 文件 | W | 说明 |
|---|---|---|
| pitfalls.md | W1159 | 改：流程组 +1 条 E-199（161→162·总 293）——大块程序化改写三重防线（E-32 同族扩展到 Edit/行扫描工具面） |
| AGENTS.md | W1159 | 改：坑表计数 292→293+分项行 161→162（级联+计数链） |
| HANDOVER.md | W1159 | 改：坑表计数三处 292→293（级联+计数链） |
| .agent/skills/puti-shouye/SKILL.md | W1159 | 改：坑表计数两处 292→293（计数链） |
| scripts/guardrails/check_rewrite_integrity.py | W1159 | 新建：E-199 机器判据（C1 py_compile/C2 函数集缩水/C3 双定义·自测 5 例） |
| scripts/guardrails/check_changed.ps1 | W1159 | 改：第 3.5 步接线改写完整性判据+聚合行 |
| scripts/guardrails/check_changed.sh | W1159 | 改：第 3.5 步接线（CI/pre-commit strict-api 路径） |
| docs/00-导读/W批次编号对账表.md | W1159 | 改：W1159 认领行 |
| CHANGELOG.md | W1159 | 改：W1159 段落（级联） |
| scripts/output/_w1159_spec.json | W1159 | 新建：本批 spec |
| scripts/output/file-index.md | W1159 | 改：W1159 段（级联） |
| scripts/output/_cascade_files_W1159.txt | W1159 | 新建：级联清单 |

## W1158 W1157 遗留收尾批（2026-11-07）

| 文件 | W | 说明 |
|---|---|---|
| scripts/preflight_check.py | W1158 | 改：拆 main 根治——复杂度 47>15/branches 48>16/statements 143>80/step_env 嵌套 6>4 → 11 个 _step_*/_load/_ruff_version_drift_line 函数（行为零变化·基线 diff 验证） |
| docs/00-导读/W批次编号对账表.md | W1158 | 改：W1158 认领行+W1157 行 hash 回填（20921299·ledger_backfill 行指纹） |
| site/data/search.html | W1157 | 改：内嵌搜索索引再生成（W1157 提交后验证轮再生·本批并入） |
| site/en/search.html | W1158 | 改：内嵌搜索索引再生成（同上并入） |
| scripts/output/_vermilion_solid_cache.json | W1158 | 改：朱砂实底增量缓存（验证轮再生产物并入） |
| CHANGELOG.md | W1158 | 改：W1158 段落（级联） |
| HANDOVER.md | W1158 | 改：最后更新行+进度（级联） |
| scripts/output/_w1158_spec.json | W1158 | 新建：本批 spec |
| scripts/output/file-index.md | W1158 | 改：W1158 段（级联） |
| scripts/output/_cascade_files_W1158.txt | W1158 | 新建：级联清单 |

## W1157 全仓文件重构分类整理批（2026-11-07）

| 文件 | W | 说明 |
|---|---|---|
| .agent/skills/huoyan-jinjing/（1 件） | W1157 | 改：坑表路径改根 |
| .agent/skills/puti-shouye/（1 件） | W1157 | 改：坑表路径改根（3 处） |
| .github/workflows/（1 件） | W1157 | 改：拆分——27KB 历史流水账单行迁 archive（77KB→21KB） |
| archive/（2 件） | W1157 | 改：再生成 |
| archive/docs/（7 件） | W1157 | 改/迁：W1157 重构整理批 |
| archive/hyperframes/（5 件） | W1157 | 迁：hyperframes 顶层目录退役整迁（git mv·TOP_DIRS 摘 |
| archive/hyperframes/compositions/（4 件） | W1157 | 改/迁：W1157 重构整理批 |
| archive/hyperframes/compositions/d3-visualizations/（3 件） | W1157 | 改/迁：W1157 重构整理批 |
| archive/hyperframes/output/（3 件） | W1157 | 改/迁：W1157 重构整理批 |
| assets/（2 件） | W1157 | 改：再生成（images/maps 摘除） |
| assets/fonts/（3 件） | W1157 | 改：再生成（+font-subset-guide） |
| assets/images/（4 件） | W1157 | 删：空壳目录 |
| assets/maps/（3 件） | W1157 | 删：空壳目录（仅 INDEX+README） |
| assets/promo/plate-set/（4 件） | W1157 | 改：再生成（raw/zoom 摘除） |
| assets/promo/plate-set/raw/（3 件） | W1157 | 删：出图原件加工层退役（用户令·git 史承载回溯） |
| assets/promo/plate-set/raw/round1/（10 件） | W1157 | 改/迁：W1157 重构整理批 |
| assets/promo/plate-set/raw/round10/（4 件） | W1157 | 改/迁：W1157 重构整理批 |
| assets/promo/plate-set/raw/round11/（14 件） | W1157 | 改/迁：W1157 重构整理批 |
| assets/promo/plate-set/raw/round12/（14 件） | W1157 | 改/迁：W1157 重构整理批 |
| assets/promo/plate-set/raw/round13/（14 件） | W1157 | 改/迁：W1157 重构整理批 |
| assets/promo/plate-set/raw/round14/（14 件） | W1157 | 改/迁：W1157 重构整理批 |
| assets/promo/plate-set/raw/round15/（14 件） | W1157 | 改/迁：W1157 重构整理批 |
| assets/promo/plate-set/raw/round16/（14 件） | W1157 | 改/迁：W1157 重构整理批 |
| assets/promo/plate-set/raw/round17/（14 件） | W1157 | 改/迁：W1157 重构整理批 |
| assets/promo/plate-set/raw/round18/（14 件） | W1157 | 改/迁：W1157 重构整理批 |
| assets/promo/plate-set/raw/round2/（10 件） | W1157 | 改/迁：W1157 重构整理批 |
| assets/promo/plate-set/raw/round3/（4 件） | W1157 | 改/迁：W1157 重构整理批 |
| assets/promo/plate-set/raw/round4/（10 件） | W1157 | 改/迁：W1157 重构整理批 |
| assets/promo/plate-set/raw/round5/（4 件） | W1157 | 改/迁：W1157 重构整理批 |
| assets/promo/plate-set/raw/round6/（14 件） | W1157 | 改/迁：W1157 重构整理批 |
| assets/promo/plate-set/raw/round7/（6 件） | W1157 | 改/迁：W1157 重构整理批 |
| assets/promo/plate-set/raw/round8/（14 件） | W1157 | 改/迁：W1157 重构整理批 |
| assets/promo/plate-set/raw/round9/（6 件） | W1157 | 改/迁：W1157 重构整理批 |
| assets/promo/plate-set/zoom-w948/（8 件） | W1157 | 删：加工放大层退役 |
| assets/promo/plate-set/zoom-w952/（9 件） | W1157 | 删：加工放大层退役 |
| assets/promo/plate-set/zoom-w953/（4 件） | W1157 | 删：加工放大层退役 |
| assets/promo/plate-set/zoom-w974/（34 件） | W1157 | 删：加工放大层退役 |
| dataset/（3 件） | W1157 | 改：再生成 |
| docs/（1 件） | W1157 | 改：再生成（859 篇） |
| docs/00-导读/（8 件） | W1157 | 改：再生成（2 件迁出） |
| docs/10-方法论沉淀/（17 件） | W1157 | 改/迁：W1157 重构整理批 |
| docs/11-方案报告/（1 件） | W1157 | 改/迁：W1157 重构整理批 |
| docs/11-方案报告/治理与核查/（2 件） | W1157 | 迁：自 10-方法论沉淀 归位 11-方案报告 |
| docs/11-方案报告/设计与架构方案/（2 件） | W1157 | 改：stats 级联标记面跟随（report_docs 165） |
| docs/11-方案报告/调研与数据复盘/（2 件） | W1157 | 迁：自 00-导读 归位 11-方案报告（退役记录类） |
| docs/agent/（2 件） | W1157 | 改：坑表路径改根 |
| hyperframes/（4 件） | W1157 | 改/迁：W1157 重构整理批 |
| hyperframes/compositions/（4 件） | W1157 | 改/迁：W1157 重构整理批 |
| hyperframes/compositions/d3-visualizations/（3 件） | W1157 | 改/迁：W1157 重构整理批 |
| hyperframes/output/（3 件） | W1157 | 改/迁：W1157 重构整理批 |
| scripts/（14 件） | W1157 | 改：font-subset-guide 行摘除 |
| scripts/output/（14 件） | W1157 | 改：再生成 |
| site/（2 件） | W1157 | 改/迁：W1157 重构整理批 |
| site/data/（3 件） | W1157 | 改/迁：W1157 重构整理批 |
| site/en/（1 件） | W1157 | 改/迁：W1157 重构整理批 |
| site/static/fonts/（6 件） | W1157 | 改：再生成（4 件摘除） |
| site/static/img/（4 件） | W1157 | 改：再生成 |
| tests/unit/（7 件） | W1157 | 改：touches 合成串 pitfalls 路径改根（8 处） |
| .gitignore | W1157 | 改：e2e baseline 两行死 ignore 移除（W773 决策落地）+archive/hyperframes/.thumbnails 改路径+.zcode/ 忽略 |
| AGENTS.md | W1157 | 改：§6 第 24/25 重复条去重（删尾条不改号）+§7/§8 四文档指针（AGENT.md 系笔误撤除·流程以 §7 为正本）+目录树 hyperframes 摘行 |
| CHANGELOG.md | W1157 | 改：W1157 段落（级联） |
| CITATION.cff | W1157 | 改/迁：W1157 重构整理批 |
| CLAUDE.md | W1157 | 改：pitfalls 指针改根+接手导航四文档行（55/60 行） |
| HANDOVER.md | W1157 | 改：pitfalls 路径引用+收官进度 |
| INDEX.md | W1157 | 改：根索引再生成（gen_folder_docs） |
| README.en.md | W1157 | 改：目录树 hyperframes 摘行 |
| README.md | W1157 | 改：目录树 hyperframes 摘行 |
| RULES.md | W1157 | 新建：必守规则单一入口（7 域分节·一行条目+权威指针·四文档体系） |
| STRUCTURE.md | W1157 | 改：顶层表补 6 目录声明缺口+4 根文件行+hyperframes 摘行 |
| pitfalls.md | W1157 | 迁根：坑表正本自 docs/agent/ 迁入（292 条·3 门禁脚本路径同批改） |
| pytest.ini | W1157 | 改：pytest_collected 1464→1465（stats 级联·本批回归锁 +1） |

## W1156 运行时数据批（2026-11-07）

| 文件 | W | 说明 |
|---|---|---|
| site/en/search.html | W1156 | 改：#32 probe 在线分支移除（W1074 镜像）+文案两处 |
| site/data/narratology-16d-network.html | W1156 | 改：#33 死 fetch 承诺删除·直读 EMBEDDED |
| site/data/timeline.html | W1156 | 改：#33 同上 |
| site/data/chapter-stats.html | W1156 | 改：#34 数据源文案实况订正 |
| site/en/chart-design.html | W1156 | 改：#35 五处中文字形→EN+目录文案对齐 |
| site/data/character-appearance.html | W1156 | 改：#36 内嵌 14 条对齐随站 JSON+回退目录文案 |
| site/data/tag-cloud.html | W1156 | 改：#37 条数 81→82 实测订正+数据源行 |
| docs/00-导读/W批次编号对账表.md | W1156 | 改：W1156 认领行 |
| CHANGELOG.md | W1156 | 改：W1156 段落（级联） |
| HANDOVER.md | W1156 | 改：最后更新链+里程碑块（级联） |
| AGENTS.md | W1156 | 改：脚注+版本（级联） |
| archive/docs/AGENTS-ARCHIVE.md | W1156 | 改：AGENTS 脚注滚动（级联） |
| README.md | W1156 | 改：版本面推进（级联） |
| STRUCTURE.md | W1156 | 改：版本面推进（级联） |
| CITATION.cff | W1156 | 改：版本面推进（级联） |
| docs/00-导读/项目说明.md | W1156 | 改：版本面推进（级联） |
| .github/workflows/README.md | W1156 | 改：版本抬头推进（级联） |
| scripts/output/file-index.md | W1156 | 改：file-index 段（级联） |
| scripts/output/stats.json | W1156 | 改：stats 刷新（级联） |
| scripts/output/stats-index.md | W1156 | 改：stats 索引（级联） |
| scripts/output/stats-changelog.json | W1156 | 改：stats changelog（级联） |
| docs/INDEX.md | W1156 | 改：docs_index 刷新（级联） |
| scripts/INDEX.md | W1156 | 改：gen_folder_docs 刷新（级联） |
| scripts/output/INDEX.md | W1156 | 改：gen_folder_docs 刷新（级联） |
| scripts/output/README.md | W1156 | 改：gen_folder_docs 刷新（级联） |
| scripts/output/tools-inventory.md | W1156 | 改：工具清单刷新 |
| scripts/output/_w1156_spec.json | W1156 | 新增：本批 spec |
| scripts/output/_cascade_files_W1156.txt | W1156 | 新增：级联清单（级联） |
| scripts/output/_vermilion_solid_cache.json | W1156 | 改：朱砂缓存刷新（门禁产物） |
| scripts/output/_vermilion_solid_report.json | W1156 | 改：朱砂报告刷新（门禁产物） |
| site/sitemap.xml | W1156 | 改：gen_sitemap 随批（级联） |
| site/data/cross-time-danmaku.html | W1156 | 改：页脚短令牌（级联） |
| site/dukou-engine.html | W1156 | 改：页脚短令牌（级联） |
| site/index.html | W1156 | 改：页脚短令牌（级联） |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1156 | 改：版本抬头（级联） |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1156 | 改：台账窗口滚动（级联） |

## W1155 假绿 P1 批（2026-11-07）

| 文件 | W | 说明 |
|---|---|---|
| scripts/ledger_backfill.py | W1155 | 改：#1 self_test 按 fails 判红 |
| scripts/verify_delivery.py | W1155 | 改：#5 site 档并 docs 段 |
| scripts/safe_commit.py | W1155 | 改：#6 expect-spec+pathspec 漂移拒绝 |
| scripts/check_commit_scope.py | W1155 | 改：#13 SpecBrokenError 哨兵+main 捕获 |
| scripts/check_structure.py | W1155 | 改：#10 三括号平衡+零面守卫 |
| scripts/check_story_timeline_sync.py | W1155 | 改：#46 双空判红 |
| scripts/check_folder_docs.py | W1155 | 改：#47 git 失效 fail-closed |
| scripts/check_citations.py | W1155 | 改：#48 恰 100 回断言 |
| scripts/check_design_asset_manifest.py | W1155 | 改：#57 零条目红 |
| scripts/check_dark_state_gate.js | W1155 | 改：#63 基线缺页+数量断言 |
| scripts/check_screenshot_gates.js | W1155 | 改：#64 --only 零命中 exit 2 |
| scripts/check_db_schema.py | W1155 | 改：#70 锚定执行形态+剥注释 |
| scripts/check_archive_health.py | W1155 | 改：#72 -C ROOT+returncode |
| scripts/check_pitfall_id_unique.py | W1155 | 改：#56 同号同标题豁免移除 |
| tests/unit/test_w1106_pitfall_id_unique.py | W1155 | 改：测试改真增量形态 |
| scripts/check_plan_template.py | W1155 | 改：#55 merge-base 回退面 |
| scripts/check_action_refs.py | W1155 | 改：#54 --ci 参数+透传 |
| scripts/check_chart_values.js | W1155 | 改：#12 console/stability 入判据+缺口进退出码 |
| scripts/check_data_drift.js | W1155 | 改：#11 双逗号正则+单侧键摘要通道 |
| scripts/check_script_coverage.py | W1155 | 改：#9 实质调用面三通道+语料补钩子+分类注入 |
| scripts/output/script-coverage-baseline.txt | W1155 | 改：48 件存量登记+check_js_syntax 陈旧行删 |
| scripts/batch_closeout.py | W1155 | 改：#14 docnums 前向 NOTE |
| scripts/check_dataset_provenance.py | W1155 | 改：#15 汇总句引文状态分布 |
| tests/unit/test_w1141_gate_mount.py | W1155 | 改：槽数断言改动态对账 |
| tests/unit/test_w1154_run_all_discovery.py | W1154 | 新增：B 类发现器锁（W1154 随批暂存） |
| docs/00-导读/W批次编号对账表.md | W1155 | 改：W1155 认领行 |
| CHANGELOG.md | W1155 | 改：W1155 段落（级联） |
| HANDOVER.md | W1155 | 改：最后更新链+里程碑块（级联） |
| AGENTS.md | W1155 | 改：脚注+版本（级联） |
| archive/docs/AGENTS-ARCHIVE.md | W1155 | 改：AGENTS 脚注滚动（级联） |
| README.md | W1155 | 改：版本面推进（级联） |
| STRUCTURE.md | W1155 | 改：版本面推进（级联） |
| CITATION.cff | W1155 | 改：版本面推进（级联） |
| docs/00-导读/项目说明.md | W1155 | 改：版本面推进（级联） |
| .github/workflows/README.md | W1155 | 改：版本抬头推进（级联） |
| scripts/output/file-index.md | W1155 | 改：file-index 段（级联） |
| scripts/output/stats.json | W1155 | 改：stats 刷新（级联） |
| scripts/output/stats-index.md | W1155 | 改：stats 索引（级联） |
| scripts/output/stats-changelog.json | W1155 | 改：stats changelog（级联） |
| docs/INDEX.md | W1155 | 改：docs_index 刷新（级联） |
| scripts/INDEX.md | W1155 | 改：gen_folder_docs 刷新（级联） |
| scripts/output/INDEX.md | W1155 | 改：gen_folder_docs 刷新（级联） |
| scripts/output/README.md | W1155 | 改：gen_folder_docs 刷新（级联） |
| scripts/output/tools-inventory.md | W1155 | 改：工具清单刷新 |
| scripts/output/_w1155_spec.json | W1155 | 新增：本批 spec |
| scripts/output/_cascade_files_W1155.txt | W1155 | 新增：级联清单（级联） |
| scripts/output/_vermilion_solid_cache.json | W1155 | 改：朱砂缓存刷新（门禁产物） |
| scripts/output/_vermilion_solid_report.json | W1155 | 改：朱砂报告刷新（门禁产物） |
| tests/unit/INDEX.md | W1155 | 改：gen_folder_docs 刷新 |
| tests/unit/README.md | W1155 | 改：gen_folder_docs 刷新 |
| pytest.ini | W1155 | 改：collected 头注（级联） |
| site/sitemap.xml | W1155 | 改：gen_sitemap 随批（级联） |
| site/data/cross-time-danmaku.html | W1155 | 改：页脚短令牌（级联） |
| site/data/tag-cloud.html | W1155 | 改：页脚短令牌（级联） |
| site/dukou-engine.html | W1155 | 改：页脚短令牌（级联） |
| site/index.html | W1155 | 改：页脚短令牌（级联） |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1155 | 改：版本抬头（级联） |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1155 | 改：台账窗口滚动（级联） |
| .github/workflows/ci.yml | W1155 | 改：级联连带 |
| tests/unit/test_ci_wiring.py | W1155 | 改：级联连带 |

## W1154 治理快批（2026-11-07）

| 文件 | W | 说明 |
|---|---|---|
| docs/00-导读/新Agent启动Prompt.md | W1154 | 改：可视化页 87→88/data HTML 88→89（N5） |
| docs/00-导读/文档规范.md | W1154 | 改：「现役 66 段」→68（N2） |
| AGENTS.md | W1154 | 改：§4.2 61 槽→63 三处 + 第 16 槽退役标注 + 脚注/版本（级联） |
| docs/agent/gates.md | W1154 | 改：第 49 槽页数 88→89 + _w857 死指针订正 |
| .git/hooks/pre-commit | W1154 | 改：origin/dev→动态 @{u} + gitleaks 缺失 WARN |
| assets/promo/README.md | W1154 | 改：_w892 死指针→已归档说明 |
| scripts/plates_verify.py | W1154 | 改：docstring 转正名 |
| scripts/gen_folder_docs.py | W1154 | 改：重复 _kind_exists 去重 |
| Makefile | W1154 | 改：.PHONY 补 cross-line |
| scripts/run_all.py | W1154 | 改：discover_scripts 排除 __init__/_ 前缀 + main-guard 优先 |
| tests/unit/test_w1154_run_all_discovery.py | W1154 | 新增：B 类发现器回归锁 2 例 |
| scripts/agent_start.py | W1154 | 改：下一自由号=台账 max(W)+1（碑化块依赖移除） |
| pytest.ini | W1154 | 改：stats 行去重 + 52 段指针化 + collected 头注（级联） |
| .github/workflows/screenshot-review.yml | W1154 | 改：内联 case 判定改调 check_screenshot_scope.py（接线） |
| tests/unit/test_ci_wiring.py | W1154 | 改：接线回归锁（断言脚本名+无内联残留） |
| docs/11-方案报告/README.md | W1154 | 改：9 份报告补登记 |
| scripts/check_index_health.py | W1154 | 改：新增 check_docs11_registration 双向对账 |
| docs/agent/batch-closeout-checklist.md | W1154 | 改：段窗/verify 段指针化 + 禁 add -A |
| .pre-commit-config.yaml | W1154 | 改：删休眠钩子 drl-contracts/check-untracked + 非等价声明 |
| scripts/check_orchestration_refs.py | W1154 | 新增：编排面引用存在性门禁（双边界判据+self-test） |
| .github/workflows/ci.yml | W1154 | 改：verify-delivery job 挂 orchestration_refs 步 |
| scripts/batch_closeout.py | W1154 | 改：index 步接入 gen_sitemap.py |
| site/sitemap.xml | W1154 | 改：gen_sitemap 重生成（854 URLs·随批） |
| docs/00-导读/W批次编号对账表.md | W1154 | 改：W1154 认领行 |
| CHANGELOG.md | W1154 | 改：W1154 段落（级联） |
| HANDOVER.md | W1154 | 改：最后更新链+里程碑块（级联） |
| archive/docs/AGENTS-ARCHIVE.md | W1154 | 改：AGENTS 脚注滚动归档（级联） |
| README.md | W1154 | 改：版本面推进（级联） |
| STRUCTURE.md | W1154 | 改：版本面推进（级联） |
| CITATION.cff | W1154 | 改：版本面推进（级联） |
| docs/00-导读/项目说明.md | W1154 | 改：版本面推进（级联） |
| .github/workflows/README.md | W1154 | 改：版本抬头推进（级联） |
| scripts/output/file-index.md | W1154 | 改：file-index 段（级联） |
| scripts/output/stats.json | W1154 | 改：stats 刷新（级联） |
| scripts/output/stats-index.md | W1154 | 改：stats 索引（级联） |
| scripts/output/stats-changelog.json | W1154 | 改：stats changelog 面（级联） |
| docs/INDEX.md | W1154 | 改：docs_index 刷新（级联） |
| scripts/INDEX.md | W1154 | 改：gen_folder_docs 刷新（级联） |
| scripts/output/INDEX.md | W1154 | 改：gen_folder_docs 刷新（级联） |
| scripts/output/README.md | W1154 | 改：gen_folder_docs 刷新（级联） |
| scripts/output/tools-inventory.md | W1154 | 改：工具清单刷新 |
| scripts/output/_w1154_spec.json | W1154 | 新增：本批 spec |
| scripts/output/_cascade_files_W1154.txt | W1154 | 新增：级联清单（级联） |
| scripts/output/_vermilion_solid_cache.json | W1154 | 改：朱砂实底增量缓存刷新（门禁产物） |
| scripts/output/_vermilion_solid_report.json | W1154 | 改：朱砂实底报告刷新（门禁产物） |
| tests/unit/INDEX.md | W1154 | 改：gen_folder_docs 刷新 |
| tests/unit/README.md | W1154 | 改：gen_folder_docs 刷新 |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1154 | 改：台账窗口滚动归档（级联） |

## W1153 安全批（2026-11-07）

| 文件 | W | 说明 |
|---|---|---|
| xiyouji-agent-web/server/engine/tools.ts | W1153 | 改：#27 GIT_DANGER 前缀族拦截 + #28 DENY_WRITE /i 与 realpath 复检 + #29 会话新写 scripts 拒执行/childEnv 大小写不敏感 |
| xiyouji-agent-web/server/engine/tools.test.ts | W1153 | 改：回归锁 4 例（S1 前缀缩写/S2 大小写/S3 会话新写拒执行/S4 childEnv） |
| scripts/rag/rag_server.py | W1153 | 改：#30 CORS 白名单（对齐 api P3-2）+ /route 异常不回显 + 每 IP 60 次分限速 |
| tests/unit/test_w1153_rag_cors.py | W1153 | 新增：回归锁 3 例（白名单三态/限速/route 不回显） |
| CHANGELOG.md | W1153 | 改：W1153 段落（级联） |
| HANDOVER.md | W1153 | 改：最后更新链+里程碑块（级联） |
| AGENTS.md | W1153 | 改：脚注+版本（级联） |
| archive/docs/AGENTS-ARCHIVE.md | W1153 | 改：AGENTS 脚注滚动归档（级联） |
| README.md | W1153 | 改：版本面推进（级联 versions·幂等） |
| STRUCTURE.md | W1153 | 改：版本面推进（级联·幂等） |
| CITATION.cff | W1153 | 改：版本面推进（级联·幂等） |
| docs/00-导读/项目说明.md | W1153 | 改：版本面推进（级联·幂等） |
| .github/workflows/README.md | W1153 | 改：版本抬头推进（级联·幂等） |
| docs/00-导读/W批次编号对账表.md | W1153 | 改：W1153 认领行 |
| scripts/output/file-index.md | W1153 | 改：file-index 段（级联） |
| scripts/output/stats.json | W1153 | 改：stats 刷新（级联） |
| scripts/output/stats-index.md | W1153 | 改：stats 索引（级联） |
| scripts/output/stats-changelog.json | W1153 | 改：stats changelog 面（级联） |
| docs/INDEX.md | W1153 | 改：docs_index 刷新（级联 index 步） |
| scripts/INDEX.md | W1153 | 改：gen_folder_docs 刷新（级联） |
| scripts/output/INDEX.md | W1153 | 改：gen_folder_docs 刷新（级联） |
| scripts/output/README.md | W1153 | 改：gen_folder_docs 刷新（级联） |
| scripts/output/tools-inventory.md | W1153 | 改：工具清单刷新 |
| scripts/output/_w1153_spec.json | W1153 | 新增：本批 spec |
| scripts/output/_cascade_files_W1153.txt | W1153 | 新增：级联清单（级联） |
| scripts/output/_vermilion_solid_cache.json | W1153 | 改：朱砂实底增量缓存刷新（门禁产物） |
| scripts/output/_vermilion_solid_report.json | W1153 | 改：朱砂实底报告刷新（门禁产物） |
| tests/unit/INDEX.md | W1153 | 改：gen_folder_docs 刷新（新增测试件登记） |
| tests/unit/README.md | W1153 | 改：gen_folder_docs 刷新（新增测试件登记） |
| pytest.ini | W1153 | 改：collected 头注推进（W830 C5b 对账面·stats 连带） |

## W1152 v4 body 行高改值批（2026-11-07）

| 文件 | W | 说明 |
|---|---|---|
| site/tokens.css | W1152 | 改：--leading-body 1.75→1.80（与 --type-body /1.80 对齐·孤儿刻度令牌防分叉地雷·页自有消费 0 实测） |
| site/system.css | W1152 | 改：body 语义消费 --type-body（font shorthand·行高 1.75→1.80 v4 明文改值项·style/variant 重置在 body 本为初始） |
| DESIGN.md | W1152 | 改：§4C type 行补 body 消费 + grid 行终裁不迁移 + 后续批范围复盘 |
| docs/00-导读/design.md | W1152 | 改：令牌导出再生成（134 键·0 警告） |
| scripts/output/design-tokens.json | W1152 | 改：令牌导出再生成（反篡改比对源） |
| docs/00-导读/W批次编号对账表.md | W1152 | 改：W1152 认领行 + 腾窗迁出 2 行（W1089-W1090） |
| archive/docs/W批次编号对账表-ARCHIVE.md | W1152 | 改：台账腾窗接收 W1089-W1090 两行 |
| tests/unit/test_w1152_body_lh_alignment.py | W1152 | 新增：行高双源对齐 + body 语义消费守卫 2 例 |
| scripts/output/_w864_accent_exemptions.json | W1152 | 改：data/aesthetics.html 豁免对齐 W886 EN 姊妹页三类（stage-color-bar/color-swatch/kpi-card·纠正误判类·16-⑦ 留痕） |
| CHANGELOG.md | W1152 | 改：W1152 段落（级联） |
| HANDOVER.md | W1152 | 改：最后更新链+里程碑块（级联） |
| AGENTS.md | W1152 | 改：脚注+版本（级联） |
| archive/docs/AGENTS-ARCHIVE.md | W1152 | 改：AGENTS 脚注滚动归档（级联） |
| README.md | W1152 | 改：版本面推进（级联 versions·幂等） |
| STRUCTURE.md | W1152 | 改：版本面推进（级联·幂等） |
| CITATION.cff | W1152 | 改：版本面推进（级联·幂等） |
| docs/00-导读/项目说明.md | W1152 | 改：版本面推进（级联·幂等） |
| .github/workflows/README.md | W1152 | 改：版本抬头推进（级联·幂等） |
| docs/00-导读/统计口径说明.md | W1152 | 改：stats 刷新连带（级联） |
| docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md | W1152 | 改：版本抬头推进（级联 versions·幂等） |
| docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md | W1152 | 改：版本抬头推进（级联·幂等） |
| scripts/output/file-index.md | W1152 | 改：file-index 段（级联） |
| scripts/output/stats.json | W1152 | 改：stats 刷新（级联） |
| scripts/output/stats-index.md | W1152 | 改：stats 索引（级联） |
| scripts/output/stats-changelog.json | W1152 | 改：stats changelog 面（级联） |
| docs/INDEX.md | W1152 | 改：docs_index 刷新（级联 index 步） |
| scripts/INDEX.md | W1152 | 改：gen_folder_docs 刷新（级联） |
| scripts/output/INDEX.md | W1152 | 改：gen_folder_docs 刷新（级联） |
| scripts/output/README.md | W1152 | 改：gen_folder_docs 刷新（级联） |
| scripts/output/tools-inventory.md | W1152 | 改：工具清单刷新（gen_folder_docs） |
| scripts/output/_w1152_spec.json | W1152 | 新增：本批 spec |
| scripts/output/_cascade_files_W1152.txt | W1152 | 新增：级联清单（级联） |
| scripts/output/_vermilion_solid_cache.json | W1152 | 改：朱砂实底增量缓存刷新（门禁产物） |
| scripts/output/_vermilion_solid_report.json | W1152 | 改：朱砂实底报告刷新（门禁产物） |
| tests/unit/INDEX.md | W1152 | 改：gen_folder_docs 刷新（新增测试件登记） |
| tests/unit/README.md | W1152 | 改：gen_folder_docs 刷新（新增测试件登记） |
| pytest.ini | W1152 | 改：collected 头注推进（W830 C5b 对账面·stats 连带） |
| site/（2 件） | W1152 | inline_css 副本同步（body 消费与 leading 值传播·_template.html + dukou-engine） |
| site/data/（89 件） | W1152 | inline_css 副本同步（同上·W1142 分组登记） |
| site/en/（138 件） | W1152 | inline_css 副本同步（同上·W1142 分组登记） |
| site/reader/（622 件） | W1152 | inline_css 副本同步（同上·W1142 分组登记） |

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

> **维护契约**：本索引按 W 追加登记（每文件 1 行 + 一句摘要），历史段禁改；新增/变更文件必须先有 CHANGELOG 对应 W 段再登记（双索引铁律），禁止无 W 段单独登记。
