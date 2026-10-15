# 全站前端页面截图审查报告

- **审查日期**：2026-09-05
- **审查范围**：`site/` 下全部 234 个 HTML 页面（中文根页面 9 + 中文可视化页 87 + 英文站 138），双视口（desktop 1280×800 / mobile 375×812），file:// 直开（站点设计口径），fullPage 整页截图——每个页面的每一个角落均被捕获并经过审查。
- **审查方法**：三层流水线——① Playwright 全量采集 + 程序化断言（console/pageerror/布局/外域请求/空白启发式）；② 联络表（每页一张全页缩拼网格）交由 19 个视觉审查代理全覆盖初审；③ 对全部告警页做「滚动穿透重截」+ 全分辨率切片，交由 8 个复核代理定案，并用代码级取证（grep/引用核对）坐实根因。
- **总体结论**：**采集 468/468 成功，0 次截图失败，0 个未捕获 JS 异常**。234 页中约 195 页完全正常；**确认真实缺陷 15 页（FAIL）**、**存疑/轻微问题 12 项（WARN）**；另有三类「审查伪影」（滚动显现动画、sticky 页脚、短页信箱留白）已被识别并从缺陷中剔除。最严重的一个系统性缺陷（10 页桑基图空白）根因唯一且修复成本极低（一行 script 引用）。

---

## 一、确认缺陷清单（FAIL，15 页）

### A. 桑基图空白渲染（10 页，中英镜像成对）— 系统性，一根因

`d3.sankey` 被调用但页面**缺少 `<script src="../static/js/d3-sankey.min.js">` 引用**（全站 24 个用 sankey 的页面中恰好这 10 个缺失；文件本身存在于 `site/static/js/d3-sankey.min.js`）。页面内建的 `typeof d3.sankey === 'undefined'` 降级守卫生效，因此只显示一行提示文字而非报错，导致此前门禁全绿漏网。

| 中文页 | 英文镜像页 |
|---|---|
| data/intertextuality-network.html | en/intertextuality-network.html |
| data/monster-female-network.html | en/monster-female-network.html |
| data/narratology-12d-network.html | en/narratology-12d-network.html |
| data/narratology-13d-network.html | en/narratology-13d-network.html |
| data/six-senses-narratology-network.html | en/six-senses-narratology-network.html |

证据截图：`screenshots/sheets/desktop/data/intertextuality-network.png`（桑基容器内仅一行小字）等；代码核对：`grep -c 'src="../static/js/d3-sankey.min.js"'` 坏页 0 / 好页（81-hardships、monster-hierarchy-network）1。
修复建议：给 10 页各补一行 script 引用（对照 81-hardships.html 第 10 行），补后重跑 `generate_csp.py`。

### B. 英文站 81 难清单表格初始渲染为空（1 页）

- **en/81-hardships.html**：『Complete List of the Eighty-One Hardships』表格初始状态（筛选器全 All）显示 `No matches, or data not loaded (run via http server).`、计数 `Showing 0/0 trials`，81 行数据全部缺失。同页三张树图与桑基图均正常渲染 81 条（By Cause 27+28+16+10=81），且页首声明 `Data source: embedded build`——数据已加载，属**筛选/初始化逻辑 bug**，不是离线降级。
- 证据：`screenshots/reshoot-slices/desktop/en/81-hardships_001.png`、`_002.png`。

### C. 英文站四维统计子图空渲染（1 页）

- **en/hardship-difficulty-heatmap.html**：『② Four-Dimension Distribution Statistics』2×2 子图中左下 `Rescue Count Distribution` 只有坐标轴（y 0–1.0）无任何柱形；同组其余三子图正常，且下方统计表给出非零 Avg. Rescue Count（0.15/0.45/1.21/2.75）——数据存在、该子图渲染为空。
- 证据：`screenshots/reshoot-slices/desktop/en/hardship-difficulty-heatmap_001.png`。

### D. 图表类型与标题不符（1 页，另见 WARN 同类）

- **en/game-webnovel.html**：`Rarity Distribution Pie Chart` 与 `Element Distribution Donut Chart` 两图标题声称饼图/环形图（副题还承诺中心总数），实际渲染为矩形色块树图（treemap）。次要问题：卡片左缘稀有度标签首字母被裁（'5SR'/'JR' 状）、Power Ranking 条图 y 轴标签被裁、卡片被动技能标签残留中文「被动」。
- 证据：`screenshots/reshoot-slices/desktop/en/game-webnovel_002.png`、`_003.png`。

