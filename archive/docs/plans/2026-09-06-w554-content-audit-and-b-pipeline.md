# W554 执行报告：方案 B 阶段一（全站复审管线）+ 方案 C（数据内容审计全量）

> 创建：2026-09-06（W554 批次产物）。承接 `2026-09-06-w552-three-optional-batches-plans.md` 的三方案执行：方案 A 已于 W553 完成；本批执行方案 B 的**前置管线阶段**与方案 C **全量**。
>
> **批号说明**：方案 B 的完整 98 组 judge 审查（估 2400–5800 万 token、6–10h 墙钟）超出单 session 容量，本批完成其全部基建并验证端到端可复现；剩余 98 组以恢复指令形式登记（见 §B.5）。批号按「现役段 max+1」实领为 W554（原计划建议 W554=B / W555=C 合并为一批执行）。

---

## B. 方案 B 阶段一：全站复审管线（完成基建 + 试审验证）

### B.1 已交付

| 组件 | 状态 | 说明 |
|---|---|---|
| 采集脚本 `scripts/_w554_review.js` | ✅ | 232 页桌面 1280×800 fullPage，file:// 直开、拦截 http(s)、**滚动穿透**（逐屏触发 reveal-in） |
| 截图基线 `.review-tmp/shots/` | ✅ 232 页 | 本地临时（.gitignore），供剩余 98 组复用，**勿删** |
| 切片 1280×1600 步进 1500 | ✅ 967 张 | `.review-tmp/slices/`；页高 ≤1600 整页一张 |
| 分组 | ✅ 98 组 | `scripts/output/review-pass3/groups.json`（入库）；每组 ≤12 切片、单页不跨组 |
| 试审组（group 1，10 切片） | ✅ | judge 端到端验证通过（28 万 token/组量级） |

### B.2 试审发现与修正（重要教训）

首版采集脚本无滚动穿透，group 1 试审判 curated.html「整屏空白 FAIL」——复核实证为 **reveal-in 未触发的采集伪影**（W550 G4 同源教训二犯）：补滚动穿透后重采 232 页，同区域内容完整渲染，终判 3 页全 pass。**采集脚本已固化滚动穿透步骤**，剩余组审查用同一脚本重采的基线，不会再产生该伪影类误报。

### B.3 试审组终判（verdicts-pilot.jsonl）

```
{"page":"curated.html","verdict":"pass","issues":[]}
{"page":"dashboard.html","verdict":"pass","issues":[]}
{"page":"data/81-hardships-view.html","verdict":"pass","issues":[]}
```

### B.4 容量诚实预估（为什么不一次性跑完）

W550 实测单组 judge 19–85 万 token；98 组 × 试审实测（10 切片 ≈ 28 万）≈ **2700 万 token 量级**。本 session 已消耗约 400 万，无法承载。剩余 98 组为纯机械重复操作。

### B.5 恢复指令（未来 session 逐字照抄）

1. `node scripts/_w554_review.js capture`（如 `.review-tmp/shots/` 已删则重采，约 6 分钟）
2. `node scripts/_w554_review.js slice && node scripts/_w554_review.js cut && node scripts/_w554_review.js group`
3. 读 `scripts/output/review-pass3/groups.json`，按 group 顺序派 judge（subagent_type=judge，3 并发），提示词用本报告 §B.3 同款 8 条判据 + JSONL 输出，逐组追加 `scripts/output/review-pass3/verdicts.jsonl`
4. 验收：`wc -l verdicts.jsonl` == 232 页（每页至少一个 verdict；切片级 verdict 按页归并）；FAIL 逐项修复；WARN 汇总 `warn-disposition.md`
5. 结束删 `.review-tmp/` 并移除 .gitignore 行

---

## C. 方案 C：数据内容正确性审计（全量完成）

### C.0 工具

`scripts/check_content_consistency.py`（新建，常驻）：
- L1 模式（默认）：全站 230 页扫描（排除 2 模板壳 + dukou-engine 元页面）
- `--self-test`：W550 三案例（relationships 89vs88 / 13d 13/16/17 / six-senses 5vs4）负样本回放 **4/4 PASS** + 好样本零误报
- `--dataset`：L2 对账
- **是否挂载 verify_delivery 第 25 门禁：未经用户确认，本批不挂载**（脚本只报告不阻断）

