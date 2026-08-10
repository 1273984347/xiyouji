# xiyouji 文件反向索引

> 与 [CHANGELOG.md](../../CHANGELOG.md) 配套：给定文件，查它被改过几次、每次对应哪个 W 条目。
> W### 编号规则见 CHANGELOG.md 顶部。
> 创建于 2026-07-22（v0.8 双索引改造）
>
> **历史归档**：W031-W087（v2.0.4-v2.0.60）site/data/ 部分已迁移至 [file-index-archive.md](file-index-archive.md)。本文件仅保留 W088+ 现役索引。

---

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
| 项目概览.md | W421 | v2.3.36 修改·头部 HEAD v2.3.36 W421 + W421 里程碑行 |
| 项目认知总览.md | W421 | v2.3.36 修改·头部 + 当前开发进度 HEAD v2.3.36 W421 |
| 项目交接参考手册.md | W421 | v2.3.36 修改·头部版本 v2.3.36 W421 + 接续编号当前 W421·下一 W422 |
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
| 项目概览.md | W420 | v2.3.35 修改·头部 HEAD v2.3.35 W420 + W420 里程碑行 |
| 项目认知总览.md | W420 | v2.3.35 修改·头部 + 当前开发进度 HEAD v2.3.35 W420 |
| 项目交接参考手册.md | W420 | v2.3.35 修改·头部版本 v2.3.35 W420 + 接续编号当前 W420·下一 W421 |
| .github/workflows/README.md | W420 | v2.3.35 修改·头部 W 链加 W420 + W420 说明行 |
| docs/00-导读/文档规范.md | W420 | v2.3.35 修改·§11.2 禁改范围 W001-W418→W001-W419（随 W420 校准·E2 深处残留） |

## W416 文件管控清单标注（2026-08-10·v2.3.31）

| 文件 | W | 说明 |
|---|---|---|
| docs/00-导读/文档规范.md | W416 | v2.3.31 修改·新增 §11 文件管控清单（11.1 必同步 8 类文件附门禁 / 11.2 禁擅自修改 12 类文件附例外 / 11.3 接手速查 6 步·多 session/Agent 协作专用） |
| 交接文档.md | W416 | v2.3.31 修改·头部/阻塞段 HEAD/当前进度 W416 里程碑/版本号列表 v2.3.31 + 下一 W417/README 引用 v2.3.31/CHANGELOG 范围 W001-W416/接续编号·跨 session 接续流程新增第 3 步「文件管控」引用文档规范 §11 |
| CHANGELOG.md | W416 | v2.3.31 修改·新增 v2.3.31 W416 段·W### 编号规则 W001-W415→W001-W416 |
| scripts/output/file-index.md | W416 | v2.3.31 修改·本段（W416 登记） |
| README.md | W416 | v2.3.31 修改·版本行 v2.3.31 W416（尾部 W 链 + W415） |
| STRUCTURE.md | W416 | v2.3.31 修改·头部版本行 v2.3.31 W416 |
| docs/00-导读/项目说明.md | W416 | v2.3.31 修改·头部 + 第 45 行"当前版本"v2.3.31 |
| site/index.html | W416 | v2.3.31 修改·页脚 v2.3.30 W415→v2.3.31 W416 |
| site/dukou-engine.html | W416 | v2.3.31 修改·页脚插入 v2.3.31 W416 段（文件管控清单标注） |
| site/data/cross-time-danmaku.html | W416 | v2.3.31 修改·页脚 v2.3.31 · W416 |
| site/data/tag-cloud.html | W416 | v2.3.31 修改·页脚 v2.3.31 · W416 |
| 项目概览.md | W416 | v2.3.31 修改·头部 HEAD v2.3.31 W416 + W416 里程碑行 |
| 项目认知总览.md | W416 | v2.3.31 修改·头部 + 当前开发进度 HEAD v2.3.31 W416 |
| 项目交接参考手册.md | W416 | v2.3.31 修改·头部版本 v2.3.31 W416 + 接续编号当前 W416·下一 W417 |
| .github/workflows/README.md | W416 | v2.3.31 修改·头部 W 链加 W416·v2.3.31 W416 + W416 说明行 |

## W415 README 视觉引导增量（2026-08-09·v2.3.30）