### E. 源文件锚文本百分号编码原样印出 + 页面横向撑宽（2 页）

- **en/essay-ming-intellectual-history.html**、**en/essay-ming-literary-thought.html**：hero 卡内 'A summary translation of' 之后把**百分号编码的中文源文件名**（`%E6%98%8E%E4%BB%A3…%E9%A2%98.md`）原样印出，读者不可读；该长 token 不可断行，把页面 scrollWidth 撑宽约 2.3 倍（内容只占左侧四成，右侧全空）。两页另有对照表右缘超出视口（表格边框被穿过）。全英文站扫描：**仅这两页**含未解码编码串（%E6 计数 3 与 4），其余 24 篇 essay 的源文件链接正常（如 `<a href="../../docs/06-个人随笔/西游与AI时代.md">`）。
- 证据：`screenshots/reshoot-slices/mobile/en/essay-ming-intellectual-history_000.png`（移动端最明显）。
- 修复建议：两页 HTML 内的锚文本改为中文原文（与 href 解码值一致），或改引英文 slug。

### F. 力导向图连线默认全部隐藏（2 页确证 + 2 页疑似，伴随 A 类）

- **data/monster-female-network.html**（17 nodes × 32 edges）、**data/narratology-12d-network.html**（12 节点 + 22 关联边）：全分辨率复核确证节点间**无任何可见连线**，与标题及边色图例矛盾。根因：页面把 kinship/rival/taming 三个连线图层全部默认 `style('display','none')`（图例开关未默认开启），而同类网络页（character-dynamic-network 等）默认显示。narratology-13d-network 与 en/monster-female-network 未单独复核，呈同样视觉模式，判定疑似同根因。
- 证据：`screenshots/slices/desktop/data/monster-female-network_001.png`。
- 修复建议：默认至少显示主要关系层，或把「连线默认隐藏」改为图例上明确的默认关态说明。

---

## 二、存疑/轻微问题清单（WARN）

| # | 位置 | 问题 | 证据 |
|---|---|---|---|
| W1 | site/index.html（桌面+移动） | 统计带「611 篇 · 研究文档」为 W505 前旧口径，当前应为 **615**（AGENTS §1；W505 起 611→615） | reshoot-slices/desktop/index_000.png |
| W2 | data/cultural-misreading.html | 「国家分布饼图」实渲染为矩形树图（treemap，实现内 treemap 3 处、无 pie/arc）——与 D 类同根因模式 | reshoot-slices/desktop/data/cultural-misreading_002.png |
| W3 | en/famous-time-travel.html | 钱锺书信件卡文字水平溢出被卡右缘裁切（'…porcelain vase at the demon king's' 宾语被裁、落款 'Respectfully, Qian Zhor' 人名中途截断） | reshoot-slices/desktop/en/famous-time-travel_000.png |
| W4 | en/tribulations.html（移动端） | 「The Complete Eighty-One」清单为 `max-height:520px; overflow-y:auto` 限高滚动容器，静态首屏只见 01–05 行、第 05 行徽章文字在容器底边被拦腰截断、无滚动渐隐提示（内容在 DOM 中，可滚动到达，非缺失）；另 Cause×Outcome 矩阵右缘溢出视口（≈660px/375px） | reshoot-slices/mobile/en/tribulations_001.png |
| W5 | 移动端 26 页 | 程序断言「表格宽度超出父容器且父容器不可横向滚动」：24 页 en essay/cipai 长文 + en/chapters-map + rum-viewer。视觉复核实际表现为**表格向右边距贴边扩展、内容完整换行、未撑破布局**（essay-poetry-imagery、essay-rhythm-analysis 最明显），属可用性瑕疵而非破坏性缺陷 | screenshots/manifest.json layoutIssues 字段 |
| W6 | en/index.html | 两张卡片同题 'The Novel's Own Verse'（全文出现 2 次，描述不同；未深究是否刻意） | pass1 G12 |
| W7 | data/workplace.html | 技能条形图「搬救兵」行条内白字标签略贴右缘（轻微） | reshoot-slices/desktop/data/workplace_002.png |
| W8 | en/essay-ming-intellectual-history / ming-literary-thought（移动端） | hero 卡宽度止于视口宽而右侧留白一半切片（E 类撑宽的伴生表现） | reshoot-slices/mobile/en/essay-ming-*_000.png |

