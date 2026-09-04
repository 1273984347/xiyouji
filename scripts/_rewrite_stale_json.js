// -*- coding: utf-8 -*-
// 一次性修复：从页面 EMBEDDED 内嵌数据回写陈旧 JSON（http 模式 fetch 到旧结构导致渲染崩溃）
// 用法：node _rewrite_stale_json.js
const fs = require('fs');
const path = require('path');
const ROOT = path.dirname(__dirname);

function extractEmbedded(html) {
  const start = html.indexOf('const EMBEDDED');
  if (start < 0) throw new Error('EMBEDDED 未找到');
  const braceStart = html.indexOf('{', start);
  let depth = 0, i = braceStart, inStr = false, quote = '', esc = false;
  for (; i < html.length; i++) {
    const c = html[i];
    if (inStr) {
      if (esc) esc = false;
      else if (c === '\\') esc = true;
      else if (c === quote) inStr = false;
      continue;
    }
    if (c === '"' || c === "'" || c === '`') { inStr = true; quote = c; continue; }
    if (c === '{') depth++;
    else if (c === '}') { depth--; if (depth === 0) break; }
  }
  const literal = html.slice(braceStart, i + 1);
  return JSON.parse(literal.replace(/,\s*([}\]])/g, '$1'));
}

const JOBS = [
  {
    page: 'site/data/methodology-matrix.html',
    map: {
      'villain_matrix': 'scripts/output/data/villain_matrix.json',
      'rescue_roi': 'scripts/output/data/rescue_roi.json',
      'summary': 'scripts/output/data/methodology_summary.json',
    }
  },
  {
    page: 'site/data/narrative-experiment.html',
    map: {
      'board_game': 'scripts/output/data/board_game.json',
      'narrative_cards': 'scripts/output/data/narrative_cards.json',
      'story_generator': 'scripts/output/data/story_generator.json',
      'narrative_experiment_summary': 'scripts/output/data/narrative_experiment_summary.json',
    }
  }
];

let changed = 0;
for (const job of JOBS) {
  const html = fs.readFileSync(path.join(ROOT, job.page), 'utf-8');
  const embedded = extractEmbedded(html);
  for (const [key, rel] of Object.entries(job.map)) {
    if (!embedded[key]) { console.log('[SKIP]', job.page, 'EMBEDDED 缺键', key); continue; }
    if (!rel.startsWith('scripts/output/data/')) { console.log('[SKIP] 路径越界', rel); continue; }
    const out = path.join(ROOT, rel);
    if (!path.resolve(out).startsWith(ROOT + path.sep)) { console.log('[SKIP] 路径越界', rel); continue; }
    const before = fs.existsSync(out) ? fs.statSync(out).size : -1;
    fs.writeFileSync(out, JSON.stringify(embedded[key], null, 2) + '\n', 'utf-8');
    const after = fs.statSync(out).size;
    changed++;
    console.log('[WRITE]', rel, before + 'B ->', after + 'B');
  }
}
console.log('---- 回写完成，共', changed, '个 JSON ----');
