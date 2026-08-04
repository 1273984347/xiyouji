# Journey to the West · Annotated — English Edition (W345)

> i18n internationalization subproject of the main **Journey to the West · Annotated** project.
> Version: v2.2.95 · W345 · 2026-08-04

## Overview

`site/en/` is the English-language subset of the main site at `site/`. It provides a curated entry point for non-Chinese readers: a landing page, a simplified data dashboard, a selected academic papers index, and six long-form essays in summary-translation form. The full Chinese site remains the canonical edition; the English pages link back to it through Chinese↔English switch links.

This subproject was created in W234-E4 (v2.2.40) as part of the AVES (Academic / Visualization / Essay / Site) fourth-direction batch. It was expanded in W345 (v2.2.95) with three new essays (E4–E6) drawn from the W344 quality-enhancement A5/A6 articles, growing the subset from 7 to 10 files.

## File list (10 files)

All files live under `d:\1\xiyouji\site\en\`.

| # | File | Lines | Purpose |
|---|---|---|---|
| 1 | `index.html` | ~280 | English landing page. Title "Journey to the West · Annotated", subtitle "A hybrid reading project". Eight entry cards (dashboard / academic papers / 6 essays). |
| 2 | `dashboard.html` | ~370 | English data dashboard. Five core KPI cards (100 chapters / 60 character analyses / 91 theme essays / 68 visualizations / 55 academic papers). |
| 3 | `academic-papers.html` | ~210 | Academic papers index. Ten representative entries selected from the 55-entry bibliography. Columns: ID / Author / Year / Title / Journal / Topic. |
| 4 | `essay-ai-era.html` | ~250 | Summary translation of `docs/06-个人随笔/西游与AI时代.md`. Five paragraphs: Subhuti · headband · mirror test · 81 tribulations · Mind Monkey. |
| 5 | `essay-information-cocoon.html` | ~240 | Summary translation of `docs/06-个人随笔/西游与信息茧房.md`. Six paragraphs: Tathagata's palm · Tang Seng's map · Bajie's bias · Wukong's immunity · Ming vs algorithmic · larger cocoon. |
| 6 | `essay-modern-management.html` | ~250 | Summary translation of `docs/06-个人随笔/西游与现代组织管理.md`. Six paragraphs: Tang Seng middle manager · Wukong senior IC · Bajie valve · Sha Seng adhesive · Jade Emperor CEO · demon backings. |
| 7 | `essay-zen-koan-vs-neidan.html` | ~265 | Summary translation of `docs/04-文化与历史背景/西游与禅宗公案专题.md`. Four sections: one Wukong two readings · Chan koan · Neidan chart · tension · conclusion. |
| 8 | `essay-version-evolution.html` | ~270 | Summary translation of `docs/04-文化与历史背景/版本演变补遗-平话层.md`. Five sections: folded 400 years · zaju layer · pinghua layer (conjectural) · abridged layer · stratified riverbed. |
| 9 | `essay-scenery-poems.html` | ~265 | Summary translation of `docs/05-诗词歌赋/原著景物诗分类赏析专题.md`. Four sections: typology · wonder-landscape · wayfaring · chan-sacred · conclusion. |
| 10 | `README.md` | (this file) | i18n English-site documentation. |

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
- Footer double-index links (`../../CHANGELOG.md` v2.2.95 W345 / `../../scripts/output/file-index.md` W345) appear on every English HTML page, matching the footer convention used across the main site.

## Verification

Each English HTML page was verified to contain:

1. A recognizable English title ("Journey to the West" or the corresponding section title).
2. The footer double-index: `CHANGELOG.md v2.2.95 W345` and `file-index.md W345`.
3. A Chinese↔English switch link pointing back to `../index.html` or the corresponding main-site page.

## Scope boundaries

This subproject creates the 10 files listed above under `site/en/`. It does **not**:

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
