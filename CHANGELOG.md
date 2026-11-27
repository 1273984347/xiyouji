### W1347（2026-11-28）：P3 标题结论化：分析页改专题名加结论双段式

> **来源**：用户 2026-11-28「P3 的标题主题化」→ 追问格式后裁决「专题名：结论（推荐）」+「全量改完」。W1341 报告 §七.1：90 页 `<title>` 全是主题名（如「语言风格雷达图」），读者需读完图才知道要点。
> - **格式裁决（含一条实测理由）**：`<title>` = `og:title` = 「专题名：结论 · 详解西游记」；`<h1>` = 结论句。主题词必须留在 `<title>` 里——`scripts/_gen_search_index.py` 用 `<title>` 经 jieba 切词写入搜索索引 `kw`（前端 +4 加权），结论前置会把「雷达图 / 关系图谱」等图型词挤出标题 ⇒ 站内搜这类词搜不到该页。故取「主题在前、结论在后」，结论通过 `<h1>` 与首屏直接送到读者眼前。
> - **结论规则**：≤18 字（去空格计）· 必须是判断而非主题名 · 优先量化（排名/占比/极差/首最）· 数字须出自本页正文或图注 · 不加句末标点 · 不重复图型词。
> - **范围**：82 个分析页改三处（`<title>` / `og:title` / `<h1>`）。8 个工具与参考页（全站搜索 / 原著全文检索 / 数据浏览器 / 知识图谱探索器 / 全站标签云 / 术语表 / 八十一难可交互视图 / 人物关系可交互视图）**保留原样**——它们是功能入口，没有可陈述的结论，硬造结论即为失真。
> - **作业方式**：代理分 5 组逐页读 tagline / KPI / 图注 / 洞察块提炼结论，回传 `{file, topic, conclusion, basis}`（basis = 支撑结论的页面原文，便于复核）；主会话用一次性脚本做 4 道机器校验后统一写盘：① ≤18 字 ② 全局唯一 ③ 专题名须命中现标题 ④ 结论里的数字 token 至少一个在该页出现过。
> - **事故与根修（本批最该记的一条）**：首轮替换用 `<title>(.*?)</title>` 直接匹配，在 `poetry-density.html` 命中**顶部模板注释**里的 `<title>` 字样（注释里写着「2. 修改 <title>、.hero 内标题…」），跨 22 行吃掉注释后半与 `<html>/<head>/<meta charset>/CSP/viewport` 整段 head 结构。发现方式=`git diff --numstat` 出现 3/25 的异常行数（其余页一律 3/3）。处置：`git checkout --` 回滚该页，把替换改成**注释掩码 + 位移替换**（`<!--…-->` 逐字符掩为空格后定位 span，再按偏移改原文），复跑后该页收敛为 3/3。教训：批量改 head 的正则必须先屏蔽注释，且批量写盘后必须看增删行数的分布，不能只看「改了几页」。
> - **级联根修**：`<h1>` 换成结论句后，页脚「同类可视化推荐」的链接名会跟着变成句子（`scripts/w1327_related_links.py::_page_title` 原取 h1 首段）。导航标签不该是结论句 ⇒ 该函数改为**优先取 `<title>` 的专题名**（剥「 · 详解西游记」后缀与「：结论」段），h1 仅作兜底；重放后 39 页标签回到专题名，`--check` 0 失败。
> - **搜索索引**：`python scripts/_gen_search_index.py` 重生成（docs 999 / zh 100 / en 138，与门禁实算一致）。
> - **验证**：`verify_delivery.py --scope full` 核心全部通过（第 46 槽索引新鲜度、第 80 槽对比度、第 82 槽内容完备度均绿）；两个对比度探针（body / graphic 两口径）各 0 处违例；`_w1266_render_legend.py` 图例渲染档案刷新；`w1327_related_links.py --check` PASS；机器校验 82 页全过，另人工逐页核对 8 页 basis 原文（81-hardships / cave-estate / monster-background / narrative-rhythm-curve / philosophy / four-dimensional / wukong-tangseng-benchmark / dialogue-sentiment）与结论一致。
> - **偏差与边界（如实）**：① `character-semantic-network` 与 `theological-intervention-network` 两页 HTML 内**各有两个 `<h1>`**（hero 与正文 header 各一），本批同步改为同一结论句，重复 h1 的既有结构缺陷未动；② `tag-cloud.html` 的条目 `title/desc` 未同步——导航标签按设计保持专题名，不随结论漂移；③ `site/en/` 138 页标题不在本批（EN 站另排）；④ 结论属编辑判断，机器只保证了长度/唯一/数字回查，语义是否成立建议人工再过一遍。
> - **文件**：见 file-index W1347 段。
> - **状态**：已落地（级联+提交后以 gh run list 为准）。

### W1346（2026-11-28）：Belbin 双页改热力矩阵 + P2 两页 3D 深度语义收口

> **来源**：用户 2026-11-28「处理 P2 的 3D 图表」（与 W1345 遗留的两页 9 轴雷达一并收口）。
> - **雷达族清零（基线 2 → 0）**：`relationships` 与 `pilgrim-team-dynamic-network` 的 9 轴 Belbin 雷达 → **行=角色、列=成员的热力矩阵**（单色顺序色阶·格内数值按底色亮度翻转·色阶条图例·`.chart-tooltip` 悬停）；`id`/函数名一并改 `heatmap`，残留雷达签名实测 **0** ⇒ R5 判据下不再有存量豁免页。
> - **P2-1 character-relationship-3d 深度改为数据维度**：原 z 由聚类环几何推导（装饰性），改 **z =（阵营层级 group 0-4 − 2）× 45**（取经团最近 −90 · 龙族最远 +90，层间距 45），层内成环；并把 `velocity.z` 置零、每帧写回 z，避免力导向把深度语义抹平；相机改 3/4 视角（theta −0.85 / phi 1.22）+ fog 200→560，使五层分面可辨；页内加读法说明。`group` 的选取依据：22 节点均有 `group` 与 `GROUP_NAMES`（5 阵营），而 `importance` 已被球半径占用、`source_chapters` 是代表性引证非全量出场。
> - **P2-2 journey-geo-3d 高度改为时间维度**：原 y 取程序化地形噪声（无数据含义），改 **高度 = 回目序号**（`chapterIndex()` 正则取首回目数·12 回 → 6 · 98 回 → 40），长安最低、灵山最高；地形保留为底景；`orbitTarget.y` 与 `VIEW_INITIAL.ty` 同步（否则复位会跳），相机 phi 1.02 + fog 220→420。
> - **验证**：`check_chart_data` 239 页 · **基线 0** · FAIL 0；`check_js_syntax` 873 通过；CSP 注入后 `--check` 0 漂移；对比度探针两口径见收官记录；代理侧另用 headless 浏览器对四页截图实测（热力矩阵 9×5 / 5×9 与色阶条正常、3D z 分层实值 g0→−90…g4→+90、路线由低到高）。
> - **边界**：`site/en/relationships|pilgrim-team-dynamic-network|character-relationship-3d` 为英文镜像，不在本批范围，需另排 EN 批；两页 3D 仍无本仓 Playwright 运行期档案（代理用临时 headless 副本取证后已清理）。
> - **文件**：见 file-index W1346 段。
> - **状态**：已落地（级联+提交后以 gh run list 为准）。

### W1345（2026-11-28）：雷达族 A 组 16 页降级 + C 组 3 页取证（基线 21 → 2）

> **来源**：用户 2026-11-28「继续处理剩余的 21 页雷达族图表」——W1341 报告 §九第 2 档的剩余面。
> - **A 组 16 页改造**（单选实体雷达 + 均值降序点图，各页 axes 实读 4–8、series 一律 1）：heaven-power(12 系列) / monster-sociology(10) / linguistics(8) / social-media(8) / risk-project(8) / language-style-radar(7) / intertextuality(7) / six-senses(7) / guanyin(6) / cognitive-psychology(5) / four-dimensional-research(5) / mbti-evolution(5·阶段切换) / pilgrim-team-psychology(5) / character-sentiment-arc(4) / monster-victims(4) / four-heavenly-kings(4)。
> - **C 组取证后分流**（先取证再处置）：monster-ecology（5 轴 × **12** 系列）改造，顺带订正图注「15 代表妖怪」→ 数据实为 12；theological-intervention（5 × 3）与 ming-political（3 × 3）**本就合规**，只补 `chart-radar-meta` 声明、渲染零改动——基线此前把合规页一并冻结属口径粗。
> - **归一化基准根修（本批最重要的把关）**：单选化会让「按传入数组取 max」的归一化退化成「每维最大值=自身」⇒ 多边形恒满格。six-senses 由子代理自查发现并改为全量基准；**intertextuality 同型缺陷由主会话复核发现**（panel 把筛选后的 1 条传给 renderRadar，后者按它取 max），改为模块级 `radarMaxes` 取自全量。其余 17 页扫过 `d3.max` 用法，无此形态。
> - **偏差与发现（如实登记）**：① social-media 八轴取值恒 0/1 ⇒ 轴均值恒 0.5、点图不可排序，改用页面既有的 `workplace_fit` 并在点图上方明示排序键；② monster-sociology 的 `json/mount_deserters.json` 缺 `harm_severity`/`owner_influence` 两字段（http 模式该两轴 undefined），属改造前既存数据漂移，本批未修；③ `site/en/mbti-evolution.html` 英文镜像仍为 5 人叠加（EN 站不在 R5 辖区，留后续 EN 批）；④ 基线注释把 four-dimensional 记为「4 轴 × 5 系列」，实读为 5 轴 × 4 系列。
> - **验证**：`check_chart_data.py` 239 页 · 基线 **2** 页 · **FAIL 0**；`check_js_syntax.js` 873 文件通过；`generate_csp.py` 17 页注入后 `--check` 0 漂移；对比度探针两口径（body / graphic）均 **0 处违例**；`verify_delivery --scope full` 见本批收官记录。
> - **过程记录（第三次撞同一判据）**：辅助三文档的批次行写了「16 页 / 3 页」，被第 31 槽 C5c 判为裸聚合数字（W1342 写「27 页」、W1345 写「16 页 / 3 页」都是同一形态）⇒ 改为不带数字的「多页 / 取证分流」，数字交给 `radar-family-baseline.txt` 与 CHANGELOG 段承载。**规律**：批次行只写结论词，不写会随清理漂移的计数。
> - **边界**：无浏览器运行期取证（仓库无 node_modules/Playwright），19 页的下拉/点图联动建议巡检手点；relationships 与 pilgrim-team-dynamic 两页 **9 轴 > 8**（Belbin），属图型改造，留 W1346 热力矩阵。
> - **文件**：见 file-index W1345 段。
> - **状态**：已落地（级联+提交后以 gh run list 为准）。

### W1344（2026-11-28）：narratology 12/16 轴雷达改热力矩阵 + 三简单页脚前插

> **来源**：用户 2026-11-28「做」——W1343 遗留项（W1341 报告 §九第 2 档最后两页 + 页脚链滞后）。
> - **双页图型改造**：narratology-12d（12 轴）/ narratology-16d（16 轴）→ **行=维度、列=4 指标的热力矩阵**（`scaleBand` 双轴 + `d3.interpolateBlues` 单色顺序色阶 + 色阶条图例 + 行标挂全名 `<title>`）。数值字色按底色相对亮度自动切墨/白，抽样对比度 5.82–17.91:1。数据零改动，原「雷达面积越大…」解释句改为「颜色越深表示得分越高」。
> - **族签名迁移（关键）**：`svg id="chart-radar"` → `chart-heatmap`、`renderRadar` → `renderHeatmap`，全页残留计数 0 —— 否则 R5 仍按 `id="*radar"` 认作雷达族，改造等于没改。两页同步从基线删行（23 → **21** 页）。
> - **页脚链收口**：`site/index.html` / `cross-time-danmaku` / `tag-cloud` 三简单页脚前插 W1344（复用 `batch_cascade._foot_upsert` 单一写入逻辑，不自建第二套插链实现），`dukou-engine.html` 由 `gen_version_footer.py --apply` 同批升到 W1344 —— 四页脚链头自此一致。
> - **验证**：`check_chart_data` 239 页 · 基线 21 · **FAIL 0**；`check_js_syntax` 873 文件通过；`generate_csp` 注入 2 页后 `--check` **0 漂移**；`check_structure` 2047 style 块平衡；第 80/82 槽探针重跑后 `verify_delivery --scope full` 见本批收官记录。
> - **过程记录（对比度探针抓出的真缺陷·三态收敛）**：首轮对比度探针（graphic 底色口径）报 **12 处 < 3:1 · 1 页**（narratology-16d 暗色态单元格数字继承页面 `--ink-soft`，根因是渲染用 `.attr('fill')` 表现属性、被样式表规则盖掉）⇒ 改 `.style('fill')` 内联样式后降到 **2 处**（仍是暗色态最高值格：暗色把蓝色阶整体提亮，浅色字对白底亮蓝仅 2.95）⇒ 最终给数值加**固定白底浅衬片**（20×14·opacity .86）+ 字色恒墨，两口径均 **0 处违例**。教训：热力矩阵的数值字色不能靠"按亮色阶算一次"决定，暗色态会整体改色阶。
> - **边界（如实）**：本批仍无浏览器运行期取证（仓库无 node_modules/Playwright）；热力矩阵的行列标签在 320px 窄屏下的换行表现建议巡检时看一眼（`chart-degrade: scroll-x` 已声明）。
> - **文件**：见 file-index W1344 段。
> - **状态**：已落地（级联+提交后以 gh run list 为准）。

### W1343（2026-11-28）：雷达 P0 四页改造（单选实体雷达 + 全量排序点图）

> **来源**：用户 2026-11-28「继续」——W1341 报告 §九第 2 档，先做系列过载四页（P0）。
> - **改造对象**：monster-female-network（4 轴 × **17**）/ underworld-power-network（5 × **16**）/ monster-capability-radar（5 × **15**）/ monster-hierarchy-network（5 × **14**）——雷达改为**只绘 1 个实体**，全量对比移入下方**均值降序点图**，下拉选择与点图点击双向联动。
> - **合规声明**：四页各加 `<!-- chart-radar-meta: axes=N series=1 -->`，并各自从基线删行 ⇒ 重新受 R5 约束且通过（基线 27 → **23** 页）。
> - **附带修正（改造引入的语义失效，一并根修）**：① 单系列时原「按类型聚合的可点击图例」会一点就把唯一多边形隐藏 ⇒ 降级为静态类型标注（多系列路径原样不动）；② monster-capability-radar 的 4 处 `renderRadar()` 调用（多边形点击 / 图例点击 / 切换按钮 / renderAll）统一改为「切换选中实体」，消除「选中实体与雷达所绘实体不一致」。
> - **验证**：`check_chart_data.py` 239 页 · 基线豁免 23 · **FAIL 0**；`check_js_syntax.js` 873 文件通过；`generate_csp.py` 注入 2 页后 `--check` **0 漂移**（874 页/916 哈希）；`check_structure.py` 2047 style 块括号平衡。
> - **过程记录（判据与工具档位不一致·待后续统一）**：第 74 槽 C1 判「CHANGELOG 65 段 > 窗口 64」时，`archive_segments.py` 默认走体积档判「体积未超阈值·无段可迁」⇒ **段判红而工具拒绝迁移**。本批以 `--keep 60` 显式走段数档解除（迁出 5 段）。根因是 W1340 把工具默认档切到体积档、门禁仍按段判红的遗留不一致；建议后续让工具在段数超窗时自动降档，而不是要求人工记得 `--keep`。
> - **边界（如实）**：本批无浏览器运行期取证（仓库无 node_modules/Playwright），下拉与点图联动建议巡检时手点一次确认；narratology-12d（12 轴）/ narratology-16d（16 轴）两页属**结构改造**（§4B 禁用条件：维度 >8 改热力矩阵），留 W1344，本次未动。
> - **文件**：见 file-index W1343 段。
> - **状态**：已落地（级联+提交后以 gh run list 为准）。

### W1342（2026-11-28）：雷达族入 §4B 选型表 + 族注册判据（W1341 审查的判据侧收口）

> **来源**：用户 2026-11-28 指令「都做」——批准 W1341 报告 §九第 1 档（判据侧三项）并补齐 3 项辅助文档 WARN。
> - **§4B 第 10 族（雷达图）**：`DESIGN.md` §4B 增行——数据形态「多实体 × 多维度同构评分（维度 ≤8·单图实体 ≤3）」/ 图型「雷达图（自绘 polygon + 径向刻度）」/ 禁用条件四款（维度 >8 改热力矩阵 · 单图系列 >3 改「单选实体雷达 + 全量排序点图」 · 多数轴取值齐平禁用 · 无精确比较需求改点图/表）/ 代表页 language-style-radar.html / degrade: simplified。章首「9 族 45 格」→「10 族 50 格」。
> - **spec-check 常量同源**：行数硬编码 9 → `EXPECT_SPEC_ROWS = 10`；改表不同批改常量即 FAIL（报错信息带常量值，避免「改了表门禁假绿」）。
> - **R4 族注册判据（新）**：site/data 实际渲染的族必须已在 §4B 章内注册——表外族一页在用即 FAIL（W1341 实证：雷达族 27 页在用而表内无此族）。签名取 id/function 级；**刻意不复用 R3 词表**：把「雷达」并入 R3 会把「页脚链到 *-radar.html」的纯提及判成措辞×实现错配（W1341 实测 6 页此形态）。
> - **R5 雷达规模判据（新）**：基线外页面须声明 `<!-- chart-radar-meta: axes=N series=M -->` 且 axes ≤8、series ≤3；基线 `scripts/output/radar-family-baseline.txt` 冻结存量 27 页（逐页标注轴×系列与超标等级·删一行 = 该页重新受判据约束）。
> - **验证**：`check_chart_data.py` 现网 239 页 · 基线豁免 27 · FAIL 0 页；`--spec-check` 10 行 0 空格；`--self-test` 10 例 PASS（新增 R4/R5 四例：表外族检出 / 已注册放行 / 缺规模声明检出 / 超限与基线豁免）；新增 `tests/unit/test_check_chart_data.py` 7 例全过（含「改表不改常量必红」与「基线 27 条且路径存在」锁）；ruff 0 违规。
> - **辅助文档补齐**：README / STRUCTURE / 项目说明 当前批次行 → W1342（`bump_version.py` 已于 W711 停用，改为按各文件现行形态手工同步）。
> - **过程记录（如实）**：首轮 `--scope full` 3 项 FAIL 均属「本批改动的跟随面」——① 第 31 槽 C5c 裸聚合数字 4 处（辅助三文档新写的「存量 27 页」被判裸数字）⇒ 改为不带数字、指向基线文件（数字随清理会漂，本就不宜写死）；② 第 31 槽 C5d stats 漂移 ⇒ `stats.py --w W1342` 刷新（pytest_collected 1968→1975 等 18 处标记面跟随）；③ 第 45 槽目录清单漂移（`_w1341/_w1342` 新件未入 Git 索引即 refresh 必漏·W896 口径）⇒ 先 `git add` 再 `gen_folder_docs --refresh`；④ 站内搜索索引内容漂移 ⇒ 重跑 `_gen_search_index.py`。另 pytest 3 例（`test_cascade_handover_rotate`）暴露手工滚动缺陷：W1341 批把指针留成「W1335 及更早」而窗口最老块是 W1336 ⇒ 本批按 W713 归位为「W1337 及更早」（= 当前 min 块），教训是**手滚概要块必须把指针同步到 min 块，或直接用 `batch_cascade` 滚动**（判据已有，本次是绕开判据所致）。
> - **边界（如实）**：本批只立判据与基线，**未改任何页面**——存量 27 页的雷达过载仍在其位，改造属 W1341 报告 §九第 2 档（另批）；3 个简单页脚（index / cross-time-danmaku / tag-cloud）仍停在 W1340 链头，由下次级联批统一前插。
> - **文件**：见 file-index W1342 段。
> - **状态**：已落地（级联+提交后以 gh run list 为准）。

### W1341（2026-11-28）：图表选型审查报告落盘（雷达族选型裸区）

> **来源**：用户指令「先把体检结果落成文档存档」（前序为 `build-web-data-visualization` 插件能力评估 → 「图表选型体检」选项 → 90 页只读扫描）。
> - **审查定位**：审查对象由「画得对不对」换成「**选得对不对**」——编码层选型，与 W1259 全站可视化图表审查（渲染/数据/门禁覆盖）互补不重叠。
> - **P0（判据缺口）**：`DESIGN.md` §4B 九族选型表的机判把表体行数硬编码为 9（`scripts/check_chart_data.py:154`），而**雷达族 27 页在用却不在表内** ⇒ 无数据形态约束 / 无禁用条件 / 无窄屏降级 / 零机器判据。页面自证：[six-senses-narratology-network.html](site/data/six-senses-narratology-network.html) 正文写「雷达图四条轴里只有引用度一条拉开差距，其余三条完全齐平」。
> - **P1（规模失效）**：系列过载 12 页 ≥7 系列（4 页 ≥14：monster-female 17 / underworld 16 / monster-capability 15 / monster-hierarchy 14）；轴数超限 2 页（narratology-16d 16 轴 / narratology-12d 12 轴）。
> - **P2（3D 无数据深度）**：`character-relationship-3d.html` 的 z 由 `groupIdx` 聚类环几何推导（L1442-L1470）；`journey-geo-3d.html` 自述「本页提供立体纵深感」（L301）。
> - **P3（编辑层）**：标题全为主题名而非结论；主题多页同构（取经路线 5 / 妖怪 7 / 叙事学 4）；实验图表页（chart-design 三装置）判为刻意保留。
> - **自我修正 4 项**（探针初判被逐页取证推翻）：截断基线轴（实为气泡半径/箱线/散点域）· 37 页缺 tooltip（命名变体假阴性，实测仅 8 页无交互且均为文本/检索页）· 力导向掩盖层级（实为 `forceX/forceY` 分层锚定）· 12 等分饼图（实为 `.value(1)` 表盘布局）。教训：族/功能探针须做命名变体枚举，禁单一命名命中即下结论。
> - **已达标面**：0/90 页命中彩虹/涡轮色阶 · 90/90 页 EMBEDDED 回退 · 87 页 a11y / 84 页 audit 注入 · 双轴 3 页 5 图全部有右轴标注（不列整改）。
> - **验证**：4 个临时只读探针实跑（族签名/域值/轴×系列/悬停实现）+ 逐页代码取证；报告落 `docs/11-方案报告/审查与评审/图表选型审查报告-2026-11-28.md`（10 章 + 2 附录）；`docs/11-方案报告/README.md` 篇数 27→28 + 编号 156 登记；`verify_delivery.py --scope docs` **退出 0**（核心 FAIL 0 · 辅助 WARN 5：页脚版本滞后 1 + 辅助文档里程碑 token 3 + 存量缺内嵌回退 7 页冻结项）；`generate_csp.py --check` 874 页 0 漂移（本批未改内联脚本）；站内搜索索引 docs 998→999 已重跑生成器刷新。
> - **边界（如实）**：只审 ZH `site/data/` 90 页；`site/en/` 82 图表面、饼图类别数、面积图系列数、浏览器渲染实测均未取证（报告 §十）；探针会话临时脚本未入库，固化为第 1 档建议。
> - **文件**：见 file-index W1341 段。
> - **状态**：已落地（级联+提交后以 gh run list 为准）。

### W1340（2026-11-27）：腾窗工具链六项收口：体积档默认与跨面事务

> **来源**：用户 2026-11-27 P3 清单六项（评估中仅 P0-3 已批，其余六项本次一并收口）。
> - **P0-1 默认体积档**：`archive_segments.py` 的 `--keep` 默认由 109（段数档）改为 None；未显式给 `--keep`/`--max-bytes` 时自动走体积档（`MAX_DOC_BYTES=262144`，单一事实源 utils/gate_common）——原段数档与真实约束（字节窗）错位。
> - **P0-2 水位**：新增 `--headroom`（默认 8192 字节），实际迁移目标 = 硬上限 − 水位，不再每次腾到贴线；最终对齐断言同用水位口径。
> - **P1-1 跨面事务**：`move()` 增 `defer` 模式——两面内容先在内存算定、全部守恒断言通过后才统一落盘（`_write_all_or_rollback`），任一写失败回滚已写件，消除「changelog 写成功、file-index 断言失败」的半迁移。
> - **P1-2 迁移台账**：新增 `archive/docs/archive-log.jsonl`（只追加 JSONL·每面一条 migrate 记录：批次/迁出段数/W 区间/迁前后段数与字节），并登记进维护手册单一写入者表。
> - **P1-3 归档检索**：新增 `scripts/history_grep.py`——一次覆盖一级卷/tier2/清单/迁移台账，支持字面量/正则/忽略大小写/每文件上限/JSON；退出码 0 有命中、1 无命中；维护手册场景 E 改以它为首选。
> - **P2 段数窗**：`check_doc_size_budget.py` 的段数窗由固定 110 改为**由字节窗推导** `SEG_WINDOW = 262144 ÷ 4096 = 64`（附一致性断言）——原 110 段在段均 ≈3.7KB 时约 430KB ≫ 262KB，段数判据永不先触发；现段数窗先于体积窗生效并留 ≈25KB 水位。**属判据收紧（非放宽）**，文档规范 §8 与维护手册同步。**跟随面**：`batch_cascade.WIN_SEGMENTS` 改为引用 `SEG_WINDOW`（回窗与门禁同源；否则门禁 64 而回窗 110 ⇒ 越窗不迁的死锁）；`test_batch_spec` 窗口断言改为与 `SEG_WINDOW` 对拍；`check_doc_size_budget --self-test` 的窗口边界样本改用 `SEG_WINDOW`（原硬编码 110）。
> - **验证**：pytest 归档工具链 42 例全过（含新增事务回滚 3 例 + history_grep 5 例 + 段数窗推导 1 例）；`archive_segments --dry-run` 默认档零迁移（61 段·226KB）；`check_archive_health` T5/T6 0 FAIL；`gen_archive_manifest --check` 与磁盘一致；第 74 槽窗口 `{CHANGELOG:64, file-index:64, 台账:60}` 0 FAIL；`history_grep W1340` 命中迁移台账。
> - **过程记录（如实）**：收官链首轮 gate 红 3 项，均为「判据跟随面」而非功能缺陷——① 第 42 槽要求新脚本四面引用，测试面只认 `import <stem>` / `from <stem> import` 形态（`import … as` 不算）⇒ `test_history_grep` 改 from-import；② `check_doc_size_budget --self-test` 与 `test_batch_spec` 硬编码 110 ⇒ 改用 `SEG_WINDOW` 对拍；③ ruff 结构档嵌套深度 6>4 ⇒ 抽 `_scan_file`。修后 verify 全量与 pytest 全量复跑绿。
> - **文件**：见 file-index W1340 段。
> - **状态**：已落地（级联+提交后以 gh run list 为准）。

### W1339（2026-11-27）：方案 D 主体：本地问答 trace 与 OBS-19

> **来源**：用户 2026-11-27 指令「先执行 P0 推送，再 P1 之后再 P2 P3 P4」——P2 = 可观测性决策方案 D 主体（D-1~D-5）。
> - **D-1 本地 trace 写入器**：新建 `server/trace.ts`——`data/trace.jsonl` 只追加（`AGENT_WEB_TRACE_LOG` 可覆盖），与 `audit.ts` **分表**（audit=合规留证 L4 / trace=高频观测元数据），留存期复用 audit 的 180 天硬下限（`purgeExpiredTrace`），写入 fail-open 但 `traceDegradation()` 可见（计数 + 最后错误，不静默）。
> - **D-2 引擎落 trace**：`AgentTurnResult.turnTrace` 逐轮记录轮次/耗时/正文字符数/工具名/该轮 usage（缺 usage 记 null 不记 0）；`chat.ts` 成功与失败路径各落一条 trace（只记元数据，不落 prompt/回答正文；错误消息脱敏 sk-* 并截断 300 字符）。
> - **D-3 读取面**：`GET /api/trace?limit=100&session=<id>` 返回 `{ok,limit,total,skipped,degraded,failures,entries}`（与 /api/audit 同受 token 与限流保护）。
> - **D-4 聚合脚本**：`xiyouji-agent-web/scripts/trace-report.mjs` + `npm run trace:report`——按模型/会话/工具聚合，token 缺样本不计入均值，成本仅在配置 `AGENT_WEB_TOKEN_PRICE_INPUT_PER_1K`/`_OUTPUT_PER_1K` 时估算（未配不估算）。
> - **D-5 OBS 挂钩**：架构方案 v1 表与 v2 目标态表各增 **OBS-19 问答 token 用量与成本**（告警级·W1339 起可算）。
> - **同批根治 P-11（W1338 复盘 A-02）**：`preflight_check.py` 终态前缀表补「占位空号」——W1262 空号行曾被判在途 ⇒ touches 假交集拒绝新批开工（W1339 开工实证）；单测 +2 断言。
> - **验证**：agent-web `npm run test:server` 167 例（163 pass / 4 skip PG 不可达 / 0 fail）· `npx tsc -b` exit 0 · `trace:report` 冒烟两态（有/无数据）· pytest `test_preflight_check.py` 41 例全过。
> - **过程记录（如实）**：① 收官链 gate 步第 43 槽在长链压力下偶发 probe_error（单跑 2 次均 0 FAIL·228 页 / 47s）⇒ 判为探针环境性抖动，未放宽判据；② 第 45 槽在新件未入 Git 索引时 refresh 必漏（E-269 类）⇒ 按门禁自带处方「先 add 再 refresh」复跑 0 FAIL。
> - **文件**：见 file-index W1339 段。
> - **状态**：已落地（级联+提交后以 gh run list 为准）。

### W1338（2026-11-27）：复盘批 T1：W1312-W1337 二十六批全区间复盘

