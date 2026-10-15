# W514 方案：治理文档口径一致性修复（五元文档数字校正 + 门禁清单补录）

- **方案编号**：W514（拟占用批次号，现役最大 W513，已预留 max+1）
- **撰写日期**：2026-08-25
- **适用基线**：HEAD `df0f8e1` = v2.3.112 W513（执行时须以 `git rev-parse --short HEAD` 实测复核，不一致则 STOP 对账）
- **批次性质**：纯文档治理批——不修改任何 Python/JS 脚本逻辑、不修改任何 site/data 可视化页、不修改任何 dataset JSON；唯一触碰的 HTML 是 dukou-engine.html 页脚版本链（纯文本插入，非内联脚本）
- **上游依据**：对抗性审查报告（同日产出）P1/P2/P3 发现 + 本方案成文前的逐行取证（所有 old_str 均为 2026-08-25 磁盘逐字原文）
- **格式依据**：skills/xiyouji-plan-authoring/SKILL.md（验收三段式 / 派生命令清单 / 裁掉项显式化 / 落地状态回写 / 启动前三问）

---

## 0. 现状基线（全部为 2026-08-25 实测，非引用）

### 0.1 真实计数（门禁算法：六板块目录顶层 .md 数，排除板块自身 README）

| 板块 | 目录 | 磁盘实测 |
|---|---|---|
| A1 逐回解读 | docs/01-全书逐回解读 | 100 |
| A2 个人随笔 | docs/06-个人随笔 | 44 |
| A3 人物分析 | docs/02-人物深度分析 | 215 |
| A4 主题专题 | docs/03-主题与情节专题 | 209 |
| A5 文化背景 | docs/04-文化与历史背景 | 34 |
| A6 诗词歌赋 | docs/05-诗词歌赋 | 13 |
| **合计** | — | **615** |

README.md 版本行已声明「共 615 篇」，故 `verify_delivery.py` 计数门禁（磁盘==README 声明）为绿。

### 0.2 陈旧点位清单（本批修复对象，T1–T18）

| 编号 | 文件 | 位置 | 陈旧内容 | 应为 |
|---|---|---|---|---|
| T1 | 新Agent启动Prompt.md | L16 | 「内容板块（611 篇）」 | 615 篇 + 86=87−_shell 注记 |
| T2 | 新Agent启动Prompt.md | L46 | 「A1–A6 真实计数：611 篇」 | 615 篇 + 门禁算式说明 |
| T3 | 新Agent启动Prompt.md | L49 | 「1173 哈希」硬编码 | 当批现测措辞（时点参考 1189） |
| T4 | 新Agent启动Prompt.md | L38 后缺失 | 无 py-stub 规避条目 | 新增 `py` launcher 条目 |
| T5 | AGENTS.md | L15 | 「约 86 个」无边界说明 | 86 = site/data 87 − _shell.html |
| T6 | AGENTS.md | L18 | 「共 611 篇」「A3 人物 211」 | 615 / 215 + 口径指针 |
| T7 | AGENTS.md | L63 | 「87 个 HTML」无 _shell 注记 | 补注记 |
| T8 | AGENTS.md | L108 | 「真实计数（611 篇）」硬编码表述 | 动态口径（磁盘==README 声明） |
| T9 | AGENTS.md | §4.2 清单止于第 20 项 | 已挂载的第 21/22 号门禁未登记 | 补录两条 |
| T10 | AGENTS.md | 版本脚注 | 缺 W514 条目 | 按 §维护契约追加 |
| T11 | 统计口径说明.md | L7 | 「篇数 = 611 篇」 | 615 篇 |
| T12 | 统计口径说明.md | L19 | 「A3 … 211」 | 215 |
| T13 | 统计口径说明.md | L28 | 「顶层 .html = 86（含 _shell.html）」 | 87（含 _shell）；86 = 87 − _shell（消除与 CHANGELOG W459 口径块的矛盾） |
| T14 | 统计口径说明.md | L24 | 校验句硬编码「共 611 篇」 | 动态措辞 + 当前 N=615 |
| T15 | 统计口径说明.md | L56 | 「（611 / 209 强制校验）」 | 动态措辞 |
| T16 | 统计口径说明.md | §6 缺溯源条目 | 无 611→615 漂移根因记录 | 新增第 5 条 |
| T17 | docs/00-导读/文档规范.md | L278 | 「A1-A6 计数 611==611」 | 动态措辞（当前 615==615） |
| T18 | docs/00-导读/项目说明.md | L58 | 「A3 人物深化 211 篇」 | 215 篇（同行「A4 主题专题 209 篇」禁动） |

### 0.3 保护位清单（历史事实，本批禁改，用于反向抽查）

| 编号 | 位置 | 内容 | 性质 |
|---|---|---|---|
| B1 | AGENTS.md 第 18 门禁项 | 「基线 frontmatter-baseline.txt 冻结存量 611 篇豁免」 | 冻结基线事实 |
| B2 | 文档规范.md §4.6 区域 | 元信息块基线 611 篇同类表述 | 冻结基线事实 |
| B3 | verify_delivery.py 全文件 | EXPECT_A4 常量 / 计数逻辑 L173-191 / 两门禁挂载 L442-464 / 注释「基线豁免存量 611」 | 禁改门禁脚本铁律 |
| B4 | CHANGELOG.md 历史段（≤v2.3.112）、file-index.md 历史段 | 一切旧数字 | 历史段只增不删 |
| B5 | site/dashboard.html L966、site/dukou-engine.html L152 既有链节 | 「CSP 1173 哈希 0 漂移」等史述 | 页脚版本史 |
| B6 | scripts/output/perf-budget.json | `"total": 921600`（L12） | 已核实正确，无需改动 |

---

## 1. 目标与非目标

