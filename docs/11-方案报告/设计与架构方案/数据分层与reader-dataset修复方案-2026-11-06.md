# 数据分层与 reader/dataset 修复方案（2026-11-06）

> **版本**：V1.0
> **日期**：2026-11-06
> **来源**：用户指令「针对 site/reader 5 类、dataset 8 类生成修复方案；对比 site/data/json 与 dataset 是否需同步或迁移；复盘最初设计问题、同类写法与防复发」
> **状态**：方案（只读审计后成文·未施工）
> **读者**：项目维护者、后续接手 Agent

---

## 0. 结论先行

1. **reader 的 5 类问题不能直接补 622 个 HTML**：占位词与多 h1 的源头在 `docs/01-06` 源文件与 `scripts/build_reader.py`；GitHub 链接前缀错误来自 `build_reader.py:30` 的单一 `BLOB = .../blob/main/docs/`。必须先修生成器与 docs 源，再重生成，并在同批加 4 个机器判据；否则下一轮生成即复发。
2. **dataset 的 8 类问题分两层**：内容修复（README、引文、哨兵、权重量纲、空值）与治理修复（meta/manifest/schema）。`extract_datasets.js` 现用 `JSON.parse` 解析页面里的 JS 对象字面量，实测 **39/44 个文件已无法解析**（页面键无引号），dataset 实际是 2026-08 的冻结快照 + 人工整形。
3. **三套数据树不需要物理合并或迁移**：`scripts/output/data`（135 个·计算权威）、`site/data/json`（47 个·运行时发布层）、`dataset`（46 个·外部分享快照）角色不同、消费方不同、schema 不同；合并会破坏 47 处页面 fetch、19 处页面 dataset 提及与 46 处文档引用。需要的是 **manifest + 发布/派生管线 + 新鲜度门禁**，不是搬目录。
4. **最初设计的核心缺陷是「按目录布门禁」而非「按产物矩阵布门禁」**：reader 622 页没有专属判据，dataset 只有 2 件受 provenance 门禁保护，output 层 135 个文件仅 1 个有 meta。新目录一出现就形成新盲区。
5. **防复发的第一优先级是 4 个基础设施件**：产物门禁覆盖矩阵、三树 manifest、dataset schema 注册表、由清单生成的 README。内容修复必须与判据同批落地（铁律 15）。

---

## 1. 证据基线（2026-11-06 实读）

| 面 | 数字 |
|:---|:---|
| `site/reader` | 622 个 HTML（reader 102 + people 216 + themes 210 + essays 45 + culture 35 + poetry 14）；205 页正文含「（待补）」410 处；199 条 GitHub 链接前缀错误（127 页）；33 页多 h1；3 组同题页；1 个零入链跳转页 |
| `dataset` | 46 个 JSON（44 根级 + `entities/` 2）；17/44 有显式 `meta`；3/9 事件零引文；9 节点 `chapter=0`；6 个文件有权重（0–1 与 4–10 两套量纲）；4 个 sankey 用数字索引；17 个空数组 + 1 个 null |
| 三树 | output 135 个（显式 meta 1/135）；site/data/json 47 个（425KB，47/47 被页面 fetch）；dataset 46 个（2.76MB，页面提及 19 处、文档提及 46 处、7 处运行时 fetch） |
| 已发布层漂移 | site/data/json 与 output 同名文件：**23 相同 / 24 不同**（其中 6 个含 site 侧附加注记，其余为顺序、标签、数值或 schema 差异） |
| 快照层漂移 | dataset 与页面 EMBEDDED：**35 相同 / 2 不同**（81-hardships、magic-system）；5 个无对应页；2 个页面无 EMBEDDED 字面量（dashboard、text-search） |
| 生成器状态 | `extract_datasets.js` 对 39/44 dataset 文件解析失败（页面对象键未加引号）；`build_reader.py` 单一 docs 前缀导致 source 链接错位 |
| 同类写法 | `docs/source` 旧前缀仅 reader 127 页；可见占位词仅 reader 205 页（docs 源 207 文件）；多 h1 另有 4 个生产页（data/en 各 2）；同题页仅 reader；`chapter=0` 仅 dataset；output 层 weight>1 有 1099 处（多为共现次数，非同一语义） |

---

## 2. site/reader 五类问题修复方案

