# MAINTAINING.md — 治理文件维护契约（W1279 拆出自 AGENTS·W1282 批）

> **📖 定位**：改治理文件（AGENTS.md / pitfalls.md / docs/agent/gates.md / 路由表）前**必读本文**。
> AGENTS.md 是每会话加载的**行为地图**（铁律+路由+命令）——它只留极简维护契约，全文在此。
> 载体铁则（16-⑥）：本文在仓内可检索·私有记忆仅镜像。
> **L2 三件**（41 槽 C1 对象）= docs/agent/gates.md + pitfalls.md + docs/agent/agent-web.md——三件存在且含阅读契约由第 41 槽 C1 守护；本文件（MAINTAINING）与 AGENTS 路由表另由 41 槽 C2 路由行判据守护。

## 一、体量预算与「超限即拆」

| 文件 | 预算 | 执行点 |
|---|---|---|
| AGENTS.md | ≤200 行（地图形态·铁律前移+路由表） | 74 槽 BYTE_CAPS 34000 字节 + 41 槽 C3 行数 |
| CLAUDE.md | ≤60 行（导入 AGENTS + Claude 专属） | 32 槽 C3 |
| pitfalls.md | ≤262144 字节（全局硬窗·test_w1120 实测口径） | 74 槽 BYTE_CAPS 262144 |
| gates.md / STRUCTURE.md 等接收方 | 摘要外移时**同步定接收方预算**（防膨胀转移） | 74 槽 BYTE_CAPS 随批挂载 |

**超限动作 = 拆分或修剪，禁压缩凑数**（W1278 教训：压缩后正本失去可执行性——后续已按
「拆分+归档兜底」纠偏；pitfalls 现役形态＝正本判据层 + archive 叙事层·E-NN 双命中）。

## 二、退役三标准（有进有出的阀门·事前而非事后）

1. **只在该次会话为真**的内容（事故细节/一次性决策来龙去脉）→ 移 pitfalls 或可检索历史，不入每次加载的规则层。
2. **已过时**的规则 → **直接删除**（归档的矛盾仍是矛盾——不在 Agent 可能读到的位置留旧规则）。
3. **已被代码/工具机械化强制**的规则（格式/Lint/CI 拦截）→ 从文本规则移除，交给工具执行。

一条规则留在入口文件的唯一理由：**它在每一次会话中都为真，且 Agent 无法从仓库一步推断出来**。

## 三、添加前四问（vLLM 式·新规则入entry前自检）

1. Agent 是不是**已经能做到**（从仓库/代码可推断）？能 ⇒ 不加。
2. 是不是**偶发单次事件**？是 ⇒ 改用 Linter/CI 修复或落 pitfalls 单条，不加。
3. 是不是**重复上游文档**（README/STRUCTURE/工具文档）？是 ⇒ 加指针，不加正文。
4. 是不是**与现有规则冲突**？是 ⇒ 先解决冲突，再加。

## 四、pitfalls「同类两犯上提」机制

同类错误**第二次**出现时：该坑的纪律上提 AGENTS 铁律区（一句版）或路由表触发条件；
pitfalls 条目保留完整故事，并在条目内标注「已上提」。上提缺位的机械化检测（按条目
域标注聚类·见 E-271 分类字段讨论）为候选槽——现役以六主题+域标注文本形态弱分类。

## 五、RULES 局部化预留形态（D 盘点结论·2026-11-19）

D 盘点实测 RULES 41 条**零真例外**（全部为全局规则指针）⇒ RULES.md 撤并（W1282 批·
索引职责并入 AGENTS 路由表）。**局部化预留**：未来若出现真例外条款——

- 形态 = **按主题族聚合**（`rules/<族>.md`·非按目录），每份头部写**作用域声明**（适用路径/触发条件）；
- 路由表条目**从作用域声明机械生成**（防两份漂移）；
- **不继承**（每份自包含全量·禁指向其他 RULES 的索引式跳转）；
- 三条件同时满足才局部化：作用域与边界重合 / 触发频率值得单独加载 / 自包含可执行；
- 主题性规则（按任务类型触发）不按目录拆——AGENTS 用触发条件描述或主题文档路由。

## 六、时间纪律与占号（详情在批次交付流水线 §九 / 坑表 E-128）

