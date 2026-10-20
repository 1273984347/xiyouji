# xiyouji 文件反向索引

> 与 [CHANGELOG.md](../../CHANGELOG.md) 配套：给定文件，查它被改过几次、每次对应哪个 W 条目。
> W### 编号规则见 CHANGELOG.md 顶部。
> 创建于 2026-07-22（v0.8 双索引改造）
>
> **历史归档**：W031-W087（v2.0.4-v2.0.60）site/data/ 部分已迁移至 [file-index-ARCHIVE.md](../../archive/docs/file-index-ARCHIVE.md)；W422 再归档 W393-W416 段；W511 归档 W417-W448 段 + W449-W463 损坏区尾部清理。；W736 归档 W449-W699 段（与 CHANGELOG 现役边界统一至 W700）。本文件仅保留 W700+ 现役索引。
>
> **维护契约**：本索引按 W 追加登记（每文件 1 行 + 一句摘要），历史段禁改；新增/变更文件必须先有 CHANGELOG 对应 W 段再登记（双索引铁律），禁止无 W 段单独登记。

---


## W812 去旧厂商 Agent 工具品牌化批（2026-10-20）

| 文件 | W | 说明 |
|---|---|---|
| .gitignore | W812 | 改：删该厂商工具目录的忽略规则（2 行） |
| AGENTS.md | W812 | 改：机器环境事实条「提交门禁 hook 解释器」改写为遵循仓内工具清单口径（全局 Python 3.12·启动器优先·去掉厂商托管运行时指向） |
| CHANGELOG.md | W812 | 改：现役与历史段该品牌字样去品牌化（认领/来源/环境事实类叙述） |
| archive/docs/CHANGELOG-ARCHIVE.md | W812 | 改：归档段该品牌字样去品牌化（豁免登记/环境事实/硬性排除三类） |
| archive/docs/file-index-ARCHIVE.md | W812 | 改：归档文件索引条该品牌字样去品牌化 |
| archive/docs/plans/2026-09-09-service-experience-and-agent-ops-plans.md | W812 | 改：品牌清零类裁决叙述去品牌化（复合表述改为旧厂商 Agent 品牌含 CodeBuddy） |
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
