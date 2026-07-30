# HTML 文件体积优化报告

> W230 E3 · 由 `scripts/optimize-html-size.py` 自动生成 · 不修改 HTML 源文件

- **扫描目录**：`site/data/`
- **HTML 文件数**：64
- **总体积（原始）**：6.02 MB
- **总体积（优化后预估）**：4.01 MB
- **可减少体积**：2.01 MB（33.4%）
- **大文件（>100KB）数量**：3
- **解析后端**：BeautifulSoup4

## 一、Top 10 大文件（按原始体积降序）

| # | 文件 | 原始 | 内联CSS | 内联JS | 注释 | 空白 | 优化后 | 减少 | 建议数 |
|---|------|------|---------|--------|------|------|--------|------|--------|
| 1 | `site/data/text-search.html` | 2.06 MB | 13.04 KB | 722.47 KB | 0.05 KB | 4.29 KB | 1.69 MB | 372.11 KB (18%) | 3 |
| 2 | `site/data/relationships.html` | 361.85 KB | 14.08 KB | 273.80 KB | 0.52 KB | 5.54 KB | 212.13 KB | 149.72 KB (41%) | 4 |
| 3 | `site/data/dialogue-sentiment.html` | 139.73 KB | 12.34 KB | 114.59 KB | 0.48 KB | 5.87 KB | 70.46 KB | 69.26 KB (50%) | 4 |
| 4 | `site/data/linguistics.html` | 99.56 KB | 20.69 KB | 54.18 KB | 0.11 KB | 1.81 KB | 58.69 KB | 40.87 KB (41%) | 2 |
| 5 | `site/data/monster-sociology.html` | 98.08 KB | 15.93 KB | 37.95 KB | 0.43 KB | 1.67 KB | 67.96 KB | 30.11 KB (31%) | 2 |
| 6 | `site/data/material-archaeology.html` | 96.42 KB | 16.11 KB | 59.22 KB | 0.47 KB | 1.80 KB | 55.44 KB | 40.99 KB (43%) | 2 |
| 7 | `site/data/ecology.html` | 95.32 KB | 18.69 KB | 55.72 KB | 0.72 KB | 1.94 KB | 54.21 KB | 41.11 KB (43%) | 2 |
| 8 | `site/data/jurisprudence.html` | 92.70 KB | 18.76 KB | 50.89 KB | 0.46 KB | 1.70 KB | 54.38 KB | 38.32 KB (41%) | 2 |
| 9 | `site/data/karma-reincarnation.html` | 92.47 KB | 15.26 KB | 42.12 KB | 0.41 KB | 1.68 KB | 60.68 KB | 31.78 KB (34%) | 2 |
| 10 | `site/data/game-webnovel.html` | 91.21 KB | 21.79 KB | 53.96 KB | 0.20 KB | 2.03 KB | 49.55 KB | 41.66 KB (46%) | 2 |

## 二、全量文件明细

