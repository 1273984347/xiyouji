# Journey to the West · Annotated — English Edition (W383)

> i18n internationalization subproject of the main **Journey to the West · Annotated** project.
> Version: v2.3.11 · W383 · 2026-08-07

## Overview

`site/en/` is the English-language subset of the main site at `site/`. It provides a curated entry point for non-Chinese readers: a landing page, a simplified data dashboard, a selected academic papers index, four data pages (the 81 tribulations, the pilgrims, the bestiary, and a 100-chapter map), thirty-six long-form essays in summary-translation form, five deep-dive character studies, a methodology reading-guide, a site map, and an English tour of all 85 visualizations. The full Chinese site remains the canonical edition; the English pages link back to it through Chinese↔English switch links.

This subproject was created in W234-E4 (v2.2.40) as part of the AVES (Academic / Visualization / Essay / Site) fourth-direction batch. It was expanded in W345 (v2.2.95) with three new essays (E4–E6) drawn from the W344 quality-enhancement A5/A6 articles, growing the subset from 7 to 10 files. It was further expanded in W347 (v2.2.98) with four data pages (TRIBULATIONS · PILGRIMS · BESTIARY · CHAPTER-MAP) bridging the project's own datasets (81-hardships, pilgrim-team-*, monster-*, chapters-metadata), growing the subset from 10 to 14 files. It was expanded again in W348 (v2.2.99) with three scholarship essays (E7–E9: historical vs. fictional Xuanzang, Heaven as a Ming bureaucracy, the hundred chapter-couplets), a visualization tour (85 pages in eight clusters), a deep-dive on Sun Wukong, and a methodology reading-guide — growing the subset from 14 to 20 files. It was expanded once more in W349 (v2.3.0) with three pilgrim deep-dives (Tang Sanzang, Zhu Bajie, Sha Wujing) and an essay on Quanzhen Daoism (E10) reading the novel's allegorical layer as a Daoist inner-alchemy manual — growing the subset from 20 to 24 files. It was expanded in W350 (v2.3.1) with the fifth pilgrim deep-dive (Ao Lie, the White Dragon Horse) completing the five-pilgrim set, plus two religion essays — Chan Buddhism (E11) and popular religion (E12) — reading the novel's allegorical layer as a Buddhist mind-cultivation tale beneath a folk-religious substrate, growing the subset from 24 to 27 files. It was expanded in W351 (v2.3.2) with three culture essays (E13 the making of the novel, E14 the Ming in disguise, E15 three-teachings synthesis) and a Site Map indexing every English page by cluster — growing the subset from 27 to 31 files. It was expanded in W352 (v2.3.3) with four A6 lyric-meter (cipai) essays (E16 Xijiangyue, E17 Linjiangxian, E18 Mantingfang, E19 Shuidiaogetou) reading the novel's poetry through four theorists and four lyric realms — growing the subset from 31 to 35 files. It was expanded in W353 (v2.3.4) with four A5 Ming-institution essays (E20 the imperial exam, E21 the weisuo garrison, E22 the maritime ban, E23 three-realm justice) reading the novel's politics through Huang Rensong, Elman, Miyazaki, Weber, Gu Cheng, Yu Zhijia, Peng Yong, Fan Shuzhi, Li Qing, Timothy Brook, Qu Tongzu, Shiga Shūzō, and Terada Hiroaki — growing the subset from 35 to 39 files. It was expanded in W354 (v2.3.5) with four more A5 Ming-institution essays (E24 the Ming court, E25 the heavenly ledger, E26 the wei-so army, E27 ordination by decree), extending the "Ming mirror" series to politics, economy, military, and religion — growing the subset from 39 to 43 files. It was expanded in W355 (v2.3.6) with three A5 Ming-thought essays (E28 customs as governance, E29 from archaism to xinling, E30 the mind as cosmos), completing the eight-layer "Ming mirror" across politics, economy, deities, judiciary, military, exam, religion, and intellectual history — growing the subset from 43 to 46 files. It was expanded in W356 (v2.3.7) with two A6 poetry essays (E31 the opening verse as "constitutional" poetics, E33 the imagery lineage of stone·peach·bone·sutra through Pound, Eliot, Bachelard, and Liu Xie) — growing the subset from 46 to 48 files. Note: scenery-poem classification (the third A6 item) was already covered earlier by E6 "Original Scenery Poems," so no duplicate was produced.

