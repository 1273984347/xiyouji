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
 * 用法：node scripts/svg_text_contrast_probe.js [--scope data|en|root|all|data,en] [--out F] [--limit N] [--conc N]
 *
 * --scope 支持逗号组合（W1285）：两个口径的**扫描面有意不同**——
 *   · graphic 口径（W1282 起·图形底色口径）⇒ 用 `--scope all`（含站点根）；
 *   · body 口径（W1265 建立·页面底色粗口径）⇒ 用 `--scope data,en`（保持原定义）。
 *     body 口径对「文字压在色块/卡片上」会产生**语义性假红**（它只取页面底色比对·
 *     而这些文字实际压在深色块上、由 graphic 口径判定）⇒ 若把根页也纳入 body 判定面，
 *     会凭空多出 dashboard 的 16 条假红（KPI 大数字白字压卡片）⇒ 故 body 口径不随 root 扩大。
 *       [--bg-mode body|backdrop|graphic] [--self-test [--json]]
 */
'use strict';

const fs = require('fs');
const path = require('path');
// W1286：**惰性加载 playwright**——自测（--self-test）是纯数据判定·不启浏览器；
//   而顶部直接 require('playwright') 会让「未装 playwright 的环境」（CI 的 pytest job
//   按设计不装浏览器）连自测都跑不起来 ⇒ 模块缺失即判红（实证 W1282 引入的用例）。
//   真跑（main）时才 require ⇒ 自测零依赖。
let chromium = null;
function _chromium() {
  if (!chromium) ({ chromium } = require('playwright'));
  return chromium;
}

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
// W1286 L-01：--pages 限定扫描页（逗号分隔 rel 路径）· --no-tool 禁用公共工具 label-contrast.js
//   ⇒ 用途：复现「公共工具失效时暴露」的**源级**标签低对比（官方口径同源·非临时脚本）
const ONLY_PAGES = String(argValue('--pages', '')).trim();
const NO_TOOL = process.argv.indexOf('--no-tool') > -1;
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

