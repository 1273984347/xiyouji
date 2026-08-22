# Phase E4（W491）EN 站同步 · 批次记录

> 主方案：[2026-08-18-phase-e-visual-elevation-roadmap.md](2026-08-18-phase-e-visual-elevation-roadmap.md) §3 E4
> 范围：EN 85 同名可视化页（CN data 86 减 journey-geo-3d，git 同名派生）；EN 根页（index/guide/dashboard 等）非可视化页不在此批（随 E5 根页口径处理）
> 规则：复用 _w490_migrate.py 六规则（改 DATA 路径 site/en/）；tokens/system 同源（W489 已传播 INLINED 块），本批只迁移页私有 <style>

## 迁移清单（页 × 规则 × 豁免 N）

| 页 | R-SHADOW | R-RADIUS | R-TRANS | R-FOCUS | 裸色→令牌 | 豁免 N |
|:---|:---|:---|:---|:---|:---|:---|
| 页 | R-SHADOW | R-RADIUS | R-TRANS | R-FOCUS | 裸色→令牌 | 豁免 N |
|:---|:---|:---|:---|:---|:---|:---|
| 81-hardships-view.html | 0 | 3 | 0 | 0 | 0 | 9 |
| 81-hardships.html | 0 | 9 | 0 | 0 | 0 | 2 |
| aesthetics.html | 0 | 12 | 0 | 0 | 0 | 7 |
| ai-dialogue.html | 0 | 14 | 0 | 0 | 0 | 1 |
| business-model.html | 0 | 13 | 0 | 0 | 0 | 7 |
| cave-estate.html | 0 | 7 | 0 | 0 | 0 | 1 |
| century-dialogue.html | 0 | 8 | 0 | 0 | 0 | 2 |
| chapter-stats.html | 0 | 5 | 0 | 0 | 0 | 1 |
| chapter-structure-graph.html | 0 | 2 | 0 | 0 | 0 | 2 |
| character-appearance.html | 0 | 6 | 0 | 0 | 0 | 2 |
| character-dynamic-network.html | 0 | 13 | 0 | 0 | 0 | 5 |
| character-presence-timeline.html | 0 | 5 | 0 | 0 | 0 | 0 |
| character-relationship-3d-view.html | 0 | 3 | 0 | 0 | 0 | 9 |
| character-relationship-3d.html | 0 | 4 | 0 | 0 | 0 | 11 |
| character-semantic-network.html | 0 | 6 | 0 | 0 | 0 | 1 |
| character-sentiment-arc.html | 0 | 6 | 0 | 0 | 0 | 3 |
| chart-design.html | 0 | 19 | 0 | 0 | 0 | 8 |
| cognitive-psychology.html | 0 | 11 | 0 | 0 | 0 | 6 |
| concept-device.html | 0 | 28 | 0 | 0 | 0 | 52 |
| counterfactual.html | 0 | 7 | 0 | 0 | 0 | 1 |
| criticism-history.html | 0 | 10 | 0 | 0 | 0 | 5 |
| cross-time-danmaku.html | 0 | 17 | 0 | 0 | 0 | 17 |
| cultural-misreading.html | 0 | 12 | 0 | 0 | 0 | 10 |
| customs-pass-route.html | 0 | 2 | 0 | 0 | 0 | 0 |
| data-explorer.html | 0 | 5 | 0 | 0 | 0 | 11 |
| deconstruction.html | 0 | 9 | 0 | 0 | 0 | 6 |
| dialogue-sentiment.html | 0 | 10 | 0 | 0 | 0 | 5 |
| ecology.html | 0 | 14 | 0 | 0 | 0 | 9 |
| emotional-heatmap.html | 0 | 11 | 0 | 0 | 0 | 7 |
| ethics-consumption.html | 0 | 27 | 0 | 0 | 0 | 9 |
| famous-time-travel.html | 0 | 7 | 0 | 0 | 0 | 2 |
| four-dimensional-research-network.html | 0 | 4 | 0 | 0 | 0 | 1 |
| four-heavenly-kings-artifacts.html | 0 | 7 | 0 | 0 | 0 | 3 |
| game-webnovel.html | 0 | 21 | 0 | 0 | 0 | 9 |
| global-pattern.html | 0 | 8 | 0 | 0 | 0 | 5 |
| graph-explorer.html | 0 | 12 | 0 | 0 | 0 | 23 |
| guanyin-six-roles-network.html | 0 | 7 | 0 | 0 | 0 | 2 |
| hardship-difficulty-heatmap.html | 0 | 9 | 0 | 0 | 0 | 4 |
| hardship-heatmap.html | 0 | 9 | 0 | 0 | 0 | 7 |
| heaven-power-network.html | 0 | 9 | 0 | 0 | 0 | 10 |
| intertextuality-network.html | 0 | 9 | 0 | 0 | 0 | 0 |
| journey-geo-semiotics.html | 0 | 8 | 0 | 0 | 0 | 1 |
| journey-map-interactive.html | 0 | 4 | 0 | 0 | 0 | 8 |
| journey-route.html | 0 | 7 | 0 | 0 | 0 | 1 |
| journey-spacetime.html | 0 | 13 | 0 | 0 | 0 | 5 |
| jurisprudence.html | 0 | 17 | 0 | 0 | 0 | 10 |
| karma-reincarnation.html | 0 | 11 | 0 | 0 | 0 | 7 |
| language-style-radar.html | 0 | 2 | 0 | 0 | 0 | 2 |
| linguistics.html | 0 | 17 | 0 | 0 | 0 | 9 |
| magic-system.html | 0 | 10 | 0 | 0 | 0 | 5 |
| material-archaeology.html | 0 | 15 | 0 | 0 | 0 | 5 |
| mbti-evolution.html | 0 | 9 | 0 | 0 | 0 | 2 |
| methodology-matrix.html | 0 | 18 | 0 | 0 | 0 | 15 |
| ming-political-thought-comparison.html | 0 | 10 | 0 | 0 | 0 | 6 |
| monster-background.html | 0 | 11 | 0 | 0 | 0 | 7 |
| monster-capability-radar.html | 0 | 10 | 0 | 0 | 0 | 6 |
| monster-ecology-network.html | 0 | 3 | 0 | 0 | 0 | 2 |
| monster-female-network.html | 0 | 6 | 0 | 0 | 0 | 0 |
| monster-hierarchy-network.html | 0 | 9 | 0 | 0 | 0 | 8 |
| monster-sociology.html | 0 | 12 | 0 | 0 | 0 | 7 |
| monster-victims-network.html | 0 | 7 | 0 | 0 | 0 | 2 |
| music-structure.html | 0 | 12 | 0 | 0 | 0 | 5 |
| narrative-experiment.html | 0 | 28 | 0 | 0 | 0 | 8 |
| narrative-rhythm-curve.html | 0 | 3 | 0 | 0 | 0 | 4 |
| narratology-12d-network.html | 0 | 9 | 0 | 0 | 0 | 0 |
| narratology-13d-network.html | 0 | 11 | 0 | 0 | 0 | 1 |
| perf-canvas-rendering.html | 0 | 14 | 0 | 0 | 0 | 5 |
| philosophy.html | 0 | 11 | 0 | 0 | 0 | 5 |
| pilgrim-team-dynamic-network.html | 0 | 13 | 0 | 0 | 0 | 5 |
| pilgrim-team-psychology-arc.html | 0 | 17 | 0 | 0 | 0 | 9 |
| poetry-rhythm-analysis.html | 0 | 17 | 0 | 0 | 0 | 6 |
| power-resources.html | 0 | 12 | 0 | 0 | 0 | 6 |
| relationships.html | 0 | 12 | 0 | 0 | 0 | 5 |
| risk-project.html | 0 | 13 | 0 | 0 | 0 | 13 |
| search.html | 0 | 4 | 0 | 0 | 0 | 9 |
| six-senses-narratology-network.html | 0 | 9 | 0 | 0 | 0 | 0 |
| social-media.html | 0 | 15 | 0 | 0 | 0 | 9 |
| tag-cloud.html | 0 | 10 | 0 | 0 | 0 | 13 |
| text-evolution.html | 0 | 8 | 0 | 0 | 0 | 2 |
| text-search.html | 0 | 12 | 0 | 0 | 0 | 1 |
| theological-intervention-network.html | 0 | 4 | 0 | 0 | 0 | 4 |
| timeline.html | 0 | 13 | 0 | 0 | 0 | 1 |
| underworld-power-network.html | 0 | 9 | 0 | 0 | 0 | 8 |
| visual-art.html | 0 | 22 | 0 | 0 | 0 | 9 |
| workplace.html | 0 | 14 | 0 | 0 | 0 | 3 |
