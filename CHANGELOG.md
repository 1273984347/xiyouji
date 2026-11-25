### W1327（2026-11-25）：页脚同类关联链接补全

> **来源**：
> - **T1**：用户旅程 V3 第 3 项——页脚关联链接补全与智能推荐：把读完一页后的死路改成同类三页可继续。
> - **推荐口径**：唯一来源为 site/dashboard.html 专题卡片（href + data-category，50 张站内卡），同类别按看板顺序循环取后 3 页、自页排除；类别成员不足 4 时取 n-1 条（Q+ 2 页互链 1 条）。
> - **注入形态**：目标页 `<footer class="site-footer">` 内追加一组 `<nav class="footer-related">`（复用既有 .site-footer nav 与 .footer-meta 样式），零新增 CSS、零新增内联脚本、零外域，file:// 直开不变。
> - **覆盖**：看板 50 张站内卡 = 45 页注入 + 5 个数据中枢工具页（整页无 site-footer，显式 NO_FOOTER 集并由 check 反向锁死：仍有 footer 或出现 MARK 即红）；其余 site/data 内容页不在看板卡上，无类别事实源，不纳入本批口径。
> - **源数据勘正**：看板专题区静态文案「51 个专题页 / 全部 51」与实际 41 张网格卡不符（全页站内卡 50 = 41 专题网格 + 4 KPI 概览 + 5 数据中枢；运行时 updateCounts 只自愈标签页数字，静态文案与无 JS 场景不自愈），本批同步订正为 41。
> - **W1325 遗留根修**：3 篇归档正本 41 条相对链接按迁移后深度重写（lint_links 默认排除 archive/，故 W1325 的 0 broken 结论不覆盖该面）；`docs/10-方法论沉淀/README.md` 三 skill 行补「已归档·指针」标。
> - **对抗式审查（W1327 已派发）**：审查发现并本批根修 4 项——① 初版写盘未带 newline 致 45 页转 CRLF（已归一，check 增行尾 LF 判据）；② 新脚本四面无引用（补单测 7 例）；③ 看板静态「51」失实（实测网格 41 卡）；④ W1325 归档内链 41 条失效（已按新深度重写）。事实澄清：Q+ 仅 2 页互链 1 条、Q++ 3 页互链 2 条，故 45 页并非每页 3 条（合计 128 条）。
> - **验证（全绿）**：w1327_related_links.py --check PASS（覆盖 50·死链 0·自页 0·分类不一致 0·杂散 0）；二次 --apply 实际改动 0（幂等）；单测 7 例；归档内链 41/41 可达；lint_links 24807 链接 0 broken；check_structure 873 文件通过。
> - **状态**：已落地（级联+提交后以 gh run list 为准）。
> - **文件**：见 file-index W1327 段。

### W1326（2026-11-25）：两轮推送 CI 等待纪律（E-321 入坑表 + 流水线第 6 步/§五）

> **来源**：用户 2026-11-25 指令「把这条教训写进 pitfalls/流水线」——W1324+W1325 两轮推送实操暴露「首轮 CI 被并发取消 + 回填笔 CI 红无法 rerun 转绿」。
>
> - **坑表**：git 主题新增 E-321（根因/判据/纪律）+ 归档全文；pitfalls 总 426→427、git 40→41，标记面 23 处跟随。
>
> - **流水线**：§二 第 6 步新增「两轮推送的 CI 等待纪律」；§五 失败模式速查新增一行。
>
> - **验证**：verify_delivery 全量；`test_cascade_handover_rotate` 3/3；E-321 计数由 stats.py 实算。
>
> - **文件**：见 file-index W1326 段。
>
> - **状态**：教训入库（无代码/页面改动；无新增豁免）。
### W1325（2026-11-25）：方法论审查 P0-P3 全量处置（5 件物理归档/合并 + 全目录指针与计数对齐）

> **来源**：用户 2026-11-25 指令「先把 P0 P1 P2 P3 的问题处理完」——承接 W1324 方法论审查报告的 106 条发现（P0 2 / P1 32 / P2 45 / P3 27）。
>
> - **结构件（物理归档/合并）**：`三skill闭环` / `记忆研究理论框架应用方法论` / `双索引可追溯改造` / `agent-web技术栈迁移评估` 4 篇迁 `archive/docs/复盘报告/`，原路径保留指针；`dispatching-parallel-agents四subagent并行模式` 并入 `多Agent干扰治理与touches纪律` §四之三；`docs/INDEX.md`、`docs/10-方法论沉淀/README.md`、站内搜索索引、RAG 索引同步。
>
> - **P0 根修**：① 三skill 退役后仍给执行指令 → 物理归档 + 顶部/§五/§七/§九 封条「历史记录·勿执行」；② 前端SOP「样式生效已覆盖」失实 → 改为「仅渲染基线间接覆盖，无专门判据」，删除 archived 脚本现役路径与 AGENTS §5.2 悬空锚点。
>
> - **P1 指针/路径/计数**：11 篇 AGENTS 章节锚统一改指「§一 铁律 2/14 + §三 常用命令」；`reserve_w.py` 入流水线第 1 步、`release_prep --check-spec` 命令订正、preflight「三轨」→ 现役 1–7 项核验；`text-search.html` → `dataset/text-search.json`；43槽/48段、87页/522行、450行、W700+、门禁 N4、第 45/48 槽全部改指针或实测值；`user_profile.md`/本机路径改仓内镜像说明。
>
> - **P2/P3**：头五要素补齐 / 重复段指针化 / 模糊措辞与行号清理 / 白屏计数与脚本状态对齐 / 素材案例边界标注 / 幂等验证命令 / README 编号说明 / DRL RunCommand 与行号引用订正。
>
> - **验证**：`verify_delivery.py` 全量核心全绿（5 项辅助 WARN 不阻断）；`lint_links` 0 broken；`generate_csp.py --check` 0 漂移；`docs_index.py` / `_gen_search_index.py` / `gen_folder_docs.py --refresh` 已重建；`stats.py --w W1325` 刷新 report_docs 255→256；RAG BM25 本地缓存重建（`rag_index.json` 为 gitignored 缓存）。
>
> - **不做**：不新增豁免/白名单/基线；不修改 `docs/11-方案报告/` 审查报告正文（W1324 保持审查时点快照）。
>
> - **文件**：见 file-index W1325 段。
>
> - **状态**：P0/P1/P2/P3 按报告主题全部处置；结构件按用户裁决物理归档。
### W1324（2026-11-25）：方法论沉淀文档审查（28 篇只读评审 + 报告落位）

> **来源**：用户 2026-11-25 指令「按这个方案生成报告」——对 `docs/10-方法论沉淀/` 全量方法论文档做一次结构与论证质量评审（HOTL document-review 通用 rubric + `docs/12-提示词库/05-项目审查任务书.md` 取证要求）。
>
> - **执行（只读审计·零被审文档改动）**：28 个 md（含 README，4,272 行 / 296,637 B）分四组评审；主会话复核 P0 2/2、P1 20/32（其余标 B），并纠正子代理 1 处证据误判（`ci.yml` 实含 `check_js_syntax.py --all`）。
>
> - **结论**：保留 7 / 需修订 16 / 建议合并 1 / 建议归档 4；P0 2（三skill 退役后仍给执行指令；前端SOP「样式生效」覆盖声明失实）· P1 32 · P2 45 · P3 27；系统性问题=W1279 地图化后 11/28 篇 AGENTS 章节锚悬空 + 退役工具按现役描述 + 计数裸写（43槽/48段、87页/522行、450行、W700+ 等）。
>
> - **落位**：报告入 [方法论审查报告-2026-11-25.md](docs/11-方案报告/审查与评审/方法论审查报告-2026-11-25.md)；[docs/11-方案报告/README.md](docs/11-方案报告/README.md) §一登记（23→24 篇·全局序号 152）。
>
> - **不做**：不改 `docs/10-方法论沉淀/` 任何文件；指针回扫/归档/计数实体化另批施工（报告 §七给建议批次主题，实际以对账表认领为准）。
>
> - **文件**：见 file-index W1324 段。
>
> - **状态**：审查报告 V1.0（只读·零被审文档改动）；修复建议待分批立项。
### W1323（2026-11-25）：八十一难难度热力图深化（V2 余项·五阶段难度地形）

> **来源**：HANDOVER「二、下一步方向」V2 可视化深化余项——八十一难难度热力图深化（W1320 对账核验后唯一未完成项）；用户 2026-11-25 指令「开 W1323」执行。
>
> - **取证（先看现状）**：页面已有 ① 四维矩阵 ② 四维分布 ③ 交叉洞察 ④ 联动清单，但 `stage`（前传/初段/中段/后段/终段）字段**从未进入任何分析或视图**——章节排序只用了 `chNum`，五阶段聚合是空白面。
>
> - **执行（新增板块）**：① 页内新增「五阶段难度地形」区块——五张阶段卡（阶段名 / 均分 / 难度条 / 难数·极难数·求助均次）+ 一张聚合表（阶段 / 回目范围 / 难数 / 均分 / 极难 / 平均求助 / 最高分难）+ 一段**运行时生成**的演进洞察；② 中英双页同步（EN 页无清单板块，新板块编号 ④；中文页清单顺延为 ⑤）；③ 所有数值由 `EMBEDDED_DATA`（含 `window.__hmData` 覆写面）实时计算，**不写死任何数字**——避免静态文案随数据漂移；④ 难度条用 `--ink-soft` 填充、峰值卡仅 1px accent 边框，不触碰第 49 槽朱砂实底判据；无新增动画，动效契约不动。
>
> - **门禁报错与根修（第 76 槽棘轮）**：首版新增十个 `.stage-*` 类名 ⇒ 公共层覆盖率 11.7% < 下限 11.8% 判红（口径＝公共层类 / 全站使用类）。修法不抬阈值：卡片复用 `.stat-card`、内部改用 header/strong/small 元素与 `data-*` 属性选择器，**零新增类名** ⇒ 棘轮保持原值。
>
> - **实测结果（file:// 直开）**：中英双页各渲染 5 卡 / 5 行，峰值卡唯一；洞察输出「后段均分 6.9，为五段最高；终段降至 3.8」；除字体 file:// CORS（既有环境行为）外零 console error；热力图 324 格照常渲染。
>
> - **验证**：check_chart_data 239 页 FAIL 0；check_chart_degrade 237 页违例 0；check_chart_content_completeness 基线外新增 0；a11y_audit 全站 P0=0 / P1=0（第 14 槽全规则锁维持）；generate_csp 已重算并 --check 零漂移；第 76 槽公共层覆盖率维持基线（零新增类名）。
>
> - **不做**：不新增图表类型（避免图表词表与图例判据的口径扩张）；不触碰四维矩阵与既有洞察文案；不做内容扩容（冻结裁决不受影响）。
>
> - **文件**：见 file-index W1323 段。
>
> - **状态**：V2 余项收口（判据零放宽·无新增豁免）。
### W1322（2026-11-25）：a11y P1 清零与全规则 P1 锁（隐式 label 假阳性根修 + 焦点可见 + 面板语义）

> **来源**：用户 2026-11-25 指令「三个都做」经实况取证后的可执行项（可访问性门禁核验批）。另两项（记录对账 / Web Agent 评估）经实读证据确认已由既有机制覆盖，本批不重复立项——证据与结论见 HANDOVER 注记。
>
> - **取证（先证后改）**：a11y_audit.py 全站 875 页实测 P0=0、P1=12，四类：E2-23 四条 / E2-4 六条 / E2-1 一条 / E2-12 一条；而第 14 槽只解析 summary.E2-2（对比度）⇒ 其余 39 条规则的 P1 **没有任何阻断位**，12 条长期只出现在报告里。
>
> - **根修①（检测器假阳性）**：E2-23 只认 `label[for]` / aria-label / aria-labelledby / title，未认 WCAG 3.3.2 认可的**隐式包裹**（控件位于 `<label>` 内）⇒ 81-hardships 与 relationships 中英四页共四条 P1 全属误判（页面本就合规）。新增 `_implicit_label_lines()`：按 label 块取**首个**可标注后代（符合「一个 label 只标注一个控件」）⇒ 假阳性清零且不放过真缺 label 的控件。单测五例（正例三 + 负例二）。
>
> - **修②（真实焦点可见）**：天庭 / 妖怪 / 阴司三个关系网络页（中英共六页）`.node-circle:focus { outline:none }` 无替代 ⇒ 拆 hover 与 focus-visible 两态，focus-visible 补 2px 实心 outline + offset。节点本有 tabindex=0 与 keydown ⇒ 键盘用户真实受益，不是为过检而写死样式。
>
> - **修③（面板语义）**：81 难难度热力图的 `#hardship-detail` 是页内非模态详情块（有独立关闭按钮 + ESC 关闭 + 无遮罩），却标 `role=dialog` ⇒ 改为 `role=region` + `aria-live=polite`（内容更新可被读屏播报），同批消 E2-1 与 E2-12 两条 P1。
>
> - **机器判据（语义强化·W1322 锁）**：第 14 槽新增「全 40 条规则 P1 合计=0」断言（原 E2-2 P0+P1 判据保留）⇒ P1 回归即红；P2/P3 仍不阻断，判据不放宽、无新增豁免。
>
> - **验证**：a11y_audit 全站 875 页 P0=0 / P1=0；test_a11y_audit.py 58 passed（新增五例）；收官链全量与推送判据见 pre_push_gate。
>
> - **不做**：P2/P3 存量（5768 / 6854）不清零——不属 P1 阻断面，避免巨批；检测器其余判据不动。
>
> - **文件**：见 file-index W1322 段。
>
> - **状态**：a11y P1 清零并上锁（判据加严·无豁免/无放宽）。
### W1321（2026-11-25）：巨批分笔与多推送固化（选项①）+ safe_commit 索引态分歧机器判据

> **来源**：W1320 Backlog 对账批登记的常设项「批级多笔推送」；用户 2026-11-25 指令「按推荐处置固化该常设项」= 采纳选项①（接受现状并固化进批次流程），并同批根治 W1320 暴露的「索引态捕获旧页」风险。
>
> - **固化①（流程面）**：`docs/10-方法论沉淀/批次交付流水线.md` §二 第 6 步新增三条硬规则——(a) 巨批分笔：容量 #7 越线时按目录分组拆笔、每笔 ≤500、**每笔必须自洽**（页面与探针/渲染档案不得跨笔拆开，第 80/82 槽按页 sha fail-closed）；(b) 逐笔推送 + 临时 worktree：一次推送只带 1 笔，首笔在主线不干净时 `git worktree add` 后在临时树推；(c) 索引态提交前须无「暂存后改写」分歧。§五 失败模式速查新增两条（#7 越线处置、探针陈旧的分笔根因）。
>
> - **固化②（登记面订正）**：第 7 步原断言「同批第二笔回填会被物理拦下 ⇒ 同批回填物理不可行」与 W1318/W1319/W1320 连续三次实证相反 ⇒ 订正为「回填笔在首笔推送后即 1 笔领先、闸门放行；物理不可行仅指同一次 push 带两笔」。
>
> - **机器判据（根治）**：`safe_commit` 新增 `_index_worktree_divergence()`——索引态提交（`--expect-spec` 无 pathspec）前扫 `git status`，X∈{M,A,R,C} 且 Y∈{M,D} 即拒绝并列出分歧件；W1320 实证：dukou 版本页脚在 `git add` 之后被重写，首笔捕获旧页 ⇒ 该笔单独检出时第 80/82 槽判红、只能本地重建。单测新增 2 例（拒绝 + 重新 add 后放行·含 blob 内容断言），全套 9 passed。
>
> - **不做**：选项②（单笔内分块 + 探针免刷新压回 1 笔）不再立项——收益是 CI 轮数，成本是验收面等价性证明，判为不划算。
>
> - **验证**：test_safe_commit_expect_spec.py 9 passed；verify_delivery / pytest 全量见收官链；本批无站点页面内容改动（版本面页脚除外），探针刷新随收官链。
>
> - **文件**：见 file-index W1321 段。
>
> - **状态**：常设项结清（转已处置 [x]）；判据加严（新增拒绝路径·无豁免/无放宽）。
### W1320（2026-11-25）：Backlog 对账批（W1021 触发器 35 批点名·遗留 7 条实况核验 + 候选陈旧清理）

> **来源**：`check_backlog_review.py` 机械点名——距上次对账（W1284）已 **35 批 ≥ 阈值 25**；W1320 开工 preflight 同报。用户 2026-11-25 指令「好的，执行吧」= 批准开对账批（判据=git 与测试实况，非条目自述）。
>
> - **取证与判定**：对 HANDOVER「四、待办」的 W1288/W1289 两块遗留逐条拿 git / 门禁 / 现势实跑核——① 复盘触发器：W1311（T140 复盘批）已清偿，现势 1 天 / 8 批 / 15 提交未触发；② 计数链 N1-N5：W1319 preflight 实读全一致（板块篇数 {1:100,2:215,3:209,4:42,5:19,6:44} / verify 88 段 / 83 槽 / 426 坑 / 启动 Prompt 三计数）；③ 坑表写窗：W1290 六主题拆分结构性解除（C7 逐文件 ≤262144 B·现最大 flow-collab.md 126,068 B）；④ `assets/game/`：W1303 纳入版本管理（`.git/info/exclude` 内有解除注记）；⑤ 探针刷新前置：`batch_closeout` 的 refresh 步已在 gate 之前（W1319 收官链实证）。⇒ 6 条结清。
>
> - **唯一未结转常设项**：W1287「下一批压到 1 笔」——W1318 实推 3 笔、W1319 实推 4 笔；根因＝容量 #7「单笔 <500 文件」× 637 页共享 CSS 重同步必然分笔，push-gate 的「每次推送 ≤1 笔」已物理兜底 ⇒ 批级多笔为已知代价，登记为 [ ] 常设项并给两条处置候选（接受并固化 / 立项研究分块提交）。
>
> - **§二 候选陈旧清理**：V2 地理 3D（journey-geo-3d.html）与人物关系动态网络（character-relationship-3d.html）、V3 标签云（tag-cloud.html）、手搓绕过级联治理批（W982 落地 + W989 收尾）均已落地 ⇒ 从候选移除；E9 治理经验移植保留（外部仓动作·需用户授权）。
>
> - **他方面**：W1240/W1241 两条他方会话行已随台账行窗归档，正本无滞留告警。
>
> - **触发器归零**：台账本批行状态列写入事件 token「Backlog 对账已执行」⇒ 下次数点从 W1320 起算。
>
> - **验证**：check_backlog_review 点名前 35 批 → 本批后归零；verify_delivery / pytest 见收官链；本批零代码/零样式改动（纯文档与登记面）。
>
> - **文件**：见 file-index W1320 段。
>
> - **状态**：对账完成（6 结 1 常设）；判据/阈值零变更；单笔提交（文件数远小于 #7 上限）。
### W1319（2026-11-25）：CSS 源瘦身（零消费规则与死声明清零·共享基线块余量 48→3,277 B）+ DESIGN Hero 规格更正

> **来源**：W1318 收官登记「#2b 余量仅 48 B ⇒ 下一批须二选一：CSS 源瘦身（推荐）或由用户裁决机制线校准」；用户 2026-11-25 指令「好的，执行吧」= 批准做 CSS 源瘦身（不动机制线·不新增豁免·不调阈值）。
>
> - **取证（零消费判定）**：对 875 个 site HTML（剔除共享 `<style>` 块后只看标记面）+ 26 个 site JS + scripts/ 生成器全扫，按「选择器内任一 class/id 记号词边界零命中且无同义选择器可匹配」判零消费。命中 16 条规则（1,576 B 源）：`.text-mono` / `.text-xs` / `.text-faint` / `.text-accent`、`.badge-{accent,blue,gold,green}`、`.link-ink`(含 :hover)、`.btn-primary`(含 :hover)、`.series-shape`、`text.heat-value`、`svg .label-strong`、`text.value-label`(含 `.is-strong`)；另检出跨文件完全重复块（tokens.css 与 system.css 各一份 W1261 暗色序列映射 8 条）、同选择器后段覆盖的死声明（`.hero` 双层、`.chart-tooltip` 首块、`svg text` font-family）、同一选择器表内重复项 2 处。
>
> - **修法（只删已证无消费者的字节·判据零放宽）**：① 16 条零消费规则删除；② hero 双层合单——tokens 覆写层（`.hero` / `.hero::after`）与 system 基础层删除，定义收敛到 system.css W1261 节单处（position/overflow 并入，逐属性与旧级联终值等值）；③ `.chart-tooltip` 首块 6 条被后块 100% 覆盖的死声明删除（布局/动效位保留）；④ `svg text` 的 font-family 死声明、tick-text 选择器表重复项、system 侧 W1261 暗色映射重复块删除；⑤ `.value-label` 死选择器与 `.is-strong` 死规则删除（`.data-label` 有效选择器保留）。机制线、阈值、白名单、压缩算法均未改。
>
> - **结果**：共享基线块 57,296 → **54,067 B**（52.80 KiB·机制线 57,344 B·余量 48 B → **3,277 B**）；637 页重同步；check_inlined_css 内联 634 页 min 54,041 B（≥20,000）；check_structure 873 文件 / 1966 style 块括号平衡通过；抽样渲染（dukou-engine / reader ch001 / dashboard / en-dashboard）零 console error，`.hero` / `.chart-tooltip` / `svg text` 计算样式与旧级联同值。
>
> - **文档同步**：DESIGN.md §3.3 Hero 规格由「135deg 三色渐变 + 径向光晕」更正为现役「玄墨纯色 + 水墨山形图·无光晕」（旧文与 W334/W1261 已落地事实相反，且其描述的空 `::after` 规则本批删除）；§4A.8 现役实测重算（内联 637 页 / 三口径字节 / 共享块 54,067 B·余量 3,277 B）。
>
> - **零消费证据边界**：`.btn-primary` / `.badge-*` 仅出现在 v2/v3 方案报告与样板 BRIEF（历史规格），现役 875 页标记面 0 消费；如后续迁移需要按 DESIGN 重新新增，不以保留死规则代替。
>
> - **验证**：pytest 全量见收官链；verify_delivery 全量见收官链；容量 #2b 0 越线（#7 仅未提交暂态，两笔提交后清零）。
>
> - **文件**：见 file-index W1319 段（site/reader 634 件按目录分组登记）。
>
> - **状态**：容量 #2b 余量 48 B → 3,277 B；判据/机制线/白名单零变更；两笔提交（457 + 210 件）绕 #7 <500。
### W1318（2026-11-25）：容量 #2b 治本（共享 CSS 无损压缩 + 全站重同步）+ 测试隔离缺陷根修

> **来源**：用户 2026-11-25 指令「继续容量软线治理」并裁决「两个都做」——对象①容量 #2b 共享基线块机制线（67.29 KB > 56 KB 越线）；对象②W1315 连带发现/W1317 实证的 batch_closeout 测试隔离缺陷（pytest 会真实回填本仓台账）。
>
> - **取证①（#2b 根因）**：共享基线块 = tokens.css + system.css 剥注释副本（68,902 B/67.29 KiB）；W1224 设线时约 55 KB，此后设计系统增长 12 KB 未同步瘦身。全站 637 个内联页（634 reader + dukou-engine + _template + _shell）同块复制。
>
> - **修法①（无损压缩 + 全站重同步）**：`inline_css.py` 新增 `minify()`——字符串段原样保留（tokens.css 含 'rgb(192, 57, 43)' 类字符串令牌），仅对代码段做 8 类等价变换（换行折叠/连续空白/`{ } ; ,` 两侧/`;}`/`:` 后/`>` 两侧/前导零/`!important`）+ 无空白 url 去引号；并补 `url(static/` 前缀替换形态（去引号后原规则失配会致子目录页字体 404）。637 页重同步：块 68,902 → 57,296 B（55.95 KiB·余量 48 B），#2b 转绿。
>
> - **修法②（测试隔离根修）**：`batch_closeout._apply_backfill` 原用 `_sp.run` 直连子进程 ⇒ 单测 mock 不住 `bc.run` ⇒ `bc.main()` 会真实回填本仓台账（W1317 收官因此多出两笔提交）。改走可注入 `run()` + 非零 rc 告警；新增回归测试（subprocess.run 换成抛错桩，退回直连即红）。
>
> - **连带收益**：#1 单页 HTML 最大 448,093 → 436,487 B、软线越线 9 → 7 页；#3 全站 HTML 79.44 → 72.39 MB（−7.05 MB）；#2 页特有最大 49.53 KB 不变。
>
> - **验证**：check_inlined_css 通过（内联 634 · min 57,267B ≥ 20,000 · 特征全过）；capacity #2b 0 越线（#7 仅因未提交暂态，分两笔提交后清零）；inline_css 单页实测字体 url 前缀正确（无无前缀 static/ 残留）；pytest 全量见收官链；verify_delivery 全量见收官链。
>
> - **残余风险（登记）**：#2b 余量仅 48 B ⇒ 共享 CSS 任何净增长都会再次触发机制线（判据按设计工作）；下一批须二选一：CSS 源瘦身（推荐）或由用户裁决机制线校准。
>
> - **文件**：见 file-index W1318 段（site/reader 636 件按目录分组登记）。
>
> - **状态**：容量 #2b 转绿（56 KiB 机制线未动）；测试隔离缺陷根治；判据零放宽（压缩为无损等价变换·分类器与阈值均未改）。
### W1317（2026-11-25）：站内搜索容量余量治理（索引去重 + 语料 gzip+base64 压缩存储）

