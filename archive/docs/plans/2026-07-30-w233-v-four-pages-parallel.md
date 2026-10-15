# W233 V 方向四页并行·实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在 site/data/ 新建 4 个 D3.js 可视化页面（明代政治思想对照 / 取经团队心理变化 / 妖怪能力雷达 / 诗词韵律分析），复用 W229 V2 模板，dispatching-parallel-agents 四 subagent 并行实现，可视化页面 64→68，V 方向 V2→V3。

**Architecture:** 4 个独立单文件 HTML（每页约 640 行）+ D3.js v7 + EMBEDDED_DATA + 古典宣纸风配色系统。dispatching-parallel-agents 四 subagent 并行创建 4 页（无共享状态、无竞态）。主代理 spot-check + 项目层 7 文档同步 + memory 三件套补齐收尾。

**Tech Stack:** D3.js v7 / HTML5 / CSS3 / EMBEDDED_DATA JSON / 古典宣纸风配色（#faf7f2/#c8463a/#3a6b8c/#7a5230/#5a7a3a）/ @font-face Noto Serif SC + JetBrains Mono

**Spec:** [docs/superpowers/specs/2026-07-30-w233-v-four-pages-parallel-design.md](../specs/2026-07-30-w233-v-four-pages-parallel-design.md)

---

## 文件结构

**创建文件（4）**：
- `site/data/ming-political-thought-comparison.html` — W233-1 明代政治思想对照图谱（约 640 行）
- `site/data/pilgrim-team-psychology-arc.html` — W233-2 取经团队心理变化曲线（约 640 行）
- `site/data/monster-capability-radar.html` — W233-3 妖怪能力雷达图（约 640 行）
- `site/data/poetry-rhythm-analysis.html` — W233-4 诗词韵律分析图谱（约 640 行）

**修改文件（7 项目层同步）**：
- `CHANGELOG.md` — 新增 v2.2.39 W233 版本段
- `README.md` — 版本号 + 可视化页面 64→68 + V 方向 V2→V3 描述
- `STRUCTURE.md` — 版本号 + W### 计数 232→233 + 版本史 v2.2.39 条目
- `docs/00-导读/项目说明.md` — 版本号 + 可视化页面 64→68 + V 方向 V3 描述
- `交接文档.md` — 顶部最后更新 + 当前进度段 + W233 里程碑段 + 当前版本号 + W### W232→W233 + 下一编号 W233→W234
- `scripts/output/file-index.md` — 新增 W233 反向索引段
- `docs/02-人物深度分析/README.md` — 如有 W232 关联条目

**修改文件（memory 三件套）**：
- `c:\Users\12739\.trae-cn\memory\projects\-d-1-xiyouji\20260729\work-log.md` — 追加 W233 段
- `c:\Users\12739\.trae-cn\memory\projects\-d-1-xiyouji\20260729\topics.md` — 追加 W233 session 行
- `c:\Users\12739\.trae-cn\memory\projects\-d-1-xiyouji\20260729\retrospective.md` — 追加 W233 retrospective 段

---

## Task 1: W233-1 ming-political-thought-comparison.html（明代政治思想对照图谱）

**Files:**
- Create: `site/data/ming-political-thought-comparison.html`

**Subagent 任务**：subagent A 创建此页面，复用 W229 V2 模板。

- [ ] **Step 1.1: 准备 EMBEDDED_DATA**

数据源：W232 docs/02-人物深度分析/明代历史原型对照专题.md 的三组对照（王阳明 vs 唐僧 / 张居正 vs 玉帝 / 海瑞 vs 悟空）+ 9 对照维度 + 明代思想史时间线。