设计内降级（复核确认为正常，不属缺陷）：`data/search.html`（离线模式空结果区）、`data/data-explorer.html` 与 `en/data-explorer.html`（离线内置示例+降级声明框）、`data/character-relationship-3d-view.html` 与 `en/character-relationship-3d-view.html`（离线为数据表查看器，22 行中可视 11 行为容器内滚动，http 模式才有 3D）、`dashboard.html`/`index.html` 对 `127.0.0.1:8777/health` 的探活请求、rum-viewer/visit-viewer 空态。

---

## 三、审查伪影（非页面缺陷，方法论记录）

首轮初审的多数「大段空白/缺失」怀疑经滚动穿透重截证伪，共三类：

1. **滚动显现动画**：`reveal-in` + IntersectionObserver 的区块在 fullPage 截图下不触发（内容停留透明）。中招判定：curated.html（移动端「6400px 空白」）、guide.html（中段 3000px 空白）、index.html（格1-2 空白）。重截后内容全部完整（reveal 计数 3/3、4/4）。
2. **sticky/fixed 页脚重复**：cross-time-danmaku、guanyin-six-roles-network、mobile-index 的「双页脚」为整页截图拼接伪影。
3. **短页信箱留白**：≤1600px 的短页在联络表单元格里居中留边，首审误读为「页头缺失/顶部空白带」（data/search、data-explorer、character-relationship-3d-view、81-hardships-view、en/dukou-engine 等）。

> 后续复用本审查管线时建议：采集脚本默认带滚动穿透（`_tmpe_reshoot.js` 的滚动逻辑），联络表对短页顶格贴放。

---

## 四、通过情况统计

| 组 | 页面数 | 桌面（初审 pass/warn/fail） | 移动复核集（初审 pass/warn/fail） |
|---|---|---|---|
| 中文根页面 | 9 | 见 verdicts-pass1（G01/G07/G16） | 9 页全审（G17/G19） |
| 中文可视化页 | 87 | G01–G06 全审 | 告警页入选 |
| 英文站 | 138 | G07–G16 全审 | 告警页入选（G17/G18） |
| **合计** | **234** | **234 页全审：pass 191 / warn 31 / fail 12** | **34 页全审：pass 15 / warn 17 / fail 2** |

（原始判定见 `report/verdicts-pass1.jsonl`，268 行 = 234 桌面 + 34 移动复核集；定案见 `report/verdicts-pass2.json`。）

- 初审共 268 个判定：pass 206、warn 48、fail 14（桌面 12 + 移动 2）。- pass2 定案调整：3 页 fail→pass（en/character-relationship-3d-view、curated 移动、guide 移动——均为伪影/设计内降级）；3 页 warn→fail（en/game-webnovel、en/essay-ming-intellectual-history、en/essay-ming-literary-thought）。
- **最终定案：FAIL 15 页**（§一），**WARN 8 项**（§二）。
- 自动断言：468 次采集 **0 capture error、0 pageerror**；非白名单 console.error 0 条；外域请求仅 4 次（127.0.0.1:8777/health 本地探活，设计内）——**零外域铁律全站达标**。

---

## 五、产物目录（本报告所在 tmpe/）

```
tmpe/
├── screenshots/
│   ├── desktop/            # 234 张桌面整页截图（1280 宽，fullPage）
│   ├── mobile/             # 234 张移动整页截图（375 宽，fullPage）
│   ├── slices/             # 2349 张全分辨率切片（>1600px 高的页面，1600px 块/100px 重叠）
│   ├── sheets/             # 468 张联络表（每页一张全页缩拼网格，pass1 审查用）
│   ├── reshoot/            # 25 组滚动穿透重截整页图
│   └── reshoot-slices/     # 重截图的全分辨率切片（pass2 复核用）
└── report/
    ├── shot-review-report.md   # 本报告
    ├── manifest.json           # 468 条采集元数据（时长/console/pageerror/布局断言/外域请求/textLen/svg/canvas/页高）
    ├── slice-index.json        # 每页切片索引与页高
    ├── judge-groups.json       # pass1 分组
    ├── reshoot-manifest.json   # 重截元数据（含 reveal 显现计数）
    └── reshoot-slice-index.json
```

