# 全站硬编码颜色盘点（W1078 · B2 落地面）

> 生成件：`python scripts/_w1078_color_inventory.py` · 机器版同目录 `_w1078_color_inventory.json`

> 扫描面：site/ 下 857 个 HTML 页（含根页 / data / en / reader）· 令牌表取自 `site/tokens.css`（浅色 103 名 · 暗色 29 名）


## 1. 总量与分类

| 分类 | 处数 | 可否换成 var() | 理由 |
|:--|--:|:--:|:--|
| 页内私有消费 | 401 | ✅ 可（逐页） | 页内自己的 `<style>` 声明 |
| 内联样式消费 | 665 | ✅ 可（逐页） | `style="…"` 属性 |
| SVG属性位 | 0 | ⚠️ 需改写法 | `fill="#xxx"` 等表现属性不解析 `var()` |
| JS字面量 | 5041 | ⚠️ 需工程化 | SVG/Canvas 属性位不解析 `var()` |
| 共享副本消费 | 57090 | ⚠️ 属共享层 | INLINED 拷贝（tokens.css+system.css）⇒ 改这里级联全站 |
| 定义面 | 15166 | ❌ 不算消费面 | `:root` / 暗色块里的令牌定义本身 |
| 标记文本 | 312 | 逐处判定 | 文本/非样式属性 |

**可逐页消费的量 = 页内私有消费 + 内联样式消费 = 1066 处**；其余 77297 处分别受「共享层边界」「属性位不解析 var()」「令牌定义非消费面」三类约束。

## 2. 令牌映射总表（hex → 令牌 → 浅/暗取值 → 替换后果）

| 色值 | 令牌 | 浅色值 | 暗色值 | 替换后果 |
|:--|:--|:--|:--|:--|
| `#221D16` | `--dark` | #221D16 | （无暗色覆盖） | 浅色零差异；暗色沿用浅色值（零差异） |
| `#221D16` | `--bg`（暗色值） | #FAF7F0 | #221D16 | 仅暗色同值；浅色会变（暗色语境替换） |
| `#23201A` | `--ink` | #23201A | #F2EBDC | 浅色零差异；暗色变为 #F2EBDC（有意变化·须列举） |
| `#2B2419` | `--paper`（暗色值） | #FFFFFF | #2B2419 | 仅暗色同值；浅色会变（暗色语境替换） |
| `#33291B` | `--paper-warm`（暗色值） | #F1EBDD | #33291B | 仅暗色同值；浅色会变（暗色语境替换） |
| `#3A6B8C` | `--accent-2` | #3A6B8C | #7FA8C9 | 浅色零差异；暗色变为 #7FA8C9（有意变化·须列举） |
| `#3A6B8C` | `--chart-2` | #3A6B8C | #7FA8C9 | 浅色零差异；暗色变为 #7FA8C9（有意变化·须列举） |
| `#6B6455` | `--ink-soft` | #6B6455 | #CBBFA9 | 浅色零差异；暗色变为 #CBBFA9（有意变化·须列举） |
| `#6B8E5A` | `--accent-4` | #6B8E5A | #9DB98A | 浅色零差异；暗色变为 #9DB98A（有意变化·须列举） |
| `#6B8E5A` | `--chart-4` | #6B8E5A | #9DB98A | 浅色零差异；暗色变为 #9DB98A（有意变化·须列举） |
| `#7FA8C9` | `--accent-2`（暗色值） | #3A6B8C | #7FA8C9 | 仅暗色同值；浅色会变（暗色语境替换） |
| `#7FA8C9` | `--chart-2`（暗色值） | #3A6B8C | #7FA8C9 | 仅暗色同值；浅色会变（暗色语境替换） |
| `#7FA8C9` | `--info`（暗色值） | var(--accent-2) | #7FA8C9 | 仅暗色同值；浅色会变（暗色语境替换） |
| `#8A6D3B` | `--accent-3` | #8A6D3B | #C9A96B | 浅色零差异；暗色变为 #C9A96B（有意变化·须列举） |
| `#8A6D3B` | `--chart-6` | #8A6D3B | #C9A96B | 浅色零差异；暗色变为 #C9A96B（有意变化·须列举） |
| `#8C2A2A` | `--rebel` | #8C2A2A | （无暗色覆盖） | 浅色零差异；暗色沿用浅色值（零差异） |
| `#8F8674` | `--ink-faint`（暗色值） | #9A9280 | #8F8674 | 仅暗色同值；浅色会变（暗色语境替换） |
| `#8FBF7F` | `--ok`（暗色值） | var(--accent-4) | #8FBF7F | 仅暗色同值；浅色会变（暗色语境替换） |
| `#9A9280` | `--ink-faint` | #9A9280 | #8F8674 | 浅色零差异；暗色变为 #8F8674（有意变化·须列举） |
| `#9DB98A` | `--accent-4`（暗色值） | #6B8E5A | #9DB98A | 仅暗色同值；浅色会变（暗色语境替换） |
| `#9DB98A` | `--chart-4`（暗色值） | #6B8E5A | #9DB98A | 仅暗色同值；浅色会变（暗色语境替换） |
| `#AF3F34` | `--accent-deep` | #AF3F34 | #C94F3F | 浅色零差异；暗色变为 #C94F3F（有意变化·须列举） |
| `#B38F58` | `--chart-3` | #B38F58 | （无暗色覆盖） | 浅色零差异；暗色沿用浅色值（零差异） |
| `#C7463A` | `--accent-text` | #C7463A | #E0604F | 浅色零差异；暗色变为 #E0604F（有意变化·须列举） |
| `#C8463A` | `--accent` | #C8463A | #E46250 | 浅色零差异；暗色变为 #E46250（有意变化·须列举） |
| `#C8463A` | `--chart-1` | #C8463A | #E0604F | 浅色零差异；暗色变为 #E0604F（有意变化·须列举） |
| `#C94F3F` | `--accent-deep`（暗色值） | #AF3F34 | #C94F3F | 仅暗色同值；浅色会变（暗色语境替换） |
| `#C9A96B` | `--accent-3`（暗色值） | #8A6D3B | #C9A96B | 仅暗色同值；浅色会变（暗色语境替换） |
| `#C9A96B` | `--chart-6`（暗色值） | #8A6D3B | #C9A96B | 仅暗色同值；浅色会变（暗色语境替换） |
| `#CBBFA9` | `--ink-soft`（暗色值） | #6B6455 | #CBBFA9 | 仅暗色同值；浅色会变（暗色语境替换） |
| `#D0A35C` | `--warn`（暗色值） | var(--accent-3) | #D0A35C | 仅暗色同值；浅色会变（暗色语境替换） |
| `#D8CFBC` | `--chart-5` | #D8CFBC | （无暗色覆盖） | 浅色零差异；暗色沿用浅色值（零差异） |
| `#D96C5C` | `--danger`（暗色值） | var(--rebel) | #D96C5C | 仅暗色同值；浅色会变（暗色语境替换） |
| `#E0604F` | `--chart-1`（暗色值） | #C8463A | #E0604F | 仅暗色同值；浅色会变（暗色语境替换） |
| `#E0604F` | `--accent-text`（暗色值） | #C7463A | #E0604F | 仅暗色同值；浅色会变（暗色语境替换） |
| `#E46250` | `--accent`（暗色值） | #C8463A | #E46250 | 仅暗色同值；浅色会变（暗色语境替换） |
| `#E5DFD0` | `--line` | #E5DFD0 | rgba(242, 235, 220, 0.14) | 浅色零差异；暗色变为 rgba(242, 235, 220, 0.14)（有意变化·须列举） |
| `#E8A99F` | `--accent-soft`（暗色值） | #E9B885 | #E8A99F | 仅暗色同值；浅色会变（暗色语境替换） |
| `#E9B885` | `--accent-soft` | #E9B885 | #E8A99F | 浅色零差异；暗色变为 #E8A99F（有意变化·须列举） |
| `#F1EBDD` | `--paper-warm` | #F1EBDD | #33291B | 浅色零差异；暗色变为 #33291B（有意变化·须列举） |
| `#F2EBDC` | `--dark-text` | #F2EBDC | （无暗色覆盖） | 浅色零差异；暗色沿用浅色值（零差异） |
| `#F2EBDC` | `--ink`（暗色值） | #23201A | #F2EBDC | 仅暗色同值；浅色会变（暗色语境替换） |
| `#FAF7F0` | `--bg` | #FAF7F0 | #221D16 | 浅色零差异；暗色变为 #221D16（有意变化·须列举） |
| `#FFFFFF` | `--paper` | #FFFFFF | #2B2419 | 浅色零差异；暗色变为 #2B2419（有意变化·须列举） |