## File list (51 files)

All files live under `d:\1\xiyouji\site\en\`.

| # | File | Lines | Purpose |
|---|---|---|---|
| 1 | `index.html` | ~470 | English landing page. Title "Journey to the West · Annotated", subtitle "A hybrid reading project". Forty-six entry cards (dashboard / academic papers / 4 data pages / 32 essays / 5 deep-dives / 2 guides / visualization tour / site map). |
| 2 | `dashboard.html` | ~370 | English data dashboard. Five core KPI cards (100 chapters / 60 character analyses / 91 theme essays / 68 visualizations / 55 academic papers). |
| 3 | `academic-papers.html` | ~210 | Academic papers index. Ten representative entries selected from the 55-entry bibliography. Columns: ID / Author / Year / Title / Journal / Topic. |
| 4 | `essay-ai-era.html` | ~250 | Summary translation of `docs/06-个人随笔/西游与AI时代.md`. Five paragraphs: Subhuti · headband · mirror test · 81 tribulations · Mind Monkey. |
| 5 | `essay-information-cocoon.html` | ~240 | Summary translation of `docs/06-个人随笔/西游与信息茧房.md`. Six paragraphs: Tathagata's palm · Tang Seng's map · Bajie's bias · Wukong's immunity · Ming vs algorithmic · larger cocoon. |
| 6 | `essay-modern-management.html` | ~250 | Summary translation of `docs/06-个人随笔/西游与现代组织管理.md`. Six paragraphs: Tang Seng middle manager · Wukong senior IC · Bajie valve · Sha Seng adhesive · Jade Emperor CEO · demon backings. |
| 7 | `essay-zen-koan-vs-neidan.html` | ~265 | Summary translation of `docs/04-文化与历史背景/西游与禅宗公案专题.md`. Four sections: one Wukong two readings · Chan koan · Neidan chart · tension · conclusion. |
| 8 | `essay-version-evolution.html` | ~270 | Summary translation of `docs/04-文化与历史背景/版本演变补遗-平话层.md`. Five sections: folded 400 years · zaju layer · pinghua layer (conjectural) · abridged layer · stratified riverbed. |
| 9 | `essay-scenery-poems.html` | ~265 | Summary translation of `docs/05-诗词歌赋/原著景物诗分类赏析专题.md`. Four sections: typology · wonder-landscape · wayfaring · chan-sacred · conclusion. |
| 10 | `tribulations.html` | ~360 | Data page bridging `dataset/81-hardships.json`: cause / outcome / resolution axes as bar charts, a cause×outcome matrix, and the full 81-row calamity ledger. |
| 11 | `characters.html` | ~155 | Data page on the five pilgrims, scored with Belbin team roles and a 5-dimension psychology profile; cohesion milestones table. |
| 12 | `bestiary.html` | ~140 | Data page on the demon ecology: KPI cards, four social tiers, by-type/origin/fate tables, capability extremes. |
| 13 | `chapters-map.html` | ~245 | Data page mapping all 100 chapters into four arcs with each chapter's couplet, key figures, and localities. |
| 14 | `essay-composition-origins.html` | ~310 | Summary translation of `docs/04-文化与历史背景/成书背景.md`. The making of the novel: authorship puzzle (Wu Cheng'en c.1500–1582, Zhuang Peiheng's doubts, Qiu Chuji / Huayang Grotto / collective-accumulation candidates), version lineage (Song shihua / Yuan zaju / 1592 Shide tang / Qing Zhengdao & Zhenquan / 1955 PLA), historical vs. fictional Xuanzang, the Ming world. |
| 15 | `essay-ming-metaphor.html` | ~300 | Summary translation of `docs/04-文化与历史背景/明代隐喻.md`. Six metaphor dimensions: officialdom (Bimawen = Imperial Stables, rank 4; Heaven's nine ranks = the court), patronage-persecution (demon-backing table), commercial economy & the vernacular novel, religious politics (Jiajing Daoism / Chechi kingdom / Heaven-Thunderclap balance), demon-bureaucrat identity overlap. |
| 16 | `essay-three-teachings.html` | ~310 | Summary translation of `docs/04-文化与历史背景/佛道思想.md`. Three-teachings syncretism: Buddhism (81 tribulations as stages, mind-monkey/will-horse, Tathagata-Guanyin-Maitreya, five skandhas → five pilgrims table), Daoism (Subodhi = heart, Metal-Sire/Wood-Mother/Yellow-Dame inner alchemy, Quanzhen Zhengdao), Confucianism (master-disciple = lord-son). |
| 17 | `site-map.html` | ~230 | Navigation capstone for the English edition: all 46 English pages indexed into seven clusters (Start Here / Data / Culture essays / Poetry essays / Contemporary essays / Characters / Visualizations), with a "how to use" note and links to the Chinese site. |
| 18 | `README.md` | (this file) | i18n English-site documentation. |
| 15 | `essay-historical-xuanzang.html` | ~290 | Summary translation of `docs/04-文化与历史背景/历史玄奘与小说玄奘专题.md`. Seven-dimension comparison of the historical vs. fictional Xuanzang; pilgrimage facts (138 kingdoms, 657 scrolls, 1,335 juan); Ming projections. |
| 16 | `essay-divine-bureaucracy.html` | ~260 | Summary translation of `docs/04-文化与历史背景/明代神祇官僚体系对照专题.md`. Heaven as Ming bureaucracy; three features; four theorists (Huang / Qian Mu / Weber / Feuchtwang); four deity groups; the "demon-revealing mirror". |
| 17 | `essay-chapter-couplets.html` | ~250 | Summary translation of `docs/05-诗词歌赋/回目对联分析专题.md`. Three coordinates; prosody (7+7 couplets); five types; structure stats (100% / 85% / 70%); narrative function. |
| 18 | `visualizations.html` | ~520 | English gallery + reading guide of the ~85 interactive D3.js pages under `site/data/`, grouped into eight analytical clusters with per-page descriptions and live links. |
| 19 | `character-wukong.html` | ~300 | Deep-dive portrait of Sun Wukong: identities, stone birth, mind / 72 transformations, rebellion, the 13,500-jin staff, the mind-monkey, reception; cross-links to character visualizations. |
| 20 | `methodology.html` | ~310 | Reading guide to the whole project: hybrid static-first design, content map (A1–A6/S counts), seven-part A4 template, rice-paper design language, dual-index traceability, zero-fabrication data trust. |
| 21 | `character-tangseng.html` | ~290 | Deep-dive portrait of Tang Sanzang: identities, the faithful centre, Belbin Coordinator role, psychology radar (faith over fury), the conflict with Wukong, the arc to Buddha. |
| 22 | `character-bajie.html` | ~270 | Deep-dive portrait of Zhu Bajie: identities (Tianpeng → pig → Altar-Cleaner), the earthy one, Belbin social glue, psychology radar, comic relief. |
| 23 | `character-shaseng.html` | ~260 | Deep-dive portrait of Sha Wujing: identities, the quiet backbone, Belbin Implementer, flat psychology radar, the unshown labour. |
| 24 | `essay-quanzhen-daoism.html` | ~300 | Summary translation of `docs/04-文化与历史背景/西游与道教全真派专题.md`. Quanzhen reading: inner-alchemy codebook (心猿/金公/木母/刀圭), four theorists (Wang/Qiu/Ma/Zhang), four core concepts; the novel as a Daoist cultivation manual. |
| 25 | `character-bailongma.html` | ~270 | Deep-dive portrait of Ao Lie / White Dragon Horse: identities (West Sea prince → steed → Eightfold Heavenly Dragon), the unseen carrier, Belbin Specialist (8)/Implementer (5), flat low-fear high-obedience radar. |
| 26 | `essay-buddhist-chan.html` | ~300 | Summary translation of `docs/04-文化与历史背景/西游与佛教禅宗专题.md`. Chan reading: four theorists (Bodhidharma/Huineng/Shenxiu/Xuanzang), the eight-consciousness cast, four core concepts (seeing nature / sudden-gradual / no-thought / precept-samadhi-wisdom). |
| 27 | `essay-folk-belief.html` | ~290 | Summary translation of `docs/04-文化与历史背景/西游与民间信仰专题.md`. Popular-religion reading: four anthropologists (Yang/Feuchtwang/Wolf/Watson), diffused religion / imperial metaphor / gods-ghosts-ancestors / standardisation. |
| 28 | `essay-cipai-xijiangyue.html` | ~250 | Summary translation of `docs/05-诗词歌赋/西游与西江月词牌赏析专题.md` (W226). Xijiangyue lyric meter (52 chars, two counterparts) as a hidden spine across four nodes (birth / furnace / spell / apotheosis); four theorists (Wang Guowei / Ye Jiaying / Long Yusheng / Xia Chengtao) and four lyric realms with line anchors 522 / 864 / 1393 / 7085. |
| 29 | `essay-cipai-linjiangxian.html` | ~240 | Summary translation of `docs/05-诗词歌赋/西游与临江仙词牌赏析专题.md` (W227). Linjiangxian (60 chars) as the soft reclusive counter-meter; four theorists (Wang / Ye / Long / Tang Guizhang); four realms (created / with-self / no-self / fulfilled) at lines 981 / 2306 / 4432 / 7052. |
| 30 | `essay-cipai-mantingfang.html` | ~245 | Summary translation of `docs/05-诗词歌赋/西游与满庭芳词牌赏析专题.md` (W228). Mantingfang — the only explicitly named cipai in the book (ch. 1, line 39, the woodcutter); four theorists (Wang / Ye / Long / Miao Yue); four realms at lines 39 / 981 / 4792 / 7085. |
| 31 | `essay-cipai-shuidiaogetou.html` | ~245 | Summary translation of `docs/05-诗词歌赋/西游与水调歌头词牌赏析专题.md` (W288). Shuidiaogetou long lyric (95 chars) set beside Su Shi's 1076 lyric; four theorists (Wang / Ye / Long / Miao Yue); four realms (created / tempered / disciplined / fulfilled) and the "meter as Band-Tightening Spell" thesis. |
| 32 | `essay-ming-examination.html` | ~300 | Summary translation of `docs/04-文化与历史背景/明代科举制度对照专题.md` (W150). The scripture quest as Ming civil-service examination: the Buddha's "open exam" (line 981), Xuanzang's nomination (line 1219), the 81 tribulations as evaluation, the gold-list at Ling Mountain (line 7085); four theorists (Huang Rensong / Elman / Miyazaki / Weber). |
| 33 | `essay-ming-garrison.html` | ~290 | Summary translation of `docs/04-文化与历史背景/明代卫所制度对照专题.md` (W293). The heavenly host / dragon palace / lion-camel border as the three Ming weisuo tiers (capital / frontier / local); four line anchors (632 / 700 / 726 / 5484); four historians (Huang / Gu Cheng / Yu Zhijia / Peng Yong). |
| 34 | `essay-ming-maritime-ban.html` | ~290 | Summary translation of `docs/04-文化与历史背景/明代海禁政策对照专题.md` (W292). HuaGuo Mountain as lawless offshore space; the sanctioned voyage as tribute trade; the ban's three phases (Hongwu / Jiajing / Longqing); four line anchors (522 / 996 / 1936 / 7085); four historians (Huang / Fan Shuzhi / Li Qing / Brook). |
| 35 | `essay-ming-judiciary.html` | ~310 | Summary translation of `docs/04-文化与历史背景/明代司法制度深化专题.md` (W142). Four novel cases as a deepened mirror of Ming law: the "quiet criminal" (exile), the repentant king (guilt-edict), the silenced queen (women's law), the forged ledger (corruption); four theorists (Huang / Qu Tongzu / Shiga / Terada). |
| 36 | `essay-ming-politics.html` | ~300 | Summary translation of `docs/04-文化与历史背景/明代政治制度对照专题.md` (W126). The Heavenly Court as the Ming polity: ritualised throne, ossified civil service, princely enfeoffment, law as dead letter; four theorists (Huang Renyu / Qian Mu / Meng Sen / Xie Guozhen); four dimensions (imperial power / bureaucracy / enfeoffment / law) with line anchors 522 / 621 / 864 / 981. |
| 37 | `essay-ming-economy.html` | ~300 | Summary translation of `docs/04-文化与历史背景/明代经济制度对照专题.md` (W130). Heaven's ledger: public finance & taxation, the granary-chief system, economic ethics, the longue durée; four theorists (Huang Renyu / Liang Fangzhong / Weber / Braudel); line anchors 660 / 840 / 1149 / 1393 / 2073 / 7085. |
| 38 | `essay-ming-military.html` | ~310 | Summary translation of `docs/04-文化与历史背景/明代军事制度对照专题.md` (W146). The heavenly army as the decaying Ming military: guard-battalions, the supreme-commander system, the retainer system, the tusi system; four scholars (Huang Renyu / Mao Haijian / Liang Fangzhong / Meng Sen); past-and-present table. |
| 39 | `essay-ming-religion.html` | ~320 | Summary translation of `docs/04-文化与历史背景/明代宗教制度对照专题.md` (W154). Ordination by decree: monk-officials, the August Supreme God, Guandi and Guanyin, ordination assessment; four theorists (Huang Renyu / Qian Mu / Weber / Yang Qingkun); the seven-layer Ming-mirror table. |
| 40 | `essay-ming-social-customs.html` | ~360 | Summary translation of `docs/04-文化与历史背景/明代社会风俗对照专题.md` (W096). Customs as governance: the five Ming customary dimensions (marriage / dress / diet / burial / exam) as institutionalised customs underwritten by the Great Ming Code; Foucault's governmentality; thirteen line anchors and a past-present five-row table. |
| 41 | `essay-ming-literary-thought.html` | ~345 | Summary translation of `docs/04-文化与历史背景/明代文学思想对照专题.md` (W122). The novel as a transitional text of Ming literary thought: four thinkers (Li Zhi's childlike mind / Yuan Hongdao's Gong'an xinling / Gui Youguang's Tang-Song School / Li Mengyang's Seven Masters); the four great novels mapped laterally; a five-stage genealogy and a past-present table. |
| 42 | `essay-ming-intellectual-history.html` | ~350 | Summary translation of `docs/04-文化与历史背景/明代思想史对照专题.md` (W180). The pilgrimage as Ming intellectual history: four thinkers (Wang Yangming's heart-mind / Li Zhi's childlike mind / Wang Ji's everyday-Way / Huang Zongxi's people-host-ruler-guest); four case mappings with line anchors 1459 / 4370 / 1868 / 7085; closing the eight-layer Ming mirror. Distinct from E15 (three-teachings synthesis). |
| 43 | `essay-poetry-opening.html` | ~270 | Summary translation of `docs/05-诗词歌赋/开篇诗专题深化.md` (W182). The opening verse as "constitutional" poetics: three poetic coordinates (Wang Guowei's realm theory / Zhu Guangqian / Ye Jiaying), six frame couplets (chs. 1/7/8/14/22/100) folding the Three Teachings into eight characters, the Dao→Buddha→synthesis power arc, and a past-present table. |
| 44 | `essay-poetry-imagery.html` | ~250 | Summary translation of `docs/05-诗词歌赋/西游诗词意象谱系专题.md` (W288). The imagery lineage: four imagery theorists (Pound / Eliot / Bachelard / Liu Xie) reading four images — stone-monkey, peach, white-bone, true-sutra — across Creation→Desire→Illusion→Awakening, with an East-meets-West table (Liu Xie c. 500 precedes Western Imagism by 1,400 years). |

| 45 | `essay-character-fu.html` | ~250 | Summary translation of `docs/05-诗词歌赋/原著人物赋诗词赏析专题.md`. Character-fu as the novel's verse-machine: four fu-types (debut / transformation / enlightenment / apotheosis) read through Liu Xie, Zhong Rong, Sikong Tu, and Wang Guowei; Ming mirrors (Archaists / Gong'an xinling / opera song-speech). |
| 46 | `essay-rhythm-analysis.html` | ~240 | Summary translation of `docs/05-诗词歌赋/西游诗词韵律分析专题.md`. Four dimensions of sound-law — tone-level, parallelism, rhythm, rounding-completion — through Wang Li, Qi Gong, Zhou Zhenfu, and Zhu Guangqian at four nodes (lines 522 / 864 / 1393 / 7085); the oblique-open / level-close closure. |
| 47 | `essay-thematic-poetry.html` | ~230 | The project's own Journey-inspired "themed creations": four poems (Five-Element Mountain / Three Strikes on White Bone / True &amp; False Monkey King / Lingyun Ford) presented in faithful translation; "old bottle, new wine." |
| 48 | `essay-original-poetry.html` | ~250 | Summary translation of `docs/05-诗词歌赋/原著诗词赏析.md`. Umbrella overview of the ~800 poems: four functions, thematic groupings, the hundred chapter-couplets, genre distribution (~6% / 37% / 10% / 25% / 4% / 6% / 5%), and a character-praise comparison. |

## Translation strategy

- **Curated summaries, not full translations.** Each English page condenses its Chinese source rather than translating word-for-word. The aim is to preserve the core argument and signature analogies while fitting a manageable English reading length.
- **Classical rice-paper palette preserved.** All HTML pages reuse the main site's CSS tokens (`--bg: #faf7f2`, `--accent: #c8463a`, `--accent-2: #3a6b8c`, plus `--accent-3: #7a5230` and `--accent-4: #5a7a3a`) and the dark-gradient hero with `rgba(232, 184, 133, 0.18)` radial highlight, so the English pages feel like a sibling of the main site rather than a separate product.
- **Chinese↔English switch links.** Every English page has a top-right `中文` link back to the corresponding main-site page (`../index.html`, `../dashboard.html`, etc.). The main site's pages are the canonical edition.
- **Source attribution.** Each essay page and the academic-papers page cite the absolute path of the original Chinese source so readers can verify or read the full text.
- **Respect original meaning, allow summary phrasing.** Translations follow the source essay's intent and structure but may rephrase, condense, or merge sentences for English readability.

