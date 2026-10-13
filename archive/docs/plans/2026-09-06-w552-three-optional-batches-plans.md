# 三项可选改进批次计划（方案 A/B/C）

> 创建：2026-09-06（W552 批次产物）。本文档自包含：全部背景、现象描述、根因定位、执行步骤、验收标准均内嵌于正文，执行者无需回溯 W550/W551 会话或已删除的 `tmpe/` 目录即可独立执行。
>
> 批号说明：本计划文档随 W552（文档批次）入库。三个方案的执行批号执行时按「CHANGELOG 现役段 max+1」重新领取，本文标注的「建议批号 W553/W554/W555」仅为预设，以实际领取为准。
>
> 背景压缩（30 秒版）：W550 对全站 234 个 HTML 页面做了截图审查并修复五类缺陷；W551 把审查能力沉淀为两道常驻门禁（`scripts/check_chart_data.py` 静态第 24 门禁 + `scripts/check_screenshot_gates.js` 动态五类，挂 screenshot-review workflow），基线 234 页 0 FAIL。此后「结构性图表缺陷」已由机器拦截，本文三方案处理机器拦不住的剩余项。W550 审查报告精简版存于 `docs/archive/w550-shot-review/`（11 文件 420KB，含逐页判定与告警清单）。

---

## 方案 A（建议批号 W553）：低危视觉细节批次

| 项 | 值 |
|---|---|
| 优先级 | 高（三方案中唯一建议近期执行） |
| 前置依赖 | 无 |
| 预计改动 | ≤6 个 HTML 文件，≤150 行 diff |
| 预计工作量 | 1.5–2.5 小时（含 4 项 judge 视觉复核） |
| 涉及工具 | Playwright（scripts/node_modules 已装）、check_screenshot_gates.js（回归）、batch_cascade.py（登记） |

### A-1 en/text-evolution.html：移动端两幅柱状图 y 轴行标签缺失

- **现象**（W550 修复验证 J3 轮判定原文，375px 视口）：`Total Comments Distribution` 图 5 个行标签仅最底行 `Zhang Shushen` 可见，其余 4 行标签区空白；`Commentary Type Distribution (Stacked)` 图同样仅最底行有标签。
- **代码定位**（已取证）：
  - `renderCommentaryCountBar`：`const width = +svg.attr("width"); const margin = { top: 20, right: 30, bottom: 50, left: 80 };`——宽度取自 svg 属性而非容器实测。
  - `renderStackedBar`：`const width = Math.max(200, containerEl.clientWidth || 1100); const margin = { ..., left: 100 };`——取 clientWidth。
  - 两图的 svg 均无 viewBox 自适应，容器在 375px 视口下宽约 327px。
- **执行步骤**：
  1. 读两函数完整代码（`grep -n "renderCommentaryCountBar\|renderStackedBar" site/en/text-evolution.html` 定位行号），确认 y 轴标签绘制的 `.attr('x', ...)` 偏移与裁剪原因（svg 默认 overflow hidden，负 x 或超左界即不可见）。
  2. 修法（对齐 W550 Power Ranking 先例，二选一，优先 a）：
     a. CSS 滚动容器：在 `</style>` 前追加 `@media (max-width: 768px){ #commentary-count-bar, #commentary-stacked { min-width: 800px; } .chart-wrap, .chart-block { overflow-x: auto; } }`（注：`#commentary-count-bar` 已有 W550 加的同类规则，合并为一条）。
     b. 渲染改造：两函数统一改为 `const width = Math.max(760, containerEl.clientWidth || 1100)` 并配 `svg.attr('viewBox', ...)`。
  3. 移动端重截复核（命令见「验收」）。
- **验收（全部满足才算完成）**：
  - `node scripts/check_screenshot_gates.js --only text-evolution` 输出 FAIL 0；
  - Playwright 断言（一次性探针或手测）：两图 y 轴 `text` 元素各 ≥5 个，且每个 bbox 完全落在所属 svg 视口内或容器可横向滚动到达；
  - verify_delivery 全绿。

### A-2 en/intertextuality-network.html：力导向图节点标签重叠

