/* render_classify_probe.js — 渲染级载体分类探针（W1266 批二·主会话独立复算）
# 用途：对「静态含图页」逐页渲染后按图元实证分类（true_chart / true_chart_canvas / icon_only / no_svg）
# 判据：svg 含 <text> 或 >=3 数据图元（rect/circle/line/polyline/polygon）且尺寸 >120x80 => chartLike；
#       否则小尺寸且无 text 且图元+path <= 2 => iconLike；canvas>40x40 或 3D 场景容器 => true_chart_canvas；
#       无 svg 且无 canvas => no_svg（真无图）
# 用法：$env:NODE_PATH='D:/xiyouji/scripts/node_modules'; node scripts/render_classify_probe.js <pages.json> <out.json>
# 取数：pages.json 须由**静态扫描直接产出**页面清单（禁派生自任何审计产物·避免循环依赖）
# 来源：W1266 批二线 B 独立探针（W1266-11-18 复跑一致：158/15/3/0）
# v3 增补（W1266 收官）：① requestfailed 按类型拆分（data / font / other）——判 env_blocked 必须
#      只看**数据类**失败（原计数把字体 CORS 混在一起会误判）；② 滚动穿透（逐屏 500px 到底→回顶→落定）
#      防 IntersectionObserver 懒渲染漏判；③ 记录滚动后的大尺寸 svg 数。
#      env_blocked（环境性未加载）**不在本探针职责内**：它需要「静态有图表载体 × 渲染级渲染不出」的**双面**对照；
#      本探针只产出**渲染级**四分类（true_chart / true_chart_canvas / icon_only / no_svg）。
#      成因枚举（数据未加载 / canvas·WebGL 不可用 / 布局未收敛 / 需交互触发）只作解释附在其后，**不作判定条件**。
#      另注：「有 fetch 报错」单独**不**构成 env_blocked（graph-explorer 有 fetch 失败却仍渲染出 EMBEDDED 兜底图）。 */
/* 主会话独立复算探针 v2：补齐 canvas / 3D 载体（v1 只数 svg ⇒ 会把 canvas 载体误判为「仅图标」） */
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

(async () => {
  const pages = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  const browser = await chromium.launch();
  const rows = [];
  let idx = 0;
  async function worker() {
    while (idx < pages.length) {
      const rel = pages[idx++];
      const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
      const page = await ctx.newPage();
      const errs = [], failed = [];
      page.on('pageerror', e => errs.push(String(e).slice(0, 100)));
      page.on('requestfailed', r => {
      const u = r.url();
      const name = u.split('/').pop().slice(0, 30);
      const kind = (/\.(json|csv|tsv)(\?|$)/i.test(u) || /\/api\//.test(u) || /\/data\//.test(u)) ? 'data'
        : (/\.(woff2?|ttf|otf|eot)(\?|$)/i.test(u) ? 'font' : 'other');
      failed.push({ kind, name });
    });
      try {
        await page.goto('file:///' + path.resolve(rel).replace(/\\/g, '/'), { waitUntil: 'load' });
        await page.waitForTimeout(2200);
        // 滚动穿透（触发 IntersectionObserver 懒渲染 · 防「图在视口外未渲染」被误判为无图）
        await page.evaluate(async () => {
          const h = document.body.scrollHeight;
          for (let y = 0; y < h; y += 500) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 120)); }
          window.scrollTo(0, 0);
        });
        await page.waitForTimeout(800);
        const info = await page.evaluate(() => {
          const svgs = Array.from(document.querySelectorAll('svg'));
          let chartLike = 0, iconLike = 0, bigSvgs = 0, withText = 0;
          for (const s of svgs) {
            const r = s.getBoundingClientRect();
            const big = r.width > 120 && r.height > 80;
            if (big) bigSvgs++;
            const marks = s.querySelectorAll('rect,circle,line,polyline,polygon').length;
            const hasText = s.querySelectorAll('text').length > 0;
            const paths = s.querySelectorAll('path').length;
            if (hasText) withText++;
            if (big && (hasText || marks >= 3)) chartLike++;
            else if (!big && !hasText && marks + paths <= 2) iconLike++;
          }
          const cvs = Array.from(document.querySelectorAll('canvas'));
          const liveCanvas = cvs.filter(c => { const r = c.getBoundingClientRect(); return r.width > 40 && r.height > 40; });
          // 3D 场景容器（three.js 常用容器）
          const scene3d = document.querySelectorAll('canvas, .three-container, [data-three], #scene, #chart3d, .chart-3d').length;
          const bigAfterScroll = svgs.filter(s => { const b = s.getBoundingClientRect(); return b.width > 120 && b.height > 80; }).length;
          return { svgTotal: svgs.length, chartLike, iconLike, bigSvgs, withText, bigAfterScroll,
                   canvasTotal: cvs.length, liveCanvas: liveCanvas.length, scene3d: scene3d };
        });
        let verdict;
        if (info.chartLike > 0) verdict = 'true_chart';
        else if (info.liveCanvas > 0 || info.scene3d > 0) verdict = 'true_chart_canvas';
        else if (info.svgTotal === 0 && info.canvasTotal === 0) verdict = 'no_svg';
        else verdict = 'icon_only';
        rows.push({ page: rel, verdict: verdict, ...info, pageErrors: errs.length,
                   failedReqs: failed.length,
                   failedData: failed.filter(f => f.kind === 'data').length,
                   failedFont: failed.filter(f => f.kind === 'font').length,
                   failedOther: failed.filter(f => f.kind === 'other').length });
      } catch (e) {
        rows.push({ page: rel, verdict: 'error', err: String(e).slice(0, 100) });
      }
      await ctx.close();
    }
  }
  await Promise.all(Array.from({ length: 4 }, worker));
  await browser.close();
  const cnt = {};
  for (const r of rows) cnt[r.verdict] = (cnt[r.verdict] || 0) + 1;
  fs.writeFileSync(process.argv[3], JSON.stringify({ rows: rows, counts: cnt }, null, 1));
  console.log('分类结果: ' + JSON.stringify(cnt) + '  共 ' + rows.length + ' 页');
})();