| 文件 | W | 说明 |
|---|---|---|
| README.md | W415 | v2.3.30 修改·顶部新增徽章区 3 枚 shields.io（在线访问/双协议授权/部署状态）·「内容导航表」改「🎁 你将会看到什么」8 条 emoji 图标化速览·在线体验区插入首页预览截图·新增「💬 反馈与建议」段·开发者区新增「技术栈」段·版本行 v2.3.30 W415 |
| assets/images/index-preview.png | W415 | v2.3.30 新建·site/index.html 首页预览截图（Playwright 1280×900·108.7KB·PNG 头校验通过） |
| CHANGELOG.md | W415 | v2.3.30 修改·新增 v2.3.30 W415 段·W### 编号规则 W001-W414→W001-W415 |
| scripts/output/file-index.md | W415 | v2.3.30 修改·本段（W415 登记） |
| STRUCTURE.md | W415 | v2.3.30 修改·头部版本行 v2.3.29→v2.3.30 W415 |
| docs/00-导读/项目说明.md | W415 | v2.3.30 修改·头部 + 第 45 行"当前版本"v2.3.30 W415·（2026-08-10 处置收尾）待办 3/4 标记完成（v0.9.1 回归/截图审查 W406） |
| 交接文档.md | W415 | v2.3.30 修改·头部/阻塞段 HEAD/当前进度 W415 里程碑/版本号列表 v2.3.30 + 下一 W416/README 引用行 v2.3.30 + CHANGELOG 范围 W001-W415/接续编号段·（2026-08-10 处置收尾）W414 段状态行/验证行纠偏 + 候选清单 RAG 阻塞 3 处标注 W402 已解除 |
| site/index.html | W415 | v2.3.30 修改·页脚 v2.3.29 W414→v2.3.30 W415 |
| site/dukou-engine.html | W415 | v2.3.30 修改·页脚插入 v2.3.30 W415 段（徽章区+图标化速览+预览截图+反馈） |
| site/data/cross-time-danmaku.html | W415 | v2.3.30 修改·页脚 v2.3.30 · W415 |
| site/data/tag-cloud.html | W415 | v2.3.30 修改·页脚 v2.3.30 · W415 |
| 项目概览.md | W415 | v2.3.30 修改·头部 HEAD v2.3.30 W415 + 里程碑列表新增 W415 行 |
| 项目认知总览.md | W415 | v2.3.30 修改·头部 + 当前开发进度 HEAD v2.3.30 W415 |
| 项目交接参考手册.md | W415 | v2.3.30 修改·头部版本 v2.3.30 W415 + 接续编号当前 W415·下一 W416 |
| .github/workflows/README.md | W415 | v2.3.30 修改·头部 W 链加 W415·v2.3.30 W415 + 新增 W415 说明行 |

## W393 降级六文档同步 核心2+辅助4自动（2026-08-08）

| 文件 | W | 说明 |
|---|---|---|

## W394 英文站 batch1 导览双页英文化（2026-08-08·v2.3.17）

| 文件 | W | 说明 |
|---|---|---|
| site/en/guide.html | W394 | 新建·导读页英文版（7 类读者路径 + 术语表 + 版本/引用）·内联 CSS·双向导航 |
| site/en/dukou-engine.html | W394 | 新建·渡口写作引擎英文版·保全内联 JS·零 CJK 残留 |
| site/en/index.html | W394 | 修改·导航卡新增 Reading Guide + Ferry Crossing |
| 交接文档.md | W394 | v2.3.17 同步·新增 W394 段 |
| CHANGELOG.md | W394 | v2.3.17 同步·新增 W394 版本段 |

## W395 英文站 batch2 三核心可视化页英文化（2026-08-08·v2.3.17）

| 文件 | W | 说明 |
|---|---|---|
| site/en/81-hardships.html | W395 | 新建·八十一难深度统计英文版·保全内联 D3 JS/CSS·双向导航 |
| site/en/chapter-structure-graph.html | W395 | 新建·回目结构图谱英文版·译 KPI/叙事簇/轴标签/tooltip |
| site/en/character-appearance.html | W395 | 新建·人物出场频次英文版·15 人物名转拼音 |
| site/en/visualizations.html | W395 | 修改·3 索引卡改指 EN 版 + 中文回链 |
| 交接文档.md | W395 | v2.3.17 同步·新增 W395 段 |
| CHANGELOG.md | W395 | v2.3.17 同步·新增 W395 版本段 |

## W396 英文站 batch3 三可视化页英文化（2026-08-08·v2.3.17）

| 文件 | W | 说明 |
|---|---|---|
| site/en/hardship-heatmap.html | W396 | 新建·八十一难难度热力图英文版 |
| site/en/character-presence-timeline.html | W396 | 新建·人物出场时间线英文版·35+ 人物名转英文 |
| site/en/character-relationship-3d.html | W396 | 新建·人物关系 3D 网络图英文版（Three.js） |
| site/en/visualizations.html | W396 | 修改·3 索引卡改指 EN 版 + 中文回链 |
| 交接文档.md | W396 | v2.3.17 同步·新增 W396 段 |
| CHANGELOG.md | W396 | v2.3.17 同步·新增 W396 版本段 |

## W397 英文站 batch4 三可视化页英文化（2026-08-08·v2.3.17）

| 文件 | W | 说明 |
|---|---|---|
| site/en/character-sentiment-arc.html | W397 | 新建·人物情感弧线英文版 |
| site/en/chapter-stats.html | W397 | 新建·章节字数与对话统计英文版 |
| site/en/narrative-rhythm-curve.html | W397 | 新建·叙事节奏曲线英文版 |
| site/en/visualizations.html | W397 | 修改·3 索引卡改指 EN 版 + 中文回链 |
| 交接文档.md | W397 | v2.3.17 同步·新增 W397 段 |
| CHANGELOG.md | W397 | v2.3.17 同步·新增 W397 版本段 |

## W398 英文站 batch5 两地理可视化页英文化（2026-08-08·v2.3.17）

