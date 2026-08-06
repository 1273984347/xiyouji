# 站点数据可视化场景 · 性能优化运行时审查报告

日期：2026-08-06 | 场景：scene#15「日常开发」→ 站点数据可视化 | 审查工具：Playwright + Chrome CDP trace

## 一、审查修复的两个问题

| # | 问题 | 性质 | 处理 |
|---|------|------|------|
| 1 | `six-senses-narratology-network.html` tick 第 1414 行 `.attr('y2', d.target.y)` 漏写 `d =>` | **我引入的回归** | 改为 `.attr('y2', d => d.target.y)`，节点恢复定位 |
| 2 | `character-relationship-3d.html` 全文件从未 `<script>` 加载 three.js（git HEAD 亦然） | **历史独立缺陷** | 补 `<script src="cdnjs.../three.js/r128/three.min.js">`（UMD 全局 THREE，与已有 d3 CDN 一致） |

## 二、运行时冒烟（scripts/_smoke_perf_review.js，ALL PASS）

- 六感官网络图：`g.node=35`、`transformOK=true`、无 pageerror
- 人物关系3D：`three=object`、`canvas=1`（此前 `three=undefined canvas=0`）
- 打工人职场黑话：`d3=object`、`svgShapes=132`、无重复 `</body>`

## 三、前后性能实测（six-senses，5s 力模拟收敛窗口，CDP trace 事件计数）

| 指标 | OLD(cx/cy 逐帧写) | NEW(g.node+transform) | 变化 |
|------|------------------|----------------------|------|
| Layout（强制重排） | 304 | 88 | **↓ 71%** |
| UpdateLayoutTree | 305 | 88 | **↓ 71%** |
| Paint（重绘） | 601 | 169 | **↓ 72%** |
| UpdateLayer（合成层更新） | 1502 | 2397 | ↑（GPU 合成，离主线程，廉价） |

结论：改用 `transform: translate()` 后，每帧不再触发 SVG 几何重排/重绘，主线程 Layout/Paint 下降约 7 成；新增的 UpdateLayer 为 GPU 合成层更新，属预期收益。

## 四、遗留与建议

- 其余 16 个重型 D3 力导向图（character-dynamic-network / guanyin-six-roles-network / character-semantic-network / narratology-12d/13d-network 等）共用同一 `cx/cy` 逐帧模式，套用本 diff 即得同等收益。**建议逐文件改 + 逐文件冒烟**，避免再次未审查落地。
- 3D 页 `setPixelRatio` 上限与 `document.hidden` 暂停为 GPU 显存/后台省电收益，难以用 trace 量化，属定性优化。