## Relationship to the main site

- `site/en/` is a **subset** of `site/`, not a fork. The English pages link outward to the main site's full visualizations (e.g. `../data/cognitive-psychology.html`, `../data/philosophy.html`) and to the original Chinese essays under `docs/06-个人随笔/`.
- The main site (`site/index.html`, `site/dashboard.html`, `site/data/*.html`) remains the canonical, complete edition. The English subset offers a curated on-ramp for non-Chinese readers; it does not attempt to mirror every page.
- The English dashboard's KPIs (`100 / 211 / 209 / 85 / 55`) match the project's current totals as of v2.3.11 (W383); they will be updated alongside the main site as the project grows.
- Footer double-index links (`../../CHANGELOG.md` v2.3.11 W383 / `../../scripts/output/file-index.md` W383) appear on every English HTML page, matching the footer convention used across the main site.

## Verification

Each English HTML page was verified to contain:

1. A recognizable English title ("Journey to the West" or the corresponding section title).
2. The footer double-index: `CHANGELOG.md v2.3.11 W383` and `file-index.md W383`.
3. A Chinese↔English switch link pointing back to `../index.html` or the corresponding main-site page.

## Scope boundaries

This subproject creates the 51 files listed above under `site/en/`. It does **not**:

- Create `scripts/a11y_audit.py` (handled by a separate subagent).
- Create `.github/workflows/` CI definitions (handled by a separate subagent).
- Modify any existing file under `site/`, `docs/`, `scripts/`, or `.github/`.
- Translate the 100 chapter-by-chapter interpretations, the 60 character analyses, or the 91 theme essays. Those remain Chinese-only for now.

## Navigation

- Back to main site: [`../index.html`](../index.html)
- Main dashboard: [`../dashboard.html`](../dashboard.html)
- Full academic bibliography (55 entries, Chinese): [`../../source/引用与网络解读/学术论文索引.md`](../../source/引用与网络解读/学术论文索引.md)
- Project changelog: [`../../CHANGELOG.md`](../../CHANGELOG.md)
- File index: [`../../scripts/output/file-index.md`](../../scripts/output/file-index.md)

---

© 2026 Journey to the West · Annotated Project · MIT License · Continuously updated