| ID | 问题 | 根因 | 修法（文件与步骤） | 验收 | 批次 |
|:---:|:---|:---|:---|:---|:---:|
| R-1 | 205 页正文「（待补）」410 处 | docs 源 207 个文件含「双索引链接 … W285 段（待补）」；`build_reader.py` 原样搬运；W285 已只存 archive | ① 一次性脚本改 docs 源：正向链接改指 `archive/docs/CHANGELOG-ARCHIVE.md`，反向改指 `scripts/output/file-index.md` 的真实条目，删除「（待补）」；② 重跑 `scripts/build_reader.py`；③ 新增 `check_shipped_placeholders.py`（可见正文命中 `待补/待完善/TODO/占位/Lorem` 即 FAIL，负样本必红） | docs 源 0 命中；reader 0 命中；207 页反向链接目标存在；门禁负样本 3/3 判红 | B1 |
| R-2 | 199 条 GitHub 链接 404（127 页） | `build_reader.py:30` 把所有 `../../*.md` 一律加 `docs/`；`../../source/…` 被写成 `docs/source/…` | ① 生成器改路径映射：`docs/*` → `docs/`，`source/*` → `source/`，`archive/*`、`scripts/*`、`dataset/*` → 仓库根；② 重生成后用本地路径存在性对拍 1327 条 blob/tree 链接；③ 新增 `check_github_repo_links.py`（解析 `blob|tree/main/<path>` 映射仓内文件，缺失即 FAIL，外仓白名单；负样本必红） | 199 条全部可解析（18/18 唯一目标存在）；门禁自测 3 例 | B1 |
| R-3 | 33 页多 h1（24 章节页 + 9 人物页） | 源 docs 有 2–3 个 `#` 一级标题；生成器逐字转成 `<h1>` | ① 生成器按「首 `#`→h1，后续 `#`→h2，原 `##`→h3」整页降级；② 只重生成受影响 33 页并 diff 复核；③ 新增 `check_heading_hierarchy.py`（内容页恰 1 个 h1；`meta refresh` 跳转页豁免 0 h1；跨级跳 h1→h3 判红） | 622 页：621 页 1 h1 + 1 跳转页 0 h1；4 个生产页同批修 | B1/B4 |
| R-4 | 3 组同题页 | 源 docs 首标题完全相同；生成器直接取首标题 | ① 改 3 组 docs 标题加区分后缀（B 稿/外传/深化）；② 重生成；③ 新增 `check_unique_titles.py` 扫全站 HTML（空白归一后同题即 FAIL） | reader 0 组同题；data/en/root 维持 0 | B1 |
| R-5 | `themes/index.html` 零入链、自指 canonical | 旧路径跳转桩：`meta refresh` 到 `themes-hub`，canonical 仍指自身 | ① canonical 改指 `../themes-hub.html`；② 保留 `noindex,follow`；③ 确认 sitemap 不含该页；④ 可选：`themes-hub` 加「旧目录入口」链接 | canonical 指目标；sitemap 0 收录；跳转实测 200→hub | B1 |

**执行注意**：`build_reader.py` 会整页重写 reader，重生成前必须 `git diff --stat` 确认只动目标页；若存在人工页内改动，先迁到 docs 源或加入生成器覆盖表，禁止直接覆盖。

---

## 3. dataset 八类问题修复方案