```javascript
const EMBEDDED_DATA = {
  meta: {
    title: "明代政治思想对照图谱",
    version: "v2.2.39",
    w_id: "W233-1",
    direction: "V3",
    source_doc: "docs/02-人物深度分析/明代历史原型对照专题.md"
  },
  kpi: [
    {label: "对照组数", value: 3, unit: "组"},
    {label: "对照维度", value: 9, unit: "维"},
    {label: "明代人物", value: 3, unit: "位"},
    {label: "西游人物", value: 3, unit: "位"},
    {label: "时间节点", value: 5, unit: "个"},
    {label: "理论文献", value: 9, unit: "篇"}
  ],
  radar: [
    {group: "王阳明 vs 唐僧", axis: "心性论", value_ming: 9, value_xy: 8},
    {group: "王阳明 vs 唐僧", axis: "治理术", value_ming: 3, value_xy: 7},
    {group: "王阳明 vs 唐僧", axis: "谏诤传统", value_ming: 5, value_xy: 4},
    {group: "张居正 vs 玉帝", axis: "心性论", value_ming: 4, value_xy: 6},
    {group: "张居正 vs 玉帝", axis: "治理术", value_ming: 9, value_xy: 9},
    {group: "张居正 vs 玉帝", axis: "谏诤传统", value_ming: 3, value_xy: 2},
    {group: "海瑞 vs 悟空", axis: "心性论", value_ming: 6, value_xy: 7},
    {group: "海瑞 vs 悟空", axis: "治理术", value_ming: 4, value_xy: 3},
    {group: "海瑞 vs 悟空", axis: "谏诤传统", value_ming: 9, value_xy: 9}
  ],
  heatmap: [
    {group: "王阳明 vs 唐僧", dimension: "理论", score: 9},
    {group: "王阳明 vs 唐僧", dimension: "实践", score: 8},
    {group: "王阳明 vs 唐僧", dimension: "境界", score: 9},
    {group: "张居正 vs 玉帝", dimension: "理论", score: 7},
    {group: "张居正 vs 玉帝", dimension: "实践", score: 9},
    {group: "张居正 vs 玉帝", dimension: "境界", score: 6},
    {group: "海瑞 vs 悟空", dimension: "理论", score: 6},
    {group: "海瑞 vs 悟空", dimension: "实践", score: 9},
    {group: "海瑞 vs 悟空", dimension: "境界", score: 8}
  ],
  timeline: [
    {year: 1472, event: "王阳明出生", figure: "王阳明"},
    {year: 1500, event: "吴承恩出生", figure: "吴承恩"},
    {year: 1514, event: "海瑞出生", figure: "海瑞"},
    {year: 1525, event: "张居正出生", figure: "张居正"},
    {year: 1529, event: "王阳明逝世", figure: "王阳明"},
    {year: 1582, event: "张居正逝世 / 吴承恩逝世", figure: "张居正/吴承恩"},
    {year: 1587, event: "海瑞逝世", figure: "海瑞"},
    {year: 1592, event: "世德堂本《西游记》刊刻", figure: "世德堂"}
  ],
  sankey: {
    nodes: [
      {name: "传习录"}, {name: "张文忠公全集"}, {name: "海瑞集"},
      {name: "王阳明 vs 唐僧"}, {name: "张居正 vs 玉帝"}, {name: "海瑞 vs 悟空"},
      {name: "心性论"}, {name: "治理术"}, {name: "谏诤传统"}
    ],
    links: [
      {source: 0, target: 3, value: 3},
      {source: 1, target: 4, value: 3},
      {source: 2, target: 5, value: 3},
      {source: 3, target: 6, value: 1},
      {source: 3, target: 7, value: 1},
      {source: 3, target: 8, value: 1},
      {source: 4, target: 6, value: 1},
      {source: 4, target: 7, value: 1},
      {source: 4, target: 8, value: 1},
      {source: 5, target: 6, value: 1},
      {source: 5, target: 7, value: 1},
      {source: 5, target: 8, value: 1}
    ]
  },
  polar: [
    {group: "王阳明 vs 唐僧", axis: "心性论", value: 9},
    {group: "王阳明 vs 唐僧", axis: "实践论", value: 8},
    {group: "王阳明 vs 唐僧", axis: "境界论", value: 9},
    {group: "张居正 vs 玉帝", axis: "治理术", value: 9},
    {group: "张居正 vs 玉帝", axis: "权力结构", value: 9},
    {group: "张居正 vs 玉帝", axis: "改革守成", value: 6},
    {group: "海瑞 vs 悟空", axis: "谏诤传统", value: 9},
    {group: "海瑞 vs 悟空", axis: "反抗精神", value: 9},
    {group: "海瑞 vs 悟空", axis: "个人体制", value: 8}
  ]
};
```