| 文件 | W | 说明 |
|---|---|---|
| site/en/journey-geo-semiotics.html | W398 | 新建·取经路径地理符号学英文版 |
| site/en/journey-route.html | W398 | 新建·取经全路程图英文版·耦合地理类型枚举整块转译 |
| site/en/character-semantic-network.html | W398 | 新建·人物语义关系网络英文版（batch5 一并入库） |
| site/en/visualizations.html | W398 | 修改·2 索引卡改指 EN 版 + 中文回链 |
| CHANGELOG.md | W398 | v2.3.17 同步·新增 W398 版本段 |
| 交接文档.md | W398 | v2.3.17 同步·新增 W398 段 |
| README.md | W398 | v2.3.17 同步·六文档同步补齐 W394-W398·版本段日期 2026-08-08 |
| STRUCTURE.md | W398 | v2.3.17 同步·六文档同步补齐 W394-W398·版本段日期 2026-08-08 |
| docs/00-导读/项目说明.md | W398 | v2.3.17 同步·六文档同步补齐 W394-W398·版本段日期 2026-08-08 |
| scripts/output/file-index.md | W398 | v2.3.17 同步·新增 W394-W398 反向索引段 |

## W399 CI 触发修复+SEO 域名+rum-viewer 埋点查看页（2026-08-08）

| 文件 | W | 说明 |
|---|---|---|

> 当前版本 v2.3.18（2026-08-08）

## W400 CI/安全 workflow 转绿（2026-08-08）