| ID | 问题 | 根因 | 修法（文件与步骤） | 验收 | 批次 |
|:---:|:---|:---|:---|:---|:---:|
| D-1 | README 索引 41/44、体积与「40/80」失真、示例死文件 | README 由 `extract_datasets.js` 一次性生成后冻结；表格手工维护 | ① 新增 `scripts/gen_dataset_index.py`：从磁盘实读 44+2 文件生成表格（名称/大小/顶层键/条目数），「提取页面」改为实读 site/data；② 示例改 `dataset/character-relationship-3d.json`；③ 新增 `check_dataset_manifest.py` 校验 README 行 ↔ 磁盘 ↔ 大小 ±5% ↔ count 字段 | README 46 行 0 缺 0 多；大小误差 ≤5%；示例文件存在 | B2 |
| D-2 | 仅 17/44 有显式 `meta` | output 层 135 个仅 1 个有 meta；dataset meta 只在 2 个 curation 文件补过 | ① 在 `dataset/CODING.md` 增补统一 meta 契约（source/derived_from/generator/generated/updated/coding_version/provenance_batch/weight_scale/link_endpoint_schema）；② 按族补 meta：35 个页面快照件标 `source=site/data/<page>.html#EMBEDDED_DATA`；5 个无页件标人工来源；③ 生成器候选模式自动注入 meta；④ 门禁要求 44/44 有 meta，历史件可 `legacy:true` + `source` | 44/44 有 meta 或 legacy；0 缺 source | B2/B3 |
| D-3 | edge 9 事件中 3 组零引文且仍报「9 条精确」 | 事件 schema 无 `quote_status`；门禁只校验已存在引文 | ① 每事件补 `quote_status: verified|not_probed`；② 59–61、65–66、75–77 三组先跑 `scripts/_cite_probe.py` 补精确子串，补不到则标 `not_probed` + 原因；③ 门禁：`verified` 必须 ≥1 引文且精确，`not_probed` 必须有 reason；④ 输出区分「已核 6 / 未探 3」 | 9/9 有状态；verified 引文全精确；文案不再混报 | B2 |
| D-4 | 9 个节点 `chapter=0` 无文档约定 | 天庭/佛门节点无具体回目，早期用数字 0 作哨兵 | **推荐**：改 `chapter:null` + `chapter_scope:"deity_no_chapter"`，并给 3 个消费页加 null 守卫（browser 冒烟）；备选：保留 0 并在 `meta.chapter_sentinel` 声明。门禁：数字 0 禁止，null 必须带 scope | 9 节点 0 个数字 0；3 页渲染无 JS 错误；门禁负样本 | B2 |
| D-5 | 0–1 与 4–10 两套权重量纲 | 各分析脚本自行定义，无逐文件声明 | ① 6 个含 weight 的文件补 `meta.weight_scale`（0-1 / 0-10）；② 门禁按声明校验范围；③ **不重标定数值**（会改变页面表达） | 6/6 声明；全部 weight 落在声明区间 | B2 |
| D-6 | 4 个 sankey 段用数字索引端点 | 早期 ECharts/Sankey 习惯用数组下标，network 段用 id | ① 补 `meta.link_endpoint_schema:"index"|"id"`（文件级或段级）；② 门禁按声明校验（index 必须 0≤x<nodes.length；id 必须闭合）；③ 可选给 sankey nodes 补 `id=index` 统一 | 4/4 声明；闭合校验 0 误报 | B2 |
| D-7 | 17 空数组 + 1 null 无「无/待补」语义 | schema 未区分 `none` 与 `missing` | ① `text-evolution` 8 处空字段 + `chapters:null` 先回源补齐，补不到改 `null` + `completeness:"unknown"`；② `cave-estate` 4 处下级空标 `"none"`；③ `criticism-history` 1 处先补或标缺；④ 门禁：空数组仅允许在 `meta.allowed_empty` 白名单内，否则 FAIL 并列出路径 | 18 处全部有归类；0 未归类空值 | B2 |
| D-8 | 无 manifest、无跨层对拍；`narratology-13d` 无对应页 | dataset 无来源声明；页面已升 16d，13d 成孤儿 | ① 新增 `dataset/MANIFEST.json`：file/source(page EMBEDDED|output|manual)/derived_from/transform/consumers/hash；② `narratology-13d-network.json` 标 `deprecated:true` 或删除（需用户确认）；③ 新增 `check_dataset_manifest.py`：46/46 有条目；页面快照件与页面 EMBEDDED 深比对；transform 件按声明校验；④ 修 `extract_datasets.js`：用括号平衡 + `vm` 解析 JS 字面量，只写候选目录，不直接覆盖 dataset | manifest 46/46；35 快照件 0 漂移；2 差异件已修或声明 transform；13d 有处置 | B3 |

---

## 4. 三套数据树对比与「同步/迁移」裁决

### 4.1 角色与实况