> **来源**：preflight T1 触发（距上篇复盘 3 天 ≥ 3 天；后续 26 批 / 56 提交，T2 ≥30 批与 T3 ≥80 提交未触发）——用户指令「先等 CI 跑完再开始 P1」，P1 即复盘批。
> - **区间与规模**：W1312-W1337 二十六批 / 53 提交（`22885b0c7..HEAD`）/ 1,145 文件（+110,788 / −1,350,141 行）；净删除中 93.2% 来自共享 CSS 压缩两笔（462 文件 −839,538 行 / 212 文件 −418,488 行）。
> - **三线收敛**：① 容量（W1315-W1319：8 模块依赖环清零 / 搜索语料三副本归一 / 索引去重 + gzip 压缩 / 共享 CSS 无损压缩与全站重同步 / CSS 源瘦身余量 48→3,277 B）；② 推送编排（W1320/W1321/W1326：Backlog 对账、巨批分笔 ≤500 件且每笔自洽、safe_commit 索引态分歧判据、两轮推送等待 E-321）；③ 归档结构（W1335-W1337：清单双形态 + T5/T6 判据 + 250 号宽范围卷 + 旧卷冻结 + 第 84 槽阻断 + 维护手册第 30 篇）。
> - **视觉全量探针三维**：移动端 375/320（8 页裁切根修）、竖版图表 165 页（81 页根修·FAIL 0）、夜读态 243 页（FAIL 46→0·深底浅字 110 块/83 页根修 + 637 页重分发）、A1 交叉引用 100 回 0 死链。
> - **报告**：`docs/11-方案报告/工作复盘与优化分析报告/工作复盘与优化分析报告-2026-11-27.md`（10 章模板 + 3 附录）——经验 E-01~E-08（Top1 手工不变量应生成化 4.75）/ 技能 S-03~S-05 任务卡 / 未用 U-01~U-05 / 场景 SC-01~SC-06 / 问题 P-01~P-12 与问题族 FAM-43~46（三族超复发阈值·均已有机器判据或挂账）/ 工作流 WF-10~12 / 行动 A-01~A-08。
> - **同批清偿**：TODOS 挂起交付两行（C1/C2）判据经 W1334 首笔 `8eafa3c1c` 实测满足（5 件 + 2 件刷新产物已在库·工作树干净）⇒ 按「完成即删」清偿；复盘登记面与目录面的口径差已显式披露（不改判据·登记为 A-08）。
> - **验证**：preflight PASS（N1-N5 一致）；区间 CI 五件套在 HEAD `4c12067b8` 全绿；本批改内联脚本 0 处（CSP 零漂移）；docs-only 面仍跑 full 全量（含第 80/82 槽探针与渲染档案刷新）。
> - **文件**：见 file-index W1338 段。
> - **状态**：已落地（级联+提交后以 gh run list 为准）。

### W1337（2026-11-27）：归档分卷维护手册（方法论沉淀第 30 篇）

> **来源**：用户 2026-11-27 指令「请生成归档分卷的后续维护文档」。
> - **落位判据**：面向「以后同类事怎么做」⇒ 按文档规范 §11 分流规则入 `docs/10-方法论沉淀/`（可复利方法论深度篇），并在该目录 README 登记为第 **30** 篇 + HANDOVER「三、方法论沉淀」同步。
> - **内容**：① 一句话定位（三层容器 + 一份清单 + 六判据）；② 三层容器与冻结边界表（两个无范围名旧卷冻结、archive 只增不改）；③ **单一写入者表**（六个文件各自的唯一写入方，其余禁写）；④ **六场景操作手册**（正本超窗 / 一级破 1MB / 盘面变更刷清单 / 第 84 槽转红的三种成因与处置 / 查 W### 在哪 / 台账行窗）；⑤ 守恒断言与**可证伪演练**（移出豁免 ⇒ exit 1 ⇒ 恢复 ⇒ 0）；⑥ **反面清单**七条（手工剪贴 / 手改清单 / 向冻结卷追加 / 为变绿加豁免 / 改宽度不刷清单 / 只分卷不刷清单 / 工具分工错位）；⑦ 复算命令附录 + 体量基线；⑧ 变更沿革（W960→W994/W995→W1119/W1308→W1335→W1336）。
> - **机器判据**：新文档经 `verify_delivery` 第 84 槽（T5 覆盖）随批全量校验；链接引用经 `lint_links` 目录级校验。
> - **验证**：`--scope full` 绿；文档索引与「10 目录 README 第 30 篇」登记一致。
> - **文件**：见 file-index W1337 段。
> - **状态**：已落地（级联+提交后以 gh run list 为准）。

### W1336（2026-11-27）：页脚版本生成化 + 归档覆盖门禁（第 84 槽）

> **来源**：用户 2026-11-27 指令「按建议 1 把 dukou 页脚版本号改成脚本生成；批准将 T5 升级为阻断性门禁」。
> - **页脚生成化**：新建 `scripts/gen_version_footer.py`——`--apply` 按 CHANGELOG 现役段前插/替换本批 token（**复用 `batch_cascade._foot_upsert` 单一写入逻辑**，不自建第二套插链实现，避免重演 W724 同号双 token 与 W1122 链长失控两族缺陷）、`--check` 滞后即 exit 1、`--self-test` 3 例（链头解析 / 幂等 / 尾注在位）。`make dukou-footer` 把「改页脚 + 重跑第 80/82 槽探针与渲染档案」收成一条命令——页面一改，探针报告页 sha 必失配（fail-closed），此前靠人记得手工补跑。
> - **归档覆盖门禁**：`check_archive_health.py` 增 `--gate` 阻断档（**只拦 T5/T6**；T1b/T2/T3 留在报告面，避免门禁长期常红）；`verify_delivery.py` 挂**第 84 槽「归档覆盖」**（`_SCOPE_CORE` 恒跑 + `EXPECTED_SECTION_NAMES` 声明双登记），`gates.md` 补第 84 条并订正槽数 83→84。verify_delivery.py 属铁律 8 禁擅改清单，**改动已获用户当日明确批准**。
> - **判据可证伪（当场演练）**：临时移出豁免簿 W934 行 ⇒ `--gate` 报 `T5 … 1 号（W934…）` 且 exit 1；恢复后归 0。证明该槽不是常绿装饰。
> - **机器判据**：`gen_version_footer.py --self-test` 3/3；`--gate` 实跑 0 FAIL；门禁段自洽锁 89 段 == 声明 51 段。
> - **验证**：页脚链前插 W1336 后第 80 槽双口径 0 违例、第 82 槽 0 FAIL（探针与渲染档案同批重跑）；`--scope full` 绿。
> - **文件**：见 file-index W1336 段。
> - **状态**：已落地（级联+提交后以 gh run list 为准）。

### W1335（2026-11-27）：归档分卷收口（C 先行 · B 终态）

> **来源**：用户 2026-11-27 指令「按 C 先行、B 终态方案执行，新卷宽度设为 250，旧卷冻结为只读」；方案出自当批只读评估（实测 6+4 个归档卷、两家族零重复、区间缺号 114/99 无人知晓、一级归档 4.7 倍于正本）。
> - **清单面（C）**：新建 `scripts/gen_archive_manifest.py`——扫卷谱系产出 `archive/docs/ARCHIVE-MANIFEST.md`（人读）+ `scripts/output/archive-manifest.json`（机读）；`--check` 判据面 = **卷谱系 / 冻结清单 / 卷宽**（其他归档件体积仅信息面，不受「每批必刷」自锁）。实测登记 2 家族 10 卷。
> - **判据面**：`check_archive_health.py` 增 **T5 覆盖完备性**（台账声明已收官的号必须在正本或某卷找到段）与 **T6 archive/docs 总量 ≤12MB**。T5 首跑抓出 12 号疑点，逐条核实：10 号属台账自述（作废 / 合并段 / 追记 / 在途 / 占位空号），2 号属历史缺口（W934 全仓无段承载、W1088 僵尸行随 W1086 落地）⇒ 建显式豁免簿 `archive/docs/ARCHIVE-T5-EXEMPTIONS.md`（逐条写核实动作），**不放宽判据、不悄悄加白名单**。现势台账 671 号全覆盖（自述豁免 29 + 显式豁免 2）。
> - **分卷面（B）**：`archive_tier2.py` 增 `--range-width 250`（卷界由 `align_boundary` 对齐）+ `--rounds`（单卷宽度受限时连迁多卷）；新卷一律范围命名，命中冻结卷即断言拒绝；两件无范围名 `-tier2.md` 冻结只读。干跑实测：CHANGELOG 一级 991KB ⇒ 迁 W951-W983 入 `CHANGELOG-ARCHIVE-tier2-W951-W983.md`、一级留存 896KB（未落盘·1MB 线尚未触发）。
> - **规范**：文档规范 §11.2 增「二级归档分卷」条款（宽度 / 命名 / manifest / T5·T6 / 豁免簿纪律），W513 原条款逐字保留。
> - **机器判据**：新增 `tests/unit/test_w1335_archive_sharding.py` 7 例（卷界对齐 / 迁出上界截断 / 冻结标注与同号多卷 / T5 三档判定 / 清单过期识别 / 非滚动件体积变化不判过期 / T6 累计）；存量归档域 9 例零回归；ruff 0。
> - **验证**：归档域单测 16 例全过；`gen_archive_manifest --check` 与磁盘一致；`check_archive_health` T5/T6 绿（余 1 项 T2 段目录组行属存量债务）。
> - **处置收尾（自捕缺陷·根修）**：收尾核验发现正本 `ARCHIVE-MANIFEST.md` 被单测污染成「1 段 W5」——根因是两例 manifest 单测只 monkeypatch 了 `ARCH`/`MANIFEST_JSON`，`refresh()` 仍把 tmp 数据写进真实清单。修法：单测同时 patch `MANIFEST_MD` + 增「单测不得污染真实清单」断言（7 例全过）；正本已重建（10 卷 · 冻结 2 卷 · 重复 0）。
> - **文件**：见 file-index W1335 段。
> - **状态**：已落地（级联+提交后以 gh run list 为准）。

### W1334（2026-11-27）：可观测性接入决策（方案 D）+ usage 前置

> **来源**：用户 2026-11-27 指令「按方案 D 执行，先实现 usage 前置逻辑；生成决策文档」。
> - **决策**：观测面走本地零依赖 trace（方案 D），排除 Langfuse Cloud / 自建 Langfuse / 标准 OTel 自建。决定性判据 = 云端留存上限 90 天 < 项目审计硬下限 180 天（Hobby 30 天 · Core $29 档 90 天 · Pro $199 档 3 年，2026-11-26 实取定价），叠加架构方案 v1 裁定 5 与 v2 裁定 5 两次否决付费 APM；依赖体积实测 3 / 15 / 67 包属可接受量级，故非排除理由。
> - **usage 前置（本批施工）**：`openai-compat.ts` 请求侧带 `stream_options.include_usage`（HTTP 400 回退重试一次并去掉该字段）、响应侧 usage 帧与 choices 解耦解析 + 归一（total 缺失以 input+output 兜底）；`types.ts` 增 `TokenUsage` / `StreamEvent{type:"usage"}` / `AgentTurnResult.usage`；`agent-loop.ts` 跨轮累计；`chat.ts` 落「问答 token 用量」结构化日志。口径：未回传记 null 不记 0（沿用 OBS-14「缺样本 ≠ 0 ms」）。
> - **只读接入实证（前序·未改代码）**：`auth_check` True；云端 2026-11-16 删旧路由（SDK 5 `api.trace.list` 抛 AttributeError），langfuse-mcp 0.14.0 的 v2 observations 回退实测 200；stdio 按拟用配置起服 11 工具，`fetch_traces` 等三工具 `isError=None`。
> - **同车安置（他批遗留暂存件·用户授权）**：`TODOS.md`（新文件）+ `STRUCTURE.md` 待办入口行 + `scripts/check_repo_layout.py` 配套 + `HANDOVER.md` 待办单一入口指针，系他方会话「待办单一入口（2026-11-27 用户令）」的暂存件（台账无认领行、无独立版段）；用户 2026-11-27 裁决「四件一并提交并披露」⇒ 随本批入库并于此披露，归属原会话，后续补段由该会话按号序回写。
> - **机器判据**：新增 `server/engine/openai-compat.test.ts` 6 例并登记 `test:server`（请求字段 / usage 帧 / 缺样本不造 0 / total 兜底 / 400 回退 / 与 tool_calls 共存）。
> - **验证**：单测 6/6；`npm run test:server` 159 例 fail 0（155 通过 / 4 跳过：PG 不可达）；`tsc --noEmit` 退出码 0。
> - **报告**：`docs/11-方案报告/设计与架构方案/可观测性接入选型与决策-2026-11-27.md`（§8 单列 5 项未验证项）。
> - **处置收尾（腾窗）**：落段后 CHANGELOG 余量仅 366 字节（261778/262144）⇒ 跑 `archive_segments.py --keep 56 --apply` 迁出 8 段（W1271-W1278）至 `archive/docs/CHANGELOG-ARCHIVE.md`（守恒断言 A1-A5 全过·逐字节未改写）；file-index 同批迁出 8 段（W1271-W1278）至 `archive/docs/file-index-ARCHIVE.md`。迁后 CHANGELOG 216623 字节（余量 45521）、file-index 229636 字节（余量 32508）。
> - **处置收尾（页脚 WARN 清零）**：`site/dukou-engine.html` 页脚版本 W1333→W1334；因页面内容变更使第 80/82 槽「报告/档案陈旧」fail-closed 触发 ⇒ 重跑 `svg_text_contrast_probe.js`（body + graphic 双口径·各 168 页 × 4 态·低对比 0）与 `_w1266_render_legend.py`（判定分布 multi_legend=3 / multi_nolegend=1 / nochart=7 / unknown=6）；两槽复跑 0 FAIL，`dukou-engine` 页脚 WARN 归零。
> - **文件**：见 file-index W1334 段。
> - **状态**：已落地（级联+提交后以 gh run list 为准）。

### W1333（2026-11-26）：A1 交叉引用与 reader 阅读体验


> **来源**：用户 2026-11-26 指令「开始 W1333」，方向经 AskUserQuestion 裁决为「1+2+4」：A1 交叉引用 + reader 阅读体验 + A5 两篇提质。
> - **A1 逐回交叉引用**：新建 `scripts/w1333_a1_crossref.py`（--dry/--apply/--check 三模式·幂等标记 `<!-- w1333-crossref -->`）——按 chapter-meta（num / main_characters）给 100 回各注入 1 条「相邻回 + 人物主文件」关联行（别名表：观世音→观音、如来佛祖→如来；外传/深化不作主链接），**0 死链**；reader 重生成后自动改写为站内链接。
> - **reader 阅读体验**：`build_reader.py` 的 `fold_sections` 让**首个折叠（剧情梗概）默认 open**——此前回目页三个折叠全收起、首屏可读内容为零；其余折叠保持渐进披露。重生成 636 页 + 内联 CSS 635 页重同步 + nav/analytics 补注入；第 62 槽 reader 完整性 0 FAIL、reader/RSS 新鲜度 0 FAIL。
> - **A5 两篇提质**：`西游与禅宗公案专题.md` 修复 2 条坏引文（第1回多余 `”`、第3回引号错乱）并按原文补全；`佛道思想.md` 新增「禅宗公案读法 vs 内丹修炼次第」对照节（复用篇首已核验的第1/78/85 回引文）。引文核验 5+3 条命中率 100%；术语门禁新违规 0；元信息块 v2 通过。
> - **同批根修（E-322·收官链拦下）**：`w1167_analytics_inject.py` 的幂等更新分支以 `</head>` 为右端整段重建 ⇒ 同区注入块（W1284 `label-contrast.js` / W1331 `chart-portrait <style>`）被洗掉 **168 页**（触发面=`build_reader.py` 收尾自动全站重跑注入器）⇒ 第 80 槽 graphic 违例 **0 → 1679**。改为**只按本块行形态收敛**，并按 HEAD 原文加法式补回 129 页；判据 = `--dry-run` 改动 0 / `--check` PASS + 单测 2 例（邻居保留 / 只换本块）。
> - **机器判据**：单测 8 例（A1 六例 + 注入器保留与幂等两例）。
> - **文件**：见 file-index W1333 段。
> - **状态**：已落地（级联+提交后以 gh run list 为准）。

### W1332（2026-11-26）：暗色对比度专项与公共层补丁


> **来源**：用户 2026-11-26 指令「开始 W1332 并处理遗留总账中的 L-13 至 L-15 项」；L-13 深度与 --accent-soft 处置经 AskUserQuestion 裁决（判据自动化+违例即修 / 保留声明例外）。
> - **L-13 判据自动化**：新建 `scripts/_w1332_dark_contrast_probe.py`——夜读态（localStorage 预置 dark）逐页量「HTML 文字 vs 逐层 alpha 合成背景」与「SVG 形状可见性」，243 页（根页+data+en+reader 抽样）。判据自纠三项：C 项（SVG 文字覆盖图形）简化几何实测误报 2/2 页（截图证伪）⇒ 删除并声明由第 80 槽 graphic 口径承担；背景基色改 body 优先 + 支持 `color(srgb …)`（修顶栏半透明背景误报）；无 class 形状与 fill alpha ≤0.2 判装饰层豁免。
> - **L-13 修复**：基线 FAIL 46 页（HTML 文字 194 条 + 不可见形状 32 条）→ **FAIL 0**（四轮·OK 240 / WARN 3）。真缺陷五族：深底浅字令牌误用 **110 块 / 83 页**（`background: var(--dark); color: var(--paper-warm)`——`--paper-warm` 暗色重定向到深色 ⇒ 深底深字，cave-estate 表头实测 1.11）→ `--dark-text`；浅米硬编码表头底 6 页 → `--surface-sunken`；footer 用 `--ink` 当深底 2 页 → `--dark`；danmaku-stage 硬编码亮底 2 页 → `--paper`；`--rebel` 暗色补 `#D96C5C`。① 标签越出 svg 边界裁决设计容差；③ 半透明底由第 80 槽覆盖（168 页 0 违例）。
> - **L-14 公共层**：`system.css` 全局屏蔽原生 details marker（reader 635 页双三角根修·自定义 ▸ 不受影响）；`tokens.css` 补 `--shadow-2` 亮（`rgba(35,32,26,.12)`）/暗（`rgba(0,0,0,.45)`）两态；`inline_css.py --force` 重分发 637 页。
> - **L-15 视觉零散**：index `.ask-form button` 衬线 → `--font-sans`；index `nav-brand` 补 `aria-current="page"`；rum-viewer / visit-viewer 接入 `system.css`；`--accent-soft` 用户裁决保留并声明例外（3,286 处消费面不收敛）。
> - **机器判据**：单测 8 例（summary 屏蔽 / 阴影两态 / aria-current / 公共壳 / 深底块令牌 / 修复器幂等与 INLINED 副本跳过 / 探针判据负样本 / CLI）；修复器幂等（重跑零变化）。
> - **验证**：夜读态探针五轮（46→15→10→0→0）；第 80 槽 SVG 对比度 168 页 0 违例；单测 8 通过。
> - **文件**：见 file-index W1332 段。
> - **状态**：已落地（级联+提交后以 gh run list 为准）。

### W1331（2026-11-26）：竖版图表专项与 T112 视觉遗留核验


> **来源**：用户 2026-11-26 指令「开始 V4 竖版图表专项和 T112 视觉遗留核验」。
> - **竖版图表专项**：新建双视口图表探针（`_w1331_chart_portrait_probe.py`：载体/压缩比/有效字号/标签越界/不可达裁切五类事实，file:// 实测 165 页）。375 竖屏基线 OK 54 / WARN 64 / **FAIL 47**——159 个 svg 被压到有效字号 <8px（最甚 2.7px），根因三类：固定 viewBox 的 svg 缺窄屏 min-width（容器有滚动条但无内容可滚·40 页）、svg 直挂 section 无滚动轴、绘制层标签越出 svg 边界。
> - **根修**：`_w1331_chart_portrait_fix.py` 对 81 页注入窄屏 `@media` 块（222 条规则·`data-w1331="1"` 幂等标记）：`min-width` = viewBox 宽（保 1:1 + 横向可滚而非压缩，DESIGN §6.4 同源）、父容器不可滚时 `*:has(> 选择器)` 精确补 `overflow-x:auto`、越界标签 `overflow:visible`。重建块继承旧规则（分阶段修复不丢前一次成果）；8–9.5px 微压缩只记 WARN 不强行加宽（避免给运行时重设 viewBox 的响应式小图强加 min-width）。
> - **实测结果**：**375：OK 109 / WARN 56 / FAIL 0；320：OK 100 / WARN 65 / FAIL 0**（WARN = 标签越出 svg 边界但容器可滚可达 + 8–9.5px 响应式小图）。最大修复项：journey-route #timeline 3.1px→10px、character-appearance #chart-timeline 3.2px→10px、concept-device #prismSvg 2.7px→10px。
> - **T112 视觉遗留核验**：`_w1331_t112_verify.py` 对 T112 报告 §9.2/§9.4/§9.6 共 24 项做机器核验（S 静态可复算 / R 引用探针 / M 未自动化）：**已清偿 10 / 部分 3 / 存续 6 / 未核验 4 / 不属视觉面 1**。已清偿含徽标对比度、暗色簇间连线、SVG 文字越出视口、表格横滚、980px 图表、3D 固定高、FAB 遮挡、数据位衬线、hero 巨号、移动端不可达裁切；存续项按族归并登记遗留总账 **L-13～L-15**（图表绘制层+暗色对比度 / 公共层 summary 双三角+--shadow-2 / 视觉零散四项）。
> - **机器判据**：单测 8 例（build_block 压缩/越界/缺锚点分支、真实页注入恰一块、规则与 viewBox 对账、grade 负样本、CLI smoke）；注入器 `--dry/--report/--revert` 三模式。
> - **验证**：全量探针 375/320 双视口 FAIL 0；`_w1331_chart_portrait_report_375.json`/`_320.json` 入库存证；T112 核验 JSON 入库。
> - **文件**：见 file-index W1331 段。
> - **状态**：已落地（级联+提交后以 gh run list 为准）。

### W1330（2026-11-26）：V1 交互二期

