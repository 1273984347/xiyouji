# 交接文档


> **📖 阅读契约（W707）**：首段型+查表型——接手时只读「零、当前阻塞」+「一、当前进度」+ 文件末尾「最后更新」链；「三、方法论沉淀」「四、待办」按需查；历史批次细节在 CHANGELOG（grep 查）勿在本文件找。
> 轨标：教学讲解
> 本文件用于跨 session 交接，记录当前进度、下一步可推进方向、方法论沉淀与待办事项。
> 创建于 2026-07-25（v2.0.41 W068 后）
> 最后更新：2026-10-27（W980 stats 标记同步机器化批）·2026-10-27（W979 收官提示位扩展批）·2026-10-27（W978 第 44 篇工作复盘批）·（W449-W549 及更早批次详见 CHANGELOG.md）
> 与 [CHANGELOG.md](CHANGELOG.md)（变更日志）/ [STRUCTURE.md](STRUCTURE.md)（目录结构）/ [README.md](README.md)（项目说明）/ [docs/00-导读/项目说明.md](docs/00-导读/项目说明.md)（项目状态）配套使用。
> **维护契约（防乱写）**：本文件是项目进度中枢，只允许结构性编辑——① 保持「零 / 一 / 二 / 三」四段骨架不变；②「最后更新」行只写最新 1–3 批摘要（每批 ≤ 1 行），**禁止把历史批次堆进该行**（历史已归档 / 在 CHANGELOG）；③ 每批详细记录只写 CHANGELOG + 归档（历史段禁改）；④ 任何「当前 HEAD / 当前版本」表述必须与 `git rev-parse --short HEAD` 核对后更新；⑤ 本文件是状态快照，与 CHANGELOG（时间线）冲突时以 CHANGELOG 为准。
> **历史归档**：v2.0.39-v2.2.49（W066-W280）段的详细进度记录已迁移至 [archive/docs/HANDOVER-ARCHIVE.md](archive/docs/HANDOVER-ARCHIVE.md)。本文件仅保留 v2.2.50+（W277）现役记录与全局概要。



---



## ⚠️ 零、当前阻塞（接手必读）