提交期门禁分层（E-265）·长任务恒后台（E-266）·快判据三件套先行（E-268）·失败续跑（E-267）·
探针按 hash 复用（E-270）·spec 形态一次定形（E-269）；占号三源并集+预留位（铁律 17·E-128）。

## 七、脚注与版本契约

AGENTS 版本脚注由级联自动滚动（保留最近 5 条·每条 ≤120 字·日期阿拉伯形态）；尾句
「如与上述权威文档冲突，以权威文档为准。」为写入侧与门禁侧共同契约（E-258·禁单方改写）；
版本号 vX.Y.Z = 内容发布批次编号（非 SemVer）——查「改了什么」看 CHANGELOG。

## 八、本机环境事实（W1279 自 AGENTS §4 迁入·每会话相关但非行为约束）

**本机环境事实（Windows 单机·机器相关不入 L2·随实测滚动更新）**：
- `make` 未安装：Makefile 目标不可用，直调 `python scripts/<对应脚本>`（映射见 Makefile 注释）。
- 全局 Python 3.12·无项目 `.venv`：`pytest`/`playwright`/`pip_audit` 加 `-m` 前缀调用，**三语境分清**——① 仓内文档/工具表/CI/Makefile 一律写可移植形态 `python -m <工具>`（CI 在 Linux·`py` 不存在）；② 本机 PowerShell 侧统一 `py -3 -m`（该侧 `python` 是应用执行存根·调用即 exit 9009 无输出）；③ 本机 git-bash 侧 `python` 为实解释器可直呼。`py -3` 两 shell 一致指向全局 3.12，但**不得写成全仓约定**（`py` 非跨平台·CI/Linux 失效）。`ruff`/`uv`/`node`/`npm`/`git`/`gh`/`pwsh` 可直呼。
- `pwsh`（PowerShell 7）与 `powershell`（5.1）并存：需 PowerShell 时一律用 `pwsh`（默认 UTF-8 无 BOM）；`powershell` 是 5.1（GBK 默认·W509 BOM 坑源），且仍遵守仓内「禁 PowerShell 写仓内文件」铁则。
- 提交门禁 hook（.git/hooks/pre-commit）与本清单同口径取解释器：首选 `py -3`，回退系统 Python 3.12 绝对路径，两者均须实测可运行（`-c "import sys"` 返回 0）才选用；**不按 PATH 上的 `python`/`python3` 形状挑选**（两 shell 解析不同·见上一条）·不依赖任何厂商托管运行时路径。
- pre-commit 框架**已装**（实测 4.6.0·W1014 订正本条与磁盘现势的矛盾）但**禁 `install`**：`pre-commit install` 会覆盖手写 `.git/hooks/pre-commit`，破坏零依赖门禁。`.pre-commit-config.yaml` 仅为「误 install 后核心门禁不丢」的等价备份（W424），现役执行路径恒为手写钩子；W1014 已删其指向退役件 `sync_docs.py` 的坏 hook 段。
- 本机取数与命令坑（W902 自 Agent 记忆固化·长期实测）：`curl` 必须 `--ssl-no-revoke`（本机代理链下否则大面积失败）；`/tmp` 对 Windows Python 不可见（Git Bash 的 /tmp 是 MSYS 虚拟路径·Python 侧须用 `tempfile` 或仓内 tmpe/）；`gh api` 查询含中文的 search 语句必须走 `-f` 参数（URL 参数形态中文被编码截断）；PMC 取 PDF 常挂 Cloudflare → 用 Europe PMC `fullTextXML` 端点兜底。
- **Bash 工具工作目录跨调用持久（W596 两犯）**：某条命令 `cd 子目录` 后，后续所有相对路径命令都落在子目录——长批次开头 `cd /d/xiyouji` 归位或全程绝对路径；「找不到文件」先查 pwd。
- **Edit 工具前置 Read**：Edit 前必须先用 Read 工具读过该文件（sed/grep 的 Bash 读取不算）——直接 Edit 报 "File has not been read yet"；批量编辑前先对每个目标文件发 Read。
- `pyyaml==6.0.2` 已登记进 CI 真实安装源 `scripts/requirements-hashed.txt`（W813 立判据·W1195 起 CI 安装源改哈希化清单·W1198 改绑）：工作流 YAML 可解析性守卫（test_ci_wiring.py J3）依赖它，依赖缺失即**判红**（禁静默跳过假绿）。