> **来源**：用户 2026-11-26 指令「按新纪律继续处理下一批」——V1 dashboard 交互二期。
> - **搜索深链**：看板状态扩为 `#cat=…&q=…`（activateCategory + syncHash + readHashState + applyHashState），搜索输入防抖后同步地址，hashchange 可回退/分享；file:// 禁 replaceState 时 try/catch 静默降级。
> - **键盘**：按 `/` 聚焦专题搜索（INPUT/TEXTAREA/contentEditable 内不劫持）；Esc 清空与方向键选择沿用。
> - **最近浏览**：新增 site/static/js/recent.js 并注入 90 个 site/data 内容页（MARK 幂等）；写 localStorage `xy-recent-pages`（最多 5 条·去重置顶·仅 data/*.html 形态）；看板渲染 chips，空列表隐藏；隐私模式/配额满静默。标题取「副段」（站点名段跳过），避免工具页只剩「详解西游记」。
> - **回到顶部**：滚动 600px 后出现 44px 圆形按钮，reduced-motion 下瞬时跳转，滚动监听 passive。
> - **根修**：初版在 allCardsIndex/resultsBox 定义前调用 applyHashState ⇒ 浏览器实测 TDZ ReferenceError（搜索/键盘全链失效）⇒ 初始化顺序改为末尾执行，复测 console 0 error。
> - **机器判据**：单测 7 例（90 页各引用恰一次 / 看板不载 recent.js / 交互 token 在位 / 注入幂等 / 缺 body fail-closed）+ 注入器 --check。
> - **验证**：浏览器实测四项（最近浏览命中内容页、#q=妖怪 3 卡、/ 聚焦 topic-search、回顶 scrollY=0）；375 探针 dashboard 0 FAIL / 0 裁切；CSP 916 哈希零漂移；check_structure 873 文件通过。
> - **文件**：见 file-index W1330 段。
> - **状态**：已落地（级联+提交后以 gh run list 为准）。

### W1329（2026-11-26）：V4 移动端回归与裁切根修

> **来源**：用户 2026-11-26 指令「按新纪律继续处理下一批」——V4 移动端回归（375/320 全量复跑）。
> - **探针复跑**：mobile_viewport_probe 全量 270 页（ZH + EN + reader 抽样）× 375/320 两档，以及 EN 148 页单档；修复后两档均 FAIL 0 / 溢出 0。
> - **裁切根修（8 页）**：wukong-tangseng-benchmark 私有 `.chart-block{overflow:hidden}` 覆盖共享移动横滚模式；en/text-evolution 两张定宽图（min-width 800）缺滚动容器 ⇒ 加 `.chart-scroll`；en/pilgrim-team-dynamic-network 五列阶段卡在窄屏挤压 ⇒ 2 列/1 列降级；en/hardship-heatmap 的条形卡被表格 min-content 撑宽 ⇒ min-width:0 + 横滚；en/global-pattern 双列卡在 ≤480 降单列；en/cross-time-danmaku 与 en/social-media 的 notice code 长路径断行。
> - **触摸线**：rum-viewer（未接公共壳的独立页）补 `.nav-item` 24px 双维下限（EN 标签实测 18px）。
> - **机器判据**：第 64 槽新增 B5/B6——375/320 报告 clipped 页数必须为 0（内容被 overflow 裁掉＝不可达，不能以「可横滚」名义蒙混）。
> - **报告**：mobile_viewport_report.json（375·270 页）、mobile_viewport_report_320.json（320·270 页）、mobile_viewport_report_en.json（EN·148 页）全部重生成并入库。
> - **验证**：第 64 槽 0 违规（契约 7 项）· 自测 7/7 · check_structure 873 文件通过 · lint_links 0 broken。
> - **文件**：见 file-index W1329 段。
> - **状态**：已落地（级联+提交后以 gh run list 为准）。

### W1328（2026-11-26）：V3 收尾与看板深链

> **来源**：用户 2026-11-26 指令「按新纪律继续处理下一批」（1+3+4 组合）——V3 收尾 + 看板交互增强 + 治理计数收口。
> - **V3 收尾**：新增文件名族规则（关系网络 17 / 人物与文风 6 / 地理与行程 5 / 叙事与文本 5 / 专题图谱 5 / 交互工具与导航 2），非看板页 100% 归族；连同 W1327 的 45 页，全站 85 个 site/data 内容页均有页脚同类入口（5 个数据中枢工具页无 footer·反向锁死）。
> - **footer 形态升级**：关联链接统一 class=footer-related-link（计数判据不惧标签链接混入）；看板类别标签成为 ../dashboard.html#cat=<类别> 深链。
> - **看板交互**：新增 #cat= 深链解析（activateCategory / syncHash / readHashCategory + hashchange）——页脚一键直达对应类别；file:// 禁 replaceState 时 try/catch 静默降级。
> - **补页脚**：glossary / poetry-density / story-timeline 三页补齐标准 site-footer（原先只有裸反馈链接），版式与其余 pages 一致。
> - **计数勘正**：A-L 静态标签 12 → 8（4 张 A-L 卡在顶部 KPI 概览、不在专题网格）；新增「筛选标签计数 ≡ 网格实卡」机器判据（同时锁住 W1327 的 51→41）。
> - **治理收口**：HANDOVER V2/V3 标「无待办」；遗留总账未清偿 12 → 0（全部已闭合）。
> - **验证**：check PASS（90 页守恒 = 85 注入 + 5 跳过；死链 0 / 自页 0 / 分组不一致 0 / 杂散 0 / 标签计数漂移 0）；单测 9 例；浏览器实测深链（URL #cat=a-l、tab 选中、网格 8 张 A-L）；CSP 零漂移；lint_links 24980 链接 0 broken。
> - **文件**：见 file-index W1328 段。
> - **状态**：已落地（级联+提交后以 gh run list 为准）。

### W1327（2026-11-25）：页脚同类关联链接补全

> **来源**：
> - **T1**：用户旅程 V3 第 3 项——页脚关联链接补全与智能推荐：把读完一页后的死路改成同类三页可继续。
> - **推荐口径**：唯一来源为 site/dashboard.html 专题卡片（href + data-category，50 张站内卡），同类别按看板顺序循环取后 3 页、自页排除；类别成员不足 4 时取 n-1 条（Q+ 2 页互链 1 条）。
> - **注入形态**：目标页 `<footer class="site-footer">` 内追加一组 `<nav class="footer-related">`（复用既有 .site-footer nav 与 .footer-meta 样式），零新增 CSS、零新增内联脚本、零外域，file:// 直开不变。
> - **覆盖**：看板 50 张站内卡 = 45 页注入 + 5 个数据中枢工具页（整页无 site-footer，显式 NO_FOOTER 集并由 check 反向锁死：仍有 footer 或出现 MARK 即红）；其余 site/data 内容页不在看板卡上，无类别事实源，不纳入本批口径。
> - **源数据勘正**：看板专题区静态文案「51 个专题页 / 全部 51」与实际 41 张网格卡不符（全页站内卡 50 = 41 专题网格 + 4 KPI 概览 + 5 数据中枢；运行时 updateCounts 只自愈标签页数字，静态文案与无 JS 场景不自愈），本批同步订正为 41。
> - **W1325 遗留根修**：3 篇归档正本 41 条相对链接按迁移后深度重写（lint_links 默认排除 archive/，故 W1325 的 0 broken 结论不覆盖该面）；`docs/10-方法论沉淀/README.md` 三 skill 行补「已归档·指针」标。
> - **对抗式审查（W1327 已派发）**：审查发现并本批根修 4 项——① 初版写盘未带 newline 致 45 页转 CRLF（已归一，check 增行尾 LF 判据）；② 新脚本四面无引用（补单测 7 例）；③ 看板静态「51」失实（实测网格 41 卡）；④ W1325 归档内链 41 条失效（已按新深度重写）。事实澄清：Q+ 仅 2 页互链 1 条、Q++ 3 页互链 2 条，故 45 页并非每页 3 条（合计 128 条）。
> - **验证（全绿）**：w1327_related_links.py --check PASS（覆盖 50·死链 0·自页 0·分类不一致 0·杂散 0）；二次 --apply 实际改动 0（幂等）；单测 7 例；归档内链 41/41 可达；lint_links 24807 链接 0 broken；check_structure 873 文件通过。
> - **状态**：已落地（级联+提交后以 gh run list 为准）。
> - **文件**：见 file-index W1327 段。

### W1326（2026-11-25）：两轮推送 CI 等待纪律（E-321 入坑表 + 流水线第 6 步/§五）

> **来源**：用户 2026-11-25 指令「把这条教训写进 pitfalls/流水线」——W1324+W1325 两轮推送实操暴露「首轮 CI 被并发取消 + 回填笔 CI 红无法 rerun 转绿」。
>
> - **坑表**：git 主题新增 E-321（根因/判据/纪律）+ 归档全文；pitfalls 总 426→427、git 40→41，标记面 23 处跟随。
>
> - **流水线**：§二 第 6 步新增「两轮推送的 CI 等待纪律」；§五 失败模式速查新增一行。
>
> - **验证**：verify_delivery 全量；`test_cascade_handover_rotate` 3/3；E-321 计数由 stats.py 实算。
>
> - **文件**：见 file-index W1326 段。
>
> - **状态**：教训入库（无代码/页面改动；无新增豁免）。
### W1325（2026-11-25）：方法论审查 P0-P3 全量处置（5 件物理归档/合并 + 全目录指针与计数对齐）

> **来源**：用户 2026-11-25 指令「先把 P0 P1 P2 P3 的问题处理完」——承接 W1324 方法论审查报告的 106 条发现（P0 2 / P1 32 / P2 45 / P3 27）。
>
> - **结构件（物理归档/合并）**：`三skill闭环` / `记忆研究理论框架应用方法论` / `双索引可追溯改造` / `agent-web技术栈迁移评估` 4 篇迁 `archive/docs/复盘报告/`，原路径保留指针；`dispatching-parallel-agents四subagent并行模式` 并入 `多Agent干扰治理与touches纪律` §四之三；`docs/INDEX.md`、`docs/10-方法论沉淀/README.md`、站内搜索索引、RAG 索引同步。
>
> - **P0 根修**：① 三skill 退役后仍给执行指令 → 物理归档 + 顶部/§五/§七/§九 封条「历史记录·勿执行」；② 前端SOP「样式生效已覆盖」失实 → 改为「仅渲染基线间接覆盖，无专门判据」，删除 archived 脚本现役路径与 AGENTS §5.2 悬空锚点。
>
> - **P1 指针/路径/计数**：11 篇 AGENTS 章节锚统一改指「§一 铁律 2/14 + §三 常用命令」；`reserve_w.py` 入流水线第 1 步、`release_prep --check-spec` 命令订正、preflight「三轨」→ 现役 1–7 项核验；`text-search.html` → `dataset/text-search.json`；43槽/48段、87页/522行、450行、W700+、门禁 N4、第 45/48 槽全部改指针或实测值；`user_profile.md`/本机路径改仓内镜像说明。
>
> - **P2/P3**：头五要素补齐 / 重复段指针化 / 模糊措辞与行号清理 / 白屏计数与脚本状态对齐 / 素材案例边界标注 / 幂等验证命令 / README 编号说明 / DRL RunCommand 与行号引用订正。
>
> - **验证**：`verify_delivery.py` 全量核心全绿（5 项辅助 WARN 不阻断）；`lint_links` 0 broken；`generate_csp.py --check` 0 漂移；`docs_index.py` / `_gen_search_index.py` / `gen_folder_docs.py --refresh` 已重建；`stats.py --w W1325` 刷新 report_docs 255→256；RAG BM25 本地缓存重建（`rag_index.json` 为 gitignored 缓存）。
>
> - **不做**：不新增豁免/白名单/基线；不修改 `docs/11-方案报告/` 审查报告正文（W1324 保持审查时点快照）。
>
> - **文件**：见 file-index W1325 段。
>
> - **状态**：P0/P1/P2/P3 按报告主题全部处置；结构件按用户裁决物理归档。
### W1324（2026-11-25）：方法论沉淀文档审查（28 篇只读评审 + 报告落位）

> **来源**：用户 2026-11-25 指令「按这个方案生成报告」——对 `docs/10-方法论沉淀/` 全量方法论文档做一次结构与论证质量评审（HOTL document-review 通用 rubric + `docs/12-提示词库/05-项目审查任务书.md` 取证要求）。
>
> - **执行（只读审计·零被审文档改动）**：28 个 md（含 README，4,272 行 / 296,637 B）分四组评审；主会话复核 P0 2/2、P1 20/32（其余标 B），并纠正子代理 1 处证据误判（`ci.yml` 实含 `check_js_syntax.py --all`）。
>
> - **结论**：保留 7 / 需修订 16 / 建议合并 1 / 建议归档 4；P0 2（三skill 退役后仍给执行指令；前端SOP「样式生效」覆盖声明失实）· P1 32 · P2 45 · P3 27；系统性问题=W1279 地图化后 11/28 篇 AGENTS 章节锚悬空 + 退役工具按现役描述 + 计数裸写（43槽/48段、87页/522行、450行、W700+ 等）。
>
> - **落位**：报告入 [方法论审查报告-2026-11-25.md](docs/11-方案报告/审查与评审/方法论审查报告-2026-11-25.md)；[docs/11-方案报告/README.md](docs/11-方案报告/README.md) §一登记（23→24 篇·全局序号 152）。
>
> - **不做**：不改 `docs/10-方法论沉淀/` 任何文件；指针回扫/归档/计数实体化另批施工（报告 §七给建议批次主题，实际以对账表认领为准）。
>
> - **文件**：见 file-index W1324 段。
>
> - **状态**：审查报告 V1.0（只读·零被审文档改动）；修复建议待分批立项。
### W1323（2026-11-25）：八十一难难度热力图深化（V2 余项·五阶段难度地形）

> **来源**：HANDOVER「二、下一步方向」V2 可视化深化余项——八十一难难度热力图深化（W1320 对账核验后唯一未完成项）；用户 2026-11-25 指令「开 W1323」执行。
>
> - **取证（先看现状）**：页面已有 ① 四维矩阵 ② 四维分布 ③ 交叉洞察 ④ 联动清单，但 `stage`（前传/初段/中段/后段/终段）字段**从未进入任何分析或视图**——章节排序只用了 `chNum`，五阶段聚合是空白面。
>
> - **执行（新增板块）**：① 页内新增「五阶段难度地形」区块——五张阶段卡（阶段名 / 均分 / 难度条 / 难数·极难数·求助均次）+ 一张聚合表（阶段 / 回目范围 / 难数 / 均分 / 极难 / 平均求助 / 最高分难）+ 一段**运行时生成**的演进洞察；② 中英双页同步（EN 页无清单板块，新板块编号 ④；中文页清单顺延为 ⑤）；③ 所有数值由 `EMBEDDED_DATA`（含 `window.__hmData` 覆写面）实时计算，**不写死任何数字**——避免静态文案随数据漂移；④ 难度条用 `--ink-soft` 填充、峰值卡仅 1px accent 边框，不触碰第 49 槽朱砂实底判据；无新增动画，动效契约不动。
>
> - **门禁报错与根修（第 76 槽棘轮）**：首版新增十个 `.stage-*` 类名 ⇒ 公共层覆盖率 11.7% < 下限 11.8% 判红（口径＝公共层类 / 全站使用类）。修法不抬阈值：卡片复用 `.stat-card`、内部改用 header/strong/small 元素与 `data-*` 属性选择器，**零新增类名** ⇒ 棘轮保持原值。
>
> - **实测结果（file:// 直开）**：中英双页各渲染 5 卡 / 5 行，峰值卡唯一；洞察输出「后段均分 6.9，为五段最高；终段降至 3.8」；除字体 file:// CORS（既有环境行为）外零 console error；热力图 324 格照常渲染。
>
> - **验证**：check_chart_data 239 页 FAIL 0；check_chart_degrade 237 页违例 0；check_chart_content_completeness 基线外新增 0；a11y_audit 全站 P0=0 / P1=0（第 14 槽全规则锁维持）；generate_csp 已重算并 --check 零漂移；第 76 槽公共层覆盖率维持基线（零新增类名）。
>
> - **不做**：不新增图表类型（避免图表词表与图例判据的口径扩张）；不触碰四维矩阵与既有洞察文案；不做内容扩容（冻结裁决不受影响）。
>
> - **文件**：见 file-index W1323 段。
>
> - **状态**：V2 余项收口（判据零放宽·无新增豁免）。
### W1322（2026-11-25）：a11y P1 清零与全规则 P1 锁（隐式 label 假阳性根修 + 焦点可见 + 面板语义）

> **来源**：用户 2026-11-25 指令「三个都做」经实况取证后的可执行项（可访问性门禁核验批）。另两项（记录对账 / Web Agent 评估）经实读证据确认已由既有机制覆盖，本批不重复立项——证据与结论见 HANDOVER 注记。
>
> - **取证（先证后改）**：a11y_audit.py 全站 875 页实测 P0=0、P1=12，四类：E2-23 四条 / E2-4 六条 / E2-1 一条 / E2-12 一条；而第 14 槽只解析 summary.E2-2（对比度）⇒ 其余 39 条规则的 P1 **没有任何阻断位**，12 条长期只出现在报告里。
>
> - **根修①（检测器假阳性）**：E2-23 只认 `label[for]` / aria-label / aria-labelledby / title，未认 WCAG 3.3.2 认可的**隐式包裹**（控件位于 `<label>` 内）⇒ 81-hardships 与 relationships 中英四页共四条 P1 全属误判（页面本就合规）。新增 `_implicit_label_lines()`：按 label 块取**首个**可标注后代（符合「一个 label 只标注一个控件」）⇒ 假阳性清零且不放过真缺 label 的控件。单测五例（正例三 + 负例二）。
>
> - **修②（真实焦点可见）**：天庭 / 妖怪 / 阴司三个关系网络页（中英共六页）`.node-circle:focus { outline:none }` 无替代 ⇒ 拆 hover 与 focus-visible 两态，focus-visible 补 2px 实心 outline + offset。节点本有 tabindex=0 与 keydown ⇒ 键盘用户真实受益，不是为过检而写死样式。
>
> - **修③（面板语义）**：81 难难度热力图的 `#hardship-detail` 是页内非模态详情块（有独立关闭按钮 + ESC 关闭 + 无遮罩），却标 `role=dialog` ⇒ 改为 `role=region` + `aria-live=polite`（内容更新可被读屏播报），同批消 E2-1 与 E2-12 两条 P1。
>
> - **机器判据（语义强化·W1322 锁）**：第 14 槽新增「全 40 条规则 P1 合计=0」断言（原 E2-2 P0+P1 判据保留）⇒ P1 回归即红；P2/P3 仍不阻断，判据不放宽、无新增豁免。
>
> - **验证**：a11y_audit 全站 875 页 P0=0 / P1=0；test_a11y_audit.py 58 passed（新增五例）；收官链全量与推送判据见 pre_push_gate。
>
> - **不做**：P2/P3 存量（5768 / 6854）不清零——不属 P1 阻断面，避免巨批；检测器其余判据不动。
>
> - **文件**：见 file-index W1322 段。
>
> - **状态**：a11y P1 清零并上锁（判据加严·无豁免/无放宽）。
### W1321（2026-11-25）：巨批分笔与多推送固化（选项①）+ safe_commit 索引态分歧机器判据

> **来源**：W1320 Backlog 对账批登记的常设项「批级多笔推送」；用户 2026-11-25 指令「按推荐处置固化该常设项」= 采纳选项①（接受现状并固化进批次流程），并同批根治 W1320 暴露的「索引态捕获旧页」风险。
>
> - **固化①（流程面）**：`docs/10-方法论沉淀/批次交付流水线.md` §二 第 6 步新增三条硬规则——(a) 巨批分笔：容量 #7 越线时按目录分组拆笔、每笔 ≤500、**每笔必须自洽**（页面与探针/渲染档案不得跨笔拆开，第 80/82 槽按页 sha fail-closed）；(b) 逐笔推送 + 临时 worktree：一次推送只带 1 笔，首笔在主线不干净时 `git worktree add` 后在临时树推；(c) 索引态提交前须无「暂存后改写」分歧。§五 失败模式速查新增两条（#7 越线处置、探针陈旧的分笔根因）。
>
> - **固化②（登记面订正）**：第 7 步原断言「同批第二笔回填会被物理拦下 ⇒ 同批回填物理不可行」与 W1318/W1319/W1320 连续三次实证相反 ⇒ 订正为「回填笔在首笔推送后即 1 笔领先、闸门放行；物理不可行仅指同一次 push 带两笔」。
>
> - **机器判据（根治）**：`safe_commit` 新增 `_index_worktree_divergence()`——索引态提交（`--expect-spec` 无 pathspec）前扫 `git status`，X∈{M,A,R,C} 且 Y∈{M,D} 即拒绝并列出分歧件；W1320 实证：dukou 版本页脚在 `git add` 之后被重写，首笔捕获旧页 ⇒ 该笔单独检出时第 80/82 槽判红、只能本地重建。单测新增 2 例（拒绝 + 重新 add 后放行·含 blob 内容断言），全套 9 passed。
>
> - **不做**：选项②（单笔内分块 + 探针免刷新压回 1 笔）不再立项——收益是 CI 轮数，成本是验收面等价性证明，判为不划算。
>
> - **验证**：test_safe_commit_expect_spec.py 9 passed；verify_delivery / pytest 全量见收官链；本批无站点页面内容改动（版本面页脚除外），探针刷新随收官链。
>
> - **文件**：见 file-index W1321 段。
>
> - **状态**：常设项结清（转已处置 [x]）；判据加严（新增拒绝路径·无豁免/无放宽）。
### W1320（2026-11-25）：Backlog 对账批（W1021 触发器 35 批点名·遗留 7 条实况核验 + 候选陈旧清理）

> **来源**：`check_backlog_review.py` 机械点名——距上次对账（W1284）已 **35 批 ≥ 阈值 25**；W1320 开工 preflight 同报。用户 2026-11-25 指令「好的，执行吧」= 批准开对账批（判据=git 与测试实况，非条目自述）。
>
> - **取证与判定**：对 HANDOVER「四、待办」的 W1288/W1289 两块遗留逐条拿 git / 门禁 / 现势实跑核——① 复盘触发器：W1311（T140 复盘批）已清偿，现势 1 天 / 8 批 / 15 提交未触发；② 计数链 N1-N5：W1319 preflight 实读全一致（板块篇数 {1:100,2:215,3:209,4:42,5:19,6:44} / verify 88 段 / 83 槽 / 426 坑 / 启动 Prompt 三计数）；③ 坑表写窗：W1290 六主题拆分结构性解除（C7 逐文件 ≤262144 B·现最大 flow-collab.md 126,068 B）；④ `assets/game/`：W1303 纳入版本管理（`.git/info/exclude` 内有解除注记）；⑤ 探针刷新前置：`batch_closeout` 的 refresh 步已在 gate 之前（W1319 收官链实证）。⇒ 6 条结清。
>
> - **唯一未结转常设项**：W1287「下一批压到 1 笔」——W1318 实推 3 笔、W1319 实推 4 笔；根因＝容量 #7「单笔 <500 文件」× 637 页共享 CSS 重同步必然分笔，push-gate 的「每次推送 ≤1 笔」已物理兜底 ⇒ 批级多笔为已知代价，登记为 [ ] 常设项并给两条处置候选（接受并固化 / 立项研究分块提交）。
>
> - **§二 候选陈旧清理**：V2 地理 3D（journey-geo-3d.html）与人物关系动态网络（character-relationship-3d.html）、V3 标签云（tag-cloud.html）、手搓绕过级联治理批（W982 落地 + W989 收尾）均已落地 ⇒ 从候选移除；E9 治理经验移植保留（外部仓动作·需用户授权）。
>
> - **他方面**：W1240/W1241 两条他方会话行已随台账行窗归档，正本无滞留告警。
>
> - **触发器归零**：台账本批行状态列写入事件 token「Backlog 对账已执行」⇒ 下次数点从 W1320 起算。
>
> - **验证**：check_backlog_review 点名前 35 批 → 本批后归零；verify_delivery / pytest 见收官链；本批零代码/零样式改动（纯文档与登记面）。
>
> - **文件**：见 file-index W1320 段。
>
> - **状态**：对账完成（6 结 1 常设）；判据/阈值零变更；单笔提交（文件数远小于 #7 上限）。
### W1319（2026-11-25）：CSS 源瘦身（零消费规则与死声明清零·共享基线块余量 48→3,277 B）+ DESIGN Hero 规格更正

> **来源**：W1318 收官登记「#2b 余量仅 48 B ⇒ 下一批须二选一：CSS 源瘦身（推荐）或由用户裁决机制线校准」；用户 2026-11-25 指令「好的，执行吧」= 批准做 CSS 源瘦身（不动机制线·不新增豁免·不调阈值）。
>
> - **取证（零消费判定）**：对 875 个 site HTML（剔除共享 `<style>` 块后只看标记面）+ 26 个 site JS + scripts/ 生成器全扫，按「选择器内任一 class/id 记号词边界零命中且无同义选择器可匹配」判零消费。命中 16 条规则（1,576 B 源）：`.text-mono` / `.text-xs` / `.text-faint` / `.text-accent`、`.badge-{accent,blue,gold,green}`、`.link-ink`(含 :hover)、`.btn-primary`(含 :hover)、`.series-shape`、`text.heat-value`、`svg .label-strong`、`text.value-label`(含 `.is-strong`)；另检出跨文件完全重复块（tokens.css 与 system.css 各一份 W1261 暗色序列映射 8 条）、同选择器后段覆盖的死声明（`.hero` 双层、`.chart-tooltip` 首块、`svg text` font-family）、同一选择器表内重复项 2 处。
>
> - **修法（只删已证无消费者的字节·判据零放宽）**：① 16 条零消费规则删除；② hero 双层合单——tokens 覆写层（`.hero` / `.hero::after`）与 system 基础层删除，定义收敛到 system.css W1261 节单处（position/overflow 并入，逐属性与旧级联终值等值）；③ `.chart-tooltip` 首块 6 条被后块 100% 覆盖的死声明删除（布局/动效位保留）；④ `svg text` 的 font-family 死声明、tick-text 选择器表重复项、system 侧 W1261 暗色映射重复块删除；⑤ `.value-label` 死选择器与 `.is-strong` 死规则删除（`.data-label` 有效选择器保留）。机制线、阈值、白名单、压缩算法均未改。
>
> - **结果**：共享基线块 57,296 → **54,067 B**（52.80 KiB·机制线 57,344 B·余量 48 B → **3,277 B**）；637 页重同步；check_inlined_css 内联 634 页 min 54,041 B（≥20,000）；check_structure 873 文件 / 1966 style 块括号平衡通过；抽样渲染（dukou-engine / reader ch001 / dashboard / en-dashboard）零 console error，`.hero` / `.chart-tooltip` / `svg text` 计算样式与旧级联同值。
>
> - **文档同步**：DESIGN.md §3.3 Hero 规格由「135deg 三色渐变 + 径向光晕」更正为现役「玄墨纯色 + 水墨山形图·无光晕」（旧文与 W334/W1261 已落地事实相反，且其描述的空 `::after` 规则本批删除）；§4A.8 现役实测重算（内联 637 页 / 三口径字节 / 共享块 54,067 B·余量 3,277 B）。
>
> - **零消费证据边界**：`.btn-primary` / `.badge-*` 仅出现在 v2/v3 方案报告与样板 BRIEF（历史规格），现役 875 页标记面 0 消费；如后续迁移需要按 DESIGN 重新新增，不以保留死规则代替。
>
> - **验证**：pytest 全量见收官链；verify_delivery 全量见收官链；容量 #2b 0 越线（#7 仅未提交暂态，两笔提交后清零）。
>
> - **文件**：见 file-index W1319 段（site/reader 634 件按目录分组登记）。
>
> - **状态**：容量 #2b 余量 48 B → 3,277 B；判据/机制线/白名单零变更；两笔提交（457 + 210 件）绕 #7 <500。
### W1318（2026-11-25）：容量 #2b 治本（共享 CSS 无损压缩 + 全站重同步）+ 测试隔离缺陷根修

> **来源**：用户 2026-11-25 指令「继续容量软线治理」并裁决「两个都做」——对象①容量 #2b 共享基线块机制线（67.29 KB > 56 KB 越线）；对象②W1315 连带发现/W1317 实证的 batch_closeout 测试隔离缺陷（pytest 会真实回填本仓台账）。
>
> - **取证①（#2b 根因）**：共享基线块 = tokens.css + system.css 剥注释副本（68,902 B/67.29 KiB）；W1224 设线时约 55 KB，此后设计系统增长 12 KB 未同步瘦身。全站 637 个内联页（634 reader + dukou-engine + _template + _shell）同块复制。
>
> - **修法①（无损压缩 + 全站重同步）**：`inline_css.py` 新增 `minify()`——字符串段原样保留（tokens.css 含 'rgb(192, 57, 43)' 类字符串令牌），仅对代码段做 8 类等价变换（换行折叠/连续空白/`{ } ; ,` 两侧/`;}`/`:` 后/`>` 两侧/前导零/`!important`）+ 无空白 url 去引号；并补 `url(static/` 前缀替换形态（去引号后原规则失配会致子目录页字体 404）。637 页重同步：块 68,902 → 57,296 B（55.95 KiB·余量 48 B），#2b 转绿。
>
> - **修法②（测试隔离根修）**：`batch_closeout._apply_backfill` 原用 `_sp.run` 直连子进程 ⇒ 单测 mock 不住 `bc.run` ⇒ `bc.main()` 会真实回填本仓台账（W1317 收官因此多出两笔提交）。改走可注入 `run()` + 非零 rc 告警；新增回归测试（subprocess.run 换成抛错桩，退回直连即红）。
>
> - **连带收益**：#1 单页 HTML 最大 448,093 → 436,487 B、软线越线 9 → 7 页；#3 全站 HTML 79.44 → 72.39 MB（−7.05 MB）；#2 页特有最大 49.53 KB 不变。
>
> - **验证**：check_inlined_css 通过（内联 634 · min 57,267B ≥ 20,000 · 特征全过）；capacity #2b 0 越线（#7 仅因未提交暂态，分两笔提交后清零）；inline_css 单页实测字体 url 前缀正确（无无前缀 static/ 残留）；pytest 全量见收官链；verify_delivery 全量见收官链。
>
> - **残余风险（登记）**：#2b 余量仅 48 B ⇒ 共享 CSS 任何净增长都会再次触发机制线（判据按设计工作）；下一批须二选一：CSS 源瘦身（推荐）或由用户裁决机制线校准。
>
> - **文件**：见 file-index W1318 段（site/reader 636 件按目录分组登记）。
>
> - **状态**：容量 #2b 转绿（56 KiB 机制线未动）；测试隔离缺陷根治；判据零放宽（压缩为无损等价变换·分类器与阈值均未改）。
### W1317（2026-11-25）：站内搜索容量余量治理（索引去重 + 语料 gzip+base64 压缩存储）

> **来源**：用户 2026-11-25 指令「先处理容量余量告警」＋同日方案裁决「去重 + 压缩都做」——对象为 check_capacity_budget.py 第 4 条「站内搜索脚本」2,965,520 B / 3 MiB（余量 5.73%）。
>
> - **取证（先证据后结论）**：三项字节 = text-search-app.js 2,160,029 B（99.3% 为内嵌原著明文）+ search-index-zh.js 393,433 B + search-index-en.js 412,058 B；实测 zh 索引 1091 条中 991 条与 en 索引同键同值（生成器「docs 全量两份共用」）⇒ 重复载荷 363,276 B；内嵌语料 gzip 压缩比 0.439（2.15 MB → 941 KB）。
>
> - **修法①索引去重**：`_gen_search_index.py` 拆出 site/data/search-index-docs.js（SITE_SEARCH_INDEX_DOCS·唯一副本）；zh/en 件只存本语言页面条目并改为 `SITE_SEARCH_INDEX_DOCS.concat([...])` 定义（消费方常量名与语义不变·页面 app 零改动）；两搜索页各加一行共享件外链（共享件必须先于本语言件加载）。
>
> - **修法②语料压缩**：`sync_search_corpus.py` 改为 gzip(紧凑 JSON)+base64 单串（EMBEDDED_CORPUS_GZ_B64·2.16 MB → 1.27 MB）；text-search-app.js 新增 decodeCorpus()，运行时以 DecompressionStream('gzip') 解压回填 EMBEDDED_DATA.chapters（file:// 可用·零外域）；旧浏览器不支持该 API 时由 showCorpusError() 给出明确降级提示（不静默失败）；--check 改为「解码后逐条对拍」（跨平台 zlib 字节差异不致假红）。
>
> - **同批根修（line_check 行号语义失效）**：该工具原从站内搜索内嵌语料取行号，W1316 去空白归一后全文无换行 ⇒ 所有引文恒为 line 1、--self-test 自 W1316 起即红。改为直读权威底本 source/原文/分回/*.md 并做空白无关匹配（折行/折行内空格仍可命中），4 正 1 负自测全绿。
>
> - **防漂移（判据同步收紧）**：第 46 槽扩为四判据（C1 三件数据件 + 两页双外链且顺序正确 / C2 docs / C3 zh / C4 en 逐条对拍），--self-test 1 正 6 负；截图分类器登记 docs 共享件为 skip 并放宽外链正则；容量 #4 清单纳入四件（诚实口径·新增字节不得隐形）；单测 6+5 例。
>
> - **验证**：容量 #4 2,965,520 → 1,713,688 B（94.30% → 54.48%·余量 45.5%）；sync_search_corpus --check 零差异；第 46 槽 0 FAIL（docs 991 · zh 100 · en 138）；line_check 自测 4 正 1 负；三页浏览器实测（全文检索「孙悟空」125 处命中 · ZH 全站搜索 24 行 · EN 搜索 7 行）零 console error；node --check 通过；pytest 1639 passed / 4 skipped；verify_delivery 全量见收官链。
>
> - **文件**：见 file-index W1317 段（本批 30+ 件·含新增 site/data/search-index-docs.js）。
>
> - **状态**：容量 #4 由 94.3% 降至 54.5% · 阈值未动 · 判据零放宽（计量面反而纳入新增共享件·无豁免/白名单新增）。
### W1316（2026-11-25）：站内搜索语料单源化（第三份副本清零 + 生成器落地）

> **来源**：用户 2026-11-25 指令「先回填台账 hash 再开批二」＋批二方向裁决「以权威 JSON 重建（推荐）」——对象为批一 triage 的 R2（2.1MB 单文件内嵌语料）与取证新发现的三副本不一致。
>
> - **取证（先证据后结论）**：text-search-app.js 内嵌 chapters 是**第三份语料**——与 source/原文/分回（剥 H1 与尾部识字表、去空白归一）**0/100 回一致**；与 dataset/text-search.json（已由 check_citations.py 与分回逐回全等机器对账）仅 **8/100 回一致**；共少 **789 字**（92 回不一致，7 回差 ≥20 字，多为漏标点/僻字，与 W737「恢复丢段与僻字」方向相反）。原定「从分回 md 生成且逐字节一致」前提不成立。
>
> - **修法（以权威 JSON 为唯一事实源）**：新增 `scripts/sync_search_corpus.py`（JSON → chapters 块渲染·幂等·`--check` 干跑 exit 1）；内嵌块头注释去数字字面量（字符数由页面 KPI 运行时计算·防静态漂移）；text-search.html 说明同步。首次重建即修正 92 回共 789 字；内嵌块 2.1MB → 2.06MB（行内换行归一）。容量 #4 实测 2.83MB / 3MB（未触发·余量 5.7%）。
>
> - **防漂移**：生成器登记 ci_sim GATES（`--check`）+ 第 42 槽脚本覆盖登记 + 单测 5 例（幂等/边界/危险序列 fail-closed/正文含方括号/真实仓树零漂移）。pytest.ini collected 标记 1887→1893。
>
> - **验证**：`sync_search_corpus.py --check` 重建前后各跑（1→0）；`node --check` 通过；全量单测 1638 passed / 4 skipped（199.0s）+ 根级 251 passed；ruff 全过；渲染复核档案 text-search.html sha 已随页面更新。
>
> - **文件**：.github/workflows/README.md, CHANGELOG.md, CITATION.cff, HANDOVER.md, README.md, STRUCTURE.md, docs/00-导读/W批次编号对账表.md, docs/00-导读/项目说明.md, docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md, pyproject.toml, pytest.ini, scripts/check_script_coverage.py, scripts/ci_sim.py, scripts/INDEX.md, scripts/output/_w1205_capacity_audit.json, scripts/output/chart-legend-render-audit.json, scripts/output/file-index.md, scripts/output/stats-changelog.json, scripts/output/stats-index.md, scripts/output/stats.json, scripts/output/svg_text_contrast_graphic_report.json, scripts/output/svg_text_contrast_report.json, scripts/output/tools-inventory.md, scripts/output/_vermilion_solid_cache.json, scripts/sync_search_corpus.py, site/data/text-search.html, site/rss.xml, site/static/js/text-search-app.js, tests/unit/INDEX.md, tests/unit/README.md, tests/unit/test_sync_search_corpus.py
>
> - **状态**：站内搜索语料三副本归一到权威 JSON · 生成器幂等可复核 · 判据零放宽（内容修正按权威源·容量/门禁阈值未动）。

### W1315（2026-11-24）：门禁链共享知识下沉（8 模块依赖环清零 + 体积窗兜底字面量清除）

> **来源**：用户 2026-11-24 指令「先跑批一，把 R5 双下沉和 R3 兜底字面量清理掉」＋同日续令「继续处理 R1 和 T5」——对象为 brooks-lint 健康检查（综合 94/100）确认的四条发现（R5 依赖环 / R3 常量副本 / R1 巨函数 / T5 空体测试）。
>
> - **根因（入口模块兼职共享库）**：同一决策分散住在三个 CLI 入口——常量链 `MAX_DOC_BYTES` / `LEDGER_WINDOW` 在 batch_closeout 顶层、`check_footnote_shape` 在 check_doc_size_budget、账本链 `ROOT` / `LEDGER` / `ARCHIVE_LEDGER` / `parse_ledger` 在 preflight_check ⇒ 消费方只能反向 import 入口，形成 `batch_cascade → check_doc_size_budget → batch_closeout → backfill_changelog → batch_cascade` 与 `preflight_check ↔ check_audit_trigger / check_backlog_review` 的 8 模块强连通分量。
>
> - **修法（双下沉·位置迁移非语义改写）**：`scripts/utils/gate_common.py` 新增治理文档共享段——`MAX_DOC_BYTES`(262144) / `LEDGER_WINDOW`(60) / `LEDGER_REL` / `ARCHIVE_LEDGER_REL` / `parse_ledger`（含 `_locate_status_idx` / `_locate_status` / `_split_touches` / `_locate_touches`）/ `check_footnote_shape`（含 `footnote_tail_shape_ok` 与两条尾句正则）。batch_closeout、check_doc_size_budget、check_audit_trigger、check_backlog_review、check_pitfalls_split、batch_cascade 改为向下引用；preflight_check 保留同名再导出面（测试与旧消费方零改动）。
>
> - **R3 兜底字面量清除**：check_pitfalls_split 的 `except → MAX_DOC_BYTES = 262144` 删除（导入失败即抛错）；check_doc_size_budget 的 `_SAME_SOURCE_ERR` fail-closed 分支与 `MAX_DOC_BYTES if MAX_DOC_BYTES else 262144` 三元同步删除——共享层导入失败在模块加载即抛，fail-fast 强于原静默降级。
>
> - **R1 认知负担治理**：`check_doc_sync.run_self_test` 361 行 → 21 行（39 个用例迁为模块级 `_SELFTEST_CASES` 数据表 + `_selftest_case` 条目工厂，用例文案/顺序/断言前缀逐字保留）；`check_pitfalls_split.evaluate` 233 行 → 33 行编排器，C1-C7 各拆独立判据函数（最长 44 行；C5 指针分支再抽 `_c5_check_pointer`），判据文案与输出数字逐项不变。
>
> - **T5 空体测试改真断言**：`test_kpi_17_dimensions_documented` 原只有 docstring、恒绿 ⇒ 改为断言 `dimensions` 16 条且 `W191` 不在数组内（17 = 16 数据维度 + W191 专题口径）；W191 若入数组即红，杜绝 KPI 口径静默漂移。
>
> - **验证**：scripts 依赖图 SCC 8 → 0（全仓脚本级 Tarjan 复算）；定向单测 135 passed（preflight_check / preflight_touches / four_digit_wnum / doc_size_budget / agents_tail_anchor / w1120 / pitfalls_split / audit_trigger / w1102）；三个门禁 `--self-test` 全过（doc-sync 39/39）；全量单测 1632 passed / 4 skipped（212.3s）+ 根级测试 251 passed；pitfalls 门禁 C1-C7 实盘输出逐项与改前一致（C4 281/281 · C5 263/12/278/0/16/0/0）；ruff 全过。
>
> - **连带发现（不在本批修·留待裁决）**：`tests/unit/test_w1102_batch_closeout.py::test_main_executes_steps_in_declared_order` 调 `bc.main()` 时只 mock 了 `bc.run`，而 `_run_backfill_prev_hash` 走 `_sp.run` 直连子进程 ⇒ 单测会真实回填本仓台账 hash（本批工作树中 W1312/W1314 的 hash 即由此产生）。属测试隔离缺陷，与本批改动无关。
>
> - **文件**：.github/workflows/README.md, CHANGELOG.md, CITATION.cff, HANDOVER.md, README.md, STRUCTURE.md, archive/docs/W批次编号对账表-ARCHIVE.md, docs/00-导读/W批次编号对账表.md, docs/00-导读/项目说明.md, scripts/batch_cascade.py, scripts/batch_closeout.py, scripts/check_audit_trigger.py, scripts/check_backlog_review.py, scripts/check_doc_size_budget.py, scripts/check_doc_sync.py, scripts/check_pitfalls_split.py, scripts/preflight_check.py, scripts/output/file-index.md, scripts/utils/gate_common.py, site/rss.xml, tests/test_narratology_data.py
>
> - **状态**：8 模块环清零 · 巨函数降至 ≤44 行 · 空体测试转真断言 · 判据零放宽（位置迁移/结构拆分/测试补断言；常量值、门禁文案与退出码逐字不变）。

### W1314（2026-11-24）：交接文档结构断言判据校正（尾链取行 + 四段骨架·两条存量假阳性清零）

> **来源**：用户 2026-11-24 指令「先不推送，帮我裁决那两个遗留的假阳性问题」——对象为 W1312/W1313 收官链连续报出的两条 SELF-CHECK 告警。
>
> - **裁决①尾链 = 判据实现缺陷（假阳性）**：原实现 `txt[rfind("最后更新："):]` 命中「维护契约」段内的引用行 ⇒ 尾链 = 整篇正文 ⇒ 日期计数恒 >3、首条 W 取自正文进度 ⇒ 每批必误报。W560 立此判据时文档形态不同，W707 结构收敛后未同步。正确口径 = 同一条 `> 最后更新：` 行内日期条目 ≤3（维护契约②「最新 1–3 批」）。
>
> - **裁决②「九、使用说明」= 判据过期（假阳性）**：该段已随 W707 结构收敛退役，现行维护契约明确零/一/二/三 四段骨架；判据仍按旧九段形态断言 ⇒ 每批必误报。改为四段存在且有序（同时覆盖原「零<一<二」部分断言）。
>
> - **修法（判据校正·非放宽）**：把交接文档结构断言抽成纯函数 `audit_handover_text(txt, batch)`（可单测），`_post_check` 只保留 CR 自愈并调用该函数；尾链改用 `^> 最后更新：` 行定位 + ISO 日期计数；九段判据删除，四段骨架含「三、方法论沉淀」。
>
> - **验证**：新增 `tests/unit/test_w1314_handover_audit.py` 7 例——先红（旧实现无该函数/基准样本误报尾链）后绿；真实 HANDOVER 审计仅剩「头链首条非 W1314」一条**正确**告警（本批入链后消失）；邻接 batch_cascade 测试全绿。
>
> - **文件**：.github/workflows/README.md, AGENTS.md, CHANGELOG.md, CITATION.cff, HANDOVER.md, README.md, STRUCTURE.md, archive/docs/AGENTS-ARCHIVE.md, archive/docs/W批次编号对账表-ARCHIVE.md, archive/docs/workflows-readme-history.md, docs/00-导读/W批次编号对账表.md, docs/00-导读/项目说明.md, docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md, pytest.ini, scripts/batch_cascade.py, scripts/output/INDEX.md, scripts/output/README.md, scripts/output/_cascade_files_W1314.txt, scripts/output/_vermilion_solid_cache.json, scripts/output/_w1266_allrender.json, scripts/output/_w1314_spec.json, scripts/output/chart-legend-render-audit.json, scripts/output/file-index.md, scripts/output/stats-changelog.json, scripts/output/stats-index.md, scripts/output/stats.json, scripts/output/svg_text_contrast_graphic_report.json, scripts/output/svg_text_contrast_report.json, scripts/output/tools-inventory.md, site/data/cross-time-danmaku.html, site/data/tag-cloud.html, site/dukou-engine.html, site/index.html, site/rss.xml, site/sitemap.xml, tests/unit/INDEX.md, tests/unit/README.md, tests/unit/test_w1314_handover_audit.py
>
> - **状态**：两条存量假阳性清零 · 判据零放宽（尾链口径与四段骨架均对齐文档现行契约，并各配机器断言）。

### W1313（2026-11-24）：CSP 面占位符语法治本（connect-src 非法源清零·合法保留域占位源·注入器双形态替换）

> **来源**：用户 2026-11-24 指令「先处理 dukou-engine.html 的占位符冻结项」→ 口径拍板「CSP 内改用合法占位源（推荐）」。
>
> - **根因**：CSP host-source 语法只允许 ALPHA/DIGIT/「-」/「.」——构建期占位符 `__XIJ_SERVICE_BASE__` 含下划线 ⇒ Chrome 判 invalid source 并报 console error（第 43 槽 site/en/dukou-engine.html V1 fail 的冻结项）；generate_csp.py 的 RAG_ORIGIN 直接引用该 token ⇒ dukou 两页 + index + dashboard 四页 CSP 同病。
>
> - **修法（契约 C-8 语义不变）**：新增 `CSP_PLACEHOLDER = https://xij-service-base.invalid`（`.invalid` 保留域·语法合法·浏览器解析零报错且不会发起请求）；generate_csp 的 RAG_ORIGIN 改取该常量并重生成 4 页 CSP；site/_headers 平台层 CSP 同步；inject_service_endpoint 对文本位与 CSP 面两种占位形态一并替换（collect_targets/--check 同步扩面）；守卫承认该 CSP 占位源合法。
>
> - **判据面**：第 70 槽新增 1 条合法形态（经用户拍板·非放宽既有阈值）；第 71 槽不变（CSP meta 属非哈希载体）；第 43 槽 EN 基线再收紧 1 行（828→826）。
>
> - **验证**：第 43 槽 228 页 0 FAIL / 冻结 0 / 可收紧 0 · 第 70 槽违规 0 · 第 71 槽违规 0 · CSP 零漂移（874 页 / 915 哈希）· pytest 19 passed（新增 3 例 + 守卫自测 6→7 例）· 注入器双形态替换有专项单例。
>
> - **文件**：.github/workflows/README.md, AGENTS.md, CHANGELOG.md, CITATION.cff, HANDOVER.md, README.md, STRUCTURE.md, archive/docs/AGENTS-ARCHIVE.md, archive/docs/W批次编号对账表-ARCHIVE.md, archive/docs/workflows-readme-history.md, docs/00-导读/W批次编号对账表.md, docs/00-导读/项目说明.md, docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md, docs/agent/gates.md, pytest.ini, scripts/check_no_hardcoded_endpoint.py, scripts/generate_csp.py, scripts/inject_service_endpoint.py, scripts/output/INDEX.md, scripts/output/README.md, scripts/output/_cascade_files_W1313.txt, scripts/output/_vermilion_solid_cache.json, scripts/output/_w1266_allrender.json, scripts/output/_w1313_spec.json, scripts/output/chart-legend-render-audit.json, scripts/output/chart-values-baseline-en.txt, scripts/output/file-index.md, scripts/output/stats-changelog.json, scripts/output/stats-index.md, scripts/output/stats.json, scripts/output/svg_text_contrast_graphic_report.json, scripts/output/svg_text_contrast_report.json, scripts/output/tools-inventory.md, site/_headers, site/dashboard.html, site/data/cross-time-danmaku.html, site/data/tag-cloud.html, site/dukou-engine.html, site/en/dukou-engine.html, site/index.html, site/rss.xml, site/sitemap.xml, tests/unit/INDEX.md, tests/unit/README.md, tests/unit/test_check_no_hardcoded_endpoint.py
>
> - **遗留（存量假阳性·与本批无关）**：收官链 SELF-CHECK 报「交接文档尾链异常」与「九、使用说明段缺失」两项——前者因检查用 rfind 命中「维护契约」段内的引用行、后者因 HANDOVER 骨架早已收敛为四段；两项均非本批引入，待另批裁决（不在本批放宽或改判据）。
>
> - **状态**：第 43 槽冻结项清零 · 判据零放宽（仅新增 1 条经拍板的合法占位源形态）。

### W1312（2026-11-24）：EN cave-estate 嵌入回退数据归一化治本（file:// 下 22 个 text y=NaN 清零·第 43 槽 EN 基线收紧）

> **来源**：用户 2026-11-24 指令「用 praxis:debug 跑一遍可视化页空白问题的取证流程；用 praxis:tdd 为 verify_delivery.py 补充判据单测」→ 用户批复「好的，执行吧」。
>
> - **取证（先证据后结论）**：第 43 槽全量 228 页扫描中 site/en/cave-estate.html V1 = fail:console-error（n=522）。file:// 直开实测 #chart-region 内 22 个 text.val 的 y="NaN" 且文本为空；同页 http 模式 0 条 NaN、中文页 0 条 NaN ⇒ 症状只出现在「file:// + EN 嵌入回退」组合。
>
> - **根因（一条解释全部症状）**：file:// 下 fetch 被拒 → loadData() catch 直接返回原始 EMBEDDED_DATA，而 by_region 归一化只写在 fetch 成功分支；EN 嵌入版 by_region 是原始嵌套组 [{region, caves:[{name, owner, luxury}]}]，renderRegionChart 读 d.luxury 得 undefined ⇒ scaleLinear(NaN) ⇒ 22 个空标签 + 动画逐帧重设属性产生数百条 console 报错。中文页嵌入版已是扁平形态 {region, luxury, name}，故不受影响。
>
> - **修复（治根不治点）**：抽出 normalizeRegion() 作为唯一归一化入口，fetch 与嵌入回退两条路径共用；嵌入分支返回 Object.assign({}, EMBEDDED_DATA, {by_region: normalizeRegion(...)})。内联脚本改动后重跑 generate_csp.py（1 页更新·874 页 915 哈希零漂移）。
>
> - **验证**：单页复测 V1 ok、冻结 0、可收紧 1 → 删除基线冻结行后全量 228 页复测 0 FAIL、冻结存量 1（余 site/en/dukou-engine.html 的 CSP 占位符·与本批无关）、可收紧 0。
>
> - **判据单测（TDD）**：新增 tests/unit/test_verify_scope_fallback.py 18 例，覆盖 _parse_scope / _classify_scope / _has_embedded_fallback 三条「决定门禁跑不跑」的纯判据；生产代码零改动（git diff scripts/verify_delivery.py 为空）；变异测试两次证明测试会咬（破坏标记剔除 ⇒ 1 例红；破坏越界回退 full ⇒ 4 例红），还原后 18/18 绿。
>
> - **文件**：.github/workflows/README.md, AGENTS.md, CHANGELOG.md, CITATION.cff, HANDOVER.md, README.md, STRUCTURE.md, archive/docs/AGENTS-ARCHIVE.md, archive/docs/W批次编号对账表-ARCHIVE.md, archive/docs/workflows-readme-history.md, docs/00-导读/W批次编号对账表.md, docs/00-导读/项目说明.md, docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md, pytest.ini, scripts/output/INDEX.md, scripts/output/README.md, scripts/output/_cascade_files_W1312.txt, scripts/output/_vermilion_solid_cache.json, scripts/output/_w1266_allrender.json, scripts/output/_w1312_spec.json, scripts/output/chart-legend-render-audit.json, scripts/output/chart-values-baseline-en.txt, scripts/output/file-index.md, scripts/output/stats-changelog.json, scripts/output/stats-index.md, scripts/output/stats.json, scripts/output/svg_text_contrast_graphic_report.json, scripts/output/svg_text_contrast_report.json, scripts/output/tools-inventory.md, site/data/cross-time-danmaku.html, site/data/tag-cloud.html, site/dukou-engine.html, site/en/cave-estate.html, site/index.html, site/rss.xml, tests/unit/INDEX.md, tests/unit/README.md, tests/unit/test_verify_scope_fallback.py
>
> - **状态**：修复 + 基线收紧 + 判据单测完成 · 判据零放宽。

### W1311（2026-11-24）：历史行状态列订正（六行登记滞后清零）+ 复盘批 T140（近三批治理面 + tmpe 清理纪律）

> **来源**：preflight 复盘触发（距上篇复盘 3 天 ≥ 3 天）+ 用户 2026-11-24 指令「现在做」。
>
> - **登记滞后一次性清零**：台账 W1299 / W1300 / W1305 / W1307 / W1309 / W1310 六行的状态列仍是「在途（认领·未收官）」而 git 已有其提交 ⇒ preflight 连续多批告警（P-43-01 口径：告警不拒绝·但长期留存会让「在途」盘点失真）⇒ 本批按 git 事实翻「已收官」并把 W1310 行 hash 回填 41294e71c（链上承载 commit·CI 6/6）⇒ C4-g 可复核。
>
> - **复盘批（T140）**：复盘 W1308–W1310 三批的治理面处置（收官链 archive 死锁治本 / L-08 伪血缘全清 406 件 / 绢本源件补缺入仓）+ tmpe 清理与归桶纪律（2.59→0.29 GiB·MD5 + 像素双证据证无丢失）。
>
> - **两处口径更正**：① 上一轮把「批号目录平铺落 w###/」判为工具缺陷 ⇒ 实查 batch_bucket_dest 的 docstring 明写「无下划线前缀的批号目录保持平铺」⇒ **契约使然** ⇒ 撤下该工具改动项·改记为已知设计边界；② 计划「台账 touches 补 406 件逐件」⇒ 实测 preflight 支持**目录前缀匹配**⇒ 并发保护已有效 ⇒ 改判**不补逐件**（避免台账行膨胀约 5 倍而无判定增益）。
>
> - **文件**：.github/workflows/README.md, AGENTS.md, CHANGELOG.md, CITATION.cff, HANDOVER.md, README.md, STRUCTURE.md, archive/docs/AGENTS-ARCHIVE.md, archive/docs/W批次编号对账表-ARCHIVE.md, archive/docs/workflows-readme-history.md, docs/00-导读/W批次编号对账表.md, docs/00-导读/项目说明.md, docs/11-方案报告/README.md, docs/11-方案报告/计划方案/T140-任务计划执行与经验沉淀报告-2026-11-24.md, docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md, docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md, docs/INDEX.md, scripts/output/INDEX.md, scripts/output/README.md, scripts/output/_cascade_files_W1311.txt, scripts/output/_vermilion_solid_cache.json, scripts/output/_w1266_allrender.json, scripts/output/_w1311_spec.json, scripts/output/chart-legend-render-audit.json, scripts/output/file-index.md, scripts/output/stats-changelog.json, scripts/output/stats-index.md, scripts/output/stats.json, scripts/output/svg_text_contrast_graphic_report.json, scripts/output/svg_text_contrast_report.json, scripts/output/tools-inventory.md, site/data/cross-time-danmaku.html, site/data/search-index-zh.js, site/data/tag-cloud.html, site/dukou-engine.html, site/en/search-index-en.js, site/index.html, site/rss.xml
>
> - **验证**：六行状态列与 git 事实一致 · W1310 行 hash 指向链上承载 commit ⇒ 第 31 门禁 C4-g 绿 · 第 48 门禁（计划方案合规）绿 · 全量门禁真全量 · 判据与阈值**零放宽**。
>
> - **状态**：**登记滞后清零 + 复盘落档**；46 件冻结窗件待 48h 窗开（已挂定时复查）· 4 个活跃工作树禁碰。

### W1310（2026-11-24）：绢本系列 8 张源件入仓（5472×3072 JPEG·补缺·新目录避免覆盖·像素级判别证画面不同）

> **来源**：用户 2026-11-24 指令「请将核对后剩余的 8 张 silk/hero 原图去重后入仓并完成验证」。
>
> - **去重与判别双证据**：tmpe 候选 86 件 → MD5 去重 **47 件** → 仓内已逐字存在 **39 件**（ci_shallow / w1287 工作树只是仓内 assets/ 的副本）⇒ 真正未入库 **8 件**；与仓内同名件尺寸相同（均 5472×3072）但**画面不同**（像素判别 corr 0.34–0.58、dhash hamming 22–32 ⇒ 非压缩差异）⇒ 属**补缺**而非冗余。
>
> - **入仓（新目录·不覆盖既有件）**：assets/promo/silk-hero-src/ —— 既有 assets/promo/silk-hero-set/ 下同名件画面不同 ⇒ 同名入仓即覆盖丢失 ⇒ 独立目录并存 + 目录内 SOURCE.md 说明三者关系与去重依据；8 件按字节拷贝，拷贝后 md5 与源**逐件一致**（8/8）+ PIL 解码校验通过；保留 JPEG 原件不转码（与仓内既有同规格 JPG 做法一致）。
>
> - **文件**：.github/workflows/README.md, AGENTS.md, CHANGELOG.md, CITATION.cff, HANDOVER.md, README.md, STRUCTURE.md, archive/docs/AGENTS-ARCHIVE.md, archive/docs/workflows-readme-history.md, assets/promo/INDEX.md, assets/promo/silk-hero-src/INDEX.md, assets/promo/silk-hero-src/README.md, assets/promo/silk-hero-src/SOURCE.md, assets/promo/silk-hero-src/silk-hero-04-baigu-furen.jpg, assets/promo/silk-hero-src/silk-hero-05-huoyanshan-yaowang.jpg, assets/promo/silk-hero-src/silk-hero-06-heifengshan.jpg, assets/promo/silk-hero-src/silk-hero-07-dumu-qiao.jpg, assets/promo/silk-hero-src/silk-hero-08-shanye-xinglu.jpg, assets/promo/silk-hero-src/silk-hero-09-wukong-tanyu.jpg, assets/promo/silk-hero-src/silk-hero-10-jingubang.jpg, assets/promo/silk-hero-src/silk-hero-11-fabao-sanjian.jpg, docs/00-导读/W批次编号对账表.md, docs/00-导读/项目说明.md, docs/11-方案报告/README.md, docs/11-方案报告/计划方案/T139-任务计划执行与经验沉淀报告-2026-11-24.md, docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md, docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md, docs/INDEX.md, scripts/output/INDEX.md, scripts/output/README.md, scripts/output/_cascade_files_W1310.txt, scripts/output/_vermilion_solid_cache.json, scripts/output/_w1266_allrender.json, scripts/output/_w1309_spec.json, scripts/output/_w1310_spec.json, scripts/output/chart-legend-render-audit.json, scripts/output/file-index.md, scripts/output/stats-changelog.json, scripts/output/stats-index.md, scripts/output/stats.json, scripts/output/svg_text_contrast_graphic_report.json, scripts/output/svg_text_contrast_report.json, scripts/output/tools-inventory.md, site/data/cross-time-danmaku.html, site/data/search-index-zh.js, site/data/tag-cloud.html, site/dukou-engine.html, site/en/search-index-en.js, site/index.html, site/rss.xml
>
> - **验证**：MD5 + 像素级双证据（去重与判别）· 拷贝完整性 8/8 · 尺寸均 5472×3072 · 既有 silk-hero-set/ 12 件未动（零覆盖）· 目录件由收官链 refresh 生成 · 门禁以本批收官时的实跑结果为准（未跑完前不作「绿」的声明）· 判据与阈值**零放宽**。
>
> - **声明与实况不符项**：① 初判「同名 ⇒ 同一画面」⇒ 像素级判别证伪（corr 0.55、hamming 22）⇒ 改为补缺入仓；② 初判「backup-v1 为高清原图·仓内为缩放版」⇒ 实测两者同尺寸 5472×3072 ⇒ 差异在画面内容而非分辨率。
>
> - **状态**：**8 张源件补缺入仓完成**（源件唯一副本风险关闭）· 判据零放宽。

### W1309（2026-11-23）：L-08 闭合（目录件伪血缘一次全清 406 件·残留 0 + 生成器去硬编码日期与 buckets 契约治本 + W1308 五处治本补记坑表 E-316~E-320 + 计数链 421→426）

> **来源**：用户 2026-11-23 指令「请启动 W1309 首批 L-08 目录件伪血缘处理，并在同批补记 W1308 五处治本坑表 E 号、同步计数链」。
>
> - **L-08 闭合（目录件伪血缘一次全清 406 件·残留 0）**：实测目录件 236 目录 / **406 件**带硬编码「生成日期/生成时点：2026-10-18」⇒ 伪血缘。**关键实测**：跑 refresh 只写入 1 件、**43 件被 showcase 保护跳过** ⇒ **405 件属生成器不再托管的目录** ⇒ refresh 永不覆写 ⇒ 只能一次性订正。**生成器治本**：INDEX.md 尾行与 README.md 元信息**不再写死日期**（改「生成来源」标记 ⇒ 伪血缘不再产生且 refresh 幂等）+ 所有权判定抽为 _GEN_OWNERSHIP_MARKERS（含存量旧标记作一次性过渡）+ 新增 **manifest 限定入口**（分小批刷新·边界确定可重放）。**存量订正**：一次性脚本只删两行元信息、**刻意不补「生成来源」标记**（补了等于声明生成器托管 ⇒ 未来 refresh 覆写人工内容）⇒ **幂等**（实测首次订正 50 · 二次 0 订正）· 本批一次全清 **406 件**（实测残留 0）⇒ 登记面按**二级目录聚合**（406 件 → 13 行）以免撑爆 file-index。
>
> - **W1308 五处治本补记坑表**：E-316 归档腾窗迁出量口径（最小达标 + 底线联立 + 两面同下界）· E-317 链首同号替换的日期前缀残留 ⇒ 双日期 · E-318 多行块按行定位 ⇒ 逐次累积 · E-319 补滚触发面（replaced 不触发）与滚动量（一次只滚一块）· E-320 git ls-files 展开目录清单的 ignore 泄漏与中文路径转义 ⇒ 判据层正本（级联 +4 / git +1）+ 归档叙事 5 段 + 根壳反查表 ⇒ 计数链由 stats.py 实算跟随：**总 421→426 · 级联 26→30 · git 39→40**。
>
> - **归档腾窗治本二则（连带）**：W1308 引入的「迁出块不得含编号规则段」保护**过严**——判据把 file-index **表格登记行**里的「本批段 + 编号规则段推进（W001-W13xx 形态）」误认成锚点 ⇒ file-index 最老段被钉死（max_k=0）⇒ 体积窗永远无法腾窗（死锁）。治本：真锚点只在**治理声明行**（以「>」开头的引用行）里识别 ⇒ 登记行文本不再构成迁出禁令（判据单测 +1 例·真锚点仍受保护）。
>
> - **文件**：.agent/skills/puti-shouye/SKILL.md, .github/INDEX.md, .github/ISSUE_TEMPLATE/INDEX.md, .github/ISSUE_TEMPLATE/README.md, .github/workflows/INDEX.md, .github/workflows/README.md, AGENTS.md, CHANGELOG.md, CITATION.cff, HANDOVER.md, INDEX.md, README.md, STRUCTURE.md, archive/INDEX.md, archive/docs/AGENTS-ARCHIVE.md, archive/docs/CHANGELOG-ARCHIVE.md, archive/docs/INDEX.md, archive/docs/README.md, archive/docs/W批次编号对账表-ARCHIVE.md, archive/docs/_dev/INDEX.md, archive/docs/_dev/README.md, archive/docs/_dev/产品管理套件应用-2026-10-02/INDEX.md, archive/docs/_dev/产品管理套件应用-2026-10-02/README.md, archive/docs/_dev/科技服务顾问-数字人文资助渠道-2026-10-02/INDEX.md, archive/docs/_dev/科技服务顾问-数字人文资助渠道-2026-10-02/README.md, archive/docs/file-index-ARCHIVE.md, archive/docs/pitfalls-detail-ARCHIVE.md, archive/docs/plans/INDEX.md, archive/docs/plans/README.md, archive/docs/specs/INDEX.md, archive/docs/specs/README.md, archive/docs/templates/INDEX.md, archive/docs/w550-shot-review/INDEX.md, archive/docs/w550-shot-review/README.md, archive/docs/workflows-readme-history.md, archive/docs/复盘报告/INDEX.md, archive/docs/复盘报告/README.md, archive/hyperframes/INDEX.md, archive/hyperframes/compositions/INDEX.md, archive/hyperframes/compositions/README.md, archive/hyperframes/compositions/d3-visualizations/INDEX.md, archive/hyperframes/compositions/d3-visualizations/README.md, archive/hyperframes/output/INDEX.md, archive/hyperframes/output/README.md, archive/scripts/INDEX.md, archive/scripts/README.md, archive/scripts/attic/INDEX.md, archive/scripts/audit/INDEX.md, archive/scripts/batches/INDEX.md, archive/scripts/batches/README.md, archive/scripts/batches/misc/INDEX.md, archive/scripts/batches/misc/README.md, archive/scripts/batches/w1071/INDEX.md, archive/scripts/batches/w1071/README.md, archive/scripts/batches/w1073/INDEX.md, archive/scripts/batches/w1073/README.md, archive/scripts/batches/w1074/INDEX.md, archive/scripts/batches/w1074/README.md, archive/scripts/batches/w1076/INDEX.md, archive/scripts/batches/w1076/README.md, archive/scripts/batches/w1078/INDEX.md, archive/scripts/batches/w1078/README.md, archive/scripts/batches/w1079/INDEX.md, archive/scripts/batches/w1079/README.md, archive/scripts/batches/w1080/INDEX.md, archive/scripts/batches/w1080/README.md, archive/scripts/batches/w1089/INDEX.md, archive/scripts/batches/w1089/README.md, archive/scripts/batches/w10xx/INDEX.md, archive/scripts/batches/w10xx/README.md, archive/scripts/batches/w1100/INDEX.md, archive/scripts/batches/w1100/README.md, archive/scripts/batches/w1169/INDEX.md, archive/scripts/batches/w1169/README.md, archive/scripts/batches/w1175/INDEX.md, archive/scripts/batches/w1175/README.md, archive/scripts/batches/w1176/INDEX.md, archive/scripts/batches/w1176/README.md, archive/scripts/batches/w4xx/INDEX.md, archive/scripts/batches/w4xx/README.md, archive/scripts/batches/w5xx/INDEX.md, archive/scripts/batches/w5xx/README.md, archive/scripts/batches/w6xx/INDEX.md, archive/scripts/batches/w6xx/README.md, archive/scripts/batches/w7xx/INDEX.md, archive/scripts/batches/w7xx/README.md, archive/scripts/batches/w8xx/INDEX.md, archive/scripts/batches/w8xx/README.md, archive/scripts/batches/w9xx/INDEX.md, archive/scripts/batches/w9xx/README.md, archive/scripts/review-pass3/INDEX.md, archive/scripts/review-pass3/README.md, archive/scripts/review-pass3/prompts/INDEX.md, archive/scripts/review-pass3/prompts/README.md, assets/INDEX.md, assets/README.md, assets/design/INDEX.md, assets/design/ai-concepts/INDEX.md, assets/design/alternatives/INDEX.md, assets/design/logo/INDEX.md, assets/design/process/INDEX.md, assets/design/screenshots/INDEX.md, assets/design/tools/INDEX.md, assets/fonts/INDEX.md, assets/fonts/README.md, assets/fonts/source/INDEX.md, assets/fonts/source/README.md, assets/game/INDEX.md, assets/game/README.md, assets/game/js/INDEX.md, assets/game/js/README.md, assets/promo/INDEX.md, assets/promo/hero-set/INDEX.md, assets/promo/hero-set/raw/INDEX.md, assets/promo/hero-set/raw/round-w1005/INDEX.md, assets/promo/hero-set/raw/round-w1005/README.md, assets/promo/output/INDEX.md, assets/promo/output/README.md, assets/promo/plate-set/INDEX.md, assets/promo/silk-hero-set/INDEX.md, dataset/INDEX.md, dataset/entities/INDEX.md, dataset/entities/README.md, docs/00-导读/INDEX.md, docs/00-导读/W批次编号对账表.md, docs/00-导读/遗留总账.md, docs/00-导读/项目说明.md, docs/07-学以致用/INDEX.md, docs/08-提升认知/INDEX.md, docs/09-精神塑造/INDEX.md, docs/11-方案报告/README.md, docs/11-方案报告/计划方案/T138-任务计划执行与经验沉淀报告-2026-11-23.md, docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md, docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md, docs/12-提示词库/INDEX.md, docs/12-提示词库/README.md, docs/INDEX.md, docs/README.md, docs/_templates/INDEX.md, docs/_templates/README.md, docs/_templates/duipai/INDEX.md, docs/agent-guardrails/INDEX.md, docs/agent/INDEX.md, docs/agent/README.md, docs/agent/pitfalls-topics/INDEX.md, docs/agent/pitfalls-topics/README.md, docs/agent/pitfalls-topics/cascade-changelog.md, docs/agent/pitfalls-topics/css-visual.md, docs/agent/pitfalls-topics/data-trust.md, docs/agent/pitfalls-topics/flow-collab.md, docs/agent/pitfalls-topics/git-concurrency.md, docs/agent/pitfalls-topics/js-csp-runtime.md, docs/agent/pitfalls.md, docs/superpowers/INDEX.md, docs/superpowers/README.md, docs/superpowers/plans/INDEX.md, docs/superpowers/plans/README.md, mcp-server/INDEX.md, packaging/INDEX.md, packaging/README.md, packaging/xiyouji-analysis/INDEX.md, packaging/xiyouji-analysis/src/INDEX.md, packaging/xiyouji-analysis/src/README.md, packaging/xiyouji-analysis/src/xiyouji_analysis/INDEX.md, packaging/xiyouji-analysis/src/xiyouji_analysis/README.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/AA_叙事实验/INDEX.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/AA_叙事实验/README.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/AB_视觉艺术/INDEX.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/AB_视觉艺术/README.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/AC_方法论矩阵/INDEX.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/AC_方法论矩阵/README.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/AD_认知心理/INDEX.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/AD_认知心理/README.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/AE_生态学/INDEX.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/AE_生态学/README.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/AF_法理经济/INDEX.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/AF_法理经济/README.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/AG_物质考古/INDEX.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/AG_物质考古/README.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/AH_语言学/INDEX.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/AH_语言学/README.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/A_文本基础/INDEX.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/A_文本基础/README.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/B_人物/INDEX.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/B_人物/README.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/C_情节/INDEX.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/C_情节/README.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/D_关系/INDEX.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/D_关系/README.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/E_地理/INDEX.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/E_地理/README.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/G_哲学/INDEX.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/G_哲学/README.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/H_风险与项目/INDEX.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/H_风险与项目/README.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/INDEX.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/I_妖怪社会学/INDEX.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/I_妖怪社会学/README.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/J_权力与资源/INDEX.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/J_权力与资源/README.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/K_命运与轮回/INDEX.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/K_命运与轮回/README.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/L_商业模型/INDEX.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/L_商业模型/README.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/M_洞府房产/INDEX.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/M_洞府房产/README.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/N_法术阵法/INDEX.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/N_法术阵法/README.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/O_美学时尚/INDEX.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/O_美学时尚/README.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/P_音乐声效/INDEX.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/P_音乐声效/README.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/Q_源流演变/INDEX.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/Q_源流演变/README.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/README.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/R_解构作品/INDEX.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/R_解构作品/README.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/S_全球模式/INDEX.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/S_全球模式/README.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/T_反事实推断/INDEX.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/T_反事实推断/README.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/U_文化错位/INDEX.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/U_文化错位/README.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/V_打工人职场/INDEX.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/V_打工人职场/README.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/W_社媒人设/INDEX.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/W_社媒人设/README.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/X_游戏网文/INDEX.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/X_游戏网文/README.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/Y_伦理消费/INDEX.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/Y_伦理消费/README.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/Z_图表设计/INDEX.md, packaging/xiyouji-analysis/src/xiyouji_analysis/analyses/Z_图表设计/README.md, pitfalls.md, pytest.ini, scripts/AA_叙事实验/INDEX.md, scripts/AA_叙事实验/README.md, scripts/AB_视觉艺术/INDEX.md, scripts/AB_视觉艺术/README.md, scripts/AC_方法论矩阵/INDEX.md, scripts/AC_方法论矩阵/README.md, scripts/AD_认知心理/INDEX.md, scripts/AD_认知心理/README.md, scripts/AE_生态学/INDEX.md, scripts/AE_生态学/README.md, scripts/AF_法理经济/INDEX.md, scripts/AF_法理经济/README.md, scripts/AG_物质考古/INDEX.md, scripts/AG_物质考古/README.md, scripts/AH_语言学/INDEX.md, scripts/AH_语言学/README.md, scripts/A_文本基础/INDEX.md, scripts/A_文本基础/README.md, scripts/B_人物/INDEX.md, scripts/B_人物/README.md, scripts/C_情节/INDEX.md, scripts/C_情节/README.md, scripts/D_关系/INDEX.md, scripts/D_关系/README.md, scripts/E_地理/INDEX.md, scripts/E_地理/README.md, scripts/F_时间/INDEX.md, scripts/F_时间/README.md, scripts/G_哲学/INDEX.md, scripts/G_哲学/README.md, scripts/H_风险与项目/INDEX.md, scripts/H_风险与项目/README.md, scripts/INDEX.md, scripts/I_妖怪社会学/INDEX.md, scripts/I_妖怪社会学/README.md, scripts/J_权力与资源/INDEX.md, scripts/J_权力与资源/README.md, scripts/K_命运与轮回/INDEX.md, scripts/K_命运与轮回/README.md, scripts/L_商业模型/INDEX.md, scripts/L_商业模型/README.md, scripts/M_洞府房产/INDEX.md, scripts/M_洞府房产/README.md, scripts/N_法术阵法/INDEX.md, scripts/N_法术阵法/README.md, scripts/O_美学时尚/INDEX.md, scripts/O_美学时尚/README.md, scripts/P_音乐声效/INDEX.md, scripts/P_音乐声效/README.md, scripts/Q_源流演变/INDEX.md, scripts/Q_源流演变/README.md, scripts/R_解构作品/INDEX.md, scripts/R_解构作品/README.md, scripts/S_全球模式/INDEX.md, scripts/S_全球模式/README.md, scripts/T_反事实推断/INDEX.md, scripts/T_反事实推断/README.md, scripts/U_文化错位/INDEX.md, scripts/U_文化错位/README.md, scripts/V_打工人职场/INDEX.md, scripts/V_打工人职场/README.md, scripts/W_社媒人设/INDEX.md, scripts/W_社媒人设/README.md, scripts/X_游戏网文/INDEX.md, scripts/X_游戏网文/README.md, scripts/Y_伦理消费/INDEX.md, scripts/Y_伦理消费/README.md, scripts/Z_图表设计/INDEX.md, scripts/Z_图表设计/README.md, scripts/api/INDEX.md, scripts/api/README.md, scripts/archive_segments.py, scripts/audit/INDEX.md, scripts/audit/README.md, scripts/gen_folder_docs.py, scripts/guardrails/INDEX.md, scripts/guardrails/README.md, scripts/lib/INDEX.md, scripts/lib/README.md, scripts/lighthouse/INDEX.md, scripts/lighthouse/README.md, scripts/output/INDEX.md, scripts/output/README.md, scripts/output/_cascade_files_W1309.txt, scripts/output/_vermilion_solid_cache.json, scripts/output/_w1266_allrender.json, scripts/output/_w1309_batch1.txt, scripts/output/_w1309_fix_legacy_dates.py, scripts/output/_w1309_pitfalls_patch.py, scripts/output/_w1309_spec.json, scripts/output/chart-legend-render-audit.json, scripts/output/data/INDEX.md, scripts/output/data/README.md, scripts/output/figures/INDEX.md, scripts/output/figures/README.md, scripts/output/file-index.md, scripts/output/stats-changelog.json, scripts/output/stats-index.md, scripts/output/stats.json, scripts/output/svg_text_contrast_graphic_report.json, scripts/output/svg_text_contrast_report.json, scripts/output/tools-inventory.md, scripts/rag/INDEX.md, scripts/rag/eval/INDEX.md, scripts/rag/eval/README.md, scripts/utils/INDEX.md, scripts/utils/README.md, site/INDEX.md, site/README.md, site/chapters/INDEX.md, site/chapters/README.md, site/characters/INDEX.md, site/characters/README.md, site/data/INDEX.md, site/data/README.md, site/data/cross-time-danmaku.html, site/data/json/INDEX.md, site/data/json/README.md, site/data/search-index-zh.js, site/data/tag-cloud.html, site/dukou-engine.html, site/en/INDEX.md, site/en/json/INDEX.md, site/en/json/README.md, site/en/search-index-en.js, site/index.html, site/js/INDEX.md, site/js/README.md, site/reader/INDEX.md, site/reader/README.md, site/reader/culture/INDEX.md, site/reader/culture/README.md, site/reader/essays/INDEX.md, site/reader/essays/README.md, site/reader/people/INDEX.md, site/reader/people/README.md, site/reader/poetry/INDEX.md, site/reader/poetry/README.md, site/reader/themes/INDEX.md, site/reader/themes/README.md, site/rss.xml, site/static/INDEX.md, site/static/README.md, site/static/css/INDEX.md, site/static/css/README.md, site/static/fonts/INDEX.md, site/static/fonts/README.md, site/static/icons/INDEX.md, site/static/icons/README.md, site/static/icons/ui/INDEX.md, site/static/icons/ui/README.md, site/static/images/INDEX.md, site/static/images/README.md, site/static/images/silk-src/INDEX.md, site/static/images/silk-src/README.md, site/static/img/INDEX.md, site/static/img/README.md, site/static/js/INDEX.md, site/static/js/README.md, site/themes/INDEX.md, site/themes/README.md, source/INDEX.md, source/README.md, source/原文/INDEX.md, source/原文/README.md, source/原文/shendu/INDEX.md, source/原文/shendu/README.md, source/原文/分回/INDEX.md, source/原文/分回/README.md, source/引用与网络解读/INDEX.md, source/引用与网络解读/README.md, tests/INDEX.md, tests/README.md, tests/e2e/INDEX.md, tests/e2e/README.md, tests/e2e/baseline/INDEX.md, tests/e2e/baseline/README.md, tests/fixtures/INDEX.md, tests/fixtures/README.md, tests/unit/INDEX.md, tests/unit/README.md, tests/unit/test_archive_segments_migration_plan.py, xiyouji-agent-web/INDEX.md, xiyouji-agent-web/deploy/INDEX.md, xiyouji-agent-web/deploy/README.md, xiyouji-agent-web/deploy/pg/INDEX.md, xiyouji-agent-web/deploy/pg/bin/INDEX.md, xiyouji-agent-web/deploy/pg/bin/README.md, xiyouji-agent-web/deploy/pg/migrations/INDEX.md, xiyouji-agent-web/deploy/pg/migrations/README.md, xiyouji-agent-web/e2e/INDEX.md, xiyouji-agent-web/e2e/README.md, xiyouji-agent-web/evals/INDEX.md, xiyouji-agent-web/evals/README.md, xiyouji-agent-web/fuzz/INDEX.md, xiyouji-agent-web/fuzz/README.md, xiyouji-agent-web/server/INDEX.md, xiyouji-agent-web/server/README.md, xiyouji-agent-web/server/compliance/INDEX.md, xiyouji-agent-web/server/compliance/README.md, xiyouji-agent-web/server/engine/INDEX.md, xiyouji-agent-web/server/engine/README.md, xiyouji-agent-web/server/storage/INDEX.md, xiyouji-agent-web/server/storage/README.md, xiyouji-agent-web/src/INDEX.md, xiyouji-agent-web/src/README.md, xiyouji-agent-web/src/components/INDEX.md, xiyouji-agent-web/src/components/README.md, xiyouji-agent-web/src/components/toolCalls/INDEX.md, xiyouji-agent-web/src/components/toolCalls/README.md, xiyouji-agent-web/src/hooks/INDEX.md, xiyouji-agent-web/src/hooks/README.md, xiyouji-agent-web/src/pages/INDEX.md, xiyouji-agent-web/src/pages/README.md, xiyouji-agent-web/src/test/INDEX.md, xiyouji-agent-web/src/test/README.md, xiyouji-agent-web/src/utils/INDEX.md, xiyouji-agent-web/src/utils/README.md, xiyouji-desktop/INDEX.md, xiyouji-desktop/assets/INDEX.md, xiyouji-desktop/assets/README.md, xiyouji-desktop/scripts/INDEX.md, xiyouji-desktop/scripts/README.md, xiyouji-desktop/src/INDEX.md, xiyouji-desktop/src/README.md, xiyouji-desktop/tests/INDEX.md, xiyouji-desktop/tests/README.md, scripts/batch_spec.py, scripts/backfill_changelog.py, scripts/batch_cascade.py
>
> - **验证**：坑表判据 **0 FAIL**（check_pitfall_id_unique 新增 5 条 · check_pitfalls_split C1–C7 全 PASS·声明 426 = 实算 426·反查表遗漏 0 多余 0）· 订正幂等自证（首次 50 · 二次 0）· 抽样 diff 仅删两行元信息·内容逐字无损 · 台账 W1308 行收官回填 a5205ba5d + W1309 认领行（touches 逐件 105 项）· 判据与阈值**零放宽**。
>
> - **声明与实况不符项**：① 初判「根因是 CRLF ⇒ 生成器改 LF 即可」⇒ 实测 LF 早已治（W1307）⇒ 根因收窄为「硬编码日期 + showcase 保护面」；② 计划「订正约 50 件」⇒ 实入库 93 件（50 + 43 历史累积）⇒ 一次清空避免每批带累积跑；③ 计划「新增 E-297~E-301」⇒ 实测 E-297~E-300 已被数据主题占用（现存最大 E-315）⇒ 改用 E-316~E-320。
>
> - **状态**：**L-08 第 1 小批完成**（剩余 313 件待 W1310–W1315）· 坑表补记与计数链同步完成 · 判据零放宽。

### W1308（2026-11-23）：收官链 L-11 治本 (hash 回填 v2 链上口径 + 排除本批 + 错值修指) + 代改 5 行悬空 hash 清零豁免基线 + L-12 确认既有闸门覆盖 + 归档腾窗治本 (迁出量最小化 + 两面同下界)

> **来源**：用户 2026-11-23 裁决「继续，给我选项我来决策」→ 四项裁决：L-08 分 8 小批 · L-11+L-12 都做 · 5 行悬空 hash 我代改 · tmpe 冻结区等窗后清且 JPG 保留本地 ⇒ 立项 W1308（收官链 L-11 治本 + 悬空 hash 代改清零 + 归档腾窗治本）。
>
> - **L-11 治本**：收官链新增 `_run_backfill_prev_hash_v2`（最小侵入：新增函数 + 只切调用点·v1 保留可回退）—— 四处口径变更：① 候选来源 `git log --reverse HEAD`（**只在当前历史链上取**·v1 用 `--all` 会把已失效 commit 再次写回台账⇒悬空复发）② subject 含**多个 W 号**时全部登记（合并推送形态）③ **排除本批**（自指不可知⇒本批 hash 必留空待下一批⇒amend 不再制造悬空）④ hash 非空但**不在链上** ⇒ 改指该批链上首笔（错值修指）。纯函数 `_parse_subject_w_ids` / `_prefix_sets` / `_hash_action` + 单测 **8 例全绿**。
>
> - **代改 5 行悬空 hash（用户授权）**：按「该批在 main 历史链上的最早承载 commit」逐行算 ⇒ W1294→`694fae2e5b` · W1295→`2d33f5f11a` · W1296→`c51794db9b` · W1301/W1303→`0c926a0aac`（合并推送那笔）⇒ 用仓内**独占回填工具** `ledger_backfill.py --w N --hash <sha>`（锁旧指纹→改→出新指纹）执行 ⇒ **`merge-base --is-ancestor` 5/5 True** ⇒ **豁免基线清零** ⇒ **C4-g 今后对任何新增悬空行一律判红**（机制保留、无存量）。
>
> - **L-12 结论**：**无需新判据**——链尾 `gate` 步调 `pre_push_gate.py`（单一事实源），其中已有「主工作树干净(含未跟踪)」一项 ⇒ 链外再改在链尾即被拦 ⇒ 已在总账转闭合（避免重复实现与口径漂移）。
>
> - **归档腾窗治本（W1308 收官链 archive 步死锁的根修）**：收官链 archive 步在本批首次失败——`archive_segments.plan_by_size` 以 `chunk=50` 为**固定步长**迁出（迁出量由 chunk 决定而非由体积决定）⇒ file-index 正本 50 段·体积 262,964 B **仅超窗 820 B**，却被迫迁出 44 段 ⇒ 正本仅剩 6 段 ⇒ 铁律 22「正本留 ≥ 20 段」断言 FAIL ⇒ 收官链死锁。**三处根修（判据只加严不放宽）**：① `plan_by_size` 改「二分求**最小达标** k」（实测迁 2 段·留存 48 段）；② 迁出上界收紧为「迁出块不得含编号规则段」（原上界会把编号规则段一并迁走⇒版本面推进器 fail-closed）；③ `_rule_seg_index` 假阳性修正——CHANGELOG 的编号规则串实际落在**末尾文件级块**（`## [Unreleased]`）内（该块不随段迁出）⇒ 原实现把最后一个批段误判为「不可迁出段」⇒ CHANGELOG 面永远无法腾窗。**新增对齐能力** `plan_align_below` + `main()` 改「各面按最小达标规划 → 取目标下界 → 两面统一迁出」⇒ 迁出后两面同下界 W1256（`rebuild_section.boundary_check` 硬断言）· 并加「迁出后体积达标」纯计算断言。判据单测 **5 例**（最小达标最小性 / 编号规则段保护 / 末尾块假阳性 / 对齐迁出语义 / 仓内两面同下界且各留 ≥ 20 段）。
>
> - **cascade 链首日期前缀残留治本（连带）**：本批 regsurface 步首次报红「HANDOVER 无「最后更新」行」⇒ 根因是 `batch_cascade._upsert_chain_entry` 的「按批号替换」分支只替换「（W#### …）」括号区间 ⇒ 同号条目**文本变更**时条目左侧的旧日期前缀残留 ⇒ 产出「最后更新：2026-11-232026-11-23（W1308 …）」双日期 ⇒ 登记面一致性闸的正则「最后更新：<日期>（W####」匹配不上。治本：新增 `_entry_start`（替换区间自日期前缀起算·头链尾链共用·单一事实源）+ `_same` 匹配纳入可选日期前缀 + 内容一致但有残留时亦清理（幂等自愈）⇒ 判据单测 **3 例**。
>
> - **文件**：.github/workflows/README.md, AGENTS.md, CHANGELOG.md, CITATION.cff, HANDOVER.md, README.md, STRUCTURE.md, pytest.ini, archive/docs/AGENTS-ARCHIVE.md, archive/docs/CHANGELOG-ARCHIVE.md, archive/docs/file-index-ARCHIVE.md, archive/docs/W批次编号对账表-ARCHIVE.md, archive/docs/workflows-readme-history.md, docs/INDEX.md, docs/00-导读/W批次编号对账表.md, docs/00-导读/遗留总账.md, docs/00-导读/项目说明.md, docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md, docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md, docs/11-方案报告/计划方案/T137-任务计划执行与经验沉淀报告-2026-11-23.md, scripts/archive_segments.py, scripts/batch_cascade.py, scripts/batch_closeout.py, scripts/output/INDEX.md, scripts/output/README.md, scripts/output/_cascade_files_W1308.txt, scripts/output/_vermilion_solid_cache.json, scripts/output/_w1266_allrender.json, scripts/output/_w1308_spec.json, scripts/output/chart-legend-render-audit.json, scripts/output/file-index.md, scripts/output/stats-changelog.json, scripts/output/stats-index.md, scripts/output/stats.json, scripts/output/svg_text_contrast_graphic_report.json, scripts/output/svg_text_contrast_report.json, scripts/output/tools-inventory.md, site/data/cross-time-danmaku.html, site/data/search-index-zh.js, site/data/tag-cloud.html, site/en/search-index-en.js, site/dukou-engine.html, site/index.html, site/rss.xml, tests/unit/INDEX.md, tests/unit/README.md, tests/unit/test_archive_segments_migration_plan.py, tests/unit/test_batch_closeout_hash_repair.py, tests/unit/test_cascade_chain_entry_date_prefix.py, tests/unit/test_cascade_handover_rotate.py
>
> - **验证**：判据单测 **8 passed**（L-11）· 归档腾窗单测 **5 passed** · cascade 链首单测 **3 passed** · W1144 补滚单测 **3 passed** · 分组展开单测 **3 passed** · 5 行代改后 `is-ancestor` 全 True · 豁免基线剩余 **0 行** · 第 31 门禁 C4-g 判红 0 · 归档 dry-run 实测「两面各迁 2 段（W1253-W1255）·留存 48 段·同下界 W1256」· **门禁段数与阈值零放宽**（只加严不加松）。
>
> - **声明与实况不符项**：① 初判「L-12 需新增链末自检判据」⇒ 实测既有闸门已等效覆盖 ⇒ 改为不新增；② 初判「立式分组可承载 400+ 行登记面」⇒ 实测 `fi_group_rows` **只对同目录连续文件压缩**（跨目录 0%）⇒ 已据此修正 L-08 的可行路径；③ 初判「archive 失败是段数窗与体积窗不可兼得」⇒ 实测根因是**迁出量由 chunk 决定**而非两窗互斥 ⇒ 改为最小达标二分 + 两面同下界对齐迁出。
>
> - **状态**：**L-11 闭合 · 豁免基线清零 · L-12 转闭合（既有闸门覆盖）· 归档腾窗已使能**；**L-08 维持未清偿**（按用户裁决分 8 小批·W1309–W1315·归档腾窗前置条件已达成）；tmpe 冻结区等 48h 窗后清、8 张 JPG 原图保留本地。

### W1307（2026-11-23）：遗留清偿批 (L-08 目录件伪血缘治本 409 件一次清且此后幂等 + L-09/L-10 W1304 spec 对齐 + W1306 行 hash 回填)

> **来源**：用户 2026-11-23 指令「继续」（承接 W1306 遗留收敛判据批）⇒ 立项 W1307（遗留清偿批）。
>
> - **L-08 治本**：`scripts/gen_folder_docs.py` 两处**硬编码日期**（生成时点 2026-10-18 / 生成日期 2026-10-18）改为**不再写死日期**（指向本文件 git 提交时间）⇒ 全仓 **409 件目录件一次性刷新**（631 增 / 632 删·仅日期行）⇒ **伪血缘消除**且**此后 refresh 幂等**（此前每次 refresh 必改日期 ⇒ 「门禁自产残留」噪声源之一）。
>
> - **L-09/L-10 治本**：`_w1304_spec.json` 的 file_index_rows 剔除**越界行** `scripts/output/chart-legend-render-audit.md`（不在 W1304 提交树内）⇒ 31→30 行与提交实算**逐条相等**；同一 spec 的 changelog_body「文件」行按 `git show --name-only -z` 实算重写（16 项→30 项）⇒ 报告型文档与实况脱节修正；两面段经 `rebuild_section --batch W1304 --apply` 同步。
>
> - **W1306 行 hash 回填**：用仓内**独占回填工具** `ledger_backfill.py --w 1306 --hash a62b3cc54 --status …`（锁旧指纹→改→出新指纹 `02350f9286b3`）⇒ **C4-g 判据实测通过**（该 hash 在 main 历史链上）。
>
> - **文件**：.github/workflows/README.md, AGENTS.md, CHANGELOG.md, CITATION.cff, HANDOVER.md, STRUCTURE.md, archive/docs/AGENTS-ARCHIVE.md, archive/docs/W批次编号对账表-ARCHIVE.md, archive/docs/workflows-readme-history.md, docs/00-导读/W批次编号对账表.md, docs/00-导读/遗留总账.md, docs/00-导读/项目说明.md, docs/11-方案报告/README.md, docs/11-方案报告/计划方案/T136-任务计划执行与经验沉淀报告-2026-11-23.md, docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md, docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md, docs/INDEX.md, scripts/output/INDEX.md, scripts/output/README.md, scripts/output/_cascade_files_W1307.txt, scripts/output/_vermilion_solid_cache.json, scripts/output/_w1266_allrender.json, scripts/output/_w1304_spec.json, scripts/output/_w1307_spec.json, scripts/output/chart-legend-render-audit.json, scripts/output/stats-changelog.json, scripts/output/stats.json, scripts/output/svg_text_contrast_graphic_report.json, scripts/output/svg_text_contrast_report.json, scripts/output/tools-inventory.md, site/data/cross-time-danmaku.html, site/data/search-index-zh.js, site/data/tag-cloud.html, site/dukou-engine.html, site/en/search-index-en.js, site/index.html, site/rss.xml, site/sitemap.xml
>
> - **验证**：第 31 门禁 **0 FAIL**（C4-g 5 行存量悬空在豁免基线内 ⇒ NOTE）· 第 48 门禁计划方案模板 **PASS（全项符合）**· refresh 二次运行**零 diff**（幂等自证）· 台账正本 60 行（窗口内·登记前先归档已收官 W1243）· **判据与阈值零放宽**。
>
> - **声明与实况不符项**：① 初判 `ledger_backfill --w W1306` 报错为工具缺陷 ⇒ 实为**参数格式**（要整数）⇒ 已改正；② 本批属「订正」而非擅改历史段：W1304 spec 与其两面段按提交实算对齐，已在 T136 §九 声明。
>
> - **状态**：**遗留总账 L-08/L-09/L-10 三项治本闭合**（未清偿 5 → 2）· **L-11/L-12 维持未清偿**（涉收官链核心路径 `_run_backfill_prev_hash` 与链尾结构 ⇒ 独立批次治本）· 豁免基线 5 行他方悬空 hash 不代改。

### W1306（2026-11-23）：遗留收敛落机器判据 (C4-g 台账 hash 历史链有效性 + C4-h 审查 P2 编号化登记 + 收尾两分类声明)

> **来源**：用户 2026-11-23 追问「为什么每次结束都有遗留的任务要下一批去做？」⇒ 立项 W1306（遗留收敛落机器判据批）。
>
> - **问题归因（四类·见报告 §四）**：A 自指不可知（数学必然）· B 链外改动打破链内闭合（**本会话自造**）· C 压缩推送挤出历史链（并发共享面）· D 审查后置发现（P2 必留）。
>
> - **判据 3（治 C）**：第 31 门禁新增 **C4-g「台账 hash 历史链有效性」**——判定口径**必须**用 `git rev-list HEAD` 前缀匹配（`git rev-parse --verify` 只查对象库存在性 ⇒ 对被压缩掉的 commit **假阳性**）；**存量豁免基线**登记在遗留总账（5 行悬空 ⇒ 基线内 NOTE、基线外 FAIL ⇒ 判据上线不即红）。
>
> - **判据 4（治 D）**：第 31 门禁新增 **C4-h「审查 P2 编号化登记」**——现役段含 P2 而遗留总账「未清偿项」区无 L-xx 登记 ⇒ FAIL（**P2 不得只留在报告/聊天里**）；对抗审查模板同步补该义务；审查 P2 三项已登记为 **L-08/L-09/L-10**。
>
> - **判据 5（治自己造成的遗留）**：收官模板新增「**遗留两分类声明**」必填条款——① 我能单方面闭合的**必须为 0**（否则本批不得收官）② 需他人/用户裁决的列明编号与对象。
>
> - **文件**：CHANGELOG.md, HANDOVER.md, archive/docs/W批次编号对账表-ARCHIVE.md, docs/00-导读/W批次编号对账表.md, docs/00-导读/遗留总账.md, docs/agent/adversarial-audit-prompt.md, docs/agent/closeout-agent-prompt.md, scripts/check_doc_sync.py, tests/unit/test_doc_sync_ledger_hash.py, scripts/output/_w1306_spec.json, scripts/output/_cascade_files_W1306.txt, scripts/output/file-index.md, scripts/output/stats-changelog.json, scripts/output/stats-index.md, scripts/output/stats.json, scripts/output/tools-inventory.md, scripts/output/INDEX.md, scripts/output/README.md, tests/unit/INDEX.md, tests/unit/README.md, docs/INDEX.md
>
> - **验证**：`python scripts/check_doc_sync.py` **0 FAIL**（C4-g 5 行降为存量豁免 NOTE）· 新增单测 `tests/unit/test_doc_sync_ledger_hash.py` **5 passed**（台账 hash 定位·祖先前缀匹配·豁免基线两态·短 hash 前缀）· 台账写窗顶破按判据归档已收官 W1242 腾移（正本 59 行 + 本批认领行 = 60 行·窗口内）· **判据与阈值零放宽**（只加严不加松）。
>
> - **状态**：**3/5 条已落成机器判据**（判据 3/4/5）；**判据 1（自指不可知 ⇒ 自动回填扩到「错值」修指）与判据 2（收官链链末自检：链跑完后工作树必须干净）**涉及收官链核心路径，本批未动（风险高）⇒ 已登记为遗留总账 L-11/L-12 候补项，下一批单独治本。
>
> - **声明与实况不符项**：① 本批初判「豁免基线解析失败 ⇒ 判据有 bug」——实为**两处自身实现缺陷**（正则缺 `re.M` + 捕获组是纯数字而正本解析出 `W####`）⇒ 已修（并各有单测覆盖）；② 上一轮普查曾误报「悬空 hash 0 行」⇒ 实为**取错列**（hash 在第 4 段不是第 3 段）⇒ 已复核为 5 行。

### W1305（2026-11-22）：对抗审查 P0/P1 同批治本 (spec 大小写归一 + 台账 hash 合并口径 + 黏行无损还原 + T135 声明不符项更正)

> **来源**：W1305 对抗审查（独立只读 subagent·实跑像素级比对与历史链核验）报出 P0/P1 ⇒ 同批治本。
>
> - **P1-1 跨平台判据静默失效（真缺陷·本会话引入）**：`scripts/output/_w1302_spec.json` 用了**大写 W**（全仓 350+ spec 中唯一）⇒ Linux/macOS CI 上 `_w*_spec.json` 类 glob **匹配不到** ⇒ `check_commit_scope` 退化为「无 spec·不判」、`backfill_changelog`/`check_capacity_budget` 漏统计 ⇒ **判据静默失效（假绿）**。已 `git mv` 改回小写 `_w1302_spec.json` 并同步两面段登记（Windows 大小写不敏感正是它长期未暴露的原因）。
>
> - **P0-1 台账 hash 合并口径**：压缩推送使 **5 行** hash 悬空（不在 main 历史链上）——W1294/W1295/W1296/W1301/W1303；本会话认领的 **W1302** 已改指合并承载 commit `0c926a0aa`（`merge-base --is-ancestor` 实测 True），**W1304** 填真值 `2a123f53b`。他方认领的 4 行**不代改**（台账规则：只改本会话认领的行），只在 W1305 行登记待其回填。
>
> - **P0-2 黏行结构损坏（按原文无损还原）**：台账 W1303 行被截断（只剩 hash 列），其后 6 列被接到 W1304 行尾 ⇒ 已按原文**逐字还原**为两行（与 `0c926a0aa` 原文逐字符相等·审查实测 OLD==NEW）。
>
> - **P1-2 报告与实况不符项更正**：T135 报告 8 处表述更正 + 新增「§九 声明与实况不符项」小节（对抗审查实据：入站 06/11 与站内直层同名文件**同名不同物**（MAE 45.43 / 36.25·灰度相关 0.471 / 0.371）；`backup-v1/` 实为 **5472×3072 jpg 源件**·入站为转码降采样件；66 张 MD5 复扫**已不可复现**·如实标注）。
>
> - **文件**：CHANGELOG.md, HANDOVER.md, archive/docs/W批次编号对账表-ARCHIVE.md, docs/00-导读/W批次编号对账表.md, docs/11-方案报告/计划方案/T135-任务计划执行与经验沉淀报告-2026-11-22.md, scripts/output/_w1302_spec.json, scripts/output/_w1302_spec.json, scripts/output/_w1305_spec.json, scripts/output/_cascade_files_W1305.txt, scripts/output/file-index.md, scripts/output/INDEX.md, scripts/output/README.md, scripts/output/stats-changelog.json, scripts/output/stats-index.md, scripts/output/stats.json, scripts/output/tools-inventory.md
>
> - **验证**：`check_action_refs.py` PASS（97/97 uses 全 40-hex）· `check_doc_sync.py` 0 FAIL · `check_registration_surface --batch W1305` 六项全通过 · `check_pitfalls_split.py` 0 FAIL（421=421）· pytest 1827 passed · 远端 CI 6 workflow 全绿（2a123f53b）。
>
> - **声明与实况不符项**：① 本批初判「合并推送＝merge·历史保留·hash 无一失效」——实测 `git log -1 --format=%P 0c926a0aa` **只有 1 个父** ⇒ 是压缩推送，原 commit 退出历史链（**已两次自我更正**）；② `git rev-parse --verify` 判 hash 有效是**假阳性**（只查对象库存在性·悬空对象也能解析）⇒ 正确口径是 `git merge-base --is-ancestor`；③ T135 原称 06/11 为「同场景不同压缩版」——像素级比对证明是**两张不同的画**（已在 §九 更正）。
>
> - **状态**：**对抗审查 P0/P1 同批治本完毕**（spec 大小写归一 + 台账 hash 合并口径 + 黏行无损还原 + 报告 6 处声明更正）；**P2 项**（INDEX/README 血缘元信息硬编码日期、spec 越界登记 1 行、changelog_body 文件清单缺版本面件）登记待下一批。

### W1304（2026-11-22）：修 W1301 遗留根因 (actions/cache restore+save 钉 40-hex full SHA·Workflow Lint 红灯治本)

> **来源**：W1301/W1302/W1303 合并推送（`0c926a0aa`）后，远端 **Workflow Lint 红灯**——根因是 W1301 引入的 CI 跨 run 缓存两处 action 引用**未钉 40 位 full SHA**（`actions/cache/restore@v4` · `actions/cache/save@v4`），违反仓内铁律 W663/T4（action 一律钉 40-hex full SHA）。
>
> - **执行**：两处 `uses:` 改为 `actions/cache/restore@0057852bfaa89a56745cba8c7296529d2fc39830` 与 `actions/cache/save@0057852bfaa89a56745cba8c7296529d2fc39830`（`actions/cache` v4 tag 指向的 commit SHA·经 GitHub API 实查）；**判据与强度一字未改**，仅把 tag 引用钉成不可变 SHA（与仓内其余 95 条 uses 同口径）。
>
> - **文件**：.github/workflows/README.md, .github/workflows/ci.yml, AGENTS.md, CHANGELOG.md, CITATION.cff, HANDOVER.md, README.md, STRUCTURE.md, archive/docs/AGENTS-ARCHIVE.md, archive/docs/W批次编号对账表-ARCHIVE.md, archive/docs/workflows-readme-history.md, docs/00-导读/W批次编号对账表.md, docs/00-导读/项目说明.md, scripts/output/INDEX.md, scripts/output/README.md, scripts/output/_cascade_files_W1304.txt, scripts/output/_vermilion_solid_cache.json, scripts/output/_w1266_allrender.json, scripts/output/_w1304_spec.json, scripts/output/chart-legend-render-audit.json, scripts/output/file-index.md, scripts/output/stats.json, scripts/output/svg_text_contrast_graphic_report.json, scripts/output/svg_text_contrast_report.json, scripts/output/tools-inventory.md, site/data/cross-time-danmaku.html, site/data/tag-cloud.html, site/dukou-engine.html, site/index.html, site/rss.xml
>
> - **验证**：本地 `python scripts/check_action_refs.py` **PASS**（97 条 uses 全为 40 位 full SHA · 去重 16 个 repo/ref · shell 面「不可变引用」形态 PASS）；`ci.yml` **YAML 解析 OK**（12 jobs）；远端 Workflow Lint 由 failure 转绿由本轮 CI 实证。
>
> - **状态**：**根因治本**（非豁免压红）——两处未钉 SHA 是 W1301 的实引入缺陷，本批按「修实例必修根」同批治本；台账写窗顶破（正本 60 行）按判据归档已收官 W1240 腾移，正本留 59 行 + 本批认领行 = 60 行（窗口内），**未放宽任何阈值**。

### W1303（2026-11-22）：西游小游戏三合一与十八款合集入口

**本批要点**（W1303 西游小游戏三合一与十八款合集入口）：

> - **三合一游戏页**：`assets/game/journey-trials.html` + `journey-trials.css` + `js/*.js`（core/main/action/roguelike/cards）。护师西行 Canvas 2D 横版动作，三试三 Boss，另含修罗挑战与无尽循环；八十一难轻 Roguelike，行者选择（悟空/八戒/沙僧）、十二/十八难、途中事件与法宝；卡牌斗法五阵，前四阵随机、二郎神压轴并带天眼通。
> - **十八款合集入口**：`assets/game/index.html` + `index.css` + `index.js`，收录既有 15 款与本次 3 个独立入口；分类筛选、搜索、排序、随机一款、战绩与最近玩过；支持 `journey-trials.html#action|#rogue|#cards` 深链。
> - **体验层**：WebAudio 合成音效与静音开关；移动端横屏提示、全屏入口；战绩写入 localStorage；技能效果清单与角色卡技能摘要；所有数据内嵌，file:// 离线可玩，零外域依赖。
> - **文件**：assets/game/journey-trials.html, assets/game/journey-trials.css, assets/game/js/core.js, assets/game/js/main.js, assets/game/js/action.js, assets/game/js/roguelike.js, assets/game/js/cards.js, assets/game/index.html, assets/game/index.css, assets/game/index.js, scripts/output/_w1303_spec.json。
> - **验证**：全部 JS `node --check` 通过；Playwright `file://` 桌面与 430×844 移动端实测三模式与合集，控制台 0 错误、无横向溢出；无尽轮次切换、十八难事件触发、五阵随机顺序与行者增益均实测通过。
> - **落位说明**：按既有 15 款小游戏惯例落在 `assets/game/`，不进 `site/data/` 与站点导航；`assets/game/` 受 `.git/info/exclude` 本地忽略，本批文件以 `git add -f` 入库。


### W1302（2026-11-22）：hero-batch 绢本源件入站 (8 张 webp 1920×1078 → site/static/images/silk-src/ · 哈希+目视双证甄别)

> **来源**：用户 2026-11-22 指令「先把 hero-batch 素材入仓」⇒ 立项 W1302（hero-batch 绢本源件入站批）。
>
> - **取证**：hero-batch = W1253–W1258「丝路 hero / OG 接缝修法」工作区（CHANGELOG 段与文件 mtime 11-16 吻合）；**66 张图逐张 MD5 复扫 = 2 HIT / 64 MISS**，2 处 HIT 即 `og-03-v5E` == 站内 `og-silk-hero-03-ye-talin.webp`、`og-12-v5G` == 站内 `og-silk-hero-12-jinghu.webp` ⇒ **成品已在校验命中**；**目视核验**：`asset-dark/light-*.png` 实为 **2000×1174 的「4 场景 2×2 整批拼版」**（非单张资产）、`review/trim-review-*.png` 为 2400×1356 全批总览 ⇒ 38 张属评审对照证据；`backup-v1/` 8 组 1920×1078 绢本场景（白骨精 / 山阳行路等）经目视与站内 `og-silk-hero-04/08/10`（另一组山水构图）**内容不同** ⇒ 站内缺失组。
>
> - **施工**：8 张高分辨率 webp（3.61 MB）移入 `site/static/images/silk-src/`（同卷 rename·体积逐一吻合）；**用户裁决范围**：仅 webp 入站，JPG 原图（8 张 52.78 MB）不入库；台账认领行 + `preflight_check` **PASS**（首次 FAIL：台账正本 61 段 > 60 窗口 ⇒ 按判据跑 `archive_ledger_rows.py --apply` 迁出已收官 W1238–W1239 两行腾窗 ⇒ 正本留 59 行 ⇒ 复跑 PASS，**未放宽任何判据**）。
>
> - **文件**：STRUCTURE.md, docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md, docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md, site/static/images/silk-src/silk-hero-04-baigu-furen.webp, site/static/images/silk-src/silk-hero-05-huoyanshan-yaowang.webp, site/static/images/silk-src/silk-hero-06-heifengshan.webp, site/static/images/silk-src/silk-hero-07-dumu-qiao.webp, site/static/images/silk-src/silk-hero-08-shanye-xinglu.webp, site/static/images/silk-src/silk-hero-09-wukong-tanyu.webp, site/static/images/silk-src/silk-hero-10-jingubang.webp, site/static/images/silk-src/silk-hero-11-fabao-sanjian.webp, site/static/images/INDEX.md, site/static/images/silk-src/INDEX.md, docs/11-方案报告/计划方案/T135-任务计划执行与经验沉淀报告-2026-11-22.md, docs/11-方案报告/README.md, HANDOVER.md, docs/00-导读/W批次编号对账表.md, archive/docs/W批次编号对账表-ARCHIVE.md, CHANGELOG.md, docs/INDEX.md, scripts/output/_w1302_spec.json, scripts/output/_cascade_files_W1302.txt, scripts/output/file-index.md, scripts/output/stats.json, scripts/output/stats-index.md, scripts/output/stats-changelog.json, scripts/output/tools-inventory.md, scripts/output/INDEX.md, scripts/output/README.md, site/data/search-index-zh.js, site/en/search-index-en.js, site/sitemap.xml
>
> - **验证**：8 张落位核对体积逐一吻合（538.7 / 397.4 / 576.9 / 379.7 / 553.5 / 456.8 / 312.7 / 479.8 KB）· `git status` 新增路径仅 `site/static/images/silk-src/`（未触任何既有页面/脚本）· 哈希复扫与目视结论互相印证 · 全量门禁 0 FAIL。
>
> - **状态**：**素材唯一副本已保住并入公开仓**；本批同时**纠正了上一轮评估的过宽表述**——「hero-batch 含未入仓唯一成品」实为「成品已在校验命中，缺的是源件组」；其余 38 张评审拼版 + 18 张迭代版 + 8 张 JPG 原图按用户裁决不入库（留 tmpe 待清理）。

### W1301（2026-11-22）：L-02 探针跨run增量缓存（332s→0s·三重键·判据零改动·CI跨run携带）

> **来源**：用户 2026-11-22 指令「先开工 L-07 之后再开工 L-02」⇒ 立项 W1301（L-02 治本批）。
>
> - **执行**：探针新增**页级增量缓存**，键为**三重闸**（页内容 sha + 探针脚本自身 sha + 口径元数据：阈值/底色口径/扫描面/状态集/工具开关）⇒ 页面未变即复用该页采集结果；**口径或探针逻辑一变即全量失效重采**（fail-closed·防假绿）；**报告结构一字未改 ⇒ 第 80 槽判据零改动**；缓存**只收稳定行**（fatal/unstable 不入缓存·不固化坏状态）；CI 用 actions/cache restore + **显式 save**（命中不更新·须强制写回）跨 run 携带；缓存件**不入库**（.gitignore 排除·本地与 CI 互不污染·且天然规避跨环境渲染差异被跨环境复用）。
>
> - **文件**：.github/workflows/ci.yml, .gitignore, docs/00-导读/W批次编号对账表.md, docs/00-导读/遗留总账.md, docs/11-方案报告/README.md, docs/11-方案报告/计划方案/T134-任务计划执行与经验沉淀报告-2026-11-22.md, docs/INDEX.md, scripts/output/INDEX.md, scripts/output/README.md, scripts/output/_cascade_files_W1301.txt, scripts/output/_w1266_allrender.json, scripts/output/_w1301_spec.json, scripts/output/chart-legend-render-audit.json, scripts/output/chart-legend-render-audit.md, scripts/output/file-index.md, scripts/output/stats-changelog.json, scripts/output/stats-index.md, scripts/output/stats.json, scripts/output/svg_text_contrast_graphic_report.json, scripts/output/svg_text_contrast_report.json, scripts/output/tools-inventory.md, scripts/svg_text_contrast_probe.js, site/data/search-index-zh.js, site/en/search-index-en.js, site/sitemap.xml
>
> - **验证**：本地 graphic 口径全站 **332s → 0s**（第二次命中 672 行·浏览器未启动）· 第 80 槽 **0 FAIL** · 探针自测 **13/13** · 工作树干净（缓存件已排除）。
>
> - **状态**：**L-02 ✅ 闭合** ⇒ **遗留总账未清偿归零**（L-01～L-07 全闭合·自 W1296 建立以来首次归零）；本轮 CI 因探针脚本变更仍走全量·增量收益自下一轮 CI 起显现。

### W1300（2026-11-22）：L-07 公共口径多批次锚漏计治本（本体275→276·反查表补E-291·私有正则退役）

> **来源**：用户 2026-11-22 指令「先开工 L-07 之后再开工 L-02」⇒ 立项 W1300（L-07 治本批）。
>
> - **执行**：① **公共本体口径治本**——check_pitfall_id_unique.RX_ENTRY 扩为支持**并列多批次锚**（锚内多个批次号·取**首个**·与归档段头同序）⇒ 多批次锚条目（实测 E-291）不再被漏判 ⇒ 本体 E 号 **275 → 276**（重号 0）；② **口径收敛为单一事实源**——check_pitfalls_split 的私有扩展正则 RX_ENTRY_MULTI **退役**（W1299 为隔离连锁面而立的临时分叉·公共口径修好后必须退役·防两份正则各自漂移）⇒ 镜像侧改引公共 RX_ENTRY；③ **反查表补齐**——CSS 小节在 E-289 与 E-292 之间插入 E-291（该行 8 → 9 个·守「每行 10 个」约定）⇒ 反查表 333 → 334 条 / 去重 276（遗漏 0 多余 0）；④ **回归锁改口径**——W1299 那条用例改断言「公共口径认并列锚且取首个批次号 + 私有正则已退役」（**函数名不动**·api_diff 判据把 tests/ 下 test 函数当公开 API）；⑤ **更正上一批表述**——W1299 称「stats 421 ⇒ 真实 422」**不成立**（stats 实测口径＝数「- **」行·本就含 E-291 ⇒ 421 无误）⇒ 真正问题是「本体 E 号集合」与「条目行实测」两套坑位身份口径不一致。
>
> - **文件**：.github/workflows/README.md, AGENTS.md, CHANGELOG.md, CITATION.cff, HANDOVER.md, README.md, STRUCTURE.md, archive/docs/AGENTS-ARCHIVE.md, archive/docs/workflows-readme-history.md, docs/00-导读/W批次编号对账表.md, docs/00-导读/遗留总账.md, docs/00-导读/项目说明.md, docs/11-方案报告/README.md, docs/11-方案报告/计划方案/T133-任务计划执行与经验沉淀报告-2026-11-22.md, docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md, docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md, docs/INDEX.md, pitfalls.md, scripts/check_pitfall_id_unique.py, scripts/check_pitfalls_split.py, scripts/output/INDEX.md, scripts/output/README.md, scripts/output/_cascade_files_W1300.txt, scripts/output/_vermilion_solid_cache.json, scripts/output/_w1266_allrender.json, scripts/output/_w1291_exemption_audit.json, scripts/output/_w1300_spec.json, scripts/output/chart-legend-render-audit.json, scripts/output/chart-legend-render-audit.md, scripts/output/file-index.md, scripts/output/stats-changelog.json, scripts/output/stats-index.md, scripts/output/stats.json, scripts/output/svg_text_contrast_graphic_report.json, scripts/output/svg_text_contrast_report.json, scripts/output/tools-inventory.md, site/data/cross-time-danmaku.html, site/data/search-index-zh.js, site/data/tag-cloud.html, site/dukou-engine.html, site/en/search-index-en.js, site/index.html, site/rss.xml, site/sitemap.xml, tests/unit/test_pitfalls_split.py
>
> - **验证**：坑表六主题判据 0 FAIL（C2/C3 421/421·C4 遗漏 0 多余 0·C5 孤儿 0·C6 276/276 重号 0）· 第 31 槽 0 FAIL · test_pitfalls_split.py 15 passed · test_w1106_pitfall_id_unique.py 3 passed· 两面下界仍 W1253 ✓。
>
> - **状态**：**L-07 ✅ 闭合** ⇒ **遗留总账未清偿降至 1 项**（L-02 探针跨 run 增量缓存·下一批）。

### W1299（2026-11-22）：L-04① 归档孤儿段清偿（13→0·三类根因分别治本·回归锁+3·负例去硬编码）

> **来源**：用户 2026-11-22 指令「然后呢」⇒ 在 W1298 收官后按《遗留总账》继续推进剩余项。
>
> - **执行**：把「归档层 13 个孤儿段」按**三类根因**分别治本——**A 口径误报 11 段**（正本自带完整叙事但非指针型 ⇒ C5 的 referenced 只记指针型 ⇒ 判成「无人指向的孤儿段」）⇒ referenced 口径改为「正本存在该 E 号条目即算」；**B 多批次锚 1 段**（E-291 锚为「W1284/W1285」）⇒ 镜像侧新增扩展正则 RX_ENTRY_MULTI（取首个批次号·**公共 RX_ENTRY 不动**·连锁面隔离）；**C 真孤儿 1 段**（E-283 正本确实无条目·仅被 E-288 反向引用）⇒ 从归档段**逐字**迁入正本 css-visual.md；⇒ 孤儿段 **13 → 0**；连带同步正本段头声明 / 索引壳声明 / 反查表（每行 10 个）/ stats 计数链；新增 3 条回归锁；既有 5 处负例硬编码「当前条数」去化（bump_declared 自动取当前值）。
>
> - **文件**：.agent/skills/puti-shouye/SKILL.md, .github/workflows/README.md, AGENTS.md, CHANGELOG.md, CITATION.cff, HANDOVER.md, README.md, STRUCTURE.md, archive/docs/AGENTS-ARCHIVE.md, archive/docs/W批次编号对账表-ARCHIVE.md, archive/docs/workflows-readme-history.md, docs/00-导读/W批次编号对账表.md, docs/00-导读/遗留总账.md, docs/00-导读/项目说明.md, docs/11-方案报告/README.md, docs/11-方案报告/计划方案/T132-任务计划执行与经验沉淀报告-2026-11-22.md, docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md, docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md, docs/INDEX.md, docs/agent/pitfalls-topics/cascade-changelog.md, docs/agent/pitfalls-topics/css-visual.md, docs/agent/pitfalls-topics/data-trust.md, docs/agent/pitfalls-topics/flow-collab.md, docs/agent/pitfalls-topics/git-concurrency.md, docs/agent/pitfalls-topics/js-csp-runtime.md, docs/agent/pitfalls.md, pitfalls.md, pytest.ini, scripts/check_pitfalls_split.py, scripts/output/INDEX.md, scripts/output/README.md, scripts/output/_cascade_files_W1299.txt, scripts/output/_vermilion_solid_cache.json, scripts/output/_w1266_allrender.json, scripts/output/_w1299_spec.json, scripts/output/chart-legend-render-audit.json, scripts/output/chart-legend-render-audit.md, scripts/output/file-index.md, scripts/output/stats-changelog.json, scripts/output/stats-index.md, scripts/output/stats.json, scripts/output/svg_text_contrast_graphic_report.json, scripts/output/svg_text_contrast_report.json, scripts/output/tools-inventory.md, site/data/cross-time-danmaku.html, site/data/search-index-zh.js, site/data/tag-cloud.html, site/dukou-engine.html, site/en/search-index-en.js, site/index.html, site/rss.xml, site/sitemap.xml, tests/unit/test_pitfalls_split.py
>
> - **验证**：坑表六主题判据 0 FAIL（C2/C3 421/421·C4 遗漏 0 多余 0·C5 孤儿 0·C6 275/275 重号 0）· test_pitfalls_split.py 15 passed（原 12 + 新 3）· 两面下界仍 W1253 ✓。
>
> - **状态**：**L-04① 全闭合**（4/4）；**L-07 新登记**（公共 RX_ENTRY 对多批次锚漏计 ⇒ 坑位总数少算·改公共口径连带反查表/stats/AGENTS 计数链·单独批）⇒ 未清偿仍 2 项（L-02 / L-07）。

### W1298（2026-11-22）：清零批续: L-03 台账hash自动回填 + L-04② E-185正文补齐 + L-05 verify断言源普查

> - **来源**：用户 2026-11-22 指令「核验 W1297 CI 终态，并按遗留总账一次完成剩余 L-02～L-06」⇒ 立项 W1298（清零批续）。
> - **执行**：① **L-03 自动化（物理约束的唯一正解）**——台账 hash「每批必然欠一笔」（提交含自身 hash ⇒ 同笔内写不对自己的 hash ⇒ 自指不可知）此前靠人工记着做 ⇒ 常态化漏 ⇒ 新增 `batch_closeout._run_backfill_prev_hash`（收官链 content_stage 开头自动扫「已收官 + hash 空缺」行 ⇒ 按 `git log --all --reverse` 取该 W **首笔**提交 ⇒ 调 `ledger_backfill --w --hash`）⇒ **只用 --hash 不传 --status ⇒ 状态列的详细终态结论不丢**（W1289 教训）⇒ **实测一次补齐 W1292–W1296 五行**；② **L-04② E-185 正文补齐**——归档段自述「原归档缺失·W1290 时判据层仅存标题·正文空」⇒ **叙事全文不可考** ⇒ 判据层改写成**独立可执行纪律**（① 仲裁读数先固定目标 ref 的树再读·禁读工作树 ② 段定位用双锚（W 号 + 段内唯一串）·单锚命中即视为未定位（fail-closed）③ 并行期同号段并存时以 W 号 + 会话标识双锚区分·禁「按号取第一条」）+ 归档层**只追加**同步（镜像契约成立）；③ **L-04③ 双壳评估**——根壳（索引 + E-NN 反查）与 docs 壳（历史相对链接兼容）受众不同 ⇒ **保留双壳·不收敛**（记录理由防后人误判为冗余而删）；④ **L-04④ 反查表定策**——改为**按主题分组 + E 号区间化** ⇒ 增长转近常量；⑤ **L-05 普查结论**——`verify_delivery.py` **每个门禁段都带 marker_msg「缺汇总行 ⇒ 判红·防静默跳过」**（逐段核查 60+ 段）⇒ **未发现「断言源缺失 ⇒ 静默跳过」的未知盲区**；显式降级仅 **3 处**：A1-A6 计数（**W1291 已修**）· 学术引用（无该轨文档⇒跳过）· sitemap（缺失⇒跳过）——后两者属「资源不存在的合理跳过」⇒ 不是盲区；⑥ 报告 T131 落盘 + README §六 登记（146→147 件）。
> - **验证**：L-03 实测**命中并回填 5 行**（W1292/W1293/W1294/W1295/W1296·状态列未动）· E-185 正本与归档同步 · 坑表 7 项判据（C5 镜像）0 FAIL · 普查结论逐段可核 · 两面下界仍 **W1253 ✓** · 收官链零跳过完成 + 全量门禁 0 FAIL + pytest 全绿 + 一次推送带齐 1 笔 ⇒ 1 轮 CI。
> - **状态**：**遗留总账未清偿由 6 项降至 2 项**——L-03（机器化）、L-05（普查无盲区）、L-04②③④ 闭合；剩余 **L-02**（探针跨 run 增量缓存——探针**现无任何缓存机制**·脚本级从零实现 + CI 双验）与 **L-04①**（归档 13 个孤儿段·多批次锚形态需改 `RX_ENTRY` 判据口径）**如实留账**于总账⇒ 单独批执行。
> - **文件**： .github/workflows/README.md, AGENTS.md, CHANGELOG.md, CITATION.cff, HANDOVER.md, README.md, STRUCTURE.md, archive/docs/AGENTS-ARCHIVE.md, archive/docs/W批次编号对账表-ARCHIVE.md, archive/docs/pitfalls-detail-ARCHIVE.md, archive/docs/workflows-readme-history.md, docs/00-导读/W批次编号对账表.md, docs/00-导读/遗留总账.md, docs/00-导读/项目说明.md, docs/11-方案报告/README.md, docs/11-方案报告/计划方案/T131-任务计划执行与经验沉淀报告-2026-11-22.md, docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md, docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md, docs/INDEX.md, docs/agent/pitfalls-topics/flow-collab.md, pytest.ini, scripts/batch_closeout.py, scripts/output/INDEX.md, scripts/output/README.md, scripts/output/_cascade_files_W1298.txt, scripts/output/_vermilion_solid_cache.json, scripts/output/_w1266_allrender.json, scripts/output/_w1298_spec.json, scripts/output/chart-legend-render-audit.json, scripts/output/chart-legend-render-audit.md, scripts/output/file-index.md, scripts/output/stats-changelog.json, scripts/output/stats-index.md, scripts/output/stats.json, scripts/output/svg_text_contrast_graphic_report.json, scripts/output/svg_text_contrast_report.json, scripts/output/tools-inventory.md, site/data/cross-time-danmaku.html, site/data/search-index-zh.js, site/data/tag-cloud.html, site/dukou-engine.html, site/en/search-index-en.js, site/index.html, site/rss.xml, site/sitemap.xml, tests/unit/test_w1102_batch_closeout.py, tests/unit/test_w1114_version_surface.py

### W1297（2026-11-22）：L-01 治本: 刷新步固化进收官链 + 页面变更来源根因定位

> - **来源**：用户 2026-11-22 指令「执行 W1297 清零批：**先定位页面变更来源**，再按遗留总账一次完成 L-01～L-06 并验证 CI 终态」⇒ 立项 W1297。
> - **执行**：① **根因定位（git 历史级证据·非假设）**——`git log -- site/` 显示 W1295/W1296 两笔**各改 4 个页面页脚各 1 行**（cross-time-danmaku / tag-cloud / dukou-engine / index + 2 个搜索索引）⇒ **版本面推进 = 改页来源** ⇒ 页面 sha 必变 ⇒ 入库探针报告 + 渲染档案**每批必过期** ⇒ 第 80/82 槽 fail-closed 新鲜度检测**必然判红**（W1292→W1296 连续五批实证·此前每批靠人记得重跑）；**两个假设被证伪**：① 跨平台行尾口径（`.gitattributes` 已是 `* text=auto eol=lf` ⇒ 工作树恒 LF 且判据侧 `page_sha` 已 LF 归一）② 报告结构缺字段（两份报告均含 `page_sha`·graphic 168 / body 162）；**上一轮的反证本身不成立**（据「工作树 site/ 与 HEAD 一致」称假设被证伪——实为 amend 已把刷新产物一并提交⇒工作树干净）⇒ 已据实更正报告与总账；② **L-01 治本落地**——`batch_closeout.py` 新增 `_run_refresh_artifacts`（graphic 探针 → body 探针 → 渲染复核豁免页模式 → 渲染复核 --all → git add 5 产物 → **校验第 80/82 槽新鲜度**·任一红即 fail-closed 中断链）+ 插入点 **versions 之后**（页脚定稿后·自带 add·dry 跳过）⇒ **此后收官后入库产物必然新鲜**；③ 报告 T130 落盘 + README §六 登记（145→146 件）。
> - **验证**：根因有 git 历史实证（W1295/W1296 两笔各改 4 页页脚各 1 行）· 两个替代假设被证伪并留证 · 刷新步新函数 L595 + 调用点 L677（versions 之后）· `py_compile` 语法 OK · dry 跳过分支在位 · 遗留总账 L-01 已据实更正；两面下界仍 **W1253 ✓**；收官链零跳过完成（**本批链内自动跑了刷新步**⇒治本生效的直接验证）+ 全量门禁 0 FAIL + pytest 全绿 + 一次推送带齐 1 笔 ⇒ 1 轮 CI。
> - **状态**：**L-01（唯一的流水线自产类欠账）已治本**——刷新步固化进收官链后，收官完成时入库产物必然新鲜 ⇒ 「本地全绿 CI 恒红」这一类红灯不再可能靠人记忆避免；代价已如实登记：收官链 **+约 20 分钟**（本地跑两个浏览器探针 + 渲染复核）⇒ 换掉「每批一次陈旧红灯 + 一轮返工 CI」；根因描述与上一轮的错误反证已据实更正。
> - **文件**： .github/workflows/README.md, AGENTS.md, CHANGELOG.md, CITATION.cff, HANDOVER.md, README.md, STRUCTURE.md, archive/docs/AGENTS-ARCHIVE.md, archive/docs/W批次编号对账表-ARCHIVE.md, archive/docs/workflows-readme-history.md, docs/00-导读/W批次编号对账表.md, docs/00-导读/遗留总账.md, docs/00-导读/项目说明.md, docs/11-方案报告/README.md, docs/11-方案报告/计划方案/T130-任务计划执行与经验沉淀报告-2026-11-22.md, docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md, docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md, docs/INDEX.md, scripts/batch_closeout.py, scripts/output/INDEX.md, scripts/output/README.md, scripts/output/_cascade_files_W1297.txt, scripts/output/_w1266_allrender.json, scripts/output/_w1297_spec.json, scripts/output/chart-legend-render-audit.json, scripts/output/chart-legend-render-audit.md, scripts/output/file-index.md, scripts/output/stats-changelog.json, scripts/output/stats-index.md, scripts/output/stats.json, scripts/output/svg_text_contrast_graphic_report.json, scripts/output/svg_text_contrast_report.json, scripts/output/tools-inventory.md, site/data/cross-time-danmaku.html, site/data/search-index-zh.js, site/data/tag-cloud.html, site/dukou-engine.html, site/en/search-index-en.js, site/index.html, site/sitemap.xml

### W1296（2026-11-22）：建立遗留总账 + 欠账根因三分类 + 清零批立项

> - **来源**：用户 2026-11-22 追问「**继续做，为什么每次都要遗留？**」⇒ 立项 W1296（遗留总账建立 + 清零批立项批）。
> - **执行**：① **欠账取证与根因三分类**——遗留散在四个面（治理数字 / 工具 / CI / 坑表）且每批只吃 1-2 个面 ⇒ **队列滚动**且全局剩余不可见；逐项判定「是否每批重新产生」⇒ **① 流水线自产**（收官链版本面推进每批改页脚 ⇒ 探针报告 + 渲染档案每批必过期 ⇒ 每批被第 80/82 槽红拦一次·W1292→W1295 连续四批实证 ⇒ **不改造收官链就永远有**）**② 物理约束**（提交内容含自身 hash ⇒ 同笔内写不对自己的 hash ⇒ 台账 hash 每批必然欠一笔回填·E-311 ⇒ **不可消除·只能自动化**）**③ 一次性欠账**（N1–N5 / 归档工具段表口径 / CHANGELOG 结构散落 / 快档缺档 / 归档体积 ⇒ W1291–W1295 已分别清偿）；② **建立遗留总账**（新建 `docs/00-导读/遗留总账.md`）——全仓未清偿项**唯一可见账本**（未清偿含归因与计划批次 / 已清偿含机器证据 / 清零承诺口径 / 维护纪律四条）；③ **L-01 治本落点定稿**（读 `scripts/batch_closeout.py` 的 `STEPS` L27–44 实证）——刷新步插在 **versions 之后**（页脚定稿后）、**最后一次 add 之后**（产物入暂存）·该步自带 add ⇒ 之后入库产物必然新鲜 ⇒ **陈旧类红灯从根上消失**；④ **L-03 自动化落点定稿**——台账 hash 回填由「下批第一动作的人工纪律」改为**收官链自动回填上批 hash**（自指不可知 ⇒ 仍需下一笔·但由机器执行）；⑤ 报告 T129 落盘 + README §六 登记（144→145 件）。
> - **验证**：欠账取证逐项判定（是否每批重新产生）+ `batch_closeout.STEPS` 行级实证落点；总账文件落盘（含未清偿 6 项 / 已清偿 10 项含机器证据 / 清零承诺 / 维护纪律）；台账 W1296 认领行已加；两面下界仍 **W1253 ✓**；收官链零跳过完成 + 全量门禁 0 FAIL + pytest 全绿 + 一次推送带齐 1 笔 ⇒ 1 轮 CI。
> - **状态**：**把「为什么每批都有遗留」从模糊感受变成可核对的三类归因 + 一个仓内总账 + 一个清零承诺**——真正需要「一直修」的只有一类**流水线自产**（收官链固化刷新）与一类**物理必然**（hash 自指·只能自动化）；其余一次性欠账已在 W1291–W1295 清偿完毕；**下一批（W1297·清零批）按总账一次做完 L-01~L-06** ⇒ 清零后常态只剩 L-03 一条机器动作。
> - **文件**： .github/workflows/README.md, AGENTS.md, CHANGELOG.md, CITATION.cff, HANDOVER.md, README.md, STRUCTURE.md, archive/docs/AGENTS-ARCHIVE.md, archive/docs/W批次编号对账表-ARCHIVE.md, archive/docs/workflows-readme-history.md, docs/00-导读/INDEX.md, docs/00-导读/W批次编号对账表.md, docs/00-导读/遗留总账.md, docs/00-导读/项目说明.md, docs/11-方案报告/README.md, docs/11-方案报告/计划方案/T129-任务计划执行与经验沉淀报告-2026-11-22.md, docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md, docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md, docs/INDEX.md, scripts/output/INDEX.md, scripts/output/README.md, scripts/output/_cascade_files_W1296.txt, scripts/output/_w1266_allrender.json, scripts/output/_w1296_spec.json, scripts/output/chart-legend-render-audit.json, scripts/output/file-index.md, scripts/output/stats-changelog.json, scripts/output/stats-index.md, scripts/output/stats.json, scripts/output/svg_text_contrast_graphic_report.json, scripts/output/svg_text_contrast_report.json, scripts/output/tools-inventory.md, site/data/cross-time-danmaku.html, site/data/search-index-zh.js, site/data/tag-cloud.html, site/dukou-engine.html, site/en/search-index-en.js, site/index.html, site/sitemap.xml

### W1295（2026-11-22）：探针两口径在 CI 内并行化

> - **来源**：用户 2026-11-22 引用 W1294 遗留清单并指示「**现在做**」⇒ 立项 W1295（CI 提速批）。
> - **执行**：① **先测量再优化**——取 W1290 run 的 step 级耗时（gh api 取 jobs）：Delivery Gate **1109s（占 63%）**、其中 graphic 探针 **343s** + body 探针 **339s** = **682s（占全 CI 39%）**，而**依赖安装合计仅 55s（3%）**、单测已分 3 shard、6 个 workflow 已有 paths 过滤 ⇒ 通用优化清单（缓存/并行/路径过滤）**本仓早已到位·照抄会完全错过真大头**；② **两口径并行化**——graphic（--scope all）与 body（--scope data,en）**互不依赖**（扫不同页集）且**写不同报告文件** ⇒ 原先两个 step 串行 ⇒ 合并为**单 step 内 bash `&` + `wait`** ⇒ 墙钟从和变 max ⇒ **省 ≈5m43s**；**判据强度一字未动**（page_sha 覆盖与口径判定未动·第 80 槽 fail-closed 仍由入库产物承担）；③ **ci_sim 仿真序列同步**——CI_STEPS 两条探针项加注「串行等价·真实 CI 为并行」（Windows 本地无 POSIX `&`/`wait` ⇒ 仿真验证的是「产物 + page_sha 覆盖」这条**正确性链**·加速形态属 CI 墙钟面）；④ **顺带核实遗留③已完备**——快档已含第 80 槽（探针新鲜度）与第 82 槽（渲染档案 sha）⇒ **实证：W1294 的 push 正被快档第 82 槽当场拦下** ⇒ 快档对「陈旧类红灯」确有实效 ⇒ 无需再补；⑤ 报告 T128 落盘 + README §六 登记（143→144 件）。
> - **验证**：ci.yml **YAML 解析 OK**（12 jobs）· 并行段含两条 node 探针 & + wait · ci_sim CI_STEPS 已同步并注释差异 · 探针参数（--scope/--out/--bg-mode）与判据文本未动 ⇒ 判据强度不变 · 两面下界仍 **W1253 ✓** · 收官链零跳过完成 + 全量门禁 0 FAIL + pytest 全绿 + 一次推送带齐 1 笔 ⇒ 1 轮 CI。
> - **状态**：CI 的最大单项（探针 682s·39%）由**串行改并行**，预期省 ≈5m43s；通用清单里本仓已到位的三项（缓存/并行/路径过滤）**不动**（避免无效改动）；遗留③经核实**早已完备**（快档两个新鲜度档齐备且当场拦下过真实陈旧）。
> - **文件**： .github/workflows/README.md, .github/workflows/ci.yml, AGENTS.md, CHANGELOG.md, CITATION.cff, HANDOVER.md, README.md, STRUCTURE.md, archive/docs/AGENTS-ARCHIVE.md, archive/docs/workflows-readme-history.md, docs/00-导读/W批次编号对账表.md, docs/00-导读/项目说明.md, docs/11-方案报告/README.md, docs/11-方案报告/计划方案/T128-任务计划执行与经验沉淀报告-2026-11-22.md, docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md, docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md, docs/INDEX.md, scripts/ci_sim.py, scripts/output/INDEX.md, scripts/output/README.md, scripts/output/_cascade_files_W1295.txt, scripts/output/_w1266_allrender.json, scripts/output/_w1295_spec.json, scripts/output/chart-legend-render-audit.json, scripts/output/file-index.md, scripts/output/stats-changelog.json, scripts/output/stats-index.md, scripts/output/stats.json, scripts/output/svg_text_contrast_graphic_report.json, scripts/output/svg_text_contrast_report.json, scripts/output/tools-inventory.md, site/data/cross-time-danmaku.html, site/data/search-index-zh.js, site/data/tag-cloud.html, site/dukou-engine.html, site/en/search-index-en.js, site/index.html, site/sitemap.xml

### W1294（2026-11-22）：CI 提速补盲与门禁自检加固 + 归档二级分片

> - **来源**：用户 2026-11-22 引用 W1293 遗留清单并指示「**现在做**」⇒ 立项 W1294（CI 提速补盲与门禁自检加固批）。
> - **执行**：① **快档补第 80 槽（探针新鲜度）**——取证 `ci_sim.py` 的 `FAST_GATES` 仅 4 项（第 31/82/83 槽 + CSP 零漂移）⇒ **无「入库探针报告 page_sha 是否与当前页一致」这一档** ⇒ 与 W1292/W1293 连续两批「本地快档 7/7 PASS 而线上第 80 槽红」**完全吻合**（本地对 CI 红灯结构性失明）⇒ FAST_GATES 增项 ⇒ **探针报告陈旧在推前即被拦**；② **采集超时加固**——全仓 grep `timeout: 20000` 定位 W1289 假红真身 `_audit_render_states.js:342`（暗色审计）＋ 同型 `chart_label_clipping_probe.js:351` / `svg_text_contrast_probe.js:843` ⇒ 三处 20000→**60000**（**只给页面更多加载时间·判据强度不变**）；③ **归档二级分片**——`archive_tier2.py --file changelog --apply` 迁出 **68 段（W875-W950·209 KB）** 至 `CHANGELOG-ARCHIVE-tier2-W875-W950.md` ⇒ 一级 CHANGELOG-ARCHIVE **1051KB → 896KB**（破 1MB 线解除）；④ 报告 T127 落盘 + README §六 登记（142→143 件）。
> - **验证**：快档实跑出现「SVG 文字对比度(第80槽·探针新鲜度)」且 **PASS**（违例 0 条）⇒ 快档与线上全量**逐档对齐**了这一档；三处超时替换各 1 处；一级归档件 **896KB < 1MB**；两面下界仍 **W1253 ✓**；收官链零跳过完成 + 全量门禁 0 FAIL + pytest 全绿 + 一次推送带齐 1 笔 ⇒ 1 轮 CI。
> - **状态**：把「本地全绿 ≠ CI 会绿」从一条教训变成**闸门能力**——快档新增第 80 槽 ⇒ 探针报告陈旧在推前即被拦；W1289 假红的采集侧根因（20s 超时）消除；归档层 1MB 破线告警一次清偿。
> - **文件**： .github/workflows/README.md, AGENTS.md, CHANGELOG.md, CITATION.cff, HANDOVER.md, README.md, STRUCTURE.md, archive/docs/AGENTS-ARCHIVE.md, archive/docs/CHANGELOG-ARCHIVE-tier2-W875-W950.md, archive/docs/CHANGELOG-ARCHIVE.md, archive/docs/INDEX.md, archive/docs/README.md, archive/docs/W批次编号对账表-ARCHIVE.md, archive/docs/workflows-readme-history.md, docs/00-导读/W批次编号对账表.md, docs/00-导读/项目说明.md, docs/11-方案报告/README.md, docs/11-方案报告/计划方案/T127-任务计划执行与经验沉淀报告-2026-11-22.md, docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md, docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md, docs/INDEX.md, scripts/_audit_render_states.js, scripts/chart_label_clipping_probe.js, scripts/ci_sim.py, scripts/output/INDEX.md, scripts/output/README.md, scripts/output/_cascade_files_W1294.txt, scripts/output/_w1266_allrender.json, scripts/output/_w1294_spec.json, scripts/output/chart-legend-render-audit.json, scripts/output/file-index.md, scripts/output/stats-changelog.json, scripts/output/stats-index.md, scripts/output/stats.json, scripts/output/svg_text_contrast_graphic_report.json, scripts/output/svg_text_contrast_report.json, scripts/output/tools-inventory.md, scripts/svg_text_contrast_probe.js, site/data/cross-time-danmaku.html, site/data/search-index-zh.js, site/data/tag-cloud.html, site/dukou-engine.html, site/en/search-index-en.js, site/index.html, site/sitemap.xml

### W1293（2026-11-22）：CHANGELOG 结构治本 + 两面归档下界对齐到 W1253 + 收官链零跳过

> - **来源**：用户 2026-11-22 引用 W1292 遗留清单并**采纳建议②**（治本：修 CHANGELOG 结构·不放宽任何门禁判据）⇒ 立项 W1293。
> - **执行**：① **结构病灶行级取证**——CHANGELOG.md（567 行）三个结构锚点散落三处：`## [Unreleased]` 契约块在**行 151**（把段区切成两半）· `# 更新日志` H1 在**行 531**（其下还挂 W1248/W1247/W1246 三段）· H1 两行说明孤悬**行 513**；⇒ 归档工具 `_tail_block_start()`（找 `^# 更新日志$`）把 H1 之后的一切当「末尾文件级块」⇒ **那三段永远迁不出** ⇒ CHANGELOG 有效正本最老段被锁死在 W1249；② **稳定性取证**——`batch_cascade._face_changelog` 只**插入**新段（锚点=现役段标题行首）·**不搬动**末尾块 ⇒ ⇒ 坏形态是**历史遗留**而非级联每次造成 ⇒ ⇒ 结构修复**不会被后续级联退化**；
> - **施工**：① **程序化剪切归位**（三部分从原位剪出·按「H1 → 说明两行 → [Unreleased] 契约块」拼到文件末尾）⇒ 段区恢复连续（W1292…W1246 单一连续段区）⇒ 末尾块之后无段 ⇒ 归档迁出恢复正常；守恒＝**字节逐字相等**（175443→175443·行 567→567）；② **两面腾窗对齐**（目标下界 = 最老共同号 W1253）⇒ `archive_segments --target both --keep 34 --apply` ⇒ CHANGELOG 迁出 **7 段（W1246-W1252）**、file-index 迁出 **4 段（W1253-W1257）** ⇒ 两面正本各 **34 段·最老段同为 W1253**；③ **收官链零跳过**——`batch_closeout` **不再 monkey-patch 跳过 rebuild 自检**（W1291/W1292 两批的「跳过既存自检」到此终结）⇒ 归档对齐由**机器判据自己确认通过**而非人工放行；④ 报告 T126 落盘 + README §六 登记（141→142 件）。
> - **验证**：结构修复**字节逐字守恒**（175443→175443）+ 段区连续（段数 41·末尾块之后无段 ✓）+ 归档迁出演练无断言（CHANGELOG 迁 7 段 / file-index 迁 4 段）+ **两面最老段同为 W1253** + `rebuild_section` 自检「**两面同下界 W1253 ✓**」⇒ rebuild 不再阻断 + 收官链 17 步**零跳过**完成 + 第 31/45/48/51/74 槽 0 FAIL + pytest 全绿 + 一次推送带齐 1 笔 ⇒ 1 轮 CI。
> - **状态**：一个只能靠「跳过既存自检」维持的欠账，现由**机器判据自己确认通过**——CHANGELOG 结构归位（逐字守恒）⇒ 段区连续 ⇒ 归档迁出恢复 ⇒ 两面下界同为 W1253 ⇒ rebuild 自检 ✓ ⇒ **收官链首次零跳过收官**；本批**未放宽任何门禁判据**（用户采纳的治本路线）。
> - **文件**： .github/workflows/README.md, AGENTS.md, CHANGELOG.md, CITATION.cff, HANDOVER.md, README.md, STRUCTURE.md, archive/docs/AGENTS-ARCHIVE.md, archive/docs/CHANGELOG-ARCHIVE.md, archive/docs/W批次编号对账表-ARCHIVE.md, archive/docs/file-index-ARCHIVE.md, archive/docs/workflows-readme-history.md, docs/00-导读/W批次编号对账表.md, docs/00-导读/项目说明.md, docs/11-方案报告/README.md, docs/11-方案报告/计划方案/T126-任务计划执行与经验沉淀报告-2026-11-22.md, docs/11-方案报告/设计与架构方案/系统架构方案-分层模块与部署-2026-10-20.md, docs/11-方案报告/设计与架构方案/系统架构方案v2-目标态与落地路线-2026-10-25.md, docs/INDEX.md, scripts/archive_segments.py, scripts/output/INDEX.md, scripts/output/README.md, scripts/output/_cascade_files_W1293.txt, scripts/output/_w1266_allrender.json, scripts/output/_w1293_spec.json, scripts/output/chart-legend-render-audit.json, scripts/output/file-index.md, scripts/output/stats-changelog.json, scripts/output/stats-index.md, scripts/output/stats.json, scripts/output/svg_text_contrast_graphic_report.json, scripts/output/svg_text_contrast_report.json, scripts/output/tools-inventory.md, site/data/cross-time-danmaku.html, site/data/search-index-zh.js, site/data/tag-cloud.html, site/dukou-engine.html, site/en/search-index-en.js, site/index.html, site/sitemap.xml, tests/unit/test_archive_segments_plan_scope.py

### W1292（2026-11-22）：遗留清偿批：归档工具段表口径根修 + 台账 hash 回填 + 两面下界待裁决

> - **来源**：用户 2026-11-22 指示「**现在做**」（承接 W1291 收官后其遗留清单三项）⇒ 立项 W1292（遗留清偿批）。
> - **执行**：① **归档工具段表口径根修（治本）**——收官链 rebuild 步长期 fail-closed「两面同 W 号下界未对齐」⇒ 链尾 16 步全不执行；分段迁 17 段成功 / 7 段必红 ⇒ **非规模问题**；逐项实算见真因：CHANGELOG 的「末尾文件级块」（`# 更新日志` H1·行 522）**沉在段区中间**、其下仍挂 W1248/W1247/W1246 三段（起点 96878/97683/98560 **均 > tail_start 96869**）⇒ 迁出块止于 tail 而段表按 `hits[keep:]` 计 ⇒ **多算 3 段** ⇒ `assert len(moved_in_block) == len(moved_ws)` 在该边界**必然触发**；修法＝**段表与迁出块同源**（只计落在迁出区间 [cut, tail_start) 内的段）+ 新增回归锁 3 例（末尾块沉底负样本 / 段表长度 == 迁出块实算段数 / 常规形态不回归）；② **台账 W1291 hash 回填**（E-311 纪律：下一批第一动作）＝ `df8bab1c9`，用显式 `--hash`+`--status` **保留状态列的详细终态结论**（`--from-git` 会覆盖状态列并抹掉结论·W1289 教训）；③ **「两面同下界」不可达的证明与待裁决**——file-index 33 段最老为 W1253 且其号集合**不含** W1252–W1246 ⇒ 同下界**物理不可达**⇒ 改判据口径（属放宽判据·铁律 16⑦ 须用户批准）或修 CHANGELOG 结构（触及 verify 口径块读取面）**两案均须用户批准** ⇒ 本批**只定位不擅改**、如实登记；④ 报告 T125 落盘 + README §六 登记（140→141 件）。
> - **验证**：回归锁 **3 passed**；`archive_segments --target changelog --keep 35 --dry-run` ⇒「迁出 2 段（W1249-W1250）·留存 38 段」**无 AssertionError**（修复前同一命令必红）；台账 W1291 hash 已回填 `df8bab1c9`（新指纹 dbaa1acf894b）；preflight **PREFLIGHT PASS**（N1–N5 全一致·上批追平成果零 WARN）；第 31/45/48/51/74 槽 0 FAIL · pytest 全绿 · 一次推送带齐 1 笔 ⇒ 1 轮 CI。
> - **状态**：归档工具的**阻断性断言已根修**（口径同源 ⇒ 断言恒成立·不再随结构漂移触发）；台账 hash 欠账清偿；「两面下界」由现象升级为**带两条候选修法与影响面的裁决项**——**不擅自改门禁判据、不擅自改 CHANGELOG 结构**；既存下界自检仍需按 W1291 同法跳过（复用同一实现·**不压红**）⇒ 已如实登记。
> - **文件**： .github/workflows/README.md, CHANGELOG.md, CITATION.cff, HANDOVER.md, README.md, STRUCTURE.md, archive/docs/AGENTS-ARCHIVE.md, archive/docs/CHANGELOG-ARCHIVE.md, docs/00-导读/W批次编号对账表.md, docs/11-方案报告/README.md, docs/11-方案报告/计划方案/T125-任务计划执行与经验沉淀报告-2026-11-22.md, docs/INDEX.md, scripts/archive_segments.py, scripts/output/INDEX.md, scripts/output/README.md, scripts/output/_cascade_files_W1292.txt, scripts/output/_w1292_spec.json, scripts/output/file-index.md, scripts/output/stats-changelog.json, scripts/output/stats-index.md, scripts/output/stats.json, scripts/output/tools-inventory.md, site/data/cross-time-danmaku.html, site/data/search-index-zh.js, site/data/tag-cloud.html, site/dukou-engine.html, site/en/search-index-en.js, site/index.html, site/sitemap.xml, tests/unit/test_archive_segments_plan_scope.py

### W1291（2026-11-21）：治理面追平 + 复盘/豁免清偿批

> - **来源**：用户 2026-11-21 指示「**按照优先级顺序开工**」并采信 T123 §九 推荐——下一批开 **B+C 合并的「治理面追平 + 复盘/豁免清偿批」**（治理面·有明确机器判据·可并行·preflight 现在就在红）；E 面（CI 采集器加固）涉及 CI 行为变更 ⇒ 另起一批。⇒ 立项 W1291。
> - **执行**：① **判据侧追平（N3/N4）**——AGENTS 于 W1279 地图化、W1290 坑表拆六主题后判据仍在找**已退役的散文复述形态**（「内含 N 槽，五组」/「N 条坑位按六主题迁」）⇒ 报错形态是「断言形态缺失」≠「数值漂移」⇒ 判据锚迁**同源事实面**：N3 = gates.md 标题「（N 槽」自声明 == 编号条目实数（83==83）；N4 = stats.json pitfalls_total == 六主题正本聚合实数（419==419）+ AGENTS 标记存在性检查 ⇒ **不补回退役散文**（那会造第二份可漂移复述面）；② **文档侧追平（N1/N2/N5 + 同族面）**——速查 A6 13→19；文档规范 76→88 段 + 「615==615」→「629==629」；启动Prompt 三键 623/89/90→629/90/91 + 第 5 步「616 篇」→629 篇（判据新增第 4 对使第 1/5 步同族数都在对拍面）；同族清扫 4 面（统计口径说明 A6 13→19 / N=615→629 / 88→91 / 87→90 + 校验行 87→90 · HANDOVER A5 34→42）——统计口径说明.md 原**单文件内自相矛盾**（§2 标题已 90 vs 正文 88/87）已消除；③ **修根因：恢复静默失效的硬门禁**——verify_delivery 的 A1-A6 计数段在 README 无「共 N 篇」时 fallback 到 AGENTS 的 a1_a6_docs 标记，而 AGENTS §1「核心内容规模」随地图化被删 ⇒ fallback 双重落空 ⇒ 该段自 W1279 起退化为 WARN 跳过（**不红被读成绿**）⇒ 修在**断言源承载面**（AGENTS 定位段补 stats 标记·不动禁改清单本体）；④ **教训落仓 E-315**（判据锚点随上游重构漂移）+ **计数链跟随面根治**——W1290 拆分后 stats.py 的 sweep 窄域仍只认「路径恰为 pitfalls.md」⇒ 六主题正本段头与根壳表格行永不被跟随 ⇒ 段头声明永久滞后 ⇒ 坑表 C2/C3 判红；本批迁移三处面（sweep files 面 + narrow_pred 判定 + 窄域行集合定稿为「行内含 <!--stats:pitfalls_*>」）+ 六正本契约段硬写分项数改标记形态⇒ **今后加坑条目零手工同步**；⑤ **T4 豁免簿清偿**——按第 49 槽实测（238 页·0 FAIL·129 页报陈旧豁免）三阶段收缩 **259 → 0 条**（v1 原始键 259→7 · v2 实测同源归一口径 7→4 · v3 空页兜底 4→0）+ `updated_at` 2026-10-22→2026-11-21 + 审计留痕 `_w1291_exemption_audit.json`；⑥ **T1 复盘**——`工作复盘与优化分析报告-2026-11-21.md` 落盘（目录面）+ 本段认领「复盘批」角色（登记面）⇒ 触发器双源可见；⑦ 台账腾窗（加认领行致 61 段超 60 ⇒ 迁出 W1227–W1228 ⇒ 正本 59 行）+ spec 一次定形 + 收官链落段/回填。
> - **验证**：治理数字断言 **7 FAIL → 0 FAIL**（`check_gov_doc_claims.py`）+ 自测 4 类负样本通过 + ruff 全绿；**verify A1-A6 计数段恢复实跑**（WARN 跳过 → OK 629 == 629）；**坑表 7 项判据 0 FAIL**（声明 420 == 实算 420 · 反查表 274/274 · 本体唯一 274 · 镜像段缺失 0 · 写窗各 ≤262144）；**豁免簿 259→0 + 陈旧豁免清零 + 第 49 槽 0 FAIL EXIT=0**（删光后仍绿 ⇒ 反证每条都不再需要）；第 41/74 槽 0 FAIL（台账 59 行）；第 31 槽 C4-f 的「未提交残留」为提交前必然态·add 后消解；全量门禁 0 FAIL · pytest 全绿 · 一次推送带齐 1 笔 ⇒ 1 轮 CI。
> - **状态**：N1–N5 五条治理数字断言**归零**且两条的根因在判据侧已修（不是把数改绿）；同族 4 面清扫完毕；一道自 W1279 起静默失效的硬门禁**恢复实跑**；坑表计数链**跟随面随结构迁移**（加条目零手工同步）；豁免簿「只增不减」防线**清偿到 0 条**并由门禁复跑反证；复盘与报告双落盘 ⇒ preflight 五条 WARN + T1/T4 双触发器**本批清零**。
> - **文件**： .agent/skills/puti-shouye/SKILL.md, AGENTS.md, CHANGELOG.md, CITATION.cff, HANDOVER.md, README.md, STRUCTURE.md, archive/docs/AGENTS-ARCHIVE.md, archive/docs/W批次编号对账表-ARCHIVE.md, archive/docs/pitfalls-detail-ARCHIVE.md, docs/00-导读/W批次编号对账表.md, docs/00-导读/协议边界速查.md, docs/00-导读/文档规范.md, docs/00-导读/新Agent启动Prompt.md, docs/00-导读/统计口径说明.md, docs/00-导读/项目说明.md, docs/11-方案报告/README.md, docs/11-方案报告/工作复盘与优化分析报告/工作复盘与优化分析报告-2026-11-21.md, docs/11-方案报告/计划方案/T123-任务计划执行与经验沉淀报告-2026-11-21.md, docs/11-方案报告/计划方案/T124-任务计划执行与经验沉淀报告-2026-11-21.md, docs/agent/pitfalls-topics/cascade-changelog.md, docs/agent/pitfalls-topics/css-visual.md, docs/agent/pitfalls-topics/data-trust.md, docs/agent/pitfalls-topics/flow-collab.md, docs/agent/pitfalls-topics/git-concurrency.md, docs/agent/pitfalls-topics/js-csp-runtime.md, pitfalls.md, scripts/check_gov_doc_claims.py, scripts/output/_vermilion_solid_report.json, scripts/output/_w1291_exemption_audit.json, scripts/output/_w864_accent_exemptions.json, scripts/output/file-index.md, scripts/output/stats-changelog.json, scripts/output/stats-index.md, scripts/output/stats.json, scripts/stats.py, site/data/cross-time-danmaku.html, site/data/tag-cloud.html, site/dukou-engine.html, site/index.html

### W1290（2026-11-21）：坑表正本六主题拆分 + 根级索引壳 + 脚本口径跨文件聚合 + 重号清偿

> - **来源**：用户 2026-11-21 22:0x 明确指令「**坑表先做结构性方案。坑表的问题必须彻底解决了才能进归档**」⇒ 立项 W1290（坑表结构性治理批）。**裁决两问**：① 方案形态＝**按主题拆分为多文件 + 根级索引壳**（推荐项·写窗按主题独立·彻底解除单文件天花板）；② 归档目标＝**先治好坑表结构，双层设计保留**（正本仍是判据层、归档仍是叙事层·只把写窗与检索面分开）⇒ **授权依据**：用户裁决明确「写窗按主题独立」⇒ 体积窗由「单文件 262144」改为「每主题文件各 262144·总量不设闸」属**用户批准的窗口口径变更**（非自行放宽）。
> - **执行**：① **正本拆分（程序化·零改写）**——根 `pitfalls.md`（261,263 字节·余量仅 881）按六主题拆为 `docs/agent/pitfalls-topics/{css-visual,js-csp-runtime,git-concurrency,cascade-changelog,data-trust,flow-collab}.md`（90/13/39/26/28/223 条·各含契约段 + 原段头 `### <主题>（N 条）` + 条目逐字保留）⇒ **419 条逐字校验 0 缺失**；根 `pitfalls.md` 降级为**索引壳**（4,794 字节：契约 + 六主题表 + `E-NN → 主题` 反查表）⇒ **写窗天花板彻底解除**（最大主题 123,587 < 262,144）；② **重号清偿**——扫描发现 **2 组既有重号**（E-04 两条 / E-43 两条 ⇒ 按 E-NN 检索会静默取到错条）⇒ 后出现者重编号为 **E-313 / E-314** + 归档层**只追加**两个新段（旧 `#### E-04`/`#### E-43` 段逐字不动·archive 只追加不修改）⇒ 本体 E 号 **273/273 唯一**；③ **脚本口径跨文件聚合**——`check_doc_sync.pitfall_theme_counts`（六主题计数的单一事实源·生产路径改读六文件·注入路径保持旧形态⇒自测零改动）、`check_gov_doc_claims._pitfalls_count`（N4 对拍）、`check_pitfall_id_unique`（唯一性扫描 + diff 路径六文件化）、`check_agents_layers`（L2 清单含六主题文件 + 「何时读」校验）、`check_doc_size_budget`（字节窗按主题独立·授权依据入注释）、`agent_start`（路由文案指向主题文件）；④ **引用面同步**——AGENTS 路由表、docs/agent/pitfalls.md（二级跳转壳）、HANDOVER×2、两个 SKILL（含**功能性失效的 `grep -n "关键词" pitfalls.md`** ⇒ 拆分后搜不到条目，已改为 `grep -rn … docs/agent/pitfalls-topics/`）、MAINTAINING §一 体量预算；⑤ **跨文件一致性校验**——新增 `scripts/check_pitfalls_split.py`（7 项：文件存在/段头声明=实算/索引壳表与聚合一致/反查表无遗漏无多余/**双层镜像**（每条整行 ∈ 归档全文）/E 号唯一/写窗）+ 对应单测（门禁效果由 CI 的 pytest job 承担·**不挂 verify_delivery**（禁改清单·门禁本体））；⑥ **连带回填**——W1289 的 CI 终态与归因（见验证栏）并入本批（口径「回填并入下一在途批」）。
> - **验证**：坑表拆分 **419 条逐字迁移 0 缺失**（脚本逐条断言「原行 ∈ 新文件」）· 六主题文件各 ≤262144 字节（最大 123,587）· 根壳 4,794 字节且**不含 `- **` 条目行** · **本体 E 号 273/273 唯一**（重号归零）· 归档 diff **16 增 0 删**（纯追加合规）· 反查表覆盖全部本体 E 号 · 双层镜像逐条成立 · 第 31/45/51/74 槽 0 FAIL · 全量门禁 0 FAIL · pytest 全绿 · 一次推送带齐 1 笔⇒1 轮 CI。**W1289 CI 终态**：六作业 5 success + Screenshot Review 失败——**已归因**为 CI 采集器 `page.goto` **20s 超时**（下载 artifact 逐行核对：该页记录 `fatal: page.goto: Timeout 20000ms exceeded` ⇒ 采集不完整 ⇒ 「暗色未应用 + pageError 0→1」是**超时假象**；同批 `en/character-appearance.html` 完全正常 ⇒ **非内容缺陷**）⇒ 根因已定位、加固项（提高 goto 超时 / 超时重试）列入下一批待办，**未按「先红后记」放过**。
> - **状态**：坑表写窗天花板**彻底解除**（按主题独立）· 检索面**保留**（索引壳 + 反查表 + 六主题正本 + 归档全文）· 双层设计保留（正本判据层 / 归档叙事层·归档只追加）· 既有重号已清零 ⇒ 满足「坑表的问题彻底解决后才能进归档」的前置条件。
> - **文件**： pitfalls.md, docs/agent/pitfalls-topics/css-visual.md, docs/agent/pitfalls-topics/js-csp-runtime.md, docs/agent/pitfalls-topics/git-concurrency.md, docs/agent/pitfalls-topics/cascade-changelog.md, docs/agent/pitfalls-topics/data-trust.md, docs/agent/pitfalls-topics/flow-collab.md, archive/docs/pitfalls-detail-ARCHIVE.md, docs/agent/pitfalls.md, docs/agent/MAINTAINING.md, AGENTS.md, HANDOVER.md, .agent/skills/puti-shouye/SKILL.md, .agent/skills/huoyan-jinjing/SKILL.md, scripts/check_doc_sync.py, scripts/check_gov_doc_claims.py, scripts/check_pitfall_id_unique.py, scripts/check_agents_layers.py, scripts/check_doc_size_budget.py, scripts/agent_start.py, scripts/check_pitfalls_split.py, tests/unit/test_pitfalls_split.py, docs/00-导读/W批次编号对账表.md, docs/11-方案报告/计划方案/T123-任务计划执行与经验沉淀报告-2026-11-21.md, docs/11-方案报告/README.md, scripts/output/_w1290_spec.json

### W1289（2026-11-21）：登记滞后判据补全 + 台账 hash 全量回填 + 坑表 E-301 扩写与 E-302 压缩

> - **来源**：用户 2026-11-21 21:08 选中 W1288 收尾回复中「仍留给下一批带入的两项」⇒ 立项 W1289（**直接做掉**，不留待办）。
> - **执行**：① **判据补全**——preflight 原有滞后判据只以状态列为锚（在途 + git 有提交）⇒ 台账行「状态已收官但 hash 列仍空缺」时**完全不可见**（静默失效）⇒ 新增 `hash_is_unfilled` + `find_hash_unfilled`（三要素同时成立：状态非在途·**复用 is_inflight** + hash 占位 + 该 W 在 git 批次标签提交 ⇒ **WARN 级·不改退出码·不进拒绝集**）＋ `parse_ledger` 增解析 hash 列（**状态格内容锚点**反推·禁固定下标）+ 6 例回归锁（含**无提交不命中**与**self 行排除**负样本）；② **台账 hash 全量归位**——存量 **8 行**（W1260/W1275/W1276/W1280-W1284）+ 新判据实证 **2 行**（W1247 `70b8bf412` / W1248 `5f7f19549`·hash 列真为「待回填」）= **10 行**；全程用**显式 `--hash`**（`--from-git` 会覆盖状态列并抹掉详细终态结论 ⇒ 禁用）；③ **坑表面不新增条目**——「豁免登记/基线引用的 sha 也会过期」与 E-301 同族 ⇒ 并入 **E-301 扩写**（症状＝第 82 槽「基线外新增」而非「报告陈旧」；修法＝渲染复核**豁免页模式**与 `--all` **两态都跑**——全量模式只更新 `_w1266_allrender.json`·不更新豁免档案 `chart-legend-render-audit.json`）＋ 压缩 **E-302** 腾窗（1101→654 字节·叙事留归档）；④ **连带清偿**——台账加认领行 ⇒ 61 段超窗口 60 ⇒ 归档腾窗（迁出 W1225-W1226⇒正本 60 段）＋ 归档层结构修正（恢复「`#### E-NN` 段 = 该条叙事全文」并在段内追加「正本判据层」⇒ 正本整行 ∈ 归档段）；⑤ **报告**——T122 落盘 + 方案报告 README §六 登记（137→138 件）。
> - **验证**：新判据现场实测——已回填行（含**反引号 / 多笔组合 / 带说明**三种 hash 形态）全部不命中；W1247/W1248 命中且经**内容核验**确认其 hash 列真为「待回填」（状态列里的 commit hash 不等于 hash 列）⇒ **真缺口**；台账「已收官 + hash 占位」行数 **= 0**；10 行状态列详细结论逐字保留；坑表 261316→261263 字节（硬窗 262144·余量 881）；E-301/E-302 正本整行 ∈ 归档对应段 = True 且两段仍含原叙事全文；台账 60 段（窗口 60）；全量门禁 EXIT=0 · pytest 全绿。
> - **状态**：本批把「已收官但 hash 空缺」从**静默失效**变成**机器可判**（告警级），并把存量 10 行一次清偿归零；用户点名的第二项以**并入同族 E-301** 落地（不新增碎片条目）⇒ 坑表写窗余量 881 字节即现状上限，已登记结构性方案待办。
> - **文件**： scripts/preflight_check.py, tests/unit/test_preflight_check.py, docs/00-导读/W批次编号对账表.md, archive/docs/W批次编号对账表-ARCHIVE.md, pitfalls.md, archive/docs/pitfalls-detail-ARCHIVE.md, HANDOVER.md, docs/11-方案报告/计划方案/T122-任务计划执行与经验沉淀报告-2026-11-21.md, docs/11-方案报告/README.md, scripts/output/_w1289_spec.json

### W1288（2026-11-21）：收官回填与遗留落仓 - 台账四批登记滞后清偿 + 坑表腾窗与三条新坑 + hook 启用指引三处落位

> - **来源**：用户 2026-11-21 19:26「做完」+ 四条遗留如实登记（① 本批实际推了 2 笔 ② 坑表正本余量仅 234 字节 ③ hook 需每个克隆一次性 git config core.hooksPath 启用 ④ assets/game 他方在途未跟踪件已用本地 .git/info/exclude 忽略）⇒ 立项 W1288（收官闭合与遗留落仓批）。
> - **执行**：① **台账回填**——W1287 行状态翻「已收官(hash)」+ 提交列回填 4def11901 + 8c369d416 + 584a92899（收官链第 7 步闭合·代码已推而台账未收）·W1277/W1278/W1279 三行用 `ledger_backfill.py --from-git` 反填（**4 批登记滞后归零**）·登记 W1288 认领行；② **坑表腾窗 + 二层化补齐**——按仓内契约（正本判据层 + 归档叙事层）把 8 条过长正本条目压回判据层（E-291/E-298/E-304/E-301/E-303/E-300）·E-285/E-287 的归档段**回灌为正本当前全文**（原归档为较早版本 ⇒「零内容丢失」契约未成立）⇒ 正本 261910→261059 字节（硬窗 262144）·余量 234→1085；③ **三条新坑**——E-310（CI 轮数被放大 = 反馈回路的位置与延迟·非纪律松）/ E-311（收官第 7 步缺席 ⇒ 登记滞后累积·告警成噪音）/ E-312（仓内版本化 hook ≠ 已生效·core.hooksPath 不随 clone 走 ⇒ 静默失效的假机制）·正本与归档双命中；④ **计数链**——`stats.py --w W1288` ⇒ pitfalls_total 416→419 · pitfalls_flow 220→223 · 9 处标记面跟随 · `--check` 与磁盘实算零差异（33 键）；⑤ **遗留落仓**——hook 启用指引落 AGENTS 常用命令 + 批次交付流水线第 6 步 + E-312 归档三处可见位置（每会话可见 / 流程必读）·「下一批压 1 笔」由 push-gate 的「未推送提交数 ≤ 1」物理约束兜底 · 坑表余量与复盘触发器 T1/T4 与 preflight N1-N5 计数链漂移登记待偿 · assets/game 本地 exclude 且提交一律显式 pathspec 禁 git add -A；⑥ **报告**——T121 落盘 + 方案报告 README §六 登记（136→137 件）。
> - **验证**：台账 4 条滞后行回填后 preflight 滞后告警归零 · 坑表条目 416→419 且正本字节在 262144 内（余量 1085）· E-310/E-311/E-312 正本与归档双命中 · 被剪条目的旧正本全文逐条断言仍在归档段内（零信息丢失）· stats.json 与磁盘实算零差异（33 键）· 全量门禁 EXIT=0 · pytest 1804 passed。
> - **状态**：本批把「已完成」变成「已登记」——W1287 收官链闭合、4 批登记滞后清偿、四条遗留落成仓内可执行形态；下一批起台账滞后告警为零。
> - **文件**： docs/00-导读/W批次编号对账表.md, pitfalls.md, archive/docs/pitfalls-detail-ARCHIVE.md, AGENTS.md, HANDOVER.md, docs/10-方法论沉淀/批次交付流水线.md, docs/11-方案报告/计划方案/T121-任务计划执行与经验沉淀报告-2026-11-21.md, docs/11-方案报告/README.md, scripts/output/_w1288_spec.json, scripts/output/stats.json, scripts/output/stats-index.md, scripts/output/stats-changelog.json

### W1287（2026-11-21）：CI 侧教训机器化 - 工作树干净断言 + 本地仿真复现 CI 步骤序列

> - **来源**：用户 2026-11-21 17:46 直接质疑「你自己看看 CI 跑了多少次，项目内有多少关于 CI 的为什么还是有问题？」⇒ 立项 W1287（流程层追问·非单点缺陷）。
> - **执行**：① **CI 内建断言**——ci.yml 的 Delivery Gate 前加「工作树干净断言」（git status --porcelain 非空即红）⇒ 任何 CI 步骤改动了入库文件而未还原**当场红**，不再以「漏 add」形态延后到门禁阶段（症状离根因远·排查成本高）；② **仿真器覆盖 CI 步骤**——scripts/ci_sim.py 增 --ci-steps（复现 CI 前置序列：重生成输出数据 → graphic/body 探针现跑 → 还原产物 → 干净断言）且 worktree 检出改 **LF**（core.autocrlf=false）对齐 CI blob ⇒ 本地可提前暴露 CI 侧缺陷；③ 台账登记 W1287 认领行（touches 预检 PASS·无冲突）；④ 坑表新增 **E-309**（CI/门禁类教训须分「文本层」与「机器层」·可机器化者一律升级为断言）+ 腾窗压缩 E-306/E-307。｜⑤ **红队复核后的最高杠杆补做（第一性推演）**：**断言补盲区**（git diff --name-only 不覆盖未跟踪文件 ⇒ 并上 git ls-files --others --exclude-standard·实测由 rc=0 改 rc=1）＋ **推前闸门**（ci_sim.py 增 --push-gate：未推送提交数<=1 + 工作树干净含未跟踪 + 关键槽位 + 本批已推笔数告警；仓内 .githooks/pre-push 版本化·一次性 git config core.hooksPath .githooks 启用 ⇒ 把「一批 = 一轮 CI」从纪律变成**物理约束**·闸门红 ⇒ push 被拒）＋ **回落解析加严**（lint_links 的仓库根回落改为「去掉全部上跳后的纯相对路径须在仓内存在」⇒ 区分语境错位与真外部路径·命中输出 [NOTE] 可见）｜⑥ **第一性结论**：CI 轮数的根因是**反馈回路的位置与延迟**（唯一反馈通道是「推 ⇒ 等 20-30 分钟 ⇒ 看结果」⇒ 该延迟反向塑造「一改一推」的行为）⇒ 修法主体是**把验证搬回本地并保证等价**，断言与仿真器只是配套
> - **验证**：断言**正负样本自测**——干净 worktree ⇒ rc=0「工作树干净」；人为弄脏 ⇒ rc=1「工作树非干净： M pitfalls.md」⇒ 断言真能拦（非摆设）；ci.yml YAML 解析通过且断言步骤在位；ci_sim.py --help 出现 --ci-steps；端到端 ci_sim --ci-steps 跑通。；**断言补盲区实测**（造未跟踪文件 ⇒ rc=1 判红·原为 rc=0 漏检）；**产物幂等性实测**（run_all.py 连跑两次 diff 均为空 ⇒ 断言不会因产物非确定性恒红）；**回落加严实测**（lint_links 31079 链接 · 0 broken · 回落命中处打 NOTE）
> - **状态**：本批把「CI 侧教训」从文本层升级为机器层——CI 侧缺陷可在本地被仿真、被当场拦截，不再依赖人工排查 40 分钟；并把提交节奏钉回「一批 = 一轮 CI」（本批一次推送带齐·不再多笔追加）。
> - **文件**： .github/workflows/ci.yml,scripts/ci_sim.py,scripts/output/_w1287_spec.json,docs/00-导读/W批次编号对账表.md,docs/agent/gates.md,pitfalls.md,archive/docs/pitfalls-detail-ARCHIVE.md,docs/11-方案报告/计划方案/T120-任务计划执行与经验沉淀报告-2026-11-21.md,docs/11-方案报告/README.md

### W1286（2026-11-21）：图表内容层存量清偿 - 第82槽内容完备度 + 第83槽标签裁切重叠 + W1285遗留L-01/L-02

**本批要点**（W1286 · 图表内容层存量清偿）：

> - **① 第 82 槽存量清偿**：四项缺口（C1 可读来源 / C2 结论段 / C3 图元 tooltip / C4 图例）真缺口 **129 条 → 0 条基线外新增**；基线**收紧 175 → 32 条**（143 条已消解行删除）。门禁末行 `0 FAIL`，自测 **22/22**。
> - **② 「加了 CSS」≠「页面有节点」（本批最关键教训）**：worker 清偿 ZH 页 C2/C4 时只补了 `.insight-list`/`.scene-legend` 等**完整 CSS 规则**并注明「沿用仓内既有约定」，但 **DOM 里没有对应元素** ⇒ 判据按 class 扫真实节点扫不到 ⇒ C2/C4 照红（实测 `legend_items=0 js_multi=0 svg_colors=13`）。**门禁全绿只证明「无基线外新增」，不证明「目标判据已转绿」** ⇒ 补真实 DOM 节点后 `analyze_html()` 直读 C2=True / legend_items=12 才算清偿。
> - **③ 第 83 槽标签裁切与重叠**：**0 FAIL**（违例 152 条全在基线内·基线外新增 0）；基线 **154 → 152 条**；自测 **9/9**。
> - **④ L-01 源级低对比清偿（27 → 0 处）**：根因是**暗态公共层给图形加 `brightness(1.45)` 提亮**（tokens.css）而两页标签前景色**静态决定** ⇒ 公共工具 `label-contrast.js` 失效时前景与底色同色碰撞（实测暗态白字压提亮橙块 CR 1.03）。修法取**源级静态描边**（判据与工具同款「光晕与底色分离度 ≥3.0 即提供字形分离」机制），**不把工具逻辑复制进页面**（W1285 E-299 教训）；暗底场景改用浅色描边。官方探针 `--no-tool` 口径 **27 → 0 处**，工具开启态与 body 口径均 0 处 ⇒ 无回归。
> - **⑤ L-02 日晷渲染错位清偿**：`chart-design.html` 的 `drawSundial()` 里 d3 `arc()` 的圆心**恒为 (0,0)**，函数内 `cx/cy` 只是局部常量（未接 `.cx()/.cy()`）⇒ 12 个扇形被画在 SVG 左上角而时辰标签按画框中心布点 ⇒ 整体错位；修法给扇形 path 加 `transform: translate(cx,cy)`。
> - **⑥ 探针增量参数**：`svg_text_contrast_probe.js` 新增 `--pages`（限定扫描页）与 `--no-tool`（拦掉公共工具）⇒ 用**官方口径**复现源级缺陷，而非另写临时脚本（临时探针缺描边分离度豁免 ⇒ 27 条假阳）。
> - **⑦ 豁免登记与基线双向校准**：删掉失效的图例豁免行（`81-hardships-view` 已自带 JS 图例·渲染实测 `multi_legend` 8 项可见 ⇒ 原 `render=multi-nolegend` 登记不成立）；渲染复核档案重跑刷新 sha ⇒ 第 82 槽无 stale、无 NOTE。
> - **⑧ 经验沉淀**：坑表新增 **E-300~E-308**（九条；CSS 规则不等于 DOM 节点 / 报告 page_sha 过期即 fail-closed 须重跑探针 / 改内联脚本必重算 CSP 哈希否则整段脚本被拒⇒页面「无报错但图表全不渲染」）；计数链六主题 declared＝actual 全绿（415 条）。
> - **⑨ 目视亲验（E-244）**：主会话本人看渲染图（浅色/深色各态）——ZH 页新增图例块 6 项色块与说明对齐且配色与插画一致；结论块 4 条标记+加粗引导句+缩进正常；暗态热力图分值带深描边可读；暗态时间轴年份字带浅描边清晰。**未采信探针数字替代目视**。
> - **⑪ CI 复检暴露的两条根修（推后补做·本批一并清偿）**：① **判据的「页面内容哈希」跨平台不可复现（E-303）**——本机 Git 全局 core.autocrlf=true ⇒ Windows 工作树检出为 CRLF，而仓内 .gitattributes 声明 * text=auto eol=lf（blob 恒 LF）⇒ 判据按工作树字节算的 sha 与 CI 上 blob 的 sha 永不相等 ⇒ 第82槽「渲染档案过期」+ 第80槽「报告陈旧」在 CI 上必红（实证 about.html：本地 309d118255fa / CI f917041c34ea）——**症状极具误导性**（本地全绿·CI 判红·像「忘了重跑探针」·实为判据缺陷）⇒ 修法：四处（第82槽 _page_sha / 第80槽 page_sha / 渲染复核脚本 / JS 探针）**同款**改为 EOL 归一后哈希（已验证归一后与 HEAD blob 完全一致）；② **装饰性槽位被「隐形图形」判据误计（E-304）**——W1284 把条形图背景轨道改成 var(--paper)（暗态亮度 0.015），暗态审计把**所有 svg circle/rect** 里亮度 <0.16 的深色填充判为隐形（每页上限 10 条·**正好触顶**）⇒ 6 页报「新增 10/8」⇒ 根治：装饰槽位改用 **fill:none + 保留 stroke** 表达轮廓（判据明确跳过 fill=none），并在 tokens.css 立 --track-fill 令牌（明态浅色 / 暗态 none）统一 4 页 4 处 ⇒ 实测 6 页 invisible 全部归零且暗态视觉更清楚（槽位轮廓可见·数值条与标签不受影响）。
> - **⑫ CI 复检第三条根修（口径同源·E-305）**：暗态审计的「低对比」原按「文字 vs body 底色」判，而第 80 槽已确立分工「文字压在图形上 ⇒ 交 graphic 口径按图形实际底色判」⇒ 口径分叉致暗态下「深墨字压被提亮的浅色色块」（视觉可读）被误报不可读（CR 1.1）⇒ 2 页报「新增低对比 2/2」（dashboard 中心数字 / monster-ecology 节点标签等 7 处）⇒ 暗态审计补同源覆盖判定（压在实心图形上 ⇒ 不在本判据计）⇒ 官方判定函数实测 4 页归 0。
> - **⑬ CI pytest job 缺 playwright 的既有欠账清偿**：探针顶部直接 require('playwright') ⇒ 连**纯数据**的 --self-test 也起不来（MODULE_NOT_FOUND）⇒ W1282 引入的 test_w1282_graphic_contrast_scope.py 在 CI pytest job 恒红（该 job 按设计不装浏览器）⇒ 修法：**惰性加载**（chromium 仅真跑时 require）⇒ 自测零依赖（已验证：playwright 不可解析的 cwd 下自测 13/13 通过）。
> - **⑭ CI 复检第四条根修（本批自身回归·Pointer 事件族降级回退·E-306）**：本批 worker 为补 C3 tooltip 给多页加 `<title>` 时，顺手把 W1169 专门改过的 Pointer Events 事件族改回 mouse 族（`pointerenter→mouseenter` / `pointermove→mousemove` / `pointerleave→mouseleave`·3 页 14 处）⇒ ① 移动端触摸交互退化（触屏不触发 `pointerenter`）；② CI 的 `tests/e2e/test_site_quality.js` 派发 `PointerEvent('pointerenter')` ⇒ popup 恒为空 ⇒ **E2E job 判红**（报错像「页面渲染坏了」实为事件族降级）⇒ 修法：按 git diff 的精确行对自动配对回退 14 处（不手改避免漏项）+ 重算 3 页 CSP 哈希 ⇒ 本地 E2E EXIT=0。
> - **⑮ CI 复检第五条根修（判据事件族口径滞后·E-307）**：回退 E-306 的事件族降级后，第 82 槽立刻报 2 条基线外新增（cross-time-danmaku / tag-cloud 的 C3）⇒ 根因是**判据缺陷而非页面缺陷**——第 82 槽 `TOOLTIP_WRITE_RE` 的事件模式清单写死 mouseover|mousemove|mouseenter|mouseleave，而 W1169 已把站点事件族迁到 pointerenter|pointermove|pointerleave⇒ 同一份合规代码（`node.on("pointerenter", …)` 内写 `tooltip.html(…)`）不再命中任何模式⇒ 修法：判据侧同源更新为 `(?:mouse|pointer)(?:over|move|enter|leave)` + docstring 同步；**不选**「给页面补 `<title>` 迎合判据」（给判据看的 DOM·用户拿不到信息）；验收：自测 22/22（含两条负样本仍判红）· 全量违例 34 → 32 条 · 基线外新增 2 → 0 · 末行 0 FAIL · 基线 32 条无需收紧。
> - **⑯ CI 复检第六条根修（CI 自身产物触发 C4-f 假红·E-308）**：本批最后一笔推送后 CI 主 run 的 Delivery Gate 判红，**唯一红项是第 31 槽 2 FAIL**（本地 check_doc_sync.py 0 FAIL）⇒ 排查排除「本地工作树脏 / 浅克隆 / 行尾差异」三个解释（LF 工作树里跑仍 0 FAIL）⇒ 在 LF 工作树里改写两份探针报告的 `generated_at` 模拟「CI 现跑过」⇒ 报出与 CI 完全一致的 2 条 C4-f ⇒ 根因坐实：**探针报告入库后，CI 在 verify 前现跑探针会重写入库文件 ⇒ 工作树残留 ⇒「漏 add」防线把 CI 自己的临时产物判红**⇒ 修法：CI 现跑后 `git checkout --` 还原工作树；检测不降级（入库报告带 page_sha ⇒「报告陈旧」fail-closed 仍由入库产物承担，CI 现跑仍承担「页面在 CI 可渲染」的自证）⇒ 判据产物入库后，新鲜度应由内容哈希承担，而非由「CI 现跑覆盖」承担。
> - **⑩ 状态**：已收官（第 82 槽 0 FAIL + 第 83 槽 0 FAIL + L-01/L-02 清偿 + 九条坑表沉淀 + 报告 T119 落盘）。
> - **文件**： site/data/,site/en/,site/dashboard.html,scripts/svg_text_contrast_probe.js,scripts/output/chart-content-baseline.txt,scripts/output/chart-label-clipping-baseline.txt,scripts/output/chart-legend-exemptions.txt,scripts/output/chart-legend-render-audit.json,scripts/output/svg_text_contrast_graphic_report.json,scripts/output/svg_text_contrast_report.json,pitfalls.md,archive/docs/pitfalls-detail-ARCHIVE.md,docs/11-方案报告/计划方案/T119-任务计划执行与经验沉淀报告-2026-11-21.md,docs/11-方案报告/README.md,docs/00-导读/W批次编号对账表.md,CHANGELOG.md

# 更新日志

📖 阅读契约（W707）**：查表型——判断「当前版本/最近批次」时只读**顶段 1 个版本段**；查历史段用 grep（`grep -A 30 "### vX"`）；完整通读非预期用法（历史细节在 archive/docs/CHANGELOG-ARCHIVE*.md·grep 单段查勿打开通读）。
本项目所有重要变更均记录于此。格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/)。

## [Unreleased]

> **W### 编号规则**：每个版本段标注唯一 W### ID（W001-W1347），v0.8 内部细分 W008.1-W008.7（B0-B7）。每个 W 附四件套字段（来源/文件/验证/状态）。反向索引见 [scripts/output/file-index.md](scripts/output/file-index.md)（给定文件查改几次）。
>
> **v/W 双键口径（W706）**：时间点查询以 W 号为准（单调键）；v 号在 W659-W667 合并段/并行批次区间不单调（v2.3.262〔W661〕列于 v2.3.261〔W666〕后）；v 号形态演化（阶段标签化·方案 D）经盘点 docs/superpowers/plans/2026-10-11-version-space-inventory.md 后另批实施。
>
> **方案 D 形态切换（W711 生效）**：自 W711 段起，CHANGELOG 段标题去 v 号（新形态 `### W###（日期）：标题`）；W001-W1000 段保留 `### vX.Y.Z（日期）：W###` 历史形态不改写；v 号降格为阶段标签（v2.3·无 patch）；CITATION.cff version 改批次号形态（"W###"·CFF free string）；file-index 历史条目保留 v 引用、新增条目 W only。
>
> **历史版本归档**：v0.1 - v2.3.17（W001-W1000）已迁移至 [archive/docs/CHANGELOG-ARCHIVE-tier2.md](archive/docs/CHANGELOG-ARCHIVE-tier2.md)（W513 二级归档）；W422 再归档 v2.3.18-v2.3.31（W400-W416）段；W511 归档 v2.3.32-v2.3.82（W417-W464）段 + v2.3.83（W484）段至 [CHANGELOG-ARCHIVE.md](archive/docs/CHANGELOG-ARCHIVE.md)。W681 归档 v2.3.84-v2.3.249（W485-W649）段至 [CHANGELOG-ARCHIVE.md](archive/docs/CHANGELOG-ARCHIVE.md)。W736 再归档 v2.3.250-v2.3.293（W650-W699）段至 [CHANGELOG-ARCHIVE.md](archive/docs/CHANGELOG-ARCHIVE.md)（源文件超 50KB/500 行阈值）。本文件正本按 110 段窗滚动（W960 窗口制·正本最老段随批推进·早期形态：W650-W710 段用历史 vX.Y.Z 形态·W711+ 段用批次键 W### 形态）。
>
> **全站页数口径**（W459 建·W702 实跑刷新，各门禁分母不同）：HTML 共 875<!--stats:html_total--> 页（site/data 91<!--stats:site_data_html--> + site/en 138<!--stats:site_en_html--> + site 根 10<!--stats:site_root_html--> + site/reader 636<!--stats:site_reader_html-->）；CSP 覆盖 874<!--stats:csp_covered--> 页（排除 `_template.html`）；check_js_syntax/check_structure 扫 873<!--stats:scan_files--> 文件（再排除 `_shell.html`）；check_seo_head 扫 873<!--stats:seo_scanned--> 页（site 全树减两个模板壳）；inline_css 同步 638<!--stats:inline_css_pages--> 页（site 全树含 INLINED 标记页）；「可视化页 90<!--stats:visualization_pages-->」= site/data 88 减 `_shell.html`。
>
> **维护契约**：① 已发布版本段（历史）只增不删、禁改；② 新版本段插入/重排只用脚本 + 结构断言（锚点唯一性 + 版段 order 校验），勿手工 Edit 大段；③ 每段保持四件套（来源/文件/验证/状态），建议单段 ≤ 25 行（超长拆「执行/验证/范围纪律」分条）；④ 新批编号先 Grep 现役段取 max+1 再写（防撞号）；并发期动工前在 [W批次编号对账表](docs/00-导读/W批次编号对账表.md) 登记认领（W663 起·版段递延时以对账表为准）。