**原唯一长期阻塞「档 B 真实生成需 LLM_API_KEY」已于 W402 解除**（provider 化 Base URL·渡口问津生成式问答·LLM_API_KEY 配于本地 .env 已 gitignore）。**访问数据基线已接入（W403·localStorage 自建·仅本浏览器可见）**，**S2 分发完成（W404 精选 27 篇发布版 + 合集页 curated.html + W405 第二批 27 篇随笔发布版·44 篇随笔全发布）**，**GoatCounter 已接入并完成自托管修复（W425 注册接入 + W426 gc.zgo.at 大陆 DNS 污染 → count.js 本地自托管·计数回传 goatcounter.com·线上实测 HTTP 200）**；**真实跨访客读者量仍待回传验证**（部署生效后观察后台数据）；有流量则继续分发（S4 学术投稿等），无流量则停止内容生产。另存在平行入口 `xiyouji-agent-web`（OpenAI-compatible 自研引擎·引擎三键配于服务端 .env·W680 起·`PROJECT_CWD`=仓库根（自动解析·W596）直接对话/检索/跑脚本），与 scripts/rag 档B 二选一或并行。**安全审计 P0-1/P1-1 已处置（W411）**：Web Agent 默认权限改 acceptEdits + 可选 AGENT_WEB_TOKEN 认证 + 权限/工作目录白名单 + 仅回环监听 127.0.0.1·MCP 4 工具路径白名单拒越界。**安全审计剩余项已处置（W412）**：P0-2 禁运行时覆盖引擎凭证/端点键（前端表单移除·仅服务端 .env·W680 起=LLM_* 三键）·P1-2 静态站 XSS 转义 6 页·P2 RAG 参数钳制/LLM 端点校验/SSE 超时与断开清理/DOMPurify 消毒/依赖锁定·P3 日志收敛/CORS 白名单/死代码/版本漂移；密钥吊销轮换需用户在 DeepSeek 控制台操作（P1-3 仅告知）。**W424 对抗性审查修正与全仓整理已处置**：A4 门禁校准 209（verify EXPECT_A4 201→209）·3D 页 defer 修复·EN 页 Ch. 腐蚀修复·security 依赖审计修复（只扫仓库 requirements.txt·high 103→0）·新Agent启动Prompt/workflows README/DESIGN 同步·全仓清理（截图 416MB + 过期报告 14 + 原始审计 JSON 4）·RAG 索引重建。**W424 SRI/CSP 已处置**：95 外部脚本标签 SRI（SHA-384）·159 页 meta CSP（680 内联脚本哈希·script-src-attr none）·EN 腐蚀第二波（""X"" 32 处 + 反引号 4 处）·6 页 sankey 漏引修复·复盘沉淀批次（腐蚀/插件引用门禁 + 方法论新增 + 内容同步）。**W417 文档健康治理已处置**：CHANGELOG/file-index/交接文档归档精简降达标·verify_delivery 新增 A1-A6 真实计数校验（611==611）·actions 升级消除 Node 20 deprecation·RAG 索引重建演练通过·bump_version 增强（--desc/W 范围锚点/页脚同步）·LICENSE 双协议边界补强·sitemap 补全 154 页。**W418 内容质量深化已处置**：全站死链巡检（site/en/ 29 broken 链接修复——EN 版存在指向同目录/无 EN 版回退中文原版 ../data/*.html 加 lang="zh-CN" 标注·docs/ 全量 4784 链接 0 broken）+ A1 逐回解读 23 回补 `> 导航：` 引用行（100 回导航全覆盖 100/100）。**W419 修复 A1 深度解读 SD 错位已处置**：22 篇 SD（SD038-052/056-062）编号≠真实回号归位（根因 W286 合并脚本只读源第一行·元数据在第三行→fallback 按编号放置）·按正文真实回号范围式复制 40-72 回全覆盖（原 63-72 十连回空白消除）·源文件 24 篇元数据/H1/正文内嵌/关联行修正·第 56 回补写 SD101。**W420 A1 内容质量深化已处置**：A1 深度解读 100/100 补全（第038/039回新增 SD102/SD103·source 切片 101→103）+ 56 回「对应原著/数据指标」结构化元数据补齐 + 99 回导航上一回/下一回错链修复（此前约 60 回指向非相邻回）+ 10 回 sd-crossref 关联块死链修复（66 处·docs/01 1715 链接 0 broken）。**W421 Screenshot Review 提速优化已处置**：screenshot-review.yml 新增改动范围判定（页脚/文档-only 跳过·site/data 变更定向截图·static/脚本/workflow 变更全量·schedule/dispatch 全量）+ batch_screenshots.js --only-pages 定向截图 + Playwright 浏览器缓存 + checkout fetch-depth 0。**W422 全量治理已处置**：perf.yml 补 push 触发（LHCI 预算门禁首次在真实发布路径运行）·verify_delivery 新增 4 项门禁（A1 导航相邻性/docs/01 链接/sitemap 覆盖/site/data 回退模式）·文档健康归档（CHANGELOG 83 行·file-index 127 行·交接文档 556 行）·双索引规则校准（新文档执行 + 存量以 file-index 追溯）·README 命令修正 + JS 检查进 CI·认知总览计数校准（756/611/211/209）·Dependabot/mypy report-only/a11y 口径/artifact 瘦身/_DEBRIS 清理。**W459 V2 审查收尾已处置**：D2 回目跳转死链修复（方案错误约定 `第NNN回-回目摘要.md` → A1_DOC_MAP 内嵌 100 条真实文件名映射·路径深度 ../→../../）+ check_dynamic_links.py 动态链接门禁挂 verify_delivery（补 lint_links 静态盲区·首跑抓出 tag-cloud dashboard 死链 + EN source_doc 虚构路径并同批修复）+ V2 方案文档回写 + 首页精选补 geo-3d 入口；W456-W458 积压改动同批基线提交（de8047a）。当前 HEAD = W980（统计标记同步机器化：对账面标记自动跟随实算，一笔登记滞后订正，计数链重判待站点地址；详见 CHANGELOG）。**W530 遗留待办已部分解除（W535）**：取数环节不再需要人工登后台——新增 `scripts/fetch_gate_stats.py`（零第三方依赖·GoatCounter API v0 拉近 7/30 日页面 UV·`--self-test` 负样本 14/14 + `--fixture` 离线端到端），仅剩「生成 API 令牌写入 `.env`」一次性动作，随后即可跑 `judge_gate.py` 正式判定。**W590 需求侧优化主计划已入库**（`docs/superpowers/plans/2026-09-21-demand-side-optimization-master-plan.md`·13 工作包约 14 批·WP-A 取数自测 14/14 过·正式裁决仅待 `.env` 配 `GOATCOUNTER_API_TOKEN` 后跑 judge_gate）。**W530 决策闸门已正式判定（W626·2026-09-30）**：GoatCounter API 令牌已配置（浏览器 UI 生成·Read statistics 权限·剪贴板提取直写 `.env` 已 gitignore），`fetch_gate_stats.py` 实测 **7 日 UV=1 / 30 日 UV=24**，`judge_gate.py` 判定输出分支 **归档**（30 日 UV<30 阈值）——**冻结 WP-D2 及一切内容扩容批，仅推进 P0/P1 工程批**（WP-C SEO 根治层等）；WP-B-ALT 维持冻结预案；复盘存档 `docs/11-方案报告/调研与数据复盘/读者数据复盘.md`（作者侧待办：UV 曲线/来源占比后台截图人工核）。

**冻结适用范围（W793 立·单一权威表述）**：内容扩容维持 W626 归档裁决冻结（30 日 UV<30·判定未翻转；UV 数据链自 2026-09-30 起中断——fetch_gate_stats 实测 HTTP 404·API 恢复后须重判）；已点名解冻项（WP-D2/E、B-5/B-6 第二步、B-7）均已全部收官，不再另议；工程/治理/门禁批不受限（W626 原文即「仅推进 P0/P1 工程批」）；新增内容扩容批须二选一：**用户点名**，或 **judge_gate 重判为「继续分发」**（30 日 UV≥30）。
## 一、当前进度（W980 统计标记同步机器化批：对账面标记自动跟随实算源，事实收官订正一笔，计数链待新站点地址重判；更早批次详见 CHANGELOG.md）
- **W980 stats 标记同步机器化批**（P-44-05 + 两登记滞后订正）：
  - sweep_markers()：C5b 权威面标记自动跟随实算（CHANGELOG 口径块截断+数字键正则两防线·首跑 2 处自证）
  - W681 事实收官追加订正（agent-web LLM 实测完成·用户确认·.env 现缺附记）
  - GoatCounter 待用户给新站点代码后重探重判（W806 退役记录 vs 口述可用·取证中）
- **W979 收官提示位扩展批**（P-44 四件收口）：
  - _close_hints() 集合化：[SIZE] 超窗回窗提示 + [TMPE] TTL 超龄报数（_shot 251MB/_inbox 215MB 待主人确认）+ [SCRIPTS] 防再积计数位
  - P-44-04 裁定免迁：三位号活面零残留（宽口径复扫实证·余量在冻结段与冷存储）
  - 全部维持只输出不拦截语义（W822）
- **W978 第 44 篇工作复盘批**（触发器 T3 首触发·W955-W977 区间）：
  - P-43 五项当期闭环 5/5（三项机器化）· 体积窗口制 17 批后首次实战咬合
  - 沉淀通道机器化（坑表 64·[TMPE]·286 件退役）+ tmpe 清理闭环首次走通
  - P-44-01~04 登记（回窗提示化/TTL 管线化/`_` 件计数位/W1000 收尾）
- **W977 一次性件批量退役批**（454 候选 → 286 入档）：
  - 语料级引用剔除（活引用面一次载入）→ 15 件现役硬保留（_cite_probe/_check_pipeline/_gen_search_index 等）+ 152 件 S4 gitignore 本地件原地不动
  - _check_json_copies 暴露 W842 恢复身份追加硬保留（W735 误归档教训防复发）
  - 286 件 git mv 入 batches 五组 + 组行台账 + 目录文档刷新（scripts 顶层 454 → 167）
- **W976 工具链体检修复批**（体检令三窗回窗 + 工具三缺陷修复）：
  - 台账修剪器 A5 断言修复（归档块保持源相对顺序·自测重写走 move() 三形态）
  - C3 修路指引分治（台账指向 archive_ledger_rows）+ preflight 认领后自撞修复（rejection_pairs）
  - 三窗回窗（109/109/59）+ W962 伪阻塞闭环 + 坑表 +1 条（自测样本判据·64 条）+ [TMPE] 收官提示位
- **W975 跨 Agent 经验沉淀入仓批**：把 W974 批的 9 条经验从 Agent 私有 Memory 搬进仓内——坑表 `docs/agent/pitfalls.md` +6 条（57→63）、深度篇《素材批处理与判据自证方法论》（10-方法论沉淀 编号 26）、AGENTS §4.3 主题视图与计数声明、HANDOVER 两处指针同批同步（门禁 N4「AGENTS 声明 == pitfalls 实数」复验一致）。
- **W974 内页题图成套批·第三组**：再出 12 张线描题图（人物 6：金角大王/银角大王/黄眉大王/黑熊精/托塔李靖/玉兔精 + 主题 6：女儿国/车迟国斗法/狮驼岭/通天河/盘丝洞/无底洞），接入 12 个 people 库页 ⇒ 站内线描题图累计 52 张、reader 有题图页 63/622；母版 249 字符从 W953 JSON 逐字复用；同批修正站点版「主体顶」抗噪口径（bbox 顶会被孤立噪点污染）。




































































































































> 历史概要（W974 及更早）的详细记录见 [CHANGELOG.md](CHANGELOG.md)（W534 裁剪：里程碑概要按维护契约只留最近 5 版，删前逐批断言 CHANGELOG 有段·信息零丢失·W713 归位=指针须指窗口最老可见块）。
## 二、下一步方向候选清单


> 按"内容扩容 / 可视化深化 / 工程化 / 分享发布 / 战略转型"五类列出。
> **需求侧批次配额（W597 起）**：每连续 3 个 W 批至少 1 批投向需求侧（主计划 docs/superpowers/plans/2026-09-21-demand-side-optimization-master-plan.md WP 队列），直至 WP-A 判定完成且 WP-B/D/F/G 落地。**〔W792 核查批注：终止条件已满足——WP-A 于 W626 判定归档·WP-B/D/F/G 及全部 WP-A~M 已收官（W790/W791 实证）·本配额规则到期终止·不再构成批次配额约束〕**

### 优先级零：战略方向（来源：references/例-佛法AI框架原始对话.txt 中的产品分析）

> 以下判断来自对项目实际状态的审计，非模板化扩容建议。

**核心问题（曾为唯一阻塞·W402 已解除）**：项目曾是"静态博物馆"——86 个可视化页面数据硬编码，RAG 后端（scripts/rag/）虽已前端接入（W336 渡口问津 + W358 修复 draft 主回答渲染 + 多轮 history 接缝），但**真实 LLM 生成路径曾未接通**（answer() 仅有 BM25+图谱检索占位，档 B 待 LLM_API_KEY）——**已于 W402 解除**（provider 化 Base URL·LLM_API_KEY 配于本地 .env 即接通真实生成，key 存在即生成/无 key 回退模板）。另有平行入口 `xiyouji-agent-web`（Web Agent「西游记·渡口问津」·OpenAI-compatible 自研引擎·引擎三键配于服务端 .env（W680 起）·PROJECT_CWD 指向本项目）可绕过 scripts/rag 直接对话/检索 docs/ + 跑 scripts/ + 写 dataset/——两条"能问"路径可并行。内容扩容（A3/A4 继续加篇）的边际收益已趋近于零。

**建议方向（按优先级）**：

1. ~~**提交存量**~~：✅ 已完成（W321-W334 全部 commit，2026-08-03）
2. ~~**RAG 前端接入**~~：✅ 已完成（W336·site/static/js/rag-chat.js「渡口问津」·index+dashboard 已嵌入·端到端验证通过）
3. ~~**数据产品化**~~：✅ 已完成（W336·dataset/ 40 个 JSON + README 数据手册·scripts/extract_datasets.js）
4. **停止模板化扩容**（策略决定）：A3 215 篇已冻结；A4 原冻结 199 篇，**用户于 W342 放宽冻结例外**：允许填补长期引用空缺的非模板化篇目（权力五联对照 W084·自 W089 起即以 W084 编号互链却长期未成稿 + 妖怪身份政治 W342 身份政治总论），A4 现 209 篇。不再按"四位理论家+七段式"模板生产新篇目。

**下一阶段方向（W340+）**：

- **手搓绕过级联治理批（候选·W965 立项登记）**：并行会话手写版本面绕过 batch_cascade 的模式治理——实证三起（W955 手搓版本面同步破坏 README·A1-A6 锚尾与 STRUCTURE 现势行、W961/W963 连环手搓致 HEAD 句尾失范与尾链 4 条粘连、里程碑块只插不旋致窗口积 19 块）；候选方案三层：① 级联单写路径文件锁（级联运行期对十面文件加锁·他方写即拒）、② 版本行契约硬门禁挂 verify（·A1-A6 锚尾/HEAD 句尾/尾链 ≤3 的形态判据——现在只在级联 assert 与 review 时现形）、③ 手搓前置劝导（preflight 检测工作树含十面文件未提交改动即提示「请走 batch_cascade」）；评审口径：②最薄（纯判据不挡路）优先，①最强但需处理级联自身的临时索引写。
- **内容质量深化（非增量）**：A1 逐回补交叉引用/结构化元数据、A5/A6 提质、全站死链与术语统一

### A 方向：docs 内容扩容

#### A2 个人随笔扩容（A2 Batch 1-10 已完成 W066-W086）

已创作 44 篇差异化主题随笔，A2 矩阵扩展到 43 维度。Batch 1-10 系列收束。

**W073 方法论升级（毕业）**：Preflight 双轨验证（W072 教训吸收）—— Preflight 阶段验证 line 号引用时必须双轨：Grep 验归属 + Read 验内容匹配。已毕业到 [docs/10-方法论沉淀/Preflight与Subagent模板.md](docs/10-方法论沉淀/Preflight与Subagent模板.md) 第三节。

#### A3 人物分析深化（已完成 W075-W077 + W040 + W132-W160 + W179 + W237-W252 + W285）

docs/02-人物深度分析/ 已有 215 篇。可继续深化方向：

- 明代历史原型对照深化（如王阳明 vs 唐僧心学/张居正 vs 玉帝权术/海瑞 vs 悟空直谏）
- 女性人物专题扩容（铁扇公主/白骨精/玉面狐狸等深化）
- 取经五众心理深度画像补遗

#### A4 主题专题扩容（已完成 Batch 1-20，W078-W190 + W285-W286）

docs/03-主题与情节专题/ 已有 209<!--stats:a4_docs--> 篇。已完成方向：


**A4 方向系列建议**：Batch 1-20 已完成 101 篇主题专题（含十六维叙事学框架 + 全新领域开拓四篇：生态批评/后人类主义/物质生态学/动物研究）。W285-W286 新增 89 篇（68 篇主题系列 .txt 拆分 + 21 篇详解.txt 随笔拆分），W359-W383 再增 8 篇（W369-W383 第二批 5 篇 + 边缘人物/理论新视野方法论），累计 209 篇。下一 batch 候选可继续新维度扩展（如取经网络叙事学专题·基于海尔斯技术生成认知 / 取经地理批评专题·基于韦斯特法尔地理批评 / 取经情感结构专题·基于雷蒙德·威廉斯情感结构理论）。

#### A5 文化与历史背景扩容（已完成 W094-W096 + W126 + W130 + W134 + W142 + W146 + W150 + W154 + W180·八层明代镜像完整闭环）

docs/04-文化与历史背景/ 已有 34 篇。可扩方向：

- 佛道思想深化（禅宗公案 vs 内丹学/三教合一明代思想史）
- 明代社会史镜像（市井百态/科举制度/海禁/卫所制）
- 版本演变史补遗（西游记古本/评点本/海外译本深化）

#### A6 诗词歌赋扩容（已完成 W097-W098 + W288 + W351/W356/W357 英文译介全覆盖）

docs/05-诗词歌赋/ 中文专题已齐备，**英文站译介（site/en/ E6/E31/E33/E34-E37）已全覆盖全部诗词专题**：人物赋(E34)/韵律分析(E35)/主题创作(E36)/原著赏析(E37)/景物诗(E6)/开篇诗(E31)/意象谱系(E33)。中文侧无新增 gap，英文侧亦无剩余未译专题。


### V 方向：可视化深化（site/data/ 87 页）

- **V1 现有页面内容深化**：dashboard KPI 卡片数据更新 / 可视化交互增强（hover/click/筛选）
- **V2 新增可视化维度**：西游地理 3D 可视化（Cesium/Three.js）/ 人物关系动态网络（d3-force）/ 八十一难难度热力图深化 / 取经路线时间-空间双轴
- **V3 跨页面导航增强**：footer 关联链接补全 / 标签云 / 智能推荐
- **V4 移动端体验**：375px 视口回归 / 触摸交互优化 / 移动端专属可视化（竖版图表）

### E 方向：工程化（E1-E8 已完成）

- **E9 治理经验移植**（W663 立项·2026-10-05·D1-D3 已裁决）：GateKeeper/绿洲/大赛三仓治理评阅反向移植——W 编号对账表 + doc-sync 口径体检（第 31 槽·含提交-版段对账）+ verify 段计数自洽锁 + CI 加固（actions SHA 钉/permissions 收敛/security dispatch）；方案 [2026-10-05-governance-experience-transplant-plan.md](archive/docs/plans/2026-10-05-governance-experience-transplant-plan.md)（W735 归档至 archive/docs/plans/）；含 W659/W660 版段追记合并段（D1 裁决）

### S 方向：分享发布

- **S2 关键随笔/专题发布**：挑选 12 篇 A2 个人随笔 + 15 篇 A4 主题专题，发布到博客/公众号/知乎
- **S4 学术投稿**：基于 docs/04-文化与历史背景/ + source/引用与网络解读/学术论文索引.md 50 条，撰写学术论文投稿

### Backlog：登记不开工（裁决留档·动工须用户另批）
- **BL-21 门禁豁免清单周期盘点（已执行·W710）**：首份盘点报告 docs/00-导读/门禁豁免盘点-2026-10-11.md——结论=豁免面健康无吞噬证据·第 28 已收敛标杆·第 22/C5c 起步态跟踪·第 29 大基线待专项收敛；BL-21 关闭（转例行动作·下次盘点随大版本段归档或 2027-01 季度点）。
- **BL-25 阅读契约配套正文手术（已执行·W710）**：STRUCTURE 02/04 段建置沿革迁 ARCHIVE（正文换现数+指针）+README 拆分评估结论=**维持不拆**（外链/统计口径/EXPECT_A4 字面量位置影响>收益·面向读者与开发者分段契约已由 W707 头部承担）。契约头部已随 W707 落 10 份。

- **BL-1 `EMBEDDED` vs `EMBEDDED_DATA` 命名分裂**（26 vs 41 文件）：全站 sed 触碰面大且需全站 CSP 重算，收益为纯一致性（W676 WP-4.5 登记）。
- **BL-2 `fetchJson`/`loadJson` 命名统一**：纯一致性重构，触碰全部 F6 骨架页（W676 WP-4.5 登记）。
- **BL-3 og:image 全站同图差异化**：需美术资源产出分页封面，非工程单批可闭合（W676 WP-4.5 登记）。
- **BL-4 GitHub blob URL 全站统一 `encodeURIComponent`**：浏览器地址栏自动编码为全站统一既有模式，单页改动反致不一致（W674 WP-3.15④ 登记·W676 WP-4.5 归位合并）。
- **BL-5 a11y 盲区增强：JS 生成色静态审计照不到**（social-media 徽章 ≈1.8:1 类，需运行时对比度审计）（W677 WP-5.3③ 登记）。
- **BL-6 角色/洞府/法宝三 master 表 + ID/aliases 体系**（跨文件一致性基建·触碰 dataset/ 全域）（W678 WP-6.5 登记）。
- **BL-7 character_cards 卡池补全与平衡性**（如来被动、大鹏性价比、白龙马 passive 位、芭蕉扇借机制）（W678 WP-6.5 登记）。
- **BL-8 counterfactual 五处表述**（如意真仙归类、青狮白象「无主」、二郎神八九玄功、阴阳二气瓶时辰、灵山若干难计数）（作者裁决项·W678 WP-6.5 登记）。
- **BL-9 domino C1 紧箍咒时点 / C3 因果牵强**（作者裁决项·W678 WP-6.5 登记）。
- **BL-10 章节格式统一（`第001回` 补零形态）**（触碰面广·纯一致性）（W678 WP-6.5 登记）。
- **BL-11 稀柿衕用字**（作者裁决项·W678 WP-6.5 登记）。
- **BL-12 全局 ID 体系（MONSTER_*/LOC_*/CHAP_*）+ JSON schema + data_dictionary + version/source_files 元数据**（第九轮设计建议·W678 WP-6.5 登记）。
- **BL-13 `tone` 字段（serious/humorous/satirical）与主观评分量纲定义**（intensity/axis_*/workplace_fit/stress+ease）（W678 WP-6.5 登记）。
- **BL-14 journey_route/geo_3d 章节口径统一**（两界山 13/14、浮屠山 19/20、号山 39/40-42、灭法国 84/85——到达 vs 事件完成须作者裁决）（W678 WP-6.5 登记）。
- **BL-15 spiral_progress vs team_effectiveness 阶段口径注记**（心性 vs 团队效能两维度）（W678 WP-6.5 登记）。
- **BL-16 content 合规三项**（后宫流合规提示、金汁→金汤、trip_report alert_level 统一）（W678 WP-6.5 登记）。
- **BL-17 food_vlog 评分制与章节排序**（W678 WP-6.5 登记）。
- **BL-18 dialogue_sentiment 缺第 9/10/11 回补提**（归属管线该三回 0 条带引号归属语·生成器重跑确定性复现·补提需扩归属算法）（W678 WP-6.3 登记）。
- **BL-19 text-search.json 与 source/原文/分回 两真源分歧**（text-search 第 1 回为节选本 1584 字 vs 分回 md 7288 字含「惊动高天上圣…玉皇大天尊」段；第 20 门禁引文以 text-search 为准不受影响，但出场统计权威口径须二者择一或重建 text-search）（W678 WP-6.4 取证发现·作者裁决项）。
- **BL-26 内容质量方差（AI 平庸化）**（外部评审机制层批评①·2026-10-17·报告 §5.1 判定**成立**）：门禁保真不保质——「论点是否平庸/论证是否扎实/情感阐释是否有共鸣」是门禁的结构性盲区，属人审战场。**处置**：markdown写作规范 §4 增 5 条 AI 内容生产特有反模式（情节复述+主题套话/平庸安全结论/情感空转/流畅权威体/引文真推论假·W776 落地）+ 对抗性审查批持续抽检（W737/W760 先例）；**不设工程关闭项**（质量是过程属性非一次性缺陷）。
- **BL-27 工程化 overhead 可持续性**（外部评审机制层批评②·2026-10-17·报告 §5.2 判定**成立·主动权衡**）：W### 双索引 + 49 段门禁的首要目的是**断点可恢复性**（一人多线现实约束），不是表演；代价=贡献者曲线陡峭、维护者精力转移即停摆（评审引「赛博好人」前车之鉴）。**处置**：记录在案；每次新增门禁/机制前自问「是否为可恢复性服务」（E36-E42 铁则同款）；**不设工程关闭项**。
- **BL-28 单点故障**（外部评审机制层批评③·2026-10-17·报告 §5.3 判定**成立·无解已缓解**）：项目存续系于单一维护者；数字人文个人项目常见失败模式（机构支持短期化/劳动不被晋升路径承认/人员变动致项目偏移）全中。**处置**：缓解=公开仓库+CI+全文档化到「新 Agent 可接管」程度（HANDOVER/对账表/门禁体系即为此设计）；无可执行工程项，**不设关闭项**——记录在案作为一切工程决策的约束背景。
- **BL-29 agent-web 攻击面负向测试缺口**（外部评审第三轮 §4.4·2026-10-18·W790 报告）：CORS 预检绕过、超大 RAG top_k、SSE 超时未清理三类负向测试在 agent-web 测试面不存在（关键词实证·38 个 node --test 用例仅覆盖工具权限/audit/citationGuard）；W411/W412 修复无回归固化，重构回退风险真实存在。**处置**：补负向测试 + CI 接线，列为下个 agent-web 触及批伴随项（同 W787 停止 churn 纪律·不单独开批）。
- **BL-30 依赖卫生两小项**（外部评审第三轮 §4.1·2026-10-18·W790 报告）：① E2E job `npm install playwright @playwright/test`（ci.yml:47）未钉版，与 scripts/package.json ^1.63.0 不一致，浏览器版本随 CI 日期浮动（10 个视觉基线长期稳定·容差内未见影响）；② 依赖清单分散三处（scripts//agent-web//site 零依赖）无根级指针。**处置**：钉版对齐 + README/CONTRIBUTING 加一行索引；低优先·随依赖变动批顺带。
- **BL-31 sync_docs.py 状态处置**（外部评审第三轮 §4.7·2026-10-18·W790 报告）：该脚本为校验器（6 文档一致性）非 CI 接线（仅 Makefile release·本机无 make）、存量 exit=1 失败态未清（W787 对拍记录）、无单测；活跃同职责门禁 check_doc_sync（第 31 槽·18 负样本）健康度不受影响。**处置**：退休/接线/修复三选一·用户裁决时机。
- **BL-32 截图审查触发粒度**（外部评审第三轮 §4.3 附带观察·2026-10-18·W790 报告）：纯页脚链路文本改动（如批次级联插 token）触发 9 分钟截图审查全量；可评估 paths 过滤细化或宽容档。**处置**：低优先·下次改 screenshot-review.yml 时评估。
- **BL-33 system.css 与页面内联块漂移（inline_css --force 回吞迁移成果·W876 实证·2026-10-22）**：W862-W875 设计迁移只改页面文件（含 INLINED 副本）未写回 `site/system.css`（自 W856 停更）——任何一次 `inline_css.py --force` 都会把迁进内联块的规则整段冲掉（`.page-wrap` 容器令牌化→1320px 字面量·`.seal` 淡底→实底·朱砂实底审计 457→710 即现形；W876 中途一次全量 --force 已污染 328 页暂存区·修复=自 HEAD 重建 + 靶向替换令牌值 + 静态 diff 审计证「三类之外逐字节一致」）。附伤：W875 给 inline_css 加的「根级页面直接 skip」早退把根级 INLINED 页（dukou-engine）重同步路径堵了（W876 已手工靶向修复）。**处置**：后续迁移批二选一——① 迁移同步写回 system.css（治本·推荐）② 禁全量 --force 改靶向同步（治标）；inline_css 根级 skip 早退修条件（有 INLINED 标记的根级页应放行）；W879 阶段 5 门禁批顺带评估接线。


