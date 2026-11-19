#!/usr/bin/env node
/**
 * svg_text_contrast_probe.js — 第 80 槽配套探针
 *   （W1265 批一·判据补盲 1-9 建立 / W1282 批·补 graphic 口径·修「图形底色盲区」）
 *
 * 背景：
 *   第 80 门禁判据 = SVG 文字填充色 vs 有效背景色 的对比度 ≥ 3.0（WCAG 图形对象 1.4.11 的 3:1 线）。
 *   W1265 建立时底色口径只有两种（body / backdrop），二者都只看 **CSS backgroundColor**：
 *     · body    = 页面 body 的 backgroundColor
 *     · backdrop= 自元素向上找第一个非透明 CSS backgroundColor
 *   ⇒ **盲区（本批修的就是它）**：SVG 图形（rect/circle/path/polygon）的底色是 **fill 属性**，
 *     不是 CSS backgroundColor ⇒ backdropOf() 永远找不到它 ⇒ 「文字压在 SVG 图形色块上」的
 *     真实对比度**从未被量测过**。
 *     实测坐实（site/data/81-hardships.html 的 treemap）：白字 rgb(255,255,255) 压在
 *     #e9b885（rgb(233,184,133)）色块上，真实 CR = 1.80（远低于 3:1·实质不可读），
 *     而 body 口径拿它跟页面 body 背景比 ⇒ 判绿（漏检）。
 *
 * 三种底色口径（body / backdrop 为 W1265 既有，行为一字未改；graphic 为 W1282 新增）：
 *   body    （默认·既有）底色 = 页面 body 的 backgroundColor。与图表图形无关 ⇒ 对
 *           「文字压在图形色块上」必然失真（漏检主因）。
 *   backdrop（既有）    底色 = 自元素向上第一个非透明 CSS backgroundColor（卡片/面板底色）。
 *           仍看不见 SVG fill ⇒ 同样漏检「图形色块上的文字」。
 *   graphic （W1282 新增）底色 = **几何上真正覆盖该文字的 SVG 图形**的 computed fill；
 *           找不到覆盖图形 ⇒ 回退 body 口径（与既有口径同源，不引入新底色语义）。
 *
 * graphic 口径的几何配对判据（§几何配对·本批核心，写错会产生大量假阳性）：
 *   坐标系：SVG 用户坐标系。元素几何用 getBBox() 取，再把 4 个角点用 getCTM() 变换到
 *           **同一 <svg> 的 viewBox 用户空间**做比较。绝不用 getBoundingClientRect()
 *           （那是视口像素：CSS 缩放/viewBox 变换/滚动后与图形层错位 ⇒ 必然误配）。
 *           getBBox() 返回的是「不含元素自身 transform 属性」的局部几何，getCTM() 含自身
 *           transform ⇒ 二者组合恰好互补（不会重复应用、也不会漏应用）。
 *           **必须归一化**：treemap 的 rect 分属不同 <g transform=translate(...)>，局部坐标
 *           直接比较会把文字错配到别的色块（实测：chart-ending 的白字会误配到 #C0392B ⇒
 *           CR 4.9 ⇒ 判绿 ⇒ 漏检真实违例）。
 *   候选图形：同一 <svg> 内的 rect / circle / ellipse / path / polygon。
 *   有效性：computed fill 非 none 且可解析；有效 alpha = fillAlpha × fillOpacity × opacity
 *           ≥ 0.3（低于则该图形「不算底色」，继续找下一个）。
 *   覆盖判定（按图形类型分档，见 coversText()）：
 *     · rect 等实心矩形 —— 「中心点在图形 bbox 内」且「交集面积 / 文字 bbox 面积 ≥ 0.6」
 *       （文字大部分落在图形上）。
 *     · circle / ellipse —— 额外要求文字中心点落在**真实椭圆**内（bbox 是外接矩形，
 *       直接用 bbox 会把「椭圆外接矩形角落」误判为覆盖 ⇒ 假阳性）。
 *     · path / polygon —— **保守档**：只有图形 bbox **完全包含**文字 bbox 才算覆盖。
 *       理由：path 的 getBBox 是路径几何包围盒，对凹形/曲线只是近似（bbox 内可能有未填充的
 *       空白区）⇒ 只在完全包含时采信（宁可漏检不可误报）。
 *   多层重叠：命中多个时取 **bbox 面积最小**者（视觉上最贴近文字的那层）。
 *   找不到覆盖图形 ⇒ 回退 body 口径。
 *
 * 光晕（paint-order:stroke）豁免：
 *   body / backdrop 口径保持 W1265 既有行为（只要 paint-order:stroke + 描边宽 ≥1 + 描边非
 *   none 就整条跳过·不计缺陷）——既有基线与既有门禁行为不变。
 *   graphic 口径按「光晕是否真的提供了分离」判定：把光晕色（按 alpha）合成到底色上，
 *   若 **光晕色 vs 底色 的对比度 ≥ 3.0** ⇒ 光晕有效 ⇒ 豁免；否则（如白字配白晕压在浅橙块上，
 *   光晕与底色几乎同色 ⇒ 光晕零增益）⇒ 豁免失效，按真实 CR 判红。
 *
 * 输出：JSON 报告（scripts/output/svg_text_contrast_report.json）
 * 用法：node scripts/svg_text_contrast_probe.js [--scope data|en|all] [--out F] [--limit N] [--conc N]
 *       [--bg-mode body|backdrop|graphic] [--self-test [--json]]
 */