**目标（可验证）**
1. 五个元文档（新Agent启动Prompt.md / AGENTS.md / docs/00-导读/统计口径说明.md / docs/00-导读/文档规范.md / docs/00-导读/项目说明.md）中，现役数字与 §0.1 实测完全一致：陈旧模式扫描 0 命中（见 §4 A2 断言表）。
2. AGENTS.md §4.2 门禁清单与 verify_delivery.py 实际挂载数量一致：清单条目数 20 → 22。
3. 六文档同步完成：CHANGELOG 新增且仅新增 1 个 W514 段；交接文档四处更新；辅助 4 文件版本行经 bump_version.py 更新；站点页脚 4 个 + 旁文档 1 份更新。
4. 全部门禁保持绿：`py scripts/verify_delivery.py` 退出码 0。

**非目标（显式裁掉，见 §5）**
- 不新增任何门禁脚本（P2 建议「元文档口径一致性校验」另立批次，见 §7 Q2）。
- 不修改任何历史段、冻结基线、门禁脚本。
- 不处理 CSP 哈希具体数值入库（采用「当批现测」措辞根治，不再硬编码）。

---

## 2. 修改清单（单点替换编辑 E 系列 18 处 + 收尾编排步骤 S/J/K/D/W 系列 10 步；old_str 均为磁盘逐字原文）

执行约定：
- 每个 old_str 在其文件中必须**恰好命中 1 次**；执行 SearchReplace 前先用 §2 各条给出的预检命令核实；命中数 ≠ 1 则 STOP 上报（R5 协议）。
- 同一文件的多个编辑必须**串行**执行（R1）。
- 编辑工具用内置 SearchReplace 或 Python `open(encoding='utf-8')`；**禁止** PowerShell Set-Content / Add-Content 写任何 .md（R2）。

### F1 新Agent启动Prompt.md（4 处）

**E1.1（对应 T1）**
- 预检：`Select-String -Path 新Agent启动Prompt.md -Pattern '内容板块（611 篇）'` → 恰 1 行
- old_str：
  ```text
  2. README.md → 项目全貌：A1–A6 内容板块（611 篇）、86 可视化页、在线站点、双协议授权
  ```
- new_str：
  ```text
  2. README.md → 项目全貌：A1–A6 内容板块（615 篇）、可视化页 86（site/data 共 87 个 HTML，「86」不含模板壳 _shell.html）、在线站点、双协议授权
  ```

**E1.2（对应 T2）**
- 预检：`Select-String -Path 新Agent启动Prompt.md -Pattern '真实计数：\*\*611 篇\*\*'` → 恰 1 行
- old_str：
  ```text
  - A4 计数：**209 篇**；A1–A6 真实计数：**611 篇**
  ```
- new_str：
  ```text
  - A4 计数：**209 篇**（EXPECT_A4 断言按字面量核查 README/STRUCTURE/项目说明/交接文档 四文件，该字样禁删）；A1–A6 真实计数：**615 篇**（门禁算法＝六板块目录顶层 .md 磁盘计数 == README「共 N 篇」声明值；W505 起 611→615）
  ```

**E1.3（对应 T3）**
- 预检：`Select-String -Path 新Agent启动Prompt.md -Pattern '1173 哈希'` → 恰 1 行
- old_str：
  ```text
  - CSP：233 页 · 1173 哈希 · `script-src-attr 'none'`
  ```
- new_str：
  ```text
  - CSP：233 页 · `script-src-attr 'none'` · 哈希总数当批现测（勿引用历史速记值作验收阈值；W513 时点实测 1189）
  ```

**E1.4（对应 T4）**
- 预检：`Select-String -Path 新Agent启动Prompt.md -Pattern 'W419 经验'` → 恰 1 行
- old_str：
  ```text
  - 批量改写：改完先 `git diff --name-only` 对比改动范围，对"本应无变化"的文件 `git restore` 回退（W419 经验）
  ```
- new_str（原行保留，其后插入一行）：
  ```text
  - 批量改写：改完先 `git diff --name-only` 对比改动范围，对"本应无变化"的文件 `git restore` 回退（W419 经验）
  - Windows 本机执行 Python 一律用 `py`（裸 `python` 可能命中 Microsoft Store 占位 stub，exit code 9009），如 `py scripts/verify_delivery.py`（W514 经验登记）
  ```

### F2 AGENTS.md（6 处）

**E2.1（对应 T6）**
- 预检：`Select-String -Path AGENTS.md -Pattern '共 611 篇（A1 逐回'` → 恰 1 行
- old_str：
  ```text
  **核心内容规模**：A1–A6 内容板块共 611 篇（A1 逐回 100 / A2 随笔 44 / A3 人物 211 / A4 主题 209 / A5 文化 34 / A6 诗词 13）；英文站 site/en/ 138 页已全量英文化。
  ```
- new_str：
  ```text
  **核心内容规模**：A1–A6 内容板块共 615 篇（A1 逐回 100 / A2 随笔 44 / A3 人物 215 / A4 主题 209 / A5 文化 34 / A6 诗词 13；算法与边界见 docs/00-导读/统计口径说明.md；W505 起 611→615）；英文站 site/en/ 138 页已全量英文化。
  ```

**E2.2（对应 T5）**
- 预检：`Select-String -Path AGENTS.md -Pattern '约 86 个 D3.js'` → 恰 1 行
- old_str：
  ```text
  - **数据可视化**：约 86 个 D3.js / Three.js 可视化页（site/data/），覆盖 133 个数据维度（章节统计、人物关系网络、八十一难热力图、取经路线、情感热力图、AI 对话等 34 类主题 A–AH）。
  ```