/** 视觉实际填充色 = computed fill x filter 的 brightness 系数（与页面侧修复工具同源·W1283）。 */
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
    const rawKey = String(t.text || '').slice(0, 24);
    const fg = t.fill;
    if (!fg) continue;
    // W1265 既有光晕豁免：body / backdrop 口径下整条跳过（既有行为不变）。
    if (mode !== 'graphic' && t.halo) continue;
    // W1285（F6）：**body 与 graphic 两口径职责分离**——body 口径只判「不压任何图形的文字 vs 页面底色」；
    //   文字若**压在图形上** ⇒ 交由 graphic 口径判（它取的是**图形底色**·更精确）。
    //   ⇒ 两口径不重叠 ⇒ body 口径不再产生「文字压色块却被粗口径判红」的语义性假红
    //   （实测 data/monster-ecology-network.html 的 8 条即此类：文字压在雷达图色块上·实际可读）。
    if (mode !== 'graphic' && pickCoveringShape(t, shapes)) continue;
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
    // W1285：去重键 = 所属 SVG + 文案 + **底色来源 + 底色值**（去重时机在底色确定之后）。
    //   原键只有文案 ⇒ **同页同名但落在不同底色的**文字只判第一个 ⇒ 其一被漏判
    //   （实测同页「无底洞·最后大难」出现在两处、底色不同 ⇒ 一处被掩盖）。
    //   现键含底色维度 ⇒ 同底色的重复仍去重（保留既有语义与基线可对账性），不同底色分别判定。
    const key = String(t.svgId || '') + '|' + rawKey + '|' + source + '|' + ('rgb(' + bg.r + ',' + bg.g + ',' + bg.b + ')');
    if (seen.has(key)) continue;
    seen.add(key);
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
  // COLLECT 是**注入浏览器执行**的独立作用域函数 ⇒ 模块级函数在此不可见
  // ⇒ 需在函数内部有一份同名副本（与模块级实现逐字同源·W1284）。
  //
  // W1284：**匿名 SVG 的稳定标识**——页面里多个 <svg> 没有 id 时，原实现一律取 ''
  // ⇒ texts 与 shapes 全部归进同一组 ⇒ 一幅 SVG 的文字会被几何配对到**另一幅 SVG**
  // 的图形上（实测 famous-time-travel：明信片正文被配到另一幅插画的矩形·CR 2.10 假红）。
  // ⇒ 改为按 DOM 顺序给无 id 的 SVG 分配稳定键（'#anon-N'），同页多 SVG 互不串扰。
  const __svgKeys = new Map();
  Array.prototype.forEach.call(document.querySelectorAll('svg'), (sv, i) => {
    __svgKeys.set(sv, sv.id || ('#anon-' + i));
  });
  const __svgKeyOf = (el) => {
    const sv = el && el.ownerSVGElement;
    if (!sv) return '';
    const k = __svgKeys.get(sv);
    return k !== undefined ? k : (sv.id || '');
  };
  const effectiveFill = (scs, raw) => {
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
  };
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
      svgId: __svgKeyOf(el),
      text: text,
      fill: fill,
      fillCss: cs.fill, // 原样 computed 串（W1265 既有键格式·违例键靠它对账既有基线）
      halo: halo,
      backdrop: backdropOf(el),
      bbox: bbox,
    });
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
      svgId: __svgKeyOf(sh),
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
      svgId: o.svgId || 's',
      text: o.text || 'T',
      fill: parseColor(o.fill || '#ffffff'),
      halo: o.halo || null,
      backdrop: o.backdrop ? parseColor(o.backdrop) : null,
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
  // 10) W1283/W1284：图形底色须乘 filter 的 brightness 系数（暗色态公共层提亮图形）
  {
    const raw = { r: 142, g: 125, b: 98, a: 1 };
    const bright = effectiveFill({ filter: 'brightness(1.45) saturate(1.05)' }, raw);
    const plain = effectiveFill({ filter: 'none' }, raw);
    const ok1 = Math.abs(bright.r - Math.min(255, 142 * 1.45)) < 0.01 && bright.g > raw.g;
    const ok2 = plain.r === raw.r && plain.g === raw.g && plain.b === raw.b;
    cases.push({
      name: '图形底色乘 brightness 系数（暗色态视觉实际色）',
      id: 'effective_fill_brightness',
      ok: ok1 && ok2,
      detail: 'bright=' + JSON.stringify(bright) + ' plain=' + JSON.stringify(plain),
    });
  }
  // 11) W1285：去重键含底色维度 ⇒ 同页**同名但底色不同**的文字分别判定；同底色仍去重。
  {
    const mkBg = (x, bg) => mk({ x: x, y: 0, w: 10, h: 10, fill: '#9a8c78', text: '同名', backdrop: bg });
    const items = judgeRows(
      {
        bodyBg,
        texts: [mkBg(0, '#f5f0e4'), mkBg(20, '#fcfaf4'), mkBg(40, '#f5f0e4')],
        shapes: [],
      },
      { mode: 'backdrop' }
    );
    const bgs = items.map((i) => i.bg).sort();
    cases.push({
      name: '同名不同底色分别判定（去重键含底色维度）·同底色仍去重',
      id: 'dedup_includes_backdrop',
      ok: items.length === 2 && bgs[0] === 'rgb(245,240,228)' && bgs[1] === 'rgb(252,250,244)',
      detail: 'n=' + items.length + ' bgs=' + JSON.stringify(bgs),
    });
  }
  // 12) 稳定判据须排除「平凡解」：指纹相同但**尚未渲染出任何图表元素**时不得判为稳定
  //     （W1285 实证：同一页单页跑判出 2 条违例、全站跑判 0 条 ⇒ 静默漏检）
  {
    const unrendered = isStableState('sig', 'sig', 0, true);
    const rendered = isStableState('sig', 'sig', 12, true);
    const changed = isStableState('sig', 'sig2', 12, true);
    const first = isStableState(null, 'sig', 12, true);
    const noReq = isStableState('sig', 'sig', 0, false);
    cases.push({
      name: '稳定判据排除平凡解（未渲染⇒不算稳定；渲染后⇒稳定；指纹变化⇒不稳定）',
      id: 'stability_excludes_trivial_solution',
      ok: unrendered === false && rendered === true && changed === false && first === false && noReq === true,
      detail: 'unrendered=' + unrendered + ' rendered=' + rendered + ' changed=' + changed + ' first=' + first + ' noReq=' + noReq,
    });
  }
  // 13) body 与 graphic 两口径**职责分离**：压在图形上的文字交由 graphic 口径判
  //     （body 粗口径只取「文字 vs 页面底色」⇒ 对「文字压色块」会产生语义性假红）
  {
    const t = mk({ x: 10, y: 10, w: 80, h: 20, fill: '#ffffff' });
    const shapes = [rect({ x: 0, y: 0, w: 200, h: 100, fill: '#e9b885' })];
    const bodyItems = judgeRows({ bodyBg, texts: [t], shapes }, { mode: 'body' });
    const graphicItems = judgeRows({ bodyBg, texts: [t], shapes }, { mode: 'graphic' });
    cases.push({
      name: 'body 口径跳过「压在图形上的文字」（交由 graphic 口径判·两口径职责不重叠）',
      id: 'body_graphic_separation',
      ok: bodyItems.length === 0 && graphicItems.length === 1 && graphicItems[0].bg_source === 'graphic',
      detail: 'body=' + bodyItems.length + ' graphic=' + graphicItems.length + ' src=' + (graphicItems[0] && graphicItems[0].bg_source),
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
  // W1285：scope 支持逗号组合（如 `data,en`）⇒ 两个口径可各自界定扫描面。
  const SCOPE_SET = new Set(String(SCOPE).split(',').map((s) => s.trim()).filter(Boolean));
  if (SCOPE_SET.has('data') || SCOPE_SET.has('all')) dirs.push(['data', path.join(SITE, 'data')]);
  if (SCOPE_SET.has('en') || SCOPE_SET.has('all')) dirs.push(['en', path.join(SITE, 'en')]);
  // W1285：**根页纳入扫描面**——此前只扫 site/data + site/en ⇒ 站点根的含图页
  //   （about / curated / dashboard / dukou-engine / guide / index）从未被测过。
  //   根页 rel 前缀为空（路径深度与子站不同⇒ 公共工具的引入路径也不同）。
  if (SCOPE_SET.has('root') || SCOPE_SET.has('all')) dirs.push(['', SITE]);
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
      // 根页 label 为空 ⇒ rel 不得带前导斜杠（否则路径解析多一层）
      out.push({ rel: label ? label + '/' + f : f, abs });
    }
  }
  const list = out.slice(0, LIMIT);
  if (!ONLY_PAGES) return list;
  const want = new Set(ONLY_PAGES.split(',').map((s) => s.trim()).filter(Boolean));
  return list.filter((p) => want.has(p.rel));
}