| 树 | 文件数 | 体积 | 实际角色 | 消费方 | 与相邻层关系 |
|:---|:---:|:---:|:---|:---|:---|
| `scripts/output/data` | 135 | — | 分析脚本批量产出（计算权威） | 发布脚本、dataset 派生、少量页面 | 显式 meta 仅 1/135 |
| `site/data/json` | 47 | 425KB | 运行时发布层 | 47/47 被页面 `fetch('json/…')` 消费 | 23/47 与 output 完全相同；24/47 有差异（6 个含 site 侧注记） |
| `dataset` | 46 | 2.76MB | 对外结构化快照（页面 EMBEDDED + 人工整形） | 19 处页面提及、46 处文档提及、7 处运行时 fetch | 35/44 根级文件与页面 EMBEDDED 完全相同；2 个不同；5 个无页 |

### 4.2 裁决：**不做物理合并，不做目录迁移**

理由（均为实读证据）：

1. **消费路径不同**：`site/data/json` 的 47 个文件名就是 47 个页面的 fetch 路径，改目录会破坏 47 处加载；`dataset` 被 19 处页面文案 + 46 处文档 + 7 处运行时 fetch 引用，改路径会同时产生站内死链与 GitHub 死链。
2. **schema 不同**：同名/近名对只有 2 组（`81-hardships` ↔ `hardships_81`、`cave-estate` ↔ `cave_estate`），且前者是「聚合 dict vs 明细 dict」、后者是「聚合 dict vs 22 项数组」；4 组与 output 同名的文件也全部 schema 不同（`magic-system` 是 5 段 bundle、`timeline` 是包一层 `timeline` 键）。
3. **权威方向不同**：site 侧 24/47 有差异，其中 6 个含「W691 口径注记」等 site 专属内容 ⇒ `site/data/json` 不是 output 的纯副本，而是「output + 发布注记」。
4. **dataset 是页面快照，不是 output 派生**：35/44 与页面 EMBEDDED 全等；`extract_datasets.js` 的输入就是 `site/data/*.html`。把 dataset 迁到 output 目录会改变其血缘。

### 4.3 正确做法：三层各自声明来源，用管线连接

```
scripts/output/data/*.json          （计算权威）
        │  build_publish.py（读取 output + overrides）
        ▼
site/data/json/*.json              （运行时发布层·文件名/路径不变）
        │  （页面 EMBEDDED 与 fetch 同源）
        ▼
site/data/*.html                   （页面 + EMBEDDED 回退）
        │  build_dataset.py（页面快照 + curated 覆盖）
        ▼
dataset/*.json + MANIFEST.json     （对外快照·命名不变）
```

- **新增 `scripts/output/data/_overrides/<name>.json`**：承接当前 site 侧 6 处注记与其余人工差异，发布时合并；禁止再直接手改 `site/data/json`。
- **新增 `scripts/build_publish.py`**：output + overrides → site/data/json，保持 47 个文件名不变；产出 `MANIFEST-publish.json`（输入 hash / 输出 hash）。
- **新增 `scripts/build_dataset.py`**：以页面 EMBEDDED 为基座（35 个）+ 5 个手工/文档派生件 + curated meta，生成 dataset 候选；`extract_datasets.js` 只保留为兼容入口。
- **迁移触发条件**（未来才考虑）：当 manifest 连续 3 个批次显示 `site/data/json` 与 output+overrides 0 漂移、且 dataset 与页面 EMBEDDED 0 漂移时，才允许讨论物理合并；当前不满足。

---

## 5. 最初设计的八个问题（根因）

| # | 设计问题 | 实证 |
|:---:|:---|:---|
| 1 | **多层数据无 manifest/血缘**：output→site-json→dataset 三层各自生成，谁派生谁、用什么变换、何时更新均无声明 | output meta 1/135；site-json 24/47 与 output 不同；dataset 无 `derived_from` |
| 2 | **发布层允许手工编辑**：site/data/json 被直接改出注记与数值差异，没有 overrides 层 | 6 个文件含 site 专属注记；journey_route 章号 19/20、translation_bias 首章 1/4 等数值差异 |
| 3 | **门禁按目录布点，不做产物矩阵**：reader 是新生成目录，未登记到任何专属门禁；dataset 只有 2 件受 provenance 保护 | reader 622 页仅被 rglob 类门禁扫到；`check_inlined_css` 漏 102 页；dataset 门禁覆盖 2/46 |
| 4 | **生成器允许「未完成态」出厂**：模板占位符无发布闸 | 207 个 docs 文件「（待补）」被原样生成到 205 个页面 |
| 5 | **路径前缀硬编码 + 链接门禁只查本地相对链接**：所有非 site 的 md 都按 `docs/` 前缀拼 GitHub URL | `build_reader.py:30` 单一 BLOB；199 条 `docs/source/` 404 全部逃过 `lint_links` |
| 6 | **schema 无注册表**：权重单位、章节哨兵、sankey 端点类型由各脚本自定义 | chapter=0 9 处；0–1 与 4–10 两套权重；4 个 sankey 数字索引 |
| 7 | **清单类文档手工维护**：README 表格、大小、页面数不随磁盘生成 | README 41/44、5.1KB vs 17.0KB、40/80 vs 89 页 |
| 8 | **教训未转机器判据**：每轮审计靠人工发现，同类缺陷在新目录重复 | 多 h1 在 reader 修完后仍在 4 个生产页；占位词只在 reader 被看见，docs 源从未被扫 |

