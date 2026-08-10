# 新 Agent 启动 Prompt（可直接发送）

> **用途**：新 session 启动时，将下方【正文】整段复制发给新 Agent，即可快速完成项目认知 + 规则约束。
> **创建**：2026-08-10（W419 处置收尾·文档规范 §11 表格化配套）·当前 HEAD 版本见 [交接文档.md](交接文档.md)「一、当前进度」。
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
- 提交后 push，验证 CI/Security/Deploy Pages/Screenshot Review 全绿，然后做状态行收尾

完成后把 W### 进展同步到交接文档「一、当前进度」+ 方法论沉淀（如有新经验）。