/**
 * W1285：稳定判据的「平凡解」排除（跨项目通用·与 E-292「产物必须校验 fatal」同族的「静默失效」族）。
 *
 * 病根：稳定判据原为「指纹连续两次相同」——但**页面尚未渲染出任何图表文字时，
 * 指纹同样是「两次相同」**（0 个 svg text + 不变化的 scrollHeight）⇒ 会**立即**被判定为
 * 「已稳定」并返回 ⇒ 采到未渲染状态 ⇒ 该页该态的真违例被**静默漏检**。
 *
 * 实测（W1285）：同一页、同一份代码，单页跑判出 2 条违例（S4 移动亮态），
 * 全站跑判 0 条 ⇒ 「全站 0 条」的收官结论**不可复现**。
 *
 * 修法：稳定须同时满足「指纹相同」**且**「已产出文字」（requireText）；
 * 判定拆为**纯函数**，单测可直接断言（不必起浏览器）。
 */
function isStableState(prevSig, curSig, readyCount, requireText) {
  if (prevSig === null || prevSig !== curSig) return false;
  if (requireText && !(readyCount > 0)) return false; // 平凡解：脚本尚未渲染出图表
  return true;
}

async function waitStable(page, maxMs, opts) {
  const requireText = !!(opts && opts.requireText);
  // W1285：要求**连续 3 次**指纹相同（原为 2 次）——抗抖动更强：
  //   图表常有「颜色渐变/淡入」动画，2 次相同可能在动画的「平台期」误判为稳定。
  const minSame = (opts && opts.minSame) || 3;
  const deadline = Date.now() + maxMs;
  let prev = null;
  let sameCount = 0;
  let lastTextCount = 0;
  while (Date.now() < deadline) {
    // W1284：稳定判据须含**样式指纹**，不能只看数量——
    //   图表常有「颜色渐变/淡入」动画（文字 fill 由数据色渐变到公共层映射色），
    //   只看数量会在动画中途提前返回 ⇒ 采到中间态颜色 ⇒ **假阳性**
    //   （实测 pilgrim-team「无底洞·最后大难」：动画完成是深墨 CR 14，
    //     动画中途是浅金 CR 2.85 ⇒ 门禁误判）。
    const cur = await page.evaluate(() => {
      const svgs = document.querySelectorAll('svg');
      const texts = document.querySelectorAll('svg text');
      const step = Math.max(1, Math.ceil(texts.length / 40));
      let sig = '';
      for (let i = 0; i < texts.length; i += step) {
        const cs = getComputedStyle(texts[i]);
        // W1285（F8）：指纹须含**显示态**——否则「标签被脚本延迟隐藏」（共享 avoidall 的
        //   1200/3000/6000/9000/12000ms display:none）不可见 ⇒ 稳定判据看不见「时隐时现」
        //   ⇒ 同一页在不同次跑动里可见标签集合不同 ⇒ 采集结果随时刻波动。
        sig += cs.fill + ',' + cs.opacity + ',' + cs.strokeWidth + ',' + cs.display + ',' + cs.visibility + ';';
      }
      // W1285（F9 修正版）：readyCount = 已渲染产出的元素数（文字 **或** 图形）。
      //   ⚠ 曾一度严格限定「图表级 svg」（viewBox 宽 ≥150 / 渲染宽 ≥200）⇒ **误伤 48 行**：
      //   实测 en/graph-explorer 等页的图表**滚出视口即卸载**（懒渲染）⇒ 采集时 texts=0、
      //   且其 svg 被判为「非图表级」⇒ readyCount=0 ⇒ 永不稳定 ⇒ 退出码 4。
      //   而这些页在**首屏**是有图表与文字的（单页实测 graph-explorer 首屏 texts=40）⇒
      //   判定面并非缺失，只是采集时刻被卸载 ⇒ 不该判 unstable。
      //   ⇒ 回到全局计数（装饰 svg 会让 readyCount 恒 >0·属可接受的保守），
      //     并把「该页该态 textCount=0」**显式记为 empty_rows**（判定面为空·非不稳定）。
      const shapes = document.querySelectorAll('svg path, svg rect, svg circle, svg polygon, svg ellipse');
      const readyCount = texts.length + shapes.length;
      return { sig: svgs.length + '|' + texts.length + '|' + document.body.scrollHeight + '|' + sig,
               readyCount: readyCount, textCount: texts.length };
    });
    lastTextCount = cur.textCount;
    if (isStableState(prev, cur.sig, cur.readyCount, requireText)) {
      sameCount += 1;
      if (sameCount >= minSame) return { stable: true, textCount: cur.textCount };
    } else {
      sameCount = 0;
    }
    prev = cur.sig;
    await page.waitForTimeout(120);
  }
  return { stable: false, textCount: lastTextCount };
}

