# Journey to the West · Annotated — English Edition (W349)

> i18n internationalization subproject of the main **Journey to the West · Annotated** project.
> Version: v2.3.0 · W349 · 2026-08-04

## Overview

`site/en/` is the English-language subset of the main site at `site/`. It provides a curated entry point for non-Chinese readers: a landing page, a simplified data dashboard, a selected academic papers index, four data pages (the 81 tribulations, the pilgrims, the bestiary, and a 100-chapter map), ten long-form essays in summary-translation form, four deep-dive character studies, a methodology reading-guide, and an English tour of all 85 visualizations. The full Chinese site remains the canonical edition; the English pages link back to it through Chinese↔English switch links.

This subproject was created in W234-E4 (v2.2.40) as part of the AVES (Academic / Visualization / Essay / Site) fourth-direction batch. It was expanded in W345 (v2.2.95) with three new essays (E4–E6) drawn from the W344 quality-enhancement A5/A6 articles, growing the subset from 7 to 10 files. It was further expanded in W347 (v2.2.98) with four data pages (TRIBULATIONS · PILGRIMS · BESTIARY · CHAPTER-MAP) bridging the project's own datasets (81-hardships, pilgrim-team-*, monster-*, chapters-metadata), growing the subset from 10 to 14 files. It was expanded again in W348 (v2.2.99) with three scholarship essays (E7–E9: historical vs. fictional Xuanzang, Heaven as a Ming bureaucracy, the hundred chapter-couplets), a visualization tour (85 pages in eight clusters), a deep-dive on Sun Wukong, and a methodology reading-guide — growing the subset from 14 to 20 files. It was expanded once more in W349 (v2.3.0) with three pilgrim deep-dives (Tang Sanzang, Zhu Bajie, Sha Wujing) and an essay on Quanzhen Daoism (E10) reading the novel's allegorical layer as a Daoist inner-alchemy manual — growing the subset from 20 to 24 files.

## File list (24 files)

All files live under `d:\1\xiyouji\site\en\`.

| # | File | Lines | Purpose |
|---|---|---|---|
| 1 | `index.html` | ~375 | English landing page. Title "Journey to the West · Annotated", subtitle "A hybrid reading project". Twenty-two entry cards (dashboard / academic papers / 4 data pages / 10 essays / 4 deep-dives / 2 guides / visualization tour). |
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
| 14 | `README.md` | (this file) | i18n English-site documentation. |
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

## Translation strategy

- **Curated summaries, not full translations.** Each English page condenses its Chinese source rather than translating word-for-word. The aim is to preserve the core argument and signature analogies while fitting a manageable English reading length.
- **Classical rice-paper palette preserved.** All HTML pages reuse the main site's CSS tokens (`--bg: #faf7f2`, `--accent: #c8463a`, `--accent-2: #3a6b8c`, plus `--accent-3: #7a5230` and `--accent-4: #5a7a3a`) and the dark-gradient hero with `rgba(232, 184, 133, 0.18)` radial highlight, so the English pages feel like a sibling of the main site rather than a separate product.
- **Chinese↔English switch links.** Every English page has a top-right `中文` link back to the corresponding main-site page (`../index.html`, `../dashboard.html`, etc.). The main site's pages are the canonical edition.
- **Source attribution.** Each essay page and the academic-papers page cite the absolute path of the original Chinese source so readers can verify or read the full text.
- **Respect original meaning, allow summary phrasing.** Translations follow the source essay's intent and structure but may rephrase, condense, or merge sentences for English readability.

## Relationship to the main site

- `site/en/` is a **subset** of `site/`, not a fork. The English pages link outward to the main site's full visualizations (e.g. `../data/cognitive-psychology.html`, `../data/philosophy.html`) and to the original Chinese essays under `docs/06-个人随笔/`.
- The main site (`site/index.html`, `site/dashboard.html`, `site/data/*.html`) remains the canonical, complete edition. The English subset offers a curated on-ramp for non-Chinese readers; it does not attempt to mirror every page.
- The English dashboard's KPIs (`100 / 60 / 91 / 68 / 55`) match the project's current totals as of W234; they will be updated alongside the main site as the project grows.
- Footer double-index links (`../../CHANGELOG.md` v2.3.0 W349 / `../../scripts/output/file-index.md` W349) appear on every English HTML page, matching the footer convention used across the main site.

## Verification

Each English HTML page was verified to contain:

1. A recognizable English title ("Journey to the West" or the corresponding section title).
2. The footer double-index: `CHANGELOG.md v2.3.0 W349` and `file-index.md W349`.
3. A Chinese↔English switch link pointing back to `../index.html` or the corresponding main-site page.

## Scope boundaries

This subproject creates the 24 files listed above under `site/en/`. It does **not**:

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