'use strict';

const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const ROOT = path.resolve(__dirname, '..');
const SITE = path.join(ROOT, 'site');

const THRESHOLD = 3.0;          // 判红线：WCAG 图形对象 1.4.11 的 3:1
const MIN_SHAPE_ALPHA = 0.3;    // 图形有效填充 alpha 下限（低于此值不算底色）
const MIN_COVER_RATIO = 0.6;    // 文字面积落入图形的最小比例（宽松档）
const HALO_MIN_SEPARATION = 3.0; // 光晕与底色的最小对比（低于此值 ⇒ 光晕无分离作用）

/** CLI 取值：同时支持 "--k v" 与 "--k=v" 两种写法。 */
function argValue(name, dflt) {
  const i = process.argv.indexOf(name);
  if (i > -1 && process.argv[i + 1] && !String(process.argv[i + 1]).startsWith('--')) {
    return String(process.argv[i + 1]);
  }
  const hit = process.argv.find((a) => String(a).startsWith(name + '='));
  if (hit) return String(hit).slice(name.length + 1);
  return dflt;
}

const SCOPE = argValue('--scope', 'all');
const LIMIT = parseInt(argValue('--limit', '0'), 10) || Infinity;
const CONC = Math.max(1, parseInt(argValue('--conc', '6'), 10) || 6);
const OUT = path.resolve(ROOT, argValue('--out', 'scripts/output/svg_text_contrast_report.json'));
const BG_MODE_RAW = String(argValue('--bg-mode', 'body')).toLowerCase();
const BG_MODE = BG_MODE_RAW === 'backdrop' ? 'backdrop' : BG_MODE_RAW === 'graphic' ? 'graphic' : 'body';

const STATES = [
  { id: 'S1-desktop-light', colorScheme: 'light', viewport: { width: 1440, height: 900 } },
  { id: 'S2-desktop-dark', colorScheme: 'dark', viewport: { width: 1440, height: 900 } },
  { id: 'S3-mobile-dark', colorScheme: 'dark', viewport: { width: 375, height: 812 } },
  { id: 'S4-mobile-light', colorScheme: 'light', viewport: { width: 375, height: 812 } },
];

/* ------------------------------------------------------------------ *
 * 纯函数层（node 侧·可被单测 require）：颜色 / 对比度 / 几何配对 / 判定
 * ------------------------------------------------------------------ */

function parseColor(str) {
  if (!str) return null;
  const m = String(str).match(/rgba?\(\s*([\d.]+)[,\s]+([\d.]+)[,\s]+([\d.]+)(?:[,\s/]+([\d.]+))?\s*\)/i);
  if (m) return { r: +m[1], g: +m[2], b: +m[3], a: m[4] === undefined ? 1 : +m[4] };
  if (/^#([0-9a-f]{6})$/i.test(str)) {
    const n = parseInt(str.slice(1), 16);
    return { r: (n >> 16) & 255, g: (n >> 8) & 255, b: n & 255, a: 1 };
  }
  if (/^#([0-9a-f]{3})$/i.test(str)) {
    const h = str.slice(1);
    return { r: parseInt(h[0] + h[0], 16), g: parseInt(h[1] + h[1], 16), b: parseInt(h[2] + h[2], 16), a: 1 };
  }
  return null;
}

function lum(c) {
  const f = (v) => {
    const s = v / 255;
    return s <= 0.03928 ? s / 12.92 : Math.pow((s + 0.055) / 1.055, 2.4);
  };
  return 0.2126 * f(c.r) + 0.7152 * f(c.g) + 0.0722 * f(c.b);
}

function contrast(fg, bg) {
  const l1 = lum(fg);
  const l2 = lum(bg);
  return (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05);
}

/** 色合成：fg 以 alpha 覆盖在 bg 上（光晕→底色的合成用）。 */
function over(fg, bg) {
  const a = fg.a === undefined ? 1 : fg.a;
  return { r: fg.r * a + bg.r * (1 - a), g: fg.g * a + bg.g * (1 - a), b: fg.b * a + bg.b * (1 - a) };
}

function rectArea(r) {
  if (!r) return 0;
  return Math.max(0, r.w) * Math.max(0, r.h);
}