## 3. 逐页清单（全站 857 页 · 有硬编码色的页按分类计数）

| 页 | 页内私有消费 | 内联样式 | SVG属性 | JS字面量 | 共享副本 | 定义面 | 主要色值（页内私有+JS） |
|:--|--:|--:|--:|--:|--:|--:|:--|
| `404.html` | 11 | 2 | 0 | 0 | 0 | 0 | #C8463A×4、#23201A×3、#FFFFFF×2 |
| `_template.html` | 0 | 1 | 0 | 12 | 173 | 44 | #C8463A×3、#3A6B8C×2、#C9A063×2 |
| `curated.html` | 0 | 0 | 0 | 0 | 0 | 0 | — |
| `dashboard.html` | 1 | 0 | 0 | 10 | 0 | 1 | #C8463A×3、#3A6B8C×3、#FFF8EC×1 |
| `data/81-hardships-view.html` | 1 | 0 | 0 | 24 | 173 | 48 | #C8463A×5、#D9CDB8×5、#6B6455×4 |
| `data/81-hardships.html` | 0 | 1 | 0 | 9 | 173 | 44 | #C8463A×4、#3A6B8C×2、#6B8E5A×2 |
| `data/_shell.html` | 0 | 1 | 0 | 0 | 173 | 44 | #C8463A×1 |
| `data/aesthetics.html` | 1 | 1 | 0 | 30 | 173 | 44 | #C8463A×5、#D4A857×4、#3A2820×3 |
| `data/ai-dialogue.html` | 0 | 1 | 0 | 0 | 173 | 44 | #C8463A×1 |
| `data/business-model.html` | 1 | 3 | 0 | 14 | 173 | 44 | #C8463A×7、#E8DDC8×4、#3A6B8C×3 |
| `data/cave-estate.html` | 0 | 1 | 0 | 11 | 173 | 44 | #D9CDB8×4、#C8463A×3、#3A6B8C×1 |
| `data/century-dialogue.html` | 1 | 1 | 0 | 0 | 173 | 44 | #3A2820×1、#C8463A×1 |
| `data/chapter-stats.html` | 0 | 5 | 0 | 4 | 173 | 44 | #C8463A×3、#3A6B8C×2、#E9B885×2 |
| `data/chapter-structure-graph.html` | 0 | 5 | 0 | 25 | 173 | 44 | #2C3E50×9、#C9A063×5、#C8463A×2 |
| `data/character-appearance.html` | 0 | 1 | 0 | 21 | 173 | 44 | #C8463A×3、#FAF7F2×2、#D9CDB8×2 |
| `data/character-dynamic-network.html` | 1 | 1 | 0 | 10 | 173 | 44 | #C8463A×3、#3A6B8C×2、#B8862A×2 |
| `data/character-presence-timeline.html` | 0 | 1 | 0 | 3 | 173 | 44 | #C8463A×2、#3A6B8C×1、#8B7355×1 |
| `data/character-relationship-3d-view.html` | 1 | 0 | 0 | 24 | 173 | 48 | #C8463A×5、#D9CDB8×5、#6B6455×4 |
| `data/character-relationship-3d.html` | 1 | 7 | 0 | 1 | 173 | 44 | #F5E9D4×2、#1A2530×1、#C8463A×1 |
| `data/character-semantic-network.html` | 0 | 1 | 0 | 51 | 173 | 44 | #C8463A×13、#3A6B8C×12、#8B7355×7 |
| `data/character-sentiment-arc.html` | 2 | 8 | 0 | 17 | 173 | 44 | #C8463A×8、#C9A063×3、#6B8E5A×3 |
| `data/chart-design.html` | 1 | 10 | 0 | 27 | 173 | 44 | #E9B885×10、#C8463A×6、#6B8E5A×5 |
| `data/cognitive-psychology.html` | 0 | 1 | 0 | 13 | 173 | 44 | #C8463A×3、#E8DDC8×3、#3A6B8C×2 |
| `data/concept-device.html` | 25 | 4 | 0 | 26 | 173 | 44 | #3A6B8C×6、#C9A063×6、#C8463A×4 |
| `data/counterfactual.html` | 0 | 1 | 0 | 10 | 173 | 44 | #C8463A×3、#C9A063×2、#E9B885×2 |
| `data/criticism-history.html` | 0 | 2 | 0 | 20 | 173 | 44 | #C9A063×8、#3A6B8C×4、#C8463A×3 |
| `data/cross-time-danmaku.html` | 3 | 1 | 0 | 0 | 173 | 44 | #2A1F18×1、#F5EFE6×1、#EDE4D3×1 |
| `data/cultural-misreading.html` | 3 | 1 | 0 | 10 | 173 | 44 | #C8463A×2、#23201A×2、#F3EEE2×1 |
| `data/customs-pass-route.html` | 0 | 1 | 0 | 0 | 173 | 44 | #C8463A×1 |
| `data/data-explorer.html` | 1 | 0 | 0 | 24 | 173 | 48 | #C8463A×5、#D9CDB8×5、#6B6455×4 |
| `data/deconstruction.html` | 2 | 3 | 0 | 24 | 173 | 44 | #C8463A×3、#B8A98E×3、#E9B885×2 |
| `data/dialogue-sentiment.html` | 0 | 3 | 0 | 13 | 173 | 44 | #6B8E5A×3、#C8463A×2、#8C2A2A×2 |
| `data/ecology.html` | 0 | 9 | 0 | 16 | 173 | 44 | #E9B885×9、#E8DDC8×7、#C8463A×3 |
| `data/emotional-heatmap.html` | 0 | 1 | 0 | 8 | 173 | 44 | #C8463A×2、#C9A063×1、#3A6B8C×1 |
| `data/ethics-consumption.html` | 6 | 2 | 0 | 9 | 173 | 44 | #C8463A×3、#D97706×2、#B88C2A×2 |
| `data/famous-time-travel.html` | 1 | 1 | 0 | 0 | 173 | 44 | #3A2820×1、#C8463A×1 |
| `data/four-dimensional-research-network.html` | 0 | 1 | 0 | 56 | 173 | 44 | #2C2416×10、#C89B3C×9、#6B6455×8 |
| `data/four-heavenly-kings-artifacts.html` | 1 | 1 | 0 | 23 | 173 | 44 | #8A7A6A×6、#C8463A×4、#8B7355×4 |
| `data/game-webnovel.html` | 1 | 4 | 0 | 35 | 173 | 44 | #D4AF37×5、#3A6B8C×5、#C9A063×5 |
| `data/global-pattern.html` | 1 | 3 | 0 | 9 | 173 | 44 | #C8463A×2、#3A2820×1、#E9B885×1 |
| `data/graph-explorer.html` | 12 | 11 | 0 | 49 | 173 | 49 | #9A8F7C×7、#8A7D68×6、#D4A017×5 |
| `data/guanyin-six-roles-network.html` | 0 | 1 | 0 | 37 | 173 | 44 | #8A7A6A×11、#8B7355×8、#D4C4A8×6 |
| `data/hardship-difficulty-heatmap.html` | 2 | 8 | 0 | 16 | 173 | 44 | #E9B885×8、#C8463A×3、#D4C4A8×3 |
| `data/hardship-heatmap.html` | 2 | 4 | 0 | 9 | 173 | 44 | #C8463A×4、#E9B885×4、#8C2A2A×2 |
| `data/heaven-power-network.html` | 1 | 1 | 0 | 84 | 173 | 44 | #C8463A×14、#8A7C6A×14、#C9A961×10 |
| `data/intertextuality-network.html` | 0 | 1 | 0 | 91 | 173 | 44 | #8B4513×22、#8A7A5A×18、#5A3828×8 |
| `data/journey-geo-3d.html` | 2 | 7 | 0 | 1 | 173 | 44 | #F2EBDC×2、#C8463A×2、#1A2530×1 |
| `data/journey-geo-semiotics.html` | 0 | 1 | 0 | 10 | 173 | 44 | #C8463A×3、#D4AF37×2、#3A6B8C×2 |
| `data/journey-map-interactive.html` | 4 | 6 | 0 | 17 | 173 | 44 | #C8463A×4、#C9A063×4、#2C3E50×4 |
| `data/journey-route.html` | 1 | 1 | 0 | 17 | 173 | 44 | #E9B885×4、#C8463A×3、#6B8E5A×2 |
| `data/journey-spacetime.html` | 3 | 5 | 0 | 8 | 173 | 44 | #3A6B8C×4、#C8463A×4、#E9B885×4 |
| `data/jurisprudence.html` | 1 | 19 | 0 | 40 | 173 | 44 | #C8463A×14、#E9B885×11、#C9A063×9 |
| `data/karma-reincarnation.html` | 1 | 2 | 0 | 48 | 173 | 44 | #C8463A×7、#E9B885×6、#3A6B8C×6 |
| `data/language-style-radar.html` | 0 | 4 | 0 | 21 | 173 | 44 | #2C3E50×6、#C9A063×5、#D9CDB8×4 |
| `data/linguistics.html` | 0 | 1 | 0 | 19 | 173 | 44 | #E8DDC8×5、#C8463A×4、#E9B885×3 |
| `data/magic-system.html` | 3 | 6 | 0 | 13 | 173 | 44 | #C8463A×6、#D4A857×6、#3A6B8C×4 |
| `data/material-archaeology.html` | 1 | 1 | 0 | 38 | 173 | 44 | #C8463A×9、#3A6B8C×8、#C9A063×7 |
| `data/mbti-evolution.html` | 0 | 4 | 0 | 9 | 173 | 44 | #E9B885×4、#C8463A×3、#3A6B8C×2 |
| `data/methodology-matrix.html` | 8 | 5 | 0 | 11 | 173 | 44 | #E9B885×4、#C8463A×4、#6B8E5A×2 |
| `data/ming-political-thought-comparison.html` | 0 | 7 | 0 | 38 | 173 | 44 | #C8463A×9、#3A6B8C×6、#D9CDB8×5 |
| `data/monster-background.html` | 2 | 6 | 0 | 18 | 173 | 44 | #C8463A×6、#6B6455×5、#3A6B8C×3 |
| `data/monster-capability-radar.html` | 0 | 10 | 0 | 32 | 173 | 44 | #E9B885×9、#C8463A×5、#3A6B8C×5 |
| `data/monster-ecology-network.html` | 0 | 8 | 0 | 19 | 173 | 44 | #C8463A×7、#C9A063×7、#3A6B8C×5 |
| `data/monster-female-network.html` | 0 | 1 | 0 | 96 | 173 | 44 | #8A7A5A×12、#8B4513×10、#5A3828×8 |
| `data/monster-hierarchy-network.html` | 0 | 1 | 0 | 81 | 173 | 44 | #8B3A2A×17、#8A7C6A×16、#6B8E6F×14 |
| `data/monster-sociology.html` | 0 | 12 | 0 | 30 | 173 | 44 | #C8463A×6、#6B8E5A×5、#3A6B8C×4 |
| `data/monster-victims-network.html` | 0 | 1 | 0 | 43 | 173 | 44 | #8A7A6A×11、#C8463A×7、#8B7355×7 |
| `data/music-structure.html` | 0 | 1 | 0 | 27 | 173 | 44 | #C8463A×5、#3A6B8C×4、#C9A14A×4 |
| `data/narrative-experiment.html` | 4 | 11 | 0 | 53 | 173 | 44 | #C8463A×17、#3A6B8C×16、#C9A063×15 |
| `data/narrative-rhythm-curve.html` | 2 | 8 | 0 | 16 | 173 | 44 | #2C3E50×7、#C9A063×6、#C8463A×3 |
| `data/narratology-12d-network.html` | 0 | 1 | 0 | 100 | 173 | 44 | #8A7A5A×19、#8B4513×16、#5A3828×12 |
| `data/narratology-16d-network.html` | 0 | 1 | 0 | 128 | 173 | 44 | #8A7A5A×21、#8B4513×13、#4A6B8A×11 |
| `data/perf-canvas-rendering.html` | 1 | 1 | 0 | 7 | 173 | 44 | #C8463A×2、#F5F0E6×1、#8B4513×1 |
| `data/philosophy.html` | 0 | 8 | 0 | 32 | 173 | 44 | #C8463A×9、#C9A063×6、#3A6B8C×4 |
| `data/pilgrim-team-dynamic-network.html` | 1 | 1 | 0 | 18 | 173 | 44 | #C8463A×4、#D9CDB8×4、#6B8E5A×3 |
| `data/pilgrim-team-psychology-arc.html` | 0 | 15 | 0 | 20 | 173 | 44 | #E9B885×12、#C8463A×5、#C9A063×2 |
| `data/poetry-rhythm-analysis.html` | 0 | 10 | 0 | 18 | 173 | 44 | #E9B885×10、#C8463A×6、#FFF8E7×3 |
| `data/power-resources.html` | 0 | 1 | 0 | 20 | 173 | 44 | #C8463A×4、#3A6B8C×4、#E8DDC8×4 |
| `data/relationships.html` | 0 | 8 | 0 | 69 | 173 | 44 | #3A6B8C×20、#C8463A×16、#6B8E5A×7 |
| `data/risk-project.html` | 7 | 12 | 0 | 27 | 173 | 44 | #C8463A×8、#E9B885×5、#3A6B8C×5 |
| `data/search.html` | 1 | 0 | 0 | 0 | 173 | 48 | #3A2820×1 |
| `data/six-senses-narratology-network.html` | 0 | 1 | 0 | 53 | 173 | 44 | #8B4513×17、#8A7A5A×12、#D4C5A9×6 |
| `data/social-media.html` | 1 | 1 | 0 | 38 | 173 | 45 | #C8463A×7、#C9A063×7、#3A6B8C×6 |
| `data/story-timeline.html` | 0 | 1 | 0 | 5 | 173 | 44 | #C8463A×2、#3A6B8C×1、#C9A063×1 |
| `data/tag-cloud.html` | 5 | 7 | 0 | 6 | 173 | 44 | #C8463A×3、#D9C9A8×2、#F0C878×2 |
| `data/text-evolution.html` | 0 | 1 | 0 | 19 | 173 | 44 | #C8463A×5、#3A6B8C×3、#C9A063×3 |
| `data/text-search.html` | 0 | 1 | 0 | 2 | 173 | 44 | #C8463A×2、#5A4A3F×1 |
| `data/theological-intervention-network.html` | 0 | 1 | 0 | 39 | 173 | 44 | #1E3A8A×12、#A83232×7、#C9B896×6 |
| `data/timeline.html` | 0 | 1 | 0 | 11 | 173 | 44 | #C8463A×3、#C9A063×2、#3A6B8C×2 |
| `data/underworld-power-network.html` | 0 | 1 | 0 | 81 | 173 | 44 | #8A7C6A×14、#C8463A×13、#3A6B8C×11 |
| `data/visual-art.html` | 3 | 8 | 0 | 32 | 173 | 44 | #D4AF37×14、#C8463A×6、#D97706×3 |
| `data/workplace.html` | 0 | 3 | 0 | 19 | 173 | 44 | #C8463A×7、#E9B885×3、#C9A063×3 |
| `dukou-engine.html` | 6 | 0 | 0 | 10 | 173 | 66 | #2B2419×2、#C8463A×2、#D4A017×2 |
| `en/81-hardships-view.html` | 1 | 0 | 0 | 24 | 173 | 48 | #C8463A×5、#D9CDB8×5、#6B6455×4 |
| `en/81-hardships.html` | 0 | 2 | 0 | 11 | 173 | 44 | #C8463A×4、#E9B885×2、#3A6B8C×2 |
| `en/academic-papers.html` | 2 | 0 | 0 | 0 | 173 | 55 | #3A2820×1、#5A3828×1 |
| `en/aesthetics.html` | 1 | 4 | 0 | 30 | 173 | 44 | #C8463A×5、#E9B885×4、#D4A857×4 |
| `en/ai-dialogue.html` | 0 | 1 | 0 | 0 | 173 | 44 | #C8463A×1 |
| `en/bestiary.html` | 6 | 0 | 0 | 0 | 173 | 55 | #3A2820×1、#5A3828×1、#F0E9DA×1 |
| `en/business-model.html` | 1 | 3 | 0 | 30 | 173 | 44 | #C8463A×12、#3A6B8C×6、#E8DDC8×4 |
| `en/cave-estate.html` | 0 | 1 | 0 | 24 | 173 | 44 | #6B6455×7、#D9CDB8×4、#C8463A×3 |
| `en/century-dialogue.html` | 1 | 1 | 0 | 0 | 173 | 44 | #3A2820×1、#C8463A×1 |
| `en/chapter-stats.html` | 0 | 8 | 0 | 4 | 173 | 44 | #E9B885×5、#C8463A×3、#3A6B8C×2 |
| `en/chapter-structure-graph.html` | 0 | 5 | 0 | 25 | 173 | 44 | #2C3E50×9、#C9A063×5、#C8463A×2 |
| `en/chapters-map.html` | 6 | 0 | 0 | 0 | 173 | 55 | #3A2820×1、#5A3828×1、#F0E9DA×1 |
| `en/character-appearance.html` | 0 | 1 | 0 | 26 | 173 | 44 | #C8463A×4、#6B6455×3、#C9A063×2 |
| `en/character-bailongma.html` | 2 | 0 | 0 | 0 | 173 | 55 | #3A2820×1、#5A3828×1 |
| `en/character-bajie.html` | 2 | 0 | 0 | 0 | 173 | 55 | #3A2820×1、#5A3828×1 |
| `en/character-dynamic-network.html` | 1 | 4 | 0 | 11 | 173 | 44 | #E9B885×3、#C8463A×3、#3A6B8C×2 |
| `en/character-presence-timeline.html` | 0 | 1 | 0 | 3 | 173 | 44 | #C8463A×2、#3A6B8C×1、#8B7355×1 |
| `en/character-relationship-3d-view.html` | 1 | 0 | 0 | 24 | 173 | 48 | #C8463A×5、#D9CDB8×5、#6B6455×4 |
| `en/character-relationship-3d.html` | 1 | 7 | 0 | 1 | 173 | 44 | #F5E9D4×2、#1A2530×1、#C8463A×1 |
| `en/character-semantic-network.html` | 0 | 1 | 0 | 51 | 173 | 44 | #C8463A×13、#3A6B8C×12、#8B7355×7 |
| `en/character-sentiment-arc.html` | 2 | 8 | 0 | 22 | 173 | 44 | #C8463A×13、#C9A063×3、#6B8E5A×3 |
| `en/character-shaseng.html` | 2 | 0 | 0 | 0 | 173 | 55 | #3A2820×1、#5A3828×1 |
| `en/character-tangseng.html` | 2 | 0 | 0 | 0 | 173 | 55 | #3A2820×1、#5A3828×1 |
| `en/character-wukong.html` | 2 | 0 | 0 | 0 | 173 | 55 | #3A2820×1、#5A3828×1 |
| `en/characters.html` | 6 | 0 | 0 | 0 | 173 | 55 | #3A2820×1、#5A3828×1、#F0E9DA×1 |
| `en/chart-design.html` | 1 | 10 | 0 | 27 | 173 | 44 | #E9B885×10、#C8463A×6、#6B8E5A×5 |
| `en/cognitive-psychology.html` | 0 | 1 | 0 | 31 | 173 | 44 | #C8463A×9、#3A6B8C×4、#C9A063×4 |
| `en/concept-device.html` | 25 | 4 | 0 | 36 | 173 | 44 | #C9A063×9、#C8463A×8、#3A6B8C×7 |
| `en/counterfactual.html` | 0 | 1 | 0 | 16 | 173 | 44 | #6B6455×4、#C8463A×3、#23201A×3 |
| `en/criticism-history.html` | 0 | 2 | 0 | 21 | 173 | 44 | #C9A063×8、#3A6B8C×4、#C8463A×3 |
| `en/cross-time-danmaku.html` | 3 | 1 | 0 | 0 | 173 | 44 | #2A1F18×1、#F5EFE6×1、#EDE4D3×1 |
| `en/cultural-misreading.html` | 3 | 2 | 0 | 10 | 173 | 44 | #C8463A×2、#E9B885×2、#23201A×2 |
| `en/customs-pass-route.html` | 0 | 1 | 0 | 0 | 173 | 44 | #C8463A×1 |
| `en/dashboard.html` | 2 | 0 | 0 | 0 | 173 | 55 | #3A2820×1、#5A3828×1 |
| `en/data-explorer.html` | 1 | 0 | 0 | 24 | 173 | 48 | #C8463A×5、#D9CDB8×5、#6B6455×4 |
| `en/deconstruction.html` | 2 | 3 | 0 | 27 | 173 | 44 | #C9A063×4、#C8463A×3、#B8A98E×3 |
| `en/dialogue-sentiment.html` | 0 | 3 | 0 | 20 | 173 | 44 | #6B6455×7、#6B8E5A×3、#C8463A×2 |
| `en/dukou-engine.html` | 2 | 0 | 0 | 10 | 173 | 51 | #C8463A×2、#D4A017×2、#F3ECE0×1 |
| `en/ecology.html` | 0 | 9 | 0 | 16 | 173 | 44 | #E9B885×9、#E8DDC8×7、#C8463A×3 |
| `en/emotional-heatmap.html` | 0 | 1 | 0 | 8 | 173 | 44 | #C8463A×2、#C9A063×1、#3A6B8C×1 |
| `en/essay-ai-era.html` | 2 | 0 | 0 | 0 | 173 | 55 | #3A2820×1、#5A3828×1 |
| `en/essay-buddhist-chan.html` | 2 | 0 | 0 | 0 | 173 | 55 | #3A2820×1、#5A3828×1 |
| `en/essay-chapter-couplets.html` | 2 | 0 | 0 | 0 | 173 | 55 | #3A2820×1、#5A3828×1 |
| `en/essay-character-fu.html` | 2 | 0 | 0 | 0 | 173 | 55 | #3A2820×1、#5A3828×1 |
| `en/essay-cipai-linjiangxian.html` | 2 | 0 | 0 | 0 | 173 | 55 | #3A2820×1、#5A3828×1 |
| `en/essay-cipai-mantingfang.html` | 2 | 0 | 0 | 0 | 173 | 55 | #3A2820×1、#5A3828×1 |
| `en/essay-cipai-shuidiaogetou.html` | 2 | 0 | 0 | 0 | 173 | 55 | #3A2820×1、#5A3828×1 |
| `en/essay-cipai-xijiangyue.html` | 2 | 0 | 0 | 0 | 173 | 55 | #3A2820×1、#5A3828×1 |
| `en/essay-composition-origins.html` | 2 | 0 | 0 | 0 | 173 | 55 | #3A2820×1、#5A3828×1 |
| `en/essay-divine-bureaucracy.html` | 2 | 0 | 0 | 0 | 173 | 55 | #3A2820×1、#5A3828×1 |
| `en/essay-folk-belief.html` | 2 | 0 | 0 | 0 | 173 | 55 | #3A2820×1、#5A3828×1 |
| `en/essay-historical-xuanzang.html` | 2 | 0 | 0 | 0 | 173 | 55 | #3A2820×1、#5A3828×1 |
| `en/essay-information-cocoon.html` | 2 | 0 | 0 | 0 | 173 | 55 | #3A2820×1、#5A3828×1 |
| `en/essay-ming-economy.html` | 2 | 0 | 0 | 0 | 173 | 55 | #3A2820×1、#5A3828×1 |
| `en/essay-ming-examination.html` | 2 | 0 | 0 | 0 | 173 | 55 | #3A2820×1、#5A3828×1 |
| `en/essay-ming-garrison.html` | 2 | 0 | 0 | 0 | 173 | 55 | #3A2820×1、#5A3828×1 |
| `en/essay-ming-intellectual-history.html` | 2 | 0 | 0 | 0 | 173 | 55 | #3A2820×1、#5A3828×1 |
| `en/essay-ming-judiciary.html` | 2 | 0 | 0 | 0 | 173 | 55 | #3A2820×1、#5A3828×1 |
| `en/essay-ming-literary-thought.html` | 2 | 0 | 0 | 0 | 173 | 55 | #3A2820×1、#5A3828×1 |
| `en/essay-ming-maritime-ban.html` | 2 | 0 | 0 | 0 | 173 | 55 | #3A2820×1、#5A3828×1 |
| `en/essay-ming-metaphor.html` | 2 | 0 | 0 | 0 | 173 | 55 | #3A2820×1、#5A3828×1 |
| `en/essay-ming-military.html` | 2 | 0 | 0 | 0 | 173 | 55 | #3A2820×1、#5A3828×1 |
| `en/essay-ming-politics.html` | 2 | 0 | 0 | 0 | 173 | 55 | #3A2820×1、#5A3828×1 |
| `en/essay-ming-religion.html` | 2 | 0 | 0 | 0 | 173 | 55 | #3A2820×1、#5A3828×1 |
| `en/essay-ming-social-customs.html` | 2 | 0 | 0 | 0 | 173 | 55 | #3A2820×1、#5A3828×1 |
| `en/essay-modern-management.html` | 2 | 0 | 0 | 0 | 173 | 55 | #3A2820×1、#5A3828×1 |
| `en/essay-original-poetry.html` | 2 | 0 | 0 | 0 | 173 | 55 | #3A2820×1、#5A3828×1 |
| `en/essay-poetry-imagery.html` | 2 | 0 | 0 | 0 | 173 | 55 | #3A2820×1、#5A3828×1 |
| `en/essay-poetry-opening.html` | 2 | 0 | 0 | 0 | 173 | 55 | #3A2820×1、#5A3828×1 |
| `en/essay-quanzhen-daoism.html` | 2 | 0 | 0 | 0 | 173 | 55 | #3A2820×1、#5A3828×1 |
| `en/essay-rhythm-analysis.html` | 2 | 0 | 0 | 0 | 173 | 55 | #3A2820×1、#5A3828×1 |
| `en/essay-scenery-poems.html` | 2 | 0 | 0 | 0 | 173 | 55 | #3A2820×1、#5A3828×1 |
| `en/essay-thematic-poetry.html` | 2 | 0 | 0 | 0 | 173 | 55 | #3A2820×1、#5A3828×1 |
| `en/essay-three-teachings.html` | 2 | 0 | 0 | 0 | 173 | 55 | #3A2820×1、#5A3828×1 |
| `en/essay-version-evolution.html` | 2 | 0 | 0 | 0 | 173 | 55 | #3A2820×1、#5A3828×1 |
| `en/essay-zen-koan-vs-neidan.html` | 2 | 0 | 0 | 0 | 173 | 55 | #3A2820×1、#5A3828×1 |
| `en/ethics-consumption.html` | 6 | 2 | 0 | 9 | 173 | 44 | #C8463A×3、#D97706×2、#B88C2A×2 |
| `en/famous-time-travel.html` | 1 | 1 | 0 | 0 | 173 | 44 | #3A2820×1、#C8463A×1 |
| `en/four-dimensional-research-network.html` | 0 | 1 | 0 | 65 | 173 | 44 | #6B6455×17、#2C2416×10、#C89B3C×9 |
| `en/four-heavenly-kings-artifacts.html` | 1 | 1 | 0 | 25 | 173 | 44 | #8A7A6A×6、#C8463A×4、#8B7355×4 |
| `en/game-webnovel.html` | 1 | 4 | 0 | 35 | 173 | 44 | #D4AF37×5、#3A6B8C×5、#C9A063×5 |
| `en/global-pattern.html` | 1 | 3 | 0 | 16 | 173 | 44 | #C8463A×4、#6B6455×4、#C9A063×2 |
| `en/graph-explorer.html` | 12 | 11 | 0 | 49 | 173 | 49 | #9A8F7C×7、#8A7D68×6、#D4A017×5 |
| `en/guanyin-six-roles-network.html` | 0 | 1 | 0 | 46 | 173 | 44 | #C8463A×11、#8A7A6A×11、#8B7355×8 |
| `en/guide.html` | 2 | 0 | 0 | 0 | 173 | 55 | #3A2820×1、#5A3828×1 |
| `en/hardship-difficulty-heatmap.html` | 0 | 8 | 0 | 25 | 173 | 44 | #E9B885×9、#C8463A×4、#D4C4A8×3 |
| `en/hardship-heatmap.html` | 2 | 4 | 0 | 20 | 173 | 44 | #6B6455×6、#C8463A×5、#E9B885×4 |
| `en/heaven-power-network.html` | 1 | 1 | 0 | 89 | 173 | 44 | #C8463A×18、#8A7C6A×14、#C9A961×10 |
| `en/index.html` | 2 | 0 | 0 | 0 | 173 | 55 | #3A2820×1、#5A3828×1 |
| `en/intertextuality-network.html` | 0 | 1 | 0 | 91 | 173 | 44 | #8B4513×22、#8A7A5A×18、#5A3828×8 |
| `en/journey-geo-semiotics.html` | 0 | 1 | 0 | 10 | 173 | 44 | #C8463A×3、#D4AF37×2、#3A6B8C×2 |
| `en/journey-map-interactive.html` | 4 | 9 | 0 | 22 | 173 | 44 | #C9A063×5、#6B8E5A×5、#C8463A×4 |
| `en/journey-route.html` | 1 | 1 | 0 | 17 | 173 | 44 | #E9B885×4、#C8463A×3、#6B8E5A×2 |
| `en/journey-spacetime.html` | 0 | 5 | 0 | 14 | 173 | 44 | #E9B885×5、#C8463A×5、#C9A063×3 |
| `en/jurisprudence.html` | 1 | 19 | 0 | 56 | 173 | 44 | #C8463A×21、#C9A063×13、#E9B885×11 |
| `en/karma-reincarnation.html` | 1 | 2 | 0 | 66 | 173 | 44 | #C8463A×12、#C9A063×9、#3A6B8C×8 |
| `en/language-style-radar.html` | 0 | 4 | 0 | 21 | 173 | 44 | #2C3E50×6、#C9A063×5、#D9CDB8×4 |
| `en/linguistics.html` | 0 | 1 | 0 | 32 | 173 | 44 | #23201A×11、#E8DDC8×5、#C8463A×4 |
| `en/magic-system.html` | 3 | 6 | 0 | 18 | 173 | 44 | #C8463A×7、#D4A857×6、#3A6B8C×4 |
| `en/material-archaeology.html` | 1 | 1 | 0 | 38 | 173 | 44 | #C8463A×9、#3A6B8C×8、#C9A063×7 |
| `en/mbti-evolution.html` | 0 | 4 | 0 | 9 | 173 | 44 | #E9B885×4、#C8463A×3、#3A6B8C×2 |
| `en/methodology-matrix.html` | 8 | 5 | 0 | 11 | 173 | 44 | #E9B885×4、#C8463A×4、#6B8E5A×2 |
| `en/methodology.html` | 2 | 0 | 0 | 0 | 173 | 55 | #3A2820×1、#5A3828×1 |
| `en/ming-political-thought-comparison.html` | 0 | 13 | 0 | 51 | 173 | 44 | #E9B885×10、#C8463A×9、#C9A063×9 |
| `en/monster-background.html` | 2 | 6 | 0 | 26 | 173 | 44 | #6B6455×8、#C8463A×6、#C9A063×5 |
| `en/monster-capability-radar.html` | 0 | 10 | 0 | 55 | 173 | 44 | #E9B885×10、#C8463A×9、#C9A063×8 |
| `en/monster-ecology-network.html` | 0 | 8 | 0 | 27 | 173 | 44 | #C8463A×7、#C9A063×7、#23201A×6 |
| `en/monster-female-network.html` | 0 | 1 | 0 | 96 | 173 | 44 | #8A7A5A×12、#8B4513×10、#5A3828×8 |
| `en/monster-hierarchy-network.html` | 0 | 1 | 0 | 81 | 173 | 44 | #8B3A2A×17、#8A7C6A×16、#6B8E6F×14 |
| `en/monster-sociology.html` | 0 | 12 | 0 | 45 | 173 | 44 | #C8463A×8、#3A6B8C×6、#C9A063×6 |
| `en/monster-victims-network.html` | 0 | 1 | 0 | 49 | 173 | 44 | #8A7A6A×11、#C8463A×10、#8B7355×7 |
| `en/music-structure.html` | 0 | 1 | 0 | 35 | 173 | 44 | #6B6455×8、#C8463A×5、#3A6B8C×4 |
| `en/narrative-experiment.html` | 4 | 11 | 0 | 55 | 173 | 44 | #C8463A×17、#3A6B8C×16、#C9A063×15 |
| `en/narrative-rhythm-curve.html` | 2 | 9 | 0 | 20 | 173 | 44 | #C8463A×7、#2C3E50×7、#C9A063×6 |
| `en/narratology-12d-network.html` | 0 | 1 | 0 | 100 | 173 | 44 | #8A7A5A×19、#8B4513×16、#5A3828×12 |
| `en/narratology-16d-network.html` | 0 | 1 | 0 | 128 | 173 | 44 | #8A7A5A×21、#8B4513×13、#4A6B8A×11 |
| `en/perf-canvas-rendering.html` | 1 | 1 | 0 | 7 | 173 | 44 | #C8463A×2、#F5F0E6×1、#8B4513×1 |
| `en/philosophy.html` | 0 | 8 | 0 | 39 | 173 | 44 | #C8463A×10、#C9A063×7、#E9B885×4 |
| `en/pilgrim-team-dynamic-network.html` | 1 | 1 | 0 | 20 | 173 | 44 | #C8463A×4、#D9CDB8×4、#6B8E5A×3 |
| `en/pilgrim-team-psychology-arc.html` | 0 | 15 | 0 | 38 | 173 | 44 | #E9B885×12、#C9A063×10、#C8463A×7 |
| `en/poetry-rhythm-analysis.html` | 0 | 10 | 0 | 41 | 173 | 44 | #E9B885×11、#C8463A×9、#C9A063×9 |
| `en/power-resources.html` | 0 | 1 | 0 | 30 | 173 | 44 | #3A6B8C×7、#C8463A×5、#C9A063×5 |
| `en/relationships.html` | 0 | 8 | 0 | 77 | 173 | 44 | #3A6B8C×20、#C8463A×16、#6B6455×7 |
| `en/risk-project.html` | 7 | 12 | 0 | 46 | 173 | 44 | #C8463A×16、#3A6B8C×6、#E9B885×5 |
| `en/search.html` | 1 | 0 | 0 | 0 | 173 | 48 | #3A2820×1 |
| `en/site-map.html` | 2 | 0 | 0 | 0 | 173 | 55 | #3A2820×1、#5A3828×1 |
| `en/six-senses-narratology-network.html` | 0 | 1 | 0 | 53 | 173 | 44 | #8B4513×17、#8A7A5A×12、#D4C5A9×6 |
| `en/social-media.html` | 1 | 1 | 0 | 39 | 173 | 45 | #C8463A×8、#C9A063×7、#3A6B8C×6 |
| `en/tag-cloud.html` | 7 | 7 | 0 | 6 | 173 | 44 | #C8463A×3、#D9C9A8×2、#F0C878×2 |
| `en/text-evolution.html` | 0 | 1 | 0 | 27 | 173 | 44 | #6B6455×6、#C8463A×5、#3A6B8C×3 |
| `en/text-search.html` | 0 | 1 | 0 | 0 | 173 | 44 | #C8463A×1 |
| `en/theological-intervention-network.html` | 0 | 1 | 0 | 45 | 173 | 44 | #1E3A8A×12、#A83232×7、#C9B896×6 |
| `en/timeline.html` | 0 | 1 | 0 | 11 | 173 | 44 | #C8463A×3、#C9A063×2、#3A6B8C×2 |
| `en/tribulations.html` | 6 | 0 | 0 | 0 | 173 | 55 | #3A2820×1、#5A3828×1、#F0E9DA×1 |
| `en/underworld-power-network.html` | 0 | 1 | 0 | 86 | 173 | 44 | #C8463A×17、#8A7C6A×14、#3A6B8C×12 |
| `en/visual-art.html` | 3 | 8 | 0 | 37 | 173 | 44 | #D4AF37×14、#C8463A×7、#E9B885×6 |
| `en/visualizations.html` | 2 | 0 | 0 | 0 | 173 | 55 | #3A2820×1、#5A3828×1 |
| `en/workplace.html` | 0 | 3 | 0 | 19 | 173 | 44 | #C8463A×7、#E9B885×3、#C9A063×3 |
| `guide.html` | 0 | 0 | 0 | 0 | 0 | 0 | — |
| `index.html` | 4 | 0 | 0 | 2 | 0 | 0 | #221D16×2、#F2EBDC×2、#FAF7F0×1 |
| `reader/ch001.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch002.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch003.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch004.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch005.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch006.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch007.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch008.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch009.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch010.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch011.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch012.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch013.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch014.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch015.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch016.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch017.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch018.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch019.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch020.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch021.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch022.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch023.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch024.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch025.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch026.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch027.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch028.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch029.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch030.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch031.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch032.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch033.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch034.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch035.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch036.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch037.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch038.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch039.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch040.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch041.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch042.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch043.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch044.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch045.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch046.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch047.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch048.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch049.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch050.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch051.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch052.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch053.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch054.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch055.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch056.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch057.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch058.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch059.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch060.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch061.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch062.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch063.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch064.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch065.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch066.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch067.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch068.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch069.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch070.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch071.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch072.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch073.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch074.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch075.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch076.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch077.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch078.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch079.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch080.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch081.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch082.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch083.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch084.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch085.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch086.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch087.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch088.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch089.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch090.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch091.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch092.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch093.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch094.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch095.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch096.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch097.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch098.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch099.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/ch100.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/index.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/themes-hub.html` | 0 | 0 | 0 | 0 | 173 | 44 | — |
| `reader/themes/index.html` | 3 | 0 | 0 | 0 | 0 | 0 | #FAF7F0×1、#23201A×1、#C8463A×1 |
| `rum-viewer.html` | 15 | 0 | 0 | 0 | 0 | 0 | #6B6B6B×4、#E8E0D2×3、#3A2820×2 |