| 文件 | 原始 | 优化后预估 | 优化比例 | 内联CSS | 内联JS | 注释 | 空白 | 外链JS | 外链CSS | img/lazy | iframe/lazy |
|------|------|-----------|----------|---------|--------|------|------|--------|---------|----------|-------------|
| `site/data/text-search.html` | 2.06 MB | 1.69 MB | 17.7% | 13.04 KB | 722.47 KB | 0.05 KB | 4.29 KB | 0 | 0 | 0/0 | 0/0 |
| `site/data/relationships.html` | 361.85 KB | 212.13 KB | 41.4% | 14.08 KB | 273.80 KB | 0.52 KB | 5.54 KB | 1 | 0 | 0/0 | 0/0 |
| `site/data/dialogue-sentiment.html` | 139.73 KB | 70.46 KB | 49.6% | 12.34 KB | 114.59 KB | 0.48 KB | 5.87 KB | 1 | 0 | 0/0 | 0/0 |
| `site/data/linguistics.html` | 99.56 KB | 58.69 KB | 41.1% | 20.69 KB | 54.18 KB | 0.11 KB | 1.81 KB | 1 | 0 | 0/0 | 0/0 |
| `site/data/monster-sociology.html` | 98.08 KB | 67.96 KB | 30.7% | 15.93 KB | 37.95 KB | 0.43 KB | 1.67 KB | 1 | 0 | 0/0 | 0/0 |
| `site/data/material-archaeology.html` | 96.42 KB | 55.44 KB | 42.5% | 16.11 KB | 59.22 KB | 0.47 KB | 1.80 KB | 1 | 0 | 0/0 | 0/0 |
| `site/data/ecology.html` | 95.32 KB | 54.21 KB | 43.1% | 18.69 KB | 55.72 KB | 0.72 KB | 1.94 KB | 1 | 0 | 0/0 | 0/0 |
| `site/data/jurisprudence.html` | 92.70 KB | 54.38 KB | 41.3% | 18.76 KB | 50.89 KB | 0.46 KB | 1.70 KB | 1 | 0 | 0/0 | 0/0 |
| `site/data/karma-reincarnation.html` | 92.47 KB | 60.68 KB | 34.4% | 15.26 KB | 42.12 KB | 0.41 KB | 1.68 KB | 1 | 0 | 0/0 | 0/0 |
| `site/data/game-webnovel.html` | 91.21 KB | 49.55 KB | 45.7% | 21.79 KB | 53.96 KB | 0.20 KB | 2.03 KB | 1 | 0 | 0/0 | 0/0 |
| `site/data/risk-project.html` | 89.87 KB | 58.04 KB | 35.4% | 16.67 KB | 40.38 KB | 0.40 KB | 1.80 KB | 1 | 0 | 0/0 | 0/0 |
| `site/data/business-model.html` | 88.88 KB | 57.40 KB | 35.4% | 16.04 KB | 40.46 KB | 0.42 KB | 1.75 KB | 1 | 0 | 0/0 | 0/0 |
| `site/data/power-resources.html` | 87.84 KB | 57.14 KB | 35.0% | 15.13 KB | 40.02 KB | 0.40 KB | 1.77 KB | 1 | 0 | 0/0 | 0/0 |
| `site/data/philosophy.html` | 84.61 KB | 61.03 KB | 27.9% | 13.73 KB | 27.56 KB | 0.47 KB | 1.58 KB | 1 | 0 | 0/0 | 0/0 |
| `site/data/narrative-experiment.html` | 81.53 KB | 45.76 KB | 43.9% | 24.92 KB | 38.61 KB | 0.20 KB | 1.89 KB | 1 | 0 | 0/0 | 0/0 |
| `site/data/cognitive-psychology.html` | 79.92 KB | 52.53 KB | 34.3% | 14.59 KB | 34.28 KB | 0.42 KB | 1.56 KB | 1 | 0 | 0/0 | 0/0 |
| `site/data/methodology-matrix.html` | 79.76 KB | 43.86 KB | 45.0% | 21.31 KB | 43.55 KB | 0.10 KB | 1.79 KB | 1 | 0 | 0/0 | 0/0 |
| `site/data/chart-design.html` | 79.75 KB | 42.97 KB | 46.1% | 20.44 KB | 46.23 KB | 0.14 KB | 1.80 KB | 1 | 0 | 0/0 | 0/0 |
| `site/data/emotional-heatmap.html` | 77.92 KB | 44.67 KB | 42.7% | 15.33 KB | 45.49 KB | 0.09 KB | 1.74 KB | 1 | 0 | 0/0 | 0/0 |
| `site/data/ethics-consumption.html` | 75.83 KB | 40.95 KB | 46.0% | 24.14 KB | 38.23 KB | 0.12 KB | 1.66 KB | 1 | 0 | 0/0 | 0/0 |
| `site/data/visual-art.html` | 75.82 KB | 41.33 KB | 45.5% | 22.80 KB | 39.10 KB | 0.09 KB | 1.69 KB | 1 | 0 | 0/0 | 0/0 |
| `site/data/narratology-13d-network.html` | 72.38 KB | 43.32 KB | 40.1% | 9.47 KB | 44.45 KB | 0.23 KB | 1.33 KB | 2 | 0 | 0/0 | 0/0 |
| `site/data/criticism-history.html` | 67.68 KB | 37.99 KB | 43.9% | 16.90 KB | 36.60 KB | 0.14 KB | 1.60 KB | 1 | 0 | 0/0 | 0/0 |
| `site/data/heaven-power-network.html` | 67.52 KB | 40.39 KB | 40.2% | 9.48 KB | 40.26 KB | 0.25 KB | 1.55 KB | 2 | 0 | 0/0 | 0/0 |
| `site/data/concept-device.html` | 65.84 KB | 35.62 KB | 45.9% | 27.27 KB | 25.41 KB | 0.13 KB | 1.48 KB | 1 | 0 | 0/0 | 0/0 |
| `site/data/intertextuality-network.html` | 63.94 KB | 37.03 KB | 42.1% | 8.17 KB | 41.78 KB | 0.15 KB | 1.39 KB | 2 | 0 | 0/0 | 0/0 |
| `site/data/underworld-power-network.html` | 63.14 KB | 37.52 KB | 40.6% | 8.87 KB | 38.13 KB | 0.23 KB | 1.45 KB | 2 | 0 | 0/0 | 0/0 |
| `site/data/monster-hierarchy-network.html` | 62.34 KB | 36.47 KB | 41.5% | 7.95 KB | 38.98 KB | 0.63 KB | 1.46 KB | 2 | 0 | 0/0 | 0/0 |
| `site/data/narratology-12d-network.html` | 62.23 KB | 36.90 KB | 40.7% | 8.19 KB | 38.74 KB | 0.22 KB | 1.21 KB | 2 | 0 | 0/0 | 0/0 |
| `site/data/text-evolution.html` | 59.73 KB | 32.80 KB | 45.1% | 15.90 KB | 32.57 KB | 0.13 KB | 1.40 KB | 1 | 0 | 0/0 | 0/0 |
| `site/data/magic-system.html` | 58.12 KB | 34.45 KB | 40.7% | 12.50 KB | 30.21 KB | 0.15 KB | 1.31 KB | 2 | 0 | 0/0 | 0/0 |
| `site/data/monster-female-network.html` | 57.67 KB | 34.84 KB | 39.6% | 6.36 KB | 35.90 KB | 0.27 KB | 1.15 KB | 2 | 0 | 0/0 | 0/0 |
| `site/data/workplace.html` | 56.86 KB | 32.10 KB | 43.6% | 15.12 KB | 29.32 KB | 0.14 KB | 1.29 KB | 1 | 0 | 0/0 | 0/0 |
| `site/data/social-media.html` | 56.40 KB | 30.81 KB | 45.4% | 16.09 KB | 29.74 KB | 0.12 KB | 1.36 KB | 1 | 0 | 0/0 | 0/0 |
| `site/data/music-structure.html` | 55.31 KB | 30.79 KB | 44.3% | 12.81 KB | 31.90 KB | 0.13 KB | 1.08 KB | 1 | 0 | 0/0 | 0/0 |
| `site/data/deconstruction.html` | 54.84 KB | 30.20 KB | 44.9% | 13.35 KB | 31.20 KB | 0.11 KB | 1.32 KB | 1 | 0 | 0/0 | 0/0 |
| `site/data/six-senses-narratology-network.html` | 54.56 KB | 30.95 KB | 43.3% | 7.83 KB | 35.91 KB | 0.13 KB | 1.17 KB | 2 | 0 | 0/0 | 0/0 |
| `site/data/guanyin-six-roles-network.html` | 52.55 KB | 30.86 KB | 41.3% | 5.28 KB | 35.16 KB | 0.14 KB | 1.16 KB | 2 | 0 | 0/0 | 0/0 |
| `site/data/cave-estate.html` | 51.26 KB | 29.60 KB | 42.3% | 9.79 KB | 29.86 KB | 0.11 KB | 1.08 KB | 1 | 0 | 0/0 | 0/0 |
| `site/data/aesthetics.html` | 49.55 KB | 27.12 KB | 45.3% | 14.36 KB | 25.77 KB | 0.13 KB | 1.15 KB | 1 | 0 | 0/0 | 0/0 |
| `site/data/monster-victims-network.html` | 48.74 KB | 29.37 KB | 39.7% | 5.28 KB | 30.70 KB | 0.14 KB | 1.04 KB | 2 | 0 | 0/0 | 0/0 |
| `site/data/cultural-misreading.html` | 48.51 KB | 26.75 KB | 44.9% | 13.95 KB | 24.83 KB | 0.13 KB | 1.21 KB | 1 | 0 | 0/0 | 0/0 |
| `site/data/monster-background.html` | 44.93 KB | 26.05 KB | 42.0% | 11.67 KB | 22.34 KB | 0.00 KB | 1.02 KB | 1 | 0 | 0/0 | 0/0 |
| `site/data/hardship-difficulty-heatmap.html` | 44.49 KB | 26.32 KB | 40.8% | 7.29 KB | 26.56 KB | 0.09 KB | 0.62 KB | 1 | 0 | 0/0 | 0/0 |
| `site/data/ai-dialogue.html` | 44.37 KB | 25.47 KB | 42.6% | 12.79 KB | 21.13 KB | 0.00 KB | 0.94 KB | 1 | 0 | 0/0 | 0/0 |
| `site/data/hardship-heatmap.html` | 44.23 KB | 26.49 KB | 40.1% | 7.50 KB | 25.29 KB | 0.11 KB | 0.70 KB | 1 | 0 | 0/0 | 0/0 |
| `site/data/cross-time-danmaku.html` | 43.75 KB | 24.19 KB | 44.7% | 13.60 KB | 21.57 KB | 0.05 KB | 0.82 KB | 1 | 0 | 0/0 | 0/0 |
| `site/data/timeline.html` | 41.46 KB | 21.37 KB | 48.5% | 13.98 KB | 21.88 KB | 0.06 KB | 1.00 KB | 1 | 0 | 0/0 | 0/0 |
| `site/data/character-sentiment-arc.html` | 40.63 KB | 25.02 KB | 38.4% | 7.61 KB | 20.91 KB | 0.00 KB | 0.83 KB | 1 | 0 | 0/0 | 0/0 |
| `site/data/global-pattern.html` | 40.28 KB | 22.93 KB | 43.1% | 11.92 KB | 18.81 KB | 0.12 KB | 0.98 KB | 1 | 0 | 0/0 | 0/0 |
| `site/data/journey-route.html` | 39.88 KB | 21.87 KB | 45.1% | 10.40 KB | 21.91 KB | 0.07 KB | 1.06 KB | 1 | 0 | 0/0 | 0/0 |
| `site/data/journey-spacetime.html` | 38.93 KB | 24.29 KB | 37.6% | 8.49 KB | 17.94 KB | 0.08 KB | 0.73 KB | 1 | 0 | 0/0 | 0/0 |
| `site/data/character-appearance.html` | 37.46 KB | 19.23 KB | 48.7% | 8.67 KB | 24.47 KB | 0.10 KB | 1.00 KB | 1 | 0 | 0/0 | 0/0 |
| `site/data/counterfactual.html` | 37.30 KB | 21.02 KB | 43.6% | 11.50 KB | 17.28 KB | 0.10 KB | 0.94 KB | 1 | 0 | 0/0 | 0/0 |
| `site/data/four-heavenly-kings-artifacts.html` | 37.06 KB | 21.85 KB | 41.0% | 5.70 KB | 22.12 KB | 0.14 KB | 0.86 KB | 1 | 0 | 0/0 | 0/0 |
| `site/data/mbti-evolution.html` | 36.72 KB | 20.04 KB | 45.4% | 7.35 KB | 23.38 KB | 0.11 KB | 0.69 KB | 1 | 0 | 0/0 | 0/0 |
| `site/data/81-hardships.html` | 34.27 KB | 19.10 KB | 44.3% | 12.29 KB | 14.10 KB | 0.08 KB | 0.96 KB | 2 | 0 | 0/0 | 0/0 |
| `site/data/chapter-stats.html` | 27.07 KB | 14.24 KB | 47.4% | 7.36 KB | 15.64 KB | 0.08 KB | 0.75 KB | 1 | 0 | 0/0 | 0/0 |
| `site/data/journey-geo-semiotics.html` | 26.21 KB | 13.88 KB | 47.0% | 9.98 KB | 11.45 KB | 0.16 KB | 0.66 KB | 1 | 0 | 0/0 | 0/0 |
| `site/data/perf-canvas-rendering.html` | 25.72 KB | 16.59 KB | 35.5% | 7.79 KB | 7.99 KB | 0.05 KB | 0.58 KB | 1 | 0 | 0/0 | 0/0 |
| `site/data/character-semantic-network.html` | 22.97 KB | 15.37 KB | 33.1% | 2.96 KB | 11.30 KB | 0.00 KB | 0.25 KB | 1 | 0 | 0/0 | 0/0 |
| `site/data/character-presence-timeline.html` | 19.87 KB | 12.85 KB | 35.3% | 2.09 KB | 11.16 KB | 0.00 KB | 0.27 KB | 1 | 0 | 0/0 | 0/0 |
| `site/data/famous-time-travel.html` | 16.03 KB | 10.22 KB | 36.2% | 5.76 KB | 4.23 KB | 0.04 KB | 0.29 KB | 1 | 0 | 0/0 | 0/0 |
| `site/data/century-dialogue.html` | 14.23 KB | 7.62 KB | 46.4% | 6.21 KB | 5.36 KB | 0.00 KB | 0.29 KB | 1 | 0 | 0/0 | 0/0 |