function intersectArea(a, b) {
  if (!a || !b) return 0;
  const x0 = Math.max(a.x, b.x);
  const y0 = Math.max(a.y, b.y);
  const x1 = Math.min(a.x + a.w, b.x + b.w);
  const y1 = Math.min(a.y + a.h, b.y + b.h);
  if (x1 <= x0 || y1 <= y0) return 0;
  return (x1 - x0) * (y1 - y0);
}

function contains(outer, inner, eps) {
  const e = eps === undefined ? 0.5 : eps;
  return (
    inner.x >= outer.x - e &&
    inner.y >= outer.y - e &&
    inner.x + inner.w <= outer.x + outer.w + e &&
    inner.y + inner.h <= outer.y + outer.h + e
  );
}

function centerOf(r) {
  return { x: r.x + r.w / 2, y: r.y + r.h / 2 };
}

/** 点是否落在（以 bbox 为轴对齐外接矩形的）椭圆内 —— 用于 circle/ellipse 的真实边界判定。 */
function inEllipse(box, px, py) {
  const rx = box.w / 2;
  const ry = box.h / 2;
  if (rx <= 0 || ry <= 0) return false;
  const dx = (px - (box.x + rx)) / rx;
  const dy = (py - (box.y + ry)) / ry;
  return dx * dx + dy * dy <= 1;
}

/**
 * 图形是否「压住」文字（几何配对核心规则）。
 * 返回规则名（'cover' | 'ellipse' | 'strict'）或 null（不覆盖）。
 */
function coversText(shape, textBox) {
  const tag = shape.tag;
  const area = rectArea(textBox);
  if (!area) return null;
  const inter = intersectArea(textBox, shape.bbox);
  const ratio = inter / area;
  const c = centerOf(textBox);
  if (tag === 'path' || tag === 'polygon') {
    // 保守档：path/polygon 的 bbox 只是几何近似（凹形/曲线内可能有空白）⇒ 仅完全包含时采信。
    return contains(shape.bbox, textBox) ? 'strict' : null;
  }
  if (tag === 'circle' || tag === 'ellipse') {
    // 椭圆档：中心点须落在真实椭圆内（bbox 是外接矩形，直接用 bbox 会误判角落）。
    if (!inEllipse(shape.bbox, c.x, c.y)) return null;
    return ratio >= MIN_COVER_RATIO ? 'ellipse' : null;
  }
  // 矩形档（rect 等实心盒）：中心点在 bbox 内 + 文字大部分落入。
  if (!contains(shape.bbox, { x: c.x, y: c.y, w: 0, h: 0 })) return null;
  return ratio >= MIN_COVER_RATIO ? 'cover' : null;
}

/**
 * 从同一 <svg> 的候选图形里挑出真正压住文字的那一个。
 * 规则：有效 alpha ≥ 0.3 → 覆盖判定 → 取 bbox 面积最小者（最贴近文字的那层）。
 */
function pickCoveringShape(textRec, shapes) {
  const hits = [];
  for (const sh of shapes || []) {
    if (sh.svgId !== textRec.svgId) continue;
    if (!sh.fill) continue;                       // fill=none / transparent / 不可解析
    if (!(sh.alpha >= MIN_SHAPE_ALPHA)) continue; // alpha 过低 ⇒ 不算底色，继续找下一个
    const rule = coversText(sh, textRec.bbox);
    if (!rule) continue;
    hits.push({ shape: sh, rule: rule, area: rectArea(sh.bbox) });
  }
  if (!hits.length) return null;
  hits.sort((a, b) => a.area - b.area);
  return hits[0];
}

/** 光晕是否真的提供了「字形与底色的分离」（否则光晕与字同色 ⇒ 零增益）。 */
function haloProvidesSeparation(textRec, bg) {
  if (!textRec.halo) return false;
  const hc = textRec.halo.stroke;
  if (!hc) return false;
  const eff = over(hc, bg);
  return contrast(eff, bg) >= HALO_MIN_SEPARATION;
}

/**
 * 判定一批文本项（纯数据 in → 判定结果 out）。
 * data = { bodyBg, texts:[...], shapes:[...] }；texts/shapes 由浏览器侧 COLLECT 采集。
 */