---

## 6. 同类写法在其他位置的扫描结果

| 模式 | reader | site/data | site/en | site 根 | dataset | output | 判断 |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---|
| `docs/source/` 旧前缀 | 127 页 / 199 处 | 0 | 0 | 0 | 0 | 0 | reader 生成路径独有，根在生成器 |
| 可见占位词 | 205 页 / 410 处 | 0 | 0 | 0 | 0 | 0 | 输出只在 reader，源头在 docs 207 文件 / 414 处 |
| 多 h1 | 33 页 | 2 页 | 2 页 | 0 | 0 | 0 | `character-semantic-network`、`theological-intervention-network` 中英各 2 页同病 |
| 同题页 | 3 组 | 0 | 0 | 0 | 0 | 0 | 仅 reader |
| `chapter=0` | — | 0 | 0 | 0 | 9 处 | 0 | 仅 dataset 快照层 |
| weight>1 | — | 0 | — | — | 59 处（4–10 量纲） | 1099 处（多为共现次数） | output 的 >1 是计数语义，不是同一缺陷；但证明「无单位声明」是全层问题 |
| 显式 meta | — | 0 | — | — | 17/44 | 1/135 | 越靠计算源头越缺溯源 |
| 已发布层漂移 | — | 24/47 vs output | — | — | 2/44 vs 页面 | — | 三处「手工快照」同构 |

**结论**：reader 的五类主要是「生成器单点缺陷」，dataset 的八类主要是「快照层无血缘」，而 **site/data/json 的 24/47 漂移与 output 的 1/135 meta 是同一设计病的另外两处**；只修 dataset 会留下另外两处。

---

## 7. 防复发机制（按优先级）

| 优先级 | 机制 | 落地件 | 判据 |
|:---:|:---|:---|:---|
| P0 | **产物门禁覆盖矩阵** | `docs/agent/gate-coverage-matrix.md` + `scripts/check_gate_coverage.py` | 每个产物族（site 根/data/en/reader、dataset、output、docs）必须登记「覆盖门禁清单」；新目录未登记即 FAIL（与 `check_repo_layout` L2 同批接线） |
| P0 | **三树 manifest** | `scripts/output/data/MANIFEST.json`、`site/data/json/MANIFEST.json`、`dataset/MANIFEST.json` | 每文件有 `source/derived_from/transform/generated/hash`；派生目标不存在或 hash 不符即 FAIL |
| P0 | **发布/派生管线** | `scripts/build_publish.py` + `_overrides/`；`scripts/build_dataset.py` | 禁止手改发布副本；`check_publish_fresh.py` 对 output+overrides 与 site-json 深比对 |
| P1 | **dataset schema 注册表** | `dataset/SCHEMA.md`（权重单位、chapter 哨兵、sankey 端点、空值语义） | 所有 dataset 文件按声明校验；未声明单位/哨兵即 FAIL |
| P1 | **生成器模板 lint** | `build_reader.py` 自检 + `check_shipped_placeholders.py` / `check_heading_hierarchy.py` / `check_unique_titles.py` | 出厂页面不得含占位词、必须单 h1、标题唯一 |
| P1 | **链接语义门禁** | `check_github_repo_links.py` | GitHub blob/tree URL 必须映射到仓内真实文件；本地与 GitHub 两类链接同批检查 |
| P2 | **清单文档由磁盘生成** | `scripts/gen_dataset_index.py` + `check_dataset_manifest.py` | README 行/大小/计数与磁盘一致；不一致即 FAIL |
| P2 | **准入规则写进治理面** | AGENTS §6 增一条「新增产物族必须同时提交 manifest + 门禁矩阵条目 + 生成器」 | 新目录 PR 缺三项即打回 |