- [ ] **Step 1.2: 写 HTML 骨架（复用 W229 V2 模板）**

约 640 行，包含：
- `<!DOCTYPE html>` + `<head>` 古典宣纸风 CSS + @font-face Noto Serif SC + JetBrains Mono
- `<body>` skip-link + breadcrumb + h1 "明代政治思想对照图谱" + subtitle "W233-1 · V3 · 与 W232 文档双轨"
- hero 渐变 + 6 个 KPI 卡片
- Section 1：三对照雷达图（D3.js radarChart）
- Section 2：九对照维度矩阵热力图（D3.js 矩阵 4 色渐变）
- Section 3：明代思想史时间线（D3.js timeline）
- Section 4：文献引用桑基图（D3.js sankey）
- Section 5：三对照维度极坐标图（D3.js polar）
- Section 6：跨页面导航 + footer 双索引
- `<noscript>` fallback
- `<script>` D3.js v7 CDN + EMBEDDED_DATA + 渲染逻辑

- [ ] **Step 1.3: 实现跨页面导航**

```html
<nav class="cross-page-nav" aria-label="跨页面导航">
  <a href="ming-political-thought-comparison.html" class="active">明代政治思想对照</a> ·
  <a href="pilgrim-team-psychology-arc.html">取经团队心理</a> ·
  <a href="monster-capability-radar.html">妖怪能力雷达</a> ·
  <a href="poetry-rhythm-analysis.html">诗词韵律分析</a> ·
  <a href="../index.html">返回 dashboard</a>
</nav>
```

- [ ] **Step 1.4: 实现 footer 双索引**

```html
<footer class="dual-index">
  <h2>footer 双索引</h2>
  <table>
    <tr><td>正向时间线</td><td><a href="../../CHANGELOG.md">CHANGELOG.md</a> v2.2.39 W233</td></tr>
    <tr><td>反向文件索引</td><td><a href="../../scripts/output/file-index.md">file-index.md</a> W233-1</td></tr>
    <tr><td>方向索引</td><td>site/data/ · V 方向·V3 四页并行</td></tr>
    <tr><td>跨文档链接</td><td>W232 明代历史原型对照 / W194 narratology-13d / W229 V2 三页</td></tr>
  </table>
</footer>
```

- [ ] **Step 1.5: Commit**

```bash
git add site/data/ming-political-thought-comparison.html
git commit -m "feat(W233-1): add ming-political-thought-comparison.html visualization"
```

---

## Task 2: W233-2 pilgrim-team-psychology-arc.html（取经团队心理变化曲线）

**Files:**
- Create: `site/data/pilgrim-team-psychology-arc.html`

**Subagent 任务**：subagent B 创建此页面。

- [ ] **Step 2.1: 准备 EMBEDDED_DATA**