function judgeRows(data, opts) {
  const mode = (opts && opts.mode) || 'body';
  const bodyBg = data.bodyBg || { r: 255, g: 255, b: 255 };
  const shapes = data.shapes || [];
  const out = [];
  const seen = new Set();
  for (const t of data.texts || []) {
    const key = String(t.text || '').slice(0, 24);
    if (seen.has(key)) continue;
    seen.add(key);
    const fg = t.fill;
    if (!fg) continue;
    // W1265 既有光晕豁免：body / backdrop 口径下整条跳过（既有行为不变）。
    if (mode !== 'graphic' && t.halo) continue;
    let bg = bodyBg;
    let source = 'body';
    let shapeInfo = null;
    if (mode === 'backdrop' && t.backdrop) {
      bg = t.backdrop;
      source = 'backdrop';
    } else if (mode === 'graphic') {
      const hit = pickCoveringShape(t, shapes);
      if (hit) {
        bg = hit.shape.fill;
        source = 'graphic';
        shapeInfo = { tag: hit.shape.tag, rule: hit.rule, alpha: hit.shape.alpha };
      } else if (t.backdrop) {
        // W1283：无覆盖图形 ⇒ 底色回退到「文字实际所处底色」（最近 CSS backgroundColor），
        // 与页面侧修复工具 site/static/js/label-contrast.js **同源**。
        // 原先回退 body 底色 ⇒ 文字实际在卡片底上时，工具按卡片底判定达标（不修），
        // 而门禁按 body 底色判红 ⇒ **工具与判据口径不一致 ⇒ 改完仍被判红**。
        // （实测 music-structure「孙悟空」：卡片底 CR 3.15 达标 / body 底 CR 2.89 判红）
        bg = t.backdrop;
        source = 'backdrop';
      }
    }
    // graphic 口径：光晕是否有效取决于它与「真实底色」的分离度。
    if (mode === 'graphic' && t.halo && haloProvidesSeparation(t, bg)) continue;
    const cr = contrast(fg, bg);
    const item = {
      text: String(t.text || '').slice(0, 30),
      // fill 字段沿用 W1265 既有键格式（cs.fill 原样串·含空格）⇒ 违例键与既有基线同形可对账
      fill: t.fillCss || 'rgb(' + fg.r + ',' + fg.g + ',' + fg.b + ')',
      bg: 'rgb(' + bg.r + ',' + bg.g + ',' + bg.b + ')',
      cr: Math.round(cr * 100) / 100,
      bg_source: source,
    };
    if (shapeInfo) item.shape = shapeInfo;
    out.push(item);
  }
  return out;
}

/* ------------------------------------------------------------------ *
 * 浏览器侧采集（注入执行·自包含·不得引用模块作用域）
 * ------------------------------------------------------------------ */

