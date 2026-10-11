<!-- 元信息块（W706）：生成来源=人工撰写（Agent 起草·scripts/_w706_vscan.py 机器扫描取数）·生成模型=GLM（ZCode 2026-10-11）·生成日期=2026-10-11·核验状态=已核验（v2 修正版：首跑踩 W523 quotePath 坑漏扫约 1100 处·加 -c core.quotePath=false 后全量重扫） -->

# v 号使用点全量盘点（W706 v2 · 方案 D 形态改造前置测绘）

> **来源**：用户方案「v 号空间元规则」（第五阶段）——方案 D（v 号降格为阶段标签·W 号承担批次编号）实施前的使用面盘点；**不盘点就改会重演 W528「页脚停 W453 脱节 74 批」**。
> **方法**：`scripts/_w706_vscan.py`（一次性·随批入库）对 git tracked 文件全量扫描 `v\d+\.\d+\.\d+` 形态，按处置域分类。扫描时点=2026-10-11（v2.3.299 现役）。
> **本文档词义**（消灭现场判断）：「历史」=W704 及更早批次的产物（CHANGELOG 历史段/归档/页脚历史链/脚注沿革/file-index 既有条目——按维护契约①只增不删）；「新增」=W705 起的条目（按新形态·决策点随本档）；「现役」=CHANGELOG 顶段三元组 ∪ 对账表现势 ∪ 各文档当前态版本行。

## 一、总量与分类（v2 修正实数）

| 类 | 文件数 | 处数 | 代表 | 处置策略 |
|---|---|---|---|---|
| A 历史段归档 | 6 | 1316 | CHANGELOG-ARCHIVE(-tier2) 852/交接文档-ARCHIVE 342/STRUCTURE-ARCHIVE 120 | **不动**（历史记录） |
| B 现役版本行 | 4 | 70 | 交接 29/项目说明 21/STRUCTURE 16（含板块建置 v0.11 W016 类=历史事实不动）/README 4 | 级联模板改 |
| C 页脚站点 | 387 | 1009 | dukou-engine 275/index 129/三页脚/EN 页脚链/site/reader 中文页 | 页脚历史链保留（边界见 §三）·新增条目 W only |
| D 脚本正则逻辑 | 37 | 137 | bump_version/bump_footer_version/jiacheck 族/_w 系一次性 | 常驻脚本同批改·一次性不动 |
| E 外部配置 | 1 | 1 | **CITATION.cff line7 `version: "2.3.299"`（无 v 前缀三段式·形态不同但即 v 号·v1 版盘点误记 0 处）** | 决策点 2（三选·倾向丙） |
| F 叙述面 | 392 | 6258 | **file-index(-archive) 4652（W↔v 双列结构=最大消费方）**+AGENTS 脚注 216+对账表版段列 80+CHANGELOG 现役 66+tests 43+superpowers 方案档+方法论 E1/E2 等引证 | file-index 见决策点 3·其余历史引证不动 |
| **合计** | **826** | **8791**（含 E） | | |

## 二、零命中确认表（扫描覆盖面实证·W707 验收可直接复用）

| 文件 | v 形态命中 | 备注 |
|---|---|---|
| `.github/workflows/ci.yml、dependency-review.yml、perf.yml、scorecard.yml` | **各 1（共 4）** | 非 0——v1 盘点未列此面；W707 须查四处版本引用形态 |
| `.github/workflows/pages.yml、security.yml、stale.yml` | 0 | |
| `pyproject.toml` / `xiyouji-agent-web/package.json` | 0 | |
| `新Agent启动Prompt.md` | 0 | |
| `CLAUDE.md` | **0** | W664「禁写会漂移的数字与现役值」设计实证 ✓ |
| `mcp-server/*.py` | 0 | |
| `CITATION.cff` | 0（v 前缀形态）/1（无前缀三段式） | E 类单列 |

## 三、file-index 拆分与边界定义（决策点 3 依据）

- **结构实测**：file-index.md 835 处 v 形态（file-index-archive 另 3817 处）；行级含 v 共 772 行，其中 W650+ 现役条目行 344。v 出现形态=头部历史归档区间括号（`W031-W087（v2.0.4-v2.0.60）`）+条目 v 副列。
- **「历史链/历史条目」边界定义**：条目 W 号 < W705 = 历史（保留双列原样）；W705 起新条目按决策点 3 所选形态。
- **决策点 3｜file-index 格式分裂**（v1 盘点未识别·用户挑刺补入）：甲=历史条目保留双列+新增 W only（承认分裂·头部说明·最小改动·**倾向**）；乙=历史也去 v 列（违维护契约①）；丙=全量重生成去 v 列（彻底但 4652 处重写+check_index_health 断言同步）。