- new_str：
  ```text
  - **数据可视化**：86 个 D3.js / Three.js 可视化页（site/data/ 共 87 个 HTML，「86」不含模板壳 _shell.html），覆盖 133 个数据维度（章节统计、人物关系网络、八十一难热力图、取经路线、情感热力图、AI 对话等 34 类主题 A–AH）。
  ```

**E2.3（对应 T7）**
- 预检：`Select-String -Path AGENTS.md -Pattern 'data/              # 可视化页（87 个 HTML'` → 恰 1 行
- old_str：
  ```text
  │   ├── data/              # 可视化页（87 个 HTML，D3/Three）
  ```
- new_str：
  ```text
  │   ├── data/              # 可视化页（87 个 HTML，D3/Three；「86 可视化页」口径不含模板壳 _shell.html）
  ```

**E2.4（对应 T8）**
- 预检：`Select-String -Path AGENTS.md -Pattern '真实计数（611 篇）'` → 恰 1 行
- old_str：
  ```text
  3. **A4 计数一致（209 篇）** + **A1-A6 真实计数（611 篇）**
  ```
- new_str：
  ```text
  3. **A4 计数一致（EXPECT_A4 字面量「209 篇」）** + **A1-A6 真实计数（六板块顶层 .md 磁盘计数 == README「共 N 篇」声明，当前 N=615）**
  ```

**E2.5（对应 T9）**
- 预检：`Select-String -Path AGENTS.md -Pattern '^### 4.3 脚本工具链要点'` → 恰 1 行；`Select-String -Path AGENTS.md -Pattern '21\. \*\*动态链接门禁'` → 0 行（防重复插入）
- old_str：
  ```text
  ；语法见文档规范 §4.8）

  ### 4.3 脚本工具链要点
  ```
- new_str：
  ```text
  ；语法见文档规范 §4.8）
  21. **动态链接门禁**（check_dynamic_links.py，W459 挂载：解析页面 JS 内拼接生成的链接目标（A1_DOC_MAP 映射、EN source_doc 等）并对仓库路径存在性断言，补 lint_links 静态盲区，死链 = FAIL 阻断提交）
  22. **治理文档维护契约**（check_governance_docs.py，挂载即生效：扫描六文档的追加式损坏模式——历史段遭改写 / 现役值残留多份 / 尾部追加速记段，命中记 WARN 不阻断提交（起步策略），为后续转 FAIL 积累监测数据）

  ### 4.3 脚本工具链要点
  ```

**E2.6（对应 T10）**
- 预检：`Select-String -Path AGENTS.md -Pattern '归档三件套 >1MB 触发规则入文档规范 §5/§8），仅版本脚注同步。如与上述权威文档冲突'` → 恰 1 行
- old_str：
  ```text
  （CHANGELOG-ARCHIVE W001-W399 下移 docs/archive/tier2·归档三件套 >1MB 触发规则入文档规范 §5/§8），仅版本脚注同步。如与上述权威文档冲突，以权威文档为准。*
  ```
- new_str：
  ```text
  （CHANGELOG-ARCHIVE W001-W399 下移 docs/archive/tier2·归档三件套 >1MB 触发规则入文档规范 §5/§8），仅版本脚注同步，2026-08-25（v2.3.113 W514）治理文档口径修复：§1 规模数字校正（核心内容 611→615·A3 人物 211→215·「约 86 个可视化页」注明＝site/data 87 个 HTML 减 _shell.html）+ §4.2 第 3 条改为动态口径（磁盘==README 声明）+ §4.2 补录第 21 门禁 check_dynamic_links（动态链接）与第 22 门禁 check_governance_docs（治理契约）。如与上述权威文档冲突，以权威文档为准。*
  ```

### F3 docs/00-导读/统计口径说明.md（6 处，最先执行——口径源先行，见 §3 Phase 1）

**E3.1（对应 T11）**
- 预检：`Select-String -Path docs\00-导读\统计口径说明.md -Pattern '^## 1. A1-A6 内容篇数 = 611 篇'` → 恰 1 行
- old_str：`## 1. A1-A6 内容篇数 = 611 篇`
- new_str：`## 1. A1-A6 内容篇数 = 615 篇`

**E3.2（对应 T12）**
- 预检：`Select-String -Path docs\00-导读\统计口径说明.md -Pattern 'docs/02-人物深度分析 \| 211'` → 恰 1 行
- old_str：`| A3 人物分析 | docs/02-人物深度分析 | 211 |`
- new_str：`| A3 人物分析 | docs/02-人物深度分析 | 215 |`

**E3.3（对应 T13，本批新发现的口径源内部矛盾）**
- 预检：`Select-String -Path docs\00-导读\统计口径说明.md -Pattern '文件数 = 86（含'` → 恰 1 行
- old_str：
  ```text
  **算法**：`site/data/` 目录**顶层** `.html` 文件数 = 86（含 `-view` 3D 视图页与内部模板 `_shell.html`）。
  ```
- new_str：
  ```text
  **算法**：`site/data/` 目录**顶层** `.html` 文件数 = 87（含 `-view` 3D 视图页与内部模板壳 `_shell.html`）；对外宣传口径「可视化页 86」= 87 减去 `_shell.html`（与 CHANGELOG 头部 W459 口径块一致）。
  ```

**E3.4（对应 T14）**
- 预检：`Select-String -Path docs\00-导读\统计口径说明.md -Pattern '强制 README 声明'` → 恰 1 行
- old_str：
  ```text
  **校验**：`scripts/verify_delivery.py` 强制 README 声明 `共 611 篇` 与真实计数一致，漂移即 FAIL。
  ```
- new_str：
  ```text
  **校验**：`scripts/verify_delivery.py` 强制「六板块目录顶层 `.md` 磁盘计数 == README『共 N 篇』声明」，漂移即 FAIL；当前 N=615（W505 起，A3 追加 4 篇方向二深化文档）。
  ```