- **现象**（pass1 G14 轮判定原文，桌面 1280）：力导向图两个标签 `Daoist Canon` 与 `Journey to the West Zaju` bbox 相交，连读成 "Daoist Canonney to the West Zaju"。
- **根因**：力导向布局随机收敛后两节点距离近，标签以节点为中心水平居中绘制，无防碰撞逻辑。
- **执行步骤**：
  1. 定位标签绘制代码：`grep -n "Daoist\|label" site/en/intertextuality-network.html`。
  2. 修法（最轻优先）：标签文本超 14 字符截断为前 12 字符 + `…`，`<title>` 子元素保留全名（hover 可见）；若截断后仍相交，对相交对中 y 值较小的标签追加 `dy=-10` 偏移。
  3. 中文镜像 `site/data/intertextuality-network.html` 同步检查（同标签可能同样相交，初审未单独报，执行时一并用验收断言检查）。
- **验收**：
  - Playwright 探针：读取力导向 svg 内全部标签 text 的 getBoundingClientRect，断言任意两两相交面积 = 0（容差 2px）；
  - `node scripts/check_screenshot_gates.js --only intertextuality` FAIL 0；
  - verify_delivery 全绿。

### A-3 en/monster-female-network.html：时间线刻度文案水平相连

- **现象**（pass1 G14 轮判定原文）：时间线 x 轴上 Ch.55 刻度文案 `Destroyed by the Pleiades Star Lord` 与 Ch.59 刻度文案 `Destroyed by Zhu Bajie` 首尾相连，无法区分归属。
- **修法**：刻度文案拆两行 tspan（第一行 `Ch.55`，第二行结局短文案 ≤16 字符；如 `Destroyed by the Pleiades Star Lord` 缩为 `Pleiades Star Lord`），或每条文案后追加固定间距。
- **执行步骤**：定位时间线刻度绘制代码 `grep -n "Pleiades\|tick\|时间线" site/en/monster-female-network.html`；中文镜像 `site/data/monster-female-network.html` 同步检查（该页时间线为中文文案，可能无此问题，验收断言跑过即可）。
- **验收**：Playwright 探针断言时间线区内任意相邻刻度 text 的 bbox 水平 gap ≥ 8px；check_screenshot_gates --only monster-female FAIL 0。

### A-4 en/social-media.html：Workplace Fit 图行标签残余裁切

- **现象**（W551 J3 轮判定原文）：最长行标签渲染为 `ite Dragon Horse`（`White Dragon Horse` 词首被图表左缘切掉）。W550 已将 `renderFitChart` 的 `margin.left` 从 130 调至 150，未彻底解决。
- **修法**：渲染前量测自适应——在 `renderFitChart` 开头用临时 text 元素 `canvas.measureText` 或 `d3.select` 量出最长标签宽，`margin.left = Math.max(150, maxLabelWidth + 20)`。
- **验收**：全部行标 bbox.left ≥ svg 左缘且右端完整（bbox.width ≤ margin.left - 8）；check_screenshot_gates --only social-media FAIL 0。

### 方案 A 收尾（四项通用）

1. `python scripts/generate_csp.py && python scripts/generate_csp.py --check`（改内联脚本/样式后必跑，0 漂移）。
2. `python scripts/verify_delivery.py` 核心全绿（含第 24 门禁）。
3. 四项各出修复前后移动端/桌面截图对比（重截 `--only` 对应页），judge 复核每项验收断言通过。
4. batch_cascade 登记（desc 建议「低危视觉细节批次」，file_index_rows 列 4 文件 + 探针脚本）。
5. 提交：`git add -A && git commit -F <msg.txt> && git push origin main`；推送后 `gh run list` 确认 5 workflow 全绿。

**回滚**：单项 `git checkout -- <file>` 即可，无数据/结构变更。

---

## 方案 B（建议批号 W554）：全站全分辨率人工复审

| 项 | 值 |
|---|---|
| 优先级 | 低（仅发布级打磨/重要展示前执行） |
| 前置依赖 | 建议在方案 A 完成后执行（避免复审期间页面变更） |
| 成本（最大项，诚实预估） | judge token 消耗约 2400–5800 万（按 W550 实测单组 19–85 万 token 外推）；墙钟约 6–10 小时（3 并发受限） |
| 产出 | `scripts/output/review-pass3/verdicts.jsonl`（入库，<500KB）+ FAIL 修复提交 |

### 范围（精确定义）

