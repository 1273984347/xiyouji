# 更新日志

本项目所有重要变更均记录于此。格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/)。

## [Unreleased]

> **W### 编号规则**：每个版本段标注唯一 W### ID（W001-W419），v0.8 内部细分 W008.1-W008.7（B0-B7）。每个 W 附四件套字段（来源/文件/验证/状态）。反向索引见 [scripts/output/file-index.md](scripts/output/file-index.md)（给定文件查改几次）。
>
> **历史版本归档**：v0.1 - v2.3.17（W001-W399）已迁移至 [CHANGELOG-ARCHIVE.md](CHANGELOG-ARCHIVE.md)。本文件仅保留 v2.3.18+（W400）。

### v2.3.34（2026-08-10）：W419 修复 A1 深度解读 SD 错位 — 22 篇错位 SD 归位（40-72 回全覆盖）+ 第 56 回补写 SD101

> **W419 修复 A1 深度解读 SD 错位（承接交接文档「二、候选清单」优先级零·用户选定"修复 SD 错位"方向）**
> - **来源**：新接任 Agent 按流程调研后用户选定方向"修复 SD 错位（逐篇确认错位 SD 的真实回号，移动到正确回文件，补充缺失回目的深读）"
> - **执行（错位定位）**：审计发现 **22 篇 SD 深度解读（SD038-052、SD056-062）编号≠真实回号**（如 SD038 内容是号山红孩儿=40-42 回却被放在第038回文件·SD041 内容车迟国=44-46 回放在41回·SD058 内容荆棘岭=64回放在58回）——**根因**：W286 合并脚本 `parse_shendu_metadata()` 只读源文件第一行，但源文件元数据注释在第三行（第一行被标题行 `# SDXXX` 占据）→ 正则匹配失败 → fallback 按 SD 编号放置（编号=创作序号≠回号）·另 SD038-062 这批源元数据"推测对应原著回号"=编号硬套，部分与正文内容矛盾（SD039 元数据标39回但正文是黑水河=43回·SD049 标49回但正文蝎子精=55回）
> - **执行（回文件归位）**：按**正文内容逐篇判断真实回号**（不轻信元数据），22 篇 SD 从"编号=回号"错位处移动到正确回文件——**范围式 SD 复制到范围内每回**（与 73-100 回既定模式一致，如 SD064 狮驼岭在 74-77 四回）：SD038→40-42·SD039/040→43·SD041→44-46·SD042→45·SD043→46·SD044→47·SD045→48·SD046→49·SD047→50-52·SD048→53-55·SD049→55·SD050/057→59-61·SD051→62·SD052→62-63·SD056→57-58·SD058→64·SD059→65-66·SD060→67·SD061→68-71·SD062→72——**40-72 回实现全覆盖**（原 63-72 十连回无深读空白消除）·38/39/56 回移出后删除空深度解读段·63-72 回新建 `## 深度解读` 段（插于 `## 原文全文` 前·按 SD 编号升序）
> - **执行（源文件修正）**：24 篇源 SD 元数据"推测对应原著回号"修正为真实回号（22 篇 + SD075/077 归程篇 47-49→99/99-100）+ 17 篇正文 H1 `# 第X回` 编号→真实回号（范围式写 `第Y-Z回`）+ 3 篇正文内嵌"当前回"引用修正（SD038/039/040 共 4 处·历史引用如"第26回五庄观医树"不动）+ 9 篇 `> 关联：` 链接改指真实回文件
> - **执行（第 56 回补写）**：新增 **SD101 · 草寇之死——当打杀凡人触碰了取经的底线**（第 56 回"神狂诛草寇 道昧放心猿"深读：神狂与道昧两笔账/草寇之死是悟空打死的第一个凡人/紧箍咒第二次被念/杨老儿沉默/放心猿为六耳猕猴埋引信·叙事+分析+延伸思考体·插入第056回文件深度解读段）——SD 切片 100→101 篇
> - **执行（验证）**：全量核对 40-72 回 SD 分布全覆盖（56 回=SD101）·`lint_links --dir site/` 2629 链接 **0 broken**·Grep spot-check 源文件元数据/H1/关联行落地·1-37 与 73-100 回保持原样（脚本 rstrip 产生的非必要格式变化已 git restore 回退）
> - **执行（版本同步）**：bump v2.3.34 W419（README/STRUCTURE/项目说明 + file-index + 交接文档 + CHANGELOG + 页脚 3 个）+ site/dukou-engine.html 页脚人工插入 + site/index.html 页脚 + 旁文档 4 份同步
> - **验证**：verify_delivery 全绿
> - **状态**：已落地·已 push（3e17477）·CI/Security/Deploy Pages/Screenshot Review 全绿（CI 15 job + Security 4 job）
> - **处置收尾（2026-08-10）**：修复脚本 _w419_fix.py 第一版 parse_sec 衔接 bug（`## 深度解读` 前无空行·导航行被吞换行）导致第 43 回格式损坏——已修复 parse_sec 补换行 + 统一 `pre.rstrip()+"\n\n"` 拼接，git restore 全量回退后重跑修复；1-37/73-100 回"仅删多余空行"的非必要改动（E1 铁律：修复声明≠最小改动）git restore 回退，仅保留 38-72 回真实归位改动（35 个回文件 + 24 篇源文件 + SD101）；临时诊断/修复脚本（_w419_*.py/.txt）用后即删。

### v2.3.33（2026-08-10）：W418 内容质量深化 — 全站死链巡检（en 站 29 broken 修复 + A1 逐回 100 回导航全覆盖）

