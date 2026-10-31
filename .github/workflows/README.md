# CI/CD 工作流说明

> **W234-E1 CI/CD 化 → W399/W400/W401/W410/W411/W412/W413/W414/W415/W416/W417/W418/W419/W420/W421/W422/W423/W424/W425/W426 → W450-W1063** — 西游记解读项目（`D:\xiyouji`，W1063）的 GitHub Actions 工作流层。
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
> **W450-W1063**：verify 门禁体系扩展（W458-W649 历批逐条明细见 CHANGELOG；实质改动 workflow 文件的仅 W523 diff quotePath/W536 dependabot ignore+eslint/W563 defer 与 SW 探针/W571 tokens 分发/W578 dark-state-gate 浅克隆五批，W450 前建批见 git log）+ W464 perf 基线确立（perf.yml 预算沿用 W424 校准值 LCP≤5000/CLS≤0.3/TBT≤300）+ 其余 W450-W649 各批无 workflow 结构改动）+ W650 第 28 门禁加固与 PRD 出库·无 workflow 结构改动）+ W651 全量启动裁决入档与三源快照·无 workflow 结构改动）+ W652 PD-5 设计令牌导出与对账门禁·无 workflow 结构改动）+ W653 PD-1a 色盲安全门禁·无 workflow 结构改动）+ W654 PD-1b 选型章与降级门禁·无 workflow 结构改动）+ W655 B-9 之一 D3 色值变量化·无 workflow 结构改动）+ W656 B-9 之一 audit 补丁合并单模块·无 workflow 结构改动）+ W657 B-6 第二步可引用性组件·无 workflow 结构改动）+ W658 B-7 分析方法 pip 包·+ 663 治理经验移植批·W659-W663 合并登记·CI 加固：61 处 uses 改 SHA 钉+顶层 permissions 收敛+security dispatch·无 workflow 结构改动）+ W664 CLAUDE.md 速查层+写作可验证纪律·无 workflow 结构改动）+ W666 工作复盘报告入库·无 workflow 结构改动）+ W661 WP-D2 索引站内化+footer-meta 改链·无 workflow 结构改动）+ W667 复盘三卡防漂移落地·无 workflow 结构改动）+ W662 暗色审计入基线+遗漏收敛·无 workflow 结构改动）+ W668 数据评审裁决落地·无 workflow 结构改动）+ W669 WP-E 内容发现架构·无 workflow 结构改动）+ W670 开放项双闭与默认源治理·无 workflow 结构改动）+ W671 共享载体治理·无 workflow 结构改动）+ W672 站点质量批次一·无 workflow 结构改动）+ W673 站点质量批次二·无 workflow 结构改动）+ W674 站点质量批次三·无 workflow 结构改动）+ W675 工作复盘报告入库·无 workflow 结构改动）+ W679 workflow 工业化方案入库与评估密钥引导·无 workflow 结构改动）+ W680 agent-web 引擎更换与全模型适配·无 workflow 结构改动）+ W681 品牌清零与归档治理（三归档件移 docs/archive/·现役面无 workflow 结构改动）+ W683 新增三 starter workflow（dependency-review/stale/scorecard·全 SHA 钉）+ W684 工作复盘报告入库·无 workflow 结构改动）+ W685 复盘下半场报告入库与工具收尾·无 workflow 结构改动）+ W686 workflow 方案退役与预留清理·无 workflow 结构改动）+ W687 S4 外部审读处置与投稿体系批·无 workflow 结构改动）+ W688 第六轮复审处置迷你批·无 workflow 结构改动）+ W689 全变动对抗复审修复批·无 workflow 结构改动）+ W690 安全告警处置·无 workflow 结构改动）+ W676 站点质量修复批次四·无 workflow 结构改动）+ W677 站点质量修复批次五·无 workflow 结构改动）+ W678 站点质量修复批次六·无 workflow 结构改动）+ W691 Backlog 裁决执行批·无 workflow 结构改动）+ W692 复盘报告入库批次·无 workflow 结构改动）+ W693 用户三裁决执行批·无 workflow 结构改动）+ W694 故事内时间线可视化页落地批·无 workflow 结构改动）+ W695 第 39 门禁挂载与 CSP 全站收紧批·无 workflow 结构改动）+ W696 复盘报告第二篇入库批次·无 workflow 结构改动）+ W697 复盘报告第四篇入库批·无 workflow 结构改动）+ W698 门禁scope分级与提交重试批·无 workflow 结构改动）+ W699 三卡工具化与三报告批·无 workflow 结构改动）+ W700 docs全量链接门禁与断链清债批·无 workflow 结构改动）+ W701 BL-20动工与S-26工具化批·无 workflow 结构改动）+ W702 六文档口径清债批·无 workflow 结构改动）+ W703 聚合数字对账门禁批·无 workflow 结构改动）+ W704 数字实体化批·无 workflow 结构改动）+ W705 Agent开局状态摘要批·无 workflow 结构改动）+ W706 编号空间盘点与元规则批·无 workflow 结构改动）+ W707 分层重构先行件与阅读契约批·无 workflow 结构改动）+ W708 全变动对抗复审修复批·无 workflow 结构改动）+ W709 BL-24分层搬迁批·无 workflow 结构改动）+ W710 BL-25与BL-21收口批·无 workflow 结构改动）+ W711 方案D形态改造批·无 workflow 结构改动）+ W712 方案档挑刺补正批·无 workflow 结构改动）+ W713 挑刺第十四次补正批·无 workflow 结构改动）+ W714 停用守卫与考古补库批·无 workflow 结构改动）+ W715 工作复盘报告批·无 workflow 结构改动）+ W716 stats 实体化补正批·无 workflow 结构改动）+ W717 页脚链头锚定根修批·无 workflow 结构改动）+ W718 变更史可追踪补正批·无 workflow 结构改动）+ W719 review 修复批·无 workflow 结构改动）+ W720 C4 认领行强制批·无 workflow 结构改动）+ W721 复盘增补与脚注滚动根修批·无 workflow 结构改动）+ W722 八项裁决执行批·无 workflow 结构改动）+ W723 级联清单反向覆盖根修批·无 workflow 结构改动）+ W724 页脚链损坏修复与链长治理批·无 workflow 结构改动）+ W725 review 收官 mini 批·无 workflow 结构改动）+ W726 本地工具链修复批·无 workflow 结构改动）+ W727 SVG 保护补打与级联根修批·无 workflow 结构改动）+ W728 门禁与工具链代码重构·无 workflow 结构改动）+ W729 性能与可访问性工具链重构·无 workflow 结构改动）+ W730 门禁脚本长函数收尾重构·无 workflow 结构改动）+ W731 发布工具链与安全扫描重构·无 workflow 结构改动）+ W732 性能与文档工具链重构·无 workflow 结构改动）+ W733 达标收尾六目标拆编·无 workflow 结构改动）+ W734 归档体系统一与交接文档更名·无 workflow 结构改动）+ W735 全仓归档大扫除·无 workflow 结构改动）+ W736 发布链工具化与文档负载治理·无 workflow 结构改动）+ W737 对抗性审查修复与报告归置·无 workflow 结构改动）+ W738 tmpe 临时文件体系策略化治理·无 workflow 结构改动）+ W739 对账表 touches 冲突声明与 preflight 交集拒绝落地·无 workflow 结构改动）+ W740 干扰治理穷举分析收敛为决策实施路线图·无 workflow 结构改动）+ W741 评估实施记录入库与 is_inflight 全星号剥离加固·无 workflow 结构改动）+ W742 复盘入库与反向扫描与计数第四检·无 workflow 结构改动）+ W743 融合层消融与加权重构·无 workflow 结构改动）+ W744 检索增强管线集成与四档开关·无 workflow 结构改动）+ W745 改写档智能路由化·无 workflow 结构改动）+ W746 路由端点与模块转正·无 workflow 结构改动）+ W747 能力总览与边界沉淀·无 workflow 结构改动）+ W748 双线收官复盘入库·无 workflow 结构改动）+ W749 ML import 坑入 pitfalls·无 workflow 结构改动）+ W751 根级工具链防护批·无 workflow 结构改动）+ W754 方法论目录全量校订（必修 4 类 + 建议改 8 类 + 索引重写）·无 workflow 结构改动）+ W755 方法论深度篇扩建与治理口径统一（新增深度篇加治理修复）·无 workflow 结构改动）+ W756 人名用字语料纯度与口径登记（清语料加口径登记）·无 workflow 结构改动）+ W757 CI 门禁接线缺陷修复批（verify-delivery job 补 Playwright 安装+缓存·D1 第 43 门禁此前 CI 必红；agent-web-build job 补 test:server·D2 安全单测此前未接线；两处均为 workflow 结构改动；W758 起无 workflow 结构改动）+ W758 CI 首跑暴露缺陷修复批（平台守卫加依赖登记加门禁加固）·无 workflow 结构改动）+ W759 脚注滚动断言与指针注记刷新根修（编号空洞兼容）·无 workflow 结构改动）+ W760 全量对抗性审查（3327 入库件，五可标准，六个审查面）收官，11 项发现 4 HIGH，25 个证据脚本可复跑，正面结论独立复算·无 workflow 结构改动）+ W761 守卫单模块化，重复消除，复杂函数拆分，命名体系统一，潜伏缺陷修复（行为零变化，对拍验证）·无 workflow 结构改动）+ W762 重构报告晋升入库（README 索引重编号 18→19，STRUCTURE 标记 21→22，stats 三连带刷新）·无 workflow 结构改动）+ W763 F-1a 照录区字级篡改全量修复（97 处修 9 文件，占位符约定与语料疑点登记不修，行尾纯净）·无 workflow 结构改动）+ W764 S-01 RCE 修复（git pager 族参数层拦截 + 全命令 shell 元字符二次校验，38 例单测含 5 拒 1 放行）·无 workflow 结构改动）+ W765 a11y_audit 收尾重构（增强辅助族注释统一 + rule_29_parsing 74 行拆为编排器加三检测臂，行为对拍逐字节一致）·无 workflow 结构改动）+ W766 F-1b C 类 59 条静默删改全量处置（51 修复+8 语料疑点登记，引文与语料逐字对齐，引文门禁 100%）·无 workflow 结构改动）+ W767 第 9 门禁口径修复（共路标量深比对+声明式基线）+F-7 双 KPI 修正+存量漂移清理·无 workflow 结构改动）+ W768 第 44 槽挂载（validate_en --all，138 页 script CJK=0）+6 页整改+豁免基线移除·无 workflow 结构改动）+ W769 动效 duration 全站归一（37 处至≤600+第 13 门禁补规则）+统计口径说明 86→87 级联（8 处现役文案+C5 域扩展）·无 workflow 结构改动）+ W770 F-2 文首文件级演绎标记识别（两判定面）+hardships 生成器 label 化输出对齐+副本回灌与字节自检工具恢复+F-8 复核·无 workflow 结构改动）+ W771 F-9 收口：区间缺号三源定性登记去向 + 门禁注释陈旧数字刷新·无 workflow 结构改动）+ W772 计划方案三篇登记入库加索引重建加报告计数 22 到 23·无 workflow 结构改动）+ W773 工程基础设施薄弱点修复（E2E 接线，视觉回归重建，英文站 a11y 补面，索引漂移门禁）·ci.yml 新增 e2e-interaction job·一处 workflow 结构改动·视觉回归与 a11y 与索引门禁均无 workflow 结构改动）+ W774 CI 首跑分歧修复（docs_index 跨平台排序根修加回归测试）与 T-02 推送闭环·无 workflow 结构改动）+ W775 JS 门禁重构落地，两公共模块与三脚本重写，外部契约五维对拍零漂移，顺手修复数据漂移门禁静默跳过两页的潜伏缺陷，外部评审七项指控逐条核查·无 workflow 结构改动）+ W776 外部评审后续四项行动全部落地，覆盖率口径决策与实证基线入仓，两条死依赖移除，机制层三项风险登记入 HANDOVER，评审原文归档 tmpe·无 workflow 结构改动）+ W777 第 41 篇工作复盘报告入库，覆盖二十八段六十提交的断档补课，八条新经验与六个问题族三条工作流，复盘断档登记与改进候选·无 workflow 结构改动）+ W778 复盘改进三项落地，latent 三问与双平台禁例入 pitfalls，外部产出七步与对拍 SOP 入流水线文档，对拍模板固化，复盘提醒 automation 提案按用户规则撤销·无 workflow 结构改动）+ W780 目录文档新鲜度门禁挂载第 45 槽，生成器治理排除与大小写冲突判定模块化并新增 refresh 安全刷新模式使修复路径闭环，三方槽位同步与速查表存量漂移顺修，stats gate_count 随批刷新·无 workflow 结构改动）+ W781 门禁防线收口三项落地，挂槽注册表派生与启动期一致性断言收敛五处同改并补自洽锁反向查，spec desc 批次号开头防线前移加页脚插入防御剥离，治理文档契约门禁转正阻断·无 workflow 结构改动）+ W782 外部重构提案收编第一批，四件 utils 加 run_all 行为保持重构，aliases 懒加载改 lru_cache 并更名反向索引构建函数，text_loader 与 analyzer_base 与 run_all 拆函数提常量，path_guard 按对账面禁改写自述跳过，对拍验收为全量重跑输出逐字节相等·无 workflow 结构改动）+ W783 外部重构提案收编第二批，character_appearance 拆聚合三函数并提首回计算函数保急切求值语义，character_network 拆共现累积函数 combinations 等价改写，character_nlp 整文件重写提案本批不收留待机械通道，对拍验收为两脚本前后输出逐字节相等·无 workflow 结构改动）+ W784 外部重构提案收编第三批小件档，chapter_stats 诗词计数拆双函数聚合提 _aggregate_totals，word_frequency 提 _is_valid_token 与最短长度常量，narrative_experiment 拆输出口志函数 build_summary 两次调用改一次复用，hardships_81 三标签字典提模块级并拆交叉统计与 label 化函数，line_check self_test 拆三查并提 _query_one，对拍验收为五脚本前后输出逐字节相等·无 workflow 结构改动）+ W785 外部重构提案收编第四批重件档其一，CORS 白名单与 MIME 映射与检索片段窗口提模块级常量，do_GET 路由拆四臂处理方法并新增 _send_error_json 统一错误结构，文档页表格行渲染提 _render_dataset_row，全部路由状态码与响应体逐字节保持，对拍为起服务前后十一个端点工件逐字节比对·无 workflow 结构改动）+ W786 外部重构提案收编第五批，Cypher 拼装提 _build_cypher 快照组装提 _build_snapshot OUTPUT 中间变量收敛路径拼接，rag 家族其余五件不收留机械通道，对拍验收为两产物与运行日志逐字节相等·无 workflow 结构改动）+ W787 外部重构提案收编第六批末批，分隔线与告警线常量化并提步进标题函数，git 状态与体量解析与版本解析拆函数，22 项门禁脚本改动点清单经裁定不执行，对拍验收为完整运行输出与退出码逐字相同·无 workflow 结构改动）+ W788 重构收尾清理两处无消费点代码，截图门禁删新增死常量公共模块删未用导入，净删两行零行为变化，验收为截图门禁八百五十七页逐页结果相同加破防态负样本可红加自检十二例通过·无 workflow 结构改动）+ W789 外部门禁重构提案对盘登记，逐字节提取五文件与磁盘现势比对，提案十五项改动已全部由此前重构批次落地，余量七处差异均为改号回退或等价噪声，裁定不执行，零代码变更，登记以防重复收编·无 workflow 结构改动）+ W790 外部评审第三轮重复投递逐条核查回应，七项与上轮全同且事实已漂移，四项不成立三项部分成立，唯一实质增量为 agent 攻击面负向测试缺口，报告归档并联登四条待办·无 workflow 结构改动）+ W791 agent-web 三类攻击面负向测试固化，安全逻辑提取得可测面，真服集成覆盖限流与鉴权，计划状态陈滞回写，服务端测试套件扩充至六十七例·无 workflow 结构改动）+ W792 全仓待办计划方案状态核查，逐项取证判定无假收敛，五处陈滞修正落地，真开面约三十项多为作者时间类，四项待用户决策·无 workflow 结构改动）+ W793 产品设计套件两页启发式走查落地，八条发现全部防虚构校验，sync_docs 退休替换为现役门禁，冻结适用范围立单一表述·无 workflow 结构改动）+ W794 PD-3 三项裁决全部落地，首页补随笔入口与全卷命名，数据提示改读者语，专题卡加图例与悬停明细，自查撤回一条假阳性·无 workflow 结构改动）+ W795 第 42 篇复盘报告入库，覆盖十八段三十九提交，外部输入三段处置与本地绿 CI 红第三型与探针自证伪三条主线，八条新经验三问题族两工作流五改进项·无 workflow 结构改动）+ W796 桌面提示词合集整理入库，九百六十六行拆为十二文件逐行照录，二十组色值逐条校准四组以十六进制为准，七段审查合并为任务书，隐私边界独立前置·无 workflow 结构改动）+ W797 三件历史模板按仓库惯例归馆，有效条目提炼为交付自检十项入文档规范，本地 PRD 维持出库裁决不动·无 workflow 结构改动）+ W798 对拍模板从工地转正入库并同步路径引用，临时区本轮归桶清垃圾约一点三吉字节，近作实验数据保留待定·无 workflow 结构改动）+ W799 截图桶保留期由三十天收紧至七天并按新规清理四十兆，临时区总量复核五百七十四兆，删除期读数差异归因记录·无 workflow 结构改动）+ W800 第四轮评审逐条判定并公开门禁保真不保质边界，阅读契约后移读者优先，维度分层与数据基础限制公开，三项登记一项即关·无 workflow 结构改动）+ W801 两处最大函数拆为职责单一小函数，旧新两版五件产物与标准输出逐字节一致，发现并登记一处生成非确定性·无 workflow 结构改动）+ W802 同模块剩余两处八十九与八十五行长函数各拆为三至四小函数，同路径对拍逐字节一致，取证法修正路径伪差·无 workflow 结构改动）+ W803 五个门禁族收敛公共骨架加 MCP 长函数拆分加 Web Agent 服务端按职责分文件，全部以新旧对拍与构建测试证明行为不变·无 workflow 结构改动）+ W804 桌面版三平台安装包与自动更新发布流水线·新增 release.yml 发布工作流与 ci.yml desktop-build job（两处 workflow 结构改动）·自动更新链路仍无 workflow 结构改动）+ W805 跨平台测试守卫热修·无 workflow 结构改动）+ W806 GoatCounter 统计链彻底退役·ci.yml 接入防回退守卫与 perf.yml 去失效 blocked pattern（两处 workflow 改动）·其余门禁接线无 workflow 结构改动）+ W807 站内搜索索引刷新·无 workflow 结构改动）+ W808 Web Agent 全栈加固（后端生产化 + 前端集成层 + 测试三件套）·无 workflow 结构改动）+ W809 站内搜索索引新鲜度门禁挂载·无 workflow 结构改动）+ W810 站内搜索两页 legacy 死数组清理·无 workflow 结构改动）+ W811 CI 断链修复（工作流 YAML 歧义语法 + 可解析性守卫）·无 workflow 结构改动）+ W812 去旧厂商 Agent 工具品牌化（工具环境解耦 + 全仓去品牌）·无 workflow 结构改动）+ W813 review 修复：P1 契约回归 + P2 门禁真空 + P3 CI 防线失效·无 workflow 结构改动）+ W814 去品牌扩展：另两个同类品牌字面一并纳入禁令并全仓清除·无 workflow 结构改动）+ W815 shell 查坑表补两条：内联 Python 的 $ 展开与引号配对坑·无 workflow 结构改动）+ W816 门禁判据可信化：引文门禁 cwd 依赖与零文件守卫 + 安全扫描构建产物排除失效与 XSS 规则覆盖缺口 + 认领行状态回填·无 workflow 结构改动）+ W817 工具层工作目录边界加固：受保护路径黑名单去 cwd 锚定 + 路径守卫解析后判越界 + git 输出重定向空格形态拦截 + 遍历类工具过黑名单·无 workflow 结构改动）+ W818 静态站与可视化页前端框架化技术选型五维对齐与推荐结论·无 workflow 结构改动）+ W820 补登 4 天缺失的干扰日志 + 判定口径加严 + 登记机制自身缺陷·无 workflow 结构改动）+ W821 系统架构方案八维成文：整体分层、模块拆分与依赖、数据流、存储选型、扩展性、容灾降级、部署拓扑、监控指标·无 workflow 结构改动）+ W822 干扰日志机器触发点（真触发才提示，不改判定与退出码）·无 workflow 结构改动）+ W823 SQLite 存储层表设计审查：字段类型与约束、索引与查询模式、范式与冗余取舍、扩展性与历史数据处理四维取证，13 项发现按影响程度分级，修复未动工·无 workflow 结构改动）+ W824 站内阅读入口打通批首步：T-04 执行前计划落库，实证站点 622 页 reader 阅读内容站内入链为 0，入口打通与阅读页体验封装分两批立项，施工待下一轮·无 workflow 结构改动）+ W825 前端流式链路修复与门禁解析层加固·无 workflow 结构改动）+ W827 修 P0-01：622 页 reader 阅读内容站内入链为 0，本次在首页与导读页打通五处入口（主导航 阅读 项 首屏 开始阅读 CTA 4 条场景化直达 全卷索引 逐回精读 行 导读页导航与首条阅读路径），不改 reader 页 不新增页面 零外域请求·无 workflow 结构改动）+ W841 补 precheck 覆盖不到的手工写段路径：三处版本行的 desc 段禁含分隔符，非空文档形态不识别即判红，自测加负样本与防误伤正样本各一例·无 workflow 结构改动）+ W842 补段工具一次补齐十二批欠账，让号序链重新接上，并顺手修正 pytest 收集数 785 到 786 的真漂移·无 workflow 结构改动）+ W843 把上一批施工中新踩的两条坑固化进查坑表，同批校准智能体指南的分节计数与总数·无 workflow 结构改动）+ W844 四处施工一次落地：会话库备份、首 token 计时、多租户与检索两项裁决回填，以及检索题集迁入仓内并扩到百题·无 workflow 结构改动）+ W845 把待批的阅读页改造先量一遍：在隔离副本里按三段管线重建全部阅读页、逐文件比对出真实影响面，并纠正计划里只跑单个脚本的量法·无 workflow 结构改动）+ W846 按三段管线重建全部阅读页，把 docs 源里积压的字级修复回灌进正文，产物结构与样式零变化·无 workflow 结构改动）+ W847 阅读页四项体验落地：速览折叠、进度与书签字号、每页反馈，以及重建幂等复验·无 workflow 结构改动）+ W848 检索增强默认档不动，把 dense 升为写明适用边界与代价的显式可选档，并修掉档位表旧口径冲突·无 workflow 结构改动）+ W849 在交付门禁挂上性能影子槽，按批采静态成本代理攒基线，暂不判红也不设阈值·无 workflow 结构改动）+ W850 补齐 Q2 悬空的真因，把等十批样本从口号变成可执行的按批采集机制·无 workflow 结构改动）+ W851 把 W826 细化规格 §4 的 v4 令牌增量落进 tokens.css，只落零消费新名、撞名项 defer，用机器证明现役页面视觉零变化·无 workflow 结构改动）+ W863 把十一个已收官但未立段的批次按号序补回 CHANGELOG 与 file-index，让级联的号序断言重新成立·无 workflow 结构改动）+ W864 十页结构页按裁决迁移：KPI 顶条收敛到首卡、徽章转淡底、间距令牌化 216 处，C 渠与 chart-3 拆专项批·无 workflow 结构改动）+ W874 把九个递延批按号序补回 CHANGELOG 与 file-index，让级联断言重新成立、B11 可进·无 workflow 结构改动）+ W876 C 渠规则级换色 173 条（落 bg 1087→253 降 77%）+ chart-3 与暗色 accent 两处值切换 + inline_css 回吞迁移事故修复（328 页自 HEAD 重建）·无 workflow 结构改动）+ W883 朱砂实底常驻门禁挂第 49 槽（浏览器计算样式实测 每页非豁免超 3 即拦 增量缓存）且六段递延账一次结清·无 workflow 结构改动）+ W886 en 首批 28 页迁到位 C 渠 49 条规则 + seal 淡底 28 页 + KPI 顶条按行收敛 16 页 + 25 条四类豁免登记·无 workflow 结构改动）+ W887 en 收口 110 页合并四批一次做完 第 49 槽门禁范围扩至全 en 138 页 豁免分册增至 302 条·无 workflow 结构改动）+ W889 GitHub 主页展示位复位与首屏重排、载体改名让位、首屏 30 秒上手、元数据补齐、dev 合 main 对齐 Pages·无 workflow 结构改动）+ W890 CI 阻塞项清偿：两处过期测试断言与上游有意变更同步、ruff 六项清零、Windows 存活探针改非终止式查询、Pillow 升级清 25 个 CVE·无 workflow 结构改动）+ W891 en 收尾清欠账 容器归并 11 页 nav-back 实底转文字态 49 页 间距令牌化 3,353 处值保留·无 workflow 结构改动）+ W892 宣传单页 A4 竖版双面 卖点层级栅格配图联系区块一次规划齐备 HTML 源导出 PDF 与 PNG 三件套·无 workflow 结构改动）+ W893 十二张素材图按四画幅各三张成套交付、四主题各三张以拉丁方排布、锚点沿用 W882 改写版（纯否定式构图句、零规则线）·无 workflow 结构改动）+ W896 门禁实算口径改目标提交树 目录清单与 stats 与文档索引三处同步 新增 ci_sim 预演工具 未落库件不再污染判据·无 workflow 结构改动）+ W897 preflight touches 分隔符根修 兼容五种分隔符 单测 11 例 ci_sim 接进 CI workflow 每次 PR 自动出 CI 侧预演结论·无 workflow 结构改动）+ W898 宣传物料投放接线 README 新增物料小节 站内入口指向仓库 英文版单页与 PDF 分享图指引 规范受管资产登记·无 workflow 结构改动）+ W899 合并后收尾修正：output 目录计数口径订正与朱砂门禁增量缓存重建·无 workflow 结构改动）+ W900 11-方案报告目录分类重组：根层二十余件归入四个分类子目录，唯一索引分区重构，入链与索引派生面全量同步·无 workflow 结构改动）+ W901 对账面随递归恢复，历史段链接改指新址，两件计划档补登索引·无 workflow 结构改动）+ W902 机制层三层审查四发现（touches 假绿待批），记忆固化八项入仓（报告落位常设指令与坑表三条）·无 workflow 结构改动）+ W903 touches 注记归一与对称目录前缀匹配闭假绿，门禁45提示语补暂存顺序·无 workflow 结构改动）+ W904 C5c 裸聚合七十四处清零并转判红，统计器增七个分板块键，豁免机制补命中后置精确形态·无 workflow 结构改动）+ W905 存量红项清理：暗色门禁补色规则与 npm 生产依赖漏洞清偿·无 workflow 结构改动）+ W906 旁文档门禁残留判定三态化：他方登记行纯追加降提示放行，在位编辑照旧判红·无 workflow 结构改动）+ W907 README 专业化改版：结构层级统一、配图补齐、头部与文案修正·无 workflow 结构改动）+ W908 README 专业化改版：结构层级统一、配图补齐、头部与文案修正·无 workflow 结构改动）+ W909 README 专业化改版：结构层级统一、配图补齐、头部与文案修正·无 workflow 结构改动）+ W912 未落地任务全量盘点五档排期，站内交互债首波清偿，渡口页主脚本考古回灌与门禁建置·无 workflow 结构改动）+ W913 波二小项四件清偿：计划头订正，测试需求随工具停用关闭，依赖钉版，站点数字修正并纳入对账·无 workflow 结构改动）+ W914 新增英文版 README：完整对照翻译、双向语言互链、站内链接指向英文站·无 workflow 结构改动）+ W915 判据文档时点数字剥离归产物文件，404 页补 v4 间距令牌等值迁移·无 workflow 结构改动）+ W916 准入门禁静态版建置并接入 CI 预演，双铁律上锁，波二余件排续批·无 workflow 结构改动）+ W917 数据库四项高危正确性修复落地，四不变量静态门禁锁定并接入 CI 预演·无 workflow 结构改动）+ W918 LLM 上游不可达时问答链路降级说明替代裸错误，波二小项全部清偿·无 workflow 结构改动）+ W919 数据库迁移框架建置记账执行，四索引与单SQL会话列表，脏数据降级，D1 真债首项清偿·无 workflow 结构改动）+ W920 副本链值级对账门禁建置，存量漂移基线冻结防增量，新漂移判红·无 workflow 结构改动）+ W921 变更日志百零二段迁一级归档，体积回基线以下，守恒断言全程护航·无 workflow 结构改动）+ W922 十二项裁决落地：四件工程当场做掉，八项方向性结论登记在案，清单全闭环·无 workflow 结构改动）+ W923 复审让号行幻影在途与前缀修复，跳号补登记，十一项实抽全过·无 workflow 结构改动）+ W924 性能三指标分治落地：页体积双层门槛升格判红，首屏归并既有防线，首 token 挂解冻条件·无 workflow 结构改动）+ W925 对 W821 架构方案的增量修订：按新规模（月活十万级）改采 PG 自建单机，新增等保合规横切面，架构图三形态交付·无 workflow 结构改动）+ W926 交互流程四维复核/跳转路径/按钮反馈/表单报错/空状态异常分支/对照前次审查逐条给闭环状态并出当前状态排序建议·无 workflow 结构改动）+ W927 四项开放项裁决落档，PG 部署基线离线施工件交付，交互审查交叉对账补一处设计遗漏·无 workflow 结构改动）+ W928 无 Docker 改走官方免安装二进制实跑 PG 16.4，6 项实跑通过，4 个真缺陷固化为守卫·无 workflow 结构改动）+ W930 W854 十八条四天后现状复核 + 三条新发现 + 六批可施工落地方案·无 workflow 结构改动）+ W932 六张 16:9 宽幅浓墨剪影成套 Hero 素材图、锚点复用 W852→W893 成熟段、底部净空带供标题叠字·无 workflow 结构改动）+ W933 认领即占号/回填独占/收官回填三件套规则 + 撞号检测与行指纹与收官体检与反引号剥离与登记类共享面排除五个机检判据·无 workflow 结构改动）+ W934 把架构方案里的「M12 PG 存储层」变成可运行的代码层：存储层四件 + 门面化 + PG 三表 schema + 迁移器，并把现役 70/134/4 条真实数据迁入 PG 16.4 且三重对账全一致·无 workflow 结构改动）+ W935 渡口档案正文 4 条工程引用改为对读者有意义的正文,溯源移入源码注释 + 英文站索引页目录型死链改纯文本,全仓真死链 1→0·无 workflow 结构改动）+ W939 把全站 UI 图标位（控件图标 / 图标槽 / CSS content 图标 / 运行时按钮文本图标）的 emoji 字符全部换成自绘的东方线描 SVG 图标：自绘 27 枚图标资产 + 建 2 个可复跑机检脚本 + 替换 1,957 处 + CSS 级联 328 页 + CSP 重算 14 页，正文装饰 emoji 与箭头符号零损伤·无 workflow 结构改动）+ W956 登记面治理批（preflight 在途判定加 git 条件与复盘触发器落地）·无 workflow 结构改动）+ W964 版本脚注治理批（滚动器形态盲区修复与条目定形落地）·无 workflow 结构改动）+ W965 脚注重生成与探针沉淀批（扫描探针常驻化与候选议题登记）·无 workflow 结构改动）+ W966 摘要层纠偏与去冗批（过期数字纠偏与超长条目收敛）·无 workflow 结构改动）+ W967 数字断言全面对账批（治理文档人工计数钉到机器事实源）·无 workflow 结构改动）+ W968 台账对账表窗口制拆分批（正本 446.6 至 150.3KB 窗口 60 行硬判据）·无 workflow 结构改动）+ W969 W1000 号位迁移批（三位号正则升三位四位兼容形态）·无 workflow 结构改动）+ W970 台账归档行工具批（号序切分常驻化与首跑回窗）·无 workflow 结构改动）+ W971 存量段状态回填批（102 段缺状态字段按 git 事实源补齐）·无 workflow 结构改动）+ W972 CodeQL 三高危修复批（审计器自身正则与转义加固）·无 workflow 结构改动）+ W973 HANDOVER 五区清理批（历史归档与指针化落地）·无 workflow 结构改动）+ W976 工具链体检修复批：台账修剪器 A5 断言、体积窗修路指引分治、preflight 认领后自撞三处修复，三窗回窗与 tmpe 收官提示位·无 workflow 结构改动）+ W977 一次性件批量退役批：引用分级剔除后 287 件入 archive scripts batches，15 件现役硬保留，目录文档刷新与台账组行登记·无 workflow 结构改动）+ W978 第 44 篇工作复盘批：触发器首次触发，区间二十一段，上篇改进项闭环五项，登记下期改进四项·无 workflow 结构改动）+ W979 收官提示位扩展批：体积窗超窗回窗提示，临时区超龄报数，脚本顶层下划线件计数，三位号活面零残留裁定免迁·无 workflow 结构改动）+ W980 统计标记同步机器化批：对账面标记自动跟随实算源，事实收官订正一笔，计数链待新站点地址重判·无 workflow 结构改动）+ W981 数据链恢复重判批：取数路径修复与判定落盘，账号重启实证，三处登记面订正，中间态维持二选一·无 workflow 结构改动）+ W982 手搓绕过级联治理批：版本面契约判据与开工劝导两项落地，文件锁按登记顾虑缓建·无 workflow 结构改动）+ W983 内页题图成套批第四组：四库混合覆盖 12 张，reader 有题图页 63 增至 75，3 张因人眼关重出（判据盲区实证）·无 workflow 结构改动）+ W984 内页题图成套批第五组：回目页 6 张线描重出加四库扩量 6 张，reader 有题图页 75 增至 81，原浓墨版保留归档·无 workflow 结构改动）+ W985 工具文档三件批：场景速查路由表，计数指针化，机器生成全量工具清单并挂刷新链·无 workflow 结构改动）+ W986 回目页 6 张线描版换主体重出：根因是同角色同范式的第二张图观感必然重复而机器判据查不出，处置为同名 stem 覆盖换角色，浓墨渲染原稿保留不删·无 workflow 结构改动）+ W987 水墨意境卡族启用：归族登记 33 张从未上线的 1:1 水墨插画并立下规范边界，另启用 6 张为回目页场景插图，首屏仍留题图·无 workflow 结构改动）+ W988 水墨卡族投放：27 张 card-* 逐张定落位并接入（13 横幅 + 14 场景图），另给 102 页换上专属 1200×630 og:image·无 workflow 结构改动）+ W989 脚注定形收紧批（C4 收紧至 120 与现网五条索引化）·无 workflow 结构改动）+ W990 内联纪律收口批：报错原文入查坑表，新增工作树吸收条目，计数链四处同步·无 workflow 结构改动）+ W991 级联运行锁与提交隔离批（运行锁常驻化与无 pathspec 拒绝）·无 workflow 结构改动）+ W993 全仓行尾定形批（gitattributes 落地与工作树重写）·无 workflow 结构改动）+ W994 归档系统打磨批：tier-2 判距探针与常驻二级归档工具，双件实跑回线，冷存储警告与台账基线·无 workflow 结构改动）+ W995 tier2 按W段拆分批：范围命名件定形，二级归档工具容量自持，探针升格与提示位扩展·无 workflow 结构改动）+ W996 流程提示位批：收官自检器反向查台账抓漏跑级联，豁免合规零段形态·无 workflow 结构改动）+ W997 协作纪律入库批（W516 载体铁则二犯的并案收口）·无 workflow 结构改动）+ W998 对抗式审查修复批（门禁死门控与锁竞态根治）·无 workflow 结构改动）+ W1000 对抗式审查常驻化批（触发器与模板落盘及四位号实战）·无 workflow 结构改动）+ W1001 回次 og:image 全覆盖批、第一轮试点（12 张线描立像/场面）·无 workflow 结构改动）+ W1002 一次性脚本三档归位：81 件入 archive/scripts/batches、4 件转正去 `_` 前缀、第 42 门禁加 C4 判据（滞留必红 + 转正候选棘轮）·无 workflow 结构改动）+ W1003 agent-web chat 组件集成验证与死重清退：验证三链全绿 + @tdesign-react/aigc 死重清退 + e2e 前端端口迁出 Windows 保留段·无 workflow 结构改动）+ W1005 hero 水墨图人数修正（4 人形 + 1 匹白马）两张原地替换，flyer A4 快照重渲染·无 workflow 结构改动）+ W1006 safe_commit 新增 --expect-spec（提交前索引态与 spec 求差，spec 外文件即拒）+ 自测 4→8 + 单测 7 例（含临时仓端到端）·无 workflow 结构改动）+ W1007 新增 check_commit_scope.py 并挂第 51 槽恒跑：归属批次按索引 CHANGELOG 顶段判定，索引态路径集超出该批 spec 即 FAIL·无 workflow 结构改动）+ W1008 回窗恢复开工态（CHANGELOG/file-index 各迁 3 段、台账迁 2 行）+ 触发器判据读取面改为正本 ∪ 归档（I2 假警根因）·无 workflow 结构改动）+ W1009 级联收尾自动刷 stats（失败即返回 2 不静默）+ spec 解析收敛到 batch_spec 单一入口（两处只调用）·无 workflow 结构改动）+ W1010 级联收尾链改为 落盘→回窗→stats（窗口常量 110 段/60 行，失败返回 2）并补单测 2 例·无 workflow 结构改动）+ W1011 五项归位（根临时脚本、空壳三目录、入口文档）+ 第 52 槽布局门禁（根文件白名单、顶层目录角色、白名单陈腐）+ 连带修 12 页断链·无 workflow 结构改动）+ W1012 scripts/output 里 33MB 一次性基线迁 archive（w8xx）+ 并行会话收尾件代收（pytest 计数与两份架构方案）·无 workflow 结构改动）+ W1013 回次 og:image 全覆盖第二轮：12 张线描立像与场面接入 12 个回目页并换专属 og:image·无 workflow 结构改动）+ W1014 工具脚本探针门禁全量体检后修 15 项真缺陷（含 4 处门禁本体）加临时系统路由根修加归档台账回写·无 workflow 结构改动）+ W1016 体检期实踩而坑表未覆盖的教训补入坑表加可机检者升硬守卫加补缺失自测加订正记账陈腐值·无 workflow 结构改动）+ W1017 产物目录回归活产物单一职责，历史批次一次性件按批号归档，临时区授权清理并保留个人稿·无 workflow 结构改动）+ W1018 回次 og:image 全覆盖第三轮：十二张线描立像与场面接入对应回目页并换专属 og:image·无 workflow 结构改动）+ W1019 CSS 单一事实源治本收敛漂移并以内联净重口径压住每页体积，补 Python 侧参数钳制负向测试·无 workflow 结构改动）+ W1020 Backlog 登记面对账：逐条核 git 与测试实况，关闭已解决却仍挂待办的条目并订正其余条目现状·无 workflow 结构改动）+ W1021 Backlog 对账触发器常驻化：新增第四哨按批数阈值点名，接线 preflight 并补齐自测与台账事件 token·无 workflow 结构改动）+ W1022 对抗审查批：按 A–G 全项核三批声明，修复 P1 与 P2 发现并把判据缺口补成回归锁·无 workflow 结构改动）+ W1023 提示词库派发骨架补齐：把审查任务书、工作复盘、导师提问三份方法论落成可直接粘贴的执行骨架·无 workflow 结构改动）+ W1024 教训固化对账：把本次任务踩过的十九类问题逐条核是否已机器化或入坑表，补齐四类缺口并订正计数·无 workflow 结构改动）+ W1025 坑表计数升机器判据：五处交叉对账取代人核，并在交接文档顶部写明新 Agent 的必读入口·无 workflow 结构改动）+ W1026 交接文档已完成叙述迁入归档容器并补回活策略约束，同时诊断出方案报告与全仓文字缺乏归档与清理机制·无 workflow 结构改动）+ W1027 治理文档文字审查：按诊断与减法清理口径扫六件导读文档，实测无 AI 腔与废话，超长句均为清单与规则·无 workflow 结构改动）+ W1028 诊断归档与临时两套系统：制度工具齐备但缺定期执行，已归桶散件并补执行触发点，回收站清空待确认·无 workflow 结构改动）+ W1029 方案报告归档判断：逐类核对报告与执行前计划的配对关系，按成本核算裁决不迁并在目录内留下理由·无 workflow 结构改动）+ W1030 抽查方案报告并厘清归档覆盖边界：归档只解单文件纵向增长，独立文件堆积该配生命周期状态而非归档器·无 workflow 结构改动）+ W1031 取经编制表数据重核：核实三处编制位载体现状，为文档加入数据时效与修订触发，并辨析空缺含义·无 workflow 结构改动）+ W1032 编制表环境依赖纠错：实测现环境连接器与技能清单，撤回旧环境 CLI 依赖并补环境差异声明与坑位·无 workflow 结构改动）+ W1033 校正执行前计划的状态与时效标注：仓内已收官仓外三项未执行，失效步骤加声明而正文保持原样·无 workflow 结构改动）+ W1034 补全授业官位：把十五类最高频判据固化为项目级速查 skill，并解决忽略规则与自动加载路径差异·无 workflow 结构改动）+ W1035 按编制表人物位补齐三处有职责无载体的位次，把常驻角色降级为可派发的只读职责书·无 workflow 结构改动）+ W1036 按编制表人物位给避坑技能定名菩提授业，补出处与约束说明并结清第三处位空·无 workflow 结构改动）+ W1037 为交付门禁加入段级耗时剖析，实测发现瓶颈集中在两段而非全线，据此推翻原定的缓存与并行方案·无 workflow 结构改动）+ W1038 优化无障碍审计性能：清除四千八百万次冗余小写化调用，实测语义等价但收益仅百分之五点七·无 workflow 结构改动）+ W1039 把仅存于用户级记忆的禁令与协作约束写进项目铁律：禁止补丁加补丁，以及五条协作与环境约束·无 workflow 结构改动）+ W1040 任务分级协议入库：计划执行沉淀三级制，战役任务微三级分流，模糊词强制替换·无 workflow 结构改动）+ W1041 为并行会话提供批次号预约机制：开批先跑 reserve_w.py 占号，写入共享预约表，避免事后登记导致的撞号·无 workflow 结构改动）+ W1042 工具面根因修复与判据补覆盖：台账回填显式参数生效、编排提示归位、门禁新增件真实文件覆盖、可疑改写面逐处复核·无 workflow 结构改动）+ W1043 回次 og:image 全覆盖第四轮：十二张线描立像与场面接入缺口回目页并换专属 og:image·无 workflow 结构改动）+ W1045 改写面候选逐处复核与存量陈旧清理：两路逐处判定、基线键升四输入、槽数统一五十二、og 切头只修真缺陷·无 workflow 结构改动）+ W1047 图表判据剥标签根修：标签按语法约束且注释优先剥离，修复五页误吞正文且零漏剥标签·无 workflow 结构改动）+ W1048 P2 治理收编孤儿批：gates.md 计数订正与 CLAUDE 速查补行，判据件收编与方案件入库·无 workflow 结构改动）+ W1050 回次 og:image 全覆盖第五轮：十二张线描立像与场面接入缺口回目页并换专属 og:image·无 workflow 结构改动）+ W1050 门禁判据加固：sweep 覆盖面纳入 gates.md 与第 3 槽计数 fallback 对拍·无 workflow 结构改动）+ W1051 复盘触发器口径根修：上篇复盘识别升级为三信号 + 目录面双源，历史段标题自洽·无 workflow 结构改动）+ W1052 补丁治理实施第一批：铁律双写根治加同段重复判据与占号支撑检测·无 workflow 结构改动）+ W1053 方案实施收尾：判据加固与制度条款度量影子全量落地·无 workflow 结构改动）+ W1054 清偿第一轮：探针时序修复与数据命名扩展及影子分层·无 workflow 结构改动）+ W1055 清偿第二轮：静态字面量提取与缺口清零及收紧升格·无 workflow 结构改动）+ W1056 提交前三问自检流程契约入库与坑表计数链同步·无 workflow 结构改动）+ W1057 对账批：待办登记面逐条 git 实况核验与压缩归档·无 workflow 结构改动）+ W1058 计数链漂移订正与对账面扩容·无 workflow 结构改动）+ W1059 复盘报告入库批十六批全景与协作主题沉淀·无 workflow 结构改动）+ W1060 CI 提效批：审计矩阵收敛与并发取消补齐·无 workflow 结构改动）+ W1061 私有记忆同步批：工具禁令入必载层与环境坑入坑表·无 workflow 结构改动）。

