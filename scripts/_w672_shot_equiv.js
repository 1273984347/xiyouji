/**
 * _w672_shot_equiv.js — W672 WP-1.1 渲染等值验收（方案 §三 WP-1.1 验收 5）。
 *
 * 用法：
 *   node scripts/_w672_shot_equiv.js capture before    # 修复前基线截图 → .review-tmp/_w672/before/
 *   node scripts/_w672_shot_equiv.js capture after     # 修复后截图     → .review-tmp/_w672/after/
 *   node scripts/_w672_shot_equiv.js diff before after # 像素级比对（PNG 无损解码），全 0 = PASS
 *
 * 确定性口径（before/after 两侧完全一致，任何像素差即真实渲染差异）：
 * - file:// 直开 + 拦截全部 http(s) 请求（EMBEDDED 回退路径，无网络抖动）；
 * - addInitScript：mulberry32 固定种子替换 Math.random；requestAnimationFrame 改
 *   setTimeout(0) 定量泵 400 帧后冻结（力导向 tick 数与过渡终态两侧一致）；
 * - 注入 CSS：*{animation:none!important;transition:none!important} + .reveal-in 强制显现；
 * - 滚动穿透（W554 教训：fullPage 不触发 IntersectionObserver）+ 回顶 settle 后 fullPage 截图。
 */
const { chromium } = require('playwright');
require('./_csp_guard').guard();
const fs = require('fs');
const path = require('path');
const zlib = require('zlib');

const ROOT = path.resolve(__dirname, '..');
const SITE = path.join(ROOT, 'site');
const OUT = path.join(ROOT, '.review-tmp', '_w672');

// 方案 §三 WP-1.1：50 页清单按文件名排序取第 1/13/25/37/50 页（2026-10-06 基线清单）
const PAGES = [
  'business-model.html',
  'four-dimensional-research-network.html',
  'language-style-radar.html',
  'narratology-12d-network.html',
  'underworld-power-network.html',
];
const VIEWPORTS = [
  ['d1280', { width: 1280, height: 800 }],
  ['m375', { width: 375, height: 812 }],
];

const INIT = `
(() => {
  // mulberry32 固定种子
  let s = 0x2f6e2b1 | 0;
  Math.random = () => {
    s = (s + 0x6d2b79f5) | 0;
    let t = Math.imul(s ^ (s >>> 15), 1 | s);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
  // 虚拟时钟：performance.now 只随泵帧步进 —— 过渡进度/力导向衰减全部帧数确定化
  const perf = window.performance;
  let virt = 0;
  perf.now = () => virt;
  // rAF 无上限泵 + 空闲探针：过渡必然跑完（终态唯一）、力导向自收敛后 rAF 停止调度
  let frame = 0;
  window.__rafLast = Date.now();
  window.requestAnimationFrame = (cb) => {
    virt += 16.67;
    window.__rafLast = Date.now();
    setTimeout(() => cb(virt), 0);
    return ++frame;
  };
  window.cancelAnimationFrame = () => {};
})();
`;
const CSS_KILL = '*{animation:none!important;transition:none!important}.reveal-in{opacity:1!important;transform:none!important}';

