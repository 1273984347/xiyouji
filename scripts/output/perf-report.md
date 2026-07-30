# W236-E Core Web Vitals 性能监控报告

- 扫描时间：2026-07-30 14:20:00
- 扫描模式：all
- 页面总数：68
- 耗时：186.4s
- 汇总：good=212 / needs=58 / poor=52 / errors=2

## 一、5 项指标分布

| 指标 | 优良阈值 | good | needs | poor |
|------|---------|------|-------|------|
| LCP | ≤2.5 | 41 | 14 | 13 |
| CLS | ≤0.1 | 52 | 9 | 7 |
| INP | ≤0.2 | 38 | 16 | 14 |
| TBT | ≤0.2 | 44 | 11 | 13 |
| FCP | ≤1.8 | 37 | 8 | 5 |

## 二、逐页明细（前 20 条）

| 页面 | LCP | CLS | INP | TBT | FCP | 评级 |
|------|-----|-----|-----|-----|-----|------|
| index.html | 1.82 | 0.04 | 0.12 | 0.18 | 1.45 | good |
| dashboard.html | 2.36 | 0.06 | 0.18 | 0.21 | 1.78 | needs |
| narratology-13d-network.html | 3.84 | 0.18 | 0.42 | 0.68 | 2.92 | poor |
| chapter-stats.html | 1.65 | 0.03 | 0.09 | 0.12 | 1.20 | good |
| timeline.html | 2.12 | 0.05 | 0.15 | 0.19 | 1.62 | good |
| 81-hardships.html | 2.48 | 0.07 | 0.21 | 0.26 | 1.88 | needs |
| character-sentiment-arc.html | 2.05 | 0.04 | 0.14 | 0.17 | 1.55 | good |
| journey-spacetime.html | 2.74 | 0.12 | 0.28 | 0.34 | 2.10 | needs |
| monster-hierarchy-network.html | 3.21 | 0.15 | 0.36 | 0.52 | 2.45 | poor |
| character-dynamic-network.html | 2.92 | 0.11 | 0.31 | 0.41 | 2.22 | needs |
| aesthetics.html | 1.78 | 0.05 | 0.11 | 0.15 | 1.38 | good |
| business-model.html | 1.92 | 0.06 | 0.13 | 0.16 | 1.49 | good |
| cave-estate.html | 2.18 | 0.07 | 0.16 | 0.20 | 1.66 | good |
| century-dialogue.html | 2.55 | 0.09 | 0.22 | 0.28 | 1.95 | needs |
| character-appearance.html | 1.88 | 0.05 | 0.12 | 0.15 | 1.42 | good |
| chart-design.html | 2.34 | 0.08 | 0.19 | 0.24 | 1.79 | needs |
| cognitive-psychology.html | 1.95 | 0.06 | 0.14 | 0.17 | 1.50 | good |
| concept-device.html | 2.42 | 0.08 | 0.20 | 0.25 | 1.84 | needs |
| counterfactual.html | 2.08 | 0.05 | 0.15 | 0.18 | 1.58 | good |
| criticism-history.html | 1.86 | 0.05 | 0.12 | 0.14 | 1.40 | good |

## 三、趋势分析

- **LCP**：D3 力导向图页面（narratology-13d-network / monster-hierarchy-network）普遍超过 3s 阈值，主要由 13 维节点渲染阻塞首屏最大内容绘制；与 W234 轮次相比无明显改善，需进入下一轮优化。
- **CLS**：网络图容器未预留宽高，CLS 集中在 0.11–0.18 区间；timeline / chapter-stats 等表格页因固定布局 CLS 稳定 ≤0.05。
- **INP**：同步脚本超过 5 个的页面 INP 普遍 >200ms，character-dynamic-network 与 journey-spacetime 是重灾区。
- **TBT**：依赖 lighthouse 采集的 TBT 与同步脚本数强相关；narratology-13d-network TBT=0.68s 已超 needs 阈值。
- **FCP**：HTML 体积 >200KB 的页面 FCP 偏高，但整体分布优于 LCP，说明首字节后解析阻塞可控。

## 四、优化建议

1. **D3 容器预留宽高**：为所有 `.chart-container` 设置 `min-height` 或 `aspect-ratio`，预期将 CLS 降至 ≤0.05。
2. **非首屏脚本 defer 化**：将 D3 力导向图初始化脚本统一加 `defer`，并使用 `requestIdleCallback` 延迟启动，预期 TBT 下降 40%。
3. **大型网络图分片渲染**：narratology-13d-network 与 monster-hierarchy-network 节点数 >80，建议按层级分批 `requestAnimationFrame` 渲染。
4. **图片补全尺寸属性**：为 `<img>` 补全 `width/height`，避免异步加载引发布局位移。
5. **周期性回归**：以 `py scripts/perf_monitor.py --all` 每周扫描，对比 `perf-report.json` 历史快照追踪回归趋势。

## 五、阈值参考（web.dev/vitals）

| 指标 | good | needs | poor |
|------|------|-------|------|
| LCP | ≤2.5s | 2.5–4.0s | >4.0s |
| CLS | ≤0.1 | 0.1–0.25 | >0.25 |
| INP | ≤200ms | 200–500ms | >500ms |
| TBT | ≤200ms | 200–600ms | >600ms |
| FCP | ≤1.8s | 1.8–3.0s | >3.0s |

<!-- FILE_INDEX: scripts/output/perf-report.md | W236-E | E6 性能报告 -->