采集/审查工具（一次性脚本，`_` 前缀，不入门禁/CI，未 git add）：
`scripts/_tmpe_shots.js`（全量采集）、`_tmpe_slice.py`（切片）、`_tmpe_sheets.py`（联络表）、`_tmpe_reshoot.js`（滚动穿透重截）。

## 六、覆盖与口径说明

- 覆盖：`site/**.html` 全部 234 页 × 2 视口 = 468 张整页截图，**无遗漏**；site/chapters|characters|themes 为空遗留目录（无页面）；`xiyouji-agent-web/` 为需后端 + CODEBUDDY_API_KEY 的本地工具型 SPA，不在静态站截图审查范围。
- 移动端视觉复核集 = 9 个中文根页 + 全部自动断言告警页（34 页）；其余移动页依赖同一套模板（英文长文页互为同模板），其桌面视图已 100% 视觉复核、移动视图 100% 截图留档 + 断言覆盖。
- 截图约定与 CI 同源（file://、load+2s、良性噪声白名单），差异：mobile deviceScaleFactor=1（CI 为 2）、新增外域请求拦截取证与空白启发式。

---

## 七、补充审查：保真度地图与二次发现（2026-09-05 追加）

### 7.1 各层审查保真度（如实说明）

| 层 | 覆盖面 | 分辨率/保真度 | 能看出什么 | 看不出什么 |
|---|---|---|---|---|
| pass1 联络表（19 代理） | 234 页桌面全量 + 34 页移动复核集 | 每屏缩至 ~31%（1280×1600→400×500）；超长页整表再被压缩，最长移动页（31064px）每格有效宽度仅 ~60-117px | 空白容器/缺图/裸 HTML/大错位等结构性问题 | 小号文字、标签裁切、细线元素、编码串等文字级问题 |
| pass2 全分辨率切片（8 代理） | 25 组告警页组合（~30 页） | ~98% 原始分辨率，文字可读 | 文字级缺陷（编码串、裁切、空状态文案、旧数字） | 未覆盖的 ~200 页的文字级问题 |
| DOM 文本扫描（_tmpe_textscan） | 234 页 × 双视口全量 | 文本层 100% 精确（含 opacity:0 隐藏元素） | 异常 token（undefined/NaN/编码串/加载失败等）、横向溢出精确值 | 视觉问题（裁切/错位/对比度） |
| 像素空带扫描（_tmpe_blankscan） | 468 张截图全量 | 逐像素（64 列采样+行均匀性） | 页中段 ≥900px 纯色空带的确定性证据 | 带内细小内容（采样列数有限） |

**结论口径**：结构性问题为 100% 覆盖；文字级问题在 30 页复核集 + 全站 DOM 文本扫描下覆盖；**视觉文字级（标签裁切类）只对 30 页复核集做了人工级确认**，其余页面依赖 DOM 扫描兜底。

### 7.2 二次发现（补充核验新坐实的问题）

1. **「标题饼图、实无饼图」扩展**（D 类升级）：全站穷尽扫描「可见标题含 饼图/环形图/Pie/Donut × d3.treemap 实现 × d3.arc/pie 缺失」，新增坐实 **data/deconstruction.html 与 en/deconstruction.html**（`国家分布饼图`标题、全页 0 处 arc/pie 代码、1 处 treemap）——与已确认的 cultural-misreading、game-webnovel 同签名。data/jurisprudence.html 同页既有 arc/pie 又有 treemap，是否存在不符**需人工确认**（初审未发现异常）。poetry-rhythm-analysis（中英）标题已改为树图口径、且代码注明「P2 试点：7 类饼图 → 矩形树图」，属有意升级，不算缺陷。
2. **「连线层默认隐藏且永不可见」扩展**（F 类升级）：`linkSels`/`LINK_LAYERS` 全仓消费端核查证实——monster-female（3 层）、narratology-12d/13d（各 1 层）、intertextuality（2 层）、six-senses（2 层）、**relationships（3 层，中英两页）** 的边层创建后仅 push/注册，**无任何运行时代码或 UI 控件能将其显示**（`LINK_LAYERS` 无运行时消费者，仅归档批量脚本写入过该模式）。即 **6 组中英镜像共 12 页**的力导向/关系网络图节点间连线不可达。部分页面（monster-female、narratology-12d/13d）经全分辨率视觉确证；relationships、intertextuality、six-senses 为代码级坐实（视觉上初审因缩放未察觉）。
3. **旧口径数字扩展**：`site/dashboard.html` 统计带为 **「A1-A6 共 611 篇文档 · A3 人物分析 211 篇」**（均旧口径，应 615 / 215），与 index.html 的 611 同类。dukou-engine.html 页脚版本链中的「611 篇」是历史版本描述（W504 基线），不算缺陷。