async function capture(tag, pagesFile) {
  const dir = path.join(OUT, tag);
  fs.mkdirSync(dir, { recursive: true });
  let rels;
  if (pagesFile) {
    rels = fs.readFileSync(pagesFile, 'utf-8').split(/\r?\n/).map((s) => s.trim()).filter(Boolean).map((r) => r.replace(/\\/g, '/') + '.html');
  } else {
    rels = PAGES.map((p) => 'data/' + p);
  }
  console.log('pages:', rels.length);
  const browser = await chromium.launch();
  let done = 0;
  for (const rel of rels) {
    for (const [vp, size] of VIEWPORTS) {
      const ctx = await browser.newContext({ viewport: size, deviceScaleFactor: 1, reducedMotion: 'reduce' });
      await ctx.addInitScript(INIT);
      const page = await ctx.newPage();
      await page.route(/^https?:\/\//, (r) => r.abort());
      const url = 'file:///' + path.join(SITE, rel).split(path.sep).join('/');
      try {
        await page.goto(url, { waitUntil: 'load', timeout: 60000 });
        await page.evaluate(() => document.fonts.ready);
        await page.waitForTimeout(1200);
        await page.addStyleTag({ content: CSS_KILL });
        await page.evaluate(async () => {
          const step = window.innerHeight || 800;
          const H = document.body.scrollHeight;
          for (let y = 0; y < H; y += step) {
            window.scrollTo(0, y);
            await new Promise((r) => setTimeout(r, 100));
          }
          window.scrollTo(0, H);
          await new Promise((r) => setTimeout(r, 250));
          window.scrollTo(0, 0);
          await new Promise((r) => setTimeout(r, 400));
        });
        await page.waitForTimeout(900);
        // 等待 rAF 空闲（d3 力导向自收敛、全部过渡终态后，泵自然停摆）
        try {
          await page.waitForFunction(() => Date.now() - window.__rafLast > 400, { timeout: 15000, polling: 250 });
        } catch (e) {
          console.log('RAF-IDLE-TIMEOUT', rel, vp, '（按现状截取）');
        }
        // 冻结一切仍在跑的动效（CSS/SMIL/WAAPI 三族统一；CSS animation:none 覆盖不到的）
        await page.evaluate(() => {
          document.getAnimations().forEach((a) => { try { a.currentTime = 0; a.pause(); } catch (err) { /* noop */ } });
        });
        await page.waitForTimeout(300);
        const stem = rel.replace(/\.html$/, '').replace(/\//g, '__');
        await page.screenshot({ path: path.join(dir, stem + '__' + vp + '.png'), fullPage: true });
        done++;
        console.log('captured', rel, vp);
      } catch (e) {
        console.log('CAPTURE-FAIL', rel, vp, String(e.message).slice(0, 100));
        process.exitCode = 1;
      }
      await ctx.close();
    }
  }
  await browser.close();
  console.log('done:', done, '/', rels.length * VIEWPORTS.length);
}

function decodePNG(buf) {
  let off = 8;
  let width = 0, height = 0, bitDepth = 0, colorType = 0;
  const idat = [];
  while (off + 8 <= buf.length) {
    const len = buf.readUInt32BE(off);
    const type = buf.toString('ascii', off + 4, off + 8);
    const data = buf.subarray(off + 8, off + 8 + len);
    if (type === 'IHDR') {
      width = data.readUInt32BE(0); height = data.readUInt32BE(4);
      bitDepth = data[8]; colorType = data[9];
    } else if (type === 'IDAT') idat.push(data);
    else if (type === 'IEND') break;
    off += 12 + len;
  }
  if (bitDepth !== 8) throw new Error('unsupported bitDepth ' + bitDepth);
  const channels = { 0: 1, 2: 3, 4: 2, 6: 4 }[colorType];
  if (!channels) throw new Error('unsupported colorType ' + colorType);
  const raw = zlib.inflateSync(Buffer.concat(idat));
  const stride = width * channels;
  const out = Buffer.alloc(height * stride);
  for (let y = 0; y < height; y++) {
    const filter = raw[y * (stride + 1)];
    const line = raw.subarray(y * (stride + 1) + 1, (y + 1) * (stride + 1));
    const cur = out.subarray(y * stride, (y + 1) * stride);
    for (let x = 0; x < stride; x++) {
      const a = x >= channels ? cur[x - channels] : 0;
      const b = y > 0 ? out[(y - 1) * stride + x] : 0;
      const c = y > 0 && x >= channels ? out[(y - 1) * stride + x - channels] : 0;
      let v = line[x];
      if (filter === 1) v = (v + a) & 0xff;
      else if (filter === 2) v = (v + b) & 0xff;
      else if (filter === 3) v = (v + ((a + b) >> 1)) & 0xff;
      else if (filter === 4) {
        const p = (a + b - c) | 0;
        const pa = Math.abs(p - a), pb = Math.abs(p - b), pc = Math.abs(p - c);
        v = (v + (pa <= pb && pa <= pc ? a : pb <= pc ? b : c)) & 0xff;
      }
      cur[x] = v;
    }
  }
  return { width, height, channels, data: out };
}

function diff(tagA, tagB) {
  const files = fs.readdirSync(path.join(OUT, tagA)).filter((f) => f.endsWith('.png')).sort();
  let bad = 0;
  for (const f of files) {
    const pa = path.join(OUT, tagA, f);
    const pb = path.join(OUT, tagB, f);
    if (!fs.existsSync(pb)) { console.log('MISSING-B', f); bad++; continue; }
    const A = decodePNG(fs.readFileSync(pa));
    const B = decodePNG(fs.readFileSync(pb));
    if (A.width !== B.width || A.height !== B.height) {
      console.log('SIZE-DIFF', f, A.width + 'x' + A.height, 'vs', B.width + 'x' + B.height);
      bad++;
      continue;
    }
    let n = 0, minX = 1e9, minY = 1e9, maxX = -1, maxY = -1;
    const len = A.data.length;
    for (let i = 0; i < len; i++) {
      if (A.data[i] !== B.data[i]) {
        n++;
        const px = Math.floor((i / A.channels) % A.width);
        const py = Math.floor(i / A.channels / A.width);
        if (px < minX) minX = px;
        if (px > maxX) maxX = px;
        if (py < minY) minY = py;
        if (py > maxY) maxY = py;
      }
    }
    if (n === 0) console.log('OK       ', f);
    else {
      console.log('DIFF ' + n + 'px bbox=(' + minX + ',' + minY + ')-(' + maxX + ',' + maxY + ')', f);
      bad++;
    }
  }
  console.log(bad === 0 ? 'EQUIV-PASS: 全部 ' + files.length + ' 张逐像素一致' : 'EQUIV-FAIL: ' + bad + ' 张不一致');
  if (bad) process.exitCode = 1;
}

(async () => {
  const cmd = process.argv[2];
  if (cmd === 'capture') await capture(process.argv[3] || 'run', process.argv[4]);
  else if (cmd === 'diff') diff(process.argv[3], process.argv[4]);
  else { console.log('usage: capture <tag> [pagesFile] | diff <tagA> <tagB>'); process.exit(2); }
})().catch((e) => { console.error(e); process.exit(1); });