---

## 8. 批次划分与验收

| 批次 | 范围 | 主要改动 | 验收 |
|:---:|:---|:---|:---|
| **B1** | reader 五类 + 4 个 reader 门禁 | `build_reader.py` 路径映射与标题降级；docs 源占位/标题；重生成 622 页；新增 `check_shipped_placeholders.py`、`check_github_repo_links.py`、`check_heading_hierarchy.py`、`check_unique_titles.py`；4 个生产页多 h1 同批修 | reader 0 占位、0 失效 GitHub 链接、0 多 h1、0 同题；4 个新门禁负样本各 3 例；`lint_links` 0 broken；浏览器抽 5 页无回归 |
| **B2** | dataset 内容修复 D-1/D-3/D-4/D-5/D-6/D-7 | README 生成器；edge quote_status；chapter null + scope + 3 页 JS 守卫；6 文件 weight_scale；4 段 endpoint schema；18 处空值归类；`check_dataset_manifest.py` 初版 | README 46 行 0 缺；9/9 quote 状态；9 节点 0 数字 0；6/6 量纲；4/4 schema；18/18 归类；3 个消费页 browser 冒烟 |
| **B3** | 数据分层治理 D-2/D-8 | `build_publish.py` + overrides（承接 24/47 差异）；`build_dataset.py` + manifest；`extract_datasets.js` 改候选模式；`check_publish_fresh.py`；13d 处置 | 47 个发布文件 0 漂移；46 个 dataset manifest 0 缺；35 快照件深比对 0 差异；2 差异件已修或声明 transform |
| **B4** | 全仓同类与防复发 | 产物覆盖矩阵 + `check_gate_coverage.py`；output 层 meta 分族补（135 件）；AGENTS 准入条 | 每个产物族有门禁登记；output meta 覆盖率从 1/135 提升到批内目标；全量 verify 绿 |

**建议顺序**：B1 → B2 → B3 → B4。B1/B2 解决用户可见内容，B3 解决血缘，B4 把教训固化为长期防线。

---

## 9. 风险与待用户裁决

| 项 | 风险 | 推荐 |
|:---|:---|:---|
| reader 重生成 | 可能覆盖 reader HTML 中的人工改动 | 先 `git diff` 基线 + 抽样核对；人工改动迁 docs 或加入生成器覆盖表 |
| D-4 chapter null | 3 个消费页可能对 chapter 做数值排序/过滤 | 推荐 null + scope，并在 B2 内做 browser 冒烟；若页面强依赖数字，退回「0 + meta 声明」 |
| 权重是否重标定 | 4–10 → 0–1 会改变页面表达与文案 | 推荐只声明量纲，不重标定 |
| `narratology-13d` | 无对应页，可能是历史资产 | 推荐先标 `deprecated:true` 并留一个批次观察，再决定删除 |
| dataset 定位 | 继续做「页面快照」还是转「output 派生」 | 推荐保持页面快照（35/44 已天然一致），用 manifest 声明；转 output 派生会改变 5 个手工件的血缘 |
| 新门禁准入 | 新增 4–6 个门禁会增加维护面 | 推荐先并入既有门禁（placeholder/heading/title 可挂 `check_seo_head` 或新文件），矩阵登记后再拆 |

---

## 10. 复现命令（审计时点临时脚本·未入库）

```
py -3 tmpe/reader_dataset_full_scan2.py     # reader 622 + dataset 46 全量
py -3 tmpe/data_tree_compare.py             # 三树命名/结构
py -3 tmpe/data_tree_compare2.py            # 同源对 schema
py -3 tmpe/publish_fresh.py                 # site-json vs output
py -3 tmpe/publish_diff.py                  # 24/47 差异明细
node tmpe/extract_embedded.js               # 页面 EMBEDDED 提取
py -3 tmpe/embedded_compare2.py             # dataset vs 页面 EMBEDDED
py -3 tmpe/pattern_scan.py                  # 同类写法全仓分布
```

---

*本方案为只读审计后的修复设计，未改动任何被审对象；所有数字以 2026-11-06 实读为准，临时脚本在 `tmpe/` 未入库。*