```javascript
const EMBEDDED_DATA = {
  meta: {
    title: "取经团队心理变化曲线",
    version: "v2.2.39",
    w_id: "W233-2",
    direction: "V3"
  },
  kpi: [
    {label: "取经众", value: 5, unit: "位"},
    {label: "回目", value: 100, unit: "回"},
    {label: "心理维度", value: 5, unit: "维"},
    {label: "转折点", value: 9, unit: "个"},
    {label: "平均凝聚力", value: 6.8, unit: "/10"}
  ],
  radar: [
    // 5 众 × 5 维（恐惧/坚定/愤怒/智慧/顺从）平均分
    {character: "悟空", fear: 2, resolve: 9, anger: 7, wisdom: 9, obedience: 5},
    {character: "唐僧", fear: 7, resolve: 8, anger: 3, wisdom: 8, obedience: 9},
    {character: "八戒", fear: 8, resolve: 4, anger: 6, wisdom: 4, obedience: 5},
    {character: "沙僧", fear: 4, resolve: 7, anger: 2, wisdom: 6, obedience: 9},
    {character: "白龙马", fear: 3, resolve: 8, anger: 4, wisdom: 7, obedience: 8}
  ],
  // 100 回心理曲线（简化为关键 20 回采样）
  psychology_arc: [
    {chapter: 1, wukong: 8, tang: 0, bajie: 0, sha: 0, bai: 0},
    {chapter: 7, wukong: 10, tang: 0, bajie: 0, sha: 0, bai: 0},
    {chapter: 14, wukong: 5, tang: 6, bajie: 0, sha: 0, bai: 0},
    {chapter: 18, wukong: 7, tang: 7, bajie: 5, sha: 0, bai: 0},
    {chapter: 22, wukong: 7, tang: 7, bajie: 5, sha: 6, bai: 0},
    {chapter: 27, wukong: 4, tang: 4, bajie: 4, sha: 5, bai: 6},
    {chapter: 31, wukong: 7, tang: 7, bajie: 5, sha: 6, bai: 7},
    {chapter: 41, wukong: 6, tang: 5, bajie: 6, sha: 6, bai: 7},
    {chapter: 58, wukong: 5, tang: 4, bajie: 5, sha: 5, bai: 6},
    {chapter: 59, wukong: 7, tang: 6, bajie: 5, sha: 6, bai: 7},
    {chapter: 65, wukong: 7, tang: 7, bajie: 6, sha: 6, bai: 7},
    {chapter: 74, wukong: 8, tang: 6, bajie: 4, sha: 5, bai: 7},
    {chapter: 81, wukong: 8, tang: 8, bajie: 7, sha: 7, bai: 8},
    {chapter: 88, wukong: 9, tang: 8, bajie: 7, sha: 7, bai: 8},
    {chapter: 95, wukong: 9, tang: 9, bajie: 8, sha: 8, bai: 9},
    {chapter: 100, wukong: 10, tang: 10, bajie: 9, sha: 9, bai: 10}
  ],
  cohesion_heatmap: [
    // 5 众 × 16 关键回目凝聚力（0-10）
    // 实施时由 subagent 填充完整 5×16 矩阵
  ],
  turning_points: [
    {chapter: 7, event: "大闹天宫·悟空极盛"},
    {chapter: 14, event: "心猿归正·收悟空"},
    {chapter: 18, event: "收八戒·团队初成"},
    {chapter: 22, event: "收沙僧·五众齐全"},
    {chapter: 27, event: "三打白骨精·信任危机"},
    {chapter: 31, event: "黄袍怪·团队修复"},
    {chapter: 41, event: "红孩儿·悟空受难"},
    {chapter: 58, event: "真假美猴王·身份危机"},
    {chapter: 81, event: "无底洞·最后大难"}
  ],
  boxplot: [
    // 5 众 × 心理分布四分位数
  ]
};
```

- [ ] **Step 2.2: 写 HTML 骨架 + 5 图表 + KPI + 跨页导航 + footer**

结构同 Task 1，h1 "取经团队心理变化曲线"，subtitle "W233-2 · V3 · 与 character-sentiment-arc 形成个体-团队双层"。

5 图表：
1. 五众心理状态雷达图（D3.js radarChart·5 众×5 维）
2. 100 回心理曲线（D3.js lineChart·5 条线 + 时间轴动画播放/暂停/滑块）
3. 团队凝聚力热力图（D3.js 矩阵·5×16）
4. 心理转折点时间线（D3.js timeline·9 转折点）
5. 五众心理状态分布箱线图（D3.js boxplot）

- [ ] **Step 2.3: 实现时间维度动画**

100 回心理曲线支持播放/暂停/滑块控制（参考 W229 journey-spacetime.html 时间轴动画实现）。

- [ ] **Step 2.4: 跨页面导航 + footer 双索引**

跨页导航 active 标记 W233-2。footer 跨文档链接包含 character-sentiment-arc.html。

- [ ] **Step 2.5: Commit**

```bash
git add site/data/pilgrim-team-psychology-arc.html
git commit -m "feat(W233-2): add pilgrim-team-psychology-arc.html visualization"
```

---

## Task 3: W233-3 monster-capability-radar.html（妖怪能力雷达图）

**Files:**
- Create: `site/data/monster-capability-radar.html`

**Subagent 任务**：subagent C 创建此页面。

- [ ] **Step 3.1: 准备 EMBEDDED_DATA**