const COLLECT = () => {
  function parseColor(str) {
    if (!str) return null;
    const m = String(str).match(/rgba?\(\s*([\d.]+)[,\s]+([\d.]+)[,\s]+([\d.]+)(?:[,\s/]+([\d.]+))?\s*\)/i);
    if (m) return { r: +m[1], g: +m[2], b: +m[3], a: m[4] === undefined ? 1 : +m[4] };
    if (/^#([0-9a-f]{6})$/i.test(str)) {
      const n = parseInt(str.slice(1), 16);
      return { r: (n >> 16) & 255, g: (n >> 8) & 255, b: n & 255, a: 1 };
    }
    if (/^#([0-9a-f]{3})$/i.test(str)) {
      const h = str.slice(1);
      return { r: parseInt(h[0] + h[0], 16), g: parseInt(h[1] + h[1], 16), b: parseInt(h[2] + h[2], 16), a: 1 };
    }
    return null;
  }
  /** getBBox（不含元素自身 transform）+ getCTM（含自身 transform）→ 同一 viewBox 用户空间的轴对齐矩形。 */
  function normBBox(el) {
    let b;
    try {
      b = el.getBBox();
    } catch (e) {
      return null;
    }
    if (!b || (!b.width && !b.height)) return null;
    const pts = [
      [b.x, b.y],
      [b.x + b.width, b.y],
      [b.x, b.y + b.height],
      [b.x + b.width, b.y + b.height],
    ];
    let m = null;
    try {
      m = el.getCTM();
    } catch (e) {
      m = null;
    }
    let xs;
    let ys;
    if (m) {
      xs = pts.map((p) => m.a * p[0] + m.c * p[1] + m.e);
      ys = pts.map((p) => m.b * p[0] + m.d * p[1] + m.f);
    } else {
      xs = pts.map((p) => p[0]);
      ys = pts.map((p) => p[1]);
    }
    const x0 = Math.min.apply(null, xs);
    const x1 = Math.max.apply(null, xs);
    const y0 = Math.min.apply(null, ys);
    const y1 = Math.max.apply(null, ys);
    return { x: x0, y: y0, w: x1 - x0, h: y1 - y0 };
  }
  /** 自元素向上找第一个非透明 CSS backgroundColor（既有 backdrop 口径·原样保留）。 */
  function backdropOf(el) {
    let node = el;
    while (node && node.nodeType === 1) {
      let cs = null;
      try {
        cs = getComputedStyle(node);
      } catch (e) {
        cs = null;
      }
      if (cs) {
        const c = parseColor(cs.backgroundColor);
        if (c && c.a > 0.05) return c;
      }
      node = node.parentElement;
    }
    return null;
  }
  function hidden(el) {
    if (el.closest('defs,clipPath,mask,pattern,marker')) return true;
    const cs = getComputedStyle(el);
    return cs.display === 'none' || cs.visibility === 'hidden';
  }
  const bodyBg = parseColor(getComputedStyle(document.body).backgroundColor) || { r: 255, g: 255, b: 255 };
  const texts = [];
  const shapes = [];
  for (const el of document.querySelectorAll('svg text')) {
    let cs;
    try {
      cs = getComputedStyle(el);
    } catch (e) {
      continue;
    }
    if (!cs || cs.fill === 'none' || cs.visibility === 'hidden' || cs.display === 'none') continue;
    if (parseFloat(cs.opacity || '1') === 0) continue;
    const text = (el.textContent || '').trim();
    if (!text) continue;
    if (hidden(el)) continue;
    const bbox = normBBox(el);
    if (!bbox || (bbox.w === 0 && bbox.h === 0)) continue;
    const fill = parseColor(cs.fill);
    if (!fill) continue;
    const halo =
      (cs.paintOrder || '').includes('stroke') && parseFloat(cs.strokeWidth) >= 1 && cs.stroke !== 'none'
        ? { stroke: parseColor(cs.stroke), width: parseFloat(cs.strokeWidth) }
        : null;
    texts.push({
      svgId: el.ownerSVGElement ? el.ownerSVGElement.id || '' : '',
      text: text,
      fill: fill,
      fillCss: cs.fill, // 原样 computed 串（W1265 既有键格式·违例键靠它对账既有基线）
      halo: halo,
      backdrop: backdropOf(el),
      bbox: bbox,
    });
  }
  /** 视觉实际填充色 = computed fill × filter 的 brightness 系数（与页面侧修复工具同源）。 */
  function effectiveFill(scs, raw) {
    if (!raw) return raw;
    const fm = String(scs.filter || '').match(/brightness\(([\d.]+)\)/);
    if (!fm) return raw;
    const k = parseFloat(fm[1]);
    if (!k || isNaN(k) || k === 1) return raw;
    return {
      r: Math.min(255, raw.r * k),
      g: Math.min(255, raw.g * k),
      b: Math.min(255, raw.b * k),
      a: raw.a,
    };
  }

  for (const sh of document.querySelectorAll('rect,circle,ellipse,path,polygon')) {
    if (!sh.ownerSVGElement) continue;
    const scs = getComputedStyle(sh);
    if (scs.display === 'none' || scs.visibility === 'hidden') continue;
    if (hidden(sh)) continue;
    const bbox = normBBox(sh);
    if (!bbox || (bbox.w === 0 && bbox.h === 0)) continue;
    const rawFill = parseColor(scs.fill);
    const fillAlpha = rawFill ? rawFill.a : 0;
    const alpha =
      fillAlpha * parseFloat(scs.fillOpacity || '1') * parseFloat(scs.opacity || '1');
    // W1283：**视觉实际底色** = computed fill × filter 的 brightness 系数。
    // 公共层在暗色态会给图形加 brightness() 提亮（实测 #8E7D62 → rgb(193,190,139)），
    // computed fill 仍是原色 ⇒ 不乘系数则暗态底色算错 ⇒ 与页面侧修复工具口径不一致
    // （工具已乘·判据未乘 ⇒ 工具改完仍被判红）。
    const fill = effectiveFill(scs, rawFill);
    shapes.push({
      svgId: sh.ownerSVGElement.id || '',
      tag: sh.tagName.toLowerCase(),
      bbox: bbox,
      fill: fill,
      alpha: alpha,
    });
  }
  return { bodyBg: bodyBg, texts: texts, shapes: shapes };
};

/* ------------------------------------------------------------------ *
 * 自测（node 侧负样本·同一套判定实现·供门禁自测与 pytest 复用）
 * ------------------------------------------------------------------ */