> **来源**：用户 2026-11-25 指令「先处理容量余量告警」＋同日方案裁决「去重 + 压缩都做」——对象为 check_capacity_budget.py 第 4 条「站内搜索脚本」2,965,520 B / 3 MiB（余量 5.73%）。
>
> - **取证（先证据后结论）**：三项字节 = text-search-app.js 2,160,029 B（99.3% 为内嵌原著明文）+ search-index-zh.js 393,433 B + search-index-en.js 412,058 B；实测 zh 索引 1091 条中 991 条与 en 索引同键同值（生成器「docs 全量两份共用」）⇒ 重复载荷 363,276 B；内嵌语料 gzip 压缩比 0.439（2.15 MB → 941 KB）。
>
> - **修法①索引去重**：`_gen_search_index.py` 拆出 site/data/search-index-docs.js（SITE_SEARCH_INDEX_DOCS·唯一副本）；zh/en 件只存本语言页面条目并改为 `SITE_SEARCH_INDEX_DOCS.concat([...])` 定义（消费方常量名与语义不变·页面 app 零改动）；两搜索页各加一行共享件外链（共享件必须先于本语言件加载）。
>
> - **修法②语料压缩**：`sync_search_corpus.py` 改为 gzip(紧凑 JSON)+base64 单串（EMBEDDED_CORPUS_GZ_B64·2.16 MB → 1.27 MB）；text-search-app.js 新增 decodeCorpus()，运行时以 DecompressionStream('gzip') 解压回填 EMBEDDED_DATA.chapters（file:// 可用·零外域）；旧浏览器不支持该 API 时由 showCorpusError() 给出明确降级提示（不静默失败）；--check 改为「解码后逐条对拍」（跨平台 zlib 字节差异不致假红）。
>
> - **同批根修（line_check 行号语义失效）**：该工具原从站内搜索内嵌语料取行号，W1316 去空白归一后全文无换行 ⇒ 所有引文恒为 line 1、--self-test 自 W1316 起即红。改为直读权威底本 source/原文/分回/*.md 并做空白无关匹配（折行/折行内空格仍可命中），4 正 1 负自测全绿。
>
> - **防漂移（判据同步收紧）**：第 46 槽扩为四判据（C1 三件数据件 + 两页双外链且顺序正确 / C2 docs / C3 zh / C4 en 逐条对拍），--self-test 1 正 6 负；截图分类器登记 docs 共享件为 skip 并放宽外链正则；容量 #4 清单纳入四件（诚实口径·新增字节不得隐形）；单测 6+5 例。
>
> - **验证**：容量 #4 2,965,520 → 1,713,688 B（94.30% → 54.48%·余量 45.5%）；sync_search_corpus --check 零差异；第 46 槽 0 FAIL（docs 991 · zh 100 · en 138）；line_check 自测 4 正 1 负；三页浏览器实测（全文检索「孙悟空」125 处命中 · ZH 全站搜索 24 行 · EN 搜索 7 行）零 console error；node --check 通过；pytest 1639 passed / 4 skipped；verify_delivery 全量见收官链。
>
> - **文件**：见 file-index W1317 段（本批 30+ 件·含新增 site/data/search-index-docs.js）。
>
> - **状态**：容量 #4 由 94.3% 降至 54.5% · 阈值未动 · 判据零放宽（计量面反而纳入新增共享件·无豁免/白名单新增）。
### W1316（2026-11-25）：站内搜索语料单源化（第三份副本清零 + 生成器落地）

> **来源**：用户 2026-11-25 指令「先回填台账 hash 再开批二」＋批二方向裁决「以权威 JSON 重建（推荐）」——对象为批一 triage 的 R2（2.1MB 单文件内嵌语料）与取证新发现的三副本不一致。
>
> - **取证（先证据后结论）**：text-search-app.js 内嵌 chapters 是**第三份语料**——与 source/原文/分回（剥 H1 与尾部识字表、去空白归一）**0/100 回一致**；与 dataset/text-search.json（已由 check_citations.py 与分回逐回全等机器对账）仅 **8/100 回一致**；共少 **789 字**（92 回不一致，7 回差 ≥20 字，多为漏标点/僻字，与 W737「恢复丢段与僻字」方向相反）。原定「从分回 md 生成且逐字节一致」前提不成立。
>
> - **修法（以权威 JSON 为唯一事实源）**：新增 `scripts/sync_search_corpus.py`（JSON → chapters 块渲染·幂等·`--check` 干跑 exit 1）；内嵌块头注释去数字字面量（字符数由页面 KPI 运行时计算·防静态漂移）；text-search.html 说明同步。首次重建即修正 92 回共 789 字；内嵌块 2.1MB → 2.06MB（行内换行归一）。容量 #4 实测 2.83MB / 3MB（未触发·余量 5.7%）。
>
> - **防漂移**：生成器登记 ci_sim GATES（`--check`）+ 第 42 槽脚本覆盖登记 + 单测 5 例（幂等/边界/危险序列 fail-closed/正文含方括号/真实仓树零漂移）。pytest.ini collected 标记 1887→1893。
>
> - **验证**：`sync_search_corpus.py --check` 重建前后各跑（1→0）；`node --check` 通过；全量单测 1638 passed / 4 skipped（199.0s）+ 根级 251 passed；ruff 全过；渲染复核档案 text-search.html sha 已随页面更新。
>
> - **文件**：.github/workflows/README.md, CHANGELOG.md, CITATION.cff, HANDOVER.md, README.md, STRUCTURE.md, docs/00-导读/W批次编号对账表.md, docs/00-导读/项目说明.md, docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md, pyproject.toml, pytest.ini, scripts/check_script_coverage.py, scripts/ci_sim.py, scripts/INDEX.md, scripts/output/_w1205_capacity_audit.json, scripts/output/chart-legend-render-audit.json, scripts/output/file-index.md, scripts/output/stats-changelog.json, scripts/output/stats-index.md, scripts/output/stats.json, scripts/output/svg_text_contrast_graphic_report.json, scripts/output/svg_text_contrast_report.json, scripts/output/tools-inventory.md, scripts/output/_vermilion_solid_cache.json, scripts/sync_search_corpus.py, site/data/text-search.html, site/rss.xml, site/static/js/text-search-app.js, tests/unit/INDEX.md, tests/unit/README.md, tests/unit/test_sync_search_corpus.py
>
> - **状态**：站内搜索语料三副本归一到权威 JSON · 生成器幂等可复核 · 判据零放宽（内容修正按权威源·容量/门禁阈值未动）。

### W1315（2026-11-24）：门禁链共享知识下沉（8 模块依赖环清零 + 体积窗兜底字面量清除）

> **来源**：用户 2026-11-24 指令「先跑批一，把 R5 双下沉和 R3 兜底字面量清理掉」＋同日续令「继续处理 R1 和 T5」——对象为 brooks-lint 健康检查（综合 94/100）确认的四条发现（R5 依赖环 / R3 常量副本 / R1 巨函数 / T5 空体测试）。
>
> - **根因（入口模块兼职共享库）**：同一决策分散住在三个 CLI 入口——常量链 `MAX_DOC_BYTES` / `LEDGER_WINDOW` 在 batch_closeout 顶层、`check_footnote_shape` 在 check_doc_size_budget、账本链 `ROOT` / `LEDGER` / `ARCHIVE_LEDGER` / `parse_ledger` 在 preflight_check ⇒ 消费方只能反向 import 入口，形成 `batch_cascade → check_doc_size_budget → batch_closeout → backfill_changelog → batch_cascade` 与 `preflight_check ↔ check_audit_trigger / check_backlog_review` 的 8 模块强连通分量。
>
> - **修法（双下沉·位置迁移非语义改写）**：`scripts/utils/gate_common.py` 新增治理文档共享段——`MAX_DOC_BYTES`(262144) / `LEDGER_WINDOW`(60) / `LEDGER_REL` / `ARCHIVE_LEDGER_REL` / `parse_ledger`（含 `_locate_status_idx` / `_locate_status` / `_split_touches` / `_locate_touches`）/ `check_footnote_shape`（含 `footnote_tail_shape_ok` 与两条尾句正则）。batch_closeout、check_doc_size_budget、check_audit_trigger、check_backlog_review、check_pitfalls_split、batch_cascade 改为向下引用；preflight_check 保留同名再导出面（测试与旧消费方零改动）。
>
> - **R3 兜底字面量清除**：check_pitfalls_split 的 `except → MAX_DOC_BYTES = 262144` 删除（导入失败即抛错）；check_doc_size_budget 的 `_SAME_SOURCE_ERR` fail-closed 分支与 `MAX_DOC_BYTES if MAX_DOC_BYTES else 262144` 三元同步删除——共享层导入失败在模块加载即抛，fail-fast 强于原静默降级。
>
> - **R1 认知负担治理**：`check_doc_sync.run_self_test` 361 行 → 21 行（39 个用例迁为模块级 `_SELFTEST_CASES` 数据表 + `_selftest_case` 条目工厂，用例文案/顺序/断言前缀逐字保留）；`check_pitfalls_split.evaluate` 233 行 → 33 行编排器，C1-C7 各拆独立判据函数（最长 44 行；C5 指针分支再抽 `_c5_check_pointer`），判据文案与输出数字逐项不变。
>
> - **T5 空体测试改真断言**：`test_kpi_17_dimensions_documented` 原只有 docstring、恒绿 ⇒ 改为断言 `dimensions` 16 条且 `W191` 不在数组内（17 = 16 数据维度 + W191 专题口径）；W191 若入数组即红，杜绝 KPI 口径静默漂移。
>
> - **验证**：scripts 依赖图 SCC 8 → 0（全仓脚本级 Tarjan 复算）；定向单测 135 passed（preflight_check / preflight_touches / four_digit_wnum / doc_size_budget / agents_tail_anchor / w1120 / pitfalls_split / audit_trigger / w1102）；三个门禁 `--self-test` 全过（doc-sync 39/39）；全量单测 1632 passed / 4 skipped（212.3s）+ 根级测试 251 passed；pitfalls 门禁 C1-C7 实盘输出逐项与改前一致（C4 281/281 · C5 263/12/278/0/16/0/0）；ruff 全过。
>
> - **连带发现（不在本批修·留待裁决）**：`tests/unit/test_w1102_batch_closeout.py::test_main_executes_steps_in_declared_order` 调 `bc.main()` 时只 mock 了 `bc.run`，而 `_run_backfill_prev_hash` 走 `_sp.run` 直连子进程 ⇒ 单测会真实回填本仓台账 hash（本批工作树中 W1312/W1314 的 hash 即由此产生）。属测试隔离缺陷，与本批改动无关。
>
> - **文件**：.github/workflows/README.md, CHANGELOG.md, CITATION.cff, HANDOVER.md, README.md, STRUCTURE.md, archive/docs/W批次编号对账表-ARCHIVE.md, docs/00-导读/W批次编号对账表.md, docs/00-导读/项目说明.md, scripts/batch_cascade.py, scripts/batch_closeout.py, scripts/check_audit_trigger.py, scripts/check_backlog_review.py, scripts/check_doc_size_budget.py, scripts/check_doc_sync.py, scripts/check_pitfalls_split.py, scripts/preflight_check.py, scripts/output/file-index.md, scripts/utils/gate_common.py, site/rss.xml, tests/test_narratology_data.py
>
> - **状态**：8 模块环清零 · 巨函数降至 ≤44 行 · 空体测试转真断言 · 判据零放宽（位置迁移/结构拆分/测试补断言；常量值、门禁文案与退出码逐字不变）。

### W1314（2026-11-24）：交接文档结构断言判据校正（尾链取行 + 四段骨架·两条存量假阳性清零）

> **来源**：用户 2026-11-24 指令「先不推送，帮我裁决那两个遗留的假阳性问题」——对象为 W1312/W1313 收官链连续报出的两条 SELF-CHECK 告警。
>
> - **裁决①尾链 = 判据实现缺陷（假阳性）**：原实现 `txt[rfind("最后更新："):]` 命中「维护契约」段内的引用行 ⇒ 尾链 = 整篇正文 ⇒ 日期计数恒 >3、首条 W 取自正文进度 ⇒ 每批必误报。W560 立此判据时文档形态不同，W707 结构收敛后未同步。正确口径 = 同一条 `> 最后更新：` 行内日期条目 ≤3（维护契约②「最新 1–3 批」）。
>
> - **裁决②「九、使用说明」= 判据过期（假阳性）**：该段已随 W707 结构收敛退役，现行维护契约明确零/一/二/三 四段骨架；判据仍按旧九段形态断言 ⇒ 每批必误报。改为四段存在且有序（同时覆盖原「零<一<二」部分断言）。
>
> - **修法（判据校正·非放宽）**：把交接文档结构断言抽成纯函数 `audit_handover_text(txt, batch)`（可单测），`_post_check` 只保留 CR 自愈并调用该函数；尾链改用 `^> 最后更新：` 行定位 + ISO 日期计数；九段判据删除，四段骨架含「三、方法论沉淀」。
>
> - **验证**：新增 `tests/unit/test_w1314_handover_audit.py` 7 例——先红（旧实现无该函数/基准样本误报尾链）后绿；真实 HANDOVER 审计仅剩「头链首条非 W1314」一条**正确**告警（本批入链后消失）；邻接 batch_cascade 测试全绿。
>
> - **文件**：.github/workflows/README.md, AGENTS.md, CHANGELOG.md, CITATION.cff, HANDOVER.md, README.md, STRUCTURE.md, archive/docs/AGENTS-ARCHIVE.md, archive/docs/W批次编号对账表-ARCHIVE.md, archive/docs/workflows-readme-history.md, docs/00-导读/W批次编号对账表.md, docs/00-导读/项目说明.md, docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md, pytest.ini, scripts/batch_cascade.py, scripts/output/INDEX.md, scripts/output/README.md, scripts/output/_cascade_files_W1314.txt, scripts/output/_vermilion_solid_cache.json, scripts/output/_w1266_allrender.json, scripts/output/_w1314_spec.json, scripts/output/chart-legend-render-audit.json, scripts/output/file-index.md, scripts/output/stats-changelog.json, scripts/output/stats-index.md, scripts/output/stats.json, scripts/output/svg_text_contrast_graphic_report.json, scripts/output/svg_text_contrast_report.json, scripts/output/tools-inventory.md, site/data/cross-time-danmaku.html, site/data/tag-cloud.html, site/dukou-engine.html, site/index.html, site/rss.xml, site/sitemap.xml, tests/unit/INDEX.md, tests/unit/README.md, tests/unit/test_w1314_handover_audit.py
>
> - **状态**：两条存量假阳性清零 · 判据零放宽（尾链口径与四段骨架均对齐文档现行契约，并各配机器断言）。

### W1313（2026-11-24）：CSP 面占位符语法治本（connect-src 非法源清零·合法保留域占位源·注入器双形态替换）

> **来源**：用户 2026-11-24 指令「先处理 dukou-engine.html 的占位符冻结项」→ 口径拍板「CSP 内改用合法占位源（推荐）」。
>
> - **根因**：CSP host-source 语法只允许 ALPHA/DIGIT/「-」/「.」——构建期占位符 `__XIJ_SERVICE_BASE__` 含下划线 ⇒ Chrome 判 invalid source 并报 console error（第 43 槽 site/en/dukou-engine.html V1 fail 的冻结项）；generate_csp.py 的 RAG_ORIGIN 直接引用该 token ⇒ dukou 两页 + index + dashboard 四页 CSP 同病。
>
> - **修法（契约 C-8 语义不变）**：新增 `CSP_PLACEHOLDER = https://xij-service-base.invalid`（`.invalid` 保留域·语法合法·浏览器解析零报错且不会发起请求）；generate_csp 的 RAG_ORIGIN 改取该常量并重生成 4 页 CSP；site/_headers 平台层 CSP 同步；inject_service_endpoint 对文本位与 CSP 面两种占位形态一并替换（collect_targets/--check 同步扩面）；守卫承认该 CSP 占位源合法。
>
> - **判据面**：第 70 槽新增 1 条合法形态（经用户拍板·非放宽既有阈值）；第 71 槽不变（CSP meta 属非哈希载体）；第 43 槽 EN 基线再收紧 1 行（828→826）。
>
> - **验证**：第 43 槽 228 页 0 FAIL / 冻结 0 / 可收紧 0 · 第 70 槽违规 0 · 第 71 槽违规 0 · CSP 零漂移（874 页 / 915 哈希）· pytest 19 passed（新增 3 例 + 守卫自测 6→7 例）· 注入器双形态替换有专项单例。
>
> - **文件**：.github/workflows/README.md, AGENTS.md, CHANGELOG.md, CITATION.cff, HANDOVER.md, README.md, STRUCTURE.md, archive/docs/AGENTS-ARCHIVE.md, archive/docs/W批次编号对账表-ARCHIVE.md, archive/docs/workflows-readme-history.md, docs/00-导读/W批次编号对账表.md, docs/00-导读/项目说明.md, docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md, docs/agent/gates.md, pytest.ini, scripts/check_no_hardcoded_endpoint.py, scripts/generate_csp.py, scripts/inject_service_endpoint.py, scripts/output/INDEX.md, scripts/output/README.md, scripts/output/_cascade_files_W1313.txt, scripts/output/_vermilion_solid_cache.json, scripts/output/_w1266_allrender.json, scripts/output/_w1313_spec.json, scripts/output/chart-legend-render-audit.json, scripts/output/chart-values-baseline-en.txt, scripts/output/file-index.md, scripts/output/stats-changelog.json, scripts/output/stats-index.md, scripts/output/stats.json, scripts/output/svg_text_contrast_graphic_report.json, scripts/output/svg_text_contrast_report.json, scripts/output/tools-inventory.md, site/_headers, site/dashboard.html, site/data/cross-time-danmaku.html, site/data/tag-cloud.html, site/dukou-engine.html, site/en/dukou-engine.html, site/index.html, site/rss.xml, site/sitemap.xml, tests/unit/INDEX.md, tests/unit/README.md, tests/unit/test_check_no_hardcoded_endpoint.py
>
> - **遗留（存量假阳性·与本批无关）**：收官链 SELF-CHECK 报「交接文档尾链异常」与「九、使用说明段缺失」两项——前者因检查用 rfind 命中「维护契约」段内的引用行、后者因 HANDOVER 骨架早已收敛为四段；两项均非本批引入，待另批裁决（不在本批放宽或改判据）。
>
> - **状态**：第 43 槽冻结项清零 · 判据零放宽（仅新增 1 条经拍板的合法占位源形态）。

### W1312（2026-11-24）：EN cave-estate 嵌入回退数据归一化治本（file:// 下 22 个 text y=NaN 清零·第 43 槽 EN 基线收紧）

> **来源**：用户 2026-11-24 指令「用 praxis:debug 跑一遍可视化页空白问题的取证流程；用 praxis:tdd 为 verify_delivery.py 补充判据单测」→ 用户批复「好的，执行吧」。
>
> - **取证（先证据后结论）**：第 43 槽全量 228 页扫描中 site/en/cave-estate.html V1 = fail:console-error（n=522）。file:// 直开实测 #chart-region 内 22 个 text.val 的 y="NaN" 且文本为空；同页 http 模式 0 条 NaN、中文页 0 条 NaN ⇒ 症状只出现在「file:// + EN 嵌入回退」组合。
>
> - **根因（一条解释全部症状）**：file:// 下 fetch 被拒 → loadData() catch 直接返回原始 EMBEDDED_DATA，而 by_region 归一化只写在 fetch 成功分支；EN 嵌入版 by_region 是原始嵌套组 [{region, caves:[{name, owner, luxury}]}]，renderRegionChart 读 d.luxury 得 undefined ⇒ scaleLinear(NaN) ⇒ 22 个空标签 + 动画逐帧重设属性产生数百条 console 报错。中文页嵌入版已是扁平形态 {region, luxury, name}，故不受影响。
>
> - **修复（治根不治点）**：抽出 normalizeRegion() 作为唯一归一化入口，fetch 与嵌入回退两条路径共用；嵌入分支返回 Object.assign({}, EMBEDDED_DATA, {by_region: normalizeRegion(...)})。内联脚本改动后重跑 generate_csp.py（1 页更新·874 页 915 哈希零漂移）。
>
> - **验证**：单页复测 V1 ok、冻结 0、可收紧 1 → 删除基线冻结行后全量 228 页复测 0 FAIL、冻结存量 1（余 site/en/dukou-engine.html 的 CSP 占位符·与本批无关）、可收紧 0。
>
> - **判据单测（TDD）**：新增 tests/unit/test_verify_scope_fallback.py 18 例，覆盖 _parse_scope / _classify_scope / _has_embedded_fallback 三条「决定门禁跑不跑」的纯判据；生产代码零改动（git diff scripts/verify_delivery.py 为空）；变异测试两次证明测试会咬（破坏标记剔除 ⇒ 1 例红；破坏越界回退 full ⇒ 4 例红），还原后 18/18 绿。
>
> - **文件**：.github/workflows/README.md, AGENTS.md, CHANGELOG.md, CITATION.cff, HANDOVER.md, README.md, STRUCTURE.md, archive/docs/AGENTS-ARCHIVE.md, archive/docs/W批次编号对账表-ARCHIVE.md, archive/docs/workflows-readme-history.md, docs/00-导读/W批次编号对账表.md, docs/00-导读/项目说明.md, docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md, pytest.ini, scripts/output/INDEX.md, scripts/output/README.md, scripts/output/_cascade_files_W1312.txt, scripts/output/_vermilion_solid_cache.json, scripts/output/_w1266_allrender.json, scripts/output/_w1312_spec.json, scripts/output/chart-legend-render-audit.json, scripts/output/chart-values-baseline-en.txt, scripts/output/file-index.md, scripts/output/stats-changelog.json, scripts/output/stats-index.md, scripts/output/stats.json, scripts/output/svg_text_contrast_graphic_report.json, scripts/output/svg_text_contrast_report.json, scripts/output/tools-inventory.md, site/data/cross-time-danmaku.html, site/data/tag-cloud.html, site/dukou-engine.html, site/en/cave-estate.html, site/index.html, site/rss.xml, tests/unit/INDEX.md, tests/unit/README.md, tests/unit/test_verify_scope_fallback.py
>
> - **状态**：修复 + 基线收紧 + 判据单测完成 · 判据零放宽。

### W1311（2026-11-24）：历史行状态列订正（六行登记滞后清零）+ 复盘批 T140（近三批治理面 + tmpe 清理纪律）

> **来源**：preflight 复盘触发（距上篇复盘 3 天 ≥ 3 天）+ 用户 2026-11-24 指令「现在做」。
>
> - **登记滞后一次性清零**：台账 W1299 / W1300 / W1305 / W1307 / W1309 / W1310 六行的状态列仍是「在途（认领·未收官）」而 git 已有其提交 ⇒ preflight 连续多批告警（P-43-01 口径：告警不拒绝·但长期留存会让「在途」盘点失真）⇒ 本批按 git 事实翻「已收官」并把 W1310 行 hash 回填 41294e71c（链上承载 commit·CI 6/6）⇒ C4-g 可复核。
>
> - **复盘批（T140）**：复盘 W1308–W1310 三批的治理面处置（收官链 archive 死锁治本 / L-08 伪血缘全清 406 件 / 绢本源件补缺入仓）+ tmpe 清理与归桶纪律（2.59→0.29 GiB·MD5 + 像素双证据证无丢失）。
>
> - **两处口径更正**：① 上一轮把「批号目录平铺落 w###/」判为工具缺陷 ⇒ 实查 batch_bucket_dest 的 docstring 明写「无下划线前缀的批号目录保持平铺」⇒ **契约使然** ⇒ 撤下该工具改动项·改记为已知设计边界；② 计划「台账 touches 补 406 件逐件」⇒ 实测 preflight 支持**目录前缀匹配**⇒ 并发保护已有效 ⇒ 改判**不补逐件**（避免台账行膨胀约 5 倍而无判定增益）。
>
> - **文件**：.github/workflows/README.md, AGENTS.md, CHANGELOG.md, CITATION.cff, HANDOVER.md, README.md, STRUCTURE.md, archive/docs/AGENTS-ARCHIVE.md, archive/docs/W批次编号对账表-ARCHIVE.md, archive/docs/workflows-readme-history.md, docs/00-导读/W批次编号对账表.md, docs/00-导读/项目说明.md, docs/11-方案报告/README.md, docs/11-方案报告/计划方案/T140-任务计划执行与经验沉淀报告-2026-11-24.md, docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md, docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md, docs/INDEX.md, scripts/output/INDEX.md, scripts/output/README.md, scripts/output/_cascade_files_W1311.txt, scripts/output/_vermilion_solid_cache.json, scripts/output/_w1266_allrender.json, scripts/output/_w1311_spec.json, scripts/output/chart-legend-render-audit.json, scripts/output/file-index.md, scripts/output/stats-changelog.json, scripts/output/stats-index.md, scripts/output/stats.json, scripts/output/svg_text_contrast_graphic_report.json, scripts/output/svg_text_contrast_report.json, scripts/output/tools-inventory.md, site/data/cross-time-danmaku.html, site/data/search-index-zh.js, site/data/tag-cloud.html, site/dukou-engine.html, site/en/search-index-en.js, site/index.html, site/rss.xml
>
> - **验证**：六行状态列与 git 事实一致 · W1310 行 hash 指向链上承载 commit ⇒ 第 31 门禁 C4-g 绿 · 第 48 门禁（计划方案合规）绿 · 全量门禁真全量 · 判据与阈值**零放宽**。
>
> - **状态**：**登记滞后清零 + 复盘落档**；46 件冻结窗件待 48h 窗开（已挂定时复查）· 4 个活跃工作树禁碰。

### W1310（2026-11-24）：绢本系列 8 张源件入仓（5472×3072 JPEG·补缺·新目录避免覆盖·像素级判别证画面不同）

> **来源**：用户 2026-11-24 指令「请将核对后剩余的 8 张 silk/hero 原图去重后入仓并完成验证」。
>
> - **去重与判别双证据**：tmpe 候选 86 件 → MD5 去重 **47 件** → 仓内已逐字存在 **39 件**（ci_shallow / w1287 工作树只是仓内 assets/ 的副本）⇒ 真正未入库 **8 件**；与仓内同名件尺寸相同（均 5472×3072）但**画面不同**（像素判别 corr 0.34–0.58、dhash hamming 22–32 ⇒ 非压缩差异）⇒ 属**补缺**而非冗余。
>
> - **入仓（新目录·不覆盖既有件）**：assets/promo/silk-hero-src/ —— 既有 assets/promo/silk-hero-set/ 下同名件画面不同 ⇒ 同名入仓即覆盖丢失 ⇒ 独立目录并存 + 目录内 SOURCE.md 说明三者关系与去重依据；8 件按字节拷贝，拷贝后 md5 与源**逐件一致**（8/8）+ PIL 解码校验通过；保留 JPEG 原件不转码（与仓内既有同规格 JPG 做法一致）。
>
> - **文件**：.github/workflows/README.md, AGENTS.md, CHANGELOG.md, CITATION.cff, HANDOVER.md, README.md, STRUCTURE.md, archive/docs/AGENTS-ARCHIVE.md, archive/docs/workflows-readme-history.md, assets/promo/INDEX.md, assets/promo/silk-hero-src/INDEX.md, assets/promo/silk-hero-src/README.md, assets/promo/silk-hero-src/SOURCE.md, assets/promo/silk-hero-src/silk-hero-04-baigu-furen.jpg, assets/promo/silk-hero-src/silk-hero-05-huoyanshan-yaowang.jpg, assets/promo/silk-hero-src/silk-hero-06-heifengshan.jpg, assets/promo/silk-hero-src/silk-hero-07-dumu-qiao.jpg, assets/promo/silk-hero-src/silk-hero-08-shanye-xinglu.jpg, assets/promo/silk-hero-src/silk-hero-09-wukong-tanyu.jpg, assets/promo/silk-hero-src/silk-hero-10-jingubang.jpg, assets/promo/silk-hero-src/silk-hero-11-fabao-sanjian.jpg, docs/00-导读/W批次编号对账表.md, docs/00-导读/项目说明.md, docs/11-方案报告/README.md, docs/11-方案报告/计划方案/T139-任务计划执行与经验沉淀报告-2026-11-24.md, docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md, docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md, docs/INDEX.md, scripts/output/INDEX.md, scripts/output/README.md, scripts/output/_cascade_files_W1310.txt, scripts/output/_vermilion_solid_cache.json, scripts/output/_w1266_allrender.json, scripts/output/_w1309_spec.json, scripts/output/_w1310_spec.json, scripts/output/chart-legend-render-audit.json, scripts/output/file-index.md, scripts/output/stats-changelog.json, scripts/output/stats-index.md, scripts/output/stats.json, scripts/output/svg_text_contrast_graphic_report.json, scripts/output/svg_text_contrast_report.json, scripts/output/tools-inventory.md, site/data/cross-time-danmaku.html, site/data/search-index-zh.js, site/data/tag-cloud.html, site/dukou-engine.html, site/en/search-index-en.js, site/index.html, site/rss.xml
>
> - **验证**：MD5 + 像素级双证据（去重与判别）· 拷贝完整性 8/8 · 尺寸均 5472×3072 · 既有 silk-hero-set/ 12 件未动（零覆盖）· 目录件由收官链 refresh 生成 · 门禁以本批收官时的实跑结果为准（未跑完前不作「绿」的声明）· 判据与阈值**零放宽**。
>
> - **声明与实况不符项**：① 初判「同名 ⇒ 同一画面」⇒ 像素级判别证伪（corr 0.55、hamming 22）⇒ 改为补缺入仓；② 初判「backup-v1 为高清原图·仓内为缩放版」⇒ 实测两者同尺寸 5472×3072 ⇒ 差异在画面内容而非分辨率。
>
> - **状态**：**8 张源件补缺入仓完成**（源件唯一副本风险关闭）· 判据零放宽。

### W1309（2026-11-23）：L-08 闭合（目录件伪血缘一次全清 406 件·残留 0 + 生成器去硬编码日期与 buckets 契约治本 + W1308 五处治本补记坑表 E-316~E-320 + 计数链 421→426）

> **来源**：用户 2026-11-23 指令「请启动 W1309 首批 L-08 目录件伪血缘处理，并在同批补记 W1308 五处治本坑表 E 号、同步计数链」。
>
> - **L-08 闭合（目录件伪血缘一次全清 406 件·残留 0）**：实测目录件 236 目录 / **406 件**带硬编码「生成日期/生成时点：2026-10-18」⇒ 伪血缘。**关键实测**：跑 refresh 只写入 1 件、**43 件被 showcase 保护跳过** ⇒ **405 件属生成器不再托管的目录** ⇒ refresh 永不覆写 ⇒ 只能一次性订正。**生成器治本**：INDEX.md 尾行与 README.md 元信息**不再写死日期**（改「生成来源」标记 ⇒ 伪血缘不再产生且 refresh 幂等）+ 所有权判定抽为 _GEN_OWNERSHIP_MARKERS（含存量旧标记作一次性过渡）+ 新增 **manifest 限定入口**（分小批刷新·边界确定可重放）。**存量订正**：一次性脚本只删两行元信息、**刻意不补「生成来源」标记**（补了等于声明生成器托管 ⇒ 未来 refresh 覆写人工内容）⇒ **幂等**（实测首次订正 50 · 二次 0 订正）· 本批一次全清 **406 件**（实测残留 0）⇒ 登记面按**二级目录聚合**（406 件 → 13 行）以免撑爆 file-index。
>
> - **W1308 五处治本补记坑表**：E-316 归档腾窗迁出量口径（最小达标 + 底线联立 + 两面同下界）· E-317 链首同号替换的日期前缀残留 ⇒ 双日期 · E-318 多行块按行定位 ⇒ 逐次累积 · E-319 补滚触发面（replaced 不触发）与滚动量（一次只滚一块）· E-320 git ls-files 展开目录清单的 ignore 泄漏与中文路径转义 ⇒ 判据层正本（级联 +4 / git +1）+ 归档叙事 5 段 + 根壳反查表 ⇒ 计数链由 stats.py 实算跟随：**总 421→426 · 级联 26→30 · git 39→40**。
>
> - **归档腾窗治本二则（连带）**：W1308 引入的「迁出块不得含编号规则段」保护**过严**——判据把 file-index **表格登记行**里的「本批段 + 编号规则段推进（W001-W13xx 形态）」误认成锚点 ⇒ file-index 最老段被钉死（max_k=0）⇒ 体积窗永远无法腾窗（死锁）。治本：真锚点只在**治理声明行**（以「>」开头的引用行）里识别 ⇒ 登记行文本不再构成迁出禁令（判据单测 +1 例·真锚点仍受保护）。
>
> - **文件**：.agent/skills/puti-shouye/SKILL.md, .github/INDEX.md, .github/ISSUE_TEMPLATE/INDEX.md, .github/ISSUE_TEMPLATE/README.md, .github/workflows/INDEX.md, .github/workflows/README.md, AGENTS.md, CHANGELOG.md, CITATION.cff, HANDOVER.md, INDEX.md, README.md, STRUCTURE.md, archive/INDEX.md, archive/docs/AGENTS-ARCHIVE.md, archive/docs/CHANGELOG-ARCHIVE.md, archive/docs/INDEX.md, archive/docs/README.md, archive/docs/W批次编号对账表-ARCHIVE.md, archive/docs/_dev/INDEX.md, archive/docs/_dev/README.md, archive/docs/_dev/产品管理套件应用-2026-10-02/INDEX.md, archive/docs/_dev/产品管理套件应用-2026-10-02/README.md, archive/docs/_dev/科技服务顾问-数字人文资助渠道-2026-10-02/INDEX.md, archive/docs/_dev/科技服务顾问-数字人文资助渠道-2026-10-02/README.md, archive/docs/file-index-ARCHIVE.md, archive/docs/pitfalls-detail-ARCHIVE.md, archive/docs/plans/INDEX.md, archive/docs/plans/README.md, archive/docs/specs/INDEX.md, archive/docs/specs/README.md, archive/docs/templates/INDEX.md, archive/docs/w550-shot-review/INDEX.md, archive/docs/w550-shot-review/README.md, archive/docs/workflows-readme-history.md, archive/docs/复盘报告/INDEX.md, archive/docs/复盘报告/README.md, archive/hyperframes/INDEX.md, archive/hyperframes/compositions/INDEX.md, archive/hyperframes/compositions/README.md, archive/hyperframes/compositions/d3-visualizations/INDEX.md, archive/hyperframes/compositions/d3-visualizations/README.md, archive/hyperframes/output/INDEX.md, archive/hyperframes/output/README.md, archive/scripts/INDEX.md, archive/scripts/README.md, archive/scripts/attic/INDEX.md, archive/scripts/audit/INDEX.md, archive/scripts/batches/INDEX.md, archive/scripts/batches/README.md, archive/scripts/batches/misc/INDEX.md, archive/scripts/batches/misc/README.md, archive/scripts/batches/w1071/INDEX.md, archive/scripts/batches/w1071/README.md, archive/scripts/batches/w1073/INDEX.md, archive/scripts/batches/w1073/README.md, archive/scripts/batches/w1074/INDEX.md, archive/scripts/batches/w1074/README.md, archive/scripts/batches/w1076/INDEX.md, archive/scripts/batches/w1076/README.md, archive/scripts/batches/w1078/INDEX.md, archive/scripts/batches/w1078/README.md, archive/scripts/batches/w1079/INDEX.md, archive/scripts/batches/w1079/README.md, archive/scripts/batches/w1080/INDEX.md, archive/scripts/batches/w1080/README.md, archive/scripts/batches/w1089/INDEX.md, archive/scripts/batches/w1089/README.md, archive/scripts/batches/w10xx/INDEX.md, archive/scripts/batches/w10xx/README.md, archive/scripts/batches/w1100/INDEX.md, archive/scripts/batches/w1100/README.md, archive/scripts/batches/w1169/INDEX.md, archive/scripts/batches/w1169/README.md, archive/scripts/batches/w1175/INDEX.md, archive/scripts/batches/w1175/README.md, archive/scripts/batches/w1176/INDEX.md, archive/scripts/batches/w1176/README.md, archive/scripts/batches/w4xx/INDEX.md, archive/scripts/batches/w4xx/README.md, archive/scripts/batches/w5xx/INDEX.md, archive/scripts/batches/w5xx/README.md, archive/scripts/batches/w6xx/INDEX.md, archive/scripts/batches/w6xx/README.md, archive/scripts/batches/w7xx/INDEX.md, archive/scripts/batches/w7xx/README.md, archive/scripts/batches/w8xx/INDEX.md, archive/scripts/batches/w8xx/README.md, archive/scripts/batches/w9xx/INDEX.md, archive/scripts/batches/w9xx/README.md, archive/scripts/review-pass3/INDEX.md, archive/scripts/review-pass3/README.md, archive/scripts/review-pass3/prompts/INDEX.md, archive/scripts/review-pass3/prompts/README.md, assets/INDEX.md, assets/README.md, assets/design/INDEX.md, assets/design/ai-concepts/INDEX.md, assets/design/alternatives/INDEX.md, assets/design/logo/INDEX.md, assets/design/process/INDEX.md, assets/design/screenshots/INDEX.md, assets/design/tools/INDEX.md, assets/fonts/INDEX.md, assets/fonts/README.md, assets/fonts/source/INDEX.md, assets/fonts/source/README.md, assets/game/INDEX.md, assets/game/README.md, assets/game/js/INDEX.md, assets/game/js/README.md, assets/promo/INDEX.md, assets/promo/hero-set/INDEX.md, assets/promo/hero-set/raw/INDEX.md, assets/promo/hero-set/raw/round-w1005/INDEX.md, assets/promo/hero-set/raw/round-w1005/README.md, assets/promo/output/INDEX.md, assets/promo/output/README.md, assets/promo/plate-set/INDEX.md, assets/promo/silk-hero-set/INDEX.md, dataset/INDEX.md, dataset/entities/INDEX.md, dataset/entities/README.md, docs/00-导读/INDEX.md, docs/00-导读/W批次编号对账表.md, docs/00-导读/遗留总账.md, docs/00-导读/项目说明.md, docs/07-学以致用/INDEX.md, docs/08-提升认知/INDEX.md, docs/09-精神塑造/INDEX.md, docs/11-方案报告/README.md, docs/11-方案报告/计划方案/T138-任务计划执行与经验沉淀报告-2026-11-23.md, docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md, docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md, docs/12-提示词库/INDEX.md, docs/12-提示词库/README.md, docs/INDEX.md, docs/README.md, docs/_templates/INDEX.md, docs/_templates/README.md, docs/_templates/duipai/INDEX.md, docs/agent-guardrails/INDEX.md, docs/agent/INDEX.md, docs/agent/README.md, docs/agent/pitfalls-topics/INDEX.md, docs/agent/pitfalls-topics/README.md, docs/agent/pitfalls-topics/cascade-changelog.md, docs/agent/pitfalls-topics/css-visual.md, docs/agent/pitfalls-topics/data-trust.md, docs/agent/pitfalls-topics/flow-collab.md, docs/agent/pitfalls-topics/git-concurrency.md, docs/agent/pitfalls-topics/js-csp-runtime.md, docs/agent/pitfalls.md, docs/superpowers/INDEX.md, docs/superpowers/README.md, docs/superpowers/plans/INDEX.md, docs/superpowers/plans/README.md, mcp-server/INDEX.md, packaging/INDEX.md, packaging/README.md, packaging/xiyouji-analysis/INDEX.md, packaging/xiyouji-analysis/src/INDEX.md, packaging/xiyouji-analysis/src/README.md, packaging/xiyouji-analysis/src/xiyouji_analysis/INDEX.md, packaging/xiyouji-analysis/src/xiyouji_analysis/README.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/AA_叙事实验/INDEX.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/AA_叙事实验/README.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/AB_视觉艺术/INDEX.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/AB_视觉艺术/README.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/AC_方法论矩阵/INDEX.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/AC_方法论矩阵/README.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/AD_认知心理/INDEX.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/AD_认知心理/README.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/AE_生态学/INDEX.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/AE_生态学/README.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/AF_法理经济/INDEX.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/AF_法理经济/README.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/AG_物质考古/INDEX.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/AG_物质考古/README.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/AH_语言学/INDEX.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/AH_语言学/README.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/A_文本基础/INDEX.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/A_文本基础/README.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/B_人物/INDEX.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/B_人物/README.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/C_情节/INDEX.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/C_情节/README.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/D_关系/INDEX.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/D_关系/README.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/E_地理/INDEX.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/E_地理/README.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/G_哲学/INDEX.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/G_哲学/README.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/H_风险与项目/INDEX.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/H_风险与项目/README.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/INDEX.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/I_妖怪社会学/INDEX.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/I_妖怪社会学/README.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/J_权力与资源/INDEX.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/J_权力与资源/README.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/K_命运与轮回/INDEX.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/K_命运与轮回/README.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/L_商业模型/INDEX.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/L_商业模型/README.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/M_洞府房产/INDEX.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/M_洞府房产/README.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/N_法术阵法/INDEX.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/N_法术阵法/README.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/O_美学时尚/INDEX.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/O_美学时尚/README.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/P_音乐声效/INDEX.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/P_音乐声效/README.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/Q_源流演变/INDEX.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/Q_源流演变/README.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/README.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/R_解构作品/INDEX.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/R_解构作品/README.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/S_全球模式/INDEX.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/S_全球模式/README.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/T_反事实推断/INDEX.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/T_反事实推断/README.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/U_文化错位/INDEX.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/U_文化错位/README.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/V_打工人职场/INDEX.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/V_打工人职场/README.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/W_社媒人设/INDEX.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/W_社媒人设/README.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/X_游戏网文/INDEX.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/X_游戏网文/README.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/Y_伦理消费/INDEX.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/Y_伦理消费/README.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/Z_图表设计/INDEX.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/Z_图表设计/README.md, pitfalls.md, pytest.ini, scripts/AA_叙事实验/INDEX.md, scripts/AA_叙事实验/README.md, scripts/AB_视觉艺术/INDEX.md, scripts/AB_视觉艺术/README.md, scripts/AC_方法论矩阵/INDEX.md, scripts/AC_方法论矩阵/README.md, scripts/AD_认知心理/INDEX.md, scripts/AD_认知心理/README.md, scripts/AE_生态学/INDEX.md, scripts/AE_生态学/README.md, scripts/AF_法理经济/INDEX.md, scripts/AF_法理经济/README.md, scripts/AG_物质考古/INDEX.md, scripts/AG_物质考古/README.md, scripts/AH_语言学/INDEX.md, scripts/AH_语言学/README.md, scripts/A_文本基础/INDEX.md, scripts/A_文本基础/README.md, scripts/B_人物/INDEX.md, scripts/B_人物/README.md, scripts/C_情节/INDEX.md, scripts/C_情节/README.md, scripts/D_关系/INDEX.md, scripts/D_关系/README.md, scripts/E_地理/INDEX.md, scripts/E_地理/README.md, scripts/F_时间/INDEX.md, scripts/F_时间/README.md, scripts/G_哲学/INDEX.md, scripts/G_哲学/README.md, scripts/H_风险与项目/INDEX.md, scripts/H_风险与项目/README.md, scripts/INDEX.md, scripts/I_妖怪社会学/INDEX.md, scripts/I_妖怪社会学/README.md, scripts/J_权力与资源/INDEX.md, scripts/J_权力与资源/README.md, scripts/K_命运与轮回/INDEX.md, scripts/K_命运与轮回/README.md, scripts/L_商业模型/INDEX.md, scripts/L_商业模型/README.md, scripts/M_洞府房产/INDEX.md, scripts/M_洞府房产/README.md, scripts/N_法术阵法/INDEX.md, scripts/N_法术阵法/README.md, scripts/O_美学时尚/INDEX.md, scripts/O_美学时尚/README.md, scripts/P_音乐声效/INDEX.md, scripts/P_音乐声效/README.md, scripts/Q_源流演变/INDEX.md, scripts/Q_源流演变/README.md, scripts/R_解构作品/INDEX.md, scripts/R_解构作品/README.md, scripts/S_全球模式/INDEX.md, scripts/S_全球模式/README.md, scripts/T_反事实推断/INDEX.md, scripts/T_反事实推断/README.md, scripts/U_文化错位/INDEX.md, scripts/U_文化错位/README.md, scripts/V_打工人职场/INDEX.md, scripts/V_打工人职场/README.md, scripts/W_社媒人设/INDEX.md, scripts/W_社媒人设/README.md, scripts/X_游戏网文/INDEX.md, scripts/X_游戏网文/README.md, scripts/Y_伦理消费/INDEX.md, scripts/Y_伦理消费/README.md, scripts/Z_图表设计/INDEX.md, scripts/Z_图表设计/README.md, scripts/api/INDEX.md, scripts/api/README.md, scripts/archive_segments.py, scripts/audit/INDEX.md, scripts/audit/README.md, scripts/gen_folder_docs.py, scripts/guardrails/INDEX.md, scripts/guardrails/README.md, scripts/lib/INDEX.md, scripts/lib/README.md, scripts/lighthouse/INDEX.md, scripts/lighthouse/README.md, scripts/output/INDEX.md, scripts/output/README.md, scripts/output/_cascade_files_W1309.txt, scripts/output/_vermilion_solid_cache.json, scripts/output/_w1266_allrender.json, scripts/output/_w1309_batch1.txt, scripts/output/_w1309_fix_legacy_dates.py, scripts/output/_w1309_pitfalls_patch.py, scripts/output/_w1309_spec.json, scripts/output/chart-legend-render-audit.json, scripts/output/data/INDEX.md, scripts/output/data/README.md, scripts/output/figures/INDEX.md, scripts/output/figures/README.md, scripts/output/file-index.md, scripts/output/stats-changelog.json, scripts/output/stats-index.md, scripts/output/stats.json, scripts/output/svg_text_contrast_graphic_report.json, scripts/output/svg_text_contrast_report.json, scripts/output/tools-inventory.md, scripts/rag/INDEX.md, scripts/rag/eval/INDEX.md, scripts/rag/eval/README.md, scripts/utils/INDEX.md, scripts/utils/README.md, site/INDEX.md, site/README.md, site/chapters/INDEX.md, site/chapters/README.md, site/characters/INDEX.md, site/characters/README.md, site/data/INDEX.md, site/data/README.md, site/data/cross-time-danmaku.html, site/data/json/INDEX.md, site/data/json/README.md, site/data/search-index-zh.js, site/data/tag-cloud.html, site/dukou-engine.html, site/en/INDEX.md, site/en/json/INDEX.md, site/en/json/README.md, site/en/search-index-en.js, site/index.html, site/js/INDEX.md, site/js/README.md, site/reader/INDEX.md, site/reader/README.md, site/reader/culture/INDEX.md, site/reader/culture/README.md, site/reader/essays/INDEX.md, site/reader/essays/README.md, site/reader/people/INDEX.md, site/reader/people/README.md, site/reader/poetry/INDEX.md, site/reader/poetry/README.md, site/reader/themes/INDEX.md, site/reader/themes/README.md, site/rss.xml, site/static/INDEX.md, site/static/README.md, site/static/css/INDEX.md, site/static/css/README.md, site/static/fonts/INDEX.md, site/static/fonts/README.md, site/static/icons/INDEX.md, site/static/icons/README.md, site/static/icons/ui/INDEX.md, site/static/icons/ui/README.md, site/static/images/INDEX.md, site/static/images/README.md, site/static/images/silk-src/INDEX.md, site/static/images/silk-src/README.md, site/static/img/INDEX.md, site/static/img/README.md, site/static/js/INDEX.md, site/static/js/README.md, site/themes/INDEX.md, site/themes/README.md, source/INDEX.md, source/README.md, source/原文/INDEX.md, source/原文/README.md, source/原文/shendu/INDEX.md, source/原文/shendu/README.md, source/原文/分回/INDEX.md, source/原文/分回/README.md, source/引用与网络解读/INDEX.md, source/引用与网络解读/README.md, tests/INDEX.md, tests/README.md, tests/e2e/INDEX.md, tests/e2e/README.md, tests/e2e/baseline/INDEX.md, tests/e2e/baseline/README.md, tests/fixtures/INDEX.md, tests/fixtures/README.md, tests/unit/INDEX.md, tests/unit/README.md, tests/unit/test_archive_segments_migration_plan.py, xiyouji-agent-web/INDEX.md, xiyouji-agent-web/deploy/INDEX.md, xiyouji-agent-web/deploy/README.md, xiyouji-agent-web/deploy/pg/INDEX.md, xiyouji-agent-web/deploy/pg/bin/INDEX.md, xiyouji-agent-web/deploy/pg/bin/README.md, xiyouji-agent-web/deploy/pg/migrations/INDEX.md, xiyouji-agent-web/deploy/pg/migrations/README.md, xiyouji-agent-web/e2e/INDEX.md, xiyouji-agent-web/e2e/README.md, xiyouji-agent-web/evals/INDEX.md, xiyouji-agent-web/evals/README.md, xiyouji-agent-web/fuzz/INDEX.md, xiyouji-agent-web/fuzz/README.md, xiyouji-agent-web/server/INDEX.md, xiyouji-agent-web/server/README.md, xiyouji-agent-web/server/compliance/INDEX.md, xiyouji-agent-web/server/compliance/README.md, xiyouji-agent-web/server/engine/INDEX.md, xiyouji-agent-web/server/engine/README.md, xiyouji-agent-web/server/storage/INDEX.md, xiyouji-agent-web/server/storage/README.md, xiyouji-agent-web/src/INDEX.md, xiyouji-agent-web/src/README.md, xiyouji-agent-web/src/components/INDEX.md, xiyouji-agent-web/src/components/README.md, xiyouji-agent-web/src/components/toolCalls/INDEX.md, xiyouji-agent-web/src/components/toolCalls/README.md, xiyouji-agent-web/src/hooks/INDEX.md, xiyouji-agent-web/src/hooks/README.md, xiyouji-agent-web/src/pages/INDEX.md, xiyouji-agent-web/src/pages/README.md, xiyouji-agent-web/src/test/INDEX.md, xiyouji-agent-web/src/test/README.md, xiyouji-agent-web/src/utils/INDEX.md, xiyouji-agent-web/src/utils/README.md, xiyouji-desktop/INDEX.md, xiyouji-desktop/assets/INDEX.md, xiyouji-desktop/assets/README.md, xiyouji-desktop/scripts/INDEX.md, xiyouji-desktop/scripts/README.md, xiyouji-desktop/src/INDEX.md, xiyouji-desktop/src/README.md, xiyouji-desktop/tests/INDEX.md, xiyouji-desktop/tests/README.md, scripts/batch_spec.py, scripts/backfill_changelog.py, scripts/batch_cascade.py
>
> - **验证**：坑表判据 **0 FAIL**（check_pitfall_id_unique 新增 5 条 · check_pitfalls_split C1–C7 全 PASS·声明 426 = 实算 426·反查表遗漏 0 多余 0）· 订正幂等自证（首次 50 · 二次 0）· 抽样 diff 仅删两行元信息·内容逐字无损 · 台账 W1308 行收官回填 a5205ba5d + W1309 认领行（touches 逐件 105 项）· 判据与阈值**零放宽**。
>
> - **声明与实况不符项**：① 初判「根因是 CRLF ⇒ 生成器改 LF 即可」⇒ 实测 LF 早已治（W1307）⇒ 根因收窄为「硬编码日期 + showcase 保护面」；② 计划「订正约 50 件」⇒ 实入库 93 件（50 + 43 历史累积）⇒ 一次清空避免每批带累积跑；③ 计划「新增 E-297~E-301」⇒ 实测 E-297~E-300 已被数据主题占用（现存最大 E-315）⇒ 改用 E-316~E-320。
>
> - **状态**：**L-08 第 1 小批完成**（剩余 313 件待 W1310–W1315）· 坑表补记与计数链同步完成 · 判据零放宽。

### W1308（2026-11-23）：收官链 L-11 治本 (hash 回填 v2 链上口径 + 排除本批 + 错值修指) + 代改 5 行悬空 hash 清零豁免基线 + L-12 确认既有闸门覆盖 + 归档腾窗治本 (迁出量最小化 + 两面同下界)

> **来源**：用户 2026-11-23 裁决「继续，给我选项我来决策」→ 四项裁决：L-08 分 8 小批 · L-11+L-12 都做 · 5 行悬空 hash 我代改 · tmpe 冻结区等窗后清且 JPG 保留本地 ⇒ 立项 W1308（收官链 L-11 治本 + 悬空 hash 代改清零 + 归档腾窗治本）。
>
> - **L-11 治本**：收官链新增 `_run_backfill_prev_hash_v2`（最小侵入：新增函数 + 只切调用点·v1 保留可回退）—— 四处口径变更：① 候选来源 `git log --reverse HEAD`（**只在当前历史链上取**·v1 用 `--all` 会把已失效 commit 再次写回台账⇒悬空复发）② subject 含**多个 W 号**时全部登记（合并推送形态）③ **排除本批**（自指不可知⇒本批 hash 必留空待下一批⇒amend 不再制造悬空）④ hash 非空但**不在链上** ⇒ 改指该批链上首笔（错值修指）。纯函数 `_parse_subject_w_ids` / `_prefix_sets` / `_hash_action` + 单测 **8 例全绿**。
>
> - **代改 5 行悬空 hash（用户授权）**：按「该批在 main 历史链上的最早承载 commit」逐行算 ⇒ W1294→`694fae2e5b` · W1295→`2d33f5f11a` · W1296→`c51794db9b` · W1301/W1303→`0c926a0aac`（合并推送那笔）⇒ 用仓内**独占回填工具** `ledger_backfill.py --w N --hash <sha>`（锁旧指纹→改→出新指纹）执行 ⇒ **`merge-base --is-ancestor` 5/5 True** ⇒ **豁免基线清零** ⇒ **C4-g 今后对任何新增悬空行一律判红**（机制保留、无存量）。
>
> - **L-12 结论**：**无需新判据**——链尾 `gate` 步调 `pre_push_gate.py`（单一事实源），其中已有「主工作树干净(含未跟踪)」一项 ⇒ 链外再改在链尾即被拦 ⇒ 已在总账转闭合（避免重复实现与口径漂移）。
>
> - **归档腾窗治本（W1308 收官链 archive 步死锁的根修）**：收官链 archive 步在本批首次失败——`archive_segments.plan_by_size` 以 `chunk=50` 为**固定步长**迁出（迁出量由 chunk 决定而非由体积决定）⇒ file-index 正本 50 段·体积 262,964 B **仅超窗 820 B**，却被迫迁出 44 段 ⇒ 正本仅剩 6 段 ⇒ 铁律 22「正本留 ≥ 20 段」断言 FAIL ⇒ 收官链死锁。**三处根修（判据只加严不放宽）**：① `plan_by_size` 改「二分求**最小达标** k」（实测迁 2 段·留存 48 段）；② 迁出上界收紧为「迁出块不得含编号规则段」（原上界会把编号规则段一并迁走⇒版本面推进器 fail-closed）；③ `_rule_seg_index` 假阳性修正——CHANGELOG 的编号规则串实际落在**末尾文件级块**（`## [Unreleased]`）内（该块不随段迁出）⇒ 原实现把最后一个批段误判为「不可迁出段」⇒ CHANGELOG 面永远无法腾窗。**新增对齐能力** `plan_align_below` + `main()` 改「各面按最小达标规划 → 取目标下界 → 两面统一迁出」⇒ 迁出后两面同下界 W1256（`rebuild_section.boundary_check` 硬断言）· 并加「迁出后体积达标」纯计算断言。判据单测 **5 例**（最小达标最小性 / 编号规则段保护 / 末尾块假阳性 / 对齐迁出语义 / 仓内两面同下界且各留 ≥ 20 段）。
>
> - **cascade 链首日期前缀残留治本（连带）**：本批 regsurface 步首次报红「HANDOVER 无「最后更新」行」⇒ 根因是 `batch_cascade._upsert_chain_entry` 的「按批号替换」分支只替换「（W#### …）」括号区间 ⇒ 同号条目**文本变更**时条目左侧的旧日期前缀残留 ⇒ 产出「最后更新：2026-11-232026-11-23（W1308 …）」双日期 ⇒ 登记面一致性闸的正则「最后更新：<日期>（W####」匹配不上。治本：新增 `_entry_start`（替换区间自日期前缀起算·头链尾链共用·单一事实源）+ `_same` 匹配纳入可选日期前缀 + 内容一致但有残留时亦清理（幂等自愈）⇒ 判据单测 **3 例**。
>
> - **文件**：.github/workflows/README.md, AGENTS.md, CHANGELOG.md, CITATION.cff, HANDOVER.md, README.md, STRUCTURE.md, pytest.ini, archive/docs/AGENTS-ARCHIVE.md, archive/docs/CHANGELOG-ARCHIVE.md, archive/docs/file-index-ARCHIVE.md, archive/docs/W批次编号对账表-ARCHIVE.md, archive/docs/workflows-readme-history.md, docs/INDEX.md, docs/00-导读/W批次编号对账表.md, docs/00-导读/遗留总账.md, docs/00-导读/项目说明.md, docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md, docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md, docs/11-方案报告/计划方案/T137-任务计划执行与经验沉淀报告-2026-11-23.md, scripts/archive_segments.py, scripts/batch_cascade.py, scripts/batch_closeout.py, scripts/output/INDEX.md, scripts/output/README.md, scripts/output/_cascade_files_W1308.txt, scripts/output/_vermilion_solid_cache.json, scripts/output/_w1266_allrender.json, scripts/output/_w1308_spec.json, scripts/output/chart-legend-render-audit.json, scripts/output/file-index.md, scripts/output/stats-changelog.json, scripts/output/stats-index.md, scripts/output/stats.json, scripts/output/svg_text_contrast_graphic_report.json, scripts/output/svg_text_contrast_report.json, scripts/output/tools-inventory.md, site/data/cross-time-danmaku.html, site/data/search-index-zh.js, site/data/tag-cloud.html, site/en/search-index-en.js, site/dukou-engine.html, site/index.html, site/rss.xml, tests/unit/INDEX.md, tests/unit/README.md, tests/unit/test_archive_segments_migration_plan.py, tests/unit/test_batch_closeout_hash_repair.py, tests/unit/test_cascade_chain_entry_date_prefix.py, tests/unit/test_cascade_handover_rotate.py
>
> - **验证**：判据单测 **8 passed**（L-11）· 归档腾窗单测 **5 passed** · cascade 链首单测 **3 passed** · W1144 补滚单测 **3 passed** · 分组展开单测 **3 passed** · 5 行代改后 `is-ancestor` 全 True · 豁免基线剩余 **0 行** · 第 31 门禁 C4-g 判红 0 · 归档 dry-run 实测「两面各迁 2 段（W1253-W1255）·留存 48 段·同下界 W1256」· **门禁段数与阈值零放宽**（只加严不加松）。
>
> - **声明与实况不符项**：① 初判「L-12 需新增链末自检判据」⇒ 实测既有闸门已等效覆盖 ⇒ 改为不新增；② 初判「立式分组可承载 400+ 行登记面」⇒ 实测 `fi_group_rows` **只对同目录连续文件压缩**（跨目录 0%）⇒ 已据此修正 L-08 的可行路径；③ 初判「archive 失败是段数窗与体积窗不可兼得」⇒ 实测根因是**迁出量由 chunk 决定**而非两窗互斥 ⇒ 改为最小达标二分 + 两面同下界对齐迁出。
>
> - **状态**：**L-11 闭合 · 豁免基线清零 · L-12 转闭合（既有闸门覆盖）· 归档腾窗已使能**；**L-08 维持未清偿**（按用户裁决分 8 小批·W1309–W1315·归档腾窗前置条件已达成）；tmpe 冻结区等 48h 窗后清、8 张 JPG 原图保留本地。

### W1307（2026-11-23）：遗留清偿批 (L-08 目录件伪血缘治本 409 件一次清且此后幂等 + L-09/L-10 W1304 spec 对齐 + W1306 行 hash 回填)

> **来源**：用户 2026-11-23 指令「继续」（承接 W1306 遗留收敛判据批）⇒ 立项 W1307（遗留清偿批）。
>
> - **L-08 治本**：`scripts/gen_folder_docs.py` 两处**硬编码日期**（生成时点 2026-10-18 / 生成日期 2026-10-18）改为**不再写死日期**（指向本文件 git 提交时间）⇒ 全仓 **409 件目录件一次性刷新**（631 增 / 632 删·仅日期行）⇒ **伪血缘消除**且**此后 refresh 幂等**（此前每次 refresh 必改日期 ⇒ 「门禁自产残留」噪声源之一）。
>
> - **L-09/L-10 治本**：`_w1304_spec.json` 的 file_index_rows 剔除**越界行** `scripts/output/chart-legend-render-audit.md`（不在 W1304 提交树内）⇒ 31→30 行与提交实算**逐条相等**；同一 spec 的 changelog_body「文件」行按 `git show --name-only -z` 实算重写（16 项→30 项）⇒ 报告型文档与实况脱节修正；两面段经 `rebuild_section --batch W1304 --apply` 同步。
>
> - **W1306 行 hash 回填**：用仓内**独占回填工具** `ledger_backfill.py --w 1306 --hash a62b3cc54 --status …`（锁旧指纹→改→出新指纹 `02350f9286b3`）⇒ **C4-g 判据实测通过**（该 hash 在 main 历史链上）。
>
> - **文件**：.github/workflows/README.md, AGENTS.md, CHANGELOG.md, CITATION.cff, HANDOVER.md, STRUCTURE.md, archive/docs/AGENTS-ARCHIVE.md, archive/docs/W批次编号对账表-ARCHIVE.md, archive/docs/workflows-readme-history.md, docs/00-导读/W批次编号对账表.md, docs/00-导读/遗留总账.md, docs/00-导读/项目说明.md, docs/11-方案报告/README.md, docs/11-方案报告/计划方案/T136-任务计划执行与经验沉淀报告-2026-11-23.md, docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md, docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md, docs/INDEX.md, scripts/output/INDEX.md, scripts/output/README.md, scripts/output/_cascade_files_W1307.txt, scripts/output/_vermilion_solid_cache.json, scripts/output/_w1266_allrender.json, scripts/output/_w1304_spec.json, scripts/output/_w1307_spec.json, scripts/output/chart-legend-render-audit.json, scripts/output/stats-changelog.json, scripts/output/stats.json, scripts/output/svg_text_contrast_graphic_report.json, scripts/output/svg_text_contrast_report.json, scripts/output/tools-inventory.md, site/data/cross-time-danmaku.html, site/data/search-index-zh.js, site/data/tag-cloud.html, site/dukou-engine.html, site/en/search-index-en.js, site/index.html, site/rss.xml, site/sitemap.xml
>
> - **验证**：第 31 门禁 **0 FAIL**（C4-g 5 行存量悬空在豁免基线内 ⇒ NOTE）· 第 48 门禁计划方案模板 **PASS（全项符合）**· refresh 二次运行**零 diff**（幂等自证）· 台账正本 60 行（窗口内·登记前先归档已收官 W1243）· **判据与阈值零放宽**。
>
> - **声明与实况不符项**：① 初判 `ledger_backfill --w W1306` 报错为工具缺陷 ⇒ 实为**参数格式**（要整数）⇒ 已改正；② 本批属「订正」而非擅改历史段：W1304 spec 与其两面段按提交实算对齐，已在 T136 §九 声明。
>
> - **状态**：**遗留总账 L-08/L-09/L-10 三项治本闭合**（未清偿 5 → 2）· **L-11/L-12 维持未清偿**（涉收官链核心路径 `_run_backfill_prev_hash` 与链尾结构 ⇒ 独立批次治本）· 豁免基线 5 行他方悬空 hash 不代改。

### W1306（2026-11-23）：遗留收敛落机器判据 (C4-g 台账 hash 历史链有效性 + C4-h 审查 P2 编号化登记 + 收尾两分类声明)

> **来源**：用户 2026-11-23 追问「为什么每次结束都有遗留的任务要下一批去做？」⇒ 立项 W1306（遗留收敛落机器判据批）。
>
> - **问题归因（四类·见报告 §四）**：A 自指不可知（数学必然）· B 链外改动打破链内闭合（**本会话自造**）· C 压缩推送挤出历史链（并发共享面）· D 审查后置发现（P2 必留）。
>
> - **判据 3（治 C）**：第 31 门禁新增 **C4-g「台账 hash 历史链有效性」**——判定口径**必须**用 `git rev-list HEAD` 前缀匹配（`git rev-parse --verify` 只查对象库存在性 ⇒ 对被压缩掉的 commit **假阳性**）；**存量豁免基线**登记在遗留总账（5 行悬空 ⇒ 基线内 NOTE、基线外 FAIL ⇒ 判据上线不即红）。
>
> - **判据 4（治 D）**：第 31 门禁新增 **C4-h「审查 P2 编号化登记」**——现役段含 P2 而遗留总账「未清偿项」区无 L-xx 登记 ⇒ FAIL（**P2 不得只留在报告/聊天里**）；对抗审查模板同步补该义务；审查 P2 三项已登记为 **L-08/L-09/L-10**。
>
> - **判据 5（治自己造成的遗留）**：收官模板新增「**遗留两分类声明**」必填条款——① 我能单方面闭合的**必须为 0**（否则本批不得收官）② 需他人/用户裁决的列明编号与对象。
>
> - **文件**：CHANGELOG.md, HANDOVER.md, archive/docs/W批次编号对账表-ARCHIVE.md, docs/00-导读/W批次编号对账表.md, docs/00-导读/遗留总账.md, docs/agent/adversarial-audit-prompt.md, docs/agent/closeout-agent-prompt.md, scripts/check_doc_sync.py, tests/unit/test_doc_sync_ledger_hash.py, scripts/output/_w1306_spec.json, scripts/output/_cascade_files_W1306.txt, scripts/output/file-index.md, scripts/output/stats-changelog.json, scripts/output/stats-index.md, scripts/output/stats.json, scripts/output/tools-inventory.md, scripts/output/INDEX.md, scripts/output/README.md, tests/unit/INDEX.md, tests/unit/README.md, docs/INDEX.md
>
> - **验证**：`python scripts/check_doc_sync.py` **0 FAIL**（C4-g 5 行降为存量豁免 NOTE）· 新增单测 `tests/unit/test_doc_sync_ledger_hash.py` **5 passed**（台账 hash 定位·祖先前缀匹配·豁免基线两态·短 hash 前缀）· 台账写窗顶破按判据归档已收官 W1242 腾移（正本 59 行 + 本批认领行 = 60 行·窗口内）· **判据与阈值零放宽**（只加严不加松）。
>
> - **状态**：**3/5 条已落成机器判据**（判据 3/4/5）；**判据 1（自指不可知 ⇒ 自动回填扩到「错值」修指）与判据 2（收官链链末自检：链跑完后工作树必须干净）**涉及收官链核心路径，本批未动（风险高）⇒ 已登记为遗留总账 L-11/L-12 候补项，下一批单独治本。
>
> - **声明与实况不符项**：① 本批初判「豁免基线解析失败 ⇒ 判据有 bug」——实为**两处自身实现缺陷**（正则缺 `re.M` + 捕获组是纯数字而正本解析出 `W####`）⇒ 已修（并各有单测覆盖）；② 上一轮普查曾误报「悬空 hash 0 行」⇒ 实为**取错列**（hash 在第 4 段不是第 3 段）⇒ 已复核为 5 行。

### W1305（2026-11-22）：对抗审查 P0/P1 同批治本 (spec 大小写归一 + 台账 hash 合并口径 + 黏行无损还原 + T135 声明不符项更正)

> **来源**：W1305 对抗审查（独立只读 subagent·实跑像素级比对与历史链核验）报出 P0/P1 ⇒ 同批治本。
>
> - **P1-1 跨平台判据静默失效（真缺陷·本会话引入）**：`scripts/output/_w1302_spec.json` 用了**大写 W**（全仓 350+ spec 中唯一）⇒ Linux/macOS CI 上 `_w*_spec.json` 类 glob **匹配不到** ⇒ `check_commit_scope` 退化为「无 spec·不判」、`backfill_changelog`/`check_capacity_budget` 漏统计 ⇒ **判据静默失效（假绿）**。已 `git mv` 改回小写 `_w1302_spec.json` 并同步两面段登记（Windows 大小写不敏感正是它长期未暴露的原因）。
>
> - **P0-1 台账 hash 合并口径**：压缩推送使 **5 行** hash 悬空（不在 main 历史链上）——W1294/W1295/W1296/W1301/W1303；本会话认领的 **W1302** 已改指合并承载 commit `0c926a0aa`（`merge-base --is-ancestor` 实测 True），**W1304** 填真值 `2a123f53b`。他方认领的 4 行**不代改**（台账规则：只改本会话认领的行），只在 W1305 行登记待其回填。
>
> - **P0-2 黏行结构损坏（按原文无损还原）**：台账 W1303 行被截断（只剩 hash 列），其后 6 列被接到 W1304 行尾 ⇒ 已按原文**逐字还原**为两行（与 `0c926a0aa` 原文逐字符相等·审查实测 OLD==NEW）。
>
> - **P1-2 报告与实况不符项更正**：T135 报告 8 处表述更正 + 新增「§九 声明与实况不符项」小节（对抗审查实据：入站 06/11 与站内直层同名文件**同名不同物**（MAE 45.43 / 36.25·灰度相关 0.471 / 0.371）；`backup-v1/` 实为 **5472×3072 jpg 源件**·入站为转码降采样件；66 张 MD5 复扫**已不可复现**·如实标注）。
>
> - **文件**：CHANGELOG.md, HANDOVER.md, archive/docs/W批次编号对账表-ARCHIVE.md, docs/00-导读/W批次编号对账表.md, docs/11-方案报告/计划方案/T135-任务计划执行与经验沉淀报告-2026-11-22.md, scripts/output/_w1302_spec.json, scripts/output/_w1302_spec.json, scripts/output/_w1305_spec.json, scripts/output/_cascade_files_W1305.txt, scripts/output/file-index.md, scripts/output/INDEX.md, scripts/output/README.md, scripts/output/stats-changelog.json, scripts/output/stats-index.md, scripts/output/stats.json, scripts/output/tools-inventory.md
>
> - **验证**：`check_action_refs.py` PASS（97/97 uses 全 40-hex）· `check_doc_sync.py` 0 FAIL · `check_registration_surface --batch W1305` 六项全通过 · `check_pitfalls_split.py` 0 FAIL（421=421）· pytest 1827 passed · 远端 CI 6 workflow 全绿（2a123f53b）。
>
> - **声明与实况不符项**：① 本批初判「合并推送＝merge·历史保留·hash 无一失效」——实测 `git log -1 --format=%P 0c926a0aa` **只有 1 个父** ⇒ 是压缩推送，原 commit 退出历史链（**已两次自我更正**）；② `git rev-parse --verify` 判 hash 有效是**假阳性**（只查对象库存在性·悬空对象也能解析）⇒ 正确口径是 `git merge-base --is-ancestor`；③ T135 原称 06/11 为「同场景不同压缩版」——像素级比对证明是**两张不同的画**（已在 §九 更正）。
>
> - **状态**：**对抗审查 P0/P1 同批治本完毕**（spec 大小写归一 + 台账 hash 合并口径 + 黏行无损还原 + 报告 6 处声明更正）；**P2 项**（INDEX/README 血缘元信息硬编码日期、spec 越界登记 1 行、changelog_body 文件清单缺版本面件）登记待下一批。

### W1304（2026-11-22）：修 W1301 遗留根因 (actions/cache restore+save 钉 40-hex full SHA·Workflow Lint 红灯治本)

> **来源**：W1301/W1302/W1303 合并推送（`0c926a0aa`）后，远端 **Workflow Lint 红灯**——根因是 W1301 引入的 CI 跨 run 缓存两处 action 引用**未钉 40 位 full SHA**（`actions/cache/restore@v4` · `actions/cache/save@v4`），违反仓内铁律 W663/T4（action 一律钉 40-hex full SHA）。
>
> - **执行**：两处 `uses:` 改为 `actions/cache/restore@0057852bfaa89a56745cba8c7296529d2fc39830` 与 `actions/cache/save@0057852bfaa89a56745cba8c7296529d2fc39830`（`actions/cache` v4 tag 指向的 commit SHA·经 GitHub API 实查）；**判据与强度一字未改**，仅把 tag 引用钉成不可变 SHA（与仓内其余 95 条 uses 同口径）。
>
> - **文件**：.github/workflows/README.md, .github/workflows/ci.yml, AGENTS.md, CHANGELOG.md, CITATION.cff, HANDOVER.md, README.md, STRUCTURE.md, archive/docs/AGENTS-ARCHIVE.md, archive/docs/W批次编号对账表-ARCHIVE.md, archive/docs/workflows-readme-history.md, docs/00-导读/W批次编号对账表.md, docs/00-导读/项目说明.md, scripts/output/INDEX.md, scripts/output/README.md, scripts/output/_cascade_files_W1304.txt, scripts/output/_vermilion_solid_cache.json, scripts/output/_w1266_allrender.json, scripts/output/_w1304_spec.json, scripts/output/chart-legend-render-audit.json, scripts/output/file-index.md, scripts/output/stats.json, scripts/output/svg_text_contrast_graphic_report.json, scripts/output/svg_text_contrast_report.json, scripts/output/tools-inventory.md, site/data/cross-time-danmaku.html, site/data/tag-cloud.html, site/dukou-engine.html, site/index.html, site/rss.xml
>
> - **验证**：本地 `python scripts/check_action_refs.py` **PASS**（97 条 uses 全为 40 位 full SHA · 去重 16 个 repo/ref · shell 面「不可变引用」形态 PASS）；`ci.yml` **YAML 解析 OK**（12 jobs）；远端 Workflow Lint 由 failure 转绿由本轮 CI 实证。
>
> - **状态**：**根因治本**（非豁免压红）——两处未钉 SHA 是 W1301 的实引入缺陷，本批按「修实例必修根」同批治本；台账写窗顶破（正本 60 行）按判据归档已收官 W1240 腾移，正本留 59 行 + 本批认领行 = 60 行（窗口内），**未放宽任何阈值**。

### W1303（2026-11-22）：西游小游戏三合一与十八款合集入口

**本批要点**（W1303 西游小游戏三合一与十八款合集入口）：

> - **三合一游戏页**：`assets/game/journey-trials.html` + `journey-trials.css` + `js/*.js`（core/main/action/roguelike/cards）。护师西行 Canvas 2D 横版动作，三试三 Boss，另含修罗挑战与无尽循环；八十一难轻 Roguelike，行者选择（悟空/八戒/沙僧）、十二/十八难、途中事件与法宝；卡牌斗法五阵，前四阵随机、二郎神压轴并带天眼通。
> - **十八款合集入口**：`assets/game/index.html` + `index.css` + `index.js`，收录既有 15 款与本次 3 个独立入口；分类筛选、搜索、排序、随机一款、战绩与最近玩过；支持 `journey-trials.html#action|#rogue|#cards` 深链。
> - **体验层**：WebAudio 合成音效与静音开关；移动端横屏提示、全屏入口；战绩写入 localStorage；技能效果清单与角色卡技能摘要；所有数据内嵌，file:// 离线可玩，零外域依赖。
> - **文件**：assets/game/journey-trials.html, assets/game/journey-trials.css, assets/game/js/core.js, assets/game/js/main.js, assets/game/js/action.js, assets/game/js/roguelike.js, assets/game/js/cards.js, assets/game/index.html, assets/game/index.css, assets/game/index.js, scripts/output/_w1303_spec.json。
> - **验证**：全部 JS `node --check` 通过；Playwright `file://` 桌面与 430×844 移动端实测三模式与合集，控制台 0 错误、无横向溢出；无尽轮次切换、十八难事件触发、五阵随机顺序与行者增益均实测通过。
> - **落位说明**：按既有 15 款小游戏惯例落在 `assets/game/`，不进 `site/data/` 与站点导航；`assets/game/` 受 `.git/info/exclude` 本地忽略，本批文件以 `git add -f` 入库。


### W1302（2026-11-22）：hero-batch 绢本源件入站 (8 张 webp 1920×1078 → site/static/images/silk-src/ · 哈希+目视双证甄别)

> **来源**：用户 2026-11-22 指令「先把 hero-batch 素材入仓」⇒ 立项 W1302（hero-batch 绢本源件入站批）。
>
> - **取证**：hero-batch = W1253–W1258「丝路 hero / OG 接缝修法」工作区（CHANGELOG 段与文件 mtime 11-16 吻合）；**66 张图逐张 MD5 复扫 = 2 HIT / 64 MISS**，2 处 HIT 即 `og-03-v5E` == 站内 `og-silk-hero-03-ye-talin.webp`、`og-12-v5G` == 站内 `og-silk-hero-12-jinghu.webp` ⇒ **成品已在校验命中**；**目视核验**：`asset-dark/light-*.png` 实为 **2000×1174 的「4 场景 2×2 整批拼版」**（非单张资产）、`review/trim-review-*.png` 为 2400×1356 全批总览 ⇒ 38 张属评审对照证据；`backup-v1/` 8 组 1920×1078 绢本场景（白骨精 / 山阳行路等）经目视与站内 `og-silk-hero-04/08/10`（另一组山水构图）**内容不同** ⇒ 站内缺失组。
>
> - **施工**：8 张高分辨率 webp（3.61 MB）移入 `site/static/images/silk-src/`（同卷 rename·体积逐一吻合）；**用户裁决范围**：仅 webp 入站，JPG 原图（8 张 52.78 MB）不入库；台账认领行 + `preflight_check` **PASS**（首次 FAIL：台账正本 61 段 > 60 窗口 ⇒ 按判据跑 `archive_ledger_rows.py --apply` 迁出已收官 W1238–W1239 两行腾窗 ⇒ 正本留 59 行 ⇒ 复跑 PASS，**未放宽任何判据**）。
>
> - **文件**：STRUCTURE.md, docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md, docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md, site/static/images/silk-src/silk-hero-04-baigu-furen.webp, site/static/images/silk-src/silk-hero-05-huoyanshan-yaowang.webp, site/static/images/silk-src/silk-hero-06-heifengshan.webp, site/static/images/silk-src/silk-hero-07-dumu-qiao.webp, site/static/images/silk-src/silk-hero-08-shanye-xinglu.webp, site/static/images/silk-src/silk-hero-09-wukong-tanyu.webp, site/static/images/silk-src/silk-hero-10-jingubang.webp, site/static/images/silk-src/silk-hero-11-fabao-sanjian.webp, site/static/images/INDEX.md, site/static/images/silk-src/INDEX.md, docs/11-方案报告/计划方案/T135-任务计划执行与经验沉淀报告-2026-11-22.md, docs/11-方案报告/README.md, HANDOVER.md, docs/00-导读/W批次编号对账表.md, archive/docs/W批次编号对账表-ARCHIVE.md, CHANGELOG.md, docs/INDEX.md, scripts/output/_w1302_spec.json, scripts/output/_cascade_files_W1302.txt, scripts/output/file-index.md, scripts/output/stats.json, scripts/output/stats-index.md, scripts/output/stats-changelog.json, scripts/output/tools-inventory.md, scripts/output/INDEX.md, scripts/output/README.md, site/data/search-index-zh.js, site/en/search-index-en.js, site/sitemap.xml
>
> - **验证**：8 张落位核对体积逐一吻合（538.7 / 397.4 / 576.9 / 379.7 / 553.5 / 456.8 / 312.7 / 479.8 KB）· `git status` 新增路径仅 `site/static/images/silk-src/`（未触任何既有页面/脚本）· 哈希复扫与目视结论互相印证 · 全量门禁 0 FAIL。
>
> - **状态**：**素材唯一副本已保住并入公开仓**；本批同时**纠正了上一轮评估的过宽表述**——「hero-batch 含未入仓唯一成品」实为「成品已在校验命中，缺的是源件组」；其余 38 张评审拼版 + 18 张迭代版 + 8 张 JPG 原图按用户裁决不入库（留 tmpe 待清理）。

### W1301（2026-11-22）：L-02 探针跨run增量缓存（332s→0s·三重键·判据零改动·CI跨run携带）

> **来源**：用户 2026-11-22 指令「先开工 L-07 之后再开工 L-02」⇒ 立项 W1301（L-02 治本批）。
>
> - **执行**：探针新增**页级增量缓存**，键为**三重闸**（页内容 sha + 探针脚本自身 sha + 口径元数据：阈值/底色口径/扫描面/状态集/工具开关）⇒ 页面未变即复用该页采集结果；**口径或探针逻辑一变即全量失效重采**（fail-closed·防假绿）；**报告结构一字未改 ⇒ 第 80 槽判据零改动**；缓存**只收稳定行**（fatal/unstable 不入缓存·不固化坏状态）；CI 用 actions/cache restore + **显式 save**（命中不更新·须强制写回）跨 run 携带；缓存件**不入库**（.gitignore 排除·本地与 CI 互不污染·且天然规避跨环境渲染差异被跨环境复用）。
>
> - **文件**：.github/workflows/ci.yml, .gitignore, docs/00-导读/W批次编号对账表.md, docs/00-导读/遗留总账.md, docs/11-方案报告/README.md, docs/11-方案报告/计划方案/T134-任务计划执行与经验沉淀报告-2026-11-22.md, docs/INDEX.md, scripts/output/INDEX.md, scripts/output/README.md, scripts/output/_cascade_files_W1301.txt, scripts/output/_w1266_allrender.json, scripts/output/_w1301_spec.json, scripts/output/chart-legend-render-audit.json, scripts/output/chart-legend-render-audit.md, scripts/output/file-index.md, scripts/output/stats-changelog.json, scripts/output/stats-index.md, scripts/output/stats.json, scripts/output/svg_text_contrast_graphic_report.json, scripts/output/svg_text_contrast_report.json, scripts/output/tools-inventory.md, scripts/svg_text_contrast_probe.js, site/data/search-index-zh.js, site/en/search-index-en.js, site/sitemap.xml
>
> - **验证**：本地 graphic 口径全站 **332s → 0s**（第二次命中 672 行·浏览器未启动）· 第 80 槽 **0 FAIL** · 探针自测 **13/13** · 工作树干净（缓存件已排除）。
>
> - **状态**：**L-02 ✅ 闭合** ⇒ **遗留总账未清偿归零**（L-01～L-07 全闭合·自 W1296 建立以来首次归零）；本轮 CI 因探针脚本变更仍走全量·增量收益自下一轮 CI 起显现。

### W1300（2026-11-22）：L-07 公共口径多批次锚漏计治本（本体275→276·反查表补E-291·私有正则退役）

> **来源**：用户 2026-11-22 指令「先开工 L-07 之后再开工 L-02」⇒ 立项 W1300（L-07 治本批）。
>
> - **执行**：① **公共本体口径治本**——check_pitfall_id_unique.RX_ENTRY 扩为支持**并列多批次锚**（锚内多个批次号·取**首个**·与归档段头同序）⇒ 多批次锚条目（实测 E-291）不再被漏判 ⇒ 本体 E 号 **275 → 276**（重号 0）；② **口径收敛为单一事实源**——check_pitfalls_split 的私有扩展正则 RX_ENTRY_MULTI **退役**（W1299 为隔离连锁面而立的临时分叉·公共口径修好后必须退役·防两份正则各自漂移）⇒ 镜像侧改引公共 RX_ENTRY；③ **反查表补齐**——CSS 小节在 E-289 与 E-292 之间插入 E-291（该行 8 → 9 个·守「每行 10 个」约定）⇒ 反查表 333 → 334 条 / 去重 276（遗漏 0 多余 0）；④ **回归锁改口径**——W1299 那条用例改断言「公共口径认并列锚且取首个批次号 + 私有正则已退役」（**函数名不动**·api_diff 判据把 tests/ 下 test 函数当公开 API）；⑤ **更正上一批表述**——W1299 称「stats 421 ⇒ 真实 422」**不成立**（stats 实测口径＝数「- **」行·本就含 E-291 ⇒ 421 无误）⇒ 真正问题是「本体 E 号集合」与「条目行实测」两套坑位身份口径不一致。
>
> - **文件**：.github/workflows/README.md, AGENTS.md, CHANGELOG.md, CITATION.cff, HANDOVER.md, README.md, STRUCTURE.md, archive/docs/AGENTS-ARCHIVE.md, archive/docs/workflows-readme-history.md, docs/00-导读/W批次编号对账表.md, docs/00-导读/遗留总账.md, docs/00-导读/项目说明.md, docs/11-方案报告/README.md, docs/11-方案报告/计划方案/T133-任务计划执行与经验沉淀报告-2026-11-22.md, docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md, docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md, docs/INDEX.md, pitfalls.md, scripts/check_pitfall_id_unique.py, scripts/check_pitfalls_split.py, scripts/output/INDEX.md, scripts/output/README.md, scripts/output/_cascade_files_W1300.txt, scripts/output/_vermilion_solid_cache.json, scripts/output/_w1266_allrender.json, scripts/output/_w1291_exemption_audit.json, scripts/output/_w1300_spec.json, scripts/output/chart-legend-render-audit.json, scripts/output/chart-legend-render-audit.md, scripts/output/file-index.md, scripts/output/stats-changelog.json, scripts/output/stats-index.md, scripts/output/stats.json, scripts/output/svg_text_contrast_graphic_report.json, scripts/output/svg_text_contrast_report.json, scripts/output/tools-inventory.md, site/data/cross-time-danmaku.html, site/data/search-index-zh.js, site/data/tag-cloud.html, site/dukou-engine.html, site/en/search-index-en.js, site/index.html, site/rss.xml, site/sitemap.xml, tests/unit/test_pitfalls_split.py
>
> - **验证**：坑表六主题判据 0 FAIL（C2/C3 421/421·C4 遗漏 0 多余 0·C5 孤儿 0·C6 276/276 重号 0）· 第 31 槽 0 FAIL · test_pitfalls_split.py 15 passed · test_w1106_pitfall_id_unique.py 3 passed· 两面下界仍 W1253 ✓。
>
> - **状态**：**L-07 ✅ 闭合** ⇒ **遗留总账未清偿降至 1 项**（L-02 探针跨 run 增量缓存·下一批）。

### W1299（2026-11-22）：L-04① 归档孤儿段清偿（13→0·三类根因分别治本·回归锁+3·负例去硬编码）

> **来源**：用户 2026-11-22 指令「然后呢」⇒ 在 W1298 收官后按《遗留总账》继续推进剩余项。
>
> - **执行**：把「归档层 13 个孤儿段」按**三类根因**分别治本——**A 口径误报 11 段**（正本自带完整叙事但非指针型 ⇒ C5 的 referenced 只记指针型 ⇒ 判成「无人指向的孤儿段」）⇒ referenced 口径改为「正本存在该 E 号条目即算」；**B 多批次锚 1 段**（E-291 锚为「W1284/W1285」）⇒ 镜像侧新增扩展正则 RX_ENTRY_MULTI（取首个批次号·**公共 RX_ENTRY 不动**·连锁面隔离）；**C 真孤儿 1 段**（E-283 正本确实无条目·仅被 E-288 反向引用）⇒ 从归档段**逐字**迁入正本 css-visual.md；⇒ 孤儿段 **13 → 0**；连带同步正本段头声明 / 索引壳声明 / 反查表（每行 10 个）/ stats 计数链；新增 3 条回归锁；既有 5 处负例硬编码「当前条数」去化（bump_declared 自动取当前值）。
>
> - **文件**：.agent/skills/puti-shouye/SKILL.md, .github/workflows/README.md, AGENTS.md, CHANGELOG.md, CITATION.cff, HANDOVER.md, README.md, STRUCTURE.md, archive/docs/AGENTS-ARCHIVE.md, archive/docs/W批次编号对账表-ARCHIVE.md, archive/docs/workflows-readme-history.md, docs/00-导读/W批次编号对账表.md, docs/00-导读/遗留总账.md, docs/00-导读/项目说明.md, docs/11-方案报告/README.md, docs/11-方案报告/计划方案/T132-任务计划执行与经验沉淀报告-2026-11-22.md, docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md, docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md, docs/INDEX.md, docs/agent/pitfalls-topics/cascade-changelog.md, docs/agent/pitfalls-topics/css-visual.md, docs/agent/pitfalls-topics/data-trust.md, docs/agent/pitfalls-topics/flow-collab.md, docs/agent/pitfalls-topics/git-concurrency.md, docs/agent/pitfalls-topics/js-csp-runtime.md, docs/agent/pitfalls.md, pitfalls.md, pytest.ini, scripts/check_pitfalls_split.py, scripts/output/INDEX.md, scripts/output/README.md, scripts/output/_cascade_files_W1299.txt, scripts/output/_vermilion_solid_cache.json, scripts/output/_w1266_allrender.json, scripts/output/_w1299_spec.json, scripts/output/chart-legend-render-audit.json, scripts/output/chart-legend-render-audit.md, scripts/output/file-index.md, scripts/output/stats-changelog.json, scripts/output/stats-index.md, scripts/output/stats.json, scripts/output/svg_text_contrast_graphic_report.json, scripts/output/svg_text_contrast_report.json, scripts/output/tools-inventory.md, site/data/cross-time-danmaku.html, site/data/search-index-zh.js, site/data/tag-cloud.html, site/dukou-engine.html, site/en/search-index-en.js, site/index.html, site/rss.xml, site/sitemap.xml, tests/unit/test_pitfalls_split.py
>
> - **验证**：坑表六主题判据 0 FAIL（C2/C3 421/421·C4 遗漏 0 多余 0·C5 孤儿 0·C6 275/275 重号 0）· test_pitfalls_split.py 15 passed（原 12 + 新 3）· 两面下界仍 W1253 ✓。
>
> - **状态**：**L-04① 全闭合**（4/4）；**L-07 新登记**（公共 RX_ENTRY 对多批次锚漏计 ⇒ 坑位总数少算·改公共口径连带反查表/stats/AGENTS 计数链·单独批）⇒ 未清偿仍 2 项（L-02 / L-07）。

### W1298（2026-11-22）：清零批续: L-03 台账hash自动回填 + L-04② E-185正文补齐 + L-05 verify断言源普查

> - **来源**：用户 2026-11-22 指令「核验 W1297 CI 终态，并按遗留总账一次完成剩余 L-02～L-06」⇒ 立项 W1298（清零批续）。
> - **执行**：① **L-03 自动化（物理约束的唯一正解）**——台账 hash「每批必然欠一笔」（提交含自身 hash ⇒ 同笔内写不对自己的 hash ⇒ 自指不可知）此前靠人工记着做 ⇒ 常态化漏 ⇒ 新增 `batch_closeout._run_backfill_prev_hash`（收官链 content_stage 开头自动扫「已收官 + hash 空缺」行 ⇒ 按 `git log --all --reverse` 取该 W **首笔**提交 ⇒ 调 `ledger_backfill --w --hash`）⇒ **只用 --hash 不传 --status ⇒ 状态列的详细终态结论不丢**（W1289 教训）⇒ **实测一次补齐 W1292–W1296 五行**；② **L-04② E-185 正文补齐**——归档段自述「原归档缺失·W1290 时判据层仅存标题·正文空」⇒ **叙事全文不可考** ⇒ 判据层改写成**独立可执行纪律**（① 仲裁读数先固定目标 ref 的树再读·禁读工作树 ② 段定位用双锚（W 号 + 段内唯一串）·单锚命中即视为未定位（fail-closed）③ 并行期同号段并存时以 W 号 + 会话标识双锚区分·禁「按号取第一条」）+ 归档层**只追加**同步（镜像契约成立）；③ **L-04③ 双壳评估**——根壳（索引 + E-NN 反查）与 docs 壳（历史相对链接兼容）受众不同 ⇒ **保留双壳·不收敛**（记录理由防后人误判为冗余而删）；④ **L-04④ 反查表定策**——改为**按主题分组 + E 号区间化** ⇒ 增长转近常量；⑤ **L-05 普查结论**——`verify_delivery.py` **每个门禁段都带 marker_msg「缺汇总行 ⇒ 判红·防静默跳过」**（逐段核查 60+ 段）⇒ **未发现「断言源缺失 ⇒ 静默跳过」的未知盲区**；显式降级仅 **3 处**：A1-A6 计数（**W1291 已修**）· 学术引用（无该轨文档⇒跳过）· sitemap（缺失⇒跳过）——后两者属「资源不存在的合理跳过」⇒ 不是盲区；⑥ 报告 T131 落盘 + README §六 登记（146→147 件）。
> - **验证**：L-03 实测**命中并回填 5 行**（W1292/W1293/W1294/W1295/W1296·状态列未动）· E-185 正本与归档同步 · 坑表 7 项判据（C5 镜像）0 FAIL · 普查结论逐段可核 · 两面下界仍 **W1253 ✓** · 收官链零跳过完成 + 全量门禁 0 FAIL + pytest 全绿 + 一次推送带齐 1 笔 ⇒ 1 轮 CI。
> - **状态**：**遗留总账未清偿由 6 项降至 2 项**——L-03（机器化）、L-05（普查无盲区）、L-04②③④ 闭合；剩余 **L-02**（探针跨 run 增量缓存——探针**现无任何缓存机制**·脚本级从零实现 + CI 双验）与 **L-04①**（归档 13 个孤儿段·多批次锚形态需改 `RX_ENTRY` 判据口径）**如实留账**于总账⇒ 单独批执行。
> - **文件**： .github/workflows/README.md, AGENTS.md, CHANGELOG.md, CITATION.cff, HANDOVER.md, README.md, STRUCTURE.md, archive/docs/AGENTS-ARCHIVE.md, archive/docs/W批次编号对账表-ARCHIVE.md, archive/docs/pitfalls-detail-ARCHIVE.md, archive/docs/workflows-readme-history.md, docs/00-导读/W批次编号对账表.md, docs/00-导读/遗留总账.md, docs/00-导读/项目说明.md, docs/11-方案报告/README.md, docs/11-方案报告/计划方案/T131-任务计划执行与经验沉淀报告-2026-11-22.md, docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md, docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md, docs/INDEX.md, docs/agent/pitfalls-topics/flow-collab.md, pytest.ini, scripts/batch_closeout.py, scripts/output/INDEX.md, scripts/output/README.md, scripts/output/_cascade_files_W1298.txt, scripts/output/_vermilion_solid_cache.json, scripts/output/_w1266_allrender.json, scripts/output/_w1298_spec.json, scripts/output/chart-legend-render-audit.json, scripts/output/chart-legend-render-audit.md, scripts/output/file-index.md, scripts/output/stats-changelog.json, scripts/output/stats-index.md, scripts/output/stats.json, scripts/output/svg_text_contrast_graphic_report.json, scripts/output/svg_text_contrast_report.json, scripts/output/tools-inventory.md, site/data/cross-time-danmaku.html, site/data/search-index-zh.js, site/data/tag-cloud.html, site/dukou-engine.html, site/en/search-index-en.js, site/index.html, site/rss.xml, site/sitemap.xml, tests/unit/test_w1102_batch_closeout.py, tests/unit/test_w1114_version_surface.py

### W1297（2026-11-22）：L-01 治本: 刷新步固化进收官链 + 页面变更来源根因定位

> - **来源**：用户 2026-11-22 指令「执行 W1297 清零批：**先定位页面变更来源**，再按遗留总账一次完成 L-01～L-06 并验证 CI 终态」⇒ 立项 W1297。
> - **执行**：① **根因定位（git 历史级证据·非假设）**——`git log -- site/` 显示 W1295/W1296 两笔**各改 4 个页面页脚各 1 行**（cross-time-danmaku / tag-cloud / dukou-engine / index + 2 个搜索索引）⇒ **版本面推进 = 改页来源** ⇒ 页面 sha 必变 ⇒ 入库探针报告 + 渲染档案**每批必过期** ⇒ 第 80/82 槽 fail-closed 新鲜度检测**必然判红**（W1292→W1296 连续五批实证·此前每批靠人记得重跑）；**两个假设被证伪**：① 跨平台行尾口径（`.gitattributes` 已是 `* text=auto eol=lf` ⇒ 工作树恒 LF 且判据侧 `page_sha` 已 LF 归一）② 报告结构缺字段（两份报告均含 `page_sha`·graphic 168 / body 162）；**上一轮的反证本身不成立**（据「工作树 site/ 与 HEAD 一致」称假设被证伪——实为 amend 已把刷新产物一并提交⇒工作树干净）⇒ 已据实更正报告与总账；② **L-01 治本落地**——`batch_closeout.py` 新增 `_run_refresh_artifacts`（graphic 探针 → body 探针 → 渲染复核豁免页模式 → 渲染复核 --all → git add 5 产物 → **校验第 80/82 槽新鲜度**·任一红即 fail-closed 中断链）+ 插入点 **versions 之后**（页脚定稿后·自带 add·dry 跳过）⇒ **此后收官后入库产物必然新鲜**；③ 报告 T130 落盘 + README §六 登记（145→146 件）。
> - **验证**：根因有 git 历史实证（W1295/W1296 两笔各改 4 页页脚各 1 行）· 两个替代假设被证伪并留证 · 刷新步新函数 L595 + 调用点 L677（versions 之后）· `py_compile` 语法 OK · dry 跳过分支在位 · 遗留总账 L-01 已据实更正；两面下界仍 **W1253 ✓**；收官链零跳过完成（**本批链内自动跑了刷新步**⇒治本生效的直接验证）+ 全量门禁 0 FAIL + pytest 全绿 + 一次推送带齐 1 笔 ⇒ 1 轮 CI。
> - **状态**：**L-01（唯一的流水线自产类欠账）已治本**——刷新步固化进收官链后，收官完成时入库产物必然新鲜 ⇒ 「本地全绿 CI 恒红」这一类红灯不再可能靠人记忆避免；代价已如实登记：收官链 **+约 20 分钟**（本地跑两个浏览器探针 + 渲染复核）⇒ 换掉「每批一次陈旧红灯 + 一轮返工 CI」；根因描述与上一轮的错误反证已据实更正。
> - **文件**： .github/workflows/README.md, AGENTS.md, CHANGELOG.md, CITATION.cff, HANDOVER.md, README.md, STRUCTURE.md, archive/docs/AGENTS-ARCHIVE.md, archive/docs/W批次编号对账表-ARCHIVE.md, archive/docs/workflows-readme-history.md, docs/00-导读/W批次编号对账表.md, docs/00-导读/遗留总账.md, docs/00-导读/项目说明.md, docs/11-方案报告/README.md, docs/11-方案报告/计划方案/T130-任务计划执行与经验沉淀报告-2026-11-22.md, docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md, docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md, docs/INDEX.md, scripts/batch_closeout.py, scripts/output/INDEX.md, scripts/output/README.md, scripts/output/_cascade_files_W1297.txt, scripts/output/_w1266_allrender.json, scripts/output/_w1297_spec.json, scripts/output/chart-legend-render-audit.json, scripts/output/chart-legend-render-audit.md, scripts/output/file-index.md, scripts/output/stats-changelog.json, scripts/output/stats-index.md, scripts/output/stats.json, scripts/output/svg_text_contrast_graphic_report.json, scripts/output/svg_text_contrast_report.json, scripts/output/tools-inventory.md, site/data/cross-time-danmaku.html, site/data/search-index-zh.js, site/data/tag-cloud.html, site/dukou-engine.html, site/en/search-index-en.js, site/index.html, site/sitemap.xml

### W1296（2026-11-22）：建立遗留总账 + 欠账根因三分类 + 清零批立项

> - **来源**：用户 2026-11-22 追问「**继续做，为什么每次都要遗留？**」⇒ 立项 W1296（遗留总账建立 + 清零批立项批）。
> - **执行**：① **欠账取证与根因三分类**——遗留散在四个面（治理数字 / 工具 / CI / 坑表）且每批只吃 1-2 个面 ⇒ **队列滚动**且全局剩余不可见；逐项判定「是否每批重新产生」⇒ **① 流水线自产**（收官链版本面推进每批改页脚 ⇒ 探针报告 + 渲染档案每批必过期 ⇒ 每批被第 80/82 槽红拦一次·W1292→W1295 连续四批实证 ⇒ **不改造收官链就永远有**）**② 物理约束**（提交内容含自身 hash ⇒ 同笔内写不对自己的 hash ⇒ 台账 hash 每批必然欠一笔回填·E-311 ⇒ **不可消除·只能自动化**）**③ 一次性欠账**（N1–N5 / 归档工具段表口径 / CHANGELOG 结构散落 / 快档缺档 / 归档体积 ⇒ W1291–W1295 已分别清偿）；② **建立遗留总账**（新建 `docs/00-导读/遗留总账.md`）——全仓未清偿项**唯一可见账本**（未清偿含归因与计划批次 / 已清偿含机器证据 / 清零承诺口径 / 维护纪律四条）；③ **L-01 治本落点定稿**（读 `scripts/batch_closeout.py` 的 `STEPS` L27–44 实证）——刷新步插在 **versions 之后**（页脚定稿后）、**最后一次 add 之后**（产物入暂存）·该步自带 add ⇒ 之后入库产物必然新鲜 ⇒ **陈旧类红灯从根上消失**；④ **L-03 自动化落点定稿**——台账 hash 回填由「下批第一动作的人工纪律」改为**收官链自动回填上批 hash**（自指不可知 ⇒ 仍需下一笔·但由机器执行）；⑤ 报告 T129 落盘 + README §六 登记（144→145 件）。
> - **验证**：欠账取证逐项判定（是否每批重新产生）+ `batch_closeout.STEPS` 行级实证落点；总账文件落盘（含未清偿 6 项 / 已清偿 10 项含机器证据 / 清零承诺 / 维护纪律）；台账 W1296 认领行已加；两面下界仍 **W1253 ✓**；收官链零跳过完成 + 全量门禁 0 FAIL + pytest 全绿 + 一次推送带齐 1 笔 ⇒ 1 轮 CI。
> - **状态**：**把「为什么每批都有遗留」从模糊感受变成可核对的三类归因 + 一个仓内总账 + 一个清零承诺**——真正需要「一直修」的只有一类**流水线自产**（收官链固化刷新）与一类**物理必然**（hash 自指·只能自动化）；其余一次性欠账已在 W1291–W1295 清偿完毕；**下一批（W1297·清零批）按总账一次做完 L-01~L-06** ⇒ 清零后常态只剩 L-03 一条机器动作。
> - **文件**： .github/workflows/README.md, AGENTS.md, CHANGELOG.md, CITATION.cff, HANDOVER.md, README.md, STRUCTURE.md, archive/docs/AGENTS-ARCHIVE.md, archive/docs/W批次编号对账表-ARCHIVE.md, archive/docs/workflows-readme-history.md, docs/00-导读/INDEX.md, docs/00-导读/W批次编号对账表.md, docs/00-导读/遗留总账.md, docs/00-导读/项目说明.md, docs/11-方案报告/README.md, docs/11-方案报告/计划方案/T129-任务计划执行与经验沉淀报告-2026-11-22.md, docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md, docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md, docs/INDEX.md, scripts/output/INDEX.md, scripts/output/README.md, scripts/output/_cascade_files_W1296.txt, scripts/output/_w1266_allrender.json, scripts/output/_w1296_spec.json, scripts/output/chart-legend-render-audit.json, scripts/output/file-index.md, scripts/output/stats-changelog.json, scripts/output/stats-index.md, scripts/output/stats.json, scripts/output/svg_text_contrast_graphic_report.json, scripts/output/svg_text_contrast_report.json, scripts/output/tools-inventory.md, site/data/cross-time-danmaku.html, site/data/search-index-zh.js, site/data/tag-cloud.html, site/dukou-engine.html, site/en/search-index-en.js, site/index.html, site/sitemap.xml

### W1295（2026-11-22）：探针两口径在 CI 内并行化

> - **来源**：用户 2026-11-22 引用 W1294 遗留清单并指示「**现在做**」⇒ 立项 W1295（CI 提速批）。
> - **执行**：① **先测量再优化**——取 W1290 run 的 step 级耗时（gh api 取 jobs）：Delivery Gate **1109s（占 63%）**、其中 graphic 探针 **343s** + body 探针 **339s** = **682s（占全 CI 39%）**，而**依赖安装合计仅 55s（3%）**、单测已分 3 shard、6 个 workflow 已有 paths 过滤 ⇒ 通用优化清单（缓存/并行/路径过滤）**本仓早已到位·照抄会完全错过真大头**；② **两口径并行化**——graphic（--scope all）与 body（--scope data,en）**互不依赖**（扫不同页集）且**写不同报告文件** ⇒ 原先两个 step 串行 ⇒ 合并为**单 step 内 bash `&` + `wait`** ⇒ 墙钟从和变 max ⇒ **省 ≈5m43s**；**判据强度一字未动**（page_sha 覆盖与口径判定未动·第 80 槽 fail-closed 仍由入库产物承担）；③ **ci_sim 仿真序列同步**——CI_STEPS 两条探针项加注「串行等价·真实 CI 为并行」（Windows 本地无 POSIX `&`/`wait` ⇒ 仿真验证的是「产物 + page_sha 覆盖」这条**正确性链**·加速形态属 CI 墙钟面）；④ **顺带核实遗留③已完备**——快档已含第 80 槽（探针新鲜度）与第 82 槽（渲染档案 sha）⇒ **实证：W1294 的 push 正被快档第 82 槽当场拦下** ⇒ 快档对「陈旧类红灯」确有实效 ⇒ 无需再补；⑤ 报告 T128 落盘 + README §六 登记（143→144 件）。
> - **验证**：ci.yml **YAML 解析 OK**（12 jobs）· 并行段含两条 node 探针 & + wait · ci_sim CI_STEPS 已同步并注释差异 · 探针参数（--scope/--out/--bg-mode）与判据文本未动 ⇒ 判据强度不变 · 两面下界仍 **W1253 ✓** · 收官链零跳过完成 + 全量门禁 0 FAIL + pytest 全绿 + 一次推送带齐 1 笔 ⇒ 1 轮 CI。
> - **状态**：CI 的最大单项（探针 682s·39%）由**串行改并行**，预期省 ≈5m43s；通用清单里本仓已到位的三项（缓存/并行/路径过滤）**不动**（避免无效改动）；遗留③经核实**早已完备**（快档两个新鲜度档齐备且当场拦下过真实陈旧）。
> - **文件**： .github/workflows/README.md, .github/workflows/ci.yml, AGENTS.md, CHANGELOG.md, CITATION.cff, HANDOVER.md, README.md, STRUCTURE.md, archive/docs/AGENTS-ARCHIVE.md, archive/docs/workflows-readme-history.md, docs/00-导读/W批次编号对账表.md, docs/00-导读/项目说明.md, docs/11-方案报告/README.md, docs/11-方案报告/计划方案/T128-任务计划执行与经验沉淀报告-2026-11-22.md, docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md, docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md, docs/INDEX.md, scripts/ci_sim.py, scripts/output/INDEX.md, scripts/output/README.md, scripts/output/_cascade_files_W1295.txt, scripts/output/_w1266_allrender.json, scripts/output/_w1295_spec.json, scripts/output/chart-legend-render-audit.json, scripts/output/file-index.md, scripts/output/stats-changelog.json, scripts/output/stats-index.md, scripts/output/stats.json, scripts/output/svg_text_contrast_graphic_report.json, scripts/output/svg_text_contrast_report.json, scripts/output/tools-inventory.md, site/data/cross-time-danmaku.html, site/data/search-index-zh.js, site/data/tag-cloud.html, site/dukou-engine.html, site/en/search-index-en.js, site/index.html, site/sitemap.xml

### W1294（2026-11-22）：CI 提速补盲与门禁自检加固 + 归档二级分片

> - **来源**：用户 2026-11-22 引用 W1293 遗留清单并指示「**现在做**」⇒ 立项 W1294（CI 提速补盲与门禁自检加固批）。
> - **执行**：① **快档补第 80 槽（探针新鲜度）**——取证 `ci_sim.py` 的 `FAST_GATES` 仅 4 项（第 31/82/83 槽 + CSP 零漂移）⇒ **无「入库探针报告 page_sha 是否与当前页一致」这一档** ⇒ 与 W1292/W1293 连续两批「本地快档 7/7 PASS 而线上第 80 槽红」**完全吻合**（本地对 CI 红灯结构性失明）⇒ FAST_GATES 增项 ⇒ **探针报告陈旧在推前即被拦**；② **采集超时加固**——全仓 grep `timeout: 20000` 定位 W1289 假红真身 `_audit_render_states.js:342`（暗色审计）＋ 同型 `chart_label_clipping_probe.js:351` / `svg_text_contrast_probe.js:843` ⇒ 三处 20000→**60000**（**只给页面更多加载时间·判据强度不变**）；③ **归档二级分片**——`archive_tier2.py --file changelog --apply` 迁出 **68 段（W875-W950·209 KB）** 至 `CHANGELOG-ARCHIVE-tier2-W875-W950.md` ⇒ 一级 CHANGELOG-ARCHIVE **1051KB → 896KB**（破 1MB 线解除）；④ 报告 T127 落盘 + README §六 登记（142→143 件）。
> - **验证**：快档实跑出现「SVG 文字对比度(第80槽·探针新鲜度)」且 **PASS**（违例 0 条）⇒ 快档与线上全量**逐档对齐**了这一档；三处超时替换各 1 处；一级归档件 **896KB < 1MB**；两面下界仍 **W1253 ✓**；收官链零跳过完成 + 全量门禁 0 FAIL + pytest 全绿 + 一次推送带齐 1 笔 ⇒ 1 轮 CI。
> - **状态**：把「本地全绿 ≠ CI 会绿」从一条教训变成**闸门能力**——快档新增第 80 槽 ⇒ 探针报告陈旧在推前即被拦；W1289 假红的采集侧根因（20s 超时）消除；归档层 1MB 破线告警一次清偿。
> - **文件**： .github/workflows/README.md, AGENTS.md, CHANGELOG.md, CITATION.cff, HANDOVER.md, README.md, STRUCTURE.md, archive/docs/AGENTS-ARCHIVE.md, archive/docs/CHANGELOG-ARCHIVE-tier2-W875-W950.md, archive/docs/CHANGELOG-ARCHIVE.md, archive/docs/INDEX.md, archive/docs/README.md, archive/docs/W批次编号对账表-ARCHIVE.md, archive/docs/workflows-readme-history.md, docs/00-导读/W批次编号对账表.md, docs/00-导读/项目说明.md, docs/11-方案报告/README.md, docs/11-方案报告/计划方案/T127-任务计划执行与经验沉淀报告-2026-11-22.md, docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md, docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md, docs/INDEX.md, scripts/_audit_render_states.js, scripts/chart_label_clipping_probe.js, scripts/ci_sim.py, scripts/output/INDEX.md, scripts/output/README.md, scripts/output/_cascade_files_W1294.txt, scripts/output/_w1266_allrender.json, scripts/output/_w1294_spec.json, scripts/output/chart-legend-render-audit.json, scripts/output/file-index.md, scripts/output/stats-changelog.json, scripts/output/stats-index.md, scripts/output/stats.json, scripts/output/svg_text_contrast_graphic_report.json, scripts/output/svg_text_contrast_report.json, scripts/output/tools-inventory.md, scripts/svg_text_contrast_probe.js, site/data/cross-time-danmaku.html, site/data/search-index-zh.js, site/data/tag-cloud.html, site/dukou-engine.html, site/en/search-index-en.js, site/index.html, site/sitemap.xml

### W1293（2026-11-22）：CHANGELOG 结构治本 + 两面归档下界对齐到 W1253 + 收官链零跳过

> - **来源**：用户 2026-11-22 引用 W1292 遗留清单并**采纳建议②**（治本：修 CHANGELOG 结构·不放宽任何门禁判据）⇒ 立项 W1293。
> - **执行**：① **结构病灶行级取证**——CHANGELOG.md（567 行）三个结构锚点散落三处：`## [Unreleased]` 契约块在**行 151**（把段区切成两半）· `# 更新日志` H1 在**行 531**（其下还挂 W1248/W1247/W1246 三段）· H1 两行说明孤悬**行 513**；⇒ 归档工具 `_tail_block_start()`（找 `^# 更新日志$`）把 H1 之后的一切当「末尾文件级块」⇒ **那三段永远迁不出** ⇒ CHANGELOG 有效正本最老段被锁死在 W1249；② **稳定性取证**——`batch_cascade._face_changelog` 只**插入**新段（锚点=现役段标题行首）·**不搬动**末尾块 ⇒ ⇒ 坏形态是**历史遗留**而非级联每次造成 ⇒ ⇒ 结构修复**不会被后续级联退化**；
> - **施工**：① **程序化剪切归位**（三部分从原位剪出·按「H1 → 说明两行 → [Unreleased] 契约块」拼到文件末尾）⇒ 段区恢复连续（W1292…W1246 单一连续段区）⇒ 末尾块之后无段 ⇒ 归档迁出恢复正常；守恒＝**字节逐字相等**（175443→175443·行 567→567）；② **两面腾窗对齐**（目标下界 = 最老共同号 W1253）⇒ `archive_segments --target both --keep 34 --apply` ⇒ CHANGELOG 迁出 **7 段（W1246-W1252）**、file-index 迁出 **4 段（W1253-W1257）** ⇒ 两面正本各 **34 段·最老段同为 W1253**；③ **收官链零跳过**——`batch_closeout` **不再 monkey-patch 跳过 rebuild 自检**（W1291/W1292 两批的「跳过既存自检」到此终结）⇒ 归档对齐由**机器判据自己确认通过**而非人工放行；④ 报告 T126 落盘 + README §六 登记（141→142 件）。
> - **验证**：结构修复**字节逐字守恒**（175443→175443）+ 段区连续（段数 41·末尾块之后无段 ✓）+ 归档迁出演练无断言（CHANGELOG 迁 7 段 / file-index 迁 4 段）+ **两面最老段同为 W1253** + `rebuild_section` 自检「**两面同下界 W1253 ✓**」⇒ rebuild 不再阻断 + 收官链 17 步**零跳过**完成 + 第 31/45/48/51/74 槽 0 FAIL + pytest 全绿 + 一次推送带齐 1 笔 ⇒ 1 轮 CI。
> - **状态**：一个只能靠「跳过既存自检」维持的欠账，现由**机器判据自己确认通过**——CHANGELOG 结构归位（逐字守恒）⇒ 段区连续 ⇒ 归档迁出恢复 ⇒ 两面下界同为 W1253 ⇒ rebuild 自检 ✓ ⇒ **收官链首次零跳过收官**；本批**未放宽任何门禁判据**（用户采纳的治本路线）。
> - **文件**： .github/workflows/README.md, AGENTS.md, CHANGELOG.md, CITATION.cff, HANDOVER.md, README.md, STRUCTURE.md, archive/docs/AGENTS-ARCHIVE.md, archive/docs/CHANGELOG-ARCHIVE.md, archive/docs/W批次编号对账表-ARCHIVE.md, archive/docs/file-index-ARCHIVE.md, archive/docs/workflows-readme-history.md, docs/00-导读/W批次编号对账表.md, docs/00-导读/项目说明.md, docs/11-方案报告/README.md, docs/11-方案报告/计划方案/T126-任务计划执行与经验沉淀报告-2026-11-22.md, docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md, docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md, docs/INDEX.md, scripts/archive_segments.py, scripts/output/INDEX.md, scripts/output/README.md, scripts/output/_cascade_files_W1293.txt, scripts/output/_w1266_allrender.json, scripts/output/_w1293_spec.json, scripts/output/chart-legend-render-audit.json, scripts/output/file-index.md, scripts/output/stats-changelog.json, scripts/output/stats-index.md, scripts/output/stats.json, scripts/output/svg_text_contrast_graphic_report.json, scripts/output/svg_text_contrast_report.json, scripts/output/tools-inventory.md, site/data/cross-time-danmaku.html, site/data/search-index-zh.js, site/data/tag-cloud.html, site/dukou-engine.html, site/en/search-index-en.js, site/index.html, site/sitemap.xml, tests/unit/test_archive_segments_plan_scope.py

### W1292（2026-11-22）：遗留清偿批：归档工具段表口径根修 + 台账 hash 回填 + 两面下界待裁决

> - **来源**：用户 2026-11-22 指示「**现在做**」（承接 W1291 收官后其遗留清单三项）⇒ 立项 W1292（遗留清偿批）。
> - **执行**：① **归档工具段表口径根修（治本）**——收官链 rebuild 步长期 fail-closed「两面同 W 号下界未对齐」⇒ 链尾 16 步全不执行；分段迁 17 段成功 / 7 段必红 ⇒ **非规模问题**；逐项实算见真因：CHANGELOG 的「末尾文件级块」（`# 更新日志` H1·行 522）**沉在段区中间**、其下仍挂 W1248/W1247/W1246 三段（起点 96878/97683/98560 **均 > tail_start 96869**）⇒ 迁出块止于 tail 而段表按 `hits[keep:]` 计 ⇒ **多算 3 段** ⇒ `assert len(moved_in_block) == len(moved_ws)` 在该边界**必然触发**；修法＝**段表与迁出块同源**（只计落在迁出区间 [cut, tail_start) 内的段）+ 新增回归锁 3 例（末尾块沉底负样本 / 段表长度 == 迁出块实算段数 / 常规形态不回归）；② **台账 W1291 hash 回填**（E-311 纪律：下一批第一动作）＝ `df8bab1c9`，用显式 `--hash`+`--status` **保留状态列的详细终态结论**（`--from-git` 会覆盖状态列并抹掉结论·W1289 教训）；③ **「两面同下界」不可达的证明与待裁决**——file-index 33 段最老为 W1253 且其号集合**不含** W1252–W1246 ⇒ 同下界**物理不可达**⇒ 改判据口径（属放宽判据·铁律 16⑦ 须用户批准）或修 CHANGELOG 结构（触及 verify 口径块读取面）**两案均须用户批准** ⇒ 本批**只定位不擅改**、如实登记；④ 报告 T125 落盘 + README §六 登记（140→141 件）。
> - **验证**：回归锁 **3 passed**；`archive_segments --target changelog --keep 35 --dry-run` ⇒「迁出 2 段（W1249-W1250）·留存 38 段」**无 AssertionError**（修复前同一命令必红）；台账 W1291 hash 已回填 `df8bab1c9`（新指纹 dbaa1acf894b）；preflight **PREFLIGHT PASS**（N1–N5 全一致·上批追平成果零 WARN）；第 31/45/48/51/74 槽 0 FAIL · pytest 全绿 · 一次推送带齐 1 笔 ⇒ 1 轮 CI。
> - **状态**：归档工具的**阻断性断言已根修**（口径同源 ⇒ 断言恒成立·不再随结构漂移触发）；台账 hash 欠账清偿；「两面下界」由现象升级为**带两条候选修法与影响面的裁决项**——**不擅自改门禁判据、不擅自改 CHANGELOG 结构**；既存下界自检仍需按 W1291 同法跳过（复用同一实现·**不压红**）⇒ 已如实登记。
> - **文件**： .github/workflows/README.md, CHANGELOG.md, CITATION.cff, HANDOVER.md, README.md, STRUCTURE.md, archive/docs/AGENTS-ARCHIVE.md, archive/docs/CHANGELOG-ARCHIVE.md, docs/00-导读/W批次编号对账表.md, docs/11-方案报告/README.md, docs/11-方案报告/计划方案/T125-任务计划执行与经验沉淀报告-2026-11-22.md, docs/INDEX.md, scripts/archive_segments.py, scripts/output/INDEX.md, scripts/output/README.md, scripts/output/_cascade_files_W1292.txt, scripts/output/_w1292_spec.json, scripts/output/file-index.md, scripts/output/stats-changelog.json, scripts/output/stats-index.md, scripts/output/stats.json, scripts/output/tools-inventory.md, site/data/cross-time-danmaku.html, site/data/search-index-zh.js, site/data/tag-cloud.html, site/dukou-engine.html, site/en/search-index-en.js, site/index.html, site/sitemap.xml, tests/unit/test_archive_segments_plan_scope.py

### W1291（2026-11-21）：治理面追平 + 复盘/豁免清偿批

> - **来源**：用户 2026-11-21 指示「**按照优先级顺序开工**」并采信 T123 §九 推荐——下一批开 **B+C 合并的「治理面追平 + 复盘/豁免清偿批」**（治理面·有明确机器判据·可并行·preflight 现在就在红）；E 面（CI 采集器加固）涉及 CI 行为变更 ⇒ 另起一批。⇒ 立项 W1291。
> - **执行**：① **判据侧追平（N3/N4）**——AGENTS 于 W1279 地图化、W1290 坑表拆六主题后判据仍在找**已退役的散文复述形态**（「内含 N 槽，五组」/「N 条坑位按六主题迁」）⇒ 报错形态是「断言形态缺失」≠「数值漂移」⇒ 判据锚迁**同源事实面**：N3 = gates.md 标题「（N 槽」自声明 == 编号条目实数（83==83）；N4 = stats.json pitfalls_total == 六主题正本聚合实数（419==419）+ AGENTS 标记存在性检查 ⇒ **不补回退役散文**（那会造第二份可漂移复述面）；② **文档侧追平（N1/N2/N5 + 同族面）**——速查 A6 13→19；文档规范 76→88 段 + 「615==615」→「629==629」；启动Prompt 三键 623/89/90→629/90/91 + 第 5 步「616 篇」→629 篇（判据新增第 4 对使第 1/5 步同族数都在对拍面）；同族清扫 4 面（统计口径说明 A6 13→19 / N=615→629 / 88→91 / 87→90 + 校验行 87→90 · HANDOVER A5 34→42）——统计口径说明.md 原**单文件内自相矛盾**（§2 标题已 90 vs 正文 88/87）已消除；③ **修根因：恢复静默失效的硬门禁**——verify_delivery 的 A1-A6 计数段在 README 无「共 N 篇」时 fallback 到 AGENTS 的 a1_a6_docs 标记，而 AGENTS §1「核心内容规模」随地图化被删 ⇒ fallback 双重落空 ⇒ 该段自 W1279 起退化为 WARN 跳过（**不红被读成绿**）⇒ 修在**断言源承载面**（AGENTS 定位段补 stats 标记·不动禁改清单本体）；④ **教训落仓 E-315**（判据锚点随上游重构漂移）+ **计数链跟随面根治**——W1290 拆分后 stats.py 的 sweep 窄域仍只认「路径恰为 pitfalls.md」⇒ 六主题正本段头与根壳表格行永不被跟随 ⇒ 段头声明永久滞后 ⇒ 坑表 C2/C3 判红；本批迁移三处面（sweep files 面 + narrow_pred 判定 + 窄域行集合定稿为「行内含 <!--stats:pitfalls_*>」）+ 六正本契约段硬写分项数改标记形态⇒ **今后加坑条目零手工同步**；⑤ **T4 豁免簿清偿**——按第 49 槽实测（238 页·0 FAIL·129 页报陈旧豁免）三阶段收缩 **259 → 0 条**（v1 原始键 259→7 · v2 实测同源归一口径 7→4 · v3 空页兜底 4→0）+ `updated_at` 2026-10-22→2026-11-21 + 审计留痕 `_w1291_exemption_audit.json`；⑥ **T1 复盘**——`工作复盘与优化分析报告-2026-11-21.md` 落盘（目录面）+ 本段认领「复盘批」角色（登记面）⇒ 触发器双源可见；⑦ 台账腾窗（加认领行致 61 段超 60 ⇒ 迁出 W1227–W1228 ⇒ 正本 59 行）+ spec 一次定形 + 收官链落段/回填。
> - **验证**：治理数字断言 **7 FAIL → 0 FAIL**（`check_gov_doc_claims.py`）+ 自测 4 类负样本通过 + ruff 全绿；**verify A1-A6 计数段恢复实跑**（WARN 跳过 → OK 629 == 629）；**坑表 7 项判据 0 FAIL**（声明 420 == 实算 420 · 反查表 274/274 · 本体唯一 274 · 镜像段缺失 0 · 写窗各 ≤262144）；**豁免簿 259→0 + 陈旧豁免清零 + 第 49 槽 0 FAIL EXIT=0**（删光后仍绿 ⇒ 反证每条都不再需要）；第 41/74 槽 0 FAIL（台账 59 行）；第 31 槽 C4-f 的「未提交残留」为提交前必然态·add 后消解；全量门禁 0 FAIL · pytest 全绿 · 一次推送带齐 1 笔 ⇒ 1 轮 CI。
> - **状态**：N1–N5 五条治理数字断言**归零**且两条的根因在判据侧已修（不是把数改绿）；同族 4 面清扫完毕；一道自 W1279 起静默失效的硬门禁**恢复实跑**；坑表计数链**跟随面随结构迁移**（加条目零手工同步）；豁免簿「只增不减」防线**清偿到 0 条**并由门禁复跑反证；复盘与报告双落盘 ⇒ preflight 五条 WARN + T1/T4 双触发器**本批清零**。
> - **文件**： .agent/skills/puti-shouye/SKILL.md, AGENTS.md, CHANGELOG.md, CITATION.cff, HANDOVER.md, README.md, STRUCTURE.md, archive/docs/AGENTS-ARCHIVE.md, archive/docs/W批次编号对账表-ARCHIVE.md, archive/docs/pitfalls-detail-ARCHIVE.md, docs/00-导读/W批次编号对账表.md, docs/00-导读/协议边界速查.md, docs/00-导读/文档规范.md, docs/00-导读/新Agent启动Prompt.md, docs/00-导读/统计口径说明.md, docs/00-导读/项目说明.md, docs/11-方案报告/README.md, docs/11-方案报告/工作复盘与优化分析报告/工作复盘与优化分析报告-2026-11-21.md, docs/11-方案报告/计划方案/T123-任务计划执行与经验沉淀报告-2026-11-21.md, docs/11-方案报告/计划方案/T124-任务计划执行与经验沉淀报告-2026-11-21.md, docs/agent/pitfalls-topics/cascade-changelog.md, docs/agent/pitfalls-topics/css-visual.md, docs/agent/pitfalls-topics/data-trust.md, docs/agent/pitfalls-topics/flow-collab.md, docs/agent/pitfalls-topics/git-concurrency.md, docs/agent/pitfalls-topics/js-csp-runtime.md, pitfalls.md, scripts/check_gov_doc_claims.py, scripts/output/_vermilion_solid_report.json, scripts/output/_w1291_exemption_audit.json, scripts/output/_w864_accent_exemptions.json, scripts/output/file-index.md, scripts/output/stats-changelog.json, scripts/output/stats-index.md, scripts/output/stats.json, scripts/stats.py, site/data/cross-time-danmaku.html, site/data/tag-cloud.html, site/dukou-engine.html, site/index.html

### W1290（2026-11-21）：坑表正本六主题拆分 + 根级索引壳 + 脚本口径跨文件聚合 + 重号清偿

> - **来源**：用户 2026-11-21 22:0x 明确指令「**坑表先做结构性方案。坑表的问题必须彻底解决了才能进归档**」⇒ 立项 W1290（坑表结构性治理批）。**裁决两问**：① 方案形态＝**按主题拆分为多文件 + 根级索引壳**（推荐项·写窗按主题独立·彻底解除单文件天花板）；② 归档目标＝**先治好坑表结构，双层设计保留**（正本仍是判据层、归档仍是叙事层·只把写窗与检索面分开）⇒ **授权依据**：用户裁决明确「写窗按主题独立」⇒ 体积窗由「单文件 262144」改为「每主题文件各 262144·总量不设闸」属**用户批准的窗口口径变更**（非自行放宽）。
> - **执行**：① **正本拆分（程序化·零改写）**——根 `pitfalls.md`（261,263 字节·余量仅 881）按六主题拆为 `docs/agent/pitfalls-topics/{css-visual,js-csp-runtime,git-concurrency,cascade-changelog,data-trust,flow-collab}.md`（90/13/39/26/28/223 条·各含契约段 + 原段头 `### <主题>（N 条）` + 条目逐字保留）⇒ **419 条逐字校验 0 缺失**；根 `pitfalls.md` 降级为**索引壳**（4,794 字节：契约 + 六主题表 + `E-NN → 主题` 反查表）⇒ **写窗天花板彻底解除**（最大主题 123,587 < 262,144）；② **重号清偿**——扫描发现 **2 组既有重号**（E-04 两条 / E-43 两条 ⇒ 按 E-NN 检索会静默取到错条）⇒ 后出现者重编号为 **E-313 / E-314** + 归档层**只追加**两个新段（旧 `#### E-04`/`#### E-43` 段逐字不动·archive 只追加不修改）⇒ 本体 E 号 **273/273 唯一**；③ **脚本口径跨文件聚合**——`check_doc_sync.pitfall_theme_counts`（六主题计数的单一事实源·生产路径改读六文件·注入路径保持旧形态⇒自测零改动）、`check_gov_doc_claims._pitfalls_count`（N4 对拍）、`check_pitfall_id_unique`（唯一性扫描 + diff 路径六文件化）、`check_agents_layers`（L2 清单含六主题文件 + 「何时读」校验）、`check_doc_size_budget`（字节窗按主题独立·授权依据入注释）、`agent_start`（路由文案指向主题文件）；④ **引用面同步**——AGENTS 路由表、docs/agent/pitfalls.md（二级跳转壳）、HANDOVER×2、两个 SKILL（含**功能性失效的 `grep -n "关键词" pitfalls.md`** ⇒ 拆分后搜不到条目，已改为 `grep -rn … docs/agent/pitfalls-topics/`）、MAINTAINING §一 体量预算；⑤ **跨文件一致性校验**——新增 `scripts/check_pitfalls_split.py`（7 项：文件存在/段头声明=实算/索引壳表与聚合一致/反查表无遗漏无多余/**双层镜像**（每条整行 ∈ 归档全文）/E 号唯一/写窗）+ 对应单测（门禁效果由 CI 的 pytest job 承担·**不挂 verify_delivery**（禁改清单·门禁本体））；⑥ **连带回填**——W1289 的 CI 终态与归因（见验证栏）并入本批（口径「回填并入下一在途批」）。
> - **验证**：坑表拆分 **419 条逐字迁移 0 缺失**（脚本逐条断言「原行 ∈ 新文件」）· 六主题文件各 ≤262144 字节（最大 123,587）· 根壳 4,794 字节且**不含 `- **` 条目行** · **本体 E 号 273/273 唯一**（重号归零）· 归档 diff **16 增 0 删**（纯追加合规）· 反查表覆盖全部本体 E 号 · 双层镜像逐条成立 · 第 31/45/51/74 槽 0 FAIL · 全量门禁 0 FAIL · pytest 全绿 · 一次推送带齐 1 笔⇒1 轮 CI。**W1289 CI 终态**：六作业 5 success + Screenshot Review 失败——**已归因**为 CI 采集器 `page.goto` **20s 超时**（下载 artifact 逐行核对：该页记录 `fatal: page.goto: Timeout 20000ms exceeded` ⇒ 采集不完整 ⇒ 「暗色未应用 + pageError 0→1」是**超时假象**；同批 `en/character-appearance.html` 完全正常 ⇒ **非内容缺陷**）⇒ 根因已定位、加固项（提高 goto 超时 / 超时重试）列入下一批待办，**未按「先红后记」放过**。
> - **状态**：坑表写窗天花板**彻底解除**（按主题独立）· 检索面**保留**（索引壳 + 反查表 + 六主题正本 + 归档全文）· 双层设计保留（正本判据层 / 归档叙事层·归档只追加）· 既有重号已清零 ⇒ 满足「坑表的问题彻底解决后才能进归档」的前置条件。
> - **文件**： pitfalls.md, docs/agent/pitfalls-topics/css-visual.md, docs/agent/pitfalls-topics/js-csp-runtime.md, docs/agent/pitfalls-topics/git-concurrency.md, docs/agent/pitfalls-topics/cascade-changelog.md, docs/agent/pitfalls-topics/data-trust.md, docs/agent/pitfalls-topics/flow-collab.md, archive/docs/pitfalls-detail-ARCHIVE.md, docs/agent/pitfalls.md, docs/agent/MAINTAINING.md, AGENTS.md, HANDOVER.md, .agent/skills/puti-shouye/SKILL.md, .agent/skills/huoyan-jinjing/SKILL.md, scripts/check_doc_sync.py, scripts/check_gov_doc_claims.py, scripts/check_pitfall_id_unique.py, scripts/check_agents_layers.py, scripts/check_doc_size_budget.py, scripts/agent_start.py, scripts/check_pitfalls_split.py, tests/unit/test_pitfalls_split.py, docs/00-导读/W批次编号对账表.md, docs/11-方案报告/计划方案/T123-任务计划执行与经验沉淀报告-2026-11-21.md, docs/11-方案报告/README.md, scripts/output/_w1290_spec.json

### W1289（2026-11-21）：登记滞后判据补全 + 台账 hash 全量回填 + 坑表 E-301 扩写与 E-302 压缩

> - **来源**：用户 2026-11-21 21:08 选中 W1288 收尾回复中「仍留给下一批带入的两项」⇒ 立项 W1289（**直接做掉**，不留待办）。
> - **执行**：① **判据补全**——preflight 原有滞后判据只以状态列为锚（在途 + git 有提交）⇒ 台账行「状态已收官但 hash 列仍空缺」时**完全不可见**（静默失效）⇒ 新增 `hash_is_unfilled` + `find_hash_unfilled`（三要素同时成立：状态非在途·**复用 is_inflight** + hash 占位 + 该 W 在 git 批次标签提交 ⇒ **WARN 级·不改退出码·不进拒绝集**）＋ `parse_ledger` 增解析 hash 列（**状态格内容锚点**反推·禁固定下标）+ 6 例回归锁（含**无提交不命中**与**self 行排除**负样本）；② **台账 hash 全量归位**——存量 **8 行**（W1260/W1275/W1276/W1280-W1284）+ 新判据实证 **2 行**（W1247 `70b8bf412` / W1248 `5f7f19549`·hash 列真为「待回填」）= **10 行**；全程用**显式 `--hash`**（`--from-git` 会覆盖状态列并抹掉详细终态结论 ⇒ 禁用）；③ **坑表面不新增条目**——「豁免登记/基线引用的 sha 也会过期」与 E-301 同族 ⇒ 并入 **E-301 扩写**（症状＝第 82 槽「基线外新增」而非「报告陈旧」；修法＝渲染复核**豁免页模式**与 `--all` **两态都跑**——全量模式只更新 `_w1266_allrender.json`·不更新豁免档案 `chart-legend-render-audit.json`）＋ 压缩 **E-302** 腾窗（1101→654 字节·叙事留归档）；④ **连带清偿**——台账加认领行 ⇒ 61 段超窗口 60 ⇒ 归档腾窗（迁出 W1225-W1226⇒正本 60 段）＋ 归档层结构修正（恢复「`#### E-NN` 段 = 该条叙事全文」并在段内追加「正本判据层」⇒ 正本整行 ∈ 归档段）；⑤ **报告**——T122 落盘 + 方案报告 README §六 登记（137→138 件）。
> - **验证**：新判据现场实测——已回填行（含**反引号 / 多笔组合 / 带说明**三种 hash 形态）全部不命中；W1247/W1248 命中且经**内容核验**确认其 hash 列真为「待回填」（状态列里的 commit hash 不等于 hash 列）⇒ **真缺口**；台账「已收官 + hash 占位」行数 **= 0**；10 行状态列详细结论逐字保留；坑表 261316→261263 字节（硬窗 262144·余量 881）；E-301/E-302 正本整行 ∈ 归档对应段 = True 且两段仍含原叙事全文；台账 60 段（窗口 60）；全量门禁 EXIT=0 · pytest 全绿。
> - **状态**：本批把「已收官但 hash 空缺」从**静默失效**变成**机器可判**（告警级），并把存量 10 行一次清偿归零；用户点名的第二项以**并入同族 E-301** 落地（不新增碎片条目）⇒ 坑表写窗余量 881 字节即现状上限，已登记结构性方案待办。
> - **文件**： scripts/preflight_check.py, tests/unit/test_preflight_check.py, docs/00-导读/W批次编号对账表.md, archive/docs/W批次编号对账表-ARCHIVE.md, pitfalls.md, archive/docs/pitfalls-detail-ARCHIVE.md, HANDOVER.md, docs/11-方案报告/计划方案/T122-任务计划执行与经验沉淀报告-2026-11-21.md, docs/11-方案报告/README.md, scripts/output/_w1289_spec.json

### W1288（2026-11-21）：收官回填与遗留落仓 - 台账四批登记滞后清偿 + 坑表腾窗与三条新坑 + hook 启用指引三处落位

> - **来源**：用户 2026-11-21 19:26「做完」+ 四条遗留如实登记（① 本批实际推了 2 笔 ② 坑表正本余量仅 234 字节 ③ hook 需每个克隆一次性 git config core.hooksPath 启用 ④ assets/game 他方在途未跟踪件已用本地 .git/info/exclude 忽略）⇒ 立项 W1288（收官闭合与遗留落仓批）。
> - **执行**：① **台账回填**——W1287 行状态翻「已收官(hash)」+ 提交列回填 4def11901 + 8c369d416 + 584a92899（收官链第 7 步闭合·代码已推而台账未收）·W1277/W1278/W1279 三行用 `ledger_backfill.py --from-git` 反填（**4 批登记滞后归零**）·登记 W1288 认领行；② **坑表腾窗 + 二层化补齐**——按仓内契约（正本判据层 + 归档叙事层）把 8 条过长正本条目压回判据层（E-291/E-298/E-304/E-301/E-303/E-300）·E-285/E-287 的归档段**回灌为正本当前全文**（原归档为较早版本 ⇒「零内容丢失」契约未成立）⇒ 正本 261910→261059 字节（硬窗 262144）·余量 234→1085；③ **三条新坑**——E-310（CI 轮数被放大 = 反馈回路的位置与延迟·非纪律松）/ E-311（收官第 7 步缺席 ⇒ 登记滞后累积·告警成噪音）/ E-312（仓内版本化 hook ≠ 已生效·core.hooksPath 不随 clone 走 ⇒ 静默失效的假机制）·正本与归档双命中；④ **计数链**——`stats.py --w W1288` ⇒ pitfalls_total 416→419 · pitfalls_flow 220→223 · 9 处标记面跟随 · `--check` 与磁盘实算零差异（33 键）；⑤ **遗留落仓**——hook 启用指引落 AGENTS 常用命令 + 批次交付流水线第 6 步 + E-312 归档三处可见位置（每会话可见 / 流程必读）·「下一批压 1 笔」由 push-gate 的「未推送提交数 ≤ 1」物理约束兜底 · 坑表余量与复盘触发器 T1/T4 与 preflight N1-N5 计数链漂移登记待偿 · assets/game 本地 exclude 且提交一律显式 pathspec 禁 git add -A；⑥ **报告**——T121 落盘 + 方案报告 README §六 登记（136→137 件）。
> - **验证**：台账 4 条滞后行回填后 preflight 滞后告警归零 · 坑表条目 416→419 且正本字节在 262144 内（余量 1085）· E-310/E-311/E-312 正本与归档双命中 · 被剪条目的旧正本全文逐条断言仍在归档段内（零信息丢失）· stats.json 与磁盘实算零差异（33 键）· 全量门禁 EXIT=0 · pytest 1804 passed。
> - **状态**：本批把「已完成」变成「已登记」——W1287 收官链闭合、4 批登记滞后清偿、四条遗留落成仓内可执行形态；下一批起台账滞后告警为零。
> - **文件**： docs/00-导读/W批次编号对账表.md, pitfalls.md, archive/docs/pitfalls-detail-ARCHIVE.md, AGENTS.md, HANDOVER.md, docs/10-方法论沉淀/批次交付流水线.md, docs/11-方案报告/计划方案/T121-任务计划执行与经验沉淀报告-2026-11-21.md, docs/11-方案报告/README.md, scripts/output/_w1288_spec.json, scripts/output/stats.json, scripts/output/stats-index.md, scripts/output/stats-changelog.json

### W1287（2026-11-21）：CI 侧教训机器化 - 工作树干净断言 + 本地仿真复现 CI 步骤序列

> - **来源**：用户 2026-11-21 17:46 直接质疑「你自己看看 CI 跑了多少次，项目内有多少关于 CI 的为什么还是有问题？」⇒ 立项 W1287（流程层追问·非单点缺陷）。
> - **执行**：① **CI 内建断言**——ci.yml 的 Delivery Gate 前加「工作树干净断言」（git status --porcelain 非空即红）⇒ 任何 CI 步骤改动了入库文件而未还原**当场红**，不再以「漏 add」形态延后到门禁阶段（症状离根因远·排查成本高）；② **仿真器覆盖 CI 步骤**——scripts/ci_sim.py 增 --ci-steps（复现 CI 前置序列：重生成输出数据 → graphic/body 探针现跑 → 还原产物 → 干净断言）且 worktree 检出改 **LF**（core.autocrlf=false）对齐 CI blob ⇒ 本地可提前暴露 CI 侧缺陷；③ 台账登记 W1287 认领行（touches 预检 PASS·无冲突）；④ 坑表新增 **E-309**（CI/门禁类教训须分「文本层」与「机器层」·可机器化者一律升级为断言）+ 腾窗压缩 E-306/E-307。｜⑤ **红队复核后的最高杠杆补做（第一性推演）**：**断言补盲区**（git diff --name-only 不覆盖未跟踪文件 ⇒ 并上 git ls-files --others --exclude-standard·实测由 rc=0 改 rc=1）＋ **推前闸门**（ci_sim.py 增 --push-gate：未推送提交数<=1 + 工作树干净含未跟踪 + 关键槽位 + 本批已推笔数告警；仓内 .githooks/pre-push 版本化·一次性 git config core.hooksPath .githooks 启用 ⇒ 把「一批 = 一轮 CI」从纪律变成**物理约束**·闸门红 ⇒ push 被拒）＋ **回落解析加严**（lint_links 的仓库根回落改为「去掉全部上跳后的纯相对路径须在仓内存在」⇒ 区分语境错位与真外部路径·命中输出 [NOTE] 可见）｜⑥ **第一性结论**：CI 轮数的根因是**反馈回路的位置与延迟**（唯一反馈通道是「推 ⇒ 等 20-30 分钟 ⇒ 看结果」⇒ 该延迟反向塑造「一改一推」的行为）⇒ 修法主体是**把验证搬回本地并保证等价**，断言与仿真器只是配套
> - **验证**：断言**正负样本自测**——干净 worktree ⇒ rc=0「工作树干净」；人为弄脏 ⇒ rc=1「工作树非干净： M pitfalls.md」⇒ 断言真能拦（非摆设）；ci.yml YAML 解析通过且断言步骤在位；ci_sim.py --help 出现 --ci-steps；端到端 ci_sim --ci-steps 跑通。；**断言补盲区实测**（造未跟踪文件 ⇒ rc=1 判红·原为 rc=0 漏检）；**产物幂等性实测**（run_all.py 连跑两次 diff 均为空 ⇒ 断言不会因产物非确定性恒红）；**回落加严实测**（lint_links 31079 链接 · 0 broken · 回落命中处打 NOTE）
> - **状态**：本批把「CI 侧教训」从文本层升级为机器层——CI 侧缺陷可在本地被仿真、被当场拦截，不再依赖人工排查 40 分钟；并把提交节奏钉回「一批 = 一轮 CI」（本批一次推送带齐·不再多笔追加）。
> - **文件**： .github/workflows/ci.yml,scripts/ci_sim.py,scripts/output/_w1287_spec.json,docs/00-导读/W批次编号对账表.md,docs/agent/gates.md,pitfalls.md,archive/docs/pitfalls-detail-ARCHIVE.md,docs/11-方案报告/计划方案/T120-任务计划执行与经验沉淀报告-2026-11-21.md,docs/11-方案报告/README.md

### W1286（2026-11-21）：图表内容层存量清偿 - 第82槽内容完备度 + 第83槽标签裁切重叠 + W1285遗留L-01/L-02

**本批要点**（W1286 · 图表内容层存量清偿）：

> - **① 第 82 槽存量清偿**：四项缺口（C1 可读来源 / C2 结论段 / C3 图元 tooltip / C4 图例）真缺口 **129 条 → 0 条基线外新增**；基线**收紧 175 → 32 条**（143 条已消解行删除）。门禁末行 `0 FAIL`，自测 **22/22**。
> - **② 「加了 CSS」≠「页面有节点」（本批最关键教训）**：worker 清偿 ZH 页 C2/C4 时只补了 `.insight-list`/`.scene-legend` 等**完整 CSS 规则**并注明「沿用仓内既有约定」，但 **DOM 里没有对应元素** ⇒ 判据按 class 扫真实节点扫不到 ⇒ C2/C4 照红（实测 `legend_items=0 js_multi=0 svg_colors=13`）。**门禁全绿只证明「无基线外新增」，不证明「目标判据已转绿」** ⇒ 补真实 DOM 节点后 `analyze_html()` 直读 C2=True / legend_items=12 才算清偿。
> - **③ 第 83 槽标签裁切与重叠**：**0 FAIL**（违例 152 条全在基线内·基线外新增 0）；基线 **154 → 152 条**；自测 **9/9**。
> - **④ L-01 源级低对比清偿（27 → 0 处）**：根因是**暗态公共层给图形加 `brightness(1.45)` 提亮**（tokens.css）而两页标签前景色**静态决定** ⇒ 公共工具 `label-contrast.js` 失效时前景与底色同色碰撞（实测暗态白字压提亮橙块 CR 1.03）。修法取**源级静态描边**（判据与工具同款「光晕与底色分离度 ≥3.0 即提供字形分离」机制），**不把工具逻辑复制进页面**（W1285 E-299 教训）；暗底场景改用浅色描边。官方探针 `--no-tool` 口径 **27 → 0 处**，工具开启态与 body 口径均 0 处 ⇒ 无回归。
> - **⑤ L-02 日晷渲染错位清偿**：`chart-design.html` 的 `drawSundial()` 里 d3 `arc()` 的圆心**恒为 (0,0)**，函数内 `cx/cy` 只是局部常量（未接 `.cx()/.cy()`）⇒ 12 个扇形被画在 SVG 左上角而时辰标签按画框中心布点 ⇒ 整体错位；修法给扇形 path 加 `transform: translate(cx,cy)`。
> - **⑥ 探针增量参数**：`svg_text_contrast_probe.js` 新增 `--pages`（限定扫描页）与 `--no-tool`（拦掉公共工具）⇒ 用**官方口径**复现源级缺陷，而非另写临时脚本（临时探针缺描边分离度豁免 ⇒ 27 条假阳）。
> - **⑦ 豁免登记与基线双向校准**：删掉失效的图例豁免行（`81-hardships-view` 已自带 JS 图例·渲染实测 `multi_legend` 8 项可见 ⇒ 原 `render=multi-nolegend` 登记不成立）；渲染复核档案重跑刷新 sha ⇒ 第 82 槽无 stale、无 NOTE。
> - **⑧ 经验沉淀**：坑表新增 **E-300~E-308**（九条；CSS 规则不等于 DOM 节点 / 报告 page_sha 过期即 fail-closed 须重跑探针 / 改内联脚本必重算 CSP 哈希否则整段脚本被拒⇒页面「无报错但图表全不渲染」）；计数链六主题 declared＝actual 全绿（415 条）。
> - **⑨ 目视亲验（E-244）**：主会话本人看渲染图（浅色/深色各态）——ZH 页新增图例块 6 项色块与说明对齐且配色与插画一致；结论块 4 条标记+加粗引导句+缩进正常；暗态热力图分值带深描边可读；暗态时间轴年份字带浅描边清晰。**未采信探针数字替代目视**。
> - **⑪ CI 复检暴露的两条根修（推后补做·本批一并清偿）**：① **判据的「页面内容哈希」跨平台不可复现（E-303）**——本机 Git 全局 core.autocrlf=true ⇒ Windows 工作树检出为 CRLF，而仓内 .gitattributes 声明 * text=auto eol=lf（blob 恒 LF）⇒ 判据按工作树字节算的 sha 与 CI 上 blob 的 sha 永不相等 ⇒ 第82槽「渲染档案过期」+ 第80槽「报告陈旧」在 CI 上必红（实证 about.html：本地 309d118255fa / CI f917041c34ea）——**症状极具误导性**（本地全绿·CI 判红·像「忘了重跑探针」·实为判据缺陷）⇒ 修法：四处（第82槽 _page_sha / 第80槽 page_sha / 渲染复核脚本 / JS 探针）**同款**改为 EOL 归一后哈希（已验证归一后与 HEAD blob 完全一致）；② **装饰性槽位被「隐形图形」判据误计（E-304）**——W1284 把条形图背景轨道改成 var(--paper)（暗态亮度 0.015），暗态审计把**所有 svg circle/rect** 里亮度 <0.16 的深色填充判为隐形（每页上限 10 条·**正好触顶**）⇒ 6 页报「新增 10/8」⇒ 根治：装饰槽位改用 **fill:none + 保留 stroke** 表达轮廓（判据明确跳过 fill=none），并在 tokens.css 立 --track-fill 令牌（明态浅色 / 暗态 none）统一 4 页 4 处 ⇒ 实测 6 页 invisible 全部归零且暗态视觉更清楚（槽位轮廓可见·数值条与标签不受影响）。
> - **⑫ CI 复检第三条根修（口径同源·E-305）**：暗态审计的「低对比」原按「文字 vs body 底色」判，而第 80 槽已确立分工「文字压在图形上 ⇒ 交 graphic 口径按图形实际底色判」⇒ 口径分叉致暗态下「深墨字压被提亮的浅色色块」（视觉可读）被误报不可读（CR 1.1）⇒ 2 页报「新增低对比 2/2」（dashboard 中心数字 / monster-ecology 节点标签等 7 处）⇒ 暗态审计补同源覆盖判定（压在实心图形上 ⇒ 不在本判据计）⇒ 官方判定函数实测 4 页归 0。
> - **⑬ CI pytest job 缺 playwright 的既有欠账清偿**：探针顶部直接 require('playwright') ⇒ 连**纯数据**的 --self-test 也起不来（MODULE_NOT_FOUND）⇒ W1282 引入的 test_w1282_graphic_contrast_scope.py 在 CI pytest job 恒红（该 job 按设计不装浏览器）⇒ 修法：**惰性加载**（chromium 仅真跑时 require）⇒ 自测零依赖（已验证：playwright 不可解析的 cwd 下自测 13/13 通过）。
> - **⑭ CI 复检第四条根修（本批自身回归·Pointer 事件族降级回退·E-306）**：本批 worker 为补 C3 tooltip 给多页加 `<title>` 时，顺手把 W1169 专门改过的 Pointer Events 事件族改回 mouse 族（`pointerenter→mouseenter` / `pointermove→mousemove` / `pointerleave→mouseleave`·3 页 14 处）⇒ ① 移动端触摸交互退化（触屏不触发 `pointerenter`）；② CI 的 `tests/e2e/test_site_quality.js` 派发 `PointerEvent('pointerenter')` ⇒ popup 恒为空 ⇒ **E2E job 判红**（报错像「页面渲染坏了」实为事件族降级）⇒ 修法：按 git diff 的精确行对自动配对回退 14 处（不手改避免漏项）+ 重算 3 页 CSP 哈希 ⇒ 本地 E2E EXIT=0。
> - **⑮ CI 复检第五条根修（判据事件族口径滞后·E-307）**：回退 E-306 的事件族降级后，第 82 槽立刻报 2 条基线外新增（cross-time-danmaku / tag-cloud 的 C3）⇒ 根因是**判据缺陷而非页面缺陷**——第 82 槽 `TOOLTIP_WRITE_RE` 的事件模式清单写死 mouseover|mousemove|mouseenter|mouseleave，而 W1169 已把站点事件族迁到 pointerenter|pointermove|pointerleave⇒ 同一份合规代码（`node.on("pointerenter", …)` 内写 `tooltip.html(…)`）不再命中任何模式⇒ 修法：判据侧同源更新为 `(?:mouse|pointer)(?:over|move|enter|leave)` + docstring 同步；**不选**「给页面补 `<title>` 迎合判据」（给判据看的 DOM·用户拿不到信息）；验收：自测 22/22（含两条负样本仍判红）· 全量违例 34 → 32 条 · 基线外新增 2 → 0 · 末行 0 FAIL · 基线 32 条无需收紧。
> - **⑯ CI 复检第六条根修（CI 自身产物触发 C4-f 假红·E-308）**：本批最后一笔推送后 CI 主 run 的 Delivery Gate 判红，**唯一红项是第 31 槽 2 FAIL**（本地 check_doc_sync.py 0 FAIL）⇒ 排查排除「本地工作树脏 / 浅克隆 / 行尾差异」三个解释（LF 工作树里跑仍 0 FAIL）⇒ 在 LF 工作树里改写两份探针报告的 `generated_at` 模拟「CI 现跑过」⇒ 报出与 CI 完全一致的 2 条 C4-f ⇒ 根因坐实：**探针报告入库后，CI 在 verify 前现跑探针会重写入库文件 ⇒ 工作树残留 ⇒「漏 add」防线把 CI 自己的临时产物判红**⇒ 修法：CI 现跑后 `git checkout --` 还原工作树；检测不降级（入库报告带 page_sha ⇒「报告陈旧」fail-closed 仍由入库产物承担，CI 现跑仍承担「页面在 CI 可渲染」的自证）⇒ 判据产物入库后，新鲜度应由内容哈希承担，而非由「CI 现跑覆盖」承担。
> - **⑩ 状态**：已收官（第 82 槽 0 FAIL + 第 83 槽 0 FAIL + L-01/L-02 清偿 + 九条坑表沉淀 + 报告 T119 落盘）。
> - **文件**： site/data/,site/en/,site/dashboard.html,scripts/svg_text_contrast_probe.js,scripts/output/chart-content-baseline.txt,scripts/output/chart-label-clipping-baseline.txt,scripts/output/chart-legend-exemptions.txt,scripts/output/chart-legend-render-audit.json,scripts/output/svg_text_contrast_graphic_report.json,scripts/output/svg_text_contrast_report.json,pitfalls.md,archive/docs/pitfalls-detail-ARCHIVE.md,docs/11-方案报告/计划方案/T119-任务计划执行与经验沉淀报告-2026-11-21.md,docs/11-方案报告/README.md,docs/00-导读/W批次编号对账表.md,CHANGELOG.md

### W1285（2026-11-20）：graphic 口径覆盖面补齐 + 探针去重盲区修复 + 判据稳定性根修

**本批要点**（W1285 · graphic 口径覆盖面补齐 + 探针去重盲区修复 + 判据稳定性根修）：

> - **① 扫描面纳入站点根**：探针页面枚举长期只含 `site/data + site/en `⇒ **站点根十页从未被测过**；本批纳入 root 作用域（根页 rel 无子目录前缀·路径深度不同 ⇒ 公共工具引入路径为 `static/js/label-contrast.js `）⇒ graphic 口径扫描页 **162 → 168**（含图根页 6 个：about / curated / dashboard / dukou-engine / guide / index）。
> - **② 去重键含底色维度**：原去重键只有文案 ⇒ **同页同名但落在不同底色的**文字只判第一个 ⇒ 其一被静默漏判；新键＝所属 SVG + 文案 + 底色来源 + 底色值，且**去重时机移到底色确定之后**（否则键里的底色维度恒空）⇒ 同底色仍去重（基线可对账性不变）· 不同底色分别判定。探针自测 11 → **12 项**（新增「同名不同底色分别判定·同底色仍去重」）。
> - **③ 第三处盲区：判定结果不可复现**——本批最关键发现。稳定判据「指纹连续两次相同」不足以保证采到**最终视觉状态**：① 颜色动画的「平台期」在两次采样恰好相同时会被误判为稳定 ⇒ 采到**动画中间态颜色**；② 页面尚未渲染出图表 ⇒ 指纹同样「两次相同」⇒ 采到空/不完整状态；③ 采集时刻该页该态无任何 svg 文字（多见于「图表滚出视口即卸载」的懒渲染页）⇒ **判定面为空·无可判内容·不产生漏检**。实证：A/B 对照（git worktree 取 HEAD 态页面·同一批页面分别用 HEAD 探针与本批探针实跑）两组结果**互不包含**（3 条 vs 59 条）⇒ 违例集合**随跑动波动**。修法四层：① 指纹加 display+visibility 且要求**连续 3 次**相同（原 2 次）+ 慢渲染页放宽超时重试；② 稳定须「已渲染产出（文字或图形）> 0」以排除平凡解（抽为纯函数·单测可直接断言）；③ 未能稳定 ⇒ 记 unstable（探针退出码 4）⇒ 门禁 unstable_rows > 0 ⇒ **fail-closed 拒绝通过**；且报告**缺** unstable_rows 字段（旧版探针产出）⇒ 同样 fail-closed（此前按缺字段→0 处理属 **fail-open**）；④ **判定面为空**（采集时刻无 svg 文字）⇒ 记 empty_rows 而**不**记 unstable（避免把「无可判内容」误判成不稳定而阻断全站）。⚠ 自我订正留痕：初稿把机制归因为「未渲染 ⇒ 平凡解 ⇒ 静默漏检」，其关键证据「同一页单页跑 2 条 / 全站跑 0 条」**跑的是同一份脚本** ⇒ 只能证明不可复现；且独立 worker 用同一脚本连跑 12 次全 0 ⇒ 那 2 条实为**动画中间态假阳** ⇒ 归因修正为上述三形态，并据此把「未加固探针的 63 条」订正为**加固后的真实暴露量 59 条 / 6 页**（63 − 59 = 4 条即 poetry-rhythm-analysis 的动画中间态假阳·与 12 次跑全 0 吻合）。
> - **④ 第五处同源化**：公共工具 site/static/js/label-contrast.js 的多层覆盖候选选择由「交集覆盖率最大」改为「**bbox 面积最小**」，与门禁 pickCoveringShape() 一致（原实现**连自己的注释「面积最小者」都不符**）⇒ 否则同一文字两侧选出不同底色 ⇒ 工具判达标而门禁判红（实证 chart-design 的「戌」：工具取黑扇形·门禁取橙扇形·白描边分离度 2.80 < 3.0）。门禁自测 25 → **27 项**（新增 unstable fail-closed 端到端 2 例）。
> - **⑤ 暴露即清偿（不冻结基线）**：加固后探针对 HEAD 态页面实测暴露 **59 条 / 6 页** ⇒ **56 条靠补接入公共工具自动清零**（根页 dashboard 16 + material-archaeology 24 + data/en power-resources 各 8）+ **3 条逐页清偿**（chart-design CR 2.94 → 5.45 · en/game-webnovel 深色描边 · aesthetics 源级指定色）+ 另含 pilgrim-team 事件标签改深一档同色系 #8a6a1c + **根修「时隐时现」**（末端直标错开 20px + 散点比例尺留白 38px ⇒ 4 态 hidden 由 1 降为 0）。
> - **⑥ 收官证据（可复现性）**：graphic 口径**连跑两遍**均 **168 页 / 672 行 / 违例 0 · 违例页 0 · unstable 0 · fatal 0 · 退出码 0**，**两遍违例集完全一致** ⇒ 结论可复现（这正是 W1284「1236 → 0 条」所缺的证据）。
> - **⑦ 口径界定与 CI**：两个口径**扫描面有意不同**（graphic --scope all 含根页 168 页 / body --scope data,en 保持 W1265 原定义 162 页——body 粗口径只取「文字 vs 页面底色」⇒ 对「文字压卡片/色块」有语义性假红·dashboard 16 条·根页由 graphic 覆盖）；body 口径报告新增全量 page_sha ⇒ stale 检测对它生效 ⇒ **CI 加跑 body 探针**（此前 body 报告无 page_sha ⇒ stale 检测对它完全失效 ⇒ 该槽长期在读一份三天的陈旧报告·实际显示 0 违例而现状 24 条）。
> - **⑧ 状态**：已收官（覆盖面 + 去重面 + 稳定性 + 第五处同源化 + 可复现性验收 + 双口径门禁全绿）。
> - **⑨ 遗留（6 项·已量化登记）**：L-01 两页源级缺陷（公共工具失效时暴露；worker 的页内加固已**备份后撤销**以免出现公共工具的第二份实现）· L-02 chart-design drawSundial() 未设 .cx()/.cy() 的既有渲染错位（另立批次）· L-03 game-webnovel 顶部散点标签自重叠（不翻转判决）· L-04 poetry-rhythm-analysis 4 条不可复现（12 次 4 态跑全 0）· L-05 ming 页延迟隐藏 · L-06 根页的 body 口径覆盖。
> - **⑩ 经验**：坑表新增 **E-295~E-299**（去重键须含判定依赖的全部维度且时机须晚于依赖量确定 / 扫描面须显式核对·别让默认子集成为永久盲区 / 批量写入产物须回读且归档面不在门禁扫描面 / 稳定判据须排除「尚未渲染」的平凡解 / worker 产出须先核对官方口径是否真违例·过度修复也要拦截）。
> - **文件**： scripts/svg_text_contrast_probe.js,scripts/check_svg_text_contrast.py,scripts/output/svg_text_contrast_graphic_report.json,scripts/output/svg_text_contrast_report.json,scripts/output/svg-text-contrast-graphic-baseline.txt,scripts/output/svg-text-contrast-baseline.txt,site/static/js/label-contrast.js,.github/workflows/ci.yml,site/,docs/agent/gates.md,pitfalls.md,archive/docs/pitfalls-detail-ARCHIVE.md

### W1284（2026-11-19）：图表标签低对比存量清偿 与 graphic 全量基线接入 CI

**本批要点**（W1284 · 图表标签低对比存量清偿 与 graphic 全量基线接入 CI）：

> - **① 存量清偿（四步并进）**：第 80 门禁 graphic 口径实测全站 **1236 条 / 89 页** → 本批 **个位数**。① **通用工具补强**（跳过 fill=none 的装饰性图形 + 底色取不到时继续找下一个候选·与门禁同源）⇒ 182 → 89 条；② **补齐 8 页漏接入**（铺开清单按最新命中面重算·89 → 97 页）⇒ 89 → 70 条；③ **逐页清偿**（四个 worker 并行·跨底色标签只能靠不透明描边或指定高对比色）；④ **判据分组键根治**。
> - **② 判据分组键根治（本批最关键发现）**：worker 清偿时发现 `famous-time-travel` 含两个无 id 的 `<svg>` ⇒ 探针的 svgId 全为空串 ⇒ **一幅 SVG 的文字被几何配对到另一幅 SVG 的图形上**（明信片正文被配到另一幅插画的矩形·CR 2.10 假红）。全站 **147 页含多 SVG、其中 23 页多个无 id** 同等中招 ⇒ 探针改按 DOM 顺序给匿名 SVG 分配稳定键 ⇒ 全站 **27 → 2 条**（大量原「违例」实为跨容器错配假红）。**若不修，对齐方向会被误导**（去改本来没问题的页面）。
> - **③ graphic 全量基线接入 CI（未改 verify_delivery.py·属禁改清单）**：门禁脚本默认**双口径判定**（body 与 graphic 各自对拍自己的基线·基线声明口径隔离·互不放行）·**末行合并汇总**取两口径基线外新增之和 ⇒ 既有挂槽取末行即得两口径总判定；报告新增**全量页面内容哈希** ⇒ 页面一改而探针未重跑即判「报告陈旧」并 fail-closed（复用第 82 槽渲染档案同款机制）；门禁自测 18 → **24 项**·探针自测 9 → **10 项**。
> - **④ 负向证明（判据有区分力）**：注入一条基线外新违例 ⇒ 门禁 **判红并逐条列出**（退出码非零）·还原后转绿；改动一个页面制造报告陈旧 ⇒ 门禁判「档案 sha 与当前不符」并指出具体页（退出码非零）。
> - **⑤ 状态**：已收官（存量清偿 + graphic 口径纳入 CI + 判据分组键与防陈旧补齐）。
> - **⑥ 遗留**：根页（站点根十页）未纳入 graphic 口径（探针页面枚举口径）· 工具与门禁两处实现须持续同源（E-287/E-294 已入坑表）。
> - **文件**： scripts/svg_text_contrast_probe.js,scripts/check_svg_text_contrast.py,scripts/output/svg_text_contrast_graphic_report.json,scripts/output/svg-text-contrast-graphic-baseline.txt,site/static/js/label-contrast.js,site/data/,site/en/,tests/unit/

### W1283（2026-11-19）：图表标签可读性存量清偿（通用工具化与判据同源化）

**本批要点**（W1283 · 图表标签可读性存量清偿 · 通用工具化与判据同源化）：

> - **① 通用工具化（新公共资源 site/static/js/label-contrast.js）**：页面引入即自动执行——按**渲染后实际底色**自适应前景色与描边（底色链＝几何覆盖图形 → 最近 CSS 背景；暗色态按公共层 brightness 提亮后的视觉实际值计算）。**八十九页各加一行外链 script**（页面零逻辑改动；CSP script-src self 已放行外链，不需重算哈希）。
> - **② 存量清偿效果**：第 80 门禁 graphic 口径实测全站 **一千二百三十六条 / 八十九页** → 本批后 **一百六十七条 / 二十六页**（**降约八成六**）；中英文站同款覆盖。
> - **③ 判据与工具同源化三处**（E-285 纪律）：矩形档补「文字中心点须落在图形包围盒内」；graphic 口径无覆盖图形时回退**最近 CSS 背景**（原先回退页面底色 ⇒ 工具按卡片底判达标、门禁按页面底判红 ⇒ 工具改完仍被判红）；图形底色乘 **滤镜提亮系数**（暗色态公共层提亮图形而计算色仍是原色）。
> - **④ 英文树图长标签根治**：字号自适应（十二至十像素实测）→ 放不下则按空格折行（至多三行）→ 实在放不下才截断，并挂原生 title 兜底 ⇒ **截断数三 → 零**，全标签完整可读。
> - **⑤ 工具自身三处坑（实证）**：去抖写法在 DOM 持续变化时会被无限推迟（改为节流）· 只监听主题属性而不监听系统配色（补监听）· 模块导出漏项。
> - **⑥ 门禁与回归**：探针自测八项扩到**九项全过**（新增图形口径回退断言）·回归锁**十三例全过**（含口径更新后的断言）。
> - **⑦ 状态**：已收官（通用工具化 + 判据同源化 + 英文标签根治）。
> - **⑧ 遗留**：剩余一百六十七条 / 二十六页属结构性（中等亮度底色下白与深墨皆不达标 · 半透明图形 · 路径保守档）需页面级改造；graphic 全量基线接入 CI 待另批裁决（未改既有门禁挂槽）。
> - **文件**： site/static/js/label-contrast.js,site/data/,site/en/,scripts/svg_text_contrast_probe.js,tests/unit/test_w1282_graphic_contrast_scope.py,scripts/output/svg_text_contrast_remaining_W1283.json

### W1282（2026-11-19）：图表标签可读性修复（treemap 六页 与 第八十门禁图形底色口径）

**本批要点**（W1282 · 图表标签可读性修复 · 自我证伪与判据补盲）：

> - **① 自我证伪（推翻上一批机制解释）**：上一批把「图表内文字看不清」归因为「treemap 标签两行 y 坐标相同 ⇒ 文字重叠成糊」；本批逐元素实测**推翻**——名称行 bbox y=4.3~16.8 · 百分比 tspan y=16.8~31.1 ⇒ **两行相接不重叠**（当时把「整体 bbox 高度」误读成重叠）。真因三条：① **白字压浅赭底色块对比度仅一点八**（远低于三比一线）② **公共层 svg text 的 !important 把页内写的字号压到十像素** ③ **页内白描边叠白字**。三处错误描述已订正入仓（CHANGELOG 第七条 / T114 第十一节 / 台账 W1281 行）。
> - **② treemap 六页可读性修复**：中文英文站各三页（八十一难 / 美学 / 全球格局）——前景按单元格底色亮度自适应 + 字号下限十二像素 + 描边随前景切换（深字配浅描边）+ 英文长标签二分截断加省略号。最低对比度**从一点八提升至三点二五**（明态）**三点三一**（暗态）。
> - **③ 双协议与目视验收**：六页乘双协议乘明暗 = **八十八组标签零差异**；非 treemap 部分十二个状态逐项一致；第八十三槽基线外新增零；控制台错误 http 侧零、file 侧与基线逐页一致（存量字体跨域）；**主会话亲自看图**（明暗四态·中英双站）确认可读。
> - **④ 第八十门禁补图形底色口径**：新增第三种底色口径——底色取**几何上真正覆盖该文字的 SVG 图形**的计算填充色（getBBox 加 getCTM 归一化到同一 viewBox 用户空间，禁用视口坐标矩形）；矩形按交集比例不小于零点六、圆形按真实椭圆、路径按包围盒完全包含三档规则；光晕按「与真实底色分离度」才豁免。**实测 site/data 存量违例从零条变为六百四十六条 / 四十五页**（既有 body 口径行为零变化·基线与报告产物零改动）。
> - **⑤ 门禁与回归**：第八十门禁自测由八项扩到**十八项全过**；探针几何自测**八项全过**；新增回归锁**十三例全过**；gates.md 第八十槽同步三口径。
> - **⑥ 状态**：已收官（treemap 六页修复 + 判据补盲 + 三处订正 + 报告 T115 落盘）。
> - **⑦ 遗留**：图形口径全量基线待另批决策（未改 verify_delivery 挂槽）·存量六百四十六条清偿待另批 · 英文标签截断后信息不完整待文案专项 · 其余网络图与雷达图同类缺陷待新口径重测后分批。
> - **文件**： CHANGELOG.md,docs/00-导读/W批次编号对账表.md,docs/11-方案报告/计划方案/T114-任务计划执行与经验沉淀报告-2026-11-18.md,docs/11-方案报告/计划方案/T115-任务计划执行与经验沉淀报告-2026-11-19.md,docs/11-方案报告/README.md,docs/agent/gates.md,scripts/check_svg_text_contrast.py,scripts/svg_text_contrast_probe.js,tests/unit/test_w1282_graphic_contrast_scope.py,site/data/81-hardships.html,site/data/aesthetics.html,site/data/global-pattern.html,site/en/81-hardships.html,site/en/aesthetics.html,site/en/global-pattern.html

### W1281（2026-11-19）：A 方案铺开第二批（公共层外链化 site/data 全站）

**本批要点**（W1281 · A 方案铺开第二批 · 公共层外链化 site/data 全站）：

> - **① 铺开第二批**：site/data **全站**公共层外链化（**排除 `_shell.html` 模板壳**）⇒ 剥离公共层规则，保留页私有层，体积 **净减 6,008,104 B**。
> - **② 双协议 × 明暗对照**：5 页 × file:// 与 http:// × 明暗 = **20 组**，改造前后 computed style **零差异**·cssLeak 0·异常 0（改造前已留同 scope 基线·E-282 纪律）。
> - **③ 判定面口径修订三处**（E-281/E-283 同族第三次、第四次）：① 第 64 槽 A8 静态契约的判定面（EN 页整页文本）随形态修订 ⇒ **公共层文本并入判定面**；② 第 29 槽色盲判据的色板提取面随形态修订（公共层并入）+ 因页内色板变化补录 1 条基线对；③ 内嵌回退判据的 `INLINE` 误匹配 `<!-- INLINED CSS -->` 注释 ⇒ 剔除后**露出 7 页真缺 file:// 数据回退**（既有缺陷·被误判掩盖）⇒ 冻结登记待专项。
> - **④ 内置浏览器明暗目视（用户在场）**：data 主站图表页（http 协议）明/暗两态亲验 —— 外链 CSS 生效、横幅/面包屑/KPI/图表容器完整、**零布局破坏**。
> - **⑤ 状态**：已收官（铺开第二批 全站 + 三处判定面修订 + 存量缺口冻结登记）。
> - **⑥ 遗留**：reader 树 636 页（须先解 build_reader 内置 --reader --inline-links）·7 页缺内嵌数据回退（存量·待专项补齐）·公共层变体面（body 58 条）·EN 首页明态 hero 文字（既有缺陷）。
> - **⑦ 目视补检抓到的既有缺陷（与本批改造无关）**：明/暗两态图表区特写复核时发现 **treemap 标签文字不可读**；经 Playwright 同页 CSSOM 逐项对拍（font-size / fill / stroke / stroke-width / paint-order / getBBox 几何）**改造前后完全一致**（EN 站同款·W1280 亦不引入）⇒ **属既有缺陷·非外链化引入**。**【W1282 订正】本条的机制解释当时写错**：原文归因为「标签两行 y 坐标相同 ⇒ 文字重叠成糊」，W1282 逐元素实测推翻——名称行 bbox y=4.3~16.8、百分比 tspan y=16.8~31.1（dy=1.25em）⇒ **两行相接不重叠**（当时把「整体 bbox 高度 27px 看起来像叠一起」误读成重叠）；真因是 **①白字压浅赭底 `#e9b885` 对比度仅 CR=1.80（远低于 3:1）②公共层 `svg text{font-size:max(9px,0.625rem) !important}` 把页面内 `0.74rem` 压到实测 10px ③页内 `svg text` 白描边 rgba(255,255,255,0.88) 叠白字** ⇒ 已于 W1282 开批修复。
> - **文件**： .github/workflows/README.md,AGENTS.md,CHANGELOG.md,CITATION.cff,HANDOVER.md,README.md,STRUCTURE.md,archive/docs/AGENTS-ARCHIVE.md,archive/docs/W批次编号对账表-ARCHIVE.md,archive/docs/workflows-readme-history.md,docs/00-导读/W批次编号对账表.md,docs/00-导读/项目说明.md,docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md,docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md,scripts/check_chart_colorblind.py,scripts/output/INDEX.md,scripts/output/README.md,scripts/output/_cascade_files_W1281.txt,scripts/output/_vermilion_solid_cache.json,scripts/output/_w1266_allrender.json,scripts/output/_w1281_spec.json,scripts/output/chart-legend-render-audit.json,scripts/output/colorblind-baseline.txt,scripts/output/file-index.md,scripts/output/stats-changelog.json,scripts/output/stats-index.md,scripts/output/stats.json,scripts/output/tools-inventory.md,scripts/verify_delivery.py,site/data/81-hardships-view.html,site/data/81-hardships.html,site/data/aesthetics.html,site/data/ai-dialogue.html,site/data/business-model.html,site/data/cave-estate.html,site/data/century-dialogue.html,site/data/chapter-stats.html,site/data/chapter-structure-graph.html,site/data/character-appearance.html,site/data/character-dynamic-network.html,site/data/character-presence-timeline.html,site/data/character-relationship-3d-view.html,site/data/character-relationship-3d.html,site/data/character-semantic-network.html,site/data/character-sentiment-arc.html,site/data/chart-design.html,site/data/cognitive-psychology.html,site/data/concept-device.html,site/data/counterfactual.html,site/data/criticism-history.html,site/data/cross-time-danmaku.html,site/data/cultural-misreading.html,site/data/customs-pass-route.html,site/data/data-explorer.html,site/data/deconstruction.html,site/data/dialogue-sentiment.html,site/data/ecology.html,site/data/emotional-heatmap.html,site/data/ethics-consumption.html,site/data/famous-time-travel.html,site/data/four-dimensional-research-network.html,site/data/four-heavenly-kings-artifacts.html,site/data/game-webnovel.html,site/data/global-pattern.html,site/data/glossary.html,site/data/graph-explorer.html,site/data/guanyin-six-roles-network.html,site/data/hardship-difficulty-heatmap.html,site/data/hardship-heatmap.html,site/data/heaven-power-network.html,site/data/intertextuality-network.html,site/data/journey-geo-3d.html,site/data/journey-geo-semiotics.html,site/data/journey-map-interactive.html,site/data/journey-route.html,site/data/journey-spacetime.html,site/data/jurisprudence.html,site/data/karma-reincarnation.html,site/data/language-style-radar.html,site/data/linguistics.html,site/data/magic-system.html,site/data/material-archaeology.html,site/data/mbti-evolution.html,site/data/methodology-matrix.html,site/data/ming-political-thought-comparison.html,site/data/monster-background.html,site/data/monster-capability-radar.html,site/data/monster-ecology-network.html,site/data/monster-female-network.html,site/data/monster-hierarchy-network.html,site/data/monster-sociology.html,site/data/monster-victims-network.html,site/data/music-structure.html,site/data/narrative-experiment.html,site/data/narrative-rhythm-curve.html,site/data/narratology-12d-network.html,site/data/narratology-16d-network.html,site/data/perf-canvas-rendering.html,site/data/philosophy.html,site/data/pilgrim-team-dynamic-network.html,site/data/pilgrim-team-psychology-arc.html,site/data/poetry-density.html,site/data/poetry-rhythm-analysis.html,site/data/power-resources.html,site/data/relationships.html,site/data/risk-project.html,site/data/search.html,site/data/six-senses-narratology-network.html,site/data/social-media.html,site/data/story-timeline.html,site/data/tag-cloud.html,site/data/text-evolution.html,site/data/text-search.html,site/data/theological-intervention-network.html,site/data/timeline.html,site/data/underworld-power-network.html,site/data/visual-art.html,site/data/workplace.html,site/data/wukong-tangseng-benchmark.html,site/dukou-engine.html,site/index.html,site/rss.xml
### W1280（2026-11-19）：A 方案铺开第一批落地 与 判定面口径再修订

**本批要点**（W1280 · A 方案铺开第一批落地 + 判定面口径再修订）：

> - **① 铺开第一批入库**：site/en 全站 **138 页**公共层外链化（剥离公共层规则 **57,545 条**·保留页私有规则 968 条·体积 **净减 9,261,742 B**）；守恒校验以 git show HEAD 为基准 0 失败（外链缺失 0 页次·body 逐字变更 0 页）。
> - **② 口径再修订（第 64 槽 A8）**：A8 静态契约读的是 EN 页**整页文本**里的三项窄屏特征（media 查询 / overflow-x / flex-column），外链化后这些声明由公共层提供 ⇒ 138 页判红（改造前实测 0）⇒ 把**公共层文本并入判定面**后 **违规 130 → 0**。
> - **③ 同源模块（横向能力抽模块不抄实现）**：新增 scripts/utils/css_public_layer.py（public_layer_text·路径按**页所在目录**解析），第 53 槽与第 64 槽一律 import 它 ⇒ 坑位 E-283。
> - **④ E-282 定性订正**：上一轮「130 违规属真回归」**订正为口径失配**——375px **真探针**实测 EN 148 页 FAIL 1 = 存量基线页 rum-viewer.html（非新增）⇒ 根因是判定面未随形态修订（E-281 同族），不是移动视口真回归。
> - **⑤ 验收口径升级为全量受影响面**：双协议 × 明暗 **20 组零差异**（cssLeak 0·异常 0）·守恒 0 失败·第 64 槽 EN 面 0 违规·375px 真探针 FAIL 1（存量基线页）·token 0 FAIL·第 82 槽 0 FAIL·pytest 1787 passed。
> - **⑥ 内置浏览器目视（用户在场）**：EN 首页与八十一难图表页（http 协议）——外链 CSS 生效（衬线标题/宣纸底/朱砂强调全对）、横幅/面包屑/数据源标注/KPI 四卡完整、**零布局破坏**；首页明态 hero 上导航文字不可见为既有缺陷（HEAD 同款·首页深底特例）。
> - **状态**：已收官（铺开第一批落地 + 判定面口径再修订 + 同源模块 + 回归锁 3 例 + 两条坑位）
> - **遗留**：reader 树 636 页（须先解 build_reader 内置 --reader --inline-links）·site/data 90 页（下一批）·公共层变体面（body 58 条）·EN 首页明态 hero 文字（既有缺陷）。
> - **文件**： CHANGELOG.md,archive/docs/W批次编号对账表-ARCHIVE.md,docs/00-导读/W批次编号对账表.md,docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md,docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md,scripts/check_chart_colorblind.py,scripts/output/_vermilion_solid_cache.json,scripts/output/_w1266_allrender.json,scripts/output/_w1281_spec.json,scripts/output/chart-legend-render-audit.json,scripts/output/colorblind-baseline.txt,scripts/output/stats-changelog.json,scripts/output/stats-index.md,scripts/output/stats.json,scripts/output/tools-inventory.md,scripts/verify_delivery.py,site/data/81-hardships-view.html,site/data/81-hardships.html,site/data/aesthetics.html,site/data/ai-dialogue.html,site/data/business-model.html,site/data/cave-estate.html,site/data/century-dialogue.html,site/data/chapter-stats.html,site/data/chapter-structure-graph.html,site/data/character-appearance.html,site/data/character-dynamic-network.html,site/data/character-presence-timeline.html,site/data/character-relationship-3d-view.html,site/data/character-relationship-3d.html,site/data/character-semantic-network.html,site/data/character-sentiment-arc.html,site/data/chart-design.html,site/data/cognitive-psychology.html,site/data/concept-device.html,site/data/counterfactual.html,site/data/criticism-history.html,site/data/cross-time-danmaku.html,site/data/cultural-misreading.html,site/data/customs-pass-route.html,site/data/data-explorer.html,site/data/deconstruction.html,site/data/dialogue-sentiment.html,site/data/ecology.html,site/data/emotional-heatmap.html,site/data/ethics-consumption.html,site/data/famous-time-travel.html,site/data/four-dimensional-research-network.html,site/data/four-heavenly-kings-artifacts.html,site/data/game-webnovel.html,site/data/global-pattern.html,site/data/glossary.html,site/data/graph-explorer.html,site/data/guanyin-six-roles-network.html,site/data/hardship-difficulty-heatmap.html,site/data/hardship-heatmap.html,site/data/heaven-power-network.html,site/data/intertextuality-network.html,site/data/journey-geo-3d.html,site/data/journey-geo-semiotics.html,site/data/journey-map-interactive.html,site/data/journey-route.html,site/data/journey-spacetime.html,site/data/jurisprudence.html,site/data/karma-reincarnation.html,site/data/language-style-radar.html,site/data/linguistics.html,site/data/magic-system.html,site/data/material-archaeology.html,site/data/mbti-evolution.html,site/data/methodology-matrix.html,site/data/ming-political-thought-comparison.html,site/data/monster-background.html,site/data/monster-capability-radar.html,site/data/monster-ecology-network.html,site/data/monster-female-network.html,site/data/monster-hierarchy-network.html,site/data/monster-sociology.html,site/data/monster-victims-network.html,site/data/music-structure.html,site/data/narrative-experiment.html,site/data/narrative-rhythm-curve.html,site/data/narratology-12d-network.html,site/data/narratology-16d-network.html,site/data/perf-canvas-rendering.html,site/data/philosophy.html,site/data/pilgrim-team-dynamic-network.html,site/data/pilgrim-team-psychology-arc.html,site/data/poetry-density.html,site/data/poetry-rhythm-analysis.html,site/data/power-resources.html,site/data/relationships.html,site/data/risk-project.html,site/data/search.html,site/data/six-senses-narratology-network.html,site/data/social-media.html,site/data/story-timeline.html,site/data/tag-cloud.html,site/data/text-evolution.html,site/data/text-search.html,site/data/theological-intervention-network.html,site/data/timeline.html,site/data/underworld-power-network.html,site/data/visual-art.html,site/data/workplace.html,site/data/wukong-tangseng-benchmark.html
### W1279（2026-11-19）：AGENTS 地图化重建批（五文件分层治理·用户框架落地）

**本批要点**（W1279 · 五文件分层治理批·用户两份框架文档落地）：

> - **① AGENTS 重建为地图（86 行 / 11.4KB·原 ~350 行 / 31.8KB）**：结构按截断安全序 = 1-2 行定位 → 铁律 24 条前移（注意力高地）→ **路由表**（13 文件·每条含触发条件·gates.md 行为指令式「任何写操作或提交前 → 先跑 verify_delivery.py，红时查对应槽条目」）→ 常用命令 → 环境指针 → 维护契约极简 → 脚注；§1 宣传/§2 技术栈/§3 目录树/§4.1 数据流/§4.2 槽位摘要/§4.3 主题视图/§4.4/§5/§7/§8 全部外移或直删（README/STRUCTURE/gates.md 正本承载·零内容丢失核验=路由表逐条覆盖）。
> - **② 铁律区职责分流（审查校准落地）**：17/18/20-24 七条流程规则各保编号压一句（关键词各自保留·「已被机械化与流程文档承载 → 流水线 §九 + MAINTAINING §六」）；15/16 长实证压一句保要点；rule5 具名例外全文恢复（并行批曾压缩·从会话原版逐字补回）。
> - **③ MAINTAINING.md 拆出**（docs/agent/·新建）：维护契约全文 = 体积预算表（AGENTS ≤200 行/CLAUDE ≤60/pitfalls 262144/接收方同步挂窗）+ **退役三标准**（会话性移 pitfalls/过时直删/机械化交工具）+ **添加前四问**（vLLM 式）+ 局部化预留形态（按族聚合·作用域声明生成路由·不继承）+ 时间纪律指针 + 环境事实接收（§八）。
> - **④ CLAUDE.md 导入式（15 行）**：`@AGENTS.md` 确定性导入 + Claude 专属段（3 行）；原 17 条速查退役（内容归宿：铁律区/文档规范 §4.9/§11.1/pitfalls·逐条核验零丢失）。
> - **⑤ 判据重锚三处**：41 槽 C2 改两方对账（gates.md == verify·AGENTS 侧改路由行判据）+ T3-T6 自测更新；31 槽 C3 声明面重锚 gates.md（agents_gate_list_max 兼容保留 + gates_gate_list_max 新增·gather 补 gates_md 输入）；41 槽 C3 的 450 行僵尸判据退役（74 槽 34000B 已覆盖·改指针）。
> - **⑥ 32 槽新增 C5 导入有效性**：@AGENTS.md 行首指令必须存在（静态面）——运行时包含性由人工抽验记录（W1279 判据重定义·锚点对拍对镜像形态退役）。
> - **⑦ pitfalls 三阶段收口并入本笔**（上批 ⑨ 收尾笔被本批巨改打断·合并入库）：221.7KB 过 262144 全局硬窗（test_w1120 实测口径·BYTE_CAPS 对齐）；计数链 379→390（并行批 W1272-76 新增 11 条·分项声明与实测一致）。
> - **⑧ workflow 治理（上批 ⑧ 合并入库）**：禁用三条死触发 workflow（ci-sim/dependency-review/stale·gh disable 可逆）——本批推送触发面实测 4-6 条 → 收敛。
> - **状态**：已收官（AGENTS 86 行地图 + MAINTAINING/CLAUDE 分层就位 + 三处判据重锚 + 瘦身收口；W1277-W1278 段内订正笔一并入库）
> - **验证**：41 槽自测 6/6 + 0 FAIL；32 槽 0 FAIL（C5 新判据）；31 槽 C5e/C5d 绿（390 计数链 sweep 一致）；74 槽 0 FAIL（221.7KB/11.4KB 在窗）；54 槽 0 FAIL；guardrails --strict-api 通过；ruff 0 错；cspcheck 0 漂移；行数 86 ≤ 200 预算。
> - **文件**：AGENTS.md,docs/agent/MAINTAINING.md,CLAUDE.md,pitfalls.md,archive/docs/pitfalls-detail-ARCHIVE.md,scripts/check_agents_layers.py,scripts/check_claude_md.py,scripts/check_doc_sync.py,scripts/check_doc_size_budget.py,docs/agent/gates.md,docs/00-导读/W批次编号对账表.md,CHANGELOG.md,scripts/output/file-index.md,README.md,STRUCTURE.md,docs/00-导读/项目说明.md,CITATION.cff,.github/workflows/README.md,site/index.html,scripts/output/_w1279_spec.json,scripts/output/_cascade_files_W1279.txt,scripts/output/stats.json,scripts/output/stats-changelog.json,scripts/output/stats-index.md,scripts/output/tools-inventory.md,scripts/output/_vermilion_solid_cache.json,site/data/search-index-zh.js,site/en/search-index-en.js,docs/INDEX.md,scripts/INDEX.md,docs/agent/INDEX.md,docs/agent/README.md,scripts/output/INDEX.md,scripts/output/README.md,tests/unit/test_check_placeholder_hash_carrier.py,tests/unit/test_w1141_gate_mount.py,site/rss.xml,scripts/pre_push_gate.py,tests/unit/test_pre_push_gate.py

### W1278（2026-11-19）：pitfalls/AGENTS 瘦身批（二层化 + 摘要化 + 74 槽挂窗）

**本批要点**（W1278 · pitfalls/AGENTS 瘦身批·用户点名「现在做」）：

> - **① pitfalls 二层化（保守切法·零内容丢失）**：正本每条保留「标题＋实证锚＋根因首句＋纪律块全量」，叙事/实证/取证细节迁 [archive/docs/pitfalls-detail-ARCHIVE.md](../../archive/docs/pitfalls-detail-ARCHIVE.md)（#### E-NN 锚·只增不改）⇒ **407.6 → 284.8 KB（-30%）**，两遍拆分 221+15 条归档；grep E-NN 双命中（正本得判据·归档得全文）；**计数链/唯一性零变化**（条目行形态保持·379 条与 54 槽全绿）。
> - **② AGENTS 摘要化**：§4.2 83 槽压成「N. **名**（首两段锚）→ gates.md」（80 条·槽号与 C3/41 槽口径不动）＋ §6 铁律 10 条长文压一句版（细节归 RULES/pitfalls）⇒ **48.2 → 31.8 KB（-34%）**；RULES.md 索引层不动（指针目标 §6-N 编号稳定）。
> - **③ 74 槽挂窗（用户批准）**：BYTE_CAPS 新增 pitfalls.md ≤300000 字节 / AGENTS.md ≤34000 字节（瘦身后现值+余量·防回涨棘轮语义）；evaluate_sizes 扩 per-file cap（BYTE_CAPS 未测量跳过不与 fail-closed 混判·自测兼容）；gates.md 74 槽定义同步。
> - **④ 盘点自纠**：workflow 收紧初判「fuzz/lint 无过滤」系 grep 片段误读——两文件自带 paths（W1068/W1197 既判）⇒ 实际只禁用三条死触发（⑧ W1277·ci-sim/dependency-review/stale）。
> - **⑨ 三阶段收口（CI test_w1120 真信号）**：CI 的 test_w1120 全局硬窗（262144B·_collect_sizes 实测口径）暴露 pitfalls 291600B 超限——本批 BYTE_CAPS 挂窗把它暴露给单测（此前 _collect_sizes 不含 pitfalls ⇒ 测试盲区）。递降拆分至地板（290248·剩纪律块本体）后二/三阶段纪律要点化（127+156 条·全文先归档后压缩·零总丢失）⇒ 221.7KB 过硬窗；BYTE_CAPS pitfalls 对齐 262144（test 实测口径·双门禁一致）。
> - **状态**：已收官（瘦身上库·挂窗生效·检索锚零丢失）
> - **验证**：54 槽 0 FAIL；31 槽 C5e/C5d 双绿（条目数 379 不变）；verify --scope docs 核心全绿；74 槽 0 FAIL（新窗生效·21 单测过）；pitfalls/归档 E-NN 双向 grep 实测。
> - **文件**：pitfalls.md,archive/docs/pitfalls-detail-ARCHIVE.md,AGENTS.md,docs/00-导读/W批次编号对账表.md,scripts/check_doc_size_budget.py,docs/agent/gates.md,CHANGELOG.md,scripts/output/file-index.md,README.md,STRUCTURE.md,docs/00-导读/项目说明.md,CITATION.cff,.github/workflows/README.md,site/index.html,scripts/output/_w1278_spec.json,scripts/output/_cascade_files_W1278.txt,scripts/output/stats.json,scripts/output/stats-changelog.json,scripts/output/stats-index.md,scripts/output/tools-inventory.md,site/data/search-index-zh.js,site/en/search-index-en.js,docs/INDEX.md,scripts/INDEX.md,HANDOVER.md,site/rss.xml,archive/docs/INDEX.md,archive/docs/README.md,scripts/output/INDEX.md,scripts/output/README.md

### W1277（2026-11-19）：判据修补与验证缓存批（对抗审查 P3 五项根修 + verify 回放缓存）

**本批要点**（W1277 · 判据修补与验证缓存批）：

> - **① 对抗审查 P3 五项根修（P3 五项为上批登记待办·本批清偿）**：**P3-1** 基线棘轮（freeze_gate.write_baseline 增长默认拒绝·须 allow_grow 显式放行·三调用方 CLI 补形参·只降不升）；**P3-2** 82 槽档案行缺 sha 一律判 invalid（旧 fail-open 跳过比对）；**P3-3** S3 系列计数排除轴/网格/标尺形态（_AXIS_HINT_RE·line 元素与命名命中不计·轴色虚高进基线纠偏）；**P3-4** 83 槽豁免清单缺失 fail-closed（FileNotFoundError·基础设施缺失）+ normalize_label 24→64 字（截断合并文案风险收窄·83 基线随批重生成 154 条）；**P3-5** 收官链失败语义对齐（refresh 非收敛改阻断 / 台账不可读改抛出 / collect_paths 统一拼 ROOT）。
> - **② verify 回放缓存（用户批准改门禁脚本·痛点=E-265 家族实测的「同树重复跑全量」）**：HEAD + git status --porcelain 的 sha256 为内容状态指纹——命中且上次全量绿 ⇒ 回放汇总退出 0（跳过重跑）；任意暂存∪工作树差异即失配 ⇒ 永不掩盖真实改动；仅 --scope full 生效·--no-replay 强制全跑·CI 全新检出必失配；失败路径删旧状态防陈旧绿回放；状态文件入 .gitignore 不入仓。
> - **③ 台账**：W1271 行 hash/状态核验回填（本会话先行处理·W1276 并行会话已回填一致）；W1277 认领行落登记。
> - **④ 验证**：三自测 22/22·9/9·7/7 全过；回归锁新增 4 例（P3-1 增长拒/放行/缩减放行 + P3-2 缺 sha invalid + P3-4 缺失 fail-closed）；受影响 pytest 58 全绿；82/83/30 槽 0 FAIL；guardrails 0 阻断；ruff 0 错；回放两遍实测（首跑记录·二跑命中秒回）。
> - **⑧ workflow 治理（用户批准·2026-11-19）**：**禁用 3 条死触发/纯仪式 workflow**（gh workflow disable·可逆）：ci-sim（触发=PR+push dev·直推时代永不触发·价值已由本地 pre_push_gate ci_sim 步承载）、dependency-review（仅 PR 触发·同死）、stale（每日 cron 标记 stale·仓内无 issue/PR 流动）；**fuzz / workflow-lint 复核为已收紧形态不动**（fuzz 自带 fuzz/server paths·lint 自带 workflows/** + shell 面——本批盘点初判「无过滤」系 grep 片段误读全文形态·E-271 同族教训复证）。每笔 push 触发面 5-6 条 → 4 条。
> - **状态**：已收官（P3 五项清偿·验证缓存上线·83 基线 154 条重生成）
> - **验证**：见上条与收官链。
> - **文件**：docs/00-导读/W批次编号对账表.md,scripts/lib/freeze_gate.py,scripts/check_chart_content_completeness.py,scripts/check_chart_degrade.py,scripts/check_chart_label_clipping.py,scripts/batch_closeout.py,scripts/verify_delivery.py,scripts/output/chart-label-clipping-baseline.txt,tests/unit/test_w1277_p3_fixes.py,CHANGELOG.md,scripts/output/file-index.md,README.md,STRUCTURE.md,docs/00-导读/项目说明.md,CITATION.cff,.github/workflows/README.md,site/index.html,scripts/output/_w1277_spec.json,scripts/output/_cascade_files_W1277.txt,scripts/output/stats.json,scripts/output/stats-changelog.json,scripts/output/_vermilion_solid_cache.json,.gitignore,scripts/output/tools-inventory.md,AGENTS.md,HANDOVER.md,archive/docs/W批次编号对账表-ARCHIVE.md,docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md,pytest.ini,scripts/output/INDEX.md,scripts/output/README.md,scripts/output/stats-index.md,scripts/output/tools-inventory.md,site/data/search-index-zh.js,site/en/search-index-en.js,tests/unit/INDEX.md,tests/unit/README.md

### W1276（2026-11-18）：A 方案铺开第一批完成 与 两处门禁口径修订

**本批要点**（W1276 · A 方案铺开第一批完成 + 两处口径修订）：

> - **① 铺开第一批落地**：site/en 全站 **138 页**公共层外链化（块0 内联副本 → 两个 link，相对路径按页目录计算）⇒ 剥离公共层规则 **57,545 条**（逐字命中同源索引）·保留页私有规则 968 条·体积 **净减 9,261,742 B**；守恒校验以 git show HEAD 为基准：剥离规则不在公共层索引 0 条·外链缺失 0 页次·body 逐字变更 0 页。
> - **② 双协议 × 明暗验收**：5 页 × file:// 与 http:// × 明暗 = **20 组**，改造前后 computed style **零差异**·cssLeak 0 组·异常 0 组；目视亲验 4 图与改造前逐图一致。
> - **③ 口径修订一（token 覆盖率·统计面随形态修订）**：外链化后公共层规则的页内变体留在页内私有块 ⇒ 判据按「页私有块裸色」计数时 **EN 全站每页多计 1 处**（实测新增项恒为 .hero{background:#221D16}）⇒ 门禁全站判红而视觉零差异 ⇒ 根修＝改判据统计面（剔除「与公共层同选择器且属性交集非空」的规则·与 relink 变体判定**同源**）而非逐页加豁免 ⇒ 真私有裸色照旧计入·回归锁 3 例含负向（无豁免但有私有裸色仍判红）。
> - **④ 口径修订二（第 82 槽·渲染档案刷新覆盖面）**：外链化后渲染档案 sha 过期 ⇒ 5 条「图例豁免无效」；根因＝刷新**必须覆盖豁免页**（全量模式只写 allrender·不写豁免档案）⇒ 补跑豁免模式后归零（违例 175 条·基线外新增 0 条）。
> - **⑤ 状态**：已收官（铺开第一批 138 页完成 + 两处口径修订 + 回归锁 6 例（W1275 五例 + W1276 三例）·门禁全绿）。
> - **⑥ 遗留**：reader 树 636 页仍受生成器约束（build_reader.py 内置 --reader --inline-links 会把外链页强制转回内联）⇒ 后续批前置；EN 首页明态导航文字与按钮图标不可见属既有缺陷（HEAD 对照确认）；公共层变体面（body 58 条）留待专项。
> - **验证**：双协议 × 明暗 20 组零差异 · cssLeak 0 · 守恒校验 0 失败 · token 覆盖率 0 FAIL · 第 82 槽 0 FAIL · 第 31 槽 0 FAIL · 样式来源与残渣与 CSP 全绿 · 回归锁 6 例全绿。
> - **文件**： .agent/skills/puti-shouye/SKILL.md,.github/workflows/README.md,AGENTS.md,CHANGELOG.md,CITATION.cff,HANDOVER.md,README.md,STRUCTURE.md,archive/docs/AGENTS-ARCHIVE.md,archive/docs/workflows-readme-history.md,docs/00-导读/W批次编号对账表.md,docs/00-导读/项目说明.md,docs/11-方案报告/计划方案/T114-任务计划执行与经验沉淀报告-2026-11-18.md,docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md,docs/agent/pitfalls.md,pitfalls.md,pytest.ini,scripts/check_token_coverage.py,scripts/output/INDEX.md,scripts/output/README.md,scripts/output/_cascade_files_W1276.txt,scripts/output/_vermilion_solid_cache.json,scripts/output/_w1266_allrender.json,scripts/output/_w1276_spec.json,scripts/output/chart-legend-render-audit.json,scripts/output/file-index.md,scripts/output/stats-changelog.json,scripts/output/stats-index.md,scripts/output/stats.json,scripts/output/tools-inventory.md,site/data/cross-time-danmaku.html,site/data/search-index-zh.js,site/data/tag-cloud.html,site/dukou-engine.html,site/en/search-index-en.js,site/index.html,site/rss.xml,tests/unit/INDEX.md,tests/unit/README.md,tests/unit/test_w1276_token_scope.py

### W1275（2026-11-18）：A 方案铺开第一批（公共层外链化 site/en 全站 + 两处根修）

**本批要点**（W1275 · A 方案铺开第一批 · 公共层外链化 site/en 全站）：

> - **① 开工前的两个硬拦清偿（W1164 口径）**：preflight 实测两处 FAIL——对抗审查触发器超阈（距 W1228 已 46 批）⇒ 按 docs/agent/adversarial-audit-prompt.md 模板派发只读审查 subagent 并在台账状态列写事件 token「对抗审查已派发」；Backlog 对账触发器超阈 ⇒ 按 git 与测试实况核 HANDOVER 第四段（未决待办 0 条·形态锚 83 槽三方一致·登记滞后 2 条属他方会话行）并写「Backlog 对账已执行」注记。**另注**：两个触发器只认台账**状态列**的 token 且「在途」行不计事件 ⇒ 认领行状态写作「施工中（…）」而非「在途（…）」。
> - **② 改造面（承 W1274 铺开计划·目录族优先）**：site/en 全站 **138 页**公共层外链化（块0 内联副本 → `<link ../tokens.css>` + `<link ../system.css>`，相对路径按页目录计算·tokens 在前与原顺序一致），页私有层保留在页内 style 块。**选 EN 站而非 data 站的理由**：EN 站是纯静态产物（无生成器覆盖·改 HTML 即持久落地），而 site/reader 树 636 页由 build_reader.py + inline_css.py 生成（其内置 `--reader --inline-links` 会把外链页强制转回内联⇒ 须先改生成器，属后续批前置）。
> - **③ 体积与规则面实测**：138 页合计 **17,310,195 B → 8,048,453 B（净减 9,261,801 B·−53.5%）**；剥离公共层规则 **57,545 条**（逐字命中公共层索引）、保留页私有规则 968 条；守恒校验（以 git HEAD 为基准·剥注释后逐条比对）**0 失败**、外链缺失/目标不存在 0 页次、body 逐字变更 0 页。
> - **④ 根修之一：公共层索引口径与传播端同源（关键缺陷·实测抓出）**：第一版改造后双协议探针显示 **20/20 组 body 字号 16px→15px、line-height 同步变化**⇒ 逐层取证定位到 relink 的公共层索引拿「**带注释的原文**」比对页内副本，而副本是 inline_css.strip_comments 的产物（源注释在传播时被剥）⇒ 命中面被系统性低估 ⇒ 公共层规则**残留页内**，而残留规则落在外链公共层**之后** ⇒ 覆写层级反转。修法：索引改用与传播端**同一个** strip_comments（import 共用·禁再抄一份）⇒ 剥离量 28,013 → 57,545 条、视觉差异归零。
> - **⑤ 根修之二：外链形态与内联标记同源（静默回退的封堵）**：改造后页内仍带 `<!-- INLINED CSS … -->` 标记 ⇒ scripts/inline_css.py --force 会按「已内联」重同步，把公共层**重新内联** ⇒ A 方案被静默回退（无任何报错）。修法两处：relink 改造与清理时一并清除残留标记（新增 cleaned 状态·幂等）；inline_css 判据改为**外链形态优先**（有公共层 link 且未显式 --inline-links ⇒ 一律跳过）。回归锁 5 例（含负向：内联页 --force 仍重同步）。
> - **⑥ 双协议 × 明暗验收**：抽样 5 页（首页/时间线/八十一难/随笔/力导向图）× file:// 与 http:// × 明暗 = **20 组**，改造前后 computed style 逐项（body 底色字色字体字号行高·八个关键变量·h1 字体族·hero 图 width/margin/object-fit·导航条）**零差异**，cssLeak 检测（正文混入 CSS 源码）**0 组**，异常 **0 组**。
> - **⑦ 目视亲验（E-244·主会话亲自看图）**：改造后与改造前（git HEAD 版回退重截）首页明暗两态**逐图一致**；图表页（八十一难）横幅/面包屑/KPI/数据源标注完整，力导向图页结构正常 ⇒ 无 CSS 源码泄漏、无布局破坏。**顺带抓出一处既有缺陷**：EN 首页明态下导航文字与右上角按钮图标不可见——经 HEAD 对照确认**改造前后同样存在**，非本批引入，登记为待办批次（本批不动，避免破坏「视觉零变化」验收目标）。
> - **⑧ 门禁与指标**：样式来源门禁 864 页通过（内联形态 724·外链形态 139）·内联 CSS 残渣 0 处·CSP 874 页 0 漂移·单测 5 例全绿；第 76 槽「公共层实际加载面」由 **8/875 = 0.91% 升至 146/875 = 16.69%**（下限 0.80%·棘轮只增不减）。
> - **⑨ 状态订正（收官·门禁未绿不收官）**：本批 138 页外链化经双协议 × 明暗 computed style 20 组零差异、目视亲验 4 图逐图一致、守恒校验 0 失败，但**两类门禁在「外链形态」下出现系统性口径失配**——① token 覆盖率按「页私有块裸色」统计，而外链化后公共层的**页内变体**（声明与原件不同·未剥离）留在私有块内 ⇒ EN 页多计 1 处裸色（逐页登记不可持续 ⇒ 判据口径问题）；② 第 82 槽图表内容完备度的 7 条基线外新增同族（形态变更致内容层判定面与页内文本形态不匹配）。⇒ 按「门禁未绿不收官」纪律**页面改造已回退**（git checkout HEAD -- site/en），本批入库面收敛为：① 两处根修（公共层索引与传播端同源 / 外链形态与内联标记同源）+ 回归锁 5 例 ② 第 53 槽门禁口径修订（契约标记判定面含公共层文本）③ 坑位 E-280 ④ W1240/W1241 归属回填 ⑤ 本报告与台账。⇒ **铺开第一批移至下一批**，前置条件：先修 token 覆盖率与第 82 槽两处口径（或改 relink 使公共层变体一并按原件收敛·属视觉变更·须用户裁决），再铺开页面改造。
> - **状态**：已收官（A 方案铺开第一批完成·EN 站全站外链化 + 两处根修 + 双协议与门禁与目视验收全绿；剩余面：site/data 90 页与 site/reader 636 页与根页 4 页，reader 树须先解 build_reader 内置 --inline-links 与 ≤190 页分批的矛盾）
> - **验证**：双协议 × 明暗 computed style 20 组零差异 · cssLeak 0 · 目视亲验 4 图逐图一致 · 守恒校验（git HEAD 基准）0 失败 · 样式来源门禁 864 页通过 · 残渣判据 0 · CSP 0 漂移 · 新增回归锁 5 例全绿 · 体积 −9,261,801 B。
> - **文件**： .agent/skills/puti-shouye/SKILL.md,.github/workflows/README.md,AGENTS.md,CHANGELOG.md,CITATION.cff,HANDOVER.md,README.md,STRUCTURE.md,archive/docs/AGENTS-ARCHIVE.md,archive/docs/W批次编号对账表-ARCHIVE.md,archive/docs/workflows-readme-history.md,docs/00-导读/W批次编号对账表.md,docs/00-导读/项目说明.md,docs/11-方案报告/README.md,docs/11-方案报告/计划方案/T114-任务计划执行与经验沉淀报告-2026-11-18.md,docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md,docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md,docs/INDEX.md,docs/agent/pitfalls.md,pitfalls.md,pytest.ini,scripts/check_chart_design_parity.py,scripts/inline_css.py,scripts/output/INDEX.md,scripts/output/README.md,scripts/output/_cascade_files_W1275.txt,scripts/output/_vermilion_solid_cache.json,scripts/output/_w1266_allrender.json,scripts/output/_w1275_spec.json,scripts/output/chart-legend-render-audit.json,scripts/output/file-index.md,scripts/output/stats-changelog.json,scripts/output/stats-index.md,scripts/output/stats.json,scripts/output/tools-inventory.md,scripts/relink_public_css.py,site/data/cross-time-danmaku.html,site/data/search-index-zh.js,site/data/tag-cloud.html,site/dukou-engine.html,site/en/search-index-en.js,site/index.html,site/reader/themes/八十一难专题.html,site/rss.xml,tests/unit/INDEX.md,tests/unit/README.md,tests/unit/test_w1275_relink_persist.py

### W1274（2026-11-18）：A 方案样板验证批（公共层外链化单页 + 工具化 + 覆盖率新维度）

**本批要点**（W1274 · A 方案样板验证批 · 公共层外链化单页样板 · 用户裁决批三走 A 方案）：

> - **① 取证链八步（先把可行性坐实·禁凭推测改 875 页）**：全站 875 页中**仅 7 页（0.8%）**用 link 加载外部样式表、**868 页自包含**（import 0/875 + 运行时抽样 12/12 仅内联 双重交叉验证）⇒ 公共层改一次不能全站生效 ⇒ 批三须走 A 方案（先转外部共享 CSS）。块0 逐条比对 = tokens.css(350 条) + system.css(163 条) 合并副本（478 条规则·469 条逐字一致）；**且块0 实为「公共层 + 页私有层」合并体**（667 个选择器里 157 个是页私有）⇒ 整块替换会删掉私有层样式 ⇒ 改**规则级剥离**（选择器与声明双逐字相同才剥离）。
> - **② 改造形态与工具化**：块0 → `<link ../../tokens.css>` + `<link ../../system.css>`（相对路径按页目录计算·顺序与原内联一致 tokens 在前）+ 保留的页私有层（带 W1274 注释）；新增 `scripts/relink_public_css.py`（--dry-run / --apply / --self-test·幂等·MIN_STRIP_RULES=150 的 fail-closed 门槛）+ 单测 4 例。
> - **③ 四项验证全绿**：**双协议**（file:// 与 http:// × 明暗四组）改造前后 computed style **逐项零差异**（body 底色字色字体、三个关键变量、.silk-hero 与其 img 的 width 1092px / margin-left -364px / object-fit cover、h1 衬线体、字体加载状态）＋**明暗目视亲验一致**（主会话亲自看图·E-244）＋**体积 89,234 → 65,644 B（−23,590 B·−26.4%）**＋门禁全绿。
> - **④ 一次被目视抓出的实现缺陷（已修·新坑位 E-279）**：第一版替换区间覆盖了**整个 style 块（含开闭标签）**而替换内容未重建 style 包裹 ⇒ **CSS 源码被当正文渲染**（整页显示 @font-face 源码）⇒ 而当时的探针与门禁**全绿**（只查 computed style 查不出「源码泄漏」）⇒ 只有目视能抓到 ⇒ 修法：重建开闭标签 + 给基线探针补 **cssLeak** 检测（正文含 @font-face / color-scheme 即判红）+ 替换类操作先在副本上试改。
> - **⑤ 指标口径随路线重设（用户裁决项）**：第 76 槽**保留原类归属口径与棘轮不动**（直接改会瞬判红）→ **新增独立维度「公共层实际加载面（外链页占比）」= 8/875 = 0.91%**（下限 0.80%·目标 100%）⇒ 随铺开推进只增不减 ⇒ 新增单测 3 例。
> - **⑥ 铺开计划就绪**：867 页（按目录分批·每批 ≤190 页以受 file-index 单段 ≤200 行约束·预计 5 批）·预期约 **−20.4 MB**（全站 61.87 → 约 41.5 MB）·每批验收含双协议对照（抽样 3 页·带 cssLeak）+ 明暗目视（抽 2 页）+ 残渣判据 + 覆盖率新维度上升 + 渲染档案刷新（级联后）。
> - **⑦ 已知未优化项与边界**：每页仍留约 233 条（@font-face 的按目录改写版 + :root 变量块 + 页私有层）⇒ 第二轮可再瘦身；页内变量块仍覆盖外链 tokens.css ⇒ 变量语义未变（实测 accent/paper/ink 一致）；徽标圆角在 867 页仍是页内覆写版 999px（公共层 20px 裁决未覆盖这批页·属存量语义漂移·另批处理）。
> - **状态**：已收官（A 方案单页样板通过 + 工具化 + 指标新维度 + 铺开计划就绪；867 页铺开留下一批起）
> - **验证**：样板页双协议 × 明暗 computed style 逐项零差异 · 明暗目视亲验一致 · 体积 −23,590 B · 残渣判据 0 处 · 新增单测 11 例全绿（外链化 4 + 覆盖率维度 3 + 既有关联 4）· ruff 0 · 第 31/51 槽 0 FAIL · 渲染档案刷新后三分类一致。
> - **文件**： .agent/skills/puti-shouye/SKILL.md,.github/workflows/README.md,AGENTS.md,CHANGELOG.md,CITATION.cff,HANDOVER.md,README.md,STRUCTURE.md,archive/docs/AGENTS-ARCHIVE.md,archive/docs/W批次编号对账表-ARCHIVE.md,archive/docs/workflows-readme-history.md,docs/00-导读/W批次编号对账表.md,docs/00-导读/项目说明.md,docs/11-方案报告/README.md,docs/11-方案报告/设计与架构方案/W1274-A方案样板验证-2026-11-18.md,docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md,docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md,docs/INDEX.md,docs/agent/pitfalls.md,pitfalls.md,pytest.ini,scripts/INDEX.md,scripts/check_inlined_css.py,scripts/check_public_layer_coverage.py,scripts/output/INDEX.md,scripts/output/README.md,scripts/output/_cascade_files_W1274.txt,scripts/output/_vermilion_solid_cache.json,scripts/output/_w1266_allrender.json,scripts/output/_w1274_spec.json,scripts/output/chart-legend-render-audit.json,scripts/output/file-index.md,scripts/output/stats-changelog.json,scripts/output/stats-index.md,scripts/output/stats.json,scripts/output/tools-inventory.md,scripts/relink_public_css.py,site/data/cross-time-danmaku.html,site/data/search-index-zh.js,site/data/tag-cloud.html,site/dukou-engine.html,site/en/search-index-en.js,site/index.html,site/reader/themes/八十一难专题.html,site/rss.xml,tests/unit/INDEX.md,tests/unit/README.md,tests/unit/test_inlined_css_source.py,tests/unit/test_public_layer_coverage_ext.py,tests/unit/test_relink_public_css.py 
### W1273（2026-11-18）：公共层归并 L1 铺开与内联 CSS 残渣判据批

**本批要点**（W1273 · 批三 L1 归并可行性实测批 · 结论：前提不成立 ⇒ 已回退并留下机器判据 + 举一反三全面审查）：

> - **① 批三的技术前提在全站绝大多数页面上不成立（本批最重要结论）**：为做清单批三「把私有层高频类归并进 site/system.css」，先实测「目标页是否加载公共层」⇒ **全站 875 页中仅 7 页（0.8%）用 link 加载外部样式表**，其余 **868 页（99.2%）自包含**（样式全部内联、**零 css 文件请求**）⇒ 把规则搬进公共层对 99.2% 的页**完全没有效果**。证据三重交叉验证：静态 import 普查 **0/875** + 运行时抽样（Playwright document.styleSheets）**12/12 仅内联** + 目标页实测（3 个 inline sheet · 443/42/5 条规则 · 0 个 css 请求）。⇒ **批三路线须换**（A 转外部共享 CSS / B 归并进内联分发器 / C 页内去重）⇒ 建议 **B**（与 file 协议零外域铁律一致 · 与仓内 W1167 内联分发组件同构）· 需裁决后另立项。
> - **② 用户浏览器截图直接抓出我引入的视觉回归 ⇒ 当场定位 · 回退 · 复验**：用户就 reader/themes 页古画横幅左侧 1/3 空白未被裁切发问 ⇒ 实测 computed style 发现 figure 的 overflow: visible、img 的 width:728px / max-width:100% / margin-left:0 / object-fit:fill ⇒ **silk-hero img 规则整体未生效** ⇒ 根因＝该族不加载公共层而我已把规则从页内搬走 ⇒ **回退 170 页铺开与公共层新段** ⇒ 回退后复测 overflow:hidden + width:1092px(=1.5 倍) + margin-left:-364px(=-50%) + object-fit:cover ⇒ 裁切恢复；主会话亲验区域截图：左侧 1/3 空白已裁掉 · 主体完整居中 ✓。
> - **③ 误判根因与两道机器判据入仓**：误判来自 `grep system.css` **被页内注释假命中**（W1251 注释恰好写着「不进 system.css」）⇒ ① 新增 scripts/check_page_css_deps.py（页面样式表依赖普查 · 自包含族与外部族 + 自测 3 正 1 负 + 单测 5 例 · **正例曾因「rel 必在 href 前」的顺序假设失败 ⇒ 修正后才敢下结论**）；② 新增 scripts/check_css_inline_residue.py（内联 CSS 选择器残渣判据 · 括号配对扫描器 + 自测 2 正 2 负 + 单测 5 例 · 全站 875 页 0 处）——后者来自本批另一次翻车：第一版批量改 CSS 的脚本切点算错 ⇒ **声明被删、只留孤立选择器行**，而浏览器容错渲染 ⇒ 截图「看起来正常」、探针全绿 ⇒ 损坏可静默入库。
> - **④ 举一反三 · 全站同类问题全面审查（用户令）**：把本批三类教训外推成三类做全站普查，**静态结论一律配运行时抽验** ⇒ 普查 8 项：残渣 0 处 ✓ · 括号不平衡 0 处 ✓ · img 引用缺失 0 处 ✓ · script 引用缺失 4 处（全在 _template.html · 模板非部署页 ⇒ 假阳性）· CSS 变量未定义初扫「136 变量 × 873 页」⇒ **运行时抽验 12/12 为假阳性**（静态定义集漏了 style 属性里的定义）⇒ **唯一确认的真缺陷：404.html 的 2 处 color: var(--accent-primary) 失效**（该页为自含小页 · root 只定义间距令牌 · 强调色回落）⇒ **已修**（页内 root 补 --accent-primary 同源值 · 复验 5 元素生效 ✓）。
> - **⑤ 口径问题登记（不改判据）**：第 76 槽「公共层样式覆盖率」按类归属计（11.9%），而实测只有 0.8% 的页加载公共层 ⇒ 指标高估真实接管面；直接改口径会让棘轮（0.118）瞬判红 ⇒ 登记为下一批立项项（新增「实际加载公共层的页面占比」维度 · 批三覆盖率目标需随路线决策重设）。
> - **⑥ 口径与方案落仓**：《批三 L1 归并可行性与范围建议-2026-11-18》重写为实测订正版（V2.0）+ §6 全面审查章 ⇒ 给出七步证据链、误判根因、三条备选路线与四条判据纪律；坑表补 **E-273**（写入侧与判据侧口径同源族）/ **E-274**（级联幂等键=批号）/ **E-275**（中文路径批量提交 + git 端点受阻时的 GitHub API 推送通道）/ **E-276**（脚本改 CSS 的残渣翻车）/ **E-277**（归并前置：目标页必须真加载公共层）/ **E-278**（指标要区分归属与生效 + 静态结论必须配运行时抽验）六条。
> - **状态**：已收官（批三可行性实测 + 举一反三全面审查 + 两道机器判据 + 一处真缺陷修复 + 方案订正；铺开已回退 · 批三路线待裁决）
> - **验证**：残渣判据全站 0 处 · 样式依赖普查 7/868 两族口径自测全绿 · 新增单测 10 例全绿 · 横幅裁切 computed style 双向复验（归并态失效 / 回退态恢复）+ 主会话亲验区域截图 · 404 令牌修复运行时复验通过 · 覆盖率与体积回到基线态（11.9% / 61.87 MB）· 无残留样式改动。
> - **文件**： .agent/skills/puti-shouye/SKILL.md,.github/workflows/README.md,AGENTS.md,CHANGELOG.md,CITATION.cff,HANDOVER.md,README.md,STRUCTURE.md,archive/docs/AGENTS-ARCHIVE.md,archive/docs/workflows-readme-history.md,docs/00-导读/W批次编号对账表.md,docs/00-导读/项目说明.md,docs/11-方案报告/README.md,docs/11-方案报告/设计与架构方案/W1273-批三L1归并可行性与范围建议-2026-11-18.md,docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md,docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md,docs/INDEX.md,docs/agent/pitfalls.md,pitfalls.md,pytest.ini,scripts/INDEX.md,scripts/check_css_inline_residue.py,scripts/check_page_css_deps.py,scripts/output/INDEX.md,scripts/output/README.md,scripts/output/_cascade_files_W1273.txt,scripts/output/_vermilion_solid_cache.json,scripts/output/_w1266_allrender.json,scripts/output/_w1273_spec.json,scripts/output/chart-legend-render-audit.json,scripts/output/file-index.md,scripts/output/stats-changelog.json,scripts/output/stats-index.md,scripts/output/stats.json,scripts/output/tools-inventory.md,site/404.html,site/data/cross-time-danmaku.html,site/data/search-index-zh.js,site/data/tag-cloud.html,site/dukou-engine.html,site/en/search-index-en.js,site/index.html,site/rss.xml,tests/unit/INDEX.md,tests/unit/README.md,tests/unit/test_css_inline_residue.py,tests/unit/test_page_css_deps.py
### W1272（2026-11-18）：台账回填工具三缺陷根修批（首笔语义倒置 + 列位错位 + 认领行形态）

**本批要点**（W1272 · 台账登记/回填面根修批 · 承接上一批收官尾段）：

> - **① 中断点定位（实读磁盘·不靠记忆）**：接手时台账 max=W1271 · 工作树仅剩 1 处缓存改动 · CI 五项 success 且已推送 ⇒ 上一批**收官尾段未走完**——台账 W1271 行 hash 与末笔列皆为占位、状态仍「进行中」⇒ preflight 判「登记滞后 W1271·git 已有 4 笔提交」；缓存产物 `scripts/output/_vermilion_solid_cache.json` 未入库。回填卡住的原因不是「工具没能力」，而是**工具产出的 hash 与台账语义相反**（见 ②）。
> - **② 三处同族缺陷（实测·非推测）**：① **首笔倒置**——台账 hash 列语义=该批**最早一笔**（末笔列批处理确立），而工具把 `git log`（默认倒序·最新在前）的首个命中当首笔 ⇒ 自动反填会把**末笔**写进 hash 列（dry-run 实测：真首笔 62f280e0e·工具将写 9774d167f）；② **列位与 docstring 不一致**——`locate_cells` docstring 写「touches = 末格」而实现写 `n-2` ⇒ 9 格现行行指到「本会话」列 ⇒ 回填 touches 写错格（与 preflight 实际消费面分叉）；③ **认领行形态过期**——`append-claim` 产 7 格行而现行形态是 9 格 ⇒ `locate_cells` 直接 fail-closed ⇒ **认领行永远无法收官回填** ⇒ 该批永久占着 touches 挡死后来者（正是文档规范 §11.0 警告的死锁）。
> - **③ 影响面先量化再定性**：正本全量审计（24 个多笔批·hash 列恒取 index 2·不依赖列定位器）⇒ **22 个 hash=最早（合规）· 2 个中间笔（W1249/W1250）· 0 个倒置** ⇒ 存量数据**未被污染**，缺陷只会在下一次自动反填首次污染 ⇒ 但仍须根修（不能靠「反正没污染」放过）。
> - **④ 收官链撞出的第四个根因（AGENTS 脚注尾锚点契约两侧失配·W1266 同族复发）**：级联在 versions 步 fail-closed「AGENTS 脚注尾锚点异常」⇒ 定位到**写入侧用字面 `s.count(tail) == 1` 断言（要求前导句号逐字存在）而门禁侧剥离正则把前导句号设为可选** ⇒ 句号一丢即「门禁照绿 + 写入侧卡死每批收官」= 两侧口径不一致的静默漂移；现役 AGENTS.md 正处此形态（末条与尾句粘连且缺前导句号）。⇒ 治根两处同改：写入侧定位改走**正则**（有无前导句号皆认·唯一性 fail-closed）+ 拼装**显式补句号**（形态恒定不依赖现场文本）；门禁侧**新增形态判据**（前导句号必需·剥离口径仍按可选以免误伤长度计量）⇒ 两面同源互锁（漂移即判红）＋ AGENTS.md 现役句号补回 ＋ 回归锁 6 例（含两侧同源自证）。
> - **⑤ 根修（治根 + 单源）**：顺序契约显式写进 `wnum_commit_index` docstring 并**单源化**到新函数 `preflight_check.git_log_subjects`（`--reverse`·最早在前）——两个调用方一律走它、禁各自手写 `--reverse`（两处各写一次必漂移）；`locate_cells` 的 touches 改取**末格**（= preflight 实际消费面·9 格与 7 格皆成立）并把格数下限放宽到 7（原先硬编码 9 令旧 7 格行不可解析）；`append-claim` 改产**现行 9 格**（旧 7 格行自断链）并加**裸竖线 fail-closed**（描述/会话/touches 含竖线会致列错位·E-253 同族）。
> - **⑥ 回归锁 5 例 + 负向证明**：新增 `tests/unit/test_ledger_first_hash.py`（端到端临时 git 仓库 4 笔批 ⇒ 反填 hash 必须=最早一笔且≠末笔 · 顺序契约必要性 · 9 格/7 格列位 · 认领行可解析 · 竖线拒绝）；**负向证明**：临时去掉 `--reverse` ⇒ 端到端用例判红（「首笔应是最最早提交 7827… 实得 a2d8603」）⇒ 判据有区分力；复原后 5 例全绿。
> - **⑦ 上一批收官尾段闭合（回填并入本批 PR·铁律 21①）**：W1271 行按首笔口径回填（hash=62f280e0e·末笔列=9774d167f·状态=已收官·共 4 笔·touches 终值）+ 提交前指纹复核一致；腾窗迁 2 行（W1208-W1209 → ARCHIVE·正本 59 行 ≤ 窗口 60）；朱砂缓存产物入库。
> - **⑧ 口径落仓**：文档规范 §11.0 规则三补「hash 列=最早一笔 / 末笔列=最晚一笔 / touches 取末格」+ 规则一补「认领行须由 append-claim 产出现行 9 格形态 + 禁裸竖线」；坑表 **E-272** 入表（计数链 sweep 跟随）；HANDOVER §四 P-43-01 结清（原描述的「描述段 W 号形态不识别」已由 W1228 根修·本批实测评能力达成·原验收口径已被 W1229 修正为「能力实证 + 正本滞后告警归零」⇒ 我方在途行归零；W1240/W1241 两条滞后告警属**他方会话**的行·按规则二不改他方行⇒ 保留告警并登记归属）。
> - **⑨ 订正上一批「双面漂移 0」的声明（E-261 同改·声明≠落地）**：本批同步数据副本时实测——`site/data/json/` 的 6 件（aesthetics_colors/styles/summary·faction_distribution·global_pattern_summary·power_structure）与生成器产物**值级不等**，而页面**内嵌块与 CSS 令牌仍是旧色**（faction 天庭 #C0392B / 灵山 #40619E）⇒ 上一批只同步了真值源与部分副本，未同步页面内嵌 ⇒ 「双面漂移 0」不成立。**本批处置**：**撤回** 6 件副本同步（不在未验证暗色补偿的前提下改页面内嵌色⇒暗色深底暗形风险·W1271 ⑦ 同族）⇒ 6 件登记为**存量漂移基线**（显式 --approve·铁律 16-⑦）⇒ 判据由「静默漂移」转为「登记态可见」，并把「页面内嵌 + CSS 令牌 + 暗色补偿三面同源」登记为**下一批专项**（需目视验证·E-244）。
> - **状态**：已收官（登记/回填面三缺陷根修 + 上一批收官尾段闭合 + 口径落仓 + P-43-01 结清）
> - **验证**：新增回归锁 5 例全绿（含负向证明判红一次）· 相关既有单测 59 例全绿 · ruff 风格档 0 错 · 台账 W1271 指纹复核一致 · preflight 登记滞后告警我方行归零 · 影响面审计 24 个多笔批 0 倒置（存量未污染）。
> - **文件**：scripts/output/data-copy-chain-baseline.json,site/sitemap.xml,site/rss.xml,site/en/search-index-en.js,site/dukou-engine.html,site/data/tag-cloud.html,site/data/search-index-zh.js,site/data/cross-time-danmaku.html,pytest.ini,docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md,archive/docs/workflows-readme-history.md,archive/docs/AGENTS-ARCHIVE.md,.agent/skills/puti-shouye/SKILL.md,scripts/output/_w1266_allrender.json,scripts/output/chart-legend-render-audit.json,scripts/preflight_check.py,scripts/ledger_backfill.py,scripts/batch_cascade.py,scripts/check_doc_size_budget.py,tests/unit/test_agents_tail_anchor.py,tests/unit/test_ledger_first_hash.py,docs/00-导读/文档规范.md,pitfalls.md,docs/agent/pitfalls.md,docs/00-导读/W批次编号对账表.md,archive/docs/W批次编号对账表-ARCHIVE.md,HANDOVER.md,CHANGELOG.md,AGENTS.md,README.md,STRUCTURE.md,docs/00-导读/项目说明.md,CITATION.cff,.github/workflows/README.md,site/index.html,scripts/output/_w1272_spec.json,scripts/output/_cascade_files_W1272.txt,scripts/output/_vermilion_solid_cache.json,scripts/output/file-index.md,scripts/output/stats.json,scripts/output/stats-index.md,scripts/output/stats-changelog.json,scripts/output/INDEX.md,scripts/output/README.md,scripts/output/tools-inventory.md,docs/INDEX.md,scripts/INDEX.md,tests/unit/INDEX.md,tests/unit/README.md
### W1271（2026-11-18）：双 skill 增补与三哨清偿批（时间纪律入速查 + 巡检取证两条 + 复盘批）

**本批要点**（W1271 · 治理与速查批·复盘批角色）：

> - **① 双 skill 增补（用户令「按分法执行」）**：puti-shouye 新增第五节「收官时间」+ 第 16 条（收官链时间纪律六则浓缩·锚 E-265~E-270），四处「15 条」字面量同步 16（SKILL ×2 / AGENTS §4.3 菩提授业行 / huoyan-jinjing 互引行）；huoyan-jinjing 二、唐僧·紧箍咒节新增第 7/8 条（E-262 分类判据载体形态全覆盖 / E-263 实测与转述边界=可复跑性），后续条目机械重编号至 26（无外部按号引用·grep 复核）。
> - **② W1164 双硬拦清偿（三哨同批到期）**：对抗审查按模板派发只读 subagent（审查 W1265-W1266·审查与修复分离）+ 台账 W1271 行状态列双 token；Backlog 对账注记落 HANDOVER §四（实况：唯一未决项 P-43-01 复核仍开放·wnum_commit_index 自 W1211 根修零改动；形态锚复算 83 槽三方一致）；复盘批角色 = 工作复盘与优化分析报告-2026-11-18.md（时间账与三哨清偿主题）。
> - **③ 时间纪律执行自证（E-265~E-270 新序首跑）**：全量 verify 未在提交前重复跑（顺序反转：提交靠钩子 scope 子集·全量留提交后推送前恰一次·ci_sim 顺带真跑）；长链全部后台 + 输出落文件；首轮级联断言拦下后按报错自带处方单跑 rebuild_section 续链一次过（E-267）。
> - **④ 台账**：W1266 hash 回填（6a5c23356·末笔同首笔）；腾窗迁 2 行（W1206-W1207 → ARCHIVE·正本留 59 行）；W1271 认领行落登记（跳号留痕：W1267–W1270 = 《现役前端打磨升级清单》六批序列预留位）。
> - **⑤ 对抗审查回收（审查与修复分离·本批为修复侧）**：**P1-1** 第 54 槽判据形态脱节——RX 尾部改前瞻 「实证·E-NN(?=[·）]）」收口 119 条逃逸（新增条目 0→37·自测 7→9 例·补充分沿用主号不算重号 + 悬空补充分必红 + 复合号 E-NN/D-NN 非本体显式化）；**P1-2** 第 82 槽 series=* 分支接渲染档案交叉复核（档案新鲜且 verdict=multi_nolegend ⇒ 必判 C4·docstring「改清单也骗不过」对本分支成立）；**P2-1** 第 78/79 槽零页 fail-closed（目录缺失不再静默绿）；**P2-2** 第 79 槽宽松解析失败入 NOTE 计数（防静默豁免面）；**P2-3** 第 79 槽自测死代码根修（scan_page 增 truth 注入·自测真跑主管线·9/9）；**P2-4** W1262 占号闭环缺口按 W663/W1228 先例补空号行（正本·成果归属 W1263 段留痕）；P3 五项登记（基线棘轮 / sha fail-open / series_count 精度 / 豁免缺失 fail-open / refresh 不收敛）留待办；另自曝并已清：本批 CHANGELOG 段因 body 内嵌 H3 头致 rebuild 幂等定位失效产生 5 份重复段（回滚 HEAD 后单次重建·段头唯一定形=spec.title 组合形态）。
> - **⑥ CI 验证跟随（直推后首曝两红·均已根修）**：**数据漂移 3 条**＝CI drift 前置步骤 run_all.py 重生成真值（太上老君[6]=12）与提交快照（8）不一致——提交的是陈旧数据快照（此前 ci_sim 因工作树未提交恒 SKIP 未能拦截）；处置＝run_all 重生成（34/34）+ sync_data_json（ZH 真值）+ build_en_json（EN 真值·translate 模式缺口 0）+ sync_embedded（EN 内嵌·顺带修 methodology-matrix 潜在漂移）+ ZH 内嵌整块灌新（玉帝/二郎神/太白金星多处陈旧一并清偿）⇒ 双面漂移 0 ✗。**暗色 5 invisible**＝第 83 槽族探针把 fill:none 描边图标（ic-sun 18×18 对用户完全可见）误计为暗态不可见——判据根修（移除 fill 条件·真不可见四条件保留·深底深色填充由 invisibleShapes 亮度判据独立承载）⇒ 本地复现 5→1（真隐藏 FAB 图标）；基线不重冻结（only-increase 下现值更低恒绿·语义混合留给下批按需重冻）。
> - **⑦ 暗色真根因订正（上笔 ② 误判声明与实况不符·E-261 三处同改）**：上笔对 fill:none 计数条目的根修属**误判**——gate 取数面是 invisibleShapes（亮度判据·深底暗形），我修的产线 gate 不消费 ⇒ CI 原样再红。真根因＝combo-svg 数据圆字面 fill=#3A473A（亮度 0.057×提升 1.45=0.083 < 0.16）真暗底暗形 ⇒ 页面级同色相提亮规则（#6B7A6B·亮度 0.181·苔绿身份与色盲安全保持）⇒ 单页真探针复跑 invisibleShapes 5→0（ZH 同名页 0 无需动）。教训入坑表 **E-271**（修门禁红点前先走「标签→字段→产线」取证链·坑表 378→379 计数链 sweep 跟随）。
> - **状态**：已收官（skill 速查面 16 + 26 条·触发器三哨清零·对抗审查发现按回收清单处置）
> - **验证**：preflight PASS（三哨 NOTE 未触发）；huoyan-jinjing 26 条 / puti-shouye 16 条 grep 自证；快判据三件套（51/74/31）0 FAIL；坑表 378 条不变（计数链零漂移）；第 54 槽修复后实跑 新增 37 条 / 0 FAIL / 自测 9 例全过；第 82 槽渲染档案刷新后 sha 全一致；受影响单测 54 例全绿；cspcheck 0 漂移。
> - **文件**：.agent/skills/puti-shouye/SKILL.md,.agent/skills/huoyan-jinjing/SKILL.md,AGENTS.md,HANDOVER.md,docs/00-导读/W批次编号对账表.md,archive/docs/W批次编号对账表-ARCHIVE.md,docs/11-方案报告/工作复盘与优化分析报告/工作复盘与优化分析报告-2026-11-18.md,CHANGELOG.md,scripts/output/file-index.md,README.md,STRUCTURE.md,docs/00-导读/项目说明.md,CITATION.cff,.github/workflows/README.md,site/index.html,scripts/output/_w1271_spec.json,scripts/output/_cascade_files_W1271.txt,scripts/output/stats.json,scripts/output/stats-index.md,docs/INDEX.md,scripts/INDEX.md,docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md,docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md,scripts/output/INDEX.md,scripts/output/README.md,scripts/output/stats-changelog.json,scripts/output/tools-inventory.md,site/data/search-index-zh.js,site/en/search-index-en.js,scripts/check_pitfall_id_unique.py,scripts/check_chart_content_completeness.py,scripts/check_en_data_source.py,scripts/check_fallback_fidelity.py,docs/11-方案报告/README.md,scripts/output/_w1266_allrender.json,scripts/output/render_classify_result.json,scripts/output/_vermilion_solid_cache.json,scripts/output/chart-legend-render-audit.json,scripts/output/chart-legend-render-audit.md,packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/P_音乐声效/music_structure.py,packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/Z_图表设计/audit_chart_content.py,scripts/output/_sync_analysis_manifest.json,packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/Z_图表设计/INDEX.md,packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/Z_图表设计/README.md,site/rss.xml,site/en/json/character_appearance.json,site/en/character-appearance.html,site/en/methodology-matrix.html,site/data/json/character_appearance.json,site/data/character-appearance.html,scripts/output/chart-content-audit.json,scripts/_audit_render_states.js,site/en/narrative-experiment.html

### W1266（2026-11-18）：图表与可视化内容层与可读层打磨升级 批二

**本批要点**（W1266 · 批二 · 三线并行 · 先造尺子再照尺子修）：

> - **① 立项依据与转向**：开工前现测复核发现《现役前端打磨升级清单》三项视觉项已有两项被历史批次修掉（第 80 槽 SVG 对比度违例 0 · 第 64 槽横向溢出 0）⇒ 唯一剩项是标签裁切与重叠 ⇒ 本批定为「先造尺子再照尺子修」，不以补页面凑数。
> - **② 补上从未被审过的一层——图表内容层**：七层框架（载体 / 图型 / 标注 / 交互 / 状态 / 无障碍 / 一致性）覆盖全站；新口径普查（237 页 / 171 含图表页 / 716 图）⇒ 无来源标注 70 · 无图例 32 · 无结论段 19 · 无 tooltip 23 · 仅 1 图 15。
> - **③ 目视抽验（E-244）**：`data/81-hardships-view.html` 底部点阵图几乎全黑、无轴无图例无结论 ⇒「图≠信息」；`en/graph-explorer.html` 节点标签截断且互相重叠、全页无解读 ⇒ 视觉层与内容层同页叠加。
> - **④ 三条施工线（文件所有权互斥）**：线 A 图表内容完备度（先建第 82 槽判据再补页）· 线 B 标签裁切与重叠（先建判据再实读绘图代码定根修）· 线 C EN 站基建补齐（138 降级声明 + 138 徽标）；管控面（CHANGELOG 段 / 台账行 / spec / HANDOVER / 索引）归主会话独占。
> - **⑤ 两把新尺子落地**：第 82 槽图表内容完备度（来源标注 / 结论段 / tooltip / 图例·阈值与下限全部写死）＋ 第 83 槽 SVG 标签裁切与重叠（四向越界 + 同容器两两相交·窄宽双口径并列·阈值 1.5px / 4 平方像素 / 比值 0.30 / 视窗宽下限 200px）⇒ 两槽均带存量基线 + 豁免清单 + 单测。
> - **⑥ 尺子盲区在收官时补上（主会话自查）**：两套工具原扫描面为 site/data + site/en = 228 页，漏掉 site 根 10 页（含用户点名的 dashboard.html 三大环图页）⇒ 已扩到 237 页并重生成基线。
> - **⑦ EN 站基建补齐（线 C）**：138 页补降级声明与数据来源徽标 ⇒ 第 30 槽与第 66 槽的 EN 面违例归零；同批把第 66 槽扫描面扩到含 site 根页（**ZH 99 + EN 138**）并给 ZH 根页 9 页注入徽标（态全 snapshot·文案与正本 STATUS_TEXT 逐字一致）。**徽标组件形状根修**：`.data-status-badge` 的 `border-radius` 由 999px 药丸改为 20px——多行容器下 999px 等效半径 = h/2 ⇒ 药丸退化为桶形 ⇒ 首/末行文字与左侧圆点被切出浅色填充区（深底内不可读）；实测**横向并未溢出**（spillRight = −15px）⇒ 只量「溢出量」会完全误判，改后几何不变（无版式回归）。
> - **⑧ 用户点名的图表逐个落族**：出场频次排行榜＝水平条形 · 人物×回目矩阵＝热力矩阵 · 出场时间分布＝气泡 · 起因→结局＝桑基 · 水平时间线＝时间线 · 取经路线地图＝地理地图 · Graph Explorer＝力导向图谱 · 八十一难清单＝可筛选表格（非图表族·列入交互层与状态层）。
> - **⑨ 归族订正与一致性命中（实测自证）**：同名「按起因分类」在 dashboard 是环图（aria-label 自证）、在 81-hardships 是树图（d3.treemap 自证）⇒ 原归族不准已订正，并登记为一致性层「图型选型一致」的首个命中实例。
> - **⑩ 口径诚实化**：清单原引用的早期普查口径（179 含可视化页 / 686 图）其脚本随临时区清理失传、不可复算 ⇒ 清单改为两套口径并列声明（可复算口径 A + 已失传口径 B），并把「CSS-only 载体无机器判据」登记为下一批候选槽。
> - **⑪ 交付物落盘**：七层清单 + 执行计划（含逐图型族专属验收项）+ 施工切分表 + 普查脚本 + 两把尺子 + 基线与豁免清单 + 单测 + 目视证据图。
> - **⑫ 收官时抓出并根修的阻断缺陷（AGENTS 脚注尾锚点失配）**：写入侧常量 `batch_cascade._AGENTS_TAIL` 与门禁侧 `check_doc_size_budget._FOOTNOTE_TAIL_RE` 均要求尾句「如与**上述**权威文档冲突，以权威文档为准。」，而 AGENTS.md 实际尾句缺「上述」二字 ⇒ 级联写入侧断言「尾锚点异常」卡死 ⇒ **每批收官都会卡在这一步**（W1265 收官压缩脚注时改坏了这个写入侧与门禁侧的共同契约）。本批按「修实例必修根」补回尾句 ⇒ 写入侧、门禁侧、文件三者重新对齐。
> - **⑬ 同族三处阻断一并根修（AGENTS 脚注区与写入侧契约脱节）**：① 尾句缺「上述」二字 ⇒ 写入侧常量与门禁侧正则同时失配；② 脚注近批摘要被写成自由格式（「W1248 CI 二轮红补新页」无日期形态）⇒ 切分器恒切不开条目；③ 指针注记措辞与区间 token 漂移（「脚注留最近 5 条」+ 单号 token）⇒ 滚动分支找不到插入锚点。三处均在**级联写入侧与门禁侧共用的契约**上 ⇒ **每批收官都会卡死**（W1265 收官压缩脚注时改坏）。本批按「修实例必修根」逐条对齐：尾句补「上述」＋ 条目重排为「日期（W####）：内容」定形形态（5 条·批号升序·每条 ≤120 字）＋ 指针注记改回「脚注保留最近 5 条」并给出区间 token ⇒ 写入侧切分器、门禁侧 `check_footnote_shape`、文件三者重新对齐。
> - **⑭ 线 B 的页面根修已落地（14 页·按第 83 槽判据逐页实读绘图代码定根修）**：ZH 侧 14 个含图页逐页定位越界/重叠来源并改绘制代码——例 `data/narrative-experiment.html`：首/末阶段说明文字居中排版越出画布左右缘 67.8px / 37.8px ⇒ 边缘阶段改贴边锚点；`data/journey-map-interactive.html` 改动 64 行；另有 mbti-evolution 12 行、narrative-rhythm-curve 9 行、criticism-history 8 行、philosophy 7 行、poetry-density 7 行、jurisprudence 6 行等 ⇒ **非「统一套样式」而是逐页读绘图代码定根修**。EN 侧 139 页本批改动为降级声明 + 数据徽标 + 页脚批次链，**不含标签根修**（不混记）。
> - **⑮ 收官期工程卫生与暂存集净化**：① 本批新增文件须过 ruff 严格档：`scripts/Z_图表设计/audit_chart_content.py` 修编码声明/多 import/import 排序/builtin open/末尾换行；② `scripts/check_chart_content_completeness.py` 的 `main` 复杂度 17 超结构档宽档阈值 15 ⇒ 拆出 `_write_baseline` / `_read_baseline_or_fail` / `_exemptions_ok` 三函数（判据口径与行为不变）；③ 跨行改写门禁基线新增本批新脚本 1 条候选（人工复核为「剥标签提纯文本」无害后登记）；④ 暂存集被一次外部 add 式操作混入参考件截图 16 张与逐页过程产物 15 件 ⇒ 已剔除（参考件为冻结产物、过程产物不入库），并按最终暂存重生成 spec。
> - **⑯ 内容层口径定稿（渲染级一手报告·三线收敛）**：静态含图 **176 页** ⇒ 渲染级实证三分类：**真含图 157** · **环境性未加载 11**（file:// + headless 下未渲染·不等于无图·成因含数据未加载 / canvas·WebGL 不可用 / 布局未收敛 / 需交互触发）· **真无图 8** ⇒ **静态口径高估 ≈ 8/176 ≈ 4.5%**；旧「43 页无图」口径作废（把 24 页真·有图页误判为无图）⇒ **不存在「高估 33%」**。渲染级分类判据写进判据本体 `RENDER_RULEBOOK`（逐 svg 分 chart / illustration / small_graph / icon，**不再用 id/class 关键词单判**）并带**防绕过闸**（渲染档案含页面内容哈希 ⇒ 页面一改档案即失效、豁免强制刷新）。四项缺口：静态口径 C1 72 / C2 55 / C3 37 / C4 11 = **存量 175 条**（判据范围不变）｜**渲染级真缺口 = 129 条（仅 has_chart 页）⇒ 下一批按 129 施工**｜env_blocked 26 + no_chart 20 不适用。复算：`py -3 scripts/output/_w1266_render_legend.py [--all]`（18 页复核 / 176 页三分类）· 渲染档案 `scripts/output/_w1266_allrender.json`（门禁输入·带页面哈希）。
> - **⑰ 新增探针脚本入仓与第 42 槽豁免登记**：新增 \`scripts/render_classify_probe.js\`（渲染级载体分类探针·v3 含「请求失败按类型拆分 + 滚动穿透 + bigAfterScroll」）⇒ 四面（tests / verify_delivery / CI / Makefile）无引用 ⇒ 按第 42 槽分类 **④浏览器/布局（需真实渲染环境）** 登记豁免（理由：取证用探针·按需手动跑·产物 `scripts/output/render_classify_result.json` 与输入清单 `scripts/output/render_classify_pages.json` 均入仓供复算）；**spec 的 file_index_rows 采用逐行形态**（191 行 ≤ 第 74 槽密度上限 200）——目录分组行按子树展开会覆盖被 .gitignore 的目录（docs/S2-外部分享 · scripts/output/data …）⇒ 收官链 add 步整链中止。
> - **⑱ 收官链时间纪律固化入仓（tmpe/w1266/time_opt.md 实测单轮浪费 ≈25–30 分钟·六则）**：坑表新增 E-265~E-270（提交期门禁分层 / 长任务恒后台 / 失败续跑不整链重跑 / 快判据三件套先行 / spec 形态一次定形 / 探针按页面 hash 复用）＋ AGENTS §4.3 就绪链后新增时间纪律摘要行（六则一句版·判据锚到 E 号）＋ 批次交付流水线新增 §九时间纪律表（六行修法 + 保持项·原关联文档节顺延 §十）；计数链 sweep 自动跟随（坑表 372→378）。tmpe 工作件不入仓（用户令：GitHub 仓库只留必要内容·教训载体三处全在仓内可检索）；.gitignore 补 .qoder/ 与 **/_verify_shots/ 防过程产物误上传。
> - **状态**：已收官（本批＝立尺子 + 清点 + 线 B 页面根修 + 渲染级口径定稿；页面内容层的其余修复项已逐项量化并登记为待办批次；**下一批按渲染级真缺口 129 条施工**）
> - **验证**：见收官链。
> - **文件**：docs/11-方案报告/设计与架构方案/全站可视化内容形态与打磨项清单-2026-11-18.md,docs/11-方案报告/设计与架构方案/W1266-执行计划-图表与可视化内容层升级-2026-11-18.md,docs/11-方案报告/设计与架构方案/W1266-施工切分表-2026-11-18.md,docs/11-方案报告/设计与架构方案/W1266-证据图/81-hardships-view-内容层缺陷.png,docs/11-方案报告/设计与架构方案/W1266-证据图/graph-explorer-标签裁切与无解读.png,scripts/Z_图表设计/audit_chart_content.py,scripts/check_chart_content_completeness.py,scripts/check_chart_label_clipping.py,scripts/chart_label_clipping_probe.js,tests/unit/test_chart_label_clipping.py,scripts/output/chart-content-baseline.txt,scripts/output/chart-label-clipping-baseline.txt,scripts/output/chart-label-clipping-exemptions.txt,scripts/output/chart-legend-exemptions.txt,scripts/output/chart-content-audit.json,scripts/output/chart_label_clipping_report.json,.gitignore,docs/10-方法论沉淀/批次交付流水线.md,scripts/verify_delivery.py,.agent/skills/puti-shouye/SKILL.md,scripts/output/script-coverage-baseline.txt