**E3.5（对应 T15）**
- 预检：`Select-String -Path docs\00-导读\统计口径说明.md -Pattern '（611 / 209 强制校验）'` → 恰 1 行
- old_str：
  ```text
  3. 发布前运行 `scripts/verify_delivery.py`（611 / 209 强制校验）与 `scripts/lint_links.py --internal`。
  ```
- new_str：
  ```text
  3. 发布前运行 `scripts/verify_delivery.py`（A1-A6 磁盘==README 声明 + A4==209 强制校验）与 `scripts/lint_links.py --internal`。
  ```

**E3.6（对应 T16）**
- 预检：`Select-String -Path docs\00-导读\统计口径说明.md -Pattern '^4\. 历史误值'` → 恰 1 行；`Select-String -Path docs\00-导读\统计口径说明.md -Pattern '^5\. '` → 0 行
- old_str：

  ```text
  4. 历史误值（首页 625 / 80 等）已在 W450 统一为 611 / 86 / 55；如再发现不一致，按本文件口径修正。
  ```

- new_str：

  ```text
  4. 历史误值（首页 625 / 80 等）已于 W450 统一修正；该次修正后所立数值再次漂移的根因与处置见第 5 条。如再发现不一致，按本文件口径修正。
  5. 数字修正溯源：W505（commit cd6d7b8）向 `docs/02-人物深度分析/` 追加 4 篇方向二深化文档，A1-A6 由 611 变为 615；当时仅 README 同步声明值，其余元文档漏更，W514 统一校正。今后任何板块增删文档，按第 2 条规则先改本文件再同步引用方。
  ```

- 断言：同文件 `'由 611 变为 615'` = 1；`('611' 命中行数) == ('变为 615' 命中行数)`（即全文每个含 611 的行都在溯源句内）；`'^5\. 数字修正溯源'` = 1。

### F4 docs/00-导读/文档规范.md（1 处）

**E4.1（对应 T17，§11.4 核对清单 A1-A6 行）**
- 预检：`Select-String -Path docs\00-导读\文档规范.md -Pattern '611==611'` → 恰 1 行
- old_str：`A1-A6 计数 611==611`
- new_str：`A1-A6 磁盘计数==README 声明（当前 615==615）`
- 保护约束：所在表格行的其余内容（含「209 篇」相关表述）一个字符不动。
- 断言：同文件 `'611==611'` = 0 且 `'615==615'` = 1；随后 `py scripts/verify_delivery.py` 中 EXPECT_A4 项仍 GREEN。

### F5 docs/00-导读/项目说明.md（1 处）

**E5.1（对应 T18，A3 板块计数）**
- 预检：`Select-String -Path docs\00-导读\项目说明.md -Pattern '人物深化 211 篇'` → 恰 1 行
- old_str：`A3 人物深化 211 篇·含心理学三视角`
- new_str：`A3 人物深化 215 篇·含心理学三视角`
- 保护约束：同一行的 `A4 主题专题 209 篇` 为门禁 EXPECT_A4 扫描目标字面量，禁改。
- 断言：同文件 `'人物深化 211'` = 0；`'人物深化 215'` = 1；`'主题专题 209 篇'` ≥ 1。

### F6 六文档同步组（收尾编排 S1→S6，顺序不可调换）

> 编排依据 docs/00-导读/文档规范.md §11.4 每批同步清单：核心 2 手工（S1/S2），辅助 4 走 bump_version.py（S3），页脚 4 中 dukou-engine 手工 + 其余 3 页随 bump 自动更新（S3/S4），旁文档手工（S5），索引再生成收尾（S6）。

**S1 CHANGELOG.md（两步）**

S1a 编号规则上限同步（门禁 #17 要求「CHANGELOG 编号规则段上限 == 最新 W 段」）：
- 预检：`Select-String -Path CHANGELOG.md -Pattern 'W001-W513'` → 恰 1 行
- old_str：`（W001-W513）`　new_str：`（W001-W514）`
- 断言：替换后 `'W001-W513'` = 0 且 `'W001-W514'` ≥ 1。

S1b 新版段插入（单锚点单次插入 + 双存在断言——防「吞相邻版段」历史事故）：
- 锚点预检：`Select-String -Path CHANGELOG.md -Pattern '^### v2\.3\.112（2026-08-25）：W513 归档二级归档（方案 A）— CHANGELOG-ARCHIVE W001-W399 下移 tier2$'` → 恰 1 行
- 在该标题行之前插入以下整块（块尾保留一个空行）：

  ~~~text
  ### v2.3.113（2026-08-25）：W514 治理文档口径修复 — 五元文档数字校正与门禁清单补录

  > 方案档：docs/superpowers/plans/2026-08-25-w514-governance-doc-consistency-fix.md

  - **来源**：W505（commit cd6d7b8）向 docs/02 追加 4 篇方向二深化文档，磁盘计数 611→615、A3 211→215、CSP 覆盖页 1173→1189；README 已同步而其余元文档漏更，且统计口径说明 §2 与 CHANGELOG W459 口径块自相矛盾（87 vs「86 含 _shell」）。
  - **执行**：五元文档共 18 处单点替换（新Agent启动Prompt ×4、AGENTS ×6、统计口径说明 ×6、文档规范 ×1、项目说明 ×1）+ 六文档同步组 S1-S6；AGENTS §4.2 补录第 21 门禁 check_dynamic_links.py（动态链接）与第 22 门禁 check_governance_docs.py（治理文档维护契约）登记。
  - **验证**：verify_delivery.py 全绿；陈旧模式全仓扫描 0 残留（方案档 §4 表 A2）；保护位反向抽查通过（方案档 §0.3）；generate_csp.py --check 0 漂移。
  - **状态**：已完成（2026-08-25）。
  ~~~