## 4. 不可替换项（分类统计与处理口径）

**定义面（15166 处）** — 令牌定义本身（改它＝改令牌取值·须走令牌批）

  色值分布：#7FA8C9×992、#C8463A×724、#3A6B8C×724、#6B8E5A×714、#221D16×662、#C9A96B×662

**共享副本消费（57090 处）** — 共享层（tokens.css/system.css 的拷贝）⇒ 级联全部内联页·须连传播同批做

  色值分布：#B78D6A×990、#C88479×990、#C5857C×990、#7D99A9×660、#BE8880×660、#D87C6E×660

**SVG属性位（0 处）** — var() 在表现属性里不生效⇒须改写成 style="fill:var(--chart-N)"

**JS字面量（5041 处）** — SVG/Canvas 属性位不解析 var()⇒须读 getComputedStyle 喂图表或改配置驱动

  色值分布：#C8463A×633、#3A6B8C×477、#C9A063×380、#6B8E5A×291、#6B6455×225、#8A7A5A×164

**标记文本（312 处）** — 文本/非样式属性·逐处判定

  色值分布：#FAF7F0×166、#FAF7F2×53、#23201A×16、#C9A063×11、#6B8E5A×11、#C8463A×9


## 4b. B2 专项（结构与回目 10 页）·逐页明细

