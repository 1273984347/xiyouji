# 重型 D3 力导向图 · 批量性能优化报告（中文）

日期：2026-08-06 | 场景：scene#15「日常开发」→ 站点数据可视化 | 审查：Playwright 运行时冒烟 + CDP trace 量化

## 一、改造范围（15 个文件，site/data/）

| 文件 | 说明 |
|------|------|
| character-dynamic-network.html | 角色动态关系 |
| character-semantic-network.html | 角色语义网络 |
| four-dimensional-research-network.html | 四维研究网络 |
| guanyin-six-roles-network.html | 观音六角色 |
| heaven-power-network.html | 天庭权力 |
| intertextuality-network.html | 互文网络 |
| monster-female-network.html | 妖女谱系 |
| monster-hierarchy-network.html | 妖界层级 |
| monster-victims-network.html | 妖害对象 |
| narratology-12d-network.html | 叙事学 12 维 |
| narratology-13d-network.html | 叙事学 13 维 |
| pilgrim-team-dynamic-network.html | 取经团队动态 |
| relationships.html | 人物关系（含 3 个力模拟，全改） |
| theological-intervention-network.html | 神佛干预 |
| underworld-power-network.html | 冥界权力 |

已排除：six-senses（首轮已优化）、cross-time-danmaku / journey-geo-semiotics / monster-ecology（本就用 transform）、perf-canvas-rendering（Canvas 演示页，非反模式）。

## 二、双重修复（每个文件）

1. **tick 内几何属性 → transform**：`node.attr('cx',d=>d.x).attr('cy',d=>d.y)` + `label.attr('x',...).attr('y',...)` 改为 `.attr('transform', d => \`translate(${d.x},${d.y})\`)`（保留偏移表达式如 `d.x||0`、`d.x+8`）。走 GPU 合成，免 SVG 重排/重绘。
2. **加速收敛**：`d3.forceSimulation(nodes)` 追加 `.alphaDecay(0.08).velocityDecay(0.5)`，让模拟更快停下 tick，减少每帧工作量。
3. **CSS**：注入 `svg circle { will-change: transform; }`。

## 三、运行时审查（scripts/_smoke_batch.js）

- 结果：**15/15 PASS**（无 pageerror、节点已定位、无双重定位 `doublePos=0`）。
- 偶发 `SOME FAILED` 为 headless 下 d3 CDN 加载抖动（env-noise 已含 `d3 is not defined`/`THREE is not defined`），非代码回归。隔离重跑 guanyin 得 `circles=80 d3=object err=none` 佐证。

## 四、性能实测（heaven-power，5s 收敛窗口，CDP trace 计数）

| 指标 | 旧(cx/cy, 默认衰减) | 新(transform+alphaDecay) | 变化 |
|------|--------------------|--------------------------|------|
| Layout | 306 | 90 | **↓ 71%** |
| Paint | 601 | 170 | **↓ 72%** |
| UpdateLayoutTree | 306 | 90 | **↓ 71%** |

与 six-senses（首轮）同量级，证明 `<g>`/transform + alphaDecay 组合有效。

## 五、关键结论与遗留

- **仅改节点 transform 不够**：若图的边用 `<line>` 的 `x1/y1/x2/y2` 每帧写几何属性（直线无法用 translate），Layout 不会下降；必须靠 `alphaDecay` 让模拟尽快收敛、停止 tick 才见效。节点多/边少的图收益大。
- **边层优化**（把 `<line>` 边改为 Canvas 叠加层或单 `<path>` 批量绘制）属更难问题，本轮未做，可后续评估。
- **改动未提交 git**，需你确认后 commit。
