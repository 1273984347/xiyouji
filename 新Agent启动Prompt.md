# 新 Agent 启动 Prompt（可直接发送）

> **用途**：新 session 启动时，将下方【正文】整段复制发给新 Agent，快速完成项目认知 + 规则约束。
> **当前 HEAD / 下一 W / 待办**：见 [交接文档.md](交接文档.md)「一、当前进度」——本文件不维护版本清单，避免过期。
> **维护契约（防乱写）**：本文档是「速用精简版」payload，只允许结构性编辑——① 保持【正文】五段骨架不变；② 新增/变更规则必须**就地替换**旧表述并全篇去重；③ 禁止追加「W### 速记 / 治理要点」类历史段（历史一律写入 [CHANGELOG.md](CHANGELOG.md) 与交接文档「三、方法论沉淀」）；④ 涉及门禁/预算/计数口径时，全篇只保留一份现役值；⑤ 与交接文档/文档规范冲突时以后两者为准。
> **修订**：2026-08-10 创建 · 2026-08-18 v2 重构（五段骨架 + 维护契约，清理历史速记与重复口径）。

---

## 正文（复制以下内容发送给新 Agent）

你是《详解西游记》项目（D:\1\xiyouji）的新接任 Agent。本项目由多 session / 多 Agent 协作制作，有严格的文档同步与文件管控规则。请按以下顺序了解项目并遵守规则：

【第 1 步 · 定位现状（必读 3 份）】
1. 交接文档.md →「零、当前阻塞」+「一、当前进度」：当前 HEAD（vX.Y.Z W###）、下一 W 编号、遗留阻塞/待办
2. README.md → 项目全貌：A1–A6 内容板块（615 篇）、可视化页 86（site/data 共 87 个 HTML，「86」不含模板壳 _shell.html）、在线站点、双协议授权
3. docs/00-导读/项目说明.md → 项目状态、轨标、关键产出

【第 2 步 · 文件管控（动手前必读）】
4. docs/00-导读/文档规范.md §11：
   - §11.1 必同步文件（核心 2 份硬门禁：CHANGELOG / 交接文档 + 辅助 4 份 + 页脚 + 旁文档）
   - §11.2 禁改文件（CHANGELOG 历史段 / 归档 / .env 密钥 / 门禁脚本 / memory / 字体源等，附误改后果）
   - §11.3 接手速查 6 步
   - §11.4 W 完成后 10 项同步核对
5. 交接文档.md →「三、方法论沉淀」：可复利经验（E1 铁律、DRL 三 skill 闭环等），必须遵循

【第 3 步 · 结构与历史（深挖时）】
6. STRUCTURE.md → 目录结构
7. scripts/output/file-index.md → 反向索引（文件 → W → 改动）
8. CHANGELOG.md → 正向时间线（每 W 附来源/执行/验证/状态四件套）

【第 4 步 · 干活铁律】
- 方向：从交接文档「二、下一步方向候选清单」按优先级选
- 每个文件修改后：Grep spot-check 验证落地（E1 铁律：声明 ≠ 落地，禁止假收敛）
- memory：按当前 Agent 环境路径读写（TRAE `~/.trae-cn/memory/` · Qwen `~/.qwenworkcn/awareness/main/` · Claude/Codex `~/.claude/projects/<编码路径>/memory/`），Read-before-Edit + Grep-verify-after-Edit + 集中写入点
- 禁改：CHANGELOG 历史段、归档 3 份、.env、SECURITY-AUDIT 档、verify_delivery.py、bump_version.py 等（见 §11.2）
- 版本行：跑 bump_version.py 后必须 Grep 校验 file-index 历史段未被污染（W418/W419 复现 2 次）
- 批量改写：改完先 `git diff --name-only` 对比改动范围，对"本应无变化"的文件 `git restore` 回退（W419 经验）
- Windows 本机执行 Python 一律用 `py -3`（裸 `python` 可能命中假解释器：Microsoft Store 占位 stub 会 exit 9009；PATH 前置的无扩展名 PE shim 更会静默 no-op——零输出零副作用 exit 0，W515 实证），如 `py -3 scripts/verify_delivery.py`
- A1 深度解读（SD001–SD101）：SD 编号 ≠ 原著回号；源文件元数据注释在第三行；**禁止重跑 `w286_merge_yuanwen_shendu.py`**（会再次错位），改动前先读交接文档 W419 段
- 改内联脚本后：必须重跑 `py -3 scripts/generate_csp.py`（否则 CSP 哈希失配，整脚本被浏览器拒执行）
- 3D/时间线页：`main()` 用 `window load` 事件触发——**内联 `defer` 属性对无 src 脚本无效**，勿依赖
- 新门禁/新生成器：先跑**负样本自测**（构造坏文件确认能抓到）再全量
- 提交流程：每完成一个 W 按 §11.4 勾选清单同步文档 → `python scripts/verify_delivery.py` 全绿 → 提交 → push → 确认 CI / Security / Deploy Pages / Screenshot Review 全绿 → 状态行收尾

【第 5 步 · 现役口径（唯一版本，勿信旧速记）】
- A4 计数：**209 篇**（EXPECT_A4 断言按字面量核查 README/STRUCTURE/项目说明/交接文档 四文件，该字样禁删）；A1–A6 真实计数：**615 篇**（门禁算法＝六板块目录顶层 .md 磁盘计数 == README「共 N 篇」声明值；W505 起 611→615）
- LHCI 硬门禁：**LCP < 5000ms · CLS < 0.3 · TBT < 300ms**（W424 实测校准）
- 性能预算：`scripts/output/perf-budget.json`（total 921600 bytes）
- CSP：233 页 · `script-src-attr 'none'` · 哈希总数当批现测（勿引用历史速记值作验收阈值；W513 时点实测 1189）
- 更早批次细节与历史坑：一律查 CHANGELOG 与交接文档「三、方法论沉淀」，本文件不内嵌历史速记