- **复审对象**：`site/` 下全部 HTML 共 234 页，**排除 2 个模板壳**（`_template.html`、`data/_shell.html`），实际 **232 页**；仅桌面视口 1280×800。
- **排除移动端整体复审的依据**：W550 已对全部 234 页移动端做过程序化断言（textscan 溢出 0/134、W551 后 gates G3 常驻），且移动端差异主要是响应式缩放而非新内容。
- **不做抽样、不做豁免**：232 页全量——本方案的存在意义就是补「人眼级 100% 覆盖」，抽样会重蹈 W550 覆盖缝问题。

### 执行步骤（可照抄）

1. **临时目录**：仓库根建 `.review-tmp/`（加入 `.gitignore`，结束删除）。
2. **采集**：新写 `scripts/_w554_shots.py`（可参照 `git show 0099f85:scripts/_tmpe_shots.js` 思路改 Python/Playwright 或直接 node）：仅 desktop、fullPage、输出 `.review-tmp/shots/<rel>.png`，file:// 直开、load + 1.5s、拦截 http(s) 请求。
3. **切片**：1280×1600、步进 1500（100px 重叠）→ `.review-tmp/slices/`；≤1600px 高的页面不切（整页一张）。按 W550 实测比例预估 **约 1150 张切片**。
4. **分组**：每组 ≤12 张切片、单页切片不跨组 → **约 96–100 组**；组清单写 `scripts/output/review-pass3/groups.json`。
5. **审查**：judge 代理（subagent_type=judge）逐组审读，3 并发（平台实测并发上限 3，超发会 `concurrency limit exceeded` 需重试）。每个 judge 的提示词必须包含：
   - 判据（8 条）：① 空白容器/缺图；② 裸 HTML 无样式；③ 明显错位重叠；④ 内容横向截断；⑤ 可读报错文字（undefined/NaN/加载失败/No matches）；⑥ 标签被容器裁切；⑦ 标签互相重叠连读；⑧ 可见文案与图形类型矛盾（如标题饼图实为方块）。
   - 明确「格内文字过小不算问题」（若用联络表）或直接用全分辨率切片（本方案用切片，无此问题）。
   - 输出格式：每页一行 JSONL `{"page":"<rel>","verdict":"pass|warn|fail","issues":["<切片号+现象>"]}`。
6. **汇总**：合并各组 JSONL → `scripts/output/review-pass3/verdicts.jsonl`；统计 pass/warn/fail 计数。
7. **处置**：FAIL 逐项修复（当批修复或登记后续 W 批次，逐项走 A 方案的「修→判→重截」流程）；WARN 汇总成表人工裁决（修/不改/登记）。
8. **清理**：删除 `.review-tmp/`；`.gitignore` 移除该行。

### 验收（可机判）

- `wc -l scripts/output/review-pass3/verdicts.jsonl` == 232（覆盖率 100%，缺一行即未完成）；
- 每行 verdict ∈ {pass, warn, fail} 且 issues 数组存在（格式完整性）；
- 全部 FAIL 修复后：`node scripts/check_screenshot_gates.js` FAIL 0 + verify_delivery 核心全绿；
- WARN 清单每条有「修复/不修（原因）」裁决记录（写在 verdicts 同目录 `warn-disposition.md`）。

### 明确非目标

- 不审数据语义正确性（数字与史实对错归方案 C）；
- 不审交互态（点击/筛选/hover）；
- 不审 http 在线模式与非 Chromium 浏览器。

---

## 方案 C（建议批号 W555）：数据内容正确性审计

| 项 | 值 |
|---|---|
| 优先级 | 中（独立维度，与 A/B 无依赖；建议在内容定稿/对外分享前执行） |
| 分层 | L1 站内自洽（机器全量）→ L2 站-dataset 对账（机器全量）→ L3 语义正确性（LLM+人工抽样） |
| 预计工作量 | L1+L2 脚本开发与跑批 3–4 小时；L3 约 260 个判读单元，LLM token 300–600 万 + 人工复核 26 项 |

### L1 站内自洽（新脚本 `scripts/check_content_consistency.py`，候选第 25 门禁）

