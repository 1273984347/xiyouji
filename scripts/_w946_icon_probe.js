const { chromium } = require('D:/xiyouji/scripts/node_modules/playwright');
const path = require('path');
const PAGES = [["reader/ch001.html", "内联 SVG（收藏/赞/踩）"], ["data/timeline.html", "时间线专属图标（内联 SVG）"], ["data/concept-device.html", "CSS content 位（同源 mask）"], ["data/graph-explorer.html", "控件图标（菜单/关闭/检索）"]];
const ENVS = [["file", "file:///D:/xiyouji/site/"], ["http", "http://127.0.0.1:8899/"]];
const PROBE = "\n() => {\n  const out = { svg: [], mask: [], err: [] };\n  document.querySelectorAll('svg.ico').forEach((s) => {\n    const b = s.getBoundingClientRect();\n    const cs = getComputedStyle(s);\n    const fs = parseFloat(getComputedStyle(s.parentElement || s).fontSize) || 16;\n    out.svg.push({\n      cls: s.getAttribute('class'),\n      w: b.width, h: b.height,\n      stroke: cs.stroke, fill: cs.fill,\n      strokeWidth: cs.strokeWidth,\n      emRatio: fs ? +(b.width / fs).toFixed(2) : null,\n    });\n  });\n  const sels = ['.radio-out .caption', '.detective-banner', '.suspect-card', '.hu-card',\n                '.warn-item', '.cc-acq', '.nc-quote', '.search-box', '.id-innovation'];\n  sels.forEach((sel) => {\n    document.querySelectorAll(sel).forEach((el) => {\n      const pb = getComputedStyle(el, '::before');\n      const mi = pb.maskImage || pb.webkitMaskImage || 'none';\n      if (mi === 'none' || pb.content === 'none') return;\n      out.mask.push({ sel: sel, w: pb.width, h: pb.height, mask: mi.slice(0, 70) });\n    });\n  });\n  return out;\n}\n";
(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  const report = {};
  for (const [env, base] of ENVS) {
    for (const [rel, note] of PAGES) {
      const p = await ctx.newPage();
      const errs = [], failed = [];
      p.on('console', (m) => { if (m.type() === 'error') errs.push(m.text()); });
      p.on('pageerror', (e) => errs.push('pageerror: ' + e.message));
      p.on('requestfailed', (r) => failed.push(r.url() + ' :: ' + (r.failure()||{}).errorText));
      await p.goto(base + rel, { waitUntil: 'load' });
      await p.waitForTimeout(1200);
      report[env + '|' + rel] = { env, note, probe: await p.evaluate('(' + PROBE + ')()'), errors: errs, failed };
      await p.close();
    }
  }
  await browser.close();
  console.log(JSON.stringify(report));
})();