### 7.3 追加扫描结果（已完成回填）

**① DOM 文本扫描（`report/text-scan.json`，234 页 × 双视口 = 468 次采集，53 次标记）**

- **异常 token 穷尽结论**：`undefined`、`NaN`、`加载失败`、`渲染失败`、`请刷新`、`Please refresh` **全站 0 命中**；`No matches`/`not loaded` 全部落在已知缺陷页（en/81-hardships、6 组桑基缺引用页）与设计内降级声明（en/data-explorer、en/chapter-stats 的「showing sample data … real data not loaded」示例声明，附生成指令，属离线说明文案）；`percent-encoded` 全部落在 2 篇 ming 长文。→ **文字级异常 token 类问题已穷尽**。
- **横向溢出精确测量（scrollWidth - 视口宽）**：
  - 桌面端全站仅 **1 页**溢出：`en/cross-time-danmaku.html` +328px（新发现；中文桌面版不溢出）。初判桌面「内容横向截断」类怀疑除此外全部排除。
  - 移动端 **36 页**溢出，最重：en/cross-time-danmaku +1193、2 篇 ming 长文 +584/+493（已知）、en/text-evolution +373（新发现，无表格、断言盲区）、data/cross-time-danmaku +322、en/tribulations +283；其余多为 80-160px 的表格/图形贴边（含此前 26 页表格断言页 + jurisprudence/hardship-heatmap/social-media 等非表格页）。

**② 像素级空带扫描（`report/blank-scan.json`，468 张截图全量）**

- 命中仅 3 张，全部为已定性的 reveal-in 伪影页的**原始截图**（desktop/curated 2389px 带、desktop/index 2266px 带、mobile/index 3903px 带——对应 §三第 1 类）。
- **其余 465 张截图中不存在任何 ≥900px 的页中段纯色空带** → 「大段空白」类问题在像素级穷尽后确无漏网。

**③ 缺陷清单增补（在 §一/§二 基础上）**

| 级别 | 位置 | 问题 |
|---|---|---|
| FAIL（新增） | data/deconstruction.html + en/deconstruction.html | 可见标题「国家分布饼图 / Country Distribution Pie Chart」，但全页无任何 d3.arc/d3.pie 代码、仅 1 处 treemap——与 cultural-misreading/game-webnovel 同签名（§一 D 类扩至 4 组页面） |
| FAIL（扩展） | 力导向连线不可见：monster-female、narratology-12d/13d、intertextuality、six-senses、relationships（各含 EN 镜像，共 12 页） | 连线层创建后仅注册（linkSels/LINK_LAYERS），全仓无任何运行时消费者与 UI 控件可将其显示（§一 F 类从 2 页扩至 12 页；其中 relationships/intertextuality/six-senses 为代码级坐实、初审因缩放未察觉） |
| FAIL（新增） | en/cross-time-danmaku.html | 桌面端内容宽超视口 +328px（横向滚动）；移动端 +1193px |
| WARN（新增） | data/cross-time-danmaku.html | 移动端 +322px 横向溢出（世界地图画布类内容宽于 375 视口） |
| WARN（新增） | 移动端溢出 36 页完整清单 | 见 `report/text-scan.json`（26 页为已知表格贴边，另 10 页为非表格内容溢出，如 en/text-evolution +373、en/jurisprudence +106） |
| WARN（待人工确认） | en/chapter-stats.html | 明示「10-chapter mock; real data not loaded」示例数据声明——与中文版数据完整度不一致，需确认是否为 EN 构建有意为之 |

### 7.4 更新后的确定性与残余盲区

- **已穷尽（可确定「仅此这些」）**：结构性渲染问题（联络表 100% 覆盖）；空白类（像素级 100%）；异常 token 文字类（DOM 100%）；横向溢出（逐页测量 100%）；已发现各缺陷类的同模式全仓扫描（代码 100%）。
- **未穷尽（诚实保留）**：① 除 30 页复核集外的页面，其「视觉细节级」问题（小字裁切、图标细节、对比度）只有 DOM/像素兜底、无人工级逐页确认；② 交互态（点击、筛选、图例开关、hover）、http 在线模式、非 Chromium 浏览器、平板/4K 视口均未审查；③ 数据内容正确性（数字/译文的语义对错）不在截图审查能力范围内。