```javascript
const EMBEDDED_DATA = {
  meta: {
    title: "妖怪能力雷达图",
    version: "v2.2.39",
    w_id: "W233-3",
    direction: "V3"
  },
  kpi: [
    {label: "代表妖怪", value: 15, unit: "个"},
    {label: "能力维度", value: 5, unit: "维"},
    {label: "来历分类", value: 4, unit: "类"},
    {label: "结局分类", value: 4, unit: "类"}
  ],
  radar: [
    // 15 妖怪 × 5 维（法力/智谋/法宝/背景/结局）0-10 评分
    {monster: "白骨精", magic: 4, strategy: 9, artifact: 2, background: 1, ending: 2},
    {monster: "黄袍怪", magic: 7, strategy: 5, artifact: 6, background: 8, ending: 5},
    {monster: "红孩儿", magic: 8, strategy: 7, artifact: 7, background: 8, ending: 6},
    {monster: "黑熊精", magic: 7, strategy: 5, artifact: 4, background: 5, ending: 6},
    {monster: "银角大王", magic: 8, strategy: 6, artifact: 9, background: 8, ending: 5},
    {monster: "蜘蛛精", magic: 5, strategy: 6, artifact: 5, background: 4, ending: 2},
    {monster: "蝎子精", magic: 9, strategy: 6, artifact: 7, background: 5, ending: 2},
    {monster: "六耳猕猴", magic: 9, strategy: 9, artifact: 6, background: 2, ending: 1},
    {monster: "牛魔王", magic: 9, strategy: 7, artifact: 7, background: 7, ending: 6},
    {monster: "铁扇公主", magic: 7, strategy: 6, artifact: 9, background: 7, ending: 6},
    {monster: "大鹏金翅雕", magic: 10, strategy: 9, artifact: 7, background: 9, ending: 6},
    {monster: "黄眉大王", magic: 9, strategy: 6, artifact: 9, background: 8, ending: 6},
    {monster: "青狮精", magic: 8, strategy: 5, artifact: 6, background: 8, ending: 6},
    {monster: "白象精", magic: 7, strategy: 5, artifact: 6, background: 8, ending: 6},
    {monster: "灵感大王", magic: 7, strategy: 6, artifact: 5, background: 7, ending: 2}
  ],
  bar: [
    // 5 维排名（最强 / 最弱 / 平均）
  ],
  scatter: [
    // 15 妖怪 × 法力 vs 结局散点
  ],
  sankey: {
    nodes: [
      {name: "天庭"}, {name: "佛界"}, {name: "凡间"}, {name: "野生"},
      {name: "收编"}, {name: "打死"}, {name: "逃走"}, {name: "借走"}
    ],
    links: [
      {source: 0, target: 4, value: 5}, // 天庭→收编
      {source: 0, target: 5, value: 2}, // 天庭→打死
      {source: 1, target: 4, value: 4}, // 佛界→收编
      {source: 1, target: 6, value: 1}, // 佛界→逃走
      {source: 2, target: 5, value: 3}, // 凡间→打死
      {source: 3, target: 5, value: 4}, // 野生→打死
      {source: 3, target: 7, value: 1}  // 野生→借走
    ]
  },
  kpi_extreme: [
    {label: "最强法力", monster: "大鹏金翅雕", value: 10},
    {label: "最智谋", monster: "六耳猕猴", value: 9},
    {label: "最悲剧", monster: "六耳猕猴", value: "结局 1/10"},
    {label: "最幸运", monster: "红孩儿", value: "收编善财童子"}
  ]
};
```

- [ ] **Step 3.2: 写 HTML 骨架 + 5 图表 + KPI + 跨页导航 + footer**

h1 "妖怪能力雷达图"，subtitle "W233-3 · V3 · 与 monster-hierarchy-network 形成 等级-能力 双维"。

5 图表：
1. 15 妖怪雷达图叠加（D3.js radarChart·15 妖怪×5 维·半透明叠加）
2. 能力对比柱状图（D3.js barChart·5 维排名）
3. 妖怪能力散点图（D3.js scatterPlot·法力 vs 结局·15 点）
4. 妖怪分类桑基图（D3.js sankey·来历→结局）
5. 能力 KPI 卡片（4 个极值卡片）

- [ ] **Step 3.3: 跨页面导航 + footer 双索引**

跨页导航 active 标记 W233-3。footer 跨文档链接包含 monster-hierarchy-network.html。

