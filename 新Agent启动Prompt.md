# 新 Agent 启动 Prompt（可直接发送）

> **用途**：新 session 启动时，将下方【正文】整段复制发给新 Agent，即可快速完成项目认知 + 规则约束。
> **创建**：2026-08-10（W419 处置收尾·文档规范 §11 表格化配套）·当前 HEAD 版本见 [交接文档.md](交接文档.md)「一、当前进度」。
> **更新**：2026-08-10 W419 补充——① bump_version 污染校验（W418/W419 复现 2 次）② 批量重写脚本最小化 diff（git restore 非必要改动）③ A1 SD 雷区（w286 脚本重跑会错位·禁止重跑）。
> **更新（2026-08-11 W423）**：① verify_delivery 四新门禁（A1 导航相邻性/docs/01 链接/sitemap 覆盖/site/data 回退模式）② 性能预算收紧（LHCI LCP 5000→4500·CLS 0.3→0.2·CJK 字体 swap→optional·D3/Three 移出 head）③ A4 计数门禁校准 **209 篇**（2026-08-11 修正）④ security 门禁修复（依赖审计只扫仓库 requirements*.txt，不再回退扫整个 Python 环境）。
> **配套**：[交接文档.md](交接文档.md)（进度中枢）/ [docs/00-导读/文档规范.md](docs/00-导读/文档规范.md) §11（文件管控）/ [scripts/output/file-index.md](scripts/output/file-index.md)（反向索引）。
> 本文件是交接文档的「速用精简版」——若正文与交接文档/文档规范冲突，以后两者为准。

---

## 正文（复制以下内容发送给新 Agent）

你是《详解西游记》项目（d:\1\xiyouji）的新接任 Agent。本项目由多 session / 多 Agent 协作制作，
有严格的文档同步与文件管控规则。请按以下顺序了解项目并遵守规则：

【第 1 步：定位现状（必读 3 份）】
1. 交接文档.md →「零、当前阻塞」+「一、当前进度」：当前 HEAD（vX.Y.Z W###）、下一 W 编号、遗留阻塞/待办
2. README.md → 项目全貌：A1-A6 内容板块（611 篇）、86 可视化页、在线站点、双协议授权
3. docs/00-导读/项目说明.md → 项目状态、轨标、关键产出

【第 2 步：明确规则（动手前必读）】
4. docs/00-导读/文档规范.md §11 文件管控清单（最重要）：
   - §11.1 必须同步的文件（核心 2 份硬门禁 CHANGELOG/交接文档 + 辅助 4 份 + 页脚 + 旁文档）
   - §11.2 禁止擅自修改的文件（CHANGELOG 历史段 / 归档 / .env 密钥 / 门禁脚本 / memory / 字体源等，附误改后果）
   - §11.3 接手速查 6 步
   - §11.4 同步核对速查表（10 项勾选清单，W 完成后逐项核对）
5. 交接文档.md →「三、方法论沉淀」：可复利经验（E1 铁律、DRL 三 skill 闭环等），必须遵循

【第 3 步：理解结构与历史（深挖时）】
6. STRUCTURE.md → 目录结构
7. scripts/output/file-index.md → 反向索引（文件→W→改动）
8. CHANGELOG.md → 正向时间线（每 W 附来源/执行/验证/状态四件套）

【第 4 步：开始干活前的铁律】
- 从交接文档「二、下一步方向候选清单」按优先级选方向
- 每完成一个 W：严格按 §11.4 十项勾选清单同步全部文档，跑 verify_delivery.py 必须全绿
- 提交前双重门禁：TodoWrite 逐项勾选 + pre-commit 自动跑 scripts/verify_delivery.py（临时跳过用 --no-verify 不推荐）
- 每个文件修改后：Grep spot-check 验证落地（E1 铁律：声明 ≠ 落地，禁止假收敛）
- 修改 memory（user_profile.md / project_memory.md）必须遵守：Read-before-Edit + Grep-verify-after-Edit + 集中写入点
- 禁止擅改：CHANGELOG 历史段、归档 3 份、.env、SECURITY-AUDIT 档、verify_delivery.py、bump_version.py 等（见 §11.2）
- 跑 bump_version.py 后：必须 Grep 校验 file-index 历史段未被全局替换污染（W418/W419 复现 2 次·E2 判据「历史条目保留旧值」·只信任 bump 改 README/STRUCTURE/项目说明版本行）
- 批量重写型脚本（重建/批量编辑多个文件）改完后：先 `git diff --name-only` 对比改动范围，对"本应无变化"的文件 `git restore` 回退，仅保留真实修复目标（W419 经验·1-37/73-100 回非必要格式改动已回退）
- 若涉及 A1 深度解读（SD001-SD101）改动：SD 编号≠原著回号（编号=创作序号）·源文件元数据注释在第三行（第一行是标题）——`w286_merge_yuanwen_shendu.py` 重跑会 fallback 按编号放置导致 SD 再次错位（W419 已归位 22 篇·40-72 回全覆盖）·**禁止重跑该合并脚本**；改动 SD 归位前先读交接文档 W419 段
- 提交后 push，验证 CI/Security/Deploy Pages/Screenshot Review 全绿，然后做状态行收尾

【W420-W423 治理要点（速记）】
- **W420/W421**：A1 深度解读 100/100 补全（SD102/SD103）；导航必须指向**相邻回**（上一回=N-1·下一回=N+1·第 1 回无上·第 100 回全书完）——lint_links 只查链接存在、不查指向正确，链接质量类任务别只做 404 审计；Screenshot Review 已提速（改动范围判定 + `--only-pages`）
- **W422**：verify_delivery 新增 4 门禁（A1 导航相邻性 / docs/01 链接 / sitemap 覆盖 154 页 / site/data 内嵌回退模式），提交前必须全绿；文档健康归档后 CHANGELOG 83 行·file-index 127 行·交接文档 556 行——新文档执行双索引、存量以 file-index 追溯
- **W423**：性能预算收紧（LHCI LCP ≤4500ms / CLS ≤0.2 / TBT ≤300ms；CJK 字体 swap→optional·D3/Three 移出 head）——新页面/改动不要在 `<head>` 同步加载外部脚本，勿破坏渲染阻塞优化
- **遗留待办**：CSP 仍含 unsafe-inline（GitHub Pages 不消费 `_headers`，部署 Netlify/Cloudflare 后切换）；真实跨访客读者量未验证（GoatCounter / Netlify 待办）；A4/A5 部分文档缺 W### 出处 ID（回填时以 file-index 追溯）；A4 计数门禁已按 **209 篇** 校准
- **安全门禁（2026-08-11 修正）**：`security_scan.py` 依赖审计只扫仓库 `requirements*.txt`（`scripts/requirements.txt`），不再回退扫整个 Python 环境——本地跑 `--all` 不应再出现 `(environment)` 高漏洞；若本地装了 `.pw-browsers/`（Playwright 浏览器），扫描已排除该目录

完成后把 W### 进展同步到交接文档「一、当前进度」+ 方法论沉淀（如有新经验）。