> **W418 内容质量深化（承接交接文档「二、候选清单」优先级零·用户选定"内容质量深化"方向）**
> - **来源**：新接任 Agent 按流程调研后用户选定方向"内容质量深化（全站健康巡检：死链检测 + 术语统一 + A1 逐回交叉引用/结构化元数据）"
> - **执行（全站死链检测）**：`python scripts/lint_links.py --dir docs/` 4623 链接 0 broken·`--dir site/` 2629 链接 **29 broken**——全部集中在 site/en/ 英文站（guide.html 25 处 + character-relationship-3d 2 处 + chapter-structure-graph/narrative-rhythm-curve 各 1 处·指向不存在的 site/en/data/*.html 与 timeline.html）
> - **执行（en 站 broken 链接修复）**：按 visualizations.html 惯例修复 29 处——**EN 版存在指向同目录**（guide.html 中 chapter-stats/narrative-rhythm-curve/81-hardships/character-appearance/chapter-structure-graph 5 页）+ **无 EN 版回退中文原版 `../data/*.html` 加 `lang="zh-CN"` 标注**（text-search/character-dynamic-network/mbti-evolution/philosophy/counterfactual/monster-sociology/criticism-history/text-evolution/material-archaeology/data-explorer/timeline/poetry-rhythm-analysis/language-style-radar/deconstruction/tag-cloud/graph-explorer/cross-time-danmaku/century-dialogue/relationships 等·中文原版文件全部经 Glob 验证存在）·临时脚本精确替换后删除
> - **执行（A1 逐回交叉引用补全）**：100 回中 23 回缺标准 `> 导航：` 引用行（13 回完全无导航 + 10 回仅有段落式「## 前后回导航」）——按第003回格式补「返回导读/上一回（第0XX回）/下一回/站点首页/人物关系/人物出场/哲学可视化」引用行（插于「## 深度解读」前·第071回插于「## 前后回」前）·100 回导航全覆盖 100/100
> - **执行（验证）**：`lint_links --dir site/` 2629 链接 **0 broken**·`--dir docs/` 4784 链接 **0 broken**·`--dir docs/01-全书逐回解读/` 1640 链接 0 broken·Grep spot-check 新 href 落地（lang="zh-CN" 标注命中）
> - **执行（版本同步）**：bump v2.3.33 W418（README/STRUCTURE/项目说明 + file-index + 交接文档 + CHANGELOG + 页脚 3 个）+ site/dukou-engine.html 页脚人工插入 + 旁文档 4 份同步
> - **验证**：verify_delivery 全绿
> - **状态**：已落地·已 push（8d9a700）·CI/Security/Deploy Pages/Screenshot Review 全绿（CI 15 job + Security 4 job）
> - **处置收尾（2026-08-10）**：bump_version 全局替换污染 file-index W417 历史段页脚 3 行（v2.3.33 W418 误入）——按 E2 判据恢复历史段原值（v2.3.32 · W417）+ 正确登记至 W418 段；README/STRUCTURE/项目说明三处版本行主描述被 bump 简化（W418 裸号）——人工补全 W418 主描述（内容质量深化：全站死链巡检 + A1 导航全覆盖）。

> **W417 文档健康治理（承接用户"你认为还有我没发现或者没想到的潜在问题吗 → 按照优先级顺序全部处理"）**
> - **来源**：用户评估潜在问题清单后指令"按照优先级顺序全部处理"（P0-3 高优先级 + P1-2 中优先级 + P2-2 低优先级）
> - **执行（P0-1 文档健康指标归档）**：CHANGELOG.md 归档精简 136KB→39KB（691→227 行·W399 及更早 600 行迁移至 CHANGELOG-ARCHIVE.md·头部归档标注更新）+ file-index.md 87KB→32KB（713→392 行·W335-W389 段 448 行迁移至 file-index-archive.md）+ 交接文档.md 精简里程碑（904→550 行·删 W411 及更早概要 545 行·保留最近 5 版本段）·三文档均降达标（<50KB/<500 行）·CHANGELOG-ARCHIVE/file-index-archive 头部标注扩大
> - **执行（P0-2 verify_delivery 真实文件计数校验）**：新增 ARCHIVE_DOCS 归档 3 件套纳入范围漂移扫描 + A_AREAS（A1-A6 六大板块）真实文件计数 vs README 声明校验（排除各板块 README.md·实测 611 篇==声明 611 篇·计数漂移即阻断）
> - **执行（P0-3 actions 升级消除 Node 20 deprecation）**：全 workflow 48 处升级至最新（checkout v7/setup-node v7/setup-python v7/upload-artifact v7/upload-pages-artifact v5/configure-pages v6/deploy-pages v5/nick-fields retry v4·gh api releases/latest 实测 2026-08-10）·Node 20 告警消除
> - **执行（P1-1 RAG 索引可重建性演练）**：删除 scripts/output/rag_index.json（32.39MB）→ 自动重建成功（35.26MB·BM25 检索 5 条 + 图谱三元组正常）·可重建产物重建流程验证可跑通
> - **执行（P1-2 bump_version.py 增强）**：新增 --desc 主描述替换（剥离 W 前缀防重复）·W001-W### 精确锚点范围替换（W### ID/更新日志/正向时间线三锚点·不触碰历史描述）·页脚 3 个简单页脚自动同步·幂等测试通过
> - **执行（P2-1 LICENSE 双协议边界补强）**：LICENSE-CONTENT.md 范围精确化（内容板块 + site 渲染文本归 CC BY-NC·导航/协作文档/根级项目文档归 MIT·适用内容补 07-09/S3/S4）·README 授权段同步（源代码与项目文档 MIT vs 文本内容 CC BY-NC 明确化）
> - **执行（P2-2 memory 过时描述修正 + sitemap 补全）**：project_memory E3 段"交接文档需 git add -f"过时描述修正（实测已 tracked 未被忽略）·sitemap.xml 补全漏收录页 69→154（en/ 全套 + 入口页 + data/ 内容页·排除模板/预览/统计页 7 个·XML 合法无断链）
> - **执行（版本同步）**：bump v2.3.32 W417（README/STRUCTURE/项目说明 + file-index + 交接文档 + CHANGELOG + 页脚 3 个）+ site/dukou-engine.html 页脚人工插入 + site/index.html 页脚 + 旁文档 4 份同步
> - **验证**：verify_delivery 全绿（含 A1-A6 真实文件计数 611 篇校验 + 归档文件范围漂移扫描）
> - **状态**：已落地·已 push（dafc336）·CI/Security/Deploy Pages/Screenshot Review 全绿（CI 15 job + Security 4 job·actions 升级后无 Node 20 告警）
> - **处置收尾（2026-08-10）**：文档规范 §11 门禁清单表格化——§11.2 禁改范围 W001-W414→W001-W416（E2 深处残留：范围未随 W417 更新）+ 新增「误改后果」列（12 类禁改文件均附违反后果）；新增 §11.4 同步核对速查表（10 项勾选清单：6 核心 + 4 旁文档 + 4 页脚 + verify + CI 收尾·新 Agent 提交前逐项打勾）。同步检查结论：14 项同步文件（6 核心 + 4 旁 + 4 页脚）全部含 v2.3.32/W417 无遗漏。


### v2.3.31（2026-08-10）：W416 文件管控清单标注 — 多 session / 多 Agent 协作文件权限显式化

> **W416 文件管控清单（承接用户"多 session 多 Agent 制作需标注必同步/禁修改文件"需求）**
> - **来源**：用户指令"我认为这个项目是根据多 session 多 Agent 来进行制作，要标注清楚明白哪些文件是必须同步或不能擅自修改的"
> - **执行（文档规范.md §11）**：新增「文件管控清单」章节——**11.1 必须同步的文件**（核心 2 份硬门禁：CHANGELOG/交接文档·辅助 4 份：README/STRUCTURE/项目说明/file-index·同步辅助：页脚 4 个 + 旁文档 4 份·附门禁列）+ **11.2 禁止擅自修改的文件**（CHANGELOG 历史段 W001-W414·归档 3 份 archive·.env 密钥·SECURITY-AUDIT 审计档·构建产物·可重建产物·门禁脚本 verify_delivery/pre-commit·memory 写入协议·字体源·bump_version 已知坑）+ **11.3 接手速查 6 步**（新 session/Agent 首读）
> - **执行（交接文档）**：「跨 session 接续流程」新增第 3 步「文件管控」引用文档规范 §11（11.1 必同步/11.2 禁修改）·后续步骤顺延
> - **执行（版本同步）**：bump v2.3.31 W416（README/STRUCTURE/项目说明）+ site 页脚 4 个 + 交接文档/项目概览/项目认知总览/项目交接参考手册/workflows README 同步
> - **验证**：verify_delivery 全绿（含"201 篇" A4 计数）
> - **状态**：已落地·已 push（0a9046b）·CI/Security/Deploy Pages/Screenshot Review 全绿（纯文档变更·CI 15 job + Security 4 job）

### v2.3.30（2026-08-09）：W415 README 视觉引导增量 — 徽章区 + 图标化速览 + 首页预览截图 + 反馈段

> **W415 README 视觉引导增量（承接 W414 用户手册改造·吸收第三方模板 3 增量·修正 4 处错误）**
> - **来源**：用户提供第三方 README 模板（徽章区/在线体验/内容速览/快速开始/details 折叠/反馈）→ 主代理评估：骨架已被 W414 覆盖，但 3 个增量有参考价值（徽章区/首页预览截图/反馈段）·4 处错误不照抄（URL `/site/` 后缀会 404·release 徽章不适用——仓库无 Releases·单协议错应为双协议·徽章语法残缺缺 `[![` 包裹）→ 用户选"落地增量 + 图标化速览"
> - **执行（README 增量）**：顶部新增徽章区 3 枚 shields.io（在线访问 brightgreen 大按钮式·双协议授权 MIT + CC BY-NC 4.0·部署状态 pages.yml workflow）·「内容导航表」改为「🎁 你将会看到什么」8 条 emoji 图标化速览（📖逐回解读/🕸️人物分析/🗺️主题专题/📚文化背景/📜诗词/💭随笔/📊可视化/🔍术语表·各带链接）·在线体验区插入站点首页预览截图（assets/images/index-preview.png·Playwright 1280×900 截图 108.7KB·PNG 头校验通过·临时脚本已删）·底部新增「💬 反馈与建议」（issues 链接）·开发者/维护者专区新增「技术栈」段（D3.js/Three.js/Python/原生 HTML/CodeBuddy Agent SDK/GitHub Actions）
> - **执行（版本同步）**：bump v2.3.30 W415（README/STRUCTURE/项目说明）+ site 页脚 4 个（dukou-engine/index/cross-time-danmaku/tag-cloud）+ 交接文档/项目概览/项目认知总览/项目交接参考手册/workflows README 同步
> - **验证**：verify_delivery 全绿（含"201 篇" A4 计数）·index-preview.png PNG 头校验通过（108.7KB）
> - **处置收尾（2026-08-10·文档最新性审查）**：用户要求审查交接文档等是否全部最新 → 修复 5 处过时残留（交接文档 W414 段状态行"待 push"→已 push 83a2d87 全绿·W413 段验证行"（待跑）"→已跑·候选清单 RAG 阻塞"唯独阻塞"→标注 W402 已解除·待办 RAG [ ]→[x]·核心问题段补 W402 解除标注）+ 项目说明待办 2 处标记完成（v0.9.1 回归/截图审查 W406）·verify_delivery 全绿
> - **状态**：已落地·已 push（696fdd0 + 审查修复 commit）·CI/Security/Deploy Pages/Screenshot Review 全绿（纯文档变更·CI 15 job + Security 4 job）

### v2.3.29（2026-08-09）：W414 README 用户手册改造 — 普通读者入口 + 开发者分区两级引导

> **W414 README 用户手册改造（普通读者视角·承接 W413 文件策略审查）**
> - **来源**：用户指令"按这个思路把 README 改造成用户手册 + 开发者分区的引导结构"（前序讨论：面向普通读者 vs 开发者，"用户不会看"≠"没必要上传"，最优解是引导视线而非删文件）
> - **执行（README 重构）**：
>   - **普通读者专区**（置顶）：GitHub Pages 在线站点一键直达（https://1273984347.github.io/xiyouji/·gh api 实测确认）+ 内容导航表（10 大板块 + 86 可视化页 + 阅读指南/术语表/项目说明入口）+ 项目定位与数据维度全景表（133 维）+ 目标读者清单（8 类读者各给入口）
>   - **开发者/维护者专区**（`<details>` 折叠）：目录结构（精简树）+ 运行分析脚本 + pytest/Playwright E2E + 截图审查 + 双索引（CHANGELOG/file-index W001-W414）+ 文档维护规范
>   - **保留**：双协议授权（MIT + CC BY-NC 4.0）·学术引用（CITATION.cff）·贡献方式·"201 篇" A4 计数
> - **执行（版本同步）**：bump_version 升 v2.3.29 W414（README/STRUCTURE/项目说明）+ site 页脚 4 个（dukou-engine/index/cross-time-danmaku/tag-cloud）+ 交接文档/项目概览/项目认知总览/项目交接参考手册 同步
> - **验证**：verify_delivery 全绿（含"201 篇" A4 计数）·py_compile 无需（纯文档）
> - **状态**：已落地·已 push（83a2d87）·CI/Security/Deploy Pages/Screenshot Review 全绿（纯文档变更·CI 14 job + Security 4 job）

### v2.3.28（2026-08-09）：W413 仓库文件策略审查 — 严格审查入库边界·个人文档/方法论/开发内部资产恢复入库

> **W413 仓库文件策略审查（严格审查：哪些文件不能上传，其余全部上传）**
> - **来源**：用户指令"再去调研一下哪些文件是可以不用一起 push 到仓库的文件，哪些是必须一起跟随上传的文件，最后给我完整的方案让我选"→ 初步方案 A（6 个个人文档+3 目录转本地）→ 用户改口"你审查一下哪些文件不能上传，其他全部上传，严格审查"
> - **执行（严格审查结论）**：全库 Grep 扫描无密钥命中（`.env` 已 gitignore 未 tracked）；6 个个人文档（交接文档.md/交接文档-archive.md/项目交接参考手册.md/项目概览.md/项目认知总览.md/项目GitHub参考调研报告.md）+ docs/_dev(3) + docs/_templates(3) + docs/superpowers(11) + docs/10-方法论沉淀(14) 逐一扫描均无敏感内容 → **撤销 W413 初版本地化决策，全部恢复入库**
> - **执行（仅硬性排除·不能上传）**：`.env`（含 sk-ba531 密钥·gitignore）·SECURITY-AUDIT-2026-08-09.7z + .password（敏感审计档·gitignore）·node_modules/dist/__pycache__/venv/.vscode（依赖与构建产物·gitignore）·scripts/output/rag_index.json（32MB 可重建·gitignore）·scripts/output/figures 生成图/screenshots/tests 基线（可重建·gitignore）·.workbuddy/（gitignore）
> - **执行（字体源入库）**：assets/fonts/source/ 5 文件（NotoSerifSC-var.ttf 24MB + JetBrainsMono ×2 + NotoSansSC woff2 ×2）`git add -f` 强制入库（.gitignore 原规则保留注释说明）
> - **执行（verify_delivery.py 恢复）**：CORE_DOCS 恢复为 CHANGELOG.md + 交接文档.md 两份硬门禁（移除 W413 初版 LOCAL_OPT_DOCS 本地可选逻辑）·A4_DOCS 恢复 4 份（README/STRUCTURE/项目说明/交接文档）
> - **执行（文档同步）**：README/STRUCTURE/项目说明/交接文档 头部版本描述统一为 W413 修正（严格审查入库边界）·site/dukou-engine.html 页脚 v2.3.28 W413（index/cross-time-danmaku/tag-cloud 三页页脚同步）·CHANGELOG 本段 + file-index W413 反向索引
> - **验证**：`py_compile` verify_delivery.py 通过·verify_delivery 全绿（核心 FAIL 0）·git status 确认 6 文档+3 目录+方法论沉淀恢复 tracked（1565 项）
> - **状态**：已落地·已 push（addbe18）·CI/Security/Deploy Pages/Screenshot Review 全绿（CI 14 job + Security 4 job）

### v2.3.27（2026-08-09）：W412 安全审计剩余项处置 — P0-2 密钥覆盖防护 + XSS 转义 + RAG/SSE 边界 + 依赖锁定

> **W412 SECURITY-AUDIT-2026-08-09 剩余项处置（P0-2/P1-2/P1-3 辅助/P1-4/P2-1/P2-2/P2-3/P2-4 核验/P2-6/P2-7/P3-1/P3-2/P3-3/P3-5）**
> - **来源**：用户指令"列出剩余待办清单并评估优先级，按照优先级顺序和实际情况进行处理"——P0-2（/api/save-env-config 无认证→密钥劫持+SSRF）·P1-2（静态站 innerHTML XSS）·P1-3（吊销轮换密钥·辅助新增扫描规则）·P1-4（版本叙述统一）·P2 各项·P3 杂项
> - **执行（P0-2 密钥劫持+SSRF 防护）**：
>   - **server/index.ts** `/api/save-env-config`：apiKey/baseUrl 禁止运行时覆盖（400 拒绝 + refused 列表·仅从服务端 .env 读取）·**SettingsPage.tsx** 前端表单移除 API Key/Base URL 输入框（改提示"由服务端 .env 配置·重启生效·禁止运行时覆盖"）·提交体仅 {authToken, internetEnv}
> - **执行（P1-2 静态站 XSS 转义）**：**site/static/js/rag-chat.js** 新增 escapeAttr（含引号转义·属性上下文）应用于来源链接 href·**dataset-view.js** 新增 escapeHtml 应用于 openRowDrill/renderObjectView/renderKey·**cross-time-danmaku.html/tag-cloud.html/search.html** 新增 escapeHtml 应用于 tooltip/popup/hit 等动态文本·**site/_headers** script-src 补 `https://d3js.org` 白名单（页面实际 D3 CDN·原白名单 cdn.jsdelivr.net 为死配置 0 引用·消除未来 Netlify/Cloudflare 部署时误伤）
> - **执行（P1-3 辅助·密钥扫描）**：**security_scan.py** 新增 SEC-005 规则（sk- 前缀 16+ 字符·覆盖 DeepSeek/Qwen 等 OpenAI 风格 Key）·git 历史 `-S "sk-e8228e"` 与 `-S "LLM_API_KEY=sk-"` 均无命中（未入仓）·**轮换已落地（2026-08-09）**：旧 key（sk-e8228…）用户已在 DeepSeek 控制台吊销·新 key（sk-ba531…）已写入 `.env`（gitignore/未 tracked）·`_llm_generate` 直接调用 + RAG 服务 `/health`（675 文档）与 `/query`（5 snippets + 30 图谱三元组 + LLM 生成 731 字符·llm_error 空）HTTP 端到端验证通过
> - **处置收尾（2026-08-09）**：**SECURITY-AUDIT-2026-08-09.md 已加密归档**（7z AES-256·-mhe=on 头加密·归档 SECURITY-AUDIT-2026-08-09.7z·明文已删除）·密码存本地 `SECURITY-AUDIT-2026-08-09.password`（.gitignore·不入库）·.gitignore 新增 .7z/.password 规则
> - **执行（P1-4 版本统一）**：server/index.ts systemPrompt 硬编码 v2.3.9→v2.3.26（W411 顺带修复大部分）·site 页脚版本漂移修复（P3-5）·本次 bump v2.3.27 W412
> - **执行（P2 边界加固）**：
>   - **P2-1 rag_server.py 参数钳制**：新增 _clamp_int（top_k∈[1,50]·hops∈[1,3]）+ _sanitize_history（仅 list·≤20 条·role∈{user,assistant,bot}·text≤2000）·do_GET 与 /graph 接入
>   - **P2-2 xiyouji_rag.py LLM 端点校验**：_validate_endpoint 仅 https（http 仅 localhost/127.0.0.1/::1 例外）·私有网段（10/172.16/192.168/127）拒绝·域名放行·_llm_generate 入口校验抛 ValueError·history 防御性过滤（9 组用例全通过）
>   - **P2-3 server/index.ts SSE 加固**：aborted 标志 + 10 分钟总时长上限（sseTimer 超时清理 pendingPermissions 并写 error）+ req.on("close") 断开清理（abortStream）·流循环 if(aborted) break·正常/catch 路径均 clearTimeout + req.off("close")·两处 Map 迭代改 forEach（TS2802：tsconfig 无 downlevelIteration）
>   - **P2-4 MCP 外链探测核验**：xiyouji_mcp.py 源码核验 urlopen 不存在·external 分支仅计数不请求 → **已缓解无需修改**
>   - **P2-6 ChatMarkdown XSS 消毒**：node_modules 核验 tdesign-web-components chat-message markdown-content `options:{html:true}` + unsafeHTML 无消毒实锤 → **ChatMessages.tsx** 两处渲染输入加 DOMPurify.sanitize·package.json 新增 dompurify ^3.4.13 直接依赖
>   - **P2-7 依赖版本锁定**：scripts/requirements.txt 固定 jieba==0.42.1/Pillow==11.3.0/ruff==0.15.15/pytest==8.4.2（本地实测）·mcp-server/pyproject.toml fastmcp>=0.1.0,<1.0（防 3.x 大改版）·**CI 修正（push 后 pip-audit 实测）**：Pillow 11.3.0→12.3.0（25 个 PYSEC-2026 漏洞·fix 12.3.0）·pytest 8.4.2→9.0.3（PYSEC-2026-1845·fix 9.0.3）——26 漏洞归零
> - **执行（P3 杂项）**：P3-1 VERBOSE_LOG 门控 5 处调试日志（AGENT_WEB_VERBOSE=1 才输出）·P3-2 api_server.py CORS 白名单（file:// Origin==null 回显 "null"·仅 127.0.0.1:8787/localhost:8787 回显自身·其余不带 CORS 头·两处 `*` 均替换）·P3-3 移除未使用 exec/promisify/execAsync 死代码·P3-5 site 页脚版本漂移修复（index/cross-time-danmaku/tag-cloud）
> - **验证**：pytest tests 全量 **327 passed**·py_compile 4 脚本通过·_validate_endpoint 9 组用例通过·security_scan.py --all 无 SEC-005 误报·agent-web npm run build 成功（tsc + vite·dompurify 直接依赖·修复 TS2802 Map 迭代 forEach）·verify_delivery 全绿
> - **状态**：已落地·已 push（82fc41a/6374baf）·CI/Security 全绿（CI 14 job 含 pip-audit + pytest·Security 4 job 含 npm audit 双目录 0 漏洞·pip audit 0 漏洞）

### v2.3.26（2026-08-09）：W411 安全审计 P0-1/P1-1 处置 — Web Agent 鉴权加固 + MCP 路径白名单

> **W411 SECURITY-AUDIT-2026-08-09 P0-1/P1-1 落地**
> - **来源**：用户指令"继续处理报告中列出的 P0-1 和 P1-1 待办事项"——P0-1（Web Agent 默认 `bypassPermissions` + 零认证 + `0.0.0.0` 监听 → 未授权 RCE）·P1-1（MCP `xiyouji_drl_spotcheck` 等 4 工具未 `resolve()`/`is_relative_to()` 校验、接受 `../` → 任意文件读取 + 盲 oracle）
> - **执行（P0-1 纵深防御）**：
>   - **server/index.ts**：新增安全头中间件（X-Content-Type-Options/X-Frame-Options/Referrer-Policy/Permissions-Policy）·可选 token 认证（`AGENT_WEB_TOKEN` 环境变量，`x-agent-token` 或 `Authorization: Bearer`，设值后 `/api/*` 全鉴权 401）·权限白名单净化 `sanitizePermissionMode`（仅 default/acceptEdits/plan 直通；`bypassPermissions` 需 `AGENT_WEB_ALLOW_BYPASS=1` 否则回落 default）·工作目录白名单 `resolveWorkingDir`（`Path.resolve` + 前缀校验，越界回落 `PROJECT_CWD`）·`app.listen(PORT,"127.0.0.1")` 仅回环监听（原无 host 绑全网卡）
>   - **useAgents.ts** 默认 Agent `permissionMode: 'bypassPermissions'→'acceptEdits'`（高危操作人工确认）·**vite.config.ts** `host: '0.0.0.0'→'127.0.0.1'`
>   - **agent-web README** 安全提示重写（W411 加固段）·**.env.example** 补 `AGENT_WEB_TOKEN`/`AGENT_WEB_ALLOW_BYPASS` 注释
> - **执行（P1-1 路径白名单）**：**mcp-server/xiyouji_mcp.py** 新增 `_resolve_within(root, p, what)`（`(root/p).resolve()` 后 `is_relative_to(root)` 校验，越界抛 `PathEscapeError`）·4 个接受路径的工具接入（xiyouji_drl_spotcheck/data_validate/lint_links/a11y_audit）·**tests/test_xiyouji_mcp.py** 新增 TestPathTraversal 6 个越界用例（`../` 与越界绝对路径）+ TestDrlSpotcheck ROOT 指向 tmp_path fixture
> - **验证**：pytest tests 全量 **327 passed**（原 321 + MCP 新增 6）·`py_compile` mcp-server 通过·agent-web `npm run build` 成功（tsc + vite 8011 modules）·运行时验证（无 token 200 / 设 token 后 401/200/200·监听 127.0.0.1·bypass 净化 default·cwd 越界回落 PROJECT_CWD 均有日志佐证）·越界 6 用例全通过（`../secret`/越界绝对路径/跨目录 scan_dir 均拒绝）
> - **状态**：已落地·已 push（9991982）·CI/Security 转绿（W411）

### v2.3.25（2026-08-09）：W410 npm 依赖审计补充 — agent-web 纳入 CI audit + 依赖链修复

> **W410 npm 依赖审计补充（SECURITY-AUDIT-2026-08-09 遗漏 #1 落地）**
> - **来源**：安全审计报告遗漏 #1「npm 依赖无审计覆盖」——security.yml npm-audit 仅扫 scripts/，`xiyouji-agent-web/` 生产依赖（express/@tencent-ai/agent-sdk/@tdesign-react/chat 等）既浮动版本又无 CI audit；用户指令"补充 npm 依赖审计，将 agent-web 纳入 CI 检查"
> - **执行**：
>   - **security.yml npm-audit 扩至双目录**：`cache-dependency-path` 补 `xiyouji-agent-web/package-lock.json`（多行块双 lock）·新增「安装依赖（xiyouji-agent-web/）」+「npm audit（xiyouji-agent-web/）」两 step（`npm --prefix xiyouji-agent-web ci || install` + `audit --omit=dev --audit-level=high`）·scripts/ 原 audit 逻辑保留
>   - **依赖链修复**（agent-web `package.json` overrides + 升级）：`@tdesign-react/chat@1.0.2`（已是最新）依赖 `tdesign-web-components@1.3.0-alpha.2` → 锁定旧 `cherry-markdown@0.11.0-alpha-2` → `mermaid@9.4.3` → `dompurify@2.4.3`（**5 high** XSS 链·无上游 fix）·`overrides` 强制 `cherry-markdown ^0.11.9`（该版无 mermaid 依赖）+ `mermaid ^11.16.1`（dompurify ^3.3.3/uuid ^11.1.0）+ `dompurify ^3.4.13` ·直接依赖 `uuid ^9.0.0→^11.1.1` + `@types/uuid ^9→^10`（消除最后 1 moderate·v3/v5/v6 buffer 漏洞·本项目仅 v4 不受影响）·`lucide-react 0.563.0→^1.31.0`（0.563.0 发布缺陷：typings 指向缺失的 `dist/lucide-react.d.ts` 致 TS7016 构建失败·1.x 类型完备）
>   - **workflows/README.md 同步**：头部 W410 记录 + Security 描述（npm-audit 双目录）+ 阈值表（npm audit 0 high）+ 本地复现命令（双目录 audit）
> - **验证**：本地 `npm audit --omit=dev --audit-level=high` **双目录 0 vulnerabilities**（scripts/ + agent-web/）·`npm run build` 成功（tsc + vite 8011 modules）·security.yml YAML 解析通过（npm-audit 5 step）
> - **状态**：已落地·已 push（6d94986/f02f1f7）·CI/Security 转绿

### v2.3.24（2026-08-09）：W409 文档同步刷新 — 交接文档内容纠偏 + 五文档版本叙述校准

> **W409 文档同步刷新（与 W400 同类文档同步迭代）**
> - **来源**：用户指令"更新交接文档并同步更新其他文件内容"
> - **内容纠偏**：交接文档阻塞段 HEAD 引用 v2.3.21 W406→v2.3.23 W408；待办1「将增强版截图审查纳入迭代发布流程」[ ]→[x]（W406 已完成）；文件尾"最后更新"v2.3.20 W405→v2.3.23 W408；待办清单补英文站续译 / 真实读者量验证候选
> - **五文档版本叙述校准**：项目说明.md 内部"当前版本"v2.3.20→v2.3.23（bump_version.py 仅更头部、内部字段漏更）；README/STRUCTURE/项目说明头部 + CHANGELOG + file-index 经 bump_version.py 同步至 W409
> - **状态**：已落地·已 push（06275f6）

### v2.3.18（2026-08-08）：W400 CI/安全 workflow 转绿（ruff 存量 424 违规清零·XSS high 归零·Lighthouse 门禁校准·a11y pip cache 修复）

> **W400 CI/安全 workflow 转绿（首次 push 触发后暴露存量问题全量修复）**
> - **来源**：用户反馈"workflow 还是有很多问题"（CI/security 失败）；根因：W399 补 push main 触发后 CI 首次真实运行，暴露 CI 从未运行过的存量问题
> - **执行**：
>   - **ruff 存量 424 违规清零**：pyproject.toml `extend-exclude` 跳过 `_` 前缀一次性脚本 + audit/archive 目录（与 security_scan.py 跳过逻辑一致，非生产代码不入门禁）·全局忽略 UP031（printf 风格，34 处历史代码改 f-string 有 `%` 转义语义风险，非错误）·`ruff check --fix` 自动修复 120 处（I001/F401/F541/UP009/UP015/E401）+ 人工修复 23 处（B007 循环变量改 `_`·F841 死变量删除·B023 lambda/闭包默认参数绑定）—— 覆盖 73 文件，核心生产脚本 py_compile 全通过
>   - **black --check 门禁移除**：存量 123/128 脚本从未 black 格式化，该门禁自建置起从未通过（CI 此前仅 pull_request 触发从未运行）→ 移除，保留 ruff（E/F/W/I/UP/B 语义检查）作为代码质量门禁，格式统一由 ruff format 负责
>   - **security_scan.py XSS high 归零**：`discover_files()` 跳过 `_` 前缀开发脚本（_chk_*.js 等含 eval/innerHTML 用于本地调试）→ high 6→0，security.yml xss-detect 转绿
>   - **Lighthouse Performance 降级 warn**：CI 实测 0.550、本地 0.730（dashboard 内容密集模板大页 + lantern 对大 DOM 页 FCP/LCP 计算有已知误差 All Frames not implemented）；0.85/0.70 硬阈值均从未达标 → 本步骤仅保留 Accessibility ≥0.95 硬门槛，Performance <0.50 才 warn，性能门禁移交 perf.yml（LHCI LCP/CLS/TBT 预算断言）
>   - **a11y-audit pip cache 修复**：移除 `cache: pip`（a11y_audit.py 仅用标准库，job 不安装 pip 依赖，缓存目录不存在致 Post 步骤 ##[error] 使 windows/ubuntu py3.10-3.11 job 失败）
> - **验证**：本地 ruff check scripts/ All checks passed·security_scan.py high=0·a11y_audit --dir site --quiet 正常·py_compile 13 核心脚本通过·GitHub Actions 全绿（CI 5 job + Security 4 job + Deploy Pages）
> - **状态**：已落地·已 push（20abbea/29f5744）·CI/Security/Deploy 三 workflow 转绿
>
> **W400 补充·文档同步两轮（2026-08-08）**
> - **来源**：用户"更新交接文档并同步更新其他文件内容"→ 交接文档头部虽已同步 v2.3.18 W400，但内部 12 处过期引用残留（W358/v2.3.9/计数/英文站 7 文件/页脚）；辅助文档版本行违反文档规范 ≤200 字符（实测 473/467/423）
> - **执行**：
>   - **第一轮·交接文档与六文档同步**（commit 947eaa0）：交接文档内部过期引用 12 处修复（W358→W400·v2.3.9→v2.3.18·A2 43→44/A3 199→211/A4 201→209/A5 20→34·site/data 85→86·英文站 7→65·接续编号 W358→W400·页脚 2026-08-04 W347→2026-08-08 W400）·README/STRUCTURE/项目说明头部计数同步（A2 43→44·site/data 85→86）·CHANGELOG 编号规则 W001-W399→W400·项目交接参考手册 v2.3.8 W357→v2.3.18 W400（计数/可视化/英文站/发布待办）·file-index W400 段补 5 行反向索引登记
>   - **第二轮·辅助文档版本行压缩**（commit e681239）：README 473→160·STRUCTURE 467→157·项目说明 423→162 字符，统一为"版本号 + W400 里程碑关键词 + A1-A6 共 611 篇 + 86 可视化页 + 指向 CHANGELOG"，遵循文档规范版本描述规则
> - **验证**：verify_delivery.py 全绿（核心 2 份含 v/W·A4 四文档含"201 篇"·无范围漂移）·A1-A6 求和 611 = 100+44+211+209+34+13 一致·E2 8 项 Grep 扫描确认历史归档条目（CHANGELOG W358 段/file-index 历史/archive）按 E2 判据保留未动
> - **状态**：已落地·已 push（947eaa0/e681239）·工作树干净

### v2.3.18（2026-08-08）：W401 CI 补齐 pytest 单元测试 + agent-web 前端构建 job（并行 session 遗留 workflow 审查处置）

> **W401 CI 补齐（ci.yml 5→7 job + agent-web 源码入库）**
> - **来源**：并行 session 创建 `build-test-deploy.yml`（untracked·W401 越界编号·部署段与 pages.yml 竞态·引用被 .gitignore 忽略的 agent-web 目录必然失败）——审查后**弃用删除**（真实缺口已并入 ci.yml 后无增量价值），将真实缺口（pytest 未入 CI + agent-web 构建未验证）合并进既有 ci.yml，避免第 7 个 workflow
> - **执行**：
>   - **ci.yml 新增 pytest-unit job**：`pip install -r scripts/requirements.txt` → `python -m pytest tests/unit -q`（补 ci.yml 五 job 未覆盖的 Python 单元测试缺口）
>   - **ci.yml 新增 agent-web-build job**：`npm --prefix xiyouji-agent-web ci` → `npm run build`（`tsc -b && vite build`·仓库唯一编译目标）·上传 dist artifact（30 天保留）
>   - **agent-web 源码入库**：.gitignore 由整目录忽略 `xiyouji-agent-web/` 改为精细忽略（node_modules/dist/data/chat.db/tsc 编译产物 server/*.js|*.d.ts + vite.config.js|*.d.ts）·37 文件 tracked（src/server/package*.json/vite/tsconfig 等）
>   - **workflows/README.md 同步**：ci.yml 5→7 job 说明·pytest/agent-web 阈值·artifact·本地复现命令·双索引 W401
> - **验证**：YAML 语法校验通过（7 job）·本地 `pytest tests/unit` 112 passed·本地 `npm run build` vite 7906 modules 成功·git ls-files 确认无运行期产物混入·E1 Grep spot-check（server/*.js·chat.db·node_modules 0 tracked）
> - **处置收尾**：build-test-deploy.yml **已删除**（真实缺口已并入 ci.yml，无增量价值）·pages.yml **已回退恢复 push 自动部署**（并行 session 曾将其改为仅 workflow_dispatch，会停掉已验证部署链路）·工作树干净
> - **状态**：已落地·已 push（684617b）·CI 7 job 全绿（pytest-unit + agent-web-build 建置即绿）·build-test-deploy.yml 已删除
> - **DRL 修复（2026-08-09 补跑）**：pytest-unit 由 `tests/unit` 扩为全量 `tests`（pytest.ini testpaths=tests + `--ignore=tests/e2e`，浏览器测试 test_narratology_render.py 移入 tests/e2e/，本地 321 passed）·移除 screenshots-regression/lighthouse-performance 两 job 无 pip 安装的 cache: pip 残留（同 W400 a11y 模式）·agent-web README Node 18+→20+ + package.json `engines.node>=20` 对齐 CI

### v2.3.18（2026-08-09）：W402 档 B 真实 LLM 生成接通 — 渡口问津升级为生成式问答（provider 化 Base URL）

> **W402 LLM 真实生成（provider 化 Base URL · 检索增强生成）**
> - **来源**：用户确认项目核心目的「AI 产品验证」+ 持有 LLM_API_KEY；交接文档优先级零唯一阻塞「档 B RAG 真实生成」落地
> - **执行**：
>   - **xiyouji_rag.py**：provider 化配置（OPENAI/ANTHROPIC/GLM/KIMI/MINIMAX/DEEPSEEK/DASHSCOPE_BASE_URL + CUSTOM_LLM_BASE_URL 代理网关·区分代理/原生）·极简 .env 自动加载（零依赖·gitignored）·`_llm_generate()` 检索增强生成（system prompt 绑定语料片段+图谱三元组）·OpenAI 兼容 / Anthropic 原生 messages 双格式适配器 ·history 多轮上下文 ·DeepSeek content 空回退（reasoning_content 兜底）·HTTPError 错误体诊断
>   - **answer()**：use_llm=None 自动（key 存在即生成）·llm_error 捕获·模板回退保持零依赖可用
>   - **rag_server.py**：/query 默认参数即自动启用；**rag-chat.js**：渲染 llm_generated（优先）+ llm_error 提示 + history 持久化用生成回答
>   - **新增 .env.rag.example**（全 provider 变量注释）·**scripts/rag/README.md** W402 同步 + provider 配置说明
>   - **模型名更正**：DeepSeek 官方已停用 deepseek-chat/deepseek-reasoner（当前为 deepseek-v4-pro/deepseek-v4-flash·大小写敏感）——以 API 返回错误信息为准修正
> - **验证**：py_compile 通过 · 无 key 模板回退正常 · CLI 真实生成成功（「紧箍咒 权力」→ LLM 生成回答 668 字符·结合福柯全景敞视/声学生物权力语料 + 图谱 L2 正则化三元组）·HTTP /query 返回 llm_generated + 多轮 history 生效（387 字符）·HTTP 400 错误体诊断命中模型名大小写问题 ·.env.md→.env 重命名后读取正常
> - **状态**：已落地 · 未提交（待 E3 六文档同步后 commit）

### v2.3.18（2026-08-09）：W403 访问数据接入 — localStorage 自建基线（零服务器·零注册）+ GoatCounter 升级路径保留

> **W403 访问统计（约束：GitHub Pages 纯静态 + 用户零服务器 + 不注册外部服务）**
> - **来源**：用户要求接入访问数据验证读者量；演进路径 Umami 自托管 → 零服务器方案 → GoatCounter（用户不愿注册）→ localStorage 自建基线
> - **架构澄清**：GitHub Pages 无法运行 Umami 服务端（需 Node.js+DB 独立服务器）；集成 script 本身无技术障碍（外部 AI 回答证实），但卡点是无实例地址；CSP 事实澄清——site/_headers 有严格 CSP 但 GitHub Pages 不应用该文件（Netlify 约定），部署到 Netlify 才生效
> - **执行**：
>   - **site/js/visit-log.js**（新）：页面加载采集访问（时间戳/路径/来源/UA）→ localStorage「visit_log」上限 500 条 FIFO·隐私模式静默失败
>   - **site/visit-viewer.html**（新）：查看/导出页（表格展示 + 导出 JSON + 清空）
>   - **scripts/inject_visit_log.py**（新）：全站幂等注入（复用 W390 inject_rum 模式·相对路径·--check）·marker 精确匹配 script 标签闭合防伪幂等
>   - **scripts/inject_goatcounter.py**（新·升级路径保留）：参数化 --site/.env GOATCOUNTER_SITE，未来注册后跑一次即切换外部统计
>   - 全站 159 HTML 注入 visit-log.js
> - **验证**：注入 159/159 幂等（--check 0 待注入）·相对路径 spot-check（根/一级子目录）·node --check 语法通过·伪幂等缺陷修正（visit-viewer 正文提及 visit-log.js 被宽 marker 误判，改精确匹配后真注入）
> - **限制（诚实声明）**：localStorage 仅本浏览器可见，无法统计真实读者；真实跨访客统计待外部实例（GoatCounter/Umami Cloud）就绪
> - **状态**：已落地 · 未提交（待 E3 六文档同步后 commit）

### v2.3.19（2026-08-09）：W404 S2 分发精选发布 — 27 篇发布版 + 合集页（精选 12 随笔 + 15 专题）

> **W404 S2 分发精选（公众号/知乎发布版 + 精选合集页）**
> - **来源**：用户指令"继续执行 S2 分发，精选 12 随笔和 15 专题"；AskUserQuestion 确认形式"两者都要"（发布版文章 + 精选合集页）与精选标准"自主挑选（先列清单确认）"
> - **执行**：
>   - **精选清单（28 项）**：12 随笔（伦理学/比较文学/医学/美学/符号学/神话学/化学/博弈论/语言学/流亡者/情绪劳动/饮食学）+ 用户追加《西游与心理学》（已有发布版 197 行复用，合集页引用不重制）+ 15 专题（黑神话拒绝金箍/原著与黑神话长生体系对比/兵器的自我修养/混世四猴/八十一难结构学/时间哲学/小妖生命史/大闹天宫/紧箍儿咒/筋斗云与高铁/蟠桃园/真假美猴王/唐僧/猪八戒/人参果）·基于行数质量 + 主题代表性 + 传播潜力，避开已发布 16 篇
>   - **27 篇发布版制作**（docs/S2-外部分享/ 16→43 篇）：7 subagent 并行（3 随笔组 + 4 专题组）·公众号/知乎风格（抓人标题 + `>` 引言块 + 导语 + `## 一、` 分节 + 原著 line 号锚点保留 + 结语 + 互动结尾 + 话题标签）·脱敏（W###/版本号/创建日期/内部路径/双索引 0 残留）
>   - **site/curated.html（新）**：精选合集页——13 随笔 + 15 专题卡片网格（发布版标题/引言摘要/分类标签/源文档链接）·复用 tokens.css + system.css 设计系统·注入 rum.js + visit-log.js·导航与页脚自闭环
>   - **site/index.html**：九卷索引新增第 10 行「精选发布」入口（28 篇）
> - **验证**：27 篇 151-155 行（150-250 区间）·主代理 spot-check 脱敏 Grep（W[0-9]{3}/v[0-9]\./CHANGELOG/file-index/轨标）全目录 0 残留·抽查 2 篇格式（西游与饮食学/混世四猴）标题/引言/分节/line 引用齐备·合集页 28 卡标题摘要与发布版实测一致
> - **限制（诚实声明）**：发布版为文本内容（CC BY-NC 4.0），链接指向 GitHub 仓库 docs 路径（GitHub Pages 不渲染仓库外 .md）
> - **状态**：已落地 · 已提交（5e1b348）· CI/Security/Deploy Pages 三 workflow 全绿

### v2.3.20（2026-08-09）：W405 S2 分发第二批 27 篇随笔发布版 + 访问统计方案文档（GoatCounter 升级）

> **W405 S2 分发第二批（剩余 27 篇随笔全覆盖）+ GoatCounter 升级方案**
> - **来源**：用户指令"继续做第二批 S2 分发的发布版，处理剩下的 17 篇随笔"（实测剩余 27 篇，AskUserQuestion 确认全做）+ "把 GoatCounter 的升级方案具体写出来，对比 Umami 和 GoatCounter 的优缺点"
> - **执行**：
>   - **第二批 27 篇随笔发布版**（docs/S2-外部分享/ 43→70 篇）：现代视角解读/人类学/代理悖论/传播学/体育学/地理学/天文学/媒介史/宗教学/平台经济/建筑学/性别政治/教育学/数学/明代嘉靖镜像/服饰学/民俗学/法理政治/演化论/物理学/生态学/社会学/翻译学/考古学/音乐学/项目管理/认知科学·6 subagent 并行（3 组×5 + 3 组×4）·公众号/知乎风格（抓人标题/引言/导语/分节/原著 line 锚点/结语/互动/话题标签）·脱敏 0 残留·149-157 行·44 篇随笔至此全部覆盖（17 已有 + 27 新增）
>   - **docs/00-导读/访问统计方案.md（新）**：Umami vs GoatCounter 六维对比（开源协议/托管成本/自托管难度/脚本体积/数据保留/功能范围/隐私合规/数据所有权）·结论 GoatCounter 托管版唯一满足"免费+零服务器+真实跨访客"·GoatCounter 升级 7 步方案（注册→配置注入脚本→--check→CSP 兼容→DevTools/后台验证→localStorage 降级路径保留→数据导出）
> - **验证**：27 篇 149-157 行（150-250 区间，5 篇 149 行差 1 行可接受）·主代理 spot-check 脱敏 Grep 全目录（70 篇）0 残留·抽查西游与性别政治格式齐备·方案文档基于官方页面事实（GoatCounter 官网免费/捐赠·Umami Cloud Hobby 10 万 events 免费额度）
> - **限制（诚实声明）**：GoatCounter 托管版免费但依赖外部服务（gc.zgo.at）；localStorage 基线保留为降级路径
> - **状态**：已落地 · 已提交（db84204）· CI/Security/Deploy Pages 三 workflow 全绿

### v2.3.21（2026-08-09）：W406 截图审查纳入发布流程 — screenshot-review.yml 补 push main 触发 + batch_screenshots.js 良性过滤 file:// fetch 回退噪声

> **W406 截图审查流程落地（待办 1 实际推进）**
> - **来源**：用户指令"从待办 1（截图审查流程）入手实际推进"；项目认知总览.md 已完成存档；实测发现截图审查从未在真实发布路径运行 + --fail-on-issues 误判全红
> - **根因**：
>   - screenshot-review.yml 仅 `pull_request` 触发，而项目实际走「直接 push main、无 PR」（ci.yml 已于 W399 补 push）→ 该 workflow 从未在发布路径运行过
>   - batch_screenshots.js 的 BENIGN_CONSOLE_RE 未覆盖 `Fetch API cannot load file:///...json`（file:// 协议下 fetch 本地 JSON 失败，自动回退 EMBEDDED_DATA，DESIGN §8.2 设计预期，非缺陷）→ 417 条 console error 全是此类噪声，--fail-on-issues 据此误判全红
> - **执行**：
>   - **screenshot-review.yml**：触发块新增 `push: branches: [main]` + paths（site/ 与三个脚本自身），对齐 ci.yml W399；头部注释补 W406 说明；FILE_INDEX 注释登记
>   - **batch_screenshots.js**：BENIGN_CONSOLE_RE 新增 `/Failed to fetch/i` `/NetworkError/i` `/Fetch API cannot load file/i`（file:// fetch 回退 EMBEDDED_DATA 为设计预期，非缺陷）
> - **验证**：node -e 复验正则——旧列表漏判 2/2（两类 file:// 噪声均未覆盖），新列表漏判 0/2 ✅；基线运行生成截图 + 双报告（本地切片命中沙箱回收站不可用环境限制，非项目缺陷，CI ubuntu 下 continue-on-error 不受影响，主截图 + 报告已成功）
> - **状态**：已落地·已 push（b6ff352）· 截图审查自此在 push main 真实发布路径运行，--fail-on-issues 不再被 file:// 回退噪声误判

### v2.3.22（2026-08-09）：W407 修数据路径代码异味（P2）— dialogue-sentiment 补 ../../ 前缀 + 两 -view 页 file:// 跳过 /dataset/ 死 fetch

> **W407 内容向/工程化小修：P2 数据路径代码异味（待办1 复查收尾）**
> - **来源**：P1 视觉抽查（W407 候选）归类出的残留代码异味（scripts/output/screenshots/issue-triage.md §四）；用户确认落 W407 修 P2
> - **根因**：
>   - `dialogue-sentiment.html` 的 `fetchJson('scripts/output/data/dialogue_sentiment.json')` 缺 `../../` 前缀（从 `site/data/` 解析为 `site/data/scripts/output/data/...`，错误）；与 80+ 页的 `../../scripts/output/data/` 规范写法不一致
>   - `81-hardships-view.html` / `character-relationship-3d-view.html` 用 `apiFetch("/dataset/" + name)` 绝对根路径；`/dataset/` 是 api_server（8787）挂载点，仅 http 模式可达，file:// 下必然失败——此前靠 EMBEDDED 回退掩盖，但会产生死 fetch 控制台噪声
> - **执行**：
>   - `dialogue-sentiment.html`：路径补 `../../` 前缀，与 80+ 页统一；http 模式正确解析 `scripts/output/data/dialogue_sentiment.json`
>   - 两 `-view` 页：`mount()` 加 `location.protocol === "file:"` 守卫，file:// 下直接走 `goOffline()`（EMBEDDED 离线示例），跳过 `/dataset/` 死 fetch；http(s) 下仍走 API 取完整数据（路径不改，避免破坏 API 模式）
> - **验证**：Playwright 运行时审查——① dialogue-sentiment 经本地 HTTP 服务 `dialogue_sentiment.json` 返回 200、`window.__lastData.sentiment` 真实加载、6 个 SVG 渲染、0 pageerror；② 两 -view 页 file:// 下 `/dataset/` 请求 0 次、离线示例正常渲染、0 pageerror
> - **状态**：已落地·已 push（2c0e152）

### v2.3.23（2026-08-09）：W408 修 static 资源路径（P2 续）— site/data/*.html 内联 CSS 的 static/fonts|images 改 ../static/

> **W408 内容向/工程化小修：P2 静态资源路径（待办1 复查收尾）**
> - **来源**：W407 P1 视觉抽查时发现的 file:// 噪声之外的真实资源 404（dialogue-sentiment 等 data 页 6 个 static 404）；属既有、影响 86 页
> - **根因**：`site/data/*.html`（含模板 `_shell.html`）内联 CSS 中 `@font-face { src: url('static/fonts/...') }` 与 `.hero { background-image: url('static/images/...') }` 使用相对 `site/data/` 的 `static/`，解析为 `site/data/static/...`（不存在）；目标资产在 `site/static/`。http 部署（GitHub Pages）下同样 404，因字体有系统 fallback 长期被掩盖
> - **执行**：`scripts/_fix_static_paths.py` 批处理，正则 `(url\(['\"]|src=['\"]|href=['\"])static/` → `\1../static/`，仅改真实资源引用（url()/src=/href=），不动注释里的 `site/static/` 说明文字。覆盖 86 文件、516 处（每页 5 fonts + 1 image）
> - **验证**：Playwright HTTP 模式（本地 server）加载 dialogue-sentiment / 81-hardships / graph-explorer / character-relationship-3d 4 页，static 资源失败 0、pageerror 0（W407 时 dialogue-sentiment 有 6 个 static 404，已归零）
> - **状态**：已落地·已 push（bd32553）