---

## 八、修复批与验证闭环（2026-09-05 追加，W550 候选）

### 8.1 已落地修复（25 个文件，git diff 可查）

| # | 修复 | 文件 | 验证 |
|---|---|---|---|
| 1 | 补 `<script src="../static/js/d3-sankey.min.js">` 引用 | 10 页（5 组中英镜像） | ✅ judge 终审：桑基流带全部正常渲染，0 pageerror |
| 2 | 连线画布可见性（两轮） | 12 页（6 组中英镜像） | ✅ A/B 像素验证 12/12 EDGES-SHOW + judge 终审全部网络连线显形 |
| 3 | 「饼图/环形图/圆环图」标题→「矩形树图」口径（含注释与副题） | cultural-misreading / deconstruction / game-webnovel / jurisprudence（中英共 9 文件） | ✅ judge 终审 4 组全部 yes；jurisprudence 图 3.2 真饼图未误改；全站「可见饼图措辞+无弧形实现」清零 |
| 4 | 编码锚文本 →「英文标题 (essay, Chinese)」 | en/essay-ming-intellectual-history / en/essay-ming-literary-thought | ✅ judge 终审：链接可读、无编码串、桌面无撑宽 |
| 5 | 旧口径数字 611→615、211→215 | index.html / dashboard.html | ✅ judge 终审：统计带 615/215 达成 |
| 6 | **工具修复**：generate_csp.py W536 写路径守卫根目录误算（scripts/ → 仓库根）——重生成模式自 W536 起必然自阻（CI 只跑只读 --check 故未暴露） | scripts/generate_csp.py | ✅ 重生成 27 页哈希更新 + 全站 --check 0 漂移 |

### 8.2 连线缺陷的真实根因链（两轮才定位，记录存档）

1. 第一轮假设「连线层默认 display:none 且无 UI 可显」→ 改为默认显示后**仍未生效**。
2. 运行时探针发现 `<line>` 载体元素存在、样式可见，但 **x1/y1/x2/y2 全部为 null**——tick 回调里是 `drawLinks();; drawLinks();;`（批量生成器 `_batch_canvas_links_multi.py` 的痕迹）：**边其实一直画在 canvas.link-canvas 上**，SVG line 只是样式载体（display:none 是有意设计，第一轮的改动方向错误，已回滚）。
3. 二轮探针：12 页的 canvas 全部有绘制内容且与 svg 像素级对齐，唯一障碍是**后置兄弟 svg 的不透明背景**（白/米白，来自 `.chart-svg` 类规则或页面覆盖）把画布完全盖住。
4. 修复：`canvas[class*="link-canvas"] + svg { background: transparent !important; }`（邻接选择器精准命中画布后面的 svg；首版无 !important 被 relationships 的页面级背景规则压制，补强后三层画布全部显形）。
5. 注意：link-canvas 架构全站共 **36 页**（18 组中英镜像），本次只修了 12 页「确认不可见」的；其余 24 页边可见（不同渲染路径），如后续发现同类症状可复用此修复。

### 8.3 修复验证中发现的新问题（既有问题，未入本批修复，已登记）

- **数据/内容类**：six-senses 桑基第三层混列（时间/空间/嗅/触四感官的流带绕过中列结构术语直达右列，与「感官→四层结构→西游案例」三层定义不符，疑数据结构问题）；relationships 演化时间线「89 回」与图例「88」不一致（中英同源）；en/narratology-13d 满页 13/16/17 维度口径混用（13d→17d 升级残留）；en/game-webnovel 卡片残留中文「被动」。
- **视觉类（轻）**：树图浅色格白色标签对比度低（cultural/deconstruction/game-webnovel/jurisprudence 多页）；en/relationships 势力分布条形图标签被裁、Belbin 表超宽膨胀、搬救兵卡片标题副题重复、全角标点直出；en/intertextuality 热力矩阵行标左裁 + 力导向节点标签重叠；en/monster-female 时间线刻度文案相连；en/game-webnovel 移动端 Power Ranking y 轴标签硬裁切。
- **横向溢出**：36 页移动端溢出与 en/cross-time-danmaku 桌面溢出（§7.3）未修——涉及模板/画布宽度策略，建议单独批次处理。