- 结构断言：`'^### v2\.3\.113'` = 1；`'^### v2\.3\.112'` 仍 = 1；v2.3.113 标题行号 < v2.3.112 标题行号（两次 Select-String 取 LineNumber 比较）。

**S2 交接文档.md（四处 J1-J4，同文件严格串行 J1→J2→J3→J4）**

J1 最后更新行头部插入：
- 预检：`Select-String -Path 交接文档.md -Pattern '^> 最后更新：'` → 恰 1 行
- old_str：`> 最后更新：`
- new_str：`> 最后更新：2026-08-25（v2.3.113 W514 治理文档口径修复：五元文档数字校正 611→615 · A3 211→215 · CSP 措辞改当批现测 · AGENTS §4.2 补录第 21/22 门禁登记 · 统计口径说明补根因溯源）·`
- 附加规则：插入后若该行批次条目总数 > 3，从行尾删除最旧条目直至 ≤ 3（只删旧不删新；测量：对该行 `-Pattern '2026-08-\d\d（v2\.3\.'` 计数 ≤ 3）。

J2 当前 HEAD 尾行替换（零、当前阻塞 小节末）：
- 预检：`Select-String -Path 交接文档.md -Pattern '当前 HEAD = v2\.3\.112 W513（归档二级归档'` → 恰 1 行
- old_str：`当前 HEAD = v2.3.112 W513（归档二级归档·方案 A：CHANGELOG-ARCHIVE W001-W399 下移 tier2·详见 CHANGELOG）。`
- new_str：`当前 HEAD = v2.3.113 W514（治理文档口径修复·五元文档数字校正 + 第 21/22 门禁补录登记·详见 CHANGELOG）。`
- 断言：`'当前 HEAD = v2\.3\.112'` = 0；`'当前 HEAD = v2\.3\.113 W514'` = 1。

J3 进度链头部插入（一、当前进度 大链 newest-first 自左向右）：
- 预检：`Select-String -Path 交接文档.md -Pattern '^## 一、当前进度（'` → 恰 1 行
- old_str：`## 一、当前进度（`
- new_str：`## 一、当前进度（v2.3.113 W514 治理文档口径修复（五元文档数字校正 + 第 21/22 门禁补录登记） + `
- 断言：插入后原链首节仍在且位于新节之后：`'（v2\.3\.112 W513 归档二级归档'` = 1。

J4 新增 W514 要点 bullet（插于既有 W513 bullet 之前）：
- 预检：`Select-String -Path 交接文档.md -Pattern '^- \*\*v2\.3\.112 W513 归档二级归档·方案 A（2026-08-25）\*\*'` → 恰 1 行
- 在该行之前插入：

  ~~~text
  - **v2.3.113 W514 治理文档口径修复（2026-08-25）**：五元文档数字校正（A1-A6 611→615 · A3 211→215 · CSP 措辞改当批现测）；AGENTS §4.2 补录第 21 门禁 check_dynamic_links.py 与第 22 门禁 check_governance_docs.py 登记；统计口径说明 §6 增数字修正溯源（根因 W505 cd6d7b8）；方案档 docs/superpowers/plans/2026-08-25-w514-governance-doc-consistency-fix.md。
  ~~~

- 断言：`'^- \*\*v2\.3\.113 W514'` = 1；原 W513 bullet 仍 = 1；W514 bullet 行号 < W513 bullet 行号。

**S3 bump_version.py 辅助四件套（README / STRUCTURE / 项目说明版本行 / scripts/output/file-index.md；site/index.html、site/cross-time-danmaku.html、site/tag-cloud.html 三页页脚随之自动更新）**

- 执行命令（Windows 必用 py 启动器——python 可能命中商店占位 stub，exit 9009）：

  ```bash
  py scripts/bump_version.py --version v2.3.113 --w W514 --note "治理文档口径修复" --desc "W514 治理文档口径修复"
  ```

- 跑完必做净化三查（AGENTS §4.3 已知坑）：
  - K1 file-index 历史段零污染：`git diff --numstat -- scripts/output/file-index.md` 输出的 deletions 列必须 = 0；若 > 0 → `git restore -- scripts/output/file-index.md` 后改为仅在最新段顶部追加一行 W514 条目（Python open(encoding='utf-8') 写，禁 Set-Content）。
  - K2 prev-version 行未被追加污染：`Select-String -Path STRUCTURE.md,docs\00-导读\项目说明.md -Pattern '\+ W51[34]\('` → 必须 0 行；若命中 → 手工将该处恢复为「上一版本主描述被整体替换」的正确形态并在 §9 记录。
  - K3 README 现役指针核对：`Select-String -Path README.md -Pattern 'v2\.3\.11[23]|W51[34]'` 逐行目检——所有现役版本指针应指向 v2.3.113 / W514；历史里程碑行保持原样。

**S4 site/dukou-engine.html 页脚长链 D1（纯 HTML 文本节点，非内联脚本 → 不触发 CSP 重哈希）**

- 预检：`Select-String -Path site\dukou-engine.html -Pattern 'v2\.3\.112 W513 归档二级归档'` → 恰 1 行（L152 footer，newest-first、以 ` · ` 分隔）
- old_str：

  ```text
  佛法=AI · 缘起即算法 · v2.3.112 W513 归档二级归档（方案 A：CHANGELOG-ARCHIVE 917→150KB·W001-W399 下移 docs/archive/tier2·归档三件套 >1MB 触发规则入文档规范）
  ```

- new_str：

  ```text
  佛法=AI · 缘起即算法 · v2.3.113 W514 治理文档口径修复（五元文档数字校正 611→615·A3 211→215·AGENTS §4.2 补录第 21/22 门禁登记）· v2.3.112 W513 归档二级归档（方案 A：CHANGELOG-ARCHIVE 917→150KB·W001-W399 下移 docs/archive/tier2·归档三件套 >1MB 触发规则入文档规范）
  ```

