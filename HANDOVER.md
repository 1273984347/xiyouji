# 交接文档


> **📖 阅读契约（W707）**：首段型+查表型——接手时只读「零、当前阻塞」+「一、当前进度」+ 文件末尾「最后更新」链；「三、方法论沉淀」「四、待办」按需查；历史批次细节在 CHANGELOG（grep 查）勿在本文件找。
> **🚪 新 Agent 必读三件套（W1025）**：① 本文件（当前状态与阻塞）② [docs/agent/pitfalls.md](docs/agent/pitfalls.md)（267 条坑·六主题——**只读前 10 条高频也强于不读**：W1019–W1024 六批踩的坑有 11 条属这里已写过的形态）③ [docs/agent/gates.md](docs/agent/gates.md)（57 槽判据）。三件之外按需再查；交接/审查/收官各有一份模板见 `docs/agent/`。
> 轨标：教学讲解
> 本文件用于跨 session 交接，记录当前进度、下一步可推进方向、方法论沉淀与待办事项。
> 创建于 2026-07-25（v2.0.41 W068 后）
> 最后更新：2026-11-04（W1128 收官链 py_compile 语法自检门禁）·2026-11-04（W1124 治理收尾批：教训入坑表 + 重建入口收进收官链 + 滚动幂等守卫）·2026-11-04（W1123 预约释放语义根修 + 提交范围门禁 merge 场景归属根修）·（W1063 及更早批次详见 CHANGELOG.md）
> 与 [CHANGELOG.md](CHANGELOG.md)（变更日志）/ [STRUCTURE.md](STRUCTURE.md)（目录结构）/ [README.md](README.md)（项目说明）/ [docs/00-导读/项目说明.md](docs/00-导读/项目说明.md)（项目状态）配套使用。
> **维护契约（防乱写）**：本文件是项目进度中枢，只允许结构性编辑——① 保持「零 / 一 / 二 / 三」四段骨架不变；②「最后更新」行只写最新 1–3 批摘要（每批 ≤ 1 行），**禁止把历史批次堆进该行**（历史已归档 / 在 CHANGELOG）；③ 每批详细记录只写 CHANGELOG + 归档（历史段禁改）；④ 任何「当前 HEAD / 当前版本」表述必须与 `git rev-parse --short HEAD` 核对后更新；⑤ 本文件是状态快照，与 CHANGELOG（时间线）冲突时以 CHANGELOG 为准。
> **历史归档**：v2.0.39-v2.2.49（W066-W280）段的详细进度记录已迁移至 [archive/docs/HANDOVER-ARCHIVE.md](archive/docs/HANDOVER-ARCHIVE.md)。本文件仅保留 v2.2.50+（W277）现役记录与全局概要。



---



## ⚠️ 零、当前阻塞（接手必读）