## 1. 工作流列表

| 工作流 | 文件 | 触发条件 | 用途 |
| --- | --- | --- | --- |
| CI | [`ci.yml`](ci.yml) | `push` main + `pull_request` + `workflow_dispatch` | 10 job 门禁：截图存活烟测 / Lighthouse / a11y / dependency / ruff / pytest / E2E 交互断言 / agent-web 构建 / 交付校验 / desktop 构建 |
| Security | [`security.yml`](security.yml) | `push` main + `pull_request` | 4 job：npm-audit（scripts/ + agent-web/ 双目录）/ pip-audit / CSP / XSS detect |
| Deploy Pages | [`pages.yml`](pages.yml) | `push` main（site/** 变更） | GitHub Pages 部署 `./site`（W401 决策：不采用 build-test-deploy.yml，避免部署竞态·已删除） |
| Lighthouse CI | [`perf.yml`](perf.yml) | `push` main（site/**）+ `pull_request` + 每周一 + `workflow_dispatch`（W422 补 push：原仅 PR 从不运行·首跑暴露性能债后阈值已校准） | LHCI 性能预算断言（LCP≤5000ms/CLS≤0.3/TBT≤300ms，W424 实测校准） |
| Screenshot Review | [`screenshot-review.yml`](screenshot-review.yml) | `push` main（site/** 或脚本/workflow 变更）+ `pull_request` + 每周一 + `workflow_dispatch`（W421：页脚/文档-only 跳过·data 页定向截图） | Playwright 截图 + 布局审计 |
| Dependency Review | [`dependency-review.yml`](dependency-review.yml) | `pull_request`（main·dependabot PR 即真实流量） | 依赖变更审查：漏洞/许可证（W683·fail-on-severity=moderate） |
| Mark Stale | [`stale.yml`](stale.yml) | 每日 01:30 UTC + `workflow_dispatch`（W683） | 陈旧 issue/PR 标记（60 天）与自动关闭（再 14 天·pinned 豁免） |
| OpenSSF Scorecard | [`scorecard.yml`](scorecard.yml) | 每周一 03:00 UTC + `branch_protection_rule` 变更 + `workflow_dispatch`（W683） | OpenSSF 安全评分（SARIF 入 Code scanning + publish_results 徽章） |
| Release Desktop | [`release.yml`](release.yml) | `push` tag `v*` + `workflow_dispatch` | 三平台桌面安装包构建（Win NSIS / macOS universal dmg+zip / Linux AppImage）并发布 GitHub Release + latest*.yml 自动更新元数据 |
| Workflow Lint | [`workflow-lint.yml`](workflow-lint.yml) | `push` + `pull_request` + `workflow_dispatch`（**不限定分支**） | 工作流 YAML 可解析性守卫（W833·**独立于 ci.yml**）：W806 同型事故（裸标量值含冒号加空格 → YAML 映射歧义 → 工作流整体不可解析 → run 0 秒失败且 PR 不生成 check）的根修——当时唯一守卫住在 ci.yml 内·与被守卫同生共死·缺陷遂复发；本工作流独立存在，ci.yml 坏掉时仍能照亮问题并指到文件与行 |

> **W400 关键教训**：ci.yml 建置时仅 `pull_request` 触发，但项目工作流是直接 push main（无 PR），**CI 从未真正运行过**。W399 补 push 触发后首次运行暴露全部存量问题。**新 workflow 必须本地语法校验 + 确认触发条件匹配真实开发流。**

## 2. ci.yml 十 job 说明

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

### Job 10 · `desktop-build`（桌面版构建回归，W804 新增）

- **运行环境**：`ubuntu-latest` + Node 22
- **流程**：`npm --prefix xiyouji-desktop ci` → `npm run prepare:content` → `npm test`（node --test）→ `npm run pack:dir`（electron-builder `--dir` 只解包不产安装包，验证 asar/extraResources/publish 配置可构建）
- **发布分工**：本 job 只做构建回归（push/PR main 触发）；三平台安装包与 GitHub Release 由 [`release.yml`](release.yml)（tag `v*` / `workflow_dispatch`）负责
- **与 agent-web-build 的差异**：桌面版不产 artifact（electron 完整包体积大，发布产物由 release job 三平台产出），仅断言打包配置可构建

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

## 10. 桌面版发布（W804）

桌面版（`xiyouji-desktop/`，Electron 壳 + 内置站点内容）的发布由 [`release.yml`](release.yml) 承担，与站点/文档的批次发布（`main` 推送 → `pages.yml`）解耦。

### 发布步骤

1. 改 `xiyouji-desktop/package.json` 的 `version`（如 `2.3.0`）并合并到默认分支 `main`（当前仓库工作分支为 `dev`，`main` 受保护走 PR）；
2. 打 tag 并推送：`git tag v2.3.0 && git push origin v2.3.0`；
3. workflow 自动执行 preflight（tag 与 package.json 版本一致性校验 + 从 CHANGELOG 首段提取内容批次 W###）→ 三平台并行构建（electron-builder `--publish never`）→ 汇总产物发布 GitHub Release；
4. 校验 Release 资产：Win `xiyouji-desktop-win-x64.exe` + `latest.yml` / macOS `xiyouji-desktop-mac-universal.dmg` + `.zip` + `latest-mac.yml` / Linux `xiyouji-desktop-linux-x86_64.AppImage` + `latest-linux.yml`（`*.blockmap` 供增量更新）。

### 自动更新机制

- `electron-updater` 读取 Release 资产内的 `latest*.yml` 与 `*.blockmap` 做增量更新；**这些文件缺失 = 自动更新静默失效**，故 release job 幂等上传全部资产。
- Windows：NSIS 安装版支持自动更新；macOS 自动更新受未签名限制（首次需手动放行，详见 `xiyouji-desktop/README.md`）；Linux：AppImage `chmod +x` 后可更新。
- 未签名构建：CI 设 `CSC_IDENTITY_AUTO_DISCOVERY=false`，不签名不公证（仓库无证书）；首次打开提示与绕过步骤见桌面版 README。

### workflow_dispatch 补发

- 漏发/需重跑时：Actions → `Release Desktop` → Run workflow，填 `version`（如 `2.3.0`，须与 `package.json` 一致），可选勾选 `prerelease`；
- 若 tag 尚未创建，`gh release create` 会基于默认分支自动建 tag；若 Release 已存在则幂等覆盖资产（`--clobber`）并刷新标题/notes。