- 断言：新节 `'v2\.3\.113 W514 治理文档口径修复'` = 1 且旧节原文仍 = 1（只插不改）；随后 `node scripts/check_js_syntax.js` 全绿不受影响。

**S5 .github/workflows/README.md 头部版本 W1**

- 背景：实测 L3 头部仍停留 v2.3.99 W500 / W450-W500（旁文档头部版本 + W 上限属文档规范 §11.4 每批同步位，此前多批漏更）。
- 预检：`Select-String -Path .github\workflows\README.md -Pattern 'W450-W500'` → 恰 1 行
- old_str：

  ```text
  → W450-W500** — 西游记解读项目（`d:\1\xiyouji\`，v2.3.99 W500）的 GitHub Actions 工作流层。
  ```

- new_str：

  ```text
  → W450-W514** — 西游记解读项目（`d:\1\xiyouji\`，v2.3.113 W514）的 GitHub Actions 工作流层。
  ```

- 断言：`'v2\.3\.113 W514'` = 1；`'W450-W500'` = 0。
- 范围注记：本批无 workflow yml 变更 → 按 §11.4 不新增里程碑行，仅更新头部版本与 W 上限。

**S6 文档索引再生成**

- 执行：`py scripts/docs_index.py`（正常静默或输出写入提示均可接受；脚本报错 → 记入 §9 并标记跳过，非阻断）。
- 断言：`Select-String -Path scripts\output\file-index.md -Pattern 'w514-governance'` ≥ 1（新增方案档被收录；若 = 0，核对脚本扫描范围后在 §9 记录原因，不阻断）。

---

## 3. 执行顺序（Phase 0-7，全程串行）

前置铁律：① 同一文件的多次编辑必须串行执行（W505 四连丢失教训）；② 禁止用 PowerShell Set-Content/Add-Content 写任何 .md（UTF-8 BOM 污染，W427 教训）——PowerShell 仅作只读检查；③ 每个编辑动作都是三拍闭环：预检（锚点恰 1）→ 替换 → 断言（新模式落位 + 旧模式清零）；④ 任一预检或断言失败 → STOP 并向用户汇报现场，禁止凭感觉重试超过 1 次。

**Phase 0 基线确认（只读，不改任何文件）**
1. `git rev-parse --short HEAD` → 期望 df0f8e1；不符 → STOP 向用户确认基线漂移。
2. `git status --porcelain` → 期望空输出（工作区干净）。
3. `Select-String -Path CHANGELOG.md,交接文档.md -Pattern 'W514'` → 期望 0 行（防撞号终检）。
4. 六板块顶层 .md 计数复核（各目录 `Get-ChildItem -File -Filter *.md`）：docs/01=100、docs/06=44、docs/02=215、docs/03=209、docs/04=34、docs/05=13；任一不符 → STOP（方案前提失效）。
5. `py scripts/verify_delivery.py` → 期望基线全绿；基线红 → STOP 先治基线。
6. 工具可用性：`node -v` 与 `git --version` 均输出版本号。

**Phase 1 五元文档单点编辑（顺序 F3→F4→F5→F1→F2；组内按 E 序号升序）**
理由：统计口径说明是口径权威源，先立标准再改引用方（F3 标题已注明）。

**Phase 2 CHANGELOG（S1a → S1b → 结构断言）**

**Phase 3 交接文档（J1 → J2 → J3 → J4，四处同文件严格串行）**

**Phase 4 辅助与站点（S3 bump → K1-K3 净化三查 → S4 D1 → S5 W1）**

**Phase 5 索引（S6）**

**Phase 6 全量验收（§4 的 A1-A5 全部执行并在 §9 留痕）**

**Phase 7 回填与汇报**
1. 本方案 §9 表格逐行 ✗→✓ 回填并附实测数字。
2. §10 追加一行变更记录。
3. `(Get-Content docs\superpowers\plans\2026-08-25-w514-governance-doc-consistency-fix.md).Count` 将最终行数记入 §9。
4. 向用户汇报 §7 三问答复情况与验收结果；未经用户明确批准不得执行 git commit / push。

## 4. 验收标准（指标=阈值(测量方法)；A1-A5 全过才算完成）

**A1 门禁全绿**
- 指标：交付门禁退出码与 FAIL 数。阈值：exit code = 0 且 FAIL = 0。
- 测量：`py scripts/verify_delivery.py`。期望输出：末项汇总 ALL GREEN/PASS。

**A2 陈旧模式清零与新模式落位（统一用 Select-String -Pattern 对单文件取命中行数）**