## 四、硬耦合清单（形态改造必须同改的机器面——漏一处即 W528 型静默脱节）

1. `scripts/check_doc_sync.py`：C1/C2 正则 `v(\d+\.\d+\.\d+)` 三段（:29/31）+ **C4 近 15 提交对账须双形态兼容**（沿革期新旧段标题并存·用户挑刺补入）。
2. `scripts/verify_delivery.py`：CHANGELOG 段标题解析、README 三元组、页脚 `v%.%s W%d` 解析（第 1 门禁页脚新鲜度）、第 17 门禁编号规则段断言、第 27 门禁 CITATION 同步。
3. `scripts/batch_cascade.py`：CHANGELOG 段标题锚点、README/STRUCTURE/项目说明三模板 ver 变量、CITATION 写入——**段锚点正则须双形态兼容**（沿革期）。
4. `scripts/bump_version.py`：`--version v2.3.18` 形态 + 全文件 W001-W### 范围替换 v 段逻辑。
5. `tests/test_verify_delivery_version.py`：**语义结果须先定义**（用户挑刺补入）——`latest_version_from_changelog()` 在去 v 后返回什么（建议：返回 `(w, date)` 二元组·版本位语义移除）；`parse_footer_version()` 对 W-only 新条目返回形态；下游第 1 门禁页脚新鲜度的期望值同步。**这是 W707 最易踩的坑——先定义语义再改代码**。
6. `CITATION.cff`（E 类）：见决策点 2。
7. `scripts/output/file-index.md`：见决策点 3。
8. AGENTS 版本脚注（216 处·历史沿革链）——**保留**。
9. `.github/workflows/` 四处 v 引用（ci/dependency-review/perf/scorecard·零命中确认表实测）——W707 逐处核形态。

## 五、方案 D 实施清单草案（W707 · 三决策点拍板后执行）

- 元规则已落文档规范 §4.11（本批）：v 号=阶段标签·W 号=批次编号单调永不复用·时间点查询以 W 号为准。
- **决策点 1｜CHANGELOG 段标题形态**：**甲（用户裁定倾向）**=`### W705（date）：标题`（去 v）——配三条沿革机器面：① CHANGELOG 头部维护契约加「自 W705 起段标题去 v 号·W001-W704 保留历史形态不改写」；② C4/batch_cascade 锚点双形态兼容（硬耦合 1/3）；③ file-index 段标题同构。
- **决策点 2｜CITATION.cff version 策略**：**丙（用户裁定倾向·改选）**=`version: "W705"`（CFF version 系 free string 不强制 SemVer·W 号单调唯一可查·彻底断开与 v 号关系）——**执行前须核下游消费者**（Zenodo 等平台对 SemVer 的假设；当前仓库无自动化 CFF 消费者实证=CI 无 cff 校验 job）。甲=冻结 2.3.0（学术引用无法区分版本）；乙=2.3.705（v 号在 CITATION 内复活）均弃。
- **决策点 3｜file-index 格式分裂**：甲（倾向）=历史双列+新增 W only。
- **执行前补做（用户建议采纳·2-3 小时）**：① 零命中确认表已补（本档 §二）；② file-index 拆分已补（§三）；③ 版本函数语义定义已入硬耦合 5——三项均完成，W707 可纯机械执行。
- 验收：盘点处置策略逐条落地 + verify full + 现役面 `v2\.3\.\d{3,}` 残留=0（历史段/脚注/页脚历史链/归档豁免清单随批）。

## 六、附带确认与本档自纠记录

- **双键不单调实证**：v2.3.262（W661）列于 v2.3.261（W666）后——W659/W660 合并段（D1）与并行区间（W659-W667）所致；时间点查询以 W 号为准。
- **v1 版盘点两处失真自纠**（保真度纪律）：① git ls-files 未加 `-c core.quotePath=false`——中文路径八进制转义致 io.open 失败漏扫约 1100 处（交接文档-ARCHIVE 342/reader 中文页/对账表 80 等），总数 7679→8791——**W523 教训在盘点脚本上再现**；② E 类 CITATION 误记 0 处（无 v 前缀形态被 pattern 排除）——用户挑刺后单列。
- file-index 与页脚的 v 列/链是「历史批次→v 号」映射记录（历史属性）——方案 D 不改写历史，只断新增。