### 8.4 门禁与残留

- 修复后：`generate_csp.py --check` 233 页 0 漂移；`check_js_syntax --all` 通过；`check_structure` 通过；`verify_delivery` 核心全部通过 ✅。
- 改动清单：24 个站点 HTML + 1 个工具脚本（generate_csp.py 守卫修复），共 61 insertions / 27 deletions，无意外文件。
- 提交前待办（不在本批）：按铁律 #1 登记 W550（CHANGELOG + 交接文档）后提交；本批未 bump 版本号。
- 验证产物：`tmpe/screenshots/verify/`（48 张修复后重截）、`verify-slices/`（363 张）、`report/verify-index.json`、`report/ab/`（12 页连线 A/B 对比帧）、`report/force-fix-test.png`。

---

## 九、遗留清单清理与 W550 登记（2026-09-05 追加，二波）

用户指令「§8.3 遗留清单也解决」→ 二波修复（站点 HTML 60 文件）：

| # | 项 | 修复 | 验证 |
|---|---|---|---|
| 1 | six-senses 桑基第三层混列 | 中英各补 16 条「术语→案例」链（案例名取自西游记公设内容，花果山/蟠桃宴复用既有节点）；案例数 5→4 全载体贯彻（CN 案例数×21 / EN Cases×21 / 统计卡 35→28 / 定义句） | judge 终审：7 感官三层全贯通、右列无悬空术语、概览卡/汇总表/定义/统计卡全部 4/28 一致 |
| 2 | relationships 文案与图例不一致 | 中英文案对齐图表可见值（88/78） | judge 确认（E2 轮） |
| 3 | en/narratology-13d 维度口径混用 | 中英统一 **16 维**（title/KPI/壹贰肆陆小节标题/定义演化链 7→12→13→16）；「4 新增维度」KPI 保留（12+4=16 自洽） | 源级断言 + 复查清零（十七维/Thirteen/13-DIMENSION 0 残留） |
| 4 | 树图浅色格白字对比度 | 8 页标签亮度自适应填色（luma>0.60 深墨 #23201A / 否则白字） | judge 终审：3 页 yes；game-webnovel 金色格踩线 → 阈值补杀后重截 |
| 5 | EN 标签裁切 | 热力矩阵左边距 200→250；势力图边距 70/140→150/210；Power Ranking 移动端横滚容器；social-media 徽标可换行；FitChart 左边距 130→150；text-evolution 定宽柱状图 min-width 滚动可达 | judge 终审（J3）+ 重截 |
| 6 | 34 页横向溢出 + danmaku 桌面溢出 | 移动端表格块级滚动（29 页）/ 图表容器横滚 / main overflow-x:clip 兜底 / 弹幕 track 裁剪 | **textscan 受影响 67 页溢出 0/134**；J3 视觉抽查 5 组 yes |

**W550 登记（batch_cascade.py 级联，12 文件）**：CHANGELOG v2.3.150 段（四件套）· file-index W550 段 · 交接文档（骨架修复 + 头尾链 W550 链首）· workflows/README（W450-W550）· README/STRUCTURE/项目说明版本行 · site 四页脚 · AGENTS（§4.3 补录变体穷尽规则 + 脚注）。级联前修复了两个前置障碍：① 交接文档「一、当前进度」章被历次级联滚动淘汰误吞（W548 起缺失，已重建）；② 头尾链每批重复两条（已去重）。级联后修正一处：CHANGELOG 段标题补 W 号前缀（工具 title 不自动带 W 号）。

**终门禁**：generate_csp --check 233 页 0 漂移 · check_js_syntax / check_structure 通过 · **verify_delivery 核心全部通过 ✅**（本报告与 W550 登记后实跑）。

**登记后剩余已知项（未修，已分级）**：text-evolution 两柱状图部分行标签移动端不显示（既有渲染问题，非本次溢出修复引入；定宽图已可滚动到达）· en/social-media Workplace Fit 个别行标 'Wh' 裁切（已加宽边距，残余待观察）· en/monster-female 时间线刻度文案相连 · en/intertextuality 力导向节点标签重叠 · jurisprudence 橄榄绿格白字对比约 3.5:1（可接受）· 树图浅色格标签在 en/deconstruction 仅最大格渲染（静态渲染现状）。
