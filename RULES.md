# RULES.md — 必守规则单一入口

> **📖 定位**：全部必守规则的**唯一查询入口**——按规则域分节，每条一行 + 权威指针。本文件是**索引层**，不复制规则正文；条目与正本冲突时以指针目标为准。
> **四文档分工（W1157 建）**：RULES.md=规则（本文件）· AGENTS.md=项目全貌与工作流程正本（§7 快速上手）· CLAUDE.md=宿主自动加载速查（最高频 17 条）· pitfalls.md=坑位表（实证教训按编号查）。
> **维护契约**：新增规则先落正本（AGENTS.md §6 / docs/00-导读/文档规范.md），再在此登记条目行并全篇去重；禁写会漂移的现役值（版本号/W 号）。

## 1. 批次与提交

1. **开批先占号**：动工前必须 `python scripts/reserve_w.py` 占号并在对账表登记认领，未占号不动手 → AGENTS.md §6-17
2. **提交前三问**：本批问题全解决或登记去向？防复发判据/坑表落地？其他 Agent 能从项目文件了解全部决策？→ AGENTS.md §6-18
3. **收官提交用 safe_commit**：`python scripts/safe_commit.py --expect-spec scripts/output/_w<批号>_spec.json`，暂存索引只许含本批件（防代提） → AGENTS.md §4.3
4. **CI 推送节奏**：回填/订正永不单独开 PR；同会话当日多批合并一 PR；收官产物须提交前生成完，禁追加提交 → AGENTS.md §6-21
5. **级联按清单 add**：batch_cascade 落盘后按 `_cascade_files_<批号>.txt` 逐面 add，禁 `git add -A` → AGENTS.md §4.3
6. **六文档同步**：每批 CHANGELOG+HANDOVER 必写（核心 2），里程碑时 bump_version 补齐辅助 4 → AGENTS.md §6-1
7. **治理文档体积窗**：CHANGELOG/file-index ≤256KiB、台账 ≤60 数据行；仅超窗才搬，压缩优先于搬段 → AGENTS.md §6-22

## 2. 代码与验证

1. **E1 铁律**：每个文件修改后 Grep spot-check 验证落地，声明≠落地=假收敛 → AGENTS.md §6-2
2. **改内联脚本必跑** `python scripts/generate_csp.py`（哈希失配=整脚本被浏览器拒执行） → AGENTS.md §6-3
3. **批量改 CSS/JS 后验括号/引号平衡**（check_structure.py） → AGENTS.md §6-4
4. **Python 改动结构检查**：改 .py 后跑 `pwsh -File scripts/guardrails/check_changed.ps1`，退出码 0 才过 → AGENTS.md §6-20
5. **异常分类对齐失败语义**：保护逻辑禁宽 except 吞代码缺陷（NameError/TypeError 直接抛）；每条新保护逻辑须配「它真的生效」正向证据 → AGENTS.md §6-23
6. **批量重写后**：`git diff --name-only` 对比改动范围，非必要改动 `git restore` 回退 → AGENTS.md §6-10

## 3. 内容与站点

1. **file:// 铁律**：新页面必须 EMBEDDED 回退 + 零外域依赖（D3/Three 本地引用，禁外域 CDN） → AGENTS.md §6-5
2. **新页落地**：可视化页进 site/data/、索引进 site/ 根+tag-cloud+sitemap；禁投 site/chapters|characters|themes → AGENTS.md §6-6
3. **内容可信度轨**：新内容走元信息块 v2 + 术语一致性 + 引文硬验证；写引文前先 `_cite_probe.py` 探针 → AGENTS.md §6-13 / AGENTS.md §4.3
4. **禁重跑 w286_merge_yuanwen_shendu.py**（A1 深度解读 SD 编号会再次错位） → AGENTS.md §6-9
5. **双协议**：代码 MIT + 文本 CC BY-NC 4.0（非商用） → AGENTS.md §6-11

## 4. 设计与动效

1. **动效契约**：新增/修改可视化页动效守 DESIGN.md §5——时长 ≤600ms、reduced-motion JS 守卫（MOYUN_RM 调用点级短路）、tooltip 统一 `.chart-tooltip`；批量改动后重跑 generate_csp.py + 时长扫描 → AGENTS.md §6-12
2. **设计方向锁定**：「新中式·数字雅集」（宣纸底/墨文/朱砂点缀/零外域依赖） → DESIGN.md §1-4

## 5. 协作与授权

1. **先取证再假设**：诊断前端显示问题先拿截图+Console+复现条件，再下根因结论 → AGENTS.md §6-7
2. **禁止擅改管控文件**：CHANGELOG 历史段、归档件、门禁脚本本体等改动须用户批准 → docs/00-导读/文档规范.md §11.2
3. **修实例必修根**：修复暴露同类风险时同批或次批根治，禁「值得排期/等点号」收尾；教训权威落坑表，私有记忆仅镜像 → AGENTS.md §6-14
4. **禁补丁加补丁**：修复必须从根因；教训须转机器判据（硬守卫/断言/自测），使下批不可能再犯 → AGENTS.md §6-15
5. **协作与环境约束**：① 禁主动创建 automation ② GPU 重负载先获批分批 ③ 禁用 ~/.minimax ④ 给用户的命令/路径完整禁缩写 ⑤ 答复必须显式给推荐 ⑥ 有复用价值的教训必须项目内留载体 → AGENTS.md §6-16
6. **豁免审批**：豁免/白名单/基线新增条目必须用户批准；豁免只增不减为默认 → AGENTS.md §6-16⑦
7. **禁 CodeBuddy/WorkBuddy**：项目一切 AI 功能不使用该品牌工具链及其任何残留 → AGENTS.md §6-19
8. **并行会话工作树隔离**：各自 `git worktree add <独立路径> -b <独立分支> <基线>`（分支名不可重名）；迁出后精确回滚共享树残留并书面告知其余会话 → AGENTS.md §6-24

## 6. 环境与工具

1. **本机环境坑全集**（make 缺失直调脚本/py 三语境/BOM 禁/heredoc 禁/curl --ssl-no-revoke//tmp 对 Python 不可见/Edit 前必 Read/Bash 工作目录跨调用持久）——唯一权威随实测滚动更新，本节不复制正文 → AGENTS.md §4.3
2. **PowerShell 选择**：`pwsh`（7）与 `powershell`（5.1）并存，需 PowerShell 一律用 pwsh；禁 PowerShell 写仓内文件 → AGENTS.md §4.3

## 7. 禁改与豁免

1. **禁改清单全量**：CHANGELOG 历史段、archive/ 归档件、.env 与审计档、verify_delivery.py 与 pre-commit、check_index_health.py、文档规范本体、bump_version.py 等 → docs/00-导读/文档规范.md §11.2
2. **归档只增不删**：archive/ 是「博物馆」，退役件 git mv 归位 + 台账必登记 → docs/00-导读/文档规范.md §5
3. **检查任务按委托字面范围执行**，超范围发现走登记去向而非顺手扩权 → AGENTS.md §6-14