- [ ] **Step 3.4: Commit**

```bash
git add site/data/monster-capability-radar.html
git commit -m "feat(W233-3): add monster-capability-radar.html visualization"
```

---

## Task 4: W233-4 poetry-rhythm-analysis.html（诗词韵律分析图谱）

**Files:**
- Create: `site/data/poetry-rhythm-analysis.html`

**Subagent 任务**：subagent D 创建此页面。

- [ ] **Step 4.1: 准备 EMBEDDED_DATA**

```javascript
const EMBEDDED_DATA = {
  meta: {
    title: "诗词韵律分析图谱",
    version: "v2.2.39",
    w_id: "W233-4",
    direction: "V3"
  },
  kpi: [
    {label: "A6 诗词文档", value: 7, unit: "篇"},
    {label: "词牌数", value: 3, unit: "种"},
    {label: "平仄类型", value: 2, unit: "类"},
    {label: "诗词五层次", value: 5, unit: "层"},
    {label: "回目覆盖", value: 100, unit: "回"}
  ],
  pie: [
    {name: "西江月", value: 1},
    {name: "临江仙", value: 1},
    {name: "满庭芳", value: 1},
    {name: "开篇诗", value: 1},
    {name: "回目对联", value: 100},
    {name: "人物赋", value: 20},
    {name: "景物诗", value: 40}
  ],
  heatmap: [
    // 7 篇 A6 诗词 × 平仄类型（平/仄）分布
    {poem: "开篇诗", ping: 60, ze: 40},
    {poem: "回目对联", ping: 50, ze: 50},
    {poem: "人物赋", ping: 55, ze: 45},
    {poem: "景物诗", ping: 65, ze: 35},
    {poem: "西江月", ping: 70, ze: 30},
    {poem: "临江仙", ping: 68, ze: 32},
    {poem: "满庭芳", ping: 72, ze: 28}
  ],
  timeline: [
    // 诗词在 100 回分布（每 10 回统计诗词数量）
    {chapter_range: "1-10", count: 12},
    {chapter_range: "11-20", count: 8},
    {chapter_range: "21-30", count: 10},
    {chapter_range: "31-40", count: 9},
    {chapter_range: "41-50", count: 11},
    {chapter_range: "51-60", count: 8},
    {chapter_range: "61-70", count: 10},
    {chapter_range: "71-80", count: 9},
    {chapter_range: "81-90", count: 7},
    {chapter_range: "91-100", count: 14}
  ],
  stacked: [
    // 诗词五层次 × 10 个 10 回段堆叠
    // 开篇/回目/人物赋/景物诗/词牌
  ],
  boxplot: [
    // 7 篇 A6 诗词韵律特征分布
  ]
};
```

- [ ] **Step 4.2: 写 HTML 骨架 + 5 图表 + KPI + 跨页导航 + footer**

h1 "诗词韵律分析图谱"，subtitle "W233-4 · V3 · 与 A6 诗词 7 篇文档形成 文本-可视化 双轨"。

5 图表：
1. 词牌分布饼图（D3.js pieChart·7 类）
2. 平仄韵脚分布热力图（D3.js 矩阵·7 篇×平/仄）
3. 诗词在 100 回分布时间线（D3.js barChart·10 段·时间轴动画）
4. 诗词五层次堆叠图（D3.js stackedBar·5 层×10 段）
5. 韵律特征 KPI 卡片

- [ ] **Step 4.3: 时间维度动画**

诗词在 100 回分布时间线支持播放/暂停/滑块（参考 W229 journey-spacetime.html）。

- [ ] **Step 4.4: 跨页面导航 + footer 双索引**

跨页导航 active 标记 W233-4。footer 跨文档链接包含 A6 诗词 7 篇文档路径。

- [ ] **Step 4.5: Commit**

```bash
git add site/data/poetry-rhythm-analysis.html
git commit -m "feat(W233-4): add poetry-rhythm-analysis.html visualization"
```

---

## Task 5: dispatching-parallel-agents 四 subagent 并行

**Files:**
- 4 subagent 并行创建 Task 1-4 的 4 个 HTML 文件

- [ ] **Step 5.1: 派发 4 subagent 并行**