| 页 | 分类 | 处数 | 色值分布（该分类内） |
|:--|:--|--:|:--|
| `data/81-hardships-view.html` | 页内私有消费 | 1 | #3A2820×1 |
| `data/81-hardships-view.html` | JS字面量 | 24 | #C8463A×5、#D9CDB8×5、#6B6455×4、#FAF7F2×3、#3A6B8C×2、#C9A063×1 |
| `data/81-hardships-view.html` | 共享副本消费 | 173 | #B78D6A×3、#C88479×3、#C5857C×3、#7D99A9×2、#BE8880×2、#D87C6E×2 |
| `data/81-hardships-view.html` | 定义面 | 48 | #C8463A×3、#3A6B8C×3、#7FA8C9×3、#221D16×2、#F2EBDC×2、#8A6D3B×2 |
| `data/81-hardships.html` | 内联样式消费 | 1 | #C8463A×1 |
| `data/81-hardships.html` | JS字面量 | 9 | #C8463A×3、#3A6B8C×2、#6B8E5A×2、#C9A063×1、#E9B885×1 |
| `data/81-hardships.html` | 共享副本消费 | 173 | #B78D6A×3、#C88479×3、#C5857C×3、#7D99A9×2、#BE8880×2、#D87C6E×2 |
| `data/81-hardships.html` | 定义面 | 44 | #7FA8C9×3、#221D16×2、#F2EBDC×2、#C8463A×2、#3A6B8C×2、#8A6D3B×2 |
| `data/81-hardships.html` | 标记文本 | 1 | #FAF7F0×1 |
| `data/chapter-stats.html` | 内联样式消费 | 5 | #C8463A×2、#3A6B8C×1、#E9B885×1、#6B8E5A×1 |
| `data/chapter-stats.html` | JS字面量 | 4 | #3A6B8C×1、#E9B885×1、#C8463A×1、#6B8E5A×1 |
| `data/chapter-stats.html` | 共享副本消费 | 173 | #B78D6A×3、#C88479×3、#C5857C×3、#7D99A9×2、#BE8880×2、#D87C6E×2 |
| `data/chapter-stats.html` | 定义面 | 44 | #7FA8C9×3、#221D16×2、#F2EBDC×2、#C8463A×2、#3A6B8C×2、#8A6D3B×2 |
| `data/chapter-stats.html` | 标记文本 | 1 | #FAF7F0×1 |
| `data/chapter-structure-graph.html` | 内联样式消费 | 5 | #C8463A×1、#FFF5E6×1、#F4D4B2×1、#C9A063×1、#8C3A0A×1 |
| `data/chapter-structure-graph.html` | JS字面量 | 25 | #2C3E50×9、#C9A063×4、#6B8E5A×2、#6B7C8C×2、#8C6E3A×1、#3A6B8C×1 |
| `data/chapter-structure-graph.html` | 共享副本消费 | 173 | #B78D6A×3、#C88479×3、#C5857C×3、#7D99A9×2、#BE8880×2、#D87C6E×2 |
| `data/chapter-structure-graph.html` | 定义面 | 44 | #7FA8C9×3、#221D16×2、#F2EBDC×2、#C8463A×2、#3A6B8C×2、#8A6D3B×2 |
| `data/chapter-structure-graph.html` | 标记文本 | 1 | #FAF7F0×1 |
| `data/hardship-difficulty-heatmap.html` | 页内私有消费 | 2 | #FFF5E6×1、#F4D4B2×1 |
| `data/hardship-difficulty-heatmap.html` | 内联样式消费 | 8 | #E9B885×5、#C8463A×1、#FFF8E7×1、#D4C4A8×1 |
| `data/hardship-difficulty-heatmap.html` | JS字面量 | 16 | #E9B885×3、#7A9C5A×2、#D98060×2、#8C2A2A×2、#C8463A×2、#D4C4A8×2 |
| `data/hardship-difficulty-heatmap.html` | 共享副本消费 | 173 | #B78D6A×3、#C88479×3、#C5857C×3、#7D99A9×2、#BE8880×2、#D87C6E×2 |
| `data/hardship-difficulty-heatmap.html` | 定义面 | 44 | #7FA8C9×3、#221D16×2、#F2EBDC×2、#C8463A×2、#3A6B8C×2、#8A6D3B×2 |
| `data/hardship-difficulty-heatmap.html` | 标记文本 | 1 | #FAF7F0×1 |
| `data/hardship-heatmap.html` | 页内私有消费 | 2 | #C8463A×1、#8C2A2A×1 |
| `data/hardship-heatmap.html` | 内联样式消费 | 4 | #E9B885×3、#C8463A×1 |
| `data/hardship-heatmap.html` | JS字面量 | 9 | #C8463A×2、#3A6B8C×1、#C9A063×1、#6B8E5A×1、#F5E9D4×1、#E9B885×1 |
| `data/hardship-heatmap.html` | 共享副本消费 | 173 | #B78D6A×3、#C88479×3、#C5857C×3、#7D99A9×2、#BE8880×2、#D87C6E×2 |
| `data/hardship-heatmap.html` | 定义面 | 44 | #7FA8C9×3、#221D16×2、#F2EBDC×2、#C8463A×2、#3A6B8C×2、#8A6D3B×2 |
| `data/hardship-heatmap.html` | 标记文本 | 1 | #FAF7F0×1 |
| `data/methodology-matrix.html` | 页内私有消费 | 8 | #3A2820×1、#5A3828×1、#D4A78F×1、#8A7A6A×1、#6B8E5A×1、#F0F5E8×1 |
| `data/methodology-matrix.html` | 内联样式消费 | 5 | #E9B885×4、#C8463A×1 |
| `data/methodology-matrix.html` | JS字面量 | 11 | #C8463A×3、#7A3A8C×2、#3A6B8C×2、#C9A063×2、#D97706×1、#6B8E5A×1 |
| `data/methodology-matrix.html` | 共享副本消费 | 173 | #B78D6A×3、#C88479×3、#C5857C×3、#7D99A9×2、#BE8880×2、#D87C6E×2 |
| `data/methodology-matrix.html` | 定义面 | 44 | #7FA8C9×3、#221D16×2、#F2EBDC×2、#C8463A×2、#3A6B8C×2、#8A6D3B×2 |
| `data/methodology-matrix.html` | 标记文本 | 1 | #FAF7F0×1 |
| `data/relationships.html` | 内联样式消费 | 8 | #FDFAF4×4、#C8463A×2、#3A6B8C×1、#6B6455×1 |
| `data/relationships.html` | JS字面量 | 69 | #3A6B8C×19、#C8463A×14、#6B8E5A×7、#C9A063×6、#9C6B3A×5、#E9B885×3 |
| `data/relationships.html` | 共享副本消费 | 173 | #B78D6A×3、#C88479×3、#C5857C×3、#7D99A9×2、#BE8880×2、#D87C6E×2 |
| `data/relationships.html` | 定义面 | 44 | #7FA8C9×3、#221D16×2、#F2EBDC×2、#C8463A×2、#3A6B8C×2、#8A6D3B×2 |
| `data/relationships.html` | 标记文本 | 1 | #FAF7F0×1 |
| `data/story-timeline.html` | 内联样式消费 | 1 | #C8463A×1 |
| `data/story-timeline.html` | JS字面量 | 5 | #C8463A×1、#3A6B8C×1、#C9A063×1、#6B8E5A×1、#8A6D3B×1 |
| `data/story-timeline.html` | 共享副本消费 | 173 | #B78D6A×3、#C88479×3、#C5857C×3、#7D99A9×2、#BE8880×2、#D87C6E×2 |
| `data/story-timeline.html` | 定义面 | 44 | #7FA8C9×3、#221D16×2、#F2EBDC×2、#C8463A×2、#3A6B8C×2、#8A6D3B×2 |
| `data/story-timeline.html` | 标记文本 | 1 | #FAF7F0×1 |
| `data/timeline.html` | 内联样式消费 | 1 | #C8463A×1 |
| `data/timeline.html` | JS字面量 | 11 | #C8463A×2、#C9A063×2、#3A6B8C×2、#6B6455×2、#8C2A2A×1、#6B8E5A×1 |
| `data/timeline.html` | 共享副本消费 | 173 | #B78D6A×3、#C88479×3、#C5857C×3、#7D99A9×2、#BE8880×2、#D87C6E×2 |
| `data/timeline.html` | 定义面 | 44 | #7FA8C9×3、#221D16×2、#F2EBDC×2、#C8463A×2、#3A6B8C×2、#8A6D3B×2 |
| `data/timeline.html` | 标记文本 | 1 | #FAF7F0×1 |

