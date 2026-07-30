# 详解西游记 · 设计规范

> 本文件记录项目前端视觉与交互规范，确保 38 个 D3.js 可视化页面 + dashboard 入口在「古典宣纸风」基调下保持一致性，并兼容 v0.9.1 引入的 Name That UI 组件语言。
>
> 适用对象：所有 `site/` 下的 HTML 页面、后续新增可视化页、dashboard 迭代。

---

## 1. 设计原则

### 1.1 视觉基调：古典宣纸风

- **灵感来源**：明代刻本、宣纸、朱砂批点、水墨层次。
- **核心隐喻**：把《西游记》的文本解读做成「可翻阅的数字刻本」，数据图表是「批注」，交互组件是「目录签」。
- **氛围关键词**：温润、厚重、留白、克制。

### 1.2 信息层级

1. **Hero 区**：深色渐变 + 大号标题，建立页面情绪。
2. **Section 卡片**：浅色底 + 细边框，承载主要内容。
3. **KPI / 数据卡片**：白底 + 阴影，作为入口或数据摘要。
4. **微件（badge/tab）**：小尺寸、低对比、圆角，用于分类与状态。

### 1.3 两条设计语言的边界

| 语言 | 来源 | 使用场景 | 核心特征 |
|:---|:---|:---|:---|
| 古典宣纸风 | 项目原生 | 可视化页、hero、section、insight-box | 暖灰底、朱砂红、靛青、深褐 |
| Name That UI 组件 | [Name That UI](https://namethatui.com/) | dashboard 筛选、搜索、徽章、空状态 | pill tab、搜索框、badge、a11y |

> 规则：Name That UI 组件的颜色、圆角、间距必须复用项目 token，禁止直接照搬原站色彩。

---

## 2. 设计 Token

### 2.1 基础色彩（12 个）

```css
:root {
    --bg: #faf7f2;          /* 宣纸底色：页面背景 */
    --paper: #ffffff;       /* 卡片底色：section、kpi-card */
    --ink: #2c2418;         /* 主文字：标题、正文 */
    --ink-soft: #6b5e4d;    /* 次级文字：描述、元信息 */
    --accent: #c8463a;      /* 朱砂红：主强调、链接、高亮 */
    --accent-soft: #e9b885; /* 淡金：hover 边框、次要强调 */
    --accent-2: #3a6b8c;    /* 靛青：数据系列 B、M-U 分类 */
    --accent-3: #7a5230;    /* 深褐：数据系列 C、表头 */
    --accent-4: #5a7a3a;    /* 苍绿：数据系列 D、A-L 分类 */
    --rebel: #8c2a2a;       /* 深红：警示、强烈对比 */
    --line: #d9cdb8;        /* 边框、分隔线 */
    --shadow: 0 1px 3px rgba(60, 40, 20, 0.08), 0 4px 12px rgba(60, 40, 20, 0.06);
}
```

### 2.2 扩展 Token（v0.9.1 Name That UI 迁移新增）

```css
:root {
    /* badge tokens */
    --badge-a-l-bg: rgba(90, 122, 58, 0.12);
    --badge-a-l-border: rgba(90, 122, 58, 0.25);
    --badge-m-u-bg: rgba(58, 107, 140, 0.12);
    --badge-m-u-border: rgba(58, 107, 140, 0.25);
    --badge-v-ah-bg: rgba(122, 82, 48, 0.12);
    --badge-v-ah-border: rgba(122, 82, 48, 0.25);
    --badge-q-plus-bg: rgba(200, 70, 58, 0.10);
    --badge-q-plus-border: rgba(200, 70, 58, 0.22);
    --badge-q-plusplus-bg: rgba(233, 184, 133, 0.18);
    --badge-q-plusplus-border: rgba(233, 184, 133, 0.35);

    /* focus ring tokens */
    --focus-ring-accent: rgba(200, 70, 58, 0.25);
    --focus-ring-accent-soft: rgba(233, 184, 133, 0.20);
    --focus-ring-clear: rgba(233, 184, 133, 0.35);

    /* table tokens */
    --cross-table-header-bg: #f5e9d4;
    --cross-table-highlight-bg: #fde8e6;
}
```

> 规则：新增组件必须先定义 token，再写样式；禁止在 CSS 中直接使用裸十六进制 / rgba（除 token 定义本身）。

### 2.3 色彩使用映射

| 元素 | Token | 说明 |
|:---|:---|:---|
| 页面背景 | `--bg` | 全局 |
| 卡片背景 | `--paper` | section、kpi-card、empty-state |
| 主标题 | `--ink` | h1-h3、value |
| 正文/描述 | `--ink-soft` | desc、subtitle |
| 主强调 | `--accent` | section-title 下划线、active tab、highlight |
| hover 边框 | `--accent-soft` | kpi-card:hover、tab:hover |
| 分类 A-L | `--accent-4` | badge-a-l |
| 分类 M-U | `--accent-2` | badge-m-u |
| 分类 V-AH | `--accent-3` | badge-v-ah |
| 分类 Q+ | `--accent` | badge-q-plus |
| 分类 Q++ | `--accent-3` / `--accent-soft` | badge-q-plusplus |

### 2.4 字体

```css
font-family: "Noto Serif SC", "Source Han Serif SC", "Songti SC", serif;
```

- 标题与正文统一使用宋体/衬线体，营造书卷气。
- 标签、徽章、数据标签使用 `JetBrains Mono` 等宽字体：`font-family: "JetBrains Mono", monospace;`。
- 字号阶梯：
  - Hero 标题：`2.2rem`
  - Section 标题：`1.3rem`
  - KPI value：`2rem`
  - 正文/描述：`0.85rem - 0.95rem`
  - 标签/徽章：`0.68rem - 0.82rem`

### 2.5 间距与圆角

| 元素 | 圆角 | 内边距 | 外边距 |
|:---|:---|:---|:---|
| Section | `8px` | `28px` | `0 0 24px 0` |
| KPI card | `8px` | `20px` | — |
| Filter tab | `20px`（pill） | `6px 14px` | — |
| Search input | `20px`（pill） | `7px 34px 7px 36px` | — |
| Category badge | `10px` | `2px 8px` | `0 0 0 8px` |
| Empty state | `8px` | `44px 24px` | — |
| Table wrapper | `6px` | — | `12px 0 0 0` |

---

## 3. 布局

### 3.1 容器

```css
.container {
    max-width: 1200px;
    margin: -30px auto 60px;
    padding: 0 24px;
    position: relative;
    z-index: 2;
}
```

- 最大宽度 1200px，居中。
- 负上边距 `-30px` 让内容区稍微叠入 hero，形成层次感。

### 3.2 KPI 网格

```css
.kpi-row {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 16px;
    margin-bottom: 32px;
}
```

- 自适应列，最小 240px。
- 与 chart-row（`minmax(280px, 1fr)`）区分。

### 3.3 Hero

```css
.hero {
    background: linear-gradient(135deg, #1a1410 0%, #3a2820 50%, #5a3828 100%);
    color: #f5e9d4;
    padding: 50px 24px 40px;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.hero::after {
    content: "";
    position: absolute;
    inset: 0;
    background: radial-gradient(circle at 70% 30%, rgba(232, 184, 133, 0.18), transparent 60%);
    pointer-events: none;
}
```

- 固定三色渐变，不可随意替换。
- `::after` 光晕层仅作装饰，`pointer-events: none` 避免遮挡点击。

---

## 4. 组件

### 4.1 Filter Tab（分类过滤标签）

```html
<div class="filter-tabs" role="group" aria-label="专题分类筛选">
    <button class="filter-tab active" data-category="all" aria-pressed="true">全部 34</button>
    <button class="filter-tab" data-category="a-l" aria-pressed="false">A-L 基础 7</button>
    <!-- ... -->
</div>
```

```css
.filter-tab {
    padding: 6px 14px;
    border: 1px solid var(--line);
    border-radius: 20px;
    background: var(--paper);
    color: var(--ink-soft);
    font-size: 0.82rem;
    cursor: pointer;
    transition: all 0.2s;
    font-family: "JetBrains Mono", monospace;
}
.filter-tab:hover { border-color: var(--accent-soft); color: var(--accent); }
.filter-tab.active { background: var(--accent); color: #fff8ec; border-color: var(--accent); }
.filter-tab:focus-visible { outline: none; box-shadow: 0 0 0 3px var(--focus-ring-accent); }
```

- 形状：pill（大圆角）。
- 状态：default / hover / active / focus-visible。
- 计数：由 JS 动态更新，格式为「标签 数量」。
- A11y：`role="group"`、`aria-label`、`aria-pressed` 必须存在。

### 4.2 Search Box（搜索框）

```html
<div class="search-box" id="search-box">
    <svg class="search-icon" ...><!-- 搜索图标 --></svg>
    <input type="search" id="topic-search" placeholder="搜索专题..." aria-controls="topic-grid" aria-label="搜索专题">
    <button class="clear-btn" id="clear-search" type="button" aria-label="清除搜索">×</button>
</div>
```

```css
.search-box input {
    padding: 7px 34px 7px 36px;
    border: 1px solid var(--line);
    border-radius: 20px;
    background: var(--paper);
    color: var(--ink);
    width: 240px;
    transition: border-color 0.2s, box-shadow 0.2s;
}
.search-box input:focus,
.search-box input:focus-visible {
    outline: none;
    border-color: var(--accent-soft);
    box-shadow: 0 0 0 3px var(--focus-ring-accent-soft);
}
.search-box .clear-btn {
    position: absolute;
    right: 6px;
    top: 50%;
    transform: translateY(-50%);
    /* 仅在输入有值时显示：.search-box.has-value .clear-btn { display: flex; } */
}
.search-box input::-webkit-search-decoration,
.search-box input::-webkit-search-cancel-button,
.search-box input::-webkit-search-results-button,
.search-box input::-webkit-search-results-decoration {
    display: none;
}
```

- 图标：左侧 SVG，颜色 `--ink-soft`，`pointer-events: none`。
- 清除按钮：右侧圆形按钮，输入有值时显示。
- Debounce：150ms，避免输入时频繁重排。
- 原生 WebKit 搜索控件必须隐藏，防止与自定义清除按钮冲突。
- A11y：`aria-controls`、`aria-label`。

### 4.3 Category Badge（分类徽章）

```html
<span class="category-badge badge-a-l">A-L</span>
```

```css
.category-badge {
    display: inline-block;
    font-size: 0.68rem;
    padding: 2px 8px;
    border-radius: 10px;
    margin-left: 8px;
    letter-spacing: 0.05em;
    font-family: "JetBrains Mono", monospace;
    vertical-align: middle;
}
.badge-a-l { background: var(--badge-a-l-bg); color: var(--accent-4); border: 1px solid var(--badge-a-l-border); }
.badge-m-u { background: var(--badge-m-u-bg); color: var(--accent-2); border: 1px solid var(--badge-m-u-border); }
.badge-v-ah { background: var(--badge-v-ah-bg); color: var(--accent-3); border: 1px solid var(--badge-v-ah-border); }
.badge-q-plus { background: var(--badge-q-plus-bg); color: var(--accent); border: 1px solid var(--badge-q-plus-border); }
.badge-q-plusplus { background: var(--badge-q-plusplus-bg); color: var(--accent-3); border: 1px solid var(--badge-q-plusplus-border); }
```

- 徽章颜色必须来自 token，禁止硬编码。
- 与 filter-tab 的分类一一对应。

### 4.4 Empty State（空状态）

```html
<div class="empty-state hidden" id="topic-empty">
    未找到与「<span class="empty-query"></span>」相关的专题。
</div>
```

```css
.empty-state {
    grid-column: 1 / -1;
    text-align: center;
    padding: 44px 24px;
    color: var(--ink-soft);
    font-size: 0.95rem;
    border: 1px dashed var(--line);
    border-radius: 8px;
    background: var(--paper);
}
.empty-state.hidden { display: none; }
.empty-state .empty-query { color: var(--accent); font-weight: 600; }
```

- 必须跨整行（`grid-column: 1 / -1`）。
- 默认隐藏，无匹配结果时显示。
- 查询词高亮使用 `--accent`。

### 4.5 KPI Card

```html
<a class="kpi-card" href="data/xxx.html">
    <div class="label">分类名 <span class="category-badge badge-a-l">A-L</span></div>
    <div class="value">38</div>
    <div class="desc">描述文字</div>
    <div class="detail">补充信息</div>
</a>
```

```css
.kpi-card {
    background: var(--paper);
    border: 1px solid var(--line);
    border-radius: 8px;
    padding: 20px;
    box-shadow: var(--shadow);
    text-decoration: none;
    color: inherit;
    display: block;
    transition: transform 0.2s, box-shadow 0.2s;
}
.kpi-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(60, 40, 20, 0.12), 0 8px 24px rgba(60, 40, 20, 0.1);
    border-color: var(--accent-soft);
}
```

- 整卡可点击，使用 `<a>` 标签保持语义。
- Hover 时轻微上浮 + 阴影加深。
- `.label` 内可放徽章，使用 flex 对齐。

### 4.6 Section

```css
.section {
    background: var(--paper);
    border: 1px solid var(--line);
    border-radius: 8px;
    padding: 28px;
    box-shadow: var(--shadow);
    margin-bottom: 24px;
}
.section-title {
    font-size: 1.3rem;
    margin-bottom: 6px;
    padding-bottom: 6px;
    border-bottom: 2px solid var(--accent);
    display: inline-block;
}
```

- Section 标题下方使用 `--accent` 2px 下划线作为视觉锚点。

### 4.7 Table Wrapper

```css
.table-wrapper {
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
    border: 1px solid var(--line);
    border-radius: 6px;
    margin-top: 12px;
}
.table-wrapper .cross-table {
    margin-top: 0;
    border: none;
    min-width: 480px;
}
.cross-table th {
    background: var(--cross-table-header-bg);
    color: var(--accent-3);
    font-weight: 600;
}
.cross-table td:first-child {
    background: var(--bg);
    font-weight: 600;
    text-align: left;
}
.cross-table .highlight {
    background: var(--cross-table-highlight-bg);
    color: var(--accent);
    font-weight: 600;
}
```

- 表格必须包裹在 `.table-wrapper` 中，确保移动端横向滚动。
- 表头使用 `--cross-table-header-bg`，高亮使用 `--cross-table-highlight-bg`。

### 4.8 Insight Box

```css
.insight-box {
    background: linear-gradient(135deg, #fff8ec 0%, #f5e9d4 100%);
    border-left: 4px solid var(--accent);
    padding: 20px 24px;
    border-radius: 4px;
    margin-top: 16px;
}
```

- 用于数据洞察/结论，左侧 4px 朱砂边框。

---

## 5. 动画与交互

### 5.1 过渡时长

| 元素 | 时长 | 缓动 |
|:---|:---|:---|
| kpi-card hover | 0.2s | ease |
| filter-tab hover/active | 0.2s | ease |
| search input focus | 0.2s | ease |
| clear-btn hover | 0.15s | ease |
| 卡片过滤进入 | 0.25s | ease |

### 5.2 卡片过滤动画

```css
.kpi-card.filter-enter {
    animation: cardFadeIn 0.25s ease;
}
@keyframes cardFadeIn {
    from { opacity: 0; transform: translateY(8px); }
    to { opacity: 1; transform: translateY(0); }
}
```

- 过滤后重新进入视口的卡片播放淡入动画。
- 隐藏卡片使用 `.hidden { display: none; }`，不参与动画。

### 5.3 动画性能

- 优先使用 `transform` 和 `opacity`，避免触发布局重排。
- 复杂动画（如 D3 force simulation、CSS keyframes）需设置 `will-change` 仅在必要元素上。

---

## 6. 响应式

### 6.1 断点

```css
@media (max-width: 768px) { /* 平板/手机 */ }
@media (max-width: 520px) { /* 窄屏手机 */ }
```

### 6.2 Dashboard 过滤栏

```css
@media (max-width: 768px) {
    .filter-bar { flex-direction: column; align-items: stretch; }
    .search-box { margin-left: 0; width: 100%; }
    .search-box input { width: 100%; }
}
```

- 768px 以下：过滤标签与搜索框垂直堆叠，搜索框占满宽度。
- 520px 以下：保持垂直堆叠，注意搜索框左侧图标与右侧清除按钮不要遮挡文字（input padding 需保留）。

### 6.3 KPI 网格

- 默认 `minmax(240px, 1fr)`，窄屏自动变为单列，无需额外媒体查询。

### 6.4 表格

- 所有表格必须包裹 `.table-wrapper`。
- 移动端通过横向滚动查看完整表格，禁止压缩列宽导致文字换行混乱。

---

## 7. 无障碍（a11y）

### 7.1 焦点

- 所有可交互元素必须有可见焦点环。
- 使用 `:focus-visible` 而非 `:focus`，避免鼠标点击时显示焦点环。
- 焦点环颜色来自 token：`--focus-ring-accent`、`--focus-ring-accent-soft`、`--focus-ring-clear`。

### 7.2 ARIA

| 元素 | 属性 |
|:---|:---|
| filter-tabs 容器 | `role="group"`、`aria-label="专题分类筛选"` |
| filter-tab | `aria-pressed="true/false"` |
| search input | `aria-controls="topic-grid"`、`aria-label="搜索专题"` |
| clear button | `aria-label="清除搜索"`、`type="button"` |
| empty state | `aria-live="polite"`（动态更新时屏幕阅读器播报） |
| div 按钮 | `role="button"`、`tabindex="0"`、Enter/Space 键盘处理 |

### 7.3 屏幕阅读器

- 徽章使用 `<span>`，不单独作为交互元素。
- 过滤结果变化时，通过 `aria-live="polite"` 告知用户当前结果数量。

### 7.4 色彩对比

- `--ink` (#2c2418) 在 `--paper` (#ffffff) 上对比度充足。
- `--accent` (#c8463a) 在 `--bg` (#faf7f2) 上用于小面积强调，避免作为大段背景。

---

## 8. 代码约定

### 8.1 F6 页面骨架（可视化页）

```text
fetchJson → loadData → main → renderXxx × N → window.__lastData cache → resize debounce 250ms → main() direct call
```

- 所有数据可视化页必须遵循此骨架，保证一致性。

### 8.2 数据回退

```javascript
function fetchJson(path, fallbackKey) {
    return fetch(path)
        .then(r => r.json())
        .catch(() => window.EMBEDDED_DATA[fallbackKey]);
}
```

- 支持 `file://` 协议直接打开，无外部 JSON 依赖。

### 8.3 XSS 预防

- 用户生成内容必须使用 D3 `.text()` 或 DOM `textContent`。
- `.html()` 仅用于开发者信任的 `EMBEDDED_DATA`。

### 8.4 空数据保护

```javascript
if (!data || data.length === 0) {
    container.append("div").text("暂无数据").attr("class", "empty-state");
    return;
}
```

---

## 9. 新增组件流程

1. **提取模式**：参考 Name That UI 等站点，提炼可复用模式。
2. **定义 token**：在 `:root` 中新增语义化 token（如 `--badge-x-bg`）。
3. **编写组件**：使用 token，遵循间距/圆角/动画规范。
4. **补充 a11y**：添加必要 ARIA 属性和 `:focus-visible`。
5. **响应式测试**：在 768px、520px、1920px 下检查布局。
6. **DRL 审查**：跑 deep review loop，确保无 P0/P1。
7. **更新 DESIGN.md**：把新组件加入本文档。
8. **同步影响面**：CHANGELOG / file-index / README / STRUCTURE / 项目说明 / project_memory。

---

## 10. 禁忌清单

- ❌ 禁止在 CSS 中直接使用裸色值（token 定义除外）。
- ❌ 禁止 filter-tab 使用 `data-count` 静态属性，计数必须由 JS 动态生成。
- ❌ 禁止搜索框显示浏览器原生清除按钮（必须用 CSS 隐藏 WebKit 搜索装饰）。
- ❌ 禁止表格直接放在 section 中而不包裹 `.table-wrapper`。
- ❌ 禁止 div 伪按钮无 `role`、`tabindex`、键盘事件。
- ❌ 禁止在 D3 `.style(name, value)` 中传函数，使用 `.each()` 模式处理条件样式。
- ❌ 禁止新增可视化页脱离 F6 骨架。

---

## 11. 相关文件

- [site/dashboard.html](site/dashboard.html) — Name That UI 组件落地实例
- [site/data/cross-time-danmaku.html](site/data/cross-time-danmaku.html) — v0.9.1 创意升级（星图/弹幕/地图）
- [CHANGELOG.md](CHANGELOG.md) — W010 / W010.1 变更记录
- [scripts/output/file-index.md](scripts/output/file-index.md) — 反向索引
- project_memory.md（Trae memory 项目级设计约定补充，路径见本地 memory 目录）
