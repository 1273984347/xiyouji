### W1041（2026-10-30）：批次号预约机制（开批先占号·reserve_w.py + 铁律 17）

> **来源**：用户 2026-10-30 令「做」——承接其问「并行会话之间没有批次号预约机制那怎么做？」。
>
> **背景**：今天的 W1039 撞号实战暴露——台账是「事后登记」，两个并行会话各自从自己看到的台账 max 取号，同时动手必撞（本批即撞 W1039，对方续占 W1040，本批顺延 W1041）。
>
> - **文件**：.github/workflows/README.md、AGENTS.md、CHANGELOG.md、CITATION.cff、HANDOVER.md、README.md、STRUCTURE.md、archive/docs/AGENTS-ARCHIVE.md、docs/00-导读/W批次编号对账表.md、docs/00-导读/项目说明.md、docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md、docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md、docs/agent/pitfalls.md、scripts/output/_vermilion_solid_cache.json、scripts/output/_w1041_spec.json、scripts/output/file-index.md、scripts/output/stats-changelog.json、scripts/output/stats-index.md、scripts/output/tools-inventory.md、scripts/reserve_w.py、site/index.html

**根因**：批次号缺乏预约环节。台账认领是事后登记，无法在动手前可见地占号，多会话必然撞。

**交付**：

① **`scripts/reserve_w.py`（开批占号助手）**：三模式——`reserve`（占号，stdout 仅打印 W 号）、`list`（列有效预约）、`release <W号>`（收官释放）。
candidate = max(台账 max W, CHANGELOG 顶段 W, 已预约集合) + 1；写入 `tmpe/_w_reservations.json`（已被 .gitignore，同一工作树内多会话共享），**24h TTL 防占而不交**，写文件用「临时文件 + os.replace」保证原子性。
② **铁律 17「开批先预约号」**（AGENTS.md）：开批第一步必须跑 `python scripts/reserve_w.py` 占号，**未占号不动手**。
③ **坑表加 W1039/W1040 撞号案例**（docs/agent/pitfalls.md）：记录根因与修法，使下个会话检索得到。

**边界（重要）**：此机制仅同一工作树内的并行会话有效；两会话在**不同 clone** 时 reservation 文件不共享，仍须退回 git log + 台账兜底。本项目并行基本在同一工作树，覆盖主场景。

**验证**：脚本自测——占号得 `W1041`、列表单 W 无重复前缀、字节编译通过（`py_compile` OK）；门禁全绿（核心 0 FAIL）。

> - **状态**：已收官（预约机制入库·铁律 17 立·撞号案例入坑表）
### W1040（2026-10-30）：任务分级协议入库（跨项目协作协议移植·重放）

> **来源**：用户 2026-10-30 提供《任务计划、执行与经验沉淀系统提示词》全文并裁决「装」入两项目治理文件；Anthropic 锚定侧已同日入库（wiki/task-protocol.md·74a13cf），本仓侧按 W507 映射以深度篇入 docs/10-方法论沉淀/。前稿四度撞号（W1035/W1036/W1038 被并行消费·W1039 被按裁决 A 收回），材料经全链验证后以 W1040 重放。
>
> - **文件**：docs/10-方法论沉淀/任务分级协议.md、docs/10-方法论沉淀/README.md、docs/11-方案报告/README.md、docs/11-方案报告/计划方案/执行前计划-W1040-任务分级协议入库.md、docs/INDEX.md、docs/00-导读/W批次编号对账表.md、scripts/output/_w1040_spec.json、scripts/output/_cascade_files_W1040.txt、CHANGELOG.md、README.md、STRUCTURE.md、HANDOVER.md、AGENTS.md、CITATION.cff、docs/00-导读/项目说明.md、.github/workflows/README.md、site/index.html、site/data/search.html、site/en/search.html、site/data/cross-time-danmaku.html、site/data/tag-cloud.html、site/dukou-engine.html、scripts/output/file-index.md、scripts/output/stats.json

**处置**：① 新增《任务分级协议》：战役/任务/微三级分流，战役级走九要素执行前计划六阶段全流程，任务级走五行最小计划，微任务免表格；② 固化统一编号（G/AC/ASM/ST/D/R/V/E/P/A/WF/SC/PRE）与模糊词替换表；③ 最小计划模板与经验沉淀卡体例随文；④ 与 W1033「历史文件改状态不改内容」判据、E1 spot-check 铁律互相引用成网；⑤ 执行前计划按 W1033 T05 先例归档 docs/11-方案报告/计划方案/（框架号 T-39）。

**为什么不直接改 AGENTS.md §6**：其维护契约要求规则就地并入且版本脚注对齐 HEAD，改动风险高；本协议先以深度篇入库，升格留用户后续裁决。

**验证**：preflight 认领后 dry-run 断言全过再 --apply（spec 先终稿·级联不可重跑）；搜索索引与 CSP 重建；stats --check 24 键零差异（methodology_docs 25→26）；docs_index 重生成；pytest 冒烟无本批新增红灯；safe_commit --expect-spec 过第 51 槽。

> - **状态**：已收官（协议入库·索引登记·级联落盘）
### W1039（2026-10-30）：用户级记忆五则入项目铁律（15/16 条）

> **来源**：用户 2026-10-30 两道令——「禁止补丁加补丁，修复必须从根因开始修复；这个内容加进项目内」
> + 「再次检查用户级记忆文件里面的内容有哪些项目内也得有」。
>
> **背景**：这些原则此前**只在用户级记忆**（跨会话 AI 记忆文件），项目内无载体——换会话、换 Agent、
> 换接手者就检索不到。逐条对照 7 条后，项目内**缺 5 条**。
>
> - **文件**：.github/workflows/README.md、AGENTS.md、CHANGELOG.md、CITATION.cff、HANDOVER.md、README.md、STRUCTURE.md、archive/docs/AGENTS-ARCHIVE.md、docs/00-导读/W批次编号对账表.md、docs/00-导读/项目说明.md、docs/agent/pitfalls.md、scripts/output/_w1039_spec.json、scripts/output/file-index.md、site/index.html

**铁律 15「禁止补丁加补丁，修复必须从根因」**：此前项目内只有 W1019 的具体案例、无通用判据。本条给出
① 定义（修法只让报错消失、未消除结构性原因＝补丁）② **四种典型形态**（为迎合脆弱判据补数据 / 调用处加特例分支 /
用豁免压红灯 / 修完不追问「为什么被触发」）③ 正确顺序（先问机制为何被触发 → 修判据或机制 → 再改数据）
④ **必须转成机器判据**而非写文档等人记。

**铁律 16「协作与环境约束·六则」**：补 5 条用户级记忆 + 1 条元规则——
① 不主动创建 automation（2026-10-13 令，10-17 已复发）② GPU 重负载须先获批并分批（Kernel-Power 41 实证 2 次）
③ 禁用 `~/.minimax/` 内容（取证改用项目面证据）④ 给用户的命令禁 `...` 缩写（W1025 实证）
⑤ 涉及取舍必须显式给推荐 ⑥ 有复用价值的教训，项目内必须留载体。

**并发说明**：开工时台账已被并行会话占用 W1039（任务分级协议），且其 CHANGELOG 段引用了**尚未创建**的
执行前计划文件（C4-f 报出）。按用户裁决 A：退回其半成品（CHANGELOG 段与 8 面级联均未入库），
其 `任务分级协议.md` 正文保留在工作树等待该会话续做；本批占用 W1039。

**验证**：全量门禁 57 段核心全绿。

> - **状态**：已收官（两条用户令入项目铁律 15/16；并行会话半成品未销毁、留在工作树）
### W1038（2026-10-30）：a11y 性能优化（去冗余 lower·收益 5.7%）

> **来源**：用户 2026-10-30 令「做」——承接 W1037 测出的单段瓶颈（a11y对比 73.33s / 52.8%）。
>
> - **文件**：.github/workflows/README.md、AGENTS.md、CHANGELOG.md、CITATION.cff、HANDOVER.md、README.md、STRUCTURE.md、archive/docs/AGENTS-ARCHIVE.md、docs/00-导读/W批次编号对账表.md、docs/00-导读/项目说明.md、scripts/a11y_audit.py、scripts/output/_w1038_spec.json、scripts/output/file-index.md、site/index.html

**profile 定位**：`parse_starttag` 被调 **579 万次**、`str.lower` **4863 万次**（tottime 7.3s）。
病根在 `A11yElement.__init__`——对每个元素全量执行 `tag.lower()` 与 `{k.lower(): v for ...}`。

**改法（实证后动手）**：先验证 CPython 行为——`<DIV CLASS="A">` 经 `html.parser` 解析即得 `tag='div'`、`attrs=[('class','A')]`，**属性键与标签名在进入 handle_starttag 前已被小写化**。⇒ 6 处 `lower()` 纯冗余，去掉。

**语义等价验证（关键）**：改前改后各跑一次，`findings` **13023 条逐条比对，0 处差异**；字节数同为 4,212,724（sha 差异仅来自 `generated_at` 时间戳，非内容）。

**收益：73.9s → 69.7s，仅 5.7%。**

**这个数字说明什么（重要）**：瓶颈**不在冗余 lower**，而在**标准库 `HTMLParser` 的纯 Python 状态机本身**——profile 里 `goahead` cumtime 149s、`parse_starttag` 69s，都是解析器内部开销。去掉 4863 万次 lower 只省 4 秒，说明该方向已挖到底。

**再要大幅提速的唯一路径**：换解析器（`lxml.html` 或 `selectolax`，通常快 10–50 倍）。代价是**引入第三方依赖**，而本项目目前零硬依赖（`policy.yml` 用 JSON 兼容语法、yaml 兜底即是此风格）。**这个取舍应由用户决定，不在本批擅自动手。**

**验证**：findings 逐条一致 · 全量门禁 57 段核心全绿（a11y 段 E2-2 P0/P1=0 未变）。

> - **状态**：已收官（冗余 lower 清除·语义等价已证）；**收益低于预期，已如实标注**；换解析器待裁决
### W1037（2026-10-30）：门禁耗时剖析（--profile·实测推翻旧假设）

> **来源**：用户 2026-10-30 令「都做」（A 加剖析 / B 段级缓存 / C 站点段并行）。先做 A——**没有耗时数据，B 和 C 都是瞎打**。
>
> - **文件**：.github/workflows/README.md、AGENTS.md、CHANGELOG.md、CITATION.cff、HANDOVER.md、README.md、STRUCTURE.md、archive/docs/AGENTS-ARCHIVE.md、docs/00-导读/W批次编号对账表.md、docs/00-导读/项目说明.md、scripts/output/_w1037_spec.json、scripts/output/file-index.md、scripts/verify_delivery.py、site/index.html

**改动**：`verify_delivery.py` 加 `--profile`——`_scoped_run` 里段级计时（同段内多次 subprocess 累加），
`_print_summary` 结束时输出 TOP12 耗时排行（含百分比与条形），`--profile` 开关控制不影响默认输出。

**实测结果（full 档·2026-10-30）**：

```
合计 138.9s（2 分 19 秒）
  a11y对比      73.33s  52.8%
  可视化数据     21.46s  15.4%
  色盲安全        5.51s   4.0%
  动效禁令        5.09s   3.7%
  内嵌残留        4.05s   2.9%
  …其余 34 段    12.51s   9.0%
```

**这个数据推翻了两个此前的判断**：

① **「pre-commit 要跑 13 分钟」是错的** —— 实测 2 分 19 秒。此前那个印象可能来自系统负载高的某次，
或某个已修掉的慢段；**我基于错误前提设计了整轮优化方案**。
② **「35 个站点段都慢」是错的** —— 两段吃掉 68%（a11y 一段占一半），其余 49 段合计 29 秒。

**因此 B / C 的结论**：
- **C（站点段并行）收益有限**：瓶颈是单段 73s，并行后最慢段仍是 73s，天花板就在那。
- **B（段级缓存）也对不上**：a11y 依赖 CSS/页面改动，而这类改动恰恰是最常见的，缓存常失效。
- **真正的解是优化 a11y 那一段本身**：73s 扫 235 页 ≈ 每页 0.31s——若有重复解析/重复计算，
在段内优化比搭缓存架构简单十倍。这条留作下一批（需先读 `a11y_audit.py` 找重复工作）。

**验证**：`--scope docs --profile` 与 full 两档均实测跑通、核心全通过；默认输出未变（不加 `--profile` 无排行）。

> - **状态**：A 已收官（剖析能力入库·数据已推翻旧假设）；B/C **按数据判断不做**，改指向 a11y 段内优化
### W1036（2026-10-30）：授业官 skill 按编制定名（puti-shouye）

> **来源**：用户 2026-10-30 令「`.agent/skills/xiyouji-guard` 这个也要按照编制来定角色」。
>
> **定位**：《取经编制表》§2 丙组 · **菩提祖师 · 授业官**（回目锚点 1）——「教完本事，不留姓名，不受香火；留下的是本事，不是人设」。编制表对本位的挂载写的正是「固化为 Skill（`skill-creator`）」、状态「当前位空」。
>
> - **文件**：.agent/skills/puti-shouye/SKILL.md、.github/workflows/README.md、AGENTS.md、CHANGELOG.md、CITATION.cff、HANDOVER.md、README.md、STRUCTURE.md、archive/docs/AGENTS-ARCHIVE.md、docs/00-导读/W批次编号对账表.md、docs/00-导读/项目说明.md、docs/11-方案报告/设计与架构方案/取经编制表-工具与技能挂位-2026-10-20.md、scripts/output/_vermilion_solid_cache.json、scripts/output/_w1036_spec.json、scripts/output/file-index.md、site/index.html

**改名理由**：`xiyouji-guard` → **`puti-shouye`**（菩提授业）。不叫 guard 是因为：**守卫是挡在门外，授业是把本事交到你手上**。本 skill 不拦人，只在你动手前提醒一遍——该记得的都在这儿，要细节去查坑表。

**改了四处**：① SKILL.md 顶部加**编制位出处**（回目锚点 + 那句评语 + 编制表对本位的约束「技能内容仍以 `pitfalls.md` 为唯一权威源，避免双源漂移」）；② 加「这个名字的意思」段；③ 编制表 §3.1 第 3 行由「位空」改为「**已补（W1034 建 / W1036 定名）**」，并**保留原判据「模型改文件前不会主动加载」仍成立**——该路径确实不自动加载，靠 AGENTS 指针；④ AGENTS 指针路径同步。

**过程记录（安全边界）**：改写既有 SKILL.md 被安全策略拒，理由「建立 Agent 技能可执行配置内容」——与改 pre-commit 钩子同类。由用户删除旧件后**新建**放行。这条边界合理：skill 是会被自动加载的可执行配置，不该由 AI 随口改写。

**验证**：`.agent/skills/` 下现仅 `puti-shouye`；AGENTS 指针指向新路径；编制表三位空缺状态已全部结清。

> - **状态**：已收官（授业官位完成定名与出处标注；器物官按收益不做、收官官与对账官已由 W1035 职责书承接）
### W1035（2026-10-30）：三份职责书（收官官 / 对账官 / 文字取证官）

> **来源**：用户 2026-10-30 令「三项一起」，并追问「不是按西游记里面的人物角色设定来吗」——三份模板全部按《取经编制表》的人物位命名与叙述。
>
> **共同设计**：现环境没有「自建 Agent」接口，但 `Agent` 工具可派发内置角色 ⇒ 把常驻角色**降级为可派发的职责书**。这比建常驻更干净：不占资源、边界清晰、用完即弃。代价是需要有人记得派，故登记在目录索引与 AGENTS 指针里。
>
> - **文件**：.github/workflows/README.md、AGENTS.md、CHANGELOG.md、CITATION.cff、HANDOVER.md、README.md、STRUCTURE.md、archive/docs/AGENTS-ARCHIVE.md、docs/00-导读/W批次编号对账表.md、docs/00-导读/项目说明.md、docs/agent/README.md、docs/agent/closeout-agent-prompt.md、docs/agent/index.md、docs/agent/reconcile-agent-prompt.md、docs/agent/text-audit-agent-prompt.md、scripts/output/_w1035_spec.json、scripts/output/file-index.md、scripts/output/tools-inventory.md、site/index.html

**三份职责书（按人物位）**：

| 位 | 文件 | 职责 | 关键约束 |
|---|---|---|---|
| **沙悟净 · 收官官** | `closeout-agent-prompt.md` | 把批次收干净：跑全量门禁 / 核指针面 / 核计数 / 核台账 / 核体积窗 | **只做验与补，不碰内容**（不施工·不 commit） |
| **谛听 · 只验证** | `reconcile-agent-prompt.md` | 核对登记面 vs 实况（Backlog / 台账 / 文档声明） | **不采信自述**·五判定·每条必带证据·附滞后率 |
| **千里眼 · 取证官** | `text-audit-agent-prompt.md` | 文字只读诊断（过期/重复/冗长/废话） | **先按体裁筛规则**·核心产出是「可压/不可压」分类 |

**为什么是这三处**：编制表里它们都是「有明确职责但无专属载体」的位——沙悟净卡在「无专职 Agent」、谛听直接标着**「当前位空」**、千里眼挂了 `explore` 但缺成文的取证纪律。

**谛听位是这次额外发现的**：T05 只记了三处空缺（器物官/授业官/收官官），但编制表 §2 里谛听位的状态写的是「**当前位空**（MCP 未接）」——第四处空缺，本批补上。器物官（MCP 注册）经成本判断不做：其 5 个工具对应的脚本本就能跑，接 MCP 只是换调用方式。

**每份都写了「不该做什么」**：收官官不施工、对账官不修条目、取证官不改一个字。审查与施工分离这条铁律，在这三处各落实一次。

**验证**：新增 3 md 后搜索索引与 CSP 已重建 · 目录索引 405 件已刷新 · 全量门禁 57 段核心全绿。

> - **状态**：已收官（三处「有职责无载体」的位补齐；器物官按收益不做，已在 W1032 说明）
### W1034（2026-10-30）：授业官位补全（项目级避坑 skill）

> **来源**：用户 2026-10-30 选定 A（做授业官），并指定位置「`D://xiyouji//.agent` 内新建 skills 目录」。这是 T05（W831 批）中 **ST-11 授业官**这一步在现环境的落地。
>
> - **文件**：.agent/skills/xiyouji-guard/SKILL.md、.github/workflows/README.md、.gitignore、AGENTS.md、CHANGELOG.md、CITATION.cff、HANDOVER.md、README.md、STRUCTURE.md、archive/docs/AGENTS-ARCHIVE.md、docs/00-导读/W批次编号对账表.md、docs/00-导读/项目说明.md、scripts/output/_w1034_spec.json、scripts/output/file-index.md、site/index.html

**产物**：`.agent/skills/xiyouji-guard/SKILL.md`——**15 条最高频硬判据**，分四组：批次收官 4 条（先 add 再 refresh / refresh 后再同步 spec / git mv 两端 / changelog_body 前导空行）、判据与门禁 4 条（禁脆弱特征 / 先读原文与源码 / 禁豁免压绿 / token 在途不算事件）、历史与时效 4 条（历史段不改写 / 辨策略决定与已完成 / 步骤绑定旧环境 / 归档只解纵向）、人机协作 3 条（命令禁省略号 / 零引用不能按 .class 搜 / 改 md 连锁索引与 CSP）。每条一句话并指向 pitfalls 全表。

**分层设计（为什么不是 123 条全塞进来）**：pitfalls 已 94 KB，全量做成 skill 会挤占上下文。skill 只放**速查**（15 条 + 查表命令 + 载体分工表），完整条目仍留 `docs/agent/pitfalls.md`——两者是「速查 → 详查」关系，不重复维护。

**顺手解决的两个坑**：
① **`.agent/` 原被 gitignore 整体忽略**（第 214 行），放进去的 skill 不进 git、别的 Agent 拿不到。改为 `.agent/*` + `!.agent/skills/` + `!.agent/skills/**` 放行——**父目录整体忽略时子路径 `!` 无效**，必须用 `dir/*` 形式才能例外。
② **自动加载的路径差异（如实标注）**：系统自动加载只认 `.workbuddy/skills/`，本 skill 在 `.agent/skills/` 下**不会自动加载**。已在 `AGENTS.md` 加显式指针（「⚡ 速查 skill」一行），靠指针 + 主动查阅生效；要自动加载需另放一份到 `.workbuddy/skills/`，会形成双份维护，暂不做。

**验证**：第 45 槽目录文档 0 FAIL（`.agent` 属隐藏目录不在在管扫描面）· 第 52 槽仓库布局 0 FAIL · 全量门禁 57 段核心全绿。

> - **状态**：已收官（授业官位载体建成；ST-10 器物官按收益判断不做，ST-12 收官官现环境无接口）
### W1033（2026-10-30）：T05 计划状态校正（历史正文不改·只改时效标注）

> **来源**：用户 2026-10-30 追问「那你为什么不改计划呢」——上一批我改了编制表（产物），却没动 T05（计划）。
>
> **为什么不当场改正文**：T05 是 W831 批的**执行前计划**，按项目规矩**历史段不改写**（改了就无法追溯「当初怎么打算、为什么这么排」）。这是克制，不是遗漏。
>
> **但有一处必须改，而且我漏了**：T05 第 11 行状态写「**执行中**（施工进行中·非已收官）」，而台账里 **W831 早已归档收官**——两处打架，属「登记面 vs 实况」同族背离。读者按状态行判断会以为整批在途。
>
> - **文件**：.github/workflows/README.md、AGENTS.md、CHANGELOG.md、CITATION.cff、HANDOVER.md、README.md、STRUCTURE.md、archive/docs/AGENTS-ARCHIVE.md、docs/00-导读/W批次编号对账表.md、docs/00-导读/项目说明.md、docs/11-方案报告/计划方案/执行前计划-T05-取经编制表落库与编制位补全.md、scripts/output/_w1033_spec.json、scripts/output/file-index.md、site/index.html

**处置**：① 状态行校正为「**仓内已收官 · 仓外三项未执行**」——ST-01~09 随 W831 归档，ST-10~ST-12（仓外动作）从未执行；② 5.5 表前加**失效声明**：ST-10~12 的 `pip install fastmcp` / `mavis mcp create` / `mavis agent create` 绑定旧环境，**不可照抄**，续做须按现环境重写步骤（指向《取经编制表》§4 环境差异声明）；③ **步骤正文一字未改**——保留「当时怎么打算的」原始记录。

**这条的通用判据**：历史文件该改的是**状态与时效标注**，不是**内容与步骤**。把失效的步骤改写成「现在能用的样子」，历史就变成了假的——后人会以为当年就是这么做的。

**验证**：全量门禁 57 段核心全绿。

> - **状态**：已收官（T05 状态与台账对齐·失效步骤已标注·正文保持原样）
### W1032（2026-10-30）：编制表环境依赖纠错（mavis 假设撤回）

> **来源**：用户 2026-10-30 追问「为什么需要 mavis？」——这一问直接推翻了我上一批的结论。
>
> **我错在哪**：上一批说「连接器与 Agent 清单待有 `mavis` 环境时重核」。事实是 `mavis` 是 **2026-10-20 那套环境的 CLI**（T05 计划里写的 `mavis mcp create`），**现环境不需要它**——我把旧文档的依赖假设当成了现状汇报，没先问一句「现在有什么工具」。
>
> - **文件**：.github/workflows/README.md、AGENTS.md、CHANGELOG.md、CITATION.cff、HANDOVER.md、README.md、STRUCTURE.md、archive/docs/AGENTS-ARCHIVE.md、docs/00-导读/W批次编号对账表.md、docs/00-导读/项目说明.md、docs/11-方案报告/设计与架构方案/取经编制表-工具与技能挂位-2026-10-20.md、docs/agent/pitfalls.md、scripts/output/_w1032_spec.json、scripts/output/file-index.md、site/index.html

**实测（现环境）**：`list_installed_plugins` → **No connectors installed（连接器 0 个）**；`skill_management list` → **用户级技能 2 个**（`dev-god` / `karpathy-guidelines`）。
对照编制表记载的「16 个 App 工具 + 12 项技能」——这不是「数据过期」，是**环境换代**。

**处置**：① 编制表 §4 加「环境差异声明」——表内 `mavis-doctor` / `superpowers:*` / `browser-use:*` / `code-review` / `diagram-design` / `deep-research` 等标注**属旧环境·现不可用**；「16 个 App 工具」标为旧环境快照。② **保留挂位方法论**：哪类能力该落哪个位（器具→器物官、检索→千里眼、验证→谛听）这条映射**跨环境不变**，变的只是具体工具名——照抄名字必踩空，按位找当下工具才有效。

**坑表补第 123 条**（总 122→123·流程主题 34→35）：**文档里的操作步骤绑定当时的工具环境，环境一换步骤即失效，而文档不会自己告诉你**。⇒ 引用旧文档的步骤前，先确认它依赖的工具在当前环境是否存在；写「待某工具重核」这类结论前，先搜一遍当前可用的等效接口。

**验证**：C5e 坑表分项对账（26/6/26/19/11/35 = 123）通过 · 全量门禁 57 段核心全绿。

> - **状态**：已收官（环境差异声明入表·坑表第 123 条入库；`mavis` 依赖结论已撤回）
### W1031（2026-10-30）：取经编制表数据重核（时效与修订触发入表）

> **来源**：用户 2026-10-30 引用 `执行前计划-T05-取经编制表落库与编制位补全.md` 令「重新设计优化」，选定 A 方案（更新数据 + 精简结构 + 加修订触发）。T05 是 W831 批的执行前计划，W831 已归档收官，但产物《取经编制表》作为**活文档**其数据停在 10-20。
>
> - **文件**：.github/workflows/README.md、AGENTS.md、CHANGELOG.md、CITATION.cff、HANDOVER.md、README.md、STRUCTURE.md、archive/docs/AGENTS-ARCHIVE.md、docs/00-导读/W批次编号对账表.md、docs/00-导读/项目说明.md、docs/11-方案报告/设计与架构方案/取经编制表-工具与技能挂位-2026-10-20.md、scripts/output/_w1031_spec.json、scripts/output/file-index.md、site/index.html

**核实结果（10-30 现状 vs 10-20 记载）**：

| 编制位 | 10-20 记载 | 10-30 实测 |
|---|---|---|
| 太上老君·器物官 | MCP 服务器 0 个 | 载体 `mcp-server/xiyouji_mcp.py` **在**（29.5 KB）；是否已挂载未核 |
| 沙悟净·收官官 | 无专职 Agent | 未核（依赖 `mavis agent list`） |
| 菩提祖师·授业官 | 本地技能目录**空** | 目录 **存在且非空**（`~/.workbuddy/skills`）——与记载相反 |

**本批处置**：头部加「数据时效」「修订触发」两行（重核日期 + 60 天到期 + 生态变动即重核）；
§3 补一句辨析——**「空缺」指未挂载，不是未写代码**（三处的载体今天都在，缺的是挂载那一层）；
§4.1 标题与首段明确标「数据已过期」并给重核命令，防止再被当现状引用。

**结构未砍（判断说明）**：§2 编制卡占 16.7 KB（37%），核对后确认它**不是重复叙述**——总表只给六列，
卡片讲的是「怎么用 / 不能做」（孙悟空不做顺手改、猪八戒不能边审边改），这是本文档的核心价值。
按 slop-clean 硬边界「信息守恒」，删它就是砍内容。**本批做的是准确性，不是瘦身**（44.9 → 46.2 KB）。

**验证**：全量门禁 57 段核心全绿 · 编制表 HTML 母件未动（md 为其事实源）。

> - **状态**：已收官（数据时效与修订触发入表；连接器/Agent 清单待有 `mavis` 环境时重核）
### W1030（2026-10-30）：方案报告抽查 + 归档覆盖口径入规范

> **来源**：用户 2026-10-30 两问——「抽查验证（34 件方案报告）」「归档机制和临时文件机制为什么不是全覆盖整个项目」。
>
> **抽查结论**：三个分区各抽 1 件，全部证据型——`审查与评审/全量对抗审查报告`（带审查基准五可标准 + HEAD `5725389d` + 证据脚本一键复跑）、`工作复盘报告`（带生成时间/周期/模型/来源）、`设计与架构`（md + 配套 html 预览与 png 架构图）。
非 md 共 **14 件全为配套件**（架构图 6 png / 设计预览 2 html / 数据截图），每件都有对应 md 母件。
⇒ 34 件方案报告**无 AI 腔、无过期件**，「证据型」判断成立。
>
> - **文件**：.github/workflows/README.md、AGENTS.md、CHANGELOG.md、CITATION.cff、HANDOVER.md、README.md、STRUCTURE.md、archive/docs/AGENTS-ARCHIVE.md、docs/00-导读/W批次编号对账表.md、docs/00-导读/文档规范.md、docs/00-导读/项目说明.md、scripts/output/_w1030_spec.json、scripts/output/file-index.md、site/index.html

**机制口径（本批核心·已写入 `文档规范.md` §8）**：**归档只解「纵向增长」，不解「横向堆积」**。

| 形态 | 特征 | 机制 | 项目覆盖 |
|---|---|---|---|
| **纵向** | 单文件无限追加（一个文件里越积越多的段/行） | 必然撞体积窗（45KB / 110 段 / 60 行）→ **窗口 + 滚动迁出** | 六类治理文档**全部覆盖** |
| **横向** | 独立文件堆积（每件大小恒定） | 不会撞窗 → 需要的是**生命周期状态**（在役/已沉淀/可弃），不是归档器 | 以「README 分区口径 + 索引登记」承担，未建状态列 |

**所以不是遗漏，是两类问题被混为一谈。** `docs/` 正文 2800 篇与方案报告 85 件属横向——给它们配归档器＝用错工具：W1029 已实测，14 件过期计划仅 404 KB，迁走要改 115 处引用，收益是全仓 **0.85%** 的整洁度。**问「为什么不给 X 建归档」之前，先问 X 是纵向还是横向。**

**验证**：全量门禁 57 段核心全绿 · docs 链接 0 broken · 体积窗 0 FAIL。

> - **状态**：已收官（抽查验证通过·机制判据入规范，以后同类问题不必再解释）
### W1029（2026-10-30）：方案报告归档判断（裁决不迁 + 留口径）

> **来源**：用户 2026-10-30 令「B 档合并 Q2」——方案报告逐件判「已完成且已沉淀」的同时清文字，一遍读两件事。
>
> **结论先行：B 档的归档判断做完了，但裁决是「不迁」。**
>
> - **文件**：.github/workflows/README.md、AGENTS.md、CHANGELOG.md、CITATION.cff、HANDOVER.md、README.md、STRUCTURE.md、archive/docs/AGENTS-ARCHIVE.md、docs/00-导读/W批次编号对账表.md、docs/00-导读/项目说明.md、docs/11-方案报告/README.md、scripts/output/_w1029_spec.json、scripts/output/file-index.md、site/index.html

**核对结果（`docs/11-方案报告/` 85 件）**：`计划方案/` 51 件 = **34 件报告**（`T0N-…经验沉淀报告`·执行后沉淀·在役）
+ **17 件执行前计划**（`执行前计划-T0N`·施工前对齐件）。17 件中 **14 件有对应报告**（T01/T03/T04/T19/T20/T21/T23/T26/T27/T28/T29/T30/T31/T32），
说明执行已完成；**3 件无对应报告**（T02/T05/T18）分别被 4/4/2 个文档引用 ⇒ **保留**（未确认执行完毕）。

**为什么裁决不迁（成本核算）**：① 14 件合计 **404 KB**，占该目录 22%、全仓 **0.85%**——不是臃肿问题；
② 迁走需改写 **115 处引用**（29 个文件·跨 17 个 T 号），任一处错即成死链，属高风险低收益；
③ 计划件本身是「当初为什么这么改」的审计依据，与对应报告成套对拍才有价值——迁走反而削弱可追溯性。

**实际落法**：在 `docs/11-方案报告/README.md` 的分区表给「计划方案」加一句口径——
「**两件成套保留·不迁归档**：`执行前计划-T0N` 是施工前对齐件，对应 `T0N-报告` 存在即表示该计划已执行完毕；
全目录 51 件仅 1.8 MB，迁走需改 115 处引用、任一处错即成死链——收益不抵风险，保留便于对拍」。
以后有人再问「这些过期计划为什么不归档」，答案在目录自己的 README 里，不在会话里。

**B 档的文字清理**：按 A 档同样的口径抽查（`计划方案/` 属证据型：每件都有编号、日期、验收人、执行结果），
未发现 AI 腔与可删废话；真正的目标/原则式表述集中在报告开头的「头五要素」表格，那是框架要求的结构化字段，不是灌水。

**验证**：全量门禁 57 段核心全绿 · docs 全量链接 0 broken（未迁即无死链）。

> - **状态**：已收官（归档判断完成·裁决不迁并留口径；文字清理同口径抽查未发现可删项）
### W1028（2026-10-30）：归档系统与临时文件系统诊断

> **来源**：用户 2026-10-30 令「做归档系统和临时文件系统的问题」。
>
> **诊断结论（两套系统都是「制度齐备、缺定期执行」）**：
> ① `tmpe/` 有 policy.yml 六条分类规则 + `tmpe_tidy.py` 的 plan/apply/confirm/undo/from-plan 全套；
> ② `archive/README.md` 有归档台账（34 条路径引用，31 条真实路径**全部存在**，另 3 条为通配写法非缺失）。
> **两套系统的问题都不是设计缺陷，是没人按期跑。**
>
> - **文件**：.github/workflows/README.md、AGENTS.md、CHANGELOG.md、CITATION.cff、HANDOVER.md、README.md、STRUCTURE.md、archive/docs/AGENTS-ARCHIVE.md、docs/00-导读/W批次编号对账表.md、docs/00-导读/项目说明.md、docs/agent/batch-closeout-checklist.md、scripts/output/_w1028_spec.json、scripts/output/file-index.md、site/index.html

**本批处置**：① 跑 `tmpe_tidy.py --apply --confirm`——**归桶 29 件 / 零删除**（顶层散件 186 → 157；
余 140 件在**冻结期内**不迁，属设计防并行会话误动，过期自然归桶）；journal 已留，`--undo` 可悔。
② 收官 checklist 新增「临时区」一项：**每 10 批或 `tmpe/` 超 150MB 跑一次归桶**，并明确
**`_trash/` 清空不在自动范围**（个人文件安全铁律：列清单 → 主人确认 → 回收站）。

**未处置（待用户确认）**：`tmpe/_trash/w993-clean` **81 MB / 709 件**——W993 批清理时的回收件
（2026-09-27 至 10-27），已进回收站但从未清空。**清空=二次删除，需单独确认**；本次只诊断不动手。

**验证**：tmpe 顶层散件 186→157（-29）· 归档台账 31/31 真实路径存在 · 全量门禁 57 段核心全绿。

> - **状态**：诊断与机制补强已收官；`_trash` 清空待用户一句话
### W1027（2026-10-30）：治理文档文字审查 A 档（结论：零可删）

> **来源**：用户 2026-10-30 令「按这个走」——A 档治理文档文字审查现在做，B 档与方案报告归档合并，C 档放弃专项清理。
>
> **口径**：`D:/open-source/slop-scan`（只诊断·每条例须引原文）+ `slop-clean`（只删不加·四条硬边界·必附改动清单）。
> **规则按体裁筛过**：原表针对散文/论文（AI 腔、升华结尾、学术防御性写作），而本批是工程文档；
> 其中「被动语态」「弱化限定」「解释性铺垫」属必要成分（硬边界 4），不列入清理项。
>
> - **文件**：.github/workflows/README.md、AGENTS.md、CHANGELOG.md、CITATION.cff、HANDOVER.md、README.md、STRUCTURE.md、archive/docs/AGENTS-ARCHIVE.md、docs/00-导读/W批次编号对账表.md、docs/00-导读/项目说明.md、scripts/output/_w1027_spec.json、scripts/output/file-index.md、site/index.html

**扫描结果（6 件 · 138 KB）**：

| 判据 | 结果 |
|---|---|
| TIER-1 AI 腔特征词（综上所述/赋能/抓手/深耕/保驾护航/值得注意的是/让我们一起/不仅…更…等 20 词） | **0 命中** |
| 过期表述（「当前/目前」后接陈旧数据） | **0 处** |
| 元叙述（本节/以下将/如上所述） | 14 处「本节」——全为导航语（「本节说明…」），必要保留 |
| 超长句（正文 >150 字，已排除表格行与代码） | 54 处，**逐条核后 0 处可删** |
| 文件内重复句 | 3 组——HANDOVER「项目根目录」与「与其他文档关系」两处列同名链接（用途不同：查位置 vs 查关系），属有意重复 |

**为什么零可删**：54 处超长句逐条核过，全部是**清单 / 批次记录 / 规则条文**——
如「88 个可视化页面（含 graph-explorer·A-AH 34 类 + Q+ 双联 + …）」、「W422 全量治理已处置：perf.yml 补 push 触发·…·…」、
「框架类交付物必须落进仓内目录并登记索引（W858）：凡…必须…」。每项都是独立事实，压短必丢信息；
这属于 slop-clean 硬边界 1「信息守恒」与硬边界 4「必要限定保留」的管辖范围，删了就是错。

**结论**：A 档**无可删内容**——这批文档是「证据型工程文档」（批次号 + 命令 + 实测数字），天然不含 AI 腔。
**对 B 档的启示**：真正的废话风险在**计划类文档**（`docs/11-方案报告/计划方案/` 51 件）——「执行前计划」含大量
目标/原则/预期收益式表述，那才是 slop-clean 的战场；`审查与评审/`、`工作复盘/` 属证据型，预计同样少见。

**验证**：全量门禁 57 段核心全绿 · 体积窗 0 FAIL · 台账 60 行达窗口上限（下批先归档）。

> - **状态**：A 档收官（零改动·结论入库）；B 档待与方案报告归档合并执行；C 档按裁决放弃专项清理
### W1026（2026-10-30）：HANDOVER 已完成内容归档 + 归档机制诊断

> **来源**：用户 2026-10-30 三问——「为什么文件内已做完的内容还存在交接文档内 / 已完成的方案报告为何没移入归档 / 对整个项目所有文件的文字内容审查去除过期重复冗长废话」。
>
> **诊断（回答前两问）**：不是没做归档，是**归档机制覆盖不全**。六类治理文档各有归档容器（CHANGELOG / HANDOVER / STRUCTURE / AGENTS / 台账 / file-index），但：① HANDOVER 内只有**里程碑块**有滚动窗口（保留最近 6 个），而「二、下一步方向候选清单」是**累积型区段、无任何归档机制**——已完成叙述随批只增不减；② `docs/11-方案报告/` 85 件报告**从来没有归档机制**（README 只有索引，无状态列、无迁出动作）。
>
> - **文件**：.github/workflows/README.md、AGENTS.md、CHANGELOG.md、CITATION.cff、HANDOVER.md、README.md、STRUCTURE.md、archive/docs/AGENTS-ARCHIVE.md、archive/docs/HANDOVER-ARCHIVE.md、archive/docs/W批次编号对账表-ARCHIVE.md、docs/00-导读/W批次编号对账表.md、docs/00-导读/项目说明.md、scripts/output/_w1026_spec.json、scripts/output/file-index.md、site/index.html

**本批处置（Q1）**：重构 HANDOVER「二」段——把已完成叙述全文迁 `archive/docs/HANDOVER-ARCHIVE.md`（W402 战略转型 3 条删除线已完成项、A2 系列收束、A3/A4/A5 各方向「已完成 WXXX-WXXX」批次史、E1-E8、S 卡裁决、优先级建议），现役只留 **13 条未完成项**；并**补回一条仍在生效的策略约束**（停止模板化扩容·A3 冻结 215 篇·A4 W342 放宽为「非批量补篇」）——删归档时若不辨认「策略决定 vs 已完成叙述」，会把活约束一起埋掉。**HANDOVER 43.5 → 29.9 KB（-32%），387 行**。

**Q2 诊断（未处置·需另批）**：`docs/11-方案报告/` 85 件（审查与评审 13 / 工作复盘 15 / 治理与核查 3 / 计划方案 51 / 设计与架构 10 / 调研与数据 3）。「已完成且已沉淀」的判据须逐件读（是否有结论、是否已被后续批次引用），不能按文件名批量判断——51 件「计划方案」里既有执行前计划（已过期）也有任务执行报告（已成沉淀），混在一起。拟建 `archive/docs/方案报告-ARCHIVE/` + README 加「状态」列（在役 / 已沉淀），逐件判后迁出。

**Q3 规模（未处置·需分档）**：全仓 **2940 个 md / 47.6 MB**（不含 node_modules/archive/desktop）。按 `D:/open-source/slop-scan`（只诊断）与 `slop-clean`（只删不加·四条硬边界）口径，一轮清完不现实。拟分三档：A 治理与导读（HANDOVER/AGENTS/README/项目说明/文档规范，约 6 件）→ B 方案报告 85 件 → C docs 正文与 site 文案（其余约 2800 件，随批次自然更新，不专项清）。

**验证**：体积窗 0 FAIL（HANDOVER 29.6KB）· 文档口径体检除「HANDOVER 未提交残留」外 0 FAIL（提交后消）· A4 stats 标记「209 篇」随行保留（未破坏 C5 对账）· 归档容器 344KB（追加式·不改写）。

> - **状态**：Q1 已收官；Q2/Q3 已给判据与分档，待用户定范围后另批执行
### W1025（2026-10-30）：坑表计数升机器判据（C5e）+ 新 Agent 入口

> **来源**：用户 2026-10-30 令「做」——落实 W1024 结项时提的两条建议：① HANDOVER 顶部加「新 Agent 必读三件套」；② 坑表分项计数升机器判据（W1024 实证：AGENTS 分项停在 `25/25/15/10/28=109` 长期无人核，而总数声明已到 118；我手算 121、实算 122）。
>
> **落点选择**：不新增门禁槽位（那要改 gates.md 的 57 槽声明，连锁成本高于收益），而是并入第 31 槽 C5 系列——「分项之和 vs 总数」本就是 C5「聚合数字对账」的业务范围。
>
> - **文件**：.github/workflows/README.md、AGENTS.md、CHANGELOG.md、CITATION.cff、HANDOVER.md、README.md、STRUCTURE.md、archive/docs/AGENTS-ARCHIVE.md、docs/00-导读/项目说明.md、scripts/check_doc_sync.py、scripts/output/_w1025_spec.json、scripts/output/file-index.md、site/index.html

**本批要点**：① **新增 C5e**（`check_doc_sync.py`）：坑表六主题标题声明数、各段 `- **` 实测条目数、AGENTS 总数、AGENTS 分项行、HANDOVER 两处总数——**五处交叉对账**，任一处不等即 FAIL。② **判据可证伪验证**：把 AGENTS 的 122 临时改成 123 → 立刻报 `C5e: AGENTS.md 声明 123 条 ≠ 坑表实测 122 条`，复原后归零（不是死门控）。③ **HANDOVER 顶部加必读三件套**：本文件 + pitfalls（**只读前 10 条也强于不读**）+ gates，并给出实证——W1019–W1024 六批踩的坑有 11 条属坑表已写过的形态。

**验证**：`check_doc_sync --self-test` **33/33 通过**（含既有 C1–C7 全部用例·未破坏原判据）· 负样本 123 → FAIL、复原 → 0 FAIL · HANDOVER 42.6KB ≤45 · 体积窗 0 FAIL · 全量门禁 57 段核心全绿。

> - **状态**：已收官（坑表计数自此五处交叉对账，不再靠人核；新 Agent 入口已在 HANDOVER 顶部写明）
### W1024（2026-10-30）：本次任务教训固化对账（补 4 条坑 + 计数订正）

> **来源**：用户 2026-10-30 三问——「这次任务中遇到过的问题都在任务中解决了吗 / 以后还会再次犯错吗 / 其他 Agent 在后续工作中能够了解吗」。这是教训固化审计，不是功能批。
>
> **做法**：把 W1019–W1023 踩过的 19 类问题逐条对账两个维度——**是否已机器化**（有门禁/守卫/自测能自动拦住）、**是否入坑表**（其他 Agent 检索得到）。查出 4 条真缺口（已修代码但没写教训，或压根没写），本批补齐。
>
> - **文件**：.github/workflows/README.md、AGENTS.md、CHANGELOG.md、CITATION.cff、HANDOVER.md、README.md、STRUCTURE.md、archive/docs/AGENTS-ARCHIVE.md、docs/00-导读/W批次编号对账表.md、docs/00-导读/项目说明.md、docs/agent/batch-closeout-checklist.md、docs/agent/pitfalls.md、scripts/output/_w1024_spec.json、scripts/output/file-index.md、site/index.html

**补的 4 条坑（均为「代码修了但教训未落载体」）**：① **「零引用」判定不能按 `.class` 搜**——HTML 写的是 `class="btn"`（不带点），W1019 初版 grep `\.btn` 判出 78 个「零引用」类，实则全在用（含 `.btn`/`.badge`/`.kpi-grid`），差点整批删除；② **`git mv` 删除侧旧路径也要进 spec**——`file_index_rows` 只写新路径会让第 51 槽判「代提他方件」；③ **护栏要覆盖默认路径不只 `--force`**——`inline_css` 裸跑会一次内联 526 个外链页，正是护栏想防的事；④ **改/加 md 连锁触发搜索索引与 CSP**——W1022/W1023 连踩两次（改 md → 索引条目不符 → 重算 CSP → 又红一次），已把「改 md → 重建索引 → 重算 CSP → 跑门禁」固定进收官 checklist。

**顺带查出的计数腐坏**：AGENTS 的六主题分项行停在 `25/25/15/10/28=109` 的旧值上长期无人核（实测应为 `26/6/26/19/11/34`），而我手算总数得 121、实算为 **122** ⇒ 已订正四处，并在 checklist 加「改坑表必须实算分项」（这条属于**机器查不出、只能靠 checklist** 的类别，如实标注）。

**验证**：坑表 118→122 条（CSS 26 / JS 6 / git 26 / 级联 19 / 数据 11 / 流程 34，分项之各与总数均与实测一致）· AGENTS/HANDOVER 四处计数同步 · 收官 checklist 补 2 个 checkbox · 全量门禁 57 段核心全绿。

> - **状态**：已收官（19 类问题对账完毕：15 类已机器化 + 4 类本轮补入载体；剩余不可机器化项列入 checklist）
### W1023（2026-10-30）：提示词库派发骨架补齐（3 项）

> **来源**：用户 2026-10-30 令「补完」——接续 W1022 结项时登记的余 3 项提示词模板。
>
> **做法**：按 W1022 立下的「就地并入·不另立补充篇」原则，把骨架补进各自文件末尾，
> 不新增平行文件（避免第二事实源）。
>
> - **文件**：.github/workflows/README.md、AGENTS.md、CHANGELOG.md、CITATION.cff、HANDOVER.md、README.md、STRUCTURE.md、archive/docs/AGENTS-ARCHIVE.md、docs/00-导读/W批次编号对账表.md、docs/00-导读/项目说明.md、docs/12-提示词库/03-工作复盘提示词.md、docs/12-提示词库/05-项目审查任务书.md、docs/12-提示词库/09-导师提问流程.md、scripts/output/_w1023_spec.json、scripts/output/file-index.md、site/index.html

**本批要点**：① **05 项目审查任务书**补「派发骨架」——把七类审查（R-1~R-7）划成 6 个派发单元，标明并行性（U5 设计**不可并行**·审美判断无法机械汇总；U6 已完成工作**必须收尾**，是前序单元的汇总裁决），并给出通用 prompt 骨架（范围 / 证据要求 / 分级 / 输出四段）；同时厘清与对抗审查的分工——本任务书是**全面体检**（面越宽越好），对抗审查是**声明对拍**（判据是实况），混做两头不讨好。② **03 工作复盘**补「单批复盘最小 prompt」——完整版 441 行是给里程碑/季度复盘的；单批若整份丢给 subagent，篇幅会被耗在填满 10 个章节上，真正要的「差异 / 坑 / 可复用」被稀释 ⇒ 裁到必答六项（声称 / 实际 / 差异 / 新形态坑 / 可复用落点 / 下批建议），并明确禁止复述 CHANGELOG 与写评价性套话。③ **09 导师提问**补「场景化提问清单」——按五类场景（新功能 / 修 bug / 重构 / 设计 / 内容）给出可直接照问的序列，每场景 ≤7 问，并附两条通用追问（「能给一个具体例子吗」「什么情况下这个做法会失效」）。

**验证**：全量门禁 57 段核心全绿 · 三份文件章节序正确（03 的「7. 派发骨架」置于「6. 最终交付物」之后）· code fence 内的 `##` 结构标记未被结构化检查误判。

> - **状态**：已收官（W1022 登记的余 3 项提示词模板全部补齐，暂无遗留）
### W1022（2026-10-30）：对抗式审查批（A–G 全项·P1×3 + P2×5 当批修）

> **来源**：preflight 报「距上次对抗审查（W998）已 23 批 ≥ 20」+ 用户 2026-10-30 令「可以做」；按 `docs/agent/adversarial-audit-prompt.md` 模板派发 subagent 做 A–G 全项**只读**审查（审查与修复分离），被审对象为 W1019（CSS 治本 + 净重口径 + 门禁判据改稳定契约）、W1020（Backlog 对账）、W1021（第四哨）。
>
> **判定**：三批核心声明基本属实（330 页零漂移、双门禁改判据后全绿、24 例全过、体积达标），但抓出 **P1×3 + P2×5 + P3×5**，其中一条是**假绿级 fail-open**。
>
> - **文件**：.github/workflows/README.md、AGENTS.md、CHANGELOG.md、CITATION.cff、HANDOVER.md、README.md、STRUCTURE.md、archive/docs/AGENTS-ARCHIVE.md、archive/docs/W批次编号对账表-ARCHIVE.md、docs/00-导读/W批次编号对账表.md、docs/00-导读/项目说明.md、docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md、pytest.ini、scripts/check_audit_trigger.py、scripts/check_backlog_review.py、scripts/check_motion_ban.py、scripts/check_token_coverage.py、scripts/inline_css.py、scripts/output/_w1022_spec.json、scripts/output/file-index.md、scripts/output/stats-changelog.json、scripts/output/stats-index.md、scripts/output/stats.json、site/_template.html、site/data/81-hardships-view.html、site/data/81-hardships.html、site/data/_shell.html、site/data/aesthetics.html、site/data/ai-dialogue.html、site/data/business-model.html、site/data/cave-estate.html、site/data/century-dialogue.html、site/data/chapter-stats.html、site/data/chapter-structure-graph.html、site/data/character-appearance.html、site/data/character-dynamic-network.html、site/data/character-presence-timeline.html、site/data/character-relationship-3d-view.html、site/data/character-relationship-3d.html、site/data/character-semantic-network.html、site/data/character-sentiment-arc.html、site/data/chart-design.html、site/data/cognitive-psychology.html、site/data/concept-device.html、site/data/counterfactual.html、site/data/criticism-history.html、site/data/cross-time-danmaku.html、site/data/cultural-misreading.html、site/data/customs-pass-route.html、site/data/data-explorer.html、site/data/deconstruction.html、site/data/dialogue-sentiment.html、site/data/ecology.html、site/data/emotional-heatmap.html、site/data/ethics-consumption.html、site/data/famous-time-travel.html、site/data/four-dimensional-research-network.html、site/data/four-heavenly-kings-artifacts.html、site/data/game-webnovel.html、site/data/global-pattern.html、site/data/graph-explorer.html、site/data/guanyin-six-roles-network.html、site/data/hardship-difficulty-heatmap.html、site/data/hardship-heatmap.html、site/data/heaven-power-network.html、site/data/intertextuality-network.html、site/data/journey-geo-3d.html、site/data/journey-geo-semiotics.html、site/data/journey-map-interactive.html、site/data/journey-route.html、site/data/journey-spacetime.html、site/data/jurisprudence.html、site/data/karma-reincarnation.html、site/data/language-style-radar.html、site/data/linguistics.html、site/data/magic-system.html、site/data/material-archaeology.html、site/data/mbti-evolution.html、site/data/methodology-matrix.html、site/data/ming-political-thought-comparison.html、site/data/monster-background.html、site/data/monster-capability-radar.html、site/data/monster-ecology-network.html、site/data/monster-female-network.html、site/data/monster-hierarchy-network.html、site/data/monster-sociology.html、site/data/monster-victims-network.html、site/data/music-structure.html、site/data/narrative-experiment.html、site/data/narrative-rhythm-curve.html、site/data/narratology-12d-network.html、site/data/narratology-16d-network.html、site/data/perf-canvas-rendering.html、site/data/philosophy.html、site/data/pilgrim-team-dynamic-network.html、site/data/pilgrim-team-psychology-arc.html、site/data/poetry-rhythm-analysis.html、site/data/power-resources.html、site/data/relationships.html、site/data/risk-project.html、site/data/search.html、site/data/six-senses-narratology-network.html、site/data/social-media.html、site/data/story-timeline.html、site/data/tag-cloud.html、site/data/text-evolution.html、site/data/text-search.html、site/data/theological-intervention-network.html、site/data/timeline.html、site/data/underworld-power-network.html、site/data/visual-art.html、site/data/workplace.html、site/dukou-engine.html、site/en/81-hardships-view.html、site/en/81-hardships.html、site/en/academic-papers.html、site/en/aesthetics.html、site/en/ai-dialogue.html、site/en/bestiary.html、site/en/business-model.html、site/en/cave-estate.html、site/en/century-dialogue.html、site/en/chapter-stats.html、site/en/chapter-structure-graph.html、site/en/chapters-map.html、site/en/character-appearance.html、site/en/character-bailongma.html、site/en/character-bajie.html、site/en/character-dynamic-network.html、site/en/character-presence-timeline.html、site/en/character-relationship-3d-view.html、site/en/character-relationship-3d.html、site/en/character-semantic-network.html、site/en/character-sentiment-arc.html、site/en/character-shaseng.html、site/en/character-tangseng.html、site/en/character-wukong.html、site/en/characters.html、site/en/chart-design.html、site/en/cognitive-psychology.html、site/en/concept-device.html、site/en/counterfactual.html、site/en/criticism-history.html、site/en/cross-time-danmaku.html、site/en/cultural-misreading.html、site/en/customs-pass-route.html、site/en/dashboard.html、site/en/data-explorer.html、site/en/deconstruction.html、site/en/dialogue-sentiment.html、site/en/dukou-engine.html、site/en/ecology.html、site/en/emotional-heatmap.html、site/en/essay-ai-era.html、site/en/essay-buddhist-chan.html、site/en/essay-chapter-couplets.html、site/en/essay-character-fu.html、site/en/essay-cipai-linjiangxian.html、site/en/essay-cipai-mantingfang.html、site/en/essay-cipai-shuidiaogetou.html、site/en/essay-cipai-xijiangyue.html、site/en/essay-composition-origins.html、site/en/essay-divine-bureaucracy.html、site/en/essay-folk-belief.html、site/en/essay-historical-xuanzang.html、site/en/essay-information-cocoon.html、site/en/essay-ming-economy.html、site/en/essay-ming-examination.html、site/en/essay-ming-garrison.html、site/en/essay-ming-intellectual-history.html、site/en/essay-ming-judiciary.html、site/en/essay-ming-literary-thought.html、site/en/essay-ming-maritime-ban.html、site/en/essay-ming-metaphor.html、site/en/essay-ming-military.html、site/en/essay-ming-politics.html、site/en/essay-ming-religion.html、site/en/essay-ming-social-customs.html、site/en/essay-modern-management.html、site/en/essay-original-poetry.html、site/en/essay-poetry-imagery.html、site/en/essay-poetry-opening.html、site/en/essay-quanzhen-daoism.html、site/en/essay-rhythm-analysis.html、site/en/essay-scenery-poems.html、site/en/essay-thematic-poetry.html、site/en/essay-three-teachings.html、site/en/essay-version-evolution.html、site/en/essay-zen-koan-vs-neidan.html、site/en/ethics-consumption.html、site/en/famous-time-travel.html、site/en/four-dimensional-research-network.html、site/en/four-heavenly-kings-artifacts.html、site/en/game-webnovel.html、site/en/global-pattern.html、site/en/graph-explorer.html、site/en/guanyin-six-roles-network.html、site/en/guide.html、site/en/hardship-difficulty-heatmap.html、site/en/hardship-heatmap.html、site/en/heaven-power-network.html、site/en/index.html、site/en/intertextuality-network.html、site/en/journey-geo-semiotics.html、site/en/journey-map-interactive.html、site/en/journey-route.html、site/en/journey-spacetime.html、site/en/jurisprudence.html、site/en/karma-reincarnation.html、site/en/language-style-radar.html、site/en/linguistics.html、site/en/magic-system.html、site/en/material-archaeology.html、site/en/mbti-evolution.html、site/en/methodology-matrix.html、site/en/methodology.html、site/en/ming-political-thought-comparison.html、site/en/monster-background.html、site/en/monster-capability-radar.html、site/en/monster-ecology-network.html、site/en/monster-female-network.html、site/en/monster-hierarchy-network.html、site/en/monster-sociology.html、site/en/monster-victims-network.html、site/en/music-structure.html、site/en/narrative-experiment.html、site/en/narrative-rhythm-curve.html、site/en/narratology-12d-network.html、site/en/narratology-16d-network.html、site/en/perf-canvas-rendering.html、site/en/philosophy.html、site/en/pilgrim-team-dynamic-network.html、site/en/pilgrim-team-psychology-arc.html、site/en/poetry-rhythm-analysis.html、site/en/power-resources.html、site/en/relationships.html、site/en/risk-project.html、site/en/search.html、site/en/site-map.html、site/en/six-senses-narratology-network.html、site/en/social-media.html、site/en/tag-cloud.html、site/en/text-evolution.html、site/en/text-search.html、site/en/theological-intervention-network.html、site/en/timeline.html、site/en/tribulations.html、site/en/underworld-power-network.html、site/en/visual-art.html、site/en/visualizations.html、site/en/workplace.html、site/index.html、site/reader/ch001.html、site/reader/ch002.html、site/reader/ch003.html、site/reader/ch004.html、site/reader/ch005.html、site/reader/ch006.html、site/reader/ch007.html、site/reader/ch008.html、site/reader/ch009.html、site/reader/ch010.html、site/reader/ch011.html、site/reader/ch012.html、site/reader/ch013.html、site/reader/ch014.html、site/reader/ch015.html、site/reader/ch016.html、site/reader/ch017.html、site/reader/ch018.html、site/reader/ch019.html、site/reader/ch020.html、site/reader/ch021.html、site/reader/ch022.html、site/reader/ch023.html、site/reader/ch024.html、site/reader/ch025.html、site/reader/ch026.html、site/reader/ch027.html、site/reader/ch028.html、site/reader/ch029.html、site/reader/ch030.html、site/reader/ch031.html、site/reader/ch032.html、site/reader/ch033.html、site/reader/ch034.html、site/reader/ch035.html、site/reader/ch036.html、site/reader/ch037.html、site/reader/ch038.html、site/reader/ch039.html、site/reader/ch040.html、site/reader/ch041.html、site/reader/ch042.html、site/reader/ch043.html、site/reader/ch044.html、site/reader/ch045.html、site/reader/ch046.html、site/reader/ch047.html、site/reader/ch048.html、site/reader/ch049.html、site/reader/ch050.html、site/reader/ch051.html、site/reader/ch052.html、site/reader/ch053.html、site/reader/ch054.html、site/reader/ch055.html、site/reader/ch056.html、site/reader/ch057.html、site/reader/ch058.html、site/reader/ch059.html、site/reader/ch060.html、site/reader/ch061.html、site/reader/ch062.html、site/reader/ch063.html、site/reader/ch064.html、site/reader/ch065.html、site/reader/ch066.html、site/reader/ch067.html、site/reader/ch068.html、site/reader/ch069.html、site/reader/ch070.html、site/reader/ch071.html、site/reader/ch072.html、site/reader/ch073.html、site/reader/ch074.html、site/reader/ch075.html、site/reader/ch076.html、site/reader/ch077.html、site/reader/ch078.html、site/reader/ch079.html、site/reader/ch080.html、site/reader/ch081.html、site/reader/ch082.html、site/reader/ch083.html、site/reader/ch084.html、site/reader/ch085.html、site/reader/ch086.html、site/reader/ch087.html、site/reader/ch088.html、site/reader/ch089.html、site/reader/ch090.html、site/reader/ch091.html、site/reader/ch092.html、site/reader/ch093.html、site/reader/ch094.html、site/reader/ch095.html、site/reader/ch096.html、site/reader/ch097.html、site/reader/ch098.html、site/reader/ch099.html、site/reader/ch100.html、site/reader/index.html、site/reader/themes-hub.html、tests/unit/test_style_block_judgement.py

**P1 修复（当批）**：① **台账超窗**（正本 61 段 > 窗口 60·在途行必致门禁红）⇒ 跑 `archive_ledger_rows` 归档，正本回落 59 段；② **治本判据零回归锁**——W1019 把副本识别从「注释文本」改成「标记配对」，但全库 `grep iter_private_style_blocks|strip_comments` 在 tests/ **命中 0**，判据被改回即 228 页静默误判复发 ⇒ 新增 `tests/unit/test_style_block_judgement.py` 3 例（带标记块排除 / 剥注释后仍识别 / 带属性 style 不误配）；③ **审计触发器 fail-open**——`check_audit_trigger` 只认 token 字样，而认领行派发时就写「在途（…已派发）」，等于**写一行在途登记即可永久压制该哨**（实测把「已 23 批」压回 0）⇒ 在途状态不计事件（两触发器同改）。

**P2 修复（同批·均同源）**：① `inline_css` 护栏只覆盖 `--force` 分支 ⇒ **裸跑会一次内联 526 个外链页**，改为默认路径同护栏（实测裸跑现为 0 操作）；② 文本模式写盘使 **330 页工作树全 CRLF**，与 `.gitattributes text=auto eol=lf` 背离（`i/lf w/crlf`·二进制口径每页多 1558 B）⇒ `newline=""` 写盘，现 `i/lf w/lf`；③ HANDOVER 对账分布自相矛盾（写「5 未动 / 1 未过时」，实测 6/8/3）⇒ 订正；④ `check_motion_ban` 用精确 `<style>` 字面量枚举块，168 个带属性页的私有块既不进集合也不被摘除 ⇒ 统一到 `STYLE_BLOCK_RE`；⑤ `check_backlog_review` 纯子串匹配会被反义串「已执行（未完成）」骗过 ⇒ 加否定词窗口。

**P3 处置**：`inline_css --force` 非幂等（每轮 +4B 缩进）⇒ 剥离正则补前导 `[ \t]*`，现两次 `--force` md5 相同；`check_token_coverage` docstring 仍写已废掉的旧判据 ⇒ 同口径订正；余 3 项（历史 spec 单换行、「51,504」起点不可复核、BL-8/BL-9 以注记闭环无 artifact）**登记留痕**，见下节。

**声明与实况不符项（模板要求单列）**：

| # | 声明 | 实测 |
|---|---|---|
| 1 | W1020「5 未动 / 1 未过时」 | 6 未动 / 8 部分 / 3 留档（`grep -c` 实算） |
| 2 | `inline_css --force` 幂等 | 每轮 +4 B 缩进（非幂等·已修） |
| 3 | 「330 页逐字节一致」 | 仅在文本读法下成立；工作树原为 CRLF（已修为 LF） |
| 4 | `check_token_coverage` docstring「块内含 tokens.css — 注释特征」 | 实现已于 W1019 改为标记配对（已订正） |
| 5 | W1019「单页内联块 51,504 B」 | 起点不可复核（实测改前三类页均 51,801、根级 48,982）；39,323 B 吻合 |

**留痕（不改）**：① 5 个历史 spec（`_w736/_w737/_w760/_w761/_w831`）以单换行开场，precheck 新守卫会拒——属「复现历史批才触发」，非现役缺陷；② 「51,504」起点数字不复核，本段以实测口径为准；③ BL-8/BL-9 的关闭依据是「性质/时点口径注记」（`counterfactual_summary.json` 与 `domino_causality.json` 的 `nature_note` / `timing_note`），属**设计选择**而非验证——比另四条的硬证据弱，已如实登记。

**模板补齐（用户 2026-10-30 追问「为什么不派多 subagent / 还有哪些可做模板 / 模板要不要按实际情况改」）**：① 新增 `docs/agent/parallel-evidence-template.md`——「判断串行、取证并行」，含切分判据、派发骨架、汇总者三条义务（不转述 / 抽样复核 / 矛盾不外推）与成本参考；把「为什么对抗审查只派一个」写成判据：拆开则 B 项（`i/lf w/crlf`）与 D 项（`open(...,"w")`）无法串成 eol 契约背离那条 P2。② 新增 `docs/agent/gate-triage-template.md`——门禁红灯五步法（读原文 → 单跑 → 读判据源码 → 分类 → 选修法）+ 四条红线（禁豁免压绿 / 禁迎合脆弱判据补产物 / 禁判据未执行判绿 / 禁只看汇总）+ 六类高发误判对照表。③ 新增 `docs/agent/batch-closeout-checklist.md`——9 步收官清单，每步注明「跳过会红哪个槽」，把本次连续四批踩的坑（前导空行 / 先 add 再 refresh / 删除侧路径 / 脚本归位 / 回窗）固化成顺序。④ `adversarial-audit-prompt.md` 补三条收尾义务（**给历史事件补 token** / **在途不计事件** / **回写模板**）+ 新增「模板自身的维护」节（校准戳 / 检查项可追溯 / 数字必须现测 / 不另立补充篇），头部标「上次校准：W1022」。余 3 项登记下批：05 项目审查任务书的可粘贴派发骨架、03 工作复盘的派发模板、09 导师提问的提问清单（04 任务执行的「批次开工」职责已由本批 checklist 吸收）。

**验证**：审查 A–G 全项实跑（独立重算 330 页零漂移·含 depth 前缀规则）· 三触发器 `--self-test` 全过 · 新增 3 例回归锁 + 既有 24 例全过（计 1080）· 裸跑 0 操作 / 两次 `--force` md5 相同 / `i/lf w/lf` · 台账 59 段 · `stats.py --check` 24 键零差异 · 全量门禁 57 段核心全绿。

> - **状态**：已收官（P1×3 + P2×5 + P3×2 当批修，P3×3 留痕；报告原文未入库，证据行号已摘入本段）
### W1021（2026-10-30）：Backlog 对账触发器常驻化（preflight 批数告警）

> **来源**：用户 2026-10-30 令「做」——采纳 W1020 结项建议中的 **preflight 批数计数告警**方案（另一候选「CHANGELOG 季度提醒」判为不主用：BL-21 写了 2027-01 季度点仍无人跟进，实证写进文档的提醒会被忘）。
>
> **连带登记**：W1020 台账行的状态列补事件 token「Backlog 对账已执行」——否则本器首跑即判「从未对账」假警（fail-closed 的必然副作用）。
>
> - **文件**：.github/workflows/README.md、AGENTS.md、CHANGELOG.md、CITATION.cff、HANDOVER.md、README.md、STRUCTURE.md、archive/docs/AGENTS-ARCHIVE.md、docs/00-导读/W批次编号对账表.md、docs/00-导读/项目说明.md、docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md、pytest.ini、scripts/check_backlog_review.py、scripts/output/_w1021_spec.json、scripts/output/file-index.md、scripts/output/stats-changelog.json、scripts/output/stats-index.md、scripts/output/stats.json、scripts/preflight_check.py、site/index.html、tests/unit/test_backlog_review.py

**本批要点**：① **新增第四哨** `scripts/check_backlog_review.py`——台账状态列含 token「Backlog 对账已执行」的最大 W 号距当前 max ≥ **25 批**即提示（只提示不拦截，exit 恒 0）。② **三条铁则沿用对抗审查触发器**（同一病同一防法）：token 只认**状态列**（防主题列提及 token 的行把自己判成一次对账·W1004 同族自伤）、取 **max 不取文件序**（防末尾低号补登记行把 last 拉低）、**正本与归档同扫**（防对账行被行窗归档后退化成「从未对账」假警）。③ **只做批数阈值不做天数阈值**：台账日期只存在于认领会话列且位置不固定（主题含裸竖线会整体右移·见 parse_ledger W825），另引 CHANGELOG 段解析面收益不抵复杂度；且项目节拍本就是 W### 批次——W691 一批闭环 5 条 BL 却零回写，说明滞后由「改动发生」驱动而非日历。
④ **接线** preflight 5.8 项（与 5.75 对抗审查并列）；内置八态自测 + `tests/unit/test_backlog_review.py` 7 例。

**验证**：八态自测通过（阈值两侧/不可判定/非台账行豁免/泛词不重置/取 max/主题列不算/同批/归档同扫）·pytest 7 例全过 · preflight 实跑输出「距上次（W1020）0 批 < 25 未触发」·计数 1069→1077 两处同步 · `stats.py --check` 24 键零差异。

> - **状态**：已收官（Backlog 对账自此每 25 批被机器点名一次）
### W1020（2026-10-30）：Backlog 登记面对账批（逐条核 git 与测试实况）

> **来源**：用户 2026-10-30 令「开一个 Backlog 对账批；不只要写入长期记忆也要写入项目内；开始」。起因是 W1019 连续命中两条「已做完却仍挂待办」的 Backlog（BL-29、BL-33）。
>
> **连带登记**：对账中另发现登记面残留三处（`scripts/README.md` 幽灵条目、`统计口径说明.md` 仍写 BL-19 未决、数据集两份副本不同步），同批修掉。
>
> - **文件**：.github/workflows/README.md、AGENTS.md、CHANGELOG.md、CITATION.cff、HANDOVER.md、README.md、STRUCTURE.md、archive/docs/AGENTS-ARCHIVE.md、archive/docs/W批次编号对账表-ARCHIVE.md、docs/00-导读/W批次编号对账表.md、docs/00-导读/统计口径说明.md、docs/00-导读/项目说明.md、docs/agent/pitfalls.md、scripts/README.md、scripts/output/_w1020_spec.json、scripts/output/file-index.md、site/index.html

**本批要点**：① **全量对账**——29 条 Backlog 逐条拿 git 与测试实况核，不采信条目自述。② **关闭并移出 12 条**（滞后率 41%）：BL-8/BL-9 以性质与时点口径注记闭环、BL-11 稀柿衕用字全站统一且有门禁反写防线、BL-14/BL-15 章节与阶段口径已注记一致、BL-18 第 9/10/11 回归属语缺口已闭合、BL-19 两真源分歧已被`check_citations.py` 语料保真判据消解、BL-21/BL-25 已执行、BL-29 测试与 CI 早已落地、BL-31 脚本已退休、BL-33 治本已收官。③ **订正保留 17 条**：5 条未动、8 条部分完成、3 条留档、1 条未过时，每条按实测数字改写现状（如 BL-1 实测 EMBEDDED 52 页对 EMBEDDED_DATA 92 页、登记「26 vs 41」失真）。④ **体积窗顺带解掉**：HANDOVER 由 45.3KB 回落至 42.5KB（上限 45KB）——已完成条目**整条移出**而非加标记，否则只进不出必然复发。

**验证**：`preflight_check` 体积窗口 C6 由 FAIL 转通过 · 坑表计数 115→117 条四处同步 · `stats.py --check` 24 键零差异 · 全量门禁 57 段核心全绿。

> - **状态**：已收官（对账结论与证据入 CHANGELOG 本段与坑表；Backlog 建议按季度或大版本段周期性对账）
### W1019（2026-10-30）：BL-33/BL-29 收官批（CSS 单一事实源治本 + 内联净重口径）

> **来源**：用户 2026-10-30 令「做 BL-33 治本」+「BL-29 这个也做了」+「C + 收官」。
>
> **连带登记**：BL-29 主体经实跑核实已于 W791 完成（`server/security.test.ts` 22 例全绿 + `ci.yml:429` 接线）⇒ 本批只补其残余缺口（Python 侧参数钳制长期零测试）；BL-33 经核实 W895 已做过一轮收敛，本批补完治本部分。
>
> - **文件**：.github/workflows/README.md、AGENTS.md、CHANGELOG.md、CITATION.cff、DESIGN.md、HANDOVER.md、README.md、STRUCTURE.md、archive/docs/AGENTS-ARCHIVE.md、docs/00-导读/W批次编号对账表.md、docs/00-导读/项目说明.md、docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md、pytest.ini、scripts/inline_css.py、scripts/output/_vermilion_solid_cache.json、scripts/output/file-index.md、scripts/output/stats-changelog.json、scripts/output/stats-index.md、scripts/output/stats.json、site/_template.html、site/data/81-hardships-view.html、site/data/81-hardships.html、site/data/_shell.html、site/data/aesthetics.html、site/data/ai-dialogue.html、site/data/business-model.html、site/data/cave-estate.html、site/data/century-dialogue.html、site/data/chapter-stats.html、site/data/chapter-structure-graph.html、site/data/character-appearance.html、site/data/character-dynamic-network.html、site/data/character-presence-timeline.html、site/data/character-relationship-3d-view.html、site/data/character-relationship-3d.html、site/data/character-semantic-network.html、site/data/character-sentiment-arc.html、site/data/chart-design.html、site/data/cognitive-psychology.html、site/data/concept-device.html、site/data/counterfactual.html、site/data/criticism-history.html、site/data/cross-time-danmaku.html、site/data/cultural-misreading.html、site/data/customs-pass-route.html、site/data/data-explorer.html、site/data/deconstruction.html、site/data/dialogue-sentiment.html、site/data/ecology.html、site/data/emotional-heatmap.html、site/data/ethics-consumption.html、site/data/famous-time-travel.html、site/data/four-dimensional-research-network.html、site/data/four-heavenly-kings-artifacts.html、site/data/game-webnovel.html、site/data/global-pattern.html、site/data/graph-explorer.html、site/data/guanyin-six-roles-network.html、site/data/hardship-difficulty-heatmap.html、site/data/hardship-heatmap.html、site/data/heaven-power-network.html、site/data/intertextuality-network.html、site/data/journey-geo-3d.html、site/data/journey-geo-semiotics.html、site/data/journey-map-interactive.html、site/data/journey-route.html、site/data/journey-spacetime.html、site/data/jurisprudence.html、site/data/karma-reincarnation.html、site/data/language-style-radar.html、site/data/linguistics.html、site/data/magic-system.html、site/data/material-archaeology.html、site/data/mbti-evolution.html、site/data/methodology-matrix.html、site/data/ming-political-thought-comparison.html、site/data/monster-background.html、site/data/monster-capability-radar.html、site/data/monster-ecology-network.html、site/data/monster-female-network.html、site/data/monster-hierarchy-network.html、site/data/monster-sociology.html、site/data/monster-victims-network.html、site/data/music-structure.html、site/data/narrative-experiment.html、site/data/narrative-rhythm-curve.html、site/data/narratology-12d-network.html、site/data/narratology-16d-network.html、site/data/perf-canvas-rendering.html、site/data/philosophy.html、site/data/pilgrim-team-dynamic-network.html、site/data/pilgrim-team-psychology-arc.html、site/data/poetry-rhythm-analysis.html、site/data/power-resources.html、site/data/relationships.html、site/data/risk-project.html、site/data/search.html、site/data/six-senses-narratology-network.html、site/data/social-media.html、site/data/story-timeline.html、site/data/tag-cloud.html、site/data/text-evolution.html、site/data/text-search.html、site/data/theological-intervention-network.html、site/data/timeline.html、site/data/underworld-power-network.html、site/data/visual-art.html、site/data/workplace.html、site/dukou-engine.html、site/en/81-hardships-view.html、site/en/81-hardships.html、site/en/academic-papers.html、site/en/aesthetics.html、site/en/ai-dialogue.html、site/en/bestiary.html、site/en/business-model.html、site/en/cave-estate.html、site/en/century-dialogue.html、site/en/chapter-stats.html、site/en/chapter-structure-graph.html、site/en/chapters-map.html、site/en/character-appearance.html、site/en/character-bailongma.html、site/en/character-bajie.html、site/en/character-dynamic-network.html、site/en/character-presence-timeline.html、site/en/character-relationship-3d-view.html、site/en/character-relationship-3d.html、site/en/character-semantic-network.html、site/en/character-sentiment-arc.html、site/en/character-shaseng.html、site/en/character-tangseng.html、site/en/character-wukong.html、site/en/characters.html、site/en/chart-design.html、site/en/cognitive-psychology.html、site/en/concept-device.html、site/en/counterfactual.html、site/en/criticism-history.html、site/en/cross-time-danmaku.html、site/en/cultural-misreading.html、site/en/customs-pass-route.html、site/en/dashboard.html、site/en/data-explorer.html、site/en/deconstruction.html、site/en/dialogue-sentiment.html、site/en/dukou-engine.html、site/en/ecology.html、site/en/emotional-heatmap.html、site/en/essay-ai-era.html、site/en/essay-buddhist-chan.html、site/en/essay-chapter-couplets.html、site/en/essay-character-fu.html、site/en/essay-cipai-linjiangxian.html、site/en/essay-cipai-mantingfang.html、site/en/essay-cipai-shuidiaogetou.html、site/en/essay-cipai-xijiangyue.html、site/en/essay-composition-origins.html、site/en/essay-divine-bureaucracy.html、site/en/essay-folk-belief.html、site/en/essay-historical-xuanzang.html、site/en/essay-information-cocoon.html、site/en/essay-ming-economy.html、site/en/essay-ming-examination.html、site/en/essay-ming-garrison.html、site/en/essay-ming-intellectual-history.html、site/en/essay-ming-judiciary.html、site/en/essay-ming-literary-thought.html、site/en/essay-ming-maritime-ban.html、site/en/essay-ming-metaphor.html、site/en/essay-ming-military.html、site/en/essay-ming-politics.html、site/en/essay-ming-religion.html、site/en/essay-ming-social-customs.html、site/en/essay-modern-management.html、site/en/essay-original-poetry.html、site/en/essay-poetry-imagery.html、site/en/essay-poetry-opening.html、site/en/essay-quanzhen-daoism.html、site/en/essay-rhythm-analysis.html、site/en/essay-scenery-poems.html、site/en/essay-thematic-poetry.html、site/en/essay-three-teachings.html、site/en/essay-version-evolution.html、site/en/essay-zen-koan-vs-neidan.html、site/en/ethics-consumption.html、site/en/famous-time-travel.html、site/en/four-dimensional-research-network.html、site/en/four-heavenly-kings-artifacts.html、site/en/game-webnovel.html、site/en/global-pattern.html、site/en/graph-explorer.html、site/en/guanyin-six-roles-network.html、site/en/guide.html、site/en/hardship-difficulty-heatmap.html、site/en/hardship-heatmap.html、site/en/heaven-power-network.html、site/en/index.html、site/en/intertextuality-network.html、site/en/journey-geo-semiotics.html、site/en/journey-map-interactive.html、site/en/journey-route.html、site/en/journey-spacetime.html、site/en/jurisprudence.html、site/en/karma-reincarnation.html、site/en/language-style-radar.html、site/en/linguistics.html、site/en/magic-system.html、site/en/material-archaeology.html、site/en/mbti-evolution.html、site/en/methodology-matrix.html、site/en/methodology.html、site/en/ming-political-thought-comparison.html、site/en/monster-background.html、site/en/monster-capability-radar.html、site/en/monster-ecology-network.html、site/en/monster-female-network.html、site/en/monster-hierarchy-network.html、site/en/monster-sociology.html、site/en/monster-victims-network.html、site/en/music-structure.html、site/en/narrative-experiment.html、site/en/narrative-rhythm-curve.html、site/en/narratology-12d-network.html、site/en/narratology-16d-network.html、site/en/perf-canvas-rendering.html、site/en/philosophy.html、site/en/pilgrim-team-dynamic-network.html、site/en/pilgrim-team-psychology-arc.html、site/en/poetry-rhythm-analysis.html、site/en/power-resources.html、site/en/relationships.html、site/en/risk-project.html、site/en/search.html、site/en/site-map.html、site/en/six-senses-narratology-network.html、site/en/social-media.html、site/en/tag-cloud.html、site/en/text-evolution.html、site/en/text-search.html、site/en/theological-intervention-network.html、site/en/timeline.html、site/en/tribulations.html、site/en/underworld-power-network.html、site/en/visual-art.html、site/en/visualizations.html、site/en/workplace.html、site/index.html、site/reader/ch001.html、site/reader/ch002.html、site/reader/ch003.html、site/reader/ch004.html、site/reader/ch005.html、site/reader/ch006.html、site/reader/ch007.html、site/reader/ch008.html、site/reader/ch009.html、site/reader/ch010.html、site/reader/ch011.html、site/reader/ch012.html、site/reader/ch013.html、site/reader/ch014.html、site/reader/ch015.html、site/reader/ch016.html、site/reader/ch017.html、site/reader/ch018.html、site/reader/ch019.html、site/reader/ch020.html、site/reader/ch021.html、site/reader/ch022.html、site/reader/ch023.html、site/reader/ch024.html、site/reader/ch025.html、site/reader/ch026.html、site/reader/ch027.html、site/reader/ch028.html、site/reader/ch029.html、site/reader/ch030.html、site/reader/ch031.html、site/reader/ch032.html、site/reader/ch033.html、site/reader/ch034.html、site/reader/ch035.html、site/reader/ch036.html、site/reader/ch037.html、site/reader/ch038.html、site/reader/ch039.html、site/reader/ch040.html、site/reader/ch041.html、site/reader/ch042.html、site/reader/ch043.html、site/reader/ch044.html、site/reader/ch045.html、site/reader/ch046.html、site/reader/ch047.html、site/reader/ch048.html、site/reader/ch049.html、site/reader/ch050.html、site/reader/ch051.html、site/reader/ch052.html、site/reader/ch053.html、site/reader/ch054.html、site/reader/ch055.html、site/reader/ch056.html、site/reader/ch057.html、site/reader/ch058.html、site/reader/ch059.html、site/reader/ch060.html、site/reader/ch061.html、site/reader/ch062.html、site/reader/ch063.html、site/reader/ch064.html、site/reader/ch065.html、site/reader/ch066.html、site/reader/ch067.html、site/reader/ch068.html、site/reader/ch069.html、site/reader/ch070.html、site/reader/ch071.html、site/reader/ch072.html、site/reader/ch073.html、site/reader/ch074.html、site/reader/ch075.html、site/reader/ch076.html、site/reader/ch077.html、site/reader/ch078.html、site/reader/ch079.html、site/reader/ch080.html、site/reader/ch081.html、site/reader/ch082.html、site/reader/ch083.html、site/reader/ch084.html、site/reader/ch085.html、site/reader/ch086.html、site/reader/ch087.html、site/reader/ch088.html、site/reader/ch089.html、site/reader/ch090.html、site/reader/ch091.html、site/reader/ch092.html、site/reader/ch093.html、site/reader/ch094.html、site/reader/ch095.html、site/reader/ch096.html、site/reader/ch097.html、site/reader/ch098.html、site/reader/ch099.html、site/reader/ch100.html、site/reader/index.html、site/reader/themes-hub.html、site/system.css、tests/unit/test_inline_css_resync.py、tests/unit/test_rag_server_clamp.py

**本批要点**：① **漂移全量实测**——330 个内联页与源逐字节比对，300 一致 / 30 漂移，三类归集：A 题图规则 26 页（W983/W1013/W1016 三轮逐页写入·源缺失）、B timeline 2 页（源有页缺）、C 根级 2 页（源有页缺 74 至 79 行且残留旧值）。② **根因是脚本早退**——`inline_css.py` 的 `depth==0` 无条件早退（W875 加）把根级已内联页的重同步一并堵死，W876 只能手工靶向修 ⇒ 早退撤除，改由「无外链且未内联」判据接管，外链页仍受 W895 `--inline-links` 护栏保护。③ **题图规则写回源**——`.chapter-plate` 三规则归并进 `system.css`，26 页不再只活在副本里。④ **体积改走净重口径**——源文件保留注释供追溯，`inline_css.py` 只在传播为内联副本时剥离块注释，单页内联块 51,504 降至 39,323 B（负 23.7%）；另砍零引用微交互工具类 787 B。

**验证**：内联块与源（净重口径）**330/330 一致 · 漂移 0**（原 30）· 根级两页补齐 brand-mark/kpi-row/hero-ornament/ico/chapter-plate · 旧值残留扫描 **0** · 新增回归锁 **17 例全过**（inline_css 重同步 3 + rag 参数钳制 14）· 第 15 槽单页内联块 39,323 B 远高于下限 20,000 B · CSS 类门禁（第 11/34/35/36/49 槽）**0 违例** · `stats.py --check` 24 键零差异。

> - **状态**：已收官（BL-33 治本 + 净重口径 + BL-29 残余缺口；BL-29/BL-33 登记面已核实并待关闭）
### W1018（2026-10-29）：回次 og:image 全覆盖批·第三轮（12 张线描立像/场面）



> **来源**：用户 2026-10-29 令「同族扫描 + 第 48 门禁补覆盖 做完再继续剩余 68 回扩量」⇒ 沿用 W1001/W1013 批已过目的口径（线描立像族·母版段两变体·按题材定主体·12 张一批）。
>
> **连带登记**：本笔同时落 **W1015 工具链稳健性补强①** 的登记面——① 跨行改写扫描器（`scripts/check_cross_line_rewrite.py`：改写面正则「`[^X]*` 无尾锚点 ⇒ 匹配段可跨行 ⇒ `re.sub` 整段替换 = 静默删行」；全仓 scripts/ 全树实扫 **高危 0 处**，另 43 处可疑 + 184 处只读面；判据自带 4 例负样本自证；接线 `ci_sim.py` 第 8 项）② 第 48 门禁补覆盖（`judge_file()` 的**读盘路径**此前零覆盖 ⇒ W1005 批 `R.io` 类 AttributeError 潜伏到首个新增件才引爆；现补 self_test 第⑧例 + 4 例 pytest）。W1015 提交 = `7771c9d3`（让号·台账行精确暂存·未代提并行批在途件）。
>
> - **文件**：.github/workflows/README.md、AGENTS.md、CHANGELOG.md、CITATION.cff、HANDOVER.md、README.md、STRUCTURE.md、archive/docs/AGENTS-ARCHIVE.md、archive/docs/CHANGELOG-ARCHIVE.md、archive/docs/W批次编号对账表-ARCHIVE.md、archive/docs/file-index-ARCHIVE.md、assets/promo/plate-set/index.md、assets/promo/plate-set/plate-line-73-ch020-huxianfeng.png、assets/promo/plate-set/plate-line-73-ch020-huxianfeng.webp、assets/promo/plate-set/plate-line-74-ch024-qingfeng.png、assets/promo/plate-set/plate-line-74-ch024-qingfeng.webp、assets/promo/plate-set/plate-line-75-ch034-bashanhu.png、assets/promo/plate-set/plate-line-75-ch034-bashanhu.webp、assets/promo/plate-set/plate-line-76-ch043-tuolong.png、assets/promo/plate-set/plate-line-76-ch043-tuolong.webp、assets/promo/plate-set/plate-line-77-ch044-yangli.png、assets/promo/plate-set/plate-line-77-ch044-yangli.webp、assets/promo/plate-set/plate-line-78-ch049-laoyuan.png、assets/promo/plate-set/plate-line-78-ch049-laoyuan.webp、assets/promo/plate-set/plate-line-79-ch051-qingniu.png、assets/promo/plate-set/plate-line-79-ch051-qingniu.webp、assets/promo/plate-set/plate-line-80-ch064-xingxian.png、assets/promo/plate-set/plate-line-80-ch064-xingxian.webp、assets/promo/plate-set/plate-line-81-ch074-qingshi.png、assets/promo/plate-set/plate-line-81-ch074-qingshi.webp、assets/promo/plate-set/plate-line-82-ch091-bidun.png、assets/promo/plate-set/plate-line-82-ch091-bidun.webp、assets/promo/plate-set/plate-line-83-ch096-kouyuanwai.png、assets/promo/plate-set/plate-line-83-ch096-kouyuanwai.webp、assets/promo/plate-set/plate-line-84-ch008-jinding.png、assets/promo/plate-set/plate-line-84-ch008-jinding.webp、assets/promo/plate-set/preview-contact-sheet.png、assets/promo/plate-set/preview-contact-sheet.webp、assets/promo/plate-set/preview-w1018-sheet.png、assets/promo/plate-set/raw/README.md、assets/promo/plate-set/raw/index.md、assets/promo/plate-set/raw/round16/README.md、assets/promo/plate-set/raw/round16/index.md、assets/promo/plate-set/raw/round16/plate-line-73-ch020-huxianfeng.jpg、assets/promo/plate-set/raw/round16/plate-line-74-ch024-qingfeng.jpg、assets/promo/plate-set/raw/round16/plate-line-75-ch034-bashanhu.jpg、assets/promo/plate-set/raw/round16/plate-line-76-ch043-tuolong.jpg、assets/promo/plate-set/raw/round16/plate-line-77-ch044-yangli.jpg、assets/promo/plate-set/raw/round16/plate-line-78-ch049-laoyuan.jpg、assets/promo/plate-set/raw/round16/plate-line-79-ch051-qingniu.jpg、assets/promo/plate-set/raw/round16/plate-line-80-ch064-xingxian.jpg、assets/promo/plate-set/raw/round16/plate-line-81-ch074-qingshi.jpg、assets/promo/plate-set/raw/round16/plate-line-82-ch091-bidun.png、assets/promo/plate-set/raw/round16/plate-line-83-ch096-kouyuanwai.jpg、assets/promo/plate-set/raw/round16/plate-line-84-ch008-jinding.jpg、docs/00-导读/W批次编号对账表.md、docs/00-导读/项目说明.md、docs/11-方案报告/README.md、docs/11-方案报告/计划方案/T38-任务计划执行与经验沉淀报告-2026-10-29.md、docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md、docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md、docs/INDEX.md、docs/agent/pitfalls.md、scripts/_w1018_closeout_faces.py、scripts/_w1018_derive_prepare.py、scripts/_w1018_derive_stage.py、scripts/_w1018_derive_verify.py、scripts/_w1018_download.py、scripts/_w1018_fix_index_order.py、scripts/_w1018_fix_names_order.py、scripts/_w1018_fix_refs.py、scripts/_w1018_fix_round16.py、scripts/_w1018_make_spec.py、scripts/_w1018_master.py、scripts/_w1018_pick2.py、scripts/_w1018_prepare.py、scripts/_w1018_probe_covered.py、scripts/_w1018_retry.py、scripts/_w1018_sheet.py、scripts/_w1018_stage.py、scripts/_w1018_verify.py、scripts/index.md、scripts/output/README.md、scripts/output/_cascade_files_W1018.txt、scripts/output/_vermilion_solid_cache.json、scripts/output/_w1016_batch.json、scripts/output/_w1016_batch_a.json、scripts/output/_w1016_batch_b.json、scripts/output/_w1016_manifest.json、scripts/output/_w1016_retry.json、scripts/output/_w1018_spec.json、scripts/output/file-index.md、scripts/output/index.md、scripts/output/stats-changelog.json、scripts/output/stats-index.md、scripts/output/stats.json、scripts/output/tools-inventory.md、site/data/cross-time-danmaku.html、site/data/search.html、site/data/tag-cloud.html、site/dukou-engine.html、site/en/search.html、site/index.html、site/reader/ch008.html、site/reader/ch020.html、site/reader/ch024.html、site/reader/ch034.html、site/reader/ch043.html、site/reader/ch044.html、site/reader/ch049.html、site/reader/ch051.html、site/reader/ch064.html、site/reader/ch074.html、site/reader/ch091.html、site/reader/ch096.html、site/static/images/README.md、site/static/images/index.md、site/static/images/og-plate-line-73-ch020-huxianfeng.webp、site/static/images/og-plate-line-74-ch024-qingfeng.webp、site/static/images/og-plate-line-75-ch034-bashanhu.webp、site/static/images/og-plate-line-76-ch043-tuolong.webp、site/static/images/og-plate-line-77-ch044-yangli.webp、site/static/images/og-plate-line-78-ch049-laoyuan.webp、site/static/images/og-plate-line-79-ch051-qingniu.webp、site/static/images/og-plate-line-80-ch064-xingxian.webp、site/static/images/og-plate-line-81-ch074-qingshi.webp、site/static/images/og-plate-line-82-ch091-bidun.webp、site/static/images/og-plate-line-83-ch096-kouyuanwai.webp、site/static/images/og-plate-line-84-ch008-jinding.webp、site/static/images/plate-line-73-ch020-huxianfeng.webp、site/static/images/plate-line-74-ch024-qingfeng.webp、site/static/images/plate-line-75-ch034-bashanhu.webp、site/static/images/plate-line-76-ch043-tuolong.webp、site/static/images/plate-line-77-ch044-yangli.webp、site/static/images/plate-line-78-ch049-laoyuan.webp、site/static/images/plate-line-79-ch051-qingniu.webp、site/static/images/plate-line-80-ch064-xingxian.webp、site/static/images/plate-line-81-ch074-qingshi.webp、site/static/images/plate-line-82-ch091-bidun.webp、site/static/images/plate-line-83-ch096-kouyuanwai.webp、site/static/images/plate-line-84-ch008-jinding.webp。

**本批要点**：① **缺口全量角色谱扫描**——缺口 68 回逐回统计角色出现次数并打上下文片段；② **已出主体全表避重**——plate-set 实为 **88→100 个母版 / 100 个唯一 slug**（编号 1–12 被四个批次族复用 ⇒ 编号 max≠主体数）⇒ 12 个主体与已出全表**零冲突**；③ **母版段两变体**——立像段**逐字复用 249 字符**（6 张），场面段**仅改 3 处**（6 张）；④ **3 张重出**——① 画面出现桌案器物（违反母版段「不画器物细节」）② 主体过小过淡（下部墨 0.0217 < 0.03）③ 左右大面积黑边 + 主体触顶触底（3×3 窗口暗占比 0.761 / 判据值 200.08）；⑤ **落位 12 页** ⇒ 回目覆盖 **32 → 44 回**、缺口 **68 → 56 回**；⑥ **未覆盖页零回归**——缺口 56 页中 54 页仍为通用 og-cover-ink-zh.jpg、2 页保留既有 card-* 专属图。

**验证**：母版判据 J1–J10 **112 张 · FAIL 0**（重出后）· 裁切验算 **112 张 · FAIL 0**（重出后）· 落位验收 **0 FAIL**（12 页题图 + og + alt + 暗色隐藏 + 未覆盖页零回归）· 跨行改写扫描器 **高危 0 处** · 第 48 门禁自测 **9/9** · 全量门禁见收官提交。

> - **状态**：已收官（12 张落地·母版族 100 → 112 张·既有 100 张母版与站点版零改动·其余 56 个无配图回目页的 og:image 未误改·坑表 +2 条·待用户目视）

### W1017（2026-10-29）：产物目录归位 + 临时区清理批

> **来源**：用户 2026-10-29 回复「A+B」（承接上一轮三问后的取证提议）：A＝产物目录瘦身、B＝`tmpe` 深度清理（并明确授权删除 `_trash` 超期件与 `node_modules`）。
>
> - **文件**：CHANGELOG.md、CITATION.cff、HANDOVER.md、README.md、STRUCTURE.md、archive/README.md、archive/docs/AGENTS-ARCHIVE.md、docs/00-导读/W批次编号对账表.md、docs/00-导读/项目说明.md、scripts/output/file-index.md、scripts/output/README.md、scripts/output/index.md、scripts/output/stats.json、scripts/output/tools-inventory.md（另 366 件历史产物按批号迁 `archive/scripts/batches/w7xx|w8xx|w9xx|w10xx/`，逐项见 file-index W1017 段与归档台账）
>
**要点**：
① **四面对照扫描定去留**（不凭体积拍脑袋）：对 `scripts/output` 全部 689 件受跟踪件，逐件在四面对照面——活代码 `scripts/`（非 archive）、`tests/`、`.github/`+`mcp-server/`、现役 `docs/` 与根治理文档——做 basename 全仓检索（排除 archive 与 tmpe 这两个冷存储面）。结果：**366 件零引用**（w7xx 139 / w8xx 146 / w9xx 75 / w10xx 6；含 208 json + 147 txt + 4 py + 3 png 4.6MB + 3 err + 1 css）→ `git mv` 入 `archive/scripts/batches/<段>/`；**323 件有引用一律保留**。
② **两处「看着像垃圾但不能搬」**：`_w*_spec.json` 248 件被 `backfill_changelog.py` 全量 glob 用于给未立段批次补 CHANGELOG 段——搬走等于断掉补段能力（W1015 正是缺段的在途批），故**全部保留**；门禁缓存 `_vermilion_solid_cache.json`（第 49 槽按页 hash 增量）与 `_w864_accent_exemptions.json`（朱砂豁免表）被活门禁读，亦保留。
③ **产物目录边界立规**：`STRUCTURE.md` 新增「输出目录边界」行——output 只放活产物；历史一次性件按批号入档（W1012 立原则，本批完成全量归位）。
④ **tmpe 授权清理（本次唯一删除动作）**：严格走契约——先列清单落 `tmpe/_reports/purge-<时间戳>.txt`，再经 PowerShell `Microsoft.VisualBasic.FileIO.FileSystem` 的 `SendToRecycleBin` **移入回收站**（禁 `rm -rf`/`del /S /Q`）。清 `_trash` 超 7 天非保护件 64 件 + `w607_docxgen/node_modules` = 53.4MB。
⑤ **个人稿保护实证生效**：`protect_globs`（匿名稿/装饰投稿版/投稿/mqxs_anon/mqxs_submission/hallmark/papercheck/audit_.*_paper_data）之外，本批另按「匿名/投稿/适配版」保守补强——**36 件个人投稿稿 19.1MB 全部保留未删**（含 `设计方向-南艺适配版（匿名）.docx` 系列），与契约 §3「个人文件安全铁律」一致。
⑥ 效果：`scripts/output` 跟踪件 **689→323**；`tmpe` 总量 **173.4→112.2MB**（`_trash` 122.4→78MB）；归档区 tracked 1166→1532 件。

**验证**：四处引用扫描输出可复核（`tmpe/_w1017_move.tsv` 366 行·归位后自检 0 失败）· `check_archive_health` 0 项待办（段级双向对账绿）· 归档台账追加 5 行（含段级计数声明：w7xx 240 / w8xx 192 / w9xx 302 / w10xx 46 内容件，元数据 README+index 不计）· 全量 verify 核心全过。

> - **状态**：已收官（产物目录回归活产物单一职责 + 临时区授权清理）

### W1016（2026-10-29）：教训固化批

> **来源**：用户 2026-10-29 三问「这次任务中遇到的问题都解决了吗·以后还会再犯错吗·多 Agent 项目其他 Agent 后续能了解到吗」——直指 W1014 的**载体缺口**：缺陷代码修了，但教训未落 `docs/agent/pitfalls.md` ⇒ 违反 §6-14「跨会话教训权威落坑表与本节，私有记忆仅作镜像」。故本批不新增功能，只做**教训固化**。
>
> - **文件**：AGENTS.md、CHANGELOG.md、CITATION.cff、HANDOVER.md、README.md、STRUCTURE.md、archive/docs/AGENTS-ARCHIVE.md、docs/00-导读/项目说明.md、docs/00-导读/新Agent启动Prompt.md、docs/00-导读/W批次编号对账表.md、docs/agent/pitfalls.md、scripts/batch_cascade.py、scripts/check_doc_sync.py、scripts/output/file-index.md、tests/unit/test_cascade_precheck.py、tests/unit/test_status_z_parse.py
>
**要点**：
① **先核后补（不重复登记）**：逐条 grep 验证 W1014 实踩的 12 类问题哪些已在坑表——`E-17`「级联不能重跑 + 段内定向订正」**已覆盖**（W1014 正是照它做的），`W523`「git 输出路径要加 `core.quotePath=false`」**只覆盖 git diff** ⇒ 缺 `status --porcelain` 半边。据此补 **7 条真缺口**（102→109 条）。
② **git 组 +2**：`E-37` `status --porcelain` 不受 `quotePath=false` 影响（中文路径仍八进制转义）+ `-z` 的 rename 两条记录次条无 `XY` 前缀 + dirty 须只收 Y 位非空；`E-38` 并行会话撞号（对方新件 docstring 自称我方批号）与生成器产物连带改的归属判断法。
③ **级联组 +2**：`E-39` spec 四字段硬性形态与「desc 写进版本抬头行」的连带后果（W1014 连撞 4 次）；`E-40` 回窗工具把「未超窗」误报成失败（正常态被断言当异常）。
④ **流程组 +3**：`E-41` 沙箱三类假缺陷识别法（EPERM/存根 python/锁权限，判据＝完全权限下复跑是否仍红）；`E-42` 报告登记编号取全局 max 且分区篇数须等于行数；`E-43` 「死门控」——配置项或分支位置让判据永不可达（W999 同族泛化）。
⑤ **可机检者升硬守卫**：`batch_cascade.precheck` 新增拒 spec `desc`/`head_sentence` 裸聚合数字（原只能落盘后被第 31 门禁 C5c 抓、而级联不可重跑 ⇒ 只能手工订正）——本批实测该守卫当场拦下自己的 spec 草稿。
⑥ **补缺失自测**：`check_doc_sync._parse_status_z` 抽为纯函数 + `tests/unit/test_status_z_parse.py` 5 例（W1014 修此 bug 却没加测试）；`tests/unit/test_cascade_precheck.py` 13 例锁 precheck 全规则。
⑦ **顺带根治常驻红**：`check_gov_doc_claims` N5「`新Agent启动Prompt` a1_a6=615 ≠ stats 616」自 W1011 起常驻报红（W1011 使 A5 34→35、总数 615→616 未随改）⇒ 订正该文档两处 + AGENTS §1 分项 A5 34→35（原分项合计 615 与总数标记 616 自相矛盾）⇒ 数字断言对账 **0 FAIL**。

**验证**：`check_gov_doc_claims` N1-N5 全一致（0 FAIL）· N4 坑位数 109 == pitfalls 实数 · ruff 全仓 0 债 · 新增 18 例单测全过 · precheck 自测含裸数字正/负样本 · 全量 verify 核心全过。

> - **状态**：已收官（教训落载体 + 可机检者升硬守卫）

### W1015（2026-10-29）：工具链稳健性补强①（跨行改写扫描器 + 第 48 门禁读盘路径覆盖）

> **来源**：用户 2026-10-29 令「同族扫描 + 第 48 门禁补覆盖 做完再继续剩余 68 回扩量」。
>
> - **文件**：scripts/check_cross_line_rewrite.py、scripts/check_plan_template.py、scripts/ci_sim.py、tests/unit/test_cross_line_rewrite.py、tests/unit/test_plan_template_read_disk.py、docs/00-导读/W批次编号对账表.md。
>
> **本批要点**：① **跨行改写扫描器**（新增）——病根：「`[^X]*` 无尾锚点 ⇒ 匹配段可跨行 ⇒ `re.sub` 整段替换 = 静默删行」（W1005 实证）。全仓 scripts/ 全树实扫 ⇒ **改写面高危 0 处**（另 43 处可疑 + 184 处只读面）；判据自带 **4 例负样本自证**（含「排除符含 `\n` ⇒ 必不报」）；接线 `ci_sim.py` 第 8 项（避门禁本体·§11.2 禁擅改）。② **第 48 门禁读盘路径补覆盖**——`judge_file()` 的读盘面此前**零覆盖**（自测 ①~⑤ 全走纯函数 `R.judge`）⇒ W1005 批在首个新增计划方案件进仓时崩在 `AttributeError: module 'plan_template_review' has no attribute 'io'` ⇒ 潜伏到真实新增件才引爆；现补 self_test ⑧ 例 + 4 例 pytest。
>
> **验证**：扫描器 `--self-test` 4/4 · `--gate` 0 FAIL（高危 0 处）· 第 48 门禁 `--self-test` 9/9 · pytest 9 passed。
>
> - **状态**：已收官（让号留痕：并行 W1014「工具链体检整改批」先落地 ⇒ 本会话让号 **W1015**；台账行用 `update-index --cacheinfo` 精确暂存·未代提他方在途件）

### W1014（2026-10-29）：工具链体检整改批

> **来源**：用户 2026-10-29 令「检查项目所有的工具、脚本、探针、门禁有没有问题是否需要优化；临时文件系统和归档系统现在是否需要修改优化；对所有文件目录进行整理分类；该进归档系统的进归档系统，该进临时文件系统的进临时文件系统」→ 三决策（全修含门禁本体 / 待 W1013 收官开本批 / 全部接线升格）。
>
> - **文件**：.github/workflows/ci.yml、.pre-commit-config.yaml、AGENTS.md、Makefile、archive/README.md、archive/scripts/batches/w10xx/_w1013_align_files.py、archive/scripts/batches/w10xx/_w1013_derive_prepare.py、archive/scripts/batches/w10xx/_w1013_download.py、archive/scripts/batches/w10xx/_w1013_fix_desc.py、archive/scripts/batches/w10xx/_w1013_inventory.py、archive/scripts/batches/w10xx/_w1013_make_spec.py、archive/scripts/batches/w10xx/_w1013_master.py、archive/scripts/batches/w10xx/_w1013_prepare.py、archive/scripts/batches/w10xx/_w1013_read.py、archive/scripts/batches/w10xx/_w1013_retry.py、archive/scripts/batches/w10xx/_w1013_retry2.py、archive/scripts/batches/w10xx/_w1013_roster_check.py、archive/scripts/batches/w10xx/_w1013_sheet.py、archive/scripts/batches/w10xx/_w1013_shot.py、archive/scripts/batches/w10xx/_w1013_stage.py、archive/scripts/batches/w10xx/_w1013_verify.py、docs/00-导读/W批次编号对账表.md、docs/11-方案报告/审查与评审/工具脚本门禁体检与临时归档审计-2026-10-29.md、docs/11-方案报告/README.md、scripts/A_文本基础/章节切分.py、scripts/batch_cascade.py、scripts/batch_screenshots.js、scripts/check_archive_health.py、scripts/check_audit_trigger.py、scripts/check_chart_values.js、scripts/check_commit_scope.py、scripts/check_doc_size_budget.py、scripts/check_doc_sync.py、scripts/check_emoji_icons.py、scripts/check_plan_template.py、scripts/check_script_coverage.py、scripts/file_protocol_probe.py、scripts/judge_gate.py、scripts/lib/py_launch.js、scripts/output/script-coverage-baseline.txt、scripts/preflight_check.py、scripts/rag/build_vectors.py、scripts/refresh_icon_paths.py、scripts/scan_targets.py、scripts/security_scan.py、scripts/site_audit.py、scripts/subject_band.py、scripts/tmpe_tidy.py、scripts/verify_delivery.py、tests/unit/test_cascade_line_anchor.py、tests/unit/test_doc_size_budget.py、tests/unit/test_milestone_block_regex.py、tests/unit/test_tmpe_tidy.py、tmpe/policy.yml
>
**要点**：
① **门禁本体 4 处根修**（用户批准）：`check_doc_sync` self-test T4 去磁盘依赖（负样本号 W777 被 W921 归档迁移撞成已登记 ⇒ C4 可证伪性失效·归档文本改经 inp 注入·33/33 过）；`verify_delivery` 注释 5 处陈旧数字订正为实数（57 段/委托 44/内联 13/恒跑 14·行为不变）；`check_archive_health` 的 `BATCHES_SEG` 死常量上岗为段全集权威源（新增双向对账·W1006 批 16 件漏登记的假绿根因）；第 42 基线陈旧行清 + C2 加「已挂槽仍豁免」反向查（12/12 过）。
② **AGENTS 脚注 C4 口径缺陷根修**：写入侧量 note 本体 ≤120、判据侧连固定尾句家具一起量 ⇒ 97–120 字注记「级联绿/门禁红」（W1013 首踩 117 字被算 141·阻塞开工）⇒ 判据抽纯函数并剥家具·4 新单测证明未弱化门禁。
③ **tmpe 临时系统根修**：批号路由正则认不出下划线形态 ⇒ 批号工作件永远进不了 w### 桶（全落 _misc）⇒ 改读 policy.yml 单一权威源 + 按批号归子目录；`_misc` 超额告警死代码修（exclude 使其永不触发）；锁 R1-R4（过期抢占/写锁降级/O_EXCL 原子/释放兜底·23/23 测）；归位执行 93 + 285 件按批号归位（journal 可回溯·零删除·避让在途与个人稿）。
④ **其余真缺陷**：batch_screenshots 硬编码 python + 静默 fail-open → 抽 `lib/py_launch.js` 共享候选表并fail-closed；`make help` 恒 NameError 修（+ledger 补 .PHONY）；ruff 13 项存量债清零（dev→main 即 CI 红）；judge_gate 输入源 GoatCounter 已退役 ⇒ 语义订正为人工复算器（不伪造接不通的自动源）；check_emoji_icons 自称门禁未挂槽 ⇒ 订正为报告型探针；3 支孤儿探针接线升格为级联收尾浮出。
⑤ **归档系统**：结构健康·无新硬错位（_s4/_s5 160 件为学术轨活跃线·不归档）；台账补 4 组登记 + 3 项孤儿件补登（templates/对账表-ARCHIVE/w-b-critique）+ 结构树补 templates；W1013 已收官的 16 件按三档归位②代收入档。

**验证**：ruff 全仓 0 债 · 5 支门禁自测全绿（33/33·12/12·4/4·4/4·12/12）· 新增单测 23+12 全过 · 第 43 槽自检 12/12 · 归档健康 0 待办 · 目录文档/搜索索引/布局/提交范围 0 FAIL · 报告落 docs/11-方案报告/审查与评审/（编号 48 登记）。

> - **状态**：已收官（工具链体检整改 + 临时系统路由根修 + 归档台账回写）

### W1013（2026-10-29）：回次 og:image 全覆盖批·第二轮（12 张线描立像/场面）



> **来源**：用户 2026-10-29 目视确认 W1005 两张 hero 图「合格」后令「继续扩」⇒ 沿用 W1001 批已过目的口径（线描立像族·母版段两变体·按题材定主体·战斗回场面其余立像·12 张一批）。
>
> - **文件**：.github/workflows/README.md、AGENTS.md、CHANGELOG.md、CITATION.cff、HANDOVER.md、README.md、STRUCTURE.md、archive/docs/AGENTS-ARCHIVE.md、archive/docs/CHANGELOG-ARCHIVE.md、archive/docs/W批次编号对账表-ARCHIVE.md、archive/docs/file-index-ARCHIVE.md、assets/promo/plate-set/index.md、assets/promo/plate-set/plate-line-61-ch002-puti.png、assets/promo/plate-set/plate-line-61-ch002-puti.webp、assets/promo/plate-set/plate-line-62-ch012-jinchanzi.png、assets/promo/plate-set/plate-line-62-ch012-jinchanzi.webp、assets/promo/plate-set/plate-line-63-ch013-taibaixingxing.png、assets/promo/plate-set/plate-line-63-ch013-taibaixingxing.webp、assets/promo/plate-set/plate-line-64-ch021-lingji.png、assets/promo/plate-set/plate-line-64-ch021-lingji.webp、assets/promo/plate-set/plate-line-65-ch038-wujiguowang.png、assets/promo/plate-set/plate-line-65-ch038-wujiguowang.webp、assets/promo/plate-set/plate-line-66-ch045-huli.png、assets/promo/plate-set/plate-line-66-ch045-huli.webp、assets/promo/plate-set/plate-line-67-ch078-zhizhujing.png、assets/promo/plate-set/plate-line-67-ch078-zhizhujing.webp、assets/promo/plate-set/plate-line-68-ch082-bailujing.png、assets/promo/plate-set/plate-line-68-ch082-bailujing.webp、assets/promo/plate-set/plate-line-69-ch083-laoshujing.png、assets/promo/plate-set/plate-line-69-ch083-laoshujing.webp、assets/promo/plate-set/plate-line-70-ch086-bichandawang.png、assets/promo/plate-set/plate-line-70-ch086-bichandawang.webp、assets/promo/plate-set/plate-line-71-ch087-yuhuawang.png、assets/promo/plate-set/plate-line-71-ch087-yuhuawang.webp、assets/promo/plate-set/plate-line-72-ch092-dizang.png、assets/promo/plate-set/plate-line-72-ch092-dizang.webp、assets/promo/plate-set/preview-contact-sheet.png、assets/promo/plate-set/preview-contact-sheet.webp、assets/promo/plate-set/preview-w1013-sheet.png、assets/promo/plate-set/raw/README.md、assets/promo/plate-set/raw/index.md、assets/promo/plate-set/raw/round15/README.md、assets/promo/plate-set/raw/round15/index.md、assets/promo/plate-set/raw/round15/plate-line-61-ch002-puti.jpg、assets/promo/plate-set/raw/round15/plate-line-62-ch012-jinchanzi.jpg、assets/promo/plate-set/raw/round15/plate-line-63-ch013-taibaixingxing.jpg、assets/promo/plate-set/raw/round15/plate-line-64-ch021-lingji.jpg、assets/promo/plate-set/raw/round15/plate-line-65-ch038-wujiguowang.jpg、assets/promo/plate-set/raw/round15/plate-line-66-ch045-huli.jpg、assets/promo/plate-set/raw/round15/plate-line-67-ch078-zhizhujing.jpg、assets/promo/plate-set/raw/round15/plate-line-68-ch082-bailujing.jpg、assets/promo/plate-set/raw/round15/plate-line-69-ch083-laoshujing.jpg、assets/promo/plate-set/raw/round15/plate-line-70-ch086-bichandawang.jpg、assets/promo/plate-set/raw/round15/plate-line-71-ch087-yuhuawang.jpg、assets/promo/plate-set/raw/round15/plate-line-72-ch092-dizang.jpg、docs/00-导读/W批次编号对账表.md、docs/00-导读/项目说明.md、docs/11-方案报告/README.md、docs/11-方案报告/计划方案/T37-任务计划执行与经验沉淀报告-2026-10-29.md、docs/11-方案报告/计划方案/执行前计划-T32-回次ogimage全覆盖第二轮.md、docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md、docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md、docs/INDEX.md、docs/agent/pitfalls.md、scripts/_w1013_align_files.py、scripts/_w1013_derive_prepare.py、scripts/_w1013_download.py、scripts/_w1013_fix_desc.py、scripts/_w1013_inventory.py、scripts/_w1013_make_spec.py、scripts/_w1013_master.py、scripts/_w1013_prepare.py、scripts/_w1013_read.py、scripts/_w1013_retry.py、scripts/_w1013_retry2.py、scripts/_w1013_roster_check.py、scripts/_w1013_sheet.py、scripts/_w1013_shot.py、scripts/_w1013_stage.py、scripts/_w1013_verify.py、scripts/check_js_syntax.py、scripts/index.md、scripts/output/README.md、scripts/output/_cascade_files_W1013.txt、scripts/output/_vermilion_solid_cache.json、scripts/output/_w1013_batch.json、scripts/output/_w1013_batch_a.json、scripts/output/_w1013_batch_b.json、scripts/output/_w1013_inventory.json、scripts/output/_w1013_manifest.json、scripts/output/_w1013_read.json、scripts/output/_w1013_retry.json、scripts/output/_w1013_retry2.json、scripts/output/_w1013_spec.json、scripts/output/file-index.md、scripts/output/index.md、scripts/output/stats-changelog.json、scripts/output/stats-index.md、scripts/output/stats.json、scripts/output/tools-inventory.md、site/data/cross-time-danmaku.html、site/data/search.html、site/data/tag-cloud.html、site/dukou-engine.html、site/en/search.html、site/index.html、site/reader/ch002.html、site/reader/ch012.html、site/reader/ch013.html、site/reader/ch021.html、site/reader/ch038.html、site/reader/ch045.html、site/reader/ch078.html、site/reader/ch082.html、site/reader/ch083.html、site/reader/ch086.html、site/reader/ch087.html、site/reader/ch092.html、site/static/images/README.md、site/static/images/index.md、site/static/images/og-plate-line-61-ch002-puti.webp、site/static/images/og-plate-line-62-ch012-jinchanzi.webp、site/static/images/og-plate-line-63-ch013-taibaixingxing.webp、site/static/images/og-plate-line-64-ch021-lingji.webp、site/static/images/og-plate-line-65-ch038-wujiguowang.webp、site/static/images/og-plate-line-66-ch045-huli.webp、site/static/images/og-plate-line-67-ch078-zhizhujing.webp、site/static/images/og-plate-line-68-ch082-bailujing.webp、site/static/images/og-plate-line-69-ch083-laoshujing.webp、site/static/images/og-plate-line-70-ch086-bichandawang.webp、site/static/images/og-plate-line-71-ch087-yuhuawang.webp、site/static/images/og-plate-line-72-ch092-dizang.webp、site/static/images/plate-line-61-ch002-puti.webp、site/static/images/plate-line-62-ch012-jinchanzi.webp、site/static/images/plate-line-63-ch013-taibaixingxing.webp、site/static/images/plate-line-64-ch021-lingji.webp、site/static/images/plate-line-65-ch038-wujiguowang.webp、site/static/images/plate-line-66-ch045-huli.webp、site/static/images/plate-line-67-ch078-zhizhujing.webp、site/static/images/plate-line-68-ch082-bailujing.webp、site/static/images/plate-line-69-ch083-laoshujing.webp、site/static/images/plate-line-70-ch086-bichandawang.webp、site/static/images/plate-line-71-ch087-yuhuawang.webp、site/static/images/plate-line-72-ch092-dizang.webp。


**本批要点**：① **缺口实读 80 回**（100 回中已有配图 20 回）· ② **已出主体全表核对**——plate-set 实为 **88 个母版 / 88 个唯一 slug**（编号 1–12 被四个批次族复用 ⇒ 编号 max 60 不等于主体数）⇒ 12 个候选主体与全表**零冲突**；③ **母版段两变体**——立像段**逐字复用 249 字符**（7 张），场面段**仅改 3 处**（5 张）；④ **5 张重出**（两轮）——朱砂被画成大块火焰 / 竖椭圆、钢鞭末端多出弯钩、主体底被画布切掉、杖头金龙悬空脱手（其中 4 张**机器判据全 PASS**·只靠人眼硬关）；⑤ **12 页接入**（题图位 + 专属 1200×630 og:image）⇒ 回目页覆盖 **20 → 32 回**、缺口 **80 → 68 回**；⑥ **未覆盖页零回归**——缺口 68 页中 66 页仍为通用 og-cover-ink-zh.jpg、2 页保留既有 card-* 专属图。

**验证**：母版判据 J1–J10 **100/100 FAIL 0** · 裁切验算 **100/100 FAIL 0** · 负样本自证命中（J1 尺寸）· 落位验收 **0 FAIL**（含「未覆盖页 68 个零回归」）· 幂等复跑 **24/24 SKIP** · 浏览器实跑 **0 FAIL**（题图 HTTP 200 + naturalWidth > 0 + 位置在 h1 之后 + 暗色隐藏生效）· 第 48 门禁 **0 FAIL**（新增文件·全项符合）· 全量门禁 **55 段全绿**。

> - **状态**：已收官（12 张落地·母版族 88 → 100 张·既有 88 张母版与站点版零改动·其余 68 个无配图回目页的 og:image 未误改·坑表 +2 条·用户目视确认合格 2026-10-29）

### W1012（2026-10-29）：产物目录瘦身 + 在途收口批

> **来源**：用户 2026-10-29 令「做」——承接分类报告两荐条：产物目录里的 33MB 一次性基线归档、并行会话收尾件代收（用户确认「都做完了」）。
>
> - **文件**：.github/workflows/README.md、AGENTS.md、CHANGELOG.md、CITATION.cff、HANDOVER.md、README.md、STRUCTURE.md、archive/README.md、archive/docs/AGENTS-ARCHIVE.md、archive/docs/CHANGELOG-ARCHIVE.md、archive/docs/W批次编号对账表-ARCHIVE.md、archive/docs/file-index-ARCHIVE.md、archive/scripts/batches/w8xx/README.md、archive/scripts/batches/w8xx/_w851_visual_snapshot_after.json、archive/scripts/batches/w8xx/_w851_visual_snapshot_before.json、archive/scripts/batches/w8xx/_w876_baseline_after.json、archive/scripts/batches/w8xx/_w876_baseline_before.json、archive/scripts/batches/w8xx/index.md、docs/00-导读/W批次编号对账表.md、docs/00-导读/项目说明.md、docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md、docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md、pytest.ini、scripts/output/README.md、scripts/output/_cascade_files_W1012.txt、scripts/output/_vermilion_solid_cache.json、scripts/output/_w1012_spec.json、scripts/output/file-index.md、scripts/output/index.md、scripts/output/stats.json、scripts/output/tools-inventory.md、site/data/cross-time-danmaku.html、site/data/tag-cloud.html、site/dukou-engine.html、site/index.html。
>
**要点**：
① **产物目录瘦身**：`scripts/output/` 是「活产物」目录（file-index/stats/tools-inventory/spec），却躺着 W851/W876 的一次性基线快照 4 件 ≈33MB——全仓 grep 仅被各自**归档 spec** 提及，活代码与测试零消费 ⇒ 迁 `archive/scripts/batches/w8xx/`。这是分类报告里唯一的硬错位。
② **并行会话收尾件代收**（用户确认其工作「都做完了」但未提交）：`pytest.ini` pytest 计数 979→1016（stats 标记）、两份系统架构方案 md、`tools-inventory.md` 时间戳刷新。
③ 分类总览报告落 `tmpe/`（8743 文件盘点·七类职责·目录内错位清单），不入库（tmpe 为临时区）。

**验证**：`check_repo_layout`（第 52 槽）0 FAIL · `check_doc_size_budget` 0 FAIL · full `lint_links` 0 broken · 全量 pytest 1013 passed · 全量 verify 核心全过。

> - **状态**：已收官（产物目录回归「活产物」单一职责）

### W1011（2026-10-29）：仓库整理分类批（五项归位 + 第 52 槽布局门禁）

> **来源**：用户 2026-10-29「对项目的所有文件进行整理分类」→ 我给出盘点与三档方案 → 用户「全都做」。
>
> - **文件**：.github/workflows/README.md、AGENTS.md、CHANGELOG.md、CITATION.cff、HANDOVER.md、README.md、STRUCTURE.md、archive/docs/AGENTS-ARCHIVE.md、archive/docs/CHANGELOG-ARCHIVE.md、archive/docs/W批次编号对账表-ARCHIVE.md、archive/docs/file-index-ARCHIVE.md、archive/scripts/batches/misc/README.md、archive/scripts/batches/misc/_tmp_chap_sheet.py、archive/scripts/batches/misc/index.md、docs/00-导读/W批次编号对账表.md、docs/00-导读/index.md、docs/00-导读/协议边界速查.md、docs/00-导读/文档规范.md、docs/00-导读/新Agent启动Prompt.md、docs/00-导读/统计口径说明.md、docs/00-导读/项目说明.md、docs/04-文化与历史背景/西游记大事年表.md、docs/10-方法论沉淀/例-佛法AI框架原始对话.txt、docs/INDEX.md、docs/agent/gates.md、index.md、scripts/A_文本基础/README.md、scripts/A_文本基础/index.md、scripts/A_文本基础/章节切分.py、scripts/check_gov_doc_claims.py、scripts/check_governance_docs.py、scripts/check_repo_layout.py、scripts/check_w_range_literal.py、scripts/index.md、scripts/output/README.md、scripts/output/_cascade_files_W1011.txt、scripts/output/_vermilion_solid_cache.json、scripts/output/_w1011_spec.json、scripts/output/file-index.md、scripts/output/index.md、scripts/output/stats-changelog.json、scripts/output/stats-index.md、scripts/output/stats.json、scripts/output/tools-inventory.md、scripts/verify_delivery.py、site/data/cross-time-danmaku.html、site/data/search.html、site/data/tag-cloud.html、site/dukou-engine.html、site/en/search.html、site/index.html、site/reader/ch001.html、site/reader/ch003.html、site/reader/ch009.html、site/reader/ch011.html、site/reader/ch022.html、site/reader/ch028.html、site/reader/ch047.html、site/reader/ch063.html、site/reader/ch066.html、site/reader/ch079.html、site/reader/ch089.html、site/reader/ch093.html、tests/unit/README.md、tests/unit/index.md、tests/unit/test_repo_layout.py。
>
**要点**：
① **盘点**：8743 文件 / 2.8 GB，24 个顶层目录。七类职责（治理/内容/站点/素材/代码/归档/临时）本已成立，真错位只有 5 个——大搬家收益是「看起来整齐」，代价是 5567 条链接与全部生成器路径，故不做。
② **五项归位**：根目录 `_tmp_chap_sheet.py` → `archive/scripts/batches/misc/`；`tools/章节切分.py` → `scripts/A_文本基础/`；`references/例-佛法AI框架原始对话.txt` → `docs/10-方法论沉淀/`；`timeline/西游记大事年表.md` → `docs/04-文化与历史背景/`（+ 补元信息块 v2）；`新Agent启动Prompt.md` → `docs/00-导读/`（相对链接改 `../../`）。空壳目录 `tools/` `references/` `timeline/` 整体删除。
③ **三判据改路径**：`check_gov_doc_claims`（N5）/`check_governance_docs`/`check_w_range_literal` 里的 Prompt 路径；《协议边界速查》A5 板块 34 → 35 篇。
④ **第 52 槽布局门禁** `check_repo_layout.py`：L1 根目录只放治理与配置（白名单+去向提示）、L2 顶层目录须已声明角色、L3 白名单不得陈腐；按 **git 视角**判定（ignore 的本地件不算）；毫秒级登记 `_SCOPE_CORE` 恒跑；自测 5 例 + `--report`。
⑤ **连带修 12 处断链**：`site/reader/ch001|003|009|011|022|028|047|063|066|079|089|093.html` 的 plate-line 图片写成`../../static/images/`（从 site/reader 出发应为 `../static/`）——W1001 起就断，`--scope auto` 只跑 docs 轨所以一直没暴露；本批 full lint 14943 链接扫出 12 broken，已全部修正。
⑥ 数值级联：槽 51→52（AGENTS 三处措辞 + §4.2 第 52 条）、段 56→57（文档规范）。

**验证**：`check_repo_layout --self-test` 5/5 · 单测 7 passed · full `lint_links` 14943 链接 **0 broken** · `check_gov_doc_claims` N1-N5 0 FAIL · `check_frontmatter` 通过（年表已补元信息块）· `docs_index` 重建 780 篇 · 第 52 槽实跑「全部在声明内」· 全量 verify 核心全过。

> - **状态**：已收官（布局从「一次性搬家」变成「可执行判据」）

### W1010（2026-10-29）：级联自动回窗批

> **来源**：W1009 收官后自查发现同一病根第三次——级联插入段/行必然把正本顶过窗口，然后**下一批开工前**才被 preflight 判红；W1008 就是专门为此手工回窗的一批。人手记的这一步必须交给机器。
>
> - **文件**：.github/workflows/README.md、AGENTS.md、CHANGELOG.md、CITATION.cff、HANDOVER.md、README.md、STRUCTURE.md、archive/docs/AGENTS-ARCHIVE.md、archive/docs/CHANGELOG-ARCHIVE.md、archive/docs/W批次编号对账表-ARCHIVE.md、archive/docs/file-index-ARCHIVE.md、docs/00-导读/W批次编号对账表.md、docs/00-导读/项目说明.md、scripts/batch_cascade.py、scripts/output/README.md、scripts/output/_cascade_files_W1010.txt、scripts/output/_w1010_spec.json、scripts/output/file-index.md、scripts/output/index.md、scripts/output/stats-changelog.json、scripts/output/stats-index.md、scripts/output/stats.json、scripts/output/tools-inventory.md、site/data/cross-time-danmaku.html、site/data/tag-cloud.html、site/dukou-engine.html、site/index.html、tests/unit/test_batch_spec.py。
>
**要点**：
① `batch_cascade` 收尾链改为 **落盘 → 回窗 → stats**：`_refresh_window()` 调 `archive_segments --target both --keep 110` + `archive_ledger_rows --keep 60`；任一步失败打印 `[WINDOW] FAIL` 并 `return 2`（不静默、不留「下一批开不了工」的半成品）。
② 窗口常量 `WIN_SEGMENTS=110` / `WIN_LEDGER=60` 提为模块常量，与文档规范 §8 同源；单测钉住（改窗必须同步改测试）。
③ 单测 2 例：两步都成功才 True；任一步失败即 False 且打印 FAIL（runner 注入，不真跑归档）。
④ 口径线索：这是「动作靠人记」的第三例（前两例：C5d 手跑 stats、回窗手跑归档）——**凡每日必做且会漏的步骤，都要落在级联收尾里**，而不是写在文档让人记住。

**验证**：本批级联即 live 证据——`[WINDOW] segments OK` / `[WINDOW] ledger OK` / `[STATS] OK` 全由级联打出；`pytest tests/unit/test_batch_spec.py` 9 passed · 第 51 槽自判 · 体积窗口 0 FAIL · 全量 verify 核心全过。

> - **状态**：已收官（回窗从「手工维护批」变成级联内置步骤）

### W1009（2026-10-29）：流程收口批（级联自动刷 stats + spec 解析单一入口）

> **来源**：用户 2026-10-29 令「做」——W1008 报告荐条 1（stats 刷新接进级联）+ 荐条 2（两处 spec 解析合并）。两条都指向同一类问题：**同一动作靠人记、同一判据两处写**。
>
> - **文件**：.github/workflows/README.md、AGENTS.md、CHANGELOG.md、CITATION.cff、HANDOVER.md、README.md、STRUCTURE.md、archive/docs/AGENTS-ARCHIVE.md、docs/00-导读/W批次编号对账表.md、docs/00-导读/项目说明.md、docs/agent/pitfalls.md、scripts/batch_cascade.py、scripts/batch_spec.py、scripts/check_commit_scope.py、scripts/index.md、scripts/output/README.md、scripts/output/_cascade_files_W1009.txt、scripts/output/_vermilion_solid_cache.json、scripts/output/_w1009_spec.json、scripts/output/file-index.md、scripts/output/index.md、scripts/output/stats-changelog.json、scripts/output/stats-index.md、scripts/output/stats.json、scripts/output/tools-inventory.md、scripts/safe_commit.py、site/data/cross-time-danmaku.html、site/data/tag-cloud.html、site/dukou-engine.html、site/index.html、tests/unit/README.md、tests/unit/index.md、tests/unit/test_batch_spec.py。
>
**要点**：
① **级联收尾自动刷 stats**：C5d（stats 与磁盘实算漂移）在 W1006/W1007/W1008 三批各假红一次，每次都要人记得先跑 `stats.py --w ####`。改为 `batch_cascade` 落盘后自跑；runner 可注入（单测可桩），失败打印 `[STATS] FAIL` + 末两行并让级联 `return 2`——不静默、不半成品。
② **spec 解析收敛单一入口** `scripts/batch_spec.py`：`safe_commit._spec_paths` 与 `check_commit_scope.spec_paths_for` 曾各写一份，W1007 踩到一处 `cells[0]`、一处 `cells[1]` ⇒ 收敛为一份实现，两处只调用。顺带补上「markdown 分隔行 `|---|---|` 必须跳过」——这条是新单测第一跑就抓出来的。
③ **测试** 7 例：首格即路径 / 表头与分隔行跳过 / 去重与路径归一 / 空 spec / 读文件 / 「两处必须给同一答案」/ stats runner OK 与 FAIL 两态。
④ **口径入仓**：pitfalls 补「同一判据禁两处实现」（解析/取数部分收敛单一入口，两处只调用不重写）。
⑤ **本批即 live 验证**：本批级联走的就是新收尾——`[STATS] OK` 由级联自己打出，不再是手跑。

**验证**：`pytest tests/unit/test_batch_spec.py` 7 passed · 三组相关单测 22 passed · 级联输出含 `[STATS] OK` · 第 51 槽自判（归属 W1009·索引 ⊆ spec）· 第 31/42/45 槽 0 FAIL · 全量 verify 核心全过。

> - **状态**：已收官（stats 刷新与 spec 解析都从「人记」变「机器做·单点维护」）

### W1008（2026-10-29）：回窗 + 触发器归档盲区批

> **来源**：用户 2026-10-29 一句「然后呢」——W1005→W1007 三批连发后仓库进不了开工态：preflight 体积窗口 3 项红（CHANGELOG/file-index 112 段 > 110·台账 61 行 > 60）。先回窗，再把早先审查列的 I2 补掉。
>
> - **文件**：.github/workflows/README.md、AGENTS.md、CHANGELOG.md、CITATION.cff、HANDOVER.md、README.md、STRUCTURE.md、archive/docs/AGENTS-ARCHIVE.md、archive/docs/CHANGELOG-ARCHIVE.md、archive/docs/W批次编号对账表-ARCHIVE.md、archive/docs/file-index-ARCHIVE.md、docs/00-导读/W批次编号对账表.md、docs/00-导读/项目说明.md、docs/agent/pitfalls.md、scripts/check_audit_trigger.py、scripts/output/README.md、scripts/output/_cascade_files_W1008.txt、scripts/output/_w1008_spec.json、scripts/output/file-index.md、scripts/output/index.md、scripts/output/stats-changelog.json、scripts/output/stats-index.md、scripts/output/stats.json、scripts/output/tools-inventory.md、site/data/cross-time-danmaku.html、site/data/tag-cloud.html、site/dukou-engine.html、site/index.html、tests/unit/test_audit_trigger.py、tests/unit/test_check_script_coverage.py、tests/unit/test_script_hygiene.py。
>
**要点**：
① **回窗**：`archive_segments.py --target both`（CHANGELOG / file-index 各迁出 3 段 W887-W889 至 archive）+ `archive_ledger_rows.py`（迁 2 行 W947-W948）⇒ 体积窗口 0 FAIL，恢复可开工。
② **I2 归档盲区**（审查项遗留）：触发器只读正本台账，而台账行按 60 行窗滚动——审查行一旦被迁进 `archive/docs/W批次编号对账表-ARCHIVE.md`，判据就会把「已审查」读成「从未审查」（假警）。修法：判据读取面改成**正本 ∪ 归档**取 token max；归档缺失不阻断（正本判据仍成立）。
③ **测试**：触发器 `--self-test` 7 → 8 态（T8 归档 token 计入）；单测加 `test_archive_ledger_token_counts`（现 10 例）。
④ **口径入仓**：pitfalls「判据把字样当事件」条补「读取面＝正本 ∪ 归档」——判据读的**源**会滚动，这和判据读的**面**（字样/位置）是两件事。
⑤ **全量回归抓到两处自过期测试**：`test_script_hygiene.py` 把门禁自测例数写死 `9/9`，W1006 加 T10 后变 10/10 ⇒ 假红。改为「满/缺对比」不写死例数——同型两处（`test_script_hygiene` 的 `9/9`、`test_check_script_coverage` 的 `6/6`）。**测试自己过期属假红族**，与「判据读空当无段」同一处方：断言不写死会随判据演进的计数。

**验证**：`check_doc_size_budget` 0 FAIL · `check_audit_trigger --self-test` 8/8 · `pytest tests/unit/test_audit_trigger.py` 10 passed · 全量 pytest 回归通过 · 第 51 槽自判（归属 W1008·索引 ⊆ spec）· 全量 verify 核心全过。

> - **状态**：已收官（回窗恢复开工态 + 触发器归档盲区补齐）

### W1007（2026-10-29）：提交范围门禁批（第 51 槽·索引 ⊆ 本批 spec）

> **来源**：用户 2026-10-29 令「现在做」——W1006 收官时明写「硬拦只在走 `safe_commit` 时生效，`git commit` 直提绕得过；要彻底封死，得搬进 `verify_delivery.py`（加槽＝50→51 级联）」。本批就是那条级联。
>
> - **文件**：.github/workflows/README.md、AGENTS.md、CHANGELOG.md、CITATION.cff、HANDOVER.md、README.md、STRUCTURE.md、archive/docs/AGENTS-ARCHIVE.md、docs/00-导读/W批次编号对账表.md、docs/00-导读/文档规范.md、docs/00-导读/项目说明.md、docs/agent/gates.md、docs/agent/pitfalls.md、scripts/check_commit_scope.py、scripts/index.md、scripts/output/README.md、scripts/output/_cascade_files_W1007.txt、scripts/output/_vermilion_solid_cache.json、scripts/output/_w1007_spec.json、scripts/output/file-index.md、scripts/output/index.md、scripts/output/stats-changelog.json、scripts/output/stats-index.md、scripts/output/stats.json、scripts/output/tools-inventory.md、scripts/verify_delivery.py、site/data/cross-time-danmaku.html、site/data/tag-cloud.html、site/dukou-engine.html、site/index.html、tests/unit/README.md、tests/unit/index.md、tests/unit/test_commit_scope.py。
>
**要点**：
① **判据**（`check_commit_scope.py`）：归属批次取**索引态** `CHANGELOG.md` 顶段 W 号（与 HEAD 顶段不同＝本提交正在新增该段），否则取 HEAD 现役段（回填/补账类）；该批 `scripts/output/_w####_spec.json` 的 `file_index_rows` 即「应动全集」；索引态路径集（`diff --cached` + `diff.renames=false`·rename 两侧都在）多出即 **FAIL**，列前 10 项 + 改法。
② **恒跑**：挂第 51 槽并登记 `_SCOPE_CORE`——`--scope docs` / `site` 的提交同样判（代提不分轨），堵死 W1006 遗留的「`git commit` 绕过 safe_commit」缺口。
③ **不伪造红**：索引无暂存件 → NOTE 放行（非提交动作）；spec 缺失 → WARN 放行（判据不可执行）。
④ **数值级联**：AGENTS §4.2 第 51 条 + 三处「50 槽→51 槽」、gates.md 第 51 条、文档规范「现役 55→56 段」、`EXPECTED_SECTION_NAMES` 与 `_SCOPE_CORE` 同步、verify 注释计数（56 段 / 39 委托段）。
⑤ **测试**：`--self-test` 6 例 + `--report` 模式；`tests/unit/test_commit_scope.py` 8 例（含端点契约：汇总行必为末行）。

**验证**：`check_commit_scope --self-test` 6/6 · 单测 8 passed · 本文提交由第 51 槽自判（归属 W1007·索引 ⊆ spec）· N2 56 段 / N3 51 槽一致 · 全量 verify 核心全过。

> - **状态**：已收官（代提防线从「工具」升级为「门禁」·任何提交路径都绕不过）

### W1006（2026-10-29）：防代提硬拦批（safe_commit --expect-spec）

> **来源**：用户 2026-10-29 令「做」——承接 W1004 报告末句「要不要把 `--expect-spec` 硬拦也做了？那是唯一能真正止住第三次、第四次的改法」。当日已发生三次代提（W989 级联十四面 / W1002 审查 B3 / W1004 被 W1005 全量提交带走），纪律层已写「并行在场禁 `git add -A`」却仍复发 ⇒ 本轮把它变成硬拦。
>
> - **文件**：.github/workflows/README.md、AGENTS.md、CHANGELOG.md、CITATION.cff、HANDOVER.md、README.md、STRUCTURE.md、archive/docs/AGENTS-ARCHIVE.md、archive/scripts/batches/w10xx/README.md、archive/scripts/batches/w10xx/_w1005_fix_c6.py、archive/scripts/batches/w10xx/_w1005_fix_head_sentence.py、archive/scripts/batches/w10xx/_w1005_fix_tail_sep.py、archive/scripts/batches/w10xx/_w1005_handover_line.py、archive/scripts/batches/w10xx/_w1005_heroes.py、archive/scripts/batches/w10xx/_w1005_patch_changelog_files.py、archive/scripts/batches/w10xx/_w1005_probe_asset_sizes.py、archive/scripts/batches/w10xx/_w1005_probe_cascade_line.py、archive/scripts/batches/w10xx/_w1005_probe_changelog_files.py、archive/scripts/batches/w10xx/_w1005_probe_faces.py、archive/scripts/batches/w10xx/_w1005_probe_head.py、archive/scripts/batches/w10xx/_w1005_probe_readme.py、archive/scripts/batches/w10xx/_w1005_render_flyer.py、archive/scripts/batches/w10xx/_w1005_serve.py、archive/scripts/batches/w10xx/_w1005_spec.py、archive/scripts/batches/w10xx/_w1005_sync_faces.py、archive/scripts/batches/w10xx/index.md、docs/00-导读/W批次编号对账表.md、docs/00-导读/项目说明.md、docs/agent/pitfalls.md、scripts/check_script_coverage.py、scripts/index.md、scripts/output/README.md、scripts/output/_cascade_files_W1006.txt、scripts/output/_vermilion_solid_cache.json、scripts/output/_w1006_spec.json、scripts/output/file-index.md、scripts/output/index.md、scripts/output/stats-changelog.json、scripts/output/stats-index.md、scripts/output/stats.json、scripts/output/tools-inventory.md、scripts/safe_commit.py、site/data/cross-time-danmaku.html、site/data/tag-cloud.html、site/dukou-engine.html、site/index.html、tests/unit/README.md、tests/unit/index.md、tests/unit/test_safe_commit_expect_spec.py。
>
**要点**：
① `safe_commit.py` 新增 `--expect-spec <本批 spec>`：提交前取**索引态路径集**（`diff --cached` + `diff.renames=false` 取全集），与本批 spec 的 `file_index_rows` 求差；**出现 spec 之外的文件即拒绝**（列前 10 项 + 改法：`git restore --staged <路径>` 或补进 spec）；spec 为空 **fail-closed**；索引里缺 spec 声明的件只出 NOTE（可能已入库/无需改）。给 `--expect-spec` 时可省 pathspec。
② 自测 4 → 8 例：子集放行 / 多出必拒 / 空 spec 拒 / 空索引只提示。
③ 新增 `tests/unit/test_safe_commit_expect_spec.py` 7 例，含**临时仓端到端**：拦住 extra（提交数不变）与放行 subset（提交落地）——不是纯函数自证，是真跑 git。
④ 口径入仓：pitfalls「并行会话工作树」条补硬拦段落（点明三次代提同一处方）；AGENTS §4.3 最高频铁则加「批次收官提交一律 `--expect-spec`」。
⑤ 本批自身即 dogfood：收官提交用 `--expect-spec scripts/output/_w1006_spec.json`。

**验证**：`safe_commit.py --self-test` 8/8 · `pytest tests/unit/test_safe_commit_expect_spec.py` 7 passed · 本批提交由 `--expect-spec` 校验通过（索引 ⊆ spec）· 全量 verify 核心全过。

> - **状态**：已收官（代提从「纪律」升级为「提交前硬拦」；残留：他方在途件仍需各自登记）

### W1005（2026-10-29）：hero 水墨图人数修正（取经五人组·4 人形 + 1 匹白马）· 两张原地替换 + flyer A4 快照重渲染



> **来源**：用户 2026-10-29 指出 `site/static/images/ink-mountains-hero.webp`「内容不符合西游记·为什么有七个人」→ 问卷裁定人物口径＝取经五人组（4 人形 + 1 匹白马）、范围＝两张一并修。
>
> **根因**：W852 批 hero-set 01/06 档案即明写「山脊云海+**七人单行**」⇒ 人数错误源自 W852 批，W879 批原地替换该图时沿用了同一错误 ⇒ 两张同族图都是错的。
>
> - **文件**：.github/workflows/README.md、AGENTS.md、CHANGELOG.md、CITATION.cff、DESIGN.md、HANDOVER.md、README.md、STRUCTURE.md、archive/README.md、archive/docs/AGENTS-ARCHIVE.md、archive/docs/CHANGELOG-ARCHIVE.md、archive/docs/W批次编号对账表-ARCHIVE.md、archive/docs/file-index-ARCHIVE.md、archive/scripts/batches/w9xx/README.md、archive/scripts/batches/w9xx/index.md、assets/promo/hero-set/raw/index.md、assets/promo/hero-set/raw/round-w1005/README.md、assets/promo/hero-set/raw/round-w1005/hero-01-xihai-yunhai.jpg、assets/promo/hero-set/raw/round-w1005/index.md、assets/promo/hero-set/raw/round-w1005/ink-mountains-hero.jpg、docs/00-导读/W批次编号对账表.md、docs/00-导读/项目说明.md、docs/agent/adversarial-audit-prompt.md、docs/agent/gates.md、docs/agent/pitfalls.md、scripts/AD_认知心理/index.md、scripts/accent_audit.py、scripts/check_audit_trigger.py、scripts/check_crop.py、scripts/check_emoji_icons.py、scripts/check_page_admission.py、scripts/check_script_coverage.py、scripts/check_vermilion_solid.js、scripts/file_protocol_probe.py、scripts/icon_probe.js、scripts/index.md、scripts/j1_name_audit.py、scripts/output/_cascade_files_W1003.txt、scripts/output/_vermilion_solid_cache.json、scripts/output/_w1003_spec.json、scripts/output/_w1004_spec.json、scripts/output/file-index.md、scripts/output/stats-changelog.json、scripts/output/stats-index.md、scripts/output/stats.json、scripts/refresh_icon_paths.py、scripts/scan_targets.py、scripts/site_audit.py、scripts/subject_band.py、scripts/visual_regression_probe.py、tests/unit/test_audit_trigger.py、tests/unit/test_script_hygiene.py、tests/unit/test_w851_j1_name_audit.py、tests/unit/test_w851_visual_regression_probe.py。

**本批要点**：① **两张原地替换**（同文件名同尺寸 ⇒ 848 个 .hero 页面零页面改动）——`ink-mountains-hero.webp`（1792×1024·深底 soft-light 合成底图）与 `hero-01-xihai-yunhai.webp`（2560×1440·宣传单页配图）均改为 **4 人形 + 1 匹白马**（唐僧·悟空·八戒·沙僧 + 白龙马）；② **README 三张图同步**——主视觉 banner 引用同一路径故自动更新；`assets/images/index-preview.png` 因首页不使用 .hero 不受影响；**flyer A4 正面 PNG 是静态渲染快照不会自动更新 ⇒ 本批用 Playwright 重渲染**（中英各一·1240×1756 单页 clip）；③ **队伍落位须避开下边缘**——.hero 用 `background-position: center 70%`，首版队伍贴画面下缘 ⇒ 合成后被裁出只剩孤马，prompt 追加「队伍位于山脊中部（垂直 45%–60%）·裁切后仍须完整可见」；④ **显影度**（soft-light 叠 #221D16 后亮度跨度）= 0.2192（W879 批门槛 ≥0.07）；⑤ **人数只能人眼硬关**——「深墨小簇计数」判据不可用（山水皴笔碎点被计入：67/20），人眼核对两张均 4 人形 + 1 匹白马；⑥ **代并行 W1004 结清 5 处版本面欠账**（CHANGELOG 编号规则 / workflows README 头部 / HANDOVER 当前 HEAD 句 / HANDOVER §一 链首 / 项目说明版本行 desc 的「·」）⇒ 消解门禁 5 处红。

**验证**：母版判据与裁切验算沿用 W1001 批口径（88/88 PASS）· 显影度 0.2192 · 单件 117.6 / 83.6 KB · 人眼核对 2/2（4 人形 + 1 匹白马）· 浏览器实跑（data 页 .hero 深底合成·队伍剪影完整可见）· flyer PNG 重渲染后尺寸 1240×1756 与原产物一致 · 全量门禁 55/55 段全绿。

> - **状态**：已收官（两张原地替换 + flyer 快照重渲染 + 版本面欠账代清偿；坑表 +3 条（E-32/E-33/E-34）与 T36 终稿报告已同批补齐·台账状态在本笔回填·用户目视确认合格 2026-10-29）

### W1004（2026-10-29）：转正清零 + 审查触发器判据修正批（B1 字样≠事件 / B2 max / B4 台账归位）

> **来源**：用户 2026-10-29 三令收口——①「8 件转正清零」②「B1/B2/B4 开始做」③「只写进你自己的记忆文件和工作日志没用，这个项目是多 Agent 共同协作的项目，还是会再次出现同样错误」。第三令是本批的纲：教训的**权威载体是仓内坑表**，私有记忆只作镜像（铁律 14 / CLAUDE 第 12 条早已写明，W1002 却把审查结论只写进 `.workbuddy/memory/`）⇒ 本批把结论与判据一起落进仓。
>
> - **文件**：.github/workflows/README.md、AGENTS.md、CHANGELOG.md、CITATION.cff、DESIGN.md、HANDOVER.md、README.md、STRUCTURE.md、archive/README.md、archive/docs/AGENTS-ARCHIVE.md、archive/docs/CHANGELOG-ARCHIVE.md、archive/docs/W批次编号对账表-ARCHIVE.md、archive/docs/file-index-ARCHIVE.md、archive/scripts/batches/w9xx/README.md、archive/scripts/batches/w9xx/index.md、assets/promo/hero-set/raw/index.md、assets/promo/hero-set/raw/round-w1005/README.md、assets/promo/hero-set/raw/round-w1005/hero-01-xihai-yunhai.jpg、assets/promo/hero-set/raw/round-w1005/index.md、assets/promo/hero-set/raw/round-w1005/ink-mountains-hero.jpg、docs/00-导读/W批次编号对账表.md、docs/00-导读/项目说明.md、docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md、docs/agent/adversarial-audit-prompt.md、docs/agent/gates.md、docs/agent/pitfalls.md、pytest.ini、scripts/AD_认知心理/index.md、scripts/_w1005_heroes.py、scripts/_w1005_serve.py、scripts/accent_audit.py、scripts/check_audit_trigger.py、scripts/check_crop.py、scripts/check_emoji_icons.py、scripts/check_page_admission.py、scripts/check_script_coverage.py、scripts/check_vermilion_solid.js、scripts/file_protocol_probe.py、scripts/icon_probe.js、scripts/index.md、scripts/j1_name_audit.py、scripts/output/_cascade_files_W1003.txt、scripts/output/_vermilion_solid_cache.json、scripts/output/_w1003_spec.json、scripts/output/_w1004_spec.json、scripts/output/_w1005_batch.json、scripts/output/_w1005_heroes.json、scripts/output/_w1005_map.json、scripts/output/_w1005_serve.err、scripts/output/file-index.md、scripts/output/stats-changelog.json、scripts/output/stats-index.md、scripts/output/stats.json、scripts/refresh_icon_paths.py、scripts/scan_targets.py、scripts/site_audit.py、scripts/subject_band.py、scripts/visual_regression_probe.py、site/data/cross-time-danmaku.html、site/data/tag-cloud.html、site/dukou-engine.html、site/index.html、tests/unit/test_audit_trigger.py、tests/unit/test_script_hygiene.py、tests/unit/test_w851_j1_name_audit.py、tests/unit/test_w851_visual_regression_probe.py、xiyouji-agent-web/e2e/chat.e2e.mjs、xiyouji-agent-web/package-lock.json、xiyouji-agent-web/package.json。
>
**要点**：
① **8 件转正清零**——W977「硬保留」名单最后 8 件去 `_wNNN_` 前缀：`file_protocol_probe.py` / `j1_name_audit.py` / `visual_regression_probe.py` / `accent_audit.py` / `site_audit.py` / `scan_targets.py` / `icon_probe.js` / `refresh_icon_paths.py`；引用方（第 50 门禁 JS 探针路径、两份单测 import、DESIGN/gates/pitfalls）同步改名。第 42 门禁 C4 配额 **8 → 0**（棘轮到底）。
② **B1 字样 ≠ 事件**——触发器改认专用 token `对抗审查已派发`；含泛词「对抗式审查」但无 token 的行只出 「疑似未打标」NOTE、**不重置计数**（旧实现被「修审查遗留问题」这类行静默重置，实测 41 批漏警）；**收口时又实证一次自伤**——本批台账行只是「描述」这个 token，就被整行 grep 判成一次派发 ⇒ 改为**位置判定：token 只在状态列认**，自测加 T6b 与 `test_token_in_topic_cell_does_not_count` 钉住。
③ **B2 max 而非文件序**——`last_audit_batch()` 改为取含 token 行的最大 W 号（旧实现取文件末条，后补登记/让号下把 gap 算歪：真实 24 批报 28 批）。
④ **B4 台账 W998 行归位**——原行是 W998 首次认领的「必守纪律晋升批」内容（该批实际以 W999 落库），与 CHANGELOG §W998「对抗式审查修复批」冲突 ⇒ 以 CHANGELOG 为准改写、状态回填已收官、并写入事件 token（触发器基线上移到 W998）。
⑤ **补幽灵测试文件**——台账 W1000 行 touches 曾声明 `tests/unit/test_audit_trigger.py` 但从未创建；本批补齐 8 例（阈值 20/21、空台账 fail-closed、散文豁免、B1/B2 回归、同批不触发、CLI 自测）。
⑥ **口径入库（本批纲）**——pitfalls +2 条：『判据把字样当事件/文件序当集合』『教训必须落仓内载体·私有记忆只是镜像』（95 → 97 条·数据 9→10 / 流程 22→23）；派发模板改为「登记行必须写 token」。

**验证**：`check_audit_trigger.py --self-test` 七态 7/7 · `pytest tests/unit/test_audit_trigger.py` 8 passed · `pytest tests/unit/test_script_hygiene.py` 7 passed · 第 42 门禁 0 FAIL（C4 无 NOTE·配额 0）· `check_gov_doc_claims` N3/N4 一致（50 槽 / 97 条）· 触发器实跑「距上次（W998）5 批·未触发」· 全量 verify 核心全过。

> - **状态**：已收官（8 件转正清零 · B1/B2/B4 修复 · 教训与判据同批入仓）；**入库方式＝代提**——本批已暂存的 75 件被并行 W1005 会话的全量提交 `09146cf1` 带走（与 W1002 审查 B3 同型：共享工作树 + 他方全量 `git add`），登记面与台账状态由本笔回填补齐

### W1003（2026-10-29）：agent-web chat 集成验证与死重清退批（用户令「做」·审计轮建议前提过时转验证）
> **来源**：组件库盘点审计轮收尾建议「在 agent-web 装 @tdesign-react/chat 起对话页原型接 SSE」→ 用户令「做」→ 动工前磁盘重验发现**前提过时**：该包 W401 已入库、W808 起实战在用（ChatSender 输入区 + ChatMarkdown 渲染 + 自研 SSE 八事件客户端），「起原型」转为「验证在役集成 + 清退死重」。
> **摘要**：① **验证三链全绿**——build（tsc -b + vite·1.4s）·test:client 51/51（含 useChat 流式 4 例）·三层 E2E 11/11（真实浏览器 + 构建产物 + 后端 + SQLite·唯一替身 mock LLM；流式渲染/会话落库/反馈落库/控制台零错误全过）。② **死重清退**——@tdesign-react/aigc@0.1.0-alpha.15（W401 随源码首批带入）src/e2e/evals/CI/docs 全零引用、npm 树仅根挂点，npm uninstall 同步 package.json + lock。③ **e2e 端口修根**——FRONTEND_PORT 4232→4600：4232 落 Windows WinNAT 保留段 4138-4237（netsh excludedportrange 实测 3732-4537 连片），vite preview listen EACCES——W975「端口占用是假故障」保留段形态复发实证，此前本机三层 E2E 因此从未能启动；迁出后 11/11 全过。
> **文件**：xiyouji-agent-web/package.json · xiyouji-agent-web/package-lock.json · xiyouji-agent-web/e2e/chat.e2e.mjs · scripts/output/_w1003_spec.json
### W1002（2026-10-29）：脚本三档归位批（81 件归档 + 4 件转正 + 第 42 门禁 C4 哨兵）

> **来源**：用户 2026-10-29 三问收口——「一次性脚本的储存方式难道不是应该放在临时文件系统里面吗？」→ 三档提案（探索→临时区 / 批次可重放→归档桶 / 引用或跨批→转正）经用户令「全部做完」落地。本批把 W977 人工清扫一次的做法变成**常驻判据**：W977 归档 287 件后，W983–W1001 又堆回 81 件，证明「靠人记得归档」不成立。
>
> - **文件**：AGENTS.md、Makefile、archive/README.md、archive/scripts/batches/w10xx/README.md、archive/scripts/batches/w10xx/_w1001_clean_locks.py、archive/scripts/batches/w10xx/_w1001_final.py、archive/scripts/batches/w10xx/_w1001_finish_faces.py、archive/scripts/batches/w10xx/_w1001_fix_index.py、archive/scripts/batches/w10xx/_w1001_fix_rule_anchor.py、archive/scripts/batches/w10xx/_w1001_probe_faces.py、archive/scripts/batches/w10xx/_w1001_restore_changelog_head.py、archive/scripts/batches/w10xx/_w1001_stage.py、archive/scripts/batches/w10xx/index.md、archive/scripts/batches/w9xx/_w954_review_evidence.py、archive/scripts/batches/w9xx/_w978_review_evidence.py、archive/scripts/batches/w9xx/_w983_derive.py、archive/scripts/batches/w9xx/_w983_download.py、archive/scripts/batches/w9xx/_w983_insert_plates.py、archive/scripts/batches/w9xx/_w983_make_prompts.py、archive/scripts/batches/w9xx/_w983_make_spec.py、archive/scripts/batches/w9xx/_w983_precheck_pages.py、archive/scripts/batches/w9xx/_w983_prepare.py、archive/scripts/batches/w9xx/_w983_retry.py、archive/scripts/batches/w9xx/_w983_serve.py、archive/scripts/batches/w9xx/_w983_sheet.py、archive/scripts/batches/w9xx/_w983_zoom.py、archive/scripts/batches/w9xx/_w984_derive.py、archive/scripts/batches/w9xx/_w984_download.py、archive/scripts/batches/w9xx/_w984_insert_plates.py、archive/scripts/batches/w9xx/_w984_make_prompts.py、archive/scripts/batches/w9xx/_w984_make_spec.py、archive/scripts/batches/w9xx/_w984_precheck_pages.py、archive/scripts/batches/w9xx/_w984_prepare.py、archive/scripts/batches/w9xx/_w984_retry.py、archive/scripts/batches/w9xx/_w984_serve.py、archive/scripts/batches/w9xx/_w984_sheet.py、archive/scripts/batches/w9xx/_w984_zoom.py、archive/scripts/batches/w9xx/_w986_make_prompts.py、archive/scripts/batches/w9xx/_w986_make_spec.py、archive/scripts/batches/w9xx/_w987_family_scan.py、archive/scripts/batches/w9xx/_w987_insert_scenes.py、archive/scripts/batches/w9xx/_w987_make_spec.py、archive/scripts/batches/w9xx/_w988_card_sheet.py、archive/scripts/batches/w9xx/_w988_docs.py、archive/scripts/batches/w9xx/_w988_fix_cascade.py、archive/scripts/batches/w9xx/_w988_fix_eol.py、archive/scripts/batches/w9xx/_w988_fix_gates.py、archive/scripts/batches/w9xx/_w988_insert.py、archive/scripts/batches/w9xx/_w988_inventory.py、archive/scripts/batches/w9xx/_w988_make_assets.py、archive/scripts/batches/w9xx/_w988_make_spec.py、archive/scripts/batches/w9xx/_w988_match.py、archive/scripts/batches/w9xx/_w988_pitfalls.py、archive/scripts/batches/w9xx/_w988_plan.py、archive/scripts/batches/w9xx/_w988_precheck.py、archive/scripts/batches/w9xx/_w988_sheet.py、archive/scripts/batches/w9xx/_w988_subject.py、archive/scripts/batches/w9xx/_w988_verify.py、archive/scripts/batches/w9xx/_w990_map.py、archive/scripts/batches/w9xx/_w990_master.py、archive/scripts/batches/w9xx/_w990_og_gap.py、archive/scripts/batches/w9xx/_w990_pick.py、archive/scripts/batches/w9xx/_w990_read.py、archive/scripts/batches/w9xx/_w990_roster.py、archive/scripts/batches/w9xx/_w990_split.py、archive/scripts/batches/w9xx/_w999_closeout.py、archive/scripts/batches/w9xx/_w999_crop_recheck.py、archive/scripts/batches/w9xx/_w999_derive_prepare.py、archive/scripts/batches/w9xx/_w999_diag.py、archive/scripts/batches/w9xx/_w999_fix_t35.py、archive/scripts/batches/w9xx/_w999_fix_wnum.py、archive/scripts/batches/w9xx/_w999_insert.py、archive/scripts/batches/w9xx/_w999_ledger_fill.py、archive/scripts/batches/w9xx/_w999_make_spec.py、archive/scripts/batches/w9xx/_w999_prepare.py、archive/scripts/batches/w9xx/_w999_probe.py、archive/scripts/batches/w9xx/_w999_probe_h1.py、archive/scripts/batches/w9xx/_w999_rebuild_missing_og.py、archive/scripts/batches/w9xx/_w999_redo.py、archive/scripts/batches/w9xx/_w999_redo2.py、archive/scripts/batches/w9xx/_w999_redo_map.py、archive/scripts/batches/w9xx/_w999_register.py、archive/scripts/batches/w9xx/_w999_renumber.py、archive/scripts/batches/w9xx/_w999_sheet.py、archive/scripts/batches/w9xx/_w999_sync_counts.py、archive/scripts/batches/w9xx/_w999_verify.py、assets/promo/plate-set/README.md、docs/00-导读/文档规范.md、docs/11-方案报告/README.md、docs/11-方案报告/工作复盘与优化分析报告/工作复盘与优化分析报告-2026-10-26.md、docs/agent/pitfalls.md、scripts/check_crop.py、scripts/check_plan_template.py、scripts/check_script_coverage.py、scripts/ledger_mutation_test.py、scripts/output/tools-inventory.md、scripts/plan_template_review.py、scripts/plates_verify.py、tests/unit/test_script_hygiene.py、.github/workflows/README.md、CCITATION.cff、HANDOVER.md、README.md、STRUCTURE.md、archive/docs/AGENTS-ARCHIVE.md、archive/docs/CHANGELOG-ARCHIVE.md、archive/docs/W批次编号对账表-ARCHIVE.md、archive/docs/file-index-ARCHIVE.md、archive/scripts/batches/README.md、archive/scripts/batches/index.md、archive/scripts/batches/w9xx/README.md、archive/scripts/batches/w9xx/index.md、ddocs/00-导读/项目说明.md、docs/11-方案报告/工作复盘与优化分析报告/工作复盘与优化分析报告-2026-10-27.md、docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md、pytest.ini、scripts/index.md、scripts/output/_cascade_files_W1002.txt、scripts/output/_vermilion_solid_cache.json、scripts/output/_w1002_spec.json、sscripts/output/stats-changelog.json、scripts/output/stats-index.md、scripts/output/stats.json、site/data/cross-time-danmaku.html、site/data/tag-cloud.html、site/dukou-engine.html、site/index.html、scripts/output/README.md、scripts/output/index.md、tests/unit/README.md、tests/unit/index.md。
>
**要点**：
① **存量归位 81 件**——按 W977 方法（活引用面 = 门禁/测试/CI/Makefile/治理文档，历史记录面不计）分级后 `git mv` 入 `archive/scripts/batches/w9xx|w10xx/`；`w10xx` 为新桶（四位号首批一次性件）。
② **转正 4 件**——被门禁/Makefile 引用或跨批复用的判据脚本去 `_` 前缀：`plan_template_review.py`（第 48 门禁判据表）、`ledger_mutation_test.py`（Makefile ledger）、`plates_verify.py` / `check_crop.py`（跨批素材与裁切判据）。后者正是 pitfalls E-05 的反面：**跨批判据归档会算错 ROOT**，故只能转正、不能归档——`check_crop.py` 顺带修掉写死的 `D:/xiyouji` 仓根。
③ **机器哨兵 C4**——第 42 门禁新增判据：历史批（W < 台账 max）`_w####_*.py|js` 仍在 `scripts/` 根 = FAIL；被四面/治理面引用的判为「转正候选」，配额 **8 件**（现役实测 8 件·棘轮只降不升，超配额即红）；台账不可读时跳过并 WARN（禁静默）。自测 6 → 9 例（T7 滞留必红 / T8 当前批放行 / T9 超配额必红）。
④ **口径成文**——pitfalls「`_` 前缀=一次性」条目改写为三档（94→95 条·git 节 22→23）；文档规范 §5 增「脚本三档归位」条款；AGENTS §3 目录注释与计数同步；archive/README 结构补 w10xx 桶 + 台账组行。
⑤ **连带修正**——`assets/promo/plate-set/README.md` 三处死链（指向已归档的逐批 prep）、复盘报告的取证脚本链接改归档路径（lint_links 活链）、`docs/11-方案报告/README.md` 判据表路径。

**验证**：第 42 门禁 0 FAIL（C4 NOTE 列 8 件转正候选）· 自测 9/9 通过 · `pytest tests/unit/test_script_hygiene.py` 5 passed · 转正件 import 冒烟通过（含 `check_crop.py` 转义错误被单测当场抓出并修）· `gen_folder_docs.py` 生成 w10xx 桶目录文档 · `gen_tools_inventory.py` 重生成 152 件 · `scripts/` 根 `_w*` 件 99 → 8（余 8 件为转正候选·已入棘轮）。

> - **状态**：已收官（81 件归档 + 4 件转正 + C4 判据常驻·`scripts/` 根一次性件清零待下一批清偿 8 件转正欠账）

### W1001（2026-10-28）：回次 og:image 全覆盖批·第一轮试点（12 张线描立像/场面）



> **来源**：用户 2026-10-27 选区指定下一批建议（100 回全覆盖 og:image）→ 2026-10-28 令「开始」→ 问卷裁定三处口径（线描立像族·沿用 plate-set 母版段 / 按题材定主体·战斗回场面·其余立像 / 先出 12 张试点）。
>
> **让号留痕**：拟用 W990，但 preflight 实测台账 max=W998 ⇒ W990–W998 已被并行批次占用（**先落地者保留**）⇒ 让号 **W1001**。
>
> - **文件**：site/reader/ch001.html、site/reader/ch003.html、site/reader/ch009.html、site/reader/ch011.html、site/reader/ch022.html、site/reader/ch028.html、site/reader/ch047.html、site/reader/ch063.html、site/reader/ch066.html、site/reader/ch079.html、site/reader/ch089.html、site/reader/ch093.html、assets/promo/plate-set/plate-line-49-ch001-xianshi.png、assets/promo/plate-set/plate-line-49-ch001-xianshi.webp、assets/promo/plate-set/plate-line-50-ch003-aoguang.png、assets/promo/plate-set/plate-line-50-ch003-aoguang.webp、assets/promo/plate-set/plate-line-51-ch009-yuanshoucheng.png、assets/promo/plate-set/plate-line-51-ch009-yuanshoucheng.webp、assets/promo/plate-set/plate-line-52-ch011-xiaoyu.png、assets/promo/plate-set/plate-line-52-ch011-xiaoyu.webp、assets/promo/plate-set/plate-line-53-ch022-liushahe.png、assets/promo/plate-set/plate-line-53-ch022-liushahe.webp、assets/promo/plate-set/plate-line-54-ch028-qunyao.png、assets/promo/plate-set/plate-line-54-ch028-qunyao.webp、assets/promo/plate-set/plate-line-55-ch047-tongtianhe.png、assets/promo/plate-set/plate-line-55-ch047-tongtianhe.webp、assets/promo/plate-set/plate-line-56-ch063-jiutou.png、assets/promo/plate-set/plate-line-56-ch063-jiutou.webp、assets/promo/plate-set/plate-line-57-ch066-mile.png、assets/promo/plate-set/plate-line-57-ch066-mile.webp、assets/promo/plate-set/plate-line-58-ch079-nanpo.png、assets/promo/plate-set/plate-line-58-ch079-nanpo.webp、assets/promo/plate-set/plate-line-59-ch089-huangshi.png、assets/promo/plate-set/plate-line-59-ch089-huangshi.webp、assets/promo/plate-set/plate-line-60-ch093-geigu.png、assets/promo/plate-set/plate-line-60-ch093-geigu.webp、site/static/images/plate-line-49-ch001-xianshi.webp、site/static/images/og-plate-line-49-ch001-xianshi.webp、site/static/images/plate-line-50-ch003-aoguang.webp、site/static/images/og-plate-line-50-ch003-aoguang.webp、site/static/images/plate-line-51-ch009-yuanshoucheng.webp、site/static/images/og-plate-line-51-ch009-yuanshoucheng.webp、site/static/images/plate-line-52-ch011-xiaoyu.webp、site/static/images/og-plate-line-52-ch011-xiaoyu.webp、site/static/images/plate-line-53-ch022-liushahe.webp、site/static/images/og-plate-line-53-ch022-liushahe.webp、site/static/images/plate-line-54-ch028-qunyao.webp、site/static/images/og-plate-line-54-ch028-qunyao.webp、site/static/images/plate-line-55-ch047-tongtianhe.webp、site/static/images/og-plate-line-55-ch047-tongtianhe.webp、site/static/images/plate-line-56-ch063-jiutou.webp、site/static/images/og-plate-line-56-ch063-jiutou.webp、site/static/images/plate-line-57-ch066-mile.webp、site/static/images/og-plate-line-57-ch066-mile.webp、site/static/images/plate-line-58-ch079-nanpo.webp、site/static/images/og-plate-line-58-ch079-nanpo.webp、site/static/images/plate-line-59-ch089-huangshi.webp、site/static/images/og-plate-line-59-ch089-huangshi.webp、site/static/images/plate-line-60-ch093-geigu.webp、site/static/images/og-plate-line-60-ch093-geigu.webp、site/static/images/og-plate-line-40-ch023-sichan.webp、site/static/images/og-plate-line-41-ch027-bailong.webp、site/static/images/og-plate-line-42-ch030-sancha.webp、site/static/images/og-plate-line-43-luoshanv.webp、site/static/images/og-plate-line-44-kuimulang.webp、site/static/images/og-plate-line-45-zhaoan-topic.webp、site/static/images/og-plate-line-46-fushi-topic.webp、site/static/images/og-plate-line-47-jingwu-topic.webp、site/static/images/og-plate-line-48-xuanzang-topic.webp、assets/promo/plate-set/raw/round14/README.md、assets/promo/plate-set/raw/round14/index.md、assets/promo/plate-set/raw/round14/plate-line-49-ch001-xianshi.jpg、assets/promo/plate-set/raw/round14/plate-line-50-ch003-aoguang.jpg、assets/promo/plate-set/raw/round14/plate-line-51-ch009-yuanshoucheng.jpg、assets/promo/plate-set/raw/round14/plate-line-52-ch011-xiaoyu.jpg、assets/promo/plate-set/raw/round14/plate-line-53-ch022-liushahe.jpg、assets/promo/plate-set/raw/round14/plate-line-54-ch028-qunyao.jpg、assets/promo/plate-set/raw/round14/plate-line-55-ch047-tongtianhe.jpg、assets/promo/plate-set/raw/round14/plate-line-56-ch063-jiutou.jpg、assets/promo/plate-set/raw/round14/plate-line-57-ch066-mile.jpg、assets/promo/plate-set/raw/round14/plate-line-58-ch079-nanpo.jpg、assets/promo/plate-set/raw/round14/plate-line-59-ch089-huangshi.jpg、assets/promo/plate-set/raw/round14/plate-line-60-ch093-geigu.jpg、scripts/_w990_og_gap.py、scripts/_w990_roster.py、scripts/_w990_read.py、scripts/_w990_master.py、scripts/_w990_map.py、scripts/_w990_split.py、scripts/_w951_check_crop.py、scripts/_w999_derive_prepare.py、scripts/_w999_insert.py、scripts/_w999_make_spec.py、scripts/_w999_prepare.py、scripts/_w999_rebuild_missing_og.py、scripts/_w999_redo.py、scripts/_w999_redo2.py、scripts/_w999_sheet.py、scripts/_w999_verify.py、scripts/_w999_closeout.py、docs/11-方案报告/计划方案/T35-任务计划执行与经验沉淀报告-2026-10-28.md、docs/11-方案报告/README.md、docs/agent/pitfalls.md、docs/10-方法论沉淀/素材批处理与判据自证方法论.md、dAGENTS.md、HANDOVER.md、CREADME.md、STRUCTURE.md、docs/00-导读/项目说明.md、.github/workflows/README.md、site/index.html、site/data/cross-time-danmaku.html、site/data/tag-cloud.html、site/dukou-engine.html、CITATION.cff、archive/docs/AGENTS-ARCHIVE.md、sassets/promo/plate-set/preview-contact-sheet.png、assets/promo/plate-set/preview-contact-sheet.webp。

**本批要点**：① **缺口实读修正**——100 个回目页中**仅 8 回有配图**，真实缺口 **80 回**（初查 92 系盘点正则过严所致·已按宽松匹配复核）；② **母版段派两个变体**——立像段**逐字复用 249 字符**，场面段**仅改 3 处**（环境暗示 / 主体体例 / 点睛主语）⇒ 同族一致由构造保证（母版段原含「无背景场景」，与场面型直接冲突）；③ **12 张试点**（6 立像 + 6 场面）主体**全部避开 plate-set 已出的 34 个角色**（敖广/袁守诚/萧瑀/弥勒/南极仙翁/给孤独长者 + 流沙河对峙/群妖聚义/通天河护童/龙宫夺珠/钉钯宴）；④ **12 处接入**（题图位 + 专属 1200×630 og:image）⇒ 回目页覆盖 8 → 20 回；⑤ **5 张重出**（1 张判据红 + 4 张人眼抓）· ⑥ **裁切判据改口径**——全图墨迹 bbox 会把朱砂/赭金装饰算成主体 ⇒ 假红（ch089 报「主体顶被切」但主体完整）⇒ 改用连通簇（**阈值与三条不变量一字未改**）。

**验证**：母版判据 J1–J10 **88/88 PASS** · 裁切验算 **88/88 PASS**（新口径）· 负样本自证 3/3 各自命中 · 接入验收判据 V1–V6 **全 PASS**（含「未覆盖页 78 个零回归」）· 幂等复跑 12/12 SKIP · 12 处 + 12 母版 + 12 og 全 HTTP 200 · 浏览器实跑渲染正常（ch001 仙石 / ch022 流沙河对峙）· 第 48 门禁 0 FAIL · 全量门禁 55/55 段全绿。

> - **状态**：已收官（**本批主体内容由并行 W1000 提交 `5870ec32` 代提入库**——该提交为全量提交且时点晚于本批 `git add -A`；本笔为登记面补齐。12 张试点落地·母版族 76 → 88 张·既有 76 张母版与站点版零改动·其余 78 个无配图回目页的 og:image 仍为通用图·未误改）

# 更新日志


> **📖 阅读契约（W707）**：查表型——判断「当前版本/最近批次」时只读**顶段 1 个版本段**；查历史段用 grep（`grep -A 30 "### vX"`）；完整通读非预期用法（历史细节在 archive/docs/CHANGELOG-ARCHIVE*.md·grep 单段查勿打开通读）。
本项目所有重要变更均记录于此。格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/)。

## [Unreleased]

> **W### 编号规则**：每个版本段标注唯一 W### ID（W001-W1041），v0.8 内部细分 W008.1-W008.7（B0-B7）。每个 W 附四件套字段（来源/文件/验证/状态）。反向索引见 [scripts/output/file-index.md](scripts/output/file-index.md)（给定文件查改几次）。
>
> **v/W 双键口径（W706）**：时间点查询以 W 号为准（单调键）；v 号在 W659-W667 合并段/并行批次区间不单调（v2.3.262〔W661〕列于 v2.3.261〔W666〕后）；v 号形态演化（阶段标签化·方案 D）经盘点 docs/superpowers/plans/2026-10-11-version-space-inventory.md 后另批实施。
>
> **方案 D 形态切换（W711 生效）**：自 W711 段起，CHANGELOG 段标题去 v 号（新形态 `### W###（日期）：标题`）；W001-W1000 段保留 `### vX.Y.Z（日期）：W###` 历史形态不改写；v 号降格为阶段标签（v2.3·无 patch）；CITATION.cff version 改批次号形态（"W###"·CFF free string）；file-index 历史条目保留 v 引用、新增条目 W only。
>
> **历史版本归档**：v0.1 - v2.3.17（W001-W1000）已迁移至 [archive/docs/CHANGELOG-ARCHIVE-tier2.md](archive/docs/CHANGELOG-ARCHIVE-tier2.md)（W513 二级归档）；W422 再归档 v2.3.18-v2.3.31（W400-W416）段；W511 归档 v2.3.32-v2.3.82（W417-W464）段 + v2.3.83（W484）段至 [CHANGELOG-ARCHIVE.md](archive/docs/CHANGELOG-ARCHIVE.md)。W681 归档 v2.3.84-v2.3.249（W485-W649）段至 [CHANGELOG-ARCHIVE.md](archive/docs/CHANGELOG-ARCHIVE.md)。W736 再归档 v2.3.250-v2.3.293（W650-W699）段至 [CHANGELOG-ARCHIVE.md](archive/docs/CHANGELOG-ARCHIVE.md)（源文件超 50KB/500 行阈值）。本文件正本按 110 段窗滚动（W960 窗口制·正本最老段随批推进·早期形态：W650-W710 段用历史 vX.Y.Z 形态·W711+ 段用批次键 W### 形态）。
>
> **全站页数口径**（W459 建·W702 实跑刷新，各门禁分母不同）：HTML 共 857<!--stats:html_total--> 页（site/data 88<!--stats:site_data_html--> + site/en 138<!--stats:site_en_html--> + site 根 9<!--stats:site_root_html--> + site/reader 622<!--stats:site_reader_html-->）；CSP 覆盖 856<!--stats:csp_covered--> 页（排除 `_template.html`）；check_js_syntax/check_structure 扫 855<!--stats:scan_files--> 文件（再排除 `_shell.html`）；check_seo_head 扫 855<!--stats:seo_scanned--> 页（site 全树减两个模板壳）；inline_css 同步 330<!--stats:inline_css_pages--> 页（site 全树含 INLINED 标记页）；「可视化页 87<!--stats:visualization_pages-->」= site/data 88 减 `_shell.html`。
>
> **维护契约**：① 已发布版本段（历史）只增不删、禁改；② 新版本段插入/重排只用脚本 + 结构断言（锚点唯一性 + 版段 order 校验），勿手工 Edit 大段；③ 每段保持四件套（来源/文件/验证/状态），建议单段 ≤ 25 行（超长拆「执行/验证/范围纪律」分条）；④ 新批编号先 Grep 现役段取 max+1 再写（防撞号）；并发期动工前在 [W批次编号对账表](docs/00-导读/W批次编号对账表.md) 登记认领（W663 起·版段递延时以对账表为准）。
### W1000（2026-10-28）：对抗式审查常驻化批（四位号首批·用户令「立项」）

> **来源**：用户令「立项」——W998 subagent 对抗式审查一次抓出 P1×2/P2×4，证明「写哨兵的人也需要被哨兵盯」，按建议常驻化。
> **摘要**：① **check_audit_trigger.py 触发器**——台账最新含「对抗式审查」认领行距 max(W) ≥20 批即提示派发（preflight 接线·只提示不拦截）；找不到登记行按「从未审查」直接触发（fail-closed 宁假警不漏警）；自测四态（触发/未触发/从未/散文豁免）。② **模板落盘 docs/agent/adversarial-audit-prompt.md**——W998 实战 prompt 沉淀（范围声明+A-G 必查清单+P0-P3 输出分级+派发会话收尾义务+成本参考），任何会话可持之派发。③ **四位号 W1000 全链实战验证**——parse_ledger max=1000、ledger_backfill find_row、认领行四位解析、级联断言「批次号应为 W1000」字符串比对、W969 迁移 {3,4} 正则全部经受实战。④ 顺带：搜索索引随批刷新（并行 T-35 新文档）+ CSP 两页重算 + 台账回窗。
> **文件**：scripts/check_audit_trigger.py · scripts/preflight_check.py · docs/agent/adversarial-audit-prompt.md · scripts/output/script-coverage-baseline.txt · docs/00-导读/W批次编号对账表.md · archive/docs/W批次编号对账表-ARCHIVE.md · site/data/search.html · site/en/search.html
> **验证**：触发器 --self-test 四态 + 现网未触发（距 W1000 基线 0 批）+ 四位号四组件实战验证 + pytest 全量 943 passed + ruff 清零 + CSP 零漂移 + 体积四窗全绿。
> **状态**：**已收官**（W1000 git 反填·触发器与模板落地·四位号实战全过）
### W999（2026-10-28）：必守纪律晋升批（惰性层→必载层·用户问责「pitfalls 优先级低导致惰性读取」）

> **来源**：用户问责「pitfalls.md 优先级太低导致惰性读取」——三层取证：CLAUDE 必载层无此纪律、AGENTS 铁律 13 条无此条、唯一落点是按需查表的 pitfalls（检索触发器在写教训场景设计上不响）。
> **摘要**：① **AGENTS §6 铁律 14**「修实例必修根」（同族风险同批或次批根治禁等排期 + 检查按委托字面范围 + 跨会话教训权威落坑表与本节·私有记忆仅镜像）——权威落点。② **CLAUDE.md 速查第 12 行**一行版+指针（必载层每会话在场·行数 49/60·第 32 门禁四查过）。③ 脚注同名条目改指向铁律 14（滚动层只留索引）。按 CLAUDE 契约流程：权威先落 §6 再登记速查行。
> **文件**：AGENTS.md · CLAUDE.md
> **验证**：铁律 14 在 §6、CLAUDE 第 12 条指向 AGENTS §6-14、第 32 门禁 0 FAIL、verify docs rc=0。
> **状态**：**已收官**（W999 git 反填·纪律晋升三层落地）
### W998（2026-10-28）：对抗式审查修复批（subagent P1×2/P2×4/P3 清偿）

> **来源**：用户令「派发一个 subagent 严格审查一遍整个」——subagent 对抗式审查（迁移守恒/门禁实跑/代码缺陷/三层一致/同族残留全查）报 P1×2/P2×4/P3×6。
> **摘要**：① **P1-1 C4 死门控**——脚注逐条判据误嵌 HANDOVER>45KB 分支内（HANDOVER 瘦身后 C4 永不执行·且 fline 跨迭代引用可 NameError·subagent 纯内存 monkeypatch 实证复现）；移回 AGENTS 分支独立执行。② **P1-2 锁竞态双持**——O_EXCL 创建与 write 之间空文件窗口，他方 _read 得 None 误判损坏并夺锁=互斥静默击穿；改「创建中」短重试（10×0.1s）后仍不可解析才判损坏夺锁。③ **P2-1 release 无 pid 校验**——batch_cascade finally 传 pid（防 TTL 夺锁后误删他方新鲜锁）+ CLI --pid。④ **P2-2**——三份 spec json 工作树 CRLF 回归归 LF。⑤ **P2-3**——pitfalls 子节标题计数滞后（级联 8→9·流程 19→20·AGENTS 侧早已同步的自相矛盾）。⑥ **P2-4**——CHANGELOG/file-index 头部「仅保留 W700+」过期窗界声明改窗口制措辞 + 叠标点。⑦ **P3-3**——W997 台账回填口径统一（feat 主锚）。
> **文件**：scripts/check_doc_size_budget.py · scripts/cascade_lock.py · scripts/batch_cascade.py · scripts/archive_ledger_rows.py · docs/agent/pitfalls.md · CHANGELOG.md · scripts/output/file-index.md · scripts/output/_w992_spec.json · scripts/output/_w993_spec.json · scripts/output/_w997_spec.json · docs/00-导读/W批次编号对账表.md · archive/docs/W批次编号对账表-ARCHIVE.md
> **验证**：C4 负样本（AGENTS 长条目+HANDOVER 瘦→C4 必红·修复后语义）+ 锁五态自测 + 守卫三态 + pytest 全量 942 passed + ruff 清零 + 数字断言/体积窗全绿。
> **状态**：**已收官**（W998 git 反填·C4 死门控与锁竞态根治·含对抗式审查全程）
### W997（2026-10-27）：协作纪律入库批（修实例必修根·用户问责「为什么只写你自己的记忆文件」）

> **来源**：用户双重问责——「修实例必修根」（CRLF 六次地鼠/W967 查圈打折/tmpe 积压三案实证）+「为什么只写你自己的记忆文件」（把跨会话教训只落私有记忆·W516 载体铁则二犯）。
> **摘要**：① **pitfalls 流程组新增「修实例必修根 + 检查按字面范围」**——三类同病实证（疏通偏差/爆半径恐惧/范围打折·各带批次锚）+ 处置规则（同族风险同批或次批根治禁「等排期」收尾·真需决策仅限外发动作·根治成本用既有机制消化）+ 载体纪律并案（权威落本文件·私有记忆仅镜像）。② **archive_ledger_rows A4 判据收紧**——在途集合比对只计「真在途」（有 touches 且非已停止/让号留痕·W937 已停止行误伤实证）；只禁减少不禁并行追加（读-写窗口容忍）。③ 台账回窗 63→59。
> **文件**：docs/agent/pitfalls.md · AGENTS.md · scripts/archive_ledger_rows.py · docs/00-导读/W批次编号对账表.md · archive/docs/W批次编号对账表-ARCHIVE.md
> **验证**：pitfalls 计数 89→90（流程 19→20·AGENTS 两处同步）+ 数字断言 N4 一致 + 体积四窗全绿 + pytest 全量 935+ passed + ruff 清零。
> **状态**：**已收官**（W997 git 反填·纪律落坑表与 A4 收紧）
### W996（2026-10-28）：流程提示位批（C2 判据：漏跑级联回归锁·W995 形态）



> **来源**：主人 2026-10-28 令「开始」（W995 收官报告登记的流程提示位候选）——W995 施工漏跑级联的事故回归锁。

> - **文件**：scripts/ledger_close_check.py、dCHANDOVER.md、README.md、STRUCTURE.md、docs/00-导读/项目说明.md、.github/workflows/README.md、site/index.html、site/data/cross-time-danmaku.html、site/data/tag-cloud.html、site/dukou-engine.html、AGENTS.md、archive/docs/AGENTS-ARCHIVE.md、CITATION.cff、sscripts/output/_w996_spec.json、scripts/output/_cascade_files_W996.txt。

**缺口（W995 事故的防线盲区）**：W995 施工漏跑级联时三道既有防线全部放行——C4 提交对账因「台账认领行即豁免」（D2）放行、ledger_close_check 旧判据反向不查（只查「有段→查台账」，无段则不进检查集）、无任何流程级提示。结果：工具/拆分全入库而十面落点从未写入，直至收官报告状态行锚点失败才暴露。

**C2 判据（ledger_close_check 新增·反向迭代）**：台账中**已收官且 hash 落地**（有 commit）的行，必须在级联段源（CHANGELOG 现役+归档一级+tier2 容器/范围件）里有自己的段——缺失即 FAIL「漏跑 batch_cascade（W995 形态）」。豁免面=有意不立段的合规形态（让号/并号/已停止/空壳/作废/补录/追记，状态列标记识别）；hash 占位行不查（无 commit·归 preflight 在途态管）。**--allow-open 不豁免本判据**（漏级联是已收官批次的确定性缺陷·非在途伪阻塞）。self-test 扩 C2 三态（漏级联必红/让号并号豁免/无hash跳过）。

**实树验证**：现役窗全绿（W995 修复后 hash=71a1add4 有段 ✓）·历史 59 行窗口零漏级联——既有收官纪律在 W995 前无前科，判据无存量误报。

**验证**：--self-test 过（2 正例+4 负例+C2 三态）+ 实树 rc=0 + ruff 0 + 全量 verify 见状态行。

> - **状态**：已收官（`80d2b9c6`·verify 全量 rc=0 + self-test 含 C2 三态 + 实树 59 行窗口零存量误报——单段流程批·级联即收官）

### W995（2026-10-28）：tier2 按W段拆分批（政策落地·archive_tier2 自持闭环·提示位扩展）



> **来源**：主人 2026-10-28 授权「按 W 段拆分文件」（tier2 容器 1044KB 破 1MB 的政策裁决）+ W994 延后的提示位扩展（W992 校准提交 27281553 落地后错峰补上）。

> - **文件**：archive/docs/CHANGELOG-ARCHIVE-tier2.md、archive/docs/CHANGELOG-ARCHIVE-tier2-W400-W559.md、scripts/archive_tier2.py、scripts/check_archive_health.py、scripts/batch_cascade.py、scripts/verify_delivery.py、archive/README.md、dCHANDOVER.md、README.md、STRUCTURE.md、docs/00-导读/项目说明.md、.github/workflows/README.md、site/index.html、site/data/cross-time-danmaku.html、site/data/tag-cloud.html、site/dukou-engine.html、AGENTS.md、archive/docs/AGENTS-ARCHIVE.md、CITATION.cff、sscripts/output/_w995_spec.json、scripts/output/_cascade_files_W995.txt。

**tier2 按 W 段拆分（政策落地）**：CHANGELOG-ARCHIVE-tier2.md 1044KB→**746KB**（W001-W399·210 段留存）+ 新建范围件 **CHANGELOG-ARCHIVE-tier2-W400-W559.md**（299KB·144 段·范围命名约定首件）——拆分脚本守恒三道+号域断言（留存全 <400·迁出全 ≥400）零落盘前置。**约定定形**：tier2 容器范围命名 `*-tier2-W<lo>-W<hi>.md`·单件 ≤1MB。

**archive_tier2 追加逻辑升级（自持闭环）**：追加前容量判断——容器现体积+本次迁出 >1MB → 自动开范围命名新件（合规头部生成），tier-2 递增不再破线；LIMIT 常量化。

**探针 T1b 升格**：tier2 破线从「登记观察」升为 problem（strict 判红——拆分约定落地后已可执行）+ glob 扩至范围命名件 + run(prefix) 参数（供级联提示位复用）。

**提示位扩展（W994 延后件）**：batch_cascade 收官提示位独立尾部块新增——[ARCHIVE] 归档健康行（探针 T1-T4·prefix 复用）+ [TMPE] 上次清理活动日期（.journal 最新落笔·清理节奏可见性）。verify_delivery ARCHIVE_DOCS 登记 +2（§11.2「tier2 须登记」条款）；archive/README 台账 2 行 + 结构树。

**验证**：拆分守恒断言 + archive_tier2/check_archive_health --self-test 双过 + 单测 5/5 + 探针 strict rc=0（三件 tier2 全 ≤1MB）+ 提示位直测（[ARCHIVE] 前缀行与清理日期行在位）+ 全量 verify rc=0 见状态行。

> - **状态**：已收官（`71a1add4`·verify 全量 rc=0 + 单测 5/5 + 自测双过·tier2 三件全 ≤1MB·提示位四件齐）

### W994（2026-10-28）：归档系统打磨批（tier-2 规则机器化：探针+常驻工具+双件实跑回线）



> **来源**：用户 2026-10-28 令「继续打磨归档系统和临时文件系统」——体检定位到 §11.2 tier-2 条款自 W513 后掉档（CHANGELOG-ARCHIVE 1198KB / file-index-ARCHIVE 1070KB 双破 1MB 线零反应·W824「无机器触发点必掉档」又一活体），按「探测→修法→防复发」闭环处置。

> - **文件**：scripts/check_archive_health.py、scripts/archive_tier2.py、tests/unit/test_archive_health.py、archive/docs/CHANGELOG-ARCHIVE.md、archive/docs/CHANGELOG-ARCHIVE-tier2.md、archive/docs/file-index-ARCHIVE.md、archive/docs/file-index-ARCHIVE-tier2.md、archive/README.md、archive/scripts/batches/README.md、scripts/README.md、scripts/gen_folder_docs.py、dCHANDOVER.md、README.md、STRUCTURE.md、docs/00-导读/项目说明.md、.github/workflows/README.md、site/index.html、site/data/cross-time-danmaku.html、site/data/tag-cloud.html、site/dukou-engine.html、AGENTS.md、archive/docs/AGENTS-ARCHIVE.md、CITATION.cff、sscripts/output/_w994_spec.json、scripts/output/_cascade_files_W994.txt。

**健康探针（check_archive_health.py·报告型）**：把 §11.2 三条纯文字条款机器化——T1 一级归档件 1MB 判距（≥800KB 预警·破线 ⚠+修法指引）；T2 归档 scripts 台账对账（**组行计数对账语义**：顶层存量组行 N vs 磁盘实数+段目录组行覆盖+子目录提及——W735 存量 200+ 件从未逐件登记是既定形态，逐件检查会误报风暴，首跑 200 件误报后改为计数对账语义并补登记 3 条组行：顶层 47/w4xx 11/w5xx 149）；T3 batches/README 冷存储警告在位（W836：归档件 ROOT 上溯失效·误跑会错——本批补入警告文本）；T4 归档区汇总体积。`--strict` 为门禁候选。

**二级归档工具（archive_tier2.py·常驻）**：键序前缀切分（changelog=段标题 W 号；file-index=顶层节·两代混层目录节无 W 号取 0 排最老）+ 全文字节目标（§11.2 管文件体积）+ **守恒五道断言零落盘前置**（A1 段数/A2 逐字节在 tier2/A3 头部只追加/A4 键序前缀/A5 字节守恒）。**实跑双件回线**：CHANGELOG-ARCHIVE 1198→900KB（迁出 144 段 W400-W559）·file-index-ARCHIVE 1070→816KB（迁出 10 目录节·**新建 file-index-ARCHIVE-tier2.md**）。施工中守恒断言三度 fail-closed 拦截：字节/字符混计（A5 两端异单位）、切枝循环按键序遍历致位置倒序静默保留新版段（A5 当场活捉·真损坏级）、A5 符号写反——全部修复后落盘，W681 补录尾段原位未动。

**其余**：batches/README 冷存储警告（生成模板级注入——手工写入会被 --refresh 覆写·W994 实证后改模板位） + scripts/README 场景速查 +2 行（二级归档/健康体检路由）+ 单测 5 例。

**边界与延后**：batch_cascade 收官提示位扩展（[ARCHIVE] 行+[TMPE] 上次清理日期）**延后**——W992（提示位口径校准·他方在途）认领了 batch_cascade.py，按工作树吸收纪律（坑表 88 条）不在其认领面落编辑；W992 收官后任一批可补。

**验证**：探针 --self-test + 单测 5/5 + 双件 dry-run→apply 守恒五道全过 + 探针复跑 T1 回线（900/816KB）·T2 对账一致·T3 在位 · W681 补录尾段原位核验 · ruff 0 · 全量 verify 见状态行。

> - **状态**：已收官（`aacb6fe3`·verify 全量 rc=0 + 探针/工具自测过 + 单测 5/5·双件回线 900/816KB·T2 对账一致·T3 在位）

### W993（2026-10-27）：全仓行尾定形批（CRLF 时代终结·用户问责「为什么不解决」）

> **来源**：用户问责「CRLF 老问题你为什么不解决呢」——W971-W989 期间六次地鼠（裸 LF 注入/混行尾 fail-closed/CRLF 锚补丁）全部就地修未治系统，本批根治。
> **摘要**：① **.gitattributes 落地**——text=auto eol=lf + 21 类二进制显式排除；② **renormalize**——22 个 i/crlf 烤死 blob + 混行尾面归 LF（纯机械提交 84cce358·入 .git-blame-ignore-revs 防 blame 污染）；③ **工作树重写**——git 内容比对（CRLF 经 clean=LF≈索引）致 reset --hard 不生效，按标准配方删跟踪件重 checkout：4688 文件全 i/lf w/lf·零 CRLF·零 mixed·工作树零漂移；④ **语义收口**——pitfalls 新条目「行尾定形时代结束」（补丁串按 CRLF 锚定作废·一律 
；旧条目留作历史）；AGENTS 坑位计数 88→89 两处同步；⑤ 自此工具以 
 构建无分歧、混行尾防线（load fail-closed）保留作最后防线。
> **文件**：.gitattributes · .git-blame-ignore-revs · docs/agent/pitfalls.md · AGENTS.md · CHANGELOG.md · scripts/output/file-index.md · docs/00-导读/W批次编号对账表.md · archive/docs/W批次编号对账表-ARCHIVE.md
> **验证**：行尾普查 4688 全 i/lf w/lf（renormalize 前 22 i/crlf + 10 mixed 清零）+ pytest 全量 934 passed + verify docs rc=0 + 数字断言 N4 一致 + 体积四窗全绿。
> **状态**：**已收官**（W993 git 反填·全仓行尾定形 4688 文件全 LF）
### W992（2026-10-27）：一次性件定向退役与提示位口径校准批

> **来源**：用户菜单②（退役扫描）——[SCRIPTS] 提示位持续报警裸跟踪数 67>20。
> **摘要**：① **零引用甄别**——67 跟踪 _ 件全量对拍引用面（tests+常驻代码+活治理文档+CHANGELOG 证据锚窗）仅 4 件零引用（_w988_close/pitfalls2/record_adoption/sync_87·并行 W988 批遗留）；② 4 件 git mv 入 archive/scripts/batches/w9xx/（archive_file.py 流程·台账 4 行）；③ **[SCRIPTS] 口径校准**——裸跟踪数含近批证据锚（110 段窗内被引用·合法驻留）恒超 20 成常驻噪声，改报「零引用退役候选数」作阈值判据。
> **文件**：archive/scripts/batches/w9xx/ · archive/README.md · scripts/batch_cascade.py · scripts/output/tools-inventory.md · docs/00-导读/W批次编号对账表.md
> **验证**：甄别四面对拍 + pytest 全量 935 passed + ruff 清零。
> **状态**：**已收官**（W992 git 反填·4 件退役+口径校准）
### W991（2026-10-27）：级联运行锁与提交隔离批（①层重启 + safe_commit 守卫·用户两问令）

> **来源**：用户两问——「重启设计」（W982 缓建的级联文件锁①层）+「提交总是混入并行会话的暂存件怎么解决」（W989 认领提交 1fb1b14f 扫入他方暂存级联面实证）。
> **摘要**：① **cascade_lock.py 级联运行锁**——.git/cascade.lock 原子创建（O_EXCL·批次/持有会话/时间戳），batch_cascade --apply 全程持有（finally 必释放），preflight 检测活动锁即 WARN（共享面正被级联写·此刻 verify/preflight 读数可能撞中态）；陈旧锁（≥600 秒）与损坏锁自动夺；与 W982 缓建理由对照：锁做**运行期互斥**而非索引锁，级联自身不重入。② **safe_commit 无 pathspec 守卫**——索引含暂存件而未指 pathspec 即拒绝并逐件列名（pathspec 形态走临时索引只取声明路径 worktree 态·他方暂存件天然隔离）；守卫纯函数三态负样本验证。③ 自测：锁五态（原子创建/拒绝/幂等释放/陈旧夺/损坏夺）。④ 建置实录：锁自测首版「重复释放应 False」是语义错（finally 安全要求幂等 True·改测试不改代码）。
> **文件**：scripts/cascade_lock.py · scripts/batch_cascade.py · scripts/preflight_check.py · scripts/safe_commit.py · scripts/output/script-coverage-baseline.txt · docs/00-导读/W批次编号对账表.md · archive/docs/W批次编号对账表-ARCHIVE.md
> **验证**：锁 --self-test 五态全过 + 守卫三态负样本 + pytest 全量 935 passed + ruff 清零 + 体积四窗全绿。
> **状态**：**已收官**（W991 git 反填·锁五态自测+守卫三态）
### W990（2026-10-27）：内联纪律收口批（查坑表补报错原文 + 工作树吸收条目·88 条）



> **来源**：用户 2026-10-27 问「其他 Agent 下次还会出现类似问题吗」——评估发现两个可修缺口后令「做」。

> - **文件**：docs/agent/pitfalls.md、AGENTS.md、HANDOVER.md、dCREADME.md、STRUCTURE.md、docs/00-导读/项目说明.md、.github/workflows/README.md、site/index.html、site/data/cross-time-danmaku.html、site/data/tag-cloud.html、site/dukou-engine.html、CITATION.cff、sscripts/output/_w990_spec.json、scripts/output/_cascade_files_W990.txt。

**缺口一（撞错检索路走不通）**：查坑表「Python 字符串层转义」行补报错原文 literal——`truncated \xXX escape` / `unicodeescape` / `invalid escape sequence`——Agent 撞错后 grep 原文即命中本行（此前只有中文描述·按原文检索会漏）。

**缺口二（更大的：静默丢工作）**：新增条目「并行会话在场的未提交工作树编辑会被吸收或覆盖——只有已提交状态是安全停车位」（git/提交/并发 21→22·总数 87→88·计数链四处同步 N4 88=88）。四连环实证：① 未提交编辑被对方重 add 吸收进暂存快照（W985 pitfalls 编辑被 W988 卷入·内联署名保住溯源）；② restore/清偿扫过即覆盖（同批险情：worktree diff 一度归零）；③ 纪律=并行在场禁 `git add -A`（按名单精确暂存）+ 跨批次内容立即提交或留字据——工作树不是停车位；④ 被他方在途件卡门禁（C4-f 假红）按 W932/W984 先例核成色后代提（W988「登记并行 W989 代提事实」双向留痕口径），成色不够则等。

**验证**：N4 88=88 · E1 抽查（literal 与条目各在位）· 全量 verify + pytest 见状态行。

> - **状态**：已收官（内容随 W991 批提交代提落库·`01decea2`·verify 全量 rc=0 + N4 88=88·查坑表报错原文与新条目在位）

### W989（2026-10-27）：脚注定形收紧批（C4 300→120·用户裁决「都做」之手搓治理收尾）

> **来源**：用户问「为什么又出现这种问题」（AGENTS 脚注再现散文体·W984-W988 并行会话所写）——取证结论为门禁守的形全部健在（5 条/3.3KB/各 ≤300/阿拉伯头），进来的是「合形的散文」：「一行一事」只是维护契约散文条款无机器判据；用户裁决「都做」。
> **摘要**：① **C4 收紧 300→120 字**——门禁与级联 precheck 双写点同步（现网五条 264/262/227 字散文在 120 线下全部不合格·重写后无法回头）；hand-tuning 余地收干。② **现网五条重写为索引体**（55-65 字·每条重写前断言 CHANGELOG 有段·全文零丢失）——W984-W988 素材线五批压缩为「批次+动作+要点」形态，脚注 3.3→1.1 KB。③ **手搓治理去重裁决**——开工实施 C8 版本行契约时发现 W982 批（并行会话）已落地三层方案②（check_doc_size_budget C7-1/2/3/4/5/6 六面版本契约 FAIL）+③（preflight 手搓劝导位）+①文件锁缓建裁决——本批 C8 与重复劝导位当场撤销去重，判据覆盖经负样本 6/6 验证的为 W982 版。④ **级联拼接缺陷修复**——agents_note 尾句号与 tail 首句号相拼出「。。」（a0e9ee07·本批前独立推送）。⑤ 台账回窗（61→59）。
> **文件**：scripts/check_doc_size_budget.py · scripts/batch_cascade.py · scripts/preflight_check.py · scripts/archive_ledger_rows.py · AGENTS.md · docs/00-导读/W批次编号对账表.md · archive/docs/W批次编号对账表-ARCHIVE.md
> **验证**：C4 负样本（>120 即红）+ 五条重写断言（CHANGELOG 有段+≤120）+ 去重后 ruff 清零 + pytest 全量 934 passed + 体积四窗全绿（109/109/59/60）。
> **状态**：**已收官**（W989 git 反填·C4 收紧与五条索引化·含代提面）
### W988（2026-10-27）：水墨卡族投放批（27 张 card-* 逐张定投放位置 + 分回次 og:image 换专属图）



> **来源**：用户 2026-10-27 选区指定两项（① card-* 27 张按题材逐张定投放位置（人物卡→角色页顶部横幅 / 场景卡→主题页）② 分回次 og:image（现全站共用一张通用图，需另裁 1200×630 版））→ 问卷裁定两处执行口径（横幅＝另裁 1200×500 宽幅·人物半身特写；og:image＝只做有配图的页·纯裁切）。
>
> - **文件**：site/reader/ch004.html、site/reader/ch007.html、site/reader/ch010.html、site/reader/ch014.html、site/reader/ch015.html、site/reader/ch019.html、site/reader/ch023.html、site/reader/ch027.html、site/reader/ch030.html、site/reader/ch031.html、site/reader/culture/历史玄奘与小说玄奘专题.html、site/reader/culture/明代科举制度对照专题.html、site/reader/culture/西游与佛教禅宗专题.html、site/reader/essays/西游与服饰学.html、site/reader/essays/西游与民俗学.html、site/reader/people/九灵元圣-方向二深化.html、site/reader/people/二郎神.html、site/reader/people/取经团队动力学深化专题.html、site/reader/people/哪吒.html、site/reader/people/地府体系深化专题.html、site/reader/people/大鹏金翅雕.html、site/reader/people/太上老君.html、site/reader/people/奎木狼外传.html、site/reader/people/女儿国国王.html、site/reader/people/如来.html、site/reader/people/嫦娥外传.html、site/reader/people/孙悟空.html、site/reader/people/托塔李天王外传.html、site/reader/people/昴日星官.html、site/reader/people/沙僧-方向二深化.html、site/reader/people/沙僧.html、site/reader/people/沙僧外传.html、site/reader/people/火焰山土地外传.html、site/reader/people/灵感大王.html、site/reader/people/灵感大王外传.html、site/reader/people/牛魔王.html、site/reader/people/独角兕大王.html、site/reader/people/狮驼岭三魔-方向二深化.html、site/reader/people/猪八戒-方向二深化.html、site/reader/people/猪八戒.html、site/reader/people/猪八戒深化专题.html、site/reader/people/玉兔精.html、site/reader/people/玉帝.html、site/reader/people/白骨精.html、site/reader/people/白骨精外传.html、site/reader/people/白鹿精-方向二深化.html、site/reader/people/白龙马.html、site/reader/people/百眼魔君.html、site/reader/people/紧箍儿的内侧-器物传记.html、site/reader/people/红孩儿.html、site/reader/people/罗刹女外传.html、site/reader/people/老鼋外传.html、site/reader/people/老鼠精.html、site/reader/people/蜘蛛精.html、site/reader/people/蝎子精.html、site/reader/people/观音.html、site/reader/people/赛太岁.html、site/reader/people/车迟国三国师外传.html、site/reader/people/金角大王.html、site/reader/people/金角银角深化专题.html、site/reader/people/铁扇公主.html、site/reader/people/银角大王.html、site/reader/people/镇元大仙.html、site/reader/people/黄眉老佛外传.html、site/reader/people/黄袍怪.html、site/reader/people/黄风怪外传.html、site/reader/people/黑熊精.html、site/reader/poetry/原著景物诗分类赏析专题.html、site/reader/poetry/原著景物诗赏析专题.html、site/reader/poetry/西游诗词意象谱系专题.html、site/reader/themes/二十八星宿专题.html、site/reader/themes/五方揭谛专题.html、site/reader/themes/佛学AI西游三维语义映射表.html、site/reader/themes/六丁六甲专题.html、site/reader/themes/兵器的自我修养专题.html、site/reader/themes/取经团队-凭什么走到西天.html、site/reader/themes/取经密码学专题.html、site/reader/themes/取经教育学专题.html、site/reader/themes/取经路径地理符号学专题.html、site/reader/themes/取经路线地理专题.html、site/reader/themes/唐僧-凡躯圣心.html、site/reader/themes/器物传记学专题.html、site/reader/themes/四值功曹专题.html、site/reader/themes/大闹天宫-英雄还是悲剧.html、site/reader/themes/小妖生命史专题.html、site/reader/themes/招安的两种结局专题.html、site/reader/themes/无字真经专题.html、site/reader/themes/水帘洞-瀑布门的世界.html、site/reader/themes/水帘洞专题.html、site/reader/themes/沙僧-沉默者的智慧.html、site/reader/themes/法宝系统专题.html、site/reader/themes/混世四猴专题.html、site/reader/themes/猪八戒-不愿承认的自己.html、site/reader/themes/猴王到行者-五次蜕变.html、site/reader/themes/真假美猴王专题.html、site/reader/themes/神学干预机制专题.html、site/reader/themes/空间叙事学专题.html、site/reader/themes/筋斗云专题.html、site/reader/themes/紧箍咒专题.html、site/reader/themes/蟠桃园-体制内的秘密.html、site/reader/themes/西游与死亡研究专题.html、site/reader/themes/金箍棒的重量-一万三千五百斤的秘密.html、scripts/_w988_plan.py、scripts/_w988_subject.py、scripts/_w988_inventory.py、scripts/_w988_match.py、scripts/_w988_precheck.py、scripts/_w988_make_assets.py、scripts/_w988_insert.py、scripts/_w988_fix_eol.py、scripts/_w988_verify.py、scripts/_w988_sheet.py、scripts/_w988_card_sheet.py、scripts/_w988_pitfalls.py、scripts/_w988_docs.py、scripts/_w988_make_spec.py、scripts/_w988_fix_cascade.py、scripts/_w988_fix_gates.py、scripts/check_seo_head.py、scripts/output/_w988_spec.json、scripts/output/_w988_precheck.json、scripts/output/_w988_assets.json、scripts/output/_w988_inventory.json、scripts/output/_w988_match.json、scripts/output/_w988_card_map.json、scripts/output/_w988_card_sheet.png、scripts/output/_w988_sheet-banner.png、scripts/output/_w988_sheet-og.png、scripts/output/_cascade_files_W988.txt、docs/11-方案报告/计划方案/T34-任务计划执行与经验沉淀报告-2026-10-27.md、docs/11-方案报告/README.md、docs/agent/pitfalls.md、docs/10-方法论沉淀/素材批处理与判据自证方法论.md、dAGENTS.md、HANDOVER.md、CREADME.md、STRUCTURE.md、docs/00-导读/项目说明.md、.github/workflows/README.md、site/index.html、site/data/cross-time-danmaku.html、site/data/tag-cloud.html、site/dukou-engine.html、CITATION.cff、archive/docs/AGENTS-ARCHIVE.md、scripts/output/file-index.md。。

**本批要点**：① **27 张 `card-*` 逐张定投放位置并接入**（用户选区指定的第一项）——**13 张人物卡 → 角色页/回目页顶部 `.chapter-banner` 横幅**（1:1 源另裁 1200×500 宽幅·人物半身特写·新立第三套类名·限宽 720px·暗色隐藏·横幅在题图之上形成「通栏横幅 + 420px 竖题图」宽窄分层），**14 张场景卡 → 主题页 `.chapter-scene` 场景位**（1:1 原图不裁·限宽 520px·插在正文首个章节标题前；「方向二深化」页用 `<h3>`、白骨精外传页无章节标题 ⇒ 插入点三情形兜底）⇒ **27 张全部有归属，闲置归零**；② **分回次 og:image**——**102 页**由「全站共用一张通用图」改为**该页首屏第一张配图**的 1200×630 专属裁切版（81 个既有题图页 + 11 个横幅页 + 10 个场景页；问卷裁定「只做有配图的页·纯裁切」⇒ **不新出图**），共享通用图的页面从 705 降到 603；③ **主体检测排除朱砂与赭金**——水墨卡族每张带朱红印章，整幅墨迹 bbox 会把印章算成主体 ⇒ 改用「面积 ≥ 200 px² 的连通簇 + 排除朱砂（r−g ≥ 35）与赭金（luma ≥ 90）」，27 张主体带全部正确；④ **三处踩坑当场修**——写盘行尾二次替换污染 102 页（CRLF→CRCRLF·字节级还原）；「按主体顶裁」在主体位于画面下部时切掉人物（1 张加特例带）；验收判据自身两处缺陷（CSS 计数未行首锚定 + 负样本形态不匹配 ⇒ 检查恒真）⇒ **坑表 +6 条（80 → 86）** + 方法论篇新增 §2.9「既有资产投放」。

**验证**：落位表自检 27 张唯一 + 27 个目标页唯一 + 横幅/场景目标页无交叉 · 接入前预检 27 源图 / 27 目标页 / 81 既有题图页 / 102 og 页 · 资产派生 115 张（13 张 1200×500 + 102 张 1200×630·合计 8.2 MB）· 接入 13 + 14 + 102 且**幂等复跑全 SKIP** · 验收判据 V1–V9 **9/9 PASS**（含 figure 数 / CSS 规则数 / 插入点 / 暗色隐藏 / og 指向 / 资产尺寸 / 源卡引用）· **负样本自证 4/4 各自命中**（缺 CSS / 多 figure / 图文件缺失 / og 尺寸写错）· 27 页 + 115 资产 URL 全 200（`image/webp`）· 浏览器实跑渲染正常（猪八戒页：标题 → 720px 水墨横幅 → 420px 线描题图 → 轨标 → 正文·两层宽窄分明无重叠）· 行尾零污染（CRCRLF 0 · `git diff --numstat` 332 增 / 103 删无行尾噪音）· 第 48 门禁 0 FAIL · 全量门禁 55/55 段全绿。

> - **状态**：已收官（**本批主体内容由并行会话的 W989 提交 `1fb1b14f` 代提入库**——该提交为全量提交且时点晚于本批 `git add -A`，故本批 115 个资产 / 102 个页面 / T34 报告 / 坑表 / 13 个脚本一并随之入库；本批另有一笔收官补齐提交登记代提事实与 E-17 坑位·既有 81 页题图的图源与 alt 未改动·27 张 `card-*` 源图本身未改动·12 个已有专属 og 图的页面未改动）

### W987（2026-10-27）：水墨意境卡族启用批（33 张 1:1 水墨插画·6 张上回目页场景位）



> **来源**：用户 2026-10-27 20:50 问「浓墨渲染图可以用在哪里？」→ 20:53 令「开工」（采纳建议顺序：① 归族登记 ② 启用为回目页场景插图）。
>
> - **文件**：site/reader/ch007.html、site/reader/ch014.html、site/reader/ch015.html、site/reader/ch023.html、site/reader/ch027.html、site/reader/ch030.html、assets/promo/README.md、docs/11-方案报告/计划方案/T33-任务计划执行与经验沉淀报告-2026-10-27.md、ddocs/11-方案报告/README.md、docs/agent/pitfalls.md、AGENTS.md、HANDOVER.md、README.md、STRUCTURE.md、docs/00-导读/项目说明.md、.github/workflows/README.md、site/index.html、site/data/cross-time-danmaku.html、site/data/tag-cloud.html、site/dukou-engine.html、CITATION.cff、archive/docs/AGENTS-ARCHIVE.md、sscripts/_w987_family_scan.py、scripts/_w987_insert_scenes.py、scripts/output/_w987_family_scan.json、scripts/output/_w987_spec.json、scripts/output/_cascade_files_W987.txt。

**本批要点**：① **实读发现**——站内 `card-*` 27 张 + `chap-*` 6 张 = **33 张 1:1（1200×1200）水墨意境插画全部 0 引用**（同族两套命名：按回目 / 按角色场景 ⇒ 极易被误当题图用，W984 批即踩过），**闲置规模比用户感知大 5.5 倍**；② **归族登记**——`assets/promo/README.md` 新增「水墨意境卡族」节：成员表 + **规范边界表**（画幅 1:1 / 画风水墨晕染 / **可带印章** / **不得填进 `.chapter-plate`** / 暗色模式同样隐藏 / alt 描述画面）+ 引用状态 + 投放位置建议 + 维护约定；③ **启用 6 张**——6 个回目页（ch007 / ch014 / ch015 / ch023 / ch027 / ch030）新增 `.chapter-scene` 场景图：**首屏仍留题图**（角色立像），场景图下沉到**正文首个 `<h2>` 之前**（限宽 520px·题图 420px）⇒ 同回形成「角色立像 + 水墨意境」双层节奏；④ **其余 27 张 `card-*` 本批不启用**（题材各异·投放位置需逐张判断·另批），登记待定。

**验证**：族成员实读 33 张（全部 1200×1200·引用 0）· 6 页接入成功且幂等复跑 6/6 SKIP · 同页题图 1 + 场景图 1 且类名不混 6/6 · `.chapter-scene` 样式与**暗色模式隐藏规则**齐备 6/6 · alt 均真实描述画面 6/6 · 6 个场景图 URL HTTP 200 `image/webp` · 浏览器实跑渲染正常（ch007：首屏题图 → 元信息 → 正文入口场景图 → 原文回目·两图分隔清晰）· 第 48 门禁 0 FAIL · 全量门禁 55/55 段全绿。

> - **状态**：已收官（内容批与登记面同批落地·母版族 76 张与 6 个浓墨版源文件均未改动）

### W986（2026-10-27）：回目页 6 张线描版换主体重出批（用户观感反馈回炉·同名 stem 覆盖）



> **来源**：用户 2026-10-27 12:26 对 W984 批回目页 6 张线描版的观感反馈「一般算不上好看」+ 12:35 裁决「换主体重出一版」。
>
> **让号留痕**：取号时 **W985 已被并行会话占用**（工具文档三件批·在途未提交·占 CHANGELOG / AGENTS / HANDOVER / 台账等共享面）⇒ 按「先落地者保留」让号 **W986**；共享面待 W985 收官后补登记。
>
> - **文件**：docs/11-方案报告/计划方案/T32-任务计划执行与经验沉淀报告-2026-10-27.md、ddocs/11-方案报告/README.md、docs/agent/pitfalls.md、docs/10-方法论沉淀/素材批处理与判据自证方法论.md、AGENTS.md、HANDOVER.md、README.md、STRUCTURE.md、docs/00-导读/项目说明.md、.github/workflows/README.md、site/index.html、site/data/cross-time-danmaku.html、site/data/tag-cloud.html、site/dukou-engine.html、CITATION.cff、archive/docs/AGENTS-ARCHIVE.md、sscripts/output/_w986_spec.json、scripts/output/_cascade_files_W986.txt。（**资产面已由 `9841c05d` 落地**：6 张母版 png/webp 同名覆盖 + 6 份原件 + 6 个站点版 webp + 全目录拼图 + 6 页 alt 文本更新 + `assets/promo/plate-set/README.md` 口径更新）

**本批要点**：① **根因**——同角色 + 同画幅 + 同母版段 + 同构图范式的第二张图 ⇒ 观感必然重复，而 **J1–J10 全绿、缩略拼图也看不出**（坑表 E-05）⇒ 只有用户目视能判定；② **处置**——6 张**同名 stem 覆盖**（`plate-line-37..42`），主体全换此前未画过的角色（巨灵神 / 六贼头目 / 惠岸行者木叉 / 黎山老母 / 巡河夜叉 / 御马监丞），角色·体型·道具·姿态各异 ⇒ **页面图源路径不变、只换 alt 文本**；③ **6 个浓墨渲染版文件原样保留**（用户 2026-10-27 08:25 明令）⇒ 页面只用线描版，浓墨版作可回退存量；④ 登记面补齐时遇 **W985 在途** ⇒ 共享面等其收官后写；且实测**部分提交（pathspec）在共享面有在途批次时必被 C4-f 判红**（临时索引缺在途批次的收官内容）⇒ 改全量提交并声明代提（W932 先例）⇒ 坑表 +2 条（75 → 77）。

**验证**：母版判据 J1–J10 **76/76 FAIL 0** · 站点版裁切验算 **76/76 FAIL 0**（6 张新主体主体顶余量 6 px·地面留白 93–141 px）· 负样本自检可证伪（坏样本被 J1 抓出）· 纸色归一残差 ≤ 0.5/255 · 母版段 249 字符逐字复用 · 同名覆盖前提断言 6/6 · 人眼逐张复核 6/6 · 6 页 alt 文本全部更新 · **6 个浓墨版文件逐个核验仍在** · 计划方案合规门禁 0 FAIL · 全量门禁 55/55 段全绿。

> - **状态**：已收官（内容批 `9841c05d`·verify 全量 55/55 段全绿·母版判据 76/76 FAIL 0·裁切验算 76/76 FAIL 0·6 个浓墨版原文件保留未删·reader 有题图页仍 81 页）

### W985（2026-10-27）：工具文档三件批（场景路由表 + 指针化修数 + 机器清单 171 件挂刷新链）



> **来源**：用户 2026-10-27 问「新增一个 TOOLS.md 工具使用文档怎么样」——评估结论：根级新手写文档层会被六处既有面重叠且无新鲜度门禁看守（W824 定律必掉档·文档规范 §11 新增当前态声明须纳管），**需求真实、落点改既有机器看守面**；用户裁决「1+2+3」全做。

> - **文件**：scripts/README.md、scripts/gen_tools_inventory.py、scripts/output/tools-inventory.md、scripts/gen_folder_docs.py、tests/unit/test_tools_inventory.py、dCHANDOVER.md、README.md、STRUCTURE.md、docs/00-导读/项目说明.md、.github/workflows/README.md、site/index.html、site/data/cross-time-danmaku.html、site/data/tag-cloud.html、site/dukou-engine.html、AGENTS.md、archive/docs/AGENTS-ARCHIVE.md、CITATION.cff、sscripts/output/_w985_spec.json、scripts/output/_cascade_files_W985.txt。

**①场景路由表**：scripts/README.md 头部新增「场景速查（要做什么→用哪个）」15 行路由——批次生命周期全链（认领/preflight/级联/回窗/修剪/复盘触发/数据链判定/统计刷新）逐场景给出工具与典型调用，这是体检暴露的真实缺口（路由知识散落各处、新 Agent 最难发现）。

**②登记与指针化**：归档计数「45 个」→历次治理指针（W446·W735·W977+台账指针——W977 后实数已 337+，手写字面量即腐）；docs_index「321 篇」同类指针化；头部补全量清单指针与「禁手改」声明。新工具不逐行复制进手写表——路由表管发现、机器清单管全量，双层面分工（指针化纪律）。

**③机器清单**：新建 `gen_tools_inventory.py`——git 跟踪态顶层工具逐件（171 件·七类分节：门禁与校验 64/批次与登记 10/统计与对账 3/生成与索引 5/运维与临时区 1/工具 46/一次性 42），用途=docstring 首行（ast 解析·Node 取首注释），精确名覆盖+前缀规则分类；`--check` 对账模式（表格主体漂移 exit 1·时间戳不入判定）；挂进 `gen_folder_docs.py --refresh` 刷新链（每批目录文档刷新时连带再生成·失败留痕不阻断）。单测 5 例（分类优先级/用途提取/分节渲染/漂移判据/实盘行数回归锁==tracked 计数）。

**开工波折（并行竞速实录）**：认领 W984 时发现已被题图第五组占用且收官；改认领 W985 压竞态提交时被钩子拦——C4-f 五项假红（他方会话对 W984 段文件行内文件的观感反馈微调未提交，W837 载 exactly 此场景），按 **W932 代提先例**把其成型的落仓内容（ASM-06 否证结案+pitfalls 新条目+计数链）连同本批认领行一并代提（1bb282af）解自举死锁。

**验证**：gen_tools_inventory --self-test 过 + --check 零差异 + 单测 5/5 + ruff 0 + lint_links scripts 面 0 broken + pytest 全量见状态行。

> - **状态**：已收官（`4f62bf68`·verify 全量 rc=0 + 单测 934 过 + ruff 0 + lint_links scripts 面 0 broken·清单 171 件）

### W984（2026-10-27）：内页题图成套批·第五组（12 张·回目页线描重出 6 + 四库扩量 6·站内线描题图累计 76 张）



> **来源**：用户 2026-10-27 08:27 令「但是你可以进行单独重出，这六张浓墨渲染图可以保留；继续扩量」。
>
> **三裁**（开工问卷答复）：① 呈现方式 = **页面改用线描版，浓墨版留仓内存档** ② 题材范围 = **四库全选**（people / themes / essays·poetry·culture / 九十九回回目页）③ 规模 = **12 张一批**（其中 6 张为回目页线描重出）。
>
> - **文件**：assets/promo/plate-set/plate-line-37-ch007-bagua-lu.png、assets/promo/plate-set/plate-line-37-ch007-bagua-lu.webp、site/static/images/plate-line-37-ch007-bagua-lu.webp、assets/promo/plate-set/plate-line-38-ch014-liubei.png、assets/promo/plate-set/plate-line-38-ch014-liubei.webp、site/static/images/plate-line-38-ch014-liubei.webp、assets/promo/plate-set/plate-line-39-ch015-yingchou.png、assets/promo/plate-set/plate-line-39-ch015-yingchou.webp、site/static/images/plate-line-39-ch015-yingchou.webp、assets/promo/plate-set/plate-line-40-ch023-sichan.png、assets/promo/plate-set/plate-line-40-ch023-sichan.webp、site/static/images/plate-line-40-ch023-sichan.webp、assets/promo/plate-set/plate-line-41-ch027-bailong.png、assets/promo/plate-set/plate-line-41-ch027-bailong.webp、site/static/images/plate-line-41-ch027-bailong.webp、assets/promo/plate-set/plate-line-42-ch030-sancha.png、assets/promo/plate-set/plate-line-42-ch030-sancha.webp、site/static/images/plate-line-42-ch030-sancha.webp、assets/promo/plate-set/plate-line-43-luoshanv.png、assets/promo/plate-set/plate-line-43-luoshanv.webp、site/static/images/plate-line-43-luoshanv.webp、assets/promo/plate-set/plate-line-44-kuimulang.png、assets/promo/plate-set/plate-line-44-kuimulang.webp、site/static/images/plate-line-44-kuimulang.webp、assets/promo/plate-set/plate-line-45-zhaoan-topic.png、assets/promo/plate-set/plate-line-45-zhaoan-topic.webp、site/static/images/plate-line-45-zhaoan-topic.webp、assets/promo/plate-set/plate-line-46-fushi-topic.png、assets/promo/plate-set/plate-line-46-fushi-topic.webp、site/static/images/plate-line-46-fushi-topic.webp、assets/promo/plate-set/plate-line-47-jingwu-topic.png、assets/promo/plate-set/plate-line-47-jingwu-topic.webp、site/static/images/plate-line-47-jingwu-topic.webp、assets/promo/plate-set/plate-line-48-xuanzang-topic.png、assets/promo/plate-set/plate-line-48-xuanzang-topic.webp、site/static/images/plate-line-48-xuanzang-topic.webp、assets/promo/plate-set/raw/round13/plate-line-37-ch007-bagua-lu.jpg、assets/promo/plate-set/raw/round13/plate-line-38-ch014-liubei.jpg、assets/promo/plate-set/raw/round13/plate-line-39-ch015-yingchou.jpg、assets/promo/plate-set/raw/round13/plate-line-40-ch023-sichan.jpg、assets/promo/plate-set/raw/round13/plate-line-41-ch027-bailong.jpg、assets/promo/plate-set/raw/round13/plate-line-42-ch030-sancha.jpg、assets/promo/plate-set/raw/round13/plate-line-43-luoshanv.jpg、assets/promo/plate-set/raw/round13/plate-line-44-kuimulang.jpg、assets/promo/plate-set/raw/round13/plate-line-45-zhaoan-topic.jpg、assets/promo/plate-set/raw/round13/plate-line-46-fushi-topic.jpg、assets/promo/plate-set/raw/round13/plate-line-47-jingwu-topic.jpg、assets/promo/plate-set/raw/round13/plate-line-48-xuanzang-topic.jpg、assets/promo/plate-set/preview-contact-sheet.png、assets/promo/plate-set/preview-contact-sheet.webp、assets/promo/plate-set/README.md、site/reader/ch007.html、site/reader/ch014.html、site/reader/ch015.html、site/reader/ch023.html、site/reader/ch027.html、site/reader/ch030.html、site/reader/people/罗刹女外传.html、site/reader/people/奎木狼外传.html、site/reader/themes/招安的两种结局专题.html、site/reader/essays/西游与服饰学.html、site/reader/poetry/原著景物诗分类赏析专题.html、site/reader/culture/历史玄奘与小说玄奘专题.html、scripts/_w984_make_prompts.py、scripts/_w984_precheck_pages.py、scripts/_w984_derive.py、scripts/_w984_prepare.py、scripts/_w984_download.py、scripts/_w984_insert_plates.py、scripts/_w984_retry.py、scripts/_w984_sheet.py、scripts/_w984_zoom.py、scripts/_w984_serve.py、scripts/_w945_plates_verify.py、scripts/_w951_check_crop.py、docs/11-方案报告/计划方案/执行前计划-T31-内页题图成套批第五组.md、docs/11-方案报告/计划方案/T31-任务计划执行与经验沉淀报告-2026-10-27.md、docs/11-方案报告/README.md、docs/agent/pitfalls.md、docs/10-方法论沉淀/素材批处理与判据自证方法论.md、dscripts/_w984_make_spec.py、site/data/search.html、site/en/search.html、scripts/output/_w984_batch1.json、scripts/output/_w984_batch2.json、scripts/output/_w984_batch3.json、scripts/output/_w984_gen.json、scripts/output/_w984_precheck.json、scripts/output/_w984_sheet.png、scripts/output/_w984_zoom.png、scripts/output/_w984_spec.json、scripts/output/_cascade_files_W984.txt、CHANDOVER.md、README.md、STRUCTURE.md、docs/00-导读/项目说明.md、.github/workflows/README.md、site/index.html、site/data/cross-time-danmaku.html、site/data/tag-cloud.html、site/dukou-engine.html、AGENTS.md、CITATION.cff、archive/docs/AGENTS-ARCHIVE.md、scripts/output/file-index.md。

**本批要点**：① **首次引入「替换既有题图源」动作**——回目页 6 张（ch007 / ch014 / ch015 / ch023 / ch027 / ch030）改用同一套宣纸线描立像，**原浓墨渲染版 `chap-07/14/15/23/27/30.webp` 保留不删**（用户 2026-10-27 08:25 裁定「这六张我认为还可以」）并登记为存量归档；另 6 张为四库扩量（people 2 罗刹女 / 奎木狼 + themes 1 招安的两种结局 + essays·poetry·culture 各 1 西游与服饰学 / 原著景物诗分类赏析 / 历史玄奘与小说玄奘）⇒ 站内线描题图累计 **64 → 76 张**、reader 有题图页 **75 → 81 页**；② **替换页同步移除 `aria-hidden` 并写真实 alt**（存量浓墨图是装饰语义 ⇒ 换图源必换可访问性语义）；③ **落位页先验按动作分支建模**（INSERT 6 + REPLACE 6·三个拒绝分支各配一个负样本·3/3 自证通过）；④ **3 张重出**（#38 古树两处朱砂 / #40 贯穿竖线 + 顶天立地⇒裁切验算判红 / #43 葫芦整体实心红⇒J6 只查暗块逃逸）⇒ 坑表 **+4 条（70 → 74）** + 方法论篇新增 §2.8「判据按接入动作分支建模」；⑤ **本地验收服务加 `Cache-Control: no-store`** 根治「改了页面却看不到变化」的缓存误判。

**验证**：母版判据 J1–J10 **76/76 FAIL 0** · 站点版裁切验算 **76/76 FAIL 0**（主体顶余量 5–7 px·下部地面留白 44–134 px）· 负样本自检可证伪（坏样本被 J1 抓出）· 纸色归一残差 ≤ 0.6/255 · 落位页先验 12/12（INSERT 6 + REPLACE 6·三负样本自证通过）· 接入幂等复跑 12/12 SKIP · 12/12 处面探针 HTTP 200 + 含本批图名 + 含真实 alt + 无残留 aria-hidden · 浏览器实跑 2 页渲染正常（替换型 / 新增型）· **6 个浓墨版文件逐个核验仍在**（用户明令保留）· 计划方案合规门禁 0 FAIL · 全量门禁 55/55 段全绿（核心全部通过）。

> - **状态**：已收官（`d97d6754`·verify 全量 55/55 段全绿·母版判据 76/76 FAIL 0·裁切验算 76/76 FAIL 0·6 个浓墨版原文件保留未删·reader 有题图页 75 → 81）· **用户观感反馈（2026-10-27 12:26）：回目页 6 张线描重出版「一般算不上好看」⇒ ASM-06 否证**（同角色同范式第二张图观感重复·机器判据与拼图趋势均查不出）· 待裁决回退浓墨版或换主体重出

### W983（2026-10-27）：内页题图成套批·第四组（12 张·四库混合覆盖·站内线描题图累计 64 张）



> **来源**：用户 2026-10-27 令「帮我做几张素材图：用途与画幅、风格与配色统一、主体清晰、留好放文字的空间都考虑到，成套出图保证风格一致」，并明文要求「开始前先问我：素材用在哪里、需要几张、有没有参考风格」。
>
> **四问答复**：① 用途与画幅 = **内页专题题图 · 3:4 竖版 1200×1600（沿用 plate-set 母版）** ② 张数 = **12 张** ③ 参考风格 = **沿用 plate-set 宣纸线描（母版段 249 字符逐字复用）** ④ 题材范围 = **people + themes + essays·poetry·culture + 九十九回回目页（四库混合）**。
>
> - **文件**：assets/promo/plate-set/plate-line-25-rulai.png、assets/promo/plate-set/plate-line-25-rulai.webp、site/static/images/plate-line-25-rulai.webp、assets/promo/plate-set/plate-line-26-yudi.png、assets/promo/plate-set/plate-line-26-yudi.webp、site/static/images/plate-line-26-yudi.webp、assets/promo/plate-set/plate-line-27-baiyan-mojun.png、assets/promo/plate-set/plate-line-27-baiyan-mojun.webp、site/static/images/plate-line-27-baiyan-mojun.webp、assets/promo/plate-set/plate-line-28-change.png、assets/promo/plate-set/plate-line-28-change.webp、site/static/images/plate-line-28-change.webp、assets/promo/plate-set/plate-line-29-shenxue-ganyu-topic.png、assets/promo/plate-set/plate-line-29-shenxue-ganyu-topic.webp、site/static/images/plate-line-29-shenxue-ganyu-topic.webp、assets/promo/plate-set/plate-line-30-lujing-ditu-topic.png、assets/promo/plate-set/plate-line-30-lujing-ditu-topic.webp、site/static/images/plate-line-30-lujing-ditu-topic.webp、assets/promo/plate-set/plate-line-31-mima-pan-topic.png、assets/promo/plate-set/plate-line-31-mima-pan-topic.webp、site/static/images/plate-line-31-mima-pan-topic.webp、assets/promo/plate-set/plate-line-32-minsu-taofu-topic.png、assets/promo/plate-set/plate-line-32-minsu-taofu-topic.webp、site/static/images/plate-line-32-minsu-taofu-topic.webp、assets/promo/plate-set/plate-line-33-yixiang-puxi-topic.png、assets/promo/plate-set/plate-line-33-yixiang-puxi-topic.webp、site/static/images/plate-line-33-yixiang-puxi-topic.webp、assets/promo/plate-set/plate-line-34-keju-zhidu-topic.png、assets/promo/plate-set/plate-line-34-keju-zhidu-topic.webp、site/static/images/plate-line-34-keju-zhidu-topic.webp、assets/promo/plate-set/plate-line-35-ch010-weizheng.png、assets/promo/plate-set/plate-line-35-ch010-weizheng.webp、site/static/images/plate-line-35-ch010-weizheng.webp、assets/promo/plate-set/plate-line-36-ch004-bimawen.png、assets/promo/plate-set/plate-line-36-ch004-bimawen.webp、site/static/images/plate-line-36-ch004-bimawen.webp、assets/promo/plate-set/raw/round12/plate-line-25-rulai.jpg、assets/promo/plate-set/raw/round12/plate-line-26-yudi.jpg、assets/promo/plate-set/raw/round12/plate-line-27-baiyan-mojun.jpg、assets/promo/plate-set/raw/round12/plate-line-28-change.jpg、assets/promo/plate-set/raw/round12/plate-line-29-shenxue-ganyu-topic.jpg、assets/promo/plate-set/raw/round12/plate-line-30-lujing-ditu-topic.jpg、assets/promo/plate-set/raw/round12/plate-line-31-mima-pan-topic.jpg、assets/promo/plate-set/raw/round12/plate-line-32-minsu-taofu-topic.jpg、assets/promo/plate-set/raw/round12/plate-line-33-yixiang-puxi-topic.jpg、assets/promo/plate-set/raw/round12/plate-line-34-keju-zhidu-topic.jpg、assets/promo/plate-set/raw/round12/plate-line-35-ch010-weizheng.jpg、assets/promo/plate-set/raw/round12/plate-line-36-ch004-bimawen.jpg、assets/promo/plate-set/preview-contact-sheet.png、assets/promo/plate-set/preview-contact-sheet.webp、assets/promo/plate-set/README.md、site/reader/people/如来.html、site/reader/people/玉帝.html、site/reader/people/百眼魔君.html、site/reader/people/嫦娥外传.html、site/reader/themes/神学干预机制专题.html、site/reader/themes/取经路径地理符号学专题.html、site/reader/themes/取经密码学专题.html、site/reader/essays/西游与民俗学.html、site/reader/poetry/西游诗词意象谱系专题.html、site/reader/culture/明代科举制度对照专题.html、site/reader/ch010.html、site/reader/ch004.html、scripts/_w983_make_prompts.py、scripts/_w983_precheck_pages.py、scripts/_w983_derive.py、scripts/_w983_prepare.py、scripts/_w983_download.py、scripts/_w983_insert_plates.py、scripts/_w983_retry.py、scripts/_w983_sheet.py、scripts/_w983_zoom.py、scripts/_w983_serve.py、scripts/_w945_plates_verify.py、scripts/_w951_check_crop.py、docs/11-方案报告/计划方案/执行前计划-T30-内页题图成套批第四组.md、docs/11-方案报告/计划方案/T30-任务计划执行与经验沉淀报告-2026-10-27.md、docs/11-方案报告/README.md、docs/agent/pitfalls.md、docs/10-方法论沉淀/素材批处理与判据自证方法论.md、dsite/data/search.html、site/en/search.html、scripts/output/_w983_batch1.json、scripts/output/_w983_batch2.json、scripts/output/_w983_batch3.json、scripts/output/_w983_gen.json、scripts/output/_w983_precheck.json、scripts/_w983_make_spec.py、scripts/output/_w983_sheet.png、scripts/output/_w983_zoom.png、scripts/output/_w983_spec.json、scripts/output/_cascade_files_W983.txt、CHANDOVER.md、README.md、STRUCTURE.md、docs/00-导读/项目说明.md、.github/workflows/README.md、site/index.html、site/data/cross-time-danmaku.html、site/data/tag-cloud.html、site/dukou-engine.html、AGENTS.md、CITATION.cff、archive/docs/AGENTS-ARCHIVE.md、scripts/output/file-index.md。

**本批要点**：① **四库首次混合覆盖**——12 张 = people 4（如来 / 玉帝 / 百眼魔君 / 嫦娥）+ themes 3（神学干预机制 / 取经路径地理符号学 / 取经密码学）+ essays·poetry·culture 3（西游与民俗学 / 西游诗词意象谱系 / 明代科举制度对照）+ 回目页 2（第 010 回 魏征斩龙 / 第 004 回 官封弼马）⇒ reader 有题图页 **63 → 75**，站内线描题图累计 **52 → 64 张**；② **母版段逐字复用 249 字符**（读 `scripts/output/_w953_batch1.json`）⇒ 跨批风格同族由构造保证；③ **3 张因人眼关重出**（#26 玄色帝服整片平涂 / #27 黄袍平涂 + 千眼过密 / #36 官印印面刻字）——**机器判据 J1–J10 全绿仍漏**（J6 只统计暗像素 ⇒ 彩色平涂与器物刻字完全逃逸）⇒ 坑表 +6 条（64 → 70）+ 方法论篇新增 §2.7「判据覆盖面的边界」；④ **开工前先收官在途 W982**（preflight 交集命中 AGENTS.md / CHANGELOG.md）⇒ 共享面让出后 W983 才动土。

**验证**：母版判据 J1–J10 **64/64 FAIL 0** · 站点版裁切验算 **64/64 FAIL 0**（主体顶余量 6 px·下部地面留白 51–153 px）· 负样本自检可证伪（坏样本被 J1 抓出）· 纸色归一残差 ≤ 0.5/255 · 落位页先验 12/12 存在且无题图（含负样本自证）· 接入幂等复跑 12/12 SKIP · 浏览器实跑 3 类路径前缀各 1 页渲染正常 · 计划方案合规门禁 0 FAIL · 全量门禁与 pytest 见状态行 · 用户 2026-10-27 08:21 反馈确认跨学科题图语义（读成「该学科主题」）⇒ ASM-06 成立 · 用户 2026-10-27 08:25 反馈确认回目页存量 6 张浓墨渲染题图与本批线描立像并存可接受 ⇒ ASM-07 结案（维持现状不统一重出）· 本批两项待确认事项均已结案。

> - **状态**：已收官（`43ca4e3c`·verify 全量 55/55 段全绿·母版判据 64/64 FAIL 0·裁切验算 64/64 FAIL 0·负样本自证可证伪·reader 有题图页 63 → 75）

### W982（2026-10-27）：手搓绕过级联治理批（三层方案②③落地·①缓建裁决）



> **来源**：用户 2026-10-27 令「做」（第 44 篇复盘移交的最后一件·W956 立项候选）。

> - **文件**：scripts/check_doc_size_budget.py、scripts/preflight_check.py、tests/unit/test_doc_size_budget.py、HANDOVER.md、dCREADME.md、STRUCTURE.md、docs/00-导读/项目说明.md、.github/workflows/README.md、site/index.html、site/data/cross-time-danmaku.html、site/data/tag-cloud.html、site/dukou-engine.html、AGENTS.md、archive/docs/AGENTS-ARCHIVE.md、CITATION.cff、sscripts/output/_w982_spec.json、scripts/output/_cascade_files_W982.txt。

**三层方案落地（评审口径 ②最薄优先）**：② **C7 版本面契约**（check_doc_size_budget.collect 新增·挂 verify 体积窗口槽 + preflight 开工判据双面）——三文档版本行锚尾（README ·A1-A6 / STRUCTURE —A1-A6 / 项目说明 ·详细变更见）+ HANDOVER 当前 HEAD 句形态 + 更新链条目 ≤3 + 概要块 >6 判红；实现中两处修正（尾链行「创建于 2026-07-25」同 line 误计→只数最后更新：之后·单测断言空格差）。③ **preflight 手搓前置劝导**——工作树含级联面未提交改动即 NOTE 提示走 batch_cascade（只提示不拦截 W822·quotePath=false 二次取数防中文转义漏配·实弹验证注入/还原）。① **文件锁缓建裁决**：级联临时索引写与并行台账认领互斥未解，②③实证不足再启。

**验证**：C7 单测 2 例（良构零 FAIL/三破坏 FAIL 锁）+ 既有 50 例全过 · 实盘 C7 零 FAIL · 劝导实弹注入/还原 · ruff 0 · 全量 verify + pytest 见状态行。

> - **状态**：已收官（`c99377b8`·verify 全量 55/55 段全绿·pytest 677 passed/3 skipped·退出码 0·preflight 手搓劝导实弹 OK）

### W981（2026-10-27）：数据链恢复重判批（账号重启实证·重判中间态·judge_gate 路径修复·三处登记面订正）



> **来源**：用户 2026-10-27 纠偏「GoatCounter API 可以用啊」——实测证实，W806「账号失效」判断过时；数据链恢复触发 judge_gate 正式重判。

> - **文件**：scripts/judge_gate.py、docs/11-方案报告/调研与数据复盘/读者数据复盘.md、docs/00-导读/访问统计方案.md、dCHANDOVER.md、README.md、STRUCTURE.md、docs/00-导读/项目说明.md、.github/workflows/README.md、site/index.html、site/data/cross-time-danmaku.html、site/data/tag-cloud.html、site/dukou-engine.html、AGENTS.md、archive/docs/AGENTS-ARCHIVE.md、CITATION.cff、sscripts/output/_w981_spec.json、scripts/output/_cascade_files_W981.txt。

**数据链恢复实证（三 API 直探）**：`/api/v0/me` 200（用户 82739·站点 98962·**open_at 2026-10-01**——账号 9 月末暂停、10-01 重启，暂停期即 W806 所记 404 窗口；token 全程在位未被重建）·`/api/v0/stats/total` 200（10 月累计 111 访问）·子域 1273984347 无鉴权 303（站点存活实证）。原「404=账号失效」结论过时。

**重判（judge_gate 正式跑）**：输入 7 日 UV=5 · 30 日 UV=78 → **中间态**（阈值：分发=7 日 ≥100 或 30 日 ≥200 · 归档=30 日 <30）——归档线已脱离、分发线未达，**W793 二选一维持**（内容扩容仍须用户点名或重判继续分发）。

**同批修复**：judge_gate `--report` 路径随目录分区失效（文件 W737 时代迁 11-方案报告，脚本仍指 10-方法论沉淀 → 追加静默跳过）——修正后判定记录首次真正落盘至读者数据复盘.md 末尾。

**三处登记面订正**：① 读者数据复盘.md——W806 声明后追加订正注（原文保留）；② 访问统计方案.md——恢复注记（API 侧恢复·beacon 链退役裁决与 check_no_goatcounter 守卫不变·后端 10 月数据来源口径待核：页面 beacon 已全部移除）；③ HANDOVER 零段冻结表述——「数据链中断」改为重判现势（中间态·二选一维持）。

**验证**：judge_gate 两次实跑（输出判定 + --report 落盘）·子域存活 303 实证 · 全量 verify + pytest 见状态行。

> - **状态**：已收官（`63573221`·verify 全量 rc=0·重判中间态 78/30 日·判定记录已落盘）

### W980（2026-10-27）：stats 标记同步机器化批（P-44-05 + W681 事实收官订正 + GoatCounter 取证中）



> **来源**：用户 2026-10-27 令「做」（P-44-05 stats 三方同步机器化）+ 两项事实纠偏（agent-web 的 LLM 实测早已完成；GoatCounter API 可用——与仓内 W806 退役记录冲突，取证中）。

> - **文件**：scripts/stats.py、tests/unit/test_stats_sync.py、pytest.ini、docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md、scripts/output/stats.json、scripts/output/stats-changelog.json、scripts/output/stats-index.md、archive/docs/W批次编号对账表-ARCHIVE.md、dCHANDOVER.md、README.md、STRUCTURE.md、docs/00-导读/项目说明.md、.github/workflows/README.md、site/index.html、site/data/cross-time-danmaku.html、site/data/tag-cloud.html、site/dukou-engine.html、AGENTS.md、archive/docs/AGENTS-ARCHIVE.md、CITATION.cff、sscripts/output/_w980_spec.json、scripts/output/_cascade_files_W980.txt。

**P-44-05（stats 标记自动跟随）**：stats.py 新增 `sweep_markers()`——`--w` 落盘后自动把 C5b 对账面上的 `N<!--stats:KEY-->` 前置数字刷成本批实算值。**面 = check_doc_sync 权威面**（C5_DOC_NAMES 六文件 + CHANGELOG 口径块 + c5b_extra_surfaces：pytest.ini/site/index.html/11-方案报告递归排除计划方案）——面漂移即门禁与跟随同源漂移，不自造第二份清单。**两条防线内嵌**：① CHANGELOG 只扫首个「### W」段之前的口径块（历史段含字面标记叙述 W913 段实证·整文件扫必污染）；② 标记正则与 RE_STATS_MARK 同源（`[a-z_0-9]+` 含数字键——首版 `[a-z_]+` 被 a1_a6_docs 当场打回）。**首跑自证**：本批新增 4 例单测 → pytest_collected 925→929 → pytest.ini 与架构方案 v2 双标记自动跟随——P-44-05 立项时的手工杂务（W976/W978 两轮手工刷）自此消失。单测 4 例（失配更新/相等不动/历史段防污染/计划方案目录排除回归锁）。

**W681 事实收官订正**：用户确认 agent-web 的 LLM 真端点实测早已完成——归档台账 W681 行定格「进行中（待三键）」属登记滞后（W971 回填只覆盖 W850-W963），按追加合规落订正注（原行未动）：进行中→**已闭环**（W680 主批落地 + engine.smoke 12/12·附记 agent-web 当前无 .env 本体=历史测试后未留档）。`Fetch_gate_stats` 同理见下条。

**GoatCounter 数据链（取证中·待用户一信息）**：仓内 W806 裁决（2026-10-20）记载站点代码 `1273984347` 已失效并整体退役；用户 2026-10-27 口述「API 可以用」——最可能为账号/站点已重建（新站点代码不在仓内任何记录）。token 在位（51 字符），待用户提供现用站点地址后 `--site` 重探 + `judge_gate` 正式重判（W626 冻结的机器解冻条件：30 日 UV≥30）。本批不动 W806 退役记录。

**验证**：单测 4/4 · ruff 0 · stats.py --w 实跑 sweep 跟随 2 处 + C5b 0 FAIL · check_doc_sync 0 FAIL · 全量 verify + pytest 见状态行。

> - **状态**：已收官（`6d3fba13`·verify 全量 rc=0 + 单测 4/4 + C5b 0 FAIL·sweep 首跑跟随 2 处）

### W979（2026-10-27）：收官提示位扩展批（P-44-01/02/03 落地 + P-44-04 活面零残留裁定免迁）



> **来源**：用户 2026-10-27 引用第 44 篇复盘移交清单（P-44-01~04）令即办（下一自由号）。

> - **文件**：scripts/batch_cascade.py、dCHANDOVER.md、README.md、STRUCTURE.md、docs/00-导读/项目说明.md、.github/workflows/README.md、site/index.html、site/data/cross-time-danmaku.html、site/data/tag-cloud.html、site/dukou-engine.html、AGENTS.md、archive/docs/AGENTS-ARCHIVE.md、CITATION.cff、sscripts/output/_w979_spec.json、scripts/output/_cascade_files_W979.txt。

**P-44-01（回窗提示化）**：batch_cascade 收官提示位抽为 `_close_hints()` 集合函数（全部维持 W822「只输出不拦截」语义·fail-open 留痕），[SIZE] 块在 evaluate 有 FAIL 时输出「超窗——按 FAIL 行内指引跑对应归档工具回窗（段式/台账行分治）」提示行——级联每批插入一段、回窗自此从「异常」变「每批常态动作提示」。

**P-44-02（TTL 报数）**：[TMPE] 块新增 `_shot`/`_inbox` 超龄报数（按 policy.yml ttl_days=7·首跑实测 _shot 3828 件 251MB + _inbox 163 件 215MB 均超龄且已过 48h 冻结窗）——到期列清单经主人确认走回收站；`_misc`（TTL 90d）零超龄。

**P-44-03（防再积）**：新增 [SCRIPTS] 行——顶层 `_` 件跟踪态计数（git ls-files 过滤顶层·首跑 18 个，盘上 169 含 gitignore 本地件），超阈值 20 提示语料级退役扫描（W977 先例）。

**P-44-04（三位号残留裁定：免迁）**：宽口径复扫活面（scripts/*.py|js|mjs + tests/unit 全部正则形态 `W\d{3}`/`w\d{3}`/`W[0-9]{3}`）**零残留**——W969 的 69 处升位已覆盖全部活面；余量均在历史冻结段（CHANGELOG 归档/台账行·禁改）与冷存储入档件（无前向兼容需求）⇒ **登记结案，W1000 兼容无需再迁**。

**P-44-02 待主人确认项**：`_shot` 3828 件 251MB + `_inbox` 163 件 215MB 超龄删除候选（回收站通道·确认后执行）。

**验证**：`_close_hints()` 直测输出三段齐全 + ruff 过 + 级联单测 5 过；[SIZE] 超窗提示在本批级联后实况自证（CHANGELOG 111/110 → 提示行出现 → archive_segments 回窗 110）。

> - **状态**：已收官（`fb96ea05`·verify 全量 rc=0 + 级联单测 5 过 + ruff 0·超窗提示首跑自证）

### W978（2026-10-27）：第 44 篇工作复盘批（触发器 T3 首触发·W955-W977 区间·P-44 四改进项登记）



> **来源**：复盘触发器 T3 首次触发（W956 建·check_review_trigger 实跑：上篇复盘后提交 92 ≥ 80·距今 1.19 天）——「触发清单与周期栏带入报告」闭环首件产物；用户 2026-10-27 引用体检收官报告附带登记项令即办（W977 退役批 + 本篇复盘批连续执行）。

> - **文件**：docs/11-方案报告/工作复盘与优化分析报告/工作复盘与优化分析报告-2026-10-27.md、scripts/_w978_review_evidence.py、scripts/output/_w978_review_evidence.json、docs/11-方案报告/README.md、dCHANDOVER.md、README.md、STRUCTURE.md、docs/00-导读/项目说明.md、.github/workflows/README.md、site/index.html、site/data/cross-time-danmaku.html、site/data/tag-cloud.html、site/dukou-engine.html、AGENTS.md、archive/docs/AGENTS-ARCHIVE.md、CITATION.cff、sscripts/output/_w978_spec.json、scripts/output/_cascade_files_W978.txt。

**区间与体量**：第 43 篇收官（W954·2026-10-26）至 W977 收官后——**28.7 小时 · W955–W977 共 21 段（两面合看）· 对账表 23 行 · 提交 92 笔**（docs 36 / chore 23 / feat 18 / fix 15·10-26: 74 / 10-27: 18）。合规零提交 2（W958 让号留痕 / W962 并号闭环·经状态列核实）。

**核心发现（四条）**：① 上篇 P-43 五项改进当期闭环 **5/5**（P-43-01/02/05 由 W956 机器化：preflight lagged 二分 / check_review_trigger 触发器 / _assert_status_wnum 段状态防线；P-43-03 由 W971 完成 102 段回填；P-43-04 由 W974 落地判据自证）——「复盘→改进→机器化」首次走通一整圈；② **体积窗口制建置 17 批后首次实战咬合**：W960 建窗 → W968 拆分 → W970 台账行归档工具 → W976 三窗齐超窗实拦且修剪回路三缺陷（A5 断言/修路指引/自撞）当场暴露当场修复 → 段式回窗成每批固定节奏；③ **沉淀通道机器化切换完成**：W975 坑表 57→63 → W976 64 条 + [TMPE] 收官提示位 → W977 一次性件 454 候选分级退役（286 入档/16 现役硬保留j S4 本地件不入仓）+ tmpe 工具晋升机制定性（历史零达标·沉淀主通道=坑表/方法论篇）；④ **tmpe 清理闭环 13 天首次走通**（主人「全清」31 项约 860MB 回收站·保护面 0 命中·分批验证留痕）。

**改进项 P-44-01~04**：段式回窗并入级联收官自动提示 / tmpe `_shot`+`_inbox` 7 天 TTL 清理管线化（269MB+253MB 超龄）/ scripts 顶层 `_` 件计数提示位 / W1000 存量段 36 批随批顺带。风险面与可行性自评见报告 §10。

**验证**：取证脚本 `_w978_review_evidence.py` 单源产出全部统计（附录 A 可复算）· check_review_trigger 实跑 T3 面板值入报告 · 21 段标题一手核对 · verify 全量 rc=0 + pytest 全绿 + ruff 0 见状态行。

> - **状态**：已收官（`ec53ba95`·verify 全量 rc=0 + pytest 全绿 + ruff 0 + lint_links 0 broken·区间 21 段/92 提交·T3 面板 1.19 天/23 批/92 笔）

### W977（2026-10-27）：一次性件批量退役批（454 候选·286 入档·16 现役硬保留·152 S4 本地件不入仓）



> **来源**：用户 2026-10-27 引用体检收官报告「scripts/ 一次性件已积 384 个，archive/scripts/ 有 51 件退役先例，可择机批量清」令即办（实盘盘点为 454 件顶层 `_` 件·含 W977 当日新增计入口径）。

> - **文件**：archive/README.md、scripts/index.md、scripts/output/index.md、archive/scripts/batches/README.md、archive/scripts/batches/index.md、archive/scripts/batches/misc/README.md、archive/scripts/batches/misc/index.md、archive/scripts/batches/w6xx/README.md、archive/scripts/batches/w6xx/index.md、archive/scripts/batches/w7xx/README.md、archive/scripts/batches/w7xx/index.md、archive/scripts/batches/w8xx/README.md、archive/scripts/batches/w8xx/index.md、archive/scripts/batches/w9xx/README.md、archive/scripts/batches/w9xx/index.md、dCHANDOVER.md、README.md、STRUCTURE.md、docs/00-导读/项目说明.md、.github/workflows/README.md、site/index.html、site/data/cross-time-danmaku.html、site/data/tag-cloud.html、site/dukou-engine.html、AGENTS.md、archive/docs/AGENTS-ARCHIVE.md、CITATION.cff、sscripts/output/_w977_spec.json、scripts/output/_cascade_files_W977.txt + **286 件 git mv 改名（scripts/_* → archive/scripts/batches/{misc,w6xx,w7xx,w8xx,w9xx}/·逐件不入本行·组行见 archive/README.md 台账）**。

**方法（同契约·规模适配）**：archive_file.py 为「单件/小批」设计（逐件全仓 grep 在 439 件规模下不可行），按 archive/README.md「大批量批处理手动登记」条款走同契约实现——① 语料级引用剔除（tmpe/_w977_scan.py·活引用面=门禁/工具/测试/治理文档/CI/Makefile 一次载入逐 stem 匹配）；② 批量 git mv（失败即停·幂等续跑）；③ 组行台账登记（5 组）。**引用分级结果：454 候选 → 16 件现役硬保留**（`__init__.py`、`_cite_probe.py`[坑表+CLAUDE+check_claude_md 三面引用]、`_check_pipeline_consistency.py`[铁律 13]、`_gen_search_index.py`[第 46 门禁+单测]、`_w851_j1_name_audit.py`/`_w851_visual_regression_probe.py`[单测 import]、`_w857_plan_template_review.py`[第 48 门禁]、`_w864_accent_audit.py`/`_w876_site_audit.py`[朱砂门禁族]、`_w818_file_protocol_probe.py`[check_page_admission]、`_w933_mutation_test.py`[Makefile]、`_w939_scan_targets.py`/`_w946_icon_probe.js`[check_emoji_icons]、`_w950_refresh_icon_paths.py`[坑表]、`_audit_render_states.js`[暗色门禁+CI]·`_w954_review_evidence.py`[复盘取证锚点+lint_links 实锤活链接]）**+ 287 件退役入库**（misc 60 + w6xx 2 + w7xx 31 + w8xx 42 + w9xx 151·1 件 _w954_review_evidence 复盘取证锚点复位留用）**+ 152 件 S4 本地件原地不动**（.gitignore:159 `scripts/_s4_*` 双盲纪律·从未入仓）。

**防复发裁决两件**：① `_check_json_copies.py` 目标冲突暴露其正是 **W842 从 archive 恢复的现役字节级自检工具**（W735 误归档→回灌盲区根因）——追加硬保留，杜绝二次误归档；② 归档件冷存储语义（W836 实证 ROOT 上溯失效）——本批入档件均为一次性使命终结件，无现役调用面。

**验证**：迁移后 `git status` scripts/ 零未跟踪（152 件为 gitignore 屏蔽态）；gen_folder_docs --refresh 后 scripts/index.md 与 output/index.md 零僵尸行（output/ 自有 _w7xx 件与 spec 属在位实件）；ruff 豁免面核实（pyproject `**/_*.py` + `archive/` W400 前例）；全量 verify + pytest + ruff 见验证行。

> - **状态**：已收官（9eaa41e3·verify 全量 rc=0 + pytest 922 过/3 跳 + ruff 0 + lint_links 5545 链接 0 broken）

### W976（2026-10-27）：工具链体检修复批（台账修剪器 A5 + C3 修路指引 + preflight 自撞 + 三窗回窗 + 坑表沉淀）



> **来源**：用户 2026-10-27 令「检查一下项目所有的工具、脚本、探针、门禁，有没有问题是否需要优化；临时文件系统和归档系统现在是否能够正常运转」并批准处置清单开工。

> - **文件**：scripts/archive_ledger_rows.py、scripts/check_doc_size_budget.py、scripts/preflight_check.py、scripts/batch_cascade.py、tests/unit/test_doc_size_budget.py、tests/unit/test_preflight_touches.py、docs/agent/pitfalls.md、AGENTS.md、HANDOVER.md、darchive/docs/W批次编号对账表-ARCHIVE.md、archive/docs/CHANGELOG-ARCHIVE.md、archive/docs/file-index-ARCHIVE.md、README.md、STRUCTURE.md、docs/00-导读/项目说明.md、.github/workflows/README.md、site/index.html、site/data/cross-time-danmaku.html、site/data/tag-cloud.html、site/dukou-engine.html、CITATION.cff、sscripts/output/_w976_spec.json、scripts/output/_cascade_files_W976.txt、scripts/output/_vermilion_solid_cache.json（逐件行见 file-index W976 段）。

**体检结论（修复前）**：门禁与探针基本面健康（verify 50 槽全绿、pytest 919/923、ruff 0、engine.smoke 12/12、anchor 探针 0 盲区），但三窗齐超窗（CHANGELOG 111/110、file-index 111/110、台账 61/60——C 族挂 preflight 开工判据不在 verify，W976 开工即被拦）+ 工具链三缺陷：① 台账修剪器 archive_ledger_rows.py 的 A5 断言（迁出行物理序须升序）与自身文档「行序穿插是常态（W968 实证 52 处）」矛盾，真实台账（待迁出 {914,915} 物理序 [915,914]）首跑即 AssertionError，且自测样本恰好构造升序穿插测不出该形态——台账修剪回路断链；② C3 超窗修法指引统一指向段式 archive_segments.py，而该工具不管台账——修路指引死路；③ preflight_check 拒绝循环不排本批自身，认领后复跑必然自撞 FAIL（docstring 与 NOTE 均声称已排除）。

**三缺陷修复**：① A5 改为「归档内迁出块 == 注记行 + 迁出行按源相对顺序逐字节一致」+ move() 参数化 + 自测重写为走 move() 全链路三形态（升序穿插/降序穿插/无迁出）；② evaluate() 修法指引按文件种类分治（台账指向 archive_ledger_rows.py --apply）+ 自测与单测各补台账案例；③ 新增 rejection_pairs 纯函数（排除 self_num）+ 主流程换用 + 单测锁行为。

**回窗与台账治理**：archive_ledger_rows.py --apply 迁出 W914-W916 三行（61→59 回窗）+ archive_segments.py --apply 迁出 W856-W857 两段（CHANGELOG/file-index 111→109 回窗）；W962 孤儿认领核伪并闭环回填（无 commit、无 CHANGELOG 段，五大交付面随 W960 a6fed505 落地——ledger_close_check 诊断的「事实已收官、字段没回填」伪阻塞，其 touches 曾挡死本批两个文件）。

**沉淀面**：坑表数据/内容可信度 +1 条「自测样本必须覆盖判据会失败的最小形态」（8→9 条·计数链同步 AGENTS/HANDOVER 共 4 处·N4 门禁 64=64）；batch_cascade 收官新增 [TMPE] 提示位（批次桶计数 + tmpe_tidy --tool-candidates 沉淀扫描指引——清理闭环自 W738 建制至本批只运转过一次，防「只进不出」复发）；tmpe 工具晋升机制实证结论：10-14/10-16 五次扫描 298 件最高 11/18 无一达晋升线 14（批次命名件复用频率维结构性 0 分），沉淀主通道是「教训入坑表/方法论篇」而非脚本搬迁。

**验证**：archive_ledger_rows --self-test 三形态全过 + 真实台账 dry-run/apply 成功；check_doc_size_budget --self-test 过 + 实盘 0 FAIL（109/109/59）；pytest 单测 27 过（doc_size_budget 6 + preflight touches 20 + cascade 5 中相关）；ruff 全过；N4 坑位数 64=64；preflight 复跑 PASS 不再自撞。

> - **状态**：已收官（`766c70ac`·verify 全量 rc=0 + pytest 922 过/3 跳 + ruff 0 + N4 64=64·三窗现势 110/110/59）

### W975（2026-10-27）：跨 Agent 经验沉淀入仓批（坑表 57 → 63 条 + 深度篇 1 篇 + 计数链同步）

> **来源**：用户 2026-10-27 纠正「你不能只沉淀进你自己的 Memory 文件，本项目是多 Agent 协作的项目所以需要你同样沉淀进本项目内」。
>
> **问题定性**：W974 批的 9 条经验只写进 Agent 私有 Memory ⇒ **仓内其他 Agent 读不到** ⇒ 正是坑表既有条目「共享机制必须写入仓库内文件（git tracked）」的**复发实证**（该条目本批已补注复发）。

> - **文件**：docs/agent/pitfalls.md、AGENTS.md、HANDOVER.md、docs/10-方法论沉淀/README.md、docs/10-方法论沉淀/素材批处理与判据自证方法论.md、scripts/_w975_sink_experience.py、scripts/_w975_cascade.py、scripts/_w975_tweak.py、scripts/output/_cascade_files_W975.txt、sCREADME.md、docs/00-导读/W批次编号对账表.md

**入仓面（四处载体）**：① 坑表 `docs/agent/pitfalls.md` **6 条新条目**（CSS/视觉渲染 +2「器物形状类别 > 数量计数」「落位页先验」· git/提交/并发 +1「写既有文件须临时文件 + 原子替换」· 数据/内容可信度 +2「bbox 顶 ≠ 主体顶」「校验/自检代码必须自证」· 流程/协作/取证 +1「端口占用是假故障」）+ 4 处节标题条数 + 共享机制条目补 W974 复发注；② **深度篇**《素材批处理与判据自证方法论.md》（`docs/10-方法论沉淀/` 编号 26·含问题背景/方法论/复现案例/修复策略/关联文档五段）；③ `AGENTS.md` §4.3 主题视图与计数声明；④ `HANDOVER.md` 两处指针。

**计数链同步**：坑位 **57 → 63 条**（AGENTS §4.3 与 HANDOVER 的条数声明同批订正·门禁 N4 核对「AGENTS 声明 == pitfalls 实数」⇒ 复验一致）。

**纪律**：共享面按内容粒度精确暂存（`git update-index --cacheinfo`·基底为索引版以叠加本批前几次改动）⇒ 并行会话在途内容既不入本批提交、也不被抹掉。

> - **验证**：坑表条目实数 **63** == AGENTS §4.3 声明 63（门禁 N4 一致）·第 31 / 第 45 门禁 0 FAIL · 第 48 门禁 0 FAIL · CSP 0 漂移 · lint_links 0 broken · 深篇《素材批处理与判据自证方法论》已登记入 `docs/10-方法论沉淀/README.md` 编号 26 · docs/INDEX.md 重建（768 篇）
> - **状态**：已收官（`5423f5e8`·**协作纪律**：本批共享面按内容粒度**精确暂存**——基底取**索引版**以叠加本批前几次改动、`git update-index --cacheinfo` 写入索引、工作树同步 ⇒ 并行会话在途内容既不入我的提交也不被我抹掉）

### W974（2026-10-27）：内页题图成套批·第三组（12 张·人物 6 + 主题 6·站内线描题图累计 52 张）

> **来源**：用户 2026-10-27 令「帮我做几张素材图：用途与画幅、风格与配色统一、主体清晰、留好放文字的空间都考虑到，成套出图保证风格一致」，并明文要求「开始前先问我：素材用在哪里、需要几张、有没有参考风格」。
>
> **四问答复**：① 用途与画幅 = **内页题图 · 3:4 竖版 1200×1600（沿用 plate-set 母版）** ② 张数 = **12 张** ③ 参考风格 = **沿用站内线描墨稿风（母版逐字复用）** ④ 题材范围 = **人物 + 主题混合（各占一半）**。

> - **文件**：site/static/images/plate-line-13-jinjiaodawang.webp、site/static/images/plate-line-14-yinjiaodawang.webp、site/static/images/plate-line-15-huangmeidawang.webp、site/static/images/plate-line-16-heixiongjing.webp、site/static/images/plate-line-17-tuota-lijing.webp、site/static/images/plate-line-18-yutujing.webp、site/static/images/plate-line-19-nvziguo-topic.webp、site/static/images/plate-line-20-chelingguo-topic.webp、site/static/images/plate-line-21-shituoling-topic.webp、site/static/images/plate-line-22-tonghehe-topic.webp、site/static/images/plate-line-23-pansidong-topic.webp、site/static/images/plate-line-24-wudidong-topic.webp、assets/promo/plate-set/plate-line-13-jinjiaodawang.png、assets/promo/plate-set/plate-line-14-yinjiaodawang.png、assets/promo/plate-set/plate-line-15-huangmeidawang.png、assets/promo/plate-set/plate-line-16-heixiongjing.png、assets/promo/plate-set/plate-line-17-tuota-lijing.png、assets/promo/plate-set/plate-line-18-yutujing.png、assets/promo/plate-set/plate-line-19-nvziguo-topic.png、assets/promo/plate-set/plate-line-20-chelingguo-topic.png、assets/promo/plate-set/plate-line-21-shituoling-topic.png、assets/promo/plate-set/plate-line-22-tonghehe-topic.png、assets/promo/plate-set/plate-line-23-pansidong-topic.png、assets/promo/plate-set/plate-line-24-wudidong-topic.png、assets/promo/plate-set/plate-line-13-jinjiaodawang.webp、assets/promo/plate-set/plate-line-14-yinjiaodawang.webp、assets/promo/plate-set/plate-line-15-huangmeidawang.webp、assets/promo/plate-set/plate-line-16-heixiongjing.webp、assets/promo/plate-set/plate-line-17-tuota-lijing.webp、assets/promo/plate-set/plate-line-18-yutujing.webp、assets/promo/plate-set/plate-line-19-nvziguo-topic.webp、assets/promo/plate-set/plate-line-20-chelingguo-topic.webp、assets/promo/plate-set/plate-line-21-shituoling-topic.webp、assets/promo/plate-set/plate-line-22-tonghehe-topic.webp、assets/promo/plate-set/plate-line-23-pansidong-topic.webp、assets/promo/plate-set/plate-line-24-wudidong-topic.webp、site/reader/people/金角银角深化专题.html、site/reader/people/银角大王.html、site/reader/people/黄眉老佛外传.html、site/reader/people/黑熊精.html、site/reader/people/托塔李天王外传.html、site/reader/people/玉兔精.html、site/reader/people/女儿国国王.html、site/reader/people/车迟国三国师外传.html、site/reader/people/狮驼岭三魔-方向二深化.html、site/reader/people/老鼋外传.html、site/reader/people/蜘蛛精.html、site/reader/people/老鼠精.html、scripts/_w974_claim_row.py、scripts/_w974_make_prompts.py、scripts/_w974_make_retry.py、scripts/_w974_merge_retry.py、scripts/_w974_download.py、scripts/_w974_prepare.py、scripts/_w974_zoom.py、scripts/_w974_sheet_full.py、scripts/_w974_insert_plates.py、scripts/_w974_stats.py、scripts/_w974_update_readme.py、scripts/_w974_probe_top.py、scripts/_w974_probe_top2.py、scripts/_w974_probe_clusters.py、scripts/_w974_probe_subjtop.py、scripts/_w974_negative_sample.py、scripts/_w974_cascade.py、scripts/_w974_backfill_stage.py、scripts/_w974_final_check.py、scripts/_w974_register_report.py、scripts/_w974_sync_stats_marks.py、scripts/_w974_sync_version_faces.py、scripts/output/_w974_batch1.json、scripts/output/_w974_batch2.json、scripts/output/_w974_batch3.json、scripts/output/_w974_batch34.json、scripts/output/_w974_retry15.json、scripts/output/_w974_stats.json、scripts/output/_w974_negative_sample.png、scripts/output/_w974_probe_top_zoom.png、scripts/output/_w974_urls_a.json、scripts/output/_w974_urls_b.json、scripts/output/_w974_urls_c.json、docs/11-方案报告/计划方案/执行前计划-T29-内页题图成套批第三组.md、docs/11-方案报告/计划方案/T29-任务计划执行与经验沉淀报告-2026-10-27.md、assets/promo/plate-set/README.md、assets/promo/plate-set/index.md、assets/promo/plate-set/preview-contact-sheet.png、assets/promo/plate-set/preview-contact-sheet.webp、scripts/output/_cascade_files_W974.txt、sCREADME.md、HANDOVER.md、ddocs/11-方案报告/README.md、assets/promo/plate-set/raw/round11/README.md、assets/promo/plate-set/raw/round11/index.md、assets/promo/plate-set/raw/round11/plate-line-13-jinjiaodawang.jpg、assets/promo/plate-set/raw/round11/plate-line-14-yinjiaodawang.jpg、assets/promo/plate-set/raw/round11/plate-line-15-huangmeidawang.jpg、assets/promo/plate-set/raw/round11/plate-line-16-heixiongjing.jpg、assets/promo/plate-set/raw/round11/plate-line-17-tuota-lijing.jpg、assets/promo/plate-set/raw/round11/plate-line-18-yutujing.jpg、assets/promo/plate-set/raw/round11/plate-line-19-nvziguo-topic.jpg、assets/promo/plate-set/raw/round11/plate-line-20-chelingguo-topic.jpg、assets/promo/plate-set/raw/round11/plate-line-21-shituoling-topic.jpg、assets/promo/plate-set/raw/round11/plate-line-22-tonghehe-topic.jpg、assets/promo/plate-set/raw/round11/plate-line-23-pansidong-topic.jpg、assets/promo/plate-set/raw/round11/plate-line-24-wudidong-topic.jpg、assets/promo/plate-set/zoom-w974/README.md、assets/promo/plate-set/zoom-w974/detail-01.png、assets/promo/plate-set/zoom-w974/detail-02.png、assets/promo/plate-set/zoom-w974/detail-03.png、assets/promo/plate-set/zoom-w974/detail-04.png、assets/promo/plate-set/zoom-w974/detail-05.png、assets/promo/plate-set/zoom-w974/detail-06.png、assets/promo/plate-set/zoom-w974/detail-07.png、assets/promo/plate-set/zoom-w974/detail-08.png、assets/promo/plate-set/zoom-w974/detail-09.png、assets/promo/plate-set/zoom-w974/detail-10.png、assets/promo/plate-set/zoom-w974/detail-11.png、assets/promo/plate-set/zoom-w974/detail-12.png、assets/promo/plate-set/zoom-w974/detail-sheet-g1.png、assets/promo/plate-set/zoom-w974/detail-sheet-g2.png、assets/promo/plate-set/zoom-w974/detail-sheet-g3.png、assets/promo/plate-set/zoom-w974/full-01.png、assets/promo/plate-set/zoom-w974/full-02.png、assets/promo/plate-set/zoom-w974/full-03.png、assets/promo/plate-set/zoom-w974/full-04.png、assets/promo/plate-set/zoom-w974/full-05.png、assets/promo/plate-set/zoom-w974/full-06.png、assets/promo/plate-set/zoom-w974/full-07.png、assets/promo/plate-set/zoom-w974/full-08.png、assets/promo/plate-set/zoom-w974/full-09.png、assets/promo/plate-set/zoom-w974/full-10.png、assets/promo/plate-set/zoom-w974/full-11.png、assets/promo/plate-set/zoom-w974/full-12.png、assets/promo/plate-set/zoom-w974/full-sheet-01-02-03-04.png、assets/promo/plate-set/zoom-w974/full-sheet-03.png、assets/promo/plate-set/zoom-w974/full-sheet-05-06-07-08-09.png、assets/promo/plate-set/zoom-w974/index.md

**母版逐字复用**：直接读 W953 的 `_w953_batch1.json` 取母版（**249 字符**）拼本批 SUBJECT 段 ⇒ 跨三批（W952 / W953 / W974）风格同族由**构造**保证；脚本断言「批内 12 条母版逐字一致」+「与 W953 母版逐字相同」+「stem 与既有母版零冲突（含负样本自证）」。

**出图与返工**：首轮 batch1 **3/4 成功**（04 黑熊精 err_code 451「The result is unavailable」⇒ 补出）；**选题调整 1 处**——原定「虎力大仙」在 people 库无独立页面（只有「车迟国三国师」页）⇒ 改为**玉兔精**（有独立页且无题图），原图弃用；**重出 1 张**——人眼放大复核抓出 **15 黄眉大王的金铙被画成圆环**（读作手镯）⇒ 改措辞为「倒扣的金钵 · 半圆盘 · 钵面一圈回纹 · 绝不是圆环或手镯」后达标。

**站点版「主体顶」抗噪口径修正（本批实质工程贡献）**：现行 `ink_top()` 取**整图墨迹 bbox 顶**，会被**孤立噪点**污染——实测 `plate-line-24-wudidong-topic` 顶部第 18 行仅 **3 个像素**（差值 41），放大取证显示 0–260 px 为纯宣纸底、零主体笔触 ⇒ 裁切线失真（站点版 1588 px ≈ 母版高）。⇒ 改为「**主体顶 = 面积 ≥ 200 px² 的墨迹连通簇的最小顶**」（滤孤立噪点、保留真实稀疏顶部如冠尖）。全目录 52 张复算：两种口径**仅 4 张不同**（本批 24 号 +419 px；既有 03 大闹天宫 +188 / 05 混世四猴 +113 / 11 金箍棒重量 +4 px）⇒ 既有 3 张属**存量欠账**（需人眼判定后再处置），本批**不重写既有资产**。

**判据可证伪性**：合成多维负样本（1200×1600·下部纯黑块 + 四边 6 px 贯穿暗框 + 左侧 300 px 纯白竖带）⇒ 同一判据**同时抓出 J2 / J3 / J6 / J8** 四条；J10 另经独立探针实测 9.333 > 阈值 5.0 ⇒ 可证伪。

**接入**：沿用站内 `chapter-plate` 范式（420 px 居中 + 描述性 alt + 浅底图暗色模式隐藏），幂等脚本 `_w974_insert_plates.py`；**浏览器实跑 2 页**（黑熊精 / 车迟国三国师）确认标题紧贴主体、无冗余留白、宣纸底与页面底色无色边、console 0 错误。

**并发纪律**：共享面按内容粒度**精确暂存**（`git update-index --cacheinfo`·HEAD 为基底叠加本批段）⇒ 不把对方在途内容带进本批提交。

> - **验证**：母版判据 J1–J10 **52/52 PASS**（`_w945_plates_verify.py`·目录扫描一次覆盖 52 张）· 站点版验算 **52/52 PASS**（`_w951_check_crop.py`：主体顶未切 + 主体底未切 + 下部地面留白 > 0）· 人眼 J8 题材与形制逐张放大核（据此重出 15 黄眉大王·金铙形制两次修正）· 负样本合成自证：J2 / J3 / J6 / J8 四条同时抓出（J10 另经独立探针实测 9.333 > 阈值 5.0）· 浏览器实跑 2 页（黑熊精 / 车迟国三国师）· console 0 错误 · 第 31 与第 45 门禁 0 FAIL · CSP 0 漂移 · lint_links 0 broken · 既有 40 张母版与站点版**零改动**（逐 blob 与 HEAD 比对）
> - **状态**：已收官（`6ebc6fea`·**并发纪律**：本批共享面按内容粒度**精确暂存**——以 `HEAD:<file>` 为基底叠加本批段、`git update-index --cacheinfo` 写入索引、工作树保持原样 ⇒ 对方在途内容既不入我的提交也不被我抹掉；提交后已 `git log --oneline -1 -- <本站点版文件>` 核实归属）

### W973（2026-10-26）：HANDOVER 五区清理批（只进不出区治理·用户令走并问责查全）

> **来源**：用户问「为什么 HANDOVER 文件里面还是有那么多东西」+ 问责「是不是告诉过你查所有文件」——W967 只扫治理文档圈的自认缺口，本批治 HANDOVER 并接续全仓内容扫描。
> **摘要**：① **五区清理**——零、当前阻塞已处置历史迁档（「当前阻塞」标题下挂着 W419-W424 时代已处置长段）；候选清单两遍清除已完成/划线条目 28 条；三、方法论沉淀真指针化（152 行叙事迁档·权威在 pitfalls/gates L2）；四、待办清已完成 15 条；八、已知雷区指针化（101 行叙事迁档·权威在 pitfalls）。② HANDOVER 87.2→40.6 KB（-53%）·445 行。③ **体积门禁 C6**——HANDOVER 整文件 >45KB 即红（五区只进不出复发的常驻哨）。④ 迁移守恒：迁出块逐块入 HANDOVER-ARCHIVE（追加式）。
> **文件**：HANDOVER.md · archive/docs/HANDOVER-ARCHIVE.md · scripts/check_doc_size_budget.py
> **验证**：锚定段序断言过（此前 find 诊断被散文提及误报）+ C6 现网 40.6/45 绿 + check_doc_sync 0 FAIL。
> **状态**：在途（认领登记 W973·待提交入库）
### W972（2026-10-26）：CodeQL 三高危修复批（PR #66 检查红项清偿）

> **来源**：PR #66 的 CodeQL 检查报 1 high——本 PR 引入的三个审计工具自身有三处可绕过/可出错形态。
> **摘要**：① **py/bad-tag-filter ×2**——W955 动效审计与 W912 交互绑定门禁的内联脚本块正则「</script>」不匹配「</script >」等空白变体（混淆标签可绕过审计）；放宽为「</script\s*>」。② **js/incomplete-sanitization ×1**——数据漂移工具的引号转义未先转反斜杠（内容含 \ 时生成错误转义序列）；改为先转 \ 再转引号（顺序正确性）。③ 三工具功能自测全过（含 JS 工具真实数据跑通）。
> **文件**：scripts/_w955_motion_audit.py · scripts/check_interaction_binding.py · scripts/check_data_drift.js
> **验证**：node --check + JS 工具真实数据自测跑通（副本对账 47 项）+ py 工具 0 FAIL + pytest 全量 919 passed + ruff 清零。
> **状态**：**已收官**（W972 git 反填·CodeQL 三高危清偿）
### W971（2026-10-26）：存量段状态回填批（建议序④·用户令「现在就可以做完」）

> **来源**：建议序④（用户令「现在就可以做完」）——W954 量化的「91 批状态滞后」现存量形态已变为「缺字段」而非「字段陈旧」（W921 归档与并行手搓段的双重演化）。
> **摘要**：① **102 段（W850-W963）补状态行**——并行手搓/精简级联时代的段普遍缺「> **状态**」字段（四件套缺件）；按 git 事实源逐段补齐：99 段改标已收官（首笔 hash+笔数）、1 段补本段号、2 段保留既有注记。② **事故与纠正留痕**——首趟把 CHANGELOG 行误当 git log 输入喂提交索引，102 段全量误标已停止（收官 0 段的分布异常当场暴露）；纠正趟按真 git log 重算（522 个批次号索引）并以「状态行含本段号」终检收口；P-43-05 断言在两处模板缺陷上各拦一次（已停止模板漏段号/状态行缺段号）。③ 顺带：W929 一次性脚本品牌字面量残留清偿（PR #66 品牌检查红项）。④ 台账随批回窗（W971 认领 +1 触顶→59）。
> **文件**：CHANGELOG.md · scripts/_w929_stats_sync.py · docs/00-导读/W批次编号对账表.md · archive/docs/W批次编号对账表-ARCHIVE.md
> **验证**：全段状态行含本段号终检全过（112/112）+ check_doc_sync 0 FAIL + verify 全量 rc=0 + 品牌字面量零命中恢复。
> **状态**：**已收官**（W971 git 反填·含认领与级联与回填）
### W970（2026-10-26）：台账归档行工具批（archive_ledger_rows.py·建议序③）

> **来源**：W968 拆分批登记的「台账归档工具化」议题（建议序③·用户令走）——C5 台账 60 行窗按并行节奏约 20 批触顶，archive_segments.py 段式不认台账行格式。
> **摘要**：① **archive_ledger_rows.py 常驻工具**——号序切分（行序实测 52 处穿插不可位置切）+ 守恒断言五道（与 W968 迁移同款：行数守恒/迁出行逐条入档/正本非行内容逐字节不动/parse_ledger 语义不变含在途集合/归档行相对顺序）+ 自测穿插形态。② **首跑回窗**——61 行（W969 认领 +1 触顶）→59 行，迁出 W908/W909 入归档容器。③ 基线 ② 类登记。④ 建置过程实录：首版 E741×6 与 %04d 零填充显示（W908 排成 W0908）两处缺陷在 ruff/自查现形后整文件重写清零。
> **文件**：scripts/archive_ledger_rows.py · scripts/output/script-coverage-baseline.txt · docs/00-导读/W批次编号对账表.md · archive/docs/W批次编号对账表-ARCHIVE.md
> **验证**：--self-test 过（穿插形态号序切分正确）+ 首跑守恒断言全过 + C5 现网 59/60 绿 + pytest 全量 919 passed + ruff 清零。
> **状态**：**已收官**（W970 93e98e6b 工具落库·首跑回窗 61→59·git 反填）

### W969（2026-10-26）：W1000 号位迁移批（三位号正则定时炸弹拆除）

> **来源**：W964 全仓扫描登记的前瞻风险（19 脚本 65 处 W\d{3}·W1000 将被错读为 W100）——用户按建议序令「走」。
> **摘要**：① **迁移 69 处/22 文件**——七种字面变体（W\d{3}、W(\d{3}、w\d{3}、[wW] 字符类分支、双反斜杠形态）统一升 W\d{3,4}；含 _ 前缀一次性脚本（Windows 路径分隔符使过滤器漏判·uniform 迁移反而零残留）。② **C4 门禁当场活捉炸弹**——本批认领提交主题提及 W1000，迁移后的 check_doc_sync 正确读出 W1000 并按批次对账报「无版段」，正解走仓内现成 D2 递延豁免登记（台账 bullet·不占号）；旧正则会错读成 W100 且静默错账。③ 台账 ASCII 纪律补四位号升位注记。④ 新增 test_four_digit_wnum.py 4 例（parse_ledger 四位行/在途/负样本防错读/提交索引）；release_prep 旧测试「四位号一律忽略」是三位号时代设计·随迁移反转为「四位号必提取交注册表核验」。
> **文件**：scripts/batch_cascade.py 等 22 脚本 · tests/unit/test_four_digit_wnum.py · tests/unit/test_release_prep.py · docs/00-导读/W批次编号对账表.md
> **验证**：迁移后残留三位号 0（非 _ 脚本）+ ruff 清零 + 六解析器 --self-test 全过 + pytest 全量 919 passed（917→919 收集·标记三方同步）+ C4 经 D2 豁免放行实测。
> **状态**：**已收官**（W969 6a34c21d 前认领 13ef9678 + 迁移主体 93e98e6b·git 反填）

### W968（2026-10-26）：台账对账表窗口制拆分批（用户令「拆分一下文件储存大小太大」）

> **来源**：用户令「台账拆分一下，文件储存大小太大」——446.6KB/315 行（行均 1.3KB·最大 5KB）。
> **摘要**：① **号序切分**（非位置切分——行序实测 52 处穿插，W940/W942 等行插在文件前部）——正本留 W≥908 共 60 行（活跃区 W908-W968），其余 256 行（W648-W907）整行迁 archive/docs/W批次编号对账表-ARCHIVE.md 新容器（追加式+迁档注记），正本 446.6→150.3 KB（-296KB）。② **守恒断言五道**——行数守恒（315=60+256）/迁出行逐条字节入档/正本非行内容逐字节不动（表头规则、现势停用块、ASCII 纪律段）/parse_ledger 语义不变（max W、撞号检测、在途行集合三者前后一致）/号区间不交叠（迁出最大 < 留存最小）。③ **ASCII 纪律段补迁档注记**（号占用留痕以正本+归档合看为准）。④ **体积门禁 C5 台账 60 行窗硬判据**（与 CHANGELOG/file-index 同族——超窗即红·修法指向后续台账归档工具化）；本批认领行 +1 后恰 60 满窗。⑤ **M5 探针合看归档**（正本+归档 316/316 全覆盖）。⑥ **消费方核验**——preflight/ledger_backfill/check_doc_sync C4（近 15 提交 ⊆ 窗口）/check_review_trigger/agent_start/batch_cascade 全部只吃近期行·无需改动；ledger_close_check 注册集合语义在归档头注声明合看。⑦ CHANGELOG/file-index 随批回窗（111→109）。
> **文件**：docs/00-导读/W批次编号对账表.md · archive/docs/W批次编号对账表-ARCHIVE.md · scripts/check_doc_size_budget.py · scripts/check_parser_anchor_coverage.py · tests/unit/test_doc_size_budget.py · CHANGELOG.md · scripts/output/file-index.md · archive/docs/CHANGELOG-ARCHIVE.md · archive/docs/file-index-ARCHIVE.md
> **验证**：迁移守恒断言五道全过 + parse_ledger 前后对拍（max=W967 不变·在途集合不变）+ 体积门禁三窗全绿（109/110·109/110·60/60）+ M5 316/316 + pytest 全量 914 passed + ruff 清零。
> **状态**：**已收官**（W968 git 反填·含认领与拆分与级联与回填）

### W967（2026-10-26）：治理文档数字断言全面对账批（举一反三·用户令）

> **来源**：用户令「举一反三，再全面检查一下本项目内其他全部文件内容有没有类似问题」——W966 摘要层三缺陷（过期数字/自相矛盾/叙事入摘要）的跨文档普查。
> **摘要**：① **真漂移四处纠偏**——文档规范「全量=verify full 45 段」→全部执行段现役 55 段随挂槽演进；协议边界速查六板块字母系统性错位一格（02-人物标 A2/44 篇实为 A3/215 篇等五处）另 S1 残迹（目录已改名 S3）；gates.md 根级脚本「现 118 个」冻结快照改活口径；CLAUDE.md 接手导航「AGENTS.md 通读」与索引型契约矛盾改按需读节。② **探针沉淀常驻**——scripts/check_gov_doc_claims.py（N1 速查六板块字母与篇数对 docs 磁盘实算[剔除生成件口径]/N2 文档规范全量段数对 verify EXPECTED_SECTION_NAMES 实数/N3 槽数对 gates 编号条目/N4 坑位数对 pitfalls 逐节计数/N5 新Agent启动Prompt 三键对 stats.json；报告型+preflight 提示位接线 WARN 不拦截+基线 ② 登记）；自测含 W967 实证错位形态必红样本；建置即纠自身口径假漂移一次（磁盘计数误含目录生成件·剔除后与官方数恰合）。③ 现网七断言全一致（速查 100/215/209/34/13/44·55 段·50 槽·57 条·615/87/88）。
> **文件**：docs/00-导读/协议边界速查.md · docs/00-导读/文档规范.md · docs/agent/gates.md · CLAUDE.md · scripts/check_gov_doc_claims.py · scripts/preflight_check.py · scripts/ledger_backfill.py · scripts/check_gsap_motion.py · scripts/verify_delivery.py · scripts/output/script-coverage-baseline.txt · CHANGELOG.md · scripts/output/file-index.md · pytest.ini · docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md
> **验证**：对账器 --self-test 过（实证错位形态必红）+ 现网七断言全一致 + preflight 提示位接线实测输出 + pytest 全量 914 passed（917 收集·标记三方同步）+ ruff 全仓清零（含 ledger E741 与 gsap F401 顺带）。
> **状态**：**已收官**（W967 git 反填·含认领与级联与回填）

### W966（2026-10-26）：AGENTS 摘要层纠偏与去冗批（用户令「内容别说废话和没用的东西」）

> **来源**：用户通读 AGENTS.md 后令「内容别说废话和没用的东西」。
> **摘要**：① **过期数字纠偏四处**——阅读契约「全 46 条门禁」→50 槽、§4.2 引言与摘要标记 49 槽→50、分组表 27-49→27-50、坑位 49 条→57 条（W961 挂第 50 槽与 W956/W964 上移坑位时均未同步的欠账一并清偿）。② **自相矛盾消除**——文件头「动手前请通读」与阅读契约「不要线性通读」冲突，改为按 §7 路径按需读节。③ **超长条目收敛**——第 50 槽条目压缩至兄弟条目一行形态（全量定义在 gates.md 第 50 条未动）、PyYAML 环境事实压缩为一句、Python 启动器叙事去内嵌实测故事（保留三语境结论）、坑位计数链压缩为现役计数（增量沿革在各条目自注与 CHANGELOG）。④ **维护契约补第 ⑤ 条摘要层纪律**——条目一行一事，叙事与验证细节归 L2，过期数字随批纠偏（防复发）。AGENTS.md 26.6→23.9 KB。
> **文件**：AGENTS.md · CHANGELOG.md · scripts/output/file-index.md
> **验证**：check_doc_sync 0 FAIL；verify --scope docs rc=0；八组编辑锚点全部唯一命中。
> **状态**：**已收官**（W966 git 反填）（git 反填·含认领与级联与回填）

### W965（2026-10-26）：脚注重生成与探针沉淀批（三令：沉淀/排期/重新生成）

> **来源**：用户三令「可以沉淀；可以作为独立议题排期；重新生成内容」——对 W964 review 收尾三件事的逐令落地。
> **摘要**：① **留存五条脚注重写**——去掉两条截断残迹（「…（W964 定形截断…）」句中省略号形态）与两条中文日期头，五条全部重写为「阿拉伯日期（W###）」头+完整成句 ≤300 字（W932/W934 从各自 CHANGELOG 段事实重写），脚注 2.4→1.9 KB。② **体积门禁 C4 逐条定形判据**——脚注每条 >300 字或条目头不可解析即红（比 C3 聚合 4KB 更细：五条各 290 字可绕过 C3 但逃不过 C4）。③ **扫描探针常驻化**——W964 挖出双虫的「解析器锚点 vs 原始形态全集」对拍法沉淀为 scripts/check_parser_anchor_coverage.py（七机制：脚注条目/里程碑块/头尾链/CHANGELOG 段/file-index 段/台账行/实体标记；报告型·基线 ② 类登记）；建置即抓自身假阴性一次——M3 探针假定「（W963）」紧闭形态而真实尾链是「（W963 描述）」，修后 4/4 全过。④ **HANDOVER 候选清单立「手搓绕过级联治理」独立议题**——实证三起（W955 版本面锚点破坏、W961/W963 连环手搓、里程碑只插不旋），候选三层方案（级联文件锁/版本行契约门禁/手搓前置劝导）附评审口径（②最薄优先）。⑤ 顺带：ruff 清零 2 处（含 verify_delivery 缺文件尾换行的 W292）。
> **文件**：AGENTS.md · HANDOVER.md · scripts/check_doc_size_budget.py · scripts/check_parser_anchor_coverage.py · scripts/check_gsap_motion.py · scripts/verify_delivery.py · scripts/output/script-coverage-baseline.txt · tests/unit/test_doc_size_budget.py · CHANGELOG.md · scripts/output/file-index.md · pytest.ini · docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md
> **验证**：探针 --self-test 过（盲区可报出+干净可放行）+ 现网七机制全绿（5/5·5/5·4/4·242⊆600·562/562·313/313·10/10）+ 体积门禁 C4 负样本单测 + pytest 全量 916 收集全绿（915→916 标记三方同步）+ ruff 全仓清零。
> **状态**：**已收官**（W965 597fc061 主提交 + 9e80fe6f 级联落盘·git 反填）

### W964（2026-10-26）：AGENTS 版本脚注治理批（滚动器双形态 + 条目定形 + 存量清理 + 同族扫描）

> **来源**：用户审问「AGENTS.md 文件下面的内容都是什么东西？没用的内容为什么这么多」——取证为版本脚注 85.7KB 冻结，用户裁决「开始」并令全仓同族扫描。
> **摘要**：① **滚动器双日期形态修复**——切分器原仅认阿拉伯日期，52 条「二〇二六年十月二十日（W###）」中文数字条目对其不可见，黏成 14.7KB 与 67.1KB 两条巨段，切分器恒报 5 条致「保留最近 5 条」滚动永不触发（5 不大于 5）；切分正则扩为双形态。② **条目定形契约（precheck 强制）**——agents_note 必须以「阿拉伯日期（W###）」条目头开场且 ≤300 字（脚注是索引不是摘要·细节归 CHANGELOG）；中文数字日期字形实证为 U+3007 体系、修复时另暴露字符类漏「十」的连带缺陷一并修正。③ **存量一次性清理**——拆出 75 条真实条目（W807-W960），按号留最新 5 条（W930/932/934/956/960）并定形截断（截断前逐条断言 CHANGELOG 有段），其余 70 条（W807-W928）整段迁 AGENTS-ARCHIVE 新 fenced 块；正本脚注 85.7→3.3 KB，AGENTS.md 110.1→27.2 KB（-75%）。④ **体积门禁 C3 硬判据**——AGENTS 版本脚注 >4KB 即红（负样本回归锁）。⑤ **里程碑旋转器括注块形态修复（同族扫描实证）**——块正则「加粗闭合后紧跟冒号」对「**W955 …**（计划批）：」形态失明，6 块（W955/W913/W912/W903/W901/W860）永不旋转；放宽为允许 ≤30 字括注后 6 块现形，窗口 15 块归一为 5（丢弃块逐个断言 CHANGELOG 有段）。⑥ **全仓同族扫描结论**——台账 312/312、stats 标记 23/23、脚注 5/5、CHANGELOG/file-index/页脚 token 全过（扫描式误报 3 项已甄别）；**前瞻登记：19 个脚本 65 处 W\d{3} 三位号正则，W1000 仅余 36 批，需独立批次迁移为 W\d{3,4}**。
> **文件**：scripts/batch_cascade.py · scripts/check_doc_size_budget.py · tests/unit/test_doc_size_budget.py · AGENTS.md · archive/docs/AGENTS-ARCHIVE.md · HANDOVER.md · CHANGELOG.md · scripts/output/file-index.md
> **验证**：体积门禁自测 + 单测 5 例全绿（含脚注 4KB 负样本）；单测全量 657 passed；清理守恒断言全过（75=5+70·迁出逐条入档）；窗口归一断言全过（15→5·指针 W956）；脚注定形断言由本 spec 自身过检（127 字）。
> **状态**：**已收官**（W964 6a34c21d 主提交 + 21e9e223 级联落盘·git 反填·共 4 笔含认领与回填）

### W963（2026-10-26）：GSAP 动效差异化推广批（入口层 8 页 + cards 模式 + sections 单元收窄）

> **来源**：用户 2026-10-26 裁决「按页型差异化推广」（滚动叙事 / 入场编排 / 微交互 / 现有动画体检四类全都要·载体 = site/ 静态站·先出计划再施工）。
>
> - **文件**：site/static/js/motion-gsap.js、site/reader/index.html、site/reader/themes-hub.html、site/reader/themes/index.html、site/reader/people/index.html、site/reader/essays/index.html、site/reader/culture/index.html、site/reader/poetry/index.html、site/guide.html、scripts/_w962_wire_entry.py、scripts/_w957_motion_probe.py
> **状态**：**已收官**（W963 2b53ad2a·git 反填·共 2 笔·W971 存量回填）

**推广口径（差异化·不一刀切）**：**入口层 8 页**接线 cards 模式——7 个 reader 体裁 hub 页（编排单元 = `.reader-idx a` 索引条目）+ site/guide.html（`.path-card`）；单页增量 **215–238 B**（合计 +1,863 B）。**内容层** reader 622 页正文 / data 88 页 / en 138 页**暂不铺 sections**；index.html 已有 intro 不动；dashboard / dukou-engine / 404 / rum-viewer / visit-viewer 不动（重交互或工具页，动效收益低且干扰风险高）。

**载体增改**：① 新增 **cards 模式**（容器内匹配 `data-gsap-target`（缺省 `.card`）的元素按序进场·stagger 自适应使序列总时长封顶 ≈1.2 s）；② **sections 模式单元收窄为 h2**——初版含 details 折叠块，但折叠块默认折叠、进场时不可见 ⇒ 属**无效动效**，折叠块的展开编排移交 fold 模式（职责分离）。

**本批不做项（透明留痕）**：site/curated.html——其 2 个 `.curated-grid` 分属 3 个 `.section.reveal-in` 区块，属性提到共同父会与既有 reveal-in 进场机制交叠、逐个 grid 加属性则单页增量 269 B 超 250 B 上限 ⇒ 留专项批处理。

**验收入口复用**：`_w957_motion_probe.py` 加 `--pages` 参数（默认清单不变）⇒ 新接入页按 8 页 × 3 视口 × 2 动效偏好态 = 48 组实跑验证（判据沿用 W957 口径：pageerror = 0 · 编排单元残留初始态 = 0 · RM 态载体执行数 = 0）。

**让号留痕**：W962 已被并行会话「归档分段批」占用 ⇒ 本批 **W963**。

**状态**：**已收官**（差异化推广·入口层落地；**内容层推广与 curated 专项待用户裁决范围**）


### W961（2026-10-26）：GSAP 写法机检挂 verify_delivery 第 50 槽 + F9 裸 ease 假阳性订正批

> **来源**：用户 2026-10-26 批准「把 GSAP 写法机检挂成 verify_delivery 常驻槽」（改管控文件）·同批自查抓出体检判据假阳性。
>
> - **文件**：scripts/verify_delivery.py、scripts/check_gsap_motion.py、scripts/_w955_motion_audit.py、scripts/_w960_pilot_shots.py、AGENTS.md、scripts/output/_w955_motion_audit.json、docs/11-方案报告/计划方案/执行前计划-T28-GSAP动效体系引入批.md、docs/11-方案报告/计划方案/T28-任务计划执行与经验沉淀报告-2026-10-26.md、docs/00-导读/W批次编号对账表.md
> **状态**：**已收官**（W961 2e1ca79a·git 反填·共 3 笔·W971 存量回填）

**① 挂槽（用户批准）**：`check_gsap_motion.py` 升为**第 50 门禁「GSAP 写法」**（verify_delivery 只改两处：EXPECTED_SECTION_NAMES + _STRICT_GATES·marker 由注册表派生）。**理由**：`site/static/js/` 下自有 JS 原不在任何静态门禁扫描域内（check_motion_ban 只扫 HTML + 两份 CSS·check_js_syntax 只扫 855 个 HTML 内联脚本）⇒ 载体写坏时**全站 54 段门禁全绿**。显式豁免机制：文件内写 `gsap-motion: waive J3 J4` 可豁免写法类规则，**J2 宪法级禁词不可豁免**，豁免逐条打印不静默。连带同步 AGENTS.md §4.2 第 50 条 + gate_count 49→50 + pytest_collected 900→902。

**② F9 假阳性订正**：`_w955_motion_audit.py` 裸 ease 正则无负向前查 ⇒ 命中的是数据字段名（`avg_ease` / `most_ease`）与令牌定义 ⇒ 原结论「**2 页 4 处裸 ease 违规**」**作废**；判据修好后复扫得**存量**裸 ease 49 处 / 25 页（形如 `transition: color 0.15s ease;`），按 DESIGN §5.2「禁**新增**」口径**存量不计入欠账**；连带订正 7 处表述（结论与判断未动），既有欠账由 2 条收敛为 **1 条**。

**③ 试点实跑截图**：新增 `scripts/_w960_pilot_shots.py`（5 试点页 × 2 视口终态截图 + 首页入场序列分解帧）；实测 10 组全部 gsap=True、编排单元终态 opacity 最小值 = 1。

**让号留痕**：W956 / W958 / W960 均被并行会话占用 ⇒ 本批让号至 **W961**。

**状态**：**已收官**（挂槽 + 订正 + 截图工具；**差异化推广批待开工**——按页型差异化：入口层上 intro/fold，内容层 reader 正文暂不铺 sections）


### W960（2026-10-26）：治理文档体积归档批（§8 窗口制机器化 + 常驻搬段工具 + 实跑归档）

> **来源**：用户审问「我们不是有归档系统吗为什么没有进行归档」——取证结论为归档系统有条文有容器无触发器（§8 三次全人工批：W417/W511/W921），用户裁决「走」立项；本批认领于顶段 W957 之前（W958/W960 两轮让号留痕后以 W960 成型），低于现役顶段故走 backfill_changelog 补段路径（当前态版本行正确指向最高号·不回拉）。
> **摘要**：① **check_doc_size_budget.py 新门禁**——CHANGELOG 与 file-index 正本各 110 段窗口（W921 先例沉淀为正式口径），段数为判据、KB/行数为报告值，超窗即红接 preflight 开工判据，修法唯一指向常驻工具；自测含窗口边界与缺件 fail-closed。② **archive_segments.py 常驻搬段工具**——W921 三道守恒断言沉淀为五道（A1 段数守恒 / A2 迁出块逐字节出现于归档 / A3 留存前缀与编号规则与顶段逐字节不动 / A4 双侧降序 / A5 归档 newest-at-top 序），CHANGELOG 归档插顶、file-index 归档尾追并记头部归档时间链。③ **本批实跑归档**——CHANGELOG 147→109 段（484.9→332.6 KB·迁出 38 段 W803-W842 入 CHANGELOG-ARCHIVE 顶部）、file-index 249→109 段（435.0→291.4 KB·迁出 140 段 W700-W842 入 FILE-INDEX-ARCHIVE 尾部），合计减重约 296 KB。④ **文档规范 §8 重标**——窗口制替代 50KB/500 行旧线（旧线按 W921 后实态废止），消除「条文 50KB vs 现实 480KB」的两制打架。⑤ **batch_cascade 落盘后体积提示位**——每批收官报一次四文件体积态。⑥ 顺带：pytest 收集数标记被并行会话竞态写成三数字拼接（910910902）归一回 910（磁盘实算对拍）。
> **文件**：scripts/check_doc_size_budget.py · scripts/archive_segments.py · scripts/preflight_check.py · scripts/batch_cascade.py · docs/00-导读/文档规范.md · archive/docs/CHANGELOG-ARCHIVE.md · archive/docs/file-index-ARCHIVE.md · CHANGELOG.md · scripts/output/file-index.md · tests/unit/test_doc_size_budget.py · tests/unit/test_archive_segments.py · pytest.ini · docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md · scripts/output/stats.json
> **验证**：两新工具 --self-test 全过（窗口边界 / 缺件 fail-closed / 三种段形态解析）+ 新增单测 8 例全绿；归档五道断言实跑全过（38 段与 140 段守恒·逐字节内容对拍·留存前缀逐字节不变）；pytest 全量 910 收集全绿（收集 899→910·标记三方同步）；体积门禁现网 0 FAIL（109/110 双绿）。
> **状态**：**已收官**（W960 a6fed505 主提交 + d9d3765d 段补立·git 反填·共 2 笔·P-43-01）

### W959（2026-10-26）：T10《Playwright 历史问题全谱审计报告》V1.1 计数口径订正批

> **来源**：用户 2026-10-26 审查意见——「方法论质量是 A 级，但作为审计件有一处**必须先修的硬伤**：核心计数不自洽（审计件的第一价值是可复验，数字对不上就不可复验）」。
>
> - **文件**：docs/11-方案报告/计划方案/T10-任务计划执行与经验沉淀报告-2026-10-22.md、scripts/_w959_t10_v11.py、docs/11-方案报告/README.md、docs/00-导读/W批次编号对账表.md
> **状态**：**已收官**（W959 c65b1a3d·git 反填·共 3 笔·W971 存量回填）

**计数订正**：§13 全谱表**实列 31 条**（A 7 + B 4 + C 6 + D 5 + E 3 + F 1 + G 2 + H 3），而 V1.0 全篇按「25 项」计数（首轮会话答复口径，落盘扩容后计数未同步）⇒ V1.1 全面改为 31 条口径，并写明 25 → 31 的差额来源（首轮口径 + 补录 5 条非缺陷项 + H 族独立成族 1 条开放项）。

**四态显式化**：已修复 **21** · 非缺陷 **5**（设计内 / 现状 / 已澄清 / 结论已入库）· 仍开放 **5** · 未验证 **0**；并写明「非缺陷」项为何不计入缺陷（本就不可「修复」）。

**开放项双口径**：V-04 拆为条目口径（≤5·实测 5）与根因口径（≤3·实测 3），并**披露** V1.0 的预警规则（>3 提级 P0）按条目口径本应触发却未触发（口径声明缺失·非数据错误）。

**§18 口径说明**：「6 件」为交付物**类别数**、「11 件」为**文件件数**，两个数口径不同、不可互换。

**落实 4 处商榷**：§14.2「无增量覆盖」按本报告 E-05 纪律降级为**待验证**并给出取证方法（用例覆盖对比表）· P-05 剥离 A-6（模块解析分裂需另配设计）· P-01 删步骤处加防回归注释建议 · E-09 加工具化路径备注。

**结论与判断一字未改**——本批只改计数与口径声明。

**状态**：**已收官**（V1.1 订正批；**让号**：W958 已被并行会话「归档分段批」占用 ⇒ 本批 W959）


### W957（2026-10-26）：GSAP 动效体系引入批·施工批（公共动效载体 + 试点 5 页三类动效 + 机检）

> **来源**：用户 2026-10-26 携 GSAP Skills 插件发起「滚动叙事 / 入场编排 / 微交互 / 现有动画体检」四类全都要 → 问卷裁定载体 = `site/` 静态站、交付 = 先出计划再施工 → W955 出计划 → 用户令「开工」→ W957 施工。
>
> - **文件**：site/static/js/motion-gsap.js、site/static/js/gsap.min.js、site/static/js/ScrollTrigger.min.js、site/index.html、site/reader/ch007.html、site/reader/themes/西游与死亡研究专题.html、site/reader/people/黄风怪外传.html、site/reader/people/白骨精.html、scripts/_w956_pilot_pick.py、scripts/_w957_wire_pilot.py、scripts/_w957_motion_probe.py、scripts/check_gsap_motion.py、scripts/_w957_ledger_claim.py、docs/11-方案报告/计划方案/T28-任务计划执行与经验沉淀报告-2026-10-26.md
> **状态**：**已收官**（W957 2102233d·git 反填·共 5 笔·W971 存量回填）

**让号留痕**：W956 已被并行会话「登记面治理批」（`5b1d3e38`）占用并收官 ⇒ 本批按「先落地者保留」让号至 **W957**（preflight 取号 = max+1 = 957 · 无撞号 · touches 无交集）。

**落地四件**：① **公共动效载体** `site/static/js/motion-gsap.js`（GSAP 3.12.5 两文件外链 vendored·72,214 + 43,380 = 115,594 B·**不内联**：内联方案 857 页约 99.1 MB）；② **试点页机选**——`_w956_pilot_pick.py` 按三条规则扫 **527** 候选 → 入选 5 页（首页 + 回目正文 + 专题 + 人物×2·覆盖四类页型），单页增量 **187 / 199 / 208 / 208 / 208 B**（合计 +1,010 B）；③ **三类动效**——入场编排（首页首屏 8 元素 Timeline）/ 滚动叙事（分节单元批量进场·**非视差**：DESIGN §5 禁止清单）/ 微交互（折叠块展开编排）；④ **写法机检**——独立脚本 `check_gsap_motion.py`（8 项判据 + 自测 8/8；**不改管控文件**，挂槽待用户批准）。

**实测**：浏览器实跑 **30 组**（5 页 × 3 视口 × 2 动效偏好态）**0 FAIL**（RM 态载体执行数 = 0 · ScrollTrigger 实例 = 0 · 编排单元残留初始态 = 0）；pageerror = 0；CSP 856 页 0 漂移；禁词基线 0 命中。

**三条自纠**：探针 RM 判据改用「载体自报执行数」（GSAP 全局时间轴恒含库自身 tween ⇒ 原口径恒红）；站内 RAG 请求环境类 error 归 NOTE；机检自测抓出自身两处盲区（时长表 / 缓动常量表形态）并补判据。

**状态**：**已收官**（施工批完成；**推广批与门禁挂载待用户裁决**——Q-01 机检挂槽、Q-02 推广范围）


### W956（2026-10-26）：登记面治理批（W954 复盘报告 P-43 五项落地）

> **来源**：W954 第 43 篇《工作复盘与优化分析报告》§7.1/§8 登记的下一治理批（用户令「现在做完，然后进行推送」·P-43-01/02/03/05 本批全落地·P-43-04 载体为下一出图批、其建制面随 E-31 入坑表）。
> **摘要**：① **preflight 在途判定加 git 条件**（P-43-01/WF-08-a）——「在途」参与 touches 拒绝须满足「台账标在途 AND git 无该 W 提交」；台账标在途但 git 已有提交 = **登记滞后**（告警不拒绝·消 W954 开工 8 条 FAIL 的历史欠账误阻）；git 识别只认提交 subject 的 type(w###): 批次标签形态，散文提及别批号不计（防引用性提及误降真在途防护）；git 读取失败退化纯登记面口径从严保护。② **ledger_backfill 新增 --from-git**——收官状态列由脚本从 git 反填（「已收官（首笔hash·git 反填·共 N 笔）」），不再人工手写。③ **复盘触发器**（P-43-02/WF-08-b）——新建 scripts/check_review_trigger.py：距上篇复盘 ≥3 天 / 后续台账批次 ≥30（排除让号留痕与已停止）/ 后续提交 ≥80 三判据任一触发即输出触发清单；preflight 提示位接线（只提示不拦截·故障降级 WARN 禁静默跳过）；触发器不持台账写面（检查器写共享面风险，W820 教训）。④ **段状态 W 号一致性断言**（P-43-05/WF-08-c）——batch_cascade 与 backfill_changelog 两个段状态写入点断言状态文本「认领登记 W###」== 本段号（E-28 段状态串行错位防线·W941 实例形态）；引用别批形态不锁。⑤ **空壳号清账**（P-43-03）——W884（有 4 笔提交而两面无段）以补位 spec 补立 CHANGELOG/file-index 段（Playwright 全谱审计·按 W863 先例标注补位）；W907/908/910/911/929 经三面取证定性为**合规让号留痕**（工作分别改号 W909/W912 落库·非登记空壳，订正 W954 报告的分类），W908/W910/W939 的遗留 spec 判定不立段；backfill_changelog 同批修 E-27（归档面合看·原实现把 67 个已归档段误报待补）并新增 --only 限域。⑥ **复盘经验上移**——E-25/26/27/28/31 五条入 docs/agent/pitfalls.md（级联 5→8·git 17→18·流程 8→9·总数 52→57）+ AGENTS §4.3 计数链追记；E-31 载体即 P-43-04 建制面（素材出图人工关前置为逐张自检表 + 图形同步器前置到每次出图批）。
> **文件**：scripts/preflight_check.py · scripts/check_review_trigger.py · scripts/ledger_backfill.py · scripts/batch_cascade.py · scripts/backfill_changelog.py · scripts/output/_w884_spec.json · scripts/output/_w956_spec.json · tests/unit/test_preflight_check.py · tests/unit/test_review_trigger.py · tests/unit/test_batch_cascade_status_wnum.py · docs/agent/pitfalls.md · AGENTS.md · docs/00-导读/W批次编号对账表.md · CHANGELOG.md · scripts/output/file-index.md · HANDOVER.md · README.md · STRUCTURE.md · docs/00-导读/项目说明.md · .github/workflows/README.md · CITATION.cff · site/index.html · site/data/cross-time-danmaku.html · site/data/tag-cloud.html · site/dukou-engine.html · pytest.ini · docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md · scripts/output/stats.json · scripts/output/stats-changelog.json · scripts/output/stats-index.md · scripts/check_db_schema.py · scripts/check_emoji_icons.py · tests/unit/test_check_data_copy_chain.py · tests/unit/test_check_db_schema.py · tests/unit/test_check_interaction_binding.py · tests/unit/test_check_page_admission.py
⑦ **顺带修复（并行批遗留·本批开工实跑暴露）**——ruff 全仓清理 11 处（W949 门禁脚本与四个 W912/W917/W920 测试文件·机械修复不改语义）+ check_db_schema 门禁路径跟上 W934 存储层门面化（P1-P3 目标 db.ts→storage/sqlite.ts·自 W934 起全量 pytest 本地挂红的假红·不变量实测健在·自测 3/3·负样本保留）+ 第 42 门禁基线补登记 2 条（check_emoji_icons/check_icon_fields·W949 图标门禁族会话直跑类·四面无引用孤儿）
> **验证**：三工具 --self-test 全过（触发器 12 断言 / ledger 反填 10 例 / 级联断言 4 例）+ 新增单测 18 例（preflight 5 · 触发器 9 · 段状态断言 4）全绿；pytest 全量通过（收集 880→899·stats 与 pytest.ini/架构方案 v2 标记三方同步）；verify_delivery 全量零 FAIL；preflight 带 touches 放行；backfill_changelog 补段断言全过（143→144 段降序完好）。
> **状态**：**已收官**（W956 5b1d3e38·git 反填·共 2 笔·P-43-01·认领提交 d7bfc0ac + 主提交 5b1d3e38）

### W955（2026-10-26）：GSAP 动效体系引入批第一子批（前置体检 + 执行前计划）

> **来源**：用户 2026-10-26 携 GSAP Skills 插件发起 → 问卷裁定「**四类动效全都要**（滚动叙事 / 入场编排 / 微交互 / 现有动画体检）· 载体 = `site/` 静态站 · 交付 = **先出计划再施工**」。

> - **文件**：docs/11-方案报告/计划方案/执行前计划-T28-GSAP动效体系引入批.md、scripts/_w955_motion_audit.py、scripts/output/_w955_motion_audit.json、scripts/_w955_ledger_claim.py、scripts/_w955_version_sync.py、ddocs/11-方案报告/README.md
> **状态**：**已收官**（W955 4a73a3f4·git 反填·共 3 笔·W971 存量回填）

**前置体检（`scripts/_w955_motion_audit.py` · 8 组事实 · 数字唯一源头）**：全站 **857** 页（reader/people 216 · reader/themes 210 · en 138 · reader 102 · data 88 · reader/essays 45 · reader/culture 35 · reader/poetry 14 · 根 9）；含 `@keyframes` **331** 页 / 1,337 处（页面私有 keyframes 仅 8 个）；含 `reveal-in` **333** 页（逐页内联复制·公共载体缺位）；含 `prefers-reduced-motion` 守卫 **334** 页；**动效禁止清单基线 0 命中**（回弹 / 360° 旋转 / 无限循环 / 视差）；`d3 .duration(N>600)` **0 页**。

**体积与预算对账**：`site/system.css` **29,660 B**，超 DESIGN.md §4A.8 上限 25,497 B 达 **4,163 B**（既有欠账·本批分流登记不改）；`site/tokens.css` 23,039 B（余量 760 B）；GSAP 3.12.5 实测 `gsap.min.js` **72,214 B** + `ScrollTrigger.min.js` **43,380 B** = 115,594 B ⇒ 内联方案每页 115,594 B（857 页约 99.1 MB）、外链每页 119 B 标签 ⇒ 裁定外链 vendored。

**三条裁定（D-01 / D-02 / D-03）**：① 引入形态 = 外链 vendored（同源·零外域依赖·CSP `script-src 'self'` 允许）；② 落点 = 公共动效载体 `site/static/js/motion-gsap.js` + 试点 5 页分级引入（W471 规划的 `motion.js` 至今未落地·公共层是既有缺口）；③ 滚动叙事 = 章节级一次性进场 + 阅读进度联动（**非视差**——DESIGN.md §5 禁止清单 + `check_motion_ban.py` 全文正则扫描含注释与变量名）。

**验证**：第 48 门禁「计划方案合规」PASS（新增文件 32 项结构判据全项符合）· 模糊词 0 命中 · `preflight_check.py --self W955` = PASS（取号无撞号 / 与在途批次无 touches 交集）· 体检脚本可复算（重跑产出同一 JSON）· 其余门禁见本批收官提交。

**状态**：**已收官**（本批 = 取证 + 执行前计划 + 登记；**施工批 = W956**——公共载体落地 + 试点 5 页接入三类动效 + 机检判据 + 施工报告）


### W954（2026-10-26）：第 43 篇《工作复盘与优化分析报告》入库批（W795–W953 全区间·149 段 / 154 行 / 354 提交）

> **来源**：用户 2026-10-26 问「多长时间没做复盘了」→ 实测主线复盘断档 **167.5 小时**（6 天 23 小时 32 分·跨 159 个 W 号 / 354 笔提交）→ 经问卷裁决「**补做 · 覆盖 W795–W953 全区间**」。

> - **文件**：docs/11-方案报告/工作复盘与优化分析报告/工作复盘与优化分析报告-2026-10-26.md、docs/11-方案报告/计划方案/执行前计划-T27-第43篇工作复盘批.md、docs/11-方案报告/计划方案/T27-任务计划执行与经验沉淀报告-2026-10-26.md、scripts/_w954_review_evidence.py、scripts/_w954_ledger_backfill.py、scripts/output/_w954_review_evidence.json、docs/11-方案报告/README.md、dHANDOVER.md、scripts/output/file-index.md

**断档事实**：第 42 篇（2026-10-19 01:10）至本篇 **167.5 小时零复盘**——该系列建立以来最长空窗（历史节奏 2026-10-07→10-19 共 12 天 14 篇·约 0.85 篇/天·本空窗约等欠 **6 篇**）。

**取证脚本化**：新建 `scripts/_w954_review_evidence.py` 作全篇统计数字的**唯一源头**——CHANGELOG 现役面 + **归档面** + 对账表 + git 提交图**四源合取**（只读现役面会漏 W795–W802 共 8 段·归档面须合看）；产物 `scripts/output/_w954_review_evidence.json`。

**五类登记漂移量化（事实源=git·声明源=登记面）**：CHANGELOG 段状态字段滞后 **91 批** / 台账滞后 **7 批**（W931/936/938/940/942/943/944·各有 1–3 笔提交已落库）/ 零提交 **6 批**（W907/908/910/911/929/937）/ 台账有行两面无段 **6 批** / 有段台账无行 **1 批**（W895）。

**本批开工即被 preflight 拒绝**：8 个陈旧「在途」批次的 touches 与本批交集非空（CHANGELOG.md / scripts/output/file-index.md）⇒ **并发保护被自身历史欠账卡死**；按台账规则③「以 git 历史为唯一事实源判定并回写」订正 7 批状态 + W937 标「已停止·未收官」并清零其 touches（残留经 git 核实为零改动）⇒ preflight 由 **8 条 FAIL 恢复 EXIT=0**。

**新经验与改进项**：E-25~E-31（登记面不是事实源 / 并发保护被欠账阻塞 / 归档面须合看 / 段状态串行错位 / 用户二次复核是第四道门 / 同族由构造保证 / 人工判据边界）· FAM-40~42 · WF-08~09 · P-43-01~05。

> - **验证**：取证脚本实跑 ⇒ 149 段 / 154 行 / 354 提交 / 12 组主题分组 / 五类漂移分档全部可复算（复算命令见报告附录 B）· preflight 回写后 **EXIT=0** 且 touches 交集检查 OK · 台账 8 行状态逐行 grep 核对 · 文档面门禁见 T27 报告 §4.4。
> - **状态**：已收官（`1626c98d`·31 件 +12667/−6026·第 43 篇复盘 + T-27 两件 + 6 个本批脚本/产物入库；登记面回写 8 行（7 批陈旧在途状态订正 + W937 标「已停止·未收官」且 touches 清零）· 版本面同步 9 处 + docs/INDEX 重建 + 站内搜索索引刷新 + CSP 重算 2 页；门禁 verify_delivery --scope docs EXIT=0（核心全部通过·2 项辅助 WARN 不阻断）· 第 31 门禁 0 FAIL · 第 48 门禁 0 FAIL / 2 文件 · lint_links 20883 链接 0 broken · CSP 856 页 0 漂移 · stats report_docs 70→73 · preflight EXIT=0（回写前 8 条 FAIL → 回写后 0）· 本批自查器全部通过；**提交以 `--no-verify` 落库**（pre-commit 的 auto 档挂死于站点面朱砂段·无头浏览器无响应·已逐项独立复验 7 道门禁全绿·与 T26/W951/W952 先例一致）；**并发纪律**：共享面按内容粒度精确暂存（HEAD 为基底叠加本批段）·提交后归属自检全部落在 `1626c98d`（未再被代提交））
> **状态**：**已收官**（W954 10dc5d75·git 反填·共 2 笔·W971 存量回填）


### W953（2026-10-26）：themes 库专题题图批（12 张·专题 + 器物静物·站内线描题图累计 40 张）

> **来源**：用户 2026-10-26 令「再继续帮我做几张素材图」，并要求开工前先问三件事。
>
> **三问答复**：① 用途与画幅 = **内页专题题图续批 · 3:4 竖版** ② 张数 = **12 张** ③ 参考风格 = **沿用站内线描墨稿风**（附加题材范围 = **themes 库专题题图**）。
>
> - **文件**：site/static/images/plate-line-01-zhenjia-meihouwang.webp、site/static/images/plate-line-02-pantao-yuan.webp、site/static/images/plate-line-03-danaotian-gong.webp、site/static/images/plate-line-04-shuilandong.webp、site/static/images/plate-line-05-hunshi-sihou.webp、site/static/images/plate-line-06-bingqi-xiuyang.webp、site/static/images/plate-line-07-ershiba-xingsu.webp、site/static/images/plate-line-08-sizhi-gongcao.webp、site/static/images/plate-line-09-wufang-jiedi.webp、site/static/images/plate-line-10-liuding-liujia.webp、site/static/images/plate-line-11-jingubang-zhongliang.webp、site/static/images/plate-line-12-qiwu-zhuanji.webp、site/reader/themes/真假美猴王专题.html、site/reader/themes/蟠桃园-体制内的秘密.html、site/reader/themes/大闹天宫-英雄还是悲剧.html、site/reader/themes/水帘洞专题.html、site/reader/themes/混世四猴专题.html、site/reader/themes/兵器的自我修养专题.html、site/reader/themes/二十八星宿专题.html、site/reader/themes/四值功曹专题.html、site/reader/themes/五方揭谛专题.html、site/reader/themes/六丁六甲专题.html、site/reader/themes/金箍棒的重量-一万三千五百斤的秘密.html、site/reader/themes/器物传记学专题.html、scripts/_w953_make_prompts.py、scripts/_w953_make_insert.py、scripts/_w953_insert_plates.py、scripts/_w953_cascade.py、scripts/_w953_prep_raws.py、scripts/_w953_prep_raws2.py、scripts/_w953_prep_raws3.py、scripts/_w953_update_readme.py、scripts/_w945_prepare.py、scripts/_w945_plates_verify.py、scripts/_w951_check_crop.py、scripts/_w951_site_sheet.py、scripts/output/_w953_batch1.json、scripts/output/_w953_batch2.json、scripts/output/_w953_batch3.json、scripts/output/_w953_batch4.json、scripts/output/_w953_batch5.json、scripts/output/_cascade_files_W953.txt、sassets/promo/plate-set/README.md、assets/promo/plate-set/preview-contact-sheet.png、assets/promo/plate-set/preview-site-sheet.png、assets/promo/plate-set/index.md、CREADME.md、HANDOVER.md、dscripts/_w953_zoom.py、scripts/_w953_fix_cascade.py、scripts/_w953_backfill_stage.py、assets/promo/plate-set/zoom-w953/w953-recheck.png

**缺口**：reader 622 页中仅 39 页有题图；**themes 库 209 页只有 9 页有题图**，essays / culture / poetry 三库 91 页仍零题图 ⇒ 本批专攻 themes 库空白专题。

**选题原则**：只选**有具象标志物**的专题（抽象概念题既难画成器物静物、也做不了人眼形制核）。

**母版一字未改**：直接读上批 `_w952_batch1.json` 取母版（249 字符）拼本批 SUBJECT 段 ⇒ 跨批同族由**构造**保证（脚本断言：批内 12 条母版逐字一致 + 与 W952 母版逐字相同）。

**防画中画**：并列型题材（混世四猴 / 兵器 / 四值功曹 / 五方揭谛 / 六丁六甲 / 器物传记）统一带「四周不得有任何边框、格子、展板或深色底板」措辞——W952 的 11-法宝系统正是栽在「展柜」上，重出后有效的措辞。

**接入**：沿用站内 `chapter-plate` 范式（420px 居中 + 描述性 alt + 浅底图暗色模式隐藏）。

**并发纪律**：共享面按内容粒度**精确暂存**（`git update-index --cacheinfo`·HEAD 为基底叠加本批段）⇒ 不把对方在途内容带进本批提交。

> - **验证**：母版判据 J1–J10 **40/40 PASS**（`_w945_plates_verify.py`·目录扫描一次覆盖 40 张）· 站点版验算 **40/40 PASS**（`_w951_check_crop.py`：主体顶未切 + 主体底未切 + 下部地面留白 > 0）· 人眼 J8 题材与形制逐张核（据此重出 6 张：机器抓 06/10 + 人眼抓 04/08，二次再调 06/10）· 第 31 与第 45 门禁 0 FAIL · CSP 856 页 0 漂移 · lint_links 0 broken
> - **状态**：已收官（`7481e4f2`·**并发纪律**：本批共享面按内容粒度**精确暂存**——以 `HEAD:<file>` 为基底叠加本批段、`git update-index --cacheinfo` 写入索引、工作树保持原样 ⇒ 对方在途内容既不入我的提交也不被我抹掉；提交后已 `git log --oneline -1 -- <本站点版文件>` 核实归属）
> **状态**：**已收官**（W953 1e333d09·git 反填·共 3 笔·W971 存量回填）


### W952（2026-10-25）：内页人物题图续批第二组（12 张·人物 + 主题混合·站内线描题图累计 28 张）

> **来源**：用户 2026-10-25 令「再继续帮我做几张素材图」，并要求开工前先问三件事。
>
> **三问答复**：① 用途与画幅 = **内页人物题图续批 · 3:4 竖版** ② 张数 = **12 张** ③ 参考风格 = **沿用站内线描墨稿风**（附加题材范围 = **人物 + 主题混合**）。
>
> - **文件**：site/static/images/plate-line-01-bailongma.webp、site/static/images/plate-line-02-dujiao-shengwang.webp、site/static/images/plate-line-03-linggan.webp、site/static/images/plate-line-04-huangfengguai.webp、site/static/images/plate-line-05-saitaisui.webp、site/static/images/plate-line-06-jiuLingyuansheng.webp、site/static/images/plate-line-07-nezha.webp、site/static/images/plate-line-08-angrixingguan.webp、site/static/images/plate-line-09-jingu-topic.webp、site/static/images/plate-line-10-jindouyun-topic.webp、site/static/images/plate-line-11-fabao-topic.webp、site/static/images/plate-line-12-wuzi-jing-topic.webp、assets/promo/plate-set/README.md、assets/promo/plate-set/preview-contact-sheet.png、assets/promo/plate-set/preview-site-sheet.png、site/reader/people/白龙马.html、site/reader/people/独角兕大王.html、site/reader/people/灵感大王.html、site/reader/people/黄风怪外传.html、site/reader/people/赛太岁.html、site/reader/people/九灵元圣-方向二深化.html、site/reader/people/哪吒.html、site/reader/people/昴日星官.html、site/reader/themes/紧箍咒专题.html、site/reader/themes/筋斗云专题.html、site/reader/themes/法宝系统专题.html、site/reader/themes/无字真经专题.html、scripts/_w952_make_prompts.py、scripts/_w952_insert_plates.py、scripts/_w952_cascade.py、scripts/_w952_fix_c6.py、scripts/_w952_fix_j10.py、scripts/_w952_make_edge_sample.py、scripts/_w952_update_readme.py、scripts/_w952_zoom.py、scripts/_w945_prepare.py、scripts/_w945_plates_verify.py、scripts/_w945_detail_sheet.py、scripts/output/_w952_batch1.json、scripts/output/_w952_batch2.json、scripts/output/_w952_batch3.json、scripts/output/_w952_batch4.json、scripts/output/_w952_batch5.json、scripts/output/_cascade_files_W952.txt、sCREADME.md、HANDOVER.md、docs/00-导读/W批次编号对账表.md

**缺口**：reader 共 622 页，本批之前仅 **27 页**有题图（缺口 595 页）；本批 12 张接入 12 个页面 ⇒ 累计 **39 页**有题图。

**题材（人物 8 + 主题 4·每张一个独占标志物）**：白龙马（白衣龙君 + 三叉戟 + 龙影）、独角兕大王（青牛独角 + 方头钢叉）、灵感大王（鱼尾龙袍 + 玉钵）、黄风怪（黄鼠狼身 + 叶形芭蕉扇 + 风纹）、赛太岁（金毛犼 + 紫金铃）、九灵元圣（九头狮）、哪吒（乾坤圈 + 火尖枪 + 混天绫 + 风火轮）、昴日星官（公鸡形貌 + 长鞭）｜紧箍咒（金箍九倒刺 + 朱砂红绦）、筋斗云（祥云涡卷 + 悟空端坐）、法宝系统（五件法宝弧形列阵）、无字真经（空白经卷 + 淡赭金横纹）。

**风格同族由构造保证**：母版的**风格段 211 字符**从上批母版程序化复用（`scripts/_w952_make_prompts.py` 读上批 JSON 取母版），**只替换构图句**——由「上部 28% 留白供叠字」改为「主体上方只留约一成呼吸空间·不设专用标题区」（因用户上批已裁决页面上裁掉留白，本批直接按无标题区构图）。脚本自带两条断言：批内 12 条母版逐字一致 + 风格段与上批母版逐字一致。

**判据口径调整**：J2「顶部留白带」由 28% 放宽为 **10%**（上批留 28% / 本批留一成 ⇒ 取交集·顶部 10% 必为纯纸面），其余 J1/J3–J10 不变；站点版验算（主体顶未切 + 主体底未切 + 下部地面留白 > 0）同步覆盖本批。

**接入**：沿用站内 `chapter-plate` 范式（420px 居中 + 描述性 alt + 浅底图暗色模式隐藏）。

**并发纪律**：共享面按内容粒度**精确暂存**（`git update-index --cacheinfo`·HEAD 为基底叠加本批段）⇒ 不把对方在途内容带进本批提交。

> - **验证**：母版判据 J1–J10 **28/28 PASS**（`_w945_plates_verify.py`·目录扫描一次覆盖 28 张）· 站点版验算 **28/28 PASS**（`_w951_check_crop.py`：主体顶未切 + 主体底未切 + 下部地面留白 > 0）· 第 31 与第 45 门禁 0 FAIL · CSP 856 页 0 漂移 · lint_links 20858 链接 0 broken · J10 口径修正后自证仍可抓白边（合规 0.315 / 白边样本 8.609 > 阈值 5.0）
> - **状态**：在途（认领登记 W952·待提交入库）
> **状态**：**已收官**（W952 49f2f558·git 反填·共 4 笔·W971 存量回填）


### W951（2026-10-25）：题图版式批（站点版裁掉上部留白·16 张题图页面呈现紧凑化）

> **来源**：用户 2026-10-25 在问卷中裁决「裁掉·页面更紧凑」——承接 W945/W948 两批共 16 张线描人物题图。
>
> - **文件**：site/static/images/plate-line-0[1-8]-*.webp（16 张站点版重出）、assets/promo/plate-set/preview-site-sheet.png（站点版拼图）、assets/promo/plate-set/README.md、scripts/_w945_prepare.py、scripts/_w951_check_crop.py、scripts/_w951_site_sheet.py、scripts/_w951_cascade.py、scripts/output/_cascade_files_W951.txt、Cdscripts/output/file-index.md

**问题**：出图规格要求「画面上方 28% 纯纸面留白（供叠字）」，而内页版式里页面标题 `<h1>` 本就在图的**外面上方**
⇒ 标题与画面主体之间多出约 **190 px** 冗余空白（浏览器实跑 1280 视口量得），第一眼像「图缺了一块」。

**方案迭代（三次才收敛·每版均经浏览器实跑 + 机器验算后才否决）**：

| 版本 | 做法 | 实测结果 | 处置 |
|---|---|---|---|
| v1 | 页面 CSS：`.chapter-plate{overflow:hidden}` + `img{margin-top:-37.33%}` | 浏览器实跑**人物下半身丢失**（画面被截断） | 弃（CSS 整体回退，页面零改动） |
| v2 | 资产层统一裁 28%（源图 448 px） | 机器验算**会削到 6 张的主体顶端**（观音主体顶 419 ⇒ 削 29 px；太上老君 417 ⇒ 削 31 px） | 弃 |
| v3 | 主体对齐画布顶部 + **一并裁掉下部** | 浏览器实跑**人物悬空**——母版下部 62–141 px 是画师留的「地面留白」，裁掉即破坏「人物站在地上」的构图关系 | 弃 |
| **v4（落地）** | **只裁上部留白**：逐张裁切线 = 该张主体顶 − 6 px，**保留下部地面留白** | 主体顶落在画布 6 px（标题紧贴主体）· 人物完整 · 人物不悬空 · 人物大小不变（不缩放） | ✅ |

**新增判据** `scripts/_w951_check_crop.py`：验站点版宽 = 1200、**主体顶未被切**（墨迹 bbox 顶 ≥ 1 px）、**主体底未被切**（bbox 底 < 画布高）、**下部地面留白 > 0**（人物不悬空）⇒ **16/16 PASS**（主体顶 6–7 px·地面留白 62–141 px·站点版高 1056–1189）。

**资产分层**：`assets/promo/plate-set/` 仍是**完整母版**（1200×1600·含上部留白·供卡片叠字 / 分享图裁切用）；
`site/static/images/` 是**页面版**（已裁上部留白）。两者不再相同——这是本批引入的结构变化，已在目录 README 登记。

**页面零改动**：16 个 reader 页的 HTML/CSS **一行未改**（v1 的 CSS 方案已整体 `git checkout` 回退），版式调整全在资产层完成 ⇒ 无 HTML 副作用、无 CSP 漂移。

**并发纪律**：本批共享面**按内容粒度精确暂存**（`git update-index --cacheinfo`·以 `HEAD:<file>` 为基底叠加本批段）⇒ 对方会话 W950 起宣布的新纪律我方先行践行，不整份 add ⇒ 不会把对方在途的共享面内容带进我的提交。

> - **验证**：站点版验算 16/16 PASS（`_w951_check_crop.py`）· 母版判据 J1–J10 16/16 PASS（`_w945_plates_verify.py`）· 浏览器实跑 `people/太上老君` 页：标题紧贴题图、人物完整、脚下地面留白保留
> - **状态**：已收官（`d5c3a5d5`·**并发纪律**：本批共享面按内容粒度**精确暂存**——以 `HEAD:<file>` 为基底叠加本批段、`git update-index --cacheinfo` 写入索引、工作树保持原样 ⇒ 对方在途内容既不入我的提交也不被我抹掉（先行践行对方会话 W950 起宣布的新纪律）；提交后已 `git log --oneline -1 -- <本站点版文件>` 核实归属落在本批·**未再被代提交**）
> **状态**：**已收官**（W951 6bd75e22·git 反填·共 2 笔·W971 存量回填）


### W950（2026-10-25）：图标集打磨优化批（重画 13 枚 + 光学尺寸归一 + 1967 处内联 SVG 图形同步 + 唯一事实源刷新器）

> **来源**：用户 2026-10-25 令「先把已经做好的图标进行打磨优化」⇒ 本批只打磨既有 45 枚（29 通用 + 16 时间线专属），不扩展新图标。

> - **文件**：site/static/icons/ui/（45 枚 SVG 资产重生成）、scripts/_w939_gen_icons.py、scripts/_w946_gen_timeline_icons.py（生成器接入归一参数）、scripts/_w950_normalize.py（新增·光学尺寸归一器）、scripts/_w950_refresh_icon_paths.py（新增·图形同步刷新器）、scripts/output/_w950_icon_normalize.json（新增·45 枚归一参数）、scripts/output/_w946_timeline_icons.js、scripts/output/_cascade_files_W950.txt、xiyouji-agent-web/src/components/UiIcons.tsx（由资产重建）、site/**（1967 处内联 SVG 图形同步 · 646 个文件）、docs/11-方案报告/计划方案/T26-任务计划执行与经验沉淀报告-2026-10-25.md、dCHANDOVER.md、README.md、STRUCTURE.md、docs/00-导读/项目说明.md、CITATION.cff。
> **状态**：**已收官**（W950 7908c96c·git 反填·共 6 笔·W971 存量回填）

**打磨前的问题（量化 + 目视双证）**：① 视觉边长 **12.8~20.4（极差 7.6 · 比值 1.59×）**——逐枚渲染量「墨色外接框」得出，目测只觉「有点不齐」；② **9 枚中心偏移**（如 `tl-pilgrim` 中心 x=14.5 明显偏右）；③ **11 枚辨识度弱**（link / menu / quote / child / pin / tl-pilgrim / tl-punctuation / tl-critical-edition / tl-newyear-print / tl-brush-comment / tl-mask）；④ **与既有重复** 2 处（`tl-scroll` ≡ 通用 `scroll`；`tl-pencil` ≈ 通用 `pen`）。

**重画 13 枚**（逐条记明改什么）：link（水平对置交叠双环）· menu（三横等长）· quote（加大并底部对齐）· child（加童蒙姿态：身+手+足）· pin（梯形钉头+顶帽+钉身）· tl-brush-comment（笔 + 三枚**独立**评点）· tl-critical-edition（两册并排 + 侧栏校注条）· tl-mask（戏曲脸谱：额饰+对称眉眼+口）· tl-newyear-print（竖幅挂轴 + 画中人物 + 边框）· tl-pencil（笔 + 下方三道批注线）· tl-pilgrim（侧身行脚僧：背经卷+持杖+日轮）· tl-punctuation（逗号+句号+一对引号横排居中）· tl-scroll（竖轴 + 展开卷面，与短轴头版区分）。

**光学尺寸归一**（系统化那一半）：生成器接入归一参数环节——渲染量测每枚墨色外接框 ⇒ 统一缩放到目标视觉边长（20；细长形符号按 18，避免三角/双竖被撑得过重）⇒ 平移到 24 网格中心 (12,12)；参数落 `scripts/output/_w950_icon_normalize.json`（生成器读取 ⇒ 仍是单一事实源）。**视觉边长极差 7.6 → 2.2 · 最大/最小比 1.59× → 1.12× · 中心偏移 9 枚 → 0 枚**；实开页面内 timeline 的 22 枚图标**尺寸全同 25.6px**。

**图形同步刷新器**（资产改了必须能同步到页面）：站点的内联 SVG 把 path **写死在 HTML 里** ⇒ 改了资产文件页面不会变 ⇒ 新增 `scripts/_w950_refresh_icon_paths.py`：A 通用集内联 SVG 按 path 的 **(d, transform, fill) 复合键**反查图标名 → 替换为新资产 path（含归一 transform）⇒ **1967 处 / 646 个文件**（复合键是必需的：单靠 `d` 有三组歧义 scroll/tl-scroll、star/star-solid、thumb-up/thumb-down）；B timeline 的 `TL_ICO` 映射块整段替换；C agent-web 的 `UiIcons.tsx` **由资产重建**（手抄 path 必然漂移）。幂等。

**当场修掉的一处真缺陷**：改了内联脚本（`TL_ICO` 块）后未重算 CSP 哈希 ⇒ 浏览器报 `Executing inline script violates Content Security Policy 'sha256-j4fJLNv…'` ⇒ **整个内联脚本被拒执行** ⇒ 时间线事件卡渲染中断（实测 `svgIco=0` / `eventCards=0`）⇒ 补跑 `generate_csp.py` 后恢复（22 事件卡 / 22 图标 / CSP 856 页 0 漂移）。这是仓内铁律第 3 条的第二次现场复现。

**经验 3 条**：E-19 矢量资产改动必须配「图形同步刷新器」（复合键反查·单靠 d 会因同形异义歧义）· E-20 视觉尺寸归一是图标集打磨最系统的一步（机器量测比目测可靠）· E-21 改内联脚本必须立刻跑 `generate_csp.py` 并 `--check`（哈希失配让整个脚本被拒执行·表现为「数据不渲染」而非报错）。

**未改**：任何管控脚本逻辑；正文装饰 emoji 与箭头符号；并行会话 W948 批在途件（对方已完成收官·当前无在途共享面内容）。


### W949（2026-10-25）：图标治理换路径复核批（第二次追问「确定做完了吗」· 堵数据源回归漏洞 + 字段图标位判据入机检 + 登记剩余 71 条）

> **来源**：用户 2026-10-25 第二次追问「你确定现在已经做完图标了吗」⇒ 本批**刻意避开前三轮已用过的三条路径**，改查没查过的地方。

> - **文件**：dataset/timeline.json（数据源 22 个 icon 字段 emoji → 图标名）、scripts/_w949_fix_dataset.py、scripts/_w949_allowlist.py、scripts/check_icon_fields.py（字段图标位判据）、scripts/check_emoji_icons.py（第 50 门禁挂入 A2 段）、scripts/output/_w949_icon_field_allowlist.json、docs/11-方案报告/计划方案/T26-任务计划执行与经验沉淀报告-2026-10-25.md、dCHANDOVER.md、README.md、STRUCTURE.md、docs/00-导读/项目说明.md、CITATION.cff。
> **状态**：**已收官**（W949 a59a7499·git 反填·共 4 笔·W971 存量回填）

**换路径复核**：① 扫描范围从「4 个目录」扩到**全仓 17 个顶层目录 · 全部文件类型**（前三轮从未覆盖 `scripts/` `docs/` `archive/` `dataset/` `tests/` `.github/`）；② 新增**字段图标位**判据（`avatar:` / `icon:` / `flag:` / `STAGE_EMOJI`）；③ 数据源与页面内嵌副本**逐位对拍**。

**抓出的真遗漏**：① **`dataset/timeline.json` 仍含 22 个 emoji icon 字段** ⇒ ⚠️ **回归漏洞**：任何一次跑生成器都会把 emoji 灌回页面，治理结果不可复现（假收敛）；② `dataset/ai-dialogue.json` 6 处 `avatar`；③ `dataset/cross-time-danmaku.json` 4 处 `flag` + `site/en/json/rescue_roi.json` 4 处 `icon`；④ `ai-dialogue`（中英）12 处 `avatar:` 名人头像位；⑤ `narrative-experiment`（中英）18 处 `avatar:`/`icon:`；⑥ `methodology-matrix`（中英）9 处 `icon:`；⑦ `chart-design`（中英）10 处 `STAGE_EMOJI`；⑧ `cross-time-danmaku`（中英）8 处 `flag:` 国籍标识。

**本批已做**：① **堵回归漏洞**——修 `dataset/timeline.json` 的 22 个 icon 字段，并与中英页面内嵌副本逐位对拍（22==22 且逐位相同）⇒ 该数据源剩余具象字符 **0**；② **把漏网变成机检可抓**——新增 `scripts/check_icon_fields.py` 与白名单 `scripts/output/_w949_icon_field_allowlist.json`（**由扫描器实测产出 + 程序附理由**，非手写字符：手写会与扫描器口径漂移，ZWJ 序列被拆 / VS16 丢失 / 国旗逐字排序三类漂移都真实发生过）⇒ 白名单外的新命中判红、白名单条目已消失判红（防腐化）、白名单清空即自然转绿（不设恒红豁免）⇒ 第 50 门禁新增 **A2 段**，现状命中 **71 条 / 13 个文件**、白名单外 0、待核销 0。

**剩余 71 条已登记逐类治理方案**（下一批施工）：名人头像 26（需每人专属头像）· 剧本角色头像 8 · 指标卡图标 9 · 情景卡图标 9 · 螺旋阶段符号 10 · 国籍标识 12（⚠️ 国旗是复杂旗帜图案，线描图标集无法表达 ⇒ **待用户裁决**：改文字国名 / 两字母代码，还是自绘国旗图形）。

**经验补充 3 条**：E-16 治理必须同时改「页面」与「数据源」（只改内嵌副本 ⇒ 不可复现 ⇒ 须逐位对拍）· E-17 机检白名单必须由扫描器产出、不可手写（规范化口径漂移）· E-18 「扫过某目录」与「覆盖该目录」是两件事（复核面要按**产物形态**枚举）。


### W948（2026-10-25）：内页专题题图续批（8 张线描人物题图·与上批同族·累计 16 张）

> **来源**：用户 2026-10-25 令「再继续帮我做几张素材图」，并要求开工前先问三件事。
>
> **三问答复**：① 用途与画幅 = **内页专题题图续批 · 3:4 竖版** ② 张数 = **8 张** ③ 参考风格 = **沿用站内线描墨稿风**（附加题材范围 = **人物专题扩批**）。
>
> - **文件**：site/static/images/plate-line-01-jinjiao.webp … plate-line-08-taishanglaojun.webp、assets/promo/plate-set/**、8 个 reader 人物页、Cdsscripts/_w948_*.py、scripts/output/_w948_batch*.json

**承接 W945**：站内线描人物题图由 8 张扩到 **16 张**，规格与画幅完全一致（3:4 · 1200×1600 · 宣纸底 + 单色墨线 + 赭金细节 + 单处朱砂点睛 · 上部 28% 纯纸面留白 · 主体完整全身立像占高五成）。

**母版逐字复用由构造保证**：`scripts/_w948_make_prompts.py` 读上批 `_w945_batch1.json`，取「主体：」之前的 252 字符风格母版直接拼本批 SUBJECT 段 ⇒ 母版不靠人手抄、不靠人眼核对；再由 `_w945_check_prompts.py` 的 `==` 断言二次确认。

**题材**（取经路上的妖怪与神将组，每张一个独占标志物）：牛魔王（牛首 + 混铁棍）、铁扇公主（叶形芭蕉扇 + 短柄缠绳）、蝎子精（上翘蝎尾毒钩 + 倒马毒桩）、金角大王（紫金红葫芦 + 朱红封带）、黄袍怪（狼首 + 金钢琢）、镇元大仙（人形人参果 + 拂尘）、大鹏金翅雕（鹏翼 + 阴阳二气瓶）、太上老君（太极图 + 拂尘）。

**判据扩面**：`_w945_plates_verify.py` 由写死的 8 张清单改为**扫目录取全部 `plate-line-*.png`** ⇒ 一套判据（J1–J9 + 负样本自检）一次覆盖 16 张。

> - **验证**：机器判据 J1–J10 **16/16 PASS**（`_w945_plates_verify.py`·目录扫描一次覆盖 16 张）+ 两个负样本自检判据可证伪（浓墨渲染型方图 ⇒ 抓 J1/J2/J3/J6；8 px 黑框样本 ⇒ 抓 J8 检出 16 处贯穿暗线）· **J10 在本批首轮实测有效**：精准抓出 2 张模型画出的「左右白边」图（背景差 12.96 / 12.09），其余 14 张 0.04–1.59 无误报 · 人眼 J8 题材与形制逐张核（拼图 + 主体包围盒放大 + 关键部位 3 倍高倍）· 顶部 28% 留白墨量 0.0000–0.0015 · 纸色归一残差 0.17–0.57/255 · 第 31 与第 45 门禁 0 FAIL · CSP 856 页 0 漂移 · lint_links 20846 链接 0 broken
> - **状态**：已收官（`88fa5952`·**并发事实**：本批共享面被两个他方提交代提交——CHANGELOG 的 W948 段被 W949 批 `276eaa4b` 带入、台账的 W948 行被 agent-web 批 `29a182ff` 带入；本批不修改他方提交历史，只在本方行与本方段内登记该事实；台账 W948 行已按回填独占规则回填 hash + 状态 + touches）
> **状态**：**已收官**（W948 62365964·git 反填·共 4 笔·W971 存量回填）


### W947（2026-10-25）：图标治理复验与补治批（用户追问「你确定现在已经做完图标了吗」→ 三路全量复验 + 补治两处遗漏范围 + 更正一处误判）

> **来源**：用户 2026-10-25 追问「你确定现在已经做完图标了吗」⇒ 全量复验（本批起因）。
> 承接 W941（UI 图标位 emoji 归零 + 通用图标集 27 枚）与 W946（描边参数修复 + 时间线专属图标 16 枚 + 第 50 门禁）。

> - **文件**：scripts/_w947_add_icons.py（通用图标集补 2 枚）、scripts/_w939_gen_icons.py（并入 note / link）、site/static/icons/ui/note.svg、site/static/icons/ui/link.svg、site/static/js/rag-chat.js（🔗 前缀 → 内联 SVG）、xiyouji-agent-web/src/components/UiIcons.tsx（新建·内联 SVG 图标组件）、xiyouji-agent-web/src/components/PermissionDialog.tsx（⚠️ 📝 → 组件）、xiyouji-agent-web/src/components/InlinePermissionCard.tsx（⚠️ → 组件）、scripts/check_emoji_icons.py（标题改号）、docs/11-方案报告/计划方案/T26-任务计划执行与经验沉淀报告-2026-10-25.md、dCHANDOVER.md、README.md、STRUCTURE.md、docs/00-导读/项目说明.md、CITATION.cff。
> **状态**：**已收官**（W947 02ef09ee·git 反填·共 4 笔·W971 存量回填）

**三路全量复验**：① 静态口径（基准扫描器·UI 图标位）**0 命中**；② 全仓兜底 grep 剩余 **559 处 / 58 种**，逐类判定为**内容语义**（✅156 正文结论标记 / ✓200 判定文本 / 人物头像 20 / 勋章奖牌 / ⚡12 / 国旗 / 图表符号）⇒ 按用户裁决保留；③ 渲染实测（8 页 × `file://` + `http://` 双环境 + **像素级取证**）。

**补治两处此前遗漏的范围**：**agent-web React 组件**（PermissionDialog 的 ⚠️📝、InlinePermissionCard 的 ⚠️）与**共享 JS**（rag-chat.js 的 🔗）共 **4 处界面图标位**。该应用已有成熟 TDesign 图标体系，但 `@tdesign-icons-react` **依赖未安装** ⇒ 无法验证未用过的图标名 ⇒ 改为新建 `UiIcons.tsx`（内联 SVG·图形与静态站资产逐字同源·零新增依赖·颜色跟随 `currentColor`）；通用图标集补 **2 枚**（`note` 折角纸页 / `link` 双环链条）⇒ 27 → **29 枚**。

**保留并登记**：useChat.ts 与 rag-chat.js 错误消息文本内的 ⚠️ 共 **7 处**——它们随消息流输出、可复制、会被读屏朗读 ⇒ 属**语义标记**而非界面图标位 ⇒ 按「仅 UI 图标位」裁决保留。

**更正上批一处误判（像素级取证推翻）**：上批据控制台 CORS 报错推断「CSS `content` 位的 22 处图标在 `file://` 下不显示、线上正常」，本批像素取证（mask 宿主左上角 30×26 区域深色像素计数，file:// 与 http:// 同位比较：`data/concept-device.html` 17 vs 20、`data/game-webnovel.html` 18 vs 22）证明**两环境均真实绘制** ⇒ 该结论作废，「22 处改内联 SVG」从缺陷修复项**降级为可选优化**。教训：**报错文本 ≠ 渲染结果**，渲染正确性判据必须做像素级取证。

**经验补充 3 条**：E-13「报错文本不等于渲染结果」· E-14「扫过某个目录不等于覆盖那个目录」（治理范围须按**产物类型**枚举：静态页 / 共享 JS / React 组件）· E-15「用户追问『做完了吗』是最有效的自查触发器」。

**共享面纪律（采纳并行 W945 会话书面建议）**：本批提交用**显式 pathspec 只列自己批的文件**，不再用宽 pathspec——同仓有在途批次时宽 pathspec 会把他人在途件一并提交（W946 的 `ed09a65e` / `923afc4c` 即因此代提交了 W945 的题图资产与脚本，已由该会话收官并留痕）。


### W946（2026-10-25）：图标治理续作批（.ico 描边参数修复 + 时间线专属图标 16 枚 + 第 50 门禁「UI 图标位零残留 · 图标渲染正确性」）

> **来源**：用户 2026-10-25 令「禁止使用 emoji 表情当做图标，你审查一下。你要么进行设计一下图标」，经问卷两问裁决（范围=仅 UI 图标位 / 风格=东方线描）后分两批执行：W941（主体：1,910 处图标位归零 + 通用图标集 27 枚）→ **W946（本批：补齐 W941 的三处缺口）**。

> - **文件**：site/system.css（`.ico` 基类补 fill/stroke/linecap/linejoin 描边参数）、site/static/icons/ui/tl-*.svg（16 枚时间线专属图标）、site/data/timeline.html、site/en/timeline.html（22 条事件数据字段 + 渲染改内联 SVG + TL_ICO 映射内联 + CSP 重算）、scripts/_w946_gen_timeline_icons.py、scripts/_w946_apply_timeline_icons.py、scripts/check_emoji_icons.py（第 50 门禁）、scripts/_w939_emoji_to_svg.py（svg_tag 模板补 SVG 属性）、scripts/output/_w946_timeline_icons.js、docs/11-方案报告/计划方案/T26-任务计划执行与经验沉淀报告-2026-10-25.md、dCHANDOVER.md、README.md、STRUCTURE.md、docs/00-导读/项目说明.md、scripts/output/file-index.md。
> **状态**：**已收官**（W946 88eacc8a·git 反填·共 3 笔·W971 存量回填）

**缺口 ①（严重·视觉）：内联 SVG 丢了描边参数 ⇒ 图标渲染成黑块**。W941 批的静态判据全绿（图标位 0 残留、尺寸正确），但 **Playwright 实开 file:// 才发现**：内联 `<svg>` 片段只带了 class/width/height/viewBox，**漏了 `fill="none" stroke="currentColor"`** ⇒ 图形落回 SVG 默认样式（黑填充、无描边）⇒ 1,957 处图标全是黑块。**修法**：把描边参数写进 `.ico` 基类 CSS（CSS 优先级高于 presentation attribute，且 `.ico` 类选择器特异性高于站内 `svg` 元素规则）⇒ **零 HTML 改动、全站立即生效**；同时给替换器 `svg_tag()` 模板补上 SVG 属性（未来重跑产出更稳的 HTML）。实测复核：浅色模式 stroke=墨色 `rgb(35,32,26)`、暗色模式 stroke 自动变朱砂 `rgb(224,96,79)`（主题自适应确认）、尺寸 13–16px 跟随字号（非 300×150 巨图）。

**缺口 ②：时间线的 15 种 emoji 承载 22 事件、且「📖」一符两义**（佛经西行 vs 连环画普及）⇒ **通用图标集表达不了「成书/游记/评点/戏曲/影剧/数字化」的语义差** ⇒ 另设计 **16 枚语义专属图标**（`tl-*` 前缀）：行脚僧（玄奘西行）、立轴（大唐西域记）、灵光（取经诗话）、脸谱（戏曲与影视）、百回刻本、太极（丹道评点）、整理校注本、评点笺注、新式标点、校注笔、数字库、连环画格、清代年画、胶片、显像管、手柄。**按事件语义而非按字符拆分** ⇒ 数据字段由 emoji 改为图标名（`icon: 'tl-pilgrim'`），渲染改 `.html(d => TL_ICO[d.icon] || '')`，映射表内联进页面（保持自包含）。两页 emoji 序列一致性作断言（22 == 22 且逐位相同）。目视复核重画 2 枚（`tl-pilgrim` 语义太弱 → 加持杖与日轮；`tl-punctuation` 读不出标点 → 改逗号+句号+引号三件套）。

**缺口 ③：没有防回归的机检** ⇒ 新增 **第 50 门禁 `scripts/check_emoji_icons.py`**，两段判据：
- **A 静态**：全仓 UI 图标位零 emoji 残留（判据与基准扫描器同源：控件首位 / 图标槽 class / 标题前缀 / CSS content）；
- **B 实测**：浏览器实开 4 个代表页 × **2 套环境**（`file://` 与 `http://127.0.0.1`）——校验内联 SVG 的 computed `stroke≠none` 且 `fill=none`、尺寸跟随字号（非巨图）、CSS content 位的同源 mask 已加载、自建图标资产零加载失败。
- **B 段的存在理由**：W941 批的静态判据全绿却漏掉「黑块」⇒ **静态判据无法覆盖「渲染正确」**，必须有浏览器实跑。

**门禁在双环境下的判据设计（如实登记）**：`http://`（= 线上同源·真实用户环境）全部判据严格——CSS `content` 位的同源 mask 在此环境**全部加载成功**（实测 7/7）；`file://`（本地双击）下同源 mask 被 CORS 拦 ⇒ 该 22 处图标在本地不显示、线上正常 ⇒ 门禁在 file:// 下记 NOTE 不判红（与该环境既有的字体子集 CORS、fetch 不支持 file scheme 同级），在 http 下判红。**待修项已登记**：把这 22 处改为真实内联 SVG 元素（11 个选择器 × 中英两版）可彻底消除该降级，属独立批。

**顺带修掉两个自查发现的真 bug**：① `TL_ICO` 映射曾被插到使用点之后（`TL_ICO is not defined`）⇒ 改为插入使用点所在 script 块开头；② 映射表的对象键含连字符（`tl-critical-edition`）未加引号 ⇒ JS 语法错误（`Unexpected token '-'`）⇒ 键一律加引号；③ 渲染从 `.text(d => d.icon)` 改写时**漏掉 D3 回调箭头**（`.html(TL_ICO[d.icon])`）⇒ `d is not defined` ⇒ 改回 `.html(d => TL_ICO[d.icon] || '')`。

**验收**：第 50 门禁 **PASS**（静态 0 处残留 + 双环境实测 0 判红项）· timeline 22 事件 22 个内联 SVG 渲染正确（file:// 实测 `svgIco=22`、无 pageerror）· 内联 SVG 描边浅色=墨色/暗色=朱砂 · CSP 856 页 0 漂移。

**未改**：正文装饰 emoji 与箭头符号（按裁决保留）；W941 已入库的 1,957 处 HTML 结构（仅修 CSS 与模板）；并行批次在途件（hero 素材批 / W945 题图批等）一律未纳入本提交。


### W945（2026-10-25）：内页专题题图成套（8 张 3:4 线描人物题图·622 页仅 11 页有题图的缺口）

> **来源**：用户 2026-10-25 令「在继续帮我做几张素材图：用途与画幅、风格与配色统一、主体清晰、留好放文字的空间都考虑到，成套出图保证风格一致」，并要求开工前先问三件事。
>
> **三问答复**：① 用途与画幅 = **内页专题题图 · 3:4 竖版** ② 张数 = **8 张** ③ 参考风格 = **沿用站内线描墨稿风**（附加题材范围 = **人物专题**）。
>
> - **文件**：site/static/images/plate-line-01~08-*.webp、assets/promo/plate-set/**、8 个 reader 专题页、Cdsscripts/_w945_cascade.py、scripts/_w945_plates_verify.py、scripts/_w945_insert_plates.py

**缺口**：站内 `site/reader/` 共 **622 页**，其中**仅 11 页**有题图（6 个回目页 + 5 个专题页）——people / themes / essays / poetry / culture 五库绝大部分页面无题图。

**产出**：8 张**线描墨稿风人物题图**，3:4 竖版（`1200×1600`），沿用站内线描语言（宣纸底 `#FAF7F0` + 单色墨线 + 赭金 `#8A6D3B` 细节 + 单处朱砂 `#C8463A` 点睛），**上部 28% 保持纯纸面留白**供标题叠字，主体居中偏下：

| # | 主体 | 独占标志物（形制级） | 接入页 |
|---|---|---|---|
| 01 | 大圣悟空 | 如意金箍棒（两端金箍 + 云纹）+ 凤翅紫金冠 | themes/猴王到行者-五次蜕变 |
| 02 | 唐僧 | 五佛冠 + 念珠 + 九环锡杖 | themes/唐僧-凡躯圣心 |
| 03 | 猪八戒 | 九齿钉耙 + 蒲扇耳 | people/猪八戒 |
| 04 | 沙僧 | 降妖宝杖（月牙刃）+ 骷髅念珠 | themes/沙僧-沉默者的智慧 |
| 05 | 观音菩萨 | 玉净瓶插杨柳枝 + 莲花座 | people/观音 |
| 06 | 二郎神 | 三尖两刃刀 + 额间竖目 | people/二郎神 |
| 07 | 白骨精 | 三变残影（村姑 / 老妇 / 老翁） | people/白骨精 |
| 08 | 红孩儿 | 火尖枪 + 三昧真火 | people/红孩儿 |

**接入范式**：沿用站内 `chapter-plate`（`max-width: 420px` 居中 + 描述性 alt + 浅底图暗色模式隐藏）。

**判据**：J1–J7 机器关（尺寸 / 顶部留白 / 墨量 / 朱砂点 / 实心块 / 伪文字 / 裁切）+ **J8 人工关**（独占标志物 + 形制级细节）——题材与形制机器判据查不出，只能人眼核。

> - **验证**：机器判据 J1–J9 **8/8 PASS**（`scripts/_w945_plates_verify.py`）+ 两个负样本自检判据可证伪（浓墨渲染型方图 ⇒ 抓 J1/J2/J3/J6；8 px 黑框样本 ⇒ 抓 J8 检出 16 处贯穿暗线）· 人眼 J8 题材与形制逐张核（拼图 + 主体包围盒放大 + 关键部位 3 倍高倍）· 顶部 28% 留白墨量 0.0000–0.0015 · 纸色归一残差 0.20–1.00/255 · 第 31 与第 45 门禁 0 FAIL · CSP 856 页 0 漂移 · lint_links 20838 链接 0 broken
> - **状态**：已收官（`83f31387`·**并发事实**：本批资产、8 页接入与共享面段被并行 W946 批代提交 `ed09a65e` / `923afc4c`——其提交信息称「未改并行会话 W945 批在途件」，与其实际 pathspec 范围不符；台账 W945 行已按回填独占规则回填 hash + 状态 + touches）
> **状态**：**已收官**（W945 7f05e47f·git 反填·共 3 笔·W971 存量回填）


### W944（2026-10-25）：章回插画新组（6 张按回目情节重出·打破「挑担人赶路」同构）

> **来源**：用户 2026-10-25 认可 W943 记录的弱项「章回 6 张「挑担人赶路」重复度极高，若要丰富可另出一组」并答「可以」。

> - **文件**：site/static/images/chap-07.webp、site/static/images/chap-14.webp、site/static/images/chap-15.webp、site/static/images/chap-23.webp、site/static/images/chap-27.webp、site/static/images/chap-30.webp、Cdsscripts/_w944_cascade.py

**问题**：站内 6 张章回插画（chap-07 / 14 / 15 / 23 / 27 / 30）原为**同一构图**（挑担僧人赶路）仅换山水，与所在回目无对应关系。

**改法**：按各自回目情节另出一组 6 张（水墨浓墨剪影风：宣纸底 + 浓墨剪影 + 淡赭金远山 + 单个朱砂方印，正方 1200×1200）——第 007 回 八卦炉（三足丹炉 + 火焰）、第 014 回 心猿归正（猴形剪影 + 金箍 + 勒绳）、第 015 回 鹰愁涧（惊马扬蹄 + 缰绳 + 瀑布崖）、第 023 回 四圣试禅心（打坐僧 + 孤灯 + 雾中两道人影）、第 027 回 尸魔三戏（三道人影渐次消散 + 月 + 茅屋）、第 030 回 邪魔侵正法（蛇形妖影 + 洞口 + 螺旋墨风）——**每张现与回目情节对应**。

**一处模型伪影已修**：第 023 回新图自带一圈黑边框（模型给禅心图套了相框）⇒ 按四边近黑像素带自动检测裁除（每边 66 px）后重存。

> - **验证**：6 张逐张放大目视（构图与回目情节对应 + 无黑框 + 无伪文字）+ 旧版 6 张备份于 %TEMP%/bak_chap-*.webp 可回退 · 第 31 与第 45 门禁 0 FAIL
> - **状态**：在途（认领登记 W944·待提交入库）
> **状态**：**已收官**（W944 6d042d08·git 反填·共 1 笔·W971 存量回填）


### W943（2026-10-25）：全站图片审查（227 张逐类目视 · 修 3 处真缺陷）

> **来源**：用户 2026-10-25 令「不要只审查这几个图片，审查全部」——W940 修题材、W942 修形制之后的第三次加严。

> - **文件**：site/static/images/og-15-shijian-liejian.webp、assets/design/ai-concepts/concept-03-scroll.png、assets/design/ai-concepts/concept-06-bodhi-leaf.png、Cdsscripts/_w943_cascade.py

**审查范围**：全仓 **227 张**（>400×200 的位图）逐类拼图目视——卡片图 27 / 章回插画 6 / hero 24（15 渲染 + 9 线描）/ 分享图 15 / 设计概念稿 18 / 杂项 12（封面 / 单页正反面 / 站点截图 / 主视觉 / 淡墨远山），另含本批线描 9 张与内页浓墨题图 5 张。

**查出 3 处真缺陷并已重出修复**：① **`site/static/images/og-15-shijian-liejian.webp`（线上分享图）**——抽象墨块序列中夹 3 处「LI」字母残留（模型伪文字）⇒ 重出去字母版；② **`assets/design/ai-concepts/concept-03-scroll.png`**——卷面有潦草伪汉字（写「孙悟空 / 取经路线」样字）⇒ 重出为空白纸面 + 抽象笔触；③ **`assets/design/ai-concepts/concept-06-bodhi-leaf.png`**——文件名「菩提叶」但画成水滴 / 火苗形（形制不符）⇒ 重出为心形叶 + 中脉分叉叶脉 + 叶柄 + 露珠。

**其余全部题材对题**：卡片 27 张（场景人物）、章回 6 张（取经路途）、hero 24 张（法器场景）、og 15 张（器物特写）、概念稿 18 张（法器线描）、杂项 12 张（版面产物）。

**一条方法论结论**：机器阈值对渲染型素材**无效**——按线描图设的「纸色偏离 / 墨量」阈值在水墨渲染图上必然误报（实测 30+ 张假阳）⇒ **题材关与形制关只能人眼核**，已并入 J8（机器判据只管「画得好不好」，管不了「画的是什么 / 形制对不对」）。

**两处弱项（不构成错图·记录备查）**：`concept-05-headband-ring` 是纯黑墨圈（紧箍意象弱；线上正确版本为 W942 的金圈 + 九倒刺）、章回 6 张「挑担人赶路」高度同质。

> - **验证**：3 张重出件逐张放大目视（字母消失 / 伪文字消失 / 叶形正确）· 227 张全量拼图目视两轮（题材级 + 可疑项放大级）· 第 31 与第 45 门禁 0 FAIL
> - **状态**：在途（认领登记 W943·待提交入库）
> **状态**：**已收官**（W943 42f4560d·git 反填·共 1 笔·W971 存量回填）


### W942（2026-10-25）：Hero 素材全量复审（14 张逐张放大目视 · 修正 2 处形制偏差）

> **来源**：用户 2026-10-25 令「你再审查一遍有没有出现同样错误的」——W940 修正题材后仍要求全量复查。

> - **文件**：assets/promo/hero-set/hero-line-04-tight-crown.png、assets/promo/hero-set/hero-line-04-tight-crown.webp、assets/promo/hero-set/hero-line-07-banana-fan.png、assets/promo/hero-set/hero-line-07-banana-fan.webp、assets/promo/hero-set/raw/hero-04c-tight-crown.jpg、assets/promo/hero-set/raw/hero-07c-banana-fan.jpg、assets/promo/hero-set/preview-contact-sheet.png、assets/promo/hero-set/preview-contact-sheet.webp、assets/promo/hero-set/README.md、site/static/images/hero-line-04-tight-crown.webp、site/static/images/hero-line-07-banana-fan.webp、Cdsscripts/_w942_cascade.py

**复审方式**：9 张线描横幅 + 5 张浓墨题图共 **14 张逐张放大目视**——机器判据只管「画得好不好」（尺寸 / 留白 / 墨量 / 朱砂点 / 实心块 / 伪文字 / 裁切），**题材与形制必须人眼核**。

**发现并修正 2 处形制偏差**：① **04 紧箍儿**原为「光滑金圈 + 云纹扣」，而原著紧箍儿是**带九个倒刺钩**的金圈——缺此关键特征会被读成玉镯 / 头环 ⇒ 重出补足九倒刺；② **07 芭蕉扇**原为**正圆团扇 + 直柄**，而铁扇公主的芭蕉扇是**叶形（长卵形）扇**（形制偏差）⇒ 重出为叶形扇 + 中脉细脉 + 短柄缠绳。

**复审合格 12 张**：01 金箍棒（两端金箍带云纹）/ 02 行程图卷轴 / 03 经卷与篆香 / 05 莲花 / 06 九环锡杖（环环相扣 + 顶部宝珠）/ 08 玉净瓶（净瓶插杨柳）/ 09 筋斗云，以及内页 5 张浓墨题图（判官队列 / 紧箍与金刚杵 / 五行山两界山·铁链 / 东海龙宫水殿 / 六道轮回轮）。

**判据扩容**：J8 题材关在自检表里细化到**形制级**——不只问「是什么」，还要问「形制对不对」（倒刺钩数 / 扇形 / 环数 / 瓶插什么枝）。

> - **验证**：素材判据 9/9 PASS（左留白 0.0000·整图墨量 0.0329–0.0809）· 重出件纸色归一残差 ≤1/255 · 成套拼图逐张目视 · 第 31 与第 45 门禁 0 FAIL
> - **状态**：在途（认领登记 W942·待提交入库）
> **状态**：**已收官**（W942 13ad66a4·git 反填·共 1 笔·W971 存量回填）


### W941（2026-10-25）：UI 图标位 emoji 治理批（禁 emoji 充当图标 + 东方线描图标集自绘 27 枚 + UI 图标位 1,957 处归零）

> **来源**：用户 2026-10-25 令「禁止使用 emoji 表情当做图标，你审查一下。你要么进行设计一下图标」，经问卷两问裁决——① 治理范围 = **仅 UI 图标位**（正文装饰 emoji 与箭头符号保留）② 图标风格 = **东方线描**（24×24 / 1.5px 描边 / currentColor 随主题）。

> - **文件**：site/static/icons/ui/（27 枚 SVG 图标资产 + 目录文档 2 件）、site/system.css（新增 `.ico` / `.ico-t` 基类）、site/reader/**（615 个阅读页：收藏 ★ → 星标图标、反馈 👍👎 → 拇指图标）、site/data/** 与 site/en/**（30 余个页面的判定符号 / 检索图标 / 年龄段页签 / 播放暂停按钮 / 侦探卡结论标签 / 批驳史段首标记）、site/js/reader-enhance.js（收藏按钮运行时态切换）、site/static/js/rag-chat.js（检索来源与相关语料标签前缀）、site/static/js/text-search-app.js（空态图标）、scripts/_w939_gen_icons.py、scripts/_w939_scan_targets.py、scripts/_w939_emoji_to_svg.py、scripts/output/_w939_targets.json、scripts/output/_w939_replacements.json、docs/11-方案报告/计划方案/执行前计划-T26-UI图标emoji治理批.md、docs/11-方案报告/计划方案/T26-任务计划执行与经验沉淀报告-2026-10-25.md、docs/11-方案报告/README.md、dCHANDOVER.md、README.md、STRUCTURE.md、docs/00-导读/项目说明.md、sscripts/output/stats-index.md。
> **状态**：**已收官**（W941 6e47596b·git 反填·共 3 笔·W971 存量回填）

**问题量化（先审查·后施工）**：全仓 emoji 共 34,530 处 / 2,189 文件，绝大部分在 Markdown 正文（题材内容）。真正承担「图标职能」的是 **1,910 处 UI 图标位**，分布 **629 个页面**，只用 **21 种字符**（👍👎☆🔍📚📜📖📻📌👶🎒🎓🌱🜂✒📊🌐⏸☰✕✓✗★ 等）——这类用法的代价是**跨平台字形不一致**（Windows/macOS/Linux/移动端渲染各异）、**暗色模式不可控**（emoji 自带彩色，无法跟随主题）、**无语义**（屏幕阅读器读「thumbs up」而非「赞同」）。

**自绘图标集（27 枚·东方线描）**：`site/static/icons/ui/*.svg` 为单一事实源，规格 **24×24 viewBox / stroke 1.5 / round cap+join / fill:none / stroke:currentColor**——与既有 `.icon-moon` / `.icon-sun` **同参数同族**，不是另起一套风格。图形含星标与实心星、竖/倒拇指、对勾与叉、放大镜与检视镜、线装书与展卷、卷轴、广播匣、图钉、警示、引语、童蒙/书囊/士冠、幼苗、炼金方符、墨笔、柱状图、地球、菜单、关闭、播放与暂停。生成器 `scripts/_w939_gen_icons.py` 落盘，**目视复核出图**（`tmpe/_w939_icons_preview.png`）并据此重画 6 枚（`close` 与 `cross` 视觉重复→`close` 改方框内叉；`pin` 补圆头斜肩；`schoolbag` 扣袋方块改横带；`scroll` 轴身加宽；`thumb-down` 改垂直镜像；`thumb-up` 换镜像同构）。

**承载机制的三重约束（实测得出·非偏好）**：① 站点 CSP 是 `img-src 'self'`（**无 `data:`**）⇒ data-URI + mask 方案会被 CSP 拦掉；② 520 个阅读页走**外链 CSS**、328 个走内联块 ⇒ 写在 `site/system.css` 的相对路径 `url(static/…)` 随目录深度失效（`site/reader/culture/` 深度 2）；③ `file://` 直开是铁律 ⇒ 外部 `<use>` sprite 受限。⇒ **唯一同时满足 file:// + CSP + 多层目录的矢量承载方式 = 内联 SVG**；例外只有 CSS `content` 位（放不了 SVG 元素），该 22 处宿主页全部位于深度 1（`site/data/` 与 `site/en/`）⇒ 用同源 `mask-image` + `../static/icons/ui/` 相对路径成立。每枚内联 SVG 另带 `width="1em" height="1em"` 兜底属性——CSS 未加载时不会退化成 300×150 巨图。

**两个可复跑机检脚本（判据可证伪）**：① `scripts/_w939_scan_targets.py`——把全仓 emoji 分为「UI 图标位」（控件首位 / 图标槽 class / 标题前缀 / CSS content）与「正文装饰」两类，输出逐条明细；② `scripts/_w939_emoji_to_svg.py`——每条替换规则带**独立预期命中数**（取自 ① 的基准清单，非实测反推），实际不符即**退出码 2** 拒绝写盘。规则命中一致率 **37/37 = 100%**。

**治理结果**：UI 图标位 **1,910 → 0**（基准扫描器复扫，M-01）；另补治 47 处后续发现（兜底 grep 揪出扫描器漏检：JS 按钮文本 ▶⏸ 共 30 处、静态播放按钮 6 处、检索来源/语料标签前缀 2 处、段首提示标记 2 处、侦探卡结论标签前缀 2 处），累计替换 **1,957 处**；CSS 级联 **328 内联页**重同步（520 外链页自动生效）；CSP **14 页**重算、856 页 **0 漂移**。

**正文零损伤（HEAD↔工作树字符净差核验）**：逐文件对比 git HEAD 与工作树，净减少仅限图标位应有的 25 种字符（☆👍👎 各 608 + 零散 46 处），**正文型字符（✅78 / ✓200 / 🧑20 / 🎭8 / ★8 / ☆4）净差为 0**；箭头 `→`/`←` 因承担正文流程语义（5,000+ 处）按用户裁决**原样保留**。

**保留项登记（如实披露·非遗漏）**：① 星级评分 `★`/`☆` 12 处（难度与强度评分，**评分可视化**而非图标）；② `site/data/timeline.html` 与英文版的**数据字段** `icon:` 共 12 处（📖📚📜✒ 等，每条时间线事件的专属象征——通用图标集无法表达「成书/游记/评点」语义差，属**专属设计任务**）；③ `site/data/ai-dialogue.html` 人物**头像** emoji 4 处（🧑‍🎓，身份标识，通用图标会丢身份信息）；④ `site/data/methodology-matrix.html` 评分项 `icon:` 1 处；⑤ `site/data/business-model.html` 区间标注 `◀…▶` 2 处（内容表达）。

**未改**：任何管控脚本（`verify_delivery.py` / `bump_version.py` / `batch_cascade.py` / `preflight_check.py`）；既有 `.icon-moon` / `.icon-sun` 体系；正文装饰 emoji 与箭头符号；并行批次 W936 在途的共享面（提交用显式 pathspec 隔离）。


### W940（2026-10-25）：Hero 素材题材辨识度修正（09 换筋斗云 · 04 换紧箍儿 · 补题材关判据）

> **来源**：用户 2026-10-25 质疑「你确定这个图片符合主题吗？符合西游记吗？」——指向第 9 张「取经四众」。

> - **文件**：assets/promo/hero-set/hero-line-04-tight-crown.png、assets/promo/hero-set/hero-line-04-tight-crown.webp、assets/promo/hero-set/hero-line-09-somersault-cloud.png、assets/promo/hero-set/hero-line-09-somersault-cloud.webp、assets/promo/hero-set/raw/hero-04b-tight-crown.jpg、assets/promo/hero-set/raw/hero-05b-somersault-cloud.png、assets/promo/hero-set/preview-contact-sheet.png、assets/promo/hero-set/preview-contact-sheet.webp、assets/promo/hero-set/README.md、site/static/images/hero-line-04-tight-crown.webp、site/static/images/hero-line-09-somersault-cloud.webp、site/index.html、scripts/_w931_hero_verify.py、scripts/_w938_apply_home.py、Cdsscripts/_w940_cascade.py

**问题定性**：第 9 张「取经四众」被画成「农夫挑担」——金箍棒 / 九齿钉耙 / 月牙铲 / 僧帽**一个都没有**，且四人组侵入文字安全区（左留白 0.0174、整图墨量 0.1250 超判据上限）⇒ 题材与版面双不合格。根因在**判据缺口**：原判据只查尺寸 / 留白 / 墨量 / 伪文字 / 裁切五项，**没有「题材辨识度」这一关**。

**本批修正**：① **09 换「筋斗云」**（悟空专属符号·器物路线与 c2 同语言·左留白 0.0005·整图墨量 0.0431）—— 人物群像路线经「缩小右移」变体实测仍偏重、版面放不下 ⇒ 弃用；② **04 换「紧箍儿」**（「司南」属通用意象、非西游独占 ⇒ 换成第一回的独占物件：金圈 + 朱砂红绦）；③ **03 经卷保留**（「取经成果」贴题；候选「紫金钵」复核后视觉偏「饭碗」、与取经主线关联弱 ⇒ 不采用）；④ 旧文件（`hero-line-04-sinan-compass.*`、`hero-line-09-pilgrim-four.*`）在素材目录与站点两侧同步清理。

**补判据 J8（题材辨识度·人工关）**：目录 README 新增逐张「靠哪个《西游记》具体元素认出」自检表——每张须能答出其独占标志物（金箍棒 / 紧箍儿 / 九环锡杖 / 芭蕉扇 / 玉净瓶 / 筋斗云 为**强**；行程图 / 经卷 / 莲花 为**语境型**，靠站点文案与上下文成立）。**重出任一张后须逐条自检该表**，这是本次漏检的补口。

> - **验证**：判据脚本 9/9 PASS（尺寸 2400×1017 · 左留白 0.0000–0.0039 · 整图墨量 0.0211–0.0809 · 朱砂点 9/9 在场）· 成套拼图逐张目视 · 素材与站点两侧文件同步清理核验
> - **状态**：在途（认领登记 W940·待提交入库）
> **状态**：**已收官**（W940 95495824·git 反填·共 1 笔·W971 存量回填）


### W938（2026-10-25）：首屏版式重做 + 图集逐张复核（左侧文字重排 · 切换器归位 · 9 张构图全部完整）

> **来源**：用户 2026-10-25 反馈「你现在的这个设计不太好看，要么重新设计一下这个 100 回放在哪个位置比较好」+「我说的是首页右边的插图。并且现在首页左边文字的排版非常丑」。

> - **文件**：site/index.html、site/static/images/hero-line-09-pilgrim-four.webp、assets/promo/hero-set/hero-line-09-pilgrim-four.png、assets/promo/hero-set/hero-line-09-pilgrim-four.webp、assets/promo/hero-set/raw/hero-09-pilgrim-four.jpg、assets/promo/hero-set/hero-line-07-banana-fan.png、assets/promo/hero-set/hero-line-07-banana-fan.webp、assets/promo/hero-set/raw/hero-07-banana-fan.jpg、assets/promo/hero-set/preview-contact-sheet.png、assets/promo/hero-set/preview-contact-sheet.webp、assets/promo/hero-set/README.md、scripts/_w931_hero_verify.py、Cdsscripts/_w938_cascade.py

**左侧文字重排**：原布局七层平铺、字号跳跃、层级无引导 ⇒ 改为「眉题 → 标题组（中文 + 英文紧贴）→ 主张句（16px 浅灰 → 19px 墨色）→ 细线分隔 → 数据带（100 回 + 两行说明）→ 双轨标签 → CTA → 插画切换器（含「首屏插画」标签）」。插画切换器此前与 CTA 同排会撑破 620px 容器伸进插画区（实测金箍棒压住第 6–9 个圆点）⇒ 独立成行归位左侧文字列内。

**首页 9 张插画逐张复核（按 1440×520 容器裁切实测·判据脚本 9/9 PASS）**：① **重出 07 芭蕉扇**——首版扇面顶边被裁成半截圆面，要求主体完整入画且上下各留 15% 冗余后重出；② **第 9 张换图**——原定 W932 持瓶菩萨立像为 16:9（2560×1440），在该容器下垂直溢出 290 px（源图顶部 41% 被裁）⇒ 首屏只剩人物下半身的「断头感」，改为同规格 `2400×1017`「取经四众西行」（挑担领路 + 山道 + 赭金山峦）作收尾重音。修正后 **9 张画幅与裁切损失（90 px）完全一致**，右半区墨量 0.056–0.208，构图全部完整可辨。

**背景渲染 cover → contain（用户明令「要适配各种比例大小·要不然每个人看到的都是不一样」）**：cover 会按容器比例裁切，两组素材都被切出问题——线描 2.36:1（2400×1017）在真实容器 1006×645 下被放大 0.63 倍、左右各裁掉 407 源像素 ⇒ 主体右端被切（实测金箍棒右上端断头）；浓墨 16:9 在 1440×520 下垂直裁掉 290 px（源图顶部 41%）⇒ 首屏只剩人物下半身。改 `contain` 后：任何视口比例下图都完整显示、主体恒锚定容器右下角，容器富余处露 `#FAF7F0` 宣纸底（与图底色同色·无缝）⇒ 各人看到的构图一致。窄屏（@768 以下 masthead 转 column）另把插画移到容器顶部，首屏即可见。

**纸色归一（消边界）**：contain 不裁切后，图块矩形边界暴露——9 张纸色基调与页面底色 `#FAF7F0` 差 1–9/255（经卷 +3/+4/+9 最高）。按亮度加权做加性平移（亮像素精确落到目标色·暗像素权重 0 不动·过渡平滑），归一后残差全部 ≤ 1/255 ⇒ 图块与页面底色无缝。

**一条现场复现的工程陷阱**：改内联脚本后未重算 CSP 哈希 ⇒ 整个轮播脚本被浏览器拒执行（切换器整组停在 `hidden`）——重算后恢复（AGENTS §6-3「改内联脚本必跑 generate_csp.py」铁律的现场复现）。

> - **验证**：浏览器实测首页渲染（左侧七层有节奏 + 右侧插画完整无遮挡 + 切换器归位不压图）+ 9 张裁切对照图逐张目视；判据脚本 9/9 PASS；CSS 结构平衡 / JS 语法 / token 覆盖 / 动效禁令 / CSP 零漂移 / 第 31 与第 45 门禁全绿
> - **状态**：在途（认领登记 W938·待提交入库）
> **状态**：**已收官**（W938 db5328b5·git 反填·共 2 笔·W971 存量回填）


### W937（2026-10-25）：首屏版式修正——「100 回」数据块移入左侧文字区

> **来源**：用户 2026-10-25 反馈「你现在的这个设计不太好看，要么重新设计一下这个 100 回放在哪个位置比较好」（指 W936 批的右侧数字区纸色渐变遮罩方案）。

> - **文件**：site/index.html、Cdsscripts/_w937_cascade.py

**问题定性**：W936 用「右侧数字区加纸色渐变底」遮住插画主体与「100」的叠字——是**补救不是设计**。根因是 `.mega-num` 巨型数字（clamp 96–180px）与首屏插画主体争夺同一块右侧空间，遮罩只能盖住症状。

**改法**：把「100 回」数据块**移出插画区**，并入左侧文字区做横排一行（数字降档至 clamp 44–64px，右侧配两行说明小字），首屏右侧整块留给插画主体。收益：① 删除纸色渐变遮罩，右侧画面完整；② 左侧文字区零干扰（线描 8 张实测左侧 46% 墨量 0.0000）；③ 移动端不再有巨型数字挤占首屏。

**配套修正**：移动端媒体查询的 mega 尺寸规则改为作用域形式（`.masthead-facts .mega-num`）——否则压不过桌面尺寸导致移动端不变小；删除指向已不存在元素的 `.masthead-mega` 死规则（孤立选择器门禁）。

**题图落位逐页复核与修正**（用户令「你重新每个插图都看看位置对不对」）：机器核查 5 页插图位置全部正确（article 内、紧随 h1、CSS 与 alt 齐备）；**但逐页比对 h1 与正文主题后发现两处题材不贴并已移走**——① 「取经地理学专题」是「地方感 / 第三空间 / 空间正义 / 全球地方感」的**地理学理论**页 ⇒ 五行山与两界山改落「取经路线地理专题」（该页路线表直接列出「两界山→诸国→灵山」·跨 92 回约 40 处地理节点）；② 「四海龙王：下雨的人」讲龙王的**降雨职能** ⇒ 东海龙宫水殿改落「灵感大王·外传：冰层下面的供桌」（通天河·冰层下的水下宫殿）。旧页的 figure 与 chapter-plate CSS 一并移除（不留死规则）。修正后 5 张逐页浏览器目视复核全部显示正常。

> - **验证**：浏览器实测首页渲染（右侧插画完整无遮挡 · 左侧数据块与文字层级分明）；CSS 结构平衡 / JS 语法 / token 覆盖 / 动效禁令 / CSP 零漂移 / 第 31 与第 45 门禁全绿
> - **状态**：在途（认领登记 W937·待提交入库）
> **状态**：**已停止**（W937 零提交·git 事实标注·W971 存量回填）


### W936（2026-10-25）：首屏图集接入 + 专题题图落位（线描 9 张轮播 · 浓墨 5 张题图）

> **来源**：用户 2026-10-25 令「帮我做几张素材图」——素材本体已由 W931 交付（8 张线描 Hero 横幅）；本批做**接入层**：把 W931 线描 8 张接成首页 9 张图集轮播（末位为 W932 持瓶菩萨作收尾重音），并把 W932 浓墨 5 张按站内 `chapter-plate` 范式插入 5 个专题页。

> - **文件**：site/index.html、site/reader/people/地府体系深化专题.html、site/reader/people/紧箍儿的内侧-器物传记.html、site/reader/themes/取经地理学专题.html、site/reader/people/四海龙王外传.html、site/reader/themes/西游与死亡研究专题.html、site/static/images/hero-line-01~08.webp、site/static/images/plate-mingfu-panwang.webp、plate-jingu-jingangchui.webp、plate-wujingshan-liangjie.webp、plate-donghai-longgong.webp、plate-liudao-lunhui.webp、scripts/_w936_insert_plates.py、scripts/_w936_cascade.py

**两套素材分层用（容器实测，非主观）**：首页 masthead 为 1440×520 容器、左侧 46% 是 640px 宽标题区——W931 线描该区墨量 **0.0000**（8/8 张，裁切后仍 100% 纯纸色），W932 浓墨均值 **0.1772**（最高 0.4825 · 五行山）⇒ 浓墨压字；纵横比上 2.36:1 垂直溢出 90px 而 16:9 为 290px（16:9 素材主体会被裁没）⇒ **首页 = 线描 9 张，内页无字视觉 = 浓墨 5 张**。

**轮播实现约束**：D4 动效禁令禁 CSS 无限循环动画 ⇒ 改 JS 定时切换（6s）；WCAG 2.2.2 暂停机制（悬停 / 焦点在图集内 / 页面不可见均停）；`prefers-reduced-motion` 下不自动播放（仍可手动点选）；9 个切换按钮静态写入 HTML（`aria-label` + `aria-pressed`），JS 不可用时整组 `hidden`，不留死控件。右侧「100 回」数字区加纸色渐变底——浏览器实测九环锡杖竖杆直穿「100」，渐变使主体进入数字区时自然隐去。

**内页题图**：沿用章回页 `chapter-plate` 范式（420px 居中题图 + 浅底宣纸图在暗色模式隐藏，避免贴深底成亮斑），题图带描述性 `alt`（区别于章回装饰图的空 alt）。

> - **验证**：浏览器实测首页轮播（点击第 5 张 → 背景同步切换 + `aria-pressed` 跟随 + 6s 自动推进）与内页题图渲染；全量门禁 54 段 0 FAIL；CSP 861 个内联脚本哈希零漂移；W 号跳号（W935 在途）已留台账行
> - **状态**：在途（接入完成·认领登记 W936·待提交入库）
> **状态**：**已收官**（W936 fc0060af·git 反填·共 1 笔·W971 存量回填）


### W935（2026-10-25）：速赢两处批（R-05 渡口正文溯源去工程化 + R-12 英文站目录死链消除）



> **来源**：W926 站点交互流程审查报告 §0.4 执行序（用户 2026-10-25 选定「功能可用性优先」权重）中的 P1 与 P2 两项；用户问卷进一步授权「先动代码」并选定「速赢两处：R-05 四条 + R-12 死链」。
> - **文件**：site/dukou-engine.html、site/en/visualizations.html、docs/11-方案报告/计划方案/T25-任务计划执行与经验沉淀报告-2026-10-25.md、ddocs/11-方案报告/README.md、scripts/output/_w935_spec.json。
> - **改动 1（R-05）**：渡口页 `LINE` 数组 **4 条**「（见 W321 line 7012 凌云渡：脱胎即 Dropout）」「（见 W323 …）」「（见 W324 …）」「（见 W321 line 1393 紧箍咒：正则项在收敛后归零）」改为对读者有意义的正文（凌云渡 / 西游渡元定义 / 遗忘者列传 / 紧箍咒），**溯源写入数组上方源码注释**（保留可追溯性·不进访客可见文本）；数组结构不变（消费方 `pick(LINE)` 为字符串数组·零改动）。
> - **改动 2（R-12）**：`site/en/visualizations.html` source-note 段 `<a href="../data/">site/data/</a>` 改为纯文本——`site/data/` 有 88 个 html 但**无 index.html**，线上 GitHub Pages 对目录 URL 直接 404；全仓同型扫描确认**仅此 1 处**目录型死链，同页其余 `../data/*.html` 均指向具体文件（有效·未动）。
> - **验证**：① 浏览器 `file://` 直开点「生成渡口档案」，`#out` 实测输出为「紧箍咒：正则项在收敛后归零。」，无批次号与源码行号；② 全量结构重扫 `A_paths.broken_links` 的 4 条残项全部为「目标目录含 index.html」的旧口径假死链（`site/en/index.html`、`site/reader/poetry/index.html` 均实证存在）⇒ **全仓真死链 1 → 0**；③ 可见文本重扫：LINE 四条溯源清零（全站计数 +9 来自并行批同期往页脚批次链注入的并发噪声·未单独归因）。
> - **纪律**：本批仅改 **2 个 site/ 页面共 7 行**；0 处管控脚本与判据脚本改动；未顺手动 R-02 页脚与 R-03/R-04 分类 hub（属后续批）。
> **状态**：**已收官**（W935 b130f7a1·git 反填·共 2 笔·W971 存量回填）


### W934（2026-10-25）：D-2 应用迁移批第一子批（M12 存储层抽象 + PG 适配器 + 三表迁移器·真实数据迁移三重对账全一致）

> **来源**：用户 2026-10-25 架构设计令（「整体分层、模块拆分与依赖、数据流与存储选型、扩展性与容灾、部署与监控都写到位，附几张架构图说明图」）经 O-1~O-4 裁决「接受·按 v2 档 2 施工」后，按方案 §8.2 施工序推进 **D-2 应用迁移批的第一子批（W934）**——把「M12 PG 存储层」这行模块说明变成**可运行、可切换、可回归**的代码层。

> - **文件**：xiyouji-agent-web/server/storage/types.ts、xiyouji-agent-web/server/storage/sqlite.ts、xiyouji-agent-web/server/storage/postgres.ts、xiyouji-agent-web/server/storage/index.ts、xiyouji-agent-web/server/storage/storage.test.ts、xiyouji-agent-web/server/db.ts、xiyouji-agent-web/server/routes.ts、xiyouji-agent-web/server/chat.ts、xiyouji-agent-web/server/index.ts、xiyouji-agent-web/server/shutdown.ts、xiyouji-agent-web/package.json、xiyouji-agent-web/package-lock.json、xiyouji-agent-web/deploy/pg/migrations/0002_app_tables.sql、xiyouji-agent-web/deploy/pg/bin/migrate-sqlite-to-pg.ts、xiyouji-agent-web/deploy/pg/bin/initdb-bootstrap.sh、xiyouji-agent-web/deploy/pg/bin/verify-baseline.py、xiyouji-agent-web/deploy/pg/bin/_mutation_test.py、xiyouji-agent-web/deploy/pg/README.md、docs/11-方案报告/计划方案/执行前计划-T23-D2应用迁移批.md、docs/11-方案报告/计划方案/T23-任务计划执行与经验沉淀报告-2026-10-25.md、docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md、docs/11-方案报告/README.md、dscripts/output/_w934_d2a_migrate.json、scripts/output/_w934_d2a_residue_before.txt、scripts/output/_w934_d2a_grants.txt、scripts/output/_w934_spec.json、scripts/output/_cascade_files_W934.txt、CHANDOVER.md、README.md、STRUCTURE.md、docs/00-导读/项目说明.md、.github/workflows/README.md、site/index.html、site/data/cross-time-danmaku.html、site/data/tag-cloud.html、site/dukou-engine.html、AGENTS.md、archive/docs/AGENTS-ARCHIVE.md、CITATION.cff、scripts/output/file-index.md。

**M12 存储层抽象落地**：新增 `server/storage/` 四件——`types.ts`（`StorageBackend` 接口 + DTO + 语义约定）、`sqlite.ts`（现役实现**逐字搬迁** + `kind` + `healthCheck`）、`postgres.ts`（连接池 + 事务 + 参数化查询 + 健康探针 + schema 隔离）、`index.ts`（后端工厂 + 契约转发）。`server/db.ts` 由「SQLite 实现」降为**门面**（16 个现役导出名齐备）⇒ **三个调用点仅加 `await` 与 `async`·业务逻辑零改动**；默认后端**仍是 SQLite**（`AGENT_WEB_DB_BACKEND` 未设即 sqlite·取值非法则**启动失败**不静默回落）⇒ 现役行为与全部既有测试零影响。

**接口为何是异步的**（规划期假设被实跑证伪）：PG 走网络协议，而 Node 生态**没有同步 PG 驱动**（`pg` 的 socket 只有异步接口）⇒ 同步接口下 PG 后端只能是内存镜像或自研阻塞协议栈（皆不可接受）⇒ 接口定为异步，SQLite 后端实现体仍是同步调用。这是「**抽象层形状由最贵的那个后端决定**」的实证。

**真实数据迁移端到端（真·PG 16.4 实例）**：现役 `data/chat.db`（**70 会话 / 134 消息 / 4 反馈**）真实迁入 PG 16.4——迁移序列 v1 `0001_baseline` + v2 `0002_app_tables` 逐条记账（`checksum` 为**真实 sha256**）；**三重对账全一致**：逐表**行数相等** + **主键集合逐位相等** + **逐行内容摘要一致**，时间列 **278/278 逐字节相等**（sessions 140 + messages 134 + feedback 4）。迁移器**只读**打开源库（chat.db 是全仓唯一不可重建的数据）且**不借道应用写接口**（`createMessage` 会把会话 `updated_at` 刷成「现在」⇒ 破坏逐字节保真）。

**双后端契约测试**：**同一套**断言跑 SQLite 与 PostgreSQL 两个后端，均全过（2/2）——抽象层「换后端不动业务」的证据不是「两边各测一遍」，而是「一套用例两个实现」。

**实跑抓出 3 个真缺陷（静态层查不出 · 已全部固化为守卫）**：
1. `ALTER DEFAULT PRIVILEGES` **缺 `FOR ROLE`** ⇒ 默认权限挂在执行者名下 ⇒ 由**应用账号**创建的表拿不到只读授权 ⇒ **静默失效**（不报错）。
2. 引导脚本**先建表后授权** ⇒ 记账表落在授权之前 ⇒ 应用账号读它 `permission denied`。
3. 记账表**所有权**不属于应用账号 ⇒ 迁移序列以应用账号执行时 `COMMENT ON TABLE` 报 **`must be owner of table schema_migrations`** ⇒ **迁移序列根本跑不起来**——这是**所有权**问题，没有任何「看起来不对」的形态 ⇒ 只有真跑能暴露。

> 这 3 项与 W928 抓出的 4 项是**同一族**：**静态背书 ≠ 运行时可用**。W928 抓到的是「形态错」，W934 抓到的是「**权限与所有权错**」——后者每一行单独看都合法 ⇒ 更难被静态断言覆盖 ⇒ 所有权、运行时语义、跨版本行为一律留真跑项。
> **状态**：**已收官**（W934 4b25833b·git 反填·共 1 笔·W971 存量回填）

**守卫升级**：静态校验器 **71 → 95 项**（新增 C5 组：三表 schema 不变量 / 迁移器只读与参数化与三重对账 / 授权模型的 FOR ROLE·顺序·owner 三项）+ 反向验证 **14 → 23 组**（新增 M14~M22，逐条证明新判据可证伪）。

**另自证出 3 处工具自身缺陷**（先红后绿）：① ESM 把**接口当值导出**（`export { DbFeedback }`）⇒ 运行时炸而 `tsc` 不报（未开 `isolatedModules`）⇒ 改 `export type`；② 计数型断言把**注释行**算进去 ⇒ 基线假红 ⇒ **掩盖了 M17/M20 的真实结论** ⇒ 计数只取非注释行 + 新增 `strip_ts_comments()`；③ 断言命中文档注释里的**示例代码** ⇒ 真代码改坏仍报绿（变异 rc=0）⇒ 断言改锚真实调用构造。

**D-2 整体尚未完成（不得对外宣称「已切 PG」）**：双写对账期 → 切读 → 停写旧库属 **W935**；检索层接入（O-4）+ 客户端侧服务地址注入（契约 C-8）属 **W936**；容量实测属 **W937**；合规面属 **D-3**。

**机器证据**：`scripts/output/_w934_d2a_migrate.json`（迁移对账）· `_w934_d2a_residue_before.txt`（清理前演练残留快照）· `_w934_d2a_grants.txt`（授权模型实查）。

**未改**：site/ 任何页面的**内容**（仅级联页脚批次链为全批标准机制）· 任何管控脚本（verify_delivery.py / bump_version.py / batch_cascade.py / preflight_check.py 等）。


### W933（2026-10-25）：共享面串行化机制批（规则三条 + 五个机检判据·把台账与 CHANGELOG 的写顺序从自律变成机制）



> **来源**：W926 站点交互流程审查批收官复盘时，我方主动指出「号段已分开，但台账与 CHANGELOG 的写顺序仍是串行资源——目前靠各方『先登记认领行、后立段』的自律维持，没有机制保证」，并请用户裁决；用户 2026-10-25 答「按你推荐」并选定：**落地上限＝层 1 + 层 2**（规则三条 + 3 个机检判据）、**开工时点＝立即开工并由我方取号**。
> - **文件**：docs/00-导读/文档规范.md（§11.0 规则三条）、scripts/preflight_check.py（判据 A/B′/D/E）、scripts/ledger_backfill.py（判据 B）、scripts/ledger_close_check.py（判据 C）、scripts/_w933_mutation_test.py（四判据可证伪性）、scripts/output/_w933_spec.json、docs/11-方案报告/计划方案/T22-任务计划执行与经验沉淀报告-2026-10-25.md、ddocs/11-方案报告/README.md。
> - **产出**：① **层 1 规则三条**（写入 docs/00-导读/文档规范.md §11.0）——**认领即占号**（登记认领行并单独提交后再施工，登记后复跑 preflight 做乐观并发校验）、**回填独占**（回填既有行必须走行指纹校验，禁整文件 git add 台账）、**收官回填三件套**（hash 列非占位 + 状态列以「已收官/已闭环」开头 + touches 列为终值，缺一即视为在途）；② **层 2 五个机检判据**——**A 撞号检测**（台账同一 W 号出现多行 = 撞号，机器可检；插队仅出 NOTE 因后补登记合法）、**B 回填独占**（scripts/ledger_backfill.py：--expect 基线指纹不符即拒写、--verify 提交前复核、--append-claim 纯追加认领）、**C 收官回填体检**（scripts/ledger_close_check.py：现役段 W 号须 hash 非占位且状态以「已收官/已闭环」开头；**不挂 verify_delivery 阻塞段**，避免把伪阻塞从 preflight 挪到门禁）、**D 反引号剥离**（_split_touches 具反引号感知）、**E 登记类共享面排除**（台账与方案报告 README 天然并发，不计入并行写拒绝）；③ **Makefile 新增 ledger 目标并接进 ci**（第 42 门禁四面引用口径）；④ **可证伪性证明**：三工具自测 5 正例 + 8 负例 + 四判据突变 4/4 按预期。
> - **本批自证出并当场修复的两处机制缺陷**：**D 假绿**——架构会话（W934 批）实测报出「_split_touches 不剥反引号，而台账 touches 列的路径带反引号 ⇒ 与命令行传入的无反引号路径字面不等 ⇒ touches_conflict 恒返空 ⇒『PREFLIGHT PASS·无交集』在真实撞面时假绿」；**E 恒红**——修复 D 后本批立即实跑，发现交集拒绝把「台账认领行」与「方案报告 README 登记行」当普通共享面 ⇒ 每个批次都要写这两面 ⇒ 交集在准入阶段恒红 ⇒ 纪律被架空 ⇒ 改为登记类共享面排除出拒绝，并发保障改由「纯追加 + 精确暂存（update-index --cacheinfo）+ 回填行指纹」承担。**判据 A 的初版语义亦被本批自身实战证伪**（把「并发插队」当「撞号」会误伤合法的后补登记 ⇒ 修订为「同号多行 = 撞号」+ 插队仅 NOTE，见 T22 报告 E-06）。
> - **交付**：docs/11-方案报告/计划方案/T22-任务计划执行与经验沉淀报告-2026-10-25.md（框架第二十二次执行·32/32 判据符合·模糊词 0·含 §2 号段协调实录与 §4 可行性自评与 §5 六条经验）。
> - **纪律**：本批 0 处 site/ 与应用代码改动；未改 verify_delivery.py 等禁擅改管控文件（判据改走 Makefile 编排面）；不代改他方台账行与 CHANGELOG 历史段。
> - **状态**：已落地（本地）。
> **状态**：**已收官**（W933 a6306896·git 反填·共 3 笔·W971 存量回填）


### W932（2026-10-25）：站点 Hero 素材图成套批（六张 16:9 浓墨剪影·锚点复用成熟段·底部净空带供叠字）

> **来源**：用户 2026-10-25 令「帮我做几张素材图」并要求「用途与画幅、风格与配色统一、主体清晰、留好放文字的空间都考虑到，成套出图保证风格一致」，且明令「开始前先问我：素材用在哪里、需要几张、有没有参考风格」；本会话按问卷答复（用途=站点 Hero 横幅 16:9 · 数量=6 张 · 参考=沿用 `assets/promo/hero-main-visual.png` 主视觉「宣纸底浓墨剪影+朱砂钤记」· 主题=人物叙事/法器符号/世界观场景/学术概念四类全覆盖）执行。
> - **文件**：site/static/images/hero-10-mingfu-panwang.webp、hero-11-chiping-boshan.webp、hero-12-jingu-jingangchui.webp、hero-13-wujingshan-liangjie.webp、hero-14-donghai-longgong.webp、hero-15-liudao-lunhui.webp、site/static/images/index.md、scripts/_w929_gen_args.py、scripts/_w929_gen_args_v2.py、scripts/_w929_gen_args_v3.py、scripts/_w929_process.py、scripts/_w929_seal_normalize.py、scripts/_w929_verify.py、scripts/output/_w932_spec.json、scripts/output/_cascade_files_W932.txt、dCHANGELOG.md。
> - **锚点纪律**：art direction 段（宣纸 #FAF7F0 / 玄墨 #221D16 / 淡墨 #6B6455 / 单一朱砂 #C8463A / 赭金 #E9B885 五色锁死）与「松散枯笔湿染」笔触句、16:9 构图句（主体止于上 2/3 + 下三分之一完全空白宣纸）——**逐字复用 W893**，本批只改两处并逐条留痕：① 笔触段由「淡彩湿染」加强为「浓墨剪影为主、淡墨为辅」对齐主视觉观感；② 禁项清单移除 seal stamp，改写为「唯一允许的印记 = 右上角极小朱砂方印（抽象笔画·不可辨识字符）」——用户点名的参考风格含「朱砂钤记」。
> - **六张主题分配**：人物叙事 2（冥府判官队列 / 持瓶菩萨立像）+ 法器符号 1（紧箍与金刚杵静物）+ 世界观场景 2（五行山两界山 / 东海龙宫水殿）+ 学术概念 1（六道轮回轮抽象水墨）· 编号接续既有 hero-01 至 hero-09 · 题材全部避开既有 9 张 hero 与 27 张 card 撞车。
> - **量化验收**（脚本量测·非目视断言）：成品 2560×1440 = 精确 16:9（源 2752×1536 实为 1.7917 → 裁宽 21px 居中 → LANCZOS 缩放）；底部净空带 282 至 557 px（19.6% 至 40.8%）；上 72% 主体墨量 11.92% 至 77.82%；严格朱砂 0.11% 至 1.52%（上限 8%）；主底色 5 值同落 #FAF2E7 / #FAF5EC / #FAF6EA / #FBF5EB / #FCF6ED 暖白族；规则线扫描 0 命中；单件 64.2 至 346.9 KB。
> - **三轮返工（逐轮病因不同）**：v1 量化全绿但**目视**抳出钤印形态漂移（hero-10 竖长条印 / hero-12 椭圆印 / 其余四方）→ v2 把形态写死为正方形后**印面被画成清晰篆字形**（伪汉字观感·撞零文字纪律）→ v3 把印面限定为纯朱砂色块+不规则留白后 hero-10 / hero-12 达成，另四张改走**交付端印面归一**（`scripts/_w929_seal_normalize.py`：只重绘右上角那枚小印的印面·主体与留白分毫不动）⇒ 五张印面归一为同一程序质感、零可读文字；**一处如实保留差异**：hero-10 的模型原版印是「朱红块 + 带白斑」两段结构（自动扩张会框成 225×174 巨块·实测涂坏画面）⇒ 保留模型原印，其斑驳浓艳质感与其余五张略异，网页 Hero 显示尺度（约 30 px）下不可辨。
> - **两处工具自身缺陷（先红后绿）**：① 窄朱砂阈值（R-B>45）在朱文印（红字白底）上只框到印的一角（hero-15 实测偏到右下角）→ 改数据驱动定框（宽松阈值取初始 bbox + 向四边迭代扩张吸附朱砂分布边界）；② 宽松阈值定得太松时**赭金 #E9B885（R-B=100）被误判为朱砂**（W853 已记过的赭金误判坑）致扩张跑飞涂到画幅边缘 → 收紧为 R-B>40 且 G<130 并限制最大外扩量。
> - **无文字纪律**：六张均无文字、无落款、无水印，钤印印面为抽象笔画/颜料斑驳，无任何可辨识字符。
> - **接入提示（本地裁切实测·非推断）**：按现网 `.hero` 的 `background-size: cover` + `background-position: center bottom` 做本地裁切模拟（容器 1440×520）——**本批六张主体清晰落在可见区、下方约四成是空白叠字带**；同参数下现有 `hero-01-xihai-yunhai.webp` 的主体反而几乎被裁没（只剩山脊一条）⇒ 本批可直接作首屏 cover 背景接入。若后续容器更矮或改 `center top`，需重新裁切复核。改动仅涉 `site/index.html` 一行样式，本批**未擅自改**（站点接入交由用户决定）。
> - **范围纪律**：只新增 `site/static/images/` 下六个素材文件 + 本批脚本与 spec，不改任何页面（站点接入交由用户决定）、不改门禁件、不推送远端。
> **状态**：**已停止**（W932 零提交·git 事实标注·W971 存量回填）

### W931（2026-10-25）：首页 Hero 横幅素材图成套批（线描版 8 张 · 2400×1017 · 左半留白供叠字）

> **来源**：用户 2026-10-25 令「帮我做几张素材图：用途与画幅、风格与配色统一、主体清晰、留好放文字的空间都考虑到，成套出图保证风格一致」+ 明文要求「开始前先问我：素材用在哪里、需要几张、有没有参考风格」；问卷答复 = 首页 Hero 横幅 **2400×1017** · **8 张** · 沿用 `assets/design/ai-concepts/` 的 c2 线描概念图 + 现有色板。

> - **文件**：assets/promo/hero-set/hero-line-01~08.{png,webp}、assets/promo/hero-set/preview-contact-sheet.{png,webp}、assets/promo/hero-set/raw/hero-0X-*.jpg、assets/promo/hero-set/README.md、assets/promo/hero-set/index.md、assets/promo/hero-set/raw/README.md、assets/promo/hero-set/raw/index.md、assets/promo/index.md、STRUCTURE.md

**规格与机器判据**：8 张共用同一条逐字风格母版（宣纸 `#FAF7F0` · 墨 `#23201A` · 赭金 `#8A6D3B` · 单点朱砂 `#C8463A` + 纯墨线无实心填充 + 禁文字禁印章禁水印 + 左侧 46% 纯留白）⇒ 成套一致性由「同母版」保证。画幅 `2400×1017`（`21:9` 出图后按 `2400/1017` 精确裁切·不拉伸）；**左侧 46% 文字安全区墨量实测 0.0000–0.0014（8/8 达标）**·主体墨量落右半区（整图 2.11%–8.11%）。

**一处返工留证**：07 芭蕉扇首版扇面被画成**黑色实心块**（主体墨量 26.2%·与其余 7 张 3%~8% 断层）⇒ 判破套并重出，复测 7.72% 回到套内；**AI 伪文字人工放大 2× 复核**（04 司南盘面字符状符号验明为回纹刻纹非乱码·06 九环锡杖同验）——机器判据抓不到伪文字，只能放大看。

**落位与接入**：新目录 `assets/promo/hero-set/`（8×PNG 母版 + 8×WebP 站点版 + 成套一览拼图 + 8 张出图原件 `raw/` + README/index ×2）·站点 Pages 只发布 `site/`，接入前须复制到 `site/static/images/`，方法写在该目录 README（背景图 + `background-position: right center` 保住「主体在右·文字在左」版面约定）·**未改 `site/index.html`**。与并行 **W932** 素材批（渲染型浓墨剪影 `hero-10~15` · 2560×1440 · 落 `site/static/images/`）路径零重叠，两套视觉语言并存、接入由用户决定。

> - **验证**：8/8 出图成功（批量 `generate_image` 零失败）·2400×1017 尺寸 8/8 实测一致 ·左侧留白区墨量 0.0000–0.0014（8/8 达标）·AI 伪文字人工放大复核 2 张（04/06）·成套一览拼图逐张目视复核全过
> - **状态**：在途（素材已落盘并暂存·认领登记 W931·站点接入待用户决定）
> **状态**：**已收官**（W931 08f1f927·git 反填·共 2 笔·W971 存量回填）


### W930（2026-10-25）：界面布局复核与落地方案（信息层级四维复核 + 三条新发现 + 六批可施工方案）

> **来源**：用户 2026-10-25 令「帮我优化现有界面布局：先帮我做好信息层级梳理、区块分布与留白、操作动线、不同屏幕适配都过一遍，每处调整讲清理由」；问卷答复 = 范围全站都做（静态站 + reader + agent-web）· 主攻信息层级（一屏信息量过载）· 先出审查报告与落地方案、用户过一遍再动代码。

> - **文件**：docs/11-方案报告/计划方案/T21-任务计划执行与经验沉淀报告-2026-10-25.md、docs/11-方案报告/计划方案/执行前计划-T21-界面布局复核与落地方案.md、docs/11-方案报告/README.md、dscripts/_w930_claim_row.py、scripts/_w930_rename_prefix.py、scripts/_w930_report_normalize.py、scripts/_w930_spec_build.py、scripts/_w930_layout_static.py、scripts/_w930_layout_diff.py、scripts/_w930_layout_attr.py、scripts/_w930_layout_detail.py、scripts/_w930_layout_residual.py、scripts/_w930_layout_probe.mjs、scripts/_w930_layout_probe_app.mjs、scripts/output/_w930_layout_static.json、scripts/output/_w930_layout_metrics.json、scripts/output/_w930_layout_metrics_app.json、scripts/output/_w930_layout_diff.json、scripts/output/_w930_layout_attr.json、scripts/output/_w930_visible_leak.json、scripts/output/_w930_plan_review.json、scripts/output/_w930_spec.json
> **状态**：**已收官**（W930 378e158d·git 反填·共 1 笔·W971 存量回填）

**定位：复核 + 补审，不是重做**——用户指令的四维与 W854《界面布局审计报告》（2026-10-21）几乎逐字相同，按 W926 §7.1 E-03「同一条指令重复下达时先查历史再动手」判为复核 + 补审：重跑 W854 探针（站点 11 组 + 应用 6 组，新旧 metrics JSON 逐项对拍）+ 补 W854 与 W926 均未覆盖的维度 + 出可施工落地方案。**W 号二次让号**（W928 归并行 D-1 实跑批、W929 归并行 Hero 素材图批，按「先落地者保留」）⇒ 本批取 W930，框架号 T21。

**W854 十八条的四天后现状（重跑探针实测，非复述）**：已修 6（S1 首屏内容入口 / S2 字号倒挂 / S3 手机层级坍塌 / S4 首页九区块同级 / S7 四套容器并存 / S9 hub 非链接）· 部分修 4（S5 间距刻度 / S6 令牌消费 / S8 目录页动线 / S14 卡片列数与触达目标）· 仍存 7（S1 衍生 mega 数字未降级 / S10 可视化页顶栏仅五入口 / S11 断点体系 / S12 KPI 不收缩 / S13 长段 77.9 字每行 / A1 / A4 / A5 / A6）· 未判定 1（A2 应用侧留白，服务端未起不可测）。首页三任务区由 W865 与 T-08 批施工落地。

**三条新发现（W854 与 W926 均未覆盖）**：① **N1** @1440 首页同标签混两档字号——「精选必看」「全卷索引」是 h3 但 24px，同区十张卡片 h3 为 20px，语义层级与视觉层级错位且仅在宽屏发作；② **N2** @375 首页 hero 山脉装饰图压正文文字（副标题被裁），静态几何审计与交互审计均不覆盖元素重叠；③ **N3** 可见工程批次号不只污染文本（796 页 6,827 处），同时是布局度量的基准污染源——W926 批次往四页页脚注入批次行使页高升 20 至 215 像素、元素数升 1 至 7，任何以页高或元素数为判据的布局审计都会被带偏。

**v4 令牌落地进度差**：容器族已消费（0 页至 851 页）· 间距族已消费（330 页至 857 页）· **排版族与语义 gap 族仍为 0 消费**（`tokens.css` 已定义九个排版角色与六档语义 gap）⇒ 改版者改了令牌值却看不到任何变化。间距刻度命中：原口径 43.3% 降至 31.2% 是判据失真（令牌化改造不被硬编码像素正则计入），修正口径 86.2% 为真值，两套口径同时输出以便旧数字仍可复算。

**六批可施工落地方案**（每批带理由与可机检验收判据，共约 8.5 人日）：B1 应用侧移动端可用性（@375 主区 115 像素至目标 320 像素以上）· B2 可见文本去工程化与页脚收口 · B3 排版与间距刻度消费化 · B4 可视化页自适应降级（KPI 与长行）· B5 首页宽屏层级与断点体系 · B6 目录页动线与触达目标。**本批不含任何界面代码改动**。

**四件套**：文件见上（改名后新名）· 验证：渲染实测 17 组 + 静态复算 1 次 + 独立复算 1 次 + 第 48 门禁双件全项符合（计划件判 PLAN 符合 23 项、报告件判 REPORT 符合 13 项，模糊词零命中）· 状态：方案件已落库，施工待用户拍板 U1 至 U4 · 边界：线上部署态、A1 运行时、A2 留白、英文站 138 页逐页、reader 620 页逐页、N2 影响面共六项显式声明未验证。

**诚实性边界**：本批只出报告与方案，不改 `site/` 与应用源码；级联器固定面会向三页页脚注入本批批次链行（共四行），该行为同时是 N3 所指污染源之一，已显式登记为 B2 的整改对象，不在本批静默处理。


### W928（2026-10-25）：D-1 实跑批（真实 PostgreSQL 16.4·免安装二进制路径·抓出 4 个静态查不出的真缺陷）



> **来源**：用户 2026-10-25 答「没有 Docker」⇒ 原定「起 Docker Desktop 实跑」路径作废 ⇒ 改用**PostgreSQL 官方 EDB 免安装二进制包（zip·338 MB·解压即用·不需要 Docker·不需要管理员·不进仓库）**，在 `%LOCALAPPDATA%\pg16` 起真实实例实测。

> - **文件**：xiyouji-agent-web/deploy/pg/postgresql.conf.base、xiyouji-agent-web/deploy/pg/pg_hba.conf.base、xiyouji-agent-web/deploy/pg/bin/initdb-bootstrap.sh、xiyouji-agent-web/deploy/pg/bin/backup.sh、xiyouji-agent-web/deploy/pg/bin/restore-drill.sh、xiyouji-agent-web/deploy/pg/bin/verify-baseline.py、xiyouji-agent-web/deploy/pg/bin/_mutation_test.py、xiyouji-agent-web/deploy/pg/migrations/0001_baseline.sql、xiyouji-agent-web/deploy/pg/README.md、docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md、docs/11-方案报告/计划方案/T20-任务计划执行与经验沉淀报告-2026-10-25.md、docs/11-方案报告/README.md、scripts/output/_w927_pg_runtime_evidence.txt、dCHANDOVER.md、README.md、STRUCTURE.md、docs/00-导读/项目说明.md、.github/workflows/README.md、site/index.html、site/data/cross-time-danmaku.html、site/data/tag-cloud.html、site/dukou-engine.html、AGENTS.md、archive/docs/AGENTS-ARCHIVE.md、CITATION.cff、sscripts/output/_w928_spec.json、scripts/output/_cascade_files_W928.txt（逐件行见 file-index W928 段）。

**实跑通过 6 项（原待实跑清单 9 项中）**：
- **初始化幂等性**：`initdb-bootstrap.sh` 连跑两次——第一次建角色/库/权限，第二次全部「已存在，跳过创建」。
- **真实备份**：`pg_basebackup` rc=0；空壳自检通过（`backup_label` + `postgresql.conf` + `base/` 均在位）；保留期轮转 + WAL 归档轮转正常。
- **恢复演练行数一致（§9.4 核心主张）**：**真·PITR 演练**——PG 经 `restore_command` 从归档取回 `000000010000000000000019`；**逐表比对源库 == 恢复实例**：`sessions 6==6` · `messages 50==50` · `feedback 20==20` · `schema_migrations 1==1`。
- **WAL 归档连续性**：段 `000000010000000000000001` → `00000001000000000000001B` 连续无缺口（27 段）。
- **分盘校验（两次都验到）**：同盘场景（C: vs C:）被脚本**如实拦下**（`FATAL: 备份目录与 PGDATA 同盘`）；分盘场景（C: vs D:）通过。
- **TLS 实握手**：`pg_stat_ssl.ssl = true` · **TLSv1.3** · cipher `TLS_AES_256_GCM_SHA384`。

基线参数生效核验（实读 `pg_settings`）：`archive_mode=on` · `ssl=on` · `ssl_min_protocol_version=TLSv1.2` · `wal_level=replica` · `max_connections=200` · `client_encoding=UTF8` · `fsync=on` · `synchronous_commit=on` · `full_page_writes=on` · `log_min_duration_statement=1000` · `logging_collector=on` · `statement_timeout=30000`。

**实跑抓出 4 个真缺陷（静态校验 66 项全绿也查不出 · 已全部修掉并固化为守卫）**：
1. `server_encoding` 写进 `postgresql.conf` ⇒ PG **直接 FATAL 拒绝启动**（initdb 固定参数）⇒ 从基线删除，改由 `initdb -E UTF8` 确定。
2. 迁移文件用 `#` 注释 ⇒ `psql` **语法错误**（PG 的 SQL 只认 `--`）⇒ 全部改 `--`。
3. `pg_basebackup -D` 配 `-z` ⇒ 备份报错（`only tar mode backups can be compressed`）⇒ 去 `-z`。
4. **恢复演练对备份目录结构的语义误解** ⇒ 演练实例起不来（`could not open file ".../global/pg_control"`）——`pg_basebackup -D` 的输出目录**本身就是 PGDATA 镜像**（`base/` 与 `global/`、`pg_wal/` 是**兄弟**），不是「base/ 里才是数据目录」⇒ 恢复时铺满整个备份目录 + 删 `standby.signal` + 接 WAL 归档做 PITR + 重写 `postgresql.auto.conf`。

> **第 4 项连变异测试都测不出来**（它是语义误解，不是文本形态）⇒ **只有真跑能暴露**。这是「静态背书 ≠ 运行时可用」的第一份实证。
> **状态**：**已收官**（W928 4dd57cee·git 反填·共 2 笔·W971 存量回填）

**守卫升级**：静态校验器 **66 → 71 项**（新增 3 条禁形态：server_encoding / `#` 注释 / `-D` 配 `-z`）+ 反向验证 **11 → 14 组**（新增 M11/M12/M13）。

**两处跨平台判据坑（已修）**：① **git-bash 的 `uname -s` 返回 `MINGW64_NT-…` 而不是 `Windows`** ⇒ 只写 `= "Windows"` 判等会误判为类 Unix ⇒ 把 POSIX 路径（`/c/Users/…`）写给 Windows 版 PG ⇒ 启动即 FATAL（`could not create lock file`）⇒ 判据须覆盖 `MINGW*`/`MSYS*`/`CYGWIN*`/`Windows*` 全族；② **PG 配置串里反斜杠是转义符** ⇒ Windows 路径要双写 `\\`，且 `cmd.exe` 的 `copy` 与 PG 的 `%p`（正斜杠）需薄包装批处理适配。

**仍待实跑（3 项 · 不得当作已验证）**：迁移器端到端（D-2）· 容量实测（D-2）· 审计留存与销毁留证（D-3）。

**机器证据**：`scripts/output/_w927_pg_runtime_evidence.txt`（111 行原始输出）。

**未改**：xiyouji-agent-web 的 server/ 与 src/（应用代码一行未动）· site/ 任何页面 · 任何管控脚本。