**原唯一长期阻塞「档 B 真实生成需 LLM_API_KEY」已于 W402 解除**（provider 化 Base URL·渡口问津生成式问答·LLM_API_KEY 配于本地 .env 已 gitignore）。**访问数据基线已接入（W403·localStorage 自建·仅本浏览器可见）**，**S2 分发完成（W404 精选 27 篇发布版 + 合集页 curated.html + W405 第二批 27 篇随笔发布版·44 篇随笔全发布）**，**GoatCounter 已接入并完成自托管修复（W425 注册接入 + W426 gc.zgo.at 大陆 DNS 污染 → count.js 本地自托管·计数回传 goatcounter.com·线上实测 HTTP 200）**；**真实跨访客读者量仍待回传验证**（部署生效后观察后台数据）；有流量则继续分发（S4 学术投稿等），无流量则停止内容生产。另存在平行入口 `xiyouji-agent-web`（OpenAI-compatible 自研引擎·引擎三键配于服务端 .env·W680 起·`PROJECT_CWD`=仓库根（自动解析·W596）直接对话/检索/跑脚本），与 scripts/rag 档B 二选一或并行。**安全审计 P0-1/P1-1 已处置（W411）**：Web Agent 默认权限改 acceptEdits + 可选 AGENT_WEB_TOKEN 认证 + 权限/工作目录白名单 + 仅回环监听 127.0.0.1·MCP 4 工具路径白名单拒越界。**安全审计剩余项已处置（W412）**：P0-2 禁运行时覆盖引擎凭证/端点键（前端表单移除·仅服务端 .env·W680 起=LLM_* 三键）·P1-2 静态站 XSS 转义 6 页·P2 RAG 参数钳制/LLM 端点校验/SSE 超时与断开清理/DOMPurify 消毒/依赖锁定·P3 日志收敛/CORS 白名单/死代码/版本漂移；密钥吊销轮换需用户在 DeepSeek 控制台操作（P1-3 仅告知）。**W424 对抗性审查修正与全仓整理已处置**：A4 门禁校准 209（verify EXPECT_A4 201→209）·3D 页 defer 修复·EN 页 Ch. 腐蚀修复·security 依赖审计修复（只扫仓库 requirements.txt·high 103→0）·新Agent启动Prompt/workflows README/DESIGN 同步·全仓清理（截图 416MB + 过期报告 14 + 原始审计 JSON 4）·RAG 索引重建。**W424 SRI/CSP 已处置**：95 外部脚本标签 SRI（SHA-384）·159 页 meta CSP（680 内联脚本哈希·script-src-attr none）·EN 腐蚀第二波（""X"" 32 处 + 反引号 4 处）·6 页 sankey 漏引修复·复盘沉淀批次（腐蚀/插件引用门禁 + 方法论新增 + 内容同步）。**W417 文档健康治理已处置**：CHANGELOG/file-index/交接文档归档精简降达标·verify_delivery 新增 A1-A6 真实计数校验（611==611）·actions 升级消除 Node 20 deprecation·RAG 索引重建演练通过·bump_version 增强（--desc/W 范围锚点/页脚同步）·LICENSE 双协议边界补强·sitemap 补全 154 页。**W418 内容质量深化已处置**：全站死链巡检（site/en/ 29 broken 链接修复——EN 版存在指向同目录/无 EN 版回退中文原版 ../data/*.html 加 lang="zh-CN" 标注·docs/ 全量 4784 链接 0 broken）+ A1 逐回解读 23 回补 `> 导航：` 引用行（100 回导航全覆盖 100/100）。**W419 修复 A1 深度解读 SD 错位已处置**：22 篇 SD（SD038-052/056-062）编号≠真实回号归位（根因 W286 合并脚本只读源第一行·元数据在第三行→fallback 按编号放置）·按正文真实回号范围式复制 40-72 回全覆盖（原 63-72 十连回空白消除）·源文件 24 篇元数据/H1/正文内嵌/关联行修正·第 56 回补写 SD101。**W420 A1 内容质量深化已处置**：A1 深度解读 100/100 补全（第038/039回新增 SD102/SD103·source 切片 101→103）+ 56 回「对应原著/数据指标」结构化元数据补齐 + 99 回导航上一回/下一回错链修复（此前约 60 回指向非相邻回）+ 10 回 sd-crossref 关联块死链修复（66 处·docs/01 1715 链接 0 broken）。**W421 Screenshot Review 提速优化已处置**：screenshot-review.yml 新增改动范围判定（页脚/文档-only 跳过·site/data 变更定向截图·static/脚本/workflow 变更全量·schedule/dispatch 全量）+ batch_screenshots.js --only-pages 定向截图 + Playwright 浏览器缓存 + checkout fetch-depth 0。**W422 全量治理已处置**：perf.yml 补 push 触发（LHCI 预算门禁首次在真实发布路径运行）·verify_delivery 新增 4 项门禁（A1 导航相邻性/docs/01 链接/sitemap 覆盖/site/data 回退模式）·文档健康归档（CHANGELOG 83 行·file-index 127 行·交接文档 556 行）·双索引规则校准（新文档执行 + 存量以 file-index 追溯）·README 命令修正 + JS 检查进 CI·认知总览计数校准（756/611/211/209）·Dependabot/mypy report-only/a11y 口径/artifact 瘦身/_DEBRIS 清理。**W459 V2 审查收尾已处置**：D2 回目跳转死链修复（方案错误约定 `第NNN回-回目摘要.md` → A1_DOC_MAP 内嵌 100 条真实文件名映射·路径深度 ../→../../）+ check_dynamic_links.py 动态链接门禁挂 verify_delivery（补 lint_links 静态盲区·首跑抓出 tag-cloud dashboard 死链 + EN source_doc 虚构路径并同批修复）+ V2 方案文档回写 + 首页精选补 geo-3d 入口；W456-W458 积压改动同批基线提交（de8047a）。当前 HEAD = W1128（py_compile 语法自检门禁入收官链 · 负样本实测拦停 · 计数链不动；详见 CHANGELOG）。

**冻结适用范围（W793 立·单一权威表述）**：内容扩容维持 W626 归档裁决冻结（2026-09-30 起判归档；**2026-10-27 重判=中间态**——账号 10-01 重启、数据链恢复、30 日 UV=78，归档线已脱离但分发线 200 未达·W793 二选一维持；详见 docs/11-方案报告/调研与数据复盘/读者数据复盘.md W981 订正注）；已点名解冻项（WP-D2/E、B-5/B-6 第二步、B-7）均已全部收官，不再另议；工程/治理/门禁批不受限（W626 原文即「仅推进 P0/P1 工程批」）；新增内容扩容批须二选一：**用户点名**，或 **judge_gate 重判为「继续分发」**（30 日 UV≥30）。
## 一、当前进度（W1128 收官链新增 pycompile 步 三态清单的改动 .py 逐件 compile 只编译不落盘 任一 SyntaxError 即中止整链 fail-closed + 负样本实测拦停 + 顺序锁行为锁同步 + 不新增坑表条目 计数链不动；更早批次详见 CHANGELOG.md）
- **图表色工程批·档 3 原型验证批（读令牌喂图表 + J2 双态取证）**：
  - 机理验证：站内图表为自研 D3 + 自绘 SVG，色值经 CSS 变量中转 ⇒ 常量内调色板 hex 可直写 var(--chart-N)
  - 改动面：两页四常量中 15 处令牌化，其余 9 处登记去向待铺开批处理
  - 取证读数：浅色态 0 差异 · 暗色态 24 处差异全为同向颜色转换 · 元素数零损失（750 → 751 / 749）· 非属性类差异 0
（**W1110 订正**：该「24 处差异全为同向颜色转换」结论已被本批复核证伪——逐项复算得 **16 个去重色对**，其中 **12 个为「回归对」**（after 落在继承色 #23201A / 黑 #000000 / 墨软 #6B6455）·这 12 个里 **ΔL* > 12 者 9 个**（若按「ΔL*>12 或 ΔE76>30」口径则为 11 个）·根因是 W1108 把页面 INLINED 副本 `:root` 的 `--chart-N` 定义写成自引用 `var(--chart-N)` ⇒ 浏览器解析为空串 ⇒ 主题色回落为继承色。已由 W1110 根修并新增第 57 槽判据。逐项读数见 scripts/output/_w1110_w1108_delta.json）
  - 塌缩防线：改内联 JS 必重算 CSP 哈希；元素数是第一道探测器
  - E-108 与 E-109 + 计数链六段求和 = 229（CSS 48 / JS 10 / git 26 / 级联 20 / 数据 15 / 流程 110）
- **坑表编号重号收敛**：16 组跨批次真重号按先落地者保留改号其余 18 条（E-110~E-127）· 本体重号清零 · 引用按无歧义口径同步 · 计数链条数不变
- **档 3 施工前置批**：门禁四槽接线（坑表编号唯一 / PowerShell 解析 / CSP 增量漂移 / CSS 变量自引用）+ P-3 L2 口径一致性告警 + W1108 CSS 变量自引用缺陷根修
- **CI 成本治理**：暗色态门禁与 Lighthouse 跳过判定补齐 PR 事件 + 非渲染面免审名单 + 13 条教训入坑表
- **CI 成本治理 + 档 3 第二批 + 归档规则工具化**：三对页 40 行安全位令牌化 · 归档体积阈值与两面同下界对齐 · 收官链内置腾窗步
- **收官链缺陷根修 + 跨克隆占号机制根修 + 台账回填**：腾窗步行窗口静默失效根修 · 跨克隆占号可见性根修 · 台账列定位改按状态格内容锚定 · 坑表 E-160 与 E-161 入表
- **预约释放语义根修 + 提交范围门禁 merge 场景归属根修**：删除语义独立并回读断言 · merge 带入面剔除与归属反查 · 坑表 E-162 与 E-163 入表
- **收官链 py_compile 语法自检门禁**：三态清单逐件编译 · 语法错即中止整链 · 负样本实测拦停
- **W1128 收官链 py_compile 语法自检门禁**（工具面·零页面内容改动·不新增门禁槽 ⇒ 门禁 62 段不变·**不新增坑表条目 ⇒ 计数链不动**）：① **病根**：批量写 .py 后若落盘出现语法错（字面两字符反斜杠 n、缺引号、续行残缺），此前**无任何机器门禁拦截** ⇒ 坏文件直接进索引进提交，而本地跑的是好版本 ⇒ 本地全绿、提交里是坏版本 ⇒ 直到 CI 才暴露（2026-11-04 实测：8 个文件同时触发 3 个 job 红灯）；② **根修 = 收官链新增 pycompile 步**（排在 add 之后·紧随其后）：对**三态清单**（索引态 + 工作树态 + 未跟踪·排除 .gitignore）的全部 .py 逐件 compile()（**只编译不落盘**·不污染 __pycache__）⇒ 任一件 SyntaxError 即打印「文件:行号 + 错误」并**中止整条收官链**（fail-closed）；纯逻辑抽为 _compile_check 便于负样本直喂；③ **负样本实测**：在工作树放入语法错文件 ⇒ 门禁拦停（退出码 3·报出 文件:1: invalid syntax）⇒ 删除探针后复跑「3 件 .py 通过」⇒ 证明该门禁真会拦而非只跑通；④ **顺序锁同步**：既有行为锁只锁 add→refresh→stats→index→csp→cspcheck 的相对顺序 ⇒ 插入 pycompile 不破坏它；另**追加**一条行为锁「pycompile 实际被调用且排在 add 之后」+ 声明顺序断言（pycompile == add + 1）防 STEPS 与 main 双写漂移；⑤ **号段让号**：W1127 于 15:11:09 被并行会话先落地占号 ⇒ 我方顺延用 W1128；台账因新增认领行达 61 段超窗 ⇒ 先腾窗迁出 W1065-W1066（正本 59 行）再动工；⑥ 收官链 14 步全绿（新增 pycompile 步）· 门禁 62 段 0 FAIL · pytest 1310 passed / 4 skipped · ruff 全量 0 违规 · 新增单测 4 例 + 行为锁 1 例；本批教训暂落 T77 报告 §5（**不新增坑表条目**·避与并行会话 W1125 未合并批的计数链对撞）
- **W1124 治理收尾批**：七条教训入坑表（E-165 ~ E-171）与计数链 13 处同步；重建入口接入收官链并锁在 precheck 之前（幂等零变化）；里程碑滚动幂等守卫下沉到函数内；台账 W1122 行例数订正与回填；自证 12 例
- **W1123 预约释放语义根修 + 提交范围门禁 merge 场景归属根修**（工具层 + 协作机制·不新增门禁槽 ⇒ 门禁 62 段不变·坑表 258 → 260 条）：① **release 删除语义根修**：预约表写回走「合并他人记录」路径 ⇒ 合并步骤把刚删的号合回 ⇒ **已释放的号复活**（自报已释放而 list 仍在·他方取号跳段）⇒ 删除走独立「替换语义」路径 + 删除后**逐落点回读断言**（打印成功不算证据）+ 他人同号仅 session 相同时才删；新增 4 例单测；**由真实让号操作证明**（release W1122 真删除并回读通过）；② **第 51 槽 merge 场景归属根修**：并行会话 W1120 实证——我方 PR 先合入 main 后对方合并 ⇒ 新增段集合含他批段 ⇒ 归属落他批 ⇒ 本提交交付面被判 spec 之外（假红）⇒ 剔除「merge 带入面」（段=origin/main 侧已存在·文件=索引 blob 与 main 侧相同）+ 剔除后用 spec 覆盖性反查定位归属，**真越界仍判红**（负样本单测）；新增 5 例单测；③ **号段让号**：取号两次得 W1122 与 W1123 ⇒ 主动 release W1122 让给并行会话（先声明者保留）·我方用 W1123；④ 坑表 E-162 + E-163 入表 + 计数链 7 处同步（258 → 260）· ruff 全量 0 违规 · pytest 1256 passed / 4 skipped
- **W1122 级联幂等 + 双面判定**：六个插入型面接幂等 upsert 原语，一致零变化、不一致替换，里程碑滚动在重跑路径跳过；补段工具改两面分判只补缺面，历史缺口须显式确认才补；台账前批两行回填；追加根修：里程碑块按批号序落位（低号批不占链首）+ 脚注条目区间按 token 定界（内部分号不再截断·同号副本收敛）；自证 36 例
- **W1121 收官链缺陷根修 + 跨克隆占号机制根修 + 台账回填**（工具层 + 登记面·不新增门禁槽 ⇒ 门禁 62 段不变·坑表 256 → 258 条）：① **静默失效根修**：W1119 腾窗步读台账行数用 io.open 却未 import io ⇒ NameError 被宽 except Exception 吞掉并 return True ⇒ **台账行窗口判定从未真正触发**（每批收官都「成功」·零红灯）⇒ 改 open(..., encoding=) + except 收窄到 ImportError/OSError；② **W605 修复**：_rule_upper 的 docstring 内反斜杠 d 未转义 ⇒ 改 raw string（scripts/ ruff 由 10 错转 0）；③ **跨克隆占号机制根修**：预约表 tmpe 随仓不随 git ⇒ 跨克隆并行互不可见 ⇒ **实测双方各占 W1120**（零红灯·session 回落 hostname 致记录同名不可仲裁）⇒ 三源合并取号（本地 + 同机兄弟克隆 + 用户级共享表）+ session 仓路径指纹 + 撞号预警 + release 只撤本工作树登记号 ⇒ **实测取号由 W1120 正确让至 W1121**；④ **台账列定位根修**：ledger_backfill 按位置定位在 10 格行整体错位一格（status 写进会话列）⇒ 改按状态格内容锚定（9 格与 10 格皆成立·缺锚点 fail-closed）；⑤ **登记面回填**：台账 W1118 与 W1119 两行 git 反填回填（W1119 批声称已回填实为假收敛·本批订正）+ 坑表 E-160 / E-161 新增 + E-159 补注 + 计数链 12 处同步（256 → 258）+ AGENTS 铁律 23
- **W1119 CI 成本治理 + 档 3 第二批 + 归档规则工具化**（工具层 + 内容面·不新增门禁槽 ⇒ 门禁 62 段不变·坑表 242 → 256 条）：① **档 3 第二批施工**（relationships / narrative-experiment / jurisprudence 中英各一对）：实测三对页的图色主体走 D3 .attr() 与 canvas（SVG presentation attribute 与 Canvas fillStyle 均不支持 var()）且带 e-track-exempt chart-data-colors 门禁豁免登记 ⇒ 只改安全位（style 属性 + CSS 声明）共 40 行；首轮替换误改 6 处暗色补偿规则的选择器 LHS ⇒ 已按 HEAD 原文逐行复原（残留越界选择器行 = 0·补偿表与指纹零改动）。② **归档规则工具化**：archive_segments 增 --max-bytes 262144 / --chunk 50 与两面同 W 号下界对齐 + 迁完断言；batch_closeout 增腾窗步并置于 precheck 之前（precheck fail-closed ⇒ 腾窗排其后即死路径·W1117 实证）；A3 编号规则行断言由全文计数收紧为留存前缀内计数；腾窗保护含编号规则串的段不被迁出。③ **取位缺陷根修**：三处判据（regsurface / version_surface.advance_changelog_rule / check_governance_docs）原取全文首个 W001-W 匹配 ⇒ 命中历史段陈述正文 ⇒ 改为按编号规则段本体行定位（判据强度不降）。④ **经验同步**：坑表 E-159（反斜杠字面量须转义）+ E-146 补注（--force-with-lease 例外）+ 计数链 12 处同步（255 → 256）。⑤ **两面腾窗**：CHANGELOG 与 file-index 各迁出 W996 段（留存 109）+ 台账迁出 W1058 行 + W1119 认领行 ⇒ 台账 60/60；体积模式迁出 W997-W1048 后正文 61 段 / 205KB ≤ 256KiB；收官链 12 步全绿 · 全量 pytest 1229 passed / 4 skipped。
- **W1118 CI 成本治理与经验同步入仓（工具层 + 文档面·不新增门禁槽 ⇒ 门禁 62 段不变·坑表 242 → 255 条）**：① **归因实测**：最近 60 个 run 的 run 级墙钟 418.1 分钟，我方 37 run / 330.7 分钟 = 79.1%，对方 23 run / 87.5 分钟 = 20.9%，PR 数 14:6 ② **根修一**：暗色态门禁跳过判定此前只挂 push 事件 ⇒ PR 下无跳过路径（每次命中 site/** 即跑全站约 163 页 × 4 分片）⇒ 判定扩展到 pull_request 且 schedule 与 workflow_dispatch 恒全量，搜索索引数据页进非渲染面免审名单，merge 汇总 job 与上游 skipped 联动 ③ **根修二**：Lighthouse CI 仅采集 5 页，未触及即跳过采集 ④ **经验同步入仓**：Agent Memory 内 W1114~W1118 的 13 条教训落坑表 E-141 ~ E-153（242 → 255 条），计数链 11 处同步 ⑤ **节奏收紧**：一批一 PR 一 push，收官链产物提交前生成完毕
（**W1110 订正**：该「24 处差异全为同向颜色转换」结论已被本批复核证伪——逐项复算得 **16 个去重色对**，其中 **12 个为「回归对」**（after 落在继承色 #23201A / 黑 #000000 / 墨软 #6B6455）·这 12 个里 **ΔL* > 12 者 9 个**（若按「ΔL*>12 或 ΔE76>30」口径则为 11 个）·根因是 W1108 把页面 INLINED 副本 `:root` 的 `--chart-N` 定义写成自引用 `var(--chart-N)` ⇒ 浏览器解析为空串 ⇒ 主题色回落为继承色。已由 W1110 根修并新增第 57 槽判据。逐项读数见 scripts/output/_w1110_w1108_delta.json）
  - 元素数零损失（750 → 751 / 749）⇒ 非塌缩；非属性类差异 0 ⇒ 无渲染错位
  - 塌缩防线：改内联 JS 必重算 CSP 哈希（首轮漏跑曾致 750 → 112）⇒ 写入坑表 E-108 与 E-109
  - 计数链六段求和 = 229（CSS 48 / JS 10 / git 26 / 级联 20 / 数据 15 / 流程 110）
- **图表色工程批·档 3 前置批（暗色图表令牌补齐 + 双态取证 + 原型验证）**：
  - 暗色令牌缺口实测：站内令牌暗色无覆盖 6 个，其中图表色 2 个须补（--chart-3 / --chart-5）
  - 暗色取值按补偿等效值定案：--chart-3 取 #C8A063，--chart-5 取 #F2E8D3（弱补偿等效呈现值）
  - 受影响面实测：var(--chart-3) 与 var(--chart-5) 已在 42 页 / 114 处在用 ⇒ 须双态视觉取证
  - 风险登记：新暗色值与既有 --chart-6 暗色值的色差偏近 ⇒ 同页共现须原型页实测
  - E-106 与 E-107 + 计数链同步
- **坑表编号唯一性体检与机器判据建置 + 档 3 前置（暗色图表令牌补齐与双态取证）**：
  - 新增判据 scripts/check_pitfall_id_unique.py：新增条目撞既有编号判红，存量同号列 NOTE（3 例单测）
  - 两条编号改号：W1104 实证的两条由 E-91 / E-92 改为 E-102 / E-103
  - 暗色图表令牌补齐：--chart-3 取 #C8A063、--chart-5 取 #F2E8D3（补偿机制等效呈现值）
  - J2 双态取证：6 页 × 亮/暗 = 11170 元素逐属性零差异；静态影响面 42 页 / 114 处
  - 计数链六段求和 = 227（CSS 48 / JS 10 / git 26 / 级联 20 / 数据 15 / 流程 108）
- **开局事实摘要 stats 新鲜度告警（P-3 L1）**：
  - 四类显式告警：缺失 / 损坏 / 空对象 / 陈旧（告警不阻断）
  - 消除静默降级（原 except: pass => 空字典或过期值无从察觉）
  - 陈旧判据：生成件 mtime vs CHANGELOG.md mtime（+2 秒容差）
  - 新增 5 例单测全绿；顺带清掉 W1100 的 CI 死锁
  - E-91 + 计数链五处同步
- **图表色工程批·档 3 落层分类盘点（只读批）**：
  - 档 3 真实口径 = 1412 处 / 145 页（互斥归类 + 色板分层）· 校验项：档 1/2 调色板色 = 0
  - 另有 3404 处页面自有 hex ⇒ 独立议题不并入档 3
  - 补偿规则：990 + 20130 条 · 330 页 · 指纹仅 1 种 · 无生成器 · tokens.css 共享副本 114 处
  - 工程次序：W1101 ΔL\* 判据 → 档 3 原型批 → 规模化 15 批 → 补偿收口
  - E-90 + 计数链五处（212→213）
- **图表色工程批·档 2 扩展批 3（档 2 收尾·四页四处）**：
  - 施工：4 页 4 处保留 .attr 直写 var(--chart-N) · 全站调色板色残留 0 · CSP 856 页零漂移
  - 施工前静态勘查：预判与实测 4/4 吻合（仅 philosophy 的 rect 命中 fill^=# 补偿规则）
  - 稳定值对拍（同态多拍取 5078）：差异 4 处且全部预期（3 令牌跟随 + 1 filter 补偿失配）· 元素数零差异
  - 零尺寸元素另测（social-media 图标 0x0）：computed 暗色 rgb(224,96,79) ⇒ 令牌跟随成立
  - 档位复算：档 2 全站剩余 4 → 0 处（归零）
  - E-89 + 计数链五处（211→212）
- **v2.3.104（W1096）**：INDEX 大小写统一（232 件改名）· 四判据同批改造 · design 文件全量审查 · 归档系统三份正本清偿
- **图表色工程批·档 2 扩展批 2（表现属性直喂与补偿失配落回类色实测）**：
  - 范围：档 2 剩余 31 处 / 14 页（同口径复算）⇒ 本批 10 页 27 处，余 4 页 4 处待批三
  - 施工：保留 .attr 直写 var(--chart-N) · 批 2 内残留 0 · CSP 856 页零漂移
  - 双态对拍：差异 93 条全部属性类（fill 37 / stroke 36 / filter 20）· 元素数零差异（两态各 14412 元素）
  - 例外 2 处经受控回退对照实测闭环：补偿规则失配 ⇒ 落回 CSS 类色 ⇒ 组内标签色值统一（非回归）
  - 档位复算：档 2 全站剩余 31 → 4 处 / 4 页
  - E-88 + 计数链五处（210→211）
- **W1096 INDEX 大小写统一 + design 审查 + 归档清偿（三合一治理批）：
  - 施工：7 页各 1 处 #c8463a → var(--chart-1)，残留扫描 0 · CSP 重算后 856 页零漂移
  - 双态取证（扩展后 J2 首次实战）：元素数前后一致（10089）· rc=1 报出颜色差异 prop={'fill': 20} · 全在 dark · rgb(200,70,58)→rgb(224,96,79)
  - 档 1 全量清零：同口径独立复算 = 0 处 / 0 页（裸字面量 1535→1509）
  - 判据口径：图表色批次的「视觉零变化」不成立（那是预期差异）




> 历史概要（W1118 及更早）的详细记录见 [CHANGELOG.md](CHANGELOG.md)（W534 裁剪：里程碑概要按维护契约只留最近 5 版，删前逐批断言 CHANGELOG 有段·信息零丢失·W713 归位=指针须指窗口最老可见块）。

## 二、下一步方向候选清单


> 按"内容扩容 / 可视化深化 / 工程化 / 分享发布 / 战略转型"五类列出。
> **需求侧批次配额（W597 起）**：每连续 3 个 W 批至少 1 批投向需求侧（主计划 docs/superpowers/plans/2026-09-21-demand-side-optimization-master-plan.md WP 队列），直至 WP-A 判定完成且 WP-B/D/F/G 落地。**〔W792 核查批注：终止条件已满足——WP-A 于 W626 判定归档·WP-B/D/F/G 及全部 WP-A~M 已收官（W790/W791 实证）·本配额规则到期终止·不再构成批次配额约束〕**

> **⚠ 仍在生效的策略约束（W342 裁决·误删即越界）**：**停止模板化扩容** —— A3 人物分析冻结于 215 篇；A4 主题专题原冻结 199 篇，W342 放宽为「允许填补长期引用空缺的非批量补篇」，**不恢复批量扩容**；A6 诗词歌赋已齐备不再扩。
>
### 待动的方向（原 A / V / E / S 四类·**只列未完成项**）

> 历史沿革（W402 战略转型、A2/A3/A4/A5 各方向已完成批次、E1-E8、S 卡裁决、优先级建议）
> 已全文迁 [archive/docs/HANDOVER-ARCHIVE.md](archive/docs/HANDOVER-ARCHIVE.md)（W1026·按关键词 grep 查）。

- **内容质量深化（非增量）**：A1 逐回补交叉引用与结构化元数据、A5/A6 提质、全站死链与术语统一
- **A3 人物分析深化**（现有 215 篇）：明代历史原型对照（王阳明 vs 唐僧心学 / 张居正 vs 玉帝权术 / 海瑞 vs 悟空直谏）· 女性人物专题（铁扇公主 / 白骨精 / 玉面狐狸）· 取经五众心理画像补遗
- **A4 主题专题扩容**（现有 209<!--stats:a4_docs--> 篇）：按需补缺，不再批量扩容
- **A5 文化与历史背景**（现有 34 篇）：佛道思想（禅宗公案 vs 内丹学 / 三教合一）· 明代社会史（市井 / 科举 / 海禁 / 卫所）· 版本演变补遗
- **A6 诗词歌赋**：中文已齐备、英文译介已全覆盖 —— **无待办**
- **V1 现有页面内容深化**：dashboard KPI 更新 / 交互增强（hover · click · 筛选）
- **V2 新增可视化维度**：西游地理 3D / 人物关系动态网络 / 八十一难难度热力图深化
- **V3 跨页面导航增强**：footer 关联链接补全 / 标签云 / 智能推荐
- **V4 移动端体验**：375px 视口回归 / 触摸交互优化 / 竖版图表
- **E9 治理经验移植**（W663 立项·D1-D3 已裁决）：GateKeeper / 绿洲 / 大赛三仓治理反向移植 —— W 编号对账口径复用
- **S2 分享发布**：12 篇 A2 随笔 + 15 篇 A4 专题 → 博客 / 公众号 / 知乎
- **S4 学术投稿**：基于 `docs/04-文化与历史背景/` + 学术论文索引 50 条撰写投稿
- **手搓绕过级联治理批（W965 立项候选）**：并行会话手写版本面绕过 `batch_cascade` 的模式治理（实证三起）


---
## 三、方法论沉淀

> **经验总入口（W755 指针化·W973 真指针化收口）**：现役坑位与门禁读
> [docs/agent/pitfalls.md](docs/agent/pitfalls.md)（267 条·六主题）与 [docs/agent/gates.md](docs/agent/gates.md)（57 槽）；
> 诊断 SOP 读 [docs/10-方法论沉淀/](docs/10-方法论沉淀/README.md)；
> 本区历史叙事全文已迁 archive/docs/HANDOVER-ARCHIVE.md（W973·grep 查）。
## 四、待办事项（短期）

> **对账注记（W1057·Backlog 对账已执行·W1021 触发器 31 批点名）**：本段历史 12 条 [x] 条目（v0.9.1 回归 / W285-W287c 源整理 / W358 推送 / W402 RAG / W445 英文站 / W536-W548 迁移 / W626 GoatCounter / W1048 P2 治理）已逐条拿 git 与测试实况核验——**11/11 批 git 提交直证（cc6feae8·f01e84e4·548b6135·7b286620·8cfc7842·4da20ab6·a460b889·c3f1c0e4·c4605517 等）·0 滞后**（对照 W1020 对账 41% 滞后率·登记面已收敛）。已完成条目移出本段（详情在各批 CHANGELOG 段与台账/归档行）；**当前无未决待办**——新待办按铁律 18 三问与 W1021 触发器（≥25 批对账）维护。

- [x] **形态锚（最近一条留存）·P2 治理微批（W1048·2026-10-31 一笔收编收官）**：gates.md:26 计数旧值 615→616（根因 = sweep_markers 覆盖面缺 gates.md·覆盖面修复已随 W1055 落地）+ CLAUDE.md 补铁律 15/16/17 速查行 + 收编 W1044 孤儿（C5e 坑表分项对拍 / 计划目录卫生 / archive 7 件 minimax 回退清除 / pytest 标记跟随）与 W1046 方案件入库（**已随 W1052-W1055 实施完毕**）+ W1047 段要点栏复制错误订正——详见 CHANGELOG W1048 段
## 五、关键文件索引

### 项目根目录

- [README.md](README.md)：项目说明（版本行由 bump 维护·以文件头部为准）
- [STRUCTURE.md](STRUCTURE.md)：目录结构详细说明
- [CHANGELOG.md](CHANGELOG.md)：更新日志（正向时间线，W001-W575；v2.2.50+ 现役段）
- [CHANGELOG-ARCHIVE.md](archive/docs/CHANGELOG-ARCHIVE.md)：历史版本归档（W400-W649·W422/W511/W681 迁入；更早 W001-W399 见 archive/docs/CHANGELOG-ARCHIVE-tier2.md）
- [HANDOVER.md](HANDOVER.md)：本文件（跨 session 交接，v2.2.50+ 现役段）
- [archive/docs/HANDOVER-ARCHIVE.md](archive/docs/HANDOVER-ARCHIVE.md)：交接文档历史归档（v2.0.39-v2.2.49，W066-W280）

### docs/ 目录

- [docs/00-导读/项目说明.md](docs/00-导读/项目说明.md)：项目状态与待办优先级
- [docs/00-导读/文档规范.md](docs/00-导读/文档规范.md)：文档写入规则（防膨胀·6 文档同步正确方式·归档触发条件）
- [docs/01-全书逐回解读/](docs/01-全书逐回解读/)：100 回逐回解读（A1 方向 100/100 收束）
- [docs/02-人物深度分析/](docs/02-人物深度分析/)：215 篇人物分析
- [docs/03-主题与情节专题/](docs/03-主题与情节专题/)：209 篇主题专题
- [docs/04-文化与历史背景/](docs/04-文化与历史背景/)：34 篇文化与历史背景
- [docs/05-诗词歌赋/](docs/05-诗词歌赋/)：诗词歌赋专题
- [docs/06-个人随笔/](docs/06-个人随笔/)：44 篇独立随笔 + 现代视角解读合集（A2 方向 Batch 1-10）
- [docs/10-方法论沉淀/](docs/10-方法论沉淀/)：5 篇主题 + 1 篇索引（S1 方向 W070 新增，W073 Preflight 双轨验证升级）

### site/data/ 可视化

- [site/data/text-search.html](site/data/text-search.html)：原著全文检索（708441 字，100 回）
- [site/dashboard.html](site/dashboard.html)：数据仪表盘（50+ 个 KPI 卡片 + 全站搜索浮层）
- 87 个可视化/交互页（含 graph-explorer·A-AH 34 类 + Q+ 双联 + Q++ 博物馆 + Q+++ 新功能 + 全文检索 + 妖怪后台论 + MBTI 演变图 + 难度热力图 + 地理符号学力导向图 + 引语情感分析 + 人物共现网络 + 关系演化时间线 + 六感/十二维/十六维/十七维叙事学关系图谱 + 四大天王器物符号图谱 + 观音六重身份关系图 + 妖怪受害者关系图 + 地府权力关系图 + 天庭权力关系图 + 互文性关系图谱 + 妖怪女性群体关系图 + W233 V3 四页 + W236 V4 Three.js 3D 升级 + W270/W274/W278/W282 跨方向整合项目可视化）

### scripts/ 工具

- [scripts/output/file-index.md](scripts/output/file-index.md)：反向文件索引（与 CHANGELOG 双向链接，W088+ 现役段）
- [archive/docs/file-index-ARCHIVE.md](archive/docs/file-index-ARCHIVE.md)：反向索引历史归档（W031-W087）
- [scripts/README.md](scripts/README.md)：工具目录说明（常驻工具清单 + archive 归档说明 + 约定）
- [scripts/extract_strings.py](scripts/extract_strings.py)：穷举 viz 页 chrome 文本节点 + script CJK 字面量（英文站翻译前置·W447 转正）
- [scripts/validate_en.py](scripts/validate_en.py)：校验 EN 页 chrome CJK 白名单 + script CJK=0（英文站翻译门禁·W447 转正）
- [scripts/verify_delivery.py](scripts/verify_delivery.py)：交付校验总闸
- [scripts/reserve_w.py](scripts/reserve_w.py)：批次号预约（开批先跑占号·防并行会话撞号·铁律 17·W1041 立）
- [scripts/generate_csp.py](scripts/generate_csp.py)：全站 CSP 注入 + `--check` 零漂移
- [scripts/lint_links.py](scripts/lint_links.py)：全站死链巡检
- [archive/scripts/](archive/scripts/)：历史一次性脚本归档（45 个，W447 治理，保留 git 历史备查）
- [scripts/batch_screenshots.js](scripts/batch_screenshots.js)：Playwright 批量截图 + 布局断言
- [scripts/slice_screenshots.py](scripts/slice_screenshots.py)：Pillow 800px 切片
- [scripts/detect_unwrapped_tables.py](scripts/detect_unwrapped_tables.py)：静态表格溢出扫描

### skills/ 项目技能（playbook）——W562 退役

W562 经用户确认整体删除 skills/ 目录（运行时不加载、维护面为负资产）；历史内容见 git 历史（<= W561）与本目录其余章节。

- [source/原文/分回/](source/原文/分回/)：100 回原文 .md（W286 从古诗文网批量抓取·W286b 转为 .md·W286c 清除第069/099回网页垃圾）
- [source/原文/shendu/](source/原文/shendu/)：100 篇深读切片 .md（W286 从 5 个深读 .txt 拆分·W286b 转为 .md·含元数据注释标注推测回号映射）
- [source/引用与网络解读/学术论文索引.md](source/引用与网络解读/学术论文索引.md)：50 条学术论文引用
- [source/引用与网络解读/网络解读精选.md](source/引用与网络解读/网络解读精选.md)：15 条网络解读

---
## 七、环境复现（假设接手者电脑为全新状态）

### 系统要求

| 依赖 | 最低版本 | 用途 |
|---|---|---|
| Python | 3.8+ | 文本分析脚本（jieba 分词 + Pillow 图像切片） |
| Node.js | 18+ | Playwright 1.45+ 截图审查（硬性要求，Node 16 会失败） |
| Git | 2.20+ | 版本控制 |
| 浏览器 | Chrome/Edge/Firefox 任意现代浏览器 | 打开 `site/` 静态站点（支持 `file://` 协议） |

### 一键复现步骤

```bash
# 1. 克隆仓库
git clone <repo-url> xiyouji
cd xiyouji

# 2. 安装 Python 依赖（jieba + Pillow）
cd scripts
pip install -r requirements.txt

# 3. 安装 Node 依赖（playwright + 自动下载 chromium）
npm install
# postinstall 钩子自动执行：npx playwright install chromium

# 4. 验证：直接双击 site/data/ 下任一 HTML 应能在浏览器渲染 D3.js 图表
#    示例：site/data/81-hardships.html

# 5. 验证截图审查工具链
npm run screenshots        # 批量截图 + 布局断言 + 自动切片
python check_js_syntax.py --all  # 批量内联 JS 语法检查（site/data + dashboard）
python detect_unwrapped_tables.py  # 表格溢出扫描
```

### 常用工具命令（见 [scripts/README.md](scripts/README.md) 完整清单）

| 命令 | 用途 |
|---|---|
| `npm run screenshots` | Playwright 批量全页截图 + 布局断言 + 800px 切片 |
| `python check_js_syntax.py --all` | 批量检查 `site/data/*.html` 内联 JS 语法（Node `--check`） |
| `python check_js_syntax.py <file>` | 检查指定 HTML 内联 JS 语法 |
| `python detect_unwrapped_tables.py` | 静态扫描无横向滚动容器的 `<table>` |
| `python fix_svg_negative_widths.py --dry-run` | 预览 SVG 负宽度修复（不写入） |
| `python slice_screenshots.py --output-dir output/screenshots` | 全页截图切片（默认 800px） |
| `node debug_page_error.js <file>` | 调试单个页面运行时错误 |
| `node debug_console.js` | 调试单个页面控制台错误 |

### 可选本地服务（静态站点无需即可运行）

本项目主体为纯静态站点，**所有可视化页面支持 `file://` 协议直接打开，所有数据内嵌于 HTML（`EMBEDDED_DATA` 模式）**；唯一"外部"依赖是 D3.js v7 CDN（首次联网加载后浏览器缓存可用）。以下两项为**可选**本地服务（开发 / 在线浏览 / 数据 API 用，非运行必需）：
- **数据 API 服务**（W337/W339）：`scripts/api/api_server.py`（默认 127.0.0.1:8787）·提供 `/datasets` + `/graph` + `/graph/<name>` 等端点；`site/data/graph-explorer.html` 在线走 `/graph`，离线回退内嵌 `graph-fallback.js`
- **本地 RAG 后端**（W330）：`scripts/rag/rag_server.py`（默认 127.0.0.1:8777）·`site/dukou-engine.html`「渡口问津」调用 `/query`；服务未启动自动回退模板引擎

---
## 八、已知雷区

> **雷区权威 = [docs/agent/pitfalls.md](docs/agent/pitfalls.md)（267 条·六主题·含 shell 场景查坑表）**；
> 本区历史雷区叙事已迁 archive/docs/HANDOVER-ARCHIVE.md（W973·grep 查勿通读）。
## 九、使用说明

### 跨 session 接续流程

1. **新 session 启动时**：先读本文件 + [README.md](README.md) + [docs/00-导读/项目说明.md](docs/00-导读/项目说明.md)，了解当前进度与待办
2. **接续 W 编号（先占号！）**：**开批第一步必须先跑 `python scripts/reserve_w.py` 占号（铁律 17·W1041 立）——stdout 即本批 W 号，未占号不动手**；占号后取号口径照旧：以本文件「一、当前进度」段标注的现役 W 为准，新批编号按 [CHANGELOG.md](CHANGELOG.md) 顶部「W### 编号规则」取现役段 max+1（与 reserve_w 的 `candidate=max(台账,CHANGELOG顶段,已预约)+1` 一致）。**本文件禁止内嵌具体 W 号**（W520「递增数字禁字面量」铁律——写死的批次号必然随项目演化漂移；本行即该规则的存量病例，W534 修复）
3. **文件管控**：先读 [docs/00-导读/文档规范.md](docs/00-导读/文档规范.md) §11 文件管控清单——11.1 必须同步的文件（核心 2 份硬门禁 + 辅助 4 份 + 里程碑旁文档）/ 11.2 禁止擅自修改的文件（历史段/密钥/门禁/归档/字体源）·跨 session 多 Agent 协作强制遵守
4. **选择方向**：本文件"二、下一步方向候选清单"按优先级列出所有可推进方向
5. **方法论参考**：本文件"三、方法论沉淀"列出所有可复利经验，新 session 应遵循
6. **完成后更新**：每轮 W### 完成后，更新本文件"一、当前进度"段 + "三、方法论沉淀"段（如有新经验）+ "四、待办事项"段
7. **质量分层声明（PRE-30·W742）**：批次交接/复盘时附四行分层表，声明本批验证覆盖范围，防「门禁过=已 review」语义混淆（W737 事后 review 实证）——模板：`门禁级（机器不变量）=<覆盖清单>｜定向语义审查=<逐条人工判读范围>｜算法判定=<判据与未复审声明>｜未覆盖=<盲区与立项链接>`

### 与其他文档关系

- **本文件**（HANDOVER.md）：跨 session 交接，记录进度/方向/方法论/待办（v2.2.50+ 现役段）
- [archive/docs/HANDOVER-ARCHIVE.md](archive/docs/HANDOVER-ARCHIVE.md)：本文件历史归档（v2.0.39-v2.2.49，W066-W280）
- [CHANGELOG.md](CHANGELOG.md)：变更日志，每个 W### 附四件套字段（来源/文件/验证/状态）
- [STRUCTURE.md](STRUCTURE.md)：目录结构详细说明
- [README.md](README.md)：项目对外说明
- [docs/00-导读/项目说明.md](docs/00-导读/项目说明.md)：项目状态与待办优先级
- [docs/00-导读/文档规范.md](docs/00-导读/文档规范.md)：文档写入规则（防膨胀·6 文档同步正确方式·归档触发条件）
- [scripts/output/file-index.md](scripts/output/file-index.md)：反向文件索引（W088+ 现役段）

---

> 本文件创建于 2026-07-25（v2.0.41 W068 后），用于跨 session 交接。每次完成新 W### 后更新。最后更新：2026-11-04（W1128 收官链 py_compile 语法自检门禁）；2026-11-04（W1124 治理收尾批：教训入坑表 + 重建入口收进收官链 + 滚动幂等守卫）；；2026-11-04（W1123 预约释放语义根修 + 提交范围门禁 merge 场景归属根修）