function selftest() {
  const cases = [];
  const bodyBg = { r: 250, g: 247, b: 240 }; // #FAF7F0 纸底
  const mk = (o) => {
    const box = { x: o.x, y: o.y, w: o.w, h: o.h };
    return {
      svgId: 's',
      text: o.text || 'T',
      fill: parseColor(o.fill || '#ffffff'),
      halo: o.halo || null,
      backdrop: null,
      bbox: box,
    };
  };
  const rect = (o) => ({
    svgId: 's',
    tag: o.tag || 'rect',
    bbox: { x: o.x, y: o.y, w: o.w, h: o.h },
    fill: parseColor(o.fill),
    alpha: o.alpha === undefined ? 1 : o.alpha,
  });

  // 1) 白字压浅色块 #e9b885 ⇒ 真实 CR 1.80 ⇒ 判红（几何命中 + 真实底色）。
  {
    const t = mk({ x: 10, y: 10, w: 80, h: 20, fill: '#ffffff' });
    const shapes = [rect({ x: 0, y: 0, w: 200, h: 100, fill: '#e9b885' })];
    const items = judgeRows({ bodyBg, texts: [t], shapes }, { mode: 'graphic' });
    const cr = items[0] ? items[0].cr : null;
    cases.push({
      name: '白字压浅色块 #e9b885 ⇒ CR 1.80 < 3.0 判红',
      id: 'light_block_red',
      ok: !!items[0] && items[0].cr < 3.0 && items[0].bg_source === 'graphic',
      detail: 'cr=' + (items[0] ? items[0].cr : 'n/a'),
    });
  }
  // 2) 白字压深色块 ⇒ 高对比 ⇒ 判绿。
  {
    const t = mk({ x: 10, y: 10, w: 80, h: 20, fill: '#ffffff' });
    const shapes = [rect({ x: 0, y: 0, w: 200, h: 100, fill: '#3A473A' })];
    const items = judgeRows({ bodyBg, texts: [t], shapes }, { mode: 'graphic' });
    cases.push({
      name: '白字压深色块 #3A473A ⇒ CR ≥ 3.0 判绿',
      id: 'dark_block_green',
      ok: !!items[0] && items[0].cr >= 3.0,
      detail: 'cr=' + (items[0] ? items[0].cr : 'n/a'),
    });
  }
  // 3) 假阳性防护：文字**旁边**有深色块（不相交）⇒ 不得误配为底色 ⇒ 回退 body ⇒ 判绿。
  {
    const t = mk({ x: 10, y: 10, w: 80, h: 20, fill: '#1a1410' });
    const shapes = [rect({ x: 300, y: 0, w: 100, h: 100, fill: '#2a1a10' })];
    const items = judgeRows({ bodyBg, texts: [t], shapes }, { mode: 'graphic' });
    cases.push({
      name: '文字旁边有深色块（不相交）⇒ 不误判为底色（回退 body·判绿）',
      id: 'adjacent_block_no_false_positive',
      ok: !!items[0] && items[0].bg_source === 'body' && items[0].cr >= 3.0,
      detail: 'cr=' + (items[0] ? items[0].cr : 'n/a') + ' src=' + (items[0] ? items[0].bg_source : 'n/a'),
    });
  }
  // 4) path 保守档：bbox 只部分覆盖（中心在内、边缘溢出）⇒ 不算覆盖 ⇒ 回退 body ⇒ 判绿；
  //    同一几何若按矩形宽松档则会命中（矩形档：中心在内 + 交集比 0.6 ⇒ 命中）。
  {
    const t = mk({ x: 40, y: 10, w: 100, h: 30, fill: '#1a1410' });
    const pathShape = rect({ x: 0, y: 0, w: 100, h: 50, tag: 'path', fill: '#2a1a10' });
    const rectShape = rect({ x: 0, y: 0, w: 100, h: 50, tag: 'rect', fill: '#2a1a10' });
    const pathItems = judgeRows({ bodyBg, texts: [t], shapes: [pathShape] }, { mode: 'graphic' });
    const rectItems = judgeRows({ bodyBg, texts: [t], shapes: [rectShape] }, { mode: 'graphic' });
    cases.push({
      name: 'path 保守档：bbox 未完全包含文字 ⇒ 不算覆盖（矩形档则会命中）',
      id: 'path_conservative',
      ok:
        !!pathItems[0] &&
        pathItems[0].bg_source === 'body' &&
        !!rectItems[0] &&
        rectItems[0].bg_source === 'graphic',
      detail:
        'path=' + (pathItems[0] ? pathItems[0].bg_source : 'n/a') +
        ' rect=' + (rectItems[0] ? rectItems[0].bg_source : 'n/a'),
    });
  }
  // 5) 多层重叠 ⇒ 取面积最小（最贴近文字）的那层。
  {
    const t = mk({ x: 10, y: 10, w: 80, h: 20, fill: '#ffffff' });
    const shapes = [
      rect({ x: 0, y: 0, w: 200, h: 100, fill: '#8E7D62' }),
      rect({ x: 5, y: 5, w: 100, h: 40, fill: '#3A473A' }),
    ];
    const items = judgeRows({ bodyBg, texts: [t], shapes }, { mode: 'graphic' });
    cases.push({
      name: '多层重叠 ⇒ 取面积最小（最贴近文字）的那层',
      id: 'min_area_layer',
      ok: !!items[0] && items[0].bg === 'rgb(58,71,58)',
      detail: 'bg=' + (items[0] ? items[0].bg : 'n/a'),
    });
  }
  // 6) alpha 过低 / fill none 的图形 ⇒ 跳过继续找（或回退 body）。
  {
    const t = mk({ x: 10, y: 10, w: 80, h: 20, fill: '#ffffff' });
    const shapes = [
      rect({ x: 0, y: 0, w: 200, h: 100, fill: '#e9b885', alpha: 0.1 }),
      rect({ x: 0, y: 0, w: 200, h: 100, fill: '#3A473A', alpha: 1 }),
    ];
    const items = judgeRows({ bodyBg, texts: [t], shapes }, { mode: 'graphic' });
    cases.push({
      name: '低 alpha 图形跳过 ⇒ 取下一个有效图形',
      id: 'low_alpha_skip',
      ok: !!items[0] && items[0].bg === 'rgb(58,71,58)',
      detail: 'bg=' + (items[0] ? items[0].bg : 'n/a'),
    });
  }
  // 7) 光晕有效性：白字 + 白晕压浅橙块 ⇒ 光晕零增益 ⇒ 不豁免 ⇒ 判红。
  {
    const t = mk({
      x: 10, y: 10, w: 80, h: 20, fill: '#ffffff',
      halo: { stroke: parseColor('rgba(255, 255, 255, 0.88)'), width: 3 },
    });
    const shapes = [rect({ x: 0, y: 0, w: 200, h: 100, fill: '#e9b885' })];
    const items = judgeRows({ bodyBg, texts: [t], shapes }, { mode: 'graphic' });
    cases.push({
      name: '白字+白晕压浅橙块 ⇒ 光晕零增益 ⇒ 不豁免 ⇒ 判红',
      id: 'halo_zero_gain',
      ok: !!items[0] && items[0].cr < 3.0,
      detail: 'cr=' + (items[0] ? items[0].cr : 'n/a'),
    });
  }
  // 8) 既有口径行为不变：body 口径下带光晕的文字仍整条跳过（W1265 既有行为）。
  {
    const t = mk({
      x: 10, y: 10, w: 80, h: 20, fill: '#ffffff',
      halo: { stroke: parseColor('rgba(255, 255, 255, 0.88)'), width: 3 },
    });
    const bodyItems = judgeRows({ bodyBg, texts: [t], shapes: [] }, { mode: 'body' });
    const graphicItems = judgeRows({ bodyBg, texts: [t], shapes: [] }, { mode: 'graphic' });
    cases.push({
      name: '既有 body 口径：光晕豁免仍整条跳过（行为未变）',
      id: 'body_mode_unchanged',
      ok: bodyItems.length === 0 && graphicItems.length === 1,
      detail: 'body=' + bodyItems.length + ' graphic=' + graphicItems.length,
    });
  }
  // 9) W1283 新口径：graphic 口径下**无覆盖图形** ⇒ 回退最近 CSS 背景（backdrop），
  //    而非 body 底色——与页面侧修复工具 site/static/js/label-contrast.js 同源。
  {
    const t = mk({ x: 10, y: 10, w: 80, h: 20, fill: '#9a8c78' });
    t.backdrop = { r: 252, g: 250, b: 244 };
    const items = judgeRows({ bodyBg, texts: [t], shapes: [] }, { mode: 'graphic' });
    cases.push({
      name: 'graphic 无覆盖图形 ⇒ 回退最近 CSS 背景（与页面修复工具同源）',
      id: 'graphic_backdrop_fallback',
      ok: !!items[0] && items[0].bg_source === 'backdrop' && items[0].bg === 'rgb(252,250,244)',
      detail: items[0] ? ('src=' + items[0].bg_source + ' bg=' + items[0].bg + ' cr=' + items[0].cr) : 'n/a',
    });
  }
  const passed = cases.filter((c) => c.ok).length;
  return { total: cases.length, passed: passed, ok: passed === cases.length, cases: cases };
}