## 三、大文件（>100KB）优化建议

### `site/data/text-search.html` — 2.06 MB → 预估 1.69 MB（减少 17.7%）

- ⚠️ 大文件（2104.7KB > 100KB 阈值），优先优化
- 内联 CSS 较大（13.0KB）：建议提取到 site/static/css/<page>.css 外部文件，多页共享时合并为 common.css，浏览器可缓存
- 内联 JS 较大（722.5KB）：建议提取到 site/static/js/<page>.js，配合 defer 异步加载

### `site/data/relationships.html` — 361.85 KB → 预估 212.13 KB（减少 41.4%）

- ⚠️ 大文件（361.9KB > 100KB 阈值），优先优化
- 内联 CSS 较大（14.1KB）：建议提取到 site/static/css/<page>.css 外部文件，多页共享时合并为 common.css，浏览器可缓存
- 内联 JS 较大（273.8KB）：建议提取到 site/static/js/<page>.js，配合 defer 异步加载
- 冗余空白较多（5.5KB）：可启用 HTML minify（如 html-minifier-terser）压缩空白

### `site/data/dialogue-sentiment.html` — 139.73 KB → 预估 70.46 KB（减少 49.6%）

- ⚠️ 大文件（139.7KB > 100KB 阈值），优先优化
- 内联 CSS 较大（12.3KB）：建议提取到 site/static/css/<page>.css 外部文件，多页共享时合并为 common.css，浏览器可缓存
- 内联 JS 较大（114.6KB）：建议提取到 site/static/js/<page>.js，配合 defer 异步加载
- 冗余空白较多（5.9KB）：可启用 HTML minify（如 html-minifier-terser）压缩空白