| 文件 | W | 说明 |
|---|---|---|
| .github/workflows/ci.yml | W400 | ruff 门禁生效·移除 black·Lighthouse Performance 降级 warn（Accessibility 硬门槛）·a11y 移除 pip cache |
| pyproject.toml | W400 | extend-exclude `_` 前缀/archive·全局忽略 UP031 |
| scripts/security_scan.py | W400 | discover_files 跳过 `_` 前缀开发脚本（XSS high 6→0） |
| scripts/a11y_audit.py | W400 | F841 parser 死代码清理·B007 循环变量改 `_` |
| scripts/perf_optimize.py | W400 | B023 闭包默认参数绑定·B007/F841 清理 |
| scripts/sync_docs.py | W400 | B023 lambda 默认参数绑定 |
| scripts/rag/xiyouji_rag.py | W400 | F841 best_head 清理·B007 循环变量 |
| scripts/perf_monitor.py | W400 | F841 categorized 死代码清理·B007 |
| scripts/B_人物/character_nlp.py | W400 | B007 循环变量改 `_`（4 处） |
| scripts/w286_merge_yuanwen_shendu.py | W400 | F841 skipped 死代码清理 |
| 其余 63 个 scripts/*.py | W400 | ruff --fix 自动修复（I001/F401/F541/UP009/UP015/E401） |
| README.md | W400 | 文档同步·头部版本行压缩至 ≤200 字符（473→160·A2 43→44 篇·site/data 85→86 个） |
| STRUCTURE.md | W400 | 文档同步·头部版本行压缩至 ≤200 字符（467→157·A2 43→44 篇） |
| docs/00-导读/项目说明.md | W400 | 文档同步·头部版本行压缩至 ≤200 字符（423→162·A2 43→44 篇·可视化 80→86 页·待办计数 A3/A4/A5 更新） |
| 交接文档.md | W400 | 文档同步·内部过期引用 12 处修复（W358→W400·v2.3.9→v2.3.18·A2 43→44/A3 199→211/A4 201→209/A5 20→34·site/data 85→86·英文站 7→65·页脚） |
| 项目交接参考手册.md | W400 | 文档同步·版本 v2.3.8 W357→v2.3.18 W400·计数 A2/A3/A4/A5·可视化 85→86·英文站 51→65·发布待办标记完成 |

## W410 npm 依赖审计补充 · agent-web 纳入 CI（2026-08-09·v2.3.25）

| 文件 | W | 说明 |
|---|---|---|
| .github/workflows/security.yml | W410 | 修改·npm-audit 扩至双目录（cache-dependency-path 补 agent-web lock·新增 agent-web 安装/audit 两 step·scripts/ 原逻辑保留） |
| xiyouji-agent-web/package.json | W410 | 修改·overrides 强制 cherry-markdown ^0.11.9 / mermaid ^11.16.1 / dompurify ^3.4.13·uuid ^9.0.0→^11.1.1·@types/uuid ^9→^10·lucide-react ^0.563.0→^1.31.0 |
| xiyouji-agent-web/package-lock.json | W410 | 修改·overrides/uuid/lucide 应用后重新解析（cherry-markdown 0.11.9·mermaid 11.16.1·dompurify 3.4.13·uuid 11.x·lucide 1.31） |
| .github/workflows/README.md | W410 | 修改·头部 W410 记录 + Security 描述（npm-audit 双目录）+ 阈值表 + 本地复现命令（双目录 audit） |
| CHANGELOG.md | W410 | 新增 W410 版本段（四件套）·编号规则 W001-W409→W001-W410 |

## W411 安全审计 P0-1/P1-1 处置（2026-08-09·v2.3.26）

| 文件 | W | 说明 |
|---|---|---|
| xiyouji-agent-web/server/index.ts | W411 | 修改·安全头中间件（X-Content-Type-Options/X-Frame-Options/Referrer-Policy/Permissions-Policy）·可选 token 认证（AGENT_WEB_TOKEN·x-agent-token/Bearer·设值后 /api/* 401）·权限白名单 sanitizePermissionMode（bypass 需 AGENT_WEB_ALLOW_BYPASS=1 否则回落 default）·工作目录白名单 resolveWorkingDir（越界回落 PROJECT_CWD）·app.listen(PORT,"127.0.0.1") 仅回环监听 |
| xiyouji-agent-web/src/hooks/useAgents.ts | W411 | 修改·默认 Agent permissionMode 'bypassPermissions'→'acceptEdits' |
| xiyouji-agent-web/vite.config.ts | W411 | 修改·dev server host '0.0.0.0'→'127.0.0.1' |
| xiyouji-agent-web/README.md | W411 | 修改·安全提示重写（W411 加固段）·默认权限模式描述改 acceptEdits |
| xiyouji-agent-web/.env.example | W411 | 修改·新增 AGENT_WEB_TOKEN / AGENT_WEB_ALLOW_BYPASS 注释 |
| mcp-server/xiyouji_mcp.py | W411 | 修改·新增 _resolve_within + PathEscapeError 路径白名单（is_relative_to 校验）·4 工具接入（drl_spotcheck/data_validate/lint_links/a11y_audit） |
| tests/test_xiyouji_mcp.py | W411 | 修改·TestPathTraversal 6 个越界用例 + TestDrlSpotcheck ROOT 指向 tmp_path fixture |
| CHANGELOG.md | W411 | 新增 W411 版本段（四件套）·编号规则 W001-W410→W001-W411 |
| 项目交接参考手册.md | W411 | 文档同步·版本 v2.3.24 W409→v2.3.26 W411·仓库已 push 至 W411 |
| 项目认知总览.md | W411 | 文档同步·HEAD 引用 v2.3.24 W409→v2.3.26 W411 |
| 项目概览.md | W411 | 文档同步·HEAD 引用 v2.3.24 W409→v2.3.26 W411（首次入库） |

## W405 S2 分发第二批 27 篇随笔 + 访问统计方案（2026-08-09）

| 文件 | W | 说明 |
|---|---|---|
| docs/S2-外部分享/S2-发布-现代视角解读.md | W405 | 新建·随笔发布版（现代视角解读） |
| docs/S2-外部分享/S2-发布-西游与人类学.md | W405 | 新建·随笔发布版（人类学） |
| docs/S2-外部分享/S2-发布-西游与代理悖论.md | W405 | 新建·随笔发布版（代理悖论） |
| docs/S2-外部分享/S2-发布-西游与传播学.md | W405 | 新建·随笔发布版（传播学） |
| docs/S2-外部分享/S2-发布-西游与体育学.md | W405 | 新建·随笔发布版（体育学） |
| docs/S2-外部分享/S2-发布-西游与地理学.md | W405 | 新建·随笔发布版（地理学） |
| docs/S2-外部分享/S2-发布-西游与天文学.md | W405 | 新建·随笔发布版（天文学） |
| docs/S2-外部分享/S2-发布-西游与媒介史.md | W405 | 新建·随笔发布版（媒介史） |
| docs/S2-外部分享/S2-发布-西游与宗教学.md | W405 | 新建·随笔发布版（宗教学） |
| docs/S2-外部分享/S2-发布-西游与平台经济.md | W405 | 新建·随笔发布版（平台经济） |
| docs/S2-外部分享/S2-发布-西游与建筑学.md | W405 | 新建·随笔发布版（建筑学） |
| docs/S2-外部分享/S2-发布-西游与性别政治.md | W405 | 新建·随笔发布版（性别政治） |
| docs/S2-外部分享/S2-发布-西游与教育学.md | W405 | 新建·随笔发布版（教育学） |
| docs/S2-外部分享/S2-发布-西游与数学.md | W405 | 新建·随笔发布版（数学） |
| docs/S2-外部分享/S2-发布-西游与明代嘉靖镜像.md | W405 | 新建·随笔发布版（明代嘉靖镜像） |
| docs/S2-外部分享/S2-发布-西游与服饰学.md | W405 | 新建·随笔发布版（服饰学） |
| docs/S2-外部分享/S2-发布-西游与民俗学.md | W405 | 新建·随笔发布版（民俗学） |
| docs/S2-外部分享/S2-发布-西游与法理政治.md | W405 | 新建·随笔发布版（法理政治） |
| docs/S2-外部分享/S2-发布-西游与演化论.md | W405 | 新建·随笔发布版（演化论） |
| docs/S2-外部分享/S2-发布-西游与物理学.md | W405 | 新建·随笔发布版（物理学） |
| docs/S2-外部分享/S2-发布-西游与生态学.md | W405 | 新建·随笔发布版（生态学） |
| docs/S2-外部分享/S2-发布-西游与社会学.md | W405 | 新建·随笔发布版（社会学） |
| docs/S2-外部分享/S2-发布-西游与翻译学.md | W405 | 新建·随笔发布版（翻译学） |
| docs/S2-外部分享/S2-发布-西游与考古学.md | W405 | 新建·随笔发布版（考古学） |
| docs/S2-外部分享/S2-发布-西游与音乐学.md | W405 | 新建·随笔发布版（音乐学） |
| docs/S2-外部分享/S2-发布-西游与项目管理.md | W405 | 新建·随笔发布版（项目管理） |
| docs/S2-外部分享/S2-发布-西游与认知科学.md | W405 | 新建·随笔发布版（认知科学） |
| docs/00-导读/访问统计方案.md | W405 | 新建·GoatCounter 升级方案 + Umami vs GoatCounter 对比（六维） |
| CHANGELOG.md | W405 | 新增 W405 版本段（四件套）·编号规则 W001-W405·W404 状态修正已提交 |

## W404 S2 分发精选发布（2026-08-09）

| 文件 | W | 说明 |
|---|---|---|
| docs/S2-外部分享/S2-发布-西游与伦理学.md | W404 | 新建·随笔发布版（伦理学） |
| docs/S2-外部分享/S2-发布-西游与比较文学.md | W404 | 新建·随笔发布版（比较文学） |
| docs/S2-外部分享/S2-发布-西游与医学.md | W404 | 新建·随笔发布版（医学） |
| docs/S2-外部分享/S2-发布-西游与美学.md | W404 | 新建·随笔发布版（美学） |
| docs/S2-外部分享/S2-发布-西游与符号学.md | W404 | 新建·随笔发布版（符号学） |
| docs/S2-外部分享/S2-发布-西游与神话学.md | W404 | 新建·随笔发布版（神话学） |
| docs/S2-外部分享/S2-发布-西游与化学.md | W404 | 新建·随笔发布版（化学） |
| docs/S2-外部分享/S2-发布-西游与博弈论.md | W404 | 新建·随笔发布版（博弈论） |
| docs/S2-外部分享/S2-发布-西游与语言学.md | W404 | 新建·随笔发布版（语言学） |
| docs/S2-外部分享/S2-发布-西游与流亡者.md | W404 | 新建·随笔发布版（流亡者） |
| docs/S2-外部分享/S2-发布-西游与情绪劳动.md | W404 | 新建·随笔发布版（情绪劳动） |
| docs/S2-外部分享/S2-发布-西游与饮食学.md | W404 | 新建·随笔发布版（饮食学） |
| docs/S2-外部分享/S2-发布-黑神话拒绝金箍.md | W404 | 新建·专题发布版（黑神话拒绝金箍） |
| docs/S2-外部分享/S2-发布-原著与黑神话悟空长生体系对比.md | W404 | 新建·专题发布版（长生体系对比） |
| docs/S2-外部分享/S2-发布-兵器的自我修养.md | W404 | 新建·专题发布版（兵器的自我修养） |
| docs/S2-外部分享/S2-发布-混世四猴.md | W404 | 新建·专题发布版（混世四猴） |
| docs/S2-外部分享/S2-发布-八十一难结构学.md | W404 | 新建·专题发布版（八十一难结构学） |
| docs/S2-外部分享/S2-发布-时间哲学.md | W404 | 新建·专题发布版（时间哲学） |
| docs/S2-外部分享/S2-发布-小妖生命史.md | W404 | 新建·专题发布版（小妖生命史） |
| docs/S2-外部分享/S2-发布-大闹天宫英雄还是悲剧.md | W404 | 新建·专题发布版（大闹天宫） |
| docs/S2-外部分享/S2-发布-紧箍儿咒四百年回响.md | W404 | 新建·专题发布版（紧箍儿咒） |
| docs/S2-外部分享/S2-发布-筋斗云与高铁速度焦虑.md | W404 | 新建·专题发布版（筋斗云与高铁） |
| docs/S2-外部分享/S2-发布-蟠桃园体制内的秘密.md | W404 | 新建·专题发布版（蟠桃园） |
| docs/S2-外部分享/S2-发布-真假美猴王二心之战.md | W404 | 新建·专题发布版（真假美猴王） |
| docs/S2-外部分享/S2-发布-唐僧凡躯圣心.md | W404 | 新建·专题发布版（唐僧） |
| docs/S2-外部分享/S2-发布-猪八戒不愿承认的自己.md | W404 | 新建·专题发布版（猪八戒） |
| docs/S2-外部分享/S2-发布-人参果人与欲望的关系.md | W404 | 新建·专题发布版（人参果） |
| docs/S2-外部分享/S2-发布-西游与心理学.md | W404 | 复用既有发布版（197 行·精选入合集页不重制） |
| site/curated.html | W404 | 新建·精选合集页（13 随笔 + 15 专题卡片·tokens.css/system.css·rum+visit-log 注入） |
| site/index.html | W404 | 修改·九卷索引新增 10「精选发布」入口（28 篇） |
| CHANGELOG.md | W404 | 新增 W404 版本段（四件套）·编号规则 W001-W404 |

## W403 访问数据接入（2026-08-09）

| 文件 | W | 说明 |
|---|---|---|
| site/js/visit-log.js | W403 | 本地访问采集（localStorage visit_log·上限 500 FIFO·隐私模式静默）·新建 |
| site/visit-viewer.html | W403 | 查看/导出页（表格展示 + 导出 JSON + 清空）·新建 |
| scripts/inject_visit_log.py | W403 | 全站幂等注入（复用 W390 inject_rum 模式·精确 marker 防伪幂等）·新建 |
| scripts/inject_goatcounter.py | W403 | GoatCounter 升级路径保留（参数化 --site/.env）·新建 |
| site/*.html（159 页） | W403 | 注入 visit-log.js tracking script |
| CHANGELOG.md | W403 | 新增 W403 版本段（四件套） |

## W402 档 B 真实 LLM 生成接通（2026-08-09）

| 文件 | W | 说明 |
|---|---|---|
| scripts/rag/xiyouji_rag.py | W402 | provider 化 Base URL（7 厂商专属变量 + CUSTOM 代理网关·区分代理/原生）·极简 .env 自动加载·_llm_generate 检索增强生成·OpenAI/Anthropic 双格式适配器·answer() use_llm 自动模式 |
| scripts/rag/rag_server.py | W402 | /query 默认参数自动启用 LLM·HTTPError 错误体诊断增强 |
| site/static/js/rag-chat.js | W402 | 渲染 llm_generated（优先）+ llm_error 提示 + history 持久化用生成回答 |
| scripts/rag/.env.rag.example | W402 | 全 provider 变量注释示例（新建） |
| scripts/rag/README.md | W402 | W402 同步 + provider 配置说明段 |
| CHANGELOG.md | W402 | 新增 W402 版本段（四件套） |

## W401 CI 补齐 pytest + agent-web 构建（2026-08-08）

| 文件 | W | 说明 |
|---|---|---|
| .github/workflows/ci.yml | W401 | 新增 pytest-unit + agent-web-build job（5→7 job）·pytest tests 全量（--ignore=tests/e2e）·npm ci + npm run build |
| .gitignore | W401 | agent-web 由整目录忽略改为精细忽略（node_modules/dist/data/server 编译产物/vite.config 产物） |
| xiyouji-agent-web/*（37 文件） | W401 | agent-web 源码入库（src/server/package*.json/vite/tsconfig 等·供 CI 构建验证） |
| .github/workflows/README.md | W401 | ci.yml 7 job 说明·阈值·artifact·本地复现命令·双索引 W401 |
| CHANGELOG.md | W401 | 新增 W401 版本段（四件套） |

> 当前版本 v2.3.21（2026-08-09）

## W406 截图审查纳入发布流程（2026-08-09）

| 文件 | W | 说明 |
|---|---|---|
| .github/workflows/screenshot-review.yml | W406 | 触发块补 push main + paths（site/ 与三个脚本自身），对齐 ci.yml W399·头部注释补 W406 说明 |
| scripts/batch_screenshots.js | W406 | BENIGN_CONSOLE_RE 补 /Failed to fetch/i /NetworkError/i /Fetch API cannot load file/i（file:// fetch 回退 EMBEDDED_DATA 为 DESIGN §8.2 设计预期，非缺陷·--fail-on-issues 不再误判全红） |
| site/dukou-engine.html | W406 | 页脚版本升 v2.3.21 W406 + 补 W406 里程碑（W400/W390-W393 历史保留） |
| CHANGELOG.md | W406 | 新增 W406 版本段（四件套）+ 编号规则 W001-W405→W406 |
| 交接文档.md | W406 | 头部/HEAD/进度段/当前版本号段同步 v2.3.21 W406 |
| README.md / STRUCTURE.md / docs/00-导读/项目说明.md | W406 | bump_version 同步 v2.3.21 W406 |
| 项目认知总览.md | W406 | 项目认知总览独立存档（背景/目标/技术栈/目录/模块职责/进度/待办/雷区） |

## W407 修数据路径代码异味（P2）（2026-08-09）

| 文件 | W | 说明 |
|---|---|---|
| site/data/dialogue-sentiment.html | W407 | fetchJson 路径补 ../../ 前缀（`scripts/output/data/`→`../../scripts/output/data/`），与 80+ 页统一，http 模式正确解析 JSON |
| site/data/81-hardships-view.html | W407 | mount() 加 file:// 守卫，跳过 /dataset/ 死 fetch 直走 EMBEDDED 离线示例（/dataset/ 为 api_server 挂载点，http 模式仍走 API） |
| site/data/character-relationship-3d-view.html | W407 | 同 81-hardships-view：file:// 守卫跳过 /dataset/ 死 fetch |
| scripts/_p1_viz_audit.js | W407 | 可复用可视化异常检测脚本（零尺寸 canvas/WebGL/SVG 空白/横向溢出，86 页全量） |
| site/dukou-engine.html | W407 | 页脚版本升 v2.3.22 W407 + 补 W407 里程碑 |
| CHANGELOG.md | W407 | 新增 W407 版本段（四件套）+ 编号规则 W001-W406→W407 |
| 交接文档.md | W407 | 头部/HEAD/进度段/当前版本号段同步 v2.3.22 W407 |
| README.md / STRUCTURE.md / docs/00-导读/项目说明.md | W407 | bump_version 同步 v2.3.22 W407 |

> 当前版本 v2.3.23（2026-08-09）

## W408 修 static 资源路径（P2 续）（2026-08-09）

| 文件 | W | 说明 |
|---|---|---|
| site/data/*.html（86 文件） | W408 | 内联 CSS @font-face/hero 的 static/fonts\|images 改 ../static/（516 处，静态资源 404 归零） |
| scripts/_fix_static_paths.py | W408 | 批处理工具：正则 `(url\(['\"]\|src=\|href=)static/` → `../static/` |
| site/dukou-engine.html | W408 | 页脚升 v2.3.23 W408 |
| CHANGELOG.md | W408 | 新增 W408 段 + 编号规则 W001-W407→W408 |
| 交接文档.md | W408 | 头部/HEAD/进度/版本号段同步 v2.3.23 W408 |
| README.md / STRUCTURE.md / docs/00-导读/项目说明.md | W408 | bump_version 同步 v2.3.23 W408 |

> 当前版本 v2.3.24（2026-08-09）

## W409 文档同步刷新（2026-08-09）

| 文件 | W | 说明 |
|---|---|---|
| 交接文档.md | W409 | 内容纠偏（HEAD 引用 W406→W408·待办1 截图审查 [ ]→[x]·文件尾最后更新 W405→W408）+ 版本号段/heading/加 W409 里程碑块 |
| CHANGELOG.md | W409 | 新增 W409 段 + 编号规则 W001-W408→W409 |
| site/dukou-engine.html | W409 | 页脚升 v2.3.24 W409 |
| README.md / STRUCTURE.md / docs/00-导读/项目说明.md | W409 | bump_version 同步 v2.3.24 W409（项目说明内部当前版本 v2.3.20→v2.3.24） |
| scripts/output/file-index.md | W409 | W409 反向索引登记 |

> 当前版本 v2.3.27（2026-08-09）

## W412 安全审计剩余项处置（2026-08-09·v2.3.27）

| 文件 | W | 说明 |
|---|---|---|
| xiyouji-agent-web/server/index.ts | W412 | 修改·P0-2 save-env-config 拒运行时覆盖 apiKey/baseUrl（400+refused·仅服务端 .env 读取）·P1-4 systemPrompt v2.3.9→v2.3.26·P2-3 SSE 加固（aborted + 10 分钟 sseTimer 超时清理 + req.on close abortStream + Map 迭代改 forEach 修 TS2802）·P3-3 移除 exec/promisify/execAsync 死代码 |
| xiyouji-agent-web/src/components/SettingsPage.tsx | W412 | 修改·P0-2 移除 API Key/Base URL 输入框（改提示"服务端 .env 配置·禁止运行时覆盖"）·提交体仅 {authToken, internetEnv} |
| xiyouji-agent-web/src/components/ChatMessages.tsx | W412 | 修改·P2-6 两处 ChatMarkdown 渲染输入加 DOMPurify.sanitize（tdesign markdown html:true+unsafeHTML 无消毒实锤） |
| xiyouji-agent-web/package.json | W412 | 修改·P2-6 新增 dompurify ^3.4.13 直接依赖 |
| site/static/js/rag-chat.js | W412 | 修改·P1-2 新增 escapeAttr（含引号转义·属性上下文）应用于来源链接 href |
| site/static/js/dataset-view.js | W412 | 修改·P1-2 新增 escapeHtml 应用于 openRowDrill/renderObjectView/renderKey |
| site/data/cross-time-danmaku.html | W412 | 修改·P2-5 escapeHtml 应用于 hero tooltip/popup·P3-5 页脚 v2.3.27 W412 |
| site/data/tag-cloud.html | W412 | 修改·P2-5 escapeHtml 应用于 tooltip·P3-5 页脚 v2.3.27 W412 |
| site/data/search.html | W412 | 修改·P2-5 全局 escapeHtml 应用于 row 数据集/hit.path/hit.snippet |
| scripts/rag/rag_server.py | W412 | 修改·P2-1 _clamp_int（top_k∈[1,50]·hops∈[1,3]）+ _sanitize_history（仅 list·≤20 条·role 白名单·text≤2000）·do_GET 与 /graph 接入 |
| scripts/rag/xiyouji_rag.py | W412 | 修改·P2-2 _validate_endpoint（仅 https·http 仅 localhost/127.0.0.1/::1 例外·私有网段 10/172.16/192.168/127 拒绝）+ history 防御性过滤·_llm_generate 入口校验抛 ValueError |
| scripts/requirements.txt | W412 | 修改·P2-7 固定 jieba==0.42.1/ruff==0.15.15 + Pillow 11.3.0→12.3.0 + pytest 8.4.2→9.0.3（CI pip-audit 实测 26 漏洞归零） |
| mcp-server/pyproject.toml | W412 | 修改·P2-7 fastmcp>=0.1.0,<1.0（防 3.x 大改版） |
| scripts/security_scan.py | W412 | 修改·P1-3 新增 SEC-005 规则（sk- 前缀 16+ 字符·high·覆盖 DeepSeek/Qwen） |
| scripts/api/api_server.py | W412 | 修改·P3-2 CORS 白名单（仅 127.0.0.1:8787/localhost:8787 + file:// null 回显·其余不带 CORS 头）·两处 `*` 均替换 |
| site/index.html | W412 | 修改·P3-5 页脚 v2.3.27 W412 |
| site/_headers | W412 | 修改·P1-2 补遗：script-src 补 https://d3js.org 白名单（页面实际 D3 CDN·原 cdn.jsdelivr.net 死配置 0 引用） |
| .gitignore | W412 | 修改·新增 SECURITY-AUDIT-2026-08-09.7z/.password 忽略规则（加密归档不入库） |
| SECURITY-AUDIT-2026-08-09.md | W412 | 加密归档·7z AES-256 -mhe=on → SECURITY-AUDIT-2026-08-09.7z·明文已删·密码存本地 .password（gitignore） |
| site/dukou-engine.html | W412 | 修改·页脚升 v2.3.27 W412（安全审计剩余项处置段） |
| README.md / STRUCTURE.md / docs/00-导读/项目说明.md | W412 | 文档同步·bump_version 升 v2.3.27 W412·主描述改 W412 + 尾部补 W411（去重复 W412） |
| CHANGELOG.md | W412 | 新增 W412 版本段（四件套）·编号规则 W001-W411→W001-W412·W411 状态行纠偏（已 push 9991982） |
| 交接文档.md | W412 | 文档同步·当前进度段加 W412 里程碑·版本号列表/HEAD/W 编号·待办安全审计剩余项更新 |
| scripts/output/file-index.md | W412 | W412 反向索引登记 |

> 当前版本 v2.3.27（2026-08-09）

## W413 仓库文件策略审查（2026-08-09·v2.3.28）

| 文件 | W | 说明 |
|---|---|---|
| 交接文档.md / 交接文档-archive.md / 项目交接参考手册.md / 项目概览.md / 项目认知总览.md / 项目GitHub参考调研报告.md | W413 | 恢复入库·严格审查无敏感内容（初版 W413 曾 git rm --cached 转本地·用户改口"其他全部上传"后 git add 恢复 tracked） |
| docs/_dev/（3 文件） | W413 | 恢复入库·开发内部资产无敏感内容 |
| docs/_templates/（3 文件） | W413 | 恢复入库·模板资产无敏感内容 |
| docs/superpowers/（11 文件） | W413 | 恢复入库·specs/plans 过程文档无敏感内容 |
| docs/10-方法论沉淀/（14 篇） | W413 | 恢复入库·方法论沉淀无敏感内容（初版 W413 曾 gitignore） |
| .gitignore | W413 | 修改·移除 W413 初版本地化规则（6 文档/方法论/_dev/_templates/superpowers）·保留 .workbuddy/ 与硬性排除规则（.env/审计档/依赖/构建产物/RAG 索引/基线） |
| scripts/verify_delivery.py | W413 | 修改·CORE_DOCS 恢复 CHANGELOG + 交接文档两份硬门禁·移除 LOCAL_OPT_DOCS 逻辑·A4_DOCS 恢复 4 份 |
| assets/fonts/source/（5 文件） | W413 | 入库·字体源 git add -f 强制入库（NotoSerifSC-var.ttf 24MB + JetBrainsMono ×2 + NotoSansSC woff2 ×2） |
| README.md / STRUCTURE.md / docs/00-导读/项目说明.md | W413 | 文档同步·头部版本描述改 W413 修正（严格审查入库边界·全部恢复入库）·项目说明 45 行 v2.3.27→v2.3.28 |
| CHANGELOG.md | W413 | 新增 W413 版本段（四件套）·编号规则 W001-W412→W001-W413 |
| 交接文档.md | W413 | 文档同步·当前进度段加 W413 里程碑·HEAD/W 编号 v2.3.28 W413·README 引用 v2.3.28·CHANGELOG 范围 W001-W413 |
| site/dukou-engine.html | W413 | 修改·页脚升 v2.3.28 W413（仓库文件策略审查段） |
| site/index.html | W413 | 修改·页脚 v2.3.27 W412→v2.3.28 W413 |
| site/data/cross-time-danmaku.html | W413 | 修改·页脚 v2.3.27 W412→v2.3.28 W413 |
| site/data/tag-cloud.html | W413 | 修改·页脚 v2.3.27 W412→v2.3.28 W413 |
| scripts/output/file-index.md | W413 | W413 反向索引登记 |

## W414 README 用户手册改造（2026-08-09·v2.3.29）

| 文件 | W | 说明 |
|---|---|---|
| README.md | W414 | 重构·用户手册 + 开发者分区两级引导（普通读者专区置顶：GitHub Pages 一键直达链接/内容导航表/数据维度全景/目标读者清单·开发者专区 details 折叠：目录/脚本/测试/截图审查/双索引/规范）·头部 v2.3.29 W414 |
| STRUCTURE.md | W414 | 文档同步·头部 v2.3.28 W413→v2.3.29 W414 |
| docs/00-导读/项目说明.md | W414 | 文档同步·头部 + 45 行当前版本 v2.3.28→v2.3.29 |
| CHANGELOG.md | W414 | 新增 W414 版本段（四件套）·编号规则 W001-W413→W001-W414 |
| 交接文档.md | W414 | 文档同步·头部/当前进度段/HEAD/W 编号 v2.3.29 W414·README 引用 v2.3.29·CHANGELOG 范围 W001-W414·接续 W415 |
| 项目交接参考手册.md | W414 | 文档同步·头部 v2.3.29 W414 + 接续 W 编号 W415 |
| 项目概览.md | W414 | 文档同步·头部/HEAD v2.3.29 W414 + W414 里程碑条目 |
| 项目认知总览.md | W414 | 文档同步·头部/HEAD v2.3.29 W414 |
| site/dukou-engine.html | W414 | 修改·页脚升 v2.3.29 W414（README 用户手册改造段） |
| site/index.html | W414 | 修改·页脚 v2.3.28 W413→v2.3.29 W414 |
| site/data/cross-time-danmaku.html | W414 | 修改·页脚 v2.3.28 W413→v2.3.29 W414 |
| site/data/tag-cloud.html | W414 | 修改·页脚 v2.3.28 W413→v2.3.29 W414 |
| scripts/output/file-index.md | W414 | W414 反向索引登记 |

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