/* ------------------------------------------------------------------ *
 * 页面枚举 / 采集执行
 * ------------------------------------------------------------------ */

/** 图表页枚举：含 '<svg' 的 HTML（data + en）。 */
function listPages() {
  const out = [];
  const dirs = [];
  if (SCOPE === 'data' || SCOPE === 'all') dirs.push(['data', path.join(SITE, 'data')]);
  if (SCOPE === 'en' || SCOPE === 'all') dirs.push(['en', path.join(SITE, 'en')]);
  for (const [label, dir] of dirs) {
    if (!fs.existsSync(dir)) continue;
    for (const f of fs.readdirSync(dir).sort()) {
      if (!f.endsWith('.html')) continue;
      if (f.startsWith('_')) continue;
      const abs = path.join(dir, f);
      let txt;
      try {
        txt = fs.readFileSync(abs, 'utf8');
      } catch {
        continue;
      }
      if (!/<svg[\s>]/i.test(txt)) continue;
      out.push({ rel: label + '/' + f, abs });
    }
  }
  return out.slice(0, LIMIT);
}

async function waitStable(page, maxMs) {
  const deadline = Date.now() + maxMs;
  let prev = null;
  while (Date.now() < deadline) {
    const cur = await page.evaluate(() => {
      const svgs = document.querySelectorAll('svg');
      const texts = document.querySelectorAll('svg text');
      return svgs.length + '|' + texts.length + '|' + document.body.scrollHeight;
    });
    if (prev !== null && cur === prev) return;
    prev = cur;
    await page.waitForTimeout(120);
  }
}

