const { chromium } = require('playwright');
const fs = require('fs');
const D3 = fs.readFileSync('xiyouji-agent-web/node_modules/d3/dist/d3.min.js', 'utf8');
(async () => {
  const browser = await chromium.launch({ executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe', args: ['--no-sandbox','--disable-gpu'] });
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  await page.route('**/d3*.js', r => r.fulfill({ contentType: 'application/javascript', body: D3 }));
  await page.route('**/d3/**', r => r.fulfill({ contentType: 'application/javascript', body: D3 }));
  await page.goto('file://' + process.cwd() + '/site/data/philosophy.html', { waitUntil: 'networkidle', timeout: 25000 }).catch(()=>{});
  await page.waitForTimeout(8000);
  const res = await page.evaluate(() => {
    const EX = ".tick,.legend,.axis,.domain,.title,.cell,.tooltip,.axis-label";
    const ts = [...document.querySelectorAll('svg text')].filter(t => {
      if (!t.closest) return false;
      if (t.closest(EX)) return false;
      const r = t.getBoundingClientRect();
      return r.width > 0 && r.height > 0;
    });
    const R = ts.map(t => ({ t: (t.textContent||'').trim().slice(0,40), r: t.getBoundingClientRect(), pid: (t.parentNode && t.parentNode.getAttribute && t.parentNode.getAttribute('class'))||'' }));
    const out = [];
    for (let i=0;i<R.length;i++) for (let j=i+1;j<R.length;j++){
      const a=R[i].r,b=R[j].r;
      const ix=Math.max(0,Math.min(a.right,b.right)-Math.max(a.left,b.left));
      const iy=Math.max(0,Math.min(a.bottom,b.bottom)-Math.max(a.top,b.top));
      if(ix>0&&iy>0){
        out.push({a:R[i].t,b:R[j].t,ix:Math.round(ix),iy:Math.round(iy),aParent:R[i].pid,bParent:R[j].pid});
      }
    }
    return {count:R.length, overlaps:out};
  });
  console.log(JSON.stringify(res, null, 2));
  await browser.close();
})();