async function measureState(context, pageRec, state) {
  const page = await context.newPage();
  const errors = [];
  page.on('pageerror', (e) => errors.push(String(e.message).slice(0, 80)));
  const url = 'file:///' + pageRec.abs.replace(/\\/g, '/');
  try {
    // W1286 L-01：--no-tool ⇒ 拦掉公共工具 label-contrast.js（模拟「工具失效」场景）
    if (NO_TOOL) await page.route('**/label-contrast.js', (r) => r.abort());
    await page.emulateMedia({ colorScheme: state.colorScheme });
    await page.setViewportSize(state.viewport);
    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 20000 });
    let s1 = await waitStable(page, 3000, { requireText: true });
    await page.evaluate(async () => {
      const step = window.innerHeight;
      for (let y = 0; y < document.body.scrollHeight; y += step) {
        window.scrollTo(0, y);
        await new Promise((r) => setTimeout(r, 100));
      }
      window.scrollTo(0, 0);
    });
    let s2 = await waitStable(page, 3000, { requireText: true });
    // W1285：慢渲染/长动画页 ⇒ 放宽超时**重试一次**（仍未稳定才记 unstable ⇒ 门禁 fail-closed）
    if (!(s1.stable && s2.stable)) {
      await page.waitForTimeout(600);
      s1 = await waitStable(page, 9000, { requireText: true });
      s2 = await waitStable(page, 9000, { requireText: true });
    }
    const data = await page.evaluate(COLLECT);
    const items = judgeRows(data, { mode: BG_MODE });
    // W1285：两处等待只要有一处未稳定 ⇒ 该行不可信 ⇒ 记 unstable ⇒ 门禁 fail-closed。
    //   ⚠ 例外：**该页该态 textCount=0**（采集时刻无任何 svg 文字）⇒ 判定面**为空** ⇒
    //   无可判内容 ⇒ 不产生漏检 ⇒ 不记 unstable，改记 empty（报告里显式可见·供人工抽查）。
    //   （实测此类页多为「图表滚出视口即卸载」的懒渲染页：en/graph-explorer 等 48 行。）
    const empty = (s1.textCount === 0 && s2.textCount === 0);
    const unstable = !(s1.stable && s2.stable) && !empty;
    return {
      page: pageRec.rel,
      state: state.id,
      svgTextCount: items.length,
      items: items,
      errors: errors.slice(0, 2),
      unstable: unstable,
      // W1285：empty = 采集时刻该页该态**无任何 svg 文字** ⇒ 判定面为空（无可判内容）
      //   ⇒ 不记 unstable（不产生漏检），但在报告里显式可见（供人工抽查「是否有漏渲染」）。
      empty: empty && !(s1.stable && s2.stable),
      unstableReason: unstable
        ? ('s1=' + (s1.stable ? 'stable' : 'unstable(text=' + s1.textCount + ')') +
           ' s2=' + (s2.stable ? 'stable' : 'unstable(text=' + s2.textCount + ')'))
        : (empty && !(s1.stable && s2.stable) ? 'empty(判定面为空·采集时刻无 svg 文字)' : ''),
      // W1284：页面内容哈希（防漂移锚点·与第 82 槽渲染档案同款机制）——
      // 报告入库后若页面被改而探针未重跑 ⇒ 报告陈旧 ⇒ 门禁须 fail-closed（否则漏检）。
      sha: pageSha(pageRec.abs),
    };
  } catch (e) {
    return { page: pageRec.rel, state: state.id, fatal: String(e.message).slice(0, 120) };
  } finally {
    await page.close();
  }
}