async function measureState(context, pageRec, state) {
  const page = await context.newPage();
  const errors = [];
  page.on('pageerror', (e) => errors.push(String(e.message).slice(0, 80)));
  const url = 'file:///' + pageRec.abs.replace(/\\/g, '/');
  try {
    await page.emulateMedia({ colorScheme: state.colorScheme });
    await page.setViewportSize(state.viewport);
    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 20000 });
    await waitStable(page, 1200);
    await page.evaluate(async () => {
      const step = window.innerHeight;
      for (let y = 0; y < document.body.scrollHeight; y += step) {
        window.scrollTo(0, y);
        await new Promise((r) => setTimeout(r, 100));
      }
      window.scrollTo(0, 0);
    });
    await waitStable(page, 1200);
    const data = await page.evaluate(COLLECT);
    const items = judgeRows(data, { mode: BG_MODE });
    return {
      page: pageRec.rel,
      state: state.id,
      svgTextCount: items.length,
      items: items,
      errors: errors.slice(0, 2),
    };
  } catch (e) {
    return { page: pageRec.rel, state: state.id, fatal: String(e.message).slice(0, 120) };
  } finally {
    await page.close();
  }
}

async function main() {
  const pages = listPages();
  const browser = await chromium.launch();
  const rows = [];
  console.log('页面 ' + pages.length + ' · 状态 ' + STATES.length + ' · conc=' + CONC + ' · 底色口径=' + BG_MODE);
  for (const state of STATES) {
    const context = await browser.newContext({ viewport: state.viewport });
    let idx = 0;
    const worker = async () => {
      for (;;) {
        const i = idx++;
        if (i >= pages.length) break;
        const row = await measureState(context, pages[i], state);
        rows.push(row);
        const low = (row.items || []).filter((x) => x.cr < THRESHOLD).length;
        if (low) console.log('  ' + row.page + ' ' + state.id + ' 低对比 ' + low + ' 处');
      }
    };
    await Promise.all(Array.from({ length: Math.min(CONC, pages.length) }, worker));
    await context.close();
  }
  await browser.close();

  const fatals = rows.filter((r) => r.fatal);
  const summary = {};
  let violations = 0;
  const perPage = {};
  for (const r of rows) {
    const low = (r.items || []).filter((x) => x.cr < THRESHOLD);
    if (!low.length) continue;
    violations += low.length;
    summary[r.page] = summary[r.page] || { page: r.page, states: {}, total: 0 };
    summary[r.page].states[r.state] = low;
    summary[r.page].total += low.length;
  }
  const report = {
    generated_at: new Date().toISOString(),
    threshold: THRESHOLD,
    scope: SCOPE,
    bg_mode: BG_MODE,
    states: STATES.map((s) => s.id),
    pages_scanned: pages.length,
    rows: rows.length,
    fatal_rows: fatals.length,
    violations: violations,
    pages_with_violations: Object.keys(summary).length,
    by_page: summary,
  };
  fs.mkdirSync(path.dirname(OUT), { recursive: true });
  fs.writeFileSync(OUT, JSON.stringify(report, null, 1), 'utf8');
  console.log(
    '完成：页面 ' + pages.length + ' · 行 ' + rows.length + ' · 低对比 ' + violations + ' 处 · 违例页 ' +
      Object.keys(summary).length + ' · fatal ' + fatals.length + ' → ' + path.relative(ROOT, OUT)
  );
  // fail-closed：全部探针失败 ⇒ 非零退出（不得产出 100% 无效产物）
  if (rows.length && fatals.length === rows.length) {
    console.error('FAIL 全部探针失败（' + fatals.length + '/' + rows.length + '）——产物无效·非零退出');
    process.exit(3);
  }
  if (fatals.length) {
    console.log('NOTE 部分探针失败（' + fatals.length + '/' + rows.length + '）——须人工确认');
  }
}

module.exports = {
  THRESHOLD: THRESHOLD,
  MIN_COVER_RATIO: MIN_COVER_RATIO,
  MIN_SHAPE_ALPHA: MIN_SHAPE_ALPHA,
  HALO_MIN_SEPARATION: HALO_MIN_SEPARATION,
  COLLECT: COLLECT,
  parseColor: parseColor,
  lum: lum,
  contrast: contrast,
  over: over,
  rectArea: rectArea,
  intersectArea: intersectArea,
  contains: contains,
  inEllipse: inEllipse,
  coversText: coversText,
  pickCoveringShape: pickCoveringShape,
  haloProvidesSeparation: haloProvidesSeparation,
  judgeRows: judgeRows,
  selftest: selftest,
};

if (require.main === module) {
  if (process.argv.indexOf('--self-test') > -1) {
    const st = selftest();
    if (process.argv.indexOf('--json') > -1) {
      console.log(JSON.stringify(st));
    } else {
      for (const c of st.cases) {
        console.log((c.ok ? 'OK  ' : 'FAIL') + ' ' + c.name + '：' + c.detail);
      }
      console.log('自测 ' + st.passed + '/' + st.total + ' 通过');
    }
    process.exit(st.ok ? 0 : 2);
  }
  if (BG_MODE_RAW !== BG_MODE) {
    console.log('NOTE 未知 --bg-mode「' + BG_MODE_RAW + '」⇒ 回退 body（可选 body|backdrop|graphic）');
  }
  main().catch((e) => {
    console.error(e);
    process.exit(1);
  });
}