| # | 目标文件 | Pattern | 期望命中 |
|---|---|---|---|
| 1 | 新Agent启动Prompt.md | `611 篇\|1173 哈希` | 0 |
| 2 | 新Agent启动Prompt.md | `615 篇` | ≥2 |
| 3 | 新Agent启动Prompt.md | `py scripts/verify_delivery.py` | ≥1 |
| 4 | AGENTS.md | `共 611 篇\|人物 211` | 0 |
| 5 | AGENTS.md | `共 615 篇` | ≥1 |
| 6 | AGENTS.md | `21\. \*\*动态链接门禁` | =1 |
| 7 | AGENTS.md | `22\. \*\*治理文档维护契约` | =1 |
| 8 | AGENTS.md | `209 篇` | ≥1（EXPECT_A4 字面量在场）|
| 9 | docs/00-导读/统计口径说明.md | `= 611` | 0 |
| 10 | docs/00-导读/统计口径说明.md | `由 611 变为 615` | =1 |
| 11 | docs/00-导读/统计口径说明.md | `= 615 篇` | =1 |
| 12 | docs/00-导读/统计口径说明.md | `\| 215 \|` | =1 |
| 13 | docs/00-导读/统计口径说明.md | `87 减去` | ≥1 |
| 14 | docs/00-导读/文档规范.md | `611==611` | 0 |
| 15 | docs/00-导读/项目说明.md | `人物深化 211` | 0 |
| 16 | docs/00-导读/项目说明.md | `主题专题 209 篇` | ≥1 |
| 17 | CHANGELOG.md | `W001-W513）` | 0 |
| 18 | CHANGELOG.md | `^### v2\.3\.113（2026-08-25）：W514 治理文档口径修复` | =1 |
| 19 | 交接文档.md | `当前 HEAD = v2\.3\.112` | 0 |
| 20 | 交接文档.md | `当前 HEAD = v2\.3\.113 W514` | =1 |
| 21 | 交接文档.md | `v2\.3\.113 W514 治理文档口径修复` | ≥3（最后更新行/进度链/要点 bullet 各一）|
| 22 | site/dukou-engine.html | `v2\.3\.113 W514 治理文档口径修复` | =1 |
| 23 | site/dukou-engine.html | `917→150KB` | =1（旧节保留佐证）|
| 24 | .github/workflows/README.md | `v2\.3\.113 W514` | =1 |
| 25 | .github/workflows/README.md | `W450-W500` | 0 |

注：表内 `\|` 为 Markdown 表格转义写法，实际执行时用单竖线字符。

**A3 保护位反向抽查（历史事实不许被动到）**

| # | 位置 | Pattern | 期望 |
|---|---|---|---|
| 1 | AGENTS.md | `冻结存量 611 篇豁免` | =1（W501 时点历史事实）|
| 2 | site/dashboard.html | `CSP 1173 哈希 0 漂移` | =1（历史链节）|
| 3 | dataset/ 与 site/data/ 与 site/en/ | `git status --porcelain` 输出按三前缀过滤 | 0 条 |

**A4 改动面白名单（最小爆炸半径）**
- 测量：`git status --porcelain`。
- modified ⊆ 白名单 16 文件：新Agent启动Prompt.md、AGENTS.md、CHANGELOG.md、交接文档.md、README.md、STRUCTURE.md、docs/00-导读/项目说明.md、docs/00-导读/文档规范.md、docs/00-导读/统计口径说明.md、site/dukou-engine.html、site/index.html、site/cross-time-danmaku.html、site/tag-cloud.html、.github/workflows/README.md、scripts/output/file-index.md、docs/INDEX.md。
- untracked ⊆ {docs/superpowers/plans/2026-08-25-w514-governance-doc-consistency-fix.md}。
- 清单外任何条目 → 逐一 git diff 审查；非预期改动一律 git restore 并在 §9 记录。

**A5 CSP 零漂移**
- 指标：哈希漂移页数。阈值：= 0。
- 测量：`py scripts/generate_csp.py --check`。期望：233 页口径下 0 drift（本批零内联脚本改动，理论必然绿，仍须当批实跑留痕——W496 验收数字当批现测铁律）。

## 5. 显式裁掉项（本批不做，防 scope creep）

X1 不改任何门禁/工具脚本本体（verify_delivery.py、bump_version.py、check_*.py 一行不动，含注释）——属禁擅改清单。
X2 不触碰描述历史时点状态的表述（AGENTS frontmatter 基线「冻结存量 611 篇豁免」、CHANGELOG/file-index/页脚中 ≤v2.3.112 的所有历史段落与既有链节）。
X3 dataset/、site/data/ 数据 JSON、site/en/ 全站：0 字节差异。
X4 方案档自身不加 frontmatter 元信息块（门禁 #18 scope 仅 docs/01-06 内容文档），且全文禁用 Markdown 链接语法（防 lint_links 误报死链），路径一律反引号包裹。
X5 不在本批实施第 23 号门禁（元文档一致性自动校验）——候选另立 W515（§7 Q2）。
X6 perf-budget.json、tokens.css/system.css、动效预算相关：不动。
X7 tests/、CI workflow yml、Makefile：不动。
X8 不顺手修白名单外顺路看到的任何无关措辞。
X9 不执行 git commit / git push（须 §7 三问获批后另行授权）。
X10 不重排 CHANGELOG 既有版段、不改写任何历史版段标题与正文。

## 6. 风险登记与对策

R1 同文件并行编辑互相覆盖（W505 曾四连丢失）→ 全程串行；J1-J4 与 E 系列逐条三拍闭环。
R2 PowerShell 写 md 引入 UTF-8 BOM（W427 全库事故）→ md 只经编辑工具或 Python open(encoding='utf-8') 写入；PowerShell 仅只读。
R3 bump 三坑（file-index 历史污染 / prev-version 追加而非替换 / README 多指针）→ K1-K3 硬卡；异常即 restore + 手工修正并留痕。
R4 误伤 EXPECT_A4 字面量「209 篇」（A4_DOCS 四文件之一即可打红门禁）→ E4.1/E5.1 显式保护约束 + A2 表 #8/#16 在场断言兜底。
R5 锚点失配或多次命中 → STOP 协议：同锚点重试不超过 1 次，仍失败即汇报，禁止模糊匹配硬上。
R6 Windows 商店 python stub exit 9009 → 一律 py 启动器（并经 E1.4 固化进启动 Prompt）。
R7 CHANGELOG 插版段吞相邻版段（历史事故）→ 单锚点单次插入 + 双存在断言 + 行序断言（S1b）。
R8 node/git 缺失致语法/链接检查不可跑 → Phase 0 第 6 步预检；缺失则先解决环境再开工。

## 7. 启动前三问（xiyouji-plan-authoring 第 6 步：未获批复不得进入 Phase 0）