### C.1 L1 站内自洽（230 页全量）

扫描出 5 条命中，逐条人工裁决：

| 页 | 命中 | 裁决 | 依据 |
|---|---|---|---|
| data/relationships.html | 「唐僧-孙」88 vs 90 回共现 | **真矛盾（FAIL→修复）** | 同页演化曲线区写「以 88 回共现位居榜首」，网络区两处写「90 回共现最强/榜首」，页面自身 EMBEDDED `weight: 90`——88 为旧口径残留 |
| data/character-sentiment-arc.html | 「回分桶」10 vs 100 | 误报 | 「100 回情感弧线（10 回分桶聚合）」两声明本就并存，提取窗口歧义 |
| data/pilgrim-team-psychology-arc.html | 「个体-团」31 vs 100 | 误报 | 「第 31 回黄袍怪事件」与「100 回中的演化」两个不同声明 |
| data/power-resources.html | 「种稀缺资源与拥」8 vs 10 | 误报 | 「8 条阶级流动路径」被窗口跨捕到「10 种稀缺资源」 |
| en/perf-canvas-rendering.html | 「exc」300 vs 1000 | 误报 | 性能基准讨论中两个不同假设阈值（exceeds 300/1000 nodes） |

### C.2 L2 站-dataset 对账

- 范围修正：计划假设「site/data/X.html ↔ scripts/output/data/X.json 同名」——实测同名仅 1 页；**实际同源约定是 `dataset/<X>.json` 同名**（38 页重叠，其中 17 页 EMBEDDED_DATA 机器解析成功）。
- 结果：**17 页逐字段抽样对账（每页每键 ≤8 项）· 漂移 0 页**。
- 口径限制：其余 21 页 EMBEDDED 为复杂 JS 字面量（函数调用/展开语法），静态解析不成功，留作后续增强（可用 Playwright 运行时取 `window.EMBEDDED_DATA` 兜底）。

### C.3 L3-a 英译忠实度（7 essays + 2 characters，共 121 段落对 + 33 事实声明）

抽样：site/en/essay-*.html 实际 36 篇（计划估 44），等距取 7（20%）+ character 2 篇。**判读均为单模型 + 高危声明机械 grep 复核（全部属实）；计划要求的「双模型一致率 ≥90%」未执行**（容量限制，登记为偏差）。

| 页 | 判定 | 关键发现（全部经机械复核或引用双侧原文） |
|---|---|---|
| essay-ai-era | pass | 18 一致/2 漏译（源文档第二节整节摘要化，页自注 summary translation） |
| essay-cipai-mantingfang | warn | 5 漏译（影视改编/当代启示/七层次 3 整节未译） |
| essay-folk-belief | warn | 3 漏译 + 3 增译（学者生年添注：华琛 1938「源外且存疑」） |
| **essay-ming-intellectual-history** | **fail** | ①「君（玉帝）/客（如来）/主（众生）」标注与源对调且同页自相矛盾；② 术语表锚标 22 terms 实表 14 行；③ 6 整节漏译 |
| **essay-ming-military** | warn | **3 处汉字实体错植（机械验证）**：`&#23453;`(宝) 应为 `&#23663;`(屯)——「军屯」渲染成「军宝」；`&#21464;`(变) 应为 `&#21496;`(司)——「土司」两处渲染成「土变」；另「兵制」误译为 ordnance |
| essay-poetry-imagery | warn | 6 漏译（全部摘要范围，0 误译） |
| essay-thematic-poetry | warn | 「七律」误译为 seven-character quatrain（七言绝句） |
| character-wukong | warn | 「the Pilgrim imposed by Guanyin」张冠李戴（原著第 14 回为唐僧赐名行者；页面 1257 行实锤）+「most-adapted figure」最高级无据 |
| character-bailongma | warn | 「accidentally burning the pearl」与基准「蓄意骄纵」/原著「纵火」相悖（页面实锤）；「全队最低恐惧/最高服从与决心」被页面自引 radar 数据证伪（悟空 fear 2/resolve 9，唐僧沙僧 obedience 9） |