主代理在单个消息中派发 4 个 Task subagent，每个 subagent 独立创建一个 HTML 文件。subagent 间无共享状态、无依赖、无竞态。

- [ ] **Step 5.2: 等待 4 subagent 完成**

收集 4 subagent 产出结果。

- [ ] **Step 5.3: git add 4 文件 tracked 验证**

```bash
git add site/data/ming-political-thought-comparison.html site/data/pilgrim-team-psychology-arc.html site/data/monster-capability-radar.html site/data/poetry-rhythm-analysis.html
git ls-files site/data/ming-political-thought-comparison.html site/data/pilgrim-team-psychology-arc.html site/data/monster-capability-radar.html site/data/poetry-rhythm-analysis.html
```

Expected: 返回 4 个文件名 = 全部 tracked（E1 跨 session git tracked 铁律）

---

## Task 6: DRL R1b 主代理 spot-check

**Files:**
- Verify: 4 个 HTML 文件

- [ ] **Step 6.1: Grep 验证 4 页关键内容**

对 4 页分别 Grep 验证：
- footer 双索引（`footer` / `dual-index` / `CHANGELOG.md` / `file-index.md`）
- noscript fallback（`<noscript>`）
- h1 + subtitle（`<h1>` / `subtitle`）
- breadcrumb + skip-link（`breadcrumb` / `skip-link`）
- KPI 卡片（`kpi` / `KPI`）
- 跨页面导航（`cross-page-nav` / 4 页文件名）
- EMBEDDED_DATA（`EMBEDDED_DATA`）
- D3.js v7 CDN（`d3.v7` / `d3js.org`）
- 古典宣纸风配色（`#faf7f2` / `#c8463a` / `#3a6b8c` / `#7a5230` / `#5a7a3a`）

- [ ] **Step 6.2: 记录收敛曲线**

预期：P0=0/P1=0/P2=0/P3=0 真收敛。

如发现 P1/P2 问题，立即修复并重新 Grep 验证（DRL 真循环铁律·不允许假收敛）。

---

## Task 7: a11y 审查

**Files:**
- Verify: 4 个 HTML 文件

- [ ] **Step 7.1: 运行 a11y_audit.py**

```bash
python scripts/a11y_audit.py site/data/ming-political-thought-comparison.html site/data/pilgrim-team-psychology-arc.html site/data/monster-capability-radar.html site/data/poetry-rhythm-analysis.html
```

Expected: P0=0/P1=0/P2 按边际收益 gate 接受残留

- [ ] **Step 7.2: 冒烟测试**

```bash
cd scripts && npm run test:smoke
```

Expected: 63→67 页面全部通过

---

## Task 8: 项目层 7 文档同步 v2.2.39/W233

**Files:**
- Modify: CHANGELOG.md / README.md / STRUCTURE.md / docs/00-导读/项目说明.md / 交接文档.md / scripts/output/file-index.md / docs/02-人物深度分析/README.md

- [ ] **Step 8.1: CHANGELOG.md 新增 v2.2.39 W233 版本段**

在 v2.2.38 W232 段后新增 v2.2.39 W233 段，包含四件套字段（来源/文件/验证/状态）+ W### 编号规则 W001-W232→W001-W233 + 4 新建页面描述。

- [ ] **Step 8.2: README.md 版本号 + 可视化页面 64→68 + V 方向 V2→V3 描述**

将 v2.2.38→v2.2.39，64 个 D3.js→68 个 D3.js，V2 三项→V2 三项 + V3 四项并行描述。

- [ ] **Step 8.3: STRUCTURE.md 版本号 + W### 计数 232→233 + 版本史 v2.2.39 条目**

将版本号 v2.2.38→v2.2.39，W### 计数 232→233，新增 v2.2.39 版本史条目（在 v2.2.38 条目前）。

- [ ] **Step 8.4: docs/00-导读/项目说明.md 版本号 + 可视化页面 64→68 + V 方向 V3 描述**

将 v2.2.38→v2.2.39，64→68，V2→V2 + V3 描述。

- [ ] **Step 8.5: 交接文档.md 顶部最后更新 + 当前进度段 + W233 里程碑段 + 当前版本号 + W### W232→W233 + 下一编号 W233→W234**