## 四、通用优化策略

### 4.1 内联 CSS 提取到外部文件
- 多页共享的样式（如 `.section` / `.kpi-card` / `.chart-block`）合并为 `site/static/css/common.css`，浏览器跨页面缓存
- 页面专属样式保留在 `<style>` 或单独 `site/static/css/<page>.css`
- 工具：`purgecss` 可剔除未使用的 CSS 规则

### 4.2 内联 JS 提取到外部文件
- 大块 D3.js 渲染逻辑提取到 `site/static/js/<page>.js`，配合 `<script defer>` 异步加载
- 共享的常量（如 `NAME_POOL` / `COLOR_BY_GROUP`）抽取到 `site/static/js/common.js`
- 第三方库（D3.js v7）改为 CDN 引用 + SRI 完整性校验

### 4.3 删除 HTML 注释
- 生产构建时通过 `html-minifier-terser` 删除所有非条件注释
- 保留 `<!--[if IE]>` 等条件注释
- 保留 `<!-- noscript -->` 等功能性注释

### 4.4 压缩空白
- 启用 HTML minify（连续空格 → 单空格、移除行尾空白、移除空行）
- 保守压缩：保留 `<pre>` / `<textarea>` 内的空白
- 工具链：`html-minifier-terser` 或 Vite `vite-plugin-html-minify`

### 4.5 懒加载非关键资源
- `<img loading="lazy">`：首屏外图片延迟加载
- `<iframe loading="lazy">`：嵌入页面延迟加载
- `<link rel="preload">` 仅用于关键字体 / 关键 CSS
- `<script defer>` 或 `<script type="module">`：非关键 JS 异步化

### 4.6 进一步压缩（gzip / brotli）
- Web 服务器启用 gzip（一般可达 70% 压缩）或 brotli（可达 80%+ 压缩）
- HTML 文本压缩率高于二进制资源，优先确保 text/html 启用压缩
- 配合 CDN 边缘缓存，命中后零字节传输

## 五、脚本运行说明

```bash
# 进入项目根
cd d:/1/xiyouji

# 运行脚本（标准库即可，无需额外依赖）
python scripts/optimize-html-size.py

# 可选：安装 beautifulsoup4 获得更精准的解析
pip install beautifulsoup4
```

- **输出位置**：`scripts/output/html-size-report.md`
- **运行模式**：只读扫描，不修改 HTML 文件
- **建议频率**：每次新增可视化页面后运行一次