**S 卡拍板记录（W693·2026-10-10 用户裁决）**：候选三卡 S-16 残留扫**吸收为第 38 门禁**（check_embedded_stale_markers.py·本批挂载）；S-17 内嵌重灌器/S-18 契约冒烟精化**登记为工具化排期项**（下个数据面批次顺带）；存量 S-04~S-15 十二张**全部关闭不建置**（skills/ 已 W562 退役——其可行能力已被既有载体吸收：S-04→test_site_quality 断言、S-05→断言式脚本模式（AGENTS §4.3）、S-06→e2e 探针规约、S-07→S4 docx 工具链（A-05 本批复用）、S-08→sync_data_json.py（W678）、S-09→派发边界（AGENTS §4.3 W671）、S-10→engine.smoke 十二断言（W680）、S-11→告警裁决两账实证（W681/W690）、S-12→手工级联模板两代（_w676/_w691）、S-13→渠道要求落夹（W687）、S-14→第 21 动态链接门禁、S-15→S2 分发冻结无触发。）

### 优先级建议

- **短期（W287+）**：A4 主题专题 Batch 16+ 扩容 / A5 文化背景 Batch 2+ 扩容 / A6 诗词歌赋 Batch 2+ 扩容 / V1 可视化深化
- **中期**：V2 新增维度 + E1 截图审查 CI 化
- **长期**：E2 a11y + S2/S3/S4 分享发布