/** 页面内容哈希前 12 位（防漂移锚点·与第 82 槽 _page_sha 同款）。
 *  W1286：按仓内规范（LF）归一后计算——`.gitattributes` 声明 `* text=auto eol=lf`
 *    ⇒ blob 恒为 LF，Windows 工作树因 core.autocrlf=true 为 CRLF
 *    ⇒ 不归一则本地报告的 sha 与 CI 上 blob 的 sha 永不相等 ⇒ CI 恒判「报告陈旧」。 */
function pageSha(absPath) {
  try {
    const raw = require('fs').readFileSync(absPath).toString('binary').replace(/\r\n/g, '\n').replace(/\r/g, '\n');
    const buf = Buffer.from(raw, 'binary');
    return require('crypto').createHash('sha256').update(buf).digest('hex').slice(0, 12);
  } catch (e) {
    return '';
  }
}

async function main() {
  const pages = listPages();
  const browser = await _chromium().launch();
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
  // W1285：未稳定行（采集时页面尚未渲染 ⇒ 该行结果不可信 ⇒ 可能静默漏检）
  const unstableRows = rows.filter((r) => r.unstable);
  // W1285：empty 行 = 采集时刻判定面为空（无 svg 文字）⇒ 不判红，但报告里显式可见。
  const emptyRows = rows.filter((r) => r.empty);
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
  // W1284：全量页面内容哈希（防漂移锚点·与第 82 槽渲染档案同款机制）。
  // 记录**每一页**（含无违例的页）⇒ 页面一改而探针未重跑 ⇒ 门禁能发现报告陈旧 ⇒ fail-closed。
  const pageShaMap = {};
  for (const r of rows) {
    if (r.sha && !pageShaMap[r.page]) pageShaMap[r.page] = r.sha;
  }
  const report = {
    generated_at: new Date().toISOString(),
    threshold: THRESHOLD,
    scope: SCOPE,
    bg_mode: BG_MODE,
    no_tool: NO_TOOL,
    only_pages: ONLY_PAGES || null,
    states: STATES.map((s) => s.id),
    pages_scanned: pages.length,
    rows: rows.length,
    fatal_rows: fatals.length,
    // W1285：不稳定行数（>0 ⇒ 判定面不完整 ⇒ 门禁须 fail-closed 拒绝通过）
    unstable_rows: unstableRows.length,
    unstable_detail: unstableRows.slice(0, 20).map((r) => ({
      page: r.page, state: r.state, reason: r.unstableReason || '', textCount: r.svgTextCount,
      // W1285（F1）：未稳定行**也要留下可核查的数据**——此前该行完全不进报告
      //   ⇒ 门禁读到的是结构性不完整的报告（且这些行恰是最可能漏检的）。
      sample: (r.items || []).slice(0, 3).map((x) => ({
        text: x.text, fill: x.fill, bg: x.bg, cr: x.cr, bg_source: x.bg_source,
      })),
    })),
    pages_unstable: Object.keys(unstableRows.reduce((acc, r) => { acc[r.page] = 1; return acc; }, {})).length,
    empty_rows: emptyRows.length,
    empty_detail: emptyRows.slice(0, 20).map((r) => ({ page: r.page, state: r.state, reason: r.unstableReason || '' })),
    violations: violations,
    pages_with_violations: Object.keys(summary).length,
    page_sha: pageShaMap,
    by_page: summary,
  };
  fs.mkdirSync(path.dirname(OUT), { recursive: true });
  fs.writeFileSync(OUT, JSON.stringify(report, null, 1), 'utf8');
  console.log(
    '完成：页面 ' + pages.length + ' · 行 ' + rows.length + ' · 低对比 ' + violations + ' 处 · 违例页 ' +
      Object.keys(summary).length + ' · fatal ' + fatals.length + ' · 不稳定 ' + unstableRows.length + ' → ' + path.relative(ROOT, OUT)
  );
  // W1285 fail-closed：存在未稳定行 ⇒ 判定面不完整 ⇒ 拒绝产出「看起来干净」的产物
  if (unstableRows.length) {
    console.error('FAIL 存在未稳定行（' + unstableRows.length + '/' + rows.length + '）——采集未达稳定态·判定面不完整·非零退出');
    for (const r of unstableRows.slice(0, 10)) {
      console.error('  ✗ ' + r.page + ' ' + r.state + ' ' + (r.unstableReason || ''));
    }
    process.exit(4);
  }
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
  effectiveFill: effectiveFill,
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
  isStableState: isStableState,
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