- **动机**：W550 实证三类同页数字矛盾均可被「同实体+不同值」规则覆盖——① `data/relationships.html` 正文「89 回共现」vs 图例「(88)」；② `en/narratology-13d-network.html` 同页 13/16/17 维度口径混用；③ `six-senses` 案例数声明 5 vs 桑基链实际 4。
- **规则（全部机器可判）**：
  1. 力导向图注模式 `(\d+)\s*(?:个?节点|nodes)` 与 `(\d+)\s*(?:条?关联?边|edges|关联边)` vs 页面 JS 中 links 数组字面长度；
  2. 桑基图注 `(\d+)\s*(?:nodes|节点)` vs links 去重节点数；
  3. 同一页面同一「实体对+计数词」出现 ≥2 个不同数字（如 `唐僧-孙悟空…89 回` 与 `唐僧-孙悟空 (88)`）——提取对 `(实体对, 数字)` 按页分组，同对多值即报。
- **验收**：`--self-test` 对 W550 三个已知矛盾样本回放全部命中、好样本零误报；全站跑批产出矛盾清单（预期非零，逐条人工裁决：改文案/改数据/登记豁免）。裁决清零后可挂 verify_delivery 第 25 门禁（挂载经用户确认 + py_compile + 全量跑通，同 W551 先例）。

### L2 站-dataset 对账（同脚本 `--dataset` 模式）

- **范围**：24 个含 EMBEDDED_DATA 的 sankey/canvas 页 + 全部含 KPI 数字卡页面。
- **比对**：页面 EMBEDDED 关键字段 vs `dataset/glossary.json`（术语与规范词）与 `scripts/output/data/*.json`（同源数据若存在）的对应字段，逐字段相等断言；抽样密度：每页 ≥3 个数值/枚举字段。
- **验收**：漂移清单每条有「改站/改 dataset/豁免」三选一裁决记录。

### L3 语义正确性（LLM 判读 + 人工抽检）

- **L3-a 英译忠实度**：对象 = `site/en/essay-*.html` 44 篇 + `site/en/character-{wukong,bajie,shaseng,tangseng,bailongma}.html` 5 篇，共 49 页；对照源 = `docs/06-个人随笔/`（essay 对应目录以各页 `source-note` 链接为准，页面内已写明 `docs/` 相对路径）与 `docs/02-人物深度分析/`。**分层抽样 20% = 10 篇**（essay 按文件名字母序等距取 8 + character 取 2）；判读单元 = 段落对（中文段 vs 英译段），预计约 150 对。判读四值：一致 / 漏译 / 增译 / 误译，LLM 逐对输出 + 引用两侧原文；人工复核其中 10%（15 对）。
- **L3-b 史实/原著口径**：三类硬清单——① `en/81-hardships.html` 八十一难清单 81 行逐行对照 `dataset/text-search.json`（行名须能命中原文关键词）；② 全站时间线年代断言（如「公元4世纪-20世纪」「1974-1996」）与 `docs/` 对应专题文档一致；③ KPI 声明（615 篇/86 页/55 条/100 回）与 AGENTS §1 口径一致。预计约 111 项。
- **产出**：审计报告 `docs/superpowers/plans/2026-09-XX-w555-content-audit-report.md`（PASS/WARN/FAIL 三级清单 + 覆盖率数字）；FAIL 转修复批次。
- **验收**：L3-a 覆盖 10/49 篇且含 150 段判读记录；L3-b 覆盖 111/111 项；双模型（两个不同 LLM 会话）判读一致率 ≥90%，低于则对不一致项扩人工复核至 100%；人工抽检 15 对与 LLM 判读分歧率 >20% 时全量升级人工。

### 明确非目标

- 不改版式/视觉（归方案 A）；
- 不建新门禁（L1 是否挂第 25 门禁在裁决清零后单独决定）；
- 不覆盖 `docs/` 本身的史实考据质量（只审「站与源一致」）。

---

## 执行顺序建议与依赖图

```
方案 A（W553，1.5-2.5h）──独立可执行，建议最先
方案 B（W554，6-10h+高 token）──依赖 A 完成（避免复审期间页面变更）
方案 C（W555，3-4h + 判读）──与 A/B 无依赖，任意时间可独立执行
```

三方案均为**可选**，无强制顺序；不做任何一项不影响当前站点的门禁健康状态（verify_delivery 24 门禁 + CI 动态五类门禁全绿基线）。