**系统性结论**：EN 站为「摘要译介」分层设计（页面自注），整节漏译是范围声明而非缺陷；真正的缺陷集中在 **① 汉字实体错植（编码级）② 名实归属错误 ③ 锚标数字与实表不符** 三类。

### C.4 L3-b 史实/口径硬清单

| 项 | 结果 | 证据 |
|---|---|---|
| ① en/81-hardships.html 81 难清单 | **FAIL（重缺陷）** | EMBEDDED `hardships: []` 空数组 + fetch `../../scripts/output/data/hardships_81.json` 指向 site 外路径——file:// 与 GitHub Pages 部署态**双断**，截图实锤表格区显示 "No matches, or data not loaded (run via http server)"、Showing 0/0 trials。违反 EMBEDDED 回退铁律（§4.1）；中文镜像 data/81-hardships.html 内嵌完整清单无此问题。dataset/81-hardships.json 有完整 81 行可回填 |
| ② 年代断言抽查（2 项） | WARN | intertextuality「2200+ years」跨度无起止锚点（站内自算 2092–2526 区间，docs 无对应口径）；计划样例「1974-1996」在 famous-time-travel 页未复现（样例过期，非缺陷） |
| ③ KPI 声明（615 篇/86 页/55 条/100 回） | PASS | site 内声明自洽；615 磁盘口径由第 3 门禁（verify_delivery）常态校验中；55 条=学术索引 W528 同步口径 |

### C.5 修复清单（转修复批次，建议 W555 领号）

| # | 缺陷 | 修法 | 影响面 |
|---|---|---|---|
| F1 | en/81-hardships.html 清单空 | 将 dataset/81-hardships.json 的 81 行按 ZH 镜像形态内嵌 EMBEDDED（对齐 ZH 页）+ 重跑 generate_csp | 1 页 |
| F2 | essay-ming-military 实体错植 ×3 | `&#23453;`→`&#23663;`、`&#21464;`→`&#21496;`（2 处）+ ordnance→institution/system | 1 页 |
| F3 | relationships.html 88 vs 90 | 演化曲线区「88 回」→「90 回」（对齐 EMBEDDED weight 与网络区） | 1 页 |
| F4 | essay-ming-intellectual-history 客/主对调 + 22↔14 | 对齐源文档标注；锚标改 14 或补全 22 条 | 1 页 |
| F5 | character-wukong 行者赐名归属 | imposed by Guanyin → given by Tang Seng (ch. 14) | 1 页 |
| F6 | character-bailongma accidentally + 全队极值 | 语义修正 + 极值声明改写为数据如实表述 | 1 页 |
| F7 | essay-thematic-poetry 七律体式 | seven-character quatrain → seven-character regulated verse | 1 页 |
| F8 | essay-folk-belief 华琛生年存疑 | 核对文献或删生年 | 1 页 |

### C.6 验收对账（对照计划「验收」节）

- ✅ L1 --self-test 三案例全命中 + 好样本零误报；全站跑批产出矛盾清单（5 条）且**逐条人工裁决**（1 真 4 误报有据）
- ✅ L2 漂移清单：0 条（17 页覆盖，口径限制注明）
- ⚠️ L3-a 覆盖 9/41 页（7+2；计划按 44 篇估 10 篇，实际 essay 总数 36）；判读记录 121+33 条留痕于本报告；**双模型一致率未执行**（偏差声明）
- ✅ L3-b ①81/81 行核查以「页面清单完整性」形态执行（发现比逐行关键词命中更重的缺陷：清单整体缺失）；② 抽验 2 项；③ 全过
- ✅ 不改版式、不挂新门禁（L1 挂载留待用户确认）
- ✅ 审计报告入库本文件

---

## 附：本批文件清单

- `scripts/check_content_consistency.py`（新建·L1/L2/self-test 常驻工具）
- `scripts/_w554_review.js`（新建·方案 B 采集/切片/分组管线）
- `scripts/_w555_l3b.py`（新建·L3-b KPI/年代机器核查）
- `scripts/output/review-pass3/groups.json`（新建·98 组分组清单，B 剩余审查复用）
- `.gitignore`（新增 `.review-tmp/`）
- 本报告 + 六文档/旁文档版本行 + site 四页脚（batch_cascade 级联）