---
## 三、方法论沉淀

> **经验总入口（W755 指针化·W973 真指针化收口）**：现役坑位与门禁读
> [docs/agent/pitfalls.md](docs/agent/pitfalls.md)（64 条·六主题）与 [docs/agent/gates.md](docs/agent/gates.md)（50 槽）；
> 诊断 SOP 读 [docs/10-方法论沉淀/](docs/10-方法论沉淀/README.md)；
> 本区历史叙事全文已迁 archive/docs/HANDOVER-ARCHIVE.md（W973·grep 查）。
## 四、待办事项（短期）

- [x] v0.9.1 runtime 验证回归（cross-time-danmaku + dashboard 浏览器复测·2026-07-29 子代理浏览器 spot-check PASS·控制台无 ERROR·网络无 404/500·三个 signature moments 渲染正常·Name That UI 五组件生效·搜索框筛选"叙事学"触发空状态）
- [x] W285 人物/主题系列 .txt 源文件整理迁移（14 个根目录 .txt 精细拆分·A3 76→197 篇 + A4 101→169 篇）
- [x] W286 source\原文 整理为.md + 补充原文内容（详解.txt 21 篇 + 5 个深读拆分 100 SD 切片 + 100 回原文 + 合并到逐回解读.md）
- [x] W286b 格式修复（分回/*.txt→.md + temp_shendu/→shendu/*.txt→.md）
- [x] W286c 审查修复（清除第069/099回网页垃圾 + 第099回追加缺失深度解读SD075 + 7个源.txt删除）
- [x] W287 pre-commit 自动化校验门禁建立 + 文件计数声明修复（scripts/pre-commit-validate.py + .git/hooks/pre-commit 钩子 + E3 双重门禁 + A3 197→196/A4 190→189 声明修正）
- [x] W358（v2.3.9）git commit + push（静态优先健壮性加固全部改动已提交，W359-W400 均已跟进 commit/push）
- [x] RAG 真实生成（档 B·W402 已解除阻塞）：provider 化 Base URL + LLM_API_KEY 配于本地 .env（gitignored）即接通 `answer()` 真实 LLM 生成（stdlib urllib 打 OpenAI 兼容/Anthropic 原生双适配器·零依赖）+ 可选 embedding 向量检索增强（W402 落地：key 存在即生成·无 key 回退模板·rag-chat.js 渲染 llm_generated）
  - **平行替代入口（推荐先试）**：`xiyouji-agent-web`（Web Agent「西游记·渡口问津」·OpenAI-compatible 自研引擎·凭证 `LLM_API_KEY`·`PROJECT_CWD`=仓库根（自动解析）直接对话/检索 docs/ + 跑 scripts/ + 写 dataset/）配好引擎三键即开箱"能问"（W680 起），与 scripts/rag 档B 二选一或并行（无需本仓库 LLM_API_KEY）；详见 `xiyouji-agent-web/README.md`

- [x] 英文站续译：site/data 86 张可视化页英文化全部完成（W445 relationships 收官）+ 52 个旧 EN 页 CJK 清理（W446·138 EN 页全过 validate_en.py）
- [x] **agent-web 技术栈大版本迁移（W536 出档·W543-W548 五阶段完成·W568 走查关闭·dependabot ignore 已解除）**：勾选补记 W651（原条目陈旧：迁移已于 2026-09-05 落地·现役栈 Express 5/TS 7/Vite 8/React 19/Tailwind v4）——评估见 [docs/10-方法论沉淀/agent-web技术栈迁移评估.md](docs/10-方法论沉淀/agent-web技术栈迁移评估.md)
- [x] 真实读者量验证：注册 GoatCounter（W425/W426 接入+自托管修复·W626 以真实数据完成 judge_gate 判定）——勾选补记 W651（原条目陈旧）

---
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

> **雷区权威 = [docs/agent/pitfalls.md](docs/agent/pitfalls.md)（64 条·六主题·含 shell 场景查坑表）**；
> 本区历史雷区叙事已迁 archive/docs/HANDOVER-ARCHIVE.md（W973·grep 查勿通读）。
## 九、使用说明

### 跨 session 接续流程

1. **新 session 启动时**：先读本文件 + [README.md](README.md) + [docs/00-导读/项目说明.md](docs/00-导读/项目说明.md)，了解当前进度与待办
2. **接续 W 编号**：以本文件「一、当前进度」段标注的现役 W 为准；新批编号按 [CHANGELOG.md](CHANGELOG.md) 顶部「W### 编号规则」取现役段 max+1。**本文件禁止内嵌具体 W 号**（W520「递增数字禁字面量」铁律——写死的批次号必然随项目演化漂移；本行即该规则的存量病例，W534 修复）
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

> 本文件创建于 2026-07-25（v2.0.41 W068 后），用于跨 session 交接。每次完成新 W### 后更新。最后更新：2026-10-27（W980 stats 标记同步机器化批）；2026-10-27（W979 收官提示位扩展批）；2026-10-27（W978 第 44 篇工作复盘批）