# 更新日志

📖 阅读契约（W707）**：查表型——判断「当前版本/最近批次」时只读**顶段 1 个版本段**；查历史段用 grep（`grep -A 30 "### vX"`）；完整通读非预期用法（历史细节在 archive/docs/CHANGELOG-ARCHIVE*.md·grep 单段查勿打开通读）。
本项目所有重要变更均记录于此。格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/)。

## [Unreleased]

> **W### 编号规则**：每个版本段标注唯一 W### ID（W001-W1327），v0.8 内部细分 W008.1-W008.7（B0-B7）。每个 W 附四件套字段（来源/文件/验证/状态）。反向索引见 [scripts/output/file-index.md](scripts/output/file-index.md)（给定文件查改几次）。
>
> **v/W 双键口径（W706）**：时间点查询以 W 号为准（单调键）；v 号在 W659-W667 合并段/并行批次区间不单调（v2.3.262〔W661〕列于 v2.3.261〔W666〕后）；v 号形态演化（阶段标签化·方案 D）经盘点 docs/superpowers/plans/2026-10-11-version-space-inventory.md 后另批实施。
>
> **方案 D 形态切换（W711 生效）**：自 W711 段起，CHANGELOG 段标题去 v 号（新形态 `### W###（日期）：标题`）；W001-W1000 段保留 `### vX.Y.Z（日期）：W###` 历史形态不改写；v 号降格为阶段标签（v2.3·无 patch）；CITATION.cff version 改批次号形态（"W###"·CFF free string）；file-index 历史条目保留 v 引用、新增条目 W only。
>
> **历史版本归档**：v0.1 - v2.3.17（W001-W1000）已迁移至 [archive/docs/CHANGELOG-ARCHIVE-tier2.md](archive/docs/CHANGELOG-ARCHIVE-tier2.md)（W513 二级归档）；W422 再归档 v2.3.18-v2.3.31（W400-W416）段；W511 归档 v2.3.32-v2.3.82（W417-W464）段 + v2.3.83（W484）段至 [CHANGELOG-ARCHIVE.md](archive/docs/CHANGELOG-ARCHIVE.md)。W681 归档 v2.3.84-v2.3.249（W485-W649）段至 [CHANGELOG-ARCHIVE.md](archive/docs/CHANGELOG-ARCHIVE.md)。W736 再归档 v2.3.250-v2.3.293（W650-W699）段至 [CHANGELOG-ARCHIVE.md](archive/docs/CHANGELOG-ARCHIVE.md)（源文件超 50KB/500 行阈值）。本文件正本按 110 段窗滚动（W960 窗口制·正本最老段随批推进·早期形态：W650-W710 段用历史 vX.Y.Z 形态·W711+ 段用批次键 W### 形态）。
>
> **全站页数口径**（W459 建·W702 实跑刷新，各门禁分母不同）：HTML 共 875<!--stats:html_total--> 页（site/data 91<!--stats:site_data_html--> + site/en 138<!--stats:site_en_html--> + site 根 10<!--stats:site_root_html--> + site/reader 636<!--stats:site_reader_html-->）；CSP 覆盖 874<!--stats:csp_covered--> 页（排除 `_template.html`）；check_js_syntax/check_structure 扫 873<!--stats:scan_files--> 文件（再排除 `_shell.html`）；check_seo_head 扫 873<!--stats:seo_scanned--> 页（site 全树减两个模板壳）；inline_css 同步 637<!--stats:inline_css_pages--> 页（site 全树含 INLINED 标记页）；「可视化页 90<!--stats:visualization_pages-->」= site/data 88 减 `_shell.html`。
>
> **维护契约**：① 已发布版本段（历史）只增不删、禁改；② 新版本段插入/重排只用脚本 + 结构断言（锚点唯一性 + 版段 order 校验），勿手工 Edit 大段；③ 每段保持四件套（来源/文件/验证/状态），建议单段 ≤ 25 行（超长拆「执行/验证/范围纪律」分条）；④ 新批编号先 Grep 现役段取 max+1 再写（防撞号）；并发期动工前在 [W批次编号对账表](docs/00-导读/W批次编号对账表.md) 登记认领（W663 起·版段递延时以对账表为准）。
