# dataset/ — 详解西游记结构化数据

> 来源：`site/data/*.html` 的 `EMBEDDED_DATA` 快照 + 人工整理件；
> 本索引由 `scripts/gen_dataset_index.py` 从磁盘实读生成（禁手改）。
> 当前规模：根级 43 个 JSON + `entities/` 2 个 JSON，合计 2692.3 KB。

## 概览

- 根级数据文件：43 个；实体聚合：2 个。
- 快照来源：页面 `EMBEDDED_DATA`（未找到对应页面的文件在「主要键」列标注人工件）。
- 校验：第 61 门禁 `python scripts/check_dataset_provenance.py`；清单对拍 `python scripts/check_dataset_manifest.py`。

## 数据索引

| 文件 | 条目数 | 大小 | 键数 | 主要键 |
|------|-------|------|------|--------|
| 81-hardships.json | 6 | 17.0 KB | 6 | by_cause、by_difficulty、by_ending、cross_cause_ending、hardships、total |
| ai-dialogue.json | 3 | 20.3 KB | 3 | celebrities、journey_quotes、quick_topics |
| cave-estate.json | 4 | 16.3 KB | 4 | by_owner_rank、by_region、caves、top_luxury |
| century-dialogue.json | 2 | 1.8 KB | 2 | roundtable_topics、triangle_dialogue |
| chapter-structure-graph.json | 5 | 8.1 KB | 5 | cluster、heatmap、kpi、meta、wordCount |
| chapters-metadata.json | 2 | 47.2 KB | 2 | chapters、meta |
| character-relationship-3d.json | 5 | 29.8 KB | 5 | _schema、kpi、links、meta、nodes |
| concept-device.json | 9 | 13.2 KB | 9 | cipher、commentators、danmaku、detective、insights、mobius… |
| criticism-history.json | 8 | 11.8 KB | 8 | _schema、alchemy、candidates、critics、lu_xun_words、streams… |
| cross-time-danmaku.json | 6 | 12.0 KB | 6 | age_groups、celebrity_profiles、global_adaptations、international_critics、modern_commentary、mouthpiece_quotes |
| edge-wukong-tangseng.json | 7 | 11.0 KB | 7 | _schema、aggregate、disputed_points、edge、events、meta… |
| emotional-heatmap.json | 4 | 37.1 KB | 4 | hardships、meta、reactions、scholars |
| famous-time-travel.json | 2 | 2.1 KB | 2 | scene_illustrations、travel_identities |
| four-dimensional-research-network.json | 8 | 13.0 KB | 8 | dimensions、indicators、meta、network、polarExtra、radar… |
| four-heavenly-kings-artifacts.json | 5 | 5.2 KB | 5 | _schema、chord、kings、radar、timeline |
| glossary.json | 3 | 9.6 KB | 3 | groups、note、source |
| guanyin-six-roles-network.json | 7 | 16.5 KB | 7 | _schema、intensity、network、radar、roles、sankey… |
| heaven-power-network.json | 6 | 15.8 KB | 6 | hierarchy、network、radar、sankey、summary、timeline |
| intertextuality-network.json | 1 | 14.2 KB | 1 | intertextuality |
| journey-geo-semiotics.json | 2 | 1.9 KB | 2 | links、nodes |
| journey-map-interactive.json | 3 | 6.3 KB | 3 | kpi、meta、nodes |
| language-style-radar.json | 5 | 2.8 KB | 5 | characters、dimensions、kpi、meta、pca |
| magic-system.json | 5 | 16.3 KB | 5 | magic_arrays、magic_energy_sankey、magic_fire、magic_system、magic_treasures |
| material-archaeology.json | 4 | 26.6 KB | 4 | artifact_materials、cave_architecture、costume_archaeology、summary |
| ming-political-thought-comparison.json | 8 | 5.8 KB | 8 | _schema、heatmap、kpi、meta、polar、radar… |
| monster-capability-radar.json | 7 | 6.0 KB | 7 | bar、kpi、kpi_extreme、meta、radar、sankey… |
| monster-ecology-network.json | 6 | 18.1 KB | 6 | kpi、meta、network、radar、sankey、timeline |
| monster-female-network.json | 1 | 17.7 KB | 1 | monsterFemale |
| monster-hierarchy-network.json | 6 | 16.3 KB | 6 | network、radar、sankey、summary、tiers、timeline |
| monster-victims-network.json | 6 | 11.7 KB | 6 | _schema、network、radar、sankey、timeline、victims |
| music-structure.json | 5 | 20.4 KB | 5 | movement、rhythm、sounds、summary、symmetry |
| narratology-12d-network.json | 1 | 21.5 KB | 1 | narratology |
| narratology-13d-network.json | 4 | 29.6 KB | 4 | deprecated、deprecation_note、narratology、replacement_page |
| pilgrim-team-dynamic-network.json | 5 | 6.3 KB | 5 | belbin、kpi、meta、network、phases |
| pilgrim-team-psychology-arc.json | 7 | 5.4 KB | 7 | boxplot、cohesion_heatmap、kpi、meta、psychology_arc、radar… |
| poetry-rhythm-analysis.json | 7 | 4.3 KB | 7 | boxplot、heatmap、kpi、meta、pie、stacked… |
| six-senses-narratology-network.json | 1 | 17.8 KB | 1 | sixSenses |
| text-evolution.json | 5 | 13.1 KB | 5 | authors、commentators、summary、variants、versions |
| text-search.json | 4 | 2091.2 KB | 4 | artifacts、chapters、characters、corpus_note |
| theological-intervention-network.json | 5 | 10.4 KB | 5 | meta、network、radar、sankey、timeline |
| timeline.json | 1 | 5.5 KB | 1 | timeline |
| underworld-power-network.json | 6 | 14.0 KB | 6 | hierarchy、network、radar、sankey、summary、timeline |
| yuanqi-graph.json | 3 | 7.8 KB | 3 | edges、meta、nodes |

### entities/

| 文件 | 条目数 | 大小 | 键数 | 主要键 |
|------|-------|------|------|--------|
| characters.json | 56 | 9.6 KB | 7 | count、entities、generated、method、source、title… |
| locations.json | 61 | 9.1 KB | 7 | count、entities、generated、method、source、title… |

## 编码与溯源

- [CODING.md](CODING.md)：人物关系编码手册（关系类型、权重、证据级别、边界案例与争议处理）。
- `character-relationship-3d.json`：22 节点 / 32 边；节点补阵营、登场回目与证据级别；边补规则、理由、权重与争议标记。
- `edge-wukong-tangseng.json`：唐僧—孙悟空单边示范档案（9 组逐回事件、引文状态、max/mean/count 权重敏感性）。
- `entities/`：`characters.json`（56 实体）与 `locations.json`（61 实体），由 `chapters-metadata.json` 的逐回聚合对拍。
- 校验：`check_dataset_provenance.py`（第 61 槽）覆盖关系网络与标杆边；`check_dataset_manifest.py` 校验本索引与磁盘一致。

> 该网络为示意性人工整理网络，不做统计推断；与 `character_nlp.py` 生成的共现网络不是同一口径。

## 使用方式

```python
import json
with open('dataset/character-relationship-3d.json', encoding='utf-8') as f:
    data = json.load(f)
print(data['meta'], len(data['nodes']), len(data['links']))
```

```javascript
const data = await fetch('dataset/character-relationship-3d.json').then(r => r.json());
```

## 许可

MIT License · 数据来源于《西游记》原著（公共版权）+ 项目原创分析标注。
