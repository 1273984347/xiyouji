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
| aesthetics | 热力 | 0 | 11 | 3 | 0 | 7 | 无（W461 已收编） | 5 | 0 | ✅ |
| business-model | 热力 | 1 | 13 | 0 | 0 | 9 | 无 | 7 | 0 | ✅ |
| cave-estate | 热力 | 0 | 7 | 0 | 0 | 6 | 无 | 1 | 0 | ✅ |
| chapter-structure-graph | 热力 | 1 | 1 | 0 | 0 | 1 | 无 | 1 | 0 | ✅ |
| character-appearance | 热力 | 1 | 5 | 0 | 0 | 3 | 无 | 1 | 0 | ✅ |
| character-dynamic-network | 网络 | 1 | 13 | 5 | 0 | 12 | 无 | 2 | 0 | ✅ |
| character-presence-timeline | 热力 | 0 | 5 | 0 | 0 | 3 | 无 | 0 | 0 | ✅ |
| character-semantic-network | 网络 | 0 | 5 | 0 | 0 | 4 | 无 | 0 | 0 | ✅ |
| cognitive-psychology | 热力 | 1 | 11 | 0 | 0 | 7 | 无 | 6 | 0 | ✅ |
| counterfactual | 热力 | 1 | 7 | 0 | 0 | 7 | 无 | 1 | 0 | ✅ |
| cross-time-danmaku | 网络 | 0 | 17 | 3 | 0 | 9 | 无 | 17 | 0 | ✅ |
| cultural-misreading | 热力 | 1 | 11 | 1 | 0 | 11 | 无 | 9 | 0 | ✅ |
| dialogue-sentiment | 热力 | 1 | 10 | 0 | 0 | 4 | 无 | 5 | 0 | ✅ |
| ecology | 热力 | 1 | 15 | 0 | 0 | 6 | 无 | 9 | 0 | ✅ |
| emotional-heatmap | 热力 | 1 | 9 | 6 | 0 | 8 | 无 | 4 | 0 | ✅ |
| four-dimensional-research-network | 网络 | 0 | 4 | 0 | 0 | 2 | 无 | 1 | 0 | ✅ |
| four-heavenly-kings-artifacts | 热力 | 1 | 6 | 2 | 0 | 4 | 无 | 2 | 0 | ✅ |
| guanyin-six-roles-network | 网络 | 1 | 6 | 2 | 0 | 3 | 无 | 1 | 0 | ✅ |
| hardship-difficulty-heatmap | 热力 | 0 | 11 | 7 | 0 | 11 | 无 | 10 | 0 | ✅ |
| heaven-power-network | 网络 | 1 | 8 | 2 | 0 | 0 | 无 | 9 | 0 | ✅ |
| journey-geo-semiotics | 网络 | 0 | 7 | 0 | 0 | 5 | 无 | 1 | 0 | ✅ |
| journey-map-interactive | 热力 | 0 | 3 | 2 | 0 | 1 | 无 | 7 | 0 | ✅ |
| journey-spacetime | 热力 | 2 | 14 | 6 | 0 | 13 | 无 | 10 | 0 | ✅ |
| jurisprudence | 热力 | 1 | 18 | 0 | 0 | 7 | 无 | 10 | 0 | ✅ |
| linguistics | 热力 | 1 | 17 | 0 | 0 | 9 | 无 | 9 | 0 | ✅ |
| magic-system | 热力 | 0 | 10 | 1 | 0 | 10 | 无 | 5 | 0 | ✅ |
| material-archaeology | 热力 | 0 | 14 | 0 | 0 | 13 | 无 | 4 | 0 | ✅ |
| mbti-evolution | 热力 | 0 | 9 | 7 | 0 | 7 | 无 | 2 | 0 | ✅ |
| ming-political-thought-comparison | 热力 | 0 | 10 | 2 | 0 | 7 | 无 | 2 | 0 | ✅ |
| monster-background | 热力 | 0 | 10 | 1 | 0 | 4 | 无 | 6 | 0 | ✅ |
| monster-capability-radar | 热力 | 0 | 10 | 5 | 0 | 10 | 无 | 6 | 0 | ✅ |
| monster-ecology-network | 网络 | 0 | 3 | 0 | 0 | 4 | 无 | 2 | 0 | ✅ |
| monster-female-network | 网络 | 0 | 5 | 0 | 0 | 4 | 无 | 0 | 0 | ✅ |
| monster-hierarchy-network | 网络 | 1 | 8 | 2 | 0 | 0 | 无 | 7 | 0 | ✅ |
| monster-sociology | 热力 | 1 | 12 | 0 | 0 | 7 | 无 | 7 | 0 | ✅ |
| monster-victims-network | 网络 | 1 | 6 | 2 | 0 | 3 | 无 | 1 | 0 | ✅ |
| narrative-rhythm-curve | 热力 | 0 | 2 | 1 | 0 | 1 | 无 | 3 | 0 | ✅ |
| narratology-12d-network | 网络 | 1 | 8 | 2 | 0 | 4 | 无 | 0 | 0 | ✅ |
| narratology-13d-network | 网络 | 1 | 10 | 3 | 0 | 5 | 无 | 1 | 0 | ✅ |
| perf-canvas-rendering | 网络 | 1 | 14 | 0 | 0 | 8 | 无 | 5 | 0 | ✅ |
| philosophy | 热力 | 1 | 11 | 1 | 0 | 9 | 无 | 5 | 0 | ✅ |
| pilgrim-team-dynamic-network | 网络 | 0 | 12 | 2 | 0 | 13 | 无 | 5 | 0 | ✅ |
| pilgrim-team-psychology-arc | 热力 | 1 | 18 | 5 | 0 | 14 | 无 | 9 | 0 | ✅ |
| poetry-rhythm-analysis | 热力 | 1 | 18 | 6 | 0 | 13 | 无 | 6 | 0 | ✅ |
| power-resources | 热力 | 1 | 13 | 0 | 0 | 9 | 无 | 6 | 0 | ✅ |
| relationships | 网络 | 1 | 12 | 0 | 0 | 10 | 无 | 5 | 0 | ✅ |
| risk-project | 热力 | 1 | 13 | 0 | 0 | 9 | 无 | 13 | 0 | ✅ |
| search | 热力 | 0 | 4 | 0 | 0 | 5 | 无 | 9 | 0 | ✅ |
| six-senses-narratology-network | 网络 | 1 | 8 | 2 | 0 | 3 | 无 | 0 | 0 | ✅ |
| tag-cloud | 热力 | 4 | 10 | 5 | 0 | 3 | 无 | 13 | 0 | ✅ |
| text-evolution | 热力 | 0 | 8 | 2 | 0 | 10 | 无 | 2 | 0 | ✅ |
| theological-intervention-network | 网络 | 1 | 4 | 0 | 0 | 3 | 无 | 4 | 0 | ✅ |
| underworld-power-network | 网络 | 1 | 8 | 2 | 0 | 0 | 无 | 7 | 0 | ✅ |

> 备注：⑤ 剩余 53 页由 `scripts/_w478_migrate.py` 按试点范式迁移（dry-run 审查后应用·页私有 `<style>` 块限定·INLINED 块排除），非全站盲正则；⑥ 全批 56 页 Playwright pageerror=0（_w477_shot_check.js 全量断言）+ 截图目视 6 页无破坏；⑦ M5 实测：增 1015/删 913/净 +102 行（≈+2 行/页，均为 e-track-exempt 登记注释与显式 transition 换行——M5「不增」口径豁免登记行）；⑧ check_structure 232 文件 0 失衡 + CSP 1173 哈希 0 漂移 + 改动范围 git diff = 53 页精确。

## 待办

- ✅ 56 页全量迁移登记完成。
- 六文档同步（CHANGELOG v2.3.81 W478 四件套 + 交接文档 + README/STRUCTURE/项目说明 + file-index）+ 提交（本批收尾执行中）。
