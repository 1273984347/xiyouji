# 角色数据源（回答问题时按此优先级取证）

## 1. 正典源头（判事实用）

- **原著原文**：`source/原文/分回/`（100 回全文本，逐回 .md/.txt）——引文必须回这里核对。
- **逐回解读**：`docs/01-全书逐回解读/第NNN回-*.md`——回目号、事件、导航的权威。
- **人物档案**：`docs/02-人物深度分析/<角色>.md`（基础七段）——身份/封号/关系/结局的权威摘要。

## 2. 项目数据（可视化/检索用）

- `dataset/` 结构化 JSON（12 个角色相关）：character-relationship-3d / character-appearance / character-semantic-network / character-sentiment-arc / character-presence-timeline / monster-* / heaven-power / underworld-power / pilgrim-team-* / guanyin-six-roles 等。已由 `scripts/check_data_drift.js` 门禁守护（内嵌与 JSON 数组长度一致）。
- `scripts/output/data/*.json`：A-AH 脚本生成的运行时数据（fetch 源，线上 404 时页面回退内嵌）。
- `site/data/character-*.html`（7 页）：人物关系 3D / 动态网络 / 语义网络 / 情感弧 / 出场时间线 / 外貌分布。
- `site/en/character-*.html`（10 页）：英文人物页（wukong/bajie/shaseng/tangseng/bailongma 等）。
- `site/data/text-search.html` + `site/static/js/text-search-app.js`：全书 100 回原文全文检索（语料含回目 fullTitle）。

## 3. 出处标注规则

- 引用事件/引文 → 标回目（"第 N 回"），并核对 `docs/01-全书逐回解读/` 文件名。
- 引用数字（出场回数、提及次数）→ 若未全量验证，标"待全量数据验证"，不编造精确值。
- 人物关系/结局 → 优先 `docs/02-人物深度分析/` 基础档案，再交叉 dataset JSON。
- 可视化页数据 → 以 `dataset/*.json` 与页面 EMBEDDED 双源一致为准（漂移门禁守护）。