Q1 批次定性：是否批准「纯文档治理批」？改动面 = §4 A4 白名单 16 个存量文件 + 本方案档 1 个新增，零脚本/零数据/零站点逻辑改动。
Q2 门禁边界：元文档一致性自动校验（构想为第 23 号门禁：校验 README 声明值 vs 磁盘计数 vs 各元文档引用值三方一致）本批一并实施，还是另立 W515？推荐另立——保持本批零脚本改动、风险最小。
Q3 编号确认：本批使用 v2.3.113 / W514 是否确认？（已核 CHANGELOG 现役 max = W513，无撞号。）

## 8. 与既有方案的关系

- 进入 Phase 0 时以目录列表复核 docs/superpowers/plans/ 在途方案；若发现与本批文件集重叠者 → STOP 汇报后再定策略（撰写时点未见重叠）。
- 后续候选：W515 = 元文档一致性门禁（对「声明值 vs 磁盘值 vs 引用值」做三方校验，WARN 起步观察后再升 FAIL）。
- 本方案档自身属 A4 白名单 untracked 项，随本批一起提交。

## 9. 落地状态记录（执行者逐行回填 ✗→✓ 并附实测值）

| 阶段 | 步骤 | 状态 | 实测结果摘要 | 时间 |
|---|---|---|---|---|
| P0 | 基线六查（§3 Phase 0）| ✓ | 全绿：HEAD=df0f8e1（v2.3.112 W513）；六板块磁盘计数 {100,44,215,209,34,13}=615==README 声明；EXPECT_A4 字面量在场；py/node/git 环境就绪 | 2026-08-25 |
| P1 | F3 E3.1-E3.6 | ✓ | 统计口径说明.md 六处口径落地；新值=1∧旧值=0 断言全绿（含 86=87−_shell 注记与 §6 根因溯源 cd6d7b8）| 2026-08-25 |
| P1 | F4 E4.1 / F5 E5.1 | ✓ | 文档规范 CSP 措辞改「当批现测」+ 项目说明五元校正；断言全绿，「209 篇」字面量保护在场 | 2026-08-25 |
| P1 | F1 E1.1-E1.4 | ✓ | 启动Prompt 四处同步（含 py 启动器固化 E1.4）；断言全绿，B1 保护块未触碰 | 2026-08-25 |
| P1 | F2 E2.1-E2.6 | ✓ | AGENTS §1 五元数字校正（611→615·211→215·86 口径注明）+ §4.2 登记第 21/22 门禁 + 版本脚注 W514 条目；断言全绿 | 2026-08-25 |
| P2 | S1a/S1b + 结构断言 | ✓ | CHANGELOG 新增 v2.3.113/W514 段；双存在断言 + 行序断言（W514@L15 < W513@L24）全绿 | 2026-08-25 |
| P3 | J1-J4 | ✓ | 交接文档 HEAD 句/进度链头/里程碑 bullet/最后更新条目四处落地；「最后更新」73→3 裁剪至最近三批；断言全绿 | 2026-08-25 |
| P4 | S3 bump + K1-K3 | ✓ | bump_version.py 补齐辅助 4 文档版本行；三查净化通过（发现 file-index.md 底部错位追加块 → 移交 P5 归位处理并留痕）| 2026-08-25 |
| P4 | S4 D1 / S5 W1 | ✓ | dukou-engine.html 页脚节点 `v2\.3\.113 W514`=1 ∧ 旧值 `917→150KB`=1；workflows README 版本帽 W450-W500→W450-W514 + v2.3.99 W500→v2.3.113 W514（路径无尾反斜杠，按盘面逐字节适配）新值=1∧旧值=0 | 2026-08-25 |
| P5 | S6 索引再生成 | ✓ | docs_index.py exit 0 重建 INDEX.md（663 篇/11 板块）；file-index.md 手工归位：bump 底部空段清除 + W514 段按兄弟约定格式置顶登记 14 行（W514@L13 < W513@L32）| 2026-08-25 |
| P6 | A1-A5 验收 | ✓ | A1 verify_delivery exit 0 全绿（33 门禁，含 #21 动态链接 234 页/295 链接/0 死链、#22 治理契约 6 项、footer v2.3.113 W514）；A2 26 行扫描全绿（#4 拆为 `共 611 篇`=0 ∧ `人物 211(?!→)`=0，轨迹感知修正）；A3 保护点全绿（P2 改判 dukou `1173 哈希`=1 + dashboard.html porcelain-clean）；A4 porcelain 13 M⊆白名单 ∧ untracked={方案档}；A5 CSP 校验 exit 0（233 页 · 1189 哈希 · 漂移 0）| 2026-08-25 |
| P7 | §9/§10 回填 + 方案档总行数 | ✓ | 本表十三行 ✗→✓ 回填 + §10 追加执行行；一次性脚本 _a2_acceptance.py 已删除；方案档总行数 546（回填后实测核验）| 2026-08-25 |

## 10. 变更记录

| 日期 | 说明 |
|---|---|
| 2026-08-25 | 初稿成文：对抗性审查结论转化为可执行治理方案；待 §7 三问批复后开工 |
| 2026-08-25 | 执行完成：Phase 0-7 全部落地，验收矩阵 A1-A5 全绿（实测值见 §9）。三处计划偏差留痕——① A2#4 改轨迹感知模式 `人物 211(?!→)`（原模式误命中 W514 脚注自身的合法 X→Y 轨迹文本）；② A3#P2 保护点改判 site/dukou-engine.html L152（dashboard.html 本就未触碰且不含该字符串，属方案 §0.3 定位笔误，保护意图等价满足）；③ S5 编辑串按盘面逐字节适配（路径无尾反斜杠）+ S6 file-index.md 因 bump_version 底部错位追加而手工归位登记 |