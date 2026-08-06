# Canvas 边层性能优化报告（scene#15 重型 D3 力导向图）

> 配套：`perf_batch_report.md`（节点 transform 批改造）。两者叠加 = 完整优化。
> 目标：削减力导向图每帧主线程成本，不退化渲染（Layout 地板由 SVG 节点 transform 决定）。

## 1. 核心结论

- **边层（每 tick 的 N×4 条 `<line>` 几何写入）是 SVG 路径下最重的主线程成本**，但浏览器把「边几何写入」与「节点 transform 写入」合并进**同一 per-tick Layout**，所以**仅改边层不会降低 Layout 事件数**。
- 边层改 Canvas 的真实收益：**削减每帧 4×N 次 SVG 属性写入及其样式重算**，Paint/UpdateLayer 显著下降。
- **Layout 地板由 SVG 节点 `transform` 写入本身决定**（单图 ~89–90；多图按图数叠加），与边层实现方式无关。

## 2. 方案：Canvas 叠加边层

每个力导向图：
1. 隐藏 SVG `<line>`：`link.style('display','none')`。
2. 在 `<svg>`（或其 `<g>` 祖先）的父容器里插入一个 `position:absolute` 的 `<canvas>` 叠加层（DPR 上限 2）。
3. 每 tick 不再写 SVG 线，改为在 canvas 用 `getContext('2d')` 重绘：`moveTo(source.x,source.y)` → `lineTo(target.x,target.y)`，并读取隐藏 `<line>` 上已算好的 `stroke / stroke-width / stroke-opacity / stroke-dasharray`。
4. viewBox 缩放时按 `dpr * clientW / viewBoxW` 缩放 ctx，保证坐标对齐。

无 `d3.zoom`（全部目标文件均无）→ canvas 对齐只需取 `<svg>` 的 `offsetLeft/Top`，无需 transform 镜像。

## 3. 交付文件

### 3.1 单 SVG 文件（13 + 1 pilot，共 14）
注入脚本：`scripts/_batch_canvas_links.py`
- `heaven-power-network.html`（pilot，手动验证）
- `character-dynamic-network.html`、`character-semantic-network.html`
- `four-dimensional-research-network.html`、`guanyin-six-roles-network.html`
- `intertextuality-network.html`、`monster-female-network.html`、`monster-hierarchy-network.html`
- `monster-victims-network.html`、`narratology-12d-network.html`、`narratology-13d-network.html`
- `pilgrim-team-dynamic-network.html`、`theological-intervention-network.html`、`underworld-power-network.html`

### 3.2 多 SVG 文件（relationships.html，3 个独立力导向图）
注入脚本：`scripts/_batch_canvas_links_multi.py`
- 全局 `window.LINK_LAYERS` 注册表；每图独立 `<canvas class="link-canvas-{IDX}">` + 独立 `drawLinks_{IDX}()`，tick 只重绘自己层。
- 关键修复（本批次）：tickle 链接链正则从 `(\w+)\.attr` 放宽为 `(\w+)\s*\.attr`，兼容 `link\n    .attr('x1',…)`（链接变量与 `.attr` 分行）写法——否则反向处理时会跨图误匹配到图2。

## 4. 关键技术决策（踩坑记录）

| 问题 | 修复 |
|---|---|
| `.format()` 误读 JS 花括号 | 改用 `str.replace('{SVG}', …)` / `{IDX}` |
| `link_create_re` 只认 `'line'` | 放宽到 `*link*` 类选择器（部分图用 `.selectAll('.rel-link')`） |
| tick 链严格 `d.source.x` | 允许 `\|\| 0` 兜底（monster-victims） |
| `monster-female` 是 timeline 散点图（网格 `line` 非边） | 守卫：必须有「力边创建」+「tick 里 x1/y2 链」才注入 |
| four-dimensional TDZ（注册代码误插箭头函数体） | `find_stmt_end()` 括号深度感知定位语句结束 |
| 多图 `const X = Y.append('g')` 误把节点组当边 | 两步检测：append('g') 与紧接 `.selectAll` 间不能有 `;` |
| 多图游标重定位崩溃（文本偏移） | **逆序处理**（按 cstart 从大到小），原始坐标全程有效 |
| tick 跨图误匹配（链接变量与 `.attr` 分行） | 正则加 `\s*` 容忍换行 |

## 5. 验证（审查）

### 5.1 运行时冒烟 — `scripts/_smoke_canvas.js`（全部 PASS）
- 拦截 CDN d3 → 本地副本（`xiyouji-agent-web/node_modules/d3/dist/d3.min.js`），消除 headless 抖动。
- 断言：无 pageerror；canvas 存在且有非空像素（边真实绘制）；节点 circle 已定位；SVG 力边 `display:none`。
- 14 单 SVG + relationships（3 层）**ALL PASS**。relationships：3 canvas 全部绘制（32224 px 总计），809/833 节点定位，161/232 SVG 线隐藏（其余 71 为其他区块的网格/散点线，应保留可见）。

### 5.2 性能基准 — `scripts/_bench_canvas.js`（CDP trace）
单图（four-dimensional）：Layout=89 → 与节点 transform 基线一致（不退化）。

**relationships.html before/after（6000ms 渲染窗口）：**

| 指标 | 基线（仅 transform） | Canvas 边层 | Δ |
|---|---|---|---|
| Layout | 309 | 312 | ≈0（噪声） |
| UpdateLayoutTree | 310 | 312 | ≈0 |
| Paint | 603 | 305 | **−49%** |
| UpdateLayer | 702 | 587 | −16% |
| 总被观察事件 | 1924 | 1516 | −21% |

→ Layout 地板不变（证明边层不增布局成本），**Paint 下降约一半**（边由「N 条 SVG line 各自 paint」变为「单 canvas 一次 paint」）。

## 6. 复现命令

```bash
# 单 SVG（13 个，幂等；heaven-power 为 pilot 已含）
python scripts/_batch_canvas_links.py

# 多 SVG（relationships.html，3 图，幂等：含 LINK_LAYERS 则跳过）
python scripts/_batch_canvas_links_multi.py

# 冒烟（需先装 playwright + 系统 Chrome）
NODE_PATH=$HOME/.workbuddy/binaries/node/workspace/node_modules \
  node scripts/_smoke_canvas.js

# 基准（argv: 文件 waitMs）
NODE_PATH=$HOME/.workbuddy/binaries/node/workspace/node_modules \
  node scripts/_bench_canvas.js site/data/relationships.html 6000
```

依赖：playwright 装于托管 node workspace（`PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1`，用系统 Chrome `C:/Program Files/Google/Chrome/Application/chrome.exe`）。

## 7. 待办 / 备注
- 未提交（`git commit` 待用户确认）。
- 单图 Layout 地板 ~89–90、边层收益在 Paint/UpdateLayer，非 Layout 计数——后续若继续优化需从「节点 transform 写入」本身入手（如降低节点数 / 简化 tick 计算），而非边层。