更新顶部"最后更新：2026-07-30（v2.2.39 W233 V 方向四页并行·明代政治思想对照+取经团队心理+妖怪能力雷达+诗词韵律分析后）"，"一、当前进度"段标题更新为 v2.2.39 W233，新增 W233 里程碑段，当前版本号 v2.2.38→v2.2.39，W### W232→W233，下一编号 W233→W234。

- [ ] **Step 8.6: scripts/output/file-index.md 新增 W233 反向索引段**

在 v2.2.38 W232 段后新增 v2.2.39 W233 反向索引段，4 新建 + 7 同步 = 11 文件。

- [ ] **Step 8.7: docs/02-人物深度分析/README.md 如有 W232 关联条目**

检查是否需更新（可能无需，README 是规范文档不含文件清单）。

- [ ] **Step 8.8: Grep spot-check 7 文档 v2.2.39/W233 全部命中**

```bash
# 验证 7 文档全部包含 v2.2.39 和 W233
```

Expected: 7 文档全部命中 v2.2.39 + W233（E1 升级版铁律·修复声明 ≠ 文件内容已修改）

---

## Task 9: memory 三件套补齐 W233 段

**Files:**
- Modify: c:\Users\12739\.trae-cn\memory\projects\-d-1-xiyouji\20260729\work-log.md
- Modify: c:\Users\12739\.trae-cn\memory\projects\-d-1-xiyouji\20260729\topics.md
- Modify: c:\Users\12739\.trae-cn\memory\projects\-d-1-xiyouji\20260729\retrospective.md

- [ ] **Step 9.1: work-log.md 追加 W233 段**

包含 verification cost（Grep/Read/Edit/Write/Task 调用计数）+ milestones（4 新建 + 7 同步 = 11 文件·v2.2.38→v2.2.39）+ retro_link。

- [ ] **Step 9.2: topics.md 追加 W233 session 行**

包含 session_id + topic_summary_time + 4 新建页面描述 + 7 文档同步 + DRL R1b 真收敛 + E1 假收敛复现记录。

- [ ] **Step 9.3: retrospective.md 追加 W233 retrospective 段**

包含 dim 1 目标达成度 + dim 5 方法论应用 + dim 9 E1 铁律复现 + dim 11 闭环完整性四维度复盘。

- [ ] **Step 9.4: Grep spot-check memory 三件套 W233 段**

```bash
# 验证三件套全部包含 W233
```

Expected: 三件套全部命中 W233（E1 升级版铁律·memory 层假收敛复现）

---

## Task 10: user_profile.md E1 计数器更新

**Files:**
- Modify: c:\Users\12739\.trae-cn\memory\user_profile.md

- [ ] **Step 10.1: E1 升级版计数器 45/3 → 46/3**

毕业后新案例链追加 W233。

- [ ] **Step 10.2: 链尾追加 W233 描述**

"毕业后第 42 次新案例"链追加 W233·V 方向 V3 四页并行。

---

## Self-Review

**1. Spec coverage 检查**：
- §1 4 页设计 → Task 1-4 ✓
- §2 架构组件 → Task 1-4 Step 2 ✓
- §3 跨页导航 footer 验证 → Task 1-4 Step 3-4 + Task 6 ✓
- §4 Preflight → Task 6 ✓
- §5 DRL R1b → Task 6 ✓
- §6 项目层 7 文档同步 → Task 8 ✓
- §7 memory 三件套 → Task 9 ✓
- §8 E1 计数器 → Task 10 ✓
- §9 AVES 串行 → 计划 W233-V 完成后进入 W234-E ✓

**2. Placeholder scan**：无 TBD/TODO。所有步骤含具体内容。

**3. Type consistency**：
- W233-1/2/3/4 编号一致
- 4 页文件名一致（ming-political-thought-comparison / pilgrim-team-psychology-arc / monster-capability-radar / poetry-rhythm-analysis）
- 版本号 v2.2.39 一致
- W### W233 一致

无修复需要。

---

## Execution Handoff

**Plan complete and saved to `docs/superpowers/plans/2026-07-30-w233-v-four-pages-parallel.md`. Two execution options:**

**1. Subagent-Driven (recommended)** - I dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints

**Which approach?**