> B2 判定小结：① 十页的**页内私有 CSS 消费面**共 13 处、**内联样式**共 38 处 ⇒ 可逐页消费的量很小；② 十页的硬编码色主体在 **JS 字面量**（共 183 处）⇒ `var()` 在 SVG/Canvas 属性位不生效 ⇒ 需工程化或改配置驱动；③ 十页容器**全部已是 `var(--container-wide)`** ⇒ 无容器归并对象；④ `--chart-3` / `--chart-5` 的**硬编码消费面为空** ⇒ defer「暗色 chart 新增」不触发。


## 5. 令牌消费面（defer 项判定用）

| 令牌 | 消费页数 | 消费页（前 8） |
|:--|--:|:--|
| `--accent` | 178 | `404.html`、`_template.html`、`dashboard.html`、`data/81-hardships-view.html`、`data/81-hardships.html`、`data/_shell.html`、`data/aesthetics.html`、`data/ai-dialogue.html` |
| `--chart-1` | 178 | `404.html`、`_template.html`、`dashboard.html`、`data/81-hardships-view.html`、`data/81-hardships.html`、`data/_shell.html`、`data/aesthetics.html`、`data/ai-dialogue.html` |
| `--accent-2` | 144 | `_template.html`、`dashboard.html`、`data/81-hardships-view.html`、`data/81-hardships.html`、`data/aesthetics.html`、`data/business-model.html`、`data/cave-estate.html`、`data/chapter-stats.html` |
| `--chart-2` | 144 | `_template.html`、`dashboard.html`、`data/81-hardships-view.html`、`data/81-hardships.html`、`data/aesthetics.html`、`data/business-model.html`、`data/cave-estate.html`、`data/chapter-stats.html` |
| `--accent-4` | 118 | `_template.html`、`dashboard.html`、`data/81-hardships-view.html`、`data/81-hardships.html`、`data/aesthetics.html`、`data/business-model.html`、`data/chapter-stats.html`、`data/chapter-structure-graph.html` |
| `--chart-4` | 118 | `_template.html`、`dashboard.html`、`data/81-hardships-view.html`、`data/81-hardships.html`、`data/aesthetics.html`、`data/business-model.html`、`data/chapter-stats.html`、`data/chapter-structure-graph.html` |
| `--accent-soft` | 83 | `data/81-hardships.html`、`data/aesthetics.html`、`data/business-model.html`、`data/cave-estate.html`、`data/chapter-stats.html`、`data/character-appearance.html`、`data/chart-design.html`、`data/cognitive-psychology.html` |
| `--ink-soft` | 69 | `404.html`、`data/81-hardships-view.html`、`data/character-relationship-3d-view.html`、`data/chart-design.html`、`data/counterfactual.html`、`data/data-explorer.html`、`data/deconstruction.html`、`data/dialogue-sentiment.html` |
| `--ink` | 67 | `404.html`、`data/81-hardships-view.html`、`data/character-appearance.html`、`data/character-relationship-3d-view.html`、`data/character-semantic-network.html`、`data/cultural-misreading.html`、`data/data-explorer.html`、`data/deconstruction.html` |
| `--rebel` | 36 | `data/81-hardships-view.html`、`data/chapter-structure-graph.html`、`data/character-dynamic-network.html`、`data/character-relationship-3d-view.html`、`data/character-relationship-3d.html`、`data/concept-device.html`、`data/criticism-history.html`、`data/data-explorer.html` |
| `--accent-3` | 6 | `_template.html`、`data/chart-design.html`、`data/game-webnovel.html`、`data/story-timeline.html`、`en/chart-design.html`、`en/game-webnovel.html` |
| `--chart-6` | 6 | `_template.html`、`data/chart-design.html`、`data/game-webnovel.html`、`data/story-timeline.html`、`en/chart-design.html`、`en/game-webnovel.html` |
| `--paper` | 5 | `404.html`、`data/concept-device.html`、`dukou-engine.html`、`en/concept-device.html`、`en/criticism-history.html` |
| `--bg` | 3 | `dashboard.html`、`index.html`、`reader/themes/index.html` |
| `--chart-5` | 2 | `_template.html`、`dashboard.html` |
| `--dark-text` | 2 | `data/journey-geo-3d.html`、`index.html` |
| `--info` | 2 | `data/graph-explorer.html`、`en/graph-explorer.html` |
| `--paper-warm` | 2 | `404.html`、`dukou-engine.html` |
| `--dark` | 1 | `index.html` |

> **defer「暗色 `--chart-3` / `--chart-5` 新增」判定**：`--chart-3` / `--chart-5` 的**硬编码消费面为空**（全站无任何页面以 `var(--chart-3)` / `var(--chart-5)` 消费）⇒ 本批**不触发**纯加法；两者的硬编码值目前只存在于**令牌定义与 JS 字面量**中 ⇒ 治理路径是「JS 侧令牌化」而非「补令牌」。


---

*本件为盘点产物（只读统计·未改动任何页面）·复算命令：`python scripts/_w1078_color_inventory.py`*
