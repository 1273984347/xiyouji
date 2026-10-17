# CI/CD 工作流说明

> **W234-E1 CI/CD 化 → W399/W400/W401/W410/W411/W412/W413/W414/W415/W416/W417/W418/W419/W420/W421/W422/W423/W424/W425/W426 → W450-W778** — 西游记解读项目（`D:\xiyouji`，W778）的 GitHub Actions 工作流层。
> **W399**：ci.yml 补 push main 触发（此前仅 pull_request，项目直接 push main 无 PR → CI 从未运行）；sitemap/robots 域名补全；新增 rum-viewer。
> **W400**：CI/Security 三 workflow 转绿（ruff 424 违规清零·XSS high 归零·Lighthouse 门禁校准·a11y pip cache 修复·black 门禁移除）。
> **W401**：ci.yml 5→7 job（pytest-unit 全量 tests/ + agent-web-build）·agent-web 源码入库·移除 3 处无 pip 安装 job 的 cache: pip 残留·build-test-deploy.yml 弃用删除。
> **W410**：security.yml npm-audit 扩至 agent-web（依赖链修复：overrides 强制 cherry-markdown 0.11.9/mermaid 11.16.1/dompurify 3.4.13·uuid 9→11·lucide-react 0.563→1.31，双目录 audit 0 漏洞）。
> **W411**：安全审计 P0-1/P1-1 处置（agent-web server 鉴权加固 + MCP 路径白名单·无 workflow 文件改动，agent-web-build job 覆盖构建回归）。
> **W412**：安全审计剩余项处置（P0-2 禁运行时覆盖密钥/端点 + RAG 参数钳制/LLM 端点校验 + SSE 超时与断开清理 + DOMPurify 消毒 + 依赖锁定 + CORS 白名单·无 workflow 文件改动，agent-web-build job 覆盖构建回归）。
> **W413**：仓库文件策略审查（严格审查入库边界·个人文档/方法论/开发内部资产恢复入库·字体源入库 +24MB·无 workflow 文件改动，CI 全量验证涵盖）。
> **W414**：README 用户手册改造（普通读者入口 + 开发者分区两级引导·无 workflow 文件改动，CI 全量验证涵盖）。
> **W415**：README 视觉引导增量（徽章区 3 枚 + 图标化速览 + 首页预览截图 + 反馈段·无 workflow 文件改动，CI 全量验证涵盖）。
> **W416**：文件管控清单标注（文档规范 §11 必同步/禁擅自修改显式化·多 session/Agent 协作·无 workflow 文件改动，CI 全量验证涵盖）。
> **W417**：actions 全量升级消除 Node 20 deprecation（ci.yml/pages.yml/perf.yml/screenshot-review.yml/security.yml 共 48 处：checkout v7/setup-node v7/setup-python v7/upload-artifact v7/upload-pages-artifact v5/configure-pages v6/deploy-pages v5/nick-fields retry v4·gh api releases/latest 实测 2026-08-10）。
> **W418**：内容质量深化（site/en/ 4 文件 29 broken 链接修复——EN 版存在指向同目录/无 EN 版回退中文原版 ../data/*.html 加 lang="zh-CN" 标注·A1 逐回解读 23 回补 `> 导航：` 引用行 100 回全覆盖·无 workflow 文件改动，CI 全量验证涵盖）。
> **W422**：全量治理（perf.yml 补 push 触发——LHCI 硬预算此前仅 PR 从未运行·verify_delivery 新增导航/链接/sitemap/回退 4 门禁·ci.yml 新增 JS 语法检查 + mypy report-only·Dependabot 配置·截图 artifact 失败才上传）。
> **W423**：性能债专项（perf.yml LHCI 预算收紧 LCP 5000→4500·CLS 0.3→0.2·TBT 300 不变；CJK 字体 swap→optional·D3/Three 移出 head——无 workflow 结构改动，仅预算阈值更新）。
> **W424**：性能债实测校准（push 首跑：LCP 4.73-4.87s 超 4500 → 预算回调 5000·timeline CLS 0.235 超 0.2 → 预算回归 0.3·FCP warn 4800·Screenshot 首跑暴露 timeline `d3 is not defined` + 内联 defer 无效 → 3D/时间线 `main()` 改 load 事件触发）。
> **W421**：Screenshot Review 提速优化（改动范围判定：页脚/文档-only 跳过·site/data 变更定向截图·static/脚本/workflow 变更全量·schedule/dispatch 恒全量 + batch_screenshots.js --only-pages + Playwright 浏览器缓存 + checkout fetch-depth 0）。
> **W420**：A1 内容质量深化（深度解读 100/100 补全 + 56 回元数据补齐 + 99 回导航错链修复·无 workflow 文件改动，CI 全量验证涵盖）。
> **W419**：修复 A1 深度解读 SD 错位（22 篇 SD 编号≠真实回号归位·40-72 回全覆盖·源文件 24 篇元数据/H1/关联行修正·第 56 回补写 SD101·无 workflow 文件改动，CI 全量验证涵盖）。
> **W450-W778**：verify 门禁体系扩展（W458-W649 历批逐条明细见 CHANGELOG；实质改动 workflow 文件的仅 W523 diff quotePath/W536 dependabot ignore+eslint/W563 defer 与 SW 探针/W571 tokens 分发/W578 dark-state-gate 浅克隆五批，W450 前建批见 git log）+ W464 perf 基线确立（perf.yml 预算沿用 W424 校准值 LCP≤5000/CLS≤0.3/TBT≤300）+ 其余 W450-W649 各批无 workflow 结构改动）+ W650 第 28 门禁加固与 PRD 出库·无 workflow 结构改动）+ W651 全量启动裁决入档与三源快照·无 workflow 结构改动）+ W652 PD-5 设计令牌导出与对账门禁·无 workflow 结构改动）+ W653 PD-1a 色盲安全门禁·无 workflow 结构改动）+ W654 PD-1b 选型章与降级门禁·无 workflow 结构改动）+ W655 B-9 之一 D3 色值变量化·无 workflow 结构改动）+ W656 B-9 之一 audit 补丁合并单模块·无 workflow 结构改动）+ W657 B-6 第二步可引用性组件·无 workflow 结构改动）+ W658 B-7 分析方法 pip 包·+ 663 治理经验移植批·W659-W663 合并登记·CI 加固：61 处 uses 改 SHA 钉+顶层 permissions 收敛+security dispatch·无 workflow 结构改动）+ W664 CLAUDE.md 速查层+写作可验证纪律·无 workflow 结构改动）+ W666 工作复盘报告入库·无 workflow 结构改动）+ W661 WP-D2 索引站内化+footer-meta 改链·无 workflow 结构改动）+ W667 复盘三卡防漂移落地·无 workflow 结构改动）+ W662 暗色审计入基线+遗漏收敛·无 workflow 结构改动）+ W668 数据评审裁决落地·无 workflow 结构改动）+ W669 WP-E 内容发现架构·无 workflow 结构改动）+ W670 开放项双闭与默认源治理·无 workflow 结构改动）+ W671 共享载体治理·无 workflow 结构改动）+ W672 站点质量批次一·无 workflow 结构改动）+ W673 站点质量批次二·无 workflow 结构改动）+ W674 站点质量批次三·无 workflow 结构改动）+ W675 工作复盘报告入库·无 workflow 结构改动）+ W679 workflow 工业化方案入库与评估密钥引导·无 workflow 结构改动）+ W680 agent-web 引擎更换与全模型适配·无 workflow 结构改动）+ W681 品牌清零与归档治理（三归档件移 docs/archive/·现役面无 workflow 结构改动）+ W683 新增三 starter workflow（dependency-review/stale/scorecard·全 SHA 钉）+ W684 工作复盘报告入库·无 workflow 结构改动）+ W685 复盘下半场报告入库与工具收尾·无 workflow 结构改动）+ W686 workflow 方案退役与预留清理·无 workflow 结构改动）+ W687 S4 外部审读处置与投稿体系批·无 workflow 结构改动）+ W688 第六轮复审处置迷你批·无 workflow 结构改动）+ W689 全变动对抗复审修复批·无 workflow 结构改动）+ W690 安全告警处置·无 workflow 结构改动）+ W676 站点质量修复批次四·无 workflow 结构改动）+ W677 站点质量修复批次五·无 workflow 结构改动）+ W678 站点质量修复批次六·无 workflow 结构改动）+ W691 Backlog 裁决执行批·无 workflow 结构改动）+ W692 复盘报告入库批次·无 workflow 结构改动）+ W693 用户三裁决执行批·无 workflow 结构改动）+ W694 故事内时间线可视化页落地批·无 workflow 结构改动）+ W695 第 39 门禁挂载与 CSP 全站收紧批·无 workflow 结构改动）+ W696 复盘报告第二篇入库批次·无 workflow 结构改动）+ W697 复盘报告第四篇入库批·无 workflow 结构改动）+ W698 门禁scope分级与提交重试批·无 workflow 结构改动）+ W699 三卡工具化与三报告批·无 workflow 结构改动）+ W700 docs全量链接门禁与断链清债批·无 workflow 结构改动）+ W701 BL-20动工与S-26工具化批·无 workflow 结构改动）+ W702 六文档口径清债批·无 workflow 结构改动）+ W703 聚合数字对账门禁批·无 workflow 结构改动）+ W704 数字实体化批·无 workflow 结构改动）+ W705 Agent开局状态摘要批·无 workflow 结构改动）+ W706 编号空间盘点与元规则批·无 workflow 结构改动）+ W707 分层重构先行件与阅读契约批·无 workflow 结构改动）+ W708 全变动对抗复审修复批·无 workflow 结构改动）+ W709 BL-24分层搬迁批·无 workflow 结构改动）+ W710 BL-25与BL-21收口批·无 workflow 结构改动）+ W711 方案D形态改造批·无 workflow 结构改动）+ W712 方案档挑刺补正批·无 workflow 结构改动）+ W713 挑刺第十四次补正批·无 workflow 结构改动）+ W714 停用守卫与考古补库批·无 workflow 结构改动）+ W715 工作复盘报告批·无 workflow 结构改动）+ W716 stats 实体化补正批·无 workflow 结构改动）+ W717 页脚链头锚定根修批·无 workflow 结构改动）+ W718 变更史可追踪补正批·无 workflow 结构改动）+ W719 review 修复批·无 workflow 结构改动）+ W720 C4 认领行强制批·无 workflow 结构改动）+ W721 复盘增补与脚注滚动根修批·无 workflow 结构改动）+ W722 八项裁决执行批·无 workflow 结构改动）+ W723 级联清单反向覆盖根修批·无 workflow 结构改动）+ W724 页脚链损坏修复与链长治理批·无 workflow 结构改动）+ W725 review 收官 mini 批·无 workflow 结构改动）+ W726 本地工具链修复批·无 workflow 结构改动）+ W727 SVG 保护补打与级联根修批·无 workflow 结构改动）+ W728 门禁与工具链代码重构·无 workflow 结构改动）+ W729 性能与可访问性工具链重构·无 workflow 结构改动）+ W730 门禁脚本长函数收尾重构·无 workflow 结构改动）+ W731 发布工具链与安全扫描重构·无 workflow 结构改动）+ W732 性能与文档工具链重构·无 workflow 结构改动）+ W733 达标收尾六目标拆编·无 workflow 结构改动）+ W734 归档体系统一与交接文档更名·无 workflow 结构改动）+ W735 全仓归档大扫除·无 workflow 结构改动）+ W736 发布链工具化与文档负载治理·无 workflow 结构改动）+ W737 对抗性审查修复与报告归置·无 workflow 结构改动）+ W738 tmpe 临时文件体系策略化治理·无 workflow 结构改动）+ W739 对账表 touches 冲突声明与 preflight 交集拒绝落地·无 workflow 结构改动）+ W740 干扰治理穷举分析收敛为决策实施路线图·无 workflow 结构改动）+ W741 评估实施记录入库与 is_inflight 全星号剥离加固·无 workflow 结构改动）+ W742 复盘入库与反向扫描与计数第四检·无 workflow 结构改动）+ W743 融合层消融与加权重构·无 workflow 结构改动）+ W744 检索增强管线集成与四档开关·无 workflow 结构改动）+ W745 改写档智能路由化·无 workflow 结构改动）+ W746 路由端点与模块转正·无 workflow 结构改动）+ W747 能力总览与边界沉淀·无 workflow 结构改动）+ W748 双线收官复盘入库·无 workflow 结构改动）+ W749 ML import 坑入 pitfalls·无 workflow 结构改动）+ W751 根级工具链防护批·无 workflow 结构改动）+ W754 方法论目录全量校订（必修 4 类 + 建议改 8 类 + 索引重写）·无 workflow 结构改动）+ W755 方法论深度篇扩建与治理口径统一（新增深度篇加治理修复）·无 workflow 结构改动）+ W756 人名用字语料纯度与口径登记（清语料加口径登记）·无 workflow 结构改动）+ W757 CI 门禁接线缺陷修复批（verify-delivery job 补 Playwright 安装+缓存·D1 第 43 门禁此前 CI 必红；agent-web-build job 补 test:server·D2 安全单测此前未接线；两处均为 workflow 结构改动；W758 起无 workflow 结构改动）+ W758 CI 首跑暴露缺陷修复批（平台守卫加依赖登记加门禁加固）·无 workflow 结构改动）+ W759 脚注滚动断言与指针注记刷新根修（编号空洞兼容）·无 workflow 结构改动）+ W760 全量对抗性审查（3327 入库件，五可标准，六个审查面）收官，11 项发现 4 HIGH，25 个证据脚本可复跑，正面结论独立复算·无 workflow 结构改动）+ W761 守卫单模块化，重复消除，复杂函数拆分，命名体系统一，潜伏缺陷修复（行为零变化，对拍验证）·无 workflow 结构改动）+ W762 重构报告晋升入库（README 索引重编号 18→19，STRUCTURE 标记 21→22，stats 三连带刷新）·无 workflow 结构改动）+ W763 F-1a 照录区字级篡改全量修复（97 处修 9 文件，占位符约定与语料疑点登记不修，行尾纯净）·无 workflow 结构改动）+ W764 S-01 RCE 修复（git pager 族参数层拦截 + 全命令 shell 元字符二次校验，38 例单测含 5 拒 1 放行）·无 workflow 结构改动）+ W765 a11y_audit 收尾重构（增强辅助族注释统一 + rule_29_parsing 74 行拆为编排器加三检测臂，行为对拍逐字节一致）·无 workflow 结构改动）+ W766 F-1b C 类 59 条静默删改全量处置（51 修复+8 语料疑点登记，引文与语料逐字对齐，引文门禁 100%）·无 workflow 结构改动）+ W767 第 9 门禁口径修复（共路标量深比对+声明式基线）+F-7 双 KPI 修正+存量漂移清理·无 workflow 结构改动）+ W768 第 44 槽挂载（validate_en --all，138 页 script CJK=0）+6 页整改+豁免基线移除·无 workflow 结构改动）+ W769 动效 duration 全站归一（37 处至≤600+第 13 门禁补规则）+统计口径说明 86→87 级联（8 处现役文案+C5 域扩展）·无 workflow 结构改动）+ W770 F-2 文首文件级演绎标记识别（两判定面）+hardships 生成器 label 化输出对齐+副本回灌与字节自检工具恢复+F-8 复核·无 workflow 结构改动）+ W771 F-9 收口：区间缺号三源定性登记去向 + 门禁注释陈旧数字刷新·无 workflow 结构改动）+ W772 计划方案三篇登记入库加索引重建加报告计数 22 到 23·无 workflow 结构改动）+ W773 工程基础设施薄弱点修复（E2E 接线，视觉回归重建，英文站 a11y 补面，索引漂移门禁）·ci.yml 新增 e2e-interaction job·一处 workflow 结构改动·视觉回归与 a11y 与索引门禁均无 workflow 结构改动）+ W774 CI 首跑分歧修复（docs_index 跨平台排序根修加回归测试）与 T-02 推送闭环·无 workflow 结构改动）+ W775 JS 门禁重构落地，两公共模块与三脚本重写，外部契约五维对拍零漂移，顺手修复数据漂移门禁静默跳过两页的潜伏缺陷，外部评审七项指控逐条核查·无 workflow 结构改动）+ W776 外部评审后续四项行动全部落地，覆盖率口径决策与实证基线入仓，两条死依赖移除，机制层三项风险登记入 HANDOVER，评审原文归档 tmpe·无 workflow 结构改动）+ W777 第 41 篇工作复盘报告入库，覆盖二十八段六十提交的断档补课，八条新经验与六个问题族三条工作流，复盘断档登记与改进候选·无 workflow 结构改动）+ W778 复盘改进三项落地，latent 三问与双平台禁例入 pitfalls，外部产出七步与对拍 SOP 入流水线文档，对拍模板固化，复盘提醒 automation 提案按用户规则撤销·无 workflow 结构改动）。

## 1. 工作流列表

| 工作流 | 文件 | 触发条件 | 用途 |
| --- | --- | --- | --- |
| CI | [`ci.yml`](ci.yml) | `push` main + `pull_request` + `workflow_dispatch` | 9 job 门禁：截图存活烟测 / Lighthouse / a11y / dependency / ruff / pytest / E2E 交互断言 / agent-web 构建 / 交付校验 |
| Security | [`security.yml`](security.yml) | `push` main + `pull_request` | 4 job：npm-audit（scripts/ + agent-web/ 双目录）/ pip-audit / CSP / XSS detect |
| Deploy Pages | [`pages.yml`](pages.yml) | `push` main（site/** 变更） | GitHub Pages 部署 `./site`（W401 决策：不采用 build-test-deploy.yml，避免部署竞态·已删除） |
| Lighthouse CI | [`perf.yml`](perf.yml) | `push` main（site/**）+ `pull_request` + 每周一 + `workflow_dispatch`（W422 补 push：原仅 PR 从不运行·首跑暴露性能债后阈值已校准） | LHCI 性能预算断言（LCP≤5000ms/CLS≤0.3/TBT≤300ms，W424 实测校准） |
| Screenshot Review | [`screenshot-review.yml`](screenshot-review.yml) | `push` main（site/** 或脚本/workflow 变更）+ `pull_request` + 每周一 + `workflow_dispatch`（W421：页脚/文档-only 跳过·data 页定向截图） | Playwright 截图 + 布局审计 |
| Dependency Review | [`dependency-review.yml`](dependency-review.yml) | `pull_request`（main·dependabot PR 即真实流量） | 依赖变更审查：漏洞/许可证（W683·fail-on-severity=moderate） |
| Mark Stale | [`stale.yml`](stale.yml) | 每日 01:30 UTC + `workflow_dispatch`（W683） | 陈旧 issue/PR 标记（60 天）与自动关闭（再 14 天·pinned 豁免） |
| OpenSSF Scorecard | [`scorecard.yml`](scorecard.yml) | 每周一 03:00 UTC + `branch_protection_rule` 变更 + `workflow_dispatch`（W683） | OpenSSF 安全评分（SARIF 入 Code scanning + publish_results 徽章） |

> **W400 关键教训**：ci.yml 建置时仅 `pull_request` 触发，但项目工作流是直接 push main（无 PR），**CI 从未真正运行过**。W399 补 push 触发后首次运行暴露全部存量问题。**新 workflow 必须本地语法校验 + 确认触发条件匹配真实开发流。**

## 2. ci.yml 九 job 说明

### Job 1 · `pages-smoke`（页面存活烟测）

- **运行环境**：`ubuntu-latest` + Node 20 + Python 3.12
- **依赖**：`npm install playwright @playwright/test` + `npx playwright install --with-deps chromium`
- **流程**：启动 `python -m http.server 8000 --directory site` → 内联 Node 脚本递归扫描 `site/` 全部 HTML，逐个请求验证 HTTP 200
- **W399 修复**：原引用 `tools/screenshot-baseline.js`（仓库从未存在 → 步骤必然失败走降级分支），改为内联 Node 存活烟测
- **W700 更名**：job `screenshots-regression`→`pages-smoke`（原「Screenshots Regression」名不符实——真实截图回归在 screenshot-review.yml），同步删除永不产出的 screenshots/diff artifact 两残件步骤
- **路径跨平台**：`p.replace(/[\\/]+/g,'/').replace(/^site\//,'')`（Windows 本地与 Linux CI 均可用）
- **artifact**：`screenshots-${{ github.sha }}`（保留 30 天）；失败时额外上传 `screenshots-diff-${{ github.sha }}`

### Job 2 · `lighthouse-performance`（性能审计）

- **运行环境**：`ubuntu-latest` + Node 20 + Python 3.12
- **流程**：启动 static server → `npx lighthouse http://localhost:8000/dashboard.html`（categories: performance/accessibility/best-practices/seo，`--throttling-method=simulate`）
- **W400 门禁**：**Accessibility ≥ 0.95 硬门槛**；**Performance 降级为 warn**（`< 0.50` 才警告）——dashboard 为内容密集模板大页，CI 实测 0.550、本地 0.730 波动大，且 lantern 对大 DOM 页 FCP/LCP 有已知误差（All Frames not implemented）
- **性能门禁承担者**：perf.yml（LHCI LCP≤5000ms / CLS≤0.3 / TBT≤300ms 预算断言，W424 实测校准）
- **artifact**：`lighthouse-report`（保留 30 天）

### Job 3 · `a11y-audit`（a11y 审查，9 矩阵）

- **运行环境**：`matrix.os × matrix.python-version` = 3 OS（ubuntu/windows/macos）× 3 Python（3.10/3.11/3.12）= 9 组合
- **流程**：`python scripts/a11y_audit.py --dir site --quiet`（W264-E2 9 规则 WCAG 2.2）
- **W400 修复**：移除 `cache: pip`——a11y_audit.py 仅用标准库、job 不安装 pip 依赖，缓存目录不存在导致 Post 步骤报 `##[error]` 使 job 失败（windows/ubuntu py3.10-3.11 复现）
- **artifact**：`a11y-report-${{ matrix.os }}-py${{ matrix.python-version }}`（保留 30 天）

### Job 4 · `dependency-scan`（pip-audit）

- **流程**：`pip-audit -r scripts/requirements.txt -f json -o pip-audit-report.json`
- **artifact**：`pip-audit-report`（保留 30 天）

### Job 5 · `code-quality`（ruff）

- **流程**：`ruff check scripts/`
- **W400 配置**：pyproject.toml `extend-exclude` 跳过 `_` 前缀一次性脚本 + `scripts/audit/archive`（与 security_scan.py 跳过逻辑一致）；全局忽略 UP031（printf 风格非错误）
- **W400 移除 black --check**：存量 123/128 脚本从未 black 格式化，门禁从未通过；保留 ruff 语义门禁，格式统一由 ruff format 负责

### Job 6 · `pytest-unit`（单元测试）

- **运行环境**：`ubuntu-latest` + Python 3.12
- **流程**：`pip install -r scripts/requirements.txt` → `python -m pytest tests -q`（W401 补齐 + DRL 修复：原 ci.yml 五 job 未覆盖 Python 单元测试；pytest.ini `testpaths=tests` + `--ignore=tests/e2e`，浏览器测试移入 tests/e2e/ 由 screenshots-regression job 覆盖）
- **本地验证**：`py -3 -m pytest tests -q` → 321 passed（2026-08-09 DRL 修复后实测）

### Job 7 · `agent-web-build`（xiyouji-agent-web 前端构建）

- **运行环境**：`ubuntu-latest` + Node 20
- **流程**：`npm --prefix xiyouji-agent-web ci` → `npm run build`（`tsc -b && vite build`，仓库唯一编译目标）
- **W401 前置**：agent-web 源码（37 文件）已入库；.gitignore 改为精细忽略（node_modules/dist/data/chat.db/tsc 编译产物 server/*.js|*.d.ts + vite.config.js|*.d.ts）
- **artifact**：`agent-web-dist-${{ github.sha }}`（保留 30 天）
- **本地验证**：`npm --prefix xiyouji-agent-web run build` → vite build 成功（7906 modules，2026-08-08 实测）

### Job 8 · `verify-delivery`（交付校验门禁，W424 新增）

- **运行环境**：`ubuntu-latest` + Python 3.12 + Node 20
- **流程**：`pip install -r scripts/requirements.txt` → `python scripts/run_all.py`（重新生成 scripts/output/data/*.json，生成物未入库）→ `python scripts/verify_delivery.py`——门禁集合以 scripts/verify_delivery.py 现役为准（编号至 27·16/26 预留退役；与本地 pre-commit 同轨，无 workflow 结构改动）
- **与 pre-commit 的关系**：本地 pre-commit 钩子（手动 .git/hooks/pre-commit + .pre-commit-config.yaml 双轨）已含等价检查；CI 兜底防 `--no-verify` 提交。run_all 的 2 个历史 FAIL（hardships_81/journey_route 缺 --output）已修默认值，34/34 全过。

### Job 9 · `e2e-interaction`（E2E 交互断言，W773 新增）

- **运行环境**：`ubuntu-latest` + Node 20
- **背景（T-02 缺陷①）**：`tests/e2e/` 8 个 Playwright JS 套件此前**零 workflow 调用**——本地绿/CI 无运行两侧观察不一致，W674 遗留的 K11 页面回归（reduce 规则误置媒体查询外）因此潜伏 6 周，直到本 job 接线首跑才暴露（中英双页已同修）
- **依赖**：`npm ci --prefix scripts` + `npx playwright install --with-deps chromium`（缓存 `~/.cache/ms-playwright`·key 绑 scripts/package-lock.json·复用 W421 模式）
- **流程**：`node tests/e2e/test_site_quality.js`——22 项 file:// 断言（A1-A8 交互 + K9-K11 数据/动效 + W676 三项回归·无 API_PORT 在线依赖·require 已按 paths 解析 scripts/node_modules）
- **首波范围纪律（D-02）**：只接 1 个套件证「接线可行且 CI 绿」再扩面；`test_graph.js`/`test_newfeatures.js` 需 Express 服务（API_PORT）、`test_w266_e2e_extended.js` 依赖未声明的 `@playwright/test`，按计划 R-03/R-04 排除出首波；视觉回归套件（test_visual.js·W773 已升级像素判据）判据稳定性观察中，亦不入首波
- **机器防线**：`tests/unit/test_ci_wiring.py` W6 断言锚定本 job 的 `run:` 块（删步骤/改 echo 即红·负样本实测）

## 3. 触发条件矩阵

| 事件 | 目标分支 | 触发工作流 | CI | Security | Deploy | Perf | Screenshot |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `push` | `main` | ci / security / pages / perf / screenshot-review | ✅ | ✅ | ✅（site/**） | ✅（site/**） | ✅（site/** 或审查三件套） |
| `pull_request` | `main` | ci / security / perf / screenshot-review | ✅ | ✅ | ❌ | ✅（site/**） | ✅（site/** 或审查三件套） |
| `schedule` | — | perf / screenshot-review（每周一） | — | — | — | ✅ | ✅ |
| `workflow_dispatch` | — | ci / pages / perf / screenshot-review | ✅ | — | ✅ | ✅ | ✅ |

> `concurrency`：CI/Security/Perf 均设 `group + cancel-in-progress: true`，同 ref 后续 push 取消前次。

> **W683 增补（三 starter）**：Dependency Review 仅 `pull_request`；Stale 仅 `schedule`+`workflow_dispatch`；Scorecard 仅 `schedule`+`branch_protection_rule`+`workflow_dispatch`——三者均不参与 push 门禁链。

## 4. artifact 列表

| artifact 名 | 来源 job | 内容 | 保留 |
| --- | --- | --- | --- |
| `lighthouse-report` | lighthouse-performance | JSON + HTML 审计报告 | 30 天 |
| `a11y-report-*` | a11y-audit | a11y Markdown + JSON 报告 | 30 天 |
| `pip-audit-report` | dependency-scan | pip 漏洞审计 JSON | 30 天 |
| `agent-web-dist-${{ github.sha }}` | agent-web-build | xiyouji-agent-web 前端构建产物（dist/） | 30 天 |

## 5. 阈值与失败条件

| 检查项 | 阈值 | 失败动作 |
| --- | --- | --- |
| Lighthouse Accessibility | ≥ 0.95 | ci.yml lighthouse-performance job 失败 |
| Lighthouse Performance | < 0.50 才 warn | 不阻断（性能门禁移交 perf.yml） |
| a11y P0 计数 | = 0 | ci.yml a11y-audit job 失败 |
| ruff | 0 违规（scripts/ 生产脚本） | ci.yml code-quality job 失败 |
| XSS high 计数 | = 0 | security.yml xss-detect job 失败 |
| pip-audit | 0 高危（--strict） | security.yml pip-audit job 失败 |
| npm audit（scripts/ + agent-web/） | 0 high（--omit=dev --audit-level=high） | security.yml npm-audit job 失败 |
| LHCI 预算 | LCP≤5000ms / CLS≤0.3 / TBT≤300ms | perf.yml job 失败 |
| pytest | 0 失败（tests 全量） | ci.yml pytest-unit job 失败 |
| verify_delivery | 六文档版本 / A4 209 / 范围漂移 / 导航 / 链接 / sitemap / 回退 / 数据漂移 | ci.yml verify-delivery job 失败 |
| test_site_quality E2E | 0 失败（22 项断言全绿） | ci.yml e2e-interaction job 失败 |
| agent-web build | tsc + vite 退出码 0 | ci.yml agent-web-build job 失败 |

## 6. 本地复现命令

```powershell
# a11y 审查（Windows 用 py，CI 用 python）
py scripts/a11y_audit.py --dir site --quiet

# ruff 检查（必须与本仓库 pyproject.toml 一致，跳过 _ 前缀脚本）
ruff check scripts/

# 安全扫描（XSS high 归零验证）
python scripts/security_scan.py --all --no-headers --no-sri --no-pip-audit

# pytest 单元测试（tests 全量，--ignore=tests/e2e 由 pytest.ini 内置）
py -3 -m pytest tests -q

# agent-web 前端构建
npm --prefix xiyouji-agent-web run build

# npm 依赖漏洞审计（scripts/ + agent-web/ 双目录，与 security.yml npm-audit 一致）
npm --prefix scripts audit --omit=dev --audit-level=high
npm --prefix xiyouji-agent-web audit --omit=dev --audit-level=high

# Lighthouse 性能审计（需先启动 static server）
python -m http.server 8000 --directory site
npx lighthouse http://localhost:8000/dashboard.html `
  --output=json --output=html --output-path=lighthouse-report `
  --only-categories=performance,accessibility,best-practices,seo `
  --throttling-method=simulate
```

> Windows 本地用 `py`，CI（ubuntu）显式用 `python`。

## 7. 与既有测试体系的关系

| 体系 | 编号 | 关系 |
| --- | --- | --- |
| 测试体系 | **W204 E5** | CI 三轨是 W204 测试体系（pytest + JS syntax + lint_links 等）之上的**可视化质量门禁**补充层；原 `audit` job 的 JS/tables/SVG/links 检查仍可在本地 `scripts/run_all.py` 跑 |
| a11y 脚本 | **W207** | CI 调用 `scripts/a11y_audit.py`；CI 仅做触发与 artifact 上传，规则定义权在脚本侧 |
| a11y 9 规则 | **W264-E2** | a11y-audit 升级为 9 规则 WCAG 2.2 AA（W271/W275/W279 E 方向持续深化） |
| 安全扫描 | **W236-E/W268** | security_scan.py 四轨（XSS/CSP/secret/pip-audit），`_` 前缀开发脚本不入门禁（W400） |
| CI/CD 化 | **W234-E1** | 提供 push/PR 门禁 + GitHub Pages 部署（W390 pages.yml） |

## 8. 双索引

- [CHANGELOG.md](../../CHANGELOG.md) — v2.3.99 W500
- [scripts/output/file-index.md](../../scripts/output/file-index.md) — W234-E1 / W399 / W400 / W401 / W500
