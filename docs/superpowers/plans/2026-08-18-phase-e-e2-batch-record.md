# Phase E2（W478）CN 可视化页传播 I · 批次记录

> 主方案：[2026-08-18-phase-e-visual-elevation-roadmap.md](2026-08-18-phase-e-visual-elevation-roadmap.md) §3 E2
> 范围：网络批（`grep -l 'forceSimulation'` = 20 页）+ 热力/统计批（`grep -l 'scaleBand|heatmap|histogram'` 去网络批 = 36 页）= **56 页**（派生清单于 2026-08-18 实测，比预估 16+20 多 20 页——`cross-time-danmaku/journey-geo-semiotics/perf-canvas-rendering/relationships` 等命中 forceSimulation）
> 规则：R-SHADOW / R-RADIUS / R-TRANS / R-FOCUS / R-EXEMPT（见主方案 §3）；逐页 Edit，禁全站盲正则
> 验收：批内页 M2/M3/M4 达标 · `.duration(>600)`=0 · CSP 0 漂移 · check_structure 0 · pageerror=0

## 迁移清单（页 × 迁出规则 × 豁免 N）

| 页 | 批次 | R-SHADOW | R-RADIUS | R-TRANS | R-FOCUS | 裸色→令牌 | tooltip 收编 | 豁免 N | pageerror | 状态 |
|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|
| hardship-heatmap | 热力 | 0 | 8（2/3/4/6px→sm/md） | 4（0.2s→dur-base） | 0 | 9（#fff8e7→paper-warm·#fffdf8/#fff→paper·暗金 tooltip→语义色） | ✅ 3 div→chart-tooltip + 6 classed | 3 | 0 | ✅ 试点 |
| intertextuality-network | 网络 | 1（hover 12px→elev-2） | 7（2/4/6px→sm/md·50%→pill） | 1（transform/box-shadow 0.2s→dur-base） | 0 | 4（#fff→paper·#f5efe4→paper-warm） | 无（W461 已收编） | 2 | 0 | ✅ 试点 |
| chapter-stats | 统计 | 1（kpi hover 8/24px→elev-2） | 5（2/3/4/6px→sm/md） | 0 | 0 | 6（#fff8ec/#f5e9d4→paper-warm·#23201A→ink·#f5e9d4→dark-text） | 无（W461 已收编） | 2 | 0 | ✅ 试点 |

> 备注：① 豁免 N = 页私有块内图表数据/渲染色（legend 渐变 + svg 文本光晕），已按 R-EXEMPT 在页私有 `<style>` 顶部登记；② 试点含 DESIGN §5.4 冲突处置——hardship-heatmap 的暗底金 tooltip（.heat-tip/.bar-tip）违反 §5.4 禁令，收编为 `.chart-tooltip` 宣纸底语义色；③ 试点运行时断言 = Playwright pageerror=0 + 图表形状数 > 0 + tooltip visible 切换 + 计算样式（tooltip bg=paper/radius=6px）；④ 截图目视确认并入批内 _w477_shot_check.js 扩页清单，全批完成前统一执行。

## 待办

- 剩余 53 页（网络批 19 + 热力/统计批 35）逐页迁移并登记本表。
- 全批完成后：六文档同步（CHANGELOG v2.3.81 W478 四件套 + 交接文档 + README/STRUCTURE/项目说明 + file-index）+ M5 行数对比 + 截图目视 + 提交。
