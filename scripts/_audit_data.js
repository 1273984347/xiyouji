// -*- coding: utf-8 -*-
// Data-consistency audit for network graphs:
//  - best-effort extract node/link counts from dataset/<base>.json (recursive)
//  - count rendered DOM svg circles (nodes) and svg lines (edges, incl hidden)
//  - report both so mismatches can be inspected (some are client-side filtering)
const { chromium } = require('playwright');
const path = require('path'), fs = require('fs');
const ROOT = path.dirname(__dirname);
const DATA = path.join(ROOT, 'site', 'data');
const DSET = path.join(ROOT, 'dataset');
const D3 = path.resolve(ROOT, 'xiyouji-agent-web/node_modules/d3/dist/d3.min.js');
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const d3body = fs.readFileSync(D3, 'utf-8');

const PAGES = [
 'character-dynamic-network.html','relationships.html','six-senses-narratology-network.html',
 'journey-geo-semiotics.html','monster-ecology-network.html','monster-hierarchy-network.html',
 'monster-victims-network.html','monster-female-network.html','heaven-power-network.html',
 'underworld-power-network.html','theological-intervention-network.html','pilgrim-team-dynamic-network.html',
 'intertextuality-network.html','guanyin-six-roles-network.html','character-semantic-network.html',
 'narratology-12d-network.html','narratology-13d-network.html','four-dimensional-research-network.html',
 'character-relationship-3d.html','cross-time-danmaku.html'
];

// recursive find largest list of dicts that look like links (source+target)
function findLinks(obj, best) {
  if (Array.isArray(obj)) {
    if (obj.length && obj.every(x => x && typeof x === 'object' && 'source' in x && 'target' in x))
      best.links = Math.max(best.links, obj.length);
    obj.forEach(x => findLinks(x, best));
  } else if (obj && typeof obj === 'object') {
    for (const k of Object.keys(obj)) findLinks(obj[k], best);
  }
  return best;
}
// recursive find node-like list (has id or name, not links). prefer under 'network' key.
function findNodes(obj, best, underNetwork) {
  if (Array.isArray(obj)) {
    const looks = obj.length && obj.every(x => x && typeof x === 'object' && ('id' in x || 'name' in x));
    if (looks) {
      const score = obj.length * (underNetwork ? 2 : 1);
      if (score > best.score) { best.score = score; best.nodes = obj.length; }
    }
    obj.forEach(x => findNodes(x, best, underNetwork));
  } else if (obj && typeof obj === 'object') {
    const un = underNetwork || (typeof obj === 'object' && 'network' in obj && Array.isArray(obj.network));
    for (const k of Object.keys(obj)) {
      const childUN = (k === 'network' && Array.isArray(obj[k])) ? true : underNetwork;
      findNodes(obj[k], best, childUN);
    }
  }
  return best;
}

const DOM = () => {
  let circles = 0, lines = 0;
  document.querySelectorAll('svg').forEach(svg => {
    circles += svg.querySelectorAll('circle').length;
    lines += svg.querySelectorAll('line').length;
  });
  return { circles, lines };
};

function url(f){ return 'file:///' + path.join(DATA, f).replace(/\\/g, '/'); }

(async () => {
  const b = await chromium.launch({ executablePath: CHROME, headless: true, args: ['--no-sandbox'] });
  const p = await b.newPage({ viewport: { width: 1440, height: 900 } });
  await p.route('**/d3*.js', r => r.fulfill({ contentType: 'application/javascript', body: d3body }));
  await p.route('**/d3js.org/**', r => r.fulfill({ contentType: 'application/javascript', body: d3body }));
  const out = [];
  for (const f of PAGES) {
    const base = f.slice(0, -5);
    if (!/^[A-Za-z0-9._-]+\.json$/.test(base)) { console.log('[SKIP] 文件名非白名单', base); continue; }
    const jp = path.join(DSET, base + '.json');
    if (!path.resolve(jp).startsWith(DSET + path.sep)) { console.log('[SKIP] 路径越界', base); continue; }
    let jn = null, jl = null, hasJson = false;
    if (fs.existsSync(jp)) {
      hasJson = true;
      try {
        const d = JSON.parse(fs.readFileSync(jp, 'utf-8'));
        jn = findNodes(d, { nodes: 0, score: 0 }, false).nodes;
        jl = findLinks(d, { links: 0 }).links;
      } catch (e) { jn = 'err'; jl = 'err'; }
    }
    const errs = [];
    p.on('pageerror', e => errs.push(String(e.message || e).slice(0, 80)));
    try { await p.goto(url(f), { waitUntil: 'load', timeout: 20000 }); } catch (e) {}
    await p.waitForTimeout(5000);
    let dom = {}; try { dom = await p.evaluate(DOM); } catch (e) { dom = { err: String(e).slice(0, 80) }; }
    p.removeAllListeners('pageerror');
    out.push({ page: f, hasJson, jsonNodes: jn, jsonLinks: jl, domCircles: dom.circles || 0, domLines: dom.lines || 0, pageErrors: errs.length, domErr: dom.err || null });
  }
  await b.close();
  fs.writeFileSync(path.join(ROOT, 'scripts', '_audit_data.json'), JSON.stringify(out, null, 2));
  out.forEach(r => console.log(`${r.page.padEnd(42)} json(n/l)=${r.jsonNodes}/${r.jsonLinks} dom(c/l)=${r.domCircles}/${r.domLines} err=${r.pageErrors}`));
})();
