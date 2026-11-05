# dataset/ — 详解西游记结构化数据

> 从 site/data/*.html 的 EMBEDDED_DATA 中提取的结构化数据集。
> 提取时间：2026-08-02
> 提取脚本：scripts/extract_datasets.js

## 概览

- 提取页面：40 / 80
- 跳过页面：40（无 EMBEDDED_DATA 或解析失败）
- 格式：JSON（UTF-8，2 空格缩进）

## 数据索引

| 文件 | 数据键数 | 大小 | 主要键 |
|------|---------|------|--------|
| 81-hardships.json | 7 | 5.1 KB | total, by_cause, by_ending, by_difficulty, cross_cause_ending, hardships（81 条逐难明细：index/name/chapter/cause/ending/difficulty，源自 scripts/C_情节/hardships_81.py） |
| ai-dialogue.json | 3 | 12.7 KB | celebrities, journey_quotes, quick_topics |
| cave-estate.json | 4 | 12.2 KB | caves, by_owner_rank, by_region, top_luxury |
| century-dialogue.json | 2 | 1.5 KB | triangle_dialogue, roundtable_topics |
| chapter-structure-graph.json | 5 | 4.1 KB | meta, kpi, cluster, heatmap, wordCount |
| character-relationship-3d.json | 4 | 4.1 KB | meta, kpi, nodes（22，含阵营/回目/证据）, links（32，含规则/理由/权重） |
| concept-device.json | 9 | 10.1 KB | nav, prism, radio, mobius, cipher |
| criticism-history.json | 7 | 8.9 KB | summary, streams, critics, triangle, candidates |
| cross-time-danmaku.json | 6 | 9.6 KB | celebrity_profiles, age_groups, mouthpiece_quotes, modern_commentary, international_critics |
| dashboard.json | 2 | 4.2 KB | meta, kpi |
| edge-wukong-tangseng.json | 6 | 10.7 KB | meta, edge, events（9 组逐回事件）, aggregate（max/mean/count 敏感性）, disputed_points, quote_policy |
| emotional-heatmap.json | 4 | 26.7 KB | meta, scholars, hardships, reactions |
| famous-time-travel.json | 2 | 1.7 KB | travel_identities, scene_illustrations |
| four-dimensional-research-network.json | 8 | 7.3 KB | meta, dimensions, indicators, radar, theorists |
| four-heavenly-kings-artifacts.json | 4 | 3.7 KB | kings, radar, chord, timeline |
| guanyin-six-roles-network.json | 6 | 9.8 KB | roles, network, sankey, radar, timeline |
| heaven-power-network.json | 6 | 9.8 KB | hierarchy, network, sankey, radar, timeline |
| intertextuality-network.json | 1 | 8.8 KB | intertextuality |
| journey-geo-semiotics.json | 2 | 1.3 KB | nodes, links |
| journey-map-interactive.json | 3 | 4.6 KB | meta, kpi, nodes |
| language-style-radar.json | 5 | 1.5 KB | meta, kpi, dimensions, characters, pca |
| magic-system.json | 5 | 12.1 KB | magic_system, magic_fire, magic_energy_sankey, magic_arrays, magic_treasures |
| material-archaeology.json | 4 | 19.4 KB | artifact_materials, costume_archaeology, cave_architecture, summary |
| ming-political-thought-comparison.json | 7 | 3.5 KB | meta, kpi, radar, heatmap, timeline |
| monster-capability-radar.json | 7 | 3.6 KB | meta, kpi, radar, bar, scatter |
| monster-ecology-network.json | 6 | 11.0 KB | meta, kpi, network, sankey, radar |
| monster-female-network.json | 1 | 10.6 KB | monsterFemale |
| monster-hierarchy-network.json | 6 | 9.8 KB | tiers, network, sankey, radar, timeline |
| monster-victims-network.json | 5 | 7.7 KB | victims, network, sankey, radar, timeline |
| music-structure.json | 5 | 14.2 KB | summary, sounds, rhythm, symmetry, movement |
| narratology-12d-network.json | 1 | 13.9 KB | narratology |
| narratology-13d-network.json | 1 | 18.8 KB | narratology |
| pilgrim-team-dynamic-network.json | 5 | 4.3 KB | meta, kpi, belbin, network, phases |
| pilgrim-team-psychology-arc.json | 7 | 3.0 KB | meta, kpi, radar, psychology_arc, cohesion_heatmap |
| poetry-rhythm-analysis.json | 7 | 2.4 KB | meta, kpi, pie, heatmap, timeline |
| six-senses-narratology-network.json | 1 | 9.3 KB | sixSenses |
| text-evolution.json | 5 | 9.6 KB | summary, versions, variants, authors, commentators |
| text-search.json | 3 | 2070.5 KB | chapters, characters, artifacts |
| theological-intervention-network.json | 5 | 5.9 KB | meta, network, sankey, radar, timeline |
| timeline.json | 1 | 4.3 KB | timeline |
| underworld-power-network.json | 6 | 8.6 KB | hierarchy, network, sankey, radar, timeline |

## 编码与溯源

- [CODING.md](CODING.md)：人物关系编码手册（关系类型、权重、证据级别、边界案例与争议处理）。
- `character-relationship-3d.json`：节点补阵营、登场回目与证据级别；边补关系规则、来源回目、判定理由、权重与争议标记。
- `edge-wukong-tangseng.json`：唐僧—孙悟空单边示范档案（9 组逐回事件、引文探针结果、max/mean/count 权重敏感性、3 条争议点）。
- 校验：第 61 门禁 `python scripts/check_dataset_provenance.py`（字段完整性、引用闭合、回目与权重范围、重复边）；`verify_delivery.py` 全量提交前自动执行。

> 该网络为示意性人工整理网络，不做统计推断；与调用 `character_nlp.py` 生成的 35 节点 / 329 边共现网络不是同一口径。

## 使用方式

```python
import json
with open('dataset/81-hardships.json', encoding='utf-8') as f:
    data = json.load(f)
print(data['hardships'])  # 八十一难完整数据
```

```javascript
const data = await fetch('dataset/philosophy.json').then(r => r.json());
```

## 许可

MIT License · 数据来源于《西游记》原著（公共版权）+ 项目原创分析标注。
